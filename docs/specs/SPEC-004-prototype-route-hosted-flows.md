# Prototype flows as hosted dev routes

Lane: normal
Type: spec-feature

## Context

`/uikit:prototype` draws each feature as a **self-contained static HTML file** in
`docs/flows/`. The file's screens are plain-CSS redraws of the design system: the
`{prefix}-tokens` block is copied verbatim out of `docs/design-system.html`, and the
`{prefix}-base` block is the system's component CSS copied out and scoped under `.frame`.
Every flow therefore carries a second copy of every component it uses, held in step by
`sync-blocks.py` and a drift ledger.

With SPEC-003 the design system became a **live route** (`/uikit/design-system`) whose
components are real framework code in the project's own stack; the static HTML is now a
fallback. The prototype's copy-from-HTML source is gone or wrong, and for a Tailwind React
project a component has no extractable CSS block at all. The user chose to resolve this by
**hosting the flows as dev routes too**, so the screens a flow shows are the real
components, and the copy that drifts is deleted rather than regenerated.

Grill: ran. Resolved branches — (1) existing-component screens must render the real
components, not redraws; (2) flows move to a dev route `/uikit/flows/<feature>` with the
same dev-surface hygiene as the design-system viewer; (3) a flow's structured record stays a
portable, machine-readable file in `docs/flows/`, separate from the screen code; (4) drift
that needs new UI is authored as a **candidate component** in the dev area, never in
production code; (5) legacy HTML flow files stay readable and are migrated on request.

Done = `/uikit:prototype <feature>` on a React, Astro, or Svelte project produces (1) a flow
definition `docs/flows/<feature>.json` carrying the requirement, steps, decisions, components
and drift ledger, and (2) a dev route `/uikit/flows/<feature>` that renders that definition's
documentation shell and each step's screen from the project's real components, plus any
candidate component the drift needs, and (3) the route hidden outside local and preview. A
screen built from a system component imports that component; nothing redraws it. The drift
ledger still drives the fold-back questions. For a project with no hostable route, the static
HTML page remains the fallback.

## Acceptance criteria

- The static-HTML flow-file model is replaced by a flow **definition** (JSON in
  `docs/flows/`) plus a dev **route** at `/uikit/flows/<feature>`; the static HTML file is a
  fallback for a project with no hostable route.
- Existing-component screens import the real components. No flow file or route carries a
  copied component CSS block, and `sync-blocks.py` is retired.
- The definition is machine-readable and holds: meta (feature, slug, group, requirement and
  its source, frame width), steps (id, number, title, state, route, `Rests on`, linked or
  drawn), the why rows, the components table, and the drift ledger.
- Drift that needs new UI is authored as a candidate component under the dev flow area, shared
  across flows and never placed in the production component tree; the ledger records it.
- `drift-report.py` reads the new definitions and still reads legacy HTML flow files, so a
  project mid-migration keeps one tally.
- A check script validates every definition (unique step ids, known `from` sources, valid
  ledger kinds/statuses, steps referenced by the components table exist) and replaces
  `sync-blocks.py --check` in the verify phase.
- The route is dev-only: env-gated, unlinked, `noindex`, `robots.txt`-disallowed, off the
  sitemap, `data-dev-surface`.
- `/uikit:prototype drift` and Phase 7 keep working on the new ledger; a promoted or folded
  drift becomes a real component in the project's stack and the design-system viewer, and the
  flow's import switches to it.
- `/uikit:implement` accepts a flow definition and its route, reads the screens from the real
  components, and still accepts a legacy HTML flow file.
- The skill README, the plugin README and `/uikit:what` describe the new model consistently,
  and the installed Codex copy matches the plugin copy except for its naming.

## Design record

**Why a route and a definition, not a richer HTML file.** The point is that an
existing-component screen is the component. A route composes the real components; a JSON
definition in `docs/flows/` keeps the portable, diffable record (requirement, steps,
decisions, ledger) that the route renders and the scripts read. The record is not the
renderer, so neither has to imitate the other.

**Why JSON for the definition.** `drift-report.py` already parses the ledger out of the flow
file. Parsing a framework module is fragile; parsing JSON is not, and it works across
TypeScript, Svelte and Astro imports. The ledger is the machine-readable core; the shell is
data too, so one file serves rendering and tooling.

**Why candidate components in a dev area.** A flow that needs new UI must show it, and a
component that does not exist cannot be imported. Candidates live under the dev flow area
(`<dev>/flows/components/`), are shared between flows, and are not production code. Promotion
moves one into the real component set and the viewer.

**Why the static HTML survives.** A project without a hostable route cannot render a flow
component, so the HTML page remains for that case — the same fallback rule as the design
system (SPEC-003).

**Why `sync-blocks.py` is retired.** It existed to keep one CSS block identical across files.
With no CSS blocks and a shared `FlowShell` component plus shared candidate components, the
thing it protected is gone. A `flow-check.py` takes its place in the verify phase, validating
the definitions instead of copying blocks.

**Files.** `SKILL.md` rewritten around the definition, the route, and candidates;
`FLOW-FILE.md` becomes the definition schema and the route/`FlowShell` anatomy;
`DRIFT.md` retargets drift CSS to candidate components and promotion to real components;
`drift-report.py` reads JSON and legacy HTML; `flow-check.py` added; `sync-blocks.py`
removed; `templates/` gains a definition template and a `FlowShell` reference; `README.md`,
the plugin README, `/uikit:what` and `/uikit:implement` follow.

## Verification

Validate every definition with `flow-check.py` against a fixture set (a valid definition, a
duplicate step id, an unknown `from`, a bad ledger kind, a components row naming a step that
does not exist). Exercise `drift-report.py` over a mixed directory (new JSON definitions and
legacy HTML files), with no filter, `--file`, `--new`, and `--json`, and confirm the tally is
unchanged against the SPEC-002 fixtures. Resolve every relative Markdown link across the
plugin. Run `quick_validate.py` on the plugin skill and the Codex copy in an isolated venv.
Have an independent reviewer read the rewritten `SKILL.md`, `FLOW-FILE.md`, `DRIFT.md`, and
`README.md` against three scenarios — a first flow on a Next.js project, a second flow
reusing a candidate, and a `drift` review promoting a candidate — and confirm each resolves to
one path. Record commands, outcomes and limitations in
`docs/verification/prototype-route-hosted-flows.md`.

## After state

`/uikit:prototype` draws a feature as a definition plus a dev route that renders the real
components, with candidate drift components in a dev area and the ledger driving the
fold-back questions. Legacy HTML flow files still read. UIkit is at 0.6.0.
