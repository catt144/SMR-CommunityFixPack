# Store description — Community Fix Pack: Opt-In Modules (build, release item ③)

**Built 2026-08-13 by `agent/prompts/public-docs/03_BUILD_STORE.md`**, in the
same voice and the same sitting as `STORE_FIXPACK.md`. Design:
`PUBLIC_DOCS_DESIGN.md`. Raw material: `docs/archive/MOD_DESCRIPTION.md`
(FROZEN — its "Optional modules" section is *split out*, never edited) plus the
eight modules' own headers in `C:\Dev\SMR-OptInPack\Code\`.

⛔ **The mod this describes lives in another repo.** This file is the chain's
deliverable and the audit target; **release prep copies the player text into
`C:\Dev\SMR-OptInPack` and into that mod's `metadata.lua`.** Nothing here edits
the other repo.

⛔ **Everything between the two `═══ PLAYER TEXT ═══` rules is player-facing** and
is governed by chain rule 4. `⛔ HOLE` markers are not publishable.

---

═══════════════════════════ PLAYER TEXT — BEGIN ═══════════════════════════

## Community Fix Pack: Opt-In Modules — Surviving Mars: Relaunched

Eight opt-in modules for *Surviving Mars: Relaunched* — every one of them off,
or sitting at the game's own setting, until you turn it on.

**What this is, and why it is a separate mod.** Its companion, the *Community
Fix Pack*, sticks to repairing defects in the game's own code: it carries no
preferences and no features, and where it had to make a judgment call it says so
on its own page. These eight are the other side of that line — they change
designed behaviour because someone wanted them to. Keeping them out of the fix
pack is what lets that mod stay a bug-fix mod, and it is what lets this one
offer things the developers deliberately decided against. *(One of the eight
also carries a real repair, because lifting a limit the game set walks you into
a defect the game never had to handle. It is described below.)*

- **You do not need the fix pack for this, and it does not need you.** Each mod
  works on its own, and they work together. We ran both ways round and measured
  it: this mod with the fix pack uninstalled, and the fix pack with this one
  uninstalled.
- **Everything is off until you switch it on.** Seven modules ship off. The two
  drone dials ship at the game's own values, where they do exactly nothing —
  they are settings, not switches, and their base positions are ordinary vanilla
  behaviour.
- **The switches are in the game, on every platform.** *Options → Mod Options →
  Community Fix Pack: Opt-In Modules*, from the main menu or in game, and they
  work with a controller. Toggles take effect as soon as you press Apply, in
  both directions — no restart needed. *(Turning the whole mod itself on or off
  in the mod manager is different: that takes effect after you restart the
  game.)*
- **Nothing is patched on disk.** The mod wraps the game's own code while it
  runs, and no game files are modified.
- **Your existing save is fine.** Turning a module off puts the game's own
  behaviour back. What a module has already done stays done — a colonist one of
  the housing modules moved lives where it moved them — but it stops doing more. What these modules store in your save is four small things: a
  "you have seen this warning" mark on a building, a "closed to new residents"
  flag on a dome, a "move jobseekers out" flag on a dome, and — only if you move
  a drone dial off its base setting — an ordinary bonus of the kind the game
  hands out itself. The first three mean nothing to the unmodded game. **The
  fourth is the one caveat on this page and it has its own paragraph below.**

**Playing on Xbox, PlayStation or the Microsoft Store version?** One rule that
applies to every mod rather than to this one: **while any mod is enabled, the
game does not unlock achievements on Xbox, PlayStation or the Microsoft Store.**
Steam and other PC versions are not affected.

### The modules

**Drone stat dials.** Two dropdowns on the Mod Options page, for colonies where
drone logistics cannot keep up — or where the breakthrough lottery never dealt
you the drone techs.

- **Drone speed** — 1x (base) / 2x / 3x / 5x. The label is the total: 2x adds
  one more helping of the drone's base speed on top of whatever speed techs your
  save already has, 3x adds two, 5x adds four. Drones only; rovers and shuttles
  are untouched.
- **Drone carry capacity** — +0 (base) / +1 / +2 extra units per trip on top of
  the base 1. The Artificial Muscles breakthrough still stacks.
