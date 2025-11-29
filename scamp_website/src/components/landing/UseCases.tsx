'use client';
import Link from 'next/link';
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { ArrowRight, Briefcase, Building, GraduationCap, HeartHandshake } from 'lucide-react';
import { TELEGRAM_CTA_LINK } from './constants';
import { motion } from 'framer-motion';

const useCases = [
  {
    icon: <Briefcase className="h-8 w-8 text-accent" />,
    title: "Gig & Freelance Workers",
    copy: "Avoid fake 'urgent payment' or 'advance refund' scams from unknown clients or impersonated platforms.",
    cta: "Protect my gigs"
  },
  {
    icon: <Building className="h-8 w-8 text-accent" />,
    title: "Small Businesses",
    copy: "Verify new vendors or customers before large UPI transfers, and get alerted when something feels off.",
    cta: "Protect my business"
  },
  {
    icon: <GraduationCap className="h-8 w-8 text-accent" />,
    title: "Students",
    copy: "Spot fake internships, job offers, or loan scams powered by AI-generated emails and calls.",
    cta: "Protect my future"
  },
  {
    icon: <HeartHandshake className="h-8 w-8 text-accent" />,
    title: "Families & Seniors",
    copy: "Detect fake voice/video of relatives asking for money, and guide them through safe steps.",
    cta: "Protect my family"
  }
];

export default function UseCases() {
  return (
    <motion.section
      id="for-businesses"
      className="py-12 sm:py-16 lg:py-20"
      initial={{ opacity: 0, y: 50 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, amount: 0.2 }}
      transition={{ duration: 0.5 }}
    >
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="text-center">
          <h2 className="font-headline text-3xl font-bold tracking-tight text-foreground sm:text-4xl">
            Built for Real People, For Real-Life Scams
          </h2>
          <p className="mt-4 max-w-2xl mx-auto text-lg text-muted-foreground">
            Scamp is designed to protect the people most targeted by digital fraud.
          </p>
        </div>

        <div className="mt-12 grid gap-8 sm:grid-cols-2 lg:grid-cols-4">
          {useCases.map((useCase, i) => (
            <motion.div
              key={useCase.title}
              initial={{ opacity: 0, y: 50 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, amount: 0.5 }}
              transition={{ duration: 0.5, delay: i * 0.1 }}
            >
              <Card className="bg-gradient-to-br from-slate-900 to-slate-800/80 border-slate-800 flex flex-col transition-all duration-300 hover:border-accent hover:-translate-y-1 h-full">
                <CardHeader>
                  {useCase.icon}
                  <CardTitle className="mt-4 font-headline text-lg font-semibold">{useCase.title}</CardTitle>
                </CardHeader>
                <CardContent className="flex-1 flex flex-col justify-between">
                  <p className="text-muted-foreground">{useCase.copy}</p>
                  <Link href={TELEGRAM_CTA_LINK} className="mt-6 inline-flex items-center text-sm font-semibold text-accent hover:text-accent/90">
                    {useCase.cta}
                    <ArrowRight className="ml-2 h-4 w-4" />
                  </Link>
                </CardContent>
              </Card>
            </motion.div>
          ))}
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
