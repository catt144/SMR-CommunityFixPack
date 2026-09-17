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
  wording and the condition under which it was made. A checklist item still
  there must still be owed by the owner; delete it once the owner has acted.
- When trimming or retiring a passage, separate settled evidence from remaining
  obligations. Follow the destination's local retirement rule; verify the full
  obligation survives at its home before cutting. A matching heading is not proof.
- To shrink a document, make deletion the default: each surviving line needs a
  reason, a home, or a slot under a stated cap. Do not defend cuts line by line.
- If the question requires historical evidence, use smr-orientation's archive
  search route. A default search excludes the archive deliberately.

## Keep regeneration within the edit

The full `python tools/doccheck.py --regen` reads every entry on disk, including peers' unfinished work.
Before choosing it, inspect changes under both `docs/agent/bugs/` and
`docs/agent/facts/` and compare them with your edit's inputs. Review the resulting
diff: fresh generated output can still contain work outside your change.

## Review meaning after the edit

- For a revised prompt, compare its `prompts/README.md` description with the
  resulting purpose, scope and lifecycle. Filename agreement does not establish
  that the row still describes the job.
- For an owner ruling, check its condition and body together, and that it lands
  where the role that obeys it reads it; the checklist keeps no rulings.
- For a move or a cut, inspect the destination passage and the source diff
  together. Preserve open work and conditions; remove the moved instruction
  from its source in the same change. Do not substitute a size target for this
  check, or restore temporarily suspended caps without the owner's ruling.

This skill supplies judgment checks. It does not verify that an agent invoked it.
