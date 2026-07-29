# Whole-Mod Audit — Findings & Remediation Plan (2026-07-29)

Product of the one-off AUDIT_PROMPT.md (now deleted per its own rule). Method:
four independent fresh-context reviews (full patch-target map over all 75
`Code/` files; registry/policy stress; documentation-as-information-system;
distribution readiness verified against the game source), top findings
spot-verified against the actual files before recording. **Nothing was modified
by the audit itself.** Remediation is tracked in the PLAN section at the bottom;
docs/AUDIT_FIX_PROMPT.md is the one-off that implements it.

Ground truth: `Code/` = **75 files** (67 `Fix_` + 6 `Opt_` + 00_Core +
90_SaveSanitizer) = **74 registered modules, 68 default-active**. Several docs'
counts disagreed with this — see D-findings.

Statuses: `[ ]` open · `[x]` fixed/done · `[~]` deliberately deferred/declined.

---

## Severity A — would ship broken behavior or block upload

### A1. Per-fix disable veto bypassed by three data-patch fixes `[x — fixed 2026-07-29, plan 1.1]`
`SMRFixPack_Disabled[id]` only skips `apply()` (00_Core.lua:90-94), but these
install file-scope `OnMsg.DataLoaded`/`DataChanged` handlers that mutate presets
regardless of the veto:
- Fix_DustSicknessDamage.lua:73-82 → `patch()` (:43) swaps
  `TraitPresets.DustSickness.daily_update_func` even when disabled.
- Fix_DustSicknessBiorobots.lua:125-133 → `patch()` (:88) appends the Android
  storybit filters even when disabled.
- Fix_IndependenceTerraforming.lua:122-130 → `patch()` (:63) rewrites the tech
  effect even when disabled — **and sets `entry.status = "active"` (:85-89),
  overwriting a `"disabled"` status**, which then also re-arms its status-gated
  LoadGame sweep (:182-184). The veto is fully defeated.

The corrective pattern exists in-repo — the QA-2026-07-25 veto re-check at
Fix_LastTransmissionStorage.lua:102-106 — applied to one file of four, never
propagated. Found independently by two reviewers; verified. FIX_POLICY §2
violation.

### A2. First mid-session enable of three optional modules is silently dead (or half-dead) until restart `[x — fixed 2026-07-29, plan 1.3; live first-enable confirmation still owed to playtest]`
Per the project's own live-proven engine fact (STATUS "Key technical facts":
runtime patches on a base class are invisible to already-flattened derived
classes), an option OFF at load installs nothing; the first in-game toggle runs
`apply()` post-flattening, so these base-class installs never reach live
instances that session:
- Opt_ClassicRockets — `UniversalRocketBase.GetFuelResourceRequest` wrap
  (Opt_ClassicRockets.lua:84-98): reports active, does nothing.
- Opt_ResidencyControl — the `Community.CanAcceptNewColonists` gate
  (Opt_ResidencyControl.lua:177-183) is dead while the `ChooseDome` global wrap
  (call-time resolution) works → **partially** working, silently.
- Opt_MultipleSuns — the `SolarPanelBase.GameInit` binding half
  (Opt_MultipleSuns.lua:111-122): limit lifts, new panels don't bind to sun #2.

All three headers claim toggles "take effect immediately, both directions" —
overstated for the first-enable session (next session self-heals: the option is
in CurrentModOptions before mod code loads). The correct pattern — **file-scope
install + per-call `IsActive` gate** — exists and is documented in
Opt_DroneOverhaul.lua:74-76; applied to one module of six.
(Opt_CohortHousing wraps Colonist methods and Opt_AcknowledgedWarnings replaces
globals — both live-enable-safe.) *Static inference from the proven engine
fact; one live confirmation still worthwhile (see UNVERIFIED).*

### A3. Packaging: four hard upload blockers + the ignore-list gap `[ ]`
Verified in the game source:
- `short_description` missing → **Paradox Mods upload hard-rejected**
  (ParadoxMods.lua:29-32).
