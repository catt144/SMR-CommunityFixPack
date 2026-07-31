# BETA READINESS REVIEW — re-runnable assessment prompt

**This is NOT a one-off. Do not delete it when you finish.** It is designed to
be run repeatedly, whenever the owner wants a read on whether the pack is fit to
put in players' hands as a beta. Every run judges the state **at the moment it
runs**.

**Do not run it until the drone work has a settled heading** (owner, 2026-07-31).
Running it mid-redesign produces a verdict about a mod that is about to change.

---

## ⛔ THE ONE RULE THAT MAKES THIS WORTH RUNNING

**Derive every fact yourself. Cite nothing from this document as current.**

This file deliberately contains **no counts, no probe numbers, no statuses, no
dates**. If you find yourself repeating a number you did not personally measure
this run, stop — you are reviewing a memory, not the mod. Docs go stale; this
project has been bitten by exactly that more than once (a "toggles are OFF"
claim that was wrong twice in one day; an audit finding already fixed but still
written as open).

**You are a reviewer, not a builder.** Fix nothing. Change no code. If you find
a defect, file it in `BUGS.md` and keep reviewing. If you find a stale doc,
note it as a finding — correcting it is a separate decision by the owner.

---

## What "beta" means here — the bar you are judging against

Beta is **not** "finished". It is: *fit to put in front of real players who
know it is a beta.* That converts to four questions, in priority order:

1. **Can it hurt them irreversibly?** Corrupted or degraded saves, permanently
   lost progress, damage that survives uninstalling. This is the only category
   where "it's a beta" is not a defence.
2. **Can they get out?** Disable, uninstall, recover. A player who dislikes it
   or hits a bug must be able to return to a working game.
3. **Do they know what they are getting?** The description must match reality —
   including limitations, known-broken vanilla interactions, and anything the
   pack cannot promise.
4. **Will their reports be useful to us?** If a beta tester says "it broke",
   can we tell what happened? This is the question a generic release checklist
   forgets, and for a beta it is nearly as important as (1).

Unfinished work, un-run playtests, and parked ideas are **normal for a beta**
and are not, by themselves, blockers. Say so plainly rather than padding the
blocker list — a review that flags everything is as useless as one that flags
nothing.

---

## PHASE 1 — Establish current state, from sources

Read, in this order, and record what you actually find:

1. `git log --oneline -15` — what landed recently, and is anything mid-flight?
   **If a build session appears to be running, stop and say so.** Reviewing a
   moving target wastes the run.
2. `docs/STATUS.md` — the authoritative counts and the A/B table.
3. `docs/BUGS.md` — the index rows. Build the real status distribution
   yourself (`fixed`, `tested`, `todo`, `wontfix`, design items).
4. `docs/PLAYTEST_CHECKLIST.md` — what verification is outstanding, and what is
   frozen.
5. `docs/FIX_POLICY.md` — the rules the pack claims to follow.
6. `docs/MOD_DESCRIPTION.md` — every claim made to players.
7. `docs/FUTURE_IDEAS.md` — parked items. **These are not blockers and must not
   be reported as outstanding work.**
8. `metadata.lua` + `items.lua` — the shipping manifest.

State clearly at the top of your report **which commit you reviewed**.

---

## PHASE 2 — Hard gates. Any failure is a NO-GO.

These are objective. Do not soften them with judgement.

