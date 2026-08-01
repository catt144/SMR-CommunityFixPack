# F86 save-safety session — findings report for independent comparison

**Written 2026-07-31 at the owner's request, for cross-checking against another
agent's findings before any code is written.** Model-neutral: nothing here
depends on which model produced it.

**Session state: NOTHING WAS BUILT.** No `Code/` file was modified, no A/B leg
was run, the game was never launched. Every repair described below is *proposed*
and unstarted. The session produced decisions, corrections and analysis only.

Commits, oldest first: `23dd59d` (decisions), `a58b06e` (13th-site correction),
`f50dbe0` (sweep, exposed half), `0fb7f31` (sweep, non-exposed half), `ace2d85`
(build authorisation).

---

## 0. How to read the confidence labels

Every finding below carries one. A reviewer should attack the **REASONED** ones
first — they are where I am most likely wrong.

| label | means |
|---|---|
| **MEASURED** | observed in a running game, in this project's recorded history |
| **SOURCE-VERIFIED** | read directly in `ModTools\Src` this session, file:line given |
| **REASONED** | follows from a measured mechanism, but not itself observed |
| **DERIVED** | computed from a documented constant rather than read at source |

---

## 1. Corrections to claims the project's own docs were carrying

These are the highest-value findings: each was a load-bearing statement that was
wrong before this session.

### 1.1 The F02 remedy's scope check was wrong and would have shipped a balance change — **SOURCE-VERIFIED**

`SAVE_SAFETY_REDESIGN.md` §2 said the `GetDisasterWarningTime` wrapper "must key
on the meteor descriptor and defer to the original otherwise." **Descriptor
keying cannot separate the call sites.** Full enumeration of every caller:

| site | passes | affected |
|---|---|---|
| `Meteors.lua:279` — the `Meteors` thread | `GetMeteorsDescr()` | the intended target |
| **`Meteors.lua:326` — the `MeteorStorm` thread** | **`GetMeteorsDescr()`** | **the same descriptor object** |
| `ColdWave.lua:231`, `:378`; `DustStorm.lua:467` | their own descriptors | no |
| `SensorTower.lua:31`; `TerraformingDisasters.lua:285` | **no argument at all** | no |

Inflating `warning_time` to `spawntime + spawntime_random` (up to 115 h) would
make the **meteor-storm warning fire ~5 sols early instead of 6 hours**, and make
Sensor Towers irrelevant to storm warning. That is a gameplay/balance change,
barred by FIX_POLICY §4, arriving as a side effect of a save-safety repair.

**Proposed replacement key:** `CurrentThread() == rawget(_G, "Meteors")`.
Supporting facts, both SOURCE-VERIFIED: `RestartGlobalGameTimeThread` sets
`_G[name] = CreateGameTimeThread(...)` (`_fixup.lua:20-23`), so the global holds
the thread; and `CurrentThread()` exists (`thread.lua:32`) and is **not** in
`ModEnvBlacklist`.

### 1.2 `Fix_DroneUnreachableForever` is exposed and was missing from every count — **SOURCE-VERIFIED**

Three legs, all checked:

1. **It blocks.** `Code/Fix_DroneUnreachableForever.lua:51` calls
   `building:DroneApproach(self, resource)`. Every one of ~20 `DroneApproach`
   implementations terminates in `drone:Goto` / `GotoBuildingSpot` /
   `GotoBuildingsSpot` / `EnterBuilding`, and `Unit:Goto` (`Unit.lua:130`) loops
   on `pfSleep(self, status)`.
2. **On a game-time thread.** `ApproachWrapper`'s only four callers are
   `Drone:Work` (`Drone.lua:920`), `PickUp` (`:972`), `Deliver` (`:1239`),
   `EmergencyPower` (`:1325`) — all drone **commands**, which run on
   `CreateGameTimeThread` command threads (`CommandObject.lua:100`).
3. **Mod code runs after the blocking call** — lines 52-77.

This is the same shape as `Opt_DroneOverhaul:188-190`, which was **MEASURED**
leaking at 98 errors/session.

### 1.3 `Fix_TrainCargoDumping` is NOT exposed and never belonged on the list — **SOURCE-VERIFIED**

