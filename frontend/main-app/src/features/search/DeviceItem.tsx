import { useState } from "react";

type DeviceItemProps = {
  name: string;
  price?: number | null;
  short_description: string;
  key_features: string[];
};

export function DeviceItem({ name, price, short_description, key_features }: DeviceItemProps) {
  const [open, setOpen] = useState(false);

  return (
    <div className="flex flex-col gap-3 rounded-xl border border-[var(--lilac-200)] bg-[var(--lilac-50)]/50 p-4 mt-4">
      <details
        open={open}
      >
        <summary
          className="cursor-pointer list-none select-none"
          onClick={(e) => {
            e.preventDefault();
            setOpen((prev) => !prev);
          }}
        >
          <div className="flex items-start justify-between gap-3">
            <div className="min-w-0">
              <p className="text-large font-semibold uppercase tracking-wider text-[var(--muted)]">
                {name}
              </p>
              <p className="mt-1 font-semibold text-[var(--foreground)]">Price: {price}</p>
            </div>

            <button
              type="button"
              aria-label={open ? "Collapse" : "Expand"}
              className="inline-flex h-9 w-9 flex-none items-center justify-center rounded-full border border-[var(--lilac-200)] bg-white/70 text-[var(--foreground)] shadow-sm hover:bg-white"
              onClick={(e) => {
                e.preventDefault();
                e.stopPropagation();
                setOpen((prev) => !prev);
              }}
            >
              {open ? (
                <svg
                  width="18"
                  height="18"
                  viewBox="0 0 20 20"
                  fill="none"
                  xmlns="http://www.w3.org/2000/svg"
                  aria-hidden="true"
                >
                  <path
                    d="M5.5 12.5L10 8l4.5 4.5"
                    stroke="currentColor"
                    strokeWidth="2"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                  />
                </svg>
              ) : (
                <svg
                  width="18"
                  height="18"
                  viewBox="0 0 20 20"
                  fill="none"
                  xmlns="http://www.w3.org/2000/svg"
                  aria-hidden="true"
                >
                  <path
                    d="M5.5 7.5L10 12l4.5-4.5"
                    stroke="currentColor"
                    strokeWidth="2"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                  />
                </svg>
              )}
            </button>
          </div>
        </summary>

        <div className="mt-3 rounded-xl border border-[var(--lilac-200)] bg-white/70 px-3 py-2">
          <p className="whitespace-pre-wrap text-sm text-[var(--foreground)]" dangerouslySetInnerHTML={{ __html: short_description }} />
        </div>
      </details>
      {key_features?.length > 0 && <div className="mt-3 rounded-xl border border-[var(--lilac-200)] bg-white/70 px-3 py-2"> • {key_features.join(" • ")}</div>}
    </div>
  );
}