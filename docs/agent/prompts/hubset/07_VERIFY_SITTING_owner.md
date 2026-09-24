# hubset 07: verify every member in the game (attended, the chain's one sitting)

Chain rules: [README.md](README.md). Read them, then `## Notes from upstream` below, first.
**Attended:** the owner clicks preloaded SMRTK slots; the session relays, reads the log and records.
Fire only after 06 has closed. Owner ruling 2026-09-24: **"One sitting only."**

**Owner time: about 30 minutes (an estimate, not measured):** segment A 13, segment B 12, relaying
words 5. If it runs long, drop in this order: the mid-spoke leg (A6 and B6), then the relocation
subject (A3b and B3b).

**Scope (owner, 2026-09-24):** "anything that was a minor addon that isn't what this chain was
created for are desk verified only." "We are doing the bare minimal testing in game needed to ship
these new fixes." **C42, F127 and P3 get no reading in this sitting.** Records the slots still log for
them (`boot_c42stale`, `p9`, `boot_f127`) are not verdicts and are not reported. Two boots, because a pack module cannot be switched off while the
game runs. `SMRFixPack_Disabled` is read only before load (`Code/00_Core.lua`, header). So "fix off"
is segment A on `main` and "fix on" is segment B on `hubset`.

## Authority and outcome

Run the script link 06 appended below, exactly as written. End state:

- an archived log per run segment;
- a verdict against every prediction;
- each member's entry updated on `main` with what the owner watched (`tested-attended` only where the
  owner watched the fix work);
- the junction restored to the main tree and read back;
- 99's inbox holding every verdict and every drift from the script.

## Before the owner sits (this session, with the game closed)

You are the second seat on 06's script. Check it from the owner's chair before asking them to
start. If a check fails, stop and route it to the owner; do not start the sitting.

- **Clicks only.** Every owner step is a slot, trigger or panel button. Any typed line carries 06's
  stated reason. No step asks the owner to wait in real time or to watch for a state among many
  objects.
- **The slots are in place.** The TestKit HEAD and slot labels match 06's outbox. Re-run
  [tools/SMRTK.md](../../../../tools/SMRTK.md)'s "Gates" commands and require their stated results.
- **The predictions can fail.** Each prediction names its refuting result, and 06's rehearsal shows
  a scratch variant producing it.
- **The price holds.** The owner-minute total at the top of the script is the one you will quote.

Then give the owner one line: *"start the game; the Slots & notes tab is loaded"*, plus the save to
load.

## Rules for the sitting

- Relay the owner's words into the log as they are spoken (`docs/agent/support/CO_RUNS.md`).
- Read results from the log yourself. Never ask the owner to read back or paste output.
- A prediction that fails is a finding, not a retry. Record it, then carry on with the script
  unless it says the failure voids later steps.
- A slot that errors is recorded and skipped as the script directs. Do not write replacement console
  code on the spot. If the owner asks for one anyway, record its exact text in the entry that cites
  its result.
- A member refuted here has no standing drop-or-hold rule. Record the facts, what the member still
  covers and what dropping or holding would ship, and give them to the owner.
- Restore the junction before closing, even on an aborted run, and read back where it points.

## Close-out

Archive the logs in the citing commit. Append the verdicts to 99's inbox, strike your row, `git rm`
this file, and commit on `main`.

## The script (written by 06, 2026-09-24)

