# Launch rehearsal — the dry run, and the gate that actually decides

♻️ **SELF-CONSUMING.** Delete this file in your closing commit, naming its grave.

**Owner design, 2026-08-17:** *"once its done sweeping it does a 'dry run' on our
launch procedure. It cannot publish the mod, but it can do every step up to that
point"* — and, on the two configurations: *"[A] is for our testing to ensure
compatibility. This [B] is for safety to ensure a clean launch of the bug fix
mod."*

⛔⛔ **THE RELEASE CRITERION IS B, NOT THE SUITE.** A green suite in A does not
authorise an upload. A exists to diagnose B.

---

## 0 · ⛔ Where the safe line actually is — read before planning anything

**"Every step up to publish" is NOT the safe boundary.** The step before publish
is `prepare_fn`, and **the first API call is the one that creates the listing**:

* `Steam_PrepareForUpload` calls `AsyncSteamWorkshopCreateItem()` — creates a real
  Workshop item and sets `params.publish = true` (`SteamWorkshop.lua:17-22`).
* `PDX_Upload` returns a `pdx_mod_id` and writes `pdx_id` / `PdxMod` back into
  `metadata.lua`, then `SaveWholeMod()` (`ParadoxMods.lua:167-173`).

⇒ ⛔ **Nothing that touches a portal API may run.** The click is nested inside the
step before it.

✅ **What IS dry-runnable is the whole valuable half**, because the upload's
**validation** is separable from its **transmission**: every guard in
`PDX_PrepareForUpload` is pure Lua reading `mod.*` before any network call.

## 1 · Stage 1 — preflight (no game, seconds)

```
python tools/upload_preflight.py
```

Runs all six Paradox guards, Steam's image-size limits, the version/`lua_revision`
pins, the `ignore_files` patterns, and the `code` ↔ disk ↔ `items.lua`
reconciliation. **Exit 0 required.**

⚠️ The tool reports the Paradox **login** guard as UNCHECKABLE, never as passed,
and portal character limits remain **check-at-paste**. Do not upgrade either.

## 2 · Stage 2 — packaging (game open, no network)

In the Mod Editor, with the mod **clean** (`IsDirty()` false — check first, a
forced save bumps the version):

```lua
DbgPackMod(Mods.SMR_CommunityFixPack, false)
```

Then list the real archive and reconcile against the emitted counts:

```
python <scratch>/listpack.py "<TmpData>/ModUpload/Pack/ModContent.fpk"
```
*(the 2026-08-17 run measured **80 = 76 `Code/*.lua` + `items.lua` +
`metadata.lua` + `LICENSE` + `preview.png`**, with `docs/`, `tools/`,
`CLAUDE.md`, `README.md`, `.git`, `.claude` all **zero** — re-measure, do not
inherit)*

⭐ **Keep this `.fpk`. It is the artifact stage 4 installs.**

## 3 · Stage 3 — run A · instrumented (⚖️ information, NOT the gate)

**Config:** TestKit **on**, opt-in **off**, mod loaded from the junction as usual.
Full restart (D13).

- `SMRTest.RunAll()` — record **by name**, ⛔ never as a total.
- The two 08-17 core-fix falsifiers:
  ```lua
  print("suspects:", #SMRFixPack.UpdateSuspects(), table.concat(SMRFixPack.UpdateSuspects(), ", "))
  DbgPackMod(Mods.SMR_CommunityFixPack, false)
  local seen, dup = {}, {} for _, id in ipairs(SMRFixPack.order) do if seen[id] then dup[#dup+1] = id end seen[id] = true end print("order:", #SMRFixPack.order, "dupes:", #dup, table.concat(dup, ", "))
  print("suspects after reload:", #SMRFixPack.UpdateSuspects(), table.concat(SMRFixPack.UpdateSuspects(), ", "))
  ```
  Expected `0` · `75` / `0` · `0`.

⚠️⚠️ **A's scope must not be overstated.** It tests this pack against **exactly one
other mod — our own.** ⛔ It may never produce a sentence like *"compatible with
other mods."* Its honest scope is "our two mods together," which is information
for the opt-in's launch, not a compatibility claim.

