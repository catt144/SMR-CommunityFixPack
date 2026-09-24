# `tools/` — what is here and which one you want

**Reader: a worker seat with this repo open.** This is a routing table, not a
manual. Every row below points at the script's own header, which is the only
authoritative account of what it does, what its verdicts mean and which flags it
takes. **Open the header before you run it.**

Companion documents in this folder:
[`TESTKIT.md`](TESTKIT.md) — the probe harness and how to read a verdict ·
[`SMRTK.md`](SMRTK.md) — the in-game toolkit and preloading a sitting ·
[`arming/README.md`](arming/README.md) — the unattended-leg harness, its five
rules and the failure behind each one.

## Where to start

| you want to … | go to |
|---|---|
| commit, and something is RED | **Repo gates** — run `python tools/doccheck.py` and read the cure it prints |
| know what a game patch changed under us | **Source-diff instruments**, and `docs/agent/WORKFLOW.md` for what they license |
| settle a defect without provisioning a colony | **Desk bench** |
| know what the pack did in a real run | **Evidence from a run** |
| ship | **Release and upload**, and `docs/UPLOAD_WORKFLOW.md` |

## ⛔ Two things that hold across all of them

1. **A tool's output is a claim until the tool is falsified.** Three instrument
   defects turned up in a single session here — a pack parser, an extraction
   script and a grep dedupe — each producing confident, wrong numbers. That is
   why the gates carry `--selftest` and why `doccheck.py` runs several of them
   as gated checks: a falsifier that stops firing is itself the finding. Which
   ones are gated is what `doccheck.py` prints — read its `SELFTEST:` lines
   rather than a count written down here.
2. **Scope a command so that contrary evidence could make it fail.** An empty
   result proves nothing until the same question has a positive control, and a
   negative search over compressed input (an `.fpk`, a `.zip`) is not a sample
   at all until the bytes are decoded.

## ⛔ Hazards on this rig, every one of them silent

The shell here is not verbatim, and its failures do not announce themselves. Each was measured in
this repo. (Mixed line endings are the exception: doccheck's EOL gate catches those, RED, with a
`--fix-eol` cure.)

1. **Quoted heredocs strip one backslash level**, repeatedly, even while patching a correct script,
   and the botched edit reports success. A heredoc may carry prose, never code with a backslash:
   write scripts with an editor tool.
2. **`git commit -m` splits on embedded quotes under PowerShell 5.1** and git reads the fragments
   as pathspecs. Use `git commit -F <file>`.
3. **PowerShell 5.1 `Get-Content`/`Set-Content` corrupt no-BOM UTF-8**: reads decode as ANSI,
   writes add a BOM. Use an editor tool, or `[System.IO.File]` with `UTF8Encoding($false)`.
4. **`grep -c` exits 1 on zero matches and breaks an `&&` chain.** Read controls in their own call.
5. **`cd ""` returns 0**, so `cd "$TMPDIR"` is a silent no-op and the command runs in the repo. Use
   an absolute scratch path, and `pwd` before any `mkdir` or `git init`.
6. **`Compress-Archive` writes backslash entry names**, which Linux unzip turns into one file with
   backslashes in its name. Build zips with Python `zipfile`, then list `namelist()`.
7. **After rewriting line endings, `git status` lists files modified with an EMPTY diff** (stale
   index stat). `git add --renormalize` clears it, but only where `hash-object --no-filters` equals
   the index blob, or it stages a peer's pending edit. Python text mode writes CRLF here: pass
   `newline="\n"` or write bytes.
8. **`$'\r'` is not ANSI-C quoting in the Bash tool's sh**: `grep -c $'\r'` returns 0 on a 100%
   CRLF file. Count the bytes in Python.
9. **`rg` with explicit directory args returned nothing for a phrase `grep -r` found in 7 files.**
   Cause undiagnosed; confirm any absence with `grep -rn`.
10. **Git Bash `ls -l` shows an NTFS junction as a symlink.** Classify with PowerShell
   `(Get-Item x).LinkType`; enumerate with `cmd /c dir /A:L /S /B <tree>`, which does not follow
   them.
11. **`grep -r` and `robocopy` walk INTO junctions** — one junction to every Claude project turned
   2,649 real hits into 31,255. Use `--exclude-dir` per junction, and `/XJ` on any bulk copy.
