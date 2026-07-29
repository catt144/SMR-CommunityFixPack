# Surviving Mars Relaunched Bug Fix Research Dossier

## Where the game stands now

*Surviving Mars: Relaunched* released on Steam on November 10, 2025. As of July 25, 2026, its Steam review profile is still only **Mixed** overall, with **53% positive among 1,375 English reviews** and **57% positive in the last 30 days**, which is consistent with a game that has clearly improved but still carries persistent technical debt and player distrust. Steam’s store page also says the game is moddable and supports Workshop, which matters because the original game’s stability reputation was heavily propped up by community fixes. citeturn12view4

Officially, the relaunch has received a steady stream of fixes: Hotfixes **1.0.1**, **1.0.2**, **1.0.3**, then patches **1.0.4**, **1.0.5**, **1.0.6**, **1.0.7**, plus a **June 11, 2026 Linux Stability Update**. That cadence shows real post-launch support rather than abandonment. At the same time, the patch notes repeatedly acknowledge that some bugs were save-specific, that some fixes only applied to **new games**, and that old saves could still retain broken state. That detail is important for your mod design, because it argues for **save repair and state sanitation** rather than only patching live simulation logic. citeturn16view3turn16view2turn19view4turn41view0turn16view0turn14view3turn16view1turn16view5

One more useful baseline: the community wiki states that **all patches from the original version are included in Surviving Mars: Relaunched**. So for your purposes, the most valuable bug candidates are not “old issues that were officially fixed years ago,” but rather three narrower groups: issues that were only ever fixed by modders in the original game, issues that were reintroduced by the remaster/relaunch, and issues the official Relaunched patches only partially fixed. citeturn20search0

The high-confidence conclusion from the public record is that Relaunched is **not** still in its launch-week state, but it **does** still appear to have a long tail of broken edge cases around **mystery sequencing, rockets and asteroid landers, trains, colonist routing, underground-surface synchronization, and save migration**. Those are the best targets for a comprehensive community bug-fix mod. citeturn41view0turn17view0turn17view2turn17view3turn17view4turn24view0turn24view1turn36search1turn36search4

## What the official patches already covered

The early patch sequence focused on severe launch blockers. **Hotfix 1.0.1** hit Asteroid Lander loading and destination logic, fixed duplicate Underground Earth Embassies, added elevator drone assignment and shared prefabs between surface and underground, and addressed the **Inspiring Architecture** freeze, though the notes warned that already-corrupted saves might remain affected. **Hotfix 1.0.2** fixed train assignment to tracks, asteroids being held indefinitely by the Asteroid Catcher, and missing funding events. **Hotfix 1.0.3** then addressed more freezes, colonist behavior issues, Lander evacuation logic, Martian Assembly population and achievement handling, and UI notification behavior. citeturn19view0turn19view2turn16view2turn19view4turn41view0

**Patch 1.0.4** looks like the first larger systems pass. The official summary says it fixed a crash when switching maps, added manual and automated Asteroid Lander modes, stopped drones from endlessly moving resources between Landers, improved cave entrance placement, fixed Bottomless Pit lab placement, fixed train power transfer, station connections, and routing, fixed colonist homelessness, unemployment, overpopulation, and suffocation cases, fixed rockets disappearing on trips to Earth, and fixed stuck construction and Terraforming update problems. That is a very broad “base systems” patch, and it already overlaps heavily with classic modder pain points from the original game. citeturn41view0turn41view1turn41view2turn41view3

**Patch 1.0.5** explicitly targeted “the most common issues and quality-of-life improvements” players had been reporting. Its most important bug-fix items were a **Research screen softlock**, another batch of crash fixes, train tracks failing to transfer power in a specific build order, trains endlessly hauling some resources while refusing others, Asteroid Landers reserving landing sites after auto-mode cancellation, and a fix for **mystery progress being lost**, though the patch notes are explicit that this applied **only to new games** and that existing saves might still be broken. It also fixed Underground Domes appearing empty while populated, colonists getting stuck in passages, research progress showing above 100%, Mars Reservation being re-fabable, and *The Last War* mystery blocking Asteroid Landers. citeturn16view0turn18view0turn18view1turn18view3turn17view5

