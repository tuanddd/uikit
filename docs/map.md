# The uikit map

The single source of truth for how uikit routes. [`README.md`](../README.md),
[`field-guide.html`](field-guide.html) and the `what` skill all point here instead of
restating it. Change the route here first, then let the others follow.

## The main flow: setup → system → flow → feature

0. **setup** — the optional pre-flight. `/uikit:setup` records which existing files are the
   approved system, the stack, and where flows live, so the steps after it do not have to
   guess or ask. Skip it and the other skills still discover these from the code.
1. **init-design-system** — define the design system once per project. Reads the `setup`
   record as its input. `/uikit:init-design-system`
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
| `setup` | Record the project's facts before the system (pre-flight) | step 0, `/uikit:setup` |
| `system` | Establish the design system, reading the record | step 1, `/uikit:init-design-system` |
| `flow` | Draw a feature, or update an existing one | step 2, `/uikit:prototype <feature>` |
| `drift` | Settle departures left open across flows | the drift loop, `/uikit:prototype drift` |
| `implement` | Build an approved flow | step 3, `/uikit:implement <flow>` |
| `unknown` | Not enough evidence to place the user yet | ask one question |

## On-ramps

A situation that generates work, then joins the main flow.

| Your situation | Join at |
|---|---|
| Just installed, lost, or returning to the project | `/uikit:what` — the router |
| A React, Astro, or Svelte project with no design foundation | step 1 — run step 0 first when more than one source competes |
| An approved system exists and you have a feature idea | step 2 |
| An existing flow needs changing | step 2 — `/uikit:prototype update <flow> <change>` |
| A screen needs UI the approved system does not provide (drift) | the drift loop |
| A flow is approved and ready to build | step 3 |

## Standalone

- **`/uikit:what [question]`** — the router. Inspects the project and recommends one next
  action. Read-only: it executes nothing.
- **`/uikit:setup`** — the pre-flight record: the approved system source, the stack, and the
  flows location, written once. It runs before `init-design-system` so that skill (and the rest)
  have one settled answer instead of guessing. Optional; worth it when more than one source
  competes or the project has never been configured.
- **`using-uikit`** — model-invoked orientation. The compact form of this map, reached
  automatically when a session touches UI work.

## Who invokes what

| You invoke it | You or the agent may invoke it |
|---|---|
| `/uikit:setup`, `/uikit:prototype` | `/uikit:what`, `/uikit:init-design-system`, `/uikit:implement`, `using-uikit` |

## The project record

`/uikit:setup` writes `docs/uikit.md` in the consuming project. When that file exists it is the
recorded source of truth for the design-system source, the stack, and the flows directory;
`/uikit:init-design-system`, `/uikit:what`, `/uikit:prototype`, and `/uikit:implement` read it
before re-deriving those facts. Without it, every skill discovers them again from the code.

The record holds **pointers and choices, not tokens** — it says which existing files are the
approved system, not what the colors are. `init-design-system` harvests from the source the
record names, and never treats the record itself as a set of design values or preferences.
