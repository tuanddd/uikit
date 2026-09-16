# Stacks

One table decides everything stack-specific: where the route lives, what a component is,
where the accessible behaviour comes from, which CSS variable names the components read,
how icons render, and how the viewer is hidden in production.

Read `package.json` first, then the file layout. The layout disambiguates the router.

---

## 1. Detect

| Signal in `package.json` / files | Stack | Path |
|---|---|---|
| `next` | React · Next.js | App Router if `app/` or `src/app/` exists, else Pages Router |
| `astro` | Astro | `src/pages/` |
| `@sveltejs/kit` | Svelte · SvelteKit | `src/routes/` |
| `svelte` + `vite` | Svelte · Vite | router optional |
| `@remix-run/*` or `react-router` | React · Remix / React Router | `app/routes/` |
| `vite` + `react` | React · Vite | router optional |
| `vue`, `nuxt`, `solid`, `qwik`, anything else | **Not in scope** | Tokens + fallback page only; say so in one line |
| No `package.json` | **No hostable route** | Tokens + fallback page only; say so in one line |

Already has `components.json` (React)? shadcn is initialized — keep the existing aliases and
skip the init step in `setup.md`.

---

## 2. The per-stack contract

`/uikit/design-system` is the route everywhere. This table is the source of every other
choice.

| | React | Svelte | Astro |
|---|---|---|---|
| **Component dir** | `src/components/ui/*.tsx` | `src/lib/components/ui/*.svelte` | `src/components/ui/*.astro` |
| **Component is a** | function component + props type | `.svelte` SFC with runes (`$props`, `$state`) | `.astro` page-less component with a frontmatter script |
| **Route file (App Router)** | `app/uikit/design-system/page.tsx`, or `src/app/uikit/design-system/page.tsx` when the project uses `src/` | `src/routes/uikit/design-system/+page.svelte` | `src/pages/uikit/design-system.astro` |
| **Route file (Pages/other)** | `pages/uikit/design-system.tsx` or `src/pages/uikit/design-system.tsx` (Pages) · `app/routes/uikit.design-system.tsx` (Remix/RR7) | Vite: see §3 no-router path | — |
| **Primitive layer** | shadcn/ui over Radix | Bits UI (`bits-ui`) | native elements + a progressive-enhancement `<script>` per interactive primitive |
| **Styling entry** | `app/globals.css` (Next) · `src/index.css` (Vite) · `app/tailwind.css` (Remix) | `src/app.css` (SvelteKit) · `src/app.css` (Vite) | `src/styles/global.css` |
| **Icons** | `@hugeicons/react` + `@hugeicons/core-free-icons` | `@hugeicons/svelte` + `@hugeicons/core-free-icons` | `@hugeicons/core-free-icons` raw node data + a thin `Icon.astro` |
| **Env signal** | `process.env.NODE_ENV`, `process.env.VERCEL_ENV` | `$app/environment` `dev` + `$env/dynamic/private` in server code; `import.meta.env` in universal code | `import.meta.env.PROD` / `DEV`; `.env` values land in `import.meta.env`, host `VERCEL_ENV`/`CONTEXT` |
| **Prod gate** | `notFound()` (App) · `getStaticProps {notFound:true}` (Pages) · `throw new Response(null,{status:404})` (loader) | `error(404, …)` in `+page.server.ts` (server-only, so `process.env` resolves) | return 404 before rendering (§4) |
| **Typecheck** | `npx tsc --noEmit` | `svelte-check` | `astro check` |
| **Build** | `npm run build` | `npm run build` | `astro build` |

Vue/Nuxt/Solid/Qwik and buildless projects are out of scope: emit `tokens.css` +
`tokens.json` + the fallback page (`html-spec.md`) and state that a route needs a supported
stack.

---

## 3. No-router SPA (Vite React, Vite Svelte)

`vite` ships no router. If the project has none (no `react-router`, `@tanstack/react-router`,
`@sveltejs/kit`, `svelte-routing`), do **not** add one just for the viewer — a router is a
dependency the user did not ask for.

Mount the viewer behind a pathname check at the app root, dev-only:

```tsx
// src/main.tsx — dev surface only, tree-shaken out of production
if (import.meta.env.DEV && location.pathname === "/uikit/design-system") {
  import("./dev/DesignSystemViewer").then(({ mount }) => mount(document.getElementById("root")!));
} else {
  // the app's normal bootstrap
}
```

The viewer entry lives at `src/dev/DesignSystemViewer.tsx` and mounts the same nine
sections directly. The dev-only `import.meta.env.DEV` guard is the gate; production never
loads the module. If the project has a router, add a normal route instead — the pathname
trick is the fallback, not the default.

---

## 4. Gating the route

The viewer is hidden outside local and preview. The env source differs by stack — Astro and
Vite put `.env` values in `import.meta.env`, never `process.env`; Next and Remix read
`process.env`; SvelteKit reads `$env/dynamic/*` on the server and `import.meta.env` in
universal code. Use the helper for the stack, beside the route:

