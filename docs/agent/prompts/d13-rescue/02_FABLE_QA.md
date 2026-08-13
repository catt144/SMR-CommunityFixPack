# Chain prompt 2 — fresh-context adversarial QA of the derivation (the gate)

**Read `README.md` first — binding chain rules apply. You are a GATE: prompt 3
may not run unless your verdict is BUILD.** Staleness check (all three repos),
todo list. Precedent floor: the split-optins QA (SESSION_LOG 2026-08-12 —
every MUST-FIX it raised was real) and the split-optins terminal audit's
method (re-derive the ROUTE, not the citations).

**Your posture: the derivation is WRONG until you fail to break it.** The
project's own history says this stance pays: the enumeration was 12, then 13,
corrected both ways in one day, by a grep later proven blind — and the
"empty `_ENV`" persistence belief survived two audits before dying. Every
number in `90_DERIVATION.md` is a claim by a session that wanted to finish.

## Job 1 — re-derive, independently, before reading the draft's reasoning

Take the draft's TABLE (membership + lists) but not its arguments. Then:

* Run your own five-shape + capture-route sweep over BOTH trees — your own
  instrument invocations, your own hand-reads. Diff your membership against
  the draft's. Every difference is a finding; zero differences is a claim
  about your sweep's independence, so vary the method (different grep axes,
  different candidate ordering, read the AMBIGUOUS set whole).
* Sample-verify per-row provenance: for every row tagged MEASURED, find the
  measurement; for SOURCE, open the cited lines; INFERRED rows are attack
  surface — try to convert or kill each one.
* ⛔ Attack the three historical blindness classes BY NAME: slot assignments,
  global assignments, preset fields — the exact shapes the old grep missed.
  Then attack route (b) (captured locals/upvalues of engine frames), which no
  grep sees at all: pick the modules with `Sleep`-bearing bodies and trace
  what their frames actually hold.

## Job 2 — attack the KEEP/REMOVE lists (the save-breaking surface)

* For every REMOVE: what reads this name on a HEALTHY save? What does the
  reading code do when it is gone? (The F35 trap generalises: a repair the
  cleaner deletes re-breaks the save silently.)
* For every KEEP: does keeping it strand anything on a save whose pack never
  returns? Is it inert by §3a's definition (named, bounded, incapable)?
* For every thread-restart: is the one-shot bound real in the draft's design,
  and is the interval-reset cost stated per thread?

## Job 3 — rule on the rest

* The disposition draft: every site dispositioned; every 6f candidate
  actually routed (a "cleaner-target" that hides a reachable in-pack repair
  is the failure shape §3a names).
