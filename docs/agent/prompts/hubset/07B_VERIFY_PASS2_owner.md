# hubset 07B: second attended pass on C111, C114 and C117 (owner-approved)

Chain rules: [README.md](README.md). Read them, then `## Notes from upstream` below, first.
**Attended:** the owner clicks preloaded SMRTK slots. The session relays the owner's words, reads the log and records.
Fire after 06B has closed, before 99.

## Authority and outcome

Owner, 2026-09-24, after 06B: "If you can write up test code that can prove it and I can easily
check it in game without fishing for circumstances then we can do another pass". That permits
this one pass as an exception to the chain's "One sitting only". It permits no other sitting. The scope is the three
members 07 left open: C111, C114 and C117. C115, C116, C42, F127 and P3 keep their 07 or desk
standing and get no reading here.

End state:
- each segment's post-exit log archived;
- a verdict against every prediction below;
- each of the three entries updated on `main` with what the owner watched. Use `tested-attended`
  only where the owner watched the fix work on `hubset`;
- the junction restored to the main tree and read back;
- 99's inbox holding every verdict and every drift from this script.

## Before the owner sits (attending session, game closed)

Check it from the owner's chair. If a check fails, stop and route it to the owner.

1. `tasklist /FI "IMAGENAME eq Mars.exe"` reports no task.
2. Heads:
   - TestKit `4fd0275` (`Code/80_AgentSlots.lua` sha256 prefix `4b1b4a214467ee28`);
   - `hubset` at or after `7f6e6bf`, which carries the C111 re-fix `e5fc0c6`;
   - `git -C ../SMR-BugFixPack-hubset status --short` is clean.
3. Save: `saves/reporters/EX4M-246R_New Horizons 2 83.savegame.sav` exists and its sha256 equals
   `saves/game/EX4M-246R_New Horizons 2 83.savegame.sav`'s (07's backup, `036e130d…`). List every
   `saves/game` file by name, size and mtime. Neither segment saves the game.
4. The junction points at `B:\Dev\SMR\SMR-BugFixPack` for segment A. Read it back with
   `powershell -NoProfile -Command "(Get-Item \"$env:APPDATA\Surviving Mars Relaunched\Mods\SMR-BugFixPack\").Target"`.
   Passage Network stays off.
5. In the `hubset` worktree:
   - `python -B tools/desk_hubset07b_rehearsal.py` ends `ALL DEMANDS HELD`, 48 of 48;
   - `python -B tools/desk_c111_rescue_text.py` passes.
6. The [tools/SMRTK.md](../../../../tools/SMRTK.md) "Gates" commands give their stated results.

Then give the owner one line: *"start the game; the Slots & notes tab is loaded"*, plus the save.

## Rules for the sitting

As 07: relay the owner's words into the log as spoken (`docs/agent/support/CO_RUNS.md`), and read
results yourself. A failed prediction is a finding, not a retry. A slot that refuses or errors is
recorded and skipped, and nothing is retyped at the console. The chime may not sound (07 drift): the
game pausing itself is the signal. Restore the junction before closing, even on an aborted run.

## The script

Every judged record carries `verdict=HELD|REFUTED|NOT_SAMPLED` and `build=main|hubset`. "Run fast"
means SMRTK's top speed (128x). Slot 5 alone runs at normal speed through the 5-second
salvage countdown, which ticks in real time (`Demolishable.lua:102-117`, archived
1.1.1.405907); it then speeds up by itself.

### Segment A: fix off (junction on `main`)

| # | owner presses | what the owner sees | predictions |
|---|---|---|---|
| A1 | start the game, load **New Horizons 2 83** (it loads paused) | the colony, paused | none |
| A2 | Slots & notes → **Scratch** | nothing for you | build=main, six `absent`; `c114_hubs`, `c111_subjects` |
| A3 | **Slot 1**, still paused | the camera moves to a selected colonist; send its status line or a screenshot | C111 |
| A4 | **Slot 2** | the game runs fast, then pauses on a selected colonist standing on a hub | selection inputs logged |
| A5 | **Slot 3** | the game runs fast, then pauses on that colonist, selected; send its status line or a screenshot | C114 |
| A6 | **Slot 4** | the game runs fast, then pauses | busy spoke found |
| A7 | **Slot 5** | a salvage countdown at normal speed, then a fast run, then a pause on a selected colonist; send a screenshot | C117, C117 entry |
| A8 | quit to desktop (no save) | none | none |

If A2 reads `c114_hubs=0`, skip A4-A5 and record C114 NOT_SAMPLED by name. Slots 2 and 4 each end
on their own after one game day if nothing qualifies, and log `found=false`.

### Between segments (attending session)

```
cmd /c rmdir "%APPDATA%\Surviving Mars Relaunched\Mods\SMR-BugFixPack"
powershell -NoProfile -Command "New-Item -ItemType Junction -Path \"$env:APPDATA\Surviving Mars Relaunched\Mods\SMR-BugFixPack\" -Target 'B:\Dev\SMR\SMR-BugFixPack-hubset' | Out-Null; (Get-Item \"$env:APPDATA\Surviving Mars Relaunched\Mods\SMR-BugFixPack\").Target"
```

