"use client";

import Link from "next/link";
import Image from "next/image";
import { useState } from "react";

const navLinks = [
  { href: "#problem-solution", label: "Problem / Solution" },
  { href: "#how-it-works", label: "How it works" },
  { href: "#marketplace", label: "Marketplace" },
  { href: "#features", label: "Features" }
];

export function LandingHeader() {
  const [open, setOpen] = useState(false);

  return (
    <header className="fixed top-0 left-0 right-0 z-50 border-b border-[var(--lilac-200)]/40 bg-[var(--background)]/80 backdrop-blur-md">
      <div className="mx-auto flex h-16 max-w-6xl items-center justify-between px-4 sm:px-6 lg:px-8">
        <Link
          href="/"
          className="flex items-center text-xl font-semibold tracking-tight text-[var(--lilac-700)]"
        >
          <Image src="/logo.svg" alt="PackMan" width={90} height={80} />
          <span className="ml-2 hidden sm:inline">PackMan</span>
        </Link>

        {/* Desktop nav */}
        <nav className="hidden items-center gap-6 text-sm font-medium text-[var(--muted)] md:flex">
          {navLinks.map((item) => (
            <Link
              key={item.href}
              href={item.href}
              className="hover:text-[var(--lilac-600)] transition-colors"
            >
              {item.label}
            </Link>
          ))}
          <Link
            href="#hero-search"
            className="rounded-full bg-[var(--lilac-500)] px-4 py-2 text-white hover:bg-[var(--lilac-600)] transition-colors"
          >
            Try AI Search
          </Link>
        </nav>

        {/* Mobile menu button */}
        <button
          type="button"
          className="inline-flex items-center justify-center rounded-full border border-[var(--lilac-200)] bg-white/70 px-3 py-2 text-sm font-medium text-[var(--foreground)] shadow-sm hover:bg-white md:hidden"
          aria-label="Toggle navigation"
          onClick={() => setOpen((prev) => !prev)}
        >
          <span className="mr-2 text-xs">Menu</span>
          <span className="flex h-4 w-4 flex-col justify-between">
            <span
              className={`h-[2px] w-full rounded bg-[var(--foreground)] transition-transform ${
                open ? "translate-y-[6px] rotate-45" : ""
              }`}
            />
            <span
              className={`h-[2px] w-full rounded bg-[var(--foreground)] transition-opacity ${
                open ? "opacity-0" : ""
              }`}
            />
            <span
              className={`h-[2px] w-full rounded bg-[var(--foreground)] transition-transform ${
                open ? "-translate-y-[6px] -rotate-45" : ""
              }`}
            />
          </span>
        </button>
      </div>

      {/* Mobile nav */}
      {open && (
        <div className="border-t border-[var(--lilac-200)]/40 bg-[var(--background)]/95 backdrop-blur-md md:hidden">
          <nav className="mx-auto flex max-w-6xl flex-col gap-1 px-4 py-3 text-sm font-medium text-[var(--foreground)]">
            {navLinks.map((item) => (
              <Link
                key={item.href}
                href={item.href}
                className="rounded-lg px-2 py-2 hover:bg-[var(--lilac-50)]"
                onClick={() => setOpen(false)}
              >
                {item.label}
              </Link>
            ))}
            <Link
              href="#hero-search"
              className="mt-2 inline-flex items-center justify-center rounded-xl bg-[var(--lilac-500)] px-4 py-2 text-white hover:bg-[var(--lilac-600)]"
              onClick={() => setOpen(false)}
            >
              Try AI Search
            </Link>
          </nav>
        </div>
      )}
    </header>
  );
}

