# Project prompt chain — run in filename order, delete as you go

**Created 2026-08-01 (owner direction). This folder is a self-consuming queue:
when it is empty except this README and the final QA prompt, the project work
between the bug-list audit and the F86 adjudication is DONE and the owner is
free to playtest.** The final QA prompt deletes this README and itself last.

Design rule (owner, 2026-08-01): **many focused prompts over few big ones** —
each prompt is sized to finish comfortably in one session's context, and
nothing is left hanging between sessions except through the written inbox
mechanism below.

## The chain

| # | file | model | owner needed? | what it drains |
|---|------|-------|---------------|----------------|
| 0 | ~~`0_harness_gate_and_probe_teardown_opus.md`~~ **✅ DONE 2026-08-01, file consumed** | Opus | — | owed F49-strip A/B code-gate leg (RAN CLEAR: `68/74` → `63/0/15/0`) · stale probe `99` teardown (deleted; sweep now returns one declared hit, `97`) |
| 1 | ~~`1_playtest_reorg_and_policy_sweep_opus.md`~~ **✅ DONE 2026-08-01, file consumed** | Opus | — (the §4 adoption needed no ask — blanket pre-clearance) | PT-54 retired unrun (C/D/E → Tier-1 legs; **A/B not absorbed → routed to prompt 3**) · four new checklist riders (F35, C32, F80, F82) · F74 rider merged into F53(a)'s · **FIX_POLICY §4 amendment APPLIED** (activates one owner decision on F29/F57(a) → **routed to prompt 7**) · MOD_DESCRIPTION community-standing facts (one conditional → **prompt 4**) · BUGS/STATUS consistency sweep (100 index rows agree with their heading tags; counts re-derived) |
| 2 | ~~`2_f86_phase0_measurements_opus.md`~~ **✅ DONE 2026-08-01, file consumed** | Opus | — (one sitting, spent) | both F86 engine measurements, log `Mars.exe-20260801-14.59.57`: **GT creation DEFERS** (measured twice, incl. GT-creates-GT with a live `WaitMsg` receipt → **rains takes the wrapper shape; F02's falsy guard is not load-bearing, kept as defence in depth**) · **autosave hook FIRES** (`autosave=true err=false`, console-forced via the engine's own `Autosave`) · probe `97` torn down — **the stale-probe sweep now returns ZERO hits in both repos** · TestKit `99_FixtureCarry` repair committed |
| 3 | ~~`3_f86_phase1_tier1_spec_fable.md`~~ **✅ DONE 2026-08-01, file consumed** | Fable | — | final Tier-1 spec = `SAVE_SAFETY_REDESIGN.md` **§6.2a** (C34 rider rides the rains pass; **mid-session F81a reconcile TAKEN**; StormWedgeHeal reorder specced) · enumeration re-derived: **exactly 13** (+1 inert route-(c) site — no non-compliant 14th) · **adjudication §4.4 CLOSED** (closure enters saves via `likes_data`→GameVar, inert) · `F86_TIER1_BUILD_PROMPT.md` written (5 legs incl. PT-54 A/B reshaped) |
| 4 | ~~`4_f86_phase2_tier1_build_fable.md`~~ **SPLIT 2026-08-01 (rule 3), file consumed** | Fable | — (legs 1-4 RUN with owner) | Tier-1 BUILT (4 units + probe realign, `d899a54..a9d68e3`; TestKit thru `49b40da`) · **legs 1-4 PASSED on log evidence** (ledger in 4b) · F89 filed mid-leg · leg-3 id-less clause amended (owner-cleared) |
| 4b | ~~`4b_f86_phase2_tier1_close_opus.md`~~ **✅ DONE 2026-08-01, file consumed** | Opus | — (leg 5 run with owner) | **TIER 1 VERIFIED — all five legs run** (`c6180ad`; logs `Mars.exe-20260801-16.42.31`/`-17.11.08`/`-19.14.11`, test-2 lineage) · **F02/F78/F81/F88 → `tested`** (row + tag both) · C34 rider verified · PT-54 absorption table marked RUN (C/D/E + the carried A/B as leg 4) · STATUS F86 rewritten to post-Tier-1 truth · **leg 5 read Tier-1 CLEAN** (`Meteors`/`MeteorStorm` alive on vanilla bodies, zero Tier-1-named lines, residue below the allowed list) **but surfaced F86 Site 2 still leaking — 80 `Opt_DroneOverhaul` orphan errors, owner-ruled out of scope → routed to prompt 5** · **MOD_DESCRIPTION no-precedent sentence NOT published** (unsoftened; its gate corrected from Tier 1 to Tier 2) · consumed `F86_TIER1_BUILD_PROMPT.md` + itself |
| 5 | ~~`5_f86_phase3_tier2_build_opus.md`~~ **SPLIT 2026-08-01 (rule 3), file consumed** | Opus | — (builds needed none) | **TIER 2 BUILT** (`88f3154`, `44e6af2`, `6f0cb95`, `ef7d49c`, `e197190`; TestKit `6eb3c0b`, `7bfa274`) — all four modules moved off their blocking bodies onto verified-synchronous seams, **F86 Site 2 repaired**, **the `ArrivalDeaths`(a) design pass RUN and it found a route** (so it was built, not deferred; nothing routed to prompt 12) · per-site dispositions recorded for all five sites · F21 **downgraded `tested`→`fixed`** (PT-43 measured a retired body) · three probes realigned off replaced behaviour, sweep clean · **PT-58 written with predictions P1-P7 BEFORE any run** · ⚠️ **the leg is UNRUN, so the D10/D12 unhold is NOT recorded** → 5b |
| 5b | `5b_f86_phase3_tier2_leg_opus.md` | Opus | **launch leg** | run PT-58 · record it · the flips it earns · **D10/D12 unhold** (gated on it) · the MOD_DESCRIPTION no-precedent unlock (gated on a clean uninstall read) |
| 6 | `6_audit_candidate_sweeps_opus.md` | Opus | no | verification reading: C32 (incl. already-patched-in-1.0.7 check), C04 call chain, F35 scope, fredware #11 comparison · owner web-check reminders |
| 6b | `6b_residual_candidate_sweeps_opus.md` | Opus | no | the rest of the C-ledger: C18-C21 evidence prep, C25 mechanism limits, C26-C30 Relaunched-presence checks, F82 trace, F80 source-audit (pre-cleared work) |
| 7 | `7_audit_candidate_decisions_opus.md` | Opus | review only | decision packages: C33 (+F44 shell amendment), C22, C23, C24 + everything 6/6b promoted — each through the §4 bar; **passing packages are PRE-CLEARED to build (blanket above)**; failing ones close honestly |
| 8 | `8_f86_phase4_conversion_batch_opus.md` | Opus | launch leg | the six §5.4-A wrapper conversions + every prompt-7-approved fix, ONE leg |
| 9 | `9_d10_workshops_build_opus.md` | Opus | decision (F84) + launch leg | D10 build (carries the bundled F84 text decision, adds PT-57) |
| 10 | `10_d12_no_homeless_build_opus.md` | Opus | launch leg | D12 build, own A/B, never entangled with D10 |
| 11 | `11_f76_depot_picker_repair_opus.md` | Opus | attended sitting | the F76 P1 depot-picker repair (its own dedicated sitting) |
| 12 | `12_final_qa_backward_check_fable.md` | **Fable** | review | backward QA over everything: notes consumed, docs consistent, nothing owed/missed/wrong; writes the QA report; **then (job 7, owner-requested 2026-08-01) the documentation structure review — assess every doc the agents read/maintain and recommend how to stop the recurring drift; `DOC_STRUCTURE_REVIEW.md`, recommendations only**; empties this folder |

