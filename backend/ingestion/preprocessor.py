"""
Code-Aware Text Preprocessor for Information Retrieval.
Splits text into code vs. prose spans, normalizes whitespace, and provides
sub-tokenization for code identifiers (camelCase, snake_case).
"""

import re
from typing import List, Tuple, Dict, Any


def split_code_and_prose(text: str) -> List[Dict[str, Any]]:
    """
    Identifies and separates fenced code blocks (```lang ... ```) and prose.
    Returns a list of dicts: [{"type": "code"|"prose", "text": str, "lang": str|None}]
    """
    pattern = re.compile(r"```([a-zA-Z0-9_-]*)\n(.*?)```", re.DOTALL)
    spans = []
    last_idx = 0

    for match in pattern.finditer(text):
        start, end = match.span()
        if start > last_idx:
            prose_content = text[last_idx:start].strip()
            if prose_content:
                spans.append({"type": "prose", "text": prose_content, "lang": None})
        
        lang = match.group(1).strip() or None
        code_content = match.group(2).strip()
        if code_content:
            spans.append({"type": "code", "text": code_content, "lang": lang})
        last_idx = end

    if last_idx < len(text):
        remaining = text[last_idx:].strip()
        if remaining:
            spans.append({"type": "prose", "text": remaining, "lang": None})

    return spans


def split_identifier(identifier: str) -> List[str]:
    """
    Splits compound identifiers:
    - snake_case -> ['snake', 'case']
    - camelCase / PascalCase -> ['camel', 'Case']
    - kebab-case -> ['kebab', 'case']
    Also includes the original identifier for exact match lookup.
    """
    # Replace snake_case and kebab-case with spaces
    s = re.sub(r"[_\-]+", " ", identifier)
    # Insert space before capital letters in camelCase / PascalCase
    s = re.sub(r"([a-z0-9])([A-Z])", r"\1 \2", s)
    # Handle acronym sequences like XMLParser -> XML Parser
    s = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1 \2", s)
    tokens = [t.lower() for t in s.split() if t.strip()]
    
    # Return both components and original lowercased identifier
    orig = identifier.lower().replace("_", "").replace("-", "")
    all_tokens = set(tokens)
    if orig and orig not in all_tokens:
        tokens.append(orig)
    return tokens


def code_aware_tokenize(text: str) -> List[str]:
    """
    Tokenizes coding text into normalized terms suitable for lexical retrieval (TF-IDF/BM25).
    Extracts words, splits compound identifiers, handles mathematical notations (O(n), logn).
    """
    if not text:
        return []

    # Extract alphanumeric words and special symbols like O(n) notation
    # Normalize Big-O notation like O(N log N) -> O, N, log, N
    clean_text = re.sub(r"\$O\((.*?)\)\$", r"O \1", text)
    clean_text = re.sub(r"O\((.*?)\)", r"O \1", clean_text)
    
    # Find all identifier-like tokens and words
    raw_tokens = re.findall(r"[a-zA-Z0-9_\-\+\*\/\#]+", clean_text)
    final_tokens: List[str] = []

    for token in raw_tokens:
        token_clean = token.strip(".-")
        if not token_clean or len(token_clean) < 2:
            continue
        
        # Split camelCase / snake_case
        sub_tokens = split_identifier(token_clean)
        final_tokens.extend(sub_tokens)

    return final_tokens
