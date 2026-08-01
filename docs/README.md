# docs/ — layout, and where new things go

Reorganised 2026-08-01 (owner). The folder had grown to 28 flat files and the
reports were burying the daily-truth documents.

## Where things live

**`docs/` (root) — daily truth. Read these; they are maintained.**

| file | what it is |
|---|---|
| `STATUS.md` | **read first.** Current state, rewritten in place every session |
| `BUGS.md` | defect truth — every F/D entry, its evidence and status |
| `PLAYTEST_CHECKLIST.md` | the PT tests + the reporting protocol |
| `PLAYTEST_HELP.md` | all playtest reference material — console facts, command table, fixtures |
| `PLAYTEST_ARCHIVE.md` | passed PTs, moved out of the checklist |
| `FUTURE_IDEAS.md` | **parking lot, NOT a backlog.** Nothing in it is work |
| `MOD_DESCRIPTION.md` | player-facing release text |

**`docs/agent/` — the rules an agent reads every session.** Small, stable,
binding.

| file | what it is |
|---|---|
| `ENGINE_FACTS.md` | hard-won engine behaviour. **Read before writing any fix** |
| `FIX_POLICY.md` | what is allowed to be built, and how |
| `WORKFLOW.md` | process rules — commits, probe hygiene, todo discipline |

**`docs/prompts/` — the two standing prompts plus any live one-off.**

| file | what it is |
|---|---|
| `FABLE_NEXT_PROMPT.md` | the **general** continuation prompt (historic filename; model-neutral) |
| `DRONE_PROJECT_PROMPT.md` | owns all drone work — re-runnable |
| others | live one-off prompts, consumed when their deliverable lands |

**`docs/reports/` — reports, plans, specs, surveys.** Written once, cited
after; not maintained line-by-line the way root docs are.

**`docs/archive/` — spent.** History and retired material. `SESSION_LOG.md`
lives here (append-only, newest first) and is still written every session.

## Where NEW things go

- A **rule or engine fact** → `agent/`. If it binds future work, it belongs here,
  not buried in a report.
- A **prompt** → `prompts/`. One-offs are deleted or archived when consumed.
- A **report, plan, spec, audit or survey** → `reports/`.
- A **defect** → `BUGS.md`. Never a report, never `FUTURE_IDEAS.md`.
- A **session leg** → `archive/SESSION_LOG.md`.
- **Spent** anything → `archive/`.

⚠️ **Reports are not authority.** When a report and `BUGS.md`/`ENGINE_FACTS.md`
disagree, the root/agent document wins — or the report is wrong and should be
corrected in the same change that discovers it.

## Retired 2026-08-01

- `F86_ADJUDICATION_PROMPT.md` → `archive/` (verdict delivered)
- `DRONE_RESEARCH_BRIEF.md` → `archive/` (all four gates ANSWERED)
