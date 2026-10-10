'use client';

import { ThemeProvider } from 'next-themes';
import { Toaster } from 'sonner';
import type * as React from 'react';

/**
 * Client providers.
 *
 * Theme only for now. The TanStack Query client lands here when the data layer
 * is wired, and it must be created inside state so it is never shared between
 * requests on the server.
 */
export function Providers({ children }: { children: React.ReactNode }) {
  return (
    <ThemeProvider
      attribute="data-theme"
      defaultTheme="light"
      enableSystem
      disableTransitionOnChange
    >
      {children}
      <Toaster
        position="bottom-center"
        // Restrained. A toast is feedback, not a celebration.
        toastOptions={{
          className: 'rounded-md border border-line bg-raised text-ink shadow-md',
          duration: 3200,
        }}
      />
    </ThemeProvider>
  );
}
