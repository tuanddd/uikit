---
name: init-design-system
description: >-
  Build a project's design system as a visual HTML page plus a working shadcn/ui setup — OKLCH colors, typography, spacing, radius, borders, layered shadows, logo, and components delivered as installed React code. Use when the user asks for a "design system", "brand design system", "design tokens", "style guide", or "brand guidelines". Reuses tokens already in the repo instead of inventing new ones. Output is code-ready, not a mood board.
---

# Brand design system

Two deliverables. Both required.

1. **`docs/design-system.html`** — the system shown, not described.
2. **The project itself**, wired with shadcn/ui on these tokens, so the next agent builds with it.

## Stance

Opinionated by default. Negotiable on request.

Everything below is the sane default: ship it unasked, without presenting options.
When the user asks for something else — hex, looser spacing, a second icon set, flat
surfaces, a bounce — the ask wins.

| Signal | Response |
|---|---|
| No preference stated | Ship the default |
| Preference stated once | Apply it, name the default it replaced in one line, move on |
| Preference repeated after a flag | Apply it in full. The flag is spent. |
| The domain argues against the default | Take the domain's side, say which default moved |

An override is applied **everywhere it touches** — tokens, components, and the page — or it
is not applied. Half a system on the default and half on the override is the one outcome
worse than either. The page still shows only what ships; it never records what was
overruled.

## Defaults

| Rule | Means |
|---|---|
| Show, never explain | No rationale, no "why this works", no options weighed, no history |
| Every value is drawn | Spacing = bars · Radius = real corners · Border = real strokes · Shadow = real elevation · Type = real specimens · Color = real swatches |
| One line per item | Token, value, role. Stop. |
| Nothing superficial | No vision, mission, voice, tone, photography, illustration, or brand-story section |
| **OKLCH only** | Every color authored `oklch(L C H)`. No hex, no HSL, no RGB, except in a legacy `@supports` fallback. |
| **Two chosen hues** | One primary, one accent — picked first, drawn largest. Neutrals derive from the primary, status is dictated by convention, charts are generated. |
| **Shadows carry surfaces** | Every surface uses the three-layer shadow-border. Borders are for lines. |
| 4-point spacing | 4 · 8 · 12 · 16 · 24 · 32 · 48 · 64. Only these. |
| Constrained scales | ~1.2 modular type scale · five shadow tokens · five radius tokens · grayscale-first hierarchy |
| **One lever, not three** | Rank with size, weight, or color level — one at a time. Two only on the single most important element in a view. |
| **Labels rank below values** | Form labels, table headers, and meta lines drop to `caption`/`eyebrow` at `neutral-700`. They support the data, never compete with it. |
| shadcn/ui is the base | Every component on the page exists as an installed React component in the repo |
| **HugeIcons is the registry** | Every icon from `@hugeicons/core-free-icons`, one style, sizes off the scale. No second set, no one-off SVG. |
| **Icons are structural** | Every component with an icon slot ships one, from the semantic map. Never decoration, never the same glyph down a column. |
| **Icons earn their keep in composites** | Card, table, alert, menu, form field, and the domain component mark every distinct kind of fact they show. A glyph per kind makes a dense block scannable. |
| **A label beside an icon holds one line** | Give the label room before letting it wrap. If it must wrap, the row aligns `flex-start` and the icon's box is the label's line-height tall, so the glyph centres on the first line and stays there. An uppercase label takes the icon one size up. |
| **Everything interactive transitions** | Hover, focus, press, and toggle all ease — named properties, `--ease-out`, under 200ms. Quick and quiet, never louder than the content. |
| **No line ends alone** | `text-wrap: balance` on every short block, `pretty` on every paragraph. Never a manual `<br>` or `&nbsp;`. |
| **Every specimen owns its label** | The label sits inside the specimen's cell, under what it names. A caption row under unequal specimens pairs the wrong label with the wrong thing. |
| **Compact by default** | Ties in spacing go to the smaller step. Loosen only on request, or when the domain needs air. |
| Only what ships | The output lists no exclusions, no rejected values, no failing pairs, no `Never` rows |
| Polish is shipped, not advised | Every rule in `polish.md` lands as code in the components and the page |
| Hierarchy is built, not decorated | Every rule in `hierarchy.md` lands in the components and the page before the polish pass |

Two rules never move, whatever the user asks: contrast that passes WCAG, and an accessible
name on every control. Everything else yields to an explicit instruction.

**Word budget:** a section may carry at most one line of prose. Everything else is a token,
a value, a swatch, a bar, or a rendered component.

**Sources stay internal.** The techniques in `references/` are the skill's own knowledge.
Never cite, link, credit, or name an external article, author, or site in anything you
generate. The output states the rule; it never says where the rule came from.

## The page

Title: `{Project name} design system`

