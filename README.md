# uikit

A set of Agent Skills for coding agents (Claude Code, OpenCode, Codex, and any SKILL.md reader) to establish a design system, draw feature flows, and implement them in your project.

**New here or unsure what comes next? Run `/uikit:what` — What do I do next?**
It inspects your project and recommends one next action. It provides guidance without changing files.
The full routing map — the main flow, the on-ramps, and who invokes what — is [docs/map.md](docs/map.md),
drawn as a diagram in the [field guide](docs/field-guide.html).

| Skill | Invoke | Produces |
|---|---|---|
| what | `/uikit:what [question]` | Project-aware guidance on where to start or resume |
| setup | `/uikit:setup` | The pre-flight before init-design-system: a recorded `docs/uikit.md` — the approved system source, stack, and flows location — so init harvests the right source and the other skills stop guessing |
| init-design-system | `/uikit:init-design-system` | A live `/uikit/design-system` route plus the component setup in the project's own stack (React/shadcn, Astro, or Svelte/Bits UI) |
| prototype | `/uikit:prototype <feature>` | A flow definition in `docs/flows/` plus a dev route `/uikit/flows/<feature>` drawn from the project's real components, with a drift ledger |
| implement | `/uikit:implement <flow>` | Working feature code in the project's native stack, using approved system components and tokens with zero drift |
| using-uikit | model-invoked | Orientation: the compact map, reached automatically when a session touches UI work |

For a new design foundation, the ideal order is setup → init-design-system → prototype → implement: `/uikit:setup` (optional) records which existing files are the approved source, `init-design-system` builds the system from that, then you draw and build features. If you already have an approved system or feature flow, start at the relevant step; `/uikit:what` helps you choose. The design system is the base every prototype is drawn on; every prototype run ends by asking, for each new drift it drew, whether it goes back into the design system as a reusable component or stays a one-off in its flow. Drift already open across earlier flows, or answered *Decide later*, waits for `/uikit:prototype drift`. Implementation checks the current approved system: open proposals and reviewed one-offs cannot ship as exceptions. A system gap must be resolved in the system first.

The design system is a **live route**, not a static page: `/uikit/design-system` renders the
project's real components, so reviewing the system and reviewing the app are the same act. So
are the flows: `/uikit/flows/<feature>` renders each step from those same components. Both are
dev surfaces — hidden outside local and preview, unlinked, `noindex`, and off the sitemap.

`/uikit:implement docs/flows/invite-team.json` reads every screen and state, inspects the
actual codebase, maps UI to approved components, builds the feature, and verifies
behavior, responsive rendering, accessibility, and design-system fidelity. It also
accepts multiple flows, a legacy `docs/flows/*.html` file, and `--system <path>`. Existing
systems and stacks are preserved; the initialization skill's library and styling defaults
are not imposed during implementation.

## Install

`uikit` is a set of Agent Skills in the standard `skills/<name>/SKILL.md` layout, plus a Claude
Code plugin manifest — so most agents that read SKILL.md can use it. Clone once, then pick your
agent.

```bash
git clone https://github.com/tuanddd/uikit.git ~/.claude/skills/uikit
```

### Claude Code

Claude Code loads any `~/.claude/skills/<name>/` that carries `.claude-plugin/plugin.json` as a
plugin, here `uikit@skills-dir`. Start a new session, or run `/reload-plugins`.

Open Claude Code in **your application project**, then run:

```text
/uikit:what
```

Confirm `/uikit:what`, `/uikit:setup`, `/uikit:init-design-system`, `/uikit:prototype`, and
`/uikit:implement` appear in the command picker. If they are missing, check that
`~/.claude/skills/uikit/.claude-plugin/plugin.json` exists, run `/reload-plugins`,
and try a new session. Files on disk alone do not confirm the plugin loaded.

### OpenCode

OpenCode discovers skills from the Claude-compatible `~/.claude/skills/**` as well as
`~/.config/opencode/skills/`, `.opencode/skills/`, `~/.agents/skills/`, and their project
equivalents. **The clone above is enough:** the skills show up to the `skill` tool as
`what`, `setup`, `init-design-system`, `prototype`, `implement`, and `using-uikit` (the last
model-invoked, with no command).

