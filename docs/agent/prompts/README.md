# prompts/ — the map (reorganised 2026-09-11, owner ask)

| where | what | lifecycle |
|---|---|---|
| **`perma/`** | reusable, standing prompts: fire any time | never `git rm`; update in place |
| root `*.md` | live one-off prompts, not yet fired or kept by an owner ruling | `git rm` when fired or consumed |
| chain folders | multi-link efforts; finished ones are records that other docs cite | keep; each README says its state |

## `perma/` — standing prompts

| prompt | use it for |
|---|---|
| `DISPATCH.md` | **start here for ad-hoc work:** orientation, bindings, and the route table to the others |
| `LINUX_DISPATCH.md` | **FR-1**: the Linux/NVIDIA 580 crash and the TEMPORARY workaround mod; every report, feedback item or patch |
| `HANDOFF_ORCHESTRATOR.md` | ⏳ temporary: the current handoff and pending outbox; removed once the outbox is empty |
| `GENERAL_USE_PROMPT.md` | a live playtest at the keyboard (a 09-09 handoff called parts of it pre-1.1.0; verify before relying on it) |
| `RELEASE.md` | an update, end to end; uses `RELEASE_OUTBOX.md` (the staged-changes ledger) and `POST_UPLOAD_CLOSE.md` (the close-out) |
| `PUBLIC_SURFACE_SWEEP.md` | making every player-facing surface match a shipped change |
| `SITE_AUDIT.md` | auditing what the LIVE Pages site says, as opposed to what is committed |
| `STATE_EVICTION.md` | when STATE is over its byte budget |
| `DRONE_PROJECT_PROMPT.md` | drone work |
| `COMBINED_SITTING.md` | the PT-20 per-era re-check recipe (it ran 08-14; nothing owed) |
| `CO_RUNS.md` | the attended co-run protocol (labor-inverted experiment legs); binding when it applies |

## Root — live one-offs