| # | Section | Shown as |
|---|---|---|
| 1 | Logo | Mark, wordmark, lockups, clearspace box, four size/background tests |
| 2 | Colors | Primary and accent first and largest, then the swatch grid with OKLCH values + budget proportion bar + contrast matrix |
| 3 | Typography | Live specimens at real size + weight ramp |
| 4 | Spacing | Horizontal bar chart, bar width = the value |
| 5 | Radius | Real corners at real curvature + concentric nesting demo |
| 6 | Border | Real strokes at real thickness + the image outline |
| 7 | Shadow | The three layers separated, then the composed tokens at rest and on hover |
| 8 | Icons | The set at every size token, drawn, then set beside the type it pairs with |
| 9 | Components | **Tabs.** One component per tab, no scrolling between them, every icon slot filled, every state live |

No section 10.

---

## Step 1 — Harvest what already ships

```
DESIGN.md · tokens.json · tokens/ · theme.ts · globals.css · app.css
tailwind.config.* · components.json · docs/brand/ · docs/design/
```

Copy every existing value **exactly**. Convert hex to OKLCH without shifting the color —
the value is preserved, only the notation changes. Fill gaps only.
A file the user points at wins over anything found.

If nothing exists, derive from the defaults in `references/tokens.md`.

## Step 2 — Fill the token set

Pick the primary and the accent before anything else; the rest of the palette is measured
against them. Then eight groups, every one mapped to a shadcn CSS variable or a documented
prop.
→ **`references/tokens.md`**

## Step 3 — Wire the project

shadcn init, token injection, component install, font install, HugeIcons swapped in for
lucide.
→ **`references/shadcn-setup.md`**

Do this **before** writing the HTML — the page documents what is installed, not the reverse.

## Step 4 — Pick the components

Core → composite → one domain component this product alone would build. Fill each
component's icon slot from the semantic map; leave empty the slots that don't exist.
→ **`references/components.md`**

## Step 5 — Set the hierarchy

Rank the content in every component and on the page: size, weight, color level, label
demotion, button ranks, and the grayscale + squint checks.
→ **`references/hierarchy.md`**

Do this **before** the polish pass — polish refines a ranking that already reads.

## Step 6 — Apply the polish pass

Font smoothing, balanced text wrapping, tabular figures, shadow-borders, image outlines,
concentric radii, icon motion, a transition on every interactive element, focus rings.
→ **`references/polish.md`**

## Step 7 — Build the page

Section markup, the visualization recipes, the tab component.
→ **`references/html-spec.md`**

---

## Before you finish

- [ ] Existing values reused, none silently changed
- [ ] Every color is `oklch()`; zero hex outside a `@supports` fallback
- [ ] Primary and accent named before any ramp was built; every other family derived from them
- [ ] Exactly two non-neutral chosen hues; the editorial mark is a step on one of them, not a third
- [ ] Chroma verified in gamut — every token renders as authored
- [ ] Contrast measured with WCAG ratios, not inferred from L
- [ ] Every token maps to a shadcn CSS variable
- [ ] `npx shadcn@latest add ...` ran clean; components exist on disk
- [ ] Domain component is written, typed, and composed from shadcn primitives
- [ ] Every icon is HugeIcons; `lucide-react` is gone from `package.json`
- [ ] Icon sizes come from the scale, strokes from the stroke tokens
- [ ] Every icon-and-label row holds one line at its shipped width; any row that can wrap aligns `flex-start` with the icon box at `1lh`
- [ ] No uppercase or letter-spaced label sits beside `icon-xs`
- [ ] Every component with an icon slot ships one; nothing carries a decorative icon
- [ ] Every composite marks each distinct kind of fact it shows — meta lines, status cells, menu verbs
- [ ] Stripping the icons out would leave the component less clear, not equally clear
- [ ] Section 9 tabs Alert, Avatar, Card, Dialog, Pagination, Spinner, Switch, Table, and Tooltip alongside the rest
- [ ] Every interactive element transitions on hover, focus, and press, from the motion tokens
- [ ] Zero `transition: all` and zero hand-typed durations in the components
- [ ] `text-wrap: balance` on every short block, `pretty` on every paragraph, in the base layer
- [ ] No heading, title, or label anywhere ends with a one-word last line
- [ ] Every specimen on the page carries its own label, under it, in its own cell
- [ ] Density preset chosen once, stated once, applied in the components and on the page
- [ ] Every user override applied everywhere it touches; no section left on the default
- [ ] The semantic icon map exists as code and as a drawn grid on the page
- [ ] Spacing is a bar chart, not a table of numbers
- [ ] Radius shows curvature; border shows thickness; shadow shows elevation
- [ ] Surfaces use `--shadow-border` with `box-shadow` in the transition
- [ ] `hierarchy.md` checklist fully satisfied
- [ ] One primary element per view; nothing moves all three levers
- [ ] Weights are 400 and 500 only; no third text gray below `neutral-700`
- [ ] Every label, table header, and meta line ranks below the value it names
- [ ] One primary button per view; routine destructive actions are not filled
- [ ] Totals, fees, terms, and the opt-out control sit at primary or secondary level
- [ ] Grayscale and squint checks both pass on the page and in every component tab
- [ ] `polish.md` checklist fully satisfied
- [ ] Section 9 tabs switch without page scroll
- [ ] Nothing in the output is an exclusion list, a fail row, or a `Never` line
- [ ] Page uses the brand's own fonts and colors
- [ ] Real product copy in every example — never "Heading 1" or "Lorem"
- [ ] Zero sentences beginning "This works because"
- [ ] No external source named anywhere in the output
- [ ] Project builds / typechecks after the change

