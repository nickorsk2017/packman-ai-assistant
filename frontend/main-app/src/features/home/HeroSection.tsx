import Link from "next/link";
import Image from "next/image";

export function HeroSection() {
  return (
    <section className=" pt-10 md:pt-20 relative flex flex-col items-center justify-center md:pb-20 sm:pb-28 lg:pb-32 overflow-hidden bg-white">
      <div className="mx-auto max-w-6xl px-4 sm:px-6  lg:px-8 ">
        <div className="grid gap-12 lg:grid-cols-2 lg:gap-16 items-center">
          <div>
            <h1 className="text-center md:text-left text-3xl font-bold tracking-tight text-[var(--foreground)] sm:text-5xl lg:text-3xl leading-[1.1]">
              Tell PackMan what you need.
            </h1>
            <p className="mt-6 text-lg text-[var(--muted)] max-w-xl leading-relaxed">
              AI finds the best match instantly from our peer-to-peer marketplace.
            </p>
            <div className="mt-10 flex flex-wrap gap-4">
              <Link
                href="/search"
                className="inline-flex items-center justify-center rounded-2xl bg-[var(--lilac-500)] px-8 py-4 text-base font-semibold text-white shadow-lg shadow-[var(--lilac-400)]/30 hover:bg-[var(--lilac-600)] transition-all hover:shadow-[var(--lilac-400)]/40"
              >
                Try AI Search
              </Link>
            </div>
            {/* AI input example */}
            <div
              id="hero-search"
              className="mt-10 rounded-2xl border border-[var(--lilac-200)] bg-white/80 p-4 shadow-sm backdrop-blur-sm"
            >
              <p className="mb-2 text-xs font-medium uppercase tracking-wider text-[var(--muted)]">
                Example search
              </p>
              <p className="font-mono text-sm text-[var(--foreground)] text-[var(--lilac-700)]">
                &ldquo;I need a phone for gaming under $800 with good battery.&rdquo;
              </p>
            </div>
          </div>
          {/* Mascot image */}
          <div className="relative flex justify-center lg:justify-end">
            <div className="animate-mascot relative md:h-[400px] md:w-[700px] rounded-3xl p-1 h-auto w-full">
              <Image src="/packman.png" alt="PackMan" width={700} height={600} className="flex-center md:mt-15" />
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

