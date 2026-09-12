# F53 / C83 / F117 one-module review

Task/agent: `/root/module_b`. Review anchor: `2983fac`. Captured inputs:
`CENSUS.json`, game **1.1.0.403908**. Module and site fix-list byte hashes still
match the capture. Direct settled registry reports `ArrivalDeaths` active at
registry-log line 237. Recommendation: **KEEP**; C83 supplies a witnessed current
benefit, and current arrival placement/destination consumers still use both
patched seams. F53 and F117 retain their separately named verification limits.

Disagreement with the existing migration derivation: a nonnegative returned
distance does **not always prove a finite foot route**. For a dome beyond the
walking cap, `CheckWalkableDistance` returns its positive straight-line distance
before pathfinding (`Dome.lua:218-225`). Therefore the `dist >= 0` safety guard
in `_GameUtils.lua:403` can still admit a far dome without establishing actual
connectivity. The ordinary fallback does exclude a returned negative distance,
but the migration report's broader finite-foot-route interpretation is too
strong. Its F53 diagnostic need not establish connectivity for that far-distance
branch. This does not supply a new observed defect or exercise F117.

No public-row contradiction requiring a correction was established in this
bounded pass. Interpret F53's waiting and passability descriptions as the
specific changes below, with their existing limits; they are not new evidence
of death prevention on 1.1.0. C83's prior attended witness remains separate.

| module | entry | applies? | consumer still reads it? | row true? | bullet true? | verdict | evidence file:line on 1.1.0.403908 | basis | what I did NOT check |
|---|---|---|---|---|---|---|---|---|---|
| Fix_ArrivalDeaths.lua | F53 + C83 + F117 | yes: direct settled registry active at line 237; installation only | yes: Arrive and transport routing read destination/elevator fields; OnArrival still follows raw placement on ordinary, expedition-return and train disembark paths; ChooseDome scoring and suitability consume the colonist shape | partial: F53 row 56 remains supported for raw placement/far fallback but fresh terrain/distance outcome unverified; C83 row 66 remains true for the witnessed overflow layout and states its no-alternative stand-down | partial: F53 death headline maps correctly but fresh 1.1.0 terrain/distance cure unverified; C83 unsafe-destination headline maps correctly and retains its attended witness; no dedicated F117 headline | KEEP | C:/Dev/SMR-SrcArchive/1.1.0.403908/Src/Lua/Units/Colonist.lua:1592; C:/Dev/SMR-SrcArchive/1.1.0.403908/Src/Lua/Units/Colonist.lua:1619; C:/Dev/SMR-SrcArchive/1.1.0.403908/Src/Lua/_GameUtils.lua:403; C:/Dev/SMR-SrcArchive/1.1.0.403908/Src/Lua/Buildings/Community.lua:445 | SOURCE: defects and consumers; F53 realized harm/cure and F117 station execution remain unobserved in this review | F53 impassable terrain; far-distance colony comparison; F117 passenger-station recipe; fresh C83 replay; UNKNOWN runtime decline; paired elevator control; train journey outcome; save/load/uninstall |

Primary evidence (game citations are read-only **1.1.0.403908/Src**):

- **Arrival entry and destination consumer:**
  `Lua/Buildings/RocketBase.lua:2064-2073` and
  `Lua/CargoTransporterNew.lua:996-1006` assign the chosen dome/elevator pair,
  mark `arriving`, construct the colonist and reserve a bed before the next
  passenger is chosen. `Lua/Units/Colonist.lua:2233-2235` remains the sole
  string-command issuer of `Arrive` found by tree-wide search. Its body reads
  `emigration_dome or self.dome` into a local at `:1592`, then commands travel
  at `:1628`. The pre-Idle correction therefore still precedes consumption.
- **F53(a), raw placement and all sibling seams:**
  `Lua/Units/Colonist.lua:1612-1623` disembarks at the raw rocket spot, without
  a passable-point search; `OnArrival` is pushed at `:1594` and runs at `:1631`
  or during the command change. `CommonLua/Classes/CommandObject.lua:231-250`
  runs pending destructors before the new command body. The same raw placement
  remains on expedition return at `Lua/Units/Colonist.lua:5104-5116`, with
  `OnArrival` pushed at `:5097`. The train-specific arrival sibling also has
  raw placement then `OnArrival` at
  `Lua/Units/ColonistTransport.lua:321-349`, before `GoToStation` at `:351`.
  Current F53's pre-OnArrival snap thus remains on meaningful paths. The
  non-arriving `GameInit` call at `Lua/Units/Colonist.lua:276-277` also exists;
  the module's holder/valid-position/passability guards limit that call.
  Contrast ejection's explicit passable-point placement at
  `Lua/CargoTransporterNew.lua:1053-1054`. No terrain cure was observed here.
- **F53(b), far fallback remains despite the new negative-distance guard:**
  `Lua/_GameUtils.lua:401-411` uses returned distance alone for the safety
  fallback, but requires `is_walking` and welcoming state for regular candidates.
  `Lua/Buildings/Dome.lua:218-225` returns a positive straight-line distance
  for an over-cap destination before testing its foot path. `ChooseDome` at
  `Lua/_GameUtils.lua:486-500` starts with `safety_dome` and retains it if no
  candidate wins with suitable space. F53 reselects without that unsafe fallback;
  an empty re-pick clears `emigration_dome`, so vanilla's `Arrive` raises
  `ConfusedColonists` at `Lua/Units/Colonist.lua:1625-1626` instead of that walk.
  This withholds the destination; it does not deliver the colonist to shelter.
