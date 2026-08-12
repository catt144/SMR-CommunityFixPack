# Chain — split-optins (the standalone opt-in mod; 5 prompts, self-consuming)

**Why this chain exists.** Owner order 2026-08-12 (checklist item 15, then
sharpened same session): *"I want the opt in to be a true standalone mod, so it
can work with or without the bug fix mod… I want a very good and cautious chain
for that. Split it, make sure all our hard fault work makes it over on it as
well like engine, fix, documentation policies ect. When I work on it, i want to
be able to cleanly load its folders and just work on it instead of having to
retrain the system."*

Three owner requirements, each a first-class deliverable:

1. **TRUE STANDALONE** — the opt-in mod loads, registers and functions with the
   fix pack ABSENT, and cleanly beside it when both are installed.
2. **The institutional discipline carries over** — engine facts, FIX_POLICY,
   WORKFLOW, doc conventions, doccheck tooling, probe hygiene.
3. **NO RETRAINING** — a fresh agent session opened in the new repo is
   productive immediately from that repo's own docs, without this repo.

**Sequencing (owner-ruled, checklist 15):** this chain runs BEFORE the D13
chain — D13's exposed-set derivation must see the FINAL module sets of both
mods, or it is done twice. `unattended-3` (F85+C39) may run in parallel; it
touches only core fixes.

## What is being split (verified 2026-08-12, this authoring session)

* The 8 `optional = true` files: `Code/Opt_ClassicRockets.lua` ·
  `Opt_AcknowledgedWarnings.lua` · `Opt_ResidencyControl.lua` ·
  `Opt_MultipleSuns.lua` · `Opt_DroneOverhaul.lua` · `Opt_CohortHousing.lua` ·
  `Opt_NoHomeless.lua` · `Opt_DroneStatDials.lua`.
* Their framework is ONE file, `Code/00_Core.lua` (504 lines): the
  `SMRFixPack` global carrying `defs`/`fixes` + `Log · IsActive ·
  OptionEnabled · PackVersion · Require · SetGlobal · WhenActive · DataPatch ·
  OnDataReady · Register · UpdateSuspects · ListFixes`. Measured usage by the
  8 Opt files: `IsActive ×13 · Register ×8 · OptionEnabled ×7 · SetGlobal ×5 ·
  ListFixes ×5 · Require ×5 · WhenActive ×3 · fixes ×3 · OnDataReady ×2 ·
  Log ×1`, plus DroneOverhaul's own `DroneReport`/`DroneOverhaulStats` surface.
* Options plumbing: `metadata.lua` `default_options` (6 toggles all `false` +
  2 D09 dial STRINGS, byte-identical to `items.lua` and
  `Opt_DroneStatDials.lua`'s maps — the comment cites `Mod.lua:473-475`,
  engine seeds `CurrentModOptions` from it before mod code loads) +
  `items.lua` `ModItemOptionToggle`/`Choice` entries + the `Code/Opt_*` file
  list at `metadata.lua:125-132`.
* TestKit (separate local-only repo): the 8 modules' probes + `OptionsMenu`
  (expects `default_options + 6 toggles + 2 D09 dials` in ONE place today).

## Binding chain rules

1. **Staleness check first, every prompt**: `git log --oneline -10` +
   `git pull` in THIS repo; same in the new repo once it exists; TestKit tree
   status too. A live todo list, updated per item (owner reads it to decide
   when to step in).
2. **Inbox/outbox in writing**; each prompt appends to the next prompt's
   `## Notes from upstream`, commits, deletes its own file in the same commit.
   Folder emptiness is prompt 5's done-condition.
3. **Recorded facts are claims** — including everything in this README and
   every number above. Re-derive the ROUTE from Src/code, not just citations.
4. **Self-split at a clean commit boundary** if context runs short. Route,
   don't drop; unsure who owns a discovery → STOP AND ASK.
5. **WORKFLOW binds in full** — all harness-rule stacks, probe hygiene
   (parked .txt instruments, ARM gate, PROBE SWEEP line, R8 `git add -f`
   logs), EF-047 (absence only from archived logs) · EF-048
   (truthiness/type) · EF-049 (save witness = disk bytes + load-back) ·
   EF-050 (savename VERBATIM). PS 5.1 hazards (no-BOM UTF-8 via Edit tool /
   `[System.IO.File]`; commits via `git commit -F <file>`); parse sweep
   before any commit touching Lua; doccheck green in EVERY repo it exists in
   before any doc commit; push what has a remote.
