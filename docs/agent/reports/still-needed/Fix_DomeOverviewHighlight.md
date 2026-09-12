# DomeOverviewHighlight — one-module review

Agent `/root` (local one-module task), 2026-09-12, anchor `2983fac`. **KEEP**;
no current consumer drift or public-claim disagreement found.

| module | entry | applies? | consumer still reads it? | row true? | bullet true? | verdict | evidence file:line on 1.1.0.403908 | basis | what I did NOT check |
|---|---|---|---|---|---|---|---|---|---|
| Fix_DomeOverviewHighlight.lua | F14 | yes, final registry active | yes, dome overview invokes inherited Community stat method and renders idLabel | yes, discarded red-tagged value remains | yes, same overview symptom | KEEP | 1.1.0.403908 Lua/X/ColonyControlCenter.lua:1300; Lua/XDef/CommandCenterDomeOverviewRow.generated.lua:56 | SOURCE | 1.1.0 screen witness, current behavior probe, reload, save/load, legacy runtime |

SOURCE, primary root `C:/Dev/SMR-SrcArchive/1.1.0.403908/Src`:
`Lua/X/ColonyControlCenter.lua:1290` declares Community's method. `:1296` builds
red-tagged text for a below-threshold average, but `:1300` still passes raw v to
SetText. The module copies this unchanged body and passes tv. This is the same
discarded-computation defect, not a newly moved UI contract.

SOURCE: `Lua/XDef/CommandCenterDomeOverviewRow.generated.lua:56` calls
`context:UICommandCenterStatUpdate(self, item)` in OnContextUpdate. Its `idLabel`
remains the displayed text child. The general stat dispatcher at
`Lua/X/ColonyControlCenter.lua:495` also delegates to this method on Community
objects. The rendered consumer has not stopped reading the changed value.

MEASURED installation: final registry archive
`docs/archive/logs/stillneeded_registry_Mars.exe-20260912-00.29.01-6a91a190.log:240`
records active. SOURCE public claims: `C:/Dev/SMR-CommunityMods/content/fix-list.md:574`
and the dedicated metadata headline at `metadata.lua:3` both name the restored
Domes Overview low-stat marking. This pass does not renew the old screen witness.

Not checked: 1.1.0 visible colour/highlight, localisation/T rendering, an executed
F14 behavior probe, menu-enable/reload, save/load/uninstall, 1.0.7 runtime.
