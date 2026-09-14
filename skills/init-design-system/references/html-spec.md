# The HTML page

`docs/design-system.html`. Standalone, no build step, no CDN. Set in the brand's own fonts
and colors — the page is a sample of the system.

Title: `{Project name} design system`

Sticky left nav, nine links. Sections in this order, nothing else:

`1 Logo · 2 Colors · 3 Typography · 4 Spacing · 5 Radius · 6 Border · 7 Shadow · 8 Icons ·
9 Components`

The page shows what is in the system. Nothing on it is an exclusion, a rejected value, a
failing pair, or a `Never` row.

Every section header is the number and the word. No subtitle, no intro sentence.

---

## Page shell

```html
<style>
  :root { /* paste the token block from globals.css, verbatim — colors, radii, shadows,
             density, icons, and the motion tokens */ }
  html { -webkit-font-smoothing: antialiased; -moz-osx-font-smoothing: grayscale; }
  body { background: var(--background); color: var(--foreground);
         font-family: var(--font-body); margin: 0; }
  h2 { font-family: var(--font-display); font-size: 30px; font-weight: 400;
       margin: 0 0 24px; }
  h1, h2, h3, h4, .lbl, figcaption, caption { text-wrap: balance; }
  p, li, .val { text-wrap: pretty; }
  img { outline: 1px solid oklch(0 0 0 / 0.10); outline-offset: -1px; }
  .wrap { display: grid; grid-template-columns: 200px 1fr; gap: 48px; max-width: 1200px;
          margin: 0 auto; padding: 48px 32px; }
  nav { position: sticky; top: 32px; align-self: start; display: grid; gap: 8px;
        font-size: 14px; }
  nav a { color: var(--muted-foreground); text-decoration: none;
          transition: color var(--dur-fast) var(--ease-out); }
  nav a:hover { color: var(--foreground); }
  section { padding-block: 24px; border-top: 1px solid var(--border); }
  section:first-of-type { border-top: 0; padding-top: 0; }
  .lbl { font-size: 11px; font-weight: 500; letter-spacing: .08em;
         text-transform: uppercase; color: var(--muted-foreground); }
  .val { font-variant-numeric: tabular-nums; font-size: 13px;
         color: var(--muted-foreground); }
  .surface { background: var(--card); border-radius: var(--radius-lg);
             box-shadow: var(--shadow-border);
             transition: box-shadow var(--dur-fast) var(--ease-out); }
  .surface:hover { box-shadow: var(--shadow-border-hover); }

  /* one specimen + its own label */
  .fig { display: grid; gap: 8px; justify-items: start; align-content: start; }
  .fig-row { display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
             gap: 24px; align-items: end; }

  /* every control on the page transitions, the way the product's do */
  .ctl { transition-property: background-color, color, box-shadow, transform, opacity;
         transition-duration: var(--dur-fast);
         transition-timing-function: var(--ease-out); }
  .ctl:active { transform: scale(0.985); transition-duration: var(--dur-press); }
  :focus-visible { outline: 2px solid var(--ring); outline-offset: 2px; }

  @media (prefers-reduced-motion: reduce) {
    *, *::before, *::after {
      transition-property: color, background-color, border-color, box-shadow, opacity;
      animation-duration: 1ms !important; animation-iteration-count: 1 !important;
    }
  }
</style>
```

Every measurement on the page uses `.val` — tabular figures so the columns line up.
Every panel on the page uses `.surface` — the page demonstrates its own shadow rule.
Every control on the page uses `.ctl` — the page transitions the way the product does, so
the reader feels the timing instead of reading a duration.
Every gap on the page comes from the shipped density preset — the page is spaced the way
the product is.
Every short block on the page carries `text-wrap: balance`, every paragraph `pretty` — the
page never orphans a word while telling the reader not to.

---

## Labelling a specimen — every section

The page is one long run of labelled specimens. One pattern for all of them.

**The label lives inside the specimen's own cell**, under the thing it names, sharing that
cell's alignment. Not in a caption row under the set, not floating beside it, never left to
be inferred from a neighbour.

```html
<div class="fig-row">
  <div class="fig">
    <svg width="14" height="14" viewBox="0 0 24 24" …></svg>
    <div class="lbl">icon-xs</div>
    <div class="val">14px · inline meta</div>
  </div>
  <div class="fig">
    <svg width="16" height="16" viewBox="0 0 24 24" …></svg>
    <div class="lbl">icon-sm</div>
    <div class="val">16px · inputs, badges</div>
  </div>
</div>
```

