# The flow

One feature, one **definition** (`docs/flows/<slug>.json`) and one **route**
(`/uikit/flows/<slug>`) that renders it. The route composes the project's real components into
each step's screen; the definition is the portable record the route renders and the scripts
read. Neither carries a copy of a component's CSS.

`<slug>` is the definition's `slug` — `<group>-<NN>-<feature>`, e.g. `v1-13-direct-contact`.
It is both the file name and the route segment.

The route is a dev surface — hidden outside local and preview, unlinked, `noindex`,
`robots.txt`-disallowed, off the sitemap, `data-dev-surface` — exactly like the design-system
viewer.

## Where it lives

```
docs/flows/
  README.md                 index, mock values, the rules that keep drift down
  <slug>.json               the definition, e.g. v1-13-direct-contact.json
<dev>/flows/
  FlowShell.<ext>           renders a definition: the doc shell around the screens
  components/<Name>.<ext>   candidate components the drift needs, shared by flows
<route>/uikit/flows/<slug>  the route file that pairs the definition with its screens
```

`<group>` is the roadmap phase or product area; `<NN>` the feature's position; `<feature>`
kebab-case. When the existing definitions name themselves differently, follow them.

`<dev>` is the project's dev area, the same one the design-system viewer's `Specimen` helper
lives in: `src/dev` (React), `src/lib/dev` (Svelte), `src/components/dev` (Astro) — see the
`init-design-system` skill's `references/setup.md` § What lands.

Route file per stack:

```
React    app/uikit/flows/<slug>/page.tsx       (App Router; src/app/ when present)
         pages/uikit/flows/<slug>.tsx          (Pages Router)
         app/routes/uikit.flows.<slug>.tsx     (Remix / React Router 7)
Svelte   src/routes/uikit/flows/<slug>/+page.svelte
Astro    src/pages/uikit/flows/<slug>.astro
```

Static output and no-router SPAs: mount behind the same dev-only gate as the design-system
viewer (`init-design-system/references/stacks.md` § 4).

## The definition

JSON, one file per feature. It is data, not markup: the route renders it, `drift-report.py`
reads the ledger, and `flow-check.py` validates it.

```json
{
  "feature": "Direct contact",
  "slug": "v1-13-direct-contact",
  "group": "v1",
  "drawnOn": "2026-09-16",
  "frameWidth": 1280,
  "requirement": {
    "text": "A visitor can reach the person who listed the home without leaving the listing.",
    "source": "docs/FEATURES.md · v1 · Direct contact"
  },
  "steps": [
    {
      "id": "step-1",
      "n": 1,
      "title": "Inquiry, step 1: the home",
      "state": "Default",
      "route": "example.com/homes/house-name/ask",
      "restsOn": "Zillow contact form · Airbnb names the recipient · Mobbin MCP",
      "linkedTo": null
    }
  ],
  "why": [
    { "decision": "Ask dates before identity; identity last", "restsOn": "Mobbin MCP — Zillow, Airbnb", "confidence": "reference" },
    { "decision": "The reply-time line shows both clocks", "restsOn": "the positioning doc, audience", "confidence": "principle" }
  ],
  "components": [
    { "name": "Button", "class": ".btn", "from": "src/components/ui/Button", "steps": "1, 2" },
    { "name": "Channel row", "class": ".channel", "from": "candidate:ChannelRow", "steps": "2" }
  ],
  "ledger": [
    {
      "name": "Channel row",
      "class": ".channel",
      "kind": "component",
      "nearest": "Dialog · .dialog",
      "why": "The listing must stay visible while the visitor writes; Dialog centres over a scrim",
      "proposal": "promote",
      "status": "open"
    }
  ]
}
```

