# uikit

A Claude Code plugin to establish a design system, draw feature flows, and implement them in your project.

**New here or unsure what comes next? Run `/uikit:what` — What do I do next?**
It inspects your project and recommends one next action. It provides guidance without changing files.

| Skill | Invoke | Produces |
|---|---|---|
| what | `/uikit:what [question]` | Project-aware guidance on where to start or resume |
| init-design-system | `/uikit:init-design-system` | A live `/uikit/design-system` route plus the component setup in the project's own stack (React/shadcn, Astro, or Svelte/Bits UI) |
| prototype | `/uikit:prototype <feature>` | One self-contained HTML flow file per feature in `docs/flows/`, drawn on that design system, with a drift ledger |
| implement | `/uikit:implement <flow.html>` | Working feature code in the project's native stack, using approved system components and tokens with zero drift |

For a new design foundation, use init-design-system → prototype → implement. If you already have an approved system or feature flow, start at the relevant step; `/uikit:what` helps you choose. The design system is the base every prototype is drawn on; every prototype run ends by asking, for each new drift it drew, whether it goes back into the design system as a reusable component or stays a one-off in its flow. Drift already open across earlier flows, or answered *Decide later*, waits for `/uikit:prototype drift`. Implementation checks the current approved system: open proposals and reviewed one-offs cannot ship as exceptions. A system gap must be resolved in the system first.

The design system is a **live route**, not a static page: `/uikit/design-system` renders the
project's real components, so reviewing the system and reviewing the app are the same act. It
is a dev surface — hidden outside local and preview, unlinked, `noindex`, and off the sitemap.

`/uikit:implement docs/flows/feature.html` reads every screen and state, inspects the
actual codebase, maps UI to approved components, builds the feature, and verifies
behavior, responsive rendering, accessibility, and design-system fidelity. It also
accepts multiple paths, `docs/flows/*.html`, and `--system <path>`. Existing systems
and stacks are preserved; the initialization skill's library and styling defaults
are not imposed during implementation.

## Install

Run in your terminal:

```bash
git clone https://github.com/tuanddd/uikit.git ~/.claude/skills/uikit
```

Claude Code loads any `~/.claude/skills/<name>/` that carries `.claude-plugin/plugin.json` as a plugin, here `uikit@skills-dir`. Start a new session, or run `/reload-plugins`.

Open Claude Code in **your application project**, then run:

```text
/uikit:what
```

Confirm `/uikit:what`, `/uikit:init-design-system`, `/uikit:prototype`, and
`/uikit:implement` appear in the command picker. If they are missing, check that
`~/.claude/skills/uikit/.claude-plugin/plugin.json` exists, run `/reload-plugins`,
and try a new session. Files on disk alone do not confirm the plugin loaded.

For an existing clone, update from your terminal with
`git -C ~/.claude/skills/uikit pull --ff-only`, then reload plugins. If Git reports
local changes or diverged history, resolve those before updating; do not overwrite
your edits.

## Choose your starting point

| Your situation | Next step |
|---|---|
| Just installed, lost, or returning to the project | `/uikit:what` |
| React project needs a design foundation | `/uikit:init-design-system` |
| Have an approved system and want to design a feature | `/uikit:prototype invite teammates` |
| Need to change an existing flow | `/uikit:prototype update docs/flows/invite-team.html add an expired invitation state` |
| Have open or deferred system proposals | `/uikit:prototype drift` |
| Have an approved system and a flow ready to build | `/uikit:implement docs/flows/invite-team.html` |

You can ask a specific question too:

```text
/uikit:what I already have a design system in Vue
```

`what`, `init-design-system`, and `implement` can also match relevant
natural-language requests. `prototype` requires explicit invocation.

## Requirements

- `/uikit:init-design-system`: a React, Astro, or Svelte web project it can wire components into. Other stacks fall back to a static design-system page.
- `/uikit:what`: no paid tools required; access to your project helps it give specific guidance.
- `/uikit:prototype`: a design system and `python3` for its helpers. Mobbin MCP is an optional paid reference source; without it, the skill asks whether to continue with free sources.
- `/uikit:implement`: an existing project, an approved design system, and an HTML feature flow. Uses the project's build/test tooling and an available browser for visual and interaction verification; no Mobbin dependency.

## Layout

```
.claude-plugin/plugin.json
skills/
  what/                SKILL.md
  init-design-system/   SKILL.md, README.md, references/
  prototype/            SKILL.md, README.md, FLOW-FILE.md, DRIFT.md, CRAFT-RULES.md,
                        REFERENCE-SOURCES.md, templates/flow.html, scripts/
  implement/            SKILL.md
```
