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

> 2026-08-03 restructure: `docs/BUGS.md` → `docs/agent/bugs/<ID>.md`;
> `docs/STATUS.md` → `docs/agent/STATE.md`; `docs/reports/` →
> `docs/agent/reports/`; `docs/prompts/` → `docs/agent/prompts/`;
> `docs/agent/ENGINE_FACTS.md` → `docs/agent/facts/`. Pre-restructure
> documents cite the old paths; translate mentally, do not edit records.
> Renamed 2026-08-03: `FABLE_NEXT_PROMPT.md` → `agent/prompts/perma/GENERAL_USE_PROMPT.md`.
> 2026-09-11 (owner): `docs/agent/reports/FIELD_REPORT_REPLIES.md` → `docs/FIELD_REPORT_REPLIES.md`,
> a human file (the owner posts, agents draft). Older records cite the old path; translate mentally.
> 2026-08-17: the pack was renamed **Community Fix Pack → Relaunched Fix Pack**
> (display name only; the mod `id` and `[CommunityFixPack]` log tag are
> unchanged). Earlier records use the old name — translate mentally, do not
> edit records.

Before committing doc changes run `python tools/doccheck.py`; red blocks. Set up
once: `git config core.hooksPath tools/hooks`. Generated files (`bugs/INDEX.md`,
`facts/INDEX.md`, and `AGENTS.md`, the Codex entry file, a byte copy of
`CLAUDE.md`) are rewritten by `python tools/doccheck.py --regen` — edit the
source, never the copy; doccheck goes RED if they drift. **Owner decisions go in
`docs/PLAYTEST_CHECKLIST.md` → "Decisions waiting on you", never only in agent
docs.** Authoring `docs/agent/WORKFLOW.md` · code `docs/agent/FIX_POLICY.md` ·
efforts over ~2 sessions `docs/agent/reports/CHAIN_METHOD.md`.
