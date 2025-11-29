'use client';
import Link from 'next/link';
import { Button } from "@/components/ui/button";
import { BookText, GaugeCircle, LifeBuoy, ScanSearch } from 'lucide-react';
import { TELEGRAM_CTA_LINK } from './constants';
import { motion } from 'framer-motion';

const coreValues = [
  {
    icon: <ScanSearch className="h-6 w-6 text-accent" />,
    text: "Detects deepfakes & scams"
  },
  {
    icon: <GaugeCircle className="h-6 w-6 text-accent" />,
    text: "Scores scam risk from 0-100"
  },
  {
    icon: <BookText className="h-6 w-6 text-accent" />,
    text: "Explains risk in simple language"
  },
  {
    icon: <LifeBuoy className="h-6 w-6 text-accent" />,
    text: "Helps you report & recover"
  }
];

export default function ValueProp() {
  return (
    <motion.section
      id="value-prop"
      className="py-12 sm:py-16 lg:py-20 bg-slate-950"
      initial={{ opacity: 0, y: 50 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, amount: 0.2 }}
      transition={{ duration: 0.5 }}
    >
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="text-center">
          <p className="text-base font-semibold uppercase tracking-wider text-accent">What is Scamp?</p>
          <h2 className="mt-2 font-headline text-3xl font-bold tracking-tight text-foreground sm:text-4xl">
            Your always-on AI bodyguard inside your chats.
          </h2>
          <p className="mt-4 max-w-3xl mx-auto text-lg text-muted-foreground">
            Scamp connects to your chat apps and web sessions, analyzes messages and media using deepfake detection and behavioral AI, then alerts you in real time with a risk score and an easy explanation.
          </p>
        </div>

        <div className="mt-12">
          <div className="grid grid-cols-2 gap-8 md:grid-cols-4">
            {coreValues.map((value, i) => (
              <motion.div
                key={value.text}
                className="flex flex-col items-center text-center"
                initial={{ opacity: 0, y: 50 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true, amount: 0.5 }}
                transition={{ duration: 0.5, delay: i * 0.1 }}
              >
                <div className="flex h-12 w-12 items-center justify-center rounded-lg bg-slate-900 border border-slate-800">
                  {value.icon}
                </div>
                <p className="mt-4 text-sm font-medium text-foreground">{value.text}</p>
              </motion.div>
            ))}
          </div>
        </div>

        <div className="mt-16 text-center">
          <Button asChild size="lg">
            <Link href={TELEGRAM_CTA_LINK}>Use Scamp on Telegram</Link>
          </Button>
        </div>
      </div>
    </motion.section>
  )
}
