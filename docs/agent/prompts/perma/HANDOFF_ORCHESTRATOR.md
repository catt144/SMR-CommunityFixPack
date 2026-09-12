# Handoff — the orchestrator session → the next session (model-agnostic)

⏳ **TEMPORARY resident of `perma/`** (owner, 2026-09-11): it stays here only until the pending outbox (§3) is empty or the owner
says things have settled, and then it is `git rm`'d. Its history is in SESSION_LOG, and each item has a named home. Written
2026-09-11 by `smr-bugfixpack-5d` at the owner's stop (context); **updated the same day by `smr-bugfixpack-0d`** at its stop
(field leads: §1b, §3, §4). **Verify every specific against `git log` and the tree**; the records win. Claude and Codex sessions both
commit here, and Codex is invisible to `ListAgents`.

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

### 1b · Later the same day (`smr-bugfixpack-0d`) — six field leads, two fixes built

- **Triage** of six owner-relayed reports (Steam + Reddit): `reports/FIELD_LEADS_2026-09-11.md` (the table at the top is current).
- **F119 (P1)** — a landed Trade rocket never re-sizes its fuel request, so the Wildfire cure rocket soft-locks the mystery.
  **Built `2c68bb1`** (`Fix_TradeRocketFuelRefresh`) from a one-off brief in a separate session; attended check staged `8787d0f`
  (checklist **149**) and RAN 09-11 (`smr-bugfixpack-24`): **tested-attended** — A/B plus the load heal, in play.
- **C86 (P3)** — the Advanced Orbital Probe downgrades deep-scanned neighbours. **Built `5ca9a0f`** (`Fix_ScanDowngrade`), desk 7/7;
  seam check in play 09-11, **tested-attended**.