Slots live in TestKit `Code/80_AgentSlots.lua` (see 06's outbox below for its HEAD). Every judged
record carries `verdict=HELD|REFUTED|NOT_SAMPLED` for the build it read (`build=main` or
`build=hubset`). The prediction table below says what each verdict means. **The owner never reads
the log: "log" means the attending session reads the `[SMRTK]` lines.** Run until drives the game at
the kit's top speed (128x, `const.MaxSaneTimeFactor`) and pauses with a chime when the watch fires.
It returns from the paused game. A real-time figure below is an estimate: it has not been measured
on this 867-colonist save at 128x.

### Before the owner sits (attending session, game closed)

1. `tasklist /FI "IMAGENAME eq Mars.exe"` reports no task.
2. Back up the fixture save before any load, since loading it runs the campaign's autosave (`EF-056`):
   copy `saves/game/EX4M-246R_New Horizons 2 83.savegame.sav` to
   `saves/reporters/EX4M-246R_New Horizons 2 83.savegame.sav`, compare `sha256sum` of both, and
   list every `saves/game` file by name with size and mtime. Neither segment saves the game.
3. The junction points at the main tree for segment A. Check it with
   `powershell -NoProfile -Command "(Get-Item \"$env:APPDATA\Surviving Mars Relaunched\Mods\SMR-BugFixPack\").Target"`,
   which must print `B:\Dev\SMR\SMR-BugFixPack`. Passage Network stays off, as in the 04 sitting.
   Name each enabled opt-in module that touches passages, hubs or colonist transport; a named one is
   a confound only where it intersects a reading.
4. Run `python -B tools/desk_hubset07_rehearsal.py` in the worktree. It must end with
   `ALL DEMANDS HELD`, with `58 of 58` held.
5. Run `python tools/bodycheck.py --src B:\Dev\SMR\SMR-Shared\SMR-SrcArchive\1.1.1.405907\Src --module VacuumWalks --all`
   in the worktree: 6 OK. That is **P3's whole check**; P3 has no player surface and nothing to play.

### Segment A: fix off (junction on `main`)

| # | owner presses | what the owner sees | real time | predictions |
|---|---|---|---|---|
| A1 | Start the game, load **New Horizons 2 83** (it loads paused) | the colony, paused | 2 min | none |
| A2 | Slots & notes → **Scratch** | nothing for you; the agent reads the log | 10 s | build=main, taint, eligibility; R1, R2 census |
| A3a | **Slot 6** (label `[1] C111 1/3`), still paused | the camera moves to a selected colonist. **Read its status line aloud.** | 30 s | P11 |
| A3b | **Slot 6** again (label `[2] C111 2/3`) | another selected colonist. **Read its status line aloud.** | 30 s | P12 |
| A4 | **Slot 1**, still paused | the game runs fast, then pauses with a chime | ≤ 1 min | P1, P2 |
| A5 | **Slot 2**, then at the chime **Slot 4** | fast run, a pause, a second fast run, a second pause | 2 min | R3 at the first pause; P3, P5, P6, R4, R6 at the second |
| A6 | **Slot 3**, then at the chime **Slot 4** | as A5 | 2 min | R5 at the first pause; P4, P6, R5 at the second |
| A7 | **Slot 5**, then at the chime **Slot 5** again (its label now reads `[2] C117 2/2`) | a pause on a busy spoke, the spoke's salvage countdown, then a pause after it clears | 2 min | P7, P8 |
| A8 | **Scratch** | nothing for you | 10 s | R1, R2 after traffic |
| A9 | not pressed: slot 6's third stage (R7) is out of scope | none | 0 | none |
| A10 | Quit to desktop (no save) | none | 30 s | none |

C111 is read first, at load, because the save's own rescues are the subjects. By A9 in segment B,
C114 and C115 have left few or none on `Transport`.
**No chime within 3x a step's time:** press **Cancel target** (Sitting tab), record the leg NOT RUN
by name, and go to the next step. A slot that answers REFUSED with a reason is recorded the same
way. Nothing is retyped at the console.

### Between segments (attending session, owner waits about 1 minute)

```
cmd /c rmdir "%APPDATA%\Surviving Mars Relaunched\Mods\SMR-BugFixPack"
powershell -NoProfile -Command "New-Item -ItemType Junction -Path \"$env:APPDATA\Surviving Mars Relaunched\Mods\SMR-BugFixPack\" -Target 'B:\Dev\SMR\SMR-BugFixPack-hubset' | Out-Null; (Get-Item \"$env:APPDATA\Surviving Mars Relaunched\Mods\SMR-BugFixPack\").Target"
```

The read-back must print `B:\Dev\SMR\SMR-BugFixPack-hubset`. Never `Remove-Item -Recurse` on the
junction. Archive segment A's post-exit log now, before B's boot writes a newer one.

### Segment B: fix on (junction on the `hubset` worktree)

B1-B8 repeat A1-A8 exactly, on the same save, with the same presses. B9 does not exist: slot 6's
third stage refuses on `hubset` by design and resets to stage 1. B10 is quit to desktop.

**Branch read-back (B2):** the Scratch line must read `build=hubset`. Every one of
`m_HubLocalAccess`, `m_HubMarkerDeparture`, `m_ObsoleteHomeRescue`, `m_PassageHubSalvageDrain`,
`m_PassageStaleHolder` and `m_RescueReturnText` must read `active`. The pack's own log carries
`[CommunityFixPack] <id>: applied` for each of those six. Segment A's Scratch must read
`build=main` with all six `absent`. A `build=mixed` line stops the segment: every slot refuses on it.

### After the sitting (attending session)

```
cmd /c rmdir "%APPDATA%\Surviving Mars Relaunched\Mods\SMR-BugFixPack"
powershell -NoProfile -Command "New-Item -ItemType Junction -Path \"$env:APPDATA\Surviving Mars Relaunched\Mods\SMR-BugFixPack\" -Target 'B:\Dev\SMR\SMR-BugFixPack' | Out-Null; (Get-Item \"$env:APPDATA\Surviving Mars Relaunched\Mods\SMR-BugFixPack\").Target"
```

The read-back must print `B:\Dev\SMR\SMR-BugFixPack`. Restore it even on an aborted run. Then
reconcile `saves/game` by name against step 2's list, and archive B's post-exit log.

### Why each leg is built as it is (departures from the brief's defaults)

- **C114's interruption is a firing**, done through `Colonist:GetFired()`. That is the call the
  workplace panel's alt-click makes (`Lua/Buildings/Workplace.lua:1700`, archived 1.1.1.405907).
  `SetWorkplace(false)` then interrupts a `Work` command (`Colonist.lua:1756-1758`), and
  `Unit:InterruptCommand` issues `SetCommand("Idle")` (`Unit.lua:860-865`). That runs the access
  check on the caller's thread (`ColonistTransport.lua:382-416`). Subjects are chosen by geometry,
  not by name: a worker whose home dome is attached to the hub and centred more than
  `g_Consts.DefaultOutsideWorkplacesRadius` hexes from it, which is the condition under which the
  native fallback at `ColonistTransport.lua:293-299` fails. Brussels is that dome on this save.
- **C115 is sampled from the save's own booked rescues at load (A3/B3).** On load, a colonist's
  `Transport` command restarts from its first line, which is where C115's bypass sits. The save's
  rescues are the field population that fixing C114 alone never cleans. If A2 reports
  `rescues_home=0`, P1 is NOT_SAMPLED and is reported by name, not rerun.
- **C117's salvage is the player's call, `PassageBase:ToggleDemolish()`** (`Passage.lua:987-994`),
  with its ~5 real-second countdown (`Demolishable.lua`, `const.DemolishCountdownMax`). The watch
  snapshots the spoke's traversers at the poll where `hub_draining` is first set, which is the
  start of `OnDemolish` (`Passage.lua:1163-1170`).
- **C42, F127 and P3 are desk-verified only**, by the owner's scope ruling at the top.
- **05's other C114 controls are not legs:** the small dome, unrelated destination, stale
  marker or holder off the hub, disconnected spoke, cross-map, outdoor, full-service and valid
  station commute. Each needs a separate fixture the brief's list does not name, and the desk covers
  them (`desk_c114_hub_access.py`, 25 demands). By the owner's scope ruling they stay
  desk-verified and are not owed.
- **R7 is not run**: it tests a stale-holder path C116's fix already handles, so it is outside the minimum.

### Predictions (written 2026-09-24, before any run)

"HELD on main" means the defect reproduced with the fix off. "HELD on hubset" means the fix worked.
Each refuting result is the verdict REFUTED on the named record. The rehearsal shows every
instrument can produce it (`docs/archive/logs/hubset06_rehearsal_2026-09-24.txt`). Normal times
are the table's; abort a leg at 3x its time and record it as NOT RUN.

| # | member | record (`[SMRTK]` verb, field) | main (fix off) | hubset (fix on) | refuted by |
|---|---|---|---|---|---|
| P1 | C115 | `TRIGGER h7_rescues`, `p1` | a rescue booked while home walks back out | every one is cleaned without leaving home | hubset: any home candidate leaves home or reaches `ready_for_pickup`; main: none does |
| P2 | C115 | `TRIGGER h7_rescues`, `p2` | a remote rescue keeps its task to pickup or shuttle | same | its task cleaned while the colonist is away |
| P3 | C114 (hub) | `TRIGGER h7_follow` after slot 2, `c114` | an own-home rescue is booked | no rescue; the colonist reaches a dome (`ended=safe`) | hubset: `booked=true` or no safe end within 4 game hours; main: no booking |
| P4 | C114 (mid-spoke) | `TRIGGER h7_follow` after slot 3, `c114` | booked mid-passage, the C115 shape (`booked_place=flight`) | no rescue; safe end | as P3 |
| P5 | C116 | `h7_follow`, `p5` | on open ground off the hub, the marker is kept and there is no outside timer | marker cleared, outside timer running | the other combination. NOT_SAMPLED if no open-ground moment (see R6) |
| P6 | C116 (ramp) | `h7_follow`, `p6` | the marker holds for the whole spoke | same | the marker drops while still traversing |
| P7 | C117 | `TRIGGER h7_drain`, `p7` | a hub-bound traverser caught by the salvage lands without holder and marker | every one lands with `holder` and `passage_hub` on the hub | hubset: any unmarked; main: none unmarked |
| P8 | C117 | `h7_drain`, `p8` | NOT_SAMPLED by design (the tunnel goes at once) | no fresh entry into the draining spoke | `entered_after > 0` |
| P11 | C111 | slot 6 stage 1, `verdict`, `tid`, `text` | T 4333, "Moving to a new Dome: <home>" | "Returning to Dome: <home>" | the other text. **The owner's spoken read is the attended witness.** |
| P12 | C111 | slot 6 stage 2, `verdict`, `tid` | T 4333, names the destination | same | any other id |
| R1 | 04 | `DUMP boot_r1`, `verdict` | every `hub.units` member holds that hub | same | `holder_mismatch > 0` (the chain author's overstatement note predicts this is possible) |
| R2 | 04 | `DUMP boot_r2`, `verdict` | every member in flight or standing on the hub | same | `neither > 0`: the stale-holder finding is live |
| R3 | 04 | `TRIGGER h7_hub_arrival`, `r3` | the arrival's logical hex is the hub's | same | `arrival_hex=false` |
| R4 | 04 | `h7_follow` after slot 2, `r4` | after the dump: no hub holder, marker kept, on the hub hex | same | `dump_hex=false` or marker lost |
| R5 | 04 | `TRIGGER h7_mid_spoke` fields and `h7_follow` `r5` | flag set and listed mid-passage; list cleared on arrival | same | flag false while listed, or still listed after landing |
| R6 | 04 | `h7_follow`, `r6` | no overland walk off the hub (INFERRED) | same | an open-ground moment after leaving the hub |

## Notes from upstream

### From hubset 06, 2026-09-24 — sitting prepared

- **Heads:** TestKit `66288da` (`Code/80_AgentSlots.lua`, sha256 prefix `4081e6a66c43c2bc`),
  `hubset` `7cf48a2` (adds `tools/desk_hubset07_rehearsal.py`), `main` at this close-out commit
  (parent `371aad5`). The script, predictions P1-P13 and R1-R7, junction commands and owner-seat
  read are in 07's `## The script` section.
- **Slot labels:** Scratch `Boot: build, fixture, census (read only)`; 1 `C115: follow own-home
  rescues from load`; 2 `Pause on a far-home worker landing on a hub (R3)`; 3 `Pause on a far-home
  worker mid-spoke (R5)`; 4 `Fire the paused worker and follow it (C114/C116)`; 5 staged
  `[1] C117 1/2: pause on a busy hub spoke` / `[2] C117 2/2: salvage the paused spoke, follow`;
  6 staged `[1] C111 1/3: select an own-home rescue` / `[2] C111 2/3: select a real relocation` /
  `[3] R7 3/3: marker clear per hex class (segment A only)`. Triggers: `h7_rescues`,
  `h7_hub_arrival`, `h7_mid_spoke`, `h7_follow`, `h7_busy`, `h7_drain`.
- **Owner minutes: about 30, an estimate, not measured** (A 13, B 12, relaying words 5). Two boots:
  fix off on `main`, fix on on `hubset`. No module can be switched off at runtime.
- **Rehearsal (declared VOID):** [archived output](../../../archive/logs/hubset06_rehearsal_2026-09-24.txt).
  58 of 58 demands held, every prediction's scratch variant read REFUTED, and nothing armed at load.
  A mutant that forces P7's hubset judge to HELD failed the harness (57 of 58, exit 1). SMRTK gates:
  parsecheck 0 errors; both `rg` gates matched 0 lines with exit 1, beside a positive control on
  the same scope. P3: bodycheck on `hubset` gave 6 OK.
- **Stop routed to the owner: F127 has no leg.** Its C83 branch needs a passenger arrival whose chosen
  dome turns unwelcoming, with a full fallback. That is a hand-built fixture: about 5-8 owner
  minutes per segment plus rocket transit, at unknown odds. Only P13, a read-only hidden-homeless
  census, is built. The owner chooses to build that fixture as a 07 amendment, or to leave F127
  desk-verified.
- **Not played, routed to 99:** 05's other C114 controls (small dome, unrelated destination, stale
  marker or holder off the hub, disconnected spoke, cross-map, outdoor, full-service and valid
  station commute). 05 called the station commute decisive. Also not played: C116 save/reload, and
  R4's visual hex and holder-list membership. The follow records only the logical hub hex at the
  dump. An idle stale marker at load is counted by place in the census, not followed.
- **C42:** no stand-alone leg. P10 (`C42STALE` after traffic) is the live witness for the owner
  decision still open in 99's inbox. P9 samples a kick only if a stale element member exists.
- **Drift:** `tools/SMRTK.md` says "A pack lane does not commit in it" of the TestKit, while 06's
  brief requires the slots "committed in the TestKit repo". The brief was followed (`66288da`); the
  tension is not resolved here.

### From the owner, 2026-09-24, after 06 closed: scope cut

Verbatim: "anything that was a minor addon that isn't what this chain was created for are desk
verified only. I have been trying to fix one set of new bugs for 4+ hours now, and I am still
talking about other stuff. We are doing the bare minimal testing in game needed to ship these new
fixes. We have around 4000 people waiting for these fixes. Re checking things from auguest on a
previous patch, that is considered minor is not on the agenda". Applied to the script above: C42,
F127 and P3 have no readings, R7 is not run, and 06's F127 stop and its list of C114 controls
routed to 99 are withdrawn. Do not add legs.
