'use client';
import Link from 'next/link';
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { ArrowRight, Bot, FileText, GaugeCircle, ScanSearch, Sparkles, Users } from 'lucide-react';
import { TELEGRAM_CTA_LINK } from './constants';
import { motion } from 'framer-motion';

const features = [
  {
    icon: <ScanSearch className="h-8 w-8 text-accent" />,
    title: "Real-time scam & deepfake detection",
    body: "Scamp screens audio, video, images, and text for impersonation, tampering, and scam scripts as soon as they appear in your chat.",
    tag: "MVP",
    cta: { text: "See detection in action", href: TELEGRAM_CTA_LINK }
  },
  {
    icon: <GaugeCircle className="h-8 w-8 text-accent" />,
    title: "Clear risk score for every request",
    body: "Each suspicious message, call, or payment request gets a 0–100 Scam Risk Score with labels like Safe, Caution, High, or Critical.",
    cta: { text: "Check your risk", href: TELEGRAM_CTA_LINK }
  },
  {
    icon: <Sparkles className="h-8 w-8 text-accent" />,
    title: "Explainable AI you can understand",
    body: "No black box decisions — Scamp breaks down why something looks risky in everyday language, like “Voice doesn’t match past samples.”",
    cta: { text: "View explanation sample", href: TELEGRAM_CTA_LINK }
  },
  {
    icon: <FileText className="h-8 w-8 text-accent" />,
    title: "One-tap cybercrime reports",
    body: "If a scam happens, Scamp auto-drafts a detailed report with evidence you can submit to cyber cells and portals.",
    cta: { text: "Generate a report", href: TELEGRAM_CTA_LINK }
  },
  {
    icon: <Bot className="h-8 w-8 text-accent" />,
    title: "Adaptive Learning Agent",
    body: "Mark messages as scam or safe, and Scamp’s agent improves its patterns for your region and language.",
    cta: { text: "Help train Scamp", href: TELEGRAM_CTA_LINK }
  },
  {
    icon: <Users className="h-8 w-8 text-accent" />,
    title: "Chrome protection for web & WhatsApp Web",
    body: "Browser extension that flags risky websites, payment links, and web-based chats in real time.",
    badge: "Coming Soon",
    cta: { text: "Join waitlist", href: "#" }
  }
];

export default function Features() {
  return (
    <motion.section
      id="features"
      className="py-12 sm:py-16 lg:py-20 bg-slate-950"
      initial={{ opacity: 0, y: 50 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, amount: 0.2 }}
      transition={{ duration: 0.5 }}
    >
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="text-center">
          <p className="text-base font-semibold uppercase tracking-wider text-accent">Features</p>
          <h2 className="mt-2 font-headline text-3xl font-bold tracking-tight text-foreground sm:text-4xl">
            Everything you need to stay safe
          </h2>
          <p className="mt-4 max-w-2xl mx-auto text-lg text-muted-foreground">
            From real-time analysis to post-scam support, Scamp is your comprehensive digital bodyguard.
          </p>
        </div>

        <div className="mt-12 grid gap-8 sm:grid-cols-2 lg:grid-cols-3">
          {features.map((feature, i) => (
            <motion.div
              key={feature.title}
              initial={{ opacity: 0, y: 50 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, amount: 0.3 }}
              transition={{ duration: 0.5, delay: i * 0.1 }}
            >
              <Card className="bg-gradient-to-br from-slate-900 to-slate-800/80 border-slate-800 flex flex-col transition-all duration-300 hover:border-accent hover:-translate-y-1 h-full">
                <CardHeader className="flex-row items-start justify-between">
                  <div>
                    {feature.icon}
                    <CardTitle className="mt-4 font-headline text-lg font-semibold">{feature.title}</CardTitle>
                  </div>
                  {feature.tag && <Badge variant="secondary">{feature.tag}</Badge>}
                  {feature.badge && <Badge>{feature.badge}</Badge>}
                </CardHeader>
                <CardContent className="flex-1 flex flex-col justify-between">
                  <p className="text-muted-foreground">{feature.body}</p>
                  <Link href={feature.cta.href} className="mt-6 inline-flex items-center text-sm font-semibold text-accent hover:text-accent/90">
                    {feature.cta.text}
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
