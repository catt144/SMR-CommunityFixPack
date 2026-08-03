# One-off — Playtest checklist redesign (Opus; run AFTER the docs-restructure chain completes)

**⛔ Gate: `docs/prompts/docs-restructure/` (or its post-move location
`docs/agent/prompts/docs-restructure/`) must be EMPTY before this runs** —
both efforts edit `PLAYTEST_CHECKLIST.md` and concurrent edits will conflict.
Staleness check first (`git log` + `git pull`). WORKFLOW elements 1–7 apply;
self-delete on completion.

## Why (owner, 2026-08-03, verbatim substance — this is the design authority)

The checklist as written is not how the owner tests. Actual workflow: get the
basics from the checklist, open an agent session, test live, and give the
agent observations **in the moment** — *"when giving it flushes in the moment
we often find out more than if I just jotted notes down and told it to trust
me."* The pre-written expectations, predictions tables, pass/fail readings and
forensic protocols are bloat on the human surface: the agent supplies all of
that context live from the entry, and links things in the logs that would take
the owner hours. And ordering by PT number burns time — the owner once ran
five train PTs spread across the numeric order instead of knocking them out
back-to-back in one sitting.

## The format (per test — NOTHING more)

```
### PT-XX — <short human name>                     Status: unrun|partial|blocked
**Bug:** 1–3 sentences, plain language, + entry link (agent/bugs/<ID>.md).
**Setup:** numbered, detailed — the part the owner actually needs.
**Requires:** hard preconditions (colony state, law enacted, save vintage…).
**Good to have:** non-blocking extras that improve the reading.
```

Explicitly REMOVED from the human surface (NOT from the project): predictions
tables, expected readings, pass/fail criteria, console forensics, method
warnings. **Those live in the linked entry and in the sitting itself** — the
protocol note below preserves the discipline.

## Structure

1. Top of file keeps: the "Decisions waiting on you" section (chain-added),
   the uptime convention line, and a **"Do first" queue** (currently: PT-62
   remainder → load-heal round-trip sweep → doctrine C-sitting, per
   CHAIN_QA_REPORT §9).
2. **Group by system, not by number**: Trains · Drones/hubs · Disasters ·
   Rockets/landers · Colonists/domes · UI/misc (adjust to what the tests
   actually cluster into — merge the §3 needs-eyes riders into their system
   groups). A sitting clears a group. PT codes are KEPT verbatim; numbering
   is identity, grouping is order.
3. **Protocol section (short)**: a sitting = owner + live agent session. The
   agent pulls full context from the entry, writes its predictions
   BEFORE the leg (the discipline stays — it moves from the document to the
   sitting; PT-61 is the proof it pays), hands one-command-per-line console
   steps, and records results/archive/status flips per the existing
   reporting protocol. The owner supplies observations; the agent supplies
   expectations and log links.

## Migration safety (the checklist is the owner's heaviest doc — no lost bytes)

1. FIRST: append the ENTIRE current checklist verbatim to
   `docs/archive/PLAYTEST_ARCHIVE.md` under a dated banner
   "pre-redesign snapshot 2026-08-03" — nothing is lost, then the rewrite is
   free to be aggressive.
2. Rewrite each live section into the format above: Setup/Requires extracted
   from existing text (condense, don't invent); anything not fitting the
   four fields is NOT carried — it survives in the snapshot and the entries.
   If a PT's expectations content is NOT in its linked entry and seems
   load-bearing (e.g. PT-61-style predictions that were never entry-side),
   move it INTO the entry (or agent/bugs/ file) rather than deleting.
3. **⭐ CHECKPOINT: convert ONE group first (Trains) and show the owner the
   result for approval before converting the rest.** The owner's read is the
   acceptance test for a human doc; iterate on their feedback.
4. doccheck must stay green throughout (the hook is armed).

## Close-out

Update STATE.md pointer, note the redesign in the archive banner, delete this
file, commit (`-F` message file, house convention), push.
