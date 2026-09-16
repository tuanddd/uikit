# The viewer route

`/uikit/design-system`, rendered by the project's own stack. One page, nine sections, built
from the app's real layout, fonts, and components.

The rule the whole page obeys: **import, never redraw.** A component is the installed one,
imported. A token value is printed from `tokens.json`; a swatch is filled from the CSS
variable. `tokens.json` is the source the CSS was derived from (`setup.md` § 2) — if the two
disagree, the CSS is wrong, and the viewer would show one value and render another. Nothing
on the page is a second definition, so nothing on the page can drift.

Route file per stack (`stacks.md` § 2):

```
React    app/uikit/design-system/page.tsx          (App Router; src/app/ when present)
         pages/uikit/design-system.tsx             (Pages Router; src/pages/ when present)
         app/routes/uikit.design-system.tsx        (Remix / React Router 7)
Svelte   src/routes/uikit/design-system/+page.svelte
Astro    src/pages/uikit/design-system.astro
```

Static output and no-router SPAs: `stacks.md` § 3–4.

Title: `{Project name} design system`.

Sticky left nav, nine links. Sections in this order, nothing else:

`1 Logo · 2 Colors · 3 Typography · 4 Spacing · 5 Radius · 6 Border · 7 Shadow · 8 Icons ·
9 Components`

The page shows what is in the system. Nothing on it is an exclusion, a rejected value, a
failing pair, or a `Never` row. Every section header is the number and the word. No
subtitle, no intro sentence.

---

## Dev-surface hygiene

Set once, checked at the end:

- The route renders through the app's own base layout (so it uses the brand's fonts and the
  global stylesheet), or a minimal layout that imports the global stylesheet.
- `<meta name="robots" content="noindex">` in the route's head.
- One comment at the top of the route file: *dev surface, not linked, gated out of
  production* — the next agent reads the file, not this reference.
- The env gate from `stacks.md` § 4 present and correct.
- `robots.txt` disallows `/uikit/`; the sitemap excludes the route; no nav links in.
- A `data-dev-surface` attribute on the page root, so a later audit can find it.

---

## Page shell

The nav and section frame are the only styles the viewer owns; everything inside a section
reads the shipped tokens. In Astro they are scoped to the page; in React/Svelte they are a
small local stylesheet beside the route. The page root element carries `data-dev-surface`
(and `noindex` in the head), so an audit can find the surface without reading the source.

```css
html { -webkit-font-smoothing: antialiased; -moz-osx-font-smoothing: grayscale; }
body { background: var(--background); color: var(--foreground); font-family: var(--font-body);
       margin: 0; }
h2 { font-family: var(--font-display); font-size: 30px; font-weight: 400; margin: 0 0 var(--space-6); }
h1, h2, h3, h4, .lbl, figcaption, caption { text-wrap: balance; }
p, li, .val { text-wrap: pretty; }

.wrap { display: grid; grid-template-columns: 200px 1fr; gap: var(--space-12);
        max-width: 1200px; margin: 0 auto; padding: var(--space-12) var(--space-8); }
nav  { position: sticky; top: var(--space-8); align-self: start; display: grid;
       gap: var(--space-2); font-size: 14px; }
nav a { color: var(--muted-foreground); text-decoration: none;
        transition: color var(--dur-fast) var(--ease-out); }
nav a:hover { color: var(--foreground); }
section { padding-block: var(--space-6); border-top: 1px solid var(--border); }
section:first-of-type { border-top: 0; padding-top: 0; }

.lbl { font-size: 11px; font-weight: 500; letter-spacing: .08em; text-transform: uppercase;
       color: var(--muted-foreground); }
.val { font-variant-numeric: tabular-nums; font-size: 13px; color: var(--muted-foreground); }
```

Every measurement on the page uses `.val` — tabular figures so the columns line up.
Every panel uses the shipped `--shadow-border`. Every gap comes from the shipped density
preset. Every short block carries `text-wrap: balance`, every paragraph `pretty`.

