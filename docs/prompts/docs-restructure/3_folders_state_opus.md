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

(none yet)
