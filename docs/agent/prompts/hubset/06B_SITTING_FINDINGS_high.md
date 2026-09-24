# hubset 06B: answer the 07 sitting's three open questions before the owner decides (desk)

Chain rules: [README.md](README.md). Read them, then `## Notes from upstream` below, first.
Fire after 07 has closed (`2e55ab8`), before 99. Desk only; nothing here is attended.

## Authority and outcome

Owner, 2026-09-24, after reading 07's close-out: "Can you give me a follow up prompt an 06B to answer
those questions before we decide". The three questions are C111, C114 and C117 below. The owner makes
the drop, hold or re-fix call on each; this link supplies the facts that call rests on and does not
make it. The owner's earlier rulings stand: one release; **one sitting only**, so this link must not
add, script or preload a second sitting; and C42, F127 and P3 stay desk-verified.

End state:
- A report at `docs/agent/reports/HUBSET_06B_SITTING_FINDINGS_2026-09-24.md` (rename it if the date moves).
  For each question it gives the answer, tagged MEASURED / SOURCE / INFERRED. Each tag carries the
  command that produced the answer and the result that would have falsified it.
- Each answer ends with what the owner's options now cost and ship, in plain words, with no
  recommendation dressed as a finding.
- An outbox appended to 99's inbox, this row struck in the README, this file `git rm`'d, all
  committed on `main`.

## Starting state

Authored on `main` at `2e55ab8`. Run `git log --oneline -5`, `git pull`, `git status --short` and
`git -C ../SMR-BugFixPack-hubset log --oneline -3` (expect `7cf48a2`). Re-derive every cited game line
with `grep -n` on `B:\Dev\SMR\SMR-Shared\SMR-SrcArchive\1.1.1.405907\Src` before relying on it.
Keep a live todo list from before your first write: one item per commit-and-verify unit, one in progress.

## Evidence from 07 (claims to check once, not re-derive)

The archived logs are `docs/archive/logs/hubset07_segA_main_2026-09-24.log` (fix off, `main`) and
`hubset07_segB_hubset_2026-09-24.log` (fix on, `hubset`). The owner relay and the two screenshots sit
beside them. Each claim below names its `grep` against those logs; a mismatch voids the claim.

### Q1 — C111: why did the text fix not change the live text?

- **Claim:** segment B, `m_RescueReturnText=active`, `RescueReturnText: applied`. Slot 6 stage 1 picked
  Colonist(2000010346) with `command=Transport dest=GeoscapeDome(1896) home=GeoscapeDome(1896)
  tid=4333 verdict=REFUTED`. Check: `grep -n "action=slot_6 command=Transport" <segB log>`.
  The owner's screenshot shows the infopanel read "Moving to a new Dome: Brussels", so the UI path
  also missed the wrapper, not only the slot's call.
- **Where things are:** the wrapper is `Code/Fix_RescueReturnText.lua` on `hubset`. The slot's subject
  filter is `H.own_home_task` in TestKit `Code/80_AgentSlots.lua` (`66288da`). That filter already requires
  `task.colonist == c`, `dest_dome == dome`, no `source_dome`, no `migration_dest`.
- **Candidates left by 07 (leads, not prescribed):** `self.dreaming`; whether a class-level
  replacement of `Colonist.Getui_command` reaches the instance's method; and anything else the wrapper
  gates on that 07 did not log.
- **Answer:** the cause, shown on the desk by a harness that reproduces the miss and then the hit.
  Also a fix shape that FIX_POLICY accepts. If you build the fix, the build and its desk harness go on
  `hubset` per chain rule 2. It stays `fixed`-pending-play at most, and it cannot be played again in
  this chain. Say so in the report.

### Q2 — C114: why did the defect not reproduce with the fix off?

- **Claim:** on `main`, both fired subjects got `booked=false ended=safe`, so P3 and P4 were REFUTED on `main`.
  The hub leg was Colonist(2000015055), holder PassageHub(2026), home GeoscapeDome(1896), `dist=29`.
  The mid-spoke leg was Colonist(2000023141) on Passage(4035) of PassageHub(2692). Check:
  `grep -n "h7_follow booked=false build=main" <segA log>` (expect 2 lines).
