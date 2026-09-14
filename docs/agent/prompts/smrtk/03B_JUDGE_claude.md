# smrtk 03B — the judge (cross-vendor secondary)

Link 03B of `smrtk`. **Claude** (Opus; the vendor difference is the point, not the tier — 99 is the top-tier
skeptic). README rules 1–22 are yours. Runs only after 03A has closed and pushed. Fresh context: you have not seen
03A's work being made.

## The stance

03A's report (`reports/SMRTK_FANOUT_REPORT.md`) is a **claim set**. Your job is to try to refute it, cheaply, and
to hand the owner ONE consolidated ask instead of five. You are not 99: you do not re-derive the whole chain; you
re-run gates, sample routes, and check the things a coordinator reading five reports is most likely to have
waved through.

**Departures are not findings.** README § "What is FIXED" gives the builder licence to change any default with a
stated reason. Judge each DEPARTURE on whether it crosses an invariant and whether its reason holds — a better
route than the plan's is a PASS with a note, and the note goes to 07 so the docs describe what was built. A
*silent* departure (found by you, absent from the report) IS a finding. Engage every SUGGESTION on its merits: adopt
(one-line fixes), route (to ck175 with your view), or decline with a reason — never ignore one.

## Job

1. **Re-run every gate 03A pasted**, on HEAD, yourself: parsecheck per file, rule 6 and rule 7 greps (presence side
   too), H-10 list membership, `doccheck` GREEN, the whole-list parse sweep. Any difference from the pasted output
   is a finding, first in your report.
2. **Sample the routes against the facts:** open every registered action in P1 and P2 (the two with the most leaf
   calls) and, for each, name the leaf it calls and confirm it is not one of `EF-098`'s 13 nor a wrapper
   (`EF-095`). Ten actions minimum from P3–P5 the same way.
3. **The shared techniques actually shared:** `reports/SMRTK_UI_HOOKS.md` §1 is what P2 built and §2 is what P3
   built — read both files against the spike's decision. Divergence is a finding even if both work.
4. **The idle invariant, on the desk:** enumerate every vanilla function assignment in the five files (`grep -n
   "^\s*[A-Za-z_.:]* *= *function\|rawset(_G" …` and the `_G.` writes); each must be inside a toggle's install
   with a matching uninstall (rule 9), or it is a finding.
5. **Stubs and cross-ids:** every "not built" stub 03A recorded resolves now that all five landed, or is listed
   as owed with its owner.
6. **Consolidate the owner items:** every OWNER-ROUTED line from the five payloads and 03A into **one** append to
   ck175, each with 03A's recommendation and yours (agree / disagree, one line why). Nothing owner-facing may
   remain only in a report.
7. **Verdict** in `reports/SMRTK_JUDGE.md`: **PASS** · **PASS WITH FIXES** (you may apply one-line label/log-shape
   fixes yourself, by pathspec, and list them) · **RE-FIRE** (name the payload and put the exact failing gate or
   route in a new `payloads/Pn_*.md` inbox for 03A to run again — restore the brief from its grave with `git show`).
   **Disagreements with 03A first**, then agreements, then the outbox.

## Scope fence

IN: gates, sampling, the two reports, ck175, one-line fixes. OUT: building anything, re-designing a page, touching
the core.

## What may NOT be claimed

That a page works in play (08). That 03A's report is true because it is well-formatted. A PASS on a payload whose
routes you did not open.

## Close-out

Outbox to 07 (the verified button lists, per page; the stubs still owed) and 99 (your disagreements with 03A,
verbatim — 99 adjudicates the cross-vendor split); strike your row; `git rm` this file; push.

## Notes from upstream

- (03A appends here)

### 03A build outbox, 2026-09-13

Codex 03A completed five payloads plus shared core/panel extensions. Final
TestKit HEAD `cee5bab230f2fac876aa0e6d86bb97f6b56ad020`; TestKit has no remote. The pack close-out commit
contains `reports/SMRTK_FANOUT_REPORT.md`, all five numbered payload reports,
format, independent gate/model commands, EF-099 source corrections, and the
spent briefs' removal. Restore a brief from the close-out commit's parent
when a re-fire is needed. No new page/native effect/save-load/stamp has run
in game. 02 final PASS/outbox remains the prerequisite authority; 08 is next
full game evidence after 03B/07. No status/version/pack-runtime edit occurred.

