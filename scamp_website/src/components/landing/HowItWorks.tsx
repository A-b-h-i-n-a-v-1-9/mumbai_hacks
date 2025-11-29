'use client';
import Link from 'next/link';
import { Button } from "@/components/ui/button";
import { TELEGRAM_CTA_LINK } from './constants';
import { motion } from 'framer-motion';

const steps = [
  {
    step: 1,
    title: "Start Scamp on Telegram",
    description: "Launch the bot and grant basic permissions. No complex setup, no app store install needed."
  },
  {
    step: 2,
    title: "Scamp watches your risky moments",
    description: "When a suspicious message, call, or payment request appears, Scamp analyzes it in seconds using deepfake and behavioral analysis."
  },
  {
    step: 3,
    title: "Get a risk score & explanation",
    description: "See the Scam Risk Score, understand why, and follow recommended actions like “don’t pay” or “verify identity”."
  }
];

export default function HowItWorks() {
  return (
    <motion.section
      id="how-it-works"
      className="py-12 sm:py-16 lg:py-20"
      initial={{ opacity: 0, y: 50 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, amount: 0.2 }}
      transition={{ duration: 0.5 }}
    >
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="text-center">
          <h2 className="font-headline text-3xl font-bold tracking-tight text-foreground sm:text-4xl">
            Scamp works in three simple steps.
          </h2>
          <p className="mt-4 max-w-2xl mx-auto text-lg text-muted-foreground">
            Get protected in under a minute. It's that easy.
          </p>
        </div>

        <div className="relative mt-12">
          <div className="absolute top-8 left-1/2 -ml-px h-[calc(100%-4rem)] w-px bg-slate-800 hidden md:block" aria-hidden="true" />
          <div className="grid gap-12 md:grid-cols-3">
            {steps.map((step, index) => (
              <motion.div
                key={step.step}
                className="relative text-center"
                initial={{ opacity: 0, y: 50 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true, amount: 0.5 }}
                transition={{ duration: 0.5, delay: index * 0.2 }}
              >
                <div className="flex justify-center items-center">
                   <div className="flex h-16 w-16 items-center justify-center rounded-full bg-slate-900 border-2 border-primary">
                    <span className="font-headline text-2xl font-bold text-primary">{step.step}</span>
                  </div>
                </div>
                <h3 className="mt-6 font-headline text-lg font-semibold text-foreground">
                  {step.title}
                </h3>
                <p className="mt-2 text-base text-muted-foreground">
                  {step.description}
                </p>
              </motion.div>
            ))}
          </div>
        </div>

        <div className="mt-16 text-center">
          <Button asChild size="lg">
            <Link href={TELEGRAM_CTA_LINK}>
              Start in under 30 seconds
            </Link>
          </Button>
        </div>
      </div>
    </motion.section>
  )
}
