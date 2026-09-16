---
name: what
description: Help users choose their next UIkit step after installation or whenever they feel lost. Use for /uikit:what, questions about which UIkit skill fits their situation, or how to resume a UIkit project. Inspects existing project context and gives read-only guidance.
---

# What do I do next?

Orient the user in UIkit: understand their intent, inspect what they already have,
and recommend one useful next action. Accept a bare `/uikit:what` or a question,
such as `/uikit:what I already have a design system in Vue`.

This is guidance. Do not edit files, install dependencies, change settings, run a
build, contact paid services, or execute a recommended skill. A subsequent request
to carry out the recommendation belongs to that skill's own workflow.

## Find the starting point

Use the current conversation first. Answer a narrow question directly; inspect
only the files needed to ground it. For a bare invocation, inspect the project:

- Read applicable repository instructions and a short product overview. Read
  `docs/uikit.md` (the `/uikit:setup` record) first when it exists: it is the recorded
  design-system source, stack, and flows directory, and it settles what discovery would
  otherwise guess.
- Identify the app and stack from manifests and existing code. If the working
  directory is the plugin itself, explain that the next step is to open the user's
  application project. If there is no app yet, ask whether they have an existing
  project or want to create one; UIkit initialization assumes an existing React app.
- Locate the approved system using the user's path or repository conventions: a
  `/uikit/design-system` route or its route file, then `docs/design-system.html`,
  `DESIGN.md`, token/theme files, CSS variables, and installed component examples.
  Init-design-system writes a live route for React, Astro, and Svelte projects; the static
  HTML page is its fallback for stacks it cannot wire. Existing native systems can be valid
  inputs; a route or an HTML page is not universally required. File existence alone does not
  establish approval. Ask if competing sources have no stated precedence.
- Find `docs/flows/README.md`, the flow definitions (`docs/flows/*.json`) and their dev
  routes (`/uikit/flows/<feature>`), any legacy `docs/flows/*.html`, their drift rows, and
  implementation or verification notes. Read targeted sections of large files.
  Do not infer the current task from modification time or claim a feature is
  complete because a flow or component file exists.

Stop inspecting once there is enough evidence for a useful recommendation. If the
user's intent remains unclear, summarize what you found and ask one focused
question about their desired outcome. Do not make them repeat discoverable facts.

On a first-use or installation question, check the available skill catalog for all the
UIkit skills — `what`, `setup`, `init-design-system`, `prototype`, `implement`, and
`using-uikit`. Distinguish files found on disk from skills actually exposed
by the current session. If the catalog is unavailable, say availability is unverified
and suggest checking the `/uikit:` commands after `/reload-plugins` or a new session.
For installation details, read the plugin's [README](../../README.md). When this
skill cannot be invoked at all, that README is the recovery path.

## Choose the next action

Route within the map, never around it. Read [../../docs/map.md](../../docs/map.md): it is the
canonical routing truth — the main flow, the stages, the on-ramps, and who invokes what. This skill
decides where the user sits on that map and names one next action; it never restates the map's
on-ramps table, which can only drift from the canonical copy.

Read the relevant sibling skill before recommending its syntax or prerequisites. Those files own
their execution rules; this guide does not override them.

Name the user's **stage** — `setup`, `system`, `flow`, `drift`, `implement`, or `unknown` — from the
map's stages and the evidence you gathered, then recommend that stage's command:

- **setup** — the pre-flight before the system: two or more system sources compete (or none is recorded) and no `docs/uikit.md` settles it: [setup](../setup/SKILL.md): `/uikit:setup`. It records the approved source so `/uikit:init-design-system` harvests the right one instead of asking whether to follow the repo or the skill defaults.
- **system** — no approved system in a React, Astro, or Svelte project: [init-design-system](../init-design-system/SKILL.md): `/uikit:init-design-system`. Say that it creates a live `/uikit/design-system` route and authors the components natively in the project's stack.
- **flow** — an approved system and a feature to draw: [prototype](../prototype/SKILL.md): `/uikit:prototype <feature>`. It produces a flow definition whose screens render the real components at a dev route, with mock data, not an interactive production feature. The design system should exist first — see **Have a design system before the first flow** below. An existing flow needs changes: `/uikit:prototype update <flow> <change>` — the stage is still `flow`.
- **drift** — open proposals or deferred drift decisions: [drift review](../prototype/DRIFT.md): `/uikit:prototype drift`. Drift is a component, variant, detail, or guideline departure the approved system does not provide.
- **implement** — a flow ready to build against an approved system: [implement](../implement/SKILL.md): `/uikit:implement <flow>`. Preserves the project's native stack and verifies real behavior and system compliance.
- **returning** — ongoing work: use the stated goal, relevant artifacts, and recorded checks to find the next unfinished step, and name that step's stage. Ask which feature if several are plausible.

