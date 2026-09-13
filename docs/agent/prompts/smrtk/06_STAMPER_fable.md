# smrtk 06 — the layout stamper

Link 06 of `smrtk`. Fable. README rules 1–20 are yours. After 02 PASS; independent of 03–05 (own file, registers
its buttons on the World page through `SMRTK.Action`). Premise: `EF-099`; re-read `PlaceConstructionSite` and
`CheatCompleteAllConstructions` in the source before writing a line (rule 12).

## Job — `Code/77_SMRTK_Stamper.lua` + `Layouts/`

1. **The capture format is a contract — design it first, write it down** (`reports/SMRTK_LAYOUT_FORMAT.md`): a Lua
   table `{ v = 1, name, anchor = { q, r }, buildings = { { t = template_name, dq, dr, a = angle, dome = <index or nil>
   } ... }, grid = { { k = "cable"|"pipe"|"passage", dq, dr } ... }, meta = { map, sol, captured } }`. Offsets are hex
   offsets from the anchor. Version it; a stamp refuses an unknown `v`.
2. **Capture** — selection (a dome captures itself + everything `GetDomeAtPoint` assigns to it), a rectangle drawn
   by two clicks (04's click-to-target), or the whole map. `MapForEach` over `Building` and the grid element classes;
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
   Write 08's stamp step into 07's inbox (what to capture, where to stamp, what the log must show).
6. **Rotation** is out of v1; note the `HexRotate` route in the format doc for v2.

## Scope fence

IN: `77_SMRTK_Stamper.lua`, `Layouts/README.md` (one paragraph: how a layout file gets there), the format report,
`metadata.lua` lines. OUT: everything else; the ck151(c) owed boot is untouched by anything here.

## Stop conditions

`PlaceConstructionSite` needs the construction controller's live state to accept a call · dome membership cannot be
recovered at capture · grid replay through the line placers cannot form connections without the controller. Report
with the line numbers; a stamper that does buildings only, grids by hand, is a legitimate v1 — say so in ck175.

## What may NOT be claimed

That a stamped colony behaves as a built one (08 reads one). That capture is complete for any class you did not
enumerate.

## Close-out

Rules 15–16. Commit per unit (format · capture · stamp · state · dry-run). Outbox to 07 (the button list and the
08 stamp step) and 99 (the format doc, and any place you departed from `EF-099`); strike your row; `git rm` this
file; push.

## Notes from upstream

- (02 appends here)
