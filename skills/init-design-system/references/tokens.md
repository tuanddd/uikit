# Tokens

Eight groups. Every token needs a **role**, not a description. Write "Page background", not
"warm light gray".

Colors are **OKLCH**. Spacing is 4-point. Surfaces get shadow-borders, not borders.
Icons come from HugeIcons.

---

## Layer model

Two layers. Keep them separate.

```css
/* Layer 1 — brand primitives. Raw values. Never referenced by components. */
--brand-stone-50: oklch(0.985 0.004 95);
--brand-teal-700: oklch(0.420 0.062 165);

/* Layer 2 — shadcn semantic tokens. What components actually consume. */
--background: var(--brand-stone-50);
--primary:    var(--brand-teal-700);
```

Components only ever read layer 2.

---

## 1. Color — OKLCH

`oklch(L C H)` · `oklch(L C H / alpha)`

| Channel | Range | Controls |
|---|---|---|
| L — lightness | `0`–`1` | Perceived brightness. Uniform across hues. |
| C — chroma | `0`–`~0.37` | Intensity. `0` is neutral gray. |
| H — hue | `0`–`360` | The hue angle. |

Why it is the only format used here: L is perceptually uniform, so a ramp built by
stepping L reads as evenly spaced at every hue, and a shade set built by holding C and H
keeps its hue instead of drifting.

### Two colors carry the brand — pick them first

**Primary, then accent. Then everything else.** Those two hues are the product. They are
what someone would name if asked what color the brand is, and they are the only two on the
screen that were chosen rather than derived or dictated. Pick them before a single ramp is
built, because every other family is measured against them.

| Rank | Family | What it is | Where it lands |
|---|---|---|---|
| 1 | **Primary** | The brand hue. Exactly one. | Buttons, links, focus ring, selected and active states, the logo mark |
| 2 | **Accent** | The second hue, and the only other chosen one. | Tag and badge fills, eyebrows, the editorial mark, anything highlighted rather than actioned |
| 3 | Neutrals | Derived — the primary's hue at a chroma near zero. | Every surface, line, and body text |
| 4 | Status | Dictated by convention, not by the brand. | Error, warning, success. Product UI only. |
| 5 | Charts | Derived — one L, one C, five H. | Data visualization only |

Rules:

1. **Two chosen hues, maximum.** A third non-neutral family means none of the three reads as
   the brand. What looks like a third is a step on one of the two — the dark end of the
   accent ramp is the editorial mark, not a new color.
2. **Primary is the action; accent is never one.** A user who learns that primary means
   "clickable" must never meet an accent-colored button.
3. **Neutrals take their hue from the primary,** at `C` between `0.002` and `0.012`. A warm
   brand gets warm grays. A neutral picked from a different hue than the primary reads as
   dirt beside it.
4. **Status colors are not brand colors.** Red, amber, green are read before they are
   recognized. Never spend the primary or the accent on a status, and never restyle a status
   to match the brand.
5. **Primary and accent must be tellable apart** from each other and from every status color,
   at every size, and in grayscale. Two hues 30° apart are one hue to most people.
6. **Harvest before picking.** If the repo, the logo, or the brand docs already ship a color,
   that is the primary and it is not up for re-selection. Pick only what is missing.

### Building a ramp

**Shades of one hue:** hold `H`, hold or gently taper `C`, step `L`.

| Step | L | Note |
|---|---|---|
| `50` | 0.98 | |
| `100` | 0.96 | |
| `200` | 0.92 | |
| `300` | 0.87 | |
| `400` | 0.78 | |
| `500` | 0.68 | peak chroma sits near here |
| `600` | 0.58 | |
| `700` | 0.48 | |
| `800` | 0.38 | |
| `900` | 0.26 | |

Chroma budget: neutrals `0.002`–`0.012` · accents `0.05`–`0.15`. Taper C at both ends of
the ramp — high chroma at L below 0.35 or above 0.92 falls out of sRGB.

**A set of hues at one weight:** hold `L`, hold `C`, step `H`. Every swatch reads at the
same brightness. This is how chart colors and tag colors get built.

