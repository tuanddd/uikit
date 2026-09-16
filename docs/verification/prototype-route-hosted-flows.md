# Prototype route-hosted flows verification

Date: 2026-09-16
Run: prototype-route-hosted-flows
Lane: normal
Spec: docs/specs/SPEC-004-prototype-route-hosted-flows.md

## Change

`/uikit:prototype` no longer draws a self-contained HTML file that copies the design system's
tokens and component CSS. It now produces a **definition** (`docs/flows/<slug>.json`: the
requirement, steps, why rows, components table and drift ledger) and a **dev route**
(`/uikit/flows/<slug>`) that renders each step from the project's real components. Drift that
needs new UI is a **candidate component** under `<dev>/flows/components/`, imported like any
other and never placed in the production component tree. A promoted candidate is authored in
the real component set and the design-system viewer, and every flow that used it switches its
import.

Files: `SKILL.md`, `FLOW-FILE.md`, `DRIFT.md`, `README.md` rewritten for the new model;
`CRAFT-RULES.md` and `REFERENCE-SOURCES.md` adjusted (the CSS is illustrative; hard-rule
number); `scripts/drift-report.py` reads JSON definitions and legacy HTML files;
`scripts/flow-check.py` added; `scripts/sync-blocks.py` and `templates/flow.html` removed;
`templates/flow.json` and `templates/FlowShell.tsx` added. The plugin README, `/uikit:what` and
`/uikit:implement` follow. Plugin version 0.6.0. The Codex copy
`~/.codex/skills/uikit-prototype` was re-synced.

## Structural validation

`quick_validate.py` (PyYAML in an isolated venv):