**Patch 1.0.6** was more architectural. Its Underground Elevator rework turned the Elevator into shared storage between maps, merged underground and surface life support and power grids, and explicitly said this solved issues where grid production could be doubled or not transferred at all. It also reworked underground dome rules, fixed mystery sequence triggers that had been failing to fire, fixed trains causing colonists to get stuck waiting indefinitely, fixed undemolishable tracks and broken station connections, fixed a Martian Assembly state stuck on “1 hour until next session,” fixed meteor markers and lingering flashing drone lights, and fixed several colonist pathing and reachability problems. Crucially, the notes also say that **existing games retain old mystery sequences in the save**, and that old Elevator saves could still require players to demolish and rebuild pipes and cables. That is exactly the kind of save-state residue a bug-fix mod can clean up. citeturn14view3turn17view0turn17view1turn17view2turn17view3turn35view0

**Patch 1.0.7** continued that trend. It reworked rocket destination and export flow, fixed colonists commuting by train and then walking huge distances and suffocating, fixed incorrect reachability checks that stopped colonists and tourists from boarding rockets or using elevators, fixed more cases of trains getting stuck, unusable or unsalvageable tracks, looped-station freezes, some underground freezes, drone task loops, old-save crashes, and several mystery-specific issues. Then the **Linux Stability Update** fixed a specific crash path when the game failed to access Braze on Linux and Steam Deck. Officially, then, the dev team has already addressed many of the loudest launch bugs. The open question is how many **edge cases** and **save-baked variants** remain. citeturn18view5turn18view6turn18view7turn17view4turn16view5

## What the classic bug-fix mods tell you to test

The original game’s mod ecosystem is a very strong map of where *Surviving Mars* historically broke. The single most important source is **ChoGGi’s “Fix Bugs”** collection, which the Steam Workshop describes as fixing **“a few dozen bugs,” mostly from Below & Beyond and bugged Storybits**. The collection description also says some items were obsolete as official fixes landed, which is useful because it means the collection is not just a pile of tweaks; it is a living record of what the official game did not reliably handle. citeturn10view1

What matters most is the *shape* of those fixes. A large share are **save-state repairers** that run on load: **Fix Rocket Stuck** checks for rockets stuck on the ground in bad states; **Fix Remove Invalid Label Buildings** cleans invalid references from long-running saves; **Fix Remove Blue Yellow Marks And Ghosts** clears persistent build markers and ghost rovers; **Fix Shuttles Stuck Mid-Air** runs on load to reset stranded craft; **Fix Buildings Broken Down And No Repair** repairs buildings that drones will not touch; **Fix Deposits Wrong Map** moves deposits that spawned on the wrong map; **Colonists underground crash** addresses cross-map pathing failures; **The Bottomless Pit Anomaly is missing** corrects a broken anomaly spawn path; and **Fix Landscaping Freeze** handles a landscape-mark overflow that could eventually freeze terrain editing. These are not balance mods. They are exactly the kind of “state sanitizer” logic that community patches excel at. citeturn10view1turn11view1turn33view0

ChoGGi’s fixes also identify recurring simulation bugs that are easy to overlook if you only read official patch notes. A few examples: repeated colonist visits to already-satisfied daily-interest buildings wasting resources; destroyed tunnels still being treated as usable; farm oxygen persisting after the farm is removed; malfunctioning drones never repairing properly at Drone Hubs; and storybit/follow-up entries assigned to the wrong category so they never trigger. These are valuable not because every one is confirmed in Relaunched, but because they show the types of engine-level invariants the original codebase routinely violated. citeturn33view0

Other modders reinforce the same pattern. **Tremualin’s Library** says it fixed colonists ending up with multiple workplaces, plus trait-loading bugs for Sanatorium and School systems. That tells you that colonist assignment and trait persistence were brittle even outside ChoGGi’s work. The **Martian Express Fix Pack** is also instructive: it combines five train-related fixes and QoL mods covering routing, crowding, per-resource storage, electrified tracks, and train usefulness. That pack is partly balance, not just bug-fixing, so you should **not** port it wholesale as a “bug fix mod.” But it is excellent evidence that the train system historically needed both correctness fixes and usability patches. citeturn34view0turn34view1

