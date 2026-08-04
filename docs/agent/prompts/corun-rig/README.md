# Chain — the co-run rig (4 prompts, self-consuming)

**Why this chain exists.** Co-runs were adopted 2026-08-04 (`WORKFLOW.md`
"Co-runs"): attended experiment legs where the agent drives the game and the
owner is on call, not on duty. Nothing has BUILT the rig. The owner's explicit
worry is **a hasty plan that needs 3 days of rework to get working** — so this
chain is designed around a kill-gate: the smallest possible end-to-end proof
runs before anything ambitious is built on it.

**Owner decisions on the record (2026-08-04):**

- **GO**, with the recommended model placement (Fable on 1+4, Opus on 2+3 —
  §4.0 owner call at ≤5 prompts). Placement lives in the filenames; bodies are
  model-neutral, re-route by renaming.
- **Scope addition, owner request:** design **sign-off tiers**. Today every
  ship needs owner sign-off, but for log-only defects the owner never sees the
  bug OR the fix — they flush logs and trust the agent's reading, which makes
  the sign-off ceremony. Wanted: some tests need no per-item sign-off; others
  get a compact **evidence card** the owner can quick-read and OK. Prompt 1
  drafts the tiers, prompt 4 finalizes and ROUTES them (they change the
  `tested` policy, which is the owner's, not ours).
- **The designated experiment save is NOT yet chosen** — prompt 1 routes that
  choice with a recommendation (what the save must contain).

## Manifest

| # | file | model | owner needed? | what it drains |
|---|------|-------|---------------|----------------|
| 1 | `01_FABLE_RIG_SPEC.md` | Fable | No (routes decisions out) | Feasibility inventory vs. EXECUTED-ONCE provenance; capability envelope; risk register + effort model; sign-off tier draft + evidence-card template; defines co-run #0; writes `CORUN_RIG_SPEC.md` |
| 2 | `02_OPUS_SKELETON_RUN.md` | Opus | **YES, ~10 min** | Co-run #0: the walking skeleton. ⛔ KILL-GATE — fails or overruns → chain STOPS and routes findings |
| 3 | `03_OPUS_PAYLOAD_RUN.md` | Opus | **YES, ~15–20 min** | Co-run #1: drains the tagged riders (F11 watch · hex tie-break · C41 loop · Done-timing if not done in #0); produces the first evidence cards |
| 4 | `04_FABLE_QA_AND_INTEGRATION.md` | Fable | No (routes the tier decision) | Adversarial audit of rig + results + ECONOMICS (did it save owner time?); finalizes+routes sign-off tiers; integrates the spec into WORKFLOW/PLAYTEST_HELP; CHAIN_METHOD lessons; empties this folder |

## Binding chain rules

1. **Staleness check first, every prompt**: `git log --oneline -10` +
   `git pull`. No sealed documents in this chain, so subject lines are fine.
2. **Inbox/outbox in writing.** A prompt ends by appending its handoff to the
   NEXT prompt's `## Notes from upstream`, committing, and deleting its own
   file in the same commit. The folder's emptiness is the done-condition,
   owned by prompt 4.
3. **Route, don't drop** — discoveries this chain does not own go to
   `agent/bugs/` or the checklist as riders (TAKEABLE WHEN / TAKEABLE IN a
   co-run). Unsure who owns it → STOP AND ASK.
4. **Self-split at a clean commit boundary** if context runs short; the
   continuation gets its own manifest row.
5. **Drift-evidence capture** — every disagreement with the record is appended,
   never silently fixed.
6. **The record is a claim too — re-derive the ROUTE, not just citations.**
7. **WORKFLOW elements 1–8 bind**, including the live todo list (the owner
   reads it to time their involvement — for prompts 2/3 it is also how they
   know when to sit down) and the declared read path.
8. **FIX_POLICY §3a binds all game runs**: staged COPY of the designated save,
   never the campaign save. **The probe-hygiene hard gate binds prompts 2/3**
   (sweep before, `PROBE SWEEP:` line in result commits, probes deleted in the
   commit that records their answer).
9. **`python tools/doccheck.py` green before every doc commit**; STATE.md
   60-line cap — adding means evicting in the same commit. Commits via
   `git commit -F <file>`; parse sweep (python + luaparser, `utf-8-sig`)
   before any commit touching Lua. Push.
10. **⛔ NO ASSUMED CAPABILITY (this chain's own rule).** Nothing may be
    planned on a primitive that is neither EXECUTED-ONCE in the record nor
    verified in Src AND flagged for proof in co-run #0. "It should work" is
    the hasty plan the owner is worried about, written down.
11. **⛔ The forced-vs-organic rule** (`WORKFLOW.md` Co-runs): force upstream
    conditions, never the measured path; every finding names what was forced.
    Forced repro is MECHANISM evidence; organic sightings still own upgrades.

## Scope fence — the whole chain

**In:** the co-run rig (launch, save staging, scenario scripts, amplification,
log round-trip, watchdog/abort); the capability envelope; the effort model;
the sign-off tiers + evidence-card template; the four tagged first candidates;
integration of all of it into the doc flow.

**Out:** building any new bug fix (file, don't fix); F99's fix itself; D12,
PT-62, drone work; changing the `tested` policy unilaterally (prompt 4 ROUTES
it); MarsDebug un-attended automation (modal assert dialogs make debug-build
legs attended BY CONSTRUCTION — record it as an envelope limit, do not fight
it).
