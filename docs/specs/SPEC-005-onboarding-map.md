# Onboarding: one map, one router, one record

Lane: normal
Type: spec-feature

## Context

uikit's onboarding was spread across three artifacts that each restated the same routing:
`README.md` ("Choose your starting point" table), the `what` skill's "Choose the next action"
table, and `docs/field-guide.html` ("Run it in this order"). Nothing said which was canonical,
so they could drift; `field-guide.html` was linked from nowhere; and `/uikit:what` described its
reply as prose plus an example rather than a fixed shape, so every invocation re-rendered the
same meaning in different words. Two reference implementations were studied: `obra/superpowers`
(an always-on `SessionStart` bootstrap that teaches the agent its skills) and `mattpocock/skills`
(a per-repo `setup` skill that records config, plus an `ask-matt` router written as a
situation-keyed map). The lesson taken from both: determinism comes from a fixed vocabulary and a
single map, not from a rigid template; and onboarding is better seeded before the user asks.

Grill: skipped. The four changes were agreed in the conversation that opened this work (canonical
map, deterministic reply contract, model-invoked orientation, per-repo setup); no branch was left
unresolved, and the decisions are recorded in this spec's `## Design record` section.

Done = a user who has just installed uikit, and one returning mid-project, each get the same
routing answer: `docs/map.md` is the single canonical map; `/uikit:what` opens every reply with the
fixed stage line and three named fields; a model-invoked `using-uikit` skill orients the agent when
a session touches UI work; and `/uikit:setup` records a project's system/stack/flows once into
`docs/uikit.md`, which `what`, `prototype`, and `implement` read before re-deriving them. README,
the field guide, and the `what` skill all point at the map instead of restating it.

## Acceptance criteria

- `docs/map.md` exists and is the only place the on-ramps routing table lives. It carries the
  main flow (`init-design-system` → `prototype` (+ `drift`) → `implement`), the on-ramps table,
  standalone entries, the who-invokes-what axis, and the `docs/uikit.md` record.
- `README.md`, `docs/field-guide.html`, `skills/what`, `skills/setup`, and `skills/using-uikit`
  each link to `docs/map.md`; none restates the on-ramps table.
- `skills/what/SKILL.md` specifies a fixed reply: the line `uikit · <stage> · <status>` with
  `<stage>` drawn from `setup | system | flow | drift | implement | unknown`, then **Where you
  are**, **Next**, **Why**, with the example rewritten to that exact shape.
- `skills/using-uikit/SKILL.md` is model-invoked (`disable-model-invocation` absent), states the
  compact map, gates on UI/design-system language, and hands off to `what` rather than routing or
  building itself.
- `skills/setup/SKILL.md` is explicitly invoked (`disable-model-invocation: true`); it explores,
  asks one section at a time with a recommended answer, confirms, then writes `docs/uikit.md` and
  an `## Design system` block into the existing `CLAUDE.md` (else `AGENTS.md`), never both and
  never overwriting surrounding edits.
- `skills/prototype` and `skills/implement` read `docs/uikit.md` as the first system source when
  it exists.
- `plugin.json` version is `0.7.0`; its description names the map, the router, and setup. The
  README skill table, requirements, and layout include `setup` and `using-uikit`.
- The plugin still has valid `plugin.json`, complete/parsable frontmatter per skill, resolving
  relative Markdown links, and even code fences in every file this change touches.

## Design record

**Why a file, not the skill, is canonical.** A skill that restates the map cannot be the map:
the README and field guide would still diverge from it. `docs/map.md` is readable by a human at
install time and by the `what` skill at runtime, so there is one text to change.

**Why the reply is a template and not just an example.** The complaint was that same-meaning
answers read differently each run. Naming the stage forces the model to commit to a routing
decision, and a literal three-field template removes the re-rendering freedom prose leaves.

**Why `using-uikit` and not a SessionStart hook.** The hook is the superpowers mechanism, but it
is Claude-Code-only and uikit advertises OpenCode, Codex, and generic SKILL.md readers. A
model-invoked skill carries the same orientation on every harness, at the cost of relying on
description matching rather than guaranteed injection — an acceptable trade at four skills.

**Why setup is separate from what.** `what` is read-only and stateless by contract, so it cannot
record anything. Setup writes; `what` recommends it. Keeping the two apart preserves `what`'s
"guidance, changes nothing" guarantee.

**Files.** `docs/map.md` added; `skills/setup/SKILL.md` and `skills/using-uikit/SKILL.md` added;
`skills/what/SKILL.md` routes from the map and fixes the reply shape; `skills/prototype/SKILL.md`
and `skills/implement/SKILL.md` read `docs/uikit.md`; `README.md`, `docs/field-guide.html`, and
`.claude-plugin/plugin.json` follow.

## Verification

Run the structural checklist over the plugin: `plugin.json` parses; every `skills/*/SKILL.md` has
frontmatter whose `name` matches its directory and whose description is not unterminated; every
relative Markdown link resolves (with the two pre-existing odd-fence verification docs noted, not
as this change's failures); every file this change touches has an even fence count. Confirm with a
search that the on-ramps table (`Your situation`) appears only in `docs/map.md`, that all five
entry points link to `docs/map.md`, and that `disable-model-invocation` is present on `prototype`
and `setup` and absent on `what`, `implement`, `init-design-system`, and `using-uikit`. Record
commands, outcomes, and limitations in `docs/verification/onboarding-map.md`.

## After state

A new or returning user has one map (`docs/map.md`), one router (`/uikit:what`) with a fixed reply
shape, a model-invoked orientation skill, and an optional per-repo `/uikit:setup` whose record the
other skills read. UIkit is at 0.7.0.
