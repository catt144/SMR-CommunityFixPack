# Chain prompt 2 — adversarial QA, then build or decline

**Read `README.md` in this folder first — its binding chain rules apply to you.**
Unattended: no game, no keyboard, no owner. Start with `git log --oneline -10` +
`git pull`. **You are the terminal prompt: this folder must be EMPTY when you
finish, and its emptiness is the done-condition.**

You are the adversary and the builder. Two sessions have now touched F11 and
F99 — the one that found them (2026-08-03) and the one that re-derived them
sealed (prompt 1). **Every "done", every "verified", every "clean" either of them
wrote is a claim.** Trust nothing forward; sample against primary evidence.

Then you decide, and you are the one who acts on the decision.

---

## What is actually at stake

**F11.** A one-line fix for a genuine `table.remove` misuse in
`Colonist:ExitVehicle`, shipped and default-on. ⛔ **The owner has decided it
ships — that is closed and you may not re-open it.** What is open: it is
currently a **full copy of a ~30-line shipped method**, and a **pre-wrapper**
conversion has been proposed that would keep the fix while letting the other ~29
lines stay vanilla. You decide whether that conversion gets built, and if so you
build it.

**F99.** A new `cand` entry: `TrackElement.lua:805` dereferences `elements[1]`
after a rebuild that can come back empty; 14 hits in one session, **every one
under `CheatCompleteAllConstructions()`**. You decide its disposition — rider,
fix, or leave it filed — and route the severity call to the owner either way.

---

## Jobs

**Job 1 — todo list up front**, one item per commit-and-verify unit, one in
progress, updated immediately (`WORKFLOW.md` element 1). The owner reads it.

**Job 2 — audit prompt 1.** Read `DERIVATION.md` and prompt 1's outbox below.
Then:

- **Verify the seal held.** `git log --diff-filter=A -- docs/agent/prompts/f11-f99-review/DERIVATION.md`
  should show the derivation committed BEFORE any commit touching `F11.md` or
  `F99.md` in that session. Check it; do not take the attestation's word.
- **Sample its claims against primary evidence** — `ModTools\Src` and the
  archived logs, not against the 2026-08-03 write-ups. Sample at least the
  load-bearing ones: the `SetHolder`/`OnExitHolder` chain, the cross-map
  ordering, the label-membership premise (point 7), and the `TrackElement`
  abort point.
- **Where prompt 1 and the 2026-08-03 session AGREE, ask whether they agree for
  the same reason.** Two sessions reaching one conclusion by the same wrong route
  is the failure this project keeps having; the seal was designed to catch it, so
  spend the check here.

**Job 3 — adjudicate F11's shape.** Decide, with reasons on the record:

- Does the pre-wrapper conversion get built? The case for it is drift: the copy
  freezes shipped lines including a travel-time comfort formula that **F21** is
  itself about. The case against is that any change to working shipped code is
  risk, and the current form is verified while a new one is not.
- If **BUILD**: write it. `FIX_POLICY.md` §3a and §2 bind. Keep the module's
  `SMRFixPack.Require` guards meaningful for the new shape — a guard that no
  longer guards anything is worse than none. Parse sweep (python + luaparser,
  `utf-8-sig`) before the commit. Update the module header comment: it currently
  documents a full-replacement approach and would be lying.
- If **DECLINE**: say why on the F11 entry, so the next session does not
  re-propose it from scratch.
- ⛔ **You may not claim the conversion is verified.** It is behaviour-preserving
  *by construction* at best; it earns `tested` only from a probe suite run or a
  keyboard leg. Say exactly that wherever you record it, and leave the
  verification owed.

**Job 4 — adjudicate F99.** Decide: does it become a checklist rider (with a
**TAKEABLE WHEN <condition>**), a fix, or does it stay filed as `cand`? The
discriminator on the table is one *normally* completed track — drones, no
cheat — on a disturbed element list. Weigh it against `FIX_POLICY` §4a (WHO
BENEFITS): if the line is only reachable through a dev cheat, nobody but us
benefits. **Severity remains an owner call regardless** — make sure it is
routed, not absorbed.

