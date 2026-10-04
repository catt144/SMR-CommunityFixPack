# Clean up `RULE_PLACEMENT_TEST.md` into the casebook behind the rule-placement skill

**One-off. Authored 2026-09-29 at `2b69662`.** Start with `git log --oneline -3` and `git status --short`.
The tree is shared, so re-check both before each write.

## Authority and outcome

The owner asked for this file to be cleaned up: *"It almost reads less like a test and more like a
journal of examples."* Since 2026-09-17 the test itself has lived in the `rule-placement` skill:
canonical copy at `C:\Users\stkot\.claude\skills\rule-placement\SKILL.md`, Codex copy at
`.agents/skills/rule-placement/SKILL.md`. `docs/agent/reports/RULE_PLACEMENT_TEST.md` (19,468 B at
authoring) is still the raw record of the 2026-09-14 design session. It mixes three things: the
test, which the skill now duplicates; the worked cases; and a build spec that is mostly unbuilt.

**End state.** The file is the casebook behind the skill. It holds:

1. **What this file is.** One short paragraph: the test is the skill; this file holds the cases and
   calibration that show how to apply it; and the owner's authority clause stays in the skill. Do
   not restate the skill's question, disposition table or shapes table. Key each case to the
   disposition or shape it illustrates instead.
2. **Cases, one per disposition or shape.** Each case gives the rule as quoted, what actually stops
   it, the disposition, and its evidence (receipt) as a repo path re-derived today. The source
   material is:
   - the "Ground rules" teardown (compact table)
   - F104 (a rule violated in practice is a wish)
   - TestKit upload (CANNOT; structure was the protection)
   - `git checkout --` (WOULD NOT, kept because an incident happened)
   - the SMRTK nonce line (an earned WOULD NOT)
   - Ground rules 2, 4 and 5a (NOT A RULE)
   - the habit wearing a rule's clothes

   You judge which cases earn a place, and whether two can be merged.
3. **Calibration.** The method points only:
   - find duplicates by meaning, not by string
   - a grep cannot bound a class defined by meaning
   - report both numbers, occurrences and distinct rules after merging
   - an inventory that classifies placement never asks whether something is a rule at all
4. **The rule-creation criteria.** Keep the owner's four verbatim, and the seven added requirements
   with the case that earned each. Label them *agreed 2026-09-14, not built*: no skill applies
   them, and the `[A3: pass]` tag does not test them.
5. **The machinery agreed 2026-09-14, as a status table.** One row per part (marker and header,
   coverage record, count-did-not-move warning, rule-creation skill, eviction rule sweep). Each row
   gives the owner's words, *built* or *not built*, and the command that shows it. Re-derive every
   status yourself. At authoring, only the marker and header was found built (`RULE_STYLE_RE` in
   `tools/doccheck.py`); the other four had no trace in `doccheck.py` or `STATE_EVICTION.md`.
   **The owner ruling that the eviction may not retire a rule, only elevate it to the owner, has no
   other home.** It survives verbatim.
6. **The scope note** ("a placement test, not a licence to delete").

Readable for the owner: plain headings, emphasis only where it carries meaning, and no emoji
stacks (`doc-editing`, "Reader and trimming").

**Completion evidence:**
- one commit
- `doccheck: GREEN`
- byte counts before and after from `wc -c`
- the blind check's result table
- the grep described under "Pointers" returning no stale hits, with its positive control

## Delegated judgment

Wording, order, merges, and which cases earn a place are yours. Record the calls in the commit
message. Default to deletion within preservation. **Content already recorded elsewhere is deleted,
not re-archived.** For example, the 2026-09-18 saves ruling is homed in `docs/agent/WORKFLOW.md`
(`grep -n "wrong anyway"`), so it leaves this file. Before you cut anything, prove the destination
body holds it: a heading match is not proof.

