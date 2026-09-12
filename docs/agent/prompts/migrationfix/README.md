# `migrationfix` — mini chain: build the migration audit's code actions, then audit both the build and the audit

Authored **2026-09-11** by `smr-bugfixpack-cb` at the owner's instruction. **Staleness anchor: HEAD was `33b9f8e`.**
Two links, self-consuming (each prompt `git rm`s itself in its own close-out commit). The owner starts link 01 by
hand; link 02 follows it.

| # | file | model | job |
|---|---|---|---|
| 01 | ~~`01_BUILD_opus.md`~~ **CONSUMED 2026-09-11, close-out in HANDOFF below** | Opus | Repair F59 (against the verified dossier, which is the report **plus** the re-derivation that found a second harmful caller); build F60's retirement as the report proposes, with its replacement trace written as falsifiable claims. |
| 02 | `02_AUDIT_fable.md` | Fable | Terminal adversarial backward QA. Grades the build, **and** surface-sweeps Astra's eight module verdicts — a logic check, not a re-run of the deep dive. **Holds the upload gate.** |

## The ordering that makes this safe

**01 build → 02 audit → owner uploads.** Not build → upload → audit. The owner's instruction was "build it as
Astra wrote it and audit after", and that is only safe while the upload sits behind the audit: a refuted build
then costs a revert instead of a release. Link 01 is told in its own text that it is the executor and not the
certifier, and link 02 is told it is the gate.

## The one place "as is" was overridden, and why

Astra's report proposes an **expedition-home exclusion** for F59. That covers one of the two harmful callers and
does nothing for the other — the manual-assign over-capacity route, desk-controlled 8/8 in
`tools/desk_f59_interact.py`, reachable by an ordinary player action, on both game branches. Building the
report's shape as-is would have shipped a fix leaving the more reachable harm in place, so link 01 builds against
`bugs/F59.md`'s last two sections instead. **F60 is built as the report proposes**, with link 02 as its check.

## Both links can stop at any time — the owner granted it explicitly

⚖️ Owner, 2026-09-11: Opus may stop and report any concern at any point; Fable has the same authority, **and**
may recommend the repair shape or recommend retirement if it thinks that is what the evidence says. On
repair-vs-retire for F59 the owner is **leaning repair** — link 01 defaults to it and weighs the alternative while
building, but that lean is not a ruling and neither link is bound by it. Because repair-vs-retire is a
`FIX_POLICY` §4a who-benefits call, it belongs to the owner: either link that reaches for it **stops and routes
it to `PLAYTEST_CHECKLIST.md` → "Decisions waiting on you"**, rather than settling it quietly.
A stop is cheaper than a wrong ship, and both links are told so in their own text, because a "tonight" deadline
biases an executor against stopping.

## What is NOT in this chain

The audit reviews eight modules but proposes only **two** code actions. The five PARTIAL rows (F51, F52, F53,
F58, F73) and F54 change what we **claim** on the fix list and the store card, not `Code/` — that is
`prompts/perma/PUBLIC_SURFACE_SWEEP.md`, and link 02 sweeps those verdicts for soundness so the sweep has
something trustworthy to work from. **F80 is capture-before-mitigate** and is not built here.

No status word in this chain is a playtest grant: `tested-attended` is the sitting's. The four-click in-play
receipt for F59 is in checklist **151** and in link 01's foot.

---

## HANDOFF

*(Link 01 appends its close-out here — disagreements first, then what it built as falsifiable claims, then what
it skipped by name, then the commands a fresh session must re-read, then the one thing it is least sure of.
Link 02 reads this section before anything else.)*

**RAN 2026-09-11 by `smr-bugfixpack-31` (Opus). A shipped alone; B stopped on its own gate.**
`01_BUILD_opus.md` is `git rm`'d in the same commit as this section.

### 1 · Disagreements first — things in the briefing or the report I found wrong, stale or incomplete

1. **The report's F59 shape is insufficient, and that is now MEASURED rather than argued.** The brief already said
   so; what was missing was a number. `tools/desk_f59_interact.py` now runs the audit's proposed expedition-home
   exclusion against the manual-assign route and the residence **still overfills 3/2 with one assert**. Claim to
   falsify: *the audit's exclusion fixes A1 only*. Leg: "AUDIT IDEA IS INSUFFICIENT".
