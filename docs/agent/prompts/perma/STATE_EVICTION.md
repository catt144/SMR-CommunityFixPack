# STATE_EVICTION — pull-only cleanup job

Use when a task, prompt or the owner calls for STATE cleanup, or when doccheck
warns on its size. One session, docs only, no code. Designed 2026-08-18 with the
owner; the reasoning record is that conversation and the first run's SESSION_LOG
entry.

**The problem this prompt exists for:** `docs/agent/STATE.md` is pull-only but
highly shared when current status is called for, so close-outs are tempted to
wedge verdicts there. Left alone, it compounds; the cure is enforcing the
push/pull boundary below, not compressing history into denser lines.

**Formatting (owner ruling 2026-08-18, checklist 42): most efficient and
safest, nothing else.** doccheck's byte caps do the reading-cost job, so
format purely for machine safety: one fact per line, every line under the
per-line byte cap, stable IDs (`F##`/`EF-###`/`H-##`/item numbers) so grep
lands, no decorative prose, and NEVER widen or pack lines to satisfy any
budget — if content doesn't fit, evict, don't compress.

## The boundary — what earns push (stays in STATE)

STATE is a kernel: **status + pointer, never derivation.** Its status categories are:

1. **Now** — current position and next action. No supersession chains: if a
   sentence needs "superseded by", the superseded half is history — evict it.
2. **Hazard pointers** — apply all three admission tests below to every line. Headline is
   push; the evidence behind it is pull.
3. **Governing pointers** — owner rulings still binding, one line each, dated,
   with a pointer to where they were made. The bodies live in the checklist,
   SESSION_LOG, `CLAUDE.md`, `docs/agent/FIX_POLICY.md` or
   `docs/agent/WORKFLOW.md`; STATE keeps only the current pointer.
4. **Open owner decisions** — item numbers + five-word gists; bodies live in
   `docs/PLAYTEST_CHECKLIST.md` "Decisions waiting on you".

Pull build counts with `python tools/doccheck.py --emit-counts` when needed;
they are no longer stored in STATE (owner's scope override, 2026-09-15,
[checklist record](../../../PLAYTEST_CHECKLIST.md#2026-09-15--state-cleanup-scope-override)).

### Hazards admission test (owner ruling 2026-09-13)

**1 · HARM — name the victim.** Who is worse off, and can they be made whole by the next command?
A mechanism is not a victim: *"files get deleted"* is not harm if nobody wanted them. **Floor:
moderate.** Below it, low risk, not worth kernel space.
**A silent harm outranks a loud one of the same size.** A loud failure self-corrects; a leg that
measures nothing and hands you a number you trust does not.

**2 · UNIVERSALITY — every agent, or one role?** Any session may be directed to read STATE,
including a read-only QA pass. If only a release, playtest, junction or triage session can reach
the hazard, the rail belongs in **that role's entry doc**, not the kernel. Destructive rails are role-gated by
construction; the **epistemic** ones — what you may not read-and-conclude, what you may not claim
— are the universal ones.

**3 · GATE — can a machine catch it?** If a hook or tool already hard-fails on it, the kernel line
is belt-and-braces: **cite the gate instead.** If a machine *could* catch it and nothing does, the
entry is a **placeholder** and the real deliverable is the check — the entry leaves when the check
lands.

**A hazard is a failure that has not yet been converted into a gate.** Graduating is the normal
end of a hazard's life. That is the list's outflow, and without one the list only grows: every
entry was admitted for a real reason, so strictness at the door can never be enough.

Everything else is pull: `docs/archive/SESSION_LOG.md` (history),
`docs/agent/reports/` (evidence), `docs/agent/bugs/` + `docs/agent/facts/`
(defect/fact truth), git graves.

## Procedure

1. Read `docs/agent/STATE.md` whole. Read the newest entry in
   `docs/archive/SESSION_LOG.md` to match its voice.
2. Note the current HEAD sha — it becomes the grave:
   `git show <sha>:docs/agent/STATE.md` is the full pre-eviction file, forever.
2b. **Record the owner register BEFORE you touch STATE**, and keep the count and
   IDs. Run `python tools/doccheck.py --regen-waiting`, record its `WAITING:`
   line, then emit the IDs in PowerShell:
   `(Select-String -Path docs/WAITING_ON_YOU.md -Pattern '^\|\s+\d+\s').Line | ForEach-Object { if ($_ -match '^\|\s*(\d+)\s') { $Matches[1] } } | Sort-Object {[int]$_}`.
   The register is parsed
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
   closed, or have a home + pointer.** Sweep-chain findings are the one
   exception — never restate link verdicts here; point at the chain's own
   findings ledger (forbidden to links) and reports.
4. Rewrite STATE.md to the kernel. Keep its `Must_Read_Header`, grave pointer,
   pull/read-path notice and exact current section headings.
5. Verify: `python tools/doccheck.py` GREEN (it enforces the warn/hard byte
   caps and the per-line cap); every hazard passes the admission test; no
   "superseded" chains remain; open decisions match the checklist. Then
   `python tools/doccheck.py --regen-waiting` and diff the register against step
   2b: **no ck number may disappear.** One that does is an owner row you deleted —
   restore the idiom, do not "fix" the register. A row whose status flips to
   `_conflict_` is fine; a row that vanishes is not.
6. Measure the clean file in bytes and put the before/after numbers in the
   report to the owner.
7. Commit (boring subject — the sweep fence may be live) and push.

Judge the eviction by what a fresh session needs when status is requested, not
by what past sessions were proud of. When meaning or authority is uncertain,
keep the pointer for one more cycle and flag it. Owner-facing asks live in the
checklist, never only here or in STATE.
