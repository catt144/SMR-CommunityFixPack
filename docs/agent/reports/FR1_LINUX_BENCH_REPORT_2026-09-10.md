# Linux Test Bench Reproduction Report
## Surviving Mars: Relaunched 1.1.0 — Linux/NVIDIA world-load CTD

**Date:** 2026-09-10  
**Purpose:** Hand-off for the bug-fix/mod agents. This report captures what was reproduced on a physical Linux test bench, what was ruled out, and the most useful next engineering targets.

## Executive summary

A dedicated Linux Mint 22.2 test bench was built on an Alienware m15 R4 to reproduce Linux crash reports for **Surviving Mars: Relaunched 1.1.0**.

The issue reproduced immediately and consistently on **NVIDIA 580.173.02**:

- Game launches normally; EULAs/front-end/menu work.
- **New Game** causes an immediate CTD.
- **Reflections = Low** still crashes.
- **Reflections = Off** still crashes.
- Same 1.1.0 build works on the laptop's **Intel integrated GPU**.
- A save created successfully on Intel also **crashes when loaded on NVIDIA 580**, so the failure is not specifically new-game generation or save creation.
- **NVIDIA 580-open + PRIME On-Demand** still crashes.
- **NVIDIA 595-open + PRIME On-Demand** works normally.

The strongest crash evidence is in the Proton log. Immediately after the engine reports reloading `BinAssets/`, the NVIDIA Vulkan shader compiler faults:

```text
Exception 0xc0000005
/usr/lib/pressure-vessel/overrides/lib/x86_64-linux-gnu/libnvidia-glvkspirv.so.580.173.02 + 0x157c88

err:vulkan:vkCreateComputePipelines Exception 0xc0000005 in Unix call.
```

Working hypothesis: **1.1.0 reaches a compute/shader pipeline during playable-world initialization that crashes NVIDIA's 580-generation Vulkan/SPIR-V compiler.** The front-end is not sufficient to trigger it. Intel works, 595-open works, and both New Game and Load fail on 580.

## Physical test bench

### Hardware

- **Laptop:** Alienware m15 R4
- **CPU:** Intel Core i7-10870H, 8C/16T
- **RAM:** ~16 GB
- **Discrete GPU:** NVIDIA GeForce RTX 3070 Laptop GPU / Ampere, 8 GB
- **Integrated GPU:** Intel UHD / Comet Lake-H GT2
- **Linux SSD:** Samsung 970 EVO Plus 2 TB
- Linux installed into an approximately 200 GB dedicated area on the spare SSD.

This is a useful match for the original reporter because it is another Intel+iGPU / Ampere RTX 30-series hybrid laptop.

### OS / graphics stack

- **Distro:** Linux Mint 22.2 "Zara"
- **Desktop:** Cinnamon
- **Session:** X11
- **Kernel:** `7.0.0-31-generic`
- **Secure Boot:** disabled
- **Initial NVIDIA branch:** `580.173.02`
- **PRIME:** tested in Performance and On-Demand during investigation

Initial 580 version:

```text
580.173.02-0ubuntu0.24.04.1
```

`nvidia-smi` confirmed:

```text
NVIDIA-SMI 580.173.02
Driver Version: 580.173.02
```

## Steam / Proton environment

- **Steam AppID:** `3215050`
- **Game install directory:**

```text
/home/ladmin/.steam/debian-installation/steamapps/common/Project Spark
```

- **Compatdata/prefix:**

```text
/home/ladmin/.steam/debian-installation/steamapps/compatdata/3215050/pfx
```

Steam explicitly maps AppID 3215050 to **Proton Hotfix**:

```text
"3215050"
{
    "name"      "proton_hotfix"
    "config"    ""
    "priority"  "250"
}
```

Captured Proton build:

```text
Proton: 1787945902 hotfix-20260828-ptr-x86_64
SteamGameId: 3215050
Kernel: Linux 7.0.0-31-generic
```

The game log reports `Proton/Wine: 11.0`; this is the Wine generation inside the Steam-selected Hotfix.

Controls:

- Steam Cloud disabled for the game.
- Workshop subscriptions may exist, but mods were disabled.
- Tests are vanilla 1.1.0 unless stated otherwise.
- `PROTON_LOG=1 %command%` was enabled for the captured trace.

## Reproduction results

### A — Vanilla 1.1.0 / NVIDIA 580

1. Launch game.
2. Accept EULAs.
3. Reach front-end normally.
4. Click **New Game**.
5. Immediate CTD.

**Result: FAIL / reproducible.**

The game's own log stops very early:

```text
*** OS info
OS:             Windows 10
Version:        10.0.19045
Proton/Wine:    11.0

*** Debug::Init()
```

### B — Reflections workaround

On the failing 580 setup:

- Reflections **Low** → CTD.
- Reflections **Off** → CTD.

**Result:** the older Reflections Off/Low workaround is not sufficient for the currently reproduced 1.1.0 failure.

### C — Intel integrated GPU

Same laptop, same 1.1.0 build, Intel graphics path.

**Result: WORKS.** A playable world can be entered and a control save can be created.

