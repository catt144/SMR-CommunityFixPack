# FR-1 Linux sitting — the owner's RTX 3070 laptop (model-agnostic) — written 2026-09-10

Paste into a session when the owner says **the laptop boots Mint**. This is an
attended sitting on a SECOND machine: the owner types on the laptop, the agent
runs on the Windows rig and cannot see the laptop's files. Every reading comes
back as text that the owner pastes, or as a file they copy over. ⛔ Never ask for a
wide screenshot (one image over 2000 px breaks every later image read in the
conversation); ask for a pasted terminal line instead.

Staleness anchor 2026-09-10: `git log --oneline -10` + `git pull` first. Then read
`agent/STATE.md`, `prompts/vanillahunt/README.md` §2b **FR-1** (what is established
and refuted), checklist **136** (asks to players, rig plan), and 04's `TRIAGE.md`
FR-1 section if link 04 has landed. The records win over this file.

## What this sitting is for

FR-1: every NEW game crashes to desktop under Proton since 1.1.0, NVIDIA on every
GPU named, clean installs, DLC-off still crashes, AA/upscaler off still crashes
(the temporal-upscaler lead is REFUTED, `7987b28`). A Windows + NVIDIA new game
works. Nothing Lua-side has been pinned yet. The game log loses its tail in a
crash (`EF-047`), so **`PROTON_LOG=1` is the instrument**. This sitting turns
"players say" into a witnessed crash with its Wine-side log, then splits it with
three same-machine controls.

## Before the first launch (owner, once)

1. Rig as mirrored (memory note): Mint 22.2 Cinnamon X11, NVIDIA **580** branch.
   Paste: `inxi -Gxx` (or `lspci -k | grep -A3 -E 'VGA|3D'`), `nvidia-smi
   --query-gpu=name,driver_version --format=csv`, `uname -r`, and
   **`prime-select query`**. ⚠️ On a hybrid laptop the PRIME profile decides which
   GPU a Steam game gets. `on-demand` runs games on the Intel iGPU unless offloaded,
   and that would make a "works" reading VACUOUS for FR-1. Record the profile;
   for the main runs we need the game on the NVIDIA dGPU (profile `nvidia`, or
   `on-demand` + launch option `__NV_PRIME_RENDER_OFFLOAD=1
   __GLX_VENDOR_LIBRARY_NAME=nvidia %command%`). The game log's adapter line
   (step 3) is the control for which GPU actually ran.
2. Steam: **Steam Cloud OFF for the game** before its first launch (`EF-051`).
   Mods stay disabled. Compatibility: force the Proton version the OP used if
   known, otherwise current stable; record the exact version string.
3. **Timeshift snapshot** once Steam + the game are installed and launch to the
   main menu (owner's standing-rig practice). Pause driver/Proton auto-updates.

## Run 1 — witness the crash (the main reading)

1. Launch option: `PROTON_LOG=1 %command%` (keep the PRIME variables from above in
   front of it if used). ⚠️ Valve's documented behaviour writes
   `~/steam-3215050.log` (app id 3215050, confirmed by `appmanifest_3215050.acf`
   on the Windows rig). **UNVERIFIED on this rig until seen**: the owner runs
   `ls -la ~/steam-3215050.log` after the run and pastes the line.
2. Main menu → **New Game**, default settings, any sponsor. The owner notes the
   EXACT moment: clicking New Game / the mission setup screen / pressing Launch /
   the loading screen / the first frame of the map / later. One line.
3. Collect and copy over (USB, cloud drive, or `scp`):
   - `~/steam-3215050.log`. The useful part is the LAST ~300 lines. If the file is
     large, paste `tail -n 300 ~/steam-3215050.log` instead.
   - the game log, newest `Mars.exe-*.log`. Expected at
     `~/.steam/steam/steamapps/compatdata/3215050/pfx/drive_c/users/steamuser/AppData/Roaming/Surviving Mars Relaunched/logs/`
     (translated from the Windows `%APPDATA%` path; the library path differs if
     the game is on another drive). ⚠️ **UNVERIFIED**: the owner runs
     `ls -la` on it and pastes the listing. If it is absent, `find ~ -name
     'Mars.exe-*.log' 2>/dev/null` finds it. That found path is what may later
     be told to players, and nothing before that (checklist 136 ⛔).
   - `…/Surviving Mars Relaunched/LatestCrash/` in the same folder: list it.
     (Empty on the Windows rig on 2026-09-10; a crash dump there would be the
     first native artefact anyone has.)
4. Agent reads: in the game log, what is PRESENT (adapter name/vendor, driver,
   `Proton/Wine:` line, DLC load, the last startup stage), never where it stopped
   (`EF-047`). In the Proton log: the last exception / `err:` / `vkd3d` /
   `nvapi` / `dxgi` lines before exit, the faulting module and address, and the
   thread. Report unexplained lines VERBATIM. Compare with the player's truncated
   log (checklist 136 item 4: ~20 lines, banner only).

⛔ If Run 1 does NOT crash, stop and reconcile before any control. Check the PRIME
profile and the adapter line (the game may have run on the iGPU), the Proton
version, and the driver branch against the OP's (580.173.02, kernel 7.0, MSI
Katana RTX 3060 Mobile). A no-crash on the dGPU with matched versions is itself a
finding for checklist 136. Do not call FR-1 hardware-specific from one machine.

