# init-design-system

A [Claude Code](https://claude.com/claude-code) skill that builds a project's design system
as a visual HTML page **plus** a working shadcn/ui setup — OKLCH colors, typography,
spacing, radius, borders, layered shadows, logo, and components delivered as installed
React code.

It reuses tokens already in the repo instead of inventing new ones. The output is
code-ready, not a mood board.

## What it produces

Two deliverables, both required:

1. **`docs/design-system.html`** — a standalone page (no build step, no CDN) set in the
   brand's own fonts and colors, with nine sections: Logo, Colors, Typography, Spacing,
   Radius, Border, Shadow, Icons, Components.
2. **The project itself**, wired with shadcn/ui on those tokens, so the next agent builds
   with the system rather than around it.

Every value is drawn rather than described: spacing is a bar chart, radius shows real
curvature, shadow shows real elevation, type shows real specimens.

## Opinions it ships by default

| Rule | Means |
|---|---|
| OKLCH only | No hex or HSL outside a legacy `@supports` fallback |
| Two chosen hues | One primary (action), one accent (highlight) — picked first; neutrals derive from the primary, status follows convention |
| Shadows carry surfaces | Three-layer shadow-border; borders are for lines |
| 4-point spacing | 4 · 8 · 12 · 16 · 24 · 32 · 48 · 64, and only these |
| Constrained scales | ~1.2 modular type scale, five shadow tokens, five radius tokens |
| shadcn/ui is the base | Every component on the page exists as installed React code |
| HugeIcons is the registry | One icon set, sizes off the scale, icons are structural |
| Everything interactive transitions | Named properties, `--ease-out`, under 200ms |

Two rules never move, whatever you ask for: contrast that passes WCAG, and an accessible
name on every control. Everything else yields to an explicit instruction.

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
SKILL.md                     entry point — stance, defaults, the six steps
references/
  tokens.md                  the eight token groups and their shadcn mappings
  shadcn-setup.md            framework detection, init, token injection, icon swap
  components.md              core → composite → domain component tiers
  polish.md                  font smoothing, text wrapping, shadow-borders, focus rings
  html-spec.md               section markup and the visualization recipes
```

## Requirements

The skill assumes a React project it can wire shadcn/ui into. It reads `package.json` to
detect the framework, and harvests any existing `DESIGN.md`, `tokens.json`, `theme.ts`,
`globals.css`, `tailwind.config.*`, or `components.json` before filling gaps.
