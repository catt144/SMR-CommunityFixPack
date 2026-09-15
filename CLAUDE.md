# Relaunched Fix Pack — Surviving Mars: Relaunched

## Must_Read_Header
<!-- RULES -->
Rule: Read `docs/agent/STATE.md` at the start of every session. [A3: pass]
Rule: Read `Must_Read_Header` before editing a document that has one. [A3: pass]
Rule: Invoke the `doc-editing` skill before editing a document. [A3: pass]
Rule: Do not edit anything in `docs/archive/`. [A3: pass]
Rule: Edit a generated file's source and regenerate the output instead of editing the output. [A3: pass]
Rule: Run `python tools/doccheck.py` before committing documentation changes. [A3: pass]
Rule: Record every owner decision in `docs/PLAYTEST_CHECKLIST.md`, not only in agent documentation. [A3: pass]
Rule: Treat the owner's instruction as authority that agent detection cannot override. [A3: pass]
Rule: Verify command output carrying its command and HEAD or build identifier once without rereading its sources. [A3: pass]
Rule: Treat every authored artifact or message as a claim. [A3: pass]
Rule: Inherit a fact after one check without rederiving it. [A3: pass]
Rule: Read volatile external values with a command every time. [A3: pass]
Rule: Read volatile in-repository status from `STATE.md` and `docs/WAITING_ON_YOU.md`. [A3: pass]
Rule: Verify durable structural facts by fingerprint and rederive only groups that moved. [A3: pass]
Rule: Prove absence with a grep after decoding compressed inputs and count the presence side. [A3: pass]
Rule: Scope every verification command so contrary evidence could make it fail. [A3: pass]
Rule: Run a measurement before writing it and mark unrun measurements `<<PENDING-RUN>>`. [A3: pass]
Rule: Record every count with its command and filter and reconcile each total against its members. [A3: pass]
Rule: Record the executed model from the transcript at close-out. [A3: pass]
Rule: Attribute shared-tree work by commit and diff rather than author identity. [A3: pass]
Rule: Recheck shared paths immediately before writing and stage only owned hunks without a pathspec. [A3: pass]
<!-- /RULES -->

A bug-fix mod: every fix repairs a verified defect in the game's shipped Lua,
patched at runtime; no game files are modified. The tree map is `docs/README.md`.

**Folder contract** (enforced by doccheck). `docs/` root holds the six
human files (PLAYTEST_CHECKLIST, PLAYTEST_HELP, UPLOAD_WORKFLOW, FIELD_REPORT_REPLIES,
FUTURE_IDEAS, README), the BUGS/STATUS stubs, `agent/` and `archive/`. Agent material is `docs/agent/`
(`bugs/`, `facts/`, `reports/`, `prompts/`, STATE/WORKFLOW/FIX_POLICY);
`docs/archive/` is append-only. `INDEX.md` in `bugs/` and `facts/` is generated from
entry and fact files (line-1 banner).
Prompts: the map is `docs/agent/prompts/README.md`. Reusable prompts live in `prompts/perma/`
(ad-hoc work: `perma/DISPATCH.md`; all FR-1/Linux work: `perma/LINUX_DISPATCH.md`).

> Older records cite pre-move paths and the old mod name — translate via `docs/README.md` "Path translation".

Hook setup is `git config core.hooksPath tools/hooks`. `python tools/doccheck.py --regen`
rewrites `bugs/INDEX.md`, `facts/INDEX.md`, `AGENTS.md`, and other generated mirrors.
Authoring: `docs/agent/WORKFLOW.md` · code: `docs/agent/FIX_POLICY.md` · efforts over
about two sessions: `docs/agent/reports/CHAIN_METHOD.md`.

The three trust classes are authority, derived fact, and authored claim; their duties are in the
header above. The open owner decision about the third class remains open.

**`docs/archive/` is hidden from a default `rg`** by a root `.rgignore` — a deliberate boundary, not
a deletion. Explicit archive searches use `rg <term> docs/archive/` or `rg --no-ignore <term>`;
`grep -r` and `git grep` include it. An empty default search is the boundary working.
