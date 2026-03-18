import type { ButtonHTMLAttributes, ReactNode } from "react";

type ButtonAppearance = "primary" | "secondary" | "outline" | "ghost";

type ButtonProps = {
  appearance?: ButtonAppearance;
  children: ReactNode;
} & ButtonHTMLAttributes<HTMLButtonElement>;

export function Button({
  appearance = "primary",
  className = "",
  children,
  ...props
}: ButtonProps) {
  const base =
    "inline-flex items-center justify-center rounded-xl text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[var(--lilac-300)] disabled:opacity-60 disabled:cursor-not-allowed";

  const variants: Record<ButtonAppearance, string> = {
    primary:
      "bg-[var(--lilac-500)] text-white hover:bg-[var(--lilac-600)] px-4 py-2 shadow-md",
    secondary:
      "bg-white text-[var(--lilac-700)] border border-[var(--lilac-300)] hover:bg-[var(--lilac-50)] px-4 py-2 shadow-sm",
    outline:
      "bg-transparent text-[var(--lilac-700)] border border-[var(--lilac-300)] hover:bg-[var(--lilac-50)] px-3 py-1.5",
    ghost:
      "bg-transparent text-[var(--lilac-700)] hover:bg-[var(--lilac-50)] px-2 py-1.5",
  };

  const appearanceClasses = variants[appearance];

  return (
    <button
      type="button"
      className={`${base} ${appearanceClasses} ${className}`}
      {...props}
    >
      {children}
    </button>
  );
}

