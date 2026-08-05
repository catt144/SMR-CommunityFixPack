# Chain prompt 3 — adversarial audit, integration, chain close

**Read `README.md` in this folder first — binding chain rules apply. You are
the terminal prompt: this folder must be EMPTY when you finish.** Unattended.
Start with `git log --oneline -10` + `git pull`. Todo list up front.

**Read path**: this folder's remaining files · the outbox below · every
entry/checklist line prompt 2 touched · the archived logs it cites · the
unattended-1 audit precedent
(`git show 2d9e901:docs/archive/SESSION_LOG.md` — the close entry — and the
consumed audit prompt at
`git show a433e42:docs/agent/prompts/unattended-1/03_FABLE_AUDIT.md`).

**Every "done", "PASS", "SKIP", "tested" and "measured" upstream is a
claim.** This sitting was attended, which changes WHAT the audit floor is
for: the owner witnessed the Tier-A moments, so your target is the record —
does the written verdict match the log AND the owner's recorded verdict
words? — plus everything nobody watches even in an attended sitting: commit
discipline, forced/organic honesty, condition-sampled zeros, the actuals.

## Jobs

**Job 1 — audit the record, verdict-by-verdict, against the archived logs.**
Cited lines say what the entries now say; forced/organic labels present and
honest; every zero states its sampled condition; `SKIP` reasons true against
prep's confirm reads; **any `tested` grant traces to a named Tier-A moment
whose claim is the ENTRY's claim** — a `tested` carried by a log line alone
is demoted, visibly, with the demotion stated on the card per the adopted
tiers. Both `[NEVER RUN]` instrument executions (`StartBombard`,
`ProcessTrackElements`) were first executions: verify the printed `pcall`
results and witnesses exist in the log. Commit discipline: probes deleted in
recording commits, sweeps present, staged/throwaway saves gone (the leg-5
FIXTURE save is the one deliberate survivor — verify it is named in a
recording commit and actually on disk), every cited log archived (`git show`
it — a claimed archive a plain `git add` silently dropped is the known
failure). ⛔ A missing archived log is an automatic finding. Corrections
visible, never silent; a correction that changes a verdict re-routes that
item to the owner.

**Job 2 — the F48 decision package.** PT-37 is a DECIDER: if both cases
completed, verify the readings support exactly one of the entry's two
outcomes (unblock into sanitizer / close `wontfix`) and put THAT decision in
front of the owner on the checklist with the evidence lines — the audit
routes it, never takes it. If the sitting already recorded the owner's live
verdict words on it, integration means landing their decision, not
re-deciding.

**Job 3 — the co-run program report (the second product).** Actuals vs the
brief: wall time per leg, owner-minutes vs estimate, moments that overran,
asks that turned out unnecessary. The unforeseen-issues ledger vs
unattended-1's baseline: what recurred (a guardrail that failed twice is a
broken guardrail), what is NEW to attended runs (owner-interaction classes
the unattended ledger could not see). Route brief-authoring lessons into
`WORKFLOW.md` "Co-runs" surgically; the batch's economics go in
`SESSION_LOG.md`.

