# Release description — Community Fix Pack: Opt-In Modules (the file the owner pastes from at ④)

**Assembled 2026-08-14 by `agent/prompts/release-3/01_BUILD_DESCRIPTIONS.md`.**
Supersedes `docs/archive/MOD_DESCRIPTION.md`'s "Optional modules" section for
this product; nothing was carried across from that frozen file.

⭐ **The player text below is VERBATIM from `STORE_OPTIN.md`'s audited block**
(built 2026-08-13, same sitting and same sweeps as the fix-pack card, terminal
audit 2026-08-14). Nothing was re-authored. What is added: the holes rendered as
`>>> FILL-IN <<<` markers, and the instruction for each beside it below.

⛔ **The mod itself lives in `C:\Dev\SMR-OptInPack`.** This file is the paste
source; its `metadata.lua` strings are a separate, already-applied thing (see the
portal-prep sheet). ⛔ **Not published. Rule 5.**

---

## Before you paste — the three fill-ins

| n | where | needs | if it does not exist yet |
|---|---|---|---|
| **1** | "You do not need the fix pack for this" bullet | **store link** to the *Community Fix Pack* | delete the marker line — the sentence names the mod already |
| **2** | end of "Your save, and removing the mod", right after the drone-dial warning | ⛔ **the Save Rescue sentence — GATED on checklist 17** | ⛔ **delete the marker line.** This is the default and it is safe: the paragraph above it already tells the reader the two steps that avoid the problem entirely |
| **3** | end of the "Acknowledged warnings" block | *optional* site link to the FAQ's fuller answer | delete the marker line. It is an offer of more detail, nothing depends on it |

### FILL-IN 2 — the one that is a decision, not a link

⛔ **Do not fill this in unless Save Rescue is actually published.** A page that
names a tool nobody can download is a broken promise, and that is the standing
ruling (`PUBLIC_DOCS_DESIGN.md` §8: *name no tool*). What has changed since that
ruling was written, and what has not:

* ✅ **The tool exists and works.** Built 2026-08-13, verified in a running game,
  and **`tested` 2026-08-14** at the owner's own keyboard — on a save that came
  by its leftovers honestly it removed 1566 entries by name, kept the repair it
  is meant to keep, and a save it had cleaned reloaded silently (`D13.md`).
