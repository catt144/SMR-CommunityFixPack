# 3 — Folders, STATE, facts (the big move; everything scripted or `git mv`)

Staleness check; requires prompt 2 complete. Read spec §§1, 3b–f, 4, 7.

## Structure knowledge (verified 2026-08-03)

- **ENGINE_FACTS.md is a BULLET LIST, not headings**: top-level facts start
  at column 0 with `- ` and carry multi-paragraph INDENTED continuation
  (including nested tables — the "OFF is three different things" fact holds
  a full table). Split rule: a new fact starts at every column-0 `- `;
  everything before the first bullet is the preamble (→ `facts/_preamble.md`).
  Assign `EF-001…` in source order. Some facts embed `[verified …]`/dated
  notes — copy bodies byte-preserved; front matter: `id`, `summary` (first
  bold phrase or first 8 words), `updated` (from git blame of the fact's
  first line, best-effort).
- **STATUS.md**: keep for `agent/STATE.md` ONLY the current top block
  (chain-complete banner), the F76/D12 adjudication summaries, the
  build-state counts block (replace numbers with doccheck `--emit-counts`
  output), release gates/holds, and pointers. Target ≤60 lines,
  rewrite-in-place style. EVERYTHING else (the ~1400 lines of dated
  narrative) is appended VERBATIM to `docs/archive/SESSION_LOG.md` under
  `# STATUS narrative archived 2026-08-03 (docs-restructure chain)`.
  ⚠️ SESSION_LOG is newest-first — append the block at the TOP, after any
  header comment.
- **Moves** are `git mv` (history-preserving): `docs/MOD_DESCRIPTION.md` →
  `docs/archive/` (+ freeze banner, spec §3d — the banner is ADDED text,
  allowed because MOD_DESCRIPTION is not yet an immutable record);
  `docs/reports/` → `docs/agent/reports/`; `docs/prompts/` →
  `docs/agent/prompts/` (⚠️ INCLUDING this chain folder — after this commit,
  the remaining chain files live at `docs/agent/prompts/docs-restructure/`).
  `docs/FUTURE_IDEAS.md` STAYS at root (owner-used, agents update).
- **Stubs** (3 lines: moved-to + date): `docs/BUGS.md` (exists from prompt
  2), `docs/STATUS.md`, `docs/agent/ENGINE_FACTS.md`.

## Jobs, separate commits

1. `tools/split_facts.py` (+ dry-run accounting, same discipline as the BUGS
   split) → `docs/agent/facts/EF-###.md` + generated `INDEX.md` + stub.
2. `docs/agent/STATE.md` + STATUS narrative → SESSION_LOG + stub.
3. The `git mv` set above, one commit, with the freeze banner.
4. `docs/README.md` rewritten as the one-screen human map + the spec §4
   translation note VERBATIM; the same note added to `CLAUDE.md`.
5. **Living-doc reference sweep — spec §3f list ONLY**
   (PLAYTEST_CHECKLIST, PLAYTEST_HELP, README, CLAUDE.md, WORKFLOW,
   FIX_POLICY, FUTURE_IDEAS, the two standing prompts now under
   `agent/prompts/`): update `docs/BUGS.md`→`docs/agent/bugs/`,
   `docs/STATUS.md`→`docs/agent/STATE.md`, `docs/reports/`→
   `docs/agent/reports/`, `docs/prompts/`→`docs/agent/prompts/`,
   `ENGINE_FACTS.md`→`agent/facts/` references. ⚠️ NOTHING in
   `docs/archive/` or `docs/agent/reports/` is edited — the translation note
   covers them.
