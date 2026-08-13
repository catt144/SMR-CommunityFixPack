# Chain prompt 3 — freeze the spec, build the artifact, correct every count

**Read `README.md` first — binding chain rules apply.** Staleness check (all
three repos), todo list. ⛔ **GATE CHECK BEFORE ANY WORK (README rule 7):**
prompt 2's verdict must be BUILD (its Notes below), and BOTH owner answers
(Q-A player story, Q-B channel/mod-shape confirmation) must be recorded on
`docs/PLAYTEST_CHECKLIST.md`. **Either missing → STOP: report which, commit
nothing but the report note, leave this file in place. The chain resumes here
when the owner answers.** Game closed throughout; nothing here launches.

## Job 1 — freeze the spec

From the QA-corrected `90_DERIVATION.md` + the owner's Q-A answer: write the
artifact spec INTO the derivation doc (one doc carries derivation → lists →
disposition → spec, so prompt 5 audits one chain of custody). The spec states:
detection (the curated list as embedded data — repo, name, kind, KEEP/REMOVE,
why), the clean pass order, the one-shot thread-restart set with per-thread
interval cost, what the player sees (report text), the version-skew statement
(which pack versions' residue it handles — say how a too-old or too-new save
is answered), the self-removal story, and the constitution-6d compliance
argument (why nothing of the artifact can persist).

## Job 2 — scaffold and build

* Scaffold the artifact repo per the QA-reviewed proposal (working name from
  prompt 1; LOCAL git, no remote unasked — README rule; junction installed
  but the mod NOT enabled — enabling is owner-only, and the verify prompt
  works junction-side per EF-055 regardless). Scaffolding depth per the
  proposal: the split's `SMR-OptInPack` scaffold is precedent, but this
  artifact is a single-purpose tool — carry PROVENANCE (what came from
  where), a README that answers the no-retraining questions AT ITS SIZE, and
  doccheck only if the proposal argued for it; do not cargo-cult the full
  pack apparatus where the proposal said it is not needed.
* Build the cleaner to the frozen spec. FIX_POLICY binds where it applies
  (fail-safe, never loud; self-checks return reasons, never error). Every
  Lua file parse-swept before commit.
* TestKit: teach the kit to see the artifact the way it learned the opt-in
  pack (a missing artifact is SKIP, never FAIL — it is legitimately absent
  from every config but the rescue ones), and write its probes: the clean
  pass on synthetic residue (KEEP survives, REMOVE goes, one-shot bound
  holds), the artifact-absent no-op, the version-skew answers. If you
  re-baseline the suite here, take the queued `FactionFundingCheck`
  PASS→SKIP repair (TestKit `62f03da`, comment on the probe) in the same
  measured commit and re-stamp the baseline everywhere it is quoted;
  otherwise leave it queued and say so.

## Job 3 — correct every count-stating doc (the derivation is authoritative)

Re-sweep BOTH repos' current docs for every count/denominator the derivation
supersedes ("≥13", "at least 13", "12 exposed", "five of the twelve", every
per-module denominator in the F86 reports). The D13 entry's location table is
the 2026-08-01 starting point with pre-restructure paths — translate and
re-sweep; your sweep's method line goes in the commit. Archive-tier files
(`docs/archive/`) are history and are NOT edited. Every corrected site cites
`agent/reports/D13_EXPOSED_SET.md` — which you create in this job by
promoting the QA-corrected derivation doc (the in-folder draft stays until
prompt 5 deletes the folder). Update the D13 entry itself: front-matter +
heading tag to `speced`/`built` per the truth at your close (edit order:
front matter first, then tag — doccheck red means you stopped halfway).

## Close

doccheck GREEN in every repo that has it; parse sweep GREEN; PROBE SWEEP line
in every result-bearing commit. Append your outbox to `04_OPUS_VERIFY.md`
`## Notes from upstream`: what shipped where (repos, shas), the spec's
verification-relevant promises (exact KEEP/REMOVE names the matrix must read,
the thread set, the version-skew answers), the fixture requirements you
foresee (which saves carry which residue classes — the split matrix's
FixtureCarry dumps say PT35FIXTURE carries fields + `MeteorLatch`; say what a
PRE-REWRITE-lineage witness needs and whether one exists in the save folder
BY NAME, or must be manufactured by a probe writing synthetic residue), and
every uncertainty. Delete this file in the same commit.

## ⛔ What you may not claim

- Not "the artifact works" — nothing launched; every claim here is
  static/probe-design tier and says so.
