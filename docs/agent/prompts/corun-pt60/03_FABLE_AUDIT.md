# Chain prompt 3 — adversarial audit, integration, chain close

**Read `README.md` first — binding chain rules apply. You are the terminal
prompt: this folder must be EMPTY when you finish.** Staleness check, todo
list. Precedents set the floor: corun-pt15's audit (SESSION_LOG 2026-08-11 —
log byte-compared over the FULL length and read whole, every conclusion
re-derived from the logged numbers, one integration gap found and filled) and
its C46 sequel (SESSION_LOG 2026-08-12 — the audited state must be shown
ORGANICALLY CONSTRUCTIBLE before harm is claimed).

**Every "done", "PASS", "SKIP", verdict and owner quote upstream is a claim.**

## Jobs

**Job 1 — audit the record.** Byte-compare every archived log against its
on-disk original over the FULL length; read the whole sitting log. Then:

* **Per-prediction re-derivation.** For each of P1–P9, recompute the verdict
  from the archived log's own lines — never from the sitting's summary. Counts
  recounted (registered/active, probe verdicts), the three P8 heal lines
  grepped by exact wording over the whole file (⚠️ boot-time preset heals fire
  every launch — do not count them as save-state heals; prep's annotation
  names which is which), P9's read located, and absence claims settled HERE
  (EF-047 — the sitting's absence reads were provisional by design).
  **A prediction that missed is a finding — chase its mechanism before
  filing; the 08-02 set's own P1 miss was count-arithmetic, not a defect.**
* **Status honesty.** F90/F91/F94/F96 and the eight conversions move only to
  what the archived log supports; execution evidence is named per module
  ("applied + N hours error-free + probe verdict"), never "verified"
  unqualified. F92/F93/F95 stay `tested` — this leg neither adds nor subtracts
  from grants it did not test. Any `tested` grant from this sitting quotes the
  owner VERBATIM from the log (corun-pt15 rule 3); a transcript-only quote is
  ruled on explicitly, never assumed either way. Heading tags and index rows
  agree; the checklist PT-60 section states its final state (archive-ready or
  what remains).
* **Riders.** Each rider taken: audit its reading like a leg. Each rider
  skipped: confirm the gate read that skipped it is in the log (a skip without
  its read is a hole, not a skip).
* **Whole-log sweep:** F99 `TrackElement.lua:805` (an ORGANIC hit reopens F99
  — route it) · C45 `invalid pos with no holder` (record per entry) ·
  unexplained lines verbatim with age · cheat markers vs the disclosed count.
  ⛔ A missing archived log is an automatic finding.
* **Save-dir close-out under rule 12 (Steam Cloud ON):** the listing is BY
  NAME; deleted staged saves are recorded "deleted, listing verified" — if a
  prior deletion has already resurfaced, attribute it to EF-051's mechanism
  (owner-armed 2026-08-12), add it to the post-untick cleanup inventory, and
  do NOT file it as a finding. Byte-verify the FOUR protected files, including
  **`USA Sol 302`** — the owner's campaign save must be untouched to the byte.

**Job 2 — the ledger.** Sitting misses vs the standing harness-rule stacks
(u1 1–4, b1 1–6, b2 1–9 as amended, corun-pt15 1–3): recurred (a rule failing
twice is broken — repair it in WORKFLOW surgically) vs NEW. Owner-time
honesty: promised **~40–60 min** vs actual, owner-directed deviation separated
from rig misses (only the owner rules their own time out of scope).
Economics one line.

**Job 3 — integrate and close.** Entries carry their verdicts; checklist
final (a fully-passed PT-60 moves WHOLE to `PLAYTEST_ARCHIVE.md` with a group
banner, per the house rule); STATE chain CLOSED + outcomes + NEXT (cap 60);
SESSION_LOG record newest-first; CHAIN_METHOD one row ONLY if this chain
taught the method something new. Delete every remaining file in this folder in
the closing commit (cite the pre-deletion sha in the SESSION_LOG record).
doccheck GREEN, push. **The owner report ENDS with the next kickoff**
(rule 14): expected front is the **`unattended-3` build chain** (F85
`dont_pause` flip + C39 compensation + the three-automation-label sweep,
verified on a `CP15PT15` staged copy) — **its chain is not authored**; say so
and name what authoring takes. The PT-20 redo co-run queues behind it.
⚠️ If the owner has reported flipping Steam Cloud OFF by the time you run,
route the EF-051 post-untick cleanup + re-verification as a named task in the
report; if not, restate the rule-12 hold so the next chain inherits it.

## Stop conditions

- A load-bearing verdict fails audit and the logs cannot settle it →
  correct visibly, re-route to the owner, keep closing.
- The sitting was partial → audit what ran, inventory the remainder as
  TAKEABLE riders, still empty the folder.

## ⛔ What you may not claim

- Not `tested` without the owner's verbatim verdict on that reading.
- Not "the batch is verified" beyond the quoted, re-derived numbers; P6/P7
  cover this sitting's executed paths only.
- Not F90/F93/F96's live halves from quiet weather.
- Not "gone" for any deleted save while Steam Cloud is ON.
- Not a new defect from a returning stray — that is EF-051, owner-armed.

---

# Notes from upstream — chain prompt 2 (the sitting), 2026-08-12

**Everything below is a claim until re-derived (rule 5).** The log is
`docs/archive/cp60sitting_Mars.exe-20260812-13.38.15.log` — **1,082 lines,
116,417 bytes, MD5 `2642D7FC4CA7DD3AEB1323B96B11DC6D`**, copied from
`AppData\Roaming\Surviving Mars Relaunched\logs\Mars.exe-20260812-13.38.15-6a22b86d.log`
and MD5-verified identical at archive time. Process exited cleanly
(`Stopping the game threads from the Lua side with exit code 0`, `:1069`).
⚠️ Line numbers below are from the archived file; **`say()` prints each line 2–3×**
(ModLog + print + ConsolePrint), so a cited number is the first of a run.

## 0. Run conditions, as READ

| item | value |
|---|---|
| launch | 13:38:15, retail, both mods loaded (`:58-59`); `[SMRTest] no debug.getinfo (mod sandbox)` — retail sandbox confirmed |
| pack | **`81/81` active** at the opening gate (`:290`), at P1 (`:575`) and at close (`:1037`) — the every-opt-in-ON branch, READ not assumed |
| ⚠️ **build staleness** | **`5a1508b` (F102 `Fix_ExoticDepositSign`) landed 13:50:35 — 12 min AFTER this launch.** `ExoticDepositSign` has **0 hits** in the log, so the process never loaded it. **The sitting's `81/81` is correct for the running build; the tree is now 82 registered / 83 files.** ⛔ Do not read the difference as a module failing |
| fixture | `CP60STAGE.savegame.sav`, byte copy of `USA Sol 302` (MD5 `2E1B12FCF48905EC6A725DE7862B00A6`), loaded BY FILENAME as `LOAD OK #1` (`:357`) |
| fixture lineage, CONFIRMED BY READ | `UIColony.day=303`, `GameTime 302.19 sols`, map `BlankBigCanyonCMix_09`, `10 dome(s), 1246 colonist(s)`, `mystery=false` (`:380-389`) — prep's claim that this is the owner's pre-batch campaign is now a reading |
| ⭐ commander profile | **`rocketscientist`** (`:333` engine dump, `:380` live read) — decides P8's branch |
| loads | 2 by the harness (`loads_this_process=2`); **plus one in-game list load before them** — see §5 deviation 1 |
| colony advanced | Sol 303 → **314** (`CLOCK close :: UIColony.day=314`, `:1058`) |
| speeds | 0 → 3× after each load (`:367`, `:944`); `speed=1` at close |

## 1. Per-prediction verdicts — recompute all of these from the log

| # | verdict | key lines | notes for the audit |
|---|---|---|---|
| **P1** | ⭐ **HIT, both halves** | `:575` `registered=81 … active=81` | registered was PREDICTED (81, from metadata's code list), active was READ. All 8 `OPTIONAL:` ids read `active` (`:557-564`), which is the independent witness for the 81/81 branch |
| **P2** | ⭐ **HIT** | `:578-590`, `:593` | five new modules `active`, **detail empty on all five**, `5/5 APPLICABLE=true`. ⚠️ **`:163` says `SaintBlessing: inactive (no dome-colonists trait presets)` — a first-pass boot artifact that resolved** (same shape as `NoHomeless` `:158-159` → `:185`). ⛔ **A grep for `inactive` in this log files a FALSE P2 miss**; the registry read is the authority. Prep's worry that `AstrogeologistExtractors` might latch `"benign"` did not fire |
| **P3** | ⭐ **HIT** | `:596-614`, `:617` | all seven conversion modules `active`, empty detail, `7/7` (eight conversions — `SequenceLatents` holds F29 items 1 and 3) |
| **P4** | ⭐ **HIT, 7/7 PASS** | `:816-830` | `TrackShellLeak` · `SaintBlessing` (**"all 10 dome Saint(s)"** — 15 on 08-11; count is save-dependent as prep predicted, and **10 matches the fixture's own two independent reads**) · `DustDevilsDescrMap` · `AsteroidVisitPrecedence` · `AstrogeologistExtractors` (12/12, preset-level) · `SinkholeIndestructible` (0 instances — `sinkholes=0`) · `DustStormBreakMapFilter` |
| **P5** | ⭐ **HIT, no regression** | `:739`, `:683`, `:620-627` | `AsteroidLanderAvailable` **PASS**, message byte-identical to the 08-11 baseline; its immunity re-derived from source (stubs `IsKindOf` true only for `UniversalRocketBase`, so all five cases take the first branch). `TrackSalvageWipe` **SKIP `[install]`** — ⛔ not coverage. Both amended-in-place ids still `active`, empty detail |
| | suite tally | `:848`, `:854` | **`77 PASS, 0 FAIL, 10 SKIP, 0 ERROR`** — identical to the 08-11 retail baseline on a different save. Thread context real (`:641`, `thread: 000001E288F55AE8`), so no silent under-report. **All 10 SKIPs matched BY NAME**: the 8 standing `[install]` (`:649 :658 :668 :681 :683 :686 :688 :711`) + `AnomalyCaveInMap` (`:795`) + `TechDescriptionBuilding` (`:797`) — the same two behaviour SKIPs as 08-11. `CrystalMysteryHang` RAN, as prep derived |
| **P6** | ✅ **ZERO**, settled on the archived file | — | `[LUA ERROR]` **0** · `TrackElement.lua:805` **0** · `invalid pos` **0** · asserts **0**. ⚠️ A naive grep for `LUA-ERROR` returns **3** — all three are the harness's own ERRORWATCH sentence (`:1063-1065`) describing the token. ⛔ Scope: **this session's executed paths only** |
| **P7** | ✅ owner verbatim IN the log | **`:1033`** | *"I have been messing around in game and everything seems normal for most of this sitting"* — spoken after ~50 min of their own play across two loads, mixed speeds. ⚠️ **General, not per-system**: the audit must rule whether that supports P7's named list (night shifts, gene forging, shuttle-hub availability, landscaping picking, upgrade modifiers, sequence latents, rocket refuelling) or only a weaker claim. It was NOT elicited per system |
| **P8** | ⭐⭐ **THE DECIDER, TAKEN — see §2** | `:329` | fired ONCE on the pre-batch save, absent on the reload |
| **P9** | ✅ **negative control held, population 19** | `:1003-1022` | `0 carriers | population=19 | APPLICABLE=true`. ⛔ Non-discriminating by construction (prep's Src derivation) — never "the field-removal half ran". ⭐ Side effect: the mix-in walk question is ANSWERED → **EF-053** |

## 2. P8 in full — the one reading only a pre-2026-08-02 save could give

**Settled from the ARCHIVED file, so these are no longer provisional (EF-047):**

| # | heal line | occurrences | real hits | verdict |
|---|---|---|---|---|
| 1 | `TrackSalvageWipe: deleted %d invisible track shell(s) …` | 6 | **0** | correct — `shells=0` of **7 `TrackBase`** walked (`:440`, `APPLICABLE=true`). A CONTROLLED zero, guarded on `shells > 0` |
| 2 | `SaintBlessing: re-based %d dome blessing(s) …` | 7 | ⭐ **1, line 329, load 1 only** | **at most one line each** HELD; **no repeat on load 2** HELD |
| 3 | `AstrogeologistExtractors: applied %d … bonus(es) …` | 6 | **0** | correct BY DESIGN — `rocketscientist`, heal returns early (`:174-178` of the module). Population 0 ⇒ ⛔ **non-discriminating, not a pass** |
| 4 | `duplicate extractor modifier` (the 08-02 inflation repair) | 0 | **0** | never fired — this save carries no inflation |

⚠️ **Every non-zero count above except line 329 is the harness's own "grep for, verbatim"
reminder line** (`:467-469`, `:988-990`), which quotes all three strings. **Re-derive this
before trusting it** — it is exactly the shape that produces a false reading.

⛔⛔ **THE TRAP HELD, and the log now contains the control:** the two boot-time preset
patches fired **exactly once each, at `:174` and `:178`, `Lua 0:00:18–19`, nine minutes
before any save loaded** — `added 2 missing extractor entr(y/ies) … (10 already present)`
and `corrected 1 dome-colonists trait modifier label(s) of 2`. Different wording, different
timestamp, wrong side of the load boundary. **Counting either as a save heal gets P8 wrong
in the direction that looks like a pass.**

**R7 effect reads, load 1 → load 2:**

| reading | after load 1 | after load 2 |
|---|---|---|
| F91 shells / `TrackBase` | `0 / 7` (`:440`) | `0 / 7` (`:961`) |
| F92 dome Saints / carrying `TraitReligious` | **`10 / 10`** (`:447-450`) | **`10 / 10`** (`:968-971`) — ⭐ the re-base PERSISTED (R4) |
| F95 `label_modifiers` (4 labels) | `2 / 0 / 4 / 2` (`:453-462`) | `2 / 0 / 4 / 2` (`:974-983`) |

⛔ **A correction the sitting made on itself, and the audit must keep it:** the F95
no-growth reading is **ALSO non-discriminating**. The identity-keyed regression lives inside
the heal, and the heal returns early on a non-astrogeologist colony — so nothing could grow
either way. The sitting first called it a discriminating control and retracted that in the
same session. What the four counts DO establish: the query works (`MetalsExtractor=4`,
`WaterExtractor=2` are vanilla's positive control) and vanilla's baseline is round-trip
stable. ⚠️ **`AutomaticMetalsExtractor=2` is NOT the regression** — the harness line saying
*"2 is the identity-keyed regression"* assumes an astrogeologist colony and misleads here.

⇒ **Still owed:** the F95 save-heal + idempotence read on an **astrogeologist** colony
predating 2026-08-02. No such fixture is known to exist. Recorded on F95.

## 3. Findings the leg was NOT looking for — all four need auditing as findings

1. ⭐ **F48's sanitizer repaired 3 of 7 tracks in the owner's own campaign, and the repair
   PERSISTED** (`:342-348`; zero repair lines on load 2). Organic state, `0 raised`. First
   R4-class evidence for that pass on an unhealed real save. Recorded on F48.
2. ⭐⭐ **F34(d)'s route documentation was wrong in three places**, found because the owner
   challenged the rider twice with screenshots. Re-derived from Src: **the RC Commander
   (`RCRover:DroneEnter`, `:275`) is the ONE live route**; the **rocket route is UNREACHABLE**
   (a rocket is a `Building` and obstructs the mark — `ObstructorsQuery.classes = {"Building"}`,
   `Construction.lua:1448`, while every `Unit` carries `DoesNotObstructConstruction`,
   `Unit.lua:3`); **RC Transport sets `Embark` nowhere**; **no train or shuttle sets it at
   all**, though the module header claims both; and the registered title says **colonists**
   when only drones are involved. ⛔ **That title is user-facing and `MOD_DESCRIPTION.md` is
   rebuilt from these at launch prep — fix it there.** Then the owner staged the exact window
   (drones mid-`Embark`, new flatten placed over them) and **20/20 boarded, no
   `ExitImpassable`, no error** — closing the "unobserved in play" gap open since 2026-07-30.
   ⚠️ Their ~2 s freeze is **attributed, not proven** (fits `RebuildPassability`, not the
   defect's `SetCommand("ExitImpassable")`); no A/B was available. Full record on F34.
3. ⭐ **EF-053** — `AllMapsForEach` works on a mix-in parent: `DroneControl` walked **19**
   while the three concrete classes walked **13**, so the base walk finds MORE. ⚠️ Same read:
   **`RocketBase` walked 0 while `labels.AllRockets` held 6** — a silent-zero hazard for any
   future rocket leg.
4. ⚠️⚠️ **THE RIG HAS CHEATS ENABLED** (owner, in-session: *"the RC Commander infopanel is
   exposed for me I have the cheats enabled, I did not use them on the rc command during
   this test"*). `PLAYTEST_HELP` asserts cheats do not exist on retail. **UNVERIFIED and
   routed here**, two consequences: (a) **external validity** — every "on retail, X" claim
   this project holds was measured on a cheats-enabled build, and assert gating could change
   what lands in an error log; (b) **capability** — object infopanels expose `Inspect` and
   `Properties`, which could let future legs read fields by CLICK instead of console typing.
   That directly attacks the owner-time cost this whole model exists to reduce. **Worth a
   targeted check before the next co-run designs its instruments.**

## 4. Riders — one taken, four skipped, every skip carrying its gate read

Gate reads, all from `:418`: `elevators=0 | passages=5 | trains=5 + tracks=7 | rockets=6 | sinkholes=0`.

* ✅ **F34(d) TAKEN** (FORCED, owner's hands) — §3 item 2. Precondition `rockets=6` is what
  permitted the offer; the *route* turned out not to involve rockets at all.
* ⛔ **F90 NOT OFFERED — `elevators=0`.** No elevator ⇒ no cross-map merged fragment; the
  live half is unreachable on this save regardless of weather. Nothing forced.
* ⛔ **F96 R2 NOT OFFERED — `sinkholes=0`** and `mystery=false`.
* ⛔ **C42 NOT TAKEN — instrument, not precondition.** `passages=5` satisfies presence, but
  the open gap is a **traversal witness**, which needs a hook or logger, i.e. TestKit code —
  **Out** by this chain's scope fence. No C42 leg was armed. ⚠️ Route it: C42 has now been
  "unsampled" three times, and each attempt failed for the same reason.
* ⛔ **F21 NOT TAKEN — same class.** Its two reads (`spent_time_sum`/`spent_time_values`,
  `transport_ticket.start_wait` restamp) have no leg in the armed harness. `trains=5 +
  tracks=7` recorded as the gate read that would have permitted it.

## 5. Ledger — misses, and which are NEW vs RECURRING

1. ⚠️ **NEW, and it is a brief defect: the brief's console order was unrunnable as written.**
   It opens at the main menu, but the kit's own boot line says the console only comes up
   *"once in a colony"* (`:240`). The sitting inferred "no console at the main menu" and
   spent an extra in-game-list load of `CP15PT15` (~2 min of owner time) to reach one. ⛔
   **That inference was WRONG in one direction and the log proves it**: `CP60.Menu()` executed
   at the main menu at `Lua 0:02:57` (`:202`) and reached the log — only the **on-screen echo**
   was missing, because `ConsolePrint` had no UI. There is also a `not understood` at
   `Lua 0:02:44` (`:200`), one rejected line. **Repair for the next brief: state that
   main-menu console input EXECUTES but does not display, so the operator must not judge by
   the screen.** ⭐ The wasted load was not wasted evidence — loading post-batch `CP15PT15`
   produced **zero** save-state heal lines, an accidental negative control that separates
   fixture heals from background noise.
2. ⚠️ **NEW: the harness's F95 line editorialises wrongly on a non-astro colony** ("2 is the
   identity-keyed regression"). Fix in the parked source if it is ever resurrected.
3. ⚠️ **NEW: `CP60.Fixture` reads `UIColony.sponsor`, which is a dead read** (`sponsor=nil`,
   `:380`, while the engine's own dump says `sponsor: NASA`). No consequence; wrong field.
4. ⚠️ **NEW: `RocketBase` is not the placed rocket class** (§3 item 3) — a walk-target trap.
5. ⚠️ **RECURRING (b2 rule class): the cheat-disclosure ask.** Six `ObjCheat CheatFill`
   (`:867-877`) were flagged and the owner had to justify them. **The owner ruled it a
   standing condition** — playtest colonies are oversized/underindustrialized and cheats are
   life support. ⇒ **WORKFLOW now carries a binding rule** (new section, "Cheats on playtest
   saves are the NORMAL condition"): expect the markers, attribute rather than excuse, **ask
   ONCE**, a cheat is a confound only where a reading intersects what it changed (named:
   NONE here), and a no-cheat leg must be declared in its brief with a prepped
   resource-rich save. Disclosure verbatim at `:903`. Checklist item 13 records the ruling.
6. ✅ **No harness resolution defect, no self-drive, no unarmed launch.** ARM GATE GREEN on
   every clause including the brief cross-check; DISARM GATE GREEN; `PROBE SWEEP: clean`
   after disarm.

**Owner-time honesty. Promised ~40–60 min. Actual ~95 min** (13:38 launch → 15:15 quit).
Split, and only the owner may rule their own time out of scope:

* **Ours (~10 min):** the console-order defect above (~2 min), and a long tail of agent-side
  source derivation the owner waited through while F34's reachability was settled.
* **Owner-directed (~45 min, NOT scored against them):** three substantive challenges (the
  trains scope question, the F34 rocket-zone challenge, the F34 transport challenge) and two
  staged F34 attempts. **All three challenges changed the record** — the trains ask became
  checklist item 12, and the other two rewrote F34's route documentation. This is the
  highest-value owner time in the chain and it should not read as overrun.
* **The measurement legs themselves ran to plan** — ⓪①②③ took roughly the briefed budget.

**Economics:** one attended sitting bought the P8 decider (unrepeatable — it needed a save
predating the batch), a full P1–P5 confirm, four unplanned findings, one new engine fact,
one binding WORKFLOW rule, and two owner decisions surfaced.

## 6. What the sitting did NOT do — pick these up or rule them unnecessary

* ⛔ **Per-entry conversion evidence is NOT written for all eight conversions.** The reading
  is identical for every one (module `active` + empty detail + 0 errors + owner's general P7
  sentence) and lives in the log; only F34/F48/F57/F90/F91/F92/F94/F95/F96 got entry
  sections. **Either write the eight one-liners or rule the shared record sufficient.**
* ⛔ **No `SESSION_LOG.md` record was written** — left to this prompt, which owns the
  newest-first record and the pre-deletion sha.
* ⛔ **The checklist has no PT-60 results section yet** (items 12 and 13 are in, the leg
  banner is not). Job 3 owns its final state.
* **`CP60RT.savegame.sav` may still exist** — it was HELD, not deleted, because the owner's
  ~11 sols of play live in it and the two autosaves that also hold them (`Autosave Sol 306`,
  `Autosave Sol 311`) rotate out within two launches. `CP60STAGE` IS deleted (listing
  verified, 83 → 82 files). Confirm the current state BY NAME and finish the deletion if the
  owner has released it.
* **Four protected files byte-verified UNCHANGED at close:** `USA Sol 302`
  `2E1B12FCF48905EC6A725DE7862B00A6` · `TEST2H TRAIN` `103B320A1434513BC8773553096A8958` ·
  `PT35FIXTURE` `D721329D1EE18604B3D6C89401F74738` · `PT-15`
  `5D0D81A3D66CA7BABFCA85D6AC118C06`. **The owner's campaign save was never written to.**
* **Unexplained lines, verbatim, with age — none attributed to the pack:**
  `:187-198` six `[Braze]` telemetry failures (*"The server name or address could not be
  resolved"*, boot, ~96 min before quit — offline analytics) · `:200` `not understood` (the
  rejected console line, §5.1) · `:235-236` `[ResManager Error] Cannot find file with base
  path: Animations/LawOfficeDoor_idle.hgacl` / `_opening.hgacl` (`Lua 0:04:48`, during the
  first asset reload, ~70 min before quit — a **vanilla/DLC asset gap**, not ours).
  ⚠️ Attribution is not dismissal (WORKFLOW log-review rule): the `LawOfficeDoor` pair is a
  real missing-asset bug in the shipped game and is unrecorded anywhere in our tree.
