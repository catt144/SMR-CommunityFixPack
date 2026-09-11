# FR-1 — reply for the Steam discussion (Paradox dev tracking it) — DRAFT, NOT POSTED

⛔ The owner posts; no agent posts. Written 2026-09-10 by `smr-bugfixpack-f0` from
`FR1_LINUX_FINDINGS_2026-09-10.md` (§1, §6, §7) and `FR1_OPTIONS_2026-09-10.md` (§1, R9).
Every line is MEASURED except where it says otherwise. Plain text, safe in a Steam post.
Files offered: `C:\Dev\SMR-FR1-DevPackage.zip` (redacted, checksummed; outside git).
⚠️ One open check: the shader-dump run was at Reflections Low OR Off (owner: "my test
attempted reflections low and off"), not confirmed which — a single Off-only dump run makes
"built while SSR is disabled" measured. The post says so.

---

Linux / NVIDIA 580 crash on world load — narrowed to one shader (evidence below)

Hi — I maintain the Relaunched Fix Pack. I set up a Linux test machine to reproduce the crash in this thread, and I think we have narrowed it to one specific shader. Posting the findings in case they help.

SHORT VERSION
On NVIDIA driver 580, every world load (New Game, or loading a save) crashes inside NVIDIA's shader compiler while the game is creating the compute pipeline for the screen-space reflections shader (Shaders/Reflections.fx, REFLECT_RAYS variant). The same laptop loads worlds fine on its Intel GPU or on NVIDIA 595. Setting Reflections to Low or Off does not avoid it.

SETUP
Alienware m15 R4, RTX 3070 Laptop GPU. Linux Mint 22.2, X11, kernel 7.0.0-31. Proton Hotfix (hotfix-20260828). Game 1.1.0.403908 (Steam build 24995074), vanilla, no mods.

WHAT WE TESTED
- NVIDIA 580.173.02, proprietary and open modules: crash on New Game, and also when loading a 1.1.0 save made on the Intel GPU.
- NVIDIA 595.84-open: world loads. Intel GPU (Mesa): world loads.
- Reflections Low and Off: still crashes.
- Film grain forced off (verified in the log): still crashes.
- VKD3D_DISABLE_EXTENSIONS=VK_NV_raw_access_chains: still crashes.
- MarsDebug straight into a map: same crash, so the menu and New Game UI are not involved.

THE CRASH (PROTON_LOG=1 with VKD3D_SHADER_DUMP_PATH set)
Right after "*** Reloading assets from folder 'BinAssets/'", all on the same thread (025c):
7537.824 - vkd3d dumps shader 38121decbc3eee12.dxil
7537.829 - vkd3d dumps 38121decbc3eee12.spv
7537.831 - access violation 0xc0000005 in libnvidia-glvkspirv.so.580.173.02 +0x157c88 (_nv014nvvm +0x9c)
7537.832 - err:vulkan:vkCreateComputePipelines Exception 0xc0000005
Nothing else happens on that thread in between. A compute pipeline holds one shader, so the pipeline NVIDIA was compiling when it crashed was built from 38121decbc3eee12.

THE SHADER
38121decbc3eee12 is Shaders/Reflections.fx compiled with REFLECT_RAYS (the 8x8 tiled SSR ray-march that writes the TileCounter buffer). Proof: recompiling the shipped Reflections.fx with the game's own dxcompiler.dll (cs_6_6, REFLECT_RAYS, HLSL 2021, row-major matrices) gives byte-identical DXIL, PSV0 and HASH chunks. The same bytecode is also in ShaderCached3d12.fpk (entry 14281071190732923386).

WHY 1.1.0 SEEMS TO HAVE CHANGED THINGS
This looks like the NVIDIA compiler bug from vkd3d-proton issue #2701 (November 2025, driver 580). Back then, on 1.0.7, it only crashed with Reflections above Low, and pyroveil added a workaround for that shader's old hash (b73d41d886185985). On 1.1.0 the shader's hash has changed, so that workaround no longer matches, and the crash now happens with Reflections Low or Off too. That suggests 1.1.0 creates the REFLECT_RAYS pipeline at world load whether or not reflections are enabled. One caveat: our shader-dump run was at Low or Off, and I haven't confirmed which. I can repeat it at Off specifically if that helps.

WHY DRIVER 595 ISN'T A FIX FOR EVERYONE
NVIDIA's 580 branch is the last one for Maxwell, Pascal and Volta GPUs (GTX 900 and 1000 series, Titan V): https://nvidia.custhelp.com/app/answers/detail/a_id/3142. Those players can never move to 595, and most affected players in this thread say they can't.

POSSIBLE FIXES ON YOUR SIDE (suggestions only; you know the engine)
1. Create the REFLECT_RAYS pipeline only when reflections are actually enabled, or defer it until first use. That alone would let NVIDIA 580 players play with Reflections Off.
2. Restructure that shader. The pyroveil workaround for the old hash worked by rewriting the shader through GLSL, so a differently structured version of the same code compiled fine on 580.
3. Expose a startup setting that skips it.

WHAT WE HAVEN'T SHOWN YET
We haven't yet run the test that swaps out just this one shader and makes the crash go away; that's our next step. We also can't see the engine's native pipeline-creation code, so "built at world load even with reflections off" is our reading of the evidence, not something we have seen in the code.

FILES
I have the shader bytecode (.dxil and .spv), the Proton crash excerpt, the shader-dump timeline, driver and system info, and the byte-identity receipt, all with checksums. Happy to share them however suits you.

Thanks for tracking this.
