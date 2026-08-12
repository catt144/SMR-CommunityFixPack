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

> ✅✅ **The 2026-08-11 "BOTH TICKS DONE" block (Mod-Manager re-enable + Steam
> Cloud untick) is CLOSED and moved WHOLE to `archive/PLAYTEST_ARCHIVE.md`.**
> The audit confirmed the second tick stuck: **two** post-untick launches
> restored nothing, every directory change reconciles by name (59 saves, all
> named, none of the 14 strays back), and the "never say gone" rule is formally
> retired. Nothing here is owed from you.

## Decisions waiting on you

Things that need **your** call, not an agent's. One line each plus where the
reasoning lives; **an agent strikes a line the moment you decide** — just say so
in any session. Added 2026-08-03 by the docs-restructure chain (spec §7 / R10):
these used to be filed only in agent reports, which is where you never read.
⭐ **And fully-CLOSED decision records move whole to `PLAYTEST_ARCHIVE.md`
(rule adopted by you 2026-08-10)** — same treatment as completed test
sections, but only when nothing is owed to you; anything on-hold or holding an
owed input stays here no matter how struck-through it looks.

### ⭐ NEW 2026-08-12 — asteroid Exotic-Minerals freeze (decided in-session; one owed minute)

11. ~~**⚖️ `F102` — the community-witnessed asteroid freeze (Linux/NVIDIA):
    ship our entity-retarget fix without being able to verify the cure?**~~
    ✅ **DECIDED 2026-08-12, your ruling in-session: "Lets do option 3, its the
    easiest and safest, and we will just disclaimer it."** Built the same day:
    `Code/Fix_ExoticDepositSign.lua` re-signs subsurface Exotic Minerals
    deposits onto the remaster's own orphaned sign asset; gameplay untouched;
    safety verified (both sign entities ship in vanilla, saves carry nothing
    of ours, harmless if the freeze lives elsewhere). Your two test legs
    (Windows rig + Steam Deck, both clean) established the freeze is
    configuration-gated to hardware we don't own — the disclaimer text for the
    mod page is drafted in the entry, ready for launch prep (MOD_DESCRIPTION
    stays frozen till then). The outreach alternative (asking the community
    mod's author to test on a freezing save) stays available any time you want
    the cure confirmed. → `agent/bugs/F102.md`.
    **Owed: one minute, next time you're in game with the pack updated** —
    load the D-type asteroid save (`Sylmacaink BH25`), eyeball the three
    crystal deposit signs: new art renders, deposits still selectable, and
    `SMRFixPack.ListFixes()` shows `ExoticDepositSign [active]`. That closes
    the local (safety) half; the entry then waits only on witness-class
    reports.

### ⭐ NEW 2026-08-12 — raised by you mid-sitting during `corun-pt60`

**Cost, stated honestly: the brief promised ~40–60 attended minutes and the
sitting took about 95** (13:38 launch → 15:15 quit). **Roughly 45 of those
minutes were your own three challenges and two staged attempts, and every one of
them changed the record** — the trains question became item 12 below, and your two
F34 challenges (the rocket's reserved pad zone, then transports) rewrote that
fix's route documentation from three wrong claims to one correct route. That is
not overrun and is not scored against you. **Ours is about 10 minutes:** the
brief's console order could not be run as written (it assumed a console at the
main menu), and I compounded it by concluding main-menu input didn't work at all
— the log shows it *did* execute and simply never echoed to the screen, so the
extra load I asked you for was avoidable. The measurement legs themselves ran to
budget. ⭐ **What your minutes bought: the P8 decider, which was unrepeatable —
it needed a save written before 2026-08-02, and `USA Sol 302` was the only one.**

12. **⚖️ TRAINS — do the remaining train items get any more of your attended
    time, or do we stop?** Your words, spoken during the PT-60 sitting and
    recorded here rather than only in an agent doc: *"I feel like I have been
    working on trains since day one of this mod and we still aren't done trying
    to fix and verify trains."* **That is a fair reading of the record, and here
    is the record so the call is yours on facts, not on mood.** Fifteen entries
    in `agent/bugs/` are train/track/platform defects — **`tested` (4):** F44,
    F45, F46, F47 · **`fixed`, never owner-witnessed as `tested` (5):** F11,
    F21, F48, F64, F91 · **`fixed*` (1):** F49 · **`wontfix` (2):** F62, F79 ·
    **still open (3):** F80 `investigating`, F99 `filed`, C45 `filed`. Four of
    the checklist's own test legs are train legs. **What that inventory says:
    the train FIXES are done — twelve of fifteen are built or deliberately
    written off, and nothing on the list is waiting on a train repair.** What
    keeps trains coming back to you is **verification**, not fixing: F21's
    re-earn rider, F80's symptom-triggered tap, and the two `filed` items that
    are rate questions. ⚠️ **F80 is the one that would genuinely cost you** —
    it can only be taken WHEN the symptom appears in your own game, and its
    entry says tapping must happen before you mitigate. **Your call, and any of
    these is a legitimate answer:** (a) close the train verification queue —
    F21 stays `fixed` forever, F80 stays `investigating`, and no future chain
    proposes a train leg; (b) keep only F80's opportunistic tap, drop the rest;
    (c) keep the queue as it stands. This sitting declined F21's rider on its
    own (no instrument in the armed harness) and **nothing here is blocked on
    your answer** — it decides what future chains are allowed to ask you for.
    → the sitting's own record lands in `agent/reports/` at close-out.
    ⭐⭐ **YOUR EXPLICIT ASK, 2026-08-12 — an AGENDA ITEM for the PT-60 audit,
    not a note.** You want the audit session to work out **a route that moves
    the train items into the ready-to-ship column**, instead of every chain
    re-proposing a train leg. ⚠️ **Two corrections the audit must carry into
    that discussion, because they change the question being asked:** (1)
    **nothing train-related blocks the release today** — F21 already ships as
    `fixed` and PT-62's remainder is explicitly NOT a release gate, so this is
    a question about what STANDARD you want (is `fixed` enough to ship, or do
    you want owner-witnessed `tested` on the train fixes before launch?), not
    about unfinished repairs; (2) **C42 is NOT a train item** — it is
    `PassageBase:TraverseTunnel` (dome passages), and it sat beside F21 in this
    sitting's skip list only because both fail for the same reason, a missing
    instrument in the armed harness. ⛔ **The audit does not get to answer the
    standard question itself.** What it owes you is a COSTED ROUTE per
    remaining train item — which instrument each read needs, whether it can
    ever be organic or is forced-only, and what it would cost you in attended
    minutes — so that the ship/no-ship standard becomes one decision in one
    sitting instead of a recurring ask.
    ✅ **ROUTE DELIVERED 2026-08-12 — `agent/reports/TRAIN_SHIP_READY_ROUTE.md`
    (the PT-60 audit).** The one-paragraph version: **three of the five
    unwitnessed `fixed` items (F11, F48, F91) cannot honestly be upgraded by
    any leg at any price** — their guarded states have no organic producer, so
    `fixed` on mechanism evidence is their ceiling and the report says why per
    item. **The two that CAN be bought are F21 (~10–15 min) and F64
    (~5–10 min), together one ~20–30 min rider block on any co-run that stages
    `TEST2H TRAIN`** — the natural host is the PT-20 redo already in the
    queue. F80/F99/C45 stay watch-only (zero scheduled minutes). **So the
    standard question collapses to one decision: ship the train group at
    `fixed` (option A, 0 minutes) or buy the F21+F64 block first (option B,
    one rider block).** Either answer closes the queue; nothing re-proposes
    afterwards.

13. ~~**⚖️ Are cheats on a playtest save a confound that needs defending every
    time?**~~ ✅ **DECIDED 2026-08-12, your ruling mid-sitting — NO, they are
    the normal condition and there is now a standing rule.** Your words:
    *"We really need a standing rule that these saves are play testing saves
    with colonies that are over sized and underindustrialized. They cannot
    support themselves so cheats are needed to keep the colonies alive and
    functional… And unless a chain truely needs a no cheat setup we will
    continue to have to use it, and we will need to prep a save with alot of
    reasouces if we need a no cheat run."* Written into
    `agent/WORKFLOW.md` as a binding rule: cheat markers are **expected** in a
    playtest log and get attributed, not excused; the reason is asked **once**;
    a cheat is a confound **only** where the reading intersects what it changed,
    and the agent must name the intersection or say there is none; and a leg
    that truly needs a no-cheat run must **declare it in its brief and prep a
    resource-rich save**, never improvise on an existing playtest colony.
    **Nothing is owed by you** — this is recorded so no future sitting spends
    your minutes re-litigating it. Trigger: six `ObjCheat CheatFill` markers in
    the PT-60 sitting log, which cost you an explanation you should not have
    had to give.

### ⭐⭐ NEW 2026-08-11 — from the `corun-pt15` SITTING (two calls, both yours)

**Cost, stated honestly: the brief promised ~45–90 attended minutes and the
sitting took about 3h10m.** The overrun is ours except the march itself — that
was you playing your own colony through the mystery, and prep had already
warned the mystery was far longer than the plan first assumed. Itemised on the
session record: our stop-instruction lost the organic wisp reading (recovered
forced — same trap, same 95 wisps, but no longer "your own click"), a speed
instrument recommended the wrong rung and had to be overridden, the HUD kept
silently dropping the march to 1×, and the cheat disclosure took three asks.
**Your deviations (the extra passenger rocket, activating all three shifts)
are what made C39 readable at all and are not scored against you.**

9. ~~**⚖️ `C39` — the four Workshops lose half their staffing with NO
   offsetting uplift whenever Service Automation passes. Repair or not?**~~
   ✅✅ **DECIDED 2026-08-12 — EXTEND THE COMPENSATION, plus the sibling-label
   sweep your questions surfaced.** Ruled after a full walkthrough: the
   Workshops DO take the cut (measured 12→6) and only miss the payback; the
   dev comment states the assumption they violate; performance feeds only the
   shift-end Comfort payment (consumption scales with staffing fraction and is
   untouched, so balance exposure ≈ nil — the fix restores the exact
   conservation your Diner already gets). ⭐ Your questions also found that
   **sibling automation laws exist for `FactoryBuildings` (confirmed in data)
   and `ResearchBuildings`**, never swept for the same label-vs-class
   mismatch — the build enumerates all three labels and covers every mismatch
   found, not just the four Workshops. The delabel alternative (your
   employment-sink intent theory) was considered and declined in favour of the
   dev comment's stated intent. Queued into the next unattended build chain;
   verification re-runs the same paused bracket on a `CP15PT15` staged copy
   (it holds the measured TV Studio Workshop). → `agent/bugs/C39.md`.
10. ~~**⚖️ `C46` — re-graded 2026-08-12 after your challenge: the phantom-power
    state we measured cannot be reached by normal play.**~~ ✅ **DECIDED
    2026-08-12 — WONTFIX, your ruling in your own words:** *"Lets just write
    that one off since its not a true bug."* Your challenge was what caught
    it: the omission is real in the shipped code, but every path that writes
    the trap's power value only runs in "free" mode and the once-only choice
    means the game can never reach the free→destroy sequence our rig forced —
    so organically there is no phantom. Nothing is built; the defensive
    one-liner was declined with this ruling. `CP15F15.savegame.sav` is no
    longer needed for any open question — keep or delete it as you like.
    → `agent/bugs/C46.md`.

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
   ⚖️ **2026-08-11 — you challenged the "no quicksave on retail" claim and the
   challenge holds: STILL OPEN by your call.** The only *sampled* fact is that
   the bindings screen has no save row. Source (including the generated
   executable) says the one Quick Save action is **Ctrl-F9** and only exists
   when `Platform.cheats` is on — but that's an inference chain, and nobody
   has ever pressed Ctrl-F9 on retail. **The 10-second check rides your PT-20
   redo sitting**: press Ctrl-F9 in a colony — a quicksave landing makes the
   default binding a live route into this defect and changes the whole
   disposition; nothing happening confirms the source read. Decision waits.
   ⭐ **Re-routed 2026-08-11 (your corun-pt15 order): the Ctrl-F9 check now
   rides the PT-15 sitting** — any colony works and it answers sooner. The
   PT-20 redo is unchanged otherwise.
   ✅✅ **THE CHECK RAN 2026-08-11 IN THE PT-15 SITTING — Ctrl-F9 IS NOT A
   ROUTE, and you were right to make us press it.** You pressed it; nothing
   happened on all three witnesses (no new save file, no `Game saved:` or
   `Save failed:` line, nothing on your screen). But three absences aren't a
   mechanism, so we took a structural read instead: **the Quick Save action is
   never built on retail.** `Platform.cheats` is falsy, so the block containing
   `idQuickSave` never runs — and `idQuickSave` reads `nil` against **437
   actions, 433 with ids, with the lookup proven working on a known-present
   id**. There is no save-the-game action in the entire set; the only
   `save`-ish entries are map/camera editor tools. ⚠️ Note the save was **not**
   refused — `CanSaveGame()` came back truthy. The action simply isn't there.
   ⇒ **your original challenge is fully vindicated and the observation is
   closed. Only the disposition is still yours** (severity, tier, whether
   anything gets built).
   ⭐ **Prep 2026-08-11 — the check now has three witnesses instead of one, so
   "nothing happened" will be a measurement rather than an impression.** (1) a
   new save file appearing in the save directory, which we list before and
   after; (2) the game's own log line — the quicksave routine prints either
   `Game saved: <name>` or `Save failed: <err>`, so **either line falsifies the
   source read**; (3) your eyes on the quicksave loading screen. Expected file
   name if one lands: `QuickSave.savegame.sav`. **Still your decision either
   way** — the sitting brings evidence, not a verdict.
   ✅✅ **DECIDED 2026-08-12 — BUILD THE `dont_pause` FLIP (your pick, on your
   own proposed fix).** You asked the question that found the better repair:
   the distress-call dialog is the game's ONLY non-pausing popup, and flipping
   it to pause like every other popup closes F85's entire remaining reachable
   surface in one property change (no autosave can land, nothing can queue
   behind it). Built as a chained wrapper, disclosed as a design-judgment
   tweak; queued into the next unattended build chain with its verification
   launch. The bigger per-site rewrite was declined; the distress-call watch
   rider below retires when the fix verifies.
6. ~~**⚖️ Disabling a mod needs a full game restart — does `PT-20` need
   redoing?**~~ ✅ **DECIDED 2026-08-10 — REDO NOW.** A dedicated PT-20 redo
   co-run is queued (your part: the Mod-Manager disable click, a **full game
   restart**, ~10 min of ordinary play; save/reload/log reads are rig-side).
   Its result supersedes the old 98-vs-98 comparison, which may have measured
   the half-disabled middle state. → `agent/bugs/D13.md`, PT-20 section below.
7. ~~**⚖️ Our save-folder cleanup has now failed twice, and we may know
   why.**~~ ✅ **DECIDED 2026-08-11 — KEEP DELETING + VERIFY.** Agent saves
   keep dying in their recording commits; the close-out directory listing
   (now a standing WORKFLOW rule, and it held on the audit's re-check — none
   of the 15 returned) verifies each deletion stuck. The Steam-Cloud
   hypothesis stays parked: if a deleted save ever returns again, that run
   tests it. → WORKFLOW "Co-runs" close-out rule.
   ⭐⭐ **AND ONE RETURNED — 2026-08-11, so the parked hypothesis is now TESTED
   and CONFIRMED. Fourteen of them returned, at the next launch, written before
   the game process even started.** Your decision above was right about the
   listing (it is what caught this) and wrong only in what the listing could
   prove: it establishes that the deletion HAPPENED, never that it held.
   Nothing about the rule changes; a tick of yours removes the cause. See the
   two-ticks block at the top of this file and `agent/facts/EF-051`.
8. ~~**⚖️ There is uncommitted work in the repo that isn't ours, including an
   answer of yours nobody recorded.**~~ ✅ **CLOSED 2026-08-11** — the
   uncommitted work landed in the sitting's commit, and you CONFIRMED the
   typed line as your D07 ruling (item 2 above). Recorded on
   `agent/bugs/D07.md`; nothing further owed.

**⚖️ What the audit changed (2026-08-10, terminal audit of the sitting — every
verdict above SUSTAINED; four corrections to the record, none of which flips a
result):** the "unattributed modal" at ~16:02 **is in the log** — it was the
keystone test's own first storybit, whose popup was answered after a reload
(the sitting's "it's in no log" was wrong; run 1 stays void, run 2 carries the
pass). The mid-sitting instrument recorded as "produced zero output" **did
print** — the game only flushes its log tail at exit, so the check couldn't
see it (that flush behavior is now a recorded fact). The keystone's run-1 gap
was ~15 minutes, not ~8. And prep's wrong "0 defence towers" figure was NOT
inherited from batch-1 — prep re-read it live through the same broken reader.
⭐ One NEW find from reading the whole log: a single vanilla engine error line
during the bombardment window (a rocket departure hitting an invalid station
position) — filed as `C45`, one occurrence, nothing owed from you.

### ⭐ NEW 2026-08-05 — from the `corun-batch-1` sitting (four calls, all yours)

**Cost: the brief promised ~24 attended minutes and the sitting ran about two
hours — but you ruled that this one is not scored against the estimate**, since
the excess was your own deliberate deviation to chase F99 and the dev-cheat
leads (which is where `F101` came from). Recorded as an **owner override** in
the audit. The one piece it does *not* cover is still logged as a real miss:
**M1 was budgeted 3 minutes and took ~25**, because prep's measured fixture had
evaporated and it had to be built live.
→ `agent/prompts/corun-batch-1/03_FABLE_AUDIT.md` §8.

1. ~~**⚖️ Does PT-37's result unblock F48?**~~ ✅ **DECIDED 2026-08-11 — SHIP.**
   The evidence beat the criterion: case A removed a real stale connection
   from your own save lineage and survived reload; case B's assert is
   measured unreachable by meteor. The corrected pass is queued into the next
   unattended chain; PT-35's do-no-harm run covers it in the same launch.
   → `agent/bugs/F48.md`.
2. ~~**⚖️ Should pinning a colonist to a residence also pin them to their
   dome?**~~ ✅ **DECIDED 2026-08-11 — NO DOME PIN**, your 2026-08-10 line
   confirmed as the ruling: *"It should not pin them to the dome, seems like a
   risk for a bunch of weird bug cases."* The module's deliberate split
   stands; no code change. → `agent/bugs/D07.md`.
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
4. ~~**⚖️ `Opt_NoHomeless` self-deactivates at the main menu**~~ ✅ **DECIDED
   2026-08-10 — the F100 hold is LIFTED and the repair is the reason-string
   fix ONLY** (the log line stops crying wolf; the preflight target stays as
   is until D12's own review settles). Queued with the C43 TestKit fix into
   the next unattended chain, which verifies both against a live boot.
   → `agent/bugs/F100.md`.

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

1. **PT-62's remainder** (→ Colonists & domes) — D12's only gate, ⛔ NOT a
   release gate (opt-in; owner, 2026-08-03). ✅ P4/P6 PASSED 2026-08-03 (dome
   23 → 0, overpop cleared); still owed: **P12 · P13 · P14 + the landing
   check** — the PT-62 block is the truth, this line is its summary.
   *(Queue line re-synced 2026-08-11 by a doc sweep — it had frozen the
   pre-08-03 remainder while the block below moved on.)*
2. ✅✅ **The load-heal round-trip sweep — CLOSED 2026-08-12 by your call.**
   Both legs ran and passed (unattended, 2026-08-04: D1 natural-state ×3 loads
   clean, D2 forced-defect heals fire once and hold; details annotated below).
   You ruled D1+D2 close it: everything sampleable passed in both directions,
   the unsampled families (H1 astro — wrong commander; H3 biorobots — none on
   the save; H2/H4 deliberately unforced) stay recorded as unsampled, never
   clean, and return as their own findings if one ever misbehaves organically.
   Nothing further owed.
   *(Original ask, kept for the annotations that follow:)* save, reload twice, read the
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

### Rider — C42: does a passage traversal leave a stale passenger behind? · Status: unrun — **TAKEABLE WHEN** any colony has a built Passage that colonists actually walk through · ⭐ mechanism link CLOSED 2026-08-04 · ⚠️ 2026-08-05: a WITHIN-SESSION read finally ran (no save/load since traffic) and was STILL unsampled — 0 unit entries over 4 passages; the gap now needs a **traversal witness** (a colonist seen inside a passage element), not merely generated traffic · ⛔ 2026-08-10: the dedicated witness poller ran (`corun-batch-2` prep) — **90 tries × 1 s at speed 20, `units` empty every sweep** — so THIS save cannot sample it; the TAKEABLE-WHEN condition is now "a colony where passages are demonstrably a colonist route", and no zero from `TEST2H TRAIN` may be quoted against the entry (C42 entry, 2026-08-10)
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

### Rider — F99: re-read the track residue BEFORE a reload · Status: **unrun — the rig RAN the recipe 2026-08-04 and the rider's own precondition never arose; ⚠️ 2026-08-05 added TWO MORE witnessed attempts (meteor repairs on one track, 201 new-build sites across three tracks with the merge confirmed) and `TrackElement.lua:805` did not fire in either, so the gate still never opened — three attempts, zero throws, rate bounds only; ⭐ 2026-08-10 a FOURTH witnessed zero (`corun-batch-2` leg Q — the 2×2's last empty cell: repair sites on 2 DISTINCT tracks completed together, sites 2→0, residue read `0 0` before any save/load) — the `:805` gate has still never opened** · **mode: unattended, STAGEABLE** (routing 2026-08-04 — the rig stages break + cheat + pre-reload read deliberately; owner-rule chain applies: Opus runs, Fable audits. The old TAKEABLE-WHEN framing — wait for a sitting to happen to use the cheat — is superseded)
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

### Rider — C39: Service Automation and the four Workshops · Status: ✅ **RUN 2026-08-11 (corun-pt15 sitting) — ANSWERED**
**Bug:** the law halves staffing by LABEL while its performance compensation
keys on CLASS; the four Workshops sit on the wrong side of that line. The sign
of the harm was genuinely unclear — this was a keyboard observation, not more
reading. → [C39](agent/bugs/C39.md)

⭐⭐ **RESULT: the Workshops are MISSING AN UPLIFT, not taking a penalty.** With
the game **paused** (both readings at the same game instant, so drift cannot
explain it), your TV Studio Workshop and a Diner in the same dome **both** took
the identical −50% staffing cut — and only the Diner was paid back for it:

| | before | law on | after revert |
|---|---|---|---|
| **Workshop** performance | 127 | **131** | 129 |
| **Workshop** workers/shift | 12 | **6** | 12 |
| **Diner** performance | 114 | **268** | 124 |
| **Diner** workers/shift | 2 | **1** | 2 |

The Diner's **114 → 268 → 124** reverses when the law is deactivated, which is
what makes it a measurement rather than a coincidence. Your words, kept in the
record: *"more than double when I reverted it dropped to 124 for the dinner."*
⇒ those four buildings lose ~half their output whenever Service Automation
passes.

⚖️ **YOUR CALL — nothing is built.** The chain's scope fence makes C39 an
observation only; if you want a repair, that is a new decision. Severity is also
open: it needs a late-game Technology policy (SortKey 900, 10th of 11) to be
voted through before it can bite anyone.
⛔ **Honest limit:** only **one** of the four Workshops (`TVStudioWorkshopCCP1`)
existed in the colony. The other three share the same class chain so the same
result is expected — but it is inferred for them, not measured.

---

# Mysteries

> ✅✅ **PT-15 RAN 2026-08-11 (`corun-pt15` attended co-run) and moved WHOLE to
> `archive/PLAYTEST_ARCHIVE.md`, audit-sustained the same day.** F07 is
> **`tested`** — your trap's 95 wisps produced 95 power (43% of the grid, ~47
> Solar Panels' worth; vanilla would have given 0.095), it survived save/reload,
> and your verdict is on the entry verbatim. F15's double-grant half is
> MEASURED gone on the same trapful. Kept saves (NOT strays — do not delete):
> **`CP15PT15.savegame.sav`** and **`CP15F15.savegame.sav`**. The two decisions
> the sitting raised (C39 repair, C46) are in "Decisions waiting on you".

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

### PT-35 — Save sanitizer does no harm (F35, F03) · Status: **case A COMPLETE 2026-08-11 (mechanism grade — not `tested`); B/C parked** *(status token corrected by the unattended-2 audit; it still read "unrun" beside the completion record below)* — ⭐ case A RAN unattended 2026-08-04: do-no-harm half PASSES, turbine half UNSAMPLED (fixture gap, see below) · ✅✅ **THE FIXTURE GAP IS CLOSED 2026-08-10** — `PT35FIXTURE.savegame.sav` is in your save folder (`corun-batch-2` leg S): FrictionlessComposites researched, **one Large Wind Turbine**, **one applied building upgrade** (Remote Medic on a Hospital, for the F03 half). **The turbine-half re-run is now an unblocked 2-prompt unattended chain** — nothing of yours needed. ⛔ Do not delete that save · **mode: UNATTENDED** (routing 2026-08-04 — all reads numeric + save/reload; owner-rule chain: Opus runs, Fable audits) · ✅✅ **CASE A IS COMPLETE 2026-08-11 (`unattended-2`, re-run after the pack was re-enabled): BOTH halves sampled on a real population for the first time. Three loads, two save+reload round trips, six pass calls, and **0 of 14 readings changed at every single comparison including start-to-finish**. `RepairTurbineBuff`'s zero is no longer the trivially-forced early return — the tech IS researched, so the pass walked its whole body and its already-buffed guard did the skipping; `RepairLeakedUpgradeModifiers` returned 0 with **3 live upgrade-shaped modifier ids and 144 upgraded buildings** in front of it. 0 `[LUA ERROR]` in the whole log. ⛔ Still not `tested` — unattended ceiling is MECHANISM — and cases B/C stay parked.** → `agent/bugs/F35.md`, log `archive/u2run3_Mars.exe-20260811-02.01.06.log`
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

### ~~PT-60 — The chain-8b batch leg (F90-F96 + eight conversions)~~ ✅ **RUN 2026-08-12 (`corun-pt60` co-run) — all nine predictions resolved, audit sustained.** Moved WHOLE to `archive/PLAYTEST_ARCHIVE.md` (results banner + the pre-run spec + this tracker). Highlights: the P8 decider taken on your `USA Sol 302` copy (heal fired once, zero on reload, effect persisted); suite 77/0/10/0 with every SKIP matched by name; 0 errors in the whole log; F48 repaired 3 of 7 tracks in your campaign and the repair stuck; F34(d) re-derived on your challenges and observed reachable 20/20. Your original save byte-verified untouched. Decisions that came out of it: items 12 and 13 above.

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

### PT-20 — Uninstall safety · Status: standing — re-run per era and before release · ⛔ **2026-08-10: a Mod-Manager disable does NOT take effect until a FULL game restart** (D13, measured) — the prior 98-vs-98 comparison may have sampled the mixed state · ⭐ **REDO ORDERED (your decision 6, 2026-08-10): a dedicated redo co-run is QUEUED** — disable click + full restart + ~10 min play are yours, everything else rig-side; its result supersedes the old comparison · **mode: co-run** (routing 2026-08-04 — you keep the disable click + the 10 min play; save/reload/log reads rig-side)
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

### Rider — §3.6 corner (optional): the sol-change autosave under a popup · Status: unrun — was M3 in `corun-batch-2` (2026-08-10) and was NOT reached (no sol boundary came near); ⭐ **now the interesting popup half**: F85's route refutation makes this the one popup that does NOT pause, i.e. the only place a vanilla autosave can reach a save under a popup with no rebind involved (F85 entry, 2026-08-10) · **mode: co-run ride-along** (routing 2026-08-04)
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
