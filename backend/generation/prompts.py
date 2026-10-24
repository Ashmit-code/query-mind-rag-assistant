"""
Prompt templates for grounded generation with local knowledge base or web search.
Produces clean markdown responses with strict anti-hallucination constraints.
"""

GROUNDING_SYSTEM_INSTRUCTION = """You are an expert Information Retrieval & Coding Assistant.
Your task is to provide an accurate, high-quality, and concise answer based STRICTLY and ONLY on the provided Context.

RULES:
1. Ground your response entirely on the provided Context.
2. DO NOT make up claims, syntax, parameters, or behaviors not supported by the Context.
3. If the Context is from the local knowledge base, explain the concept, provide relevant code snippets, and cite the document section.
4. If the Context is from Web Search, clearly mention what the search found and cite the source links.
5. If the Context is insufficient to answer the question, clearly state: "The provided context does not contain enough information to answer this question accurately."
6. Format your answer using clean GitHub-flavored Markdown (headings, bullet points, fenced code blocks with language identifiers).
"""


def build_generation_prompt(query: str, context: str, source_type: str = "local") -> str:
    source_label = "Local Knowledge Base" if source_type == "local" else "Live Web Search Results"
    return f"""Context ({source_label}):
{context}

User Question:
{query}

Provide a comprehensive, strictly grounded answer in clean markdown:"""