| prompt | state |
|---|---|
| ~~`SITTING_158.md`~~ | **FIRED 2026-09-12** (`smr-bugfixpack-2a`, attended, owner at the keyboard; grave = this commit): **the v10 gate is CLEAR.** C85, C89 and C88 all `tested-attended` in ONE boot — 49/49 modules applied, zero error-shaped lines, exit 0. C89's A/B ran as a **boundary pair on one dome** (10 → gate inactive, 9 → `GATE ACTIVE`, 3 rows `shipped=true live=false`), stronger than the recipe asked. C88 confirmed the prefab branch from the site itself (`prefab=true`) and measured maintenance 1000 → 700. ⛔ **B2 NOT RUN by owner ruling** — one link unmeasured (`CountDome` 0 ⇒ panel clear); **reopen C89 on a countering field report**. Evidence lives in each entry's §Attended check + checklist 158. Next: `perma/RELEASE.md` on the Held batch = v10. |
| ~~`VANILLA_DIFF_DISPOSITION.md`~~ | **FIRED 09-12** (`smr-bugfixpack-b2`; grave = the commit landing `reports/VANILLA_DIFF_DISPOSITION.md`): the procedure gap is CLOSED — `WORKFLOW.md` gains a binding **"After a game patch — the source-diff instruments"** section (archive-first, `bodycheck`+`sigcheck` every patch, `treediff`/`presetdiff` on trigger) carrying the **canonical trust table** and the four-claim rule; `FIX_POLICY` §2b points at it, nothing duplicated. Nothing retired. Re-derived rather than relayed: `HUNT_AUDIT` §1.4's 1,281 hunks **reproduce from scratch** (1,325 / 378 files) — its script `a4_gap.py` was never committed — and **29 of the 51 files the pack pins carry hunks `bodycheck` cannot see**, which prices the one pass worth taking. NO-MANIFEST = `00_Core.lua` (omission) + `90_SaveSanitizer.lua` (real gap). Owner decisions = checklist **163**, which if ruled closes 137/138/140/141/142. |
| ~~`DESKBENCH_C90.md`~~ | **FIRED 09-12** (Codex; grave = the commit landing `reports/DESKBENCH_C90.md`): F60 harness repaired from git with all 16 demands kept; C90 actual-core control 18/18, complete four-plus-two callback census, eight scratch falsifiers. C90 remains cand; fix shape stays with owner, no shipped Lua changed. |
| ~~`SURFACE_AUDIT_FABLE.md`~~ | **FIRED 09-12** (`smr-bugfixpack-07`; grave = the commit that landed `reports/SURFACE_AUDIT_2026-09-12.md`): F37/F43 retirements confirmed, F31 settled → RETIRE recommended, three ruled sentences refuted with replacements; decisions on checklist 159. Next: `perma/RELEASE.md` on the Held batch = v10 |
| ~~`C85_C88_BUILD.md`~~ + ~~`CLOGGED_BUILD.md`~~ + ~~`C88_PREFAB_BUILD.md`~~ | **FIRED 09-12** (`smr-bugfixpack-aa`; graves = `59c8c47` C85, `98d0461` C89, `4dc5073` C88): all three modules built, desk-controlled and falsified; **C90** and **C91** filed on the way (our own DataPatch self-check gap; vanilla leaks the Building Codes modifier on repeal). Attended A/B for all three = checklist **158**. Next: `perma/RELEASE.md` on the Held batch + the three new Pending entries = v10 |
| ~~`migrationfix/`~~ | **CONSUMED 09-11, both links.** Link 01 (`3b41d9f`) repaired F59 by deferring the notification (a THIRD harm found while building) and stopped F60's retirement on the uncommitted-release-file gate; link 02's terminal audit ruled **SHIP A** — `reports/MIGRATIONFIX_AUDIT.md`. Link 01's HANDOFF lives in git: `git show 3b41d9f:docs/agent/prompts/migrationfix/README.md` |
| ~~`C90_GUARDS_BUILD.md`~~ | **FIRED 2026-09-12** (Codex; grave = the commit landing `reports/C90_GUARDS_BUILD.md`): Saint + Sinkhole apply-success guards built for v10; historical harm demands preserved, live decline controls held, scratch falsifiers discriminate. C89 retry claim refuted on the current non-optional path; C89 unchanged. Status `fixed`, ships unexercised in play, no public row. |
| ~~`SITE_ALIGNMENT_AUDIT.md`~~ | **FIRED 2026-09-13** (`smr-bugfixpack-17`; grave = `d86a347` in `SMR-CommunityMods`): built the retired set (40 modules deleted since hotfix 2 + F60/F37/F43+F118/F31) and swept every player-facing surface against it. **One orphaned promise found, the predicted one** — `faq.md`'s save-repair list still named F37's "phantom farm oxygen"; fixed and pushed alongside the already-sitting judgment-call Three→Four edit. Nothing else orphaned: the hotfix-2 batch's fix-list rows, and F60/F43/F31/F118's, were already clean. Live-vs-committed re-derived via the deployments API (50 vs 49, unchanged). Owner's 2 remaining pared files (`for-modders.md`, `install.md`) left untouched, decision 47 still open. **Site deploy is content-clear to fire** — never fired here (H-04/owner's act). Closed the hole permanently: `PUBLIC_SURFACE_SWEEP.md` §1 gains a "When a fix is RETIRED" check. |
| ~~`DOC_OVERHAUL_AUDIT.md`~~ | **FIRED 2026-09-13** (Codex; grave = the commit landing [the report](../reports/DOC_OVERHAUL_AUDIT.md)). Loose ends remain: GREEN can hide owner obligations, fingerprints omit dependencies, and the archive script cannot execute D4. The delivered v10 archive was found; its apparent extra entries are a nested-table reader defect. Policy choices are checklist **170**. Report-only; no tools, existing statuses, or shipped Lua repaired. |
| ~~`C92_PLACEMENT.md`~~ | **FIRED 2026-09-13** (Codex with three sub-agents; grave = the commit landing [the report](../reports/C92_PLACEMENT.md)). Packed Data/Lua/DLC comparison, full research-art survey, owner-directed Industry/Hi-Tech pass, historical mappings and production/residue controls completed. Prior 44% water, complete conversion-cohort, never-drawn art and unremovable-residue claims corrected. Underground I is authored family evidence; the owner's complete ring supplies no missing seat. Exact intended icon/position remains unrecovered. C92 stays `cand`; owner scope choice is checklist **171**, recommendation narrow achievement repair. |
| ~~`HAZARD_KERNEL_PASS.md`~~ | **FIRED 2026-09-13** (Codex; grave = phase 2 commit deleting the brief). Owner's kernel rulings implemented in separate hazard and redundancy commits; [handover](../reports/HAZARD_KERNEL_PASS.md) quotes all landings and records verification. Open-decisions enumeration, naming prohibition, upload-overwrite rule and frozen-v5 service text retained where marker coverage or canonical homes prevent collapse. Separate-session adjudication still required. |
| `C92_ACHIEVEMENT_BUILD.md` | ⛔ **LIVE, NOT FIRED — HARD-GATED TO PLAYTESTING** (owner, 2026-09-13). Builds C92's narrow achievement repair: additional listener (the vanilla filter is a file local), a named recovery trigger for an already-complete colony, and a REQUIRED four-shape behaviour decline. Evaluates `EF-093`'s self-healing residue seam but should need no residue at all. ⛔ Build + desk-control + checklist recipe, then STOP — no release, no public row. Presumes decision **171 = A**. |
| `STANDDOWN_AUDIT.md` | **LIVE, authored 2026-09-13** (owner ask): can our full-body replacements stand down when vanilla fixes the defect? 21 of 45 modules do not delegate; `bodycheck` is at full coverage but declares a **class-c** blind spot (semantics moving under an unchanged body), and `debug.getinfo` is unavailable in the mod sandbox so only behaviour probes are buildable. Design record [D14](../bugs/D14.md). |
| `DLC_DEEP_CHECK.md` | desk NEXT, after the fix pack is stable |
| `HOTFIX2_SITTING.md` | closed 09-09; kept for the recipes the owed v7 sitting uses |
| `SELFCHECK_PILOT.md` | ⛔ **UNREACHABLE 09-12 — do not fire.** Its job was ck133 (1), the self-check pilot; the owner ruled the **reword** instead (ck112 = (a)), so there is nothing for it to measure. **Removal recommended, awaiting the owner's word** (ck133) — nothing has been deleted. |
| `CAPTURE_SITTING.md` | owner ruling 09-09: KEEP ("we may get to it") |
| `SMRCF_CHAIN_SET.md` | owner ruling: keep for now (it goes with `smrcf-modbrowser/` and `smrcf-verify/`) |

