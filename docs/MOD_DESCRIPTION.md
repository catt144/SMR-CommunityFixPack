# Mod Description (draft) — Community Fix Pack

This file is the working draft of the public mod page text (Paradox Mods /
Steam Workshop). Keep it in PLAYER language — no file paths, no function names.
Update the fix lists in the same commit that implements a fix. Sections marked
[DRAFT NOTE] are instructions to ourselves and get deleted before publishing.

---

## Community Fix Pack — Surviving Mars: Relaunched

Fixes bugs. Only bugs. Every fix in this pack targets a defect we verified in
the game's own code — no balance changes, no redesigns, no opinions. If the
game's code says a Sensor Tower should delay meteors and instead it attracts
them, we fix that. If we merely disagreed with a design choice, it's not in
this pack (with one clearly-labeled optional exception below).

**Works with your existing saves, and built to be safe to add or remove at any
time.** The mod
writes almost nothing into your savegame, and what it does write is inert
without it: a few `SMRFixPack_*` bookkeeping fields (a timestamp on a housing
reservation, a "the player has set this payload" flag on a rocket, and — from
the optional modules — an acknowledgment stamp on a dismissed building warning
and a "closed to new residents" flag on a dome) whose absence simply means the
pre-fix behavior, and — where a save-repair pass restored a bonus a broken
patch migration dropped — an ordinary label modifier the game handles like any
other. Removing the mod simply lets the original bugs come back. One footnote
for the optional **Drone stat dials**: a non-base dial is stored in the save
as an ordinary modifier too, so a save made with a dial active keeps that
boost if you later remove the mod — harmless, but permanent. Set the dials
back to base (and load/save once) before uninstalling if you want a clean
vanilla save.

**What we can promise, and what we can't.** We would rather tell you this
plainly than have you find it out. Here is what actually stands behind the
paragraph above: every fix inspects the game's own code before it patches
anything, and switches itself off if the game no longer looks the way that fix
expects, so an official patch that fixes a bug retires our version rather than
fighting it. The savegame footprint is deliberately tiny and is enumerated above
rather than summarised. The pack carries an automated suite of 77 checks that is
run against both a modded and an unmodded build before release, and
add-then-remove cycles are part of that testing.

**Why we make a fuss about this at all.** `[FAQ]` The game's own modding
documentation says that when you save, any mod code that happens to be waiting
on something is written into the savegame and keeps running from there after
you load — that is a deliberate engine feature, not a bug, and it means the
normal state of affairs is that a mod leaves traces in your save. Almost no
Surviving Mars mod promises otherwise, and that is a reasonable position, not a
failing on their part: the engine makes a clean uninstall expensive rather than
impossible. We decided to treat it as a requirement instead, which is why the
footprint above is a list rather than a summary. *(Sources: the original
game's `LuaSavegame.md.html` modding page and a survey of 471 published mods —
`docs/reports/PRIOR_ART_SURVEY.md` §1, §2, §4. **[DRAFT NOTE]** keep this
paragraph's claims to what that survey and `BUG_LIST_AUDIT.md` can cite; it is
about a documented engine behaviour and a community norm, never about other
authors doing worse work.)*

**[DRAFT NOTE — CONDITIONAL, do not publish until F86 Tier 1 has landed AND
verified** (project prompt chain 4; then delete this note and keep the
sentence)**.]** `[FAQ]` Once the Tier-1 repairs ship, one more sentence becomes
true and belongs here: *"As far as we can tell, no mod in either game's
community has held itself to this uninstall standard before — not because
others fell short, but because the engine never made it cheap enough to
promise."* The survey found the shapes we use all have precedent
individually; what has none is treating uninstall-cleanliness as a requirement
with an enumeration behind it (`PRIOR_ART_SURVEY.md` §6). **Until Tier 1
verifies, the claim is not ours to make** — our own `Fix_MeteorFrequency` is
currently one of the modules that leaves a running thread behind.

**None of that is a guarantee, and we are not going to pretend otherwise.** We
cannot test every combination of other mods, every colony shape, every save
state, or every future game patch — and a patch can change the code underneath
us at any time. If a save matters to you, back it up before adding *any* mod to
it for the first time. That advice is not specific to this pack; it is just
true, and most people only learn it the expensive way.

