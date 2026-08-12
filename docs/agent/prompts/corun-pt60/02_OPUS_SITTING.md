# Chain prompt 2 — the sitting (owner attended, ~40–60 min)

**Read `README.md` first — binding chain rules apply.** Staleness check, todo
list the owner can read to know when to step in. The owner drives the mouse
and types every console line (the rig has no input path into a running game);
you hand lines ONE AT A TIME, pre-flighted, and keep the sent/checked/
outstanding ledger. An owner override is a course change — state the plan's
position once, then follow (WORKFLOW).

**⛔ PT-00 first** (stale-probe sweep, CLEAN or declared), then arm via
`CP60_ARM.ps1` (the ARM GATE refuses an unarmed launch), then launch.

## The leg, in priority order (decider first; a truncated sitting still banks ①–③)

**⓪ Gate + fixture.** `CP60.Load("CP60STAGE.savegame.sav")` → the run-top pack
gate (**STOPS if the pack is not loaded** — any re-enable is handed back to
the owner explicitly). Fixture confirm by READS: map, sol (~302 lineage),
`81/81` module count, CLOCK line. Re-arm any wanted loggers (restart cleared
them). ⚠️ The first load has ALREADY landed the P8 first-load heal lines in
the log buffer at zero owner cost — note the time window; the authoritative
absence/presence read is from the ARCHIVED log after exit (EF-047).

**① P1–P3.** `CP60.Fixes()` — registered/active counts, the five new modules
and seven converted modules' statuses, Note-relayed against prep's annotated
predictions. Read the detail string of anything not `active` before
concluding.

**② P4–P5.** `*r`-prefixed `CP60.Suite()` — the runnable new probes' verdicts
plus the no-regression check on the two at-risk probes prep named. Quote the
header line and per-probe verdicts; do not chase a total (the archive's own
rule).

**③ P8/P9 round trip.** `CP60.SaveNamed("CP60RT")` → `CP60.Load
("CP60RT.savegame.sav")` → P9 read (`CP60.P9()` — the key must be absent after
one load-and-save) → P8 idempotence expectation: none of the three save-state
heal lines repeats on this second load (mid-session = provisional presence
read; the audit settles absence from the archived file). R4 satisfied by
construction — this IS the round trip.

**④ The owner plays, 15–20 minutes, ORGANIC.** Mixed speeds, at least one
of their own saves if they feel like it. Watching for P6 (zero `[LUA ERROR]`
naming the five new files or seven converted modules) and P7 (no visible
behaviour change from the conversions — night shifts, gene forging,
shuttle-hub availability, landscaping sites, upgrade modifiers, sequence
latents, rocket refuelling all feel vanilla). ⚠️ Rule 13: F92/F95 legitimately
move morale/production on this save — do not let anyone read those as drift,
and say so out loud if the owner remarks on either.
**Riders — ONLY if the gate reads their precondition true, never forced:**
F21 (a working train line → the two reads from the entry), F34(d) (owner
stages a landscape mark over a loading rocket — hands + eyes), C42 (passages
demonstrably trafficked → the within-session read BEFORE any further
save/load), F90 (a surface storm arrives on an elevator colony → the
notification watch). Each rider names FORCED vs ORGANIC per reading.

**⑤ Owner verdicts.** At every measure moment, put the question, and relay
the owner's words through `CP60.Note` **the moment they are spoken**
(corun-pt15 rule 3 — a `tested` grant needs the verbatim IN the log). Expected
verdict moments: the suite outcome vs predictions; the play window's "nothing
felt different" (P7 — that sentence, theirs, is the reading); any rider taken.

