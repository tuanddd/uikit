# init-design-system

A [Claude Code](https://claude.com/claude-code) skill that builds a project's design system
as a **live route** at `/uikit/design-system` plus a working component setup in the
project's own stack — OKLCH colors, typography, spacing, radius, borders, layered shadows,
logo, and components authored natively (React / shadcn, Astro, or Svelte / Bits UI).

It reuses tokens already in the repo instead of inventing new ones. The output is
code-ready, not a mood board.

## What it produces

Three deliverables. The first two are always required.

1. **A live route** — `/uikit/design-system`, built in the project's own stack, with nine
   sections: Logo, Colors, Typography, Spacing, Radius, Border, Shadow, Icons, Components.
   Its Components section imports the project's real components; its token values print from
   `tokens.json`, the one source the CSS is derived from. The viewer cannot drift: nothing on
   it is a second copy.
2. **The project itself**, wired with the tokens and native components, so the next agent
   builds with the system rather than around it.
3. **`docs/design-system.html`** — fallback only, for a project with no framework that can
   host a route.

Every value is drawn rather than described: spacing is a bar chart, radius shows real
curvature, shadow shows real elevation, type shows real specimens — and the components are
the shipped ones, imported unmodified.

The route is a dev surface: hidden in production by env detection, unlinked, `noindex`,
disallowed in `robots.txt`, and excluded from the sitemap.

## Opinions it ships by default

| Rule | Means |
|---|---|
| OKLCH only | No hex or HSL outside a legacy `@supports` fallback |
| Two chosen hues | One primary (action), one accent (highlight) — picked first; neutrals derive from the primary, status follows convention |
| Shadows carry surfaces | Three-layer shadow-border; borders are for lines |
| 4-point spacing | 4 · 8 · 12 · 16 · 24 · 32 · 48 · 64, and only these |
| Constrained scales | ~1.2 modular type scale, five shadow tokens, five radius tokens |
| The stack's components are the base | Every specimen is a real component, imported: shadcn/Radix, Bits UI, or native Astro |
| The viewer cannot drift | Components are imported; token values print from `tokens.json`, fills read the CSS derived from it |
| HugeIcons is the registry | One icon set, sizes off the scale, icons are structural |
| Everything interactive transitions | Named properties, `--ease-out`, under 200ms |

Two rules never move, whatever you ask for: contrast that passes WCAG, and an accessible
name on every control. Everything else yields to an explicit instruction.

## Stacks

Native components and a live route are authored for **React** (Next App / Pages, Vite,
Remix, React Router), **Astro**, and **Svelte** (SvelteKit, Vite). An inaccessible stack, or
a project with no framework or bundler, falls back to the static page.

## Install

Part of the `uikit` plugin. Clone the plugin into your skills directory:

```bash
git clone https://github.com/tuanddd/uikit.git ~/.claude/skills/uikit
```

Start a new session (or run `/reload-plugins`) and the skill is available as `/uikit:init-design-system`.

## Use

Ask for it in plain language — the skill triggers on phrases like:

- "build a design system for this project"
- "set up design tokens"
- "make a style guide"
- "brand guidelines"

Or invoke it directly:

```
/uikit:init-design-system
```

## Layout

```
SKILL.md                     entry point — stance, defaults, the eight steps
references/
  tokens.md                  the eight token groups and their CSS variable map
  stacks.md                  stack detection; per-stack route, component, primitive, icon, env
  setup.md                   wiring per stack: token injection, primitives, fonts, icons, verify
  viewer-spec.md             the live route: page shell, specimen helper, nine sections, gating
  components.md              core → composite → domain component tiers
  polish.md                  font smoothing, text wrapping, shadow-borders, focus rings
  hierarchy.md               the three levers, label demotion, button ranks
  html-spec.md               fallback page, when a route cannot exist
```

## Requirements

The skill reads `package.json` and the file layout to detect the stack, and harvests any
existing `DESIGN.md`, `tokens.json`, `theme.ts`, `globals.css`, `app.css`,
`tailwind.config.*`, or `components.json` before filling gaps. React projects are wired with
shadcn/ui; Svelte projects with Bits UI; Astro projects get native components.
