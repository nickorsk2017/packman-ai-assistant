"use client";

import { useEffect, useState } from "react";

const STORAGE_KEY = "packman_intro_seen";

export function IntroModal() {
  const [open, setOpen] = useState(false);

  useEffect(() => {
    if (typeof window === "undefined") return;
    const seen = window.localStorage.getItem(STORAGE_KEY);
    if (!seen) {
      setOpen(true);
    }
  }, []);

  const handleClose = (hide: boolean) => {
    if (typeof window !== "undefined" && hide) {
      window.localStorage.setItem(STORAGE_KEY, "true");
    }
    setOpen(false);
  };

  if (!open) return null;

  return (
    <div className="fixed inset-0 z-[60] flex items-center justify-center bg-black/40 backdrop-blur-sm px-4">
      <div className="max-w-lg rounded-3xl bg-white p-6 shadow-2xl sm:p-8">
        <h2 className="text-xl font-semibold text-[var(--foreground)] sm:text-2xl">
          PackMan Demo MVP
        </h2>
        <div className="mt-4 space-y-3 text-sm leading-relaxed text-[var(--muted)] sm:text-base">

          <p>
            The AI-powered assistant for fast product discovery.
          </p>
          <p>
            It helps users discover the right product in under a minute.
          </p>
          <p>This version is built for presentation and technical evaluation purposes.</p>

          <a
            href="https://www.linkedin.com/in/nickot"
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-2 rounded-full border border-[var(--lilac-300)] bg-white px-4 py-1.5 text-xs font-medium text-[var(--lilac-700)] shadow-sm hover:bg-[var(--lilac-50)]"
          >
            <span>View LinkedIn Author</span>
          </a>
        </div>
        <div className="mt-6 flex justify-end gap-3">
          <button
            type="button"
            onClick={() => handleClose(false)}
            className="rounded-xl border border-[var(--lilac-200)] bg-white px-4 py-2 text-sm font-medium text-[var(--foreground)] hover:bg-[var(--lilac-50)]"
          >
            Close
          </button>
          <button
            type="button"
            onClick={() => handleClose(true)}
            className="rounded-xl bg-[var(--lilac-500)] px-4 py-2 text-sm font-semibold text-white shadow-md hover:bg-[var(--lilac-600)]"
          >
            Got it
          </button>
        </div>
      </div>
    </div>
  );
}

