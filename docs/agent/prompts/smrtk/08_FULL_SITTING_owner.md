# smrtk 08 — the full attended sitting

Link 08 of `smrtk`. A **Claude** session attending (rule 22), the owner at the keyboard. README rules 1–22; 07 wrote the script below and the
predictions (`reports/SMRTK_FULL_SITTING_PREDICTIONS.md`). The stale-probe gate binds before any reading.

## Job

Run the script; score every step against its prediction; **read `CheatsUsed` at the end of the sitting** (the
whole-sitting taint control — one read, after everything) and the toolkit's
eligibility read with the Mod Manager closed. On build 24995074 that read is
`UNAVAILABLE:sandbox` (`EF-096`): CanUnlockAchievement is blacklisted. Do not
claim full eligibility was measured. Write `reports/SMRTK_FULL_SITTING.md` with the archived log path, per-step verdicts, and every drift
(a button that logged twice, a line without the tag, an armed thing that survived a load) as evidence for 99.

## Verdict classes

PASS · PASS WITH CORRECTIONS (list them; the fixing link is named in 99's inbox as owed) · FAIL (name the button
class; 99 decides SHIP WITH CHANGES vs NO SHIP).

## What may NOT be claimed

Anything the log does not show. A gamepad path. Behaviour of a button class the script did not reach.

## Close-out

Outbox to 99; strike your row; `git rm` this file; push. Tell the owner in one line whether the panel is theirs to
use from now on (it is, in whatever state 99 confirms — the TestKit never ships).

## Notes from upstream

- **01 correction, 2026-09-13:** no eligibility verdict is available to the
  mod on build 24995074. 07 must script the honest unavailable read separately
  from taint. Use a clean 1.1.0 baseline; normal already-cheated fixtures cannot
  prove no added taint. See 01's predictions §Disagreements/§DEPARTURES.

### 07 outbox — 2026-09-14: preparation and full script

Predictions: `reports/SMRTK_FULL_SITTING_PREDICTIONS.md`, numbered classes 1–18.
Docs describe the TestKit runtime at `f093e3b`, README successor `c886fb7`.
All new page behavior is **as built**, not attended. Use 03C's coverage wording:
22 curated + 84 More names, 106/106 source-name capacity, conditional AddDustRC
alias omission; not 106 simultaneous buttons or the entire vanilla menu.

**Price: 40 minutes at the keyboard**, including three native load transitions
and three small stamps, after fixture/slot preparation. Agent desktop setup:
about 20 minutes once a suitable clean fixture exists. Provisioning a new 1.1.0
colony if none exists costs hours and is separate; do not conceal it in the
40-minute estimate. Each numbered block below has a first-screen witness.
Use the predictions' 3× abort times; do not turn an abort into repeated mutation.

## Attendee preparation — before telling the owner to start

Maintain a live todo list for preparation, sitting/archive, report/gates/close-out.
Read current STATE/WORKFLOW and `perma/SMRTK_SLOTS.md`; implement the following
bindings in agent-owned 80 with Mars.exe closed. 07 intentionally made no Code
edit. Parse, no-sync/no-print gates, doccheck GREEN and commit the slots before
launch. Their callbacks must use MARK → setup → act → DUMP → MARK and checked
results; no detached mutation or automatic arms.

| slot | plain label | sitting-owned job |
|---|---|---|
| 1 | Console and status | mark, ConsoleControl, TaintRead/eligibility and attributed dump |
| 2 | Probe preflight | real desktop evidence embedded before boot; populate live session/sitting/game at invocation and attest through ProbePreflight |
| 3 | Check after load | dump arms count, pin presence, loaded provenance and current session; read-only, survives reload through mod binding |
| 4 | Read map click | armed shared on_click reader, once_click=true, explicit cleanup, no mutation |
| 5 | Short breakpoint | register smrtk08_break disarmed before boot, prepare target GameTime()+5000 when armed, predicate read-only; effects mark/sound, pause=false; arm it then arm run_until with that id |
| 6 | Dump selected | checked selected dump and scalar state before/after a representative mutation |
| Scratch | Read sitting | read sol/map/error delta; no mutation |

Slot 5's trigger must leave pausing to run_until so its game-time poll can
observe the fire before stopping. Its registration never arms at mod load.
The attendee must reject stale desktop HEADs/evidence; slot 2 must reject stale
runtime session/sitting/build state. Resweep/update the evidence if a peer
changes code before boot. The required exact grep token/schema is in 76.
Run that desktop sweep, inspect every hit and declare it needed in this brief
or make it unavailable before trusting any probe. Full HEADs/check time/output/
exit/hit names are **emitted values**, never a fake CLEAN. After either load,
preflight expires and slot 2 must be invoked again only with still-current
desktop evidence. If it cannot establish freshness, stop probes and prepare anew.