**Job 5 — reconcile the record.** Whatever you decide, `F11.md`, `F99.md`,
`STATE.md` and `PLAYTEST_CHECKLIST.md` must agree with each other and with the
evidence when you are done. Corrections to the 2026-08-03 text are made
**visibly** — the project records overturned reasoning rather than overwriting it
(see how the old F11 audit block was superseded rather than deleted). Owner
decisions go to the checklist's "Decisions waiting on you" with a recommendation.
`python tools/doccheck.py` green before every doc commit; STATE.md is capped at
60 lines, so adding means evicting to `SESSION_LOG.md` in the same commit.

**Job 6 — close the chain and REPORT.** Delete `DERIVATION.md`, this file and
`README.md`; the folder goes away entirely. In the same commit, write the outcome
where it will be found later — a short section on each entry is enough; do not
create a new report document unless there is a finding that belongs nowhere else.
Then report to the owner in the session: what changed, what you overturned, what
you declined and why, and what verification is still owed.

---

## Scope fence

**In:** F11's fix shape, F99's disposition, the correctness of both prior
sessions' reasoning, and the code if you decide to build it.

**Out:** whether the F11 fix ships (owner decided). Any other module. Any live
playtesting or game launch. The `PLAYTEST_HELP.md:312` `ListFixes` staleness
(needs a live reading). D12, PT-62, drone work.

## Stop conditions

- **Prompt 1 and the 2026-08-03 session disagree on a load-bearing premise and
  you cannot settle it from source → STOP. Do not build.** Route the open
  question to the owner with both readings laid out. Building on an unsettled
  premise is precisely what this chain exists to prevent.
- The seal is shown to have been broken in a way that anchored prompt 1 → say so,
  discount its agreement accordingly, and weight your own derivation instead.
- Context running short → self-split (chain rule 4). The folder-empty gate
  belongs to whichever prompt finishes last.

## ⛔ What you may not claim

- **Not** that anything is `tested`. No leg ran in this chain. `tested` is earned
  at the keyboard.
- **Not** that the conversion is safe because it "reads equivalent" — say what
  would falsify that, and leave it owed.
- **Not** that F11's guarded state is unreachable in general; only that specific
  enumerated producers do or do not produce it.
- **Not** that F99 is reachable without the cheat absent a shipped non-cheat path
  to that line, nor that it is unreachable absent a real search.
- **Not** that agreement between two sessions is verification when both may share
  an inherited route.

## Notes from upstream

*(2026-08-03, chain author — the session whose findings you are auditing. My own
soft spots, stated so you can aim at them: the underground-label premise behind
the "index 1513 proves the connected-cities append" claim is mine and unverified;
my "no other producer of a stale `train.units`" position reflects not having
searched, not a search that came up empty; and the pre-wrapper proposal has never
been executed by anything but reading. The F11 measurement I stand behind —
`#units` = 6 and `holder == rocket` exist precisely so the counter could fail —
but the inference drawn from it is fair game, and so is my F99 attribution.)*

---

*(2026-08-03, chain prompt 1 — Opus, the second set of eyes. Everything below is
mine. My full working is `DERIVATION.md` in this folder, committed as `28c253f`
**before** I opened any sealed material; read it if any verdict here looks thin.)*

## ⛔ SEAL ATTESTATION — I did not hold it, and it was not holdable

**Two of the five sealed items are forced into context by rules that outrank a
prompt's discretion. I broke the seal on both, before reading this chain at all.**

1. **`docs/agent/STATE.md`** — `CLAUDE.md`'s first paragraph makes it a mandatory
   every-session read. I read it, whole, before opening prompt 1. Exposure:
   STATE.md:39-47, the F11 and F99 paragraphs.
2. **`git log --oneline -10`** — chain rule 1 *and* prompt 1's own first
   instruction. It prints the subject lines of `787ebcf` and `9ef9efa`, and a
   subject line is the first line of a message body.

**Exactly what I was anchored with**, so you can discount accordingly: that the
rider ran and was called settled; the phrase "no demonstrated producer"; that a
`TransferToMap` hypothesis was called refuted by measurement; that the old F11
entry "cited the wrong class in the wrong file"; that F99 is `cand` with no-cheat
reachability unproven; and 787ebcf's subject, *"the state its fix guards against
has no producer"*. I did **not** open `F11.md` below `**Fix:**`, `F99.md`, the
archive rider, or `git show` on either commit, until after `28c253f`.

**What this costs you.** My F11 "no enumerable producer" conclusion is the same
one I was anchored toward. **Do not count it as independent confirmation** — I
do not. What I do claim as clean: everything that contradicts the anchor
(disagreements 1, 2, 4 below), the alternative-states enumeration, and the whole
of F99, where the anchor gave me nothing beyond "cheat-correlated, unproven".

