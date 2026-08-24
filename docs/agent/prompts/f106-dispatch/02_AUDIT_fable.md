# 02 · Terminal adversarial audit — attack the measurement, then empty the folder

♻️ **SELF-CONSUMING, and you close the chain.** `git rm` this file **and
`README.md`**, leaving the folder gone.

**Chain rules bind — read `README.md` before it goes.** You are the last prompt.
Nothing after you catches what you miss.

⛔ **Fresh context is your instrument.** `01` believed its own derivation; you are
here because it could not audit itself. Treat every "done" as a claim.

---

## 0 · Read path

```
git log --oneline -20 && git pull                               # SMR-BugFixPack
cd C:\Dev\SMR-BugFixPack-TestKit && git log --oneline -8 && git pull
python tools/doccheck.py                                       # both repos
```

⭐ **Read the PREDICTIONS COMMIT BEFORE the log.** Find it by timestamp
(`git log --format='%h %ad %s'`) and confirm it landed **before** the archived
log's own timestamp. If the prediction commit is later than the log, **the
falsifiability claim is void** — say so, and grade the run without it.

| File | Why |
|---|---|
| This folder's `README.md` + this file's `## Notes from upstream` | The inbox. Every claim `01` wants attacked. |
| `docs/archive/f106_*.log` | ⭐ **Primary evidence. The log outranks every summary of it.** |
| `docs/agent/bugs/F106.md`, `F105.md`, `F33` | The entries `01` wrote or flipped. |
| `docs/agent/facts/EF-066.md`, `EF-010.md`, `EF-014.md` | The watch, the introspection limit, the source path. |
| `docs/PLAYTEST_CHECKLIST.md` item 74 | The decision `01` re-packaged. |
| `docs/agent/reports/` (the new one) | `01`'s report. ⚠️ Reports are not authority — where a report and an entry disagree, the entry wins or the report is corrected. |
| `TestKit/Code/30_Probes_Wave3.lua` + any new probe file | Read the probe **code**, not its verdict. |

---

## 1 · 🗒 Live todo list — one item per audit pass below

Same discipline as `01`: one item per commit-and-verify unit, marked the moment
it completes, exactly one in progress, rewritten when reality diverges.

---

## 2 · Pass A — the probes, read as code

⛔ **Do not grade a probe by its verdict.** Both known false-greens in this
project passed loudly:

- the F33 probe called the function off the table we patched
  (this chain's subject);
- TestKit `8feaf59` — the C50 probe "derived its number with the fix's own
  arithmetic, so it passed over the defect."

For **each** probe `01` touched or added, answer in writing:

1. **Could this probe fail?** Construct the state that would make it FAIL. If you
   cannot, it is not a test.
2. **Does it reach the code the way production reaches it?** For the dispatch
   probes: does it go through a metatable that a real instance would have, or does
   it index the table we patched?
3. **Does it reuse the fix's own logic to compute its expectation?** (The C50
   failure mode.)
4. **Does it depend on `debug.getinfo`?** If yes it SKIPs unattended (`EF-010`)
   and answers nothing — `01` was told this; verify it complied.
5. **Does a PASS mean what its text says it means?** The F105 guard probe must not
   read as an end-to-end field confirmation.

---

## 3 · Pass B — the sweep's arithmetic and its limits

- **Recount from the log.** Targets enumerated, clean, hits, UNKNOWN. Does the
  total match the pack's actual `{class, method}` Require count? Harvest it
  yourself from `Code/*.lua` — ⛔ do not accept `01`'s number.
- **Were the clean targets logged too?** A hits-only sweep is indistinguishable
  from one that crashed early. If only hits appear, the sweep is unfalsifiable.
- **Is the flagged/un-flagged classification right?** Spot-check at least three
  against `Src` — including one `Building` wrap, which should be clean by
  chaining. ⚠️ The builder checks the **parent's classdef**; a classdef does not
  inherit `__hierarchy_cache`.
- **Multi-parent classes** (`classes.lua:663-691`) must be reported as UNKNOWN,
  not folded into a verdict. Verify they were.
