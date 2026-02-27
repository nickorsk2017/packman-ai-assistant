export function HowItWorksSection() {
  const steps = [
    {
      step: "1",
      title: "Describe what you need",
      description: "Type in plain language: budget, use case, features. No filters or menus.",
    },
    {
      step: "2",
      title: "AI analyzes marketplace",
      description: "PackMan scans live listings and ranks offers by your criteria in real time.",
    },
    {
      step: "3",
      title: "Get the best match instantly",
      description: "See your top match with a clear comparison. Connect with the seller in one click.",
    },
  ];

  return (
    <section id="how-it-works" className="border-t border-[var(--lilac-200)]/40 bg-white/50 py-15 md:py-20 sm:py-24">
      <div className="mx-auto max-w-6xl px-4 sm:px-6 lg:px-8">
        <h2 className="text-center text-3xl font-bold tracking-tight text-[var(--foreground)] sm:text-4xl">
          How It Works
        </h2>
        <p className="mx-auto mt-4 max-w-2xl text-center text-[var(--muted)]">
          Three steps to your perfect phone.
        </p>
        <div className="mt-16 grid gap-10 sm:grid-cols-3">
          {steps.map((item) => (
            <div
              key={item.step}
              className="relative rounded-2xl border border-[var(--lilac-200)]/60 bg-white p-8 shadow-sm transition-shadow hover:shadow-md"
            >
              <span className="text-3xl font-bold text-[var(--lilac-200)]">{item.step}</span>
              <h3 className="mt-4 text-xl font-semibold text-[var(--foreground)]">{item.title}</h3>
              <p className="mt-2 text-[var(--muted)] leading-relaxed">{item.description}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

