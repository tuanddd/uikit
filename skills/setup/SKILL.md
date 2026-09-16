---
name: setup
description: "Record a project's uikit facts once, per repo: the approved design-system source, the stack, and where flows live. Run before the first flow when more than one system source exists or the answers are unclear. Writes docs/uikit.md and an `## Design system` block, so /uikit:what, /uikit:prototype, and /uikit:implement stop guessing."
disable-model-invocation: true
---

# Setup

Scaffold the per-repo facts the other uikit skills assume:

- **Design-system source** — which tokens, viewer, or files are the approved system
- **Stack** — the framework and component library the system is authored in
- **Flows** — where flow definitions live and where their dev routes sit

This is a prompt-driven skill, not a deterministic script. Explore, present what you found,
confirm with the user, then write. Nothing is written before the user confirms.

The goal is a single recorded answer, so `/uikit:what`, `/uikit:prototype`, and
`/uikit:implement` read it instead of re-deriving it and disagreeing.

## Process

### 1. Explore

Look at the current repo. Read what exists; assume nothing:

- `git remote -v` and `.git/config` — only to name the project; no network calls.
- `package.json` and the lockfile — framework, version, component and icon libraries.
- The approved system, by convention: a `/uikit/design-system` route or its route file, then
  `docs/design-system.html`, `DESIGN.md`, `tokens.json`, `tokens/`, `theme.ts`,
  `globals.css`/`app.css`, `tailwind.config.*`, `components.json`, and installed component
  examples. Record every candidate, not just the first.
- `docs/uikit.md` — this skill's prior output. If it exists, this run is an update, not a
  first setup.
- `docs/flows/README.md` and `docs/flows/*.json` — is there an existing flows convention?
- `AGENTS.md` and `CLAUDE.md` at the repo root — does either exist? Is there already an
  `## Design system` section?

### 2. Present findings and ask

Summarise what is present and what is missing in a few lines. Then take the sections in order,
**one section, one answer**, leading each with the recommended answer so the user can accept it
in a word. Skip a section entirely when exploration already settled it and no real choice
remains. Give a one-line explainer only where the choice genuinely branches.

**Section A: Design-system source.** Only ask when two or more sources compete and none is
stated as canonical.

> Explainer: The "design system source" is the tokens and components the other skills read and
> build against. When several files could be it, recording one stops `/uikit:what`,
> `/uikit:prototype`, and `/uikit:implement` from each picking a different one.

Recommend the live `/uikit/design-system` route and the components it imports when present;
otherwise the static page or the token file that actually ships. Offer the found candidates,
then **Other** (a path the user names).

**Section B: Stack.** Default to the framework read from `package.json`; ask only when the
monorepo has more than one app, or the framework is none of React, Astro, or Svelte.

> Explainer: React, Astro, and Svelte get native components and a live design-system route.
> Another stack still gets the static fallback page and `tokens.css`, but no native route.

Record the framework, the component library (shadcn / Bits UI / native / other), and whether the
project gets a native route or the static page.

**Section C: Flows location.** Default to `docs/flows/` with dev routes at
`/uikit/flows/<feature>`. Ask only if `docs/flows/` (or another convention) already exists and
differs.

### 3. Confirm and edit

Show the user a draft of:

- The `## Design system` block to add to whichever of `CLAUDE.md` / `AGENTS.md` is being edited
  (step 4 has the selection rule)
- The full contents of `docs/uikit.md`

Let them edit before writing.

### 4. Write

**Pick the file to edit:** if `CLAUDE.md` exists, edit it; else if `AGENTS.md` exists, edit it;
if neither exists, ask which one to create and do not pick for them. Never create `AGENTS.md`
when `CLAUDE.md` exists (or the reverse). If an `## Design system` block already exists, update
it in place rather than appending a duplicate, and leave the surrounding sections alone.

The block:

```markdown
## Design system

Approved source: [path or `/uikit/design-system`]. Stack: [framework + component library].
Flows: `docs/flows/`, drawn at `/uikit/flows/<feature>`. See `docs/uikit.md`.
```

Write `docs/uikit.md` from this template, filled in:

```markdown
# uikit project record

Written by `/uikit:setup`. `/uikit:what`, `/uikit:prototype`, and `/uikit:implement` read this
before re-deriving the same facts. Edit it directly; re-run `/uikit:setup` only to change a
recorded choice.

## Design system

- Approved source: <path, or `/uikit/design-system`>
- Tokens: <path to the authored token source, or "none">
- Viewer: <live route `/uikit/design-system`, or static page `docs/design-system.html`>

## Stack

- Framework: <React | Astro | Svelte | other>
- Components: <shadcn | Bits UI | native | other>
- Route support: <native route | static page>

## Flows

- Definitions: <`docs/flows/`>
- Dev routes: <`/uikit/flows/<feature>`>
```

Reuse the map's vocabulary: the stages are `setup`, `system`, `flow`, `drift`, `implement`, as
[../../docs/map.md](../../docs/map.md) defines them.

### 5. Done

Tell the user setup is complete, name the file written (`docs/uikit.md`) and the block added,
and say which skills now read them. Mention they can edit `docs/uikit.md` directly later;
re-running this skill is only needed to change a recorded choice.