To keep agents separate, clone elsewhere and link the skills in:

```bash
git clone https://github.com/tuanddd/uikit.git ~/.local/share/uikit
mkdir -p ~/.config/opencode/skills
ln -s ~/.local/share/uikit/skills/* ~/.config/opencode/skills/
```

Skill names must be unique across every location OpenCode reads; a same-named skill elsewhere
shadows this one, so remove or rename the other if `prototype` does not appear.

### Codex and other skill-dir agents

Agents that read a flat `~/.<agent>/skills/<name>/SKILL.md` (Codex uses `~/.codex/skills/`) need
one entry per skill. Clone once and link them:

```bash
git clone https://github.com/tuanddd/uikit.git ~/.claude/skills/uikit
mkdir -p ~/.codex/skills
ln -s ~/.claude/skills/uikit/skills/* ~/.codex/skills/
```

### Invocation

| Agent | Invoke |
|---|---|
| Claude Code | `/uikit:what`, `/uikit:setup`, `/uikit:init-design-system`, `/uikit:prototype`, `/uikit:implement` |
| OpenCode / Codex / generic | Ask in plain language, or invoke the skill by name (`what`, `setup`, `init-design-system`, `prototype`, `implement`, `using-uikit`) |

`what`, `init-design-system`, `implement`, and `using-uikit` also match relevant natural-language
requests. `setup` and `prototype` are explicit-invocation only. Skills that reject unknown
frontmatter keys can drop the Claude Code-only `disable-model-invocation: true` line carried by
`setup` and `prototype`.

### Update

```bash
git -C ~/.claude/skills/uikit pull --ff-only
```

If Git reports local changes or diverged history, resolve those before updating; do not
overwrite your edits. Then reload the agent (Claude Code: `/reload-plugins`).

## Choose your starting point

The [map](docs/map.md) is canonical, and `/uikit:what` routes within it. If you remember one
thing: just installed, lost, or returning — run `/uikit:what`; it reads the project and names the
actual next step. The [field guide](docs/field-guide.html) is the same map, drawn per skill.

The ideal order on a new project is `/uikit:setup` (optional) → `/uikit:init-design-system` →
`/uikit:prototype` → `/uikit:implement`. Setup records the approved system, the stack, and where
flows live; running it first is what stops `init-design-system` from having to ask whether to
follow the repo's files or the skill defaults. Without it, the skills rediscover those facts each
time and may disagree.

You can ask a specific question too:

```text
/uikit:what I already have a design system in Vue
```

`what`, `init-design-system`, `implement`, and `using-uikit` can also match relevant
natural-language requests. `setup` and `prototype` require explicit invocation.

## Requirements

- `/uikit:init-design-system`: a React, Astro, or Svelte web project it can wire components into. Other stacks fall back to a static design-system page.
- `/uikit:what`: no paid tools required; access to your project helps it give specific guidance.
- `/uikit:setup`: no paid tools required; access to your project lets it record the right source. Run once per repo; re-run only to change a recorded choice.
- `using-uikit`: no requirements; model-invoked orientation, never editable by hand.
- `/uikit:prototype`: a design system it can render (a live route, or the static fallback page) and `python3` for its helpers. Mobbin MCP is an optional paid reference source; without it, the skill asks whether to continue with free sources.
- `/uikit:implement`: an existing project, an approved design system, and a flow (a definition plus its route, or a legacy HTML file). Uses the project's build/test tooling and an available browser for visual and interaction verification; no Mobbin dependency.

## Layout

```
.claude-plugin/plugin.json
docs/
  map.md               the canonical routing map
  field-guide.html     the same map, drawn
skills/
  using-uikit/         SKILL.md              (model-invoked orientation)
  what/                SKILL.md
  setup/               SKILL.md
  init-design-system/  SKILL.md, README.md, references/
  prototype/           SKILL.md, README.md, FLOW-FILE.md, DRIFT.md, CRAFT-RULES.md,
                       REFERENCE-SOURCES.md, templates/, scripts/
  implement/           SKILL.md
```