Re-run actual HEAD commands, opening routes rather than accepting reports:

```text
python docs/agent/reports/SMRTK_FANOUT_GATES.py --ordered --presence
python tools/parsecheck.py --dir ../SMR-BugFixPack-TestKit/Code --quiet
python docs/agent/reports/SMRTK_FANOUT_SMOKE.py
python docs/agent/reports/SMRTK_P1_SMOKE.py --selftest --list
python docs/agent/reports/SMRTK_P2_SMOKE.py
python docs/agent/reports/SMRTK_P3_SMOKE.py
python docs/agent/reports/SMRTK_P4_SMOKE.py
python docs/agent/reports/SMRTK_P5_DESK.py
python docs/agent/reports/SMRTK_FANOUT_MERGE.py --selftest
python tools/doccheck.py
```

Coordinator per-file gates are copied verbatim in the main report: parse0,
no-sync0/no-bare-print0 on each owned file, H-10 listed, doccheckGREEN;
presence26. Final TestKit tree clean. Main report contains all warnings,
full core/panel/90 diff and emitted file/function/line inventory. No payload
failed the required gate; no gate re-fire was used. Every final page and
cross-id resolves. Slot buttons deliberately remain unbound until sitting
preparation; print_tee is a registry helper, not a Kit button.

Cross contracts: P2 Dump=dump_selected; Pins=pin_A/B/C; P4 watch_field creates
P3 watch_selected_field disarmed, then explicit Arm; P5 follow-ups dynamically
Run fill_storages(), spawn_colonists(10), funding(500000000). Logger ids are
logger_<native name>; read-only 90 LoggerState returns enabled-copy. Quiet
and any native/toolkit logger refuse nesting, preserving captured originals.
MARK -> primary record -> taint assertion -> guarded after_record.MARK ->
separate fingerprint action covers normal/screenshot marks; refused marks
skip hook. The callback coordinates read-only/separately dispatched evidence.

Required disagreements/departures first: no building construction test flag;
terrain is not complete fit; owned-site completion avoids CompleteAll scope;
grid steps include endpoints/each returned cell must pass; passage topology
not represented; non-Code layouts load early via literal queue; safe helper
installation corrects broad blacklist claims; Delete class overrides/busy
mechanized refusal; ["do"] Lua spelling; trigger real-time effect handoff;
native screenshot accepted is not pixels; native metadata read helper avoids
DoneGame; deterministic save name; provenance callback attempts/last record;
scoped snapshot; explicit sitting-bound desktop probe attestation; P5 second
unit follows THREE SYNTHETIC PLANS, not native stamps. Passage/special objects
and variants have named v1 skips; native geometry/GameInit remains unmeasured.

Main report OWNER-ROUTED contains every merged payload recommendation, with
recommendations on hybrid surface/Delete/48-character save strip, unavailable
eligibility, quiet/modern rocket, run-until attempt semantics, scalar/error/
screenshot limits, probe attestation/current-branch fixture/legacy00 console,
scoped two-map snapshot and bounded Stamper/passages/partial abort. 03B makes
ONE ck175 append with its recommendation for each, no scattered requests.
Final per-page button table, emitted World registry, P3 verbatim slot template,
P4 preflight contract and P5 measured-count 08 recipe are for07 AFTER03B.

DRIFT is preserved, including stale02 header vs finalPASS, initial wrong
paths/quotes/globs/parse CLI, EF-099 linesRED->emittedregenGREEN, corrected P2
SHA before commit, untracked pathspec refusal before git-add, source/helper
claims, screenshot-thread falsifier failure, quiet re-arm correction, false
reads/provenance/id/disaster scope, P5 parent/FIRE refusal, shared scrollbar,
combined fake PropObjHasMember omission, and nine alias UNKNOWN initializer
false positives (00_TestCore order/probes/last opened19-21). Foreign dirty
archive planning remains untouched. Do not count failed queries as negatives.

Late03A source correction: native XTextEditor.Init clears its buffer; raw
constructor Text does not initialize it. P3 already used SetText correctly;
coordinator after release added setters in72/76/77, one-file gated commits.
Strict combined fake now discards constructor Text; three editor counterfeits
(World/Kit/Stamper) each goRED. Review XTextEditor171-175,221-228 and
XControl624-634. P5 nineteen cases did not model editor initialization.