- **Elevator and train consumers remain current:**
  `Lua/Units/Colonist.lua:3562-3579` reads the paired elevator and can use a
  train on the far side. `Lua/_GameUtils.lua:432`, `:441`, `:499-500` maintains
  the chosen dome/elevator relationship. The module preserves a valid assigned
  elevator connection. The transport sibling reads the pair before Arrive at
  `Lua/Units/ColonistTransport.lua:196-201`; its command routing can start a
  station journey at `:405-442`, with arrival-specific disembark at `:370`.
  Re-selection is not proof of the eventual train/elevator journey.
- **C83, the current omission and its bounded cure:**
  `Lua/_GameUtils.lua:382-384` defines welcoming as player-enabled, accepting
  colonists and life-supported; `:403-407` omits that check from the safety
  fallback, while `:408` checks it for normal candidates. `:487-496` retains
  the unsafe fallback once suitable housing is unavailable. The module's
  arrival-only reroute picks the nearest returned welcoming candidate as the
  homeless fallback, including a full safe dome. It keeps vanilla's assignment
  with no welcoming alternative or UNKNOWN argument shape. Public
  `Community:CanAcceptNewColonists` remains at
  `Lua/Buildings/Community.lua:96-98`; life support remains water plus breathable
  atmosphere or power/air at `:462-464`. The station append happens after sorting
  at `Lua/_GameUtils.lua:446-478`, so the module correctly scans returned
  distances instead of assuming `domes[1]` is nearest.
- **F117, both current argument consumers were opened independently:**
  `Lua/_GameUtils.lua:490`, `:492` passes the same colonist to scoring and
  housing suitability. `Lua/Buildings/Community.lua:445` directly reads
  `colonist.traits`; its housing branch at `:412-413` passes the colonist to
  `Residence:IsSuitable`, which reads `.traits` at
  `Lua/Buildings/Residence.lua:198-200`. Trait scoring delegates through
  `Lua/Traits.lua:1122-1123` to the attribute index in `Lua/Filter.lua:116`.
  Current ArrivalDeaths' discriminator selects the colonist shape for this
  source body; its live re-selection passes that shape. This is a repair to
  our wrapper's changed contract, not a distinct vanilla defect.
- **F117 station reach is separate from C83:**
  `Lua/_GameUtils.lua:450-478` appends welcoming dome-cluster destinations
  reachable through a passenger station, including destinations outside foot
  range and without a paired elevator. That is the source route for the
  unrun station recipe. A far pad without that station gives an empty ordinary
  candidate list; the re-selection then does not call `GetScoreFor` inside
  `ChooseDome`. A paired elevator bypasses F53's reachability reroute. C83 can
  also fill the session argument-shape cache, so that cache alone does not
  establish execution of a later station landing.

Public surfaces assessed separately:

- **F53 row** `C:/Dev/SMR-CommunityMods/content/fix-list.md:56-64` and card
  headline **Rocket loads of new arrivals died on their way to a dome**:
  current code still changes raw placement and withholds a far unsafe fallback.
  The far branch can use straight-line distance as that row describes. A
  passable snap is conditional on a nearby point being found and does not prove
  destination connectivity; no fresh terrain/death-prevention result is claimed.
- **C83 row** `C:/Dev/SMR-CommunityMods/content/fix-list.md:66-80` and card
  headline **New arrivals moved into a dome that was switched off, quarantined
  or without air**: both remain supported by the current fallback omission,
  the unchanged arrival-only correction and the owner-attended 2026-09-10
  witness. That witness covered safe control, forced overflow reroute and one
  sol follow-through; it did not observe eventual deaths in the unfixed dome.
  Archived primary log
  `docs/archive/c83_attended_Mars.exe-20260910-17.36.10.log:372` records the
  reroute. C83 does not override intentional later must-have-filter migration
  into an unsupplied dome (`Lua/Buildings/Community.lua:437`).
- **F117** has no separate public row/headline in these captured surfaces.
  The C83 witness does not upgrade F117's station recipe to attended coverage.

Installation evidence:
`docs/archive/logs/stillneeded_registry_Mars.exe-20260912-00.29.01-6a91a190.log:237`
reports active; prior archived boot reports applied at
`docs/archive/logs/stillneeded_Mars.exe-20260912-00.25.42-6a91a190.log:92`.
No colony loaded, suite ran or ArrivalDeaths reroute/heal message occurred in
that menu measurement. Captured bodycheck success is not consumer clearance;
the current primary paths above were read independently.

What I did NOT check, by name:

- F53 impassable terrain placement and nearby-point success in a fresh colony.
- F53 far-distance landing comparison or eventual oxygen/death outcome.
- F117 passenger-station recipe, per-landing re-pick list or wrong-shape game leg.
- F117 UNKNOWN runtime decline or fresh TestKit argument/arrival probes.
- Fresh C83 replay, alternative layouts or no-welcoming-dome outcome in play.
- Paired elevator arrival and eventual train/return journey execution.
- Cross-mod Residency Control runtime composition or tourist exemption control.
- Save/load/uninstall behavior, fresh 1.0.7 branch execution or screen rendering.
- Other modules, whole-card counts or fenced prelaunch sweep verdict reports.