* The two owner questions as packaged: options honest, costs real, the
  recommendation supported by the derivation data (not inherited from the
  entry's hint). The channel-dissolving argument verified or refuted.
* The artifact sketch vs constitution 6d: anything in it that could persist
  (a thread, a GameVar, a named field, a notification closure) fails here,
  not in prompt 4.
* The doc-correction plan: is the location re-sweep actually complete
  (post-restructure paths), or does it inherit the entry's 2026-08-01 table?

## Verdict and close

Verdict: **BUILD** / **BUILD with MUST-FIXes** (enumerated, each with its
exact edit) / **BACK TO DERIVE** (with the break that forced it). Correct the
draft in place (strike-and-supersede, visibly — never silently). Append your
outbox to `03_OPUS_BUILD.md` `## Notes from upstream`: the verdict, every
MUST-FIX, your membership diff and how it settled, and what you did NOT get
to (named residue for prompt 5). Commit (doccheck GREEN), delete this file in
the same commit.

## ⛔ What you may not claim

- Not "complete" without your own independent sweep having found ZERO
  membership differences OR every difference settled by source reading.
- Not "the lists are safe" without Job 2 run per-name, both directions.
- A verdict of BUILD with unconverted INFERRED rows on load-bearing sites is
  a contradiction — convert them, kill them, or hold the gate.

## Notes from upstream (prompt 1 appends here)

**From prompt 1 (Opus, 2026-08-12). Subject: `90_DERIVATION.md`, this folder.**
Staleness check ran clean: fix-pack `155869a`, opt-pack `a90d128`, TestKit
`62f03da` — all three at the commits the chain was authored against, all three
with clean trees. The two owner questions are packaged as **checklist items 17
and 18**, and a THIRD (item 19) had to be added — see "6f routings" below.
⛔ Prompt 3 now gates on **three** answers, not two.

### The derived count and membership

**27 sites over both trees**, deliberately finer-grained than any recorded
count: **12 capturable-code sites (E1-E12)** + **15 persisted-data sites
(D1-D15)**. The historical numbers counted capturable code in the fix pack
only, so the like-for-like comparison is **12 vs the recorded "13 + 1"**.
Membership and per-row provenance: `90_DERIVATION.md` §2. Every row carries its
own MEASURED / SOURCE / INFERRED tag; there is no blanket claim.

### Deltas vs the record, both directions (§4.1 has the full table)

* **Removed (4 modules), each with the tier that repaired it named:**
  `Fix_MeteorFrequency` (Tier 1 — layer 3, no mod thread body left),
  `Fix_DroneUnreachableForever` (Tier 2 — consumer patch, target synchronous),
  `Fix_TrainWaitTime` (Tier 2 — `AddSpentTime` wrapper, synchronous),
  `Opt_DroneOverhaul` (Tier 2 — moved off `Drone:Idle`, and out of the repo).
* **Added (1):** `Fix_BombardmentSpread`'s **per-missile closure** (E3) — the
  record counted the module once; it has two independently capturable bodies.
* **Same member, different reason (1):** `Fix_RainsDeadlock` (E1) stays exposed
  **only** because vanilla passes `RainsDisasterActivation` *by value* to
  `CreateGameTimeThread` (`TerraformingDisasters.lua:313`). Tier 1 removed the
  forever-orphan; what is left is a layer-2 frame.
* **Never on any list (2):** E12 (`Fix_MoraleComfortTooltip`'s instance-level
  `GetProperty` window) and the whole of §2b, because the historical
  enumeration key was a key for *code*, not for *state*.

### ⭐ The result I most want you to try to break (§1.4)

I closed the global-replacement shape **exhaustively** rather than by sampling.
17 globals are replaced across the two trees. **None is in `PersistableGlobals`
anywhere in `Src`** (checked name by name against
`CommonLua/Core/persist.lua:117-134`), and grepping `Src` for every *non-call*
use of all 17 returns **exactly one real hit in the entire source tree** — the
`RainsDisasterActivation` thread-body pass above. If that grep is unsound, a
whole shape re-opens. It is the single highest-leverage thing to re-run.

### Instrument-vs-hand reconciliation (§1.3) — read this before trusting either

The instrument produced **4 false positives**, all one defect class (bare-name
aggregation over every class declaring a method): `MirrorSphere:StartAction`
(the yield is in a nested closure, a different frame), `RCTransport:Interact-
WithObject`, and **both `Done` rows** — where the decider is that
`Train:DestroySilent` zeroes `demolishing_countdown` on the line *before*
calling `DoDemolish`, making that body's `Sleep` loop unreachable. Had the tool
been right, `Fix_TrackConnectorPingPong:185-188` would be a live layer-2
violation. Conversely, hand-reading recovered **two sites the tool's summary
line would have cleared**: `Colonist:Idle` *does* yield (`Colonist.lua:1783`,
`:1795`) and is a command, but Colonist was not among the four classes the
AMBIGUOUS evidence string happened to name.

### KEEP / REMOVE (§5) — 26 named entries, nothing on neither list

* **KEEP (4):** `SMRFixPack_F35_<label>` ⭐ (the residue IS the repair — a
  pattern-sweeping cleaner re-breaks the turbine buff), `..._F48_Station-
  Connectors`, `..._MeteorLatch`, and every captured frame in §2a.
* **REMOVE (13 names)**, each with why-safe, what-reads-it, and what a save
  that never had it looks like. ⭐ The headline is **`SMRFixPack_DroneSpeedDial`
  / `..._DroneCarryDial`** — the only residue in either pack that keeps
  *changing the game* after uninstall (the module's own header says the boost
  survives permanently). That single row is the artifact's reason to exist.
* One placement I flag as least certain: `SMRFixPack_FirstAsteroidPrefabs`
  (REMOVE) — reasoning and the counter-case are in its row.

### ⛔ 6f routings — 3 sites, and they became checklist item 19

`FIX_POLICY` §3a's orphan gate is written as a universal. Four modules own a
game-time thread body; **one complies** (`Fix_MeteorStormWedge`, gated `:145` /
re-armed `:156`). The other three — `Fix_CrystalMysteryHang:44-54`,
`Fix_ExtenderFlapChurn:77-84`, `Fix_TrackConnectorPingPong:156-160` — have
**no gate at all**, and all three are all-vanilla bodies, which under `EF-023`'s
corrected orphan-reach rule is exactly the case that *keeps executing* after
uninstall. Repair is three one-line insertions. Per rule 6f I did **not**
disposition them to the cleaner; they are ROUTED with cost and a recommended
inserted build prompt. ⚠️ A cleaner cannot reach them by construction anyway —
those bodies run *from* the save the moment it loads.

**Fourth item, comment-only, routed with them:**
`Fix_MeteorStormWedge.lua:138-141` still carries the **disproven** by-name
persistence model, contradicting its own rewritten header 80 lines above. So
**`EF-023`'s closing claim "nothing in `Code/` states it any more" is FALSE**
and needs correcting alongside the counts.

### The two questions as packaged (§8, checklist 17-18)

* **Q-A → item 17.** I recommend **(c)**, and §8.2 supports it from the Job 1/4
  data rather than from the entry's hint: the packs already heal the only two
  residues that ever *did* anything (meteor + rains, both onto vanilla bodies,
  on load), so the artifact's population is precisely the already-uninstalled
  player — who cannot run any in-pack pass, and whose save may be carrying D15.
  ⚠️ I also recorded the tension (c) creates: a once-per-save latch is
  persisted state and would violate 6d, so I recommend **no latch, idempotent
  pass instead**. Attack that.
* **Q-B → item 18.** The channel-dissolving argument is **verified** from the
  entry's own owner-run Paradox Mods findings (2026-08-01), not from vibes: a
  mod-shaped cleaner's reach is a strict superset of a console procedure's on
  every platform, and the only shape that reaches console *at all*.

### ⛔ Every place I am uncertain — §6 lists six; these are the load-bearing ones

1. **E7 / the general question: is a created-but-never-run game-time thread
   captured by a save?** Creation defers (`EF-029`), the body has no yield, and
   the thread-persist machinery is C-side (`cthreads.lua:224`). **This is the
   derivation's only load-bearing INFERRED row.** Convert it or kill it.
2. **E12's synchronicity argument** rests on `Colonist:UIStatUpdate`'s 201-line
   rollover path being yield-free; I checked *direct* yields only.
3. **D10 (`SMRFixPack_F35_*`) was never SAMPLED.** The FixtureCarry dumps show
   no F35 modifier — but those saves may simply not be affected saves. Absent
   ≠ refuted, and this is the headline KEEP entry.
4. **"A cleaner cannot touch §2a's captured frames at all"** — my working
   assumption, resting on adjudication §8.5. If it holds, §2a is entirely
   inert-accepted and the artifact **has no thread surgery in it**, which is a
   dramatic shrink versus every prior sizing. It deserves a hostile read
   precisely because it is convenient.
5. **Site-vs-module granularity.** E9/E10 are two wrappers on one method; E2/E3
   are two bodies in one module. A reviewer could defensibly say 10 code sites
   rather than 12. I chose the finer grain because the disposition is per-site,
   and I state it rather than smooth it.

### Housekeeping for you

* The doc-correction list (§4.3) was **re-swept live this session** against
  post-restructure paths — it is not the entry's 2026-08-01 table. Prompt 3
  executes it. Archive files are append-only and are NOT corrected.
* Instrument target list preserved at `scratchpad/d13_targets.json`
  (80 rows); re-run with `python tools/blocking_analysis.py <list>`.
* No probe was armed and no game was launched — this prompt was game-free.
