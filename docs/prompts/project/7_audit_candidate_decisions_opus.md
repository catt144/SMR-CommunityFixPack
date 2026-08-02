# Chain 7 — audit candidate DECISION packages (pre-cleared: the package's own §4 pass IS the decision)

> ## ⛔ SEALED: `docs/reports/BLIND_AUDIT.md` — DO NOT OPEN
>
> **This prompt is FORBIDDEN from reading, grepping, summarising, or acting on
> `docs/reports/BLIND_AUDIT.md` or any part of its contents.**
>
> **Why (so this is not rationalised around):** it is a **blind control**. It was
> produced by a fresh session that deliberately read no project docs, and its
> entire evidential value is that it was written without the project's own
> conclusions in view. **Chain prompt 12, job 6b** examines it against the full
> record it was forbidden to see, doing its own pass first and only then opening
> the sealed key — so that neither reading anchors the other. **Any earlier
> prompt that reads it destroys the independence that comparison depends on, and
> the contamination is undetectable afterwards.**
>
> - Do not open it. Do not `grep`/`Read` it. Do not ask a subagent to.
> - **If a broad search incidentally surfaces its contents: stop, discard, do not
>   use it, and say so in your handoff notes.**
> - This is not a scope call you may weigh against a deadline or a judgment call
>   the blanket pre-clearance covers. **Only prompt 12, at job 6b, may open it.**

**One-off; delete this file in your final commit. Read `README.md` in this
folder first — especially the owner blanket pre-clearance block, which
changes this prompt's nature:** the owner pre-approved building every
package that PASSES its own §4 bar (as amended by prompt 1 — check which §4
is in force FIRST). **Evidence remains the gate; the ask is removed.** The
owner reviews the outcome table; they are not needed per-item.

**Staleness check: `git log --oneline -10` + `git pull`.** Read prompts
6/6b's outboxes below before packaging anything they swept.

## The decision packages (todo list first; one package = one item)

Work each package to the same standard as if the owner were deciding:
defect claim + Src evidence (on the C-entry), the intent tell, the
reachability tier YOU derive this session (§4 enumeration — the audit did
NOT do these), who benefits (§4a), the fix shape and cost. Then:
**PASSES all bars → record the pass on the entry and hand the spec to
prompt 8 (pre-cleared). FAILS any bar → close it honestly on the entry
(`wontfix` with grounds, or stays a candidate) — the clearance never
converts a failed bar into a build.** Borderline → that is what
stop-and-ask is for; the clearance covers clear passes, not judgment calls
you are unsure of.

1. **C33 — the track-shell leak (+ the F44 amendment).** The package the
   owner most needs: whole-track demolition leaks an undeletable invisible
   `TrackBase` shell, **and our own F44 mass-salvage path reproduces it**.
   Recommendation to present: file the F-row; amend `Fix_TrackSalvageWipe`
   to stop producing shells at source; adopt fredware's exact-signature
   shell deletion (temp-tables + `DoneObject`) as the repair shape + a
   sanitizer sweep for saves that already carry shells. Note the shell pins
   `demolishing = true`, the field F47 half-B stands down on.
2. **C22 — Saint blessing label mismatch.** Airtight Src evidence; the fix
   is a targeted label substitution (`GetTraitLabel("Religious")`) — cheap,
   data-shaped. Derive reachability (Saint is a breakthrough trait —
   R2-ish?); present.
3. **C23 — the three dust-devil scheduler defects.** Each sub-item is its
   own §4 subject (bundle lesson): the chance-as-count truncation, the
   `CurrentMap`/`MainMap` descriptor read, the missing `DustStormsDisabled`
   term. Present individually; they may get different answers.
4. **C24 — the asteroid-visit precedence bug.** Verified on the line;
   complements our F72 (we fix the false negative; vanilla's false positive
   passes through). Present with the empty-selection-screen player symptom.
5. **Anything prompt 6 promoted** (C04 F-row? C32 verdict? F35 extension?)
   gets the same package treatment here.

