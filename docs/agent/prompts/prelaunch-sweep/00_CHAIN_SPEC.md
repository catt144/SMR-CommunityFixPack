# Pre-launch sweep chain — the governing spec

**Owner design, 2026-08-17.** *"A chain that is self replicating… it does the
sweep and if it finds a bug or issue it fixes it and creates another opus to redo
a sweep with no report on what it actually found or fixed. And it doesn't stop
self replicating until a chain finds nothing… The reason for this is I frequently
see even today where a new session finds something the previous one missed."*

⛔ **THIS FILE IS NOT SELF-CONSUMING.** It governs every link and must survive
until the chain closes. `01_LINK.md` is likewise re-runnable. Only
`98_LAUNCH_REHEARSAL.md` and `99_TERMINAL_AUDIT_fable.md` delete themselves.

---

## 1 · The premise, and why it is not paranoia

The owner's observation is measurable in this repo, not a feeling:

| effort | surveyed | actual |
|---|---|---|
| `SHIP_SOLO_PREP` | 22 passages | **~46** |
| `RENAME_RELAUNCHED_FIX_PACK` | 72 occurrences / 26 files | **113 / 43** — two of them *paintings*, not text |
| public-docs checkup | — | a count already corrected **twice** |
| the 2026-08-17 upload sitting | ④ declared "decision-free" | a **missing `image` field** that hard-rejects the upload, plus 2 core defects |

⭐ **The diagnosis matters more than the tally.** In every case the miss was not
laziness — it was that **the previous brief never asked that question.** Tonight's
finds came from asking *"what does the game's upload code actually do?"*, which no
brief had ever asked. ⇒ **The lever is variation in the QUESTION, not repetition
of the SWEEP.** A chain of identical sweeps hits sharp diminishing returns; a
chain of different lenses converges.

## 2 · ⛔ What the owner's design gets right, and the one thing that would have defeated it

**Right:** independent sessions · repeat-until-dry · a terminal audit over the
whole body · the owner between links as the safety net.

⛔ **The flaw: blinding does not work in this repo, and pretending it does is
worse than not trying.** Every brief opens with `git log` as a staleness gate;
`STATE.md` and the checklist are mandatory reads; and this project's commit
messages are **three-paragraph essays** that explain exactly what was found and
why. A link that obeys the house rules learns everything the previous link found,
in more detail than the owner's report.

⇒ **The chain resolves this in three ways:**

1. **Blind on VERDICTS, sighted on COVERAGE.** Findings live in
   `SWEEP_FINDINGS.md`, which a link ⛔ **may not open**. Coverage lives in
   `SWEEP_LEDGER.md`, which a link ⛔ **must** open. Coverage is what makes the
   chain converge; blind sweeps cannot, because five sessions can each cover the
   comfortable 60% and never touch the awkward 40%.
2. ⭐ **Chain links break the house essay-commit convention on purpose.** Subject
   line is exactly `sweep: link N — lens <name> — see SWEEP_FINDINGS.md`, and
   ⛔ **it names no finding** — detail goes in the body.
   ⚠️ **This drifted on the very first link:** `e5c6e8a` shipped as
   *"…structure & collision — **L1-F1 enforced**, see SWEEP_FINDINGS.md"*, which
   leaks a finding id into `git log --oneline`, the one command every link runs
   first. Keep the subject boring; that is its entire job.
3. **Replace fake blinding with the rule we already have** — *recorded facts are
   claims too; re-derive the ROUTE, not the citations.* Treating a prior fix as a
   claim to be re-derived is strictly stronger than pretending you cannot see it.

### ⚖️ AMENDED 2026-08-18 — resolution 1 is PARTIAL, and saying otherwise was the error

