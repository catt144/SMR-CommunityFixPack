# F07 + F15 one-module review

Task/agent: `/root/module_b`. Review anchor: `2983fac`. Game **1.1.0.403908**;
captured inputs and final direct registry in `CENSUS.json`. Recommendation:
**KEEP** both reward repairs. The power unit mismatch and duplicate research
grant remain, with current gameplay callers and current reward consumers.

Disagreements first: no current implementation, public-row or card-example
contradiction found. The important consumer change is research: current
`UIColony:AddResearchPoints` forwards to the player's accumulated research
balance and tech-point economy, rather than the old queued technology's scaled
`status.points`. The duplicate grant remains a duplicate **research-point**
payment; it need not produce twice as many tech points because conversion costs
change. Historical delayed lab-contaminated readings are not reused as proof.

| module | entry | applies? | consumer still reads it? | row true? | bullet true? | verdict | evidence file:line on 1.1.0.403908 | basis | what I did NOT check |
|---|---|---|---|---|---|---|---|---|---|
| Fix_WispRewards.lua | F07 power + F15 duplicate RP; later-catch silent UI half excluded | yes: final direct registry active at line 225; replacement target and both defects remain | yes: both compiled mystery choices call the global; power modifier feeds production/grid/UI; batch and death RP flow to current player balance and tech-point conversion | yes: F07 count-based choice is 1000 times too small until a later sibling update; F15 retains duplicate RP for the initial trapped batch and removes only that duplicate | yes: card intro thousandth-power example remains source-supported; no dedicated F07/F15 headline | KEEP | C:/Dev/SMR-SrcArchive/1.1.0.403908/Src/Lua/Mysteries/Fireflies.lua:695; C:/Dev/SMR-SrcArchive/1.1.0.403908/Src/Lua/Mysteries/Fireflies.lua:690; C:/Dev/SMR-SrcArchive/1.1.0.403908/Src/Lua/Mysteries/Fireflies.lua:547; C:/Dev/SMR-SrcArchive/1.1.0.403908/Src/Lua/ElectricityProducer.lua:66; C:/Dev/SMR-SrcArchive/1.1.0.403908/Src/Lua/TechTree.lua:661 | SOURCE | fresh 1.1.0 mystery choice, trap power and grid reading; uncontaminated current death RP accounting; actual tech-point conversion; interrupted death; save/load/uninstall; excluded silent UI and C46 changes |

Primary evidence (read-only **1.1.0.403908/Src**):

- **Both current gameplay callers reach the replacement:**
  `Lua/Scenario/Mystery 11.generated.lua:426-440` waits for 30 cumulative
  catches, presents the once-only choice and calls `SetLightTrapMode("free")`.
  Its other branch calls `SetLightTrapMode("destroy")` at `:470-471`.
  Editable counterparts are `Data/Scenario/Mystery 11.lua:526` and `:570`.
  A full source search finds no other gameplay callers, including DLC.
  The shipped mystery also calls `MassFireflySpawn` at
  `Lua/Scenario/Mystery 11.generated.lua:337-351`, so populated traps are
  ordinary mystery content, not inherently a forced or mod-only fixture.
- **F07 current defect and both sibling updates:**
  `Lua/Mysteries/Fireflies.lua:695` still calls
  `trap.el_prod_modifier:Change(#trap.fireflies)`. Detachment at `:343-348` and
  later capture at `:479-484` both multiply the same count by 1000 in free mode.
  `LightTrapBase` has zero base production at `:557` and initializes the
  modifier targeting `electricity_production` at `:567`. The current compiled
  `LightTrap` inherits that base at
  `Lua/BuildingTemplate/LightTrap.generated.lua:5`, with no production override.
  Thus a positive held count at the choice is converted to an amount exactly
  1000 times smaller than the sibling paths. An empty trap yields zero in both
  cases; a subsequent capture or release updates the amount correctly even in
  unpatched vanilla. This is the initial mode-choice defect, not a claim that
  all subsequent free-mode production is perpetually wrong.
- **F07 changed value still reaches production, grid and current UI:**
  `Lua/Modifiers.lua:321-329` sets the modifier's absolute amount, applying its
  delta through `UpdateModifier`; `:80-84` updates the target property and calls
  `OnModifiableValueChanged`. `Lua/ElectricityProducer.lua:64-66` sends the
  changed production to the supply-grid element; `:56-60` resolves performance
  when present, and `:70-71` reads that element for UI production.
  The current display at `Lua/XDef/sectionPowerProduction.generated.lua:22`
  formats that value through `power(UIPowerProduction)`. Resource formatting
  uses `const.ResourceScale` at `Lua/Resources.lua:331` and the scaled figure
  at `:405-406`, unlike forced-integer Research. The current Solar Panel's
  2000 production at `Lua/BuildingTemplate/SolarPanel.generated.lua:60` is
  consistent with the same internal power convention. Working, connectivity
  and performance still determine actual usable grid output; this fix changes
  the count's unit, not those conditions.
