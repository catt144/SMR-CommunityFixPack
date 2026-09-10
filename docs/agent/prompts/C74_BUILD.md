# C74 build — restore the Rare Metals hammer + MOXIE pump strike FX (model-agnostic)

⛔ ONE-SHOT: `git rm` this file at close-out. **TAKEABLE WHEN the owner rules
checklist 139 = build.** If 139 says "file and watch", do nothing here.
Written 2026-09-10 by the dispatch session that found and live-proved the fix;
verify every specific against `git log` and the trees before trusting it.

## 0 · Read first
`git log --oneline -10` + `git pull` + `git status --short` (+ `ListAgents` where
available — the vanillahunt 03b/03c/03d/04 sessions may be running). Then:
`agent/STATE.md` · `prompts/DISPATCH.md` §1–§2 (bindings) · `agent/bugs/C74.md`
(the whole case) · `agent/facts/EF-086.md` (moments = name-keyed Lua presets; the
index trap) · `EF-058` (classdef-time vs runtime patching) · `EF-019`/`EF-022`/
`EF-023`/`EF-072` (what enters a save) · `EF-031` · `agent/FIX_POLICY.md` §1, §2,
§2a, §2b, §3a, §4a · `reports/REACHABILITY_AUDIT.md` "Challenge review".

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
   the tracker + Metatron; write the enumeration into C74.
2. **Times.** Hammer (`UniversalExtractorHammer` / `working`): `Hit` at **3083**
   and **9250** (¼ and ¾ of the measured 12,333 ms loop) — heard "perfectly in
   sync" by the owner. **MOXIE (`MoxiePump` / `working`): `Hit` at 3325 and 9975**
   (¼ and ¾ of the measured 13,300 ms loop; `GetAnimEntity` → `MoxiePump`,
   MEASURED) — "works and in sync", owner, attended 2026-09-10 (C74 "MOXIE LIVE FIX
   PROVEN"). **Metatron: owed** — only if the owner wants it (rare mystery unit):
   the same placeholder-then-ear sitting. Resolve `GetAnimEntity(entity, "working")`
   for any further group before keying a preset (`EF-086` ⚖️). C77's five units
   (presets only, no conversion) are a separate owner decision in checklist 139.
3. **Build** one module (FIX_POLICY shape): `-- SRC:` + `-- DEFECT:` headers
   (`python tools/bodycheck.py --pin …`); `Require` gates; the conversion installed
   at classdef time (file-scope `Register`, safe per `EF-058` amended); presets
   registered only where `Presets.AnimMetadata[group][id]` is absent; §2a guard =
   a BEHAVIOUR probe (does an index already resolve a known preset?), never a
   version check. `items.lua` entry (H-10). `python tools/parsecheck.py`, doccheck.
4. **Save-safety (§3a):** presets and class methods are not persisted (class
   tables never reach a save, `EF-072`); the tracker thread is vanilla's own
   (`track_multiple_hit_thread`). Confirm no mod closure lands on a persisted
   object (`EF-022`), and walk uninstall.
5. **Desk control** with a lupa harness loading the shipped `AnimMoment.lua` /
   `BaseBuilding.lua` bodies under their real names (memory: desk harness shims):
   index in → preset found; a negative control where the guard must decline.
   ⛔ A control must test the premise, not only the arithmetic — the first C74
   probe passed its desk control and failed in game (root-bound spots).
6. **Attended check with the owner:** pack on — hammer skin and classic MOXIE
   thunk/puff in sync; drill and CP3 MOXIE stay silent (by design); nothing else
   changes. Readout via a prefixed `print` line + a LOG FLUSH, not screenshots.
7. **Patch note** (post-launch maintenance, not the release gate): explain the two
   skins — the drill/CP3 variants are silent by design — with the owner's screenshots
   in `agent/reports/c74_skins/` (dev captures, fine to publish as they are).

## 3 · Proven console lines (1.1.0, attended 2026-09-10; gone at quit; do not save during)
- Readout: `local l = {SelectedObj} for _, a in ipairs(SelectedObj:GetAttaches() or {}) do l[#l+1] = a end for _, a in ipairs(l) do if a:HasEntity() then print(a.class, a:GetStateText(), a:GetAnimMomentsCount(a:GetAnim(1), "Hit")) end end print("hit thread live:", IsValidThread(SelectedObj.track_multiple_hit_thread))`
- Preset (swap group for `MoxiePump`): `local p = SelectedObj:GetAttach("UniversalExtractorHammer") local d = p:GetAnimDuration() PlaceObj('AnimMetadata', {group = "UniversalExtractorHammer", id = "working", Moments = { {Type = "Hit", Time = MulDivRound(d, 1, 4)}, {Type = "Hit", Time = MulDivRound(d, 3, 4)} }})`
- Conversion (class-level; a runtime `CObject` patch would miss flattened subclasses): `local p = SelectedObj:GetAttach("UniversalExtractorHammer") local cls = g_Classes[p.class] local orig = cls.GetAnimMoments cls.GetAnimMoments = function(self, anim, t) if type(anim) == "number" then anim = GetStateName(anim) end return orig(self, anim, t) end`
- Then power the building off and on (restarts the vanilla tracker).

## 4 · Fence
Never the game dir or the source archives. No `metadata.lua` version edits (H-02),
no Mod Editor, no upload. Our pack and TestKit touch none of this path today.

## 5 · Close-out
C74 status per the result; STATE only if the kernel changed; SESSION_LOG; commit
with `git commit -F <msg> -- <paths>`, push; `git rm` this prompt.
