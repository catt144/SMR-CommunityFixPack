# STATE_EVICTION — standing cleanup prompt (reusable; do not delete after a run)

Fired by the owner whenever doccheck WARNs on STATE.md's size, or on their own
call. One session, docs only, no code. Designed 2026-08-18 with the owner; the
reasoning record is that conversation and the first run's SESSION_LOG entry.

**The problem this prompt exists for:** STATE.md is the one mandatory read, so
every close-out is tempted to wedge its verdicts there — presence in STATE has
felt like the only guaranteed audience. Left alone, the file compounds (it hit
71,077 bytes = 33,066 tokens on 2026-08-18 while satisfying its then 60-line
budget — lines became walls). The cure is not a summary pass; it is enforcing
the push/pull boundary below.

**Formatting (owner ruling 2026-08-18, checklist 42): most efficient and
safest, nothing else.** doccheck's byte caps do the reading-cost job, so
format purely for machine safety: one fact per line, every line under the
per-line byte cap, stable IDs (`F##`/`EF-###`/`H-##`/item numbers) so grep
lands, no decorative prose, and NEVER widen or pack lines to satisfy any
budget — if content doesn't fit, evict, don't compress.

## The boundary — what earns push (stays in STATE)

STATE is a kernel: **status + pointer, never derivation.** Five sections only:

1. **Now** — current position and next action. No supersession chains: if a
   sentence needs "superseded by", the superseded half is history — evict it.
2. **Hazards** — admission test, applied per line: *it names an action an agent
   could take unattended, states the rail, and points to the detail.* Anything
   that fails the test is orientation, not a hazard — evict it. Headline is
   push; the evidence behind it is pull.
3. **Rules in force** — owner rulings still binding, one line each, dated,
   with a pointer to where they were made. A ruling fully discharged or
   recorded in a policy doc (FIX_POLICY/WORKFLOW) needs only the pointer.
4. **Open owner decisions** — item numbers + five-word gists; bodies live in
   `docs/PLAYTEST_CHECKLIST.md` "Decisions waiting on you".
5. **Build state** — the `--emit-counts` block, verbatim, never hand-typed.

Everything else is pull: `SESSION_LOG` (history), `agent/reports/` (evidence),
`agent/bugs/` + `agent/facts/` (defect/fact truth), git graves.

## Procedure

1. Read STATE.md whole. Read the newest SESSION_LOG entry to match its voice.
2. Note the current HEAD sha — it becomes the grave:
   `git show <sha>:docs/agent/STATE.md` is the full pre-eviction file, forever.
3. Prepend ONE SESSION_LOG entry (below the preamble; archive entries are
   never edited): a digest of each closed effort being evicted — a few lines
   each, dated, with pointers to its reports/graves — opening with a
   `tags:` line listing every F##/C##/D##/EF-###/item-## the entry touches, so
   future greps land here. **Move, never delete: every evicted claim must be
   closed, or have a home + pointer.** ⛔ Sweep-chain findings are the one
   exception — never restate link verdicts here; point at the chain's own
   findings ledger (forbidden to links) and reports.
4. Rewrite STATE.md to the kernel. Keep the mandatory-read header, the grave
   pointer, and the read-path pointers.
5. Verify: `python tools/doccheck.py` GREEN (it enforces the warn/hard byte
   caps and the per-line cap); every hazard passes the admission test; no
   "superseded"/"⇒" chains remain; open decisions match the checklist; the
   emitted block is byte-identical to `--emit-counts` output.
6. Measure the clean file (bytes; tokens ≈ bytes/2 for emoji-dense prose to
   bytes/4 for plain text — the 08-18 file measured 2.15 B/token) and put the
   numbers in the report to the owner, beside the pre-eviction size.
7. Commit (boring subject — the sweep fence may be live) and push.

## Rules

- Fresh context preferred: the evicting session should not be the session
  whose material is being evicted.
- The eviction is judged by what a fresh session NEEDS at boot, not by what
  past sessions were proud of. When in doubt whether something is still
  load-bearing, it stays one more cycle and gets flagged in the report.
- Owner-facing asks always live in the checklist, never only here or in STATE.
