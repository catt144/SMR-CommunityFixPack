# FR-1 round 3 — turn the Q2 overlay into a TEMPORARY standalone workaround mod (one-shot, model-agnostic)

⏸ **HELD 2026-09-11. Do not run this unless the owner re-fires it.** The owner then asked the orchestrator to build the mod
directly ("build it in a directory and I pak it in the mod editor"). The build is `C:\Dev\SMR-FR1-TempMod-2026-09-11\SMR_FR1TempWorkaround`
(checklist 145 P1; desk harness 21/21). If re-fired, treat this brief as an **audit of that build**, not a rebuild.

⛔ ONE-SHOT: consume this file (`git rm`) in your delivery commit. Written 2026-09-11 by `smr-bugfixpack-5d` (the orchestrator)
for **Astra** (the builder), after the owner's v2 bench and scope ruling. The records win if they disagree with this brief.
Verify every specific against `git log` and the tree; Codex sessions are invisible to `ListAgents`.

## 0 · Orient

`git pull` · `git log --oneline -10` · `git status --short` · `AGENTS.md` · `docs/agent/STATE.md` · `prompts/DISPATCH.md` §0–§3.
Open a **live todo list**, one item per task in §3, and update it immediately. Then read `reports/FR1_LINUX_FINDINGS_2026-09-10.md`
**§11** (the v2 bench, recorded by the orchestrator), checklist **145** (the result block and the "Can it be released? Not yet" risk
list), and your own `reports/FR1_CACHE_ROUTE_2026-09-11.md` §5–§8.

## 1 · What v2 showed (MEASURED; evidence `C:\Dev\Success\fr1-cache-v2\fr1-cache-v2\`, outside git)

- **Q2 `noop-noreload` loads worlds on 580.** No forced reload. At New Game's first `before-LoadBinAssets`, loading thread 013c dumped
  your no-op **18×** (one per RAYS record) in 17 ms, then all **36 REFLECT_FULL**. There were 0 faults in a 1.88 GB log, and New Game
  plus two saves loaded in one process. No original RAYS digest was dumped.
- **R2 (no marker) reverses it:** `38121decbc3eee12` rebuilt from the original bytes, fault 2 ms later at `glvkspirv +0x157c88`.
  **C2** reproduced the boot crash (271ec). F2 was not needed.
- **The first world load builds all 54 Reflections records; later loads in the same process build none.** Both saves therefore ran on
  pipelines already built. **A cold launch straight into a save is NOT SAMPLED.**
- **Q2-only log shapes vs C2/R2:** (a) `d3d12_resource_QueryInterface: {6b3b2502-…} not implemented, returning E_NOINTERFACE` ×4
  (UNATTRIBUTED: no vanilla 580 world load exists to compare); (b) the clean-exit `AppPolicyGetProcessTerminationMethod` fixme.
  No `err:vulkan`/`err:vkd3d`/device-lost; no Lua errors.

## 2 · The owner's ruling (2026-09-11, checklist 145), verbatim

> "We wouldn't launch it on the main pak, we would launch it as a one off clearly tempory pak that tells people this a work around
> and to uninstall it as soon as paradox fixes the real issue. I wouldn't even want to do a full git hub repo for it. Just stand it
> up on a temp basis since this will eventually be hotfixed"

