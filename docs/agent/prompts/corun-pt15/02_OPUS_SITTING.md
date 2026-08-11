# Chain prompt 2 — the sitting (ATTENDED co-run; owner at the keyboard)

**Read `README.md` first — binding chain rules apply.** Staleness check, todo
list. This brief is a PRIORITY QUEUE, not a schedule (batch-1 lesson): a
truncated sitting still banks the deciders first, owner deviation is absorbed
(witness whatever runs), and once the owner overrides onto a lead, state the
plan's position once and keep the ledger — no nagging.

**Honest cost.** Owner time: **~45–90 min**, dominated by the mystery march
(open-ended, and it is the owner PLAYING THEIR OWN COLONY — organic time, not
overhead). Legs 1–2 alone: ~15 min. Estimates have missed before; the queue
order is what protects the sitting, not the estimate.

## Before launch

ARM via `CP15_ARM.ps1` (gate GREEN or no launch). Confirm the three protected
MD5s and `CP15STAGE.savegame.sav`. Take the pre-launch save-dir listing if
prompt 1's is stale. Console: TestKit loaded → Enter (or Alt-Shift-C) once in
a colony.

## The queue

**Leg 0 — gate + fixture confirm.** Load `CP15STAGE.savegame.sav` (a COPY —
say so in the log). `RequirePackLoaded` — a 0/0 STOPS the sitting (owner
re-enable + full restart, D13). `CP15.MysteryWhere()`: founder approval
state + trigger countdown, raw values printed. Record run conditions
(build, map, speed read-back, pack count AS READ).

**Leg 1 — F85's Ctrl-F9 check (10 seconds, highest value per second).**
Owner presses **Ctrl-F9** in the colony. Read: did a quicksave land — on-disk
file (name recorded verbatim, EF-050 eyes) + any notification. Either answer
is a finding: landing = a live default-keybind route into F85's defect
(changes the whole disposition); nothing = the source read confirmed on
retail. **Route the evidence to the checklist F85 item; the decision stays
the owner's.** FORCED (a keypress on request); say so.

**Leg 2 — C39, observed at last.** All readings by the parked instruments,
FORCED and disclosed; D10 stays parked; everything else at base.
1. Setup (setup-cheats sanctioned, disclosed): a staffed Workshop + an
   in-family Service control (Diner/Spacebar) in one dome. If the new-ish
   colony lacks them: `CheatResearchAll` + place + `CheatCompleteAllConstructions`
   + `CheatSpawnNColonists`/`CheatUpdateAllWorkplaces` as needed. ⚠️ Cheats
   AFTER leg 0's fixture confirm and AFTER leg 1, never before; they are
   setup for THIS leg only, and `CheatResearchAll` is fine for PT-15 (the
   mystery grants its own tech — but state it in the record).
2. `CP15.C39Before()` — the full read set on both buildings.
3. `CP15.C39Enact()` — first execution of
   `LawDefs.Policy_Automation_ServiceAutomation:Activate()`, pcall printed,
   `ActiveLaws` read back (EF-048: truthiness/type).
4. Readings per prompt 1's shift-boundary answer (if a shift change is
   needed, take it at ultra — the same fast sols advance the mystery
   countdown; label every reading with its game time).
5. `CP15.C39After()` → the entry's question: do the four-Workshop
   `max_workers` drop, does `performance`/Comfort move, WHICH DIRECTION, and
   does the Diner control behave per the compensated path. The owner LOOKS
   at both infopanels — their observation is the attended half; quote it.
6. `CP15.C39Revert()` — `:Deactivate()`, read the policy default restored,
   full read set again (do-no-harm on the revert).
   R4: if any C39 claim is about persisted state, round-trip it; otherwise
   stamp PRE-RELOAD ONLY explicitly.

**Leg 3 — the mystery march (ORGANIC; the owner plays).**
`SetGameSpeedState("ultra")` through the dead time; the owner plays the
beats: founder approval if not yet passed → trigger (10–20 sols) → sinkhole
popup → anomaly scan → tech → build Light Traps → wisps caught over the
following nights. The rig's part: `CP15.MysteryWhere()` on request, periodic
condition reads, the standing F02/F78/F81 organic watch, and NOTHING forced
into the sequence. Every popup/beat gets a one-line timestamped record.

