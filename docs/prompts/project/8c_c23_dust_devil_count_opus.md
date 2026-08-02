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

### Handed over by chain prompt 8b (2026-08-02) — your gate is now concrete

**Your gate has fired on the BUILD side and NOT on the verification side. Read
this before you start.**

`F93` is built and pushed: `Code/Fix_DustDevilsDescrMap.lua` (`b22dda5`), a
§1.4b global replacement of `GetDustDevilsDescr` — seven lines copied from
`DustDevils.lua:58-66` with `CurrentMap` → `MainMap` on both reads. **That is the
same subsystem you are about to patch, and it is UNRUN.** The batch leg is
`PLAYTEST_CHECKLIST.md` **PT-60**, predictions P1-P9 written before any run.

**What that means for you, concretely:**

- ⚠️ **Do not start until PT-60 has run.** The README gates you on 8b precisely
  so that two changes to the dust-devil subsystem do not land against one unrun
  leg — a result then cannot be attributed to either. If PT-60 has run, quote its
  P2/P4/P6 readings for `DustDevilsDescrMap` in your own leg's baseline; if it has
  not, that is the thing to fix before building anything.
- **The function you will be reading is now OURS, not vanilla's.** Your item sits
  in the `DustDevils` thread body (`DustDevils.lua:193-240`), which calls
  `GetDustDevilsDescr` at `:193`, `:234` and `:237`. Those calls now reach our
  replacement. Nothing about the descriptor's *contents* changed — only which
  map's `mapdata` it is read from — so your `spawn_chance`/`count_min`/`count_max`
  reasoning is unaffected. But when you re-verify the thread body against Src (and
  you must — see prompt 8's carry-over above), **remember that the shipped
  `GetDustDevilsDescr` is no longer what runs.**
- ⭐ **A rider already exists for the live half of F93** and it is worth taking in
  the same sitting as yours, because it needs the same map switch you will
  already be doing: `PLAYTEST_CHECKLIST.md`, needs-eyes section, "F93 dust-devil
  map rider". Two readings, one map switch.
- **F93 needed no new §3a site and yours will.** F93's replacement is synchronous
  and stores nothing, so it is route-(a)/(b)/(c) clean. Your item is inside the
  thread body itself — a 14th §3a exposed site and a sleeping game-time thread —
  which is exactly the asymmetry that got you split out. Do not let F93's
  cheapness set your expectations.

**One more carry-over, and it is the strongest one from 8b:** of prompt 7's six
approved specs, **five had a defect in their supporting detail** — a wrong line
citation, a method name that does not exist, a self-check placed where it cannot
run, two writes described as equivalent when only one was load-bearing, and an
overclaimed equivalence. Every *shape* survived; every *detail* had to be
re-derived. Your entry was written by the same session in the same sitting.
**Re-verify its code sketch, its line numbers and its self-check against Src
before you build, and treat the "should not need to re-derive" framing as the
thing that has now been falsified five times.** Full list on prompt 12, job-7
seed block.

⛔ **The sealed document was NOT read, grepped, or surfaced at any point in
prompt 8b.** One staging slip is recorded rather than hidden: a `git add -A`
staged it in one commit, which was amended out before any push; the file is
untracked again and **nothing in it was opened, read or summarised**.


### ⭐ ADDENDUM — written AFTER PT-60 ran (2026-08-02). Three things the notes above predate.

**Your gate is genuinely open now, not merely landed.** The note above said F93 was
built and unrun. **PT-60 has since run**: `76 PASS, 0 FAIL, 9 SKIP, 0 ERROR`,
`79/79` modules active, zero `[LUA ERROR]`, and the `DustDevilsDescrMap` probe
PASSes on all three legs (*"the descriptor follows MainMap in both directions, and
MainMap's own disabled setting still wins"*). The dust-devil subsystem therefore has
a **verified baseline** before you touch it — anything that misbehaves afterwards is
attributable to you.

**1 · ⛔ THE TRAP THAT WOULD COST YOU A WHOLE SITTING: dust devils are OFF on a
terraformed colony.** `MapSettings_DustDevils` shares the **`Atmosphere` /
`DustStormStop`** gate with dust storms (`TerraformingDisasters.lua:34-52`), and
`OverrideDisasterDescriptor` **returns nil** once that parameter passes the
threshold (`:69`) — after which the scheduler parks in
`while not new_descr do Sleep(const.DayDuration) end` indefinitely. **Your entire
item is about how many dust devils spawn.** On a terraformed save the answer is
zero, for a reason with nothing to do with your fix. **Check before choosing a
colony:**

```
*r ConsolePrint("DustStormsDisabled: "..tostring(rawget(_G,"DustStormsDisabled")).." | Atmosphere: "..tostring(GetTerraformParamPct("Atmosphere")))
```

`true` means that colony cannot produce dust devils at all. The campaign's deep
colony (`TEST 2H`, sol 285) is past the threshold and **cannot host this work**.
⚠️ Related correction: F93's own entry claimed its window runs *"forever"*. It does
not — it is large but bounded by terraforming, and that is fixed on the entry.
Expect the same bound on your item's reachability.

**2 · ⛔ YOU PERSIST STATE, AND THAT IS EXACTLY WHERE THIS BATCH BROKE.** Two of
8b's three load-time heals were **not idempotent**, and — the part that matters for
you — **neither was visible to source review, to code review, or to its own passing
probe.** `Fix_AstrogeologistExtractors` added +10% on *every* load, unbounded,
because its presence test compared **object identity** while `label_modifiers` is
persisted: the save deserialises its own copy of the key, so the test can never
match across a load. Its probe PASSed throughout, because the probe asserted the
*preset* while the *applied* count doubled.

**You own a sleeping game-time thread and a version latch. Both cross a save
boundary.** So:

- **never key a presence/already-done test on an object identity that crosses a
  save** — test a stable property instead;
- **save, reload, and re-read the number** before believing any idempotence claim.
  That round trip is the only instrument that found either defect;
- a Mod-Manager re-enable does **not** load edited Lua — **exit and relaunch**.

Full write-up: prompt 12's job-7 block, filed as a third axis that corpus lacked.

**3 · A SIXTH spec-detail defect, on top of the five listed above.** F96's spec
enumerated `Building.lua:1814` as a runtime clear of `indestructible` *"on other
objects"*. It is `Building:CheatDestroy`, a **generic `Building` method** applying
to any building including the one being fixed. The conclusion survived (cheat-only,
so unreachable in normal play) but the stated reason was wrong. **Six of prompt 7's
six specs have now had a defective supporting detail. Treat "should not need to
re-derive" as fully falsified.**

**Counts, already re-derived — recount, never inherit:** 108 rows = 96 F + 12 D;
38 C; **79 registered modules / 73 default-active**; **85 probes**.
⚠️ Any prediction quoting an *active* count must read the toggles first — **Mod
Options survive a Mod Manager disable**, so `metadata.lua`'s all-`false` defaults do
not describe a profile anyone tests with. PT-60's P1 missed on exactly that
(`ENGINE_FACTS.md`, three-switches table).