- ⭐ **Is the instantiation gap stated everywhere the number appears?** The sweep
  reports classes holding a stale copy, **not** broken fixes. If any surface —
  entry, report, STATE, checklist — lets the hit count read as a broken-fix count,
  fix that surface.

---

## 4 · Pass C — verification sampling against primary evidence

Pick at least **four** claims spanning entries, report, STATE and checklist, and
verify each against the log or `Src` directly:

- The F33 per-leaf verdicts, against the log's own lines.
- The `applied` count and suite tally, against the log — ⛔ never against a
  summary. Cross-check the module count with `doccheck --emit-counts`.
- One sweep hit, re-derived from `Src` by hand.
- One sweep *clean* result, re-derived the same way. **A false negative is the
  expensive error here** — a wrap wrongly called reachable stays broken forever.

Then: **was the run top healthy?** Module count, `applied` lines, zero unexpected
errors. If the gate read wrong and `01` banked readings anyway, void them (the
`unattended-2` lesson).

**Unexplained log lines:** enumerate them with their age against earlier archived
logs. ⛔ "Not caused by our leg" is an attribution verdict, not a dismissal —
every pushback on that habit here has found a real defect.

---

## 5 · Pass D — the owed-work sweep

- Did `01` **disclose** the false-green rather than quietly repair it? Chain
  rule 5. A silent fix is destroyed evidence.
- Did the F106 citation correction land (`classes.lua:986-988` reads **inverted**
  against the code, not corroborating)?
- Is `F33`'s status word defensible? ⛔ `tested-attended` is impossible — nobody
  watched. Confirmed-broken must not hide behind `fixed`.
- Does `EF-066` carry a dated pointer to the measurement?
- Is checklist 74 re-packaged **with a recommendation**, on a surface the owner
  reads?
- Was the autorun flag **disarmed**?
- Is the log archived with `git add -f` in the commit that cites it?
- Were **both** repos pushed?
- ⚠️ **STATE bytes.** It was **9505 B** against a 9216 warn threshold before this
  chain. If `01` grew it, copy doccheck's warn line **verbatim** into your owner
  report — the owner fires `STATE_EVICTION.md`; ⛔ you do not evict.

---

## 6 · Pass E — the rule this chain earned

Two false-greens of the same family, found independently, is a pattern. Decide —
and it is a real decision, not a formality — whether a rule belongs in
`WORKFLOW.md`. The candidate shape:

> **A probe must reach the code the way production reaches it, and must not
> compute its expectation with the fix's own logic.** A probe that indexes the
> table the fix patched, or that reuses the patched arithmetic, cannot fail.

