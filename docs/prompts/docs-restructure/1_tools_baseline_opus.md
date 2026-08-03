# 1 — Tools + baseline (run FIRST; nothing moves in this prompt)

Staleness: `git log --oneline -10` + `git pull`. Read
`docs/reports/DOC_RESTRUCTURE_SPEC.md` §5 and §6 in full. Live todo list per
WORKFLOW element 1.

## Jobs, one commit each

1. **`tools/doccheck.py` v1** (spec §5). Checks, exact knowledge from the
   2026-08-03 QA session that hand-ran all of this:
   - **Index rows**: `^\| ([FDC]\d+) \|` over `docs/BUGS.md`. ⚠️ Traps the QA
     hit: (a) the pattern ALSO matches a rate table inside the F97 entry
     (`| F97 | **50%** (gate fails) | …`) — dedupe by ID keeping the FIRST
     occurrence; (b) rows F and D live in one table near the top, C rows in a
     second table below — both are index rows.
   - **Heading tags**: heading lines are `^### <ID> <title>  \`[<tag>]\``.
     ⚠️ Titles contain backticks (e.g. `` `table.remove` ``) — extract the tag
     as the **LAST** `` `[...]` `` group on the line
     (regex `` r"`\[(.*)\]`\s*$" ``), never the first backtick group.
     ⚠️ `^### ` alone is NOT an entry delimiter — entries contain their own
     `###` sub-headings (e.g. F97's "### ⭐⭐ AND THE UNINSTALL LOG…"). Match
     `^### ([FDC]\d+)\b` specifically.
   - **Status-word agreement** row vs tag: compare the first status word from
     a fixed vocabulary, checking longest-first so `fixed*` is not read as
     `fixed`: `tested, fixed*, fixed, wontfix, blocked, todo, open,
     investigating, closed, built, directed, parked, opt-in, candidate,
     folded, filed, speced, cand, dsgn`. Strip leading `**`/`⭐`/`⛔`/`~~`
     markup before matching. Expect ZERO mismatches (verified 2026-08-03).
   - **Counts** (`--emit-counts` prints a STATE-ready block):
     `Code/*.lua` file count; files containing `SMRFixPack.Register(` minus
     `00_Core.lua` (= registered modules); files containing
     `optional = true` (informational; default-active = modules − 7, because
     `Opt_DroneStatDials` is the 8th optional but reports active at base);
     TestKit probes = occurrences of `SMRTest.Register(` in
     `C:\Dev\SMR-BugFixPack-TestKit\Code\*.lua` minus 1 (the definition in
     `00_TestCore.lua`); index rows per kind.
   - **TEMPORARY sweep**: `TEMPORARY` in `Code/` and the TestKit `Code/` —
     zero hits or list them.
   - Exit non-zero on any red. **Expected baseline TODAY: green, 98 F + 12 D
     + 41 C, 82 files, 81 modules, 87 probes.** If the baseline is NOT green,
     STOP and report — that is a finding, not something to fix here.
2. **Pre-commit hook**: `tools/hooks/pre-commit` (sh, `python
   tools/doccheck.py || exit 1`); header documents
   `git config core.hooksPath tools/hooks`; RUN that config command in this
   repo and verify the hook fires on a no-op commit.
3. **`CLAUDE.md`** at repo root per spec §6 skeleton (≤25 lines). It cites
   TARGET paths that prompts 2–3 will create — include the line
   "(layout live after the docs-restructure chain completes)" which prompt 4
   removes.
4. **Checklist decisions section** (spec §7 / R10): insert
   `## Decisions waiting on you` at the very top of
   `docs/PLAYTEST_CHECKLIST.md`, seeded from `CHAIN_QA_REPORT.md` §8's
   owner-decision items: the mod-page relabel package (§3) · the D03/D07 dead
   `SMRFixPack_Disabled` veto · the F46 group C→B move · the C36-adjacent
   mysteries grep · DOC_STRUCTURE_REVIEW adoptions beyond this chain. One
   line + pointer each; agents strike lines when the owner decides.

## Fence / stops / claims

Fence: NO file moves, no BUGS content edits, no STATUS edits. Stop: baseline
red. May not claim: a green baseline without pasting doccheck's full output
in the commit body. Close-out: append notes to prompt 2's
`## Notes from upstream`, strike README row 1, delete this file, push.

## Notes from upstream

(none yet)
