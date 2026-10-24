// API client for the Query Mind backend

export interface QueryRequest {
  query: string;
  mode: 'tfidf' | 'semantic' | 'hybrid';
  top_k?: number;
  allow_web_fallback?: boolean;
  ollama_model?: string;
}

export interface SourceCitation {
  chunk_id: string;
  section: string;
  source: string;
}

export interface RetrievedChunk {
  chunk_id: string;
  doc_id: string;
  score: number;
  rank: number;
  source: string;
  filename: string;
  section: string;
  language: string;
  topic: string;
  text: string;
  has_code: boolean;
}

export interface WebResult {
  title: string;
  href: string;
  body: string;
}

export interface GeneratedResponse {
  query: string;
  answer_markdown: string;
  source_type: 'local' | 'web' | 'none';
  model_used: string;
  local_results: RetrievedChunk[];
  web_results: WebResult[];
  score: number;
}

export interface IngestResponse {
  status: string;
  documents_loaded: number;
  chunks_created: number;
  indices_updated: boolean;
}

export interface KnowledgeStatsResponse {
  raw_files: number;
  qdrant_points: number;
  tfidf_terms: number;
  qdrant_target: string;
}

export interface OllamaStatusResponse {
  running: boolean;
  message: string;
}

export interface OllamaModelsResponse {
  models: string[];
  error?: string;
}

const BASE_URL = 'http://127.0.0.1:8000';

async function request<T>(path: string, options?: RequestInit, signal?: AbortSignal): Promise<T> {
  const res = await fetch(`${BASE_URL}${path}`, {
    headers: { 'Content-Type': 'application/json' },
    signal,
    ...options,
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(err.detail || `HTTP ${res.status}`);
  }
  return res.json();
}

export const api = {
  health: () => request<{ status: string; qdrant_mode: string; qdrant_points: number }>('/health'),

  stats: () => request<KnowledgeStatsResponse>('/knowledge/stats'),

  query: (req: QueryRequest, signal?: AbortSignal) =>
    request<GeneratedResponse>('/query', {
      method: 'POST',
      body: JSON.stringify(req),
    }, signal),

  /** Re-ingest all documents in data/raw */
  ingest: () => request<IngestResponse>('/ingest', { method: 'POST' }),

  /** Upload a file and ingest it into the knowledge base */
  ingestFile: async (file: File): Promise<IngestResponse> => {
    const form = new FormData();
    form.append('file', file);
    const res = await fetch(`${BASE_URL}/ingest/file`, { method: 'POST', body: form });
    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: res.statusText }));
      throw new Error(err.detail || `HTTP ${res.status}`);
    }
    return res.json();
  },

  /** Ingest a document from a public URL */
  ingestUrl: (url: string) =>
    request<IngestResponse>('/ingest/url', {
      method: 'POST',
      body: JSON.stringify({ url }),
    }),

  /** Check if Ollama is running */
  ollamaStatus: () => request<OllamaStatusResponse>('/ollama/status'),

  /** List locally available Ollama models */
  ollamaModels: () => request<OllamaModelsResponse>('/ollama/models'),
};
