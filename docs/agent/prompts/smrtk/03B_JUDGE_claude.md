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
