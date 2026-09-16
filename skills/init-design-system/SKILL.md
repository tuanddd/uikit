---
name: init-design-system
description: >-
  Build a project's design system as a live route at /uikit/design-system plus a working component setup in the project's own stack — OKLCH colors, typography, spacing, radius, borders, layered shadows, logo, and components authored natively (React/shadcn, Astro, or Svelte/Bits UI). Use when the user asks for a "design system", "brand design system", "design tokens", "style guide", or "brand guidelines". Reuses tokens already in the repo instead of inventing new ones. The viewer imports the real components, so it cannot drift. Output is code-ready, not a mood board.
---

# Brand design system

Three deliverables. The first two are always required.

1. **A live route** — `/uikit/design-system`, built in the project's own stack, showing the
   nine sections. Its Components section imports the project's real components; its token
   values are printed from `tokens.json`, the one authored source the CSS is derived from.
   Nothing is redrawn.
2. **The project itself**, with the tokens wired into its styling entry and the component
   set authored natively, so the next agent builds with the system rather than around it.
3. **`docs/design-system.html`** — fallback only. Produce it solely when the project cannot
   host a route (no framework or bundler). Say in one line which path you took.

The route is a dev surface: hidden in production, unlinked, `noindex`, disallowed in
`robots.txt`, excluded from the sitemap.

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

An override is applied **everywhere it touches** — tokens, components, and the viewer — or
it is not applied. Half a system on the default and half on the override is the one outcome
worse than either. The viewer still shows only what ships; it never records what was
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
| **The stack's own components are the base** | Every specimen in the viewer is a real component, imported. React uses shadcn/Radix, Svelte uses Bits UI, Astro uses native components. |
| **The viewer cannot drift** | The Components section imports the real components; token values print from `tokens.json` and fills read the CSS derived from it. Nothing is a second copy. |
| **The viewer is a dev surface** | Hidden in production by env, unlinked, `noindex`, robots-disallowed, off the sitemap |
| **HugeIcons is the registry** | Every icon from HugeIcons, one style, sizes off the scale. No second set, no one-off SVG except the logo mark. |
| **Icons are structural** | Every component with an icon slot ships one, from the semantic map. Never decoration, never the same glyph down a column. |
| **Icons earn their keep in composites** | Card, table, alert, menu, form field, and the domain component mark every distinct kind of fact they show. A glyph per kind makes a dense block scannable. |
| **A label beside an icon holds one line** | Give the label room before letting it wrap. If it must wrap, the row aligns `flex-start` and the icon's box is the label's line-height tall, so the glyph centres on the first line and stays there. An uppercase label takes the icon one size up. |
| **Everything interactive transitions** | Hover, focus, press, and toggle all ease — named properties, `--ease-out`, under 200ms. Quick and quiet, never louder than the content. |
| **No line ends alone** | `text-wrap: balance` on every short block, `pretty` on every paragraph. Never a manual `<br>` or `&nbsp;`. |
| **Every specimen owns its label** | The label sits inside the specimen's cell, under what it names. A caption row under unequal specimens pairs the wrong label with the wrong thing. |
| **Compact by default** | Ties in spacing go to the smaller step. Loosen only on request, or when the domain needs air. |
| Only what ships | The output lists no exclusions, no rejected values, no failing pairs, no `Never` rows |
| Polish is shipped, not advised | Every rule in `polish.md` lands as code in the components and the viewer |
| Hierarchy is built, not decorated | Every rule in `hierarchy.md` lands in the components and the viewer before the polish pass |

Two rules never move, whatever the user asks: contrast that passes WCAG, and an accessible
name on every control. Everything else yields to an explicit instruction.

**Word budget:** a section may carry at most one line of prose. Everything else is a token,
a value, a swatch, a bar, or a rendered component.

**Sources stay internal.** The techniques in `references/` are the skill's own knowledge.
Never cite, link, credit, or name an external article, author, or site in anything you
generate. The output states the rule; it never says where the rule came from.