- Both take effect as soon as you press Apply, in both directions, and the base
  positions are exactly the unmodded game. Honest expectations: this is relief
  rather than a cure. Most of a colony's drone time goes on hauling resources
  about, so faster, roomier drones help without changing what is underneath.
- ⚠️ **Set both dials back to base (press Apply) and save before you
  uninstall.** A dial that
  is not at base is stored in your save as an ordinary bonus, and it goes on
  boosting your drones after the mod is gone — permanently, with nothing left in
  the game to say where it came from. Setting the dials to base clears it from
  the colony you are playing; **saving is what clears it from the file.**

**Acknowledged warnings.** Changes what dismissing a **"Building Not Working"**
warning means. The game silences that warning for a fixed quiet window and then
lets it back if the problem is still there — which is a defensible design, and
not a broken dismiss button. It has no answer for a building that can never
recover, though: an unfixable wreck re-nags for the rest of the game. With this
on, dismissal means *"I have seen these particular buildings"*.

- The buildings listed on the warning you dismiss stay quiet **until they
  actually recover** — a permanently broken building never nags again.
- If an acknowledged building recovers and later breaks again, that is news, and
  you are warned again.
- A **newly** broken building always warns immediately, even right after you
  dismissed others. The old category-wide quiet window used to hide it.
- Only the "Building Not Working" warning changes. Every other notification
  keeps its normal behaviour.

**Residency control.** Adds the dome policy the game never had: **"Closed to new
residents"** — stop colonists moving into a dome *without* quarantining it. (The
accept-colonists toggle is a full quarantine by design: nobody enters *or*
leaves, and story events rely on that. This module leaves quarantine exactly as
it is.)

- A new toggle row on every dome and asteroid habitat infopanel. Ctrl+click
  applies it to every dome at once, and on a controller the row names the button
  that does the same.
- A closed dome takes no new residents: colonists looking to resettle skip it,
  and new arrivals from rockets and landers are routed elsewhere.
- Its **current** residents notice nothing — they keep commuting, working,
  shopping and training through passages exactly as before.
- You stay in charge: manually relocating a colonist into a closed dome still
  works, tourists still check into its hotels, and births are unaffected.
- A colonist stranded outside with nowhere else to go is still let in — the
  policy is built so that it is never the reason someone is left out there.

**Multiple Artificial Suns.** The game hard-limits the Artificial Sun to one per
colony. This module lifts that limit — and ships the repair that makes a second
sun actually work. There is a real defect in the game here: a solar panel built
near a second sun never connects to it, so those panels produce as if the sun
were not there — which is why lifting the limit without repairing the
binding is not worth doing. This module fixes the panel binding at the same
time, including panels already sitting dark beside a second sun in an existing
save. With the module off, the game's one-sun limit governs what you build from
then on, and suns you have already built are ordinary buildings that keep
working either way.

⚠️ **One thing if you switch it on mid-game:** panels that were already
standing keep ignoring a second sun until you save and load. Panels built after
you switch it on bind straight away, and a reload snaps the older ones into
place.

**Drone dispatch overhaul — experimental.** In a colony with overlapping Drone
Hub coverage, and especially with Hub Extenders, the game happily lets a hub on
the other side of the map claim a repair that idle drones are parked next to:
task assignment knows nothing about distance across hubs, the first claimant
wins, and the near fleet is not even allowed to help. This module makes dispatch
care about proximity.

- **Repair and cleaning jobs go to the closest hub's fleet first.** A farther
  fleet steps in if the near one does not respond within a few seconds, so a
  broken-down near fleet never means the job goes undone.
- Honest note from our own measurements: most repairs that need parts are
  decided by which hub delivers them — a hand-off this module deliberately
  leaves alone — so the change matters most for repairs and cleaning that
  need no resources.
- **Idle drones pitch in next door.** A drone with nothing to do takes a nearby
  repair from a neighbouring hub whose own drones are all busy.
- **Your orders always win.** Directly commanding a drone is untouched — the
  module only steers automatic assignment.
