import Link from 'next/link';
import { Shield } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { NAV_LINKS, TELEGRAM_CTA_LINK } from './constants';

const footerLinks = {
  company: NAV_LINKS,
  legal: [
    { href: '#', label: 'Privacy Policy' },
    { href: '#', label: 'Terms of Service' },
    { href: '#', label: 'Contact' }
  ]
};

export default function Footer() {
  return (
    <footer className="border-t border-slate-800 bg-slate-950">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 gap-8 md:grid-cols-12">
          <div className="md:col-span-4">
            <Link href="#" className="flex items-center gap-2">
              <Shield className="h-7 w-7 text-primary" />
              <span className="font-headline text-2xl font-bold text-foreground">Scamp</span>
            </Link>
            <p className="mt-4 text-base text-muted-foreground">
              AI-powered protection from deepfake scams.
            </p>
          </div>
          <div className="md:col-span-2">
            <h3 className="text-sm font-semibold text-foreground">Company</h3>
            <ul role="list" className="mt-4 space-y-2">
              {footerLinks.company.map((link) => (
                <li key={link.label}>
                  <Link href={link.href} className="text-base text-muted-foreground hover:text-foreground">
                    {link.label}
                  </Link>
                </li>
              ))}
            </ul>
          </div>
          <div className="md:col-span-2">
            <h3 className="text-sm font-semibold text-foreground">Legal</h3>
            <ul role="list" className="mt-4 space-y-2">
              {footerLinks.legal.map((link) => (
                <li key={link.label}>
                  <Link href={link.href} className="text-base text-muted-foreground hover:text-foreground">
                    {link.label}
                  </Link>
                </li>
              ))}
            </ul>
          </div>
          <div className="md:col-span-4">
             <h3 className="text-sm font-semibold text-foreground">Stay Protected</h3>
             <p className="mt-4 text-base text-muted-foreground">Get started for free and secure your digital life from AI-powered scams.</p>
             <Button asChild size="lg" className="mt-6 w-full sm:w-auto">
               <Link href={TELEGRAM_CTA_LINK}>Use Scamp on Telegram</Link>
             </Button>
          </div>
        </div>

        <div className="mt-12 border-t border-slate-800 pt-8">
          <p className="text-base text-muted-foreground text-center">
            &copy; {new Date().getFullYear()} Scamp. All rights reserved.
          </p>
        </div>
      </div>
    </footer>
  );
}
