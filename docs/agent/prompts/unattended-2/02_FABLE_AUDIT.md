# Chain prompt 2 — adversarial audit, integration, chain close

**Read `README.md` in this folder first — binding chain rules apply. You are
the terminal prompt: this folder must be EMPTY when you finish.** Unattended.
Start with `git log --oneline -10` + `git pull`. Todo list up front.

**Read path**: this folder's remaining files · the outbox below · every
entry/checklist line prompt 1 touched · the archived logs it cites · every
module/TestKit file it edited (diff the shipped Lua against the entry's
described change — the CODE is a claim too) · the audit precedents
(`git show 0b22bc4^:docs/agent/prompts/corun-batch-2/03_FABLE_AUDIT.md` had
no build to audit; the batch-2 close record in SESSION_LOG 2026-08-10 sets
the log-fidelity floor).

**Every "done", "PASS", "SKIP" and "repaired" upstream is a claim.** This
chain SHIPPED CODE, which raises the floor: the audit verifies the shipped
diff against the entry's decision block AND against Src (README rule 13),
not just the log against the record.

## Jobs

**Job 1 — audit the record against the archived logs and the shipped code.**
Byte-compare every archived log against its on-disk original over the FULL
length; read the WHOLE log yourself. Per item: **F48** — the pass's repair
count line exists (R7), the case-A repair held across the R4 round trip, the
clean-fixture run reports zero, and the shipped diff is exactly the corrected
call the entry specifies (Src-verify the site yourself — trust nothing
carried). ⛔ If prompt 1 shipped on a failed acceptance, the audit REVERTS
and routes — that is a stop-condition breach, not a judgment call. **C43** —
the suite log carries zero TestKit `[LUA ERROR]`, the SKIPs print their
reason, no other probe verdict flipped, and the `set_global` caller count
landed on the entry. **F100** — the new line is in the boot log verbatim and
`81/81 active` holds. **PT-35 leg A** — every read has its before/after AND
its round trip; APPLICABLE=true on the turbine half (population 1, not 0);
zeros state their sampled condition. Forced/organic labels present (all
forced); no `tested` granted anywhere (nothing here can earn it). Commit
discipline: probes deleted, sweeps present, staged copies gone,
**`PT35FIXTURE.savegame.sav` and `TEST2H TRAIN` present and byte-verified**,
every cited log `git show`-verified. ⛔ A missing archived log is an
automatic finding. Whole-log sweep: unexplained lines with their age;
`TrackElement.lua:805` (an ORGANIC hit reopens F99 per the owner's
passive-watch ruling — route it); `invalid pos with no holder` (C45's
settling grep — a hit here is its second occurrence, record per its entry).

**Job 2 — status honesty.** F48's status matches what actually held
(`fixed` needs 4a+4b+4c; anything less stays `directed` with the gap named).
C43/F100 close only if their acceptance readings are in the archived log.
PT-35: leg A's turbine half either moves to its archive-ready state (case A
complete IN FULL — say whether the section archives or what remains) or
records exactly which read failed. Corrections visible, never silent; a
correction that changes a verdict re-routes that item to the owner.

**Job 3 — the ledger.** Prompt 1's misses vs the standing harness-rule
blocks (unattended-1's 1–4, batch-1's 1–6, batch-2's 1–9): what recurred (a
rule that fails twice is broken — say which and repair it in WORKFLOW
surgically), what is NEW. Economics one line (machine time; owner cost =
the kickoff word).

**Job 4 — integrate and close.** Entries verified carrying their verdicts;
checklist PT-35 line final; `STATE.md` chain CLOSED + outcomes + NEXT
(cap 60); `SESSION_LOG.md` record newest-first; `CHAIN_METHOD.md` one row
ONLY if this chain taught something the method does not already record.
Delete every remaining file in this folder in the closing commit (cite the
pre-deletion sha in the SESSION_LOG record). doccheck GREEN, push. **The
owner report ENDS with the next-chain kickoff** (chain rule 14): the
expected front is the **PT-20 redo co-run** (+ the 10-second Ctrl-F9 check
that settles F85) — if its chain is not yet authored, say so plainly and
name what authoring it takes.

## Stop conditions

- A load-bearing verdict fails its audit and the logs cannot settle it →
  correct visibly, re-route to the owner, keep closing.
- The run was partial → audit what ran, inventory the remainder into
  TAKEABLE riders with staged state cleaned up, and still empty the folder.

## ⛔ What you may not claim

- Not `tested` for anything — no owner eyes were anywhere in this chain.
- Not "the sanitizer is safe" in general — one fixture, one lineage; PT-35
  cases B/C stay parked and the do-no-harm claim stays scoped to what ran.
- Not any owner decision — F85 waits on its Ctrl-F9 evidence; the relabel
  wording stays owed; nothing this chain finds changes a ruling on its own.

## Notes from upstream

*(Prompt 1 appends its outbox here before self-consuming.)*