- Deliberately untouched: resource hauling, construction sites (several fleets
  swarming a build is good), rover fleets, rockets and shuttles.
- It does not move drones between hubs. Balancing fleet sizes is still your
  call; the module stops distance-blind claims and lets idle neighbours help.
- Marked **experimental** while it is being play-tuned. Turning it off hands
  dispatch straight back to the game's own behaviour, and saves made with it on
  load without the mod.

**Cohort housing — Seniors & Children.** Nurseries and Retirement Homes never
fill on their own: the game only ever relocates a housed colonist for a strictly
better home, so Seniors and Children settled in ordinary housing stay put and
your cohort buildings sit empty unless you micromanage trait filters. With this
on:

- Seniors and Children living in ordinary housing move into free Retirement Home
  and Nursery slots — their own dome first, then any reachable dome, using the
  game's own migration rules (walk, passage, shuttle, train or elevator).
- When no such slot exists anywhere, they are left completely alone.
- Employed Seniors keep their jobs and are not moved.
- Your manual dome assignments always win, and pinning a colonist to a
  particular home stops them being re-housed inside their own dome. It does not
  pin them to that dome: a pinned Senior whose dome has no free cohort slot can
  still move to one that has. Quarantined domes and domes closed to new
  residents are respected; tourists are ignored entirely.
- When a Child comes of age the Nursery slot frees up immediately, instead of at
  the next housing shuffle.
- No dome designation needed: put the cohort buildings where you want the cohort
  to live and the colonists follow. It stores nothing at all in your save —
  turning it off simply stops the moves.

**Nursery / Retirement Dome policy.** For the dome you dedicate to Children or
Seniors. That dome keeps only enough ordinary housing to staff its services — so
unhoused jobseekers drift in and pile up, and once it holds enough homeless the
game counts it as overcrowded and **stops sending it anyone at all**, including
the Children or Seniors it was built for. It quietly stops doing its job.

- A new toggle row on every dome and asteroid habitat infopanel that has a
  Nursery or Retirement Home (Ctrl+click, or the button the row names on a
  controller, applies it to every such dome at once). The row shows what it
  will do *before* you click it — *"Nursery / Retirement Dome (3 would move)"*
  becomes *"(3 moving out)"*.
- When it is on, **unemployed** colonists with no home in that dome move to the
  nearest dome with housing they can use, using the game's own migration rules —
  unless that dome still has a job standing open that one of them could take, in
  which case nobody is moved out, because staffing the place is the point.
- **Colonists who work there stay.** They are who that dome's ordinary housing
  exists for, and moving them out is how you break its services.
- **Seniors and Children stay, even while homeless.** That is not an oversight:
  a homeless Senior in your Retirement Dome is the game telling you to build
  more Retirement Homes, and hiding that from you would not help you. *(The one
  exception follows the game's own rules: in a colony where Seniors can work —
  the Forever Young / "Put Them To Work" unlocks — an unemployed Senior counts
  as a jobseeker like anyone else and can be moved.)*
- **Nobody is ever put outside.** If there is nowhere suitable to send someone
  they simply stay. A quarantined dome still releases no one, and your manual
  dome assignments always win.
- Two domes with the policy on never trade the same colonist back and forth.
- It composes with **Residency control**: a dome can refuse newcomers and move
  jobseekers out at the same time, which is exactly what a nursery dome wants.
- ⚠️ One thing to watch if you put a Hotel in that dome: leave it on "Tourists
  Only". Switched to "Any Colonist" a Hotel stops being tourist housing and
  becomes ordinary housing, so arriving jobseekers get a *room* — which means
  they are not homeless, which means this policy will not move them out.

**Classic rocket behaviour.** This one is not a repair, and we want to be
completely transparent about what it changes and what the game offers instead.

- **In the original *Surviving Mars*,** a rocket parked at your colony looked
  after itself: drones automatically kept it fuelled for launch.
- **Relaunched intentionally removed that.** An idle rocket requests nothing —
  fuel arrives after you pick a destination, and exporting is something you set
  up yourself, through the payload dialog per trip or through the new
  **Automated Mode**, where you tell each rocket which resources to export and
  above what stockpile level. That is the developers' intended replacement, it
  works, and if you like managing rockets that way you do not want this module.
