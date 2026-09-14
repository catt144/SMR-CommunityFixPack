# SMRTK 03A — shared UI spike

2026-09-13, Codex coordinator. Source build 24995074, inherited by
`python tools/doccheck.py --emit-fingerprint` (1.1.0 group HOLDS).
This is source evidence and a build decision, not a rendering/play verdict.
Spike precedes payload launch. TestKit starting HEAD `5d8d3b3`.

## 1. Infopanel section injection

**Decision:** listen to `OnMsg.DialogOpen(dlg)` and, for an `InfopanelDlg`,
resolve `idContent`, then create a toolkit-owned `InfopanelSection` and open
it explicitly. Make this idempotent by toolkit section id. Place it adjacent
to `idSectionCheats` where present, otherwise at the end of `idContent`.
`CommonLua/X/XDialog.lua:283-290` opens the host before sending DialogOpen;
`Lua/XDef/Infopanel.generated.lua:331-364` composes its named section host.
`Lua/X/Infopanel.lua:338-351` opens the object-specific dialog; its update
thread at :104-109 invokes `RebuildInfopanel`, whose body at :419-437 only
notifies modified objects. It does not replace the section list. Resolve the
actual object with `ResolvePropObj(dlg.context)`, validate supported methods
with `PropObjHasMember`, and never assume the selected object remains the
one that originally rendered a button. Register actions using selected needs.

**Rejected 1:** reuse `sectionCheats:new` or set the cheats config. Its
generated :15-18 requires `config.BuildingInfopanelCheats`; its toolbar at
:21-30 uses vanilla actions. `InfopanelObj:CreateCheatActions` at
`Lua/X/Infopanel.lua:22-54` invokes the tainting object wrapper at :49 for
ordinary methods. This violates the owner's route/config requirements.

**Rejected 2:** replace `InfopanelDlg:Open` or `OpenXInfopanel`. Even a
perfectly chained wrapper is a vanilla function patch while idle (rule 9).
If the named host is missing in a particular dialog, report that dialog and
expose Selected controls through a toolkit page; do not patch its rebuild.
The sitting proved the vanilla cheats section renders, not this new hook.

## 2. Armed map clicks

**Decision:** a temporary `TerminalTarget` instance registered with
`terminal.AddTarget` only while armed, removed with `terminal.RemoveTarget`
on disarm. Source: `CommonLua/Core/terminal.lua:11-30,210-225`; mouse dispatch
walks targets and stops on `break`. Priority 10001 precedes the desktop's -1
(`CommonLua/X/XDesktop.lua:15`). Use the existing modal window's
`GetMouseTarget(pt)` (desktop routing :320) to ignore toolkit/HUD/editor clicks;
accept the desktop, game interface or current world mode only. Right click
disarms. Read the cursor with `GetTerrainCursor` and optional object with
`SelectionMouseObj` (`Lua/UI/SelectionModeDialog.lua:43-51`).

Construction takes a left click in
`Lua/Construction/Construction.lua:392-399`, reads cursor at :439-441;
`Data/CheatDef.lua:315-326` uses that same terrain cursor for cave-ins.
**Rejected 1:** wrapping construction or selection mouse methods: possible
while armed, but a listener avoids any replacement and class/mode churn.
**Rejected 2:** a fullscreen mouse-capture window: it would swallow HUD/editor
clicks and conflict with focusing the advanced pages.

The coordinator adds shared `SMRTK.AcquireClick(id, callback)` and
`ReleaseClick(id)` to the core BEFORE launch. Owner id must already be armed;
only one click consumer may own the listener. Callback `(pos,obj)` dispatches
`Fire` inside any thread which actually mutates. Core logs ARM/DISARM through
the action; each click mutation logs FIRE. One-shot consumers disarm after
firing. P1 meteors, P3 slots and P5 rectangle capture inherit this service.
No payload creates an additional input route. No vanilla method is patched.

## 3. Dock icon, native menus and advanced side panel

**Decision: preferred dock/section plus rung-2 advanced pages.** Listen to
DialogOpen for `HUDClass`, with an InGameInterfaceCreated/PostLoadGame
idempotent lookup as fallback. `Lua/X/HUD.lua:18-30` calls XDialog.Open;
`Lua/XDef/HUD.generated.lua:365-383` creates `idBottom` and `idLeft`.
Append toolkit-owned controls there; never replace HUD.Open. The game does
not give `idLeft` a horizontal-list layout: use a separately positioned
child without changing existing children's layout or the parent method.

