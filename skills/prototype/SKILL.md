---
name: prototype
description: Prototype a feature as one or more self-contained HTML flow files drawn on the project's design system (docs/design-system.html, the output of /uikit:init-design-system) — every step of the flow as a screen, the decisions and the shipped products they rest on, and a ledger of where the drawing drifts from the system. Researches flows through the paid Mobbin MCP and checks it is connected before starting. Only runs when explicitly invoked; it does not trigger on its own.
disable-model-invocation: true
---

# Prototype

Take a feature the user asks for, learn how shipped products solved its flow, and draw it start to end as a static HTML flow file on top of the project's design system. The file is what a build of the feature starts from, and what the next feature is drawn against.

**Input:** a feature request, the project's design system, and any flow files already drawn.
**Output:** one self-contained HTML file per feature in `docs/flows/`, in the same format as the files already there.

You are the designer, the researcher and the builder. Nobody will ask how step 2 works, what the empty state offers or where the price sits, so ask yourself, and answer from evidence.

`<skill-dir>` below is the directory this file lives in (`~/.claude/skills/uikit/skills/prototype` for a skills-dir install).

## Operating posture

Three failure modes to design against:

- **Building from taste.** Nearly every step of every flow has been solved by a shipped product. Phase 3 goes and looks. Skip it and the file is an opinion.
- **Reinventing the wheel.** Drawing a Modal while the system has a Dialog, a custom dropdown while it has a Select, a hand-rolled toast while it has an Alert. The system exists so nobody redraws what is already solved. A near-copy of a system component is the most expensive drift there is: it looks like a new component and is not one.
- **Silent drift.** Departing from the system without writing it down. Drift is allowed. Drift nobody recorded is how the next feature stops matching this one.

## The design system is the base, not a cage

`docs/design-system.html` is where every screen starts. It is not a rulebook that forbids whatever it does not show. Every UI need on a screen goes through this lookup, in order:

| The need | Do |
|---|---|
| A system component covers it, as-is or with a variant it already ships | Use it: its class, its markup, its variants. The content changes; the component does not |
| An earlier flow file already proposed a component for it | Reuse that one, under the same name and class; the second use is evidence for promoting it |
| Nothing covers it, or the nearest component cannot carry what this flow needs | Drift: draw what the flow needs from the system's tokens, and record it in the ledger |

Drift is for what the narrative, the flow or the requirement genuinely asks for: a drawer the page must stay visible beside, a denser row where eight dates are compared, two primary actions on the one screen where both are equally the point. It is not for a component you would have styled differently.

**The reuse test, before any drift:** name the nearest system component and the concrete reason it cannot carry this need: a state it lacks, content it cannot hold, a layout the flow requires. If the only reason is how it looks, it is not drift. Use the component.

**Tokens do not drift.** Colour, typeface, radius, shadow and spacing come from the system. A token that does not exist is a question for the user, asked before it is drawn.