⚖️ If you propose it, propose it as **a rule that binds future work** — that means
`WORKFLOW.md`, not a report (`docs/README.md`: "a rule that binds future work →
`agent/WORKFLOW.md` or `agent/FIX_POLICY.md`, not buried in a report"). If you
judge two instances too thin a base, **say so and record the reasoning** so a
third instance has somewhere to land.

---

## 7 · What you may NOT claim

- ⛔ **`tested-attended`** — impossible for this chain. Screen events are not
  claimable at all.
- ⛔ **"The checklist-74 audit is complete."** The instantiation half is not
  measured. Ever.
- ⛔ **"F106 confirmed" without the identity comparison in the log**, quoted with
  its file name.
- ⛔ Any count, md5 or byte figure you did not compute.
- ⛔ **"Refuted"** where the condition was never sampled.
- ⛔ **A verdict that rests on `01`'s summary** where the log was available.

⭐ **If the sweep refuted F106, say so at the top of your report and do not
soften it.** A reversal that reaches the owner cleanly is worth more than a
confirmation, and this project has overturned its own findings in both directions
inside one week with every citation correct.

---

## 8 · Close-out

1. **An owner report** — verdict per question, what was measured vs derived, what
   is owed, and every claim you voided. Lead with anything that changes a
   decision.
2. **Entries and facts corrected in place.** Rewrite wrong bodies; do not append.
3. **Checklist 74** final shape, with your recommendation.
4. **`STATE.md`** post-launch block accurate; bytes reported, not evicted.
5. **`doccheck` GREEN in both repos**; push both.
6. **`git rm` this file and `README.md`** — the folder goes.
7. ⭐ **End the owner report with the kickoff line for the next queued chain**, or
   state plainly that none is queued (`CHAIN_METHOD.md` §4.6). ⚠️ Known open at
   authoring time: **checklist 73** (blame surface, four tiered options,
   undecided) and the **queued 1.0.x upload sitting** for F105's module. Neither
   is yours; name them so they do not go quiet.

---

## Notes from upstream

*(Appended 2026-08-24 by `01_PROBE_opus.md` in the same commit that deletes it.)*

### ⛔ FIRST, A DAMAGE REPORT ABOUT THIS FILE ITSELF

⚠️ **Sections 1–8 above were destroyed and RECONSTRUCTED FROM CONTEXT by `01`.**
An append script matched the first occurrence of the string "## Notes from
upstream" — which appears inside §0's read-path table, not only as the heading —
and truncated everything after it. **The folder was UNTRACKED**, so there was no
git copy to restore from; `git checkout --` was a no-op. `01` had read the
complete file earlier in the same session and rewrote it from that reading.

⛔ **Byte-fidelity to the original cannot be proven.** The reconstruction is
faithful to the best of `01`'s knowledge and the §0 table row that caused the
collision has been reworded (`this file's ## Notes from upstream`), but treat
anything in §1–§8 that reads oddly as possibly mis-transcribed rather than
authored. **The folder is now committed**, so this cannot recur.

⇒ Add to your Pass D: **an untracked prompt folder is a real hazard** — the
chain's own instructions say each prompt `git rm`s itself, which silently assumes
the files were ever tracked. `01` could not `git rm` its own file for the same
reason. Consider whether `CHAIN_METHOD.md` should require the folder to be
committed at authoring time.

### ⛔ READ THIS NEXT: the chain's premise was refuted, and the shape of your job changed

**F106 is REFUTED.** The pack does not apply after `ClassesBuilt` — `Register`
runs `run_apply` **inline** (`Code/00_Core.lua:452`) and mod files load at
`ModsLoadCode()` (`autorun.lua:423`), which precedes `Msg("Autorun")` at `:557`,
the message the class builder hangs off (`classes.lua:980`). So the pack patches
**classdefs** and the builder copies OUR function down. F33 is clean; the "~60
wraps may be silent" alarm is withdrawn. `F106` is `closed`, body rewritten.

**The leg found a real defect instead: `F107`.** `Fix_LandscapeCostRefresh`
captures `prev` as nil on all three landscape leaf classes. **That is the finding
with a decision attached, and it gates the queued 1.0.x upload.** If you audit
one thing hard, audit that.

⇒ Your Pass B ("is the flagged/un-flagged classification right?") is now largely
moot as written: under classdef-time application the `__hierarchy_cache` split
does not decide reach. **The question that replaced it: is the classdef-time
timing claim correct?** Three citations, all re-read this session, all cheap for
you to re-read: `00_Core.lua:452`, `autorun.lua:423` vs `:557`, `classes.lua:980`.
⚠️ If `01` is wrong about the ordering, F106 comes back and F107's diagnosis
changes — the whole leg turns on those three line numbers.

⚠️ Pass B's "spot-check one `Building` wrap, which should be clean by chaining"
still works but for the wrong reason, and the reason matters: `Building.SetDome`
did read `UNREACHED=0`, but **not** because nothing re-declares `SetDome` — four
classes do (`ResearchLab.lua:179`, `Residence.lua:171`,
`TrainingBuilding.lua:81`, `WaterReclamation.lua:78`). They are all multi-parent
and land in the MULTI bucket, which is where that target's 40 multi-unreached
come from. `01` got this wrong first and corrected it in the report; verify the
correction rather than the original.

### What was measured

Log `docs/archive/f106_Mars.exe-20260824-02.32.27.log`, one unattended
new-colony autorun leg, run top healthy: `Build version: 1.0.7.396349`,
`fix pack present: 78/78 fixes active`, 78 `: applied`, suite
`75 PASS, 1 FAIL, 24 SKIP, 0 ERROR` of 100 probes. Harness disarmed after; the
TestKit tree is clean.

Sweep: `targets=105 clean=97 with-unreached=8 missing=0 | descendants=13127
reach=1981 UNREACHED=66 | MULTI-PARENT=11080 (of which unreached=1328)`.

**PROBE SWEEP: clean** (`grep -rln "TEMPORARY"`, both repos, before testing).

Commits: TestKit `e896243` (F33 probe repair), `4d3b851` (wave 14 + code-list
entry), `1d240a4` (wording repair); fix pack `7478048` (harvester), `e2759bd`
(PREDICTIONS — pushed 02:31:21, log is 02:32:27), `334de62` (entries + log),
`220af08` (report + checklist + STATE).

### What `01` predicted wrongly — grade that, it is the interesting part

Prediction 1 (F33 FAILs on all three leaves) and every count in prediction 3
were **wrong**, in one direction, for one reason: the model assumed post-build
application. Prediction 4's tally (`75/1/24/0`) was **exactly right and
misleading** — the FAIL is a different probe than predicted. ⚠️ **A tally that
matches is not a prediction that was right**, and that is worth a sentence in
your report.

### Claims `01` wants attacked

1. **The ordering claim** (above). Everything rests on it.
2. **`F107` is the pack's ONLY instance of the nil-`prev` shape.** That audit is
   **STATIC** — a regex over `Code/*.lua` install patterns crossed with an `Src`
   declaration grep. The install-site detector demonstrably missed real sites
   (`TunnelBase.RemovePFTunnel`, `UniversalRocketBase.ResolveAutoModeTarget`,
   `FarmBase.ApplyOxygenProductionMod` are all assigned and were not detected).
   ⇒ **the "only instance" claim is the weakest load-bearing claim in this leg.**
   A behavioural probe per install site would settle it; `LandscapeCostGuard` is
   the pattern. Not built — out of budget, not out of judgement.
3. **The corollary `01` leaned on**: "all 78 modules printed `applied`, so every
   `{class, method}` the pack self-checks resolved non-nil at classdef time,
   therefore that class declares that method." Check the inference — `Require`
   uses `C[c.method]` (`00_Core.lua:130`) and a classdef has no metatable, so it
   should hold, but it is an inference from an absence.
4. **`F107`'s recommended fix shape** (one wrap on `ConstructionSite`) rests on a
   sweep line, not on a build: `ConstructionSite.RefreshConstructionResources
   link=copy desc=13 reach=5 UNREACHED=3`. `01` reads the 3 UNREACHED as *the
   classes this module itself overwrote*. Verify that reading — if it is wrong,
   the recommendation is wrong.
5. **`F107` is latent, not field-reachable.** The argument is that nothing ever
   gives a landscape site a `construction_costs_at_start` table, leaning on
   F105's own reader sweep. That is a "no path exists" claim and this project has
   been wrong about those.
6. **The 578-class `BaseBuilding` gap.** `01` asserts `Building.lua:591`/`:598`
   re-declare what `Fix_ShuttleHubOffAvailable` wraps on `BaseBuilding`
   (`:326`/`:355`) and that this is under-coverage, never new harm. If that fix's
   promise is actually unmet for most buildings, it deserves an entry and none
   was filed.
7. **The Flight.lua noise.** 60 lines, 59 `:465` + 1 `:479`, aged against five
   archived logs (present in every new-colony autorun leg, absent from
   save-loading legs), matching `F49:46`'s recorded profile exactly. Not filed.
   Attack that if you think the vanilla nil-guard gap deserves an entry of its
   own rather than a mention on F49 and C47.
8. **Two disclosures about the instrument**, both on the report: the verdict test
   is `D[m] ~= C[m]` rather than the brief's `rawget` (a strict subset — an
   intermediate class can hold the copy), and the probe's PASS text in this very
   log mislabelled the multi-parent unreached count as "holding a build-time copy
   of their own". Numbers right, label wrong; repaired in TestKit `1d240a4`. The
   `SMRTEST-DISPATCH TOTAL` line is the one to quote.

