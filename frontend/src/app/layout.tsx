import type { Metadata, Viewport } from 'next';
import { Fraunces } from 'next/font/google';
import { GeistSans } from 'geist/font/sans';

import { Providers } from '@/components/layout/providers';
import './globals.css';

/**
 * Fraunces carries the brand. Loaded as a variable font and self-hosted by
 * next/font so there is no third-party request in the critical path.
 *
 * No `weight` here on purpose. next/font rejects an explicit weight list
 * alongside `axes`: listing weights pins the font to static instances, and the
 * custom axes only exist on the variable file. Omitting weight keeps the full
 * `wght` range, which is what the type scale in globals.css assumes.
 */
const fraunces = Fraunces({
  subsets: ['latin'],
  variable: '--font-fraunces',
  display: 'swap',
  axes: ['SOFT', 'WONK', 'opsz'],
});

const SITE_URL = process.env.NEXT_PUBLIC_SITE_URL ?? 'http://localhost:3000';

export const metadata: Metadata = {
  metadataBase: new URL(SITE_URL),
  title: {
    default: 'Bliss by Uddy',
    template: '%s | Bliss by Uddy',
  },
  description:
    'Bags, sneakers, gowns, heels and denim. Picked in Lagos, delivered across Nigeria.',
  openGraph: {
    type: 'website',
    locale: 'en_NG',
    siteName: 'Bliss by Uddy',
  },
  robots: { index: true, follow: true },
  formatDetection: { telephone: false },
};

export const viewport: Viewport = {
  width: 'device-width',
  initialScale: 1,
  // Never disable zoom. Pinch-to-zoom is how a lot of people read a size chart.
  maximumScale: 5,
  themeColor: [
    { media: '(prefers-color-scheme: light)', color: '#fbf9f6' },
    { media: '(prefers-color-scheme: dark)', color: '#141110' },
  ],
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html
      lang="en-NG"
      suppressHydrationWarning
      className={`${GeistSans.variable} ${fraunces.variable}`}
    >
      <body className="min-h-dvh antialiased">
        <Providers>
          {/* First tab stop on every page. Keyboard users should not have to
              walk the whole nav to reach the content. */}
          <a
            href="#main"
            className="sr-only focus:not-sr-only focus:fixed focus:top-4 focus:left-4 focus:z-50 focus:rounded-md focus:bg-ink focus:px-4 focus:py-2 focus:text-ink-inverse"
          >
            Skip to content
          </a>
          <main id="main" className="min-h-[60dvh]">
            {children}
          </main>
        </Providers>
      </body>
    </html>
  );
}
