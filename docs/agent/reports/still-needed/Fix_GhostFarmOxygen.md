# GhostFarmOxygen - one-module review

Agent `/root`, 2026-09-12, anchor `2983fac`. Recommendation only; owner decides.

## Disagreements first

Vanilla now closes the ordinary leak route. F37 already records this (2026-09-11)
and checklist150 asks for retirement; this review independently read the working
edge and consumption consumer in primary source. Hotfix2 surviving attachment
was not consumer clearance. Recommend RETIRE for ordinary 1.1.0 play. This is not
an all-routes proof: narrow refab/direct-script and historical-save/legacy
constituencies remain named limits. No module or public claim is edited here.

| module | entry | applies? | consumer still reads it? | row true? | bullet true? | verdict | evidence file:line on 1.1.0.403908 | basis | what I did NOT check |
|---|---|---|---|---|---|---|---|---|---|
| Fix_GhostFarmOxygen.lua | F37 | yes: direct final registry line 232 active | yes: dome/grid demand still reads air_consumption; prevention is redundant on ordinary 1.1.0 removal route | no: ordinary current-game salvage/destruction clears the modifier in vanilla; narrow refab residual unmeasured | no: farm oxygen headline presents closed ordinary 1.1.0 leak as current | RETIRE | 1.1.0.403908 Lua/Buildings/Farm.lua:165; 1.1.0.403908 Lua/Buildings/Farm.lua:630; 1.1.0.403908 Lua/Buildings/Farm.lua:641; 1.1.0.403908 Lua/Buildings/Building.lua:1570; 1.1.0.403908 Lua/Buildings/Building.lua:537; 1.1.0.403908 Lua/Buildings/Dome.lua:1881; 1.1.0.403908 Lua/Buildings/Workplace.lua:962 | SOURCE | Current live farm salvage/destruction and consumption readout; Refab during last-worker dying window and direct custom DoneObject/SetDome routes; Orphan modifiers in existing 1.1.0 saves, menu enable/reload, save/load/uninstall; Fresh 1.0.7 runtime and live-pack legacy constituency owner decision |

Primary root: `C:/Dev/SMR-SrcArchive/1.1.0.403908/Src`.

- `Lua/Buildings/Farm.lua:165`, `:630` and `:648` now all pass a crop only while
  working. An idle initial farm no longer installs oxygen. `:641` clears its
  own keyed modifier when the crop argument is false; `:643` notifies the dome.
- `Lua/Buildings/Building.lua:1560` marks destroyed; `:625` then prohibits work;
  `:1570` runs UpdateWorking(false) before Done's SetDome(false) at `:537`.
  Shipped farms retain the demolished-state path. The ordinary leak window the
  historical audit found has a vanilla replacement, rather than a renamed body.
- `Lua/Buildings/Dome.lua:1881` still installs current air_consumption as grid
  demand. `Lua/LifeSupportConsumer.lua:54` updates consumption on a changed
  modifiable value. The output is still read: redundancy is earlier cleanup,
  not removal of the oxygen consumer.
- Refab differs: `Lua/Buildings/Building.lua:1870` calls OnDestroyed, followed by
  DoneObject at `:1889`; `Lua/Buildings/Workplace.lua:58` kicks workers and
  `:472` recalculates working when they are removed. `:962` skips dying workers.
  Whether that narrow window can preserve oxygen until Done is INFERRED and
  unmeasured; it is not promoted into a verified defect. Direct scripted
  SetDome/DoneObject paths and orphan 1.1.0-save state also remain unmeasured.
- The module's LoadGame sibling still removes unmatched Farm-number modifiers;
  its prevention wrapper still clears at SetDome. Neither has lost its reader.
  EF-079 blocks 1.0.7 saves on1.1.0; it does not remove the live-pack1.0.7 player
  constituency. Owner must decide that constituency and residual risk before
  deleting the module. Existing Saint legacy retention is not silently applied
  to every other fix or used as a blanket reason to ignore this candidate.
- `C:/Dev/SMR-CommunityMods/content/fix-list.md:257` and `metadata.lua:3` still
  describe farms leaking after ordinary salvage. Those current claims need
  retirement or explicit narrowing via the held surface workflow after v9.

Registry archive `docs/archive/logs/stillneeded_registry_Mars.exe-20260912-00.29.01-6a91a190.log:232` measures active; bodycheck passes. No current cure witnessed.

Not checked:

- Current live farm salvage/destruction and consumption readout
- Refab during last-worker dying window and direct custom DoneObject/SetDome routes
- Orphan modifiers in existing 1.1.0 saves, menu enable/reload, save/load/uninstall
- Fresh 1.0.7 runtime and live-pack legacy constituency owner decision
