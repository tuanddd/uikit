# prototype

`/uikit:prototype <feature>` draws a feature as a flow definition plus a dev route that
renders every step from the project's real components. Part of the `uikit` plugin.

## What it produces

One flow per feature:

- `docs/flows/<slug>.json` — the definition: the requirement and its source, every step with
  its state and route, the decisions and the shipped products they rest on, the components,
  and the drift ledger.
- `/uikit/flows/<slug>` — a dev route that renders the definition's documentation and each
  step's screen, composed from the project's real components. A screen built from the system
  imports the system component; nothing redraws it.
- For drift that needs new UI, a **candidate component** in the dev flow area
  (`<dev>/flows/components/`), imported like any other and never placed in the production
  component tree.

Values the flow does not demonstrate are fixed mock values shared by every flow. The route is
a dev surface: hidden outside local and preview, unlinked, `noindex`, and off the sitemap.

## Why a route

The screens show the real components, so a flow cannot drift from the design system the way a
copied stylesheet can. The definition stays the portable, diffable record a build and the
scripts read; the route is the renderer. A new feature starts from the closest existing flow,
so each feature is drawn against what is already drawn.

## The design system is the base

The live system — the project's components and `tokens.json`, the same one
`/uikit/design-system` renders — is where every screen starts.

- **Covered by the system:** import the system component. No Modal when there is a Dialog.
- **Not covered, or the nearest component cannot carry what the flow needs:** drift, authored
  as a candidate component from the system's tokens and recorded in the ledger.
- **Tokens never drift.** A new colour, typeface, radius or shadow is asked for first.

Every run ends by asking you about each new drift it drew, with a recommended answer: add it
as a system component, fold it into an existing one as a variant, or keep it as a one-off.
Minor drift stays a candidate in its flow; reusable drift is promoted into the real component
set and the viewer, so the next run imports it. Drift already open across several flows, and
drift you answer *Decide later*, waits for `/uikit:prototype drift`.

## Requirements

- A Mobbin plan with its MCP server connected. It is paid; the skill checks it first and tells
  you. Without it the skill can continue on free sources, where more decisions rest on a
  principle instead of a shipped reference.
- A design system. Without one, the skill recommends running `/uikit:init-design-system`
  first, or — where a live route cannot be hosted — the static fallback page.
- `python3`, for `scripts/flow-check.py` and `scripts/drift-report.py`.

## Usage

| Invocation | Behavior |
|---|---|
| `/uikit:prototype <feature>` | One flow for that feature, then the fold-back questions |
| `/uikit:prototype <feature>, <feature>` | One flow per feature, drawn one at a time, then one round of fold-back questions |
| `/uikit:prototype <feature> --system <path>` | That file as the design system |
| `/uikit:prototype update <flow> <change>` | Redraws or adds steps in an existing flow, then the fold-back questions |
| `/uikit:prototype migrate <flow.html>` | Converts a legacy HTML flow to a definition and a route |
| `/uikit:prototype drift` | Asks again about drift still open across all flows |

## How it works

| Phase | What happens |
|---|---|
| 0 · Preflight | Checks the Mobbin MCP (paid) and tells you; finds the live design system, the flows and the domain docs |
| 1 · Map the flow | Names the feature and its requirement line, lists every step, picks the closest flow |
| 2 · Map to the system | Every UI need goes to a system component, an earlier flow's candidate, or a recorded drift |
| 3 · Bank references | Looks up how shipped products solved each step |
| 4 · Draw | Writes the definition, authors the route and screens, and any candidate the drift needs |
| 5 · Verify | Definitions valid, ledger tallied, the app builds, the route renders, dev-gated, craft rules, no sideways scroll |
| 6 · Report | The definition and route, the reuse tally, drift, the decisions resting on a principle |
| 7 · Fold back | Asks, per new drift, whether it joins the design system or stays a one-off, then applies your answers |

## Files

```
SKILL.md                 workflow, hard rules, invocations
FLOW-FILE.md             the definition schema, the route, the FlowShell and the index
DRIFT.md                 the reuse test, drift kinds, the ledger, candidates, the drift review
CRAFT-RULES.md           eight layout constraints every screen is built and checked against
REFERENCE-SOURCES.md     the Mobbin check, Mobbin MCP first and the site second, free fallbacks, banking
templates/flow.json      the starter definition for a project's first flow
templates/FlowShell.tsx  a React reference for the shell every flow renders through
scripts/flow-check.py    validates every definition against the schema
scripts/drift-report.py  tallies drift across definitions and legacy HTML files; --file and --new scope it to one run
```
