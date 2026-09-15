# Documentation skills: gate audit and build record

## Evidence and scope

MEASURED 2026-09-15 at `f7db0fdccd0dbde5ded30baf23ef9766b01d4185`:
`git pull` reported already up to date; `git status --porcelain` was empty;
`python tools/doccheck.py` exited 0, `doccheck: GREEN`.
The installed `core.hooksPath` resolves to this repository's `tools/hooks`.
Checks below were read in `tools/doccheck.py`, including their calls from `main()`;
the hook was read too. These are checks of the current working tree, not proof of
the editing process or of invocation. Bootstrap authority is the initiating brief's
explicit instruction to create the missing `doc-editing` skill.

## A. Every item from DOC_RULES_ARCHITECTURE section 5

DROP below means omit a duplicate from the new skill, not retire its source rule.
SKILL identifies the ungated remainder, including a procedure that applies an
existing rule. No classification grants authority to change a rule's meaning.

| Runbook item | Verified check and observed output | Limits and disposition |
|---|---|---|
| Generated bug and fact INDEXes, register, regeneration | `check_index`: `INDEX: fresh`; `check_facts_index`: `FACTS INDEX: fresh`; `check_waiting`: `WAITING: fresh`. Each compares the rendered source with the output. `regen()` writes these outputs. | DROP freshness instructions. The checks cannot prove an editor used regeneration: identical hand-written output also passes. Source-first authority already lives in CLAUDE; no duplicate process rule. Shared regeneration scope is the SKILL row below. |
| CLAUDE/AGENTS drift | `check_entry_mirror`: `ENTRY MIRROR: AGENTS.md == CLAUDE.md, byte for byte (3778 bytes)`. | DROP the mirror duty. It checks equality, not which copy was authored or how long peers saw drift. Source-first authority remains in CLAUDE. |
| Shared tree: status, pathspec, no bypass, regeneration | No applicable gate. The configured hook executes `python tools/doccheck.py --emit-counts || exit 1`; it cannot prevent its own bypass. `regen()` reads every entry on disk. | SKILL: select a contained regeneration operation and review its inputs/outputs before staging. Global status/pathspec duties remain in CLAUDE; do not repeat them. The initiating brief's no-bypass instruction applies to this work. |
| GREEN before commit | Configured pre-commit hook invokes the full `main()` path, including with `--emit-counts`; baseline output ends `doccheck: GREEN`. | DROP. This is an enabled, bypassable hook, not proof that every historical commit passed. |
| Archive search boundary | No archive-search check in doccheck or the hook; `.rgignore` contains `docs/archive/`. | SKILL: choose an explicit archive search when the question requires history. Existing orientation has the commands; route there rather than reproduce them. No new boundary gate: it would not verify an agent's search scope. |
| docs/ folder contract | `check_root` compares README names against `os.listdir(DOCS)` in both directions; output starts `ROOT: docs/ holds exactly the 11 entries docs/README.md's map declares`. | DROP root membership. Semantic placement below agent/ and whether material belongs in a human document are not checked; SKILL: review the intended reader and existing destination passage. |
| Checklist markers and register | `marker_integrity` checks syntax, statuses and duplicate identities: `MARKER INTEGRITY: 96 on disk, 96 parsed; WARN` (agreeing duplicate ck144). `WAITING: fresh` compares a fresh rendering. | DROP syntax/freshness instructions. SKILL: status and owner-action meaning must track the ruling; a syntactically valid stale marker passes. No mandatory-marker gate added (ck177 is outside scope). |
| ck177 retirement | `check_rule_headers` validates header structure/style, not retirement of completed bodies. Output: `RULES HEADERS: PASS - 9 required block(s), 32 canonical header rule(s)`. The checklist preamble still requires moving completed bodies and retaining heading, marker, pointer. | SKILL: distinguish settled content from remaining obligations before moving it. Keep the existing local retirement rule authoritative. No open ck177 marker-enforcement decision is resolved here. |
| Byte caps, temporary raises | `check_state_and_stubs`: `STATE + STUBS: STATE.md 12221 bytes (warn 15360 TEMPORARY, hard 18432, line 200); 3 stubs present and pointing`; header size checks are in `check_rule_headers`. | DROP enforced byte/line thresholds. SKILL: preserve obligations when trimming. Owner-only restoration is an instruction, not mechanically verified; no cap changed or new authority rule duplicated. Skill caps are currently report-only. |
| PROMPT MAP file and row | `check_prompt_map` compares filename sets and rejects struck cells: `PROMPT MAP: PASS` with `agree with disk in both directions; no tombstones`. `prompt_map_rows` discards all description cells. | DROP existence/tombstone duty. SKILL: compare the map description with the revised purpose, scope and lifecycle. A hash proves bytes changed, not semantic accuracy; no reliable cheap semantic gate was established. |
| Owner decisions in checklist | No decision-completeness gate. WAITING reads only its existing source items; it cannot discover an omitted decision in another document or conversation. | SKILL: review whether an edit creates, resolves or changes an owner action and reconcile its condition and marker. The global filing duty remains authoritative in CLAUDE. |