- **F15 current duplicate grants and retained message:**
  `Lua/Mysteries/Fireflies.lua:682` counts 100 RP per trapped wisp;
  `:683-684` schedules each `Die`; `:689` notifies with that total and `:690`
  grants it directly. Each normal `Die` destructor waits at `:542`, removes the
  wisp at `:545`, advances the destroyed count at `:546`, and grants another
  100 RP at `:547`. The replacement removes only the batch `AddResearchPoints`
  call, retaining the notification and per-death payer. The retained
  `fireflies_destroyed` value remains consumed by the mystery's progression
  gate at `Lua/Scenario/Mystery 11.generated.lua:473`.
- **F15 remaster reward consumer is different and still live:**
  Colony inherits Research at `Lua/Colony.lua:2`.
  `Lua/Research.lua:510-511` now forwards its RP argument directly to
  `UIPlayer:AddResearchPoints`. Player explicitly selects
  `TechPointObj.AddResearchPoints` at `Lua/TechTree.lua:728-732`; that method
  adds the unscaled argument to `AccumulatedResearchPoints` at `:659-663` and
  consumes accumulated points into `TechPoints` at `:692-698`.
  There is no queued-tech prerequisite or multiplier in this forwarding and
  addition path. Consequently the initial batch still supplies N times 100
  twice in vanilla when its scheduled deaths complete, and once under F15.
  Tech-point conversions can change the balance while it is being read, so a
  raw balance difference alone would not fully account for the reward.
- **F15 current notification uses the same RP unit:**
  `Data/NotificationPreset.lua:2472-2475` displays
  `Mystery11WispsKilled` through `research(points)`; the common notification
  helper passes the instance to its update at
  `CommonLua/Libs/Notifications/Notifications.lua:138-139`.
  `Lua/Resources.lua:501` registers that Research formatter; `:364` makes
  Research a forced integer and `:433` prints the unscaled value. Its N times
  100 figure therefore names the same RP quantity now added to the player's
  balance, not 1000-scaled legacy queue points or a number of tech points.
- **Named excluded residual, later catches remain silent:**
  `Lua/Mysteries/Fireflies.lua:471-474` calls `self:SetCommand("Die")` before
  its per-wisp notification and second grant. Drain runs as the wisp's command;
  `CommonLua/Classes/CommandObject.lua:356-358` creates its replacement command
  thread and `:378` deletes the old one. Those two later statements remain
  unreachable on normal successful command replacement. The actual death
  grant is the payer retained by F15. The entry deliberately excludes adding
  the later-catch notification; this module does not claim to repair it.
  `CommandObject:Done` does not replace a command when invoked from that same
  command thread (`:136-140`), consistent with the explicit post-`DoneObject`
  reward inside the normal death destructor. Interrupted death completion is
  not a cure witnessed in this review.

Public rows `C:/Dev/SMR-CommunityMods/content/fix-list.md:524-530` and `:532-539`
remain true about the initial count conversion and initial trapped-batch
double payment. The first row and card introduction's **about a thousandth**
example are supported by the exact sibling factor; the mystery's choice text
promises Water for Power rather than a separate numeric per-wisp contract.
The second row describes RP, not tech-point count or every later notification.
There are no dedicated F07/F15 card headlines.

Latest entry limits remain important. F07's August 11 **1.0.7.396349** power
and round-trip cure was witnessed with 95 wisps; its final enact was forced
after an organic daytime click found an empty trap. The archived agreeing power
read is `docs/archive/cp15sitting_Mars.exe-20260811-15.09.30.log:1277`.
F15's clean historical discriminator observed no immediate batch grant at
`:1558`; its delayed total included colony labs and did not isolate per-death
payments. These are historical execution evidence, not current 1.1.0 cures.
C46 remains the owner's excluded forced free-to-destroy phantom-power case:
current callers still offer only the single free-or-destroy choice, and all
power-amount writers require free mode. That prior decision is not reopened.

Direct final registry
`docs/archive/logs/stillneeded_registry_Mars.exe-20260912-00.29.01-6a91a190.log:225`
reports active; the settled second boot reports applied at
`docs/archive/logs/stillneeded_Mars.exe-20260912-00.25.42-6a91a190.log:78`.
No colony loaded or suite ran. This establishes installation; both current
reward repairs are source conclusions with the named execution limits above.

What I did NOT check, by name:

- Fresh 1.1.0 mystery choice with a populated trap, production/grid/UI readings.
- Uncontaminated current per-death RP accounting and tech-point conversions.
- Interrupted/deleted wisp death before the delayed payer completes.
- Fresh WispRewards TestKit probe or `RunAll()`.
- Save/load/uninstall or fresh 1.0.7 execution.
- Later-catch silent notification addition or C46 forced transition changes.
- Third-party modifiers, other mystery rewards, aggregate card repair counts.
- Other modules or fenced prelaunch sweep verdict reports.