### Gotchas

| Gotcha | Handling |
|---|---|
| Out of gamut | The browser clips to the nearest displayable color, which can shift it hard. Verify each token renders as authored; drop C until it does. |
| Gradient hue detours | H is circular, so an OKLCH gradient can swing through hues nobody picked. Interpolate gradients `in oklab`. |
| L is not WCAG luminance | Two tokens at the same L can have different contrast ratios. Measure WCAG ratios; never infer them from L. |

### Legacy fallback

Only if the project supports browsers older than 2023.

```css
:root {
  --background: #FAFAF7;
  @supports (color: oklch(0 0 0)) {
    --background: oklch(0.985 0.004 95);
  }
}
```

### Budget

Draw this as a proportion bar, not a list.

| Family | Budget | Job |
|---|---|---|
| Neutrals | ~90% | Every surface, line, and body text |
| Accent | ~5% | Tag and badge fills, eyebrows, the editorial mark |
| Primary | ~4% | Buttons, links, focus ring |
| Status | ~1% | Error, warning, success. Product UI only. |

Numbers, never "sparingly".

The two chosen hues are ~9% of the pixels and 100% of what the brand is remembered as. That
is the point of the budget: reserved is what makes them read as deliberate. A primary spent
on decoration stops meaning "action" the first time it is.

### Primitives

`primary-*` and `accent-*` are the two chosen hues. Everything above and below them follows
from that choice, so fill those two rows first and derive the rest.

| Token | OKLCH | Role | Pairs with |
|---|---|---|---|
| `neutral-50` | `oklch(0.985 ___ ___)` | Page background | ink, neutral-200 |
| `neutral-100` | `oklch(0.960 ___ ___)` | Second surface | ink |
| `neutral-200` | `oklch(0.920 ___ ___)` | Divider, input border | — |
| `neutral-300` | `oklch(0.870 ___ ___)` | Disabled fill | dark text only |
| `neutral-500` | `oklch(0.680 ___ ___)` | Icons | never body text |
| `neutral-700` | `oklch(0.480 ___ ___)` | Secondary text | neutral-50 |
| `ink` | `oklch(0.260 ___ ___)` | Body text. The only near-black. | neutral-50 |
| `accent-50` | `oklch(0.960 ___ ___)` | Tag fill | accent-900 |
| `accent-400` | `oklch(0.780 ___ ___)` | Badge fill | accent-900 |
| `accent-900` | `oklch(0.300 ___ ___)` | Text on accent fills | — |
| `primary-500` | `oklch(0.560 ___ ___)` | Hover | light text |
| `primary-700` | `oklch(0.460 ___ ___)` | Buttons, links | light text |
| `primary-900` | `oklch(0.340 ___ ___)` | Pressed | light text |
| `error` | `oklch(0.520 0.180 27)` | Destructive | light text |
| `warning` | `oklch(0.800 0.140 85)` | Caution fill | dark text |
| `success` | `oklch(0.520 0.110 155)` | Confirmed fill | light text |

### shadcn map

Fill every row. An unmapped variable is an unstyled component.

| shadcn variable | Source token |
|---|---|
| `--background` | `neutral-50` |
| `--foreground` | `ink` |
| `--card` / `--card-foreground` | `neutral-50` / `ink` |
| `--popover` / `--popover-foreground` | `neutral-50` / `ink` |
| `--primary` / `--primary-foreground` | `primary-700` / `neutral-50` |
| `--secondary` / `--secondary-foreground` | `neutral-100` / `ink` |
| `--muted` / `--muted-foreground` | `neutral-100` / `neutral-700` |
| `--accent` / `--accent-foreground` | `accent-50` / `accent-900` |
| `--destructive` | `error` |
| `--border` | `neutral-200` |
| `--input` | `neutral-200` |
| `--ring` | `primary-700` |
| `--chart-1` … `--chart-5` | one L, one C, five H — see "a set of hues at one weight" |
| `--sidebar*` | mirror the above; only if the product has a sidebar |

### Contrast

