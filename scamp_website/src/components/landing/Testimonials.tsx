'use client';
import Link from 'next/link';
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { TELEGRAM_CTA_LINK } from './constants';
import { motion } from 'framer-motion';

const testimonials = [
  {
    quote: "Scamp flagged a fake voice note pretending to be my manager and literally saved me ₹25,000.",
    name: "Ravi K.",
    title: "Freelancer",
    initials: "RK"
  },
  {
    quote: "The risk score gave me the confidence to ignore a fake vendor request. The explanation was simple enough for my parents too.",
    name: "Priya S.",
    title: "Small Business Owner",
    initials: "PS"
  },
  {
    quote: "As a student, I get so many spam job offers. Scamp helps me filter out the obvious fakes in seconds. A must-have tool.",
    name: "Anjali M.",
    title: "Student",
    initials: "AM"
  }
];

export default function Testimonials() {
  return (
    <motion.section
      id="testimonials"
      className="py-12 sm:py-16 lg:py-20"
      initial={{ opacity: 0, y: 50 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, amount: 0.2 }}
      transition={{ duration: 0.5 }}
    >
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="text-center">
          <p className="text-base font-semibold uppercase tracking-wider text-accent">Loved by early users</p>
          <h2 className="mt-2 font-headline text-3xl font-bold tracking-tight text-foreground sm:text-4xl">
            Scamp has already stopped scams like these...
          </h2>
        </div>
        <div className="mt-12 grid grid-cols-1 gap-8 md:grid-cols-2 lg:grid-cols-3">
          {testimonials.map((testimonial, i) => (
            <motion.div
              key={testimonial.name}
              initial={{ opacity: 0, y: 50 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, amount: 0.5 }}
              transition={{ duration: 0.5, delay: i * 0.2 }}
            >
              <Card className="bg-gradient-to-br from-slate-900 to-slate-800/80 border-slate-800 flex flex-col h-full">
                <CardContent className="p-6 flex-1 flex flex-col justify-between">
                  <blockquote className="text-lg text-foreground">
                    " {testimonial.quote} "
                  </blockquote>
                  <div className="mt-6 flex items-center">
                    <Avatar>
                      <AvatarFallback className="bg-primary text-primary-foreground">{testimonial.initials}</AvatarFallback>
                    </Avatar>
                    <div className="ml-4">
                      <p className="font-semibold text-foreground">{testimonial.name}</p>
                      <p className="text-sm text-muted-foreground">{testimonial.title}</p>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </motion.div>
          ))}
        </div>
        <div className="mt-16 text-center">
          <Button asChild size="lg">
            <Link href={TELEGRAM_CTA_LINK}>Start protecting yourself</Link>
          </Button>
        </div>
      </div>
    </motion.section>
  )
}