12. ⛔ **`git checkout -- <path>` is not a restore.** It restores to HEAD, not to the state you
   started from, and it silently destroyed an uncommitted rewrite here. Copy the file aside before
   any temporary edit, restore from the copy, and `sha256sum` both to prove the restore landed; a
   harness that breaks a file to watch a gate fire does the same and prints the hash, as
   `ck170_selftest.py` does. On a path a peer is mid-write on, it discards their work too.

When a command's fidelity matters, use a tool that writes bytes, and verify afterwards.

## ⭐ The rows below are GENERATED

The prose in this file is hand-authored. Everything between the two marker
comments is written by `python tools/doccheck.py --regen` and checked by
`doccheck.py` on every commit, on the same contract as `docs/agent/bugs/INDEX.md`:
**RED only on drift, and cured by `--regen`, never by hand.**

- The row **set** is `glob(tools/*.py)`. There is no exempt class, because an
  exemption list is the same stale hand-kept list wearing a smaller hat. Add a
  script, run `--regen`, and it is listed.
- A row's **text** is copied from the script's own header. If a row reads badly,
  **fix the script's docstring** — this file cannot be a second, divergent
  account of what a tool does, and is built so that it cannot become one.
- The **grouping** is declared data (`TOOL_GROUPS` in `doccheck.py`), not a
  filename heuristic. A new script you have not grouped renders under
  *Ungrouped* with its row already correct; grouping it is tidying, not a fix,
  and **no peer is ever blocked by a RED that `--regen` cannot cure.**

<!-- GENERATED TOOL ROWS — never hand-edit; regenerate with: python tools/doccheck.py --regen -->

*79 scripts, every `tools/*.py` on disk. This block is GENERATED: a row's text is copied from the script's own header, so a wrong row is repaired in the script, never here.*

### Repo gates, and the falsifiers that keep them honest

The pre-commit hook runs `doccheck.py`; the four `*_selftest.py` are required BY it, so a gate whose falsifier stops firing is itself RED.

| script | what its own header says |
|---|---|
| [`doccheck.py`](doccheck.py) | doccheck.py — the structure checker (DOC_RESTRUCTURE_SPEC.md §5). |
| [`parsecheck.py`](parsecheck.py) | Does every Lua file in the pack actually parse? |
| [`ck170_selftest.py`](ck170_selftest.py) | Exercise ck170 gates on disk copies; never corrupt the shared checkout. |
| [`counts_selftest.py`](counts_selftest.py) | Check on-demand counts, RED withholding, and regeneration without STATE writes. |
| [`prompt_map_selftest.py`](prompt_map_selftest.py) | Falsify the PROMPT MAP gate in disposable directory fixtures. |
| [`repair_pass_selftest.py`](repair_pass_selftest.py) | Repair-pass falsifiers; mutants execute only in a temporary directory. |

### Source-diff instruments — after a game patch

Run order, trigger rule and — this is the part that matters — what their output does and does not license: `docs/agent/WORKFLOW.md`, "After a game patch". Read it before you quote a verdict from any of these.

| script | what its own header says |
|---|---|
| [`patchcheck.py`](patchcheck.py) | After a game patch: one desk command that says none / scoped / full, and why. |
| [`patchcheck_selftest.py`](patchcheck_selftest.py) | Regression test for patchcheck.py: it must reproduce the 1.0.7 -> 1.1.0 backtest. |
| [`flpk_extract.py`](flpk_extract.py) | FLPK (Surviving Mars: Relaunched .fpk) extractor, v2. |
| [`bodycheck.py`](bodycheck.py) | Is the shipped code each module patches still the code it was pinned to? |
| [`sigcheck.py`](sigcheck.py) | Compare every function this pack replaces against the SHIPPED signature. |
| [`treediff.py`](treediff.py) | What did the game change, function by function, between two ModTools/Src trees? |
| [`presetdiff.py`](presetdiff.py) | What did the game change inside its PRESET DATA between two ModTools/Src trees? |

### Reading the shipped game by hand

When a diff says something moved and you need the body itself.