* ✅ **The name is ratified** — *Save Rescue* (owner, 2026-08-13; it is the
  `title` in that mod's `metadata.lua`).
* ⛔ **Publishing is still your call and still unmade** — checklist 17 recorded
  "build ≠ publish" in the same breath as approving the shape.

**If you publish it, this is the sentence** (drafted here, not card text — it was
put through the shipped-module control at assembly, see Provenance):

> If you have already uninstalled without doing that, there is a separate
> one-shot tool — **Save Rescue**. Install it, load the save once, read what it
> tells you it removed, save, and delete it again.

…followed by its store link once that link exists.

### FILL-IN 1 and 3 — the links

**Store link (1)** does not exist until the fix pack is uploaded. **Site link
(3)** does not exist until Pages is switched on — the site is built and
terminal-audited but the publish workflow is `workflow_dispatch`-only and Pages
is OFF. When it is on, the page this marker wants is `content/faq.md`'s section
*"I dismissed a 'Building Not Working' warning and it came back"*, at
`faq/#i-dismissed-a-building-not-working-warning-and-it-came-back`, under the
site root **that GitHub prints on the Pages settings screen — copy it from there
rather than typing it**.

ℹ️ A second site link would fit the Retirement-Dome hotel wrinkle
(`faq/#my-retirement-domes-hotel-is-filling-up-with-jobseekers`, verified to
exist). No marker is placed for it: one link per page is enough, and a second is
a second thing to break.

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
>>> FILL-IN 1 — store link to the Community Fix Pack, or DELETE THIS LINE <<<
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
>>> FILL-IN 3 — optional site link to the fuller answer, or DELETE THIS LINE <<<

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
you write a new save.
>>> FILL-IN 2 — the Save Rescue sentence, ONLY if you publish it; otherwise DELETE THIS LINE <<<

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

## Provenance, and the counts re-emitted at assembly time

The claim-by-claim source table is `STORE_OPTIN.md`'s own and is not duplicated
here. **Counts re-emitted at assembly (rule 3):**

| count in the text | re-emitted | source |
|---|---|---|
| "**Eight** opt-in modules" · "**Seven** modules ship off" · "the **two** drone dials … at the game's own values" | `python tools/doccheck.py --emit-counts` in `C:\Dev\SMR-OptInPack`, 2026-08-14: **8 registered modules, 1 default-active, 7 optional-gated** | the emitter, this session |
| "game version **1.0.7.396349**" | `EF-014`; STATE's pinned build line | the fact |

⭐ The emitted `1 default-active / 7 optional` is exactly why the card says *off
**or at the game's own setting*** rather than a flat "all eight are off": the
dials module registers without `optional` and is active-at-base by design. A flat
"all off" would be false in the one place a player can check it (deliberate call
1 on the card).

### The shipped-module control on the ONE non-card sentence

The Save Rescue sentence in FILL-IN 2 is **not** card text, so it was put through
*"which shipped module delivers this?"* at assembly. ⚠️ **Prompt 2 re-runs this
regardless, and should — this is the exact class of sentence that inherits a
page's defects.**

| clause | delivered by | evidence |
|---|---|---|
| "a separate one-shot tool — **Save Rescue**" | mod `SMR_CommunitySaveRescue`, `Code/00_Core.lua` + `Code/10_SaveRescue.lua`, both in `metadata.lua`'s `code` list | the shipped tree; `title` is "Save Rescue", owner-ratified 2026-08-13 |
| "load the save once" and it acts | the automatic `OnMsg.PostLoadGame` pass | witnessed 2026-08-14: `removed 1566` by name, matching a prediction committed beforehand (`D13.md`) |
| "read what it tells you it removed" | `report_text()` shown by `WaitMessage` | the report dialog was **witnessed raising** with matching text, 2026-08-14 |
| "delete it again" | it persists nothing of its own | residue-zero MEASURED — 0 artifact-namespace names over 4510 objects, `UIColony`, every rains entry and all 440 `PersistableGlobals` (`D13_VERIFICATION.md`) |

⚠️ The sentence deliberately does **not** say the reader will see nothing after
deleting it: they will see the engine's one mod-reference notice, exactly as the
paragraph three lines below already explains for any removed mod
(`D13_EXPOSED_SET.md` §10.9(4), corrected by measurement).

**Terminal audit, 2026-08-14 (prompt 2):** the firewalled re-run of this control
made two changes. ⛔ **"save," added to the sentence** — the pass edits the
loaded colony and only the player's next save writes the cleaned state into the
file; "load once … delete it again" without a save loses the cleanup (full
reasoning: `RELEASE_DESCRIPTION_RESCUE.md`, audit section). ⚖️ And the
engine-notice premise in the paragraph above is now **routed as checklist item
29**: the measured line is a log write, and the on-screen missing-mods warning
excludes `optional_mod` mods — which all three of ours are — so the card
paragraph it leans on promises a notice the game does not show. Left as-written
pending that one ruling, because the same sentence sits on both audited cards
and the site.

### What changed between `STORE_OPTIN.md` and this file

**Nothing in any sentence.** Three `>>> FILL-IN <<<` marker lines placed — one
replacing the card's `⛔ HOLE` notation in place (number 2), two newly placed at
the store-link and site-link points the card's notes enumerate as hole 2 but
never marked in the text.

### Routed, not fixed here

⚠️ `Opt_DroneOverhaul.lua`'s header comment in the other repo still names the old
*"Options → Mod Options → Community Fix Pack"* path — the display-name sweep
missed a wrapped line. Code comment, never shipped to a player (`docs/` and
comments are not the Mod Options page), carried forward from `STORE_OPTIN.md`'s
own note. Still open.