## 4 · Stage 4 — run B · player configuration ⛔ **THE GATE**

⭐⭐ **This has never been run in the history of this project.** Every gate
reading — `80/0/16/0`, `75/75`, `8/8`, ~60 archived launches — was taken with the
mod **unpacked through a junction** and a **third mod loaded that mutates `_G`**
(`SMRTest.SetGlobal`, the loggers, an added UI action). Nobody has confirmed the
pack behaves identically without it.

**Build the player's configuration:**

1. ⛔ **Pull the fix-pack junction** (`EF-055` — agent-side, real uninstall, zero
   owner cost). Record what you pulled so you can restore it.
2. Create a mod folder under `AppData/Mods/` containing **only** the stage-2
   `ModContent.fpk`. The loader takes the packed branch on
   `io.exists(pack_path) and not CheckModPackSignature(pack_path)`
   (`Mod.lua:1724-1740`): `MountPack`, `def.packed = true`, and `metadata.lua`
   read **from inside the archive**.
   ⚠️ **Determine what `CheckModPackSignature` does first** — if it returns true
   the branch is not taken and your rehearsal is not the player's path.
3. ⭐ **Run it under TWO folder names, and this is a real test, not pedantry.**
   First load computes `hpk_mounted_path = ModContentPath .. (prev_id or
   folder_name) .. "/"` — **the FOLDER NAME, not the mod id** — then caches the id
   and **unmounts if they differ**. A player's folder name is chosen by the portal
   installer and is *not* the mod id (`pdx_<id>_<version>` shape).
   ⇒ Run once as `SMR_CommunityFixPack` (id-matching) and once as a
   portal-shaped name. **`'image', "Mod/SMR_CommunityFixPack/preview.png"` was
   written against the UNPACKED path and this is the first test of it.**
4. Disable **TestKit** and **opt-in** in the Mod Manager. Full restart (D13).

**⛔ B has no console and you may not add one** — dropping an instrument into
`Code/` contaminates the exact tree under test. **B looks; it does not poke.**
Everything below is readable from the log file and the screen.

### B's pass criteria — all of them, by name

| # | criterion | how it is read |
|---|---|---|
| 1 | the mod loads **packed** | `[CommunityFixPack]` lines exist at all |
| 2 | **every module** registers | install-witness lines **BY NAME**, ⛔ not a total; the name set must equal run A's |
| 3 | `0 [LUA ERROR]` | log |
| 4 | ⛔ **no `update report:` line** | `00_Core.lua:540` logs **before** it shows the dialog, so its ABSENCE is the falsifier for the 08-17 false-alarm defect — no console needed |
| 5 | ⛔ **nothing on screen** | no dialog, no notification, first launch through to a loaded save |
| 6 | version renders **1.0.0** | Mod Manager |
| 7 | ⭐ **the preview image renders** in the mod list | tests the `Mod/<id>/` path in the PACKED case — the assumption stage 4.3 exists to break |
| 8 | save round trip | load a save · play · save · reload — no corruption, no residue surprise |
| 9 | uninstall holds for all 75 at once | remove the packed mod · load the save · `RELEASE_UNINSTALL_ASSEMBLY.md` still true |
| 10 | save directory reconciles **by name** | `EF-056`, after **every** launch |

⛔ **Any of 1–7 failing blocks the upload.** 8–10 failing blocks it and is worse.

## 5 · Stage 5 — restore, and report

- **Restore the junction** and re-enable TestKit / opt-in to the rig's usual
  shape, or the next session inherits a configuration nobody documented.
- Delete the staged packed install.
- Reconcile the save directory **by name** one final time.

**Report, in this order:** does B pass · what A said and how it differed from B ·
⭐ **any behaviour that differs between packed and unpacked** (that difference is
the single most valuable thing this rehearsal can produce, and nothing else in
the project would have surfaced it) · what you could not run and why.

⚠️ ⛔ **"The rehearsal passed" is not "the upload will succeed."** You did not log
in, did not transmit, and did not create a listing. Say the narrower true thing.
