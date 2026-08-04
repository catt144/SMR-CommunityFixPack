# Chain prompt 3 — co-run #1: the first payload, and the first evidence cards

**Read `README.md` in this folder first — binding chain rules apply.** Start
with `git log --oneline -10` + `git pull`, then `CORUN_RIG_SPEC.md` (as
corrected by prompt 2 — the corrections are part of the spec) and prompt 2's
outbox below. If prompt 2's outbox is missing, STOP — the kill-gate may have
fired; check the manifest.

**ATTENDED (~15–20 min of owner time), batched per the WORKFLOW batch rule:**
one launch drains everything below. Prep everything unattended first; the
todo list tells the owner when to sit down.

## The payload (from the checklist's tagged candidates)

1. **F11 pre-wrapper watch** (Tier A — WITNESS): staged passenger line, owner
   watches one unload — train leaves, stats move, `ListFixes` shows
   `TrainPlatformWedge [active]`. This is the rider "F11: verify the
   pre-wrapper conversion"; a PASS earns the conversion `tested` **per the
   rider's own terms** (it was written for exactly this).
2. **F99 hex tie-break read** (ride-along, no eyes): on a hex holding a hidden
   broken element and its repair site, what does `HexGetTrackGridElement`
   return? One console/scripted read; settles `F99.md`'s last C-side link.
3. **C41 amplification loop** (Tier A — WITNESS): drive the depot spawn/open
   cycle repeatedly while the owner watches for the picker failing to appear
   (`F76MISS` is the instrument). Intermittent-trigger amplification is THE
   class-2 use case — record hit rate per N cycles, even if the answer is
   0/N.
4. **F11 Done-timing trace** — ONLY if prompt 2's outbox says it was not
   settled in the skeleton.

For each: produce an **evidence card** per the spec's Tier B template — even
for the Tier A items, because prompt 4 audits whether the cards would have
sufficed without the owner's eyes. The cards are the experiment inside the
experiment.

## Jobs

**Job 1 — todo list up front**, one item per payload item plus prep/close
units, "OWNER SITS DOWN HERE" marked.

**Job 2 — prep unattended:** probe sweep (record the line); staged save copy;
scenario scripts as `TEMPORARY` TestKit files — ⚖️ **permitted for YOU ONLY, by
a one-time owner override; read the override block below before using it**;
parse sweep; measure-moments list with the owner's verdict words pre-written
("train left / train stuck", "picker appeared / missing", …).

### ⚖️ ONE-TIME OWNER OVERRIDE — armed prep, granted to this prompt only (2026-08-04)

`WORKFLOW.md` probe hygiene **rule 5** says a probe file is present in `Code/`
only while its run is actually happening, so prep may not commit an armed probe.
**The owner has granted this prompt a one-time override of that rule for its
prep**, verbatim: *"You can give prompt 3 a one time owner override for its
prep."* You may therefore write the scenario scripts as real `TEMPORARY` files
in `Code/` and commit them **before** the sitting.

**This is an override, not a repeal.** Overrides in this project are *"never
inferred, never assumed from precedent, and never carried forward to a second
case"* (FIX_POLICY §4a's procedure, applied here). Rule 5 is unchanged for
everyone else and for every later co-run. **Do not cite this grant as
precedent** and do not extend it past your own prep.

**Conditions — all five, and they are the reason the grant is safe:**

1. **ONE prep commit may be armed.** Name it in your todo list. Every other
   commit you make is subject to rule 5 normally.
2. **`doccheck.py` will be RED and the hook will block; `--no-verify` is
   authorised for that single commit and nothing else.** The commit body MUST
   state, plainly: that doccheck is red, that the ONLY red is the TEMPORARY
   sweep, the exact files armed, the test that declares each, and this override
   with its date. That is a true and complete statement — which is the whole of
   what the hook asks for. A body that says less than that is the failure mode.
