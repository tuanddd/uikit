# Prototype fold-back verification

Date: 2026-09-15
Run: prototype-drift-fold-back
Lane: normal
Spec: docs/specs/SPEC-002-prototype-drift-fold-back.md

## Change

`skills/prototype/SKILL.md` gains Phase 7, *Fold drift back*, which runs at the end of
every drawing run (one feature, several, or `update`). It asks the user one question
per **new drift** the run drew, with a recommended answer: keep as a one-off, fold
into the nearest component, add to the system, or decide later. New drift is open in
a file the run drew and open in at most one other flow file (a first use, a second
use, or a reused one-off), plus every open guideline drift in those files. Guideline
drift gets its own two answers. Drift already open across several flows is listed in
one line and left to `/uikit:prototype drift`. Hard rule 11 makes the questions
mandatory; hard rule 10 still keeps production code untouched.

`DRIFT.md` describes the two entry points into one review procedure, the answer
order, guideline and replaced-drift handling, and names installed components for
`/uikit:implement` instead of writing them. `FLOW-FILE.md`, both READMEs and the
plugin version (0.3.0) follow.

`scripts/drift-report.py` gains `--file` (repeatable; keeps counting every file that
uses each drift; rejects anything that is not a flow file in the given directory)
and `--new` (requires `--file`; applies the new-drift test). JSON output gains an
additive `open_in` list. The table output without filters is unchanged.

The installed Codex copy, `~/.codex/skills/uikit-prototype`, received the same diff
with its naming substituted.

## Structural validation

```sh
uv run --with pyyaml python ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py ~/.codex/skills/uikit-prototype
uv run --with pyyaml python ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py ~/.claude/skills/uikit/skills/prototype
```

The Codex copy exited 0. The plugin copy exited 1 with `Unexpected key(s) in SKILL.md
frontmatter: disable-model-invocation`. The same command against the skill as it was
at HEAD, extracted with `git archive`, fails identically: the validator only knows
Codex frontmatter keys, and `disable-model-invocation` is a Claude Code key the skill
already carried. Not a regression.

An inline Python check parsed `plugin.json` (uikit 0.3.0) and resolved every relative
Markdown link in `README.md`, `skills/` and `docs/`, with none missing.

The Codex copy was patched from the plugin diff with `/uikit:prototype`,
`/uikit:init-design-system` and the skill path substituted. For `SKILL.md`,
`DRIFT.md`, `README.md`, `FLOW-FILE.md` and `drift-report.py`, the normalized
difference between the two copies after the change equals the difference before it:
only the pre-existing Codex naming and tool notes remain. Patch backup files were
moved out of the skill directory. A scan of both copies and the spec for retired
wording (`Then stop`, `later decides`, `reviewed with`, `drift the run added`) found
none.

## drift-report.py

The HEAD script was extracted as the control.

Real flows: the Wu and Kin site's `docs/flows`, read-only, 53 open drifts.

| Case | Result |
|---|---|
| No filter, HEAD script against the new one | Identical table output: 53 drifts, 43 shared |
| `--file v2-03-signed-documents.html` | 17 rows, equal to the rows naming that file in the unfiltered report; each still lists every file using it (Breadcrumbs: 25) |
| Two `--file` flags | 21 rows, equal to the rows naming either file |
| The file given as `docs/flows/…` and as an absolute path | 17 rows each |
| The same file name in another folder | Exit 1, `not a flow file in …` |
| `--file v9-99-nope.html` | Exit 1, `not a flow file in …` |
| `--file v2-03-signed-documents.html --new` | 4 new drifts: Document page, Signature block, Stamps (2 files each), Clause (1); 13 already open across several flows |

Fixture: five minimal flow files in the session scratchpad, where `c.html` is the
file a run just drew.

