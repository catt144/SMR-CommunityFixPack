# F106 chain — terminal audit (02): every verdict survived, three citations did not

⚠️ **A report is not authority** — entries win; primary evidence is
`docs/archive/f106_Mars.exe-20260824-02.32.27.log`. Written 2026-08-24 by
`02_AUDIT_fable.md` (terminal prompt, chain `f106-dispatch`, consumed in this
commit). Companion: `reports/F106_DISPATCH_SWEEP.md` (01's report, corrected in
place where noted) and `reports/F106_PREDICTIONS.md` (untouched — it is the
falsifiability artifact).

---

## 0 · What changes a decision — read this much

1. ⭐ **The refutation of F106 SURVIVES adversarial audit.** I re-derived the
   entire route at Src without trusting a single inherited citation:
   `Register` applies inline (`00_Core.lua:452`) while mod files load
   (`ModsLoadCode()`, `autorun.lua:423`), the whole of autorun.lua runs inside
   `dofile` at `lib.lua:370`, and the tree's ONLY `Msg("Autorun")` raise is
   **`lib.lua:371`** — after which `classes.lua:980` builds classes and copies
   the pack's wraps down. F33 is clean; the ~60-silent-wraps alarm stays
   withdrawn. **No claim from this chain was voided.**
2. ⭐ **F107 is real, measured, and independently re-verified as the pack's only
   nil-`prev` instance** (my own second static detector, different blind spots,
   same 8 sites, one defect). **Checklist 74 is unchanged and still yours**;
   option (a) is slightly STRENGTHENED — I verified at
   `ConstructionSite.lua:636-684` that the widening can only ever prevent an
   error, never cause one (the derivation is now on F107 and item 74).
3. ⚠️ **One citation the chain handed me did not check out — and had I trusted
   it in the other direction, a correct refutation could have been re-opened.**
   `autorun.lua:557` was cited as the `Msg("Autorun")` raise in F106, F107,
   F105, F33, EF-066, STATE and the sweep report; it is the HANDLER
   (`OnMsg.Autorun`, `:556-557`). The chain author's appended note flagged it;
   I verified rather than inherited it (whole-Src grep: `lib.lua:371` is the
   only raise). Corrected in all seven places. The ordering conclusion gets
   STRONGER, not weaker.
4. ⛔ **Owner action, verbatim from doccheck:**
   `warn STATE.md is 10596 bytes, warn threshold is 9216 — copy this line VERBATIM into the owner report; the owner fires agent/prompts/STATE_EVICTION.md`
5. ⛔ **Durability gap that needs your hands: the TestKit repo has NO git
   remote** (`git remote -v` is empty). Chain rule 10 ("push both repos")
   cannot be satisfied for it; four commits of instrument work
   (`e896243`, `4d3b851`, `1d240a4`, `ac4d46a`) exist on one disk only.
6. **Two rules adopted (Pass E), one of them machine-enforced from today** —
   §5 below. The enforcement demonstrably would have caught F107 on the day it
   was committed.

## 1 · The falsifiability claim, verified against the clock

The predictions commit `e2759bd` was **committed 02:31:21 and PUSHED 02:31:28**
(origin/main reflog, `update by push`); the archived log's boot stamp is
**02:32:27**. Predictions preceded the run. Grading (01's own §5 table checks
out against the log):

- Predictions 1 and 3 were WRONG, in one direction, for one reason — the model
  assumed post-build application. Writing them down first is what made the
  reversal one reading instead of an argument.
- ⚠️ **Prediction 4's tally (`75/1/24/0`) was EXACTLY right and misleading** —
  the 1 FAIL is `LandscapeCostGuard`, not the predicted `SmallLandscapeSites`.
  A tally that matches is not a prediction that was right; only the
  pre-declared per-probe expectations exposed that.

## 2 · Pass A — the probes, read as code (not by their verdicts)

