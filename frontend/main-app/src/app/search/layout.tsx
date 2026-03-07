import { Header, Footer } from "@/shared/ui/layout";

export default function SearchLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="min-h-screen gradient-mesh bg-[var(--background)] text-[var(--foreground)]">
      <Header />
      <main className="pt-16 pb-16">{children}</main>
      <Footer />
    </div>
  );
}