- The defect's evidence is the MEASURED rides on TheGodUncle's save
  (`docs/agent/reports/HUB_FIELD_FINDINGS_2026-09-24.md`) and the entry `docs/agent/bugs/C114.md`.
- **Lead (INFERRED, unchecked by 07):** native `HasLocalAccess` grants access through the home
  community (`HasAccessViaCommunity`, near `ColonistTransport.lua:288`) before the radius fallback the
  fix repairs. Verify it or discard it.
- **Answer:**
  - Which branch of native access returned true for these subjects.
  - Whether the reporter's condition differs from this fixture's, and how.
  - Whether the fix changes behaviour in any case reachable in play, with the desk showing native
    false and fixed true on that case's real shape.
  - If the finding is that the defect cannot fire as the entry describes, say so: the entry and the fix
    then need the owner.

### Q3 — C117: is 07's instrument diagnosis right, and what do the desk and source alone support?

- **Claim:** `h7_drain` ended `timeout drain_seen=false` after 90,368 game ms in both segments. Its window
  is 3 game hours (`80_AgentSlots.lua`, `hours(3)` in the `h7_drain` trigger).
  `Demolishable:DoDemolish` lowers the 5,000 ms countdown by `1000*1000/GetTimeFactor()` per game-second
  sleep, so at factor 128000 it needs about 640,000 game ms (07's arithmetic, INFERRED). Check:
  `grep -n "action=h7_drain" <both logs>` and `grep -n "real_sleep\|demolishing_countdown - dt" Demolishable.lua`.
- **Answer:**
  - Confirm or refute the diagnosis.
  - State what the C117 fix's desk harness does and does not prove about play.
  - State whether any other 07 watch shared the same real-time blind spot, which would void more
    NOT_SAMPLED or HELD verdicts than 07 reported.
  - Describe the instrument correction in the report. Do not build it: a corrected slot serves only a
    sitting the owner has not asked for.

## Scope

In: the three questions, desk harnesses and source reading that answer them, and a C111 re-fix on
`hubset` if you find the cause.
Out: any attended step, any new or amended sitting, entry status flips, and C42, F127 and P3. File
anything else you find (`smr-bug-library`) or route it to 99's inbox; do not fix it.

## Stops (report instead of continuing)

1. The answer needs the running game. Write the exact reading that would answer it, and stop that
   question. Whether any sitting happens is the owner's decision alone.
2. A finding undermines a member already HELD on the desk (C115, C116), or the chain's on-hub test.
3. A C111 fix needs a technique outside FIX_POLICY §1's ranking, or a saved field.

## Claim limits

- "C111 is fixed" is not supported without play. The supported claim is "cause found; desk
  reproduces the miss and the fix".
- "C114 works" is not supported by 07. The supported claim is whatever Q2 establishes, with its tag.
- "C117 works in play" is unsupported by anything yet. Say "desk-verified; unobserved in play".

## Unattended result

This link runs unattended. Its report is a claim until 99 audits it on a different, owner-selected
model. Nothing here changes an entry's status. Add a dated pointer to the report in each touched
entry only after 99 has audited it; until then the pointer goes in 99's inbox.

## References

`CLAUDE.md`; `docs/agent/WORKFLOW.md`; `docs/agent/FIX_POLICY.md`; skills `doc-editing`,
`smr-bug-library`, `smr-orientation`. 07's verdict table and drift list are in 99's inbox
(`### From hubset 07`).

## Notes from upstream

### From hubset 07, 2026-09-24

- The verdict table, the owner decisions and the drift list are in `99_AUDIT_high.md`, `### From hubset 07`.
  Each entry (C111, C114, C115, C116, C117) has a dated "hubset 07 sitting" section.
- The junction is back on the main tree. The fixture `saves/game/EX4M-246R_New Horizons 2 83.savegame.sav`
  is byte-identical to its backup in `saves/reporters/` (sha256 `036e130d…`).
- The owner's unexamined A6 observation (screenshots SMRTK_0074-0076 in `SMR-ScreenCaptures`, colonists
  outside with O2 bars) is not one of the three questions. Look at it only if it bears on Q2.
