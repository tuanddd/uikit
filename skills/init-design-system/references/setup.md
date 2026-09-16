# Wiring the project

The viewer renders what is installed. So install first, then build the viewer.

Detect the stack (`stacks.md` § 1) before doing anything. The token injection, fonts, and
icons are shared; the primitive layer and the component authoring are per stack.

---

## 1. Initialize the primitive base

### React — shadcn/ui

```bash
npx shadcn@latest init
```

Answers: **CSS variables → yes**. Base color → the closest neutral to the brand; it gets
overwritten in step 2 anyway.

Astro-in-React or Next adds `app/globals.css`; Vite adds `src/index.css`; Remix adds
`app/tailwind.css`. That file is the target for step 2.

### Svelte — Bits UI

`bits-ui` is the Svelte analogue of Radix: headless, accessible, unstyled. Install it and
nothing else for behaviour.

```bash
npm i bits-ui
```

Components are written as `.svelte` files that wrap the Bits UI parts. Styling uses the
project's approach — scoped `<style>` reading the tokens if the project does not use
Tailwind, Tailwind classes if it does. Do **not** add a variants library: a five-line local
`cn()` that joins truthy class strings is enough, and add `tailwind-merge` only if the
project already ships it.

### Astro — nothing to initialize

Astro ships routing and islands. No primitive library is installed: the interactive
primitives are native `.astro` components with a small progressive-enhancement `<script>`.
If the project already mounts a UI framework (React, Svelte) for islands, author the
components in that framework's directory instead and reuse its primitive layer.

---

## 2. Inject the tokens

One block, the same in every stack. Replace the generated `:root` block, or append it to the
project's global stylesheet if there is none. Keep every color in OKLCH.

`tokens.json` is the single authored source (SKILL.md step 2, `tokens.md` § Output); this
`:root` block is its projection into CSS, and every component and the viewer read these
variables. Write the JSON first, then derive the CSS from it, and check the two agree before
shipping — the viewer prints values from `tokens.json` and fills swatches from `var(--…)`,
so a disagreement is a token that shows one value and renders another.

In React, keep shadcn's variable **names** exactly — every installed primitive reads them.
In Svelte and Astro the same names are the contract; the components are authored to read
them, so a name is a promise the whole system depends on.

`--space-*` and `--radius-*` are defined here as raw custom properties, not only as Tailwind
utilities: the viewer's shell and the component examples read `var(--space-*)` /
`var(--radius-*)` directly, and they must resolve in a project without Tailwind.