These go without replacement:
- measurements true only on 2026-09-14 (`^Rule:` in 1 file, the 66-file heading count, the 852
  inventory's figures), except where a case needs one as its receipt, dated
- checklist item numbers that are no longer open (`grep -n "### ck" docs/PLAYTEST_CHECKLIST.md`)
- the pointer to `HANDOFF_PROMPT.md` §6. That file is gitignored and rewritten, so a committed
  document must not cite it. The `git checkout --` incident is recorded in `tools/README.md`,
  "Hazards on this rig" (`grep -n "checkout --" tools/README.md`); point there.

## Work list and procedure

Use the todo tool before your first write, with one item in progress at a time.

1. **Inventory first.** Before editing, write `scratch/rule_placement_inventory.md` listing every:
   - owner quote, verbatim
   - owner ruling, with its date
   - disposition and shape
   - criterion (all eleven)
   - case, with its receipt
   - machinery part

   Give each item its line in the current file.
2. **Rewrite** the file to the end state.
3. **Pointers.** Two skill copies name this file's sections:
   - `doc-editing` (`.claude/skills/doc-editing/SKILL.md` and `.agents/skills/doc-editing/SKILL.md`)
     cites §§ "The question", "Audit criterion" and "Calibration".
   - `rule-placement` (canonical first, then the `.agents/` copy) describes what the file holds.

   Change only the pointer sentence in each to match the new sections; doccheck fails on mirror
   drift. Then run `rg -n "RULE_PLACEMENT_TEST" --glob '!docs/archive/**'`, and justify every hit
   or fix it. Positive control: the same `rg` must hit the `doc-editing` pointer.
4. **Blind check.** Launch a fresh-context subagent per the `subagents` skill. Give it only the
   inventory, the new file and the skill. It returns, for each inventory item, one of: *present*
   (where), *in the skill*, *homed elsewhere* (path and the passage), or *missing*. Confirm each
   *homed elsewhere* yourself with a command. A *missing* item is restored, or its cut is justified
   in the commit message by the test's disposition.
5. **Commit.** `python tools/doccheck.py` must be GREEN. Commit with a pathspec: this file, the four
   skill copies you touched, and this prompt's removal. The canonical skill is outside the repo and
   is not committed; name its change in the commit message. In the same commit, **delete this
   prompt and its row in `docs/agent/prompts/README.md`.**

## Scope

**In:** the file, the four skill pointer sentences, and this prompt's retirement.

**Out:** changing the test itself. That means any wording in either skill beyond the pointer
sentence, and adding the expiry condition or any criterion to the skill. Also out: building any
machinery part, and editing anything under `.claude/` other than the tracked
`.claude/skills/doc-editing/SKILL.md` pointer sentence named in step 3. Report outside findings
in your final message.

## Resume (added 2026-10-04)

A first run did steps 1, 2 and 4 on 2026-09-29 and stopped correctly. This brief contradicted
itself: step 3 named `.claude/skills/doc-editing/SKILL.md`, and this Scope's Out line excluded
`.claude/`. That is now resolved above. The run's rewrite is uncommitted in the working tree;
its inventory, checks and blind-check result are in `scratch/rule_placement_*`. The blind check
found no preservation gap. **Continue from the tree; do not start again.**

What is still owed:
- **The TestKit case is stale.** The run rechecked it at 12:11 on 09-29, finding no remote. At
  15:51 the same day, `92e9418d` gave the kit the private remote `catt144/SMR-CommunityTestKit`,
  and `docs/agent/WORKFLOW.md`, Layout, now records it. Re-derive the case under the test: which
  upload routes are still structurally closed, and which are now open. The case shows criterion 5
  (expiry) firing. Do not decide whether a rule should come back; report that as an owner ask.
- **Step 3.** `doc-editing` cites §§ "The question" and "Audit criterion", and the rewrite has
  neither. Repoint it.
- **Step 5.**
- **One more blind-check pass** over the changed TestKit case only.

## Stops

Report instead of continuing if:
- the file or a skill copy is dirty or held by a peer;
- a cut would remove an owner quote or ruling that has no other home; or
- matching a pointer needs more than its one sentence.

## Claim limits

- "Shorter" does not mean "preserved"; the blind check is the evidence.
- "Built" means a command shows the gate or sweep firing, not a grep for its name.

## Owner asks to return, not act on

End your final message with these for the coordinator seat to file:
- whether the skill should gain the expiry condition (criterion 5) and the incident-or-mechanism
  bar (criterion 7), the costliest unbuilt parts;
- whether the unbuilt machinery rows stay planned, get scheduled, or retire.
