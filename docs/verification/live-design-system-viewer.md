# Live design-system viewer verification

Date: 2026-09-16
Run: live-design-system-viewer
Lane: normal
Spec: docs/specs/SPEC-003-live-design-system-viewer.md

## Change

`/uikit:init-design-system` now produces a **live route** `/uikit/design-system` in the
project's own stack instead of a static `docs/design-system.html`. The route's token sections
print values from `tokens.json` and fill swatches from the CSS derived from it; its
Components section imports the project's real components. The viewer is hidden outside local
and preview by an env gate plus dev-surface hygiene. The static HTML survives as a fallback
only, for a project with no hostable route.

Non-React stacks gained native component authoring. React keeps shadcn/Radix; Svelte uses
Bits UI; Astro uses native `.astro` components with platform-first progressive enhancement.
Astro and Svelte now have a live route and authored components; Vue/Solid/Qwik and buildless
projects fall to the static page.

Files: `SKILL.md` rewritten; `references/shadcn-setup.md` replaced by `references/setup.md`;
`references/stacks.md` and `references/viewer-spec.md` added; `references/html-spec.md`
demoted to the fallback spec; `references/tokens.md`, `components.md`, `hierarchy.md`
generalised (CSS variables are the contract, the shadcn names one mapping). Plugin
`README.md`, `skills/what/SKILL.md`, `skills/implement/SKILL.md`, the skill `README.md` and
`plugin.json` (0.5.0) follow. The Codex copy `~/.codex/skills/uikit-init-design-system`
received the same diff with its naming substituted.

## Structural validation

`quick_validate.py` needs PyYAML, absent from the system Python, so it ran in an isolated
venv (no global change):

```sh
python3 -m venv qv && ./qv/bin/pip -q install pyyaml
./qv/bin/python .../skill-creator/scripts/quick_validate.py ~/.claude/skills/uikit/skills/init-design-system
./qv/bin/python .../skill-creator/scripts/quick_validate.py ~/.codex/skills/uikit-init-design-system
```

Both exited 0 with `Skill is valid!`. The sibling skills were validated too: `what` and
`implement` pass; `prototype` exits 1 on `Unexpected key(s) in SKILL.md frontmatter:
disable-model-invocation`, a pre-existing Claude-Code frontmatter key the validator does not
know. Not a regression and out of scope.

An inline Python check resolved every relative Markdown link across `README.md`, `skills/`
and `docs/`: all resolve. A second check extracted every `var(--…)` reference from
`viewer-spec.md`, `setup.md` and `components.md` and diffed it against the tokens defined in
`setup.md`'s `:root`: the only unmatched names are the prose wildcards `--radius-*` and
`--space-*`. Every real token consumed by the viewer and the examples is defined.

Every edited file has an even number of ``` fences. `rg wuk-` across the skill is empty.

The Codex copy was patched from the plugin copy. `diff` between the two is only the SKILL.md
frontmatter `name` line and the README install/use section; every reference file is
byte-identical.

## Independent review

A read-only reviewer read `SKILL.md`, `stacks.md`, `setup.md`, `viewer-spec.md` and the
READMEs against three scenarios — Next.js App Router, Astro, SvelteKit — and checked
contradictions, leftover static-HTML primacy, the no-drift claim, achievability of the
production gate, Astro primitive concreteness, and cross-references.

**First pass:** 14 defects. The load-bearing ones: `--space-*` was never emitted in the
injected `:root` though the viewer shell reads it; `--shadow-none`, `--radius-full`, and the
`--radius-*` scale outside Tailwind v4 were undefined; the Astro `Icon.astro` example was a
no-op that imported symbols from a module never specified to export them; the env helpers
read `process.env` for stacks that expose `import.meta.env`/`$env`; the SvelteKit gate named
two different files; Next `src/app/` was misclassified; the `tokens.json` ↔ CSS "cannot
drift" claim was overstated with no single source. All 14 were repaired:

1. `--space-1…16`, `--radius-sm/md/lg/xl/full`, `--shadow-none` added to `:root` as raw
   custom properties, with a note that the viewer and examples read them directly.
2. The stray `var(--wuk-space-2)` corrected to `var(--space-2)`.
3. Per-stack env helpers added (React `process.env`, SvelteKit `$app/environment` +
   `$env/dynamic/private`, Astro/Vite `import.meta.env`), and the table row reconciled.
4. SvelteKit gate unified on `+page.server.ts` (`error(404)`).
5. Svelte component layout unified on flat `.../ui/<name>.svelte`.
6. Next detection accepts `app/` or `src/app/`; the route row names both.
7. `icons.ts` and a working `Icon.astro` supplied; proved against a real HugeIcons node
   shape.
8. Tailwind v3 got a `tailwind.config.js` mapping to the `var()` tokens; the v4-only imports
   are marked as such.
9. Static-output gating rewritten: build the preview with the override, host redirect where
   available, and an explicit `[UNAVAILABLE: …]` path that forbids claiming a gate that does
   not exist.
10. `tokens.json` made the single authored source, the CSS its projection, with `setup.md`,
    `tokens.md`, `SKILL.md`, `viewer-spec.md` and both READMEs aligned.
11. Astro interactive primitives specified platform-first (`<dialog>`, `popover`, native
    `input`/`select`) with a concrete Dialog and a keyboard/ARIA verification list.
12. `data-dev-surface` added to the shell and the checklist; the prod-gate item reworded;
    helper paths and "What lands" completed.

**Second pass:** defects 3, 5, 6, 9, 10, 11, 12, 13 resolved; 1, 2, 4, 7, 8 resolved with a
new finding each. Four new defects were then fixed:

1. Stroke tokens were emitted as an SVG `stroke-width` **attribute** (`var()` does not
   resolve in presentation attributes); moved to `style`.
2. SvelteKit's override read `import.meta.env.PUBLIC_…`, which SvelteKit does not expose;
   switched to `$env/dynamic/private`.
3. Two README lines still said the viewer "reads the real CSS variables" / "cannot drift,
   because it is the system"; aligned to the `tokens.json`-canonical model.
4. Two icon rules numbered `3.`/`3a.`; renumbered 1–10.

**Third pass:** the four held. The reviewer's remaining notes are that `setup.md`'s
"What lands" lists only the primary route path (the `src/`-prefixed and Pages/Remix/Vite
variants live in `stacks.md` § 2, which is the normative table) — a pointer, not a
contradiction.

## Limitations

- No live run of the skill against a real Next/Astro/Svelte project was attempted. The skill
  is an execution contract, not a runtime; it was verified through the instructions, three
  review passes, and the static checks above. The route file paths, primitives, and env
  helpers were checked against each framework's documented conventions, not executed.
- The Astro interactive-primitive guidance gives a coded Dialog and a platform-first spec for
  Dropdown/Select/Tooltip; each still needs the keyboard/ARIA check named in `setup.md` when
  a real project authors it.
- The prototype skill (`skills/prototype/`) still sources its flow files from
  `docs/design-system.html` (`SKILL.md`, `DRIFT.md`, `FLOW-FILE.md`, templates). It was left
  untouched deliberately: changing its source-of-truth is a separate decision. With the HTML
  now fallback-only, a React/Astro/Svelte project gets the route and no HTML, so the
  prototype skill's sourcing needs a follow-up.
- The static-output gate cannot be stronger than the host allows; the `[UNAVAILABLE]` path
  records that honestly rather than over-claiming.

## Scope and operational notes

Branch `feat/live-design-system-viewer`; not committed or pushed in this session. The Codex
copy lives outside this repository and was updated in place.
