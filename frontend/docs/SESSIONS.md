# Sessions

Append a new entry at the top at the end of each working session. Say what
changed, what was decided and why, and what the next session should pick up.

---

## 10/10/2026: frontend foundation and handoff

**Who:** Claude Opus 5, with Eli

### Start here if you are a new session

1. Read [`AGENTS.md`](../AGENTS.md). It is the operating contract and it is short.
2. Read [`docs/decisions/0001-jwt-in-httponly-cookies-via-bff.md`](decisions/0001-jwt-in-httponly-cookies-via-bff.md).
   It is the one decision everything in the data layer depends on.
3. The next task is **the BFF auth layer**. It is specified under "Next" below.

---

### Context: what this repository is

A commerce platform for **Bliss by Uddy**, a Lagos fashion retailer selling
bags, sneakers, sunglasses, gowns, heels, polos, caps, joggers and jeans.
Real business, real customers, real money.

Unusual layout. The Django API lives at the **repository root**
(`engine/`, `authenticator/`, `manage.py`). The Next.js storefront lives in
**`frontend/`**. It is not a pnpm workspace; the storefront is a standalone app.

A **previous attempt at this project exists at `/home/praise/Desktop/WORK/bliss`**.
It is a different, more complete repository (Django 5.2, full domain model,
Monnify payments, seven ADRs). It is the source the design system and docs were
ported from and is worth reading for reference, but **it is not this project**
and its backend decisions do not apply here.

**Eli's stated reason for starting over:** on the previous project, decisions
were taken on the backend ahead of need and then became expensive to undo. The
explicit instruction for this repository is that **the frontend does not
pre-empt backend contracts**. Money representation, pagination shape, stock
semantics and the payment flow are the backend dev's to define. Where the
frontend needs one of these, raise it as an open question. Do not invent it.

### The backend, as it actually stands

Written by a separate backend developer. Only one app exists.

| | |
|---|---|
| Stack | Django 4.2.30, Django Ninja 1.6.2, ninja-extra, **ninja-jwt** |
| Database | Postgres via `dj-database-url`, SQLite fallback locally |
| Auth | JWT, HS256, 30 min access, 7 day refresh |
| User | `authenticator.User`, UUID primary key, `USERNAME_FIELD = "email"`, `username` still required |
| Endpoints | `POST /api/auth/register`, `GET /api/auth/me`, `POST /api/auth/change-password` |
| JWT endpoints | `/api/token/pair`, `/api/token/refresh`, `/api/token/verify` |
| OpenAPI | `/api/openapi.json` |
| Email | Sendlib, a third-party relay. Welcome template only |
| Deploy | Vercel, `@vercel/python`, WSGI |

**There is no catalogue, cart, order, payment, wishlist, password reset or
email verification.** Anything the storefront needs beyond sign-in does not
exist yet. That is an opportunity: the contract can be agreed before it is
built, which is the whole point of this repository.

### Done this session

- Scaffolded the Next.js storefront into `frontend/` with
  `create-next-app`. Next 16.4.0, React 19.3.0, TypeScript 5.9.3, Tailwind v4.
- Installed the full dependency set. The reasoning for each package was agreed
  with Eli before installing, not after.
- Turned the **React Compiler on** in `next.config.ts`. The scaffold defaults to
  off, which left `babel-plugin-react-compiler` installed and inert.
- Ported the design token system from `bliss` verbatim into
  [`src/app/globals.css`](../src/app/globals.css).
- Wired both typefaces in [`src/app/layout.tsx`](../src/app/layout.tsx):
  Fraunces with its `opsz`, `SOFT` and `WONK` axes, and Geist Sans. Both
  self-hosted through `next/font`.
- Wrote [`docs/DESIGN.md`](DESIGN.md) and [`docs/FRONTEND.md`](FRONTEND.md).
  `FRONTEND.md` was rewritten around the BFF rather than the old repo's session
  cookies, and three points where it needs a backend contract are marked as
  open questions rather than assumed.
