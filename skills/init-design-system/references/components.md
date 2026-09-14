# Components

Three tiers. Section 9 tabs them: core first, composite second, domain last.

Every tab carries the same four blocks, in this order:

1. **Live render** — every variant, side by side, every icon slot filled
2. **State row** — default · hover · focus-visible · active · disabled · error/loading,
   rendered, with the transition live on the interactive ones
3. **Variant table** — variant, background, text, edge (border or shadow token), radius,
   icon slot, transitioned properties
4. **Usage** — the import line and one JSX snippet with real product copy

No paragraph anywhere in a tab. Every component ships the `hierarchy.md` ranking and then
the `polish.md` pass, at the density preset from `tokens.md` §3 — compact unless the user
or the domain moved it. Inside every component: one primary element, labels below the
values they name, one primary button.

### Every specimen is labelled under itself

The label that names a variant, a state, or a size sits **directly beneath the specimen it
names**, in the same grid cell, sharing its left edge. Never in a row above the set, never
floating to one side, never left to be inferred from the neighbouring cell.

The failure is silent and constant: a row of five variants with five labels underneath, and
because the specimens are different widths, label three sits under specimen four. Wrap each
specimen and its label in one cell and the pairing cannot drift.

| Wrong | Right |
|---|---|
| One caption row under a flex row of specimens | One cell per specimen, label inside the cell |
| Label beside a specimen in a horizontal row of specimens | Label under it, sharing the cell's alignment |
| Sizes labelled `14 16 20 24` in a single line under four icons | Each size labelled in its own column |
| Label on the container that holds several variants | Label on each variant |

One exception: when specimens stack vertically, one per row — the type ramp, the border
scale — the label may sit in a second column of that same row. The pairing is still
unambiguous because the row is the cell.

Markup in `html-spec.md` § Labelling a specimen. Every drawn thing on the page uses it —
swatches, bars, corners, strokes, shadows, icons, and every component variant and state.

---

## Icons in components

Icons are part of the component, not decoration laid over it. Each component below has an
**icon slot**. Fill the slots that exist; leave alone the ones that don't.

The composite and domain components are where icons earn the most: they carry several
kinds of fact at once, and a glyph per kind turns a paragraph of text into something
scannable. Draw them there generously, and cut only what fails the strip test.

### The slots — fill these

| Slot | Icon | Size |
|---|---|---|
| Button, leading | The verb of the action | `icon-md` |
| Button, trailing | Disclosure or direction only — chevron, external link | `icon-md` |
| Icon-only button | The action, plus `aria-label` and a ≥44px target | `icon-md` |
| Input, leading | The field's kind — search, mail, date, currency | `icon-sm` |
| Input, trailing | The field's control — clear, reveal, calendar, chevron | `icon-sm` |
| Select · dropdown · accordion | The disclosure chevron, rotating 180° on open | `icon-sm` |
| Checkbox · radio | The tick, the dash, the dot | `icon-xs` |
| Switch knob | The tick, appearing as the knob travels to on | `icon-xs` |
| Badge · tag | Status glyph, on status badges only | `icon-xs` |
| Alert | The variant's status mark, leading, one per variant | `icon-md` |
| Toast · inline error | One status mark: success, error, warning, info | `icon-md` |
| Tooltip trigger | The glyph the tooltip explains — info, help, or the control itself | `icon-sm` |
| Avatar | Presence or verified badge, overlaid bottom right | `icon-xs` |
| Spinner | The one loading glyph, product-wide, rotating | Matches its slot |
| Empty state | One mark, the largest icon in the product | `icon-xl` |
| Card meta line | The kind of each fact — location, date, area, price | `icon-xs` |
| Card footer action | The action's verb | `icon-sm` |
| Table header | Sort state on every sortable column; direction on the sorted one | `icon-xs` |
| Table row | Status glyph in a status column · row actions in the last cell | `icon-xs` |
| Pagination | Previous and next arrows · the ellipsis for the skipped range | `icon-sm` |
| Dialog · sheet | Close, top right | `icon-md` |
| Menu item | The item's verb, leading — including the destructive item | `icon-sm` |
| Nav · sidebar item | The section | `icon-md` |
| Breadcrumb | The separator | `icon-xs` |
| Domain component | The verification mark · the kind of each data cell | `icon-md` · `icon-xs` |

### Leave these empty

| Case | Instead |
|---|---|
| The same glyph repeating down every row of one column | Text alone — a repeated icon stops meaning anything |
| The one primary action in a form or dialog | Text alone. One primary button, no ornament. |
| Inside body copy or a heading | Text alone |
| A second icon on the same side of one control | Keep the one that carries meaning |
| A glyph that needs a caption to be read | The word |
| Separator, skeleton, textarea, the inside of a tooltip bubble | Nothing — these have no slot |

### Rules

1. One icon per meaning, product-wide. The semantic map in `tokens.md` §7 is the source.
2. **Two icons maximum on a single control.** A composite block — card, table row, alert,
   form field, the domain component — carries one icon per *distinct* meaning it shows. A
   meta line of location, date, and area draws three, and reads faster for it.
