# HOTFIX 1 — AUDIT (link 2 of 2, TERMINAL; link 1 was `HOTFIX_1_APPLY.md`)

Paste into a **fresh** Claude Code session that did NOT do the implementation.
**Start with `git log --oneline -15` + `git pull`.** Read `docs/agent/STATE.md`
(mandatory), `docs/agent/FIX_POLICY.md`, and `bugs/F111`–`F116`.

> 🎯 **YOU ARE THE GATE. Your verdict decides whether the owner uploads.**
> ⛔ You do not fix, you do not upload, you do not open the Mod Editor. You
> **audit, and you are allowed — expected — to say NO.**
>
> ⚖️ **The standing rule, and it points at US now:** a "Fixed" claim is FALSE
> UNTIL CONFIRMED. Every sentence the apply link wrote is a claim, including its
> measurements. ⭐ **This project has been wrong in BOTH directions in one week**
> — a desk audit said 6 self-disabled modules and the game measured 13; a sweep
> called every train module "clean" and two live P1s were sitting in them.

## 0 · Why this patch exists, in one paragraph you must not take on trust

Game 1.1.0 + the first DLC shipped 2026-09-08. Two of our own fixes broke
**visibly in players' games**: `F114` (trains never move between stations — 157
throws in a 42-minute session) and `F115` (landscaping raises the engine's
mod-error dialog naming our pack). Three more were gated or guarded from a
source read (`F111`, `F112`, `F113`). ⛔ **The pack's self-checks did not catch
any of it**, because they ask whether the target still EXISTS. That is the
defect behind the defects, and it is the thing you are auditing.

## 1 · The six changes under audit

Everything since live tree `version` **5**:

| file | defect | shape |
|---|---|---|
| `Fix_LanderCargoRatchet.lua` | F113 | gate (`{class, method}` on a deleted method) |
| `Fix_ExtractorStaffedPerformance.lua` | F111 | **guard, not a gate** — a `type()` test inside the body |
| `Fix_AutomationLawCompensation.lua` | F112 | gate (`test` content check, deliberately NOT named in the dialog) |
| `Fix_TrainCargoDumping.lua` | F114 | gate (`MultiResourceDepotBase` exists ⇒ decline) |
| `Fix_LandscapeUnitFilter.lua` | F115 | gate (added by the apply link) |
| `Fix_TrackSalvageWipe.lua` | F116 | ⛔ **REPAIR, not a gate** — two in-body additions; the ONLY change here that puts NEW code on a player's machine. §2f. |
| `00_Core.lua` | — | ⛔ **UNCHANGED from shipped v5.** The +151-line override surface was reverted per owner ruling 110; verify that in §2c. |

## 2 · What you must actually do (not a checklist to tick — findings to produce)

### 2a · Re-derive every gate's ROUTE, not its citations

⛔ **`EF-081`/the recorded-facts lesson binds hardest here:** the project has
twice inherited a cited line, re-checked the citation, stamped it verified, and
been wrong — because the citation was right and the ROUTE was not. For each of
the five: open the shipped 1.1.0 source yourself and answer **"does this
discriminator actually separate 1.1.0 from 1.0.7, and does the module decline on
the tree the owner is running?"**

