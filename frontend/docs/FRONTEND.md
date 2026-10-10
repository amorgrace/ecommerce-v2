# Frontend guide

Next.js 16.4 App Router, React 19.3, TypeScript 5.9, Tailwind v4, Motion.

This document covers the storefront only. Backend contracts (money
representation, pagination shape, stock semantics, payment flow) are the API's
to define and are not assumed here. Where this guide needs one, it says so and
names it as an open question rather than inventing it.

---

## 1. Rendering

**Server Components are the default. A `'use client'` directive is a decision
that needs a reason.**

| Use | For |
|---|---|
| Server Component | Anything that reads data, renders content, or composes layout |
| Client Component | Interactivity that needs browser state: bag, save, size picker, search, forms |

The rule in practice: push `'use client'` **down** the tree, never up. A page
that is a Client Component because one button inside it needs `onClick` ships
the entire page to the browser.

```tsx
// Wrong: the whole card ships to the browser for one heart icon.
'use client';
export function ProductCard({ product }) { ... }

// Right: the card renders on the server, one island hydrates.
export function ProductCard({ product }) {
  return (
    <article>
      <Image ... />
      <SaveButton productId={product.id} />   {/* 'use client' lives here */}
    </article>
  );
}
```

### Cache Components

`cacheComponents` is on in `next.config.ts`. The static shell of a page is
pre-rendered and served from the edge immediately, and dynamic holes stream in
behind `<Suspense>`.

This is what makes a product page feel instant on a Nigerian mobile connection:
the layout, the header and the skeleton arrive in one round trip from a nearby
edge node, and the data fills in afterwards.

Consequence: **every `<Suspense>` needs a real skeleton**, at the exact final
dimensions. Placeholder text or a spinner defeats the point.

### View Transitions

Reserved for the grid to product-detail morph, where the card image becomes the
detail image. It is the one page-level animation in the app and it is worth it
because it preserves the shopper's sense of place.

Do not add view transitions to routine navigation. The header changing between
two pages is not an event.

---

## 2. Data and auth

The API is Django Ninja with **JWT bearer authentication**. The browser never
holds a token. See [`docs/decisions/0001-jwt-in-httponly-cookies-via-bff.md`](decisions/0001-jwt-in-httponly-cookies-via-bff.md).

### Shape

```
Browser  ──fetch, same origin, cookies only──▶  Next.js
Next.js  ──fetch + Authorization: Bearer ────▶  Django
```

- `lib/api/server.ts` is marked `server-only`. It reads the access token from
  the HttpOnly cookie and attaches the `Authorization` header. Importing it
  into a Client Component is a build error, not a runtime leak.
- `lib/api/browser.ts` calls **our own** Route Handlers, never Django directly.
  It sends no `Authorization` header because it has nothing to send.
- Route Handlers under `app/api/` are the only place a token is read or written.

### Reads

Server Components fetch directly from Django. No public round trip.

- Read helpers return a discriminated result and never throw.
- A variant that takes a fallback exists for anything that must not fail the
  render. A failed "trending" fetch renders an empty rail, not a 500.
- Every call has a timeout. A hung upstream must not hold a render.
- `revalidate` plus `tags`, so a change in the admin can purge exactly what
  changed rather than the whole site.

### Writes

Client Components mutate through Route Handlers, wrapped in TanStack Query
mutations.

- `credentials: 'same-origin'`. Our session cookie is the only credential the
  browser sends.
- Errors arrive with a stable `code`. **Branch on `code`, never on the message
  string.**

```tsx
try {
  await placeOrder();
} catch (error) {
  if (error instanceof ApiRequestError) {
    if (error.code === 'out_of_stock') return showSoldOut(error.meta);
    if (error.code === 'price_changed') return showPriceChange(error.meta);
  }
  toast.error('Could not place that order. Try again.');
}
```

> **Open with the backend:** a stable machine-readable error `code` on every
> 4xx. Django Ninja does not give one by default. Without it the frontend has
> to parse prose, which breaks the first time a message is reworded.

### Token refresh

The access token lives 30 minutes, the refresh token 7 days. Middleware decodes
the access token's `exp` with `jose` and refreshes **before** it lapses, rather
than reacting to a 401. Reacting to a 401 means one request per page load fails
first, and a failed mutation is not always safe to replay.

### Types

`openapi-typescript` generates TypeScript from Django Ninja's live OpenAPI
document at `/api/openapi.json`. Regenerate after any change to a Ninja schema.
The generated file is **gitignored on purpose**: a committed copy rots
silently, and a stale type that still compiles is worse than no type.

---

## 3. State

Four kinds, four homes. Putting one in the wrong home is the most common
frontend mistake in a commerce app.

| Kind | Home | Example |
|---|---|---|
| Server data | TanStack Query | Bag contents, order list, saved items |
| URL state | `nuqs` | Filters, sort, search query, pagination cursor |
| Ephemeral UI | `useState` | Is the drawer open, which tab is active |
| Cross-tree UI | React context | Bag drawer open state |

**Filters live in the URL.** Not in `useState`. A filtered grid must be
shareable, bookmarkable, and survive a back button. This is not a nicety: a
shopper who sends a link to a friend and gets an unfiltered page has been let
down by the app. `nuqs` is installed precisely so this is as easy as `useState`
and there is no excuse to reach for the wrong one.

**There is no global store of server data.** The bag lives in TanStack Query
keyed `['bag']`. Duplicating server state into a client store is how a bag
count and a bag page come to disagree. We deliberately did not install a state
library; if one ever seems necessary, that is a signal something is in the
wrong home.

### Optimistic updates

Used where the round trip would make the app feel slow and the failure is
cheap to reverse:

- Save to wishlist: heart fills instantly, reverts and toasts on failure.
- Bag quantity: number changes instantly, reverts on failure.

