# HOTFIX 1 — AUDIT REPORT (link 2 of 2, terminal)

**VERDICT: SHIP WITH CHANGES — text only. Two player-surface sentences should be reworded before the upload sitting; no code changes. If the owner declines both, the code ships safely as it stands.**

Audited 2026-09-08 by a fresh session (`smr-bugfixpack-6c`) that did none of the
implementation. Brief: `prompts/HOTFIX_1_AUDIT.md`. Tree at `09f11cc`, clean.
Game source read: the shipped 1.1.0 tree at `A:\SteamLibrary\...\ModTools\Src`
(mtime 2026-09-08). The 1.0.7 tree does not exist anywhere on this machine
(checked `ModTools\Src`, `C:\Dev\workshop_fpk_archive`, `C:\Dev\_ref`, git).

## 1 · Findings, most severe first

Nothing was found in the six code changes. Every finding below is a wording or
a documentation defect. Numbered for the checklist.

### F-1 (medium, player surface, re-posted by this upload) — the store description's self-check sentence was falsified by 1.1.0

`metadata.lua` `description`, HOW IT WORKS bullet 3, verbatim:

> Every fix checks the game's code before it touches anything, and stands down
> by itself if an official patch changes what it was written for. A fix that
> stands down does nothing at all — it never guesses.

**What is wrong.** The self-checks test whether a target *exists*
(`00_Core.lua` `Require`: `rawget`/`type` on a name, class, method or path).
They cannot see a same-name body or signature change. F114 (157 throws in one
session) and F115 (engine mod-error dialog) are two fixes that did **not** stand
down when an official patch changed what they were written for. The sentence is
a general promise the pack cannot keep, and `00_Core.lua`'s own HONESTY LIMIT
comment says so.

**How I know.** `Require` at `00_Core.lua:118-166`; F114/F115 measured in
`archive/logs/f114repro110_*` (159 error headers, zero self-disables for either
module); `sigcheck.py` rates 52 of 54 replacement sites OK by name+arity while
one of them (`TrackSalvageWipe`) has a changed body.

**Why it matters now.** Every upload overwrites both store page bodies from
`description` (`ParadoxMods.lua:158`, `SteamWorkshop.lua:110`), so the hotfix
upload re-posts this sentence beside a changelog that admits two fixes broke
players' games on the new version. A player who reads both sees the contradiction.

**Cost to a player.** Credibility, not gameplay. But it is the exact class of
overclaim the brief says would do real damage.

**Recommended wording** (owner-worded surface, approved verbatim in 22d(1), so
it is theirs to change — checklist 112):

> Every fix checks the game's code before it touches anything, and stands down
> by itself if the code it was written for has been renamed or removed. That
> check cannot see every kind of change, which is why each game update gets a
> compatibility pass. A fix that stands down does nothing at all — it never
> guesses.

Surfaces to sync if changed: `metadata.lua`, `docs/UPLOAD_WORKFLOW.md` §3 (both
the plain and the BBCode form, lines 144-146 and 236), `reports/STORE_CARD_LIVE.md`
(lines 182-184 and 280). The site repo carries no copy of the sentence (grepped).

### F-2 (low, player surface) — the patch note overstates the F116 repair

`last_changes` bullet 3: "One track-salvage fix was also brought in line with
the new game code."

**What is wrong.** "Brought in line" reads as parity. `Fix_TrackSalvageWipe`
now matches 1.1.0 at two points and deliberately diverges at two others
(orphan policy `TrackElement.lua:580-595`; combined post-split processing
`:609-613`), and the repair has never run in a game. Under the owner's own
rule a "done" claim about untested code is a claim.

**Recommended wording:** "One track-salvage fix was also updated for the new
game code." Same length, no parity claim. Sync `UPLOAD_WORKFLOW.md` §3 line 267.

### F-3 (low, evidence quality, non-blocking) — bullet 1's "Fixed" is confirmed by construction, not by play

"Fixed for game 1.1.0: trains that would not leave their station, and an error
popup when landscaping."

**What holds.** Both modules report `inactive` with their gate's own reason
on the owner's shipped-config boot, so neither body is installed and neither
throw can occur. That is stronger than a sample. The 1.1.0 vanilla bodies then
run, and the reporter's own A/B says vanilla trains move.