Fixture: a **clean, resource-rich 1.1.0 colony**, Mod Manager/GED closed,
Platform.cheats unset, dome, ordinary depot, drone hub and universal rocket
travelling to our colony in its SleepFlight wait. Have at least one supported
dome interior with one built upgrade and two flat connected cable/pipe patches
with room for duplicates. Two completed sacrificial buildings, one disposable
colonist and drone are required for destructive controls. Keep all test objects
separate from the source layouts. If any are absent, provision before the owner
sits or record the associated leg NOT RUN; do not substitute a fake desk object.
No warm-up before initial clean read; this is explicitly a clean experiment.
Do not use a 1.0.7 save or an already-cheated fixture to prove no added taint.

Tell the owner: **"start the game; the Agent tab is loaded"** only after the
bindings, predictions and fixture route are concrete and the gates pass.

## Owner script — one boot, every page and button class

Console fences contain one complete command per line, no comments or placeholders.
Paste each line separately. Prefer the named panel button when a step names it;
console-only diagnostics are explicitly marked. The attending agent reads the
file log and scores each block; the owner supplies the screen witnesses.

1. **Dock, status and navigation — 3 minutes (classes 1–4).** Load the prepared
   colony, close the Mod Manager and any editor. First screen: SMR dock icon,
   CLEAN taint, eligibility unavailable. Open its menu and every page: Sitting,
   Selected, World, Agent, Saves, Kit, Stamper. Press Ctrl-Shift-F11 twice; collapse
   then expand, and check the status/common row stays visible. Press MARK and
   Flush; use these explicit initial markers/status reads:

```lua
*r SMRTK.sitting08_begin = SMRTK.Mark("SMRTK08_BEGIN")
SMRTK.TaintRead()
SMRTK.Run("eligibility")
```

2. **Console control — 2 minutes (class 3).** Agent → Slot 1 Console and status.
   First screen: slot result; agent requires console=false then console=true
   shortcut records and discriminates=true, not merely an open console. Close
   input, press Enter to reopen, then use Kit → Open console. Press F9; overlay
   clears. Old auto-open and Ctrl-Alt-C fallbacks remain; no before-load workaround.

3. **Probe negative/preflight and kit views — 4 minutes (classes 16–17).**
   First screen: probe controls disabled before Slot 2, then enabled. The following
   console diagnostic intentionally tries the guarded dispatch once:

```lua
*r SMRTK.Run("run_all")
```

   Require the named preflight REFUSED without any suite execution. Use Agent →
   Slot 2 Probe preflight, Kit → choose one registered probe → Run selected probe,
   then Run all probes once. Agent archives full completion and SKIPs/FAILs/ERRORs
   by name, never infers a suite baseline. Inspect the tail/error counter,
   Fingerprint and selected Dump. Arm/disarm Print tee and one logger (DustDevils
   for the next block); compare original function identities/read-only logger
   state in agent evidence. Suite completion may extend the 4-minute block to
   its declared 360 s abort threshold.

4. **World direct, target, quiet and speed — 4 minutes (classes 9–11).**
   First screen: World intensity/list controls and visible effect. Choose Cold
   wave intensity, start it, observe notification and Stop disaster. Arm Meteor
   single, aim at an empty scratch area, click once and observe the strike plus
   automatic disarm. Never use camera-center targeting. Arm quiet while the
   toolkit DustDevils logger is armed: require the named conflict refusal;
   disarm the logger, then arm/disarm quiet successfully. Normal/Fast/Ultra and
   Pause/Resume must change the visible clock; restore Normal. Use Funding +500M,
   Tech points 1 and Applicants 50 once each; check their named totals. Kit →
   snapshot before and after Funding supplies two snapshots and a known DIFF;
   do not silently credit snapshots made after both changes.

5. **Selected curated rows — 3 minutes (class 5).** First screen: selected depot's
   section, supported rows and visible stock. Pin depot A, hub B, dome C; validate
   the three refs. Fill, Empty, Fill on the ordinary depot and Dump; require the
   storable_resources discriminator and after values. On a scratch building
   use Malfunction then Clean & Fix, Add Maintenance/Add Dust and Add Prefab if
   supported; on hub/dome use a supported Spawn row and Upgrade row. Missing
   methods are named unavailable, not invented universal coverage. Slot 6
   brackets/dumps the selected representative. Keep the game running for queued
   curated mutations; do not dismiss a paused game-time queue as a dead button.