**Job 4 — integrate.** Entries carry their verdicts (verify, don't rewrite);
checklist: strike/annotate what this sitting settled; completed sections move
WHOLE to `PLAYTEST_ARCHIVE.md` per the documented rule (PT-37/PT-47 if
complete); `STATE.md`: chain CLOSED line + F48 outcome + open-decisions count
(cap 60, evict in-commit); `SESSION_LOG.md`: the chain's record newest-first
(verdicts, actuals-vs-predictions, economics incl. owner-minutes actual vs
estimate, the unforeseen delta); `CHAIN_METHOD.md`: one lesson ONLY if the
first BATCHED co-run taught something unattended-1 and corun-rig did not.

**Job 5 — close the chain.** Delete every remaining file in this folder in
the closing commit (parked sources included — cite the pre-deletion sha in
the SESSION_LOG record). doccheck green, push. Report to the owner: what ran,
what each leg found, what it cost against the estimate, what the audit
caught, what is owed or routed. ⛔ **The report ENDS with the next-chain
kickoff** (chain rule 14): read `STATE.md`'s NEXT pointer and give the exact
line — or say plainly nothing is queued and name what the front of the queue
looks like.

## Stop conditions

- A load-bearing verdict fails its audit and the logs cannot settle it →
  correct visibly, re-route to the owner, keep closing.
- The sitting was partial (owner left, stop condition): audit what ran,
  inventory the remainder into TAKEABLE riders with staged state cleaned up,
  and still empty the folder.

## ⛔ What you may not claim

- Not `tested` for anything the owner's eyes were not on — the tiers say what
  sign-off each result gets, and the audit enforces the tier, never upgrades
  it.
- Not "the co-run program is validated" from one batch — report the delta
  against unattended-1's ledger and stop there.
- Not F48's decision, PT-42's faction verdicts beyond what was sampled, or
  any severity call — routed, the owner's.

## Notes from upstream

*(Prompt 2 appends its handoff here.)*

*(Appended by chain prompt 2, 2026-08-05 — the sitting's product. Evidence log:
`docs/archive/cb1sitting_Mars.exe-20260805-14.28.49.log`, archived `git add -f`
in this commit. Uptime at close `1:58:42`, 8 loads, one process, one save
lineage: `CB1STAGE` → `CB1CASEA` → `F99UG`.)*

## 0. ⛔ Read this before auditing anything else

**The sitting did not run its own plan.** Legs 1 (PT-37) and 4 (PT-53 E) ran;
**PT-47, the popup trio + F85, PT-35 and the PT-53 uninstall half never ran at
all.** The owner spent roughly **two hours** against a brief promising ~24
attended minutes, and most of the overrun went into (a) building leg 4's fixture
live because the one prep measured had evaporated, and (b) the owner's own F99
investigation, which they drove and which produced the sitting's most novel
finding. **Audit the cost honestly — it is the largest single deviation here.**

## 1. Per-leg verdicts, with their evidence

| leg | verdict | recorded |
|---|---|---|
| **1 — PT-37 / F48 case A** | **PASS, better than a no-op.** `connections_total` 559→558 (= `2×279`, the clean-chain value); `start_el`/`end_el`/`node_idx`/`n` unchanged; **persisted through save+reload**. Owner Tier-A verbatim: *"I seen a train pass through every station atleast once"* | `agent/bugs/F48.md` |
| **1 — case B** | ⛔ **DECIDER UNSAMPLED; prediction 3 FALSIFIED.** 8 broken elements + 8 repair sites, yet `shadowed=0 missing=0`. The gate REFUSED the leg. **Settles the C-side question: `HexGetTrackGridElement` returns the hidden original**, so the assert is unreachable via meteor damage and F48's blocking premise is contradicted for the scenario it cites | `agent/bugs/F48.md` |
| **3 — PT-42** | **SKIP**, re-confirmed LIVE (not on prep's word): LastTransmission 0 of 5 active, 0 seats | this file |
| **4 — PT-53 E, in-dome** | **MEASURED DRAIN**: Seniors-in-normal 76→37 as slots came online; 0 in-dome-reachable at steady state. **Prediction 10 HOLDS** | `agent/bugs/D07.md` |
| **4 — PT-53 E, precedence** | **ROUTED**, fixture unholdable after 3 attempts. Owner design decision raised instead | `agent/bugs/D07.md` + checklist |
| **C42 ride-along** | ⛔ **UNSAMPLED**, gap NOT discharged: 0 unit entries over population 0, **no traversal witness exists** | this file |
| **F21 ride-along** | **HALF measured** — platform population read (11 stations / 21 waiting); penalty half UNMEASURED, all trains `spent_time=nil` | this file |
| **F99** (opportunistic, out of scope, owner-driven) | **two witnessed NEGATIVES**, both rate bounds not refutations; one 2×2 cell still empty | `agent/bugs/F99.md` |
| ⭐ **F101** (new) | **5 witnessed throws**, two mechanisms, owner attribution for each | `agent/bugs/F101.md` |
| **D12** (new) | `Opt_NoHomeless` self-check names the wrong class (F64 shape); recovers | `agent/bugs/D12.md` |

## 2. Predictions vs actuals — audit these hardest

- **1, 2 HOLD.** **3 FALSIFIED** — prep had flagged it genuinely 50/50, so the
  harness's refusal is the design working, not a miss. **4 NOT REACHED** (no
  failure path existed to inspect).
- **5–9 NOT RUN** (PT-47 never happened). **13 UNSAMPLED**, **14 UNMEASURED**,
  **15 NOT RUN**.
- **10 HOLDS at steady state** — but see S4: the instrument asserted the
  opposite three times before the steady state arrived.
- ⚖️ **Audit target:** the case-A "559→558 is a repair" reading is an
  **inference from a count**, not a per-connection proof. It is labelled as such
  on the entry. Decide whether the entry still over-reaches.

## 3. Unforeseen-issues ledger (8 entries; unattended-1 had 8, prep had 6)

| # | what | class |
|---|---|---|
| S1 | Leg 2 aimed at the wrong map — `WaitBombard` hard-codes `MainMap` (shipped **and** the pack's replacement) while `LabelAll` walks every city; the watcher would have polled a table nothing writes to and reported "never started" | **recurrence** of prep's P2; caught PRE-FLIGHT, fixed before launch |
| S2 | M1 had 3 minutes budgeted and no instrument to find its subject among 184 Seniors / 108 residences | **new**: a measure moment with no way to reach its subject |
| S3 | The parked `CB1_ARM.ps1.txt` will not run via a plain `Copy-Item` — PS 5.1 reads a no-BOM `.ps1` as ANSI and the em-dashes break the parse | **new**, exact mirror of prep's P4 (BOM added where unwanted → BOM absent where required) |
| S4 | `CB1.Leg4Pick` printed **"PREDICTION 10 FALSIFIED … a DEFECT to file against D07"** three times off single snapshots, with no settling window and no screen for the module's own exemptions. All three were transients mid-drain | **new**, and it is prep's P2 family inside a reader written the same day |
| S5 | `CB1.Leg4Before(SelectedObj)` stored a `LifeSupportGridElement` without type-checking, poisoning `leg4_colonist`; `Leg4After` prefers the poisoned ref | **new**: an instrument that trusts whatever the UI selection happened to be |
| S6 | **Structural:** the rig can launch and arm but has **no input path into a running game**, and this sitting was console-driven by design — so the owner typed every line. The measure-moments model counts only the moments | **new**, and it under-counts owner time for *every* attended sitting |
| S7 | `D07` entry stale vs `PLAYTEST_ARCHIVE` (trigger A passed 2026-07-30); prep inherited it and wrote a false SKIP line; prompt 2 repeated it twice; **the owner corrected it from memory** | **recurrence** of "recorded facts are claims too" |
| S8 | Two static audit scripts produced **four** distinct false-positive classes (`else` branches, `end -- comment` closers, `local` with a dev override, call sites in unshipped editor code) before per-candidate verification | **new**: a static auditor over-claiming; only 2 of ~45 candidates verified, only those filed |

**What that says about the guardrails.** G1 earned itself twice — the pre-flight
pass found S1 before launch, and the entry-point check it grew was new. **G2 is
the sitting's hero:** it is why case B refused, why both F99 samples carry
completion witnesses, and why C42 is recorded UNSAMPLED rather than as a zero.
**G2's absence is equally the root cause of S4 and S5** — the readers added
mid-chain carried no witnesses, which is exactly the rule prep applied to the
legs but not to its own instruments.

## 4. Owner decisions taken live (verbatim) vs still open

**Taken live:**

- On how to test D07 precedence: *"Why not just build a new retirement home"* —
  adopted; better than the eviction plan proposed to them.
- On witness discipline during a hunt: *"unless there is a real reason we need
  that everything even with no lua errors ?"* — **correct, and conceded.** A
  witness is needed to record a NEGATIVE, not to run a hunt. **Audit whether the
  rule was over-applied elsewhere in this sitting.**
- On stopping: *"I agree with this one last log dump, it was my last idea"* →
  PT-47/M5/M6/M7 dropped, sitting closed.
- Attribution, given on request for both F101 mechanisms: *"Test meteor will not
  work"* (infopanel click) and *"opened the inspector"*.

**Still open — all four routed to `PLAYTEST_CHECKLIST.md` "Decisions waiting on
you"; none decided here:** F48 unblock · D07 forced-residence vs forced-dome ·
F101 severity · D12 preflight fix.

## 5. Routed gaps (do not let these drop)

1. **PT-47 / M5 / M6 / M7** — never ran. M7 still needs owner hands for the
   Mod-Manager click; the rig cannot do it.
2. **C42 within-session** — still UNDISCHARGED, and now known to need a
   **traversal witness**, not merely traffic.
3. **F21 penalty half** — reader gap; `ts_spent_time` and `spent_time` both nil.
4. **F99's untested cell** — repair-path sites across MULTIPLE merging tracks.
   Instrument: `SelectedObj:CheatBreakElement()` (ungated, works on retail).
5. **F101's third instance** — console `!` → `ShowMe`, static only, unwitnessed.
6. **The dev-gate audit** — ~45 candidates, 2 verified. The rest need per-file
   reading before any is claimed.

## 6. What prompt 3 must not do

- Do not upgrade case A to `tested` beyond what the owner's eyes covered: they
  witnessed **route formation and trains running**, not the connection count.
- Do not read case B's result as "F48 is safe" — it refutes **one route** to the
  assert.
- Do not treat F99's two negatives as a refutation, or C42's zero as a negative.
- Do not report owner-minutes "saved". Report ~2 h against a ~24 min promise.

## 7. Late amendment — a restart was attempted for PT-47 and ABORTED

Recorded per chain rule 5 (drift corrected visibly, never silently). After the
close-out had begun, the owner clarified that "lets move on" had meant *move on
to the remaining legs*, not *close the sitting* — prompt 2 had misread it. The
game had already been closed and the harness disarmed, so a fresh `CB1STAGE`
copy was staged, the harness re-armed (ARM GATE GREEN) and a relaunch issued at
**16:50:11**. The owner then decided against deviating further:

> *"Actually since you have already deleted prompt and made notes lets not
> deveate from the chain. lets let fable audit and out context has probably
> gotten tight, lets close"*

⇒ **The relaunch was abandoned before any leg ran.** No second log was consumed,
no second save lineage exists, and the second `CB1STAGE` copy was deleted along
with the first. **PT-47 / M5 / M6 / M7 remain NEVER RUN and routed** — the state
described in §0 and §5 is unchanged by this amendment.

**Close-out state at hand-off:** disarm GREEN, `PROBE SWEEP: clean` in both
repos, both working trees clean, all four staged/throwaway saves deleted, and
`TEST2H TRAIN` verified byte-identical (MD5 `103B320A1434513BC8773553096A8958`,
LastWriteTime still 2026-08-03 22:21:48) — the campaign save was never opened,
let alone written.