⚠️ **This is a chain-method defect, not a one-off, and it is owed to
`CHAIN_METHOD.md` before you delete this folder.** Rule 1 and the mandatory
STATE.md read structurally defeat rule 11. Any future sealed prompt must either
name a `git log` form that hides subjects, or extract the sealed STATE.md
paragraphs into a sealed side-file before the chain starts. **Please carry it —
if you would rather not, say so explicitly rather than letting it die with the
folder.**

## Verdict per point

| # | topic | verdict |
|---|---|---|
| 1 | the stale-passenger branch, and what a throw costs | **AGREES**, and goes further: the wedge is `Train.lua:451-453`'s `while #self.units > remaining_passengers` spinning on a decrement (`:448`) that already happened |
| 2 | what happens to `vehicle.units` on `EnterTransporter` | **DISAGREES on route** — see disagreement 1. Same end state, wrong call named |
| 3 | cross-map vs same-map | **NOT ADDRESSED** by the record; they differ, and only one was measured |
| 4 | does `F11COUNTER nil 6 true` support "cannot fire" | **AGREES** on the limit ("does NOT establish that `train.units` can never go stale") — the record is properly hedged and deserves credit. **GOES FURTHER** on the enumeration: six other states of the world produce that identical triple |
| 5 | is the hand call faithful | **AGREES** on the last leg (verbatim `ExpeditionLoadCrew`, I verified it). **GOES FURTHER**: the real loop fires `SetCommand` on many colonists with no `Sleep`; one hand call cannot reproduce a multi-passenger interleaving |
| 6 | does the pool rebuild reproduce the gather pool | **DISAGREES** — see disagreement 3. It reproduces steps 1-2 of a six-step function |
| 7 | ⚠️ the underground-label premise | **premise CONFIRMED, route REFUTED** — see disagreement 2. This is the big one |
| 8 | other producers of a stale `units` entry | **AGREES** (I found none either), with the search named. **GOES FURTHER**: found the same defect class in shipped code elsewhere → filed as `C42` |
| 9 | what is nil at `TrackElement.lua:805` and why | **the record's route is RIGHT and mine was WRONG** — see the reversal below. **GOES FURTHER** on the cause: the guard on that block can never be false |
| 10 | what is left undone, and the residue | **DISAGREES on severity, both directions** — see disagreement 5 |
| 11 | is the cheat load-bearing | **AGREES** — `quick_build` is read once at `:748-750` and never again; the cheat drives frequency, not the path. **GOES FURTHER**: the *block* is entered on every repair completion regardless, because of the dead guard |
| 12 | already covered by F44/F45/F48/C12-C38 | **AGREES** — not a duplicate; I checked rather than assumed. One misdescription noted (disagreement 7) |
| 13 | is the pre-wrapper safe here | **NOT ADDRESSED** anywhere in the record — see below. My answer: **yes, build it** |
| 14 | what the full copy costs | **NOT ADDRESSED** — my answer: two balance expressions and an invisible file-local, all frozen at 1.0.7.396349 |

## Disagreements — all of them, including the small ones (rule 5)

**1. ⛔ The F11 mechanism paragraph names the wrong call, and it is the same
failure mode the entry itself apologises for two sections lower.**
`F11.md:57-66` and `PLAYTEST_ARCHIVE.md:4720-4726` both state the route as
`EnterTransporter` → `SetHolder(transporter)` → `SetHolderOnMap` →
`OnExitHolder`, and add: *"The cross-map case runs `self:TransferToMap(transporter)`
FIRST … the measurement shows it does not drop the holder link."*

**It does drop the holder link. That drop is what removed the colonist.**
`Unit:OnTransferToMapDone` (`Unit.lua:846-851`):

```lua
if self.holder and not IsSameMap(self.holder, self) then
	self:SetHolder(false)
end
```

`SetHolder(false)` → `SetHolderOnMap` → `holder:OnExitHolder(self)` →
`table.remove_entry(train.units, col)`. By the time `EnterTransporter` reaches
its own `SetHolder(transporter)` at `Unit.lua:1209`, `self.holder` is already
`false` and the train's list is already clean.

