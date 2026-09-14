# SMRTK P2 — section, dock and Selected fallback

2026-09-13, Codex payload P2. **Source/desk only; no P2 game leg ran.**
Starting pack HEAD `8d1a6aa`, frozen TestKit HEAD `05c7e45`
(core `265fde7`, panel `05c7e45`). Final gate identities are emitted below.
The coordinator owns commits and metadata. This payload never committed, removed
a file, edited core/panel/metadata, or touched pack runtime code.

## 1. Disagreements first

1. The prescribed **Delete (vanish)** wording overpromises. Read
   `Track.lua:614-616` (delegates to Destroy), `TrackElement.lua:277-279`
   (Demolish) and `RubbleBase.lua:187-189` (OnClear). The built button says
   **Delete**, with always-visible text explaining class removal and those
   exceptions. The coordinator agreed to this departure. Destroy retains the
   prescribed label; an already-destroyed Building instead clears itself
   (`Building.lua:1923-1930`). No play semantics are claimed.
2. MechanizedDepot Fill/Empty defer mutation through `func_after_anim_end`
   while `is_storing` is a live thread (`StorageDepot.lua:1762-1800`).
   The toolkit refuses that state **before** invoking the leaf, so a primary
   success and its taint assertion do not precede a deferred mutation.
3. The maintenance leaf is `CheatAddMaintenancePnts`, and rover dust is
   `CheatAddDustRC`. Capability checks use those actual names with
   `PropObjHasMember`; no metatable traversal is needed.
4. The sitting report's opening “NO GAME LEG HAS RUN” is stale prose. Its
   final verdict and outbox record the attended four-premise PASS. This
   payload inherited that outbox, without claiming its own UI had run.

## 2. Built and verified how

1. **Infopanel:** `DialogOpen(InfopanelDlg)` resolves the actual property
   object and named `idContent`, creates one toolkit `InfopanelSection`,
   and opens it explicitly. The new child goes immediately after
   `idSectionCheats` when that sibling exists, otherwise at the end.
   Original siblings retain their order. Missing named hosts return a logged
   `fallback=Selected`; no vanilla method or configuration is changed.
   The section's private IdNode contains an actual XSleekScroll/VScroll pair,
   fixed button columns, and a bounded scrolling body.

2. **Selected actions:** every owned leaf has `needs="selected"`.
   Invocation re-probes the live selected object and optionally checks the
   object rendered by the button. The UI checks again inside the thread that
   dispatches the mutation, closing the selection-change race. Companions
   resolve their registry IDs at invocation and display “not built” when
   absent; no stub definition can mask P3/P4. Direct API calls log NOT_BUILT
   through the same dispatcher. Universal depots read the table
   `storable_resources`, use its length to identify single/multiple
   resources, and report aggregate before/after amounts. They call the
   live object's override; no `StorageDepot.resource` assumption remains.
   Other supported classes invoke their probed leaf and report method,
   object identity and post-call validity, without inventing an amount.

3. **Dock:** `DialogOpen(HUDClass)` appends a private XActionsHost row under
   `idBottom`, above the lower-left dock. InGameInterfaceCreated,
   PostLoadGame and CurrentMapChangeDone perform an idempotent fallback
   lookup. The row leaves `idLeft`, MapSwitch and all vanilla layout
   methods untouched. It has an SMR button and text that remains visible
   while the menu and advanced panel are closed: CLEAN/TAINTED/UNKNOWN,
   eligibility availability, armed count, errors since mark and logger
   failure. Colour only supplements text. Refresh occurs after dispatch
   through the supplied core hook and every 250 ms; unchanged strings do
   not redraw the text. Load/map/end lifecycle removes owned instances.

4. **Native menus:** the SMR button opens XPopupMenu on the desktop using
   its native action host, nested menus, scrolling and focus/dismissal
   behavior. Toolkit XActions dispatch one primary result. Menus rebuild
   from registrations on HUD creation and each reopen. Common sitting
   commands have known complete contracts. Other payloads opt in with
   `menu=true` (Run), `menu="arm"` (Arm/Disarm), or
   `menu={phase="run"/"arm",args={...}}`; unannotated argument-consuming
   actions never become naked menu entries. IDs resolve at invocation.
   A selected-object action is always excluded from generic menu opt-ins.
   Native menu callbacks dispatch inside a real-time thread, accommodating
   yielding actions such as P3's screenshot marker.

