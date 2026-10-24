"""
Multi-format Document Loader for Ingestion Pipeline.
Loads Markdown, Plain Text, Python, JavaScript, and PDF files from disk.
"""

import os
import hashlib
from pathlib import Path
from typing import List, Dict, Any, Optional

try:
    from pypdf import PdfReader
    HAS_PYPDF = True
except ImportError:
    HAS_PYPDF = False


class LoadedDocument:
    def __init__(self, doc_id: str, source: str, filename: str, content: str, language: str, topic: str):
        self.doc_id = doc_id
        self.source = source
        self.filename = filename
        self.content = content
        self.language = language
        self.topic = topic

    def to_dict(self) -> Dict[str, Any]:
        return {
            "doc_id": self.doc_id,
            "source": self.source,
            "filename": self.filename,
            "content": self.content,
            "language": self.language,
            "topic": self.topic,
        }


def detect_language(ext: str, filename: str, content: str) -> str:
    ext = ext.lower()
    fname = filename.lower()
    content_lower = content[:1500].lower()

    if ext == ".py" or "python" in fname:
        return "python"
    elif ext in [".js", ".jsx", ".mjs"] or ("javascript" in fname and "java" not in fname):
        return "javascript"
    elif ext in [".ts", ".tsx"] or "typescript" in fname:
        return "typescript"
    elif ext == ".java" or ("java" in fname and "javascript" not in fname):
        return "java"
    elif ext in [".cpp", ".cc", ".cxx", ".hpp"] or "cpp" in fname or "c++" in fname or "cplusplus" in fname:
        return "cpp"
    elif ext in [".c", ".h"] or "c_fundamentals" in fname or "c_basics" in fname:
        return "c"
    elif ext in [".html", ".htm"] or "html" in fname:
        return "html"
    elif ext == ".css" or "css" in fname:
        return "css"
    elif ext in [".md", ".markdown"]:
        # Inspect content for language hints
        if "```python" in content:
            return "python"
        elif "```javascript" in content or "```js" in content:
            return "javascript"
        elif "```java" in content:
            return "java"
        elif "```cpp" in content or "```c++" in content:
            return "cpp"
        elif "```c\n" in content or "```c " in content:
            return "c"
        elif "```html" in content:
            return "html"
        elif "```css" in content:
            return "css"
        return "markdown"
    return "text"


def detect_topic(filename: str, content: str) -> str:
    fname_lower = filename.lower()
    content_lower = content[:500].lower()
    
    if "complexity" in fname_lower or "big-o" in content_lower:
        return "complexity"
    elif "dsa" in fname_lower or "algorithm" in fname_lower or "search" in fname_lower or "sort" in fname_lower:
        return "algorithms"
    elif "async" in fname_lower or "promise" in fname_lower:
        return "concurrency"
    elif "concept" in fname_lower or "syntax" in fname_lower or "fundamental" in fname_lower or "basic" in fname_lower:
        return "language-features"
    elif "oop" in fname_lower or "object" in fname_lower:
        return "oop"
    return "general"


def load_file(file_path: str | Path) -> Optional[LoadedDocument]:
    path = Path(file_path)
    if not path.is_file():
        return None

    filename = path.name
    ext = path.suffix.lower()
    content = ""

    if ext == ".pdf":
        if not HAS_PYPDF:
            raise ImportError("pypdf is required to read PDF files")
        reader = PdfReader(str(path))
        pages_text = []
        for i, page in enumerate(reader.pages):
            text = page.extract_text()
            if text:
                pages_text.append(f"<!-- Page {i+1} -->\n" + text)
        content = "\n\n".join(pages_text)
    else:
        # Text/Code/Markdown
        try:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
        except UnicodeDecodeError:
            with open(path, "r", encoding="latin-1") as f:
                content = f.read()

    if not content.strip():
        return None

    # Deterministic doc_id derived from filename
    doc_id = "doc_" + hashlib.md5(filename.encode("utf-8")).hexdigest()[:10]
    language = detect_language(ext, filename, content)
    topic = detect_topic(filename, content)

    return LoadedDocument(
        doc_id=doc_id,
        source=str(path.as_posix()),
        filename=filename,
        content=content,
        language=language,
        topic=topic,
    )


def load_directory(dir_path: str | Path) -> List[LoadedDocument]:
    """
    Recursively scans and loads all supported documents in a directory.
    Supported extensions: .md, .txt, .py, .js, .ts, .pdf
    """
    path = Path(dir_path)
    documents = []
    supported_extensions = {
        ".md", ".markdown", ".txt", ".py", ".js", ".ts", ".pdf",
        ".java", ".cpp", ".cc", ".cxx", ".c", ".h", ".hpp",
        ".html", ".htm", ".css"
    }

    if not path.exists():
        return []

    for item in sorted(path.rglob("*")):
        if item.is_file() and item.suffix.lower() in supported_extensions:
            # Skip hidden files or README stubs in raw dir if desired
            if item.name.lower() == "readme.md" and item.parent.name == "raw":
                continue
            doc = load_file(item)
            if doc:
                documents.append(doc)

    return documents