3. ⛔ **DISARM DEADLINE — the condition the grant actually rests on. If the
   sitting does not happen in the same working session, DELETE the probe files
   and their metadata lines before you stop.** An armed probe may never survive
   a session boundary. The owner's stated fear is verbatim *"I do not want to
   get back into the situations where armed probes start giving us false
   problems or issues"*; a probe armed for days is exactly that, and 2026-07-31
   is what it looks like. Re-arming next session costs a paste.
4. **`PROBE SWEEP:` line in every affected commit reads
   `armed: <files>, declared by <test>, owner override 2026-08-04`** — never
   just `armed`. A reader must see the authorisation without leaving the log.
5. **Rule 2 is untouched:** the probes still die in the commit that records
   their answers.

⭐ **You are also live evidence for prompt 4's rule-5 audit — report both
halves.** The owner asked prompt 4 to recheck rule 5 and is open to
recommendations. You are the first and only session to work under the override,
so say plainly at close: **did armed prep actually buy anything** over
committing the scripts as fenced blocks and pasting them at the sitting? If it
bought little, that is a finding that strengthens rule 5; if it bought a lot,
that is a finding that argues for a permanent hatch. Do not editorialise —
report what it cost and what it saved.

**Job 3 — the run**, batched: fixed cost first (launch, load, warm-up per
spec), then payload items in the order above — owner-needed items
back-to-back so their attended window is contiguous, ride-alongs after they
leave. Record actual wall-clock and actual owner-minutes.

**Job 4 — record, one commit per verdict class:** rider outcomes to their
entries and checklist rows (strike/annotate per convention); the tie-break
verdict to `F99.md`; every recorded number cites its log line; forced/organic
labels on everything; TEMPORARY probes deleted in the recording commits;
`PROBE SWEEP:` lines throughout; archive the log if cited.

**Job 5 — close:** outbox to prompt 4 — verdicts, evidence cards (or where
they live), actual costs vs. spec, owner-minutes used vs. promised, and your
honest note on which payload items the cards alone would have settled; delete
this file in the same commit; doccheck green; push.

## ⭐ You may ASK the owner to act on your blocked items — inside a stated balance

Owner, 2026-08-04, on being shown that two of your four payload items are
blocked on a gap: *"for its blocked items it can ask me to assist if it needs me
to do something. This whole method isn't to take me completely out of the loop,
its to take my time commitment to a more reasonable level and streamline."* And,
sharpening it: *"As much that can be optimized while not reducing quality it
probably the better framing of it. Keep a good balance of quality and minimal
time investment as there is only one of me."*

> **Their time is the objective to minimise; quality is the constraint that
> binds.** Optimise as hard as it will go, and stop where going further would
> cost evidence quality. Asking is legitimate when the ask genuinely beats the
> alternative on that trade — **not because asking is permitted.** Every ask
> competes with the moments that actually need their eyes.

Standing framing: `WORKFLOW.md` "Co-runs". What it means concretely here:

- **The hex tie-break and F99 items are gapped** — the save carries 926 track
  elements and **zero** broken ones, so both need damage staged. `CheatMeteors`
  at a position is the agent-side route (forced upstream, named). **If that
  turns out to be fiddly, or if a player-driven break would give better
  evidence, ask them** — it is their colony and they know where the track is.
  ⚠️ F99's constraint is unchanged either way: the BREAK may be forced, the
  **REPAIR must stay organic**.
- **Any ask goes in the measure-moments list up front**, with what they do, why,
  and how long — not sprung on them mid-sitting. Batch it with the moments they
  are already sitting for.
- ⛔ **Do not silently drop an item because it needs a human.** "Needs the
  owner" is a precondition to route, never a reason to descope. If you run out
  of their window, the item becomes a TAKEABLE-WHEN rider with the measured cost
  attached so they can price it.

## Scope fence

