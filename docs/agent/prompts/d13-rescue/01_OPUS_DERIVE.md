# Chain prompt 1 — the authoritative derivation, the disposition draft, the two questions

**Read `README.md` first — binding chain rules apply.** Staleness check (all
three repos), todo list before anything else — one item per job below, expanded
the moment a job turns out to be more units than listed.

**Read path (file granularity):** `agent/bugs/D13.md` WHOLE (the requirement
record — every constraint in this prompt traces there) · `agent/FIX_POLICY.md`
§3 + §3a WHOLE (the mechanism statement, the three-tier ethos, the orphan gate,
the layer ordering) · `agent/reports/F86_ADJUDICATION.md` §3.1/§5.1/§8 (the
capture-route adjudication and the enumeration-blindness finding) ·
`agent/reports/SAVE_SAFETY_REDESIGN.md` (the prior disposition framing and its
stale denominators) · `agent/facts/INDEX.md` scan + OPEN the persistence-
mechanism facts your derivation leans on · both repos' `Code/` — every shipped
file · `tools/blocking_analysis.py` header (its v2 semantics: DIRECT is
trustworthy, propagation only through unambiguous callees, AMBIGUOUS is read by
hand). The indexes find more; the D13 entry's report list is 2026-08-01-era
with PRE-restructure paths — translate, re-sweep, trust nothing as complete.

## Job 1 — the exposed set, derived (the chain's load-bearing product)

Enumerate, over `C:\Dev\SMR-BugFixPack\Code\` AND `C:\Dev\SMR-OptInPack\Code\`
(the TestKit ships nowhere and is OUT), every site where anything of ours can
enter a savegame. Constitution rule 6a binds: all five shapes (class-method
wrap / table-slot / global assignment / preset-field / own-thread) UNION the
§3a capture routes ((a) blocked game-time-thread frames, (b) captured
locals/upvalues of any frame — engine frames included, (c) persisted state:
object fields, GameVar contents, notification closures). Method requirements:

* Run `blocking_analysis.py` over both trees as the INSTRUMENT; then read
  every candidate — and every AMBIGUOUS — at source before filing. A site
  files only on a per-candidate reading (corun-batch-1 rule 6). State what
  the instrument missed that hand-reading found, and vice versa — that
  reconciliation is evidence the sweep was real.
* Per site, the row records: repo · file:line · shape/route · the EXACT
  name(s)/value(s) that persist · the §3a orphan question answered (dies /
  expires / runs forever after uninstall — and would anyone notice) ·
  orphan-gate present? · Tier 1/2 already repairs it? · provenance tag
  (MEASURED / SOURCE / INFERRED), per row, never blanket.
* ⛔ The five persisted names the opt-in pack writes
  (`SMRFixPack_ack_notworking`, `SMRFixPack_closed_to_new_residents`,
  `SMRFixPack_no_homeless`, `SMRFixPack_DroneSpeedDial`,
  `SMRFixPack_DroneCarryDial`) are save contract (its `PROVENANCE.md` §2) —
  they appear in this table like everything else, and their disposition is
  decided here like everything else. So do the fix pack's
  (`SMRFixPack_F48_StationConnectors`, `SMRFixPack_reserved_at` — the
  fixture-measured 919×/1257× field — `SMRFixPack_F35_<label>` modifiers,
  `SMRFixPack_FirstAsteroidPrefabs`, `SMRFixPack_MeteorLatch`, and whatever
  else the derivation actually finds; those six names are a starting claim
  from the split audit's logs, not a list to inherit).

## Job 2 — reconcile against every historical number, both ways

The record says 12, then 13, then "≥13", and the F86 builds changed the set
underneath. Diff your derived membership against the ≥13-era list and explain
EVERY difference in both directions (added: why the old grep was blind to it;
removed: which Tier repaired it, cited). A derivation that cannot explain its
own deltas has not superseded the record — it has just disagreed with it.

## Job 3 — the curated KEEP/REMOVE draft (constitution 6b/6c)

Every persisted name and every capturable body lands on exactly one list:
**KEEP** (the residue is a repair or an inert latch — why-kept, what breaks if
removed) or **REMOVE** (why-safe, what reads it, what happens on a save that
never had it). A name on neither list is a derivation gap. Known traps bind:
`SMRFixPack_F35_<label>` modifiers ARE the repair; thread restarts reset
intervals (one-shot only); detection is by THIS list, never pattern-guess.

## Job 4 — the disposition-table draft (FIX_POLICY §3a release gate)

Per site from Job 1: **repaired-in-pack** (which Tier, cited) ·
**inert-accepted** (three-tier ethos level 2 — named, bounded, disclosed) ·
**cleaner-target** (what the artifact does about it, per Job 3's lists) ·
**KEEP**. ⛔ Rule 6f: a site with an apparently reachable in-pack route and no
existing repair does NOT get "cleaner-target" — it gets **ROUTED** (stop on
it, package the in-pack repair with cost, offer the inserted build prompt).

## Job 5 — the artifact design sketch + the two questions

* Verify the channel-dissolving argument from README rule 7 (a mod-shaped
  artifact is the only shape that reaches console at all; a console procedure
  reaches nobody there) — from the D13 entry's console-channel findings, not
  from vibes. Then package **Q-A** (player story a/b/c) and **Q-B** (confirm
  mod-shaped + channel note) into `docs/PLAYTEST_CHECKLIST.md` → "Decisions
  waiting on you", each one line + recommendation + what each option costs,
  reasoning pointer back to your draft. The entry's own architecture points
  at (c) — the pack already IS its own cleaner via Tier 1/2, so the artifact
  serves the already-removed case — but CONFIRM that against your Job 1/4
  data before recommending it.
* Sketch the artifact per Q-A branch (mechanism core is shared; say what
  actually differs per branch so the owner's answer selects rather than
  respecifies): detection (curated list as embedded data), the clean pass
  (synchronous, ordered, one-shot restarts), reporting (what the player
  sees), self-removal story, version-skew statement. Propose the repo/
  packaging shape (working name, third junction, scaffolding depth — the
  split's `SMR-OptInPack` scaffold is the precedent; say what this one does
  NOT need and why). Constitution 6d binds the sketch.

## Output and close

Write `90_DERIVATION.md` in THIS folder (the QA's subject; prompt 3 promotes
the corrected version to `agent/reports/D13_EXPOSED_SET.md` — the draft never
outlives the chain). Checklist edits committed (doccheck GREEN first). Append
your outbox to `02_FABLE_QA.md` `## Notes from upstream`: the derived count
and membership, the deltas-vs-record explanation, the KEEP/REMOVE lists, any
6f routings, the questions as packaged, and EVERY place you were uncertain —
the QA attacks your doubts first. Delete this file in the same commit.