`align-items: end` on the row puts specimens of different heights on one baseline while
each label stays welded to its own.

| Wrong | Right |
|---|---|
| One caption row beneath a flex row of specimens | One `.fig` per specimen |
| `<svg>` then `<span class="val">16</span>` on the same line | `.val` on the line under the `<svg>` |
| Four sizes labelled `14 16 20 24` in one line | Each size labelled in its own column |
| One label on the container holding five variants | One label on each variant |
| Label centred over a left-aligned specimen | Label takes the specimen's alignment |

The single exception: when specimens stack vertically, one per row — the type ramp, the
border scale — the label may sit in a second column of that same row. The row is the cell,
so the pairing still cannot drift.

Run the check by reading only the labels, top to bottom, and pointing at what each one
names. Any hesitation is a misplaced label.

---

## 1 · Logo

Four blocks, no prose.

```html
<!-- a: mark, wordmark, lockup, side by side on the page background -->
<!-- b: clearspace — the mark inside a dashed box, padding = mark height -->
<div style="display:inline-block;padding:var(--mark-h);outline:1px dashed var(--border)">
  <svg class="mark">…</svg>
</div>

<!-- c: size test — the same mark at four sizes, real pixels, each label under its own mark -->
<div class="fig-row">
  <div class="fig"><svg width="16" height="16">…</svg><span class="val">16px</span></div>
  <div class="fig"><svg width="24" height="24">…</svg><span class="val">24px</span></div>
  <div class="fig"><svg width="48" height="48">…</svg><span class="val">48px</span></div>
  <div class="fig"><svg width="96" height="96">…</svg><span class="val">96px</span></div>
</div>

<!-- d: background test — same lockup on 4 grounds -->
<!-- light · ink · accent · a photo, carrying the inset outline -->
```

Then one table: lockup, where it is used, the rule. One row per shipped lockup.

---

## 2 · Colors

### Budget bar

One stacked bar, widths = the budget percentages.

```html
<div style="display:flex;height:40px;border-radius:var(--radius-md);overflow:hidden">
  <div style="flex:90;background:var(--muted)"></div>
  <div style="flex:5;background:var(--accent)"></div>
  <div style="flex:4;background:var(--primary)"></div>
  <div style="flex:1;background:var(--destructive)"></div>
</div>

<!-- legend, not a proportional caption row: a 1% segment cannot hold its own label -->
<div style="display:flex;flex-wrap:wrap;gap:16px;margin-top:8px">
  <span style="display:inline-flex;align-items:center;gap:8px" class="val">
    <i style="width:12px;height:12px;border-radius:2px;background:var(--muted)"></i>
    Neutrals 90%</span>
  <!-- accent 5% · primary 4% · status 1%, same shape -->
</div>
```

The label never rides on the segment. A 1% segment is 10px wide and cannot hold a word, so
the pairing is carried by a color chip in a legend instead.

### The two chosen hues — first, and largest

Before the full palette grid, the two colors the brand is: primary and accent, side by side
at a size nothing else on the page gets, each with its OKLCH value, its role, and the one
word that separates them — **action** and **highlight**. Every other swatch on the page is
smaller.

```html
<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:24px">
  <div class="fig" style="justify-items:stretch;gap:8px">
    <div style="height:160px;border-radius:var(--radius-lg);background:var(--primary);
                box-shadow:var(--shadow-border)"></div>
    <div class="lbl">Primary</div>
    <div class="val">oklch(0.420 0.062 165)</div>
    <div class="val">Action. Buttons, links, focus ring.</div>
  </div>
  <div class="fig" style="justify-items:stretch;gap:8px">
    <div style="height:160px;border-radius:var(--radius-lg);background:var(--accent);
                box-shadow:var(--shadow-border)"></div>
    <div class="lbl">Accent</div>
    <div class="val">oklch(0.520 0.058 72)</div>
    <div class="val">Highlight. Tags, badges, the editorial mark.</div>
  </div>
</div>
```

A reader who sees only this block has seen the brand. That is the test.

### Swatch grid

OKLCH value on every swatch. No hex anywhere on the page.

