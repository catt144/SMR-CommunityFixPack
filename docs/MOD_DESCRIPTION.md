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

**Buildings & economy**
- Salvaging an upgraded building now removes its dome-wide and colony-wide
  upgrade bonuses. Previously these leaked forever and could be stacked
  infinitely by rebuilding (this silently corrupted long-running colonies).
- Faction storylines that check your recent export or tourism income
  (Blue Sun, Brazil, Russia) can now actually progress — the income check
  crashed internally on any hour you earned nothing.

**Colonists**
- Night-shift workers who were busy at shift start (eating, resting, seeing a
  doctor) now go to work after midnight instead of skipping the rest of their
  shift. Your night-shift buildings were quietly running understaffed.
- Higher tourist star ratings now correctly attract MORE new applicants.
  The chance was inverted — 1-star reviews attracted more colonists than
  5-star ones.

**Trains**
- Demolishing a train station no longer permanently deletes the trains that
  were docked there (or mid-trip from it). They are properly stored and can
  be redeployed — previously your colony's train count silently shrank until
  no station could ever send out a train again.

**Asteroids & rockets**
- Automatic rockets and asteroid landers no longer take off with nothing
  aboard. They wait for cargo as intended instead of burning fuel on endless
  empty round trips.
- Automatic rockets no longer load cargo and then dump it straight back out.
  Their hourly cargo recalculation used to "forget" whatever was already in the
  hold, so drones spent the day carrying the same resources up and down the ramp.
- Asteroid landers no longer strand themselves. Landing manually made the lander
  treat the fuel reserved for the trip home as surplus and unload it — on an
  asteroid with no drones and no fuel production, that was permanent.

**Story & milestones**
- Completing all milestones no longer breaks in games using the
  No Terraforming or No Politics rules (the completion popup was lost to a
  hidden error).
- St. Elmo's Fire mystery: choosing to free the wisps now produces the power
  the game promised (it produced ~1/1000th of it). Destroying wisps now grants
  exactly the research the notification says (it secretly paid double for some
  wisps and nothing visible for others).

### [DRAFT NOTE] Planned next — move up as they're implemented
- Asteroid landers: payload settings that stick, valuables prioritized over
  waste rock, and "no available landers" no longer shown while a lander sits on
  the pad.
- Asteroid colonists seek shelter before suffocating and can move into
  habitats that had a momentary power blip.
- Track salvage: deleting one hex no longer deletes your entire track (and
  your trains with it); meteor-damaged tracks become salvageable again.
- Colonists: no more suffocating on "short" walks between domes when passages
  exist; homeless colonists find the housing that's actually free (invisible
  stale reservations were eating it); turning off "accept colonists" no longer
  secretly stops your residents from shopping through passages; drones keep
  servicing opened domes; rockets stop yanking their delivery drones away
  every hour.
- The Philosopher's Stone mystery can no longer hang forever at the finale.
- The "Low Storage" warning fires for Food and spare parts (it mathematically
  never could); Command Center resource numbers display again; dome overview
  stat warnings turn red as intended.
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