| script | what its own header says |
|---|---|
| [`luafn.py`](luafn.py) | Print a top-level Lua function body from the shipped ModTools/Src tree (added 2026-09-08 for the 1.1.0 re-verification). |
| [`pack_list.py`](pack_list.py) | List a Surviving Mars .fpk WITHOUT extracting it, and reconcile it against the tree it was supposed to be built from. |

### Desk bench — shipped Lua under a real interpreter, no game

`deskbench.py` is the harness; every `desk_*.py` is one investigation's control, kept because a control is re-runnable evidence. A stub for a function that can REFUSE is a behaviour change, not a shim.

| script | what its own header says |
|---|---|
| [`deskbench.py`](deskbench.py) | Desk bench -- run shipped game Lua under a real interpreter, at the desk, without a game. |
| [`c90_scratch_verify.py`](c90_scratch_verify.py) | External scratch-source falsifiers for DESKBENCH_C90; never edits Code/. |
| [`desk_c104_political_animal.py`](desk_c104_political_animal.py) | C104 investigation: can Political Animal ("Enact all laws") be earned on 1.1.0? |
| [`desk_c105_water_reclamation.py`](desk_c105_water_reclamation.py) | C105 investigation: does the Water Reclamation automation upgrade remove the spire's water saving? |
| [`desk_c74_hit_moment_fx.py`](desk_c74_hit_moment_fx.py) | Desk falsifier for C74/C77's seven-unit animation-moment repair. |
| [`desk_c83_arrivals.py`](desk_c83_arrivals.py) | C83 arrival reroute control over shipped GetDomes/ChooseDome bodies. |
| [`desk_c85_clogged.py`](desk_c85_clogged.py) | C85 clogged-building release over the shipped Setexceptional_circumstances body. |
| [`desk_c86_scan_downgrade.py`](desk_c86_scan_downgrade.py) | C86 scan-downgrade control over the shipped MapSector:Scan body. |
| [`desk_c88_prefab.py`](desk_c88_prefab.py) | C88 Building Codes vs prefabs, over the shipped LawDef ConstructionComplete handlers. |
| [`desk_c89_faction_gate.py`](desk_c89_faction_gate.py) | C89 faction dome-size gate over the shipped FactionDef DomeFilter evals. |
| [`desk_c90_datapatch.py`](desk_c90_datapatch.py) | C90: missing Require targets through the REAL core and whole modules. |
| [`desk_c92_achievement.py`](desk_c92_achievement.py) | C92 investigation: execute shipped registry, state, and achievement bodies. |
| [`desk_c93_open_pasture.py`](desk_c93_open_pasture.py) | C93 desk controls for the production Outside Ranch module. |
| [`desk_c95_habitat_draft.py`](desk_c95_habitat_draft.py) | C95 desk falsifier. Extract current shipped bodies; never launch/provision a game. |
| [`desk_c95_return_home.py`](desk_c95_return_home.py) | Registered C95 return repair, extracted shipped selector/dispatcher controls. |
| [`desk_c96_rover_subclass.py`](desk_c96_rover_subclass.py) | C96 desk falsifier. Extract current shipped bodies; never launch/provision a game. |
| [`desk_caller_seam.py`](desk_caller_seam.py) | Vanillahunt 03d source control; no game, mod, or archive writes. |
| [`desk_ck53_hostile_globals.py`](desk_ck53_hostile_globals.py) | Desk control for checklist 53's hardening rows 1 + 2 (built 2026-09-16). |
| [`desk_f117_argshape.py`](desk_f117_argshape.py) | F117 desk falsifier -- does the module's argument-shape probe actually discriminate? |
| [`desk_f117_kitprobe.py`](desk_f117_kitprobe.py) | Does the KIT probe for F117 actually discriminate, on both branches? |
| [`desk_f117_recipe.py`](desk_f117_recipe.py) | Which landing layouts make Fix_ArrivalDeaths half (b) call Community:GetScoreFor at all? |
| [`desk_f119_trade_fuel.py`](desk_f119_trade_fuel.py) | F119 trade-rocket fuel-request control over shipped Lua bodies. |
| [`desk_f59_expedition.py`](desk_f59_expedition.py) | F59: immediate vacancy notification can steal an expedition home, and the repair (2026-09-11) defers the notification out of the caller's call stack. |
| [`desk_f59_interact.py`](desk_f59_interact.py) | F59 verification, 2026-09-11: the hook also fires inside the MANUAL-ASSIGN operation, and that one overfilled a residence -- plus the repair that stops it. |
| [`desk_migration_cluster.py`](desk_migration_cluster.py) | Migration audit controls, 2026-09-11. No engine or colony execution. |
| [`desk_migration_observations.py`](desk_migration_observations.py) | Extracted topology controls. Engine geometry/buildability is NOT exercised. |
| [`desk_mystery_tech_migration.py`](desk_mystery_tech_migration.py) | Mystery techs: exercise shipped reveal, lock, research and legacy migration bodies. |
| [`desk_probes_f67_f59.py`](desk_probes_f67_f59.py) | Do the kit probes for F67 (LanderEmptyLaunch) and F59 (FreedHousingNotice) discriminate on the 1.1.0 bodies? |
| [`desk_progress_seam.py`](desk_progress_seam.py) | Vanillahunt 03c source controls; no game, mod, or archive writes. |
| [`desk_seam_food.py`](desk_seam_food.py) | Vanillahunt 03 source controls; no game, mod, or archive writes. |
| [`desk_shelter_reflex.py`](desk_shelter_reflex.py) | F73 wrapper control only. No engine, no full Idle simulation, no colony reach claim. |

