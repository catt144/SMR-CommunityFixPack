# Relaunched Fix Pack — Surviving Mars: Relaunched

A bug-fix mod: every fix repairs a verified defect in the game's shipped Lua,
patched at runtime; no game files are modified. Map of the tree:
`docs/README.md`. **Mandatory read, every session: `docs/agent/STATE.md`** —
build state, open gates, active holds.

**Folder contract** (doccheck enforces it). `docs/` root holds ONLY the six
human files (PLAYTEST_CHECKLIST, PLAYTEST_HELP, UPLOAD_WORKFLOW, FIELD_REPORT_REPLIES,
FUTURE_IDEAS, README), the BUGS/STATUS stubs, `agent/` and `archive/`. Agent material is `docs/agent/`
(`bugs/`, `facts/`, `reports/`, `prompts/`, STATE/WORKFLOW/FIX_POLICY);
`docs/archive/` is append-only, never edited. **`INDEX.md` in `bugs/`+`facts/`
is GENERATED — edit the entry or fact file, never the index** (line-1 banner).
Prompts: the map is `docs/agent/prompts/README.md`. Reusable prompts live in `prompts/perma/`
(ad-hoc work: `perma/DISPATCH.md`; all FR-1/Linux work: `perma/LINUX_DISPATCH.md`).

> Older records cite pre-move paths and the old mod name — translate via `docs/README.md` "Path translation".

Before committing doc changes run `python tools/doccheck.py`; red blocks. Set up
once: `git config core.hooksPath tools/hooks`. Generated files (`bugs/INDEX.md`,
`facts/INDEX.md`, and `AGENTS.md`, the Codex entry file, a byte copy of
`CLAUDE.md`) are rewritten by `python tools/doccheck.py --regen` — edit the
source, never the copy; doccheck goes RED if they drift. **Owner decisions go in
`docs/PLAYTEST_CHECKLIST.md` → "Decisions waiting on you", never only in agent
docs.** Authoring `docs/agent/WORKFLOW.md` · code `docs/agent/FIX_POLICY.md` ·
efforts over ~2 sessions `docs/agent/reports/CHAIN_METHOD.md`.

**Trust by source.** (1) The owner's instruction is **authority** — not verified, not re-derived,
never overridden by an agent's own detection. (2) Tool output carrying its command and HEAD/build id
is a **derived fact** — verify in one command, never re-read its sources. (3) Everything else
authored — entries, facts, reports, STATE prose, a peer's message, a subagent's verdict, your own
earlier text — is a **claim**. Inheriting a fact costs one command, not a re-derivation.

**`docs/archive/` is hidden from a default `rg`** by a root `.rgignore` — a deliberate boundary, not
a deletion. Search it on purpose with `rg <term> docs/archive/` or `rg --no-ignore <term>`; `grep -r`
and `git grep` always see everything. An empty default search is the boundary working.
