import { useState, useCallback } from 'react';
import { Copy, Check, Terminal } from 'lucide-react';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';

// Custom dark theme matching DESIGN.md tokens
const codeTheme: { [key: string]: React.CSSProperties } = {
  'code[class*="language-"]': { color: '#c9d1d9', background: 'none', fontFamily: '"JetBrains Mono", "Fira Code", monospace', fontSize: '13px', lineHeight: '1.6' },
  'pre[class*="language-"]': { color: '#c9d1d9', background: '#0D1117', margin: 0, padding: '1rem', overflow: 'auto', borderRadius: '0 0 6px 6px' },
  comment: { color: '#6B6B70', fontStyle: 'italic' },
  prolog: { color: '#6B6B70' },
  doctype: { color: '#6B6B70' },
  cdata: { color: '#6B6B70' },
  punctuation: { color: '#8b949e' },
  namespace: { opacity: 0.7 },
  property: { color: '#79c0ff' },
  tag: { color: '#7ee787' },
  boolean: { color: '#79c0ff' },
  number: { color: '#79c0ff' },
  constant: { color: '#79c0ff' },
  symbol: { color: '#79c0ff' },
  deleted: { color: '#ffa198' },
  selector: { color: '#7ee787' },
  'attr-name': { color: '#7ee787' },
  string: { color: '#a5d6ff' },
  char: { color: '#a5d6ff' },
  builtin: { color: '#ffa657' },
  inserted: { color: '#56d364' },
  operator: { color: '#d2a8ff' },
  entity: { color: '#ffa657', cursor: 'help' },
  url: { color: '#a5d6ff' },
  variable: { color: '#c9d1d9' },
  atrule: { color: '#d2a8ff' },
  'attr-value': { color: '#a5d6ff' },
  function: { color: '#d2a8ff' },
  'class-name': { color: '#f0883e' },
  keyword: { color: '#ff7b72' },
  regex: { color: '#7ee787' },
  important: { color: '#ff7b72', fontWeight: 'bold' },
  bold: { fontWeight: 'bold' },
  italic: { fontStyle: 'italic' },
};

interface Props {
  code: string;
  language?: string;
}

export default function CodeBlock({ code, language = 'python' }: Props) {
  const [copied, setCopied] = useState(false);

  const handleCopy = useCallback(async () => {
    await navigator.clipboard.writeText(code);
    setCopied(true);
    setTimeout(() => setCopied(false), 1500);
  }, [code]);

  if (!code.trim()) return null;

  return (
    <div className="rounded-lg overflow-hidden border border-border-subtle">
      {/* Header bar */}
      <div className="flex items-center justify-between px-4 py-2 bg-bg-surface-hover border-b border-border-subtle">
        <div className="flex items-center gap-2">
          <Terminal className="w-3.5 h-3.5 text-text-muted" />
          <span className="text-xs font-medium text-text-muted uppercase tracking-wider">{language}</span>
        </div>
        <button
          onClick={handleCopy}
          className="flex items-center gap-1.5 text-xs text-text-muted hover:text-text-primary transition-colors duration-150 px-2 py-1 rounded-md hover:bg-bg-primary"
          aria-label="Copy code"
        >
          {copied ? (
            <>
              <Check className="w-3.5 h-3.5 text-success" />
              <span className="text-success">Copied!</span>
            </>
          ) : (
            <>
              <Copy className="w-3.5 h-3.5" />
              <span>Copy</span>
            </>
          )}
        </button>
      </div>
      <SyntaxHighlighter
        language={language}
        style={codeTheme}
        customStyle={{ margin: 0, background: '#0D1117', borderRadius: 0 }}
        showLineNumbers
        lineNumberStyle={{ color: '#30363d', fontSize: '12px', minWidth: '2.5em' }}
      >
        {code}
      </SyntaxHighlighter>
    </div>
  );
}
