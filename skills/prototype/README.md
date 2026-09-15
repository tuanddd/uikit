# prototype

`/uikit:prototype <feature>` draws a feature as a self-contained HTML flow file on top of the project's design system. Part of the `uikit` plugin.

## What it produces

One static HTML file per feature, in `docs/flows/`:

- every step of the flow as a screen, start to end, with its state and route
- the decisions behind each screen and the shipped products they rest on
- the routes, mock values and components a build starts from
- a drift ledger: everything on the screens the design system does not already provide, why, and whether it should become a system component

Each file opens by double-click. No build, no server, no data. Values the flow does not demonstrate are fixed mock values shared by every file.

## Why one file per feature

A new feature starts as a copy of the flow file closest to it, and every file carries the same shared style blocks. Each feature is drawn against what is already drawn, so the UI drifts as little as possible from one feature request to the next.

## The design system is the base

`docs/design-system.html`, written by `/uikit:init-design-system`, is where every screen starts.

- **Covered by the system:** the screen uses the system component. No Modal when there is a Dialog.
- **Not covered, or the nearest component cannot carry what the flow needs:** drift, drawn from the system's tokens and recorded in the ledger.
- **Tokens never drift.** A new colour, typeface, radius or shadow is asked for first.

Every run ends by asking you about each new drift it drew, with a recommended answer: add it as a system component, fold it into an existing one as a variant, or keep it as a one-off. New drift is a drift no other flow has, its second use, a one-off another flow now reuses, or a broken guideline. Minor drift stays in its flow; reusable drift goes into the system, so the next run reuses it. Drift already open across several flows, and drift you answer *Decide later*, is listed and waits for `/uikit:prototype drift`.

## Requirements

- A Mobbin plan with its MCP server connected. It is paid; the skill checks it first and tells you. Without it the skill can continue on free sources, where more decisions rest on a principle instead of a shipped reference.
- A design system page. Without one, the skill recommends running `/uikit:init-design-system` first.
- `python3`, for `scripts/sync-blocks.py` and `scripts/drift-report.py`.

## Usage

| Invocation | Behavior |
|---|---|
| `/uikit:prototype <feature>` | One flow file for that feature, then the fold-back questions |
| `/uikit:prototype <feature>, <feature>` | One file per feature, drawn one at a time, then one round of fold-back questions |
| `/uikit:prototype <feature> --system <path>` | That file as the design system |
| `/uikit:prototype update <flow-file> <change>` | Redraws or adds steps in an existing file, then the fold-back questions |
| `/uikit:prototype drift` | Asks again about drift still open across all flow files |

## How it works

| Phase | What happens |
|---|---|
| 0 · Preflight | Checks the Mobbin MCP (paid) and tells you; finds the design system, the flow files and the domain docs |
| 1 · Map the flow | Names the feature and its requirement line, lists every step, picks the closest existing file |
| 2 · Map to the system | Every UI need goes to a system component, an earlier flow's component, or a recorded drift |
| 3 · Bank references | Looks up how shipped products solved each step |
| 4 · Draw | Copies the closest file, draws every step, fills the decisions, build notes and drift ledger |
| 5 · Verify | Self-contained, blocks in sync, anchors, reuse, ledger, craft rules, no sideways scroll |
| 6 · Report | Paths, reuse tally, drift, the decisions resting on a principle |
| 7 · Fold back | Asks, per new drift, whether it joins the design system or stays a one-off, then applies your answers |

## Files

```
SKILL.md                 workflow, hard rules, invocations
FLOW-FILE.md             the flow file's anatomy: head, style blocks, sections, the index README
DRIFT.md                 the reuse test, drift kinds, the ledger, the drift review
CRAFT-RULES.md           eight layout constraints every screen is built and checked against
REFERENCE-SOURCES.md     the Mobbin check, Mobbin MCP first and the site second, free fallbacks, banking
templates/flow.html      the skeleton for a project's first flow file
scripts/sync-blocks.py   copies shared style blocks into every flow file; --check verifies
scripts/drift-report.py  tallies drift across flow files for the review; --file and --new scope it to one run
```
