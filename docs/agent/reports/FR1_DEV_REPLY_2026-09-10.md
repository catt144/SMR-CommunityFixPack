# FR-1 — reply for the Steam discussion (Paradox dev tracking it) — POSTED by the owner (no dev response yet, 09-11)

> **Owner, 2026-09-11:** posted, editable, "doesn't look like it's been read yet". The text below is the CURRENT version.
> Three passages changed after the owner posted: the end of "WHY 1.1.0 SEEMS TO HAVE CHANGED THINGS", the new
> "It is also not just one shader" paragraph, and "WHAT WE HAVEN'T SHOWN YET". These are the owner's paste-in edits.

⛔ The owner posts; no agent posts. Written 2026-09-10 by `smr-bugfixpack-f0` from
`FR1_LINUX_FINDINGS_2026-09-10.md` (§1, §6, §7) and `FR1_OPTIONS_2026-09-10.md` (§1, R9).
Every line is MEASURED except where it says otherwise. Plain text, safe in a Steam post.
Files offered: `C:\Dev\SMR-FR1-DevPackage.zip` (redacted, checksummed; outside git).
✅ The open check was ANSWERED on 09-10 late by the owner's Off-only legs (FINDINGS §9): SSR read 0 before the load, and the
crash was on 38121 on the same thread. The post below was updated to match and adds the second crashing RAYS variant. If the
owner already posted the earlier text, this becomes a follow-up post.

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
This looks like the NVIDIA compiler bug from vkd3d-proton issue #2701 (November 2025, driver 580). Back then, on 1.0.7, it only crashed with Reflections above Low, and pyroveil added a workaround for that shader's old hash (b73d41d886185985). On 1.1.0 the shader's hash has changed, so that workaround no longer matches, and the crash now happens with Reflections Low or Off too. 1.1.0 creates the REFLECT_RAYS pipeline at world load even with reflections disabled. In a repeat run with Reflections Off, the game's own setting read hr.EnableScreenSpaceReflections = 0 just before the world load, and the crash was on the same shader, on the same thread, 1 ms after it was dumped.

It is also not just one shader. Forcing a shader-cache reload (hr.ForceShaderCacheReload = true) makes the game rebuild its reflection pipelines during startup, and driver 580 then crashes the same way on a second REFLECT_RAYS variant (USE_HYPERBOLIC_DEPTH + REFLECT_IMPORTANCE_SAMPLE, hash 271ec9634b1ab87b), before the main menu appears. So the ray-queue kernel as a family seems to be what trips NVIDIA's compiler.

WHY DRIVER 595 ISN'T A FIX FOR EVERYONE
NVIDIA's 580 branch is the last one for Maxwell, Pascal and Volta GPUs (GTX 900 and 1000 series, Titan V): https://nvidia.custhelp.com/app/answers/detail/a_id/3142. Those players can never move to 595, and most affected players in this thread say they can't.

POSSIBLE FIXES ON YOUR SIDE (suggestions only; you know the engine)
1. Create the REFLECT_RAYS pipeline only when reflections are actually enabled, or defer it until first use. That alone would let NVIDIA 580 players play with Reflections Off.
2. Restructure that shader. The pyroveil workaround for the old hash worked by rewriting the shader through GLSL, so a differently structured version of the same code compiled fine on 580.
3. Expose a startup setting that skips it.

WHAT WE HAVEN'T SHOWN YET
We haven't yet run the test that swaps out just this one shader and makes the crash go away. We also can't see the engine's native pipeline-creation code: "built at world load even with reflections off" is what the runtime logs show, not something we have read in the code. We also tried the hidden SSR settings from a mod (hr.SSRFullTile8x8 = 1, and alongside a forced cache reload). Neither changed which reflections shader the game built, so there doesn't seem to be a setting a mod can use to avoid it.

FILES
I have the shader bytecode (.dxil and .spv), the Proton crash excerpt, the shader-dump timeline, driver and system info, and the byte-identity receipt, all with checksums. Happy to share them however suits you.