Measure. Do not copy ratios from another document, and do not infer them from L.

| Pair | Ratio | Verdict |
|---|---|---|
| ink on neutral-50 | `__:1` | AAA |
| neutral-700 on neutral-50 | `__:1` | AA body |
| neutral-50 on primary-700 | `__:1` | AA |

Render each row in the actual color pair. A ratio the reader can see is a ratio the reader
believes. Only pairs that pass go on the page.

---

## 2. Typography

Two families, maximum. Two weights each.

| Slot | Family | Weights | Use |
|---|---|---|---|
| Display | `______` | 400, 500 | Headings |
| Body | `______` | 400, 500 | Everything else |

### Scale — only these

~1.2 modular, hand-tuned.

| Token | Size | Weight | Line height | Tracking | Use |
|---|---|---|---|---|---|
| `display` | 36–56px | 400 | 1.05 | -0.02em | Hero |
| `h2` | 30px | 400 | 1.15 | -0.01em | Section |
| `h3` | 24px | 400 | 1.20 | -0.01em | Card title |
| `lead` | 18px | 400 | 1.50 | 0 | Intro line |
| `body` | 16px | 400 | 1.60 | 0 | Body |
| `small` | 14px | 400 | 1.50 | 0 | Meta |
| `caption` | 12px | 500 | 1.40 | 0 | Labels |
| `eyebrow` | 11px | 500 | 1.40 | 0.08em | Uppercase labels beside a value; never above a heading |

### Rules

1. Headings 1.0–1.25 line height. Body 1.5–1.75.
2. All caps only at `eyebrow`, and `eyebrow` only on labels that name a value: table headers, form labels, timeline stamps. Never as a line above a title.
3. Buttons sentence case.
4. Prices, counts, dates, timers: `font-variant-numeric: tabular-nums`.
5. Touch inputs ≥16px, or iOS zooms on focus.
6. Running text 45–75 characters.
7. `-webkit-font-smoothing: antialiased` once, on the root.
8. `text-wrap: balance` on every block under ~4 lines — headings, card and dialog titles,
   alert titles, captions, any label that can wrap. `text-wrap: pretty` on paragraphs,
   helper text, and descriptions. No line is left holding one word; no `<br>` or `&nbsp;`
   is used to fix one. Both ship in the base layer (`polish.md` § Text).

### Script test

If the product uses diacritics or a non-Latin script, name the exact test string and
render it at every shipped weight.

> `Đà Nẵng · Hồ Chí Minh · Nguyễn`

---

## 3. Spacing

4-point scale. **Only these values.** No 7, no 18, no 22.

| Token | Value | Tailwind | Use |
|---|---|---|---|
| `space-1` | 4px | `p-1` | Icon to label · label to control |
| `space-2` | 8px | `p-2` | Tag to tag · control padding |
| `space-3` | 12px | `p-3` | Field to field · control padding |
| `space-4` | 16px | `p-4` | Card padding · card to card |
| `space-6` | 24px | `p-6` | Card padding when comfortable |
| `space-8` | 32px | `p-8` | Block to block |
| `space-12` | 48px | `p-12` | Section to section |
| `space-16` | 64px | `p-16` | Around a hero |

Gap between groups always exceeds gap within a group. At both densities.

### Density — compact is the default

One decision, made once, applied to every component and to the page. Never two presets in
one product.

| Slot | Compact | Comfortable |
|---|---|---|
| Label → control | 4 | 8 |
| Icon → label | 4 | 8 |
| Control padding — button, input | 8 / 12 | 12 / 16 |
| Field → field | 12 | 16 |
| Card padding | 16 | 24 |
| Card → card | 16 | 24 |
| Block → block | 32 | 48 |
| Section → section | 48 | 64 |
| Page margin, mobile / desktop | 16 / 32 | 24 / 48 |

Rules:

1. A tie between two steps goes to the smaller one.
2. Touch targets stay ≥44×44px at both densities. Compact shrinks padding, never the target.
3. Line height and the 45–75 character measure never tighten with the spacing.
4. Compact is not crowded: the group/within-group gap ratio holds, it just holds at 16/8
   instead of 24/12.

