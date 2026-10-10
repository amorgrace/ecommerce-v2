# Design system

The brief: a shopper should want the thing within seconds of the page settling,
and should be able to buy it without thinking about the interface at all.

Everything below serves that. Nothing here is decoration for its own sake.

---

## The position

This is a Lagos fashion label, not a marketplace and not a SaaS product. The
interface should feel like a well-made lookbook that happens to take payments.
That means:

- **Editorial, not e-commerce-template.** Large photography, generous
  whitespace, quiet type, one confident accent.
- **Warm, not clinical.** The neutrals are warm. Pure `#FFFFFF` and pure
  `#000000` do not appear anywhere.
- **Confident, not loud.** No countdown timers, no "23 people are viewing this",
  no full-screen newsletter interrupt. Urgency comes from real scarcity
  ("2 left in your size"), because that one is true.

---

## Banned

These are the tells of a machine-generated interface. Any of them in a pull
request is a rejection.

| Banned | Why |
|---|---|
| Purple-to-pink or blue-to-violet gradients | The default output of every image generator and every AI app template |
| Glassmorphism on a blurred abstract background | Costs paint performance, adds nothing, dates instantly |
| Emoji as interface icons | Renders differently on every platform, unreadable to screen readers, reads as unserious |
| Everything centred at the same size | No hierarchy means no place for the eye to land |
| More than one accent colour | Two accents means neither is the primary action |
| Four radii, six greys, three shadow ramps | Reads as accidental, because it is |
| "Discover our amazing collection" | Says nothing. Write what is actually true |
| A hero carousel | The second slide is seen by almost nobody, and it moves what someone was about to click |
| A `<div>` with an `onClick` | Not focusable, not announced, not keyboard operable |
| Em dashes | House rule, without exception |

---

## Tokens

All defined in [`src/app/globals.css`](../src/app/globals.css). No component
hard-codes a value. If you need something not listed, add it there first and
justify it in review.

### Colour

| Token | Light | Dark | Use |
|---|---|---|---|
| `paper` | `#FBF9F6` | `#141110` | Page ground |
| `raised` | `#FFFFFF` | `#1D1917` | Cards, sheets, anything above the page |
| `sand` | `#F1EBE3` | `#262120` | Quiet fills, chips, hovers, skeletons |
| `line` | `#E4DDD4` | `#322C29` | Hairlines, 1px, never 2 |
| `line-strong` | `#CFC5B9` | `#453D39` | Input borders |
| `ink` | `#16110F` | `#F6F2ED` | Primary text |
| `ink-muted` | `#6B615C` | `#A99F97` | Secondary text, AA on paper |
| `ink-faint` | `#948A83` | `#7C726B` | Tertiary. Never for anything essential |
| `accent` | `#B3452E` | `#E0674C` | Primary action, active state, sale price |
| `accent-soft` | `#F7E9E5` | `#2C1D19` | Accent background at low emphasis |
| `success` | `#1F7A4D` | `#4DBD84` | Delivered, in stock, payment confirmed |
| `warn` | `#9A6B0D` | `#D9A441` | Low stock, expiring session |
| `danger` | `#9B2C1F` | `#E0705F` | Destructive action, payment failed |

**The accent is clay red.** It was chosen because it is warm, it sits well
against fashion photography, it reads as confident rather than corporate, and
it is nothing like the blue-violet every generated interface reaches for. It
appears on the primary button, the active nav state, and a discounted price.
Nowhere else.

The dark accent is lifted to `#E0674C` because `#B3452E` on `#141110` fails
contrast. Dark mode is a warm dark, not an inversion: pure black flattens
product photography on an OLED screen.

### Type

Two families, both self-hosted through `next/font` so there is no third-party
request in the critical path.

| Role | Family | Notes |
|---|---|---|
| Display | **Fraunces** variable | Headings, prices, the brand voice. `opsz`, `SOFT` and `WONK` axes available |
| Interface | **Geist Sans** variable | Anything that must be read quickly |
| Numerals | Geist with `tnum` | Prices, quantities, order numbers. Applied via `.tnum` |

