---
name: prototype
description: Prototype a feature as a flow definition in docs/flows/ plus a dev route at /uikit/flows/ that renders every step from the project's real components — the decisions and the shipped products they rest on, and a ledger of where the drawing drifts from the system. Researches flows through the paid Mobbin MCP and checks it is connected before starting. Only runs when explicitly invoked; it does not trigger on its own.
disable-model-invocation: true
---

# Prototype

Take a feature the user asks for, learn how shipped products solved its flow, and draw it
start to end as a flow that renders the project's **real components**. The route is what a
build starts from and what the next feature is drawn against; the definition beside it is the
portable record of the steps, the decisions and the drift.

**Input:** a feature request, the project's design system, and the flows already drawn.
**Output:** one flow definition in `docs/flows/` and one dev route at `/uikit/flows/<slug>`
per feature.

You are the designer, the researcher and the builder. Nobody will ask how step 2 works, what
the empty state offers or where the price sits, so ask yourself, and answer from evidence.

`<skill-dir>` below is the directory this file lives in (`~/.claude/skills/uikit/skills/prototype` for a skills-dir install).

## Operating posture

Three failure modes to design against:

- **Building from taste.** Nearly every step of every flow has been solved by a shipped product. Phase 3 goes and looks. Skip it and the file is an opinion.
- **Reinventing the wheel.** Drawing a Modal while the system has a Dialog, a custom dropdown while it has a Select, a hand-rolled toast while it has an Alert. A screen built from the system **imports** the system component; there is no redraw to drift. A near-copy of a system component is the most expensive drift there is: it looks like a new component and is not one.
- **Silent drift.** Departing from the system without writing it down. Drift is allowed. Drift nobody recorded is how the next feature stops matching this one.

## The design system is the base, not a cage

The live system — the project's components and `tokens.json`, the same one
`/uikit/design-system` renders — is where every screen starts. It is not a rulebook that
forbids whatever it does not show. Every UI need on a screen goes through this lookup, in
order:

| The need | Do |
|---|---|
| A system component covers it, as-is or with a variant it already ships | **Import it** and use it. Its props, variants and states are the component's own. The content changes; the component does not |
| An earlier flow already proposed a component for it | Import that **candidate**; the second use is evidence for promoting it |
| Nothing covers it, or the nearest component cannot carry what this flow needs | **Drift:** author a candidate component from the system's tokens under the dev flow area, import it, and record it in the ledger |

Drift is for what the narrative, the flow or the requirement genuinely asks for: a drawer the
page must stay visible beside, a denser row where eight dates are compared, two primary
actions on the one screen where both are equally the point. It is not for a component you
would have styled differently.

**The reuse test, before any drift:** name the nearest system component and the concrete
reason it cannot carry this need: a state it lacks, content it cannot hold, a layout the flow
requires. If the only reason is how it looks, it is not drift. Import the component.

**Tokens do not drift.** Colour, typeface, radius, shadow and spacing come from the system. A
token that does not exist is a question for the user, asked before it is drawn.