```html
<div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(180px,1fr));gap:16px">
  <div class="fig" style="justify-items:stretch;gap:4px">
    <div style="height:88px;border-radius:var(--radius-md);
                background:oklch(0.985 0.004 95);
                box-shadow:var(--shadow-border)"></div>
    <div class="lbl" style="margin-top:4px">neutral-50</div>
    <div class="val">oklch(0.985 0.004 95)</div>
    <div class="val">Page background</div>
  </div>
</div>
```

Swatch, token, OKLCH, role. Four lines. Nothing else.

### The ramp, drawn

Show that L is doing the work. One row per ramp, swatches in L order, L printed under each.

```html
<div style="display:flex;gap:2px">
  <div class="fig" style="flex:1;justify-items:center;gap:4px">
    <div style="height:56px;width:100%;background:oklch(0.98 0.006 165)"></div>
    <div class="val">.98</div>
  </div>
  <!-- .96 · .92 · .87 · .78 · .68 · .58 · .48 · .38 · .26, one .fig each -->
</div>
```

Repeat for neutrals, primary, and accent. Same L steps across all three rows — the
alignment is the point, and it shows the two chosen hues sitting at the same brightness as
the neutrals they will be seen against.

### Contrast matrix

Render each pair in its own colors so the ratio is visible, not asserted.

```html
<div style="background:oklch(0.985 0.004 95);color:oklch(0.242 0.004 60);
            padding:12px 16px;border-radius:var(--radius-md)">
  Reserve from May 15 <span class="val">16.6:1 · AAA</span>
</div>
```

Every pair on the page passes. A pair that fails is not a token pairing, so it is not drawn.

---

## 3 · Typography

### Ramp

One row per step. Specimen at real size, on the left; token and metrics on the right.

```html
<div style="display:grid;grid-template-columns:1fr 200px;gap:32px;align-items:baseline;
            padding-block:16px;border-bottom:1px solid var(--border)">
  <div style="font-family:var(--font-display);font-size:36px;line-height:1.05;
              letter-spacing:-.02em;text-wrap:balance">
    Apartments worth six months of your life.</div>
  <div><div class="lbl">display</div><div class="val">36 / 1.05 / 400 / -0.02em</div></div>
</div>
```

Real product copy in every specimen. Never "The quick brown fox", never "Heading 1".

### Weight ramp

The same word at every shipped weight, side by side, weight number under each.

### Figures

Two columns of the same prices, one default and one `tabular-nums`, so the alignment
difference is visible.

### Script test

The test string from `tokens.md`, rendered at every shipped family and weight.

---

## 4 · Spacing

**Bar chart, not a table.** Two visual columns: the bar, and the real gap.

```html
<style>
  .sp { display:grid; grid-template-columns:80px 1fr 120px 140px; gap:16px;
        align-items:center; padding-block:10px; }
  .sp-bar { height:14px; background:var(--primary); border-radius:2px;
            width:calc(var(--v) * 4px); }
  .sp-gap { display:flex; gap:calc(var(--v) * 1px); }
  .sp-gap i { width:14px; height:14px; background:var(--muted); border-radius:2px;
              display:block; }
</style>

<div class="sp" style="--v:4">
  <div class="lbl">space-1</div>
  <div><div class="sp-bar"></div></div>
  <div class="val">4px · p-1</div>
  <div class="sp-gap"><i></i><i></i></div>
</div>
<div class="sp" style="--v:64">
  <div class="lbl">space-16</div>
  <div><div class="sp-bar"></div></div>
  <div class="val">64px · p-16</div>
  <div class="sp-gap"><i></i><i></i></div>
</div>
```

Bar length is 4× the value — state the multiplier once, under the chart. The right-hand
column shows the gap at 1×, so the reader sees the real distance too.

Grid: one row of columns rendered as vertical stripes at each breakpoint, gutter and
margin labelled on the drawing.

### Density, drawn — required

The shipped preset only. One real card, at the padding, gap, and field spacing the product
actually uses, with the values under it. One line names the preset; the card is the proof.

```html
<div class="surface" style="padding:16px;display:grid;gap:12px;max-width:320px">
  <div style="height:120px;border-radius:12px;background:var(--muted)"></div>
  <div style="font-size:16px">Quiet two-bedroom, Tao Dan</div>
  <div class="val">Card padding 16 · media gap 12 · outer 20 = inner 12 + padding 8</div>
</div>
<div class="val">Compact · card 16 · field 12 · block 32 · section 48</div>
```

