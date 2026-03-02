"use client";

import { useState } from "react";
import { LandingHeader } from "../components/LandingHeader";
import { LandingFooter } from "../components/LandingFooter";

const CATEGORIES = [{ id: "phones", label: "Phones" as const }];
const ITEM_COUNT = 100;

export default function SearchPage() {
  const [prompt, setPrompt] = useState("");
  const [maxPrice, setMaxPrice] = useState<string>("");
  const [selectedCategory] = useState(CATEGORIES[0]); // Phones is default and only category

  return (
    <div className="min-h-screen gradient-mesh bg-[var(--background)] text-[var(--foreground)]">
      <LandingHeader />

      <main className="pt-24 pb-16">
        <div className="mx-auto max-w-5xl px-4 sm:px-6 lg:px-8">
          <div className="max-w-2xl">
            <h1 className="text-3xl font-bold tracking-tight text-[var(--foreground)] sm:text-4xl">
              AI Searching
            </h1>
            <p className="mt-3 text-[var(--muted)]">
              Describe what you&apos;re looking for in natural language. PackMan will use your prompt and the
              selected category to find the best product match.
            </p>
          </div>

          <div className="mt-10 grid gap-8 md:grid-cols-[220px,minmax(0,1fr)]">
            {/* Categories block */}
            <aside className="rounded-2xl border border-[var(--lilac-200)]/70 bg-white/80 p-5 shadow-sm">
              <p className="text-xs font-semibold uppercase tracking-wider text-[var(--muted)]">
                Categories &amp; price
              </p>
              <div className="mt-4 flex flex-col items-stretch gap-3 sm:flex-row sm:items-center sm:justify-between">
                <div
                  className="w-full py-2"
                >
                  <label className="mb-[6px] block text-xs font-semibold uppercase tracking-wider text-[var(--muted)]">
                   Category
                  </label>
                  <button
                    type="button"
                    className="h-[38px] w-full rounded-xl bg-[var(--lilac-500)] rounded-full px-2 py-0.5 text-[10px] uppercase tracking-wide text-white"
                  >
                    <span>{selectedCategory.label}</span>
                    <span className="rounded-full bg-white/20 px-2 py-0.5 text-[10px] uppercase tracking-wide">
                      Selected
                    </span>
                  </button>
                </div>
                <div className="w-full sm:w-[300px]">
                  <label className="block text-xs font-semibold uppercase tracking-wider text-[var(--muted)]">
                    Max price (USD)
                  </label>
                  <input
                    type="number"
                    min={0}
                    value={maxPrice}
                    onChange={(e) => setMaxPrice(e.target.value)}
                    placeholder="e.g. 800"
                    className="mt-1 w-full rounded-xl border border-[var(--lilac-200)] bg-white px-3 py-2 text-sm text-[var(--foreground)] shadow-sm outline-none focus:border-[var(--lilac-500)] focus:ring-2 focus:ring-[var(--lilac-300)]"
                  />
                </div>
              </div>
              <p className="mt-4 text-xs text-[var(--muted)]">
                More categories will be added in future versions of the MVP.
              </p>
            </aside>

            {/* Searching block */}
            <section className="rounded-2xl border border-[var(--lilac-200)]/70 bg-white/90 p-6 shadow-sm">
              <p className="text-xs font-semibold uppercase tracking-wider text-[var(--muted)]">
                Selected category
              </p>
              <p className="mt-1 text-sm font-medium text-[var(--foreground)]">{selectedCategory.label}</p>
              <p className="mt-1 text-xs text-[var(--muted)]">
                {ITEM_COUNT} items in this category
              </p>

              <label className="mt-6 block text-sm font-medium text-[var(--foreground)]">
                Your AI prompt
              </label>
              <textarea
                value={prompt}
                onChange={(e) => setPrompt(e.target.value)}
                placeholder="Type your prompt"
                className="mt-2 w-full min-h-[140px] resize-y rounded-2xl border border-[var(--lilac-200)] bg-white/90 px-3 py-2 text-sm text-[var(--foreground)] shadow-sm outline-none focus:border-[var(--lilac-500)] focus:ring-2 focus:ring-[var(--lilac-300)]"
              />

              <div className="mt-4 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
                <p className="text-xs text-[var(--muted)]">
                  Example: &ldquo;I need a phone for gaming under $800 with good battery.&rdquo;
                </p>
                <button
                  type="button"
                  className="inline-flex items-center justify-center rounded-xl bg-[var(--lilac-500)] px-4 py-2 text-sm font-semibold text-white shadow-md hover:bg-[var(--lilac-600)] disabled:opacity-60"
                  disabled
                >
                  Ask PackMan (demo)
                </button>
              </div>

              <p className="mt-3 text-xs text-[var(--muted)]">
                This is a visual MVP of the AI search experience.
              </p>
            </section>
          </div>
        </div>
      </main>

      <LandingFooter />
    </div>
  );
}

