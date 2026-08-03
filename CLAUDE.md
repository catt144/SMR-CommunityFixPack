# Community Fix Pack — Surviving Mars: Relaunched

A bug-fix mod: every fix repairs a verified defect in the game's shipped Lua,
patched at runtime; no game files are modified.

**Mandatory read, every session: `docs/agent/STATE.md`** — build state, open
gates, active holds. *(Layout live after the docs-restructure chain completes.)*

**Folder contract.** `docs/` root holds ONLY the four human files
(PLAYTEST_CHECKLIST, PLAYTEST_HELP, FUTURE_IDEAS, README) plus `agent/` and
`archive/`. Agent material lives in `docs/agent/` (`bugs/`, `facts/`, `reports/`,
`prompts/`, STATE/WORKFLOW/FIX_POLICY); `docs/archive/` is append-only and
never edited. Generated files say so on line 1 — change `tools/doccheck.py`.

> 2026-08-03 restructure: `docs/BUGS.md` → `docs/agent/bugs/<ID>.md`;
> `docs/STATUS.md` → `docs/agent/STATE.md`; `docs/reports/` →
> `docs/agent/reports/`; `docs/prompts/` → `docs/agent/prompts/`;
> `docs/agent/ENGINE_FACTS.md` → `docs/agent/facts/`. Pre-restructure
> documents cite the old paths; translate mentally, do not edit records.

Before committing doc changes run `python tools/doccheck.py`; red blocks. Set
up once: `git config core.hooksPath tools/hooks`. **Owner decisions go in
`docs/PLAYTEST_CHECKLIST.md` → "Decisions waiting on you", never only in agent
docs.** Authoring: `docs/agent/WORKFLOW.md` · code: `docs/agent/FIX_POLICY.md`
· efforts over ~2 sessions: `docs/agent/reports/CHAIN_METHOD.md`.