- **This module restores the refuelling half of the old behaviour** for those
  who miss it. A parked rocket with no destination keeps its launch fuel
  requested, so drones top it up while it waits. It changes nothing about
  Automated Mode or the payload dialog — rockets you automate behave exactly as
  Relaunched intends, module on or off.
- **One thing to know if you switch it on mid-game:** a rocket that is *already*
  sitting parked will not start refuelling right then; it picks the behaviour up
  the next time it lands. Rockets that land after you enable it fill
  immediately. That is deliberate — the alternative was poking at rockets
  mid-flight-cycle, and we would rather leave a working system alone than risk
  breaking it for a few seconds of convenience. If it bothers you, land the
  rocket once.

### Your save, and removing the mod

Turning a module off puts the game's own behaviour back, and a save made with a
module on loads without the mod. Remove the mod and the marks it left — the
acknowledged-warning stamps and the two dome policy flags — sit there unread;
the unmodded game has no idea they exist. What a module already did to your
colony stays done: colonists a housing module moved do not move back.

⚠️ **The one exception, and it is worth thirty seconds of your time: the drone
dials.** A dial that is not at its base position is stored in your save as an
ordinary bonus of the kind the game hands out itself, and it goes on boosting
your drones after the mod is gone. Two steps avoid that: **set both dials back
to base and press Apply, then save the game** — and then uninstall. Setting them to base clears
the boost from the colony you are playing; the file on disk only loses it when
you write a new save. ⛔ HOLE — [the rescue tool, for anyone who uninstalled
already; see notes, hole 1].

One more thing you will see, and it is not ours: the first time you load a save
that was made with any mod you have since removed, the game itself prints a
notice that the save refers to a mod that is not there. It disappears as soon as
you save again.

### Other mods, and the game version

Built to coexist. Each module wraps the smallest thing it needs, chains politely
with other mods' hooks, and checks the game's code before it changes anything —
if the game stops looking the way a module expects, that module stands down
rather than guessing. Built against game version 1.0.7.396349.

### Reporting a bug

Tell us what happened, roughly when it started, which modules you had on, and
whether it survives a save and reload. A save file where it reliably happens is
worth a thousand words. On PC the game's logs are usually in your
`%AppData%\Surviving Mars Relaunched\logs` folder, and Ctrl+F1 opens the
official bug reporter (on Steam Deck the game leaves that one out). On Xbox and
PlayStation there are no logs to collect, and a plain description is still
genuinely useful.

═══════════════════════════ PLAYER TEXT — END ═══════════════════════════

---

## Notes — what is deliberate, what is a hole

### The holes

| # | hole | who closes it |
|---|---|---|
| 1 | **The rescue tool** — name, link, publish status | release-time owner call, checklist 17 ("build ≠ publish") |
| 2 | **Store link** to the fix pack, and the site link | neither exists until upload / until Pages is on |

### Deliberate calls

1. **"Eight modules, seven off and two dials at base"** is stated as *off or at
   the game's own setting*, never as a flat "all eight are off". `DroneStatDials`
   registers **without** `optional`, is active-at-base by design, and the opt-in
   repo's own STATE says so (`1 default-active`). A flat "all off" would be
   false in the one place a player can check it.
2. **The uninstall caveat is given its own paragraph, twice** — in the dials
   block and in the removal section. It is the only genuinely harmful residue in
   either mod (`D13_EXPOSED_SET.md` §2b D15), and burying it once would be the
   omission the whole surface design exists to prevent.
3. **The Retirement-Dome hotel wrinkle is one bullet, not the essay.** §6.1 files
   it as an FAQ question; it stays here in short form because it decides whether
   *this module* does its job, and the essay goes to the site.
4. **The "dismissed warnings come back" essay is compressed to three sentences**
   inside the module block for the same reason, with the full version routed to
   the FAQ.
