# Archive recheck — 2026-09-14

Executed model (R-G): Codex, identified by this session as a GPT-5-based agent.
The exact deployment model identifier is not exposed; it is not inferred from an earlier report.

MEASURED anchor: `1281499ed28874e83bb65b62084c4b7985ec90b9`, clean checkout,
`python tools/doccheck.py` GREEN. An unrelated peer commit advanced HEAD to
`8c2f384e6b3857f963e1618169928829b898e5d0` during the read; `git diff 1281499 --`
the checklist, archive and both selection JSONs was empty, and status remained clean.
No pull was run: this audit honoured the brief's no-writing-git fence rather than
its contradictory anchor pull. No archive history before the addendum was read.

Five leading candidates below need human disposition. This is not a ruling that
any obligation remains owed today, nor that the archival was right or wrong overall.
**34 of 35 items were unprotected by number-based rule (d); all 24 group-2 items
rest on a date heuristic.** A short candidate list cannot validate that selection.

## Progress

- [x] A: all stub-pointer checks and positive controls.
- [x] B: group 2, items 1–9.
- [x] B: group 2, items 10–18.
- [x] B: group 2, items 19–24.
- [x] B: group 1, items 1–11.
- [x] C: group 2, items 1–9, bodies read through the end.
- [x] C: group 2, items 10–18, bodies read through the end.
- [x] C: group 2, items 19–24, bodies read through the end.
- [x] C: group 1, items 1–11, bodies read through the end.
- [x] Report validation: 35 unique ledger members, archive byte comparison and positive controls passed; doccheck GREEN.
- [x] Dispatch-seat consume: brief and prompt-map row removed together; both deletions land with this report in the same commit.

## A · Pointer damage, measured rather than assumed

Commands used the Python subprocess argv route, `rg -n -F -- <literal>
 docs/archive/`; controls used the explicitly named archive file. The old archive
was 365,038 B (`git show 4624ec2:docs/archive/PLAYTEST_ARCHIVE.md`), current is
530,884 B, delta 165,846 B. The old bytes remain an exact prefix of the current
file. Selection JSON lengths are 11 and 24; the addendum has 35 entry wrappers,
34 labelled ck- and one ck139. INHERITED live-move evidence JSONs record body_bytes 44,288 + 115,333 =
159,621; subtraction from the measured delta gives 6,225 B of wrappers under
that recorded tally. This pass did not redo the earlier byte-copy falsifier.

