"""
Ollama-Driven Answer Generation Module.
Synthesizes strictly grounded Markdown answers from local or web contexts.
Includes strict anti-hallucination guards.
"""

import os
import logging
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
import requests

from backend.retrieval.retriever import UnifiedSearchResult, RetrievalResult
from backend.generation.prompts import GROUNDING_SYSTEM_INSTRUCTION, build_generation_prompt

logger = logging.getLogger(__name__)

DEFAULT_OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://127.0.0.1:11434")
DEFAULT_OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2:latest")


class GeneratedResponse(BaseModel):
    query: str
    answer_markdown: str
    source_type: str  # 'local' | 'web' | 'none'
    model_used: str
    local_results: List[RetrievalResult] = []
    web_results: List[Dict[str, str]] = []
    score: float = 0.0


def _call_ollama(prompt: str, model_name: str, host: str = DEFAULT_OLLAMA_HOST) -> Optional[str]:
    """Calls Ollama generate endpoint."""
    url = f"{host.rstrip('/')}/api/generate"
    payload = {
        "model": model_name,
        "prompt": f"{GROUNDING_SYSTEM_INSTRUCTION}\n\n{prompt}",
        "stream": False,
        "options": {
            "temperature": 0.2,
            "top_p": 0.9,
            "num_predict": 1024,
        },
    }
    try:
        resp = requests.post(url, json=payload, timeout=60)
        if resp.status_code == 200:
            data = resp.json()
            return data.get("response", "").strip()
        else:
            logger.warning(f"Ollama returned status {resp.status_code}: {resp.text}")
    except Exception as e:
        logger.error(f"Failed to communicate with Ollama at {url}: {e}")
    return None


def _fallback_deterministic_markdown(search_result: UnifiedSearchResult) -> str:
    """Fast deterministic synthesis if Ollama is unreachable."""
    if search_result.source_type == "web" and search_result.web_results:
        parts = ["### Web Search Findings\n"]
        for res in search_result.web_results:
            title = res.get("title", "Web Result")
            href = res.get("href", "#")
            snippet = res.get("body", "")
            parts.append(f"- **[{title}]({href})**\n  > {snippet}\n")
        return "\n".join(parts)

    if search_result.source_type == "local" and search_result.local_results:
        top = search_result.local_results[0]
        parts = [
            f"### Retrieved from {top.filename} ({top.section})\n",
            top.text,
            "\n\n#### Additional Sources:",
        ]
        for c in search_result.local_results[1:3]:
            parts.append(f"- `{c.filename}` > **{c.section}** (Relevance: {c.score:.2f})")
        return "\n".join(parts)

    return "No relevant information found in the knowledge base or web search."


def generate_answer(
    search_result: UnifiedSearchResult,
    model_name: Optional[str] = None,
    ollama_host: Optional[str] = None,
) -> GeneratedResponse:
    """
    Synthesizes grounded markdown response for the query using Ollama.
    """
    query = search_result.query
    source_type = search_result.source_type
    model = model_name or os.getenv("OLLAMA_MODEL", DEFAULT_OLLAMA_MODEL)
    host = ollama_host or os.getenv("OLLAMA_HOST", DEFAULT_OLLAMA_HOST)

    # If no relevant context found from either local or web:
    if source_type == "none" or not search_result.formatted_context.strip():
        return GeneratedResponse(
            query=query,
            answer_markdown="I could not find sufficiently relevant information in the local knowledge base or via web search to answer your question accurately.",
            source_type="none",
            model_used="guardrail",
            local_results=[],
            web_results=[],
            score=0.0,
        )

    # Prepare grounded prompt
    prompt = build_generation_prompt(
        query=query,
        context=search_result.formatted_context,
        source_type=source_type,
    )

    # Call Ollama
    answer_text = _call_ollama(prompt, model_name=model, host=host)

    if not answer_text:
        logger.warning("Ollama unavailable or failed; using deterministic fallback formatting.")
        answer_text = _fallback_deterministic_markdown(search_result)
        model_used = "fallback-extractor"
    else:
        model_used = f"ollama/{model}"

    return GeneratedResponse(
        query=query,
        answer_markdown=answer_text,
        source_type=source_type,
        model_used=model_used,
        local_results=search_result.local_results,
        web_results=search_result.web_results,
        score=search_result.max_score,
    )