**Leg 4 — PT-15, the reading it all exists for.** At the free-the-wisps
choice: `CP15.TrapRead()` BEFORE (wisp count per trap, trap output, grid
production), owner makes the choice (their click, their observation), read
AFTER. The fix's claim: ~1000× wisp count of power, a real source — against
the broken trickle. R7: the effect is grid numbers, not a popup. R4: save +
reload (chain-named save, full `.savegame.sav`) and re-read — the power must
survive serialization. **Owner verdict verbatim** — with owner eyes this can
earn `tested` (Tier per WORKFLOW sign-off; package the raw lines for their
quick read).

**Leg 5 — F15 rider (good-to-have).** If a second trapful exists: destroy
mode, research-points read either side. N/A is a fine answer; say why.

## Recording (incremental, per leg)

Bank each leg's readings to the entries/checklist AS THEY LAND (self-split
safe). Every reading: FORCED/ORGANIC label + what was cheated for setup.
Logs archived with R8 `git add -f`, `cmp`-verified, named
`cp15_<exe>-<stamp>.log`. `PROBE SWEEP:` in every result commit.

## Close-out

Disarm (gate GREEN), delete staged saves EXCEPT the three protected files +
any save the owner asks to keep (list them), **save-dir listing = the EF-051
post-untick confirm** — compare against prompt 1's baseline + this sitting's
known writes; a returned stray REOPENS EF-051, a clean listing is the
evidence that retires the WORKFLOW caveat (the audit rules on it). Byte-verify
the three protected files. Whole-log review: 0 `[LUA ERROR]` expected;
F99/C45 greps; unexplained lines verbatim with age. Outbox to
`03_FABLE_AUDIT.md` (`## Notes from upstream`): per-leg verdicts with their
log line numbers, what was forced, what the owner said verbatim, misses.
Commit, delete this file in the same commit, push.

## Stop conditions

README's chain-wide set, plus: the owner ends the sitting → bank what ran,
inventory the remainder as TAKEABLE riders, still hand prompt 3 a clean
close-out.

---

# Notes from upstream

*Written by prompt 1 (prep), 2026-08-11, game closed. Everything below was
re-derived from `A:\SteamLibrary\steamapps\common\Project Spark\ModTools\Src` at
1.0.7.396349 — chain rule 5, recorded facts are claims. Lines are marked
**Src-verified** (a file was opened and the numbers read this session) or
**trust-carried** (inherited and NOT re-checked).*

## 0. What prep changed about the plan, in one block

Three things this brief says are now known to be wrong or incomplete, and the
queue above should be read with these in front of it. Nothing else moved.

1. **⛔⛔ LEG 3/4 ALMOST CERTAINLY DOES NOT REACH THE WISP CHOICE THIS SITTING.**
   Leg 3's sketch ("trigger 10–20 sols → sinkhole popup → anomaly scan → tech →
   build Light Traps → wisps caught") is the shape of the mystery but not its
   size. §2 below has the full sequence with every sleep. Scripted sleeps to the
   choice total **40–80 sols**, and on top of those the sequence blocks on **two
   anomaly scans, a Large Water Tank filled to 80%, a Light Trap built, and 30
   wisps caught** (`fireflies_caught > 29` is the literal gate). Plan leg 3 as a
   march that ENDS SOMEWHERE and gets saved, not as a march that arrives. The
   README's own stop condition already covers this — use it early rather than
   late, and let the owner decide how long to march once they see
   `CP15.MysteryWhere()`'s first output.
2. **⚠️ LEG 2's SETUP CHEATS CAN DESTROY LEG 5's MEASUREMENT.**
   `CheatResearchAll` is ungated on retail (Src-verified: `Lua\Cheats.lua:78-90`
   has no `CheatsEnabled()` check, unlike `CheatStartMystery`) — but it empties
   the research queue, and F15's reward is measured as a delta on the **queued
   tech's** points (§3). With nothing researchable, `AddResearchPoints` returns
   early and the points are silently lost. ⇒ if leg 5 is wanted, either skip
   `CheatResearchAll` or queue a tech again afterwards and say so.
