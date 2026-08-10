# Manual Playtest Checklist — Community Fix Pack

**Who this is for:** the project owner, playing the real retail game **with a
live agent session alongside**. This file is the work list and nothing else:
what to test, how to set it up, what each test needs. Expectations,
predictions, pass/fail readings and console forensics are NOT written here —
the agent supplies them in the sitting, from each test's linked entry.
Reference material (ground rules, console facts, the verified command table,
Test Kit helpers, save fixtures) stays in [PLAYTEST_HELP.md](PLAYTEST_HELP.md);
completed tests move whole to
[PLAYTEST_ARCHIVE.md](archive/PLAYTEST_ARCHIVE.md) — 44 sections as of
2026-08-01, plus the 2026-08-03 pre-redesign snapshot.

> Redesigned 2026-08-03 (`docs/agent/prompts/PT_REDESIGN_PROMPT.md`, owner
> design authority of the same date): tests grouped **by system, not by PT
> number** — a sitting clears a group — and each test reduced to
> **Bug / Requirements / Setup / Good to have** (Requirements: the at-a-glance
> save/colony line, owner amendment at the checkpoint). PT codes are unchanged;
> numbering is identity, grouping is order. The full pre-redesign text,
> recorded results included, is in the archive under the "pre-redesign
> snapshot 2026-08-03" banner.

## Decisions waiting on you

Things that need **your** call, not an agent's. One line each plus where the
reasoning lives; **an agent strikes a line the moment you decide** — just say so
in any session. Added 2026-08-03 by the docs-restructure chain (spec §7 / R10):
these used to be filed only in agent reports, which is where you never read.

### ⭐⭐ NEW 2026-08-10 — from the `corun-batch-2` SITTING (four calls, all yours)

**Cost, stated honestly: the brief promised 33–36 attended minutes and it took
about 75.** All seven legs ran and nothing was cut. The overrun is ours and it
is itemised — a keybinding the brief invented, three broken readers in one
function, a save witness that stopped witnessing, a leg that had to run twice
because it took no reading before its own save, an uninstall that needed a
restart nobody knew about, and one console line of mine that produced nothing.
**Your three deviations all bought evidence and none is scored against you.**

⭐ **What went right, so the list below reads in proportion:** the popup-audit
keystone is ANSWERED (a storybit popup survives a save/load *and* still applies
its outcome when you answer it afterwards), F21's fix was WITNESSED firing on a
real boarding, PT-47 passed every check it could sample, F99's last untested
cell is filled, and **`PT35FIXTURE.savegame.sav` now exists in your save folder**
— keep it, it unblocks a test that has been stuck since 2026-08-04.

5. **⚖️ `F85` — the defect is real, and the route we told you about doesn't
   exist. What do you want done?** A save **landed 39 seconds inside the open
   breakthrough-choice popup**, and reloading it **voided the choice** — popup
   gone, breakthrough never discovered. So the entry is right that the save
   system doesn't protect you. **But the entry's route is dead:** it said "rebind
   Quick Save to F9", and you established there is no save action in the
   key-bindings screen at all. The entry's own fork only has two outcomes
   ("R2-by-rebind" or "drop to I/R4, documentation") and **neither fits** — the
   defect is real and unreachable by the one route anyone had named.
   **Your call: severity, and whether anything gets built.** ⚠️ The half worth
   your attention now is the **distress-call popup** (audit §3.6) — it's the
   game's one popup that *doesn't* pause, so it's the only place a normal
   autosave could land inside a popup window with no rebind involved. That
   rider didn't run. → `agent/bugs/F85.md`.
6. **⚖️ Disabling a mod needs a full game restart — does `PT-20` need redoing?**
   We found a state nobody had named: disable the pack in the Mod Manager, go
   back to the main menu, load a save, and **all 81 modules are still live**
   while the mod's saved data has *already* been discarded. It takes a full
   restart to actually unload. Done properly it's completely clean (0 errors,
   nothing in the log after a minute of play). **The question is backwards-looking:
   any earlier uninstall test done without a restart was measuring that middle
   state, not an uninstall — and `PT-20`'s 98-vs-98 comparison is the one to
   re-check.** Cheap to redo if you want it. → `agent/bugs/D13.md`.
7. **⚖️ Our save-folder cleanup has now failed twice, and we may know why.**
   `CB1STAGE`, `CORUN0`, `CORUN1`, `U1STAGE` — the exact four that batch-1's
   audit said it deleted on 2026-08-05, and that this morning's prep *also* said
   it deleted — **were still in your save folder tonight**, along with five more
   from earlier chains. All 15 are gone now (~780 MB) and `PT35FIXTURE` is the
   only agent save left. ⭐ **Hypothesis worth one line from you: Steam Cloud.**
   There's a `steam_autocloud.vdf` in that folder, and a deletion made while
   Steam is running would get restored from the cloud — which would explain two
   honest sessions both recording a deletion that didn't stick. **Unverified.**
   If you'd rather we stop deleting your saves entirely and just list them for
   you, say so — that's a reasonable answer too.
8. **⚖️ There is uncommitted work in the repo that isn't ours, including an
   answer of yours nobody recorded.** The `F101` decision and this morning's prep
   routing were both left uncommitted (prep reported clean trees and pushed
   without them); they're in tonight's commit now. **One of those lines is yours**
   — on checklist item 2 you typed *"It should not pin them to the dome, seems
   like a risk for a bunch of weird bug cases"*. That reads like a **decision on
   `D07`**, and it isn't recorded as one anywhere. **Confirm and we'll strike the
   item; correct us and we'll fix it.** → `agent/bugs/D07.md`.

### ⭐ NEW 2026-08-05 — from the `corun-batch-1` sitting (four calls, all yours)

**Cost: the brief promised ~24 attended minutes and the sitting ran about two
hours — but you ruled that this one is not scored against the estimate**, since
the excess was your own deliberate deviation to chase F99 and the dev-cheat
leads (which is where `F101` came from). Recorded as an **owner override** in
the audit. The one piece it does *not* cover is still logged as a real miss:
**M1 was budgeted 3 minutes and took ~25**, because prep's measured fixture had
evaporated and it had to be built live.
→ `agent/prompts/corun-batch-1/03_FABLE_AUDIT.md` §8.

1. **⚖️ Does PT-37's result unblock F48?** Case A passed and did **better than a
   no-op** — it removed one stale connection (559 → 558, exactly the clean-chain
   value) and that survived save+reload. Case B could not be sampled *at all*:
   we measured that the hex grid hands the walk the hidden original element, so
   `OrderTrackElements` **succeeds** on a meteor-damaged track and the assert
   path is unreachable that way. Your unblock criterion said *"case B failing
   cleanly"*; what we got is *"case B does not fail"* — a different answer, and
   arguably stronger. **Ship the sanitizer repair, or hold for a route that does
   reach the assert?** → `agent/bugs/F48.md`, 2026-08-05 block.
2. **⚖️ Should pinning a colonist to a residence also pin them to their dome?**
   D07's in-dome pass respects `CheckForcedResidence`; the cross-dome pass
   checks `CheckForcedDome` instead, so a Senior you pin to a residence can
   still be emigrated out of the dome when no local cohort slot exists. The
   module's header calls this deliberate. Derived from source, no fixture
   needed. → `agent/bugs/D07.md`.
   -It should not pin them to the dome, seems like a risk for a bunch of weird bug cases
3. ~~**⚖️ How much do the two new dev-tool defects matter?**~~ ✅ **DECIDED
   2026-08-10 — OUT OF SCOPE, `F101` is `wontfix`. Nothing gets built.** Your
   ruling, in your own words: *"If it works fine from what we can tell in dev
   mode then its not in this mods scope. If a modder wants to build out a
   toolkit for users then that should be something they fix."* ⭐ **What the
   session found before you ruled, because it is the reason the question was
   answerable at all:** neither throw is *possible* on a build where those
   buttons belong — `TestMeteor` is missing precisely because `Platform.cheats`
   is false, and `GetSpotNameColor` precisely because the `DevToolsPublic`
   library is absent — so there is nothing to reproduce in dev mode. On retail
   the button only executed because the engine's own gate passed first
   (`ObjCheat CheatMeteorHit` prints one line ABOVE each throw), and that gate
   is `Platform.cheats or AreModdingToolsActive()` — so a **Ged mod-tool window
   was open**, the same state that blocks achievements. ⛔ **And it was not our
   TestKit forcing it:** the kit enables only the console, which is not part of
   that gate, and neither repo writes the cheat flags at all. Pressing them
   damages nothing (the meteor button throws before it runs anything, under
   `procall`; the spot toggle only leaves its own dev-UI state one click out of
   phase). → `agent/bugs/F101.md`, "The reachability gate".
   **The dev-tools-for-players idea is parked** in
   [FUTURE_IDEAS.md](FUTURE_IDEAS.md) as a SEPARATE post-launch mod — not this
   pack, and not work.
4. **⚖️ `Opt_NoHomeless` self-deactivates at the main menu** because its
   preflight names `Community` while `HasFreeWorkplacesAround` is declared on
   the `Workforce` mixin — the F64 mistake again. It recovers (81/81 active by
   load) and the runtime is separately guarded, so nothing broke. **Fix the
   preflight target, or leave it?** → `agent/bugs/D12.md`.

### ⭐ NEW 2026-08-10 — from `corun-batch-2` prep (nothing needs your call; two are cleanup already done)

**FYI, and it is a gap in our own gate.** Four agent-created staged saves —
`CB1STAGE`, `CORUN0`, `CORUN1`, `U1STAGE`, about **223 MB**, all byte-identical
copies of `TEST2H TRAIN` — were still sitting in your save folder and in your
in-game load list, while `corun-batch-1`'s terminal audit had recorded *"all
staged/throwaway saves gone from the save dir"*. **Deleted this session**, with
`TEST2H TRAIN` re-verified byte-identical (MD5 `103B320A…8958`, mtime unchanged).
⛔ **The cause is structural, not a slip:** the co-run close-out gate runs
`git status` in both repos and **never looks at the save directory at all**, so
a staged copy that outlives its commit is invisible to every check we have. The
next chain's close-out is told to check it; whether that becomes a standing
WORKFLOW rule is worth one line from you if you care.

**Also, two entries had results that never reached them** — C42's and F21's
2026-08-05 readings were on their checklist riders only. Both entries corrected;
the archive cross-check rule you got from batch-1 caught both on its first use.
**And F21's "penalty half unmeasured" turned out to be our reader**: `spent_time`
is not a field on any class in the game, so that `nil` was guaranteed. The real
statistic reads fine — station rolling average **516,309** against its trains'
**47,968–183,186**, which is the shape F21 predicts.

