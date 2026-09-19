# GAME_PATCH_PROMPT — triage a game patch against both packs

A reusable job: keep it after each run. Fire it when a new game build is on disk (Steam `buildid` in
`appmanifest_3215050.acf` differs from the newest `C:\Dev\SMR-SrcArchive\` version) or the owner asks.
Built 2026-09-19 by `GAME_PATCH_BUILD_high.md` from `reports/GAME_PATCH_INSTRUMENTS.md`; check
`git log -- tools/patchcheck.py docs/agent/prompts/perma/GAME_PATCH_PROMPT.md` before inheriting its facts.

## Decided (owner, 2026-09-18/19): not yours to reopen

- **This prompt runs in the fix pack first, always.** At patch time players cannot switch off
  single fix modules. The opt-in pack is swept by the same command and gets an outbox entry in its fork.
- **Verdict limits:** scoped at ≤ 12 flagged modules, full above that, above 1,000 changed hand
  declarations (T), with a base-class structure change (B) or broken fpk parity. These are **budget
  defaults, not measurements**; step 9 revisits them.
- **In game:** the unattended suite A/B runs on scoped or full only. On none, the boot census is due
  at the next sitting: that is a 24 h gate, never a block.
- **Dependencies are harvested from module text (D1), never stamped.** Do not add `SRC:` lines to
  make a module visible to the sweep.
- **Patch notes are fetched by the tool and can only escalate.** They may add a module to the read
  list or raise the verdict, with the stated line; they never drop a module or lower a verdict.
  (1.1.0's notes named none of our ten breakages.)
- No fire-rate counters and no `Code/` edits in this job. A defect goes to a FIX prompt.

## Work list: put it in the todo tool before the first write

One item per step below. Each item ends with a token line (`tokens: ~N`, your estimate of what the
step cost), marked as it lands. The 1.1.0 response recorded no cost; this list is the record.

## Steps, in order

1. **Archive.** If `patchcheck` says `A NOT archived`, copy the live `ModTools\Src` to
   `C:\Dev\SMR-SrcArchive\<BuildVersion>\Src`, write its `MANIFEST.sha256` by the archive README's
   recipe, and add the README row. Stop the job until this is done: nothing downstream is valid
   without the old tree (`EF-075`).
2. **Sweep.** `python tools/patchcheck_selftest.py` (GREEN, ~20 s), then
   `python tools/patchcheck.py --code Code --code C:\Dev\SMR-OptInPack\Code > <scratchpad>\patchcheck.txt`
   (defaults: newest older archive → the live install). Also `python tools/bodycheck.py` for the
   `DEFECT-GONE` candidates D1 does not look for. Open the run report
   `docs/agent/reports/GAMEPATCH_<BuildVersion>_<date>.md` and paste the patchcheck block verbatim.
   Every count in the report comes from that block; none is typed.
3. **D3 rows first.** Each D3 row is a save-exposure site whose call contract moved. It is a FIX row
   whatever the verdict: read the call and the reached declaration in both trees before anything else.
4. **Act per verdict.**
   - **stop**: step 1.
   - **none**: file the D5 list as one checklist rider; go to step 6.
   - **scoped**: per module in M, read every flagged row in both trees and give a FIX / REMOVE / KEEP
     verdict. A REMOVE traces the replacement body (R-15: a rename reads as "gone"). D2 ranks
     `incompatible` above `prefix-compatible`; a `prefix-compatible` row still gets its body read.
   - **full**: every module, the 1.1.0 method (`PACK_1_1_0_REVERIFICATION.md`); then `treediff.py` /
     `presetdiff.py` seam reads on the flagged systems only.
5. **Notes.** Read the `notes adds` lines: each module there joins the read list for step 4 with the
   quoted line as its reason. If the block says `notes: not fetched`, read the announcement once by
   hand and apply the same rule. Notes are pointers, never evidence.
6. **In game, by verdict.** Scoped or full: the unattended `-smrautorun` A/B pair (boot census,
   `DispatchReach` and `SMRTest.RunAll()`, pack off then on; `tools/TESTKIT.md`), read with
   `python tools/logscan.py`. None: the boot census at the next sitting, as a checklist item. The
   owner launches; you write the launch line (fenced, one copy-paste line).
7. **FIX / REMOVE prompts.** One per verdict from step 4, within what `WORKFLOW.md` "After a game
   patch" says the instruments license, shaped by `prompt-authoring`. A found defect is filed (`smr-bug-library`),
   not fixed here. Put a deep-sweep decision and its cost line in the checklist.
8. **The opt-in outbox entry.** Write
   `C:\Dev\SMR-OptInPack\docs\agent\prompts\perma\gamepatch\<BuildVersion>_<date>.md` in the format
   of that folder's README, **even when nothing is flagged**. Copy the opt-in section of the block
   verbatim; never interpret an opt-in row. Commit it in the fork with a pathspec.
9. **Limits review.** In the run report, record |M|, T, B, D3 and the verdict next to what the reads
   actually found (FIX / REMOVE / KEEP counts), and say whether 12 and 1,000 sized this patch
   correctly. On the first real patch after 1.1.0, put a proposed pair of limits on the owner's
   checklist with that evidence; the owner rules.

## Drop order when budget runs out

Seam reads (step 4, full) → notes (step 5) → the suite half of step 6 → the D5 filing → the reach
sweep (`DispatchReach`). Never drop D1–D3, the boot census or the outbox entry: they are the sweep,
and the entry is the fork's only route to it.

## Scope

In: both packs' modules against the new build, the run report, prompts, filings, checklist items and
the outbox entry. Out: `Code/` edits, TestKit edits, and any file in the fork outside `gamepatch/`.

## Stops

Report instead of pushing on if `patchcheck_selftest.py` is RED, if a second build lands mid-run,
or if the fork's `gamepatch/` folder is dirty or held by a running seat there.

## Do not claim

"Nothing moved under us" or "the limits are validated". A **none** certifies the one-hop
neighbourhood of what the packs name, and nothing outside it (report §4). Until a real patch has
been through step 9, write "the small-patch regime is uncalibrated".