**What does not hold yet.** No 1.1.0 colony has been played with the gated
pack. If a second module also stalls trains, bullet 1 is wrong. The other ten
train/track modules are name-clean and two of the three body copies are diffed
(`TrackSalvageRefund` clean, `TrackSalvageWipe` = F116, demolish path), so a
second cause is unlikely, not excluded.

**Recommendation.** One in-play check on the colony the owner already
provisioned (BlankBig_02): load, watch the first train leave its platform,
assign the second. About five minutes, and it is the one thing the owner can
*see*. Non-blocking: skipping it risks a wrong patch note, not a harmed player.

### F-4 (low, not shipped) — the Test Kit's override header misstates what it re-arms

`SMR-BugFixPack-TestKit/Code/97_ForceInactive.lua:37-43` says forcing will
re-arm F113, F114 and F115. It re-arms **F113 only**. `make_forcing_require`
(`:85-104`) honours every `test` spec that returns false, and both the F114
gate (`Fix_TrainCargoDumping.lua:68-71`) and F115's belt
(`Fix_LandscapeUnitFilter.lua:98-99`) are `test` specs, so under force both
modules log "content check still honoured" and stay inactive. That is the safe
direction, and the Test Kit never ships. Fix the comment when the file is next
touched; nothing in the patch depends on it.

### F-5 (info) — two stale internal comments, no action needed for the upload

- `metadata.lua` comment above `last_changes`: "do not upload this string until
  a 1.1.0 boot reads the predicted 17 inactive / 14 named" is satisfied
  (`archive/logs/gated110_*`).
- `EF-081` says a forced boot refuses 5 modules; with the F114 and F115 `test`
  gates it would now refuse 7. The fact is dated and correct for its boot.

## 2 · What I verified, and what I could not

### Verified — routes re-derived from the shipped 1.1.0 tree, not inherited

**F115 gate (`Fix_LandscapeUnitFilter.lua:84-111`).**
- `Landscaping.lua:21` is `MapVar("Landscapes", {})`; it is the only definition
  of that name in the tree. `:509` is `LandscapeForEachUnit(map, mark,
  callback, ...)`, `:510` reads `map.Landscapes[mark]`, and `:522` still passes
  `callback` instead of `filter_embark`, so F34(d) is still a live vanilla defect
  and the fix is still wanted.
- `lib.lua:1061-1076` `GameVar` rawsets the global to `false` at registration
  (`:1069-1071`); `:984-1000` `MapVar` writes `MapVars`/`MapVarValues`/
  `PersistableMapVars` and never `_G`. `MapVarValues["Landscapes"]` is a
  function (table values are wrapped, `:985-992`), so the belt's `~= nil` test
  is sound.
- `autorun.lua:431-434`: `dofolder("Lua")` → `DlcsLoadCode()` →
  `ModsLoadCode()`. `Register` calls `run_apply` inline and `run_apply` runs
  `pcall(def.apply)` immediately, so the checks run after every top-level
  `MapVar` in the game tree has executed.
- Composition: `Require` walks the spec in order and returns on the first
  failure. The `{ global = "Landscapes", kind = "any" }` spec is entry 3, the
  `test` is entry 4. `ok = (kind == "any") and v ~= nil or type(v) == kind`
  parses as `((any and v~=nil) or type(v)==kind)`, which is nil-vs-not-nil for
  `kind = "any"`. On 1.1.0 the primary fails and declines; the belt is only
  reached if a foreign global named `Landscapes` exists, and then
  `MapVarValues` is necessarily populated and it declines too. The brief's
  directional-redundancy argument holds.
- The `update_suspect` route: the primary is a shape spec, so `Require` marks
  natively (`00_Core.lua:157-163`); the belt's branch is hand-marked at
  `:107-110`. Measured: named in the 14-module report on both 17:xx boots.
- **The 1.0.7 half, re-derived from our own verbatim copies rather than from
  the "it was a GameVar" record.** Two independent pieces of 1.0.7 vanilla code
  index `Landscapes` as a bare global: our replacement body (a verbatim copy of
  1.0.7 `Landscaping.lua:455-469`, `Fix_LandscapeUnitFilter.lua:122`) and
  `ClearWasteRockConstructionSite:GameInit` as cited in `bugs/F34.md` (:60-63).
  A bare-global read that did not throw on 1.0.7 means the key existed in `_G`
  on 1.0.7, whether by `GameVar`, `GlobalVar` or assignment. F34(d) is
  `fixed*` with an attended witness of the module running on 1.0.7. So the
  primary passes on a 1.0.7 tree; the belt passes there too because `MapVar`
  asserts on a duplicate name, so `Landscapes` cannot have been both. Not a
  re-read of the 1.0.7 source, but a route, and it is the same route the
  defect ran on.