3. **⭐ LEG 2's TIMING QUESTION IS ANSWERED AND IT IS BETTER NEWS THAN EXPECTED.**
   `performance` recomputes immediately on `:Activate()`; no shift change is
   needed for the main reading (§4). Only the *Comfort payment* needs a shift
   boundary. Leg 2 step 4's "if a shift change is needed" resolves to: **not for
   the numbers; yes for one optional extra reading.**

## 1. PT-15 / F07 — the read surface, Src-verified

**The defect line and its two clean siblings** (Src-verified, exact):
`Lua\Mysteries\Fireflies.lua:692` — `trap.el_prod_modifier:Change(#trap.fireflies)`
inside the `"free"` branch of `SetLightTrapMode` (whole function `:674-701`).
The sibling sites `:346` (release) and `:479` (catch) both read
`...:Change(#self.water_source.fireflies * 1000)`. The shipped fix
(`Code/Fix_WispRewards.lua:50`) replaces the function and multiplies.

**Why the value sticks and then heals** (Src-verified): the game
`UndefineClass("ObjectModifier")`s CommonLua's version (`Lua\Modifiers.lua:288`)
— so the `Change` that runs is `Lua\Modifiers.lua:321-331`, which **sets
absolutely** (`self.amount, self.percent = amount, percent`), not additively.
The CommonLua `ModSet` variant at `CommonLua\Classes\Modifiers.lua:486` is dead
code here. ⇒ the broken number persists **until the next wisp event**, at which
point `:346`/`:479` re-Change the same modifier *with* the ×1000 and the
evidence is gone. The routine wisp event is the 4 AM `FirefliesGoHome`
(`Fireflies.lua:257-263`, `elseif hour == 4`).
⇒ **`CP15.TrapRead()` must be the FIRST thing after the choice.** This is in the
leg's own comment block and on the checklist.

**The chain from the modifier to a number a player sees** (Src-verified):
`Change` → `target:UpdateModifier` → `ElectricityProducer:OnModifiableValueChanged`
(`Lua\ElectricityProducer.lua:68-73`) → `electricity:SetProduction(self.working
and self:GetPerformanceModifiedElectricityProduction() or 0)`.
`LightTrapBase` has no `performance` member, so that resolves to
`electricity_production` unchanged (`:60-66`).

**What `CP15.TrapRead(when)` prints, per trap** — every one of these is a named
object's field, not a screen impression:

| read | where it comes from | why it is in the set |
|---|---|---|
| `#trap.fireflies` | `LightTrapBase:Init` (`Fireflies.lua:557-565`) | the multiplicand — **without ≥1 wisp the reading is meaningless**, since 0×1 and 0×1000 are both 0. The leg's second `Applicable` says exactly that. |
| `el_prod_modifier.amount / .percent / .is_applied` | the modifier the patched line writes | the defect's own site, read directly |
| `electricity_production` own + resolved | class default 0 (`Fireflies.lua:551`) + modifier | ⭐ **THE VERDICT FIELD**: `== #fireflies` ⇒ BROKEN, `== #fireflies * 1000` ⇒ FIXED |
| `working`, `work_state` | `LightTrapBase:OnSetWorking/SetWorkState` | `working` gates the GRID number but not the property — a not-working trap reads correct property, zero grid |
| `electricity.production` | `SupplyGridElement` (`Lua\SupplyGrid.lua:48-53`) | the grid-facing figure |
| `GetUIPowerProduction()` | `ElectricityProducer:75-76` | the infopanel's own number |
| `grid.production / current_production / current_consumption / current_reserve`, producer/consumer/storage counts | `SupplyGridFragment` (`SupplyGrid.lua:346-360`) | "the power grid" half of the ask |

**Reference scale, trust-carried from the module's own comment:** a Solar Panel
produces 2000 internal units. 3 wisps broken = 3 units; 3 wisps fixed = 3000.