Every drift gets a ledger row with its kind, the nearest system component, why it departs, and a first proposal: `promote` (it would serve other features) or `one-off` (it belongs to this feature's story). Every run then ends by asking the user, one question per new drift it drew, whether that drift goes back into the design system (Phase 7). Reusable drift becomes a system component, so future runs reuse it instead of drifting again; minor drift stays a one-off in its flow. Ledger format, kinds and the review: [DRIFT.md](DRIFT.md).

## Hard rules

1. **Check Mobbin before anything else.** It is a paid service. The user hears whether it is connected before any research starts.
2. **Reuse before drift.** A drift that fails the reuse test is a defect, not a design choice.
3. **Record every drift.** A class on a screen that is neither in the system nor in the ledger is a defect.
4. **No new tokens without asking.** Drift happens in components, variants, details and guidelines, never in the token set.
5. **Each file is self-contained.** It opens by double-click from disk: no build, no server, no data loading. Its only external request is the web-font stylesheet; everything else is inline.
6. **Screens are static, with mock values.** Anything the flow does not demonstrate uses the fixed mock values in the flows README. States (validation, empty, error, sent) are drawn as their own steps, never toggled by script.
7. **Shared style blocks are identical in every flow file.** A change to one goes into every file at once, through `scripts/sync-blocks.py`. Retyping a block per file is how drift starts.
8. **Never load the design-system page whole.** It runs to hundreds of KB. Pull the section, class list or component you need with `grep` and `sed`.
9. **Never bypass a paywall, blur or login wall.** In the user's real browser, open only your own tab and close only what you opened.
10. **Never touch production code.** A run writes to `docs/flows/` only. The design system page changes only on the user's answer, in Phase 7 or a drift review.
11. **Ask before the run ends.** A run that drew new drift, as Phase 7 defines it, ends with the fold-back questions. It never folds drift into the system on its own, and never ends without asking.

## Workflow

### Phase 0 — Preflight

**1. Mobbin, paid.** Load the tools before any other work:

```
ToolSearch("+mobbin")
```

- **Tools load:** tell the user in one line, then continue. *"Mobbin MCP is connected. It is a paid service; this run uses it for the reference lookups, about one search per step."* The first lookup doubles as the auth check: if it fails with an auth or quota error, stop and say so.
- **No tools:** stop and ask. *"Mobbin MCP is not connected. It comes with a paid Mobbin plan and is where this skill finds how shipped products solved each step. Connect it and rerun, or continue on free sources, where more decisions rest on a principle instead of a reference."* Wait for the answer.

**2. The design system.** Look for `docs/design-system.html` first, the page `/uikit:init-design-system` writes. Then `docs/**/design-system*.html`, `**/style-guide.html`, and machine-readable tokens (`tokens.json`, `tailwind.config.*`, CSS custom properties). A path passed with `--system` wins.

- One found: it is the base.
- Several found: ask which.
- None found: say so and recommend `/uikit:init-design-system` first. If the user goes ahead anyway, distill a token block from whatever tokens the repo has; every component is then drift, and the ledger says so.

**3. Flow files already drawn.** Look for `docs/flows/README.md` and `docs/flows/*.html`.

- Found: they are the baseline. Their shared style blocks, mock values, cast, naming and sections are reused as they are.
- None: this run creates `docs/flows/`, its README, and the shared blocks from [templates/flow.html](templates/flow.html).

**4. Domain docs.** Product, audience and their state on arrival, the one question every screen answers, voice rules, hard constraints, and the roadmap or feature list the request belongs to. Search `README.md`, `PROJECT.md`, `PRODUCT.md`, `CLAUDE.md`, `positioning.md`, `docs/brand/*`, `docs/FEATURES.md`.

State what you found in one line each, then continue. Stop only for the Mobbin answer, a missing design system, or two candidates that conflict.

### Phase 1 — Map the feature's flow

1. **Name the feature and its requirement.** Quote the roadmap or feature-list line it implements; with none, quote the user's ask.
2. **Split into files.** One file per feature. A request spanning several features becomes several files, drawn one at a time. Confirm the split only when the boundary is genuinely unclear.
3. **List the steps, start to end.** One row per screen: title, state, route. The states that belong to this flow (validation, empty, error, sent, too many results) are steps of their own.
4. **Link, do not redraw.** A step another flow file already draws is linked (`other-file.html#step-3`), not drawn again.
5. **Pick the closest file.** The existing flow file sharing the most screens or components with this feature. The new file starts as a copy of it; with no flow files yet, from the template.

### Phase 2 — Map every need to the system

Write `component-map.md` in the scratchpad, one row per UI need across all steps:

```
| Need | Covered by | Source | Reuse test |
|---|---|---|---|
| Confirm before withdrawing an inquiry | Dialog `.dialog` | design system | — |
| Channel rows with an action | Channel `.channel` | proposed in v1-13-direct-contact.html | — |
| Panel from the right, page visible beside it | Drawer `.drawer` | drift: component | Dialog centres over a scrim; the listing must stay visible while the visitor writes |
```

Read the inventory from the files, not from memory: the tab names and classes in the design-system page's components section, each component's variants, and the product block of the closest flow file for what earlier flows proposed. Run the reuse test on every drift row before drawing it. Details and a table of the usual reinventions: [DRIFT.md](DRIFT.md).

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

### Phase 4 — Draw the flow file

**Read [FLOW-FILE.md](FLOW-FILE.md) and [CRAFT-RULES.md](CRAFT-RULES.md) before writing markup.** The first is the file's anatomy; the second is eight layout constraints every screen is checked against.

1. **Copy the closest file,** or the template, to the new file name. Keep the shared style blocks exactly as they are.
2. **Draw each step as a board:** number, title, state and route; one *Rests on* line from the bank; the screen at the frame width the other flow files use.
3. **Build every screen from the component map.** System components with their own classes and markup; proposed components from the product block; drift CSS from system tokens only, placed where its proposal points: `promote` into the shared product block, `one-off` into this file's `flow-local` block.
4. **Real content, in the project's voice.** Everything the flow does not demonstrate takes the fixed mock values from the flows README. A value this flow needs that the README lacks is added to the README first, so the next file uses the same one.
5. **Fill the sections:** the flow list, the steps, *Why it looks like this* from the bank, and *Building on it* with routes, mock values, the Components table and the drift ledger.
6. **Propagate shared-block changes.** When the product block changed, copy it into every flow file:

   ```bash
   python3 <skill-dir>/scripts/sync-blocks.py docs/flows --from docs/flows/<new-file>.html --block <prefix>-product
   ```

7. **Wire it in.** Add the index row to `docs/flows/README.md`, and point the previous and next files' pagers at the new file.

### Phase 5 — Verify

Run every check before reporting. A breach is fixed, not reported as a note.

1. **Self-contained:** the only `<link rel="stylesheet">` is the web font, there is no `<script src>`, and the file renders from `file://`.
2. **Blocks in sync:** `python3 <skill-dir>/scripts/sync-blocks.py docs/flows --from docs/flows/<new-file>.html --check` exits 0.
3. **Anchors:** every flow-list link, pager link and cross-file step link resolves.
4. **Reuse:** every drift row passes the reuse test on a second read, and every class used inside a frame is defined in the tokens, base, product or local block and listed in the Components table.
5. **Ledger:** `python3 <skill-dir>/scripts/drift-report.py docs/flows` lists every drift this file introduced or reused, and nothing it did not.
6. **Craft:** screenshot the boards with the browser tool the session has (`playwright-cli`, `browser-harness`, or headless Chrome) and run the eight checks at the end of `CRAFT-RULES.md`.
7. **No sideways scroll:** the page body does not scroll horizontally at 400px or 1400px; screens scroll inside their own stage.

### Phase 6 — Report

1. The file paths, and how to open them: `open docs/flows/<file>.html`.
2. The steps drawn, and which steps link to other files instead.
3. The reuse tally: components from the system, components reused from earlier flows, drifts.
4. The drift introduced: each one, its kind and its proposal.
5. The `principle, not reference` rows, named as the likeliest to be wrong.
6. Which research route ran: Mobbin MCP, the Mobbin site, or free sources.

After the last file's report, go to Phase 7.

### Phase 7 — Fold drift back

Runs automatically at the end of every run that draws: one feature, several features, or an `update`. With several features it runs once, after the last file's report, over every file the run drew, so a drift two of them share shows up as shared. The procedure is DRIFT.md's *The review*, scoped to this run.

**New drift** is what this phase asks about:

- a drift open in a file this run drew and open in at most one other flow file. That covers a drift no other flow has, its second use, and a drift an earlier flow kept as a one-off that this run reused;
- every open `guideline` drift in those files, however many flows share it, since keeping an exception is each flow's own call.

In an `update`, only the ledger rows the update added can be new drift, under the same test.

1. **Tally the files this run drew,** one `--file` per file: every open drift they use, then the new drift among them.

   ```bash
   python3 <skill-dir>/scripts/drift-report.py docs/flows --file <first-file>.html --file <second-file>.html
   python3 <skill-dir>/scripts/drift-report.py docs/flows --file <first-file>.html --file <second-file>.html --new
   ```

   Each row still counts every flow file that uses the drift.
2. **Re-run the reuse test** on every open drift in the first tally, new or not. A drift the system now covers is replaced, not asked about: swap in the system component's markup, remove the drift's CSS and ledger rows, set its `From` in the Components table to `docs/design-system.html`, run DRIFT.md's checks, and report it. A new drift is replaced in every file that uses it; any other covered drift is replaced in the files this run drew, and named for `/uikit:prototype drift` to replace in the rest.
3. **List the open drift that is not new in one line,** with its count: drift already open across two or more other flows and, in an `update`, rows kept from before the update, once the `--new` tally is narrowed to the rows the update added. With no new drift left, say *"No new drift in this run, nothing to fold back."*, offer to go through the listed drift now, and end the run unless the user says yes.
4. **Recommend an answer per new drift,** taking the first that fits, with a one-line reason:

   | Answer | Recommend when |
   |---|---|
   | **Keep as a one-off** (`one-off`) | Used by one flow file, and either a `detail` or tied to that feature's story. Too small or too specific to earn a place in the system |
   | **Fold into the nearest component** (`fold`) | A system component nearly covers it; it becomes a variant of that component |
   | **Add to the system** (`promote`) | Used by two or more flow files, or its anatomy carries nothing specific to this feature, and no system component covers it with a variant |

   A drift an earlier flow kept as a one-off is now used twice: say so, since that is the reason to reconsider it. A `guideline` drift has two answers of its own: **Change the guideline** in the system, or **Keep as this flow's exception**.
5. **Ask, and wait.** One question per new drift: its name and class, its kind, the files using it, the nearest system component, and the recommended answer first with its reason. The options are the three answers above, or a guideline's two, plus **Decide later**. Ask with the session's question tool when it has one, up to four drifts per call; otherwise ask in plain text. When step 3 listed drift, the last question offers to go through it now; a yes runs DRIFT.md's *The review* over it once these answers are applied. No answer is applied before the user gives it.
6. **Apply the answers** as DRIFT.md's *The review* applies them, then run its checks. *Decide later* leaves the row `open` for `/uikit:prototype drift`.
7. **Report** each new drift's final status in one line, and name the design-system components added or extended.

**Completion criterion:** every step of the feature is drawn or linked, every UI need maps to the system, an earlier flow or a ledger row, every Phase 5 check passes, every new drift the run drew has the user's answer or was replaced with a system component, and the user has the paths.

## Drift review

The review runs in two places, with one procedure, in [DRIFT.md](DRIFT.md):

- **At the end of every run,** as Phase 7, over the new drift that run drew.
- **On demand,** as `/uikit:prototype drift`, over every open drift across all flow files: drift answered *Decide later*, drift already open across several flows, and files drawn before Phase 7 existed.

1. Tally with `python3 <skill-dir>/scripts/drift-report.py docs/flows`. A run adds one `--file` per file it drew, and `--new` for its new drift. Each row gives the drift, its class, kind, the files using it, proposals and statuses.
2. Re-run the reuse test against the current system, then recommend an answer per drift: **one-off**, **fold** into an existing component as a variant, or **promote** to a component; for a guideline, change it or keep the exception.
3. Ask per drift and wait for the user's answers.
4. Apply the answers: promoted and folded components go into `docs/design-system.html` under `/uikit:init-design-system`'s component and page rules, and their CSS moves from the product block to the base block in every flow file; one-offs move to their file's `flow-local` block. Ledger statuses update to match.

## Invocation variants

| Invocation | Behavior |
|---|---|
| `/uikit:prototype <feature>` | The full workflow for one feature, one flow file, ending with the fold-back questions |
| `/uikit:prototype <feature>, <feature>` | One file per feature, drawn one at a time, with one round of fold-back questions after the last |
| `/uikit:prototype <feature> --system <path>` | That file as the design system |
| `/uikit:prototype update <flow-file> <change>` | Redraws or adds steps in an existing flow file, with the same map, ledger, checks and fold-back questions |
| `/uikit:prototype drift` | The drift review across all flow files, for drift still open |

## Tone

Report what you actually drew. If a drift turns out to be taste rather than need, say so and redraw it with the system component. If a step was decided on a principle rather than a reference, flag it: it is the row most likely to be wrong. When recommending a fold-back answer, say plainly when a drift is too small to earn a place in the system.
