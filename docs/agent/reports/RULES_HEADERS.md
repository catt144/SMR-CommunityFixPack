# RULES_HEADERS — partial inventory and stop report

SOURCE / INFERRED audit, 2026-09-14. **PARTIAL; not a migration-ready owner-gate proposal.** The commissioned task's section 6 says to stop on conflicting rules. X1 below was encountered during the main-doc read. No rule, header, kernel line, checker or prompt lifecycle has changed.

The owner permitted reading the initially dirty working copies. Those edits subsequently landed in peer commits `f78d7a8` and `72ed20e`; this report uses the now-clean committed snapshots below. Initial preflight was at `25acafe`, rather than the task's older authored anchor. SOURCE: executed agent Codex (transcript identity); the exposed transcript does not identify a precise serving-model identifier. None is inferred. No subagents were used.


MEASURED continuation note: packaging HEAD 2bbdbd315a74a1a5a7868fbbd883fde2701d5653. Only STATE moved after the source anchor (peer commit 2bbdbd3). Source excerpts and line numbers remain at 72ed20e; current STATE arithmetic is separately recorded below.

## Progress

- [x] Anchor: pull, log, status, doccheck GREEN; owner allowed read-only analysis of the dirty working copies.

- [ ] Complete inventory CLAUDE.md — read in full; selected rules recorded, completeness not certified.
- [ ] Complete inventory docs/README.md — read in full; selected rules recorded, completeness not certified.
- [ ] Complete inventory docs/agent/STATE.md — read in full; selected rules recorded, completeness not certified.
- [ ] Complete inventory docs/PLAYTEST_CHECKLIST.md — preamble read only, before decisions H2; selected editing rules recorded.
- [ ] Complete inventory docs/agent/WORKFLOW.md — sampled inventory; exact source ranges in appendix.
- [ ] Complete inventory docs/agent/FIX_POLICY.md.
- [ ] Complete inventory docs/PLAYTEST_HELP.md.
- [ ] Complete inventory docs/UPLOAD_WORKFLOW.md.
- [ ] Complete inventory docs/agent/prompts/perma/CO_RUNS.md.
- [ ] Complete inventory docs/agent/prompts/perma/COMBINED_SITTING.md.
- [ ] Complete inventory docs/agent/prompts/perma/DISPATCH.md.
- [ ] Complete inventory docs/agent/prompts/perma/DRONE_PROJECT_PROMPT.md.
- [ ] Complete inventory docs/agent/prompts/perma/GENERAL_USE_PROMPT.md.
- [ ] Complete inventory docs/agent/prompts/perma/HANDOFF_ORCHESTRATOR.md.
- [ ] Complete inventory docs/agent/prompts/perma/LINUX_DISPATCH.md.
- [ ] Complete inventory docs/agent/prompts/perma/POST_UPLOAD_CLOSE.md.
- [ ] Complete inventory docs/agent/prompts/perma/PUBLIC_SURFACE_SWEEP.md.
- [ ] Complete inventory docs/agent/prompts/perma/RELEASE.md.
- [ ] Complete inventory docs/agent/prompts/perma/RELEASE_OUTBOX.md.
- [ ] Complete inventory docs/agent/prompts/perma/SITE_AUDIT.md.
- [ ] Complete inventory docs/agent/prompts/perma/SMRTK_SLOTS.md.
- [ ] Complete inventory docs/agent/prompts/perma/STATE_EVICTION.md.
- [x] Classify recorded members and reconcile the partial counts against their IDs.
- [ ] Complete redundancy pass — R1–R5 established within sampled boundary.
- [ ] Complete dead-rule pass — no confirmed dead occurrence; X1 unresolved.
- [ ] Complete header spec and per-doc eligibility list — provisional below.
- [x] Package and verify this stop report: 80 member IDs unique, class/doc tables reconciled, every excerpt byte-exact in the anchored git blob; doccheck GREEN.
- [ ] **In progress (blocked):** owner direction to continue analysis with X1 unresolved.
- [ ] **Blocked:** owner migration gate; remaining inventory and binding decisions pending.
- [ ] Migrate CLAUDE.md — conditional commit-and-verify unit; blocked, eligibility not asserted.
- [ ] Migrate docs/README.md — conditional commit-and-verify unit; blocked, eligibility not asserted.
- [ ] Migrate docs/agent/STATE.md — conditional commit-and-verify unit; blocked, eligibility not asserted.
- [ ] Migrate docs/PLAYTEST_CHECKLIST.md — conditional commit-and-verify unit; blocked, eligibility not asserted.
- [ ] Migrate docs/agent/WORKFLOW.md — conditional commit-and-verify unit; blocked, eligibility not asserted.
- [ ] Migrate docs/agent/FIX_POLICY.md — conditional commit-and-verify unit; blocked, eligibility not asserted.
- [ ] Migrate docs/PLAYTEST_HELP.md — conditional commit-and-verify unit; blocked, eligibility not asserted.
- [ ] Migrate docs/UPLOAD_WORKFLOW.md — conditional commit-and-verify unit; blocked, eligibility not asserted.
- [ ] Migrate docs/agent/prompts/perma/CO_RUNS.md — conditional commit-and-verify unit; blocked, eligibility not asserted.
- [ ] Migrate docs/agent/prompts/perma/COMBINED_SITTING.md — conditional commit-and-verify unit; blocked, eligibility not asserted.
- [ ] Migrate docs/agent/prompts/perma/DISPATCH.md — conditional commit-and-verify unit; blocked, eligibility not asserted.
- [ ] Migrate docs/agent/prompts/perma/DRONE_PROJECT_PROMPT.md — conditional commit-and-verify unit; blocked, eligibility not asserted.
- [ ] Migrate docs/agent/prompts/perma/GENERAL_USE_PROMPT.md — conditional commit-and-verify unit; blocked, eligibility not asserted.
- [ ] Migrate docs/agent/prompts/perma/HANDOFF_ORCHESTRATOR.md — conditional commit-and-verify unit; blocked, eligibility not asserted.
- [ ] Migrate docs/agent/prompts/perma/LINUX_DISPATCH.md — conditional commit-and-verify unit; blocked, eligibility not asserted.
- [ ] Migrate docs/agent/prompts/perma/POST_UPLOAD_CLOSE.md — conditional commit-and-verify unit; blocked, eligibility not asserted.
- [ ] Migrate docs/agent/prompts/perma/PUBLIC_SURFACE_SWEEP.md — conditional commit-and-verify unit; blocked, eligibility not asserted.
- [ ] Migrate docs/agent/prompts/perma/RELEASE.md — conditional commit-and-verify unit; blocked, eligibility not asserted.
- [ ] Migrate docs/agent/prompts/perma/RELEASE_OUTBOX.md — conditional commit-and-verify unit; blocked, eligibility not asserted.
- [ ] Migrate docs/agent/prompts/perma/SITE_AUDIT.md — conditional commit-and-verify unit; blocked, eligibility not asserted.
- [ ] Migrate docs/agent/prompts/perma/SMRTK_SLOTS.md — conditional commit-and-verify unit; blocked, eligibility not asserted.
- [ ] Migrate docs/agent/prompts/perma/STATE_EVICTION.md — conditional commit-and-verify unit; blocked, eligibility not asserted.
- [ ] Land single new kernel line — blocked.
- [ ] Implement RULES HEADERS checker, watch broken-copy failures and restore by hash — blocked.
- [ ] Final report and per-source-commit verification — blocked.
- [ ] Consume RULES_HEADERS prompt and map row together — blocked until the task is completed.

## X1 — live description editing conflicts with the archive prohibition

SOURCE: WORKFLOW affirmatively requires editing MOD_DESCRIPTION. The map translates that name to its frozen archive file; the entry file forbids archive edits. This report quotes both, resolves neither and proposes no destination wording.

`W12` — `docs/agent/WORKFLOW.md:153-155`

> 4. One commit per fix or tight group; agent/bugs/ updated in the same commit;
>    MOD_DESCRIPTION.md updated in the same commit as the code change it
>    describes.

`W13` — `docs/agent/WORKFLOW.md:640-649`

> - MOD_DESCRIPTION.md: delete the `[DRAFT NOTE]` markers; do NOT promise the
>   ClassicRockets export half; sync the fix list with agent/bugs/ statuses.
>   ⭐ **Add the "judgment calls" section** (owner ADOPTED the relabel proposal
>   2026-08-04: F55, F40, F73(b), F70, F97 presented as design-judgment repairs,
>   not plain bugs) — ⚠️ **its wording is OWED BY THE OWNER** and must be asked
>   for if it does not exist yet; the checklist line tracks it.
>   **Recount the probe number** quoted in the "What we can promise, and what we
>   can't" block — it moves whenever a wave file gains or loses a probe, and a
>   stale number there is a false claim in player-facing text. Authoritative count
>   is in `agent/STATE.md`.

`C04` — `CLAUDE.md:12-13`

> `docs/archive/` is append-only, never edited. **`INDEX.md` in `bugs/`+`facts/`
> is GENERATED — edit the entry or fact file, never the index** (line-1 banner).

`docs/README.md:33-34` identifies the frozen home:

