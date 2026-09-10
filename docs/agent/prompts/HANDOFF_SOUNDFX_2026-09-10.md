# Handoff — the silent-FX sitting of 2026-09-10 → the next session (model-agnostic)

⛔ ONE-SHOT: read this first; `git rm` it once every item below is done, routed to its home,
or restated in its own prompt. It replaces nothing — the records it points at win if they
disagree. Written by `smr-bugfixpack-08` at a context limit. **Verify every specific against
`git log` + the tree** (other sessions commit here too).

## 0 · Orient

`git log --oneline -15` · `git pull` · `git status --short` · `ListAgents` · `agent/STATE.md` ·
`prompts/DISPATCH.md` §1–§3. Open a **live todo list**, one item per numbered task below; the
owner reads it to decide when to step in.

## 1 · Where things stand (verify, don't inherit)

- **All seven silent-FX units are PROVEN in play** with the owner at the keyboard (1.1.0.403908,
  colony `BlankBig_02`, cheats on). Records: `agent/bugs/C74.md` (hammer + classic MOXIE: markers
  + an index→name conversion) and `agent/bugs/C77.md` (Water Extractor, Shuttle Hub shuttle, RC
  Driller, RC Dozer = RC Terraformer, The Excavator: markers only, plus a Water-Extractor-only
  start-order defect). Each entry's **Fix shape** section holds the exact times. Sweep that
  found C77: `agent/reports/C74_SOUND_SWEEP.md`.
