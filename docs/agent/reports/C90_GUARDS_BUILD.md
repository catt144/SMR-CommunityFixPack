# C90 guards build — 2026-09-12

Owner authority: checklist 158, v10 carries module-local apply-success guards in
Saint and Sinkhole. Baseline HEAD: `fb3751a`. Production changes are confined to
`Code/Fix_SaintBlessing.lua` and `Code/Fix_SinkholeIndestructible.lua`.

**SOURCE:** each local flag begins false, is set true only after Require clears,
and is checked before any pass target lookup. No shared-core or version test was
added. A failed apply cannot write preset/class data, arm Saint's repair, or heal
away the failed self-check. No field target-loss trigger is established.

**SOURCE — reset/retry claim REFUTED on the current path:** core run_apply is called
at Register (`00_Core.lua:525`) and optional reconciliation (`:558`), with the latter
inside `def.optional` (`:539`). All three relevant definitions (C89, Saint,
Sinkhole) omit optional. Register replaces entry/definition before applying
(`:513-514`). A normal Lua reload executes the file-local false initialiser and
creates the new pass closure before Register. Thus a successful apply cannot be
followed by a declining engine retry retaining the same flag in these modules.
C89 matches the current ordering and remains unchanged, retaining its attended
status. If a future optional/direct retry path is added, reset before Require.
Direct console invocation or externally mutating defs is outside this engine-path
finding. Registry status is still unsuitable as an apply-time gate because
run_apply assigns it only after apply returns (`:460-485`). This is source evidence,
not a measured engine reload sequence.

**MEASURED:** original harm/stop demands are retained verbatim in historical_main,
loading actual pre-guard modules from `fb3751a`. live_main exercises the same
missing-target matrix, intact branches and vetoes against production guards;
it requires zero writes, no new pass logs or save-repair arming, inactive status
and a retained update suspect after decline. The original scratch falsifiers run
on historical bodies; separate live guard removals must resurrect the bypass.
Full output below records every assertion and command exit.

**Status: fixed; ships unexercised in play**, following ck158/ck130. No Mars.exe
was running at the separate pre-edit tasklist check. No game was launched; a
healthy-install boot would not exercise missing-target guards. No save repair
execution, engine flattening, naturally failing update, reload/idempotency matrix
or logscan detection is claimed. Existing write-proxy rawget limitation remains.

C90 has no public row and changes no registered module set or count. The outbox
names both changed modules for release accounting. Checklist 158 remains
`<!-- ck:158 status:closed owner:no -->`; this build closes no new owner decision.
The consumed prompt is removed and its map row records the grave commit.

**By-name exclusions:** C89 back-port (retry claim refuted; attended module),
shared core and OnDataReady (unruled scope), C91 (separate work), retirement lane
items.lua/metadata.lua/F37/F43/F118/F31 and their modules (sibling fence),
STATE eviction (held until v10 live), Mod Editor/version edits, upload and site
deployment (outside this build). No other repository or source tree was edited.

**Bodycheck limitation:** the global command exits 1 on DEFECT-GONE in
`90_SaveSanitizer.lua:82` (Station fixup ResolveMap expression). Its source is
unchanged from the baseline. Both changed modules are checked separately below;
their manifests and existing named exceptions are preserved. No sanitizer repair
or bodycheck clearance is claimed.

Landing receipt: the commit containing this report is emitted by
`git log -1 -- docs/agent/reports/C90_GUARDS_BUILD.md`; its SHA is supplied in the
owner handback, since a commit cannot contain its own hash.

## Control transcripts

### `python tools/parsecheck.py` ? exit 0

```text
PARSE: 50 file(s) in Code, 0 error(s) [Lua 5.5]
```


### `python tools/desk_c90_datapatch.py` ? exit 0

```text
==============================================================================
C90 actual core: decline, ordered writes, and healing of status
==============================================================================
lua: Lua 5.5 | lupa 2.8

  PASS  1.0.7 Saint intact: exact writes and status  -- active -> active; ['Saint.modify_trait=TraitReligious']
  PASS  1.0.7 Saint GetTraitLabel: exact writes and status  -- inactive -> inactive; []
  PASS  1.0.7 Saint TraitPreset.AddDomeColonistsModifier: exact writes and status  -- inactive -> inactive; []
  PASS  1.0.7 Saint LabelContainer.SetLabelModifier: exact writes and status  -- inactive -> active; ['Saint.modify_trait=TraitReligious']
  PASS  1.0.7 Saint failed self-check is erased from UpdateSuspects
  PASS  1.0.7 Saint veto stops the pass
  PASS  1.1.0 Saint intact: exact writes and status  -- active -> active; []
  PASS  1.1.0 Saint GetTraitLabel: exact writes and status  -- inactive -> inactive; []
  PASS  1.1.0 Saint TraitPreset.AddDomeColonistsModifier: exact writes and status  -- inactive -> inactive; []
  PASS  1.1.0 Saint LabelContainer.SetLabelModifier: exact writes and status  -- inactive -> active; []
  PASS  1.1.0 Saint failed self-check is erased from UpdateSuspects
  PASS  1.1.0 Saint arms the save re-base despite decline
  PASS  1.1.0 Saint veto stops the pass
  PASS  Sinkhole intact: exact ordered writes and status  -- active -> active; ['class.indestructible=true', 'template.indestructible=true']
  PASS  Sinkhole class: exact ordered writes and status  -- inactive -> inactive; []
  PASS  Sinkhole DestroyBuildingImmediate: exact ordered writes and status  -- inactive -> active; ['class.indestructible=true', 'template.indestructible=true']
  PASS  Sinkhole failed self-check is erased from UpdateSuspects
  PASS  Sinkhole veto stops the pass

==============================================================================
18 of 18 demands held
ALL DEMANDS HELD -- injected target loss, not a field reproduction.
==============================================================================
C90 live guards: declined apply cannot write, arm, or heal
==============================================================================
lua: Lua 5.5 | lupa 2.8

  PASS  1.0.7 live Saint intact: exact writes and status  -- active -> active; ['Saint.modify_trait=TraitReligious']
  PASS  1.0.7 live Saint GetTraitLabel: exact writes and status  -- inactive -> inactive; []
  PASS  1.0.7 live Saint TraitPreset.AddDomeColonistsModifier: exact writes and status  -- inactive -> inactive; []
  PASS  1.0.7 live Saint LabelContainer.SetLabelModifier: exact writes and status  -- inactive -> inactive; []
  PASS  1.0.7 live Saint preserves failed self-check in UpdateSuspects
  PASS  1.0.7 live Saint veto stops the pass
  PASS  1.1.0 live Saint intact: exact writes and status  -- active -> active; []
  PASS  1.1.0 live Saint GetTraitLabel: exact writes and status  -- inactive -> inactive; []
  PASS  1.1.0 live Saint TraitPreset.AddDomeColonistsModifier: exact writes and status  -- inactive -> inactive; []
  PASS  1.1.0 live Saint LabelContainer.SetLabelModifier: exact writes and status  -- inactive -> inactive; []
  PASS  1.1.0 live Saint preserves failed self-check in UpdateSuspects
  PASS  1.1.0 live Saint does not arm save re-base after decline
  PASS  1.1.0 live Saint veto stops the pass
  PASS  live Sinkhole intact: exact ordered writes and status  -- active -> active; ['class.indestructible=true', 'template.indestructible=true']
  PASS  live Sinkhole class: exact ordered writes and status  -- inactive -> inactive; []
  PASS  live Sinkhole DestroyBuildingImmediate: exact ordered writes and status  -- inactive -> inactive; []
  PASS  live Sinkhole preserves failed self-check in UpdateSuspects
  PASS  live Sinkhole veto stops the pass

==============================================================================
18 of 18 demands held
ALL LIVE GUARDS HELD -- desk evidence; ships unexercised in play.
```


### `python tools/c90_scratch_verify.py` ? exit 0

