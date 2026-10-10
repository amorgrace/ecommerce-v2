import { ThemeToggle } from '@/components/ui/theme-toggle';

/**
 * Holding page. It exists to prove the token system, the two typefaces and the
 * theme switch all resolve. It gets replaced by the storefront home the moment
 * there is a catalogue endpoint to read.
 */
export default function Home() {
  return (
    <div className="rail py-20">
      <div className="flex items-start justify-between gap-6">
        <div className="max-w-prose">
          <p className="eyebrow">Storefront</p>
          <h1 className="mt-3 text-display">Bliss by Uddy</h1>
          <p className="mt-5 text-lg text-ink-muted">
            The design system is in place. The catalogue is not. Next step is the
            auth layer, then the first real surface.
          </p>
        </div>
        <ThemeToggle />
      </div>

      <div className="mt-16 grid gap-px overflow-hidden rounded-lg border border-line bg-line sm:grid-cols-3">
        {[
          { label: 'Paper', className: 'bg-paper', label_class: 'text-ink-muted' },
          { label: 'Sand', className: 'bg-sand', label_class: 'text-ink-muted' },
          { label: 'Accent', className: 'bg-accent', label_class: 'text-accent-ink' },
        ].map((swatch) => (
          <div key={swatch.label} className={`${swatch.className} px-5 py-10`}>
            <span className={`eyebrow ${swatch.label_class}`}>{swatch.label}</span>
          </div>
        ))}
      </div>
    </div>
  );
}
