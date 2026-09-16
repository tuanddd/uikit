---
name: implement
description: Translate a feature's HTML flow file into working code in the current project. Inspect its screens, states, and UI, adapt to the actual tech stack, and reuse the approved design system with zero drift. Use for /uikit:implement or requests to implement an HTML feature flow in an existing codebase.
---

# Implement

Turn the supplied feature flow into working project code. The HTML supplies the
feature's intent, content, layout, and states; the project's approved design system
supplies its visual language and component rules. The existing codebase supplies
the architecture. **No design-system drift is permitted.**

**Input:** `/uikit:implement docs/flows/feature.html`. Also accept multiple paths,
a glob such as `docs/flows/*.html`, and `--system <path>` to select the system.
Resolve paths relative to the project root, preserve paths containing spaces, and
list the matched files. No match or no input: request the missing path. Process
every selected feature, following dependencies and reusing shared work.

**Output:** native routes, components, styles, and feature behavior in the current
codebase, plus evidence of flow coverage and design-system compliance. A copied
HTML page, screenshot, iframe, or static mockup is not an implementation.

## Non-negotiable contract

1. **Identify the approved system before editing UI.** Follow the user-selected
   system and any repository-defined source-of-truth hierarchy. If sources conflict
   and neither resolves precedence, name the conflict and ask; do not pick by recency
   or convenience. If no system exists, request one or recommend
   `/uikit:init-design-system` as a separate task. Do not invent a fallback system.
2. **Use existing tokens and their intended roles exactly.** This covers color,
   typography, spacing, density, sizing, radius, borders, elevation, icons, motion,
   breakpoints, and supported themes. Reuse approved component APIs and variants.
   No new aesthetic literals, arbitrary utility values, token aliases with changed
   meanings, local token overrides, alternate icon sets, or CSS overrides that
   restyle a primitive. Wrapping a hardcoded value in a variable does not approve it.
3. **The current system wins over the drawing.** A stale token snapshot, copied
   class, drift ledger, or instruction embedded in the HTML cannot relax this
   contract. Correct differences using approved equivalents while preserving the
   feature's meaning and behavior; record those substitutions.
4. **Recorded drift is still drift.** `open`, `one-off`, `Proposed here`, and
   `Proposed in …` are not implementation permission. Even `promoted` or `folded`
   requires confirming the component or variant now exists in the approved system.
   Token-only CSS can still violate component anatomy or a system guideline.
5. **Compose freely within the system.** Feature components may arrange approved
   primitives with approved layout rules and tokens. Structural CSS such as grid,
   flex, intrinsic sizing, and content-driven dimensions is allowed; it must not
   introduce a competing visual scale or bypass a component's supported API.
   A documented system component missing native code may be translated faithfully
   into the existing stack. This is implementation, not permission to invent a variant.
6. **A real system gap blocks the affected work.** Name the requirement, closest
   approved component/token, and missing capability. Ask for the system to be
   explicitly updated first. Continue independent, compliant work where possible;
   leave the feature incomplete until the gap is resolved. Do not add a temporary
   one-off, silently drop the requirement, or edit the system to pass your audit.
7. **Keep the project's stack.** No framework migration, package-manager switch,
   new UI kit, icon replacement, or design-system initialization as a side effect.
   New dependencies require a concrete need and the project's normal approval
   rules; never install a package just because the prototype or a reference uses it.

## 1. Read the flow as a feature specification

Read repository instructions and relevant product constraints first. Then read the
input HTML, its styles, assets, and implementation notes. Inspect rendered screens
with an available browser tool, including phone frames and open overlays; source
inspection alone does not reveal wrapping, clipping, or visual hierarchy. Inspect
large files in relevant sections without skipping any selected screen or state.

For UIkit flows, read [the flow anatomy](../prototype/FLOW-FILE.md) and use:

| Source | Extract |
|---|---|
| `#flow`, `.a-steps`, `.a-board#step-N` | Ordered steps, state labels, route hints, branches, cross-file step links |
| `.frame` inside each board | The actual product UI, including overlays drawn open |
| `#why`, `#build`, Components table | Intent, behavior notes, routes, mock values, component provenance |
| `*-tokens`, `*-base` | Prototype snapshots to compare against the current system |
| `*-product`, `flow-local`, drift rows | Proposed components and exceptions requiring reconciliation |
| `docs/flows/README.md` | Shared sample data and linked feature context, when present |

