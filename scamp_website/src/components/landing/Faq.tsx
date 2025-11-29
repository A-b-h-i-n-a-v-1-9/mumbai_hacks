'use client';
import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "@/components/ui/accordion"
import { Button } from "@/components/ui/button"
import { motion } from 'framer-motion';

const faqs = [
  {
    question: "Does Scamp read all my messages?",
    answer: "No. Scamp prioritizes your privacy. It uses on-device processing where possible and only analyzes message metadata and content when you explicitly forward it or when a high-risk pattern is detected, all with end-to-end encryption. You have full control over its permissions."
  },
  {
    question: "How accurate is the deepfake detection?",
    answer: "Our detection models are constantly updated and achieve high accuracy (above 90% for Pro users) on known deepfake generation techniques. However, no system is perfect. Scamp is designed to be a powerful co-pilot, giving you a strong signal to be cautious, not a guarantee."
  },
  {
    question: "Will Scamp work with Hindi and regional languages?",
    answer: "Yes! Scamp is being trained on a diverse dataset including Hindi, Hinglish, and other major Indian regional languages. The adaptive learning agent gets better at understanding local scam nuances as more users in a region use it."
  },
  {
    question: "Do I need to install a separate app?",
    answer: "No. The core functionality of Scamp works directly within Telegram. For web protection, a lightweight Chrome extension will be available, but it's not required to start protecting your chats."
  },
  {
    question: "Can I use Scamp with my team or business?",
    answer: "Absolutely. We have Small Business and Enterprise plans designed to protect teams, verify vendor payments, and monitor merchant accounts for suspicious activity. These plans include a shared dashboard and advanced support."
  },
  {
    question: "What happens if a scam still gets through?",
    answer: "While Scamp significantly reduces your risk, determined scammers can still find ways. If you are a victim, Scamp helps by auto-drafting a detailed cybercrime report with all available evidence, making it easier for you to file a complaint with the authorities."
  }
];

export default function Faq() {
  return (
    <motion.section
      id="faq"
      className="py-12 sm:py-16 lg:py-20"
      initial={{ opacity: 0, y: 50 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, amount: 0.2 }}
      transition={{ duration: 0.5 }}
    >
      <div className="mx-auto max-w-4xl px-4 sm:px-6 lg:px-8">
        <div className="text-center">
          <h2 className="font-headline text-3xl font-bold tracking-tight text-foreground sm:text-4xl">
            Frequently Asked Questions
          </h2>
          <p className="mt-4 text-lg text-muted-foreground">
            Find answers to common questions about Scamp.
          </p>
        </div>
        <Accordion type="single" collapsible className="mt-12 w-full">
          {faqs.map((faq, index) => (
            <AccordionItem key={index} value={`item-${index}`}>
              <AccordionTrigger className="text-left">{faq.question}</AccordionTrigger>
              <AccordionContent className="text-base text-muted-foreground">
                {faq.answer}
              </AccordionContent>
            </AccordionItem>
          ))}
        </Accordion>
        <div className="mt-12 text-center">
          <p className="text-lg text-muted-foreground">Still have questions?</p>
          <Button size="lg" className="mt-4">Talk to us</Button>
        </div>
      </div>
    </motion.section>
  )
}
