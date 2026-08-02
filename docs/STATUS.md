# Project Status — read this first in a new session

> 🔗 **THE PROJECT PROMPT CHAIN (2026-08-01, owner direction) —
> `docs/prompts/project/`.** All pending project work between the bug-list
> audit and the F86 adjudication now runs as a numbered, self-consuming
> prompt chain (13 prompts, model routing in the filenames, mechanics in the
> folder's README): harness gate → playtest reorg → F86 Phases 0-4 → audit
> candidate sweeps/decisions → D10 → D12 → F76 → final backward QA. **Run in
> filename order; each prompt hands notes forward and deletes itself; when
> the folder is empty the owner is free for the playtest campaign.**
> `FABLE_NEXT_PROMPT.md` was rewritten the same day as a PURE playtest-standby
> prompt and no longer carries the board — chain-owned work found in a
> playtest session is routed to the chain, never started there. The spent
> `F86_NEXT_SESSION_PROMPT.md` and `F86_ADJUDICATION_FOLLOWUP.md` are
> archived. All six research-mod FPKs (incl. the removed fredware mod) are
> archived at `C:\Dev\workshop_fpk_archive\` — workshop subscriptions are no
> longer needed for any planned work.

Rewritten in place every session (structure since 2026-07-29, audit
remediation 3.3). Session legs are append-only in
`docs/archive/SESSION_LOG.md` (newest first); engine facts live in
`docs/agent/ENGINE_FACTS.md`; defect truth lives in `docs/BUGS.md`.

> 🚧 **TWO PROMPTS since 2026-07-31 (owner).** `docs/prompts/FABLE_NEXT_PROMPT.md` is the
> **general** prompt and no longer drives drone work — it may answer drone
> questions but may not start, plan or schedule that work.
> **`docs/prompts/DRONE_PROJECT_PROMPT.md`** owns it: D06, D08, D09, F77, the drone queue
> machinery, the consolidated drone playtest, and the cleanup mod. Reason: the
> drone project grew its own open design decision, its own frozen tests, and
> constraints that do not generalise, and sharing a prompt was degrading both.

**Build state (authoritative counts — stated here and nowhere else):**
`Code/` = **75 files** (66 `Fix_` + 7 `Opt_` + `00_Core` +
`90_SaveSanitizer`) = **74 registered modules, 68 default-active** (the 6
toggle `Opt_` modules are opt-in via Mod Options; `Opt_DroneStatDials` (D09)
registers active but is byte-vanilla until a dial leaves base). Pinned game
build: **1.0.7.396349** (fpk parity proven — ENGINE_FACTS.md). BUGS.md index:
**100 rows** (88 `F` + 12 `D`; **recounted 2026-08-01** — the "98 (87 F + 11 D)"
recorded on 2026-07-31 went stale within the same day, when F88 and D13 were
filed after that count was taken; the count before it, "93", had gone stale the
same way), **plus 34 `C` candidate rows** (was 11 — the
2026-08-01 bug-list audit filed C12–C31, and its same-day packed-source
addendum filed C32–C34; C rows are leads, not defects, and are not counted in
the 100). **TestKit probes: 78** (re-verified 2026-08-01 by counting
`SMRTest.Register(` across the TestKit's nine probe files: 10+20+18+12+7+3+2+6,
excluding the definition in `00_TestCore.lua`; **unchanged by the 2026-08-01
teardown of `97_SaveHookProbe` — it was declared, never registered**, and the
stale-probe sweep now returns **zero** hits in both repos). **74 registered
modules** likewise re-verified
(75 `SMRFixPack.Register(` occurrences minus the definition in `00_Core.lua`).
Counts moved 2026-07-31 with **PHASE 4 COMPLETE** (below).
> ⭐ **2026-07-31 (live sitting) — ALL FOUR DRONE RESEARCH GATES ARE ANSWERED and
> F83 is `tested`.** Nothing on the drone research side is owed. Full leg in
> `docs/archive/SESSION_LOG.md`; the answers live on the **D06 entry** and in
> `docs/reports/DRONE_PRIORITY_SYSTEM.md` §8-§10.
> - **Q1 = HONOURED, both legs** — a band-4 repair AND a band-4 haul were
>   consumed, the second on a cheat-free symmetric pair. The band scheme
>   survived the gate that could have killed it.
> - **Q2 = queues are PERSISTED** — allocated in `TaskRequestHub:Init()` at
>   construction, never on load. Learned by breaking a live save (§8).
> - **Q3** — both data tests settled with exact enumerations (5 life-support
>   producers; 4 food services). **Q4** — defaults are omitted from saves,
>   live-confirmed on both branches.
>
> ⚠️ **But the band scheme picked up TWO constraints that did not exist when it
> was drafted, and NO SIDE HAS BEEN PICKED — that is a design decision owed to a
> fresh session.** §9: uninstall is safe and silent but **lossy**, and the heal
> path **expires** once the map is fully scanned. §10: `DroneControl:RemoveBuilding`
> is bounded by a **file-local pinned at 3**, so every re-registration duplicates
> band-4/5 entries **with the mod installed and working**. The `-1..3` fallback
> now has two independent arguments in its favour.
>
> 🆕 **A NEW ENGINE FACT WITH PACK-WIDE REACH** (ENGINE_FACTS.md): a
> mod-authored closure stored on a **persisted game object** goes into the save,
> **survives uninstall, and keeps running** — measured, with zero errors logged.
> 5 of 6 `= function` sites in `Code/` are cleared (UI windows, class tables);
> **`Fix_MeteorFrequency` is UNRESOLVED**, and **PT-20 now carries a mandatory
> step 5** that names it. "It does not break" is no longer a sufficient PT-20
> pass.
>
> 💡 **THE CLEANUP MOD** (D06 entry) — owner frames it as a **beta response
> channel**. **Not approved to build**; owed with the overhaul, not with launch.
> ⚠️ **Its stated justification was corrected 2026-07-31:** the claim that mods
> get *no save hook at all* is **false** — `OnMsg.SaveGameStart` /
> `SaveGameDone` reach mods (measured; only `PersistSave`/`PersistLoad`/
> `PersistGatherPermanents` are blacklisted). A tear-down-on-save scheme is
> implementable after all. What survives is that no mod can run after its own
> removal, so residue *already inside a player's saves* still needs someone else
> to clean it.

> ⭐ **2026-08-01 — THE BUG-LIST AUDIT RAN (`docs/reports/BUG_LIST_AUDIT.md`,
> game-free, one-off prompt consumed).** Every shipped fix tiered against
> external witnesses: final **16 GOLD / 25 SILVER / 30 BRONZE / 0 HOLD**
> (initial 17/25/29/1; F04 fell to the §9 packed-source read, and F49(a)'s
> brief HOLD was reclassified on owner challenge — it is a high-confidence
> adjudicated R4, which fails HOLD's lacks-confidence definition); **the HOLD
> tier ends the audit EMPTY**, and a **NON-FIX tier (12 items) was formalized
> at the owner's direction** (audit §2.4) so hard we-are-not-fixing-this
> decisions (R4 / tier-I / §4a-barred / owner-declined) never muddy the
> maybe-BRONZEs — checked: nothing in BRONZE belongs there; the latent R3s
> ship deliberately per §4a. **And the tier's one code wrinkle is CLOSED
> (owner direction, same day): the F49(a) no-op guard was STRIPPED from
> `Fix_TrainMinors`** — wrapper + 3 Require entries + the probe's palette
> half (probe retained, cap-only; count stays 78; its PASS text changed —
> expect that one line in the next fingerprint diff). Counts unchanged
> (74 registered / 68 default-active). ✅ **The owed unattended A/B code-gate
> leg RAN CLEAR 2026-08-01** (default config; log
> `Mars.exe-20260801-14.15.08`): `fix pack present: 68/74 fixes active` ·
> `---- 63 PASS, 0 FAIL, 15 SKIP, 0 ERROR ----` · 78 verdict lines · zero
> `[CommunityFixPack]` error/disabled/FAILED lines · the predicted ONE
> fingerprint change (TrainMinors now `train cap recomputed 4->1, 40->2, 0->0`)
> plus the two known RNG lines · documented noise only. **Nothing is owed on
> the harness side.** Full quoted numbers on the F49 entry. Headlines: a native Relaunched fix-modding scene exists and
> independently converges on F01/F04/F71/F74/F78/F81 (fredware's 13-fix "Bug
> Fixes" created 2026-07-31, GromGor, Oxygenus); the Relaunched dev patch-note
> thread witnesses the train/lander/homeless clusters wholesale; **20 gap
> candidates filed as C12–C31** (6 VERIFIED against Src this audit — incl.
> Fhtagn cowards-everyone and two storybits that promise rewards they never
> apply); **`Lua.hpk` extraction: needed by ZERO entries — recommend not
> building it**. Corrections en route: F42's stale index row fixed; F34's
> claimed ChoGGi corroboration falls; F35's witness may out-scope the fix
> (work item); F01's recorded forum-report claim is not re-derivable
> (Paradox forum crawler-blocked). **Owner actions requested (audit §7.1):**
> logged-in Paradox subforum check (F01/F64/F74 reports), Paradox Mods
> browser check (console channel, matters for D13), ~~consider subscribing to
> GromGor's + fredware's mods for source comparison~~ — **DONE same day: the
> owner subscribed, all six FPKs (including fredware's REMOVED "Bug Fixes")
> were extracted and read (audit §9).** Results: **F04 GOLD→BRONZE** (its
> witness fits the newly-filed C32 label-desync better), final verdict
> **16 GOLD / 25 SILVER / 30 BRONZE / 0 HOLD**; C31 resolved (F78-heal, not a
> new mechanism); C04 mechanism confirmed vs Src; C22/C23/C24 VERIFIED vs Src
> (Saint blessing never worked; 3 dust-devil scheduler defects; asteroid-visit
> precedence bug); **C33 filed — whole-track demolition leaks an undeletable
> TrackBase shell AND OUR OWN F44 PATH REPRODUCES IT** (needs an F-row
> decision); C34 filed (stale-active rain state, F81b's sibling). fredware's
> F74 misses refugee rockets (ours is a superset); his disasters fix never
> restarts the wedged scheduler (ours does); nothing in his source explains
> the Workshop removal.

> ✅ **2026-08-01 — CHAIN PROMPT 1 DRAINED (playtest reorg + the §4 amendment +
> the consistency sweep; game-free, prompt consumed).** Five things changed:
> - **`FIX_POLICY.md` §4 is AMENDED AND IN FORCE** — the reachability audit's
>   drafted replacement applied verbatim (intent-first with five hard tells ·
>   per-tier reachability with symmetry of proof · R1-R4/U dispositions ·
>   tested-by-playing · evidence freshness). Authority: the owner's blanket
>   pre-clearance; the blocker died when F49(a)'s guard was stripped. **Every
>   session from here judges fixes by the amended §4, not the old
>   three-sentence rule.** ⚠️ **One decision it activated is OWED and routed to
>   chain prompt 7:** F29 (items 1+3) and F57(a) are R3 latent-by-data shipped
>   as §1.5 replacements — the combination the new R3 bullet makes conditional
>   on an explicit owner decision. Nothing presumed; both entries carry it.
> - **PT-54 is RETIRED UNRUN** — it tested bodies the F86 Tier-1 build deletes
>   and reorders. Triggers C/D/E ride the Tier-1 legs (prompt 4 records them as
>   the retirement made good); **triggers A and B are NOT absorbed** (they test
>   `Fix_DisasterPredictionLeak`, which is in no tier) and were routed to
>   prompt 3 to be written into the build prompt as legs. Full text preserved
>   in `PLAYTEST_ARCHIVE.md` under a RETIRED-UNRUN banner.
> - **The needs-eyes list gained four bug-list-audit riders** (F35 live-label,
>   C32 label-membership, F80 enumeration tap, F82 timing) and lost one: **F74
>   merged into F53(a)**, its question answered twice from outside.
>   **⬇️ THREE REMAIN as of 2026-08-01 evening: the F35 live-label rider was
>   TAKEN AND CLOSED** during the F86 Phase-0 keyboard sitting — exactly the
>   opportunistic capture it was written for. **The live label path works, all
>   three turbine labels including `WindTurbine_Large` (+100% applied, Power
>   doubled on every turbine), from a pre-research save with no reload** — so the
>   audit's suspicion that F35 is aimed one layer too shallow is dead and F35 is
>   the old-save migration failure it was filed as. Evidence and the
>   wrong-tech trap that nearly mis-filed it: BUGS.md F35; prompt 6's job 3 is
>   pre-answered and told not to re-run it. The list is
>   now split by intake, because two of the new rows check whether something we
>   believe is *incomplete*, which is not what the other two tables mean.
> - **`MOD_DESCRIPTION.md`** gained the documented-engine-behaviour paragraph
>   and a conditional, do-not-publish-yet no-precedent claim tied to prompt 4.
> - **The consistency sweep found four divergences** beyond the F42 row the
>   audit had already caught (F18's stale `fixed*`, F86's stale *heading*,
>   D01's missing tag, plus vocabulary drift on F84/F88/F10/D06). All 100 index
>   rows now agree with their heading tags, and the comparison is mechanical.
>   **Counts re-derived from the files, not inherited:** 100 index rows
>   (88 F + 12 D) — the 2026-07-31 "98" had gone stale within its own day.

> ✅ **F86 TIER 1 IS BUILT AND VERIFIED (2026-08-01, chain prompts 4 + 4b) —
> ALL FOUR BUILD UNITS LANDED AND ALL FIVE LEGS HAVE RUN** (owner at the
> keyboard, one game sitting plus the uninstall sitting). Save lineage
> `save_game_id HdmSxGs6kyd0uz6-` (test-2, map BlankBigCanyonCMix_09); logs
> `Mars.exe-20260801-16.42.31` (first load), `-17.11.08` (main sitting),
> `-19.14.11` (uninstall). **F02, F78, F81 and F88 are flipped to `tested` on
> that evidence** (index rows and heading tags both), and C34's rider is
> verified. What shipped:
> - **`Fix_MeteorFrequency` REWRITTEN (§6.2a-A):** layer-3 keyed
>   `GetDisasterWarningTime` wrapper over VANILLA's thread body; the body copy
>   and its heartbeat surface are deleted; the per-load restart (F88's defect)
>   replaced by a one-shot version-latched heal (`SMRFixPack_MeteorLatch`
>   GameVar + new core helper `SMRFixPack.PackVersion()`); watchdog liveness
>   moved onto an additive `OnMsg.MeteorDone` timestamp, threshold/ladder/
>   guards unchanged, restarts recreate vanilla's body.
> - **`Fix_RainsDeadlock` REWRITTEN (§6.2a-B):** the bounded-loop copy is
>   deleted; a layer-2 wrapper on `RainsDisasterActivation` mirrors the
>   collision test BEFORE the call and posts `Msg("RainDisasterEnd")` on the
>   early-return; the version-stamped PostLoadGame migration pass
>   (`SMRFixPack.MigrateRainsState`, `SMRFixPack_loop_version`, id-less
>   entries resolved by unique type) moves every persisted loop onto vanilla's
>   body and **carries the C34 rider** (structure → stale-ACTIVE
>   `FinishRainProcedure` heal → migration; manual fallback for invalid
>   `g_RainDisaster`).
> - **`Fix_DisasterPredictionLeak` rider (§6.2a-C):** the stranded-flag sweep
>   also runs on `OnMsg.NewDay` (the taken mid-session reconcile) — Tier-1 leg
>   4's A/B triggers test it in their changed shape.
> - **`SMRFixPack.StormWedgeHeal` REORDERED (§6.2a-D):** orphan gate at body
>   start and after every Sleep, vanilla-state resets before any mod-name
>   touch, logging last — the pack's one mod-owned GT thread in Tier-1 scope
>   is now §3a gate-compliant.
> - **TestKit probes realigned, count stays 78:** the F02 probe drives the
>   keyed wrapper + `wd.last_seen` watchdog (heartbeat surface is gone); the
>   RainsDeadlock probe drives the collision Msg, the version-stamped
>   migration (incl. the id-less `test 2i` shape) and the C34 heal;
>   FixtureCarry's version-lock warning is RESOLVED (the migration is
>   version-stamped) and `SMRFixPack_MeteorLatch` joins its GameVar list.
> - **F89 filed mid-sitting (2026-08-01, leg 1):** vanilla's `MeteorsDisaster`
>   drain loop wedges the Meteors thread on ORDINARY strikes (F78's class on
>   the singles path, invisible to the storm watchdog); measured live at 192h
>   silence and healed by the F02 watchdog at its threshold — the insurance
>   the spec kept proved itself. Covered, not fixable directly (entry).
>   **Index rows now 101 (89 F + 12 D).**
>
> **What the legs actually read (2026-08-01):**
> - **Leg 1 — cadence + warning timing.** Scheduler gaps 75h, 83h, 72h (plus
>   86.7h around the natural storm), all inside the designed 65–90h roll.
>   Storm-warning timing UNCHANGED, proven three independent ways: probe
>   keyed/unkeyed discrimination; a live `GetDisasterWarningTime` read from a
>   non-Meteors thread returning **2250000** (the tower cap, not the keyed
>   2700000); and the natural storm's UI countdown reading ≈74h. **Both**
>   §6.2a-D heal branches ran live on the reordered body — the release branch
>   on a forced storm and the force-clean branch on the scheduler's own
>   natural storm — with logging last in both, exactly as specced. Storms are
>   2-for-2 wedging in this colony, so F78's repro is robust.
> - **Leg 2 — F88's own repro as its regression test.** `t=216351730` →
>   quicksave → **three loads with zero pack lines** → `t=218608231
>   (+2256501 ms = 75 game hours)`. The meteor arrived on the pre-load
>   deadline; the per-load re-roll is gone.
> - **Leg 3 — rains.** The collision arrived NATURALLY (re-roll posted, rain
>   returned; a second one later), `'normal'` migrated and stamped 1.0.1 with
>   no re-migration on later loads, `toxic` correctly silent per the amended
>   id-less reading (`70e6d0c`), and the C34 stale-ACTIVE plant healed through
>   vanilla `FinishRainProcedure`.
> - **Leg 4 — stranded flags, both halves.** A stranded flag cleared on a
>   NewDay tick with NO reload *and* inside a load block; a genuine live
>   countdown survived both sweeps (reload and sol tick) with its flag intact.
> - **Leg 5 — uninstall (PT-20 method).** With the pack disabled: `Meteors`
>   and `MeteorStorm` threads both `valid=true` on vanilla bodies, **zero
>   lines and zero errors naming any Tier-1 module**, and residue only from
>   the allowed list — `SMRFixPack_MeteorLatch = (absent)` (below budget) and
>   inert `loop_version` fields in vanilla's own `RainsDisasterThreads`. F86
>   **Site 1's harm no longer happens**: removing the pack no longer kills the
>   colony's meteors.
>
> ⚠️ **Two limits leg 5 did NOT clear, recorded rather than glossed:**
> (1) **F86 Site 2 is untouched and still leaks** — the uninstall log carries
> **80** `[LUA ERROR] Opt_DroneOverhaul.lua:96` orphan errors, the same
> `(96)←(190)←sprocall←CommandObject.lua(246)` shape BUGS.md already records
> at 98/session. New this leg: they are confined to the FIRST load and are
> **zero after a save+reload** — the leak self-clears in one load. That site
> is layer-2/Tier-2 work and belongs to chain prompt 5, where its carve-out is
> pre-granted; it is **not** a Tier-1 falsification and did not gate the flips.
> (2) **No meteor cycle was instrumented in the uninstalled state** — the
> meteor logger is a per-session toggle and the game restart cleared it. The
> owner saw a warning with no strike behind it, which is ordinary vanilla F89
> with no watchdog to heal it. The uninstall claim rests on the thread/body
> read and the zero-error log, not on that observation. FixtureCarry also
> reports label modifiers as `NOT INSPECTABLE` — absence there is not evidence
> of absence.
>
> - ~~**Tier 2 still owes** (chain prompt 5): `DroneUnreachableForever`,
>   `TrainWaitTime`, `ArrivalDeaths` (b) + the (a) design pass, **F86 Site 2
>   (`Opt_DroneOverhaul`)**, and the D10/D12 unhold record.~~ **→ BUILT
>   2026-08-01, see the Tier-2 block immediately below.** The §5.4-A
>   conversions are chain prompt 8. Tier 1 verifying does not by itself make
>   the pack uninstall-clean.
>

> ⭐ **F86 TIER 2 IS BUILT — 2026-08-01, chain prompt 5 (`88f3154`, `44e6af2`,
> `6f0cb95`, `ef7d49c`; TestKit `6eb3c0b`, `7bfa274`). ⚠️ NOT YET VERIFIED — the
> one leg for the tier is specced and UNRUN (`PLAYTEST_CHECKLIST.md` PT-58,
> predictions P1-P7 written before the run). The D10/D12 unhold is therefore NOT
> recorded: its gate is "repairs land AND verify", and only half of that is true.**
> Chain prompt **5b** carries the leg, the unhold and the outbox.
>
> **All four Tier-2 modules now sit on synchronous seams; none replaces a blocking
> body any more. Per-site dispositions (FIX_POLICY §3a per-site release gate):**
>
> | site | was | now | disposition |
> |---|---|---|---|
> | `Fix_DroneUnreachableForever` | replaced `Drone:ApproachWrapper` (blocks in `DroneApproach`, our code after the call) | pre-wrapper on the **verified-synchronous** `Drone:CleanUnreachables` — `ts > GameTime()` → `ts - max_int` recovers the exact failure time; vanilla's writer and its 5-sol expiry both untouched | **REPAIRED IN-PACK, layer 3. No residue; nothing owed to D13.** |
> | `Fix_TrainWaitTime` | replaced `Colonist:BoardVehicle` (blocks for the whole journey via `PlayPrg`) | wrapper on the **verified-synchronous** `TransportStatistics:AddSpentTime`, keyed `IsKindOf(self,"Station")` — the only Station call site of three, and vanilla's own "the wait is paid" line. Boarding colonist identified by `command_thread == CurrentThread()` | **REPAIRED IN-PACK, layer 3. No residue.** |
> | `Fix_ArrivalDeaths` (a) | inside the replaced `Colonist:Arrive`, in a destructor after a `Sleep`, on an upvalue nothing could change | pre-wrapper on the **verified-synchronous** `Colonist:OnArrival`, which runs after the placement and (on the walking path) before `TransportByFoot` starts. **This is the design pass §6.2 booked as owed — run, and it found a route** | **REPAIRED IN-PACK, layer 3. No residue.** |
> | `Fix_ArrivalDeaths` (b) | same replaced body; destination read into a local at `:1260` before anything else runs | pre-wrapper on `Colonist:Idle` keyed on `self.arriving` — the only issuer of `"Arrive"`. Work before the call, `return orig_idle(...)` with nothing after | **REPAIRED IN-PACK, layer 2. Accepted residual: one inert captured frame — ethos tier 2, named and disclosed. Nothing owed to D13.** |
> | `Opt_DroneOverhaul` — **F86 Site 2** | post-wrapper on `Drone:Idle`, under three `Sleep`s: **80 orphan errors** on the Tier-1 uninstall leg, 98 when first measured | post-wrapper on `Drone:CleanUnreachables` gated `self.command == "Idle"` — vanilla's own last statement in the same fall-through, with **no statement between it and the end of `Idle`**. Beats the layer 2 the spec asked for | **REPAIRED IN-PACK, layer 3. No residue.** Verification = PT-58 P5. |
>
> **Carve-out honoured, not stretched:** the `Opt_DroneOverhaul` move changed the
> hook's call position and nothing else — same trigger condition, same ordering,
> same code — so no drone-design judgement was required and the pre-granted
> clearance covered it exactly. Part 1's `TaskRequestHub:FindTask` wrapper was
> checked in the same pass and is already on a synchronous C-backed seam, so the
> module now has **no capturable frame anywhere**.
>
> **Two records were corrected rather than quietly dropped:** `Opt_DroneOverhaul`'s
> header claimed *"saves made with the module enabled load identically without
> it"* — false, and Site 2 is the counter-example; and F53's entry claimed *"no
> wrapper can run in time"* for F21 — right about `BoardVehicle`, wrong about the
> repair, because it only ever asked whether that one body could be wrapped.
>
> **F21 was DOWNGRADED `tested` → `fixed`** in the same move: PT-43's pass was read
> against a body that no longer ships. PT-58 carries the optional re-take that
> earns the tag back; the probe alone does not.
>
> **`ChooseDome` was deliberately NOT wrapped**, though it is where F53's bad
> fallback is born: eight shipped call sites, only the arrival ones are F53's
> subject, and suppressing the fallback globally would change android spawning and
> the "Abandoned" path — behaviour with no evidence behind it (FIX_POLICY §4), and
> §5.3 requires the narrowest key that separates the sites.
>
> **Probe hygiene:** sweep **CLEAN** (zero `TEMPORARY` hits, both repos) at
> `ef7d49c`. Three probes asserted behaviour the pack no longer replaces and were
> **realigned onto the new seams** before any leg was specced — `ArrivalDeaths`
> and `DroneUnreachableForever` (TestKit `7bfa274`), `TrainWaitTime` (`6eb3c0b`).
>
> ⭐ **ETHOS + RELEASE GATE RESTATED BY THE OWNER 2026-08-01 (authoritative
> text: `FIX_POLICY.md` §3a — any "leave no trace" framing left elsewhere in
> the docs is superseded by it).** Leftovers are an accepted fact of this
> engine — the game's own code spells the mechanism out — so the ethos is
> three-tier: **(1)** leave no trace; **(2)** failing that, leave **inert**
> trace, named and disclosed; **(3)** failing that, leave harmful trace **only
> paired with its remedy**, the D13 cleaner. **The release gate is now
> PER-SITE, not blanket:** every exposed site needs a recorded disposition
> (repaired in-pack, or handed to the cleaner where no layer 3/2 route exists).
> A site without a disposition blocks release; a site with one does not.
> ⛔ **This is not permission to descope — build every reachable repair NOW.**
> A cleaner hand-off counts only *after* the in-pack attempt failed, because
> D13's target list is the OUTPUT of the builds and cannot be designed before
> them. **D13 is a HARD LAUNCH DEPENDENCY: launch waits for it, it does not
> wait for launch.**
>
> ⚠️ **DO NOT TRUST ANY EXPOSED-SET COUNT IN THESE DOCS — including the ones
> in this file.** Every recorded figure is an **open lower bound** ("at least
> 13", "≥13"), it moved 12→13 within a single day with the membership
> corrected *both* ways, the enumeration grep behind it is known blind to
> slot/global/preset assignments, and Tiers 1-2 have since changed the set by
> repairing modules. Several per-module tables still carry a stale **12**
> denominator. **D13 derives the set itself from source and that derivation is
> authoritative**, superseding every number recorded anywhere; it then updates
> all of them (the locations are listed on the D13 entry in `BUGS.md`).

> ✅ **F86 PHASE 0 IS DONE (2026-08-01, owner at the keyboard, one sitting) —
> the two engine measurements that gated the Tier-1 designs are MEASURED, and
> both came back the permissive way.** Log
> `Mars.exe-20260801-14.59.57-6a22b86d.log`; full records in ENGINE_FACTS.
> - **`CreateGameTimeThread` DEFERS** — the body does not run before the creating
>   statement continues. Measured twice, the second form creating the GT thread
>   *from a GT thread* and confirming a live `WaitMsg` receipt (the actual vanilla
>   shape), so the answer is not an inference off the console-context form.
>   **→ the authorised rains wrapper works as written; the synchronous-heal
>   fallback is NOT needed.** F02's defer-when-falsy guard turns out not to be
>   load-bearing and is kept only as defence in depth.
> - **The pre-save hook COVERS AUTOSAVES** — `SaveGameStart`/`SaveGameDone` with
>   `autosave=true err=false`, twice, positive control `LoadGame FIRED` present.
>   Both autosaves were console-forced through the engine's own `Autosave` entry
>   point (`CreateRealTimeThread(Autosave)` — literally what
>   `Savegame.lua:1550-1555` does); no naturally-timed autosave was observed.
> - `97_SaveHookProbe.lua` torn down in the recording commit; **the stale-probe
>   sweep now returns zero hits in both repos.**
> Phase 1 (chain prompt 3) is unblocked and inherits the wrapper shape.

> ⚖️ **F86 STATE AS OF 2026-07-31 EVENING — the block below is the original
> filing and parts of it are SUPERSEDED. Current truth:** the design was
> **adjudicated twice** (`F86_ADJUDICATION.md` — yes-with-changes) and a
> **prior-art survey ran** (`PRIOR_ART_SURVEY.md`). Corrections that override
> the text below: capture is **value-reachability**, not frame position ("an
> empty `_ENV`" is WRONG — orphans resolve vanilla globals and lose only
> mod-created names, measured); "synchronous can never be captured" holds for
> the **thread-stack route only** (exposed set is **≥13**, incl. the compliant
> `Fix_CaveInsNoDisasters`); F02's hold is LIFTED and the build is authorised
> (Tiers 1+2, layer 1 gated); the sweep is DONE; **F88 filed** (the per-load
> restart). **Plan of record: `F86_EXECUTION_PLAN.md`; next session:
> ~~`F86_NEXT_SESSION_PROMPT.md`~~ **→ since 2026-08-01 the numbered chain in
> `docs/prompts/project/` (prompts 2-3 carry the split + the audit's C34
> rider; the original is archived).**
> Owner directives of the evening: orphan-gate rule (FIX_POLICY §3a), latched
> heal, and the **prelaunch save-exit deliverables** (uninstall procedure +
> standalone cleaner — WORKFLOW release gates).
> **PHASE 0 MEASURED + PHASE 1 DONE (2026-08-01, chain prompts 2-3):** GT
> creation DEFERS and the autosave hook FIRES (ENGINE_FACTS); the **final
> Tier-1 spec is `SAVE_SAFETY_REDESIGN.md` §6.2a** (rains wrapper shape final,
> C34 rider riding the rains pass, F81a mid-session NewDay reconcile taken,
> StormWedgeHeal orphan-gate reorder specced); the five-shape enumeration
> re-derived the durable exposed list at **13, plus one inert route-(c) site**
> (`Fix_LastTransmissionStorage`, adjudication §4.4 CLOSED — no build); the
> build prompt was `F86_TIER1_BUILD_PROMPT.md` (chain prompt 4 ran it;
> **consumed 2026-08-01 once Tier 1 was built and verified** — see the
> post-Tier-1 block higher up this file for what the legs read).
>
> 🛑 **PT-20 FAILED 2026-07-31 — WE HAVE A P1 DEFECT OF OUR OWN, AND IT BLOCKS
> RELEASE. See `BUGS.md` F86.** Executing PT-20's step 5 for the first time
> measured **pack code being written into the player's savegame and still
> running after the mod is removed**. Two sites proven live:
> `Fix_MeteorFrequency` (the colony's meteors stop **permanently** and do not
> self-heal) and `Opt_DroneOverhaul` (98 errors/session, log noise only — and it
> leaked with **its own opt-in toggle OFF**). **Ten more are exposed — 12 in total**; the sweep corrected the membership both ways the same day (`Fix_DroneUnreachableForever` IN, `Fix_TrainCargoDumping` OUT — see the F86 entry).
> - **The route is a THREAD STACK, not a storage location.** A save captures
>   every game-time thread with its blocked stack; a mod function there is
>   serialised by value and comes back with an empty `_ENV`. The audit's
>   "class tables are safe" clearance is void — `Drone.Idle` is a class-table
>   write and leaked anyway.
> - **Synchronous code cannot be captured**, so ~62 of 74 modules are safe by
>   construction.
> - Controls: reproduces identically with the pack *disabled* and with the
>   junction *physically removed* (98 vs 98 errors, same locals).
> - ✅ **THE OWNER DECISION IS TAKEN (2026-07-31) — all four calls answered, and
>   ONE game-free item is owed.** Full spec and the recorded calls in
>   **`docs/reports/SAVE_SAFETY_REDESIGN.md`** §4.
>   1. **Layer ordering 3 → 2 → 1 ADOPTED** and written into **`FIX_POLICY.md`
>      §3a** as a hard rule binding new fixes as well as repairs (that section,
>      not BUGS.md, is now authoritative for it): patch a synchronous input
>      instead of replacing a blocking body; no mod code after a call that can
>      block; `SaveGameStart` tear-down last, only for what survives, each with
>      its own A/B plus a soak.
>   2. **The layer-3 sweep is AUTHORISED at full scope** (all full-replacement
>      modules, not just the 12 exposed). Game-free. ✅ **IT HAS RUN over the
>      exposed set** (`SAVE_SAFETY_REDESIGN.md` §5): **five of the twelve have a
>      layer-3 or layer-2 route out**, each via a verified-synchronous input;
>      only four own-thread modules plus `BombardmentSpread` are layer-1
>      candidates. ✅ **The non-exposed half ran too (§5.4, all 22 modules): 6
>      convert cleanly to a chained wrapper, 4 need a design pass, 9 are
>      correctly full replacements, 3 already optimal. DECISION 2 IS
>      DISCHARGED** — nothing further is owed on the sweep.
>   3. **F02 is HELD until that sweep reports.** Do not touch
>      `Fix_MeteorFrequency`. Accepted cost: the measured leak stays shipped
>      meanwhile.
>   4. **D10 and D12 are sequenced BEHIND the rules** — neither build starts yet.
> - ⚠️ **The F02 worked example was corrected with the decision:** the wrapper
>   keys on **`CurrentThread()`**, not the meteor descriptor — `Meteors.lua:279`
>   and the **`MeteorStorm`** thread at `Meteors.lua:326` pass the *same*
>   descriptor, so descriptor-keying would fire the storm warning ~5 sols early
>   and make Sensor Towers irrelevant to it (a balance change, FIX_POLICY §4).
> - ⚠️ **And the exposure list grew: 13, not 12.** The sweep caught
>   **`Fix_DroneUnreachableForever`** — it replaces `Drone:ApproachWrapper`, whose
>   `DroneApproach` call blocks, and runs mod code after it, the same layer-2
>   violation measured in `Opt_DroneOverhaul`. An earlier "no 13th site"
>   certification is **withdrawn**. Detail: `SAVE_SAFETY_REDESIGN.md` §4a.
> ⭐ **THE BUILD IS AUTHORISED (owner, 2026-07-31) — scope in
> `SAVE_SAFETY_REDESIGN.md` §6. Tiers 1 and 2; ⛔ LAYER 1 IS NOT TO BE BUILT.**
> The scope follows a severity tiering: exposure matters most where we
> **replaced a vanilla body**, because then uninstall leaves the player *worse
> than never installing* — as opposed to modules that **own their thread**, where
> the only cost is one log line for a fix the player just removed.
> - **Tier 1 (build first)** — `Fix_MeteorFrequency` (**measured**: meteors stop
>   permanently) and `Fix_RainsDeadlock` (**same shape, not previously called
>   out**: we replace the *global* `RainsDisasterLoop`).
> - **Tier 2** — `Fix_DroneUnreachableForever`, `Fix_TrainWaitTime`,
>   `Fix_ArrivalDeaths` half (b); plus `Opt_DroneOverhaul` ⛔ **blocked on the
>   drone carve-out**.
> - **NOT built** — the four own-thread modules and `Fix_BombardmentSpread`
>   (which has no layer-3 route at all). Accepted residual.
> - **⚠️ `Fix_ArrivalDeaths` half (a)** — the raw `SetPos` with no passability
>   search — **has no route yet** and needs a design pass.
> - **F02's hold is LIFTED**; D10/D12 stay held **until these repairs land**.
> - ⚠️ The tiering is **reasoned from the measured mechanism, not measured**.
>   The control, if ever wanted, is one PT-20-method leg against an own-thread
>   module.
> - ✅ **Remedy measured:** reinstalling the pack DOES revive a killed thread
>   (`IsValidThread(Meteors)` → `true`, restarted by our own `LoadGame`). The
>   answer for an affected player is "put the mod back" — real, and uncomfortable.

> ✅ **F87 IS FIXED (2026-07-31) — and the repair went into the shared scaffold,
> not the one file.** `Fix_DustSicknessBiorobots` threw at apply when the player
> enabled the mod, leaving F40 silently unfixed for that whole session — **every
> player's first run**, because a mod is never auto-enabled and the main-menu
> tick triggers an in-place reload where the presets are already loaded and the
> classes are not yet built.
> - **`SMRFixPack.DataPatch` now runs nothing before `ClassesBuilt`**, fires from
>   `ClassesBuilt` / `DataLoaded` / `ModsReloaded` / `DataChanged`, seeds its
>   `data_loaded` gate from the engine's own `DataLoaded` global (the message
>   never re-fires on that path), and `pcall`s its pass — `Msg` dispatches
>   through `procall`, so a throw there was swallowed and the fix would keep
>   reporting `active` while doing nothing. The filter is now built with
>   `PlaceObj`, which fails soft; the old `type(X) == "table"` guard passed on an
>   unflattened classdef, which is exactly why this shipped.
> - **The sweep it earned found THREE MORE sites silently dead on the enable
>   path** — `Fix_TechDescriptionBuilding` (the patch itself),
>   `Opt_MultipleSuns` (the build-limit lift, so the module ran half-live) and
>   `Fix_FirstAsteroidPrefabs` (its self-check). All repaired through the new
>   **`SMRFixPack.OnDataReady`**. Constructor sites: 6, all at runtime, none
>   exposed.
> - **FIX_POLICY §2 carries the rule** (no `apply()` may assume a cold boot;
>   both paths must be tested) and **ENGINE_FACTS carries the traced sequence**.
> - **Cold-boot A/B re-verified CLEAR** — see the leg rows below.
> - ✅ **AND THE ENABLE PATH ITSELF IS NOW MEASURED — the leg RAN and PASSED
>   (19.09, owner ticked the box).** `68/74` → **63/0/15/0**, probe-for-probe
>   identical to the cold boot bar two RNG lines, with the `DustSicknessBiorobots`
>   probe — which reads live preset data — PASSing on the path that used to
>   throw. The harness logged its own positive control (`ARMED — the pack is OFF`
>   before the click, `ENABLE DETECTED` after), so it is provably not a cold boot.
>   **This is the first measurement this project has ever taken of a player's
>   first session.**
> - ✅ **AND AGAIN WITH ALL SEVEN OPTIONAL MODULES ACTIVE (19.24): `74/74` ->
>   68/0/10/0**, matching the all-ON cold-boot reference exactly. All five `Opt_`
>   probes PASS on the enable path. The log carries
>   `MultipleSuns: Artificial Sun build-once limit lifted` — a line that can only
>   come from the new `OnDataReady`, so one of the three sweep repairs is
>   confirmed firing on the very path where it was dead.
> - 🛠 **CORRECTION: "this leg also verifies audit A2" is WITHDRAWN.** A2 was
>   **answered YES in play by PT-55 on 2026-07-30** ("all three hooks install and
>   run on a first mid-session enable, no relaunch") and the audit caveat was
>   retired then. A2 is also a different path — the MODULE toggle mid-session,
>   not the PACK enabled at the main menu.

**⛔ NEW HARD RULE 2026-07-30 (owner) — FIX_POLICY §4a: this pack never fixes
other mods' problems.** Neither bugs caused by another mod, nor vanilla bugs
reachable only from mod code. "For modder benefit" is no longer a valid reason
to ship anything. Overridable ONLY by asking the owner explicitly, per case —
never inferred, never carried forward. **The test is WHO BENEFITS, not how visible the problem is** (owner's
clarification, same day): if a player could be harmed now or after a future
patch/DLC — even invisibly, even latently — it is a real fix and it ships; only
"the sole conceivable beneficiary is another mod" is barred. Operationally that
is the **R4/R3 boundary**: R4 needs new *calling code* (mod territory, barred),
R3 needs new *data* (ships with patches and DLC, so player territory, allowed).
It retired **F28** (R4, zero callers anywhere) and **nothing else** —
**F29 was briefly flagged and is KEPT**: its self-description as "mod-facing /
No shipped user" is factually wrong, the audit found four live shipped callers
in Mystery 2, making it R3 latent-by-data like F27/F31/F43. §4a now warns
explicitly: judge by enumeration, never by an entry's own words.

**Counts changed twice on 2026-07-30 — TWO modules deleted:**
**`Fix_ReplaceTechCount` (F28)** went under the new §4a rule: `Research:ReplaceTech`
has **zero callers in all of Src** (re-verified independently), so only mod code
could reach it, and it was carried as a §1.5 full replacement. Its TestKit probe
went with it (**probes 77 → 76**) — it asserted the fixed counter, so it would
have FAILed every leg. **The A/B that owed for it RAN the same evening and is
CLEAR** (19.20 leg — `73/73`, 76 probes, `66/0/10/0`; table below). Earlier the
same day:
**`Fix_DomePipeMoveInside` DELETED**
— F24 closed `wontfix` by user decision after the trigger was proven
unreachable in the shipped game (full proof on the F24 entry). No TestKit probe
existed for it, so the 77-probe suite is unchanged. **The owed A/B RAN the same
evening and the code gate is CLEAR** — see the post-removal row in the table
below. `Fix_TrainMinors` also lost its (c) guard the same day (F49(c)
`wontfix`, designed behaviour), which changes no counts.

**Just landed (2026-07-29 late, D09 build):** the drone stat dials DECISION is
BUILT — `Code/Opt_DroneStatDials.lua` + two Mod Options dropdowns: Drone
speed 1x/2x/3x/5x (range widened from the DECISION's 1.5x/2.0x by user call
after the live no-clamp probe: `SetMoveSpeed(10000)` read back exactly, clean
movement at ultra) and Drone carry +0/+1/+2. Techs' own label-modifier
machinery, reconciled on ApplyModOptions/CityStart/PostLoadGame, base =
modifiers removed = vanilla. D09 entry in BUGS.md; **PT-56 PASSED IN FULL
2026-07-30 → D09 `tested`**. **The owed
post-D09 A/B pair RAN unattended the same night — see the probe-state table
below (code gate CLEAR).**

**Landed earlier the same day (audit-remediation session):** `docs/archive/AUDIT_FINDINGS.md` (ARCHIVED 2026-07-30 — Phases 1-3 complete; **Phase 4 EXECUTED 2026-07-31**, C3 permanently barred)
Phases 1-3 implemented — code: veto re-check in the three data-patch fixes
(A1), DustSickness data-loaded latch (B3), file-scope install for the three
flattening-unsafe Opt_ hooks so a first mid-session enable works (A2),
reconciler "error" retry + skip logging (B1), MeteorStormWedge clears the
prediction flag itself (B2), logger escaping + build stamps (C4);
packaging: short_description / last_changes / optional_mod / ignore_files +
75 ModItemCode items (editor round-trip no longer wipes the mod) (A3);
description/README truthful: CohortHousing block, honest savegame claim,
console achievements + per-fix-disable disclosures (A4/B4/D1/D2). Docs
restructured (this header, ENGINE_FACTS, SESSION_LOG, archives). Details:
the newest SESSION_LOG leg.

**⭐ F83 IS BUILT AND `tested` — `Code/Fix_FirstAsteroidPrefabs.lua`, shape
(i), the load-time heal.** (Built 2026-07-30 late; **PT-59 PASSED IN FULL on the
keyboard 2026-07-31**, archived — see the block below the build description.) The owner's go was recorded, the corrected brief was
followed, and the build ran with its own probe and a CLEAR harness leg
(`74/74`, `67 PASS / 0 FAIL / 10 SKIP / 0 ERROR` at 77 probes — the all-toggles-ON
configuration *as it stood at build time*; that leg and its owed twin have both
since been superseded by the post-Phase-4 set at 78 probes, and **nothing is owed
on the harness side for the COLD-BOOT configurations** — see the enable-path
caveat on the A/B table below, added 2026-07-31). What
ships: an `OnMsg.LoadGame` sweep that, when the FirstAsteroid popup notification
is still sitting in the persisted `Notifications` table after a load — the only
state the dead real-time waiter can leave — **removes** it, **grants** the three
prefabs through the shipped `ColonyAddPrefabs` calls, **latches** a persistent
`SMRFixPack_FirstAsteroidPrefabs` GameVar, and **re-shows** the popup as pure
display so the player still gets the story text. The healthy path is untouched
(no reload means no `LoadGame`), which is what makes the double-grant trap
unreachable rather than merely guarded. Removing the notification is
load-bearing: its `PressFunc` is the only route back to the dead context, so
exactly one grant path exists — and that stays true even if a future patch moves
the shipped waiter to a game-time thread. **Shape (ii), the `show_once`
pre-mark, was verified against Src and REJECTED** (it depends on OnMsg order and
on `CreateRealTimeThread` scheduling that Src cannot settle, it moves the grant
off the healthy path for everyone, and it cannot heal an already-stranded save).
**Correction to the audit's build note:** matching the notification on `text[1]`
works only in a dev build — retail `T()` returns **light userdata** when the id
is in the translation table (`localization.lua:268`); the fix uses `TGetID`
(`:48-65`) and reads the id from the live preset rather than hardcoding it.
**✅ PT-59 PASSED IN FULL 2026-07-31 → F83 is `tested`** (archived to
`PLAYTEST_ARCHIVE.md`; nothing owed). Reload leg **1/1/1** with the grant line;
healthy leg **1/1/1** with `SMRFixPack_FirstAsteroidPrefabs` still `false`, so
vanilla granted and our code never ran; and the sitting logged **10 game loads
against exactly 2 grants**, with 7 non-granting loads between the two — Trigger
C many times over. Log clean. Two unasked-for results worth keeping: the heal
**discriminated between two asteroid notifications** sitting in the corner list
together (the loc-id match is doing real work), and **8 of 10 loads granted
nothing**, so the no-op path is the common one and it is silent.
⚠️ **The test's own procedure was wrong and has been corrected** — it never said
*which* popup to answer, and answering `ReconCenterDiscoveryAsteroid` produces
`0/0/0`, indistinguishable from a fix failure. It was reported as a FAIL before
the source settled it. The `FirstAsteroid` preset declares no choices at all and
its callback runs on any answer, so there is no wrong *button*, only a wrong
*popup*.

**The finding it closes (2026-07-30, live play) — F83, P2, mechanism PROVEN.**
Minimized story popups lose their callback across a save/load: the waiter is a
real-time thread and the async popup context is not persisted, while the corner
notification *is* — so after a reload the notification still opens, any choice
closes it, and the callback never runs. Found via a dead **View** button on a
founder popup (unrelated to F23/PT-44; not caused by this pack), isolated at the
keyboard, and confirmed by a controlled quicksave/reload leg. Six of the seven
affected call sites are cosmetic; **the seventh is `FirstAsteroid`, whose
callback grants three Micro-G Auto Extractor prefabs that the popup's own text
promises and `show_once` never re-offers.** **PT-58 RAN AND PASSED the same day
and the consequence is now OBSERVED, not inferred:** one purpose-built fixture,
one variable, **1/1/1 answered without a reload vs 0/0/0 answered after one**.
The notification survives the load, opens normally, and grants nothing.
**✅ THE QUEUED POPUP AUDIT RAN 2026-07-30 (`docs/reports/POPUP_CONSEQUENCE_AUDIT.md`)
and the hold is LIFTED: the narrow-decouple recommendation is REINSTATED.** The
storybit alarm that stopped the fix was wrong about the engine — **game-time
threads persist by default with their blocked stacks; only real-time threads
die on load** (new ENGINE_FACTS entry, three source proofs + observed
unit-command resumption). Storybits, mysteries, anomaly sequences and
challenges are save-safe by design; the defect family is exactly "consequence
owned by a REAL-TIME popup waiter": F83's two consequential sites (FirstAsteroid
OBSERVED; ReconCenterDiscoveryAsteroid — Detailed Scan recoverability still
needs eyes), six-ish cosmetic dead-View sites, and one latent shielded class
filed as **F85** (breakthrough choices ×3 + the Assembly "Colony Values"
choice — real-time waiters behind an open-immediately modal window; tier U,
settling observation = the rebind-quicksave check). F06 is NOT this family
(one-shot Msg race; its fix stands). The audit also left a **4-item needs-eyes
list** (audit §8, mirrored on the checklist) and repaired a BUGS.md structural
break (the F84 filing had swallowed the D06 heading). **The owner gave the
build GO the same evening** ("review and action on your findings") — the F83
decouple is queued as the next session's headline task with a **corrected
build brief** (double-grant trap caught after the go: vanilla's popup callback
always runs, even show_once-suppressed — see the F83 entry and
FABLE_NEXT_PROMPT's board; PT-58's kept fixture is the A/B — reload leg must
read 1/1/1 AND the no-reload leg must still read 1/1/1, not 2/2/2). Full trail
on the F83/F85 entries and the audit file.

**⛔ SCOPE CONTROL, owner 2026-07-31 — `docs/FUTURE_IDEAS.md`.** New parking
file for good ideas that are NOT needed before launch. **Nothing in it is work:
not owed, not scheduled, not counted, and never to be reported as
outstanding**; un-parking is an explicit owner decision, one item at a time,
after launch. Reason on record: mission creep — every three items closed were
adding about six. **Defects never go there** (they stay in `BUGS.md` with a real
status; declining one is a `wontfix` with reasoning). Entry 1 is
seniors-in-workshops. A proposed-parking list sits at the bottom of that file
awaiting the owner's yes/no — **read it before treating anything on it as
owed.**

**⭐ PHASE 4 COMPLETE AND CERTIFIED (2026-07-31).** C2 shared helpers
(`SMRFixPack.Log/Require/SetGlobal/WhenActive/DataPatch` in 00_Core, 58 files
migrated), C4 deeper self-checks (42-file EXIST-only tier enumerated and
raised; declaring-class failures now loudly diagnosed via a `__parents` walk),
and the C1 update-deactivation report (pregame-menu dialog, console-visible,
shown only when ≥1 fix deactivated over a game-code change; honest about what
self-checks cannot see). Eleven unattended legs, every one identical to the
control fingerprint (`docs/archive/fingerprint_before.txt` →
`fingerprint_after.txt`); full certification with evidence and residual risk
in the newest SESSION_LOG leg. C3 merges were BARRED and not done; the three
drone modules are untouched per the carve-out. **✅ The owed default-config leg
RAN 2026-07-31 12.44 after the owner set the six toggles OFF + dials to base:
`68/74`, 63 / 0 / 15 / 0 at 78 probes — the certification's predicted numbers
exactly (fingerprint: `docs/archive/fingerprint_after_default.txt`). NOTHING
is owed on the harness side; both shipping configurations are measured
post-Phase-4, and the account is in the clean all-OFF/base state.**

> 🧭 **UNDECIDED, and deliberately so — a possible PACK SPLIT (owner, 2026-07-31).**
> Under serious consideration: separating the project into **(a) the true fixes**
> and **(b) a companion mod holding the opt-in modules**. **No decision has been
> made and the owner does not want one yet** — a third state, like D08 and
> D06-structural. It is **not owed, not scheduled, not counted**, and **nothing
> may be deferred "until the split is decided".**
>
> **The reason for not deciding is itself the record:** the current single-mod
> shape is the best one for *testing*. One mod is one configuration matrix, and
> every measurement we hold is calibrated to it — the `fix pack present: N/74
> fixes active` line, the 78-probe fingerprint, the three-leg A/B set, and the
> baseline mechanism (emptying the `code` list). Splitting mid-testing would
> invalidate the comparison base.
>
> **Known impacts, recorded so the eventual decision is informed rather than
> rediscovered:**
> - **The harness is calibrated to one mod.** Counts, the baseline leg, and the
>   opt-in leg bridge (`SMRFixPack_Optional`) all assume a single `code` list.
> - **The `OptionsMenu` probe asserts six toggle wirings PLUS the two D09 dial
>   wirings** in one place; a split divides that surface across two mods.
> - **D05 (Mod Options) currently lives in the pack**, and the opt-ins are
>   reached through it — the companion would need its own options surface or a
>   cross-mod bridge (note `CurrentModOptions` is **per-mod-env**, ENGINE_FACTS).
> - **It composes with the cleanup-mod proposal** (D06 entry): that would already
>   make a second shipped artifact, so the question becomes the shape of a
>   *family*, not whether to have one.
> - **It has a natural deadline** — it changes what players install, so it is
>   cheap before beta and expensive after.

**Open user decisions:** ~~F83 fix option 1 go/no-go~~ — **GO GIVEN, BUILT
2026-07-30, and `tested` 2026-07-31** (PT-59 PASSED IN FULL; nothing owed).
~~Phase 4 go/no-go~~ — **EXECUTED 2026-07-31, see above.** Still open:
D01 standing-export half
(spec decided 2026-07-26, unwritten); F48 (parked section below); drone
overhaul structural choice (DRONE_OVERHAUL_OPTIONS.md — the stat dials are
BUILT (D09); the structural choice stays gated on the B2 re-run);
**~~F79~~ — CLOSED `wontfix` 2026-07-31 (owner: risk exceeds benefit on large
multi-stop maps; F80 must be explained first if ever revisited)**; D08;
**~~seniors-in-workshops~~ — PARKED 2026-07-31, see `docs/FUTURE_IDEAS.md`**;
**D11 shuttle same-pair passenger batching — candidate with feasibility on
file (BUGS.md entry), explicitly NOT green-lit: re-ask the user before any
build; multi-hop passenger routing REJECTED outright.**
**Decided, build queued:** D10 workshops module (speced + user-approved
2026-07-30, BUGS.md entry — text repairs + capacity dial; build gated on
PT-56 PASS — **that gate is now OPEN, PT-56 passed 2026-07-30**). **D12
no-homeless dome policy** (speced + user-approved
2026-07-30, BUGS.md entry — own module, `Opt_ResidencyControl` as donor pattern
only; breaks vanilla's emigration tie for homeless colonists so specialist
domes stop stranding them, which also unwinds the D07 overpopulated deadlock
without touching D07). **D10 and D12 both touch colonist assignment — land them
separately, each with its own A/B.** ~~Unfiled candidate: Universal Tunnel
description~~ **now FILED as F84** (2026-07-30) — the description is wrong twice:
it claims rovers cannot use the tunnel (**disproven by play** during PT-25) and
omits that it bridges life support. Text patch, but it converts a localized `T`
into an English-only `Untranslated` string, so **decide it together with D10's T1
text repairs** — identical tradeoff, should not be answered twice differently.

**A/B probe state — CURRENT is the POST-PHASE-4 set at 78 probes (2026-07-31).**
All six toggles ON: `74/74` → **68 / 0 / 10 / 0** (leg 12.30.34). Baseline
(`code` list emptied): **1 / 62 / 15 / 0** (leg 12.32.11), where both the
`FirstAsteroidPrefabs` and the new `UpdateReport` probes **FAIL** with
`fix pack not loaded (bug reproduces)`, proving they discriminate. Default
config, six toggles OFF + dials at base (owner-flipped, leg 12.44.39):
`68/74` → **63 / 0 / 15 / 0** — predicted before the run and landed exactly;
the D09 probe reports the carry dial AT BASE on entry, so the account is
genuinely clean. Every measured leg: zero `[CommunityFixPack]`
error/disabled/FAILED lines, no log line naming our `Code/`, known noise only.

> ✅ **THE ENABLE PATH IS NO LONGER UNMEASURED (2026-07-31 19.09).** Every leg
> above except the 19.09 row is a COLD BOOT — launched with the pack already
> enabled, describing the *second session onward*. The session in which a player
> *turns the mod on* is where **F87** lived, and it now has its own leg: TestKit
> `Code/98_EnablePathLeg.lua` (armed like `96_AutoRunFlag`, recipe in
> `PLAYTEST_HELP.md`) boots with the pack off, waits for **the owner to tick it
> at the main menu**, then drives the normal flow. **Its first run PASSED.**
> ⚠️ **Coverage note:** that run had the six toggles OFF, so the five `Opt_`
> probes SKIPped — the optional modules are still unexercised on this path. A
> second leg with them forced ON closes it. **It does NOT bear on audit A2**,
> which PT-55 answered in play on 2026-07-30.
The post-F83 set at 77 probes (`74/74` → `67/0/10/0`; default `68/74` →
`62/0/15/0`; baseline `1/61/15/0`) is now historical, as are all older rows.

| Leg | Active | Result |
|---|---|---|
| **⭐ NEWEST — the F49(a)-strip code-gate leg, default config, 2026-08-01 14.15 (unattended), 78 probes** | **68/74** | **63 / 0 / 15 / 0** — the owed leg for the F49(a) guard strip, CLEAR. Fingerprint vs the 18.44 default-config reference differs in exactly ONE real line (`TrainMinors` now `train cap recomputed 4->1, 40->2, 0->0`, palette clause gone as predicted) plus the two known RNG lines (`TouristApplicants`, `FounderTraitNotification`). `PROBE SWEEP:` armed `97_SaveHookProbe.lua` only (declared); `99_OrphanEnvProbe.lua` deleted before the leg and no `SMRTEST-ORPHANENV` line in the log |
| **⭐ CURRENT — THE ENABLE-PATH LEG, all optional modules ON via the `SMRFixPack_Optional` bridge, 2026-07-31 19.24 (owner ticked the box), 78 probes** | **74/74** | **68 / 0 / 10 / 0** — matches the all-ON cold-boot reference exactly; all five `Opt_` probes PASS on the enable path, and `MultipleSuns: … limit lifted` proves the `OnDataReady` repair fired there |
| **⭐ CURRENT — THE ENABLE-PATH LEG, default config, 2026-07-31 19.09 (owner ticked the box at the main menu), 78 probes** | **68/74** | **63 / 0 / 15 / 0** — **the first leg ever run on a player's FIRST session.** Probe-for-probe identical to the 18.44 cold boot bar 2 RNG lines. `DustSicknessBiorobots` PASS on live preset data = the F87 patch really ran. ⚠️ toggles OFF, so the five `Opt_` probes SKIPped |
| **CURRENT — POST-F87-REPAIR cold-boot re-verify, default config, 2026-07-31 18.44 (unattended), 78 probes** | **68/74** | **63 / 0 / 15 / 0** — identical to the 12.44 reference; proves the scaffold change did not regress the cold boot. Says NOTHING about the enable path |
| **CURRENT — POST-PHASE-4, all six toggles ON, 2026-07-31 12.30 (unattended), 78 probes** | **74/74** | **68 / 0 / 10 / 0** |
| **CURRENT baseline — POST-PHASE-4, `code` list emptied, 2026-07-31 12.32 (unattended), 78 probes** | — | **1 / 62 / 15 / 0** — `FirstAsteroidPrefabs` + `UpdateReport` FAIL here (`bug reproduces`) |
| **CURRENT — POST-PHASE-4 default config, six toggles OFF + dials at base, 2026-07-31 12.44 (unattended), 78 probes** | **68/74** | **63 / 0 / 15 / 0** — predicted exactly; carry dial AT BASE on entry |
| Baseline, historical (`code` list emptied) | — | **1 PASS / 61 FAIL / 15 SKIP / 0 ERROR** *(77 probes, pre-F28)* |
| Fixed, default config (six toggles OFF) | 69/75 *(pre-F24-removal)* | **62 / 0 / 15 / 0** |
| Fixed, all six toggles ON + dials | 75/75 *(pre-F24-removal)* | **67 / 0 / 10 / 0** |
| Post-removal re-verify, 2026-07-30 17.25 (unattended) | 74/74 *(pre-F28-removal)* | **66 / 1 / 10 / 0** — the 1 FAIL was the probe defect below |
| All six toggles ON, 2026-07-30 19.20 (unattended), 76 probes | 73/73 | **66 / 0 / 10 / 0** — pre-F83-build |
| Default config, six toggles OFF + dials at base, 2026-07-30 19.32 (unattended), 76 probes | 67/73 | **61 / 0 / 15 / 0** — pre-F83-build |
| Post-F83 build (superseded by Phase 4), all six toggles ON, 2026-07-30 23.29 (unattended), 77 probes** | **74/74** | **67 / 0 / 10 / 0** |
| Post-F83 baseline (superseded by Phase 4), `code` list emptied, 2026-07-30 23.46 (unattended), 77 probes** | — | **1 / 61 / 15 / 0** — `FirstAsteroidPrefabs` FAILs here (`bug reproduces`) |
| Post-F83 default config (LAST measured default, superseded by Phase 4), six toggles OFF + dials at base, 2026-07-31 01.37 (unattended), 77 probes** | **68/74** | **62 / 0 / 15 / 0** |

**The 01.37 leg (2026-07-31) — the shipping default configuration post-F83,
CLEAN, and the last thing the build owed on the harness side.** Run after the
owner set all six toggles OFF and both dials back to base (their own
`deactivated via Mod Options` lines are on record in the 01.33 session log).
`fix pack present: 68/74 fixes active`, **62 / 0 / 15 / 0** — predicted before
the run and landed exactly: the five opt-module probes flip PASS→SKIP as
`inactive (opt-in)`, so 67/10 becomes 62/15 with the same zero FAIL and zero
ERROR. `FirstAsteroidPrefabs` applied and its probe PASSed here too, confirming
the F83 fix is toggle-independent (it is a default-on fix, not an opt module).
The D09 probe reported the **carry dial AT BASE on entry** — the account state
is genuinely clean for the first time since the PT-58 sitting. Six
`[CommunityFixPack] … inactive (opt-in module …)` lines (six, not five —
DroneOverhaul reports status despite having no probe), zero error / disabled /
FAILED lines, no log line names our `Code/`, same noise profile
(2 `ResManager` `LawOfficeDoor`, `objects_to_mark` 48).

**The 23.29 leg — the F83 build's gate, CLEAR.** `fix pack present: 74/74 fixes
active`, **67 / 0 / 10 / 0** at 77 probes — the predicted arithmetic exactly
(66 + the one new `FirstAsteroidPrefabs` probe). `[CommunityFixPack]
FirstAsteroidPrefabs: applied` on load; the probe PASSed all three of its legs
(*"stranded save granted 1/1/1 and latched; already-healed and non-FirstAsteroid
states granted nothing"*). Zero error / disabled / FAILED lines, no log line
names our `Code/`, known noise only. **What this leg also revealed: the account
toggles are ON again** — the prompt doc's "owner left all six OFF" had gone
stale during the PT-58 sitting, and the D09 dial probe reported the carry dial
off base too. Read the account state, never trust a doc for it.

**The 19.32 leg — the shipping default configuration, CLEAN.** Run after the
owner set all six toggles OFF and both dials to base. `fix pack present: 67/73
fixes active`, and the result was **predicted before the run and landed exactly**:
the five opt-module probes flip PASS→SKIP as `inactive (opt-in)` (five, not six —
D06 has no probe of its own), so 66/10 becomes 61/15 with the same zero FAIL and
zero ERROR. `DroneStatDials` and `OptionsMenu` both stay PASS, confirming the
dials and the Mod Options wiring are independent of the toggles. The six
`[CommunityFixPack] … inactive (opt-in module, off by default …)` lines are the
expected healthy default-config signature, **not** error lines — six here, not
five, because DroneOverhaul reports its status even though it has no probe. Zero
error / disabled / FAILED lines, no log line names our `Code/`, same noise
profile again (2 `ResManager` `LawOfficeDoor`, 1 shutdown artifact,
`objects_to_mark` 48).

**The 19.20 leg — the owed A/B, run and CLEAR.** `fix pack present: 73/73 fixes
active`, matching the post-F28 registry exactly; **zero** `[CommunityFixPack]`
error / inactive / disabled / FAILED lines; no log line names our `Code/`; noise
profile identical to the 17.25 leg (same 2 pre-existing `ResManager` animation
errors, same shutdown-artifact `[mod] Error in mod … Test Kit`, `objects_to_mark`
48→59 with the random map). The account had all six toggles ON at that point,
hence `73/73` — **read the state, never assume it.**

**The D09 probe defect is REPAIRED (TestKit, 2026-07-30 late) and verified.**
The probe used to take its baseline from the live const, valid only when the
account dial already sat at base; it now forces both dials to base through the
real Apply path, measures from there, and restores the leg's entry values, with
a cleanup check against the entry reading rather than against base. It went
**green on the 19.20 leg with the account carry dial still at +1** — the exact
state that FAILed it at 17.25. Consequence: **an A/B leg no longer has a
set-the-dials-to-base precondition.** PT-56 still does, for its own step-1
baseline reads (BUGS.md D09 entry, item 1).

**The 17.25 leg (superseded by 19.20, kept for the record):** the code gate for
the F24 and F49(c) removals, run unattended after both. `74/74 fixes active` —
exactly one fewer than the pre-removal 75/75, which was the F24 deletion and
nothing else — zero `[CommunityFixPack]` error lines, `DroneStatDials: applied`,
probe total still 77 (F24 had no probe). Its single FAIL was the D09 probe
defect described above, now repaired.

**Reading any leg:** baseline's 1 PASS is the FactionFundingCheck canary, and
the D09 probe FAILs baseline by design ("fix pack not loaded"). The 10 SKIPs in
a fixed leg are 9 `[install]` retail-sandbox probes + TechDescriptionBuilding; a
default-config leg's extra 5 are the opt-module probes reporting `inactive
(opt-in)` — five, not six, because D06 has no probe of its own (the stress
harness covers it). Known synthetic-map noise only: ~50-60 `Flight.lua`
`objects_to_mark` errors, a few GameInit nil-call lines, 2 `ResManager Error`
missing-animation lines (`LawOfficeDoor`, pre-existing and present in every leg),
the MultipleSuns "not found → lifted" load transient, and a `[mod] Error in mod …
Test Kit` line at quit (shutdown artifact).

**The post-D09 pair caught two real defects en route** (both fixed
same-session, see the D09 entry): the module's file-scope `Modifier.new` check
tripped the F64 pre-flattening trap, and the probe's first version wrote the
TestKit env's own `CurrentModOptions` (per-mod-env — new ENGINE_FACTS entry).

**⚠️ ACCOUNT STATE as of 2026-07-30 19.32 — READ IT, NEVER ASSUME IT.** The
owner set **all six toggles OFF and both dials to base** before that leg, and the
`67/73` reading confirms the toggles. **This is the clean state PT-56 needs** —
if a later sitting moves the dials again, PT-56's step-1 baseline reads go stale
the same way they did on 2026-07-30 afternoon. Note the repaired D09 probe is
deliberately *immune* to account dial state, so a leg's PASS no longer proves the
dials are at base; the probe was therefore extended the same evening to **report
the dial state it found on entry**, restoring the observability the broken
version had by accident. **Read the DIALS too, not just the toggles.** Pre-D09
reference set (76 probes): baseline 1/60/15/0 · default 61/0/15/0 at 68/74 ·
all-toggles 66/0/10/0 at 74/74.

**Next gates (owner playtests — PLAYTEST_CHECKLIST.md):** **PT-55 CLOSED IN
FULL 2026-07-30** (archived; audit A2 caveat retired; the D01 parked-rocket
limitation ACCEPTED by user call `4f5f61e` — a parked rocket picks the
behavior up on its next landing, `on_activate` enhancement on record but
unbuilt). **PT-48 CLOSED IN FULL 2026-07-30 → D02 `tested`** (archived; all
five steps on console counters, opened with a positive control; the acked
building held 4.2 vanilla windows and the stamp survived save/reload; a vanilla
GameTime-vs-RealTime curiosity on `InsufficientResources` was filed on the D02
entry for a game-free look). **PT-25 PASSED IN FULL 2026-07-30 → F38 `tested`**
(archived; rover used the tunnel, took the long way once destroyed, **still took
the long way after a save/quit/load** — the leak the fix closes — and **used it
again after Rebuild**, the over-reach guard. Its setup line was WRONG and was
corrected at the keyboard: the tester spotted that the underground has no tunnel
at all, and tunnels turned out to be a surface building — fourth PT found faulty
by executing it. F38 itself survived the challenge. **SAVE-B is retired**, PT-25
was its last consumer and never needed it. The rover check also **disproved the
Universal Tunnel's description → F84**.)
**PT-44 PASSED 2026-07-30 → F23 `tested`**
(archived; the notification fired 0→1 on the module's own counter and read
"Founder Has Trait / Ciara Grant: Fit" — exactly one, with the dead shipped
handler staying dead. Console-injected grant, so it verifies rendering; the path
is R1 by enumeration. It also corrected a checklist expectation: a notification
click selects its object **only when that object is visible** — an indoors
colonist gets a camera pan and no selection, which is correct vanilla.)
**PT-56 PASSED IN FULL 2026-07-30 → D09 `tested`**
(archived; all four steps live, including the stale-save reconcile — a save
carrying 2x/+1 modifiers, loaded against base dials, came back at the baseline
`1728/1`. **This UN-GATES the D10 workshops build**, which is speced,
user-approved and ready to write). Next: PT-53 Trigger E (the
last thing between D07 and `tested`); ~~PT-54 wedge watchdog~~ **(RETIRED
unrun 2026-08-01 → the F86 Tier-1 build legs)**; PT-52 Trigger B +
the B2 re-run on the v2 stress harness; PT-20 save/remove/load
incl. wave-6 persisted state; PT-21. **PT-46 tail: (d) PASSED 2026-07-30**
(cap follows length, `43/2`→`13/1` across a salvage); **(a) settled R4 by the
reachability audit** (no player-reachable entry into `place_track` — see the
audit's lead-pass block); **(c) closed `wontfix` 2026-07-30 (user decision,
tier I — designed behaviour), guard REMOVED (`d03417b`)**. F49 now holds at
`fixed*` on (a)+(d), carried by (d).

**Newest legs:** `docs/archive/SESSION_LOG.md` → the 2026-07-30 set, newest
first: the PT-55 closure leg, the PLAYTEST_CHECKLIST/PLAYTEST_HELP split leg,
the curiosity leg (tunnel water, workshop research → D10 spec, shuttle limits
→ D11 candidate), and the parallel playtest legs (PT-55/PT-53-A/D12); the
2026-07-29 D09-build and PT-11 legs sit below them.

**Playtest-method rule earned 2026-07-29 (applies beyond PT-11):** compressing a
scheduler's `g_Consts` interval does NOT shorten the sleep already in flight, so
a "nothing should happen" test must **re-arm the repeat**
(`RestartPeriodicRepeatThread`) and **carry a positive control**, or it
false-PASSes regardless of the fix. Full rule in PLAYTEST_HELP.md (the
checklist's reference half, split out 2026-07-30). Two tests have now been found unrunnable-as-written by actually running
them (PT-29, PT-11) — treat an un-run PT's procedure as unverified until it has
been executed once.

**Tech-gated fixes — coverage settled 2026-07-29, re-grounded by the
2026-07-30 reachability audit.** F41 is `tested` (PT-29). Of the other four,
**F28** (R4 — zero callers in all of Src; the audit's one DELETE candidate,
user decision pending), **F43** (R3 — corrected grounds: MoistureVaporator IS
tech-locked, but its `require_prefab`+unlocked cargo item routes it into the
branch the shipped code handles; the old "no tech-locked entry" wording was
wrong) and **F25** (R2 — pre-1.0.6 legacy saves; note the probe's SKIP label
may be mislabeled, see the entry) are correctly untestable in play. **F18** is
the only genuinely uncovered one: preset half probe-covered, play half needs
the Independence arc + a special project; judged not worth a PT for a
data-only P2.

**REACHABILITY AUDIT COMPLETE 2026-07-30 — `docs/reports/REACHABILITY_AUDIT.md`.**
All 66 fix modules + both sanitizer passes audited for player reachability
(the F24 question, asked pack-wide): ~21 R1, ~38 R2, five R3 (kept — F27,
F29†, F31, F43, F57(a)†; † = §1.5-latent, flagged), one U (F11, settling
observation on the entry), two R4 — F49(a) (kept, lives inside a module with
two live halves) and **F28 (DELETE candidate, awaiting user decision)**. A
proposed FIX_POLICY §4 amendment (reachability tier required before a fix
ships) ~~is drafted in the audit file, not applied~~ — **APPLIED 2026-08-01,
`FIX_POLICY.md` §4 is the authority now**; the two † entries above are exactly
the R3-plus-§1.5 combination it makes conditional on an owner decision, routed
to chain prompt 7. Eleven BUGS.md entries
carry new "Audit 2026-07-30" notes (evidence corrections: F06, F17, F22, F25,
F34, F37, F40, F43, F49, F74, F81 — plus F11's observation).
**CHALLENGED same day and one verdict fell: F49(c) was tabled "live R2"
unenumerated and was in fact designed behaviour** — closed `wontfix` by user
decision, guard removed. The "Challenge review 2026-07-30" appendix in the
audit file answers it: the three-part method failure (bundle inheritance;
grading reachability while inheriting defectiveness — source is decisive on
"can this path execute" and near-mute on "is it wrong", so UI-shaped
misreadings come back confident, not uncertain; evidence base going stale
mid-audit — `c3c4383`/`ba1e88b` landed during the run and were not re-read),
the two unenumerated verdicts (F49(c) wrong, F49(d) late-enumerated and
holding), the eleven-row source-blind-spot list with settling observations,
the new tier **I — Intentional**, and the REVISED §4 (**APPLIED 2026-08-01**,
`FIX_POLICY.md` §4) now requiring a
positive intent statement (hard tells: player report / dead code / sibling
contradiction / self-contradiction / dev comment; no tell → keyboard
observation before any fix is written). Still not applied — user go-ahead.

## What this project is

"Community Fix Pack" — a runtime-Lua bug-fix mod for Surviving Mars: Relaunched
(game dir `A:\SteamLibrary\steamapps\common\Project Spark`, Haemimont Sol engine,
NOT Unreal; full gameplay source shipped in `<game>\ModTools\Src`). No game files
are modified; planned community release after user testing. Dev repo:
`C:\Dev\SMR-BugFixPack` (git). Installed via junction at
`%AppData%\Surviving Mars Relaunched\Mods\SMR-BugFixPack`.

Companion **Test Kit** mod (never shipped): `C:\Dev\SMR-BugFixPack-TestKit` (git).
`SMRTest.RunAll()` runs one probe per fix and prints PASS/FAIL/SKIP; run it with
the fix pack disabled (expect FAILs) and enabled (expect PASSes). It also enables
the Lua console at load and carries observability loggers and state reports.

## Optional modules (6, off by default)

**Players enable them in Options → Mod Options (D05 — live toggles, both
directions, including a first mid-session enable since the 2026-07-29 audit
fix);** the pre-load `SMRFixPack_Optional = { <Id> = true }` table remains as
the override surface for other mods and the test harness.
`SMRFixPack.ListFixes()` reports them as `inactive` with the opt-in reason
until enabled. Files use an `Opt_` prefix instead of `Fix_` to mark them as
not-bug-fixes. Full detail: each module's BUGS.md D-entry and file header;
build history in SESSION_LOG.md.

- **ClassicRockets** (D01, `Code/Opt_ClassicRockets.lua`) — a player-controlled rocket
  parked at the colony keeps its launch ration requested even with no destination selected,
  so drones refuel it while it waits. Only the fuel half of D01; the standing Rare Metals
  export half is deliberately unwritten (see the D01 entry).
- **AcknowledgedWarnings** (D02, `Code/Opt_AcknowledgedWarnings.lua`, added 2026-07-27,
  **`tested` 2026-07-30 — PT-48 PASS in full**) — dismissing "Building Not Working"
  acknowledges the listed buildings until they recover; new breakages always warn
  immediately.
- **ResidencyControl** (D03, `Code/Opt_ResidencyControl.lua`, added 2026-07-27) —
  per-dome/habitat "closed to new residents" policy row; quarantine untouched.
- **MultipleSuns** (D04, `Code/Opt_MultipleSuns.lua`, added 2026-07-27) — lifts the
  Artificial Sun build-once limit and carries the absorbed F39 panel-binding fix.
  **This module is also where F56 would land** if the closed-`wontfix` auto-offload
  decision is ever reopened (user decision 2026-07-26): auto-offload and the export half
  are the same "rockets should load and unload themselves like they used to" request over
  the same machinery, so they ship together behind this one flag or not at all. Do not
  create an `Opt_AutoRocketOffload`.
- **DroneOverhaul** (D06, `Code/Opt_DroneOverhaul.lua`, added 2026-07-28, experimental) —
  closest-fleet-first claim gate on repair/clean work + idle-drone moonlighting for
  saturated neighbor hubs + `SMRFixPack.DroneReport()` telemetry. Stat dials and the
  structural choice are an open decision (DRONE_OVERHAUL_OPTIONS.md), gated on the
  B2 re-run with the v2 stress harness.
- **CohortHousing** (D07, `Code/Opt_CohortHousing.lua`, added 2026-07-28) — Seniors and
  Children in normal housing auto-move into free Retirement Home / Nursery slots (own
  dome first, reachable dome second); employed Seniors exempt, player orders win,
  quarantine/closed domes respected. PT-53 3-of-5 PASS; A/E halves owed.

## Parked by decision, not by effort — one entry left open (F48)

Each has a full write-up on its BUGS.md entry. None was parked for effort; each was parked
because the remedy is not a defect repair, or because the shipped code no longer matches
the tracker. **Only F48 is still open** — the other four are closed.

| ID | Why it is parked | What would unblock it |
|----|------------------|------------------------|
| **F56** | ~~blocked~~ **CLOSED `wontfix` 2026-07-26 (user decision), same grounds as F62/F63.** Screened in the wave-4 build leg: the cited code is designed scope (`GetAutoGatherDeposits` is a declared accessor; the `Automation_Unload` rocket exclusion goes through the Relaunched `IsRocketClass` shim, i.e. maintained intent; auto mode promises only "gather resources"). **No standalone opt-in** — if revisited it belongs in `Opt_ClassicRockets` beside D01's unwritten export half, never in an `Opt_AutoRocketOffload` of its own. | — done. Rides on whatever design decision D01's export half gets, or stays closed. |
| **F32** | ~~blocked~~ **CLOSED `wontfix` 2026-07-26 (user decision).** The shipped data already carries the fix (`NotWorkingBuildings` is now `Suppressable`); the other two presets are one-shot adds. The residual by-design annoyance (2-real-minute window, per-category suppression, no per-building ack) is spun out as **D02** — a planned `Opt_AcknowledgedWarnings` module, gated on **PT-38**; MOD_DESCRIPTION carries a player-facing "looks like a bug, isn't" explainer. | — done. D02 build belongs to a wave-4+ leg after PT-38. |
| **F42** | **NEW, wave-5 screening.** `blocked` — wontfix candidate. The tracked observation is entirely correct and does not add up to a defect: the guard it names exists to stop units being entombed, a dust devil has no footprint to be entombed in, the omission sits in declared overridable class members, no shipped text promises the block, and the game's one weather-gated placement rule (`RocketLandingDustStorm`) is implemented and working. Full write-up on the entry. | **A user decision.** Recommend `wontfix` on the F56/F62/F63 grounds. |
| **F48** | Mechanism confirmed, but the corrected call runs `OrderTrackElements`, which clears and rebuilds `el.connections` and rewrites `node_idx` on **every element of every track**, with a non-unwinding `assert` as its only failure handling. Too invasive to ship untested for a P3. | **PT-37** (added 2026-07-26) — exact console steps for the healthy-network + meteor-damaged-track test, on the user's in-person list. PASS → sanitizer behind a one-shot flag; FAIL → `wontfix`. |
| **F24** | **CLOSED `wontfix` 2026-07-30 (user decision) — fix DELETED.** Real defect (water grid passes `dome` where its electricity twin passes `self`), but **unreachable in the shipped game**: its only live call site can't reach the buggy line (`SpireBase` is not a life-support object), and the `Dome:OnLoad` sweep needs a state vanilla can't produce — domes refuse to place over buildings, no dome has an upgrade, interior shapes never change at runtime. Carried as a 34-line full-function replacement, so deletion beat latency. Counts 75→74 / 69→68. | — done. Rollback is one `git revert` if a counter-example appears. |
| **F49(c)** | **CLOSED `wontfix` 2026-07-30 (user decision) — guard REMOVED. It was fixing DESIGNED BEHAVIOUR**, a different and worse failure mode than F24's unreachable-but-real defect. Established at the keyboard: salvage mode targets objects not hexes, the cursor always names its target (red `Salvage` = no action permitted), the `Salvage Train Station`→`Salvage Track` handoff is seamless to the millimetre, and **no exposed control separates a station from its own connector track**. The propagation the item called a defect is what makes that boundary continuous; the guard would have carved a dead band into it. The module keeps (a) and (d) — counts unchanged. | — done. The reachability audit rated (c) "live R2" **without ever enumerating it**, and its R1-R4 vocabulary cannot express "reachable, but intended" — both ANSWERED in the audit's own "Challenge review 2026-07-30": new tier `I` — Intentional — with (c) reassigned to it. |
| **F28** | **CLOSED `wontfix` 2026-07-30 — barred by the new FIX_POLICY §4a hard rule.** Real defect, but `Research:ReplaceTech` has **zero callers in all of Src** — only mod code or the console can reach it, and it shipped as a §1.5 full replacement (37-line body copy) carrying per-update re-verification cost forever. Not an oversight: the entry said "No vanilla caller" the day it was filed and shipped anyway on a "modder benefit" rationale, which §4a now bars. Fix **and its probe** deleted; counts 74→73 / 68→67, probes 77→76. | — done. Rollback is one `git revert`. Optional later: rebuild the probe as a vanilla canary on the F10 precedent. |
| **F62** | ~~blocked~~ **CLOSED `wontfix` 2026-07-26 (user decision).** Verified identical to the original game (same one-hop algorithm, same two transitive-predicate callers): carried-forward dev vision in both games, breaks nothing. No opt-in module planned. | — done. |
| **F63** | ~~blocked~~ **CLOSED `wontfix` 2026-07-26 (user decision), same grounds** — no training term ever existed in either game's emigration score. | — done. |

Recorded on those entries but deliberately untouched (real inconsistencies, no action):
walkability says A↔C is walkable while services say C is invisible from A;
`CanWorkTrainHereDomeCheck` permits training at a train-reachable school that
`ChooseTraining` never offers; the `PlanetaryAsteroidVisitPossible` legacy branch's
`and`/`or` precedence slip; `IsDifferentAsteroidLocation` comparing a map to a
MapDescriptor. All are permissive failures — none blocks a player.

## Key technical facts — MOVED

The engine-facts section that lived here is now **docs/agent/ENGINE_FACTS.md** (sole
authoritative home; moved verbatim 2026-07-29, audit remediation 3.2).

## Waiting on the user

1. DONE 2026-07-25/26 — retail A/B pairs clean AND the MarsDebug [install] pass is
   complete (49 PASS / 0 FAIL, F73 fully verified — see the QA session leg in
   SESSION_LOG.md).
   **Automated + attended probe coverage is now 100%**; ~~nothing further is owed
   to the harness~~ — **corrected 2026-07-31: that "100%" covers the cold-boot
   path only. The enable path (player ticks the mod at the main menu) has never
   been measured and is where F87 lived.** ✅ **RAN 2026-07-31 19.09 and
   PASSED** — see the A/B table. A second leg with the optional modules forced
   ON covers the five `Opt_` probes on that path. All that remains otherwise is
   the human playtest.
2. DONE 2026-07-26 — author set to **catt144** in both mods' metadata.lua.
3. For the save-failure lead: logs from `%AppData%\Surviving Mars Relaunched\logs`
   and Ctrl+F1 reports from affected players would pin it.
4. An in-game observation for F55: do drones still enter a dome after the roof is
   opened? The Lua half of that report turned out not to be actionable (see the
   F55 entry) — only play can tell us whether the entity data is at fault.
5. Manual playtest per `docs/PLAYTEST_CHECKLIST.md` (**recounted 2026-08-01:
   17 PT sections carried, of which 2 are not runnable — PT-52 frozen, PT-54
   retired — so 15 live, plus the §6 needs-eyes riders**; the previous "35"
   predates the archive sweeps; no third-party mods;
   covers what scripts can't: feel, visuals, UI, long-running behavior). Results
   reported back flip each covered fix's BUGS.md status to `tested` — see that
   file's "Reporting protocol" section for the exact follow-up workflow.
6. **All decisions made (2026-07-26).** F32 closed `wontfix` → D02 filed (planned
   `Opt_AcknowledgedWarnings`, gated on PT-38); F62/F63 closed `wontfix` (carried-forward
   design in both games, user decision); F10 retirement STAGED (46 modules / 45 active,
   final `wontfix` gated on PT-36; rollback is one metadata line); F48 rides on PT-37;
   TestKit stays local-only. Nothing is blocked on a decision anymore — only on play.
8. ~~TestKit remote~~ **DECIDED 2026-07-26: local-only, by design.** The kit was never
   meant to ship publicly, so no remote is created. Note the consequence: the repo's
   51 commits exist in exactly one place — if a local backup is ever wanted,
   `git -C C:\Dev\SMR-BugFixPack-TestKit bundle create <somewhere-else>\testkit.bundle --all`
   is the one-liner (a bundle is a single file that `git clone` accepts).
7. A donated save that researched **Frictionless Composites before the game patched the
   tech** is the only true fixture for the F35 sanitizer pass (PT-35 case C). Everything
   else about that pass is probe-covered.
10. **~~OPEN (2026-07-29)~~ — CLOSED: the F81/F78 disaster fix scope decision was
   made and built on 2026-07-29** (both open questions answered by the QA
   review, watchdog chosen over the full replacement; label corrected
   2026-08-01, the resolution was already recorded in this item's own closing
   parenthetical). Kept for the reasoning. F81 is
   CONFIRMED LIVE and the leak is unconditional (every completed meteor storm
   strands the flag and kills that colony's weather). Proposed package:
   (a) replace the global `MeteorsDisaster` with a **per-invocation** bounded
   drain loop + guaranteed notification removal on every exit path; (b) a
   one-shot `OnMsg.LoadGame` reconciliation clearing stranded predicted flags,
   which is what heals saves already poisoned; (c) a bounded `WaitMsg` in
   `RainsDisasterLoop`. **Gated on the `QA_REVIEW_PROMPT.md` review** — the open
   danger is how to distinguish a stranded flag from a legitimate warning in (b)
   without suppressing a real disaster warning, plus whether a watchdog (F02
   precedent) beats a full-body replacement that rots on game patches.
   *(Review since fired and both questions answered: `FindNotification` +
   Dismissable=false makes the stranded/legit test sound, and the watchdog DID
   beat the replacement — wave 6 built 2026-07-29 late; ~~PT-54 gates it~~ →
   PT-54 RETIRED unrun 2026-08-01, the F86 Tier-1 build legs gate it.)*
11. **OPEN (2026-07-29): D08 — the extender overhaul**, five layers speced in
   `DRONE_OVERHAUL_OPTIONS.md` with a risk table. Recommended order is
   dispatcher → Command Center tab + advisory → cluster scoping → adjustable
   radius → building (last, gated on PT-20). Also gated on the QA review.
9. **~~OPEN: the F79 decision~~ — CLOSED `wontfix` 2026-07-31 (owner).** Trains
   never carry service seekers; the gap is real but feature-completion was
   DECLINED — risk of new issues exceeds the benefit, especially on a large
   multi-stop end-game map. Two facts on file back it: F80 (the train boarding
   layer has an open, unexplained defect) and the fix sketch's post-wrap on
   `Dome:GetService`, a hot path whose added station walk scales with exactly
   that map shape. **Not parked, not owed.** If ever revisited, F80 must be
   explained and closed first. Full reasoning on the F79 entry.

## Save-rescue expectations (for release messaging + sanitizer design)

~60% of fixes help broken saves IMMEDIATELY (behavioral code re-evaluated every
tick/cycle: drones, colonists, schedulers — F02 pattern of thread-restart on
LoadGame where needed). ~25% need active repair; those passes now ship — eight in
their own fix files plus F03 and F35 in `Code/90_SaveSanitizer.lua`. Only F48
remains queued, and it is blocked on an in-game test (see the blocked table). ~15% is irreversible history (dead colonists,
lost expeditions; F64 voided trains have no recorded count — heuristic
compensation option at best, and document the vanilla train re-purchase at
stations, Station.lua:573-611). Save rescue is the headline differentiator vs
official patches ("new games only") — lead with it.

## Distribution facts (researched 2026-07-25, source-verified)

- BOTH Steam Workshop AND Paradox Mods are supported; the in-game Mod Editor has
  upload buttons for each (ModEditor.lua:78/:115). Steam Workshop reaches PC
  only; **Paradox Mods is the only channel that reaches Xbox/PS5** — platform
  fan-out is automatic on the backend, no platform fields, no modder-side
  signing (PS5 signatures are created client-side at install, Mod.lua:49-95).
  Console loads packed Lua code mods fine; no engine restriction found.
- PDX upload hard-requires: title, short_description (≤200 chars), description,
  preview image, lua_revision; last_changes on every update; ≤10 tags
  (ParadoxMods.lua:13-54, Mod.lua:410). GitHub repo link goes in metadata
  `external_links` — "github" is a supported LinkType shown on the PDX portal
  (Mod.lua:180-201). Default ignore_files already excludes *.git/*.
- Public repo: github.com/catt144/SMR-CommunityFixPack (main). Commit identity
  is the GitHub noreply address — never commit with a real email again.
- **CORRECTED 2026-07-26 (user unlocked one in play):** achievements are NOT
  disabled by mods on PC/Steam. `DoModsBlockAchievements()` returns
  `Platform.playstation or Platform.xbox or Platform.windows_store`
  (Achievement.lua:61-63) — the ModManager.lua:78 string is warning TEXT shown
  only behind that gate. Mods block achievements on console/MS Store ONLY.
  Separately, cheat use is logged per save (`LogCheatUsed` → persisted
  `CheatsUsed`, Network.lua:241-255) and adds "cheats used" to the
  unlock-refusal reasons on retail — so cheated fixture saves self-block their
  achievements. Mod description: say achievements keep working on PC, are
  disabled on consoles.

## Release checklist (when fixes are tested)

Real author + version bump in metadata.lua; player-facing fix list in README +
mod description; upload via in-game Mod Editor (check docs/.git exclusion; the
Test Kit must NOT be uploaded); credit ChoGGi (Fix Bugs) + LukeH (Martian
Express) as prior art; keep per-fix disable instructions in the description.
Four `[DRAFT NOTE]` markers remain in `MOD_DESCRIPTION.md` (lines ~6, ~90 F76 explainer, ~390 ClassicRockets export half, ~448 final) and are
deleted before the text ships. The export-half one is load-bearing: do NOT promise the
ClassicRockets module's unwritten Rare Metals export half.
