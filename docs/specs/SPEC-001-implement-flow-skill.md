# Implement feature flows

Lane: normal
Type: spec-feature

## Context

Add `/uikit:implement <flow.html>` to the existing UIkit plugin. The input describes
a feature across screens and states. Translate its UI into the current project's
native stack, using the existing design system without drift. Reuse the knowledge
in `init-design-system` without imposing its initialization defaults on a project.

Grill: skipped; the user's request resolves input, output, stack adaptation,
knowledge source, and strict design-system fidelity.

Done = the plugin exposes an implementation skill that maps the complete flow to
native components and behavior, refuses design-system drift, passes structural
validation, and is exercised independently against a representative fixture.

## Acceptance criteria

- Accept a local HTML file or glob; read rendered screens, states, transitions,
  linked steps, component sources, and drift records without shipping flow chrome.
- Inspect actual project configuration and component usage before choosing an
  implementation. Do not require a framework, UI library, or icon migration.
- Require an identified design system, approved token/component mapping, and
  zero unresolved drift before claiming completion. Recorded prototype drift
  does not authorize production exceptions.
- Reference the existing hierarchy, polish, token, and component knowledge;
  project conventions outrank initialization defaults.
- Implement real feature behavior and verify flow coverage, responsive rendering,
  accessibility, and design-system fidelity with honest evidence.
- Update plugin discovery documentation and the existing Codex skill installation.

## Design record

One new skill directory in the existing plugin; sibling references remain the
knowledge source. No additional runtime, package dependencies, hooks, or automatic
design-system modification. The Codex installation mirrors the instructions with
its existing skill naming and sibling paths.

## Verification

Run `quick_validate.py` on the plugin skill and its Codex copy. Validate plugin
JSON and relative references. Independently execute the skill in a temporary
project with an HTML flow and existing system, and probe a drift case. Record the
commands, outcomes, review, and limitations in `docs/verification/implement-flow-skill.md`.

## After state

The plugin has three skills: initialize, prototype, and implement. Implement
produces project code within the approved system; unresolved system gaps block
the affected work. No website feature implementation or remote publication is
part of this change.