3. Size pairs with the text beside it; stroke matches that text's weight. An uppercase or
   letter-spaced label takes the icon one size up (`icon-sm` beside an eyebrow).
3a. **The label holds one line.** Widen the cell, drop a column, or shorten the copy before
   letting it wrap. A row that can still wrap aligns `flex-start` with the icon box at
   `height: 1lh`, so the glyph centres on the first line and stays there. Never
   `align-items: center` on a row whose text can wrap.
4. Gap is `space-1` at `icon-xs`, `space-2` from `icon-sm` up.
5. `currentColor` inside text, buttons, and links. `--muted-foreground` standalone.
6. Beside a label: `aria-hidden="true"`. Alone: `aria-label`.
7. A state change swaps the glyph, never the color alone. Cross-fade at `--dur-icon`.
8. Icons transition with the control they sit in — `color`, `opacity`, `transform` — never
   independently, and never on a delay.
9. **Two tests, both run:** strip every icon out — anything that reads just as clearly was
   decoration. Then squint at each composite — if nothing marks where one kind of fact ends
   and the next begins, it is under-drawn.

---

## Tier 1 — Core

shadcn primitives, unmodified except by tokens.

| Component | Must show | Icon slot |
|---|---|---|
| Button | primary · secondary · outline · ghost · destructive · link · sizes sm/default/lg/icon · disabled · loading | Leading verb on secondary actions · trailing chevron on disclosure · spinner replacing the leading icon while loading · icon-only variant |
| Input | default · focused · error · disabled · with icon | Leading kind · trailing clear or reveal |
| Label + Textarea | label above field, `space-1` gap · helper text · counter | None. The counter is a figure. |
| Select | closed · open · selected · disabled | Trailing chevron, rotates 180° on open · tick on the selected item |
| Checkbox / Radio | off · on · indeterminate (checkbox) · disabled | Tick · dash · dot, `icon-xs`, inside the control |
| Switch | off · on · disabled · with label | Tick inside the knob at `icon-xs`, fading in as the knob travels |
| Badge | default · secondary · outline · destructive | Status glyph on status badges only |
| Alert | info · success · warning · destructive · with action · title-only | Leading status mark, `icon-md`, one per variant, straight from the semantic map |
| Avatar | image · initials fallback · sizes · stacked group with an overflow count | Presence or verified badge overlaid bottom right, `icon-xs`. The fallback is initials, never a person glyph. |
| Tooltip | on hover · on keyboard focus · one placement · with a keyboard hint | On the trigger: the `icon-sm` glyph the tooltip explains. Nothing inside the bubble. |
| Spinner | sizes xs–xl · inside a button · inside a card · standalone beside a label | It *is* the icon — `icon-loading`, rotating, one glyph product-wide |
| Separator | horizontal · vertical | None |
| Skeleton | line · block · circle | None |

Rules:

- Touch targets ≥44×44px.
- Buttons sentence case. Never "BOOK NOW".
- One primary button per section.
- Focus is a 2px `--ring` on `:focus-visible`, offset 2px. Never removed.
- Disabled keeps readable text on the fill. Pale on pale is a bug.
- Label above the field. A placeholder is not a label.
- Input and card edges come from `--shadow-border`, not `border`. Hover swaps to
  `--shadow-border-hover`; `box-shadow` is in the transition at `--dur-fast`.
- **Every state change is a transition, never a jump.** Named properties, `--ease-out`,
  `--dur-fast`; `:active` compresses the control to `scale(0.985)` at `--dur-press`.
  Per-element property map in `polish.md` § Transitions.
- Icons come from HugeIcons via `HugeiconsIcon`, at a size token and a stroke token.
  Buttons take `icon-md`; inputs, badges, and tooltip triggers take `icon-sm`.
- Conditional icons cross-fade opacity, scale, and a small blur — never a hard cut.
- Icons align optically, not by bounding box.
- Icon-only buttons carry `aria-label`; an icon beside a label carries `aria-hidden="true"`.
- Icon-only targets stay ≥44×44px at every density. Compact shrinks padding, never the target.
- Figures inside components use `tabular-nums`.
- Titles and any label that can wrap to two lines carry `text-wrap: balance`; helper text
  and descriptions carry `text-wrap: pretty`.
- Control padding follows the density preset: compact `8px 12px`, comfortable `12px 16px`.
- The spinner is the only element in the system that loops. It rotates at a constant rate,
  no pulse, no bounce, and it is removed the frame the content arrives.

---

## Tier 2 — Composite

Core parts assembled. Show the assembly, numbered.

