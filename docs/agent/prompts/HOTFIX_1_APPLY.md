# HOTFIX 1 — APPLY (link 1 of 2; the audit is `HOTFIX_1_AUDIT.md`)

Paste into a fresh Claude Code session. Written **2026-09-08**, the day game
**1.1.0 + the first DLC** shipped and the pack's first field breakages landed.
**Start with `git log --oneline -10` + `git pull`.** Read `docs/agent/STATE.md`
(mandatory) and `docs/agent/FIX_POLICY.md` §2.

> 🎯 **ONE JOB: make the pack safe on 1.1.0 and leave it ready for the owner to
> upload.** ⛔ **You do not upload. You do not open the Mod Editor. You do not
> touch `version`.** (`H-02`, `H-03`.)
>
> ⚖️ **THE RULE THAT CREATED THIS PATCH (owner, 2026-09-08):** a dev "Fixed" line
> is a CLAIM until we confirm it — and so is ours. ⭐ **This week the project was
> wrong in both directions**: a desk audit predicted 6 self-disabled modules and
> the game measured 13; a "clean" call-site sweep missed two live P1s because it
> compared NAMES. **Check the thing, not its label.**

## 0 · What is ALREADY DONE — do NOT redo, do NOT re-derive

The live published pack is **tree `version` 5** (`pdx_id` 156049, `steam_id`
3787202810). **Five code changes are already committed since it**, and they ARE
the patch. Read them, do not rebuild them:

| commit | file | what |
|---|---|---|
| `2efbcf6` | `Fix_LanderCargoRatchet.lua` | **F113** gate — `Require`s the deleted `UniversalRocketBase:GetEarthExportResPossibleReward` |
| `2efbcf6` | `Fix_ExtractorStaffedPerformance.lua` | **F111** guard — `type(self.overtime) == "table"` (1.1.0 collapses it to a boolean) |
| `2efbcf6` | `Fix_AutomationLawCompensation.lua` | **F112** gate — `test` content check; quiet where `Workplace.GetWorkersPerformance` exists |
| `8bc6821` | `Fix_TrainCargoDumping.lua` | **F114** gate — declines where `MultiResourceDepotBase` exists |
| `be4c99e` | `00_Core.lua` | the self-check **override surface** (`SMRFixPack_Force`, `SMRFixPack_NoUpdateDialog`, `SMRFixPack.ForceApply`) — **+151 lines, ships INERT** |

⛔ **`items.lua` needs NO change** — no module was added, renamed or dropped, so
`H-10` is already satisfied. Verify, do not assume.

**Measured state, do not re-measure from source:** the last unforced boot read
**15 inactive / 12 named** (`archive/logs/unforced110_*`). `EF-078`'s 13/11 is
the PRE-gate baseline and is superseded. Facts: `EF-078`–`EF-081`. Entries:
`F111`–`F116`.

## 1 · Bindings

- ⛔ **`tasklist | grep -i Mars` — `Mars.exe` must NOT be running before you edit
  loadable code.** A step of its own, in your todo list.
- ⛔ Never modify the game directory. `A:\SteamLibrary\steamapps\common\Project
  Spark\ModTools\Src` is read-only 1.1.0 truth. ⛔ Never "correct" a 1.0.7
  citation in an old entry — `EF-075`, the 1.0.7 tree is GONE from disk.
- ⛔ `H-08` never pull a junction · `H-09` never stage a packed folder beside one.
- ⛔ `H-02` **an agent never opens the Mod Editor and never hand-sets `version`.**
  The upload sitting owns the bump. Every other `metadata.lua` edit
  (`last_changes`, descriptions) is ordinary agent work.
- **The release gate is NOT a per-change tax** (owner 08-20, ck57). Post-release
  is patch-note maintenance: `items.lua` (nothing here) + one boot `applied` log
  + doccheck counts. ⛔ **Do NOT quote `FIX_POLICY` §3a's per-module cost, and do
  NOT run config B or a lens sweep** — those return only for a major overhaul.
- `python tools/doccheck.py` GREEN before any doc commit. `STATE.md` is
  byte-capped — an addition needs an eviction **in the same commit**.
