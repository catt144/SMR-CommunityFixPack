# Chain prompt 3 — adversarial audit, the unforeseen-issues report, integration

**Read `README.md` in this folder first — binding chain rules apply. You are
the terminal prompt: this folder must be EMPTY when you finish.** Unattended.
Start with `git log --oneline -10` + `git pull`. Todo list up front.

**Read path**: this folder's remaining files · the outbox below · every
entry/checklist line prompt 2 touched · the archived logs it cites · the
`CORUN_RIG_SPEC` audit precedent if useful
(`git show 93088ba:docs/agent/prompts/corun-rig/CORUN_RIG_SPEC.md`).

**Every "done", "PASS", "SKIP" and "measured" upstream is a claim.** This is
the owner's audit floor for unattended work (their rule, 2026-08-04): the
whole reason this prompt exists on a separate tier is that nobody watched
the run.

## Jobs

**Job 1 — audit the run record, verdict-by-verdict, against the archived
logs.** Does each cited line say what the entry now says? Are
forced/organic labels present and honest — leg C's repair especially: the
log must show the repair happened WITHOUT the completion cheat. Are `SKIP`
reasons true against the cycle-0 confirm reads? Did any number get rounded
or any zero get dressed as a refutation (condition-sampled rule)? Were the
`[NEVER RUN]` → `[RAN]` flips justified by readable log evidence? Commit
discipline: probes deleted in their recording commits, sweeps present,
staged/throwaway saves gone, every cited log actually archived
(`git show` it — a claimed archive that a plain `git add` silently dropped
is the known failure). ⛔ A missing archived log is an automatic finding,
not a shrug. Corrections visible, never silent; a correction that changes a
verdict re-routes that item to the owner.

**Job 2 — audit the SAVE-primitive claim chain.** If prompt 2 promoted it
to PROVEN, verify the proof cycle's log shows save → list → load-back on
the throwaway name, and that the WORKFLOW envelope update (Job 4) states
exactly what ran, no more. If the proof failed, verify legs A/D were routed
as gaps and not quietly improvised.