- Not "residue-zero" — that is prompt 4's measured claim; yours is the
  compliance ARGUMENT (no thread, no GameVar, no field, no closure — cited).
- Not "all docs corrected" without the sweep method stated and the archive
  exclusion honored.
- Not "suite baseline unchanged" if you touched any probe — recount or say
  which change is pending measurement.

## Notes from upstream (prompt 2 appends here)

**From prompt 2 (Fable QA gate, 2026-08-13). Verdict: ⭐ BUILD — with
MUST-FIXes, every one already applied in place in `90_DERIVATION.md`
(strike-and-supersede, tagged `[QA 2026-08-13]`). You build from the corrected
doc; nothing below is left for you to re-derive, but every MUST-FIX carries a
spec obligation you must honor.** Staleness at my run: fix-pack `8908367`,
opt-pack `a90d128`, TestKit `62f03da`, all clean (a parallel session's
uncommitted owner-decision edits — opt-in remote now PUBLIC — landed mid-run
and ride this commit; they do not touch the derivation's substance).

### The membership diff: ZERO differences, by a genuinely different route

Independent sweep, different axes than prompt 1's: `SetGlobal(` call-site
inventory + direct `_G` writes (catches the F87 latch paths) · whole-`Src`
regex classification of all 17 replaced names (252 occurrences, exactly ONE
non-call use = `TerraformingDisasters.lua:313`, E1's route — **§1.4 re-confirmed
independently**, including the `PersistableGlobals` whitelist mechanism read
at `persist.lua:119-143`) · literal persisted-name token sweep · own-thread /
`rawset` / `= function` / notification-closure / label-modifier axes · the
instrument re-run on the preserved 80-row list (verdict pattern reproduced,
same four false positives, Colonist again absent from the Idle summary line).
Chases that settled to no-finding: `Fix_RainsDeadlock:195` (entry value is
vanilla's `RainsDisasterLoop`, never replaced), `Opt_NoHomeless:52`
(comment-only mention), the opt pack's `ProcessToggle` rawsets (UI windows,
§2c's class), `Fix_MilestoneCrash:41`'s popup (vanilla-valued params, vanilla
id). §1.3's reconciliation verified at source 4-for-4 (DestroySilent decider
at `Train.lua:183-184` + `Demolishable.lua:91/104`; MirrorSphere's yield is in
the nested closure at `MirrorSphere.lua:836`; RCTransport dispatch body;
both recovered `Colonist:Idle` yields — second cite corrected to `:1796`).

### MUST-FIXes applied — and what each obliges YOU to do

1. **D2 (and D1) — the GameVar rows were wrongly treated as cleaner-visible.**
   Mod-registered GameVars are DROPPED on any load without the registering mod
   and never re-saved (`persist.lua:136-142`, verified at source). D2's REMOVE
   was unexecutable; its "least-certain placement" dissolves. **Spec: the
   cleaner's list must NOT contain D1 or D2, and the artifact must NEVER
   register a `GameVar` to reach a value (that re-persists the name — 6d).**
2. **§8.3 "no thread surgery whatsoever" — struck.** Doubt 4 is SUSTAINED
   (captured frames unreachable, §2a inert-accepted wholesale), but the
   artifact's population includes PRE-REWRITE-LINEAGE saves the current pack
   never touched (uninstalled before Tier 1/2) — the D13 entry's own expected
   leftover classes. **Spec: keep TWO one-shot bounded heals, vanilla bodies
   only: `Meteors` restart only-if-dead/foreign (cost: one 35-115 h re-roll,
   stated to the player) and the rains stale-ACTIVE/dead-loop heal via
   `FinishRainProcedure` / recreate-onto-vanilla-`RainsDisasterLoop` (the
   pack's proven C34 recipe; cost: one rain re-roll). Never repeated;
   skip-and-report on ambiguity. Your Job 1 already demands the per-thread
   cost lines.** Checklist item 17 got an owner-facing QA update saying
   "smaller, not zero"; the (c) recommendation is unchanged.
3. **Count corrections inside the draft** (the project's own defect class):
   §4.1's summary arithmetic ("Removed: 5", "14−5+1") contradicted its own
   table — now 14−4=10, +E3+E12=12; RT thread count 2→**3**; "14 distinct
   persisted names"→**16** (15 rows, F35 family as one, D15 as two).
4. **Cite corrections:** D9's second cite `:173`→`:201` (write) + `:209`
   (guard); `Colonist:Idle` `:1795`→`:1796`; D11 `:339` and D12 `:105`
   verified CORRECT (variable-keyed writes my literal grep couldn't see).
5. **Report dialog placement (spec requirement added to §8.3):** the
   `WaitMessage` report MUST ride a real-time thread (00_Core:498's pattern);
   the clean pass stays synchronous. A yield on the load-path GT frame would
   be the exact shape the artifact exists to avoid.

### Rulings you can lean on

* **E7 defanged** (still INFERRED, no longer load-bearing): the own-thread
  axis is exhaustive — exactly 6 GT creations in both trees, E7's the only
  yield-free body — so neither answer to the created-never-run question
  changes any list or disposition; the 6f gate covers its worst case. An
  optional prompt-4 probe leg is sketched in §6 doubt 1.
* **Doubt 5 settled** (option tables are not save state — mechanism verified).
* **Doubt 2 extended** (zero `Sleep`/`Wait*` tokens anywhere in
  `UIStatUpdate` :2932-3133); still conditional on indirect helpers, still
  disclosed, not a gate item.
* **§4.3's doc-correction list verified complete** by an independent sweep
  (all 9 files confirmed; no unlisted file; TestKit + opt-pack docs clean).
* **KEEP/REMOVE ran per-name, both directions**: D15's removal path is the
  module's own base-position call (`SetLabelModifier(label, id, nil)`,
  labels "Drone"/"Consts", ids at `:64-65`); D5/D6/D7 absence semantics
  verified at `:81-83`/`:65-70`/`:97`; D10's re-add guard at
  `90_SaveSanitizer:69-76` confirms a pattern sweep would re-break F35.
  6f routings verified by my own reads (gates present only in StormWedge,
  `:145`/`:156`; E5/E6/E7 ungated; the stale `:138-141` comment confirmed —
  EF-023's closing claim is FALSE and rides your Job 3).

### Observation, not a MUST-FIX

E9/E10 (and the "frame" wording generally): both Idle wrappers end in strict
tail calls with yield-free pre-work; under proper-tail-call semantics those
frames are elided before vanilla's Sleep, so E9/E10 are likely over-included.
Kept deliberately — same basis as the historical counts, no disposition
changes either way, and un-measurable without a game. Do not cite them as
capture-proven.

### What I did NOT get to (named residue for prompt 5)

* **No game launch** — E7 unmeasured (optional probe sketched); the
  tail-call elision observation unmeasured.
* **D10 still UNSAMPLED** — ROUTED to prompt 4: the damaged-fixture leg must
  plant/manufacture an F35-affected witness and read the modifier back
  (absent ≠ refuted; the house rule requires the condition SAMPLED).
* **E12's indirect-helper yield audit** — token scan only; the conditional
  tag stands.
* The parallel session's owner-decision edits (checklist item 15, STATE's
  remote line) were in the tree uncommitted at my close; they ride my commit
  unreviewed beyond a read of their diff.

**Addendum (same session, 2026-08-13, post-verdict decision batch):** the
owner answered everything you were gated on and more — all recorded on the
checklist. For you specifically: **Q-A = (c)** (launch dependency REAFFIRMED
after an explicit challenge; build ≠ publish — store publication is a
release-time call) · **Q-B = mod-shaped CONFIRMED** · **item 19 = GO** (the
inserted `02b_OPUS_GATES.md` runs before you; read its outbox above yours) ·
**naming RATIFIED as proposed** (display "Save Rescue", mod id
`SMR_CommunitySaveRescue`, log tag `[CommunitySaveRescue]`) · ⭐ **the owner
pre-created the artifact's PUBLIC remote themselves:
`github.com/catt144/SMR-CommunitySaveRescue` (empty)** — scaffold locally,
set that as `origin`, push; align the local folder name to the remote
(`C:\Dev\SMR-CommunitySaveRescue`) rather than the proposal's shorter
`SMR-SaveRescue`. Also decided the same day, opt-in side (not yours to act
on, but your doc sweeps will see it): display name = "Community Fix Pack:
Opt-In Modules" (swept, opt-pack `e17586b`), default-OFF ratified.

### From prompt 2b (Opus, the three orphan gates — 2026-08-13, CONSUMED)

Staleness at my run: fix-pack `0a21da1`, opt-pack `e17586b`, TestKit `62f03da`,
all three trees clean. Nothing in either `Code/` had changed since this prompt
was authored (the five commits after `ea81faa` are docs only), so the line
numbers it gave were still live. Game closed throughout — **every claim below
is source/parse tier; nothing was launched or measured.**

#### Job 1 — the three §3a gates, inserted (final line numbers)

| module | gate (final line) | placement | §3a reset clause |
|---|---|---|---|
| `Code/Fix_CrystalMysteryHang.lua` | **`:78`** | first statement after `Sleep(const.HourDuration)` (`:74`), ahead of the generation/mystery check | vacuous — the loop body sets no vanilla state, so a bare `return` complies |
| `Code/Fix_ExtenderFlapChurn.lua` | **`:96`** | first statement after `Sleep(DEBOUNCE)` (`:91`), ahead of `pending[hub] = nil` and the hub rebuild | vacuous — nothing vanilla is touched before it |
| `Code/Fix_TrackConnectorPingPong.lua` | **`:179`** | the created closure's first statement (`CreateGameTimeThread(function(station)` at `:174`) | vacuous |

All three are the identical one-liner `if not SMRFixPack then return end`, form
copied from the proven precedent `Fix_MeteorStormWedge` — whose gate lines are
now **`:154` (first statement) and `:165` (re-arm after the `Sleep`)**, having
moved from `:145`/`:156` because my Job-2 comment rewrite in that file is
longer than what it replaced. Every insertion comment cites the precedent by
file and those FINAL line numbers, and every header citation in the four files
was re-read and corrected after the edits (closure ranges: CrystalMysteryHang
`:71-85`, ExtenderFlapChurn `:90-102`, TrackConnectorPingPong `:174-183`).

**Installed-path claim, STRUCTURAL and by eye — not a measurement:** the pack
creates the real global `SMRFixPack` before any of these bodies can run, so on
the installed path all three gates evaluate true and the three modules behave
byte-identically. Reading a nil global is safe; the gate is false only when the
mod is gone. No behaviour change, no new persisted state, no interval change.

**No probe reads a touched line** (checked, not assumed): the only probes naming
these modules are `20_Probes_Wave2.lua:720` (asserts a `CrystalFlyAway` handler
is registered — never enters the repeater closure) and `40_Probes_Wave4.lua:146`
(drives `CreateConnectorElements` directly, and its reclaim leg at `:224-250`
**stubs `CreateGameTimeThread` to capture the station argument without running
the closure** — so the new gate line is never executed by it). TestKit tree
untouched and clean; the queued `FactionFundingCheck` PASS→SKIP repair is still
queued (not mine).

#### Job 2 — disclosure

1. **Three module headers** now carry a `Save footprint / §3a orphan gate`
   paragraph: what the GT thread body is (with its line range), that a save
   captures blocked GT threads BY VALUE per `EF-023`, what an orphan does
   (E5: hourly `CrystalFlyAway` to a frozen 10-sol deadline · E6: one hub
   disconnect/reconnect cycle, then ends · E7: one connector rebuild, and only
   if a created-but-never-run thread is captured at all), that the body now
   gates, and that the module persists no name/GameVar/field of its own. E7's
   paragraph states its INFERRED status and `EF-029` window explicitly, and
   says the gate makes that open question moot rather than load-bearing.
2. **`Fix_MeteorStormWedge` `:138-141`** (the comment adjudication §3.4 ordered
   in Tier 1 and only half-did) is rewritten: the "persist-safe by name … not
   persisted (F06/F77 precedent)" model is struck, replaced by the by-value
   rule, and the zero-upvalue discipline is now explained by its INVERTED
   reason (global lookups make an orphan die loudly). It now agrees with the
   header 80 lines above instead of contradicting it.
3. **`Fix_MeteorStormWedge` header `:65`** no longer reads as a completeness
   claim: it says this was the one GATED mod-owned GT thread, names E5/E6/E7 as
   the three the D13 derivation found ungated, and records that all three
   gained this gate form on 2026-08-13.

#### ⚠️ Prompt 1's item-2 finding was INCOMPLETE — two more files carried the model

`Fix_MeteorStormWedge:138-141` was not the only surviving statement of the
disproven by-name persistence belief in `Code/`. Also found and corrected in
this pass, as part of Job 2 item 1:

* **`Fix_ExtenderFlapChurn`, the whole "Savegame note" (old `:35-40`)** —
  *"the debounce thread is a mod game-time thread — those are **NOT persisted
  across save/load** (F06 precedent: 'the thread from before the save is
  gone')"*. That is the disproven model stated flatly, and it was the module's
  entire save-footprint disclosure. Replaced by the corrected paragraph, marked
  `⚠️ REWRITTEN 2026-08-13`.
* **`Fix_CrystalMysteryHang`, the LoadGame inline comment (old `:79`)** —
  *"the thread from before the save is gone"*, the F06 sentence the Extender
  note was quoting. Corrected in place (comment only; the `stop_repeater()`
  call is unchanged).

**⇒ EF-023 comment-state note, for your Job 3.** After this commit, EF-023's
closing line *"nothing in `Code/` states it any more"* is **TRUE AGAIN** — I
swept `Code/` for the belief and corrected all three surviving sites. So
**annotate it, do not re-falsify it**: the accurate correction is that the line
was FALSE from the Tier-1 rewrite until 2026-08-13, that its "two shipped file
headers" count was wrong (four files carried it: `Fix_MeteorFrequency` and
`Fix_RainsDeadlock`, fixed in Tier 1, plus `Fix_MeteorStormWedge` and
`Fix_ExtenderFlapChurn`, fixed here, and a fifth inline site in
`Fix_CrystalMysteryHang`), and that it is true again as of the fix-pack commit
that carries this outbox (2026-08-13). STATE.md's warning line is flipped to
match.

#### ⚠️ Owed — one live-path observation I disclosed but did NOT repair

Found while writing E5's disclosure; **SOURCE-derived, unmeasured**, and left
alone because my scope fence was gate insertion plus comments only. Recorded in
the `Fix_CrystalMysteryHang` header under "Disclosed, NOT repaired here":

> Persist restores a thread's upvalues **by value**, so a repeater restored with
> a save holds its own copies of `repeater_gen` / `my_gen`, while the LoadGame
> handler's `stop_repeater()` bumps the **freshly loaded chunk's** locals. The
> two lineages cannot see each other. With the pack INSTALLED, loading a save
> taken during an active Crystals mystery therefore leaves the restored repeater
> running beside the one LoadGame starts — duplicate hourly `CrystalFlyAway`
> broadcasts, one extra lineage per save/load cycle inside the mystery, each
> still self-limited by its own mystery check and 10-sol deadline.

Inert as far as I can tell (the message has exactly one consumer, a `WaitMsg`
that wants it), which is why I did not file it as a defect on my own authority —
but it is a live-path effect of the corrected persistence model, not an orphan
question, and it belongs to somebody. **Route:** yours to file or to hand to the
owner (a bug entry changes the BUGS row counts, which my close was told to leave
unchanged). It is also the cheapest possible witness for the model itself.

#### Optional leg for prompt 4 (offered, nothing gates on it)

The three gates become measurable in the junction-pull legs at near-zero extra
cost: with a save taken while one of these bodies is asleep, pull the junction
(EF-055 → off-state 4) and load back — a gated body returns silently at its
first wake, and the E5 case is directly observable as `CrystalFlyAway` traffic
stopping rather than continuing for 10 sols. The same leg would settle §6
doubt 1 for E7 if a yield-free thread can be caught in its creation window.

#### Close state

* Parse sweep: **77/77 Lua files OK, 0 FAIL** (`luaparser` over `Code/**` + root).
* `python tools/doccheck.py`: **GREEN**.
* `--emit-counts`: **74 modules / 75 `Code/*.lua` / 88 probes**, index rows
  102 F + 12 D + 46 C — unchanged, as expected: no module, file, or probe added.
  ⛔ This is a STRUCTURAL assertion that the suite baseline is untouched (no
  probe edited, counts re-emitted), **not** a measurement of the baseline.
* **Not claimed:** orphan behaviour verified (nothing launched); baseline
  measured; anything about how these bodies behave in a real save.

⚠️ **Tree note (read before you `git add`).** A parallel `public-docs` session
was editing this repo while I ran. I committed only my seven paths and left
theirs (`.gitignore`, `agent/prompts/public-docs/*`, untracked `.github/` and
`public-site/`) — **except one I could not separate:** their new
**checklist item 21** (GitHub Pages ruling + the "which repo hosts the site"
question) was sitting unstaged in `PLAYTEST_CHECKLIST.md`, the same file my
item-19 close-out edits, so it rode my commit `91fc5d0` under a message that
does not describe it. Nothing of theirs was altered or lost; their next commit
simply finds that block already in — which is what happened: they committed
`d2970cf` minutes later, and the tree is theirs-and-mine, both pushed. (Item 21
says "a working scaffold is committed at `public-site/`"; that was untrue at
`91fc5d0`, where the folder was still untracked, and became true at `d2970cf`.)