- **Owner decision pending: checklist 139** — build all seven for hotfix 3, or file. The
  recommendation in the checklist is build all seven. ⚠️ Do not confuse with **checklist 142**
  (the vanillahunt 99 audit's hotfix-3 list for C56–C82, rec none) — separate decision.
- **STATE NEXT = `prompts/DLC_DEEP_CHECK.md`** (owner raises it; kickoff line in
  `reports/vanillahunt/HUNT_AUDIT.md` §8). Its banner carries the owner's framing: DEEP on
  the new DLC functions, BOUNDED — never an exhaustive per-row census (owner ruling that cut
  vanillahunt 04 to a skim; SESSION_LOG 09-10).
- **FR-1 (Linux)**: `prompts/FR1_LINUX_SITTING.md` is ready; fire it when the owner says the
  RTX 3070 laptop boots Mint (checklist 136).

## 2 · If the owner rules 139 = BUILD — update the brief FIRST

`prompts/C74_BUILD.md` covers only the hammer + MOXIE. Before anyone builds, extend it to all
seven, then build per `FIX_POLICY.md` (header lines, §2a behaviour-probe guard, §3a save-safety,
H-10 `items.lua`, `tools/parsecheck.py`, `tools/bodycheck.py --pin`). The content (all times
live-proven; ⛔ keep the moment TYPE per unit):

| group / id (the `GetAnimEntity` result, measured) | moments | notes |
|---|---|---|
| `UniversalExtractorHammer` / `working` | `Hit` 3083, 9250 (of 12,333) | needs the conversion |
| `MoxiePump` / `working` | `Hit` 3325, 9975 (of 13,300) | needs the conversion |
| `WaterExtractorCP3Pump` / `working` | `Hit` 1667, 5000 (of 6,667) | + tracker restart (below) |
| `WaterExtractorPump` / `working` | `Hit` 1658, 4975 (of 6,633) | + tracker restart |
| `Shuttle` / `landing`, `landing2` | `Hit` 1033 (of 2,067) | both hub skins; classic ShuttleHub only |
| `Shuttle` / `takeOff`, `takeOff2` | `Hit` 2500 (of 5,000) | the Jumper hub is NOT a unit |
| `RoverRussiaDriller` / `workIdle` | `Hit` 2708, 8125 (of 10,833) | Roscosmos-only for players |
| `RoverTerraformer` / `workIdle` | **`Hit1`** 1083, 3250 (of 4,333) | Load phase carries the sound |
| `ExcavatorShovel` / `working` | 24: `Hit`*i* at `MulDivRound(40000, i-1, 12)`, `Out`*i* = that + 20000 mod 40000 | ⛔ SORT by Time — `IterateMoments` walks list order |

- **The conversion (C74 only):** `BaseBuilding:TrackMultipleHitMoments` passes a state INDEX
  (`Lua/Buildings/BaseBuilding.lua:1045-1046`, `:1053`, `:1065`) to a NAME-keyed lookup.
  `C74_BUILD.md` step 1 already says: enumerate every index caller first, choose the narrowest
  wrap site, classdef-time (`EF-058`), and `AnimMoment.lua:17` aliases `GetEntityAnimMoments`
  locally (replacing the global does not reach `CObject:GetAnimMoments`). The live proof wrapped
  the pump's/hammer's own class `GetAnimMoments`.
- **The Water Extractor restart:** `WaterExtractorBase:OnSetWorking` starts
  `TrackAllMoments(pump, "working", self)` (`WaterExtractor.lua:112-115`) while the pump is still
  at anim speed 0 (`BaseBuilding.lua:1009`); speed returns to 1000 only in the `Notify`-queued
  `UpdateWorkingStateAnim` (`:1092`, `:945`), so the first `TimeToMoment` sleeps `max_int`
  (`AnimMoment.lua:117-119`) — alive, silent. Proven fix: (re)start the tracker once the pump runs.
  Design the hook point (e.g. after the working anim/speed is applied) and show it survives a
  power cycle AND a save load.
- **Guards:** skip any group/id that already exists (vanilla may ship presets later — the
  falsifier in both entries); the §2a probe must test behaviour, not a version.
- **Patch note must explain the skins:** the Rare Metals drill skin and the white (CP3) MOXIE
  are silent BY DESIGN (C74). Owner's skin screenshots: `agent/reports/c74_skins/`.
- **Metatron** (C74): 7 `End1..7` particles are fixable the same way but untimed (rare mystery
  unit; include only if the owner wants a sitting). Its 7 rotate SOUNDS are unreachable (thread
  emits only `Start`/`End`, `Metatron.lua:78`, `:86`) — never promise them.
- The attended check after the build: every unit heard/seen once with the pack on; ⛔ the
  Water Extractor across a power cycle and a reload.

## 3 · Optional owner glances (checklist 139 lists them; none required)

Shuttle touchdown/lift-off, Dozer shovel and Excavator bite/throw timing vs the motion (first
guesses: midpoint / ¼-¾ / geometric); whether the white MOXIE stayed silent after the C74 patch
(recorded as not checked).

## 4 · Loose ends found this session (homed in SESSION_LOG 09-10 "lookback" entry)

- **C75** (filed by Codex 03b) cites only 1.1.0 lines; the 03b brief required old/new citations.
  Add the 1.0.7 line numbers (never "correct" existing 1.1.0 citations — `EF-075`).
- Unexplained, verbatim: `Missing spot 'Top' in 'ElectricityGridElement' state 'idle'`
  (`Mars.exe-20260910-13.22.25-6a91a190.log:582`, just after a Quick Build cheat; no console
  line of ours touches power grids). Attribution only if someone asks — probably an asset warning.

## 5 · Working with the owner at the keyboard (learned 09-10)

- Console readouts: ONE line with a fixed prefix → owner **flushes the log** → grep newest
  `%APPDATA%\Surviving Mars Relaunched\logs\Mars.exe-*.log`. ⚠️ Unflushed = absent, not zero.
- Parse-check every line with `lupa` + a must-fail control, AND desk-run it on stubs for its
  premise cases (absent / wrong skin / not working) — twice today that caught a line that would
  have read the wrong object or printed nothing.
- Sound/FX tests: memory `sound-bug-test-method` — hand-fire to learn the sound (next to the
  SELECTED object), a log-only `PlayFX` hook as proof, `SetAllVolumesReason` + a strict hook to
  isolate, `.Moments = {}` in place for an A/B. Ear A/B alone was wrong twice today.
- Shared tree: before `doccheck.py --regen` + committing `INDEX.md`, check `git status --short
  docs/agent/bugs/` for other sessions' ` M`/`??` — one slip today (900fb79, resolved).
  Commit with `git commit -F <file> -- <paths>`; write the message with the Write tool
  (PowerShell `Set-Content`/pipes added a BOM to two commit subjects today).
- The owner is a dev: cheat UI and cheat-unlocked buildings are expected; say when a cheat
  widens what a player could do (the RC Driller).

## 6 · Close-out

Route every result to its home (entries, checklist, STATE only if the kernel changed,
SESSION_LOG). doccheck GREEN; guarded pathspec commit; push; `git rm` this file when §2–§4 are
done or restated elsewhere.