### Censuses over our own tree — the pre-launch sweep

The L-series, one census per question the launch sweep had to answer.

| script | what its own header says |
|---|---|
| [`l2_reload_sim.py`](l2_reload_sim.py) | L2 (lifecycle & idempotency) — two-Lua-load simulator for the DataPatch scaffold. |
| [`l3_save_footprint.py`](l3_save_footprint.py) | L3 — aggregate save-footprint census over the shipped Code/ tree. |
| [`l4_player_surfaces.py`](l4_player_surfaces.py) | L4 — census of every surface a PLAYER can see or read, over the shipped tree. |
| [`l5_containment.py`](l5_containment.py) | L5 — census of every route by which pack code can THROW, and what catches it. |
| [`l6_promise_map.py`](l6_promise_map.py) | L6 — promise vs behaviour. Mechanical censuses for the pre-launch sweep chain. |
| [`l6_reachability.py`](l6_reachability.py) | L6 — dead-coded targets. Does the shipped game still CALL what we patch? |
| [`l7_env_map.py`](l7_env_map.py) | L7 (environment & namespace) — the global map, taken from the COMPILER. |
| [`l8_deference_map.py`](l8_deference_map.py) | L8 (adversarial / hostile modder) — the DEFERENCE census. |
| [`l8_hostile_input.py`](l8_hostile_input.py) | L8 (adversarial / hostile modder) — hostile-input harness for the pack's PUBLIC globals. |

### Pack-shape audits and chain bookkeeping

What the pack declares, writes and blocks, and what prior work left open.

| script | what its own header says |
|---|---|
| [`aliascheck.py`](aliascheck.py) | A Test Kit probe that calls a bare helper its file never bound ERRORs at run time while parsing perfectly. |
| [`audit_preset_fields.py`](audit_preset_fields.py) | Terminal-audit instrument (2026-08-19): preset-FIELD write census over Code/. |
| [`blocking_analysis.py`](blocking_analysis.py) | Blocking analysis, v2 -- v1 was useless: bare-name resolution marked half the codebase blocking (IsValid, SetText, Random all collided with some unrelated blocking method). |
| [`harvest_wrap_targets.py`](harvest_wrap_targets.py) | Harvest every `{ class = C, method = M }` target the pack declares. |
| [`fact_provenance.py`](fact_provenance.py) | Read-only provenance leads, not automatic build classification. |
| [`seam_coverage.py`](seam_coverage.py) | Reproduce/check link 03's close-out receipt and disjoint continuation queues. |

### Evidence from a run

⛔ Module counts come from `logscan.py`, never a hand-grep, and a log copied while the game is RUNNING is a partial log.

| script | what its own header says |
|---|---|
| [`logscan.py`](logscan.py) | Scan Surviving Mars logs for what the fix pack did, and for anything that threw. |

### Release and upload

`docs/UPLOAD_WORKFLOW.md` owns the procedure; these are its local gates.

