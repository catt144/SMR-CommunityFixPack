# 2 — The BUGS split (scripted; the riskiest prompt — go slow)

Staleness check; requires prompt 1's doccheck green. Read spec §§1–3a, §5-v2.

## Parser knowledge (from the session that verified all 110 entries — trust
## these specifics over guesses, verify them over trust)

- **Entry delimiter**: `^### ([FDC]\d+)\b` ONLY. Entries contain their own
  `##` and `###` sub-headings that belong to the entry (F97 contains
  `## ⚠️ THE RATE QUESTION…` and a `### ⭐⭐ AND THE UNINSTALL LOG…`; D12
  contains `## WHAT D12 SHIPS`; F86/F87 contain `> ##`-quoted headings —
  none of these start a new file).
- **File regions**: (1) everything before the first entry heading = the
  intro + the two index tables (F/D table, C table) → consumed (the
  generated INDEX replaces the tables; keep the intro prose at the top of
  `_notes.md`); (2) entries, in file order (NOT sorted — preserve order in a
  `seq:` front-matter field so INDEX can reproduce it); (3) everything from
  `^## Not yet swept` to EOF → `_notes.md` (it follows the C41 entry and is
  NOT part of it).
- **Tag extraction**: LAST `` `[...]` `` group on the heading line
  (`` r"`\[(.*)\]`\s*$" ``) — titles contain backticks. A handful of tags are
  long (D12's is ~90 words) — the tag goes INTO the body's heading line
  unchanged; front matter carries only the derived fields.
- **Front matter** per spec §2; `status:` = first vocabulary word of the tag
  (prompt 1's matcher — import it from doccheck, do not re-implement);
  `title:` from the INDEX ROW (not the heading — heading titles and row
  titles differ in wording for some entries; the row title is the short
  form); `priority:`/`evidence:` from the row's columns 3–4 (C rows: `?` and
  their col-4 as evidence).
- **The F97 rate-table trap** applies to row extraction here too: dedupe by
  ID keeping first.
- Cross-entry prose exists INSIDE entries (e.g. the drone-sweep material in
  the C40 region) — do NOT try to be clever about it; the delimiter rule
  alone decides ownership, byte-for-byte.

## Jobs

1. `tools/split_bugs.py` with `--dry-run` printing full accounting: total
   source lines == (lines landed in entry files) + (index-table + intro
   lines consumed) + (`_notes.md` lines). Abort on: row↔tag status mismatch,
   heading without a row, row without a heading, duplicate ID files.
2. Run real: write `docs/agent/bugs/<ID>.md` (front matter + body
   byte-preserved incl. the heading line), `_notes.md`, generated `INDEX.md`
   (banner per spec §1; columns: seq · id · title · status · priority ·
   evidence · file link). Replace `docs/BUGS.md` with the 3-line stub
   (spec §3e).
3. Extend doccheck to v2 (spec §5): front-matter validation (all fields,
   status in vocabulary), INDEX freshness (regenerate → diff must be empty),
   and `--verify-split` re-running the accounting from
   `git show HEAD~1:docs/BUGS.md`.
4. **Verification, in the commit body**: the accounting block; plus
   spot-diffs of THREE entries (F86, D12, C41 — chosen as largest, most
   markup-heavy, and last-in-file) against `git show` of the original: body
   bytes identical.

Fence: content byte-preserved — no entry may be "improved" in passing; no
other doc touched except the stub. Stop: ANY accounting mismatch you cannot
explain to the byte → `git revert`, report, stop. May not claim "migrated"
without the accounting block. Close-out: notes → prompt 3, strike README
row 2, delete self, push.

## Notes from upstream

(none yet)