| Component | Parts | Icon slot |
|---|---|---|
| Card | 1 media · 2 title · 3 meta line · 4 tag row · 5 body · 6 footer action | `icon-xs` on each meta fact — one per kind, so location, date, and area draw three · `icon-sm` on the footer action |
| Form field | 1 label · 2 control · 3 helper · 4 error · 5 submit | Kind icon in the control · status mark on the error line · none on submit |
| Dialog | 1 overlay · 2 title · 3 body · 4 cancel + confirm | Close, top right, `icon-md` · leading verb on a destructive confirm |
| Dropdown menu | 1 trigger · 2 items · 3 separators · 4 destructive item | Leading verb on every item · trailing tick on the checked one |
| Tabs | 1 list · 2 active marker · 3 panel | Leading icon only if every tab has one that earns it. Otherwise none. |
| Table | 1 header row · 2 sortable column · 3 body rows · 4 status cell · 5 row action · 6 selected row · 7 empty state · 8 footer | Sort state on every sortable header, direction on the sorted one · status glyph in the status column · `icon-more` in the last cell |
| Pagination | 1 previous · 2 numbers · 3 ellipsis · 4 next · 5 current · 6 disabled ends | Previous and next arrows at `icon-sm` · the ellipsis glyph for the skipped range |
| Toast (sonner) | success · error · loading | One leading status mark, `icon-md` · close trailing |
| Empty state | 1 icon at `icon-xl` · 2 line · 3 one action | The `icon-xl` mark. The largest icon in the product. |

Card container: `radius-lg`, `--shadow-border`, overflow hidden, padding at the density
preset — `space-4` compact, `space-6` comfortable. Inner media radius satisfies
`outer = inner + padding`.
Hover and focus-visible: `--shadow-border-hover`, `--dur-fast`, opacity change only — the
card never moves.

Table: `--shadow-border` on the container, hairline rules between rows, row hover
transitions `background-color` at `--dur-fast`, every figure `tabular-nums`, the header row
sticky if the table scrolls. Sort control is the whole header cell, not the glyph.

Pagination: page numbers `tabular-nums` so they do not shift width, current page marked by
fill rather than by weight, disabled ends keep readable text, every target ≥44×44px.

---

## Tier 3 — The domain component

One per product. The reason this document is worth writing.

### Find it

Ask: **what could a competitor not copy in a week?**

A card layout takes an afternoon. A person who visits every property, a lab that tests
every sample, a signed-off audit trail — those take longer. Whatever answers the question
is the component.

### Shapes

| Shape | Shows | The part that matters |
|---|---|---|
| Record | A check that was done | A person's name and a date |
| Ledger | Where the money went | A total that adds up on screen |
| Timeline | What happened, in order | Dated steps |
| Reading | A measurement | Value + when + how taken |

### Rules

0. **Draw the kinds, not the rows.** The verification mark sits beside the title at
   `icon-md`. Each data cell carries the glyph of *its own kind* at `icon-xs` — sound
   level, speed, and hours on site are three different marks, and marking them is what
   makes the block scannable. The status column swaps its glyph per state; the method link
   takes a trailing `icon-external`. What is forbidden is the same glyph repeating down a
   column — that turns evidence into a sticker sheet.
1. **Name the person.** "Checked by our team" is a claim. "Checked by Trang, March 14" can be wrong, so it can be trusted.
2. **Show the method, not the verdict.** "47 of 47 checked", not a green tick.
3. **Carry a number nobody could guess.** 38 dB at 9pm. 187 Mbps. Four hours on site.
4. **Design the empty state first.** Every value reads `— Pending`. No invented data.
5. **Always full size.** It is the argument, so it never reduces to a badge or a tick.
6. **Biggest example on the page.** It is the main argument.

### Spec template

```markdown
### [Name] — [shape]

Appears on: [pages]

Parts:
1. Label — names what was done
2. Title — the person and the date
3. Data cells — the measurements only this work produces
4. Human note — a quote from whoever did it
5. Link — to the full method

States: complete · pending · not applicable
```

### Examples

| Product | Component | The number |
|---|---|---|
| Long-stay rentals | Inspection record | "38 dB at 9pm", "47 of 47" |
| Money transfer | Fee breakdown | Every fee, plus who receives it |
| Lab software | Result card | Value, method, reference range |
| Second-hand goods | Condition report | The list of faults, not the highlights |
| Developer tools | Run record | Commit, config hash, per-step timing |
| Food supply | Origin trail | Each handover, gaps shown as gaps |

The component that leads with what is **wrong** is the one nobody can fake.

### Ship it as code

```
src/components/<domain>/<Name>.tsx
```

Composed from installed shadcn primitives. Typed props. All states implemented.
Polish pass applied: `tabular-nums` on every measurement, `text-wrap: balance` on the
title and `pretty` on the human note, `--shadow-border` on the surface, a `--dur-fast`
transition on every interactive part, density preset on the padding, staged entrance if it
animates in.

---

## Block order, when order carries the argument

If shuffling the blocks loses the argument, write the order down. As questions, not
section names.

| # | Block | Question answered |
|---|---|---|
| 1 | Title + meta | Is this what I want? |
| 2 | Domain component | Has anyone actually checked? |
| 3 | Cost breakdown | What will I really pay? |
| 4 | Terms, plain | What am I agreeing to? |
| 5 | Form | *Only now.* |

Rule that falls out: **the form never comes before the proof.**