Finally, a few standalone original fixes remain worth preserving as explicit regression tests even if you do not port them directly. **Stuck Rocket Fix - Force Launch** exists because rockets could get stuck in a “ready for takeoff” limbo and sometimes remain bad even after returning. **Fix Sol 2983** exists because some very long saves hit integer-overflow-like behavior that made late-game play unstable. I did **not** find clean current evidence that the Sol 2983 issue is present in Relaunched, so I would treat that one as a **carry-over test candidate**, not a confirmed Relaunched bug. But the fact it needed a dedicated mod in the original means it is worth consciously regression-testing in long automated colonies. citeturn34view2turn34view3turn20search0

## The bug families that still look alive in Relaunched

**Mysteries and storybit sequencing** are still the clearest “partially fixed, probably still worth modding” category. Official patches hit this area repeatedly: 1.0.5 fixed lost mystery progress for **new games only**; 1.0.6 says it fixed underlying global sequence issues and many specific triggers; 1.0.7 fixed additional mystery-specific cases like Wildfire applicant generation and AI-mystery drone havoc. But as of late July 2026, Steam’s active discussion list still includes **“Mystery do not start”** and **“Mysteries that Work,”** and the pinned discussion list also still shows **“Inner Light Mystery Will Not Start.”** That combination strongly suggests the official fixes reduced mystery failures without eliminating them, especially for certain saves, certain mysteries, or certain trigger chains. citeturn18view3turn14view3turn18view7turn36search1turn41view0

**Rockets and asteroid landers** are another high-priority candidate. Official fixes here are extensive: 1.0.1 fixed Lander loading and destination confusion; 1.0.2 fixed Asteroid Catcher retention; 1.0.4 added manual/automated modes and stopped drones endlessly moving resources between Landers; 1.0.5 fixed landing-site reservation after canceling auto mode; 1.0.6 improved asteroid rules again; and 1.0.7 reworked the entire rocket destination/payload flow. Despite that, Steam discussions in May, June, and July 2026 still show **rockets stuck on “unloading,”** resources getting stuck inside rockets, and trade rockets that cannot be canceled and can remain stuck with the issue. The Workshop history around **Fix Rocket Stuck** also shows Relaunched users still asking for a port and still reporting “foreign aid” rockets stuck on the pad in 2026. That is enough evidence to keep rocket-state repair very high in your backlog. citeturn19view0turn16view2turn41view1turn18view0turn14view3turn18view5turn24view0turn24view1turn24view2turn38search0turn38search4

**Trains** remain the most obvious subsystem with a “death by edge cases” reputation. Officially, the devs have fixed train assignment, power transfer, station connections, routing, colonists getting stuck waiting at stations, undemolishable tracks, stuck trains, unusable tracks, looped-station freezes, and old-save station reconnection issues. But the public record still shows train pain surfacing in several places: the long negative Steam review complaining about undeletable tracks and limited train functionality; current Workshop comments in 2025–2026 describing passenger transport failing after repairing meteor-damaged track while cargo keeps working; and community posts in early 2026 still asking whether trains are “already working as intended.” The train system is very likely improved compared with launch, but it still looks like the best candidate for a mod that adds **self-healing route reconstruction** and **validation of station-track graph integrity**. citeturn41view1turn17view0turn18view6turn31view0turn34view1turn27view2

**Colonist pathing, employment, and homelessness** are also still worthy of a dedicated pass. Relaunched patches have hit this repeatedly: 1.0.3 fixed erratic unemployment and dome-selection issues; 1.0.4 fixed homelessness, unemployment, overpopulation, and suffocation cases; 1.0.5 fixed colonists getting stuck in passages; 1.0.6 fixed dome-filter relocations, refabbed Naturalist Habitat pathing failures, and more behavior issues; and 1.0.7 fixed multiple commuting, dome preference, and boarding/reachability bugs. Yet launch-period Steam threads and reviews repeatedly report colonists remaining unemployed or homeless despite open jobs and housing, manually assigned workers immediately abandoning work, and citizens suffocating on long cross-dome or train-related trips. I would treat this as **partially fixed but still structurally fragile**, especially when multiple systems interact: filters, passages, trains, underground transitions, and special housing. citeturn19view4turn41view1turn17view5turn17view3turn17view4turn25view2turn25view0turn25view1turn31view0