Prices use tabular numerals so a grid of them aligns and so a count does not
jitter as it changes.

Scale is fluid via `clamp()` rather than breakpoint jumps, so nothing lands at
an awkward intermediate size on a 390px phone:

| Token | Size |
|---|---|
| `text-display` | `clamp(2.75rem, 7vw, 5.25rem)`, line-height 0.94 |
| `text-h1` | `clamp(2rem, 4.2vw, 3rem)` |
| `text-h2` | `clamp(1.5rem, 2.6vw, 2rem)` |
| `text-h3` | `clamp(1.125rem, 1.6vw, 1.375rem)` |
| `text-base` | `0.9375rem` / 1.6 |
| `text-sm` | `0.8125rem` / 1.55 |
| `text-micro` | `0.6875rem`, uppercase, `0.08em` tracking |

`text-wrap: balance` on headings, `text-wrap: pretty` on paragraphs. A heading
with one orphaned word looks careless.

### Shape

Two radii and a pill. A third always looks like an accident.

`--radius-sm` 6px, `--radius-md` 10px, `--radius-lg` 18px, `--radius-pill` 999px.

### Elevation

Three steps, warm-tinted, low contrast. Shadows suggest lift, they do not
announce it.

`--shadow-xs` resting controls, `--shadow-sm` cards on hover, `--shadow-md`
sheets and popovers, `--shadow-lifted` the bag drawer only.

### Motion

| Token | Value | Use |
|---|---|---|
| `--duration-instant` | 90ms | Colour and opacity on hover |
| `--duration-quick` | 160ms | Button press, small state change |
| `--duration-base` | 240ms | Panel open, image swap, badge pop |
| `--duration-slow` | 380ms | Page-level transition, hero reveal |
| `--ease-out-expo` | `cubic-bezier(0.16, 1, 0.3, 1)` | Things entering |
| `--ease-out-quart` | `cubic-bezier(0.25, 1, 0.5, 1)` | Things settling |
| `--ease-spring` | `cubic-bezier(0.34, 1.4, 0.64, 1)` | Confirmation, one overshoot |

**Rules:**

1. **Transform and opacity only.** Never animate `width`, `height`, `top`,
   `left`, or anything that triggers layout. Those animate on the main thread
   and drop frames on a mid-range Android.
2. **Never `ease-in`.** It starts slow, which makes the interface feel
   unresponsive. Entering and exiting both use an ease-out curve.
3. **Never animate from `scale(0)`.** Start at `scale(0.95)` or higher, paired
   with opacity. Nothing in the real world appears from nothing.
4. **Nothing over 400ms.** A shopper deciding in ten seconds cannot be made to
   wait for an animation before they can act.
5. **Frequency decides whether it animates at all.** Something a person
   triggers a hundred times a day does not animate. Something they see once a
   session can.
6. **Never animate a keyboard-initiated action.**
7. **`prefers-reduced-motion` is honoured globally** in `globals.css`. Do not
   re-implement it per component, and never bypass it.
8. **Motion earns its place.** The count badge pops because it confirms an add
   landed without interrupting the browse. The card image swaps on hover
   because it answers "what does the back look like" without a click. A fade on
   a section heading does neither and should not exist.

---

## Components

### Product card

The most-rendered component in the app, so it is a Server Component with
exactly one client island (the save button). Shipping the whole card to the
browser to make a heart toggle would cost every shopper a few hundred kilobytes
for a feature most never touch.

- 3:4 aspect ratio, `object-cover`, sand placeholder behind.
- Second image cross-fades on hover. This is the one flourish and it does real
  work on a fashion grid.
- At most **one** badge. "Sold out" beats "% off" beats "Low stock". Two
  competing badges means neither is read.
- Save button hidden until hover on pointer devices, always visible on touch
  where there is no hover to reveal it.
- The title link uses `after:absolute after:inset-0` so the whole card is one
  target, while the accessible name stays on the link.

### Button

