import { MessageSquare, Plus, Upload, Link, Loader2, X, CheckCircle, AlertCircle, FolderOpen } from 'lucide-react';
import { useState, useRef } from 'react';
import { api } from '../api/client';

export interface HistoryItem {
  id: string;
  query: string;
  mode: string;
  timestamp: Date;
}

interface Props {
  history: HistoryItem[];
  activeId: string | null;
  onSelect: (item: HistoryItem) => void;
  onNew: () => void;
}

type UploadStatus = { type: 'success' | 'error'; message: string } | null;

export default function Sidebar({ history, activeId, onSelect, onNew }: Props) {
  const [ingesting, setIngesting] = useState(false);
  const [status, setStatus] = useState<UploadStatus>(null);
  const [urlInput, setUrlInput] = useState('');
  const [showUrl, setShowUrl] = useState(false);
  const fileRef = useRef<HTMLInputElement>(null);

  const showStatus = (type: 'success' | 'error', message: string) => {
    setStatus({ type, message });
    setTimeout(() => setStatus(null), 4000);
  };

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;
    e.target.value = ''; // reset so same file can be re-uploaded
    setIngesting(true);
    setStatus(null);
    try {
      const res = await api.ingestFile(file);
      showStatus('success', `✓ ${file.name} — ${res.chunks_created} chunks indexed`);
    } catch (err: any) {
      showStatus('error', err.message || 'Upload failed');
    } finally {
      setIngesting(false);
    }
  };

  const handleUrlIngest = async () => {
    const url = urlInput.trim();
    if (!url) return;
    setIngesting(true);
    setStatus(null);
    try {
      const res = await api.ingestUrl(url);
      setUrlInput('');
      setShowUrl(false);
      showStatus('success', `✓ URL ingested — ${res.chunks_created} chunks indexed`);
    } catch (err: any) {
      showStatus('error', err.message || 'URL ingest failed');
    } finally {
      setIngesting(false);
    }
  };

  const handleReIngest = async () => {
    setIngesting(true);
    setStatus(null);
    try {
      const res = await api.ingest();
      showStatus('success', `✓ Re-indexed ${res.chunks_created} chunks from ${res.documents_loaded} docs`);
    } catch (err: any) {
      showStatus('error', err.message || 'Re-ingest failed');
    } finally {
      setIngesting(false);
    }
  };

  return (
    <aside className="w-64 h-full glass border-r border-border-subtle flex flex-col">
      {/* New Chat button */}
      <div className="p-3 border-b border-border-subtle">
        <button
          onClick={onNew}
          className="w-full flex items-center gap-2.5 px-3 py-2.5 rounded-xl btn-ghost text-sm font-medium"
        >
          <Plus className="w-4 h-4" />
          New Chat
        </button>
      </div>

      {/* History */}
      <div className="flex-1 overflow-y-auto py-2">
        {history.length === 0 ? (
          <div className="px-4 py-8 text-center">
            <MessageSquare className="w-9 h-9 text-border-subtle mx-auto mb-3 opacity-40" />
            <p className="text-xs text-text-muted">No conversations yet</p>
            <p className="text-[11px] text-text-muted mt-1 opacity-60">
              Ask a question to get started
            </p>
          </div>
        ) : (
          <div className="space-y-0.5 px-2">
            <p className="text-[10px] font-semibold text-text-muted uppercase tracking-widest px-2 py-1.5 mt-1">
              Recent
            </p>
            {history.map(item => (
              <button
                key={item.id}
                onClick={() => onSelect(item)}
                className={`w-full text-left px-3 py-2.5 rounded-xl text-xs transition-all duration-150 border ${
                  item.id === activeId
                    ? 'bg-accent/10 border-accent/30 text-text-primary font-medium'
                    : 'border-transparent text-text-muted hover:text-text-primary hover:bg-bg-surface-hover'
                }`}
              >
                <div className="flex items-start gap-2">
                  <MessageSquare className="w-3.5 h-3.5 mt-0.5 shrink-0 opacity-60 text-accent" />
                  <div className="min-w-0 flex-1">
                    <p className="truncate font-medium leading-snug">{item.query}</p>
                    <div className="flex items-center gap-1.5 mt-1">
                      <span className={`px-1.5 py-0.5 rounded-full text-[10px] font-medium ${
                        item.id === activeId
                          ? 'bg-accent/20 text-accent'
                          : 'bg-black/5 dark:bg-white/5 text-text-muted'
                      }`}>
                        {item.mode}
                      </span>
                      <span className="text-[10px] text-text-muted opacity-60">
                        {item.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                      </span>
                    </div>
                  </div>
                </div>
              </button>
            ))}
          </div>
        )}
      </div>

      {/* Document ingestion footer */}
      <div className="p-3 border-t border-border-subtle space-y-2">
        <p className="text-[10px] font-semibold text-text-muted uppercase tracking-widest px-1 pb-1">
          Knowledge Base
        </p>

        {/* Upload file button */}
        <input
          ref={fileRef}
          type="file"
          accept=".md,.txt,.py,.js,.ts,.pdf"
          className="hidden"
          onChange={handleFileUpload}
        />
        <button
          onClick={() => fileRef.current?.click()}
          disabled={ingesting}
          className="w-full flex items-center gap-2 px-3 py-2 rounded-xl btn-ghost text-xs disabled:opacity-40"
        >
          {ingesting ? (
            <Loader2 className="w-3.5 h-3.5 animate-spin" />
          ) : (
            <Upload className="w-3.5 h-3.5" />
          )}
          Upload Document
        </button>

        {/* URL ingest */}
        <button
          onClick={() => setShowUrl(s => !s)}
          disabled={ingesting}
          className="w-full flex items-center gap-2 px-3 py-2 rounded-xl btn-ghost text-xs disabled:opacity-40"
        >
          <Link className="w-3.5 h-3.5" />
          Ingest from URL
          {showUrl && <X className="w-3 h-3 ml-auto opacity-60" />}
        </button>

        {showUrl && (
          <div className="space-y-1.5 animate-slide-up">
            <input
              type="url"
              value={urlInput}
              onChange={e => setUrlInput(e.target.value)}
              onKeyDown={e => e.key === 'Enter' && handleUrlIngest()}
              placeholder="https://example.com/doc.md"
              className="glass-input w-full rounded-lg px-3 py-2 text-xs"
            />
            <button
              onClick={handleUrlIngest}
              disabled={!urlInput.trim() || ingesting}
              className="w-full btn-accent rounded-lg py-1.5 text-xs font-medium"
            >
              {ingesting ? 'Ingesting…' : 'Ingest URL'}
            </button>
          </div>
        )}

        {/* Re-index all */}
        <button
          onClick={handleReIngest}
          disabled={ingesting}
          className="w-full flex items-center gap-2 px-3 py-2 rounded-xl btn-ghost text-xs disabled:opacity-40"
        >
          <FolderOpen className="w-3.5 h-3.5" />
          Re-index All Docs
        </button>

        {/* Status toast */}
        {status && (
          <div className={`flex items-start gap-2 px-3 py-2 rounded-lg text-xs animate-slide-up ${
            status.type === 'success'
              ? 'bg-success/10 text-success border border-success/20'
              : 'bg-danger/10 text-danger border border-danger/20'
          }`}>
            {status.type === 'success'
              ? <CheckCircle className="w-3.5 h-3.5 shrink-0 mt-0.5" />
              : <AlertCircle className="w-3.5 h-3.5 shrink-0 mt-0.5" />}
            <span className="leading-relaxed">{status.message}</span>
          </div>
        )}
      </div>
    </aside>
  );
}
