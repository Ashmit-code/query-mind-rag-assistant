import { useState, useEffect, useCallback } from 'react';
import { Send, Square, ChevronDown, SlidersHorizontal, Cpu, RefreshCw } from 'lucide-react';
import { api } from '../api/client';

type Mode = 'hybrid' | 'semantic' | 'tfidf';

interface Props {
  loading: boolean;
  onSubmit: (query: string, mode: Mode, topK: number, alpha: number) => void;
  onStop: () => void;
  ollamaModel: string;
  onModelChange: (model: string) => void;
}

const MODES: { id: Mode; label: string; desc: string }[] = [
  { id: 'hybrid', label: 'Hybrid', desc: 'Weighted blend of vector and keyword search' },
  { id: 'semantic', label: 'Dense', desc: 'Semantic embedding vector retrieval' },
  { id: 'tfidf', label: 'TF-IDF', desc: 'Exact keyword / lexical retrieval' },
];

export default function QueryInput({ loading, onSubmit, onStop, ollamaModel, onModelChange }: Props) {
  const [query, setQuery] = useState('');
  const [mode, setMode] = useState<Mode>('hybrid');
  const [topK, setTopK] = useState(5);
  const [alpha, setAlpha] = useState(0.5);
  const [showAdvanced, setShowAdvanced] = useState(false);
  const [ollamaModels, setOllamaModels] = useState<string[]>([]);
  const [ollamaOnline, setOllamaOnline] = useState<boolean | null>(null);
  const [probing, setProbing] = useState(false);

  // Probe Ollama status
  const probeOllama = useCallback(async () => {
    setProbing(true);
    try {
      const s = await api.ollamaStatus();
      setOllamaOnline(s.running);
      if (s.running) {
        const r = await api.ollamaModels();
        const models = r.models || [];
        setOllamaModels(models);
        if (models.length && !ollamaModel) {
          onModelChange(models[0]);
        }
      } else {
        setOllamaModels([]);
      }
    } catch {
      setOllamaOnline(false);
      setOllamaModels([]);
    } finally {
      setProbing(false);
    }
  }, [ollamaModel, onModelChange]);

  useEffect(() => {
    probeOllama();
    const id = setInterval(probeOllama, 30_000);
    return () => clearInterval(id);
  }, []); // eslint-disable-line

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim() || loading) return;
    const q = query.trim();
    setQuery('');
    onSubmit(q, mode, topK, alpha);
  };

  return (
    <div className="w-full space-y-3">
      <form onSubmit={handleSubmit} className="space-y-2.5">
        {/* Main Textarea Dock */}
        <div className="relative group rounded-xl transition-all duration-200">
          <textarea
            id="query-input"
            value={query}
            onChange={e => setQuery(e.target.value)}
            onKeyDown={e => {
              if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                handleSubmit(e as any);
              }
            }}
            placeholder="Ask about syntax, algorithms, data structures, loops, classes… (Enter to send)"
            rows={2}
            disabled={loading}
            className="glass-input w-full rounded-xl px-4 py-3 pr-14 text-sm resize-none leading-relaxed disabled:opacity-50 transition-all duration-200"
          />

          {/* Action button (Send or Stop) */}
          {loading ? (
            <button
              type="button"
              onClick={onStop}
              className="absolute bottom-3 right-3 p-2.5 rounded-xl bg-red-500/10 border border-red-500/30 text-red-500 hover:bg-red-500/20 active:scale-95 transition-all duration-150"
              aria-label="Stop generation"
              title="Stop generation"
            >
              <Square className="w-4 h-4 fill-current" />
            </button>
          ) : (
            <button
              type="submit"
              disabled={!query.trim()}
              className="btn-accent absolute bottom-3 right-3 p-2.5 rounded-xl active:scale-95 transition-transform"
              aria-label="Send query"
            >
              <Send className="w-4 h-4" />
            </button>
          )}
        </div>

        {/* Controls Row */}
        <div className="flex items-center justify-between gap-3 flex-wrap">
          {/* Segmented Mode Pill Control */}
          <div
            role="radiogroup"
            aria-label="Retrieval Mode"
            className="inline-flex items-center p-1 rounded-xl glass border border-border-subtle"
          >
            {MODES.map(m => {
              const active = mode === m.id;
              return (
                <button
                  key={m.id}
                  type="button"
                  role="radio"
                  aria-checked={active}
                  onClick={() => setMode(m.id)}
                  title={m.desc}
                  className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-all duration-150 ${
                    active
                      ? 'btn-accent text-white shadow-sm'
                      : 'text-text-secondary hover:text-text-primary hover:bg-bg-surface-hover'
                  }`}
                >
                  {m.label}
                </button>
              );
            })}
          </div>

          {/* Right Status & Advanced Controls */}
          <div className="flex items-center gap-2">
            {/* Ollama Status & Model Selector */}
            <div className="flex items-center gap-1">
              {ollamaOnline && ollamaModels.length > 0 ? (
                <div className="flex items-center gap-1.5 glass px-2.5 py-1.5 rounded-xl text-xs border border-border-subtle">
                  <Cpu className="w-3.5 h-3.5 text-accent" />
                  <select
                    value={ollamaModel}
                    onChange={e => onModelChange(e.target.value)}
                    className="bg-transparent text-text-secondary hover:text-text-primary outline-none cursor-pointer text-xs max-w-[120px]"
                    title="Ollama local model"
                  >
                    {ollamaModels.map(m => (
                      <option key={m} value={m} className="bg-bg-surface text-text-primary">
                        {m}
                      </option>
                    ))}
                  </select>
                </div>
              ) : ollamaOnline === false ? (
                <span className="text-[11px] text-amber-500/80 px-2.5 py-1 glass rounded-lg border border-border-subtle">
                  Ollama offline
                </span>
              ) : (
                <span className="text-[11px] text-text-muted px-2.5 py-1 glass rounded-lg border border-border-subtle animate-pulse">
                  Checking…
                </span>
              )}

              {/* Refresh Button */}
              <button
                type="button"
                onClick={probeOllama}
                disabled={probing}
                title="Refresh Ollama status"
                className="btn-ghost p-1.5 rounded-lg disabled:opacity-40"
                aria-label="Refresh Ollama"
              >
                <RefreshCw className={`w-3.5 h-3.5 ${probing ? 'animate-spin' : ''}`} />
              </button>
            </div>

            {/* Advanced Toggle */}
            <button
              type="button"
              onClick={() => setShowAdvanced(s => !s)}
              className="btn-ghost flex items-center gap-1.5 text-xs px-2.5 py-1.5 rounded-xl"
              aria-label="Toggle advanced settings"
            >
              <SlidersHorizontal className="w-3.5 h-3.5" />
              <span>Advanced</span>
              <ChevronDown
                className={`w-3.5 h-3.5 transition-transform duration-150 ${showAdvanced ? 'rotate-180' : ''}`}
              />
            </button>
          </div>
        </div>

        {/* Advanced Sliders Drawer */}
        {showAdvanced && (
          <div className="grid grid-cols-2 gap-4 px-4 py-3 glass rounded-xl animate-slide-up border border-border-subtle">
            <div>
              <label className="text-xs font-medium text-text-secondary mb-2 flex justify-between">
                <span>Top-K Chunks</span>
                <span className="text-accent font-semibold">{topK}</span>
              </label>
              <input
                type="range"
                min={1}
                max={15}
                value={topK}
                onChange={e => setTopK(Number(e.target.value))}
                className="w-full h-1.5 rounded-full cursor-pointer"
              />
              <div className="flex justify-between text-[10px] text-text-muted mt-1">
                <span>1</span>
                <span>15</span>
              </div>
            </div>

            <div>
              <label className="text-xs font-medium text-text-secondary mb-2 flex justify-between">
                <span>Hybrid Weight (α)</span>
                <span className="text-accent font-semibold">{alpha.toFixed(2)}</span>
              </label>
              <input
                type="range"
                min={0}
                max={1}
                step={0.05}
                value={alpha}
                disabled={mode !== 'hybrid'}
                onChange={e => setAlpha(Number(e.target.value))}
                className="w-full h-1.5 rounded-full cursor-pointer disabled:opacity-40 disabled:cursor-not-allowed"
              />
              <div className="flex justify-between text-[10px] text-text-muted mt-1">
                <span>Dense</span>
                <span>Lexical</span>
              </div>
            </div>
          </div>
        )}
      </form>
    </div>
  );
}
