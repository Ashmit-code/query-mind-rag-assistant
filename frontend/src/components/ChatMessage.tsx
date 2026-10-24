import type { GeneratedResponse } from '../api/client';
import AnswerDisplay from './AnswerDisplay';
import LoadingSkeleton from './LoadingSkeleton';
import { ServerCrash, StopCircle } from 'lucide-react';

export type ChatMessageData = {
  id: string;
  role: 'user' | 'assistant';
  query?: string;
  answer?: GeneratedResponse;
  loading?: boolean;
  stopped?: boolean;
  error?: string;
};

interface Props {
  message: ChatMessageData;
  onRelatedClick?: (topic: string) => void;
}

export default function ChatMessage({ message, onRelatedClick }: Props) {
  /* ── User bubble (right-aligned gradient pill) ── */
  if (message.role === 'user') {
    return (
      <div className="flex justify-end animate-slide-up">
        <div className="bubble-user">
          <p className="text-sm font-medium leading-relaxed">{message.query}</p>
        </div>
      </div>
    );
  }

  /* ── Assistant bubble (left-aligned glass card) ── */
  return (
    <div className="flex justify-start animate-slide-up">
      <div className="bubble-assistant">
        {/* Loading */}
        {message.loading && (
          <div className="space-y-4">
            <div className="flex items-center gap-2 mb-4">
              <span className="text-xs text-text-muted font-medium">Thinking</span>
              <div className="flex items-center gap-1">
                <span className="typing-dot" />
                <span className="typing-dot" />
                <span className="typing-dot" />
              </div>
            </div>
            <LoadingSkeleton />
          </div>
        )}

        {/* Stopped by user */}
        {message.stopped && !message.loading && (
          <div className="flex items-center gap-2.5 py-1 text-text-muted">
            <StopCircle className="w-4 h-4 text-warning/70 shrink-0" />
            <span className="text-xs">Generation stopped</span>
          </div>
        )}

        {/* Error */}
        {message.error && !message.loading && (
          <div className="flex items-start gap-3 p-4 rounded-xl border border-danger/30 bg-danger/5">
            <ServerCrash className="w-5 h-5 text-danger shrink-0 mt-0.5" />
            <div>
              <p className="text-sm font-semibold text-danger">Request failed</p>
              <p className="text-xs text-text-secondary mt-1">{message.error}</p>
              <p className="text-xs text-text-muted mt-2 font-mono">
                Make sure the backend is running: uvicorn backend.api:app --reload --port 8000
              </p>
            </div>
          </div>
        )}

        {/* Answer */}
        {message.answer && !message.loading && (
          <AnswerDisplay answer={message.answer} onRelatedClick={onRelatedClick} />
        )}
      </div>
    </div>
  );
}