```text
EXPECTED FAIL: runner suppressed (exit 1)
  1.0.7 Saint LabelContainer.SetLabelModifier: exact writes and status
  1.0.7 Saint failed self-check is erased from UpdateSuspects
  1.0.7 Saint intact: exact writes and status
  1.1.0 Saint LabelContainer.SetLabelModifier: exact writes and status
  1.1.0 Saint arms the save re-base despite decline
  1.1.0 Saint failed self-check is erased from UpdateSuspects
  1.1.0 Saint intact: exact writes and status
  Sinkhole DestroyBuildingImmediate: exact ordered writes and status
  Sinkhole failed self-check is erased from UpdateSuspects
  Sinkhole intact: exact ordered writes and status
EXPECTED FAIL: veto removed (exit 1)
  1.0.7 Saint veto stops the pass
  1.1.0 Saint veto stops the pass
  Sinkhole veto stops the pass
EXPECTED FAIL: heal removed (exit 1)
  1.0.7 Saint LabelContainer.SetLabelModifier: exact writes and status
  1.0.7 Saint failed self-check is erased from UpdateSuspects
  1.1.0 Saint LabelContainer.SetLabelModifier: exact writes and status
  1.1.0 Saint failed self-check is erased from UpdateSuspects
  Sinkhole DestroyBuildingImmediate: exact ordered writes and status
  Sinkhole failed self-check is erased from UpdateSuspects
EXPECTED FAIL: Saint label-existence guard removed (exit 1)
  1.0.7 Saint GetTraitLabel: exact writes and status
  1.1.0 Saint GetTraitLabel: exact writes and status
EXPECTED FAIL: Saint behaviour refusal removed (exit 1)
  1.0.7 Saint TraitPreset.AddDomeColonistsModifier: exact writes and status
  1.1.0 Saint LabelContainer.SetLabelModifier: exact writes and status
  1.1.0 Saint TraitPreset.AddDomeColonistsModifier: exact writes and status
  1.1.0 Saint arms the save re-base despite decline
  1.1.0 Saint intact: exact writes and status
EXPECTED FAIL: Sinkhole class guard removed (exit 1)
  Sinkhole class: exact ordered writes and status
EXPECTED FAIL: C89 apply-success guard removed (exit 1)
  (k) NEGATIVE -- a module registered but never applied patches nothing
  (k2) NEGATIVE -- a module whose self-check DECLINED patches nothing, even though DataPatch's runner still fires its pass
  (m3) Report() with the fix NOT applied says shipped=not-wrapped and does NOT claim the gate is active -- the owner cannot bank a false PASS
EXPECTED FAIL: F60 harmful argument removed (exit 1)
  F60 patch reports all 3 applicants housed while arrival space gate rejects home
  F60 patched tally counts 3 but migration gate still rejects
All 8 scratch variants failed as required; 18/18 C90 demands falsified.
EXPECTED FAIL: live SaintBlessing apply-success guard removed (exit 1)
  1.0.7 live Saint GetTraitLabel: exact writes and status
  1.0.7 live Saint LabelContainer.SetLabelModifier: exact writes and status
  1.0.7 live Saint TraitPreset.AddDomeColonistsModifier: exact writes and status
  1.0.7 live Saint preserves failed self-check in UpdateSuspects
  1.1.0 live Saint GetTraitLabel: exact writes and status
  1.1.0 live Saint LabelContainer.SetLabelModifier: exact writes and status
  1.1.0 live Saint TraitPreset.AddDomeColonistsModifier: exact writes and status
  1.1.0 live Saint does not arm save re-base after decline
  1.1.0 live Saint preserves failed self-check in UpdateSuspects
EXPECTED FAIL: live SinkholeIndestructible apply-success guard removed (exit 1)
  live Sinkhole DestroyBuildingImmediate: exact ordered writes and status
  live Sinkhole class: exact ordered writes and status
  live Sinkhole preserves failed self-check in UpdateSuspects
Both live guard removals resurrected the measured bypass as required.
```


### `python tools/bodycheck.py` ? exit 1

```text
DEFECT-GONE   90_SaveSanitizer.lua:82
              target  Lua/Buildings/Station.lua SavegameFixups.A_StationConnectorElements3
              /ResolveMap\(track, track\.elements\)/ no longer matches -- vanilla may have fixed it (REMOVE candidate, not a verdict: read the replacement)
NO-DEFECT     00_Core.lua
              pinned but cannot state the expression it corrects (FIX_POLICY §2b exception)
NO-DEFECT     Fix_SinkholeIndestructible.lua
              pinned but cannot state the expression it corrects (FIX_POLICY §2b exception)
SRC-NONE      00_Core.lua:18
              target  none
              registry only -- 00_Core patches no shipped body; it registers, gates and reports
SRC-NONE      90_SaveSanitizer.lua:119
              target  none
              F95 cleans residue this pack itself wrote; no shipped body is involved
SRC-NONE      Fix_BuildingCodesPrefab.lua:115
              target  none
              an additive OnMsg handler beside a preset's MsgReaction -- no function body of ours replaces a shipped one
SRC-NONE      Fix_CloggedBuildingRelease.lua:106
              target  none
              a StoryBit data defect plus a load/daily sweep -- no body of ours
SRC-NONE      Fix_DustSicknessBiorobots.lua:162
              target  none
              a StoryBit preset patch -- no function body to hash
SRC-NONE      Fix_ExoticDepositSign.lua:59
              target  none
              a class-default patch on a classdef table -- no function body to hash
SRC-NONE      Fix_FactionDomeSizeGate.lua:110
              target  none
              a FactionDef preset patch -- no function body of ours replaces a shipped one
SRC-NONE      Fix_SaintBlessing.lua:3
              target  none
              DataPatch on shipped preset data — no game function body is replaced
SRC-NONE      Fix_SilentHitMomentFX.lua:11
              target  none
              additive AnimMetadata presets for shipped moment-keyed FX
==============================================================================
138 manifest row(s) over 50 stamped module(s); 0 module(s) carry no manifest.
  1 DEFECT-GONE, 2 NO-DEFECT, 9 SRC-NONE, 126 OK
A GREEN here is NOT a clearance: it sees a changed body, a vanished defect
and a vanished target. It does NOT see semantics moving under a wrapper
(class c), and it sees nothing at all for a NO-DEFECT or NO-MANIFEST module.
```


### `python tools/bodycheck.py --module SaintBlessing` ? exit 0

```text
SRC-NONE      Fix_SaintBlessing.lua:3
              target  none
              DataPatch on shipped preset data — no game function body is replaced
==============================================================================
3 manifest row(s) over 1 stamped module(s); 0 module(s) carry no manifest.
  1 SRC-NONE, 2 OK
A GREEN here is NOT a clearance: it sees a changed body, a vanished defect
and a vanished target. It does NOT see semantics moving under a wrapper
(class c), and it sees nothing at all for a NO-DEFECT or NO-MANIFEST module.
```


### `python tools/bodycheck.py --module SinkholeIndestructible` ? exit 0

```text
NO-DEFECT     Fix_SinkholeIndestructible.lua
              pinned but cannot state the expression it corrects (FIX_POLICY §2b exception)
==============================================================================
2 manifest row(s) over 1 stamped module(s); 0 module(s) carry no manifest.
  1 NO-DEFECT, 1 OK
A GREEN here is NOT a clearance: it sees a changed body, a vanished defect
and a vanished target. It does NOT see semantics moving under a wrapper
(class c), and it sees nothing at all for a NO-DEFECT or NO-MANIFEST module.
```


### `python tools/deskbench.py` ? exit 0