## 2. ⭐ The mystery timeline, Src-verified end to end — the biggest finding of prep

`Lua\Scenario\Mystery 11.generated.lua`, sequence **"Trigger"** (`:37`), the
scenario's autostart sequence. Sol arithmetic uses **1 game hour = 30,000
game-ms (MEASURED, PLAYTEST_HELP:118-121)** ⇒ 1 sol = 720,000 ms.

| # | line | wait | sols | who unblocks it |
|---|---|---|---|---|
| 1 | `:75` | `WaitMsg("ColonyApprovalPassed")` | — | founder stage (§5) |
| 2 | `:76` | `Sleep(7200000 + rand(7200000))` | **10–20** | clock |
| 3 | `:80-88` | Sinkhole Spawner sequence + "Sinkhole!" message | — | clock |
| 4 | `:108-123` | `Wait Sinkhole 1 Scanned` → `while not _anomalyScanned` | — | ⛔ **OWNER: scan the anomaly** |
| 5 | `:127-141` | choice 1, "A Turn for the Positive" | — | ⛔ **OWNER: answer** |
| 6 | `:153` | `Sleep(1440000 + rand(2160000))` | **2–5** | clock |
| 7 | `:160` | `spawn_fireflies = true` + "Illuminating a Mystery" | — | clock |
| 8 | `:181` | `Sleep(2160000 + rand(1440000))` | **3–5** | clock |
| 9 | `:200-213` | "Nights of Wonder", Research 1: Effects, Spawner Repeater, then `Sleep(10800000 + rand(10800000))` | **15–30** | clock ⚠️ the big one |
| 10 | `:214-216` | `while not (#MainCity.labels.Sinkhole > 2)` | — | spawner |
| 11 | `:235-250` | `Wait Sinkhole 2 Scanned` → `while not _anomalyScanned` | — | ⛔ **OWNER: scan anomaly 2** |
| 12 | `:252` | `Sleep(3600000 + rand(3600000))` | **5–10** | clock |
| 13 | `:267` | `Sleep(3600000 + rand(3600000))` | **5–10** | clock |
| 14 | `:282-284` | `SA_GrantTech{Research = "MegaStorage"}` | — | — |
| 15 | `:290-295` | `WaitMsg("ConstructionComplete")` until a `WaterTankLarge` | — | ⛔ **OWNER: build one** |
| 16 | `:296-328` | loop until the tank is **80% full of water** | — | ⛔ **OWNER: supply it** |
| 17 | `:389-404` | "The Light Traps" → `while not (#MainCity.labels.LightTrap > 0)` | — | ⛔ **OWNER: build a Light Trap** |
| 18 | `:406-408` | `while not (fireflies_caught > 0)` | — | wisps |
| 19 | `:426-428` | `while not (fireflies_caught > 29)` | — | ⛔ **30 wisps** |
| 20 | `:429-438` | **choice 2 — "Prisoners of Light"**: choice1 = *Symbiotic coexistence* → `SetLightTrapMode("free")` (`:440`); choice2 = *Experiment upon them* → `SetLightTrapMode("destroy")` (`:471`) | — | ⭐ **THE PT-15 READING POINT** |

**Scripted sleep total: 40–80 sols.** Derived real time (NOT measured — the
project has no measured real-seconds-per-sol figure; this assumes the game clock
advances 1 game-ms per real-ms at 1× and ultra = 20×, `const.ultraGameSpeed`,
PLAYTEST_HELP:345): **~25–50 real minutes of pure sleeping** at ultra, before
any owner-gated stage and before catching 30 wisps.

**Wisp supply, Src-verified** (`Fireflies.lua:230-252`): each `SinkholeBase`
spawns `starting_fireflies = 2` on its first night (hour 22), then **1 in 3 per
night** thereafter, capped at `max_firefly_number = 10`. With three sinkholes
that is a handful up front and roughly one a night after — 30 caught wisps is
tens of sols on its own.

## 3. F15 rider — the entry's implied instrument is WRONG, and here is the right one

