# Relaunched Fix Pack — Surviving Mars: Relaunched

## Must_Read_Header
<!-- RULES -->
Rule: Read `Must_Read_Header` before editing a document that has one. [A3: pass]
Rule: Invoke the `doc-editing` skill before editing a document. [A3: pass]
Rule: Append to `docs/archive/` only; never rewrite or delete what is archived there. [A3: pass]
Rule: Edit a generated file's source and regenerate it, never the output. [A3: pass]
Rule: Run `python tools/doccheck.py` before committing documentation changes. [A3: pass]
Rule: Ask the owner for a decision in `docs/PLAYTEST_CHECKLIST.md` and record the ruling where the role that obeys it reads it. [A3: pass]
Rule: Treat the owner's instruction as authority that agent detection cannot override. [A3: pass]
Rule: Verify command output carrying its command and HEAD or build identifier once without rereading its sources. [A3: pass]
Rule: Treat any authored artifact or message other than the owner's instruction as a claim, cleared by one check rather than a re-derivation. [A3: pass]
Rule: Read volatile external values with a command every time. [A3: pass]
Rule: Read `docs/agent/STATE.md` and `docs/PLAYTEST_CHECKLIST.md` only when a task, a prompt or the owner calls for them; current work is pull, never session-start reading. [A3: pass]
Rule: Verify durable structural facts by fingerprint and rederive only groups that moved. [A3: pass]
Rule: Cite a game source line with the build it was read on, from that build's archived tree. [A3: pass]
Rule: Prove absence with a grep after decoding compressed inputs and count the presence side. [A3: pass]
Rule: Scope every verification command so contrary evidence could make it fail. [A3: pass]
Rule: Run a measurement before reporting it; mark `<<PENDING-RUN>>` any figure written before its command ran. [A3: pass]
Rule: Record every count with its command and filter and reconcile each total against its members. [A3: pass]
Rule: Record the executed model from the transcript at close-out. [A3: pass]
Rule: Attribute shared-tree work by commit and diff rather than author identity. [A3: pass]
Rule: Recheck shared paths before writing; commit with a pathspec unless partial hunks of a peer-shared file are staged, which a pathspec would discard. [A3: pass]
Rule: Delegate work to a subagent when that costs less than doing it in your own context. [A3: pass]
Rule: Give each subagent the lowest model tier that can do its task, and tier 3 only when a lower tier's result would need redoing. [A3: pass]
Rule: Set each subagent's effort explicitly; going above your own tier or a tier's effort cap needs the owner's approval, asked with a justification. [A3: pass]
<!-- /RULES -->

A bug-fix mod: every fix repairs a verified defect in the game's shipped Lua,
patched at runtime; no game files are modified. The tree map is `docs/README.md`.

**Folder contract** (enforced by doccheck). `docs/` root holds the five
human files (PLAYTEST_CHECKLIST, UPLOAD_WORKFLOW, FIELD_REPORT_REPLIES,
FUTURE_IDEAS, README), the BUGS/STATUS stubs, `agent/` and `archive/`. Agent material is `docs/agent/`
(`bugs/`, `facts/`, `reports/`, `prompts/`, `support/`, STATE/WORKFLOW/FIX_POLICY);
`docs/archive/` is append-only. `INDEX.md` in `bugs/` and `facts/` is generated from
entry and fact files (line-1 banner).
Prompts: the map is `docs/agent/prompts/README.md`. Reusable prompts live in `prompts/perma/`;
all FR-1/Linux work uses `perma/LINUX_DISPATCH.md`.
Prompt-supporting protocols and references live outside that tree in `docs/agent/support/`.

> Older records cite pre-move paths and the old mod name — translate via `docs/README.md` "Path translation".

Hook setup is `git config core.hooksPath tools/hooks`. `python tools/doccheck.py --regen`
rewrites `bugs/INDEX.md`, `facts/INDEX.md`, `AGENTS.md`, and other generated mirrors.
Authoring: `docs/agent/WORKFLOW.md` · code: `docs/agent/FIX_POLICY.md` · efforts over
about two sessions: `docs/agent/support/CHAIN_METHOD.md`.

The three trust classes are authority, derived fact, and authored claim; their duties are in the
header above. The open owner decision about the third class remains open.

**Model tiers** for the subagent rules: 1 = Sonnet / Codex Terra · 2 = Opus / Codex Sol ·
3 = Fable / Codex Astra. Tier 1 reasons less deeply; with good instructions it handles doc work,
pre-planned builds and simple investigation. Tier 2 is for work that needs depth. Haiku and Codex
Luna are unused: too light in reasoning, with far less context than the 1M of tiers 1-3. Effort
caps: tier 1 xhigh · tier 2 high · tier 3 high. On this machine, Claude Code sets effort through
the `tier<N>-<effort>` types in `.claude/agents/`; a bare model choice inherits the session's effort.

**`docs/archive/` is hidden from a default `rg`** by a root `.rgignore` — a deliberate boundary, not
a deletion. Explicit archive searches use `rg <term> docs/archive/` or `rg --no-ignore <term>`;
`grep -r` and `git grep` include it. An empty default search is the boundary working.