- Wrote [`AGENTS.md`](../AGENTS.md) as the operating contract, including the
  scope rule above.
- Wrote one ADR, on auth transport. Deliberately only one.
- `eslint-plugin-jsx-a11y` at strict, Prettier with the Tailwind plugin,
  scripts for `typecheck`, `test`, `e2e`, `format` and `api:types`.
- `pnpm lint`, `pnpm typecheck` and `pnpm build` all pass.

### Decided

**1. The browser never holds the JWT.** Next acts as a backend-for-frontend:
Route Handlers call Django server to server and write the tokens into HttpOnly
cookies. Full reasoning and the rejected alternatives are in
[ADR 0001](decisions/0001-jwt-in-httponly-cookies-via-bff.md). This was chosen
over asking the backend to switch to session cookies, which would have been
cleaner but is real rework for a benefit the BFF already gives.

**2. Components are hand-built on Radix primitives.** No shadcn/ui. Radix gives
behaviour and accessibility; every style is ours against our own tokens. The
reason is stated plainly in `DESIGN.md`: shadcn's defaults are the most
recognisable machine-generated look there is, and stripping that out properly
costs more than it saves.

**3. The `bliss` design system carries over as-is.** Clay red accent, warm
neutrals, Fraunces plus Geist, two radii, three shadows, four durations. It
represents real thinking that did not need redoing.

**4. No state library.** `zustand` was considered and rejected. Server state
lives in TanStack Query, URL state in `nuqs`, ephemeral state in `useState`,
cross-tree UI state in React context. If a store ever seems necessary, that is
a signal something is in the wrong home.

**5. `embla-carousel-react` is installed but restricted** to the product detail
gallery. Rails and horizontal scrollers are CSS scroll-snap. The rule is
written into `FRONTEND.md` so it does not erode.

### Deliberately not done

Per Eli's instruction, **backend concerns were not ported** from `bliss`, even
though the files exist there and are good. Specifically left out:

- `money.ts` and the money-as-integer-kobo ADR. The money representation in
  this API has not been decided and the frontend must not presume one.
- The ADRs on stock reservation, payment verification, cursor pagination,
  email-and-password auth, and the monorepo shape.

If a future session wants any of these, they are at
`/home/praise/Desktop/WORK/bliss/docs/decisions/`. Agree them with the backend
developer first. Do not copy them in unilaterally.

Also not done:

- No `middleware.ts`, no CSP. `FRONTEND.md` section 9 describes the intent.
- No `lib/api/` at all yet. No generated types.
- No components beyond a theme toggle. `Button`, `Input`, `Field`,
  `ProductCard`, `SaveButton`, `ProductRail`, header and footer all exist in
  `bliss` at `apps/web/src/components/` and are worth porting when the surfaces
  that need them are built. Port them when needed, not speculatively.
- `src/app/page.tsx` is a holding page that exercises the tokens. It is meant to
  be replaced.
- Playwright browsers are **not installed**. `pnpm e2e` will fail until someone
  runs `pnpm exec playwright install chromium`. It is a ~190MB download and was
  skipped deliberately on a weak connection.

### Next

In order. The first one blocks everything else.

**1. Build the BFF auth layer.** This is the next task.

```
src/lib/api/server.ts      'server-only'. Reads the access cookie, attaches
                           Authorization, times out, returns a discriminated
                           result rather than throwing.
src/lib/api/browser.ts     Calls our own Route Handlers. Never Django. Sends
                           no token because it has none.
src/lib/api/errors.ts      ApiRequestError with a stable `code`.
src/app/api/auth/login/route.ts     POST -> Django /api/token/pair -> set cookies
src/app/api/auth/register/route.ts  POST -> Django /api/auth/register
src/app/api/auth/logout/route.ts    POST -> clear cookies
src/app/api/auth/refresh/route.ts   POST -> Django /api/token/refresh
src/middleware.ts          Decode `exp` with jose, refresh ahead of expiry.
                           Never react to a 401.
src/lib/env.ts             Split server and client schemas so a secret cannot
                           end up behind NEXT_PUBLIC_ by accident.
```

