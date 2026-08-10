# Chain prompt 3 — adversarial audit, integration, chain close

**Read `README.md` in this folder first — binding chain rules apply. You are
the terminal prompt: this folder must be EMPTY when you finish.** Unattended.
Start with `git log --oneline -10` + `git pull`. Todo list up front.

**Read path**: this folder's remaining files · the outbox below · every
entry/checklist line prompt 2 touched · the archived logs it cites · the
batch-1 audit precedent (`SESSION_LOG.md` 2026-08-05 close record, and the
consumed audit prompt at
`git show 530df63:docs/agent/prompts/corun-batch-1/03_FABLE_AUDIT.md`).

**Every "done", "PASS", "SKIP", "tested" and "measured" upstream is a claim.**
Attended sitting: the owner witnessed the Tier-A moments, so the target is the
record — does the written verdict match the log AND the owner's recorded
verdict words? — plus everything nobody watches even attended: commit
discipline, forced/organic honesty, condition-sampled zeros, the actuals.

## Jobs

**Job 1 — audit the record, verdict-by-verdict, against the archived logs.**
Cited lines say what the entries now say — and ⛔ **quote stacks whole**:
batch-1's one real audit finding was a truncated stack quote that hid the
frames contradicting the recorded trigger. **Diff the archived log against
the on-disk original** (byte-faithful-prefix check + read the unarchived
tail) — that check earned itself last time. Forced/organic labels present and
honest; every zero states its sampled condition; `SKIP` reasons true against
prep's confirm reads; any `tested` grant traces to a named Tier-A moment
whose claim is the ENTRY's claim — a log-only `tested` is demoted visibly.
`StartBombard` was a FIRST EXECUTION: verify the printed `pcall` result and
witnesses exist in the log. **Read the WHOLE log yourself** — organic module
firings, unexplained lines with their age (never silently discounted).
Commit discipline: probes deleted in recording commits, sweeps present,
staged/throwaway saves gone, **the leg-S FIXTURE save named in a recording
commit and actually on disk** (leg S ran; if it did not, verify none exists
or is claimed), every cited log archived (`git show` it). ⛔ A missing
archived log is an automatic finding. Corrections visible, never silent; a
correction that changes a verdict re-routes that item to the owner.

**Job 2 — the decision surfaces.** PT-47's result lands on F26's entry and
any owner call it raises goes to the checklist with evidence lines — routed,
never taken. Leg Q's result lands on F99 (rate datum on the named cell;
reachability untouched; if `:805` THREW, the residue rider's precondition
finally arose — check whether its read was taken pre-reload and route
accordingly). C42's witnessed read either discharges the within-session gap
or sharpens it further — record which, honestly.

**Job 3 — the co-run program report.** Actuals vs the brief per the override
rule: owner-directed deviation is not scored (only the owner may rule this —
if they said nothing this sitting, everything is scorable); the rig's own
misses are, each named. Ledger delta vs batch-1's 8 (and unattended-1's 8):
what recurred (a rule that failed twice is a broken rule — say which), what
is NEW. Route brief-authoring lessons into `WORKFLOW.md` "Co-runs"
surgically; economics go in `SESSION_LOG.md`.