## Chain folders

- `fixtoggles/`: **LIVE** (authored 09-11): an on/off button per fix, Beta labels, linked buttons; link 09 researches
  versioning for a B step. Its README is the manifest; checklist 148.
- `arming/`: the unattended-leg harness (`tools/arm_leg.ps1` reads it). Infrastructure, not a prompt.
- `hotfix2/`: done (v6 shipped 09-09); STATE and the entries cite its manifest.
- `vanillahunt/`: done (CLOSED 09-10).
- `prelaunch-sweep/`: done 08-20. ⛔ H-05 sweep fence: never read `SWEEP_FINDINGS.md` to reach a verdict.
- `smrcf-modbrowser/`, `smrcf-verify/`: see `SMRCF_CHAIN_SET.md`.

**Removed 2026-09-11** (git history keeps them): `FR1_LINUX_SITTING.md` (ran 09-10; superseded by `perma/LINUX_DISPATCH.md`),
`FR1_TEMP_MOD_R3.md` (held, then overtaken by the live mod), `ONCALL_HANDOFF.md` (09-09; duplicated DISPATCH and nothing cited it),
`SELFCHECK_PROMISE_AUDIT.md` and `CODEX_CROSSCHECK_SELFCHECK_PROMISE.md` (both delivered their reports). Find any of them with
`git log --diff-filter=D -- docs/agent/prompts/<name>`.

**New prompts:** a reusable one goes in `perma/`; a one-off goes in the root and deletes itself when consumed.

**Consumed 2026-09-12:** `STILL_NEEDED_SWEEP.md` completed by Codex fan-out across46 modules. Output: `agent/reports/STILL_NEEDED_SWEEP.md`, verbatim pairs under `agent/reports/still-needed/`, owner ck156 and held after-v9 surface/outbox routing. Brief preserved at `git show 2be1402:docs/agent/prompts/STILL_NEEDED_SWEEP.md`. No module/public change.
