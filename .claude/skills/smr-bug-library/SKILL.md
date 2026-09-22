---
name: smr-bug-library
description: Look up, check or file Relaunched Fix Pack defects (F/D/C) and engine facts (EF), using indexes, evidence fields and the filing checks.
---

# The bug library

## Must_Read_Header

Treat library records as claims; apply `docs/agent/WORKFLOW.md`, "Records and rulings", before relying on them.

## Reading: cheapest first; stop when answered

1. For ours-or-vanilla triage, search `rg -l -F -- <keyword> Code/` and inspect hits.
   No hit is only a vanilla lead; aliases and indirect effects remain possible.
2. Search `docs/agent/bugs/INDEX.md` for known defects and status; open only the
   relevant entry section for detail. Search `docs/agent/facts/INDEX.md`, never
   read it whole. Both indexes are generated; edit their source records.

## Front matter

| Field | Meaning |
|---|---|
| `status` / `status_source` | Current disposition and its evidence source |
| `derived_at` (facts) | Derivation SHA or game build |
| `seq` / `row` | Ordering; preserve contiguous numbering |
| `updated` / `verified` | Dates, not evidence. Blank `verified` means derivation is owed, not unreliability; fill only after a run |
| `row_status` | Frozen migration text; never use as current evidence or repurpose |

Doccheck checks `row_status`'s first status word; disagreement with `status`
is an expected warning. `split_bugs.render_entry` emits only `FRONT_FIELDS`:
unsupported keys are silently dropped. Put durable context in supported fields
or the body.

## Checking facts

`python tools/doccheck.py --emit-fingerprint` routes checks by `derived_at`.
`HOLDS` matches build identity, not claim validity, scope or dependencies.
`MOVED` requires a new baseline for current claims. Verify historical citations
in the named build's archived tree; establish current behavior against the
current build's archived tree or a current run. Date-inferred fingerprints are
weaker evidence than explicit ones.

## Filing

Use `doc-editing`. Copy a suitable recent record's shape: same-letter entry for
`docs/agent/bugs/<ID>.md`, or an EF record for `docs/agent/facts/EF-NNN.md`.

1. Match `id` to filename and continue `seq` without gaps. For bugs, align heading
   tag and `status`; for facts, state the derivation SHA or build in `derived_at`.
2. State the control that would falsify the claim.
3. Price harm in a named game phase, evaluating early-game constraints: limited
   domes, no factories, mostly 1x speed and no headroom. For a threshold or guard,
   ask the owner which regime it protects; do not infer it.
4. Before making a reporter's save decisive, record what shipped source settles,
   what a live TestKit probe could establish, and whether an existing measurement
   recipe can be extended. Only if all fail is a save a conditional ask, never
   drafted or put on an owed list. Logs also burden reporters, though less than
   saves. Our own fixtures follow WORKFLOW's "Fixtures, mutations and owner-typed lines".
5. Apply doc-editing's regeneration check to both bugs and facts, including peers'
   unfinished entries. Run `python tools/doccheck.py --regen`, review generated
   diffs, then `python tools/doccheck.py` until GREEN.
6. Commit only this edit's paths: `git add <exact paths>` then
   `git commit -F <msgfile> -- <same paths>`. Never `-a`.

Status changes require evidence, not opinion. `tested-attended` means the owner
watched in-game; never bulk-upgrade legacy bare `tested`.
