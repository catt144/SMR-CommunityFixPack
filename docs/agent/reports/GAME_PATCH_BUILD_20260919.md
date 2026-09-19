# GAME_PATCH_BUILD — patchcheck, its regression test, the perma job and the fork outbox

**2026-09-19, firing `prompts/GAME_PATCH_BUILD_high.md` (grave: this commit).** Authoring sha
`598fafe`; `git diff --stat 598fafe..HEAD -- tools/ Code/ docs/agent/reports/GAME_PATCH_INSTRUMENTS.md`
was empty at start, so the brief's facts held. Design: `reports/GAME_PATCH_INSTRUMENTS.md`. Executed
model: Claude Opus 5; one read-only tier-2 subagent for the D2 reads (§3). No game launched, no
`Code/` or TestKit edit.

> ⚖️ **Headline.** `python tools/patchcheck.py` reproduces the 1.1.0 backtest: every §3.1 column
> (PIN, REQ, SIGCALL, CITE, D1) matches on the pre-patch pack, identity is 0/80 → none, and F117 is
> found and ranked incompatible. It is the regression test, and it goes RED when any harvested
> column is emptied. On today's packs it says **full** over 1.0.7 → 1.1.0 and **none** over
> 1.1.0 → 1.1.0. Its eleven D2 rows are all harmless on 1.1.0, so there is no defect to file. The
> small-patch regime is uncalibrated until the first real patch.

## 1 · What landed

| commit | repo | what |
|---|---|---|
| `49e1420` | fix pack | `tools/patchcheck.py`, `tools/patchcheck_selftest.py`, TOOL CATALOG group |
| `a7aa5af` | fix pack | `prompts/perma/GAME_PATCH_PROMPT.md` + map row; WORKFLOW "After a game patch" routes to it; the class-c count corrected at `WORKFLOW.md` and `bodycheck.py` |
| `6afedb7` | opt-in fork | `docs/agent/prompts/perma/gamepatch/README.md`, `done/README.md`, map row |
| this commit | fix pack | this report; the brief and its map row deleted; a comment in `patchcheck.py` (§4) |

## 2 · The regression test

`python tools/patchcheck_selftest.py` (~17 s on this rig; it indexes both archived trees once and
reuses the index across legs) printed GREEN on 16 legs:

```
PASS  §3.1 PIN     FIX/REMOVE/KEEP/flagged = 6/21/16/43  — got 6/21/16/43
PASS  §3.1 REQ     FIX/REMOVE/KEEP/flagged = 6/14/17/37  — got 6/14/17/37
PASS  §3.1 SIGCALL FIX/REMOVE/KEEP/flagged = 3/7/4/14  — got 3/7/4/14
PASS  §3.1 CITE    FIX/REMOVE/KEEP/flagged = 10/34/28/72  — got 10/34/28/72
PASS  §3.1 D1      FIX/REMOVE/KEEP/flagged = 10/34/32/76  — got 10/34/32/76
PASS  1.0.7 -> 1.1.0 verdict is full  — full
PASS  D2 finds ArrivalDeaths -> ChooseDome, incompatible (F117)  — incompatible
PASS  ANON flags MeteorFrequency (R-9, the D1 miss)  — ANON=True D1=False
PASS  identity overlay: 0/80 flagged
PASS  identity overlay verdict is none  — none
PASS  one-file overlay (SYNTHETIC) flags exactly DomeFreeSpaceMismatch, StaleReservations  — DomeFreeSpaceMismatch, StaleReservations
PASS  one-file overlay verdict is full by B alone  — verdict: FULL — B = 1  (…)
PASS  one-file overlay Community.lua (SYNTHETIC) flags exactly ShelterReflex  — ShelterReflex
PASS  Community.lua overlay verdict is scoped  — scoped
```

(Two setup legs are omitted above: the pack has 80 modules, and the answer key splits 10/35/35.)
Falsified before the pass was trusted: `--break REQ` → RED on 3 legs (D1 fell to 10/34/28/72);
`--break PIN`, `--break CITE` and `--break SIGCALL` each exit 1. Per-module flags on the full run equal
the prototype's `backtest_rows.tsv` for all 80 modules and every column.

