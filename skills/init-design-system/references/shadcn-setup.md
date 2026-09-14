# Wiring the project

The HTML page documents what is installed. So install first.

---

## 1. Detect the framework

Read `package.json`.

| Found | Path |
|---|---|
| `next` | shadcn native. Go to step 2. |
| `vite` + `react` | shadcn native. Go to step 2. |
| `astro` | `npx astro add react` first, then step 2. |
| `@remix-run` / `react-router` | shadcn native. Go to step 2. |
| React absent, no framework | Ask before adding React. Meanwhile ship the HTML page + `tokens.css` + `tokens.json` only. |
| No `package.json` | Ship the HTML page + `tokens.css` + `tokens.json` only. Say so in one line. |

Already has `components.json`? shadcn is initialized. Skip step 2, keep the existing
aliases, go to step 3.

## 2. Init

```bash
npx shadcn@latest init
```

Answers: **CSS variables → yes**. Base color → the closest neutral to the brand; it gets
overwritten in step 3 anyway.

Astro adds `src/styles/global.css`; Next adds `app/globals.css`; Vite adds
`src/index.css`. That file is the target for step 3.

## 3. Inject the tokens

Replace the generated `:root` block. Keep shadcn's variable **names** exactly — every
installed component reads them. Keep every color in OKLCH.

```css
@import "tailwindcss";
@import "tw-animate-css";

@custom-variant dark (&:is(.dark *));

:root {
  /* brand primitives — raw values, never consumed by components.
     Two of these were chosen; the rest follow. --brand-teal-700 is the primary
     and --brand-bronze is the accent, and the stone ramp takes the primary's
     warmth at a chroma near zero. */
  --brand-stone-50:  oklch(0.985 0.004 95);
  --brand-stone-100: oklch(0.962 0.006 95);
  --brand-stone-200: oklch(0.918 0.008 92);
  --brand-stone-700: oklch(0.512 0.006 85);
  --brand-ink:       oklch(0.242 0.004 60);
  --brand-teal-700:  oklch(0.420 0.062 165);
  --brand-bronze:    oklch(0.520 0.058 72);

  /* semantic — what components consume */
  --background: var(--brand-stone-50);
  --foreground: var(--brand-ink);
  --card: var(--brand-stone-50);
  --card-foreground: var(--brand-ink);
  --popover: var(--brand-stone-50);
  --popover-foreground: var(--brand-ink);
  --primary: var(--brand-teal-700);
  --primary-foreground: var(--brand-stone-50);
  --secondary: var(--brand-stone-100);
  --secondary-foreground: var(--brand-ink);
  --muted: var(--brand-stone-100);
  --muted-foreground: var(--brand-stone-700);
  --accent: var(--brand-bronze);
  --accent-foreground: var(--brand-stone-50);
  --destructive: oklch(0.520 0.180 27);
  --border: var(--brand-stone-200);
  --input: var(--brand-stone-200);
  --ring: var(--brand-teal-700);

  --radius: 0.75rem;

  --font-display: "Fraunces", Georgia, serif;
  --font-body: "Inter", system-ui, sans-serif;

  /* shadows carry the edge and the elevation */
  --shadow-border:
    0 0 0 1px oklch(0 0 0 / 0.06),
    0 1px 2px -1px oklch(0 0 0 / 0.06),
    0 2px 4px 0 oklch(0 0 0 / 0.04);
  --shadow-border-hover:
    0 0 0 1px oklch(0 0 0 / 0.08),
    0 1px 2px -1px oklch(0 0 0 / 0.08),
    0 2px 4px 0 oklch(0 0 0 / 0.06);
  --shadow-md:
    0 0 0 1px oklch(0 0 0 / 0.06),
    0 4px 8px -2px oklch(0 0 0 / 0.08),
    0 8px 16px -4px oklch(0 0 0 / 0.06);
  --shadow-lg:
    0 0 0 1px oklch(0 0 0 / 0.06),
    0 12px 24px -6px oklch(0 0 0 / 0.10),
    0 24px 48px -12px oklch(0 0 0 / 0.08);

  --outline-image: 1px solid oklch(0 0 0 / 0.10);

  /* density — compact by default, one preset per product */
  --pad-control: 8px 12px;
  --pad-card: 16px;
  --gap-field: 12px;
  --gap-block: 32px;
  --gap-section: 48px;

  /* icons — HugeIcons, stroke rounded */
  --icon-xs: 14px;
  --icon-sm: 16px;
  --icon-md: 20px;
  --icon-lg: 24px;
  --icon-xl: 32px;
  --icon-stroke: 1.5;
  --icon-stroke-bold: 2;

  /* motion — quick, quiet, interruptible */
  --ease-out: cubic-bezier(0.2, 0, 0, 1);
  --ease-entrance: cubic-bezier(0.25, 0.46, 0.45, 0.94);
  --dur-press: 80ms;
  --dur-fast: 120ms;
  --dur-icon: 150ms;
  --dur-panel: 160ms;
  --dur-dialog: 240ms;
  --dur-enter: 800ms;
}
```

