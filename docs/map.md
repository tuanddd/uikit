# The uikit map

The single source of truth for how uikit routes. [`README.md`](../README.md),
[`field-guide.html`](field-guide.html) and the `what` skill all point here instead of
restating it. Change the route here first, then let the others follow.

## The main flow: system → flow → feature

1. **init-design-system** — define the design system once per project.
   `/uikit:init-design-system`
2. **prototype** — draw one feature as a flow against that system.
   `/uikit:prototype <feature>`
   ↳ **drift loop** — `/uikit:prototype drift`, for departures left open across flows.
3. **implement** — build the feature in the project's own stack.
   `/uikit:implement docs/flows/<feature>.json`

Each step reads what the one before it wrote. The order is a default, not a gate: a
project with an approved system can start at step 2 or 3.

## Stages

Every route on the map belongs to one stage. `/uikit:what` names the user's stage in its reply,
and `/uikit:setup` uses the same vocabulary.

| Stage | Means | Command |
|---|---|---|
| `setup` | Record the project's facts before routing | `/uikit:setup` |
| `system` | Establish the design system | step 1, `/uikit:init-design-system` |
| `flow` | Draw a feature, or update an existing one | step 2, `/uikit:prototype <feature>` |
| `drift` | Settle departures left open across flows | the drift loop, `/uikit:prototype drift` |
| `implement` | Build an approved flow | step 3, `/uikit:implement <flow>` |
| `unknown` | Not enough evidence to place the user yet | ask one question |

## On-ramps

A situation that generates work, then joins the main flow.

| Your situation | Join at |
|---|---|
| Just installed, lost, or returning to the project | `/uikit:what` — the router |
| A React, Astro, or Svelte project with no design foundation | step 1 |
| An approved system exists and you have a feature idea | step 2 |
| An existing flow needs changing | step 2 — `/uikit:prototype update <flow> <change>` |
| A screen needs UI the approved system does not provide (drift) | the drift loop |
| A flow is approved and ready to build | step 3 |

## Standalone

- **`/uikit:what [question]`** — the router. Inspects the project and recommends one next
  action. Read-only: it executes nothing.
- **`/uikit:setup`** — record this project's design-system source, stack, and flows location
  once. Worth running before the first flow when more than one system source exists.
- **`using-uikit`** — model-invoked orientation. The compact form of this map, reached
  automatically when a session touches UI work.

## Who invokes what

| You invoke it | You or the agent may invoke it |
|---|---|
| `/uikit:setup`, `/uikit:prototype` | `/uikit:what`, `/uikit:init-design-system`, `/uikit:implement`, `using-uikit` |

## The project record

`/uikit:setup` writes `docs/uikit.md` in the consuming project. When that file exists it is
the recorded source of truth for the design-system source, the stack, and the flows
directory; `/uikit:what`, `/uikit:prototype`, and `/uikit:implement` read it before
re-deriving those facts. Without it, every skill discovers them again from the code.