Specific traps already known:
- **F115's discriminator is NOT the `MapVars` membership test this brief
  suggested — it was replaced, and here is what to attack instead.** What
  shipped is `{ global = "Landscapes", kind = "any" }` (decline when the global
  is absent), with `MapVarValues["Landscapes"] ~= nil ⇒ decline` as a secondary
  `test`. Rationale: `GameVar` rawsets its global at registration
  (`lib.lua:1069-1071`), `MapVar` never touches `_G` (`:984-1000`), so the check
  is the literal read that raised `attempt to index a nil value (global
  'Landscapes')` — the defect's own expression, not a correlate. The load-order
  question the brief raised IS answered: `autorun.lua:432-434` runs
  `dofolder("Lua")` → `DlcsLoadCode()` → `ModsLoadCode()`. Verify that yourself.
  ⚠️ **The four things actually worth attacking:**
  * ⛔ **The 1.0.7 half rests on OUR RECORDS, not a re-read** — the 1.0.7 tree is
    gone (`EF-075`). If `GameVar` did not rawset on 1.0.7, the module declines
    there too. Claimed SAFE-and-inert (no players on that branch). Is it?
  * It detects the STORAGE move, not the ARITY change. They shipped together in
    1.1.0; a future patch touching only one would fool it. Is that acceptable,
    and is it stated where a future agent will see it?
  * A stray global named `Landscapes` from another mod defeats the `_G` side.
    Does the secondary `test` actually catch that, in that order?
  * ⭐ **The redundancy is DIRECTIONAL, not doubled — say it that way in the
    report, and check the composition rather than the two checks separately.**
    `Require` walks the spec in array order and `return`s on the FIRST failure
    (`00_Core.lua:118`, `:157-163`); the global check is at
    `Fix_LandscapeUnitFilter.lua:92-93` and the `test` at `:98`, so the primary
    is reached first. Under an unpopulated `MapVarValues` the two fail in
    OPPOSITE directions: the primary sees a nil global and **declines** (safe),
    while the secondary — `not landscapes_is_per_map()`, truthy-passes
    (`ok = c.test()`, `:120-121`) — would **pass** (unsafe alone). Because the
    primary is evaluated first and fails in exactly that condition, **the
    composition fails safe and the secondary can never be what lets a bad
    install through.** ⇒ the belt's only real job is the one case the primary
    genuinely cannot see: another mod defining a global named `Landscapes`. In
    that scenario the game tree has necessarily already run, so `MapVarValues`
    is populated and the belt does work.
    ⚠️ **The consequence worth carrying into your verdict:** the load-order
    proof (`autorun.lua:432-434`) is **NOT load-bearing for the primary** — its
    failure mode on an unloaded tree is "decline", the safe direction — so the
    primary holds whether or not that ordering claim survives. The ordering
    proof is what makes the SECONDARY meaningful and what establishes the module
    still applies on a 1.0.7-shaped tree. ⛔ If you overturn
    `autorun.lua:432-434`, the consequence is a dead-but-safe module, **never a
    shipped throw** — do not report it as the latter.
  * ⭐ **`update_suspect` reaches the dialog by a DIFFERENT ROUTE than F114's.**
    F115 rides on `Require`'s native marking for shape specs
    (`00_Core.lua:157-163`); F114 uses a hand-written mark. Confirm both, and
    note that a boot reading 17/13 isolates F114's, not F115's. ⛔ `EF-081`
    already MEASURED that a `test`-only decline is inactive-but-unnamed
    (`AutomationLawCompensation`) — that is the control for this mechanism.
- **F112 is a `test` content check and is inactive but NOT named in the dialog.**
  That is correct by design (`00_Core` exempts content checks from
  `update_suspect`). ⛔ Do not "fix" it into the dialog.
- **F111 is a GUARD, not a gate** — the module still applies and runs a patched
  body on 1.1.0. ⚠️ It is no longer the only change that leaves our code live —
  **F116 is a REPAIR** and adds new code (§2f). Give it
  the hardest look: `type(self.overtime) == "table"` must be correct on BOTH
  shapes, and the module's own header admits an assumption it could not verify
  because the 1.0.7 tree is gone (`EF-075`).
- **F116 is the only REPAIR in the patch** and the only change that ships code a
  player has never run. It gets its own item — **§2f — and it is the one you
  should be slowest to pass.**

### 2b · Reconcile the boot log against the prediction

The apply link predicted **17 inactive / 14 named**, zero
`Fix_TrainCargoDumping.lua:89`, zero `Fix_LandscapeUnitFilter.lua:63`.
⛔ **A difference is a FINDING, not a nuisance.** Run
`python tools/logscan.py --build 6a91a190` over every 1.1.0 log and read the
errors verbatim. ⚠️ Confirm the log you are reading was copied **after
`Mars.exe` exited** — mid-session copies produced a wrong count twice on
2026-09-08 (a "1" that was 6; a "30" that was 157).

### 2c · Verify decision 110 was actioned cleanly

⚖️ **Owner ruled 2026-09-08: the override surface does NOT ship — "that's a
diagnostic tool only."** `Code/00_Core.lua` was reverted to `ce77162` (the
shipped v5 file) and the mechanism moved wholly into the Test Kit's
`Code/97_ForceInactive.lua`.

⛔ **Verify, do not assume:**
- `Code/00_Core.lua` is byte-identical to the shipped v5 file. `git diff` it
  against the last commit that touched it before 2026-08-30.
- The pack's diff vs live v5 contains **only** the five gate/guard files.
- The Test Kit replacement actually works from outside — it swaps
  `SMRFixPack.Require` around a re-apply and replicates `run_apply`'s verdict
  handling **by hand**. ⚠️ That hand-copy can drift from `00_Core`. Check it
  matches, and say so if it does not.
- ⚠️ The Test Kit is NOT in the shipped artifact, so a bug there cannot reach a
  player — weigh your effort accordingly and do not spend the patch's time on it.

