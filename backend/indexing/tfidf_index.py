"""
TF-IDF Inverted Index Module for Lexical Information Retrieval.
Uses scikit-learn TfidfVectorizer with code-aware tokenization, supporting
persistence to disk and cosine similarity query scoring.
"""

import pickle
from pathlib import Path
from typing import List, Tuple, Dict, Any, Optional
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from backend.ingestion.preprocessor import code_aware_tokenize
from backend.ingestion.chunker import Chunk


class TfidfIndex:
    def __init__(self):
        self.vectorizer: Optional[TfidfVectorizer] = None
        self.tfidf_matrix = None
        self.chunk_ids: List[str] = []
        self.chunks_by_id: Dict[str, Chunk] = {}

    def build(self, chunks: List[Chunk]):
        self.chunk_ids = [c.chunk_id for c in chunks]
        self.chunks_by_id = {c.chunk_id: c for c in chunks}
        corpus_texts = [f"{c.section}\n{c.text}" for c in chunks]

        self.vectorizer = TfidfVectorizer(
            tokenizer=code_aware_tokenize,
            token_pattern=None,
            lowercase=True,
            sublinear_tf=True,
            norm="l2",
        )
        self.tfidf_matrix = self.vectorizer.fit_transform(corpus_texts)

    def save(self, index_dir: str | Path):
        path = Path(index_dir)
        path.mkdir(parents=True, exist_ok=True)

        data = {
            "vectorizer": self.vectorizer,
            "tfidf_matrix": self.tfidf_matrix,
            "chunk_ids": self.chunk_ids,
            "chunks_by_id": {cid: c.to_dict() for cid, c in self.chunks_by_id.items()},
        }
        with open(path / "tfidf_index.pkl", "wb") as f:
            pickle.dump(data, f)

    def load(self, index_dir: str | Path) -> bool:
        path = Path(index_dir) / "tfidf_index.pkl"
        if not path.exists():
            return False

        with open(path, "rb") as f:
            data = pickle.load(f)

        self.vectorizer = data["vectorizer"]
        self.tfidf_matrix = data["tfidf_matrix"]
        self.chunk_ids = data["chunk_ids"]
        self.chunks_by_id = {cid: Chunk.from_dict(cdict) for cid, cdict in data["chunks_by_id"].items()}
        return True

    def search(self, query: str, top_k: int = 5) -> List[Tuple[Chunk, float]]:
        """
        Executes lexical cosine similarity search against indexed chunks.
        Returns sorted list of (Chunk, score).
        """
        if self.vectorizer is None or self.tfidf_matrix is None:
            raise RuntimeError("TF-IDF Index is not built or loaded.")

        query_vec = self.vectorizer.transform([query])
        # Compute cosine similarity (dot product of L2-normalized vectors)
        scores = cosine_similarity(query_vec, self.tfidf_matrix).flatten()

        top_indices = np.argsort(scores)[::-1][:top_k]
        results = []
        for idx in top_indices:
            score = float(scores[idx])
            if score > 0.0:  # Only return matches with positive lexical overlap
                chunk_id = self.chunk_ids[idx]
                results.append((self.chunks_by_id[chunk_id], score))

        return results


# Global singleton instance
_tfidf_instance: Optional[TfidfIndex] = None


def get_tfidf_index() -> TfidfIndex:
    global _tfidf_instance
    if _tfidf_instance is None:
        _tfidf_instance = TfidfIndex()
    return _tfidf_instance


def build_and_save_tfidf(chunks: List[Chunk], index_dir: str | Path = "data/indices") -> TfidfIndex:
    idx = get_tfidf_index()
    idx.build(chunks)
    idx.save(index_dir)
    return idx
