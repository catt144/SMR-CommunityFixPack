# FR-1 — Linux/NVIDIA 580 world-load crash: what is established (2026-09-10)

Owner ran the bench (Alienware m15 R4, RTX 3070 Laptop, Mint 22.2 / X11 / kernel
7.0.0-31, Proton Hotfix `hotfix-20260828`); `smr-bugfixpack-f0` read the evidence
and the two source trees. The owner's first report is verbatim beside this file
(`FR1_LINUX_BENCH_REPORT_2026-09-10.md`); the second update is quoted in §4.
⛔ Game 1.1.0.403908 unless a line says 1.0.7. Evidence folder (outside git, 168 MB):
**`C:\Dev\SMR-FR1-Evidence\`** — index in §5.

## 1 · MEASURED on the bench (owner-run, vanilla, mods off unless stated)

| run | result |
|---|---|
| Intel iGPU (Mesa) | world loads — PASS; a save made here is the control save |
| NVIDIA **580.173.02** proprietary, PRIME Performance | New Game → CTD |
| NVIDIA 580.173.02 open, PRIME On-Demand | CTD |
| NVIDIA **595.84-open**, PRIME On-Demand | world loads — PASS |
| 580: load the Intel-made save | CTD ⇒ not new-game generation; entering ANY world |
| 580: Reflections Low / Off | CTD both |
| 580: FR1Test mod (film grain off) | mod RAN (`[FR1Test] mod load: EnablePostProcGrain 1 -> 0` in a clean-exit log) — still CTD ⇒ **film grain REFUTED** (condition sampled) |
| 580: `VKD3D_DISABLE_EXTENSIONS=VK_NV_raw_access_chains %command%` | CTD ⇒ that extension alone is not it |
| 580: MarsDebug straight into a map | same CTD ⇒ the menu / New Game UI is not involved |

Crash signature (Proton log, `steam-3215050.log:677943-678804`): `*** Reloading assets
from folder 'BinAssets/'` at 7537.814 (thread 0340) → 17 ms later on thread 025c
`Exception 0xc0000005 … libnvidia-glvkspirv.so.580.173.02 + 0x157c88`, unwind through
`_nv014nvvm + 0x9c` (NVIDIA's NVVM compiler backend) → `err:vulkan:vkCreateComputePipelines
Exception 0xc0000005 in Unix call`. The game log stops at `Debug::Init()` — tail lost
in a crash (`EF-047`), matching the players' ~20-line logs.

## 2 · RESOLVED from source / upstream (desk, cited)

- **Upstream precedent:** VKD3D-Proton #2701 (read via API) — same game, NVIDIA 580.105.08,
  closed 2025-11-17 by the maintainer: *"Another NV compiler bug"*, *"Sent report to NV"*;
  workaround pyroveil commit `e1f5473…`, file `hacks/surviving-mars-relaunched-nv-580-stable/
  pyroveil.json`: match OpString `b73d41d886185985` → `glsl-roundtrip`, disable
  `VK_NV_raw_access_chains`. On 1.0.7 it needed Reflections > Low.
- **`b73d41d886185985` is NOT in the 1.1.0 dump** (243 files) — the old workaround's hash no longer matches.
- **The Reflections option is honest and unchanged:** "Off" sets `EnableScreenSpaceReflections = 0`
  in both trees (1.0.7 `CommonLua/Core/options.lua:515`, 1.1.0 `:519`); `Lua/Config/render.lua` unchanged.
- **Map load path:** `PreloadMap` → `WaitLoadBinAssets` → `LoadBinAssets` (`CommonLua/Core/map.lua:283-296`,
  `:236-247`) — same for New Game and Load. `Msg("ChangingMap")` fires before it (`:482`). The
  "Reloading assets" string itself is engine-side (no Lua hit).
- **Retail console:** none without a mod — `Mars.exe` log `Libs:` has no `DevToolsPublic`, `Platform:`
  has no `cheats`; the shortcut is gated `AreCheatsEnabled() or ConsoleEnabled or Libs.DevToolsPublic`
  (`CommonLua/Classes/XDef/CommonShortcuts.generated.lua:176`).
- **1.1.0 render deltas found (Lua-visible):** film grain (new compute pass `PostProcFilmGrainNoise.fx`,
  `Postprocessing.lua:51-52`, gated `hr.EnablePostProcGrain > 0` `:104`, reads **1** on retail, never set
  by Lua; its `FilmGrain` option has empty `hr = {}` and is not in the menu) — REFUTED as the cause (§1);
  new global volumetric fog (`CommonLua/VolumetricLighting.lua`, `volumetric_fog` NOT in
  `config.LightModelUnusedFeatures`, `Lua/Config/config.lua:50-53`); Lights option now
  `LightsDistantTileThreshold` (`options.lua:740-742`).
- **Shaders:** the game ships HLSL source (`Packs/Shaders.fpk`, 281 files, extracted) and its own
  `dxcompiler.dll`; `Packs/ShaderCached3d12.fpk` (134 MB) is a precompiled cache. Shaders mount
  "seethrough" from `svnProject/Shaders/`, `svnSrc/HR/Shaders/`, then the pack (`CommonLua/Core/mount.lua:47-51`);
  `ReloadShaders()` (DevTools) and `DlcReloadShaders` (`CommonLua/Dlc.lua:406`) exist. NOT explored further.

## 3 · The faulting shader — STRONG INFERENCE, not byte-proven

**`38121decbc3eee12`** (dump: `.dxil` 16,584 B, `.spv` 49,964 B) is the prime candidate:
last shader written (20:08:07.88) after a ~15.4 s gap in which nothing else was dumped; the crash
is ~12–17 ms after the reload. Its own properties (`tools/spvscan.py` + a DXBC/PSV0 parse):
- `GLCompute`, entry `ComputeShaderMain`, `LocalSize 8×8×1`, **2,599 SPIR-V instructions** — the
  largest of the dump's 23 compute shaders by 2.4× (next: 1,083); dozens of vkd3d structurizer
  names (`frontier_phi…ladder`, `transposed_selector`) = heavy branching.
- Bindings (PSV0): CBV b0, b1, b2 · Sampler s2, s4 · typed SRV t0–t7 · typed UAV u0 · **structured UAV u1**.
- Absent from `ShaderCached3d12.fpk` (debug-hash string, DXBC digest `cdc9ad58…`, first 64 bytes: 0 hits)
  ⇒ compiled at runtime from source.

**Matched to `Shaders/Reflections.fx`, variant `REFLECT_RAYS`** (screen-space reflections):
only 2 of 281 sources declare a structured UAV at u1 (`Reflections.fx:54` `TileCounter`;
`TerrainSplatMask.fx:7` — ruled out, binds only t0/b0). `Reflections.fx`: t0 depth (`regDepthMap 0`,
`:2`, `Raytracing.fh:4`), t1–t5 depth/colour/GBuffers, t6–t7 env cubemaps (`:45-51`); u0 `Reflections`
(`:53`); u1 `TileCounter` written only in `REFLECT_RAYS` (`InterlockedAdd`, `:456`) — the u1 in the
DXIL means REFLECT_RAYS; no u2 ⇒ not `REFLECT_IMPORTANCE_SAMPLE` (`:56-58`); `BEGIN_COMPUTE_SHADER(TILE_SIZE,
TILE_SIZE, 1)`, `TILE_SIZE 8` (`:243`, `:440`); samplers used = `LinearClamp` s2 + `TrilinearClamp` s4 from
`Common.fh:189`, `:191`; b0 = its `MainParams` (`:15`). No game Lua names any `REFLECT_*` define (grep, 0).
⇒ **Reflections "Off" stops SSR running but 1.1.0 still BUILDS its compute pipeline at world load;
NVIDIA 580's NVVM crashes compiling it.** Same shader family as #2701, new hash.
⚠️ Not proven: b1/b2 not traced; the proof is compiling `Reflections.fx` (REFLECT_RAYS) with the game's
dxc and comparing, or overriding just this hash on the bench and watching the crash move/vanish.

## 4 · Owner's second update, verbatim (2026-09-10)

> New Game and loading an Intel-created known-good 1.1.0 save both crash on NVIDIA 580. […]
> Reflections Low and Off both still crash. The FR1 diagnostic mod successfully executed and logged:
> "[FR1Test] mod load: EnablePostProcGrain 1 -> 0" but the game still crashed. […]
> VKD3D_DISABLE_EXTENSIONS=VK_NV_raw_access_chains also did not prevent the crash. Debug/MarsDebug boot
> reproduces the same underlying failure […] roughly 12 ms later […] _nv014nvvm + 0x9c. Debug startup
> confirms the game sees NVIDIA-G0, D3D12 Feature Level 12.1, 8160 MB VRAM. It also logs Failed
> activating D3D12 Dred and a separate graphics-options warning that OptionsData.Options.Antialiasing
> sets hr.ResolutionUpscale after another table already set it. I don't know whether either is
> relevant, but they are preserved. […] 243 files. The historical upstream/pyroveil shader hash
> b73d41d886185985 is not present. […] ~15.4 seconds with no new shader files. The final shader pair
> before the crash was: 38121decbc3eee12.dxil 16,584 bytes 20:08:07.882190879 / 38121decbc3eee12.spv
> 49,964 bytes 20:08:07.887276030 […] shader compilation is parallel so timestamp ordering is not proof.

Also owner-stated: **"The vast majority of users that I have seen say their computers cannot goto 595"**,
and Paradox's recommendation is the driver with no timetable. Unexplained, verbatim, not attributed:
`Failed activating D3D12 Dred`; the `OptionsData.Options.Antialiasing` / `hr.ResolutionUpscale` warning.

## 5 · Evidence index — `C:\Dev\SMR-FR1-Evidence\`

- `linux_testbench_surviving_mars_1.1.0_report.md` — first report (also in-repo, verbatim)
- `linux-handoff/` — `fr1dump-complete.zip` (243 files), `fr1dump-timeline.txt`, `primary-candidate/38121decbc3eee12.{dxil,spv}`,
  `fr1-newest-5.zip`, `steam-3215050.log` (~106 MB), `game-logs/` (Mars + MarsDebug, 14:56–20:07), `FR1-first-crash/`,
  `FR1-baseline/` (driver/PRIME/kernel/packages), `pdxsdk.log`
- `shaders-1.1.0-extracted/` — all of `Packs/Shaders.fpk` (281 files) via `tools/flpk_extract.py extract()`
- `tools/spvscan.py` — minimal SPIR-V scanner (`one <file.spv>` / `zip <dump.zip>`)
- `fr1test-mod/` + `.zip` — the film-grain diagnostic mod (refuted; a template for any Lua bench test)


## 6 · 2026-09-10 late — options exploration correction (desk, not another Linux bench)

**Supersedes §3's shader-identity/cache claims:** identity is now **PROVEN**:
rebuilding 1.1.0 `Reflections.fx REFLECT_RAYS` with the game's dxcompiler and
row-major matrices produced byte-identical DXIL, PSV0 and HASH chunks. b1/b2
were traced and NRD's resource macros checked independently. The complete
original DXBC was also found verbatim in a **decompressed** packaged cache
entry; the earlier compressed-pack search did not establish absence, and its
runtime-source-compilation conclusion is **REFUTED**. This does not establish
which source/cache route that process used. SPIR-V entry is `main`, distinct
from the DXIL entry `ComputeShaderMain`.

**Attribution remains a STRONG INFERENCE:** parallel dump timing does not prove
that this is the pipeline whose compile faulted; exact-hash intervention or
isolated replay remains owed. The ~15.4-second gap is still unexplained.
No new Linux mitigation was tested. Full evidence, ranked options, unrun
recipes and two unposted upstream drafts: [options report](FR1_OPTIONS_2026-09-10.md).
Archived desk receipt: `docs/archive/fr1-options-desk-2026-09-10.json`;
engine facts EF-088/EF-089; owner bench/scope routing is checklist **145**.

## 7 · 2026-09-10 night — same-thread attribution (`smr-bugfixpack-f0`, from the dump run's Proton log)

**MEASURED, `steam-3215050.log` (the dump run: 772 `vkd3d_shader_dump_blob` lines into
`fr1dump/`):** thread **025c** dumps `38121decbc3eee12.dxil` at **7537.824** and `.spv` at
**7537.829**, then faults at **7537.831** in `libnvidia-glvkspirv.so.580.173.02 +0x157c88` →
`vkCreateComputePipelines` error at 7537.832. The only lines on 025c in between are two
`msvcrt_get_flags incorrect mode flag: x` errors. A compute pipeline has exactly one shader stage.
⇒ §6's "parallel dump timing cannot attribute" is answered by the THREAD, not the timestamps:
the pipeline NVIDIA was compiling at the fault was built from `38121decbc3eee12` on that thread.
Grade: **direct log evidence**. The exact-hash override is still the formal proof (it would also show
no OTHER pipeline faults once this one is fixed). ⚠️ The dump run's Reflections setting is
**Low or Off, not confirmed which** (owner, 09-10). "Built while SSR is disabled" becomes MEASURED
only with an Off-only dump run. The developer reply is `FR1_DEV_REPLY_2026-09-10.md` (not posted).

## 8 · 2026-09-10 night — M1 + M2 desk checks, probe v2 (`smr-bugfixpack-bd`, owner: "start with M1 and M2")

Tree **G** = `C:\Dev\SMR-SrcArchive\1.1.0.403908\Src\`. Scratch (outside git): `C:\Dev\SMR-FR1-Options-2026-09-10\`
`variant-map\` (compiled variants, scan scripts + JSON receipts, `classify_dump.py`) and `fr1-options-probe-v2\` + `.zip`.

**M1 (`ForceShaderCacheReload`) — DEAD from Lua on this install.** SOURCE: its only Lua setter is `G/CommonLua/Dlc.lua:413`,
reached only when `find()` (`:262-274`) sees a DLC whose `assets_revision` is **strictly greater** than `AssetsRevision`.
MEASURED: `AssetsRevision` = 33006 (printed at `G/CommonLua/Core/mount.lua:240`; Windows log `Mars.exe-20260910-19.35.56`
lines 51/57/59) and both DLCs (norman, thomas) = 33006, same in the dump run's Proton log. ⇒ the flag is never set by Lua,
at boot or via `ModsLoadAssets` (`G/CommonLua/Modding/Mod.lua:2239`, same `find()`). A native default is UNSAMPLED: probe v2's
inventory reads it; an M1 leg is worth running ONLY if it reads `true` before LoadBinAssets.
- **Owner challenge, answered (MEASURED):** "two DLCs, different release dates, same revision?" The revision is a BUILD STAMP,
  not a release date. Retail DLCs read their own `revisions.lua` (`Dlc.lua:198`; `:196` is developer-only), and in both
  decoded packs it is `return 403908, 33006`. Both `DLC/norman.fpk` (= **Feeding the Future**, steam_dlc_id 3889430) and
  `DLC/thomas.fpk` (= **Interplanetary Codex**, 3889420) were written 2026-09-08 23:24, the same minute as
  `Packs/ShaderCached3d12.fpk`: 1.1.0 rebuilt both packs. **Second, independent kill:** neither pack carries a shader cache
  at all. `tools/flpk_extract.py` decoded both (2,493 + 66 files) and found 0 names containing "shader" and 0 nested packs. Control:
  `revisions.lua` was found in each. `find()` needs BOTH the newer revision AND `ShaderCache<api>.fpk` in the DLC, so M1 stays
  dead even after a future DLC rebuild bumps the revision, unless that DLC also ships a shader cache.
- **Owner's two follow-on ideas, homed (09-10 night):**
  - **(a) "Blank push":** force the reload with nothing new behind it, as probe v2 marker
    `ForceShaderCacheReload:1` (ck145 Leg D). INFERRED low odds: the base cache holds `38121decbc3eee12` verbatim (§6),
    so the same program reaches NVVM. Kept because the owner's lead is that a forced reload may change pipeline-creation
    behaviour, which the leg's dump can show. Falsifier: `CHANGED false -> true` at before-LoadBinAssets + the same 38121 crash.
  - **(b) Fake-DLC cache (SOURCE, NEVER RUN):** `DlcReloadShaders` is NOT in `ModEnvBlacklist`, but `MountPack` / `MountFolder` are
    (`Mod.lua:1366-1367`). So a mod could call `DlcReloadShaders{ {folder = <mod path>, assets_revision = <above 33006>} }` and have
    the game's own env mount a mod-shipped `ShaderCached3d12.fpk` (`Dlc.lua:406-414`). This is M4's delivery route, better than
    `DlcMountFolder`. Cost: a cache-pack writer in the engine's format, an NVVM-safe replacement for the RAYS entry, packed-mod path
    readability, and Windows/AMD render checks. Scope it only if M2 Legs B and D BOTH fail.
- **Probe v3, the owner's actual design (09-10 night):** the idea is the COMBINATION: set the selector, THEN force the
  reload. If the engine reads `SSRFullTile8x8` once at renderer init (before any mod runs, EF-089), the world-load reload is what
  would make it re-read the value. This supersedes (a)'s framing; the blank push is a component, not the idea. v3 takes a comma
  list applied in the order written and fails closed on any bad or duplicate pair. lupa 8/8 (`variant-map/probe_harness3.py`,
  game-faithful ModLog mocks). ck145 **Leg D** = `SSRFullTile8x8:1,ForceShaderCacheReload:1`. The reload alone is now Leg E, a
  control run ONLY if D loads, to tell which half did it.

## 9 · 2026-09-10 late night — bench legs A/B/D/E RAN (owner; laptop on 580, probe v3, Reflections Off, New Game)

Evidence (outside git): **`C:\Dev\fr1-mm-complete\fr1-mm\`**: per-leg dumps `A B D E`, `steam-{A,B,D,E}.log`, and the owner's extras
in `D/` + `E/` (game logs, key-line extracts, `D-test-config.txt`). C was not run because no leg loaded. Readers: `variant-map/classify_dump.py`,
plus a faulting-thread script (the last `vkd3d_shader_dump_blob` on the thread that faults).

| leg | marker | probe witness (Proton log) | Reflections program built | faulting thread, last dump | result |
|---|---|---|---|---|---|
| A | none | inventory; `render device: NVIDIA-G0 4318/9437` | `38121decbc3eee12` RAYS default | 013c: 38121 `.spv`, 1 ms before | CTD at world load |
| B | `SSRFullTile8x8:1` | mod-load `CHANGED 0 -> 1`; ChangingMap + before-LoadBinAssets `NOOP` (holds 1) | `38121decbc3eee12` | 013c: 38121, 1 ms | CTD at world load |
| D | `SSRFullTile8x8:1,ForceShaderCacheReload:1` | both `CHANGED` at mod-load | `271ec9634b1ab87b` RAYS hyp+imp (cache entry `12556516658419309610`) | 013c: 271ec, 1 ms | **CTD during boot slides, before the menu** |
| E | `ForceShaderCacheReload:1` | `CHANGED false -> true` | `271ec9634b1ab87b` | 0140: 271ec, 1 ms | CTD during boot, same as D |

- **MEASURED — "built while SSR is Off":** A's before-LoadBinAssets inventory reads `hr.EnableScreenSpaceReflections = 0`, and the fault
  is on 38121 on the same thread. This closes §7's ⚠️ and the dev reply's open check.
- **REFUTED (condition sampled) — `SSRFullTile8x8` as a mod-reachable selector:** B held 1 through before-LoadBinAssets and still built 38121.
  D set it BEFORE a forced rebuild, and the rebuild still chose a RAYS program. Neither dump holds a FULL program. §8's INFERRED bet is withdrawn.
- **MEASURED — the live `hr` SSR values do not pick this pipeline's defines:** A's baseline has `hr.SSRTraceHiZ = 1`, yet 38121 is the build
  WITHOUT `TRACE_HIZ`, so these values are either read only at init or are not the selecting vars. The `SSRTraceHiZ` / `SSRForceHyperbolicDepth`
  legs are dropped: the hyperbolic RAYS program (271ec) is itself measured crashing. `hr.SSRDenoiserMode` reads string `""`.
- **MEASURED — NVVM fails on the RAYS KERNEL FAMILY, not one hash:** 38121 and 271ec both fault at `glvkspirv +0x157c88` (`_nv014nvvm +0x9c`).
  ⇒ a pyroveil rule or override must cover every shipped RAYS program (6 distinct; cache entries in §8 / `variant-map`).
- **MEASURED — `ForceShaderCacheReload = true` set at mod load is consumed AT ONCE:** the engine re-creates reflections pipelines from the
  cache during boot (fault 67 ms after the SET in D, 1.07 s in E), NOT "on next map/savegame load" as the comment at `Dlc.lua:412`
  says, and that boot build selects the hyp+imp variant. ⇒ the "blank push" makes things worse (menu unreachable), but it proves that
  a cache change takes effect at boot, which is the lever the §8(b) fake-DLC route needs.
- **Routes left.** Mod-side: §8(b), a fake-DLC cache carrying replacement entries for the 6 RAYS programs (e.g., a no-op kernel with the same
  root signature, for players who keep Reflections Off). Unknowns: the cache record format (entry `14281071190732923386` is 25,133 B with
  the DXBC at 8,549, plus `index.bin` / `index.txt`); whether a partial pack overlays seethrough; whether the RAYS pass dispatches when Off; and the
  Windows/AMD effect if installed. Launch options (L2 `VKD3D_CONFIG=force_static_cbv`, L1 `PROTON_DISABLE_NVAPI=1`) and pyroveil (every RAYS
  hash) are still NEVER RUN. Routed: ck145.
- **Developer reply (2026-09-11, owner):** POSTED in the Steam discussion the Paradox dev tracks; editable; **no dev response yet**
  ("doesn't look like it's been read yet"). The owner is pasting in the three §9 updates (`FR1_DEV_REPLY_2026-09-10.md` header).

**M2 grounding — MEASURED desk.** The 1.1.0 `Reflections.fx` variants were compiled with the game's `dxcompiler.dll` and the argv that reproduced
`38121decbc3eee12` (§6), plus `TRACE_HIZ` / `USE_HYPERBOLIC_DEPTH` / `REFLECT_IMPORTANCE_SAMPLE` / `REFLECT_TILE`. The DXIL payloads
were then searched across all 6,455 decoded `ShaderCached3d12.fpk` entries (the 2 with no DXBC are `index.bin` / `index.txt`).
Control PASS (RAYS default → entry `14281071190732923386`).
- REFLECT_RAYS: all **6** distinct programs ship (hiz+hyp ≡ hyp, the `#elif` at `Reflections.fx:135-138`).
- REFLECT_FULL: **tile 8 and tile 16** ship, 6 distinct programs each; tile 4 does not.
- The dump run (`fr1dump-complete.zip`, 115 `.dxil`) holds exactly **one** Reflections program: `38121decbc3eee12` = RAYS
  default. No other RAYS variant and no FULL variant. ⚠️ The crash truncates the run: this is "not built BEFORE the crash".