⚠️ **There is no research-point bank to read.** Src-verified,
`Lua\Research.lua:810-846`: `AddResearchPoints` adds to the **current queue's
tech**, as `status.points = status.points + ModifyResearchPoints(points * scale)`
with `scale = const.ResearchPointsScale = 1000` (`Lua\_GameConst.lua:44`), and it
**returns early and silently when no researchable tech exists** (`:816-819`).
`ModifyResearchPoints` (`:722-737`) applies four multipliers —
`BreakthroughResearchSpeedMod`, `ExperimentalResearchSpeedMod`,
`OmegaTelescopeResearchBoostPercent`, `IndependenceLawResearchSpeedMod`.
⇒ the granted figure is **Δ`tech_status[queued].points` / 1000**, and every
multiplier must be printed beside it. `CP15.RPRead()` prints all of them and
refuses to be a measurement when the queue is empty.

⚠️ **The grant is DELAYED 3.33 game hours.** Each wisp's RP comes from the `Die`
destructor, which `Sleep(100000)`s first (`Fireflies.lua:533-544`). Read after
≥4 game hours, not immediately. `CP15.F15Destroy()` says so and
`CP15.F15After()` is the second half.

⚠️ **ONE SHOT.** Once `lighttrap_mode == "destroy"`, `SinkholeBase:BuildingUpdate`
stops spawning wisps entirely (`Fireflies.lua:248-250`). There is no second
trapful to retry on. Take this rider LAST, after PT-15's own reading is banked.

⛔ **And it is FORCED by construction.** On a save that answered choice 2 with
"free", the destroy branch has no organic route — `CP15.F15Destroy()` calls
`CP15.ForceMode("destroy", "I-KNOW-THIS-IS-FORCED")`, which is deliberately
awkward to type. Chain rule 12 stands: this is the one place the mystery's own
payload function is called directly, and the leg labels itself FORCED.

## 4. C39 — the shift-boundary answer, and the setup requirement nobody had written down

All four of the entry's citations were re-read and are **EXACT**:
`LawDef-Technology.lua:227-234` · `Workplace.lua:205-217` (dev comment
`:209-210`) · `ArtWorkshop.lua:24-27` · `PolicyDef.lua:740-747`.

* **✅ `performance` recomputes IMMEDIATELY on `:Activate()`.**
  `LawEffectModifyLabel:OnStart` → `container:SetLabelModifier`
  (`ClassDef-Factions.generated.lua:2039-2059`) → each member's
  `Workplace:OnModifiableValueChanged("max_workers", …)`, which ends with
  `SetWorkshift(current_shift)`, `CheckWorkForUnemployed()`,
  `UpdatePerformance()` **and `RebuildInfopanel(self)`**
  (`Workplace.lua:376-409`). No shift change needed for the numbers.
  ⚠️ `Laws.lua:626`'s `bld:UpdatePerformance()` loop is inside
  `SavegameFixups.MinistriesRework104` and is NOT the live path — do not cite it.
* **⛔ The Comfort PAYMENT needs a shift boundary.** Paid in
  `Workshop:OnChangeWorkshift` to the workers of the **outgoing** shift, only
  `if working`, as `Min(MulDivRound(g_Consts.WorkInWorkshopComfortBoost=5000,
  self.performance, 100), 100*const.Scale.Stat)`
  (`ArtWorkshop.lua:19-32`, const at `Lua\__const.lua:1730-1736`). The leg prints
  the arithmetic instantly; the payment is one optional extra reading after a
  shift change with the law active.
* **⚠️⚠️ THE SETUP REQUIREMENT: FILL THE WORKSHOP'S ACTIVE SHIFT BEFORE
  ENACTING.** `OnModifiableValueChanged` **fires the overflow workers** when
  `max_workers` drops (`Workplace.lua:378-390`). A shift that was full stays
  full at the reduced max — which is exactly the "full reduced shift" the
  entry's ~200 arithmetic assumes. A half-staffed workshop settles nothing.
  On `:Deactivate()` the fired workers do **not** snap back
  (`CheckWorkForUnemployed` re-hires over game time), so an after-revert reading
  below the baseline is expected and is not a second defect. Both facts are in
  the leg's own output lines.
