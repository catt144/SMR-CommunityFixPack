# Chain 1 — playtest reorganisation + the §4 amendment decision + doc consistency sweep

**One-off; delete this file in your final commit. Read `README.md` in this
folder first.** Model-neutral body. Game-free — do not launch the game, do
not modify `Code/`.

**Staleness check: `git log --oneline -10` + `git pull`.** Written 2026-08-01
after the bug-list audit (`docs/reports/BUG_LIST_AUDIT.md` — read its §1, §2.4
and §9 before editing anything; it is the evidence base for every change
below).

## Jobs (todo list first; one item per commit-and-verify unit)

### A. Playtest reorganisation (`docs/PLAYTEST_CHECKLIST.md`, protocol intact)

1. **Retire PT-54 as written.** It tests the current
   `Fix_MeteorStormWedge`/`Fix_RainsDeadlock`/`Fix_MeteorFrequency` bodies,
   which chain prompt 4 (F86 Tier 1) deletes and replaces; its intent is
   absorbed by that build's own legs (A/B + F88 load-3× regression +
   PT-20-method uninstall). Record the retirement in the checklist AND on the
   BUGS F78/F81 entries ("PT-54 retired 2026-08-01 → verification rides the
   Tier-1 build leg"), so no session re-runs it against doomed code.
2. **Add cheap riders to the needs-eyes list (§6):**
   - **F35 live-label check** — one console read in any colony: does
     Frictionless Composites' modifier reach `LargeWindTurbine` in a CURRENT
     game? Decides whether our old-save fixup under-scopes (audit §2.2 F35
     flag). Cite the audit's witness thread on the rider.
   - **C32 label-membership read** — after visiting and leaving an asteroid:
     is every `ShiftsBuilding` still in `UIColony.labels.ShiftsBuilding`?
     (BUGS C32; one console line; pairs with any asteroid sitting.)
   - **F80 settling observation** — the boarding-skip forensics on the F80
     entry name the suspected walk-direction mechanism; add the controlled
     observation as a rider on any train sitting.
   - **F82 timing observation** — one timed watch of the split-grid
     notification clearing (entry has the owner's verbatim report).
3. **Downsize the F74 rider** — the audit found a 1.0.7 dev note + an
   independent Relaunched fix (fredware #10) corroborating it; the rider's
   remaining value is the fresh never-modded-colony check it shares with
   F53(a). Merge them into one item if the checklist still lists them apart.
4. **Verify checklist/HELP cross-references still hold** after the edits
   (the split rule: tests in CHECKLIST, reference in HELP).

### B. The FIX_POLICY §4 amendment — present for decision

The drafted replacement §4 (end of `docs/reports/REACHABILITY_AUDIT.md`,
"Revised FIX_POLICY §4 amendment") was blocked on the F49(a) R4-ships
contradiction. **That blocker died 2026-08-01** — the guard is stripped
(BUGS F49 entry). Present the amendment to the owner as a yes/no:
- **Yes** → apply the drafted text into `FIX_POLICY.md` §4 verbatim, note
  adoption date + the F49(a) resolution, commit.
- **No / defer** → append the standing decision to prompt 12's inbox with the
  owner's stated reason.

### C. Doc consistency sweep

1. BUGS.md index rows vs entry heading tags — every status identical in both
   places (the F42 lesson; one stale row was already caught 2026-08-01,
   check for others).
2. STATUS.md counts vs reality (modules, probes, C-rows).
3. `docs/prompts/` holds only: the two standing prompts, this chain's folder,
   and live one-offs. Anything spent → `docs/archive/`.

## Scope fence

**In:** the checklist, HELP cross-refs, BUGS entry notes for retired/changed
tests, FIX_POLICY §4 (on approval), consistency fixes. **Out:** `Code/`,
TestKit, the game, new defect investigation (file + route instead).

## Stop conditions

- The §4 decision: owner unavailable → do everything else, route the decision
  to prompt 12's inbox, say so.
- A consistency error that implies a WRONG recorded result (not just a stale
  label) → stop and report before "fixing" the record; recorded facts are
  claims (project memory rule).

## What may not be claimed

No test may be marked retired without naming what absorbs its intent. No
checklist item may be added without citing the entry/audit section that
motivates it.

## On completion

Outbox → `2_f86_phase0_measurements_opus.md` (§4 decision result, any
checklist facts a keyboard session should know). Delete this file, commit,
push.

## Notes from upstream

(prompt 0 appends here if it finds checklist-relevant anything)