The measured sitting was **cross-map** (`col:GetMap() == MainMap` false,
`rocket:GetMap() == MainMap` true). So the record attributes a cross-map
measurement to the **same-map** mechanism. Every cited line is individually
correct; the route is wrong; the end state is identical, which is exactly why the
measurement cannot tell them apart. **Second instance of this project's signature
failure, in the NEW text, written in the same commit that corrects the first
one.** 787ebcf's own words — *"Both citations were right about what they said and
the route to them was wrong"* — apply verbatim to its own replacement paragraph.

Consequence, not just bookkeeping: the same-map removal path (`SetHolder` at
`:1209` doing the work) is now **unmeasured and unnoticed**, because the record
believes it was the one observed.

**2. ⛔ "index 1513 proves the connected-cities append" is unsupported by the
evidence it cites — while its conclusion is true for a different reason.**
`F11.md:117-123` and 787ebcf's body: *"An underground colonist cannot be in
`MainCity.labels.Colonist`, so the rider's index `1513` in a `1543`-entry pool
can only have come from the append."*

The inference needs `#MainCity.labels.Colonist < 1513`. **That number was never
printed.** The console line printed `#pool` and `table.find(pool, col)` and
nothing else. If MainCity held 1520 colonists, index 1513 sits inside MainCity's
own block and the argument reverses.

The **premise** is true and I verified it independently: `CityObject:Init`
(`CityObject.lua:11-17`) sets `self.city = map.City` under
`assert(self.city:GetMap() == map)`; `OnTransferToMap`/`OnTransferToMapDone`
(`:70-81`) move label membership on both edges of every transfer;
`Colonist:AddToCityLabels`/`RemoveFromCityLabels` (`Colonist.lua:272-311`) act on
`self.city` and are the only route into the label.

And the **conclusion** survives — but via **step 4 of the same sitting**, which
measured `col.city == MainCity -> false` directly. Premise + that reading gives
`col ∉ MainCity.labels.Colonist` with no reference to index positions at all.

⚠️ Two riders on the premise: `SavegameFixups.FixCityLabels2` (`CityObject.lua:89-116`)
exists *because* objects have shipped with the wrong `city`, and prints a count
when it finds any; and `ManualCityLabels` (`:83-87`) opts classes out entirely.
So **"cannot"** is too strong — "does not, unless a known-buggy state exists" is
the defensible form.

**Recommendation: strike the index argument and substitute the step-4 argument.**
The danger is not this entry; it is the next agent quoting "1513 proves
underground" as an established lemma.

**3. "the rider's index in a surface rocket's gather pool" overstates what the
console line rebuilt.** `F11.md:39` and `PLAYTEST_ARCHIVE.md:4703`. The rebuild
reproduces `CargoTransporter.lua:240-251` — the raw concatenation. The shipped
function then runs three more stages the console line does not:
`thread_running_destructors` filtering (`:252-260`), an idle/`Abandoned`-before-busy
partition (`:262-285`), and `FilterColonistsByTrait` + truncation to `amount`
(`:270-291`). **Membership in the raw pool is established; selectability is not**,
and the index is a position in an ordering the shipped code never uses. The entry
already says the right thing about trait scarcity at `:101-113` — that reading is
correct and its `FilterColonistsByTrait` citation at
`Lua/CargoTransporterNew.lua:163-194` is right (the function is a global defined
in that file and called from `CargoTransporter.lua:270`; I checked, expecting to
find a second route error, and did not).

**4. "Why the counter is honest" is right about what it rules out and silent
about what it does not.** `F11.md:51-55`. `#units = 6` does rule out the
empty-list artifact and `holder == rocket` does rule out "the call did nothing" —
both fair, and designing the counter to be able to fail was the right instinct.
But at least two other states print the same triple and neither is excluded:

- **the `units` table was replaced.** `Holder:KickUnitsFromHolder`
  (`Holder.lua:11-25`) sets `self.units = nil`; `OnEnterHolder` rebuilds a fresh
  `{unit}`. If the train stopped and reloaded between step 2 and step 7 — six
  console commands of wall-clock — `table.find` is `nil` trivially, and `6` is
  just a busy line refilling.
- **`col` was aboard a different train by step 7.** `#units == 6` is the only
  thing tying `col` to `SMRF11_train` at that moment, and `6` is not an identifier.

Cheap prophylactic for any future counter of this shape: print the container's
identity, or `#units` immediately *before* the operation as well as after.

**5. F99's severity is wrong in both directions, and the milder half matters
more.** `F99.md:51-57` — *"a partially-completed track, 14 times in one session"*.