* **Reachability, partly answered:** neither the LawDef nor `PolicyDef
  Automation` carries a tech prerequisite or condition field. Gating, if any, is
  the ordinary Assembly policy flow; SortKey 900 = 10th of 11 in Technology.
* **The population instrument:** `CP15.C39Scan()` walks
  `UIColony.labels.ServiceBuildings` — the same container `OnStart` writes to —
  and splits it live by `IsKindOf("Service")`. That measures the entry's central
  claim on the actual colony instead of counting templates. Then
  `CP15.C39Set(i, j)` picks subject (Service=false) and control (Service=true),
  and warns if they are in different domes.

All of §4 is also appended to `agent/bugs/C39.md` — the entry is the record, the
prompt is the errand.

## 5. The countdown read — what it measures and what it CANNOT

⭐ **The founder stage is exactly measurable, and prep found a better instrument
than the entry had.** `g_ColonyNotViableUntil` is a GameVar
(`Lua\ColonyViability.lua:80`) whose encoding is documented at `:74-78`:
`-3` before the first passenger rocket launched · `-2` in transit · `-1`
**approval PASSED** · `> 0` = the `GameTime()` at which the founder stage ends
(`OnMsg.NewHour` fires `Msg("ColonyApprovalPassed")` on the first hour past it,
`:87-98`; `const.ColonyViableByDelay = 10 * const.DayDuration`, `:102`).
⇒ when it is `> 0`, remaining founder time is exactly `value − GameTime()`, and
`CP15.MysteryWhere()` prints both raw numbers and the derived figure.

