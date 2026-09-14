# uikit

A Claude Code plugin with three skills for a product's UI:

| Skill | Invoke | Produces |
|---|---|---|
| init-design-system | `/uikit:init-design-system` | `docs/design-system.html` plus a working shadcn/ui setup on the project's tokens |
| prototype | `/uikit:prototype <feature>` | One self-contained HTML flow file per feature in `docs/flows/`, drawn on that design system, with a drift ledger |
| implement | `/uikit:implement <flow.html>` | Working feature code in the project's native stack, using approved system components and tokens with zero drift |

Run them in that order. The design system is the base every prototype is drawn on; the drift the prototypes record goes back into the design system through `/uikit:prototype drift`. Implementation checks the current approved system: open proposals and reviewed one-offs cannot ship as exceptions. A system gap must be resolved in the system first.

`/uikit:implement docs/flows/feature.html` reads every screen and state, inspects the
actual codebase, maps UI to approved components, builds the feature, and verifies
behavior, responsive rendering, accessibility, and design-system fidelity. It also
accepts multiple paths, `docs/flows/*.html`, and `--system <path>`. Existing systems
and stacks are preserved; the initialization skill's library and styling defaults
are not imposed during implementation.

## Install

```bash
git clone https://github.com/tuanddd/uikit.git ~/.claude/skills/uikit
```

Claude Code loads any `~/.claude/skills/<name>/` that carries `.claude-plugin/plugin.json` as a plugin, here `uikit@skills-dir`. Start a new session, or run `/reload-plugins`.

## Requirements

- `/uikit:init-design-system`: a React project it can wire shadcn/ui into.
- `/uikit:prototype`: a Mobbin plan with its MCP server connected. It is paid; the skill checks it before starting, says so, and can fall back to free sources. `python3` runs its two scripts.
- `/uikit:implement`: an existing project, an approved design system, and an HTML feature flow. Uses the project's build/test tooling and an available browser for visual and interaction verification; no Mobbin dependency.

## Layout

```
.claude-plugin/plugin.json
skills/
  init-design-system/   SKILL.md, README.md, references/
  prototype/            SKILL.md, README.md, FLOW-FILE.md, DRIFT.md, CRAFT-RULES.md,
                        REFERENCE-SOURCES.md, templates/flow.html, scripts/
  implement/            SKILL.md
```