| probe | can it FAIL? | production route? | own-logic expectation? | `debug.getinfo`? | PASS text honest? |
|---|---|---|---|---|---|
| `SmallLandscapeSites` (repaired, wave 3) | YES — an unwrapped leaf raises vanilla's nil-index on the 2-hex cache | YES — `setmetatable({…}, leaf)`, `site:GetClosestDests(…)`, the same `__index` path instances use (`classes.lua:730`) | NO — expected counts (2, 5) are independent constants; clause 0 (the old non-discriminating call) is kept but LABELLED as proving only the clamp | no | yes |
| `DispatchReach` (wave 14) | YES — FAILs on a missing class/method or a scan raise; its PASS is a completeness claim, and both header and report say "do not read PASS as the wraps are fine" | YES — `D[m]` is the full metatable resolution, literally the instance lookup; classes with foreign `__index` are flagged out (2 found, neither a target) | NO — identity comparison only | no | yes — and the one mislabel it shipped (multi-parent count called "build-time copies") was disclosed and repaired (TestKit `1d240a4`), not silently fixed |
| `LandscapeCostGuard` (wave 14) | YES — it DID fail, and clause 1 fails if the guard is missing (vanilla raises at `:673`) | YES — same metatable route | NO — clause 2's expectation (SetAmount 90, write-back 50) is computed from VANILLA's algorithm at `:669-680` | no | yes — PASS text explicitly disclaims the field route |