| Drift | Ledger rows | `--file c.html --new` |
|---|---|---|
| Tile | open in c | Asked: first use |
| Drawer | open in a, c | Asked: second use |
| Chip | one-off in b, open in c | Asked: a reused one-off |
| Two primaries (guideline) | open in a, c, d, e | Asked: open guideline |
| Legacy | open in c, d, e | Not asked: open in two other flows |

With `--file c.html --file d.html --new`, Legacy is asked too, since only `e.html`
lies outside the run. `--new` without `--file` exits 2 with `--new needs at least one
--file`. `--json` rows carry `open_in`.

Asking about every open drift a flow uses was rejected on this evidence: one real
flow would have produced 17 questions, 13 of them about drift already open across
several flows.

## Independent review

A read-only reviewer read the change against nine scenarios: a run with a one-file
detail and a two-file component, a run with no drift, a two-feature run, an update,
*Decide later*, drift the system now covers, guideline drift, contradictions across
all files, and the script diff.

**First pass:** seven scenarios passed, guideline drift was partial, and the
contradiction scan failed. Nine findings were repaired:

1. DRIFT.md asked to write installed components during a review, against hard rule
   10. It now names them for `/uikit:implement`.
2. Guideline answers had no apply step; they now have statuses and no CSS move.
3. Replaced drift had no follow-through, and the completion criterion demanded an
   answer it never gets. Both now spell out the replacement.
4. Overlapping recommendation criteria are now ordered: one-off, fold, promote.
5. A multi-feature run could reach Phase 7 after its first file; it now waits for the
   last file's report.
6. `FLOW-FILE.md` pointed at the separate review, and the Codex copy held a `.orig`
   file. Both fixed.
7. An `update` re-asked rows answered earlier; only rows it added count now.
8. "Nothing is applied before the answers" read as contradicting the replacement
   step. Reworded.
9. `--file` ignored directories; it now rejects paths outside the flow directory.

**Second pass:** all nine held. The first scoping rule ("used by at most one other
file") introduced four gaps, all repaired:

1. A reused one-off shared by two or more flows was never asked about. New drift now
   counts files where the drift is still open, so a reused one-off qualifies.
2. A new guideline exception merged with earlier rows and went unasked. Open
   guideline drift now always qualifies.
3. "Added" meant two things. The term is now *new drift*, defined once and used in
   hard rule 11, the completion criterion, the READMEs and the spec; the update case
   applies the same test to the rows the update added.
4. Rows not asked about never got the reuse test. Step 2 now re-checks every open
   drift in the tally and names covered non-new drift for the on-demand review.

**Final pass:** all four gaps held, and the Codex copy matched the plugin apart
from naming. Three smaller points were fixed in wording, without a further pass:

1. In an `update`, `--new` also returns rows from before the update. The agent
   narrows the tally to the rows it added, and the one-line list names kept rows as
   such. The script cannot tell which rows an update added, so this narrowing is the
   one step it does not do.
2. DRIFT.md now scopes Phase 7 the way SKILL.md does: questions for new drift, after
   a reuse re-check of every open drift the run's files use.
3. Covered drift in a file the run just drew is replaced there instead of deferred,
   so hard rule 2 holds in the run's own files.

The reviewer also noted that drift reused from flows drawn before Phase 7 is always
listed rather than asked, and piles up if nobody runs the on-demand review. Phase 7
now offers to go through the listed drift before the run ends.

## Limitations

- No live `/uikit:prototype` run was attempted. It needs the paid Mobbin MCP and a
  full drawing session, so an agent asking the fold-back questions was not observed.
  The phase was verified through the instructions, two review passes and the script
  behavior above.
- The ledger has no deferred status. A row answered *Decide later* stays `open`,
  indistinguishable from one never asked, so it is asked again only while it still
  counts as new drift, or in the on-demand review.
- Skill instructions are an execution contract, not a runtime hook.

## Scope and operational notes

Committed on `feat/prototype-drift-fold-back` and pushed on the user's request; the
merge to `main` is not part of this change. The Codex copy lives outside this
repository and was updated in place, with its previous state kept in the session
scratchpad.
