# Archived defect records — the 1.0.7-era candidate block

⛔ **PULL-ONLY, AND NOTHING TRACKS THIS FOLDER.** No INDEX row, no count, no owed
list, no agent raises it. It exists so that **if a pointer ever arrives**, the
original record is still here to read. Do not sweep it, do not re-investigate it,
do not surface it unasked.

## What is here, and why it left

Archived **2026-09-16** by owner ruling. Every candidate whose evidence was
derived before the 1.1.0 baseline move (2026-09-08) — which turned out to be
*exactly* the set carrying priority `?`, by two independent cuts.

**The owner's reason, recorded so it is not re-litigated:** mysteries and much
else have always been famously broken, but the developers did a **massive
overhaul in 1.1.0**. Investigating stale candidates whose only evidence is a
1.0.7 report is a poor use of resources while true 1.1.0 candidates are waiting.
If one ever comes up again, it is still here as a reference.

⚠️ **ARCHIVED IS NOT REFUTED.** Nothing here was disproved. A 1.0.7-era defect can
survive into 1.1.0 byte-identical — `C96` is exactly that, filed 2026-09-15. If a
**1.1.0** report matches one of these, read the record here, then file it fresh
against the current baseline rather than reviving the row.

## The four files

| file | holds |
|---|---|
| `C01.md` | one ordinary entry (seq 111, row 111) |
| `C03-C11.md` | grouped: head C03 plus C04–C11 as `members:` (seq 112, rows 113–121) |
| `C12-C38.md` | grouped: head C12 plus C13–C38 as `members:` (seq 113, rows 122–148) |
| `C02_orphan_row.md` | row 112 — an index row that never had an entry body |

**38 rows in total: 25 `cand`, 12 `closed`, and 1 `filed`.** The closed rows rode
along because they live inside the same two grouped files; they were already
resolved (C04 was promoted to F90). The single `filed` row is **C36**, whose own
cell reads *"filed AND closed 2026-08-01 — a downstream victim of F81(a), which
our pack already fixes"* with evidence "✅ SOLVED — not a new defect", so it is
resolved bookkeeping rather than open work.

Every archived id, so a `grep -r` for any of them lands here:

> C01 · C02 · C03 · C04 · C05 · C06 · C07 · C08 · C09 · C10 · C11 · C12 · C13 ·
> C14 · C15 · C16 · C17 · C18 · C19 · C20 · C21 · C22 · C23 · C24 · C25 · C26 ·
> C27 · C28 · C29 · C30 · C31 · C32 · C33 · C34 · C35 · C36 · C37 · C38

⚠️ **Live entries still cite some of these.** `F81` cites **C36** three times,
`F16` once. Those citations carry the mechanism themselves, so they stand on
their own — but a default `rg` will never reach the row behind them, because
`docs/archive/` sits behind the root `.rgignore`. That is the boundary working,
not a missing file.

## Reading it on purpose

```
rg <term> docs/archive/bugs/     the archive alone — naming the path defeats the filter
rg --no-ignore <term>            live + archive in one pass
grep -r <term> docs/             ignores .rgignore entirely
```

## How the numbering survives this

Archived entries keep their original `seq` and `row` **verbatim**. That is
load-bearing: `doccheck` reads those numbers back out of this folder and accepts
the matching holes in the live library's numbering. Before 2026-09-16 the rule
was `seq`/`row` must be 1..N contiguous, which meant archiving three files would
have forced a `seq`/`row` rewrite of **83 surviving entries**. The gate now
requires only that every gap be *accounted for* here, so duplicates and genuine
losses still fail RED while archiving costs nothing.

⛔ **Never renumber a file in this folder**, and never reuse an archived number
for a new entry — doccheck goes RED on a number claimed by both sides.