### 2d · Audit the PATCH NOTES as hard as the code

`metadata.lua`'s `last_changes` is a player surface and it is where an
overclaim would do real damage.
- ⛔ Must NOT imply the pack is verified on 1.1.0. **17 of 22 full-body
  replacements are still undiffed**, and NO instrument we own bounds body
  divergence — the name sweep sees names, `tools/sigcheck.py` sees arity, the
  runtime self-checks see existence, and **F114 was invisible to all three until
  a player reported it.**
- ⛔ Never name fredware's mod on a player surface (`EF-054`, `FIX_POLICY` §8).
  No load-order advice.
- ⛔ No save-safety claim for 1.1.0 — uninstall safety (PT-20) was verified on
  1.0.7 only.
- ⚠️ **Route-check every "you can X"**: the project overturned a line three
  reviews had passed because nobody walked the steps a real player would.

### 2e · The one thing nobody has done, and you must decide whether it blocks

**17 of the 22 full-body replacements have never been diffed against 1.1.0.**
Five were: `TrainCargoDumping` (F114, broken), `LandscapeUnitFilter` (F115,
broken), `TrackSalvageWipe` (F116 — now diffed in FULL, structurally: a real
divergence, REPAIRED, §2f), `TrackSalvageRefund` (clean),
`TrackConnectorPingPong` (clean). **That is a 3-in-5 hit rate on the
only subset anyone has checked.** ⚠️ And the F116 diff found a divergence the
first pass had MISSED entirely (post-split processing) while overturning two it
had asserted — so "diffed" is only as good as the diff: a keyword comparison of
two bodies is not a diff of them.

⇒ **Ask yourself plainly: is it responsible to ship a "safety" hotfix while 17
untested copies of that same shape remain?** There is a real answer either way —
the two known-visible breakages are fixed now and players are hitting them
today; against that, the next player report may already be in the queue.
**State your position and your reasoning.** The remaining 17 are a bounded,
mechanical job (one body diff each against `ModTools\Src`). If you judge the
patch should ship first, say what the follow-up commitment is.

### 2f · `Fix_TrackSalvageWipe` (F116) — the patch's only REPAIR

⚖️ **Rule on this one separately, and be willing to say "gate it or drop it".**
Every other change in this patch makes our code do LESS. This one makes it do
something NEW, in the salvage path — where the original defect's cost was *an
entire track and every train on it*.

**What landed** (two in-body additions, both marked `-- FIX (F116)`; the ~13
interleaved `F44`/`F45`/`F91` sites were NOT re-copied):

1. the PRE-SORT `node_idx` revalidation 1.1.0 runs at `TrackElement.lua:473-476`,
   guarded by `IsValid(track_obj)` + `type(track_obj.ProcessAllElements) == "function"`;
2. `skip_track_process` forwarded to `self.broken:Demolish` (1.1.0 `:471`).

⛔ **Re-derive the ROUTE, not the citations.** The claim to break is:
*our tail `ProcessTrackElements` calls did not already do this job.* Settle it
yourself by reading the two bodies. The specific trap that made the FIRST
version of `bugs/F116.md` wrong, and that will catch you the same way:

> ⚠️ **Our body DOES call `ProcessTrackElements` — four times, at its tail. It
> looks like the same work and it is not.** Those calls are the **POST-split**
> step (1.1.0's own `:609-613`); they run AFTER the sort, on the RESULTING
> tracks, and ONLY inside the split branch. The 1.1.0 call under audit runs
> BEFORE the sort, on the PRE-split track, on EVERY path. The entry was
> originally filed off `grep -c ProcessAllElements` = 0 — a right grep with a
> wrong inference — and its own author reversed it. **Do not settle this with a
> keyword count in either direction.**

**Questions you must answer:**
- Is the pre-sort call genuinely absent from our body, and does its absence
  actually change the deletion set? The asserted mechanism is that `node_idx` is
  a monotonic build counter (`Tracks.lua:370-371`) that a track MERGE restamps
  from **two separate array positions** (`TrackElement.lua:415-425`) whose values
  collide, repaired only when nothing is under construction (`:430-432`).
  ⛔ **Check that merge path yourself** — the whole repair rests on it.
- Is the capability guard right? ⛔ It is deliberately NOT a `Require` spec,
  because a Require spec would make the module DECLINE where the method is
  absent and cost players `F44` and `F91`. Rule on whether that trade is
  correct — it is a judgement call, not a fact.
- ⛔ **Does the repair PIN US TO 1.1.0's BODY?** It does, and no gate went in
  beside it. Our copy now tracks 1.1.0 at two points and 1.0.7 everywhere else —
  a hybrid matching NEITHER shipped version. **The next game patch re-breaks it
  silently, exactly as this one did, and nothing in the pack will notice.**
  ⚖️ **The auditor must rule on whether that is acceptable for a live patch, or
  whether this module should be GATED like `F113`/`F114`/`F115` instead.**
  The cost of gating is real and was verified, not assumed: `F44` is still live
  on 1.1.0 (an orphaned element with `track_obj == false` reaches
  `track_obj:ProcessAllElements()` at `:475` and `ipairs(track_obj.elements)` at
  `:481`, both of which index a boolean), and `F91` is still live
  (`TrackBase:OnDemolish`, `Track.lua:248-284`, still never calls `DoneObject`;
  1.1.0's new empty-track sweep at `:597-604` is in the SPLIT branch only and
  does not cover the `mass_delete` path). ⚠️ Gating also kills the module's
  `OnMsg.LoadGame` debris/shell sweep, because `SMRFixPack.WhenActive` tests
  `status == "active"` (`00_Core.lua:183-191`).
- ⚖️ **Two divergences from 1.1.0 were left IN DELIBERATELY** and are owner-facing
  in `bugs/F116.md`. Rule on whether leaving them was right:
  * **orphan policy** — 1.1.0 (`:580-595`) REHOMES an element left with
    `track_obj == false`; we DELETE it. ⛔ **On 1.1.0 our "safety" fix can
    destroy a track fragment vanilla would have saved.** Left because the
    repair above removes what manufactures orphans, and because changing
    destructive playtest-derived logic with no reproduction is its own risk.
  * **post-split processing** — 1.1.0 processes each track's COMBINED element
    list (`:609-613`); our 1.0.7 tail processes one array and only when the
    other is empty, so a track with both completed AND under-construction
    elements gets none.
- ⛔ **Nothing here is tested.** F116 was never reproduced, produces no throw and
  no log line, and the repair has never run in a game. A boot log showing
  `TrackSalvageWipe: applied` proves the module loaded, **not** that the repair
  is correct. ⚠️ Do not let `applied` read as verified.
- ⚠️ **`tools/sigcheck.py` rates this module `OK`** — same name, same arity,
  changed body. It rated it OK before the defect was found and it rates it OK
  now. That is §2e's point in one line, and it is why an `OK` from that tool
  must never appear in a patch note as evidence of anything.

## 3 · Bindings

- ⛔ `Mars.exe` must not be running before any loadable-code edit — but **you
  should not be editing code at all**; report instead.
- ⛔ `H-02` no Mod Editor, no `version` edit, **no upload**. `H-03` no portal API
  from a launched game — the first call CREATES the listing.
- ⛔ `H-04` never call a future release ready, and never treat "published" as
  covering anything the owner has not done.
- ⛔ `H-08` never pull a junction · `H-09` never stage a packed folder beside one.
- ⛔ Never modify the game directory. ⛔ Never "correct" a 1.0.7 citation
  (`EF-075`).
- `python tools/doccheck.py` GREEN before any doc commit; a WARN is copied
  **verbatim** into your summary. `STATE.md` is byte-capped — additions need an
  eviction in the same commit.
- ⛔ **Never silently discount a log line.** "Not caused by our leg" is an
  attribution verdict, not a dismissal — report unexplained lines verbatim with
  their age. Every pushback the project has had on this found a real defect.

## 4 · Your deliverable

A report at `agent/reports/HOTFIX_1_AUDIT.md` with, in this order:

1. **VERDICT: SHIP / SHIP WITH CHANGES / DO NOT SHIP.** One line, first line.
2. **Findings**, most severe first, each with: the file and line, what is wrong,
   how you know (the route you re-derived, not the citation you inherited), and
   what it costs a player.
3. **What you verified and what you could NOT** — explicitly. ⛔ A thing you did
   not check is not a thing that passed. Name the gaps.
4. **Decision 110** ruled, with reasoning.
5. **Your position on 2e**, with reasoning.
6. Anything for `PLAYTEST_CHECKLIST.md` → "Decisions waiting on you".

Then: `doccheck` GREEN → commit → **push** → hand back to the owner.

⛔ **Do not soften a real finding to avoid delaying the patch, and do not
manufacture one to look thorough.** If it should ship, say so plainly — a clean
audit that says SHIP is a real result, and the owner's time is the scarce
resource here. If it should not, say that just as plainly and say exactly what
would change your mind.