**Underground and cross-map synchronization** still look important because the official notes openly admit old-save residue. The 1.0.6 elevator rework merged surface and underground grids and changed resources into shared storage logic, but the official notes warn that older saves might still need pipes and cables demolished and rebuilt. ChoGGi’s old modded fixes around deposits appearing on the wrong map, colonists crashing on cross-map pathing, and the Bottomless Pit anomaly spawning incorrectly are all examples of exactly the kind of cross-map bugs that survive normal patching because they are already baked into a save. If your mod has a single signature feature, it should probably be a **load-time cross-map consistency pass**. citeturn14view3turn14view2turn33view0

**Visual residue and stale state cleanup** are lower severity but good “community patch” material. Relaunched has already fixed stuck dust-storm notifications, lingering smoke and particles, meteor prediction markers stuck on the map, red flashing drone lights, stuck effect-radius hexes, and stuck colorizations during placement. But community reporting still mentions rare metal extractors leaving perpetual smoke after refab, depots and anomalies vanishing when zoomed in after 1.0.7, and older mystery reports about permanent map markers from Dredgers-like events. These are not always game-breaking, but they are exactly the sort of fixes that make a bug-fix pack feel high quality. citeturn17view3turn17view4turn28view1turn26search3turn21search5

## The shortlist I would put at the top of your backlog

If your goal is a **comprehensive** bug-fix mod rather than a grab bag of isolated scripts, I would prioritize the backlog in this order.

**First priority should be save-baked hard blockers.** That means mystery/state sequencer repair, rocket and lander stuck-state repair, train graph repair, cross-map reachability cleanup, and construction objects that become unusable or unsalvageable. These are the categories where official notes most often either admit old saves can remain broken or where players still report “dead save” outcomes after several patches. citeturn14view2turn17view2turn24view0turn24view1turn24view2turn17view0turn18view6turn37view0turn27view4

**Second priority should be colonist and drone behavioral sanity checks.** The original and Relaunched records both point to broken employment, housing, maintenance, repair, and cross-dome routing logic as recurring weak points. A “sanity” module that periodically or on-load verifies reachable homes, reachable workplaces, repair eligibility, and stale task loops is likely to fix more real player pain than another pass on balance or UI. citeturn34view0turn33view0turn25view2turn17view3turn17view4

**Third priority should be train-specific state repair.** Even though trains have received a lot of official attention, they remain one of the most complained-about subsystems in reviews, discussions, and historical mod packs. I would strongly consider a train watchdog that validates station connectivity, passenger-route reachability, unbuilt/unsalvageable track elements, and stale “too far” results after damage-and-repair cycles. citeturn34view1turn31view0turn17view0turn18view6

**Fourth priority should be visual and notification cleanup.** This is lower urgency, but it is classic community-patch territory and highly visible to players. Lingering FX, range hexes, impact markers, map ghosts, negative resource displays, and stale warnings are all areas where the public record shows official progress and remaining long-tail weirdness. citeturn17view3turn35view0turn11view1

**Fifth priority should be regression tests for old original-problem areas even when not freshly confirmed in Relaunched.** Sol 2983 overflow, destroyed tunnels still behaving as valid, follow-up storybits in the wrong category, and other deep-state bugs should be put into an automated or scripted test suite. I would not ship a fix for every one of these on day one, but I would absolutely add them to your lab checklist. citeturn34view3turn33view0turn20search0

## How I would hunt these bugs and structure the mod

The clearest design lesson from both the original mod scene and the Relaunched patch notes is that your mod should probably have **two layers**.

