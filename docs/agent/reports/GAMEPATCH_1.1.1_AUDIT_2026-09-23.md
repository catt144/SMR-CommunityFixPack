# Audit of the 1.1.1 build — `16ff1aa..45578d4` (2026-09-23)

The one-off audit brief `GAMEPATCH_1_1_1_FIX_AUDIT_high.md` (authored at `16ff1aa`, before the
build existed; deleted with this report) run on a different vendor from the one that built
`45578d4`. Judged on the diff and the archived `1.1.0.403908` and `1.1.1.405907` trees, never
on the build report's account of itself.

## Must_Read_Header

Reader: the owner deciding what is safe to ship, what is owed to play and what is still wrong;
then the release job. Verdicts are **confirmed**, **corrected** (the record was changed in this
commit) or **unproven**. Game citations are SOURCE on the archived `1.1.1.405907` tree unless
marked `1.1.0.403908`; module lines are the pack at `45578d4` (HEAD `76c18ed` adds only the
audit prompt). **desk-MEASURED** means a named harness this seat ran itself at `76c18ed`; the
build's receipt was not accepted as a measurement. Nothing here launched the game or changed
code; five of the owner's save files were read as bytes, never loaded (§4). Owner play is
ck210 and ck211.

## 0 · Outcome in one screen

| area | verdict | what it rests on / what the owner decides |
|---|---|---|
| Track unit — F124 rebase, F44/F91/F116, F45 retirement, refund wrapper | **confirmed** at the desk | every vendor repair-site semantic is verbatim in the installed body (§2); only marked F44/F91 sites differ; refund answered by harness legs, not asserted. Play: ck210 phase 2 |
| F125 `Fix_VacuumWalks` | **confirmed** at the desk | both passage sites repaired by input wrappers whose bounds are proved against the native body (§3); the builder's challenge to the old F52 design note is sound. Play: ck210 phase 2 |
| F121 `Fix_CloggedBuildingRelease` | **confirmed** at the desk and on real saves | the provenance chain is closed from the installed pack's revision file and confirmed by reading five of the owner's saves: 1.1.1 saves carry `lua_revision = 405907`, 1.1.0 saves `403908` (§4); the builder's challenge is sound with one residual named. Play: ck210 phase 4 |
| Sixteen retirements | 15 **confirmed**; C93 `Fix_OpenPastureStockpiles` **corrected** | replacement and consumer traced for all sixteen; references gone by name on every live surface (§5). The C93 retail gate proves less than the record said: asset half **unproven** → ck211 |
| F122 / F123 / F126 two-sided controls | **confirmed** run | the pack-off legs call the archived native body; run by this seat (§6). Retail legs remain ck210 phase 3 |
| Reconciliation and gates | **confirmed** | four independent name lists agree; census, doccheck, both selftests green; `bodycheck --all` exit 1 is the pre-build standing state, diagnosed (§7) |
| Controls able to fail | **confirmed** | six guard reversals by this seat in scratch copies, all red as expected (§7) |
| Builder's challenges | three **sound**, one suggestion left as a lead (§8) | no record needed correcting for them; silence on the KEEP rows, ranking and A/B noted |
| Safe to ship? | code: nothing found wrong | what stands between the desk and a release is ck210, ck211 and the release job's surface reconciliation (§10) |

## 1 · Range, method, receipts

- Range: `16ff1aa..45578d4` is one commit, 72 files, 3,973 insertions / 3,205 deletions
  (`git diff --stat`). HEAD `76c18ed` adds only the audit prompt. Origin is not ahead.
- **The build receipt is tied to the committed bytes.** Its 112 "validated source" hashes
  (`Code/*.lua`, `tools/*.py`) all equal the sha256 of the `45578d4` blobs (script
  `scratchpad/receipt_hashes.py`: 112 ok, 0 bad, 0 missing; the committed set is 113 because
  `tools/held/Fix_MysteryTechMigration.lua` is held outside the pack). Every receipt line says
  `HEAD: 16ff1aa` because the commands ran on the working tree before the commit; the hash
  match is what makes them evidence about `45578d4`.