---

## The specimen helper

Every drawn thing goes through one local component, and it enforces the labelling rule in
its own structure so the rule cannot be forgotten: the label is a child of the same cell as
the specimen, after it.

| Stack | File | Props |
|---|---|---|
| React | `src/dev/Specimen.tsx` | `name`, `note?`, `group?`, `children` |
| Svelte | `src/lib/dev/Specimen.svelte` | `name`, `note?`, `children` |
| Astro | `src/components/dev/Specimen.astro` | `name`, `note?`, `roomy?`, `<slot />` |

```astro
---
// Astro form; React/Svelte are the same shape in their syntax.
interface Props { name: string; note?: string; roomy?: boolean }
const { name, note, roomy = false } = Astro.props;
---
<div class:list={["specimen", roomy && "specimen--roomy"]}>
  <div class="specimen__head">
    <span class="specimen__name">{name}</span>
    {note && <span class="specimen__note">{note}</span>}
  </div>
  <div class="specimen__stage"><slot /></div>
</div>
<style>
  .specimen { display: flex; flex-direction: column; gap: var(--space-2); }
  .specimen__name { font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
                    font-size: 11px; letter-spacing: .08em; text-transform: uppercase;
                    color: var(--muted-foreground); }
  .specimen__note { font-size: 13px; color: var(--muted-foreground); opacity: .75; }
  .specimen__stage { display: flex; align-items: center; flex-wrap: wrap;
                     gap: var(--space-6); padding: var(--space-8);
                     border-radius: var(--radius-lg); background: var(--secondary); }
  .specimen--roomy .specimen__stage { align-items: flex-start;
                                      padding-bottom: var(--space-16); }
</style>
```

`name` is the state or variant being shown; `note` explains it when the name alone would
not. `roomy` adds room under the stage for a component whose popover opens downward.

**The label lives inside the specimen's own cell, under the thing it names.** Never a
caption row under the set, never floating to one side, never inferred from a neighbour.

| Wrong | Right |
|---|---|
| One caption row beneath a flex row of specimens | One `Specimen` per specimen |
| A label on the container holding five variants | A label on each variant |
| Four sizes labelled `14 16 20 24` in one line | Each size in its own `Specimen` |
| Label centred over a left-aligned specimen | Label takes the specimen's alignment |

Only exception: specimens stacked vertically, one per row — the type ramp, the border scale.
There the label may sit in a second column of that row. The row is the cell, so the pairing
still cannot drift.

Run the check by reading only the labels top to bottom and pointing at what each names. Any
hesitation is a misplaced label.

---

## 1 · Logo

Render the real brand components, not redrawn SVG. If the mark exists as a component,
import it; if it exists only as an asset, use the project's image pipeline.

- Mark, wordmark, lockup, side by side on the page background.
- Clearspace — the mark inside a dashed box whose padding equals the mark height.
- Size test — the same mark at four sizes, real pixels, each in its own `Specimen`.
- Background test — the same lockup on light, `--foreground`, `--accent`, and a photo, the
  photo carrying `outline: var(--outline-image)`.

Then one table: lockup, where it is used, the rule. One row per shipped lockup.

## 2 · Colors

Values come from `tokens.json` (the same source the CSS was generated from); fills come from
the CSS variables. They cannot disagree because they are one table.

### Budget bar

One stacked bar, widths = the budget percentages, segments filled from the variables, a
legend beside it — a 1% segment cannot hold its own label.

### The two chosen hues — first, and largest

Before the full grid, primary and accent side by side at a size nothing else gets: a large
block filled `var(--primary)` / `var(--accent)`, its OKLCH value from `tokens.json`, its
role, and the one word that separates them — **action** and **highlight**. A reader who sees
only this block has seen the brand.

### Swatch grid

Swatch, token, OKLCH value, role. Four lines each. The swatch is `background:
var(--<token>)`; the value is read from `tokens.json`; the role is that token's description.

