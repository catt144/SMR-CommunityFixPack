---
name: doc-editing
description: Edit Relaunched Fix Pack documentation while preserving owner decisions, obligations and meaning across source documents, maps and generated views. Use before a documentation edit here.
---

# Documentation edits

Check the meaning that doccheck cannot check. Work from the document's existing
purpose and its actual destination passages, not a topic match or a fresh GREEN.

## Before changing the text

- Identify the reader and the action this passage supports. Use `docs/README.md`
  for placement; do not move a rule to a new home without existing authority.
- Identify any owner decision the edit creates, settles or changes. Preserve its
  wording and the condition under which it was made. Reconcile the checklist
  body with its marker's status and whether an action is still owed by the owner.
  A valid marker can still describe yesterday's decision.
- When trimming or retiring a passage, separate settled evidence from remaining
  obligations. Follow the destination's local retirement rule; verify the full
  obligation survives at its home before cutting. A matching heading is not proof.
- If the question requires historical evidence, use smr-orientation's archive
  search route. A default search excludes the archive deliberately.

## Keep regeneration within the edit

For a checklist-only edit, use `python tools/doccheck.py --regen-waiting`.
The full `--regen` reads every entry on disk, including peers' unfinished work.
Before choosing it, inspect changes under both `docs/agent/bugs/` and
`docs/agent/facts/` and compare them with your edit's inputs. Review the resulting
diff: fresh generated output can still contain work outside your change.

## Review meaning after the edit

- For a revised prompt, compare its `prompts/README.md` description with the
  resulting purpose, scope and lifecycle. Filename agreement does not establish
  that the row still describes the job.
- For an owner ruling, check the condition, body and marker together. A fresh
  WAITING register faithfully renders a wrong marker too.
- For a move or a cut, inspect the destination passage and the source diff
  together. Preserve open work and conditions; remove the moved instruction
  from its source in the same change. Do not substitute a size target for this
  check, or restore temporarily suspended caps without the owner's ruling.

This skill supplies judgment checks. It does not verify that an agent invoked it.