2. **⛔ THERE IS A THIRD HARM, and neither the report nor the dossier had it in either direction — A3,
   `Residence:OnDestroyed`.** The dossier filed this site as an UNRESOLVED lead on the reasoning that "whether a
   homeless colonist can be assigned INTO the residence being destroyed … is NOT SAMPLED". I sampled it, and the
   answer is split in a way no one predicted:
   * at a capacity the evictions fill exactly, **all three module shapes end identically** — because the evicted
     resident is appended LAST to the dome Homeless label and `CheckHomeForHomeless` walks it BACKWARDS, so our
     old hook only ever reached the colonist vanilla's own `:86` was about to re-house. Our hook added nothing.
   * give the dying residence **one spare slot** and our old hook reaches a colonist who was **never a resident**
     and whom vanilla never touches. `:89 self.colonists = {}` then drops them ⇒ pointing at a dead home.
   So the lead was right to be open, and the natural reading of it ("our hook causes the dangling") is **wrong** —
   vanilla causes the dangling; we caused a *different*, narrower harm on top. Claim to falsify: the three A3 legs.
3. **Deferral alone would NOT have fixed A3 — it makes that site worse.** After the eviction loop, `colonists`
   and `reserved` are both empty, so free space is the FULL capacity and a deferred guard opens **wider** than the
   synchronous one did. This is the one place the generic repair needed a specific guard (`not home.destroyed`).
   If you attack one thing in this build, attack this: it is the only non-uniform part of the design.
4. **`FIX_POLICY` §1.4 — written today from this very module — points at a design I deliberately did NOT build,
   and I am flagging the tension rather than resolving it.** It says that when a caller keeps using the state,
   "the hook needs a guard keyed on that caller's own state, **not a later cleanup pass**". I read "later cleanup
   pass" as *let the harm land, then repair it*, which deferral is not — deferral never publishes the vacancy
   until the operation is done. But a reviewer could read §1.4 as preferring caller-keyed guards outright, so
   here is the measured reason I rejected them: **`Residence:KickResident` has THREE shipped callers**, and the
   other two are the infopanel's own kick button (`Lua/XDef/sectionOccupantList.generated.lua:34`,
   `sectionResidenceList.generated.lua:34`), where the bed genuinely frees and the notification is the benefit.
   A re-entrancy guard on `KickResident` would suppress it there. Keying on the forced colonist is worse:
   `user_forced_residence` survives `g_Consts.ForcedByUserLockTimeout` = one sol (`__const.lua:171-177`), so a
   "somebody is forced to this home" test suppresses ordinary notifications for that residence for a sol of game
   time. **Both variants are the stop-tell the brief named** (a guard that also suppresses ordinary notifications
   in reachable cases). Deferral is the only shape I found that keeps the benefit. ⚠️ **If you disagree, this is
   an owner-facing §4a call, not yours or mine.**
5. **The brief's "both existing harnesses must still pass (12/12, 8/8)" is not satisfiable as literally written,
   and should not be.** Those counts included legs asserting *F59 applied ⇒ the harm expresses*. A repaired module
   must fail them. Rather than delete the falsifiers I gave both harnesses a third shape: the **pre-repair wrapper,
   extracted from git** at `bb50f5d` (`desk_migration_cluster.F59_HARMFUL_REV`), never retyped. The harm legs run
   on that; the repair legs run on `Code/`. Counts are now **18/18** and **23/23**.
6. **The brief says H-10 makes item A need no `items.lua` entry. Confirmed** — no module was added, renamed or
   dropped, and `doccheck`'s MODULE SETS line still reports Code/, `items.lua` and `metadata.lua` agreeing by
   name, with the owner's uncommitted v8 files untouched.
7. **A side effect the brief did not anticipate: the repair INVALIDATED the Test Kit's own F59 probe.**
   `FreedHousingNotice` in `30_Probes_Wave3.lua` read `notified` immediately after
   `C.SetResidence(colonist, false)`, so against the corrected module it returned **FAIL** — a false negative
   waiting in the owner's next `RunAll()`. Fixed and committed in the Test Kit repo (`4d34735`). Not raised as an
   owed item — the Test Kit being local-only is settled; a probe making a false claim is a different thing.

### 2 · What I built, as claims you can falsify

**A · F59 — `Code/Fix_FreedHousingNotice.lua`. THE GUARD'S SHAPE:** the wrapper on `Colonist:SetResidence` is
kept, but it no longer calls `left:CheckHomeForHomeless()` inline. It schedules
`CreateGameTimeThread(notify_freed_home, left)` and **re-takes the entire decision after the wake**, on state that
by then includes whatever the enclosing operation did with the slot. The schedule-time test is deliberately the
**same one the pre-repair module used, plus `not left.destroyed`**, so no event this module used to consider is
dropped at the door; the real decision moved, not the scope.