| script | what its own header says |
|---|---|
| [`upload_preflight.py`](upload_preflight.py) | Upload preflight — run every portal guard clause locally, before the sitting. |
| [`pack_predict.py`](pack_predict.py) | Predict the file list DbgPackMod will put into ModContent.fpk. |
| [`store_screenshots.py`](store_screenshots.py) | Build the store-gallery screenshots from the owner's marked-up originals. |

### One-shot document migrations — already fired

⛔ Never re-run these. They re-execute a migration from a pre-split document that is now a stub; `--regen` is what rebuilds an index.

| script | what its own header says |
|---|---|
| [`split_bugs.py`](split_bugs.py) | split_bugs.py — docs/BUGS.md -> docs/agent/bugs/ (DOC_RESTRUCTURE_SPEC §3a, as amended by the ROUTE (a) decision in the docs-restructure chain's prompt 2). |
| [`split_facts.py`](split_facts.py) | split_facts.py — docs/agent/ENGINE_FACTS.md -> docs/agent/facts/ (DOC_RESTRUCTURE_SPEC §3b, executed by the docs-restructure chain's prompt 3). |

### Ungrouped

New since the last grouping pass. Give each a home in `TOOL_GROUPS` in `tools/doccheck.py` — but the row is already correct, so this is tidying, not a defect.

| script | what its own header says |
|---|---|
| [`desk_c107_dry_farming.py`](desk_c107_dry_farming.py) | C107 Dry Farming reaches the four Feeding the Future plant farms: the module through the REAL core, over the shipped DryFarming preset, the shipped farm templates and the shipped BuildingTemplates builder, in the engine's load order. |
| [`desk_c108_wildfire_cure.py`](desk_c108_wildfire_cure.py) | C108 Wildfire cure: the shipped 1.1.0 at-home service payment keeps an infected colonist above the medical-visit threshold, and the module sends them anyway. |
| [`desk_c111_rescue_text.py`](desk_c111_rescue_text.py) | C111 command-text control on shipped 1.1.1.405907 Colonist UI Lua. |
| [`desk_c115_home_rescue.py`](desk_c115_home_rescue.py) | C115: archived Transport, task cleanup and dome position check on a desk fixture. |
| [`desk_c42_passage_stale.py`](desk_c42_passage_stale.py) | C42 passage-element stale-holder teardown over archived 1.1.1.405907 Lua. |
| [`desk_f124_track.py`](desk_f124_track.py) | F124 track rebase: archived split/repair bodies, refunds, shells and branch decline. |
| [`desk_f125_vacuum.py`](desk_f125_vacuum.py) | F125/F52 composable migration controls on archived 1.1.1.405907 Lua. |
| [`desk_f127_arrival_booking.py`](desk_f127_arrival_booking.py) | F127: archived 1.1.1 arrival booking, full-dome Homeless label, and fix-removed control. |
| [`desk_gamepatch_retirements.py`](desk_gamepatch_retirements.py) | 1.1.1 retirement source controls and active pack-on/pack-off desk controls. |
| [`gamepatch_111_census.py`](gamepatch_111_census.py) | Reconcile the 1.1.1 build response by name, including companion probe removal. |
| [`paradox_card.py`](paradox_card.py) | Open the Paradox store description as a formatted page, ready to copy. |
| [`replacecheck.py`](replacecheck.py) | Which modules redefine a shipped declaration outright, and which delegate to a captured original they actually call? |

<!-- END GENERATED TOOL ROWS -->

## Also in this folder, and not a `*.py`

| path | what it is |
|---|---|
| `arm_leg.ps1` | the arming harness — [`arming/README.md`](arming/README.md) is its documentation and stands on its own |
| `arming/legs/`, `arming/payloads/` | one JSON manifest per leg, and the Lua each installs **into the kit, never into the pack** |
| `hooks/pre-commit` | the hook that runs `doccheck.py`. Install it once: `git config core.hooksPath tools/hooks`. ⛔ `--no-verify` is not an alternative to a RED |
| `held/` | code parked out of the load path on purpose; an unlisted file does not load, and parking is how a module waits without shipping |
| `c95_blocking_targets.json` | data for the C95 desk controls |
