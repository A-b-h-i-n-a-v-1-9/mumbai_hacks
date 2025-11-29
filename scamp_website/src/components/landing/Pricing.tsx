'use client';
import Link from 'next/link';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Check } from 'lucide-react';
import { cn } from '@/lib/utils';
import { TELEGRAM_CTA_LINK } from './constants';
import { motion } from 'framer-motion';

const plans = [
  {
    name: "Free",
    price: "₹0",
    period: "/ month",
    tagline: "Perfect for individuals and families getting started.",
    features: [
      "Basic scam & deepfake screening",
      "Approx. 90% accuracy alerts",
      "Scam Risk Score (limited detail)",
      "Up to 50 scans / month",
      "Basic cyber report template"
    ],
    cta: "Start Free on Telegram",
    href: TELEGRAM_CTA_LINK
  },
  {
    name: "Pro",
    price: "₹99",
    period: "/ month",
    tagline: "For heavy users who want stronger protection.",
    features: [
      "Enhanced accuracy & more advanced models",
      "Full risk score breakdown with explanations",
      "Unlimited scans",
      "Automated cybercrime report drafting",
      "Priority response for new scam types"
    ],
    cta: "Upgrade to Pro",
    href: "#",
    highlight: true
  },
  {
    name: "Small Business",
    price: "₹4,999",
    period: "/ month",
    tagline: "Protection for small teams and merchant accounts.",
    features: [
      "Up to 20 team members",
      "Merchant / vendor verification assistant",
      "Real-time alerts on suspicious customers",
      "Shared dashboard with incident history",
      "Direct support during business hours"
    ],
    cta: "Talk to Sales",
    href: "#"
  },
  {
    name: "Enterprise",
    price: "Custom",
    period: "",
    tagline: "Custom protection for banks, platforms, and large teams.",
    features: [
      "Custom SLAs and onboarding",
      "API & webhook access to risk engine",
      "Safe payment tracking & anomaly alerts",
      "Dedicated account manager",
      "Security & compliance reporting"
    ],
    cta: "Book a Demo",
    href: "#"
  }
];

export default function Pricing() {
  return (
    <motion.section
      id="pricing"
      className="py-12 sm:py-16 lg:py-20 bg-slate-950"
      initial={{ opacity: 0, y: 50 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, amount: 0.2 }}
      transition={{ duration: 0.5 }}
    >
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="text-center">
          <p className="text-base font-semibold uppercase tracking-wider text-accent">Pricing</p>
          <h2 className="mt-2 font-headline text-3xl font-bold tracking-tight text-foreground sm:text-4xl">
            Simple plans for everyone
          </h2>
          <p className="mt-4 max-w-2xl mx-auto text-lg text-muted-foreground">
            Start free. Upgrade only if you need more protection and support.
          </p>
        </div>

        <div className="mt-12 grid max-w-md grid-cols-1 gap-8 mx-auto lg:max-w-none lg:grid-cols-4">
          {plans.map((plan, i) => (
            <motion.div
              key={plan.name}
              initial={{ opacity: 0, y: 50 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, amount: 0.5 }}
              transition={{ duration: 0.5, delay: i * 0.1 }}
              className="flex flex-col h-full"
            >
              <Card className={cn(
                "flex flex-col flex-1 bg-gradient-to-br from-slate-900 to-slate-800/80 border-slate-800",
                plan.highlight && "border-2 border-primary shadow-2xl shadow-primary/20"
              )}>
                <CardHeader className="relative">
                  {plan.highlight && <Badge className="absolute top-0 right-6 -translate-y-1/2">Most Popular</Badge>}
                  <Badge variant={plan.highlight ? "default" : "secondary"}>{plan.name}</Badge>
                  <CardTitle className="mt-4">
                    <span className="font-headline text-4xl">{plan.price}</span>
                    <span className="text-base font-medium text-muted-foreground">{plan.period}</span>
                  </CardTitle>
                  <CardDescription>{plan.tagline}</CardDescription>
                </CardHeader>
                <CardContent className="flex-1">
                  <ul className="space-y-3">
                    {plan.features.map((feature) => (
                      <li key={feature} className="flex items-start">
                        <Check className="h-5 w-5 mr-2 text-primary shrink-0" />
                        <span className="text-sm text-muted-foreground">{feature}</span>
                      </li>
                    ))}
                  </ul>
                </CardContent>
                <CardFooter>
                  <Button asChild className="w-full" variant={plan.highlight ? "default" : "outline"}>
                    <Link href={plan.href}>{plan.cta}</Link>
                  </Button>
                </CardFooter>
              </Card>
            </motion.div>
          ))}
        </div>

        <div className="mt-12 text-center">
          <p className="text-muted-foreground">
            Need a custom plan? <Link href="#" className="font-medium text-primary hover:underline">Contact us</Link>
          </p>
        </div>
      </div>
    </motion.section>
  )
}