**Link 2 found the hole and it is real: `STATE.md` is a mandatory read (CLAUDE.md
*and* `01_LINK.md`'s own read path) and links write their verdicts into it.** A
link is therefore contaminated **by the brief's own instructions**. Measured
2026-08-18, the leak is on **six** surfaces, not one:

`STATE.md` (L1-F1…F4 in full, with file:line verdicts) · ⛔ `SWEEP_LEDGER.md`'s
own *NOT reached* column (link 1's cell names **L1-F1** by id) · the checklist
(item 38, in owner prose) · `reports/L1_COLLISION_MAP.md` · `tools/doccheck.py`
(link 1's `LOAD_ORDER_RULES`, visible to every link that runs it) · and the commit
subject above.

⛔ **The response is NOT to plug the leak.** Sealing it means degrading `STATE.md`
— a document that serves the whole project, not this chain — into coverage-only
prose. **An accurate STATE is worth more than a sealed fence.**

⭐ **The response is to stop over-claiming, because blinding was never the
mechanism that produces the effect this chain exists for.** Every case in §1 —
`SHIP_SOLO_PREP`, `RENAME`, the upload sitting — was a **fully sighted** session
finding what a previous **fully sighted** session missed. The fresh-eyes effect
comes from asking a **new question**, never from ignorance of prior answers.

**And this chain ran the experiment.** Link 2 was contaminated — it read STATE
carrying all four of link 1's findings — and it still found a defect link 1
missed, *and* identified this hole, which link 1 did not. ⇒ **Contamination did
not suppress the effect. The lens rotation did the work.**

⇒ **What is actually load-bearing, in order:** ① the **lens rotation** ② the
**coverage ledger** ③ re-derivation of prior claims. The findings fence is ④ —
kept because it is cheap and it prevents **method** anchoring (*"link 1 grepped,
so I'll grep"*), which is a different and still-real risk — but it is ⛔ **not
what makes this chain work, and no report may describe the chain as "blind."**

⇒ ⛔ **The contamination-disclosure ritual is DROPPED for `STATE.md`, the ledger,
the checklist, `reports/` and `doccheck`.** A link cannot disclose its way out of
a mandatory read, and false confessions pollute the only convergence signal the
chain has. **Deliberately opening `SWEEP_FINDINGS.md` or a sweep commit body is
still a nameable act and is still reported.**

⚖️ **For the terminal audit:** the hole is established — do not re-litigate it.
**Rule instead on whether this amendment was the right call**, and on whether any
link's findings show signs of having been anchored by a prior link's verdicts.

## 3 · The lens rotation — pick the next unused one

A link takes the **first lens the ledger does not yet record**. When all eight are
used, a link may re-take one but must go **deeper** and say so explicitly.

| # | lens | the question only this lens asks |
|---|---|---|
| L1 | **Structure & collision** | do our own 75 modules patch the same symbols and fight each other? (⭐ the collision map — never produced here) |
| L2 | **Lifecycle & idempotency** | what happens on the SECOND apply? does any module wrap its own wrapper? (the direct descendant of the 08-17 `order` bug) |
| L3 | **Save & exit** | aggregate save footprint — not per-module. Does `90_SaveSanitizer` cover the CURRENT module set? Does uninstall hold for all 75 at once? |
| L4 | **Player experience** | what does a player actually SEE and READ? first run, dialogs, notifications, in-game wording, log noise |
| L5 | **Failure & containment** | one module throws — at apply, in a wrapper, in an `OnMsg`. Is `FIX_POLICY` §2 "fail safe, never loud" true in AGGREGATE? |
| L6 | **Promise vs behaviour** | registry ↔ package ↔ card/site/README. Dead-coded targets (is F85 the only one?). Does the veto route actually work for all 75? |
| L7 | **Environment & namespace** | globals we leak · packed vs unpacked load paths · console platforms · what the TestKit's own `_G` mutations have been hiding |
| L8 | **Adversarial / hostile modder** | another mod wraps what we wrap, loads before or after us — what breaks, and whose fault does it look like? |

## 4 · What a link may and may not do

| link | may fix? | rule |
|---|---|---|
| 1–2 | **yes** | fix what you find and verify each fix with its own falsifier |
| 3+ | ⛔ **record only** | findings go to `SWEEP_FINDINGS.md`; the terminal audit applies them with the whole set visible |

**Why the switch:** every fix adds risk to a release candidate, and by link 3 the
expected value of another edit to `00_Core.lua` is plausibly negative. ⚠️ **One
exception:** a **launch-blocking** finding is fixed immediately at any link, and
the report says so in its first sentence.

⚖️ **CLARIFIED 2026-08-19 — "record only" means CODE, not records.** Correcting a
`docs/agent/facts/` entry that your own measurement disproves is ✅ **expected**,
not a scope breach — *recorded facts are claims too*, and the verification launch
was right to amend `EF-055` in place when it measured that fact's stated cause was
not necessary. ⛔ What record-only forbids is changing **shipped behaviour**:
`Code/`, `metadata.lua`, `items.lua`.

⛔⛔ **AND ONE TRAP THAT LOOKS HARMLESS: adding a TestKit probe is NOT free
pre-launch.** The suite count is a **player-facing claim** — *"a suite of 96
checks"* on the store card (`RELEASE_DESCRIPTION_FIXPACK.md:147`) and its audited
source. A new probe makes it 97 and puts a wrong number on the card — the same
count that already survived **two** corrections as "95 checks". ⇒ **Probe ideas
are recorded as post-launch work, not built now**, however good they are.

⛔ **No link may:** bump the version · publish anything · touch the opt-in or
rescue repos · edit `docs/archive/` · add an instrument to `Code/` (it would
contaminate the tree under test) · change what the mod PROMISES (route it).

## 5 · The stopping rule — ⛔ NOT "a link found nothing"

"Found nothing" has two causes and only one of them is good. The chain stops when
**any** of these is true, and the report must name which:

1. A link finds nothing new **in territory the ledger marks unswept**, *and* the
   ledger shows no unswept area of consequence remaining.
2. **Two consecutive links** return only cosmetic findings.
3. The hard cap is reached — ⚖️ **8 links** (raised from 5, owner, 2026-08-18).

⛔ **A link that returns "nothing found" while the ledger still lists unswept
territory has NOT converged — it has run out of lens.** Say that plainly.

### ⚖️ AMENDED 2026-08-18 — the cap was 5, and 5 was arithmetically broken

**Eight lenses under a cap of five means the pool can never exhaust**, so the
chain was *guaranteed* to stop on clause 3 — which this spec itself says is not
convergence. The cap made the only good stopping clauses unreachable. It is now
**8, one per lens**, so clause 1 or 2 is actually attainable.

⛔ **8 is structural, not a number to raise again.** A further raise means
re-running lenses, which needs its own justification — a cap that rises whenever
it is reached is not a cap.

## 6 · The terminal gate — A then B, and B is the one that matters

⚖️ **Owner ruling, 2026-08-17:** *"[A] is for our testing to ensure
compatibility. This [B] is for safety to ensure a clean launch of the bug fix
mod."*

⇒ ⛔⛔ **THE RELEASE CRITERION MOVES. A green suite in A is no longer sufficient
to ship.** A is diagnostic support for when B says something is wrong.

| run | configuration | proves | status |
|---|---|---|---|
| **A** | TestKit **on**, opt-in **off** | suite, gates, probes, console | ⚖️ information |
| **B** | TestKit **off**, opt-in **off**, **packed install, junction pulled** | what a player receives | ⛔ **THE GATE** |

⚠️ **A's scope must not be overstated.** It tests this pack against **exactly one
other mod — our own.** ⛔ It may never produce a sentence like *"compatible with
other mods."* Its honest scope is "our two mods together," which is information
for the opt-in's launch.

⭐ **B has never been run in the history of this project.** Every gate reading —
`80/0/16/0`, `75/75`, `8/8`, all ~60 archived launches — was taken with the mod
**unpacked via a junction** and a **third mod loaded that mutates `_G`**. Full
procedure and B's pass criteria: `98_LAUNCH_REHEARSAL.md`.

## 6.5 · ⛔⛔ THE LAUNCH OBLIGATION — added 2026-08-18, after four links and zero launches

**Links 1–4 ran L1 through L4 and NOT ONE opened the game.** Every one declared it
honestly and in detail — those NOT-reached columns are exemplary, which is exactly
how the pattern became visible:

> L1 *"neither core fix has yet executed"* · L2 *"remain unexecuted in Surviving
> Mars"* · L3 *"Nothing was run in a game. No save was opened, no footprint was
> weighed, no object counted"* · L4 *"Nothing was run in a game — **fourth link
> running**"*

⛔ **That is a defect in this spec, not four lazy sessions.** Launches were
*permitted* and never *obliged*, so the cheap path was always available and always
taken, and a link discharged its duty by **declaring** the gap instead of closing
it. The chain was producing an excellent reading of the mod and **zero evidence
about the running mod** — while the two `2f077e8` core fixes that paused this
upload had still never executed, and while the release gate itself (run B) is a
launch.

⇒ **THE RULE.** A link whose lens has accumulated *"needs a running game"* items —
its own, or inherited from the ledger — must **either take a launch, or state in
its report why it refused.** ⛔ Silence is no longer an option. This is the same
move that makes the NOT-reached column work: turn a silent default into a
declared decision.

⇒ **AND THE BACKLOG IS DISCHARGED SEPARATELY:** `97_VERIFICATION_LAUNCH.md` pulls
**run A forward** out of the terminal rehearsal and runs it now. A is diagnostic,
not the gate, so running it early is safe and re-running it later is cheap.
⛔ **Run B stays terminal — it must test the final tree.**

## 7 · Standing rules every link inherits

- ⛔ **`EF-056`** — byte-copy every autosave-tagged save before **every** launch,
  keep copies **outside** the save directory, reconcile **by name** after every
  launch. It has already eaten files twice.
- ⛔ **Probe hygiene gate** before any recorded result:
  `grep -rln "TEMPORARY" Code/ ../SMR-BugFixPack-TestKit/Code/`
- ⛔ **Pre-register predictions in a pushed commit** before each launch.
- ⚠️ **Configuration labelling is mandatory.** Every number recorded carries which
  of A / B / dev-tree it came from. The recorded baselines are the
  **all-three-mods** configuration; numbers from A or B are **re-derived, not
  compared**, and a mismatch is not a regression until someone shows it is.
- ⚖️ **This amends a standing owner ruling** — *"BOTH MODS LOADED is the rig's
  NORMAL config"* (owner, 2026-08-12, active `WORKFLOW` clause). The amendment is
  deliberate and scoped to this chain.
- ⛔ **`tested` (bare) is closed to new work** — use `tested-unattended` (⛔ never
  for a screen event) or `tested-attended`.
- **Live todo list**, one item per commit-and-verify unit, updated as work moves.

## 8 · The files

| file | who reads it | self-consuming? |
|---|---|---|
| `00_CHAIN_SPEC.md` | every link | ⛔ no |
| `01_LINK.md` | every link | ⛔ no |
| `SWEEP_LEDGER.md` | ⛔ **must** be read by the next link | no — appended |
| `SWEEP_FINDINGS.md` | ⛔ **must NOT** be read by the next link; owner + terminal audit only | no — appended |
| `98_LAUNCH_REHEARSAL.md` | the A/B gate runner | ✅ yes |
| `99_TERMINAL_AUDIT_fable.md` | Fable, once, at the end | ✅ yes |

## 9 · The owner's loop

Each link ends with a **plain-language report** — what it swept, what it found,
what it could not reach, and whether anything blocks launch. **The owner then
kicks off the next link.** That manual gate is the chain's real safety mechanism
and its real cost control; it is not ceremony, and no link may spawn its
successor automatically.
