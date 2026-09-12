# NightShiftWork — one-module review

Agent `/root` (coordinator's local review), 2026-09-12, anchor `2983fac`.
No disagreement with the retained module or current public symptom was found.

| module | entry | applies? | consumer still reads it? | row true? | bullet true? | verdict | evidence file:line on 1.1.0.403908 | basis | what I did NOT check |
|---|---|---|---|---|---|---|---|---|---|
| Fix_NightShiftWork.lua | F04 | yes, final registry active | yes, Idle consumes predicate and sets Work | yes, midnight catch-up window | yes, same symptom as row | KEEP | 1.1.0.403908 Lua/Units/Colonist.lua:2198 and :2362 | SOURCE | organic 1.1.0 staffing/cure, enable path, save/load, legacy runtime |

Primary source root is `C:/Dev/SMR-SrcArchive/1.1.0.403908/Src`:

- `Lua/Units/Colonist.lua:2198` still compares the unwrapped clock hour against
  start minus one through start plus three. It has no midnight wrap. The sibling
  early-departure arm is `:2199`; both remain delegated to vanilla first.
- `Lua/_GameConst.lua:395` defines third-shift start 22/end 6. The original
  catch-up window includes arithmetic hours 24/25 which a daily clock cannot
  reach. `Lua/Lightmodel.lua:11` takes the next hour modulo HoursPerDay;
  `Lua/Colony.lua:197` records the emitted hour.
- `Lua/Units/Colonist.lua:2362` is the only shipped caller found in Lua/DLC. A true
  answer reaches suitability/health gates and `:2366` sets command Work. The
  consumer still reads the predicate the wrapper widens; it has not moved.
- `Code/Fix_NightShiftWork.lua:68` onward returns a vanilla true unchanged, then
  adds modular-window results for existing workplaces. It does not replace the
  Work body or promise every ill/unsuitable colonist will work.
- Direct registry archive
  `docs/archive/logs/stillneeded_registry_Mars.exe-20260912-00.29.01-6a91a190.log:224`
  measures active. `BODYCHECK.txt` matches the pinned body and defect expression.
- `C:/Dev/SMR-CommunityMods/content/fix-list.md:130` describes being busy at shift
  start and returning after midnight; the metadata headline at `metadata.lua:3`
  maps to that row. No external witness is restored: F04's existing thread
  attribution decision remains unchanged.

Not checked: organic 1.1.0 third-shift return/staffing, exact delay/catch-up
distribution, a current TestKit behavior firing, menu-enable propagation,
save/load/uninstall, 1.0.7 runtime, or the external thread's originating build.
