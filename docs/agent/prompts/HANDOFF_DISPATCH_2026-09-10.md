# Handoff — dispatch session of 2026-09-10 → the next session (model-agnostic)

⛔ ONE-SHOT: read this first, then `git rm` it once every item below is either done,
routed to its home, or restated in its own prompt. It replaces nothing — the
records it points at win if they disagree. Written by `smr-bugfixpack-ae` at a
context limit; **verify every specific against `git log` + the trees** (the
vanillahunt 03b/04 sessions may have committed since).

## 0 · Orient
`git log --oneline -15` · `git pull` · `git status --short` · `ListAgents` ·
`agent/STATE.md` · `prompts/DISPATCH.md` §1–§3 (bindings, filing). Then open a
**live todo list** with one item per numbered task below and keep it current —
the owner reads it to decide when to step in.

## 1 · How to work with the owner at the keyboard (learned this session)
- For any console readout: make it print ONE line with a fixed prefix
  (`C74 x:`), then ask the owner to **flush the log**, and grep
  `%APPDATA%\Surviving Mars Relaunched\logs\Mars.exe-*.log` (newest) for the prefix.
  Console `print` DOES reach the log after a flush (`EF-015`, scoped 09-10).
- ⛔ Avoid wide screenshots: once a >2000 px image is in the conversation, every
  later image read fails, even crops. The OS also saves captures to
  `C:\Users\stkot\OneDrive\Pictures\Screenshots\`.
- Parse-check every console line before handing it over (`lupa` `load()`), and
  desk-test logic whose PREMISE matters — the first C74 probe passed its desk
  control and failed in game because the control assumed what it had to test.
- The owner is a dev: cheat UI in their screenshots is expected and publishable.

## 2 · The sound bug — `C74` (read `agent/bugs/C74.md` + `agent/facts/EF-086.md`)
**State:** two vanilla defects, both trees. (1) `BaseBuilding:TrackMultipleHitMoments`
passes `obj:GetAnim(1)` — a state INDEX (measured `anim 20 number`) — into a lookup
keyed by NAME (`AnimMoment.lua:8`), so the hit count is always 0; every other
caller wraps `GetStateName`. (2) Moments are Lua `AnimMetadata` presets and only 5
groups ship; `UniversalExtractorHammer`, `MoxiePump`, `Metatron` have none.
**Proven live, attended:** hammer preset (Hit at 3083 + 9250 of the 12,333 ms loop)
+ a class-level index→name conversion ⇒ the game's own tracker played the authored
thunks/puffs "perfectly in sync". CP3 skins (the drill, the white MOXIE) are FX-less
BY DESIGN — not a defect.
**Owner decision pending:** checklist **139** (build or file; rec build). If build →
`prompts/C74_BUILD.md` is the brief; do not start it before the ruling.

### 2a · YES — the MOXIE needs the same live test (not yet done)
Done on the classic MOXIE: readout `MoxiePump working 0`, tracker dead; hand-fired
`PlayFX("Working","hit-moment1",bld,pump)` plays the pump sound. NOT done: the
preset + conversion test that finds its in-sync times. With the owner at a
**classic** (not white/CP3) working MOXIE, not saving meanwhile:
1. Preset (placeholder times — start with ¼ and ¾, then adjust by ear):
   `local p = SelectedObj:GetAttach("MoxiePump") local d = p:GetAnimDuration() PlaceObj('AnimMetadata', {group = "MoxiePump", id = "working", Moments = { {Type = "Hit", Time = MulDivRound(d, 1, 4)}, {Type = "Hit", Time = MulDivRound(d, 3, 4)} }}) print("C74 moxie: dur", d)`
2. Conversion on the pump's own class (a runtime `CObject` patch misses flattened
   subclasses, `EF-058`):
   `local p = SelectedObj:GetAttach("MoxiePump") local cls = g_Classes[p.class] local orig = cls.GetAnimMoments cls.GetAnimMoments = function(self, anim, t) if type(anim) == "number" then anim = GetStateName(anim) end return orig(self, anim, t) end local g = Presets.AnimMetadata.MoxiePump print("C74 moxie: preset", g and g.working and #(g.working.Moments or {}) or "none", "count", p:GetAnimMomentsCount(p:GetAnim(1), "Hit"))`
3. Power off/on; owner listens. MOXIE FX: `hit-moment1` = `LoopPeaks` + `LoopSteam`
   + steam at spot `Steam2`; `hit-moment2` = `LoopPeaks` + steam at `Steam1`. The
   pump strokes may not be at ¼/¾ — re-run step 1 with new `MulDivRound(d, n, m)`
   values (a second `PlaceObj` replaces the lookup entry) until in sync; record
   the times in C74. Metatron: same method, only if the owner wants it (rare).

## 3 · Sweep for other sound candidates (not started — scope it, then propose)
The C74 class is "authored FX that can only fire from animation moments that
never resolve". Measured/predicted so far: Rare Metals hammer (measured), MOXIE
pump (measured), Metatron (predicted, `Metatron.lua:52-57`). A desk census of
both trees found **40 `ActionFX*` entries keyed to `hit-moment*`**, 9 actor/target
combos; code-fired ones are fine (MirrorSphere `MirrorSphere.lua:872`, dust storms
`DustStorm.lua:267`, Stirling `StirlingGenerator.lua:72`); Advanced Stirling has a
preset. **Unresolved: 13 entries with NO `Actor` field** (9 particles + 4 sounds,
`Target = "ignore"`) — classify who fires them before calling the sweep done.
Sweep plan, desk first:
1. **Every moment consumer passing an index:** all `GetAnimMoment*` /
   `IterateMoments` / `TimeToMoment` / `WaitAnimMoment` / `GetAnimMomentsCount`
   callers in `Lua/`, `CommonLua/`, `DLC/`, classed name vs index. Any index caller
   is broken like the tracker.
2. **Every `ActionFX*` whose `Moment` is not `start`/`end`/code-fired** (not only
   `hit-moment*` — any moment type an animation would have to emit), mapped to the
   entity whose animation must carry it; cross-check against the 5 preset groups
   (`EF-086`). No preset ⇒ candidate.
3. **`AnimMomentHook` users** (`anim_moments_hook`, `OnAnimMoment`,
   `PlayFXMoment`, e.g. `Colonist.lua:4965`) — same test: does the entity have a
   preset for the moment it waits on?
4. **FX targets that name a class/entity no longer spawned** (the CP3 pattern:
   `ActionFXRemove.lua:3-8`) — design, not defect, unless an FX is orphaned.
⚠️ The census script used this session lived in the scratchpad (gone); its
class-count regex was broken (read 0 — `DefineClass` bodies contain nested `{}`).
Rebuild it; never report a "0" from it without a control. Each surviving candidate
gets the §1 owner test: readout → hand-fire → (if the owner wants) preset test.
File as `C` entries per `DISPATCH.md` §3; claims about absence need the presence
side enumerated.

## 4 · Linux — FR-1 (read `prompts/vanillahunt/README.md` §2b + checklist 136)
- **Established:** vanilla (clean installs, no mods), 1.1.0 × Proton × new-game
  start × NVIDIA; DLC-off still crashes; a Windows + NVIDIA control with DLSS 4 on
  works. ⛔ **The temporal-upscaler lead is REFUTED** (anti-aliasing Off/FXAA still
  crashes, `7987b28`); map generation / new native calls now lead — 04 carries it.
  Game logs lose their crash tail (`EF-047`); `PROTON_LOG=1` is the instrument.
- **The OP's machine:** MSI Katana laptop, hybrid Intel + RTX 3060 Mobile, driver
  580.173.02, Mint 22.2 Cinnamon X11, kernel 7.0 — and **1.0.7 ran fine on it**.
- **The owner's rig:** the RTX 3070 laptop, set up to mirror the OP (checklist 136
  item 5; memory note on the rig). **Owed when it boots Mint:** the FR-1 sitting
  script — crash moment, `PROTON_LOG=1` (`~/steam-3215050.log`), the game log at
  `…/compatdata/3215050/pfx/drive_c/users/steamuser/AppData/Roaming/Surviving Mars Relaunched/logs/`
  (translated from the Windows path, UNVERIFIED until seen), the integrated GPU
  via Options → Graphics Adapter (non-NVIDIA control), the 1.0.7 branch (regression
  control), a no-mod 1.1.0 Sol-1 save from the owner (load vs new-game). ⛔ The game
  is D3D12-only on PC (`options.lua:443-447`) — `PROTON_USE_WINED3D` changes nothing.
  Steam Cloud off for the game on the laptop before first launch.
- Player-facing instructions (log paths, `PROTON_LOG`) are route-checked on the rig
  before anyone posts them.

## 5 · Other loose ends
- README rule 15 covers only `bugs/INDEX.md` merges; parallel vanillahunt links
  closing together will also conflict on STATE's NEXT line, the README queue and
  the 99 inbox. Offered to the owner, not ruled — ask once, or leave.
- The C74 reporter reply text is in checklist 139, for the owner to post if wanted.
- Owner screenshots of the two skins: `agent/reports/c74_skins/` (full-res outside
  git at `C:\Dev\SMR-ScreenCaptures\c74_skins\`).

## 6 · Close-out
Route every result to its home (C entries, checklist, STATE only if the kernel
changed, SESSION_LOG). doccheck GREEN; `git commit -F <msg> -- <paths>`; push;
`git rm` this file when §2a, §3 and §4 are done or restated elsewhere.