>   archive/                spent. SESSION_LOG.md, PLAYTEST_ARCHIVE.md,
>                           MOD_DESCRIPTION.md (frozen), retired prompts

`docs/README.md:128-129` translates the live path:

> `MOD_DESCRIPTION.md` and `PLAYTEST_ARCHIVE.md` moved from `docs/` to
> `docs/archive/` in the same change.

MEASURED at `72ed20e`: `git ls-files --error-unmatch docs/MOD_DESCRIPTION.md` exited 1, reporting that the old live path is not tracked. `git ls-files -- docs/MOD_DESCRIPTION.md docs/archive/MOD_DESCRIPTION.md` returned only `docs/archive/MOD_DESCRIPTION.md`. This proves the old live path is gone and the frozen successor exists. It does **not** prove the named file is absent everywhere, so this is **not a confirmed dead rule**.

Proposed eventual disposition: retire the stale live-doc edit clauses, or explicitly redirect them to an approved live-description source. A redirect is a rewording that must carry a quoted before/after at the owner gate. Neither is authorised here.

Additional SOURCE flag: CLAUDE.md:8–11 omits WAITING_ON_YOU.md from its closed root folder list; docs/README.md:20–22 includes it and doccheck accepts it. These are not exact duplicates. An approved header migration must not reinstate the old incomplete list.

## Boundary and counting method

The list is an occurrence inventory, not a count of unique policies or warning glyphs. Each recorded member is an imperative or inseparable same-scope rule cluster. Supporting status/fact prose inside an excerpt is retained for context and does not become an additional rule. The cluster convention matters for C04 (two adjacent generated/archive prohibitions) and C08 (the three-class trust protocol); subdivide these at migration planning before giving them different homes.

CLAUDE, docs/README and STATE were read in full and selected rules recorded. Their inventory completeness is **not certified**. Checklist coverage stops before the first decisions H2 (preamble lines 1–45). Its historical redesign and settled-session narratives are records, not new editing rules. WORKFLOW is sampled only: the appendix gives exact excerpt ranges. FIX_POLICY and PLAYTEST_HELP were partly read; UPLOAD_WORKFLOW was read but not classified. Perma prompts are not inventoried. tools/doccheck.py was read only for the STATE byte-check model and temporary-cap authority.

Pointers and facts are excluded: pack route, observed coverage, unexercised legs, retired-prompt status and branch/save facts are not rules merely because they have warning glyphs. Current holds and reopening conditions do constrain actions. No archive body, chain payload or unrelated one-off was audited. No bug/fact index extension was needed.

Canonical occurrences retain doc-local/task-local/global class; proven restatement occurrences get only redundant. Task procedure specialisations and pointers are not claimed redundant. Proposed homes are analysis, not moved bindings. No unconfirmed referent gets dead classification.

## Counts — computed from recorded members

| class | occurrences |
|---|---:|
| doc-local | 7 |
| task-local | 59 |
| global | 8 |
| redundant | 6 |
| dead | 0 |
| **Total** | **80** |

| doc | doc-local | task-local | global | redundant | dead | total | coverage |
|---|---:|---:|---:|---:|---:|---:|---|
| CLAUDE.md | 0 | 4 | 2 | 3 | 0 | 9 | selected rules; not certified complete |
| docs/README.md | 1 | 19 | 0 | 3 | 0 | 23 | selected rules; not certified complete |
| docs/agent/STATE.md | 4 | 23 | 4 | 0 | 0 | 31 | selected rules; not certified complete |
| docs/PLAYTEST_CHECKLIST.md | 2 | 0 | 0 | 0 | 0 | 2 | preamble only |
| docs/agent/WORKFLOW.md | 0 | 13 | 2 | 0 | 0 | 15 | sampled |
| docs/agent/FIX_POLICY.md | — | — | — | — | — | — | not inventoried |
| docs/PLAYTEST_HELP.md | — | — | — | — | — | — | not inventoried |
| docs/UPLOAD_WORKFLOW.md | — | — | — | — | — | — | not inventoried |
| docs/agent/prompts/perma/CO_RUNS.md | — | — | — | — | — | — | not inventoried |
| docs/agent/prompts/perma/COMBINED_SITTING.md | — | — | — | — | — | — | not inventoried |
| docs/agent/prompts/perma/DISPATCH.md | — | — | — | — | — | — | not inventoried |
| docs/agent/prompts/perma/DRONE_PROJECT_PROMPT.md | — | — | — | — | — | — | not inventoried |
| docs/agent/prompts/perma/GENERAL_USE_PROMPT.md | — | — | — | — | — | — | not inventoried |
| docs/agent/prompts/perma/HANDOFF_ORCHESTRATOR.md | — | — | — | — | — | — | not inventoried |
| docs/agent/prompts/perma/LINUX_DISPATCH.md | — | — | — | — | — | — | not inventoried |
| docs/agent/prompts/perma/POST_UPLOAD_CLOSE.md | — | — | — | — | — | — | not inventoried |
| docs/agent/prompts/perma/PUBLIC_SURFACE_SWEEP.md | — | — | — | — | — | — | not inventoried |
| docs/agent/prompts/perma/RELEASE.md | — | — | — | — | — | — | not inventoried |
| docs/agent/prompts/perma/RELEASE_OUTBOX.md | — | — | — | — | — | — | not inventoried |
| docs/agent/prompts/perma/SITE_AUDIT.md | — | — | — | — | — | — | not inventoried |
| docs/agent/prompts/perma/SMRTK_SLOTS.md | — | — | — | — | — | — | not inventoried |
| docs/agent/prompts/perma/STATE_EVICTION.md | — | — | — | — | — | — | not inventoried |

Dashes mean unknown, not zero. Totals reconcile to this partial list only.

## Redundancy — both instances quoted

### R1: Archive append-only/no-edit duty

Proposed canonical home: `docs/README`. Only the archive imperative is duplicated; C04's index clause is separately scoped.

`M05` — `docs/README.md:39-40`

> `docs/archive/` is append-only history — spent reports, retired prompts, session
> logs, settled decision bodies. A root **`.rgignore`** keeps it out of a *default*

`C04` — `CLAUDE.md:12-13`

> `docs/archive/` is append-only, never edited. **`INDEX.md` in `bugs/`+`facts/`
> is GENERATED — edit the entry or fact file, never the index** (line-1 banner).

`M18` — `docs/README.md:100-100`

> - **Spent** anything → `archive/`, which is append-only and never edited.

### R2: Generated index no-hand-edit duty

Proposed canonical home: `generated indexes' own line-1 banners`. The broader regeneration route stays as a pointer or specialisation; do not delete its extra meaning.

`M09` — `docs/README.md:81-83`

> ⚠️ **`INDEX.md` is generated in both folders and is never hand-edited.** Edit
> the entry or fact file; doccheck regenerates the index and fails on any
> difference. Generated files say so on line 1.

`C04` — `CLAUDE.md:12-13`

> `docs/archive/` is append-only, never edited. **`INDEX.md` in `bugs/`+`facts/`
> is GENERATED — edit the entry or fact file, never the index** (line-1 banner).

### R3: Doccheck before doc commits

Proposed canonical home: `WORKFLOW`. Hook setup appears in both.

`W10` — `docs/agent/WORKFLOW.md:103-104`

> 7. **Run `python tools/doccheck.py` before committing doc changes** — red
>    blocks. One-time setup: `git config core.hooksPath tools/hooks`.

`C05` — `CLAUDE.md:19-20`

