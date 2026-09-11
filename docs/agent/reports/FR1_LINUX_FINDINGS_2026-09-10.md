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

## 10 · 2026-09-11 — cache-probe v1 bench RAN (owner, laptop on 580): the overlay WORKS; 12 debug RAYS records were uncovered

Evidence (outside git): **`C:\Dev\fr1-cache\fr1-cache\`** (C1 + N1 dumps and Proton logs; owner note `N1/N1-result.txt`). Readers: Astra's
`fr1-cache-probe/analysis/classify_dump.py`, plus the faulting-thread script (§9). Build and design: `reports/FR1_CACHE_ROUTE_2026-09-11.md`.

- **First attempt — NO TREATMENT (marker typo):** the markers were `-fr1-cache-control` / `-fr1-cache-noop` (dash, not `=`; the game log's
  `Command line:` shows it). The probe logged `DECLINED marker must be exactly control or noop` in both; menu reached, then the usual
  world-load CTD with the faulting thread on `38121decbc3eee12` (1 ms). This is a baseline repeat, not a result. Fail-closed worked.
- **C1 `control` — MEASURED:** `ARMED Control` → `MOUNT_HELPER_OK` → `RELOAD_REQUESTED`; CTD during boot. The faulting thread's last dump is
  `271ec9634b1ab87b`, 1 ms before. That reproduces D/E.
- **N1 `noop` — MEASURED, the overlay wins precedence and is consumed:** the dump holds the no-op DXIL (`4f866e2c54fc9064.dxil`, sha256
  `516fc383…` = the probe's `EXPECTED_DXIL_SHA256`). Past C1's stage, the game built 260 DXIL (C1: 123), including REFLECT_FULL tile 16
  (`c2aacc1919769303`) **without a fault** ⇒ that FULL kernel passes NVVM 580. The owner saw a pre-menu loading screen hang for seconds, then
  a CTD ~11 s after `RELOAD_REQUESTED`, still in the boot rebuild (no ChangingMap). The faulting thread's last dump is **`a26e0bbfe7751fbf`**,
  1 ms before, at the same NVVM site.
- **`a26e0bbfe7751fbf` identified (MEASURED desk):** compute cs_6_6, cache record `5519638363063710019`; `index.txt` names it
  `Reflections.fx|USE_HYPERBOLIC_DEPTH|(TRACE_HIZ|)REFLECTION_DEBUG|REFLECTION_ITERATIONS|REFLECT_RAYS`. It is a **debug RAYS build**. Its
  RTS0 is byte-identical to the default RAYS root. It is absent from every earlier dump.
- **The gap:** `index.txt` `[k]` lines (source|defines → record key) list **18 REFLECT_RAYS records**; v1 replaced the 6 non-debug ones. The
  12 `REFLECTION_DEBUG` builds are recorded in `reports/FR1_CACHE_ROUTE_2026-09-11.md` §8 and its round-2 receipt. A third RAYS program is now measured faulting 580 (38121,
  271ec, a26e), which strengthens the family inference (Astra's precision note stands: the rest are not individually measured).
- **MEASURED desk follow-up:** Astra built probe v2 covering all 18 records, with a separate no-reload treatment: 36 shader/root checks
  and 35/35 harness cases pass. Game bench NEVER RUN; copy-paste steps replace v1 in ck145. Report: `reports/FR1_CACHE_ROUTE_2026-09-11.md` §8.

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

## 11 · 2026-09-11 — cache-probe v2 bench RAN (owner, laptop on 580): Q2 LOADS WORLDS with the RAYS no-op; R2 reverses it

Evidence (outside git): **`C:\Dev\Success\fr1-cache-v2\fr1-cache-v2\`**: C2/Q2/R2 dumps plus `steam-{C2,Q2,R2}.log`. Q2's `after-action/` holds
the owner's result note, the game logs, key-line extracts, the file timeline, sha256 list and system state; `R2/` holds `R2-result.txt` and its
game log. `C:\Dev\Success\Q2-SUCCESS-BACKUP\` is the owner's duplicate of Q2 (same 965 files and sizes; not re-hashed).
`C:\Dev\Success\fr1-cache\` is the v1 C1/N1 set (795 files, same byte total as `C:\Dev\fr1-cache\fr1-cache\`). **F2 was not run, by
design: Q2 loaded.** Readers: Astra's v2 `classify_dump.py` (the 228 compute programs plus the no-op, by DXIL bytes), plus a timeline
scan of the dump lines. Read by `smr-bugfixpack-5d`. Setup (Q2 `system-state` / result notes): probe v2 (`9031634`), NVIDIA
580.173.02, PRIME On-Demand, Reflections Off. Only `SMR_FR1CacheProbe` loaded mod items; the fix pack was installed but not loaded.

| leg | `Command line:` (game log) | probe witness (Proton log) | Reflections programs dumped | fault | result |
|---|---|---|---|---|---|
| C2 | `-fr1-cache=control` | `ARMED Control reload=true records=18` → `MOUNT_HELPER_OK` → `RELOAD_REQUESTED` | 1 original RAYS (`271ec9634b1ab87b`), 0 FULL; 123 DXIL | thread 0140, last dump 271ec `.spv`, 1 ms; `glvkspirv +0x157c88`; 90 ms after `RELOAD_REQUESTED` | CTD during boot, no ChangingMap: reproduces C1/D/E |
| Q2 | `-fr1-cache=noop-noreload` | `ARMED Noop reload=false records=18` → `MOUNT_HELPER_OK` → `EXPECTED_DXIL_SHA256=516fc383…` → `NO_RELOAD_REQUESTED` | **the no-op** `4f866e2c54fc9064` (DXIL sha256 `516fc383…` = expected), dumped 18×; **0 original RAYS**; **all 36 FULL**; 2 ReflectionConvolution; 476 DXIL | **none**: 0 `c0000005` in the 1.88 GB log | menu → New Game loaded, ran ~1 min; two saves loaded in the same process; quit through the menu (exit code 0) |
| R2 | empty | `UNARMED` (probe installed and enabled) | 1 original RAYS (`38121decbc3eee12`), 0 FULL; 115 DXIL | thread 013c, last dump 38121 `.spv`, 2 ms; same site; 19 ms after `before-LoadBinAssets` | menu → CTD on New Game: the original crash |

- **MEASURED — normal world loading consumes the overlay WITHOUT a forced reload (Q2).** The probe left `ForceShaderCacheReload` false
  (its own witness). At New Game's first `before-LoadBinAssets` (Proton 21659.949), loading thread 013c dumped the no-op **18 times**
  in 17 ms (21659.961–.978), one per covered RAYS record, then all 36 REFLECT_FULL programs (to 21661.005), with no fault. That is
  the stage where leg A (§9) and R2 die on 38121. No Q2 dump matches any original RAYS digest. ⇒ The overlay reaches the pipelines
  the normal first world load creates. F2's forced rebuild is not needed, which answers the route report's §8.3 open question for this path.
- **MEASURED — the first world load builds the whole Reflections family, and later loads build none of it.** Q2 dumped all 54
  Reflections records at the first map change (18 no-op + 36 FULL). It dumped none of them at the later map changes or at either
  save load, although vkd3d does not de-duplicate (the same no-op dumped 18×). ⚠️ So both save loads ran on pipelines already created
  in this process. **A cold launch straight into a save is NOT SAMPLED.** It is that process's first world load and is expected to take
  the same path. This also sharpens the dev reply's "built at world load even when Off" claim: 1.1.0 builds every cached Reflections.fx
  variant, the debug ones included, at the first world load with Reflections Off.
- **MEASURED — REFLECT_FULL passes NVVM 580: 36 of 36** were dumped on 013c with no fault, and the process then ran ~5 min (§10 had 1 of 36).
  Astra's caveat stands: a dump is not an instrumented pipeline return. Here the evidence is survival plus the owner's loaded worlds.
- **MEASURED — the reversal (R2).** The probe was still installed and enabled with no marker, so it logged `UNARMED` and mounted nothing.
  The first world load rebuilt `38121decbc3eee12` from the original bytes and faulted on the same thread 2 ms later at `+0x157c88`.
  R2's 115 DXIL equals the original dump run's count (§10 grounding). ⇒ The treatment is what made Q2 load, and Q2 left nothing the next
  launch reused on this path.
- **MEASURED — the control is valid (C2):** the boot crash on 271ec, 1 ms, same thread, as C1/D/E. The witness lines rule out marker, gate or
  setup drift.
- **Count, graded:** still three distinct original RAYS programs attributed to faults (38121, 271ec, a26e); C2/R2 repeat two of them. With
  all 18 replaced, nothing else faulted in three world loads. §8.2's working completeness hypothesis ("a fault in another family would
  falsify it") is **not falsified in this sample**; it is not proven for other maps, settings or drivers.
- **Owner statements reconciled.** The world-loading leg was **Q2** (not F2). The game log names the two saves. Save 1 (Lua 03:19):
  `BlankTerraceBig_05`, orig 403908, mods `SMR_CommunityFixPack`; this is the Intel-made 1.1.0 save per the owner (not identified from
  the log). Save 2 (04:32): `BlankBig_02`, mods TestKit + fix pack, i.e. the owner's Windows colony (checklist item 5 names that map).
  Both loaded with the fix pack "present, but not loaded" and TestKit missing, so they ran as vanilla + probe. "Fully functional" is
  owner-witnessed.
- **NOT MEASURED:** whether the picture matches Reflections Off (no comparison was made); what the no-op does with Reflections **On**;
  a cold launch into a save; other maps; packed-mod (`ModContent.fpk`) delivery; Windows/AMD with the overlay installed.
- **MEASURED: no other error the log can see in Q2 (owner's ask, 09-11: "any other errors I was not able to see?").** Every
  `err:`/`fixme:` line and every vkd3d/vulkan/d3d `warn:` line was bucketed by shape in all three legs (C2 50 shapes, R2 55, Q2 54).
  There is no `err:vulkan`, `err:vkd3d`, `VK_ERROR`, device-lost or `c0000005`, and the game log has no Lua error. Only two shapes are
  Q2-only. (a) `warn:vkd3d-proton:d3d12_resource_QueryInterface: {6b3b2502-6e51-45b3-90ee-9884265e8df3} not implemented, returning
  E_NOINTERFACE`, ×4 at 21666.870 (PreGame map load, 7 s after the Reflections builds). (b) `fixme:kernelbase:AppPolicyGetProcessTerminationMethod`
  at the clean exit, which the crash legs never reach. (a) is a CPU-side COM query on a resource, not shader content. It is
  **UNATTRIBUTED**: no vanilla world load on 580 exists to compare, and `C:\Dev\SMR-FR1-Evidence\` holds no world-loading Proton log (0 hits).
  A 595 or Intel world-load Proton log from the same laptop would settle it. The 1.88 GB is volume, not errors: PROTON_LOG's unwind trace,
  plus 3.6 M `ResourceBarrier: Issuing split barrier(s)` warnings that vanilla R2 also prints (900 in its short run).
- **Unexplained, verbatim (DISPATCH §2), attribute only if asked:** (1) an extra `-fr1-cache=control` launch,
  `Mars.exe-20260911-01.47.24`, whose game log stops at `*** Debug::Init()`. R2's crashed log stops at the same line, the shape a crash
  leaves. Its Proton log was overwritten by the next launch. **Owner-attributed 09-11:** the launch option was set before the mod was
  enabled, so this was a setup launch, not a leg. It was followed by `01.47.47`, no marker, `UNARMED`,
  menu, clean exit at 34 s: the recipe's pre-leg check. (2) `Failed activating D3D12 Dred` and `[Console Error]
  OptionsData.Options.Upscaling sets hr.ResolutionUpscale which was already set by another table` (every leg; both already listed). (3)
  `err:msvcrt:msvcrt_get_flags incorrect mode flag: x` brackets the dump lines on the faulting threads (C2 152397/152399, R2
  414729/414731).
- **Routed:** scope decision (fix pack / separate opt-in mod / instructions) is the owner's, ck145; if productized, Astra gets a
  round-3 brief (Windows/AMD with Reflections On, a self-gate with no Proton detector per EF-089, Reflections turned On, packed delivery,
  H-02/H-03/H-10). Dev reply FOLLOW-UP POST 2 drafted (`FR1_DEV_REPLY_2026-09-10.md`).

## 12 · 2026-09-11 — P1: the temporary workaround mod, PACKED, works on the laptop (owner-witnessed)

The build is `SMR_FR1TempWorkaround` (`C:\Dev\SMR-FR1-TempMod-2026-09-11\`, outside git; built by `smr-bugfixpack-5d` at the owner's
ask). It is Q2's path with no marker and no reload. Steps are in checklist 145 P1.
- **OWNER-WITNESSED:** "That pakd mod is working" (09-11), on the laptop from the Mod Editor pack. The same hour: "I have also
  tested reflections on low and high and I can still get into a colony mid run and cold boot with them enabled", then "Ultra works
  as well". ⇒ On the owner's word, §11's unsampled cold launch into a save is closed (cold boot straight into a colony), and
  Reflections On (Low, High, Ultra; Medium not reported) does
  not crash with the overlay, whether switched mid-run or set at boot. **Visuals with Reflections On: owner saw nothing wrong, on a bare colony
  with few reflective surfaces ("I don't know I didn't see anything"); NOT properly tested.** The stand-in writes nothing to the
  reflection target, so glitchy or missing reflections are INFERRED likely. The owner ruled the store page says exactly that:
  it loads, may have issues, isn't fully tested, and Off is recommended.
- **MEASURED desk — what was packed:** `ModUpload\Pack\ModContent.fpk`, 100,411 B, 02:43:03. `tools/pack_list.py --tree` against the
  staged folder gives 21 entries: code, `items.lua` and all 18 `Noop/ShaderCache` records byte-identical to the current build; `metadata.lua`
  differs (1,162 B = the pre-store-page version; no preview entry). ⇒ P1 exercised the shipping code and payload. The upload's
  `CreatePackageForUpload` re-packs the current folder (`GedModEditor.lua:713-733`), so it carries the new metadata and picture.
- **MEASURED: P1's log** (`C:\Dev\Success\fr1-packed-proof.zip`, extracted beside it; one launch: New Game, Reflections HIGH, per
  the owner's `TEST-RESULT.txt`). It shows `Loaded mod def TEMPORARY … (id SMR_FR1TempWorkaround, v0.00-001) packed from appdata`, then
  `[FR1 Temp Workaround] ACTIVE … (SSR=1)` and the SSR-on `WARNING`; only `SMR_FR1TempWorkaround` loaded mod items. The stand-in
  `4f866e2c54fc9064` was dumped **18×** on thread 013c (25475.714–.730). The log holds 348 distinct DXIL (510 dump lines), **0
  `c0000005`**, 36/36 REFLECT_FULL, none of 38121/271ec/a26e, and exit code 0. ⇒ The #1 risk from §11, packed delivery, is
  **answered and MEASURED**: `DlcMountFolder` on a folder inside a mod's `ModContent.fpk` works.
- **MEASURED: the dump-name rule.** vkd3d names a dump by the 64-bit FNV-1 hash of the DXBC blob. Three Q2 dumps reproduce their own
  names, and the rule maps 38121/271ec/a26e to cache keys 14281071190732923386/12556516658419309610/5519638363063710019 (§8, §10).
  ⇒ a Proton log alone can identify cached programs, without the dump files.
- **MEASURED: the 5 DXIL in P1 never seen in Q2 (Reflections High).** `3c6ebc2a5299d67f` is cached compute `8728250156999904579`,
  `SinglePassDownsample.fx|REDUCE_MIN…` (on the route report's §8.2 watch list; not a replaced key), dumped during the PreGame
  load. `936b11865bd194f2`, `eafb0d16984cf7f7`, `2bfc5215a03eac7e` and `d351fa9ffff99063` are **not among the 228 cached compute
  programs**, so none is one of the 18 RAYS records. They are most likely graphics shaders, UNIDENTIFIED without their bytes, and
  were dumped ~38 s into play on thread 015c. All 5 compiled with no fault.
- **PUBLISHED 09-11 (owner):** Paradox `pdx_id` 158711, Steam `steam_id` 3799500849. **MEASURED via Steam's public API**
  (`GetPublishedFileDetails`): result 1, visibility 0 (public), title as built, tag Other, file 164,043 B, created 07:09:48Z. The
  description auto-filled as the plain text (3,089 chars, no BBCode). The upload saves bumped `version` to 3 and rewrote
  `items.lua` (`FileName` → `CodeFileName`; the `code` list was kept). The Mods-folder copy is the master; the source copy was
  re-synced from it (22 files identical), and the description still matches the UPLOAD_WORKFLOW Paradox block word for word.
- **FIELD REPORT 1 (Steam Workshop comment, "Artificial Insanity", read 2026-09-11 from the owner's screenshot), verbatim:** "Didn't
  work, still crashes on "new game". Game version 1.1.0.403908 / Distro: Manjaro Linux KDE, kernel 6.18.49-1 / Wayland (might be
  the problem, but X11 isn't "supported" anymore) / NVIDIA GeForce GTX 1070 (Driver 580.178.04) / Intel 6600K CPU (iGPU is disabled
  due to problems, so NOT hybrid graphics) / Proton Hotfix / Initially had Reflections Medium, but tested again with them turned Off
  since Medium is the one configuration not mentioned. Still didn't work. Tested after disabling the mod as instructed."
  **UNATTRIBUTED; three hypotheses that need different fixes.** H1: the **Workshop-delivered** copy does not mount. P1 used an
  appdata pack; the Steam-delivered path is desk-equivalent only (`Mod.lua:872`, the same `Mod/<id>/` content path), so it would hit
  every player. H2: **Pascal** (GTX 1070) faults on a different shader (P1/Q2 were Ampere RTX 3070). H3: the mod did not activate
  (not enabled or restarted, or a gate declined). **Splitters:** the owner subscribes on the laptop with the appdata copy removed
  (falsifies H1 cheaply); the player's Proton log gives the `[FR1 Temp Workaround]` line (H3) and the dump just before the fault on
  the faulting thread (H2, identifiable from the log alone by the FNV-1 rule above). The request for the log is drafted for the owner.
- **Discrepancies, verbatim:** (1) `TEST-RESULT.txt` gives the launch line as `PROTON_LOG=1 %command% -fr1-cache=noop-noreload` (no
  `VKD3D_SHADER_DUMP_PATH`), yet the log holds dump lines, so a dump path was set; the dump files are not in the zip. (2) The old
  probe marker was still on the command line; it is inert (no probe mod def loaded, and the temp mod reads no marker). (3) "World
  observed for several minutes": the log shows ~77 s between `BlankBigTerraceCMix_20` loading (25497.0) and the quit (25574.4). (4)
  The owner's cold boot into a colony and the Low/Ultra runs were separate launches. Each launch overwrites Steam's log, so only this
  run is measured; those stay owner-witnessed.
