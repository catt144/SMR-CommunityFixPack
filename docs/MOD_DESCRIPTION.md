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

**Works with your existing saves. Safe to add or remove at any time.** The mod
stores nothing in your savegame — removing it simply lets the original bugs
come back.

### What this fixes right now

**Disasters & world**
- Cave-ins no longer happen in games created with the "No Disasters" rule.
- Meteors now follow their intended schedule (roughly every 35–115 hours)
  instead of striking about every 6 hours — and Sensor Towers now genuinely
  delay strikes instead of accidentally making things worse.

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
- A second Artificial Sun works. Panels only ever checked the *first* one you
  built, so everything you put up around sun number two produced as if the sun
  were not there. Panels in an existing save are reconnected when you load it.
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
- **Some damage needs active repair, which this pack includes.** Every time you
  load, the pack looks for damage that is already sitting in your save and undoes
  it: upgrade bonuses left behind by buildings you salvaged long ago, Large Wind
  Turbines that lost their Frictionless Composites bonus to a faulty patch
  migration, phantom oxygen from deleted farms, housing held for colonists who
  never arrived, tunnels destroyed but still routed through, solar panels beside a
  second Artificial Sun, Biorobots infected with Dust Sickness, meteor-damaged
  track that could not be salvaged, and mysteries frozen mid-sequence. Each pass
  is conservative — it changes something only when it can positively identify what
  went wrong — and re-running it does nothing.
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
that loads before this one.

### Optional module (off by default)

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

Turn it on with `SMRFixPack_Optional = { ClassicRockets = true }` in the console
or in a tiny mod that loads before this one. Off unless you turn it on.

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
real, we're building an **optional module** that changes dismissal to mean "I've
seen *these particular buildings*": the ones you dismissed stay quiet until they
actually recover (if they later break again, that's news and you'll be told), while
newly broken buildings always warn immediately. Off by default, like every opinion
in this pack.

[DRAFT NOTE: the AcknowledgedWarnings module is NOT written yet — see the D02
entry in docs/BUGS.md, gated on PT-38. When it ships, add its opt-in instructions
(`SMRFixPack_Optional`) to this section and to the Optional-modules section above.
Until then this section must promise only that it is planned.]

### Reporting bugs

Found something broken? Tell us: what happened, roughly when it started, and
whether it survives a save/load. For crashes and save failures, the game's
logs live in `%AppData%\Surviving Mars Relaunched\logs`, and Ctrl+F1 opens the
official bug reporter. A save file where the bug reliably happens is worth a
thousand words.

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
