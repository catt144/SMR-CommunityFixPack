# C74 + C77 build — restore the silent hit-moment FX of seven units (model-agnostic)

⛔ ONE-SHOT: `git rm` this file at close-out. **TAKEABLE WHEN the owner rules
checklist 139 = build.** If 139 says "file and watch", do nothing here; if it
names a subset, build only that subset (C74's conversion is needed only for the
hammer + MOXIE rows). Written 2026-09-10 by the dispatch session that found and
live-proved the fix; widened to C77's five units the same day from the silent-FX
handoff (`HANDOFF_SOUNDFX_2026-09-10.md` §2, retired into this file). Verify every
specific against `git log` and the trees before trusting it.

## 0 · Read first
`git log --oneline -10` + `git pull` + `git status --short` (+ `ListAgents` where
available — other sessions commit here). Then:
`agent/STATE.md` · `prompts/DISPATCH.md` §1–§2 (bindings) · `agent/bugs/C74.md`
and `agent/bugs/C77.md` (the whole cases; each **Fix shape** section holds the
exact times) · `agent/facts/EF-086.md` (moments = name-keyed Lua presets; the
index trap) · `EF-058` (classdef-time vs runtime patching) · `EF-019`/`EF-022`/
`EF-023`/`EF-072` (what enters a save) · `EF-031` · `agent/FIX_POLICY.md` §1, §2,
§2a, §2b, §3a, §4a · `reports/REACHABILITY_AUDIT.md` "Challenge review". Sweep
that found C77: `agent/reports/C74_SOUND_SWEEP.md`.

## 1 · Live todo list from your first action — one item per step below, updated as each finishes.

## 2 · Steps

1. **Enumerate before choosing the wrap site.** Every call of
   `GetAnimMoments` / `GetAnimMomentsCount` / `GetAnimMoment` / `IterateMoments` /
   `TimeToMoment` / `GetEntityAnimMoments` in BOTH trees, each classed as passing a
   state NAME or a numeric INDEX (`obj:GetAnim(n)` / `GetState()` = index). Known
   broken: `BaseBuilding:TrackMultipleHitMoments` (1.1.0 `:1045-1046`, `:1053`,
   `:1065`), `Metatron.lua:52-57`. ⚠️ `AnimMoment.lua:17` aliases
   `local GetEntityAnimMoments = GetEntityAnimMoments`, so replacing the GLOBAL
   does not reach `CObject:GetAnimMoments`. Pick the narrowest site that covers
   the tracker + Metatron; write the enumeration into C74. (The live proof
   wrapped the pump's/hammer's own class `GetAnimMoments`, §3.)
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
   geometric) the owner may glance at (checklist 139); they are proven to FIRE.
   **Metatron (C74): owed** — only if the owner wants a sitting (rare mystery
   unit): its 7 `End1..7` particles are fixable the same way but untimed. Its 7
   rotate SOUNDS are unreachable (the thread emits only `Start`/`End`,
   `Metatron.lua:78`, `:86`) — never promise them. Resolve
   `GetAnimEntity(entity, state)` for any further group before keying a preset
   (`EF-086` ⚖️).
3. **The Water Extractor restart (C77 only).** `WaterExtractorBase:OnSetWorking`
   starts `TrackAllMoments(pump, "working", self)` (`WaterExtractor.lua:112-115`)
   while the pump is still at anim speed 0 (`BaseBuilding.lua:1009`); speed
   returns to 1000 only in the `Notify`-queued `UpdateWorkingStateAnim` (`:1092`,
   `:945`), so the first `TimeToMoment` sleeps `max_int` (`AnimMoment.lua:117-119`)
   — alive, silent. Proven fix: (re)start the tracker once the pump runs. Design
   the hook point (e.g. after the working anim/speed is applied) and show it
   survives a power cycle AND a save load.
4. **Build** one module (FIX_POLICY shape): `-- SRC:` + `-- DEFECT:` headers
   (`python tools/bodycheck.py --pin …`); `Require` gates; the conversion installed
   at classdef time (file-scope `Register`, safe per `EF-058` amended); presets
   registered only where `Presets.AnimMetadata[group][id]` is absent (vanilla may
   ship presets later — the falsifier in both entries); §2a guard = a BEHAVIOUR
   probe (does an index already resolve a known preset?), never a version check.
   `items.lua` entry (H-10). `python tools/parsecheck.py`, doccheck.
5. **Save-safety (§3a):** presets and class methods are not persisted (class
   tables never reach a save, `EF-072`); the tracker threads are vanilla's own
   (`track_multiple_hit_thread`, `anim_moments_thread`). Confirm no mod closure
   lands on a persisted object (`EF-022`) — the Water Extractor restart is the
   one place that could — and walk uninstall.
6. **Desk control** with a lupa harness loading the shipped `AnimMoment.lua` /
   `BaseBuilding.lua` bodies under their real names (memory: desk harness shims):
   index in → preset found; a negative control where the guard must decline.
   ⛔ A control must test the premise, not only the arithmetic — the first C74
   probe passed its desk control and failed in game (root-bound spots).
7. **Attended check with the owner:** pack on — every built unit heard/seen once;
   drill and CP3 MOXIE stay silent (by design); nothing else changes. ⛔ The
   Water Extractor across a power cycle AND a reload. Readout via a prefixed
   `print` line + a LOG FLUSH, not screenshots; proof via a log-only `PlayFX`
   hook (memory `sound-bug-test-method` — ear A/B alone was wrong twice).
8. **Patch note** (post-launch maintenance, not the release gate): explain the two
   skins — the Rare Metals drill skin and the white (CP3) MOXIE are silent by
   design — with the owner's screenshots in `agent/reports/c74_skins/` (dev
   captures, fine to publish as they are).

## 3 · Proven console lines (1.1.0, attended 2026-09-10; gone at quit; do not save during)
- Readout: `local l = {SelectedObj} for _, a in ipairs(SelectedObj:GetAttaches() or {}) do l[#l+1] = a end for _, a in ipairs(l) do if a:HasEntity() then print(a.class, a:GetStateText(), a:GetAnimMomentsCount(a:GetAnim(1), "Hit")) end end print("hit thread live:", IsValidThread(SelectedObj.track_multiple_hit_thread))`
- Preset (swap group for `MoxiePump`): `local p = SelectedObj:GetAttach("UniversalExtractorHammer") local d = p:GetAnimDuration() PlaceObj('AnimMetadata', {group = "UniversalExtractorHammer", id = "working", Moments = { {Type = "Hit", Time = MulDivRound(d, 1, 4)}, {Type = "Hit", Time = MulDivRound(d, 3, 4)} }})`
- Conversion (class-level; a runtime `CObject` patch would miss flattened subclasses): `local p = SelectedObj:GetAttach("UniversalExtractorHammer") local cls = g_Classes[p.class] local orig = cls.GetAnimMoments cls.GetAnimMoments = function(self, anim, t) if type(anim) == "number" then anim = GetStateName(anim) end return orig(self, anim, t) end`
- Then power the building off and on (restarts the vanilla tracker).
- C77 units' proof lines: each unit's section in `agent/bugs/C77.md`.

## 4 · Fence
Never the game dir or the source archives. No `metadata.lua` version edits (H-02),
no Mod Editor, no upload. Our pack and TestKit touch none of this path today.

## 5 · Close-out
C74 + C77 status per the result; STATE only if the kernel changed; SESSION_LOG;
commit with `git commit -F <msg> -- <paths>`, push; `git rm` this prompt.