## The viewer

Title: `{Project name} design system`. Route: `/uikit/design-system`.

| # | Section | Shown as |
|---|---|---|
| 1 | Logo | Mark, wordmark, lockups, clearspace box, four size/background tests |
| 2 | Colors | Primary and accent first and largest, then the swatch grid with OKLCH values + budget proportion bar + contrast matrix |
| 3 | Typography | Live specimens at real size + weight ramp |
| 4 | Spacing | Horizontal bar chart, bar width = the value |
| 5 | Radius | Real corners at real curvature + concentric nesting demo |
| 6 | Border | Real strokes at real thickness + the image outline |
| 7 | Shadow | The three layers separated, then the composed tokens at rest and on hover |
| 8 | Icons | The set at every size token, drawn by the real icon component, then set beside the type it pairs with |
| 9 | Components | **The real components, one anchored group per tier**, no scrolling between them, every icon slot filled, every state live |

No section 10.

Section 9 changes from the fallback page: the groups are anchored under a sticky sub-nav,
not tabs, because one of the specimens may itself be the product's Tabs component and the
gallery must not switch with the thing it demonstrates.

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
against them. Then eight groups, every one mapped to a CSS variable the components read.
Author `tokens.json` first — it is the single source — and derive the CSS `:root` from it.
→ **`references/tokens.md`**

## Step 3 — Detect the stack and wire the project

Read `package.json` and the file layout. Pick the stack's route file, component directory,
primitive layer, styling entry, icon renderer, and env signal.
→ **`references/stacks.md`** · **`references/setup.md`**

Inject the tokens, install or author the primitives, install the fonts, and put HugeIcons in
as the only icon registry. Do this **before** building the viewer — the viewer renders what
is installed, not the reverse.

## Step 4 — Author the components

Core → composite → one domain component this product alone would build. Each one in the
stack's own idiom, reusing any component the project already ships instead of duplicating
it. Fill each component's icon slot from the semantic map; leave empty the slots that don't
exist.
→ **`references/components.md`** · **`references/setup.md`**

## Step 5 — Set the hierarchy

Rank the content in every component and in the viewer: size, weight, color level, label
demotion, button ranks, and the grayscale + squint checks.
→ **`references/hierarchy.md`**

Do this **before** the polish pass — polish refines a ranking that already reads.

## Step 6 — Apply the polish pass

Font smoothing, balanced text wrapping, tabular figures, shadow-borders, image outlines,
concentric radii, icon motion, a transition on every interactive element, focus rings.
→ **`references/polish.md`**

## Step 7 — Build the viewer route

The route file, the specimen helper, the nine sections, and the gating.
→ **`references/viewer-spec.md`**

Only if the project cannot host a route: build the fallback page instead.
→ **`references/html-spec.md`**

## Step 8 — Gate the route

Hide it outside local and preview: env detection, `noindex`, `robots.txt` disallow, sitemap
exclusion, no inbound link. The exact signal per stack is in `references/stacks.md`; the
checklist is at the end of `references/viewer-spec.md`.

---

## Before you finish

- [ ] A route exists at `/uikit/design-system` in the project's own routing idiom, or the
      fallback page was produced and the reason stated in one line
- [ ] Components section imports the project's real components — none is redrawn
- [ ] Token sections print from `tokens.json`; fills use `var(--…)`; the CSS `:root` was
      derived from `tokens.json` and the two agree
- [ ] The viewer is hidden in production, unlinked, `noindex`, robots-disallowed, and off
      the sitemap