**For every YES: write the fix SPEC (module, technique per FIX_POLICY §1,
probe outline, intent statement, tier) into the BUGS entry and hand the
build to prompt 8's inbox.** For every NO/defer: record the reasoning on the
entry (a declined defect is a `wontfix` with grounds, or stays a candidate —
owner's wording rules).

## Scope fence

**In:** packaging, tier derivation, pass/fail dispositions, specs for
passing items. **Out:** building anything (prompt 8); re-sweeping (prompts
6/6b did it); any candidate 6/6b left at CANNOT-DETERMINE (it stays a
candidate — no package without settled evidence).

## Stop conditions

- A package's reachability derivation surprises you (R4, or intent turns
  ambiguous) → record the narrower true thing; never round up to "fixable".
  A borderline call you cannot make cleanly → stop and ask (the clearance
  covers clear passes only); route the question to the owner, not to a
  guess.

## What may not be claimed

No recommendation may cite the audit's tier column as reachability — the
audit graded witnesses, not call-site enumerations. Every package derives
its own tier this session or says it didn't.

## On completion

Outbox → `8_f86_phase4_conversion_batch_opus.md`: the approved-fix specs
(or "none approved"). Delete this file, commit, push.

## Notes from upstream

**From prompt 1 (2026-08-01) — the §4 amendment is APPLIED, and applying it
activated one decision on ALREADY-SHIPPED code. It is yours; it is not a
candidate package.**

