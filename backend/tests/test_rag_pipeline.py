"""
Unit and integration test suite for Query Mind.
Tests loader, chunker, preprocessor, TF-IDF, Qdrant index, hybrid retriever, and API.
"""

import pytest
from pathlib import Path
from unittest.mock import patch

from backend.ingestion.loader import LoadedDocument, detect_language, detect_topic
from backend.ingestion.chunker import Chunk, chunk_by_markdown_sections, chunk_sliding_window
from backend.ingestion.preprocessor import code_aware_tokenize
from backend.indexing.tfidf_index import TfidfIndex
from backend.indexing.qdrant_index import QdrantIndex
from backend.retrieval.web_search import format_web_context, search_web
from backend.generation.prompts import build_generation_prompt


def test_detect_language():
    assert detect_language(".py", "script.py", "def foo(): pass") == "python"
    assert detect_language(".js", "app.js", "const x = 1;") == "javascript"
    assert detect_language(".md", "doc.md", "```python\nprint(1)\n```") == "python"
    assert detect_language(".txt", "notes.txt", "just plain text") == "text"


def test_detect_topic():
    assert detect_topic("algorithms_complexity.md", "Big-O notation") == "complexity"
    assert detect_topic("python_dsa.md", "Binary search algorithm") == "algorithms"
    assert detect_topic("javascript_async.md", "Promise and async/await") == "concurrency"


def test_code_aware_tokenize():
    tokens = code_aware_tokenize("binarySearch(arr, target) def quick_sort():")
    assert "binarysearch" in tokens or "binary" in tokens
    assert "target" in tokens
    assert "quick_sort" in tokens or "quick" in tokens


def test_chunker_markdown_sections():
    doc = LoadedDocument(
        doc_id="test_doc",
        source="test.md",
        filename="test.md",
        content="""# Title

## Binary Search
Binary search runs in O(log N) time.

```python
def binary_search(arr, x):
    pass
```

## Linear Search
Linear search runs in O(N) time.
""",
        language="python",
        topic="algorithms",
    )
    chunks = chunk_by_markdown_sections(doc)
    assert len(chunks) >= 2
    assert any("Binary Search" in c.section for c in chunks)
    assert any(c.has_code for c in chunks)


def test_tfidf_indexing_and_search():
    chunks = [
        Chunk(
            chunk_id="c1",
            doc_id="d1",
            filename="algo.md",
            section="Binary Search",
            text="Binary search has time complexity O(log N) on sorted arrays.",
            language="python",
            topic="algorithms",
        ),
        Chunk(
            chunk_id="c2",
            doc_id="d2",
            filename="async.md",
            section="JavaScript Async",
            text="Promises and async await handle asynchronous operations in JavaScript.",
            language="javascript",
            topic="concurrency",
        ),
    ]

    index = TfidfIndex()
    index.build(chunks)
    assert index.vectorizer is not None

    results = index.search("binary search complexity", top_k=2)
    assert len(results) > 0
    top_chunk, score = results[0]
    assert top_chunk.chunk_id == "c1"
    assert score > 0.0


def test_qdrant_local_indexing_and_search():
    index = QdrantIndex(collection_name="test_collection_memory", local_path="data/test_qdrant")
    chunks = [
        Chunk(
            chunk_id="c101",
            doc_id="d1",
            filename="binary_search.md",
            section="Complexity",
            text="Binary search divides search interval in half. Worst-case logarithmic time complexity.",
        ),
        Chunk(
            chunk_id="c102",
            doc_id="d2",
            filename="bubble_sort.md",
            section="Complexity",
            text="Bubble sort repeatedly steps through list. Worst-case quadratic time complexity.",
        ),
    ]
    index.clear()
    indexed = index.index_chunks(chunks)
    assert indexed == 2

    results = index.search("logarithmic search time", top_k=2)
    assert len(results) > 0
    assert results[0][0].chunk_id == "c101"
    assert results[0][1] > 0.40


def test_format_web_context():
    web_res = [
        {"title": "Rust 1.85 Released", "href": "https://rust-lang.org", "body": "Rust 1.85 is now stable."}
    ]
    formatted = format_web_context(web_res)
    assert "[1] Rust 1.85 Released" in formatted
    assert "https://rust-lang.org" in formatted


def test_search_web_normalizes_ddgs_results():
    with patch("ddgs.DDGS") as ddgs_class:
        ddgs = ddgs_class.return_value.__enter__.return_value
        ddgs.text.return_value = [
            {"title": "Rust release", "href": " https://rust-lang.org ", "body": " New features "},
            {"title": "", "href": "", "body": ""},
        ]

        results = search_web(" Rust 1.85 ", max_results=2)

    ddgs_class.assert_called_once_with(timeout=10)
    ddgs.text.assert_called_once_with("Rust 1.85", max_results=2)
    assert results == [
        {
            "title": "Rust release",
            "href": "https://rust-lang.org",
            "body": "New features",
        }
    ]


def test_search_web_surfaces_provider_errors():
    with patch("ddgs.DDGS") as ddgs_class:
        ddgs_class.side_effect = OSError("network unavailable")

        with pytest.raises(RuntimeError, match="DuckDuckGo web search failed"):
            search_web("Rust 1.85")


def test_prompt_builder():
    prompt = build_generation_prompt(
        query="Explain quicksort",
        context="Quicksort is divide and conquer algorithm.",
        source_type="local",
    )
    assert "Explain quicksort" in prompt
    assert "Quicksort is divide and conquer" in prompt
    assert "Local Knowledge Base" in prompt
