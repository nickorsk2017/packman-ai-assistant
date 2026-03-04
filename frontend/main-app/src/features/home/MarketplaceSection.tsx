export function MarketplaceSection() {
  const items = [
    {
      title: "Find the perfect product in under a minute.",
      description: "Describe your needs in simple words — PackMan finds it in seconds.",
      icon: "⏱",
    },
    {
      title: "Buy from other people",
      description: "Deal directly with sellers. Transparent prices and real availability.",
      icon: "🤝",
    },
    {
      title: "Exchange second-hand easily",
      description: "Trade or buy used devices with confidence. Simple, fast, secure.",
      icon: "🔄",
    },
  ];

  return (
    <section id="marketplace" className="border-t border-[var(--lilac-200)]/40 py-15 md:py-20 sm:py-24">
      <div className="mx-auto max-w-6xl px-4 sm:px-6 lg:px-8">
        <h2 className="text-center text-3xl font-bold tracking-tight text-[var(--foreground)] sm:text-4xl">
          Peer-to-Peer Marketplace
        </h2>
        <p className="mx-auto mt-4 max-w-2xl text-center text-[var(--muted)]">
          Sell, buy, and exchange with real people. No middleman markup.
        </p>
        <div className="mt-16 grid gap-8 sm:grid-cols-3">
          {items.map((item) => (
            <div
              key={item.title}
              className="rounded-2xl border border-[var(--lilac-200)]/60 bg-gradient-to-b from-[var(--lilac-50)]/50 to-white p-8"
            >
              <span className="text-2xl" aria-hidden>
                {item.icon}
              </span>
              <h3 className="mt-4 text-xl font-semibold text-[var(--foreground)]">{item.title}</h3>
              <p className="mt-2 text-[var(--muted)] leading-relaxed">{item.description}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