```text

##############################################################################
# desk_c74_hit_moment_fx.py
##############################################################################
==============================================================================
C74/C77 silent hit-moment FX -- shipped bodies + whole module
==============================================================================
lua: Lua 5.5 | lupa 2.8

  PASS  [L0] shipped lookup finds the name but misses its numeric index  -- name/index=1/0
extracted CommonLua/Classes/AnimMoment.lua:5-37
extracted CommonLua/Classes/AnimMoment.lua:329-331
extracted Lua/Buildings/BaseBuilding.lua:856-858
extracted Lua/Buildings/BaseBuilding.lua:1037-1079
extracted Lua/Buildings/Building.lua:3346-3409
  PASS  [setup] current shipped lookup shape applies the module
  PASS  [L1] conversion resolves the two owned attach classes and leaves a foreign object inert  -- owned/foreign=2/0
  PASS  [L3] existing group/id wins; first pass adds ten and second adds zero  -- added=10/0, kept=True
  PASS  [L4] Excavator has 24 sorted moments and each Hit/Out type exactly once  -- count=24
  PASS  [L5] old-save pass replaces exactly four apparently-live vanilla trackers  -- TrackAll/Multi=2/2, replaced=True
  PASS  [L6] each load pass replaces rather than adds, leaving one live tracker per unit  -- after second=4/4, replaced=True, live=True
  PASS  [L7] Water update deletes/replaces one early tracker; foreign object passes through  -- TrackAll=5, foreign=1
  PASS  [L2] resolved future lookup makes the conversion guard decline cleanly  -- ; kept=True
  PASS  [L8] archived 1.0.7 bodies expose the same defect and take the shared repair  -- status=active, moments=2

==============================================================================
10 of 10 demands held
ALL DEMANDS HELD -- current defect, future decline, preset guards, load repair and Water replacement discriminate.

##############################################################################
# desk_c83_arrivals.py
##############################################################################
==============================================================================
C83 arrivals -- welcoming fallback and composition control
==============================================================================
lua: Lua 5.5 | lupa 2.8

extracted Lua/_GameUtils.lua:382-501 (120 lines)
  PASS  control: without apply, the dead assignment survives (the harness cannot pass by vanilla alone)

== A/B: reachable dead assignment, welcoming target with and without housing ==
  PASS  A: dead reachable dome -> welcoming dome with space
  PASS  log: first C83 reroute names the colonist and both domes once per session
  PASS  B: full welcoming dome is still the fallback (arrival becomes homeless there)

== stand-down controls ==
  PASS  C: no welcoming dome -> preserve vanilla's assignment
  PASS  D: welcoming assigned dome is untouched and never asks the F117 probe
  PASS  F: unknown ChooseDome argument shape -> stand down

== F53 regression and station-order falsifier ==
  PASS  E: F53 not-reachable branch still re-picks with no safety fallback
  PASS  G: station-sweep dome appended after sort wins by minimum dome_dist, not list order

== D03 composition and elevator pairing ==
  PASS  D03: non-tourist fallback cannot bypass a closed dome's CanAcceptNewColonists veto
  PASS  D03: tourists retain the opt-in module's documented closed-dome exemption
  PASS  pairing: a rerouted elevator dome keeps its matching emigration_elevator

==============================================================================
12 of 12 demands held
ALL C83 DEMANDS HELD -- negative control discriminates; all seven prompt cases, D03 composition, one-shot logging and elevator pairing pass.

##############################################################################
# desk_c85_clogged.py
##############################################################################
==============================================================================
C85 clogged release -- shipped Setexceptional_circumstances and module
==============================================================================
lua: Lua 5.5 | lupa 2.8

extracted Lua/Buildings/BaseBuilding.lua:470-480 (11 lines)
  PASS  the behaviour probe accepts the shipped setter
  PASS  a setter that no longer clears the fields declines the module fail-closed
  PASS  (a) a building stuck with the clogged reason is released
  PASS  (a2) the sweep enumerates BaseBuilding, the devs' own reconcile class
  PASS  (a3) the release is logged so the owner can read it back
  PASS  (b) a building whose BuildingClogged is still running is untouched
  PASS  (b2) ... while a different stuck building in the same pass IS released
  PASS  (c) a building with the fix-after-storm follow-up armed is untouched
  PASS  (c2) ... and an unrelated stuck building is still released
  PASS  (c3) a follow-up armed with NO object stands the sweep down (fail closed)
  PASS  (d) a law-disabled building (different reason id) is untouched
  PASS  (d2) the drones reply's end state is untouched (ec already false)
  PASS  (d3) a building disabled with no reason at all is untouched
  PASS  (e) a queued or open story-bit popup stands the whole pass down
  PASS  (e2) a non-story-bit popup does NOT stand the sweep down
  PASS  (e3) the exposed predicate itself refuses while a story-bit popup is pending
  PASS  (f) the daily pass releases a mid-session loss with no load
  PASS  (g) a Duration on the shipped effect latches the module inactive
  PASS  (g2) ... and it touches nothing in that pass
  PASS  (g3) ... and says RETIRE candidate in the log, for logscan
  PASS  (g4) a changed shipped reason id also latches inactive, and releases nothing
  PASS  (h) a coexisting maintenance state is released but keeps its reason field (shipped :474 -- vanilla's own behaviour for this call)
  PASS  (i) NEGATIVE -- a module registered but never applied releases nothing
  PASS  (j) NEGATIVE -- a mid-session veto stops the sweep (FIX_POLICY §2, A1)

==============================================================================
24 of 24 demands held
ALL DEMANDS HELD -- the shipped setter clears the stuck pair; the module releases only buildings carrying THIS reason id with no story bit running, no follow-up armed and no story-bit popup pending, and stands down when the shipped effect gains a Duration or changes its reason.

##############################################################################
# desk_c86_scan_downgrade.py
##############################################################################
==============================================================================
C86 scan downgrade -- shipped MapSector:Scan and module
==============================================================================
lua: Lua 5.5 | lupa 2.8

extracted Lua/Exploration.lua:229-286 (58 lines)
  PASS  vanilla reproduces deep scanned -> scanned
  PASS  module shape guard accepts the shipped status schema
  PASS  module preserves an already deep-scanned MapSector
  PASS  unexplored -> scanned is unchanged
  PASS  scanned -> deep scanned is unchanged
  PASS  foreign sector subclasses delegate unchanged
  PASS  shape drift declines the module fail-closed

==============================================================================
7 of 7 demands held
ALL DEMANDS HELD -- vanilla downgrades; the module blocks only the known downward transition on exact shipped sectors.

##############################################################################
# desk_c88_prefab.py
##############################################################################
==============================================================================
C88 Building Codes vs prefabs -- shipped LawDef handlers and module
==============================================================================
lua: Lua 5.5 | lupa 2.8

extracted Data/LawDef/LawDef-Efficiency.lua          Policy_BuildingCodesLax      Handler at :699  maintenance_change=+50
extracted Data/LawDef/LawDef-Efficiency.lua          Policy_BuildingCodesStrict   Handler at :907  maintenance_change=-30


  PASS  the module applies and the behaviour probe accepts the shipped handlers
  PASS  (a) THE DEFECT REPRODUCED -- with the law ACTIVE, the shipped handler applies no maintenance modifier to a prefab building
  PASS  (a2) ... while the SAME handler does apply it to a normally-built one (so the fixture is not vacuous)  -- [{'amount': 0, 'id': 'Policy_BuildingCodesStrict', 'percent': -30}]
  PASS  (b) the module applies exactly one modifier to a prefab building, under the LAW'S OWN id, with the shipped -30  -- [{'amount': 0, 'id': 'Policy_BuildingCodesStrict', 'percent': -30}]
  PASS  (b2) Lax too, with its shipped +50 -- both laws, as the owner ruled (option 1), and neither value hard-coded  -- [{'amount': 0, 'id': 'Policy_BuildingCodesLax', 'percent': 50}]
  PASS  (c) a normally-built building gets exactly ONE modifier (vanilla's) -- our handler adds nothing and cannot double it  -- [{'amount': 0, 'id': 'Policy_BuildingCodesStrict', 'percent': -30}]
  PASS  (c2) ... and it took exactly one modifier write on that building  -- 1
  PASS  (c3) ... and SetModifier was CALLED exactly once -- our handler returned at the prefab gate and never touched a normally-built building. ⚠️ The end state alone cannot show this: a second call with identical amounts no-ops inside the shipped body, so the call count is what holds the claim  -- 1
  PASS  (d) with NO Building Codes law active, a prefab gets no modifier
  PASS  (e) a building that is not RequiresMaintenance gets no modifier
  PASS  (e2) an invalid building is skipped before anything is read
  PASS  (f) simulated post-patch vanilla: the module STANDS ITSELF DOWN -- the discriminator is that ActiveLaws carries no law table with no game loaded, so their repaired handler throws; no version check anywhere  -- the Building Codes handlers no longer skip prefab buildings (C88 repaired by the game?)
  PASS  (f1b) ... and it says RETIRE candidate in the log, for logscan  -- ['BuildingCodesPrefab: inactive (the Building Codes handlers no longer skip prefab buildings (C88 repaired by the game?) — already correct, RETIRE candidate)']
  PASS  (f2) ... and a prefab still gets EXACTLY ONE modifier with the right value, applied by THEIR repaired handler alone  -- [{'amount': 0, 'id': 'Policy_BuildingCodesStrict', 'percent': -30}]
  PASS  (f3) ... in exactly one modifier write -- no churn  -- 1
  PASS  (f4) ⭐ BOTH handlers running -- theirs and ours -- still yields ONE modifier and ONE write, because the LAW'S id makes the second call a no-op in vanilla's own SetModifier (Lua/Modifiers.lua:181-204)  -- ([{'amount': 0, 'id': 'Policy_BuildingCodesStrict', 'percent': -30}], 1)
  PASS  (g) NEGATIVE -- a module registered but never applied leaves the prefab with no modifier (the defect stands)
  PASS  (g2) NEGATIVE -- a mid-session veto stops the handler (FIX_POLICY §2, A1)
  PASS  (h) with a game already loaded the probe CANNOT discriminate, so the module stays UNDECIDED rather than banking a verdict either way
  PASS  (h2) ... and while undecided it applies NOTHING -- an undecided guard is not permission (fail closed)
  PASS  (j) Report() on a repaired prefab prints the law's modifier and its percent  -- BuildingCodesPrefab: Building Codes applied to a prefab-deployed nil | C88-AB building=nil guard=true active_law=Policy_BuildingCodesStrict maintenance=100 | C88-AB   mod
  PASS  (j2) Report() on a prefab with NO modifier says C88 reproduces -- the owner cannot bank a false PASS  -- C88-AB building=nil guard=true active_law=Policy_BuildingCodesStrict maintenance=100 | C88-AB   NO Building Codes modifier on this building -- on a PREFAB-deployed one th
  PASS  (h3) the module loaded with an EMPTY LawDefs (the cold-boot order) and was still armed once the presets arrived -- the F75 trap
  PASS  (i) the 1.0.7 tree has no Building Codes Lax/Strict handler at all, so there is nothing for this module to find (1.0.7 had only the old cost-only law, now Obsolete)  -- Data/LawDef/LawDef-Efficiency.lua -> 0 id lines for Policy_BuildingCodesLax

==============================================================================
24 of 24 demands held
ALL DEMANDS HELD -- the shipped handler applies nothing to a prefab while applying -30 to the same building built normally; the module supplies it for both laws at their shipped values, under the law's own id, and adds nothing to a normal build, an inactive law, a non-maintenance building or an invalid one; and once vanilla's exit is gone the module declines while a prefab still ends up with exactly one modifier.

##############################################################################
# desk_c89_faction_gate.py
##############################################################################
==============================================================================
C89 faction dome-size gate -- shipped DomeFilter evals and module
==============================================================================
lua: Lua 5.5 | lupa 2.8

extracted Data/FactionDef/JusticeMovement.lua      JusticeUnemployment      at :103
extracted Data/FactionDef/JusticeMovement.lua      JusticeHomeless          at :128
extracted Data/FactionDef/ProsperityForMars.lua    ProsperityUnemployment   at :224
extracted Data/FactionDef/MarsDemocraticParty.lua  UtopiaUnemployment       at :87
extracted Data/FactionDef/MarsDemocraticParty.lua  UtopiaHomeless           at :106
extracted Data/FactionDef/WorkersParty.lua         CollectiveUnemployment   at :113
extracted Data/FactionDef/WorkersParty.lua         CollectiveHomeless       at :132
extracted Data/FactionDef/NewSol.lua               NewSolUnemployment       at :46
extracted Data/FactionDef/NewSol.lua               NewSolHomeless           at :65

  PASS  the module applies and the pass runs clean
  PASS  (a) THE DEFECT REPRODUCED -- all seven shipped evals fire on a dome of 3 with 1 idle/homeless colonist
  PASS  (a2) after the patch all seven refuse that dome
  PASS  (b) a dome of 10 with 1 idle/homeless: shipped evals fire
  PASS  (b2) ... and the patched evals still fire -- the gate changes nothing at ten or above
  PASS  (c) a dome of 30 with 2 idle/homeless (under 10%): both refuse
  PASS  (d) CONTROL -- both Justice evals are the SAME function object after the pass (not wrapped, not replaced)
  PASS  (d2) ... and Justice already refused the small dome, which is the whole precedent
  PASS  (e) exactly the seven target likes were patched, and no other  -- ['CollectiveHomeless', 'CollectiveUnemployment', 'NewSolHomeless', 'NewSolUnemployment', 'ProsperityUnemployment', 'UtopiaHomeless', 'UtopiaUnemployment']
  PASS  (e2) the module logged the count and the threshold it read from Justice  -- ['FactionDomeSizeGate: 7 faction dislike(s) now wait for 10 colonists in a dome']
  PASS  (f) a like the developers have ALREADY gated is skipped, not double-gated
  PASS  (f2) ... while the five still-unguarded ones ARE patched, and the log names the skipped ones  -- ['FactionDomeSizeGate: 5 faction dislike(s) now wait for 10 colonists in a dome (2 already gated: UtopiaHomeless, NewSolUnemployment)']
  PASS  (f3) a fully post-patch vanilla latches the module inactive as benign (the RETIRE signal), and patches nothing  -- every faction dislike already waits for 10 colonists in a dome
  PASS  (g) a second pass (DataChanged re-fire) double-gates nothing and does not latch
  PASS  (h) one missing like ⇒ NOTHING is patched and the module latches (a partial application would leave the five factions inconsistent)  -- 6 of 7 gated faction dislikes found
  PASS  (h2) a like whose DomeFilter.eval is not a function ⇒ nothing patched, module latches
  PASS  (i) Justice WITHOUT its own gate ⇒ the module declines and patches nothing -- the precedent this judgment call copies must be present  -- JusticeUnemployment on JusticeMovement carries no dome-size gate
  PASS  (j) the 1.0.7 tree: the module DECLINES on every run -- the duplicate unguarded `JusticeHomeless` is caught deterministically, with no version check  -- {'JusticeHomeless on MarsDemocraticParty carries no dome-size gate'}
  PASS  (j2) ... and the 1.0.7 expressions themselves are the same defect (the branch differs by ID, not by expression)
  PASS  (k) NEGATIVE -- a module registered but never applied patches nothing
  PASS  (k2) NEGATIVE -- a module whose self-check DECLINED patches nothing, even though DataPatch's runner still fires its pass  -- FactionLikeDomes.CountDome not found
  PASS  (m) Report() on a dome of 3 says GATE ACTIVE and shows shipped=true vs live=false on all seven rows  -- C89-AB dome=nil colonists=3 unemployed=1 homeless=1 threshold=10 | C89-AB   ProsperityUnemployment   shipped=true live=false | C89-AB   UtopiaHomeless           shipped=true live=false | C89-AB   Utop
  PASS  (m2) Report() on a dome of 10 shows no difference -- the gate is a gate, not a blanket suppression  -- C89-AB dome=nil colonists=10 unemployed=1 homeless=1 threshold=10 | C89-AB   ProsperityUnemployment   shipped=true live=true | C89-AB   UtopiaHomeless
  PASS  (m3) Report() with the fix NOT applied says shipped=not-wrapped and does NOT claim the gate is active -- the owner cannot bank a false PASS  -- C89-AB dome=nil colonists=3 unemployed=1 homeless=1 threshold=false | C89-AB   ProsperityUnemployment   shipped=not-wrapped live=true | C89-AB   UtopiaHomeless           shipped=not-wrapped live=true
  PASS  (m4) Report() on a non-dome says so instead of printing numbers  -- C89-AB: select a DOME first (no labels.Colonist on NotADome)
  PASS  (l) a missing like BEFORE DataLoaded does NOT latch (absence proves nothing yet -- the F75 lesson)

==============================================================================
26 of 26 demands held
ALL DEMANDS HELD -- the seven shipped evals fire on a dome of three with one idle colonist and stop after the patch; a dome of ten is unchanged; Justice is the same function object throughout; the module reads its threshold from Justice's own behaviour, skips a like already gated, latches benign when all seven are, and patches nothing at all if any part of the shape is missing.

##############################################################################
# desk_c90_datapatch.py
##############################################################################
==============================================================================
C90 actual core: decline, ordered writes, and healing of status
==============================================================================
lua: Lua 5.5 | lupa 2.8

  PASS  1.0.7 Saint intact: exact writes and status  -- active -> active; ['Saint.modify_trait=TraitReligious']
  PASS  1.0.7 Saint GetTraitLabel: exact writes and status  -- inactive -> inactive; []
  PASS  1.0.7 Saint TraitPreset.AddDomeColonistsModifier: exact writes and status  -- inactive -> inactive; []
  PASS  1.0.7 Saint LabelContainer.SetLabelModifier: exact writes and status  -- inactive -> active; ['Saint.modify_trait=TraitReligious']
  PASS  1.0.7 Saint failed self-check is erased from UpdateSuspects
  PASS  1.0.7 Saint veto stops the pass
  PASS  1.1.0 Saint intact: exact writes and status  -- active -> active; []
  PASS  1.1.0 Saint GetTraitLabel: exact writes and status  -- inactive -> inactive; []
  PASS  1.1.0 Saint TraitPreset.AddDomeColonistsModifier: exact writes and status  -- inactive -> inactive; []
  PASS  1.1.0 Saint LabelContainer.SetLabelModifier: exact writes and status  -- inactive -> active; []
  PASS  1.1.0 Saint failed self-check is erased from UpdateSuspects
  PASS  1.1.0 Saint arms the save re-base despite decline
  PASS  1.1.0 Saint veto stops the pass
  PASS  Sinkhole intact: exact ordered writes and status  -- active -> active; ['class.indestructible=true', 'template.indestructible=true']
  PASS  Sinkhole class: exact ordered writes and status  -- inactive -> inactive; []
  PASS  Sinkhole DestroyBuildingImmediate: exact ordered writes and status  -- inactive -> active; ['class.indestructible=true', 'template.indestructible=true']
  PASS  Sinkhole failed self-check is erased from UpdateSuspects
  PASS  Sinkhole veto stops the pass

==============================================================================
18 of 18 demands held
ALL DEMANDS HELD -- injected target loss, not a field reproduction.
==============================================================================
C90 live guards: declined apply cannot write, arm, or heal
==============================================================================
lua: Lua 5.5 | lupa 2.8

  PASS  1.0.7 live Saint intact: exact writes and status  -- active -> active; ['Saint.modify_trait=TraitReligious']
  PASS  1.0.7 live Saint GetTraitLabel: exact writes and status  -- inactive -> inactive; []
  PASS  1.0.7 live Saint TraitPreset.AddDomeColonistsModifier: exact writes and status  -- inactive -> inactive; []
  PASS  1.0.7 live Saint LabelContainer.SetLabelModifier: exact writes and status  -- inactive -> inactive; []
  PASS  1.0.7 live Saint preserves failed self-check in UpdateSuspects
  PASS  1.0.7 live Saint veto stops the pass
  PASS  1.1.0 live Saint intact: exact writes and status  -- active -> active; []
  PASS  1.1.0 live Saint GetTraitLabel: exact writes and status  -- inactive -> inactive; []
  PASS  1.1.0 live Saint TraitPreset.AddDomeColonistsModifier: exact writes and status  -- inactive -> inactive; []
  PASS  1.1.0 live Saint LabelContainer.SetLabelModifier: exact writes and status  -- inactive -> inactive; []
  PASS  1.1.0 live Saint preserves failed self-check in UpdateSuspects
  PASS  1.1.0 live Saint does not arm save re-base after decline
  PASS  1.1.0 live Saint veto stops the pass
  PASS  live Sinkhole intact: exact ordered writes and status  -- active -> active; ['class.indestructible=true', 'template.indestructible=true']
  PASS  live Sinkhole class: exact ordered writes and status  -- inactive -> inactive; []
  PASS  live Sinkhole DestroyBuildingImmediate: exact ordered writes and status  -- inactive -> inactive; []
  PASS  live Sinkhole preserves failed self-check in UpdateSuspects
  PASS  live Sinkhole veto stops the pass

==============================================================================
18 of 18 demands held
ALL LIVE GUARDS HELD -- desk evidence; ships unexercised in play.

##############################################################################
# desk_caller_seam.py
##############################################################################
CALLER SEAM DESK: Lua 5.5 | lupa 2.8 (archived bodies; no runtime claim)
In Progress while active, 1.0.7 waits: (0, None)
In Progress while active, 1.1.0 waits: (1, 'TechResearched')
already researched control, 1.0.7/1.1.0: (0, None) (0, None)
counterfactual: restoring the named In Progress branch makes the active case return without a wait
meal return, same-shift A+B remaining count: 1
meal return, old A/new-shift B remaining count: 0
counterfactual: tagging A with its reservation shift would leave new-shift B counted
VisitService entered=true fulfilled/eaten: (1, 1000)
VisitService entered=false fulfilled/eaten: (1, 1000)
counterfactual: guarding fulfillment/eating with successful entry would make the false case (0, 0)
PROBE SWEEP: clean
PASS: all three seam contradictions discriminate

##############################################################################
# desk_f117_argshape.py
##############################################################################
==============================================================================
F117 desk falsifier -- shipped bodies verbatim, our probe verbatim, real Lua
==============================================================================
lua: Lua 5.5 | lupa 2.8

[1.1.0] Community:GetScoreFor extracted, 19 lines; first line: function Community:GetScoreFor(colonist)
  PASS  [1.1.0] probe answers 'colonist'  -- got 'colonist'
  PASS  [1.1.0] no decline logged  -- []
[1.0.7] Community:GetScoreFor extracted, 28 lines; first line: function Community:GetScoreFor(traits)
  PASS  [1.0.7] probe answers 'traits'  -- got 'traits'
  PASS  [1.0.7] no decline logged  -- []

  PASS  [1.1.0] the OLD call ChooseDome(self.traits, ...) THROWS  -- [string "<python>"]:4: attempt to index a nil value (local 'obj_attributes')
  PASS  [1.1.0] the NEW call ChooseDome(colonist, ...) does not throw  -- <Lua table at 0x0000017B760B02B0>
  PASS  [1.0.7] passing the COLONIST does not throw (so no instrument would see it)  -- 100.0
  PASS  [1.0.7] ... but MIS-SCORES: correct=110.0, with-colonist=100.0  -- ck118's 'pass self on both branches' really is silently wrong

  PASS  [control] a body that indexes neither table is answered UNKNOWN, not guessed  -- shape=False
  PASS  [control] ... and the decline is NAMED in the log  -- ["ArrivalDeaths: ChooseDome's argument contract could not be read from Community:GetScoreFor -- the F53(b) arrival re-choose stands down for this session (F117)"]
  PASS  [control] a body that indexes BOTH tables is answered UNKNOWN too  -- shape=False

==============================================================================
11 of 11 demands held
ALL DEMANDS HELD -- the probe fires on 1.1.0, does not fire on 1.0.7,
both defects it guards against are real, and UNKNOWN is not guessed.

##############################################################################
# desk_f117_kitprobe.py
##############################################################################
==============================================================================
F117 KIT PROBE falsifier -- shipped bodies + module + kit probe, all verbatim
==============================================================================
lua: Lua 5.5 | lupa 2.8

  PASS  [1.1.0] the kit probe PASSes  -- PASS: the colonist is accepted; the old traits-table call still throws ([string "<python>"]:4: attempt to index a nil value (local 'obj_attributes'))
  PASS  [1.1.0] ... and its message says why it is not vacuous  -- the colonist is accepted; the old traits-table call still throws ([string "<python>"]:4: attempt to index a nil value (local 'obj_attributes'))
  PASS  [1.0.7] the kit probe PASSes  -- PASS: the traits table is accepted; the colonist object would mis-score (110.0 vs 100.0)
  PASS  [1.0.7] ... and its message says why it is not vacuous  -- the traits table is accepted; the colonist object would mis-score (110.0 vs 100.0)

  PASS  [C] no published ReadArgShape -> FAIL, not a quiet PASS  -- FAIL: SMRFixPack.ArrivalDeaths.ReadArgShape is missing — F117's discriminator is not installed
  PASS  [D] an UNKNOWN verdict -> FAIL, not a quiet PASS  -- FAIL: the module cannot read ChooseDome's argument contract (got nil) — F53(b)'s re-choose stands down (F117 UNKNOWN)
  PASS  [E] a stub that stopped discriminating -> SKIP, not a PASS  -- SKIP: the stub no longer discriminates: the traits table did not throw either, so the no-throw result proves nothing

==============================================================================
7 of 7 demands held
ALL DEMANDS HELD -- the kit probe passes on both branches for the right
reason, and refuses to pass when it cannot tell the arguments apart.

##############################################################################
# desk_f117_recipe.py
##############################################################################
==============================================================================
F117 recipe falsifier -- which landings reach GetScoreFor, on the shipped _GameUtils span
==============================================================================
lua: Lua 5.5 | lupa 2.8

extracted Lua/_GameUtils.lua:382-501 (120 lines)

== S0 control: one welcoming dome IN walking distance, with space ==
  S0: assigned=Near via=nil landing_list=1 safety=Near | wrapper fires=false | re-pick list=0 GetScoreFor calls=0 -> nil
  PASS  S0: assigned the walkable dome; wrapper stands down

== S1 the refuted recipe: every dome beyond walking distance (foot route exists), no station ==
  S1: assigned=Far via=nil landing_list=0 safety=Far | wrapper fires=true | re-pick list=0 GetScoreFor calls=0 -> nil
  PASS  S1: landing list EMPTY, far dome assigned as safety_dome, wrapper FIRES, re-pick list empty, GetScoreFor NEVER called  -- a clean arrival whether or not F117 is present

== S1b the refuted recipe, no foot route at all (dist -1) ==
  S1b: assigned=nil via=nil landing_list=0 safety=nil | wrapper fires=false | re-pick list=0 GetScoreFor calls=0 -> nil
  PASS  S1b: nothing assigned (safety needs dist >= 0), wrapper cannot fire

== S2 the station route: no dome walkable; a passenger station by the pad reaches a far welcoming dome ==
  S2: assigned=Far via=nil landing_list=1 safety=Far | wrapper fires=true | re-pick list=1 GetScoreFor calls=1 -> Far
  PASS  S2: far dome on the landing list WITHOUT an elevator pairing, assigned, wrapper FIRES, re-pick list non-empty, GetScoreFor CALLED

== S2b the station route with the far dome FULL (assignment falls to safety_dome) ==
  S2b: assigned=Far via=nil landing_list=1 safety=Far | wrapper fires=true | re-pick list=1 GetScoreFor calls=1 -> nil
  PASS  S2b: still assigned (as safety), wrapper FIRES, GetScoreFor CALLED in the re-pick

== S2c the station route with NO foot route to the far dome (dist -1) ==
  S2c: assigned=Far via=nil landing_list=1 safety=Far | wrapper fires=true | re-pick list=1 GetScoreFor calls=1 -> Far
  PASS  S2c: safety_dome comes from the station sweep (:470-472), wrapper FIRES, GetScoreFor CALLED

== S3 the elevator case the sitting guessed: elevator by the pad, dome on the other side ==
  S3: assigned=Under via=Lift landing_list=1 safety=Under | wrapper fires=false | re-pick list=0 GetScoreFor calls=0 -> nil
  PASS  S3: dome assigned WITH its elevator; the wrapper's elevator clause holds -> stands down (NOT a trigger)

== S4 a walkable dome that is FULL plus a far foot-reachable dome ==
  S4: assigned=Near via=nil landing_list=1 safety=Near | wrapper fires=false | re-pick list=0 GetScoreFor calls=0 -> nil
  PASS  S4: safety_dome is the NEAREST foot-reachable community = the walkable one, so the full dome is assigned and the wrapper stands down

==============================================================================
8 of 8 demands held
ALL DEMANDS HELD -- the refuted recipe never scores, the station route does,
the elevator route stands down by design, and a full walkable dome is not a route either.

##############################################################################
# desk_f119_trade_fuel.py
##############################################################################
==============================================================================
F119 trade fuel -- shipped request/status bodies and module
==============================================================================
lua: Lua 5.5 | lupa 2.8

extracted:
  Lua/CargoTransporterNew.lua:1288-1306
  Lua/CargoTransporterNew.lua:1430-1463
  Lua/UniversalRocket.lua:1891-1908
  Lua/UniversalRocket.lua:2631-2638
  Lua/UniversalRocket.lua:1916-1920
  Lua/UniversalRocket.lua:1937-1953
  PASS  vanilla DROP reproduces status 'unloading'
  PASS  vanilla DROP leaves supply at 0
  PASS  vanilla RISE reproduces status 'loading'
  PASS  vanilla RISE leaves demand at 0
  PASS  module behaviour guard accepts the shipped defective body
  PASS  module DROP sets a 20000 supply request
  PASS  module DROP reaches 'ready' once that fuel is unloaded
  PASS  module RISE sets a 10000 demand request
  PASS  load heal refreshes one pre-stuck Trade rocket
  PASS  load heal is a no-op on a healthy Trade rocket
  PASS  player rocket behaviour is unchanged (one vanilla refresh)

==============================================================================
11 of 11 demands held
ALL DEMANDS HELD -- the shipped bodies reproduce the request mismatch; the module repairs the desk model and the heal is selective.

##############################################################################
# desk_f59_expedition.py
##############################################################################
==============================================================================
F59 expedition hold: same shipped sequence, module absent / pre-repair / repaired
==============================================================================
lua: Lua 5.5 | lupa 2.8

  PASS  vanilla: crew retains reserved home with a homeless neighbour
  PASS  PRE-REPAIR: neighbour takes bed and expedition hold is lost
  PASS  PRE-REPAIR: residence remains within capacity (this is loss of hold, not overflow)
  PASS  REPAIRED: the expedition hold survives a competing homeless neighbour
  PASS  REPAIRED: the neighbour is not given a bed the boarding crew still holds
  PASS  REPAIRED: the deferred notification really ran (it declined, it was not skipped)
  PASS  CONTROL: with the deferral defeated the harm returns => the deferral IS the repair
  PASS  negative control: REPAIRED preserves crew home when no neighbour competes
  PASS  PRE-REPAIR: F58 exemption cannot protect a hold F59 prevented from being created
  PASS  PRE-REPAIR: F58 daily sweep does not restore the missing hold
  PASS  REPAIRED: with F58 also loaded the hold is held, so F58 has nothing to rescue
  PASS  original F59 gap: vanilla ordinary departure leaves an eligible neighbour homeless beside a free bed
  PASS  original-gap control: a later housing update takes that same bed
  PASS  PRE-REPAIR: ordinary departure was notified immediately
  PASS  REPAIRED: ordinary departure is STILL notified, one scheduler step later
  PASS  AUDIT IDEA (A1 only): exact expedition-home exclusion preserves the hold
  PASS  AUDIT IDEA: ordinary vacancy still offered immediately
  PASS  AUDIT IDEA: unrelated expedition pointer does not suppress this vacancy
  PASS  REAL comfort: the A1 hold loss is REAL -- neighbour takes the bed, hold cleared
  PASS  REAL comfort: REPAIRED keeps the expedition hold against a competing neighbour
  PASS  REAL comfort: defeating the deferral loses the hold again
  PASS  REAL comfort: an ordinary vacancy is still offered (the benefit survives)
  PASS  REAL comfort: vanilla still leaves that neighbour homeless beside the free bed

==============================================================================
23 of 23 demands held
ALL DEMANDS HELD

##############################################################################
# desk_f59_interact.py
##############################################################################
==============================================================================
F59 manual assign: same shipped ColonistInteract, module absent / pre-repair / repaired
==============================================================================
lua: Lua 5.5 | lupa 2.8

  PASS  vanilla: the kicked resident is evicted and the forced colonist takes the slot
  PASS  vanilla: the residence stays within capacity and no assert fires
  PASS  PRE-REPAIR: the hook re-homes the just-kicked resident into the slot in hand
  PASS  PRE-REPAIR: the forced colonist is inserted anyway -> OVER-CAPACITY residence
  PASS  PRE-REPAIR: the capacity assert fired (EF-008: reported, did not unwind)
  PASS  PRE-REPAIR: the player-visible infopanel count exceeds capacity
  PASS  REPAIRED: exactly one colonist lands and the residence stays within capacity
  PASS  REPAIRED: the player's eviction stands -- the kicked resident is homeless
  PASS  REPAIRED: no capacity assert fires and the infopanel reads 2/2
  PASS  REPAIRED: the deferred notification really ran (it declined, it was not skipped)
  PASS  CONTROL: with the deferral defeated the overfill returns => the deferral IS the repair
  PASS  AUDIT IDEA IS INSUFFICIENT: the expedition-home exclusion still overfills on manual assign
  PASS  negative control (pre-repair): a better free bed elsewhere draws the kicked resident away
  PASS  negative control (pre-repair): with nobody competing, the assignment stays within capacity
  PASS  REPAIRED: with a better bed elsewhere the assignment is still exactly in capacity
  PASS  vanilla: the infopanel kick leaves the freed bed unoffered
  PASS  REPAIRED: the infopanel kick DOES still offer the freed bed (same method, benign caller)
  PASS  STUB comfort: the pre-repair hook APPEARS to drag a non-resident into a dying home
  PASS  ⛔ REAL comfort REFUTES it: the pre-repair hook drags nobody in -- A3 does not exist
  PASS  REAL comfort: absent / pre-repair / repaired are INDISTINGUISHABLE at OnDestroyed
  PASS  LEAD CLOSED in vanilla's favour: even vanilla's own :86 re-homes nobody into the dying home
  PASS  the repaired guard still declines at the door, so no thread is created either way
  PASS  REAL comfort: A2 overfill is REAL -- 3 residents in a capacity-2 home, one assert
  PASS  REAL comfort: REPAIRED lands exactly one colonist, 2/2, no assert
  PASS  REAL comfort: defeating the deferral brings the overfill back
  PASS  REAL comfort: the audit's expedition-only exclusion still overfills
  PASS  REAL comfort: the infopanel kick still gets its freed bed offered

==============================================================================
27 of 27 demands held
ALL DEMANDS HELD

##############################################################################
# desk_migration_cluster.py
##############################################################################
==============================================================================
Migration cluster: controlled branch evidence, not in-play reproduction
==============================================================================
lua: Lua 5.5 | lupa 2.8

  PASS  F51 vanilla retains false after shuttles become available
  PASS  F51 patch recomputes both false-to-true and true-to-false
  PASS  F51 old permanent-block inference fails: false mode still creates shuttle task
  PASS  F52 vanilla 300-unit vacuum leg omits passage
  PASS  F52 patch uses available passage
  PASS  F52 no-passage control remains an outside walk
  PASS  F52 breathable control unchanged
  PASS  F54 vanilla admits player-disabled hub
  PASS  F54 wrapper rejects player-disabled hub
  PASS  F54 working-hub control admitted
  PASS  F54 self-lifting suspension control admitted
  PASS  F60 vanilla tally/gate exclude unpowered home, assignment accepts it
  PASS  F60 vanilla applicant housing estimate excludes the unpowered home
  PASS  F60 patched tally counts 3 but migration gate still rejects
  PASS  F60 patch reports all 3 applicants housed while arrival space gate rejects home
  PASS  F60 powered-home control agrees on tally and gate

==============================================================================
16 of 16 demands held
ALL DEMANDS HELD

##############################################################################
# desk_migration_observations.py
##############################################################################
==============================================================================
Migration observations: supplied topology, no in-play reproduction
==============================================================================
lua: Lua 5.5 | lupa 2.8

  PASS  F62 ordinary A-B-C chain: network includes C, service candidates do not
  PASS  F62 Passage Hub connects its spokes pairwise and offers C service to A
  PASS  F61 selector has no own/destination quarantine gate with eligible-service fixture
  PASS  F61/F62 service-passage switch still excludes remote service
  PASS  F80 real builder produces a three-station loop from paired-connector fixture
  PASS  F80 loop seam C->A uses stride -2 and omits B on that departure track
  PASS  F80 ordinary forward direction covers both remaining loop stations
  PASS  F80 opposite track from C covers B and A: union can hide per-track omission
  PASS  F80 passenger flag correctly truncates a cargo-only edge
  PASS  F80 open-line control visits both destinations without loop seam

==============================================================================
10 of 10 demands held
ALL DEMANDS HELD

##############################################################################
# desk_probes_f67_f59.py
##############################################################################
==============================================================================
F67 / F59 kit-probe falsifier -- shipped bodies at their real lines, module + probe text verbatim
==============================================================================
lua: Lua 5.5 | lupa 2.8

extracted Lua/UniversalRocket.lua function UniversalRocketBase:IsCargoReady :535-559
extracted Lua/UniversalRocket.lua function UniversalRocketBase:WaitsForManualLaunch :3006-3012
extracted Lua/UniversalRocket.lua function UniversalRocketBase:GetArrivalLocType :952-954
extracted Lua/Units/Colonist.lua function Colonist:SetResidence :2898-2917
extracted Lua/Buildings/Residence.lua function Residence:GetFreeSpace :232-234

== LanderEmptyLaunch (F67) ==
  PASS  [F67 L0] pre-rebuild probe text vs 1.1.0 body reproduces the sitting's ERROR line  -- ERROR: Lua/UniversalRocket.lua:544: attempt to call a nil value (method 'WaitsForManualLaunch')
  PASS  [F67 L1] module registered active, apply NOT run (vanilla body) -> FAIL on the empty clause  -- FAIL: empty auto rocket reports ready — it launches with nothing and comes straight back (F67)
  PASS  [F67 L2] module applied -> PASS  -- PASS: empty flight blocked, loaded flight still ready (1.1.0 body :535-559 driven; fixture past the :554 automode gate)
  PASS  [F67 L3] over-broad wrapper (always false) -> FAIL on the loaded clause  -- FAIL: a LOADED auto rocket is blocked too — an over-broad fix, or vanilla's automode gate (:554-556) closed on a fixture that should pre-date it by two hours
  PASS  [F67 L4] vanilla alone: LOADED fixture reads false inside its first automode hour, true two hours in (the :554 gate; retyped fixture)  -- false/true

== FreedHousingNotice (F59) ==
  PASS  [F59 L0] pre-rebuild probe text vs 1.1.0 body reproduces the sitting's ERROR line  -- ERROR: Lua/Units/Colonist.lua:2914: attempt to call a nil value (method 'UpdateLowComfortNotification')
  PASS  [F59 L1] module registered active, apply NOT run (vanilla body) -> FAIL: nobody told  -- FAIL: a home that just fell vacant does not offer itself to the dome's homeless — they wait for their own update, up to 12 game hours in a large colony
  PASS  [F59 L2] module applied -> PASS  -- PASS: vacated home offers the bed to the dome's homeless once the caller's operation has finished, not inside it; a residence with no free slot does not
  PASS  [F59 L3] a wrapper that notifies INLINE -> FAIL on the repair's own clause  -- FAIL: the vacancy notification fires INSIDE Colonist:SetResidence — a caller that frees the slot as a middle step of a larger operation (expedition boarding, manual Set Residence) loses the bed to a neighbour (F59 A1/A2)
  PASS  [F59 L3b] over-broad wrapper (defers, but no free-space test) -> FAIL on the no-slot clause  -- FAIL: a residence with no usable slot still walks the homeless list

==============================================================================
10 of 10 demands held
ALL DEMANDS HELD -- both probes fail without the module, pass with it, fail on an
over-broad wrapper, and the pre-rebuild text reproduces the sitting's ERROR lines.

##############################################################################
# desk_progress_seam.py
##############################################################################
PROGRESS SEAM DESK: Lua 5.5 | lupa 2.8 (archived bodies; no runtime claim)
expired disaster 1.0.7: (False, 0, 'FactionDisasterStop', True)
expired disaster 1.1.0 zero seats: (True, 1, None, None)
expired disaster 1.1.0 one seat: (False, 0, 'FactionDisasterStop', True)
counterfactual one-seat branch stops and removes the disaster (control discriminates)
expired completed task, no active task: 1
expired completed task, active-task control: 0
counterfactual active-task branch removes the expired approval bonus (control discriminates)
First-session popup route: old declaration+BeginSession call became a new declaration only; the retained EarthCouncilIntro preset and new closure message have no literal consumer
DeepScanning route: live Tech carries both effects; TechPreset is an inert id/group stub; exploration reads DeepScanAvailable; probes separately require AdaptedProbes
PROBE SWEEP: clean
PASS: disaster and completed-task controls discriminate; popup orphan and research route are source-connected

##############################################################################
# desk_seam_food.py
##############################################################################
SEAM DESK: Lua 5.5 | lupa 2.8 (archived bodies; no runtime claim)
pasture 1.0.7 performance=0: actual=0, expected=0, ui=None
pasture 1.0.7 performance=48: actual=2400, expected=2400, ui=None
pasture 1.0.7 performance=100: actual=5000, expected=5000, ui=None
pasture 1.1.0 performance=0: actual=0, expected=0, ui=0
pasture 1.1.0 performance=48: actual=2500.0, expected=1200.0, ui=1200
pasture 1.1.0 performance=100: actual=2500.0, expected=2500.0, ui=2500
counterfactual identity round helper: mismatch demand would FAIL (control discriminates)
ingredient enabled=True registry=True vegan=False: advertised, consumed, remaining=(1, 1, 200)
ingredient enabled=False registry=True vegan=False: advertised, consumed, remaining=(0, 1, 200)
ingredient enabled=False registry=False vegan=False: advertised, consumed, remaining=(0, 0, 300)
ingredient enabled=True registry=True vegan=True: advertised, consumed, remaining=(1, 0, 300)
1.0.7: ingredient consumer absent; no equivalent ingredient behavior control claimed
GetNextCrop 1.0.7: adjacent=B, gap-before-B=None (bounded loop; player caller not found)
GetNextCrop 1.1.0: adjacent=B, gap-before-B=None (bounded loop; player caller not found)
PASS: pasture branch difference and ingredient-toggle contradiction discriminate

##############################################################################
# desk_shelter_reflex.py
##############################################################################
==============================================================================
F73 shelter wrapper: branch and stand-down controls only
==============================================================================
lua: Lua 5.5 | lupa 2.8

  PASS  module-absent control calls original Idle and supplies no Rest command
  PASS  half-budget vacuum condition sends Rest and does not call original
  PASS  below half budget: original Idle runs, no shelter command
  PASS  no residence: original Idle runs, no shelter command
  PASS  nonworking residence: original Idle runs, no shelter command
  PASS  transport task present: original Idle runs, no shelter command
  PASS  dying colonist: original Idle runs, no shelter command
  PASS  no outside timer: original Idle runs, no shelter command
  PASS  retry throttle: original Idle runs, no shelter command
  PASS  breathable atmosphere: original Idle runs, no shelter command

==============================================================================
10 of 10 demands held
ALL DEMANDS HELD

==============================================================================
DESK BENCH: 20 harness(es)
  desk_c74_hit_moment_fx.py        HELD
  desk_c83_arrivals.py             HELD
  desk_c85_clogged.py              HELD
  desk_c86_scan_downgrade.py       HELD
  desk_c88_prefab.py               HELD
  desk_c89_faction_gate.py         HELD
  desk_c90_datapatch.py            HELD
  desk_caller_seam.py              HELD
  desk_f117_argshape.py            HELD
  desk_f117_kitprobe.py            HELD
  desk_f117_recipe.py              HELD
  desk_f119_trade_fuel.py          HELD
  desk_f59_expedition.py           HELD
  desk_f59_interact.py             HELD
  desk_migration_cluster.py        HELD
  desk_migration_observations.py   HELD
  desk_probes_f67_f59.py           HELD
  desk_progress_seam.py            HELD
  desk_seam_food.py                HELD
  desk_shelter_reflex.py           HELD
```


