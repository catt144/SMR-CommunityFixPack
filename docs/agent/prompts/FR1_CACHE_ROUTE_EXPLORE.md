# FR-1 — the shader-cache route: can a mod hand the game a safe reflections shader? (one-shot, model-agnostic)

⛔ ONE-SHOT: consume this file (`git rm`) in your delivery commit. Written 2026-09-10 late by `smr-bugfixpack-bd`
for the owner, who is routing it to **Astra**, the author of `reports/FR1_OPTIONS_2026-09-10.md` (the options report).
You are welcome back. The records win if they disagree with this brief. **Verify every specific against `git log`
and the tree:** Claude and Codex sessions both commit here, and Codex sessions are invisible to `ListAgents`.

## 0 · Orient first

`git pull` · `git log --oneline -15` · `git status --short` · read **`AGENTS.md` / `CLAUDE.md`**, **`docs/agent/STATE.md`**,
`docs/agent/prompts/DISPATCH.md` §0–§3 (bindings, judgment rules, filing). Open a **live todo list** with one item per
numbered task in §3, and update it the moment each item changes state; the owner reads that list to decide when to step in.
Then read, in this order:
1. **`docs/agent/reports/FR1_LINUX_FINDINGS_2026-09-10.md` §6–§9.** §8–§9 are new since your report.
2. **Checklist item 145** in `docs/PLAYTEST_CHECKLIST.md`: the owner-facing state, results, and "What's left".
3. Your own report, `reports/FR1_OPTIONS_2026-09-10.md`, now read against §8–§9.

## 1 · What happened to your report since you delivered it (all committed; verify)

Your work held up and moved the problem forward. Here is what the next four hours added (FINDINGS §8–§9, commits
`3a72792`..`1251c3d`):

- **Kept:** shader identity PROVEN (your byte-identical rebuild), and your cache correction (the crasher IS in
  `ShaderCached3d12.fpk`, record `14281071190732923386`). Both are the foundation for everything below.