### The ramp, drawn

One row per family, swatches in L order, L printed under each. Same L steps across neutrals,
primary, and accent — the alignment is the point.

### Contrast matrix

Render each pair in its own colors (a block with the fill token and the text token as real
classes) and measure the ratio; print the measured value and the verdict. Every pair on the
page passes. A pair that fails is not a token pairing, so it is not drawn.

## 3 · Typography

The ramp is live: real text elements carrying the project's real type classes, at real size,
one row per step. Real product copy in every specimen — never "The quick brown fox", never
"Heading 1". Metrics (size / line-height / weight / tracking) come from `tokens.json`.

Then the weight ramp (the same word at every shipped weight), the figures comparison
(default vs `tabular-nums`), and the script test string at every shipped family and weight.

## 4 · Spacing

Bar chart, not a table. Two visual columns: the bar, and the real gap.

```html
<div class="sp" style="--v:4">
  <div class="lbl">space-1</div>
  <div><div class="sp-bar"></div></div>
  <div class="val">4px · p-1</div>
  <div class="sp-gap"><i></i><i></i></div>
</div>
```

Bar length is 4× the value — state the multiplier once, under the chart. The right column
shows the gap at 1× so the reader sees the real distance.

One row per spacing token, generated by iterating `tokens.json`: `--v` is that entry's
numeric value and the printed label is read from the same entry. Do not hand-type the value
or the Tailwind name per row — the loop is what keeps the chart honest.

**Density, drawn — required.** One real card from the system, at the padding, gap, and field
spacing the product actually uses, with the values under it. One line names the preset; the
card is the proof.

## 5 · Radius

Draw the curvature, big enough to read: a box per radius token, `border-radius:
var(--radius-*)`, label and value under each.

**Concentric demo — required.** Three nested cards at the shipped padding steps, the
arithmetic labelled under each (`outer 20 = inner 12 + padding 8`). The arithmetic, drawn
three times, is the rule.

## 6 · Border

Draw the thickness: strokes at real width, then a box using each. Hairline, emphasis, heavy,
each named and valued.

**Image outline — required.** A light thumbnail carrying `outline: var(--outline-image);
outline-offset: -1px` at `radius-lg`, values under it.

### One line, last

> Borders draw lines. Shadows draw surfaces.

## 7 · Shadow

### The three layers, separated

Four boxes: each layer alone (the raw `box-shadow` values from `tokens.json`), then all
three composed as `var(--shadow-border)`. This is the section's main drawing.

### The tokens

`shadow-border` · `shadow-border-hover` · `shadow-md` · `shadow-lg` · `shadow-none`, each on
a real card, on the real page background. Never on white if the page is not white.

### Rest vs hover, and four grounds

Two identical cards, one pinned to the hover token so the opacity step is visible without a
pointer. Then the same card on light, `--muted`, `--accent`, and a photo. The transparency
is the point.

## 8 · Icons

One line first, then drawings:

> `HugeIcons · {stroke style} · {package}`

Every icon renders through the project's one icon component — the same component the
product uses, so the glyph is identical by construction.

### Size scale, drawn

The same icon at every size token, real pixels, on one baseline, each in its own `Specimen`.

### Stroke, drawn

The same icon at 24px, regular then bold stroke, side by side.

### Set beside type — required

Each size token next to the type step it pairs with, on one baseline — the icon in the line,
not on top of it. Gap is `space-1` at `icon-xs`, `space-2` from `icon-sm` up.

### The semantic map

Every role in the map, rendered through the icon component, role token and registry name
under each.

### Usage

The import line and one snippet, in the stack's own syntax, with real product copy.

## 9 · Components

**The real components, imported unmodified.** This is the whole point of the live route: the
panel for Button renders the project's Button, so what the reader sees is what ships.

