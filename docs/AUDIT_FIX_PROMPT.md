# ONE-OFF FIX PROMPT — implement the 2026-07-29 audit remediation (Phases 1-3)

**Paste everything below into a FRESH session (any model).** This is a one-off.
Delete it when the plan's Phase 1-3 boxes are checked off in
docs/AUDIT_FINDINGS.md (and update every doc that references this file).

---

You are implementing the remediation plan in **docs/AUDIT_FINDINGS.md** for the
Surviving Mars: Relaunched "Community Fix Pack" at `C:\Dev\SMR-BugFixPack`.
The audit is done and verified; do not re-litigate its findings — but DO
re-read each cited site before editing it (line numbers may have drifted), and
if the code contradicts a finding, stop and flag it instead of forcing the fix.

## Read first, in this order

1. `docs/AUDIT_FINDINGS.md` — the findings and the plan. Your scope is
   **Phase 1 (code), Phase 2 (packaging/description), Phase 3 (docs)**.
   Phase 4 is deferred: do NOT extract core helpers, do NOT merge modules.
2. `docs/STATUS.md` → "Key technical facts" section — engine behaviors that
   will otherwise mislead you (mod code loads before classes are built;
   `error()`/`assert()` report and CONTINUE; the sandbox blacklist; `rawget`
   vs `_G[k]=v` semantics; `/` is integer division). Phase 3.2 has you move
   this section to `docs/ENGINE_FACTS.md` — read it BEFORE moving it.
3. `docs/FIX_POLICY.md` — you will be extending it (Phase 3.6); follow it
   meanwhile.
4. `Code/00_Core.lua`, `Code/Fix_LastTransmissionStorage.lua` (:96-125 — the
   veto-re-check + data-loaded-latch donor pattern), and
   `Code/Opt_DroneOverhaul.lua` (:74-76 header — the file-scope-install +
   per-call-gate donor pattern). These two files are the models Phase 1 copies;
   match their idioms exactly rather than inventing new ones.

## Ground rules

- **Never modify anything under
  `A:\SteamLibrary\steamapps\common\Project Spark\ModTools\Src`** (game source,
  read-only reference). The TestKit repo is out of scope.
- Minimal diffs. Phase 1 items are surgical edits to existing files — no
  renames, no moves, no style sweeps beyond what an item names.
- Every code file you touch: re-verify its patch target still matches the
  cited game-source lines before and after your edit (the house discipline).
- Parse-check every edited Lua file (the project's parse sweep; a syntax error
  in ANY listed file breaks the whole pack at load).
- Doc rules that bind you: BUGS.md statuses live in TWO places (index row +
  heading tag) — never flip one without the other. MOD_DESCRIPTION.md changes
  land in the SAME commit as the code change they describe. Keep all docs
  model-neutral (no model names in prompts/docs).
- Commit in logical units (one commit per plan item or tight group), messages
  naming the plan item (e.g. "Audit fix 1.1: ..."). PowerShell 5.1 mangles
  embedded double quotes in `git commit -m` — write the message to a temp file
  and use `git commit -F <file>`.
- As you complete each item, tick its `[ ]` → `[x]` in docs/AUDIT_FINDINGS.md
  (same commit).

## Sequencing and item-specific cautions

**Phase 1 first (code), then 2, then 3.** Within Phase 1:

- **1.1 / 1.2** are pure additions inside the three `patch()` functions and
  their DataLoaded bookkeeping. Caution on Fix_IndependenceTerraforming: the
  status-heal exists to fix a real mislabel case (see its :92-98 comment) —
  keep the heal, but gate it so `"disabled"` is never overwritten and a vetoed
  fix never patches.
- **1.3** is the riskiest item. Moving installs to file scope means they run
  at classdef time even when the option is OFF — that is the point (the hooks
  become pass-throughs via the per-call `IsActive` gate, exactly like
  Opt_DroneOverhaul). Requirements: (a) guard each file-scope install with the
  same existence checks `apply()` used, so a missing target degrades to the
  reason-string path instead of erroring at load; (b) `apply()` keeps its
  self-checks and returns the same strings, so registry semantics and the
  Mod Options reconciliation are unchanged; (c) Opt_ResidencyControl: ONLY the
  `Community.CanAcceptNewColonists` wrap moves — the `ChooseDome` global wrap
  and the two UI `Init` wraps are already live-enable-safe; (d)
  Opt_MultipleSuns: ONLY the `SolarPanelBase.GameInit` wrap moves — the
  build_once data patch and sweeps stay as they are (they are
  `module_active`-gated and correct); (e) update each header's toggle-semantics
  paragraph to the truth.
- **1.5**: the flag clear goes in the heal path only, after the
  vanilla-end-path release verdict; read Fix_DisasterPredictionLeak's handler
  first so the two stay idempotent side by side.

**Phase 2 cautions:**

- **2.2 (ModItemCode)** is order-critical: the engine regenerates
  `metadata.lua`'s `code` list from these items on any editor save, so the
  items must appear in EXACTLY the current metadata.lua:20-97 order (00_Core
  first, 90_SaveSanitizer after the last Fix_, then the six Opt_ in their
  current order). After writing, diff the item order against the metadata list
  name-by-name. Do not otherwise touch the six ModItemOptionToggle entries;
  their `name` fields are load-bearing (they ARE the Register ids).
- **2.1**: `lua_revision` stays 350453 (verified correct). `default_options`
  stays in sync with the toggles. Keep the description ≤ its current length
  class; `short_description` ≤ 200 chars.
- **2.3**: the achievements disclosure must state the verified fact precisely:
  achievements are blocked while any mod is enabled on Xbox / PlayStation /
  Microsoft Store — NOT on Steam/PC. Don't soften it.

**Phase 3 cautions:**

- **3.2/3.3 are moves, not rewrites**: content moved to `docs/ENGINE_FACTS.md`
  and `docs/archive/SESSION_LOG.md` must survive verbatim (these are the
  project's evidence trails). What gets *written new* is only the ~40-line
  STATUS current-state header. Update every pointer you break: FABLE_NEXT's
  read-list, PLAYTEST_CHECKLIST references to "STATUS key facts", WORKFLOW.
  Grep for `Key technical facts` and `STATUS.md` references when done.
- **3.4**: promote RESEARCH.md §3's unpromoted leads to C-rows in BUGS.md
  BEFORE archiving the file; move TESTING.md's probe-taxonomy table to the
  TestKit's README before archiving TESTING.md.
- **3.7** is mechanical: index rows become `status (+ date + PT ref)`; the
  prose you remove from a row must already exist in (or be moved into) the
  entry — never delete information outright.
- FABLE_NEXT_PROMPT (3.1): per its own convention, prefer rewriting the stale
  blocks over stacking more banner corrections.

## Deliver

1. All Phase 1-3 boxes in docs/AUDIT_FINDINGS.md ticked (or explicitly
   annotated why an item was skipped/changed — with the user's go-ahead for
   any scope change).
2. A STATUS.md leg (in the new current-state format you just built) recording
   what was done, plus anything you found that the audit missed.
3. A note in the wrap listing what now needs a HUMAN playtest pass:
   at minimum the three reworked Opt_ modules' live-toggle behavior (both
   directions, mid-session first enable) and a PT-20-shaped save/remove/load
   cycle — these belong to the owner's ongoing playtesting, do not attempt
   them yourself.
4. Delete this file (docs/AUDIT_FIX_PROMPT.md) in the final commit and fix any
   reference to it.

Work autonomously through the plan; stop and ask only where an item's
instructions conflict with what you find in the code.
