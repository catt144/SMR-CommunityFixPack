# Docs-restructure chain — 4 prompts, run in filename order, delete as you go

Executes `docs/agent/reports/DOC_RESTRUCTURE_SPEC.md` (the DECIDED spec — Fable,
2026-08-03, owner-delegated; do not re-litigate its decisions, DO verify its
facts). Chain mechanics per `docs/agent/reports/CHAIN_METHOD.md` §4 and
`docs/agent/WORKFLOW.md` elements 1-7: staleness check first, inbox/outbox
(`## Notes from upstream`), route-don't-drop (unsure → STOP AND ASK the
owner), self-split on context pressure, self-delete in the close-out commit,
live todo list, commit convention
(`git -c user.name="SMR-BugFixPack" -c user.email="154917955+catt144@users.noreply.github.com"`,
messages via `-F <file>`).

| # | file | model | drains |
|---|------|-------|--------|
| ~~1~~ | ~~`1_tools_baseline_opus.md`~~ | ~~Opus~~ | ~~doccheck v1 green on CURRENT structure + pre-commit hook + CLAUDE.md + checklist decisions section~~ — **DONE 2026-08-03**; hook armed, baseline green |
| ~~2~~ | ~~`2_bugs_split_opus.md`~~ | ~~Opus~~ | ~~BUGS → agent/bugs/ per-entry + generated INDEX + stub, byte-verified~~ — **DONE 2026-08-03**; 116 entry files, 151 INDEX rows, accounting balanced to the line, doccheck v2 green |
| ~~3~~ | ~~`3_folders_state_opus.md`~~ | ~~Opus~~ | ~~agent/ tree, STATE split, facts split, moves, stubs, living-doc sweep, WORKFLOW block~~ — **DONE 2026-08-03**; 43 fact files, STATE.md at 60/60 lines, root allowlist clean, doccheck v3 green with ten negative controls |
| 4 | `4_backward_qa_opus.md` | Opus | conservation QA, folder-empty gate |

Binding rules:
1. **ALL content moves are SCRIPTED** — hand-editing entry/fact content is
   forbidden; reusable scripts live in `tools/`, throwaways in the session
   scratchpad.
2. Every prompt runs doccheck **before and after** its work; red = stop.
3. **Immutable records (`archive/`, `reports/`) are never edited** — the spec
   §4 translation note covers their old paths.
4. Each close-out commit **strikes this table's own row** (manifest-ownership
   rule, CHAIN_METHOD §3).
5. ⚠️ Prompt 3 moves `docs/prompts/` → `docs/agent/prompts/` INCLUDING this
   folder's remaining files — prompt 4 runs from
   `docs/agent/prompts/docs-restructure/`.
6. The playtest campaign may run concurrently; nothing here touches the
   checklist beyond prompt 1's added section, and stubs keep old paths hot.
7. Sizing/placement note (per CHAIN_METHOD §4 step 0): 4 prompts, all Opus —
   the compounding point of this effort was the DESIGN, already spent at the
   top tier (the spec); execution errors are caught mechanically
   (byte-accounting, doccheck, git). Owner may re-route.

## Notes from upstream

(chain-authoring session, 2026-08-03: none — the spec is the inbox)
