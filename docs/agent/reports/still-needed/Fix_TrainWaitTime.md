# F21 one-module review

Task/agent: `/root/module_b`. Review anchor: `2983fac`. Game **1.1.0.403908**;
captured inputs and final direct registry in `CENSUS.json`. Recommendation:
**KEEP-BUT-FIX-CLAIM**. The remaining train/track statistics defect is current;
the advertised correction to a duration-based Comfort charge is obsolete.

Disagreements first: current `ExitVehicle` no longer spends elapsed ride time
through `ChangeComfort`. It still spends that time on the train and track.
The fix-list row at `fix-list.md:399` and the card introduction's **a Comfort
penalty billed for longer than the journey actually took** example therefore
overstate what F21 repairs on 1.1.0. `PACK_1_1_0_REVERIFICATION.md:128` already
recognized that the Comfort half was gone, but the public example and module
prose still describe it. The new fixed train-travel Comfort target contribution
does not read the restamped field and is not changed by this wrapper.

| module | entry | applies? | consumer still reads it? | row true? | bullet true? | verdict | evidence file:line on 1.1.0.403908 | basis | what I did NOT check |
|---|---|---|---|---|---|---|---|---|---|
| Fix_TrainWaitTime.lua | F21; F86 layer-3 conversion is historical technique | yes: final direct registry active at line 254; synchronous AddSpentTime target and boarding trigger remain | partial: both train/track elapsed-time consumers remain; former duration-based Comfort consumer is gone; station retains its computed wait | partial: title, timestamp mechanism and statistics correction remain true; current Comfort-benefit claim is false | no: card intro Comfort-duration example is obsolete on 1.1.0; no dedicated F21 headline | KEEP-BUT-FIX-CLAIM | C:/Dev/SMR-SrcArchive/1.1.0.403908/Src/Lua/Units/ColonistTransport.lua:622; C:/Dev/SMR-SrcArchive/1.1.0.403908/Src/Lua/Units/ColonistTransport.lua:671; C:/Dev/SMR-SrcArchive/1.1.0.403908/Src/Lua/Units/ColonistTransport.lua:696; C:/Dev/SMR-SrcArchive/1.1.0.403908/Src/Data/StatsImpact.lua:134; C:/Dev/SMR-SrcArchive/1.1.0.403908/Src/Lua/Units/Colonist.lua:2542 | SOURCE | fresh organic 1.1.0 boarding restamp; paired station/train/track readings; fresh Comfort target observation; interrupted or no-holder boarding; save/load/uninstall; probe firing; other train defects |

Primary evidence (read-only **1.1.0.403908/Src**):

- **Named current residual, both statistics consumers:**
  `Lua/Units/ColonistTransport.lua:600-605` stamps `ticket.start_wait` when
  waiting begins. `BoardVehicle` at `:614-639` credits the station's wait at
  `:622` but never restamps it. `ExitVehicle` snapshots elapsed time at `:671`
  and spends that same wait-plus-ride value on the train at `:696` and track at
  `:697`. A full source search for `start_wait` finds just the wait stamp, its
  inbound diagnostic, station credit and this exit calculation. There is no
  vanilla boarding restamp. The wrapper therefore still removes a real extra
  platform-wait contribution from both train and track samples.
- **Current boarding caller and synchronous identification still fit:**
  `Lua/Units/ColonistTransport.lua:558-569` enters the station, adds the colonist
  to `waiting_for_train` and starts waiting. `Lua/Units/Train.lua:962-973`
  selects a waiting ticket, marks it `Boarding`, then issues
  `colonist:SetCommand("BoardVehicle", self)` at `:971`.
  `CommonLua/Classes/CommandObject.lua:356-358` creates and stores the subject's
  command thread. At station `AddSpentTime`, `BoardVehicle` has not yet changed
  the holder or removed the waiting-list entry: those happen at
  `Lua/Units/ColonistTransport.lua:625` and `:628`, before stage `Traveling`
  at `:630`. The wrapper's current-thread comparison therefore still identifies
  the boarding subject from the station list. The newer `Boarding` intermediate
  stage does not matter because the wrapper does not filter on stage.