- `Mars.exe` 0xfaa290–0xfaa580: the `hr.SSR*` names sit beside `Reflections.fx`, `REFLECT_FULL/RAYS/TILE`, `TRACE_HIZ` and
  `REFLECT_IMPORTANCE_SAMPLE`; `USE_HYPERBOLIC_DEPTH` sits at 0xfaa468.

**INFERRED — the M2 bet:** the engine builds the variant its settings select, and `hr.SSRFullTile8x8 = 1` selects REFLECT_FULL
tile 8. That is the one-pixel-per-thread kernel (`:515-529`) with no ray-queue `while(true)`/atomics loop (`:440-513`), and the game
already forces it on every AMD GPU (`G/CommonLua/Core/options.lua:81-85`). It is the top M2 treatment; `SSRTraceHiZ:1` and
`SSRForceHyperbolicDepth:1` keep the same ray-queue kernel (lower odds). ⚠️ Timing risk: the AMD block runs BEFORE
`InitRenderEngine` (`G/CommonLua/Core/autorun.lua:332→341`); if the engine reads the key only at init, a mod's late set does nothing.
⇒ **the witness is the leg's dump (which program was built), never the readback line.** The M3 "saved adapter name contains
amd" route is DEAD: `options.lua:57-59` re-reads `GraphicsAdapter` from the live device every startup, before that test.

**Probe v1 defect (desk, lupa `variant-map/probe_harness.py`).** Log → `ModLog(msg)` → `ModPrint` runs `string.format(msg)` with
no arguments (`G/CommonLua/Core/lib.lua:144,174`; `Mod.lua:109-132`), so a `%` in any `hr` string printed by the mod-load
full inventory throws before the LoadBinAssets wrapper and ChangingMap hook install. The harness showed v1 at `load_error`,
`wrapper=False`, `writes=1`. Whether a live `hr` string holds a `%` is UNSAMPLED (no Lua-side assignment does, grep G); Astra's 7
mocks never logged one. **v2** escapes `%`, installs hooks first, pcalls each phase and logs the render device: 7/7 PASS (v1 6/7).
Mock execution does not prove retail sandbox reach; the leg's `[FR1Options v2]` lines do. Owner steps: checklist **145**.
