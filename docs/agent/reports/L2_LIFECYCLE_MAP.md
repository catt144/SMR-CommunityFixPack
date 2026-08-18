# L2 — lifecycle & idempotency map

**Pre-launch sweep chain, link 2, 2026-08-18.** Lens L2: *what happens on the
SECOND apply, and does any module wrap its own wrapper?* Coverage row in
`prompts/prelaunch-sweep/SWEEP_LEDGER.md`; findings in `SWEEP_FINDINGS.md`.

⚠️ Every number here was emitted or measured this sitting. Nothing is inherited.
Configuration is named per row: **archive** = two real retail sessions already in
`docs/archive/`; **Src** = re-derived from `ModTools\Src` by symbol; **sim** =
`tools/l2_reload_sim.py`, which runs the pack's own shipped source under Lua 5.4.

---

## 1 · The question, made precise

"Second apply" is not one thing. There are exactly three ways our code can run
twice, and only one of them is reachable by a player today.

| # | route | reachable? | evidence |
|---|---|---|---|
| A | **`ReloadLua` — mod code re-executed in the SAME process** | ⭐ **YES, and easily** | `ModsUIDialogEnd` reloads when the Mod Manager dialog CLOSES after any change (`ModManager.lua:123-165`) → `ModsReloadItems` → `if reload_lua then ReloadLua() end` (`Mod.lua:2145-2147`); `reload_lua` is set by ANY loaded mod having code (`:2100`, `:2115`), and ours does. **Measured twice** — see §3 |
| B | `run_apply` twice in ONE Lua load | ⛔ **dead today** | the only second caller is `OnMsg.ApplyModOptions` → `run_apply` for `def.optional` entries (`00_Core.lua:432-481`); doccheck emits **0 files carry `optional = true`**, and the pack has no Mod Options page |
| C | a DataPatch/OnDataReady **pass** several times in one load | YES, by design | `ClassesBuilt` · `ModsReloaded` · `DataLoaded` · `DataChanged`, all guarded by `ctx.patched` / `ever_changed` |

⛔ Route A is the whole story. A player who ticks our mod at the main menu gets
**one** load; a player who then opens the Mod Manager again and changes anything
gets a **second** — with the game's Lua reloaded underneath our modules and the
game's *data* not reloaded at all.

## 2 · What survives a `ReloadLua` and what does not — the table this lens needed

`ReloadLua` (`lib.lua:353-382`) posts `Msg("ReloadLua")`, collects garbage, and
`dofile`s `CommonLua/Core/autorun.lua`, which re-runs `dofolder("Lua")` then
`ModsLoadCode()` (`autorun.lua:423-424`) and finally `Msg("Autorun")`, whose
`classes.lua:980` handler rebuilds every class and posts `ClassesBuilt` (`:1099`).
⭐ **It never touches the thread register, and it never re-runs `LoadData`.**

| surface a fix can land on | rebuilt by `ReloadLua`? | route (Src) |
|---|---|---|
| game **global function** (`function F()` under `Lua/`) | ✅ YES | `dofolder("Lua")`, `autorun.lua:423` |
| **class method** | ✅ YES | class globals are cleared first (`classes.lua:37-38`), classdefs rebuilt (`:57-72`), `g_Classes` tables cleared and refilled (`:1006-1013`, `:1083-1085`) |
| **`OnMsg` registration** | ✅ YES (discarded, then re-registered) | `local message_to_staticfuncs = {}` is a plain file-local, **not** under `FirstLoad` (`cthreads.lua:6`) |
| **`PeriodicRepeatInfo` slot** | ✅ YES | `PeriodicRepeatInfo = {}` unguarded (`lib.lua:1532`), and a running repeat re-reads `PeriodicRepeatInfo[name]` **every iteration** (`:1568-1594`), so it picks up the new body |
| **preset / shipped data** | ⛔ **NO** | `Presets = rawget(_G,"Presets") or {}` (`Preset.lua:1339-1340`) and `LoadData` is called only from `LoadDlcs`, not from autorun (`Dlc.lua:636-668`) |
| **`const`** | ⛔ NO | `SetupVarTable(const, …)` only under `FirstLoad` (`const.lua:1-3`); `const.LuaReloads` increments across reloads (`lib.lua:367`) |
| **`GameVar` value** | ⛔ NO (correctly) | `if FirstLoad or rawget(_G,name) == nil` — a non-nil value is left alone (`lib.lua:1049-1051`) |
| **real-time / game-time threads** | ⛔ NO | `ReloadLua` never enters `ThreadsRegister`; `ClearGameThreads` runs only on `NewGame`/`DoneGame` (`cthreads.lua:82-93, 101-113`) |
| **the mod env table + `SMRFixPack`** | ⛔ NO | `env._G = env` and `ModEnvMeta.__newindex` rawsets into the REAL `_G` (`Mod.lua:1557-1563, 1599-1611`); proven in this repo by the `order` double-listing fixed in `2f077e8` |