---

## 5 · Radius

**Draw the curvature.** Big enough to read.

```html
<style>
  .rad { display:grid; grid-template-columns:repeat(auto-fit,minmax(140px,1fr)); gap:24px; }
  .rad-box { height:120px; background:var(--muted); box-shadow:var(--shadow-border); }
</style>

<div class="rad">
  <div>
    <div class="rad-box" style="border-radius:var(--radius-sm)"></div>
    <div class="lbl" style="margin-top:8px">radius-sm</div>
    <div class="val">8px · tags, checkboxes</div>
  </div>
  <div>
    <div class="rad-box" style="border-radius:9999px"></div>
    <div class="lbl" style="margin-top:8px">radius-full</div>
    <div class="val">9999px · avatars, pills</div>
  </div>
</div>
```

### Concentric demo — required

Three nested cards at the shipped padding steps. Label the maths under each.

```html
<div style="border-radius:20px;padding:8px;box-shadow:var(--shadow-border)">
  <div style="border-radius:12px;height:96px;background:var(--muted)"></div>
</div>
<div class="val">outer 20 = inner 12 + padding 8</div>
```

Repeat at `16 = 12 + 4` and `12 = 8 + 4`. The arithmetic, drawn three times, is the rule.

---

## 6 · Border

**Draw the thickness.** Strokes at real width, then a box using each.

```html
<div style="display:grid;gap:20px;max-width:560px">
  <div style="display:grid;grid-template-columns:120px 1fr 180px;gap:16px;align-items:center">
    <div class="lbl">hairline</div>
    <div style="border-top:1px solid var(--border)"></div>
    <div class="val">1px · dividers, input edge</div>
  </div>
  <div style="display:grid;grid-template-columns:120px 1fr 180px;gap:16px;align-items:center">
    <div class="lbl">emphasis</div>
    <div style="border-top:2px solid var(--ring)"></div>
    <div class="val">2px · focus, active tab</div>
  </div>
  <div style="display:grid;grid-template-columns:120px 1fr 180px;gap:16px;align-items:center">
    <div class="lbl">heavy</div>
    <div style="border-top:4px solid var(--foreground)"></div>
    <div class="val">4px · quote rule</div>
  </div>
</div>
```

### Image outline — required

A light thumbnail carrying the inset outline, at `radius-lg`. Values under it.

```html
<img src="…" style="outline:1px solid oklch(0 0 0 / 0.10);outline-offset:-1px;
                    border-radius:var(--radius-lg)">
<div class="val">1px oklch(0 0 0 / 0.10) · offset -1px</div>
```

### One line, last

> Borders draw lines. Shadows draw surfaces.

---

## 7 · Shadow

### The three layers, separated

Four boxes: each layer alone, then all three composed. This is the section's main drawing.

```html
<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:32px">
  <div>
    <div style="height:100px;background:var(--card);border-radius:var(--radius-lg);
                box-shadow:0 0 0 1px oklch(0 0 0 / 0.06)"></div>
    <div class="lbl" style="margin-top:12px">1 · edge</div>
    <div class="val">0 0 0 1px / 6%</div>
  </div>
  <div>
    <div style="height:100px;background:var(--card);border-radius:var(--radius-lg);
                box-shadow:0 1px 2px -1px oklch(0 0 0 / 0.06)"></div>
    <div class="lbl" style="margin-top:12px">2 · contact</div>
    <div class="val">0 1px 2px -1px / 6%</div>
  </div>
  <div>
    <div style="height:100px;background:var(--card);border-radius:var(--radius-lg);
                box-shadow:0 2px 4px 0 oklch(0 0 0 / 0.04)"></div>
    <div class="lbl" style="margin-top:12px">3 · ambient</div>
    <div class="val">0 2px 4px 0 / 4%</div>
  </div>
  <div>
    <div style="height:100px;background:var(--card);border-radius:var(--radius-lg);
                box-shadow:var(--shadow-border)"></div>
    <div class="lbl" style="margin-top:12px">composed</div>
    <div class="val">shadow-border</div>
  </div>
</div>
```

### The tokens

