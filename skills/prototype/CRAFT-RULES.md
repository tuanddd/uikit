# Craft rules

Layout constraints every screen in a flow file is built against and checked against in Phase 5. Each one
came from a defect that survived a full build, so none is optional. They are written as the
constraint, then the CSS shape that satisfies it, then the check that catches a breach.

The theme under all of them: **repeated things are one object.** Siblings share an anatomy,
a height contract, and an edge. Anything that lets one sibling drift from the next, by a
line, a pixel, or an extra element, breaks the row.

---

## 1. Siblings in a row share one anatomy

Every column, card, or cell that sits beside another has the same slots in the same order,
and nothing extra. An element that only one sibling needs is either given to every sibling
(as a reserved slot) or moved out of the row entirely, above or below it.

```
wrong:  [card] [card + "join list" row] [card]      → the middle column runs long
right:  [card] [card] [card]  +  a full-width row underneath for the extra element
right:  every card carries the slot; two of them render it empty at its reserved height
```

**CSS shape:** the row is `display: grid` with the siblings as direct children; per-sibling
extras live inside the sibling's own slot list, never appended after it in the same column.

**Check:** the bottom edges of siblings in a row sit on one line when their content is
comparable; the row's tallest and shortest sibling differ only by wrapped body text, never
by an element the others lack.

## 2. Content under an icon-led label hangs from the label's text edge

Anything that sits below a label that starts with an icon, avatar, bullet, or number is
indented by the leading element's width plus the gap, so its left edge lines up with the
label's first letter, not with the icon. This is a hanging indent and it applies to every
level of the block: value under label, sub-line under value, quote under name.

```css
/* the block is a two-column grid: leading element | everything else */
.labelled {
  display: grid;
  grid-template-columns: 16px 1fr;
  column-gap: 6px;
  align-items: start;
}
.labelled > svg {
  grid-row: 1;
  height: 1lh;
} /* first-line aligned, rule 3 */
.labelled > .label {
  grid-column: 2;
}
.labelled > .value,
.labelled > .sub {
  grid-column: 2;
} /* hang from the text edge */
```

The same shape with `grid-template-columns: 40px 1fr` covers an avatar beside a title with a
date line under the title. Padding-left on the content with a hard-coded number is the wrong
tool: it drifts the moment the icon size or the gap changes.

**Check:** draw a vertical line down the label's first letter; every line of content in the
block starts on it. The icon sits alone to the left of that line.

## 3. A leading element aligns to the first line of the text beside it

Icon, avatar, checkbox, bullet, step number: whatever leads a text block sits centred on the
text's first line and stays there when the text wraps. Never `align-items: center` on a
container whose text can wrap; the leading element then floats between lines two and three.

```css
.row {
  display: flex;
  align-items: flex-start;
  gap: 6px;
}
.row > .lead {
  height: 1lh;
  display: inline-flex;
  align-items: center;
  flex: none;
}
```

For an avatar taller than one line, the avatar's top aligns with the text block's top and the
title's line-height absorbs the difference; the date or role line under the title hangs from
the title's text edge (rule 2), not from under the avatar.

**Check:** wrap the title to three lines in the browser. The leading element has not moved.

## 4. Cells side by side reserve the same lines for the same slot

In a grid of key/value cells (readings, stats, a spec table), each slot reserves as many
lines as the tallest sibling needs for that slot, so line N of one cell sits at the same y as
line N of its neighbour. The reservation follows the siblings, never a fixed count: if one
cell carries a sub-line, every cell reserves it; if none does, none does. A slot that is
empty in one cell still reserves its height; the empty line is invisible, not absent.

```
wrong:  CHECKS            INTERNET            → "142 Mbps" sits lower than "45 of 47"
        45 of 47          142 Mbps              because the sub-line in the first cell
        2 flagged                               pushed nothing in the second
right:  CHECKS            INTERNET
        45 of 47          142 Mbps
        2 flagged         (reserved, empty)
```

