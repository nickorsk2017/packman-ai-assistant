export function FeaturesSection() {
  const features = [
    { title: "Natural language search", desc: "Ask like you’d ask a friend." },
    { title: "Smart AI ranking", desc: "Offers sorted by your priorities." },
    { title: "Instant comparison", desc: "Side-by-side specs and prices." },
    { title: "Personalized results", desc: "Matches that fit your needs." },
  ];

  return (
    <section id="features" className="border-t border-[var(--lilac-200)]/40 bg-white/50 py-15 md:py-20 sm:py-24 mb-30">
      <div className="mx-auto max-w-6xl px-4 sm:px-6 lg:px-8">
        <h2 className="text-center text-3xl font-bold tracking-tight text-[var(--foreground)] sm:text-4xl">
        Features
        </h2>
        <p className="mx-auto  md:mt-4 mt-2 max-w-2xl text-center text-[var(--muted)]">
          Built for smart shoppers who value speed and simplicity.
        </p>
        <div className="mt-16 grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
          {features.map((item) => (
            <div
              key={item.title}
              className="rounded-2xl border border-[var(--lilac-200)]/60 bg-white p-6 shadow-sm"
            >
              <h3 className="font-semibold text-[var(--foreground)]">{item.title}</h3>
              <p className="mt-1 text-sm text-[var(--muted)]">{item.desc}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