The first layer should be a **load-time save sanitizer**. That is the pattern ChoGGi used over and over, and it aligns perfectly with Relaunched’s own admission that some fixes do not fully heal existing saves. This layer should search for invalid labels, broken rocket states, stations linked to dead tracks, impossible colonist path targets, wrong-map deposits or anomalies, ghost markers, stale malfunction states, and underground/surface connection mismatches. The high leverage here is that it can rescue old saves the official patches no longer can. citeturn11view1turn33view0turn14view2turn17view2

The second layer should be a **runtime guardrail layer** that prevents the bad states from reforming. Based on the sources, that means hooks around mystery trigger progression, rocket status transitions, train/station graph updates, reachability checks for colonists moving between domes and maps, drone repair task assignment, and cleanup of visual residues after objects are destroyed or refabbed. That is also where you can add lightweight self-healing: if a train route becomes invalid after meteor repair, rebuild route links; if a rocket is empty but stuck unloading, re-evaluate its state; if a colonist’s work or home target is unreachable, force reassignment before suffocation logic triggers. Those are inferences from the pattern of failures, but they are directly grounded in the problem families players and patch notes keep surfacing. citeturn24view2turn34view1turn17view4turn17view0turn25view2turn31view0

For testing, I would build a matrix around **new game vs old save**, **surface vs underground vs asteroid**, and **recoverable vs unrecoverable state**. At minimum, I would script test scenarios for: mystery start and progression under different mysteries; rockets returning from expeditions with empty or partial payloads; asteroid evacuation with manual and automated Landers; train repair after meteor damage; colonists commuting via passages, trains, tunnels, elevators, and dome filters; refabbing Naturalist Habitats and rare-metal extractors; and late-game save load on a colony with heavy politics, underground usage, and large logistics networks. The official notes and community complaints repeatedly show those transitions are where state corruption hides. citeturn19view0turn41view1turn17view0turn17view1turn17view2turn17view3turn17view4turn28view1

For evidence collection, the best practical workflow is to collect **save files, logs, and exact reproduction seeds**. Relaunched players are repeatedly told on Steam to use **Ctrl+F1** for bug reporting, and Paradox staff on Reddit explicitly asked players for crash logs from **`%AppData%\Surviving Mars Relaunched\logs`** on Windows. If you are building a community bug-fix effort, copying that discipline will help you separate true engine bugs from mod conflicts and from one-off corrupted saves. citeturn24view0turn24view1turn37view1

## Bottom line for your mod plan

If I were scoping this project, I would describe the current state of *Surviving Mars: Relaunched* like this: **the official patches have already fixed a lot of the headline launch disasters, but the game still shows a strong pattern of edge-case failures and save-baked corruption in a handful of subsystems**. That means a community bug-fix mod still makes sense, but it should not try to re-solve everything the official team already solved. It should focus on the remaining fault lines where modders historically added the most value and where player reports still cluster now: **mysteries, rockets/landers, trains, colonist reachability and assignment, underground-surface synchronization, and save cleanup**. citeturn12view4turn41view0turn17view4turn24view1turn24view2turn36search1turn36search4turn31view0

The most important strategic insight is that your best “hook” is probably **not** a single megafix for one subsystem. It is a **reliable state-repair framework** that can sanitize old saves on load, enforce a few critical invariants at runtime, and then layer targeted subsystem fixes on top. That approach matches the original mod ecosystem, matches the official patch caveats, and gives you the best chance of creating something the Relaunched player base will actually trust. citeturn10view1turn11view1turn33view0turn14view2turn17view2


Best guess count and list of known or likely bugs:
Best working estimate: about 50 distinct bug candidates

I can extract 52 reasonably distinct bug mechanisms from the report. That does not mean Relaunched currently has 52 independently confirmed, reproducible bugs:

Roughly 24 have recent or relatively strong Relaunched evidence.
About 18 are likely still possible or only partially repaired.
The final 10 are legacy regression tests inherited from the original game’s bug-fix ecosystem.

Some will probably collapse into the same underlying root cause once you inspect the Lua—for example, several mystery failures may all originate in one broken sequencer.

