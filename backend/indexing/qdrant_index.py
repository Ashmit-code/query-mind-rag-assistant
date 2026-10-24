"""
Qdrant Vector Database Integration for Dense Semantic Search.
Supports Qdrant Cloud (via QDRANT_URL + QDRANT_API_KEY) and local file/in-memory fallback.
Uses sentence-transformers/all-MiniLM-L6-v2 (384-dimensional dense embeddings).
"""

import os
import uuid
import logging
from pathlib import Path
from typing import List, Tuple, Optional, Dict, Any
from dotenv import load_dotenv

from qdrant_client import QdrantClient
from qdrant_client.http import models
from sentence_transformers import SentenceTransformer

from backend.ingestion.chunker import Chunk

load_dotenv()

logger = logging.getLogger(__name__)

DEFAULT_COLLECTION = os.getenv("QDRANT_COLLECTION", "ir_mini_collection")
DEFAULT_MODEL = os.getenv("EMBEDDING_MODEL_NAME", "all-MiniLM-L6-v2")
VECTOR_DIMENSION = 384


class QdrantIndex:
    def __init__(
        self,
        collection_name: str = DEFAULT_COLLECTION,
        model_name: str = DEFAULT_MODEL,
        url: Optional[str] = None,
        api_key: Optional[str] = None,
        local_path: Optional[str] = "data/qdrant",
    ):
        self.collection_name = collection_name
        self.model_name = model_name
        self.url = url or os.getenv("QDRANT_URL", "").strip() or None
        self.api_key = api_key or os.getenv("QDRANT_API_KEY", "").strip() or None
        self.local_path = local_path
        
        self._embedder: Optional[SentenceTransformer] = None
        self._client: Optional[QdrantClient] = None
        self._init_client()

    @property
    def embedder(self) -> SentenceTransformer:
        if self._embedder is None:
            logger.info(f"Loading embedding model: {self.model_name}")
            self._embedder = SentenceTransformer(self.model_name)
        return self._embedder

    def _init_client(self):
        """Initializes client connecting to Qdrant Cloud if credentials exist, else local storage."""
        if self.url:
            logger.info(f"Connecting to Qdrant Cloud at {self.url}...")
            self._client = QdrantClient(url=self.url, api_key=self.api_key, timeout=60.0)
        else:
            path = Path(self.local_path) if self.local_path else Path("data/qdrant")
            path.mkdir(parents=True, exist_ok=True)
            logger.info(f"QDRANT_URL not set. Using local persistent storage at {path}")
            self._client = QdrantClient(path=str(path), timeout=60.0)
            
        self._ensure_collection()

    def _ensure_collection(self):
        """Ensure that the vector collection exists with cosine distance."""
        try:
            collections = [c.name for c in self._client.get_collections().collections]
            if self.collection_name not in collections:
                logger.info(f"Creating Qdrant collection: {self.collection_name} (dim={VECTOR_DIMENSION})")
                self._client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=models.VectorParams(
                        size=VECTOR_DIMENSION,
                        distance=models.Distance.COSINE,
                    ),
                )
        except Exception as e:
            logger.error(f"Error ensuring Qdrant collection: {e}")

    def index_chunks(self, chunks: List[Chunk], batch_size: int = 25) -> int:
        """
        Computes dense embeddings for chunks and upserts them into Qdrant.
        """
        if not chunks:
            return 0

        logger.info(f"Encoding {len(chunks)} chunks using {self.model_name}...")
        texts = [f"{c.section}\n{c.text}" for c in chunks]
        embeddings = self.embedder.encode(
            texts,
            show_progress_bar=False,
            normalize_embeddings=True,
        )

        points = []
        for i, (chunk, emb) in enumerate(zip(chunks, embeddings)):
            # Deterministic UUID from chunk_id
            point_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, chunk.chunk_id))
            payload = {
                "chunk_id": chunk.chunk_id,
                "doc_id": chunk.doc_id,
                "filename": chunk.filename,
                "source": chunk.source,
                "text": chunk.text,
                "section": chunk.section,
                "language": chunk.language,
                "topic": chunk.topic,
                "has_code": chunk.has_code,
                "chunk_index": chunk.chunk_index,
                "metadata": chunk.metadata or {},
            }
            points.append(
                models.PointStruct(
                    id=point_id,
                    vector=emb.tolist(),
                    payload=payload,
                )
            )

        # Upsert in batches
        total_indexed = 0
        for i in range(0, len(points), batch_size):
            batch = points[i : i + batch_size]
            self._client.upsert(
                collection_name=self.collection_name,
                points=batch,
            )
            total_indexed += len(batch)

        logger.info(f"Successfully indexed {total_indexed} points in Qdrant.")
        return total_indexed

    def search(self, query: str, top_k: int = 5) -> List[Tuple[Chunk, float]]:
        """
        Executes semantic cosine search on indexed chunks in Qdrant.
        """
        if not query.strip():
            return []

        query_vector = self.embedder.encode(
            query,
            show_progress_bar=False,
            normalize_embeddings=True,
        ).tolist()

        try:
            if hasattr(self._client, "query_points"):
                response = self._client.query_points(
                    collection_name=self.collection_name,
                    query=query_vector,
                    limit=top_k,
                    with_payload=True,
                )
                scored_points = response.points
            else:
                scored_points = self._client.search(
                    collection_name=self.collection_name,
                    query_vector=query_vector,
                    limit=top_k,
                    with_payload=True,
                )

            results: List[Tuple[Chunk, float]] = []
            for hit in scored_points:
                payload = hit.payload or {}
                chunk = Chunk(
                    chunk_id=payload.get("chunk_id", str(hit.id)),
                    doc_id=payload.get("doc_id", "unknown"),
                    source=payload.get("source", ""),
                    filename=payload.get("filename", ""),
                    text=payload.get("text", ""),
                    section=payload.get("section", ""),
                    language=payload.get("language", "text"),
                    topic=payload.get("topic", "general"),
                    has_code=payload.get("has_code", False),
                    chunk_index=payload.get("chunk_index", 0),
                    metadata=payload.get("metadata", {}),
                )
                score = float(hit.score)
                results.append((chunk, score))

            return results
        except Exception as e:
            logger.error(f"Search failed in Qdrant: {e}")
            return []

    def count(self) -> int:
        """Returns the number of points in the collection."""
        try:
            info = self._client.get_collection(self.collection_name)
            return info.points_count or 0
        except Exception as e:
            logger.warning(f"Failed to get collection count: {e}")
            return 0

    def clear(self):
        """Clears all points in the collection."""
        try:
            self._client.delete_collection(self.collection_name)
            self._ensure_collection()
            logger.info(f"Collection {self.collection_name} cleared.")
        except Exception as e:
            logger.error(f"Failed to clear collection: {e}")


# Singleton instance
_qdrant_instance: Optional[QdrantIndex] = None


def get_qdrant_index() -> QdrantIndex:
    global _qdrant_instance
    if _qdrant_instance is None:
        _qdrant_instance = QdrantIndex()
    return _qdrant_instance
