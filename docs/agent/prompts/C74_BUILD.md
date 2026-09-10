# C74 + C77 build — restore the silent hit-moment FX of seven units (model-agnostic)

⛔ ONE-SHOT: `git rm` this file at close-out. ✅ **TAKEABLE NOW — the owner ruled
checklist 139 = BUILD on 2026-09-10**: all seven proven units (C74 hammer + MOXIE,
C77 Water Extractor, Shuttle, RC Driller, RC Dozer, Excavator). **Metatron is OUT**
unless the owner adds it. Steps 1–7 run unattended; step 9 needs the owner at the
keyboard — ask for it in ONE batched request when you reach it. Written 2026-09-10
by the dispatch session that found and live-proved the fix, widened the same day
with the owner's two patch-safety questions (§3). Verify every specific against
`git log` and the trees before trusting it.

## 0 · Read first
`git log --oneline -10` + `git pull` + `git status --short` (+ `ListAgents` where
available — other sessions commit here). Then:
`agent/STATE.md` · `prompts/DISPATCH.md` §0–§2 (bindings; §0.4 stale-probe gate
binds before step 9's launch) · `agent/bugs/C74.md` and `agent/bugs/C77.md` (the
whole cases; each **Fix shape** section holds the exact times) ·
`agent/facts/EF-086.md` (moments = name-keyed Lua presets; the index trap) ·
`EF-058` (classdef-time vs runtime patching) · `EF-019`/`EF-022`/`EF-023`/`EF-072`
(what enters a save) · `EF-029` (`CreateGameTimeThread` defers) · `EF-031` ·
`agent/FIX_POLICY.md` §1, §2, §2a, §2b, §3a, §4a · `reports/REACHABILITY_AUDIT.md`
"Challenge review". Sweep that found C77: `agent/reports/C74_SOUND_SWEEP.md`.

## 1 · Live todo list from your first action — one item per step below, updated the moment each finishes (the owner reads it to decide when to step in).

## 2 · Steps

0. **Challenge §3 before coding.** §3's old-save table and the dev-fix rules were
   DESK-DERIVED in conversation (source reads, nothing run). Re-derive each claim
   from the 1.1.0 tree (and check 1.0.7 for §2a). One that fails changes the
   design: fix the design here, and if it changes what the owner was told (no
   player action needed; declines clean; worst case doubled sound), route that to
   checklist 139 before building.
1. **Enumerate before choosing the wrap site.** Every call of
   `GetAnimMoments` / `GetAnimMomentsCount` / `GetAnimMoment` / `IterateMoments` /
   `TimeToMoment` / `GetEntityAnimMoments` in BOTH trees, each classed as passing a
   state NAME or a numeric INDEX (`obj:GetAnim(n)` / `GetState()` = index). Known
   broken: `BaseBuilding:TrackMultipleHitMoments` (1.1.0 `:1045-1046`, `:1053`,
   `:1065`), `Metatron.lua:52-57`. ⚠️ `AnimMoment.lua:17` aliases
   `local GetEntityAnimMoments = GetEntityAnimMoments`, so replacing the GLOBAL
   does not reach `CObject:GetAnimMoments`. Pick the narrowest site that covers
   the tracker (Metatron is out of scope, but note whether the site would reach
   it); write the enumeration into C74. (The live proof wrapped the pump's/hammer's
   own class `GetAnimMoments`, §4.)
