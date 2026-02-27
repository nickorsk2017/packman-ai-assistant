import { LandingHeader } from "./components/LandingHeader";
import { HeroSection } from "./components/HeroSection";
import { ProblemSolutionSection } from "./components/ProblemSolutionSection";
import { HowItWorksSection } from "./components/HowItWorksSection";
import { MarketplaceSection } from "./components/MarketplaceSection";
import { FeaturesSection } from "./components/FeaturesSection";
import { FinalCTASection } from "./components/FinalCTASection";
import { LandingFooter } from "./components/LandingFooter";
import { IntroModal } from "./components/IntroModal";

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
