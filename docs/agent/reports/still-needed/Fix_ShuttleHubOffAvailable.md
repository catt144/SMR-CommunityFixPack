# F54 one-module review

Task/agent: `/root/module_b`. Review anchor: `2983fac`. Inputs: `CENSUS.json`
(capture anchor `8469ae453b3d6312128ab187f38305f62fa41b92`, game 1.1.0.403908).
The module and site fix-list byte hashes still match the captured inputs.

Disagreement: the fix-list row's dust-storm example is false. Its final sentence
says game-imposed suspensions, "a dust storm, for instance", still count as
available. A dust-storm-suspended Shuttle Hub is already excluded by vanilla:
its template opts into dust-storm suspension, the storm sets `self.suspended`,
and that is a work-not-possible reason. F54 preserves permission-only exceptional
disabling, not physical suspension. Recommend **KEEP-BUT-FIX-CLAIM**: retain the
module and replace that example with the accurately bounded permission-only
exceptional-circumstances case through the existing surface-correction workflow.

| module | entry | applies? | consumer still reads it? | row true? | bullet true? | verdict | evidence file:line on 1.1.0.403908 | basis | what I did NOT check |
|---|---|---|---|---|---|---|---|---|---|
| Fix_ShuttleHubOffAvailable.lua | F54 | yes: archived settled boot reports applied at line 103; installation only | yes: all ten shipped call sites consume its boolean; graph, mode selection, passage walkability, transport requests, pickup waiting and stranded-home rescue remain live consumers | partial: off-hub availability discrepancy and filtering remain true; dust-storm example is false; fresh 1.1.0 waiting symptom unobserved | n/a: no dedicated F54 headline bullet in the captured description; generic shuttles mention has no F54-specific promise | KEEP-BUT-FIX-CLAIM | C:/Dev/SMR-SrcArchive/1.1.0.403908/Src/Lua/Buildings/ShuttleHub.lua:413; C:/Dev/SMR-SrcArchive/1.1.0.403908/Src/Lua/Units/Colonist.lua:3408; C:/Dev/SMR-SrcArchive/1.1.0.403908/Src/Lua/Buildings/BaseBuilding.lua:635 | SOURCE: predicate, consumers and false example; realized waiting symptom remains INFERRED | fresh 1.1.0 colony cure; named F54 TestKit probe; working and exceptional-circumstances runtime controls; exact wait duration; airborne ride completion; nonstandard hub labels; 1.0.7 runtime |

Primary evidence (all game citations below are from read-only **1.1.0.403908/Src**):

- `Lua/Buildings/ShuttleHub.lua:410-419`: vanilla still accepts a nonworking hub
  with any permission reason and no physical reason, provided it has shuttles
  and allows people transport. `Lua/Buildings/BaseBuilding.lua:657-663` supplies
  `TurnedOff` when `ui_working` is false. The player toggle reaches that field
  through `Lua/Buildings/BaseBuilding.lua:554-557` and `:519-526`, which also
  updates working state. Thus the off-hub discrepancy remains in primary code.
- `Lua/Buildings/ShuttleHub.lua:585-588` and `:1836-1840`: both shipped
  `SendOutShuttles` callers require `working`. `:1915-1928` obtains a transport
  task and creates the shuttle. The availability clause and dispatch guards
  still disagree when every otherwise eligible hub is player-disabled.
- `Lua/Units/Colonist.lua:3408-3413`: `BuildReachableGraph` still adds remote
  shuttle-landing communities when the predicate is true. Its shipped consumer
  `FindEmigrationDome` uses that graph at `:3514-3517`, then directly reads the
  predicate again at `:3524-3525` for transportation-mode selection.
- `Lua/Units/Colonist.lua:1914-1927`, `:1961-1970`, and `:3588-3597`: the
  predicate still influences passage/foot selection, source-pickup lookup and
  same-city transport availability before a task is booked.
- `Lua/Buildings/Dome.lua:315-316`: a passage-connected dome pair's cached
  walking verdict still reads the predicate. There is no F60-style abandoned
  consumer here.
- `Lua/Units/Colonist.lua:3626-3629` and `:3667-3699`: an uncommitted pickup
  task's waiting test still reads the predicate, as does the check after the
  colonist reaches the pickup point. These are primary paths for unnecessary
  waiting while eligible hubs remain off; this review did not observe the
  complete player sequence on 1.1.0.
- `Lua/Units/ColonistTransport.lua:460-470` and `:852-857`: both ordinary failed
  home routing and the stranded retry loop still gate shuttle rescue booking
  on this predicate. Tree-wide `rg IsLRTransportAvailable` found these ten
  consumers plus the single global definition; all ten were read in context.
- `Data/BuildingTemplate/ShuttleHub.lua:50` enables dust-storm suspension;
  `Lua/DustStorm.lua:112-117` collects opted-in templates and `:592-599` suspends
  their outside buildings. `Lua/Buildings/BaseBuilding.lua:771` stores the
  reason and `:784` updates working state. `:635-636` returns the suspension as
  a physical inability, so `Lua/Buildings/ShuttleHub.lua:413` excludes it
  before F54 filters anything. `Lua/DustStorm.lua:428-432` clears that reason
  when the storm ends. The public dust-storm example at
  `C:/Dev/SMR-CommunityMods/content/fix-list.md:103` contradicts this chain.
- `Lua/Buildings/BaseBuilding.lua:660-661` and
  `Lua/RequiresMaintenance.lua:131-134` provide the permission-only exceptional
  reasons that the wrapper continues to admit when the player switch is on
  and no physical inability exists. These are the properly bounded exception.
- `Lua/Units/Colonist.lua:3694-3701` bounds pickup waiting;
  `Lua/LRTransport.lua:43-59` expires uncommitted tasks; and
  `Lua/LRManager.lua:50-62` releases obsolete requests outside the `Transport`
  command. Consequently no indefinite-wait claim is established by this review.

Runtime installation evidence: archived settled boot
`docs/archive/logs/stillneeded_Mars.exe-20260912-00.25.42-6a91a190.log:103`
reports `ShuttleHubOffAvailable: applied`; no later F54 data/heal message was
found. No colony loaded and no suite ran. Captured `BODYCHECK.txt` matches the
pinned global body and defect expression; the consumer chain above was read
independently rather than treating that match as semantic clearance.

What I did NOT check, by name:

- Fresh 1.1.0 colony reproduction and cure of F54's pickup-waiting symptom.
- TestKit `ShuttleHubOffAvailable` behavior probe or `RunAll()`.
- Working-hub, permission-only exceptional-circumstances and exceptional
  maintenance runtime controls.
- Exact wait duration, retry frequency or downstream suffocation probability.
- Already airborne/committed rides when a hub is switched off.
- Nonstandard/DLC hub label coverage beyond the unchanged vanilla label scan.
- Fresh 1.0.7 runtime behavior, save/load or uninstall testing.
- Live portal card rendering, whole-card bullet counts and judgment-call counts.
- Any other module, fenced prelaunch sweep verdict reports or code changes.