```css
@import "tailwindcss";          /* Tailwind v4 only — drop for v3 or plain CSS */
@import "tw-animate-css";       /* Tailwind v4 only */
@custom-variant dark (&:is(.dark *));  /* Tailwind v4 only */

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
  --radius-sm: calc(var(--radius) - 4px);
  --radius-md: calc(var(--radius) - 2px);
  --radius-lg: var(--radius);
  --radius-xl: calc(var(--radius) + 4px);
  --radius-full: 9999px;

  /* spacing — the 4-point scale, only these */
  --space-1: 4px;
  --space-2: 8px;
  --space-3: 12px;
  --space-4: 16px;
  --space-6: 24px;
  --space-8: 32px;
  --space-12: 48px;
  --space-16: 64px;

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
  --shadow-none: none;

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

**No Tailwind:** drop the three v4 lines; the `:root` block is plain CSS and every component
and the viewer read it directly, so nothing else changes.

**Tailwind v4:** add the `@theme inline` block below so the brand names generate utilities.
`inline` inlines the value into the utilities rather than emitting a variable — which is why
the real variables live in `:root` above, and why `var(--radius-lg)` resolves without it.

```css
@theme inline {
  --font-display: var(--font-display);
  --font-body: var(--font-body);
  --radius-sm: var(--radius-sm);
  --radius-md: var(--radius-md);
  --radius-lg: var(--radius-lg);
  --radius-xl: var(--radius-xl);
  --shadow-border: var(--shadow-border);
  --shadow-border-hover: var(--shadow-border-hover);
  --ease-out: var(--ease-out);
  --duration-fast: var(--dur-fast);
  --duration-icon: var(--dur-icon);
  --duration-panel: var(--dur-panel);
  --duration-dialog: var(--dur-dialog);
}
```

**Tailwind v3:** the same names go in `tailwind.config.js` under `theme.extend`; the `:root`
variables above still carry the values, so the components work either way.

```js
// tailwind.config.js
export default {
  theme: {
    extend: {
      fontFamily: { display: ["Fraunces", "Georgia", "serif"], body: ["Inter", "system-ui", "sans-serif"] },
      borderRadius: {
        sm: "var(--radius-sm)", md: "var(--radius-md)",
        lg: "var(--radius-lg)", xl: "var(--radius-xl)", full: "var(--radius-full)",
      },
      boxShadow: {
        border: "var(--shadow-border)", "border-hover": "var(--shadow-border-hover)",
        md: "var(--shadow-md)", lg: "var(--shadow-lg)",
      },
    },
  },
};
```

## 3. The polish base layer

`polish.md` covers the details; this is the base.

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

Astro scopes styles per component, so the base layer goes in the Astro global stylesheet
(`src/styles/global.css`), imported once in the base layout.

**Dark theme:** only if the brand ships one. In dark, the shadow stack collapses to a
single light edge — `0 0 0 1px oklch(1 0 0 / 0.08)`, hover `0.12`. If the brand is
light-only, delete the `.dark` block.

## 4. Verify the gamut

OKLCH accepts values no display can show; the browser silently clips them. Render each
token and confirm it matches what was authored. If a swatch looks flat or shifted, lower
its chroma until it does not.

---

## 5. Author the components

`components.md` owns the inventory, the anatomy, the states, and the icon slots. It is
stack-neutral. This section is only *how* each stack builds them.

### React — install and patch

One command. List comes from `components.md`; trim it to what the product actually renders.

```bash
npx shadcn@latest add button input label textarea select checkbox radio-group switch \
  badge alert card separator avatar tabs dialog dropdown-menu popover tooltip sheet \
  table pagination form sonner skeleton spinner accordion
```

`spinner` is a newer registry entry. If the CLI does not resolve it, build one from the
`icon-loading` role instead — the semantic glyph, `animate-spin`, sized off the icon scale
— and keep it in `src/components/ui/spinner.tsx` so the rest of the system imports it the
same way.

Then patch the installed primitives onto the system:

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

### Svelte — wrap Bits UI

`bits-ui` gives each primitive as composable parts; the wrapper is a `.svelte` file whose
props mirror the shadcn API, so the rest of the system reads the same way. One file per
component, in the component directory.

```svelte
<!-- src/lib/components/ui/button.svelte -->
<script lang="ts">
  import type { Snippet } from "svelte";
  let {
    variant = "primary", size = "md", disabled = false, children,
  }: {
    variant?: "primary" | "secondary" | "ghost" | "destructive";
    size?: "sm" | "md" | "lg";
    disabled?: boolean;
    children: Snippet;
  } = $props();
</script>

<button
  class="btn btn-{variant} btn-{size}"
  {disabled}
  data-slot="button"
>{@render children()}</button>

<style>
  .btn {
    display: inline-flex; align-items: center; gap: var(--space-2);
    padding: var(--pad-control); border-radius: var(--radius-md);
    background: var(--primary); color: var(--primary-foreground);
    border: 0; font: inherit; cursor: pointer;
    transition-property: background-color, color, box-shadow, transform;
    transition-duration: var(--dur-fast);
    transition-timing-function: var(--ease-out);
  }
  .btn:active { transform: scale(0.985); transition-duration: var(--dur-press); }
  .btn:focus-visible { outline: 2px solid var(--ring); outline-offset: 2px; }
  .btn:disabled { opacity: 0.5; }
