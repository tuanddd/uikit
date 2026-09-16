# Hierarchy

Not everything can be important. Rank the content, then style it.

Three levers: **size**, **weight**, **color**. All three draw on tokens that already exist
in `tokens.md` — nothing new is invented here, and no value is hand-picked.

---

## The one rule

One lever moves at a time. Two only on the single most important element in the view.
Never three.

| Rank | Lever moved | Lands as |
|---|---|---|
| Primary | Size up — or color to `ink` | `h3` · 400 · `ink` |
| Secondary | Neither — the base | `body` · 400 · `neutral-700` |
| Tertiary | Size down, tracking up | `caption` or `eyebrow` · 500 · `neutral-700` |

An element already larger, heavier, and darker than everything around it has nothing left
to escalate to.

---

## The levers, in this system

### Size

The type scale in `tokens.md` §2 is the whole range. One step of the scale is one rank.
Two adjacent ranks never share a token.

### Weight

400 and 500. That is the full set — the display and body families ship two weights each,
and 600/700 do not exist. Emphasis inside a line is `500` or it is a different size; it is
never synthetic bold.

`eyebrow` and `caption` carry 500 at their size so they read as labels, not as small body.

### Color

| Level | Token | CSS variable | Use |
|---|---|---|---|
| Primary text | `ink` | `--foreground` | Titles, values, figures, body |
| Secondary text | `neutral-700` | `--muted-foreground` | Labels, meta, helper, descriptions |
| Marks only | `neutral-500` | — | Icons standalone. Never body text. |

There is no third text gray. A third rank is made with size, never by lightening past
`neutral-700` — the contrast floor does not move.

Status color is not a rank. `error`, `warning`, and `success` say *what*, not *how
important*; a red label is not a promoted label.

---

## Labels rank below what they name

Form labels, table headers, card meta, axis ticks, and captions support the data. They
never compete with it.

A label names a value, never a heading. The eyebrow stack, a small uppercase line placed
above a large title, is banned in every size: hero, section, card, form. The heading is the
first element in its block and names the section on its own. A fact the small line carried
(city, date, status) goes to the meta line under the heading; a category it carried is
either redundant or is the better heading.

| Pair | Label | Value |
|---|---|---|
| Form field | `caption` · 500 · `neutral-700`, above the input | `body` · 400 · `ink` |
| Table column | `eyebrow` · 500 · `neutral-700` · uppercase | `body` · 400 · `ink` |
| Metric tile | `caption` · 500 · `neutral-700`, under the figure | `display` · 400 · `ink` · `tabular-nums` |
| Card meta line | `icon-xs` + `small` · 400 · `neutral-700` | — |
| Specimen label | `caption` · 500 · `neutral-700`, inside the cell | the specimen |

---

## Buttons carry the same three ranks

One primary action per view. Everything else steps down.

| Rank | Variant | Fill | Icon slot |
|---|---|---|---|
| Primary | `default` | `primary-700` | None — text alone |
| Secondary | `secondary` · `outline` | `neutral-100` · border only | Leading verb |
| Tertiary | `ghost` · `link` | None | Leading verb, or none |
| Destructive, routine | `ghost` or `outline`, `error` text | None | Leading verb |
| Destructive, irreversible | `destructive` | `error` | None |

A row-level delete is routine. A filled `error` button on every row makes the one
irreversible confirm unreadable.

Variant names are the component's API and stay the same in every stack — the Svelte and
Astro components take `variant="secondary"` too, so a reader of the viewer reads one
vocabulary.

---

## Never de-emphasized

These sit at primary or secondary level in every view that shows them, whatever the layout
argues:

| Always readable |
|---|
| The total, and the all-in figure |
| Any fee, deposit, or charge not inside that figure |
| Notice period, lock-in, and cancellation terms |
| The control that cancels, closes, or opts out |

Hierarchy ranks content. It does not hide it.

---

## Two checks, both run

| Check | How | Pass |
|---|---|---|
| Grayscale | Render the view with `filter: grayscale(1)` | The ranking is unchanged — color was not carrying it |
| Squint | Blur to ~6px, or step back from the screen | The primary element is still the first thing found |

Run both before the polish pass. A view that fails either is fixed with size and spacing,
not with a stronger color.

---

## Wrong / right

| Wrong | Right |
|---|---|
| Title is larger, 500, and `ink` | Larger and `ink`. Save 500 for the one element that outranks it. |
| Form label same size and color as its value | Label `caption` · `neutral-700`; value `body` · `ink` |
| Table header styled like the cells | `eyebrow` · uppercase · `neutral-700` |
| A small uppercase line above a title (eyebrow, kicker, overline) | Delete it, or move its fact to the meta line under the title; the heading stands first |
| A third text gray invented for tertiary text | Step the size down; keep `neutral-700` |
| `neutral-500` used for a meta line | `neutral-500` is for icons; text takes `neutral-700` |
| Filled destructive button on every table row | `ghost` + `error` text; fill only the irreversible confirm |
| Two primary buttons in one view | One. The rest step down. |
| Brand color used to make something important | Size and weight rank it; primary color marks the action |
| Status color read as a rank | Status says what it is; rank is size, weight, color level |
| Price or cancellation term set in the smallest gray | Primary or secondary level, always |
| Everything at `ink` | Only the ranked content; labels and meta drop to `neutral-700` |

---

## Checklist

- [ ] Every view has exactly one primary element
- [ ] No element moves all three levers
- [ ] Weights are 400 and 500 only; zero 600/700 and zero synthetic bold
- [ ] Text is `ink` or `neutral-700`; no third text gray exists
- [ ] `neutral-500` appears on icons only, never on text
- [ ] Every label ranks below the value it names
- [ ] Table headers are `eyebrow`, uppercase, `neutral-700`
- [ ] No heading has a smaller line above it; `eyebrow` labels name values, never titles
- [ ] One primary button per view; routine destructive actions are not filled
- [ ] Totals, fees, terms, and the opt-out control sit at primary or secondary level
- [ ] Grayscale check passes — the ranking survives without color
- [ ] Squint check passes — the primary element is found first