Group the components core → composite → domain, and give each group a heading and an anchor.
A sticky sub-nav lists the groups; the reader jumps, never scrolls through everything. Do
**not** use the product's own Tabs component to switch the gallery — it may itself be a
specimen.

| Tier | Groups to cover |
|---|---|
| Core | Button · Input · Textarea · Select · Checkbox · Radio · Switch · Badge · Alert · Avatar · Tooltip · Spinner · Separator · Skeleton |
| Composite | Card · Form field · Dialog · Dropdown menu · Tabs · Table · Pagination · Toast · Empty state |
| Domain | The one component this product alone would build |

Trim a group only when the product genuinely does not render that component — and then trim
it from the authored set too, so the viewer and the repo agree.

### Inside every group

1. **Live render** — every variant, each in its own `Specimen`, every icon slot filled from
   the semantic map. Real components, real props.
2. **State row** — default · disabled · loading · error/selected/open, whatever the
   component's own API exposes, each rendered in its state, not described. Where the
   component's API reaches a state (`disabled`, `loading`, `error`, `open`), pass the prop.
   Pointer states (hover, focus, press) are **live**: the reader hovers the real control and
   feels the shipped transition, because the control carries the real transition. Do not
   clone the component to fake a pseudo-state.
3. **Variant table** — variant, background token, text token, edge token, radius token,
   icon slot (role + size, or `—`), transitioned properties.
4. **Usage** — the import line and one snippet in the stack's syntax, with real product copy.

A group whose component has no icon slot shows none. An icon that could be deleted without
the component reading less clearly is deleted before the group ships.

The component's own state is the state shown. If the viewer needs a special prop to force a
state, that prop belongs in the component's real API, not in a viewer-only wrapper.

---

## Checks

- [ ] Route resolves at `/uikit/design-system` and renders without console errors
- [ ] Every component in section 9 is imported from the project — none is redrawn
- [ ] No token value is typed in the viewer; fills use `var(--…)`, values come from `tokens.json`
- [ ] `tokens.json` and the CSS `:root` agree; the CSS was derived from the JSON
- [ ] The page renders through the app's layout, in the brand's fonts and colors
- [ ] `noindex` meta present, `data-dev-surface` on the root, route unlinked, `robots.txt` disallows it, sitemap excludes it
- [ ] The env gate 404s (or the page is not built) in production, and the route resolves in dev and preview
- [ ] On a static host, the hiding path from `stacks.md` § 4 was applied, or `[UNAVAILABLE]` was recorded
- [ ] Every section shows a drawing, not only a table
- [ ] Zero hex values anywhere on the page
- [ ] Shadow section separates the three layers before composing them
- [ ] Radius section includes the concentric demo
- [ ] Border section includes the image outline
- [ ] Icons section shows every size token drawn, and each one set beside its type step
- [ ] Section 4 names the shipped density once and draws a real component at it
- [ ] **Every specimen carries its own label, inside its own cell, under what it names**
- [ ] Reading the labels alone, each one points at exactly one specimen
- [ ] Section 9 covers Alert, Avatar, Card, Dialog, Pagination, Spinner, Switch, Table, and Tooltip
- [ ] Every group's state row reaches the component's own states; pointer states are live
- [ ] Hovering a control plays the shipped transition at the shipped duration
- [ ] Every component group fills its icon slots; composites mark each distinct kind of fact
- [ ] Padding, gaps, and grid gutters on the page match the shipped density preset
- [ ] Every icon renders through the project's single icon component
- [ ] Nothing on the page is an exclusion, a failing pair, or a `Never` row
- [ ] The page's own panels use `--shadow-border` and transition it on hover
- [ ] `antialiased`, `text-wrap: balance` / `pretty`, and `tabular-nums` applied to the page
- [ ] No heading or label on the page ends with a one-word last line
- [ ] `prefers-reduced-motion` block present and honoured
- [ ] Zero sentences starting "This works because"
- [ ] No external source, author, or URL named anywhere
- [ ] Renders correctly at 375px wide
