# CK170 and fingerprint provenance — 2026-09-13

## Phase 1 — owner rulings implemented

Anchor: `5b807be`, clean checkout, doccheck GREEN. Executed model: GPT-6
(session developer identity; no more specific executed model identifier exposed).
Owner authority: the fired `CK170_AND_FINGERPRINTS.md` brief records the rulings;
this pass did not re-adjudicate them. Checklist 170 now says `ruled owner:no`.

### Measurements, separated by change

MEASURED with `python tools/doccheck.py | Select-String
'MARKER|duplicate|PUSH SET|STATE \+ STUBS|^doccheck'`, at the anchor and then
after each working-tree change, in the order below:

| stage | marker integrity | push set | STATE |
|---|---|---|---|
| before | 46 on disk, 45 parsed; WARN | 42199 B | 10388 B |
| (a) marker repair only | 46 on disk, 46 parsed; WARN | 42199 B | 10388 B |
| (b) LF accounting only | 46 on disk, 46 parsed; WARN | 42199 B | 10388 B |
| (c) reading routes | 46 on disk, 46 parsed; WARN | 42517 B | 10388 B |

All runs ended `doccheck: GREEN`. The matching ck144 duplicate is deliberately
WARN; the recorded ruling does not authorize renumbering. Current warning:

```
  warn duplicate ck:144 at lines 2269, 2343 (agree)
PUSH SET: 42517 B in 5 file(s) ≈ 20k tokens (budget 40960 B)  ⚠ OVER
```

(a) `tools/doccheck.py` rejects unknown vocabulary, malformed ck comments and
disagreeing duplicate status/owner pairs. The main gate consumes its Boolean
result. ck169's current marker uses legal `open owner:yes`; its historical marker
uses `ck:-`. Its current heading now agrees with its existing FAQ-discharge body.
The old heading is a subsection: **changing its marker alone does not exclude a
historical ask**, because the register selects decision-level headings. Verify:
`rg -n '^\| 169 |^\| 170 ' docs/WAITING_ON_YOU.md`.
The register now selects `owner:yes` independently of decision status: a settled
decision can still owe an action. A synthetic ruled/closed + owner:yes fixture
exposed the former status filter; live rows are unchanged by removing that filter.

(b) STATE total and per-line budgets, the push set and skill budgets count LF
content bytes. Byte-identity gates remain raw-byte comparisons. Caps and measured
document content are unchanged. The predicted line-ending saving did **not**
reproduce: this checkout's measured files already use LF. `.gitattributes` keeps
the STATE pin but no longer describes raw-byte accounting as current behavior.

(c) DISPATCH and WORKFLOW now route index searches by task ID/keyword instead of
full scans. DISPATCH cites R-A/R-B/R-E/R-F/R-G at work/close-out and points brief
authors to R-C. WORKFLOW's required brief elements now include R-C and contain
the unchanged R-D body, moved out of the working verification section. Verify:
`rg -n 'R-[A-G]\b' docs/agent/prompts/perma/DISPATCH.md docs/agent/WORKFLOW.md`.
No additional skill text: both skills already route fingerprints, and duplicating
the labels there adds no reach beyond the dispatch/authoring routes.

### Falsifiers

`python tools/ck170_selftest.py` exercises deliberately broken **disk copies**:
unknown/hyphenated status, malformed identifier, unterminated comment, status
disagreement and owner disagreement all FAIL. Matching duplicates WARN. LF and
CRLF readings agree; real total/per-line overruns FAIL under both endings. A
reverted raw-byte measuring instrument FAILS the equivalence fixture. Restored
copies rerun the cases and print SHA256; the live file is asserted unchanged.
Skill caps also FAIL real overruns under both endings; their mirror gate still
rejects raw-byte drift. Owner-action fixtures cover every legal status and falsify
a reverted status filter. These added checks leave the live measurements unchanged.

`python tools/repair_pass_selftest.py` also passes, including its reverted
instrument falsifiers; its marker expectations were updated to the adopted gate.
`git diff --check` passes. Pre-test probe sweep:
`rg -n 'TEMPORARY' Code ../SMR-BugFixPack-TestKit/Code` returned no matches.

### Not done / scope limits

- ck169 still carries `owner:yes` as instructed. Its body and STATE contain later
  discharge information; this pass does not invent permission to close that item.
- No other owner status, game code, hazard or release artifact changed.
- No push-set eviction; the warning remains. No separate peer adjudication run.
- Phase 2 provenance audit follows in a separate commit; not included in Phase 1.

Commit receipts and Phase 2 findings will be appended after their runs.
