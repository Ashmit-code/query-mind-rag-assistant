# Retrieval Module

Implements:
- TF-IDF Cosine similarity retrieval.
- Dense Embedding Cosine/ANN similarity retrieval.
- Hybrid scorer combining lexical and semantic scores (`score = α * tfidf + (1 - α) * semantic`).
- Top-K ranking and candidate selection.