6. **⛔⛔ THE STANDALONE INVARIANTS (this chain's constitution):**
   * **(a) Fix-pack-absent:** the new mod contains ZERO references to
     `SMRFixPack` in executable code — its framework is a full copy under its
     OWN global (working name `SMROptInPack`; log prefix
     `[CommunityOptInPack]`). No cross-mod `Require`, no load-order
     assumption, no shared file.
   * **(b) Both-installed:** no global-namespace collision, no vanilla patch
     point owned by both mods (design job 1 proves the disjointness or stops
     the chain), two separate Mod Options pages, log prefixes distinguishable
     at a glance.
   * **(c) ⛔⛔ PERSISTED NAMES ARE SAVE CONTRACT.** Any string that ever
     entered a savegame — modifier ids (D09 dials, F35-class), instance
     fields, GameVars, thread names — keeps its EXACT bytes regardless of the
     code's new namespace. Renaming a persisted id is FORBIDDEN in this chain
     (it would need a migration heal + D13 coordination — Out of scope).
     Design inventories every persisted name; QA audits this hardest; verify
     witnesses it on a real save.
   * **(d) Byte-conservative port:** module BEHAVIOUR does not change. The
     only edits are namespace strings, registration glue, and file location.
     `Opt_DroneOverhaul` carries PT-52's freeze with it — frozen it stays.
   * **(e) The fix pack still stands afterwards:** its counts are re-derived
     (expected 74 registered / 74 files + Core & sanitizer = 75 `Code/*.lua`,
     but DERIVE, never assume), its suite passes, doccheck green.
7. **Doc migration policy:** the 8 modules' bug/design entries MOVE to the
   new repo's `docs/agent/bugs/` (fix-pack side keeps a one-line tombstone
   row pointing across — INDEX stays generated, edit entries only);
   `docs/agent/facts/` is COPIED WHOLE (engine facts describe the game, both
   repos need them; divergence is accepted and dated from the copy);
   FIX_POLICY + WORKFLOW + CHAIN_METHOD are ADAPTED copies (pack-specific
   clauses rewritten, nothing silently dropped — a clause that does not apply
   is kept and marked N/A rather than deleted); `tools/doccheck.py` + hooks
   ported and configured (`git config core.hooksPath tools/hooks`).
   `docs/archive/` here is append-only and does NOT move — history stays
   where it happened.
8. **The no-retraining acceptance test (owner requirement 3):** prompt 5 must
   answer, from the NEW repo alone with this repo closed: where is build
   state? what are the policies? what does each module do and what is its
   defect/feature record? how do I run the suite? what is banned (persisted
   renames, behaviour changes)? what came from where (provenance page)? If
   any answer needs this repo, the scaffolding is incomplete — fix before
   close.
9. **Owner decisions routed, nothing blocked on them:** the mod's DISPLAY
   NAME + store description (launch prep, joins the wording items); GitHub
   remote for the new repo (until then it is a local git repo — do NOT
   create a public remote unasked); ⚠️ changing the mod id resets Mod Options
   account state — the owner re-ticks their toggles ONCE after the split
   (say so in the report, cost ~1 minute in-game).
10. **Steam Cloud rule inherits (EF-051 HOLD):** any staged save used by
    prompt 4 records "deleted, listing verified", never "gone"; a returning
    stray is the owner-armed mechanism, not a finding. Protected files: the
    four standing MD5s (see corun-pt60 close, SESSION_LOG 08-12) — this chain
    should not need to touch any save it did not stage; `CP15PT15` is a KEPT
    save (copy only).
11. **Model placement:** prompts 1/3/4 = Opus executes; prompts 2/5 = Fable
    (fresh-context QA gate; terminal audit). Bodies are model-neutral.

## Scope fence — the whole chain

**In:** the split itself; the framework copy under the new namespace; metadata/
items/default_options on both sides; TestKit taught to serve both registries;
doc + tooling + policy port; new-repo scaffolding (CLAUDE.md, STATE, WORKFLOW,
FIX_POLICY, bugs, facts, README map, memory conventions); baseline
re-derivation (gate reads, suite tallies, doccheck counts, both repos); the
three-cell verification matrix + save-compat witness; junction install for the
new mod.
**Out:** ANY behaviour change to any module; renaming ANY persisted string;
D13 (next chain); `unattended-3`'s content; new features; publishing/remotes;
re-testing anything the freeze (checklist 14) already closed; changing owner
decisions.

## Stop conditions (chain-wide)

- The coupling map finds shared state that cannot be duplicated (a vanilla
  patch point both mods would own, or cross-module runtime dependency between
  a Fix_ and an Opt_) → STOP, route to the owner with the exact site.
- Prompt 2's QA verdict is NOT "build" → back to design; prompt 3 may not run
  on a rejected design.
- Any verification-matrix cell shows cross-mod interference or a persisted-id
  break → stop that leg, record verbatim, keep independent legs, route.
- Any `[LUA ERROR]` naming either mod's code → stop that leg, record, route.
- Context runs short → self-split at a clean commit boundary (rule 4).

## Manifest

| # | file | owner needed? | what it does |
|---|------|---------------|--------------|
| 1 | `01_OPUS_DESIGN.md` | No — game closed | authoritative coupling map · persisted-name inventory · namespace/repo/options/TestKit design · doc-migration inventory · scaffolding spec · verification-matrix design. Outbox = prompt 2's Notes |
| 2 | `02_FABLE_QA.md` | No | fresh-context ADVERSARIAL review of the design; verdict gates the build |
| 3 | `03_OPUS_BUILD.md` | No — game closed | execute the split in both repos + TestKit; parse sweep; doccheck green ×2; no launch |
| 4 | `04_OPUS_VERIFY.md` | No at keyboard (game/Steam must be free; unattended-harness launches) | the three-cell matrix + save-compat witness; logs archived |
| 5 | `05_FABLE_AUDIT.md` | No (routes decisions) | byte-compare + whole-log read · re-derive every matrix verdict · no-retraining acceptance test · integrate both repos · folder EMPTY · kickoff = D13 chain |