Ship comfortable when the user asks, or when the domain earns it:

| Domain | Why |
|---|---|
| Editorial, long reading | The air is the reading experience |
| Property, hospitality, luxury goods | Space is part of what is being sold |
| Marketing pages, one idea per screen | The idea needs the room |
| Anything read at distance — print, projection, TV | Viewing distance |

Compact is right for dashboards, tables, admin tools, anything used daily, and anything
mobile-first — density is the feature there, and scrolling is the cost.

### Grid

Compact. Comfortable adds one step to gutter and margin.

| Breakpoint | Columns | Gutter | Margin |
|---|---|---|---|
| Desktop | 12 | 24px | 32px |
| Tablet | 8 | 16px | 24px |
| Mobile | 4 | 16px | 16px |

---

## 4. Radius

| Token | Value | Wraps |
|---|---|---|
| `radius-sm` | `calc(var(--radius) - 4px)` | Tags, checkboxes |
| `radius-md` | `calc(var(--radius) - 2px)` | Buttons, inputs |
| `radius-lg` | `var(--radius)` | Cards, dialogs |
| `radius-xl` | `calc(var(--radius) + 4px)` | Heroes, sheets |
| `radius-full` | `9999px` | Avatars, pills |

Set `--radius` once. shadcn derives the rest.

**Concentric rule:** `outer radius = inner radius + padding`.
A 12px inner element inside 8px of padding needs a 20px outer radius. Anything else
reads as pinched at the corners.

---

## 5. Border

Borders are for **lines**, not for surfaces. Surfaces get a shadow-border (group 6).

| Token | Value | Use |
|---|---|---|
| `border-hairline` | 1px | Dividers, table rules, input edge |
| `border-emphasis` | 2px | Focus ring, active tab marker |
| `border-heavy` | 4px | Quote rule |
| `outline-image` | `1px solid oklch(0 0 0 / 0.10)` + `outline-offset: -1px` | Every image and video |

The image outline is not optional. It keeps a light photo from bleeding into a light page
and matches the edge weight of every other surface.

---

## 6. Shadow

Shadows carry both the **edge** and the **elevation**. Every token opens with a
`0 0 0 1px` layer, so a surface never loses its edge as it rises. Because the layers are
transparent, they hold up on any background — a solid border color does not.

```css
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
```

| Token | Use |
|---|---|
| `shadow-border` | Every resting surface: card, input, table, thumbnail |
| `shadow-border-hover` | The same surface on hover and focus-visible |
| `shadow-md` | Dropdown, popover, tooltip |
| `shadow-lg` | Dialog, sheet |
| `shadow-none` | Flush surfaces inside an already-elevated container |

Three layers, one job each: **1px spread** = the edge · **short blur, negative spread** =
the contact shadow · **wide blur** = the ambient.

Hover changes opacity only, never geometry — the surface should not appear to jump. Put
`box-shadow` in the transition property, at `--dur-fast` and `--ease-out` (group 8).

Dark theme, if the brand ships one: a single light layer replaces the stack —
`0 0 0 1px oklch(1 0 0 / 0.08)`, hover `0.12`.

If the brand forbids depth entirely, ship `shadow-border` alone as a flat 1px spread.

---

## 7. Icons

**Registry: HugeIcons.** One registry for every icon in the product.

```bash
npm i @hugeicons/react @hugeicons/core-free-icons
```

| Package | Holds |
|---|---|
| `@hugeicons/react` | `HugeiconsIcon`, the renderer |
| `@hugeicons/core-free-icons` | Stroke Rounded — the shipped style |
| `@hugeicons-pro/core-solid-rounded` | The solid twin, only with a pro licence |

```tsx
import { HugeiconsIcon } from "@hugeicons/react";
import { Search01Icon } from "@hugeicons/core-free-icons";

<HugeiconsIcon icon={Search01Icon} size={20} strokeWidth={1.5} color="currentColor" />
```