**⑥ Close-out.** Quit to desktop (flushes the log). Archive the log
(`cmp`-verify + MD5, `git add -f`). Whole-log first pass: 0 `[LUA ERROR]` /
F99 `:805` / C45 `invalid pos`; every unexplained line VERBATIM with its age;
cheat markers counted + owner's reason verbatim if any were used. Save-dir
listing **BY NAME** against expected survivors; delete `CP60STAGE` +
`CP60RT` in the recording commit and record **"deleted, listing verified" —
NEVER "gone" (rule 12: Steam Cloud is ON; they may return at the next launch
and that is EF-051's mechanism, not a failure)**. Byte-verify the FOUR
protected files (`PT-15`, `TEST2H TRAIN`, `PT35FIXTURE`, `USA Sol 302`).
Update entries incrementally (per-prediction readings; F90/F91/F94/F96 +
conversion evidence moves only to what was read; status flips front-matter
AND heading tag, regenerate index). Owner-time honesty: promised vs actual,
deviations separated. doccheck GREEN, commit (`PROBE SWEEP:` line), push.
Append `## Notes from upstream` to `03_FABLE_AUDIT.md` — run conditions as
read, per-prediction verdict table with log line numbers, owner verbatims
(flag any that exist only in the transcript), misses, riders taken/skipped
with the gate reads that decided them. Delete this file in the same commit.

## Stop conditions

- Pack gate fails → STOP the run; hand the re-enable back; bank nothing.
- Fixture confirm fails on the staged copy → try the `USA Sol 298` fallback
  (stage it live, MD5 first); both failing → bank the gate reads, route.
- Any `[LUA ERROR]` naming pack/TestKit code → stop that leg, record
  verbatim, continue independent legs.
- The owner has to leave → ①–③ are the bank; inventory ④'s remainder as
  TAKEABLE riders and close honestly.

## ⛔ What you may not claim

- No `tested` grant without the owner's verbatim verdict relayed through
  `CP60.Note` on that reading — and name what was forced anyway.
- P6/P7 hold only for the paths this sitting executed — say "this session's
  paths", never "the conversions are verified" unqualified.
- Absence claims (no heal repeat, no error) are PROVISIONAL until the audit
  reads the archived file (EF-047).
- Nothing about F90/F93/F96 live halves from quiet weather.
- No "gone" for any deleted save while Steam Cloud is ON.

---

# Notes from upstream — chain prompt 1 (prep), 2026-08-12

**Provenance tags used throughout. Rule 5 binds: everything below is a claim
until re-derived.** `MEASURED` = this session, agent-side, game closed ·
`Src-VERIFIED 08-12` = read this session in
`A:\SteamLibrary\steamapps\common\Project Spark\ModTools\Src` (Relaunched's
installdir is literally `Project Spark`, EF-014) · `MODULE-READ 08-12` = read
this session in `Code/` · `LOG-READ` = read this session from a named archived
log · `INHERITED` = carried from a record and NOT re-derived here.

## ⚠️ 0. Three things that change the plan, read these first

1. **P9 IS DEGRADED — it cannot discriminate on any shipped save.** Derivation
   in the P9 row below. The read is still taken (it is free), but it is a
   **negative control**, not evidence that `8f58f30`'s field-removal ran.
2. **Two pack lines that look like P8 heals are boot-time preset patches that
   fire on EVERY launch, before any save loads.** A grep that counts them as
   save heals gets P8 wrong in the direction that looks like a pass. Both
   wordings are given below with the log lines that prove the class.
3. **The suite half of this leg already has a retail baseline from
   2026-08-11** (`docs/archive/u2run3_Mars.exe-20260811-02.01.06.log`) in which
   all seven new probes PASS. That does **not** retire P4/P5 — that log is a
   different save and P8 needs this fixture — but it means ② is a *confirm*,
   not a discovery, and the owner's scarce minutes belong on ⓪/③/④.

## 1. Fixture — MEASURED 2026-08-12, and what is still a claim

| item | value |
|---|---|
| source | `USA Sol 302.savegame.sav` · **MD5 `2E1B12FCF48905EC6A725DE7862B00A6`** · 54,842,984 bytes · LastWrite **2026-08-01 17:55:48** — matches the chain README exactly |
| staged copy | `CP60STAGE.savegame.sav` · **MD5-identical** · created by `Copy-Item` **2026-08-12 12:52:59** (recorded because a byte copy has the same metadata shape as a Cloud restore — EF-051) |
| fallback | `USA Sol 298.savegame.sav` · MD5 `AC305FA61FE9BADD168C948AB020186D` · 2026-08-01 17:41:58 |
| save directory | `C:\Users\stkot\Saved Games\Surviving Mars Relaunched\76561198020568696` |
| protected #1–#3 re-verified | `TEST2H TRAIN` `103B320A1434513BC8773553096A8958` ✅ · `PT35FIXTURE` `D721329D1EE18604B3D6C89401F74738` ✅ · `PT-15` `5D0D81A3D66CA7BABFCA85D6AC118C06` ✅ — all three unchanged |
| protected #4, from now | **`USA Sol 302.savegame.sav`**, MD5 above |

⛔ **Still a CLAIM, and `CP60.Fixture("after load 1")` is what settles it:** that
this save is the owner's campaign, that the pack was on when it was written, and
that its colony has never seen F90–F96. Prep can read the file; only the sitting
can read the colony. If the confirm fails → stage `USA Sol 298` live (MD5 first)
and re-take P8 there.

### ⚠️ EF-051 fired between the owner's launch today and this prep — attributed, NOT a finding

Chain rule 12 predicted this and it happened. **18 previously-deleted staged
saves were restored**, every one created **2026-08-12 12:29:54–12:30:35** with
its ORIGINAL LastWriteTime preserved. Inventory BY NAME, for the post-untick
cleanup (`steam_autocloud.vdf` rewritten 12:07:05):

`U1C6FORCED` · `U1C2PT35` · `U2RT1` *(extensionless — EF-050's artifact)* ·
`CB2PKEY` · `U1C0PROOF` · `U1C1HEAL` · `U2RT1.savegame.sav` · `U1C6HEALED` ·
`U2RT2` · `CB2F85` · `CB2UNINSTALL` · `U2STAGE` · `CB2PKEY2` · `U1STAGE` ·
`CORUN1` · `CORUN0` · `CB2STAGE` · `CB1STAGE`.

This is EF-051's measured mechanism working, owner-armed. **Do not file it.**
`TEST2 AST.savegame.sav` (created 12:10:50, written 12:15:15) is the owner's own
save from today's session, not a stray.

## 2. THE ANNOTATED PREDICTION SET — 08-02 wording is the record, the annotation is prep's

### P1 — registered/active counts

> *08-02, as corrected mid-leg:* predict the **registered** count; **read**
> `CurrentModOptions`/`ListFixes()` for active, never the defaults.

* **Predict registered = `81`.** Derivation: `python tools/doccheck.py
  --emit-counts` 2026-08-12 → *81 registered (74 default-active, 8
  optional-gated files), 82 `Code/*.lua`, 87 probes*. Not from defaults.
* **READ active.** The owner's campaign profile has run **every opt-in ON**:
  `81/81` LOG-READ on 2026-08-03 (`PLAYTEST_HELP`) and again on 2026-08-11
  (`u2run3…log:780`). Default config would read `74/81`. A reading of `74/81`
  here is **not a miss** — it means the toggles are off in this profile; say
  which, do not "correct" it.
* **Instrument lines:** `CONDITIONS pack=%d/%d active` and the explicit
  `CONDITIONS P1 :: registered=… active=…` from `CP60.ReadConditions`, plus the
  suite header `fix pack present: %d/%d fixes active`
  (`TestKit/Code/00_TestCore.lua:351`, re-read 08-12 — `PLAYTEST_HELP` said
  `:286` and has been corrected in this commit).
* A miss on the **registered** half = a module failed its self-check. Read its
  `detail` string before anything else.

### P2 — the five new modules report `active` with an empty detail

MODULE-READ 08-12: all five exist in `Code/` and register under exactly the ids
the prediction names —
`SaintBlessing` (`Fix_SaintBlessing.lua:61/183`) ·
`DustDevilsDescrMap` (`:56/116`) ·
`AstrogeologistExtractors` (`:61/220`) ·
`SinkholeIndestructible` (`:76/126`) ·
`DustStormUndergroundBreaks` (`:131/133`).
**Instrument:** `CP60.Fixes()` → `FIXES P2 five-new :: <id> status=… detail=…`.
⚠️ `AstrogeologistExtractors` has a `latch(…, "benign")` branch that would set a
non-empty detail if the shipped profile already paid every extractor — it cannot
fire, because the boot-time patch adds 2 entries on every launch (LOG-READ,
twice, §P8 below).

### P3 — all eight conversions' modules report `active`

⚠️ **Eight conversions, SEVEN modules, SEVEN commits** — `SequenceLatents` holds
F29 items 1 *and* 3. All seven commits verified present in git today
(`git show --stat`): `69c02b9` SmallLandscapeSites · `26f0b57` NightShiftWork ·
`ab7d432` GeneForging · `388c72a` ShuttleHubOffAvailable · `21990fb`
UpgradeModifierLeak · `1471533` SequenceLatents · `8f58f30` DroneTransportMinors.
All seven module files MODULE-READ 08-12 with those Register ids. The seven
fix-build commits are likewise present: `a5b9db0 eb4c6d6 b22dda5 3966fb3
125783e 08b5d84 b5628a7`.

### P4 — the seven new probes PASS · **probe total is 87, not 85**

**All seven RUN on retail.** Derived 08-12 from `57_Probes_Wave8.lua`: not one
of them calls `SMRTest.FromFixPack`/`SourceOf`, so the retail sandbox's missing
`debug.getinfo` cannot skip them. Their SKIP conditions are class/preset
presence and `FixMissing` only.

**The eight standing retail `[install]` SKIPs, named** (derived from source —
each returns `FAIL` when `FromFixPack` is nil, and a deferred SKIP outranks FAIL,
`00_TestCore.lua:326-334` — and then CONFIRMED against the 2026-08-11 retail
log, which shows exactly these eight with `introspection unavailable (retail
sandbox)`): `CaveInsNoDisasters` · `MilestoneCrash` · `TrainsToVoid` ·
`BrokenTrackSalvage` · **`TrackSalvageWipe`** · `LakeEntombment` ·
`GhostFarmOxygen` · `LowStorageWarning`.
⚠️ A **ninth** probe is `kind = "install"` — `CrystalMysteryHang` — but it needs
no introspection and RUNS. ⚠️ `STATE.md`'s *"retail probes 78/87"* is a **PASS
count** from 2026-08-03, not a runnable count; **79** probes attempt a verdict on
retail.

**Expected messages, verbatim from the last retail suite run**
(`docs/archive/u2run3_Mars.exe-20260811-02.01.06.log`, 2026-08-11, 81/81 active,
`77 PASS, 0 FAIL, 10 SKIP, 0 ERROR`). ⚠️ That was a *different, post-batch* save:

| probe | 08-11 message | varies with this save? |
|---|---|---|
| `TrackShellLeak` | `mass salvage deletes the emptied track, and zero shells survive in the loaded save` | ⚠️ yes — before the heal it could read `N undeletable TrackBase shell(s) still in this save` (a **FAIL**), which on a pre-batch save loaded WITH the pack should be impossible because the heal runs inside `LoadGame` first |
| `SaintBlessing` | `Saint's modifier names TraitReligious, and all 15 dome Saint(s) have it registered` | ⚠️ yes — count differs; `…(no Saint in a dome in this save, so the live half had nothing to read)` is a **PASS**, not a miss |
| `DustDevilsDescrMap` | `the descriptor follows MainMap in both directions, and MainMap's own disabled setting still wins` | no — pure stand-ins |
| `AsteroidVisitPrecedence` | `supply rockets no longer open the picker; landers and F72's unloading case still do` | no — pure stand-ins |
| `AstrogeologistExtractors` | `all 12 buildable extractors are paid (12 Effect_ModifyLabel entries on the profile)` | no — reads the **preset**, not the colony, so it PASSes on a non-astrogeologist save too |
| `SinkholeIndestructible` | `Sinkhole is indestructible on the class and the template; 0 instance(s) inspected, none overriding` | ⚠️ instance count only |
| `DustStormBreakMapFilter` | `merged fragments are filtered to MainMap connectors, single-map fragments pass straight through, and the persisted array is restored by identity in both cases` | no — pure stand-ins |

### P5 — no probe that passed before this batch now fails

* **`AsteroidLanderAvailable`** (F94 rewrote the body it drives) — Src-READ
  08-12 in `30_Probes_Wave3.lua`: it stubs `IsKindOf` to answer true only for
  `"UniversalRocketBase"`, so **all five of its cases take the FIRST branch and
  never reach the corrected `elseif`**. F94's entry claimed this; it is now
  re-derived. 08-11: PASS, `busy-but-unassigned landers on the pad count;
  assigned and off-world ones do not`.
* **"any probe touching `Fix_TrackSalvageWipe`"** — the probe named
  `TrackSalvageWipe` is `kind = "install"` and **SKIPS on retail**. The probe
  that actually reads F91 here is **`TrackShellLeak`**. Do not record the SKIP
  as coverage.
* **Baseline tally to compare against:** `77 PASS, 0 FAIL, 10 SKIP, 0 ERROR`
  (2026-08-11, retail). Its two non-`[install]` SKIPs were
  `AnomalyCaveInMap` (*"stub target undeclared on this build: AddAreaRubble,
  IsNearDome"* — build-dependent, expect it again) and
  `TechDescriptionBuilding` (*"the tech has no description T"* —
  save/data-dependent). **Do not chase a total** (the archive's own rule); a
  moved SKIP is read by NAME.

### P6 — zero `[LUA ERROR]` naming the batch's files

Grep set for the close-out, exact filenames:
`Fix_SaintBlessing` · `Fix_DustDevilsDescrMap` · `Fix_AstrogeologistExtractors` ·
`Fix_SinkholeIndestructible` · `Fix_DustStormUndergroundBreaks` ·
`Fix_SmallLandscapeSites` · `Fix_NightShiftWork` · `Fix_GeneForging` ·
`Fix_ShuttleHubOffAvailable` · `Fix_UpgradeModifierLeak` ·
`Fix_SequenceLatents` · `Fix_DroneTransportMinors` — plus the two amended in
place, `Fix_TrackSalvageWipe` and `Fix_AsteroidLanderAvailable`.
**Partial evidence already banked, quotable:** every launch since 2026-08-02 has
run the batch live; the corun-pt15 sitting was ~3h20m at 81/81 with 0
`[LUA ERROR]`. What this leg adds is *this* save's paths and the owner's own
play, so the verdict is written **"this session's paths"**, never "the
conversions are verified".

### P7 — the conversions produce no visible behaviour change

Owner-facing list, in their words at the end of ④: night shifts, gene forging,
shuttle-hub availability, landscaping site picking, upgrade modifiers, sequence
latents, rocket refuelling. ⚠️ **Rule 13**: F92 and F95 legitimately DO change
morale/production on load — if the owner remarks on either, that is the fix
landing, not drift, and it is said out loud in the moment.

### P8 — ⭐ THE DECIDER. The three heals, at most one line each, none on reload

**The three SAVE-STATE heal lines, current wording MODULE-READ 2026-08-12 —
these are the grep strings:**

| # | line (format string) | source | fires when |
|---|---|---|---|
| 1 | `TrackSalvageWipe: deleted %d invisible track shell(s) left behind by a whole-track salvage (F91)` | `Fix_TrackSalvageWipe.lua:362` | **only if `shells > 0`** (`:361`) |
| 2 | `SaintBlessing: re-based %d dome blessing(s) onto the label colonists are actually filed under` | `Fix_SaintBlessing.lua:179` | **only if `rebased > 0`** (`:178`) — needs ≥1 dome Saint lacking the corrected modifier |
| 3 | `AstrogeologistExtractors: applied %d Astrogeologist extractor bonus(es) this save started without` | `Fix_AstrogeologistExtractors.lua:213` | **only if `healed > 0`** (`:212`) — and the whole pass returns early unless `GetCommanderProfile().id == "astrogeologist"` (`:174-178`) |

A fourth, related line exists and is NOT one of the three:
`AstrogeologistExtractors: removed %d duplicate extractor modifier(s) left by
the identity-keyed heal` (`:216`). If it appears, that is the 2026-08-02
inflation being repaired — quote it, it is a finding about the save's history.

**⛔⛔ THE TRAP. These two fire on EVERY LAUNCH, before any save is loaded, and
are NOT save heals:**

```
[CommunityFixPack] AstrogeologistExtractors: added 2 missing extractor entr(y/ies) to the astrogeologist profile (10 already present)
[CommunityFixPack] SaintBlessing: corrected 1 dome-colonists trait modifier label(s) of 2
```

LOG-READ twice: `docs/archive/cp15sitting_Mars.exe-20260811-15.09.30.log:174` and
`:178` (printed on an unrelated save, during boot, at `Lua 0:00:19`), and again
in `u2run3…log:174/:178`. They are the `DataPatch` preset patches. **Counting
either as a P8 heal is a wrong reading, and it is the reading a careless grep
produces.**

**The idempotence half already has a control.** On 2026-08-11 `u2run3` loaded
three post-batch saves in one process (`U2STAGE` → `U2RT1` → `U2RT2`) and
produced **zero** save-state heal lines across all three, while the two boot
lines appeared exactly once each. So "a second load logs none of them" is
already sampled on healed saves. **What PT-60 uniquely buys is the FIRST-load
half on a genuinely pre-batch save** — nobody has ever taken that.

**⚠️ SILENCE IS NOT A MISS.** The archived prediction says *"at most one line
each"*. Line 3 is silent on a non-astrogeologist colony **by design**; lines 1
and 2 are silent on a save with no shells / no dome Saints. `CP60.Fixture` reads
all three populations at the gate so the sitting knows which branch it is in
**before** the log is greped. The MISS is: a line appearing **twice**, or
**reappearing on the second load**, or the F95 effect reading **2** entries per
label after the round trip (that is the identity-keyed regression, keyboard-found
2026-08-02).

**Effect reads (R7 — `CP60.Heals(when)`), taken after load 1 and after load 2:**
shells surviving vs total `TrackBase`; dome Saints vs Saints carrying a
`TraitReligious` modifier; `UIColony.label_modifiers[…]` entry counts for
`AutomaticMetalsExtractor` + `MicroGAutoWaterExtractor` (want exactly 1 each on
an astrogeologist colony) with `MetalsExtractor` + `WaterExtractor` as vanilla's
own **positive control** — they prove the query works, so a pair of zeros beside
two ones is a real shortfall rather than a dead read.

### P9 — ⛔ DEGRADED. It cannot discriminate on any shipped save.

> *08-02:* `SMRFixPack_rocket_fuel_key` is **absent** from `DroneControl` after
> one load-and-save (`8f58f30` clears it, including from saves that already
> carry it).

**No shipped save can carry it.** Derivation, both halves re-read this session:

1. The §1.5 shape this conversion replaced wrote the field at **exactly one
   line**: `if r.FuelResource ~= "Fuel" then self.SMRFixPack_rocket_fuel_key =
   r.FuelResource end` — `git show 8f58f30^:Code/Fix_DroneTransportMinors.lua`,
   lines 173-175. (The other two mentions, `:149/:152`, only *read and clear* it.)
2. **Src-VERIFIED 08-12:** `FuelResource` is a template property declared
   `default = "Fuel"` (`Lua/UniversalRocket.lua:47`), and a grep of
   `Lua/BuildingTemplate`, `Data` and `DLC` for any assignment returns **zero
   hits** — every hit in the tree is a *reader*. So `r.FuelResource == "Fuel"`
   always, the guard was never true, and the field was **never written into any
   save**.

⇒ **An ABSENT reading is TRUE but NON-DISCRIMINATING** — it would read absent
whether or not the clearing line works. Record it as **"negative control held,
population 0"**, never as "the field-removal half ran". A **PRESENT** reading
would be a genuine finding: report it verbatim with the object id, value and
type. `CP60.P9()` says all of this in its own output so the archived log carries
the caveat.

**The console read is pre-flighted for its own failure mode.** `DroneControl` is
a **mix-in parent** (`__parents` of `DroneHub`, `RocketBase`, `RCRover` —
Src-VERIFIED 08-12), never a placed template, and this project has never walked
one with `AllMapsForEach`. So `CP60.P9()` walks the base class **and** the three
concrete classes and prints both counts: **a base walk of 0 while the concrete
walks find objects means the enumeration failed**, and that is exactly the shape
of a false clean result.

## 3. THE SITTING BRIEF

### Measure moments and what each costs the owner

| # | moment | owner does | cost |
|---|---|---|---|
| M0 | launch + Mod-Manager state | clicks Play; confirms the pack is enabled if the gate stops | 2–3 min (mostly boot: 19 s + their hands) |
| M1 | load the staged copy | types `*r CP60.Load("CP60STAGE.savegame.sav")` | ~1 min (load ≈10 s + 15 s settle) |
| M2 | fixture + heal effect reads | types 2 lines | ~2 min |
| M3 | registry + suite | types 2 lines; **eyes on nothing** — this is Tier C, delegated | ~3 min (suite runtime) |
| M4 | round trip (save → load → heals → P9) | types 4 lines | ~4 min |
| M5 | **ordinary play** | plays their colony however they like | **15–20 min** |
| M6 | verdict words | answers 2–3 questions out loud | ~2 min |
| M7 | riders, only if M2 read their precondition true | varies — each rider states its own cost before it is offered | 0–10 min |
| M8 | quit to desktop | one click | 1 min |

**Honest attended estimate: ~40–60 min**, and the 15–20 min of play is the
**floor, not the total** (batch-1 rule 4 — console driving is owner time and it
is counted here). A truncated sitting still banks ①–③.

### Priority queue — decider first

1. **⓪ + P8 first-load heals.** The moment `CP60.Load` returns, the three heal
   lines are already in the log at **zero extra owner cost**. This is the only
   thing in the leg that a pre-batch save is required for. Do it before anything
   can go wrong.
2. **① + ② registry and suite** — confirm against the annotated table above.
3. **③ round trip** — P8's idempotence half and P9, `R4` satisfied by
   construction.
4. **④ the owner's 15–20 min** — P6/P7, riders opportunistic only.

### Console lines, pre-flighted, in order

Hand them **one at a time**. Every one carries `*r`: the bare console has no
thread context (`SMRTest.RunAll` under-reports without it) and three of these
Sleep or yield. ⛔ Never append a `--` comment to any of them.

```
*r CP60.Menu()
*r CP60.Gate()
*r CP60.Load("CP60STAGE.savegame.sav")
*r CP60.Fixture("after load 1")
*r CP60.Heals("after load 1")
*r CP60.Fixes()
*r CP60.Suite()
*r CP60.SaveNamed("CP60RT")
*r CP60.Load("CP60RT.savegame.sav")
*r CP60.Heals("after load 2")
*r CP60.P9()
*r CP60.Note("<owner verbatim>")
*r CP60.Close()
```

⭐ **The load mechanism is `CP60.Load`, not the in-game list** (batch-2 rule 2):
`Copy-Item` duplicates the display name, so `CP60STAGE` and `USA Sol 302` are
indistinguishable in the load dialog. Filename only, from the console.
⭐ **No logger is wanted this sitting** — nothing in P1–P9 reads one, so the
post-restart `SMRTest.Log.<name>(true)` re-arm is deliberately **skipped**. Say
so rather than leaving it as an unexplained omission.

### Rider preconditions — READ at M2, never promised blind

`CP60.Fixture` prints, in one line: elevators · passages · trains + tracks ·
rockets · sinkholes, plus dome Saints and TrackBase shells. **A rider whose
precondition reads 0 is not offered to the owner** — it is inventoried as
TAKEABLE WHEN and the close-out names the read that decided it.

* **F21** re-earn → needs a *working* train line (trains > 0 **and** track).
* **F34(d)** → needs a rocket loading with drones embarking; owner stages it —
  hands + eyes, ~5 min. Offer only if rockets > 0.
* **C42** → needs passages **demonstrably trafficked**, not merely present; the
  within-session traversal witness must be taken **before** any further
  save/load.
* **F90** → needs elevators ≥ 1 **and** a surface dust storm arriving during ④.
  ⛔ Never force the storm: F90's live half is a *victim distribution*. Quiet
  weather ⇒ the rider is not taken, and that is recorded, not worked around.
* **F96** R2 needs a large meteor on the sinkhole's hex during St. Elmo's Fire.
  **Nobody waits for that coincidence** (the archive says so). Not offered.

### What is already settled and must NOT be re-litigated

F92 / F93 / F95 are `tested`; PT-61 closed F93's live half. F90 and F91 already
carry in-play verification from 2026-08-02 — but on **manufactured** fixtures (a
built sandbox colony with an all-underground 1668-connector fragment for F90; a
deliberately created shell for F91). This leg's marginal value on those two is
**this fixture's organic state**, not re-proving the mechanism.

### Close-out additions specific to this prep

* Delete `CP60STAGE` **and** `CP60RT`; record **"deleted, listing verified"** —
  ⛔ never "gone" (rule 12). List the directory **BY NAME**.
* Byte-verify all **four** protected files against the MD5s in §1.
* Carry the 18-name EF-051 stray inventory forward for the post-untick cleanup.
* If P9 read absent, the entry line is *"negative control held"* — and F57's
  entry gets the Src-verified note that the removed shape could never have
  written the field on shipped data.

## 4. Stop conditions prep did NOT resolve

* Whether this colony is astrogeologist, has dome Saints, or carries shells —
  **unknowable with the game closed**. All three are read at M2 and all three
  are legitimate zeros.
* Whether `AllMapsForEach` accepts the mix-in class `DroneControl` — never
  driven; `CP60.P9()` carries its own witness for it.
