# GraphConsumedCaption — one-module review

Agent `/root` (local one-module task), 2026-09-12, anchor `2983fac`. **KEEP**;
the maintenance term is still omitted only from the caption.

| module | entry | applies? | consumer still reads it? | row true? | bullet true? | verdict | evidence file:line on 1.1.0.403908 | basis | what I did NOT check |
|---|---|---|---|---|---|---|---|---|---|
| Fix_GraphConsumedCaption.lua | F19 | yes, final registry active | yes, colony stats UI consumes returned panel caption and consumed series | yes, caption/bar still disagree | n/a, no dedicated headline | KEEP | 1.1.0.403908 Lua/X/ColonyControlCenter.lua:184; Lua/ResourceTracking.lua:162 | SOURCE | live panel Matched/readout, language rendering, current behavior firing, save/load, legacy runtime |

SOURCE, primary root `C:/Dev/SMR-SrcArchive/1.1.0.403908/Src`:
`Lua/X/ColonyControlCenter.lua:184` still captions consumption-only;
`Lua/ResourceTracking.lua:162` still plots consumption plus maintenance. The
overview getters at `Lua/ResourceOverview.lua:225` and `:229` read separate
accumulators. The current returned resource panel has consumed as its second
series, so the module's structural match remains valid at source.

SOURCE: `Lua/XDef/CommandCenterColonyStats.generated.lua:78` consumes
UICity:GetColonyStatsButtons, then selecting the returned item sets it as dialog
context at `:93`. The graph subcontext carries item caption/data to the
CommandCenterGraph child. This is a current UI consumer of the corrected closure,
not an unused descriptor table. The wrapper delegates vanilla before changing
only matched resource-panel captions and keeps the original translation/layout.

MEASURED: final registry archive
`docs/archive/logs/stillneeded_registry_Mars.exe-20260912-00.29.01-6a91a190.log:253`
records GraphConsumedCaption active. SOURCE: current site row
`C:/Dev/SMR-CommunityMods/content/fix-list.md:582` describes the same retained
caption-versus-bar mismatch. Metadata has no dedicated F19 headline. No current
claim correction was found.

Not checked: actual 1.1.0 resource-panel matching/Matched(), visible caption and
bars, localisation/T formatting, current F19 behavior probe, menu-enable/reload,
save/load/uninstall, 1.0.7 runtime. Installation is not a rendering witness.
