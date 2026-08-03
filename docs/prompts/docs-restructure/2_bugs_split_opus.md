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

**From prompt 1 (Opus, 2026-08-03).** All line numbers below are as of the
commit that closed prompt 1 — re-derive them after any BUGS.md edit.

**State you inherit.** doccheck v1 is green. The pre-commit hook is **ARMED**
(`core.hooksPath = tools/hooks` is set in this clone), so every commit you make
runs doccheck and is refused on red — both paths were verified, not assumed.
`--no-verify` exists; using it means "the docs are inconsistent and I am
committing anyway" and must be said in the commit message.

`doccheck.status_word()` is the matcher to import, as your brief says. Two
behaviours to know: it strips **all** leading non-letters (the markup zoo is
`**`, `~~`, `` ` ``, ⭐, ⛔, ✅, ⚠️, ⏸️ and growing), and the **tag is
authoritative** — spec §2 derives from it and the row is deleted, so a row
that opens with prose instead of a status word is checked by containment and
reported `warn`, not red. Two today, F82 and F93; both are fine.

D12's row/tag mismatch was red when prompt 1 started and was repaired in
`b243e3e` by a parallel session — do not re-derive it.

**Correction 1 — there is ONE index table, not two.** Your parser section says
"the two index tables (F/D table, C table)". Wrong: rows 19–169 are a single
contiguous table with no interior header, in kind runs **F×63, D×12, F×35,
C×41**. Region 1 also holds, *after* the table: the `Severity:` legend (171),
a `---` (173) and `## P1 — gameplay-breaking` (175).

**Correction 2 — three structural lines belong to no entry, and byte-accounting
cannot catch them.** A naive "entry runs to the next `###`" rule swallows each
into the *preceding* entry, and the accounting still balances, because nothing
is lost — the corruption is invisible to your only check. Assert on them:

| line | line content | sits between |
|---|---|---|
| 666 | `## P2 — wrong numbers / notable misbehavior` | F11 and F12 |
| 932 | `## P3 — cosmetic / latent / mod-facing` | F22 and F23 |
| 1327 | `## Phase 2 findings — details (2026-07-24)` | F29 and F30 |

**⛔ BLOCKER — spec §3a's verification is unsatisfiable as written. STOP AND
ASK before you split.** There are **151 index rows but only 116 `###` entry
headings**. Every F and D row has its own heading (98 + 12); **C has 41 rows
and 6 headings**. So your job-1 abort "row without a heading" fires **35
times**, and §3a's "regenerated INDEX row-count == 98 F + 12 D + 41 C" cannot
hold against 116 entry files. Verified breakdown:

- The 35 heading-less rows: **C02**, C04–C11, C13–C38.
- 34 of them have their text inside two grouped headings — `### C03–C11`
  (10548–10615) and `### C12–C31` (10616–12293). ⚠️ **The second heading's
  stated range is stale: it actually holds C12 through C38.**
- **C02 has an index row and no entry text anywhere in the file.** Its status
  cell is `runtime-check` and it carries no `(entry)` marker.

The spec never decided what a grouped-section C row becomes. Three routes, and
the choice is the owner's:

- **(a) recommended** — INDEX carries all 151; a grouped C row's link points at
  the grouped file plus an anchor; entry files stay 116. The only route that
  keeps the row count, keeps bytes preserved, and needs no judgment. C02 gets
  an INDEX row with no target, flagged.
- (b) split the grouped sections into per-ID files — needs judgment *inside*
  grouped prose, which collides with binding rule 1 (no hand-editing content).
- (c) INDEX carries only the 116 and the C rows go to `_notes.md` — loses index
  coverage of 35 candidates.

**✅ DECIDED 2026-08-03 (the chain-authoring Fable session, under the owner's
delegated structure authority): ROUTE (a), with these refinements — treat this
block as spec §3a's amendment:**
1. **116 entry files.** The two grouped sections become `C03-C11.md` and
   `C12-C38.md` — **filenames tell the truth even though the second HEADING's
   stated range is stale**; heading bytes stay preserved (rule 1), and the
   generated INDEX is the truth surface from now on. Front matter for grouped
   files: `id: C03-C11` / `id: C12-C38`, `kind: grouped`, plus a `contains:`
   list of the member IDs.
2. **INDEX carries all 151 rows.** Grouped members' rows link to their grouped
   file with `grouped → C12-C38.md` in the link column (no fake anchors —
   per-ID anchors inside grouped prose don't exist and must not be invented).
3. **C02**: INDEX row kept, link column `NO ENTRY TEXT (verified prompt 1,
   2026-08-03)`; add one line to `_notes.md` recording the same. Do not
   fabricate an entry.
4. **Amended abort rule**: "row without heading" aborts UNLESS the ID is in
   the verified set {C02, C04–C11, C13–C38} — assert that set EXACTLY (a 36th
   heading-less row means the file changed; stop).
5. **Assert the three structural `##` lines** (P2/P3/Phase-2 headers) land in
   `_notes.md`, not in the preceding entry — prompt 1 is right that
   byte-accounting alone cannot see that corruption.