5. **The Rare Metals auto-export half is not promised.** It is decided but not
   written (frozen file's own draft note); only the refuelling half ships, and
   only the refuelling half is described.
6. **"Experimental" is kept on the drone dispatch overhaul.** Its playtest is
   frozen (PT-52), and dropping the word to make the page read better would be
   exactly the kind of quiet upgrade rule 6 forbids.
7. **No count of anything**, per §4.4 — "eight modules" is the product's shape,
   not an achievement count, and it is checkable on the Mod Options page.

### What this text asserts, and where each assertion comes from

| claim | source |
|---|---|
| both mods stand alone, measured both directions | opt-in `STATE.md` — 9 launches 2026-08-12, this mod at `8/8` with the fix pack uninstalled, the fix pack at `74/74` with this one uninstalled; audit-sustained |
| toggles take effect immediately, both directions | all eight module headers state the mechanism (per-call `IsActive`; `Opt_MultipleSuns` uses `on_activate`/`on_deactivate`); design `PUBLIC_DOCS_DESIGN.md` §12 hole 4, CLOSED by the chain QA. ⚠️ **SOURCE-VERIFIED, not play-verified** — the combined sitting measures one flip |
| mod enable/disable needs a full game restart | D13 / fix-pack `STATE.md` |
| save footprint: three inert flags + the dial bonus | `D13_EXPOSED_SET.md` §2b rows D12–D15; §2c "the whole opt pack has no game-time thread and no GameVar" |
| the dial boost survives uninstall permanently | §2b D15, MEASURED; the module's own header says so |
| cohort housing stores nothing | `Opt_CohortHousing.lua` header — "zero persisted state" |
| the engine's mod-reference notice, self-clearing | `D13_EXPOSED_SET.md` §10.9(4) as corrected by measurement |
| Mod Options page exists and is controller-friendly | `D05` (`tested`); the split verification read the page at `1/8` on fresh defaults |
| second-sun panel binding is a real vanilla defect | `F39` (folded into this module) + `D04`; module header cites the build-once enforcement |
| the four-game-hour re-nag window is designed behaviour | `D02` (`tested`), measured live in PT-38 |
| specialist domes strand homeless colonists | `D12` — observed in play 2026-07-30 (68 free Child slots, 28 homeless), vanilla tie re-verified against the pinned build 2026-08-02 |
| the display name | owner decision 2026-08-13, swept `e17586b` |
| achievements on Xbox / PlayStation / Microsoft Store | `Achievement.lua:61-63`, consumed `:77`; `FIX_POLICY.md` §7 for the no-logs half |
| the Hotel "Tourists Only" wrinkle | `Opt_NoHomeless.lua:289-312` (citing `Hotel.lua:6-27`, `Residence.lua:462-466`) — ⚠️ **NOT** the frozen file, which is the design report's only citation for it |
| drone dial arithmetic (2x adds one more helping of base) | `D09` PT-56, measured `1728 → 3168` = +1440 = one× base; module header "+(N-1)×100% of BASE" |
| the free-work door (a dome with an open job holds its jobseekers) | `D12` — logic proven at the wrapper; ⚠️ **P14 unmeasured in play**, so the page states the rule, not an outcome |
| pinning a home does not pin the dome | `D07` — in-dome pass checks forced residence, cross-dome pass checks forced dome only; owner-ruled 2026-08-11 |
| second-sun panels bind on reload, not on a mid-session flip | `D04` PT-55 — the entry itself says this is "worth saying in player-facing text" |
| hauling dominates drone time | `D06` B2 — hauling 3h03m of a 3h27m leg. ⚠️ The **distance** reading from that leg was WITHDRAWN, so the page claims hauling only |
| game version 1.0.7.396349 | `EF-014` |

### Owed elsewhere

* The player text above is copied into `C:\Dev\SMR-OptInPack` at release prep,
  and its `metadata.lua` `description` / `short_description` replaced with the
  strings drafted in `STORE_METADATA_STRINGS.md`.
* ⚠️ `Opt_DroneOverhaul.lua`'s header still names the old *"Options → Mod
  Options → Community Fix Pack"* path (the display-name sweep missed a wrapped
  line). Code comment, other repo, harmless to players — routed, not fixed here.