Comfortable swaps that one block to `12px 16px` · `24px` · `16px` · `48px` · `64px`.
Nothing else in the file moves.

Then expose the brand-specific ones to Tailwind (v4):

```css
@theme inline {
  --font-display: var(--font-display);
  --font-body: var(--font-body);
  --radius-sm: calc(var(--radius) - 4px);
  --radius-md: calc(var(--radius) - 2px);
  --radius-lg: var(--radius);
  --radius-xl: calc(var(--radius) + 4px);
  --shadow-border: var(--shadow-border);
  --shadow-border-hover: var(--shadow-border-hover);
  --ease-out: var(--ease-out);
  --duration-fast: var(--dur-fast);
  --duration-icon: var(--dur-icon);
  --duration-panel: var(--dur-panel);
  --duration-dialog: var(--dur-dialog);
}
```

And the polish base layer (`polish.md` covers the rest):

```css
@layer base {
  html {
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
  }

  /* no block under ~4 lines is left holding one word on its last line */
  h1, h2, h3, h4, h5, h6,
  blockquote, figcaption, caption, label,
  [data-slot="card-title"], [data-slot="dialog-title"],
  [data-slot="alert-title"], [data-slot="tooltip-content"] { text-wrap: balance; }

  p, li,
  [data-slot="card-description"], [data-slot="dialog-description"],
  [data-slot="alert-description"], [data-slot="form-description"] { text-wrap: pretty; }

  img, video { outline: var(--outline-image); outline-offset: -1px; }

  /* every control answers the pointer */
  button, [role="button"], a, input, select, textarea,
  [data-slot="switch"], [data-slot="checkbox"], [data-slot="radio-group-item"] {
    transition-property: background-color, border-color, color, box-shadow, opacity, transform;
    transition-duration: var(--dur-fast);
    transition-timing-function: var(--ease-out);
  }
  button:active, [role="button"]:active {
    transform: scale(0.985);
    transition-duration: var(--dur-press);
  }

  @media (prefers-reduced-motion: reduce) {
    *, *::before, *::after {
      transition-property: color, background-color, border-color, box-shadow, opacity;
      animation-duration: 1ms !important;
      animation-iteration-count: 1 !important;
    }
  }
}
```

Tailwind v3 instead? The same names go in `tailwind.config.js` under `theme.extend`.

**Dark theme:** only if the brand ships one. In dark, the shadow stack collapses to a
single light edge — `0 0 0 1px oklch(1 0 0 / 0.08)`, hover `0.12`. If the brand is
light-only, delete the `.dark` block the CLI generated.

## 4. Verify the gamut

OKLCH accepts values no display can show; the browser silently clips them. Render each
token and confirm it matches what was authored. If a swatch looks flat or shifted, lower
its chroma until it does not.

## 5. Install the components

One command. List comes from `components.md`.

