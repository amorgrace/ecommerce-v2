<!-- BEGIN:nextjs-agent-rules -->

## This is NOT the Next.js you know

This version has breaking changes — APIs, conventions, and file structure may all differ from your training data. Read the relevant guide in `node_modules/next/dist/docs/` (resolved from this file's directory; in monorepos the `next` package may not be visible from the repo root) before writing any code. Heed deprecation notices.

This block is written and re-added by `next dev` — verify at `node_modules/next/dist/server/lib/generate-agent-files.js`. Removing it from a diff only re-creates the uncommitted change; committing it with your work keeps the tree clean.

<!-- END:nextjs-agent-rules -->

---

# Storefront operating contract

Read this before touching a file. If something here conflicts with what you
were about to do, this wins.

## What this is

The Next.js storefront for **Bliss by Uddy**, a Lagos fashion retailer. It sits
in `frontend/` alongside a Django Ninja API at the repository root.

The business already exists and already has customers. This is not a demo.
A bug in checkout costs the owner a sale she cannot get back.

| Layer | Choice |
|---|---|
| Framework | Next.js 16.4 App Router, React 19.3, TypeScript 5.9 |
| Styling | Tailwind v4 via `@tailwindcss/turbopack`, tokens only |
| Components | Radix primitives, styled by hand. No component library |
| Motion | Motion (Framer), plus `sonner` and `vaul` |
| Server state | TanStack Query |
| URL state | nuqs |
| Forms | react-hook-form with zod |
| API client | openapi-fetch, types generated from the live OpenAPI document |
| Auth | JWT held by Next in HttpOnly cookies. See ADR 0001 |

## Scope

**This directory owns the storefront and nothing else.** Money representation,
pagination shape, stock semantics and the payment flow are the API's decisions.
Do not encode an assumption about them here. Where the frontend needs one,
raise it as an open question with the backend rather than inventing a contract
and discovering later that it disagrees.

## Never

1. **Never put a token where JavaScript can read it.** Not `localStorage`, not
   `sessionStorage`, not a module-level variable. Cookies are HttpOnly and
   Next is the only thing that touches them. See
   [`docs/decisions/0001-jwt-in-httponly-cookies-via-bff.md`](docs/decisions/0001-jwt-in-httponly-cookies-via-bff.md).
2. **Never hard-code a visual value.** No hex, no magic duration, no invented
   radius. Every value is a token in [`src/app/globals.css`](src/app/globals.css).
3. **Never use `transition-all`.** Name the properties that change.
4. **Never use `ease-in`** for UI, and never animate from `scale(0)`.
5. **Never ship a surface without its loading, empty and error states.** They
   are the feature, not a follow-up ticket.
6. **Never put a secret behind `NEXT_PUBLIC_`.** It is inlined into the browser
   bundle in plain text.
7. **Never use an em dash.** Anywhere. Not in code comments, not in UI copy,
   not in commit messages, not in these docs.
8. **Never let a generic AI-looking interface ship.** The banned list in
   [`docs/DESIGN.md`](docs/DESIGN.md) is a rejection list, not a suggestion.

## Always

1. **Always use British English** in copy, comments and documentation. Nigerian
   commerce copy uses NGN, `DD/MM/YYYY` and metric.
2. **Always default to a Server Component.** `'use client'` is a decision that
   needs a reason, and it belongs as far down the tree as it will go.
3. **Always put filters in the URL** via nuqs, never in `useState`.
4. **Always branch on an error `code`**, never on a message string.
5. **Always give every interactive element hover, active, focus-visible and
   disabled states.** A control that does not respond to a press reads as
   broken.
6. **Always run `pnpm lint && pnpm typecheck` before pushing.**
7. **Always update [`docs/SESSIONS.md`](docs/SESSIONS.md)** at the end of a
   working session with what changed, what was decided and what is still open.
   It is how the next session picks up without re-deriving everything.

## Before you build

For anything larger than a one-line fix, do not open an editor first:

1. State the requirement in one sentence.
2. List the edge cases, including the unpleasant ones.
3. Name the API contract it needs, and whether that contract exists yet.
4. Say what the loading, empty and error states are.

## Commands

```bash
pnpm dev          # storefront on :3000
pnpm lint         # eslint, jsx-a11y at strict
pnpm typecheck    # tsc --noEmit
pnpm test         # vitest
pnpm e2e          # playwright (needs `pnpm exec playwright install chromium` once)
pnpm format       # prettier
pnpm api:types    # regenerate types from the running API's OpenAPI document
```

## Where to look

| Question | File |
|---|---|
| What it looks like and why | [`docs/DESIGN.md`](docs/DESIGN.md) |
| Rendering, data, state, performance | [`docs/FRONTEND.md`](docs/FRONTEND.md) |
| Why the browser never holds a token | [`docs/decisions/0001-jwt-in-httponly-cookies-via-bff.md`](docs/decisions/0001-jwt-in-httponly-cookies-via-bff.md) |
| Every design token | [`src/app/globals.css`](src/app/globals.css) |
| What happened last session, and what is next | [`docs/SESSIONS.md`](docs/SESSIONS.md) |
| What needs an answer from the backend developer | [`docs/SESSIONS.md`](docs/SESSIONS.md), "Open" |