</style>
```

The interactive primitives wrap Bits UI parts instead of a native element: `Dialog` over
`Dialog.Root`/`Trigger`/`Content`, `Select` over `Select.Root`/`Trigger`/`Content`,
`DropdownMenu` over `DropdownMenu.*`, `Tooltip` over `Tooltip.*`, `Switch`, `Checkbox`,
`RadioGroup`, `Tabs`, `Accordion`, `Popover`. Style the Bits parts from the tokens; the
behaviour, focus management, and ARIA come from the library. Bits UI ships `data-state`
attributes (`open`, `closed`, `checked`) — transition on those, not on your own flags.

Rules that do not change: one component per file, typed props with defaults, no `any`,
every state in `components.md` implemented, the icon slot filled from the semantic map.

### Astro — native components with progressive enhancement

One `.astro` file per component. Frontmatter holds the props interface; the template holds
the markup; a scoped `<style>` reads the tokens. Server-render everything; add client JS
only where a state needs it.

```astro
---
// src/components/ui/Button.astro
import Icon from "./Icon.astro";
import type { IconName } from "./icons";
interface Props {
  variant?: "primary" | "secondary" | "ghost" | "destructive";
  size?: "sm" | "md" | "lg";
  disabled?: boolean;
  icon?: IconName;
  href?: string;
}
const { variant = "primary", size = "md", disabled = false, icon, href } = Astro.props;
const Tag = href ? "a" : "button";
---
<Tag class:list={["btn", `btn--${variant}`, `btn--${size}`]}
     href={href} disabled={!href && disabled} data-slot="button">
  {icon && <Icon name={icon} size="md" />}
  <slot />
</Tag>

<style>
  .btn { display: inline-flex; align-items: center; gap: var(--space-2);
         padding: var(--pad-control); border-radius: var(--radius-md);
         transition-property: background-color, color, box-shadow, transform;
         transition-duration: var(--dur-fast); transition-timing-function: var(--ease-out); }
  .btn:active { transform: scale(0.985); transition-duration: var(--dur-press); }
  .btn:focus-visible { outline: 2px solid var(--ring); outline-offset: 2px; }
</style>
```

Interactive primitives take their behaviour from the **platform first**, then a small script.
A native element that already implements the semantics beats a hand-rolled one, and it needs
no dependency:

| Primitive | Base | Behaviour |
|---|---|---|
| Dialog | `<dialog>` | `showModal()` gives the focus trap, Esc, and the top layer; the script only opens and closes |
| DropdownMenu | `popover` attribute + `popovertarget` | open/close is the platform's; a small script adds arrow-key roving focus over `role="menuitem"` |
| Select | native `<select>` | style it; only build a popover listbox when the design cannot use the native control |
| Tooltip | `popover` with `role="tooltip"` | show on `focusin`/`mouseenter`, hide on `focusout`/`mouseleave`/Esc; the trigger carries `aria-describedby` |
| Tabs | buttons + `role="tablist"` | roving focus and `aria-selected` in one script |
| Switch / Checkbox / Radio | native `input` | only the visual layer is custom; the input keeps the state |

A concrete Dialog, native-first:

```astro
---
// src/components/ui/Dialog.astro
interface Props { id: string; title: string }
const { id, title } = Astro.props;
---
<button class="btn" data-open={id} aria-haspopup="dialog">Open</button>
<dialog id={id} class="dialog" aria-labelledby={`${id}-title`}>
  <h2 id={`${id}-title`}>{title}</h2>
  <slot />
  <form method="dialog"><button class="btn btn--secondary">Close</button></form>
</dialog>
<script>
  document.querySelectorAll("[data-open]").forEach((trigger) => {
    trigger.addEventListener("click", () =>
      document.getElementById(trigger.dataset.open)?.showModal());
  });
</script>
```

Without the script a Dialog degrades to its closed state — the trigger does nothing. That is
acceptable for a dev-surface specimen and honest for production; do not fake an open state.
Whatever the primitive, verify it with the keyboard (Tab, Shift-Tab, Esc, arrows) and check
the accessible name, `aria-expanded` / `aria-controls` or `aria-describedby`, focus return on
close, and, for Dialog, the background scroll lock. A primitive that cannot be operated by
keyboard is not shipped.

Every component file shares the same icon renderer (`Icon.astro`, step 7), so the semantic
map stays the single source.

---

## 6. Fonts

Self-host. No CDN link.

```bash
npm i @fontsource-variable/<display> @fontsource-variable/<body>
```

Import once, in the root layout, above the CSS import. Astro: the base layout frontmatter.
SvelteKit: `src/routes/+layout.svelte`. Next: `app/layout.tsx`. Vite: `src/main.tsx`.

Then confirm the script test string from `tokens.md` renders in the real font at every
shipped weight — a missing glyph falls back silently.

## 7. Icons

HugeIcons is the registry, and each stack renders it through one component.

**React:**

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

**Svelte:**

```bash
npm i @hugeicons/svelte @hugeicons/core-free-icons
```

Same wrapper shape, `src/lib/components/ui/icon.svelte`, exporting the semantic map as a
`const` and a component that takes `name` / `size` / `label`.

**Astro:** `@hugeicons/core-free-icons` ships raw node data, so no renderer package is
needed. Two files: the semantic map, then the one renderer every component imports.

```ts
// src/components/ui/icons.ts
import { Add01Icon, Search01Icon } from "@hugeicons/core-free-icons";