> Before committing doc changes run `python tools/doccheck.py`; red blocks. Set up
> once: `git config core.hooksPath tools/hooks`. Generated files (`bugs/INDEX.md`,

### R4: Owner-call mirroring to checklist

Proposed canonical home: `WORKFLOW`. W06's marker, status and regeneration procedure is not duplicated by the shorter copies.

`W06` — `docs/agent/WORKFLOW.md:54-62`

> 5. **Owner-decision mirroring (R10).** Every item needing the owner's call is
>    mirrored into `docs/PLAYTEST_CHECKLIST.md` → "Decisions waiting on you"
>    (one line + pointer), and struck the moment it is decided. **An owner
>    decision recorded only in an entry or a report is not considered asked.**
>    **Changing an item's status ALSO means updating its marker.** Update the
>    checklist's `<!-- ck:N status:... owner:... -->` marker in the same edit,
>    including whether an action is still owed by the owner. Regenerate the
>    owner register after editing its source; for the contained regeneration
>    route, see "Writing in a shared tree" below.

`C07` — `CLAUDE.md:23-25`

> Owner decisions go in
> `docs/PLAYTEST_CHECKLIST.md` → "Decisions waiting on you", never only in agent
> docs.**

`M16` — `docs/README.md:95-96`

> - A **decision the owner must make** → `PLAYTEST_CHECKLIST.md` →
>   "Decisions waiting on you". Never only in an agent doc.

### R5: Read STATE first

Proposed canonical home: `STATE with an entry-file bootstrap pointer`. The entry-file pointer cannot be removed: a rule inside STATE cannot discover itself.

`C02` — `CLAUDE.md:5-6`

> `docs/README.md`. **Mandatory read, every session: `docs/agent/STATE.md`** —
> build state, open gates, active holds.

`M04` — `docs/README.md:26-26`

> READ FIRST.

General R-A volatile-source verification versus the deployed-SHA/pack-prediction API instructions is **not** declared redundant: specific instruments are local specialisations. STATE_EVICTION and other perma copies need actual quoted comparisons before any proposed removal.

## Dead pass

No confirmed dead rule within this partial boundary. X1's live path is gone but its archived successor exists. Missing original paths alone must not justify deletion. The remaining task documents may contain spent processes; they are not classified yet.

## Preliminary header specification — approval pending

Immediately after H1 and its blank separator, before prose, put visible rules between these exact markers:

```markdown
<!-- RULES -->
the verbatim rules governing edits to this document
<!-- /RULES -->
```

The interior is a schema placeholder, not proposed rule wording. Only docs with actual editing constraints qualify. No empty ceremonial block. Preserve source text and wrapping; mandatory bullets or flattening blockquotes could change presentation and require explicit before/after review. An inseparable rule can span lines. Never rewrite text merely to fit.

Proposed cap: **1,536 bytes warning / 2,048 bytes hard**, UTF-8 with CRLF normalised to LF (the STATE checker model), inclusive of markers and final newline. Equality is allowed. Whole-doc/per-line budgets still apply independently. These are approval proposals, not rulings.

Future checker: explicit approved-doc list, exactly one correctly ordered marker pair immediately after H1/blank separator, non-empty payload, warning above 1,536 and RED for missing/malformed/oversized blocks. Falsify using a broken copy, including absence, reverse/duplicate markers and threshold boundaries; restore by hash. Do not mutate shared live docs for the demonstration.

**The structural check cannot establish that an agent read the header.** It cannot prove inventory completeness, continued binding when a task doc is never opened, preserved meaning or absence of contradictions.

## Preliminary eligibility — not an approved migration list

| doc/group | outcome | reason |
|---|---|---|
| STATE | qualifies | Kernel content, parser idioms and generated-count rules constrain its edits. |
| PLAYTEST_CHECKLIST | qualifies | Worklist content and whole-body retirement constrain edits; decisions below preamble remain excluded. |
| docs/README | qualifies | Changing this map must preserve its root allowlist contract. |
| CLAUDE | conditional | Generated AGENTS mirror must be synchronised; any standalone rewrite of the source instruction requires before/after review. |
| WORKFLOW | pending | Much of its content governs authoring/testing/releasing other files; finish inventory before deciding what governs editing this doc. |
| FIX_POLICY | pending | Writing a fix and editing the policy are different actions; inventory unfinished. |
| PLAYTEST_HELP | pending | Separate test-running and snippet-authoring rules from edits to the reference. |
| UPLOAD_WORKFLOW | likely qualifies, unconfirmed | Read step-3 backup synchronisation rule constrains editing its paste blocks; not yet classified. |
| each perma prompt | pending individually | Instructions for doing a task alone do not qualify it for an editing header; none inventoried yet. |
| generated indexes / WAITING_ON_YOU | no handwritten block proposed | Existing generated banners are the precedent; changes require their generator. |
| AGENTS | no independent authoring | A CLAUDE header, if approved, arrives through mirror regeneration. |
| archive / one-offs / chain payloads | no migration | Out of scope. |

Per-doc perma reasons are required at the eventual gate; the pending group above does not satisfy that deliverable.

## STATE bytes — framing-only proposal

MEASURED baseline **12191 bytes**; warning **15,360 temporary**, permanent warning **12,288**, hard **18,432**, per-line **200**. Measured at the source anchor via doccheck STATE + STUBS; ck178 is owner authority for the temporary cap. Only the owner can retire it.

One proposed new Rules-in-force line:

```text
- Read the rules header of any doc you are about to edit.
```

The line is **58 bytes** including LF. Candidate local excerpts S01/S28/S30/S31 total **307 bytes** including LFs; unchanged text inside marker framing is **338 bytes**. Moving text within STATE saves no rule-text bytes. With no removals, net **+89 bytes**, projected STATE **12280 bytes** (temporary warning headroom **3080 bytes**, permanent warning headroom **8 bytes**). Source excerpts retain mixed-line context where applicable; actual source separators and any approved pointer require measuring the eventual diff. This is not a migration patch or an inherited final byte result.

**No offsetting eviction has been established.** This proposal does not satisfy the brief's lose-at-least-as-much-as-you-gain requirement. The temporary cap changes affordability, not permission to remove holds/rules. Complete perma comparisons before claiming a net saving. Do not compress obligations to fit.

## Binding / revert risks

- The editing-header rule does not require opening a task doc an agent is not editing. Code fixes, test launches and portal actions need existing read triggers or approved pointers; a docs-only header must not silently stop them binding.
- A global trust rule cannot become doc-local merely by entering CLAUDE's editing header. Ordinary sessions do not edit CLAUDE; preserve mandatory discovery.
- Keep owner holds, recovery ownership, sweep fences and open obligations reachable from the kernel. They are not spare budget bytes.
- Preserve generated-file routing. An approved CLAUDE change requires its separate announced mirror regeneration.
- Do not delete entire quoted blocks as redundant when their extra scope/conditions are specialised.
- One source doc per approved migration commit; text survival and structural GREEN are independent checks. Avoid full-doc reformatting.
- The prompt and map row remain live through the partial inventory and approval gate; consume both only on eventual completion.
- Checklist 177's marker gate is untouched.

## Derived-fact route / verification

MEASURED preflight: git pull already up to date; log identified `25acafe`; status showed only PLAYTEST_HELP and WORKFLOW dirty. Owner authorised read-only inventory. Later log/status identified committed peer work `f78d7a8`/`72ed20e` and a clean tree.

[RAN 2026-09-14, tool transcript] `python tools/doccheck.py`: GREEN at preflight. STATE + STUBS reported 12,191 / 15,360 TEMPORARY / 18,432 / 200. PROMPT MAP and ENTRY MIRROR passed. Existing unrelated warnings were not changed.

One-command committed-source recheck (then status for working-copy drift):


```powershell
git diff --stat 72ed20e1d815c84904099db8edf42840d5fb2ba0..HEAD -- CLAUDE.md docs/README.md docs/agent/STATE.md docs/PLAYTEST_CHECKLIST.md docs/agent/WORKFLOW.md docs/agent/FIX_POLICY.md docs/PLAYTEST_HELP.md docs/UPLOAD_WORKFLOW.md docs/agent/prompts/perma/
```

An empty committed diff means no reread of those sources; `git status --porcelain` still detects uncommitted changes. Fingerprints of unread perma files establish a continuation anchor, not evidence that their rules were inventoried.

## Source fingerprints

HEAD `72ed20e1d815c84904099db8edf42840d5fb2ba0`.

| file | raw bytes | SHA-256 |
|---|---:|---|
| CLAUDE.md | 2506 | e93decba30b268509726eb48824ad35a76ff501bd96a50dbb4aaa755ac480ea5 |
| docs/README.md | 7586 | 6d83d254a111dceb6cad999936f4b70907fff8eccb8587339f1bdaedeb62db41 |
| docs/agent/STATE.md | 12191 | e822ebffba0f95d864a480e4faa7acf86f1440f9bc22b77b8fe85d8943e943ad |
| docs/PLAYTEST_CHECKLIST.md | 613437 | f29bd2300d02da693cf0001c0a253607d9c7449f329df6317feab79926b8b166 |
| docs/agent/WORKFLOW.md | 59724 | a737b9efbb2c6cb82849bce00ba9babf03554b89eac115f64eb2084a29a1eff0 |
| docs/agent/FIX_POLICY.md | 50756 | 9ead24ce83a147de2eda1c6da7ade3768adb53be0b2a4c13ae795e8380fad0bf |
| docs/PLAYTEST_HELP.md | 62709 | 6c238e134a92896c6bf202a16895da8ad79ccfc4b4882c1bc44bb899e1d5c1c7 |
| docs/UPLOAD_WORKFLOW.md | 30307 | 96beb49c758a0ce50e27a25977283e260c95b6449324be02eacc0a81def64d87 |
| docs/agent/prompts/perma/CO_RUNS.md | 28987 | c9972bedc06c18872a6b99e862d611835eec039d00c2e2351d2e83a2cd54f3cc |
| docs/agent/prompts/perma/COMBINED_SITTING.md | 29429 | d3922cb4b7313bd3eef7a4a204d502e65a3c08386bfbab25961090112ecaab76 |
| docs/agent/prompts/perma/DISPATCH.md | 10500 | 27fc6f782cebcf84f747afcfa8ec961728c6f5ba8b1ed5eb73af8d9565047169 |
| docs/agent/prompts/perma/DRONE_PROJECT_PROMPT.md | 21392 | e4aa278724d264dfbbb523fb221aba72bf141e2be888325795795d2999392cf2 |
| docs/agent/prompts/perma/GENERAL_USE_PROMPT.md | 4227 | bf6ceacf58d96475d47d93f2b162471718dbecee9c13a7c02e4107e9c8e71925 |
| docs/agent/prompts/perma/HANDOFF_ORCHESTRATOR.md | 16251 | 494ebe5e685e17bfa1125b2c38b20831f7cb655ebf5a6ba8cdbc3c2c460c3e3d |
| docs/agent/prompts/perma/LINUX_DISPATCH.md | 10752 | 6004e63d8065c2cd1debe98334e594daec9d41673cb3bbe58a9f1752607eccb0 |
| docs/agent/prompts/perma/POST_UPLOAD_CLOSE.md | 5379 | ba484c6a732cf0884f2140ff4755f9c60477b9b40f2fa9d25264a5d9646f679a |
| docs/agent/prompts/perma/PUBLIC_SURFACE_SWEEP.md | 24879 | 63fbbf05d8686d0f8aeaa8d7bfe7e358927923e9db2753956215fd1d97df9c79 |
| docs/agent/prompts/perma/RELEASE.md | 10013 | 69a3a2c903f5f886dc0c5fec9a0cb19c431e9f01ae454ecdc47b0b14faf1d93f |
| docs/agent/prompts/perma/RELEASE_OUTBOX.md | 14474 | f20fcfbc599138e5d2718d8faa26f2ac5adfa6fc402eaaa6a8e9ed25b78be06c |
| docs/agent/prompts/perma/SITE_AUDIT.md | 9866 | 3c4357cc3f9b5fc9dfe33e7676d29e75d938850a277464ad709f99b3ee3c5f5a |
| docs/agent/prompts/perma/SMRTK_SLOTS.md | 5438 | 42e13a73524a958bb88e242ef5e31cd4f049013e0f2159c61c1ef87fb6dcbe0a |
| docs/agent/prompts/perma/STATE_EVICTION.md | 6504 | 614aa01a1033e5c9b7bf3a59f16fae2a3e15f9e24e86f675d19e80d8e3d9fdd9 |

## Full recorded inventory — attachment within report

The JSON is the full list of the partial inventory. Each member carries exact source text (including source newline escapes), file/lines, one class and proposed home. Counts above are generated from it.

```json
[
  {
    "id": "C01",
    "file": "CLAUDE.md",
    "first_line": 3,
    "last_line": 4,
    "classification": "task-local",
    "proposed_home": "FIX_POLICY",
    "reason": "No game-file modification.",
    "verbatim": "A bug-fix mod: every fix repairs a verified defect in the game's shipped Lua,\npatched at runtime; no game files are modified. Map of the tree:"
  },
  {
    "id": "C02",
    "file": "CLAUDE.md",
    "first_line": 5,
    "last_line": 6,
    "classification": "global",
    "proposed_home": "STATE with entry-file bootstrap pointer",
    "reason": "Mandatory kernel read; preserve bootstrap.",
    "verbatim": "`docs/README.md`. **Mandatory read, every session: `docs/agent/STATE.md`** —\nbuild state, open gates, active holds."
  },
  {
    "id": "C03",
    "file": "CLAUDE.md",
    "first_line": 8,
    "last_line": 11,
    "classification": "task-local",
    "proposed_home": "docs/README",
    "reason": "Folder placement; old root list omits WAITING_ON_YOU. Not an exact duplicate.",
    "verbatim": "**Folder contract** (doccheck enforces it). `docs/` root holds ONLY the six\nhuman files (PLAYTEST_CHECKLIST, PLAYTEST_HELP, UPLOAD_WORKFLOW, FIELD_REPORT_REPLIES,\nFUTURE_IDEAS, README), the BUGS/STATUS stubs, `agent/` and `archive/`. Agent material is `docs/agent/`\n(`bugs/`, `facts/`, `reports/`, `prompts/`, STATE/WORKFLOW/FIX_POLICY);"
  },
  {
    "id": "C04",
    "file": "CLAUDE.md",
    "first_line": 12,
    "last_line": 13,
    "classification": "redundant",
    "proposed_home": "docs/README and generated indexes' banners",
    "reason": "Archive and index editing prohibitions; R1/R2. Two prohibitions form a source cluster here.",
    "verbatim": "`docs/archive/` is append-only, never edited. **`INDEX.md` in `bugs/`+`facts/`\nis GENERATED — edit the entry or fact file, never the index** (line-1 banner)."
  },
  {
    "id": "C05",
    "file": "CLAUDE.md",
    "first_line": 19,
    "last_line": 20,
    "classification": "redundant",
    "proposed_home": "WORKFLOW",
    "reason": "Doccheck before doc commits, with hook setup; R3.",
    "verbatim": "Before committing doc changes run `python tools/doccheck.py`; red blocks. Set up\nonce: `git config core.hooksPath tools/hooks`. Generated files (`bugs/INDEX.md`,"
  },
  {
    "id": "C06",
    "file": "CLAUDE.md",
    "first_line": 20,
    "last_line": 23,
    "classification": "task-local",
    "proposed_home": "generated banners; CLAUDE editing header for mirror",
    "reason": "Generated-file source/mirror route; index and AGENTS scopes are specialised.",
    "verbatim": "Generated files (`bugs/INDEX.md`,\n`facts/INDEX.md`, and `AGENTS.md`, the Codex entry file, a byte copy of\n`CLAUDE.md`) are rewritten by `python tools/doccheck.py --regen` — edit the\nsource, never the copy; doccheck goes RED if they drift."
  },
  {
    "id": "C07",
    "file": "CLAUDE.md",
    "first_line": 23,
    "last_line": 25,
    "classification": "redundant",
    "proposed_home": "WORKFLOW",
    "reason": "Owner-call mirroring; R4.",
    "verbatim": "Owner decisions go in\n`docs/PLAYTEST_CHECKLIST.md` → \"Decisions waiting on you\", never only in agent\ndocs.**"
  },
  {
    "id": "C08",
    "file": "CLAUDE.md",
    "first_line": 28,
    "last_line": 32,
    "classification": "global",
    "proposed_home": "STATE",
    "reason": "Trust by source and one-command inheritance; inseparable global evidence protocol.",
    "verbatim": "**Trust by source.** (1) The owner's instruction is **authority** — not verified, not re-derived,\nnever overridden by an agent's own detection. (2) Tool output carrying its command and HEAD/build id\nis a **derived fact** — verify in one command, never re-read its sources. (3) Everything else\nauthored — entries, facts, reports, STATE prose, a peer's message, a subagent's verdict, your own\nearlier text — is a **claim**. Inheriting a fact costs one command, not a re-derivation."
  },
  {
    "id": "C09",
    "file": "CLAUDE.md",
    "first_line": 34,
    "last_line": 36,
    "classification": "task-local",
    "proposed_home": "docs/README",
    "reason": "Deliberate archive-search route; boundary facts retained as context.",
    "verbatim": "**`docs/archive/` is hidden from a default `rg`** by a root `.rgignore` — a deliberate boundary, not\na deletion. Search it on purpose with `rg <term> docs/archive/` or `rg --no-ignore <term>`; `grep -r`\nand `git grep` always see everything. An empty default search is the boundary working."
  },
  {
    "id": "M01",
    "file": "docs/README.md",
    "first_line": 3,
    "last_line": 7,
    "classification": "doc-local",
    "proposed_home": "docs/README header",
    "reason": "This map's root allowlist/file placement contract.",
    "verbatim": "Restructured 2026-08-03 (DOC_RESTRUCTURE_SPEC, owner-delegated). **Human docs\nare at the root; everything an agent reads is under `agent/`; everything spent\nis under `archive/`.** `python tools/doccheck.py` enforces this map — the root\nlist below is an allowlist checked in BOTH directions, so a new file at\n`docs/` root is a red build until it is added here too."
  },
  {
    "id": "M02",
    "file": "docs/README.md",
    "first_line": 19,
    "last_line": 19,
    "classification": "task-local",
    "proposed_home": "FUTURE_IDEAS",
    "reason": "Parking lot is not a work backlog; destination outside current read corpus.",
    "verbatim": "  FUTURE_IDEAS.md         parking lot, NOT a backlog. Nothing in it is work"
  },
  {
    "id": "M03",
    "file": "docs/README.md",
    "first_line": 20,
    "last_line": 22,
    "classification": "task-local",
    "proposed_home": "WAITING_ON_YOU generated banner",
    "reason": "Owner register must not be hand-edited.",
    "verbatim": "  WAITING_ON_YOU.md       GENERATED owner register — every decision and playtest\n                          leg currently held for the owner, newest first. Never\n                          hand-edit: `python tools/doccheck.py --regen`"
  },
  {
    "id": "M04",
    "file": "docs/README.md",
    "first_line": 26,
    "last_line": 26,
    "classification": "redundant",
    "proposed_home": "STATE with entry-file bootstrap pointer",
    "reason": "Mandatory-read restatement; R5.",
    "verbatim": "READ FIRST."
  },
  {
    "id": "M05",
    "file": "docs/README.md",
    "first_line": 39,
    "last_line": 40,
    "classification": "task-local",
    "proposed_home": "docs/README",
    "reason": "Append-only archive contract; canonical occurrence for R1.",
    "verbatim": "`docs/archive/` is append-only history — spent reports, retired prompts, session\nlogs, settled decision bodies. A root **`.rgignore`** keeps it out of a *default*"
  },
  {
    "id": "M06",
    "file": "docs/README.md",
    "first_line": 54,
    "last_line": 56,
    "classification": "task-local",
    "proposed_home": "docs/README",
    "reason": "Deliberate archive search before concluding a historical record never existed.",
    "verbatim": "everything. If a default search comes back empty on something you are sure this\nproject once knew, that is the boundary working — re-run with one of the two forms\nabove before concluding it was never here. It is not a bug and not a missing file."
  },
  {
    "id": "M07",
    "file": "docs/README.md",
    "first_line": 67,
    "last_line": 69,
    "classification": "task-local",
    "proposed_home": "WORKFLOW",
    "reason": "Re-derive stale prose counts before quoting; map-specific specialisation.",
    "verbatim": "Re-derive from\n`INDEX.md` before quoting them."
  },
  {
    "id": "M08",
    "file": "docs/README.md",
    "first_line": 78,
    "last_line": 79,
    "classification": "task-local",
    "proposed_home": "docs/README",
    "reason": "Carry engine facts across repos when appropriate; conditional, not an automatic copy mandate.",
    "verbatim": "copies **diverge from that date**: a fact learned here should usually be carried\nacross, and one learned there will not appear here by itself."
  },
  {
    "id": "M09",
    "file": "docs/README.md",
    "first_line": 81,
    "last_line": 83,
    "classification": "task-local",
    "proposed_home": "generated indexes' banners and map routing pointer",
    "reason": "Index no-hand-edit route; canonical for R2 in recorded corpus.",
    "verbatim": "⚠️ **`INDEX.md` is generated in both folders and is never hand-edited.** Edit\nthe entry or fact file; doccheck regenerates the index and fails on any\ndifference. Generated files say so on line 1."
  },
  {
    "id": "M10",
    "file": "docs/README.md",
    "first_line": 87,
    "last_line": 87,
    "classification": "task-local",
    "proposed_home": "docs/README",
    "reason": "Defects belong in bug entries.",
    "verbatim": "- A **defect** → a new file in `agent/bugs/`. Never a report, never FUTURE_IDEAS."
  },
  {
    "id": "M11",
    "file": "docs/README.md",
    "first_line": 88,
    "last_line": 88,
    "classification": "task-local",
    "proposed_home": "docs/README",
    "reason": "Dated engine-fact placement.",
    "verbatim": "- An **engine fact** → a new `EF-###.md` in `agent/facts/`, with its date."
  },
  {
    "id": "M12",
    "file": "docs/README.md",
    "first_line": 89,
    "last_line": 90,
    "classification": "task-local",
    "proposed_home": "docs/README",
    "reason": "Binding future-work rules belong in governing docs, not reports.",
    "verbatim": "- A **rule that binds future work** → `agent/WORKFLOW.md` or `agent/FIX_POLICY.md`,\n  not buried in a report."
  },
  {
    "id": "M13",
    "file": "docs/README.md",
    "first_line": 91,
    "last_line": 91,
    "classification": "task-local",
    "proposed_home": "docs/README",
    "reason": "Report/plan/spec/audit placement.",
    "verbatim": "- A **report, plan, spec, audit or survey** → `agent/reports/`."
  },
  {
    "id": "M14",
    "file": "docs/README.md",
    "first_line": 92,
    "last_line": 93,
    "classification": "task-local",
    "proposed_home": "prompts/README",
    "reason": "Prompt placement, consumption and map update; exact comparison with prompt-map home pending.",
    "verbatim": "- A **prompt** → reusable: `agent/prompts/perma/`; one-off: the `agent/prompts/` root, deleted when consumed. Update the\n  map, `agent/prompts/README.md`, either way."
  },
  {
    "id": "M15",
    "file": "docs/README.md",
    "first_line": 94,
    "last_line": 94,
    "classification": "task-local",
    "proposed_home": "docs/README",
    "reason": "Session-leg placement and order.",
    "verbatim": "- A **session leg** → `archive/SESSION_LOG.md` (append-only, newest first)."
  },
  {
    "id": "M16",
    "file": "docs/README.md",
    "first_line": 95,
    "last_line": 96,
    "classification": "redundant",
    "proposed_home": "WORKFLOW",
    "reason": "Owner-call mirroring; R4.",
    "verbatim": "- A **decision the owner must make** → `PLAYTEST_CHECKLIST.md` →\n  \"Decisions waiting on you\". Never only in an agent doc."
  },
  {
    "id": "M17",
    "file": "docs/README.md",
    "first_line": 97,
    "last_line": 99,
    "classification": "task-local",
    "proposed_home": "WORKFLOW",
    "reason": "Maintain player replies after an owner ask under rule 5b; this is not unsolicited-draft authority.",
    "verbatim": "- A **reply to a player's report** (Steam, Reddit, GitHub) → `FIELD_REPORT_REPLIES.md`\n  at the root. The owner posts; agents draft, record what went up, and update a\n  draft in the same commit that changes the fact it states."
  },
  {
    "id": "M18",
    "file": "docs/README.md",
    "first_line": 100,
    "last_line": 100,
    "classification": "redundant",
    "proposed_home": "docs/README",
    "reason": "Same-doc restatement of append-only archive contract; R1.",
    "verbatim": "- **Spent** anything → `archive/`, which is append-only and never edited."
  },
  {
    "id": "M19",
    "file": "docs/README.md",
    "first_line": 102,
    "last_line": 104,
    "classification": "task-local",
    "proposed_home": "WORKFLOW",
    "reason": "Entry/report claim conflict handling.",
    "verbatim": "⚠️ **Reports are not authority.** When a report disagrees with `agent/bugs/` or\n`agent/facts/`, the entry wins — or the report is wrong and is corrected in the\nsame change that discovers it."
  },
  {
    "id": "M20",
    "file": "docs/README.md",
    "first_line": 111,
    "last_line": 112,
    "classification": "task-local",
    "proposed_home": "docs/README",
    "reason": "Legacy paths: translate instead of editing historical records.",
    "verbatim": "Pre-restructure\n> documents cite the old paths; translate mentally, do not edit records."
  },
  {
    "id": "M21",
    "file": "docs/README.md",
    "first_line": 115,
    "last_line": 117,
    "classification": "task-local",
    "proposed_home": "docs/README",
    "reason": "Standing-prompt legacy-path specialisation, not redundant.",
    "verbatim": "> 2026-09-11 (owner ask): the standing prompts moved into `agent/prompts/perma/` (DISPATCH, GENERAL_USE_PROMPT, RELEASE,\n> RELEASE_OUTBOX, POST_UPLOAD_CLOSE, PUBLIC_SURFACE_SWEEP, SITE_AUDIT, STATE_EVICTION, DRONE_PROJECT_PROMPT, COMBINED_SITTING).\n> Live references were rewritten; the archive and `metadata.lua` comments still cite `agent/prompts/<name>.md`, so translate them."
  },
  {
    "id": "M22",
    "file": "docs/README.md",
    "first_line": 119,
    "last_line": 121,
    "classification": "task-local",
    "proposed_home": "docs/README",
    "reason": "Reply-file legacy-path specialisation, not redundant.",
    "verbatim": "> 2026-09-11 (owner ask): `agent/reports/FIELD_REPORT_REPLIES.md` → `FIELD_REPORT_REPLIES.md` at the root, a human file (the\n> owner posts, agents draft). Live references were rewritten; the archive and the committed Codex report still cite the\n> old path, so translate them."
  },
  {
    "id": "M23",
    "file": "docs/README.md",
    "first_line": 123,
    "last_line": 126,
    "classification": "task-local",
    "proposed_home": "docs/README",
    "reason": "Old-name interpretation and historical-record preservation; not a duplicate of a bare archive prohibition.",
    "verbatim": "> 2026-08-17: the pack was renamed **Community Fix Pack → Relaunched Fix Pack** (display name only; the mod\n> `id` and the `[CommunityFixPack]` log tag are UNCHANGED). Earlier records use the old name — translate\n> mentally, do not edit records. The old name is still live in `agent/bugs/`, `agent/facts/EF-054.md` and\n> several reports."
  },
  {
    "id": "S01",
    "file": "docs/agent/STATE.md",
    "first_line": 3,
    "last_line": 3,
    "classification": "doc-local",
    "proposed_home": "STATE header",
    "reason": "Kernel-only content contract.",
    "verbatim": "Kernel only: status + pointer, never derivation."
  },
  {
    "id": "S02",
    "file": "docs/agent/STATE.md",
    "first_line": 14,
    "last_line": 14,
    "classification": "task-local",
    "proposed_home": "pack/release task doc, comparison pending",
    "reason": "Never carry a pack size; predict it. Citation context is not another rule.",
    "verbatim": "Never carry a pack size — predict with `tools/pack_predict.py`."
  },
  {
    "id": "S03",
    "file": "docs/agent/STATE.md",
    "first_line": 21,
    "last_line": 21,
    "classification": "task-local",
    "proposed_home": "entry/fact authoring rules",
    "reason": "Preserve old entries' build stamps.",
    "verbatim": "Old entries KEEP their version stamp."
  },
  {
    "id": "S04",
    "file": "docs/agent/STATE.md",
    "first_line": 22,
    "last_line": 22,
    "classification": "global",
    "proposed_home": "STATE",
    "reason": "Runtime/source priority; branch/save fact in the excerpt is not another rule.",
    "verbatim": "Trust runtime over source (`EF-078`). ⛔ **1.0.7 SAVES CANNOT LOAD ON 1.1.0** (`EF-079`) — the fixture library"
  },
  {
    "id": "S05",
    "file": "docs/agent/STATE.md",
    "first_line": 23,
    "last_line": 23,
    "classification": "task-local",
    "proposed_home": "playtest provisioning doc",
    "reason": "Provision branch-correct fixtures; triage-only override.",
    "verbatim": "  is branch-locked; a 1.1.0 leg needs a NEW colony provisioned from scratch (hours). Override is triage-only (`EF-080`)."
  },
  {
    "id": "S06",
    "file": "docs/agent/STATE.md",
    "first_line": 24,
    "last_line": 26,
    "classification": "task-local",
    "proposed_home": "F116/F117/F118 entries with STATE hold pointer",
    "reason": "Do not promote these specific held defects without play evidence.",
    "verbatim": "- ⛔ NEVER REPRODUCED, status HELD at `filed`/source-derived, never promote without a play leg: **F116** (repaired\n  in-body `add94b3`), **F117** (`777249d`; station recipe in `bugs/F117.md` §Control, desk 8/8, ⛔ untested in play —\n  a nil `CachedArgShape()` makes the control vacuous), **F118** (rider `0136af1`, no probe)."
  },
  {
    "id": "S07",
    "file": "docs/agent/STATE.md",
    "first_line": 29,
    "last_line": 29,
    "classification": "task-local",
    "proposed_home": "probe-kit reporting",
    "reason": "Kit verdicts are predictions until owed boot, not measurements.",
    "verbatim": "Kit verdicts are PREDICTIONS until then; still FAIL/ERROR by name:"
  },
  {
    "id": "S08",
    "file": "docs/agent/STATE.md",
    "first_line": 33,
    "last_line": 33,
    "classification": "task-local",
    "proposed_home": "C89 entry",
    "reason": "Specific reopening trigger; unavailable-arm facts are not rules.",
    "verbatim": "**Reopen C89 on a countering field report.**"
  },
  {
    "id": "S09",
    "file": "docs/agent/STATE.md",
    "first_line": 35,
    "last_line": 35,
    "classification": "task-local",
    "proposed_home": "WORKFLOW",
    "reason": "Never re-derive a leg from implementation.",
    "verbatim": "never re-derive a leg from the module."
  },
  {
    "id": "S10",
    "file": "docs/agent/STATE.md",
    "first_line": 39,
    "last_line": 40,
    "classification": "task-local",
    "proposed_home": "C92 brief with retained STATE hold pointer",
    "reason": "Shipping hold, not spare kernel budget.",
    "verbatim": "  ⭐ **ck172 RULED 09-13: build the RESTORATION, ⛔ SHIPPING HELD until the owner lifts it in words** —\n  brief `prompts/C92_ACHIEVEMENT_BUILD.md`; ck171 (scope) stays OPEN. Achievement testing = `EF-094`."
  },
  {
    "id": "S11",
    "file": "docs/agent/STATE.md",
    "first_line": 49,
    "last_line": 49,
    "classification": "task-local",
    "proposed_home": "player-report investigation route",
    "reason": "Tracker API route.",
    "verbatim": "- ⛔ Read the GitHub tracker via `api.github.com/.../issues/<n>/comments`, never the HTML page."
  },
  {
    "id": "S12",
    "file": "docs/agent/STATE.md",
    "first_line": 52,
    "last_line": 53,
    "classification": "task-local",
    "proposed_home": "site task docs",
    "reason": "Owner deployment and deployed-SHA recheck protocol; exact perma comparison pending.",
    "verbatim": "The deploy is the owner's act — `publish-site.yml` is\n  `workflow_dispatch` only. ⛔ Never quote a stored \"deployed = <sha>\"; read the deployments API (`perma/SITE_AUDIT.md`)."
  },
  {
    "id": "S13",
    "file": "docs/agent/STATE.md",
    "first_line": 60,
    "last_line": 60,
    "classification": "task-local",
    "proposed_home": "toolkit testing/provisioning doc",
    "reason": "Do not equate untainted and achievement-eligible.",
    "verbatim": "  ⛔ Eligibility stays `UNAVAILABLE:sandbox` (`EF-096`) — no-taint is necessary, NOT proven sufficient."
  },
  {
    "id": "S14",
    "file": "docs/agent/STATE.md",
    "first_line": 64,
    "last_line": 65,
    "classification": "task-local",
    "proposed_home": "C92 brief with retained STATE hold pointer",
    "reason": "Hold repeated inside NEXT is contextual routing, not independently claimed redundant.",
    "verbatim": "- ⏭ NEXT: fire `prompts/STANDDOWN_AUDIT.md` (no blocker) · `prompts/C92_ACHIEVEMENT_BUILD.md` (build+test, ⛔ ships never\n  without ck172's hold lifted) · then the playtest sitting. ⛔ `SELFCHECK_PILOT` REMOVED 09-13 (`cf8d51f`)."
  },
  {
    "id": "S15",
    "file": "docs/agent/STATE.md",
    "first_line": 71,
    "last_line": 71,
    "classification": "task-local",
    "proposed_home": "DestroyedRebuild entry",
    "reason": "Hardening hold plus specific reopening prerequisites.",
    "verbatim": "  ⛔ Do NOT harden `DestroyedRebuild`'s `efVisible` guard; reopen ONLY with the hex's buildings list + mod list + a save."
  },
  {
    "id": "S16",
    "file": "docs/agent/STATE.md",
    "first_line": 75,
    "last_line": 76,
    "classification": "task-local",
    "proposed_home": "release/console task docs plus retained kernel hazard pointer",
    "reason": "Launched-game portal-API prohibition with portal order.",
    "verbatim": "- **H-03** No script/console in a launched game may touch a portal API — the FIRST call **creates the listing**\n  (`SteamWorkshop.lua:17-22`). Safe: `DbgPackMod`, `tools/upload_preflight.py`. Paradox before Steam."
  },
  {
    "id": "S17",
    "file": "docs/agent/STATE.md",
    "first_line": 77,
    "last_line": 78,
    "classification": "global",
    "proposed_home": "STATE",
    "reason": "Cross-document sweep evidence fence, including specialised kernel/log writing restriction.",
    "verbatim": "- **H-05** Sweep fence: no session reads `prompts/prelaunch-sweep/SWEEP_FINDINGS.md` or the link reports to reach\n  a verdict, and neither STATE nor SESSION_LOG ever restates a link verdict — point at the ledger instead."
  },
  {
    "id": "S18",
    "file": "docs/agent/STATE.md",
    "first_line": 79,
    "last_line": 81,
    "classification": "task-local",
    "proposed_home": "rig/junction task docs plus retained kernel hazard pointer",
    "reason": "Owner-only enable recovery and same-id swap qualification.",
    "verbatim": "- **H-08** ⛔ Pulling a mod's junction COSTS its enable and restoring the folder does NOT buy it back (`EF-055`);\n  recovery = owner tick + restart, never an agent's. ⚠️ The cost lands when the **id vanishes**; a folder-for-\n  folder swap under the **same id KEEPS** the enable (the opt-in pack is in that state now, ck43)."
  },
  {
    "id": "S19",
    "file": "docs/agent/STATE.md",
    "first_line": 82,
    "last_line": 83,
    "classification": "task-local",
    "proposed_home": "pack/rig task docs plus retained kernel hazard pointer",
    "reason": "No packed folder beside a live junction.",
    "verbatim": "- **H-09** Never stage a packed folder beside a live junction — at equal version the **unpacked one WINS**,\n  silently (`Mod.lua:1770`), and the leg measures nothing."
  },
  {
    "id": "S20",
    "file": "docs/agent/STATE.md",
    "first_line": 86,
    "last_line": 86,
    "classification": "global",
    "proposed_home": "STATE",
    "reason": "Truthful readiness/publication claims.",
    "verbatim": "- **H-04** ⛔ Never call a FUTURE release ready, and never treat \"published\" as covering anything the owner has not done."
  },
  {
    "id": "S21",
    "file": "docs/agent/STATE.md",
    "first_line": 87,
    "last_line": 87,
    "classification": "task-local",
    "proposed_home": "release governance doc",
    "reason": "Shipping bar is a normative definition.",
    "verbatim": "- Ship line FROZEN (08-12): `fixed` + suite + self-checks + verified save-safety IS the bar."
  },
  {
    "id": "S22",
    "file": "docs/agent/STATE.md",
    "first_line": 88,
    "last_line": 90,
    "classification": "task-local",
    "proposed_home": "release/fix maintenance procedure",
    "reason": "One-time gate versus major-overhaul qualification.",
    "verbatim": "- ⛔ The gate was ONE-TIME, not a per-change tax (08-20, item 57). Post-release = patch-note-driven maintenance:\n  `items.lua` entry (doccheck MODULE SETS) + one boot `applied` log + doccheck counts. ⛔ Never quote `FIX_POLICY` §3a's per-module\n  cost for a single added fix — run B / lens sweep / audit return only for a **major overhaul**."
  },
  {
    "id": "S23",
    "file": "docs/agent/STATE.md",
    "first_line": 91,
    "last_line": 91,
    "classification": "global",
    "proposed_home": "STATE",
    "reason": "Vendor patch assertion is unconfirmed until verified.",
    "verbatim": "- ⚖️ A vendor patch note saying \"Fixed\" is a **CLAIM, false until we confirm it** (owner, 09-08)."
  },
  {
    "id": "S24",
    "file": "docs/agent/STATE.md",
    "first_line": 95,
    "last_line": 95,
    "classification": "task-local",
    "proposed_home": "WORKFLOW",
    "reason": "SKIPs named individually; perma comparisons pending.",
    "verbatim": "- ⛔ SKIPs BY NAME, never a total."
  },
  {
    "id": "S25",
    "file": "docs/agent/STATE.md",
    "first_line": 96,
    "last_line": 96,
    "classification": "task-local",
    "proposed_home": "release metadata doc",
    "reason": "Preserve mod id and log tag through display-name change.",
    "verbatim": "- Display name Relaunched Fix Pack; `id` + `[CommunityFixPack]` log tag KEPT (08-17)."
  },
  {
    "id": "S26",
    "file": "docs/agent/STATE.md",
    "first_line": 97,
    "last_line": 97,
    "classification": "task-local",
    "proposed_home": "public-surface task doc",
    "reason": "Naming and load-order advice restriction; exact source comparison pending.",
    "verbatim": "- Never name fredware's mod on a player surface; no player load-order advice (`EF-054`, FIX_POLICY §8)."
  },
  {
    "id": "S27",
    "file": "docs/agent/STATE.md",
    "first_line": 102,
    "last_line": 102,
    "classification": "task-local",
    "proposed_home": "UPLOAD_WORKFLOW",
    "reason": "Paste backups required and current; no reopening auto-fill question.",
    "verbatim": "  `UPLOAD_WORKFLOW` §3 paste backups stay REQUIRED every cycle. Auto-fill is CLOSED (ck155, never re-ask)."
  },
  {
    "id": "S28",
    "file": "docs/agent/STATE.md",
    "first_line": 106,
    "last_line": 107,
    "classification": "doc-local",
    "proposed_home": "STATE header",
    "reason": "Preserve parser idioms in this enumeration.",
    "verbatim": "This enumeration feeds `WAITING_ON_YOU.md` — keep the\n  literal `STILL OPEN:` and `Owner OWES: ck##` idioms, or the owner's register silently drops items."
  },
  {
    "id": "S29",
    "file": "docs/agent/STATE.md",
    "first_line": 113,
    "last_line": 113,
    "classification": "task-local",
    "proposed_home": "F59 entry",
    "reason": "Repair must cover both callers; frozen-download description retained as factual context.",
    "verbatim": "must cover both,"
  },
  {
    "id": "S30",
    "file": "docs/agent/STATE.md",
    "first_line": 117,
    "last_line": 117,
    "classification": "doc-local",
    "proposed_home": "STATE header",
    "reason": "Generated count section is never typed.",
    "verbatim": "Build state — `python tools/doccheck.py --emit-counts`, never hand-typed"
  },
  {
    "id": "S31",
    "file": "docs/agent/STATE.md",
    "first_line": 125,
    "last_line": 125,
    "classification": "doc-local",
    "proposed_home": "STATE header",
    "reason": "Re-emit this document's build region after a change.",
    "verbatim": "Re-emit after any change."
  },
  {
    "id": "K01",
    "file": "docs/PLAYTEST_CHECKLIST.md",
    "first_line": 4,
    "last_line": 7,
    "classification": "doc-local",
    "proposed_home": "checklist header",
    "reason": "Worklist-only content; predictions and console forensics supplied in sitting.",
    "verbatim": "live agent session alongside**. This file is the work list and nothing else:\nwhat to test, how to set it up, what each test needs. Expectations,\npredictions, pass/fail readings and console forensics are NOT written here —\nthe agent supplies them in the sitting, from each test's linked entry."
  },
  {
    "id": "K02",
    "file": "docs/PLAYTEST_CHECKLIST.md",
    "first_line": 11,
    "last_line": 25,
    "classification": "doc-local",
    "proposed_home": "checklist header",
    "reason": "Whole-body retirement, test/decision/session distinctions and residual pointers; keep the qualifications.",
    "verbatim": "> ⛔ **RETIREMENT RULE — owner ruling 2026-09-14, item 177. EVERY section in this\n> file retires to [archive/PLAYTEST_ARCHIVE.md](archive/PLAYTEST_ARCHIVE.md) once it\n> is settled — not tests alone.** This extends the old rule (*\"completed tests move\n> whole\"*, 44 sections as of 2026-08-01, plus the 2026-08-03 pre-redesign snapshot),\n> which covered ~1% of the file while the other 99% had no rule reaching it.\n>\n> - a **test** retires when it is completed;\n> - a **decision** retires once its marker reads `ruled` or `closed`;\n> - a **dated session record** does not belong here at all — it goes to\n>   `archive/SESSION_LOG.md`. This file is the work list, nothing else.\n>\n> The move is whole-body, leaving the heading, the marker and a pointer behind.\n> `.claude/tools/archive_settled.py` performs exactly that move over the marked set.\n> ⚠️ **An unmarked item can never become settled, so it can never retire** — the\n> marker is what makes this rule run, and neglecting it is how this file reached 54%"
  },
  {
    "id": "W01",
    "file": "docs/agent/WORKFLOW.md",
    "first_line": 16,
    "last_line": 19,
    "classification": "task-local",
    "proposed_home": "WORKFLOW",
    "reason": "Update entry with fixes; generated-index clause is a scoped specialisation.",
    "verbatim": "   Update the ENTRY in the same change that adds or edits a fix. **`INDEX.md`\n   is GENERATED — never hand-edit it.** A status still lives in two places, but\n   both are now inside the entry file: front-matter `status:` and the heading\n   tag. doccheck goes red if they disagree, and red on a stale INDEX."
  },
  {
    "id": "W02",
    "file": "docs/agent/WORKFLOW.md",
    "first_line": 31,
    "last_line": 34,
    "classification": "task-local",
    "proposed_home": "WORKFLOW",
    "reason": "Human-doc execution markers.",
    "verbatim": "1. **Execution markers (R2).** Every console line, lever or command printed in a\n   human doc carries `[RAN <date>, log <name>]` or `[NEVER RUN]`. Unmarked, a\n   never-executed snippet reads exactly like a proven one — the PT-61 near-miss\n   was a gate that would have parked a whole attended sitting."
  },
  {
    "id": "W03",
    "file": "docs/agent/WORKFLOW.md",
    "first_line": 35,
    "last_line": 40,
    "classification": "task-local",
    "proposed_home": "WORKFLOW",
    "reason": "Per-claim and per-row provenance.",
    "verbatim": "2. **Provenance words (R3).** Load-bearing claims in entries, specs and briefs\n   are prefixed **MEASURED / SOURCE / INFERRED / INHERITED / GUESS**, and **the\n   ROUTE sentence is tagged separately from its citations** (\"therefore the only\n   way is…\" is a different claim from the lines it cites — the project has been\n   wrong about a route while every cited line was right, twice). ⛔ **A blanket\n   verification claim over a table is banned: the tag goes per row.**"
  },
  {
    "id": "W04",
    "file": "docs/agent/WORKFLOW.md",
    "first_line": 41,
    "last_line": 45,
    "classification": "task-local",
    "proposed_home": "WORKFLOW",
    "reason": "Takeability and owner routing.",
    "verbatim": "3. **TAKEABLE-WHEN on routed items (R5).** Routing names the owner prompt AND\n   the precondition (\"needs a suite run\" / \"a colony with the law enacted\" /\n   \"the owner at the keyboard\"). An item whose precondition is a *situation*\n   goes to the checklist as a rider immediately, not to a prompt that will\n   forward it again."
  },
  {
    "id": "W05",
    "file": "docs/agent/WORKFLOW.md",
    "first_line": 46,
    "last_line": 53,
    "classification": "task-local",
    "proposed_home": "WORKFLOW",
    "reason": "Archive cited logs in same commit; force ignored log additions.",
    "verbatim": "4. **Archive load-bearing logs (R8).** If a leg's numbers will be cited by a\n   status flip, copy the log into the repo in the SAME commit. The game's\n   rotation cap is ~20 files and it has already eaten founding measurements.\n   Cannot be applied retroactively, which is the whole argument for now.\n   ⛔ **`.gitignore` line 2 is `*.log`, so the archive copy needs\n   `git add -f`** — a plain `git add` drops it SILENTLY and the commit looks\n   complete (one commit shipped with a false archive claim before this was\n   caught, 2026-08-03)."
  },
  {
    "id": "W06",
    "file": "docs/agent/WORKFLOW.md",
    "first_line": 54,
    "last_line": 62,
    "classification": "task-local",
    "proposed_home": "WORKFLOW",
    "reason": "Canonical owner-call mirroring plus marker/regeneration specialisations; R4.",
    "verbatim": "5. **Owner-decision mirroring (R10).** Every item needing the owner's call is\n   mirrored into `docs/PLAYTEST_CHECKLIST.md` → \"Decisions waiting on you\"\n   (one line + pointer), and struck the moment it is decided. **An owner\n   decision recorded only in an entry or a report is not considered asked.**\n   **Changing an item's status ALSO means updating its marker.** Update the\n   checklist's `<!-- ck:N status:... owner:... -->` marker in the same edit,\n   including whether an action is still owed by the owner. Regenerate the\n   owner register after editing its source; for the contained regeneration\n   route, see \"Writing in a shared tree\" below."
  },
  {
    "id": "W07",
    "file": "docs/agent/WORKFLOW.md",
    "first_line": 63,
    "last_line": 77,
    "classification": "task-local",
    "proposed_home": "WORKFLOW",
    "reason": "Record ruling conditions; check expiry.",
    "verbatim": "5a. **A ruling carries the state it was made in (R10b, adopted 2026-09-12,\n   checklist 161).** When you write an owner ruling down, record the CONDITION\n   it was made under beside the words — what was broken, what was being triaged,\n   which release it was steering. ⚖️ **A ruling made under a named condition\n   expires with that condition**: re-read it against today's state before\n   treating it as binding, and ⛔ **never record a later, different ruling as a\n   \"reversal\" without first checking whether the earlier one's condition still\n   holds.** Named after the miss: the 09-08 *\"we fix anything negatives, a small\n   positive I am not as concerned about\"* ruling was **triage scoped to the 1.1.0\n   recovery** — an attention-routing device for a period when the pack could do\n   active harm. Recorded without that scope (and, worse, stamped \"it generalises\n   well beyond this one case\"), it read as standing policy, and **three separate\n   documents re-derived a false contradiction with the 09-09 ask and handed it\n   back to the owner as an open question** — the exact attention drain the\n   original triage rule existed to prevent."
  },
  {
    "id": "W08",
    "file": "docs/agent/WORKFLOW.md",
    "first_line": 79,
    "last_line": 92,
    "classification": "task-local",
    "proposed_home": "WORKFLOW",
    "reason": "Player replies pull-only; triage exemption is part of the rule.",
    "verbatim": "5b. **Player replies are PULL-ONLY (R10c, owner ruling 2026-09-12, checklist\n   165).** Rule 5's mirroring obligation ⛔ **does NOT extend to replies to player\n   reports.** Never draft one unasked, never put one on the owner's owed list\n   (`STATE.md`'s OWES line, a handoff's decisions table, a session summary's\n   \"waiting on you\"), never raise a waiting `DRAFT` as a nudge, and never gate\n   other work on a reply going out. A draft in `docs/FIELD_REPORT_REPLIES.md`\n   waits indefinitely **by design**. When the owner asks for one, write it and\n   stop — one ask, one draft, no follow-on queue. ✅ **This does not touch\n   triage:** a player's report is evidence about a defect, and filing it into\n   `agent/bugs/` is ordinary bug-fixing work that continues unchanged — ⛔ never\n   cite this rule to avoid reading, filing or investigating a report. ⚖️ Condition\n   (per 5a): the owner had fielded a day of reply questions while the project's\n   real gate was an unrun playtest. The cost being cut is **owner attention\n   diverted from fixing bugs**, not the replies themselves."
  },
  {
    "id": "W09",
    "file": "docs/agent/WORKFLOW.md",
    "first_line": 96,
    "last_line": 102,
    "classification": "task-local",
    "proposed_home": "WORKFLOW",
    "reason": "Status-flip edit order; not a duplicate of a short generated-output banner.",
    "verbatim": "6. **`INDEX.md` in `agent/bugs/` and `agent/facts/` is GENERATED.** Edit the\n   entry or fact file; doccheck regenerates the index and goes red on any\n   difference, and red when front-matter `status:` and the heading tag disagree.\n   **Edit order for a status flip** (adopted 2026-08-03, standing-prompts\n   redesign O4): front-matter `status:` first — the index regenerates from\n   it — then the heading tag to match, in the same edit. A red doccheck means\n   you stopped halfway."
  },
  {
    "id": "W10",
    "file": "docs/agent/WORKFLOW.md",
    "first_line": 103,
    "last_line": 104,
    "classification": "task-local",
    "proposed_home": "WORKFLOW",
    "reason": "Canonical doccheck-before-commit rule; R3.",
    "verbatim": "7. **Run `python tools/doccheck.py` before committing doc changes** — red\n   blocks. One-time setup: `git config core.hooksPath tools/hooks`."
  },
  {
    "id": "W11",
    "file": "docs/agent/WORKFLOW.md",
    "first_line": 105,
    "last_line": 114,
    "classification": "task-local",
    "proposed_home": "STATE header / STATE_EVICTION, allocation pending",
    "reason": "STATE edit/eviction procedure; cannot allocate fully without the perma read.",
    "verbatim": "8. **STATE.md is BYTE-budgeted with an eviction rule** (owner ruling 2026-08-18,\n   checklist 42; the 2026-08-03 60-line cap is RETIRED — it was satisfied while\n   being defeated). doccheck enforces warn/hard byte caps plus a per-line cap;\n   a doccheck WARN must be copied VERBATIM into the owner report, and the owner\n   fires `agent/prompts/perma/STATE_EVICTION.md`. Format for machine efficiency and\n   safety: one fact per line, never widen or pack lines to satisfy a budget —\n   evict, don't compress. Resolved or superseded material moves to\n   `docs/archive/SESSION_LOG.md` (append-only, newest-first, `tags:` line).\n   Evict history, never obligations — open gates, holds, owner decisions and\n   the counts block stay."
  },
  {
    "id": "W12",
    "file": "docs/agent/WORKFLOW.md",
    "first_line": 153,
    "last_line": 155,
    "classification": "task-local",
    "proposed_home": "WORKFLOW, unresolved X1",
    "reason": "Per-fix commit discipline includes editing the frozen description.",
    "verbatim": "4. One commit per fix or tight group; agent/bugs/ updated in the same commit;\n   MOD_DESCRIPTION.md updated in the same commit as the code change it\n   describes."
  },
  {
    "id": "W13",
    "file": "docs/agent/WORKFLOW.md",
    "first_line": 640,
    "last_line": 649,
    "classification": "task-local",
    "proposed_home": "WORKFLOW, unresolved X1",
    "reason": "Release instructions edit the frozen description; no retirement self-authorised.",
    "verbatim": "- MOD_DESCRIPTION.md: delete the `[DRAFT NOTE]` markers; do NOT promise the\n  ClassicRockets export half; sync the fix list with agent/bugs/ statuses.\n  ⭐ **Add the \"judgment calls\" section** (owner ADOPTED the relabel proposal\n  2026-08-04: F55, F40, F73(b), F70, F97 presented as design-judgment repairs,\n  not plain bugs) — ⚠️ **its wording is OWED BY THE OWNER** and must be asked\n  for if it does not exist yet; the checklist line tracks it.\n  **Recount the probe number** quoted in the \"What we can promise, and what we\n  can't\" block — it moves whenever a wave file gains or loses a probe, and a\n  stale number there is a false claim in player-facing text. Authoritative count\n  is in `agent/STATE.md`."
  },
  {
    "id": "W14",
    "file": "docs/agent/WORKFLOW.md",
    "first_line": 874,
    "last_line": 875,
    "classification": "global",
    "proposed_home": "STATE",
    "reason": "Volatile-external recheck; site/pack instrument instructions specialise it.",
    "verbatim": "  Read it with a command, every time. ⛔ Never quote a stored number: it was true once, and\n  this rig auto-updated into a new game build unasked while nobody was looking."
  },
  {
    "id": "W15",
    "file": "docs/agent/WORKFLOW.md",
    "first_line": 883,
    "last_line": 886,
    "classification": "global",
    "proposed_home": "STATE",
    "reason": "Command-based absence proof, decoded input and presence-side count.",
    "verbatim": "**R-B · Never read a file to prove a negative.** Absence is settled by a grep, never by\nreading. And a negative in a *compressed* artifact is not a sample at all — decode first. Three\nincidents here: the fpk \"not found\", the grep on an old name that was really a rename, and a\none-sided count. A claim about what is ABSENT needs the presence side counted too."
  }
]
```

## Stop / next request

[RAN 2026-09-14, tool transcript] Final report-only doccheck: GREEN at 2bbdbd3; STATE is now 12,331 bytes. A scoped diff shows only toolkit routing/boot obligations changed, leaving the candidate local excerpts unchanged. The same framing-only +89-byte proposal would therefore yield 12,420 bytes currently, 2,940 below the temporary warning and 132 above the permanent warning. No offsetting eviction is approved.


Under the commissioned task's section 6, X1 requires owner direction before proceeding. The concrete request is permission to **finish the remaining inventory while keeping X1 unresolved for the later migration gate**. This authorises analysis only, not deletion/rewording of the stale instruction. Complete per-doc inventory, redundancy/dead checks, eligibility and offsetting STATE arithmetic before seeking migration approval.