Use vanilla `XPopupMenu` and toolkit `XAction`s:
`CommonLua/X/XActions.lua:873-883` shows the native spawn/host contract;
`CommonLua/X/XMenu.lua:91-108,121-180` supports nested action menus and
per-menu scrolling. Populate from registered toolkit actions AFTER all mod
files load (on HUD creation), and resolve ids dynamically. Give menus only
one-shot/arm commands with complete arguments or a command that opens an
advanced page. Do not put an input-requiring registry action on a menu with
missing arguments. Every page/action remains reachable via advanced pages.

**Split:** World's action lists and common sitting commands use menus;
Selected actions use the section. Agent, Saves, Kit and layout configuration
use the closable left-side panel (rung 2), because editor state, slots,
metadata/provenance and a scrolling tail cannot be represented by menu
entries. The existing panel becomes fixed along the left edge, starts closed
on migration from skeleton settings, and has a scrolling page body. It
remains the hotkey's fallback. All tabs share one footprint. P2 owns the dock
and section; the coordinator owns this core/panel adaptation, frozen at launch.

**Safety glance:** P2 adds an always-visible compact dock read showing
CLEAN/TAINTED/UNKNOWN, eligibility unavailable, armed count and errors since
mark, even with every menu/panel closed. Refresh on a dock-owned thread and
after dispatch. Colours supplement text, not replace unknown readings.

**Rejected 1:** force all pages into XPopupMenu: its :161-180 menu-entry
construction does not provide editors or stateful scrolling evidence hosts.
**Rejected 2:** retain the floating panel as default: owner ranked it last.
If native dock/menu construction fails, P2 reports it; fixed side panel
remains rung 2. Rung 3 remains a possible subsequent judge repair.

## Upstream and frozen API additions

02 PASSed all four premises on build 24995074. Native ConsoleLine and print
tee both deliver real output; Ctrl-Shift-F11 is the working toolkit shortcut.
Depots are UniversalStorageDepotBase, discriminate `#storable_resources`,
never StorageDepot.resource. Eligibility stays UNAVAILABLE:sandbox. CopySince
must be the last clipboard operation. AsyncCheat methods already avoid taint.

Chrome verbs TAB/MOVE/PANEL/COLLAPSE/CLEAR/SHORTCUT/PANEL_RESTORE/DOCK/MENU/SECTION
are file-and-ring only, via the core logger's ConsolePrint condition.
`Action.screen=false` also suppresses display without suppressing the log.
Errors, world changes and sitting evidence keep display. Panel restores log
only an actual creation/make-visible, across all three existing messages.

Cross-page registry contract: P3 `pin_A`, `pin_B`, `pin_C`; P4 `dump_selected`,
`watch_field`. P3 supplies `T.Trigger`, `T.triggers`, `T.pins`; slots preserve
the original Run/Arm/Disarm/Fire contract and extend Bind in its OWN file.
P4 resolves P3 services dynamically. P5 registers a separate Stamper page
if that makes configuration safer than crowding World. Do not edit metadata
in parallel: report exact requested lines; coordinator adds each before its
file commit. No payload owns or changes core/panel during parallel work.

## DEPARTURES

Three techniques instead of the old two (owner enlarged the surface).
TerminalTarget listeners replace the proposed armed method wrapper: fewer
patches, same logging/lifecycle invariants. Dock plus a fixed side panel is
the owner's pre-approved per-page hybrid. P2 is re-seated to Astra/xhigh for
its enlarged two-surface job (old seat Sol/high at estimated difficulty 4).
Five logical payloads run in waves because only three child slots exist;
independent files and full inboxes preserve the fan-out contract.
Metadata writes are centralized to eliminate concurrent edits to one file.

## Live todo

- [x] Spike and upstream payload inboxes committed before launch.
- [x] Core/panel extensions gated and committed sequentially before launch.
- [x] P1 World: build, independent gates, file commit.
- [x] P2 section/dock: build, independent gates, file commit.
- [x] P3 Agent/slots: build, independent gates, commits.
- [x] P4 Saves/Kit: build, independent gates, commits.
- [x] P5 Stamper/format: build, independent gates, commits.
- [ ] Ordered merge checks, report, successor/audit inboxes, consumption/push.
