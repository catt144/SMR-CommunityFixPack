# Chain prompt 2 — adversarial QA, then build or decline

**Read `README.md` in this folder first — its binding chain rules apply to you.**
Unattended: no game, no keyboard, no owner. Start with `git log --oneline -10` +
`git pull`. **You are the terminal prompt: this folder must be EMPTY when you
finish, and its emptiness is the done-condition.**

You are the adversary and the builder. Two sessions have now touched F11 and
F99 — the one that found them (2026-08-03) and the one that re-derived them
sealed (prompt 1). **Every "done", every "verified", every "clean" either of them
wrote is a claim.** Trust nothing forward; sample against primary evidence.

Then you decide, and you are the one who acts on the decision.

---

## What is actually at stake

**F11.** A one-line fix for a genuine `table.remove` misuse in
`Colonist:ExitVehicle`, shipped and default-on. ⛔ **The owner has decided it
ships — that is closed and you may not re-open it.** What is open: it is
currently a **full copy of a ~30-line shipped method**, and a **pre-wrapper**
conversion has been proposed that would keep the fix while letting the other ~29
lines stay vanilla. You decide whether that conversion gets built, and if so you
build it.

**F99.** A new `cand` entry: `TrackElement.lua:805` dereferences `elements[1]`
after a rebuild that can come back empty; 14 hits in one session, **every one
under `CheatCompleteAllConstructions()`**. You decide its disposition — rider,
fix, or leave it filed — and route the severity call to the owner either way.

---

## Jobs

**Job 1 — todo list up front**, one item per commit-and-verify unit, one in
progress, updated immediately (`WORKFLOW.md` element 1). The owner reads it.

**Job 2 — audit prompt 1.** Read `DERIVATION.md` and prompt 1's outbox below.
Then:

- **Verify the seal held.** `git log --diff-filter=A -- docs/agent/prompts/f11-f99-review/DERIVATION.md`
  should show the derivation committed BEFORE any commit touching `F11.md` or
  `F99.md` in that session. Check it; do not take the attestation's word.
- **Sample its claims against primary evidence** — `ModTools\Src` and the
  archived logs, not against the 2026-08-03 write-ups. Sample at least the
  load-bearing ones: the `SetHolder`/`OnExitHolder` chain, the cross-map
  ordering, the label-membership premise (point 7), and the `TrackElement`
  abort point.
- **Where prompt 1 and the 2026-08-03 session AGREE, ask whether they agree for
  the same reason.** Two sessions reaching one conclusion by the same wrong route
  is the failure this project keeps having; the seal was designed to catch it, so
  spend the check here.

**Job 3 — adjudicate F11's shape.** Decide, with reasons on the record:

- Does the pre-wrapper conversion get built? The case for it is drift: the copy
  freezes shipped lines including a travel-time comfort formula that **F21** is
  itself about. The case against is that any change to working shipped code is
  risk, and the current form is verified while a new one is not.
- If **BUILD**: write it. `FIX_POLICY.md` §3a and §2 bind. Keep the module's
  `SMRFixPack.Require` guards meaningful for the new shape — a guard that no
  longer guards anything is worse than none. Parse sweep (python + luaparser,
  `utf-8-sig`) before the commit. Update the module header comment: it currently
  documents a full-replacement approach and would be lying.
- If **DECLINE**: say why on the F11 entry, so the next session does not
  re-propose it from scratch.
- ⛔ **You may not claim the conversion is verified.** It is behaviour-preserving
  *by construction* at best; it earns `tested` only from a probe suite run or a
  keyboard leg. Say exactly that wherever you record it, and leave the
  verification owed.

**Job 4 — adjudicate F99.** Decide: does it become a checklist rider (with a
**TAKEABLE WHEN <condition>**), a fix, or does it stay filed as `cand`? The
discriminator on the table is one *normally* completed track — drones, no
cheat — on a disturbed element list. Weigh it against `FIX_POLICY` §4a (WHO
BENEFITS): if the line is only reachable through a dev cheat, nobody but us
benefits. **Severity remains an owner call regardless** — make sure it is
routed, not absorbed.

**Job 5 — reconcile the record.** Whatever you decide, `F11.md`, `F99.md`,
`STATE.md` and `PLAYTEST_CHECKLIST.md` must agree with each other and with the
evidence when you are done. Corrections to the 2026-08-03 text are made
**visibly** — the project records overturned reasoning rather than overwriting it
(see how the old F11 audit block was superseded rather than deleted). Owner
decisions go to the checklist's "Decisions waiting on you" with a recommendation.
`python tools/doccheck.py` green before every doc commit; STATE.md is capped at
60 lines, so adding means evicting to `SESSION_LOG.md` in the same commit.

**Job 6 — close the chain and REPORT.** Delete `DERIVATION.md`, this file and
`README.md`; the folder goes away entirely. In the same commit, write the outcome
where it will be found later — a short section on each entry is enough; do not
create a new report document unless there is a finding that belongs nowhere else.
Then report to the owner in the session: what changed, what you overturned, what
you declined and why, and what verification is still owed.

---

## Scope fence

**In:** F11's fix shape, F99's disposition, the correctness of both prior
sessions' reasoning, and the code if you decide to build it.

**Out:** whether the F11 fix ships (owner decided). Any other module. Any live
playtesting or game launch. The `PLAYTEST_HELP.md:312` `ListFixes` staleness
(needs a live reading). D12, PT-62, drone work.

## Stop conditions

- **Prompt 1 and the 2026-08-03 session disagree on a load-bearing premise and
  you cannot settle it from source → STOP. Do not build.** Route the open
  question to the owner with both readings laid out. Building on an unsettled
  premise is precisely what this chain exists to prevent.
- The seal is shown to have been broken in a way that anchored prompt 1 → say so,
  discount its agreement accordingly, and weight your own derivation instead.
- Context running short → self-split (chain rule 4). The folder-empty gate
  belongs to whichever prompt finishes last.

## ⛔ What you may not claim

- **Not** that anything is `tested`. No leg ran in this chain. `tested` is earned
  at the keyboard.
- **Not** that the conversion is safe because it "reads equivalent" — say what
  would falsify that, and leave it owed.
- **Not** that F11's guarded state is unreachable in general; only that specific
  enumerated producers do or do not produce it.
- **Not** that F99 is reachable without the cheat absent a shipped non-cheat path
  to that line, nor that it is unreachable absent a real search.
- **Not** that agreement between two sessions is verification when both may share
  an inherited route.

## Notes from upstream

*(2026-08-03, chain author — the session whose findings you are auditing. My own
soft spots, stated so you can aim at them: the underground-label premise behind
the "index 1513 proves the connected-cities append" claim is mine and unverified;
my "no other producer of a stale `train.units`" position reflects not having
searched, not a search that came up empty; and the pre-wrapper proposal has never
been executed by anything but reading. The F11 measurement I stand behind —
`#units` = 6 and `holder == rocket` exist precisely so the counter could fail —
but the inference drawn from it is fair game, and so is my F99 attribution.)*