- **Every gate and harness was re-run by this seat at `76c18ed`** (§7 has the table).
- Two subagents were used, each cleared by one check aimed at what it rested on: a tier-2
  reader traced all sixteen replacements and consumers on the archived tree (its Open Pasture
  claim was verified against the deleted probe's text, §5); a tier-1 reader produced the
  by-name reference census (its four-list diff was checked against
  `gamepatch_111_census.py`'s printed members). Neither edited a file.
- The TestKit repo (`B:\Dev\SMR\SMR-BugFixPack-TestKit`) has no remote; its companion commit
  `aa47d3e` is its HEAD and its tree is clean. Only desk harnesses read that tree; the pack
  does not depend on it.

## 2 · The track unit

Installed body: `Code/Fix_TrackSalvageWipe.lua:47-247`. Archived body:
`Lua/Buildings/TrackElement.lua:467-637`, sha `2f08d0c5…`, which the module pins and
`bodycheck` reports OK. Compared span by span:

| vendor semantic the brief named | archived | installed | result |
|---|---|---|---|
| repair-site exclusion from `all_elements` | `:484-488` | `:66-70` | verbatim |
| correct-array removal (`remove_from_track_arrays`) | `:517-525` | `:113-121` | verbatim |
| repair-site rehome and `repair_cgs` rebuild | `:598-614` | `:208-224` | verbatim |
| repair-aware `ProcessAllElements`, pre-sort and post-split | `:473-476`, `:628-632` | `:55-58`, `:238-242` | verbatim; `Track.lua:466-474` is the vendor body, and the only 1.1.0→1.1.1 change in `Track.lua` is that method's repair filter (`diff`) |
| orphan safeguard, `ripairs` cleanup, `UpdateEndElements`/`UpdatePos` | `:581-595`, `:616-627` | `:191-206`, `:226-237` | verbatim |

Every other line differs only at a site marked `-- FIX`: the legacy-debris exit (`:49-50`),
the decline on a non-numeric `node_idx` (`:71-74`, where vanilla would raise inside the sort
comparator), F91's finish-the-deletion block (`:80-87`), the anchor fallback (`:105-107`), the
two short-remainder `OnDemolish` exits removed (`:125`, `:138`), the two `IsValid` guards on
`UpdateEndElements` (`:133`, `:146`) and the valid-survivor seeding (`:164-189`). On the path
where both seeds are valid, that seeding does exactly what `:570-579` does; on 1.1.1 repair
sites are not in `all_elements`, so the twin-invalidation case it was written for cannot arise
from the zone loop, and the extra generality is harmless.

- **F91's premise still holds on 1.1.1.** `TrackBase:OnDemolish` (`Track.lua:248-284`) still
  sets `CanDelete = ret_false` and `demolishing`, destroys trains and elements, and never
  deletes itself; the module restores the three arrays before `DoneObject` so `TrackBase:Done`
  (`:69-76`) can walk them.
- **The refund wrapper question was answered with evidence.** Under 1.1.1's array rule a
  repair site lives in `elements_under_construction` (`TrackElement.lua:611`) and completed
  elements stay in `track.elements`, which is the only array
  `Fix_TrackSalvageRefund.lua:210-229` snapshots; a repair-site click delegates on the same
  test the split body uses (`:470-471` ↔ `:204-207`). desk-MEASURED: the harness cases
  "curved split and physical refund", "repair split ownership and repair_cgs", "repair click
  delegates once and forwards skip", "surviving stamps are not refunded" and "whole salvage
  refund and shell cleanup" each assert the refunded amount.
- **`Fix_BrokenTrackSalvage` is gone** from disk, `items.lua`, `metadata.lua`, the TestKit
  registrations and capture rows (census and §5), with no stale pin (`bodycheck --all` has no
  row for it); F45's entry keeps its PT-03 evidence under "Historical filing and evidence".
- **Branch guard, a limit not a defect.** The module's `test` names `Colonist.MigrateStep`, a
  declaration that exists on 1.1.1 only. FIX_POLICY §2a allows that form when nothing in the
  target is probe-able; the split body cannot be driven on a stub. No track-local shape
  exists (`TrackElement.lua` gained no declaration between the builds; `Station.lua` gained
  `Station:GetNumTrainsOnTracks`, an alternative of the same strength). The guard identifies
  the branch, not the body's semantics; the desk discriminator for the next patch is the SRC
  pin and DEFECT regex.

## 3 · F125 `Fix_VacuumWalks`

Both native bodies are pinned and OK: `Colonist:TryToEmigrateToDome` (`Colonist.lua:1894-1982`)
and `Colonist:MigrateStep` (`:2155-2221`), with a DEFECT regex on each threshold line.

**Direct site (`:1911-1922`).** The wrapper (`Code/Fix_VacuumWalks.lua:153-182`) delegates
unchanged unless the call is a positive walk within `ColonistMaxDomeWalkDist`, in vacuum, with
the runtime gap `MaxDomeWalkDist + 1 < MinDistToIgnorePassage`, and
`AreDomesConnectedWithPassage(current, dest)` — which is `GetDomesPassagePath`'s own first gate
(`Passage.lua:1300-1303`). Then it passes `MaxDomeWalkDist + 1`. Against the native body: it is
positive, so the `-1` conversion at `:1912-1915` is not entered; it exceeds `min_dist` at
`:1916`, so the passage is looked up; it is below `dome_passage_dist` at `:1922`, so the
walk-versus-shuttle choice is unchanged; and `transport_mode_dist` is not read after `:1922`.
The pre-build fix (`min_dist = 0` with the original distance) produced the same three
decisions, so shipped behaviour is equivalent where the old copy applied and native everywhere
else. The old F52 note's objection ("a distance pre-wrapper flips the `-1` conversion and the
walk-vs-shuttle choice") was about an unbounded change; the bound removes both. **Challenge
sound.**

**Intermediate site (`:2196-2202`).** It is reachable in vacuum: `MigrateStep`'s final `else`
runs for a walk leg that is not final while the colonist is in a dome. `GetNextMigrationLeg`'s
wrapper arms a marker keyed by the command thread only under those conditions (`:2166` is the
only call with `command == "MigrateStep"` on its own thread; `:3803`, `:4330`,
`ColonistTransport.lua:679`, `:853` run under other commands or on other threads), and the
`IsInWalkingDistDome` wrapper consumes it on the very next call on that thread, which is
`:2198` — no other call sits between, and each loop iteration clears before re-arming. Seven
callers of `IsInWalkingDistDome` were enumerated; only `:2198` can match the armed domes and
city. Forcing `-1` there makes native ask for the passage (`:2199`) and then discard the value.
The wrappers are synchronous, the direct one tail-calls the native body, the marker table is
weak and process-local: no frame of ours can be on a persisted thread.

**Guard limit.** The apply-time probe drives `StartShuttleLeg` on a stub; the threshold lines
cannot be probed at apply time because `g_Consts` is `false` then, so the runtime guard proves
the branch shape, and the two DEFECT regexes carry the discrimination at the desk.

desk-MEASURED by this seat: `desk_f125_vacuum.py` 25/25 (direct, no-passage, breathable, long
detour, threshold edges, retarget, shuttle, train, cancellation, unrelated caller, failed
`SetGlobal`, the actual TestKit probe); `desk_migration_cluster.py` 16/16 and its `--selftest`.

## 4 · F121 `Fix_CloggedBuildingRelease`

The module is a synchronous `LoadGame` handler and nothing else: no `NewDay`, no thread, no
field, no UI (`Code/Fix_CloggedBuildingRelease.lua:114-139`). The interlocks of C85 are intact.

**The provenance chain, closed without a save file.** `SMRFixPack.WhenActive` forwards the
message arguments (`00_Core.lua:269-276`), and `Msg("LoadGame", metadata, …)` is sent at
`CommonLua/Savegame.lua:808` with the save's own metadata: `GetFullMetadata` (`:951-985`)
merges the file's `savegame_metadata` into it and nothing re-stamps it before `UnpersistGame`
(`:798`). The stamp itself is `AddSystemMetadata` (`:775`, `metadata.lua_revision =
LuaRevision`). On a packed retail boot `LuaRevision` comes from `pdofile("_LuaRevision.lua")`
(`CommonLua/Core/autorun.lua:308-310`; the unpacked `svn` route at `:307` is not taken). This
seat read that file from the installed `Packs/Lua.fpk`: `LuaRevision = 405907`,
`BuildVersion = '1.1.1.405907'`. So every save written on 1.1.1 carries 405907 and fails the
module's `< 405907`; every save written on 1.1.0 or 1.0.7 carries its own build number.

**Confirmed on the owner's own saves, read as bytes.** The live folder is the repo junction
`saves/game` (EF-110; `C:\Users\stkot\Saved Games\Surviving Mars Relaunched\<steamid>`, 63
files). Their metadata is plain text in the first few KB, and each mod entry inside
`active_mods` carries its own `lua_revision = 350453` (EF-077), so the save's field is the one
that stands beside `orig_lua_revision` (`scratchpad/save_meta.py`, no file loaded or copied):

| save (written) | `lua_revision` | `orig_lua_revision` | F121 handler |
|---|---|---|---|
| `Japan Sol 497 (Drone Hub Integrated)` (2026-09-23 12:56, game 1.1.1) | 405907 | 403908 | declines |
| `Autosave Sol 493` (2026-09-23 12:35, game 1.1.1) | 405907 | 403908 | declines |
| `C95PLACEMID`, `C95MID`, `C95BUILD` (2026-09-17, game 1.1.0) | 403908 | 403908 | accepts |

The two 1.1.1 rows also show the mechanism the builder argued from: a colony started on 1.1.0
keeps `orig_lua_revision = 403908` while an ordinary 1.1.1 save rewrites `lua_revision` to
405907, which is why the module keys on `lua_revision` and not on the original. Loading a
pre-1.1.1 fixture on 1.1.1 spends it on the next write; the peer-authored playtest plan says
to copy fixtures first.

**Healthy 1.1.1 events stay vanilla-owned; the legacy fixture heals.** desk-MEASURED
(`desk_c85_clogged.py`, 32/32): the native Duration thread built from the archived
`SetBuildingEnabledState:__exec` (`ClassDef-Effects.generated.lua:2772-2790`) survives a
current-save load and releases the building itself; six provenance values including `405907`
leave a healthy building alone; the legacy fixture is released once and idempotently; the
`16ff1aa` module reproduces F121 on the same fixture. Its `--selftest` fails all six
guard-reverted mutants.

**Challenge sound, residual named.** A healthy timed disable and an old stranded disable share
their saved fields (`OnScreenTimer` false, no building-owned handle), so provenance is the only
available discriminator. Two consequences the record should carry: (1) a pre-1.1.1 stranded
building whose save is first loaded on 1.1.1 without the pack and then re-saved is never
healed — deliberate, and narrower than the original F121 complaint; (2) the bound assumes no
build between 403908 and 405907 shipped the Duration; the archive holds only those two trees
and Steam's build history was not consulted.

## 5 · The sixteen retirements

**Replacement and consumer, traced.** All sixteen were re-derived on the archived tree by a
reader who opened the deleted module (`git show 16ff1aa:…`), the replacement body and the code
that reaches it, with the 1.1.0 body for contrast. Twelve are covered outright. Four carry a
note:

| module | note |
|---|---|
| `Fix_OpenPastureStockpiles` (C93) | **corrected — the settled gate is narrower than recorded.** The retail decline (`ck208on_…:135`) rests on the deleted probe (`16ff1aa:Code/Fix_OpenPastureStockpiles.lua:132-148`), which returns `false` at the *first* of `Resourcepile7..9` whose closed-entity range is missing or whose open-entity range exists. It proves `OpenPasture_Open` changed at one or more of the three spots, not that all three now exist. The Lua tree cannot show entity spots (`_EntityData.generated.lua` is byte-identical across the builds), and nothing native re-homes piles at runtime: `RebuildPastureStockpilePool` (`Animals.lua:1382-1560`) runs only from the two save fixups (`:1569-1583`). If a spot is still missing, a ranch opened after load can strand piles again with the module gone. The Lua and fixup half stands; the asset half is **unproven**. Records corrected: adjudication §0 and §3, C93's entry; **ck211** asks for the three `GetSpotRange` reads. |
| `Fix_FounderTraitNotification` (F23/F126) | covered by removal, not repair: the vendor deleted the feature. Not in the build's table but strengthening the retirement: `OnMsg.PostLoadGame` (`Notifications.lua:429-440`) deletes notifications whose preset no longer exists, so a 1.1.0 save's live `FounderGainsTrait` notification is cleaned on load. |
| `Fix_TrainCargoDumping` (F46) | covered for the defect. The module's "unload anyway if no station on the route accepts the resource" hatch has no native equivalent: such cargo now stays aboard. Vendor design, not a gap in the repair. |
| `Fix_TradeRocketFuelRefresh` (F119) | covered. The new gate (`IsRocketLanded()` in place of `IsPlayerControlled()`, `UniversalRocket.lua:1922-1926`) also stops refreshing a player rocket that has not landed; a vendor change this audit did not evaluate. |

Line leads that were off by an edge, left as leads: `Sinkhole.generated.lua` runs to `:26`;
the LawDef handler bodies are `:703-708` / `:905-910`; the `indestructible` check is
`Building.lua:1465`.

**References gone by name.** Over both repos, excluding `docs/archive` and `.git`, every one
of the sixteen names and its `Fix_` form was grepped, with `TrackSalvageWipe` as the positive
control (it hits `items.lua`, `metadata.lua`, its module and three TestKit probe files).
Live surfaces — `items.lua`, `metadata.lua`'s code list, root `README.md`, `docs/README.md`,
TestKit registrations and capture rows — hold zero hits. Four name lists were built at HEAD
and at `16ff1aa` (`Code/Fix_*.lua`, `SMRFixPack.Register` ids with the `FIX_ID` indirection
resolved, `items.lua` names, `metadata.lua` entries): the removed set is exactly the sixteen in
all four, nothing was added, and nothing else was removed. `README.md`'s changes are
hand-typed counts removed and the version line; the checklist lost ck193 (F21, retired) and
ck195's Mirror Sphere clause (F16, retired) while keeping F06. Two remaining live-surface hits
are not defects: ck207 cites `Fix_OpenPastureStockpiles` as evidence for an owner decision, and
`Code/Fix_FactionDomeSizeGate.lua:229` carries a comment naming `Fix_SinkholeIndestructible`
— stale, comment-only, a one-line hygiene item for the next code job (code is outside this
audit's authority). Every tool that names a retired module reads it from git `16ff1aa`
(`desk_c88_prefab.py`, `desk_c93_open_pasture.py`, `desk_f119_trade_fuel.py`,
`desk_c90_datapatch.py`, `desk_gamepatch_retirements.py`); none reads it from disk.

**History preserved, one gap.** Each of the sixteen entries gained a dated "build response"
block above "Historical filing and evidence"; nothing was erased. The gap: the F43 precedent
(owner ruling ck156) puts "⚖️ RETIRED <date>, module no longer ships" in the *title*, so
`bugs/INDEX.md` shows it. These sixteen rows still read `tested`/`fixed` with no marker —
F45 is a P1 `tested` row for a module that no longer ships. Not a wrong claim (the body says
so), so not corrected here; recommended for the next record pass.

## 6 · F122 / F123 / F126 two-sided controls

Read in `desk_gamepatch_retirements.py:84-235` and run by this seat (54/54): the pack-off
legs execute the archived native body — `Community:UICommandCenterStatUpdate` on an empty
and a populated dome, `GetRareTraitChance` with Gene Forging researched (50, and 150 with both
techs), and a `ColonistAddTrait` message with no handler and no constructor call. The pack-on
legs load the `16ff1aa` module through `git show` and reproduce the regression (red empty
dome; 100; the unknown-id assertion followed by the base-class instance). Each native body has
a scratch-broken mutant that fails. The earlier retail F123 pack-off short circuit is not
reused anywhere. Retail two-sided legs remain ck210 phase 3.

## 7 · Reconciliation, gates and reversals

**Reconciliation, by name, once, against the final state.** `gamepatch_111_census.py
--live-source` at `76c18ed` prints its members: disk = metadata = editor, 37 files; baseline
53 = surviving 37 + retired 16 by name; registered fixes 36 + core 1 = 37; TestKit 83 parsed
probes = 83 `Register` lines, retired rows absent; metadata differs only by the retired
entries; live game `1.1.1.405907`, Steam build `25390750`, live and archived source match the
manifest. `doccheck`'s MODULE SETS line agrees.

**Gates re-run by this seat at `76c18ed`.**

| command | result |
|---|---|
| `python tools/bodycheck.py --selftest` | PASS, every verdict fired |
| `python tools/bodycheck.py --src <archive 1.1.1> --all` | 148 OK, 9 SRC-NONE, 3 BODY-CHANGED, 1 DEFECT-GONE, 1 NO-DEFECT; exit 1 — diagnosed below |
| `python tools/patchcheck_selftest.py` | GREEN |
| `python tools/doccheck.py` | GREEN (37 files, 36 modules, 83 probes) |
| `desk_f124_track.py` / `desk_f125_vacuum.py` / `desk_c85_clogged.py` (+`--selftest`) | 28/28 · 25/25 · 32/32, six mutants red |
| `desk_gamepatch_retirements.py` / `desk_migration_cluster.py` (+`--selftest`) | 54/54 · 16/16, selftest PASS |

The `bodycheck --all` red is the standing pre-build state, not a build regression: the five
non-OK rows are `Fix_HabitatExpeditionDraft`, `Fix_HabitatExpeditionReturn` and
`Fix_RocketInteractGuard` (BODY-CHANGED under wrappers, read and confirmed KEEP in the
adjudication §6), `90_SaveSanitizer` (DEFECT-GONE, triaged in D14) and `00_Core`
(NO-DEFECT, the FIX_POLICY §2b exception). None of those files is in the commit range. The
builder's per-module runs were scoped to its six modules and green, which is consistent.

**Controls shown able to fail — this seat's own reversals, in scratch copies, production
bytes hash-checked unchanged.**

| scratch mutant | control | result |
|---|---|---|
| track: F44 anchor fallback removed | curved split and physical refund | red |
| track: F91 shell deletion removed | whole salvage refund and shell cleanup | red |
| clogged: provenance bound `<` → `<=` 405907 | (g2) `405907` untouched, (g3), (g4), (k) | four legs red |
| vacuum: direct distance not raised | direct vacuum final leg receives the real passage path | red, intermediate still green |
| vacuum: intermediate `-1` not forced | intermediate leg traverses its passage | red, direct still green |

Scripts: `scratchpad/revert_track.py`, `revert_clogged.py`, `revert_vacuum.py` (session
scratch, not committed).

## 8 · The builder's challenges

1. **F121 needs a saved-provenance condition.** Sound (§4). Residual named there.
2. **F125 by input wrappers, revising the F52 design note.** Sound (§3). F52's entry records
   the changed decision as a dated section and keeps the 1.0.7 and 1.1.0 history; no
   correction needed.
3. **F126's consumer asserts before the fallback.** Sound: the corrected control runs the
   archived `AddNotification` and `PropertyObject:CreateInstance`, models EF008's
   report-and-continue assert explicitly, and a weakened-assert scratch variant loses the
   diagnostic (measured, §6).
4. **C55's duplicate-geometry premise may be obsolete.** Not acted on by the build and not
   adjudicated here: C55 is a `cand` entry outside the range. The lead stands — native
   processing now excludes repair sites (`Track.lua:466-474`), so C55's "walk comes up short"
   premise should be re-read on 1.1.1 by whoever next opens it.

**Silence.** The builder raised nothing on the 33 KEEP rows, the severity ranking or the
bounded retail A/B, as the brief expected. The one over-read this audit found (C93's gate) sat
in the adjudication and the deleted build brief, and neither the builder nor its internal
reviewers questioned it. The KEEP rows keep their surface-pass status.

**Departures 1 and 2** changed how a repair was built, not whether: confirmed. No disposition
was reversed.

## 9 · Records corrected in this commit

- `GAMEPATCH_1.1.1_ADJUDICATION_2026-09-23.md`: §0 Open Pasture row and a dated paragraph in
  §3 (the gate is narrower than written; asset half unproven).
- `docs/agent/bugs/C93.md`: an audit paragraph in its 2026-09-23 build-response block.
- `docs/PLAYTEST_CHECKLIST.md`: ck209 deleted (this audit is the owner's action on it);
  **ck211** opened — three console reads that decide the C93 retirement.
- `docs/agent/prompts/GAMEPATCH_1_1_1_FIX_AUDIT_high.md` and its map row deleted.
- No entry status was changed.

## 10 · What is safe to ship, what is owed to play, what is still wrong

- **Safe at the desk:** all three rebases and the sixteen deletions. Nothing in the shipped
  code was found wrong; every behaviour claim the build made was confirmed on the archived
  source or by a harness this seat ran, except the C93 asset half, which is unproven.
- **Owed to play:** ck210 (unattended single-variable legs, the old-save and remove-and-load
  round trips, repair-site salvage, direct and intermediate vacuum routes, the three retail
  two-sided reads, the F121 fixture) and ck211 (three `GetSpotRange` reads; a `-1` reopens
  C93 as FIX). ck211 is the only leg that can send a retirement back.
- **Still wrong or open:** the C93 asset half; the sixteen INDEX rows without a retirement
  marker; the stale comment in `Fix_FactionDomeSizeGate.lua:229`; the C55 lead.
- **Not opened:** the vendor's player-rocket refresh gate; whether `assert` prints in a retail
  log; engine geometry, scheduling and thread serialization behind every desk shim; whether
  any of the owner's pre-1.1.1 saves actually holds a stranded clogged building (only their
  revision fields were read).
- **Claim limits.** Nothing here is retail-verified. The desk harnesses stub geometry, object
  lifetime, commands and reservations; they measure delegation, exclusion and branch choice,
  not the engine. Retail statements inherit the completed A/B's limits: not single-variable,
  neither leg at zero errors. A matching body hash is not compatibility; a passing gate is not
  a correct build. The release surfaces (store copy, site fix list, version) remain the
  previous release's, as the outbox entry says.