```bash
npx shadcn@latest add button input label textarea select checkbox radio-group switch \
  badge alert card separator avatar tabs dialog dropdown-menu popover tooltip sheet \
  table pagination form sonner skeleton spinner accordion
```

`spinner` is a newer registry entry. If the CLI does not resolve it, build one from the
`icon-loading` role instead — the semantic glyph, `animate-spin`, sized off the icon scale
— and keep it in `src/components/ui/spinner.tsx` so the rest of the system imports it the
same way.

Trim the list to what the product actually renders. An installed component nobody uses is
dead code, and the page has to show every one of them.

Then patch the installed primitives to the system:

| Primitive | Patch |
|---|---|
| Card, input, table, popover surfaces | `border` → `shadow-[var(--shadow-border)]`, `hover:shadow-[var(--shadow-border-hover)]` |
| Every interactive primitive | `transition-[background-color,color,box-shadow,transform] duration-[--dur-fast] ease-[--ease-out]` |
| Button, menu item, pagination link | add `active:scale-[0.985]` |
| Select, accordion, dropdown chevron | `transition-transform duration-[--dur-icon]`, `rotate-180` on open |
| Switch knob | `transition-transform duration-[--dur-fast]` |
| Dialog, sheet | `duration-[--dur-dialog]`; popover, tooltip, dropdown `duration-[--dur-panel]` |
| Table, pagination figures | `tabular-nums` |
| Card title, dialog title, alert title | `text-wrap: balance`; descriptions `pretty` |

Named properties only. A `transition-all` left in a generated component is a patch that was
not applied.

## 6. Fonts

Self-host. No CDN link.

```bash
npm i @fontsource-variable/<display> @fontsource-variable/<body>
```

Import once, in the root layout, above the CSS import. Then confirm the script test string
from `tokens.md` renders in the real font at every shipped weight — a missing glyph falls
back silently.

## 7. Icons

HugeIcons is the registry. Install the renderer and the free set:

```bash
npm i @hugeicons/react @hugeicons/core-free-icons
```

shadcn primitives ship with `lucide-react` imports. Replace every one of them:

```tsx
- import { Check } from "lucide-react"
- <Check className="h-4 w-4" />
+ import { HugeiconsIcon } from "@hugeicons/react"
+ import { Tick02Icon } from "@hugeicons/core-free-icons"
+ <HugeiconsIcon icon={Tick02Icon} size={16} strokeWidth={1.5} />
```

Files that carry them: `checkbox`, `select`, `dropdown-menu`, `dialog`, `sheet`,
`accordion`, `radio-group`, `sonner`, `table` pagination. Then remove `lucide-react` from
`package.json` — two icon sets in one build is two icon sets on one screen.

```bash
npm uninstall lucide-react
```

Wrap the recurring ones once, so the semantic map from `tokens.md` exists as code:

```tsx
// src/components/ui/icon.tsx
import { HugeiconsIcon } from "@hugeicons/react";
import { CheckmarkBadge01Icon, Search01Icon } from "@hugeicons/core-free-icons";

export const icons = { verified: CheckmarkBadge01Icon, search: Search01Icon } as const;

export function Icon({ name, size = 20, ...rest }: { name: keyof typeof icons; size?: number }) {
  return <HugeiconsIcon icon={icons[name]} size={size} strokeWidth={1.5} {...rest} />;
}
```

## 8. The domain component

shadcn primitives only. No new dependencies.

```
src/components/<domain>/<Name>.tsx
```

Typed props, no `any`. Every state from `components.md` implemented, including the empty
one. Polish pass from `polish.md` applied.

## 9. Verify

```bash
npx tsc --noEmit          # or the project's typecheck script
npm run build
```

Both clean before writing the HTML page.

---

## What lands in the repo

```
components.json                     # shadcn config
src/components/ui/*.tsx             # installed primitives
src/components/ui/icon.tsx          # HugeIcons wrapper + the semantic map
src/components/<domain>/*.tsx       # the domain component
src/styles/global.css               # tokens + polish base layer
tokens.json                         # same values, machine-readable
docs/design-system.html             # the page
```
