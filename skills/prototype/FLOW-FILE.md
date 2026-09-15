# The flow file

One static HTML file per feature. It shows the feature as a flow, start to end, one screen per step, with the reasoning and the build notes beside it. It is the reference a build starts from and the baseline the next feature is drawn against, so every file has the same anatomy.

Where the project already has flow files, they are the format: copy the closest one. This page is the format for a project's first file, and the checklist for every file after it.

## Where it lives

```
docs/flows/
  README.md                      index, mock values, the rules that keep drift down
  <group>-<NN>-<feature>.html    e.g. v1-10-inquiry.html, v2-03-signed-documents.html
```

`<group>` is the roadmap phase or product area; `<NN>` the feature's position in that list; `<feature>` kebab-case. When the existing files name themselves differently, follow them.

## The head

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{Feature} · {group} flow · {Product}</title>
  <link rel="stylesheet" href="{the design system's web-font stylesheet}">
  <style id="{prefix}-tokens">…</style>
  <style id="{prefix}-base">…</style>
  <style id="{prefix}-product">…</style>
  <style id="flow-doc">…</style>
  <style id="flow-local">…</style>
</head>
```

The doctype is required: without it the file renders in quirks mode, where tables stop inheriting colour and font.

`{prefix}` is a short project slug (`wuk`, `acme`). Existing files already set it; keep theirs.

## The style blocks

| Block | Holds | Comes from | In |
|---|---|---|---|
| `{prefix}-tokens` | The `:root` custom properties, and `@font-face` rules if the system self-hosts | `docs/design-system.html`, verbatim | every file, identical |
| `{prefix}-base` | The system's components, scoped under `.frame` | `docs/design-system.html` | every file, identical |
| `{prefix}-product` | Components flow files proposed that are not in the system yet | flow files | every file, identical |
| `flow-doc` | The page around the screens: header, bar, boards, tables, pager, fit script styles | [templates/flow.html](templates/flow.html) | every file, identical |
| `flow-local` | This feature's one-off drift | this file | this file only; omit when empty |

The four shared blocks are byte-identical across `docs/flows/`. Change one in one file, then copy it into the rest with `scripts/sync-blocks.py`; `--check` fails when any file differs.

For a project's first flow file, build `{prefix}-tokens` and `{prefix}-base` from the design-system page's own `<style>`: the token declarations, and the CSS of each component scoped under `.frame` so the page chrome stays untouched. Then point the chrome variables at the top of `flow-doc` (`--a-serif`, `--a-sans` and the `--a-*` colours) at the system's font and neutral tokens.

## The body

In this order. Class names are the template's.

| Section | Markup | Holds |
|---|---|---|
| Header | `header.a-head` | `h1` the feature · `p.a-meta` group, step count, frame width, "Static, mock values" · `p` the flow start to end in one paragraph · `figure.a-road` the requirement line, quoted, and where it comes from |
| Bar | `nav.a-bar` | Link to the index, the section anchors, the Fit width / Actual size toggle |
| The flow | `section#flow` › `ol.a-steps` | Every step in order: number, title, state, route, linking to `#step-N` |
| Steps | `section#steps` › `article.a-board#step-N` | One board per step |
| Why it looks like this | `section#why` › `table.a-tbl` | Decision · Rests on · Confidence (`a-conf--ref` for reference, `a-conf--pr` for principle) |
| Building on it | `section#build` | Routes and mock values as `a-card`s · the Components table · the drift ledger |
| Pager | `nav.a-pager` | Previous and next feature in the index |
| Foot | `p.a-foot` | Part of `docs/flows`, the date it was drawn, what it was drawn on |

A heading has no small label above it, in the chrome or in the screens.

### A board

```html
<article class="a-board" id="step-2">
  <div class="a-bh">
    <span class="a-num">2</span>
    <h3>Inquiry, step 2: how to reach you</h3>
    <span class="a-state">One reply channel</span>
    <code>example.com/homes/house-name/ask?step=2</code>
  </div>
  <p class="a-why"><b>Rests on</b> Zillow contact form · Airbnb names the recipient · Mobbin MCP</p>
  <div class="a-stage">
    <div class="frame">…the screen…</div>
  </div>
</article>
```

- `.frame` has a fixed width: 1280px for a desktop screen; `.frame frame--phone` is 390px, for a step whose layout forks on a phone. Follow the widths the existing files use.
- The fit script scales each frame to its stage; nothing else in the file runs script.
- The screen is static markup built from the base, product and local blocks.
- An overlay (dialog, drawer, menu) is drawn open, in place, over the page it opens from, with its scrim.
- A step another flow file already draws is not a board: its row in the flow list links to `other-file.html#step-N`.

### The Components table

| Component | Class | From | Steps |
|---|---|---|---|
| Button | `.btn` | docs/design-system.html | 1, 2 |
| Channel row | `.channel` | Proposed in v1-13-direct-contact.html | 2 |
| Drawer | `.drawer` | Proposed here | 2 |

Every class used inside a frame is in this table. `From` is `docs/design-system.html`, `Proposed in <file>`, or `Proposed here`. Every row that is not `docs/design-system.html` also has a row in the drift ledger ([DRIFT.md](DRIFT.md)).

## The index

`docs/flows/README.md` carries:

1. One line on what the files are, and that they open in a browser with no build step.
2. **What the files are for:** onboarding, and the base a build takes routes, components, copy and decisions from.
3. **Inside a file:** the sections table above, shortened.
4. **Rules that keep drift down:** the shared blocks are identical in every file; a new feature starts as a copy of its closest file; screens are static with mock values; nothing outside the system's tokens; every drift is in the ledger, and the run that draws a new drift asks whether it joins the design system or stays a one-off.
5. **The index:** a table per group, `# · Feature (linked) · Steps`.
6. **Mock values:** today's date, the cast, the sample records every file uses. A file that needs a new value adds it here first.