`Train:UnloadAll` (`Train.lua:783-803`) read line by line is `pairs`/`ipairs`
table work over `RequestUnassignUnit`, `GetStoredAmount`, `GetTargetAmount`,
`AddResource` — **none of which yields**. A thread can never be *blocked inside
it*, so a save cannot capture it. It was listed on the assumption that a command
body is exposed by virtue of being a command body.

**Net effect of 1.2 + 1.3: the exposed set stays at 12, with membership changed
in both directions.** An interim published figure of "13" is superseded.

### 1.4 ⚠️ `Fix_MeteorFrequency` restarts the meteor timer on EVERY load — a shipped, player-affecting defect — **SOURCE-VERIFIED**

**This was found by the owner, not by me, and I had been about to carry it
forward into the rewrite.** It is the most consequential finding in this report
and is not recorded anywhere in the project's docs.

`OnMsg.PersistPostLoad` (`_fixup.lua:50-66`) creates a global thread **only
`if data[name] == nil`** — only when the save carries nothing for that name.
Otherwise **the persisted thread resumes with its remaining sleep intact.** So
vanilla's meteor timer survives a load correctly.

`Code/Fix_MeteorFrequency.lua:187-197` overrides that with an **unconditional**
`RestartGlobalGameTimeThread("Meteors")` on every `OnMsg.LoadGame`. Each restart
re-rolls `spawn_time` from zero. The rolled interval is 35–115 game hours
(**DERIVED**: ≈1.5–4.8 sols at 24 h/sol), so **a player who loads more often
than that interval never receives a meteor** — indefinitely and silently.

Same permanent-silence harm class as F86 itself. Currently shipped.

*Note the project already held half of this:* the F86 entry records that
`_fixup.lua:54-55` only rebuilds a thread when the save carries nothing for it.
The consequence for our own restart was never drawn.

**Open: whether this gets its own F-number or rides on the F02 entry. Not
decided — the owner paused here.**

### 1.5 A stale count in `PLAYTEST_HELP.md` — **SOURCE-VERIFIED, already fixed**

Line 269 documented `ListFixes()` as showing "67 default fixes". Correct is
**68 of 74** — 67 was true only between the F24/F28 deletions and the F83 build.
Corrected in `23dd59d`.

---

## 2. New analysis produced this session

### 2.1 The severity tiering — **REASONED, not measured**

Exposure severity is not about the module; it is about **whether we replaced
something vanilla would otherwise keep running**:

- **Module ADDS a thread** → after uninstall it resumes, errors once, dies. The
  player loses a fix they lose by uninstalling anyway. Net harm ≈ one log line.
- **Module REPLACES a vanilla body** → our version is what got serialised, so
  when it errors after uninstall **vanilla's behaviour is gone too**. The player
  ends up worse than if they had never installed the pack.

This tiering set the build scope and justified barring layer 1. **It is reasoned
from the measured mechanism, not itself observed.** Only two sites have ever
been measured leaking.

**The control, if a reviewer wants one:** one PT-20-method leg against a single
own-thread module — block it, save, uninstall, load, count errors. The owner
accepted the residual without requiring it. *A reviewer who disagrees with the
tiering should attack this first, because layer 1 was barred on its strength.*

### 2.2 `Fix_RainsDeadlock` is the same hazard class as `Fix_MeteorFrequency` — **REASONED**

Both replace a **global disaster loop** — `GlobalGameTimeThreadFuncs.Meteors`
and the global `RainsDisasterLoop` respectively. By 2.1 both therefore leave the
player permanently short a vanilla system after uninstall. MeteorFrequency was
MEASURED doing exactly that; RainsDeadlock had never been identified as the same
class in any doc.

### 2.3 The repair may be retroactive — **REASONED, and now complicated by 1.4**

Because `OnMsg.LoadGame` runs *while the mod is installed*, a restart there
replaces a persisted thread carrying our body with one running vanilla's — so
the **next** save contains no pack code on that thread. That would mean the fix
cleans already-damaged saves, not merely prevents new damage.

`SAVE_SAFETY_REDESIGN.md` §7 currently says the only remedy for existing damage
is "put the mod back", calling it "uncomfortable, but real", and rules out a
cleanup mod on that basis. If 2.3 holds, that framing is too pessimistic.

⚠️ **But 1.4 shows an unconditional load-restart is itself harmful.** The
reconciliation I proposed — and did **not** get to validate — is a **one-shot,
GameVar-latched heal** that fires once per save lineage and never again. **This
is unbuilt and unreviewed. It is the weakest link in this report.**

