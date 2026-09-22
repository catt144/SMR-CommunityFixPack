---
name: smr-orientation
description: Start work or resume a handoff in the Relaunched Fix Pack repo; locate documents, search archives and verify counts, builds or status without loading current work unasked.
---

# Orientation: Relaunched Fix Pack

A bug-fix mod for Surviving Mars: Relaunched. Fixes repair verified shipped-Lua
defects at runtime; game files stay unchanged.

## Must_Read_Header

Status is pull-only (owner, 2026-09-15). Session start does not authorize reading
current work. Read `docs/agent/STATE.md` only when a task, prompt or owner calls
for status; its `NEXT`, `OWED` and `## Hazards` bind you. Read
`docs/PLAYTEST_CHECKLIST.md` only when the task or owner calls for it; new owner
asks must pass its entrance gate.

## Map and generated files

`docs/README.md` is the doccheck-enforced map.

| Material | Home |
|---|---|
| Defects / engine facts | `docs/agent/bugs/` / `docs/agent/facts/`; generated `INDEX.md` in each |
| Process / code rules | `docs/agent/WORKFLOW.md` / `docs/agent/FIX_POLICY.md` |
| Prompts | `docs/agent/prompts/`; `perma/` standing, root live one-offs |
| Human docs | `docs/` root; add no file without its map row |

Emit counts with `python tools/doccheck.py --emit-counts`; never hand-type them.
A `GENERATED` banner means edit the source, never the generated file. Regenerate
with `python tools/doccheck.py --regen`, following doc-editing's shared-input
check; doccheck rejects drift. Edit `CLAUDE.md`; `AGENTS.md` is its generated
byte copy.

## Archive searches

`docs/archive/` is append-only and excluded from default ripgrep by `.rgignore`.
For historical evidence, use `rg <term> docs/archive/` (archive only) or
`rg --no-ignore <term>` (live and archive). An empty default search cannot prove
an archived record is missing. `grep -r`, `git grep` and `git log` ignore
`.rgignore`.

## Evidence and citations

Facts' `derived_at` names their SHA or game build. Run
`python tools/doccheck.py --emit-fingerprint` to route checks: `HOLDS` matches
build identity, not claim validity, scope or dependencies; `MOVED` requires a
new baseline for current claims. Follow smr-bug-library's "Checking facts".
Never assume live `ModTools/Src` still matches an old citation.

## Harness, peers and commits

Read `tools/README.md`, "Hazards on this rig", before shell or git scripting.
Use exact paths and `git commit -F <msgfile> -- <paths>`, never `-a`.
Doccheck must be GREEN; the commit hook enforces it. For peer-shared paths,
including staged hunks, first follow `docs/agent/WORKFLOW.md`, "Committing in a
shared tree": a pathspec does not isolate edits within a file.

- Recheck `git status` and `git log` before shared writes, and
  `git log --oneline -4` immediately before committing. Peers move HEAD without
  a pull; an empty `git log HEAD..origin/main` proves nothing about their work.
  Attribute work by SHA and diff, never author: the git identity is shared.
- Before allocating an EF id, check existing filenames and uncommitted work.
  Prefer a dated observation in the relevant existing entry over a new id;
  directory order alone does not establish the next free number.
- Claude's `ListAgents` does not show Codex sessions. For foreign uncommitted
  work with no visible owner, ask the owner rather than wait on an unreachable
  peer. A quiet run may be awaiting the owner; do not assume it is stuck.
  Check foreign `??` files before treating a one-off as unclaimed, and make
  your own run git-visible.
- Message overlapping peers before editing their entries, STATE or checklist
  items, and before either commits a shared file. Report what actually landed
  with your own SHAs: your commit may discharge work a peer was holding.
  Check your transcript before accepting a peer's attribution of a commit to you.

Before executing a brief, check relevant records for prior owner rulings:
its bug entry, chain README row and, when the task calls for it, checklist.
Follow the later owner instruction and surface any tension rather than silently
resolving it; a brief can omit a ruling.