Cookie rules: `HttpOnly`, `Secure`, `SameSite=Lax`, and the **refresh cookie
path-scoped to the refresh route only** so it is not sent on every request.

**2. Generate the API types.** Start Django, then `pnpm api:types`. The output
at `src/lib/api/schema.d.ts` is gitignored on purpose; a committed copy rots
silently and a stale type that still compiles is worse than no type.

**3. Build the auth surfaces.** Sign-in and registration. Note the register
endpoint currently requires `email`, `username`, `password` **and**
`password_confirm`. The username requirement is worth questioning with the
backend dev: it is a field a fashion shopper has no reason to invent.

**4. Then, and only then, agree the catalogue contract** with the backend
developer before any product UI is built.

### Open: for the backend developer

Raised in priority order. The first two are correctness, the rest are contract.

1. **`DEBUG = True` is hardcoded** in `engine/settings.py`, not read from the
   environment. That ships stack traces and settings to production.
2. **`vercel.json` pins Python 3.9**, which is past end of life. Separately,
   `conn_max_age=600` on a serverless runtime will exhaust Postgres connections
   under load. Serverless plus a long-lived Django DB connection is a poor fit
   and may deserve a different host.
3. **`CORS_ALLOW_ALL_ORIGINS = True`** and `ALLOWED_HOSTS` contains `*`. Under
   the BFF design the browser never calls Django cross-origin, so CORS can be
   closed to the server's own origins once staging exists.
4. **No API versioning.** It is `/api/`, not `/api/v1/`. Cheap now, painful
   later.
5. **A stable machine-readable error `code` on every 4xx.** Django Ninja does
   not provide one. Without it the frontend has to branch on prose, which
   breaks the first time a message is reworded. This one matters a lot for
   checkout.
6. **Does `/api/token/refresh` rotate the refresh token, and is reuse
   detected?** Is there a server-side logout that invalidates a refresh token,
   or is clearing the cookie the whole of logout?
7. **Password reset and email verification endpoints do not exist.** The
   storefront needs both.
8. **Possible bug, worth verifying:** `UserResponseSchema.date_joined` is typed
   `str` but the model field is a `DateTimeField`. Confirm that serialises
   rather than raising.
9. **Media:** who generates image blur placeholders, and is media served from
   Django or a CDN? Both change `next.config.ts`.
10. **Phone normalisation:** the storefront accepts `0803...`, `+234803...` and
    `234803...`. Agree which side normalises, and do it in exactly one place.

### Environment notes

- Node v22.23.2, pnpm 10.33.0. pnpm offers an upgrade to 12.x; not taken.
- **The npm registry was switched** from `registry.npmmirror.com` (an Alibaba
  mirror, very slow from Nigeria) to `registry.npmjs.org`. The network is
  generally weak here. Expect installs to take minutes and plan commands so a
  failure is cheap to retry.
- TypeScript is pinned to `~5.9` and ESLint to `^9` **deliberately**. The
  plugin ecosystem caps below the next majors, and upgrading breaks `pnpm lint`
  and `pnpm api:types` together. The `eslint@9.39.5 is no longer supported`
  warning on every install is expected and is not a problem to fix.
- `eslint-config-next` already registers the jsx-a11y plugin, so
  `eslint.config.mjs` spreads the strict ruleset's **rules** rather than
  extending its config. Extending it directly throws
  `Cannot redefine plugin "jsx-a11y"`.
- The `bliss` Postgres and Redis containers were stopped this session. Nine
  `supabase_*_errands` containers belong to an unrelated project and were left
  running.
