export function LandingFooter() {
  return (
    <footer className="border-t border-[var(--lilac-200)]/40 py-8">
      <div className="mx-auto flex max-w-6xl flex-col items-center justify-between gap-4 px-4 sm:flex-row sm:px-6 lg:px-8">
        <span className="font-semibold text-[var(--lilac-700)]">PackMan</span>
        <p className="text-sm text-[var(--muted)]">
          AI-powered smartphone marketplace. Buy, sell, exchange.
        </p>
      </div>
    </footer>
  );
}