- [ ] Existing values reused, none silently changed
- [ ] Every color is `oklch()`; zero hex outside a `@supports` fallback
- [ ] Primary and accent named before any ramp was built; every other family derived from them
- [ ] Exactly two non-neutral chosen hues; the editorial mark is a step on one of them, not a third
- [ ] Chroma verified in gamut — every token renders as authored
- [ ] Contrast measured with WCAG ratios, not inferred from L
- [ ] Every token maps to a CSS variable the components consume
- [ ] The primitive layer is installed / authored and the components exist on disk
- [ ] Domain component is written, typed, and composed from the stack's primitives
- [ ] Every icon is HugeIcons through the stack's single renderer; no second set, no `lucide`
- [ ] Icon sizes come from the scale, strokes from the stroke tokens
- [ ] Every icon-and-label row holds one line at its shipped width; any row that can wrap aligns `flex-start` with the icon box at `1lh`
- [ ] No uppercase or letter-spaced label sits beside `icon-xs`
- [ ] Every component with an icon slot ships one; nothing carries a decorative icon
- [ ] Every composite marks each distinct kind of fact it shows — meta lines, status cells, menu verbs
- [ ] Stripping the icons out would leave the component less clear, not equally clear
- [ ] Section 9's groups cover Alert, Avatar, Card, Dialog, Pagination, Spinner, Switch, Table, and Tooltip alongside the rest
- [ ] Every interactive element transitions on hover, focus, and press, from the motion tokens
- [ ] Zero `transition: all` and zero hand-typed durations in the components
- [ ] `text-wrap: balance` on every short block, `pretty` on every paragraph, in the base layer
- [ ] No heading, title, or label anywhere ends with a one-word last line
- [ ] Every specimen in the viewer carries its own label, under it, in its own cell
- [ ] Density preset chosen once, stated once, applied in the components and the viewer
- [ ] Every user override applied everywhere it touches; no section left on the default
- [ ] The semantic icon map exists as code and as a drawn grid in the viewer
- [ ] Spacing is a bar chart, not a table of numbers
- [ ] Radius shows curvature; border shows thickness; shadow shows elevation
- [ ] Surfaces use `--shadow-border` with `box-shadow` in the transition
- [ ] `hierarchy.md` checklist fully satisfied
- [ ] One primary element per view; nothing moves all three levers
- [ ] Weights are 400 and 500 only; no third text gray below `neutral-700`
- [ ] Every label, table header, and meta line ranks below the value it names
- [ ] One primary button per view; routine destructive actions are not filled
- [ ] Totals, fees, terms, and the opt-out control sit at primary or secondary level
- [ ] Grayscale and squint checks both pass on the viewer and in every component group
- [ ] `polish.md` checklist fully satisfied
- [ ] Section 9's groups are reachable by anchor without a full-page scroll between them
- [ ] Nothing in the output is an exclusion list, a fail row, or a `Never` line
- [ ] The viewer uses the brand's own fonts and colors
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
| A component redrawn in the viewer instead of imported | Import the real component |
| A token value retyped in the viewer | Read the CSS variable |
| A viewer that ships to production | Env-gate it, `noindex` it, disallow it, keep it off the sitemap |
| A gallery that scrolls forever | A sticky sub-nav with anchors per group |
| Components as screenshots | Render the real thing |
| A second icon set, or a hand-drawn SVG | HugeIcons, one style |
| Icon sized by `transform: scale()` | The `size` prop, off the scale |
| A "not in this system" list at the end | Delete it; the viewer shows only what ships |
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

- `references/tokens.md` — the eight token groups, OKLCH recipes, shadow stack, icon scale, CSS variable map
- `references/stacks.md` — stack detection and the per-stack route, component, primitive, styling, icon, and env idioms
- `references/setup.md` — wiring per stack: token injection, primitive install, native component authoring, fonts, icons, verify
- `references/viewer-spec.md` — the live route: page shell, specimen helper, the nine sections, production gating
- `references/components.md` — core / composite / domain inventory and specs
- `references/hierarchy.md` — the three levers, label demotion, button ranks, the grayscale and squint checks
- `references/polish.md` — the detail pass applied to every component and the viewer
- `references/html-spec.md` — fallback page skeleton, visualization recipes, when a route cannot exist