So: a **separate mod** with its own id (never `SMR_CommunityFixPack`, never inside `Code/`); **temporary by name and text**; **no
GitHub repo**. The build lives outside git like the probes (e.g. `C:\Dev\SMR-FR1-TempMod-2026-09-11\`), with a receipt JSON in
`docs/archive/` and your report here. The owner uploads; no agent touches a portal.

## 2b · Owner directive, same day (verbatim): THIS IS THE LAST ROUND

> "tell astra that I want this to be the last round, we are doing an emergency workaround until its hot fixed. not a long term mod.
> If the answer is reflections off thats fine to. It lets them play where otherwise they wouldn't be able to"

What that changes (**it wins over §3–§4 wherever they conflict**):
- **Ship-ready in one pass.** Deliver a build the owner can pack and upload after ONE bench sitting. There is no round 4, so fold every
  fallback into this delivery. If the packed mount might fail, ship plan B in the same package (e.g., player steps to drop the unpacked
  folder into `Mods/`, the route the benches proved), and state in advance which leg decides between the plans.
- **The smallest safe thing wins.** Anything that is polish gets cut: the description carries the "temporary, uninstall when Paradox
  fixes it" message, and the in-game notice happens only if it is nearly free. Open questions that don't block an emergency release go
  in "not opened", not into new work.
- **Reflections Off is an accepted answer.** The mod may work only with Reflections Off. Either instruct players to keep it Off, or set
  it Off if that is simpler and safer; say which you chose and why. Keeping reflections looking right with Reflections On is not a goal.
- **The owner may run P1 first** (checklist 145: the unchanged v2 probe, packed through the Mod Editor, launched straight into a save
  with `-fr1-cache=noop-noreload`). If its result is in, build on it: the release mod should be the v2 probe with the bench parts
  stripped, not a rebuild. If P1 is not in yet, keep §3 task 5 answerable by the owner's first leg.
- **Portals:** Steam for certain, Paradox possibly. Draft the Steam text first; the Paradox text is optional.
- **Owner legs: only the minimum that makes it safe to hand out.** On Linux 580: the packed mount, a cold launch into a save, and the
  disable reversal. Plus one look on the Windows rig. Order them so the first failure tells the owner which plan to ship.

## 3 · Tasks — leads, not a plan

1. **The mod: Q2's shape only.** Mount the 18 RAYS no-op records at mod load with no forced reload, and no launch marker (players won't
   type one; enabling the mod IS the opt-in). Drop `Control/` and the bench diagnostics, but keep one log line per launch that says
   whether it mounted or declined, and why. Propose the id and display name: temporary must be obvious in the Mod Manager list.
2. **Self-retire when the game changes.** The payload is byte-tied to this cache (1.1.0.403908 / assets 33006). A Paradox patch should
   leave the mod **inert and saying so** ("the game has been updated; this workaround no longer applies — please uninstall"). That is
   the owner's "uninstall when Paradox fixes it" made mechanical. A revision pin is acceptable here: it is not a fix-pack module, so
   `FIX_POLICY` §2a does not bind it. If you can reach something closer to the cache's identity than the revision numbers, prefer it,
   and name the trade-off. A Lua-only hotfix that bumps the revision but leaves the shaders alone would retire a still-needed mod.
3. **Who it touches.** Keep the d3d12 + NVIDIA-vendor gate. There is no Proton detector (EF-089; the `wine_get_version` banner is native,
   FR1_OPTIONS §2.3). Re-check that once, cheaply, then design for the fallback: a Windows NVIDIA player who enables it anyway. Predict
   what they see with Reflections Off and On, and make that an owner leg (§4).
4. **Reflections On.** The probe refused unless SSR = 0. For a player mod, on 580, the choices include: mount anyway and tell them to
   keep Off; force the setting Off (this changes a player setting, so it is the owner's call; propose, don't decide); or decline (then
   they crash as before). Say what the no-op does to the picture when SSR is On, if you can predict it.
5. **Packed delivery, the #1 risk.** Portals ship `ModContent.fpk`; the benches ran unpacked. Establish whether `DlcMountFolder` works
   on a folder inside a packed mod, and if not, the alternative. Pack route per STATE: main menu → MOD EDITOR → File → Pack Mod (the
   owner's sitting). Mind H-02 (the Mod Editor save bumps `version`), H-03 (first portal call creates the listing), H-09 (never stage
   a packed copy beside an unpacked one with the same id), and the H-10 analogue (the mod's `code` list is rebuilt from `items.lua`).
6. **A player-visible notice.** The owner wants it to tell people it is a temporary workaround. At minimum that goes in the
   description. Consider a one-time in-game message, weighing it against how much code it adds. Uninstall behaviour: a save made
   with it, loaded without it, should only show the "missing mod" warning (Q2 showed that shape for TestKit). Also note that
   disabling it needs a restart, because the mount lives for the process.
7. **Store text drafts** (Steam, and Paradox if the owner wants both): who needs it (Linux/Proton + NVIDIA 580, world-load crash),
   keep Reflections Off, temporary, uninstall when Paradox fixes it, how to tell it's working, and no claim beyond what was measured.
   Never name another author's mod (FIX_POLICY §8).
8. Anything we're missing. Take a better route if you find one, and say why.

## 4 · Owner legs to write (checklist 145, copy-paste steps, expected result stated in advance)

Linux 580, **packed** build: cold launch → load a save directly; New Game plus ~15 min of play; Reflections On briefly (record what
happens); disable → restart → New Game crashes again (the reversal). Windows rig, mod enabled: Reflections Off → normal play;
Reflections On → look at reflective surfaces. Save with the mod, then load without it. Keep each leg's first-screen witness and the
log line from task 1. Tell the owner which files to bring back.

## 5 · Deliverables and bindings

- A round-3 section in your cache-route report: verdict first, numbered claims graded MEASURED/SOURCE/INFERRED/NEVER RUN, and a
  "not opened" list. The mod build (unpacked, plus a packing note) goes outside git; the receipt JSON goes in `docs/archive/`.
- Owner steps plus the store-text drafts in **checklist 145**, replacing the v2 steps (keep the v2 result block).
- Same bindings as rounds 1–2: no game-dir, pack or archive writes; no game launch; no Mod Editor or portal; nothing into `Code/` or
  the fix pack's `metadata.lua`/`items.lua`. Commit by explicit pathspec with doccheck GREEN; push. The owner's standing rule:
  **the orchestrator reads and briefs, Astra builds.**
