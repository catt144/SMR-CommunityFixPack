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


## Additional bounded F46 native premise control - 2026-09-12

Parked/committed plan before arming: `F46_NATIVE_PLAN.md`, payload and harness
manifest in this directory. Retail launch 01:00:26, complete archive
`docs/archive/logs/stillneeded_f46_Mars.exe-20260912-01.00.26-6a91a190.log`, SHA256
`a24941a12a7ae1269a62a65587c6fd829405f5be983dc6b69635b3feac4260db`.
:53 measures 1.1.0.403908, :217 reports copied colony loaded in 7364 ms. No speed
change, actual unloading, route execution, new object, suite or save write.

MEASURED real Station Concrete request userdata:
:223 baseline flags1548 enabledtrue actual2500 target2500;
:224 AddFlags(rfSuspended65536) flags67084 enabledfalse actual2500 target2500;
:225 cleared and :226 SetFlags-restored reproduce exact baseline;
:227 control and independent restore both true. Positive suspended native cap
settles the F46 premise that was previously explicitly unestablished. Lua still
reads it in Train UnloadAll; actual dumping and cured routing remain unobserved.

Backup inventory `F46_SAVE_BACKUP.json`: 121 original saves, 5,964,340,606 bytes,
externally copied with hashes/mtime before launch. Result `F46_NATIVE_RESULT.json`:
all originals hash-verified unchanged, zero rotated originals and zero additional
saves, designated copy removed. External recovery backup remains under
`C:/Dev/tmp/stillneeded-f46-backup-20260912`.
Harness disarm passed. TestKit metadata SHA256 restored to
`9eaee43ba86ff1e0731c17bc4997928648ad63d3a8413f405665a8f0a6f18f76`, tree clean.
All temporary Code hits removed; no game remains running. Graceful quit/WM_QUIT
and complete Debug::Done footer at log end. This control adds no tested-attended
status and transfers no cure coverage to F114 or other modules.


## Byte preservation in git - append-only raw companions

A post-push byte check found core.autocrlf normalized the readable .log blobs.
Their lines are identical but their git-blob hashes differ from the original
mixed-line-ending log bytes captured above. No existing archive record was edited.
Three new `.log.raw` companions preserve the original bytes with a narrow -text
attribute; `RAW_LOG_MANIFEST.json` maps both forms and hashes. The original boot,
registry and native-control SHA256 values above/CENSUS refer to these raw bytes.
Line numbers are identical in the readable and raw forms. Fresh-checkout byte
verification should use the raw companions, not the normalized readable .log.
