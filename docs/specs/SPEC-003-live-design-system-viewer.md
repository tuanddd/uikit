# A live design-system viewer instead of a static HTML page

Lane: normal
Type: spec-feature

## Context

`/uikit:init-design-system` produces two deliverables: `docs/design-system.html`, a
standalone page that **redraws** every token and component in raw HTML/CSS/SVG, and the
project itself wired with shadcn/ui. The HTML page is fast to open, but it is a second,
frozen copy of the system. Nothing links it to the installed components, so the two drift
the moment either side changes. The wuandkin-site repo shows the cost: a hand-written
`scripts/sync-design-system.mjs` scrapes CSS out of the HTML into `src/styles/system.css`
with marker strings, and the HTML page's component drawings are re-typed versions of real
`.astro` components that already exist in the repo.

The user wants the viewer to show the **real components**, in the project's own stack,
through a route — without Storybook or a comparable dependency. The working pattern already
exists in wuandkin-site: `src/pages/dev/ui.astro` plus `src/components/dev/Specimen.astro`
render `src/components/ui/*.astro` unmodified, dev-only, `noindex`, excluded from the
sitemap and unlinked. The skill should generate that, adapted to the stack, instead of a
static page.

Grill: ran. Resolved branches — (1) non-React projects get **native components authored by
the skill**, not a gallery over whatever the project happens to have; (2) the route is
hidden outside local/preview via framework env detection plus dev-surface hygiene, not
build-time omission; (3) the static HTML survives as a **fallback only**, for a project that
cannot host a route; (4) the route is exactly `/uikit/design-system` with dev-surface
hygiene; (5) non-React accessible behaviour comes from a **headless primitive library per
stack**; (6) stacks in scope are **React, Astro, Svelte**.

Done = running `/uikit:init-design-system` on a React, Astro, or Svelte web project produces
(1) a live route `/uikit/design-system` that renders the nine design-system sections, with
the Components section rendering the project's own components imported unmodified, and (2)
that same component set authored natively in the project's stack, and (3) the route hidden
outside local/preview by env detection and dev-surface hygiene. For a project with no
framework that can host a route, it falls back to `docs/design-system.html` and says so.
No value or component is retyped in the viewer: token swatches read the CSS variables and
components are imported, so the viewer cannot drift from the system.

## Acceptance criteria

- The skill's primary deliverable is a route at `/uikit/design-system`, generated in the
  project's own routing idiom; `docs/design-system.html` is described as a fallback that is
  produced only when no route can be hosted.
- Framework detection covers React (Next App, Next Pages, Vite, Remix / React Router),
  Astro, and Svelte (SvelteKit, Vite), plus has a named path for "no hostable route".
- Each in-scope stack has a documented route file path, component directory and file type,
  primitive layer, styling entry, icon renderer, env signal, and hiding mechanism.
- Non-React components are authored by the skill with the stack's headless primitive
  library: React keeps shadcn/Radix, Svelte uses Bits UI, Astro uses native `.astro`
  components with progressive-enhancement scripts.
- The viewer never retypes a token value (swatches reference the live CSS variables) and
  never redraws a component (the Components section imports the real ones).
- The route is hidden in production: framework env detection (`NODE_ENV`,
  `import.meta.env.PROD`, `VERCEL_ENV`, Netlify `CONTEXT`) plus `noindex`, a robots
  disallow, a sitemap exclusion, and no inbound link.
- The nine sections survive: Logo, Colors, Typography, Spacing, Radius, Border, Shadow,
  Icons, Components. Section 9 groups the real components by tier under an anchored
  sub-nav.
- The static fallback path still works: when a project cannot host a route, the skill emits
  `docs/design-system.html` + `tokens.css` + `tokens.json` and states why it fell back.
- The skill README, the plugin README, `/uikit:what`, and `/uikit:implement` describe the
  route deliverable consistently, and the installed Codex copy matches the plugin copy
  except for its intentional naming.

## Design record

**Why a route, not a gallery library.** The gallery is a page the app already knows how to
build. Using the app's router means zero new dependencies, the project's own layout, fonts,
and bundling, and — the point — the components are imported, so the viewer and the app
share one definition. Storybook and equivalents were rejected for weight; the static HTML
was rejected because a second definition cannot be kept in sync by discipline alone.

**Why native component authoring was added.** The old skill only generated React code and
left non-React projects with the static page, which is exactly the drift source. To render
real components in Astro and Svelte, the skill has to install them there; so component
authoring becomes stack-aware. React keeps shadcn (skeleton + Radix). Svelte takes Bits UI
for Dialog / Select / Dropdown / Tooltip / Switch behaviour, the Svelte analogue of Radix.
Astro takes native `.astro` components with a small progressive-enhancement script per
interactive primitive, because no framework-agnostic headless library fits Astro without
adding a UI-framework island; this matches the hand-built `src/components/ui/*.astro`
already proven in wuandkin-site.

**Why the components section is anchored, not tabbed.** The former spec forced tabs so a
static page did not become one long scroll. In a live route the page shell already carries
a sticky nav, and one of the real components being demonstrated may itself be Tabs; using
the product's own Tabs to switch the gallery is recursive. An anchored sub-nav per tier
keeps the real components out of the switching mechanism.

**Why the static HTML is kept as a fallback.** A project with no bundler or router still
needs some view of its tokens. The fallback is narrow: the route exists whenever a route
can exist, and the skill says which path it took.

**Files.** `references/shadcn-setup.md` becomes `references/setup.md` (stack detection,
token injection, primitive install, per-stack component authoring, icons, verify). New
`references/stacks.md` (the per-stack table) and `references/viewer-spec.md` (the route,
the specimen helper, the nine sections, gating). `references/html-spec.md` stays,
re-labelled as the fallback spec. `tokens.md`, `components.md`, `hierarchy.md`, and
`polish.md` stay; their stack-specific wording is generalised so the CSS variables are the
contract and the React names are one mapping of them.

## Verification

Resolve every relative Markdown link across the plugin (SKILL.md, README.md, the four
sibling skills, and all references); no link may point at a renamed or deleted file. Run
`quick_validate.py` from the skill-creator scripts on the plugin skill and the Codex copy
in an isolated venv (the script needs PyYAML, absent from the system Python — record that).
Diff the plugin copy against the Codex copy and confirm the only differences are the
frontmatter `name` and the README install/use section. Have an independent reviewer read
the rewritten `SKILL.md`, `stacks.md`, `setup.md`, and `viewer-spec.md` against three
scenarios — a Next.js App Router project, an Astro project, and a SvelteKit project — and
confirm the route file, component type, primitive library, and env gate each resolve. Record
commands, outcomes, and limitations in
`docs/verification/live-design-system-viewer.md`.

## After state

`/uikit:init-design-system` produces a live `/uikit/design-system` route that renders the
real components in React, Astro, or Svelte, hidden outside local and preview, with the
static HTML page kept only for projects that cannot host a route. UIkit is at 0.5.0.