## Controls (only after Run 1 crashes; one variable each)

- **C-a · non-NVIDIA, same machine.** Options → Video → **Graphics Adapter** →
  the Intel iGPU (the combo lists every D3D12 adapter the device exposes,
  `CommonLua/Core/options.lua:456-463`, 1.1.0), OR the PRIME `on-demand` profile
  with no offload variables. Restart, New Game. Confirm from the game log's
  adapter line which GPU ran. Crash ⇒ not NVIDIA-specific. Works ⇒ NVIDIA ×
  Proton, as the reports suggest. ⛔ `PROTON_USE_WINED3D` is NOT a control: the
  game is D3D12-only on PC (`options.lua:443-447`), so it changes nothing.
- **C-b · regression.** Steam → Properties → Betas → **`1.0.7 / Rollback
  version`** (the branch name as seen in the owner's screenshot, checklist 118).
  New Game. Works ⇒ 1.1.0 regression on this machine, as the OP reports.
  ⚠️ Switching branches re-downloads the game. Switch back to `Default Public
  Version` afterwards and confirm the version in the main menu.
- **C-c · new game vs load.** The owner copies a **no-mod 1.1.0 Sol-1 save** from
  the Windows rig (`%USERPROFILE%\Saved Games\Surviving Mars Relaunched\<steam-id>\`,
  `EF-050`) into the prefix. Expected path, **UNVERIFIED**:
  `…/pfx/drive_c/users/steamuser/Saved Games/Surviving Mars Relaunched/<id>/`.
  Launch once first so the folder exists, and `ls` it. Load it. Load works +
  new game crashes ⇒ new-game / map-generation code (surface (a), 04's lead).
  Both crash ⇒ the shared map-entry/render path (surfaces (c)/(d)). Read the save
  header before handing it over (`orig_lua_revision=403908`, `active_mods` empty;
  memory note "savegame metadata is readable").
- Optional, only if cheap: a second Proton version (e.g. Experimental vs stable)
  to reconfirm "every Proton" on our own machine.

Record driver / kernel / Proton / PRIME profile at EVERY run.

## Where results go

- The witnessed crash, the Proton-log excerpt and the controls → a new
  `agent/reports/FR1_LINUX_SITTING_<date>.md` (verbatim lines, run table).
- A pinned cause → an `agent/bugs/` entry (vanilla, `C` series) per
  `DISPATCH.md` §3; an engine behaviour learned (log paths under Proton,
  LatestCrash contents, PRIME effect) → an `agent/facts/EF-###.md`.
- Route-checked player instructions (the real log paths, the `PROTON_LOG` step)
  → checklist **136**, for the owner to post. Never post them from an agent.
- Feed 04 / 99: a `vanillahunt` inbox line pointing at the report.
- `SESSION_LOG.md` leg; STATE only if the kernel changed. doccheck GREEN;
  `git commit -F <msg> -- <paths>`; push.
