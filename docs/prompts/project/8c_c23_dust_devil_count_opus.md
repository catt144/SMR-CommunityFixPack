# Chain 8c — C23 item 1: the dust-devil count truncation, on its own leg

> ## ⛔ SEALED: `docs/reports/BLIND_AUDIT.md` — DO NOT OPEN
>
> **This prompt is FORBIDDEN from reading, grepping, summarising, or acting on
> `docs/reports/BLIND_AUDIT.md` or any part of its contents.**
>
> It is a **blind control**: a fresh session produced it having deliberately read
> no project docs, and its whole evidential value is that it was written without
> the project's own conclusions in view. **Prompt 12, job 6b** examines it against
> the full record it was forbidden to see — doing its own pass FIRST, then opening
> the sealed key — precisely so that neither reading anchors the other. **A prompt
> that reads it early destroys that independence, and the contamination cannot be
> detected afterwards.**
>
> - Do not open it. Do not `grep`/`Read` it. Do not ask a subagent to.
> - **If a broad search incidentally surfaces its contents: stop, discard, do not
>   use it, and say so in your handoff notes.**
> - The blanket pre-clearance does NOT cover opening it. **Only prompt 12 may.**

**One-off; delete this file in your final commit. Read `README.md` in this
folder first.**

**Staleness check: `git log --oneline -15` + `git pull`.** This prompt was
written at **`8f58f30`**. **Gate: `8b` must have landed and run its leg**, because
this build touches the dust-devil scheduler and `8b` ships **F93**, which patches
the same subsystem (the descriptor-map read). Building both against one unrun leg
is how two changes to one scheduler become one unattributable result.

## Why this is its own prompt

Chain prompt 8 made the scale call the brief asked it to make, and split.
**Prompt 8's own batch was ten build units before this one; this item is
Tier-1-scale work on a P3 item and does not belong in a shared leg.** The owner's
words when approving it are the reason the split is conservative rather than
lazy: *"build it, accept the thread — for now, but it's not locked. I want the QA
run to personally review it and provide feedback."*

So: **it is a build**, chain prompt 12 has a standing job (**job 8**) to
re-examine the decision, and **the owner may reverse it**. Do not treat it as
settled precedent for anything else, and do not let its existence justify a
second sleeping thread anywhere.

## Jobs (todo list first; one item per commit-and-verify unit)

1. **Read the C23 entry's build spec in full before starting.** ⚠️ **This is NOT
   the small fix an earlier draft of the chain notes described** — that
   description was corrected the same day. ⛔ **The "§1.4b replacement of the
   count line" that draft promised DOES NOT EXIST.** The defective line is
   **inside the `GlobalGameTimeThread("DustDevils", …)` body**, so the fix means
   owning a **sleeping game-time thread** — a **14th §3a exposed site**.
2. **Build it**, against the three edges below, two of which have already bitten
   this project.
3. **Its probe** (TestKit; explicit `return "PASS", …` — the fall-off-the-end
   trap is documented).
4. **Its own A/B leg + a long soak.** Stale-probe gate first; predictions written
   down before launching. The verification rider is on the entry: **`VeryHigh_3`,
   3-4 per wave before, 0-or-6-8 after, dust storms off.**
5. **A recorded per-site disposition in `SAVE_SAFETY_REDESIGN.md`** — this adds a
   site to the exposed set, and §3a's release gate is per-site.
6. STATUS.md: counts, result, remaining tail.

### The three edges

1. **The F88 trap.** `RestartGlobalGameTimeThread` re-rolls the pending wave
   timer, so installing on every load recreates F88 exactly. Use F88's
   **version-latched one-shot**; a table swap alone does not reach an existing
   save.
2. **The `Fix_MeteorFrequency` uninstall trap.** A bare
   `if not SMRFixPack then return end` leaves the save with **no dust-devil
   scheduler at all, forever**. The gate must **hand the loop back to vanilla**
   (Tier 1's shape).
3. **Own A/B + long soak + the recorded disposition** (job 5).

## Scope fence

**In:** C23 item 1 only — the build, its probe, its leg, its disposition, STATUS.
**Out:** **C23 item 3** (marker dust devils ignoring `DustStormsDisabled`) —
defect confirmed, **declined on shape**; all four routes over-reach into scripted
content or put a sleeping mod thread in every save. F89's disposition. Also out:
**F93** (shipped by `8b`, same subsystem, different defect — do not merge them);
the rate question as a *balance* question (see below); layer 1 (⛔).

## Stop conditions

- The leg fails prediction → stop, report; the chain waits.
- The spec on the entry does not match Src when you re-verify it → **do not
  improvise.** Record the divergence and route it. Chain prompt 8 found one
  "verified feasible" §5.4 route that did not exist (BUGS F46); recorded specs
  are claims too.
- You find yourself widening this into a difficulty-tuning change → stop. The
  owner decided the SHAPE question, not the rate.
- Context pressure → self-split (`8d_…_opus.md`).

## What may not be claimed

Nothing here may be called `tested` without the leg passing on the recorded
rider. **Do not claim the rate question is settled** — it is not (below). Do not
record this as precedent for owning further sleeping threads. The result commit
carries its `PROBE SWEEP:` line.

## On completion

Outbox → `12_final_qa_backward_check_fable.md` (**job 8**: personally review the
decision; reversal is a legitimate outcome) and → `9_d10_workshops_build_opus.md`
if counts moved. Delete this file, commit, push.

## Notes from upstream

### Why it was approved (prompt 7, 2026-08-02) — and what is still open

**C23 item 1 — the dust-devil `spawn_chance` truncation.** Defect confirmed and
sharpened: `count_max` is unreachable whenever `spawn_chance < 100`, and the
count can be 0 while `count_min` is 1.

**The SHAPE question is answered, by a second control in another file.**
`MapSettings_Meteor` declares the same trio with an identical idiom
(`multispawn_chance` 30/1/100) and uses it **gate-then-count**: the chance decides
*whether* (`Meteors.lua:284-290`), the count is drawn independently and never
multiplied (`:137`). **Two controls for gate-then-count, zero for
chance-as-multiplier anywhere in `Lua\`.** The intent case then became
data-driven: **`DustDevils_VeryHigh_3` is authored `6..8 @ 50%` and the multiply
makes that range unreachable**, and the original game's presets are identical to
Relaunched's across all eight.

⚠️ **The RATE question is still open, and this prompt does not close it.**
`DustDevils_Low` accidentally approximates the gate today (50% × count 1..2
truncates to 0-or-1), so the shipped rates may have been tuned around the bug.
That is what the owner is deciding, not the shape — and the decision is
provisional pending prompt 12's review.

### Handed over by chain prompt 8 (2026-08-02)

Prompt 8 did the conversion batch and **split under chain rule 3** before
reaching this item. Two carry-overs worth having:

- **A recorded "verified feasible" route turned out not to exist** (§5.4's
  `GetTargetAmount` wrapper for `Fix_TrainCargoDumping` — it is a native
  metatable method behind a savegame permanent). Re-verify this entry's spec
  against Src before building it; the project's own rule that *recorded facts are
  claims too* earned another instance that day.
- **"The new shape needs no persisted field" does not remove that field from
  saves already written by the old shape.** F57(a)'s conversion had to clear
  `SMRFixPack_rocket_fuel_key` explicitly. If this build changes what is
  persisted — and a version latch is persisted state — ask the same question
  about existing saves, and about what an uninstall leaves behind.

⛔ **The sealed document was NOT read, grepped, or surfaced at any point in
prompt 8** — no broad search touched it.