- **Milder than filed: the auto-connect self-heals.**
  `g_ConstructedTracksQueue[track_obj] = GameTime() + 500` is set at
  `TrackElement.lua:799`, **one line before** the throw. The
  `ConstructedTracksCheck` repeater (`:677-693`) then performs the identical work
  500 ms later **with the guards the failing block is missing** — `#track.elements > 0`,
  a re-check between the two `AutoConnectTracks` calls, plus `TryConnectStations()`.
  That the engine ships a correctly-guarded copy of lines 803-806 is also the
  clearest possible statement of what a fix should look like.
- **Also milder: the un-run `table.clear(repair_cgs)` is a no-op on a clean
  build-out.** `repair_cgs` is only ever populated by `Meteors.lua:609` and
  `TrainDisasterHandling.lua:58-59`. Cheat-building underground with no meteor or
  disaster repair groups outstanding means `:811-812` had nothing to clear. When
  it *is* populated the damage is real and persistent: `repair_cgs` is a persisted
  member (`Track.lua:41`), and non-empty means the track reports damage
  (`Track.lua:382`) and refuses deletion (`Track.lua:372`) forever.
- **Worse than filed: the throw escapes the cheat entirely.** The log's paired
  line is `Error calling Lua function "exec" from C` — it unwound out of the
  console `exec`. So per throw: the rest of that `MapForEach` pass never ran, the
  second `for i=1,2` pass never ran, and
  `CurrentMap:ResumeTerrainInvalidations("cheat_all_constructions")`
  (`Cheats.lua:128`) **never ran** — a leaked suspend, seven times over. Cheat-tag
  scoped, so no non-cheating player is affected, but it is real state left wrong.
- ⚠️ **`F99.md:56` cites `EF-008` for "`error()` does not unwind … so execution
  continues with that state in place."** `EF-008` is about `assert()` and about
  mod code; this was a genuine runtime error and the log shows it unwinding all
  the way to C. **The citation does not support the sentence.** (`EF-008` *is*
  load-bearing elsewhere and correctly so — it is why `OrderTrackElements`
  continues past its own `assert(false, ...)` into the restore loop.)

**6. ⚠️ The count is 7, not 14.** `grep -c "TrackElement.lua:805"` on
`Mars.exe-20260803-21.18.38-6a22b86d.log` returns 14; the lines are **7 pairs** —
`[LUA ERROR]` headers at 333, 364, 395, 425, 456, 486, 517 and their C-side
`Error calling Lua function "exec" from C` twins at 363, 393, 424, 454, 485, 515,
546. The other two archived logs contain zero. The figure appears in `F99.md:10`
and `:18`, `F99.md:55`, 787ebcf's body, 9ef9efa's body and
`PLAYTEST_CHECKLIST.md`. **I corrected the checklist by appending a correction
line rather than editing the old one** (rule 5). The entries I left alone — they
are yours to adjudicate (scope fence).

**7. Small: `F99.md:74` describes F44 as "twin elements sharing `node_idx`".**
F44 is *"One-hex track salvage can delete the entire track"* —
`DemolishAndSplitTrack`'s whole-track fallbacks. The description belongs to
neither F44 nor F45 as written. Ten-second correction, recorded because rule 5
says a silently-fixed one is destroyed evidence.

**8. `Fix_TrainPlatformWedge` is still a §1.5 full replacement**
(`REACHABILITY_AUDIT.md:69, 213`) after the F86 §5.4-A conversion campaign
converted five of six. It survived because it is rated **U**, not R3, so
`FIX_POLICY:357-358` never barred it. Not a disagreement with anyone — worth
saying because it makes the conversion a loose end being tidied rather than a new
idea, and `SAVE_SAFETY_REDESIGN.md:318` records it as *"safe — no yield in 32
lines"*, a claim the conversion shrinks to six.

## ⚠️ Where I was WRONG and the record was RIGHT

I want this as prominent as the disagreements, because a second opinion that only
ever finds fault is not a second opinion.

**`DERIVATION.md` point 9 argues by construction that the new-build path cannot
produce the empty list, and concludes the `self.broken` repair branch is
*required*. The load-bearing step of that argument was incomplete.** I checked
that nothing between `TrackGridElement:Init` (`:176-180`, which inserts `element`
into `track.elements`) and line 803 removes elements — and missed that line 802's
`ProcessTrackElements` → `OrderTrackElements` does `table.clear(elements)` at
`Tracks.lua:575` and rebuilds. **`F99.md:45-49`'s route — "clears and rebuilds
`elements`; when the rebuild returns empty, `elements[1]` is nil" — is
mechanically correct and mine was not.**

