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

⇒ **The chain resolves this in three ways, and all three are binding:**

1. **Blind on VERDICTS, sighted on COVERAGE.** Findings live in
   `SWEEP_FINDINGS.md`, which a link ⛔ **may not open**. Coverage lives in
   `SWEEP_LEDGER.md`, which a link ⛔ **must** open. Coverage is what makes the
   chain converge; blind sweeps cannot, because five sessions can each cover the
   comfortable 60% and never touch the awkward 40%.
2. ⭐ **Chain links break the house essay-commit convention on purpose.** Subject
   line is exactly `sweep: link N — lens <name> — see SWEEP_FINDINGS.md`, detail
   in the body. That way the next link can run `git log --oneline` for staleness
   **without being contaminated**, and reading a prior link's commit *body*
   becomes a single, nameable, forbidden act rather than an accident.
3. **Replace fake blinding with the rule we already have** — *recorded facts are
   claims too; re-derive the ROUTE, not the citations.* Treating a prior fix as a
   claim to be re-derived is strictly stronger than pretending you cannot see it.

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

⛔ **No link may:** bump the version · publish anything · touch the opt-in or
rescue repos · edit `docs/archive/` · add an instrument to `Code/` (it would
contaminate the tree under test) · change what the mod PROMISES (route it).

## 5 · The stopping rule — ⛔ NOT "a link found nothing"

"Found nothing" has two causes and only one of them is good. The chain stops when
**any** of these is true, and the report must name which:

1. A link finds nothing new **in territory the ledger marks unswept**, *and* the
   ledger shows no unswept area of consequence remaining.
2. **Two consecutive links** return only cosmetic findings.
3. The hard cap is reached — **5 links**, unless the owner raises it.

⛔ **A link that returns "nothing found" while the ledger still lists unswept
territory has NOT converged — it has run out of lens.** Say that plainly.

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
