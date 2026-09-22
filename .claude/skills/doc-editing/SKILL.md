---
name: doc-editing
description: Create, edit, move or retire Relaunched Fix Pack documentation while preserving decisions, obligations and rules headers. Use before any documentation change here.
---

# Documentation edits

Verify meaning in actual passages; matching headings and passing doccheck
do not prove preservation.

## Scope and authority

- Read the document's `Must_Read_Header`; maintain it for new or edited
  documents, consistent with audience, scope and body.
- Identify the reader and supported action. Use `docs/README.md` for placement;
  relocate rules only with existing authority.
- Preserve owner decisions verbatim with their conditions, where the role
  that obeys them reads them. The checklist holds outstanding owner asks,
  never rulings; remove completed asks.
- For historical evidence, use smr-orientation's archive search route.

## Rules

Apply the placement criteria, exceptions and calibration before writing,
moving, retaining or removing rules: the `rule-placement` skill states them
compactly, and `docs/agent/reports/RULE_PLACEMENT_TEST.md` §§ "The question",
"Audit criterion" and "Calibration" hold the same test with its worked
reasoning. The report's historical implementation plans are not new duties.

The owner delegates removal authority to this test: execute decided
dispositions without another ruling and record evidence in the commit
message. Apparent uselessness alone is insufficient. Where the test does
not decide, preserve the rule and ask.

Find duplicates by meaning. When excluding a category, state what the
exclusion must not cover in every copy.

## Reader and trimming

- Agent-only documents may favor machine-checkable structure over prose.
  Optimize for fewer errors and lower context cost; document count is
  unconstrained. Translate for the owner on demand.
- Anything the owner reads, including handoffs, needs readable structure
  and useful links; avoid emoji-dense emphasis.
- Default to deletion within preservation and authority requirements.
  Surviving lines need a purpose, home or slot under a stated cap.
  Do not defend every cut.

## Moves and cuts

Separate settled evidence from open obligations; follow the destination's
retirement rule. Before cutting, compare source diffs with actual destination
passages: full obligations and conditions must survive. Remove relocated
instructions from the source in the same change.

Retiring a rule repo-wide is decided by tense, not by file type: a
present-tense statement in a report, an entry's prose or a `row_status:` line
still instructs its reader. Re-run the grep afterwards and justify each
remaining hit.

Parked or cut items belong only in pull-only documents, marked not
agent-tracked. Search doccheck's `PUSH_SET` and remove every mention,
including tombstones.

Size targets never override preservation; restore suspended caps only
on the owner's ruling.

## Verification

Before `python tools/doccheck.py --regen`, compare changes in both
`docs/agent/bugs/` and `docs/agent/facts/` with this edit's inputs.
Regeneration includes peers' unfinished entries; review generated diffs
for unrelated changes.

Check preserved decisions, conditions, obligations, header/body agreement
and required homes. For revised prompts, check purpose, scope and lifecycle
against `docs/agent/prompts/README.md`.

This skill checks judgment, not its own invocation.
