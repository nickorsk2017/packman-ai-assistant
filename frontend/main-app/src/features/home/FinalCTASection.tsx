import Link from "next/link";

export function FinalCTASection() {
  return (
    <section id="cta" className="border-t border-[var(--lilac-200)]/40 py-20 sm:py-28">
      <div className="mx-auto max-w-3xl px-4 text-center sm:px-6 lg:px-8">
        <h2 className="text-3xl font-bold tracking-tight text-[var(--foreground)] sm:text-4xl lg:text-5xl">
          Stop Searching. Start Finding.
        </h2>
        <p className="mt-6 text-lg text-[var(--muted)]">
          Get your best product match in minutes. No endless scrolling.
        </p>
        <Link
          href="/search"
          className="mt-10 inline-flex items-center justify-center rounded-2xl bg-[var(--lilac-500)] px-10 py-4 text-lg font-semibold text-white shadow-lg shadow-[var(--lilac-400)]/30 hover:bg-[var(--lilac-600)] transition-all hover:shadow-[var(--lilac-400)]/40"
        >
          Find My Phone Now
        </Link>
      </div>
    </section>
  );
}