⚠️ One thing Pass A found that the chain missed: **the wave-14 file's own
header still asserted the refuted premise as fact** ("The pack applies every
fix AFTER ClassesBuilt") — an instrument documenting a mechanism its own first
run refuted. Corrected in TestKit `ac4d46a` (comments only, parse sweep GREEN,
disclosed there).

## 3 · Pass B — the sweep's arithmetic, recounted from primary evidence

Everything below computed by me, from the log or the tree, never from a summary:

- **Targets: 105.** Re-ran `tools/harvest_wrap_targets.py` (105 entries / 100
  distinct pairs / 46 classes) and counted the probe's generated table (105).
- **Clean targets ARE logged** — 105 per-target `SMRTEST-DISPATCH` lines in the
  log (109 with the two headers, TOTAL, and the `__index` warning). A sweep
  that crashed early could not fake this.
- **The TOTAL line's arithmetic reproduces from the per-target lines**: my
  independent parse sums to clean=97, with-unreached=8, desc=13,127,
  reach=1,981, UNREACHED=66, MULTI=11,080, multi-unreached=1,328 — every
  figure matches.
- **Multi-parent is reported separately, never folded** — verified in the probe
  code (separate counters) and the TOTAL line. Better than the brief's
  "UNKNOWN": the values ARE measured (`D[m]` reads what production resolves),
  and the separation is a provenance label. The old §3 question ("is the
  flagged/un-flagged classification right?") is moot under classdef-time
  application, exactly as 01 said.
- **Spot-checks at Src, mine:** HIT re-derived — `Fix_TrainsToVoid
  Building.OnDemolish UNREACHED=4` is `AsteroidCatcherBase:OnDemolish`
  (`AsteroidCatcher.lua:188`) and `TradePadBase:OnDemolish` (`TradePad.lua:209`)
  plus their leaves. CLEAN re-derived — `Dome.RefreshFreeLivingSpaces
  UNREACHED=0`: the only other declarations are `Community` (an ancestor, above
  the wrap) and `MicroGHabitatBase` (`MicroGHabitat.lua:42`), which is NOT a
  Dome descendant (`__parents` = LivingBase/LifeSupportConsumer/WaypointsObj/
  Community/MicroGHabitatAutoResolve). The expensive false-negative error is
  absent where I looked.
- **01's own corrected spot-check verified**: the four `SetDome` re-declarers
  are exactly `Residence.lua:171`, `ResearchLab.lua:179` (BaseResearchLab),
  `TrainingBuilding.lua:81`, `WaterReclamation.lua:78` — all multi-parent, which
  is why they sit in `Building.SetDome`'s MULTI=478 (unreached 40) rather than
  the single-parent column. The 578-gap citations
  (`Building.lua:591`/`:598` vs `BaseBuilding.lua:326`/`:355`) and the
  RC Constructor pair (`RCConstructorBase.lua:341`/`:356`) also check out.
- ⭐ **The instantiation gap is stated on every surface** — entry (F106, F107),
  report, EF-066, STATE, checklist 74, and inside the probe's own PASS text.
  No surface lets the hit count read as a broken-fix count. **Checklist 74's
  audit stays half-open permanently on instantiation; nothing may close it.**

## 4 · Pass C/D — verification sampling and the owed-work sweep

- **Run top healthy**, from the log: `Build version: 1.0.7.396349` (EF-014 pin),
  `fix pack present: 78/78 fixes active`, 78 `: applied` (equals doccheck's 78
  registered modules), suite `75 PASS, 1 FAIL, 24 SKIP, 0 ERROR` of 100 (probe
  count matches doccheck), opt-in and save-rescue both absent as required,
  armed → BEGIN → END → done. Readings stand.
- **F33 per-leaf verdicts** re-read from the log's own lines (3 ×
  `rawget=own-copy resolved==base=true`, PASS text naming all three leaves).
  `fixed` is the right status word; nothing here claims a screen event.
- **Unexplained lines:** the 60 `[LUA ERROR]` are 59×`Flight.lua:465` +
  1×`:479`; I re-aged them (49/60/0/0 across `vl97a`/`u3suite`/`u2run3`/
  `corun1` — new-colony legs have them, save-loading legs don't), matching
  F49:46's profile. ⚠️ 01's "none unexplained" under-enumerated: the log also
  holds 2×`[Braze] SessionStart error` and 2×`[ResManager
  Error] …LawOfficeDoor…` — aged by me at exactly 2 per `Mars.exe` leg back to
  2026-08-04, pack on or off; ambient, intersecting nothing. Report corrected
  to carry them.
- **Disclosure discipline held**: both false-greens are disclosed on entries and
  in TestKit commit messages, never silently repaired; the F33 probe's old call
  survives as labelled clause 0.
- **Mechanics:** log archived via `git add -f` in the commit that flips the
  entries (`334de62`, 1,477 lines — matches my count); harness disarmed
  (`metadata.lua` carries no `96_AutoRunFlag` row; TestKit tree clean); the
  `classes.lua:986-988` inverted-comment warning is on F106/F105/EF-066 and the
  report; EF-066 carries the dated 105-target measurement; checklist 74 is
  re-packaged with a recommendation on the owner surface. Fix pack pushed;
  TestKit unpushable (§0.5).
- **Corrections this audit made beyond the `:557` family** (all in
  `e4caf55`): `ClassNonInheritableMembers` reads `{ UNREADABLE }` because the
  builder ERASES it at `classes.lua:1091` after build — not "a mod environment
  cannot see it"; "the only writer of `construction_costs_at_start`" was too
  strong (`Track.lua:651` writes it on a track group leader — F49's latent
  territory, unreachable from landscape classes; latency verdict unchanged);
  `classes.lua:729`→`:730` for the `__index` line; F105's cross-ref still
  called F33 "now F106-suspect"; checklist 72's annotation still presented the
  refuted mechanism as a valid correction. **None of these voids a claim.**
- **The upstream "claims to attack", each with a verdict:** (1) ordering —
  CONFIRMED, §0. (2) "only instance" — independently re-derived, CONFIRMED
  static ×2, and now enforced forward by the FIX_POLICY §2 gate rather than by
  a one-off probe build. (3) the `applied` corollary — SOUND: `Require`'s
  class+method check is a plain index on a metatable-less classdef
  (`00_Core.lua:130`), so 78 `applied` ⇒ every declared pair is self-declared;
  the residual is precisely the non-declared install sites, all six verified at
  Src. (4) the F107 recommendation's sweep line — re-read from the log; the 3
  UNREACHED are exactly the three leaves holding this module's own wrappers
  (`own-copy 3`), and `RefreshConstructionResources` has a single declaration
  tree-wide (`ConstructionSite.lua:665`), so one wrap on `ConstructionSite` is
  exhaustive for shipped classes. (5) latency — condition SAMPLED by me (all
  writers of the field enumerated; the one non-gatherer writer cannot touch a
  landscape class). (6) the 578-gap — citations verified; it is EF-066-class
  under-coverage, correctly routed, no entry owed (existing behaviour kept,
  never new harm — the same call link 5 made at 1.0.0). (7) Flight noise —
  aged, carried on F49/C47, correctly not re-filed. (8) both instrument
  disclosures — verified in the probe source and `1d240a4`.

## 5 · Pass E — the rule decision (it was a real decision)

**Adopted both, in the surfaces that bind:**

1. **WORKFLOW leg-design rules** — *a probe must reach the code the way
   production reaches it, and must not compute its expectation with the fix's
   own logic; guard probes also assert delegation.* Two independent instances
   (C50 `8feaf59`, F33 `e896243`) is enough base when the repair of the second
   produced this chain's entire result — the strongest possible demonstration
   that the rule's absence had been hiding real answers.
2. **FIX_POLICY §2 — the F107 rule**, and it is ENFORCED, not advisory:
   every capture+install `(class, method)` pair must appear in its module's
   `Require` block. `tools/harvest_wrap_targets.py --check` (wired into
   doccheck, RED on violation) flags the shape statically.
   ⭐ Falsifiability of the checker itself: with its allowlist cleared it flags
   8 sites **including all three F107 installs** — the gate would have gone red
   on the day F107 was committed, no launch needed. Five pre-rule benign sites
   are allowlisted with Src citations; F107's three rows are allowlisted as a
   FILED DEFECT and leave with its repair.
3. **CHAIN_METHOD §4.1** — chain folders are committed at authoring time; both
   self-consumption and `git checkout --` silently no-op on an untracked
   folder, which is how this chain's own `02` was part-destroyed and
   reconstructed from memory. (The reconstruction, for the record, was
   faithful: every §1–§8 instruction I executed reconciled with the chain's
   README and the standing rules.)

## 6 · Owed and open — routed, so nothing goes quiet

- **Checklist 74 (yours):** repair F107 before the queued 1.0.x upload, or
  upload knowing. Recommendation stands: **(a)**, one wrap on
  `ConstructionSite` — now with the widening verified error-preventing-only.
  The repair commit must also rewrite the module's header (it still asserts
  the refuted premise; noted on F107) and delete the three F107 allowlist rows
  in `harvest_wrap_targets.py`.
- **Checklist 73 (yours, untouched by this chain):** the blame surface —
  four tiered options, undecided.
- **The queued 1.0.x upload sitting (yours):** waits on 74's decision.
- **STATE eviction (yours):** the verbatim warn line in §0.4.
- **TestKit remote (yours):** §0.5 — until it has one, its record is one disk.
- **F105 field route (a co-run rider, not this chain's):** the guard is
  measured; a cost tech sweeping a real levelling site on a real map has never
  run. It must not vanish between F105 reading `fixed` and F107 taking the
  attention.
- **F104 (open, not ours):** reporter reply + confirmation, then close.

## 7 · What is NOT claimed

No `tested-attended` anything — nobody watched; screen events unclaimed. The
checklist-74 audit is NOT complete (instantiation unmeasured, permanently by
this instrument). The "only instance" claim remains STATIC (twice-derived,
now gate-enforced forward — still not a behavioural measurement). Every count
above was recomputed by me from the log, the tree, or the tools named beside it.

---

**Next chain: none is queued.** The next moves are yours, in order of blockage:
decide **checklist 74** (its repair is a normal post-release-priced change:
module edit + `items.lua` untouched + one boot `applied` log + doccheck), then
the **1.0.x upload sitting**; **checklist 73** remains the open design
decision; the **opt-in pack effort** (checklist 68) starts after the upload,
kicking off from that repo's own STATE and
`reports/PARKED_OPTIN_REFERENCES.md`.