6. **Delete, Destroy and More — 3 minutes (classes 6–8).** First screen: two
   separate scratch buildings; Delete one, Destroy (blow up) the other. Observe
   removal versus actual destruction/rubble. On the disposable colonist More:
   Cheat → Kill, and disposable drone More: Cheat → Despawn; observe completion
   and CLEAN taint. Scroll the full More section; report clipped/unclear labels.
   On a supported surviving object use More: AsyncCheat → Inspect, observe the
   editor or explicit retail failure and close it. Properties/editor effects do
   not prove taint or eligibility; leave no editor open for the final reads.

   Stale-selection diagnostic: select a **surviving** drone, capture its ref,
   select the hub, then try the old action once. First screen: neither is removed.

```lua
*r SMRTK.sitting08_old = SelectedObj
*r SMRTK.Run("selected_more",SMRTK.sitting08_old,"CheatDespawn")
*r SMRTK.sitting08_old = nil
```

   The middle command is pasted only **after** switching selection to the hub;
   expected result REFUSED selection changed, not a second destructive action.

7. **World lists, spawn, repair and completion — 2 minutes (class 9).**
   First screen: chosen dome and a supported colonist trait picker. World →
   Colonists 1 on the intended dome; on a disposable surviving colonist pick a
   trait not initially present, Add then Remove it, inspecting each state. Use
   Fix all buildings, Complete constructions and Complete wires/pipes against
   a separately prepared scratch construction/grid segment; inspect completion.
   These sweeps are colony/current-map scope as labelled. Research visible Main
   techs and unlock controls may be inspected without firing during this sitting;
   they share direct dispatch but their individual behavior is NOT RUN.

8. **Agent click, note, trigger and run-until — 2 minutes (classes 11–13).**
   First screen: all six labels and Scratch; invoke Scratch once, Slot 4 and a
   world click, check one fire and disarm. Arm Slot 4 again, right-click cancel,
   no fire. Enter a note with Enter and another with Add note. Slot 5 Short
   breakpoint arms smrtk08_break and run_until; wait for TRIGGER then run-until
   FIRE and automatic pause, both disarmed. Restore Normal. On a drone choose
   field command in Kit, Configure watch, separately Arm; observe a real command
   transition if supplied, then Disarm. Do not inject an error merely to exercise
   First error since mark; inspect that row and mark it NOT RUN.

9. **Screenshot and evidence copy — 1 minute (classes 2,14).** First screen:
   marked scene. Agent → Screenshot + Mark; agent opens the exact logged path
   and owner confirms the image after capture. Paste Copy since mark into a
   desktop text viewer and verify attributed records. Copy layout later replaces
   the clipboard; do not assume this copy survives later clipboard actions.

10. **Save A and same-session load — 3 minutes (class 15).** First screen:
    Saves status, process session and provenance. Before Save A arm Slot 4,
    quiet, Print tee and a watch, with pins still set; no conflicting logger.
    Save A must disarm all those arms and restore owned wrappers. Re-arm a
    read-only target and watch, Load A; require no surviving arms, cleared pins,
    native loaded colony and PROVENANCE present=true. Slot 3 Check after load
    supplies the exact arms/pins/provenance dump. Attestation must be expired;
    do not run probes until a fresh Slot 2 establishes it again.

11. **Trip the foreign-session guard once, then Override — 2 minutes (class 15).**
    First screen: colony unchanged after refusal, then loaded A after Override.
    This changes only the toolkit comparison nonce temporarily, not native save
    metadata; no second boot. Paste separately and inspect the refusal before
    Override. Even if Override fails, restore the original nonce with the last
    two lines and abort this class. Agent records this is a comparison control,
    not proof of nonce regeneration across process restart.

```lua
*r SMRTK.sitting08_session = SMRTK.session SMRTK.session = SMRTK.session .. ":guard-control"
*r SMRTK.Run("load_A")
*r SMRTK.Run("load_override_A")
*r SMRTK.session = SMRTK.sitting08_session
*r SMRTK.sitting08_session = nil
```

12. **Rocket wait and landing trigger — 1 minute (classes 9,13).** First screen:
    rocket travelling to our colony; select through its pinned/list route after
    reload, pins must be recreated. Agent arm Next rocket landed, World → Finish
    selected rocket flight; require travel_wait_finished and a native landing
    event/trigger if it actually lands. Respect the built 2 s policy bound;
    a refusal is NOT RUN with its reason, never a repeated forced arrival.
    The custom trigger in block 8 is the required firing even if landing is delayed.

