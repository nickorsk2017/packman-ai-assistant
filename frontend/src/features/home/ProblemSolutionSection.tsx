export function ProblemSolutionSection() {
  return (
    <section id="problem-solution" className="border-t border-[var(--lilac-200)]/40 py-15 md:py-20 sm:py-24">
      <div className="mx-auto max-w-6xl px-4 sm:px-6 lg:px-8">
        <h2 className="mb-12 text-center text-3xl font-bold tracking-tight text-[var(--foreground)] sm:text-4xl">
          The Problem &amp; The Solution
        </h2>
        <div className="grid gap-8 lg:grid-cols-2 lg:gap-12">
          <div className="rounded-2xl border border-[var(--lilac-200)]/60 bg-white p-8 shadow-sm">
            <span className="text-sm font-semibold uppercase tracking-wider text-[var(--muted)]">
              The Problem
            </span>
            <p className="mt-4 text-lg text-[var(--foreground)] leading-relaxed">
              Endless scrolling, confusing specs, too many options — finding the right phone takes hours.
              Comparing prices and features across marketplaces is exhausting.
            </p>
            <ul className="mt-6 space-y-2 text-[var(--muted)]">
              <li className="flex items-center gap-2">• Dozens of tabs and filters</li>
              <li className="flex items-center gap-2">• No clear “best match” for you</li>
              <li className="flex items-center gap-2">• Wasted time instead of buying</li>
            </ul>
          </div>
          <div className="rounded-2xl border-2 border-[var(--lilac-300)] bg-gradient-to-br from-[var(--lilac-50)] to-white p-8 shadow-sm">
            <span className="text-sm font-semibold uppercase tracking-wider text-[var(--lilac-600)]">
              The Solution
            </span>
            <p className="mt-4 text-lg text-[var(--foreground)] leading-relaxed">
              PackMan understands what you need in plain language and shows the best match in one click. No
              filters, no guesswork — just tell us once and get your result.
            </p>
            <ul className="mt-6 space-y-2 text-[var(--foreground)]">
              <li className="flex items-center gap-2">✓ One search, one answer</li>
              <li className="flex items-center gap-2">✓ AI ranks offers by your criteria</li>
              <li className="flex items-center gap-2">✓ Find and buy in minutes</li>
            </ul>
          </div>
        </div>
      </div>
    </section>
  );
}