- Commits `git commit -F <file>`, then **push**.
- ⚠️ **A log copied while the game is RUNNING is a PARTIAL log.** This cost the
  project twice on 2026-09-08 (a "1 throw" that was 6; a "30 throws" that was
  157). **Re-copy after the process exits before quoting any count or rate.**
  Use `python tools/logscan.py <file>` — hand-grepping for a file path misses
  the `[LUA ERROR]` header form that carries no path.

## 2 · TASK A — the F115 gate (the only code you must write)

**F115 is confirmed live and reproduced on demand** (`bugs/F115.md`):
`Fix_LandscapeUnitFilter` full-body-replaces the global `LandscapeForEachUnit`,
and 1.1.0 changed its SIGNATURE —

```
1.0.7:  function LandscapeForEachUnit(mark, callback, ...)
1.1.0:  function LandscapeForEachUnit(map, mark, callback, ...)   Landscaping.lua:509
```

— so every argument arrives one slot late and the body then indexes the global
`Landscapes`, which 1.1.0 moved to `MapVar("Landscapes", {})` and reads as
`map.Landscapes[mark]`. Owner decision **109 = GATE** (not repair).

**Write a `Require` entry that declines on the 1.1.0 shape.** ⛔ You cannot use
`{ global = "LandscapeForEachUnit" }` — the name still exists, which is the
whole reason this shipped. ⛔ You cannot read arity: `debug.getinfo` is absent
in the mod sandbox (the boot log says so).

**Suggested discriminator, and you must justify or replace it:**

```lua
{ test = function()
        local mv = rawget(_G, "MapVars")
        if type(mv) ~= "table" then return false end   -- cannot tell => decline
        for _, n in ipairs(mv) do
            if n == "Landscapes" then return false end -- 1.1.0 shape => decline
        end
        return true                                    -- 1.0.7 shape => apply
    end,
  reason = "the landscape API is per-map now (game update changed it?)" },
```