2. **Times — all live-proven 1.1.0.403908, owner attended 2026-09-10.** Group/id
   = the `GetAnimEntity` result, MEASURED. ⛔ Keep each unit's moment TYPE.

   | group / id | moments | notes |
   |---|---|---|
   | `UniversalExtractorHammer` / `working` | `Hit` 3083, 9250 (of 12,333) | C74 — needs the conversion; "perfectly in sync" |
   | `MoxiePump` / `working` | `Hit` 3325, 9975 (of 13,300) | C74 — needs the conversion; "works and in sync" |
   | `WaterExtractorCP3Pump` / `working` | `Hit` 1667, 5000 (of 6,667) | C77 — + tracker restart (step 3) |
   | `WaterExtractorPump` / `working` | `Hit` 1658, 4975 (of 6,633) | C77 — + tracker restart |
   | `Shuttle` / `landing`, `landing2` | `Hit` 1033 (of 2,067) | C77 — both hub skins; classic ShuttleHub only |
   | `Shuttle` / `takeOff`, `takeOff2` | `Hit` 2500 (of 5,000) | C77 — the Jumper hub is NOT a unit |
   | `RoverRussiaDriller` / `workIdle` | `Hit` 2708, 8125 (of 10,833) | C77 — Roscosmos-only for players (the owner's colony has it by cheat) |
   | `RoverTerraformer` / `workIdle` | **`Hit1`** 1083, 3250 (of 4,333) | C77 "RC Dozer" — the Load phase carries the sound |
   | `ExcavatorShovel` / `working` | 24: `Hit`*i* at `MulDivRound(40000, i-1, 12)`, `Out`*i* = that + 20000 mod 40000 | C77 — ⛔ SORT by Time: `IterateMoments` walks list order |

   The shuttle, Dozer and Excavator times are first guesses (midpoint / ¼-¾ /
   geometric), proven to FIRE; the owner may glance at their timing in step 9.
   Metatron (out of scope): its 7 `End1..7` particles are fixable the same way but
   untimed; its 7 rotate SOUNDS are unreachable (`Metatron.lua:78`, `:86` emit only
   `Start`/`End`) — never promise them.
3. **The Water Extractor restart.** `WaterExtractorBase:OnSetWorking` starts
   `TrackAllMoments(pump, "working", self)` (`WaterExtractor.lua:111-116`) while the
   pump is still at anim speed 0 (`BaseBuilding.lua:1009`); speed returns to 1000
   only in the `Notify`-queued `UpdateWorkingStateAnim` (`:1092`, `:945`), so the
   first `TimeToMoment` sleeps `max_int` (`AnimMoment.lua:117-119`) — alive,
   silent. Proven fix: (re)start the tracker once the pump runs. Design the hook
   point (e.g. after the working anim/speed is applied). ⛔ **REPLACE, never add**:
   delete `self.anim_moments_thread` before starting a new one (vanilla's own
   pattern: `StopTrackingMultipleHitMoments`, `BaseBuilding.lua:1031-1035`, called
   first at `:1042`) — one tracker per building, always, so a vanilla start-order
   fix makes ours a redundant restart, never a doubled sound (§3 row 3).
4. **The old-save load pass (§3 table A).** On game load, once: for each Rare
   Metals Extractor (hammer skin), classic MOXIE, Water Extractor and Excavator
   that is working AND has no live tracker, start that tracker by calling the
   game's OWN start routine with the exact arguments vanilla uses — hammer/MOXIE:
   `self:TrackMultipleHitMoments(obj, "Working", nil, <override as :947>, true)` on
   the attach playing the work loop (`BaseBuilding.lua:940-948`); Water Extractor:
   the same call as step 3; Excavator: ONLY
   `self.dig_fx_thread = TrackAllMoments(self.arm, "ExcavatorDigging", self.arm)`
   (`TheExcavator.lua:120`) — its restart is gated on `dig_anim_thread`, which is
   still alive in an old save (`:116`). ⛔ Never re-run `UpdateWorkingStateAnim` /
   `OnSetWorking` for this: it replays start animations and FX (visible hiccup).
   ⛔ Gate every start on "no live tracker" so a vanilla load restart (added later)
   and ours never both run (§3 row 4). Pick the load message from `EF-028`'s hook
   list and confirm when the threads resume relative to it. Shuttle, RC Driller and
   RC Dozer need NOTHING (they restart per flight / job / task, §3 table A).
5. **Build** one module (FIX_POLICY shape): `-- SRC:` + `-- DEFECT:` headers
   (`python tools/bodycheck.py --pin …`); `Require` gates; the conversion installed
   at classdef time (file-scope `Register`, safe per `EF-058` amended); presets
   registered only where `Presets.AnimMetadata[group][id]` is absent; §2a guard =
   a BEHAVIOUR probe (does an index already resolve a known preset?), never a
   version check. ⛔ **Guard timing (§3 row 1):** the "absent" test is only true if
   every game AND DLC `AnimMetadata` preset (e.g. `DLC/norman/Presets/AnimMetadata.lua`)
   is already registered when ours run. MEASURE the order (mod `Code/` load vs
   preset/DLC load), and read what `Preset` registration does with a duplicate
   group/id (`CommonLua/Preset.lua:562-581`, `:667-676`). If mods can load first,
   register at a later point (game start/load), not file scope. `items.lua` entry
   (H-10). `python tools/parsecheck.py`, doccheck.
6. **Save-safety (§3a):** presets and class methods are not persisted (class
   tables never reach a save, `EF-072`); the tracker threads are vanilla's own
   (`track_multiple_hit_thread`, `anim_moments_thread`, `dig_fx_thread`). Confirm no
   mod closure lands on a persisted object or below a yield on a game-time thread
   (`EF-022`, `EF-023`) — steps 3 and 4 are the places that could: our code may
   only CALL the vanilla starters, never be the thread body. Walk uninstall: a save
   made WITH the module, then loaded without it — trace what each blocked vanilla
   tracker does when it wakes to no markers (must be vanilla's silence, no error).
7. **Desk control** with a lupa harness loading the shipped `AnimMoment.lua` /
   `BaseBuilding.lua` / `Building.lua` bodies under their real names (memory: desk
   harness shims): index in → preset found; guard declines when a preset already
   exists; load pass starts exactly one tracker, and none when one is live.
   ⛔ A control must test the premise, not only the arithmetic — the first C74
   probe passed its desk control and failed in game (root-bound spots).
8. **Post-update check, written into C74 + C77:** a line that after any game
   update someone listens once for DOUBLED hit sounds and runs each entry's
   falsifier — the one dev-fix route our guards cannot see (§3 row 6).
9. **Attended check with the owner** (one batched ask; readouts = a prefixed
   `print` line + a LOG FLUSH, proof via a log-only `PlayFX` hook — memory
   `sound-bug-test-method`; ear A/B alone was wrong twice). Pack on:
   (a) **old save, first load** (every existing save predates the module): the
   four table-A units that were running at save time sound WITHOUT a power cycle;
   (b) every built unit heard/seen once; drill and CP3 MOXIE stay silent (by
   design); (c) ⛔ the Water Extractor across a power cycle AND a reload;
   (d) save with the pack on, reload — still sounding; (e) the `applied` boot line.
10. **Patch note** (post-launch maintenance, not the release gate): explain the two
   skins — the Rare Metals drill skin and the white (CP3) MOXIE are silent by
   design — with the owner's screenshots in `agent/reports/c74_skins/` (dev
   captures, fine to publish as they are). Route it to the next release's inbox
   (`prompts/RELEASE_OUTBOX.md`, per its header) — shipping is the owner's.

## 3 · Design rules — the owner's patch-safety questions, 2026-09-10 (desk-derived; step 0 re-derives)

**A · Old saves need no player action.** Both trackers give up for good when they
start with no markers — `TrackMultipleHitMoments` returns at `BaseBuilding.lua:1047-1049`;
`TrackAllMoments` reads the list once (`Building.lua:3369`) and never enters its loop
(`:3379`). A save made before the module therefore holds dead trackers for units
that were running, and nothing restarts them on load.

| unit | what restarts its tracker | load pass (step 4)? |
|---|---|---|
| Shuttle | every landing / take-off (`ShuttleHub.lua:1632`, `:1649`) | no — heals on the next flight |
| RC Driller | every new drill job (`RCDriller.lua:104-105`) | no |
| RC Dozer | every scoop task (`RCTransport.lua:133-134`) | no |
| hammer, MOXIE | only a stop/start (`BaseBuilding.lua:1092` → `:946-947`) | **yes** |
| Water Extractor | only a stop/start (`WaterExtractor.lua:111-116`) | **yes** (with step 3) |
| Excavator | only a stop/start, gated on `dig_anim_thread` (`TheExcavator.lua:114-120`) | **yes** |

Saves made WITH the module keep their trackers blocked mid-sleep (`EF-019`/`EF-023`)
and resume on load — nothing to do.

**B · If the devs fix it, we decline clean or fail safe:**

| # | the devs… | required behaviour |
|---|---|---|
| 1 | ship the markers | per-group/id skip → theirs win (needs step 5's guard timing) |
| 2 | fix the number-vs-name lookup | conversion touches only numbers; §2a probe declines when an index already resolves |
| 3 | fix the Water Extractor start order | our restart REPLACES (step 3) → redundant, never doubled |
| 4 | add their own load restart | our pass gated on "no live tracker" (step 4); vanilla starters check/replace too |
| 5 | rename/restructure what we hook | `Require` declines the module, a throwing probe is logged not raised (`Code/00_Core.lua:142-165`); rest of the pack runs |
| 6 | fix it by another route (sound from code, not markers) | NOT detectable — our markers still register → doubled sound, cosmetic, no save impact; step 8 is the backstop |

## 4 · Proven console lines (1.1.0, attended 2026-09-10; gone at quit; do not save during)
- Readout: `local l = {SelectedObj} for _, a in ipairs(SelectedObj:GetAttaches() or {}) do l[#l+1] = a end for _, a in ipairs(l) do if a:HasEntity() then print(a.class, a:GetStateText(), a:GetAnimMomentsCount(a:GetAnim(1), "Hit")) end end print("hit thread live:", IsValidThread(SelectedObj.track_multiple_hit_thread))`
- Preset (swap group for `MoxiePump`): `local p = SelectedObj:GetAttach("UniversalExtractorHammer") local d = p:GetAnimDuration() PlaceObj('AnimMetadata', {group = "UniversalExtractorHammer", id = "working", Moments = { {Type = "Hit", Time = MulDivRound(d, 1, 4)}, {Type = "Hit", Time = MulDivRound(d, 3, 4)} }})`
- Conversion (class-level; a runtime `CObject` patch would miss flattened subclasses): `local p = SelectedObj:GetAttach("UniversalExtractorHammer") local cls = g_Classes[p.class] local orig = cls.GetAnimMoments cls.GetAnimMoments = function(self, anim, t) if type(anim) == "number" then anim = GetStateName(anim) end return orig(self, anim, t) end`
- Then power the building off and on (restarts the vanilla tracker).
- C77 units' proof lines: each unit's section in `agent/bugs/C77.md`.

## 5 · Fence
Never the game dir or the source archives. `Mars.exe` NOT running (`tasklist`)
before touching `Code/`, in a separate step. No `metadata.lua` version edits
(H-02), no Mod Editor, no upload, no tag move (H-01). A design-flavoured call →
the checklist, not an agent doc.

## 6 · Close-out
C74 + C77 status per the result (`fixed` after the build; `tested-attended` only
after step 9); checklist 139 receipt; STATE only if the kernel changed (module
count via `doccheck.py --emit-counts`); SESSION_LOG; commit with
`git commit -F <msg> -- <paths>`, push; `git rm` this prompt.
