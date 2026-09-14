# Implement skill verification

Date: 2026-09-15
Run: implement-flow-skill
Lane: normal
Spec: docs/specs/SPEC-001-implement-flow-skill.md

## Change

Added `skills/implement/SKILL.md`, updated plugin discovery documentation, and
bumped UIkit to 0.2.0. Installed the equivalent Codex skill in
`~/.codex/skills/uikit-implement`, with runtime-specific invocation names and
relative references. Existing initialization and prototype skills were preserved.

The implementation contract requires complete flow/state mapping, native stack
adaptation, approved component/token reuse, and zero unresolved drift. It expressly
rejects prototype one-offs as production permission and distinguishes system-safe
composition from new variants. It reuses the existing craft references without
running initialization or applying their conflicting stylistic defaults.

## Structural validation

Commands (each exited 0):

```sh
uv run --with pyyaml python /Users/vincent/.codex/skills/.system/skill-creator/scripts/quick_validate.py /Users/vincent/.claude/skills/uikit/skills/implement
uv run --with pyyaml python /Users/vincent/.codex/skills/.system/skill-creator/scripts/quick_validate.py /Users/vincent/.codex/skills/uikit-implement
uv run --with pyyaml python /Users/vincent/.codex/skills/.system/skill-creator/scripts/generate_openai_yaml.py /Users/vincent/.codex/skills/uikit-implement --interface 'display_name=UIkit Implement' --interface 'short_description=Build HTML feature flows with zero design-system drift' --interface 'default_prompt=Use $uikit-implement to implement the supplied HTML flow in this project using its existing stack and approved design system.'
```

An inline Python check also exited 0 after parsing plugin JSON, checking the name
and version, discovering all three skill directories, resolving every Markdown
reference in both new skill copies, and comparing their full text after normalizing
the intentional naming/path differences.

The first direct Python validator attempt failed because that interpreter lacked
PyYAML. Running the same validator with the isolated `uv --with pyyaml` dependency
resolved the environment issue; no project dependency was added.

## Independent review

An independent explorer read the skill against four scenarios:

- Astro, Tabler, and locked hex tokens remain unchanged despite initialization's
  React, HugeIcons, and OKLCH defaults.
- An allegedly promoted non-modal drawer absent from the system cannot be replaced
  with a modal Dialog when the background must remain usable; dependent work blocks.
- Ordinary HTML, globs, and cross-file steps are supported without requiring UIkit
  markup, copying the documentation shell, or rebuilding unrelated features.
- An inaccessible locked color combination is resolved through approved usage or
  raised as a system gap; neither new colors nor inaccessible completion are allowed.

The review identified a verification gap: contrast measurement was only implicit.
The skill now explicitly requires measuring rendered text/control/state contrast
and following the system-gap rule when approved usage cannot resolve a failure.

## Behavioral evaluation

An independent worker executed the actual skill against a temporary native
JavaScript project with an HTML profile-editing flow, three snapshots of one route,
approved hex tokens, existing button primitives, and a real localStorage service.
The request was `/uikit:implement docs/flows/profile.html`, with no hints about the
expected substitutions. It implemented the route, dialog, validation, cancel/back,
real saving, pending protection, failure/retry, and success announcements.

The worker detected an unlisted magenta button in the input and substituted the
approved primary button. It reused the button API and field/panel/error primitives,
implemented an already documented native dialog, and preserved hex notation,
Arial, 400/700 typography, and the system's no-motion rule. No system files,
services, or dependencies changed.

Fixture and inspectable evidence:
`/var/folders/mw/r4366z0x3xnb_l0521bcwfj40000gn/T/uikit-implement-eval-wyxr4qjj/`.
The `evidence/` directory contains `implementation.md`, `browser-acceptance.js`,
`browser-results.txt`, `audit.json`, `original-main.js`, and screenshots.

Commands run in that fixture:

```sh
npm test
node --check src/main.js
npm start
playwright-cli -s=uikit-eval open http://127.0.0.1:4179/docs/flows/profile.html
playwright-cli -s=uikit-eval run-code --filename=evidence/browser-acceptance.js > evidence/browser-results.txt
```

Results: unit test 1/1 passed; syntax check exited 0; browser acceptance exited 0
with 54 checks passed. These exercised persistence/reload, failure/retry, duplicate
submission prevention, keyboard/focus, responsive bounds at 320/480/640/688px,
computed component styles, rendered contrast, and reduced motion. No overflow or
unresolved design drift was found. Rendered text contrast ranged from 7.46:1 to
16.29:1; field boundary contrast was 5.74:1 and focus contrast was 7.85:1.

Negative control: the same entry acceptance was run with the exact original
`main.js` intercepted in the browser. It failed as expected with `Missing Edit
name control`. Interception was removed and the implemented app restored and
checked. Source files were never reverted on disk.

Browser testing caught reverse Tab escaping the modal; the worker corrected
boundary cycling and reran the checks. A service-interception cache issue was
fixed in the harness without weakening acceptance. The original source flow and
implemented screenshots were visually inspected. Browser/server sessions were
stopped after evidence capture.

Acceptance: the native fixture demonstrated the requested translation, real state
behavior, approved substitution, stack preservation, and zero-drift verification.
Scope is one native-JavaScript fixture in Chromium; other stacks were reviewed as
decision scenarios, not exhaustively executed. No manual screen-reader or
cross-engine testing was attempted. Claude Code's CLI was not available on PATH,
so plugin discovery was checked structurally rather than through a live CLI load.

## Scope and operational notes

No website feature, external integration, remote push, or deployment is part of
this change. Skill instructions are an execution/review contract, not a runtime
hook or proof that every future implementation will comply automatically.

The initial grill-skip ledger call was rejected because its reason delimiter was
invalid; it was corrected using `reason=density-low:`. The advisory descent report
therefore shows the earlier phases preceding the corrected grill record. The
requirements and done scenario were resolved before implementation; the ledger
was not rewritten to conceal the recording error.