Two things survive that correction and you should weigh them:

- **Every exit from `OrderTrackElements` I can trace restores or repopulates.**
  The named failure path asserts and then — because `assert` does not unwind
  (`EF-008`) — runs `for i, el in ipairs(all_elements) do elements[i] = el end`
  (`Tracks.lua:616-620`), restoring the original. The `start_el`-nil path never
  reaches the `table.clear` at all. **So neither of us has demonstrated the exit
  that leaves the list empty.** The record's route is the better-supported one and
  is still not closed. If you want one thing settled by reading, make it this.
- **The dead guard stands on its own and is in nobody's write-up.**
  `TrackElement.lua:800` is `if not self.broken then`, and `:774` — inside the
  branch taken when `IsValid(self.broken)` — has already done `self.broken = nil`.
  **`not self.broken` is unconditionally true at line 800.** The guard was
  evidently written to skip that block for repair completions and never once
  does. Whatever route empties the list, repair completions are being fed into a
  block written to exclude them. The dead locals `el1, el2` at `:801` — computed,
  never read — are the matching fingerprint of the unfinished refactor.

Corroboration for the repair angle either way: `CaveIn` appears in both `Mars.exe`
logs and `BreakTrackElement` in the `MarsDebug` log from the same sitting. Cave-ins
break underground track; that is what creates repair sites in a cheat-built
underground colony.

⚠️ **Also: there are THREE logs in `docs/archive/logs/`, not two.** Prompt 1's
"Allowed" list and 9ef9efa both name two. `MarsDebug.exe-20260803-23.14.05-6a22b8b3.log`
is also present and it is where two of my filings came from.

## What I filed (job 4)

- **`C42`** — `cand`. `PassageBase:TraverseTunnel` (`Lua/Passage.lua:1055`) ends
  with a raw `unit.holder = nil`, bypassing `Holder:OnExitHolder`, so the last
  passage element keeps the colonist in `units` permanently; destroying that
  element later runs `KickFromBuilding` on an uninvolved colonist. Found while
  enumerating point 8. ⚠️ **Source-only, unobserved, and one link untraced** —
  whether `LeadIn` actually sets the holder. Rider written with a one-line
  console read that can refute it outright.
- **`C43`** — **ours.** `00_TestCore.lua:172`'s `set_global` trips the engine's
  strict-global guard, so two Wave-5 probes print
  `[LUA ERROR] Attempt to create a new global 'IsNearDome'` / `'AddAreaRubble'`
  into the owner's log and then PASS. Second instance in one day of the pack
  logging its own authoring noise (F100 is the first). Routed to the checklist as
  an owner call.
- **Checklist**: the F99 count correction (appended, not edited), the C43
  decision, and two riders — C42's read, and **F99RESIDUE re-run BEFORE a
  reload**, since the original `0 0` was taken *after* one and load runs
  `SavegameFixups.RebuildBrokenTracksAndConnect` (`TrackElement.lua:824-837`),
  which sweeps exactly what the probe looks for. **That null result is not
  evidence of no damage** and nothing in the record says so.
- Nothing else discovered. `Flight.lua:465/479` (`objects_t` boolean index) and
  `GridObject.lua:77` (`GetShapePoints` nil) appear once each in the debug log;
  **not investigated, not ours as far as the stack shows, and explicitly not
  dismissed** — flagging them rather than absorbing them.

## What I would do — my recommendation, not just findings

**On the pre-wrapper conversion: BUILD IT.** The case does not rest on
reachability at all, which is why the owner's "fix it and ship it" decision does
not need re-opening to justify it.

```lua
local orig = Colonist.ExitVehicle
function Colonist:ExitVehicle(vehicle)
	if not self.holder or self.holder ~= vehicle or not IsSameMap(self, vehicle) then
		TrainsLogging.warn(self, "not in train", self.command)
		table.remove_entry(vehicle.units, self)
		self:DiscardTransportTicket()
		return
	end
	return orig(self, vehicle)
end
```

- **Behaviour-preserving.** Condition true → repaired branch, `orig` never
  entered. False → `orig` re-evaluates the same three clauses, finds them false,
  proceeds untouched.
