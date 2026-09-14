# Polish

The details that separate a system that works from one that feels right. Every one is
cheap. Apply all of them to the installed components **and** to the HTML page.

Each rule ships as code, never as advice on the page.

Runs **after** `hierarchy.md`. Polish refines a ranking that already reads; it never
substitutes for one.

---

## Root

Set once, on the layout root. Everything downstream inherits.

```css
html {
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
```

Tailwind: `class="antialiased"` on `<body>`.

---

## Text

No line ends alone. A last line carrying a single word — an orphan — is the most common
wrap defect on a responsive page, and CSS fixes it natively. Never fix it with a manual
`<br>`, a `&nbsp;`, or a hand-set `max-width`.

| Rule | Code | Applies to |
|---|---|---|
| Short blocks break evenly | `text-wrap: balance` | Anything under ~4 lines: headings, card titles, dialog and alert titles, toast lines, empty-state lines, blockquotes, captions, and any label that can wrap to two lines |
| Long blocks never orphan | `text-wrap: pretty` | Body copy, helper text, descriptions, list items |
| Digits never jitter | `font-variant-numeric: tabular-nums` | Prices, counts, timers, timestamps, table figures |

```css
@layer base {
  h1, h2, h3, h4, h5, h6,
  blockquote, figcaption, caption,
  [data-slot="card-title"], [data-slot="dialog-title"],
  [data-slot="alert-title"], [data-slot="tooltip-content"] {
    text-wrap: balance;
  }
  p, li,
  [data-slot="card-description"], [data-slot="dialog-description"],
  [data-slot="alert-description"], [data-slot="form-description"] {
    text-wrap: pretty;
  }
}
```

`balance` is applied by the browser only up to a handful of lines and ignored past that, so
it is free on every short block. Pair the two: `balance` on the title, `pretty` on the
description directly under it. Both ship in the base layer, so no component has to
remember them.

`tabular-nums` is mandatory on anything that updates or aligns in a column — prices,
counts, timers, timestamps, table figures.

---

## Surfaces

Borders draw lines. Shadows draw surfaces.

```css
.surface {
  box-shadow: var(--shadow-border);
  transition: box-shadow var(--dur-fast) var(--ease-out);
}
.surface:hover,
.surface:focus-visible {
  box-shadow: var(--shadow-border-hover);
}
```

The hover step changes opacity only. Geometry stays put, so nothing appears to jump.

---

## Images

Every image, video, and thumbnail:

```css
img, video {
  outline: 1px solid oklch(0 0 0 / 0.10);
  outline-offset: -1px;
}
```

The negative offset draws the line inside the frame, so it survives a rounded corner and
never adds to the element's box.

---

## Density

Compact by default. Padding, gaps, and gutters come from the preset in `tokens.md` §3, and
one preset covers the whole product.

| Rule | Code |
|---|---|
| Ties go to the smaller step | `p-4` over `p-6` on a card |
| Padding shrinks, targets don't | `min-height: 44px` stays; the padding moves |
| Reading comfort is not spacing | Line height and the 45–75ch measure never tighten |

Tight is not crowded: the gap between groups still exceeds the gap inside a group, at 16/8
instead of 24/12.

---

## Corners

`outer radius = inner radius + padding`

| Outer | Padding | Inner |
|---|---|---|
| 20px | 8px | 12px |
| 16px | 4px | 12px |
| 12px | 4px | 8px |

Get this wrong and the inner element looks pinched at every corner. It is the single most
visible spacing error in a card.

---

## Icons

HugeIcons, Stroke Rounded, rendered through `HugeiconsIcon`. Size from a size token, stroke
from a stroke token.

```tsx
import { HugeiconsIcon } from "@hugeicons/react";
import { Copy01Icon, Tick02Icon } from "@hugeicons/core-free-icons";

<Button onClick={copy}>
  <HugeiconsIcon icon={copied ? Tick02Icon : Copy01Icon} size={20} strokeWidth={1.5} />
</Button>
```

Swap conditional icons with motion, not a hard cut. Cross-fade `opacity`, `scale`, and a
small `blur`, 150ms — wrap the icon, animate the wrapper, so the stroke never redraws
mid-transition.