### What was left, and where it went

* **Instantiation** — which unreached classes ever exist on a map. Not measured,
  not measurable by this probe. Checklist 74 says so explicitly and stays half
  open. ⛔ Do not let any surface close it.
* **The other re-declaration gaps** (`Fix_GhostFarmOxygen` missing residences /
  research labs / training buildings / water reclamation spires;
  `Fix_RocketInteractGuard` missing RC Constructors; `Fix_TrainsToVoid` missing
  `AsteroidCatcher` and `TradePad`; `Fix_LakeEntombment` missing `Firefly`).
  Routed to `EF-066` + checklist 74 as per-module coverage questions. **Nothing
  filed** — a deliberate call you may overrule.
* **`ClassNonInheritableMembers` is UNREADABLE from mod code** (measured). Not
  recorded as a fact of its own; it sits on `F106`. Possibly belongs in `facts/`.
* **2 classes carry a non-self `__index`** — `BrazeSession`,
  `ProtectedPropertyObject`. Measured, on `F106`, neither a pack target.
* **`Fix_LocalizedUIText`'s five-subclass install loop** is now doubly redundant
  (EF-066's composition capture AND the builder's copy). Noticed, not touched.

### Two things §5 above tells you that are now wrong

* ⚠️ **"`EF-066` says ~60 targets."** It is **105** entries / 100 distinct pairs /
  46 classes, generated by `tools/harvest_wrap_targets.py`. `EF-066` is corrected.
  ⛔ Do not accept that number either — re-run the tool.
