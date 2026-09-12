# F29 one-module review

Task/agent: `/root/module_b`. Review anchor: `2983fac`. Game **1.1.0.403908**;
captured inputs and direct registry in `CENSUS.json`. Module and site fix-list
byte hashes still match the capture. Recommendation: **KEEP** both subfixes as
R3 protection. The bodies remain defective, shipped mystery callers still reach
them, and current shipped values still hide both defects.

Disagreements first: no module or public-row disagreement found. The older F29
entry's claim of **no subclass** is too broad: `AlienDiggerBig` is a shipped
subclass. It has no timing override, so it inherits the already ordered values
and does not alter the R3 conclusion. The older **mod-facing / no shipped user**
description is also contradicted by the current compiled mystery calls below;
the public row correctly says both run in ordinary play.

| module | entry | applies? | consumer still reads it? | row true? | bullet true? | verdict | evidence file:line on 1.1.0.403908 | basis | what I did NOT check |
|---|---|---|---|---|---|---|---|---|---|
| Fix_SequenceLatents.lua | F29(a) sampling + F29(b) timing swap; tracker items 1 and 3 | yes: direct settled registry active at line 256; both source target declarations remain; live fixed/skipped arrays not read separately | yes: four compiled Mystery 2 callers consume the returned lists; spawned Diggers consume both timing fields during landing | yes: both defects remain and both are hidden by current shipped values; compiled mystery calls disprove mod-only provenance | yes: no dedicated headline; F29 supports the shared invisible-repairs paragraph; whole-list count of three not checked here | KEEP | C:/Dev/SMR-SrcArchive/1.1.0.403908/Src/Lua/Sequences/SA_Filters.lua:33; C:/Dev/SMR-SrcArchive/1.1.0.403908/Src/Lua/Scenario/Mystery 2.generated.lua:298; C:/Dev/SMR-SrcArchive/1.1.0.403908/Src/Lua/Mysteries/Diggers.lua:94; C:/Dev/SMR-SrcArchive/1.1.0.403908/Src/Lua/Mysteries/Diggers.lua:120 | SOURCE | fresh Mystery 2 playthrough; live per-subfix fixed/skipped arrays; nondefault runtime sampling; reversed runtime timing control; future content; excluded workshift generator; save/load/uninstall |

Primary evidence (read-only **1.1.0.403908/Src**):

- **Subfix (a), defect and intent:**
  `Lua/Sequences/SA_Filters.lua:10-11` defines full-list defaults
  (`random_count = 0`, `random_percent = 100`) and explicitly promises bounded
  number/percentage selection. `:21-26` advertises those choices;
  `:33-39` computes the requested count, shuffles, then returns the entire list
  without using the count. Current F29's post-wrapper truncates that result.
- **Subfix (a), current actual callers and result consumers:**
  `Lua/Scenario/Mystery 2.generated.lua:298`, `:315`, `:365`, `:369` are the
  four compiled `SA_GetLabelToRegister:SARun` calls. The returned lists feed
  deposit validation/class filtering at `:302-330`, and building/deposit range
  filtering plus digger placement at `:373-396`. `Registers Init` autostarts at
  `:286-287`; the trigger starts `Digger Spawner (First)` at `:110-111`.
  `CommonLua/Libs/Sequences/SequenceAction.lua:265-267` dispatches `SARun` to
  the patched `instance:SAExec()`; the interpreted executor also stores results
  in output registers at `:251-261`. These are shipped gameplay calls, not
  editor-only callers or direct generated replacements that bypass the wrapper.
- **Subfix (a), current data still hide it:** each of those four compiled calls
  sets only label/register, as do their editable counterparts at
  `Data/Scenario/Mystery 2.lua:235-238`, `:252-255`, `:280-287`. An exact-token
  search for `random_count` or `random_percent` in all `Data/**/*.lua` and
  `Lua/Scenario/**/*.lua` returned **zero** hits; unrelated `random_count_add`
  fields were excluded. The action thus still inherits 0/100 full-list defaults
  through instance creation (`CommonLua/PropertyObject.lua:1470-1475`). On that
  data the post-wrapper removes nothing; the defect becomes observable only
  when later shipped data request a subset.
- **Subfix (a), returned storage is still safe to truncate:**
  `Lua/Sequences/SA_Gameplay.lua:147-168` returns `table.icopy(labels[label])`
  for ordinary labels and builds a fresh table for `Working-age`. The wrapper
  changes a result list consumed by the mystery, not the city's live label.
- **Subfix (b), defect and current values:**
  `Lua/Mysteries/Diggers.lua:91-95` still saves `t` then overwrites both timing
  fields with the larger value. `:53-54` still declares 1000/500, already in
  descending order. An exact-token search across all archived `Src/**/*.lua`
  finds timing-name occurrences only in `Diggers.lua`: the two defaults, the
  broken swap and the landing readers. There is no preset or assignment that
  reverses them. `AlienDiggerBig` at `:350-362` inherits `AlienDigger` and changes
  other values without overriding either timing or `GameInit`.
- **Subfix (b), current caller and timing consumers:**
  `Data/Scenario/Mystery 2.lua:318`, `:333`, `:981` spawns the small and boss
  classes; compiled small-digger placement is at
  `Lua/Scenario/Mystery 2.generated.lua:392-407`.
  `Lua/Sequences/SA_Gameplay.lua:1814-1848` resolves and places the class.
  Ordinary object construction invokes `GameInit` at
  `CommonLua/Classes/_object.lua:184-192`, with load-time initialization at
  `:135-141`. `AlienDigger:GameInit` labels it and starts `Idle` at
  `Lua/Mysteries/Diggers.lua:87-89`; `Idle` calls `Land` at `:248-250`.
  `Land` reads both timing fields in its waits and distinct pre-hit effects at
  `:120-125`. Current F29 orders the fields before delegating, making the broken
  branch false. This is live mystery code protected against later data changes;
  the defective swap does not execute with current shipped values.

Public row `C:/Dev/SMR-CommunityMods/content/fix-list.md:605-609` accurately
describes the discarded sampling count and broken timing swap, their currently
benign values, and their shipped mystery consumers. The card has no dedicated
F29 headline, but its **three repairs you cannot see today** paragraph is
supported by this module as one contributor. Other contributors and the total
are the coordinator's whole-list question, not evidence produced here.

Direct settled registry
`docs/archive/logs/stillneeded_registry_Mars.exe-20260912-00.29.01-6a91a190.log:256`
reports active; prior archived boot reports applied at
`docs/archive/logs/stillneeded_Mars.exe-20260912-00.25.42-6a91a190.log:114`.
No colony loaded or suite ran, and no later SequenceLatents heal/data message
was found. This is installation evidence; the two runtime `fixed`/`skipped`
lists were not separately captured. Source declarations and the current
consumer/data traces above establish the bounded source conclusion without
re-running the hotfix-2 survivor audit.

What I did NOT check, by name:

- Fresh 1.1.0 Mystery 2 playthrough, register output or Digger landing visuals.
- Live `SMRFixPack.SequenceLatents.fixed` / `.skipped` arrays.
- Nondefault sampling controls or reversed timing controls in the game.
- Fresh TestKit `SequenceLatents` probe or `RunAll()`.
- Future preset/DLC values or third-party content.
- Tracker item 2, the deliberately excluded workshift-code generator.
- Save/load/uninstall, fresh 1.0.7 execution, whole-card invisible-repair count.
- Other modules or fenced prelaunch sweep verdict reports.