```css
.cell {
  display: grid;
  grid-template-rows: 1lh auto;
} /* label · value */
.grid--has-sub .cell {
  grid-template-rows: 1lh auto 1lh;
} /* + sub, only when a sibling uses it */
.cell > .sub:empty {
  visibility: hidden;
} /* still takes its row */
```

The same rule reaches across cards in a row: every card's title, facts and price slots
reserve the lines the tallest card in the row needs, so the tag rows and the footers of
neighbouring cards sit on one line. When a column carries text above its card (a note, a
sample label), every column in the row carries that slot at the same reserved height, or
none does (rule 1).

Labels in such a grid hold one line (widen the cell or shorten the copy before wrapping);
if a label must wrap, every label slot in the grid reserves two lines.

**Check:** lay a ruler across the grid at each slot's top edge; it touches the same slot in
every cell. Compare the cell with the most lines to the one with the fewest.

## 5. Media boxes keep one aspect ratio; nothing inside may grow them

A photo, a placeholder, a map, a cover: the box's height comes from its width and its aspect
ratio, and from nothing else. Overlays (badges, counters, captions, the typographic fallback)
are absolutely positioned inside it and clamp or truncate rather than push. Two media boxes
in one row or rail are always the same height.

```css
.media {
  position: relative;
  aspect-ratio: 4 / 3;
  overflow: hidden;
}
.media > * {
  position: absolute;
} /* badges, caption, fallback text */
.media > .cap {
  left: 12px;
  right: 12px;
  bottom: 12px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
```

A flex or grid media box whose caption sits in normal flow will grow past its ratio the
moment the caption wraps, and the card below it shifts by a line. That is the defect.

**Check:** in a rail or grid of cards, the top edges of every card's title sit on one line.

## 6. A heading stands alone; nothing small sits above it

No label, kicker, category, section number, or status line sits above a heading in a
smaller size. The "eyebrow" stack (11px uppercase line, then the serif title, then the
lede) is the pattern this rule bans: it reads as a template, it spends the reader's first
glance on the least important line, and it lets the heading be vague because the label
above it is doing the naming. The heading is the first element in its block and it names
the section on its own.

What the small line carried goes to one of three places, decided per instance:

```
redundant with the title or lede    → delete it
a fact: city, date, status, count   → the meta line under the heading, or the lede
the plainer noun the title needed   → it becomes the heading; the evocative line opens the lede

wrong:  WHAT LANDING COSTS            right:  What landing costs
        The all-in, up front                  The all-in, up front: everything you pay to
        Everything you pay to move in…        move in, added up. Not a deposit shown alone…
```

The `eyebrow` token survives as a label beside or above a *value*: a table header, a form
label, a key/value cell, a timeline stamp beside its step, a badge. It never sits above a
title of any level, in a hero, a section, a card, or a form.

**CSS shape:** a section head is `h2 + p.lede` (or `h1 + p.meta + p.lede` in a hero), and the
heading is the first element child of its block. There is no `.eyebrow`, `.kicker`, or
`.overline` class in the kit; a small-caps label class exists only for labels.

**Check:** for every `h1`, `h2`, `h3` on the screen, the previous sibling is nothing, a
divider, or the previous section's last element. A small-text element immediately before a
heading is a breach. `grep -B1 '<h[1-3]'` over the markup finds them in one pass.

## 7. A horizontal group wraps before it shrinks a child below its content

In a row of controls, cells or buttons laid side by side, no child is ever narrower than
its own content: a label holds one line, a button holds one line, a value stays unbroken.
When the row cannot hold every child at that width, the last child moves to the next line.
Nothing shrinks, nothing clips, nothing pushes past the container's edge.

```
wrong:  [Tuesday 3 | [Any | [Any  | [Show homes ready▸   → controls squeezed to one word
         November  |  city]  size]                          per line and the button still
         2026]                                              overflows the container
right:  [Tuesday 3 November 2026] [Any city] [Any size]
        [Show homes ready by then]                        → the widest child took its own line
```