`shadow-border` · `shadow-border-hover` · `shadow-md` · `shadow-lg` · `shadow-none`, each
on a real card, on the real page background. Never on white if the page is not white.

### Rest vs hover

Two identical cards, one forced to the hover token, so the opacity step is visible without
the reader hovering. Values under each.

### On four grounds

The same `shadow-border` card on light, on `--muted`, on `--accent`, and on a photo. One
row. The transparency is the point.

---

## 8 · Icons

One line first, then drawings:

> `HugeIcons · Stroke Rounded · @hugeicons/core-free-icons`

Paste the real HugeIcons path data into the page. Same icon, same 24 viewBox, same stroke
the React component renders — the page and the product draw the identical glyph.

### Size scale, drawn

The same icon at every size token, real pixels, sitting on one baseline.

```html
<div class="fig-row">
  <div class="fig">
    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor"
         stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">…</svg>
    <div class="lbl">icon-xs</div>
    <div class="val">14px</div>
  </div>
  <!-- 16 · 20 · 24 · 32, one .fig each -->
</div>
```

### Stroke, drawn

The same icon at 24px, `stroke-width` 1.5 then 2, side by side, value under each.

### Set beside type — required

Each size token next to the type step it pairs with, on one baseline. This is the section's
main drawing: the icon has to sit in the line, not on top of it.

```html
<div style="display:flex;align-items:center;gap:8px;font-size:16px">
  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor"
       stroke-width="1.5" aria-hidden="true">…</svg>
  <span>Inspected by Trang · March 14</span>
</div>
<div class="val">icon-md 20 · body 16 · gap space-2</div>
```

Gap is `space-1` at `icon-xs`, `space-2` from `icon-sm` up.

### The semantic map

Every icon the product uses, rendered. Role token and HugeIcons name under each.

```html
<div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(180px,1fr));gap:16px">
  <div class="surface" style="padding:16px">
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor"
         stroke-width="1.5">…</svg>
    <div class="lbl" style="margin-top:12px">icon-verified</div>
    <div class="val">CheckmarkBadge01Icon</div>
  </div>
</div>
```

### Usage

```html
<pre style="background:var(--muted);padding:16px;border-radius:var(--radius-md);
            font-size:13px;overflow:auto"><code>import { HugeiconsIcon } from "@hugeicons/react"
import { CheckmarkBadge01Icon } from "@hugeicons/core-free-icons"

&lt;HugeiconsIcon icon={CheckmarkBadge01Icon} size={20} strokeWidth={1.5} /&gt;</code></pre>
```

---

## 9 · Components — tabbed

One component per tab. The reader never scrolls between components.

Tabs, in this order — core, then composite, then the domain component last:

| Tier | Tabs |
|---|---|
| Core | Button · Input · Textarea · Select · Checkbox · Radio · **Switch** · Badge · **Alert** · **Avatar** · **Tooltip** · **Spinner** · Separator · Skeleton |
| Composite | **Card** · Form field · **Dialog** · Dropdown menu · Tabs · **Table** · **Pagination** · Toast · Empty state |
| Domain | The one component this product alone would build |

Trim a tab only when the product genuinely does not render that component — and then trim
it from the install list too, so the page and the repo agree.

```html
<div class="tabs">
  <div role="tablist" aria-label="Components"
       style="display:flex;flex-wrap:wrap;gap:4px;border-bottom:1px solid var(--border)">
    <button role="tab" aria-selected="true" data-panel="p-button" class="ctl">Button</button>
    <button role="tab" aria-selected="false" data-panel="p-input" class="ctl">Input</button>
    <!-- … core, then composite, then the domain component last -->
  </div>
  <div role="tabpanel" id="p-button">…</div>
  <div role="tabpanel" id="p-input" hidden>…</div>
</div>

<script>
  document.querySelectorAll('.tabs').forEach(function (root) {
    var tabs = Array.from(root.querySelectorAll('[role=tab]'));
    function show(i) {
      tabs.forEach(function (t, j) {
        t.setAttribute('aria-selected', String(i === j));
        t.tabIndex = i === j ? 0 : -1;
        root.querySelector('#' + t.dataset.panel).hidden = i !== j;
      });
      tabs[i].focus();
    }
    tabs.forEach(function (t, i) {
      t.addEventListener('click', function () { show(i); });
      t.addEventListener('keydown', function (e) {
        if (e.key === 'ArrowRight') show((i + 1) % tabs.length);
        if (e.key === 'ArrowLeft') show((i - 1 + tabs.length) % tabs.length);
      });
    });
  });
</script>
```