**Job 3 — the unforeseen-issues report (the run's second product, and the
owner's actual question).** From prompt 2's ledger AND your own audit
residue: everything that surprised, deviated, retried, or would have needed
a hand — each with its log line, whether it recurs, and what it means for
the CO-RUN program specifically (that is the decision this feeds: the owner
runs co-runs next; what should their briefs guard against?). "None observed
over N cycles" is a legitimate report if the audit sustains it. Route
anything that changes a co-run assumption into `WORKFLOW.md` "Co-runs" or
the HELP rig section — surgically, no sprawl.

**Job 4 — integrate.** Entries carry their verdicts (already, per prompt 2
— verify rather than re-write); checklist: strike/annotate the lines this
run settled (PT-35, the F99 residue rider, leg E's rows; the F99
discriminator RESULT lands on the owner's existing F99 decision line as
input, never as the decision); `WORKFLOW.md` capability envelope: add what
this run PROVED (the save primitive, if it passed) and nothing it did not;
`STATE.md`: chain CLOSED line (cap 60, evict in-commit); `SESSION_LOG.md`:
the chain's record, newest-first — verdicts, actuals-vs-predictions,
economics of the batch (machine time, owner time ≈ 0 + kickoff word, token
actuals unrecorded unless you have them), the unforeseen-issues summary;
`CHAIN_METHOD.md`: one lesson entry ONLY if this chain taught something the
corun-rig close did not (the first Opus-executes/Fable-audits instance —
did the audit floor catch anything? Say honestly either way).

**Job 5 — close the chain.** Delete every remaining file in this folder in
the closing commit (parked sources included — they survive in git; cite the
pre-deletion sha in the SESSION_LOG record). doccheck green, push. Then
report to the owner: what ran, what each leg found, what the batch cost
(against the ~90 s/cycle + zero-owner expectation), what the audit caught,
the unforeseen-issues verdict for the co-run program, and what is owed or
routed. ⛔ **The report ENDS with the next-chain kickoff** (chain rule 14):
read `STATE.md`'s NEXT pointer and give the owner the exact line to start —
which model, which prompt file — or say plainly that nothing is queued and
name what the front of the co-run queue looks like instead. If a
`02b_OPUS_CORUN.md` was inserted upstream, its results were claims like any
other (Job 1 covers them) and its owner-minutes go into the batch cost.

**Job 6 — the owner answered three decisions in their own hand; integrate
them (added 2026-08-04 by the owner, via prompt 2).** They are committed
verbatim in `docs/PLAYTEST_CHECKLIST.md` as informal end-of-bullet markers.
**Read them in place — do not work from this summary alone**, and do not
reword or relocate the owner's own text until the decision it carries has
landed somewhere durable.

| marker | attaches to | what it decides |
|---|---|---|
| `----Approved` | the **sign-off TIERS** item (Tier A/B/C + hands axis + visible-demotion rule) | **ADOPTED.** Standing policy, not a per-item call |
| `--approved` | the **mod-page relabel package** ("judgment calls" section for F55, F40, F73(b), F70, F97) | **ADOPTED as a proposal** |
| `---on hold` | **F100**, the `NoHomeless` self-check repair | ⛔ **NOT a decision.** Stays open, stays counted in STATE's open-decisions number |

⛔ **Four traps, each of which is a way to take a decision the owner did not
give:**

1. **The tiers item states its own limits:** *"`tested` still means a pass at
   the keyboard per WORKFLOW, and no already-granted status is
   reclassified."* Adoption touches neither. Widening it is not integration.
2. **The relabel package says "The wording is yours."** Approval adopts the
   *proposal*; the wording is still **owed by the owner**. And
   `MOD_DESCRIPTION.md` is **FROZEN** until launch prep — so this becomes a
   launch-prep instruction with an owed input, not an edit to make now. Route
   the wording ask back to the checklist.
3. **`on hold` ≠ resolved.** F100 keeps its decision line; do not strike it,
   do not archive it, do not decrement the open count for it.
4. ⚖️ **This prompt's own "What you may not claim" forbids "any tier/sign-off
   change (still routed, still the owner's)". That was written while the
   decision was open. It is now ANSWERED, and the prohibition is SUPERSEDED
   for the tiers item only** — every other item on that list stands
   unchanged, F99 severity included. Say in your report that you relied on
   this supersession.

Where an adopted decision changes standing policy, it lands on the standing
surface (`WORKFLOW.md` sign-off/co-run rules), not only on the checklist —
and the checklist keeps the owner-facing record of *what they decided and
when*, per the "owner decisions go in the checklist" rule.

**Job 7 — stale records in the checklist: apply the documented rule, don't
invent one (owner ask, 2026-08-04).** The checklist is **1,037 lines** and
carries a growing layer of items that are finished: struck-through decision
bullets marked `✅ DONE`/`DECIDED`, sections this chain settled, and routing
notes overtaken by events.

⛔ **The rule already exists — find it before you act.** The checklist's own
reporting protocol says a completed section **moves WHOLE to
`docs/archive/PLAYTEST_ARCHIVE.md` and is deleted from the checklist with no
stub and no pointer left behind**; the header says the same. `docs/archive/`
is **append-only, never edited**. Anti-sprawl (chain rule 12) still binds: no
new document, folder, or document class — `PLAYTEST_ARCHIVE.md` is the
destination that already exists.

**Do this:**

- **Inventory first, move second.** List what you judge stale and why, with
  line references, before touching anything. A section is stale when its
  question is *answered and recorded elsewhere* — never merely because it
  looks old.
- ⛔ **Never archive an item that still owes the owner something.** A decision
  bullet with an open ask, an `on hold`, or an owed input (the relabel
  wording) stays put no matter how much struck-through text surrounds it.
- ⛔ **Nothing is deleted whose durable content does not already live in an
  entry, `PLAYTEST_ARCHIVE.md`, `SESSION_LOG.md`, or an archived log.** Check,
  per item. The checklist is the owner's working surface; a fact that exists
  only there is not stale, it is unfiled — file it, then archive it.
- **The class the rule does not cover: resolved DECISION bullets.** The
  documented rule is written for completed *test sections*. Struck-through
  decision records are a different shape, and there is no precedent for them.
  ⛔ **Do not invent one silently.** Pick the treatment you think is right,
  apply it to at most a couple of clear cases as a worked example, and **route
  the general question to the owner on the checklist** with your
  recommendation and what it would cost to apply across the file.
- **Report the size delta** (lines before → after) and what moved, so the
  owner can see the effect without reading the diff.
- doccheck green; `PLAYTEST_ARCHIVE.md` grows by exactly what the checklist
  lost, verbatim.

## Stop conditions

- A load-bearing verdict fails its audit and the logs cannot settle it →
  correct visibly, re-route the item to the owner, keep closing the chain.
- Prompt 2 stopped mid-run (owner interrupt, stop condition): audit what
  ran, inventory what did not into routed items with their staged state
  cleaned up, and still empty the folder — an honestly-closed partial chain
  beats a lingering one.

## ⛔ What you may not claim

- Not `tested` for anything in this chain.
- Not "the rig is ready for co-runs" as a blanket — say which assumptions
  this run exercised and which it could not (it had no eyes/hands moments,
  which is precisely what co-runs add).
- Not owner-time savings — one batch is a data point; report cost against
  the expectation, per WORKFLOW.
- Not F99 severity, reachability beyond what leg C actually sampled, or any
  tier/sign-off change (still routed, still the owner's).

## Notes from upstream

*(Appended by prompt 2, 2026-08-04. The run happened: 7 cycles planned, 11
launches made, 1 killed from outside. Owner attendance: the kickoff word, plus
one unprompted mid-run message that caught a stall before my own outside bound
did — recorded in the ledger as I2 because it is a real data point about
unattended running.)*

### 0 · Read this first: three of the seven legs were rewritten mid-run

The parked probes were parse-swept GREEN and Src-verified, and **three of them
still produced wrong answers on their first run.** Every rewrite is in the file
header of the source it changed, and every voided log is archived beside the good
one. **Audit the rewrites as hard as the results** — I am the one who wrote them,
under time pressure, in the same session that needed them to work:

| source rewritten | why | void log |
|---|---|---|
| `97_U1Common` (`ErrorWatchNote`) | never defined; all 7 payloads call it | — (pre-launch) |
| `97_U1Common` (`save_proven`) | per-process flag used as a per-chain gate | `u1c2` run 1 (in the good log's own text) |
| `98_U1C4` (leg C) | completion counter could not fail | `u1c4void_Mars.exe-20260804-17.09.15.log` |
| `98_U1C5` (leg E) | `pcall` result discarded; row recipe broken | `u1c5r1_…17.16.14.log`, `u1c5r2_…17.19.01.log` |

### 1 · Per-leg verdicts, with the log that carries each

| leg | verdict | log |
|---|---|---|
| **SAVE primitive** | ✅ **PROVEN** — `SaveGame` → `ListForTag` (57→58) → `LoadGame` back live, pack still 81/81. Cost **0.60 s** on the 56 MB save (predicted 10–20 s) | `u1c0_…16.37.16.log` |
| **F (C42)** | `C42STALE 0 \| 4 passages, 50 elements, **0 unit entries**`. ⛔ **UNSAMPLED** — zero-entry denominator, and taken post-load when nothing establishes `Holder.units` survives serialisation. But limit 2 is **CLOSED**: `LeadIn` really does set the holder (`PassageGridElement` IS a `Holder` via `Building`→`BaseBuilding`), so the mechanism holds. Refinement: **one** stale entry per traversal, not N | `u1c0` |
| **D1** | ✅ 3 loads, `0 of 6 families changed` ×3, **no heal line anywhere**. Falsifies the F92 and F88 shapes. H1 + H3 **unsampled** | `u1c1_…16.46.30.log` |
| **A (PT-35)** | ✅ both passes `0` twice, `0 of 7 readings changed` ×4. ⛔ **turbine half UNSAMPLED** — `FrictionlessComposites researched=false` ⇒ early return at `90_SaveSanitizer.lua:58`. Upgrade half sampled over 175 modifier entries | `u1c2_…17.03.10.log` |
| **B (F99 residue)** | Pre-reload `F99RESIDUE 0 0`, but **`:805` never threw** ⇒ the rider's own precondition unmet, **rider stays `unrun`**. Gained: rate datum, instrument confirmed, counter has a liveness witness | `u1c3_…17.06.05.log` |
| **C (F99 discriminator)** | ✅ **4 forced breaks, all witnessed, 4 organic repairs, ZERO `:805`.** Rate bound with condition stated — **not** a refutation | `u1c4_…17.12.54.log` (+ void) |
| **E (`[NEVER RUN]`)** | ✅ **both rows flipped.** `CheatDustStorm` works as documented (start+stop <0.5 s). Devil row **RAN with a CORRECTED recipe** — the documented `table.copy` form raises | `u1c5_…17.21.26.log` (+2 void) |
| **D2** | ✅ **PASSES all three conditions** — H5 and H6 each heal exactly once, land exactly on baseline, silent on reload. H1 **unsampled** (rocketscientist). Ceiling MECHANISM | `u1c6_…17.24.57.log` |

### 2 · Actuals vs predictions

| cycle | predicted | actual (wall) | launches |
|---|---|---|---|
| 0 | ~1.5 min | **79 s** | 1 |
| 1 | ~1.7 min | **97 s** | 1 |
| 2 | ~1.5 min | **75 s** | 3 (1 unarmed, 1 self-aborted) |
| 3 | ~1.7 min | **61 s** | 1 |
| 4 | ~6 min | **64 s** | 2 (1 void) |
| 5 | ~3 min | **74 s** | 3 (2 void) |
| 6 | ~2.5 min | **97 s** | 1 |

**Predicted total ≈ 18 min. Actual useful ≈ 9 min across 7 good launches; ≈ 21
min including the 4 wasted launches and the 8-minute unarmed stall.** Cycle 4's
6× overshoot is the interesting one: the prediction assumed drone repairs would
take minutes; they take ~2 s of real time at speed 20.
**Component actuals** (from the log's own `Lua H:MM:SS:mmm` markers): boot→menu
**19.0–19.4 s** (the largest fixed cost, and the argument for batching legs per
launch); cold load **9.6–10.1 s**; repeat load same map **5.8–6.0 s**; settle
15.5 s as designed; **save 0.58–0.63 s** across 5 saves.

### 3 · Unforeseen-issues ledger — 8 entries, 0 of them the game's fault

**I1 · `U1.ErrorWatchNote` never existed.** All 7 payloads called it. Would have
closed every cycle as `PAYLOAD ERROR`. Caught by the pre-launch sweep, not by the
parse sweep — **8/8 GREEN is a syntax verdict, not a resolution one.** Found by
diffing `U1.*` used against `U1.*` defined. ⇒ **co-run briefs should require that
cross-check, it is one command.**

**I2 · The game launched UNARMED and ran 8 minutes doing nothing.** `metadata.lua`
never got its two lines. **Not C11** — I used a script file. I piped it through
`| Select-Object -First 2`, and `Select-Object -First N` **terminates the upstream
pipeline**, killing the script before its metadata write. Cycle 1's `-First 3`
happened to sit after the write, which is why only this cycle broke.
⇒ **C11 gains a corollary** (piping an arming script truncates its *execution*),
and the real repair is an **ARM GATE**: the launcher now reads `metadata.lua` and
`Code/` back off disk and refuses to launch unarmed. Cost of this class: 8 min →
0.2 s. ⚠️ **The owner spotted it before my outside bound did** — that is the
single most important line in this ledger for the co-run program.
⚠️ **NOT a watchdog defect**: it never fired because the probe never started. The
rig's watchdog is still *present, never fired* and this run must not be quoted as
its first test.

**I3 · A leg aborted citing a proof that had passed.** `U1.save_proven` is
per-process; cycle 0's proof is per-chain. Leg A printed "the SAVE primitive was
not proven in cycle 0" — the opposite of true. **Cycle 6 checks the same flag
first and would have produced nothing at all**, killing the only leg that samples
anything for leg D.

**I4 · Leg C's completion counter could not fail.** Scored 4 organic repairs
having observed none: the test was true on its first evaluation. WORKFLOW
leg-design rule 1, violated by a probe this chain authored. ⇒ **any co-run brief
whose leg counts completions must name its liveness witness in the brief.**

**I5 · Two probes discarded `pcall`'s result** (leg C, leg E). In leg E this
turned 34 crashes into "the vegetation early-out is the documented cause" — a
false sentence that would have been recorded as a measurement.

**I6 · A documented `[NEVER RUN]` command's recipe is broken.**
`table.copy(preset)` drops every inherited property default, so
`GenerateDustDevilIn` raises on `descr.duration`. **This is the strongest single
argument for the `[NEVER RUN]` marker discipline existing at all** — the row was
source-verified and wrong.

**I7 · Forcing C34's defect state made vanilla throw** —
`TerraformingDisasters.lua:411`, `UpdateRainsThreads`. Ours, in the marked
window; corroborates C34. Prompt 1 predicted it at `:190/:249/:280/:328` "if a
rain event fired" — right in kind, wrong in every specific.

**I8 · Cosmetic, but it burned reading time:** `storm_state`'s
`tostring(has(map) or "?")` renders `false` as `?`, and `el.broken` is a **table**,
not a boolean.

### 4 · Routed gaps — nothing dropped, none of them owner-blocking

1. **C42 needs a WITHIN-SESSION read** — passage traffic, then `C42STALE` before
   any save or load. Leg B's shape, no eyes. *(Also unanswered: does
   `Holder.units` persist? Source-answerable.)*
2. **PT-35 case A needs a fixture** — a save with Frictionless Composites
   researched and ≥1 upgraded building. A **fixture request, not a sitting**.
3. **The F99 residue rider stays `unrun`** — it needs a run in which `:805`
   actually throws.
4. **Leg C's N=4 can be widened** — ~1 min of machine time per 4 more.
5. **`CORUN0.savegame.sav`** from co-run #0 is still in the owner's saves folder;
   it should have died in that run's recording commit. Not touched by me.

### 5 · Owed, and what I could not do

- **Nothing is owed to the owner except decisions**: F99 severity (leg C's result
  is on their existing decision line as input, not as the decision), and whether
  D1+D2 close Do-first item 2.
- **No `02b_OPUS_CORUN.md` was raised.** No leg turned out to need eyes or hands.
  The one moment a human mattered was I2 — and that was a **stall**, not a
  measurement, which is an argument for better gates rather than for attendance.
- ⛔ **I audited my own rewrites.** Three legs run on code I wrote hours after the
  chain author parked it, and I am the wrong person to certify it. **That is Job
  1's real target.**