- **Attribution upgraded:** the faulting thread dumps its shader **1 ms** before the NVVM fault in **all five crashing runs** (the
  original dump run plus the owner's legs A/B/D/E). That is direct log evidence; the exact-hash override is still the formal proof.
- **"Built while SSR is Off": MEASURED.** Leg A's probe read `hr.EnableScreenSpaceReflections = 0` just before LoadBinAssets,
  and the fault was on `38121decbc3eee12`.
- **M1 (clear `ForceShaderCacheReload`) is DEAD, for two independent reasons.** (a) `find()` (`Dlc.lua:262-274`) needs a DLC
  `assets_revision` STRICTLY greater than `AssetsRevision`. Both DLCs' own `revisions.lua` read `return 403908, 33006`, equal
  to the base game, because 1.1.0 rebuilt both packs on 2026-09-08 23:24. `norman` = Feeding the Future, `thomas` = Interplanetary
  Codex. (b) Neither DLC pack contains a shader cache at all (decoded with `tools/flpk_extract.py`: 0 shader-named files and
  0 nested packs; control: `revisions.lua` was found in each).
- **M2 (hidden `hr` selectors) is REFUTED on the bench, with the condition sampled.** The cache ships all **6** distinct REFLECT_RAYS
  programs and REFLECT_FULL at **tile 8 and tile 16**; the game forces `hr.SSRFullTile8x8 = 1` on AMD (`options.lua:81-85`).
  But leg B held `SSRFullTile8x8 = 1` from mod load through before-LoadBinAssets and still built `38121`, and leg D set it
  BEFORE a forced rebuild and the rebuild still chose a RAYS program. Leg A's baseline has `hr.SSRTraceHiZ = 1`, yet `38121` is the
  no-`TRACE_HIZ` build. ⇒ the live `hr` SSR values do not pick this pipeline's defines, at least not after renderer init.
- **The crash is the RAYS KERNEL FAMILY, not one hash.** A forced reload (legs D/E, the owner's "blank push") made the
  engine rebuild reflections pipelines **from the cache during boot**, consumed at once and not "on next map load" as the
  `Dlc.lua:412` comment says. The boot build picked `271ec9634b1ab87b` (RAYS + `USE_HYPERBOLIC_DEPTH` +
  `REFLECT_IMPORTANCE_SAMPLE`, cache record `12556516658419309610`), and 580 crashed on it the same way, before the main menu.
- **Your probe:** v1 had a latent defect. `ModLog(msg)` → `ModPrint` runs `string.format(msg)` with no args (`lib.lua:144,174`),
  so any `%` in a logged `hr` string threw before the hooks installed; your 7 mocks never logged a `%`. v2/v3
  (`C:\Dev\SMR-FR1-Options-2026-09-10\fr1-options-probe-v3\`) fix it, install hooks first, and v3 takes a comma list of treatments.
  It ran cleanly in the retail sandbox on Linux (`[FR1Options v3]` lines in every leg's Proton log).
- **Tooling left for you** (outside git): `C:\Dev\SMR-FR1-Options-2026-09-10\variant-map\` holds the compiled RAYS/FULL variants
  (`var_*.dxil`, your exact argv plus defines), the scan scripts with JSON receipts, `classify_dump.py <dump dir|zip>`, and the lupa
  probe harness. The bench legs are at `C:\Dev\fr1-mm-complete\fr1-mm\`.

## 2 · What we're thinking now — the owner's idea, and why it might work

The owner's instinct: *make the game think there's something new to load.* Pulled to its end, that becomes a **fake-DLC shader
cache**:

- **SOURCE:** `DlcReloadShaders(dlcs)` (`G/CommonLua/Dlc.lua:406-414`) is **not** in `ModEnvBlacklist`, while `MountPack` / `MountFolder`
  are (`G/CommonLua/Modding/Mod.lua:1366-1367`). It calls `find(dlcs, "/ShaderCache" .. config.GraphicsApi .. ".fpk", AssetsRevision,
  "assets_revision")`, then `MountPack("ShaderCache", path, "seethrough,in_mem,priority:high")` in the game's own environment, and sets
  `hr.ForceShaderCacheReload = true`. So a mod passing `{ {folder = <mod path>, assets_revision = <above 33006>} }` could, in
  principle, have the game mount a **mod-shipped** `ShaderCached3d12.fpk` over the real one.
- **MEASURED (legs D/E):** once that flag is set after mod load, the engine re-creates reflections pipelines **from the cache
  immediately, during boot**. So a swapped cache would take effect before the menu, which is exactly what's needed.
- **The payload idea:** replace the 6 RAYS records with something NVIDIA 580's NVVM accepts. The simplest candidate is a
  kernel with the same root signature and bindings that does nothing, for players who keep Reflections Off (it currently
  can't be played at all on 580).

**Peeked at the desk, not yet analysed (MEASURED, 09-10 late):**
- Cache record names are NOT vkd3d hashes (`0x38121decbc3eee12` = 4040324718312484370 ≠ 14281071190732923386).
- A record starts with the magic `rphs` plus typed fields (`invalid`, `bool`, …).
- The DXBC in record `14281071190732923386` sits at offset 8,549, preceded by the uint32 `0x000040c8` = 16,584 = the DXBC length.
- `shadercache-extracted\index.txt` is lines of `[b]<key>=<n>`; `index.bin` is 1,269,962 bytes.
- We have `tools/flpk_extract.py` (a reader) but **no FLPK writer**.

**The RAYS records** (the scan's variant → cache record): default `14281071190732923386` · imp `6121468085666728083` · hyp `3532759928818375094` ·
hyp+imp `12556516658419309610` · hiz `14433279818421691317` · hiz+imp `7464541473171016648` (hiz+hyp ≡ hyp). FULL tile 8 and tile 16:
`variant-map\full_variant_scan.json`.

## 3 · The task — a feasibility study, then (only if it holds) a disposable bench instrument

The questions below are the ones we can see. **They are leads, not a plan.** If you find a better route (to this
payload, around it, or a different mod-side lever altogether), take it and say why. You re-derived a recorded claim
last time and were right to; do it again anywhere this brief looks wrong.

1. **The record format.** What is an `rphs` record: header, typed-parameter table, root signature, blob(s), trailer, checksums?
   How are record names (keys) derived? How do `index.txt` / `index.bin` relate to the records, and does the engine need them to find
   a record? Use the 6,455 decoded records as a corpus: compare the 6 RAYS records with each other and with the FULL ones.
2. **The pack format, writing side.** Can we emit a valid FLPK (`.fpk`) containing only replacement records, and does a
   `seethrough, priority:high` mount of a PARTIAL cache overlay the base one per record? Is a partial pack enough, or does the engine
   read the pack's index as the whole truth?
3. **The mod-side mount route.** Walk `DlcReloadShaders` / `find` with a mod-supplied `dlc` table. Does `io.exists` / `MountPack` accept a
   mod content path (unpacked `AppData/Mods/<id>/`, and packed: `ModContent.fpk` mounted at `ModContentPath .. id`, which would be a pack inside a
   pack)? What does `config.GraphicsApi` read at that point (the probe logged `d3d12`)? When must the call happen relative to
   the boot-time rebuild that D/E measured?
4. **The payload.** What replaces RAYS: a no-op with the exact root signature; the FULL tile-8 DXIL placed under the RAYS keys (dispatch
   semantics differ — check what a mismatch does); or a semantics-preserving restructure of the ray-queue loop that NVVM accepts
   (pyroveil's old fix was a GLSL round-trip, so restructured control flow compiled fine). Do signed DXIL, the container `HASH` or the
   record checksum need regenerating, and does vkd3d or D3D12 validate them?
5. **Does the RAYS pass even dispatch when Reflections is Off?** If it doesn't, a no-op costs players nothing visible. If it does, what shows on screen?
6. **Blast radius.** The mod cannot tell Proton from Windows (§2.3 of your report). What would the replacement do on Windows NVIDIA, AMD
   (which forces `SSRFullTile8x8`) and Intel? Is there a behaviour gate a mod CAN see, or is "opt-in, Linux-580 players only, keep
   Reflections Off" the honest shape?
7. **Anything we're missing.** For example: can a missing or invalid record make the engine fall back to compiling HLSL (`EnableShaderCompilation
   = 1`), so that a mod-mounted `Shaders/Reflections.fx` through `DlcMountFolder` wins after all? Could a record for a different pass stand in?
   Is there a cleaner lever in the `rphs` parameter table than the `hr` values that failed?

## 4 · Deliverables

- **`docs/agent/reports/FR1_CACHE_ROUTE_<date>.md`**: a verdict first (feasible / blocked-at-X / better-route-found), then
  numbered falsifiable claims, each graded **MEASURED / SOURCE / INFERRED / NEVER RUN**, then a **"not opened"** list. Put all
  G-tree citations against `C:\Dev\SMR-SrcArchive\1.1.0.403908\Src\`, and keep your evidence-key convention (G/S/B/D).
- A desk receipt JSON in `docs/archive/` (as last time), plus any tools you write. Keep them outside git, or in `tools/` if they are
  reusable and doccheck-clean.
- **If and only if** the route survives the desk: a disposable bench mod outside git (in the probe's style: no persistent writes,
  explicit opt-in marker, fail closed, desk-harnessed with game-faithful `ModLog` mocks), plus plain-words owner steps added to
  **checklist 145**. The owner's laptop is on driver 580 with PRIME On-Demand; the Linux Mods folder, the Proton log and the dump
  recipe are in checklist 145's "M1 + M2 bench" block. Plan legs that tell you **which** program the crashing thread built
  (`classify_dump.py`), not just crash/no-crash.
- Route owner decisions to the checklist's "Decisions waiting on you", never only into agent docs. Add a one-line NEXT update to
  STATE only if it fits the byte cap (doccheck reports it; the owner rules evictions).

## 5 · Bindings (never bend)

- Never modify the game directory, `Packs/`, the source archives, or the evidence folders. Extract, compile and write only into
  scratch directories outside the game tree.
- Never launch the retail game yourself for a reading, never open the Mod Editor, never touch a portal API (STATE H-02/H-03).
- A driver/compiler workaround is **not** a shipped-Lua defect (`FIX_POLICY` §1). Whether any of this ships in the fix pack,
  in a separate opt-in mod, or as player instructions is the **owner's** decision (checklist 145). Build nothing into `Code/`.
- A negative search over packed or compressed bytes proves nothing; decode first (your own EF-088 correction). A probe's
  "CHANGED" line is not a treatment witness when the question is which program got built; the dump is.
- Commits: `git add <explicit paths>` then `git commit -F <msgfile> -- <same paths>`; `python tools/doccheck.py` GREEN first;
  push (standing-allowed). Commit your report verbatim, so a cross-vendor audit can read it.