Model routing lives in the FILENAME only — prompt bodies are model-neutral
(project rule). Order is strict through 8; prompts 9-11 are independent of
each other and may run in any order after their gates open (9/10 after **5b**
verifies — prompt 5 built the repairs but did not run their leg; 11 anytime
after 1). 12 runs last, when the folder holds only it
and this README.

## ⭐ Owner blanket pre-clearance (2026-08-01, recorded verbatim in intent)

The owner cleared, in advance and "regardless of flags", **all work items
derived from the 2026-08-01 audit-and-adjudication conversation** that the
chain's author judged appropriate. Scope and limits, stated precisely:

- **What it clears:** the approval STEP on items already evidenced in that
  conversation — the §4 amendment adoption (prompt 1), the
  `Opt_DroneOverhaul` carve-out (prompt 5), building the audit's verified
  candidates when their own §4 package passes (prompts 6b/7/8), and the
  residual-candidate sweeps (prompt 6b).
- **What it does NOT clear:** the EVIDENCE bars — a package that fails its
  own intent/reachability/§4a test still does not ship (the clearance
  removes the ask, not the bar); anything the owner previously REJECTED
  outright (e.g. the C1 wording fallback) stays rejected; NEW scope that
  did not come from that conversation still stops and asks (rule 2 below).