**CSS shape:** a wrapping flex row with a basis, or an auto-fit grid. Never a grid row of
`1fr auto auto` for a container whose width you do not control: `auto` tracks shrink to
min-content and the `1fr` track absorbs nothing once the minimums exceed the container.

```css
.controls { display: flex; flex-wrap: wrap; gap: 12px; }
.controls > .field { flex: 1 1 160px; min-width: max-content; }
.controls > .btn   { flex: 0 0 auto; }                 /* a button never shrinks */

/* or */
.controls { display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: 12px; }
.controls > .full { grid-column: 1 / -1; }             /* the question, the primary button */
```

**Check:** narrow the container until it is one pixel too small for the children side by
side. The last child has dropped to a new line, no control's text has wrapped inside it, and
`el.scrollWidth <= el.clientWidth` holds for the row and for the container around it.

## 8. A value holds one line; only prose absorbs the squeeze

A date, a time, an amount, a measurement with its unit, a count, a reference number, a
status, and one person's name are single values: each renders on one line at every width.
When a table, a meta line, or a row of text runs short of width, the element that carries
prose (a note, the last action, an address, a description) narrows and wraps. A value never
breaks inside itself to make room, and the text never shrinks in a way the layout did not
ask for. Rule 7 keeps a control from shrinking below its content; this rule does the same for
text inside a cell, a column, or a line.

```
wrong:  SIGNED BY     DATE    LAST ACTION
        Nguyễn Minh   26      Han signed the lease on 26 Oct
        Anh, Trang    Oct
                      2026
right:  SIGNED BY          DATE          LAST ACTION
        Nguyễn Minh Anh,   26 Oct 2026   Han signed the lease
        Trang                            on 26 Oct
```

A list of names may wrap between names, never inside one. The defect above is the browser
doing what it was told: auto table layout hands the prose column its full width first and
squeezes the rest to min-content, and the min-content of "26 Oct 2026" is "2026". Nothing in
plain markup says the date is one unit, so it breaks at every space the moment a table, an
`auto` grid track, or a `flex: 1 1 0` child is tight. Mark values in markup (`<time>` for
dates, `<data>` or `.value` for amounts, counts and measurements) so the CSS and the check
both find them.

```css
th, time, data, .value { white-space: nowrap; }     /* a value is one unit */
td.prose { width: 100%; }                            /* the one table column that wraps */
.meta > .value { flex: none; }
.meta > .prose { flex: 1 1 auto; min-width: 0; }
.table-wrap { overflow-x: auto; }                    /* only when the values alone overflow */
```

In running text a date or amount may move to the next line as a whole, never split: join
its parts with `&nbsp;` in the data layer (`26&nbsp;Oct&nbsp;2026`, `96&nbsp;Mbps`), so every
surface that renders it inherits the rule. When the values of a table cannot sit side by side
even with the prose column at its narrowest (phone width, many columns), the table becomes a
list of stacked rows with each value beside its header label (rule 4), or scrolls inside its
own wrapper. It never re-wraps the values.

**Check:** narrow the viewport until the widest table or meta line is under pressure, then
run this in the console. It lists every value that broke across lines and must return `[]`.

```js
[...document.querySelectorAll("th, time, data, .value")].filter((el) => {
  const r = document.createRange();
  r.selectNodeContents(el);
  return new Set([...r.getClientRects()].map((b) => Math.round(b.top))).size > 1;
});
```

---

## The check, run in Phase 5

Screenshot one row of siblings, one icon-led block with a sub-line, one avatar-and-title,
one key/value grid, one card rail, every section head, one row of controls at its narrowest,
and every table and meta line that carries dates or amounts, at phone width. Each of the
eight rules has a one-line check above; run all eight on those screenshots before reporting.
A breach is reported as a defect, never rounded away as "close enough at this width."
