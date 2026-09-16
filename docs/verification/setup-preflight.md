# Setup pre-flight verification

Date: 2026-09-16
Run: setup-preflight
Lane: bug
Spec: docs/specs/SPEC-006-setup-preflight.md

## Change

`/uikit:setup` and `/uikit:init-design-system` no longer collide. The order is now explicit —
**setup → init-design-system → prototype** — and setup's output is an unambiguous pointer that
init consumes as input rather than weighing against the skill defaults.

- `skills/setup/SKILL.md` frames itself as the pre-flight before `init-design-system`; Section A
  records `none yet` and recommends init when no source exists; the `AGENTS.md`/`CLAUDE.md` block
  is renamed `## uikit` and marked "a pointer, not tokens"; the `docs/uikit.md` template says the
  same; the Done step names init (or prototype, if a system exists) as the next step.
- `skills/init-design-system/SKILL.md` reads `docs/uikit.md` first in Step 1, takes its Approved
  source as the harvest input, treats `none yet` as "copy what exists, derive the rest from
  defaults", and states it must never ask the user to choose between the record, `AGENTS.md`,
  `DESIGN.md`, and the defaults. Its Stance adds "the record is not a preference".
- `docs/map.md` shows the main flow as step 0 setup → step 1 system → step 2 flow → step 3
  implement, lists `init-design-system` among the record's readers, and states the record holds
  pointers and choices, not tokens.
- `README.md`, `skills/what/SKILL.md`, and `skills/using-uikit/SKILL.md` state the same order;
  `what`'s setup bullet explains it feeds init.

## Structural validation

| Check | Result |
|---|---|
| `plugin.json` parses | pass — `name=uikit`, `version=0.7.0` |
| Frontmatter, all six skills | pass — `name` == directory |
| Relative links (`*.md`, `*.html`) | pass — every target resolves |
| Fence parity, touched files | pass |

## Collision checks

Searching the plugin for `## Design system`:

| Location | Kind | Disposition |
|---|---|---|
| `skills/setup/SKILL.md:113` | the `docs/uikit.md` **record's own section**, inside the template | intended |
| `docs/specs/SPEC-005-*.md`, `docs/verification/onboarding-map.md` | dated records of the prior change | left as written |
| `docs/specs/SPEC-006-*.md` | this change's references to the old name | intended |

No skill writes an `## Design system` block. `/uikit:setup` writes `## uikit`.

`docs/uikit.md` is named by every skill that must respect the record: `init-design-system`, `what`,
`prototype`, `implement`, `using-uikit`, and `setup` itself. `init-design-system` carries the
explicit prohibition: "Never ask the user to choose between the record, `AGENTS.md`, `DESIGN.md`,
and the skill defaults" (`skills/init-design-system/SKILL.md:117`).

The order **setup → init-design-system → prototype** is stated at each entry point:
`docs/map.md` (main flow step 0→1, stages table, standalone), `README.md` (skill table and "Choose
your starting point"), `skills/what/SKILL.md` ("Have a design system before the first flow"), and
`skills/using-uikit/SKILL.md` (the compact map, 0→1→2→3).

## Limitations

- No live `setup → init-design-system` run against a real repo. Both skills are execution
  contracts; the fix is verified by reading, the targeted collision checks above, and the
  structural pass.
- SPEC-005 and its verification record still describe the `## Design system` block name and
  setup-as-standalone ordering. They are dated records and were not rewritten; SPEC-006 supersedes
  them.
- Plugin version stays 0.7.0: this is a fix within the cycle, not a new feature surface.