### 2.4 Command threads may self-clean — **REASONED, UNVERIFIED**

A drone/colonist command thread ends when its command completes, and the next
command starts on the new code. If so, Tier 2 exposure ages out of a save
naturally once a repair ships, with no heal needed. **I did not verify this and
a reviewer should treat it as a hypothesis.**

### 2.5 The upgrade-path hazard — **SOURCE-VERIFIED**

`Fix_MeteorFrequency`'s current body calls `SMRFixPack.MeteorsBeatSet` /
`MeteorsNote` at **eight points inside the thread body** (30 `SMRFixPack.`
references in the file). Every save made with the current pack carries that body
*by value* on the persisted thread.

Deleting those helpers in a layer-3 rewrite would make a resumed thread throw →
thread dies → **meteors stop permanently**. That is the F86 harm, delivered by
the F86 repair, on the upgrade path.

**General rule this implies, absent from the redesign:** a layer-3 conversion
must either keep every `SMRFixPack.*` helper the *old serialised body* calls, or
guarantee that old thread is restarted on load.

### 2.6 A wrapper degrades gracefully; a body copy does not — **REASONED**

If a future patch fixes the vanilla bug, a chained wrapper becomes a harmless
no-op, whereas a FIX_POLICY §1.5 body copy silently reinstates the old body's
shape and can **undo the official fix**. Written into FIX_POLICY §1 in `0fb7f31`.

---

## 3. The sweep result (owner decision 2, discharged)

### 3.1 Exposed set — 5 of 12 have a route out

Every "input" named was separately checked and is **synchronous**.

| module | verdict |
|---|---|
| `Fix_MeteorFrequency` | **Layer 3** via `GetDisasterWarningTime` (see 1.1 for the keying correction) |
| `Fix_DroneUnreachableForever` | **Layer 3 — patch the CONSUMER**: the defect is only the timestamp value, and its reader `Drone:CleanUnreachables` is synchronous |
| `Fix_TrainWaitTime` | **Layer 3** — restamp from a wrapper on the synchronous `TransportStatistics:AddSpentTime`, which vanilla calls at the exact boarding moment (`ColonistTransport.lua:511`) |
| `Fix_RainsDeadlock` | **Layer 2** — wrap `RainsDisasterActivation` to post `RainDisasterEnd` on the collision early-return; vanilla's loop untouched |
| `Fix_ArrivalDeaths` | **Layer 3 for half (b)** via `ChooseDome` / `GetDomesReachableByColonists`. ⚠️ **Half (a), the raw `SetPos` with no passability search, has NO route — unresolved** |
| `Opt_DroneOverhaul` | **Layer 2** — move moonlighting out of the command body |
| `Fix_ShelterReflex` | already compliant |
| `Fix_BombardmentSpread` | **no layer-3 route** — the defect is a discarded local mid-function |
| 4 own-thread modules | layer 1 only — **barred by owner decision** |

### 3.2 Non-exposed set — 6 of 22 convert to a chained wrapper

All 22 are already synchronous; the benefit is rot reduction (2.6), not save
safety. Verified feasible: **`Fix_SmallLandscapeSites`** (`GetClosestDests(drone,
top_count)` *already takes* the bound its only caller never passes — zero copied
logic), **`Fix_NightShiftWork`** (vanilla returns `true`/nil and the fix only
widens it, so shift 1/2 is identical *by construction*),
**`Fix_UpgradeModifierLeak`** (vanilla iterates a string-keyed table with
`ipairs`, so the original is a verified no-op), `Fix_GeneForging`,
`Fix_ShuttleHubOffAvailable`, `Fix_TrainCargoDumping`.

4 need a design pass; 9 are correctly full replacements — including
**`Fix_TrackSalvageWipe`, a 130-line copy, the pack's largest rot exposure, with
no route out**; 3 are already optimal.

---

## 4. Method — including two approaches that were discarded

A reviewer should check my *method* as well as my conclusions, because two
plausible ones produced garbage.

1. **Pattern-grepping for yield-looking names — FAILED.**
   `Colonist:BoardVehicle` contains no `Sleep`/`WaitMsg` yet blocks for an entire
   train journey via `self:PlayPrg(...)`. Any fixed name list misses one.