⭐ **FACTS CANDIDATE (not filed, following link 1's precedent for L1-F4):** the
table above is a reusable engine truth this project has never recorded, and every
future preset-patching module needs it. It belongs in `docs/agent/facts/` as one
fact — *"what a `ReloadLua` rebuilds and what it does not"* — but filing it is a
doc build, not a sweep, so it is routed to the terminal audit rather than done
here.

⭐ **The hazard is one mismatch:** a fix whose *edit* lands on a NON-rebuilt
surface while its *"have I already done this?"* state lives on a rebuilt one.
That is the entire finding set below.

⚠️ One route worth naming because it is the opposite of what a reader expects:
`rawget(_G, "X")` from mod code reads the **real** global (`env.rawget =
safe_rawget`, `Mod.lua:1576-1582`), and mod writes go straight to the real `_G`
without leaving a copy in the env — so no module can be holding a stale load-1
global. That is why §4 comes out clean.

## 3 · The measurement — two real sessions that already ran mod code twice

`grep -c "\[CommunityFixPack\] .*: applied"` over all **58** pack-carrying logs in
`docs/archive/` (configuration: **archive**, all-three-mods rig, unpacked):

| logs | `applied` lines | reading |
|---|---|---|
| 56 | 74 · 75 · 76 · 81 · 82 (one per registered module) | one Lua load |
| **2** | **148 = 2 × 74** | ⭐ **two Lua loads in one process** |

The two are `spowner_Mars.exe-20260812-18.30.09.log` and
`rs_ownertick_Mars.exe-20260813-11.16.44.log` — both sessions that spent an owner
Mod-Manager tick, which is exactly route A.

Splitting each at the second occurrence of the first module id and diffing the two
blocks as SETS gives an identical answer in both sessions:

```
load1 lines: 80    load2 lines: 79
LOAD 1 only (5):  SaintBlessing: inactive (no dome-colonists trait presets)
                  LastTransmissionStorage: 6 storage condition(s) made effective, 1 retargeted
                  IndependenceTerraforming: … now discounts special projects by 20% as its param1 says
                  SaintBlessing: corrected 1 dome-colonists trait modifier label(s) of 2
                  AstrogeologistExtractors: added 2 missing extractor entr(y/ies) … (10 already present)
LOAD 2 only (4):  LastTransmissionStorage:  inactive (the shipped presets are already correct)
                  IndependenceTerraforming: inactive (the shipped tech already matches its own param1)
                  SaintBlessing:            inactive (every dome-colonists trait preset already names a real label)
                  AstrogeologistExtractors: inactive (the shipped profile already pays every buildable extractor)
```

⭐⭐ **That is the pack's ENTIRE second-load delta.** 71 of 75 modules are
byte-identical across the two loads. The four that are not all say the same false
thing: *the shipped data is already correct*. It is correct because **we** corrected
it on load 1, and the correction survived the reload while the module's memory of
having made it did not.

⛔ `update report:` appears **0 times in all 58 archived logs** — the deactivation
dialog has never fired in anything this project has archived. Its only witness is
the 2026-08-17 upload sitting, whose log is not in `archive/`.

## 4 · The mechanical census — every patch site against the table in §2

Extracted this sitting from all **76** `Code/*.lua`: **284** table-field assignment
sites, grouped by root symbol. Sites whose root is a mod-local (`ctx`, `stats`,
`seen`, `owned`, …) or a live game object (`self`, `drone`, `track`, …) are not
lifecycle-relevant and are not listed. What remains:

| class of patch | count | reload verdict | how checked |
|---|---|---|---|
| **global function replacement** | **13** | ✅ clean — every target is a plain top-level `function F()` under `Lua/`, so the reload restores vanilla before we re-wrap | each name looked up in Src: `TriggerCaveIn` `CaveInRubble.lua:94` · `FindCaveInLocation` `:21` · `PlanetaryAsteroidVisitPossible` `PlanetaryView.lua:433` · `WaitBombard` `Bombardment.lua:55` · `GetDustDevilsDescr` `DustDevils.lua:58` · `OverrideDisasterDescriptor` `MapSettings.lua:31` **and** `TerraformingDisasters.lua:54` · `GetRareTraitChance` `Colonist.lua:3541` · `GetGridGlobalStorage` `ResourceOverview.lua:891` · `GetDisasterWarningTime` `MapSettings.lua:94` · `CompleteMilestone` `Milestones.lua:108` · `RainsDisasterActivation` `TerraformingDisasters.lua:276` · `IsLRTransportAvailable` `ShuttleHub.lua:350` · `ExpandTrackFromElement` `TrackElement.lua:714` |
| **`OnMsg` registration** | **23** (+8 in `00_Core`) | ✅ clean — store discarded per load, so exactly one registration per load | `cthreads.lua:6`; also checked all 14 distinct message names against `ModMsgBlacklist` (`Mod.lua:1430-1440`) — **0 hits**, so none is silently dropped |
| **`PeriodicRepeatInfo` slot** | 1 (`Fix_CaveInsNoDisasters:35`) | ✅ clean, twice over | table rebuilt (`lib.lua:1532`) **and** a live repeat re-reads its body each iteration (`:1568-1594`) |
| **`GameVar` once-flag** | 1 (`Fix_FirstAsteroidPrefabs:115`) | ✅ clean — a set flag is NOT reset by the reload | `lib.lua:1049-1051` |
| **class / template field write** | 3 (`Fix_SinkholeIndestructible:102,107`, `Fix_ExoticDepositSign:72`) | ✅ clean — absolute writes, and the class half is rebuilt so it re-applies | archive shows Sinkhole logging its success line on **both** loads |
| **in-place preset data edit** | **9 sites in 7 modules** | ⚠️ **the hazard class** — see §5 | |
| **real-time thread at file scope** | 1 (`00_Core.lua:545`) | ⚠️ one new thread per Lua load — see L2-F2 | `cthreads.lua`; contrast `autorun.lua:353-357`, where the engine guards its own startup thread with `if FirstLoad` |

Preset-edit sites, and whether the edit is idempotent against data that survives:

| module | site | shape | second-load behaviour |
|---|---|---|---|
| `Fix_AstrogeologistExtractors` | `:137` `profile[#profile+1]` | **append**, but searched-for first by `Label` (`:118-129`) | ✅ adopts, never duplicates |
| `Fix_DustSicknessBiorobots` | `:89` `filters[#filters+1]` | append into a storybit filter list, guarded by `has_android_filter(filters)` (`:86`) | ✅ never duplicates, and its no-op branch is silent — it has **no** "already correct" latch to fall into (`:150-154`) |
| `Fix_DustSicknessDamage` | `:60` `trait.daily_update_func = …` | absolute set | ✅ re-set to the current load's closure |
| `Fix_IndependenceTerraforming` | `:84` `effect.Amount = WANTED` | absolute set | ✅ value idempotent — ⛔ **status not**, see L2-F1 |
| `Fix_LastTransmissionStorage` | `:122-123` field move, `:130` absolute, `:134` closure | guarded by `if not like.Condition` | ✅ value idempotent — ⛔ **status not** (L2-F1); ⚠️ closure lifetime, see L2-F3 |
| `Fix_SaintBlessing` | `:103` `p.modify_trait = get_label(raw)` | guarded by `get_label(raw) ~= raw` | ✅ value idempotent — ⛔ **status not**, see L2-F1 |
| `Fix_TechDescriptionBuilding` | `:75` `tech.description = T(…)` | absolute, gated on the wrong literal still being present (`:63-74`) | ✅ status stays `active` — this site latches nothing. ⚠️ its diagnostic `SMRFixPack.TechDescriptionBuilding.result` reads the decline string on load 2, because that table is rebuilt each load (`:79`) — same family as L2-F1, no player consequence |
| `Fix_DustDevilSpawnGate` | `:243-245` on a **copy** it builds (`:173-201`) | copy, not an in-place preset edit | ✅ the shipped preset is never mutated, so there is nothing to be idempotent about |
| ~~`Fix_SequenceLatents:104`~~ | — | ⚠️ **census correction:** `objs[i] = nil` is a runtime write to a `table.icopy` returned inside a class-method wrapper (`:92-108`), **not** a preset edit — class methods are rebuilt, so it is reload-clean | |

⭐ **Answering the lens's headline question directly: no module wraps its own
wrapper, anywhere, on any route.** The three ways it could have happened were all
closed by the engine and each was checked rather than assumed — the global targets
are re-executed, the class targets are cleared and rebuilt, and the mod env keeps
no shadow copy of either.

## 5 · L2-F1 — the four modules that lie about themselves on the second load

**Root cause, one sentence:** `ctx.ever_changed` was seeded `false` on every Lua
load, but the data it describes lives for the whole **process**, so on load 2 the
pass sees `changed == 0` with no memory of why and falls to its site's *"the
shipped data is already correct"* latch.

⛔ **The cost is not cosmetic.** Three save-repair paths are gated on the entry
reading `active` and stop running for the rest of the session:

| repair | gate | what a player loses |
|---|---|---|
| `Fix_AstrogeologistExtractors` `OnMsg.LoadGame` (`:174`) | `SMRFixPack.WhenActive` | a save begun before this fix never receives the two extractor modifiers |
| `Fix_IndependenceTerraforming` sweep (`:126-128`) | its own `entry.status == "active"` test | a save that researched the tech keeps the wrong −10% discount |
| `Fix_SaintBlessing` `OnMsg.LoadGame` (`:151`) | `SMRFixPack.WhenActive` | dome Saints keep their blessing filed under the raw label (⚠️ also blocked a second way — `rebased_from` is per-load and empty on load 2) |

`Fix_LastTransmissionStorage` has no heal, so its loss is the status line only.

⚠️ **A fourth consequence, PREDICTED FROM SOURCE and deliberately not claimed as
measured:** the TestKit's `fix_missing` helper returns **`FAIL`** — not SKIP — for
any fix whose status is not `active` (`00_TestCore.lua:314-326`), and the
`SaintBlessing` (`57_Probes_Wave8.lua:128`) and `AstrogeologistExtractors`
(`:320`) probes open with it. ⇒ a suite run in a session that had reloaded would
have reported **2 false FAILs**. ⛔ **This has never been observed**, because
neither two-load session ran the suite (14 `SMRTEST` lines each, against 96
probes) — so every `80/0/16/0` reading this project owns is a **single-load**
reading, and that is now part of what "configuration" means for this pack. The
`LastTransmissionStorage` and `IndependenceTerraforming` probes read the DATA
rather than the status and would have passed either way.

⚠️ **What it is NOT:** all four second-load latches pass `benign`, so
`update_suspect` is never set and **the "check for a new version" dialog cannot
fire from this**. That is the `2f077e8` design holding. The two defects are
siblings — same file, same root, same week — but distinct, and this one was left
standing.

**The fix (`00_Core.lua`):** seed `ctx.ever_changed` from, and write it back to, a
per-process memo `SMRFixPack.data_edited[id]`, which rides the one table that
survives a reload. The B3 branch (*"nothing left to change is SUCCESS"*) then spans
the reload, which is the lifetime it always meant. A new process starts with an
empty memo, so a future game patch that genuinely fixes the shipped data still
latches benign on its first load.

### Falsifier — `tools/l2_reload_sim.py` (configuration: **sim**)

Runs the pack's own shipped `00_Core.lua` and the four modules under Lua 5.4
(`lupa`), twice in one process, reproducing the engine's persistence rules from §2:
`SMRFixPack` and the preset fixtures persist, the `OnMsg` store is discarded, the
classes are rebuilt, `LoadData` is not re-run on the second load.

| run | result |
|---|---|
| **control** — does the harness reproduce the archive? | ⭐ **load 1 emits all 5 archived load-1 lines, verbatim and in order**, including SaintBlessing's empty-preset line, and nothing else |
| **pre-fix** | load 2 reproduces **4 of 4** archived false-`inactive` lines; 4 modules not `active` |
| **post-fix** | load 2 emits **0 of 4**; **0** modules not `active`; load 1 output byte-identical to pre-fix |
| **negative control** — fixtures rewritten to the state a future game patch would ship | all four still latch `inactive` with their benign verdict on **both** loads (`--negative-control`, exit 0) |

⚠️ **Scope of this evidence, stated plainly:** the harness executes our real source
against stub engine globals. It is not a launch. It proves the branch taken and it
reproduces a real measurement, but ⛔ **the fix has not run inside Surviving Mars**
— and neither have the two `2f077e8` core fixes it sits beside. One unattended
launch that performs a `ReloadLua` would close all three at once; the design for it
is in `SWEEP_FINDINGS.md`.

## 6 · What this lens could not reach

- ⛔ **Nothing was run in a game.** No launch this link.
- ⛔ **Mid-game reload.** Every route A caller found is main-menu or Ged; whether a
  reload can happen with a colony loaded — and what our wrappers do to live objects
  if it can — is **unmeasured**.
- ⛔ **Third and later loads.** Both archived sessions stop at two. The §2 table
  predicts load 3 = load 2, but it is a prediction.
- ⛔ **The TestKit's own second-load behaviour** — `Code/` only, again.
- ⛔ **Uninstall / disable mid-session**, save footprint, and whether anything of
  ours is left behind by a reload → **L3**.
- ⛔ **Runtime cost of 75 modules re-applying** — still never measured by anything.
- ⛔ Whether a **foreign** mod's reload interacts with ours → **L8**.