Props: `icon` · `altIcon` · `showAlt` · `size` (24) · `color` (`currentColor`) ·
`strokeWidth` (1.5) · `absoluteStrokeWidth` · `className`.

### Style

One style, product-wide: **Stroke Rounded**. It carries the same drawn-line weight as the
type, so an icon sits inside a line of text without shouting.

Every free icon has a solid twin in the pro set, so an active state swaps the drawing
instead of recoloring it:

```tsx
<HugeiconsIcon icon={FavouriteIcon} altIcon={FavouriteSolidIcon} showAlt={saved} />
```

### Size — only these

| Token | Value | Set beside | Use |
|---|---|---|---|
| `icon-xs` | 14px | caption 12 · small 14, lowercase, inside a sentence | Tag, inline meta in running text |
| `icon-sm` | 16px | body 16 · any uppercase or letter-spaced label (eyebrow 11, caption 12) | Inside inputs and badges; beside every label that reads in caps |
| `icon-md` | 20px | body 16 · buttons | Button leading icon. The default. |
| `icon-lg` | 24px | h3 24 | List rows, card headers |
| `icon-xl` | 32px | h2 30 · display | Empty state, feature mark |

Size comes from the `size` prop. `transform: scale()` thins the stroke with it.

### Stroke

| Token | Value | Use |
|---|---|---|
| `icon-stroke` | 1.5 | 14–24px, beside 400-weight text |
| `icon-stroke-bold` | 2 | 32px and up, or beside 500-weight text |

Icon stroke matches the weight of the text next to it. An uppercase or letter-spaced label
reads larger than its font size, so it takes the icon one size up: eyebrow 11 pairs with
`icon-sm` 16, never `icon-xs`.

### Beside a label

The label holds one line. If it must wrap, the row aligns to the first line, not the middle:

```css
.label { display: flex; align-items: flex-start; gap: var(--space-1); }
.label > svg { height: 1lh; width: 16px; flex: none; }  /* box = line-height, glyph centred */
```

### Color

| Case | Color |
|---|---|
| Icon inside text, a button, or a link | `currentColor` |
| Standalone and decorative | `--muted-foreground` |
| Status | `--destructive` · `warning` · `success` |

### Rules

1. Every icon comes from HugeIcons. The logo mark is the one hand-drawn SVG.
2. Icon-only controls carry `aria-label`. An icon beside a label carries `aria-hidden="true"`.
3. Icon-only touch targets stay ≥44×44px; the icon keeps its size token, the target grows.
4. Align optically, not by bounding box.
5. One icon per meaning, product-wide. The map below is the source of truth.

### The semantic map

Roles, not pictures. One row per recurring meaning in this product. Start from these — the
components in `components.md` reference them by role — then add the roles the domain needs.

**Structural — every product ships these.** They are the ones the shadcn primitives read.

| Role | HugeIcons name | Where |
|---|---|---|
| `icon-chevron-down` | `ArrowDown01Icon` | Select, dropdown, accordion — rotates 180° on open |
| `icon-chevron-right` | `ArrowRight01Icon` | Breadcrumb separator, nested menu |
| `icon-arrow-left` · `icon-arrow-right` | `ArrowLeft01Icon` · `ArrowRight01Icon` | Pagination |
| `icon-check` | `Tick02Icon` | Checkbox, switch knob, selected menu item |
| `icon-indeterminate` | `MinusSignIcon` | Checkbox, mixed state |
| `icon-close` | `Cancel01Icon` | Dialog, sheet, toast, clearable input |
| `icon-loading` | `Loading03Icon` | Spinner — one glyph, product-wide |
| `icon-more` | `MoreHorizontalIcon` | Row actions, overflow menu |
| `icon-sort` | `ArrowUpDownIcon` | Table header, unsorted |
| `icon-sort-asc` · `icon-sort-desc` | `ArrowUp01Icon` · `ArrowDown01Icon` | Table header, sorted |
| `icon-info` | `InformationCircleIcon` | Tooltip trigger, info alert |
| `icon-success` | `CheckmarkCircle02Icon` | Success alert, success toast |
| `icon-warning` | `Alert02Icon` | Warning alert |
| `icon-error` | `AlertCircleIcon` | Destructive alert, field error |
| `icon-search` | `Search01Icon` | Search field |
| `icon-hidden` · `icon-visible` | `ViewOffIcon` · `ViewIcon` | Password reveal |
| `icon-external` | `LinkSquare01Icon` | Link leaving the product |
| `icon-delete` | `Delete02Icon` | Destructive menu item |
| `icon-empty` | product-specific | Empty state, `icon-xl` |