- **Double evaluation is free and safe.** All three clauses are pure reads
  (`self.holder`, a comparison, `IsSameMap`). The delegation is a direct Lua call
  with no yield between the evaluations, so nothing can change underneath.
- **`EF-012` applies and is why it must be a PRE-wrapper. I verified the premise
  rather than inheriting it:** `ExitVehicle`'s sole shipped invocation is
  `colonist:SetCommand("ExitVehicle", self)` at `Train.lua:447` (grepped the whole
  tree), and its normal path ends in `PopAndCallDestructor` → self-directed
  `SetCommand` (`ColonistTransport.lua:562/564/570`). A post-wrapper here would be
  silently dead. Worth one line in the module header so the next person does not
  try.
- **`return orig(self, vehicle)` never returns** in the delegated case — correct,
  and a proper Lua tail call, so no frame is retained.
- **It is what un-freezes the copy.** The full copy pins
  `ColonistTransport.lua:548-570`, of which two lines are live tuning: the
  `LuxuriousTrains`-gated comfort penalty (`:555-557`, a tech gate + a stat scale
  + a rate in one expression) and the `seen_forest` sanity bonus reading
  `TechDef.GreenView.param1` (`:558-560`). Plus the recreated file-local
  `stat_scale = const.Scale.Stat` — **invisible to any `Require` check, because a
  file-local is not a symbol you can guard on.** A patch changing any of them
  produces no error, no warning and no `Require` failure; the mod just serves
  stale numbers. The pre-wrapper's frozen surface is the condition and the branch
  body, and the branch body is what we are deliberately overriding.

**Three things to do while you are in there:**

1. **Drop `{ path = { "const", "Scale", "Stat" } }` from `Require`**
   (`Fix_TrainPlatformWedge.lua:26`) and the `local stat_scale` line. The
   pre-wrapper does not use it, and leaving it gates the fix on a symbol the fix
   no longer touches.
2. **Confirm apply-once before shipping.** The full copy is idempotent; a
   pre-wrapper is not — a second `apply` captures the first wrapper as `orig` and
   nests. Functionally harmless as written (the branch returns before delegating)
   but it is a property the current file has for free and the new one does not.
   **I did not audit the loader and will not assert it is safe.**
3. **Consider `if vehicle.units then` around the removal.** `KickUnitsFromHolder`
   sets `self.units = nil` (`Holder.lua:13`); `table.remove_entry(nil, self)` is
   then `find(nil, self)`. Cheap insurance, not required by the defect.

**On F99: file it properly as work, at low priority, and do not build yet.**

- **The defect is real and is more specific than the entry says.** The dead guard
  at `:800` is a concrete, checkable authoring error that nobody has written down,
  and it means repair completions enter that block on every path, cheated or not.
- **But the exit that leaves `elements` empty is still not demonstrated by
  anyone** — see the reversal above. That is a reading job, not a keyboard job,
  and it is the honest blocker on a fix. **If you do one thing on F99, do that.**
- **The fix, when it comes, is not novel** — the engine already ships it at
  `TrackElement.lua:680-687`. Guard `#elements > 0`, re-check between the two
  `AutoConnectTracks` calls, and either use `track_obj` (= `element.track_obj`)
  instead of `self.track_obj` or make the dead guard live. **Do not decide which
  until the emptying route is known**, because the two candidate causes want
  different fixes and shipping the wrong one buys nothing.
- **Severity: low, and lower than the entry implies** — the auto-connect
  self-heals via the queue, and `repair_cgs` damage needs meteor or disaster
  groups outstanding. It is not a release gate on anything. FIX_POLICY §4a (WHO
  BENEFITS) is still unsatisfied and the rider I wrote is what would satisfy it.
- **Keep "unproven" on no-cheat reachability.** The record is right to refuse the
  claim and I found nothing that would let anyone stop refusing it.

**On the F11 record itself:** the two route errors (disagreements 1 and 2) are
worth more than either finding, because the project's stated failure mode is
*"every cited line is right and the route is wrong"* — and 787ebcf corrected one
instance of it while writing two more into the replacement text. That is not a
criticism of that session; it is evidence about how hard the failure is to see
from inside, and it is the strongest argument this chain has produced for keeping
sealed second derivations. **Which is exactly why the seal being unholdable
matters, and why I would rather you fixed the method than praised the outcome.**
