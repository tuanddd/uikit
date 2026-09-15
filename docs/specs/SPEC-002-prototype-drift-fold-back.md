# Fold prototype drift back after every run

Lane: normal
Type: spec-feature

## Context

`/uikit:prototype` records drift in each flow file's ledger, but what goes back into
the design system is only decided when the user separately runs
`/uikit:prototype drift`. Nothing prompts that run, so drift piles up open. The user
expects the prototype run itself to ask, drift by drift, whether to fold it back:
minor drift is not worth a system component, while reusable drift should become one
so later flows share it.

Grill: skipped; the request fixes the trigger (the end of every run), the question
(fold back or not, per drift) and the deciding factor (minor versus reusable).

Done = a prototype run that drew new drift ends by asking the user, per new drift
and with a recommended answer, whether it joins the design system, applies the
answers, and leaves deferred rows open for `/uikit:prototype drift`. Drift already
open across several earlier flows is listed in one line, not asked again. A run with
no new drift says so and asks nothing.

## Acceptance criteria

- Phase 7 follows Phase 6 on every drawing invocation (one feature, several, or
  `update`), once per run, after the last file.
- New drift is defined once: open in a file the run drew and open in at most one
  other flow file (a first use, a second use, or a reused one-off), plus every open
  guideline drift in those files. In an `update`, only rows the update added count.
- The tally of new drift comes from `drift-report.py --file … --new`, still counting
  every flow file that uses each drift; an `update` narrows it to the rows the update
  added.
- Every open drift the run's files use is re-checked against the current system.
  Covered drift is replaced in the files the run drew, not asked about.
- Open drift that is not new is listed in one line, and the run offers to review it
  before ending.
- Each question names the drift, its kind, the files using it and the nearest system
  component, and leads with a recommended answer and its reason. The options are
  keep as a one-off, fold into the nearest component, add to the system, and decide
  later; guideline drift gets change the guideline or keep the exception.
- Nothing is applied before the answers; decide later leaves the row open.
- Answers are applied and verified through the existing review procedure, without
  writing production code.
- `/uikit:prototype drift` remains, for drift still open.
- Plugin documentation and the installed Codex copy describe the same behavior.

## Design record

No new runtime, hook or dependency. `drift-report.py` gains two filters: a
repeatable `--file`, and `--new`, which applies the new-drift test so the agent does
not filter by hand. Its JSON output gains an additive `open_in` list; the table
output is unchanged. Phase 7 points at DRIFT.md's review procedure instead of
restating it. The on-demand drift mode stays as the catch-up path for deferred rows,
drift already shared before a run, and older files.

Asking about every open drift a new flow reuses was rejected: in the Wu and Kin flow
files, a single flow reuses 13 drifts that were already open across several flows,
so every run would ask 17 questions and the questions would stop being read.

## Verification

Run `quick_validate.py` on the plugin skill and its Codex copy. Exercise
`drift-report.py` against a real flow directory (no filter as the control, one file,
two files, paths inside and outside the directory, an unknown name) and against a
small fixture covering each new-drift case: first use, second use, a reused one-off,
a guideline shared by several flows, and drift already open in two other flows.
Resolve every relative Markdown reference, and confirm the Codex copy differs from
the plugin copy only by its intentional naming. Have an independent reviewer read
the changed skill against the fold-back scenarios. Record commands, outcomes and
limitations in `docs/verification/prototype-drift-fold-back.md`.

## After state

Every prototype run ends with the fold-back questions for its new drift. Reusable
drift enters the design system on the user's answer, minor drift stays a one-off,
and deferred or long-shared drift stays open for the on-demand review. UIkit is at
0.3.0.