* **Claim A-i.** Soundness rests on **EF-029** (`CreateGameTimeThread` DEFERS — body does not run before the
  creating statement continues; MEASURED 2026-08-01, owner at the keyboard) plus cooperative scheduling. If
  EF-029 is wrong, the whole build is wrong. I did not re-measure it.
* **Claim A-ii.** A1 stops because `Residence:GetFreeSpace` (`:232-234`) subtracts `#self.reserved`, so once
  `OnDisappear:5005` has taken the hold there are 0 free and we decline. **Pinned in the manifest**, because the
  repair dies silently if vanilla stops counting reservations.
* **Claim A-iii.** A2 stops because `ColonistInteract:348` has assigned the forced colonist by the wake ⇒ 0 free.
* **Claim A-iv.** A3 stops because `Building:Destroy` sets `self.destroyed` (`Building.lua:1560`) **before**
  calling `OnDestroyed` (`:1576`); the other two entry paths (`Residence:Done:78`,
  `Building:Refabricate:1870` → `DoneObject:1889`) leave the object invalid by the wake, caught by `IsValid`.
* **Claim A-v.** The benefit is intact: ordinary vacancies still notify, one scheduler step later instead of
  synchronously, versus `Clamp(#Colonist/300, 0, 12)` hours. Both harnesses carry benefit legs, and the interact
  harness proves it specifically on `KickResident`'s **benign** caller (the infopanel kick), which is the caller a
  caller-keyed guard would have broken.
* **Claim A-vi — the control that makes the rest mean something.** Each harness has `synchronous=True`, which
  defeats the deferral and leaves everything else identical. **Both harms come back.** That pins the deferral as
  the repair rather than an incidental change to the guard.

