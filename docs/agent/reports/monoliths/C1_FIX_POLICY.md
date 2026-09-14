> ⛔ **SUBAGENT OUTPUT — THIS IS A CLAIM, NOT A FINDING.** Produced 2026-09-14 by a read-only
> characterisation agent under checklist **181**. Only the items graded **CONFIRMED** in
> [`../C1_MONOLITHS.md`](../C1_MONOLITHS.md) were re-derived by the orchestrator seat; everything
> else here is unverified. ⚠️ At least one claim in this set was materially imprecise — read the
> adjudication first, and never quote a number from this file without re-deriving it.

# C1 — Characterisation of `docs/agent/FIX_POLICY.md` (50,756 B)

Read in full (785 lines). All commands below were run read-only against the working tree at HEAD (`b162e37`... current uncommitted status only touches `SMRTK_FULL_SITTING.md`, unrelated).

## 1. Section inventory (sorted by size, descending)

| Heading | Lines | Bytes | % of doc | What it's for |
|---|---|---|---|---|
| ### 3a. SAVE SAFETY... | 356–518 | 10,781 | 21.2% | Design ethos + 3-tier remedy ordering for what enters a save; orphan gate; exposure-count history |
| ## 1. Choose the least invasive technique | 6–109 | 6,668 | 13.1% | Ranked technique menu (data patch → wrap → full replace) + wrapper/global-replace mechanics |
| ## 2. Fail safe, never loud | 110–202 | 6,730 | 13.3% | Register/pcall contract, self-check rules (F64/F107/F87/F110), veto handling, inert-for-foreign-object |
| ## 4. Only fix proven, reachable, UNINTENDED defects | 519–580 | 4,085 | 8.0% | Intent test, reachability tiers R1–R4/U, shipping rules per tier |
| ## 2b. Pinned-defect manifest | 264–336 | 4,433 | 8.7% | SRC/DEFECT header-line grammar, `bodycheck.py` contract, trust-table pointer |
| ## 5. Optional modules (`Opt_*`) | 648–705 | 3,715 | 7.3% | N/A-tombstone notice + install-pattern rules for the (relocated) opt-in machinery |
| ## 2a. Branch guards | 203–263 | 3,772 | 7.4% | "probe IS the guard, never a version check" — LuaRevision-as-label clarifications |
| ### The test is WHO BENEFITS (under 4a) | 588–647 | 3,406 | 6.7% | Who-benefits test, barred/not-barred lists, override procedure |
| ## 6. Engine semantics | 706–736 | 2,132 | 4.2% | error()/assert() non-unwind, T()/localisation rules, ModLog `%` escaping |
| ## 7. Console platforms | 737–762 | 1,766 | 3.5% | Console-invisibility of veto/logs, achievement-block platform list |
| ## 8. Release hygiene | 763–785 | 1,493 | 2.9% | File-per-fix, load-order deference, pre-release checklist |
| ## 3. Savegame discipline (top, before 3a) | 337–355 | 1,181 | 2.3% | No new persisted classes, cleanup sweeps, uninstall paving |
| ## 4a. SCOPE heading only | 581–587 | 410 | 0.8% | Heading + "HARD RULE" tag for the who-benefits test below it |
| # title/intro | 1–5 | 184 | 0.4% | One-line mission statement |

Notes: §3a alone is over a fifth of the file. §4a's heading (410 B) plus its "who benefits" subsection (3,406 B) together = 3,816 B, comparable to §2a or §5. The three biggest sections (§3a, §2, §1) are 60% of the document between them.

## 2. Tombstones

**Definition used:** a rule/example whose *referent* (file, module, decision state) is now gone or changed, verified by one command.

