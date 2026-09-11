# FR-1 options hunt — every way around the Linux/NVIDIA 580 crash (model-agnostic) — written 2026-09-10

⛔ ONE-SHOT: `git rm` this file when §5's deliverables are committed. Staleness anchor
2026-09-10: `git log --oneline -10` + `git pull` first — the records win over this file.
Tool-neutral: any Claude or Codex session can run it. Open a **live todo list**, one item
per numbered task in §3, updated the moment each changes — the owner reads it to decide
when to step in.

## 0 · Read first (in order)

1. `agent/STATE.md`; `prompts/DISPATCH.md` §0–§3 (bindings: never modify the game dir or
   `C:\Dev\SMR-SrcArchive\`; commits by explicit pathspec; doccheck GREEN).
2. **`agent/reports/FR1_LINUX_FINDINGS_2026-09-10.md`** — everything established, with citations,
   and the evidence index. Then `FR1_LINUX_BENCH_REPORT_2026-09-10.md` (owner's report, verbatim).
3. Evidence: **`C:\Dev\SMR-FR1-Evidence\`** (outside git, read-only for you — copy, never edit).
4. Background: `prompts/vanillahunt/README.md` §2b FR-1; checklist 136; `agent/FIX_POLICY.md` §1, §2, §4a.

## 1 · The problem in five lines

Every world load (New Game or Load) crashes to desktop on Linux + NVIDIA **580** under Proton;
Intel and NVIDIA 595 work. The fault is inside NVIDIA's shader compiler (`_nv014nvvm`) during
`vkCreateComputePipelines`, ~12–17 ms after the engine reloads `BinAssets/`. The prime suspect is
shader `38121decbc3eee12` = **`Reflections.fx` `REFLECT_RAYS`** (screen-space reflections), which
1.1.0 builds at world load **even with Reflections Off** — a structural match, NOT byte-proven.
Most affected players say they **cannot move to driver 595**, and Paradox gives no timetable.

## 2 · What the owner wants

**Explore creatively — every option, including ones nobody has raised.** Prefer what **a mod** can
do, but report **every** available option, whoever would carry it out: our mod, a separate mod,
the player, the owner, Paradox/Haemimont, vkd3d-proton/pyroveil, NVIDIA. Desk work plus bench
RECIPES — the bench is the owner's (Linux laptop; driver 580 restorable by Timeshift). ⛔ You cannot
run the Linux game; write each test as a short recipe with its expected result and its falsifier.

## 3 · Tasks

1. **Re-check the shader identification before building on it** (`WORKFLOW` / memory "probe verdicts
   are claims too"). Try to FALSIFY `38121decbc3eee12` = `Reflections.fx REFLECT_RAYS`: trace CBVs b1/b2;
   look for any other source that could produce t0–t7 + typed u0 + structured u1 + s2/s4 at 8×8×1
   (the NRD `*.cs.hlsl` family uses its own macros — check it independently of the `Define*` grep);
   if feasible, compile `Reflections.fx` with `-D REFLECT_RAYS` using the game's own `dxcompiler.dll`
   (or any dxc) and compare structure/size/bindings with the dumped DXIL. State the verdict
   PROVEN / STRONG / WEAK with what was checked. Also say whether the ~15 s dump gap is explained.
2. **Mod-side options (preferred) — explore each; add your own.** For each: mechanism, the
   Lua/engine lines that make it possible or impossible, what it changes for Windows/console players,
   and a bench recipe. Seeds, not a limit:
   a. **Keep the pipeline from being built:** which native path builds SSR compute pipelines at
      `BinAssets` load? Is there an `hr.*` variable, option, lightmodel or render-feature switch that
      selects `REFLECT_FULL` (simpler) instead of `REFLECT_RAYS`, or skips SSR pipeline creation?
      Enumerate the engine's `hr` names (`CommonLua/LuaExportedDocs/`, `uiRenderDebugForceMode.lua`,
      `RenderFeaturesParams.lua`, `Lightmodel.lua`; a runtime `hr` dump on the owner's Windows rig via
      the Test Kit console is one cheap owner ask). A mod can act before the map (`Msg("ChangingMap")`,
      `map.lua:482`; mod-load time).
   b. **Ship a modified shader source from a mod:** shaders mount "seethrough" (`mount.lua:47-51`) and
      compile at runtime from source; `ReloadShaders()` / `DlcReloadShaders` (`Dlc.lua:406`) exist. Can
      mod Lua mount a folder over `Shaders/` (sandbox permitting) with a `Reflections.fx` whose
      REFLECT_RAYS body compiles to SPIR-V that NVVM 580 survives — semantics-preserving, or gated?
      What would it cost Windows players, and does a shader cache defeat it?
   c. **Gate any workaround to Proton only:** Lua does not see `Platform.linux` under Proton (vanillahunt
      README §2b) — is there ANY Lua-readable signal of Wine/Proton (adapter/driver strings, OS version,
      the engine's `Proton/Wine:` detection, env, registry, file paths)? A workaround that cannot be gated
      changes every player's rendering — say so.
   d. Anything else a mod can reach: delaying SSR setup until after a first frame, forcing a different
      reflections quality path, swapping the pass list, etc.
3. **Player / owner options — every one, route-checked.** Seeds: `VKD3D_SHADER_OVERRIDE` with a
   GLSL-round-tripped `38121decbc3eee12.spv` (spirv-cross → glslang; the trick pyroveil used; could a mod
   ship the file? the env var must still be a launch option); a pyroveil config with the new hash; vkd3d-proton
   config flags that change its SPIR-V codegen (`VKD3D_CONFIG`, dxil-spirv options) — test whether a
   different Proton/vkd3d version emits different SPIR-V; driver branches between 580 and 595 (which NVIDIA
   release fixed NVVM — read NVIDIA changelogs; and WHY players "cannot go to 595": distro packaging, Mint
   Driver Manager, GPU support, kernel — route-check the real steps on Mint/Ubuntu/Fedora/Arch); the Steam
   `1.0.7 / Rollback` branch with Reflections Low; forcing the iGPU on hybrid laptops. ⛔ Memory rule
   "claims about what a player can do need a route check": every player-facing step must be one a real
   user can walk.
4. **Upstream options.** Draft (do NOT post): a vkd3d-proton / pyroveil report that 1.1.0's hash moved
   (`b73d41d886185985` → `38121decbc3eee12`), and a Paradox/Haemimont report that 1.1.0 builds the SSR
   compute pipeline at world load even with Reflections Off (they can fix it at the source — lazy creation).
   Read trackers via `api.github.com`, never rendered pages. Posting is the OWNER's (outward-facing).
5. **Scope ruling for the owner.** A workaround for a driver bug is not "a defect in the game's shipped
   Lua" (`FIX_POLICY` §1); whether it belongs in the fix pack, a separate mod, or only in player advice is
   a DESIGN call → a checklist "Decisions waiting on you" item with a recommendation, never decided here.

## 4 · Rules that bind

- Cite every claim with file:line in a NAMED tree version; label inference as inference.
- "Refuted" needs the condition SAMPLED (the film-grain test is the model: the mod's line was seen).
- Never modify the game dir, the archive, or `C:\Dev\SMR-FR1-Evidence\`. No portal or tracker writes.
- Do not build a shipping module. A throwaway bench mod (template: `C:\Dev\SMR-FR1-Evidence\fr1test-mod\`)
  lives OUTSIDE the repos and is the owner's to install.
- Several sessions edit this tree: re-check `git status` / `git log` before every shared-doc write.

## 5 · Deliverables

- **`agent/reports/FR1_OPTIONS_2026-09-XX.md`**: (1) the shader verdict; (2) an options table — option ·
  who acts · mechanism · evidence level · what it changes for non-Linux players · cost · bench recipe
  (numbered steps, expected result, falsifier) — ranked, mod-side first, but EVERY option listed, including
  ones ruled out (with the line that rules them out); (3) the two upstream drafts; (4) a NOT-explored list.
- **Checklist**: one "Decisions waiting on you" item — plain words, the ranked short list, the scope question
  (task 5), and the next bench test with a recommendation. Owner-facing prose only there.
- `agent/reports/FR1_LINUX_FINDINGS_2026-09-10.md`: append a dated line if the verdict changed. Any new engine
  behaviour learned → `agent/facts/EF-###.md`. SESSION_LOG entry; STATE only if the kernel changed.
- doccheck GREEN; `git commit -F <msg> -- <paths>`; push; `git rm` this file in the same commit.
