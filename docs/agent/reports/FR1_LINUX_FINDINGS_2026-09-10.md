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