**Job 4 — integrate.** Entries carry their verdicts (verify, don't rewrite);
checklist: strike/annotate what settled; completed sections move WHOLE to
`PLAYTEST_ARCHIVE.md` (PT-47 if complete; PT-35 stays — its leg-A re-run is
a routed unattended chain, now unblocked if the FIXTURE exists, and SAY SO);
`STATE.md`: chain CLOSED + outcomes + NEXT (cap 60, evict in-commit);
`SESSION_LOG.md`: the chain's record newest-first; `CHAIN_METHOD.md`: one
lesson ONLY if this chain taught something batch-1 did not (the
simplest-first ordering rule's first real test — did it pay? say honestly
either way).

**Job 5 — close the chain.** Delete every remaining file in this folder in
the closing commit (parked sources included — cite the pre-deletion sha in
the SESSION_LOG record). doccheck green, push. Report to the owner: what ran,
what each leg found, actuals against the estimate (scored per the override
rule), what the audit caught, what is owed or routed. ⛔ **The report ENDS
with the next-chain kickoff** (chain rule 14): read `STATE.md`'s NEXT pointer
and give the exact line — or say plainly nothing is queued and name what the
front of the queue looks like (if the FIXTURE save exists, the 2-prompt
unattended PT-35 leg-A chain is the obvious front).

## Stop conditions

- A load-bearing verdict fails its audit and the logs cannot settle it →
  correct visibly, re-route to the owner, keep closing.
- The sitting was partial: audit what ran, inventory the remainder into
  TAKEABLE riders with staged state cleaned up, and still empty the folder.

## ⛔ What you may not claim

- Not `tested` for anything the owner's eyes were not on — enforce the tier,
  never upgrade it.
- Not "the co-run program is validated" — report the delta and stop.
- Not any owner decision — F48's, F26's severity calls, F99's, all routed.
- Not that the ordering rule "worked" from a sitting that never stressed it —
  the claim needs a course change to have actually happened.

## Notes from upstream

**THE SITTING'S HANDOFF — written by prompt 2 (Opus, ATTENDED, 2026-08-10),
which is consumed in the same commit that wrote this.**

⛔ **You are auditing an attended sitting that OVERRAN by more than double.**
Estimate 33–36 attended minutes; actual ≈ 75. **All seven legs ran; nothing was
cut.** The overrun is itemised in the ledger below and is the rig's, not the
owner's — but do not take that framing on trust, it is exactly the kind of
self-serving attribution you are here to check.

## 0 · Run conditions and where the evidence is

Retail `Mars.exe` **1.0.7.396349**. Two processes:

| log (archived, `git add -f`) | what it holds |
|---|---|
| `docs/archive/cb2sitting_Mars.exe-20260810-15.30.16.log` (152,783 B, 2,881 lines) | the whole sitting: ride-along + legs P, Q, R, S, and leg T's VOID first attempt |
| `docs/archive/cb2uninstall_Mars.exe-20260810-17.20.20.log` (6,667 B) | leg T's real reading — the pack-disabled process |
| `docs/archive/cb2confirm_Mars.exe-20260810-10.20.03.log` | prep's, already archived |

Both new logs verified **byte-identical to the on-disk originals** by `cmp`
after copying. ⚠️ The sitting log was **39,382 bytes when read mid-session and
152,783 after the process exited** — the engine flushes a large tail only at
exit, so every mid-session read this project has ever taken was of a partial
file. Worth a fact.

Staged copy **`CB2SIT.savegame.sav`** (`Copy-Item` of `TEST2H TRAIN`, game
closed, MD5 `103B320A1434513BC8773553096A8958`), map `BlankBigCanyonCMix_09`,
sol 333→335, pack **81/81 active AS READ**, cold load 9,312 ms.
**`TEST2H TRAIN` re-verified after the sitting: MD5 `103B320A…8958`, mtime
2026-08-03 22:21:48 — UNCHANGED.**

## 1 · Verdict summary — 7 legs, 9 predictions HELD, 0 FALSIFIED, 1 unscorable

| leg | verdict | the one line that carries it |
|---|---|---|
| **F21 ride-along** | **PASS** | `start_wait 239310758 -> 239344642 | RESTAMPED=true` at try 206/600, organic boarding |
| **P (a) keystone** | **PASS** | `g_StoryBitActive=1` before AND after the round trip; thread handle rebuilt; outcome applied |
| **P (b) F85** | **DEFECT CONFIRMED, ROUTE REFUTED** | save landed 39 s inside the modal; reload = popup gone + techs still 50 |
| **Q — F99 cell** | **ZERO throws** (rate datum) | 2 distinct tracks, 3-way witnessed breaks, sites 2→0, no `:805` |
| **R — PT-47/F26** | **PASS** | 5 volleys, all ENDED (peaks 5/6/6/7/7), owner: "trails seemed scattered" |
| **S — PT-35 fixture** | **FIXTURE BUILT** | `PT35FIXTURE.savegame.sav`, 54,424,001 B — the one survivor |
| **T — PT-53 E** | **CLEAN** | `pack=0/0 active`, 0 `LUA ERROR`, 0 new lines after a minute of sim |

⛔ **Prediction 3 is UNSCORABLE, not held.** It reads "a REBOUND-to-F9 Quick
Save LANDS". No such rebind exists on this build (§3). Its substance was
confirmed by a different route and is recorded as that, never as prediction 3.

## 2 · ⛔ THREE THINGS PREP TOLD THE SITTING THAT WERE WRONG

Audit these first; two of them would have produced false records.

1. **"0 defence towers on this save (13 domes). Say 'unsampled'."** The save
   carries **23 `MDSLaser`** (read live: `SelectedObj.class` → `MDSLaser`,
   `#MainCity.labels.MDSLaser` → 23). The instrument walked `DefenceTowerBase`
   and got 0 five times. The owner **watched interceptions happen**. Prep
   inherited the "0 towers" figure from batch-1's confirm log instead of
   re-reading it. ⇒ PT-47's interception check is **SAMPLED AND POSITIVE**.
2. **"Rebind Quick Save → F9 in Options ▸ Key Bindings."** The key-bindings
   screen exists and contains **no save-related action at all** (owner read it
   twice, screenshot). This came from F85's source-derived `ActionBindable`
   property, which nobody had ever confirmed surfaces in the retail UI. The
   owner spent minutes hunting for a control that does not exist.
3. **Every console line in the brief is written bare.** Four entry points
   (`PKeystone`, `QBreak`, `QComplete`, `SGrant`) call `Sleep()` at top level
   and the bare console has **no thread context** (`PLAYTEST_HELP.md:299`).
   Caught at pre-flight, not in flight; the sitting typed `*r` throughout.

## 3 · Owner decisions and verdict words, VERBATIM at the moment said

- leg P (a), after the reload: **"done and the notification is still there"**
- leg P (a), the outcome, watched live as they answered: **"yes it disappears"**
- leg P (b): **"I have looked 2 times now and I do not see quick save keybind
  options in the game menu. Are you sure it populates there or is that done in
  a config file?"** → and later, with the bindings screen open: **"Yes but
  nothing save related from what I can tell"**
- leg Q: **"done flushed"**
- leg R: **"Most hit I think only one per volly got hit by the mds, maybe to"** ·
  **"trails seemed scattered"** · **"yes incoming missle notification"** ·
  **"I don't see scortch marks on the dome, only the cracks"**
- leg S: **"yes it is"** (turbine placed) · **"applied it to the hospital"**
- leg T: **"toggle is the disable for me"** · **"already done that"** · **"check"**
- on the explorer baseline the session had declined: **"Does this mean we need
  to run it again at a later date?"** — the pushback that reopened it.

⚖️ **The owner made no ruling on scoring their own deviations.** Per the
override rule that makes everything scorable — but note their three deviations
each **bought** evidence (below), and the session recorded them as gains.

## 4 · The owner's leads — all three produced evidence the brief did not plan

1. **Disabling the MDS lasers for volleys 4–5.** Turned an interception check
   the brief had written off as UNSAMPLED into a controlled A/B with a
   quantitative signature: peak in-flight **5, 6, 6 (lasers on) → 7, 7 (off)**.
   Nothing in the brief asked for this.
2. **Pushing back on the abandoned explorer baseline.** The session had priced
   the confirmation as a load + a re-answer and declined it. The owner asked
   whether that meant a re-run later. Re-pricing showed the load was already
   owed to the next leg, so the true cost was ~1 minute — and it closed
   prediction 2's outcome half. **The standing rule ("do not pre-decline a
   cheap confirmation on marginal-value grounds") was violated and recovered.**
3. **Reading the key-bindings list twice and challenging the instruction.**
   That is what refuted F85's documented route instead of leaving it assumed.

## 5 · Minutes — actuals against the estimate, per moment

| moment | est | actual | why |
|---|---|---|---|
| M1 leg P keystone | 6 | ~16 | run 1 void (no read before the save, 8-min conversational gap); re-run tight |
| M2 leg P / F85 | 5 | ~15 | ~2 min hunting a keybinding that does not exist; timer-save route improvised |
| M3 §3.6 corner | 0–3 | **0 — NOT RUN** | not reached; sol boundary never near. Still open. |
| M4 leg Q | 0 | 0 | Tier C, 2 lines |
| M5 leg R volley | 4 | ~12 | five volleys incl. the owner's A/B |
| M6 leg S placement | 5 | ~6 | on estimate |
| M7 leg T uninstall | 5 | ~10 | first attempt VOID — restart required |
| console driving | +8 | ~12 | ~28 lines typed, not the 16 budgeted |
| **TOTAL** | **33–36** | **≈75** | |

⛔ Not reported as minutes "saved" anywhere. The overrun is stated as cost.

## 6 · ⛔ THE LEDGER — 14 entries, 0 of them the game's fault

Numbered for your diff against batch-1's 8 and unattended-1's 8.

1. **S1 · The brief's console lines could not have executed as written.** Four
   `Sleep()`-carrying entry points, no `*r`. G1 checks that `CB2.*` names
   resolve; it cannot see that a line has no thread context. **NEW class.**
2. **S2 · No UI path exists to load a staged copy.** `Copy-Item` duplicates the
   display name, so every staged save shows in the load list as "TEST2H TRAIN".
   Every prior load was probe-driven, so no brief ever budgeted a line for it.
   Owner hit this in the first minute. **NEW.**
3. **S3 · The SAVE primitive's liveness witness is dead.**
   `Savegame.ListForTag("savegame")` returned a non-table on **all five** saves
   (`-1 -> -1`, `ok=true`) — it read 57→58 in unattended-1. Every save this
   sitting made was witnessed instead by on-disk size/mtime and by loading it
   back. **REGRESSION in a PROVEN primitive.**
4. **S4 · `CB2.RResidue` — three engine-name reader defects in one function.**
   `DefenceTowerBase` (it is `MDSLaser`), `MapGet("map","DecRocketSplatter")`
   (returns non-table, decals unread), and the dome-crack field guess
   (`crack_visuals`/`cracks`/`dome_cracks` — printed 0 of 13 while a dome
   carried 3 fractures). **All three are the F21 `spent_time` class**, and G1
   cannot see any of them because it only covers the harness's own namespace.
5. **S5 · A mid-sitting instrument written without a printed `pcall`.** The
   session's own `PEFFECT` console line produced **zero** output — not even its
   unconditional first line. Dropped rather than debugged live. Candidate
   cause: `ModLog` is not reachable from the console sandbox (unconfirmed —
   every line that DID reach the log went through `CB2.Say` from mod code).
   **This is the S4/S5 attended class from batch-1, recurring.**
6. **S6 · The keystone took no read immediately before its save.** Run 1's
   `1 → 0` was uninterpretable because ~8 minutes elapsed between activation
   and save with nothing sampled in between. The leg trusted the sitting to
   keep the window short. Cost: the whole leg run twice.
7. **S7 · A leg that ANSWERS a popup counted nothing before answering.** The
   reply text named its own target ("temporarily lose an RC Explorer") for
   free. Recovered only because the pre-answer save happened to exist.
8. **S8 · The brief sent the owner to a keybinding that does not exist** (§2.2).
9. **S9 · The Mod-Manager disable requires a FULL PROCESS RESTART**, and
   nothing in PT-53 E, the brief, or the rig envelope said so. Leg T's first
   attempt read `pack=81/81 active` after the disable. **Caught only by the
   `ReadConditions` gate** — without it a clean log of the pack RUNNING would
   have been banked as a clean uninstall.
10. **S10 · …and the intermediate state is a NEW one.** `Unpersist missing
    permanent: Mod/SMR_CommunityFixPack` appears **twice in the pack-loaded
    process** (sitting log 2787, 2829) and in **none** of the six loads before
    the Mod-Manager round trip. Disable-without-restart = permanent gone, code
    and all 81 registrations live. **"OFF is three different things" is now
    four** — see [[D13]]. ⇒ **Any prior uninstall reading taken without a
    restart measured this state. PT-20's 98-vs-98 needs re-checking.**
11. **S11 · Prep's save-directory cleanup DID NOT HAPPEN.** Prep's brief §8 and
    its checklist entry both state `CB1STAGE`, `CORUN0`, `CORUN1`, `U1STAGE`
    were "deleted this session". **All four were still on disk at close-out**,
    along with `CB2STAGE` (prep's own staged copy, also claimed deleted),
    `U1C0PROOF`, `U1C1HEAL`, `U1C2PT35`, `U1C6FORCED`, `U1C6HEALED`.
    ⭐ **This is the SECOND session to record deleting those exact four files.**
    Batch-1's terminal audit said the same thing on 2026-08-05. A claim that
    two independent sessions have made falsely is not carelessness twice — 
    **HYPOTHESIS TO TEST: Steam Cloud (`steam_autocloud.vdf` is in that
    directory) restores saves deleted while Steam is running.** Unverified.
    15 saves totalling ~780 MB were deleted at this close-out and did not
    return on immediate re-check; **the audit should check again.**
12. **S12 · No `ModTools\Src` on this machine.** Every source line number cited
    today was taken on trust; nothing was Src-verified during the sitting.
    Prep's own re-verifications were done elsewhere or inherited.
13. **S13 · The working tree was DIRTY at sitting start and prep said it was
    clean.** Four files uncommitted — the F101 `wontfix` decision AND prep's own
    P5 checklist routing. Prep's close-out reported clean trees and pushed
    without them. **Includes an owner-typed D07 answer** ("It should not pin
    them to the dome, seems like a risk for a bunch of weird bug cases") that is
    recorded nowhere as a decision. Carried into this sitting's commit.
14. **S14 · Three engine return types that defeat a naive `== true`**, all found
    live today: `el.broken` is a **TABLE**, `IsTechResearched` returns **1**,
    `IsTechDiscovered` returns **163**, and (from F21) `GetSpentTimeAverageInHours`
    returns a **T() object**. Bank as a reading-trap fact.

⚖️ **Recurrence vs batch-1:** S5 is batch-1's S4/S5 mid-chain instrument class,
**recurring after being written into WORKFLOW**. S4 is the F21 reader class,
recurring. S11 is P5, **recurring for the second time with the same four
filenames**. S1/S2/S3/S6/S7/S9/S10/S12/S14 are NEW.

## 7 · Routed to the owner — decisions, NOT taken here

All are on `PLAYTEST_CHECKLIST.md` "Decisions waiting on you".

1. **F85's disposition — its own fork cannot express the result.** The entry
   says "if a save lands → R2-by-rebind; if the binding or save is refused →
   I/R4, documentation". The halves split: **binding refused, save NOT
   refused**. Third cell. Severity and whether anything gets built are the
   owner's.
2. **The 4th OFF state and PT-20.** Whether PT-20's 98-vs-98 uninstall
   comparison sampled a real disable or the mixed state (S10).
3. **The save-directory gate hole, now with a mechanism hypothesis** (S11).
4. **The dirty working tree** (S13), including the unrecorded D07 answer.

## 8 · Still open / not run

- **M3, the §3.6 sol-change corner rider** — never reached, sol boundary never
  near. Unchanged, still TAKEABLE.
- **The unattributed modal popup.** At ~16:02 a modal appeared, blocked the
  console, and the owner had to click it to continue; it is in NO log. The
  notification list at the time held `Seed Vegetation`, `New Trade Offer`,
  `Faction Dislikes` — organic events firing at speed 3, the likely class.
  ⛔ **Recorded as unattributed, never dismissed.** It happened AFTER the
  post-reload read showed `g_StoryBitActive=0`, so it was not the keystone's.
- **Decal fade (F26 integrity check 1)** — UNSAMPLED. No working instrument on
  either side; owner saw no scorch on the dome and ground-decal fade was not
  separately observed.
- **The "Incoming Missile" notification CLEARING** — appearing is confirmed,
  clearing was not separately confirmed.
- **C42** — SKIP as prep ruled; untouched, and the fork on its entry stands.

## 9 · Close-out record

- `DISARM GATE: GREEN` · `PROBE SWEEP: clean` · both `Code/` trees swept.
- `metadata.lua` restored, no BOM, 2 lines removed.
- **Save directory checked (P5's whole point)** — 15 stranded saves deleted,
  ~780 MB; `PT35FIXTURE.savegame.sav` is the ONE deliberate survivor and is
  NAMED in the recording commit. `TEST2H TRAIN` MD5/mtime unchanged.
  `last_save = "TEST2H TRAIN.savegame.sav"` in `LocalStorage.lua` after five
  in-run saves — the `save_as_last` discipline confirmed empirically.
- Both logs archived with `git add -f`, byte-identical by `cmp`.

## 10 · The banked cards, verbatim as written the moment each leg completed

⚠️ These were written live, before the next leg started (rule 1). Where a later
reading changed a card, the change is IN the card with the original reasoning
left standing — run 1 of the keystone especially. Audit the cards against the
logs, not against this summary.

### BANKED CARDS — written the moment each leg completed (rule 1)

Run conditions common to every card below unless a card says otherwise: retail
`Mars.exe` **1.0.7.396349** · staged copy **`CB2SIT.savegame.sav`** (`Copy-Item`
of `TEST2H TRAIN`, game closed, MD5 `103B320A1434513BC8773553096A8958`) · map
`BlankBigCanyonCMix_09` · sol 333 · pack **81/81 active AS READ** · cold load
**9,312 ms**, arrived PAUSED, speed set 0→3 with read-back (C4 held) · log
`Mars.exe-20260810-15.30.16-6a22b86d.log`.

```
RIDE-ALONG — F21 restamp witness — PASS (the wrapper was OBSERVED firing)
Run conditions: as above · load 1 of the process · 0 engine error lines in window
FORCED: nothing. Game speed 3 was set at load; the boarding itself is the
  game's own and no call touched the subject, the station or the train.
ORGANIC: the entire measured event — a colonist's own train arriving and their
  own BoardVehicle running.
Readings:
  F21SUBJ candidate[1] colonist=Colonist#2000038450 station=StationSmall#4552
    ticket.stage=Waiting ticket.start_wait=239310758 (GameTime now=239324158,
    waited=13400 ms)
  READ F21-restamp-subject = 115 | population=115 | APPLICABLE=true
  F21WITNESS subject Colonist#2000038450 BEFORE: stage=Waiting
    start_wait=239310758
  F21WITNESS subject Colonist#2000038450 BOARDED at try 206/600 — stage Waiting
    -> Traveling | start_wait 239310758 -> 239344642 | RESTAMPED=true
    (GameTime at read=239344929)
  ⭐ THE WRAPPER FIRED — start_wait advanced by 33884 ms to the boarding moment
  F21 11 station(s) holding 114 colonist(s) waiting | 8 train(s) carrying 48
    rider(s) | when=immediately after a witnessed boarding
Witness: the counter could have been false in the way that matters — `start_wait`
  is read on ONE named subject BEFORE the transition and again AFTER
  `stage` reaches "Traveling", and the subject is only selected once already in
  `station.waiting_for_train` with a live ticket. An absent fixture produces
  UNSAMPLED (the bound-hit line), never RESTAMPED=true. 205 polls read
  stage=Waiting before the 206th read Traveling, so the transition was crossed,
  not assumed.
Owner verdict (tier C — no eyes, ran in the background under M1): none taken;
  this rider is not eyes-class and none was asked for.
Predictions: 1 HELD / 0 FALSIFIED — prediction 12 (start_wait CHANGES as stage
  becomes "Traveling") HELD.
Falsifier for this card in one sentence: the same subject reaching
  stage="Traveling" with `start_wait` unchanged at 239310758 — which the
  instrument prints as an explicit DEFECT line and did not.
⛔ Not claimed: NOT a `tested` re-earn — F21 stays `fixed`, exactly as the rider
  says. ONE boarding on ONE save is a single witnessed instance, not a rate.
  Says nothing about the Comfort charge actually billed at ExitVehicle; that is
  downstream of the stamp and was not read.
⭐ Both of the entry's banked reading traps RE-CONFIRMED live rather than
  inherited: `GetSpentTimeAverageInHours` returned `table: 000001B07CE8D640` (a
  T() object, useless in a log line) and `rawget(train,"trip_time")` returned
  nil on all four sampled trains while the class default is 0.
⚠️ Aggregate shape unchanged from prep and still only suggestive: station
  StationSmall#4552 avg=455344 against trains avg=69764–144376.
Minutes: estimate 0 / actual 0 (rode free under M1, as designed)
```

```
LEG P (a) — popup keystone, POPUP_CONSEQUENCE_AUDIT §8 item 1 — PASS (survives)
Run conditions: as above · load 3 of the process (CB2PKEY2.savegame.sav, an
  in-run save of the CB2SIT lineage) · 0 engine error lines in window
FORCED: ForceActivateStoryBit("ArcadiaCross", MainMap) — a storybit that would
  not otherwise have fired now. The save and the reload are also forced.
ORGANIC: the popup machinery itself — nothing touched g_StoryBitActive, the
  waiter, or the notification between the reads.
Readings (verbatim):
  TRY ForceActivateStoryBit [FIRST EXECUTION] ok=true result=nil
  PKEYSTONE g_StoryBitActive=1 entr(ies) | first.id=ArcadiaCross
    run_thread=thread: 000001B07ACC4F98 IsValidThread=true (read ok=true) |
    when=after activation, before any save
  PKEYSTONE g_StoryBitActive=1 entr(ies) | first.id=ArcadiaCross
    run_thread=thread: 000001B07ACC4F98 IsValidThread=true (read ok=true) |
    when=immediately before the save
  SAVE SaveGame returned err=false name=CB2PKEY2.savegame.sav
  LOAD OK #3 file=CB2PKEY2.savegame.sav — LoadGame returned no error
  PKEYSTONE g_StoryBitActive=1 entr(ies) | first.id=ArcadiaCross
    run_thread=thread: 000001B07C596698 IsValidThread=true (read ok=true) |
    when=after reload
Witness: THREE reads on the same named subject, the middle one taken
  IMMEDIATELY BEFORE the save — so the interval in which the population could
  have decayed on its own is ~30 s, not the ~8 min of run 1. The population was
  demonstrably 1 at the instant of the save, so the post-load 1 is a survival
  and not an empty denominator. Owner's eyes corroborate: the "Arcadia Cross"
  notification is visibly still in the corner list after the reload.
  ⭐ The run_thread HANDLE CHANGED across the load (…ACC4F98 → …C596698) — the
  waiter was rebuilt by the persist machinery, which is what distinguishes
  "persisted and restored" from "the read is stale".
Owner verdict (tier A): "done and the notification is still there"
Predictions: 1 HELD / 0 FALSIFIED — prediction 1 (the popup-carrying thread
  SURVIVES the save/load) HELD.
Falsifier for this card in one sentence: g_StoryBitActive reading 0, or
  IsValidThread false, after the reload while the pre-save read was 1 — which
  is precisely what run 1 appeared to show and did not survive scrutiny.
⛔ Not claimed: prediction 2 (answering after the reload still applies the
  outcome) is NOT settled by this card. ONE storybit on ONE save — nothing here
  generalises to the real-time-thread popups F85 is about, which are a
  DIFFERENT thread class; the audit's own text predicts storybits survive
  precisely because they wait in game time.

⚠️ RUN 1 OF THE SAME LEG — VOID, and recorded rather than discarded.
  Subject AnythingForLove, activated with g_StoryBitActive=1 /
  IsValidThread=true, read again after save+reload as g_StoryBitActive=0 /
  run_thread=nil. It LOOKS like a falsification of prediction 1 and must not be
  read as one: ~8 minutes of real time at speed 3 elapsed between the
  activation read and the save (the sitting's own conversation), with NO read
  in between, so "the round trip killed it" and "it expired before the save"
  are indistinguishable. The instrument's own Applicable line called it
  correctly — population=0, APPLICABLE=false, UNSAMPLED. Run 2 explains it: the
  mechanism survives, so the disappearance happened before the save.
  ⇒ Instrument gap for the next brief: PKeystone must take its own read
  IMMEDIATELY before the save, inside the same call, rather than trusting the
  sitting to keep the window short.
Minutes: estimate 6 / actual ~16 across both runs (the overrun is the rig's —
  no read before the save, and an 8-minute conversational gap the leg design
  did not defend against)
```

```
LEG P (a) ADDENDUM — prediction 2 (answering after the reload applies the
outcome) — MECHANISM HELD / SPECIFIC OUTCOME UNSAMPLED
FORCED: the activation, the save, the reload. The reply itself is the owner's
  own choice, taken at the keyboard.
Readings (verbatim):
  PKEYSTONE g_StoryBitActive=0 entr(ies) | first.id=- run_thread=nil
    IsValidThread=nil (read ok=true) | when=after answering the reply
  READ popup-keystone-thread-survival = nil | population=0 | APPLICABLE=false
The popup DID open from the surviving notification after the reload, and it was
  the right one: title "Arcadia Cross", three replies, the owner took reply 1
  ("Well, why not? Prepare the explorer! Name it Vigor!" — stated consequence
  "temporarily lose an RC Explorer").
Witness: g_StoryBitActive went 1 -> 0 ACROSS THE ANSWER, having read 1 twice
  before it. That is the waiter resuming: WaitStoryBitPopup returned, the
  storybit ran past its wait and completed. A reply that was never consumed
  leaves the bit active.
Owner verdict (tier A): "possibly I don't see a named explorer but I also
  don[']t see rc explorer one in my list, but not sure if it was there before
  the test"
⭐ THE BASELINE WAS RECOVERED RATHER THAN WRITTEN OFF, and it closes the card.
  The gap was that no RC-Explorer count existed from before the answer. But
  CB2PKEY2.savegame.sav IS that state — saved with ArcadiaCross active and
  UNANSWERED. So the owner read their rover list in the live post-answer state,
  then `*r CB2.Load("CB2PKEY2.savegame.sav")` restored the pre-answer state and
  they read the SAME list again. Same colony, same save lineage, one variable
  different. That load was needed for leg P (b) regardless, so the marginal cost
  was the owner's eyes on one list twice (~1 min).
Owner verdict (tier A), BASELINED: "yes it disappears" — the RC Explorer present
  in the pre-answer load is absent in the post-answer state.
Predictions: 1 HELD / 0 FALSIFIED — prediction 2 (answering after the reload
  still applies the outcome) HELD, mechanism AND specific consequence.
Witness for the outcome half: the reply's own stated consequence ("temporarily
  lose an RC Explorer") names its target, and that target is present in the
  pre-answer save and absent after. A reply consumed WITHOUT applying anything
  leaves the two lists identical — that is the falsifier, and it did not hold.
Falsifier for this card in one sentence: g_StoryBitActive still reading 1 with
  id=ArcadiaCross after the reply was taken, or the two rover lists matching.
⛔ Not claimed: ONE storybit, ONE reply, ONE save lineage. Says nothing about
  the real-time-thread popups F85 is about — a DIFFERENT thread class, and the
  audit's own text predicts storybits survive precisely because they wait in
  game time. The rover comparison is the owner's eyes on a UI list, not a
  scripted count.
⇒ Instrument gap STILL recorded for the next brief, because the recovery
  depended on the right save happening to exist: a leg that ANSWERS a popup must
  count the outcome's own target BEFORE the answer. The reply text names the
  target for free; nothing read it, and only the pre-answer save saved the card.
⚖️ Method note for the audit: the session first declined this confirmation as
  "not worth it" on cost grounds and the OWNER pushed back ("Does this mean we
  need to run it again at a later date?"). The re-pricing was the correct call —
  the load was already owed to the next leg, so the true marginal cost was ~1
  minute, not the load-plus-re-answer the session had priced. Standing rule
  reaffirmed: do not pre-decline a cheap confirmation on marginal-value grounds.
Minutes: folded into leg P (a) above, +~1 min for the baseline recovery.
```

```
LEG P (b) — F85, breakthrough choice popup — DEFECT CONFIRMED on its own site,
  ROUTE REFUTED. ⛔ The entry's two-way fork was WRONG and this is the finding.
Run conditions: as above · loads 4 and 5 of the process · sol 335 · 0 engine
  error lines in window
FORCED: ShowBreakthroughChoicePopup opened by call; the save fired by a timer.
  ⛔ THE SAVE WAS NOT A REBOUND QUICK SAVE — see ROUTE below.
ORGANIC: nothing.
Readings (verbatim, with the log's own timestamps — the ORDERING is the witness):
  PPOPUP available breakthrough techs = 50 (read ok=true)
  TRY ShowBreakthroughChoicePopup [FIRST EXECUTION] ok=true result=nil   [Lua 1:10:59]
  SAVE SaveGame returned err=false name=CB2F85.savegame.sav              [Lua 1:11:38-39]
  TRY SaveGame CB2F85.savegame.sav (yielding) ok=true result=false
  LOAD OK #5 file=CB2F85.savegame.sav — LoadGame returned no error
  POPUPSUBJ breakthrough choice popup: available techs = 50 (read ok=true)
  READ F85-choice-popup-route(ShowBreakthroughChoicePopup) = 50 | population=50
    | APPLICABLE=true
  on-disk: CB2F85.savegame.sav, 54,395,258 bytes, written 16:41:56
Witness: the save fired ~39 SECONDS AFTER the popup opened and the log's own
  line order proves it — popup at 1:10:59, SaveGame at 1:11:38. A save taken
  before the popup opened would sit ABOVE the PPOPUP block, not below it. And
  the count discriminates the timing a second way: had the owner answered before
  the timer fired, SetTechDiscovered would have dropped the count to 49; it read
  50 both before the popup and after the reload.
Owner verdict (tier A, on the reload): "flushed" + the screenshot showing no
  popup on screen after LOAD OK #5.
⭐ THE DEFECT: a save landing inside the open choice window comes back with the
  popup GONE and the breakthrough NOT discovered. The pending choice is
  unrecoverable — the real-time waiter (Anomaly.lua:703) did not persist, which
  is exactly what the entry says happens.
⛔⛔ ROUTE REFUTED — and the entry's fork cannot express the result.
  F85's settling observation reads: "rebind Quick Save to F9 … if a save lands,
  this is R2-by-rebind …; if the binding or save is refused, this drops to I/R4
  and stays documentation." BOTH branches are wrong here, because the two halves
  split:
   * THE BINDING IS REFUSED. The key-bindings screen EXISTS on retail (owner
     screenshot: Report Bug, Politics, Pan/Rotate/Zoom/Orbit, Pause Game, Speed
     Up …) and carries NO save-related action at all. Owner read it twice.
     Condition sampled: the owner's own read of the retail options bindings
     list; NOT a source enumeration, because ModTools\Src is not installed on
     this machine (see ledger). ⇒ "a player who rebinds Quick Save onto F9"
     is NOT a route on this build.
   * THE SAVE IS NOT REFUSED. CanSaveGame permitted a save 39 s into the open
     modal, measured. The entry's central claim about the save system is
     CORRECT.
  ⇒ Third cell: the defect is REAL and the audit's named player route is DEAD.
  This is an OWNER DECISION, not an agent call — routed to the checklist.
Predictions: prediction 4 HELD (popup gone AND breakthrough not discovered).
  ⛔ PREDICTION 3 IS NOT SCORED — it says "a REBOUND-to-F9 Quick Save LANDS".
  No rebind exists, so the prediction as written was untestable. Its SUBSTANCE
  (a save can land in the open window) is confirmed by a different route and is
  recorded as such, NOT as prediction 3 holding.
Falsifier for this card in one sentence: the count reading 49 after the reload
  (the save was post-answer), or the popup re-opening on load.
⛔ Not claimed: NOT reachability by an ordinary player — the one route the audit
  named does not exist, and no other player-side route has been sampled. NOT
  `tested`. The popup was FORCED, so nothing here says a real subsurface-anomaly
  or Breakthrough-law popup behaves identically, though it is the same function.
  The AssemblyChoicePopup half of F85 was not touched at all.
⚠️ The §3.6 corner (M3) was NOT run and is not claimed either way — but note for
  the disposition that it is the one popup where the game does NOT pause, i.e.
  the one place a vanilla autosave could reach a save under a popup with no
  rebind at all. That is now the interesting half.
Minutes: estimate 5 / actual ~15 (two of those spent on a rebind that does not
  exist — a brief instruction taken from a source-derived property that nobody
  had ever confirmed in the UI)
```

```
LEG Q — F99's untested cell (repair sites x multi-track merge) — ZERO THROWS
  ⛔ RATE DATUM FOR ONE CELL. NOT a refutation. NOT reachability.
Run conditions: as above · load 5 of the process (CB2F85 lineage) · map
  BlankBigCanyonCMix_09 · 0 engine error lines in window · NO save or load
  between the breaks, the completion and the residue read
FORCED: BOTH HALVES, and the leg says so on every line — the two breaks
  (CheatBreakElement) and the completion (CheatCompleteAllConstructions).
ORGANIC: nothing whatsoever.
Readings (verbatim):
  LEGQ 17 track(s), 926 element(s), 0 already-broken, 0 existing repair site(s)
  LEGQ breakable[1] track=TrackBase#4569 (4 elements) mid-element=TrackGridElement#4573
  LEGQ breakable[2] track=TrackBase#4619 (23 elements) mid-element=TrackGridElement#4606
  TRY CheatBreakElement ok=true result=nil                      (x2)
  LEGQ BREAK WITNESS element=TrackGridElement#4573 broken=true (type=table) |
    repair sites 0 -> 1 | repair_cgs 0 -> 1 | WITNESSED=true
  LEGQ BREAK WITNESS element=TrackGridElement#4606 broken=true (type=table) |
    repair sites 0 -> 1 | repair_cgs 0 -> 1 | WITNESSED=true
  ⭐ LEGQ CELL BUILT — 2 DISTINCT tracks each carrying a witnessed repair site
  F99RESIDUE 0 0 | when=after the breaks, before the completion
  TRY CheatCompleteAllConstructions ok=true result=nil
  LEGQ COMPLETION WITNESS 2 track(s) watched, 0 repair site(s) still outstanding
  F99RESIDUE 0 0 | when=immediately after the completion, BEFORE any save or load
  whole-log scan: `grep -c "LUA ERROR"` = 0; ZERO occurrences of
    TrackElement.lua:805 anywhere in the log except the leg's own watch-line text
Witness — TWO of them, and both were needed:
  (1) BREAK witness: each break confirmed three independent ways after a 1.5 s
      settling window (el.broken truthy AND a new repair site AND repair_cgs
      growth). This matters because BreakTracks silently skips start_el/end_el
      and station elements — an unwitnessed break would have left the cell
      unbuilt while the leg reported a zero over nothing.
      ⭐ `el.broken` came back type=TABLE, exactly as the entry warns — an
      `el.broken == true` test would have read false forever.
  (2) COMPLETION witness: repair sites 2 -> 0. A zero-throw reading over
      uncompleted sites would sample nothing; the sites demonstrably drained.
Owner verdict (tier C — no eyes, none asked for): "done flushed"
Predictions: 2 HELD / 0 FALSIFIED — prediction 5 (every named break is
  witnessed) HELD 2/2; prediction 6 (the completion produces zero
  TrackElement.lua:805 throws) HELD.
Falsifier for this card in one sentence: one or more `TrackElement.lua:805:
  attempt to index a nil value (local 'start_el')` throws in the completion
  window — which would have been the first reproduction since 2026-08-03.
⛔ Not claimed, and this is the whole point of the card: BOTH HALVES WERE
  FORCED. This is a RATE DATUM for one cell of F99's 2x2 and says NOTHING about
  whether a player can reach it. Zero throws is a RATE BOUND, not a refutation.
  F99 stays `cand`. Sample size: ONE completion over TWO broken elements on two
  tracks — the seven original throws happened on an unknown, probably larger,
  configuration.
⭐ WHAT IT DOES CLOSE: the 2x2's empty cell is no longer empty. Sample 1 had the
  repair path without a merge; sample 2 had the merge without the repair path;
  this is repair sites on TWO DISTINCT tracks completed together — the
  configuration the entry names and nobody had run. Third witnessed negative.
⚠️ Scale caveat for the audit: this cell was built with 2 broken elements on
  2 tracks. Sample 2 ran 201 sites across 20 tracks. If throw probability scales
  with site count, this sample is far weaker than sample 2 and the bound should
  be read accordingly.
Minutes: estimate 0 / actual 0 (Tier C; two console lines, ~1 min of driving)
```

```
LEG R — PT-47 / F26 bombardment volley — PASS on every reading that was
  sampled. ⛔ AND ALL THREE AGENT-SIDE READERS IN THIS LEG ARE DEFECTIVE.
Run conditions: as above · load 5 of the process · FIVE volleys · speed 3 (4 of
  them) and speed 1 (the last) · 0 engine error lines across the whole log
FORCED: five StartBombard volleys that would not otherwise happen, 8 missiles
  each, radius 4000, on domes DomeMedium#8984 (x3) and DomeBasic#1243 (x1) and
  DomeMedium#8984 again. ⭐ ALSO FORCED, by the OWNER's own initiative: the MDS
  lasers were DISABLED for volleys 4-5 (see the A/B below).
ORGANIC: the volley behaviour itself — spread, interception, dome damage,
  notification. Nothing scripted touched a missile.
Readings (verbatim):
  DOME 11 of 13 dome(s) are on MainMap — WaitBombard hard-codes MainMap
  READ PT47-usable-dome(on MainMap) = 11 | population=13 | APPLICABLE=true
  TRY StartBombard [FIRST EXECUTION] ok=true result=nil            (x5)
  LEGR VOLLEY ENDED — peak in-flight missiles = 5 / 6 / 6 / 7 / 7  (x5, each
    carrying the witness clause: the table was non-empty first)
  SelectedObj.class -> MDSLaser
  #MainCity.labels.MDSLaser -> 23        (the interception DENOMINATOR)
  grep -c "LUA ERROR" = 0 across the entire sitting log
⭐⭐ THE OWNER'S OWN CONTROL, and it is the strongest thing in this card. The
  brief had no A/B for interception. The owner disabled the MDS lasers for the
  last two volleys unprompted, and the peak in-flight count moved with it:
      MDS ENABLED  -> peak 5, 6, 6
      MDS DISABLED -> peak 7, 7
  That is a QUANTITATIVE interception signature independent of the eyes, and it
  agrees with what the eyes reported (1-2 intercepted per volley). An owner lead
  converted a check the brief had written off as UNSAMPLED into a controlled A/B.
THE FIVE INTEGRITY CHECKS (F26's own list):
  1. impacts leave scorch decals that FADE — ⛔ UNSAMPLED. The rig read -1 five
     times. Owner: "I don't see scortch marks on the dome, only the cracks."
     Ground-decal fade was not separately observed. NOT claimed either way.
  2. a missile hitting a dome CRACKS it — ✅ SAMPLED AND POSITIVE. Owner
     screenshot: notification "Dome at Risk", panel "Hoffman #1 - 3 fractures".
  3. "Incoming Missile" notification appears and clears — ✅ APPEARS (owner:
     "yes incoming missle notification"). ⚠️ The CLEARING half was not
     separately confirmed and is not claimed.
  4. missiles shot down by defences — ✅ SAMPLED AND POSITIVE (owner's eyes +
     the peak A/B above). ⛔ THIS OVERTURNS PREP'S BRIEF (§3): "0 defence towers
     on this save (13 domes) … say UNSAMPLED". See the reader defects below.
  5. the bombardment ENDS — ✅ 5 of 5, each with its liveness witness.
Witness for "ENDED": the missile table was observed NON-EMPTY before each zero
  (peak > 0 recorded), so none of the five zeros describes a volley that never
  started. Prediction 7's falsifier (ok=false, or peak 0 after 3 minutes) did
  not fire once.
Owner verdict (tier A), verbatim: "trails seemed scattered" · "yes incoming
  missle notification" · "I don't see scortch marks on the dome, only the
  cracks" · "Most hit I think only one per volly got hit by the mds, maybe to"
Predictions: 3 HELD / 0 FALSIFIED — 7 (executes, missiles spawn), 8 (the volley
  ENDS), 9 (arrives as a SCATTER, not a rank of parallel trails).
Falsifier for this card in one sentence: ok=false on the TRY line, or a peak of
  0, or the 3-minute bound hitting with missiles still in flight, or the owner
  reporting a rank of parallel trails.
⛔⛔ THREE READER DEFECTS IN ONE FUNCTION — CB2.RResidue's entire agent-side
  half is broken, and only the owner's eyes carried the leg:
  R1. `CB2.LabelAll("DefenceTowerBase")` returned 0 and the leg printed
      "population=0 | APPLICABLE=false … 0 towers means UNSAMPLED" five times.
      THE CLASS IS `MDSLaser` (read live off SelectedObj). The zero was the
      label name, not the colony. ⇒ Prep's §3 assertion "0 defence towers on
      this save" is REFUTED, and it was inherited from batch-1's confirm log
      rather than re-read. Exactly the F21 `spent_time` class: a reader that
      could not have printed anything else.
  R2. `map:MapGet("map","DecRocketSplatter")` did not return a table — decals
      = -1 on all five volleys. The decal check has no working instrument.
      ⚠️ R1's magnitude, stated plainly: the save carries **23** MDSLasers. The
      brief said "0 defence towers". The reader was not marginally wrong.
  R3. the dome-crack reader guesses three field names
      (`crack_visuals`/`cracks`/`dome_cracks`) and printed 0 of 13 five times
      while a dome was carrying THREE FRACTURES and the game was showing a
      "Dome at Risk" notification for it. Wrong field, silently.
  ⇒ All three are the SAME class and none was caught by G1 (which checks that
    CB2.* names resolve, not that ENGINE names do). A resolution gate that only
    covers the harness's own namespace cannot see any of these.
⛔ Not claimed: NOT `tested` — the volley is forced. Says nothing about a
  Mystery 7 bombardment arising organically. The dome-crack reading is the
  game's own UI, not a scripted read. Decal fade UNSAMPLED. Notification
  CLEARING unsampled. No count of MDSLasers was taken, so interception is
  positive-by-observation with no denominator.
Minutes: estimate 4 / actual ~12 (five volleys, and the owner's A/B — the
  overrun bought the interception control the brief did not have)
```

```
LEG S — PT-35 turbine FIXTURE build — FIXTURE BUILT. ⭐ THE ONE SURVIVOR.
Run conditions: as above · load 6 of the process, a FRESH reload of CB2SIT (so
  the fixture carries no bombardment state and no fractured dome) · 0 engine
  error lines in window
FORCED: UIColony:SetTechResearched("FrictionlessComposites"), then the owner's
  own UI placement and upgrade. This leg MEASURES NOTHING and claims no result
  of its own — it exists to make a later unattended chain possible.
ORGANIC: nothing.
Readings (verbatim):
  PT35 FrictionlessComposites researched=false (ok=true) discovered=nil
    (ok=true) | 0 Large, 6 plain, 12 Diffuser turbine(s) | when=before the grant
  TRY SetTechResearched(FrictionlessComposites) ok=true result=true
  PT35 FrictionlessComposites researched=1 (ok=true) discovered=163 (ok=true)
    | 0 Large, 6 plain, 12 Diffuser | when=after the grant
  PT35 … | 1 Large, 6 plain, 12 Diffuser | when=leg S, before the fixture save
  READ PT35-turbine-half-fixture(a Large Wind Turbine exists) = 1 |
    population=1 | APPLICABLE=true
  SAVE SaveGame returned err=false name=PT35FIXTURE.savegame.sav
  on-disk: PT35FIXTURE.savegame.sav, 54,424,001 bytes, written 17:14
Witness: the grant is a genuine before/after on the same read — researched went
  false -> 1 and discovered nil -> 163 in ONE call, and the turbine count went
  0 -> 1 only after the owner placed. SSave REFUSES at 0 Large turbines, so a
  save that happened is a save over a fixture that exists.
Owner verdict (tier HANDS-ONLY): "yes it is" (turbine placed and working,
  screenshot) · "applied it to the hospital" (Remote Medic upgrade, screenshot)
Predictions: 1 HELD / 0 FALSIFIED — prediction 10 (SetTechResearched moves
  researched false->true in one call on a save where discovered is nil) HELD.
⭐ AND IT RETRO-CONFIRMS PREP'S CORRECTION BY MEASUREMENT. discovered read `nil`
  immediately before the grant, which is exactly the state in which
  `CheatResearchAll()` grants a Breakthrough NOTHING (Cheats.lua:84 against
  TechFieldPreset.lua:279). Batch-1's parked leg-5 instrument would have
  researched the entire rest of the tree and produced no Frictionless
  Composites. The premise is now false BY READING, not only by source.
⚠️ TYPE TRAP, third of the day: IsTechResearched returned `1` and
  IsTechDiscovered returned `163` — NUMBERS, not booleans. Both truthy, but an
  `== true` test reads false. Same class as `el.broken` being a TABLE (leg Q)
  and GetSpentTimeAverageInHours being a T() object (F21). Bank all three.
⛔ Not claimed: this leg proves NOTHING about F35 or F03. It builds a fixture.
  The tech was granted BEFORE the turbine was placed, so this fixture does NOT
  reproduce F35's own scenario (a save that researched the tech pre-hotfix) —
  it is the do-no-harm fixture PT-35 case A needs, nothing more.
FIXTURE CONTENTS, for whoever runs PT-35 next: CB2SIT lineage (Copy-Item of
  TEST2H TRAIN, MD5 103B320A…8958), FrictionlessComposites researched=1
  discovered=163, ONE Large Wind Turbine (working, Polymer Blades offered),
  ONE applied building upgrade — Remote Medic on a Hospital — for the F03
  leaked-upgrade-modifier half.
Minutes: estimate 5 / actual ~6
```

```
LEG T — PT-53 E, the UNINSTALL half — PASS (clean), and it took TWO attempts,
  the first of which was a FALSE CONDITION the witness caught.
Run conditions: retail 1.0.7.396349 · CB2UNINSTALL.savegame.sav (saved from the
  CB2SIT lineage WITH the pack active: `CONDITIONS pack=81/81 active | speed=5 |
  loads_this_process=6`, BombardmentSpread/TrainWaitTime/CohortHousing/
  SaveSanitizer all active BY NAME) · SECOND process,
  log `Mars.exe-20260810-17.20.20-6a22b86d.log` (6,433 bytes, whole process)
FORCED: the save, the Mod-Manager disable, the load.
ORGANIC: ~1 minute of sim at speed 3 after the load.
⛔ ATTEMPT 1 — VOID, AND THIS IS THE MOST USEFUL PART OF THE LEG.
  Owner disabled the Fix Pack in the Mod Manager (screenshot: "Community Fix
  Pack — Disabled", "Test Kit — Enabled"), quit to the MAIN MENU only, and
  loaded. The gate read:
    CONDITIONS pack=81/81 active | speed=3 | loads_this_process=2 |
      note=leg T: after the Mod-Manager disable
  The pack was STILL FULLY LOADED. A clean log read here would have been a
  clean log of the pack RUNNING. ⇒ THE MOD-MANAGER TOGGLE REQUIRES A FULL
  PROCESS RESTART. Returning to the main menu is not enough.
  ⭐⭐ AND THE PT-22 REVIEW FOUND THE STATE IS WORSE THAN "STILL LOADED".
  `Unpersist missing permanent: Mod/SMR_CommunityFixPack | Fallback permanent:
  … [7]` appears TWICE in that same pack-loaded process (main log lines 2787
  and 2829, at the two CB2UNINSTALL loads) and appears in NONE of the six
  normal loads before the Mod-Manager round trip. So a disable-without-restart
  leaves a MIXED state: the mod's persisted permanent is already gone while its
  code and all 81 registrations are still resident.
  ⇒ "OFF IS THREE DIFFERENT THINGS" IS NOW FOUR: (1) module toggle off,
    (2) Mod-Manager disable WITHOUT restart — permanent gone, code live,
    (3) Mod-Manager disable WITH restart, (4) real uninstall. State (2) is new
    and is what anyone gets who toggles and reloads without restarting.
  ⛔ CONSEQUENCE TO ROUTE: any prior uninstall-style reading taken without a
    full restart was measuring state (2), not an uninstall. PT-20's 98-vs-98
    comparison should be re-checked for which state it actually sampled.
✅ ATTEMPT 2 — the real reading. Full process restart, pack still Disabled.
Readings (verbatim):
  [mod] Loaded mod items for: SMR_CommunityFixPackTestKit      ← ONLY the kit
  Unpersist missing permanent: Mod/SMR_CommunityFixPack | Fallback permanent:
    table: 00000172F0A7A608 [7]
  [mod] This savegame tries to load Mod Community Fix Pack (id
    SMR_CommunityFixPack, v1.00-001), which is present, but not loaded
  Game loaded on map BlankBigCanyonCMix_09 in 8576 ms
  CB2 LOAD OK #1 file=CB2UNINSTALL.savegame.sav
  CONDITIONS pack=0/0 active | map=BlankBigCanyonCMix_09 | speed=5 |
    loads_this_process=1 | note=leg T: after a full restart with the pack disabled
  READ speed: SetGameSpeed(3) call=true | before=5 after=3
  whole-process scan: grep -c "LUA ERROR" = 0; no `attempt to index/call`, no
    traceback, no assert. SIX lines name the pack, ALL of them accounted for:
    2 mod-def loads, 1 items-loaded (kit only), 1 save's own recorded mod list,
    1 unpersist fallback, 1 "present, but not loaded".
  after ~1 minute of sim at speed 3 + FlushLogFile(): file size UNCHANGED at
    6,433 bytes — zero new lines of any kind.
Witness: `pack=0/0` is the liveness witness for the whole leg, and it is the
  reason attempt 1 was thrown away instead of banked. `Loaded mod items for:
  SMR_CommunityFixPackTestKit` corroborates it independently from the engine's
  own side — the kit's items loaded, the pack's did not.
Owner verdict (tier HANDS-ONLY): "already done that" (restart + Mod Manager
  re-checked) · "check" (the one-minute run)
Predictions: 1 HELD / 0 FALSIFIED — prediction 11 (the Mod-Manager-disabled
  load is clean of engine error lines naming pack code) HELD.
Falsifier for this card in one sentence: any `[LUA ERROR]` naming pack code in
  the post-load window — or, as attempt 1 showed, `pack` reading anything other
  than 0/0, which makes the whole reading void rather than clean.
⛔ Not claimed: this bounds THAT SAVE on THAT PATH. It is NOT a general
  zero-persisted-state proof. One minute of sim is a shallow probe — the
  fallback permanent is only dangerous if something later tries to USE it, and
  a minute at speed 3 exercises very little. NOT a real uninstall either: the
  mod is still installed on disk, merely not loaded. The Test Kit remained
  ENABLED throughout (deliberately — it is the constant across both sides and
  it is what keeps the console alive), so this is not a no-mods baseline.
Minutes: estimate 5 / actual ~10 (the extra 5 is the wasted first attempt —
  a rig miss: the brief did not know a restart was required)
```