Tab button styling: active gets a 2px bottom border in `--ring` and `--foreground` text;
inactive gets `--muted-foreground`. Panel padding `24px 0`.

### Inside every panel

1. **Live render** — every variant, side by side, styled from the same variables, with the
   component's icon slot filled from the semantic map. Real HugeIcons path data, the same
   glyph the React component draws. Each variant sits in its own `.fig`, labelled under
   itself.
2. **State row** — default · hover · focus-visible · active · disabled · error/loading,
   each rendered in its state, not described. Where a state swaps a glyph — chevron
   rotating, spinner replacing the leading icon, tick appearing — the row shows both.
   Two kinds of specimen, both required:
   - **live** — one real control carrying `.ctl`, so hovering and pressing it plays the
     shipped transition at the shipped duration
   - **forced** — clones pinned to `:hover`, `:focus-visible`, `:active`, and `disabled`
     styling, so every state is visible at once without a pointer

   Label each specimen under itself with the state and the transitioned properties:
   `hover · box-shadow 120ms`.
3. **Variant table** — variant, background, text, edge (border or shadow token), radius,
   icon slot (role token + size, or `—`), transition (properties + duration token)
4. **Usage** — the import line and one JSX snippet with real product copy

```html
<button class="ctl" style="display:inline-flex;align-items:center;gap:8px;padding:8px 12px;
               border-radius:var(--radius-md);background:var(--primary);
               color:var(--primary-foreground);border:0;font-size:16px">
  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor"
       stroke-width="1.5" aria-hidden="true">…</svg>
  Request a viewing
</button>
<div class="val">icon-md 20 · gap space-2 · padding 8/12 compact</div>
<div class="val">bg, color, box-shadow, transform · 120ms · active scale .985</div>
```

A panel whose component has no icon slot shows none. An icon that could be deleted without
the component reading less clearly is deleted before the panel ships.

```html
<pre style="background:var(--muted);padding:16px;border-radius:var(--radius-md);
            font-size:13px;overflow:auto"><code>import { Button } from "@/components/ui/button"

&lt;Button&gt;Reserve from May 15&lt;/Button&gt;</code></pre>
```

The HTML render and the installed React component must produce the same result. If they
differ, the HTML is wrong.

---

## Checks

- [ ] Opens with no console errors, no network requests
- [ ] Tabs switch by click and by arrow keys
- [ ] Every section shows a drawing, not only a table
- [ ] Zero hex values anywhere on the page
- [ ] Shadow section separates the three layers before composing them
- [ ] Radius section includes the concentric demo
- [ ] Border section includes the image outline
- [ ] Icons section shows every size token drawn, and each one set beside its type step
- [ ] Section 4 names the shipped density once and draws a real component at it
- [ ] **Every specimen carries its own label, inside its own cell, under what it names**
- [ ] Reading the labels alone, each one points at exactly one specimen
- [ ] No caption row sits under a flex row of unequal specimens
- [ ] Section 9 tabs every component in the inventory — Alert, Avatar, Card, Dialog, Pagination, Spinner, Switch, Table, and Tooltip included
- [ ] Every panel's state row includes a live control and forced-state clones
- [ ] Hovering a control on the page plays the shipped transition at the shipped duration
- [ ] Every component panel fills its icon slot; composites mark each distinct kind of fact
- [ ] Padding, gaps, and grid gutters on the page match the shipped density preset
- [ ] Every icon on the page is real HugeIcons path data at the shipped stroke
- [ ] Nothing on the page is an exclusion, a failing pair, or a `Never` row
- [ ] Page's own panels use `--shadow-border` and transition it on hover
- [ ] `antialiased`, `text-wrap: balance` / `pretty`, and `tabular-nums` applied to the page itself
- [ ] No heading or label on the page ends with a one-word last line
- [ ] `prefers-reduced-motion` block present and honoured
- [ ] Zero sentences starting "This works because"
- [ ] No external source, author, or URL named anywhere
- [ ] Token values identical to `globals.css`
- [ ] Renders correctly at 375px wide
