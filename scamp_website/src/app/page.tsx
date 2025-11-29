import Header from '@/components/landing/Header';
import Hero from '@/components/landing/Hero';
import Problem from '@/components/landing/Problem';
import ValueProp from '@/components/landing/ValueProp';
import Features from '@/components/landing/Features';
import HowItWorks from '@/components/landing/HowItWorks';
import UseCases from '@/components/landing/UseCases';
import Pricing from '@/components/landing/Pricing';
import Testimonials from '@/components/landing/Testimonials';
import Faq from '@/components/landing/Faq';
import Footer from '@/components/landing/Footer';

export default function Home() {
  return (
    <div className="flex min-h-screen flex-col bg-background">
      <Header />
      <main className="flex-1">
        <Hero />
        <Problem />
        <ValueProp />
        <Features />
        <HowItWorks />
        <UseCases />
        <Pricing />
        <Testimonials />
        <Faq />
      </main>
      <Footer />
    </div>
  );
}