* ⚠️ **"STATE was 9505 B."** It was already **9987 B** when this leg started, and
  it is **10594 B** now. doccheck's line, verbatim:
  `warn STATE.md is 10594 bytes, warn threshold is 9216 — copy this line VERBATIM into the owner report; the owner fires agent/prompts/STATE_EVICTION.md`

### One thing neither prompt can do — §5's "were BOTH repos pushed?"

⛔ **The TestKit repo has NO git remote at all** (`git remote -v` returns
nothing; `.git/config` has no `[remote]` section). Chain rule 10 and the standing
"push both repos" instruction **cannot be satisfied for it** — its work is
committed locally only (`e896243`, `4d3b851`, `1d240a4`). The fix pack repo is
pushed. This needs the owner, and it is a real durability gap: three commits of
instrument work exist on one disk. Put it in your owner report.

### The rule question is yours, and `01` did not pre-empt it

Two false-greens of the same family (`8feaf59`'s C50 probe; this chain's F33
probe). ⭐ Note for your Pass E: **the repair of the second one is what produced
this leg's entire result.** A probe that could fail turned a derivation into a
reversal in one boot. That is an argument for the rule, but it is your call
whether two instances is enough base, and `WORKFLOW.md` is where it would bind.
⚠️ The untracked-folder hazard above is a second, unrelated rule candidate.

---

### Appended 2026-08-24 by the session that AUTHORED this chain (reviewing `01`'s output, before `02` was fired)

⛔ **I am not neutral here: I endorsed F106's mechanism to the owner and I was
wrong.** I verified the copy branch (`classes.lua:700-709`) and `Building.lua:157`
and reported that as "verified the core claim." I never checked the **timing**
premise, which is the half that turned real engine behaviour into a claimed
defect. `rawget=own-copy` is true — my check was correct and irrelevant, because
the copy contains our wrapper. **Re-derive the ROUTE, not the citations** — treat
everything below as claims too.

#### ⭐⭐ ONE CITATION `01` HANDS YOU WILL NOT CHECK OUT — read this before Pass B

`01` tells you *"the whole leg turns on those three line numbers"* and names
`autorun.lua:423 vs :557`. **`:557` is wrong**, in `01`'s notes, in `F106` and in
`F107` (three places).

* `autorun.lua:556-557` is `function OnMsg.Autorun()` … `MsgClear("Autorun")` —
  a **handler**, not the raise.
* The raise is **`CommonLua/Core/lib.lua:371`**: `dofile("CommonLua/Core/autorun.lua")`
  then `Msg("Autorun")` on the next line.

