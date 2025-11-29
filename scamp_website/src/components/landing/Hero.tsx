import Image from 'next/image';
import Link from 'next/link';
import { Button } from '@/components/ui/button';
import { Check } from 'lucide-react';
import { PlaceHolderImages } from '@/lib/placeholder-images';
import { TELEGRAM_CTA_LINK } from './constants';

const heroImage = PlaceHolderImages.find((img) => img.id === 'hero-mockup');

export default function Hero() {
  return (
    <section id="hero" className="relative overflow-hidden bg-slate-950">
      <div className="absolute inset-0 bg-gradient-to-b from-background to-transparent opacity-30"></div>
      <div className="container relative py-16 sm:py-24 lg:py-32">
        <div className="grid grid-cols-1 gap-12 lg:grid-cols-2 lg:gap-8">
          <div className="flex flex-col justify-center text-center lg:text-left">
            <p className="text-base font-semibold uppercase tracking-wider text-accent">
              AI Scam Protection for WhatsApp, Telegram & Web
            </p>
            <h1 className="mt-4 font-headline text-4xl font-extrabold tracking-tight text-foreground sm:text-5xl md:text-6xl">
              Stop Deepfake Scams Before They Drain Your Wallet.
            </h1>
            <p className="mt-6 text-lg text-muted-foreground sm:text-xl">
              Scamp is an AI-powered chat bodyguard that scans messages, calls, and media in real time, scores scam risk, and explains exactly why something looks suspicious — so you don’t get fooled.
            </p>
            <div className="mt-10 flex flex-col sm:flex-row items-center justify-center lg:justify-start gap-4">
              <Button asChild size="lg">
                <Link href={TELEGRAM_CTA_LINK}>Use Scamp on Telegram</Link>
              </Button>
              <Button asChild variant="outline" size="lg">
                <Link href="#">Watch Demo</Link>
              </Button>
            </div>
            <ul className="mt-8 flex flex-col sm:flex-row items-center justify-center lg:justify-start gap-x-6 gap-y-2 text-sm text-muted-foreground">
              <li className="flex items-center gap-2">
                <Check className="h-4 w-4 text-primary" />
                Works with WhatsApp & Telegram
              </li>
              <li className="flex items-center gap-2">
                <Check className="h-4 w-4 text-primary" />
                Deepfake & scam detection
              </li>
              <li className="flex items-center gap-2">
                <Check className="h-4 w-4 text-primary" />
                Simple explanations
              </li>
            </ul>
          </div>
          <div className="flex items-center justify-center">
            {heroImage && (
              <Image
                src={heroImage.imageUrl}
                alt={heroImage.description}
                data-ai-hint={heroImage.imageHint}
                width={500}
                height={700}
                className="rounded-xl shadow-2xl shadow-primary/10 transform-gpu transition-all duration-300 hover:scale-105"
                priority
              />
            )}
          </div>
        </div>
      </div>
    </section>
  );
}