`MapVars` is the engine's registry of MapVar names (`CommonLua/Core/lib.lua:980,
:994`); `Landscapes` is registered at `Lua/Landscape/Landscaping.lua:21`.
⚠️ **Verify at runtime that `MapVars` is populated when mod code loads** — if it
is not, this test declines always, which is SAFE but makes the module dead on
1.0.7 too. If you cannot verify it, say so and pick a discriminator you can.

⛔ **It must set `update_suspect` explicitly.** This IS patch rot and the dialog
must name it. A bare `test` entry does NOT set it — `00_Core`'s `Require`
deliberately exempts content checks, and `run_apply` clears `update_suspect`
ONLY on the active branch, so a write inside `apply` before returning the reason
string survives. Follow `Fix_TrainCargoDumping`'s F114 gate (`8bc6821`) exactly.

⛔ **Do NOT repair the body.** A repair pins us to 1.1.0's signature and
re-breaks on the next change. The owner ruled gate.
⭐ **Record in the entry, do not act on it:** 1.1.0 did NOT fix the underlying
F34(d) defect (`Landscaping.lua:520` still passes `callback` instead of its own
`filter_embark`), so this fix is still WANTED — a live fix with a broken body,
not an obsolete one. It gets re-armed properly in a later patch, not this one.

## 3 · TASK B — two open questions you must ANSWER, not assume

### B1 · Does `00_Core`'s override surface ship? (**decision 110 — NEW, put it in the checklist**)

`be4c99e` adds **+151 lines** to `00_Core.lua`: `SMRFixPack_Force`,
`SMRFixPack_NoUpdateDialog`, `SMRFixPack.ForceApply`, plus an `entry.data_latched`
marker. It **ships inert** — nothing in the pack writes the override, and with
the table unset every path is byte-for-byte the shipped behaviour. It has booted
cleanly 4+ times including a 42-minute session.

⚠️ **But this patch's whole premise is "our fail-safe did not work."** Shipping
151 lines of unrelated diagnostic scaffolding in that patch is a real risk-hygiene
question, and the agent who wrote it (this session's predecessor) flagged it
rather than waving it through. **Two routes, and the AUDIT link rules:**
- **(a) ship it inert** — no new untested state; it is already exercised.
- **(b) revert `00_Core.lua` to `ce77162` for the hotfix**, re-apply after — but
  that CREATES a new untested tree, which is its own risk.
⛔ Do not decide this alone. Put it in `PLAYTEST_CHECKLIST.md` as **110** with a
recommendation, and let the audit link and the owner settle it.

### B2 · Does F116 belong in this patch?

`F116` (`bugs/F116.md`) is **source-read, NOT reproduced, and silent by
construction** — `Fix_TrackSalvageWipe`'s 1.0.7 `DemolishAndSplitTrack` copy
lacks 1.1.0's `ProcessAllElements()` node_idx revalidation AND its
orphan-reassign safeguard. The owner's bar for this patch is **"failing hard and
visually right now."** F116 has never been seen fail.

⇒ **Default: NOT in patch 1.** But its branch (a) is player-visible ("click
demolish on a mid-track element, nothing happens"), so:
⭐ **Run its control during the audit playtest** (`bugs/F116.md` names it):
salvage a MIDDLE element of a multi-element track, pack on. Nothing happens, no
log line ⇒ branch (a) confirmed ⇒ it IS failing visibly and should be gated into
this patch. Splits correctly ⇒ leave it filed for patch 2.
⛔ Run it only AFTER the F114/F115 gates are in, or the train throw confounds it.

## 4 · Verification — the boot log IS the test

There is no Lua binary on this rig. Structure review + `python tools/sigcheck.py`
+ a block-balance check are the desk half; **the owner's boot log is the real
one.** ⛔ Never report a gate as working on a parse sweep.

**Predict before you look, then reconcile** — a difference is a FINDING:
- **17 inactive / 14 named** (15/12 measured + `TrainCargoDumping` + `LandscapeUnitFilter`).
  ⚠️ The peer session predicted 16/13 for the F114 gate alone; yours adds one to each.
- `TrainCargoDumping: inactive (...)` and `LandscapeUnitFilter: inactive (...)`, both NAMED in the dialog.
- **ZERO** `Fix_TrainCargoDumping.lua:89` lines and **ZERO** `Fix_LandscapeUnitFilter.lua:63` lines.
- The owner's train **leaves its platform**; landscaping raises **no mod-error dialog**.
- ⛔ If the count is 16/13 or 17/13, that is a finding about `00_Core`'s
  `update_suspect` handling, NOT a bookkeeping slip. Investigate, do not adjust.

Run `python tools/logscan.py --build 6a91a190` and reconcile every 1.1.0 log.

## 5 · Close out

- `bugs/F115.md` → the gate landed + the measured boot result. `F116` → the
  control's result, whatever it is. Status words: `tested-attended` needs an
  attended witness; the owner is present, so a screen claim CAN be made **for
  what was actually watched** and nothing else.
- New facts → `agent/facts/` (`EF-082`+), INDEX regenerated via
  `split_facts.load_from_dir()` + `render_index()` (it returns a LIST — join it);
  `lines:` must equal body length. ⛔ The INDEX is GENERATED, never hand-edited.
- **`metadata.lua` `last_changes`** — write the patch notes. ⛔ Never name
  fredware's mod on a player surface (`EF-054`, `FIX_POLICY` §8); no load-order
  advice. ⚠️ **Do not imply the pack is now verified on 1.1.0**: **17 of the 22
  full-body replacements are still undiffed**, and no instrument we own bounds
  body divergence (the name sweep sees names, `sigcheck` sees arity, the runtime
  self-checks see existence — F114 was invisible to all three).
- ⚠️ **`UPLOAD_WORKFLOW` §3 paste backups are REQUIRED, not polish** — auto-fill
  has never delivered a clean page in 2 cycles. Sync them with `metadata.lua`.
- Owner decisions → `PLAYTEST_CHECKLIST.md` → "Decisions waiting on you"
  (110 at minimum), never only an agent doc. A `doccheck` WARN is copied
  **verbatim** into your summary.
- A leg in `archive/SESSION_LOG.md` (append-only, newest first). Update `STATE`.
- `doccheck` GREEN → commit → **push** → **hand to `HOTFIX_1_AUDIT.md`.**

## 6 · What "done" is

The F115 gate is in and MEASURED on a boot log; 110 and the F116 control are
answered rather than assumed; patch notes written and honest about what is not
verified; doccheck GREEN; everything pushed. ⛔ **No upload, no `version` edit,
no Mod Editor, and no status moved on anything not actually witnessed.**