**In:** the four payload items, their evidence cards, cost accounting.
**Out:** any fix (route findings); the F99 no-cheat discriminator (needs
drone-repair wall-clock the spec has not budgeted — route it as a rider for
the NEXT co-run with the measured fixed-cost numbers attached, so the owner
can price it); new candidates discovered mid-run (rider them, rule 3).

## Stop conditions

- The C41 loop perturbs the game state it measures (spawn side-effects piling
  up) → stop the loop, record N so far, note the perturbation — an honest
  0/N-with-caveat beats a contaminated 0/2N.
- Owner has to leave mid-window → finish the current item, run the remaining
  ride-alongs, leave the rest as riders. Their time budget is the contract.

## ⛔ What you may not claim

- Not `tested` for anything except F11's watch rider on ITS OWN terms (Tier A
  witness PASS) — nothing else in this run has a rider granting that word.
- Not "C41 refuted" from 0/N — absence of the intermittent under N forced
  cycles is a rate bound, not a refutation; say the number.
- Not that the evidence cards suffice for sign-off — that is prompt 4's
  question and then the owner's.

## Notes from upstream

*(2026-08-04, prompt 2 — Opus. **⛔ KILL-GATE: PASS WITH CORRECTIONS. The chain
continues.** Full run record is `CORUN_RIG_SPEC.md` §8; §1's S1/S2/S4/S5/S7 are
now PROVEN. Raw lines: `docs/archive/corun0_Mars.exe-20260804-10.51.15.log`.
What changes your jobs:*

- ***The fixed cost is ~80 s, not 5–8 min.** Launch → menu ~2.7 s; the 56 MB
  load **9,968 ms**; quit ~1.5 s; whole cycle **79.9 s**, owner-attended **~1.5
  min** of the ~10 promised. §3's effort model is ~4–6× pessimistic. Two
  consequences for you: your ~15–20 min promise is probably generous, so **do
  not pad the sitting to fill it** — and a relaunch now costs ~1.5 min, which
  makes "one probe = one question" cheap rather than expensive.*
- ***The launch recipe is proven verbatim and needs no owner click.** No Steam
  picker interposed (U3 = NO, by timestamp). Launch WITHOUT `-smrautorun`; a
  `TEMPORARY` TestKit file in the `code` list is the whole arming mechanism, and
  95_AutoRun stands down by itself. Copy 97_CoRun0's shape from
  `docs/archive/corun0_*.log`'s behaviour + git history of this commit.*
- ***⛔ Four spec corrections BIND you (§8 C1–C5). The two that will bite:***
  - ***C1 — never time a step with `RealTime()` deltas.** It froze across the
    loading screen and under-reported the load 11.5× (864 ms vs 9,968 ms).
    `agent/facts/EF-045`. Your cost accounting is a deliverable; time it from
    the engine's `Game loaded on map … in Nms` line, OS file timestamps, or
    externally.*
  - ***C4 — a freshly loaded save arrives PAUSED** (speed read back `0`). Any
    game-time thread you schedule is dead until you call
    `UIColony:SetGameSpeed(n)`. This is not in §5 and it silently voids
    amplification loops.*
- ***Your item 4 (F11 Done-timing) is NOT settled — but it is half-done, and the
  half that IS done changes how you run it.** The trace ran and fired, but the
  pair it picked was **same-map**, so `OnTransferToMapDone` never fired and
  routes (a)/(b) are untouched. What IS now measured is the same-map removal
  path (`F11.md`, block dated 2026-08-04). **To settle the cross-map question you
  must SELECT for it: an UNDERGROUND train rider plus a SURFACE rocket, and
  assert `cross_map == true` in the log before driving `SetCommand`.** ⭐ And use
  a better instrument: wrap **`Holder.OnExitHolder`** and print its caller, not
  just `Unit.OnTransferToMapDone` — a post-hoc `find == nil` cannot exclude an
  ordinary unload having removed the rider first (this run hit that limit).*
- ***§6 confirm table, as read: your items 1 and 3 are GO** — 8 trains with **59
  riders aboard**, a landed `UniversalZeusRocket` on the surface, 11 depots and
  658 stockpiles. ***Your item 2 (hex tie-break) is BLOCKED on a gap*** — **0**
  broken track elements and **0** repair sites in the save (926 track elements,
  all healthy). You must stage a break first (`CheatMeteors` at a position —
  forced upstream, named); budget it, and note the F99 discriminator's repair
  must stay organic.*
- ***`OnTransferToMapDone` is a COMBINED method** (`_cobject.lua:158`) — any wrap
  of it MUST be installed on the classdef at mod-FILE scope, before flattening.
  An apply()-time wrap never reaches `Colonist`. Same trap shape as the A2
  lesson; it cost nothing here only because it was caught by reading first.*
- ***⛔ A BINDING RULE LANDED AFTER YOUR BODY WAS WRITTEN, AND IT CHANGES YOUR
  JOB 2 (which is struck above).*** `doccheck.py` reds on ANY `TEMPORARY` hit
  with no escape hatch and the pre-commit hook blocks, so prep **cannot** commit
  an armed probe (§8 C5). The owner ruled on it the same day and asked for the
  safest option: the tool was **not** loosened. **`WORKFLOW.md` probe hygiene
  rule 5 now binds you — a probe file is present in `Code/` only while its run
  is actually happening.** In practice:
  1. **Prep commit:** staged save, measure-moments list, doc edits, and each
     scenario script **as a fenced Lua block inside this prompt file**. A probe
     parked in a doc is inert by construction — the mod loads only files listed
     in `metadata.lua` `code`, all under `Code/` — so nothing is armed.
  2. ⭐ **Still run the parse sweep in prep.** Rule 5's known weak spot is that
     it pushes syntax errors to the sitting. Untested mitigation, and you are the
     first to try it: paste the file into `Code/`, parse-sweep it, delete it
     again, and record `parse sweep GREEN on the source at <sha>` in the prep
     commit. **Report whether this worked — prompt 4 is auditing rule 5 and this
     is live evidence.**
  3. **At the sitting:** write the files into `Code/`, add the metadata lines,
     parse sweep again, launch.
  4. **Result commit:** files AND metadata lines deleted, `PROBE SWEEP:` line
     present. Rule 2 unchanged.
  ⛔ `--no-verify` is barred — its documented meaning ("the docs are
  inconsistent, I know") would be a false statement when the only red is a
  declared probe.*
- ***⛔ LEAVE THE TESTKIT'S ORPHANED EDIT ALONE — it is under investigation by
  prompt 4, by the owner's explicit instruction.*** `C:\Dev\SMR-BugFixPack-
  TestKit\Code\96_AutoRunFlag.lua` carries an uncommitted comment-only change
  (an `EXECUTED ONCE` marker for the 2026-08-03 87/87 MarsDebug pass). It
  predates this chain, is not a probe, and the owner declined an offer to commit
  it standalone — *"I would be more comfortable having 04 investigate instead of
  committing and forgetting."* **You WILL be running `git` in that repo, and a
  `git add -A` there would silently absorb it into a co-run commit and destroy
  the evidence prompt 4 is being asked to weigh.** Stage the TestKit
  explicitly by path, never with `-A`. If your `git status` there shows anything
  BEYOND that one file, that is new drift — report it, do not tidy it.*
- ***Not caused by our leg, reported anyway** (WORKFLOW's log rule): two
  `[ResManager Error] Cannot find file with base path: Animations/LawOfficeDoor_
  idle.hgacl` / `_opening.hgacl` lines fire on every load of this map. They are
  also in the owner's own 2026-08-03 campaign logs (`21.18.38`, `22.23.59`) and
  absent from a boot-only session — i.e. a **vanilla missing-asset reference**,
  pre-dating us, not on any list. Unfiled by design (prompt 2's scope fence);
  it is on the checklist for the owner's call.)*
