"use client";

export function SearchPageHeader() {
  return (
    <div className="max-w-2xl">
      <h1 className="text-3xl font-bold tracking-tight text-[var(--foreground)] sm:text-4xl">
        AI Searching
      </h1>
      <p className="mt-3 text-[var(--muted)]">
        Describe what you&apos;re looking for in natural language. PackMan will use your prompt and the
        selected category to find the best product match.
      </p>
    </div>
  );
}

