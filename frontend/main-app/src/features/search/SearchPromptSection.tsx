"use client";

import type { DeviceSearchResult } from "@/services/ai";

type Category = { id: string; label: string };

type SearchPromptSectionProps = {
  selectedCategory: Category;
  itemCount: number;
  prompt: string;
  onPromptChange: (value: string) => void;
  onAddDeviceClick: () => void;
  onAskClick: () => void;
  askLoading?: boolean;
  bestMatch?: DeviceSearchResult | null;
  askError?: string | null;
  noMatchFound?: boolean;
};

export function SearchPromptSection({
  selectedCategory,
  itemCount,
  prompt,
  onPromptChange,
  onAddDeviceClick,
  onAskClick,
  askLoading = false,
  bestMatch = null,
  askError = null,
  noMatchFound = false,
}: SearchPromptSectionProps) {
  return (
    <section className="rounded-2xl border border-[var(--lilac-200)]/70 bg-white/90 p-6 shadow-sm">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div>
          <p className="text-xs font-semibold uppercase tracking-wider text-[var(--muted)]">
            Selected category
          </p>
          <p className="mt-1 text-sm font-medium text-[var(--foreground)]">{selectedCategory.label}</p>
          <p className="mt-1 text-xs text-[var(--muted)]">
            {itemCount} items in this category
          </p>
        </div>
        <button
          type="button"
          onClick={onAddDeviceClick}
          className="inline-flex items-center justify-center rounded-xl border border-[var(--lilac-300)] bg-white px-4 py-2 text-sm font-medium text-[var(--lilac-700)] shadow-sm hover:bg-[var(--lilac-50)]"
        >
          Add Device
        </button>
      </div>

      <label className="mt-6 block text-sm font-medium text-[var(--foreground)]">
        Your AI prompt
      </label>
      <textarea
        value={prompt}
        onChange={(e) => onPromptChange(e.target.value)}
        placeholder="Type your prompt"
        className="mt-2 min-h-[140px] w-full resize-y rounded-2xl border border-[var(--lilac-200)] bg-white/90 px-3 py-2 text-sm text-[var(--foreground)] shadow-sm outline-none focus:border-[var(--lilac-500)] focus:ring-2 focus:ring-[var(--lilac-300)]"
      />

      <div className="mt-4 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
        <p className="text-xs text-[var(--muted)]">
          Example: &ldquo;I need a phone for gaming under $800 with good battery.&rdquo;
        </p>
        <button
          type="button"
          onClick={onAskClick}
          disabled={!prompt.trim() || askLoading}
          className="inline-flex items-center justify-center rounded-xl bg-[var(--lilac-500)] px-4 py-2 text-sm font-semibold text-white shadow-md hover:bg-[var(--lilac-600)] disabled:opacity-60"
        >
          {askLoading ? "Finding…" : "Ask PackMan (demo)"}
        </button>
      </div>

      {askError && (
        <p className="mt-3 text-sm text-red-600">
          {askError}
        </p>
      )}

      {noMatchFound && !askError && (
        <p className="mt-3 text-sm text-[var(--muted)]">
          No devices match your prompt. Try different keywords or add more devices.
        </p>
      )}

      {bestMatch && !askError && (
        <div className="mt-4 rounded-xl border border-[var(--lilac-200)] bg-[var(--lilac-50)]/50 p-4">
          <p className="text-xs font-semibold uppercase tracking-wider text-[var(--muted)]">
            Best match
          </p>
          <p className="mt-1 font-semibold text-[var(--foreground)]">{bestMatch.name}</p>
          {bestMatch.price != null && (
            <p className="mt-0.5 text-sm text-[var(--lilac-700)]">
              ${Number(bestMatch.price).toFixed(2)}
            </p>
          )}
          {bestMatch.tags?.length > 0 && (
            <p className="mt-1 text-xs text-[var(--muted)]">
              {bestMatch.tags.join(" · ")}
            </p>
          )}
        </div>
      )}

      <p className="mt-3 text-xs text-[var(--muted)]">
        This is a visual MVP of the AI search experience.
      </p>
    </section>
  );
}