6. WORKFLOW addition: the spec §7 adopted-rules block; FIX_POLICY §2 gains
   the one-line foreign-object rule ("every wrapper must be inert for a
   foreign object before it touches one").
7. doccheck v3 (spec §5): root allowlist BOTH directions against the README
   map (root must be exactly: PLAYTEST_CHECKLIST.md, PLAYTEST_HELP.md,
   FUTURE_IDEAS.md, README.md, BUGS.md-stub, STATUS.md-stub, agent/,
   archive/), STATE ≤60 lines, stubs present, INDEX freshness for bugs and
   facts. Green output in the final commit body.

Stop: any sweep edit that would touch archive/ or agent/reports/ → skip and
note it; accounting mismatch → revert, report, stop. May not claim
root-clean without doccheck v3 output. Close-out: notes → prompt 4 AT ITS
NEW PATH, strike README row 3, delete self, push.

## Notes from upstream

**From prompt 2 (Opus, 2026-08-03).** `docs/BUGS.md` is a 3-line stub; the
tracker is 116 files + a generated `INDEX.md` + `_notes.md` under
`docs/agent/bugs/`. doccheck is at **v2 and GREEN**; the hook is armed and runs
it on every commit.

**⛔ CORRECTION TO PROMPT 1's TABLE — there are FOUR structural `##` lines, not
three.** The fourth is **10122 `## Candidates under investigation`**, between the
D11 and D12 entries. Prompt 1 was right that byte-accounting cannot see this
class of corruption: unfound, it would have been swallowed into D11 with the
books still balancing. It was caught because the splitter derives the set by
SHAPE (a `## ` line followed by a blank line and an entry heading) and asserts
that derivation against the recorded table — the two disagreed. All 34 `## `
lines in the entries region were then read by hand: the other 30 are entry
sub-headings. **Apply the same two-derivations-must-agree discipline to the
ENGINE_FACTS split** — its "a new fact starts at every column-0 `- `" rule has
exactly the same failure mode (a stray column-0 bullet, or a divider that is not
a fact, lands inside the previous fact and every line still adds up).

**What prompt 2 decided that prompt 3 inherits (all recorded in the split
commit body, all mechanical):**
- Front-matter scalars are **JSON** (`title: "…"`), because entry titles carry
  backslashes, quotes and em-dashes and YAML double-quoting mangles `\B`.
  `members:` / `orphan_rows:` items are one JSON object per line. Result:
  `json.loads` round-trips exactly and no YAML library is needed.
  **`split_bugs.parse_front()` and the field conventions are generic — import
  them for `split_facts.py` rather than writing a second parser.**
- Two orders are preserved, because they differ: `seq:` = position in the old
  BUGS.md **file** order (1..116), `row:` = position in the old **index table**
  (1..151). INDEX is emitted in row order (so it is a drop-in replacement for
  the deleted table) with `seq` as its first column.
- **Nothing from the index table was thrown away.** Each row's five cells are
  preserved verbatim in front matter (`id`/`title`/`priority`/`evidence`/
  `row_status`), so "consumed" means "replaced by INDEX.md", not "deleted".
  `status:` is derived; `status_source:` records where it came from
  (`tag` ×113, `row-evidence` ×36, `row-status` ×1, `c-row-default` ×1).
- Route (a) as decided: 2 grouped files named for what they **hold** —
  `C03-C11.md`, `C12-C38.md` (the second heading's own "C12–C31" is stale and
  stays that way, byte-preserved); their members' rows are adopted into
  `members:` so INDEX still carries all 151. **C02** has an INDEX row pointing
  at `NO ENTRY TEXT`, and its row is in `_notes.md`'s front matter.

**doccheck v2, and what v3 has to know:**
- `recount()` now takes the **model**, not rows: `split_bugs.load_from_dir()`
  → `check_entries` / `check_index` / `recount`. The counts block is unchanged
  in shape, so STATE.md can paste `--emit-counts` as job 2 plans.
- `--verify-split [REV]` re-runs the whole migration accounting against
  `REV:docs/BUGS.md` and compares it to the files on disk. **REV defaults to
  `HEAD~1`, which stops being the pre-split commit as soon as you commit
  anything** — pass the sha explicitly (`--verify-split 5b374eb`, the split's
  parent) if prompt 4 wants to re-run it.
- **10 `warn` lines are expected and are not drift**: C12–C17, C34, C35, C37,
  C38's frozen row cell opens `filed …` while the entry's status is `cand`,
  taken from the row's disposition column (on a C row, column 4 is the
  disposition, not a confidence). Deliberate, documented in `c_status()`.
  ⚠️ Row-cell-vs-status is a **warn, not red, by design**: `row_status` is a
  frozen copy of a deleted row, and a live status must be free to advance past
  it. The red check is front-matter `status:` vs the entry's own heading tag —
  both live surfaces. All three v2 checks were negative-controlled (flipped
  status → red, hand-edited INDEX row → red, deleted body line → red).

**For job 5 (the living-doc sweep) and job 4 (the README map):**
- `_notes.md` carries BUGS.md's old intro **byte-preserved**, including the
  instruction *"Update this file in the same change that adds or edits a fix"*.
  That sentence now names a stub. It may **not** be edited (binding rule 1 —
  it is preserved content), so the live rule has to be stated where authors
  actually read it: WORKFLOW's new block and CLAUDE.md — *edit the entry file
  under `agent/bugs/`; INDEX.md is generated, never hand-edited*.
- The README map should say what the folder is: **116 entry files** (`F*.md`,
  `D*.md`, `C*.md`), **2 of them grouped**, `INDEX.md` **generated**,
  `_notes.md` = the residue that belonged to no entry (intro, the five `##`
  section dividers, the "Not yet swept" backlog, and C02's homeless row).
- v3's root allowlist is unaffected by this prompt: `docs/BUGS.md` is the stub
  spec §3e asks for.