- Original heading, verbatim across explicitly named `docs/archive/`: **0 of 35**.
- Date-free full title tail in `docs/archive/PLAYTEST_ARCHIVE.md`: **34 of 35**,
  each once. **ck139's full tail also returns zero**: its header is truncated at
  “staged for the next…” ([line 5544](../../archive/PLAYTEST_ARCHIVE.md#L5544)).
  The brief's expected 35 full-tail matches is therefore false.
- Positive identification: 34 exact title-tail controls plus the sole ck139
  header resolve **35 distinct bodies**. No body-missing claim follows from a
  failed heading/full-tail search. An initial parser incorrectly assumed full
  titles survived; corrected identification uses the ck139 header for that item.
- Any literal offered by the stub returns some hit: **35 of 35**, when the shared
  ck- label counts. Across the archive file ck- appears on **59 lines**; in the
  addendum alone it names 34 headers. This is discoverability without individual
  identification. **Only 1 of 35 stubs offers a unique entry label**, ck139.
- The literal offered heading identifies **0 of 35**. The combined “ck- and this
  heading” instruction identifies no unnumbered entry by both literal parts.
  Neither “all stubs find nothing” nor “all stubs uniquely work” is supported.

Proposed replacement line (for each stub, substitute its current header line):

> Body archived in [archive/PLAYTEST_ARCHIVE.md](archive/PLAYTEST_ARCHIVE.md); search the unique archive heading `<paste the exact current ## ck… header, including any truncation>`.

Example for the first stub:

> Body archived in [archive/PLAYTEST_ARCHIVE.md](archive/PLAYTEST_ARCHIVE.md); search the unique archive heading `## ck- -- archived 2026-09-14 (was checklist status:closed): ✅ v7 IS LIVE on both stores (your word). Nothing to decide; three things to tell me when convenient.`

This proposal only changes checklist pointer text and uses existing headers;
archive edits are unnecessary. No pointer was changed. Line positions below
are a snapshot locator, not proposed stable anchors.

## B · Ranked restoration candidates

INFERRED routing assessments below come from inspected live hits, not from word
co-occurrence. Body quotations are in the complete ledger. Rank favours an
explicit checklist dependency or an unrecorded owner input; historical urgency
is not transported into today's queue.

| Rank | Item / group | Evidence literal and live hit | Why bring the body back for review |
|---:|---|---|---|
| 1 | G2-11, ck34, ONE MOD FIX ALL / 2 | `smrcf-verify`, `C49`; [SMRCF_COVERAGE_SWEEP:195](SMRCF_COVERAGE_SWEEP.md#L195); checklist:5596 | Report explicitly mirrors the decision to checklist item 34, and live item 56 says the now-or-after question is still the owner's. Body itself still calls that question open. |
| 2 | G2-24, corun-batch-2 prep / 2 | `CHAIN_QA_REPORT.md`; [CHAIN_QA_REPORT:252](CHAIN_QA_REPORT.md#L252) | Archived body expressly says wording is still owed by owner and stays until it exists. The report explains whose wording it is; it does not contain that owed-input instruction's disposition. This is a C finding, not a claim of a dangling explicit checklist citation. |
| 3 | G2-15, ck28, rescue dialog / 2 | `report_text()`, `drone stat dials`; [D13:137](../bugs/D13.md#L137), [D13_EXPOSED_SET:968](D13_EXPOSED_SET.md#L968) | Live sources still route owner choice to checklist item 28; archived body prices the two branches and contains no answer. Self-contained rescue contingency instructions are acknowledged separately, without settling the body from another record. |
| 4 | G1-04, ck75, applied hazard / 1 | `last_changes`, `F104`; [PUBLIC_SURFACE_SWEEP:251](../prompts/perma/PUBLIC_SURFACE_SWEEP.md#L251), STATE:48 | Completed hazard receipt appends an unanswered request for two issue URLs and a pending patch-note edit. Live hits explain the subject themselves; restoration rationale is the appended C input, not those co-occurrences. |
| 5 | G2-23, ck9/10, corun-pt15 / 2 | `CP15F15.savegame.sav`, `C46`; checklist:7864–7865 | Live rider directs the two decisions to Decisions waiting on you. This archived body supplies the ruling and still queues a build/verify without an execution receipt. Entries supply independent defect detail; that does not make the checklist handoff accurate. |

## C · Complete item ledger and obligation wording

MEASURED membership: **5 leading candidates + 20 review-only flags + 10 clean
under this audit's definition = 35**. Group 1: 1 candidate, 5 review-only, 5 clean.
Group 2: 4 candidates, 15 review-only, 5 clean.

“Clean” means no additional restoration candidate or bespoke unresolved owner
ask was identified in that body's current framing. It does not mean every
historical statement was true, every test ran, or absence of all paraphrased
live dependencies. Explicit optional/unavailable measurement limits are recorded.
“Review-only” retains unfinished/conditional/evidence-gap wording without
asserting that the body is needed in the checklist or that today's owner owes it.
No obligation is adjudicated against later records.

Clean list (10): G1-01, G1-05, G1-07, G1-09, G1-11, G2-04, G2-07, G2-19,
G2-21, G2-22. Every member's title and evidence follow, so this tally reconciles.

### G1-01 · v7 live receipt · clean

Source: [archive:5523](../../archive/PLAYTEST_ARCHIVE.md#L5523); original heading: ✅ 2026-09-10 — v7 IS LIVE on both stores (your word). Nothing to decide; three things to tell me when convenient.

MEASURED literals → live hit lines: `c58eea7e3b51de227adf1759e7bbc61e` → 0; `C74` → 92; `C83` → 98.

Body at archive:5536:

> > Nothing more is asked here (the Paradox version display is never chased, item 71).
> >

INFERRED assessment: Receipt; no additional bespoke ask located.

### G1-02 · ck139 silent units · review

Source: [archive:5544](../../archive/PLAYTEST_ARCHIVE.md#L5544); original heading: ✅✅ 2026-09-10 — 139 BUILT + TESTED-ATTENDED: all seven silent units (C74 hammer + MOXIE, C77's five), Metatron left out. `Fix_SilentHitMomentFX.lua`; old saves heal without a power cycle; staged for the next release. Nothing is owed from you.

MEASURED literals → live hit lines: `Fix_SilentHitMomentFX.lua` → 32; `C74_SOUND_SWEEP.md` → 4; `Metatron` → 113.

Body at archive:5628:

> > **In the same MOXIE sitting (about 1 extra minute):** one console line prints
> > which of these units your colony has and how many strike markers each one
> > sees. The agent hands it over; a zero on a unit that is visibly moving proves
> > it. Report: `agent/reports/C74_SOUND_SWEEP.md`.

INFERRED assessment: Tail still schedules a console read; also asks for an optional timing glance and a skin explanation in the patch note. Opening receipt does not explicitly account for this last console line. C74/C77 entries independently explain the sound repair.

### G1-03 · 100_DOCSWEEP receipt · review

Source: [archive:5635](../../archive/PLAYTEST_ARCHIVE.md#L5635); original heading: ✅ 2026-09-09 — `100_DOCSWEEP` IS DONE: the words now match the pack that ships. The hotfix-2 chain is closed; the only thing left is your upload sitting.

MEASURED literals → live hit lines: `777249d` → 6; `F117` → 136; `100_DOCSWEEP` → 15.

Body at archive:5651:

> >   only route to one was a passenger train is gone"*. Written against `777249d`,
> >   the repair on `main`, in the words of the re-derived recipe (the
> >   passenger-station layout), not the withdrawn "ordinary mid-game" one.
> >   ⛔ "Is gone" is a claim until the F117 control runs; the note's last bullet

INFERRED assessment: F117 control is explicitly outstanding; F95 residue remains unencountered, upload/site sitting instructions survive, and owner item 47 is expressly untouched. STATE and F117 independently carry the current boot recipe; no new owner ask created here.

### G1-04 · ck75 hazard applied · candidate

Source: [archive:5677](../../archive/PLAYTEST_ARCHIVE.md#L5677); original heading: ✅ 2026-08-24 — RULED AND APPLIED. The hazard is reworded; nothing blocks the update but your sitting.

MEASURED literals → live hit lines: `last_changes` → 51; `Initial release.` → 5; `F104` → 46.

Body at archive:5745:

>     ⚠️ **Unrelated, and it needs your hands too — the reporter's GitHub issue
>     numbers were never captured.** F104 and F105 both cite "GitHub, Keelai" with
>     no issue number, so neither entry can be found from the issue or vice versa,
>     and F105's issue is titled something like *"Error when completing

INFERRED assessment: Extra request for two issue numbers/URLs has no answer in this body. Earlier paragraph also awaits a last_changes edit. The ruling in the heading covers the hazard, not these appended requests. Historical inputs need human disposition.

### G1-05 · ck57 testing model · clean

Source: [archive:5755](../../archive/PLAYTEST_ARCHIVE.md#L5755); original heading: ⚖️⚖️ 2026-08-20 — YOU RULED THE POST-RELEASE TESTING MODEL, and corrected a cost I had been quoting wrong.

MEASURED literals → live hit lines: `major overhaul` → 4; `one-time cost` → 0; `C51` → 92.

Body at archive:5759:

> 57. ⚖️ **STANDING RULING — the release gate was a one-time cost, not a per-change
>     tax.** Your words: *"I do not plan to do a major lens sweep and b leg like we

INFERRED assessment: Standing recurring procedure; no specific unpaid sitting or unanswered bespoke question. STATE:88-90 independently restates the one-time gate and ordinary post-release checks.

### G1-06 · ck55 sibling receipts · review

Source: [archive:5793](../../archive/PLAYTEST_ARCHIVE.md#L5793); original heading: ✅ 2026-08-20 — your two rulings are carried out. Nothing owed back; this is the receipt.

MEASURED literals → live hit lines: `SMR-OptInPack` → 52; `9c912b3` → 0; `Project Spark` → 71.

Body at archive:5806:

>       now code-identical to ours. ⚠️ **Not verified in a running game there** —
>       nothing was launched, and its STATE now carries the one boot check its
>       launch session owes (that its eight modules register once each after a
>       script reload). ⚠️ One honest split you should know: the double-name fix is

INFERRED assessment: Opt-in mirror still awaits a boot/script-reload check; Save Rescue missing-items consequence remains unresolved behind a future upload gate. Body explicitly places each in the sibling repo; sibling files were not inspected.

### G1-07 · ck42 STATE eviction · clean

Source: [archive:5837](../../archive/PLAYTEST_ARCHIVE.md#L5837); original heading: ✅✅ 2026-08-18 — STATE.md WAS EVICTED ON YOUR DIRECTION, AND YOU RULED THE CAPS THE SAME DAY. Nothing here is owed from you.

MEASURED literals → live hit lines: `STATE_EVICTION.md` → 21; `200-byte` → 0; `71,077` → 1.

Body at archive:5856:

>     ✅✅ **RULED SAME DAY** — you asked whether the line budget still matters
>     (*"Is the line budget even important anymore if we are capping the token

INFERRED assessment: Standing formatting/cap policy, restated in WORKFLOW:105-113 and perma/STATE_EVICTION:14-19. No unpaid bespoke action located; historical threshold is not today's threshold.

### G1-08 · ck36 rename · review

Source: [archive:5873](../../archive/PLAYTEST_ARCHIVE.md#L5873); original heading: ⭐ 2026-08-17 — THE RENAME IS DONE, EVERYWHERE A PERSON LOOKS. ✅ Your two calls came back the same day; nothing is owed.

MEASURED literals → live hit lines: `154004` → 4; `CommunityFixPack` → 173; `Opt_DroneOverhaul` → 62.

Body at archive:5921:

>     ⚠️ **One small call I did not make for you.** The mod's internal id and its
>     log tag both still say `CommunityFixPack`. Neither is something a player
>     ever searches. **My recommendation is to leave both alone** — for the same
>     reason you gave about GitHub: risk without reward. Every archived log and

INFERRED assessment: Third recommendation about keeping internal id/log tag appears after the two answered calls; trailing Owed sentence still repeats those two calls. Record that internal inconsistency; no inference about later fulfilment. Rescue re-witness is conditional and restated in its dedicated report.

### G1-09 · ck35 solo launch · clean

Source: [archive:5944](../../archive/PLAYTEST_ARCHIVE.md#L5944); original heading: ⛔⛔ 2026-08-17 — SOLO LAUNCH: ✅ the parking work is DONE; one question left before you upload

MEASURED literals → live hit lines: `PARKED_OPTIN_REFERENCES.md` → 16; `fixpack-v1.0.1` → 1; `SILENCE IS APPLIED` → 0.

Body at archive:5977:

>     remote), and the ④ sheet says so. **Nothing on this item is owed any
>     more — ④ is decision-free: upload the fix pack, link, Pages.** Your

INFERRED assessment: Body explicitly frames the launch decision as free of further asks. Restore policy is self-contained in PARKED_OPTIN_REFERENCES:13-79; its instruction to update item 35 targets the surviving stub but does not require the old body to understand restoration.

### G1-10 · ck30 C39 scope · review

Source: [archive:5998](../../archive/PLAYTEST_ARCHIVE.md#L5998); original heading: ⭐ NEW 2026-08-15 — the C39 repair you ruled turns out to touch TWICE as many buildings as the ruling pictured. ✅ CONFIRMED THE SAME DAY.

MEASURED literals → live hit lines: `TVStudioWorkshopCCP1` → 27; `C39` → 119; `all eight families` → 2.

Body at archive:6071:

>     and prompt 03 will have to say so on the store card. ⛔ **That disclosure
>     survives the ruling** — shipping as built settles the SCOPE, not whether the
>     card mentions it.
>     ⭐ **Mitigating fact, from the sweep:** all three Automation laws share the

INFERRED assessment: Scope confirm explicitly leaves card disclosure to prompt 03. Seven SOURCE families are an evidence boundary, not seven newly owed play legs. C39 itself restates the scope/ruling; its older still-OPEN lines are an internal stale-record inconsistency.

### G1-11 · ck26b combined sitting · clean

Source: [archive:6098](../../archive/PLAYTEST_ARCHIVE.md#L6098); original heading: ⭐⭐ NEW 2026-08-13 — D13 CHAIN CLOSED; the ONE combined sitting is READY (step ② — the release line's next move is yours)

MEASURED literals → live hit lines: `D13` → 221; `COMBINED_SITTING.md` → 4; `tested-unattended` → 51.

Body at archive:6103:

>     ⭐⭐ D13 IS `tested`. NOTHING HERE IS OWED BY YOU ANY MORE.**
>     **Your cost: 34 minutes** of parked handover time measured off the harness

INFERRED assessment: Current framing says no owner action owed; historical prep is struck. Attendance vocabulary and no-retro-pass are standing rules restated in WORKFLOW:413 onward. Screen/source limits and F103 WATCH are not fresh scheduled asks.

### G2-01 · F105 first build · review

Source: [archive:6229](../../archive/PLAYTEST_ARCHIVE.md#L6229); original heading: ⭐⭐ 2026-08-24 — F105 IS FIXED ON YOUR WORD, AND BUILDING IT EXPOSED A NEW QUESTION. One receipt, one call.

MEASURED literals → live hit lines: `LandscapeCostRefresh` → 48; `ClearWasteRockConstructionSite` → 117; `F105_INVESTIGATION.md` → 1.

Body at archive:6250:

> * ⛔ Still never reproduced on the rig. The 10-minute repro (place a levelling
>   site, research a dome-cost tech, watch `ConstructionSite.lua:673` stay
>   silent) rides your next sitting if you want the attended upgrade.

INFERRED assessment: Optional attended repro and normal upload sitting remain in the body. F105 entry independently describes its field route; this audit does not reconcile the chronological receipts.

### G2-02 · ck77 F105 rig receipt · review

Source: [archive:6256](../../archive/PLAYTEST_ARCHIVE.md#L6256); original heading: ⭐⭐⭐ 2026-08-24 — F105 IS REPRODUCED ON OUR OWN RIG, AND THE FIX WAS WATCHED TO STOP IT. Nothing is owed; this is a receipt.

MEASURED literals → live hit lines: `ReportModLuaError` → 28; `Unpersist missing permanent` → 13; `F87` → 63.

Body at archive:6306:

>     ℹ️ ⚠️ One loose thread I am not dropping: leg A's log line 107,
>     `Unpersist missing permanent: Mod/SMR_CommunityFixPack`. It is what PROVED
>     the pack was off — but it also says a save carries a persisted reference to
>     our code, and `FIX_POLICY` §3a's posture is that it should not. Filed for a

INFERRED assessment: Persisted-reference investigation is explicitly filed for after upload. Receipt also explains how to measure ReportModLuaError for item 73; it does not record that popup leg here.

### G2-03 · ck71 first dual publication · review

Source: [archive:6314](../../archive/PLAYTEST_ARCHIVE.md#L6314); original heading: ⭐⭐⭐ 2026-08-20 — IT IS PUBLISHED, ON BOTH PORTALS. The ids are committed. One number came out differently on each store, and that was mechanical, not a mistake.

MEASURED literals → live hit lines: `350453` → 35; `upload_preflight` → 50; `temp_pdx` → 1.

Body at archive:6388:

>     ⇒ **Still owed on the live listings, all yours:** §0.5(d) the required game
>     version **350453** on the Paradox page if it offers the field · §0.5(f) the
>     download checksum · then the site: I put both store links in, you switch
>     Pages on, and the site link goes back onto the two store pages (§1 steps

INFERRED assessment: Owner boot/download/checksum, required-version field and Pages/link actions are explicitly owed. Conflicting Paradox version claim is expressly unresolved in the body. RELEASE_PORTAL_PREP:404 onward provides a self-contained download route; no later execution adjudicated.

### G2-04 · ck59 C50 three screens · clean

Source: [archive:6398](../../archive/PLAYTEST_ARCHIVE.md#L6398); original heading: ⚠️ 2026-08-20 — C50 IS BUILT, AND IT TOUCHES THREE SCREENS RATHER THAN THE TWO ITS BRIEF NAMED. Your sitting in link 4 changes slightly.

MEASURED literals → live hit lines: `challenge landing-spot` → 6; `C50` → 103; `SpaceY` → 233.

Body at archive:6422:

>     changes; the challenge landing-spot wrapper ships. ⭐ **Looking at it during the
>     sitting stays optional** — §2a of the test brief says that if it is not opened,

INFERRED assessment: Challenge screen is explicitly optional/unobserved, rather than an owed test. Ruling is restated by C50 and the sitting records. No extra bespoke unanswered ask located.

### G2-05 · ck58 closeout plan · review

Source: [archive:6440](../../archive/PLAYTEST_ARCHIVE.md#L6440); original heading: ⭐⭐ 2026-08-20 — THE PLAN CHANGED ON YOUR RULING: C50+C51 ship IN 1.0.0, C52 is frozen, and the chain that closes this repo is written and waiting.

MEASURED literals → live hit lines: `C52` → 49; `closeout-1.0.0` → 3; `C51` → 92.

Body at archive:6450:

>     ✅ **`C52` is `parked` — frozen, reversible, and fenced.** No session may open
>     it without a fresh word from you. ⚠️ One piece of it is *not* parked because it
>     is not a code fix: the mod browser caches preview art on **id + version**, so
>     if you ever replace the preview after publishing **without a version bump**,

INFERRED assessment: C52 hold needs fresh owner words; table also assigns an attended sitting to the owner. Hold is distinct from a completed plan. C51:171 independently states the C50/C51 shipping ruling.

### G2-06 · ck48 rescue items gate · review

Source: [archive:6494](../../archive/PLAYTEST_ARCHIVE.md#L6494); original heading: ⚠️ 2026-08-19 — the SAME defect class, in the third mod. Not today's problem; do not let it be forgotten.

MEASURED literals → live hit lines: `Save Rescue` → 67; `10_SaveRescue.lua` → 13; `item 55` → 0.

Body at archive:6509:

>     ⛔ **But it must be settled before that mod ever uploads**, and the sweep
>     chain's own rules forbid its sessions from touching sibling repos, so this
>     would otherwise be lost. ⚠️ I have **not** derived what the game actually does
>     when the file is absent — it may refuse to rebuild rather than rebuild empty,

INFERRED assessment: Missing items.lua consequence remains an unresolved pre-upload gate; owner directs filing it in the sibling, not deriving now. This body cites its receipt, but the underlying gate is still conditional.

### G2-07 · ck49 packed control · clean

Source: [archive:6529](../../archive/PLAYTEST_ARCHIVE.md#L6529); original heading: ⚠️ 2026-08-19 — the launch test's own first question could not fail. Already fixed; nothing owed unless you disagree.

MEASURED literals → live hit lines: `first check` → 4; `66 recorded sessions` → 0; `packaged copy` → 0.

Body at archive:6562:

>     loose, say so and I will put it back. Otherwise nothing is owed here.

INFERRED assessment: Change receipt; only an optional objection is invited. No bespoke unpaid action located. L7_ENVIRONMENT_MAP:332 explains the packed-load criterion itself.

### G2-08 · ck45 attended run-B change · review

Source: [archive:6566](../../archive/PLAYTEST_ARCHIVE.md#L6566); original heading: ⚠️ 2026-08-19 — run B now has an ATTENDED moment in it. Nothing to decide; something to know.

MEASURED literals → live hit lines: `update_suspect` → 72; `Mod-Manager tick` → 11; `UpdateSuspects` → 55.

Body at archive:6580:

>     ⭐ **Two console lines ride along on that same visit, and they are the last
>     outstanding verification of the two fixes that paused this upload.** The
>     console is blacklisted in unattended runs, so this visit is the only place
>     they can happen — and they now cost nothing extra:

INFERRED assessment: Owner tick and two console reads are still assigned to run B. A permanent TestKit probe is expressly postponed until post-launch. Core source explains UpdateSuspects and registration itself; historical test fulfilment is not judged.

### G2-09 · ck37 upload pause · review

Source: [archive:6603](../../archive/PLAYTEST_ARCHIVE.md#L6603); original heading: ⛔⛔ 2026-08-17 — THE UPLOAD IS PAUSED ON YOUR OWN WORD. Two defects found at the sitting and fixed; two questions for you.

MEASURED literals → live hit lines: `NoHomeless` → 45; `SWEEP_LEDGER.md` → 2; `item 37` → 0.

Body at archive:6633:

>     what 1.0.0 now is.** ⛔ **Nothing is verified yet in a running game**, and
>     the release tag is deliberately parked one commit behind until it is.
>     ⭐⭐ **Your chain is built and waiting: `agent/prompts/prelaunch-sweep/`** —

INFERRED assessment: Body contains the unverified-running-game gate and sweep/rehearsal assignments, while later saying Q1/Q2 close item 37 in full. Keep both statements visible; do not infer core boot coverage from a closed version question.

### G2-10 · ck38 sweep lens 1 · review

Source: [archive:6706](../../archive/PLAYTEST_ARCHIVE.md#L6706); original heading: ⭐ 2026-08-17 — SWEEP CHAIN, LINK 1 REPORTED. Nothing blocks launch. One small call for you, and it can wait.

MEASURED literals → live hit lines: `L1_COLLISION_MAP.md` → 0; `Naturalist Habitat` → 5; `metadata.lua` → 410.

Body at archive:6760:

>     nothing was run in a game; the two 08-17 core fixes still have not executed
>     once; save footprint, uninstall, what a player sees, failure containment,
>     packed-vs-unpacked, and any other mod are all untouched — those are lenses
>     2–8. The chain has **not** converged; it has finished one lens of eight.

INFERRED assessment: Lens-1 receipt contains explicit unexecuted core fixes and unmeasured overlap. Owner order-pin question has a resolution recorded in the same body; the scope disclaimer is a separate evidence gap.

### G2-11 · ck34 ONE MOD FIX ALL · candidate

Source: [archive:6767](../../archive/PLAYTEST_ARCHIVE.md#L6767); original heading: ⭐⭐ NEW 2026-08-16 — "ONE MOD FIX ALL": I checked the other community mod against the game's code. Four real bugs we had missed. **One call from you: build them now, or after launch?**

MEASURED literals → live hit lines: `SMRCF_COVERAGE_SWEEP.md` → 0; `C49` → 41; `smrcf-verify` → 1.

Body at archive:6860:

>     ⇒ **Still nothing owed from you except the original question: now or after
>     launch?** My answer is unchanged — after. ⛔ And one small thing is owed
>     from me either way: **`C49` should be flipped to `wontfix — unreachable`**,
>     which is what our own policy says for a defect no player can reach. Say the

INFERRED assessment: Live report routes owner decision to checklist item 34; surviving checklist item 56 also says item 34's now-or-after question is still the owner's. Archived body ends by calling it still open. This is a routing dependency, not mere C49/C50/C51 co-occurrence.

### G2-12 · ck33 Open Farm · review

Source: [archive:6923](../../archive/PLAYTEST_ARCHIVE.md#L6923); original heading: ⭐⭐ NEW 2026-08-15 (late) — WE MEASURED YOUR OPEN FARM CASE ON YOUR OWN SAVE, AND IT DID NOT REPRODUCE. One sentence from you would explain that.

MEASURED literals → live hit lines: `seed_cooldowns` → 5; `SEED_LOGISTICS_HANDOFF.md` → 1; `C47FARM` → 25.

Body at archive:6985:

>     terraformed map. Whether that's a bug or a design cost is your ruling to
>     make, whenever you want to make it — nothing ships either way, and the
>     top-up ("gleaner") idea in the opt-in mod remains the remedy that fixes
>     the waste without touching the choice.** → `agent/bugs/C48.md`.

INFERRED assessment: Optional bug-versus-design ruling remains reserved amid later nothing-owed wording. Original farm question is struck and body records the opt-in-only direction. Quote the tension; C48 independently holds mechanism and routing.

### G2-13 · ck31 F85 shelf · review

Source: [archive:7100](../../archive/PLAYTEST_ARCHIVE.md#L7100); original heading: ⛔⛔ NEW 2026-08-15 (later) — pricing your "quick playtest?" question found that the F85 dialog CANNOT BE OPENED IN THE GAME AT ALL, and two player-facing pages describe it as if you had seen it

MEASURED literals → live hit lines: `SHELVED_F85_DISTRESS_PAUSE.md` → 9; `Fix_DistressPopupPause.lua` → 10; `idQuickSave` → 21.

Body at archive:7125:

>     `75/75`. No launch has run since the removal — the next unattended leg
>     measures it. Nothing is owed by you either way.
>     *The question as it stood, kept for the record:*
>     ~~The distress-call dialog is dead-coded out of the shipped game. The fix

INFERRED assessment: Removal receipt still predicts a next-unattended-leg rebaseline. Original owner removal question is historical; shelf report and F85 independently state the re-arm route. No new F85 playtest assigned.

### G2-14 · release sheet / ck29 · review

Source: [archive:7229](../../archive/PLAYTEST_ARCHIVE.md#L7229); original heading: ⭐ NEW 2026-08-14 (later) — ④ IS CUT: your launch afternoon reads ONE sheet, and the audit found one more call that comes before any paste

MEASURED literals → live hit lines: `RELEASE_PORTAL_PREP.md` → 15; `Steam Cloud re-untick` → 0; `EF-051` → 25.

Body at archive:7310:

> nothing ships with it; ⛔ **if the contingency ever fires, re-open the dialog
> text before upload and add the save-step line in the same one-launch
> re-witness** (recorded on item 17 and in the rescue card's header).

INFERRED assessment: Save Rescue future upload expressly requires dialog save-step edit plus re-witness. Body also retains a pre-paste rule-31 instruction. Current rescue report:18-38 independently restates the conditional gate.

### G2-15 · ck28 rescue dialog · candidate

Source: [archive:7316](../../archive/PLAYTEST_ARCHIVE.md#L7316); original heading: ⭐ NEW 2026-08-14 — the release descriptions are being written: ONE question, and it is bundled with a call you already owe

MEASURED literals → live hit lines: `drone stat dials` → 9; `report_text()` → 10; `D13_EXPOSED_SET.md` → 52.

Body at archive:7320:

> 28. ⚖️ **The Save Rescue dialog buries the one line it exists to print. Fix the
>     code (costs you one launch) or ship it as built (costs nothing)?**
>     **Answer this together with item 17** — whether the rescue tool publishes at
>     all — because better dialog text is only worth anything if a player ever

INFERRED assessment: Body opens an owner choice, prices a re-witness, and has no answer recorded within it. Live D13:137 and D13_EXPOSED_SET:968-971 still route this question to the checklist. Rescue report has a self-contained contingency gate, but the original live owner-routing statements still point to this missing body.

### G2-16 · site chain / ck27 · review

Source: [archive:7366](../../archive/PLAYTEST_ARCHIVE.md#L7366); original heading: ⭐ NEW 2026-08-13 — the SITE is built (unpublished): one small question, and two things for your awareness

MEASURED literals → live hit lines: `SITE_BUILD_AUDIT.md` → 3; `Sensor Towers` → 33; `Where do I tell you` → 0.

Body at archive:7377:

> web; publishing remains yours. Open decisions stay at 3.
> *(Superseded the same day: the release-description chain added **item 28**
> above, so open decisions became **4** — its terminal audit added **item 29**
> for **5** — and the owner then ruled all five release calls in one sitting

INFERRED assessment: Publishing remains owner action despite nothing-owed introduction; store link still a hole until upload. Optional offered issue form is not a request to build it. Site audit independently states comments-first reporting rule.

### G2-17 · ck14/15 ship line and split · review

Source: [archive:7414](../../archive/PLAYTEST_ARCHIVE.md#L7414); original heading: ⭐⭐ NEW 2026-08-12 — THE SHIP LINE (three rulings, decided in the process-audit review session)

MEASURED literals → live hit lines: `C42` → 22; `F86 Tiers 1+2` → 0; `default-OFF RATIFIED` → 0.

Body at archive:7441:

>     * **D13 stays BLOCKING, at hours-scale.** You challenged the audit-review
>       estimate ("adds a week") and you were right — testing is: build the
>       artifact, probe it, uninstall on a big save, run the after-sweep — a few
>       hours unless it finds something. The heavy part is agent-side (the

INFERRED assessment: Item 14 retains a D13 blocker/spec-time reserved question and upcoming combined sitting. Item 15's explicit split receipts settle its own framing, not every item-14 obligation. Standing rig and ship-line policy is restated live.

### G2-18 · ck21 site topology · review

Source: [archive:7573](../../archive/PLAYTEST_ARCHIVE.md#L7573); original heading: ⭐ NEW 2026-08-13 — public documentation: platform decided, one question back to you

MEASURED literals → live hit lines: `LAYOUT SPECIMENS` → 1; `public-docs` → 23; `SMR-CommunityMods` → 128.

Body at archive:7607:

>     opt-in toggle needs a restart is now labelled *do not publish* rather than
>     guessed at — two of our own documents claim it both ways and neither has
>     been checked against the code. The `public-docs` chain settles it.
>     **Nothing further owed by you here.** ~~The ask as it stood:~~

INFERRED assessment: Restart claim remains deliberately unverified and fenced from publication pending public-docs chain; publication itself remains owner-controlled. Topology choice is recorded in this body; no later site action is adjudicated.

### G2-19 · ck20 history scrub ruling · clean

Source: [archive:7631](../../archive/PLAYTEST_ARCHIVE.md#L7631); original heading: ⚖️ NEW 2026-08-13 — your Steam ID is scrubbed from the live docs, but NOT from git history

MEASURED literals → live hit lines: `No history rewrite` → 0; `SteamID64` → 0; `git filter-repo` → 0.

Body at archive:7638:

>     citation in three repos stays valid. CLOSED — nothing is scheduled and
>     nothing rides prompt 5. The ask as it stood:

INFERRED assessment: Current framing explicitly chooses leave-history-alone and schedules nothing. Reopen condition is standing authority, not an outstanding request. Positive live control used even though all three chosen literals return zero.

### G2-20 · ck16 deleted autosave · review

Source: [archive:7668](../../archive/PLAYTEST_ARCHIVE.md#L7668); original heading: ⛔ NEW 2026-08-12 — I DELETED ONE OF YOUR AUTOSAVES. Telling you straight.

MEASURED literals → live hit lines: `Autosave Sol 306` → 6; `EF-056` → 39; `Autosave Sol 311(2)` → 9.

Body at archive:7696:

>     post-untick cleanup). The Steam-Cloud check at your next launch stays live.
> ---

INFERRED assessment: Steam Cloud return check explicitly stays live. Autosave-protection mechanism is independently explained by EF-056 and CO_RUNS:95 onward. No save-directory investigation performed.

### G2-21 · ck11 exotic-sign minute · clean

Source: [archive:7700](../../archive/PLAYTEST_ARCHIVE.md#L7700); original heading: ⭐ NEW 2026-08-12 — asteroid Exotic-Minerals freeze (decided in-session; one owed minute)

MEASURED literals → live hit lines: `ExoticDepositSign` → 41; `F102` → 50; `Sylmacaink BH25` → 3.

Body at archive:7704:

> 11. ✅✅ **DONE 2026-08-14 — THE OWED MINUTE IS PAID, nothing further owed by you.**
>     Moment C of the combined sitting. ⛔ Two things the item had wrong and you

INFERRED assessment: Body frames local minute as paid while cure remains explicitly unverified/disclaimered and field-only. Record the cure boundary and original Owed paragraph; do not promote coverage or infer a new owner test. F102 independently states the same cure boundary.

### G2-22 · ck12/13 trains and cheats · clean

Source: [archive:7744](../../archive/PLAYTEST_ARCHIVE.md#L7744); original heading: ⭐ NEW 2026-08-12 — raised by you mid-sitting during `corun-pt60`

MEASURED literals → live hit lines: `TRAIN_SHIP_READY_ROUTE.md` → 0; `no chain may schedule a train leg` → 0; `cheat markers` → 0.

Body at archive:7764:

>     group ships at `fixed`; the verification queue is CLOSED.** F21 stays
>     `fixed` (its restamp was already witnessed organically 08-10), F64 ships

INFERRED assessment: Body gives current queue-closed framing, delivered route, and standing cheat rule. Historical proposed train legs are not counted as a new ask. TRAIN_SHIP_READY_ROUTE introduction independently restates owner ruling.

### G2-23 · ck9/10 corun-pt15 calls · candidate

Source: [archive:7852](../../archive/PLAYTEST_ARCHIVE.md#L7852); original heading: ⭐⭐ NEW 2026-08-11 — from the `corun-pt15` SITTING (two calls, both yours)

MEASURED literals → live hit lines: `Service Automation` → 4; `C46` → 12; `CP15F15.savegame.sav` → 8.

Body at archive:7881:

>    dev comment's stated intent. Queued into the next unattended build chain;
>    verification re-runs the same paused bracket on a `CP15PT15` staged copy
>    (it holds the measured TV Studio Workshop). → `agent/bugs/C39.md`.
> 10. ~~**⚖️ `C46` — re-graded 2026-08-12 after your challenge: the phantom-power

INFERRED assessment: Live C39 rider points readers to Decisions waiting on you for the C39/C46 calls; this body contains the ruling and queued C39 build/paused verify, without its own execution receipt. Bug entries explain subject/ruling themselves, so dependency is specifically the checklist handoff, not absence of defect facts.

### G2-24 · corun-batch-2 prep · candidate

Source: [archive:7898](../../archive/PLAYTEST_ARCHIVE.md#L7898); original heading: ⭐ NEW 2026-08-10 — from `corun-batch-2` prep (nothing needs your call; two are cleanup already done)

MEASURED literals → live hit lines: `CHAIN_QA_REPORT.md` → 18; `wording is still` → 0; `F99` → 47.

Body at archive:7930:

>   `--approved`, in your own hand), ⚠️ but NOT closed: the wording is still
>   owed by you.** Five shipped fixes (F55 forever-mark, F40 android dust
>   sickness, F73(b) shelter reflex, F70 template refill, F97 dust-devil gate)
>   are correct repairs whose *bug-ness* is a design judgment; the adopted

INFERRED assessment: Explicit owner wording input survives in a cleanup-headed body; line says it stays until wording exists. Other unresolved routing/test work remains (PT-47/M5/M7, F99, no-cheat go and pending close-out rule suggestion). CHAIN_QA_REPORT:236-253 independently says wording is owner's, but the body carries the concrete owed-input instruction. Human must disposition it.

## Additional obligation and boundary quotations

These excerpts retain secondary asks, tests, contingent gates and conflicting
receipts that the primary quotation in an item row cannot represent alone.
They are body statements, not present-day owner obligations.

### G1-02

Archive:5621

> > seen working by you; it's one module, cosmetic only, and nothing goes into saves. Still worth a
> > glance when convenient, not required: whether the shuttle's touchdown/lift-off

Archive:5628

> > **In the same MOXIE sitting (about 1 extra minute):** one console line prints
> > which of these units your colony has and how many strike markers each one

Archive:5586

> > **If we fix it, the patch note has to explain the two skins**, or drill-skin
> > players will report the fix as broken. Your three screenshots are saved for

### G1-03

Archive:5645

> >   identical by script. ⚠️ Still a claim: the pass has never met a save that
> >   carried the residue (your sitting read `removed 0 … left 0`). If a

Archive:5654

> >   ⛔ "Is gone" is a claim until the F117 control runs; the note's last bullet
> >   says so in your words, as it does for everything else in it.

Archive:5656

> > * **The one sitting instruction that survives — 129:** upload → check or paste
> >   both store pages (`UPLOAD_WORKFLOW` §3) → **then** publish the site (§4), in

Archive:5667

> > **47**'s two wordings on that page are untouched and still yours); and the
> > retired-phrase sweep over the store strings, both backups and the whole site

### G1-04

Archive:5699

>     ⚠️ **One thing left before the sitting, and it is mine:** `last_changes` still
>     says `"Initial release."` That string ships inside the mod and is the patch

### G1-06

Archive:5819

>       in the words that stop it being repeated as fact — that **the consequence
>       is still not derived**: nobody has read what the game does when the file is

Archive:5808

>       launch session owes (that its eight modules register once each after a
>       script reload). ⚠️ One honest split you should know: the double-name fix is

### G1-08

Archive:5939

>     ⇒ **Owed from you: the Mod Manager search above, and the sibling-titles
>     timing call. Nothing else.**

Archive:5915

>     so if that contingency ever fires, the already-required item-28 re-witness
>     launch covers the new wording too. **This repo's README was also rewritten

### G1-10

Archive:6080

>     is MEASURED (08-11 unfixed, 08-15 fixed). The other seven are SOURCE — a
>     class-graph resolution with every row re-read by hand at its declaring file.

### G2-02

Archive:6286

>     in the stack to match. So seeing the real player popup needs **pack ON with
>     this one module disabled** — no console trickery required, and the uncaught

### G2-03

Archive:6365

>     ⏳ **Paradox needs one more thing from you, and it is small.** Subscribing on
>     the website downloads nothing — `PdxMods\` holds only an empty `temp_pdx`; the

Archive:6379

>     way. ⚠️ Until then, do not repeat "Paradox is 1.0.0" as settled, including
>     anywhere on the store pages.

### G2-05

Archive:6464

>     | 4 | ⭐ **the sitting** | **YES, ~30 min** | the only eyes either fix ever gets |
>     | 5 | Fable audit | no | breaks it, moves the tag, rules ship-or-revert |

Archive:6476

>     game to German, look at the same three things, and switch back. ⭐ That German
>     look is the only way `C51` is visible to anybody, and it is also the first time

Archive:6450

>     ✅ **`C52` is `parked` — frozen, reversible, and fenced.** No session may open
>     it without a fresh word from you. ⚠️ One piece of it is *not* parked because it

### G2-08

Archive:6577

>     ⇒ Run B now budgets **one Mod-Manager tick from you** after the swap, and
>     reads the gate line before believing any other number.

Archive:6597

>     add a Test Kit probe that checks this every run — is **post-launch work**.
>     Adding a probe moves the suite count 96 → 97, and *"a suite of 96 checks"* is

### G2-09

Archive:6633

>     what 1.0.0 now is.** ⛔ **Nothing is verified yet in a running game**, and
>     the release tag is deliberately parked one commit behind until it is.

Archive:6657

>     **Each link reports to you and stops; you kick off the next.** The Fable
>     terminal audit reads everything, re-reads today's fixes hostilely, does its

### G2-10

Archive:6730

>       start silently skipping the other. ⛔ I have **not** proven a player can
>       actually hit the overlap; that needs a running game.

### G2-12

Archive:7004

>     keeps only the records and the probe. Nothing is built, nothing is owed.
>     → `agent/bugs/C47.md` (shapes section), opt-in

### G2-13

Archive:7125

>     `75/75`. No launch has run since the removal — the next unattended leg
>     measures it. Nothing is owed by you either way.

### G2-14

Archive:7267

> the cards, the mod-page blurb, the site and the portal sheet. ⛔ **One thing
> now stands between you and the ④ paste: item 31 above** — the same-day route

Archive:7268

> now stands between you and the ④ paste: item 31 above** — the same-day route
> check found the F85 dialog dead-coded, so rule 31 (one word; it also closes

Archive:7310

> nothing ships with it; ⛔ **if the contingency ever fires, re-open the dialog
> text before upload and add the save-step line in the same one-launch

### G2-16

Archive:7377

> web; publishing remains yours. Open decisions stay at 3.
> *(Superseded the same day: the release-description chain added **item 28**

Archive:7392

>     mod repos (verified live). ⛔ The store-page link is still a hole until you
>     upload. ℹ️ Offered, not built: a short issue form that asks for platform,

### G2-17

Archive:7446

>       some residue IS the repair and must survive). ⚠️ One design question is
>       yours at spec time, deliberately reserved on the entry: what the player

Archive:7470

>     Nothing owed by you until its verification lands in the combined sitting.
>     ⭐ **CHAIN AUTHORED 2026-08-12, same session, to your sharpened order**

### G2-20

Archive:7696

>     post-untick cleanup). The Steam-Cloud check at your next launch stays live.
> 

### G2-21

Archive:7718

>     ⛔ **The CURE is still unverified and still ships disclaimered** — that has not
>     moved and only a Linux/NVIDIA player's report moves it. → `agent/bugs/F102.md`.

### G2-23

Archive:7881

>    dev comment's stated intent. Queued into the next unattended build chain;
>    verification re-runs the same paused bracket on a `CP15PT15` staged copy

Archive:7882

>    verification re-runs the same paused bracket on a `CP15PT15` staged copy
>    (it holds the measured TV Studio Workshop). → `agent/bugs/C39.md`.

### G2-24

Archive:7925

> sitting. PT-47, M5 and M7 never ran and stay routed. F99 did not fire once in
> two hours; the one condition it names is still untested and the recipe for

Archive:7926

> two hours; the one condition it names is still untested and the recipe for
> building it is on the entry.

Archive:7911

> next chain's close-out is told to check it; whether that becomes a standing
> WORKFLOW rule is worth one line from you if you care.

Archive:7983

> | → **UNATTENDED** | **PT-35** (all reads are numbers + save/reload — the "nothing changes on screen" check becomes "the read-back numbers don't change", which is the entry's own claim) · **F99 residue rider** (the rig can STAGE break + cheat + pre-reload read deliberately — it no longer waits for a sitting to happen to use the cheat) · **F99 no-cheat discriminator** (forced break, organic drone repair at speed, log watch — no eyes; still gated on your go, it feeds your severity call) · **load-heal sweep** (Do-first #2 — was ~1 h of you; save/reload cycles are the rig's proven core; re-scope first) — ⭐ **all four are now the `unattended-1` chain** (`agent/prompts/unattended-1/`, built 2026-08-04, Opus×2 + Fable audit per your rule), plus the two `[NEVER RUN]` command verifications and a C42 ride-along | kick off the chain |
> | → **CO-RUN** (was full playtest) — ⭐ **the front four + ride-alongs are now the `corun-batch-1` chain** (`agent/prompts/corun-batch-1/`, built 2026-08-04: PT-37 · PT-47 · PT-42 · PT-53 E + F21/C42/popup-trio rides + the optional PT-35 fixture build; Opus prep → your ONE sitting, est. 15–25 attended min → Fable audit. Kickoff: Opus on `01_OPUS_PREP.md`; the sitting runs when you sit) | **PT-37** (break staged via the proven `BreakTrackElement` route, reload cycles rig-driven; your eyes: route formation + the salvage-cursor check) · **PT-47** (agent forces the volley + runs the 5 integrity checks; your eyes: scatter-vs-rank, the one thing that is eyes by nature) · **PT-27/PT-28** (provisioning is the real cost; catch-lists and Health-drop patterns are console reads; PT-28 rides PT-27's storm nearly free) · **PT-42** (agent stages stock/drain at speed; your eyes: the faction panel goals at 3–4 moments) · **PT-53 E** (two hands moments — manual assign, Mod-Manager disable; the load-clean read is log) · **PT-18** (agent stages the landings on a SAVE-E copy; deaths/stranding are counters; ⚠️ SAVE-E itself is still ~30 min of your provisioning) · **PT-10** (setup rig-driven; your eyes: clumping + screenshots) · **PT-15** (reads scripted, `SetLightTrapMode` is a verified command; fixture still needs the mystery pick) · **F74+F53(a)** (harness builds the fresh colony unattended; you: the pack-disable click + the two UI acts) · **PT-60** (suite/reload/log halves rig-side; you keep only the 15–20 min ordinary-play segment) · **PT-20** (you keep the disable click + 10 min play) · riders **F21 · F34(d) · F85 · F38 · popup keystone · §3.6** (each a hands-moment or ride-along once staged) | minutes, named per brief |

## Search controls, reproducibility and limits

All 105 fixed-literal scans used the exact live path list below; archive was
excluded from B. Each command returned 0 or 1; neither missing paths nor shell
errors were accepted as a zero. Full rg output was scanned for routing words
(checklist/item/see/owed/hold/untested), with bounded diagnostic samples and
number-reference follow-ups; the report does not claim every broad-term hit
was read whole. Broad terms such as CommunityFixPack or metadata.lua are
context only; the distinctive companion literals and explicit routing clauses
carry the conclusions.

Live argv paths:

```text
docs/agent/STATE.md
docs/agent/prompts/perma/
docs/agent/WORKFLOW.md
docs/agent/FIX_POLICY.md
docs/agent/bugs/
docs/agent/facts/
docs/agent/reports/
docs/PLAYTEST_CHECKLIST.md
docs/PLAYTEST_HELP.md
docs/UPLOAD_WORKFLOW.md
docs/FIELD_REPORT_REPLIES.md
docs/README.md
Code/
```

Positive live controls with those exact paths and fixed-literal argv:

- `function SMRFixPack.UpdateSuspects()` → `Code/00_Core.lua:594`.
- `STATE_EVICTION.md` → `docs/agent/STATE.md:4`, among 21 hits.
- Number-reference instrument: pattern
  `(?i)\b(?:checklist(?: item)?|item)\s*[*\x60]*42\b`
  → STATE:4/98, WORKFLOW:106 and perma/STATE_EVICTION:14.
  Same pattern template checked recovered body numbers, including 34 and 28.
  Numeric surface-list item 12/14 co-occurrences were not treated as train/ship-line dependencies.

Archive controls are individually named by each original heading in the ledger:
its date-free title tail is the positive literal for every item except G1-02.
The G1-02 control is `ck139` → archive:5544, exactly one line.
The live controls above are necessary before accepting all recorded live zeros,
including G2-19's three zero-hit literals; those zeros alone do not justify archival.

Reproduce identification without reading old history:

```python
import json, pathlib, re, subprocess
root = pathlib.Path('.')
raw = (root / 'docs/archive/PLAYTEST_ARCHIVE.md').read_bytes()
old = subprocess.check_output([
    'git', 'show', '4624ec2:docs/archive/PLAYTEST_ARCHIVE.md'])
assert len(old) == 365038 and raw.startswith(old)
addendum = raw[len(old):].decode('utf-8')
headers = list(re.finditer(r'^## ck[^\n]*', addendum, re.M))
assert len(headers) == 35
for group in (1, 2):
    selection = json.loads((root / (
        '.claude/checklist_archive_group%d.json' % group)).read_text(
            encoding='utf-8'))
    for index, heading in enumerate(selection, 1):
        tail = re.split(
            r'\d{4}-\d{2}-\d{2}(?: \([^)]*\))? \u2014 ',
            heading, maxsplit=1)[1]
        matches = [h for h in headers if h.group().endswith(tail)
            or (group == 1 and index == 2
                and h.group().startswith('## ck139 '))]
        assert len(matches) == 1
        for literal in (heading, tail):
            run = subprocess.run(['rg', '-n', '-F', '--', literal,
                'docs/archive/PLAYTEST_ARCHIVE.md'], capture_output=True,
                text=True, encoding='utf-8')
            assert run.returncode in (0, 1)
            print(group, index, literal, len(run.stdout.splitlines()))
```

The ledger's three literals per member reproduce B by substituting each literal
in `subprocess.run(['rg','-n','-F','--',literal] + live_paths, ...)`.
Read each matched wrapper's body up to the next `^## ck` header, including its
last paragraph. There were no urgent/time-sensitive present-owner requests
identified that required the brief's immediate stop; historical launch asks are
flagged with their date/condition rather than treated as new deadlines.

Out-of-scope findings recorded without repair: ck139 header truncation; G1-08's
stale trailing owed sentence and third recommendation; G1-09's general queue/
archival-rule paragraph moved along with its body; C39's live old still-OPEN
sentences followed by a scope-confirm receipt. No status, marker, owner register,
checklist pointer, archive byte or generated index was edited.

Dispatch-seat validation at `29db8900c56dbbfaae742081e84ae014abaaf72b` confirmed
35 unique ledger members, the archive byte-identical to its initial snapshot,
and positive controls passed. The peer's C95 filing is unrelated to this audit;
the checklist, archive and both selection JSONs remain unchanged since the anchor.
No audit result was used to change an owner obligation or archival status.
Final doccheck after removing the brief/map row: GREEN; PROMPT MAP PASS
(13 perma + 6 one-off rows). Commit scope is exactly this report, the removed
brief and its prompt-map row. The agreeing duplicate ck144 and TestKit alias
warnings remain pre-existing; no generated file was rewritten.