- `image` (preview) missing → **Paradox Mods hard-rejected** (ParadoxMods.lua:39-42,
  ≤2 MB :87-92). Steam tolerates absence (SteamWorkshop.lua:113) but the listing
  is presentation-poor; ≤1 MB when present.
- `last_changes` empty → **Steam upload rejected** (SteamWorkshop.lua:39-41);
  PDX requires it on updates (ParadoxMods.lua:49-51).
- **Mod Editor round-trip wipes the mod:** `SaveDef` regenerates `code` solely
  from `ModItemCode` items (Mod.lua:960-974, :816-840); items.lua has zero
  (only 6 option toggles) while the 75-file `code` list is hand-written in
  metadata.lua:20-97. The upload flow saves-if-dirty (GedModEditor.lua:838-839),
  so publishing through the editor as-is writes `code = false` → the published
  mod loads **no code at all**. There is no CLI upload path in the shipped tools.
- No `ignore_files`: the packer includes everything recursively minus the default
  `{*.git/*, *.svn/*, */Source/*, */SourceData/*}` (Mod.lua:250-256,
  GedModEditor.lua:716-732) — so `docs/` (~788 KB incl. BUGS.md and the prompt
  docs), `README.md`, `.gitignore`, `.claude/settings.json` all ship in the .hpk.

### A4. Consoles: any loaded mod silently disables ALL achievements — undisclosed `[ ]`
`DoModsBlockAchievements()` returns true on PlayStation, Xbox, and Microsoft
Store, and any loaded mod then blocks every unlock (Achievement.lua:61-63,
:77-79 — verified). Steam/PC unaffected. Neither MOD_DESCRIPTION.md nor
README.md mentions it. The single most important storefront disclosure for a
"safe, fixes-only" pack.

## Severity B — real defects, low blast radius

### B1. Optional module in `status="error"` is permanently untoggleable, silently `[x — fixed 2026-07-29, plan 1.4]`
The `OnMsg.ApplyModOptions` reconciler excludes `"error"` entries forever
(00_Core.lua:110-111) and logs nothing on the attempt — a dead checkbox until
restart. (`on_activate`/`on_deactivate` failures are also swallowed, :122/:129.)

### B2. F78↔F81 hidden coupling degrades per-fix disable `[x — fixed 2026-07-29, plan 1.5]`
Fix_MeteorStormWedge's pulse-release heal path relies on
Fix_DisasterPredictionLeak's `MeteorStormEnded` handler to clear
`g_DisastersPredicted.DisasterMeteorStorm` (Fix_MeteorStormWedge.lua:142-163 vs
Fix_DisasterPredictionLeak.lua:75-85). With F81 individually disabled, a
pulse-released storm strands the prediction flag — the exact leak F81 fixes.
Only cross-fix functional coupling found in the pack.

### B3. DustSickness pair reports `active` forever if a future patch removes its targets `[x — fixed 2026-07-29, plan 1.2]`
`patch()` returns silently with no data-loaded latch
(Fix_DustSicknessDamage.lua:45-47, Fix_DustSicknessBiorobots.lua:90-99); their
siblings got the latch (Fix_LastTransmissionStorage.lua:96-125). Reporting
integrity only.

### B4. "Every fix can be individually disabled" (metadata.lua:3) oversells `[ ]`
For the 68 default fixes the only surface is `SMRFixPack_Disabled` set BEFORE
mod code loads — realistic via a two-line companion mod on PC, **nonexistent on
Xbox/PS** (no console, no file access, Paradox-Mods-only installs). 00_Core's
header is honest; the storefront sentence is not. Related console reality:
every failure/recovery surface (registry verdicts, `ListFixes()`, "please
report this log", `%AppData%`/Ctrl+F1 instructions in MOD_DESCRIPTION.md
:329-332/:475-481) is log-or-console-only — invisible on console. No fix
*degrades* there (self-deactivation still fails safe); the player just can't
see or steer any of it.

## Severity C — structural, decide deliberately