**Not decisions, just so you know where things stand:** D07 is **4-of-5**, not
3-of-5 — trigger A passed on 2026-07-30 with your Forever Young A/B and the
entry had been stale for five days; you caught that from memory during the
sitting. PT-47, M5 and M7 never ran and stay routed. F99 did not fire once in
two hours; the one condition it names is still untested and the recipe for
building it is on the entry.

- ~~**CO-RUN #1 IS PREPPED AND WAITING ON YOUR ~7 MINUTES**~~ ✅ **RAN
  2026-08-04. It cost you about 6 minutes against the 15–20 asked for**, across
  two launches (398 s and 85 s, zero `[LUA ERROR]` in either). Three of the four
  payload items settled, one narrowed. **Your `TEST2H TRAIN` is untouched**
  (same bytes, same timestamp); the copy and both probes are deleted.
  → `agent/reports/CORUN1_EVIDENCE_CARDS.md` for the four cards.
  - ⭐ **F11's cross-map question is ANSWERED** — the one the entry said could
    not be proven from Lua. It is **route (a)**; the removal was watched
    happening, not inferred afterwards. → `agent/bugs/F11.md`.
  - ⭐ **F99's last unknown is MEASURED** — the hex returns the hidden element,
    which is what the seven crashes implied. Still `cand`, nothing built.
  - ⭐ **C41 got its first real mechanism, and you were right to make me close
    it.** Your mouse genuinely reports coordinates outside the game's own window
    box (up to `x=7665` against a box ending at `3840`) — because `GetMousePos`
    spans both monitors while the game's box is just the G7. Feeding that to the
    picker fires the clamps. I first recorded the bottom-right-corner case as
    **refuted**, on a reason that was simply wrong; it was **unsampled**. Your
    third run sampled it and the box came back at
    **`(2224,1731)-(3840,2160)` — the exact four numbers predicted before the
    picker opened.** ⛔ **The picker still appeared 52 times out of 52**, so the
    "icon does not appear" symptom did *not* reproduce: this is a mechanism,
    not a confirmation, and `C41` stays `cand`.
- ~~**DECISION: may the load-heal sweep use a COPY of your CAMPAIGN save?**~~
  ✅ **WITHDRAWN the same day, 2026-08-04 — nothing needed from you.** I asked
  whether `TEST2H TRAIN` carries the conditions the pack's load-time heal passes
  repair; you said you did not know. That was the right answer, and the fix was
  to stop needing to know. **The record already knew:** three archived co-run #1
  loads of a copy of that save (81/81 active) fired **zero** heal lines between
  them — so the sweep would have measured a save with nothing to heal. **And two
  of the six heal families turn out to be forceable on any save at all** (the
  meteor latch and the C34 rains structure are both shipped persistent
  variables), so the sweep now creates the defect state deliberately and watches
  the heal fire once and only once. It samples something real whatever the save
  contains, on `TEST2H TRAIN`, with no copy of your campaign involved.
  → `agent/prompts/unattended-1/02_OPUS_RUN.md` §2.
- ~~⭐⭐ **DECISION FOR YOU: adopt the co-run sign-off tiers?**~~ ✅ **ADOPTED
  2026-08-04 — you wrote `----Approved` on this item in your own hand;
  integrated by the unattended-1 terminal audit the same day.** The tiers are
  now **standing policy** in `agent/WORKFLOW.md` (sign-off tiers block): Tier A
  witness / Tier B evidence card (incl. the HANDS-ONLY sub-class) / Tier C
  delegated, with the visible-demotion rule. ⛔ In the item's own words,
  adoption does **not** touch: *"`tested` still means a pass at the keyboard
  per WORKFLOW, and no already-granted status is reclassified."* The adopted
  proposal, kept for the record of what was decided:
  (routed 2026-08-04 by the corun-rig chain's terminal prompt.) The problem it
  solves is the one you named: for log-only defects you never see the bug or
  the fix, so per-item sign-off is ceremony. The proposal, finalized against
  co-run #1's four REAL evidence cards rather than the draft's guesses:
  - **Tier A — WITNESS.** Your eyes genuinely add information the log cannot
    carry; you attend the measure moment. Unchanged from today.
  - **Tier B — EVIDENCE CARD.** Log-demonstrable; you quick-read a one-screen
    card — scenario, what was forced vs organic, the raw before/after log
    lines, run conditions, and the one-sentence falsifier — and OK it. Under a
    minute each. ⭐ **New sub-class the run exposed: HANDS-ONLY** — a leg that
    needs your *hands* (park the cursor on the other monitor, click launch)
    but none of your *eyes*. You do the named act, then read the card like any
    Tier B. The draft rule ("would eyes add information?") could not classify
    this at all, and it was the cheapest ask in the whole payload.
  - **Tier C — DELEGATED.** Mechanically self-verifying (the probe-suite
    class): ships on the suite verdict; you get a one-line digest per batch
    and keep the veto; you are not asked per item.
  **What the real cards showed:** Card 1 (the F11 train watch, classed A) —
  your eyes added nothing; the 340-removal counter over 7 trains was strictly
  stronger than watching one, so that rider class should be **A → B**, and the
  general rule is: when a designed-A item's card turns out stronger than the
  eyes, the demotion is stated on the card and applies to the NEXT instance —
  never silently. Cards 2 and 4 (the two ride-along reads) needed no eyes and
  the cards alone settle them — the clean Tier B/C cases.
  **What changes if you adopt:** log-only items stop needing per-item attended
  sign-off; you read cards (B) or batch digests (C) instead; Tier A is
  untouched. **What does NOT change without your word:** `tested` still means
  a pass at the keyboard per WORKFLOW, and no already-granted status is
  reclassified. **Recommendation: adopt, with the hands axis and the
  visible-demotion rule.** → `agent/reports/CORUN1_EVIDENCE_CARDS.md` (the
  four cards — transient sign-off artifacts per your anti-sprawl rule; their
  durable content already lives in the entries and archived logs).
  *(Your `----Approved` marker stood here; consumed into the ✅ heading above
  once the policy landed in WORKFLOW.)*

- ⭐ **DECISION FOR YOU: does the F11 pre-wrapper rider close on two of its
  three readings?** (2026-08-04) You wrote the rider, so this is yours. Two
  readings passed cleanly — `TrainPlatformWedge [active]`, and 7 trains
  completing full unload cycles with 340 passenger removals and **zero** wedges,
  with you watching one. **The third cannot be taken on that save**:
  `LuxuriousTrains` is researched so the travel-time comfort call is skipped by
  design, and no train runs a forest track, so both stat counters read `0` —
  and `0` is what a working fix and a broken one both produce there.
  **My recommendation, not a decision:** the two expressions in question are
  *vanilla's own lines*, so checking they still fire checks vanilla rather than
  our wrapper — and the wrapper's own behaviour is now witnessed. Closing on two
  of three looks right to me. **If you'd rather have the third**, it needs a
  save without `LuxuriousTrains` or a train on a forest track, and it is one
  ride-along in any future co-run. → `agent/bugs/F11.md`.
- **The mod-page relabel package** — ✅ **proposal ADOPTED 2026-08-04 (your
  `--approved`, in your own hand), ⚠️ but NOT closed: the wording is still
  owed by you.** Five shipped fixes (F55 forever-mark, F40 android dust
  sickness, F73(b) shelter reflex, F70 template refill, F97 dust-devil gate)
  are correct repairs whose *bug-ness* is a design judgment; the adopted
  proposal is a short "judgment calls" section in `MOD_DESCRIPTION.md` so they
  aren't presented identically to, say, F23 or F12. **The wording is yours** —
  the item said so, and approval adopts the proposal, not the words.
  `MOD_DESCRIPTION.md` is **FROZEN until launch prep**, so this is now a
  **launch-prep instruction with an owed input**: when the freeze lifts, the
  section goes in with your wording. This line stays until that wording
  exists. → `docs/agent/reports/CHAIN_QA_REPORT.md` §3.
- **The dead `SMRFixPack_Disabled` veto on D03/D07.** The console veto lever
  does nothing for those two modules — only `IsActive` is consulted. Either
  honor it per-call in both, or record that the lever exists only for
  D12/F97-class modules. Nothing measures wrong today, but a future leg that
  used the lever on D03/D07 would silently run live and you'd read the result
  as a fix failure. → `CHAIN_QA_REPORT.md` §5.
- **F46 `Fix_TrainCargoDumping`: move group C → group B.** The record says "no
  route" and a route demonstrably exists (F90's approved shape); the honest
  ground for skipping is cost-benefit, not impossibility. Moving it does *not*
  commit you to ever doing the conversion. → `CHAIN_QA_REPORT.md` §7.
- **F100 — how do we repair the `NoHomeless` self-check?** It names `Community`
  for a method `Workforce` declares, so the module reports itself `inactive` in
  every boot log and then applies anyway. Three options on the entry: point the
  `Require` at `Workforce` (checks a different surface than the module calls);
  teach `00_Core`'s `Require` to accept an inherited method (correct, but
  changes self-check semantics for **all 81 modules** and needs a suite run
  either side); or fix only the misleading reason string. ⚠️ It sits on D12,
  which is under review. → `docs/agent/bugs/F100.md`.
  ⏸️ **ON HOLD (your `---on hold`, in your own hand, 2026-08-04).** Not a
  decision — the item stays OPEN and stays counted; nobody builds any of the
  three options until you lift the hold and pick one.
- **Does F11 keep `P1`?** The F11 rider ran 2026-08-03 and the state its fix
  guards against has **no demonstrated producer** — crew-gathering abduction
  keeps `train.units` synced on both maps. The fix is still a correct repair of
  a real `table.remove` misuse in shipped code, so it is not a removal
  question; it is a priority question, and it is not an agent's call.
  → `docs/agent/bugs/F11.md`.
  *(Update 2026-08-03, chain close: the fix's SHAPE changed — the ~30-line full
  copy became a 10-line pre-wrapper, so it no longer freezes the two balance
  expressions a game patch would most plausibly touch. The P1 question is
  unchanged; the conversion is behaviour-preserving by construction but NOT yet
  verified at the keyboard — see the rider below.)*