| Field | Required | Values |
|---|---|---|
| `feature`, `slug`, `group`, `drawnOn`, `frameWidth` | yes | The feature name; the slug (`<group>-<NN>-<feature>`, and the file name); the roadmap group; the date drawn; the desktop frame width (1280) |
| `requirement.text`, `requirement.source` | yes | The roadmap line quoted, and where it comes from |
| `steps` | yes, non-empty | One row per screen |
| `steps[].id` | yes | `step-N`, unique; the anchor and the `screens` key |
| `steps[].n` | yes | The integer in the id; the board number |
| `steps[].title`, `state`, `route` | yes when drawn | The step title; the state shown (`Default`, `Validation error`, `Empty`, `Sent`, …); the real route |
| `steps[].restsOn` | yes when drawn | One line: the reference or principle the step rests on |
| `steps[].linkedTo` | yes | `null` when the step is drawn; `<other-slug>#step-3` when another flow draws it (a linked step needs only `id`, `n`, `title`, `linkedTo`) |
| `why[].decision`, `restsOn`, `confidence` | yes | The decision; what it rests on; `reference` or `principle` |
| `components[].name`, `class`, `from`, `steps` | yes | The component; its class; `src/…` (a system component, the project's own path), `candidate:<Name>`, or `—`; the step numbers it appears in |
| `ledger[].name`, `class`, `kind`, `nearest`, `why`, `proposal`, `status` | yes | See DRIFT.md. `kind` ∈ `component`/`variant`/`detail`/`guideline`; `proposal` ∈ `promote`/`one-off`; `status` ∈ `open`/`promoted`/`folded`/`one-off` |

A flow with no drift carries `"ledger": []`, and the route says so in one line.

## The route

The route imports the definition and the real components, and renders the shell with one
screen per step. Screens are code — the components composed as the feature needs them.

```tsx
// React · app/uikit/flows/v1-13-direct-contact/page.tsx  (dev surface, not linked, gated)
import { notFound } from "next/navigation";
import { designSystemEnabled } from "@/dev/design-system-enabled";
import { FlowShell } from "@/dev/flows/FlowShell";
import { Button } from "@/components/ui/button";
import { ChannelRow } from "@/dev/flows/components/ChannelRow";
import def from "../../../../docs/flows/v1-13-direct-contact.json";

function Step1() {
  return <main>…Button…</main>;
}
function Step2() {
  return <main>…ChannelRow…</main>;
}

export default function Page() {
  if (!designSystemEnabled()) notFound();
  return (
    <div data-dev-surface>
      <FlowShell def={def} screens={{ "step-1": <Step1 />, "step-2": <Step2 /> }} />
    </div>
  );
}
```

Import the definition by a path relative to the route file (four `../` from
`app/uikit/flows/<slug>/`, one more when the project uses `src/app/`), or through a path alias
if the project has one; TypeScript needs `resolveJsonModule`. The Svelte and Astro forms are
the same in their syntax: import the definition, import the components, render
`<FlowShell def={def} screens={{ "step-1": … }} />`, each screen a component or markup
fragment. An overlay (dialog, drawer, menu) is drawn **open**, in place, over the page it opens
from.

`FlowShell` renders, in this order, from the definition:

| Section | Holds |
|---|---|
| Header | the feature · group, step count, frame width, "Static, mock values" · the requirement, quoted, and its source |
| Bar | link to `/uikit/flows` (the index), the section anchors |
| The flow | every step in order: number, title, state, route, linking to `#step-N` |
| Steps | one board per step: its stage holds that step's screen at `def.frameWidth` |
| Why it looks like this | the `why` rows: decision · rests on · confidence |
| Building on it | routes and mock values · the Components table · the drift ledger |
| Pager | previous and next flow in the index |
| Foot | part of `docs/flows`, the date drawn, what it was drawn on |

Author the shell once per project and reuse it in every flow, like the viewer's `Specimen`
helper. [templates/FlowShell.tsx](templates/FlowShell.tsx) is a React reference; the Svelte and
Astro forms follow the same props and section order. It reads the tokens for its own chrome; it
never restyles a screened component.

Frame width comes from `def.frameWidth` (1280 for desktop); a step whose layout forks on a
phone is drawn in a `390px` frame, named in its own screen. The shell scales a frame to its
stage; nothing else runs script.

### Screens

- **A system component covers the need** — import it and use it. Its props, variants and states
  are the component's own. The content changes; the component does not.
- **An earlier flow already proposed a component** — import that candidate (`from:
  candidate:<Name>`); the second use is evidence for promoting it.
- **Nothing covers it** — author a **candidate component** under `<dev>/flows/components/` from
  the system's tokens, record it in the ledger, and import it. Never put a candidate in the
  production component tree.

A candidate is a real component in the project's stack, typed, with the states the ledger
records. When the user promotes or folds it, it moves into the real component set and the
viewer, and every flow that imports it switches to the system component.

## The index

`docs/flows/README.md` carries:

1. One line on what the flows are, and that they run as dev routes (`/uikit/flows`), hidden
   outside local and preview.
2. **What they are for:** onboarding, and the base a build takes routes, components, copy and
   decisions from.
3. **Inside a flow:** the section order above, shortened.
4. **Rules that keep drift down:** a screen built from the system imports the system component;
   a new feature starts from the closest existing flow; screens are static with mock values;
   nothing outside the system's tokens; every drift is in the ledger, and the run that draws a
   new drift asks whether it joins the design system or stays a one-off.
5. **The index:** a table per group, `# · Feature (linked to its route) · Definition · Steps`.
6. **Mock values:** today's date, the cast, the sample records every flow uses. A flow that
   needs a new value adds it here first.