13. **Native stamp 1: ordinary depot — 2 minutes (class 18).** First screen:
    surviving source depot and empty level target. Name smrtk08_depot, Capture
    selected, Copy layout; agent opens/preserves literal text. Plan at click on
    the new target, freeze numeric ready/skipped/buildings/grid prediction before
    placement. While paused, try Stamp at click there once: require REFUSED and
    zero mutation. Resume, re-arm and stamp at the same target after a fresh plan
    if anything changed. Require final native STAMP, owned-site completion,
    left_sites=0, actual stockpile/functionality and after-taint read.

14. **Native stamp 2: dome/interior and upgrades — 3 minutes (class 18).**
    First screen: selected source dome with supported upgraded interior. Name
    smrtk08_dome, Capture selected. Plan first over the original occupied fixture:
    skips and zero mutation. Re-plan at empty level space; freeze numeric counts
    and PENDING_DOME interiors, then stamp at that same target while running.
    Inspect native fit, completed dome **GameInit**, each interior's actual dome
    membership and operation. Apply captured upgrades separately: check the
    affected new building's built state and colony unlock disclosure; queue
    success alone does not pass. Keep source objects unchanged.

15. **Native stamp 3: flat connected grids, capture lifecycle — 3 minutes (class 18).**
    First screen: source flat connected cable/pipe patch. Name smrtk08_grids,
    Capture rectangle; first click sets one corner without CAPTURE, second emits
    it and disarms. Copy literal layout. Plan/stamp at fresh level space using
    frozen native numeric counts, and inspect **connected** grids supplying their
    scratch consumers. Include a passage/suspended/switch row only if present:
    require its named skip, not replay. Inspect Capture map on the small clean
    fixture with a fresh name smrtk08_map; record a cap refusal as unavailable
    if over-cap. Next saved, Copy layout and Cancel target/work exercise their
    distinct controls. Arm a rectangle and Save A then Load A once: require
    DISARM/no retained corners, pins cleared and Slot 3's lifecycle dump.
    This final round trip also demonstrates target cleanup; native waits may
    extend the priced block, within the save/load abort threshold.

    Separate follow-ups (Fill storages all maps, Add 10 colonists on intended
    selected dome, Funding +500M) may be fired after base inspection; check actual
    World results and scope, not just STAMP_FOLLOWUP. They do not establish a
    complete colony duplication feature.

16. **Whole-sitting control and archive — 1 minute (classes 2,4,17).**
    First screen: editors/Mod Manager closed, no arms, CLEAN taint and unavailable
    eligibility. Use these final commands separately, with CopySince last:

```lua
SMRTK.Mark("SMRTK08_END")
SMRTK.TaintRead()
SMRTK.Run("eligibility")
*r local entries={} for k,v in pairs(CheatsUsed or {}) do entries[#entries+1]=tostring(k)..":"..tostring(v) end table.sort(entries) SMRTK.Log("DUMP",{cheats_used=table.concat(entries,"|"),cheats_count=#entries,arms=SMRTK.ArmedCount(),errors=SMRTK.error_count})
SMRTK.CopySince(SMRTK.sitting08_begin)
```

    Copy uses the numeric opening mark retained in SMRTK: string labels resolve
    only the current mark, which later marks replace. If COPY says truncated=true,
    preserve the partial clipboard but use the complete archived boot log for
    the whole-sitting audit; the ring is bounded.
    Agent inspects the actual CheatsUsed table's named entries in the log dump,
    not only AreCheatsUsed or the strip, and compares captured function identities
    after lifecycle cleanup. Save/open the copied evidence; archive the complete
    boot log, actual screenshot and captured layouts with source paths in the
    sitting report. Record per-block PASS/REFUSED/UNAVAILABLE/NOT RUN with named
    uncovered subclasses. Any residual arm, wrapper, taint or untagged/double
    primary result is drift for 99. 99 owns the transitive taint/source audit.

### 07 cautions / suggestions for 99

The bootstrap inversion remains owed to a code link. More inspectors can depend
on retail-unavailable debug services; do not silently score them PASS. Native
fit/GameInit/membership/connectivity/upgrades each need witnesses. Source-only
stamp counts are in predictions, and actual fixture counts must be frozen before
placement. Quiet must be disarmed before console loggers. FIX_POLICY is untouched.