### C1. 29 of 74 modules are full replacements pinned to build 1.0.7.396349 `[~ accepted risk — mitigations tracked]`
Self-checks are existence/layout checks (the sandbox has no introspection) —
they catch renamed/removed targets, **not** an edited same-named function. After
a game patch that edits those functions in place, the pack silently reinstates
the 1.0.7 bodies — the one lifecycle scenario where a player ends up *worse*
than unmodded, invisible on console. FIX_POLICY §1.5's "keep the list short" is
not met at ~40% of the pack. Mitigations: the after-every-patch extraction-diff
re-verify is a **release gate** (WORKFLOW), and a user-visible "N fixes
deactivated after game update" surface is buildable (engine precedent:
Mod.lua:2231-2243). Merging is not the answer; the risk is inherent to
replacements.

### C2. Duplicated machinery belongs in the core `[~ deferred — Phase 4]`
Quantified: `log()` helper cloned in 11 files + 5 inline variants (6 copies
missing the `%%` escaping 00_Core documents as a crash class, :26-30 — latent);
~154 self-check preflight sites of the same loop shape; status-gate prologue
×20; LoadGame `AllMapsForEach` sweep skeleton ×6; DataLoaded/DataChanged
`patched`-flag scaffold ×6 (only one has the veto check — a shared
`SMRFixPack.DataPatch` runner would fix A1 structurally); global-install
verifier ×7. Candidates: `Require{}`, `WhenActive(id, fn)`, `DataPatch(id,
opts)`, `SetGlobal(name, fn)`, shared watchdog skeleton (hand-rolled twice:
F02, F78).

### C3. Merge candidates `[~ deferred — Phase 4]`
Track-salvage trio F45/F44/F47 (F44 re-implements F45's stamping inline;
F47's logic written in terms of F44's semantics); DustSickness pair (same
scaffold — merging fixes A1 once); weather family F02/F78(/F81) (identical
watchdogs; internalizes B2); F55/F57b (same `unreachable_buildings`
structure). Lander pipeline F67/F68/F69 optional. **No fix found redundant; no
load-order sensitivity beyond core-first; the only same-function double patch
(`GetFuelResourceRequest`: F69 pre-wrap + D01 post-wrap) verified correct in
both orders and under any single disable.**

### C4. Consistency drift + policy gaps `[ ]` (cheap parts in Phase 1/3)
Late files are strictly better (build-stamped provenance, deeper self-checks,
policy citations); lessons never flowed backward: 6 unescaped loggers, early
headers cite "shipped Src 2026-07" instead of the build (F05, F08, F07/F15;
F29 unstamped), Fix_MoraleComfortTooltip.lua:60-64 comment claims return
pass-through the code doesn't do (latent — shipped target returns nothing).
FIX_POLICY is missing its most expensive lessons: the declaring-class
self-check rule (F64), "OnMsg handlers must re-check status AND veto" (A1's
root), an optional-modules section (A2's root), assert/error semantics, a
T()/Untranslated stance, a "reconstruction" category for non-byte-copy
replacements (F03/F04/F09 live in that gap), and the global-replacement
technique rank.

## Severity D — documentation drift (current-state layer)

Verdict: **restructure moderately — the append-only logs are fine (BUGS.md
entries, PLAYTEST_ARCHIVE are *good* bloat); everything that RESTATES a current
fact instead of pointing at it drifted within 24-48 h of being written.**

Concrete drift (all verified):
- **D1** README.md two waves stale: fix table missing ExtenderFlapChurn,
  DisasterPredictionLeak, MeteorStormWedge, RainsDeadlock; optional-modules
  table missing DroneOverhaul + CohortHousing; "73 verified findings" vs 91
  index rows. `[ ]`
- **D2** MOD_DESCRIPTION.md missing the CohortHousing module entirely
  (same-commit-rule violation, never remediated) and claims "**the mod stores
  nothing in your savegame**" — **false** (seven `SMRFixPack_*` persisted
  fields + F35 modifiers; README.md:90-97 has the honest wording). `[ ]`