## ⛔ What you may not claim

- Not "complete" for the enumeration — that word belongs to prompt 2's
  verdict and prompt 5's re-derivation, never to the deriving session.
- Not "safe to remove" for any name without its REMOVE row's why-safe filled
  from source reading.
- Not "already repaired" without citing the Tier commit/lines that repair it.
- No count without its per-row provenance tags behind it.

## Notes from upstream (chain authoring, 2026-08-12)

* Authored the evening the split-optins chain closed; both trees are
  audit-sustained as of fix-pack `ada5cbb` / opt-pack `a90d128`. The split
  audit re-verified: 11 `SMRFixPack` tokens in the opt pack (5 persisted-name
  definitions + 6 comments, zero references); the five opt-side persisted
  names read back live off 4 real saves; `EF-055`'s junction route re-derived
  from Src (its fact file cites the exact lines).
* The split matrix's FixtureCarry dumps (`archive/spd2_*`, `spe_*` logs) are
  MEASURED field inventories on real saves — `SMRFixPack_reserved_at` on
  1257/1260/1336 objects, `payload_set` on 3, `shelter_try` on 0–1, the three
  opt flags, `FirstAsteroidPrefabs`/`MeteorLatch` GameVars — use them as
  ground truth to CHECK your derivation's field list against, not as the list.
* `FactionFundingCheck`'s PASS→SKIP repair is queued on the probe itself
  (TestKit `62f03da`) for whichever chain touches the suite next — if your
  chain's prompt 3/4 re-baselines the suite anyway, it may take that repair
  and re-stamp the baseline in the same measured commit; if not, leave it.