| Target | Result |
|---|---|
| `~/.codex/skills/uikit-prototype` | `Skill is valid!` |
| `~/.claude/skills/uikit/skills/prototype` | exits 1 on `disable-model-invocation`, a pre-existing Claude-Code-only key the Codex validator rejects (the same failure exists at HEAD and in the plugin skill's other entries) |
| `~/.claude/skills/uikit/skills/init-design-system` | `Skill is valid!` |

Every relative Markdown link across the plugin resolves. Every edited file has an even number
of ``` fences. The Codex copy differs from the plugin copy only by the intentional naming
(`uikit-prototype`), the `Codex tools` section, the Mobbin tool-discovery prose, the
`$uikit-` command form, `AGENTS.md` in the doc list, and `agents/openai.yaml`; every reference
file and every script is byte-identical.

## flow-check.py

A fixture from `templates/flow.json`, renamed to its slug, passes. A deliberately broken
definition produced 11 errors, all intended: slug/filename mismatch, duplicate step id, a step
number not matching its id, a missing `linkedTo`, a bad `why` confidence, an unknown `from`, a
components row naming a step that does not exist, a bad ledger kind, a bad proposal, and two
ledger classes absent from the components table. A directory with only legacy HTML files is
reported as legacy, not failed.

## drift-report.py

Regression against the SPEC-002 shape: on a directory of legacy HTML flow files, the new script
and the HEAD script produce **identical data** — same rows, kinds, proposals, statuses, file
lists and counts. The only difference is the column header `Files` → `Flows` and the summary
line `flow files` → `flows`, a deliberate rename now that a "flow" is a definition or a legacy
file.

Mixed directory (JSON definitions + legacy HTML) behaviours, all as specified:

| Case | Result |
|---|---|
| No filter | Merges a drift by class across JSON and HTML (same `.drawer` in a definition and two HTML files → one row, 3 flows) |
| `--file v1-01-f.json` | Scopes to that flow; a drift open in two other flows is not new |
| `--file legacy-a.html --new` | Both legacy drifts are new (open in one other flow) |
| `--json` | Emits the rows with sorted `kinds`/`proposals`/`statuses`; the internal `guidelines_open` key is excluded |
| `--file nope.json` | Exit 1, `not a flow in …` |
| `--new` without `--file` | Exit 2, `--new needs at least one --file` |

The open-guideline rule was fixed during review: `--new` used to treat any row whose *kinds*
included `guideline` as new, even when the guideline row itself was not open. It now tests the
guideline's own open status per file.

## Independent review

A read-only reviewer read the rewritten `SKILL.md`, `FLOW-FILE.md`, `DRIFT.md`, `README.md`,
`CRAFT-RULES.md`, `REFERENCE-SOURCES.md`, `templates/flow.json` and both scripts against three
scenarios — a first flow on Next.js, a second flow reusing a candidate, and a `drift` review
promoting one — plus contradiction, leftover-static-HTML, schema-vs-validator, script-output,
cross-check and gating probes.

**Verdict:** all three scenarios initially AMBIGUOUS. The reviewer found no leftover static-HTML
mechanics (`{prefix}` blocks, `sync-blocks.py`, `.frame` CSS, "double-click" all gone), and
confirmed the schema enums agree with the validator and the ledger field shape agrees with the
script. It raised these defects, all repaired:

1. Hard Rule 11 ("never touch the production component tree") contradicted promotion, which
   writes into `src/components/ui/`. Scoped: a **drawing run** never touches production;
   promotion is the one exception.
2. The route segment was named `<feature>` in one place and the slug in another. Unified on the
   definition's `slug` for both the file name and the route segment.
3. A reused candidate's `from` was ambiguous between `candidate:<Name>` and `proposed:<flow>`.
   Simplified to `candidate:<Name>`; the `proposed:` form and its validator branch were removed.
4. The route example did not compile (undefined `<Step1/>`, an aliased import out of `src/`).
   Replaced with a compiling example: screens defined in the file, a relative JSON import with
   a note on `resolveJsonModule`, and `data-dev-surface` on the root.
5. `flow-check.py` required `state`/`route`/`restsOn` even on a linked step, and validated
   fields the schema table did not list. The check now requires those only when `linkedTo` is
   `null`, validates `drawnOn`/`frameWidth`/`linkedTo` format, and the schema table now lists
   every field the validator enforces.
6. `drift-report.py`'s open-guideline rule (above).
7. `CRAFT-RULES.md` prescribed raw CSS while screens are now framework components. Added a note
   that the CSS is illustrative and the constraint and check bind.
8. `REFERENCE-SOURCES.md` cited "Hard Rule 9" for the paywall rule; it is Hard Rule 10.
9. `FLOW-FILE.md` cited the wrong sections for the `<dev>` paths and the static gate. Pointed at
   the `init-design-system` `setup.md` "What lands" and `stacks.md` § 4.
10. Promotion updated "the flow's import" although a candidate is shared. Changed to every flow
    that imports it.
11. `templates/flow.json` baked Astro paths. Generic `src/…` paths now, documented as the
    project's real path.
12. `templates/` claimed a FlowShell reference but had none. Added `templates/FlowShell.tsx`
    (React reference); `FLOW-FILE.md` and the README point at it.

A second targeted re-read confirmed 1–12 held and raised no new contradictions.

## Limitations

- No live `/uikit:prototype` run was attempted: it needs the paid Mobbin MCP, a real browser
  session, and a project to draw into. The skill is an execution contract, not a runtime; it
  was verified through the instructions, two review passes, and the script checks above.
- `flow-check.py` validates definitions, not the route code. A step in the definition with no
  screen, or a component a screen imports but the components table omits, is caught manually in
  Phase 5, not by the script. Stated as a Phase 5 check.
- `templates/FlowShell.tsx` is a React reference. The Svelte and Astro shells are translations
  the skill authors; they were not exercised.
- No promotion was executed end to end: the promote path (author the component, add it to the
  viewer, switch every flow's import, update the ledger) is verified by reading, not by running.
- Legacy HTML flow files are read for the tally and offered a `migrate` path; the migration
  itself was not run against a real project.

## Scope and operational notes

Changes committed to `main` and pushed to `tuanddd/uikit` at the user's request. The Codex copy
lives outside the repository and was updated in place.
