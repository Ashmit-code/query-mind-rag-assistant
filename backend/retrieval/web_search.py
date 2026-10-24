"""
DuckDuckGo Web Search Fallback Module.
Performs live internet search when knowledge base similarity scores fall below confidence thresholds.
"""

import logging
from typing import List, Dict

logger = logging.getLogger(__name__)


def search_web(query: str, max_results: int = 4) -> List[Dict[str, str]]:
    """
    Searches the web via DuckDuckGo and returns list of results:
    [{'title': '...', 'href': '...', 'body': '...'}]
    """
    clean_query = query.strip()
    if not clean_query:
        return []

    try:
        from ddgs import DDGS
        with DDGS(timeout=10) as ddgs:
            raw_results = ddgs.text(clean_query, max_results=max_results)
            results = []
            for result in raw_results:
                title = result.get("title", "").strip()
                link = (result.get("href") or result.get("link", "")).strip()
                snippet = (result.get("body") or result.get("snippet", "")).strip()
                if title or link or snippet:
                    results.append({"title": title, "href": link, "body": snippet})
        return results
    except Exception as exc:
        logger.exception("DuckDuckGo web search failed")
        raise RuntimeError(f"DuckDuckGo web search failed: {exc}") from exc


def format_web_context(results: List[Dict[str, str]]) -> str:
    """
    Formats web results into a concise text block for LLM prompting.
    """
    if not results:
        return ""

    blocks = []
    for i, res in enumerate(results, 1):
        title = res.get("title", "Web Source")
        link = res.get("href", "")
        body = res.get("body", "")
        blocks.append(f"[{i}] {title} ({link})\n{body}")

    return "\n\n".join(blocks)
