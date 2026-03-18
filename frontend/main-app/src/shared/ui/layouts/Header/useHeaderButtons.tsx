"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

export const mainNavLinks = [
  { href: "#problem-solution", label: "Problem / Solution" },
  { href: "#how-it-works", label: "How it works" },
  { href: "#marketplace", label: "Marketplace" },
  { href: "#features", label: "Features" },
];

export function useHeaderButtons(): React.ReactNode {
  const pathname = usePathname();

  // Search layout: show "My added devices" only when not on my-devices page
  if (pathname === "/my-devices") return null;
  
  if (pathname === "/search") {
    return (
      <nav className="flex items-center">
        <Link
          href="/my-devices"
          className="rounded-full bg-[var(--lilac-500)] px-4 py-2 text-white hover:bg-[var(--lilac-600)] transition-colors text-sm font-medium"
        >
          My added devices
        </Link>
      </nav>
    );
  }

  // Home (main) layout: nav links + Try AI Search
  return (
    <nav className="hidden items-center gap-6 text-sm font-medium text-[var(--muted)] md:flex">
      {mainNavLinks.map((item) => (
        <Link
          key={item.href}
          href={item.href}
          className="hover:text-[var(--lilac-600)] transition-colors"
        >
          {item.label}
        </Link>
      ))}
      <Link
        href="/search"
        className="rounded-full bg-[var(--lilac-500)] px-4 py-2 text-white hover:bg-[var(--lilac-600)] transition-colors"
      >
        Try AI Search
      </Link>
    </nav>
  );
}
