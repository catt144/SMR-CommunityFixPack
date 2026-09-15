# 02 - Evictions

Move the closed chains to the archive and the arming infrastructure to tools,
preserving their bytes and repairing live consumers. Execute after leg 01 lands.
Produce the commits below; do not execute any other leg.

Authored against `b5662a4`. Owner override authorizes these briefs in
`C:\Dev\SMR-BugFixPack\zz-owner`; it does not lift the prompts firing freeze.

## Live progress

- [IN PROGRESS - not executed] Archive prelaunch-sweep, vanillahunt, smrtk and
  hotfix2; repair live citations/map and remove their gate migration allowances;
  verify and commit the mechanical move.
- [PENDING - waits for archive commit] Move arming to tools, repair consumers and
  remove its migration allowance; verify and commit, consuming this brief.

Update the list as each commit lands. If a unit splits, split its item immediately;
exactly one unfinished unit is in progress, with real state in its text.

## Read path and constraints

Start with `git log --oneline -6`, `git pull`, `git status --short`. Read
`.claude/promptsrot/00_CHAIN_SPEC.md` completely and the relevant answered
2026-09-15 rulings in `.claude/DECISIONS.md`. Apply `doc-editing`; read target
Must_Read_Headers. Read `docs/README.md`, `docs/agent/prompts/README.md`,
`tools/arm_leg.ps1`, and the PROMPT MAP migration handling in `tools/doccheck.py`.
For closure evidence read only these entry files initially:

- `docs/agent/prompts/prelaunch-sweep/00_CHAIN_SPEC.md`
- `docs/agent/prompts/vanillahunt/README.md`
- `docs/agent/prompts/smrtk/README.md`
- `docs/agent/prompts/hotfix2/README.md`
- `docs/agent/prompts/arming/README.md`

Inventory descendants for the move without reading their bodies as orientation.
Open a specific additional file only when a consumer or manifest points to it.
Preserve the prelaunch H-05 fence: never read `SWEEP_FINDINGS.md` to reach a verdict.
For defect/fact questions, search `docs/agent/bugs/INDEX.md` or
`docs/agent/facts/INDEX.md`, then the matching entry section; no whole-folder reads.
Read STATE only if the citation search identifies a live reference to repair.

The spec's fixed rulings remain fixed: prompts only, map retained, evidence allowed
in live chains, closed chains leave, RELEASE_OUTBOX is the ledger exception, one
lean release prompt, CO_RUNS becomes support, SMRTK_SLOTS reference stays here,
and the specified purges proceed in their owning leg. Replies have one pull-only
source, `docs/FIELD_REPORT_REPLIES.md`, with the owner as transport; write no rule
about them. CUT is the default; retention needs a written reason. These moves are
verbatim because the owner authorized preserving records and infrastructure.
Never edit `LINUX_DISPATCH.md` or `HANDOFF_ORCHESTRATOR.md`. Do not fire any prompt
in `docs/agent/prompts/`; only the owner can lift the freeze after chain completion.

## Moves and scope

Move each named closed chain from `docs/agent/prompts/<name>/` to
`docs/archive/prompts/<name>/`. Move `docs/agent/prompts/arming/` to `tools/arming/`.
Check resolved destinations first; never overwrite an existing archive entry.
Archive content is append-only. Preserve relative descendant paths and bytes.

Sweep live docs and functional code consumers in the corresponding move commit.
Search the old full paths, relative paths, and path construction using `arming`;
inspect each hit before calling it a dependency. `tools/arm_leg.ps1` is a required
consumer check: repair its references and any runtime path construction that
actually resolves to the old directory. Do not infer a runtime dependency merely
from a comment. Check other tools for the same dependency. Preserve arming behavior.
Update map descriptions as well as paths and retire each gate migration allowance
in the commit that removes its source.

Do not sweep `docs/agent/reports/`, `docs/agent/bugs/`, `docs/agent/facts/`,
`docs/archive/` or dated record entries. Records keep historical paths, including
the newly archived bodies. Do not rewrite infrastructure bodies for style. If a
functional consumer inside the moved infrastructure needs a path change, separate
and explain that necessary exception; preserve everything else byte-for-byte.

Out of scope: perma purges/trims, release work, live-chain review, game code and
playtests. Route a finding to its owning brief in `zz-owner/`; if not yet authored,
bank it in `.claude/SEAT_WORKLIST.md` V6 with its leg number. An exempt handoff
reference belongs to the next handoff session, never this sweep. No overhaul
reports/checklist items in house docs and no repairs licensed just by discovery.

## Evidence

Inherited inventory: spec section 4 measured these directories at `0020c33` using
an os.walk file-size inventory. Re-emit before moving with this PowerShell-safe
command, alongside `git rev-parse HEAD`:

```powershell
@'
import os
for d, _, fs in os.walk('docs/agent/prompts'):
    print(sum(os.path.getsize(os.path.join(d,f)) for f in fs), d, len(fs))
'@ | python -
```

Falsify staleness with `git diff --stat 0020c33..HEAD -- <source paths>`;
recheck only changed groups. Record relative file names, SHA-256 hashes, lengths
and totals before and after each move. Compare the renamed inventories: fail on
a missing/extra file or changed byte sequence except a declared functional repair.
Every reported count carries its emitting command, filter, HEAD and reconciled
members; unexecuted figures are `<<PENDING-RUN>>`.

For each old and new path, use `git grep -n -F -- <path>` (includes tracked archive)
plus explicit `rg -n -F -- <path> .claude/ zz-owner/` for local materials. Count
actual path citations before and after, classify historical/exempt/live hits,
and prove the remaining live unresolved set is empty. Count destination presence
too. Search relative forms and constructed tool paths separately; a word match
is not a citation. Decode compressed inputs if used in an absence claim.

After the arming move, run its `-SelfTest` through PowerShell and verify consumer
path resolution against the moved files without arming the game or modifying the
TestKit installation. Run `python tools/doccheck.py` before each commit. Regenerate
only when needed, inspect peer bug/fact changes first, and review generated diffs.

## Stop, land, consume

Stop and report on dirty/peer-owned targets, destination collisions, RED outside
this lane, contradictory authority, a missing owner decision, changed meaning,
lost owner rulings, an unprovable cut/move or an unopened destination passage.
Recheck status immediately before writes; attribute shared-tree work by SHA/diff.

Use `git commit -F <msgfile> -- <exact paths>`, without bypassing hooks or switching
the main checkout's branch. Append findings to their owning leg, then `git rm`
this brief in the final result commit. Report commits, evidence, DEPARTURES and
SUGGESTIONS; record the executed model from the transcript without guessing.
Do not claim "the folder is clean", "GREEN therefore correct", or "nothing cited
it" from a default rg. Say exactly what moved and what historical/exempt references
remain. This one-off ends after its own commits; the full chain is not complete.
