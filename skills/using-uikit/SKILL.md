---
name: using-uikit
description: Orient UI and design-system work in a project that already uses uikit. Use only when the project shows a uikit signal — a /uikit dev route, docs/flows/, docs/uikit.md, or the user naming uikit — and the work touches a screen, component, feature flow, or the design system. Establishes uikit's skills, the map that orders them, and the router that names the next step.
---

# Using uikit

A project that uses uikit keeps one product brief, one design system, and one drawing per
feature, each written by the skill before it. This orientation tells you the shape of the work
and where to hand off. It builds nothing.

## When this applies

Apply only when the project shows a uikit signal: a `/uikit/design-system` or `/uikit/flows/`
route, a `docs/flows/` directory, a `docs/uikit.md` record, or the user naming uikit. With none of
those, this is an ordinary UI codebase: do not use uikit. When in doubt, hand off to `what`
(`/uikit:what`) and let it make the call.

## The map

The canonical routing truth is [../../docs/map.md](../../docs/map.md). The compact form:

1. **init-design-system** (`/uikit:init-design-system`) — define the design system once per
   project; authors the components in the project's own stack.
2. **prototype** (`/uikit:prototype <feature>`) — draw one feature as a flow against that
   system; ends by asking which new drift joins the system.
   ↳ **drift loop** (`/uikit:prototype drift`) — settle departures left open across flows.
3. **implement** (`/uikit:implement <flow>`) — build the feature in the project's stack with
   zero drift.

A project with an approved system can enter at step 2 or 3. The order is a default, not a gate.

## What to do with it

- **Unsure where the user stands, or which skill fits** — hand off to `what`
  (`/uikit:what [question]`). It inspects the project and returns one next action. Do not guess
  a stage and start building.
- **The design system is the base, not a cage.** Never invent tokens or one-off styles. A need
  the system does not cover is *drift*, and drift is recorded and folded back, never smuggled in.
- **This is read-only orientation.** It edits nothing, runs no build, and invokes no sibling
  skill. The handoff is a recommendation; the next skill's own workflow does the work.

## Who invokes what

| You invoke it | You or the agent may invoke it |
|---|---|
| `/uikit:setup`, `/uikit:prototype` | `/uikit:what`, `/uikit:init-design-system`, `/uikit:implement`, `using-uikit` |

`prototype` never auto-triggers; invoke it explicitly when the user wants a flow drawn.

## The project record

If the project has `docs/uikit.md` (written by `/uikit:setup`), it records the approved
design-system source, the stack, and the flows directory. Read it before re-deriving those from
the code. With no record and ambiguous sources, recommend `/uikit:setup`.