5. **Advanced pages and fallback:** every registered page gets an Open
   entry, dynamically including later Stamper registration. The supplied
   `T.OpenPanel` opens the fixed side panel with the requested tab and
   expanded body. A Close advanced panel entry closes it. The Selected page
   mirrors supported controls and rebuilds on selection changes. This is
   the spike's named-host fallback, not a third injection route. The
   coordinator owns the shared page scrollbar and tab-width follow-ups.

6. **One primary and chrome:** section/dock/menu/page actions all use
   `T.Run`; arm commands call `T.Arm/T.Disarm` directly from the UI rather
   than nesting dispatchers. Chrome definitions specify `screen=false`.
   Leaves dispatch inside their game-time thread. Fake taint and error
   controls in the desk model establish that warnings appear independently
   of the primary, including with the advanced panel closed. No vanilla
   function is patched at load or while idle.

7. **Source routes opened, installed build 24995074:** the full
   `SMRTK_UI_HOOKS.md` route set; `XDialog.lua:283-300`,
   `Infopanel.lua:22-54,85-112,338-351,419-437`,
   `Infopanel.generated.lua:17-41,331-364`,
   `InfopanelSection.generated.lua:4-134`,
   `sectionCheats.generated.lua:4-32`,
   `HUD.lua:18-30,536-640`,
   `HUD.generated.lua:365-399`, `MapSwitch.generated.lua:14-107`,
   `HUDButtonTemplate.generated.lua:4-40`,
   `HUDButtonFrame.generated.lua:4-96`,
   `XActions.lua:104-139,200-220,285-349,700-710,873-883`,
   `XMenu.lua:91-193`, `XControl.lua:682-1008`,
   `XWindow.lua:225-278`, `XScroll.lua:563-590,823-848`.
   Method bodies read: Building (including generated upgrades and spawn
   helper), BaseRover, Community, Dome, DroneFactory/Hub, ShuttleHub,
   MicroGHabitat, StorageDepot, MultiResourceDepot, BuildingComponents,
   Farm, Mine, Deposit, SubsurfaceDeposit, SurfaceDeposit, Elevator,
   LandscapeLake, LanderRocket, UniversalRocket, Water/Air/ElectricityStorage,
   WasteRock, RubbleBase, Track, TrackElement, Drone and CObject.
   The leaf families contain their own class behavior; method availability
   alone is not proof of a useful mutation (Deposit's Empty is an empty body).
   The route test is source-derived, with per-action play readings still owed.

## 3. Exact gates

Before the Code edit, a separate `tasklist /FI "IMAGENAME eq Mars.exe"` emitted:

```text
INFO: No tasks are running which match the specified criteria.
```

`python docs/agent/reports/SMRTK_P2_SMOKE.py` uses the actual
`tools.parsecheck.runtime`, emits the source digest, counts the required
forbidden-token lines with a shipped positive control, then executes the
actual core/panel/P2 in a desk model:

```text
PACK HEAD: e245d80
TESTKIT HEAD: 05c7e45
P2 SHA256: 3dbbce3a4c093de6b033f31f476707473228593aa2b3bae4b5f22762bedd83ea
P2 PARSE: PASS [Lua 5.5]
RULE 6: 0 lines []
RULE 7: 0 lines []
FORBIDDEN STATE: 0 lines []
RULE 6 PRESENCE: 26 lines
P2 DESK: PASS — selected guards, single/multi depots, busy refusal, dynamic companions, injection/order/idempotence, queued selection race, fallback, argument-safe menus, late actions, one primary per click, arms, side page, CLEAN/TAINTED/UNKNOWN/errors, lifecycle
P2 CATALOG: 21 selected leaf actions + 4 companion registry ids; actual objects show supported subsets
P2 LIMIT: fake X controls and game services; no rendering, save mutation, or in-game no-taint claim
e245d80 Re-emit STATE.md's counts block after filing C94 (93 C -> 94 C)
```

The negative/positive cases include absent selection, changed selection,
unsupported methods, busy animation, a queue-time selection change, absent
and subsequently registered companions, a missing named host, unannotated
parameter consumers versus explicit arguments, later registry additions,
one primary per click/arm, and synthetic taint/unknown/error readings.
The fake X model uses the real IdNode lookup scope rather than recursive ID
search. It does not claim layout, engine class construction, or real taint
behavior.

`python tools/parsecheck.py --dir C:/Dev/SMR-BugFixPack-TestKit/Code --quiet`
emitted `PARSE: 30 file(s) in ..\\SMR-BugFixPack-TestKit\\Code, 0 error(s) [Lua 5.5]`.
That tree includes concurrent payload files; the own-file gate above is the
P2 result. `git pull --ff-only` emitted “Already up to date.” TestKit has no
remote. Agent enumeration showed the coordinator and P2/P3/P5 payloads.

`python tools/doccheck.py` emitted **doccheck: GREEN**. Its warning lines,
verbatim (pending P2 files are handed to the coordinator; peers are untouched):

```text
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
STATE + STUBS: STATE.md 11946 bytes (warn 12288, hard 18432, line 200); 3 stubs present and pointing
MARKER INTEGRITY: 51 on disk, 51 parsed; WARN
  warn duplicate ck:144 at lines 2553, 2627 (agree)
    smr-bug-library           3622 B  ⚠ over the 3072 B target
    smr-orientation           3248 B  ⚠ over the 3072 B target
  WARN ?? Code/73_SMRTK_Infopanel.lua
  WARN ?? Code/74_SMRTK_Agent.lua
  WARN ?? Code/77_SMRTK_Stamper.lua
  WARN ?? Code/80_AgentSlots.lua
  WARN ?? Layouts/
```

## 4. Final button list / integration contract

The emitted catalog is **21 selected leaf actions + 4 companion IDs**;
each object shows its supported subset.

| Label | Registry ID | Probed method / owner |
|---|---|---|
| Fill | selected_fill | CheatFill |
| Empty | selected_empty | CheatEmpty |
| Delete | selected_delete | CheatDelete; class-removal caveat shown |
| Destroy (blow up) | selected_destroy | CheatDestroy |
| Clean & Fix | selected_clean_fix | CheatCleanAndFix |
| Malfunction | selected_malfunction | CheatMalfunction |
| Add Prefab | selected_add_prefab | CheatAddPrefab |
| Add Dust | selected_add_dust | CheatAddDust, else CheatAddDustRC |
| Add Maintenance | selected_add_maintenance | CheatAddMaintenancePnts |
| Spawn Worker | selected_spawn_worker | CheatSpawnWorker |
| Spawn Visitor | selected_spawn_visitor | CheatSpawnVisitor |
| Spawn Child | selected_spawn_child | CheatSpawnChild |
| Spawn Colonist | selected_spawn_colonist | CheatSpawnColonist |
| Spawn Drone | selected_spawn_drone | CheatSpawnDrone |
| Spawn Shuttle | selected_spawn_shuttle | CheatSpawnShuttle |
| Upgrade 1–6 | selected_upgrade_1 through selected_upgrade_6 | corresponding CheatUpgrade1 through CheatUpgrade6 |
| Dump | dump_selected | P4; resolves at press |
| Pin A / B / C | pin_A / pin_B / pin_C | P3; resolves at press |

Dock: **SMR** opens/closes the native menu. Its **Sitting** submenu exposes
registered MARK, Copy since mark, Flush, Clear screen, Pause / Resume,
Stop disaster, Read taint, Read eligibility. Other action submenus are the
complete-contract opt-ins described above, grouped by page. Root entries
open each registered advanced page (Sitting, Agent, World, Saves, Kit,
Selected, and Stamper when registered) and **Close advanced panel**.
The final World action list belongs to P1, which had not been built during
P2's final gate; the integration contract avoids guessing its IDs.

Requested metadata line, coordinator-owned:

```lua
        "Code/73_SMRTK_Infopanel.lua",
```

Place after core/panel (normally after 72 World, before 74 Agent). Own files:

- TestKit `Code/73_SMRTK_Infopanel.lua`.
- Pack `docs/agent/reports/SMRTK_P2_SMOKE.py`.
- This report.

## 5. Stopped / OWNER-ROUTED / for 07

**Stopped:** no source injection contradiction; no implementation gate is
blocked. All P2 work is uncommitted for coordinator review. No game was
launched and no fixture changed.

**OWNER-ROUTED recommendations for 03B's single ck175 append:**
accept the honest Delete label and class-removal caveat; retain the visible
eligibility-unavailable read alongside taint; assess the dock-row placement
and bounded section size at 08. These are recommendations, not a new
permission request or a claimed eligibility PASS. Plain X chrome with a
lettered SMR icon needs an attended visual check before any stronger UX claim.

**For 07 / predictions for 08:** the first visible witness is Tool Kit on a
selected supported object and SMR plus safety text above the lower-left
dock. Opening menus/panels should produce file/ring-only MENU/TAB/DOCK/SECTION
records. Selecting a single-resource UniversalStorageDepotBase, then Fill,
should produce `SMRTK_ACTION action=selected_fill` with method CheatFill,
resources=1 and before/after fields, followed by a clean independent taint
reading. Multi-resource depots should say resource=multiple. A busy
MechanizedDepot should produce REFUSED with the animation reason and perform
no deferred action. Check one Delete and one Destroy on disposable fixture
objects and read their actual class semantics. Companion presses must resolve
P3/P4 once, and advanced page input, scrolling, closing/reopening, and
missing-host fallback remain attending/judge checks. Normal response 5 s,
abort at 15 s (3×); any new taint or unexpected engine error stops that leg.
Copy since mark remains the final clipboard operation.

## 6. DRIFT

- Stale 02 report header versus its final attended verdict: inherited outbox,
  reported above; no re-run.
- Delete's fixed “vanish” phrase contradicted source overrides; corrected
  openly with coordinator agreement.
- Generic Add Maintenance naming needed the real Pnts suffix; rover dust
  uses its separate RC leaf.
- The first source-read attempt used an incorrect SKELETON_PREDICTIONS
  location; the actual reports path was read. A guessed Shuttles.lua and
  XPopup.lua path did not exist; tree searches located ShuttleHub.lua and
  XControl.lua. These errors were never counted as negative gates.
- The first parsecheck invocation incorrectly supplied a positional file;
  its usage error was replaced by the supported directory invocation and
  the exact own-file runtime gate above.
- Review caught an invented cheats.png asset name and used the shipped
  section's dust.png. It also caught a Lua `and nil or` expression that
  would always disable Close advanced panel; the branch is now explicit
  and the desk model checks both visible/closed states.
- An added catalog-count probe initially inherited a truthy fake deleted
  member from its all-methods metatable and emitted an invalid count. The
  mock now sets deleted=false explicitly and asserts its total can contain
  the registered leaf catalog; the final emitted catalog is reproduced above.
- Shared tree HEAD advanced through peers' commits; their dirty files
  (including EF-099, generated fact index, archive planning and P3/P5 work)
  were preserved. Initial doccheck reported PUSH SET over budget; final
  doccheck emitted 40158 B and no PUSH SET warning after a peer's prompt edit.

## 7. DEPARTURES

- Expanded P2 owns both surfaces; coordinator re-seated Astra/xhigh and
  recorded this in the spike. This follows the owner's revised scope.
- Plain **Delete** plus an explicit class-removal caveat replaces the
  inaccurate “vanish” promise. It preserves truthful evidence and leaf-only
  dispatch.
- The Selected page is implemented here as the spike's approved fallback,
  despite the older payload stop-text saying not to build it. The frozen
  inbox and coordinator instruction explicitly requested it; no new hook.
- A plain toolkit XButton with **SMR** lettering is appended under idBottom,
  instead of constructing HUDButtonFrame's index-dependent child template.
  It still uses the spike's HUD message and native XPopupMenu route, with
  no method replacement. HUDButtonFrame's special child indices and
  notification handlers add coupling without supplying an SMR asset.
- Explicit menu metadata is an additive opt-in on action definitions.
  Core registration retains arbitrary definition fields, so this requires
  no core change and prevents argumentless dispatch of input actions.
- Busy mechanized-depot operations refuse instead of accepting deferred
  leaves, protecting the action-result/taint timing invariant.

## 8. SUGGESTIONS

- Have 03B read native XPopup focus/close behavior and actual IdNode
  registration as part of the route review; a permissive fake UI can mask
  precisely these mistakes.
- Judge the lettered icon's position at the owner's resolution and UI
  scale. Native dock frames are a later styling option once an appropriate
  icon and their notification child contracts have been costed.
- A future per-object capability catalog could explain known no-op leaves
  and disabled upgrade slots. This build intentionally reports the exact
  invoked leaf rather than inferring useful behavior from its name.
- Keep menu opt-in adjacent to the payload's complete argument contract;
  do not turn “has a registered action” into “safe to run without input.”
