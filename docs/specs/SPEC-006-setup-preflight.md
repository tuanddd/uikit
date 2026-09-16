# Setup is the pre-flight; init consumes its record

Lane: bug
Type: bug

## Context

SPEC-005 added `/uikit:setup`, which writes an `## Design system` block into `AGENTS.md`/`CLAUDE.md`
and a `docs/uikit.md` record naming an "Approved source". It also demoted setup to a rarely-needed
standalone, and left the order between setup and `/uikit:init-design-system` undefined.

Run against a real repo, the two skills collide: `/uikit:init-design-system` reads `AGENTS.md`
(with the block setup just wrote) and any `DESIGN.md`, and — because its Stance treats found files
as design *preferences* — it stops and asks the user whether to follow "the choices in
AGENTS.md/DESIGN.md" or adopt the skill defaults. Nothing told it that the record is a pointer, not
a preference set.

Grill: skipped. The one open decision — the order between the skills — was put to the user, who
chose **setup → init-design-system → prototype**. The rest follows from that.

Done = on a fresh project, running the ideal order setup → init-design-system → prototype never
raises the either/or question: `/uikit:setup` records the approved source (or `none yet`) as a
pointer in `docs/uikit.md` and an `## uikit` block, and `/uikit:init-design-system` reads that
record as its harvest input, applies the defaults only to the gaps, and never presents the record,
`AGENTS.md`, `DESIGN.md`, and the skill defaults as a choice.

## Acceptance criteria

- The order **setup → init-design-system → prototype** is stated consistently in `docs/map.md`
  (main flow, stages, standalone), `README.md`, `skills/using-uikit/SKILL.md`, and
  `skills/what/SKILL.md`.
- `/uikit:setup` frames itself as the pre-flight before `init-design-system`; its Section A records
  `none yet` and recommends init when no source exists, rather than inventing one.
- The block setup writes is renamed `## uikit` and marked "a pointer, not tokens"; the
  `docs/uikit.md` record says the same. No skill writes an `## Design system` block.
- `/uikit:init-design-system` Step 1 reads `docs/uikit.md` first, takes its Approved source as the
  harvest input, treats `none yet` as "copy what exists, derive the rest from defaults", and
  explicitly forbids asking the user to choose between the record, `AGENTS.md`, `DESIGN.md`, and
  the skill defaults. Its Stance states the record is not a preference.
- `docs/map.md`'s record section lists `init-design-system` among the readers and states the record
  holds pointers and choices, not tokens.
- SPEC-005 and its verification record are left as written (dated records); this spec supersedes
  their `## Design system` block name and their setup-is-standalone ordering.

## Design record

**Why setup stays a separate skill and runs first.** The user's order makes setup the single place
where "which existing file wins" is decided, before init harvests. Folding it into init
(SPEC-005's option 3) would lose the pre-flight for a repo that never runs init; keeping it
standalone before init preserves that, at the cost of the two skills sharing one subject — which
this change resolves by making the record a pointer, not a source of design values.

**Why rename the block.** `## Design system` named the block after the very thing
`init-design-system` creates, so both a human and an agent read it as the system itself. `## uikit`
names it for what it is: this plugin's record.

**Why init must not ask.** The either/or question is init guessing at something setup already
answered. Removing the guess is the fix; the fallback (no record, competing sources) is to ask
once or recommend `/uikit:setup`, not to re-ask every source it finds.

**Files.** `skills/setup/SKILL.md`, `skills/init-design-system/SKILL.md`, `skills/what/SKILL.md`,
`skills/using-uikit/SKILL.md`, `docs/map.md`, `README.md`, `docs/field-guide.html`.

## Verification

Run the structural checklist over the plugin (plugin.json parses; frontmatter `name` matches each
directory; every relative Markdown link and HTML `href` resolves; fence parity on the touched
files). Confirm by search that no `## Design system` block remains except the `docs/uikit.md`
record's own section and the two dated SPEC-005 files; that `docs/uikit.md` is named in
`init-design-system`, `what`, `prototype`, and `implement`; and that `map.md`, `README.md`,
`what`, and `using-uikit` all state the setup → init order. Record commands, outcomes, and
limitations in `docs/verification/setup-preflight.md`.

## After state

Setup is the documented pre-flight before `init-design-system`, its output is an unambiguous
pointer (`## uikit` + `docs/uikit.md`), and init harvests from the recorded source without asking
the repo-or-defaults question. Plugin 0.7.0 (no version bump; a fix within the cycle).
