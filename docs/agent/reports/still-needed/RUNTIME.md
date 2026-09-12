# Runtime installation evidence — 1.1.0.403908

Coordinator `/root`, 2026-09-12. Three retail launches, main menu only. Both packs
and TestKit enabled. No colony loaded, no save written, no suite fired. No screen
witness. Code, metadata and registration in the fix pack were unchanged.

## Direct final registry measurement

MEASURED: **46/46 active**, including SaintBlessing. The third launch's temporary
reader calls the actual `SMRFixPack.ListFixes()` and enumerates the same registry,
after a main-menu wait and five seconds' settling. Archived verbatim:
`docs/archive/logs/stillneeded_registry_Mars.exe-20260912-00.29.01-6a91a190.log`.
SHA256 `c2b3b25f6862b4aeb9e80648e2938e3f54308cc8b705153aa844469afa8b275c`.

- `:53`: Build version 1.1.0.403908.
- `:176`: reader begins after menu settling.
- `:224` onward: one status per registered module.
- `:264`: SaintBlessing active.
- `:270`: TOTAL 46/46.
- `:271`: F102 `entity=SignRareMineralsDeposit rare-sign-valid=true`.
- `:272`: reader completes without a trapped error.

The final F102 entity and replacement-sign existence are directly measured.
This proves installation and class-default retargeting, **not** a freeze cure,
rendering correctness, affected-hardware safety, or the load-game re-sign sweep.
Saint's registry being active permits its historical save healer; it does not
mean that its 1.0.7 data repair is applied on 1.1.0 or that a damaged Saint save
was sampled.

## Raw boot messages differ from final registry

The settled second boot is also archived verbatim:
`docs/archive/logs/stillneeded_Mars.exe-20260912-00.25.42-6a91a190.log`.
Its raw last status-shaped messages are 45 applied / one Saint inactive. Later,
the Saint module arms the save re-base path and calls `ctx.heal()`
(`Code/Fix_SaintBlessing.lua:274`; `Code/00_Core.lua:345`). That changes the
registry without emitting another applied line. A parser of only applied/inactive
messages therefore yields a stale registry count. The direct third-launch read
supersedes it. `CENSUS.json` preserves both readings distinctly.

The first launch closed while data was loading; it was not used as the settled
evidence. The second and third finished through graceful WM_QUIT / `quit()`,
respectively; complete logs were read after process exit (EF-047).

## Instrument hygiene

Stale-probe sweep CLEAN before launching. The registry reader was committed as
parked text in `BOOT_READ_PLAN.md` before arming. The only declared TEMPORARY hit
was TestKit `Code/97_StillNeededBootRead.lua`. Readback confirmed its exact payload
and active metadata entry. Parsecheck: 25 TestKit Lua files, zero parse errors.
The payload was removed immediately after the successful read and TestKit
metadata restored byte-for-byte; SHA256 before/after
`9eaee43ba86ff1e0731c17bc4997928648ad63d3a8413f405665a8f0a6f18f76`.
The post-read TEMPORARY sweep has zero hits and TestKit git status is clean.

## Other boot diagnostics, preserved without attribution verdicts

The second boot includes the following lines; this sweep has not established
their cause. They do not justify a verdict on a fix-pack module:

- `:137` / `:138`: opt-in NoHomeless names Community while Workforce declares
  HasFreeWorkplacesAround, then logs inactive; `:162` logs NoHomeless applied.
- `:156`: opt-in MultipleSuns reports ArtificialSun template absent on an early
  data pass; `:159` later logs the build-once limit lifted.

The first, unsettled launch separately logged
`Invalid object SIE_ExporterValidity present on the map`; it is not present in
either settled archived log. That launch is not used to certify final status.

The archived bytes retain the full diagnostic strings, including the game log's
replacement characters. No `[LUA ERROR]` or `Error in mod` line occurs in either
complete archived log. These absence checks do not establish error-free colony
play. No developer-dialog or screen-rendering claim is made.

Both logs also contain Braze network diagnostics (second `:166`, `:169`, `:171`,
`:173`, `:175`, `:177`; registry log `:163`, `:166`, `:168`, `:170`, `:172`, `:174`):

```text
[Braze] SessionStart error The server name or address could not be resolved
[Braze] Failed sending launcher ev The server name or address could not be resolved
[Braze] Failed to init
```

Each sequence appears twice. They are preserved as reported SDK failures; this
sweep did not establish their cause or alter network/SDK configuration.