For a stroke-to-solid state change, hand `HugeiconsIcon` both glyphs and let it swap:

```tsx
<HugeiconsIcon icon={FavouriteIcon} altIcon={FavouriteSolidIcon} showAlt={saved} />
```

### Reach for icons — then cut the ones that only decorate

Icons carry meaning faster than words and give a dense block its structure. Composite
components — card, table, alert, form field, menu, pagination, the domain component — are
where they pay: each distinct kind of fact gets its glyph, and the block becomes scannable
instead of a wall of text. Draw generously there, then cut whatever survives the strip
test below.

| Draw it | Skip it |
|---|---|
| It names a kind — a field's type, a fact's category, a status, a unit | It repeats a word already right beside it and adds nothing |
| It is the whole control — icon-only button, chevron, close, tick, spinner | The same glyph repeats down every row of one column |
| It marks a state that text alone would bury — verified, error, loading, locked | It decorates a heading or a paragraph |
| It is the one mark in an empty state | Two glyphs sit on the same side of one control |

**The cap is per meaning, not per component.** Two icons maximum on a single control. A
composite block carries one icon per distinct meaning it shows — a card meta line with
location, date, and area draws three, and is clearer for it.

Two tests, run both:

- **Strip test.** Delete every icon. Anything the component reads just as clearly without
  was decoration; leave it out.
- **Scan test.** Squint at the composite. If nothing marks where one kind of fact ends and
  the next begins, it is under-drawn — put the kind icons back.

Align icons **optically, not geometrically**. A play triangle centred by its bounding box
sits left of where the eye wants it. Correct it inside the SVG viewBox where possible;
otherwise a 1px asymmetric padding on the container.

Icon stroke weight matches the text weight beside it. An uppercase or letter-spaced label
reads larger than its size; pair it with the icon one step up (`icon-sm` beside an eyebrow),
and `icon-stroke-bold` when the label is 500 weight.

### Beside a label — one line, first-line aligned

The label stays on one line at its shipped width. Give it room first: widen the cell, drop a
column, shorten the copy. Only then let it wrap, and when it wraps the icon must not float
between the lines:

```css
.label { display: flex; align-items: flex-start; gap: var(--space-1); }
.label > svg { height: 1lh; width: 16px; flex: none; }
```

The icon's box is exactly one line tall, so the glyph centres on the first line whether the
text is one line or three. `align-items: center` only works on rows that can never wrap.

---

## Motion

| Case | Use | Why |
|---|---|---|
| Hover, focus, press, toggle | CSS `transition` | Interruptible — reverses cleanly mid-flight |
| One-shot entrance, staged reveal | `@keyframes` | Fixed timeline, runs once |

Never animate an interaction with keyframes. A user who moves the cursor away mid-animation
gets stuck watching it finish.

### Transitions — every interactive element carries one

A control that snaps between states reads as a rendering glitch. A control that eases
between them reads as a response. The transition is **felt, not watched**: under 200ms,
ease-out, never louder than the content beside it.

Durations and easings come from the motion tokens in `tokens.md` §8 — no hand-typed `ms`
in a component.

| Element | Transitions | Duration |
|---|---|---|
| Button | `background-color, color, box-shadow, transform` | `--dur-fast`, `--dur-press` on `:active` |
| Input · textarea · select trigger | `box-shadow, background-color, color` | `--dur-fast` |
| Checkbox · radio · switch track | `background-color, box-shadow` | `--dur-fast` |
| Switch knob | `transform` | `--dur-fast` |
| Card · table row · menu item · nav item | `background-color, box-shadow` | `--dur-fast` |
| Link | `color, text-decoration-color` | `--dur-fast` |
| Icon inside a control | `color, opacity, transform, filter` | `--dur-icon` |
| Disclosure chevron | `transform` (rotate 180°) | `--dur-icon` |
| Tab · active marker | `color, border-color` | `--dur-fast` |
| Tooltip · popover · dropdown | `opacity, transform` | `--dur-panel` |
| Dialog · sheet | `opacity, transform` | `--dur-dialog` |
| Accordion · collapsible | `height, opacity` | `--dur-panel` |

```css
.control {
  transition-property: background-color, color, box-shadow, transform;
  transition-duration: var(--dur-fast);
  transition-timing-function: var(--ease-out);
}
.control:active { transform: scale(0.985); transition-duration: var(--dur-press); }
```