Thanks for tracking this.

---

## FOLLOW-UP POST 1 — POSTED by the owner (confirmed 09-11); drafted 2026-09-11 from FINDINGS §10

Every line is MEASURED unless it says "we think" / "if we read it right". Hold the "swap makes it go away" claim for FOLLOW-UP 2
(Astra's v2 covering all 18 REFLECT_RAYS records).

---

UPDATE — shader swap test (partial)

We tested replacing the REFLECT_RAYS shaders ourselves. A test mod layered a small ShaderCache folder over the game's cache using the game's own DlcMountFolder helper. In it, the six non-debug REFLECT_RAYS entries were replaced by an empty compute shader with the same root signature. The mod then forced a shader-cache reload.

- The game used our replacement: the shader vkd3d dumped matches the empty shader byte for byte.
- The game got past the REFLECT_RAYS pipelines that had been crashing. It built about twice as many shaders as the control run, including the REFLECT_FULL (tile 16) compute shader, which NVIDIA 580 compiled with no problem.
- It then crashed at the same place in NVIDIA's compiler (libnvidia-glvkspirv.so.580.173.02 +0x157c88) on a REFLECT_RAYS variant we hadn't replaced: USE_HYPERBOLIC_DEPTH + REFLECTION_DEBUG + REFLECTION_ITERATIONS, hash a26e0bbfe7751fbf, on the same thread, 1 ms after it was dumped.

With the same mod loading the original, unchanged shaders instead, the game crashes exactly as before.

So three different REFLECT_RAYS programs now crash driver 580 (38121decbc3eee12, 271ec9634b1ab87b, a26e0bbfe7751fbf). The one REFLECT_FULL program we saw compiled fine. Two related observations:
- With hr.SSRTraceHiZ = 1, the game still built the REFLECT_RAYS variant without TRACE_HIZ, so the live SSR settings don't seem to choose which variant gets built.
- A forced shader-cache reload rebuilds every cached Reflections.fx variant, including the debug ones, during startup.

What this suggests on your side (you know the engine better than we do):
- Not building REFLECT_RAYS when reflections are Off would unblock NVIDIA 580 players.
- The REFLECT_FULL path compiles on 580. If we read the Lua right, the game already switches AMD cards to a "full tile" path (hr.SSRFullTile8x8 = 1), so using REFLECT_FULL on NVIDIA as well might be a low-risk option.

We're next testing a replacement for all 18 REFLECT_RAYS cache entries (the 12 debug variants included) and will post the result. Happy to share the test mod, the cache records and the logs.

---

## FOLLOW-UP POST 2 — draft 2026-09-11 (from FINDINGS §11) — ⛔ SUPERSEDED by "CURRENT DEV NOTE" below unless already posted

Every line is MEASURED unless it says "suggestions" / "if we read it right". POST 1 is up (owner, 09-11), so this posts as-is.
Owner 09-11: yes, a later post will mention the temporary workaround mod once it is live. Draft that as POST 3 when the listing exists.

---

UPDATE 2 — replacing the REFLECT_RAYS shaders makes the crash go away

We extended the test to all 18 REFLECT_RAYS entries in the shader cache: the 6 regular variants and the 12 REFLECTION_DEBUG ones. Each was replaced by the same empty compute shader with the original root signature. The 36 REFLECT_FULL entries and every other shader were left untouched. Same laptop, NVIDIA 580.173.02, Reflections Off. This time the mod did not force a shader-cache reload; it only layered the replacement folder over the cache.

- New Game loaded and ran normally. Two 1.1.0 saves then loaded in the same session.
- Right after "*** Reloading assets from folder 'BinAssets/'" (exactly where the original crash happens), vkd3d dumped our empty shader 18 times on the loading thread, once per replaced entry. None of the original REFLECT_RAYS shaders was built.
- The same thread then built all 36 REFLECT_FULL compute shaders. NVIDIA 580 compiled every one of them with no fault.
- There was no access violation anywhere in the Proton log.

Then the reverse: with the mod still installed but not switched on, New Game crashed exactly as before. The shader was 38121decbc3eee12, the crash was at libnvidia-glvkspirv.so.580.173.02 +0x157c88, on the same thread, 2 ms after the dump. A control run loading the original shaders through the mod crashed during startup as before (271ec9634b1ab87b).

So on driver 580 it is the REFLECT_RAYS shaders: take them out of the cache and the world loads; put them back and it crashes.

One more observation: with Reflections Off, 1.1.0 built all 54 cached Reflections.fx variants (the debug ones included) at the first world load, and none again at later loads in the same session.

Suggestions for your side (you know the engine):
- Not creating the REFLECT_RAYS pipelines while reflections are Off would fix this for NVIDIA 580 players.
- All 36 REFLECT_FULL variants compile on 580. If we read the Lua right, the game already uses the full-tile path on AMD (hr.SSRFullTile8x8), so that path looks like a workable option for NVIDIA on Linux when reflections are on.

What we haven't shown: that the picture is identical to Reflections Off (we didn't compare), or what happens with Reflections On while the empty shader is in place (we kept it Off). The test mod is a bench tool and isn't published. Happy to share it, the cache records and the logs.

