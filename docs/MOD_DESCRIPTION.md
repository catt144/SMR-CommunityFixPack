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
- A second Artificial Sun works. Panels only ever checked the *first* one you
  built, so everything you put up around sun number two produced as if the sun
  were not there. Panels in an existing save are reconnected when you load it.
- Salvaging an upgraded building now removes its dome-wide and colony-wide
  upgrade bonuses. Previously these leaked forever and could be stacked
  infinitely by rebuilding (this silently corrupted long-running colonies).
- Faction storylines that check your recent export or tourism income
  (Blue Sun, Brazil, Russia) can now actually progress — the income check
  crashed internally on any hour you earned nothing.

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
- Turning off "accept colonists" on a dome no longer stops its own residents from
  shopping, working and studying in the domes next door. That switch is the
  migration policy — whether outsiders may move in — but it was also being used to
  decide whether your own residents were allowed to leave through a passage.
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

### [DRAFT NOTE] Planned next — move up as they're implemented
- A save-repair pass (see below).

### Fixing your already-broken save

Be aware of what a mod can and cannot do for damage that already happened:

- **Most fixes help immediately.** Anything about ongoing behavior — drones,
  colonists, schedulers, rockets — starts working correctly the moment you
  load your save. A colony that was falling apart should stop deteriorating.
- **Some damage needs active repair, which this pack includes.** [DRAFT NOTE:
  reword when sanitizer ships] Leaked upgrade bonuses already baked into your
  save, phantom oxygen from long-deleted farms, invisible housing
  reservations, mysteries frozen mid-sequence — the pack's save-repair pass
  detects and cleans these on load.
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

**Classic rocket behavior** [DRAFT NOTE: implement as D01]: the remaster
intentionally changed rockets to not auto-refuel or auto-load Rare Metals
while idle — that's a design decision, not a bug, so it's not part of the
standard pack. This optional module restores the original game's behavior for
players who want it. Off unless you turn it on.

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

[DRAFT NOTE — before publishing: delete draft notes; fill author name; sync
the fix list with BUGS.md statuses (only `tested` fixes go in the shipped
list); add Workshop/Paradox-appropriate formatting; screenshot of
ListFixes() output.]