## Common mistakes

| Mistake | Fix |
|---|---|
| Hex or HSL in the tokens | OKLCH |
| Three non-neutral families competing | One primary, one accent; the third is a shade of one of them |
| An accent-colored button | Primary is the action; accent never is |
| Grays picked from a hue the primary does not share | Neutrals take the primary's hue at C 0.002–0.012 |
| A status color restyled to match the brand | Red, amber, green are read before they are recognized |
| Chroma cranked past the gamut | Drop C until it renders as authored |
| Contrast guessed from lightness | Measure the WCAG ratio |
| 1px solid border on every card | Three-layer shadow-border |
| Hover moves the element | Change shadow opacity only |
| Table of spacing numbers | Bar chart |
| Radius listed as `12px` | Draw the corner |
| Inner radius equals outer radius | outer = inner + padding |
| An element larger, heavier, and darker at once | Move one lever; two only on the one most important element |
| A form label set like its value | `caption` · 500 · `neutral-700` above `body` · 400 · `ink` |
| A table header styled like its cells | `eyebrow`, uppercase, `neutral-700` |
| A small uppercase line above a title (the eyebrow / kicker / overline stack) | Delete it, or move its fact to the meta line under the title; the heading is the first element in its block |
| A third text gray invented for tertiary text | Step the size down; keep `neutral-700` |
| `neutral-500` used on text | Icons only; text takes `ink` or `neutral-700` |
| Two primary buttons in one view | One. The rest step down. |
| A filled destructive button on every row | `ghost` + `error` text; fill only the irreversible confirm |
| Status color read as importance | Status says what it is; rank is size, weight, color level |
| A price or cancellation term set smallest and lightest | Primary or secondary level, always |
| Hierarchy that collapses in grayscale | Color was carrying it; fix with size and spacing |
| Prose explaining the palette | Delete it; the swatches are the explanation |
| HTML page only | The repo must build with these components |
| Components as screenshots | Install them; render the real thing |
| Section 9 as a long scroll | Tabs |
| A second icon set, or a hand-drawn SVG | HugeIcons, one style |
| Icon sized by `transform: scale()` | The `size` prop, off the scale |
| A "not in this system" list at the end | Delete it; the page shows only what ships |
| Reads like any competitor | Add the domain component |
| The same icon on every row of a list | One icon per meaning; the rows carry text |
| A decorative icon in a heading or a paragraph | Delete it |
| Two icons on one side of one control | Keep the one that carries meaning |
| A component's icon slot left empty | Fill it from the semantic map |
| A card meta line or table row left as unmarked text | One `icon-xs` per kind of fact |
| `align-items: center` on an icon row whose text wraps; the icon floats between two lines | `align-items: flex-start`, icon box `height: 1lh`, glyph centred inside it |
| An eyebrow or uppercase label beside a 14px icon; the glyph reads smaller than the letters | `icon-sm` 16 beside uppercase and letter-spaced labels; `icon-stroke-bold` when the label is 500 weight |
| A label wrapping to two lines because its cell is narrow | Widen the cell, drop a column, or shorten the copy; the label holds one line |
| A control that jumps between states | Transition the named properties at `--dur-fast` |
| `transition: all` | Name the properties |
| A duration typed as `200ms` in a component | Use the motion token |
| A heading whose last line holds one word | `text-wrap: balance` |
| `<br>` or `&nbsp;` inserted to fix a wrap | `text-wrap: balance` |
| A caption row under a flex row of unequal specimens | One cell per specimen, label inside it |
| A variant label sitting beside, above, or between specimens | Under the specimen it names |
| Comfortable spacing shipped unasked | Compact; the smaller step wins ties |
| Padding tightened until the touch target shrinks | Target stays ≥44px; only the padding moves |
| The user asked for X and the output shipped the default | The ask wins, in every file it touches |

## References

- `references/tokens.md` — the eight token groups, OKLCH recipes, shadow stack, icon scale, shadcn map
- `references/shadcn-setup.md` — framework detection, init, token injection, install list, HugeIcons swap
- `references/components.md` — core / composite / domain inventory and specs
- `references/hierarchy.md` — the three levers, label demotion, button ranks, the grayscale and squint checks
- `references/polish.md` — the detail pass applied to every component and the page
- `references/html-spec.md` — page skeleton, visualization recipes, tabs