### `python tools/doccheck.py --emit-counts` ? exit 0

```text
ENTRIES: 187 files (2 grouped), 222 preserved index rows, 184 heading tags compared
  status derived from: c-row-default x1, row-evidence x36, row-status x1, tag x184
  warn F59: the frozen index-row cell says 'fixed*', entry says 'tested-attended' (from 'tag')
  warn F85: the frozen index-row cell says 'filed', entry says 'wontfix' (from 'tag')
  warn C12: the frozen index-row cell says 'filed', entry says 'cand' (from 'row-evidence')
  warn C13: the frozen index-row cell says 'filed', entry says 'cand' (from 'row-evidence')
  warn C14: the frozen index-row cell says 'filed', entry says 'cand' (from 'row-evidence')
  warn C15: the frozen index-row cell says 'filed', entry says 'cand' (from 'row-evidence')
  warn C16: the frozen index-row cell says 'filed', entry says 'cand' (from 'row-evidence')
  warn C17: the frozen index-row cell says 'filed', entry says 'cand' (from 'row-evidence')
  warn C37: the frozen index-row cell says 'filed', entry says 'cand' (from 'row-evidence')
  warn C35: the frozen index-row cell says 'filed', entry says 'cand' (from 'row-evidence')
  warn C34: the frozen index-row cell says 'filed', entry says 'cand' (from 'row-evidence')
  warn C38: the frozen index-row cell says 'filed', entry says 'cand' (from 'row-evidence')
  warn C39: the frozen index-row cell says 'filed', entry says 'tested-unattended' (from 'tag')
  warn F100: the frozen index-row cell says 'filed', entry says 'fixed' (from 'tag')
  warn C43: the frozen index-row cell says 'filed', entry says 'fixed' (from 'tag')
  warn C49: the frozen index-row cell says 'filed', entry says 'wontfix' (from 'tag')
  warn C50: the frozen index-row cell says 'filed', entry says 'tested-attended' (from 'tag')
  warn C51: the frozen index-row cell says 'filed', entry says 'tested-attended' (from 'tag')
  warn C52: the frozen index-row cell says 'filed', entry says 'parked' (from 'tag')
INDEX: fresh — regenerating from front matter reproduces INDEX.md byte for byte (222 rows)
FACTS: 92 files, 60 state an observation date, 3184 source lines preserved
FACTS INDEX: fresh — regenerating from front matter reproduces INDEX.md byte for byte (92 rows)
ROOT: docs/ holds exactly the 11 entries docs/README.md's map declares (BUGS.md, FIELD_REPORT_REPLIES.md, FUTURE_IDEAS.md, PLAYTEST_CHECKLIST.md, PLAYTEST_HELP.md, README.md, STATUS.md, UPLOAD_WORKFLOW.md, WAITING_ON_YOU.md, agent, archive)
ENTRY MIRROR: AGENTS.md == CLAUDE.md, byte for byte (2506 bytes)
STATE + STUBS: STATE.md 17451 bytes (warn 12288, hard 18432, line 200); 3 stubs present and pointing
  warn STATE.md is 17451 bytes, warn threshold is 12288 — copy this line VERBATIM into the owner report; the owner fires agent/prompts/perma/STATE_EVICTION.md
WAITING: fresh — 120 checklist items, 42 marked, 2 waiting on the owner, 28 need a marker
SKILLS: 2 skill(s), mirrored to .agents/skills/
    smr-bug-library           3685 B  ⚠ over the 3072 B target
    smr-orientation           3312 B  ⚠ over the 3072 B target
COUNTS: 50 Code/*.lua files, 49 registered modules (49 default-active, 0 files carry optional = true), 97 probes
        index rows: 119 F + 12 D + 91 C = 222 (in 187 entry files)
TEMPORARY SWEEP: 0 hit(s) in Code/ + TestKit Code/
LOAD ORDER: 1 shared-symbol constraint(s) checked, 50 file(s) in the code list
WRAP CHECK: 0 wrap site(s) outside Require, 4 allowlisted (FIX_POLICY §2; detector+allowlist in tools/harvest_wrap_targets.py)
PARSE: 50 file(s) in Code, 0 error(s) [Lua 5.5]
PARSE: 25 file(s) in ..\SMR-BugFixPack-TestKit\Code, 0 error(s) [Lua 5.5]  (report-only)
MODULE SETS: 50 file(s) in Code/, items.lua and metadata.lua's code list agree by name
BODYCHECK SELFTEST: PASS (the falsifier; every verdict fired on a known case)
PUSH SET: 48947 B in 5 file(s) ≈ 23k tokens (budget 40960 B)  ⚠ OVER
    CLAUDE.md                                 2506 B
    docs/agent/STATE.md                      17451 B
    prompts/perma/GENERAL_USE_PROMPT.md       7947 B
    prompts/perma/DISPATCH.md                10110 B
    MEMORY.md (Claude, outside the repo)     10933 B
    → every session pays this before it has decided anything; evict from the largest, not the easiest
TESTKIT TREE: clean
ALIASCHECK: 25 file(s), 37 SMRTest member(s) derived, 0 finding(s)  (report-only)
doccheck: GREEN

BUILD STATE (emitted by tools/doccheck.py)
- modules: 49 registered (49 default-active, 0 optional-gated files)
- Code/*.lua files: 50
- TestKit probes: 97
- BUGS index rows: 119 F + 12 D + 91 C
```
