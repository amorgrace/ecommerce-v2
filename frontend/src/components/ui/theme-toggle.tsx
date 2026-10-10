'use client';

import { Moon, Sun } from 'lucide-react';
import { useTheme } from 'next-themes';

/**
 * Theme toggle.
 *
 * The icon and the accessible name are swapped by CSS off the `data-theme`
 * attribute, not by React state. next-themes sets that attribute before first
 * paint, so there is no flash, no hydration mismatch, and no mount-gating
 * effect. `resolvedTheme` is read only inside the click handler, where a
 * server and client difference cannot matter.
 */
export function ThemeToggle() {
  const { resolvedTheme, setTheme } = useTheme();

  return (
    <button
      type="button"
      onClick={() => setTheme(resolvedTheme === 'dark' ? 'light' : 'dark')}
      className="inline-flex size-9 items-center justify-center rounded-pill border border-line text-ink-muted transition-[color,background-color,transform] duration-instant ease-out-quart hover:bg-sand hover:text-ink active:scale-[0.97]"
    >
      <Moon className="size-4 dark:hidden" aria-hidden />
      <Sun className="hidden size-4 dark:block" aria-hidden />
      <span className="sr-only dark:hidden">Switch to dark theme</span>
      <span className="sr-only hidden dark:inline">Switch to light theme</span>
    </button>
  );
}
