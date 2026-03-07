import { Header, Footer } from "@/shared/ui/layout";

export default function HomeLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="min-h-screen gradient-mesh bg-[var(--background)] text-[var(--foreground)]">
      <Header />
      <main>{children}</main>
      <Footer />
    </div>
  );
}