**THE PER-CALLER ANSWER, all 11 sites.** Independently re-derived, not inherited: a grep of the 1.1.0.403908 tree
returns **exactly 11 call sites, ONE definition (`Colonist.lua:2898`), no subclass override**. Full table in the
module header. Behaviour **CHANGES** at three: `Colonist.lua:435` (A1), `Residence.lua:157` (A2),
`Residence.lua:85` (A3). **UNCHANGED in effect, one scheduler step later:** `Colonist.lua:1255` (Erase), `:1297`
(death), `:2926` (UpdateResidence — the intended case), `Residence.lua:348` (ColonistInteract's own assignment),
`Data/TraitPreset.lua:772` (Youth leaving a Nursery). **No-ops:** `Colonist.lua:4995` (OnDisappear — `:5039`'s
`SetDome` already cleared residence, so `:2901` returns early) and `NaturalHabitat.lua:7` (`:6`'s `SetDome(false)`
already cleared it via `:435`). **`Residence.lua:265` (capacity shrink) is SAFE by computation, which I redid
rather than inherit:** the loop runs only while `#reserved + #colonists > capacity - closed`, so `GetFreeSpace()`
is `Max(0, negative)` = 0 at every hook call and the pre-filter declines — **zero threads created there.**
⚠️ `NaturalHabitat.lua:7` is worth your attention: its `:6 SetDome(false)` reaches `:435` **inside
`KickOldestResident`**, i.e. A2's shape again on a MicroGHabitat. Deferral covers it without knowing it exists;
the audit's expedition-exclusion would not have.

**MANIFEST (§2b): three SRC rows added**, each with a DEFECT pinning the load-bearing *property* (the absence
form the module already used): `Residence:GetFreeSpace`, `Unit:EnterTransporter` (boarding must reach
`OnDisappear` synchronously — `Unit.lua:1305` → `:1225`, no yield) and `Residence:ColonistInteract` (kick and
assignment must stay in ONE synchronous body). **If vanilla ever splits either leg across a yield, the deferred
notification lands in the gap and the harm returns** — bodycheck now goes red instead of staying silent.

**§3a: a NEW capturable site, disclosed.** The thread blocks in `Sleep`, so a save in that window serialises our
body by value (EF-023 route (a)). It is **layer-2-equivalent by construction**: the FIRST statement after the only
yield is the orphan gate `if not SMRFixPack then return end`, nothing vanilla is touched before it, the body has
**zero upvalues**, and it holds **no colonist reference** — which matters because `Erase` and death delete the
colonist inside the same operation. An orphan executes nothing and exits where we chose.
⚠️ I did **not** edit `reports/D13_EXPOSED_SET.md` — that is D13's own derivation. Flagging that its capturable-code
set has gained a row.

**B · F60 — NOT BUILT. STOPPED on gate 1, which is the gate's own instruction, not a judgement of mine.**
`items.lua` **and** `metadata.lua` are modified-and-uncommitted in the tree (the owner's v8 Mod Editor pack — both
are comment-stripped, i.e. a `SaveDef` round-trip). Retiring a module rebuilds both via `SaveDef`, so the brief
says ship A alone and leave B. **I did not re-audit F60, did not trace its replacement, and did not touch it.**
It is still registered and still shipping. Routed to the owner in checklist **152 (b)**.

### 3 · What I did NOT do, by name

* **F60 retirement** (item B) — stopped on the release-lane gate, above. No trace produced; do not read its
  absence as a verdict either way.
* **`reports/D13_EXPOSED_SET.md`** — not updated for F59's new capturable row (D13 derives its own set).
* **`reports/MIGRATION_DEV_REPORT.md`** — not edited. The report stands as Astra wrote it; my disagreements are
  here and in `bugs/F59.md`, not retrofitted into it.
* **The PARTIAL rows (F51, F52, F53, F58, F73) and F54** — out of scope per the brief; public-surface work.
* **F80** — capture before mitigating; untouched.
* **The new infopanel-kick lead** — filed in `bugs/F59.md`, deliberately NOT fixed: it is pre-existing,
  unchanged by this repair, and the who-benefits call is the owner's (checklist 152 c).
* **No playtest status word, no version touch, no Mod Editor, no upload.** The 1.0.7 frozen build still carries
  the unrepaired module (ck151 e ruled it stays frozen) — recorded, not acted on.
* **Did not promote to a fact file** the ordering `Building.lua:1560 destroyed = true` → `:1576 OnDestroyed()`,
  which is load-bearing for A-iv. It is cited in the module header and `bugs/F59.md`. Worth an EF if you agree.

### 4 · Commands a fresh session must re-read, with results

| command | result |
|---|---|
| `python tools/desk_f59_expedition.py` | **18 of 18** (was 12/12 pre-repair) |
| `python tools/desk_f59_interact.py` | **23 of 23** (was 8/8 pre-repair) |
| `python tools/desk_probes_f67_f59.py` | **10 of 10** (was 9, L3 split into L3/L3b) |
| `python tools/deskbench.py` | **16 harnesses, ALL HELD** |
| `python tools/parsecheck.py` | `48 file(s) in Code, 0 error(s) [Lua 5.5]` |
| `python tools/bodycheck.py` | `121 manifest row(s) / 46 stamped modules` — **116 OK**, 2 NO-MANIFEST, 1 NO-DEFECT, 4 SRC-NONE (was 115 rows / 110 OK) |
| `python tools/doccheck.py` | **GREEN** (indexes regenerated with `--regen`) |
| `python tools/bodycheck.py --module FreedHousingNotice --all` | **8 of 8 rows OK** (4 SRC + 4 DEFECT) |

⚠️ `deskbench.py` went **REFUTED** mid-build when the repair broke the kit-probe harness, and that was a true
signal, not noise — it is what surfaced disagreement 7. If you re-run it and it is green, the probe fix is in.

### 5 · The one thing I am least sure of

**That `Sleep(0)` on a game-time thread wakes soon enough, and at all, in the states a player is actually in.**
Everything above is desk-measured on shipped bodies, but the deferral's *latency* is modelled, never measured:
`desk_migration_cluster.defer_shim` models **ordering only** (EF-029 + cooperative scheduling) and says so. EF-029
itself scopes its claim the same way — *"this measures the create call, not scheduling latency"*. Two specific
places that could bite and that no leg here covers:
1. **Paused game.** Game time does not advance while paused, so a bed freed during a pause is offered at unpause.
   I believe that is harmless (nothing else moves either) but it is an argument, not a measurement.
2. **A save taken inside the window** — the thread persists (EF-019) and resumes on load; I reasoned it through
   and the body re-reads everything after the wake, but no save/load A/B was run.
If one thing gets attended time, make it the four-click receipt in checklist 152: it settles A2 in play in under a
minute and it is the harm a real player is most likely to meet.