**Have a design system before the first flow.** The ideal order is `/uikit:setup` →
`/uikit:init-design-system` → `/uikit:prototype` → `/uikit:implement`. `/uikit:prototype` draws
every screen from the approved system — the live `/uikit/design-system` route, or the static page
for a stack that cannot host one. That system is the output of `/uikit:init-design-system`. Running it first is
highly recommended but **not a hard gate**: with no system, prototype falls back to whatever
tokens the repo has and every component it draws counts as drift. On a project that has none, say
plainly that the flow will be drawn against a stand-in and that `/uikit:init-design-system` is the
strongly preferred first step; if the user chooses to proceed anyway, that is their call.

Treat these as entry points, not a sequence everyone must repeat. A project with an approved
system can go to prototype or implement whatever its stack. Do not recommend React
initialization or a migration just to use UIkit. Init-design-system authors components and a
live route for React, Astro, and Svelte; for another stack with a system, it can still write
the static design-system page, and for another stack without one, explain the initialization
skill's scope and recommend establishing an approved native system first. Do not invent a
UIkit command for that missing step.

Before recommending implementation, inspect relevant drift and the current system.
Open proposals, `Proposed here`, `Proposed in …`, and reviewed `one-off` exceptions
are not permission to ship. A `promoted` or `folded` status needs a matching approved
definition. The drift command reviews open rows; it does not automatically reopen
reviewed one-offs. For a reviewed exception, name the gap and recommend explicitly
resolving it in the system or revising the flow to use approved components first.
Do not equate a clean ledger with a completed implementation audit.

## Explain prerequisites only when relevant

- **Prototype:** Python 3 runs the bundled helpers. Mobbin is a paid reference
  source with a free-source alternative. Report tool availability if visible, but
  do not perform lookups or claim authentication/quota was checked. If absent,
  explain that the prototype skill asks whether to continue with free sources.
- **Implement:** Needs the project, approved system, and feature flow. Project
  checks and a browser are needed for full verification. Mobbin is not required.
- **Init:** Needs a React, Astro, or Svelte web project for its live route and native
  components; other stacks get a static page. Existing tokens are reused; this command
  changes the app as well as producing the viewer.

Unavailable optional tools should not derail guidance. Name a required missing
input and the smallest action that supplies it. If the user asks for work outside
UIkit's scope, say so and recommend an appropriate ordinary project task without
inventing capabilities or forcing it through the pipeline.

## Reply

Open every reply with the stage line, then the three fields, in exactly this shape. Fill the
angle-bracketed slots. Do not reorder, rename, or drop them, and do not replace the line with a
sentence: this contract is what makes every invocation read the same.

**uikit · `<stage>` · `<status>`**

- **Where you are:** <one or two findings, with paths when useful>
- **Next:** `<command>`
- **Why:** <one sentence explaining what it accomplishes>

`<stage>` is one of `setup`, `system`, `flow`, `drift`, `implement`, `unknown`. `<status>` is two
to four words: `ready`, `none found`, `1 flow, drift open`, `system found, flow missing`. Add a
fourth field only for a real open decision. Show alternatives only for a real decision or when
asked for the full map. Returning users get current context, not the welcome tutorial again.

Example:

**uikit · `drift` · `1 flow, 1 open proposal`**

- **Where you are:** `docs/flows/invite-team.json` exists and the system renders at `/uikit/design-system`; the flow still has an open Drawer proposal.
- **Next:** `/uikit:prototype drift`
- **Why:** review that proposal against the system before implementing the invitation flow.

If a missing answer prevents routing, ask that question on the **Next:** line instead of offering
a placeholder command, and set `<stage>` to `unknown`. When instead the ambiguity is two or more
competing system sources with no `docs/uikit.md` record to settle them, `setup` is the honest stage
and `/uikit:setup` the next action.

Finish after the guidance. Recommendations are not proof that a build, visual review, connection
check, or installation test has run.
