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

- Read applicable repository instructions and a short product overview.
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
- Find `docs/flows/README.md`, relevant flow files, their drift rows, and any
  implementation or verification notes. Read targeted sections of large HTML files.
  Do not infer the current task from modification time or claim a feature is
  complete because a flow or component file exists.

Stop inspecting once there is enough evidence for a useful recommendation. If the
user's intent remains unclear, summarize what you found and ask one focused
question about their desired outcome. Do not make them repeat discoverable facts.

On a first-use or installation question, check the available skill catalog for
the four UIkit skills. Distinguish files found on disk from skills actually exposed
by the current session. If the catalog is unavailable, say availability is unverified
and suggest checking the `/uikit:` commands after `/reload-plugins` or a new session.
For installation details, read the plugin's [README](../../README.md). When this
skill cannot be invoked at all, that README is the recovery path.

## Choose the next action

Read the relevant sibling skill before recommending its syntax or prerequisites.
These files own their execution rules; this guide does not override them.

| User's situation | Recommendation |
|---|---|
| Existing React, Astro, or Svelte project needs a design foundation | [init-design-system](../init-design-system/SKILL.md): `/uikit:init-design-system`. Explain that it creates a live `/uikit/design-system` route and authors the components natively in the project's stack. |
| Existing approved system, feature idea to explore | [prototype](../prototype/SKILL.md): `/uikit:prototype <feature>`. Produces static HTML screens and states, with mock data, rather than an interactive production feature. |
| Existing flow needs changes | [prototype](../prototype/SKILL.md): `/uikit:prototype update <flow-file> <change>`. Reuse the existing file. |
| Open proposals or deferred drift decisions | [drift review](../prototype/DRIFT.md): `/uikit:prototype drift`. Drift means a component, variant, detail, or guideline departure that the approved system does not provide. |
| Flow ready to build using an approved system | [implement](../implement/SKILL.md): `/uikit:implement <flow.html>`. Preserves the project's native stack and verifies real behavior and system compliance. |
| Returning to ongoing work | Use the stated goal, relevant artifacts, and recorded checks to identify the next unfinished step. Ask which feature if several are plausible. |

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

Keep the usual answer to a short paragraph and one next action:

1. **Where you are:** one or two relevant findings, with paths when useful.
2. **Next:** one copyable command using the actual feature or quoted file path.
3. **Why / result:** one sentence explaining what it accomplishes; include a
   prerequisite or unresolved choice only when it affects the next step.

If a missing answer prevents routing, ask that question instead of offering a
placeholder command. Show alternatives only for a real decision or when asked for
the full map. Returning users get current context, not the welcome tutorial again.

Example:

> Found your design system and `docs/flows/invite-team.html`. The flow still has
> an open Drawer proposal.
>
> **Next:** `/uikit:prototype drift`
>
> Review that proposal against the system before implementing the invitation flow.

Finish after the guidance. Recommendations are not proof that a build, visual
review, connection check, or installation test has run.
