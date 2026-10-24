export default function LoadingSkeleton() {
  return (
    <div className="space-y-5 w-full">
      {/* Explanation skeleton */}
      <div className="space-y-2.5">
        <div className="flex items-center gap-2">
          <div className="h-3.5 w-3.5 rounded shimmer" />
          <div className="h-2.5 w-20 rounded shimmer" />
        </div>
        <div className="pl-5 space-y-2">
          <div className="h-3 w-full rounded shimmer" />
          <div className="h-3 w-5/6 rounded shimmer" />
          <div className="h-3 w-4/6 rounded shimmer" />
          <div className="h-3 w-5/6 rounded shimmer" />
        </div>
      </div>

      {/* Code block skeleton */}
      <div className="space-y-2.5">
        <div className="flex items-center gap-2">
          <div className="h-3.5 w-3.5 rounded shimmer" />
          <div className="h-2.5 w-28 rounded shimmer" />
        </div>
        <div className="pl-5">
          <div className="rounded-xl border border-border-subtle overflow-hidden">
            <div className="h-8 shimmer border-b border-border-subtle" />
            <div className="bg-code-bg p-4 space-y-2">
              {[100, 75, 90, 60, 85, 45].map((w, i) => (
                <div
                  key={i}
                  className="h-3 rounded shimmer"
                  style={{ width: `${w}%` }}
                />
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Complexity / tags skeleton */}
      <div className="flex gap-2 pl-5">
        {[80, 100, 65].map((w, i) => (
          <div key={i} className="h-6 w-20 rounded-full shimmer" style={{ width: `${w}px` }} />
        ))}
      </div>
    </div>
  );
}