- **D3** The withdrawn fpk-divergence doctrine still asserted as proven in
  STATUS.md:126-128 and DRONE_OVERHAUL_OPTIONS.md:619-621; stale framing at
  BUGS.md:6 and WORKFLOW.md:33 — the "withdrawn in all four places it lived"
  sweep missed places five and six. `[ ]`
- **D4** F02 tells three stories (index `fixed`, heading "root cause NOT yet
  pinned", reality: pinned to F78/F81 2026-07-29 with wave-6 fixes shipped; no
  cross-ref). D07 heading contradicts its index row (heading says B/D
  confirmed; index says 3-of-5 with A/E owed — index is right). D06 index row
  understates (heading carries the 2026-07-29 null-result verdict). `[ ]`
- **D5** FABLE_NEXT_PROMPT: counts stale ("71 modules, 65/71" → 74/68; "no
  D06/F77 probes" → wave-6 probes exist); read-list points at the wrong
  "newest" STATUS section and disagrees with its own banner; stale session
  sequence (D07 "only exists on disk" — it was live-tested); duplicate PT-53
  board bullets. `[x — fully rewritten 2026-07-29 (audit session): current
  counts, restructured-checklist read-list, audit items on the board,
  opt-module first-enable caveat in the briefing]`
- **D6** Structure: STATUS.md's reference-grade content ("What this project
  is", "Key technical facts") is buried under ~1,300 lines of session legs
  behind a five-deep "Prior wrap" paragraph stack; a stale headline ("47
  tracked defects DONE across 46 registered modules", ~:1042) sits mid-file
  styled as current. WORKFLOW.md describes a dead workflow (lists 3 docs of
  14). TESTING.md is era-2 sediment the live checklist carries a warning label
  about. `[ ]`
- **D7** PLAYTEST_CHECKLIST.md: fossilized preamble (30-fix/wave-3 era), stale
  archive list (missing 11 archived PTs), "all 30"/"all 39" fix counts,
  reporting-protocol step 6 pointing at a STATUS header string that no longer
  exists, group numbering out of order (1,2,4,5,6,8,9,8,10,7). `[x — rewritten
  2026-07-29, this session]`

Hygiene-rule assessment: the two-place status rule held ~90% (23/25 sampled)
but exists only because one fact is stored twice; the same-commit description
rule was violated on back-to-back builds (wave-6 "caught late"; D07 never);
the FABLE_NEXT staleness banner corrected three statements while the counts
rotted underneath it. **Every doctrine-grade fact needs exactly one
authoritative home plus pointers** — that is the structural lesson.

## Platform-readiness checklist

| Item | PDX PC | Steam | Xbox | PS |
|---|---|---|---|---|
| Code sandbox-legal, platform-clean, perf-safe | PASS | PASS | PASS | PASS |
| `lua_revision` 350453 | PASS (exactly the value the tooling writes; shipped LuaRevision 396349 confirmed from Lua.fpk) | PASS | PASS | PASS |
| Mod Options on gamepad | PASS | PASS | PASS (no platform gate; options screen is gamepad-native) | PASS |
| Save-removal safety | PASS (+ set `optional_mod=true` to suppress the missing-mods prompt) | PASS | PASS | PASS |
| `short_description` / `image` / `last_changes` / ModItemCode / ignore_files | FAIL (A3) | FAIL (A3) | FAIL | FAIL |
| Achievement-lockout disclosure | n/a | n/a (not blocked on Steam) | FAIL (A4) | FAIL (A4) |
| Console-appropriate description text | — | — | FAIL (B4) | FAIL (B4) |
| Description accuracy (CohortHousing, savegame claim, DRAFT NOTEs) | FAIL (D2) | FAIL | FAIL | FAIL |
| Fix-deactivation visibility | log-only | log-only | none | none |
| Portal-side console review requirements | — | — | UNKNOWN | UNKNOWN |
| PS pack signatures | — | — | — | PASS (handled by the Paradox pipeline) |

## Unverified (and what it would take)

1. **A2 live confirmation** — enable ClassicRockets mid-session, park a rocket,
   watch fuel requests (one sitting; also re-verifies the Phase-1 fix).
2. **Save → remove-mod → load cycle for the newest fixes** (RainsDeadlock's
   persisted-by-global-name threads, MeteorStormWedge) — one PT-20-shaped cycle.
3. **Paradox Mods portal-side rules for console exposure** — needs the
   portal/publishing docs, not the game source.
4. **Console-hardware performance** — judged statically safe; unverifiable here,
   very unlikely to matter.

---

# REMEDIATION PLAN

Playtesting items are excluded (owner runs those). Phases 1-3 are implemented
by the one-off **docs/AUDIT_FIX_PROMPT.md**; Phase 4 is deliberately deferred
and needs a separate go-decision.

## Phase 1 — code defects (minimal diffs; no refactors; each item independently testable)

- `[x]` **1.1 (A1)** Add the veto re-check (pattern:
  Fix_LastTransmissionStorage.lua:102-106) to `patch()` in
  Fix_DustSicknessDamage, Fix_DustSicknessBiorobots, Fix_IndependenceTerraforming.
  In IndependenceTerraforming, additionally guard the status heal so it never
  overwrites `"disabled"` (heal only an `"inactive"` mislabel).
- `[x]` **1.2 (B3)** Add the data-loaded latch to the DustSickness pair
  (pattern: Fix_LastTransmissionStorage / Fix_IndependenceTerraforming's
  `ever_changed` + DataLoaded bookkeeping): if the target is still absent once
  DataLoaded has fired, flip the entry to `inactive` with a reason string.
- `[x]` **1.3 (A2)** Rework Opt_ClassicRockets (GetFuelResourceRequest wrap),
  Opt_ResidencyControl (CanAcceptNewColonists wrap only), Opt_MultipleSuns
  (SolarPanelBase.GameInit wrap only) to the Opt_DroneOverhaul pattern:
  file-scope install (classdef time, guarded by target-existence checks) +
  per-call `SMRFixPack.IsActive` gate; `apply()` keeps only the self-checks;
  headers updated to describe the real first-enable semantics.
- `[x]` **1.4 (B1)** 00_Core reconciler: on toggle-ON, retry `run_apply` for
  entries in `"error"` (treat like `inactive`+not-installed); log a line
  whenever reconciliation skips or a retry fails, so a dead checkbox is at
  least diagnosable on PC.
- `[x]` **1.5 (B2)** Fix_MeteorStormWedge: after the vanilla-path release
  (heal step "released through the vanilla end path"), clear
  `g_DisastersPredicted.DisasterMeteorStorm` itself if still set — idempotent
  alongside F81, self-sufficient without it.
- `[ ]` **1.6 (C4 cheap parts)** Add `%%` escaping to the 6 unescaped local
  loggers (Fix_DestroyedTunnels.lua:70, Fix_BrokenTrackSalvage.lua:66,
  Fix_DustSicknessDamage.lua:30, Fix_DustSicknessBiorobots.lua:44,
  Fix_GhostFarmOxygen.lua:89, Fix_StaleReservations.lua:96) and the 4
  unescaped inline sites; fix the Fix_MoraleComfortTooltip.lua:60-64 comment
  (or actually pass returns through); add the pinned build number to the
  F05/F08/F07-F15 headers and a stamp to F29.

## Phase 2 — packaging & storefront layer

- `[ ]` **2.1 (A3/B4)** metadata.lua: add `ignore_files` (defaults +
  `*/docs/*`, `*/.claude/*`, `*README.md`, `*.gitignore` — LICENSE ships),
  `short_description`, `last_changes`, `optional_mod = true`; keep
  `lua_revision` (correct as-is); qualify the description's "individually
  disabled" sentence (PC surface only, all six optional modules toggleable
  everywhere via Mod Options); consider `version_major/version_minor`.
- `[ ]` **2.2 (A3)** items.lua: add one `ModItemCode` entry per `Code/` file,
  in EXACTLY the current metadata.lua `code` order (00_Core first,
  90_SaveSanitizer before the Opt_ block), so an editor round-trip regenerates
  the same list. Verify names/order against metadata.lua:20-97 after writing.
- `[ ]` **2.3 (A4/B4/D2)** MOD_DESCRIPTION.md: add the CohortHousing module
  block; replace the "stores nothing in your savegame" claim with README's
  honest wording; add the console achievements disclosure (Xbox/PS/MS Store);
  add console-appropriate variants for per-fix disable honesty and bug
  reporting (no %AppData%, no console commands).
- `[ ]` **2.4 (D1)** README.md: sync the fix table (4 missing), the
  optional-modules table (2 missing) and the findings count.
- `[ ]` **2.5 — OWNER TASKS (not for the implementing session):** thumbnail
  image (PDX ≤2 MB / Steam ≤1 MB), screenshots, check Paradox Mods portal
  rules for console publishing.

## Phase 3 — documentation

- `[ ]` **3.1 (D3/D4/D5)** Mechanical drift fixes: F02 index+heading updated
  with the F78/F81 resolution + cross-refs; D07 heading matched to its index
  row; D06 index row carries the null-result pointer; the two un-withdrawn
  fpk-doctrine copies (STATUS.md:126-128, DRONE_OVERHAUL_OPTIONS.md:619-621)
  corrected + stale framing at BUGS.md:6 and WORKFLOW.md:33 pointed at the
  parity proof. (FABLE_NEXT_PROMPT is already DONE — rewritten 2026-07-29 in
  the audit session; do not re-edit it here except to update its read-list
  pointers after 3.2/3.3 move things.)
- `[ ]` **3.2 (D6)** Extract STATUS.md "Key technical facts" into
  `docs/ENGINE_FACTS.md` (sole authoritative home; STATUS keeps a one-line
  pointer; update the readers: FABLE_NEXT read-list, checklist references).
- `[ ]` **3.3 (D6)** STATUS.md: replace the "Prior wrap" paragraph stack with
  a ~40-line rewritten-in-place current-state header (build counts — stated
  here and NOWHERE else — open user decisions, next gates, pointer to newest
  leg); move the session legs + superseded A/B tables to
  `docs/archive/SESSION_LOG.md` (append-only, newest first); delete the stale
  mid-file headline.
- `[ ]` **3.4 (D6)** Archive sediment to `docs/archive/`:
  ChatGPT-deep-research-report.md, RESEARCH.md (promote its §3 unpromoted
  leads to C-rows in BUGS.md first), TESTING.md (move the four-kinds probe
  table to the TestKit first), CHEATS_INVENTORY.md (fold anything not already
  in the checklist's verified table).
- `[ ]` **3.5 (D6)** Rewrite WORKFLOW.md: keep the true mechanics (junction/
  install, fpk extraction-diff verification as a release gate, release steps),
  point at ENGINE_FACTS/STATUS/BUGS as the reading path, drop the dead
  discovery-era loop.
- `[ ]` **3.6 (C4)** FIX_POLICY.md additions: declaring-class self-check rule;
  OnMsg handlers re-check status AND veto; optional-modules section
  (file-scope install + per-call gate, on_activate/on_deactivate contract);
  assert/error report-and-continue semantics; T()/Untranslated stance;
  "reconstruction" replacement category; global-function replacement as its
  own technique rank; console-platform constraints note.
- `[ ]` **3.7 (D4 prevention)** Slim BUGS.md index rows to
  `status + date + PT ref` (result prose lives in the entry; heading tag
  stays the summary) — mechanical, one pass.

## Phase 4 — DEFERRED (separate go-decision; touches tested code mid-playtest)

- `[~]` Core helper extraction (C2): `DataPatch` runner, `Require`,
  `WhenActive`, `SetGlobal`, shared watchdog.
- `[~]` Module merges (C3): track-salvage trio, DustSickness pair, weather
  family, F55/F57b.
- `[~]` User-visible deactivation surface (C1): "N fixes deactivated after a
  game update" pregame notice.
- `[~]` Early-file self-check deepening beyond 1.6 (C4).

Rationale for deferral: all four change code that is probe-verified and
partially play-verified; the defect fixes above are minimal diffs, these are
restructures. Best window: after the current playtest wave, before release
packaging.