---

## FOLLOW-UP POST 3 — draft 2026-09-11 (the temporary mod is LIVE) — ⛔ SUPERSEDED by "CURRENT DEV NOTE" below

⚠️ If POST 2 is not up yet, post it first. POST 2's last paragraph says "The test mod is a bench tool and isn't published". That is
still true of the bench probe, but it reads oddly next to this, so either delete that sentence from POST 2 or post both together.
Every line is MEASURED or a published fact.

---

UPDATE 3 — a temporary workaround mod for players stuck on driver 580

Until there's a fix on your side, we've published a clearly marked temporary workaround for Linux players on NVIDIA driver 580:
- Steam Workshop: https://steamcommunity.com/sharedfiles/filedetails/?id=3799500849
- Paradox Mods: https://mods.paradoxplaza.com/mods/158711/Any

It uses the same approach as the test above: at startup it layers the empty compute shader over the 18 REFLECT_RAYS entries in the shader cache. No game files are modified, and nothing is written into saves. It only acts on NVIDIA + D3D12 on build 1.1.0.403908, and it switches itself off after any game update, so it won't linger past your fix. The page tells players to keep Reflections Off and to remove it as soon as you ship a fix.

On our test laptop it loads New Game and existing saves on driver 580. We tested one machine only, and the page says so.

We'd much rather see this fixed properly, and we'll retire the mod the moment it is.

---

## ⭐ CURRENT DEV NOTE — ONE POST, 2026-09-11 late (replaces POSTS 2 + 3)

**Use this instead of POSTS 2 and 3**, as a new reply after POST 1 (which is up). ⚠️ **If you already posted POST 2**, post only
the part from "A TEMPORARY WORKAROUND" down. Every line is MEASURED, published, or the owner's own observation ("including
straight from a fresh launch" and the Low/Ultra runs are the owner's). Plain text, safe in a Steam post.

---

UPDATE 2 — replacing the REFLECT_RAYS shaders stops the crash, and a temporary workaround is out

Following on from the partial swap test above: we extended it to all 18 REFLECT_RAYS entries in the shader cache (the 6 regular variants and the 12 REFLECTION_DEBUG ones), each replaced by the same empty compute shader with the original root signature. The 36 REFLECT_FULL entries and every other shader were left untouched. Same laptop, NVIDIA 580.173.02. This time nothing forced a shader-cache reload; the replacement folder was simply layered over the cache at startup.

