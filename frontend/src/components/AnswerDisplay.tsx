import { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import CodeBlock from './CodeBlock';
import type { GeneratedResponse } from '../api/client';
import {
  Sparkles,
  Globe,
  Database,
  SearchX,
  ExternalLink,
  ChevronDown,
  ChevronUp,
  Copy,
  Check,
  FileCode,
} from 'lucide-react';

interface Props {
  answer: GeneratedResponse;
  onRelatedClick?: (topic: string) => void;
}

export default function AnswerDisplay({ answer }: Props) {
  const [copied, setCopied] = useState(false);
  const [showSources, setShowSources] = useState(false);

  const handleCopy = () => {
    navigator.clipboard.writeText(answer.answer_markdown);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  /* ── No relevant information found ── */
  if (answer.source_type === 'none') {
    return (
      <div className="flex flex-col items-center justify-center py-6 text-center space-y-3 animate-slide-up">
        <div className="p-3.5 rounded-2xl bg-amber-500/10 border border-amber-500/20 text-amber-400">
          <SearchX className="w-7 h-7" />
        </div>
        <div>
          <p className="text-sm font-semibold text-text-primary">No Sufficient Information Found</p>
          <p className="text-xs text-text-secondary mt-1.5 max-w-md leading-relaxed">
            {answer.answer_markdown}
          </p>
        </div>
        <div className="flex flex-wrap justify-center gap-2 pt-2 text-[11px] text-text-muted">
          <span className="glass px-3 py-1 rounded-full border border-border-subtle">
            Tip: Upload more documents to the Knowledge Base in the sidebar
          </span>
        </div>
      </div>
    );
  }

  const isLocal = answer.source_type === 'local';
  const isWeb = answer.source_type === 'web';

  return (
    <div className="space-y-4 animate-slide-up">
      {/* Top Metadata Bar */}
      <div className="flex flex-wrap items-center justify-between gap-2 pb-2 border-b border-border-subtle/50 text-xs">
        <div className="flex items-center gap-2">
          {isLocal ? (
            <span className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-[11px] font-medium bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
              <Database className="w-3 h-3" />
              Knowledge Base
            </span>
          ) : isWeb ? (
            <span className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-[11px] font-medium bg-sky-500/10 text-sky-400 border border-sky-500/20">
              <Globe className="w-3 h-3" />
              Web Fallback
            </span>
          ) : null}

          <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[11px] text-text-muted glass border border-border-subtle">
            <Sparkles className="w-3 h-3 text-accent" />
            {answer.model_used}
          </span>

          {isLocal && answer.score > 0 && (
            <span className="text-[11px] text-text-muted font-mono">
              Score: {answer.score.toFixed(2)}
            </span>
          )}
        </div>

        <button
          onClick={handleCopy}
          className="inline-flex items-center gap-1 text-[11px] text-text-muted hover:text-text-primary px-2 py-1 rounded hover:bg-white/5 transition-colors"
          title="Copy response"
        >
          {copied ? <Check className="w-3 h-3 text-emerald-400" /> : <Copy className="w-3 h-3" />}
          {copied ? 'Copied' : 'Copy'}
        </button>
      </div>

      {/* Main Markdown Body */}
      <div className="prose prose-invert max-w-none text-sm text-text-primary leading-relaxed space-y-3">
        <ReactMarkdown
          components={{
            code({ className, children, ...props }) {
              const match = /language-(\w+)/.exec(className || '');
              const isInline = !match && !String(children).includes('\n');
              if (isInline) {
                return (
                  <code className="px-1.5 py-0.5 rounded bg-black/5 dark:bg-white/10 font-mono text-[13px] text-accent" {...props}>
                    {children}
                  </code>
                );
              }
              const language = match ? match[1] : 'python';
              return (
                <div className="my-3">
                  <CodeBlock code={String(children).replace(/\n$/, '')} language={language} />
                </div>
              );
            },
            h1: ({ children }) => <h2 className="text-base font-bold text-text-primary mt-4 mb-2">{children}</h2>,
            h2: ({ children }) => <h3 className="text-sm font-semibold text-text-primary mt-3 mb-1.5">{children}</h3>,
            h3: ({ children }) => <h4 className="text-xs font-semibold uppercase tracking-wider text-accent mt-3 mb-1">{children}</h4>,
            p: ({ children }) => <p className="mb-2.5 text-text-secondary leading-relaxed">{children}</p>,
            ul: ({ children }) => <ul className="list-disc pl-5 space-y-1 mb-2.5 text-text-secondary">{children}</ul>,
            ol: ({ children }) => <ol className="list-decimal pl-5 space-y-1 mb-2.5 text-text-secondary">{children}</ol>,
            blockquote: ({ children }) => (
              <blockquote className="border-l-2 border-accent/40 pl-3 italic text-text-muted my-2">
                {children}
              </blockquote>
            ),
          }}
        >
          {answer.answer_markdown}
        </ReactMarkdown>
      </div>

      {/* Citations & Sources */}
      {(answer.local_results.length > 0 || answer.web_results.length > 0) && (
        <div className="pt-3 border-t border-border-subtle/40">
          <button
            onClick={() => setShowSources(!showSources)}
            className="flex items-center gap-1.5 text-xs text-text-muted hover:text-text-primary font-medium transition-colors"
          >
            <span>
              {isLocal
                ? `Knowledge Base Sources (${answer.local_results.length})`
                : `Web Search Sources (${answer.web_results.length})`}
            </span>
            {showSources ? <ChevronUp className="w-3.5 h-3.5" /> : <ChevronDown className="w-3.5 h-3.5" />}
          </button>

          {showSources && (
            <div className="mt-2.5 space-y-2 animate-slide-up">
              {isLocal &&
                answer.local_results.map((c, i) => (
                  <div
                    key={c.chunk_id || i}
                    className="p-2.5 rounded-lg glass border border-border-subtle text-xs space-y-1"
                  >
                    <div className="flex items-center justify-between text-text-muted">
                      <span className="font-semibold text-text-primary flex items-center gap-1.5">
                        <FileCode className="w-3.5 h-3.5 text-accent" />
                        {c.filename} — {c.section}
                      </span>
                      <span className="font-mono text-[10px] text-accent/80">
                        Score: {c.score.toFixed(3)}
                      </span>
                    </div>
                    <p className="text-[11px] text-text-secondary line-clamp-2 font-mono bg-black/20 p-1.5 rounded">
                      {c.text}
                    </p>
                  </div>
                ))}

              {isWeb &&
                answer.web_results.map((w, i) => (
                  <a
                    key={i}
                    href={w.href}
                    target="_blank"
                    rel="noreferrer"
                    className="block p-2.5 rounded-lg glass border border-border-subtle hover:border-accent/40 text-xs transition-colors group"
                  >
                    <div className="flex items-center justify-between">
                      <span className="font-medium text-sky-400 group-hover:underline flex items-center gap-1.5">
                        {w.title}
                        <ExternalLink className="w-3 h-3 opacity-70" />
                      </span>
                    </div>
                    <p className="text-[11px] text-text-muted line-clamp-2 mt-1">{w.body}</p>
                  </a>
                ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
