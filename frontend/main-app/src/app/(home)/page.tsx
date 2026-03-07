import {
  IntroModal,
  HeroSection,
  ProblemSolutionSection,
  HowItWorksSection,
  MarketplaceSection,
  FeaturesSection,
  FinalCTASection,
} from "@/features/home";

export default function Home() {
  return (
    <>
      <IntroModal />
      <FinalCTASection />
      <HeroSection />
      <ProblemSolutionSection />
      <HowItWorksSection />
      <MarketplaceSection />
      <FeaturesSection />
    </>
  );
}