Not used where the failure is expensive or confusing:

- Placing an order. Never optimistic. The shopper waits and gets the truth.
- Applying a discount code. It either applies or it does not.

---

## 4. Styling

Tailwind v4, tokens only. Tailwind is wired through `@tailwindcss/turbopack`,
so there is no `postcss.config` and no PostCSS step.

```tsx
// Wrong. A hex, a magic duration, an invented radius.
<div className="bg-[#B3452E] rounded-[14px] transition-all duration-300" />

// Right. Tokens, and only the properties that actually change.
<div className="bg-accent rounded-md transition-colors duration-instant" />
```

- **Never `transition-all`.** It animates properties you did not intend,
  including layout properties, and it is a measurable performance cost.
- **`cn()` for conditional classes**, so later Tailwind utilities win properly.
- **`cva` for component variants.** A component with more than two visual
  variants gets a `cva` definition, not a chain of ternaries.
- **No CSS-in-JS runtime.** No `styled-components`, no `emotion`. They cost
  bundle size and break in Server Components.
- **No arbitrary values in components** except where a token genuinely does not
  fit, and then only with a comment saying why.

---

## 5. Images

Product photography is the product. It is also, by a wide margin, the largest
thing on any page.

- **Always `next/image`.** `@next/next/no-img-element` is an error.
- **Always `sizes`.** Without it the browser downloads the largest candidate.
  Get it right against the actual grid:
  ```tsx
  sizes="(min-width: 1280px) 22vw, (min-width: 768px) 30vw, 47vw"
  ```
- **`priority` on exactly one image per page.** The hero, or the first card
  above the fold. Marking many priority means none of them is.
- **`placeholder="blur"` with a stored blur data URL** so the grid never
  flashes an empty box.
- **`fill` with a fixed aspect-ratio parent**, never a bare `fill` in a
  container without dimensions.
- AVIF then WebP, a long cache TTL, both configured in `next.config.ts` once
  there is a real media host.

> **Open with the backend:** who generates the blur placeholder, and whether
> media is served from Django or a CDN. Both change `next.config.ts`.

---

## 6. Forms

`react-hook-form` with a `zod` resolver. The client schema is for **user
experience, not security**. The server validates independently and does not
trust anything the client checked.

- Validate on blur, not on every keystroke. Validating as someone types their
  first character tells them they are wrong before they have finished being
  right.
- Errors sit next to the field, are announced with `aria-describedby`, and the
  first invalid field receives focus on a failed submit.
- Submit buttons show loading and stay disabled while pending.
- Nigerian phone input accepts `0803...`, `+234803...` and `234803...`.
  Rejecting a format someone naturally types is a self-inflicted conversion
  loss. Agree with the backend which side normalises, and do it in one place.

---

## 7. Performance

1. **The React Compiler is on.** Do not add `useMemo` or `useCallback` for
   performance. Hand-rolled memoisation can defeat it.
2. **Dynamic import anything heavy and below the fold.** The size guide modal,
   the image zoom viewer.
3. **No barrel file re-exports from `components/`.** `export * from './x'`
   defeats tree shaking and pulls the whole directory into every bundle.
4. **Watch the bundle** before merging anything that adds a dependency. A new
   package that adds 40kB to the first load needs to justify itself.
5. **Never fetch in a `useEffect`** for initial data. That is a waterfall: the
   page renders, then hydrates, then fetches. Fetch on the server.
6. **`embla-carousel-react` is for the product detail gallery only.** Rails and
   horizontal scrollers are CSS scroll-snap and import nothing.

---

## 8. Accessibility

`eslint-plugin-jsx-a11y` at `strict`. Lint fails on a violation. Beyond the
lint rules:

- Keyboard-complete every flow before calling it done. Tab, Enter, Space, Esc.
- Focus trapped in dialogs, restored to the trigger on close. Radix handles
  this; do not hand-roll a dialog.
- Live regions for changes that happen away from focus: bag count, stock
  warnings, "added to bag".
- `aria-pressed` on toggles, `aria-busy` on loading controls, `aria-label` on
  icon-only buttons.
- Test with a screen reader on the checkout flow at minimum. Playwright plus
  `@axe-core/playwright` covers the mechanical checks, not the experience.

---

## 9. Security

- **No secret behind `NEXT_PUBLIC_`.** Anything so prefixed is inlined into the
  browser bundle in plain text.
- **`server-only`** on `lib/api/server.ts`. Importing it into a Client
  Component is a build error.
- **No token in `localStorage`, `sessionStorage` or a JS-reachable variable.**
  Cookies are HttpOnly. A single XSS should not be a permanent account
  takeover. This is not negotiable.
- **Never `dangerouslySetInnerHTML`** with anything from the API. If rich text
  is ever needed, sanitise on the server with an allow-list, not on the client.
- **CSP enforced by middleware** with a per-request nonce and `strict-dynamic`,
  so there is no `unsafe-inline` on scripts. Adding a third-party script means
  adding its exact origin and justifying it. Not yet built.

---

## 10. The checklist

- [ ] Server Component unless interactivity genuinely requires otherwise
- [ ] `'use client'` is as far down the tree as it can be
- [ ] Loading, empty and error states all exist
- [ ] Skeleton matches the final dimensions exactly
- [ ] Tokens only. No hex, no magic duration, no invented radius
- [ ] `sizes` on every image, `priority` on exactly one
- [ ] Filters are in the URL via `nuqs`, not in state
- [ ] Errors branch on `code`, never on a message string
- [ ] Keyboard complete, focus visible, screen reader sensible
- [ ] `prefers-reduced-motion` honoured
- [ ] No em dashes in any copy
- [ ] `pnpm lint && pnpm typecheck` clean
