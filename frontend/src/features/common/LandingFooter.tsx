export function LandingFooter() {
  return (
    <footer className="border-t border-[var(--lilac-200)]/40 py-8">
      <div className="mx-auto max-w-6xl px-4 sm:px-6 lg:px-8 space-y-4">
        <div className="flex flex-col items-center justify-between gap-4 sm:flex-row">
          <span className="font-semibold text-[var(--lilac-700)]">PackMan</span>
          <p className="text-sm text-[var(--muted)]">
            AI-powered smartphone marketplace. Buy, sell, exchange.
          </p>
        </div>

        <div className="flex flex-col items-center justify-between gap-3 border-t border-[var(--lilac-200)]/60 pt-4 text-sm sm:flex-row">
          <p className="text-[var(--muted)]">
            Author: <span className="font-medium text-[var(--foreground)]">Nikolai Stepanov</span>
          </p>
          <a
            href="https://www.linkedin.com/in/nickot"
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-2 rounded-full border border-[var(--lilac-300)] bg-white px-4 py-1.5 text-xs font-medium text-[var(--lilac-700)] shadow-sm hover:bg-[var(--lilac-50)]"
          >
            <span>View LinkedIn profile</span>
          </a>
        </div>
      </div>
    </footer>
  );
}

