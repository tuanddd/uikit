# Drift

The design system is the base every screen is drawn on. Drift is anything on a screen the system does not already provide. It is allowed, it is recorded, and it is reviewed, so that what serves more than one feature becomes part of the system and the next run reuses it instead of drifting again.

## Reuse first

Before drawing anything the system does not show, run the reuse test: name the nearest system component and the concrete reason it cannot carry this need.

| Reaching for | The system probably has | It is drift only when |
|---|---|---|
| Modal, popup, lightbox | Dialog | the page must stay usable beside it, or it holds a multi-step form Dialog has no layout for |
| Side panel, slide-over | Sheet, Drawer | the system has neither |
| Custom dropdown or picker | Select, Combobox, Dropdown menu | options need rich rows (avatar, meta, price) the component cannot hold |
| Toast, snackbar, banner | Alert, Toast | the message must persist inline where Alert does not fit |
| Pill, chip, label | Badge, Tag | it is interactive (removable, toggles) and no chip or toggle variant exists |
| Stat box, number tile | Card, key/value cell | the value needs a comparison or trend the card has no slot for |
| Stepper, progress rail | Progress, Tabs, Breadcrumb | each step must show its own state |
| Info icon with a popup | Tooltip, Popover | never on touch; use inline help text instead |

Reasons that pass: a state the component lacks, content it cannot hold, a layout the flow requires, a guideline the flow has a stated reason to break.

Reasons that fail: it would look better, it feels more modern, the system's version is plain.

A failed test means using the system component, with this flow's content in it.

## Kinds of drift

| Kind | What it is | Example |
|---|---|---|
| `component` | A new component the system has nothing for | A floor-plan diagram of a home's rooms |
| `variant` | An existing component in a shape it does not ship | A Badge with a leading avatar |
| `detail` | A one-place adjustment inside a system component or layout | A denser table row where eight dates are compared |
| `guideline` | A system rule broken on purpose, for a stated reason | Two primary buttons on the one screen where both are equally the point |

Composing system components in a layout the system page does not show is not drift. It is using the system.

Tokens are not a kind. A new colour, typeface, radius, shadow or spacing step is asked for before it is drawn, and when the user agrees it goes into the design system first.

## The ledger

Every flow file carries its drift in a table under *Building on it*. One row per drift, marked up so `scripts/drift-report.py` can read it:

```html
<h3 class="a-sub">Drift from the design system</h3>
<div class="a-tblwrap">
  <table class="a-tbl">
    <thead>
      <tr><th>Drift</th><th>Kind</th><th>Nearest in the system</th><th>Why it departs</th><th>Proposal</th><th>Status</th></tr>
    </thead>
    <tbody>
      <tr data-drift="Drawer" data-class=".drawer" data-kind="component" data-proposal="promote" data-status="open">
        <td>Drawer <code>.drawer</code></td>
        <td>component</td>
        <td>Dialog <code>.dialog</code></td>
        <td class="prose">The listing must stay visible while the visitor writes; Dialog centres over a scrim</td>
        <td>promote</td>
        <td>open</td>
      </tr>
    </tbody>
  </table>
</div>
```

A file with no drift says so in one line in place of the table: `<p class="a-empty">No drift. Every component on these screens is in docs/design-system.html.</p>`

| Field | Values |
|---|---|
| `data-drift` | The drift's name, spelled the same in every file that uses it |
| `data-class` | The CSS class it is drawn with, or `—` for a guideline |
| `data-kind` | `component`, `variant`, `detail`, `guideline` |
| `data-proposal` | `promote` (it would serve other features) or `one-off` (it belongs to this feature's story): the first read, made while drawing |
| `data-status` | `open`, then `promoted`, `folded` or `one-off` after a review |

A drift reused from an earlier flow file keeps its name and class and gets a row in this file's ledger too, so the tally counts the second use.

## Where drift CSS lives

| Proposal or status | Block | Shared |
|---|---|---|
| `promote`, still open | the product block (`{prefix}-product`) | every flow file, synced |
| `one-off` | `flow-local`, in the one file that uses it | no |
| `promoted` or `folded` | the base block (`{prefix}-base`), and the design system page | every flow file, synced |

All of it is built from the system's tokens.

## The review

`/uikit:prototype drift`

1. **Tally.** `python3 <skill-dir>/scripts/drift-report.py docs/flows` prints every open drift across the flow files: name, class, kind, the files using it, proposals and statuses. Add `--all` to include reviewed rows.
2. **Re-run the reuse test** on every open row against the current system. The system may have gained a component since the drift was drawn; a drift the system now covers is replaced in its files, not promoted.
3. **Propose a verdict per row:**

   | Verdict | When |
   |---|---|
   | **promote** | Used by two or more features, or its anatomy carries no feature-specific content, and no system component covers it with a variant |
   | **fold** | A system component nearly covers it; it becomes a variant of that component instead of a new one |
   | **one-off** | Used by one feature, and its anatomy is tied to that feature's story |

   A `guideline` drift used by two or more features is a sign the guideline does not fit this product. Say so; changing the guideline is the user's call.

4. **Show the table and wait.** The user picks per row. Nothing is promoted without a pick.
5. **Apply the picks:**
   - **promote or fold:** add the component or variant to `docs/design-system.html` following the `init-design-system` skill's rules (`references/components.md`, `hierarchy.md`, `polish.md`, `html-spec.md`): a tab in the components section, every state live, real copy. Move its CSS from the product block to the base block in one flow file, then sync both blocks to the rest. Update every file's components table (`From` becomes `docs/design-system.html`) and ledger status (`promoted` or `folded`). If the project's design system also ships as installed components, name the component that now needs writing and ask before touching code.
   - **one-off:** move its CSS from the product block to the `flow-local` block of the one file that uses it, sync the product block, set the status to `one-off`.
6. **Verify.** `sync-blocks.py --check` exits 0, `drift-report.py --all` shows the new statuses, and every touched flow file renders as it did.

## Files drawn before the ledger existed

Older flow files may mark drift only in the components table, as `Proposed here` or `Proposed in <file>`. `drift-report.py` reads those rows as open `component` drift with no proposal. Give such a file a ledger the next time it is updated.