Tailwind: `transition-[background-color,box-shadow,transform] duration-[--dur-fast] ease-[--ease-out] active:scale-[0.985]`.

Rules:

1. **Name the properties.** `transition: all` animates layout properties nobody chose and
   costs a frame every time one changes.
2. **Composite properties only** — `opacity`, `transform`, `color`, `box-shadow`,
   `background-color`. Never `width`, `height`, `top`, or `margin` on an interaction.
3. **Surfaces never move on hover.** Opacity, color, and shadow change; geometry does not.
4. **Press is the one geometry change.** `scale(0.985)` on `:active`, on controls only,
   at `--dur-press`, released the instant the pointer lifts. A card is not a control.
5. **Same duration in and out.** A slow exit makes a button feel sticky.
6. The focus ring transitions its color and offset, never its presence — it appears on the
   first frame of `:focus-visible`.
7. `@media (prefers-reduced-motion: reduce)` keeps the color and opacity transitions and
   drops every `transform`.

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    transition-property: color, background-color, border-color, box-shadow, opacity;
    animation-duration: 1ms !important;
    animation-iteration-count: 1 !important;
  }
}
```

### Staged entrance

Split the block. Stagger the parts 80–100ms apart.

```css
@keyframes enter {
  from { transform: translateY(8px); filter: blur(8px); opacity: 0; }
}
.animate-enter {
  animation: enter 800ms cubic-bezier(0.25, 0.46, 0.45, 0.94) both;
  animation-delay: calc(var(--delay, 80ms) * var(--stagger, 0));
}
```

```tsx
<div className="animate-enter" style={{ "--stagger": 1 }}><Title /></div>
<div className="animate-enter" style={{ "--stagger": 2 }}><Description /></div>
<div className="animate-enter" style={{ "--stagger": 3 }}><Actions /></div>
```

### Exits

Exits are softer than entrances. Partial movement, plus opacity and blur — never the full
distance in reverse.

```tsx
exit={{ opacity: 0, filter: "blur(4px)", x: "-70%" }}
transition={{ type: "spring", duration: 0.45, bounce: 0 }}
```

`bounce: 0`. Nothing in the system bounces.

---

## Focus

`:focus-visible`, never `:focus`. 2px `--ring`, offset 2px. Never removed, never replaced
by a color change alone.

---

## Checklist

- [ ] `antialiased` on the root
- [ ] `text-wrap: balance` on every short block — headings, card / dialog / alert titles, captions, wrapping labels
- [ ] `text-wrap: pretty` on every paragraph, helper line, and description
- [ ] Zero manual `<br>` or `&nbsp;` used to fix a wrap
- [ ] `tabular-nums` on every figure that aligns or updates
- [ ] Surfaces use `--shadow-border`, hover uses `--shadow-border-hover`, `box-shadow` is in the transition
- [ ] Every interactive element transitions on hover, focus, and press
- [ ] Transitions name their properties; zero `transition: all`
- [ ] Durations and easings come from the motion tokens; no hand-typed `ms`
- [ ] Press compresses controls to `scale(0.985)`; surfaces never move
- [ ] `prefers-reduced-motion` block drops transforms, keeps color and opacity
- [ ] Images carry the inset outline
- [ ] Nested radii satisfy outer = inner + padding
- [ ] Every icon is HugeIcons, at a size token and a stroke token
- [ ] Every icon slot filled; each composite marks every distinct kind of fact it shows
- [ ] Every icon-and-label row holds one line; rows that can wrap align `flex-start` with the icon box at `1lh`
- [ ] Uppercase and letter-spaced labels sit beside `icon-sm` or larger, never `icon-xs`
- [ ] Strip test and scan test both run: nothing decorative, nothing under-drawn
- [ ] Padding and gaps come from one density preset, compact unless it was moved
- [ ] Touch targets ≥44px at that density
- [ ] Conditional icons cross-fade
- [ ] Interactions are transitions; only staged reveals are keyframes
- [ ] Entrances stagger 80–100ms; exits are subtler than entrances
- [ ] `:focus-visible` ring on every interactive element
- [ ] Nothing bounces