Negative check: `rg -n 'rgignore|177|retir|pathspec|no-verify|git status|R-C|R-G|derived.facts|provenance|execution marker' tools/doccheck.py tools/hooks/pre-commit`
returned comments/messages and an unrelated TestKit index-isolation discussion,
not enforcement of the ungated duties above. The positive check was reading all
gate dispatches in `main()` and the relevant function bodies. These inputs are
plain text; no compressed evidence was searched. Do not infer broad absence
from the keyword search alone.

## C. Prompt-authoring packaging audit

| WORKFLOW element | Existing gate coverage | Disposition |
|---|---|---|
| 1: live list, one commit-and-verify unit per item | No gate in the enumerated dispatcher | SKILL: package the live-list procedure. |
| 2: log, pull, named anchor | No gate | SKILL: retain the staleness anchor. |
| 3: scope and out-of-scope routing | No semantic gate | SKILL. |
| 4: stop conditions | No gate | SKILL. |
| 5: forbidden claims and bounded verdicts | No semantic gate | SKILL. |
| 6: lifecycle | PROMPT MAP enforces membership and tombstones, not choosing the lifecycle or stating it | DROP mechanical pairing prose; SKILL for declaring lifecycle and owner-retained exceptions. |
| 7: probe sweep before testing/recording | `temporary_sweep` scans temporary code; it does not validate brief instructions or a sweep's age | SKILL only after reconciling the source's refusal instruction with the current owner ruling recorded in STATE. No authority to silently restate the old refusal. |
| 8: declared file-level read path | No gate | SKILL. |
| 9 / R-C: fact, measurement, HEAD/build, falsifier; rebase harm legs after a fix | No brief-content gate | SKILL; one body for element 9 and R-C. |
| R-G: executed model | No transcript/model gate; duty already moved to CLAUDE | DROP duplicate global rule; keep the existing duty. |

R-D follows the source section but is outside the brief's specified elements
1–9 plus R-C/R-G; leave it where it is.

## Progress and unresolved scope

- Complete: baseline, gate source/output audit, remainder classifications.
- Complete: doc-editing (`d716d9f`); prompt-authoring with WORKFLOW source removal (`7013326`).
- Complete: pending move 1 disposition.
- Complete: pending move 2 disposition.
- Complete: pending move 3 disposition.
- In progress: size report and proposals.
- Pending: revisit criteria; final verification and consume.

No new gate is selected: syntax and freshness already fail loudly; the remaining
questions concern meaning, authority, timing or an editor's actions. Invocation
is not verified. Skills can guide a reader; they do not prove they were read.

Executed model: GPT-6 (the model identity supplied in this session's instructions;
no finer model/version identifier is exposed in the transcript).

## D. Deferred moves

1. PENDING: commit granularity and same-commit bug-entry timing remain in
   WORKFLOW Per-fix discipline item 4. The fix-authoring destination was not
   created by this task. Neither new documentation skill is that destination;
   copying the clauses there would change their task scope. The local move
   register records this reason. The existence/timing overlap with item 1
   remains a finding to carry when the authorized destination is built.

2. PENDING: the save-selection duty needs the future playtest/fix-authoring
   destination. Its dedicated source brief remains intact; no prose was
   copied into either new skill. The local move register records the reason.

3. PENDING: the warmed-up-save rider line now has a prompt-authoring
   destination. Current register evidence says ck182 is ruled; the initiating
   brief's claim that it remains open is stale. Its explicit PLAYTEST_HELP
   relocation exclusion still limits this task. The dissolution task can move
   this line with its source removal. Neither source nor destination was
   changed for this row; the local register records the scope reason.
