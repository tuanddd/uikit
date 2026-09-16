# Onboarding map verification

Date: 2026-09-16
Run: onboarding-map
Lane: normal
Spec: docs/specs/SPEC-005-onboarding-map.md

## Change

uikit's onboarding is consolidated onto one canonical map and given a deterministic router:

- **`docs/map.md`** added — the single source of routing truth: the main flow
  (`init-design-system` → `prototype` (+ `drift`) → `implement`), a `## Stages` vocabulary, the
  on-ramps table, standalone entries, who-invokes-what, and the `docs/uikit.md` record.
- **`skills/what/SKILL.md`** routes within the map and opens every reply with the fixed line
  `uikit · <stage> · <status>` followed by **Where you are** / **Next** / **Why**.
- **`skills/using-uikit/SKILL.md`** added — model-invoked orientation, gated on a project that
  shows a uikit signal; hands off to `what`.
- **`skills/setup/SKILL.md`** added — explicitly invoked; records a project's approved system,
  stack, and flows once into `docs/uikit.md` plus an `## Design system` block.
- **`skills/prototype/SKILL.md`** and **`skills/implement/SKILL.md`** read `docs/uikit.md` as a
  system source, with `--system` winning.
- **`README.md`**, **`docs/field-guide.html`**, **`.claude-plugin/plugin.json`** point at the map
  and list the new skills. Plugin version 0.7.0.

## Structural validation

A Python check over the plugin (plugin.json parse; per-skill frontmatter with `name` == directory
and a terminated description; every relative Markdown link and HTML `href` resolving; fence
parity):

| Check | Result |
|---|---|
| `plugin.json` parses | pass — `name=uikit`, `version=0.7.0` |
| Frontmatter, all six skills | pass — `name` == directory, descriptions terminated |
| Relative links (`*.md` and `*.html`) | pass — every target resolves |
| Fence parity, every file touched | pass |

Model-invocation flags match the spec AC: `disable-model-invocation` is present on `prototype` and
`setup` and absent on `what`, `implement`, `init-design-system`, and `using-uikit`.

## Single-source check

Searching the plugin for the on-ramps table header (`Your situation` / `User's situation`) returns
only `docs/map.md` and the SPEC-005 prose that names the header — no routing surface restates it.
All five entry points link to the map: `README.md`, `docs/field-guide.html`, and the `what`,
`setup`, and `using-uikit` skills. `docs/map.md` gained a `## Stages` section so the stage
vocabulary the `what` reply and `setup` cite is defined where they claim it is.

## Independent review

A read-only reviewer read every added and changed file against the intent and probed for
contradictions, leftover routing restatements, over-broad model triggering, precedence disputes,
and dangling references.

**Verdict:** the architecture landed, but the first pass was not clean. Sixteen defects were
raised and all sixteen repaired:

1. `README.md` OpenCode section claimed "the four skills"; now names all six.
2. `README.md` command-picker check omitted `/uikit:setup`; added.
3. `README.md` Invocation table omitted `/uikit:setup` and `using-uikit`; added.
4. `README.md` natural-language and `disable-model-invocation` notes were stale; corrected
   (`using-uikit` model-invoked; `setup` and `prototype` explicit-only).
5. `what` said "the four UIkit skills"; now lists all six.
6. Field-guide footer still read "plugin v0.6.0"; bumped to v0.7.0.
7. Field-guide lead said "Three skills" while the plugin ships six; reworded to "Three skills in
   one flow".
8. `setup` cited a stage vocabulary `docs/map.md` did not define; added `## Stages` to the map
   (fixes 8 and 9 together).
9. `what` said it names the stage "from the map's on-ramps"; now "from the map's stages".
10. `what` offered `flow (update)` and `returning` as stages the reply contract forbids; `update`
    is now folded into `flow`, and `returning` names the next unfinished step's stage.
11. `what` recommended `setup` for "no `docs/uikit.md`", which is nearly every repo; narrowed to
    "two or more competing system sources and no record", matching the map and setup's own scope.
12. `using-uikit`'s description triggered on generic UI nouns with no project gate; added a
    "When this applies" section and a signal-scoped description (a `/uikit` route, `docs/flows/`,
    `docs/uikit.md`, or the user naming uikit).
13. `implement` listed `docs/uikit.md` before `--system` and stated no precedence while
    `prototype` said `--system` wins; both now state `--system` → `docs/uikit.md` → repo sources.
14. `what` claimed it never restates the map, then restated it; reworded to "never restates the
    map's on-ramps table" (the per-stage command list remains, by design).
15. SPEC-005 referenced a non-existent `docs/design-record.md`; pointed at its own
    `## Design record` section.
16. This verification file was missing; written.

The reviewer confirmed as correct: the on-ramps table lives only on the map; all relative links
resolve; `plugin.json` parses; frontmatter names match directories; the flags match the AC; fence
counts are even in every touched file; `docs/uikit.md` field names line up between the writer
(`setup`) and the readers (`what`, `prototype`, `implement`); `what`'s read-only rule stays
consistent with recommending `/uikit:setup`; and `setup`'s CLAUDE.md-else-AGENTS.md rule is
unambiguous and non-destructive.

## Limitations

- No live `/uikit:what` or `/uikit:setup` run in a real consumer project. Both skills are
  execution contracts, not runtimes; they were verified through reading, one independent review
  pass with fixes, and the structural checks above.
- `using-uikit` is selected by description matching, whose reliability varies per harness. The
  description is now gated on a project signal, but no harness's matcher was exercised.
- The Codex skill copies under `~/.codex/skills/` were not re-synced; they live outside the
  repository. The README's link instructions pick up the new skills from
  `~/.claude/skills/uikit/skills/*`.
- Two pre-existing verification docs (`prototype-route-hosted-flows.md`,
  `live-design-system-viewer.md`) have an odd number of code-fence markers. They are unchanged by
  this work and left as found.