| # | Quote | Referent | Command proving it's gone/changed | Verdict |
|---|---|---|---|---|
| T1 | §5 heading (line 650–658): *"⛔ N/A IN THIS PACK SINCE 2026-08-12 — and kept, not deleted. All eight `Opt_` modules and the whole Mod Options surface moved to the standalone Community Opt-In Pack"* | The `Opt_*` modules themselves | `ls Code/ \| grep -i "^Opt_"` → empty in this repo; `ls "C:\Dev\SMR-OptInPack\Code"` → populated | **Not a hidden tombstone — self-declared and accurate.** Verified the stated reasons still hold: `grep -n "optional\|OptionEnabled\|ApplyModOptions" Code/00_Core.lua` → 10+ live hits, so "machinery stays" claim is true today. This is a *correctly maintained* tombstone, i.e. the doc is doing its job here. |
| T2 | §4 amendment header (line 528–531): *"that guard was stripped from `Fix_TrainMinors` on 2026-08-01 (`agent/bugs/F49.md`; A/B code-gate leg ran clear), so the rule and the shipped code now agree."* | `Code/Fix_TrainMinors.lua` | `git ls-files Code/ \| grep -i TrainMinors` → no output. `docs/agent/bugs/F49.md:279`: *"⇒ **Fix_TrainMinors** — removed from the pack in hotfix 2 (re-verification row R-34; owner decision 98, ruled 2026-09-08: delete rather than gate...)"* | **Genuine tombstone.** The file this passage narrates as "guard stripped, kept" was **entirely deleted** a month later (2026-09-08), a fact FIX_POLICY does not know about. The passage is now misleading: a reader following the citation finds a module that no longer exists. |
| T3 | Same header, closing sentence (line 535–536): *"the decision is routed and owed, not assumed either way"* (re: F29/F57(a) needing an explicit owner decision on R3+§1.5) | The open decision | `grep -n "^status" docs/agent/bugs/F29.md docs/agent/bugs/F57.md` → both `"fixed*"` | **Stale claim, not quite a tombstone** — the decision this text says is "owed" has since been made and executed. Overlaps with finding #3 (dated session record) below. |
| T4 | §4a example (line 642–646): *"The pack shipped `Fix_ReplaceTechCount` (F28) against a function with zero callers in all of Src... It was not an accident: the entry said 'No vanilla caller' in its second line and it shipped anyway."* | `Code/Fix_ReplaceTechCount.lua` | `git ls-files \| grep -i Fix_ReplaceTechCount` → no output. `docs/agent/bugs/F28.md:14`: *status "wontfix" ... "Code/Fix_ReplaceTechCount.lua and its TestKit probe both DELETED"* | **Not a tombstone rule** — this is a historical illustration cited as *evidence for a still-binding rule* (§4a scope bar), and the doc itself already frames F28 as retired ("An existing shipped fix is NOT precedent — one (F28) already violated this rule and was retired under it," line 639-640). The example correctly presents itself as dead code. No fix needed. |
| T5 | §2b regex worked example (line 310–316): F46 phrasing example — checked live, not flagged. `docs/agent/bugs/F46.md` not checked for status; example is illustrative of a *method*, not a claim the code still exists this way. Lower priority — **not pursued**, boundary stated. |

**Boundary on this section:** I did not check every dated citation in the doc (there are ~30+ bug-id references). I ran the check on every citation that is used to justify a *currently binding* rule via a *specific still-existing artifact claim* (T2, T4) plus the one the task flagged as highest-value (self-declared tombstone, T1). Citations used purely as "see also" (e.g. F111/F112/F-1..F-5 at line 326, which I verified are a **different ID namespace** — VANILLA_FIX_QA re-verification rows, not `agent/bugs/` entries, confirmed via `grep -rn "F-1\b" docs/agent/` showing `HOTFIX_1_AUDIT.md`/`GAME_1_1_0_AUDIT.md` usage) were not exhaustively re-verified.

## 3. Dated session records

Passages narrating a specific incident/day rather than stating durable policy. The doc's house style is "rule + worked example," which blurs this — I'm flagging the ones that lean hardest toward incident-narration:

