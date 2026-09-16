# Drift

The design system is the base every screen is drawn on. Drift is anything on a screen the
system does not already provide. It is allowed, it is recorded, and a run that draws new drift
ends by asking the user whether it goes back into the system, so that what serves more than
one feature becomes part of the system and the next run reuses it instead of drifting again,
while minor drift stays in its flow.

## Reuse first

Before drawing anything the system does not show, run the reuse test: name the nearest system
component and the concrete reason it cannot carry this need.

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

Reasons that pass: a state the component lacks, content it cannot hold, a layout the flow
requires, a guideline the flow has a stated reason to break.

Reasons that fail: it would look better, it feels more modern, the system's version is plain.

A failed test means using the system component, with this flow's content in it.

## Kinds of drift

| Kind | What it is | Example |
|---|---|---|
| `component` | A new component the system has nothing for | A floor-plan diagram of a home's rooms |
| `variant` | An existing component in a shape it does not ship | A Badge with a leading avatar |
| `detail` | A one-place adjustment inside a system component or layout | A denser table row where eight dates are compared |
| `guideline` | A system rule broken on purpose, for a stated reason | Two primary buttons on the one screen where both are equally the point |

Composing system components in a layout the viewer does not show is not drift. It is using the
system.

Tokens are not a kind. A new colour, typeface, radius, shadow or spacing step is asked for
before it is drawn, and when the user agrees it goes into the design system first.

## The ledger

Every flow definition carries its drift in its `ledger` array. `drift-report.py` reads it, and
the route renders it under *Building on it*.

```json
"ledger": [
  {
    "name": "Drawer",
    "class": ".drawer",
    "kind": "component",
    "nearest": "Dialog · .dialog",
    "why": "The listing must stay visible while the visitor writes; Dialog centres over a scrim",
    "proposal": "promote",
    "status": "open"
  }
]
```

| Field | Values |
|---|---|
| `name` | The drift's name, spelled the same in every definition that uses it |
| `class` | The CSS class it is drawn with, or `—` for a guideline |
| `kind` | `component`, `variant`, `detail`, `guideline` |
| `nearest` | The nearest system component, name and class |
| `why` | The concrete reason it departs from `nearest` |
| `proposal` | `promote` (it would serve other features) or `one-off` (it belongs to this feature's story): the first read, made while drawing |
| `status` | `open`, then `promoted`, `folded` or `one-off` once the user answers; *Decide later* keeps it `open` |

A drift reused from an earlier flow keeps its name and class and gets a row in this file's
ledger too, so the tally counts the second use.

## Where drift lives

Drift that needs new UI is a **candidate component** under `<dev>/flows/components/`, shared
by every flow that uses it. A `detail` that is a one-place layout adjustment may instead live
as local markup or styles inside that flow's route.

| Proposal or status | Where it lives |
|---|---|
| `promote`, still open | `<dev>/flows/components/<Name>.<ext>`, imported by every flow that uses it |
| `one-off` | the same candidate folder, or local markup in the one flow that uses it |
| `promoted` or `folded` | the real component set (`src/components/ui/…`, `src/lib/components/ui/…`) and the design-system viewer; the flow's import switches to the system component |

All of it is built from the system's tokens. A candidate is never placed in the production
component tree, and a production page never imports one.

## The review

Two ways in, one procedure:

| Entry | Scope |
|---|---|
| Phase 7 of every drawing run, automatically | Questions for the new drift that run drew (`drift-report.py docs/flows --file <flow>.json --new`, one `--file` per flow drawn), after a reuse re-check of every open drift those flows use. SKILL.md, Phase 7, defines new drift |
| `/uikit:prototype drift`, on demand | Every open drift across all definitions |

1. **Tally.** `python3 <skill-dir>/scripts/drift-report.py docs/flows` prints every open drift:
   name, class, kind, the flows using it, proposals and statuses. `--file` limits it to drift
   used by the named definitions, still counting every flow that uses each one. `--new`, used
   with `--file`, keeps only new drift: open in a named flow and open in at most one other
   flow, or any open guideline. Add `--all` to include reviewed rows.
2. **Re-run the reuse test** on every row in scope against the current system. The system may
   have gained a component since the drift was drawn. A drift the system now covers is
   replaced, not promoted: swap in the system component in every flow that uses it, delete the
   candidate, remove the ledger row, set its `from` in the components table to the component
   path, then run the checks.
3. **Propose a verdict per row,** taking the first that fits:

   | Verdict | When |
   |---|---|
   | **one-off** | Used by one feature, and either a `detail` or tied to that feature's story: too small or too specific for the system |
   | **fold** | A system component nearly covers it; it becomes a variant of that component instead of a new one |
   | **promote** | Used by two or more features, or its anatomy carries no feature-specific content, and no system component covers it with a variant |

   A drift one feature kept as a one-off that another now reuses is no longer tied to one
   story; say so. A `guideline` drift is proposed as **change the guideline** or **keep as this
   flow's exception**. One used by two or more features is a sign the guideline does not fit
   this product; say so. Changing the guideline is the user's call.
4. **Ask per row and wait.** Lead with the recommended verdict and its one-line reason. *Decide
   later* is always an option and leaves the row `open`. Nothing is promoted without an answer.
5. **Apply the answers:**
   - **promote or fold:** author the component or variant in the real component set following
     the `init-design-system` skill's rules (`references/components.md`, `hierarchy.md`,
     `polish.md`, `viewer-spec.md`), add it to the design-system viewer's Components section,
     and move the candidate out of `<dev>/flows/components/`. Point **every flow that imports
     it** at the system component: in each one the components-table `from` becomes the new
     path and the ledger status becomes `promoted` or `folded`. The review writes component
     code; it does not write production pages.
   - **one-off:** keep the candidate in `<dev>/flows/components/` (or the local markup), set
     the status to `one-off`.
   - **change the guideline:** rewrite the rule in the design system's component rules so the
     flow's case is allowed, and set the status to `promoted` in every flow that uses it.
   - **keep as this flow's exception:** set the status to `one-off`. A guideline drift has no
     component to move.
6. **Verify.** `flow-check.py` passes for every touched definition, `drift-report.py --all`
   shows the new statuses, and the app typechecks and the touched flow routes render.

## Legacy flow files

A project migrating from the static-HTML model has `docs/flows/*.html` files. `drift-report.py`
still reads their ledgers, so the tally is continuous, and `/uikit:prototype drift` reviews
them alongside the definitions. Migrate one on request: convert its shell to a definition and
its screens to the route, then delete the HTML. Until then the HTML file is the record.
