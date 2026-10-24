import { useState, useRef, useCallback, useEffect } from 'react';
import { Menu, Sun, Moon, ArrowRight, Activity, ShieldCheck, Database, Cpu, Globe } from 'lucide-react';
import { api } from './api/client';
import Sidebar, { type HistoryItem } from './components/Sidebar';
import QueryInput from './components/QueryInput';
import ChatMessage, { type ChatMessageData } from './components/ChatMessage';

type Mode = 'hybrid' | 'semantic' | 'tfidf';

let counter = 0;
const uid = () => String(++counter);

export default function App() {
  const [messages, setMessages] = useState<ChatMessageData[]>([]);
  const [history, setHistory] = useState<HistoryItem[]>([]);
  const [activeId, setActiveId] = useState<string | null>(null);
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [ollamaModel, setOllamaModel] = useState('');
  const [showEngineDetails, setShowEngineDetails] = useState(false);
  const [theme, setTheme] = useState<'dark' | 'light'>(() => {
    try {
      const saved = localStorage.getItem('querymind_theme');
      if (saved === 'dark' || saved === 'light') return saved;
      return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
    } catch {
      return 'dark';
    }
  });

  const bottomRef = useRef<HTMLDivElement>(null);
  const abortRef = useRef<AbortController | null>(null);

  // Apply theme to document element
  useEffect(() => {
    const root = document.documentElement;
    if (theme === 'dark') {
      root.classList.add('dark');
    } else {
      root.classList.remove('dark');
    }
    try {
      localStorage.setItem('querymind_theme', theme);
    } catch {
      // storage unavailable
    }
  }, [theme]);

  const toggleTheme = () => {
    setTheme(t => (t === 'dark' ? 'light' : 'dark'));
  };

  // Scroll chat to bottom whenever messages change
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages.length]);

  /**
   * Core execution — calls the backend query endpoint.
   */
  const executeQuery = useCallback(
    async (
      query: string,
      mode: Mode,
      topK: number,
      _alpha: number,
      addToHistory: boolean,
    ) => {
      abortRef.current?.abort();
      const controller = new AbortController();
      abortRef.current = controller;

      const userMsgId = uid();
      const assistMsgId = uid();

      setMessages(prev => [
        ...prev,
        { id: userMsgId, role: 'user', query },
        { id: assistMsgId, role: 'assistant', loading: true },
      ]);

      try {
        const result = await api.query(
          {
            query,
            mode,
            top_k: topK,
            allow_web_fallback: true,
            ollama_model: ollamaModel || undefined,
          },
          controller.signal,
        );

        setMessages(prev =>
          prev.map(m =>
            m.id === assistMsgId
              ? { ...m, loading: false, answer: result }
              : m,
          ),
        );

        if (addToHistory) {
          const histId = uid();
          setHistory(prev => {
            if (prev.some(h => h.query === query && h.mode === mode)) return prev;
            const item: HistoryItem = { id: histId, query, mode, timestamp: new Date() };
            return [item, ...prev.slice(0, 19)];
          });
        }
      } catch (e: any) {
        if (e?.name === 'AbortError') {
          setMessages(prev =>
            prev.map(m =>
              m.id === assistMsgId ? { ...m, loading: false, stopped: true } : m,
            ),
          );
          return;
        }
        setMessages(prev =>
          prev.map(m =>
            m.id === assistMsgId
              ? { ...m, loading: false, error: e.message || 'Failed to connect to backend.' }
              : m,
          ),
        );
      } finally {
        if (abortRef.current === controller) abortRef.current = null;
      }
    },
    [ollamaModel],
  );

  const handleStop = useCallback(() => {
    abortRef.current?.abort();
    abortRef.current = null;
  }, []);

  const handleQuery = useCallback(
    (query: string, mode: Mode, topK: number, alpha: number) => {
      executeQuery(query, mode, topK, alpha, true);
    },
    [executeQuery],
  );

  const handleHistorySelect = useCallback(
    (item: HistoryItem) => {
      setActiveId(item.id);
      executeQuery(item.query, item.mode as Mode, 5, 0.5, false);
    },
    [executeQuery],
  );

  const handleNew = () => {
    setMessages([]);
    setActiveId(null);
  };

  const handleRelatedClick = useCallback(
    (topic: string) => {
      executeQuery(topic, 'hybrid', 5, 0.5, true);
    },
    [executeQuery],
  );

  const isLoading = messages.some(m => m.loading);

  const promptSuggestions = [
    'What is binary search time complexity?',
    'Python list comprehension examples',
    'JavaScript Promise.all vs allSettled',
    'Explain Merge Sort algorithm step by step',
    'What are the latest features in Rust 1.85?',
  ];

  return (
    <div className="relative flex flex-col h-screen w-screen overflow-hidden text-text-primary bg-bg-primary">
      {/* Ambient background motion */}
      <div className="bg-scene">
        <div className="orb orb-1" />
        <div className="orb orb-2" />
      </div>

      {/* App layer */}
      <div className="relative z-10 flex flex-col h-full">

        {/* ── Header Bar ── */}
        <header className="glass shrink-0 h-14 px-4 flex items-center justify-between border-b border-border-subtle">
          <div className="flex items-center gap-3">
            <button
              onClick={() => setSidebarOpen(s => !s)}
              className="btn-ghost p-2 rounded-lg"
              aria-label="Toggle sidebar"
            >
              <Menu className="w-4 h-4" />
            </button>

            {/* Brand Logo & Name */}
            <div className="flex items-center gap-2.5">
              <div className="logo-glow-container">
                <img
                  src="/logo-rag.png"
                  alt="QUERY MIND Logo"
                  className="relative z-10 w-8 h-8 rounded-lg object-contain bg-bg-surface border border-border-subtle p-0.5 shadow-sm"
                />
              </div>
              <span className="font-semibold text-sm tracking-tight text-text-primary">
                QUERY MIND
              </span>
            </div>

            {/* Engine Ready Badge with Interactive Popover */}
            <div className="relative hidden sm:block">
              <button
                onClick={() => setShowEngineDetails(s => !s)}
                className="flex items-center gap-1.5 px-2.5 py-1 rounded-full text-[11px] font-medium bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 border border-emerald-500/20 hover:border-emerald-500/40 transition-colors"
                title="Click for engine details"
                aria-label="Engine status"
              >
                <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse" />
                <span>Engine Ready</span>
              </button>

              {showEngineDetails && (
                <div className="absolute top-8 left-0 z-50 w-64 p-3 rounded-xl glass border border-border-strong text-xs space-y-2 animate-slide-up shadow-lg">
                  <div className="flex items-center justify-between font-semibold text-text-primary border-b border-border-subtle pb-1.5">
                    <span>Active Pipeline</span>
                    <Activity className="w-3.5 h-3.5 text-accent" />
                  </div>
                  <div className="space-y-1.5 text-[11px] text-text-secondary">
                    <div className="flex items-center gap-1.5">
                      <Database className="w-3 h-3 text-accent shrink-0" />
                      <span>Qdrant Cloud (Cosine Dense)</span>
                    </div>
                    <div className="flex items-center gap-1.5">
                      <ShieldCheck className="w-3 h-3 text-emerald-500 shrink-0" />
                      <span>TF-IDF Inverted Index</span>
                    </div>
                    <div className="flex items-center gap-1.5">
                      <Cpu className="w-3 h-3 text-accent shrink-0" />
                      <span>Ollama Local (llama3.2)</span>
                    </div>
                    <div className="flex items-center gap-1.5">
                      <Globe className="w-3 h-3 text-sky-500 shrink-0" />
                      <span>DuckDuckGo Web Fallback</span>
                    </div>
                  </div>
                </div>
              )}
            </div>
          </div>

          {/* Top Right Controls (Theme Switcher) */}
          <div className="flex items-center gap-2">
            <button
              onClick={toggleTheme}
              className="btn-ghost p-2 rounded-xl text-text-secondary hover:text-text-primary transition-colors"
              aria-label="Toggle color theme"
              title={`Switch to ${theme === 'dark' ? 'light' : 'dark'} mode`}
            >
              {theme === 'dark' ? (
                <Sun className="w-4 h-4 text-amber-400" />
              ) : (
                <Moon className="w-4 h-4 text-slate-700" />
              )}
            </button>
          </div>
        </header>

        {/* ── Main Body ── */}
        <div className="flex flex-1 overflow-hidden">

          {/* Sidebar */}
          <div
            className={`transition-all duration-200 ease-in-out overflow-hidden shrink-0 ${
              sidebarOpen ? 'w-64' : 'w-0'
            }`}
          >
            <Sidebar
              history={history}
              activeId={activeId}
              onSelect={handleHistorySelect}
              onNew={handleNew}
            />
          </div>

          {/* Main Chat Area */}
          <main className="flex-1 flex flex-col overflow-hidden">

            {/* Scrollable Chat Area */}
            <div className="flex-1 overflow-y-auto px-4 py-6 space-y-4">
              <div className="max-w-3xl mx-auto w-full space-y-4">

                {/* Empty State / Hero Section */}
                {messages.length === 0 && (
                  <div className="flex flex-col items-center justify-center min-h-[55vh] text-center px-4 animate-slide-up">

                    {/* Logo with Ambient Back-Glow */}
                    <div className="mb-5 logo-glow-container">
                      <div className="relative z-10 p-4 rounded-2xl bg-bg-surface border border-border-subtle shadow-card">
                        <img
                          src="/logo-rag.png"
                          alt="QUERY MIND Logo"
                          className="w-14 h-14 rounded-xl object-contain"
                        />
                      </div>
                    </div>

                    {/* Humanized Heading & Description */}
                    <h1 className="text-2xl font-bold text-text-primary mb-2.5 tracking-tight">
                      Grounded Coding Intelligence
                    </h1>
                    <p className="text-sm text-text-secondary max-w-lg leading-relaxed mb-4">
                      QUERY MIND searches your codebase using hybrid vector and keyword matching.
                      It automatically checks live web documentation for up-to-date syntax,
                      with local AI models producing grounded answers without hallucinations.
                    </p>

                    {/* Secondary Technical Feature Chips */}
                    <div className="flex flex-wrap items-center justify-center gap-1.5 mb-8 text-[11px] text-text-muted">
                      <span className="glass px-2.5 py-0.5 rounded-full border border-border-subtle">
                        Qdrant Vector
                      </span>
                      <span className="glass px-2.5 py-0.5 rounded-full border border-border-subtle">
                        TF-IDF Lexical
                      </span>
                      <span className="glass px-2.5 py-0.5 rounded-full border border-border-subtle">
                        Ollama Local
                      </span>
                      <span className="glass px-2.5 py-0.5 rounded-full border border-border-subtle">
                        Web Fallback
                      </span>
                    </div>

                    {/* 5 Prompt Suggestions (Balanced Grid Layout) */}
                    <div className="w-full max-w-xl grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs">
                      {promptSuggestions.map((q, idx) => (
                        <button
                          key={q}
                          onClick={() => handleQuery(q, 'hybrid', 5, 0.5)}
                          className={`flex items-center justify-between p-3 rounded-xl glass border border-border-subtle text-text-secondary hover:text-text-primary hover:border-accent/40 hover:-translate-y-0.5 transition-all text-left group ${
                            idx === promptSuggestions.length - 1 ? 'sm:col-span-2' : ''
                          }`}
                        >
                          <span className="line-clamp-1 pr-2">{q}</span>
                          <ArrowRight className="w-3.5 h-3.5 text-accent opacity-60 group-hover:opacity-100 group-hover:translate-x-0.5 transition-all shrink-0" />
                        </button>
                      ))}
                    </div>
                  </div>
                )}

                {/* Messages List */}
                {messages.map(msg => (
                  <ChatMessage
                    key={msg.id}
                    message={msg}
                    onRelatedClick={handleRelatedClick}
                  />
                ))}

                <div ref={bottomRef} />
              </div>
            </div>

            {/* Input Dock */}
            <div className="shrink-0 glass border-t border-border-subtle px-4 py-4">
              <div className="max-w-3xl mx-auto w-full">
                <QueryInput
                  loading={isLoading}
                  onSubmit={handleQuery}
                  onStop={handleStop}
                  ollamaModel={ollamaModel}
                  onModelChange={setOllamaModel}
                />
              </div>
            </div>

          </main>
        </div>
      </div>
    </div>
  );
}