### D — Load Intel-created control save on NVIDIA

A vanilla 1.1.0 save created successfully on Intel was loaded after returning to NVIDIA.

**Result: CTD.**

This proves the failure is **not specific to New Game generation**. A valid existing world also fails when the NVIDIA 580 rendering path initializes the playable world.

### E — NVIDIA 580-open / PRIME On-Demand

**Result: CTD.**

### F — NVIDIA 595-open / PRIME On-Demand

**Result: WORKS normally.**

### Matrix

| Rendering path | NVIDIA branch | PRIME mode | 1.1.0 world result |
|---|---:|---|---|
| Intel / Mesa | N/A | Intel path | **WORKS** |
| RTX 3070 / NVIDIA proprietary | 580.173.02 | Performance | **CTD** |
| RTX 3070 / NVIDIA open | 580.173.02 | On-Demand | **CTD** |
| RTX 3070 / NVIDIA open | 595.84 | On-Demand | **WORKS** |

**Not tested on this bench:** NVIDIA 580 proprietary + PRIME On-Demand. It was judged low-value after 580-open failed and 595-open passed, especially because the captured fault is in the 580 userspace shader compiler.

## Primary crash evidence

Immediately before the failure, the Proton trace contains repeated VKD3D D3D12 resource-barrier warnings and then:

```text
*** Reloading assets from folder 'BinAssets/'
```

About 25 ms later:

```text
Exception 0xc0000005 at
/usr/lib/pressure-vessel/overrides/lib/x86_64-linux-gnu/libnvidia-glvkspirv.so.580.173.02 + 0x157c88
```

Wine/Vulkan then reports:

```text
err:vulkan:vkCreateComputePipelines Exception 0xc0000005 in Unix call.
```

The nearby backtrace includes Proton Hotfix's `winevulkan.so`.

Interpretation: the immediate fatal event occurs in **NVIDIA's 580.173.02 Vulkan/SPIR-V shader compiler while Vulkan compute pipelines are being created**. Later RPC/service errors appear to be shutdown fallout rather than the initiating cause.

## External correlation

Existing upstream issue:

- **VKD3D-Proton #2701 — “Surviving Mars: Relaunched crash on Nvidia proprietary”**
- RTX 4080
- NVIDIA 580.105.08
- crash when starting game/tutorial
- same `libnvidia-glvkspirv.so` family
- same `0xc0000005` exception
- older reporter found the trigger only with Reflections above Low

URL: `https://github.com/HansKristian-Work/vkd3d-proton/issues/2701`

The older trace was around `+0x157c48`; this bench faults around `+0x157c88` on 580.173.02.

Do **not** assume the current 1.1.0 defect is identical to the old reflections-only case. This bench crashes with Reflections Low and Off. Possible explanations include a new/changed compute shader or pipeline in 1.1.0, changed driver behavior, or multiple problematic pipelines.

AMD/Linux crash reports also exist, but some fail at different phases (for example at/before main menu). Do not group every “Linux CTD” into this defect without matching the phase and trace signature.

## Separate PRIME / Steam desktop issue

A second issue was found while changing NVIDIA configurations:

- In NVIDIA **Performance** PRIME mode, launching Steam can terminate the Cinnamon/X11 user session and return to login.
- Switching PRIME to **On-Demand** allows Steam to launch normally.
- `steam -cef-disable-gpu` also allowed Steam to open when its Chromium UI caused the session failure.

Treat this as separate from the Mars world-load CTD unless later evidence links them. PRIME On-Demand is the preferred stable desktop configuration for further game testing.

## What has been ruled out / weakened

- **New Game generation itself:** ruled out as primary trigger; loading an Intel-created valid 1.1.0 save also crashes on NVIDIA 580.
- **Bad/corrupt save:** strongly weakened; same save works on Intel.
- **Reflections alone:** ruled out as a complete workaround on this bench; Low and Off still crash.
- **Generic Proton failure:** weakened; the immediate captured fault is in NVIDIA's 580 shader compiler, though VKD3D/game workload may still be what exposes it.
- **Bad RTX 3070 hardware:** effectively ruled out; same GPU works with NVIDIA 595-open.
- **All Linux GPUs affected by this exact defect:** unsupported; Intel works on this bench. AMD reports need signature-level comparison.

## Current technical hypothesis

```text
1.1.0 begins playable-world initialization
        |
        v
renderer/assets/pipelines required for the world are initialized
        |
        v
D3D12 compute pipeline passes through VKD3D -> Vulkan
        |
        v
NVIDIA 580.173.02 compiles/creates pipeline
        |
        v
libnvidia-glvkspirv.so.580.173.02
        |
        v
access violation 0xc0000005 in vkCreateComputePipelines
        |
        v
CTD
```

Because the menu works but both New Game and Load fail, the trigger is likely a shader/pipeline used by the **playable 3D world**, not the front-end.

Because 595-open works while 580-open fails in PRIME On-Demand, the highest-value distinction is currently **580-generation NVIDIA userspace/Vulkan behavior vs 595-generation behavior**, not PRIME mode.

## Recommended work for the bug-fix mod agents

