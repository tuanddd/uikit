# uikit

A Claude Code plugin with two skills for a product's UI:

| Skill | Invoke | Produces |
|---|---|---|
| init-design-system | `/uikit:init-design-system` | `docs/design-system.html` plus a working shadcn/ui setup on the project's tokens |
| prototype | `/uikit:prototype <feature>` | One self-contained HTML flow file per feature in `docs/flows/`, drawn on that design system, with a drift ledger |

Run them in that order. The design system is the base every prototype is drawn on; the drift the prototypes record goes back into the design system through `/uikit:prototype drift`.

## Install

```bash
git clone https://github.com/tuanddd/uikit.git ~/.claude/skills/uikit
```

Claude Code loads any `~/.claude/skills/<name>/` that carries `.claude-plugin/plugin.json` as a plugin, here `uikit@skills-dir`. Start a new session, or run `/reload-plugins`.

## Requirements

- `/uikit:init-design-system`: a React project it can wire shadcn/ui into.
- `/uikit:prototype`: a Mobbin plan with its MCP server connected. It is paid; the skill checks it before starting, says so, and can fall back to free sources. `python3` runs its two scripts.

## Layout

```
.claude-plugin/plugin.json
skills/
  init-design-system/   SKILL.md, README.md, references/
  prototype/            SKILL.md, README.md, FLOW-FILE.md, DRIFT.md, CRAFT-RULES.md,
                        REFERENCE-SOURCES.md, templates/flow.html, scripts/
```