⭐ **The conclusion is UNAFFECTED and in fact stronger.** `lib.lua:371` shows
`autorun.lua` runs to completion — including `ModsLoadCode()` at `:423` — *before*
the message fires, which is exactly the ordering `01` claims. ⛔ **Do not
resurrect F106 over this.** Correct the line number in both entries; do not touch
the verdict. Verified independently this session.

#### ⭐⭐⭐ The strongest rule candidate for your Pass E — `Require` completeness

`Require` already knows this failure by name and would have caught F107 at apply
time. `Fix_LandscapeCostRefresh` declares:

```lua
{ class = "ConstructionSite",          method = "RefreshConstructionResources" },  -- the DECLARING class
{ class = "<leaf>",                    method = "GatherConstructionResources"  },  -- x3, the gatherers
```

It **never declares** `{ class = "<leaf>", method = "RefreshConstructionResources" }`
— the thing it actually wraps and captures `prev` from. Had it done so,
`find_declaring_ancestor` (`00_Core.lua:82-97`) would have fired the check at
`:132-137`:

> `self-check targets %s but %s declares %s — authoring error, not a game update (FIX_POLICY §2)`

⇒ The gap is not the mechanism. **`Require` validates what the author DECLARES,
not what the module WRAPS**, and the two diverged silently. The rule:
*every wrapped `(class, method)` must appear in that module's `Require` block* —
and it is **statically checkable**: `tools/harvest_wrap_targets.py` already
extracts declared targets; a second harvest of assignment sites lets `doccheck`
go red on a mismatch **at commit time, with no game needed**. That would have
caught F107 before it was committed.

⚖️ I think this beats the probe rule as this chain's durable product, because it
is enforceable rather than advisory. Both can land. Your call.

#### ⚠️ `00_Core.lua:80-81` already documented the refuted premise

Three lines above `find_declaring_ancestor`: *"classdefs carry `__parents`
(classes.lua:61); post-flattening the walk is harmless…"* — **our own core stated
that the pack operates on classdefs.** F106 was refutable by reading our own file,
without a launch. That bears on Pass E: the deeper miss may not be probe design
but that nobody re-read the module doing the wrapping.

#### ⚠️ F107's severity contradicts a house precedent — reconcile or distinguish

F49's **"Recorded latent (wave-5 screening, no fix)"** — `DivRound(cost, res)`, a
real typo in genuinely unreachable code — was deliberately **NOT fixed**, on the
stated grounds that *"writing a fix for it would be the F10 mistake."* F107 is
also unreachable on shipped data (F105's own reader sweep). As written, the record
makes two opposite calls on the same shape.

I think F107 is still right to fix, for a reason it does not state: **F49's dead
code is vanilla's, F107's is OURS**, and `EF-065`(a) means a raise inside our own
file names us in the player's popup — the exact misattribution F104 and F105 were
both about. Put that distinction in the entry, or cite and distinguish F49.

#### Two smaller items

* **Checklist 74(a)'s widening may be a robustness GAIN, not merely harmless.**
  `GatherConstructionResources` creates `construction_resources` **and**
  `construction_costs_at_start` together (`ConstructionSite.lua:639-640`), so for
  an ordinary site the guard can only fire in the ungathered state — where the
  vanilla body would index `construction_resources == false` at `:670` anyway.
  ⛔ **My derivation, this session, UNVERIFIED.** Check it before it reaches the
  owner's decision; if it holds it belongs in the repair's header, not in a report.
* **Is F107's "the pack's ONLY module with this shape" measured or static?** The
  entry says static audit. The harvester already walks all 105 targets — ask
  whether uniqueness can be made a measurement cheaply, or state plainly that it
  is a static read.

#### Owed work that is OUT of this chain's scope — route it, do not let it go quiet

**F105 has still never been reproduced end to end.** The guard is measured; the
field route (a cost tech sweeping a real levelling site on a real map) is not, and
it needs an attended sitting. It is not yours to run — name it in your close-out
so it does not vanish between F105 reading `fixed` and F107 taking the attention.
