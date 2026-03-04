import { 
  IntroModal, 
  HeroSection, 
  ProblemSolutionSection, 
  HowItWorksSection, 
  MarketplaceSection, 
  FeaturesSection, 
  FinalCTASection, 
} from "@/features/home";
import { Header, Footer } from "@/shared/ui/layout";

export default function Home() {
  return (
    <div className="min-h-screen gradient-mesh bg-[var(--background)] text-[var(--foreground)]">
      <IntroModal />
      <Header />

      <main>
        <FinalCTASection />
        <HeroSection />
        <ProblemSolutionSection />
        <HowItWorksSection />
        <MarketplaceSection />
        <FeaturesSection />
        <Footer />
      </main>
    </div>
  );
}