**G1. The harness is green on the CURRENT head.**
Both shipping configurations measured, **0 FAIL / 0 ERROR**. Not "measured
recently" — measured on what is about to ship. If the last legs predate the
current code, **run them** (the harness facts are in the continuation prompt;
account toggles are player state, so read each leg's own `fix pack present:
N/M fixes active` line rather than assuming the configuration).

**G2. No `[CommunityFixPack]` error / disabled / FAILED lines** in a clean leg,
and no log line naming our `Code/` as the source of an error.

**G3. Shipping manifest integrity.** `metadata.lua`'s `code` list and
`items.lua`'s `ModItemCode` entries must be **identical in content and order**.
A mismatch means an editor round-trip can publish a mod that loads no code at
all. Verify by comparison, not by trust.

**G4. Uninstall safety is demonstrated, not assumed.** A save made with the pack
enabled must load without it. If the uninstall playtest has never been run on
anything close to current code, that is a **NO-GO for beta** — this is gate (1)
and (2) of the bar above, and it is the one thing a beta cannot hand-wave.

**G5. Nothing default-on rests on an unproven defect.** Every default-active
module traces to a BUGS entry with real evidence. A fix shipped default-on
against a suspected-but-unproven defect is a policy violation (`FIX_POLICY` §4)
and a beta risk.

**G6. Player-facing claims are true.** Every number and promise in
`MOD_DESCRIPTION.md` must match what you measured in Phase 1 — fix counts, probe
counts, save-safety claims, module lists. A false claim to players is a blocker
even when the underlying code is fine.

**G7. §4a compliance.** Nothing ships whose only beneficiary is another mod.
Judge by enumeration, never by an entry's self-description — this project has
been burned by an entry that described itself wrongly.

---

## PHASE 3 — Judgement areas. Report, weigh, recommend — do not auto-block.

**J1. Verification depth vs surface area.** How much of what ships has been
seen working in an actual game, as opposed to passing a probe? Probes drive
planted globals and cannot reach code that localised a global at load time —
so a green suite is *not* evidence of in-game correctness. Give an honest read
on the ratio, and name the riskiest untested thing.

**J2. Blast radius of the optional modules.** For each, ask: if this is wrong,
what does it cost the player, and can they undo it? An opt-in module with a
clean off switch and no savegame footprint is a very different risk from one
that writes persistent state. **Recommend explicitly whether each should ship
enabled, disabled, or not at all in a beta.**

**J3. Diagnosability.** If a tester reports "it broke", what can we get from
them? Is there a documented way to capture the pack's state and hand it over?
If diagnosis depends on something a player cannot reach, say so.

**J4. Platform asymmetry — do not skip this.** Console players (Xbox /
PlayStation / MS Store) have **no developer console, no log access, and no
per-fix disable**. Mod Options is the only surface they can reach. So a beta
that is reasonable on PC may not be reasonable on console. **Give a separate
verdict per platform** if they differ, and say why.

**J5. Known limitations, and whether players are warned.** Enumerate what the
pack knows is imperfect — accepted limitations, unfixed vanilla traps that will
generate false reports against us, anything unproven that ships anyway. For
each: is it disclosed in the description? An undisclosed known limitation is a
finding.

**J6. Support load.** What will the first fifty testers most likely report, and
is there an answer ready? A beta that generates reports nobody can act on burns
goodwill for nothing.

---

## PHASE 4 — The verdict

Exactly one of:

- **GO** — ship the beta. List what you accepted as beta-acceptable risk, so
  the owner is agreeing to something specific rather than to your confidence.
- **GO WITH CONDITIONS** — ship once N named, small, checkable things are done.
  Each condition must be concrete enough that someone can tell when it is met.
- **NO-GO** — with the failed hard gates named, and the shortest honest path to
  GO.

**Then, separately: the three things most likely to go wrong in the beta**, with
what would detect each one early. That list is usually more valuable than the
verdict.

### Rules for the verdict

- **A conditional GO with vague conditions is a NO-GO wearing a disguise.** If
  you cannot state a condition precisely, it is not a condition, it is a worry —
  put it in the risk list.
- **Do not pad the blocker list.** Un-run playtests and parked ideas are normal
  for a beta. Blocking on them makes the review worthless as a decision tool.
- **Do not talk yourself into GO either.** If a hard gate fails, the verdict is
  NO-GO regardless of how close everything else is, and regardless of how much
  work has gone in.
- **Say what you could not check.** A review that hides its own blind spots is
  worse than one that names them. You cannot verify in-game behaviour you did
  not observe; say which conclusions rest on source reading, which on probes,
  and which on actual play.

---

## Output

Post the report to the owner and write it into `docs/archive/SESSION_LOG.md` as
a dated entry so successive runs can be compared — **the trend across runs is
the real signal.** Do not overwrite a previous review; add to the record.

If this run produced findings that belong in `BUGS.md` (a real defect) or that
contradict a doc, file/flag them — but **make no other changes**. This review
changes nothing except what is known.