**Domain — the meanings only this product has.** One row per recurring fact kind, so a
card meta line, a table column, and a detail page all mark the same thing the same way.

| Role | HugeIcons name | Where |
|---|---|---|
| `icon-verified` | `CheckmarkBadge01Icon` | Inspection record, verified badge |
| `icon-location` | `Location01Icon` | Listing meta |
| `icon-calendar` | `Calendar03Icon` | Availability |
| `icon-area` | `Ruler01Icon` | Listing meta |
| `icon-price` | `MoneyBag02Icon` | Cost breakdown |

### CSS

```css
--icon-xs: 14px;
--icon-sm: 16px;
--icon-md: 20px;
--icon-lg: 24px;
--icon-xl: 32px;
--icon-stroke: 1.5;
--icon-stroke-bold: 2;
```

Verify every HugeIcons export name against the installed package before shipping it — a
name that does not exist renders nothing, silently. The names above are the starting map,
not a guarantee; substitute the nearest real export and record it in the table.

---

## 8. Motion

Motion is a token group like any other: named durations, one easing, spent on every
interactive element. It is not a page section — it ships inside the components.

**Every interactive element transitions.** A control that snaps between states reads as a
glitch; a control that eases reads as a response. Quick and quiet is the whole brief —
under 200ms, ease-out, no motion loud enough to pull the eye off the content.

### Tokens

```css
--ease-out:     cubic-bezier(0.2, 0, 0, 1);
--ease-entrance: cubic-bezier(0.25, 0.46, 0.45, 0.94);

--dur-press:   80ms;   /* :active compression */
--dur-fast:   120ms;   /* hover, focus, color, shadow — the default */
--dur-icon:   150ms;   /* glyph swap, chevron rotate */
--dur-panel:  160ms;   /* popover, dropdown, tooltip, accordion */
--dur-dialog: 240ms;   /* dialog, sheet */
--dur-enter:  800ms;   /* staged entrance, keyframes only */
```

| Action | Token | Easing |
|---|---|---|
| Press | `--dur-press` | `--ease-out` |
| Hover, focus, shadow, color change | `--dur-fast` | `--ease-out` |
| Icon swap, chevron rotate | `--dur-icon` | `--ease-out` |
| Popover, dropdown, tooltip, accordion | `--dur-panel` | `--ease-out` |
| Dialog, sheet | `--dur-dialog` | `--ease-out` |
| Staged entrance | `--dur-enter` | `--ease-entrance` |

### Rules

1. Interactions use **transitions** so they can be interrupted mid-flight. Keyframes are
   for one-shot staged sequences only.
2. Name the transitioned properties. Never `transition: all`.
3. Composite properties only — `opacity`, `transform`, `color`, `background-color`,
   `box-shadow`. Never `width`, `height`, or `margin` on an interaction.
4. Hover changes opacity, color, and shadow. Only `:active` changes geometry, and only on
   a control: `transform: scale(0.985)`.
5. Same duration in both directions.
6. Nothing bounces. No easing overshoots.
7. `prefers-reduced-motion: reduce` keeps color and opacity, drops every transform.

The per-element property map lives in `polish.md` § Transitions.

---

## Output as code

Write the tokens twice, same values:

1. **CSS** — into the project's `globals.css` (see `shadcn-setup.md`).
2. **`tokens.json`** — flat, one `$value` and one `$description` (the role) per token,
   plus one top-level `density` key: `compact` or `comfortable`.

Both files are generated from the same table. If they disagree, the CSS is wrong.