### Priority 0 — inspect the 1.0.7 -> 1.1.0 renderer/world-init delta

The project already considers 1.0.7 broadly confirmed good, so focus on **what changed in 1.1.0 that causes a new/changed compute pipeline during world initialization**.

Compare:

- graphics/render initialization Lua;
- world-load hooks;
- renderer quality presets;
- reflections / SSR;
- contact shadows;
- post-processing;
- compute-based effects;
- asset reload/init around `BinAssets/`;
- new shader permutations/render defaults;
- features moved from lazy creation to world-load-time creation.

### Priority 1 — determine whether a mod can act early enough

A mod-side workaround is plausible only if it can alter renderer state **before** the offending pipeline is created.

Questions:

- When are mods initialized relative to playable-world render-pipeline creation?
- Can the mod set renderer `hr.*` / engine settings before map entry?
- Can it intercept world-init before shader creation?
- Are renderer settings persisted in a config/preferences file that can be pre-seeded?
- Can the relevant effect be disabled without first instantiating its shader?

If normal Lua mod execution begins after the failing pipeline is created, a pure mod-hook workaround may be impossible; a config/pre-init workaround may be required instead.

### Priority 2 — inspect shipped source

Linux bench source/tooling path:

```text
/home/ladmin/.steam/debian-installation/steamapps/common/Project Spark/ModTools/Src
```

Useful searches:

```bash
grep -RniE --include='*.lua' \
'reflection|screen.?space|ssr|contact.?shadow|shadow|taa|dlss|xess|upscal|render.?quality|compute' \
"/home/ladmin/.steam/debian-installation/steamapps/common/Project Spark/ModTools/Src"
```

Also search world-load/render-init code and anything touching `BinAssets`.

### Priority 3 — identify the exact offending shader/pipeline

If setting-level bisection is insufficient, use VKD3D/Fossilize debugging to identify the pipeline being compiled when `libnvidia-glvkspirv` faults.

Candidate tooling:

- `VKD3D_SHADER_DUMP_PATH`
- VKD3D debug output
- shader/pipeline hash comparison
- Fossilize pipeline capture/replay

Goal:

```text
580 crash
  -> exact shader/pipeline
  -> game asset/render feature requesting it
  -> earliest Lua/config point capable of suppressing or altering it
```

## Practical mitigation discovered

For a temporary Linux advisory:

- **NVIDIA 580.173.02:** reproduced world-entry CTD.
- **NVIDIA 595-open 595.84 + PRIME On-Demand:** worked normally on this RTX 3070 Laptop bench.
- **Intel/Mesa:** worked normally on the same machine.

Do not generalize “595 fixes everyone” from one bench, but it is a real workaround candidate.

## Evidence retained on the Linux bench

Crash evidence:

```text
/home/ladmin/Desktop/FR1-first-crash/
```

Contains/captured:

- Mars.exe game log;
- `pdxsdk.log`;
- Proton log `steam-3215050.log` (~106 MB);
- Mint info;
- kernel info;
- session info;
- PRIME info;
- `nvidia-smi`;
- `inxi -Gxxx`.

Baseline environment capture:

```text
/home/ladmin/Desktop/FR1-baseline/
```

Game log directory:

```text
/home/ladmin/.steam/debian-installation/steamapps/compatdata/3215050/pfx/drive_c/users/steamuser/AppData/Roaming/Surviving Mars Relaunched/logs/
```

## Things not to overstate

1. **1.0.7 was not independently rerun on this bench.** It was skipped because project/community evidence already treats it as known good.
2. **580 proprietary + PRIME On-Demand was not tested.** Current evidence makes it low priority.
3. **595-open working does not prove every 595 configuration or every NVIDIA GPU is fixed.**
4. **AMD crash anecdotes do not prove the same defect.** Compare exact crash phase and Proton/Vulkan trace.
5. A crash inside an NVIDIA library does not necessarily mean NVIDIA alone “caused” the regression. The 1.1.0 game/VKD3D workload may expose a latent NVIDIA compiler defect. For the mod, the key question is what changed in the workload and whether it can be avoided.

## Bottom line

The Linux test bench successfully reproduced the issue that could not be investigated from the Windows 11 development computer.

```text
Surviving Mars: Relaunched 1.1.0
Linux Mint 22.2 / X11 / kernel 7.0.0-31

Intel GPU:
    world loads -> PASS

NVIDIA 580.173.02:
    menu -> PASS
    New Game / enter world -> CTD
    load known-good Intel-created world -> CTD
    Reflections Low -> CTD
    Reflections Off -> CTD

NVIDIA 595-open / PRIME On-Demand:
    world loads -> PASS

580 crash signature:
    libnvidia-glvkspirv.so.580.173.02
    vkCreateComputePipelines
    Exception 0xc0000005
```

**Recommended direction:** stop treating this as a generic Linux CTD or New Game bug. Investigate the **1.1.0 playable-world render/compute pipeline delta**, identify the shader/pipeline that causes NVIDIA 580's compiler to fault, and determine whether the bug-fix mod can disable or alter that path before world rendering initializes.
