'use client';
import Link from 'next/link';
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { TELEGRAM_CTA_LINK } from './constants';
import { motion } from 'framer-motion';

const stats = [
  { value: "₹1,000+ crore", label: "Reported scam losses in India every year." },
  { value: "900M+", label: "Indians using WhatsApp & Telegram — prime targets." },
  { value: "Seconds", label: "All scammers need to make a fake voice or video." }
];

export default function Problem() {
  return (
    <motion.section
      id="problem"
      className="py-12 sm:py-16 lg:py-20"
      initial={{ opacity: 0, y: 50 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, amount: 0.2 }}
      transition={{ duration: 0.5 }}
    >
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="text-center">
          <p className="text-base font-semibold uppercase tracking-wider text-accent">The Deepfake Scam Epidemic</p>
          <h2 className="mt-2 font-headline text-3xl font-bold tracking-tight text-foreground sm:text-4xl">
            Deepfake scams are exploding—and most people never see them coming.
          </h2>
          <p className="mt-4 max-w-3xl mx-auto text-lg text-muted-foreground">
            From fake boss/relative calls using AI-generated voices to UPI payment fraud, scammers are getting smarter. Traditional methods can't keep up.
          </p>
        </div>

        <div className="mt-12 grid grid-cols-1 gap-8 sm:grid-cols-2 lg:grid-cols-3">
          {stats.map((stat, i) => (
            <motion.div
              key={stat.label}
              initial={{ opacity: 0, y: 50 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, amount: 0.5 }}
              transition={{ duration: 0.5, delay: i * 0.2 }}
            >
              <Card className="bg-gradient-to-br from-slate-900 to-slate-800/80 border-slate-800 text-center h-full">
                <CardContent className="p-6">
                  <p className="font-headline text-4xl font-bold text-primary">{stat.value}</p>
                  <p className="mt-2 text-base text-muted-foreground">{stat.label}</p>
                </CardContent>
              </Card>
            </motion.div>
          ))}
        </div>
        
        <div className="mt-12 text-center">
            <Button asChild size="lg">
                <Link href={TELEGRAM_CTA_LINK}>Start Free on Telegram</Link>
            </Button>
        </div>
      </div>
    </motion.section>
  )
}