## 3 · First real output

**Today's `Code/` and the opt-in `Code/`, 1.0.7 → the live install** (`python tools/patchcheck.py
--code Code --code C:/Dev/SMR-OptInPack/Code --no-d5-list`, HEAD `a7aa5af`):

```
A archived: live Src == 1.1.0.403908\MANIFEST.sha256 (digest a4577da25cb3fe85…)
P holds — Lua.fpk 2373/2373 byte-identical, 0 divergent, 0 absent; Data.fpk 2191/2191 byte-identical, 0 divergent, 0 absent
T 4710 changed hand declarations = body 3487 + body+sig 291 + removed 828 + moved+body 104 (moved 456, added 4244 excluded)
B 40 file(s) with a DefineClass/__parents line changed under a pinned/required/cited file
notes: fetched — 'Services & Science Patch Notes - Version 1.1.0' (2026-09-08)
columns: PIN 30 · REQ 22 · CITE 44 · ANON 35 · SIGCALL 8 · D1 50 · M 50
D3 save-exposed sites in this Code/: 6; flagged 1
summary Code: modules 52 · M 50 · notes-added 0 · D3 1
summary C:/Dev/SMR-OptInPack/Code: modules 4 · M 4 · notes-added 0 · D3 0
verdict: FULL — |M| = 50 > 12; B = 40; T = 4710 > 1000  (…)
```

P re-proves `EF-085` for this build (in memory, not on disk). T equals the report's 4,710.
Today's modules cite 1.1.0 lines, so CITE and ANON map them into the 1.0.7 tree wrongly on this
pair. That is expected: on a real patch the old tree is the one the citations were written against.

**Today's packs, 1.1.0 → 1.1.0** (`--old 1.1.0.403908`): `M 0`, `D3 0`, `B 0`, `T 0`,
`notes: n/a (no file changed between the trees)`, **`verdict: NONE`**, for both packs.

**The D2 rows, read.** The known unread row, `DustSicknessBiorobots` → `Affect`, was read, and so were
the rows with only a thin record. Every read was done by a subagent in both archived trees; I
re-read `Affect` myself (1.1.0 `Lua/Units/Colonist.lua:1514`, whose remove branch clears
`status_effect_explanation` itself).

| module | call | record | verdict |
|---|---|---|---|
| CloggedBuildingRelease | `setter` (gone) | none | **false match**: our `local setter` (`Code/Fix_CloggedBuildingRelease.lua:261`) paired with a local in 1.0.7 `CommonLua/Libs/DevToolsPublic/FlightDebug.lua:118`, a file 1.1.0 deleted |
| ArrivalDeaths | `ChooseDome`, `GetScoreFor` | F117 | known |
| LandscapeUnitFilter | `LandscapeForEachUnit` | F115 | known |
| ArrivalDeaths, ShuttleTransportCache | `ValidateBuilding` (−`for_story_bits`) | report §1, no reason | harmless: our calls pass one argument, so the dropped branch (1.0.7 `Workplace.lua:958`) never ran |
| CloggedBuildingRelease | `Setexceptional_circumstances` (+`reason`) | C85 | harmless; the 1.1.0 overrides (`Workplace.lua:597`, `Elevator.lua:1183`) pass `reason` through to `BaseBuilding.lua:470` |
| DustSicknessBiorobots | `Affect` (+`explanation`) | none | **harmless**: `explanation` is read only when applying; our call removes (`Code/Fix_DustSicknessBiorobots.lua:182`) |
| PayloadTemplateRefill | `resolve_loc_cargo_template` | F70 | our own local copy, which already takes both parameters |
| TrackSalvageRefund | `PlaceResourceStockpile_Delayed` (+`tall_piles`) | report §1, no reason | harmless: nil gives the old pile shape (1.1.0 `ResourceStockpile.lua:1101`); amounts unchanged. Our partial-trim refunds use normal-height piles where vanilla's demolish now uses tall ones; that is cosmetic |
| VacuumWalks | `DiscardTransportTicket` (+`mode`) | partial (`Code/Fix_VacuumWalks.lua:51`) | harmless: the same argument-less call vanilla makes at 1.1.0 `Colonist.lua:1918` |

No defect was found, so nothing is filed.

## 4 · Departures from the report, with the reason

- **§3.5's one-file control names the wrong KEEP module.** The prototype, re-run today
  (`backtest.py --overlay Lua/Buildings/Residence.lua`), flags `DomeFreeSpaceMismatch` (cited
  `ChooseResidence` changed), not `FreedHousingNotice`. The brief copied the report's prose; the
  test asserts the measured pair.
- **That control's verdict is full, not scoped.** B was not built when the report wrote "scoped".
  1.1.0's `Residence.lua` changes two `__parents` lines, so B = 1 raises the verdict by itself while
  |M| = 2. A second overlay (`Community.lua` alone → ShelterReflex) exercises scoped.
- **ANON is its own column, inside M but outside D1.** That keeps D1 equal to §3.1's
  PIN+REQ+CITE row. ANON implements §3.3's "flagged whenever their file changes" as "a citation
  outside every keyed declaration", which catches R-9 MeteorFrequency, D1's one miss. It is broad:
  a citation into a `DefineClass` table also counts.
- **T's definition** is the one that reproduces 4,710: body + body+sig + removed + moved+body, over
  hand files; additions are excluded.
- **PIN also reads `-- SRC:` selectors.** The pre-patch pack has none, so the backtest is unchanged.
- **Notes → modules:** phrases of two or more words from what a module names, or a single word found
  in at most 5 game class names; a phrase shared by more than 5 modules routes nowhere. Notes are
  skipped when no file changed or under an overlay. The 1.1.0 notes route no module; a planted
  sentence routes two, so the matcher can hit. It is weak by nature, because notes are written in
  player language.
- **A local-name filter on D2 was tried and reverted.** It removed the `setter` false match, but
  it also dropped PayloadTemplateRefill's `resolve_loc_cargo_template`: a local copy of a vanilla
  file-local is the stale-copy FIX signal (§3.1 SIGCALL FIX 3 → 2, caught by the regression test).
  The reason is recorded at the harvest in `patchcheck.py`.
- **The run record is a report per patch** (`reports/GAMEPATCH_<build>_<date>.md`), not a log
  inside the perma prompt, because `prompts/` holds prompts only.
- **`SMRFixPack.ListFixes()` at autorun quit: not added.** The boot census that `logscan.py` reads
  already carries applied/inactive per module, and the kit is out of this build's scope. Three
  lines, if the first real patch shows the census missing it.

## 5 · Suggestions

1. The fork's PROMPT MAP gate keys perma rows on `*.md` files directly in `perma/`, so the
   `gamepatch/` row is for readers only. Enumerating a perma subfolder by its README would make
   the row gated.
2. `B` fires on any `DefineClass`/`__parents` line change in a touched file, which is 40 files on
   1.0.7 → 1.1.0. On a hotfix that is right. If a real patch shows B raising a verdict for a
   property-only edit, narrow it to `__parents` lines.
3. The first real patch should record per-step tokens in `GAME_PATCH_PROMPT.md`'s todo list. It is
   the first cost figure this project will have for a patch response.

## 6 · Out-of-scope findings

- `docs/agent/reports/GAME_PATCH_INSTRUMENTS.md` §3.5 misnames the one-file control's KEEP flag (see
  §4). The report is not edited; this entry is the correction.
- `prompts/STANDDOWN_AUDIT.md:86` says the D1 detector was "built by `GAME_PATCH_BUILD_high.md`",
  which this commit deletes; the tool is `tools/patchcheck.py`. Not edited: that prompt is out of
  this build's scope.
- `Fix_StaleReservations.lua` still does not pin `CancelResidenceReservation` (report §3.3).
  patchcheck's REQ covers it, so a pin is no longer needed for the sweep.

## 7 · Not done

- No game launch: the G3 recall boot (§3.4) and G4 are out of scope.
- The D5 list (43 facts on 1.0.7 → 1.1.0) is emitted but not filed. Most of those facts were
  re-derived on 1.1.0, and D5 maps citations into the old tree.
- `STANDDOWN_AUDIT.md` is untouched except for its map row, which pointed at this brief and now
  points at `tools/patchcheck.py`.