- A loading button keeps its exact width, so a row never reflows mid-click.
- A loading button is disabled and sets `aria-busy`, with an `sr-only` label,
  because silence during a slow action reads as a dead app.
- Every variant has hover, active, focus-visible and disabled.
  `active:scale-[0.97]` gives the press physical feedback. A control that does
  not respond to a press reads as broken.
- Minimum 44px touch target on the sizes used on mobile.

### Popovers and menus

Scale in from their trigger, not from their own centre. Set
`transform-origin` from the trigger position. A menu that grows from the middle
of itself has no spatial relationship to what opened it. Modals are the
exception: they are centred by nature and scale from centre.

### States, all four, always

Every data-driven surface ships with all of these. They are the feature, not a
follow-up.

| State | Requirement |
|---|---|
| Loading | A skeleton at the exact final dimensions. A skeleton of the wrong height teaches the eye a layout and then breaks it. |
| Empty | Says why it is empty and offers the next action. Never a bare "No results". |
| Error | Plain words, one action that might work, a human as fallback. Never a stack trace or a code a shopper cannot act on. |
| Success | Confirmed in place where possible. A toast for things that happen away from where the eye is. |

---

## Accessibility

Not a phase. It is a build failure: `eslint-plugin-jsx-a11y` runs at `strict`
and the lint script fails on a violation.

- **Contrast.** Body text meets WCAG AA (4.5:1). Large text meets 3:1.
  `ink-faint` is never used for anything a shopper needs.
- **Focus.** One treatment, global, in `globals.css`. A 2px accent outline at
  2px offset. It is never removed. Removing it makes the app unusable by
  keyboard.
- **Keyboard.** Every flow completable without a mouse. Tab, Enter, Space, Esc,
  and arrow keys inside a listbox or a size picker. Focus is trapped inside a
  dialog and restored to the trigger on close. Radix handles this; do not
  hand-roll a dialog.
- **Semantics.** A button is a `<button>`. A link that navigates is an `<a>`.
  An icon-only control has an `aria-label`. Every image has real alt text, and
  a decorative duplicate has `alt=""` with `aria-hidden`.
- **Announcements.** Live regions for anything that changes without focus
  moving: bag count, "added to bag", stock warnings.
- **Zoom.** `maximumScale: 5`. Never `user-scalable=no`. Pinch-to-zoom is how
  many people read a size chart.
- **Motion.** `prefers-reduced-motion` is honoured, globally, always.

---

## Performance

The conversion target is a decision in seconds, which is a performance
requirement before it is a design one.

| Metric | Target | How |
|---|---|---|
| LCP | under 2.0s on 4G | One `priority` image per page, static shell, no render-blocking font |
| INP | under 200ms | Server Components by default, React Compiler, no heavy client state |
| CLS | under 0.05 | Fixed aspect ratios, reserved scrollbar gutter, no layout-shifting ads |
| JS on first load | under 120kB gzipped | Client islands only, no component library shipped wholesale |

- **`priority` on exactly one image per page**, the hero or the first card.
  Marking a grid of them priority means none of them is.
- **`sizes` on every `next/image`.** Without it the browser downloads the
  largest candidate, which on a product grid is enormous.
- **Fonts are variable, subset to `latin`, `display: swap`.** No FOIT.
- **The React Compiler is on.** Do not add `useMemo` or `useCallback` for
  performance; the compiler handles it and hand-rolled memoisation can defeat
  it.

---

## Copy

The interface talks like the person who runs the shop, not like a brand deck.

| Instead of | Write |
|---|---|
| "New arrivals" | "Landed this week" |
| "Add to cart" | "Add to bag" |
| "Discover our collection" | "Shop new in" |
| "An error occurred" | "That did not load" |
| "Please refer to care instructions" | "Cold hand wash. Do not tumble dry." |
| "Out of stock" | "Sold out" |
| "Proceed to checkout" | "Checkout" |
| "Your cart is empty" | "Nothing in your bag yet" |

Specific beats enthusiastic. "2 left in your size" is worth more than "Selling
fast" because it is true and checkable.

British English throughout. No em dashes, anywhere.