- **Station wait and both downstream statistics remain readable:**
  `Lua/TransportStatistics.lua:31-37` updates a capped 20-sample array and sum
  synchronously, without a yielding callee. `:39-45` computes and displays the
  rolling average. The wrapper restamps before delegation, but the caller has
  already evaluated `GameTime() - ticket.start_wait` at
  `Lua/Units/ColonistTransport.lua:622`, so the station retains the full wait.
  Station, Train and StationsLink inherit this method at
  `Lua/Buildings/Station.lua:53`, `Lua/Units/Train.lua:17`, and
  `Lua/Buildings/StationsLink.lua:5`; tracks inherit StationsLink at
  `Lua/Buildings/Track.lua:29`. Their current display consumers are station
  waiting average at `Lua/Buildings/Station.lua:1302`, train travel average at
  `Lua/XDef/ipTrain.generated.lua:85`, and track travel average at
  `Lua/XDef/ipTrack.generated.lua:186` plus `ipTrackElement.generated.lua:188`.
  These are the remaining two repaired statistics and the preserved station
  statistic, not a dead field or an unused display path.
- **Current exit caller still reaches both statistics:**
  `Lua/Units/Train.lua:430-433` issues `ExitVehicle` to an unloading rider.
  The current `ExitVehicle` source at
  `Lua/Units/ColonistTransport.lua:660-699` snapshots its ticket before clearing
  the live reference, computes the time and sends it to both statistics before
  calling the exit destructor. It contains no duration-based Comfort charge.
  Its green-view effect is Sanity at `:686-687`, separate from this fix.
- **Comfort was moved to a different input and target calculation:**
  `Data/StatsImpact.lua:133-138` defines `TrainTravel` with `Comfort = -12000`
  and a condition of recent train travel plus no `LuxuriousTrains`.
  `Lua/Units/ColonistTransport.lua:685` stamps `last_train_travel` on exit;
  `Lua/Units/Colonist.lua:5314-5315` tests that stamp against `DayStart` and a
  day duration. `GetRestStatTarget` applies conditional Rest presets at
  `:2542-2545`; `:2610-2624` settles current target stats toward that aggregate
  target. The -12000 is a fixed Comfort target contribution, not a direct
  per-hour charge or necessarily a -12 change on one rest. Its Outlook display
  uses the same conditional presets at `Lua/Stats.lua:887-891`.
  None of these reads `start_wait` or the train/track elapsed-time average.
  The leftover reason label at `Lua/Units/ColonistTransport.lua:5` and old tech
  description at `Data/Tech.lua:5266` do not restore the removed consumer.
- **Other journey and waiting values stay distinct:**
  `StartTransport` initializes `ticket.timestamp` at
  `Lua/Units/ColonistTransport.lua:363`; `GetTravelTime` still uses that booking
  timestamp at `:181-185`, not the restamped platform/ride boundary. Thus its
  full-journey read is not another repaired elapsed-time consumer.
  The independent full-train Comfort charge at `Lua/Units/Train.lua:975` remains
  and does not read `start_wait`. The wrapper does not remove actual waits,
  alter capacity, or protect every interrupted journey.

Public row `C:/Dev/SMR-CommunityMods/content/fix-list.md:398-406` remains correct
about the wait/ride timestamp defect and the train/track figures. It needs its
Comfort example removed or explicitly marked as historical 1.0.7 behavior.
The same applies to the F21 example in `metadata.lua:3`'s card introduction;
there is no separate F21 headline. The code requires no repair for this
consumer removal: its two surviving downstream consumers still use the field
it restamps, and the new Comfort mechanism is independent.

Latest F21 entry decisions remain limited: the July PT-43 pass exercised a
retired `BoardVehicle` replacement; the August 10 organic wrapper restamp was
witnessed on one named subject in **1.0.7.396349**, not on the current patch.
The archived witness is
`docs/archive/cb2sitting_Mars.exe-20260810-15.30.16.log:293`.
The entry explicitly kept `fixed`, without re-earning `tested` or reading the
actual exit Comfort charge. Those historical observations are not promoted
into fresh 1.1.0 statistics or Comfort verification here. Hotfix 2's retained
wrapper decision is the starting point, not a new runtime proof.

Direct final registry
`docs/archive/logs/stillneeded_registry_Mars.exe-20260912-00.29.01-6a91a190.log:254`
reports active; the settled second boot reports applied at
`docs/archive/logs/stillneeded_Mars.exe-20260912-00.25.42-6a91a190.log:111`.
No colony loaded or suite ran. Installation is measured; correction of the
remaining statistics is a current source conclusion, not a fresh cure witness.

What I did NOT check, by name:

- Fresh organic 1.1.0 boarding and per-subject `start_wait` transition.
- Paired station/train/track samples for the same current journey.
- Fresh Comfort target, LuxuriousTrains or full-train charge observations.
- Interrupted/abducted boarding, missing Station holder or failed identification.
- Fresh TrainWaitTime TestKit probe or `RunAll()`.
- Save/load/uninstall or fresh 1.0.7 execution.
- F79/F80 triggers, capacity, route failures or other train modules.
- Other public examples, aggregate repair counts, fenced prelaunch verdicts.
