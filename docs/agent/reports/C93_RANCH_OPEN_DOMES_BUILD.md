# C93 — Outside Ranch Open Domes repair build

## Outcome

The repair is built and desk-verified, but not yet run in the game. The earlier brief targeted
the wrong mechanism. Open Domes changes an Outside Ranch from `OpenPasture` to
`OpenPasture_Open`; the open entity loses three anchors while `OpenPastureBase` continues to
declare `Resourcepile1`–`Resourcepile9`. That turns the last three attached piles into the
measured `Origin` group without changing their resources or supply requests.

`Code/Fix_OpenPastureStockpiles.lua` prevents the transition for this building only. Its
chained `OpenAirBuilding:CalcOpenAirEntity` wrapper immediately delegates for every foreign
receiver. For the exact Outside Ranch entity pair it returns `OpenPasture` as both the open and
closed entity. Open-air atmosphere, consumption and law state remain vanilla; the tradeoff is
that this one building keeps its closed visual.

For an already-affected save, synchronous `LoadGame` and `ModsReloaded` handlers change an
`OpenPasture_Open` object back to `OpenPasture`. If the engine does not restore the old numeric
attachments automatically, the handler reattaches only still-invalid pile objects to vacant
spots 7–9 and resets their attach offset. The operation does not recreate a pile or read/write
any stored amount.

## Why this shape

- Reducing the Lua list to six would discard the 1.1.0 design change that deliberately grew
  the pasture lists and added a third producer slot.
- Moving resources between piles would introduce loss, capacity and request-reconciliation
  risks. Keeping the same objects preserves those semantics by construction.
- Adding spots to a shipped 3D entity is not a Lua data patch. Keeping the matching nine-spot
  entity is the narrow runtime repair available to the pack.
- The generic `HasEntity` guard from the retired brief remains unrelated: every measured ranch
  pile has the `ResourcePlatform` entity.

## Self-deactivation and save safety

The module's apply-time probe checks the defect itself with engine spot APIs. It applies only
when `OpenPasture` has spots 7–9, `OpenPasture_Open` lacks all three, and
`OpenPastureBase.stockpile_spots1` still declares them. Any unknown or changed result declines.

The repair adds no persisted class, GameVar, field, thread or callback. A save written after
repair contains only vanilla ranch and pile objects on vanilla anchors. If the mod is later
removed, the closed ranch visual can persist until vanilla next changes its open-air state;
there is no executable mod residue and no resource mutation to undo.

## Verification completed

Against the installed 1.1.0.403908 source archive for build 24995074:

- `bodycheck.py --module OpenPastureStockpiles --all`: four manifest rows `OK`.
- `python tools/desk_c93_open_pasture.py`: ten of ten demands held against the production
  module — routing, object/resource preservation, reattachment, idempotency, veto and the
  corrected-entity decline.
- `doccheck.py`: GREEN; Lua 5.5 parsed all production modules, module lists agree, and the wrap
  detector reports no new out-of-Require site.
- The source callers of `CalcOpenAirEntity` were enumerated. All foreign buildings delegate to
  the captured original before the wrapper inspects any receiver state.

No Mars process was launched for this build. Checklist 191 requires one affected-save leg and
one ranch constructed after Open Domes before the entry can advance beyond `fixed`.
