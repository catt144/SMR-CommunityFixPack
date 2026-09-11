# Handoff — the orchestrator session → the next session (model-agnostic)

⏳ **TEMPORARY resident of `perma/`** (owner, 2026-09-11): it stays here only until the pending outbox (§3) is empty or the owner
says things have settled, and then it is `git rm`'d. Its history is in SESSION_LOG, and each item has a named home. Written
2026-09-11 by `smr-bugfixpack-5d` at the owner's stop (context). **Verify every specific against `git log` and the tree**; the records
win. Claude and Codex sessions both commit here, and Codex is invisible to `ListAgents`.

## 0 · Orient, then ask

`git pull` · `git log --oneline -15` · `git status --short` · `ListAgents` · `docs/agent/STATE.md` ·
`prompts/perma/DISPATCH.md` §0–§3 · `prompts/README.md` (the prompt map, new 09-11). Open a **live todo list**. Unless the owner's
message names a task, this handoff is **orientation**: summarise §3 and **ask** what to take (memory:
handoff-invocation-means-orient-first).

**⛔ FR-1 is NOT on this handoff.** Every Linux / NVIDIA 580 / workaround-mod item goes to `prompts/perma/LINUX_DISPATCH.md`,
which is fully briefed.

## 1 · What happened on 2026-09-11

- **FR-1 v2 bench read** (FINDINGS §11). The no-reload shader-cache overlay loads worlds on 580, the reversal brings the crash back,
  and the control is valid.
- **Scope ruled (ck145):** a separate, TEMPORARY mod with no repo. The owner then asked this session to build it directly, a
  deliberate departure from "Astra builds". The Astra R3 brief was held, then removed.
- **Built** `SMR_FR1TempWorkaround` (desk harness 21/21). P1, the packed mod, is MEASURED working. Store pages were written, and the
  mod went **LIVE**: Steam 3799500849 (public), Paradox 158711 (FINDINGS §12).
- **Dev and player posts** drafted: "CURRENT DEV NOTE", "PLAYER REPLY" and "PLAYER LOG REQUEST". **Field reports so far:** 3 working
  (one a 10xx), 1 failing (GTX 1070), with the Workshop copy verified working.
- **Prompts reorganised:** `perma/` holds the reusable prompts, the root holds live one-offs, and five fired one-offs were removed.
  The map is `prompts/README.md`.

## 2 · Where things live now

- STATE is the kernel. Owner decisions are in checklist → "Decisions waiting on you".
- FR-1 has the LINUX_DISPATCH prompt, FINDINGS §11–§12 and ck145.
- The release machinery is `prompts/perma/RELEASE.md`, with its outbox ledger `perma/RELEASE_OUTBOX.md`.

## 3 · Pending outbox — retire this file when every line is done or rehomed

**FR-1 (all of it goes to `perma/LINUX_DISPATCH.md`; listed here only so the outbox is complete):**
- The GTX 1070 player's log: PLAYER LOG REQUEST sent? Answer pending.
- The dev "CURRENT DEV NOTE" and the "PLAYER REPLY": posted? Ask.
- The Steam BBCode and Paradox paste-in styling: done? The owner was pasting on 09-11.

**Fix pack:**
- **ck144 (a): the owed v7 sitting, ONE boot.** A3 (F118), A10, A5 c2, A9 c4/c5, F117's station recipe, and the first `RunAll()` on the
  94-probe kit (the STATE OWED line). Recipes: the checklist's "THE SITTING RAN" block, `prompts/HOTFIX2_SITTING.md` and
  `bugs/F117.md`. `prompts/SELFCHECK_PILOT.md` rides the same boot (see its banner).
- **ck144 (b):** the Steam sounds thread. A "still checking" follow-up is drafted in `reports/FIELD_REPORT_REPLIES.md`.
- **Desk NEXT:** `prompts/DLC_DEEP_CHECK.md` (bounded; the owner's framing is in its banner).
- **`FIELD_REPORT_REPLIES.md`:** the Hydroponic Farm stub (the owner's design question) and Metatron `End1..7` particles (fixable,
  untimed).
- **Open owner decisions:** checklist → "Decisions waiting on you" (STATE lists the numbers).
- **Upstream drafts:** options report §5.1 (vkd3d/pyroveil) and §5.2 (Paradox) are unposted; the owner's call.
- **Unexplained lines, verbatim; attribute only if asked:**
  - `Failed activating D3D12 Dred`
  - `OptionsData.Options.Upscaling sets hr.ResolutionUpscale which was already set by another table`
  - `Missing spot 'Top' in 'ElectricityGridElement' state 'idle'`
  - P1's `d3d12_resource_QueryInterface {6b3b2502-…} E_NOINTERFACE` ×4

**Closed here:** the Astra R3 brief (removed 09-11). Astra has nothing open from this session.

## 4 · Practice from this session (also in the SESSION_LOG lookback)

- **"Run <handoff>" plus an evidence path** meant: execute what the handoff names. The owner's later direct asks (build it,
  reorganise) overrode standing rules. Each override was flagged in one line and done.
- **vkd3d dump names are the FNV-1 hash of the DXBC,** so a Proton log alone identifies cached shaders. The tool is
  `C:\Dev\SMR-FR1-TempMod-2026-09-11\tools\identify_dump_names.py`.
- **PowerShell:** `git commit … *> $null` sets `$?` false even when the commit succeeds, which once skipped a push silently. Test
  `$LASTEXITCODE`, and read back `HEAD` against `origin/main`.
- **Store text:** `metadata.lua`'s `description` is the upload auto-fill source. Keep it word-identical to the Paradox block, and check
  that with a script, not by eye.