A. Known or high-confidence Relaunched candidates — 24
Mysteries and events
Mystery never starts at all despite the prerequisites apparently being met.
Inner Light fails to start.
Mystery progress is lost or corrupted in older saves.
Mystery stalls midway through its sequence, such as Cave of Wonders or Last War–type failures.
Event or mystery objectives fail to clean up or advance, including Dredgers/Treasure Map–type behavior.
Rockets and asteroid operations
Rocket remains stuck on “Unloading” while empty.
Resources remain trapped inside a rocket and are not assigned unloading tasks.
Trade, expedition, or story rocket cannot be canceled, leaving it permanently stuck.
Passenger rockets malfunction during challenges.
Asteroid rocket or lander payload state becomes corrupted, producing waste, loss, duplication, or failure to unload correctly.
Trains
Passenger transport stops working after meteor-damaged track is repaired, while cargo may continue functioning.
Train becomes permanently stuck or route-deadlocked.
Track section cannot be demolished or salvaged.
Station-to-track graph becomes disconnected or corrupted.
Train endlessly transports certain resources while ignoring others.
Colonists and domes
Colonists remain unemployed despite reachable open workplaces.
Colonists remain homeless despite reachable available residences.
Colonists become stuck in passages or waiting at train stations.
Colonists select an excessively long route and suffocate while commuting.
Incorrect reachability result prevents boarding a rocket or using an elevator.
Underground and stability
Surface and underground resource, power, or life-support state becomes desynchronized.
Underground pipes can apparently be damaged by a surface dust storm.
Depots or anomalies disappear visually at certain zoom levels.
A colony enters a reproducible simulation hardlock or save-specific freeze.
B. Likely or partially fixed candidates — 18

These were officially addressed in some form, historically common, or closely related to current reports. They should be tested before assuming they are gone.

Rockets and landers
Rocket enters launch limbo or disappears during departure/return.
Asteroid Lander loads the wrong payload or retains an incorrect destination/state.
Canceled automated landing leaves a landing site permanently reserved.
Drones endlessly transfer resources between rockets or Asteroid Landers.
Trains
Train tracks fail to transfer power depending on construction or repair order.
A looped station arrangement freezes the simulation or corrupts routing.
Colonists
Manual workplace assignment is immediately discarded.
Dome filters or preferences fail to relocate colonists correctly.
A colonist is assigned to multiple workplaces simultaneously.
Cross-map colonist routing between surface and underground crashes or strands the colonist.
Underground and anomalies
Deposits or anomalies exist on the wrong map layer.
Bottomless Pit anomaly is missing, inaccessible, or associated structures cannot be placed correctly.
Refabbing a Naturalist Habitat leaves invalid paths or unreachable colonists.
Drones, vehicles, and construction
Broken building receives no valid repair task.
Drone enters an endless task-selection loop.
Malfunctioning Drone Hub drones do not repair correctly.
Shuttle remains permanently suspended in mid-air.
Construction site becomes permanently stuck, unusable, or unsalvageable.
C. Legacy regression-test candidates — 10

I would not advertise these as confirmed Relaunched bugs yet, but they are worthwhile test cases because original-game modders had to repair them.

Mystery or storybit follow-up is assigned to the wrong category and never fires.
Invalid building or object references remain in internal labels after deletion.
Ghost rovers, build markers, or other deleted objects remain visible or registered.
Destroyed tunnel continues to be treated as a valid transport connection.
Farm oxygen production persists after the farm is removed.
Colonists repeatedly visit an already-satisfied interest building and consume resources unnecessarily.
Research interface softlocks or research progress exceeds 100%.
Lingering smoke, particles, meteor markers, flashing drone lights, or effect-radius hexes remain indefinitely.
Landscaping freezes after excessive or corrupted landscape marks accumulate.
Very late saves encounter Sol 2983–style timing, integer, or scheduling overflow.
What I would call the actual project scope

A realistic first release should probably target 12–18 repairs, not all 52. The highest-value initial modules would be:

Mystery state validation and recovery.
Rocket unloading and state-machine repair.
Train graph validation and reconstruction.
Colonist reachability and assignment sanity checks.
Surface-underground synchronization repair.
Stuck drone, shuttle, construction, and building-repair recovery.
Stale object, marker, and visual-effect cleanup.