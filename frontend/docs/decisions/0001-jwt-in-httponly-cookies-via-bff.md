# 0001. The browser never holds the JWT

**Status:** Accepted
**Date:** 10/10/2026
**Scope:** Storefront only. This decision changes no backend code.

## Context

The API authenticates with JWT. `django-ninja-jwt` is installed and
`NinjaJWTDefaultController` is registered, exposing `/api/token/pair`,
`/api/token/refresh` and `/api/token/verify`. Access tokens live 30 minutes,
refresh tokens 7 days, both signed HS256 with the Django secret key.

The conventional client for that is a bearer token kept in `localStorage`.
That is the thing we are refusing.

A previous iteration of this project chose Django session cookies instead,
precisely to avoid a JS-reachable credential. That decision is recorded here
rather than discarded, because its reasoning still holds even though its
mechanism no longer applies:

> A single XSS anywhere on the storefront hands an attacker a bearer
> credential that cannot be revoked before it expires.

The backend has since been built on JWT. Rather than ask for a rewrite, the
storefront absorbs the difference.

## Decision

**The browser never receives, stores or sends a JWT.** Next.js acts as a
backend-for-frontend.

1. Sign-in posts to a Next Route Handler, same origin.
2. That handler calls Django's `/api/token/pair` server to server.
3. It writes `access` and `refresh` into cookies that are `HttpOnly`, `Secure`,
   `SameSite=Lax`, path-scoped, with the refresh cookie scoped to the refresh
   route only.
4. Server Components read the access cookie and call Django with an
   `Authorization: Bearer` header.
5. Client Components call our own Route Handlers, never Django. They send no
   token because they have none.
6. Middleware decodes `exp` with `jose` and refreshes ahead of expiry rather
   than reacting to a 401.

## Alternatives considered

**JWT in `localStorage`.** The default pattern and the reason this ADR exists.
Rejected: one XSS is a permanent, unrevokable account takeover.

**Access token in memory, refresh in an HttpOnly cookie.** Less code than a
BFF. Rejected on two counts: every page load costs a refresh round trip before
anything authenticated can render, and the access token is still reachable by
injected script for as long as the tab lives.

**Ask the backend to move to Django session cookies.** The cleanest auth model,
and what the earlier project chose. Rejected for now because it is real backend
rework for a benefit the BFF already delivers, and it forces the API onto a
subdomain of the storefront's registrable domain, which constrains deployment.
Worth revisiting only if refresh rotation becomes painful.

## Consequences

- **Every authenticated browser call goes through a Route Handler.** That is
  more files than calling Django directly. It is also the only place a token is
  ever touched, which makes the surface auditable.
- **`lib/api/server.ts` carries `server-only`.** Importing it from a Client
  Component is a build error, not a runtime leak.
- A hop is added to client-initiated writes. Reads from Server Components are
  unaffected and still go straight to Django.
- **Revocation is weak and we should be honest about it.** A stateless JWT
  cannot be withdrawn before it expires. The 30 minute access lifetime is the
  only bound. If the ability to sign a customer out immediately turns out to
  matter, that needs a backend denylist and is not something the frontend can
  solve.
- Refresh rotation and reuse detection are the backend's to implement. The
  storefront assumes a refresh may be used once.

## Open with the backend

1. Does `/api/token/refresh` rotate the refresh token, and is reuse detected?
2. Is there a logout endpoint that invalidates a refresh token server-side, or
   is clearing the cookie the whole of logout?
3. `CORS_ALLOW_ALL_ORIGINS` is currently `True`. Under this design the browser
   never calls Django cross-origin, so it can be closed to the server's own
   origins once staging exists.