- New Game loaded and ran normally. 1.1.0 saves loaded too, including straight from a fresh launch.
- Right after "*** Reloading assets from folder 'BinAssets/'" (exactly where the crash happens), vkd3d dumped our empty shader 18 times on the loading thread, once per replaced entry. None of the original REFLECT_RAYS shaders was built.
- The same thread then built all 36 REFLECT_FULL compute shaders. NVIDIA 580 compiled every one of them.
- No access violation anywhere in the Proton log. With Reflections set to Low, High or Ultra the game also loaded, and the Proton log from the High run is just as clean.

Then the reverse: with the mod installed but not switched on, New Game crashed exactly as before, on 38121decbc3eee12 at libnvidia-glvkspirv.so.580.173.02 +0x157c88, on the same thread, 2 ms after the dump. A control run loading the original shaders through the mod crashed during startup as before (271ec9634b1ab87b).

So on driver 580 it is the REFLECT_RAYS shaders: take them out of the cache and the world loads; put them back and it crashes.

One more observation: with Reflections Off, 1.1.0 built all 54 cached Reflections.fx variants (the debug ones included) at the first world load, and none again at later loads in the same session.

A TEMPORARY WORKAROUND
Since most affected players can't move to driver 595, we've published this as a clearly marked temporary mod for Linux players on driver 580:
Steam Workshop: https://steamcommunity.com/sharedfiles/filedetails/?id=3799500849
Paradox Mods: https://mods.paradoxplaza.com/mods/158711/Any

It layers the empty shader over the 18 REFLECT_RAYS cache entries at startup. It doesn't modify any game files or write anything into saves. It only acts on NVIDIA with D3D12 on build 1.1.0.403908, and it switches itself off after any game update, so it won't linger once you ship a fix. The page asks players to keep Reflections Off and to remove it as soon as a fix is out. We'd much rather see this fixed properly, and we'll retire the mod the moment it is.

SUGGESTIONS (you know the engine better than we do)
- Not creating the REFLECT_RAYS pipelines while reflections are Off would fix this for NVIDIA 580 players.
- All 36 REFLECT_FULL variants compile on 580. If we read the Lua right, the game already uses the full-tile path on AMD (hr.SSRFullTile8x8), so that path looks like a workable option for NVIDIA on Linux when reflections are on.

WHAT WE HAVEN'T SHOWN
That the picture with the empty shader matches Reflections Off (we didn't compare), or how reflections look with Reflections on (not properly tested, and very likely wrong). And it's one test machine.

Happy to share the mod, the cache records and the logs.

---

## 📋 PLAYER REPLY — for players asking for help in the thread (2026-09-11)

Plain text, safe in a Steam discussion. It can be reused as-is in any thread. Every claim matches the store page.

---

If you're on Linux with an NVIDIA card on driver 580, and the game crashes to the desktop when you start a New Game or load a save (1.1.0), there's now a temporary workaround mod while we wait for Paradox's fix:

Steam Workshop: https://steamcommunity.com/sharedfiles/filedetails/?id=3799500849
Paradox Mods: https://mods.paradoxplaza.com/mods/158711/Any

How to use it:
1. Subscribe to the mod.
2. Start the game. On the main menu, open MOD MANAGER and enable "TEMPORARY - Linux NVIDIA 580 Crash Workaround".
3. Recommended: Options, then Video, set Reflections to Off.
4. Quit the game completely, then start it again.
5. Start a New Game or load your save.

What it does: driver 580's shader compiler crashes on the game's screen-space reflection shaders, which 1.1.0 prepares even with Reflections Off. The mod swaps those shaders for an empty stand-in, so the world loads. Reflections will very likely look wrong if you turn them on, so keep them Off.

Please remove it as soon as Paradox releases a fix (it also switches itself off after any game update). It doesn't change your saves, and you don't need it on Windows, Steam Deck, AMD or Intel graphics, or NVIDIA driver 595.

It's been tested on one laptop (RTX 3070, Linux Mint 22.2, driver 580.173.02, Proton Hotfix), so it may not work on every setup. Whether it helps or not, please reply with your graphics card, driver version, Linux distribution and Proton version. That helps us, and it helps Paradox track the bug down.
