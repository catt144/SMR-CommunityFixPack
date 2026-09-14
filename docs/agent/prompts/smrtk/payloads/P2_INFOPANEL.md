# smrtk payload P2 — the per-object section in the infopanel

Payload P2 of link 03A (`smrtk`). README rules 1–22 are yours, **21 especially: you write, you never commit.**
Independent of P1/P3–P5.

## Job — `Code/73_SMRTK_Infopanel.lua`: a "Tool Kit" section where vanilla's Cheats section sits, untainted

1. **The injection technique is decided — inherit it.** 03A's spike (`reports/SMRTK_UI_HOOKS.md` §1, pasted into
   your inbox) names the route that (a) needs no Mod Editor, (b) does not set `config.BuildingInfopanelCheats`
   (rule 10), (c) does not wrap a vanilla function while idle (rule 9). Build on it, or on its declared fallback.
   Not a third route on your own — not because the spike is authority, but because five of you run in parallel and
   cannot negotiate; a better route you see goes in your SUGGESTIONS section and the coordinator may re-spike on it
   (README § "What is FIXED"). Re-read the cited lines before building (rule 12); if they do not say what the
   spike says, STOP and report — that is a DRIFT finding.
2. **Buttons, all via `SMRTK.Action` with `needs = "selected"`, all leaf calls** (`EF-095` bodies): Fill, Empty, Delete
   (label it "Delete (vanish)"), Destroy (label it "Destroy (blow up)"), Clean & Fix, Malfunction, Add Prefab, Add Dust,
   Add Maintenance, Spawn Worker / Visitor / Child / Colonist / Drone / Shuttle as the class supports (probe with
   `PropObjHasMember` exactly as `InvokeObjCheat` does), Upgrade 1–6, **Dump** (P4's object dump — call its registry id;
   stub "not built" if it is not registered at load), **Pin A/B/C** (P3's pins — same).
3. The section renders only when `SelectedObj` supports at least one action; the vanilla Cheats section is left
   exactly as it is (with the panel on, the owner should simply never need to open the Mod Manager).
4. ⭐ **THE SECOND SURFACE IS NOW YOURS TOO — read the README's ⚖️ THE SURFACE block before starting.** The owner
   re-ruled the UI during the 02 sitting: the floating panel is **demoted**, and the preferred surface is your
   per-object section **plus an SMR icon on the game's dock reusing vanilla's own popout menus**. Three rungs, all
   pre-approved, descend them rather than asking; **03A's spike picks the route** (`reports/SMRTK_UI_HOOKS.md` §3) and
   reports which rung the build landed on. Feasibility handed down, not a route: `Data/XDef/HUD.lua` has named
   containers (`idBottom`, `idLeft`) and `HUDButtonFrame`/`HUDButtonTemplate` exist to spawn into it. Rule 9 binds
   hardest here — append a button when the HUD opens, never patch a vanilla HUD method while idle. Surface chrome
   follows the destination policy (03A's inbox item 1): logged, not printed to screen.
   ⚠️ **Two things the ruling makes yours that the old brief did not:** (a) a vanilla popout is a **menu**, so the
   Agent page's text field and the Kit page's log tail may not fit it — 03A is asked to settle the per-page split at
   the spike, and you build to whatever it decides; (b) your difficulty was read as **4 when the spike carried your
   only hard part** — with the second surface added that is closer to 6–7, so if 03A has not re-seated you, say so
   rather than absorbing it. ⛔ If no idle-clean route exists for the dock icon, that is a **finding, not a failure**:
   the ladder falls to rung 2 or 3 and the floating panel already exists.

## Scope fence

IN: `73_SMRTK_Infopanel.lua` + its `metadata.lua` line. OUT: any change to the vanilla section, any World action.

## Stop conditions

The spike's route does not hold on re-read · the infopanel rebuild path would need a wrapped vanilla function.
Report; the fallback is a "Selected" tab on the floating panel (say so in your for-07 section) — do not build the
fallback here.

## What may NOT be claimed

That the section appears in play (08). That Delete/Destroy semantics match play (08 reads one of each).

## Close-out (payload — rule 21)

Do NOT commit, do NOT `git rm`. Parse-check your file; rule 6's and rule 7's greps, counts quoted. Return a
**numbered-claims report** to 03A: built · verified how (command + output) · stopped · OWNER-ROUTED · for-07 · DRIFT. Plus **DEPARTURES** (every default you changed, why, which invariant you checked) and
**SUGGESTIONS** (better ways, things the plan missed — wanted, not tolerated; README § "What is FIXED").

## Notes from upstream

- (03A pastes 02's outbox and `SMRTK_UI_HOOKS.md` §1 here before launch)


### 03A frozen upstream inbox, 2026-09-13

(one paragraph, for every payload's inbox)

P1-P4 all PASS on build 24995074; the core, the logger, the taint assert, the
`ConsoleEnabled` arm, the ring, the clipboard and LocalStorage persistence are
all confirmed in play, so build on them. The native console tap **and** the print
tee both carry real output, so either is a valid capture route. Five things to
carry: **(a)** per-object code must target `UniversalStorageDepotBase` and
`#storable_resources`, never `StorageDepot.resource` — 01's leaf refused on every
depot in the game; **(b)** `AsyncCheat*` infopanel entries bypass `ObjCheat` and
never taint even in vanilla (`ClassHierarchy`, `ClipPlane`, `Gizmo`, `Inspect`,
`Properties`, `Screenshot`), so they need no re-implementation; **(c)** `CLEAR`
logs onto the screen it just wiped, and the fix is a per-action opt-in honoured
by `dispatch`, never moving `T.Log` before the callback, which would empty
`before`/`after` on every action; **(d)** `PANEL_RESTORE` logs once per
registration and there are **three** (`InGameInterfaceCreated`, `PostLoadGame`,
`CurrentMapChangeDone`) though only one panel results — log on actual
create/make-visible; **(e)** `CopySince` is destroyed by the operator's next
copy, so it must be the last command of a block, and the panel **button** form is
immune. The owner's surface ruling and ranked fallback ladder are in ck175.

Shared routes and API are in `docs/agent/reports/SMRTK_UI_HOOKS.md` ??1?3 (read all).
Infopanel: DialogOpen ? toolkit InfopanelSection under idContent; no vanilla patch.
Map targeting: SMRTK.AcquireClick(id, callback(pos,obj)) / ReleaseClick(id); exclusive TerminalTarget listener, armed only.
Dock: DialogOpen on HUDClass ? appended controls; native XPopupMenu action menus, advanced pages in fixed left-side panel.
Always-visible safety text lives on dock. Chrome display policy is in core; use screen=false for pure chrome actions.
Registry ids: P3 pin_A/pin_B/pin_C; P4 dump_selected/watch_field. Resolve at invocation, not initial file load.
Core/panel are frozen while payloads run; do not edit them. Report requested metadata lines; coordinator owns metadata writes.
Each payload owns only its assigned files, never commits/removes files, and writes its numbered-claims report to docs/agent/reports/SMRTK_PN_REPORT.md (replace N with your number).