**Playing on Xbox, PlayStation, or the Microsoft Store version?** One platform
rule to know before you install — it applies to every mod, not just this one:
**while any mod is enabled, the game does not unlock achievements on Xbox,
PlayStation, or the Microsoft Store.** Steam and other PC versions are not
affected — achievements keep unlocking normally there with mods enabled.

### What this fixes right now

**Disasters & world**
- Cave-ins no longer happen in games created with the "No Disasters" rule.
- Meteors now follow their intended schedule (roughly every 35–115 hours)
  instead of striking about every 6 hours — and Sensor Towers now genuinely
  delay strikes instead of accidentally making things worse.
- A finished meteor storm no longer switches off your weather forever. The
  game kept treating the storm as "still being predicted" after it ended,
  which silently blocked rains, cold waves, dust storms, some special-project
  rewards and one mystery — for the rest of the colony's life. Colonies
  already affected are healed the moment you load them: if your long-running
  save has mysteriously never seen rain, this is why.
- A meteor storm that stalls mid-run is now detected and wound down, so
  future storms keep coming. One stuck storm used to mean no meteor storm
  would ever be scheduled again on that save.
- Rain that collided with another disaster comes back. If a rain tried to
  start during any other disaster (or even during another disaster's warning),
  that rain type died permanently for the rest of the save — now it simply
  tries again a few sols later.

**Interface**
- The Command Center's resource rows show their numbers again — eleven of them
  rendered as blank space.
- The Domes Overview marks low colonist stats in red again, so you can see at a
  glance which dome is in trouble.

**Buildings & economy**
- You get warned before running out of Food, Machine Parts or Electronics again.
  The calculation behind that warning could only ever produce a value outside the
  range that triggers it, so it had never fired since the remaster.
- A drone that fails to reach a building once no longer ignores it for the rest of
  the game. The game has a five-sol "try again" timer for this, but the failure was
  recorded so far in the future that the timer could never fire — so drones quietly
  stopped servicing buildings that were briefly blocked.
- A Drone Hub Extender losing or regaining power no longer recalls the whole
  hub's fleet. Every flicker of an extender — brownout, malfunction, repair,
  even toggling it yourself — made its hub drop and re-scan everything it
  services, twice, kicking every drone that was en route to anything back to
  Idle. The rebuild is now bundled into a single short deferred pass, so a
  dusty night of power cuts doesn't repeatedly paralyze your logistics.
- Salvaging a farm now removes the oxygen it was giving its dome. Every farm you
  ever removed was still supplying air to that dome forever, and each rebuild
  added another invisible supply on top. Existing phantom oxygen is cleaned out
  of your save when you load it.
- A destroyed tunnel stays destroyed. Loading a save handed every tunnel its
  pathfinding shortcut back without checking whether it was still standing, so
  rovers and colonists kept routing through a ruin until you repaired it. Existing
  saves are corrected the moment you load them.
- Building an artificial lake no longer entombs the RC Constructor that built it,
  along with any drones nearby. The basin is dug after the site clears units out,
  so anything still standing there was sealed under the new terrain and quietly
  ran out of power.
- Starting a landscaping job over a boarding point no longer interrupts the
  colonists boarding there. The sweep that clears units off a new landscaping
  area was supposed to leave anyone mid-boarding alone — the game builds that
  exclusion and then forgets to use it, so boarding colonists were pulled back
  out (sometimes more than once).
- Small landscaping jobs actually get done. A clear, paint or levelling area only
  a few hexes across gave the approaching drone fewer destinations than the game
  unconditionally read back, which errored and dropped whatever the drone was
  doing — so tiny terraforming touch-ups sat there unworked.
- Large Wind Turbines get their Frictionless Composites bonus back. The patch
  migration that was supposed to re-apply that breakthrough to existing saves only
  ever restored it to Shrouded turbines, so a colony that researched it before
  that patch ran its Large turbines unbuffed forever. Repaired when you load.
- Salvaging an upgraded building now removes its dome-wide and colony-wide
  upgrade bonuses. Previously these leaked forever and could be stacked
  infinitely by rebuilding (this silently corrupted long-running colonies).
  Bonuses already leaked into your save are cleaned up when you load it.

**Colonists**
- The **Gene Forging** research does something. The tech promises a higher chance
  of rare traits and defines the bonus, but no part of the game ever read it — only
  its sibling Gene Selection was wired up. Both now add together as the numbers say.
- Dust Sickness does the damage it was designed to do. The code rolls a random
  5-14 Health loss per sol and then throws the roll away, dealing a flat 10 to
  everybody instead.
- Biorobots no longer catch Dust Sickness. The event that hands out the illness
  excluded children and nobody else, so your synthetic colonists lost Health in
  every dust storm — and on the "they shouldn't work" branch were barred from
  working until the cure was researched. Biorobots already suffering from it are
  cured when you load the save.
- Tourist Satisfaction stops sliding downwards. A tourist's stat climbing past two
  thresholds at once only ever collected one bonus, while falling back charged
  both — so satisfaction (and your holiday income) drifted down no matter how well
  you treated them.
- [DRAFT NOTE — F76 (2026-07-27): before release, add a "known vanilla issue we did
  NOT cause" explainer (D02-precedent) for the RC Transport depot resource picker:
  on scaled/wide displays it renders far from the cursor and can't be clicked, so
  "transports won't load from depots" reads as a mod bug and will generate false
  reports. If the wave-6 Fix_ResourcePickerAnchor ships, this becomes its fix
  bullet instead.]
- Housing reserved for a colonist who never turns up is released again. Those
  reservations are invisible in the UI and had no expiry at all, which is why a
  dome could sit half empty and still refuse to house anybody.
- New arrivals no longer set off for a dome they cannot actually reach. When
  nothing walkable was available the game picked the nearest dome by straight-line
  distance and sent them anyway, which is why rocket loads of colonists died on
  the surface. They now wait by the rocket instead, and they no longer disembark
  into ground they cannot walk out of.
- Colonists moving between two nearby domes now use the passage you built. Below
  400m the game never even looked for a passage route and marched them across the
  surface instead — a walk that fits into their oxygen supply only if nothing
  delays them.
- Building a Shuttle Hub actually helps. The game caches its verdict on whether a
  dome is reachable, and that cache never noticed new shuttles — so colonists
  stayed homeless (and seniors stayed put) even after you built the hub that
  would have moved them.
- A dome no longer reads as "full" while its power is out. The free-housing
  figure that births and immigration are gated on counted only residences that
  were running at that instant, while the code that actually moves colonists in
  counted every residence you had switched on — so a power or air dip made a
  dome look full even though homes were being assigned inside it.
- A home that falls vacant is offered to the dome's homeless straight away. The
  game only ever re-checked the homeless when YOU made housing available — built
  a residence, switched one back on. A bed emptied by a death, a retirement or a
  colonist moving out was invisible until each homeless colonist's own periodic
  update came round, which is once every 12 hours in a colony past 3600 people.
- Switching a Shuttle Hub off now actually takes it out of service. A hub you had
  turned off still counted as "shuttle transport available" for the whole colony,
  even though nothing will ever launch a shuttle from a hub that is switched off —
  so colonists queued outside for a ride that was never coming. Suspensions the
  game imposes on itself still count, as before.
- Universities stop training geologists nobody needs. Once Extractor AI lets your
  Metals and Rare Metals Extractors run without colonists, those posts still counted
  as vacancies waiting to be filled — so an "auto" university kept churning out
  geologists for jobs that no longer exist, instead of the specialists you were short of.
- Night-shift workers who were busy at shift start (eating, resting, seeing a
  doctor) now go to work after midnight instead of skipping the rest of their
  shift. Your night-shift buildings were quietly running understaffed.
- Higher tourist star ratings now correctly attract MORE new applicants.
  The chance was inverted — 1-star reviews attracted more colonists than
  5-star ones.

**Trains**
- Trains no longer park at a platform forever. If a passenger stopped being aboard
  mid-journey, unloading hit an internal error and the train sat waiting for
  someone who could never get off, blocking the line.
- Salvaging a single track piece no longer deletes the entire line — and the
  trains assigned to it. Curved sections and short tracks were the worst
  offenders, and salvage is instant with no confirmation.
- Meteor-damaged track can be salvaged again. Damaged pieces were missing a
  piece of internal bookkeeping that made every salvage attempt on that track
  fail silently — including via Ctrl+click and the Salvage button. Tracks
  already damaged in your save are repaired when you load it.
- Salvaging track pays back what the track actually cost. Track is built in
  sections, and the refund only ever counted one of them, so a long line handed
  back the same few Metals as the shortest possible stub. Salvaging part of a
  track returned nothing at all — now those pieces come back as a stockpile
  where they stood.
- A track's train limit follows its real length. It was worked out once, when the
  track was first laid, and never again — so salvaging a long line down to a stub,
  or cutting one in two, left the pieces carrying the original's limit. Existing
  saves are corrected on load.
- Track placed instantly (map setup and similar) is coloured like track rather
  than like pipes. It used to correct itself only if you changed colour scheme.
- Trains respect the resource switches on a station. Unloading ignored them
  completely, so a train would drop Waste Rock at a station you had told not to
  store Waste Rock — and the cargo planner would then send another train to haul
  it back out. The same resource ping-ponged up and down the line forever.
- Demolishing a train station no longer permanently deletes the trains that
  were docked there (or mid-trip from it). They are properly stored and can
  be redeployed — previously your colony's train count silently shrank until
  no station could ever send out a train again.

**Asteroids & rockets**
- Drones can finally deliver to rockets. A landed rocket was cancelling the
  orders of every drone walking towards it, once per game hour, so any trip
  longer than an hour could never finish no matter what priority you set.
- Automatic rockets and asteroid landers no longer take off with nothing
  aboard. They wait for cargo as intended instead of burning fuel on endless
  empty round trips.
- Automatic rockets no longer load cargo and then dump it straight back out.
  Their hourly cargo recalculation used to "forget" whatever was already in the
  hold, so drones spent the day carrying the same resources up and down the ramp.
- An automatic lander fills up with the valuable cargo first. It used to allocate
  its weight limit in alphabetical order, so Concrete, Metals and Polymers took
  the hold before Rare Metals and Exotic Minerals were even considered — and the
  one-sol departure timer shipped whatever had loaded first. It now follows the
  order the flight policy itself lists, valuables first and Waste Rock last.
- Edit Payload remembers what you told it. Any row you emptied was quietly filled
  back in from the flight policy's default cargo list every single time you opened
  the dialog — and since every landing clears the payload, that was every trip. The
  defaults still prefill a payload you have never configured.
- "No available Asteroid Landers" is no longer shown while a lander is standing
  on the pad. The Planetary View asked a stricter question than the lander list
  it was about to open: a lander that had not finished unloading, or was waiting
  for maintenance parts, was refused even though it was free and would have been
  offered in the list.
- Asteroid landers no longer strand themselves. Landing manually made the lander
  treat the fuel reserved for the trip home as surplus and unload it — on an
  asteroid with no drones and no fuel production, that was permanent.
- The First Asteroid message pays out the prefabs it promises, even if you
  saved and reloaded before answering it. That message arrives as a corner
  notification and says you have gained a Micro-G Auto Extractor prefab of each
  type — but if you left it sitting there across a save and a load, opening it
  afterwards granted nothing at all. It is a once-per-game message, so those
  three prefabs were simply gone, with no warning and no second chance. Loading
  such a save now delivers them and re-offers the message to read.
- Asteroid colonists no longer stand around outside until they suffocate. A
  colonist idling in vacuum now heads home before the oxygen runs out — and a
  brief power or air interruption no longer throws every resident out of a
  habitat permanently.
- You hear about it when a Founder gains a trait again. The notification's own
  eligibility check could never come out true, so it never fired once.
- Domes clean up properly when they grow over a building. The building's old
  pipe connections were being torn down against the dome instead of against the
  building, leaving stale plumbing behind that a repair pass re-ran on every
  load.
- Bombardment missiles come in from spread directions instead of arriving as a
  parallel rank. The game was already picking a separate angle for each missile
  and then launching them all along the same one.
- The Underground Medium Dome technology describes the building it unlocks rather
  than naming an unrelated one. Only visible in saves from before the 1.0.6
  underground rework.
- Story steps that collapse a cave can no longer take the whole story with them.
  Eight places in the underground anomaly and Buried Wonder sequences ask for a
  cave-in on the underground map by name rather than on the map they are running
  on, and if that map does not exist — the "No Underground and Asteroids" rule —
  the request errors out and the sequence stops where it stands. It now declines
  quietly and the story continues.
- Drones keep an accurate list of the places they could not reach. Every change to
  the map's passability — a building completed, terrain reshaped, a route opened —
  rebuilt that list in a way that clung to buildings you had already salvaged and
  left its own tally wrong, and the wrong tally is what the drone hub reads when it
  decides whether there is anything worth doing.
- Five more repairs are aimed at other mods and future updates rather than at
  anything you can see today: battery and tank charge-rate modifiers now reach
  the power grid, swapping one researched technology for another keeps the
  research counters straight, two scripting-system helpers do what their own
  descriptions promise, and pre-set building layouts check your research before
  handing you a building.
- Command Center graphs stop lying about consumption. The "Consumed" figure in
  the caption left out maintenance, so Machine Parts and Electronics read as
  almost nothing next to a full-height bar. The caption now counts what the bar
  counts.
- A colonist's Morale tooltip adds up again. It listed a bonus for high Comfort
  that the game deliberately stopped applying, so the effects shown never
  matched the Morale above them. The penalty for LOW Comfort is real and is
  still listed.
- Waiting on a train platform is not charged twice. The wait was counted again
  as riding time — costing extra Comfort on arrival and inflating the travel
  statistics on the train and the track.
- The Last Transmission faction notices your reserves. Six of its opinions —
  power, water and oxygen storage, praise and complaint alike — were attached to
  a field the game never reads, so they scored nothing no matter how well you
  stocked up, while the UI kept listing them as goals to achieve. Its Oxygen
  goal was also measuring Power. Both are fixed.
- "Stored for more than 2 sols" checks look at the whole colony as one figure.
  They used to add each map's reserve up separately, and a map with nothing
  running counted as roughly 41 sols on its own, so once the Underground existed
  those checks were permanently satisfied — and "nothing stored" became
  impossible to reach.
- Tracks connect to stations and tunnels again. When two train buildings sit one
  hex apart, both want the same connector tile — and the game let them delete
  each other's, endlessly, so neither ever held a working connection. Now the
  first one keeps it.
- A train tunnel really does carry power. The tunnel's description promises it
  connects power grids across the map, but a station attached directly to the
  entrance (or to another station a short track away) was skipped by that
  wiring. It now bridges whenever the two ends genuinely sit on separate grids,
  including in saves where the link is already missing.
- RC Transports keep their hands off trade and refugee rockets. The game already
  forbids that, but the rule stopped matching anything when the rocket classes
  were rebuilt for Relaunched, so an RC Transport could be sent to load from or
  unload into a visiting rocket and leave it in a state nothing else understood.

**Story & milestones**
- The Philosopher's Stone mystery no longer gets stuck at the finale. If you left
  its Epilogue popup minimised for more than a sol, the crystal's departure was
  announced while nothing was listening and the mystery never completed.
- A finished Mirror Sphere excavation no longer accepts more work. The lockout
  compared progress against 100 on a scale that runs to four million, so it never
  triggered — and "Pierce the Shell" would happily tie up your drones on a site
  that was already done.
- Completing all milestones no longer breaks in games using the
  No Terraforming or No Politics rules (the completion popup was lost to a
  hidden error).
- St. Elmo's Fire mystery: choosing to free the wisps now produces the power
  the game promised (it produced ~1/1000th of it). Destroying wisps now grants
  exactly the research the notification says (it secretly paid double for some
  wisps and nothing visible for others).

### Fixing your already-broken save

Be aware of what a mod can and cannot do for damage that already happened:

- **Most fixes help immediately.** Anything about ongoing behavior — drones,
  colonists, schedulers, rockets — starts working correctly the moment you
  load your save. A colony that was falling apart should stop deteriorating.
- **Some damage needs active repair, and the pack ships a framework that
  attempts it — but please read this honestly before you count on it.** Every
  time you load, the pack looks for specific damage already sitting in your save
  and tries to undo it: upgrade bonuses left behind by buildings you salvaged
  long ago, Large Wind Turbines that lost their Frictionless Composites bonus to
  a faulty patch migration, phantom oxygen from deleted farms, housing held for
  colonists who never arrived, tunnels destroyed but still routed through,
  Biorobots infected with Dust Sickness, meteor-damaged track that could not be
  salvaged, and mysteries frozen mid-sequence.

  **What we can promise:** every pass is deliberately conservative — it changes
  something only when it can positively identify exactly what went wrong, it
  errs towards doing nothing when unsure, and running it twice does nothing the
  second time. It is built so that failing to help is the normal failure, not
  making things worse.

  **What we cannot promise:** that it will fix *your* save. These repairs are
  aimed at specific, identified damage patterns. A save broken in some other way
  — or broken in a way we have not seen yet — may get no benefit at all, and the
  pack will not tell you it tried and failed. We have deliberately not built
  repairs we could not do safely (one station-track fixup was left out for
  exactly this reason). Consider it a genuine attempt, not a guarantee, and keep
  a backup of an important save before loading it with any mod for the first
  time. **We intend to keep improving this as real broken saves turn up** — if
  one of these repairs helps you, or obviously should have and did not, that
  report is genuinely useful to us.
- **Some history is gone for good.** Colonists who already died stay dead,
  destroyed buildings stay destroyed, expeditions lost to the lander bugs are
  lost. Trains that were voided by the station bug can't be counted or
  restored exactly — but you can build replacement trains at any station for
  Metals + Electronics (a vanilla feature the game never tells you about).

### Compatibility

Built to coexist with other mods. We patch the smallest thing that fixes each
bug, chain politely with other mods' hooks, and every fix checks the game's
code first — if an official patch fixes a bug, our version of the fix
deactivates itself automatically instead of fighting it.

Want to disable a single fix? Every fix has an ID (console:
`SMRFixPack.ListFixes()` shows them and their status). Set
`SMRFixPack_Disabled = { FixIdHere = true }` in the console or in a tiny mod
that loads before this one. **This per-fix switch is PC-only** — it needs the
developer console or a companion mod, neither of which exists on Xbox or
PlayStation. The optional modules are different: their toggles live in
Options → Mod Options and work on every platform, controller included.

### Optional modules (off by default)

Everything above this line is a bug fix and ships on. The modules in this
section are **preferences and features** — they change designed behavior, so
every one of them is **off until you turn it on**, with its own switch in
**Options → Mod Options → Community Fix Pack** (main menu or in-game; works
with a controller). Toggles take effect immediately — no restart needed.
(Modders: the pre-load `SMRFixPack_Optional = { ModuleIdHere = true }` table
still works as an override.)

**Drone stat dials** (`DroneSpeedDial` / `DroneCarryDial`). Two dropdowns on
the same Mod Options page, for colonies where drone logistics can't keep up
(or where the breakthrough lottery never dealt you the drone techs):

- **Drone speed** — 1x (base) / 2x / 3x / 5x. Adds that multiple of base
  drone speed on top of whatever speed techs your save has. Drones only —
  rovers and shuttles are untouched.
- **Drone carry capacity** — +0 (base) / +1 / +2 extra units per trip, on
  top of the base 1; the Artificial Muscles breakthrough still stacks.
- Both take effect immediately, both directions; the base positions are
  exactly vanilla behavior. Honest expectations: these are relief, not a
  cure — in our stress tests, colony-scale repair time was dominated by trip
  count and distances, so faster, bigger drones help but don't change the
  underlying logistics.
- Uninstalling the mod while a dial is active leaves that save with the
  boost permanently (see the savegame note near the top) — set dials back
  to base first.

**Acknowledged warnings** (`AcknowledgedWarnings`). Changes what dismissing a
**"Building Not Working"** warning means: instead of silencing the whole warning
category for a fixed window (after which the same wrecks re-nag — see the
"Looks like a bug, but isn't" section below), dismissal now means *"I've seen
these particular buildings."*

- The buildings listed on the warning you dismiss stay quiet **until they
  actually recover** — a permanently broken building never nags again.
- If an acknowledged building recovers and later breaks again, that's news —
  you'll be warned again.
- A **newly** broken building always warns immediately, even right after you
  dismissed others — the old category-wide quiet window no longer hides it.
- Only the "Building Not Working" warning changes. Every other notification
  keeps its normal behavior.

**Residency control** (`ResidencyControl`). Adds the dome policy the game never
had: **"Closed to new residents"** — stop colonists from moving into a dome
*without* quarantining it. (The accept-colonists toggle is a full quarantine by
design: nobody enters *or leaves*, and story events rely on that. This module
leaves quarantine exactly as it is.)

- A new toggle row on every dome and asteroid habitat infopanel (Ctrl+click
  applies it to all domes at once).
- A closed dome takes no new residents: colonists looking to resettle skip it,
  and new arrivals from rockets and elevators are routed elsewhere.
- Its **current** residents notice nothing: they keep commuting, working,
  shopping and training through passages exactly as before.
- You stay in charge: manually relocating a colonist into a closed dome still
  works, tourists still check into its hotels, and births are unaffected.
- A colonist stranded outside with nowhere else to go will still be let in —
  the policy never suffocates anyone.

**Multiple Artificial Suns** (`MultipleSuns`). The game hard-limits the
Artificial Sun to one per colony. This module lifts that limit — and ships the
repair that makes a second sun actually work. The vanilla game has a real bug
here: solar panels only ever check the *first* sun you built, so panels around
sun #2 would produce as if it weren't there. Players who lift the limit with a
generic "multiple wonders" mod walk straight into that bug; this module fixes
the panel binding at the same time (including panels already dark beside a
second sun in an existing save). With the module off, the game's one-sun limit
applies untouched.

**Drone dispatch overhaul — experimental** (`DroneOverhaul`). In a colony with
overlapping Drone Hub coverage (especially with Hub Extenders), the base game
happily lets a hub on the other side of the map claim a repair that idle
drones are parked right next to — task assignment has no idea of distance
across hubs, first claimant wins, and the near fleet then isn't even allowed
to help. This module makes dispatch care about proximity:

- **Repair and cleaning jobs go to the closest hub's fleet first.** A farther
  fleet only steps in if the near one doesn't respond within a few seconds —
  so a broken-down near fleet never means the job goes undone.
- **Idle drones pitch in next door.** A drone with nothing to do will take a
  nearby repair from a neighboring hub whose own drones are all busy.
- **Your orders always win.** Directly commanding a drone is untouched —
  the module only steers the automatic assignment.
- Deliberately untouched: resource hauling, construction sites (multiple
  fleets swarming a build is good), RC rover fleets, rockets and shuttles.
- It doesn't move drones between hubs — balancing fleet sizes is still your
  call; the module just stops distance-blind claims and lets idle neighbors
  help.
- Marked **experimental** while it's being play-tuned. Turning it off restores
  the game's stock behavior instantly and completely, and saves made with it
  on are unaffected without it.

**Cohort housing — Seniors & Children** (`CohortHousing`). Nurseries and
Retirement Homes never fill on their own: the game only ever relocates a
housed colonist for a strictly better home, so Seniors and Children settled in
normal housing stay put and your cohort buildings sit empty unless you
micromanage trait filters. With this module on:

- Seniors and Children living in normal housing automatically move into free
  Retirement Home / Nursery slots — in their own dome first, then in any
  reachable dome (walk, passage, shuttle, train or elevator, using the game's
  own migration rules).
- When no such slot exists anywhere, they are left completely alone.
- Employed Seniors keep their jobs and are not moved.
- Your manual residence and dome assignments always win; quarantined domes and
  domes closed to new residents (the Residency-control module) are respected;
  tourists are ignored entirely.
- When a Child comes of age, the Nursery slot frees up immediately instead of
  at the next housing shuffle.
- No dome designation needed: put the cohort buildings where you want the
  cohort to live, and the colonists follow. It stores nothing in your save —
  turning it off (or removing the pack) simply stops the moves.

**Classic rocket behavior** (`ClassicRockets`). This one is not a bug fix, and we
want to be completely transparent about what it changes and what the game offers
instead:

- **In the original Surviving Mars,** a rocket parked at your colony took care of
  itself: drones automatically kept it fuelled for launch, and automatically
  loaded it with Rare Metals for export (with a per-rocket switch to say "not
  this one").
- **Relaunched intentionally removed that.** An idle rocket requests nothing —
  fuel arrives only after you pick a destination, and exporting is something you
  set up yourself, either through the payload dialog per trip or through the new
  **Automated Mode**, where you tell each rocket which resources to export and
  above what stockpile level. That is the developers' intended replacement, it
  works, and if you like managing rockets that way you do not want this module.
- **This module restores the original behavior for those who miss it.** It is a
  preference, not a repair — which is why it ships off by default and lives
  apart from the fixes. Currently it restores the refuelling half: a parked
  rocket with no destination keeps its launch fuel requested, so drones top it
  up while it waits. It changes nothing about Automated Mode or the payload
  dialog — rockets you automate behave exactly as Relaunched intends, module on
  or off.
- **One thing to know if you switch it on mid-game:** a rocket that is *already
  sitting parked* at the moment you enable the module will not start refuelling
  right then. It picks the behaviour up the next time it lands. Rockets that
  land after you enable it fill immediately. This is a known limitation and it
  is deliberate — the alternative was poking at rockets mid-flight-cycle, and we
  would rather leave a working system alone than risk breaking it for a few
  seconds of convenience. If it ever bothers you, land the rocket once.

Turn it on in **Options → Mod Options → Community Fix Pack** ("Classic rockets
— refuel while parked"). Off unless you turn it on.

[DRAFT NOTE: the standing Rare Metals export half is DECIDED (user, 2026-07-26:
match the original game exactly — the legacy loader is the spec, see the D01
entry in docs/BUGS.md) but NOT YET WRITTEN. Do not promise it in released text;
when it ships, extend the third bullet with the export half — including the
per-rocket "allow export" toggle — and keep this side-by-side format.]

### Looks like a bug, but isn't: dismissed warnings that come back

You dismiss a **"Building Not Working"** warning. Two minutes later it's back.
Dismiss, return, dismiss, return — it feels exactly like a broken dismiss button,
and it gets reported as one constantly. We investigated it for this pack, expecting
to fix it. Here is what we found:

**Dismissal genuinely works — it's just designed to be temporary.** The game
deliberately silences that warning for a fixed quiet window after you dismiss it,
and then allows it back if the problem still exists. That's a defensible design:
the game refuses to let you *permanently* silence a warning about something that's
still wrong, because a dismissed-forever warning is how you lose a colony to a
problem you forgot about. (An earlier version of the game really did have a bug
here — dismissal did nothing at all — but the developers have already fixed that.
What you see now is the intended behavior.)

**Why it still drives you up the wall:** the design has no answer for a building
that can *never* recover — say, one entombed by a landscaping lake. You've seen the
warning. You can't do anything about it. And it will re-surface every couple of
minutes for the rest of the game, because the game can't tell "unacknowledged
problem" apart from "problem the player has understood and accepted". There's a
second wrinkle, too: the quiet window silences the whole warning *category*, so for
those couple of minutes a **freshly** broken building is also kept quiet — arguably
the opposite of what you'd want.

So: not technically a bug, and this pack only ships bug fixes by default — which is
why you won't find a "fix" for this in the list above. But because the annoyance is
real, the pack carries an **optional module** for it: **Acknowledged warnings**
(`AcknowledgedWarnings`, described in the Optional-modules section above) changes
dismissal to mean "I've seen *these particular buildings*" — the ones you dismissed
stay quiet until they actually recover (if they later break again, that's news and
you'll be told), while newly broken buildings always warn immediately. Off by
default, like every opinion in this pack — turn it on in **Options → Mod
Options → Community Fix Pack**.

### Reporting bugs

Found something broken? Tell us: what happened, roughly when it started, and
whether it survives a save/load. On PC, the game's logs live in
`%AppData%\Surviving Mars Relaunched\logs` (crashes and save failures show up
there), and Ctrl+F1 opens the official bug reporter. A save file where the bug
reliably happens is worth a thousand words. On Xbox and PlayStation there are
no log files or console commands to collect — a plain description (platform,
what happened, when it started, whether it survives a save/load) is still
plenty useful.

### Credits

- **ChoGGi** — whose "Fix Bugs" collection for the original Surviving Mars
  documented dozens of these bug families years before the remaster. All
  fixes here were independently re-verified against the Relaunched code.
- **LukeH** — Martian Express patch research for the original game.
- Everyone reporting bugs on the Paradox forums and Steam discussions —
  many fixes here started as your reports.

[DRAFT NOTE — before publishing: delete draft notes; sync the fix list with
BUGS.md statuses (only `tested` fixes go in the shipped list); add
Workshop/Paradox-appropriate formatting; screenshot of ListFixes() output.
Author name is set (catt144, 2026-07-26).]