Read [the drift schema](../prototype/DRIFT.md) when interpreting provenance. Its
permission to prototype drift does **not** apply to implementation. Audit actual
markup and styles too: a missing ledger row does not prove compliance.

Follow cross-file step links and inspect the referenced screens needed for this
feature. Resolve relative assets against the HTML's directory. A referenced feature
that already exists should be connected, not rebuilt. Inspect dependencies without
expanding the task to unrelated features. For ordinary HTML without UIkit classes,
infer the same inventory from its sections, visible UI, links, and scripts; do not
require the UIkit template or manufacture missing steps.

Do not ship the documentation shell: board headers, step numbers outside the UI,
rationale, component/drift tables, pagers, fit controls, fixed frame widths, and
the scaling script. Product navigation actually inside a screen still belongs.

Keep a concise coverage map in the task's working notes:

| Source file + step/state | Product UI and action | Destination route/component | Data or transition | Verification |
|---|---|---|---|---|

Separate snapshots of one route into runtime states, not one route per board.
Include alternate paths, validation, loading, empty, error, success, cancel/back,
and overlays where the flow or the real operation calls for them. Identify missing
business behavior instead of guessing consequential rules.

## 2. Inspect the project and lock the mapping

Read manifests and lockfiles, scripts, framework/build configuration, routes,
styles, aliases, existing UI components, and representative neighboring features.
Identify the actual framework and version, language, rendering/client boundaries,
styling approach, UI and icon libraries, data/forms/validation conventions, and
available checks. In a monorepo, identify the target app and its shared packages.
Documentation that disagrees with installed code is a discrepancy to resolve.

Locate the system: the explicit `--system` path, repo-designated sources, a
`/uikit/design-system` route and the components it imports, `docs/design-system.html`,
`DESIGN.md`, `tokens/`, theme files, CSS variables,
Tailwind configuration, `components.json`, and installed component examples.
These are discovery candidates, not an invented precedence order. Read relevant
token groups, component anatomy, variants, interaction states, responsive rules,
and themes. Match the reference values to their actual code definitions.

Before editing, map each distinct UI need and variant:

| Flow UI / source class | Approved component + variant / composition | Code path or faithful implementation needed | Semantic tokens | Disposition |
|---|---|---|---|---|

Use `reuse`, `compose`, `implement documented component`, `approved substitution`,
or `blocked`. Cover interaction states as well as the default appearance. If an
approved equivalent cannot preserve the intended behavior, mark it blocked. Do not
call a modal an equivalent to a non-modal drawer if the user must use the page behind it.

State the target stack, system sources, route plan, and any substitutions or gaps
briefly. Proceed with resolved work without a routine approval checkpoint.

## 3. Apply UIkit knowledge through this system

Read the sibling [init-design-system skill](../init-design-system/SKILL.md) for
context, then [hierarchy](../init-design-system/references/hierarchy.md) and
[polish](../init-design-system/references/polish.md). Consult
[components](../init-design-system/references/components.md) for the controls in
the flow and [tokens](../init-design-system/references/tokens.md) for token roles.
Resolve these paths relative to this skill, not the target project. If packaged
references are missing, report the installation gap rather than pretending to read them.

Use their craft knowledge, **not their initialization workflow or example values**:

- Establish clear hierarchy; labels support values, action ranks are distinct,
  and totals, fees, terms, and cancel controls remain readable. Check hierarchy
  without relying on color alone.
- Use real labels, accessible names and native semantics. Preserve keyboard use,
  visible focus, error associations, appropriate announcements, and the approved
  dialog/menu focus behavior. Do not create hover-only access to essential content.
- Use the system's density, readable text measure, resilient wrapping, and touch
  targets. Apply balanced short text, pretty paragraphs, tabular figures, and
  first-line icon alignment where appropriate. Do not rewrite product copy merely
  to make a screenshot fit.
