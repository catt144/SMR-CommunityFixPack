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
- **The designated experiment save is `TEST2H TRAIN`** (owner, 2026-08-04) —
  the large multihop line with underground track. Prompt 1 VALIDATES it
  against the skeleton's needs instead of routing the choice; if it lacks
  something a payload item requires, route the gap, not a new choice. All
  runs stage a COPY; the save itself is never written.

## Manifest

| # | file | model | owner needed? | what it drains |
|---|------|-------|---------------|----------------|
| 1 | ✅ DONE 2026-08-04 (file consumed; output = `CORUN_RIG_SPEC.md`) | Fable | No (schedule ask routed to checklist) | Delivered: inventory (11 PROVEN / 8 Src-verified / 6 UNKNOWN, §1); envelope (§2); risks + effort (§3); tier DRAFT + card template (§4); co-run #0 definition (§5); `TEST2H TRAIN` validated on disk, gaps routed (§6). No stop condition tripped: the skeleton rests on nothing outside the bins, and owner time stays ~10 min |
| 2 | ✅ DONE 2026-08-04 (file consumed; output = `CORUN_RIG_SPEC.md` §8) | Opus | **YES — asked for ~10 min, used ~1.5** | ⛔ KILL-GATE **PASSED WITH CORRECTIONS**, chain continues. U1 ran end to end first try; U2 = **9,968 ms** load, whole cycle **79.9 s**; U3 = no picker; U4 = §6 read (F11 + C41 GO, hex/F99 gapped on 0 broken track). S1/S2/S4/S5/S7 → PROVEN. 5 corrections (C1 `RealTime()` lies across loads → `facts/EF-045`; C2 the ride-along verdict table is cross-map-only; C3 the readiness poll is redundant; C4 a loaded save arrives PAUSED; C5 doccheck vs probe hygiene). F11 same-map path measured, cross-map still open. Log archived |
| 3 | ✅ DONE 2026-08-04 (file consumed; outputs = `CORUN1_BRIEF.md`, `agent/reports/CORUN1_EVIDENCE_CARDS.md`, `CORUN_RIG_SPEC.md` §9) | Opus | **YES — asked ~15–20 min, used ~6.5** | Co-run #1 **RAN THREE TIMES** (398 s + 85 s + 64 s cycles, each authored from the previous one's gaps, all in one sitting). ⭐ **F11 cross-map route SETTLED — route (a)**, the one the entry called unprovable from Lua. ⭐ **F99 hex tie-break MEASURED** — returns the hidden element. ⭐ **C41's M5 lead MEASURED** and **both** clamps shown guilty for an out-of-range anchor — run 3 reproduced a pre-registered corner box to the pixel, at the owner's insistence after I recorded it as *refuted* when it was merely *unsampled*; ⛔ picker appeared 52/52, OG symptom unreproduced, `cand` unchanged. ⚖️ **F11 pre-wrapper rider: 2 of 3 readings pass**, `tested` NOT claimed, close-decision routed. ⚖️ **The armed-prep override was DECLINED** and replaced by a measurement (arming costs 0.4 s) — rule 5 stands. 6 spec corrections (C6–C11). All three probes deleted, all three logs archived |
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