The read-back must print `B:\Dev\SMR\SMR-BugFixPack-hubset`. Never `Remove-Item -Recurse` on the
junction. Archive segment A's post-exit log before B's boot writes a newer one.

### Segment B: fix on (junction on `hubset`)

B1-B8 repeat A1-A8 with the same presses. At B2 the Scratch line must read `build=hubset` with all
six modules `active`, and the pack log must carry `[CommunityFixPack] <id>: applied` for each.
`build=mixed` stops the segment.

### After the sitting (attending session)

Restore the junction to `B:\Dev\SMR\SMR-BugFixPack` with the same two commands and read it back, even
on an aborted run. Reconcile `saves/game` by name against step 3's list. Archive B's post-exit log.

### Predictions (written 2026-09-24, before any run)

| member | record | main (fix off) | hubset (fix on) | refuted by |
|---|---|---|---|---|
| C111 | `slot_1` `verdict`, `tid`, `text`, `emigration_dome` | T 4333, "Moving to a new Dome: Brussels" | "Returning to Dome: Brussels", `tid` not 4333 | hubset: T 4333. The owner's read of B3 is the attended witness |
| C114 | `TRIGGER h7b_follow` `verdict`, `booked`, `ended` | `booked=true`: the worker gets a shuttle rescue although it stands on a hub linked to its home | `booked=false ended=safe`: it walks home through the passage | main: no booking. hubset: a booking, or no safe end within 4 game hours |
| C117 | `TRIGGER h7b_drain` `verdict`, `hub_bound`, `hub_bound_unmarked` | at least one walker lands on the hub hex without holder and marker, left outside | every hub landing is held and marked | hubset: any unmarked. main: none unmarked |
| C117 entry | `h7b_drain` `entry_verdict`, `entered_after` | NOT_SAMPLED by design | no fresh walker enters the draining spoke | `entered_after > 0` |

**C114's selection** (`fire_before` DUMP) must show `exposed=true`, which means every input native
`HasLocalAccess(home)` reads was out of reach: `nearest_reach`, `home_reach`, `in_dome`, `train` and
`work_route` false, `dist_hub` and `dist_unit` over `radius`, and `shuttles` and `linked` true.
Selection reads these inputs with the game's own helpers and never the answer under test. The
rehearsal flips each one alone and requires the subject to be rejected.

**NOT_SAMPLED** is not a pass. C117 reads NOT_SAMPLED only if no traverser caught by the drain landed
on the hub hex. Record it by name with `at_drain` and `arrivals`.

### Why each leg is built as it is

- **C111** needs nothing staged. The fixture loads with Colonist(2000010346) in an own-home
  `Transport`, as both 07 segments showed. The slot now also logs the raw `emigration_dome` and
  `dreaming`, the reading 06B said was missing.
- **C114** replaces 07's "any far-home worker" with the reporter's shape, checked on its native
  inputs. 07's subjects stood near a dome that granted access natively, so fix-off and fix-on could
  not differ there (06B). 07's census shows four hubs on this save whose every attached dome is over
  20 hexes away: 2692, 4113, 1908 and 11714. Firing is `Colonist:GetFired()`, the workplace alt-click
  call, as in 07.
- **C117** keeps 07's salvage, `PassageBase:ToggleDemolish()`, the player's call. It now runs the
  countdown at 1x, where 07's watch had timed out at 128x after 90,368 game ms (06B), and it requires
  at least 5 walkers on the spoke. The snapshot is taken at the first poll that sees `hub_draining`,
  so walkers who leave during the countdown are not counted (06B's sampling limit).

## Close-out

Archive the logs, the owner relay and any screenshots in the citing commit. Update C111, C114 and C117 on `main`,
append the verdicts and drift to 99's inbox, strike your row, `git rm` this file, and commit on
`main`. A member refuted here has no standing drop-or-hold rule: record the facts and bring them to
the owner.

## Notes from upstream

### From the second-pass author, 2026-09-24

- Heads: TestKit `4fd0275` (07B slots); `hubset` `7f6e6bf` (adds `tools/desk_hubset07b_rehearsal.py`,
  pins `desk_hubset07_rehearsal.py` to TestKit `66288da`); C111 re-fix `e5fc0c6`.
- Desk: 48 of 48 demands held. Two mutants each failed it: a forced C114 hubset HELD (47 of 48) and
  dropping the train input from the selection (44 of 48). Gates: parsecheck 0 errors; both `rg`
  gates 0 lines, exit 1, beside a positive `SelectObj` control on the same file.
- Unverified until the game runs: that one of the four hubs yields a worker whose nearest community
  is out of reach (Scratch's `c114_hubs` answers it at A2), and that the `h7b_follow` and `h7b_drain`
  auto-screenshots include the infopanel.
