"""
Chunking and Metadata Retention Module.
Segments documents by section/headings or sliding window, preserving
traceable citations (doc_id, chunk_id, section, language, topic, has_code).
"""

import re
import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from backend.ingestion.loader import LoadedDocument


class Chunk:
    def __init__(
        self,
        chunk_id: str,
        doc_id: str,
        source: str = "",
        filename: str = "",
        section: str = "General",
        language: str = "text",
        topic: str = "general",
        text: str = "",
        has_code: bool = False,
        chunk_index: int = 0,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        self.chunk_id = chunk_id
        self.doc_id = doc_id
        self.source = source
        self.filename = filename
        self.section = section
        self.language = language
        self.topic = topic
        self.text = text
        self.has_code = has_code
        self.chunk_index = chunk_index
        self.metadata = metadata or {}

    def to_dict(self) -> Dict[str, Any]:
        return {
            "chunk_id": self.chunk_id,
            "doc_id": self.doc_id,
            "source": self.source,
            "filename": self.filename,
            "section": self.section,
            "language": self.language,
            "topic": self.topic,
            "text": self.text,
            "has_code": self.has_code,
            "chunk_index": self.chunk_index,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Chunk":
        return cls(
            chunk_id=data["chunk_id"],
            doc_id=data["doc_id"],
            source=data.get("source", ""),
            filename=data.get("filename", ""),
            section=data.get("section", "General"),
            language=data.get("language", "text"),
            topic=data.get("topic", "general"),
            text=data.get("text", ""),
            has_code=data.get("has_code", False),
            chunk_index=data.get("chunk_index", 0),
            metadata=data.get("metadata", {}),
        )


def chunk_by_markdown_sections(doc: LoadedDocument) -> List[Chunk]:
    """
    Splits markdown documents into semantically coherent chunks based on headings (##, ###).
    """
    lines = doc.content.split("\n")
    sections: List[Dict[str, Any]] = []
    current_heading = "Introduction"
    current_lines: List[str] = []

    heading_regex = re.compile(r"^(#{1,3})\s+(.+)$")

    for line in lines:
        match = heading_regex.match(line)
        if match:
            if current_lines:
                text = "\n".join(current_lines).strip()
                if text:
                    sections.append({"section": current_heading, "text": text})
            current_heading = match.group(2).strip()
            current_lines = [line]
        else:
            current_lines.append(line)

    if current_lines:
        text = "\n".join(current_lines).strip()
        if text:
            sections.append({"section": current_heading, "text": text})

    # If document has no headings or resulted in only 1 large section, fall back to sliding window
    if not sections or (len(sections) == 1 and len(sections[0]["text"].split()) > 400):
        return chunk_sliding_window(doc, max_words=350, overlap=50)

    chunks: List[Chunk] = []
    chunk_index = 1
    for sec in sections:
        sec_text = sec["text"]
        has_code = (
            "```" in sec_text
            or "def " in sec_text
            or "function " in sec_text
            or "const " in sec_text
            or "class " in sec_text
            or "public " in sec_text
            or "#include " in sec_text
            or "void " in sec_text
            or "struct " in sec_text
            or "<div" in sec_text
            or "<html" in sec_text
            or "display:" in sec_text
        )
        
        # If an individual section is exceedingly long, sub-chunk it
        words = sec_text.split()
        if len(words) > 500:
            sub_chunks = chunk_text_sliding(sec_text, max_words=350, overlap=50)
            for sub_idx, sub_text in enumerate(sub_chunks):
                chunk_id = f"{doc.doc_id}_c{chunk_index:03d}"
                chunks.append(
                    Chunk(
                        chunk_id=chunk_id,
                        doc_id=doc.doc_id,
                        source=doc.source,
                        filename=doc.filename,
                        section=f"{sec['section']} (Part {sub_idx+1})",
                        language=doc.language,
                        topic=doc.topic,
                        text=sub_text,
                        has_code="```" in sub_text,
                    )
                )
                chunk_index += 1
        else:
            chunk_id = f"{doc.doc_id}_c{chunk_index:03d}"
            chunks.append(
                Chunk(
                    chunk_id=chunk_id,
                    doc_id=doc.doc_id,
                    source=doc.source,
                    filename=doc.filename,
                    section=sec["section"],
                    language=doc.language,
                    topic=doc.topic,
                    text=sec_text,
                    has_code=has_code,
                )
            )
            chunk_index += 1

    return chunks


def chunk_text_sliding(text: str, max_words: int = 350, overlap: int = 50) -> List[str]:
    words = text.split()
    if len(words) <= max_words:
        return [text]

    chunks = []
    step = max_words - overlap
    for i in range(0, len(words), step):
        chunk_words = words[i : i + max_words]
        if chunk_words:
            chunks.append(" ".join(chunk_words))
        if i + max_words >= len(words):
            break
    return chunks


def chunk_sliding_window(doc: LoadedDocument, max_words: int = 350, overlap: int = 50) -> List[Chunk]:
    text_chunks = chunk_text_sliding(doc.content, max_words=max_words, overlap=overlap)
    chunks: List[Chunk] = []

    for idx, text in enumerate(text_chunks):
        chunk_id = f"{doc.doc_id}_c{idx+1:03d}"
        has_code = "```" in text or "def " in text or "function " in text
        chunks.append(
            Chunk(
                chunk_id=chunk_id,
                doc_id=doc.doc_id,
                source=doc.source,
                filename=doc.filename,
                section=f"Section {idx+1}",
                language=doc.language,
                topic=doc.topic,
                text=text,
                has_code=has_code,
            )
        )

    return chunks


def process_and_save_chunks(documents: List[LoadedDocument], output_path: str | Path) -> List[Chunk]:
    all_chunks: List[Chunk] = []
    for doc in documents:
        if doc.filename.endswith(".md") or doc.filename.endswith(".markdown"):
            doc_chunks = chunk_by_markdown_sections(doc)
        else:
            doc_chunks = chunk_sliding_window(doc)
        all_chunks.extend(doc_chunks)

    out_file = Path(output_path)
    out_file.parent.mkdir(parents=True, exist_ok=True)
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump([c.to_dict() for c in all_chunks], f, indent=2)

    return all_chunks


def load_saved_chunks(chunks_path: str | Path) -> List[Chunk]:
    path = Path(chunks_path)
    if not path.exists():
        return []
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return [Chunk.from_dict(item) for item in data]