2. **Transitive analysis resolved by bare function name — FAILED WORSE.** Marked
   **7,621 of 15,106** names blocking, claiming `LandscapeForEachUnit` blocks
   "via `IsValid`". Common accessor names collide with unrelated blocking
   methods. Discarded, not reported.
3. **What works** (`tools/blocking_analysis.py`, kept in-repo): seed from the
   engine's four primitives — `Sleep`/`WaitMsg`/`WaitWakeup`/`PlayState`
   (`PersistGatherPermanents`, `cthreads.lua:451-464`) — then propagate **only
   through unambiguous callees**, where *every* definition of a name blocks.
   Mixed names are reported AMBIGUOUS and read by hand against the specific class
   patched. Gives **633 of 15,106** direct yielders.

**Enumeration key:** what each module **assigns**, extracted alias-blind
(`grep -oE 'function [A-Za-z_][\w]*:[A-Za-z_][\w]*\('`). **Do NOT key on
`SMRFixPack.Require{class=,method=}`** — that declares a *self-check* target, not
a replacement, and over-catches (`Fix_LakeEntombment` checks
`Unit:ExitImpassable`, which does block, but never replaces it).

---

## 5. Things I got wrong this session

Listed deliberately — a diagnostic comparison is more useful with the misses.

1. **Certified "no 13th site"** and committed it. Wrong; withdrawn within hours.
   My grep anchored `^function Drone:` at column 0 and the module installs via
   `local D = Drone` … `function D:ApproachWrapper` **indented inside `apply()`**
   — an alias *and* a broken anchor.
2. **Then published "the list is 13".** Also wrong — `Fix_TrainCargoDumping`
   came off, so the total is 12 with two membership changes.
3. **Estimated "~17" remaining non-exposed modules.** Actually **22**.
4. **Floated `Fix_DomeFreeSpaceMismatch` as a layer-3 candidate.** Rejected on
   inspection: an input patch on `GatherFreeLivingSpaces` would also hit
   `MicroGHabitatBase:RefreshFreeLivingSpaces`, which the module **deliberately
   excludes for a recorded reason**.
5. **Nearly proposed `ValidateBuilding` as a layer-3 input** for
   `Fix_UniversityOvertraining`. Counted callers first: **55**, reaching story
   bits and staffing. Rejected.
6. **Was about to carry the per-load restart (1.4) into the rewrite.** The owner
   caught it. This is the one a reviewer should weigh most heavily, because it
   means my design pass did not independently audit the *existing* fix's
   behaviour — only its save-safety shape.

---

## 6. Open questions

1. **`Fix_ArrivalDeaths` half (a)** — the raw `SetPos` with no passability
   search. No route found. Needs a design pass, not a guess.
2. **Filing of 1.4** — own F-number, or a note on F02? Undecided.
3. **Does the one-shot latched heal earn its place** given it costs one re-rolled
   interval? Undecided. Alternatives considered: drop it and rely on the ~6-8 sol
   watchdog latency; or gate on `IsValidThread` reporting a dead thread, which
   cannot catch an old-body thread that is alive but doomed to throw.
4. **Is the tiering (2.1) sound enough to bar layer 1?** Reasoned, not measured.
5. **PT-01's original cause was never found** — the historical hunt falsified
   every static explanation. A layer-3 F02 does not explain it either, so the
   watchdog is still doing real work.
6. **Does 2.4 hold** — do command threads really self-clean?

---

## 7. Decisions taken by the owner this session

Recorded so a reviewer knows what is settled versus open.

| # | decision |
|---|---|
| 1 | Layer ordering **3 → 2 → 1 adopted**, written into `FIX_POLICY.md` §3a as a hard rule |
| 2 | Layer-3 sweep **authorised at full scope** — now discharged |
| 3 | F02 **held**, then **hold lifted** once the sweep reported |
| 4 | **D10 and D12 stay held until the F86 repairs LAND and verify** (gate is the build, not the written rules) |
| 5 | Build scope **Tiers 1 + 2**; ⛔ **layer 1 barred** |
| 6 | **`Opt_DroneOverhaul` carve-out GRANTED** — its layer-2 repair is save-safety surgery, not drone work |
| 7 | **One A/B leg per tier** |
| 8 | Build, but stop and report on anything troubling — **which is why the build is paused here** |
| 9 | Six wrapper conversions batched **after** the F86 build, single leg |