export const iconSize = { xs: 14, sm: 16, md: 20, lg: 24, xl: 32 } as const;
export type IconSize = keyof typeof iconSize;

export const icons = { search: Search01Icon, add: Add01Icon } as const;
export type IconName = keyof typeof icons;
```

```astro
---
// src/components/ui/Icon.astro — the only icon renderer in the product.
import { icons, iconSize, type IconName, type IconSize } from "./icons";
interface Props { name: IconName; size?: IconSize | number; label?: string; class?: string }
const { name, size = "md", label, class: className = "" } = Astro.props;
const px = typeof size === "number" ? size : iconSize[size];
const strokeWidth = px >= 32 ? "var(--icon-stroke-bold)" : "var(--icon-stroke)";
const kebab = (k: string) => k.replace(/[A-Z]/g, (c) => `-${c.toLowerCase()}`);
const drop = new Set(["key", "stroke", "strokeWidth", "strokeLinecap", "strokeLinejoin"]);
const parts = (icons[name] as [string, Record<string, string | number>][]).map(([tag, attrs]) => {
  const out: Record<string, string | number> = {};
  for (const [k, v] of Object.entries(attrs)) if (!drop.has(k)) out[kebab(k)] = v;
  return { tag, attrs: out };
});
---
<svg class:list={["icon", className]} width={px} height={px} viewBox="0 0 24 24" fill="none"
     stroke="currentColor" style={`stroke-width:${strokeWidth}`} stroke-linecap="round"
     stroke-linejoin="round" role={label ? "img" : undefined} aria-label={label}
     aria-hidden={label ? undefined : "true"} focusable="false">
  {parts.map((p) => { const Tag = p.tag; return <Tag {...p.attrs} />; })}
</svg>
```

The stroke width goes in `style`, not in the `stroke-width` attribute: a `var()` reference does
not resolve inside an SVG presentation attribute, so the attribute form would silently fall
back to the default width and break the stroke token.

Verify every HugeIcons export name against the installed package before shipping it — a
name that does not exist renders nothing, silently.

## 8. The domain component

The stack's primitives only. No new dependencies.

```
React   src/components/<domain>/<Name>.tsx
Svelte  src/lib/components/<domain>/<Name>.svelte
Astro   src/components/<domain>/<Name>.astro
```

Typed props, no `any`. Every state from `components.md` implemented, including the empty
one. Polish pass from `polish.md` applied.

## 9. Verify

```bash
React   npx tsc --noEmit && npm run build
Svelte  npx svelte-check && npm run build
Astro   npx astro check && npm run build
```

All clean before building the viewer route.

---

## What lands in the repo

```
# shared
tokens.json                         # the single authored source; the CSS is its projection
<global stylesheet>                 # the :root tokens + the polish base layer
robots.txt                          # Disallow: /uikit/  (create if absent)
<sitemap config>                    # excludes the route (only if the project has a sitemap)

# React
components.json                     # shadcn config
src/components/ui/*.tsx             # shadcn primitives, patched
src/components/ui/icon.tsx          # HugeIcons wrapper + the semantic map
src/components/<domain>/*.tsx       # the domain component
src/dev/design-system-enabled.ts    # the env gate
src/dev/Specimen.tsx                # the specimen helper
app/uikit/design-system/page.tsx    # the viewer route

# Svelte
src/lib/components/ui/*.svelte      # one file per component, on Bits UI
src/lib/components/ui/icon.svelte
src/lib/components/<domain>/*.svelte
src/lib/dev/design-system-enabled.ts
src/lib/dev/Specimen.svelte
src/routes/uikit/design-system/+page.svelte

# Astro
src/components/ui/*.astro           # one file per component
src/components/ui/icons.ts          # the semantic map
src/components/ui/Icon.astro        # the only icon renderer
src/components/<domain>/*.astro
src/lib/design-system-enabled.ts
src/components/dev/Specimen.astro
src/pages/uikit/design-system.astro
```