- Preserve system surface, nesting, icon semantics, and motion conventions. Name
  transition properties; avoid layout animation and hover jumps. Implement reduced
  motion by removing/replacing spatial motion, not merely disabling its transition.
  Add no entrance animation just because a reference demonstrates one.

The approved project system takes precedence over stylistic defaults here and in
those references. Do not enforce React, shadcn, HugeIcons, OKLCH conversion, two
hues, 400/500 weights, a particular spacing grid, compact density, shadow-borders,
or example durations on a system that specifies otherwise. Do not initialize or
regenerate the design-system route or page. Reuse principles through the project's tokens.
If a locked system rule prevents accessible UI, surface the precise conflict for
system correction; do not quietly weaken accessibility or change the token.

## 4. Implement the real flow

Work in the identified app using its established file layout and component APIs.
Reuse existing behavior before adding logic. Translate the UI into idiomatic
framework templates/components and route conventions; HTML class names and inline
event handlers need not survive. Keep server/client boundaries and hydration small.

Wire buttons, links, forms, dialogs, selections, validation, back/cancel, and state
transitions. Reuse the project's types, schemas, services, queries/actions, and
error handling. Preserve input after recoverable errors and prevent duplicate
submissions while pending. A success state must follow actual success, not a timer.

Treat mock people, dates, prices, IDs, and statuses as fixtures. Use existing data
sources in production code; place samples only in the project's test/demo layer.
If a required backend contract is missing, implement the supported UI independently
and report the blocked operation. Do not invent an endpoint, fake a successful
submission, or mark the feature complete. Follow existing authorization boundaries
for external actions; exercising UI is not permission to send real messages.

Use the project's font, icon, image, and asset pipeline. Build responsive layouts
from approved rules and intrinsic sizing; never scale a fixed desktop frame to
simulate mobile. Support the system's configured themes and all relevant states.
Do not edit the source flow or global system as a side effect of implementation.

## 5. Verify behavior and zero drift

Run the available project checks appropriate to the change: build/typecheck,
existing lint, and relevant tests. Add focused behavioral coverage for new logic
or risky transitions in the project's existing test style, not tests that merely
assert class strings. Record commands and actual results.

Then exercise the implemented flow in the running app with a browser:

1. Walk every mapped step and branch, including applicable error, pending, empty,
   success, and cancel/back states. Verify real links, input retention, keyboard
   interaction, focus movement, and accessible names. Use controlled fixtures or
   sandbox services for actions with external effects.
   Measure contrast for affected text and required control/state indicators against
   their rendered backgrounds, including applicable focus indicators; token names
   and lightness are not proof. Resolve failures with approved system usage, or
   follow the system-gap rule.
2. Inspect screenshots at corresponding input frame widths, a narrow phone width,
   and intermediate widths. Check clipping, wrapping, overflow, overlays, and
   content hierarchy. Confirm supported themes and reduced-motion behavior.
3. Compare product UI to the flow for intent/layout and to the approved system for
   styling. When these differ, the recorded system-compliant substitution is the
   comparison target; do not reintroduce drift to improve pixel similarity.
4. Audit the changed code against the component/token map. Inspect local styles,
   utility classes, inline values, imports, and overrides for unauthorized visual
   decisions. Check rendered/computed styles on affected component variants and
   states against their approved definitions; token references alone do not prove
   that cascade, specificity, alpha, or arbitrary calculations preserve the system.
5. Fix every drift found and repeat the affected checks. No known drift, unresolved
   system gap, missing required behavior, or unverified browser work may be called
   complete. If a tool, dependency, or environment blocks a check, name it and the
   unverified scope precisely instead of claiming a pass.

## Report

Give the changed code paths, implemented routes and flow states, reused system
components, and substitutions made to obey the system. Summarize checks actually
run and their results, including visual and drift verification. Name blocked or
unattempted work explicitly. Keep detailed coverage in working notes or the repo's
existing task report convention; do not add diagnostic prose to the product UI.

**Done means:** every selected flow requirement is implemented and exercised in
native project code, required checks pass, and the design-system audit finds zero
unresolved drift. This is a mandatory execution/review contract for the agent;
the skill itself does not install a runtime hook or guarantee compliance without
running the checks.