| Lines | Bytes | Content | Judgment |
|---|---|---|---|
| 519–536 | 1,247 | §4 amendment header: narrates the 2026-08-01 adoption, the F49(a)/R4-rider contradiction that "blocked" it, and the now-stale "routed and owed" claim (see T3) | **Strongest candidate for archival.** This is pure changelog prose (what blocked adoption, what got fixed, on what date) wrapping a rule that is fully stated afterward without it. The rule survives intact if this block moves to `SESSION_LOG.md` and is replaced by one sentence: "Adopted 2026-08-01, superseding the old 'only fix proven defects' line." |
| 33–46 | 1,086 | §1.4 CALLERS rule: full F59 incident narrative (`Fix_FreedHousingNotice`, `SetResidence`'s 11 callers, the two callers that broke) | Borderline — the incident IS the proof the rule is non-obvious, but the rule itself ("list every caller... does this caller keep using the state my hook just published?") is stated in 2 sentences; the rest is case history. |
| 48–62 | 1,238 | §1.4 game-time-thread-persistence rule: cites `cthreads.lua:481-524`, `Fix_FreedHousingNotice`, `Fix_ExtenderFlapChurn:97` as precedent sites | Same shape — mechanism explanation (durable) mixed with "which modules currently do this" (session-report flavor). |
| 123–147 | 1,855 | §2 F107 rule: full incident (`Fix_LandscapeCostRefresh`, nil `prev`, `find_declaring_ancestor`, the allowlist-tool mechanics, "checklist 74(a), 2026-08-24") | Longest of these. The binding rule is one sentence (line 123–125); everything else is the F107 post-mortem plus tool-usage instructions (which arguably belong near the tool, not here). |
| 148–169 | 1,646 | §2 F87 rule: cold-boot-vs-reload incident, `ModsReloadItems`/`ReloadLua`/`Mod.lua:2145` citation, "The F87 sweep found three sites" | Same shape. |
| 718–733 | 1,219 | §6 T()/localisation rule: F98/F25 incident ("`Fix_TechDescriptionBuilding` did exactly this and has never changed anything"), dated 2026-08-02, plus a forward-looking owner decision note | Same shape; rule occupies ~2 sentences, rest is the F25/F98 story. |
| 748–754 | 538 | §7 wording correction: *"this line said 'not on Steam/PC' until 2026-08-16 and that wording would have misled a Game Pass player"* | Small, clearly a dated correction note rather than policy — cheapest one to trim. |

**Total across these 7 blocks: ~7,829 bytes (~15% of the file).** None of them are wrong, but all of them read as `SESSION_LOG.md` material wrapped around a one- or two-sentence rule. I did not attempt to separate "rule sentence" from "incident prose" byte-for-byte inside each block — that would need editorial judgment, which is outside a read-only characterisation.

## 4. Superseded-in-place

Only one clear instance — a literal struck-through (`~~...~~`) passage with a correction still sitting next to it:

**Location:** lines 503–517 (1,094 B total span).

**Dead half (struck, still present, 397 bytes):**
> `(~~**13** after two same-day membership corrections — `DroneUnreachableForever` in, `TrainCargoDumping` out, compliant `CaveInsNoDisasters` counted; **re-derived 2026-08-01 by the five-shape Phase-1 enumeration, which confirmed the 13 and classified one additional inert route-(c) preset-field site** — `Fix_LastTransmissionStorage`'s `Condition.eval`, disclosed-no-build, adjudication §4.4~~`

**Correction (live, immediately following):**
> `⛔ **SUPERSEDED 2026-08-13 — the authoritative figure is `agent/reports/D13_EXPOSED_SET.md`: 27 sites over BOTH shipped trees = 12 capturable-code + 15 persisted-data. The "13+1" was an open lower bound over capturable CODE in the fix pack only; the like-for-like number is 12, and §4.1 there reconciles the difference row by row in both directions...**`

397 of the 1,094 bytes here are dead weight kept for audit-trail reasons (visible strikethrough, not deleted) — this is a **deliberate** superseded-in-place (the strikethrough IS the disclosure mechanism this project uses elsewhere), not an oversight. Only one instance found; I searched for the pattern specifically:

```
grep -n '~~' docs/agent/FIX_POLICY.md   → only this one strikethrough pair in the whole file
```

No other ⛔ CORRECTED/SUPERSEDED/REVERTED markers in the doc leave their original text intact elsewhere — the other ⛔-marked passages (F59, F87, F107, F110, branch-guard clarifications) are all *additions* of new binding text, not corrections superseding an older sentence that's still visible. (5b90e7e, checked via `git show`, shows §3a's *actual* rewrite in 2026-08-01 deleted the old text outright rather than striking it — so that section's history is clean, not superseded-in-place.)

## 5. Rules inventory

Every binding instruction (an agent's behaviour is bound by it), with line and a 10-word gloss. Duplicates against WORKFLOW.md/CLAUDE.md flagged inline (full quotes in §6 below).

| Line | Rule (10-word gloss) |
|---|---|
| 8–32 | Technique ranking: data-patch > additive-handler > registry-surgery > wrap > replace |
| 21–31 | Wrapper: capture `orig` at apply time, always call it, pass through returns |
| 33–46 | Post-hook must enumerate wrapped function's CALLERS, not its callees |
| 55–58 | Thread body: zero upvalues; orphan gate is first statement after yield |
| 66–73 | Global replace: plain `_G` assignment, never `rawset`; verify with `rawget` |
| 74–91 | Prefer wrapper over body-copy even when both work (degrades gracefully) |
| 95–101 | Full replacement: byte-identical copy, `-- FIX:` comments, header names source+version |
| 102–108 | "Reconstruction" replacements must say so; can't be byte-diffed later |
| 114 | `apply()` runs under `pcall`; one fix's error deactivates only itself |
| 115–117 | Sanity-check target before patching; return reason string, never throw |
| 118–122 | Self-check the DECLARING class, not an inherited method on a subclass |
| 123–147 | Every wrapped/captured `(class,method)` pair must appear in module's `Require` block |
| 148–169 | `apply()` may not assume cold boot; no class/preset construction at apply time |
| 162–167 | `OnMsg.DataLoaded` insufficient trigger; use `DataPatch`/`OnDataReady` instead |
| 170–176 | Wrapper must be inert for a foreign object before touching it |
| 177 | Respect `SMRFixPack_Disabled["<id>"]` veto |
| 178–183 | Every `OnMsg` handler must re-check both registry status AND the veto |
| 184–191 | Track `data_loaded` flag; only latch `inactive` after real `DataLoaded` fires |
| 192–201 | Never put a per-game runtime global (`Cities` etc.) in a `Require` block |
| 210–219 | Unknown probe answer DECLINES; exception needs owner's explicit word, never inferred |
| 221–228 | `LuaRevision` may only be an observation label, never a branch guard |
| 238–246 | Do not build a game-version detector (two independent reasons given) |
| 248–262 | The per-module `probe` in `Require` IS the branch guard mechanism |
| 269–275 | A module that can't state its corrected defect should not ship |
| 277–306 | SRC/DEFECT header-line grammar: path, selector, hashing rule, `SRC: none` form |
| 307–316 | State the DEFECT, never incidental phrasing (regex must survive refactors) |
| 318–322 | An absence-defect can't be stated directly; note the known limitation |
| 324–328 | `bodycheck.py` green ≠ clearance; `DEFECT-GONE` is a REMOVE **candidate**, not a verdict — ⚠️ **near-duplicate of WORKFLOW.md.** FIX_POLICY: *"A `DEFECT-GONE` is a REMOVE **candidate**, never a verdict: read the replacement body before retiring anything."* WORKFLOW.md line ~201 (table row): *"`DEFECT-GONE` \| the stated expression is no longer in the target \| ⛔ a REMOVE **candidate, never a verdict** — trace the REPLACEMENT body and name residuals first."* Same clause almost verbatim in both. |
| 339–341 | New persisted classes/GameVars only if unavoidable; name `SMRFixPack_*` |
| 342–344 | Corrupt-state cleanup is a separate, marked one-shot `LoadGame` sweep |
| 345 | Never break saves for players who later disable the mod |
| 452–461 | Every thread body opens with orphan gate `if not SMRFixPack then return end` |
| 463–498 | Remedy order is binding: Layer 3 (patch input) → 2 (no post-yield code) → 1 (teardown/rebuild) |
| 494–498 | Re-arm teardown from a persisted deadline, never restart blind (autosave trap) |
| 541–546 | Intent must cite a hard tell before any fix is written (no tell = hypothesis) |
| 554–559 | Enumerate every call site; assign a reachability tier (R1–R4/U) |
| 560–564 | Every tier's claim needs stated evidence; a sub-item's proof doesn't cover siblings |
| 565–569 | R1/R2 ship; R3 needs §1.1–1.4 only (full-replace R3 needs owner decision); R4 never ships; U needs a queued observation |
| 570–573 | `tested` only counts if reached by playing; console/debug-only reach is R4 evidence |
| 574–576 | Re-check `git log` between drafting and recording a verdict |
| 577–579 | No balance/opinion changes; prefer the sibling-code-proven reading |
| 604–611 | Never fix another mod's bug or a defect reachable only from mod code (R4, barred) |
| 617–623 | DO fix vanilla code merely benign-by-data (R3, not barred) |
| 636–640 | Exceptions to scope bar need an explicit, case-specific owner yes — never inferred |
| 673–679 | Opt-in hooks install at file/classdef scope, gated per call by `IsActive(id)` |
| 685–689 | `on_activate`/`on_deactivate` only for non-call-path state; must be idempotent |
| 694–704 | "Off" says nothing about the save — hooks stay installed and capturable |
| 708–710 | `error()`/`assert()` report-and-continue; never use for control flow |
| 712–717 | Copied bodies keep `T()` byte-identical; new strings use `Untranslated()` |
| 718–725 | Never re-use a shipped translation id to change text (silent no-op in retail) |
| 726–729 | To append to localized text, concatenate `shipped_T .. Untranslated(...)` |
| 734–735 | Every `ModLog` call must escape `%` before formatting |
| 739–743 | Fail-safe behaviour must never depend on the player seeing a message (console) |
| 744–745 | Anything a console player must steer goes through Mod Options or nowhere |
| 749–750 | Say "Steam and other PC versions," never bare "PC" (MS Store is PC too) |
| 765–766 | One fix per `Code/Fix_*.lua`; filename matches Register id; listed in `metadata.lua` |
| 767 | `00_Core.lua` must load first |
| 775–780 | Never build behaviour on load-order deference; it's structural, not a lever |
| 781–784 | Pre-release: verify vs shipping fpk, test in-game, update statuses, credit prior art |

**Other duplicate found (paraphrase, not verbatim):** FIX_POLICY §2b's class-b/c/d/e gloss (lines 324–328: *"It sees a changed body (class b), a vanished defect (class d) and a vanished target (class e). It does not see semantics moving under a wrapper (class c...)"*) restates, in miniature, WORKFLOW.md's full trust table (WORKFLOW.md lines 210–228, headed *"⭐ **This is the canonical copy.** `FIX_POLICY` §2b points here; the tool headers carry the machine half. Do not copy it to a fourth place."*). FIX_POLICY does point at WORKFLOW as canonical (line 330–333: *"The full trust table... lives in `WORKFLOW.md`... this paragraph is the authoring-time warning only"*) — so this is a **declared, intentional** summary-with-pointer, not an accidental fork. Flagging it because the summary itself (class b/c/d/e + DEFECT-GONE wording) is close enough to count as *content* duplication even though the doc's own text disclaims it.

## 6. Duplication against WORKFLOW.md and CLAUDE.md

Checked against both in full (not skimmed):

- **DEFECT-GONE / REMOVE-candidate clause** — near-verbatim, see §5 above. Both sides quoted there.
- **bodycheck instrument classes (b/c/d/e)** — paraphrased duplication, see §5 above. FIX_POLICY explicitly disclaims itself as non-canonical for this.
- **"Trust by source" three-class framework** — CLAUDE.md states it in full (*"(1) The owner's instruction is authority... (2) Tool output... derived fact... (3) Everything else... is a claim."*). WORKFLOW.md deliberately does **not** restate it: *"The three classes are stated once, in `CLAUDE.md`... R-A is how class 2 is discharged: one command, not a re-read."* (WORKFLOW.md line 916-918). **FIX_POLICY does not mention this framework at all** — no duplication here, and worth noting as a model of what FIX_POLICY's other pointers (§2b) are trying to do.
- **agent/bugs/ entry + reachability-tier citation** — WORKFLOW.md line 146: *"Every fix links to an `agent/bugs/` entry with file:line evidence (FIX_POLICY §4)."* This is a one-line pointer to FIX_POLICY's §4, not a restatement — no duplication.
- **fpk verification / release gate** — WORKFLOW.md has its own full "fpk verification — RELEASE GATE" section (lines 157–173) with the current parity numbers (1.1.0.403908, 0 divergent). FIX_POLICY §1.5 only says *"the fpk extraction diff is a release gate, WORKFLOW.md"* (line 100–101) — a pointer, not a copy. No duplication.
- **§3a "D13"/save-rescue** — WORKFLOW.md line 857 cites `FIX_POLICY.md §3a` as one of three pointers for a prompt-authoring checklist; not a restatement.
- **CLAUDE.md folder-contract / doccheck rules** — not duplicated in FIX_POLICY at all (different subject matter; CLAUDE.md is repo-hygiene, FIX_POLICY is code-authoring).

No other cross-doc duplication found in a full read of both siblings.

## 7. Growth history

`git log --format='%h %ci %s' -- docs/agent/FIX_POLICY.md` — 22 commits, 2026-08-01 through 2026-09-12. Sizes measured via `git show <hash>:docs/agent/FIX_POLICY.md | wc -c` at every commit:

| Commit | Date | Size (B) | Δ (B) | What it added |
|---|---|---|---|---|
| 9916679 | 08-01 | 24,334 | — | baseline (doc-reorg landing point) |
| e8eb1bc | 08-01 | 27,960 | +3,626 | §4 amendment (reachability-tier rewrite) |
| 5b90e7e | 08-01 | 27,766 | −194 | **rewrote §3a's opening in place** (old "empty `_ENV`" framing deleted outright, not struck — see §4 above) |
| 7efa2d0 | 08-01 | 28,012 | +246 | re-derived exposure count (13, five-shape enumeration) |
| ce77c51 | 08-01 | 30,953 | +2,941 | the three-tier ethos + per-site release gate |
| 7552ade | 08-01 | 31,434 | +481 | D13 exposed-set derivation note |
| a5d4b89 | 08-01 | 32,279 | +845 | "no persisted state" claim struck; toggle-vs-save clarified |
| fa3bdad | 08-02 | 33,550 | +1,271 | D10/localisation parking note |
| 46f60db | 08-03 | 33,589 | +39 | translation-note path sweep (tiny) |
| fc1858a | 08-03 | 34,136 | +547 | wrapper-inspects-first behaviour-change rule |
| 4026ea2 | 08-03 | 34,252 | +116 | QA-session commit landing |
| c29a19e | 08-12 | 34,921 | +669 | **§5 Opt_* tombstone marker added** (the split to SMR-OptInPack) |
| 689a396 | 08-13 | 35,518 | +597 | exposure-list superseded-in-place strikethrough (§4 above) added here |
| d202bcf | 08-16 | 37,564 | +2,046 | load-order deference ruling (§8) |
| 7667b65 | 08-24 | 39,133 | +1,569 | F107 Require-block rule, full incident |
| f6eba26 | 08-24 | 39,419 | +286 | F107 follow-up (delegation fix landed) |
| 409f552 | 08-30 | 40,225 | +806 | F110 rule (no per-game global in Require) |
| **6db7457** | **09-08** | **46,542** | **+6,317** | **largest single jump: all of §2a (branch guards) + §2b (pinned-defect manifest) added whole** |
| b3570e0 | 09-11 | 47,629 | +1,087 | F59 CALLERS-not-callees rule |
| 9c333d1 | 09-11 | 48,868 | +1,239 | F59 game-time-thread-persistence rule |
| cc3edf2 | 09-12 | 49,271 | +403 | vanilla-diff-instrument pointer to WORKFLOW.md |
| b162e37 | 09-12 | 50,756 | +1,485 | ck166 branch-guard hybrid-exception ruling (§2a clarifications) |

**Was anything ever removed?** Yes, once cleanly: commit `5b90e7e` (08-01) deleted ~700 bytes of the old §3a opening outright (verified via `git show 5b90e7e -- docs/agent/FIX_POLICY.md`, diff quoted in my working notes — old "empty `_ENV`" text removed, replaced by the current mechanism paragraph). Every other commit is additive; the file has never had a net-negative month. The single biggest addition (6db7457, +6,317 B, 12.4% of the current file in one commit) is sections §2a+§2b — both still fully live and cited elsewhere (WORKFLOW.md, multiple bug entries), not padding.

## 8. Verdict

**If 40% (≈20,300 B) had to go without losing a binding rule, my candidates, in order of confidence:**

1. **The 7 dated-session-record blocks in §3 (≈7,829 B, high confidence).** Each wraps a 1–3 sentence rule in a paragraph of incident narrative (F59, F87, F107, F98/F25, the §4 amendment's own adoption story, the Steam/PC wording fix). Move the narrative to `SESSION_LOG.md`/leave a one-line "why" citation, keep the imperative sentence. This is the single biggest lossless cut I found and matches the task's own framing of what a policy doc should not contain.
2. **The struck-through 397 B in §3a (line 505–510, low value, low confidence it should go).** It's *deliberately* kept as an audit trail for a corrected figure. Cutting it loses no rule, but the project's own practice elsewhere (e.g. F25/F92 entries) is to keep strikethroughs as provenance — I'm unsure whether the orchestrator wants that norm broken here just for size.
3. **§3a's exposure-count history entirely (lines 500–518, ~1,200 B beyond item 2).** The number itself ("27 sites... `D13_EXPOSED_SET.md` §7") is fully re-derivable from the cited report and is *already* labelled "not to be quoted from these docs" one paragraph earlier (line 417-423: *"the table is built against D13's OWN derivation... not against any count recorded in these docs"*). The doc arguably no longer needs to carry the count at all, only the pointer.
4. **Tighten T2 (Fix_TrainMinors) before anything else — not a size cut, a correctness fix.** This is the one place I'd flag as needing an edit regardless of size pressure: the passage currently misleads a reader into thinking `Fix_TrainMinors` still exists.

**Argument against cutting further:** the doc's habit of pairing every non-obvious rule with the incident that forced it (F59, F107, F87, F110, the branch-guard hybrid) is plausibly *why the rules stick* — this project's own memory notes elsewhere emphasize "challenge the cause before filing" and treating claims skeptically; a rule with its receipt attached is harder to silently violate than a bare imperative. Cutting all narrative risks turning binding, well-earned rules back into arguable opinions. I'm **unsure** where the orchestrator wants that line drawn — that judgment call is squarely the adjudication this report is feeding, not something I should resolve unilaterally.

**What I did NOT verify (explicit boundary):** every dated citation to an `agent/bugs/` entry in the doc (~30+) was not individually re-checked for "does the referenced fix/module still exist" — only the ones load-bearing for a currently-binding rule (T2, T4) or self-flagged (T1) were run down. A full sweep of all citations would be the natural next pass if the orchestrator wants exhaustive tombstone coverage rather than the highest-value ones.