- Detects the storage move, not the arity change: true, and stated at
  `Fix_LandscapeUnitFilter.lua:60-67` and `EF-082`. Acceptable for a gate
  whose failure direction is decline.

**F114 gate (`Fix_TrainCargoDumping.lua:68-83`).** `DefineClass.
MultiResourceDepotBase` at `MultiResourceDepot.lua:8`; `Station.__parents`
lists it at `Station.lua:51`. The three earlier specs pass on 1.1.0 (the logged
reason is the `test`'s). Hand-written `update_suspect` mark confirmed in the
boot's named list. 1.0.7 half rests on the F46 header's citation of
`UniversalStorageDepotBase` and on the name appearing nowhere in the
project's pre-09-08 history; bounded downside if wrong is F46 quiet on 1.0.7.

**F113 gate (`Fix_LanderCargoRatchet.lua:91-92`).**
`GetEarthExportResPossibleReward`: 0 hits tree-wide. `CreateAutoCargoRequest`
rewritten at `UniversalRocket.lua:2028`; `GetEarthAutomodeFundingState` at
`:1959`. `{class, method}` form, marked natively, measured named.

**F112 gate (`Fix_AutomationLawCompensation.lua:252-256`).** `law_scale`: 0
files tree-wide. `automation_workforce_reduction`: only
`Data/LawDef/LawDef-Technology.lua`. `Workplace:GetWorkersPerformance` at
`Workplace.lua:250`. `test` form, so inactive and unnamed: measured on the
15:57 boot. Correct by design; not to be "fixed" into the dialog. 1.0.7 half:
our C39 and F108 headers place the per-worker loop inline in
`GetWorkshiftPerformance` at 1.0.7 `Workplace.lua:219-228`, which is
incompatible with an extracted `GetWorkersPerformance` existing then.
Records, not a re-read; bounded downside is C39 quiet on 1.0.7.

**F111 guard (`Fix_ExtractorStaffedPerformance.lua:76`).**
`Workplace:IsOvertime` `:718-729` collapses the table and writes it back
(`:726`); class default `overtime = false` (`:21`); `GetWorkersPerformance`
adds the overtime additive at `:263-265`; `GetWorkshiftPerformance` takes
`Max(performance, auto_performance)` at `:285-287`. `Colonist:GetWorkPerformance`
is `Max(self.performance, 25)` (`Colonist.lua:794-796`), byte-equivalent to our
inline term, so on 1.1.0 `staffed` can never exceed `orig`'s answer and the
wrapper is inert. `type(...) == "table"` is the shipped test on a 1.0.7 table
and a short-circuit on a 1.1.0 boolean. Correct on both shapes; changes no
outcome on either. Guard trigger unreached in play.

**F116 repair (`Fix_TrackSalvageWipe.lua:105-140`).** Ruled separately in §5.
Route verified: see there.

**Decision 110.** `git diff ce77162 HEAD -- Code/00_Core.lua` is empty, and
`00_Core.lua` is absent from `git diff 7863f3d HEAD --stat` (the v5 close-out
commit), so it is byte-identical to the shipped v5 file. The full diff against
v5 is `Fix_AutomationLawCompensation`, `Fix_ExtractorStaffedPerformance`,
`Fix_LanderCargoRatchet`, `Fix_LandscapeUnitFilter`, `Fix_TrackSalvageWipe`,
`Fix_TrainCargoDumping` and `metadata.lua`. `items.lua` untouched (no module
added, H-10 satisfied). The Test Kit's `apply_forced` reproduces `run_apply`'s
three branches exactly (error / string → inactive / else active + installed +
`update_suspect = nil`); no drift today.

**Boot reconciliation (§2b).** `python tools/logscan.py --build 6a91a190`
over all eight 1.1.0 logs. The live `Mars.exe-20260908-17.51.09` file is
byte-identical to `archive/logs/gated110_*` (diff empty), ends with
`Debug::Done()` at 117,704 ms, and has zero game-load lines: a complete,
post-exit, menu-only log. Reading: 63 applied / 17 inactive / 14 named, 0
error-shaped lines, `TrainCargoDumping` and `LandscapeUnitFilter` both in the
named list. An earlier boot two minutes before it (`17.49.54`, 222 lines,
68 s, clean exit, not archived) reads identically. Prediction met exactly; no
unexplained line in either. Every error-shaped line in the other six logs is
attributed in `EF-081` (LowStorageWarning under force, 6×) and `bugs/F114.md`
/ `F115.md` (157 + 2 on the 15:57 session, pre-gate). None discounted.

**Patch notes (§2d).** `last_changes` names no fix id, no count, no other mod,
gives no load-order advice, makes no save-safety claim, and does not claim
1.1.0 compatibility. The only "you can" is "please keep reporting", whose
route (tracker, store comments) is on the description. `UPLOAD_WORKFLOW.md` §3
lines 265-267 match `metadata.lua` verbatim. Findings F-1 and F-2 above.

**Instruments.** `sigcheck.py`: 54 sites, 1 MISMATCH (F115, correct and
deliberately left), 1 ABSENT (`TouristSatisfaction`, self-disabled), 52 OK.
`doccheck` GREEN before this session's edits.

### Not verified — a thing not checked is not a thing that passed

- **Any 1.0.7 source.** Gone (`EF-075`). Every "on 1.0.7 this passes" above
  is a route through our own recorded copies, never a re-read.
- **Anything in play on 1.1.0 with this patch.** Trains, landscaping, track
  salvage, the F111 trigger (staffed automated extractor with overtime), an
  automation law (F112), an automode rocket at Earth (F113). All unexercised.
- **The F116 repair has never executed.** `applied` in a boot log proves the
  module loaded, not that the added call does what the source says.
- **The foreign-global scenario for F115** is reasoned, not tested.
- **The 17 undiffed body replacements.** Out of this audit's scope; §6.
- **Whether the "22" is the right count.** `PACK_1_1_0_REVERIFICATION.md`
  itself says "~21". A mechanical census of `Code/` finds 19 files defining a
  function with no `local orig` capture, several of which are `OnMsg` handlers
  or pack helpers, not replacements. The set needs a proper enumeration before
  anyone diffs it.
- **Portal behaviour of the upload** (description length, auto-fill). Not this
  link's job; `UPLOAD_WORKFLOW` §3 backups are in place.

## 3 · Decision 110 — ruled: actioned cleanly

The override surface does not ship. Verified by diff, not by reading the
commit message: `Code/00_Core.lua` is byte-identical to the shipped v5 file;
the pack's diff against v5 is exactly the six expected files plus
`metadata.lua`; the mechanism lives wholly in the Test Kit and works from
outside by swapping `SMRFixPack.Require` around a re-apply, with a hand-copied
verdict handler that matches `run_apply` today. One documentation defect in
the Test Kit header (F-4), zero reach to a player. Clean.

## 4 · Position on §2e — ship first; the 17 diffs are the next job, not a gate on this one

**Ship.** Reasoning:

1. The 17 undiffed bodies are already on every 1.1.0 player's machine at v5.
   Holding the hotfix does not reduce that exposure by one module. It only
   keeps F114 in every colony with a train and F115 on every landscaping site,
   today.
2. The hotfix subtracts code (five gates/guards) and adds one call that vanilla
   1.1.0 itself makes at the same point (§5). Its own risk surface is small and
   was measured at boot.
3. The 3-in-5 hit rate is a real signal about the *remaining* set, and the
   honest response is the patch-note line that already ships ("a safety pass,
   not a full re-check"), plus the commitment below.

**The commitment.** Before any further upload:
- Run `prompts/PACK_1_1_0_REVERIFICATION.md` pass 1, but first enumerate the
  replacement set mechanically (the count is approximate; see §2) so the pass
  has a closed list.
- Each body diffed structurally against `ModTools\Src` (comments stripped, not
  a keyword count: the F116 lesson).
- Every game patch from now on repeats that diff before the pack is called
  compatible. Nothing the pack owns can substitute for it.

What would change my position: a *second* player-visible breakage in a module
that is not one of the six, arriving before the upload. That would say the
remaining set is hotter than 3-in-5 and the safety pass should widen first.

## 5 · F116 — ruled: keep the repair, do not gate, leave both divergences

**The crux, re-derived.** Our body's four tail `ProcessTrackElements` calls
(`Fix_TrackSalvageWipe.lua:342-355`) are the post-split step, inside the split
branch only, after the sort. 1.1.0's `:473-476` call runs before `all_elements`
is built and before the sort, on every path including both trim branches and
the `mass_delete` return. Settled by reading both bodies, not by counting.

**Does its absence change the deletion set?** Yes, on the merge route, which I
walked:
- `node_idx` is stamped from `track_obj.last_node_idx + 1` at build
  (`Tracks.lua:370-371`, `:393-401`), a counter, not a distance.
- `TrackGridElement:AutoConnectTracks` (`TrackElement.lua:328-441`) merges a
  track into an existing one and restamps completed elements from
  `#track.elements` (`:419`) and under-construction ones from
  `#track.elements_under_construction` (`:424`). Two sequences that both start
  low collide; the repair via `ProcessTrackElements` runs only when
  `#track.elements_under_construction == 0` (`:430-432`).
- `ProcessAllElements` (`Track.lua:466-469`) concatenates both arrays and
  `OrderTrackElements` restamps `el.node_idx = i` in walked order
  (`Tracks.lua:579`, `:633`). `RebuildIndexes` (`Track.lua:471-504`) is not a
  general revalidation: `TryConnectStations` calls it only when
  `elements[1].node_idx` is falsy (`:522-523`).
- With colliding keys, `table.sort` at our `:177` orders by a stale key and the
  zone math (`:218-230`, `:281`) deletes a physically scattered set. The entry's
  mechanism holds.

**The guard, not a `Require` spec.** Correct trade. A spec would decline the
module wherever `ProcessAllElements` is absent, and the cost is verified live
in vanilla 1.1.0: the F44 walk-off at `TrackElement.lua:504-509` is unchanged,
both short-remainder `OnDemolish` calls survive (`:528-531`, `:542-545`), and
`TrackBase:OnDemolish` (`Track.lua:248-284`) still never reaches `DoneObject`
(F91). F44 is a store-card headline. Gating would hand it back to every 1.1.0
player to remove a divergence that has never produced a throw, a log line or a
report. The capability guard degrades to the pre-repair behaviour on an older
tree instead. Right call.

**Does it pin us to 1.1.0's body?** It pins us to one vanilla call, guarded.
The module was already a 1.0.7 body over whatever the game ships; every one of
the replacements is, and the next patch re-breaks any of them silently. The
mitigation for that is the §4 commitment, not a gate on this module alone.

**The two divergences left in.** Right to leave both in a safety pass:
- Orphan policy: ours deletes, 1.1.0 rehomes (`:580-595`). With the pre-sort
  restamp in place, orphans arise only when the track is already physically
  disconnected, which is also when `OrderTrackElements` bails without
  restamping (`Tracks.lua:615-620`, `ProcessTrackElements` `:818-819`) and
  our F45 guard returns before deleting anything. Changing destructive,
  playtest-derived logic with no reproduction is the larger risk. Item 111
  stands as written; I agree with (a) now, (b) later with a colony.
- Post-split processing on a mixed track: inherited 1.0.7 behaviour, no harm
  on record. Leave.

**What `applied` does not prove.** The repair has never run. The control in
`bugs/F116.md` (build, extend during construction, salvage a middle element,
pack on vs off) is the only thing that would, and it needs a provisioned 1.1.0
colony. `sigcheck` rates the module OK before and after; that rating must
never appear in a patch note as evidence.

## 6 · For `PLAYTEST_CHECKLIST.md` → "Decisions waiting on you"

- **112.** Reword the description's self-check sentence (F-1) before the
  upload, or leave it. Proposed text in F-1. Owner-worded surface, so the call
  is theirs.
- **113.** Reword `last_changes` bullet 3 (F-2): "brought in line with" →
  "updated for". Text only.
- **Pre-upload check, not a decision (F-3):** five minutes on BlankBig_02
  watching the first train leave and the second assign. Recommended, not
  required.

## 7 · Bindings honoured

No code edited. No game launched. No Mod Editor, no `version` edit, no upload,
no portal API. Game directory untouched. No 1.0.7 citation corrected.
`doccheck` result and any WARN are in the session summary verbatim.
