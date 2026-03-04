import { 
  IntroModal, 
  HeroSection, 
  ProblemSolutionSection, 
  HowItWorksSection, 
  MarketplaceSection, 
  FeaturesSection, 
  FinalCTASection, 
} from "@/features/home";
import { LandingHeader, LandingFooter } from "@/features/common";

export default function Home() {
  return (
    <div className="min-h-screen gradient-mesh bg-[var(--background)] text-[var(--foreground)]">
      <IntroModal />
      <LandingHeader />

      <main>
        <FinalCTASection />
        <HeroSection />
        <ProblemSolutionSection />
        <HowItWorksSection />
        <MarketplaceSection />
        <FeaturesSection />
        <LandingFooter />
      </main>
    </div>
  );
}
