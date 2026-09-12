# Still-needed wording batch — OWNER-RULED text (2026-09-12)

This is the text the public-surface sweep applies. It supersedes the phrasing in
`SURFACE_PLAN.md` (Codex's verbatim proposal, kept unedited as the record) wherever
the two differ. Rulings by the owner, 2026-09-12, in `smr-bugfixpack-d0`:

- **Retire F37 and F43 (with its F118 rider).** The frozen 1.0.7 build (`v5-game-1.0.7`)
  stays exactly as it is.
- **F21 stays.** On 1.1.0 the inflated duration still feeds `AddSpentTime` on the
  train and the track (`Lua/Units/ColonistTransport.lua:671`, `:696-697`), and that
  number is the **"Travel time (rolling average)"** line on every train and track
  info panel (`Lua/XDef/ipTrain.generated.lua:85`, `ipTrack.generated.lua:186`,
  `Lua/Buildings/Track.lua:601`). Only the Comfort charge is gone from `ExitVehicle`
  (no `ChangeComfort` in `:665-700`). The Comfort claim goes; the fix does not.
- **F31 is HELD** for the deep half of `prompts/SURFACE_AUDIT_FABLE.md`. No text
  below is final for it.
- **F52 is HELD** as already ruled (Codex marked it inferred; the row is right).

## ⚖️ Voice rule (owner, 2026-09-12) — binds every public surface from now on

> We are trying to be more dev-friendly, but the public has to understand what we
> are talking about too. Two developers use the fix list; two thousand players and
> rising use the mod. We are not held to a developer's disclosure standard: the
> mod cannot be full of "no guarantees" and "unverified", because that reads as
> no confidence in the product and nobody will want it. If the wording confuses
> the author, it is word salad and it fails.

How to apply it: state scope by saying **what the fix does and for whom**, never by
disclaiming what it does not do. Plain sentences a player would use; precise enough
that a developer reading the row finds the right code. The dated entry in
`agent/bugs/<ID>.md` keeps every limit and caveat; the public row does not carry them.

## The batch — replacement text per item

Line numbers are `content/fix-list.md` in `SMR-CommunityMods` at `a061665`. Only the
lines quoted change; everything else in the row stays.

### 1 · F54 Shuttle hub switched off (`:94`) — approved, polished
- **After the fix:** a hub you switch off stops counting. Only hubs that are on and
  able to fly count.
- (drops the "Suspensions the game imposes on itself — a dust storm, for instance —
  still count as before" sentence; the dust-storm case was never measured)

### 2 · Saint's blessing (`:142`) — approved, polished
- **What you saw:** nothing, which is the problem — the blessing meant for the
  Religious colonists in the Saint's dome had never applied to a single one of them.
- (replaces "the trait's colony-wide effect had never applied to a single colonist")

### 3 · F58 stale reservations (`:105`) — rewritten plain (owner: word salad)
- **Headline:** Beds stayed reserved for colonists who were never going to take them
- **What you saw:** free beds in a dome, homeless colonists outside it, and nothing
  happening. *(unchanged)*
- **What was wrong:** a bed could stay reserved for a colonist who had died, left, or
  moved to another dome, and those reservations are invisible in the interface.
- **After the fix:** reservations held by a colonist who can no longer use the bed are
  released, and stale ones expire. A bed held for a colonist away on an expedition
  is kept for their return.
- **Card, all five copies:** headline bullet "A dome sat half empty and still refused
  to house anyone." → "Beds stayed reserved for colonists who were never going to
  take them."

### 4 · F52 vacuum walks (`:46`) — HELD, no change

### 5 · F21 train wait time (`:398`) — approved; Comfort claim removed, fix stays
- **Headline:** Waiting on the platform was counted again as time on the train
- **What you saw:** the Travel time figure on trains and tracks reading larger than
  the journeys actually were.
- **What was wrong:** *(unchanged)*
- **After the fix:** the ride is timed from boarding, so the platform wait is counted
  once, at the station.
- **Card intro, all five copies:** "a Comfort penalty billed for longer than the
  journey actually took" → "a train travel-time figure that counted the platform
  wait twice".
- Record note for the entry, not the row: on 1.0.7 the same wait also charged
  Comfort; 1.1.0 removed that charge.

### 6 · F34 landscaping vs boarding (`:242`) — approved, polished (factual error: drones, not colonists)
- **Headline:** Starting a landscaping job yanked drones out of the RC Commander they
  were boarding
- **What you saw:** drones pulled back out of an RC Commander they were climbing into
  — sometimes more than once — when you started a landscaping job nearby.
- **After the fix:** the exclusion is used, and boarding drones are left alone.
- In-game registered title: same correction (colonists → drones).

### 7 · F77 extender flapping (`:206`) — approved, polished
- **After the fix:** changes within two seconds of each other are handled as one, so
  a flickering Extender costs the fleet one interruption instead of one per flicker.
- In-game registered title: "Nearby Extender changes share one hub rebuild".

### 8 · F30 lake entombment (`:229`) — rewritten plain (owner: word salad)
- **What was wrong:** the pass that clears units off a construction site skips the
  constructor doing the clearing, and it runs *before* the basin is dug, so anything
  still standing there (including units that had been moved and wandered back) was
  sealed under the new terrain and ran out of power.
- **After the fix:** the moment the basin exists, anything standing in it is sent to
  solid ground nearby, so the rover drives out instead of being sealed in.

### 9 · F06 Philosopher's Stone hang (`:498`) — rewritten plain
- **After the fix:** the departure is re-announced every hour for ten sols, so
  answering the popup any time in that window lets the mystery finish.
- In-game registered title: drop "can no longer hang forever".

### 10 · F50 rocket drone churn (`:219`) — approved, polished
- **What was wrong:** once every game hour the rocket re-issued its work requests,
  cancelling the orders of every drone already walking towards it.
- **After the fix:** requests that have not changed are left alone, so the drones
  arrive.
- (drops "so any trip that took longer than an hour could never finish")

### 11 · F40 Biorobots dust sickness (`:166`) — approved, polished; judgment marker stays
- **After the fix:** Biorobots do not catch it, and Biorobots already suffering from
  it are cured when you load the save. The current game has retired these
  dust-sickness events; the fix stays for saves that still carry the illness.

### 12 · F48 old-track migration pass (`:408`) — rewritten plain (owner: word salad)
- **What was wrong:** one of the game's own repair passes for saves from an earlier
  version was written so that it did nothing. The current game has corrected that,
  but a save that already recorded the repair as done will never run it.
- **After the fix:** the pass runs properly, once, when you load. If the sort fails
  on a track, that track is put back the way it was and the rest carry on.
- **Worth knowing:** keep the first two sentences ("we cannot tell you this fixes a
  symptom you have. It puts your save into the state the game's own migration
  intended, and on our test save it corrected several tracks and stayed corrected.");
  drop the rest, which the new After line now says.

### 13 · F31 cave-in on a missing map (`:561`) — HELD for the deep audit
- If the audit confirms the No Underground route cannot stop a story on either
  branch and nothing player-visible remains: **retire** (row and headline off,
  module out under H-10), and the headline count drops with it.
- If a guard with a real player-visible reach survives: the row is rewritten plain
  after the audit names that reach, and the headline stays or goes on that basis.

### 14 · F73 asteroid vacuum reflex (`:189`) — approved, polished; judgment marker stays
- **After the fix:** a colonist with a home who is idling out in vacuum is sent home
  once half their oxygen is gone.

## Whole-list arithmetic after the batch (derive once, at apply time — never carry)

- Card count word: Forty-nine → **Forty-seven** with F37 + F43 retired; one lower again
  if F31 retires.
- Headlines on the card: 21 → 19 (F37's farm-oxygen line and F31's stopped-story line
  gone) — F31's removal is conditional on item 13; F58's headline keeps its slot with
  the new words.
- "Real defects you cannot see today" count on the card: three → **two** (F57a and
  F29; F43 leaves that set).
- Judgment calls: **three**, unchanged.
- Modules 46 → 44 (45 if F31 also goes); `Code/*.lua` 47 → 45 (44). TestKit probes:
  `GhostFarmOxygen`, `LayoutTechLock` and the already-loose `DomeFreeSpaceMismatch`
  retire with their modules (local kit, not part of the release).