- **F99 severity, and whether it becomes work at all.** New 2026-08-03 from
  your own log: 14 `TrackElement.lua:805` errors, every one under
  `CheatCompleteAllConstructions()` during your underground build-out.
  Reachable **without** the cheat is unproven and deliberately not claimed. The
  cheap discriminator is one no-cheat track completion on a disturbed element
  list — say the word and it becomes a rider; otherwise it stays `cand`.
  → `docs/agent/bugs/F99.md`.
  *(2026-08-04: the discriminator is **leg C of the `unattended-1` chain** —
  kicking that chain off is the word. Its RESULT lands back on this line as
  input; the severity decision stays yours either way.)*
  ⭐ **THE DISCRIMINATOR RAN, 2026-08-04. Result: ZERO occurrences in 4 organic
  completions — and that is a rate bound, not an all-clear.** Four track
  elements broken with `BreakTracks` (the meteor's own funnel, lottery removed),
  each break **witnessed** as real damage (`broken=true sites=1 repair_cgs=1`),
  each repair finished **by drones with no cheat on the stack**, `0 [LUA ERROR]`
  in the whole log. Fixture: 244 drones (81 idle), 15 hubs, two tracks (4 and 23
  elements). Log: `docs/archive/u1c4_Mars.exe-20260804-17.12.54.log`.
  **What it means for your call:** no-cheat reachability is still **UNPROVEN**,
  so F99 stays `cand` and nothing gets built — but the failure is now bounded:
  it did not appear in four clean organic repairs, against seven appearances in
  ~1 h of your own cheat-driven build-out. **The decision in front of you is
  unchanged in shape** — severity, and whether this becomes work at all — with
  one more piece of evidence under it. ⚠️ Four is a small N and the leg can be
  re-run cheaply on a bigger one if you want a tighter bound; say so and it is
  ~1 min of machine time per four more.
- ⚠️ **CORRECTION to the line above, and it cuts both ways.** The second-opinion
  chain re-read the log: **the count is 7, not 14** — the 14 matching lines are
  7 `[LUA ERROR]` headers each paired with a C-side `Error calling Lua function
  "exec" from C` report of the same throw. The old figure is left standing above
  rather than edited, per the drift-evidence rule. Two things the re-read also
  found, pulling severity in opposite directions: the auto-connect work
  **self-heals** (the queue entry is set one line *before* the throw and the
  engine's own 500 ms repeater redoes it correctly), which makes it milder than
  filed; but each throw escaped the console `exec`, so the rest of that cheat
  pass never ran and `ResumeTerrainInvalidations` was skipped **seven times**.
  Also new: the `if not self.broken` guard on the failing block **can never be
  false** — the line above it already cleared the field. → `docs/agent/bugs/F99.md`
  ("Mechanism settled by reading"; the chain folder is deleted — its sealed
  derivation survives in git at `28c253f`).
  *(Chain close 2026-08-03: the terminal prompt settled the mechanism from
  source — the element list was empty BEFORE the rebuild call; the filed
  "rebuild comes back empty" route is refuted, and the drain is the engine's
  own track-merge absorb-walk. This does not change the decision in front of
  you: no-cheat reachability is still unproven, nothing is built, and the
  cheap discriminator offer stands.)*
- **C43 — how do we stop the TestKit printing `[LUA ERROR]` into your logs?**
  Two Wave-5 probes install stubs through `set_global`, which trips the engine's
  strict-global guard on `IsNearDome` and `AddAreaRubble`; both probes then PASS,
  so the cost is entirely two alarming lines in the log next to real errors.
  ⚠️ **Second instance in one day** of the pack logging its own authoring noise
  (F100 is the first). Three options on the entry. → `docs/agent/bugs/C43.md`.
- **The C36-adjacent mysteries grep.** A cheap sweep of `Lua\Mysteries\` and
  `Scenario\` for `IsDisasterPredicted` gates, deliberately left unassigned:
  your call whether it becomes work at all. Not owed. → `CHAIN_QA_REPORT.md` §8.
- ⭐ **DECISION FOR YOU: archive resolved decision bullets the way completed
  test sections are archived?** (routed 2026-08-04 by the unattended-1
  terminal audit, per your stale-records ask.) The checklist's documented rule
  — a completed section moves WHOLE to `PLAYTEST_ARCHIVE.md`, deleted here, no
  stub — covers *test sections*; the growing layer of struck-through ✅
  DONE/DECIDED **decision bullets** has no rule. **Two clear cases were moved
  as a worked example** (co-run #0, and the `LawOfficeDoor`/C44 call — both
  fully closed, durable content already in `SESSION_LOG`/entries; see the
  archive's "Resolved decision records" banner). **My recommendation:** adopt
  the same treatment for the rest — move only bullets that are fully closed
  with nothing owed to you; anything holding an open ask, an on-hold, or an
  owed input (the relabel wording) stays here no matter how struck-through it
  looks. Applying it today would move ~4 more bullets (~60 lines), including
  the 41-line probe-gate record; cost is one commit. Say go/no-go.
- ~~**The probe-gate blocker**~~ ✅ **DECIDED 2026-08-04 — you asked for the
  safest option and that is what was adopted: the tool was NOT loosened.**

  No escape hatch was added to `doccheck.py`. The sweep stays absolute — any
  `TEMPORARY` marker in `Code/` is red, full stop — because a hatch a hurried
  session can open without saying so is how 2026-07-31 happened.

  **What changed instead is when a probe is allowed to exist at all.** New
  binding rule (`WORKFLOW.md` probe hygiene, rule 5): **a probe file is present
  in `Code/` only while its run is actually happening.** Placing it and running
  are the same act; deleting it and recording the answer are the same commit.
  There is no state in between, so **no armed probe can outlive the sitting that
  needed it** — which is the failure you told me to design against.

  **It costs nothing.** Prep still commits early: the staged save, the
  measure-moments list, the doc edits, and the probe's *source* as a code block
  in the brief. A probe parked in a doc physically cannot run — the mod only
  loads files listed in `metadata.lua`, all under `Code/` — so it is inert by
  construction, not merely unused. If a sitting slips, nothing is stranded and
  nothing is armed.

  ⚖️ **One-time override granted 2026-08-04, recorded here so it is not
  invisible.** You gave prompt 3 an override of this rule **for its prep only**.
  It may commit armed probes in **one named commit**, using the `--no-verify`
  bypass with a body stating exactly what is red and why — and ⛔ **if the
  sitting does not happen in the same working session it must delete the probes
  before it stops.** That deadline is the condition the grant rests on: an armed
  probe never survives a session boundary, which is the situation you said you
  did not want back. Not precedent, not carried to any later co-run, and prompt
  4 audits every condition against git.

  ⚖️ **You asked for it to be rechecked — DONE 2026-08-04 (prompt 4): your
  decision holds and the rule stands as written.** The diagnosis re-verified
  from the tool and the hook themselves. The one claim that had been asserted
  without source was verified: the game loads **only** the files listed in
  `metadata.lua` `code` (`Mod.lua:490-521` — both load loops iterate that list,
  nothing scans directories), so a parked probe genuinely cannot run. The
  feared cost was measured away — the parse sweep works on the parked file, so
  prep loses nothing — and declining your override measured what any escape
  hatch would have bought: **0.4 seconds of machine time and none of yours.**
  No recommendation to change anything; the safest option was also free.
- ~~**One cheap hardening from the same investigation, your call:** nothing
  checks the TestKit repo's working tree — a doccheck line that *reports* (not
  blocks on) a dirty tree would close the gap.~~ ✅ **GO given and BUILT
  2026-08-04.** Every doccheck run now prints a `TESTKIT TREE:` line — `clean`,
  or each uncommitted file as a `WARN`. Report-only per your word: it never
  blocks a commit, so TestKit work-in-progress cannot jam the pack. Verified
  on both paths (clean, and a planted temp file).
- **The `DOC_STRUCTURE_REVIEW` recommendations this chain does not adopt** — R4
  (a round-trip step for state-transition claims), R7 (effect-evidencing
  verdicts), R9 (an agent/facts/ review cadence), R14 (a context budget for
  agent docs). Adopt, defer, or drop.
  → `docs/agent/reports/DOC_STRUCTURE_REVIEW.md` §3 and §6.
⭐ **CONVENTION (added 2026-08-03, chain-12 QA, from `BUG_LIST_AUDIT.md`
§10.6f(i)): record the SESSION UPTIME next to any error COUNT.** Cross-arm
count comparisons (this leg's 0 vs that leg's 80) depend on comparable
exposure, and the owner's sessions run 1–6 hours — which makes zero-error
results *stronger* than they read, but only if the uptime is on the record.
One line per leg: "session ~Nh".

⭐ **CONVENTION (added 2026-08-04, owner): CO-RUNS — a rider class where the
agent drives and you are on call, not on duty.** For items with heavy setup and
a short measure, or intermittent triggers you'd never catch in hours of
organic play: the agent preps everything unattended (scripts, staged save
copy, a measure-moments list), launches and drives the game, and you attend
ONLY the minutes where eyes or a judgment call are needed. Such riders are
tagged **TAKEABLE IN a co-run**. Protocol and the forced-vs-organic evidence
rule: `docs/agent/WORKFLOW.md` "Co-runs". First candidates: the F11
pre-wrapper watch (below), C41's vanishing picker (amplified spawn/open loop),
F99's no-cheat discriminator (forced break, organic drone repair), plus the
two C-side console reads that need no eyes at all.

⭐ **ROUTING SWEEP 2026-08-04 (post-rig; the block above predates the rig).**
Every open item re-triaged under WORKFLOW's routing rule now that the rig is
proven. ✅ **ADOPTED by the owner same day** — each item's Status line now
carries its mode; ⚠️ each converted test still gets its setup re-derived in
rig terms by the session that runs it — the designs below were written
assuming the owner drove everything.

⚖️ **Execution rule for unattended work (owner, 2026-08-04):** a truly
unattended item runs as a **two-prompt chain — Opus executes, Fable audits**.
Batched unattended work runs as a **full chain: Opus throughout** (top tier
mid-chain only where something is genuinely complicated), **closed by a
terminal Fable audit**. Full form: `agent/WORKFLOW.md` routing triage.

⚠️ **CORRECTED same day, and it upgrades two verdicts:** the sweep first
claimed "no verified command forces a dust storm". **Wrong — table-staleness,
not a source fact.** `CheatDustStorm(storm_type, setting)` exists, ungated,
with `"normal"` / `"great"` / `"electrostatic"` types (`DustStorm.lua:540`),
and a **static-charged dust devil** can be forced outright (both now in the
HELP verified table, `[NEVER RUN]`). So **F90 moves from organic-only to
co-run STAGEABLE**, and PT-27/PT-28 no longer wait sols for a storm.

| verdict | items | what you still do |
|---|---|---|
| → **UNATTENDED** | **PT-35** (all reads are numbers + save/reload — the "nothing changes on screen" check becomes "the read-back numbers don't change", which is the entry's own claim) · **F99 residue rider** (the rig can STAGE break + cheat + pre-reload read deliberately — it no longer waits for a sitting to happen to use the cheat) · **F99 no-cheat discriminator** (forced break, organic drone repair at speed, log watch — no eyes; still gated on your go, it feeds your severity call) · **load-heal sweep** (Do-first #2 — was ~1 h of you; save/reload cycles are the rig's proven core; re-scope first) — ⭐ **all four are now the `unattended-1` chain** (`agent/prompts/unattended-1/`, built 2026-08-04, Opus×2 + Fable audit per your rule), plus the two `[NEVER RUN]` command verifications and a C42 ride-along | kick off the chain |
| → **CO-RUN** (was full playtest) — ⭐ **the front four + ride-alongs are now the `corun-batch-1` chain** (`agent/prompts/corun-batch-1/`, built 2026-08-04: PT-37 · PT-47 · PT-42 · PT-53 E + F21/C42/popup-trio rides + the optional PT-35 fixture build; Opus prep → your ONE sitting, est. 15–25 attended min → Fable audit. Kickoff: Opus on `01_OPUS_PREP.md`; the sitting runs when you sit) | **PT-37** (break staged via the proven `BreakTrackElement` route, reload cycles rig-driven; your eyes: route formation + the salvage-cursor check) · **PT-47** (agent forces the volley + runs the 5 integrity checks; your eyes: scatter-vs-rank, the one thing that is eyes by nature) · **PT-27/PT-28** (provisioning is the real cost; catch-lists and Health-drop patterns are console reads; PT-28 rides PT-27's storm nearly free) · **PT-42** (agent stages stock/drain at speed; your eyes: the faction panel goals at 3–4 moments) · **PT-53 E** (two hands moments — manual assign, Mod-Manager disable; the load-clean read is log) · **PT-18** (agent stages the landings on a SAVE-E copy; deaths/stranding are counters; ⚠️ SAVE-E itself is still ~30 min of your provisioning) · **PT-10** (setup rig-driven; your eyes: clumping + screenshots) · **PT-15** (reads scripted, `SetLightTrapMode` is a verified command; fixture still needs the mystery pick) · **F74+F53(a)** (harness builds the fresh colony unattended; you: the pack-disable click + the two UI acts) · **PT-60** (suite/reload/log halves rig-side; you keep only the 15–20 min ordinary-play segment) · **PT-20** (you keep the disable click + 10 min play) · riders **F21 · F34(d) · F85 · F38 · popup keystone · §3.6** (each a hands-moment or ride-along once staged) | minutes, named per brief |
| **stays PLAYTEST** | **PT-62 remainder** (the campaign gate — behavioural drain judgment through a landing; rig can carry P12's save/disable/load mechanics) · **PT-21** (organic play IS the test) · **PT-30** (mystery playthrough, UI actions) · **C39** (explicitly a keyboard judgment) · **doctrine C-sitting** (likely co-runnable — re-scope against `CHAIN_QA_REPORT.md` §1.3 before promising) | the sitting |
| **stays ORGANIC-ONLY rider** | **F80 · C25 · F06 · F83 · C40 · C32 · F76/C41 recurrence** (situation must arise; the READS are one-line co-run/console asks when it does) · ~~F90~~ (moved to co-run — see the correction above) | tap when it happens |

Two consequences worth knowing: **your dominant remaining cost shifts from
sittings to fixture provisioning** (SAVE-A/D/E builds — cheats are
scriptable but building placement is UI, so those stay co-op sessions); and
since co-runs ARE attended, a co-run pass you witness can earn `tested`
exactly as a sitting does — F11's watch was denied only by a fixture gap,
not by the format.

## Do first — the campaign's ordered top (chain-12 QA, `agent/reports/CHAIN_QA_REPORT.md` §9)

1. **PT-62's remainder** (→ Colonists & domes) — the only gate left on D12: a
   stable colony so the drain is not fighting an inflow, then the Mod-Manager
   uninstall half and the repaired A/B lever.
2. **The load-heal round-trip sweep** (~1 hour) — save, reload twice, read the
   heal numbers (the Astrogeologist +10% class of defect; two-for-two
   defective on the heals actually tested is the project's worst base rate).
   Design: `CHAIN_QA_REPORT.md` §9 item 2.
   ⭐ **HALF DONE UNATTENDED, 2026-08-04, and it cost you nothing** — the
   `unattended-1` chain re-scoped this into two legs and ran the first.
   **Leg D1 (natural state) — RESULT: nothing fired, nothing repeated.** Three
   loads of a staged copy of `TEST2H TRAIN` (load 1 cold, save, reload, reload),
   pack **81/81 active as READ**, **0 `[LUA ERROR]`**, six heal families read
   identically at every load: all three `HEALDIFF VERDICT` lines say **0 of 6
   families changed**, and **not one pack heal line appears anywhere in the log**.
   Log: `docs/archive/u1c1_Mars.exe-20260804-16.46.30.log`.
   ⛔ **What that does and does not buy, because the difference is the whole
   point.** It *does* falsify the F92 shape on this save — the identity-keyed
   heal that turned 1 modifier into 2 after one save+reload would have shown as a
   growing count, and `AutomaticMetalsExtractor` read 2 on all three loads — and
   the F88 shape, the unlatched restart, which would have re-printed every load.
   It does **not** test any heal doing its job: nothing was broken, so nothing
   healed. Two families were **not sampled at all** — H1 astro (the colony runs
   the **rocketscientist** commander, not astrogeologist) and H3 biorobots (0
   biorobots on the save) — and are reported as unsampled, never as clean.
   ⇒ **The remaining hour of your time is not owed:** leg D2 forces the defect
   state and samples the heals firing. Your call is only whether the D2 result
   plus this one closes the item.
   ⭐⭐ **LEG D2 RAN TOO — DONE, and it PASSES. Nothing here is owed to you.**
   Two families were driven from their actual defect state on a staged copy and
   watched through a save/reload/save/reload cycle
   (`docs/archive/u1c6_Mars.exe-20260804-17.24.57.log`):

   | family | forced to | after the healing load | after a further save+reload |
   |---|---|---|---|
   | **H5** `Fix_MeteorFrequency` (F88) | `SMRFixPack_MeteorLatch = false` | one `one-shot heal … (latch false -> 1.0.1)` line, latch `1.0.1` | **no line**, latch `1.0.1` |
   | **H6** `Fix_RainsDeadlock` (C34) | `RainsDisasterThreads = false` | one `RainsDisasterThreads was false — recreated as an empty table` line, `type=table entries=2` | **no line**, `type=table entries=2` |

   All three PASS conditions hold: a heal line for each forced family after the
   healing load, **none** after the idempotence load, and every number back to
   **exactly** the baseline — never above it, which is the F92 compounding shape
   that would have been the failure.
   ⛔ **Ceiling and honest gaps, stated with the result rather than after it.**
   This is **MECHANISM**, not `tested` — it says how these heals behave when they
   fire, not how often a real save needs them. **H1** (Astrogeologist) stayed
   **unsampled**: the colony runs the **rocketscientist** commander, so there was
   nothing to strip. **H2 / H3 / H4** were deliberately not forced — doing so
   means editing colonist traits, dome membership or built objects, a bigger
   mutation than the measurement is worth — so they stand as leg D1 found them.
   ⭐ **A vanilla fact fell out of the forcing:** with `RainsDisasterThreads`
   set to `false`, shipped code threw `attempt to index a boolean value (upvalue
   'old_threads')` at `TerraformingDisasters.lua:411`. The state C34 repairs is
   not merely untidy — vanilla indexes that GameVar with no type check and
   raises. That error is **ours**, inside the probe's marked forcing window, and
   is reported as a consequence of the forcing, not as a new defect.
   ⇒ **Do-first item 2 is complete to its unattended ceiling.** What is left is
   your judgment call on whether that closes it, not an hour of your play.
3. **The doctrine C-sitting** — closes the one INFERRED cell in the "OFF is
   three different things" doctrine, the one the owner said we cannot be wrong
   about. Protocol ready in `CHAIN_QA_REPORT.md` §1.3; the agent builds the
   TEMPORARY probe in-sitting and it dies in the result commit.
4. After those: pick a group and clear it in one sitting. Riders are
   opportunistic — take them when their situation arises; never schedule one.

## The protocol — what a sitting is

A sitting = you at the game + a live agent session reading this file and the
entries. You supply observations **in the moment**; the agent supplies
expectations, forensics and log links. Probe-verified ≠ tested: a pass at the
keyboard is what earns a fix `tested` in `agent/bugs/`.

1. **⛔ PT-00 — the stale-probe sweep, BEFORE the game launches** (hard rule,
   owner, 2026-08-01). The agent runs
   `grep -rln "TEMPORARY" Code/ ../SMR-BugFixPack-TestKit/Code/` and reports
   **CLEAN** — zero hits, or every hit declared by this sitting's design. Not
   clean → delete the stale probe (+ its metadata/items lines), commit,
   re-sweep — or the sitting does not test. No result is recorded without it;
   the `PROBE SWEEP:` line goes in every result commit. Full rule:
   `agent/WORKFLOW.md` "Probe hygiene".
2. **Predictions BEFORE the leg.** The agent writes numbered predictions from
   the entry before anything runs — the discipline moved from this document
   into the sitting, and PT-61 is the proof it pays (ten predictions, ten
   readings, two riders closed free). A prediction that misses is the finding.
3. **Console steps come from the agent, one command per line**, drawn from the
   entry and PLAYTEST_HELP's verified command table.
4. **PT-22 — the log review, after EVERY session, together.** Newest
   `Mars.exe-*.log` under `%AppData%\Surviving Mars Relaunched\logs`: any
   `[CommunityFixPack]` error/inactive/deactivation line, any `[LUA ERROR]`
   naming pack code, any engine error you did not see vanilla,
   `SMRFixPack.ListFixes()` reading `active` for every default fix (count per
   `agent/STATE.md`; opt-ins read `inactive` unless you enabled them — and
   Mod Options survive a Mod-Manager disable, so read the list, never assume).
   ⛔ **Every unexplained line is reported verbatim with its age** — "not
   caused by our leg" is an attribution verdict, never a dismissal; every
   pushback so far has turned up a vanilla defect that was not on our list.
   Passive watch, no action: if `WATCHDOG — Meteors thread silent` ever
   appears, report it verbatim (F02).
5. **Recording (the agent, same sitting or next session):** the result goes on
   the `agent/bugs/` entry with the date and the **session uptime next to any
   error count**; a PASS flips status in front matter AND heading tag (INDEX
   is generated — never hand-edit); a FAIL files a finding and flips nothing;
   when a status flip will cite a log's numbers, the log is copied into the
   repo in the same commit (R8) — ⛔ **`.gitignore` line 2 is `*.log`, so a
   plain `git add` DROPS IT SILENTLY and the commit still looks complete; use
   `git add -f docs/archive/logs/<name>.log`** (found the hard way 2026-08-03,
   after one commit shipped claiming logs it had not committed); the completed
   section moves WHOLE to
   `PLAYTEST_ARCHIVE.md` and is **deleted from here with no stub or pointer
   left behind**. `python tools/doccheck.py` before every doc commit.

*(This section recreates the checklist's "Reporting protocol", which turned
out to have been deleted by accident in commit `22d7b36`, 2026-08-02 — the
top-of-file link had been dangling since. The original text, old paths and
all, is in git and in the snapshot.)*

---

# Trains — one sitting clears the group

> ✅ **PT-37 RAN 2026-08-05 (corun-batch-1 sitting, attended) and moved WHOLE
> to `archive/PLAYTEST_ARCHIVE.md`.** Case A PASS (better than a no-op:
> 559→558 connections, persisted through save+reload; you watched a train pass
> through every station); case B UNSAMPLED — the harness refused to run it
> because the walk cannot fail via meteor damage, which contradicts F48's
> blocking premise for its cited scenario. **The F48 ship/hold decision is
> yours — "Decisions waiting on you", item 1.**

### Rider — F80: colonists wait at platforms, or walk past working stations · Status: unrun — take it WHEN the symptom appears; never schedule it
**Bug:** trains sometimes never enumerate a valid destination from a stop —
one origin/destination pair fails inside an otherwise healthy network, so
colonists either queue forever or set off overland and suffocate. The
strongest reported-but-unpinned defect on the list; the mechanism now has an
exact source predicate but the trigger has never been proven.
→ [agent/bugs/F80.md](agent/bugs/F80.md)
**Requirements:** None / any colony where the symptom appears — colonists
queued while trains come and go, or walkers passing a working station.
**Setup:**
1. ⛔ **Tap before mitigating** — adding trains is the known workaround and it
   destroys the evidence. Open the agent session the moment you see either
   symptom.
2. Tell the agent which symptom (waiting vs walking) and the exact
   origin/destination pair that fails.
3. The agent hands the three reads (classify · enumeration tap · both-ends
   reachability test) — all read-only, all on the entry.
**Good to have:** note whether any track segment on the line was under
construction (the rival explanation the agent must exclude).

### Rider — F21: re-earn `tested` for the wait-time fix · Status: unrun — optional · ⭐⭐ **2026-08-10 THE PENALTY HALF IS MEASURED AND THE FIX WAS WITNESSED FIRING** (`corun-batch-2`): one named colonist watched across a real, unforced boarding — `start_wait 239310758 -> 239344642`, **+33,884 ms to the boarding moment**, after 205 polls reading `Waiting`. The 2026-08-05 `spent_time=nil` was our reader, not the game. ⚠️ Still NOT re-earned as `tested` — one boarding is an instance, not a keyboard pass · **mode: co-run ride-along** (routing 2026-08-04) · ⚠️ 2026-08-05 HALF measured: the platform-population read ran live (11 stations / 21 colonists waiting / 8 trains) but the penalty half is UNMEASURED — every train sampled read `spent_time=nil` (4 of 8 sampled), a reader gap, not a verdict; stays `fixed`, not re-earned
**Bug:** the fix (platform waiting no longer billed as travel time) passed
PT-43, but the Tier-2 rewrite replaced the mechanism that pass exercised, so
F21 was honestly downgraded to `fixed`. Two quick reads on any working train
line re-earn the tag; skipping costs nothing — it simply stays `fixed`.
→ [agent/bugs/F21.md](agent/bugs/F21.md)
**Requirements:** None / any colony with a working train line and commuting
colonists.
**Setup:**
1. Let someone wait long at a platform; the agent reads their Comfort log (no
   "travel time" entry from the wait) and the train's *Travel time (rolling
   average)* (excludes the wait).
**Good to have:** a long platform queue — it makes the discrimination obvious.

---

# Drones & hubs

> ⛔ **DRONE PLAYTEST FREEZE (owner decision, 2026-07-31).** No drone
> playtesting of any kind until a final drone plan is in place — half-finished
> tests of superseded designs cost sittings and produce evidence about code
> being replaced. When the rebuild lands, **ONE multi-step drone playtest
> replaces the whole PT-52 family** (one toggle, all or nothing). If a drone
> anomaly shows up organically mid-sitting, capture it on the D06 entry or as a
> new F-number — observing is not playtesting. **NOT frozen:** PT-10 below
> (dome-entrance data, untouched by any dispatch redesign) and F77's own fix
> (shipped, default-on; only its test's packaging was frozen).

### PT-52 — Drone dispatch overhaul · Status: blocked (frozen, pending invalidation and rewrite)
**Bug:** tests D06 `Opt_DroneOverhaul`'s v1 design, and that design is being
rebuilt — every result it could produce would be evidence about code that will
not exist. → [D06](agent/bugs/D06.md), [F77](agent/bugs/F77.md),
`docs/agent/reports/DRONE_OVERHAUL_OPTIONS.md`.
**Requirements:** ⛔ BLOCKED — waits on the approved drone plan; do not run any
part of it. ⚠️ For whoever rewrites this test: the old Trigger C rider's
"uninstall shape" conflated the module TOGGLE with a Mod-Manager disable —
the toggle arm is VOID as an uninstall test ("OFF is three different things",
chain-12 QA re-label, in the snapshot); the rewrite must keep the two arms as
separate steps.
**Setup:** none until the rebuild. The B2 stress protocol and the CAN/CANNOT
judging lists are preserved in the archive snapshot — the rebuild's
verification leg is derived from them.

### PT-10 — Open-roof drone observation (F55) · Status: unrun · ❓ open question · **mode: co-run** (routing 2026-08-04 — your eyes: clumping + screenshots; setup rig-driven)
**Bug:** no expected answer — either result is useful data. The forever-cache
half is fixed and probe-verified; whether opening a dome's roof destroys the
dome-entrance attaches carrying the only drone pathfinding tunnels in is engine
entity data Lua cannot read. Drones-enter-normally closes F55; drones-locked-out
is a new engine-data finding. → [F55](agent/bugs/F55.md)
**Requirements:** SAVE-A / one dome with interior buildings needing maintenance
/ a drone hub with drones parked outside.
**Setup:**
1. `CheatOpenAllDomes()` (also maxes terraforming and activates the Open Domes
   policy — the prerequisites).
2. Run 1-2 sols at ultra; the agent records the four observations (entry): do
   drones enter · does interior maintenance pile up · do drones clump at the
   entrance · does `CloseAllDomes(MainCity)` recover it, alone or only after a
   save/load.
**Good to have:** screenshots — the clustering picture is half the evidence.

### Rider — C25: Jumbo Cave waste-rock wedge · Status: unrun — take it the moment a Reinforcement site sticks
**Bug:** the wedge chain is Src-verified; only the trigger is unproven — does
cave geometry actually strand a waste rock? Non-zero-while-stuck earns C25 its
F-row; **zero while stuck is the more useful result** (the wedge is something
else). → [C25](agent/bugs/C12-C38.md)
**Requirements:** the situation — a Jumbo Cave Reinforcement site stuck on
"construction site is being cleared" / read taken while looking at the
underground map / save vintage recorded (colony begun pre- or post-1.0.6).
**Setup:** while the site is stuck, the agent hands the one console dump
(entry); the reading decides C25 either way.

### Rider — F77: extender-flap Idle-kick · Status: blocked (frozen with PT-52)
**Bug:** the fix ships default-on and is NOT invalidated — how big is the
fleet Idle-kick with and without it? Its check folds into the consolidated
drone PT when the rebuild lands. → [F77](agent/bugs/F77.md)
**Requirements:** ⛔ BLOCKED with the drone freeze.

---

# Disasters

### PT-27 — Biorobots and Dust Sickness (F40) · Status: unrun · **mode: co-run** (routing 2026-08-04 — `CheatDustStorm` forces the storm, HELP table; catch-lists are console reads)
**Bug:** Dust Sickness infected Biorobots — androids bled Health every storm
until cure tech. Fixed: only organic colonists catch it; a load-time heal
clears already-sick Biorobots. → [F40](agent/bugs/F40.md)
**Requirements:** SAVE-A with the Dust In The Wind rule / Biorobots obtainable
(The Positronic Brain breakthrough — provisioning route on the entry) / a dust
storm.
**Setup:**
1. The agent provisions Biorobots and confirms the trait (entry; if none can be
   produced, record "could not set up" and skip).
2. Note who is a Biorobot; wait through a dust storm with the Dust Sickness
   event active.
3. When it resolves, list who caught it — the agent reads against the entry.
**Good to have:** load a save with already-sick Biorobots — the heal log line
(entry). Run PT-28 in the same storm; same save, same sitting.

### PT-28 — Dust Sickness damage spread (F17) · Status: unrun · **mode: unattended ride-along** (routing 2026-08-04 — pure numeric pattern; rides PT-27's storm sitting)
**Bug:** the per-colonist damage roll was computed then discarded — every
carrier lost a flat 10 Health/sol instead of 5-14. Fixed: the losses spread.
→ [F17](agent/bugs/F17.md)
**Requirements:** SAVE-A (Dust In The Wind) / an active dust storm / several
Dust Sickness carriers (PT-27 gets you there).
**Setup:**
1. Pick 4-5 sick colonists in the same dome; note each one's Health.
2. One sol at ultra speed.
3. Compare the drops — the agent reads the pattern (not exact numbers) against
   the entry.

### PT-47 — Bombardment volley shape (F26) · Status: ⭐ **RAN 2026-08-10** (`corun-batch-2` leg R, five forced volleys) — spread reads as a **scatter** from a low camera (your words: "trails seemed scattered"), volley **ENDS 5/5**, dome crack **POSITIVE** ("Hoffman #1 - 3 fractures"), notification **appears**, interception **POSITIVE** via your own MDS-on/off A/B (peak 5/6/6 → 7/7). Only **decal fade** is unsampled — no working instrument. ⛔ NOT `tested`: the volley is forced. Full readings + the three reader defects on `agent/bugs/F26.md` · **mode: co-run** (routing 2026-08-04 — your eyes: scatter-vs-rank; forcing + integrity checks rig-side)
**Bug:** Mystery 7 bombardment missiles flew in a parallel rank instead of a
scatter. The fix is the pack's largest copied function (100 lines), so
"nothing else about a bombardment broke" is half the test. → [F26](agent/bugs/F26.md)
**Requirements:** a Mystery 7 bombardment, or any save + the console force
(the agent hands it, entry) / a low camera angle so the trails are visible.
**Setup:**
1. Watch a volley arrive — scatter, not a rank.
2. The agent walks the five integrity checks from the entry (decals, dome
   cracks, notification, interception, and the volley ENDING).
3. Log check for bombardment errors.
**Good to have:** an off/on A/B of the spread — that is the reachability
audit's settling observation for F26.

### Rider — F90: underground breaks during a surface storm · Status: unrun · **mode: co-run, STAGEABLE** (routing correction 2026-08-04 — `CheatDustStorm` is real and ungated, so the storm can be forced on a staged elevator-colony copy; the break DISTRIBUTION stays the organic measured path. An organic storm sighting still counts — take it if one arrives first)
**Bug:** surface dust storms could break cables/pipes on the underground map
through the merged elevator grid. The defect is a victim *distribution*, so
one quiet session proves nothing — the read is zero NEW underground leak
notifications during a surface-only storm, cave-ins excluded.
→ [F90](agent/bugs/F90.md)
**Requirements:** underground unlocked / at least one elevator built / a
surface dust storm running / the merged fragment holding >10 connectors
(agent checks).
**Setup:** while the storm runs and for a while after, watch the underground
map's notifications; the agent excludes cave-ins and reads per the entry
(including the known surface-rate residual that is NOT a miss).

---

# Rockets & landers

### PT-18 — Arrival deaths, including the elevator path (F53) · Status: unrun · **mode: co-run** (routing 2026-08-04 — landings staged, deaths/strandings are counters; ⚠️ SAVE-E provisioning is still yours, ~30 min)
**Bug:** newly arrived colonists could walk toward unreachable domes and
suffocate, and the reworked fix's broken case WAS the elevator path — so that
path is tested deliberately. Fixed = nobody dies on arrival: safe drop spots,
elevator riders keep their assignment, unreachable-dome arrivals wait under
"Confused Colonists" and retry. → [F53](agent/bugs/F53.md)
**Requirements:** SAVE-E / an underground dome with free housing reachable
only via the Elevator / a surface rocket landing pad.
**Setup:**
1. Case A — land colonists on the surface away from any dome; watch where they
   walk and whether anyone dies or goes Abandoned.
2. Case B (the important one) — make the underground dome the only free
   housing (fill/close the surface domes), land a rocket, follow the arrivals:
   to the Elevator, down, and in.
3. Case C — land where the nearest dome by straight line is unwalkable while a
   walkable one exists further away.

### Rider — F74 + F53(a): the never-modded fresh-colony pair · Status: unrun · **mode: co-run** (routing 2026-08-04 — the harness builds the fresh colony; you: the pack-disable click + the two UI acts)
**Bug:** two "is the vanilla harm real at all" observations that need a true
vanilla control — a pack-lineage save cannot serve (persisted thread stacks
carry pack code). F74's half no longer decides anything (two outside witnesses
answer it); it rides only because the colony is already there.
→ [F74](agent/bugs/F74.md), [F53](agent/bugs/F53.md)
**Requirements:** a FRESH ten-minute colony that has NEVER had the pack
installed / pack disabled for the sitting.
**Setup:**
1. Order an RC Transport onto a landed storybit trade rocket — does the
   original harm actually occur?
2. Land a passenger rocket flush against a Universal Depot — do arrivals
   actually strand?

### Rider — F83: is the paid Detailed Scan reachable elsewhere? · Status: unrun
**Bug:** after declining or losing a `ReconCenterDiscoveryAsteroid` popup, is
the paid Detailed Scan reachable anywhere else (planetary view)? Settles the
popup audit's verdict on F83's second site. → [F83](agent/bugs/F83.md)
**Requirements:** a Recon Center holding enough Electronics for the scan / the
asteroid popup declined or lost.

### Rider — C32: the asteroid-abandon label read · Status: unrun
**Bug:** does abandoning an asteroid desync building labels? The row was
rewritten 2026-08-01: you must ABANDON manually (asteroids never expire on
1.0.7) and destroyed buildings must be excluded or the first meteor strike
false-confirms it. Non-zero = the defect; zero still proves nothing.
→ [C32](agent/bugs/C12-C38.md)
**Requirements:** an asteroid mission you are willing to abandon
(`UIAbandonAsteroid`) / the read taken on the map whose buildings you care
about.
**Setup:** after abandoning, the agent hands the corrected membership read
(entry).

### Rider — F34(d): landscape mark over a loading rocket · Status: unrun · **mode: co-run** (routing 2026-08-04 — staging rig-side; your eyes on the yank)
**Bug:** drop a landscape mark over a rocket actively loading drones — is a
mid-"Embark" drone visibly yanked, or does it recover silently? Settles the
reachability audit's verdict. → [F34](agent/bugs/F34.md)
**Requirements:** a rocket mid drone-embark / landscaping unlocked.

---

# Colonists & domes

### PT-62 — D12 "no homeless" remainder · Status: ✅ P4/P6 PASSED 2026-08-03 (dome went 23 → 0, overpop cleared) — P12 · P13 · P14 · the landing check still owed. ⛔ NOT a release gate (opt-in; owner, 2026-08-03)
**Bug:** the module works — same colonist, same moment: vanilla answered
`false nil`, D12 supplied a reachable suitable dome — but the first sitting's
drain fought an inflow (the ping-pong finding), and the three changes built in
response are UNRUN. This remainder is D12's only gate. → [D12](agent/bugs/D12.md)
**Requirements:** a STABLE colony — the drain must not fight an inflow /
restart first (**four** unrun changes as of 2026-08-03) / Mod Manager for the
uninstall half / **a flagged dome with an open service work slot, for P14**.
⛔ **Do NOT use D03 "Closed to new residents" as a fixture control** — the old
plan said to; withdrawn 2026-08-03. It works, and that is the problem: D03 sits
on the SAME two seams D12's guards do, so it would mask the guard under test and
make the loop check trivially 0 for the wrong reason. It also blocks Seniors.
Entry (incl. the same-day correction to an earlier, wrong reason for this).
**Setup:**
1. Restart, then the suite run.
2. The loop check — ⛔ **use the SPLIT counter, not the old one** (entry,
   2026-08-03): the blind version counts cohort delivery, which a flagged dome
   is REQUIRED to keep receiving, so it cannot fail honestly. Only **inbound
   SUBJECTS** is a leak, and it must be 0 and STAY 0 **through a rocket
   landing** — a single at-rest reading does not test the `ChooseDome` half.
3. P4/P6: the drain clears the dome, **run clean — no D03 crutch** (above); a
   dome that refills anyway is a FINDING, not a fixture problem. Mind the
   entry's employed-homeless caveat before reading P6.
4. ⭐ **P14 — the free-work door** (new 2026-08-03): flag a dome that has an
   open work slot and watch whether the slot **FILLS**. ⚠️ **`0 would move` on
   a recruiting dome is the door WORKING, not a miss** — that is the reading
   most likely to be misfiled. If the slot never fills while unemployed
   homeless sit there, the door needs a dwell bound and D12 does not ship as
   built.
5. P13: the repaired `SMRFixPack_Disabled.NoHomeless` lever mid-drain.
6. P12: save flag-ON → Mod-Manager disable → load clean.
   (Predictions P1-P13 and the four setup traps: archive snapshot; the re-run
   musts incl. P14: entry.)

### PT-53 — Cohort housing, Trigger E (D07) · Status: partial (A-D passed; E owed) · **mode: co-run** (routing 2026-08-04 — two hands moments: the manual assign, the Mod-Manager disable; the load-clean read is log) · ⚠️ 2026-08-05: E's precedence half ROUTED (fixture unholdable — every slot created was consumed in seconds; a design decision went to you instead, item 2 above); in-dome pass MEASURED at colony scale (76→37); **only the uninstall half below is still runnable as written**; ⭐ **the UNINSTALL half RAN 2026-08-10 (`corun-batch-2` leg T) and is CLEAN** — `pack=0/0 active`, zero engine errors, zero new log lines after a minute of play. ⛔ **But it took two attempts: a Mod-Manager disable does NOT take effect until a full game restart** (first attempt read `pack=81/81` and would have banked a clean log of the pack RUNNING). See decision 6 above and `agent/bugs/D13.md`
**Bug:** Seniors/Children in normal housing move to free cohort slots and are
otherwise left alone — triggers A-D passed live ("it worked wonderfully").
Only E remains: player-order precedence and the uninstall shape.
→ [D07](agent/bugs/D07.md)
**Requirements:** any colony with the module on / a Senior you can manually
assign to a normal residence / Mod Manager for the uninstall half.
**Setup:**
1. Manually assign a Senior to a normal residence (player order) — they must
   STAY. ⚠️ 2026-08-05: build the pin BEFORE any free cohort slot exists —
   pin first, create the motive second (three failed attempts and the 5-sol
   pin timeout are on the entry).
2. Toggle the module off — instantly vanilla (behaviour check).
3. Save with it ON → disable the PACK in the Mod Manager → load: clean, no
   `[LUA ERROR]` naming pack code. (A toggle cannot answer an uninstall
   question — "OFF" is three different things, `agent/facts/`.)

### Rider — C40: Crowded Living capacity read · Status: unrun — take it when the law + a working Ministry of Culture exist
**Bug:** not a defect hunt — the ministry gating is intended. Open: the law's
description says +3 while possibly delivering +6, and losing the ministry may
evict people already housed. Harm unproven and deliberately not guessed.
→ [C40](agent/bugs/C40.md)
**Requirements:** Crowded Living enacted / a Ministry of Culture built and
working.
**Setup:** note a Residence's capacity → stop the ministry (off, or cut power)
→ re-read the same Residence; then watch whether anyone was actually evicted
(entry details, including why shift rotation will not trigger it).

### Rider — F11: verify the pre-wrapper conversion · Status: ⚖️ **TWO OF THREE READINGS PASSED 2026-08-04 (co-run #1, you attended)** — the third is unavailable on that save; **your call whether it closes** (decision above). Remainder is **TAKEABLE WHEN** a sitting runs on a save WITHOUT `LuxuriousTrains`, or with a train on a `seen_forest` track
**What ran.** `TrainPlatformWedge` read `active`; 7 trains completed full
`GotoStation → UnloadTrain → LoadTrain → GotoStation` cycles over 238 s, **340**
passenger removals from train holders, **0** wedge candidates, and you watched
one unload and leave. ⛔ **The stat reading could not be taken** — both shipped
branches are switched off on that save by design, so `0` and `0` mean nothing.
⛔ **`tested` is NOT claimed.** Card 1 in `agent/reports/CORUN1_EVIDENCE_CARDS.md`.


**Change, not a bug:** 2026-08-03 the F11 fix was converted from a ~30-line full
method copy to a 10-line pre-wrapper (same repaired branch, original method
called for everything else). It is behaviour-preserving **by construction** and
has NOT been verified live — this rider is what earns that back.
→ [F11](agent/bugs/F11.md)
**Requirements:** pack ON, any train line that actually moves colonists. No
cheats, no save juggling — an organic warm-up leg is enough.
**Setup:** none beyond playing. Watch three things during normal train use:
`SMRFixPack.ListFixes()` shows `TrainPlatformWedge [active]`; trains unload and
LEAVE stations normally; passenger comfort/sanity still move on disembark (the
travel-time penalty and the forest bonus now run vanilla's own lines instead of
our copy).
**The check can fail:** a train wedged at a platform, or disembark stat changes
that stopped happening, falsifies the conversion — say so and the copy form
comes back from git (`3a6512f^`).

### Rider — C42: does a passage traversal leave a stale passenger behind? · Status: unrun — **TAKEABLE WHEN** any colony has a built Passage that colonists actually walk through · ⭐ mechanism link CLOSED 2026-08-04 · ⚠️ 2026-08-05: a WITHIN-SESSION read finally ran (no save/load since traffic) and was STILL unsampled — 0 unit entries over 4 passages; the gap now needs a **traversal witness** (a colonist seen inside a passage element), not merely generated traffic
**Bug:** `PassageBase:TraverseTunnel` ends with a raw `unit.holder = nil`
(`Lua/Passage.lua:1055`), which skips the call that would remove the colonist
from the last passage element's `units` list. If so, demolishing that passage
later teleports uninvolved colonists to it and cancels what they were doing.
⭐ **The untraced link is TRACED and HOLDS (unattended-1 leg F, 2026-08-04;
re-derived independently by the terminal audit):** a passage element IS a
`Holder` (`Building`→`BaseBuilding`→`Holder`) and `LeadIn` really does set
the holder, so the stale-entry mechanism is real as written — refined: **one**
stale entry per traversal (on the last element entered), not N. The rig's
post-load read was `C42STALE 0` over **0 unit entries** — UNSAMPLED, and
nothing establishes `Holder.units` survives a load at all. → [C42](agent/bugs/C42.md)
**Requirements:** a Passage with traffic. Nothing else; no cheats, no save
juggling. ⛔ **The read must be WITHIN-SESSION** — after real traversals and
**before any save or load** (a post-load zero is the F99 mistake shape).
**Setup:** one console line, any time after some colonists have crossed —

```
*r local a=0 for _, c in ipairs(Cities) do for _, p in ipairs(c.labels.Passage or empty_table) do for _, el in ipairs(p.elements or empty_table) do for _, u in ipairs(el.units or empty_table) do if u.holder ~= el then a=a+1 end end end end end ConsolePrint(print_format("C42STALE", a))
```

**The counter can fail:** ⚠️ *(corrected 2026-08-04 by the unattended-1 audit —
this line used to say "`0` refutes the entry outright", and that is wrong: a
`0` counts as a refutation ONLY if the denominator was populated — units
actually inside passage elements when the read runs, within-session.)* A `0`
over a non-zero unit-entry population refutes the entry; a `0` over zero
entries samples nothing. Non-zero confirms the desync and the follow-up is to
demolish that passage and watch whether an unrelated colonist teleports to it.

### Rider — F99: re-read the track residue BEFORE a reload · Status: **unrun — the rig RAN the recipe 2026-08-04 and the rider's own precondition never arose; ⚠️ 2026-08-05 added TWO MORE witnessed attempts (meteor repairs on one track, 201 new-build sites across three tracks with the merge confirmed) and `TrackElement.lua:805` did not fire in either, so the gate still never opened — three attempts, zero throws, rate bounds only** · **mode: unattended, STAGEABLE** (routing 2026-08-04 — the rig stages break + cheat + pre-reload read deliberately; owner-rule chain applies: Opus runs, Fable audits. The old TAKEABLE-WHEN framing — wait for a sitting to happen to use the cheat — is superseded)
⭐ **What the 2026-08-04 attempt (unattended-1 leg B) established:** one staged
break + `CheatCompleteAllConstructions()` produced **zero** `:805` throws, so
the "if `:805` appears" gate below never opened — the rider needs a run in
which the throw actually happens. Gained anyway: `F99RESIDUE 0 0` pre-reload
is the reading a *healthy* completion produces (so the fixup is no longer the
only explanation shape); the `BreakTracks({element})` instrument is confirmed
by execution (`repair_cgs` 0→1); and the counter has a liveness witness. Log:
`docs/archive/u1c3_Mars.exe-20260804-17.06.05.log`; full record on the entry.
**Bug:** the `F99RESIDUE 0 0` reading that made F99 look harmless was taken
**after** a reload, and load runs `SavegameFixups.RebuildBrokenTracksAndConnect`,
which sweeps exactly what the probe was looking for. The null result is
therefore not evidence of no damage. → [F99](agent/bugs/F99.md)
**Requirements:** the cheat, plus at least one outstanding repair group —
`repair_cgs` is only ever populated by meteor strikes and disaster damage, so on
a clean build-out there is nothing for the probe to find and `0 0` is
guaranteed regardless.
**Setup:** run the cheat, and if `TrackElement.lua:805` appears in the log,
**read this before saving or loading anything**:

```
*r local a,b=0,0 for _, c in ipairs(Cities) do for _, t in ipairs(c.labels.TrackBase or empty_table) do if #(t.elements or empty_table) == 0 then a=a+1 end if t.repair_cgs and #t.repair_cgs > 0 and #(t.elements_under_construction or empty_table) == 0 then b=b+1 end end end ConsolePrint(print_format("F99RESIDUE", a, b))
```

**The counter can fail:** a non-zero `b` is a track stuck showing damage and
refusing to be salvaged, and would move F99 off `cand` on the spot. Note the
session uptime next to the count (the 2026-08-03 convention above).

### Rider — C39: Service Automation and the four Workshops · Status: unrun — take it when the law is enactable
**Bug:** the law halves staffing by LABEL while its performance compensation
keys on CLASS; the four Workshops sit on the wrong side of that line. The sign
of the harm is genuinely unclear — this is a keyboard observation, not more
reading. → [C39](agent/bugs/C39.md)
**Requirements:** Service Automation enacted / a staffed Workshop plus a
Diner or Spacebar in the same dome as the in-family control.
**Setup:** read workers-per-shift, performance and the Comfort the shift pays,
workshop vs control (entry).

---

# Mysteries

### PT-15 — Wisp power output (F07, + F15 bonus) · Status: unrun · **mode: co-run** (routing 2026-08-04 — reads scripted, `SetLightTrapMode` verified; the SAVE-D mystery fixture is the real cost)
**Bug:** freeing the wisps rewarded ~1/1000 of the promised power — a trickle
instead of kilowatts. Fixed: ~1000 × wisp count, a real power source.
→ [F07](agent/bugs/F07.md), [F15](agent/bugs/F15.md)
**Requirements:** SAVE-D — St. Elmo's Fire mystery with Light Traps holding
wisps (pick the mystery at new-game setup; the console route is on the entry —
disclose if used).
**Setup:**
1. Choose "free the wisps" (or the console form, entry).
2. The agent reads a trap's output (entry): trickle = broken, ~1000×wisps =
   fixed.
**Good to have:** on a separate trapful, destroy mode — the research points
granted must MATCH the notification's number (the F15 half).

### PT-30 — Finished Mirror Sphere site (F16) · Status: unrun
**Bug:** a finished excavation site kept offering its actions, wasting drone
work on a site that cannot progress. Fixed: the finished site starts nothing;
cancelling still works. → [F16](agent/bugs/F16.md)
**Requirements:** a Mirror Sphere mystery game (new-game pick) / played to a
scanned excavation site with a Drone Hub in range.
**Setup:**
1. Control: while the site is part-way done, confirm its actions can start.
2. Run the excavation to 100% — the sphere launches and detaches.
3. Try each action on the finished site — the agent reads per the entry.
**Good to have:** the settling observation rides along: do drones engage a
dead request when an action is clicked?

### Rider — F06: Mystery 10 epilogue arrival · Status: unrun
**Bug:** reach the finale and ignore the corner notification for one sol at
speed — does the Epilogue really arrive minimized and unpaused? Settles the
reachability audit's verdict. → [F06](agent/bugs/F06.md)
**Requirements:** a colony at the Mystery 10 finale.

---

# Any-save & factions

### PT-35 — Save sanitizer does no harm (F35, F03) · Status: unrun (case A only; B/C parked) — ⭐ case A RAN unattended 2026-08-04: do-no-harm half PASSES, turbine half UNSAMPLED (fixture gap, see below) · ✅✅ **THE FIXTURE GAP IS CLOSED 2026-08-10** — `PT35FIXTURE.savegame.sav` is in your save folder (`corun-batch-2` leg S): FrictionlessComposites researched, **one Large Wind Turbine**, **one applied building upgrade** (Remote Medic on a Hospital, for the F03 half). **The turbine-half re-run is now an unblocked 2-prompt unattended chain** — nothing of yours needed. ⛔ Do not delete that save · **mode: UNATTENDED** (routing 2026-08-04 — all reads numeric + save/reload; owner-rule chain: Opus runs, Fable audits)
**Bug:** the pack's two sanitizer passes run automatically on every load for
every player, and the F03 pass REMOVES label modifiers from persisted colony
state — this is the do-no-harm check on auto-running save-writing code, and
the only part of PT-35 that was ever about risk. Cases B and C are PARKED
(`FUTURE_IDEAS.md` entry 4). Both passes are probe-covered; this is cheap
insurance, not substitute coverage. → [F35](agent/bugs/F35.md),
[F03](agent/bugs/F03.md)
**Requirements:** None / any healthy save with a Large Wind Turbine and an
upgraded Medical Center in a dome / ~5 minutes.
**Setup:**
1. Note the turbine's Power production and the dome's birth-comfort figure.
2. Run both console calls — `SMRFixPack.Sanitizer.RepairTurbineBuff()` and
   `SMRFixPack.Sanitizer.RepairLeakedUpgradeModifiers()` — both must return
   **0** and nothing on screen may change.
3. Save, reload, check again. A bonus that GREW on the second run is the FAIL
   (the pass is not idempotent — record the exact figures).

⭐ **RAN UNATTENDED 2026-08-04 (unattended-1 leg A) — case A's do-no-harm half
PASSES; half of it is UNSAMPLED. Status stays `unrun`; this is not a `tested`
grant and cannot be (unattended ceiling is MECHANISM).**

**Run conditions.** Retail `Mars.exe` **1.0.7.396349**, cold load of a staged
COPY (`U1STAGE.savegame.sav`) of `TEST2H TRAIN`, pack **81/81 active as READ**,
speed 3, 2 loads, **0 `[LUA ERROR]` lines in the window**. FORCED: nothing but
the two calls themselves. ORGANIC: nothing. Raw lines:
`docs/archive/u1c2_Mars.exe-20260804-17.03.10.log`.

| step | reading |
|---|---|
| both calls, load 1 | `RepairTurbineBuff ok=true returned=0` · `RepairLeakedUpgradeModifiers ok=true returned=0` |
| numbers before → after, load 1 | `0 of 7 readings changed` |
| save → reload, numbers across the round trip | `0 of 7 readings changed` |
| both calls again, load 2 | both `returned=0` |
| numbers before → after, load 2 | `0 of 7 readings changed` |
| start → finish | `0 of 7 readings changed` |

⇒ **Nothing grew, nothing changed, both passes returned 0 twice.** That is
step 2's "nothing on screen may change" and step 3's FAIL condition, in the
numbers the entry's own claim is about.

⛔ **What is NOT sampled, stated before anyone quotes the PASS.** The fixture
this test asks for is **not on this save**: `FrictionlessComposites
researched=false`, **0 Large Wind Turbines**, **0 Medical Centers** (13 domes,
47 dome label modifiers).

- **`RepairTurbineBuff`'s 0 is trivially forced and samples nothing.** It
  early-returns at `Code/90_SaveSanitizer.lua:58` —
  `if not colony:IsTechResearched("FrictionlessComposites") then return 0 end` —
  so the pass never reached its body. **UNSAMPLED, not a do-no-harm result.**
  Re-running this half needs a save with that tech researched.
- **`RepairLeakedUpgradeModifiers`'s 0 is real but partial.** It ran its full
  body over the colony, every city and all 13 domes — 175 label-modifier
  entries — and removed none. So *"it does not strip live state"* is sampled on
  a real population. *"It clears leaks"* is not: whether the save held any id of
  the form `<handle>_upgrade<N>_mod_<M>` at all was not measured.

**What it would take to close case A properly:** the same leg on a save with
Frictionless Composites researched and at least one upgraded building — which is
a fixture request, not a sitting. ⇒ routed as a gap by unattended-1 prompt 2.
⚠️ 2026-08-05: the corun-batch-1 sitting re-read the fixture on every load —
still `FrictionlessComposites researched=false`, 0 Large Wind Turbines — and
the sitting ended before its optional leg-5 fixture build was reached. The
fixture request stands; no FIXTURE save exists.

### PT-42 — Last Transmission notices your reserves (F22, F75) · Status: unrun · **mode: co-run** (routing 2026-08-04 — stock/drain staged at speed; your eyes: the faction panel goals at 3–4 moments) · ⚠️ 2026-08-05 SKIP re-confirmed LIVE, not on prep's word: Last Transmission read `active=false` on the staged `TEST2H TRAIN` copy — 5 active factions, none it, 0 legislature seats — so the fixture requirement below is real and still unmet
**Bug:** the faction's stored-resource goals never cleared no matter how much
you banked, the Oxygen goal was satisfied by Power, and the penalties became
unreachable once a second map was loaded. Probes prove the reserve maths; only
play shows the approval actually moving and the UI goal clearing.
→ [F22](agent/bugs/F22.md), [F75](agent/bugs/F75.md)
**Requirements:** a game with Last Transmission as an active faction (ideally
with the Underground map opened — that is what made the old maths hopeless) /
storage you can build up and then drain.
**Setup:**
1. Open the faction panel; note approval and the listed "How to achieve"
   goals.
2. Stock Power past 2 sols' worth, let a day pass — the Power goal stops being
   listed and approval rises (reason in the approval breakdown).
3. Repeat for Water, then Oxygen — the important one: only Oxygen clears it.
4. Drain one to zero — the matching "No X stored" penalty appears and approval
   falls.
5. The agent checks the two log lines (entries).
**Good to have:** F22's settling observation rides along — where is the
corrupted number player-visible in a young politics colony, before the Martian
Assembly stage?

---

# Cross-cutting — once per era of the pack

### PT-60 — The chain-8b batch leg (F90-F96 + eight conversions) · Status: unrun · ⭐ attended · **mode: co-run** (routing 2026-08-04 — suite/reload/log halves rig-side; you keep the 15–20 min ordinary-play segment)
**Bug:** seven approved fixes and eight technique-only conversions have never
executed in a game; a byte-equivalence argument is not an observation. Nothing
from that batch may be called verified until this leg's numbers are quoted.
→ entries [F90](agent/bugs/F90.md)-[F96](agent/bugs/F96.md); the conversions
and the dated prediction set: the archive snapshot.
**Requirements:** a save PREDATING 2026-08-02 (that is what makes the heal and
idempotence predictions readable) / pack on / ~30-40 minutes.
**Setup:**
1. Load the pre-batch save; note the heal log lines immediately.
2. Suite run + `ListFixes()` — the agent reads the counts and probe verdicts
   against the prediction set written 2026-08-02 (preserved in the snapshot —
   use it, do not re-derive it after the fact).
3. 15-20 minutes of ordinary play — zero pack-named errors, zero visible
   behaviour change from the conversions.
4. Save and reload — no heal line repeats; the cleared rocket-fuel key stays
   absent.
5. Log review per the protocol.
**Good to have:** the F90 rider if a storm arrives on an elevator colony.
⚠️ F92/F95 change real morale/production numbers on load — do not read them as
drift in any A/B taken across this leg.

### PT-21 — Long-save soak · Status: unrun
**Bug:** the whole-pack background check — nothing drifts, leaks or degrades
over a real session of ordinary play.
**Requirements:** any healthy colony / all default fixes `active`
(`ListFixes`) / 45-60 minutes of real play, no cheats.
**Setup:**
1. Just play — mixed speeds, at least one save/reload midway; note anything
   that feels off (stuck colonists, drone clusters, flickering notifications,
   unexplained deaths).
2. At the end, the agent runs the three state reports (reservations, trains,
   broken track — Test Kit, PLAYTEST_HELP).
3. Log review per the protocol.

### PT-20 — Uninstall safety · Status: standing — re-run per era and before release · **mode: co-run** (routing 2026-08-04 — you keep the disable click + the 10 min play; save/reload/log reads rig-side)
**Bug:** the pack must never hold a save hostage. Steps 1-4 passed 2026-07-31;
step 5's hunt found F86 (both sites since repaired — PT-58 measured the same
shape at ZERO errors against leg 5's 80). This is the per-era re-check, not an
open debt. → [F86](agent/bugs/F86.md), `agent/FIX_POLICY.md` §3.
**Requirements:** any current save with the pack on / Mod Manager / ~20
minutes.
**Setup:**
1. Play a few sols, save.
2. Quit → disable the Community Fix Pack ONLY in the Mod Manager (Test Kit
   stays) → restart, load.
3. 10 minutes of ordinary play, one save/reload — the save must behave
   normally (the original bugs coming back is expected and fine).
4. Log: zero errors naming pack code. The agent pulls the full step-5 hunt and
   the 2026-07-31 method corrections from the archive snapshot before running.

### Rider — popup-audit keystone: storybits survive save/load · Status: unrun · **mode: co-run ride-along** (routing 2026-08-04)
**Bug:** the ~5-minute console check that a popup-carrying storybit thread
survives a save taken under its corner notification, and that answering it
afterwards still applies the outcome. Settles the popup audit's keystone.
→ `docs/agent/reports/POPUP_CONSEQUENCE_AUDIT.md` §8 (procedure).
**Requirements:** any save / console open.

### Rider — F85: quicksave under a choice popup · Status: unrun · **mode: co-run moment** (routing 2026-08-04 — the rebind + keypress are hands)
**Bug:** rebind Quick Save to F9, open any choice popup (a launch-issue prompt
is cheapest), press it — does a save land, and does loading it void the
choice? → [F85](agent/bugs/F85.md)
**Requirements:** any save / a cheap choice popup.

### Rider — §3.6 corner (optional): the sol-change autosave under a popup · Status: unrun · **mode: co-run ride-along** (routing 2026-08-04)
**Bug:** with the distress-call popup left open, does the sol-change autosave
fire under it? → `POPUP_CONSEQUENCE_AUDIT.md` §3.6.
**Requirements:** any save approaching a sol change.

### Rider — F38: tunnel-ruin routing (vanilla read) · Status: unrun · **mode: co-run** (routing 2026-08-04 — the pack-disable click is hands; the rest stages)
**Bug:** destroy a tunnel, save/load IN VANILLA, order a colonist or rover
across — does the route still use the ruin? → [F38](agent/bugs/F38.md)
**Requirements:** a vanilla control (pack disabled is fine for this read) / a
destroyed tunnel.

### Rider — F76/C41: depot-picker recurrence · Status: unrun — ONLY if a depot click-load misbehaves again; do NOT go looking
**Bug:** the picker is vanilla and was measured CORRECT — it opens ABOVE the
cursor by its own height, which is intended; do not report that as
displacement. If a Load click ever misbehaves, capture with the two read-only
hooks BEFORE touching anything — and if the symptom is *no picker at all*,
that is the different, never-reproduced C41 witness: say so explicitly.
→ [F76](agent/bugs/F76.md), [C41](agent/bugs/C41.md)
**Requirements:** the symptom recurring — an RC Transport/Dozer depot or heap
Load click that misfires.
**Setup:** the agent hands the two hooks (entry) and records the desktop box /
multi-display geometry alongside.
**Good to have:** the known-good workaround while capturing (verified command):
`rc:SetCommand("TransferResources", depot, "load", "<Resource>", <amount*1000>, true)`.
