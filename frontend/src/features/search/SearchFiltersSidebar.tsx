"use client";

type Category = { id: string; label: string };

type SearchFiltersSidebarProps = {
  selectedCategory: Category;
  maxPrice: string;
  onMaxPriceChange: (value: string) => void;
};

export function SearchFiltersSidebar({
  selectedCategory,
  maxPrice,
  onMaxPriceChange,
}: SearchFiltersSidebarProps) {
  return (
    <aside className="rounded-2xl border border-[var(--lilac-200)]/70 bg-white/80 p-5 shadow-sm">
      <p className="text-xs font-semibold uppercase tracking-wider text-[var(--muted)]">
        Categories &amp; price
      </p>
      <div className="mt-4 flex flex-col items-stretch gap-3 sm:flex-row sm:items-center sm:justify-between">
        <div className="w-full py-2">
          <label className="mb-[6px] block text-xs font-semibold uppercase tracking-wider text-[var(--muted)]">
            Category
          </label>
          <button
            type="button"
            className="h-[38px] w-full rounded-xl rounded-full bg-[var(--lilac-500)] px-2 py-0.5 text-[10px] uppercase tracking-wide text-white"
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
            onChange={(e) => onMaxPriceChange(e.target.value)}
            placeholder="e.g. 800"
            className="mt-1 w-full rounded-xl border border-[var(--lilac-200)] bg-white px-3 py-2 text-sm text-[var(--foreground)] shadow-sm outline-none focus:border-[var(--lilac-500)] focus:ring-2 focus:ring-[var(--lilac-300)]"
          />
        </div>
      </div>
      <p className="mt-4 text-xs text-[var(--muted)]">
        More categories will be added in future versions of the MVP.
      </p>
    </aside>
  );
}