Every drift gets a ledger row with its kind, the nearest system component, why it departs, and
a first proposal: `promote` (it would serve other features) or `one-off` (it belongs to this
feature's story). Every run then ends by asking the user, one question per new drift it drew,
whether that drift goes back into the design system (Phase 7). Reusable drift becomes a system
component, so future runs import it instead of drifting again; minor drift stays a one-off in
its flow. Ledger format, kinds and the review: [DRIFT.md](DRIFT.md).

## Hard rules

1. **Check Mobbin before anything else.** It is a paid service. The user hears whether it is connected before any research starts.
2. **Reuse before drift.** A drift that fails the reuse test is a defect, not a design choice.
3. **Record every drift.** A component on a screen that is neither a system component nor a candidate with a ledger row is a defect.
4. **No new tokens without asking.** Drift happens in components, variants, details and guidelines, never in the token set.
5. **Screens import real components.** A screen built from the system imports the system component; no screen redraws one. Drift that needs new UI is a candidate component, imported like any other.
6. **Screens are static, with mock values.** Anything the flow does not demonstrate uses the fixed mock values in the flows README. States (validation, empty, error, sent) are drawn as their own steps.
7. **One shell, reused.** The `FlowShell` that renders the documentation around the screens is authored once per project and reused by every flow. Retyping it per flow is how drift starts.
8. **The route is a dev surface.** Hidden outside local and preview: env-gated, unlinked, `noindex`, `robots.txt`-disallowed, off the sitemap, `data-dev-surface`.
9. **Never load the design-system route whole.** Read the components it imports one at a time; do not dump a hundred components into context. Use `grep` to find the one you need.
10. **Never bypass a paywall, blur or login wall.** In the user's real browser, open only your own tab and close only what you opened.
11. **A drawing run never touches production code.** It writes to `docs/flows/` and the dev flow area only. A candidate component is not placed in the production component tree, and no production page imports one. **Promotion is the one exception:** when the user answers Phase 7 or the drift review, that step authors the component in the real component set and the viewer, and the flows switch their import to it.
12. **Ask before the run ends.** A run that drew new drift, as Phase 7 defines it, ends with the fold-back questions. It never folds drift into the system on its own, and never ends without asking.

## Workflow

### Phase 0 — Preflight

**1. Mobbin, paid.** Load the tools before any other work:

```
ToolSearch("+mobbin")
```

- **Tools load:** tell the user in one line, then continue. *"Mobbin MCP is connected. It is a paid service; this run uses it for the reference lookups, about one search per step."* The first lookup doubles as the auth check: if it fails with an auth or quota error, stop and say so.
- **No tools:** stop and ask. *"Mobbin MCP is not connected. It comes with a paid Mobbin plan and is where this skill finds how shipped products solved each step. Connect it and rerun, or continue on free sources, where more decisions rest on a principle instead of a reference."* Wait for the answer.

**2. The design system.** Read `docs/uikit.md` (the `/uikit:setup` record) first when it exists: it names the approved source. Then find the live system: the `/uikit/design-system` route and the components it imports, `tokens.json`, and the global stylesheet. Then `docs/design-system.html` (the fallback), `docs/**/design-system*.html`, and machine-readable tokens. A path passed with `--system` wins.

- One found: it is the base. Note the component directory and import aliases — Phase 4 imports from them.
- Several found: ask which.
- None found: say so and recommend `/uikit:init-design-system` first. If the user goes ahead anyway, distill a token block from whatever tokens the repo has; every component is then drift, and the ledger says so.

**3. Flows already drawn.** Look for `docs/flows/README.md`, `docs/flows/*.json` (definitions) and `docs/flows/*.html` (legacy files from the static model). When `docs/uikit.md` records a different flows path, that path is the one.

- Found: they are the baseline. Their mock values, cast, naming and shell are reused as they are. A legacy HTML flow is read for its ledger and components; migrate it on request.
- None: this run creates `docs/flows/`, its README, and the first flow.

**4. Domain docs.** Product, audience and their state on arrival, the one question every screen answers, voice rules, hard constraints, and the roadmap or feature list the request belongs to. Search `README.md`, `PROJECT.md`, `PRODUCT.md`, `CLAUDE.md`, `positioning.md`, `docs/brand/*`, `docs/FEATURES.md`.

State what you found in one line each, then continue. Stop only for the Mobbin answer, a missing design system, or two candidates that conflict.

### Phase 1 — Map the feature's flow

1. **Name the feature and its requirement.** Quote the roadmap or feature-list line it implements; with none, quote the user's ask. That quote becomes `requirement.text` and its source.
2. **Split into flows.** One flow per feature. A request spanning several features becomes several flows, drawn one at a time. Confirm the split only when the boundary is genuinely unclear.
3. **List the steps, start to end.** One row per screen: title, state, route. The states that belong to this flow (validation, empty, error, sent, too many results) are steps of their own.
4. **Link, do not redraw.** A step another flow already draws is linked (`<other-flow>#step-3`), not drawn again.
5. **Pick the closest flow.** The existing definition sharing the most steps or components with this feature. The new definition starts as a copy of it; with no flows yet, from [templates/flow.json](templates/flow.json).

### Phase 2 — Map every need to the system

Write `component-map.md` in the scratchpad, one row per UI need across all steps:

```
| Need | Component | Import | Reuse test |
|---|---|---|---|
| Confirm before withdrawing an inquiry | Dialog | src/components/ui/dialog.tsx | — |
| Channel rows with an action | Channel row (candidate) | dev/flows/components/channel-row | — |
| Panel from the right, page visible beside it | Drawer (candidate) | dev/flows/components/drawer | Dialog centres over a scrim; the listing must stay visible while the visitor writes |
```

Read the inventory from the code, not from memory: list the component directory and the design-system route's imports, each component's variants and props, and the candidate folder for what earlier flows proposed. Run the reuse test on every drift row before drawing it. Details and a table of the usual reinventions: [DRIFT.md](DRIFT.md).

### Phase 3 — Bank the references

For each step, find how shipped products solved it and bank the answer before drawing. Method, sources, gate handling and fallbacks: [REFERENCE-SOURCES.md](REFERENCE-SOURCES.md).

Bank to `reference-bank.md` in the scratchpad, one row per step:

```
| Step | Decision | Source | Confidence |
|---|---|---|---|
| 2 of 5 | Ask dates before identity; identity last | Mobbin MCP — Zillow, Airbnb | reference |
| 4 of 5 | A failed send keeps every field and names one next action | Mobbin MCP — Etsy, Gusto | reference |
| 3 of 5 | The reply-time line shows both clocks | the positioning doc, audience | principle, not reference |
```

**Completion criterion:** every step has at least one banked row, or an explicit "no reference found, decided by principle" note naming the principle.

### Phase 4 — Draw the flow

**Read [FLOW-FILE.md](FLOW-FILE.md) and [CRAFT-RULES.md](CRAFT-RULES.md) before writing anything.** The first is the definition schema, the route and the shell; the second is eight layout constraints every screen is checked against.

1. **Write the definition** `docs/flows/<slug>.json` from the closest definition or the template. Fill the requirement, the steps, the why rows, the components table and the ledger.
2. **Author the `FlowShell`** in the dev flow area if this project has none, from
   [templates/FlowShell.tsx](templates/FlowShell.tsx) or its Svelte/Astro translation. Every
   flow reuses it.
3. **Create the route** at the stack's path (`FLOW-FILE.md` § The route). Import the definition and the real components, and render `<FlowShell def={…} screens={{ "step-1": …, }} />`, one screen per step.
4. **Build every screen from the map.** Import system components and use them as they are; import candidates for drift. An overlay is drawn open, in place, over the page it opens from. A `detail` that is a one-place adjustment may live as local markup in the route.
5. **Author every candidate** the drift needs under `<dev>/flows/components/`, from the system's tokens, typed, with the states the ledger records. It is a real component of the project's stack; production never imports it.
6. **Real content, in the project's voice.** Everything the flow does not demonstrate takes the fixed mock values from the flows README. A value this flow needs that the README lacks is added to the README first, so the next flow uses the same one.
7. **Wire it in.** Add the index row to `docs/flows/README.md`, and point the previous and next flows' pagers at the new route.

### Phase 5 — Verify

Run every check before reporting. A breach is fixed, not reported as a note.

1. **Definitions valid:** `python3 <skill-dir>/scripts/flow-check.py docs/flows` exits 0.
2. **Ledger:** `python3 <skill-dir>/scripts/drift-report.py docs/flows` lists every drift this flow introduced or reused, and nothing it did not.
3. **The app builds:** the project's typecheck and build pass with the new route and candidates.
4. **The route renders:** open `/uikit/flows/<slug>` in dev; every definition step has a screen and every screen has a step, every anchor resolves, every component a screen imports is in the components table, and the console is clean.
5. **Dev-gated:** the route is unlinked, `noindex`, `robots.txt`-disallowed, off the sitemap, and 404s (or is not built) in production, per the design-system viewer's gate.
6. **Craft:** screenshot the boards with the browser tool the session has (`playwright-cli`, `browser-harness`, or headless Chrome) and run the eight checks at the end of `CRAFT-RULES.md`.
7. **No sideways scroll:** the flow page does not scroll horizontally at 400px or 1400px; each screen sits in its own frame.

### Phase 6 — Report

1. The definition path and the route, and how to open it: `/uikit/flows/<slug>` in dev.
2. The steps drawn, and which steps link to other flows instead.
3. The reuse tally: components imported from the system, components reused from earlier flows, drifts.
4. The drift introduced: each one, its kind and its proposal.
5. The `principle, not reference` rows, named as the likeliest to be wrong.
6. Which research route ran: Mobbin MCP, the Mobbin site, or free sources.

After the last flow's report, go to Phase 7.

### Phase 7 — Fold drift back

Runs automatically at the end of every run that draws: one feature, several features, or an `update`. With several features it runs once, after the last flow's report, over every flow the run drew, so a drift two of them share shows up as shared. The procedure is DRIFT.md's *The review*, scoped to this run.

**New drift** is what this phase asks about:

- a drift open in a flow this run drew and open in at most one other flow. That covers a drift no other flow has, its second use, and a drift an earlier flow kept as a one-off that this run reused;
- every open `guideline` drift in those flows, however many flows share it, since keeping an exception is each flow's own call.

In an `update`, only the ledger rows the update added can be new drift, under the same test.

1. **Tally the flows this run drew,** one `--file` per flow: every open drift they use, then the new drift among them.

   ```bash
   python3 <skill-dir>/scripts/drift-report.py docs/flows --file <first-flow>.json --file <second-flow>.json
   python3 <skill-dir>/scripts/drift-report.py docs/flows --file <first-flow>.json --file <second-flow>.json --new
   ```

   Each row still counts every flow that uses the drift.
2. **Re-run the reuse test** on every open drift in the first tally, new or not. A drift the system now covers is replaced, not asked about: import the system component in place of the candidate, delete the candidate, remove the ledger row, set the components-table `from` to the component path, run DRIFT.md's checks, and report it. A new drift is replaced in every flow that uses it; any other covered drift is replaced in the flows this run drew, and named for `/uikit:prototype drift` to replace in the rest.
3. **List the open drift that is not new in one line,** with its count: drift already open across two or more other flows and, in an `update`, rows kept from before the update, once the `--new` tally is narrowed to the rows the update added. With no new drift left, say *"No new drift in this run, nothing to fold back."*, offer to go through the listed drift now, and end the run unless the user says yes.
4. **Recommend an answer per new drift,** taking the first that fits, with a one-line reason:

   | Answer | Recommend when |
   |---|---|
   | **Keep as a one-off** (`one-off`) | Used by one flow, and either a `detail` or tied to that feature's story. Too small or too specific to earn a place in the system |
   | **Fold into the nearest component** (`fold`) | A system component nearly covers it; it becomes a variant of that component |
   | **Add to the system** (`promote`) | Used by two or more flows, or its anatomy carries nothing specific to this feature, and no system component covers it with a variant |

   A drift an earlier flow kept as a one-off is now used twice: say so, since that is the reason to reconsider it. A `guideline` drift has two answers of its own: **Change the guideline** in the system, or **Keep as this flow's exception**.
5. **Ask, and wait.** One question per new drift: its name and class, its kind, the flows using it, the nearest system component, and the recommended answer first with its reason. The options are the three answers above, or a guideline's two, plus **Decide later**. Ask with the session's question tool when it has one, up to four drifts per call; otherwise ask in plain text. When step 3 listed drift, the last question offers to go through it now; a yes runs DRIFT.md's *The review* over it once these answers are applied. No answer is applied before the user gives it.
6. **Apply the answers** as DRIFT.md's *The review* applies them, then run its checks. *Decide later* leaves the row `open` for `/uikit:prototype drift`.
7. **Report** each new drift's final status in one line, and name the design-system components added or extended.

**Completion criterion:** every step of the feature is drawn or linked, every UI need maps to a system component, an earlier flow or a ledger row, every Phase 5 check passes, every new drift the run drew has the user's answer or was replaced with a system component, and the user has the definition path and the route.

## Drift review

The review runs in two places, with one procedure, in [DRIFT.md](DRIFT.md):

- **At the end of every run,** as Phase 7, over the new drift that run drew.
- **On demand,** as `/uikit:prototype drift`, over every open drift across all flows: drift answered *Decide later*, drift already open across several flows, and legacy HTML flows.

1. Tally with `python3 <skill-dir>/scripts/drift-report.py docs/flows`. A run adds one `--file` per flow it drew, and `--new` for its new drift. Each row gives the drift, its class, kind, the flows using it, proposals and statuses.
2. Re-run the reuse test against the current system, then recommend an answer per drift: **one-off**, **fold** into an existing component as a variant, or **promote** to a component; for a guideline, change it or keep the exception.
3. Ask per drift and wait for the user's answers.
4. Apply the answers: a promoted or folded component is authored in the real component set and added to the design-system viewer, the candidate is removed from the dev flow area, the flow's import switches to the system component, and the components table and ledger statuses follow. A one-off stays a candidate. This writes component code, never production pages.

## Invocation variants

| Invocation | Behavior |
|---|---|
| `/uikit:prototype <feature>` | The full workflow for one feature, one flow, ending with the fold-back questions |
| `/uikit:prototype <feature>, <feature>` | One flow per feature, drawn one at a time, with one round of fold-back questions after the last |
| `/uikit:prototype <feature> --system <path>` | That file as the design system |
| `/uikit:prototype update <flow> <change>` | Redraws or adds steps in an existing flow, with the same map, ledger, checks and fold-back questions |
| `/uikit:prototype migrate <flow.html>` | Converts a legacy HTML flow to a definition and a route, then deletes the HTML |
| `/uikit:prototype drift` | The drift review across all flows, for drift still open |

## Tone

Report what you actually drew. If a drift turns out to be taste rather than need, say so and replace it with the system component. If a step was decided on a principle rather than a reference, flag it: it is the row most likely to be wrong. When recommending a fold-back answer, say plainly when a drift is too small to earn a place in the system.