⛔ **The 10–20 sol sleep is NOT readable, and the leg is DEGRADED by design
rather than guessed** (prompt 1's stop condition). Lua is given no wake-time
accessor: the sleeping coroutine's deadline lives engine-side, `ThreadsRegister`
is `dbg()`-gated (`CommonLua\Core\cthreads.lua:87-104`), and a **script**
sequence has no instruction pointer to read — `StartSequenceScript`
(`CommonLua\Libs\Sequences\SequenceListPlayer.lua:431-459`) runs the whole
generated `Run` closure as one coroutine. ⇒ the leg reports **ARMED / NOT ARMED
plus the 0–20 sol bound**, never a remaining figure, and says so in the log.

**What it does read** (Src-verified): `GetScenarioPlayer("Mystery 11")`
(`CommonLua\Libs\Sequences\SequenceList.lua:278-280`) → `player.seq_states`,
per-sequence `status` + `IsValidThread(thread)`, and the **Trigger sequence's
`GetRegisters()` closure** — which is where `choice_result`, `choice_result2`,
`_anomalyScanned` and `_grantedTech` live. `choice_result2` is the direct answer
to "has the wisp choice been answered, and how".
⚠️ `MysteryBase.seq_player` is declared (`Lua\Mysteries\Mystery.lua:6`) and
**never assigned anywhere in the tree** — do not reach for it; the leg prints it
with that warning attached.

## 6. F85 — the Ctrl-F9 check has three witnesses, not one

Src-verified. `idQuickSave` = `ActionShortcut "Ctrl-F9"`, `ActionBindable true`,
`OnAction` → `QuickSaveGame()` (`Data\XDef\GameCheatShortcuts.lua:1990-2003`);
`ActionState` returns `"disabled"` when `not CanSaveGame()`. (Sibling note, since
the entry pairs them: `idQuickLoad` is **Ctrl-F12**, not Ctrl-F9.)
`QuickSaveGame` → `WaitQuickSaveGame` (`CommonLua\Savegame.lua:1342-1400`):

1. ⭐ **On disk.** `display_name = display_name or "QuickSave"` (`:1370`) →
   `DoSaveGame("QuickSave", params)`. EF-050 ⇒ expect
   **`QuickSave.savegame.sav`**. The leg asserts nothing about the name; the
   close-out **diffs the directory listing** and reports whatever appeared.
   ⚠️ if a save already carries the display name "QuickSave" it reuses that
   savename (`:1372-1381`) — the diff, not the expected name, is the instrument.
2. **In the log.** `print("Game saved:", name)` on success / `print("Save
   failed:", err)` on failure (`:1383-1387`). **Either line falsifies** the
   inference that Ctrl-F9 does nothing on retail.
3. **The owner's eyes.** `LoadingScreenOpen("idQuickSaveScreen", …)` (`:1369`).

`CP15.CtrlF9Before()` / `CP15.CtrlF9After()` bracket the press with timestamped
markers and print `CanSaveGame()` raw (EF-048 truthiness). ⛔ EF-047: the
"nothing happened" verdict is taken from the **archived** log after the process
exits, never mid-session — the legs say so on their own lines.

## 7. The instruments, and how they differ from every prior harness

Parked in this folder, **parse sweep GREEN** (python + `luaparser`), nothing
armed by prompt 1's commit:

* `97_CP15Common.lua.txt` — resurrected from `e5dca6f`'s `97_U2Common`
  (say/Fmt/IdOf/Try/TryYield/Applicable/WaitFor/GameIsLive/LabelAll/Load/Save
  with the EF-050 verbatim-savename guard/ReadConditions/RequirePackLoaded/
  Void/ErrorWatchNote). **New here:** `CP15.Guard(leg)`, `CP15.Label(kind, …)`,
  `CP15.Now(when)`, `CP15.Sols(ms)`. `say` also mirrors to `ConsolePrint` —
  this sitting is attended and the owner reads the console.
* `98_CP15Sitting.lua.txt` — the menu. `CP15.Menu` `CP15.Gate` `CP15.Fixture`
  `CP15.CtrlF9Before` `CP15.CtrlF9After` `CP15.MysteryWhere` `CP15.TrapRead`
  `CP15.RPRead` `CP15.ForceMode` `CP15.F15Destroy` `CP15.F15After`
  `CP15.C39Scan` `CP15.C39Set` `CP15.C39Before` `CP15.C39Enact` `CP15.C39After`
  `CP15.C39Revert` `CP15.Note` `CP15.SaveNamed` `CP15.Close`.
* `CP15_ARM.ps1.txt` — arm / arm-rehearsal / disarm.

⭐⭐ **Two gates are DIFFERENT from unattended-2's and the difference is
deliberate — do not "fix" them back:**

1. **The self-drive gate is INVERTED.** unattended-2's ARM gate *failed* a
   payload that did not call `U2.Boot()`, because nobody would be there to start
   it. This sitting is attended, and a self-driving payload would race the
   owner's play and mutate a save under them. The gate now **fails if either
   file starts a flow at file scope**.
2. **WORKFLOW rule 7's gate is PER-LEG, and the ARM script enforces that it
   really is.** A menu has no single run top, so every leg's first line is
   `CP15.Guard(...)` and a false return means the leg returns having read and
   changed nothing. The ARM script parses each `function CP15.*` body and FAILS
   the launch if any gated leg omits the call (`Menu`/`Note`/`Close` are the
   three declared gate-free ones — they read nothing and change nothing).

The **resolution cross-check now reads this brief too**: every `CP15.*(` in
`02_OPUS_SITTING.md` must resolve against the two Lua files, so a name the brief
tells you to type cannot be one that does not exist (unattended-1 defect class
1). ⇒ **if you add a leg name to this brief, add the function too, or ARM goes
RED.** The gate FAILS if the brief file is missing entirely.

## 8. Staging + the EF-051 baseline (all measured 2026-08-11, game closed)

Save directory: `C:\Users\stkot\Saved Games\Surviving Mars Relaunched\76561198020568696`

**The three protected files, MD5 (chain rule 7 — byte-verify all three at
close-out):**

| file | MD5 | bytes | last write |
|---|---|---|---|
| `PT-15.savegame.sav` ⭐ NEW standing fixture | `5D0D81A3D66CA7BABFCA85D6AC118C06` | 48,086,314 | 2026-08-11 11:13:41 |
| `TEST2H TRAIN.savegame.sav` | `103B320A1434513BC8773553096A8958` | 55,667,524 | 2026-08-03 22:21:48 |
| `PT35FIXTURE.savegame.sav` | `D721329D1EE18604B3D6C89401F74738` | 54,424,001 | 2026-08-10 17:14:03 |

The two carried MD5s match the README's recorded values exactly.

**Staged:** `CP15STAGE.savegame.sav`, `Copy-Item` of `PT-15.savegame.sav`,
**MD5 identical** (`5D0D81A3D66CA7BABFCA85D6AC118C06`), 48,086,314 bytes.

**⭐ THE PRE-LAUNCH LISTING — this is the EF-051 falsifier's baseline. LISTED,
not assumed: 56 `.sav` before staging, 57 after.** 55 was EF-051's post-untick
baseline; `PT-15` is the owner's own +1 (saved 11:13 today); `CP15STAGE` is ours.
**No stray from any prior chain is present** — every name below is either an
owner save or a fixture:

```
asttest, asttestnoans, asttestnoans2, Autosave Sol 11, Autosave Sol 16,
D10test1, dronetest1, Dronetest2, F59 Test1, f59 test2, F90 Alert,
F95 Baseline, F95 fresh, f95 healed, No disasters underground setup,
PT-15, PT-20TEST, PT-20TEST-B, PT35FIXTURE, pt611uninstall, PT61save,
randotest, saint test, Save A post research setup,
Save A setup pre research all, savesavetest, T1-UNINSTALL, T1-UNINSTALL-R,
T2-Uninstall, T2-UNINSTALL-R, test 2 pre events, Test 2 pre test, test 2,
Test 2B, Test 2C, Test 2D, TEST 2E, TEST 2F, TEST 2G, TEST 2H,
TEST 2I TEST, TEST 2I TEST2, TEST 2I TEST3, TEST 2I TEST4, TEST 2I,
Test2 H, test2 J, TEST2H TRAIN, TestE, TestF, USA Sol 2, USA Sol 298,
USA Sol 3, USA Sol 302, USA Sol 55, USA Sol 59        [+ CP15STAGE = 57]
```

⇒ **the EF-051 test is exact**: after this chain's first launch, the count must
still be **57 plus only what the sitting itself wrote**. Any of the fourteen
2026-08-11 strays returning (`CB1STAGE`, `CB2STAGE`, `CORUN0`, `CORUN1`,
`U1STAGE`, `CB2F85`, `CB2PKEY`, `CB2PKEY2`, `CB2UNINSTALL`, `U1C0PROOF`,
`U1C1HEAL`, `U1C2PT35`, `U1C6FORCED`, `U1C6HEALED`) or the extensionless `U2RT1`
REOPENS EF-051.

**⭐ A free second witness prep noticed:** `steam_autocloud.vdf` sits in the same
directory, last written **2026-08-11 09:47**. EF-051 records that it is
"rewritten at each launch". Record its `LastWriteTime` again after the sitting's
launch — if it did **not** change, that is independent evidence the sync is off,
on top of the file count.

## 9. Things that surprised me, in the order they'd bite

1. The mystery is roughly an order of magnitude longer than "10–20 sols" — the
   choice this whole chain is named for is 40–80 sols of sleep plus five
   owner-gated stages away (§2). The checklist now says so; the owner should not
   discover it at the keyboard.
2. F15's reward has no counter to read, three multipliers on it, a 3.3-game-hour
   delay, and exactly one attempt (§3).
3. Enacting the C39 law **fires workers**, which is both the trap (a half-staffed
   reading proves nothing) and the reason the reading is clean if the shift was
   full first (§4).
4. `CheatResearchAll` is ungated on retail but silently destroys F15's
   instrument (§0.2).
5. The founder-stage timer turned out to be exactly readable while the thing
   everyone assumed was readable — the countdown — is not exposed at all (§5).
6. `MysteryBase.seq_player` is declared and never assigned. A reader who trusted
   the field name would have printed `false` forever and called it a state.

## 10. Nothing is armed

Prompt 1 wrote no file into either `Code/` tree; the TEMPORARY sweep is 0 hits
and doccheck is GREEN. `CP15_ARM.ps1 arm` is prompt 2's first act.
