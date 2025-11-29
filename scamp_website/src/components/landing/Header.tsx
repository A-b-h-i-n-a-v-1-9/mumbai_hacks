'use client';

import { useState } from 'react';
import Link from 'next/link';
import { Shield, Menu, X } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Sheet, SheetContent, SheetTrigger } from '@/components/ui/sheet';
import { cn } from '@/lib/utils';
import { NAV_LINKS, TELEGRAM_CTA_LINK } from './constants';

export default function Header() {
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  return (
    <header className="sticky top-0 z-50 w-full border-b border-border/40 bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="container flex h-14 max-w-screen-2xl items-center">
        <div className="mr-4 flex">
          <Link href="/" className="mr-6 flex items-center space-x-2">
            <Shield className="h-6 w-6 text-primary" />
            <span className="font-headline text-xl font-bold">Scamp</span>
          </Link>
          <nav className="hidden gap-6 md:flex">
            {NAV_LINKS.map((link) => (
              <Link
                key={link.label}
                href={link.href}
                className="text-sm font-medium text-muted-foreground transition-colors hover:text-primary"
              >
                {link.label}
              </Link>
            ))}
          </nav>
        </div>

        <div className="flex flex-1 items-center justify-end space-x-2">
          <Button asChild className="hidden md:inline-flex">
            <Link href={TELEGRAM_CTA_LINK}>Use Scamp on Telegram</Link>
          </Button>

          <Sheet open={isMobileMenuOpen} onOpenChange={setIsMobileMenuOpen}>
            <SheetTrigger asChild>
              <Button variant="ghost" className="md:hidden">
                <Menu className="h-5 w-5" />
                <span className="sr-only">Toggle Menu</span>
              </Button>
            </SheetTrigger>
            <SheetContent side="left" className="pr-0 bg-background">
              <Link href="/" className="mr-6 flex items-center space-x-2">
                 <Shield className="h-6 w-6 text-primary" />
                <span className="font-headline text-xl font-bold">Scamp</span>
              </Link>
              <div className="my-4 h-px w-full bg-border" />
              <div className="flex flex-col space-y-4">
                {NAV_LINKS.map((link) => (
                  <Link
                    key={link.label}
                    href={link.href}
                    onClick={() => setIsMobileMenuOpen(false)}
                    className="text-muted-foreground hover:text-primary"
                  >
                    {link.label}
                  </Link>
                ))}
              </div>
               <Button asChild className="mt-8 w-full">
                <Link href={TELEGRAM_CTA_LINK}>Use Scamp on Telegram</Link>
              </Button>
            </SheetContent>
          </Sheet>
        </div>
      </div>
    </header>
  );
}
