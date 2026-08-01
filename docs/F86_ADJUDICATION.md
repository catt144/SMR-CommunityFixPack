# F86 adjudication — where the project actually stands

**Written 2026-07-31 by an independent session against `docs/F86_ADJUDICATION_PROMPT.md`.
Every load-bearing claim below was re-derived from `ModTools\Src`, `Code\`, or the
2026-07-31 game logs — not from either position document.** Labels: **RE-VERIFIED**
(I reproduced it from primary sources), **FALSIFIED** (I can show it wrong),
**OPEN** (needs a measurement; the measurement is named).

---

## 1. Verdict

**Yes-with-changes.** The measured mechanism, the layer ordering, the F02
thread-keying correction, both exposure-list membership changes, and the
command-thread self-cleaning hypothesis all survive independent re-derivation —
the authorised Tiers 1+2 are the right four repairs. But the build should not
start until three things change: **(1)** one unmeasured engine fact — whether
`CreateGameTimeThread` runs the new thread before or after the creating statement
continues — gates *both* Tier-1 designs and is settleable with a two-line console
probe; **(2)** the `Fix_RainsDeadlock` build spec is missing a migration pass for
existing saves and its wrapper shape, as written, can be defeated by that same
engine fact; **(3)** the `Fix_MeteorFrequency` rewrite must pick its restart
semantics *as part of the spec*, because the unconditional load-restart is
simultaneously the shipped §1.4 defect, the measured repair mechanism, and the
only thing standing between the upgrade path and re-delivering the F86 harm.
Separately: the rule text both documents share — "synchronous mod code can never
be captured" — is **falsified as a universal** (a concrete pack module is
capturable today, §3.1), and one owner decision (`Fix_BombardmentSpread`,
"one broken volley") was taken on a **falsified harm statement** (§3.2) and
should be re-taken. Neither falsification changes which modules get repaired.

---

## 2. Settled — independently confirmed, with evidence

**2.1 The PT-20 core measurement is real, and the controls hold. RE-VERIFIED
from the logs themselves.** `Mars.exe-20260731-16.28.52` (pack disabled in Mod
Manager: "present, but not loaded") and `Mars.exe-20260731-16.51.27` (junction
removed: "not present") each contain **exactly 99** `attempt to index a nil
value (global 'SMRFixPack')` errors — 98 drone + 1 meteor — with the injected
`spawn_time | number 60000` locals in both, and the
`Unpersist missing permanent: Mod/SMR_CommunityFixPack | Fallback permanent:`
line in both. `Mars.exe-20260731-17.55.09` is the reinstall leg: "persisted
Meteors thread on load was DEAD — restarting with the fixed body". One
correction to the record: the adjudication prompt's pointer named 17.14 as a
PT-20 leg; `17.14.47` is actually the **save-hook probe** session (SaveGameStart
FIRED / SaveGameDone FIRED, manual save, `autosave=nil`). The junction leg is
16.51.27. Evidence unaffected.

**2.2 The persist mechanics read exactly as recorded. RE-VERIFIED.** Saves
capture persistable threads only (`ThreadsPersistSave()`, cthreads.lua:471), and
the saving thread is asserted non-persistable (cthreads.lua:467) — so no
*running* frame is ever captured; capture means blocked. Permanents are a
**curated list**, not a walk of `_G` (persist.lua:17 — "add some functions as
permanents so they can be safely stored in upvalues"), which is why anything not
on the list — mod and vanilla functions alike — serialises **by value**.
`PersistableGlobals` restore at persist.lua:136-142; the `data[name] == nil`
rebuild gate at `Config\_fixup.lua:54-56`. One addition to the record: the
sleeping-permanents block registers a **fifth** stack sleeper, `WaitThread`
(cthreads.lua:463), beside Sleep/WaitMsg/WaitWakeup/PlayState — see §3.3.

**2.3 The F02 keying correction (`F86_SESSION_FINDINGS` §1.1) is correct.
RE-VERIFIED.** Full grep of Src finds exactly the seven call sites the findings
table lists, none more. Both meteor threads pass the same `GetMeteorsDescr()`
descriptor (Meteors.lua:270/:279 and :309/:326), and the `MeteorStorm` poll loop
consumes `warning_time` directly in its break-and-notify test and its
notification `expiration` — so descriptor-keyed inflation to `spawntime +
spawntime_random` would fire the storm warning up to ~115 h early and pin its
countdown there. Barred by FIX_POLICY §4; the correction stands. The replacement
key's parts each check out: `CurrentThread()` is a C export absent from
`ModEnvBlacklist` (Mod.lua:1267-1428 contains no thread entries);
`RestartGlobalGameTimeThread` assigns the thread to `_G[name]` (_fixup.lua:21);
and on load `_G.Meteors` is restored to the persisted thread via the generic
`PersistableGlobals` pass — so the key survives loads. The +10-game-minute
residual also re-derives: with warning ≥ spawn, vanilla's dead `if` turns true
and adds `Sleep(5000)` = 5000/30000 h. The discovery document's descriptor-key
caveat was wrong precisely where its author ranked it their weakest claim (§7.3)
— the self-assessment was accurate.

**2.4 The per-load restart (`F86_SESSION_FINDINGS` §1.4) is a real, shipped,
player-facing defect. RE-VERIFIED.** `Code/Fix_MeteorFrequency.lua:187-197`:
`OnMsg.LoadGame` calls `RestartGlobalGameTimeThread("Meteors")` gated only on
the fix being active — never on the persisted thread's health. The restarted
body re-rolls `spawn_time` from zero (`:90`). So a player who never plays a full
rolled interval (35-115 **game** hours ≈ 1.5-4.8 sols) between loads never
receives a single meteor, silently, for as long as they own the pack. The file's
own header saw the mechanism and stopped one inference short: "worst case a
pending strike/warning is rescheduled **once** on load" (`:18-19`) — true per
load, false in aggregate. **The collision with the MEASURED "reinstalling
repairs it" claim resolves cleanly: they are the same mechanism.** The
unconditional restart is what revives a dead thread on reinstall *and* what
re-rolls a live timer on every load. Both documents are right; "put the mod
back" remains honest advice for *reviving the thread*, and must now carry the
caveat that the current pack then suppresses meteors under frequent loading.
Recommendation on filing: **own F-number** (§7, D1).

**2.5 Both membership changes are correct. RE-VERIFIED.**
- **`Fix_DroneUnreachableForever` in.** All three legs re-checked:
  `Code/Fix_DroneUnreachableForever.lua:51` calls `building:DroneApproach(...)`
  with lines 52-77 after it; Src has 26 `DroneApproach` implementations and
  `Unit:Goto` (Unit.lua:130) loops on `pfSleep(self, status)`; the only four
  `ApproachWrapper` callers are Drone.lua:920/:972/:1239/:1325 — command bodies
  — and `CommandObject.CreateThread = CreateGameTimeThread`.
- **`Fix_TrainCargoDumping` out.** `Train:UnloadAll` (Train.lua:783-803) read
  with its callee tree: `RequestUnassignUnit` (_TaskRequest.lua:394 — a C
  `UnassignUnit` plus debug-only bookkeeping), `ResourceStockKeeping:AddResource`
  (pure arithmetic), `UniversalStorageDepotBase:AddResource`
  (StorageDepot.lua:536-543 — AddAmount/SetCount/RebuildInfopanel, no yield).
  One trap disarmed on the way: there **is** a `Sleep(500)` nearby in
  StorageDepot.lua:559 — inside `DroneLoadResource`, not `AddResource`. The
  original listing really was the wrong test ("it is a command body"), and the
  removal is sound.

**2.6 The upgrade-path hazard (`F86_SESSION_FINDINGS` §2.5) is real and
understated. RE-VERIFIED.** 30 `SMRFixPack.` references in
`Fix_MeteorFrequency.lua` as claimed; the count of helper call points *inside
the thread body* is ~12, not "eight" (`:71,:73,:83,:84,:92,:94,:104,:106,:113,
:114,:116,:122`) — more sites, same direction. Every save made with today's
pack carries that body by value on the live `Meteors` thread. Its interaction
with §1.4 and §2.3 is not a loose end but a forced design — see §5.3.

**2.7 Command threads self-clean (`F86_SESSION_FINDINGS` §2.4) — CONFIRMED,
with the mechanism.** `CommandObject` runs each command via
`sprocall(command_func, ...)` and then pulls the next command from the queue
**in the same thread** (CommandObject.lua:243-262). So it is the *frame*, not
the thread, that ages out: once the in-flight command ends (completes, errors,
or is interrupted by `DoSetCommand`), our function is off that stack and the
next save is clean. Tier-2 exposure therefore expires within one command
duration after a repair ships — no heal needed. The same read explains the
PT-20 observation that drones behaved normally through 98 errors: `sprocall`
absorbs the throw, throttles (`Sleep(1000)` on repeat), and the thread carries
on with the next command.

**2.8 The save hook is measured, including for this adjudication.
RE-VERIFIED.** Logs 17.14.47 and 17.55.09 both show `SaveGameStart FIRED —
SavingGame=true` and `SaveGameDone FIRED` with `OnMsg.LoadGame` as positive
control, manual saves only (`autosave=nil`). `DoSaveGame` fires the message
before the write (Savegame.lua:1043) and `SaveAutosaveGame` is one flag plus a
call into the same function (Savegame.lua:1450-1453). **The autosave leg
remains unobserved**, and the probe is still armed:
`SMR-BugFixPack-TestKit/Code/97_SaveHookProbe.lua`. One sol of play closes it.

**2.9 `Fix_RainsDeadlock` is correctly Tier 1. RE-VERIFIED.** It replaces the
global (`SMRFixPack.SetGlobal("RainsDisasterLoop", fixed_loop)`, the module's
apply), and the orphaned `fixed_loop` dies at its first global lookup
(`Sleep`) after uninstall — that rain type is then gone for the save, vanilla
behaviour with it. Note its header still carries the falsified by-name
persistence belief (`:51-52`), as the F86 entry records.

**2.10 The analysis tool's figures are honest. RE-VERIFIED by running it.**
`tools/blocking_analysis.py` against today's Src prints **15,106 names; 633
yield directly** — exactly as reported. What the figures *mean* is narrower
than the findings imply — see §3.3.

**2.11 The Tier-3 "one log line" claim is now source-verified per module.**
All four own-thread modules (`MeteorStormWedge`, `CrystalMysteryHang`,
`ExtenderFlapChurn`, `TrackConnectorPingPong`) create their own GT threads and
replace no vanilla body — `Fix_MeteorStormWedge` in particular only *checks*
`GlobalGameTimeThreadFuncs.MeteorStorm` in `Require` and restarts **vanilla's**
body when healing. Each orphaned thread errors at its first post-resume global
lookup and dies; nothing vanilla dies with it. The proposed control leg is no
longer needed to trust the tiering's ADD side (owner may still want the datum —
§7, D4).

**2.12 The retroactive heal (`F86_SESSION_FINDINGS` §2.3) has a shipped
precedent neither document cites.** `Fix_RainsDeadlock` already implements a
**one-shot latched heal**: `SMRFixPack.RefreshRainsLoops()` on `PostLoadGame`
swaps each persisted old-body loop thread for a fresh one exactly once,
latched by a `SMRFixPack_fixed_loop` marker inside the existing
`RainsDisasterThreads` GameVar entry (`Fix_RainsDeadlock.lua:80-110`). The
"unbuilt and unreviewed" weakest link is in fact built, shipped, and — as far
as the record shows — has not misbehaved. That materially raises confidence in
the same pattern for meteors (§5.3).

---

## 3. Wrong — falsified, with proof

### 3.1 "Synchronous mod code can NEVER be captured by a save" — FALSIFIED as a universal, and the exposure count with it

This is the load-bearing claim (`F86_DISCOVERY_POSITION` §3, carried into
FIX_POLICY §3a and the ENGINE_FACTS "REAL RULE"). Its *thread-frame* arm is
sound — I re-verified that saves capture only blocked persistable threads
(§2.2). But the rule as stated tests only **where our frame is**. Persist
serialises by value **everything reachable from a captured thread** — every
frame's function, locals, and upvalues (measured: PT-20's injected locals came
back) — and everything in persisted storage. Two capture routes the rule
excludes:

- **The storage route — which this project itself MEASURED and then defined
  out of the rule.** The 2026-07-31 instance-closure experiment (ENGINE_FACTS:
  `GetPriorityForRequest` written onto a Building, saved, mod removed, function
  came back and *ran*) is a synchronous mod function entering a save with no
  yield anywhere. The later "the test is not *where is this function stored*"
  framing is wrong as written: storage location is exactly what put that
  closure in the save.
- **The live-local route — and the pack has a concrete capturable module
  today: `Fix_CaveInsNoDisasters`.** The chain, every link source-verified:
  1. The module wraps the FUNC slot: `info[FUNC] = function(sleep, map, ...)`
     (`Fix_CaveInsNoDisasters.lua:35`).
  2. The engine's periodic-repeat loop holds `local info` across the call —
     provably live, because the same statement reads it again after the call
     returns: `sleep = info[FUNC](sleep, obj) or info[SLEEP] or -1`
     (lib.lua, `PeriodicRepeatCreateThread`). Block scoping protects the
     *between-ticks* `Sleep(sleep)`, not the in-call window.
  3. Vanilla's UndergroundMarsquake FUNC **yields inside the call**:
     `Sleep(SessionRandom:Random(g_Consts.MarsquakeRandomTime * const.HourDuration))`
     (Marsquake.lua:313), then per-rubble `Sleep(duration)` inside
     `TriggerUndergroundMarsquake` (:273).
  4. The repeat thread is persistable (`MakeThreadPersistable(thread)` in
     `PeriodicRepeatCreateThread`).
  So on an Underground map, any save landing in the pre-quake delay or the
  quake itself captures the `info` table — with **our wrapper at slot 3 and
  vanilla's FUNC as our `orig` upvalue — by value**. With
  `MarsquakeSpawnTime = 384 h` and `MarsquakeRandomTime = 96 h` (__const.lua),
  the window is roughly **one in nine Underground-map saves**.

**Harm today: none.** The wrapper is layer-2 shaped (guard, then
`return orig(...)`, nothing after), the stale captured table is only read for
the remainder of the in-flight iteration, and the loop re-reads the global
`PeriodicRepeatInfo` next tick. Dead weight, zero errors — verified frame by
frame. **What breaks is the bookkeeping, not the build:**

- "Can never be captured" must become "can never be captured **through the
  thread-stack route**"; the real test is value-reachability (§5.1).
- "~62 of 74 safe **by construction, needing no work at all**" is an overclaim:
  safe-by-construction additionally requires that the module stores no function
  value into persisted state and none of its assignment targets is held live
  across a yield by engine code. I swept `Code/` for those routes: no module
  permanently stores a closure into persisted state (`Fix_MoraleComfortTooltip`
  installs an instance-level `GetProperty` but removes it within one
  synchronous call under pcall, documented no-yield window;
  `Fix_FirstAsteroidPrefabs` persists one boolean GameVar;
  `Fix_LastTransmissionStorage`'s preset-eval write is the one residual —
  §4.4). The practical scope survives; the *rule* and the *count* do not.
- **The exposure list is at least 13 by its own definition** (it already counts
  the compliant `Fix_ShelterReflex`); `Fix_CaveInsNoDisasters` belongs on it
  with disposition "compliant — no work". And the enumeration method is proven
  incomplete: the sweep's key (`grep 'function C:m('` over `Code/`) structurally
  cannot see table-slot assignments (`info[FUNC] = …`), global replacements
  (`SetGlobal`), or preset-field writes — CaveIns fell through *both* sessions'
  nets. "Is any fixed number defensible?" — only relative to an enumeration
  that names all five assignment shapes (§6, step 7).

### 3.2 `Fix_BombardmentSpread`: "the damage is one broken volley" — FALSIFIED

`WaitBombard` has exactly one caller: `StartBombard` runs it on a one-shot GT
thread and posts `Msg("BombardEnd", obj)` **after it returns**
(Bombardment.lua:156-161). Mystery 7's generated sequence does
`StartBombard(RandomDome, …)` then **`WaitMsg("BombardEnd")` with no timeout**
(`Scenario/Mystery 7.generated.lua:941-942`), inside its bombardment loop. So
if a save lands mid-volley (our replaced `WaitBombard` blocked in its missile
sleeps) and the pack is later removed, the resumed frame errors, the one-shot
thread dies **before posting `BombardEnd`**, and the mystery's sequence thread
blocks forever on an untimed WaitMsg — the same shape as F81. Corrected harm:
not one broken volley but **Mystery 7's recurring bombardment permanently
stops for that save** (plus a wedged sequence thread). The window is small —
volleys last a couple of game minutes on a 10-20-sol cycle
(`Sleep(7200000 + InteractionRand(7200000))` = 240-480 game hours) — but the
§6.3 decision ("accepted residual") was taken on a wrong description and
should be re-taken on this one (§7, D3).

### 3.3 `tools/blocking_analysis.py` — figures honest, verdicts not standalone

The 633/15,106 reproduce (§2.10), but three structural blind spots mean a
"clear" from the tool must never close a question by itself:

1. **Bare global calls do not propagate.** `CALL = r'[:.](name)\s*\('` requires
   a preceding `.`/`:`, so `WaitBombard(obj, …)`, `pfSleep(self, status)`, and
   every other global-style call is invisible to the fixpoint. `Unit:Goto` —
   the function the whole drone exposure rests on — is *not* marked blocking by
   this tool; the humans hand-read it (correctly).
2. **The definition universe is column-0 named functions only.** `local
   function` definitions and anonymous bodies — including the `Meteors` /
   `MeteorStorm` / `RainsDisasterLoop` thread bodies this defect is about — are
   not in `defs` at all.
3. **The seed omits `WaitThread`**, the fifth sleeping function the engine
   itself registers as found-in-thread-stacks (cthreads.lua:463), and the
   pathfinding sleeps (`pfSleep`/`MoveSleep`) that block every `Goto`.

The sweep's conclusions stand because every membership call was also hand-read
against Src (I re-did the two contested ones, §2.5). Keep the tool as triage;
record in its header that "clear" means "clear of the four literals among
column-0 dot-called names", nothing stronger.

### 3.4 Small corrections to the record

- `F86_SESSION_FINDINGS` §2.5: "eight points" — the body has ~12 helper
  reference points. More, not fewer; direction unchanged.
- The adjudication prompt's log pointers: 17.14 is the save-hook probe leg;
  the junction-removed PT-20 leg is **16.51.27** (§2.1).
- `Fix_MeteorStormWedge.lua:127-130` comments claim the heal is "persist-safe
  by name" and that "a mod game-time thread … is not persisted" — **both
  contradict the measured F86 mechanism** (mod GT threads persist by default;
  nothing mod-authored persists by name). The heal thread is transient so the
  exposure is negligible, but this is a third file carrying the disproven
  persistence model and it should be re-commented in the Tier-1 build.

---

## 4. Unproven and load-bearing

**4.1 GT-thread creation ordering — the one fact that gates BOTH Tier-1
designs. OPEN.** Does `CreateGameTimeThread(f)` run `f` synchronously to its
first yield, or only on a later scheduler tick? Nothing in ENGINE_FACTS or
Src's Lua answers it (the scheduler is C). It matters twice:

- **Rains.** The authorised repair ("wrap `RainsDisasterActivation` to post
  `RainDisasterEnd` on the collision early-return; vanilla's loop stays") only
  works if the activation thread runs **after** the vanilla loop reaches its
  `WaitMsg` (loop: `CreateGameTimeThread(RainsDisasterActivation, settings)`
  then `WaitMsg("RainDisasterEnd")`, TerraformingDisasters.lua:310-316). Under
  run-at-creation semantics the wrapper's message fires before anyone is
  listening and **the fix does nothing** — the deadlock it exists to break
  survives it. (A shape immune to the ordering exists — post the message from
  a `Sleep(1)`-first micro-thread — but costs a 1 ms own-thread window; decide
  after measuring, not instead of.)
- **F02.** `RestartGlobalGameTimeThread` assigns `_G.Meteors` *after*
  `CreateGameTimeThread` returns (_fixup.lua:21). Under run-at-creation
  semantics, vanilla's body would make its first `GetDisasterWarningTime` call
  before the global holds the thread — the `CurrentThread()` key would miss
  once and that cycle would run at the broken ~6 h cadence. Cheap guard either
  way: defer when `rawget(_G,"Meteors")` is falsy, and accept one short cycle
  per restart, or fail the probe first and know it never happens.

**Settling it costs two console lines** (`CreateGameTimeThread` a `ModLog`;
`ModLog` after the create; `FlushLogFile()`; read the order). Run before any
Tier-1 code.

**4.2 The autosave leg of the save hook. OPEN, probe armed.** Source-verified
(§2.8) but never observed. With layer 1 barred nothing in the authorised build
depends on it, but it is a recorded ENGINE_FACTS claim resting on source-only
evidence, the probe (`97_SaveHookProbe.lua`) is already in the Test Kit, and
one sol of ordinary play closes it. Fold into the same session as 4.1.

**4.3 The severity tiering's ADD side.** Was REASONED; I have upgraded it to
source-verified per module (§2.11). The one-leg control (block an own-thread
module, save, uninstall, load, count errors) remains available if the owner
wants a measured datum, but no build decision now rests on it.

**4.4 `Fix_LastTransmissionStorage`'s `Condition.eval` closure. OPEN, low.**
The module writes a mod closure into a FactionDefs preset sub-object
(`Fix_LastTransmissionStorage.lua:134`). Presets are permanents
(Preset.lua:1362-1394), so the walk stops at the preset root — the closure
enters a save only if engine code holds the *Condition sub-object* live across
a yield while evaluating likes. One source check of the faction-likes
evaluation path closes it. Until then this is the only unclassified
function-value write among the "safe" modules.

**4.5 `Fix_ShelterReflex` / `Fix_CaveInsNoDisasters` compliance** rests on the
layer-2 argument (nothing after the call ⇒ nothing to execute after removal),
which is unfalsifiable by design and was correctly cancelled as an experiment.
Accepted residual; nothing to do.

---

## 5. Missed by both

**5.1 The corrected capture rule (this is the one to write into the docs).**

> A mod function enters a savegame **iff its VALUE is reachable from the
> persisted graph at write time**. Three routes: **(a)** its frame sits below a
> yield on a blocked persistable game-time thread; **(b)** it is held in a live
> local or upvalue of *any* captured frame — including engine frames
> (`Fix_CaveInsNoDisasters`, §3.1); **(c)** it is stored in persisted state —
> object instance fields, GameVar contents, notification closures (the measured
> instance-closure experiment). Class tables, `OnMsg` registrations, presets,
> and UI windows are safe (permanents / rebuilt / not persisted); real-time
> threads are never persisted; the saving thread itself is asserted
> non-persistable, so purely synchronous code is safe **from route (a) only**.

Both position documents test route (a) alone. Route (c) was measured by this
project and then written out of the rule; route (b) was invisible to every
sweep. The corrected rule costs nothing operationally — layers 3/2/1 address
route (a), and the route (b)/(c) sweep of `Code/` is §3.1's (done, one residual
in §4.4) — but the *test* the policy teaches must be the reachability test, or
the next module written against §3a will repeat CaveIns.

**5.2 The rains migration gap.** Every existing save made with today's pack
carries `fixed_loop` threads **by value** (they are the activation threads;
the module marked them `SMRFixPack_fixed_loop` when it created them). The
authorised repair deletes `fixed_loop` and leaves "vanilla's loop alone" — but
vanilla's loop is not what is running in existing saves; *ours* is. Those
threads keep working after the upgrade (their `_ENV` is the mod env, which
resolves while the pack is installed, and the body calls no `SMRFixPack.*`
helper), **but the pack code stays in the save indefinitely, and a player who
later uninstalls still loses rain types — the exact Tier-1 harm the repair is
being built to remove.** The Tier-1 spec needs one more line: a
`RefreshRainsLoops`-style pass keyed on a **new** marker (the old one now means
"old fixed body", not "current"), swapping persisted loops onto **vanilla's**
`RainsDisasterLoop`. The precedent code is already in the module (§2.12).

**5.3 The §1.4 / §2.3 / §2.5 triangle is a forced design, not three open
questions.** For `Fix_MeteorFrequency`, enumerate the restart options:

| option | §1.4 (re-roll per load) | §2.5 (old body + deleted helpers) | saves cleaned? |
|---|---|---|---|
| (a) delete helpers, no restart | fixed | **old thread dies on first helper call → meteors stop — the F86 harm, shipped by the repair** | never |
| (b) keep unconditional restart | **defect stays shipped** | safe | yes, every load |
| (c) restart only if `IsValidThread` fails | fixed | **misses the alive-but-doomed old body** (findings Q3 saw this) | only after a death |
| (d) **one-shot latched heal** — restart once per save lineage on first load under the new version, GameVar latch | fixed (one re-roll, once) | safe (old body replaced before it can run) | yes, once |

Only (d) closes all three at once — and it is the pattern already shipped in
`RefreshRainsLoops` (§2.12). (c) plus a dead-thread check on `NewDay` (the
watchdog the rewrite keeps anyway) converges to (d) with ≤1-sol latency and
one error line; acceptable fallback. "Keep the helpers forever as stubs" makes
(a) safe but leaves the old body looping in every existing save permanently —
F86 unfixed for the installed base — and is not recommended. The findings
called the latched heal "the weakest link in this report"; adjudicated, it is
the **only complete answer on the table**, and it should be specified, reviewed
and built as part of Tier 1 — not dropped. (Owner call: §7, D2.)

**5.4 What actually dies is the contract, not the body.** The tiering's
add/replace split is a good proxy, but the three Tier-1-class harms found so
far (Meteors loop, rains loops, `BombardEnd`) share a sharper signature: **our
frame was keeping a promise some other thread was waiting on** — a global loop
that must never end, or a message someone WaitMsg's on with no timeout. That is
the question to ask of any future module: *who is waiting on what this frame
was going to do?* It is how §3.2 was found, and it belongs next to the tiering
in the redesign doc.

---

## 6. What to do next — ordered

1. **Run the two measurements (one short game session, before any code):**
   the GT-creation-ordering console probe (§4.1) and the autosave-hook sol
   (§4.2, probe already armed). Record both in ENGINE_FACTS.
2. **Land the rule corrections** — done in this commit: capture rule
   (ENGINE_FACTS + FIX_POLICY §3a), exposure count ≥13 with CaveIns compliant
   (BUGS F86 + redesign §5.2), BombardmentSpread harm (redesign §6.3).
3. **File the per-load restart** as its own F-number (recommendation D1), fix
   delivered by the F02 rewrite.
4. **Build Tier 1 with two spec amendments:** `Fix_MeteorFrequency` — layer-3
   wrapper (thread-keyed, deferring when `_G.Meteors` is falsy) **plus the
   one-shot latched heal (5.3-d)** plus the split watchdog;
   `Fix_RainsDeadlock` — wrapper shape chosen from the 4.1 probe result **plus
   the migration pass (5.2)**.
5. **Build Tier 2 as authorised** (consumer patch for DroneUnreachableForever;
   `AddSpentTime` wrapper for TrainWaitTime; ArrivalDeaths half (b);
   DroneOverhaul layer-2 move under the granted carve-out). Unchanged by this
   review; `ArrivalDeaths` half (a) still needs its design pass.
6. **Re-take the BombardmentSpread decision** on the corrected harm (D3).
7. **Re-run the exposure enumeration once, with all five assignment shapes** —
   class-method replacements, table-slot writes, `SetGlobal`/global
   assignments, preset-field writes, own threads — and record the resulting
   list as the durable one. My sweep of the non-method shapes found only
   CaveIns (capturable, compliant) and the §4.4 residual, so this is expected
   to confirm 13, but it should be the recorded method, not a grep that has
   now twice missed a module.
8. Then the six wrapper conversions as one batch, and only after Tier 1+2
   verify, D10/D12 — both unchanged.

---

## 7. Open decisions for the owner

**D1 — Does the per-load restart get its own F-number? Recommend YES.** It is
a distinct, currently-shipped, player-facing defect (silent meteor suppression
scaling with load frequency), found by you, fixed by the F02 rewrite but not
identical to F02. An index entry keeps it visible if the rewrite slips; the
repair record then lives in one place.

**D2 — MeteorFrequency restart semantics. Recommend the one-shot latched heal
(5.3-d).** One GameVar (`SMRFixPack_*`, absent-tolerant per FIX_POLICY §3),
one re-roll per save lineage as the total cost, shipped precedent in
`RefreshRainsLoops`, and it is the only option that also clears old bodies out
of existing saves. Fallback if you want zero new GameVars: (c) + the NewDay
dead-thread watchdog, accepting one thread death + ≤1 sol of silence per
upgraded save.

**D3 — BombardmentSpread, decided on corrected facts.** Options: **(i)** keep
the fix, accept the corrected residual (rare — a save must land inside a
~2-minute volley window on a 10-20-sol cycle — but the harm when hit is a
permanently wedged Mystery-7 bombardment loop, not one volley); **(ii)** drop
the fix entirely — removes the exposure at the cost of re-shipping the vanilla
same-line-volley defect; **(iii)** layer 1 for this one module — still barred
by your own decision and I do not recommend reopening it. **Recommend (i)**,
with the corrected text in the docs (done) and the option of revisiting if a
report ever matches the signature. The deciding fact for me: the vanilla
defect the fix cures is real and player-visible every volley, the residual
fires only on the uninstall-after-mid-volley-save path.

**D4 — The Tier-3 control leg.** No longer needed for the build (§2.11 is
source-verified module by module). Run it only if you want one measured datum
on file for the tiering; half a session by the PT-20 method.

**D5 — The exposure list's definition.** Recommend the list track **capturable
modules** with a disposition column (exposed-harmful / compliant-inert), i.e.
count 13 including ShelterReflex and CaveInsNoDisasters. A list that only
contains harmful sites invites the next "safe by construction" overclaim; the
disposition column is where the nuance lives.

---

*Method note: every Src citation above was read in
`A:\SteamLibrary\steamapps\common\Project Spark\ModTools\Src` this session
(read-only); pack citations in `Code/` at commit `0450fd1`; log citations in
`%AppData%\Surviving Mars Relaunched\logs`, files of 2026-07-31. The analysis
tool was re-run against Src today. Nothing in `Code/` or the game directory
was modified.*
