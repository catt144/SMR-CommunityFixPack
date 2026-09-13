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
2. **Hazards** — apply all three admission tests below to every line. Headline is
   push; the evidence behind it is pull.
3. **Rules in force** — owner rulings still binding, one line each, dated,
   with a pointer to where they were made. A ruling fully discharged or
   recorded in a policy doc (FIX_POLICY/WORKFLOW) needs only the pointer.
4. **Open owner decisions** — item numbers + five-word gists; bodies live in
   `docs/PLAYTEST_CHECKLIST.md` "Decisions waiting on you".
5. **Build state** — the `--emit-counts` block, verbatim, never hand-typed.

### Hazards admission test (owner ruling 2026-09-13)

**1 · HARM — name the victim.** Who is worse off, and can they be made whole by the next command?
A mechanism is not a victim: *"files get deleted"* is not harm if nobody wanted them. **Floor:
moderate.** Below it, low risk, not worth kernel space.
⛔ **A silent harm outranks a loud one of the same size.** A loud failure self-corrects; a leg that
measures nothing and hands you a number you trust does not.

**2 · UNIVERSALITY — every agent, or one role?** STATE is read by every session, including a
read-only QA pass. If only a release, playtest, junction or triage session can reach it, the rail
belongs in **that role's entry doc**, not the kernel. Destructive rails are role-gated by
construction; the **epistemic** ones — what you may not read-and-conclude, what you may not claim
— are the universal ones.

**3 · GATE — can a machine catch it?** If a hook or tool already hard-fails on it, the kernel line
is belt-and-braces: **cite the gate instead.** If a machine *could* catch it and nothing does, the
entry is a **placeholder** and the real deliverable is the check — the entry leaves when the check
lands.

⇒ **A hazard is a failure that has not yet been converted into a gate.** Graduating is the normal
end of a hazard's life. That is the list's outflow, and without one the list only grows: every
entry was admitted for a real reason, so strictness at the door can never be enough.

Everything else is pull: `SESSION_LOG` (history), `agent/reports/` (evidence),
`agent/bugs/` + `agent/facts/` (defect/fact truth), git graves.

## Procedure

1. Read STATE.md whole. Read the newest SESSION_LOG entry to match its voice.
2. Note the current HEAD sha — it becomes the grave:
   `git show <sha>:docs/agent/STATE.md` is the full pre-eviction file, forever.
2b. ⛔ **Record the owner register BEFORE you touch STATE**, and keep the number:
   `python tools/doccheck.py | grep WAITING` plus the ck numbers themselves,
   `sed -n 's/^| \([0-9]*\) .*//p' docs/WAITING_ON_YOU.md | sort -n`. The register is parsed
   from TWO LITERAL IDIOMS inside STATE — `Owner OWES: ck##` and
   `STILL OPEN: <n> <word>` — so rewording either line DROPS an owner row with no
   error anywhere. The 2026-09-13 eviction lost checklist 53 exactly this way and
   nothing caught it; the note that was added inside STATE is itself byte-capped,
   which is why the check belongs here instead.
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
   emitted block is byte-identical to `--emit-counts` output. Then
   `python tools/doccheck.py --regen-waiting` and diff the register against step
   2b: **no ck number may disappear.** One that does is an owner row you deleted —
   restore the idiom, do not "fix" the register. A row whose status flips to
   ⚠️ _conflict_ is fine; a row that vanishes is not.
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