The amended §4 is in force (`FIX_POLICY.md` §4, adopted verbatim from
`REACHABILITY_AUDIT.md` §4 under the owner's blanket pre-clearance) — that is
the "check which §4 is in force FIRST" answer for your header. Its new R3
bullet reads: **"R3 ships only as a §1.1–§1.4 patch; an R3 §1.5 full
replacement needs an explicit user decision (the F24 lesson)."**

**Two shipped items are in that combination and have no such decision on
record: F29 (items 1 and 3) and F57(a).** Both are R3 latent-by-data fixed by
§1.5 method replacements; both entries anticipated this in writing before the
amendment landed ("No action unless the owner wants the stricter line" — the
owner now has it). Add them as a **package 0** ahead of the candidate work:

- The bar is the same one you apply to candidates, run backwards: does the
  latent benefit justify a permanent §1.5 maintenance cost, given the fix is
  already built, probe-covered and A/B-clean?
- Three live answers, none presumed: keep both as replacements · convert to a
  §1.1–§1.4 shape where a wrapper can reach the defect · drop the latent
  halves. **F57(a)'s defect is a mid-function key write, so the conversion
  option may not exist there** — weigh it, do not use it to skip the ask.
- **This one is NOT covered by the blanket pre-clearance.** The clearance
  removed the approval step for adopting the rule; it did not pre-decide what
  the rule then asks about existing code. If the answer is anything other than
  "keep", it changes shipped modules — put it to the owner.
- Nothing here says either fix is wrong. F29's own entry is the project's
  worked example of an entry's self-description being false while the fix was
  right; do not re-litigate the defect claims.

### From prompt 6 (2026-08-01) — your item 5 is now concrete: ONE package, ONE tier decision, and two things you must NOT package

**Read `BUG_LIST_AUDIT.md` §10 before item 5.** It is new, and it contradicts
§9 twice. Full trails are on the BUGS entries.

#### 5a. ⭐ ONE NEW PACKAGE: **F90** (was C04) — dust storms break underground cables/pipes

Filed as an F-row because the sweep closed the chain with no gaps, not because
anyone decided anything. **Nothing built. The defect claim and the intent tells
are done for you; the tier, the §4a answer and the fix shape are yours.**

- The whole chain, and both intent tells, are on the **F90** entry with
  file:line. Short version: `City:HourlyUpdate` gates the break pass on
  `HasDustStorm`, which is hard-wired to `MainMap`, then hands it a fragment
  list containing the elevator-merged cross-map fragment; the victim is picked
  by `table.rand` over every connector in it. The sibling production pass
  sixteen lines above **does** guard the shared-fragment case, with a comment
  saying fragments span cities.
- **The hard part is the SHAPE, and it is a genuine FIX_POLICY §3a problem.**
  The bad line is `SupplyGrid.lua:677`, mid-function, behind the roll — a
  wrapper cannot reach it without re-implementing the roll, and a body copy is
  what F86 constrains. Two layer-2 candidates are named on the entry; the
  cheaper-looking one is vetoing an off-`MainMap` `BreakableSupplyGridElement
  :Break` during a dust storm rather than touching the picker at all. **Weigh
  that before defaulting to a replacement** — GromGor's working fix IS a body
  replacement, and copying his shape would walk straight into §3a.
- **Two scope questions are flagged on the entry, not decided.** The merged
  element count also inflates the *surface* break rate (`IsBreakable` :695 and
  the probability at :673 both count underground elements) — that is an intent
  question, and it may not be a defect at all. And GromGor's version would
  index a nil element on an empty surface list; ours must guard rather than
  inherit the shape.

#### 5b. ⚠️ A TIER DECISION YOU OWN THAT IS NOT A CANDIDATE PACKAGE: **F04**

**The audit's §9 demotion of F04 (GOLD → BRONZE-B2) rested on C32 being the
better mechanism match, and the sweep took that reasoning apart.** C32 has no
route in current Src; the specific inference that carried the reassignment —
"an asteroid leaving range fits label rebuilds on map transitions" — is **false
of Src**, there is no label rebuild on a map transition; and the observable
that made C32 look real (GromGor's fix firing in the wild) fires on
destroyed-but-unrebuilt buildings, which is not a defect. Separately, the
onset condition the reporter named cannot occur unattended on 1.0.7 at all.

**This is yours because it is a decision, and the sweep deliberately did not
make it.** The three live options are written out on the F04 entry: restore
its witness and tier, leave both entries witness-less, or hold for the
corrected live rider. **The limit that constrains all three:** the sweep read
1.0.7 only and the thread's reports are 1.0.6-era, so source alone does not
discriminate the two mechanisms *for that reporter's build*. **F04's own defect
claim is untouched and stands on its sibling tell either way — do not
re-litigate it.**

#### 5c. Two things that must NOT become packages

- **C32 — DOWNGRADED, not closed, and not a package.** No route in current Src;
  no F-row; no fix. It keeps its row as history. Your scope fence already says
  a candidate left without settled evidence stays a candidate — this is that.
  (The live rider that could still settle it was **rewritten**, not deleted:
  its old trigger no longer occurs unattended and its old "any non-zero count
  is the defect" rule would have confirmed C32 on the first meteor strike.
  Corrected row in `PLAYTEST_CHECKLIST.md` §6.)
- **C35 (new) — a real gap, an unproven harm, explicitly NOT for you.** The
  fredware-#11 comparison found zero overlap with F67/F68/F70/F71 and located
  a clean sibling asymmetry (the payload path tears down the command-centre
  connection with no wait where the takeoff path waits). But nobody has shown
  a unit stranding, fredware ships it beta and off by default, and his remedy
  removes a player action — a §4 behaviour change, not a repair. **It needs a
  live repro first**, named on the C35 entry. Packaging it today would be
  packaging a description.

#### 5d. LATE ADDITION (same day) — a possible LIVE symptom for your item 1 (C33)

**The owner ran the audit's logged-in Paradox browse on 2026-08-01** (results in
`BUG_LIST_AUDIT.md` §10.4). One thing it surfaced belongs to **your C33
package**, and it is recorded on the C33 entry as a **lead, not evidence**:

> "Cannot add trains to tracks" — *"I redid my entire train network with large
> train stations, and now I cannot assign trains to either track… I check the
> track and it says 0/10 trains. I have 7 trains in my inventory, but still
> can't assign any to the tracks."*

**Why it may be yours.** The reporter *has* trains, so this is not F64's
counter-at-zero failure — it is the opposite. What preceded it was a **mass
track redo**, i.e. the `DemolishAndSplitTrack` path, and what is broken is the
**track's** ability to accept an assignment. A persisted `TrackBase` shell with
`elements`/`assigned_vehicles` emptied to `false` is a candidate explanation for
a track reporting `0/10` and silently swallowing the click.

**⚠️ Do NOT put this in the package as a witness yet.** Its **provenance is not
established** — it was seen as an in-game Bug Report dialog (over a *"Sending
bug report failed: 500"*), not a forum thread, so there is no author, date or
build, and it may never have reached Paradox. The chain is also untraced, and
F80's enumeration suspicion could produce the same surface. **The cheap move
that would settle it is a source question you are already in the file for:
trace what `assign train to track` checks, and whether a shell-state
`TrackBase` fails it silently.** If it does, C33 gains a real player-visible
symptom and its reachability tier changes. If it doesn't, drop the lead.

#### 5e. Two witness upgrades that touch your tier work (bookkeeping, not decisions)

Both from the same browse; neither changes code, both were already shipped and
tested. **F01's** witness is found (May 8 2026, Game Version **1.0.7**, with
repro steps) — the audit's "NOT re-derivable" is retracted. **F74's**
rival-rocket report is found **twice from the same reporter** (OG Sep 5 2022,
overflow trigger; Relaunched **May 2 2026 on 1.07**, halt-mid-load trigger),
both ending in a permanently bricked rocket — **primary evidence now supersedes
the paraphrase-grade 1.0.7 dev note**, and the honest reading is that the note
covers one trigger while a player on 1.07 hit the other. If any of your tier
derivations lean on the audit's witness grades for these two, use §10.4 instead.

#### Housekeeping that lands on you

- **F35 needs nothing from you.** Its live half was measured by prompt 2 and
  its source half re-checked here; scope confirmed both ways, no F-row, no
  extension. Item 5's "F35 extension?" question is answered: no.
- **STATUS's index count was stale by two rows again** and has been re-derived
  by counting (now **102 rows = 90 F + 12 D**, plus **35 C**). If your packages
  file or close anything, re-derive it the same way rather than incrementing.

---

### From prompt 6b (2026-08-02) — the residual C-sweeps

Full trails on every BUGS entry named here; the audit's running record is
`BUG_LIST_AUDIT.md` §10.8.

#### 6b-1. C38 — a NEW verified defect, filed by the C18 sweep, decision is yours

**C18 itself is CLOSED `wontfix — intent`** (no promise broken; the label
system is exact-string and the tech names its four buildings) — nothing for
you there. But the intent question sent the sweep looking for a positive
statement of what "all extractors" means to this game, and it found one that
does not keep its own promise:

**The Astrogeologist commander profile promises an unqualified "Extractor
production increased by 10%" and enumerates ten labels, missing
`AutomaticMetalsExtractor` and `MicroGAutoWaterExtractor`** —
`Data\CommanderProfilePreset.lua:333,:336-385`. Both are buildable, both carry
the exact prop being modified, and the two hidden legacy templates are already
excluded from the count (10 of 12, not 10 of 14).

**Why it is yours and not built here:** the harm is a silent 10% shortfall on
two buildings under one commander profile — verified, but small, and "repair
the omission" vs "leave a balance number alone" is a §4 call. If it passes,
the shape is data (two `Effect_ModifyLabel` entries, or moving the water entry
to the shared `object_class` label `WaterExtractorBase`), not a code patch.

#### 6b-2. C21 (St. Elmo sinkholes) — destruction route VERIFIED, promoted to you

The audit left this as "whether the meteor damage path can still hit them is
unchecked". It is checked now and the answer is yes, end to end:

Sinkhole carries neither `indestructible` nor `disasters_strike_immunity`
(`Sinkhole.generated.lua:1-24`; both default false), a large meteor's query and
filter both pass it (`Meteors.lua:405-409,:393-399`), the building branch
excludes only Dome and ConstructionSite (`:817-825`), and
`DestroyBuildingImmediate`'s only guard is the flag it does not have
(`Building.lua:1371-1374`) -> `DoneObject` (`Demolishable.lua:132-141`).

**The tell is as clean as this project gets:** every other mystery set-piece in
the game carries `indestructible = true` - Crystals, Monolith, MirrorSphere,
CaveOfWonders, JumboCave, ArkPod, MartianAssembly, BottomlessPit - and the
property's own help text names meteors. Sinkhole is the only one missing it.

**What you are deciding is the soft-lock, and it is LOCATED, not proven.**
Best route is `Mystery 11.generated.lua:146`: `_sinkhole:GetMap()` with no
`IsValid` guard, on a persisted register, on the Trigger sequence, in a window
that stays open until the player scans the first anomaly. The label-count gate
at `:214` is the weaker route because the repeater keeps respawning until
count > 9 (`:689-704`) - say so if you package it, do not lead with it.

**Ruled out, so you do not re-derive it:** the anomalies are safe.
`SubsurfaceAnomaly` is not a Building and matches none of the meteor query's
classes, so no scan stage can be broken by losing an anomaly.

**Package shape if it passes §4:** the minimal repair is the flag the whole
rest of the game already uses on set-pieces, not a wrapper on the meteor path.
Weigh that a flag change alters vanilla data rather than patching a method.

---

### From 6c (2026-08-02) — one new package for you, and two method facts that will change how you read the others

6c ran the last three of 6b's jobs: the five SkiRich OG candidates (C26-C30),
the F82 trace, and the F80 source audit. **It filed nothing and promoted one
thing.** Counts unchanged and re-derived: 102 rows (90 F + 12 D), 38 C.

#### ⭐ Your new package: F82 (split-grid notification)

**The trace is DONE and the mechanism is source-verified**, so this arrives as
a decision, not an investigation. The notification has **no removal path at
all** — `Lua\SupplyGrid.lua:1626-1629` is the only reference to
`PowerGridSplit`/`LifeSupportGridSplit` in the whole tree — and what it
registers is `self:GetPos()`, a **position, not the grid**, so a rejoin is not
an input to it in any sense. It clears only by the preset's
`Expiration = 120000` with `GameTime = false`, and `Notifications.lua:188-217`
runs that branch on a **real-time** thread: **2 real minutes, independent of
game speed and of whether anything was repaired.** Sibling tell: `PowerLeak`
and `LifeSupportLeak`, children of the same two parents in the same preset
file, carry **no `Expiration`** and are cleared by state.

**Two things to weigh that the original entry did not have:**

1. ⚠️ **The symmetric half is arguably the worse one and it was never
   reported**: an **unrepaired** split also stops being reported after 2 real
   minutes. The entry is filed P3 on the lingering half alone; the vanishing
   half may argue for P2. That is a severity call, and it is yours.
2. **The repair shape is a genuine design question, which is why 6c built
   nothing.** A `RemoveObjectFromNotification` heal needs a **key**, and the
   notification is keyed by the break *position* — a rejoin does not happen at
   a known position, so there is no key to match on without either tracking
   split→rejoin pairs ourselves or clearing the whole notification. Decide the
   key before deciding the fix.

✅⭐ **UPDATE, SAME DAY: THE RIDER LANDED AND IT PASSED. This package is
measured, not inferred — you are not gambling on a source read.** Owner at the
keyboard, No-Disasters save so nothing but the player could break a cable, grid
deliberately left **unrepaired**, console watcher timing both clocks:

| leg | speed | real ms | game ms |
|---|---|---|---|
| 1 | 5x (retail max) | **119 999** | 600 000 |
| 2 | 1x | **120 001** | 120 000 |

Against a preset `Expiration = 120000`: **real time constant to within 2 ms
across a 5x speed change, while game time varies by exactly 5.000x.** No
state-cleared notification can behave that way. **And because both legs left the
split unrepaired and the notification vanished regardless, the symmetric half —
the colony stops reporting a break that is still there — is now an observed
fact, so the P3-vs-P2 call is yours to make on data.**

⚠️ **One figure in the entry was corrected by that run and it may matter to you
elsewhere:** the fastest *player-reachable* speed is **5x**, not the 20x that
`const.ultraGameSpeed` advertises — `"ultra"` is `Platform.debug`-gated
(`Lua\X\HUD.lua:462-467`, `:481-487`). It is now an `ENGINE_FACTS.md` entry,
because any real-time-vs-game-time arithmetic in this project inherits it.

#### ⚠️ Method fact 1 — the label rule you inherited from 6b is WRONG as written, and 6c corrected it in three places

6b recorded, under C18: *"No parent class ever contributes a label."* **That is
false.** `AddToCityLabels` is a **combined method** —
`DefineCombinedMethod("AddToCityLabels", "call")` (`Lua\CityObject.lua:8`,
machinery `CommonLua\Core\classes.lua:1499-1511`) — so **every** parent
implementation runs, and parents really do contribute labels
(`ResourceExploiter`, `ResourceProducer`, `DroneControl`, `Frozen`, and for
units `Unit`/`Rover`/`self.class`). C18's *verdict* is unaffected and the
reason is recorded on its entry: every parent-contributed label is a **role**
name, never a **building-type** name, and XenoExtraction names four
building-type labels. **The corrected rule is now in `ENGINE_FACTS.md`** along
with the fact that `City:AddToLabel` forwards to the **colony** container first
(`Lua\City.lua:83-86`) — which is where `Effect_ModifyLabel` writes — so "the
tech was researched before the unit existed" is **not** a way for a label
modifier to miss. Read the corrected version before you use the label argument
in any C22/C38 package.

#### ⭐ Method fact 2 — three of the four closes turned on the same shape, and it will recur in your packages

**C27, C28 and C30 all looked like "the missing code" from outside and all
three had the code present, written somewhere other than where the symptom
points.** Signal Boosters commits the extender's new radius through the *hub's*
`Effect_Code` (the hub's forced reconnect recurses into `linked_extenders` and
re-reads their live `work_radius`). Supply-pod pins survive a generic path that
genuinely would strand them — `PinnableObject:Done` unpins **without force**
while `RocketBase:CanBeUnpinned()` returns false unconditionally — only because
every affected class force-unpins in its **own** `Done`. **Before you grade any
package on "the vanilla code for X is missing", check whether X is done by the
neighbour, the parent, or the caller.** 6c's five sweeps went 4-0 against that
reading.

Related engine fact now recorded because it decided C30: **`Init` and `Done`
are combined with OPPOSITE order** — `Init` is `procall` (parents first),
`Done` is `procall_parents_last` (**most-derived first**),
`CommonLua\PropertyObject.lua:1663-1664`. Reading either `Done` alone gives the
wrong answer. And a rule that binds anything **we** ever make pinnable: it must
force-unpin in its own `Done`, because `map.pinned` is a `MapVar` and a leaked
entry is saved into the player's game.

#### Not for you, recorded so you do not pick them up

- **C26 stays `cand`, CANNOT DETERMINE.** The engine ships two savegame heals
  named for exactly the symptom (`RequiresMaintenance.lua:531-566`, `:568-574`)
  but `AppliedSavegameFixups` is pre-seeded at new-game
  (`CommonLua\SavegameFixup.lua:10-16`), so they never run on a save started on
  our build — **presence in Src is not reachability in this save, the same gate
  C25 hit.** No producer found; both obvious guesses are checked and written
  down. Next step is a console dump on a loaded save, which is playtest work,
  not chain work. **Do not package it.**
- **F80 stays `investigating`.** The audit gave it an exact predicate —
  `traverse_dir = next_idx - start_idx` is never normalised to ±1
  (`TrainTransport.lua:374`) and a stride ≠ ±1 hits a missing `link_edge` and
  **hard-returns** (`:417`), silently dropping the tail — and it explains
  **both** public symptoms from one function (waits via `Train.lua:882`, walks
  via `Station:GetReachableStations`). But **the trigger is not proven**, so it
  is not a package. ⚠️ If a fix is ever written here: `ForEachStationAlongTrack`
  is **not re-entrant** (`stations_visited` is one shared file-local table,
  `:365`, `:386-390`), so our callback must never enumerate.

### From the 2026-08-02 blind-audit review — one inheritance guard for package 0

`docs/reports/BLIND_AUDIT.md` §7 grades F29(a) *"a Mod-Editor sequence action
with no shipped user."* **That is the known-false self-description** — the
reachability audit enumerated FOUR live shipped callers in Mystery 2, and §4a
uses F29 as its worked example of exactly this trap. If you read the blind
audit while working package 0 (F29/F57(a)), do not inherit its provenance
reasoning; its latency conclusion happens to match the record anyway. The full
merit review of that report is chain prompt 12's job 6b, not yours.
