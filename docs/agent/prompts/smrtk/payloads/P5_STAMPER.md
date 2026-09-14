# smrtk payload P5 — the layout stamper

Payload P5 of link 03A (`smrtk`) — **the vendor's top tier** (the capture format is a contract). README rules 1–22
are yours, **21 especially: you write, you never commit.** Independent of P1–P4 (own file, registers its buttons
on the World page through `SMRTK.Action`). Premise: `EF-099`; re-read `PlaceConstructionSite` and
`CheatCompleteAllConstructions` in the source before writing a line (rule 12).

## Job — `Code/77_SMRTK_Stamper.lua` + `Layouts/`

1. **The capture format is a contract — design it first, write it down** (`reports/SMRTK_LAYOUT_FORMAT.md`): a Lua
   table `{ v = 1, name, anchor = { q, r }, buildings = { { t = template_name, dq, dr, a = angle, dome = <index or nil>
   } ... }, grid = { { k = "cable"|"pipe"|"passage", dq, dr } ... }, meta = { map, sol, captured } }`. Offsets are hex
   offsets from the anchor. Version it; a stamp refuses an unknown `v`.
2. **Capture** — selection (a dome captures itself + everything `GetDomeAtPoint` assigns to it), a rectangle drawn
   by two clicks (the spike's click-capture route, `SMRTK_UI_HOOKS.md` §2 — the same one P3 builds on), or the whole map. `MapForEach` over `Building` and the grid element classes;
   skip construction sites and `EF-099`'s special objects by name (rockets, landing pads, the map-specific set — list
   them). Result → `CopyToClipboard` as `return { ... }` and `LocalStorage.smrtk_layouts[name]`; log
   `SMRTK_CAPTURE name=<n> buildings=<b> grid=<g>`.
3. **Stamp** — from `Layouts/<name>.lua` (files the agent adds to `metadata.lua`'s list; H-10) or LocalStorage; anchor
   at cursor; ordered passes **domes → complete → interiors → complete → grids → complete**, each pass through
   `PlaceConstructionSite` with a per-hex `IsBuildableZoneQR` fit check that logs `SMRTK_STAMP_SKIP t=<t> hex=<q,r>
   reason=<r>` and continues; `CurrentMap` guarded for multi-map colonies. Log `SMRTK_STAMP name=<n> placed=<p>
   skipped=<s>`. Grid elements via the line placers, `steps = 1`, `test = true` first.
4. **Then state** (second commit, only after 3 stamps clean on the desk — see 5): upgrades via `ApplyUpgrade(i, true)`
   per captured `upgrades`, then the World presets (`FillAllStorages`, colonists, funding) as an optional follow-up
   button on the same page.
5. **Desk falsification** — a lupa harness cannot run this; instead write the **stamp dry-run**: `test = true` on
   every placer and a "plan only" mode that logs each intended placement without placing. 08 runs the real one.
   Write 08's stamp step into your report's for-07 section (what to capture, where to stamp, what the log must show).
6. **Rotation** is out of v1; note the `HexRotate` route in the format doc for v2.

## Scope fence

IN: `77_SMRTK_Stamper.lua`, `Layouts/README.md` (one paragraph: how a layout file gets there), the format report,
`metadata.lua` lines. OUT: everything else; the ck151(c) owed boot is untouched by anything here.

## Stop conditions

`PlaceConstructionSite` needs the construction controller's live state to accept a call · dome membership cannot be
recovered at capture · grid replay through the line placers cannot form connections without the controller. Report
with the line numbers; a stamper that does buildings only, grids by hand, is a legitimate v1 — mark it OWNER-ROUTED
in your report (03B carries it to ck175).

## What may NOT be claimed

That a stamped colony behaves as a built one (08 reads one). That capture is complete for any class you did not
enumerate.

## Close-out (payload — rule 21)

Do NOT commit, do NOT `git rm`. Parse-check your file; rule 6's and rule 7's greps, counts quoted. Return a
**numbered-claims report** to 03A: per unit (format · capture · stamp · state · dry-run) — built · verified how
(command + output) · stopped · OWNER-ROUTED · for-07 (the button list and the 08 stamp step) · DRIFT (any place you
departed from `EF-099`, with the line numbers — 99 reads this). Plus **DEPARTURES** (every default you changed, why, which invariant you checked) and
**SUGGESTIONS** (better ways, things the plan missed — wanted, not tolerated; README § "What is FIXED").

## Notes from upstream

- (03A pastes 02's outbox and `SMRTK_UI_HOOKS.md` §2 here before launch)


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