- Both sit in `perma/RELEASE_OUTBOX.md` → Pending (both tested-attended 09-11; the upload is the owner's). The build brief was closed and removed
  (`91f32af`).
- **Candidates:** C85 (clogged after a dust storm), **C87** (lakes, reopened on the owner's pushback), **C88** (Building Codes vs
  prefabs, reopened on the owner's pushback, waiting on the devs). Meteors: not a bug. Deep scan: the Adapted Probes rule.
- Peer `smr-bugfixpack-24` authored the fixtoggles chain (`prompts/fixtoggles/`, checklist **148**); it owns any Beta label.

### Later on 2026-09-11 — the migration cluster shipped, from `smr-bugfixpack-cb` (+ `-31`, `-b7`, `-d3`)

- **F59 REPAIRED, AUDITED AND WITNESSED IN PLAY.** An independent re-derivation confirmed the audit's expedition
  claim and found a **second, more reachable harm** the report missed (manual **Set Residence** on a full home
  left it **over capacity** with the eviction undone — both game branches, shipped since the module was written).
  Repaired by deferring the notification out of the caller's stack (`3b41d9f`), Fable-audited **SHIP A**
  (`74b2c8f`), then **observed working by the owner at the keyboard** (`11d163e`): `residents=14` against
  `cap=20 closed=6`, with `HasAnyFreeLivingSpace()=false` proving the check was not vacuous.
  Owner granted **`tested-attended` for the A2 half only** (`2cbd729`).
- **F60 RETIRED** by owner ruling (`9bc4360`) — module deleted across `Code/` + `items.lua` + the `metadata.lua`
  code list together; card count **50 → 49** on all five copies (`0392162`); site fix-list row removed and the
  **F51/F58 rows narrowed** (`SMR-CommunityMods` `a061665`).
- **C85 (clogged producers) solved at source** and written up: vanilla's `SetBuildingEnabledState` has a
  `Duration` branch that auto-re-enables and two shipped events use it, while `BuildingClogged` passes only a
  `Reason`; and a **lost reply is permanent, not delayed**. Build prompt `prompts/CLOGGED_BUILD.md` is fireable.
- **A Reddit report was REFUTED, not filed** ("160% productivity"): the extractor upgrades move Production, never
  Performance, in either version, and 1.1.0 made that goal *easier* twice over. Reply drafted; **ck153**.
- **Two of our own records were corrected** — F108's Amplify attribution and C39/F112's reading of the
  automation-law uplift (1.1.0 deleted it, and the arithmetic says that removed a bug).
- **Rules landed:** `FIX_POLICY` §4 ×2 (enumerate the wrapped function's **callers**; anything deferred into a
  game-time thread **rides in the player's save**) and `EF-019`'s unpersistable-body fallback. `EF-092` (a
  constant-comfort desk stub deletes an inherited validity test) came from `-31` and cost a false finding that
  three sessions agreed on.

## 2 · Where things live now

- STATE is the kernel. Owner decisions are in checklist → "Decisions waiting on you".
- FR-1 has the LINUX_DISPATCH prompt, FINDINGS §11–§12 and ck145.
- The release machinery is `prompts/perma/RELEASE.md`, with its outbox ledger `perma/RELEASE_OUTBOX.md`.
- Field-report reply drafts: `docs/FIELD_REPORT_REPLIES.md` (the 2026-09-11 section).

## 3 · Pending outbox — retire this file when every line is done or rehomed

**FR-1 (all of it goes to `perma/LINUX_DISPATCH.md`; listed here only so the outbox is complete):**
- The GTX 1070 player's log: PLAYER LOG REQUEST sent? Answer pending.
- The dev "CURRENT DEV NOTE" and the "PLAYER REPLY": posted? Ask.
- The Steam BBCode and Paradox paste-in styling: done? The owner was pasting on 09-11.

**Fix pack — from `smr-bugfixpack-e6` (2026-09-11, the PDX dev's reply):**
- ✅ **Migration audit DISCHARGED 09-11 (was: complete, awaiting decisions).** Report
  `reports/MIGRATION_DEV_REPORT.md`, Fable cross-check `reports/MIGRATIONFIX_AUDIT.md`. **151 (a)–(e) all ruled:**
  F59 repaired + witnessed, F60 retired, 1.0.7 stays frozen. ⛔ **What is still owed from it:** F59's **A1
  expedition half is UNTESTED** (no expedition boarded — source-derived only, and no in-play reproduction of the
  original defect exists on either branch); **F80** is still capture-before-mitigate and nothing here mitigated
  it; and the developer-sharing decision in 151 (b) is untouched. ⚠️ The report's F51/F58/F73 verdicts were
  surface-swept by the audit, not re-derived.
- **`prompts/C88_PREFAB_BUILD.md` — READY, not started. ⚖️ Owner ruling 09-11: this build goes to a CLAUDE session,
  not Astra** (hunts → Astra, builds → Claude). Gated on (1) the release lane clearing (H-10 needs an `items.lua`
  entry, and `items.lua`/`metadata.lua` are the owner's uncommitted v8 pack) and (2) checklist 150 (b).
- **Checklist 150** carries the owner's three decisions: the "where do you collect your bugs" wording, the C88 fix
  shape, and retiring F37 (1.1.0 closed its leak — the dev was right).

**Fix pack — from `smr-bugfixpack-cb` (2026-09-11, the migration cluster):**
- ⏳ **`RELEASE.md` IS RUNNING** in `smr-bugfixpack-d3` as this was written — it consumes `RELEASE_OUTBOX`
  (four Pending entries, count chaining to **49**), sweeps the public surfaces and hands the owner the upload.
  ⚠️ Three surfaces were applied **ad hoc from a dispatch session** before the sweep ran (card count, site
  fix-list rows, F51/F58 rewordings) — treat them as unverified input, not a completed sweep; the F51/F58 wording
  has had no second reader. **`last_changes` was the real hole** and is the release prompt's to fill.
- **`prompts/CLOGGED_BUILD.md` — FIREABLE, not started** (C85). Fold-in slot closed empty. **ck154** carries one
  decision that changes what gets built (sweep only vs sweep + a `Duration` DataPatch; default = sweep only, and
  only the sweep rescues already-stuck saves) and one on whether its in-game A/B joins the owed sitting.
- **ck153 — the Reddit "160% productivity" reply:** post it or not. Not a defect; nothing to build.
- **Loose end, not release-blocking:** the TestKit probe `DomeFreeSpaceMismatch` (`30_Probes_Wave3.lua`) targets
  the deleted F60 module and will fail on the next kit run. TestKit is local-only by design.

**Fix pack — from `smr-bugfixpack-0d` (newest first):**
- ⭐ **ck149: the check RAN 09-11 — F119 and C86 are both tested-attended (`smr-bugfixpack-24`). The upload remains**, the
  owner's: `prompts/perma/RELEASE.md` (the outbox holds both entries).
- **ck147: field replies.** Post the Wildfire, clogged and deep-scan drafts (`FIELD_REPORT_REPLIES.md`); the lakes reply is
  HELD until the lake check; meteors: skip. The owner decides.
- **C87 lakes:** the 2-minute in-game check plus the copy-paste `LAKECHK` line in ck147 decides "every 1.1.0 map" vs
  "that player's map". The code is unchanged from 1.0.7, so a new warning means an input changed (C87 §Evidence).
- **C88 Building Codes:** ✅ the dev ANSWERED 09-11 (not intended, fixed in their next patch; include it meanwhile), recorded
  in C88. The same post: F37 not reproducible, which is TRUE on 1.1.0 (F37's 1.1.0 section, a REMOVE candidate). Checklist
  **150**: the reply wording, the C88 shape, and F37 removal. Reply draft: `FIELD_REPORT_REPLIES.md`, "Reply to the developer".
- **C85 clogged:** needs the reporters' answer (which popup reply; save/load with the popup open). The fix sketch is
  hypothesis-agnostic but needs the owner's call on overriding "fix it after the storm".
- **Checklist numbering collision:** two headings are numbered 144 — the open v7 asks (`### 2026-09-10 — 144: two small asks`)
  and a closed C84 item (`### ✅ 2026-09-10 — 144 CLOSED`). Renumber the closed one only if the owner agrees.

**Fix pack — from `smr-bugfixpack-5d`:**
- **ck144 (a): the owed v7 sitting, ONE boot.** A3 (F118), A10, A5 c2, A9 c4/c5, F117's station recipe, and the first `RunAll()` on the
  94-probe kit (the STATE OWED line). Recipes: the checklist's "THE SITTING RAN" block, `prompts/HOTFIX2_SITTING.md` and
  `bugs/F117.md`. `prompts/SELFCHECK_PILOT.md` rides the same boot (see its banner). It can share ck149's boot.
- **ck144 (b):** the Steam sounds thread. A "still checking" follow-up is drafted in `docs/FIELD_REPORT_REPLIES.md`.
- **Desk NEXT:** `prompts/DLC_DEEP_CHECK.md` (bounded; the owner's framing is in its banner).
- **`FIELD_REPORT_REPLIES.md`:** the Hydroponic Farm stub (the owner's design question) and Metatron `End1..7` particles (fixable,
  untimed).
- **Open owner decisions:** checklist → "Decisions waiting on you" (STATE lists the numbers).
- **Upstream drafts:** options report §5.1 (vkd3d/pyroveil) and §5.2 (Paradox) are unposted; the owner's call.
- **Unexplained lines, verbatim; attribute only if asked:**
  - `Failed activating D3D12 Dred`
  - `OptionsData.Options.Upscaling sets hr.ResolutionUpscale which was already set by another table`
  - `Missing spot 'Top' in 'ElectricityGridElement' state 'idle'` — ✅ attributed 09-11 (`smr-bugfixpack-24`, owner asked):
    vanilla. A broken cable's sign (`SupplyGridBreakable.lua:277-282`) asks for the building sign spot "Top", which the
    cable model lacks; `gamelib.lua:161-166` prints once and falls back to origin. Identical Lua on 1.0.7; harmless.
  - P1's `d3d12_resource_QueryInterface {6b3b2502-…} E_NOINTERFACE` ×4

**Closed here:** the Astra R3 brief (removed 09-11); the F119/C86 build brief (fired and removed 09-11, `91f32af`). Astra has nothing
open from either session.

## 4 · Practice from these sessions (also in the SESSION_LOG lookbacks)

- **"Run <handoff>" plus an evidence path** meant: execute what the handoff names. The owner's later direct asks (build it,
  reorganise) overrode standing rules. Each override was flagged in one line and done.
- **vkd3d dump names are the FNV-1 hash of the DXBC,** so a Proton log alone identifies cached shaders. The tool is
  `C:\Dev\SMR-FR1-TempMod-2026-09-11\tools\identify_dump_names.py`.
- **PowerShell:** `git commit … *> $null` sets `$?` false even when the commit succeeds, which once skipped a push silently. Test
  `$LASTEXITCODE`, and read back `HEAD` against `origin/main`.
- **Store text:** `metadata.lua`'s `description` is the upload auto-fill source. Keep it word-identical to the Paradox block, and check
  that with a script, not by eye.
- **Field-lead triage (0d):** fan the leads out to read-only investigators, then re-read every load-bearing line yourself before
  filing — the re-read caught a wrong citation and found the 1.1.0 laws that explain why F119 surfaced now.
- **Two verdicts the owner overturned (0d):** a terrain story fitted to a report pattern without the screenshot (C87), and
  "intended" for an explicit code exemption that contradicts the player-facing text (C88). When the evidence artefact is missing,
  say "unverified"; when code contradicts the description, report the mismatch and ask the devs.
- **Three sessions committing at once, zero collisions:** claim ids and checklist numbers by message before writing, re-check
  `git status` before every `--regen`, commit by pathspec.