## Chain mechanics (binding for every prompt here)

1. **Inbox/outbox.** Each prompt ends with a `## Notes from upstream` section.
   On completion, a session APPENDS its handoff notes to the NEXT prompt's
   `## Notes from upstream` (or to whichever later prompt actually owns a
   discovered item), commits, then **deletes its own file in the same commit**.
2. **Discovered work is routed, not dropped.** New owner-work found mid-prompt:
   decide WHICH later prompt owns it and WHEN it must happen, append it there
   with one line of reasoning. **Unsure which prompt owns it → STOP AND ASK
   the owner** — never guess a route, never silently expand your own scope.
3. **Self-split on context pressure (owner rule).** If a session judges the
   remaining work might not fit its context, it STOPS at a clean commit
   boundary, writes a continuation prompt (same number + letter suffix, e.g.
   `5b_…_opus.md`) carrying precise state + remaining units, commits, and
   ends. A continuation prompt is a normal chain member. Never push a job to
   the edge of a context window.
4. **New defects:** file in `BUGS.md` (never here, never FUTURE_IDEAS), then
   route any follow-up per rule 2.
5. **Every prompt obeys `WORKFLOW.md` "Authoring a prompt" elements 1-7**:
   live todo list (one item per commit-and-verify unit), `git log`+`git pull`
   staleness check first, scope fence, stop conditions, what-may-not-be-
   claimed, self-deletion, and the stale-probe gate before ANY test.
6. Commit convention:
   `git -c user.name="SMR-BugFixPack" -c user.email="154917955+catt144@users.noreply.github.com"`,
   messages via `git commit -F <file>` (no embedded double quotes), push the
   fix pack (TestKit stays local-only).
7. **STATUS.md is updated by every session that changes counts or state** —
   counts live there and nowhere else.

## Deliberately NOT in this chain (recorded so QA doesn't flag them)

- **The drone track** (D06 rebuild, D08, drone playtests, cleanup mod):
  owned by `docs/prompts/DRONE_PROJECT_PROMPT.md`; its design decision is a
  standing owner decision. PT-52 A/B/B2 stay frozen.
- **D13 (uninstall procedure + standalone cleaner)**: its own spec gate
  forbids speccing before Tier 1/2 land AND verify, and it is release-phase
  work — it comes AFTER the playtest campaign, before release. Prompt 12
  carries it forward as the standing next item.
  ⭐ **Clarified 2026-08-01 (owner): D13 is a HARD LAUNCH DEPENDENCY — "we
  won't launch till it does."** Its absence from this chain is a *sequencing*
  fact, not a deprioritisation: the cleaner's target list is the OUTPUT of the
  builds, so it cannot be designed until they are done. **The corollary binds
  every prompt here: build every reachable repair NOW, and never defer a site
  to the cleaner as a way to descope** — a cleaner hand-off is a valid
  disposition only *after* the in-pack attempt has been made and the route
  proven absent (FIX_POLICY §3a).
- **The playtest campaign itself** (PT-53, needs-eyes riders, the PT backlog):
  that is what the owner is freed FOR; prompt 1 leaves the checklist current.
- **Pack split / D11 / C1 wording fallback / FUTURE_IDEAS**: undecided or
  parked by explicit owner rule — not work.