```ts
// React — Next.js, Remix, React Router. src/dev/design-system-enabled.ts
export const designSystemEnabled = () =>
  process.env.SHOW_DESIGN_SYSTEM === "true" ||
  (process.env.VERCEL_ENV
    ? process.env.VERCEL_ENV !== "production"
    : process.env.NODE_ENV !== "production");
```

```ts
// Svelte — SvelteKit. src/lib/dev/design-system-enabled.ts, imported only by +page.server.ts.
// PUBLIC_-prefixed values reach SvelteKit through $env, not import.meta.env.
import { dev } from "$app/environment";
import { env } from "$env/dynamic/private";

export const designSystemEnabled = () =>
  dev ||
  env.PUBLIC_SHOW_DESIGN_SYSTEM === "true" ||
  (env.VERCEL_ENV ? env.VERCEL_ENV !== "production" : env.NODE_ENV !== "production");
```

```ts
// Astro. src/lib/design-system-enabled.ts
export const designSystemEnabled = () =>
  import.meta.env.DEV || import.meta.env.PUBLIC_SHOW_DESIGN_SYSTEM === "true";
```

```ts
// Vite React / Vite Svelte.
export const designSystemEnabled = () =>
  import.meta.env.DEV || import.meta.env.VITE_SHOW_DESIGN_SYSTEM === "true";
```

**Request-time (SSR, server, or edge).** Return 404 before rendering:

- Next App Router: `if (!designSystemEnabled()) notFound();`
- Next Pages Router: `getStaticProps` → `{ notFound: true }`
- Remix / React Router: `throw new Response(null, { status: 404 })` in the loader
- SvelteKit: `error(404, "Not found")` in `+page.server.ts` (server-only, so the gate is not
  evaluated on the client)
- Astro on-demand: `if (!designSystemEnabled()) return new Response(null, { status: 404 });`

**Build-time (static output).** A static site emits the page file whatever the route returns,
so request-time code cannot hide it. In order:

1. **Build the preview, not the production page.** For the preview environment, build with
   the override set (`PUBLIC_SHOW_DESIGN_SYSTEM=true` / `VITE_SHOW_DESIGN_SYSTEM=true`); for
   production, the content branch renders the `noindex` stub with no specimens.
2. **Host redirect**, if the host supports one: `public/_redirects` (Netlify, Cloudflare
   Pages) or `vercel.json` `redirects` mapping `/uikit/design-system` to `/404` for the
   production environment.
3. **Discovery hygiene** — `noindex`, `robots.txt`, sitemap exclusion, no inbound link (§5).

A static page cannot be both emitted and unreachable without a host rule. If the host offers
neither a redirect nor an environment-scoped build, record `[UNAVAILABLE: static host cannot
gate <host>]` in the report and state plainly that the page is reachable by URL in
production, protected only by `noindex`, `robots.txt`, and the sitemap exclusion. Do not
claim a production gate that does not exist.

---

## 5. Dev-surface hygiene — every stack, required

The env gate is not enough on its own. The viewer is a dev surface, and the repo says so:

- **`noindex`** — `<meta name="robots" content="noindex">` in the route's head.
- **`robots.txt`** — a `Disallow: /uikit/` line. Add the file if the project has none.
- **Sitemap** — exclude the route. Next: filter the sitemap generator. Astro:
  `@astrojs/sitemap` `filter`. SvelteKit: the prerender/`entries` list. Vite: the sitemap
  plugin's exclude. If the project has no sitemap, do nothing here.
- **No inbound link** — no nav, footer, menu, or page links to it. Reachable by URL only.
- **A comment at the top of the route file** — one sentence stating it is a dev surface and
  must stay unlinked. The next agent reads the file, not this reference.

---

## 6. What "authored natively" means per stack

The component inventory, anatomy, states, and craft rules are identical across stacks
(`components.md`, `hierarchy.md`, `polish.md`). Only the implementation differs:

- **React** — install shadcn primitives and patch them onto the tokens
  (`setup.md` § React). The component file is a function returning JSX.
- **Svelte** — install `bits-ui`, wrap each primitive in a `.svelte` component whose props
  mirror the shadcn API (`variant`, `size`, `disabled`, `icon`, …), styled with the same
  tokens. Use runes: `let { variant = "primary" }: Props = $props()`.
- **Astro** — author each component as `.astro`: a frontmatter `interface Props`, the
  markup, and a scoped `<style>` that reads the tokens. Interactive primitives (Dialog,
  DropdownMenu, Select, Tooltip) carry a small `<script>` that toggles `data-state` and
  manages focus; the component works without it for the non-interactive states. This is the
  proven `src/components/ui/*.astro` pattern — no framework island.

In every stack the component **consumes the same CSS variables** (`--background`,
`--primary`, `--shadow-border`, `--radius`, `--space-*`, `--dur-fast`). The variable names
are the contract; a stack-specific mapping is only notation.
