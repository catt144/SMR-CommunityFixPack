# Manual Playtest Checklist — Relaunched Fix Pack

## Must_Read_Header
<!-- RULES -->
Rule: Keep this file limited to playtest work items and put reusable agent procedures in their task-specific `docs/agent/` home. [A3: pass]
Rule: Move each completed test or settled decision body to `archive/PLAYTEST_ARCHIVE.md` while leaving its heading, marker, and pointer. [A3: pass]
Rule: Move dated session records to `archive/SESSION_LOG.md`. [A3: pass]
<!-- /RULES -->

This is the owner's work list for tests run in the retail game with a live agent session.
Item 177 records the still-open question of mechanically enforcing checklist markers.

> Redesigned 2026-08-03 (`docs/agent/prompts/PT_REDESIGN_PROMPT.md`, owner
> design authority of the same date): tests grouped **by system, not by PT
> number** — a sitting clears a group — and each test reduced to
> **Bug / Requirements / Setup / Good to have** (Requirements: the at-a-glance
> save/colony line, owner amendment at the checkpoint). PT codes are unchanged;
> numbering is identity, grouping is order. The full pre-redesign text,
> recorded results included, is in the archive under the "pre-redesign
> snapshot 2026-08-03" banner.

> ✅✅ **The 2026-08-11 "BOTH TICKS DONE" block (Mod-Manager re-enable + Steam
> Cloud untick) is CLOSED and moved WHOLE to `archive/PLAYTEST_ARCHIVE.md`.**
> The audit confirmed the second tick stuck: **two** post-untick launches
> restored nothing, every directory change reconciles by name (59 saves, all
> named, none of the 14 strays back), and the "never say gone" rule is formally
> retired. Nothing here is owed from you.

## Decisions waiting on you

### 2026-09-16 — 191 CLOSED: C93 passed attended — affected save reloaded, no food stuck
<!-- ck:191 status:closed owner:no -->

✅⚖️ **CLOSED 2026-09-16 on your word:** *"c93 tested i re loaded it and watched it end to end no food stuck"*. **MEASURED:** `OpenPastureStockpiles: applied`, then on load `restored 2 open ranch(es), explicitly reattached 6 pile(s)` and `restored 4 open ranch(es), explicitly reattached 12 pile(s)` (`Mars.exe-20260916-16.47.23-6a91a190.log`, repeated on reload in `16.57.56`). C93 is `tested-attended`. ⛔ Declared limits, not hidden passes: Leg B (a newly built ranch) was not stated and no numeric pile reconciliation was read; the acceptance rests on your attended watch. The HasSpot flood in the reload log is the reporter save's twelve missing mods, by your attribution — not ours, not investigated.

**Why:** the owner identified the missing timing condition: Outside Ranches work before the
Open Domes law and fail after it. Source now joins that timing to the ranch's entity swap, and
`Fix_OpenPastureStockpiles` is built to keep the nine-anchor entity and recover existing piles.
The build is desk-verified only; this is its one required attended window.

**Requirements:** the already-affected save used for C93 diagnosis, with Open Domes active;
enough space/resources to construct one additional Outside Ranch; one completed production
cycle. The temporary reader is agent-side. Do not share the window with an unrelated invasive
probe.

**Leg A — affected save:**

1. Load the affected save with the new module active. The log must say
   `OpenPastureStockpiles: applied` and report the restored ranch count.
2. Confirm each ranch remains functional with nine unique pile objects, all attached to named
   `Resourcepile1`–`Resourcepile9` spots and zero at `Origin`.
3. Reconcile the previously stranded ranch's total and per-resource amounts before/after the
   repair read. No Food, Meat or other output may disappear.
4. Let drones collect the formerly stranded output, then save/reload. All nine anchors must
   remain valid and no centre pile may return.

**Leg B — prevention:** while Open Domes remains active, construct a new Outside Ranch, let it
complete a production cycle, and confirm the same nine-named/zero-Origin shape with successful
drone pickup. The closed ranch visual is the repair's declared tradeoff, not a failure.

**Pass:** both legs, resource reconciliation exact, zero C93/module Lua errors. **Status ceiling
before this runs:** `fixed`; this item alone can grant `tested-attended`.

### ✅ 2026-09-16 — 190 RULED: C93 diagnosis excludes the mall-mod targets
<!-- ck:190 status:ruled owner:no -->

Owner ruling archived in [C93 diagnosis scope](archive/PLAYTEST_ARCHIVE.md#c93-diagnosis-scope-2026-09-16).
The ranch result is in [C93's diagnosis report](agent/reports/C93_RANCH_ORIGIN_DIAGNOSIS.md);
no further in-game diagnostic window is owed for this fired brief.

### 2026-09-16 — 188: PLAYTEST RIDER, ready to run — does a FRESH 1.1.0 Wildfire colony show a researchable cure?
<!-- ck:188 status:open owner:yes -->

⚖️ **This is the only route left to Jäger's report.** F120 is pulled (187) and could never have
explained it; the desk is exhausted. What is left is a live look, and it is cheap. **Take it at the
next sitting, or say drop it and the report closes as unexplained.**

**The question:** on a colony started on 1.1.0, does the shipped reveal put a cure node in the tech
tree that a player can find and buy? If yes, the reporter's cause is finding it, not having it, and
the answer is a reply. If no, we have a live defect worth building against.

⭐ **The lead the audit found, and the reason the look matters.** The tree has two sections, MAIN and
SPECIAL. The SPECIAL button centres on a hidden spacer tech at MapPos **(2366, 4480)**. Breakthroughs
occupy y **1920-4480**; the mystery techs are a separate band at y **4736-6272**, and the cure chain
runs at y **5504**, x **3846 → 5474**. So SPECIAL lands you on the breakthroughs with the cure row
about **1000 below and 1500-3100 to the right**. Whether it is on screen is a function of zoom and
resolution — ⛔ **source cannot answer it and neither can the desk.** (`Lua/TechTree.lua:1-14`,
`Lua/XDef/XTechTree.generated.lua:715-748`, MapPos measured from `Data/Tech.lua`.)

⭐ **Two things that may make this a one-line reply instead of a fix.** The tree has a **search**:
`Ctrl-F`, fuzzy over name and description (`XTechTree.generated.lua:827-843`). All **eleven** chain
nodes are named **"Wildfire Cure"** with the same icon, so a search must find it. And the reveal
raises a **TechDiscovered notification** for non-breakthrough techs (`Lua/Research.lua:854-859`).

#### Leg A — five minutes, any save, settles the main question

⚠️ **Do this on a scratch copy.** `CheatStartMystery` writes `FinishedMysteries` into `account.dat`
if a mystery is already running, and cheats taint the save lineage.

1. Open the console (SMRTK **Kit** page → **Open console**).
2. Read where you stand — paste as one line:

```
print(UIColony.mystery_id, GetTechState("WildfireCure_1", UIPlayer), UIPlayer.TechPoints)
```

3. Only if `mystery_id` is not already `TheMarsBug`:

```
CheatStartMystery("TheMarsBug")
```

4. Run **the exact line the scenario runs** (`Mystery 8.generated.lua:145`):

```
SA_RevealTech.SAExec{tech = "WildfireCure", cost = 90000}
```

5. Read back all eleven nodes:

```
for i = 0, 10 do local id = i == 0 and "WildfireCure" or ("WildfireCure_" .. i) print(id, GetTechState(id, UIPlayer), UIPlayer:CanResearch(id)) end
```

**First-screen witness:** line `WildfireCure_1` reads `enabled` and `true` (with a tech point spare);
the other ten read `hidden`.

6. ⭐ **The measurement.** Open the tech tree, click **SPECIAL**, and **do not pan or zoom**.
   **Screenshot what is on screen.** Then press `Ctrl-F`, type `Wildfire`, and screenshot again.

**What each outcome means**
- Node reads `enabled` **and** is visible after clicking SPECIAL without panning ⇒ the fresh path is
  healthy; the reporter's problem is elsewhere (stage, or they looked before the reveal).
- Node reads `enabled` but is **off screen** until you pan ⇒ ⭐ **that is very likely the report**, and
  the deliverable is a reply ("SPECIAL section, scroll right/down, or Ctrl-F Wildfire"), not a fix.
- Node does **not** read `enabled` ⇒ a live defect the desk missed. File it and stop; that is a new
  entry, not F120.

#### Leg B — only if Leg A comes back healthy, and only if you want it

Play the mystery to its own reveal instead of calling it. The Trigger gates are, in order
(`Mystery 8.generated.lua:38-148`): **100 colonists** (`CheatSpawnNColonists(100)`; stand in a dome or
it scatters them outside), ~1-2 Sols, **an anomaly that must be scanned by a rover**, a message, 5-10
Sols, the Infected trait, then ~3-4 hours to the reveal. Cheat past the colonist gate, then play at
speed. ⛔ This tests the **timing** story only; Leg A already tested the reveal itself.

#### Recording

Screenshots to `C:\Dev\SMR-ScreenCaptures\`, then `python tools/store_screenshots.py`. The console
lines and their output go in the entry. ⛔ Whatever it shows, **do not ask the reporter for a save**
(ruling 2026-09-15).

### 2026-09-16 — 189 CLOSED: C95 re-point passed attended; optional transports stay desk-only
<!-- ck:189 status:closed owner:no -->

**MEASURED with you at the keyboard:** clean boot, `HabitatExpeditionDraft: applied`,
and `CrewDraft` armed before assignment. The live trace fired on
`UniversalZeusRocket(1053)` through `CargoTransporterNew`: all **5** Naturalist
Habitat residents were present in the eligible pre-fix busy/unemployed bucket,
none appeared in the returned crew, and the picker filled **5/5** from ordinary
dome residents. You pinned the habitat residents and read **5 before → 5 after**;
the expedition departed. Whole-log scan: **0 error-shaped lines**. Evidence:
[sitting report](agent/reports/C95_SITTING_20260916.md) ·
[archived log](archive/logs/c95_repoint_Mars.exe-20260916-12.45.56-6a91a190.log).

**Your ruling after the pass:** *"we will mark those as desk verified and not play
tested and we won't be playtesting unless we get a reported issue. We have too many
other things on deck right now."* Condition: the save has neither an asteroid lander
nor a space elevator available, and the core automatic-draft repair just passed.
⇒ The lander/elevator player-choice controls remain **desk-verified, not playtested**;
they reopen only on a reported issue. Nothing from that pair is owed to you.

**Declared limits, not hidden passes:** this fixture has no Micro-G habitat; live
pack-removal/load and the deliberate-shortage EF-104 panel reading were not run.
Desk evidence covers both habitat classes, lander/elevator non-interference, exact
global restoration, scarcity and removal of the wrapper. C95 is `tested-attended`
for its player-visible automatic-draft repair; release remains separate.

### 2026-09-16 — 188: habitat residents walk out on their own. Defect, or the cost of the building?
<!-- ck:188 status:open owner:yes -->

**Your observation, from your own C95 sitting:** Dermot rode the rail back into the Naturalist
Habitat and then **left again a few hours later** for `Fuller #1`, once he had an apartment and a
job there — *"which from my understanding is not what people living in habitats are supposed to
want to do."*

**What the source says, filed as [C100](agent/bugs/C100.md).** The emigration scorer runs for every
colonist on a heavy-update tick. It normally needs a destination to beat the current community's
score — but there is an override: a colonist with **no job** moves to the first reachable community
offering a free apartment **and** a free job, with **no score margin required**. And a habitat
forbids connected work by design, so its residents are structurally jobless. ⇒ **the habitat's
defining rule is what supplies the trigger that empties it.**

**The question, and only you can answer it.** Habitat residency is explicitly score-gated and
re-evaluated in vanilla, so the game does contemplate people moving out. Is this an oversight —
the same shape as C95, where one system's deliberate rule is not honoured by another — or is it
the intended price of a building that cuts its residents off from the colony?

⛔ **Nothing is authored and nothing is classified until you say.** ⚠️ This does **not** change
C95's ruled repair; that one stops the expedition draft and is unaffected either way. If you rule
it a defect, C100 rises from P3 and needs its own shape decision.

⭐ **One cheap thing to watch next time you are in that colony, before ruling:** does a habitat
resident **with** a job (an outside workplace near the habitat) stay put while a jobless one
leaves? If a working resident also walks out, C100's mechanism is wrong and the entry says so.

### ✅ 2026-09-16 — 187 RULED: F120 is PULLED from the ship set — built, audited, held
<!-- ck:187 status:ruled owner:no -->

Your words: *"Pull it from the ship set, the only relatively minor use we get is the evidence
you gather."* Your reasoning, recorded: the fix repairs only a colony started on 1.0.7 and
loaded past the old-save gate; Steam (about 75% of subscribers) refuses that load, console
cannot do it, and only a PC copy bought from the Paradox store could — a fix nobody you can
name will use, and untestable here because your copy is Steam. The audit that preceded the
ruling had widened it from the cure to all 17 legacy mystery technologies (85/85 desk) and
settled that it never reached Jäger's Steam report, which stays open.

**Done the same sitting:** module moved to `tools/held/Fix_MysteryTechMigration.lua`
(excluded from the pack, registered nowhere), F120 parked, release-ledger row withdrawn,
handoff updated. **Reopen condition:** a report of a lost mystery technology on a
carried-over 1.0.7 colony from a platform that offers Load anyway — one commit from live.
You also questioned whether two frontier models on the investigation and the audit were
worth it for this reach; the lesson (check who can reach the affected state before building)
is recorded in memory, not as policy. Record: [F120](agent/bugs/F120.md),
[audit section](agent/reports/WILDFIRE_CURE_RESEARCH.md#cross-vendor-audit--2026-09-16-fired-on-fable-promptsf120_auditmd-consumed).

### 2026-09-16 — Do not build a fix for a version players cannot play
<!-- ck:- status:closed owner:no -->

Owner ruling archived in [Do not build a fix for a version players cannot play](archive/PLAYTEST_ARCHIVE.md#do-not-build-a-fix-for-a-version-players-cannot-play-2026-09-16). Landed as a header rule in `agent/FIX_POLICY.md` and as item 11 of the `prompt-authoring` skill.

### 2026-09-16 — A successful fix includes recovery of affected saves
<!-- ck:- status:closed owner:no -->

Owner requirement archived in [Affected-save recovery requirement](archive/PLAYTEST_ARCHIVE.md#affected-save-recovery-requirement-2026-09-16). Applies to F120 and future bug fixes; prevention alone does not satisfy it.

### 2026-09-16 — Wildfire investigation authorised during prompt teardown
<!-- ck:- status:closed owner:no -->

Owner ruling archived in [Wildfire investigation override](archive/PLAYTEST_ARCHIVE.md#wildfire-investigation-override-2026-09-16).

### 2026-09-15 — Complete STATE admission door installed
<!-- ck:- status:closed owner:no -->

Body archived in [STATE admission door installation](archive/PLAYTEST_ARCHIVE.md#state-admission-door-installation-2026-09-15).

### 2026-09-15 — STATE cleanup scope override
<!-- ck:- status:closed owner:no -->

Body archived in [STATE cleanup scope override](archive/PLAYTEST_ARCHIVE.md#state-cleanup-scope-override--2026-09-15).

### 186: choose skill caps after the documentation skills first cut
<!-- ck:186 status:open owner:yes -->

2026-09-15, requested by the documentation-skills brief: the new `doc-editing`
and `prompt-authoring` skills fit the 3,072 B design target. Measured at
`5245727` with `python tools/doccheck.py` (SKILLS section): doc-editing 2,461 B;
prompt-authoring 2,912 B; smr-bug-library 3,622 B; smr-orientation 3,248 B;
smr-session-close 4,490 B. These are complete LF-normalized SKILL.md sizes.

**Proposed, not set:** common warning **3,072 B**, hard limit **5,120 B**. Keep
pressure to review the larger existing skills while allowing the current
session-close procedure without deleting obligations just to restore a cap.
The later attended skills/rules audit judges the contents; the thresholds and
restoration remain yours. Caps are still down. Evidence and revisit criteria:
[documentation skills report](agent/reports/DOC_EDITING_SKILLS_AUDIT.md).

### 2026-09-15 — 185: C95 built; C96 passed attended — launch and return

<!-- ck:185 status:ruled owner:yes -->

✅⚖️ **RULED IN PART 2026-09-16 — (a) C95 is AUTHORISED to build and test.** Your words: *"can you
rewrite the c95 build I want to fire it and then we can test it, already have the test ready in a
save."* The build is now recorded in [the C95 report](agent/reports/C95_HABITAT_DRAFT_BUILD.md),
with the game acceptance recipe at **189**. It carries the design you worked out — the predicate
keys on `MicroGHabitatBase` (covers both habitats), and the hook wraps the per-bucket filter **only
for the duration of the picker call**, which is what keeps the lander and the space elevator out of
it. ⛔ **Build and test only** — the shipping *shape* was already ruled (main pack, with the mark),
but the release itself goes through the normal release path, not that brief.

⚖️⭐ **RULED IN PART AGAIN 2026-09-16 — (b) C96's REPAIR IS NOW AUTHORED, on your word:
*"Go ahead and author the fix"*.** ⛔ That **lifted your own 09-15 playtest-first hold** quoted
below; the lift is yours, not an agent deciding the gate had lapsed. **BUILT the same day:**
`Code/Fix_RoverSubclassManifest.lua`, 22 desk legs falsified with three mutants,
[build report](agent/reports/C96_ROVER_SUBCLASS_BUILD.md).
**The original desk pass preceded the live test; the live test subsequently FAILED.** The ESA
fixture is provisioned. The module attempts both transporter paths and cargo accounting, but
those design claims do not establish that it works. Current diagnosis follows the ship ruling.

⚖️⭐ **BOTH REMAINING CALLS RULED 2026-09-16 — C96 SHIPS IN v11, and the fixture is being
provisioned now.** Your words, asked whether C96's module should ride v11 or be pulled because it had
never run in a game: *"Both of those, and both of the ones we are setting up to test right now are the
planned fixes."* ⇒ `Fix_RoverSubclassManifest` stays registered (`items.lua`, `Code/`), and C93's
`Fix_OpenPastureStockpiles` ships with it (its validation is **191**). ⛔ **This closes (b)'s "whether it
ships" call; it does NOT assert either fix has been witnessed in play** — both are under test today and
the acceptance legs stay owed at **191** and in the C96 build report. A ship decision is not a test result.

**C96 follow-up, 2026-09-16:** its original repair failed on the Seeker-only ESA/Wildfire
fixture. The exact-name probe then returned `RCSensor list: 1 | city same: true | connected label: 1`.
The cause was the installer targeting old/empty built-class tables instead of the definitions
used by the next class build. The earlier function-equality check had been misinterpreted.

**Owner authority in this session:** "You are clear to handle this in any way explore or look
at any file, rewirte any part of it you want". Condition: you were juggling multiple tasks and
explicitly removed restrictions from the agent-authored C96 brief. Design and implementation
may proceed without another approval stop. The earlier v11 ship ruling remains recorded.

**Repaired at the desk:** install on definitions; include subclasses in availability and busy
warnings; reserve stricter manifest requests; record a loaded Seeker as Seeker cargo. The
fulfilled Commander request transfers to that Seeker line, so native return/unload handling
cannot spawn an extra Commander. Native city labels stay intact. **MEASURED:** 55 legs pass;
the old module fails the new loading-order regression. [Evidence](agent/reports/C96_ROVER_SUBCLASS_BUILD.md).
**Attended result at `efebdf7`, retail 1.1.0.403908:** rocket `1051` launched toward an anomaly
requiring Commander with the original Seeker `2000000261` aboard. The cargo line correctly
recorded Seeker 1/1 and Commander 0/0. Your return observation: "Done and its still a seeker
and looks correct".

✅⚖️ **ACCEPTED ATTENDED 2026-09-16 on your return count — no rerun, your ruling.** Your words:
*"I am not re running a test ... the rocket came back I had a seek when it came out, I only ever
had one seeker and I had zero while it was gone."* ⇒ one Seeker before, none while away, the same
single Seeker back — no duplicate. **C96 is `tested-attended`.** ⛔ The prepared numeric
`C96 RETURN` probe was never run (no such line in any 2026-09-16 log); the acceptance rests on your
attended count, not a probe figure, and you declined the rerun. The C96 brief is consumed. Live
pack removal/reload stays unclaimed. Your solar-panel variant question is also answered:
RC Generator (`RCSolar`) is covered and desk-verified on both receivers, but has not flown here.

⛔ **(b)'s ORIGINAL TEXT, kept because the ruling above amends it rather than replacing the
record:** C96 was still open and nothing about it was authorised by the C95 lift.

⚖️ **You ruled both of these on 2026-09-15 and both rulings are recorded here because an
agent-doc-only record is not considered asked (rule 5 / R10).** Each entry carries the evidence,
the controls and the reasoning; ⛔ this item is the decision, not a retelling.

**Both were `filed` with their repair NOT written, on your instruction** (*"file it as a fix
that needs playtesting then. Don't author the fix yet"*) — ⭐ **superseded for C95 by the 09-16
ruling above; it still stands for C96.**

**(a) [C95](agent/bugs/C95.md) — the game takes Naturalist Habitat residents on expeditions
without asking and cannot bring them home.** ⭐ **Reproduced in play with you at the keyboard**,
2026-09-15: two residents taken, neither returned, both re-homed into a dome; one rode the rail
back unaided, proving the habitat was reachable the whole time. A returnee who picks up a job
elsewhere never comes back, so a habitat drains one resident per expedition, silently.
⚖️ **You ruled the repair shape:** exclude habitat residents from the expedition draft, rather
than teach the return path about habitats. ⚖️ **And its classification, settled with you:** an
**oversight bug solved by a judgment call** — it ships in the **main pack with the judgment-call
mark** and its reasoning on the fix list, ⛔ **not** as an opt-in module. Precedent is C89.
⛔ **Scope, load-bearing:** nothing becomes ineligible — you can still move a resident into a dome,
and still hand-pick them for an asteroid lander (verified). It subtracts from one automatic picker.

**(b) [C96](agent/bugs/C96.md) — a rover's own subclass never satisfies a requirement for its
base class**, so an RC Seeker is refused where an RC Commander is asked for. ⛔ **The obvious
one-token repair is VACUOUS** — a rover registers only under its leaf class, so the Commander list
never held a Seeker for the filter to discard; a real repair must widen the source list too.
⚠️ **Its playtest needs an ESA colony or the leg is vacuous** (the Seeker is sponsor-locked), and
`EF-079` branch-locks the fixture library, so cost that before scheduling it. The unlocked
`RCSolar` variant may be a cheaper fixture and is worth checking first.

**What is actually waiting on you, and they are independent:**
1. **(a)'s build is authorized and complete; its game acceptance is item 189.**
2. **Authorize (b)'s build, and accept its fixture cost?** Or park it until an ESA colony exists
   for another reason.
3. **Anything to change in (a)'s public wording** before it reaches the fix list? The line drafted
   from your own words is in the entry.

### 2026-09-14 — 184 RULED + CLOSED 09-15: the probe-sweep gate is an age, never a refusal; the ck144 (a) boot ran and is DISCHARGED; the toolkit chain has nothing hanging

<!-- ck:184 status:ruled owner:yes -->

#### ⚖️ RULED 2026-09-15, in your words, and CLOSED the same day

**(a) The probe-sweep gate.** *"5 hours is too short. 24 hours is the minimal. But this is just
resolved around playtesting. The rule would be 24 hours or post change that warrants a probe
sweep to be done on next play test. An agent may recommend a sweep outside of play testing if
it can articulate a reason that it should be done and explain the harm. But it cannot block
work, it cannot override the owner."* Framing: *"I prefer gate over hard rule framing."*
⇒ A desktop sweep is fresh for **24 hours** or until a change that warrants one; a stale sweep
is satisfied at the **next playtest**. An agent may **recommend** an earlier sweep only with a
reason and the harm named. ⛔ **No agent, gate or kit code refuses work, an upload, a boot or a
RunAll over a sweep's age, and none overrides the owner.** 99's C-4 (b) refusal is NOT built.
The sitting-side wording is already in `perma/SMRTK_SLOTS.md`; the documentation agent homes the rest.

**(b)** 08b's RunAll did **not** discharge ck144 (a). ✅ **The owed first RunAll then RAN 09-15
under a same-day stamp** — `reports/CK144A_CLOSEOUT_SITTING.md`: 69 PASS / 4 FAIL / 18 SKIP /
6 ERROR, the same names as 08b, nothing regressed. **(c)** The text status chip stands; the
ck175 dock icon is not built and not owed.

**(d) ck144 (a) is DISCHARGED.** Your ruling: fixes that fail loudly, live for weeks with
thousands of daily players and no report, are closed by **field evidence** — A5 c2 (F70),
A9 c4/c5 (F116) and F117's station recipe close that way, their recipes staying in the
entries for a countering report; A3 (F118, module deleted 09-12) and A10 (optional pack-off
boot) are **struck**. The RunAll half is (b). ⛔ **Nothing from ck144 (a) is owed to anyone.**

**(e) The toolkit's last loose ends, closed by your word 09-15** (*"in my mind its good
enough … unless it poses a real risk"* — none does): C-3 editor colour **refuted in play, low
priority, not routed** · C-5 arm-time refusal built, **unwitnessed**, one press at any later
sitting · C-8 was never owed · ck183 item 5 (eligibility off the strip) **confirmed**.

⭐ **MEASURED in the 08b sitting, and it is the highest-value thing that sitting
found.** The full `RunAll()` recorded its own gate as:

```
preflight="DESKTOP sweep CLEAN: 2026-09-14T15:20:31Z pack=3ae67dea… kit=c886fb70…"
```

⛔ **The tree that was actually running was TestKit `8e25f6b` — several commits
later — and the sweep was ~5 hours old.** The gate whose entire job is to assert
"the swept code is the running code" passed a sweep of *different* code, and said
CLEAN while doing it.

⚠️ **Why this is worse than one bad run.** Every probe verdict rides on that
attestation. A stale one does not produce a visible failure — it produces a
**confident green** over a tree nobody swept. That is the same silent-success
shape as the other two defects 08b found (a depot record that proves nothing, a
field watch that can never fire), and it sits underneath the whole suite.

⇒ **It also weakens 08b's own probe result** — 69 PASS / 4 FAIL / 18 SKIP /
6 ERROR was read under this attestation. ⛔ Do not quote that run as a clean
baseline without saying so.

**The ask as originally put (2026-09-14) — ruled above, kept as the record:**
1. **Should the preflight refuse a stale or mismatched attestation** (compare its
   recorded `pack=`/`kit=` against the live HEADs, and refuse rather than warn)?
   That is a behaviour change to a gate you rely on, so it is yours.
2. **Does the 08b `RunAll()` discharge ck144 (a)'s owed first `RunAll()`?** 08b is
   explicit that this is UNRULED, and the stale attestation is a reason for
   caution. ⛔ No session may assume it either way — STATE records it as *run,
   under a stale attestation*.

**Evidence:** `reports/SMRTK_08B_SURFACE.md` "Defects FOUND AND NOT REPAIRED" §1;
raw line in `archive/logs/smrtk08b_Mars.exe-20260914-20.03.09-6a91a190.log`.

### 2026-09-14 — 182 RULED + CLOSED 09-15: PLAYTEST_HELP has no owner-facing core — DISSOLVE it

<!-- ck:182 status:ruled owner:yes -->

#### ⚖️ RULED — dissolve. Re-confirmed 2026-09-15 because the marker never moved

> *"Haven't we decided that in about 4 different conversations at this point, including this one?"*

⇒ **`docs/PLAYTEST_HELP.md` (62,965 B) is DISSOLVED, not reframed.** The split below stands as
written: **SMRTK reference** (agent-facing, pull-only) · **the hazards and the rider-authoring line
into `prompt-authoring`** · **launch mechanics into `perma/CO_RUNS.md`** · **cut** the command table,
the save-fixture recipes and the archived-`TESTING.md` do-not-use list. Execution waits only on
`prompts/DOC_EDITING_SKILLS.md` building the skill that receives the hazards; nothing else gates it.

⛔ **The ruling was already in force and this item still regenerated onto `WAITING_ON_YOU.md` every
session, so every session re-asked it.** `.claude/HANDOFF_PROMPT.md` carried it under *"Owner
rulings in force — authority, not to be re-derived"* and, twelve lines later, called it a pending
*"dissolution decision"*. ⇒ **A verbal ruling with no marker flip re-asks itself forever.** The
generated queue is only as good as the last agent who remembered to move a marker, and that is the
defect this row is now the receipt for.

> ⭐ **NEW EVIDENCE 2026-09-14 (08b, walked with the owner) — the file is now
> MEASURABLY STALE, which bears on whether it is worth keeping at all.** Its
> toolkit section describes *"the 03A/03C build; sitting 08 checks the new pages
> in play"* and walks **six** pages. The real surface after 09's re-layout and the
> Stamper cut is **seven**: Sitting · Run · Selected · Slots & notes · World ·
> Saves · Probes & logs. ⚠️ **It has no `Run` page at all** — the page that now
> holds every trigger and `run_until` — and two tab LABELS differ from their ids
> (`Agent` renders as "Slots & notes", `Kit` as "Probes & logs"), which is exactly
> the kind of mismatch that wastes a sitting's first ten minutes.
> ⛔ **NOT corrected by 08b, deliberately:** its scope fence bars the checklist and
> a rewrite would pre-empt YOUR dissolve/keep call here. ⇒ **If you dissolve it,
> this cost disappears. If you keep it, it needs a re-walk, not a patch** — and
> the walk was already done once in 08b, so it is cheap now and gets dearer the
> longer the surface moves.

From the 09-14 design session with you. Full derivation:
[RULE_PLACEMENT_TEST.md](agent/reports/RULE_PLACEMENT_TEST.md) ·
[C1_MONOLITHS.md](agent/reports/C1_MONOLITHS.md).

⭐⭐ **The test we landed on, and it replaces "is this important?":**
**"What actually stops this, if not the reader's memory?"** Structure ⇒ delete the rule · a guard
⇒ one-line pointer · nothing and it's been violated ⇒ it was never a rule · binds one job ⇒ that
job's skill · already a fact ⇒ keep the fact, cut the prose.

- ⛔ **"Ground rules" goes to ZERO.** All six items fall; only 5a's *"never write 'play for a
  while first'"* survives, into the prompt-authoring skill. **3,900 B → one line.** You had never
  read it, correctly — it was an agent section under an owner-sounding heading.
- ⛔ **Rule 1 ("NO third-party mods") was DEAD and nothing noticed.** `bugs/F104.md:64` records a
  rig leg with *"all six mods + TestKit loaded"*, and F104 is the project's cleanest field closure.
  **Zero** agents ever flagged the violation. ⇒ **This project has no gate that asks whether a rule
  is being followed**, and an unenforced rule still costs every agent who reads it.
- **Rule 3 ("TestKit never uploaded") is enforced by STRUCTURE, not compliance** — the TestKit repo
  has **no git remote at all**, and it is a sibling directory the packer cannot reach.

⚠️ **THE DECISION FOR YOU — dissolve `PLAYTEST_HELP.md` rather than reframe it.** It is an agent
doc with an owner's name on it, which is why it accreted for six weeks unread. Proposed split:
**SMRTK reference** (agent-facing, pull-only; your own surfaces need no manual — a manual on a
system commissioned to be self-explanatory is a UI defect list, not a doc) · **playtest /
prompt-authoring skill** (the hazards, the rider-authoring line) · **`perma/CO_RUNS.md`** (launch
mechanics — finishes the 09-12 split, which took the protocol and left the mechanics behind) ·
**cut** (command table, save-fixture recipes, the archived-`TESTING.md` do-not-use list).
⛔ Settle it at the **181** attended audit, after sitting 08 shows what SMRTK actually covers.

- ⚠⚠ **ONE LIVE GAP, and it does NOT wait on any of the above.** You assumed an agent setting up a
  playtest **scans the existing saves for a suitable one** instead of asking you to build a
  fixture. The facts exist (7 `EF-*` files) and agents have done it — sitting 08's fixture was
  chosen 09-14 by reading `CheatsUsed` off disk. ⛔ **But no standing prompt requires it.** It is a
  habit, not a rule. A session that does not think of it will ask you to build a save you already
  have. ⇒ First thing into the new skill.

⭐ **ADDED TO THE AUDIT BRIEF (your ask, same day):** look for rules that should not be rules at
all — *"either because it's beyond what an agent could even do, or something an agent would never
do via its programming."* Recorded with a falsifier, because that second half can delete an earned
rule: **⛔ the discriminator is not "would a well-behaved agent do this?" but "has this actually
happened?"** *"Never `git checkout --` as a restore"* reads as gratuitous, and exists because an
agent here did it and silently destroyed an uncommitted rewrite. ⇒ **A recorded incident means
KEEP; no incident and no guard means cut** — which gives the audit a mechanical first pass, and
makes the house habit of pairing a rule with its incident load-bearing rather than decorative.
⚠️ Two keyword samples found the genre nearly absent here, so the yield may be small and the
criterion worth more as a filter on NEW rules — but a class defined by meaning cannot be grepped,
so the audit must READ for it.

⭐ **THREE MORE AUDIT REQUIREMENTS (your ask, same day).** (1) **Duplicates by MEANING, not by
string** — two rules with different names, in different docs, can impose the same duty; the
existing pass found 14 pairs and they were near-verbatim. (2) **Every rule in the repo, with a
number.** (3) **A fourth shape: the "rule" that is actually just INFORMATION** — requires no action
of the reader → engine fact to `facts/EF-*`, lesson to a pull-only doc, never the always-loaded set.

⛔ **The existing 852-rule inventory does NOT answer (2), for three measured reasons.** Its own
`count_unit` says *"Counts are not unique policies or atomic predicates"* — 852 is **occurrences**,
and `WORKFLOW`'s 10 entries proved to be **7 distinct rules**. It covers **22 of ~618 rule-bearing
files** — never opened: `bugs/` 195, `reports/` 197, `facts/` 103, `tools/` 56, non-perma prompts
39, **the skills** (the only cross-vendor-gated rule carrier), and `metadata.lua`/`items.lua` —
where `items.lua:204` carries *"a module absent from this file SHIPS ABSENT"*, a rule with a
player-visible consequence living in a Lua comment. And it never deduplicated by meaning.
⇒ **Report two numbers, occurrences and distinct rules, and say which is which.**

⭐⭐ **Why that pass could not have answered any of this: it asks "where should this rule live",
never "is this a rule."** All five of its classes are placement, which is why **780 of 852 landed
in "task-local"** and it moved on. ⛔ The audit must not inherit its classifications — existence is
the first question, placement the second.

⭐⭐ **AGREED 2026-09-14 — the machinery, all five parts.** Spec:
[RULE_PLACEMENT_TEST.md](agent/reports/RULE_PLACEMENT_TEST.md) § THE MACHINERY. ⛔ Your words: the
marker is **mandatory or all of this is for nothing.**

1. **Every rule is written `Rule: <duty>` at line start**, collected under a **`Must_Read_Header`**
   — deliberately without the word "rule" in it. Measured: headings containing "rule(s)" appear in
   **66 files**, `^Rule:` in **1** — which is exactly why the header must not say "rule".
2. ⛔ **The tagging is the AUDIT'S OUTPUT, not a find-and-replace** — there is no string to find;
   deciding which sentences are duties IS the audit. ⇒ It delivers a **tagged tree + a coverage
   manifest**, so the number is re-derivable forever by grep and the audit never re-runs.
3. **The gate:** an untagged rule cannot be detected mechanically, but *"a rule-bearing file changed
   and its `^Rule:` count did not move"* can. ⭐ **Same mechanism as ck177's marker gate, which is
   ruled but NOT BUILT** — build once, point it at both.
4. **A rule-creation skill** — your four criteria plus seven, each earned by a case today. The
   sharpest: ⭐⭐ **an EXPIRY condition on every rule** (*"what would make this stop being true?"*),
   because your four are all admission tests and nothing removes a rule — which is exactly how rule
   1 survived six weeks dead. And ⚠️ **rule 3 passes all four of your criteria** and was still
   unnecessary, so "what stops this if not memory?" has to be asked first.
5. **`STATE_EVICTION` gains a rule sweep** — rules with no marker, and rules whose expiry condition
   has fired. ⛔⛔ **It may NEVER retire a rule; it ELEVATES to you and you rule.** Precedent: ck178
   (*"no agent retires this on its own judgement"*). ⚠️ The elevation must be **ranked and small
   with the receipt inline** — a sweep surfacing forty rules a run will be ignored.

⚠️ **Two sequencing constraints:** the skill ships **with** the gate, never before it (friction on
writing rules otherwise pushes agents to write duties as untagged prose — worse than unwritten,
because the count then looks complete); and **`RULES_HEADERS` must be RE-READ against this before it
fires**, not just re-fired — it was built on the 852 inventory, which answers placement, and
existence now comes first.

⭐ **SEQUENCING RULED 2026-09-14 (owner):** *"I want to get smrtk finished and then I will refire
rules header."* ⇒ **`RULES_HEADERS` is blocked on SMRTK COMPLETION** — sitting **08** then **99** —
**not merely on the sitting ending**, and the owner fires it, not an agent. ⛔ It is also not a
straight re-fire: it must be **re-read against this item first** (it was built on the 852
placement inventory, and existence now comes first). The sequencing is not arbitrary — what SMRTK
covers decides what `PLAYTEST_HELP` loses, which decides which headers are needed at all.

⚠️ **Scale note, corrected 2026-09-14.** This seat described the day as having "produced less
deletion than it looks like." That was wrong. Decided for removal or relocation in
`PLAYTEST_HELP` alone: ~31,600 B superseded by SMRTK · 3,900 B of Ground rules down to one line ·
2,788 B of fixtures · 1,517 B of the archived-`TESTING` list · ~7,100 B of co-run mechanics moving
to `CO_RUNS`. ⇒ **~75% of a 62,709 B doc, decided** — on the FIRST of four monoliths, before the
attended audit has run, with three still un-audited. ⛔ Counting a session in bytes removed from
the tree measures execution and ignores adjudication, which is the part that was hard.

✅ **RULED 2026-09-14 — both `WORKFLOW` questions, and the audit's timing. ⛔ NOT YET EXECUTED:**
the owner also ruled *"stay out of the tree"* while smrtk sitting 08 runs, so these are recorded
here and the `WORKFLOW` edits are deferred until the sitting lands.

- **Rule 4 → RETIRE OUTRIGHT.** No successor, no repoint. `perma/PUBLIC_SURFACE_SWEEP.md` already
  carries the identical duty — *"run whenever a fix is added, retired, or materially re-scoped…
  this one covers what the words say"* (2026-08-24, written against surfaces that exist).
  ⭐ Rule 4 and that sweep are **the same duty under different names, in different docs, naming
  different artifacts** — a live worked example of the semantic-duplicate class this item's audit
  is being built to find, and one a string match would never have caught.
- **`WORKFLOW:664` → RETIRE THE BLOCKER**, recording that it lapsed with the rescue tool (item 17,
  2026-08-14). The uninstall procedure is on no live surface and ten versions shipped past it;
  practical harm is low because the card already states the pack writes almost nothing to saves
  and that removing it simply lets the original bugs return. ⛔ Retiring the gate is the point — a
  release blocker that ten uploads passed unsatisfied is not a gate.
- **The rules audit runs AFTER SMRTK and BEFORE `RULES_HEADERS` refires.** Its tagging answers
  placement as a side effect, so it makes the header pass cheaper and may cut the seven headers
  down; running it first avoids doing the same reading twice. ⛔ It never touches the tree during
  a sitting.

### 2026-09-14 — 181: the monoliths get automated first, then YOU AND I audit all of them together

<!-- ck:181 status:open owner:yes -->

**Your ruling, 2026-09-14:** *"we can automate the other monoliths as much as possible. But as a
final pass I want a you+me session on all the monoliths as a second pass audit."*

- **Automate as far as it goes — that is now the DEFAULT for monolith work, not a fallback.**
  Characterisation, inventories, tombstone hunts and the mechanical passes are delegated:
  subagents and Codex, adjudicated by the orchestrator seat.
- **⚠️ THE ATTENDED SECOND PASS IS A GATE, and it is the LAST step — not an optional review.**
  The doc overhaul does not close until you and I have sat over **all** the monoliths together.
  ⛔ No agent declares the overhaul finished on its own judgement, and no automated pass is
  treated as the final word on a monolith.
- **The four this covers:** `PLAYTEST_CHECKLIST.md` · `PLAYTEST_HELP.md` · `agent/WORKFLOW.md`
  · `agent/FIX_POLICY.md`. ⛔ Re-measure at the sitting, never quote a size from here: three of
  the four are ungated and all four are written to by peers.
- **Where it stands 2026-09-14:** the three never-opened docs are under automated
  characterisation now (read-only, one agent each). The checklist's own pass ran 09-14
  (35 items / 159,621 B out). ⇒ What the attended session audits is the OUTPUT of those
  passes — which is exactly why it is sequenced last.

⛔ **This item stays `open` until the attended session actually happens.** The automated passes
landing does NOT discharge it; they are its input.

### 2026-09-14 — 180: archive follow-ups — ⚠️ one still needs your word, two are approved work

<!-- ck:180 status:open owner:yes -->

Three loose ends from the 09-14 checklist archival ([ARCHIVE_RECHECK](agent/reports/ARCHIVE_RECHECK.md)).

- **✅ DISCHARGED 2026-09-14 (`aad4021`) — the 5 restoration candidates.** Each was checked
  against CURRENT state rather than against the archived body: **0 of 5 need restoration**, and
  you ruled no restorations. ⭐ The sharpest one was real, and is fixed: the LIVE item reading
  *"Item 34's 'now or after' is still yours"* had been **stale for 25 days** — true the morning
  of 2026-08-20, false by that evening, when the close-out chain built C50/C51 and parked C52.
  Corrected, and marked `ck:56 status:closed` (it was one of the 12 unmarked, so it could never
  have retired). Verdicts: [ARCHIVE_RECHECK §B2](agent/reports/ARCHIVE_RECHECK.md).
- **✅ APPROVED — fix the archiver, leave the 35 landed headers alone.** It drops the leading
  date from a heading and truncates long ones (`ck139` was cut mid-word at
  `` `Fix_SilentHitMomentFX.lu ``). Bodies are intact and findable; only the archive's header
  text is lossy. ⛔ Do **not** rewrite the 35 — that would mean editing the append-only archive
  for a cosmetic gain.
- **✅ APPROVED — replace the stub pointer wording.** Every stub says *"search `ck-` and this
  heading"*; **that search returns 0** (the archive re-levels `###`→`##` and drops the date) and
  `ck-` is shared by 34 of the 35. Replace with the exact `## ck… -- archived …` line that
  actually exists. Touches checklist stub text only, never the archive.

### ✅ 2026-09-14 — 179 RULED: the doc-rules architecture — all six calls approved, build it
<!-- ck:179 status:ruled owner:no -->

**RULED 2026-09-14. All six calls approved as proposed**, plus two scope answers:

1. ✅ **Three tiers adopted** — permanent (`CLAUDE.md`, mirrored to `AGENTS.md`) · local (folder)
   · task (skills).
2. ✅ **7 headers, not 16**, plus **deleting the 9 perma restatements** of the rule
   `prompts/README.md:5` already states once for all of them.
3. ✅ **`CLAUDE.md` gets an explicit rules list**, including *"Editing a doc? Invoke the
   doc-editing skill first."* — **and `WORKFLOW.md`'s 10 global rules move into it.**
4. ✅ **`STATE.md` goes to zero rules** (its own line 3: *"Kernel only: status + pointer"*; the
   audit found 30 in it).
5. ✅ **Build `doc-editing`, package `prompt-authoring`, set a skill byte cap.**
6. ⛔ **DECLINED** — the 09-13 *"not yet converted into a **gate**"* wording **STAYS AS IT IS**.
   ⛔ Do not re-ask; do not "helpfully" rephrase it in any doc.

**`RULES_HEADERS` gate: ALL-CLEAR with three amendments** — 7 headers not 16 · cap **1,024 warn
/ 2,048 hard** (14 of the 16 measured headers are under 800 B; the old 1,536 was an arbitrary
number this seat invented, and one header missed it by a single byte) · **re-deriving the STATE
arithmetic before writing is a STOP condition, not a note** — its figure went stale within two
hours (12,331 → 12,504 B).

**A9 scope answered:** the redundant-doc review covers **the docs this workspace's agents use
regularly — `SMR-BugFixPack`, `SMR-BugFixPack-TestKit`, `SMR-CommunityMods`.** Not OptInPack,
not CommunitySaveRescue, not the non-SMR repos.

Full proposal: [DOC_RULES_ARCHITECTURE](agent/reports/DOC_RULES_ARCHITECTURE.md). Nothing has
moved. Built on Codex's inventory (`968c58e`, 852 rule occurrences) — that evidence survives
intact; what changes is the shape of the migration.

**Your design, 2026-09-14:** one permanent rules source kept as small as possible · per-folder
rules seen only by an agent working there · task rules on skills, loaded when the skill is.

**⭐ The reversal you should look at first.** The audit proposes **16 per-doc headers**, eleven
of them in `prompts/perma/`. But `prompts/README.md:5` **already states that rule once for all
of them** (*"never `git rm`; update in place"*), and **seven of the nine restate it in their own
text** — 10 copies live. Per-doc headers would make nine of those permanent. That is the exact
failure this effort exists to end. ⇒ **7 headers, not 16**, plus **deleting the 9 restatements**:
a net reduction in rules rather than a reshuffle.

**The six calls:**

1. **Adopt the three tiers** — permanent (`CLAUDE.md`) · local (folder) · task (skills).
2. **7 headers, not 16**, plus the 9 deletions.
3. **`CLAUDE.md` gets an explicit rules list** (it has none today; its 8 rules sit in prose),
   including one line: *"Editing a doc? Invoke the doc-editing skill first."* ⚠️ And move
   `WORKFLOW.md`'s **10 global rules** into it — they bind every session but sit in a doc read
   only per task. The audit does not move them; this is the biggest adherence win available.
4. **`STATE.md` goes to zero rules.** Its own line 3 says *"Kernel only: status + pointer"*, and
   the audit found **30 rules in it**. That is also why it keeps pressing its cap.
5. **Build a `doc-editing` skill**, package `prompt-authoring`, and set a skill byte cap
   (⚠️ both existing skills are already over doccheck's 3,072 B target).
6. **Amend your 09-13 wording** — *"a hazard is a failure not yet converted into a gate"* should
   read *"into a **loud** failure"*. Your own 09-14 point: nothing here is a real gate except
   your stop button. Same substance; the current wording promises what this system cannot do.
   Your words, so flagged rather than changed.

⚠️ **Do not approve this for context savings.** Measured: the whole always-loaded surface is
~16,000 tokens, while one undirected `rg "OnMsg"` over the shipped tree costs **~76,000**. The
context prize is elsewhere. **This is worth doing for adherence and doc rot**, which are reasons
enough.

⛔ Independent of **177** (the marker gate, still open) and **178** (the temporary cap, which
this does not retire).

### ✅ 2026-09-14 — 178 RULED: STATE's warn cap is TEMPORARILY +25% — ⚠️ you end it, and only you

<!-- ck:178 status:ruled owner:yes -->

**Your ruling, 2026-09-14:** *"it does no good to keep evicting until we can fix the bleed
of docs everywhere, inact a temporary increase of the state cap 25% more headroom to be
removed as soon as we are fully done with the doc overhaul (basically when I say we are
done)."*

**Landed:** `STATE_WARN_BYTES` **12,288 → 15,360** (12 KiB → 15 KiB, +25%). ⛔ The **hard**
cap stays **18,432** — unmoved, same as the 09-09 raise, because it is the backstop for
flags nobody read.

**Restore, when you say the overhaul is done:** set `STATE_WARN_TEMPORARY = False` in
`tools/doccheck.py`. That single edit returns the warn to 12,288 and nothing else changes.
**Falsified 2026-09-14 on the live file:** flipped to `False` → warn read 12,288 and the
reminder line vanished; flipped back → 15,360; restored from a copy and `sha256sum -c` OK.

**Why it cannot quietly become permanent:** every `doccheck` run now prints a `⏳` line
saying the raise is temporary, who ruled it, and the one edit that ends it. The 09-09 raise
(9 → 12 KiB) carried only a source comment reading *"REVISIT once the 1.1.0 fallout is
closed"* — nothing ever surfaced it again, and it is still in force a month later. A note
in a file nobody opens is not a reminder; a line in the output every session reads is.

⛔ No agent retires this on its own judgement — it ends on your word, not on a measurement.

### ✅ 2026-09-14 — 177 RULED: retirement now covers EVERYTHING in this file, not just tests — ⚠️ one gate still yours
<!-- ck:177 status:ruled owner:no -->

**✅ THE OPEN GATE IS ANSWERED, 2026-09-14: make the marker count RED — scoped to the items the
committing change itself touches.** A commit fails only if *it* leaves a checklist item
unmarked, so a peer is never blocked by someone else's omission. That is what turns the
retirement rule from a habit into a loud failure.

⚠️ **Owner rider: the remaining unmarked backlog still has to be gone through** — doccheck
reports **12 need a marker** today. The gate stops NEW unmarked items; it does not clear the
existing ones, and those are a separate pass.

**Your ruling, 2026-09-14:** the archive rule in this file's own preamble —
*"completed tests move whole to `PLAYTEST_ARCHIVE.md`"* — **is extended to every kind
of section here.** The preamble carries the operative text and is the only place it is
written; you ruled against copying it into `STATE.md` or `WORKFLOW.md`, on the grounds
that a session which never touches this file should not carry a rule about it.

**Why it was needed** — `wc -c` on this file at dated commits:

| 08-01 | 08-15 | 09-01 | 09-10 | 09-13 | after the 09-14 archival |
|---:|---:|---:|---:|---:|---:|
| 87,314 B | 187,322 B | 363,972 B | 539,297 B | 761,372 B | 606,050 B |

**8.7× in six weeks**, and the 09-10 → 09-13 leg runs at ~**74 KB/day**. The 09-14
archival removed **155,769 B — about two days of growth at that rate.** The old rule
covered PT test sections, **~1.0%** of the file, and was honoured; `Decisions waiting
on you` is **92.3%** and nothing reached it. **47.9%** is dated session records, kept
in parallel with `archive/SESSION_LOG.md` (91 hits for `2026-09-12` here against 20
there) — which is why the rule now sends those out of this file entirely.

**⚠️ STILL OPEN — one gate, and without it this is a habit, not a rule.** The mover
moves exactly the `ruled`/`closed` marked set, so an **unmarked item never retires**;
that is how this file reached 54% unmarked. `doccheck` already computes the shortfall
and prints it as a count (**12 today**) — it has never been allowed to fail. Prose in
the preamble does not fix this: an agent editing by targeted string may never read it.

- **(a)** Make the count RED — no commit leaves a checklist item without a status
  marker. The check exists; only its severity changes. Your own 09-13 rule applied
  here: *a hazard is a failure not yet converted into a gate.* Would need to fail only
  on items the committing change itself touched, so a peer is not blocked by someone
  else's omission.
- **(b)** Leave it a count, and accept periodic owner-approved sweeps like 09-14's.

⛔ No agent changes that severity on its own judgement — a gate that can block every
peer's commit is yours. Recommendation if you want one: **(a)**, scoped as above.

### 2026-09-13 — 176: the checklist cleanup you ruled (D4) never ran, and D4 is ~6% of the problem
<!-- ck:176 status:open owner:no -->

**You asked 2026-09-13:** *"I thought this was supposed to be cleaned out in this
migration. Moving all the done and stale records to an archive."* **You are right, and
it never happened.** Re-derived rather than relayed:

- **`--apply` has never been exercised.** The route exists —
  `.claude/tools/archive_settled.py` + `.claude/CHECKLIST_MOVE_MANIFEST.md`, 17 approved
  members.
- **The instrument is refuted and must not be applied.**
  [DOC_OVERHAUL_AUDIT](agent/reports/DOC_OVERHAUL_AUDIT.md) §4: `ARCHIVE-OLD` is
  report-only and can never enter `move_items`, so `--apply` cannot execute D4 as ruled;
  membership drifted 17 → 18. This file already records that at item 163's note.
- **Even run perfectly, D4 moves only 43,223 B of 741,708 B (5.8%)** — ⭐ and the reason
  is not that the rest is live. See the corrected breakdown below.
- **Growth outran the remedy ~9×.** This file took **+371,007 B across 192 commits since
  09-06**, a median ~2 KB per commit from every peer. One week of drift is 8.6× what the
  whole approved migration would remove.

**What this file is now**, by measurement across its 158 `###` sections: live decisions
**1.3%** · PT test sections **1.0%** · settled decisions 28.8% · dated session records
47.9% · done-marked 19.9%. It opens by saying it is *"the work list and nothing else:
what to test"* — the tests are **1%** of it. It is also carrying history in parallel with
`archive/SESSION_LOG.md` (91 hits for `2026-09-12` here against 20 there).

⚠️ **Separate risk, needs no decision — flagging it because it is silent.** Both
`archive_settled.py` and `CHECKLIST_MOVE_MANIFEST.md` sit under `.claude/`, which
`.gitignore:15` excludes. **Your approved membership exists on one machine.** No peer can
see it, a fresh clone has neither, and losing that disk loses the approval.

**⭐ Why it is only 5.8% — the tool is keyed on MARKERS, and the dead mass has none**

**Corrected 2026-09-13 after the owner scrolled the file and said the done/dated material
is obviously massive. They are right; 5.8% was the size of D4's approved move set, not the
size of the problem, and quoting it alone under-stated the cause.**

The script's universe is correct — `## Decisions waiting on you` is **92.3%** of the file
(678,779 chars, 129 items). It leaves 94% of that in place, and its own per-item verdicts
say exactly why:

| bucket | items | bytes | why it stays |
|---|---|---|---|
| `KEEP-unmarked` | 65 | **366,052 B (54%)** | ⚠️ label is a misnomer — it means *not a candidate*: no marker, **or** a marker whose status is not `ruled`/`closed` (see the correction below) |
| `KEEP-d` number-cited | 27 | 141,153 B (21%) | STATE/perma cite these numbers |
| `KEEP-archive-old` | 18 | 92,261 B (14%) | correctly identified as old — but **report-only, never moves** |
| `KEEP-c` procedure-bearing | 3 | 18,381 B (3%) | carries a recipe or fenced block |
| **`MOVE`** | **16** | **43,223 B (6%)** | the only bucket that moves |

**The bottleneck is marking, not moving.** Measured independently of the script: the
decisions section holds **79 items with no marker at all, 454,783 B** — and **68 of them,
373,458 B, are demonstrably settled-or-old from their own headers** (38 items / 220,007 B
whose heading says ✅ or RULED/CLOSED/DONE/RAN/LANDED; 30 more / 153,451 B dated before
2026-09-01). One of the largest untouched items is headed *"✅ 2026-09-12 — 168 RULED BY
YOU (batch 2)"*. **That is 8.6× what D4 would move, sitting still because nobody stamped a
marker on it.**

Re-check both numbers:
`python -X utf8 .claude/tools/archive_settled.py` (per-item table, tally the last column) ·
`doccheck` already reports the same shortfall from the other end as **"29 need a marker"**.

**⚠️ Correction 2026-09-14 — the `KEEP-unmarked` gloss above was wrong, and the bucket
table is now a 09-13 snapshot.** Two things, so nobody re-derives them:

- **The label does not mean "carries no marker".** `is_candidate` is
  `marker and status in ("ruled", "closed")` (`archive_settled.py:148`), so an item marked
  `status:open` is a non-candidate and falls into the same bucket. Live proof: **176, 173,
  171 and 169** all carry `open` markers and all report `KEEP-unmarked` — run the script
  and read the rows whose status column is not `unmarked`. The substantive figures in this
  item were measured independently and stand; only the "why it stays" wording was wrong.
- **The re-check recipe no longer reproduces these numbers.** The archival below moved
  155 KB out, so the script now reports a different split. Re-run it for *today's* position,
  not to confirm the table — the table is the pre-archival state the decision was taken on.

**The decision — scope, and it is yours**

D4's approved membership was fixed when this file was a fraction of its size, and the
audit is explicit that widening it needs its own owner decision. Revised now that the
cause is known to be **unmarked items**, not a stingy mover:

- **(a)** Repair the script to execute D4 as ruled — reclaims **~43 KB (6%)** and changes
  nothing about the 373 KB that carries no marker. On its own, this does not fix what you
  were scrolling past.
- **(b) ⭐ Mark the settled-but-unmarked backlog, then move it.** 68 items / 373,458 B
  already announce themselves as settled or pre-09-01 in their own headings, so the
  marking pass is mostly mechanical and auditable — and once marked they flow through the
  existing route instead of needing a new one. Needs your approval of the membership, and
  a rule that settles whether "unmarked + ✅ in the heading" may be auto-marked or must be
  eyeballed.
- **(c)** Also let `ARCHIVE-OLD` actually move (18 items / 92,261 B). It is report-only
  today by deliberate design, so this is a genuine scope change, not a bug fix.
- **(d)** Leave it — the cost lands on you reading it, not on agent context, since agents
  are told never to read it whole.

⛔ No agent should widen D4's scope or auto-mark your decisions on its own judgement.
Recommendation if you want one: **(b) then (a) then (c)** — biggest reclaim first, and
commit `CHECKLIST_MOVE_MANIFEST.md` into the repo before any of it, so the approval
outlives the disk.


**Execution 2026-09-14 (Codex): OWNER ALL-CLEAR GRANTED 2026-09-14, both groups.**
Group 1 markers: `d80fe75`; group 2 markers: `8988d90`; preparation: `2be7c73`.
Both moves committed and pushed separately: group 1 `1090f70` (761,372 -> 718,296 B);
group 2 `cfd97bc` (718,296 -> 605,603 B). Each kept 160 headings, parsed all 86
markers, balanced bytes, and passed doccheck. Original bodies and surviving bytes matched.
You accepted that marking brought 16 of the 18 report-only ARCHIVE-OLD items into
group 2; this was authorised retirement under your date rule, not completed tests.
The archival script is unchanged; ARCHIVE-OLD remains report-only. **D4's original
16 items / 43,223 B did NOT move and remain here. This is not complete archival.**
The all-clear is discharged; the broader backlog remains open with no new owner ask.
The task prompt and its map row are consumed together; evidence and risks:
[CHECKLIST_ARCHIVE](agent/reports/CHECKLIST_ARCHIVE.md).

### 2026-09-13 — 175 RULED: build the SMR Tool Kit (chain `prompts/smrtk/`); two sittings are yours when their scripts land
<!-- ck:175 status:ruled owner:yes -->

**Owner ruling, 2026-09-13, in one design conversation** (`smr-bugfixpack-8f`): replace the game's built-in cheat
menu, for playtesting, with a **tool kit panel in the TestKit mod**. Your requirements, verbatim in the chain
README: **(A)** nothing it does may register as a cheat in vanilla's detection; **(B)** every line it writes is tagged
`SMRTK_<Verb>` so an agent never has to ask. You accepted the whole tiered list — slots an agent pre-loads, triggers,
save slots A/B/C, console tap + clipboard copy, the TestKit on buttons, and the layout stamper (*"a game changer"*) —
home in the TestKit, **both** UIs (infopanel section + floating tabbed panel), and a chain with a separate audit.

**What the source says, filed as facts so nobody re-derives it:** the taint is written only by three
`NetSyncEvents` wrappers and the work bodies are clean (`EF-095`); everything the panel needs is outside the mod
blacklist, but code-from-a-string is not (`EF-096`); the console "lock" is the hotkey action never being created
when the Mod Manager is closed, and `ConsoleEnabled` fixes it without mod tools (`EF-097`); the meteor cheats aim at
the camera, not the cursor, and silently do nothing on a nil position (`EF-098`); `PlaceConstructionSite` is the
game's own front door for the stamper (`EF-099`). You confirmed **F9 clears the console** today.

**Yours, in order:** the **02 kill-gate sitting** (~20–30 min, TAKEABLE WHEN link 01 has written its script into
`02_SKELETON_SITTING_owner.md`), then the **08 full sitting** (TAKEABLE WHEN 07 has written its script). Nothing
else is asked. Defaults you may change at any time: hotkey **Ctrl-Shift-K**, six agent slots.

**Shape, your ruling later the same day:** *"3A and 3B … cross platform this as a primary / secondary with B being
a judge of the work done. Codex does A and Claude does B."* Done: the five page builds are one fan-out link
(**03A**, Codex, which first settles the two shared UI-hook techniques so the builds cannot diverge) and a
cross-vendor judge (**03B**, Claude) sits between the build and the docs. 03B is also where every owner-routed item
from the builds lands — **as ONE append here**, not five. The queue is now 01 → 02 → 03A → 03B → 07 → 08 → 99.

**Seating, your third ruling:** *"nearly all the work is being done by claude which makes our cross vendor checks
weak … flip it to codex doing most of the build."* Flipped: **Codex builds 01, 03A and 07; Claude judges 03B and
audits 99 (Fable)**; your two sittings are attended by Claude. 01's re-validation of the cut is now the first
cross-vendor check, before any code.

**⭐ UI RULING, 2026-09-13, during the 02 sitting — the floating panel is NOT the shape you want.**
Verbatim: *"I am not a huge fan of the panel anyway, its in my way. I would honestly much prefer a smart panal that
replaces the area the cheats would normally be in. And for things that don't need to be there Create a SMR Icon on
the games dock and just reuse the games natural popout menu system if thats possible. That would likely be safer,
clearer, and a better experience."* This **supersedes** the "both UIs" line above: the per-object half stays (it was
always the plan), the **floating tabbed panel is demoted**, and the second surface becomes a **dock icon reusing the
game's own popout menus**.

Feasibility, read at source during the sitting, so 03A does not start from zero:
- **Per-object section: route PROVEN.** `Infopanel.lua:26-51` builds the vanilla Cheats section from the selected
  object's own `Cheat*` methods; the sitting watched it render, and your own screenshots show a depot's section
  carrying **Fill** and **Empty**. This was already P2's job.
- **Dock icon + native popout: route PLAUSIBLE, not verified.** The HUD is an XDef with named containers including
  **`idBottom`** (`Data/XDef/HUD.lua`), and there are ready-made `HUDButtonFrame` / `HUDButtonTemplate` XDefs to
  spawn. That is the same injection shape as the `OnMsg.Shortcuts` hook the sitting proved works. ⛔ Not tested —
  it is the third vanilla-UI injection problem and belongs in 03A's spike.

⚠️ **One thing to decide, raised not assumed:** the floating panel's **status strip** (CLEAN/TAINTED, eligibility,
armed count, errors-since-mark) is the at-a-glance safety read, and a popout that is closed most of the time cannot
carry it. Options: keep a one-line strip with no panel behind it; fold taint/armed state into the dock icon itself
(colour or badge); or accept it is only visible while a popout is open. **Not decided.**

**⭐ FALLBACK LADDER, same conversation — so 03A is never blocked on this.** Verbatim: *"Now if it turns out we
cannot do that, I am ok with the panel if we need it or a hybrid cheats menu along the side where I can popout and
close a more adv menu."* Ranked, highest first:

| # | surface | status |
|---|---|---|
| 1 | per-object **smart panel** in the vanilla cheats area **+ SMR icon on the dock** reusing the game's own popout menus | **preferred**; half proven, half is the spike's job |
| 2 | a **hybrid**: a cheats menu **along the side**, which pops out and closes, carrying the more advanced menu | acceptable |
| 3 | the **floating tabbed panel** as built in 01 | acceptable *"if we need it"* |

⇒ **03A does not stop and ask if the dock injection fails** — it descends the ladder and says in its report which
rung it landed on and why. The owner has pre-approved all three, so a failed spike costs a surface, not a link.
⚠️ Option 2 is the one nobody has costed: "along the side, popout and close" is a docked, collapsible strip rather
than either a free-floating window or a vanilla popout, and no source route for it has been read yet.

⭐ **The 02 verdict is unaffected by this ruling.** P1-P4 concern taint, the console gate, the console tap and
persistence; none depends on the panel being a floating window. The panel was the vehicle for the measurements, not
the thing measured, so the kill gate's result stands whatever surface 03A builds.


**Fourth ruling — licence for the builder:** *"don't tie codex up with too many restrictions … it could see better
ways or even suggestions we missed via model blindness."* The manifest now separates a short list of **invariants**
(your two requirements, idle = no patches, TestKit only, commit hygiene, never-same-vendor) from **everything else,
which is a default any build link may depart from with a stated reason**; every build report carries DEPARTURES and
SUGGESTIONS sections, questions are a first-class move, and the judge weighs departures on evidence, not conformance.

**Seats (Codex), your fifth ruling, on the difficulty read 01=7 · P1=5 · P2=4 · P3=7 · P4=6 · P5=8 · 07=4:**
**Astra** on 01 (xhigh), P3 (xhigh) and P5 (max); **Sol** on the 03A coordinator (xhigh or max), P1/P2/P4 and 07
(high). Load-bearing: 01 alone poisons the chain (a wrong core contract or `ConsoleEnabled` hook kills at 02);
everything else is contained to its own page.

**01 built, 2026-09-13 (Codex):** local TestKit core `774b55a`, floating frame
`b400683`, code list `5d8d3b3`. Desk smoke and parse/doc gates passed; **nothing
has run in the game**. **02 is now takeable** from its complete one-line-at-a-time
script in `agent/prompts/smrtk/02_SKELETON_SITTING_owner.md`; it needs a **clean
1.1.0 baseline**, not an already-cheated playtest save. Provisioning time is
separate from the sitting. 03A stays held behind that sitting.

**The cut was re-validated with corrections, not silently accepted.** The
default Ctrl-Shift-K is free in GameShortcuts/CommonShortcuts but collides with
Toggle Collisions in DevToolsShortcuts; the built binding is **Ctrl-Shift-F11**
(no source/TestKit collision found). The old TestKit already enables/opens the
console, so 02 now isolates the new gate with a negative/positive rebuild.
Toolkit ring lines alone cannot prove native capture; 02 measures actual print
output and its clipboard source, with the tee off then on.

**A measurement limit to keep visible:** `CanUnlockAchievement` is blacklisted
in the shipped mod sandbox (`EF-096`, corrected). The panel reports eligibility
**unavailable**, alongside an independent CLEAN/TAINTED read. It cannot honestly
show vanilla's eligibility reason or claim an observed eligibility PASS. Your
no-taint/achievement requirement stays in force; 03B/99 must adjudicate this
limit explicitly. Recommendation: first run 02's no-taint control, retain the
honest unavailable display, and let the judge decide the remaining evidence
needed before the tool is adopted. No achievement/account mutation was used.
Details, departures, suggestions and gates:
`agent/reports/SMRTK_SKELETON_PREDICTIONS.md`.

**Your notes from inside the 02 sitting, 2026-09-13 — all routed, nothing owed from you.**
Three were the same finding wearing different hats: the panel logs its own
**chrome** (tab switches, panel moves, open/close, clear) to the screen, where it
crowds out the evidence lines. The fix is a **destination policy** — every action
still emits exactly one tagged line (requirement B untouched), but chrome goes to
the log and the ring buffer only, never the screen. That also disposes of the
clear-button line landing on the freshly cleared screen, with no ordering change
needed. ⭐ The fourth is a **scope addition, accepted**: an **SMR icon in the
bottom HUD bar** that opens and closes the panel without the hotkey. It is a third
vanilla-UI injection problem, so it joins 03A's spike and P2 builds it; if no
route exists that leaves vanilla unpatched while idle, the hotkey stays and that
is a finding, not a failure. All four are in `03A_PAGES_FANOUT_codex.md`'s inbox.

**03B JUDGED 03A, 2026-09-13 (Claude, cross-vendor): PASS WITH FIXES.** Every
gate re-ran identically on HEAD; all 54 World actions and all 21 Selected
actions were opened against the game source and every one calls a clean leaf —
none of `EF-098`'s 13, no `NetSyncEvent` wrapper. Idle patching is **zero**
(two toggles, both with matching uninstalls). Nothing needed re-firing. Report:
[SMRTK_JUDGE](agent/reports/SMRTK_JUDGE.md). ⛔ Still nothing seen in play — 08
is the first sitting for every page, stamp and effect.

**⚖️ SIX THINGS TO RULE — this is the one consolidated append, as you asked.**
Each carries 03A's recommendation and mine. **Nothing here blocks 07;** items
1 and 6 are the only ones that could change what 08 tests.

1. **The dock, the lettered SMR icon, the honest Delete caveat, the 48-character
   Saves strip.** *03A:* accept provisionally, judge look-and-feel at 08; keep
   eligibility showing **unavailable** next to the taint read, since no clean
   read proves eligibility. *03B: **agree** on all of that* — and I fixed the
   Delete caveat myself (it described buildings only; on a colonist Delete
   removes the unit outright, so the label now says so).
   ⚠️ **But one scope question is yours, and it is the biggest thing I found.**
   The per-object section offers **22 actions where the vanilla cheats section
   offers 106** — vanilla lists whatever the object has, the toolkit uses a
   fixed list. Because the toolkit never re-enables vanilla's section, the other
   84 are simply gone. Concretely: select a **colonist** and you get *Delete*
   (which removes them outright) and nothing else, while vanilla would offer
   Kill, Starve, Make Renegade, Age 1 Year and more. **Recommendation: extend
   it, and my strong preference is before 08** — the safe route is already
   proven (list the object's own actions the way vanilla does, but call them
   the toolkit's untainted way, which P2 already does for its 22). It is a
   build, so it is 03A's or a follow-up's, not mine. **Your call: extend before
   08, extend after, or ship 22 as v1?**
2. **Quiet mode delays scheduled disasters rather than stopping them; the
   selected-rocket finish uses ordinary landing policy.** *03A:* retain both;
   at 08 provoke quiet while a disaster is already running, re-arm rapidly, and
   save/load once. *03B: **agree**, nothing to add.* Manual logger arms stay
   yours to own.
3. **Run-until pauses on any trigger *attempt*, not only a successful fire.**
   *03A:* accept that, because the fire counter cannot tell success from
   attempt; if you want success-only, someone must build a success signal
   before 07 documents it. *03B: **agree** — accept attempt-pause for v1.*
   Success-only is a real feature, not a bug fix; it is not worth holding the
   chain. Related limits to know rather than decide: field watches see plain
   values only, polling stops while paused, and "first Lua error since mark"
   means first error *notification*.
4. **Probes refuse to run until an agent provisions fresh desktop evidence for
   that sitting; save/load legs use a disposable current-branch fixture.**
   *03A:* retain. *03B: **agree**.* 03A also asked me to rule on the old
   TestKit's console bootstrap: **I ruled keep it, with one line inverted** so
   it stops forcing the on-screen console overlay — details are in my report and
   in 07's inbox. Nothing for you there.
5. **Snapshots stay scoped and bounded; verify on two loaded maps at 08.**
   *03B: **agree**.* Whole-colony totals can wait until something needs them.
6. **The layout stamper ships as a bounded v1:** flat cables and pipes, named
   skips for passages, switches and special buildings, and no promise of
   duplicating a whole colony. *03A:* accept the scope; 08 must witness fit,
   dome membership, connected grids and upgrade state. *03B: **agree** — and
   note the stamper has never placed a single object in the game.* Its desk
   checks are three synthetic plans that deliberately mutate nothing, because
   no link before 08 is allowed to launch the game. That is the correct
   sequence, not a shortcut, but it does mean **08's stamp leg is the first real
   test of the feature you called a game changer** — expect to spend real time
   there, and expect v1 to skip things.

⛔ **Nothing else is owed by you on smrtk right now.** 07 writes the docs and
your 08 script next; 08 becomes takeable when that script lands.

**⚖️ RULED BY THE OWNER, 2026-09-14 — in their words: *"item 1 ruled — extend
before 08."*** Items **2–5 accepted as both seats recommended**; item **6 noted**
(no decision was asked — it is the warning that 08's stamp leg is the stamper's
first contact with the game).

⇒ **Item 1: the Selected section is EXTENDED BEFORE 08.** It lists the selected
object's own `Cheat*`/`AsyncCheat*` members the way vanilla does, called the
untainted way P2 already uses for its 22. Build link `03C_SELECTED_EXTEND_codex.md`
(Codex/Sol, the seat that built P2); **07 runs after it**, so the docs describe the
shipped surface and 07's "do not write *replaces the cheat menu* until item 1 is
ruled" inbox line is now discharged — with the extension, the qualifier it was
guarding against is what changes. 99 absorbs the cross-vendor check on 03C rather
than the chain growing a fourth judge link.

⏳ **The condition this was ruled under (rule 5a), so a later reader can test
whether it still holds:** ruled on 03B's **PASS WITH FIXES** with **nothing yet
seen in play** and 07 not yet written, on the orchestrator's recommendation that
extending costs **Codex time rather than owner time** and spares a second attended
sitting — 08 tests one surface instead of a 22-action one that then changes. ⛔ If
the extension turns out NOT to ride P2's proven route, the cost basis of this
ruling is gone and it is worth re-asking rather than pressing on.

**⭐ 99 AUDITED, 2026-09-14 (Fable): SHIP WITH CHANGES — the Tool Kit is yours to use.** Plain language:
- **Is it safe for achievements?** The toolkit never registers a cheat: three sittings read `CheatsUsed` empty after
  every kind of action it has, and the game's own list of "why an achievement could be blocked" has five entries, of
  which the toolkit can only ever touch that one. The game will not let a mod ASK it for the final verdict
  (`UNAVAILABLE:sandbox` is honest, not a bug), so nobody may write "eligibility PASS". One caveat you already know:
  the More → AsyncCheat Inspect/Properties buttons open an editor window, and achievements are blocked **while it is
  open**; close it and the block is gone.
- **Does every line say it is the toolkit's?** Yes — every archived toolkit line in 02, 08 and the four 08b boots.
- **What changes before you lean on it?** Eight small items in `reports/SMRTK_AUDIT.md` §11; four are one short Code
  link (the mechanized-depot readout, the white `command` field, a watch that arms on a missing field, the console
  bootstrap order). None needs a boot of its own. Two docs (TestKit README, PLAYTEST_HELP steps) were corrected today.
- **Nothing here needs your word** except what ck184 already asks (the stale preflight, the RunAll question, icon vs
  status bar). ⛔ The Stamper stays parked and is not raised.
- **Next real sitting:** the owed ck144 (a) boot is the first one the panel serves — an agent preloads the slots
  first (`perma/SMRTK_SLOTS.md`), then you sit.

### 2026-09-14 — 183 RULED: SMRTK 08 ran — the design half; every ruling below stands, item 5 confirmed 09-15 (ck184 e)
<!-- ck:183 status:ruled owner:yes -->

**08's verdict is PASS WITH CORRECTIONS** (classes 1–17 pass, class 18 blocked;
`reports/SMRTK_FULL_SITTING.md`). ⭐ **Requirement (A) is PROVEN, not asserted:**
`cheats_count=0` with `CheatsUsed` enumerated by name after every destructive
action the toolkit offers — 844 records, zero TAINT, zero ERROR, zero surviving
arms. The 25 defects live in that report and are a build's problem.

⚠️ **This block exists because 08 routed its design findings to a REPORT only.**
Rule 5 (R10): a decision recorded only in a report **is not considered asked**.
Everything below is the owner-facing half, moved where it belongs.

#### ⭐⭐ THE OWNER'S ARCHITECTURE RULING, 2026-09-14 — this supersedes the page split

*"The buttons might make sense via category, but they do not make sense in use.
I should not have to go from World, find a button, to Agent, click a button, and
then to Kit and click a button and then back to World to click a button to do
something. Related actions and items should be on one page. And if an item is
used in conjunction with multiple items it should be on the top hot bar."*

⇒ **Group by TASK, not by taxonomy.** A page holds everything one job needs, start
to finish. Anything used *in conjunction with* other pages' work belongs on a
**persistent hot bar**, never on a page you have to travel to.

**The case that proves it, in the owner's words:** *"Like to finish a rocket
flight the steps for that, it was so confusing I would rather just hit ultra speed
and wait the 30 seconds."* Measured: `rocket_arrive` is registered on **World**
(`72:260`) in a row with `complete_constructions`/`complete_grids`, but it acts on
the **selection** — and an in-flight rocket cannot be selected by clicking
(defect 25), so the only working route was the **console**
(`SelectObj(HandleToObject[4080])`), with the handle coming from a Kit dump.
Four pages and the console, beaten by **ultra speed — a button on the same World
page**. ⇒ Two rules fall out, and they are general:
- ⛔ **An action that operates on a selection belongs on Selected.** `rocket_arrive`
  was filed on World because it is a "completion thing" — taxonomy beat task.
- ⛔ **A toolkit action must beat the vanilla workaround, or it should not exist.**

#### The measured tab-hop count (orchestrator, 2026-09-14) — why this is structural

| process | pages, in order | distinct |
|---|---|---|
| Watch a selected field until it changes | SELECTED → **KIT** (`watch_field`) → **AGENT** (`trigger_field`) → **WORLD** (`run_until`) → KIT | **4** |
| Finish a rocket flight | WORLD → (cannot select) → KIT (handle) → **console** → WORLD | **3 + console** |
| Run until next rocket lands | AGENT (`trigger_rocket`) → WORLD (`run_until`) | 2 |
| Short breakpoint / timed run | AGENT (`smrtk08_break`) → WORLD (`run_until`) | 2 |
| First Lua error since mark | AGENT (`mark`) → work elsewhere → AGENT (`trigger_error`) → WORLD | 2 + return |
| Fire a bound slot on click | AGENT (bind/arm) → map click → KIT (read) | 2 + defect 20 |
| Screenshot + Mark mid-test | leave your work → AGENT → back | +2 every time |
| Run probes | KIT | 1 ✅ |
| Dump the selected object | SELECTED | 1 ✅ |

⛔ **The cause is structural, not cosmetic: all four triggers are registered on
Agent (`74`), and the only thing that consumes a trigger — `run_until` — is
registered on World (`72`).** Every "run until X" task is therefore a two-page task
before anything else happens; no renaming or reordering fixes it. `watch_field`
adds a third page and two names for one feature: **"Watch selected field"** on Kit,
**"Selected field changed"** on Agent. ⇒ **Defect 10** (arm/disarm pressable before
a watch exists, answering `NOT_BUILT`) is that split showing through as a bug, not
a bad affordance.

✅ **The remedy already exists in our own code — this is not new machinery.**
`73_SMRTK_Infopanel.lua:29-32` surfaces `dump_selected` (registered on Kit) and
`pin_A/B/C` (registered on Agent) as buttons **on Selected**, i.e. actions
registered anywhere, surfaced where the work happens. That is exactly the hot-bar
principle, already built and working — and it is why "Dump the selected object" is
the one agent-type task with zero hops. Apply it to the seven flows that missed it.

**Highest-value single change:** one **Run** grouping holding `run_until` *and all
four triggers* — it collapses four of the seven flows. Then `watch_field` moves to
Selected (it acts on the selection) and surfaces on Run; `mark` and
`screenshot_mark` go to the hot bar, since neither is ever the task itself.

#### 08's surface findings — the rest of the design set

- ⭐ **RULED:** *"Just open and close the panel on click, opens it next click closes
  it."* **One SMR button toggling the whole panel; drop the popout menu.** `71`'s
  panel already carries a fuller status strip than the dock (it includes `quiet:`).
  Keep a compact clean/tainted colour on the button so requirement (A) stays
  visible while the panel is closed.
- **1. The dock inflates the HUD** — `idSMRTKDock` parents into `idBottom` at 62 px
  with `Margins = box(8,0,0,106)`, inflating `idBottom` by ~168 px and permanently
  pushing up MapSwitch/`idLeft` and the pinned shuttle/dome/rover row. Owner:
  *"its broken the UI layout its kicked up all of the things that usually sit right
  above the doc."* Fix: parent as a **sibling** of `idBottom`. Owner wants it
  **bottom-right**.
- **2.** `XWindow.FoldWhenHidden` defaults **false**, so hiding alone does not free
  the space (`XWindow.lua:751`). The owner asked; the sibling fix makes it moot.
- **4. A true dock icon IS available** (was "plausible, unverified"):
  `HUDMiddle → idMiddleList`, an `XWindow` with `LayoutMethod = "HList"` holding the
  vanilla `HUDButtonNoFrame` buttons. Appending costs **zero vertical space** and
  fixes item 1 **by construction** — the natural home for the single toggle button.
  ⚠️ Source-read only, NOT built, NOT run. Needs an image asset; text is the fallback.
- **5.** Drop the Delete caveat from the section body (`73:181`) — *"I don't need
  this info here"* — but **move it to the Delete button's `RolloverText`**, since
  03B added it to make the label honest about units.
- **7.** Size rows to their text and shrink the font. Today `selected_button`
  hard-codes `MinWidth/MaxWidth = 146` (296 for More) at `MinHeight = 30`.
- **8.** A disabled button is not visibly disabled — `RunAll`/`Run one` look normal
  while `SetEnabled(false)`.
- **9.** Kit labels do not match how the work is described; the owner could not find
  "Run all probes".
- **13.** Controls belong at the **top** of every page — Kit's verdict list grows
  with every run and pushes the buttons down, so the page gets worse with use.
- **20. ⭐ An armed click slot blocks ALL map selection, with no warning.**
  `AcquireClick` installs a `TerminalTarget` at priority 10001 returning `"break"`.
  Measured: slot 4 armed, the owner tried to select a drone, the click fed the slot
  (`object=FlyingDrone(2000244981)`) and the drone was never selected. Right-click
  to cancel appears **nowhere on screen** ⇒ hot-bar candidate: a persistent armed
  indicator naming the slot and its escape.

#### ⭐⭐ 2026-09-14 — THE STAMPER MAY BE RECOMMENDED FOR REMOVAL (owner licence, given live to 09)

⚖️ **Owner, 2026-09-14, spoken directly into the running 09 session:** *"The stamper is
complex and heavy, you are allowed to recommend its removal if its never going to be able
to do its job right, or its overly fragile."*

⛔ **Recorded here because it was given verbally and exists in no file.** 09's brief on
disk does not carry it, and `prompts/smrtk/` is 09's lane while it runs, so it could not
be added there. ⇒ 09 folds it into its own close-out; until then **this is the only
written copy**.

⚖️ **It is a licence to RECOMMEND, not to decide.** Removing a whole feature is a
`FIX_POLICY` §4a design call and stays the owner's. 09 reports; the owner rules.

⚠️ **This does NOT contradict ck175, and nobody should read it as the chain overruling an
owner ruling.** ck175 records the owner calling the stamper *"a game changer"* and
approving the whole tiered list *"once we have it as a tool we have it forever"*. Rule 5a:
a ruling carries the state it was made in — **that one was made before anyone knew the
stamper had never placed a single object in the game, and before defect 21 showed its
capture guard rejects every building.** The condition changed, so revisiting is legitimate.

⭐ **08b SURVIVES A REMOVAL VERDICT — it has a second job (owner, 2026-09-14):** *"08B will
still have a job we need to confirm the new menu layout, the positioning."* ⇒ **08b is the
first play contact for 09's re-layout**, and that is true whatever happens to the stamper.
⛔ **An earlier version of this block said 08b would be "moot" and should be retired — that
was WRONG and is struck.** What a removal verdict changes is 08b's *scope*, not its
existence: it loses the class-18 half (blocks 13–15, the three native stamps) and keeps the
surface half.

⚠️ **The machinery for that was already right, only the conclusion was wrong.** 09's
close-out already requires it to **name every 08 verdict its changes invalidate and append
that list to 08b's inbox** — because 08 scored **block 1 (dock, status, navigation —
classes 1, 2, 4) PASS against the OLD surface**, and a re-layout puts that verdict out of
date. ⇒ 08b's surface job comes in through that inbox; what it needs is the brief's own
"⛔ re-runs nothing from classes 1–17" line relaxed to match, **folded in at 09's close-out**
(`prompts/smrtk/` is 09's lane while it runs, so it is not edited from outside).

⚠️ Defect 21's one-line fix goes in **either way** — it is what makes an honest evaluation
possible, and it is far too cheap to gate on the outcome. ⛔ A verdict of *"it can never
work"* reached without first fixing the guard that rejects every capture would not be worth
recording.

#### ✅⭐ 2026-09-14 — RULED BY YOU: THE STAMPER IS CUT

⚖️ **Your words:** *"with the impovements of the whole kit and making instant construction
easier, I think the stamper isn't as important as I originally thought. Unless you can come
up with a good reason to not cut it, I say we just cut it, its complex and the most likely
thing to break in the whole toolkit."*

⛔ **The counter-reason was looked for and did not survive.** You asked for one, so this is
what the search found rather than an agreement:

- **The one real argument FOR keeping it** is fixture provisioning — `EF-079` branch-locks
  the 1.0.7 save library, so every 1.1.0 leg needs a colony built from scratch in hours,
  and **151 (c)** says outright *"Building those conditions from scratch is expensive."*
- **It fails anyway, three ways.** ① Capture needs a source layout to read, and the
  fixtures worth reproducing are on 1.0.7 and cannot be loaded — so there is nothing to
  capture from, and the feature only pays back on a *second* replay we have never needed.
  ② `EF-099`'s own correction: *"Capturing only kind and hex loses the grouping/order
  needed to replay a connected passage"* — and the first layout 151 (c) names is **F52
  passage**. The same correction shows `IsBuildableZoneQR` is a terrain filter, not a
  footprint fit check. ③ A partial placement has **no rollback**; the recovery boundary is
  a disposable save. Underneath all three: **it never placed one native object.**
- **Your standing rule already pointed the same way** — 151 (c) takes those checks only if
  the colony *already has* the layouts, *"otherwise SKIP THEM BY NAME"*, under ⛔ never
  build a layout to make a check possible. Manufacturing layouts was the Stamper's job.

**Done, 2026-09-14** — TestKit `d80fb5e` deleted `Code/77_SMRTK_Stamper.lua` (725 lines,
the largest module in the toolkit) and `Layouts/`, plus the metadata code-list entry, the
`"Stamper"` page id and slot 3's three dead layout fields. **The panel is seven pages, not
eight.** No pack module was touched — TestKit is local-only, **0 shipped hashes**, so there
is no player-facing surface and no release risk. 08b keeps its second job and loses only
the class-18 half; 99 is told not to audit deleted code.

⭐ **THE WORK IS ARCHIVED, NOT LOST — `docs/FUTURE_IDEAS.md` entry 5.** It carries the v1
format contract, the design reports, the engine routes in `EF-099` (still true and still
useful for instant construction), the three unsolved problems any revival must answer
first, and the git coordinates to recover the body (TestKit `9057fb6`, a local-only repo
with no remote).

⛔ **IT IS NOT AGENT-TRACKED, BY YOUR INSTRUCTION.** *"Any mention of it must be in pull
only documents, not stubs of it in things that are read always."* ⇒ It is on **no** owed
list, generates **no** row in `WAITING_ON_YOU.md`, and is **absent from `STATE.md`,
`CLAUDE.md`, `DISPATCH.md` and `GENERAL_USE_PROMPT.md`** — the always-read push set. ⛔ **No
agent raises it, re-costs it, or counts it as outstanding.** You un-park it in words when
the workload allows, or it stays parked.

#### ⭐ 2026-09-14 — THE 08b SITTING RAN ITEM 1, AND YOUR UI RULINGS FROM IT

⚠️ **Recorded here because rule 5 (R10) binds: a decision that lives only in a
report — or in a commit message, a code comment and a chat transcript — is not
considered asked.** These are yours, given live at the keyboard during 08b's
class-1 walk. ⛔ They are RULINGS, not proposals; a later session does not
re-litigate them.

**The rulings.**
1. ⭐ **The dock chip goes in the RIGHT CORNER**, not jammed against the game's
   dock. *"it whould be in the right corner not right up against the dock."*
2. ⭐ **It carries the status at a glance** — *"it should have all the info as
   the old one just no expandable menu"* and, on review, *"its still missing the
   information like clean errors ect."* ⇒ taint, armed count, errors, quiet.
   ⛔ The popout stays gone; the chip is not a menu.
3. ⭐ **Quiet is an INDICATOR, not a button** — *"Quiet mode: On/Off As an
   indicator not a button"*. It reads On/Off at all times, never only-when-on.
4. ⭐ **The console must NOT auto-open on game load** — *"now that this is build
   can we stop the console from auto opening on game load?"* ⛔ Only the
   auto-open changed: the console is still ENABLED (02's kill gate measures
   `ConsoleEnabled` in `70_SMRTK_Core`, a different thing), Ctrl-Alt-C still
   opens it, and the Kit's force-open still works.
5. ⚖️ **Eligibility came OFF the always-on strip** — you asked *"I don't
   understand the purpose of eligibility"*. It can never read anything but
   `unavailable (sandbox)`: `CanUnlockAchievement` is blacklisted to mods
   (`EF-096`). It is a disclaimer, not a measurement — it exists so CLEAN is
   never read as "achievements are safe", since CLEAN proves only the taint half
   of requirement (A). It is still answered on demand by Sitting's **Read
   eligibility** and still in the log, where 99 re-derives it. ⚠️ This one is a
   RECOMMENDATION I implemented, not a verbatim ruling — reversible on your word.

**Eight defects found and repaired during the walk** (all TestKit, 0 shipped
hashes). ⛔ None was a redesign; the surface read as "a mess" because of them:
`5a281f1` every button caption invisible · `f58b3b2` status strip clipped by a
fixed `MaxHeight`, dock jammed + carrying no status, quiet ambiguous, eligibility
noise, console auto-open · `78305d4` the bar 106 logical units too high.

⭐ **The caption bug is the one worth remembering:** `T.Button` passed a
mod-declared TextStyle that never resolved, so **every** caption in the toolkit
drew blank while every plain label rendered. It was **defect 7's own partial fix**
— the size-20 style invented to answer your font complaint is what blanked the
UI. ⇒ **A surface cannot be design-judged while a render bug is live**; this one
nearly bought a full redesign sweep of a panel whose buttons had no labels.

**Item 1 verdict: PASS with the defects above repaired.** Walked with you:
7 tabs (Sitting · Run · Selected · Slots & notes · World · Saves · Probes & logs
— note two labels differ from their ids), hot bar visible on every page, controls
above the growing readouts, collapse/expand intact.

⭐⭐ **DEFECT 7 IS RULED, 2026-09-14 — FONT SIZE 16, AND THE TAB ROW WRAPS.**
Owner, once the real style was finally live: *"Drop the font to 16 is fine its
plenty big and wrap."* ⛔ **This SUPERSEDES defect 7's original premise.** That
premise was *shrink `ConsoleLog` while remaining LARGER than vanilla Cheats (18)*
— which 09 reported as literally unfulfillable, `ConsoleLog` being 13 and Cheats
18. **16 is SMALLER than vanilla Cheats**, and that is the owner's call: the
"larger than Cheats" constraint is dropped, not satisfied. ⛔ No session may
"restore" a larger size on the strength of the old premise.

⚠️ **The verdict was only takeable at the third attempt**, and the sequence is
the lesson: size 20 was invented to answer defect 7 → its malformed TextStyle
blanked every caption → a file-scope re-declaration still did not register, so
the first "verdict" would have been passed on the 13pt fallback → only after
lazy registration (log line gone) was the real typography on screen to judge.
⇒ ⛔ **A font verdict is worthless unless the log proves which font rendered.**

⭐ **Its side effect is itself the finding:** at 20 the seven tab labels
overflowed the 780-wide panel and clipped on both edges. That is the **THIRD**
fixed cap to clip content once the font grew (status strip `MaxHeight`, dock chip
`MaxWidth`, tab row `MaxHeight` + non-wrapping `HList`). ⇒ **The class, not the
number, is the defect** — the tab row wraps now, so the next label or font change
cannot re-break it.

⛔ **STILL OPEN, and not yours to answer:**
- **Item 2 (Class 2 evidence) PASSED with witnessed evidence**, not agreement:
  `COPY flushed=true from=42 lines=5 truncated=false` scoped to `MARK mark=42`,
  a `CLEAR`, then a NEW `TAINT_READ` after it — with records 36–41 still in the
  file. ⇒ Clear screen clears PRESENTATION ONLY and destroys no evidence.
- ⚠️ **Reading a toolkit log: every record appears TWICE** (file + console tap)
  **except chrome verbs**, which appear once. `SMRTK_TAB` tallied an odd 13 for
  exactly this reason. ⛔ Never quote a raw verb count as an action count.
- **The command field is white-on-light until hovered** (`74:336-341` sets a
  near-white `TextColor` *and* `TextStyle="ConsoleLog"` on an `XTextEditor` whose
  dark `Background` is not painting). You called it minor and deferred it.
- ⚠️ **This sitting DEPARTED from 08b's own scope fence** — the brief says a
  defect found here is *filed, not repaired*, and you licensed repair instead
  (*"I am ok with either you fixing it or firing up a subagent"*). Eight commits
  came out of an attendee link. ⛔ 99 must be told, not left to discover it.

#### ⭐⭐ 2026-09-14 — 08b ITEMS 3, 4, 5 PASSED, AND REQUIREMENT (A) IS RE-ESTABLISHED

⭐⭐ **REQUIREMENT (A) HOLDS ON THE REBUILT TREE.** 08 proved it on the OLD
surface and 09's rebuild invalidated that verdict for changed code. Re-measured
in play 2026-09-14: **19 unique vanilla cheat leaves dispatched, then
`SMRTK_TAINT_READ ... used=false`.** Zero ERROR, zero REFUSED, the `SMRTK_TAINT`
assert never fired, every record `valid_after=true`. Leaves: `CheatCleanAndFix`
×7 · `CheatFill` ×4 · `CheatMalfunction` ×3 · `CheatEmpty` ×3 ·
`CheatLightningStrike` ×1 · `CheatAddDust` ×1. Provenance in the same log:
`fix_pack_present=46/46 game=403908 pack_version=11 save=SMRTK_490.savegame.sav
sol=490`, all three mods loaded.
⛔ **This is a 19-dispatch SAMPLE, not 08's 844, and NOT universal proof.** It
re-establishes (A) on the current tree and nothing more. ⛔ No session may quote
it as a global guarantee.

**Item 3 — status and ownership: PASS.** The arm lifecycle was read from the log,
not agreed to: `ARM slot_4 mutation=none once_click=true` → `FIRE clicks=1
mutation=none object=FusionReactor(8179)` → `DISARM cleanup="click target
released" reason="click complete"`, then a second cycle ending `DISARM clicks=0
reason="right click"`. **Arms balance exactly 3/3 with 2 fires and zero
survivors**, matching the chip's `armed 0`. ⇒ The right-click escape is a real
input release, not a cosmetic one, and a read-only slot mutates nothing.

**Item 5 — More: PASS.** `SMRTK_SELECTED action=selected_more category=Cheat
method=CheatLightningStrike` — a retained More name genuinely dispatching through
its leaf. ⛔ Still not a licence to call other names play-proven; the census
retaining a name remains no evidence at all.
⚖️ **The stale-selection guard is NOT hand-reachable, and that is CORRECT.** Each
row captures its object at build time and refuses if selection moved
(`73:257,263`), checked twice because the async thread can outlive the click. In
play the section is simply rebuilt for the new building, so the guard is
**defence-in-depth against the async race**, not a user-facing behaviour. ⛔ Do
not send anyone to reproduce it by hand.

**Item 4 — Selected and depots: PASS, and it caught a real defect.** Fill/Empty
produced measured changes on three classes across BOTH `EF-102` branches:
`StorageFuel` 25018→180000→0 · `MechanizedDepotFood` 1490000→3950000→0 ·
`UniversalStorageDepot` ten resources →30000→0.

⭐ **THE DEFECT, and it is `EF-102` landing where that fact predicted.**
`selected_fill`/`selected_empty` carried `before=`/`after=` for `StorageFuel` and
`UniversalStorageDepot` but **NO numbers at all** for `MechanizedDepotFood`.
`depot_read` returned early whenever `storable_resources` was not a non-empty
table, so `before` stayed nil and the caller then skipped `after` too. ⇒ **The
mutation worked and only the EVIDENCE was missing** — a record that reads
`status=OK valid_after=true` while proving nothing, which is worse than a visible
failure. Fixed (TestKit `8e25f6b`) by falling back to the scalar chain
`76_SMRTK_Kit.lua:175` already used for Dump — which is exactly why Dump could
read that depot when the measurement could not. ⚠️ Needs a boot to confirm the
numbers appear.

⭐ **`EF-102` surfaced TWICE in one item** — once as the readout shape (`storage`
is a TABLE on `StorageFuel`/`UniversalStorageDepot` and a bare SCALAR on
`MechanizedDepotFood`) and once as this missing measurement. ⇒ **An agent parsing
a Dump must handle both shapes**; assuming `storage` is a table breaks silently
on the mechanized branch.

⭐ **Unplanned lead for C91, recorded so it is not re-derived.** Every Dump
carries a `modifiers` field, and it showed
`Policy_BuildingCodesStrict percent=-30 prop=maintenance_resource_amount` on a
live building. ⚠️ **This is NOT evidence of the C91 leak** — the policy is active,
so its presence is correct. It is a ROUTE: dump a building, repeal Building
Codes, dump again, and read whether the modifier survives.

#### ⚖️ STILL YOURS TO ANSWER — three open design questions

1. ✅ **Item 6 — ANSWERED BY THE OWNER 2026-09-14, and 08 had it wrong.** *"clean
   button means clean the on screen log."* ⛔ **NOT `Clean & Fix`** — 08 read the
   original *"add a clean button at the top of these lists, that gives me the easy
   quick way to clean"* as the per-object repair action and flagged it unconfirmed;
   it is the **log/readout clear** (`cls`), surfaced **at the top of every list that
   grows**. ⇒ This is the same complaint as **item 13**, not a separate ask: a
   readout that grows downward pushes its own controls off the page, so the clear
   belongs above the list, on every page that has one. ⚖️ Worth keeping as a
   precedent — the unconfirmed flag is the only reason a per-object repair button
   did not get built for a request about clearing a log.
2. **Where the slot engine lives** (bind, pins, note) once triggers move to Run — its
   own page, or riding with Probes?
3. **Defect 20's remedy shape** — cursor change, or a persistent banner?

#### ⭐ OWNER-REQUESTED WORK ITEM — the More section has never been checked

Asked again 2026-09-14 (*"did 08 include testing the rest of the buttons we imported
from the cheat menu to make sure they both work, and are useful"*) — **it did not,
and 08 recorded that as finding 16.** 08 sampled the group (Delete, Destroy, enough
of More to pass block 6, `AsyncCheatInspect`); it never enumerated it. ⛔ 03C migrated
the **84 More names by metatable walk**, so they are *"what the object exposes"* —
nothing establishes that each still does something on 1.1.0, or that the something
earns a button. Owner, at the sitting: *"I want a full round of checking in the games
logic to see if the stuff migrated over is actually working and if it is, is it
useful."*

⭐⭐ **RULED BY THE OWNER, 2026-09-14 — IT IS A DESK TRACE, NOT A PLAYTEST.** *"I mean
that not as play testing I want the next build section to answer that. Trace them and
determine if the old imported ones work and are relevant."* ⛔ **08's sizing is
SUPERSEDED** — it priced 84 presses and a dedicated sitting link; the owner wants the
**84 leaf bodies READ in the 1.1.0 source** and judged there, **inside the next build
link**, with no launch and none of the owner's hours. ⇒ Output stays a
**keep / cut / needs-rollover** list; only the route to it changes, and it gets much
cheaper.

⚠️ **What a desk trace can and cannot settle, so the verdict is honest.** Reading the
leaf answers *does this still exist, is its body a no-op, does it reference a system
1.1.0 removed, and does it do anything a playtester would want* — that is the whole
"relevant" half and most of "works". It does **not** prove runtime behaviour
(`EF-078`: trust runtime over source). ⇒ Anything the trace cannot resolve from the body
becomes a short named **needs-rollover** residue — never a silent keep, and never a
claim that it was tested.

⭐ **RUN IT AS A SUBAGENT LEG, CONCURRENT WITH THE BUILD (owner, 2026-09-14):** *"I feel
like that desk trace is a good job for a sub agent while it builds."* ✅ **And it is
structurally safe to parallelise, not merely convenient** — 03C built the More group by
**dynamic metatable walk**, not a fixed list of 84 names, so the layout work arranges a
*group*, never the individual entries. The prune therefore lands as a filter on the walk
at close-out and **cannot collide with the re-layout**. ⇒ The earlier "must land before
the layout" caution is withdrawn; it assumed a hard-coded list that does not exist.

#### ⚠️ A grading gap, recorded for 99

Block 12 (rocket transit) was scored **PASS** — the mechanism worked — while being
unusable enough that the owner preferred ultra speed. 08's verdict structure had
nowhere to record *"works, but loses to doing nothing"*. ⛔ A mechanism-only PASS is
how a chain ships something nobody uses; 99 should treat usability failure as a
verdict class, not a note.

### ✅ 2026-09-13 — 174 RULED: a fired one-off leaves the prompts map entirely
<!-- ck:174 status:ruled owner:no -->

**Owner ruling, 2026-09-13**, on finding ck170's brief `git rm`'d with its
"NOT FIRED — for Codex" row still standing in `agent/prompts/README.md`:

- **(a)** Firing a one-off deletes **the file and its row, in the same commit**.
  No tombstones: the map lists LIVE prompts only. Graves come from
  `git log --diff-filter=D -- docs/agent/prompts/`.
- **(b)** The obligation is a **machine gate**, not a habit — doccheck's
  **PROMPT MAP** holds both directions (every prompt file has a row, every row
  names a file that exists, a struck-through row is RED). Nobody has to remember.
- **(c)** The 13 struck rows and the removal-prose blocks are **purged**, not
  relocated: 10 of 13 already pointed at a `reports/` file, and the other three
  (`SITTING_158`, the `C85`/`C88`/`C89` build trio, `SITE_ALIGNMENT_AUDIT`) were
  checked to be recorded in checklist 158, the three entries' §Attended check,
  `perma/PUBLIC_SURFACE_SWEEP.md` §"When a fix is RETIRED" and STATE's site line
  before their rows were removed. `README.md` 12,659 → 4,959 B.

Why it mattered: the row is what a next session reads to decide what to fire, so
a row outliving its file points at spent work. Measured first: **13 of 14**
post-reorg consumptions did update the row, so this was a first failure and not a
pattern — but compliance was one agent's habit absorbed by another's cleanup
commit, which is not a rule. Falsifiers: the gate was shown RED on a row without
a file, a file without a row, a struck row, a dropped `perma/` row, **and on the
real HEAD README**, then restored to `sha256 27a5e29c…`.

### 2026-09-13 — 172: C92 direction RULED — build the restoration, shipping HELD
<!-- ck:172 status:ruled owner:yes -->

**You ruled this in conversation 2026-09-13; recording it so it is not only in a prompt.**

> *"We will be holding it open as a fix, I want to test it, and then we may ship it, but
> shipping is on hold until I lift the hold. Right now I want to finish it, because even
> if we never ship it I think we will gain valuable knowledge attempting it along with
> the poison pill part of the testing."*

⇒ **Build option B (restore the technology), not the narrow exemption.** Brief is
[`prompts/C92_ACHIEVEMENT_BUILD.md`](agent/prompts/C92_ACHIEVEMENT_BUILD.md), reshaped to
match. ⛔ **SHIPPING IS HELD until you lift it in words** — no release, no outbox entry,
no public row. Knowledge is an accepted deliverable even if it never ships.

⚠️ **171 is NOT thereby ruled** and stays open. 172 says what to build and that it will
not ship; 171 is still the scope decision for whether it ever does.

⭐ Testing route is settled and recorded as [`EF-094`](agent/facts/EF-094.md): **move
`account.dat` aside, test, move it back.** No mod and no retail console can clear an
achievement flag — the console *is* the mod sandbox on a retail build. The file move
resets your account options until you restore it, which is why it is your call, not an
agent's.

### 2026-09-13 — 173: FIX_POLICY §2a's version-detector ban is factually wrong in one half
<!-- ck:173 status:open owner:yes -->

§2a gives two reasons for ⛔ **DO NOT BUILD A GAME-VERSION DETECTOR**. **Reason 2 is
wrong**: it says a detector is *"unbuildable from the mod's own fields anyway"* because
`lua_revision` / `ModMinLuaRevision` are 350453 on both branches. That is true of the
**metadata** fields and false of the **runtime** `LuaRevision`, which is **403908** on
1.1.0 and tracks the build — confirmed independently from `account.dat`'s plain metadata
block (`EF-094`).

⚠️ **And we already ship a version guard.** The live FR-1 temp workaround mod goes inert
on `lua_rev ~= 403908 or assets_rev ~= 33006`. Nobody raised §2a when it was built.

**Reason 1 survives** and is the real rule: *check the thing, not its label*. The
defensible narrowing is **"use a behaviour test whenever the guarded thing is
inspectable; a version label is legitimate only where it is not"** — FR-1 guards pinned
binary shader assets, which cannot be behaviour-tested; C92's preset can be.

**Your call:** narrow §2a to that, record FR-1 as a named exception beside the existing
blanket ban, or leave it. ⛔ Left as-is, the next agent either over-applies the rule or
rediscovers the contradiction the way this session did.

### 2026-09-13 — 171: C92 — achievement repair or full technology restoration
<!-- ck:171 status:open owner:yes -->

**The [placement/icon investigation](agent/reports/C92_PLACEMENT.md) is complete.**
Your screenshot confirms the visible Underground ring is complete. The broader
Industry/Hi-Tech pass found plausible substitute art, particularly retired
`closed_loop_extraction.png`, but no intended C92 icon, seat or connection.
The earlier 44% water-bonus and technically unremovable-residue claims were
refuted; neither is a reason to reject restoration.

**Scope choice — recommendation A:**

- **A — repair the achievement.** Build the narrow exemption for this one
  verified unreachable requirement, including recovery for an already-completed
  colony and decline when the technology becomes reachable/changes/disappears.
  Preserve normal achievement restrictions and all other research requirements.
- **B — finish the technology.** Proceed with an explicit placement, prerequisite
  and art choice, plus a tested save-residue/refund contract. Underground I has
  authored family evidence; its satellite row and `UndergroundDeepMining` are
  leading design candidates, not recovered developer intent. Industry V remains
  a thematic alternative, not a proven vacancy for this tech.
- **C — defer a mod repair.** Retain the investigation for a later scope decision.

**TAKEABLE-WHEN:** the report is read; no game launch is needed to choose scope.
This item authorizes no implementation by itself. C92 stays `cand`; no fix,
award, save edit or external report was made in this investigation.

### ✅ 2026-09-13 — 170 RULED: marker semantics, LF byte accounting, and reading routes
<!-- ck:170 status:ruled owner:no -->

**Owner ruling, 2026-09-13, after the documentation-overhaul audit:**
- **(a)** Keep `open`, `ruled`, `closed`, `deferred`; a partial ruling is `open`
  with `owner:yes`. Decision status and owner action are independent. Unknown or
  malformed markers fail doccheck; duplicate numbers warn when status and owner
  agree, fail when they disagree. Preserve existing checklist numbering.
- **(b)** Normalize line endings to LF before byte accounting; caps and content stay.
- **(c)** Cite R-A…R-G where the applicable work fires, use targeted index lookup,
  and home R-D in WORKFLOW's brief-authoring section, outside working-leg instructions.

Implementation and falsifiers: [CK170_AND_FINGERPRINTS](agent/reports/CK170_AND_FINGERPRINTS.md).
The original audit questions below are retained as the condition of this ruling.

> [The audit](agent/reports/DOC_OVERHAUL_AUDIT.md) is complete, report-only. It found owner actions that disappear while doccheck stays GREEN, fingerprints that overstate what they verify, and a nested-directory reader bug behind the v10 pack-count discrepancy. Existing markers and rulings were left untouched.
>
> **Your policy calls:**
>
> - **(a) Marker vocabulary:** keep the existing words or add a partial-ruling status? **Recommendation:** keep the words, use `open` while a decision remains unresolved, and let `owner:yes` independently retain an outstanding action. Reconcile existing entries to recorded rulings in the follow-up.
> - **(b) Byte accounting:** measure normalized LF bytes, keeping the current caps? **Recommendation: yes.** Identical content can currently pass with LF and fail with CRLF.
> - **(c) Reading routes:** connect adopted R-A…R-G to actual authoring/working routes and replace mandatory full-index scans with targeted lookup? **Recommendation: yes.** Keep the author-only depth rule out of working-leg instructions and resolve inheritance versus re-derivation explicitly.
>
> Ordinary tool repairs are recommendations in the report, not changes made by this audit. **D4 is not being re-asked:** its original membership remains the scope; the current script cannot execute it and should not be applied. No old owner decision was reopened here.

### ⭐ 2026-09-13 — 169 ➊ **UPLOADED — v10 IS LIVE on both portals.** ➋ **FAQ commit DISCHARGED.** ➌ accepted as shipped.
<!-- ck:169 status:open owner:yes -->

> **➊ Receipt.** You confirmed both Paradox and Steam ran this sitting. Tree writeback: `version`
> 10 → **11**, `pdx_version` "8" → **"9"** (`pdx_id` 156049, `steam_id` 3787202810 — unchanged,
> already-listed ids). Comments restored in the same commit (`POST_UPLOAD_CLOSE.md`); doccheck GREEN.
>
> **§0.5(d) — required-game-version field:** you said the field is not offered on the page this
> upload. Nothing to set; recorded, not chased further.
>
> **§0.5(f) — delivered-bytes check.** Paradox has no local auto-download (subscribing there writes
> no file — the game pulls it at startup), so its pack is unread, same as every prior release.
> Steam's subscribed copy WAS read: `A:\SteamLibrary\steamapps\workshop\content\3215050\3787202810\
> ModContent.fpk`, **371,327 B**, md5 **`bef42a2d5405e06444b7e6efdf28cf38`**, written 2026-09-13
> 00:25 local. ⚠️ **`pack_list.py` counts 56 entries inside it; `pack_predict.py` on the current tree
> predicts 54.** The two extra entries are `smr-bug-library/SKILL.md` and
> `smr-orientation/SKILL.md` — present in the delivered archive, absent from the working tree (no
> such folders on disk, checked). Best guess: a byproduct of this session's own tooling mirroring
> skill files at pack time, cleaned up after — but that is a guess, not a checked cause. It shipped
> as two small non-code documentation files; no code loads from them (`items.lua`/`metadata.lua`'s
> `code` list is unaffected and unchanged). Flagged, not fixed — say if you want it chased down.
>
> **37 Q2 (Steam's version number)** is not reopened — it stayed closed since 2026-08-29 (both
> listings ship the same tree `version` on an update; unaffected by which portals ran which sitting).
>
> ✅ **➋ DISCHARGED 2026-09-13** — `faq.md` was committed and pushed as `d86a347` by the site-alignment
> audit (it carried the F37 promise removal). Verified in the site repo: the only files still uncommitted
> there are your own two pared ones, `content/for-modders.md` and `content/install.md` — that is decision
> **47**, not this one. The site deploy is content-clear; firing it is still your act (`workflow_dispatch`).
>
> <sub>The original ➋, kept for the record:</sub>
>
> **➋ Still yours:** `content/faq.md` in `C:\Dev\SMR-CommunityMods` is still sitting uncommitted
> beside your own paring edits (unread by any agent) — the site deploy for v10 stays blocked on you
> committing it. Everything else from the original ➊/➋/➌ block below is otherwise discharged.

<details><summary>Original 2026-09-12 ask (kept for the record)</summary>

#### ⭐ 2026-09-12 — 169 **v10 IS READY TO UPLOAD.** All the words are written and committed; the pack is waiting on your hands. Two small calls inside, and one thing only you can commit.
<!-- ck:- status:open owner:yes -->

> **The release in one line: the count word does NOT move.** Three fixes retire (F37 ghost farm
> oxygen, F43 layout tech lock, F31 cave-in on a missing map) and three arrive (C85 clogged after
> a dust storm, C88 Building Codes prefabs, C89 faction dome size), so the card still says
> **Forty-nine repairs**. ⛔ Re-derived from the fix list itself (`grep -c '^??? '` = 49, section
> tally sums), **not** carried from `WORDING_RULED.md`, which predicted *Forty-six* because it
> priced the retirements before the three new builds joined the same release.
>
> **➊ TO DO — the upload.** `docs/UPLOAD_WORKFLOW.md`, unchanged route: main menu → MOD EDITOR →
> File → Pack Mod, then **Paradox first, then Steam**. The change note and both card bodies are
> already in `metadata.lua`, so both pages auto-fill; §3 still holds the two paste blocks for the
> formatting pass. When the listings are up, tell me the three things §5 asks for and I will run
> the close-out.
>
> **➋ ONLY YOU CAN COMMIT THIS — `content/faq.md` in `C:\Dev\SMR-CommunityMods`.** C89 is a
> judgment call, so the FAQ's judgment-call count had to go **three → four** in its three places.
> That file was already holding **your** uncommitted modder-doc paring, and no agent commits over
> your unread working copy — so I edited the three count passages (`:24`, `:141`, `:145-148`) and
> **left the file uncommitted**, sitting beside your own changes. My hunks and yours do not
> overlap. ⛔ **The site must not deploy until that file is committed** — the card will say
> *Forty-nine* and mark four judgment calls, and a deployed FAQ still saying *three* contradicts
> it. The deploy was already held on your ruling for these three files, so it is the same gate.
> `content/fix-list.md` **is** committed (3 rows out, 3 in, 12 re-worded).
>
> **➌ A CALL I MADE — say if you want it different.** I added **one** new card headliner, C85's
> *"A building clogged by a dust storm never started again."*, taking the bullet list 21 → **20**
> (F37's and F31's bullets came off). It clears the *recognisable* bar — two independent player
> reports, and the symptom is a building visibly stuck with its reason on screen. C88 (one law)
> and C89 (a judgment call) I left in the *"… and a good deal more"* tail. Reversing any of that
> is a one-line edit before you pack.
>
> ⚠️ **Nothing is uploaded and `version` was not touched** (`editor/version rail (agent/prompts/perma/RELEASE.md § Release rails)`) — the bump is your sitting's.
> Detail and the byte-identity proof for all five card copies: `reports/STORE_CARD_LIVE.md`
> (2026-09-12 section).

</details>

### ✅ 2026-09-12 — 168 RULED BY YOU (batch 2): **98 → baseline moves to 1.1.0 · hardening row 3 → BUILT into v10 · 151 (c) → the three cheap checks join the owed boot.** ⏳ **151 (b) came back as a question and is answered below — the call is still yours.**
<!-- ck:168 status:ruled owner:no -->

> **(a) 98 — THE BASELINE MOVES TO 1.1.0. 1.0.7 is history.** ⛔ No branch install, no re-download.
> ⚠️ **The item's own framing was out of date and that is why it looked harder than it is:** it said a
> branch install was *"the only way to tell '1.1.0 changed this' from 'we were wrong'"*. That stopped
> being true when `C:\Dev\SMR-SrcArchive.0.7.396349\Src` was archived — **four such questions were
> settled from it on 2026-09-12 alone** (Station's paren, `Tracks.lua`'s body, `Residence`'s parents,
> Farm's removed parent). What the archive cannot give is a **runnable** 1.0.7, and the price of one is
> steep: Steam serves **one branch at a time**, so the 1.1.0 install goes away while switched, and
> `EF-079` means the entire fixture library is branch-locked anyway.
> ✅ **This also aligns the records with a ruling you already made:** ck151 (e), *1.0.7 STAYS FROZEN,
> work targets 1.1.0*. 1.0.7 players keep the frozen `v5-game-1.0.7` GitHub build (ck118).
> ⇒ **Every re-verification is now a 1.1.0 derivation.** ⛔ Existing entries are NOT re-pointed — an
> entry records a defect in the version it names, and re-writing old citations to the live tree is
> forbidden. New work cites 1.1.0; old work keeps its version stamp.
>
> **(b) Hardening row 3 — BUILT, and it ships in v10.** `Code/Fix_StaleReservations.lua`'s `OnMsg.NewDay`
> sweep now runs **one `pcall` PER COLONIST**. Before, a single throw abandoned every remaining Residence
> for that sol — and every sol after — while `ListFixes()` still reported the module `active`.
> - ⛔ **Per colonist, not per residence:** a residence-level guard would still abandon the rest of that
>   residence's list on one bad slot.
> - A raise is **logged with the residence handle and slot**, and a **separate summary line** says the
>   sweep did not complete — deliberately not folded into the "released N" line, because *"nothing was
>   stale"* and *"this sol's sweep was incomplete"* must never read the same in a log.
> - Donor shape is our own F48 pass in `90_SaveSanitizer.lua` — not a new pattern.
> - ⚠️ **Honest limit, recorded in the module:** per `EF-008`, `pcall` catches a genuine runtime error but
>   **not an `assert()` in shipped code**, because asserts do not unwind in this engine. This bounds the
>   throw case, which is what the audit raised. It cannot bound that one.
> - ✅ **Checked, not assumed:** `parsecheck` 50/50 clean · `desk_f59_expedition.py` **23/23 demands held**
>   after the change · the three TestKit probes that cover this module key on the **wrap pairs** and the
>   `SMRFixPack_reserved_at` field, not on the log text, so none is invalidated. ⛔ No public fix-list row
>   changes — this is a hardening, not a new repair.
>
> **(c) 151 (c) — F52 passage / F54 hub / C83 arrival JOIN the owed 144 (a) boot.** ⚠️ They are cheap
> **only if the colony you load already has those layouts** — a passage, a shuttle hub, an arrival route.
> ⛔ If it does not, **skip them by name and say so**; do not build the layouts to make the checks
> possible. F59's expedition check is **not** joining — it needs full housing, a competing homeless
> neighbour and a housed crew member, which is a provisioning job, not an addition to a boot.
>
> **(d) ⏳ 151 (b) — your question: "Are we completely finished with our migration passes and checks?
> Nothing outstanding?" NO. Five residuals and one unswept case, read from the entries:**
>
> | | what is outstanding |
> |---|---|
> | [F51](agent/bugs/F51.md) | 1.1.0 **PARTIAL** — stale cache desk-controlled, the permanent migration-block claim **not established**; its leg is re-filed **UNRUN** |
> | [F53](agent/bugs/F53.md) | **PARTIAL** — no fresh 1.1.0 game evidence |
> | [F59](agent/bugs/F59.md) | repaired 09-11, but the **A1 expedition half is UNTESTED** |
> | [F73](agent/bugs/F73.md) | **PARTIAL** — retained wrapper 10/10 at the desk, organic benefit unverified |
> | [F80](agent/bugs/F80.md) | still `investigating` — buildability and July incident causation **unproved** |
> | [F54](agent/bugs/F54.md) | never swept |
> | ✅ F60 · C83 | done — retired, and `tested-attended` |
>
> ⭐ **What that means for the decision, stated plainly:** the recommended scope was **written knowing
> this** — it offers F80's evidence as *"a candidate explanation, not a solved incident"* and names
> F59/F60 as **our maintenance findings** rather than game defects. So sending it does not overstate
> anything. But *"we are finished"* is not true, and if the covering note said so it would be wrong.
> ❓ **Still your call, and ck165 gives you a third option:** send the recommended scope · send nothing ·
> or **defer it as pull-only messaging** and ask for it whenever you want it. ⛔ No agent will raise it.

### ✅ 2026-09-12 — 167 RULED BY YOU: **the opt-in mod's decisions move to the opt-in mod's repo.** Eleven items off your list; three stay because they bind the fix pack. **Nothing is owed from you.**
<!-- ck:167 status:ruled owner:no -->

> **Your words:** *"Can we fully offload anything opt-in related to its repo, and just retain anything
> that's fact based that could be useful, like engine facts etc, and just rehome those facts where
> they should be?"*
>
> **Done.** Items **84, 85, 89, 90, 91, 92, 93, 94, 95, 96, 97** now live in
> `C:\Dev\SMR-OptInPack\docs\DECISIONS_OWED.md`, **reproduced verbatim** — nothing deleted, nothing
> re-summarised. The four source reports were already in that repo, so only the decisions needed
> moving. ⛔ They are that mod's launch obligations and it is not launching.
>
> ⭐ **Three did NOT move, because they bind the fix pack rather than that mod** — and this is the
> "retain anything useful to us" half of your ruling:
>
> | item | why it stayed |
> |---|---|
> | **83** | the **Test Kit is SHARED**, so those edits land in our tree. ⏸ Not owed and not urgent, but two of its five proposals (a `RunAll` owner filter, a `PACK_ID` on the enable-path leg) would improve the kit **for us** regardless of that mod |
> | **86** | `EF-###` ids are allocated **by this repo** — a rule about OUR facts index. ⚠️ **Already in force**, resolved 08-31: a fact learned there is filed here first, then mirrored. Nothing owed |
> | **88** | `FUTURE_IDEAS.md` #9 is a **fix-pack feature** (per-fix player toggles), parked there only by analogy. ⭐ Overtaken: it is what checklist **148**'s `fixtoggles/` chain builds, so it rises or falls with 148 |
>
> ✅ **On the facts half — checked, not assumed, and the answer is that nothing was stranded.** Every
> engine fact those items cite (`EF-023`, `EF-059`, `EF-069`, `EF-072`) is **already in this repo's
> `agent/facts/INDEX.md`**, which is the canonical home for both repos — that is exactly what item 86
> above enforces. So the offload rehomed no facts because there were none to rehome, and item 86 is
> the reason why.
>
> ⚠️ **One thing recorded on the way out, because it is what would most mislead whoever opens that
> file next:** all eleven were written 2026-08-31 / 09-01, **before 1.1.0 + the first DLC shipped on
> 09-08**, and **none has been re-verified since**. The new file says so at the top and tells its
> reader to re-check every citation against the live tree first. This project has already been bitten
> by exactly that: line numbers moved, modules were deleted, and some defects vanilla fixed itself.

### ✅ 2026-09-12 — 166 RULED BY YOU (batch 1 of the decision sweep): **133 (2) as a hybrid · 133 (4) label-only · 135 into hotfix 3.** All three landed the same session. **Nothing is owed from you.**
<!-- ck:166 status:ruled owner:no -->

> **(a) 133 (2) — an UNKNOWN probe answer DECLINES, and an exception is PROPOSED, never taken.**
> Your steer: *"Is a hybrid possible — do decline as a plan, but allow an agent to propose an
> exception if we ever find a need for one."* ⭐ **Yes, and it is the better rule than either option
> I offered**, because it keeps the safe default absolute while leaving a door that only you can
> open. Written into `agent/FIX_POLICY.md` **§2a (i)**:
> - Decline is the standing plan. Only a literal `true` applies — a throw, a `nil`, or any other
>   value declines. ⚠️ This is **already what the code does** (`Code/00_Core.lua:156-167`); the
>   ruling makes the existing behaviour binding so a future module cannot quietly choose otherwise.
> - An agent that finds a real case **PROPOSES** it as a checklist item — naming the module, the
>   probe, and why declining is the worse outcome there. ⛔ **An agent never self-authorises one.**
> - **No exception exists today**, and if one is ever granted it is named in that module's wording.
>
> **(b) 133 (4) — `LuaRevision` is allowed as an OBSERVATION LABEL, never as a guard.** Written into
> §2a **(ii)**. It may record **which build a reading was taken on**, in an entry, a report, a log
> line or a probe's output. ⛔ It may not gate whether a fix applies — that stays a behaviour probe,
> and **decision 118 is not weakened by a word.** The line is *describing* a build versus *deciding*
> on one. ⚠️ Worth keeping in view: `lua_revision` is **350453 on BOTH branches** (`EF-077`), so it
> could not separate them even if it were allowed to try — which is precisely why it is a label.
>
> ⇒ **133 is now fully closed.** (1), (3), (5) and (6) fell with the reword and the 73 closure;
> (2) and (4) are these. ⚠️ One loose thread it leaves, unchanged and still only a recommendation:
> `agent/prompts/SELFCHECK_PILOT.md` was authored for 133 (1), never fired, and was unreachable —
> ✅ **REMOVED 2026-09-13 on the owner's word.** Recoverable with
> `git log --diff-filter=D -- docs/agent/prompts/SELFCHECK_PILOT.md`.
>
> **(c) 135 — take the `luafn.py` delimiter fix in hotfix 3.** Small standalone change to a **desk
> tool**, not shipped code; measured to change **0 shipped hashes**, so nothing re-pins and no module
> is affected. Its blocker discharged when vanillahunt closed on 09-10. ⛔ It is **not** part of v10
> and must not be smuggled into that pass — it waits for the hotfix-3 batch, where 135 is now the
> only item left after 137/138/140/141/142 closed with 163 (a).

### ✅ 2026-09-12 — 165 RULED BY YOU: **replies to players are PULL-ONLY from now on.** Nothing is owed from you, and no agent will raise one at you again unless you ask.
<!-- ck:165 status:ruled owner:no -->

> **Your words:** *"We are gonna move replies to pull only, when I ask for them, not agent tracked.
> We keep getting side tracked with replies. Replies are as we can do them, our primary focus is
> fixing bugs, not a messaging service. And I have fielded a load of reply questions today."*
>
> **What changes, in the order an agent is most likely to get it wrong:**
>
> 1. ⛔ **No agent drafts a reply unless you ask in that session.** A new field report is not a
>    request for a draft.
> 2. ⛔ **Replies come off your owed list entirely** — `STATE.md`'s OWES line, the handoff's
>    decisions-owed table, and the "waiting on you" summary at the end of a session. They are not
>    owed. They are pulled.
> 3. ⛔ **A `DRAFT` sitting in `docs/FIELD_REPORT_REPLIES.md` is not a nudge and not work in
>    progress.** It waits indefinitely, by design. No "while you're here".
> 4. ⛔ **Nothing else is ever gated on a reply going out** — not a fix, not a release, not a sitting.
> 5. ✅ **When you ask, you get one draft and then silence** — no follow-on queue.
>
> **Applied immediately:** item **157** is the only reply currently on your list and it comes off —
> see below. Nothing was deleted; the drafts stay where they are, waiting.
>
> ✅ **WHAT THIS DOES NOT TOUCH, stated so no agent narrows it wrongly.** A player's report is
> **evidence about a defect**, and triaging one into `agent/bugs/` is **ordinary bug-fixing work and
> continues exactly as before** — the pack exists because players tell us things. What is pull-only
> is the **messaging**: writing the reply and chasing whether it went up. ⛔ No agent may cite this
> ruling to avoid reading, filing or investigating a report. Today's Foreign Aid Rocket report is the
> live example: it stays a lead, and if the reporter answers it gets filed like any other.
>
> **Where it is written down, so it binds rather than being remembered:**
> - `agent/WORKFLOW.md` authoring **rule 5b** (`R10c`) — the rule agents are bound by, placed directly
>   under rule 5, which is the mirroring obligation it carves the exception out of.
> - `docs/FIELD_REPORT_REPLIES.md` — at the very top, as the first thing anyone opening that file reads.
> - `agent/STATE.md` — in "Rules in force", and the OWES line no longer carries a reply.
>
> ⚖️ **The condition it was ruled under** (authoring rule 5a): you had fielded a day of reply questions
> while the project's actual gate was an unrun playtest. **The cost being cut is your attention being
> diverted from fixing bugs** — not the replies, which still go out as and when you want them.

### ✅ 2026-09-12 — 164 RULED BY YOU: **KEEP** — "fine as long as we are sure it won't cause issues." **The condition was checked, not assumed; it holds, and the check closed a gap.** Nothing further is owed.
<!-- ck:164 status:ruled owner:no -->

> **What was checked, because "are we sure" deserved a real answer rather than a restatement.**
>
> **1. The pass's shape, read from the CODE, not its comments.** One-shot per save (`F48_FLAG` on
> `UIColony`, gated at `:499`) · every call `pcall`'d **per track**, so a raise costs that track and is
> logged by name · it counts an **effect**, not an execution — a track counts as repaired only if its
> connection total or duplicate-`node_idx` count actually moved, so a healthy save logs a plain zero ·
> it declines cleanly, with a log line, if a game update moves `ProcessTrackElements`/`ResolveMap` · and
> it does **not** hand-assign `track.start_el`/`end_el`, which the shipped fixup does. Every one of those
> is in the executable body, not only in the header prose.
>
> **2. ⭐ A real gap, found and closed by the check.** PT-37's do-no-harm measurement (2026-08-05, you at
> the keyboard, on a copy of your own save) was taken against the **1.0.7** tree — and the function the
> pass actually calls is `ProcessTrackElements` in `Tracks.lua`, which **was not pinned by anything**.
> The manifest pinned only the fixup that was *supposed* to call it. So the safety evidence rested on a
> body nothing was watching. **It has moved:** 1.0.7 `:807-990` (184 lines) vs 1.1.0 `:807-988` (182).
>
> **3. The change is in our favour, which is what settles your condition.** 1.0.7 asserted that every
> element share one `is_construction_site` state (*"we only support all built or all under
> construction"*). 1.1.0 replaces that with `assert(el.track_obj == track)` plus a comment saying a
> **mix** of built track and construction sites is now supported, and reads `is_construction_site` per
> element at the visuals step. ⇒ 1.1.0 is **strictly more tolerant** of exactly the messy track PT-37's
> case B was written about. The failure path is **byte-identical** in both trees —
> `if not OrderTrackElements(map, elements, start_element) then return end` — an early return *before*
> `start_el`/`end_el` are touched.
>
> ⇒ **`Tracks.lua ProcessTrackElements` is now pinned** in the module, with **no `DEFECT:` line** on
> purpose: we patch nothing there and claim no bug in it. The pin exists so the next game patch that
> moves it flips `BODY-CHANGED` and forces a read, instead of silently invalidating the measurement the
> ship decision rests on. `bodycheck`: 126 OK, 0 NO-MANIFEST.
>
> ⚠️ **The one residual, stated rather than smoothed** — unchanged by today and already on the record
> from the 2026-08-11 SHIP decision: `assert` does not unwind in this engine ([EF-008](agent/facts/EF-008.md)),
> so a failure *inside* `OrderTrackElements` reports and continues rather than raising, and `pcall`
> cannot catch what never raises. PT-37 case B measured the one route the original block was written
> about and found the walk **succeeds** there. What was never established — then or now — is that the
> assert is unreachable by *every* route. **Keeping the pass does not change that risk; retiring it
> would not reduce it either**, since the same call shape is what the repair is made of.
>
> **The original ask is kept below as the reasoning you ruled on.**

> Surfaced by your 163 (d) ruling within minutes of the manifest lines going in, which is precisely
> what you bought them for. **Nothing was changed except the stale sentence; no pass was touched.**
>
> **What the machine-readable line found.** `90_SaveSanitizer.lua`'s header asserted *"F48 STAYS.
> The paren is still misplaced upstream."* It is not. Vanilla repaired it in 1.1.0 — verified on both
> sides, which is the standard this project now holds itself to:
>
> | tree | `SavegameFixups.A_StationConnectorElements3` |
> |---|---|
> | **1.0.7** archive, `Station.lua:1346` | `ProcessTrackElements(ResolveMap(track, track.elements))` — the misplaced paren |
> | **1.1.0** live, `Station.lua:1504` | `ProcessTrackElements(ResolveMap(track), track.elements)` — **corrected** |
>
> `ResolveMap` takes one argument, so on 1.0.7 `track.elements` was silently swallowed and
> `ProcessTrackElements` received `nil` — the migration re-ordered nothing, ever.
>
> ⭐ **But the upstream fix cannot heal a single existing save, and this is the part that decides it.**
> Savegame fixups run **once per save and never again**: `FixupSavegame` skips any fixup already in
> `AppliedSavegameFixups` (`CommonLua/SavegameFixup.lua:33-39`). The corrected function **kept the same
> name** — `A_StationConnectorElements3` is still the only one of its family in the tree, there is no
> `…Elements4`. So on any save where the broken version already ran, that key is set, vanilla's
> repaired body is skipped forever, and the track elements stay unordered. **Our pass is the only
> thing that repairs them.**
>
> **Reach, stated plainly:** a player on a **pre-1.1.0 save**, **off Steam**. 1.1.0 blocks old saves on
> Steam and only warns elsewhere (`config.OldSavegameBehavior`), so off-Steam players can "Load anyway".
> ⇒ **Exactly the same reach as the F35 pass in the same module, which you already ruled stays.**
>
> ❓ **Your call:**
> - ⭐ **KEEP (recommended).** Nothing about the pass was wrong — only the sentence explaining it, which
>   is now corrected in place. Retiring it would strand the one group of players it exists for, and
>   they are the same group F35 serves.
> - **RETIRE.** Defensible only if you want the sanitizer to carry nothing that depends on pre-1.1.0
>   saves — but then F35 goes with it, and that reverses item 126.
>
> ⚠️ **Left deliberately noisy until you rule:** the module's `DEFECT:` line for F48 now reports
> **`DEFECT-GONE`** on every `bodycheck` run, because the expression genuinely is gone. That is the
> honest state and it does **not** turn doccheck red (doccheck gates on bodycheck's selftest only).
> ⛔ Whoever reads that verdict next: **do not "repair" it by rewriting the regex** — the manifest says
> so in place, and this item is why.

### ✅ 2026-09-12 — 163 RULED BY YOU: **all four — (a) accept · (b) yes · (c) confirm · (d) yes.** Items 137/138/140/141/142 CLOSE with (a); **(b) RAN AND FOUND NOTHING** (`reports/PINNED_PARENTS_PASS.md`); (d) is BUILT and surfaced a new call (**164**). **Nothing is owed from you here.**
<!-- ck:163 status:ruled owner:no -->

> ✅ **RULED BY YOU 2026-09-12 — all four: (a) accept · (b) yes · (c) confirm · (d) yes.**
> **Nothing is owed from you here.** The original ask is kept below as the reasoning you ruled on.
>
> **(a) ACCEPTED — the four-group disposition stands, and it CLOSES items 137, 138, 140, 141 and 142.**
> All five are stamped closed and name this ruling. Group A (C63, C66, C82) stay candidates as
> **organic riders only** — ⛔ never provision a colony for them. Group B (C64, C67, C75, C78, C79)
> need no action ever, absent a field report. Group C (C58, C68, C69, C76, C80) and the 12 P3s of
> group D are source-only. ⛔ **A disposition, not a dismissal:** every entry stays and any field
> report naming one reopens it instantly.
> ⭐ **Done on the back of it:** [C80](agent/bugs/C80.md)'s status flip, which the disposition flagged
> as owed and unowned — its entry said REFUTED while its index row still said `cand`.
>
> **(b) ✅ YES — COMMISSIONED, RUN AND FINISHED THE SAME DAY. Nothing found; nothing owed.**
> Report: `agent/reports/PINNED_PARENTS_PASS.md`. **All seven rows resolved, no defect filed, no `Code/`
> change, no game launched.** ⛔ **Option (ii) is NOT triggered** — §1b's own rule is *"do it only if (i)
> finds anything"*, and (i) found nothing. Option (iii) stays recommended against.
> - **`Unit` + `BaseBuilding` gaining `ReactionObject`** — the two the report flagged hardest, being the
>   base classes of every colonist and every building: **12 methods, zero collisions** with our 83 hooked
>   names, and it defines no `Init`/`GameInit`/`Done`, so it never enters the composition chain.
> - **`WaterExtractor` + `ContinuousOps`** clean · **`Farm` losing `InteriorAmbientLife`** clean (deleted
>   tree-wide, provided two decorative methods, we touch neither) · **`Fireflies`** clean and strictly
>   additive.
> - **`Residence`** — the row the report left ⚠️ UNSETTLED, and our biggest exposure (4 Residence hooks +
>   6 `Building` hooks): **resolved.** `Building` moved from a transitive ancestor to a direct parent and
>   the stats parent was swapped — but `Building` is in the ancestry in **both** trees, and our four
>   Residence methods are defined on `Residence` itself. **Re-composed, not re-scoped.**
> - ⛔ **The `Station` row was a FALSE POSITIVE**, wrong in both halves: the class is not new (it is in
>   1.0.7 at `:7`, moved to `:9`) and its parent is not `Door` (it is `BuildingEntityClass`; the `Door`
>   classes are two different, also pre-existing, blocks nearby). **A pure line-shift artefact.**
>
> ⭐ **The useful output is about the instrument, not the game.** The classifier reports blocks that merely
> *moved* as new, and attributes `__parents` across adjacent blocks. So the `TABLE-HUNK` list `treediff` is
> meant to grow (`HUNT_AUDIT` §8 item 2) **must compare content between trees, not position**, or it will
> spend reader attention on rows containing no change at all.
> ⚠️ **And the cost estimate was wrong in your favour:** priced at one desk session, it took about fifteen
> tool calls, because the decisive question is a **set intersection, not a reading task**. ⛔ Do not budget
> the next pass of this kind as a reading pass.
>
> **(c) CONFIRMED — and nothing further added to the after-patch step.** `bodycheck` + `sigcheck` on
> every patch (binding, `WORKFLOW.md:156`); `treediff` + `presetdiff` on trigger, never retired. The
> archive-first step keeps its ⭐⭐: copy `ModTools\Src` **before** an update or a Steam branch switch.
>
> **(d) YES — DONE THE SAME DAY, and it paid for itself on the first run.** Both modules now carry
> machine-readable manifests; `bodycheck` reports **0 modules with no manifest** where it reported 2.
> `00_Core.lua` took a one-line `SRC: none` declaration (it is the registry and patches nothing).
> ⭐⭐ **`90_SaveSanitizer.lua`'s new pins immediately surfaced a second stale claim — exactly the
> failure you bought these lines to catch.** Its header asserted *"F48 STAYS. The paren is still
> misplaced upstream."* **Vanilla repaired that paren in 1.1.0.** Verified both sides: the 1.0.7
> archive (`Station.lua:1346`) carries the broken `ProcessTrackElements(ResolveMap(track,
> track.elements))`; live 1.1.0 (`:1504`) carries the corrected
> `ProcessTrackElements(ResolveMap(track), track.elements)`. The prose is corrected in place and the
> `DEFECT:` line is deliberately left to report **DEFECT-GONE** on every run until you rule.
> ⇒ **That is a new decision for you: checklist 164.** ⛔ The pass is **not** thereby dead — it
> repairs saves the broken migration already ran on.

> Full reasoning: `agent/reports/VANILLA_DIFF_DISPOSITION.md`. **(a) is the one that saves you
> time — it retires items 137, 138, 140, 141 and 142 in one go. (b) is a yes/no on a desk
> session. (c) and (d) are one word each. Nothing here needs you to play.**
>
> **(a) The 25 source-only candidates — rule them as GROUPS, not one by one. Recommendation:
> accept the four-group disposition below, which CLOSES items 137/138/140/141/142.** Those five
> items are five different phrasings of "provision a fixture or leave it source-only", each
> already carrying its own rider. The terminal audit re-derived all 12 P2s at the cost of a chain
> link and **zero became fixes**, so the expensive work is done and only the decision is missing.
>   - **A — worth a look, but only if you are already there (C63, C66, C82):** the only three with
>     a plain player-visible loss on an ordinary route. Keep as candidates and attach as *organic
>     riders* — "if you happen to have an RC Transport carrying two resources, click to dump one".
>     ⛔ Never provision a colony for them. Cost: **zero extra play time.**
>   - **B — the player BENEFITS (C64, C67, C75, C78, C79):** every "loss" turned out to be an
>     unearned gain or freedom. No action ever, absent a field report. Cost: zero.
>   - **C — weakened or refuted (C58, C68, C69, C76, C80):** no fixture. ⚠️ **C80 is REFUTED in
>     its own entry but its status still reads `cand`** — a status flip is owed (I left it alone;
>     that brief was read-only). Cost: zero.
>   - **D — the 12 P3s (C56, C57, C59–C62, C65, C70–C73, C81):** source-only, and no re-derivation
>     pass either. Cost: zero.
>   - ⛔ This is a disposition, **not a dismissal**: every entry stays, and a field report naming
>     any of them reopens it instantly.
>
> **(b) One bounded desk session on the blind spot that touches US. Recommendation: YES, take it.**
> The chain left ≥1,281 changed hunks that no instrument lists (I reproduced that number
> independently today — it had rested on a script that was never committed). Most of it is not
> worth reading. But I measured the part that is: **29 of the 51 shipped files our pack pins carry
> such hunks, and `bodycheck` cannot see one of them by construction.** Eight have a known
> mechanism and are real — e.g. `Unit` and `BaseBuilding` (the base classes of every colonist and
> every building) each gained a new parent in 1.1.0, and a Farm parent was removed. Whether any of
> that changes our behaviour is **unread**. Cost: **one desk session, no game, no play time.**
> ⛔ I filed no defect and am not claiming one — this is an unexamined overlap, not a bug report.
> The alternative (read all 1,281) is several sessions and I recommend against it.
>
> **(c) The instruments' schedule. Recommendation: `bodycheck` + `sigcheck` run on EVERY patch
> (now binding in `WORKFLOW.md`); `treediff` + `presetdiff` run ON TRIGGER only, never retired.**
> Your store card now publishes *"Every game patch is read against the pack as well"* — that was
> true in practice but rested on a track record, and no procedure named the tools. It does now.
> ⭐ The step that actually matters is free and irreversible if missed: **archive `ModTools\Src`
> BEFORE any game update or Steam branch switch** (~48 MB). When Steam auto-updated on 09-08 it
> overwrote the tree unasked and we only got it back because the old branch happened to still be
> offered. Do you want anything else added to the after-patch step?
>
> **(d) Two modules ship without the header that says what they correct.** `00_Core.lua` is the
> registry and patches nothing — a one-line declaration closes it, no real exposure.
> ⚠️ `90_SaveSanitizer.lua` is the real one: its header prose already names the shipped defects it
> depends on, and one of its three passes was retired earlier precisely because the game fixed the
> bug itself — caught by a human re-reading that prose, which is the expensive way. Recommendation:
> **give it the machine-readable lines** so the next one is caught in five seconds. Cost: minutes.
> ⛔ Not done — the brief was read-only.

### ✅ 2026-09-12 — 162 FULLY RULED: **(a) leave dropped · (b) cut · (c) declined on cost, C87 is file-and-watch · (d) closed with item 73.** **Nothing is owed from you; all four §4 loose ends are shut.**
<!-- ck:162 status:ruled owner:no -->

> ⚖️ **RULED BY YOU 2026-09-12 — (a) leave dropped · (b) don't remember ⇒ the loss is ACCEPTED.**
> ⏳ **(c) is still owed** — it is a 2-minute look, not a decision. ⏳ **(d) you asked for more
> information; it is below, and the call is still yours.**
>
> **(a) LEAVE IT DROPPED — closed.** F54's row ships without the dust-storm sentence. The surface
> audit's D3 had it backwards and that is now recorded in [F54](agent/bugs/F54.md) and in
> `reports/still-needed/WORDING_RULED.md`, which says ⛔ do not restore. No replacement sentence is
> offered, because the two states the fix really does leave alone are the game's two
> "exceptional circumstances" ones and no player would call either a dust storm.
>
> **(b) ✅ CUT — DONE 2026-09-12 on your word ("thats fine cut 162b").** The follow-up's posting
> condition ("post only if your 09-10 post said *still checking*") can never be evaluated, so it could
> never go up. **Both `SUPERSEDED` C74 blocks are REMOVED from `docs/FIELD_REPORT_REPLIES.md` now**
> rather than left for the v10 sweep, and both are recorded in that file's "Cut from this file, and
> why" table with the reason and a `git show` pointer to the prose. ⛔ This is an accepted loss, not an oversight — it is being recorded as a
> decision so no later session treats the deletion as a mistake and tries to reconstruct the prose.
> ✅ **Nothing of substance is lost:** both *leads* live in [C74](agent/bugs/C74.md) ("Two leads the
> fix does not cover"), re-derived from the 1.1.0 tree. Only the written reply goes.
>
> **(c) ✅ RULED 2026-09-12 — DECLINED ON COST, and the reply no longer depends on it.** Your words:
> *"162 (c) is a lead not a test, we have only ever had one report. So I am not spending time to run it
> down when we have so many other things to work on."* ⇒ **C87 is file-and-watch.**
> ⛔ **This is a pricing call, not a doubt about the lead** — the source read stands unchanged and a
> **second field report reopens it immediately**. No agent should re-ask you for this sitting.
> ⭐ **One thing it forced, and it is the reason this needed acting on rather than just recording:** the
> held reply's closing clause read *"we're checking whether it happens on every 1.1.0 map"* — a promise
> of work we have now decided not to do. **Removed**, not left to go quietly false. The reply is
> re-drafted, its hold is discharged, and it is now a plain `DRAFT` you can post whenever you like: every
> remaining sentence is source-derived and true either way. It also now says plainly that the pack does
> not touch lakes, which the reporter has reason to want in writing.
> ⚠️ The `[NEVER RUN]` recipe is kept in [C87](agent/bugs/C87.md), marked declined-on-cost, so a second
> report revives a correct instrument rather than a rebuilt one.
>
> **(d) ✅ RULED 2026-09-12 — CLOSED WITH ITEM 73. The log breadcrumb is not built.** Your words:
> *"Right now I just want to close it, we have only had the blame issue once and it was quickly resolved.
> If the problem comes up more we will revisit it."*
>
> **What this settles.** Item 133 sub-decision (5) is closed by your closure of 73, which is what one of
> the two records said all along. ⛔ **The disagreement between those two records is resolved and removed
> from both** — nobody re-derives it. Nothing was built either way, so being wrong here cost nothing, and
> the ~15 lines remain unwritten.
>
> ⚖️ **THE CONDITION THIS WAS CLOSED UNDER, recorded deliberately** (authoring rule 5a,
> `agent/WORKFLOW.md:60` — *a ruling made under a named condition expires with that condition*, the
> lesson from checklist 161): **closed because the rate is effectively zero.** The blame issue produced
> **two sightings — F104 and F105 — from one reporter on one day, 2026-08-23, and nothing since.** It was
> diagnosed and answered quickly, and neither error was ours.
> ⇒ **The trigger to revisit is named: more of them.** A further false-blame report — particularly one
> from a *different* reporter — puts this back on the table, and the argument changes when it does: the
> breadcrumb would no longer be saving an agent derivation time (that derivation is written down in
> [EF-065](agent/facts/EF-065.md), F104, F105 and 73's closure), it would be producing evidence in the
> **player's own log**, which we cannot get any other way. ⛔ Absent that trigger, do not re-ask.
>
> ⚠️ **Untouched by this:** 133 **(2)** and **(4)** are still open — one `FIX_POLICY` §2a line each.
> `agent/prompts/SELFCHECK_PILOT.md` was ✅ **REMOVED 2026-09-13** on the owner's word.

> These are the handoff's §4 — each was raised, written down, and then nothing happened.
> **(a) is already settled by evidence and only needs your agreement; (b) turns on a single
> question about a post you made; (c) is a 2-minute in-game look; (d) is a yes/no.**
>
> ---
>
> **(a) The dropped dust-storm sentence on the shuttle-hub row — recommendation: leave it dropped.
> The audit that flagged it was wrong.**
>
> The wording batch you approved drops this sentence from F54's row:
>
> > *"Suspensions the game imposes on itself — a dust storm, for instance — still count as before."*
>
> The 09-12 surface audit recorded that the dropped sentence was the **true** one and left
> "restore it?" as your call. **It is not true, and restoring it would put a false sentence in
> front of the two Paradox developers who read the fix list.** Re-derived from the game's own
> code rather than taken from the audit: a Shuttle Hub caught in a dust storm is *suspended*,
> and the game files a suspension as "can't work" — not as "not allowed to work". The shipped
> test only ever forgave the second kind. **So a dust-stormed hub never counted as available
> transport, before our fix or after it.** The two states our fix really does leave alone are
> the game's two "exceptional circumstances" ones — a law or a story event switching a building
> off, and an event putting it into emergency maintenance — and no player would call either of
> those a dust storm, so there is no honest one-line replacement to offer.
>
> Full route, link by link, is in [F54](agent/bugs/F54.md) (2026-09-12 section);
> `reports/still-needed/WORDING_RULED.md` has been corrected so no later pass restores it.
> ❓ **Your call:** agree it stays dropped (recommended, and nothing more is owed), or say restore
> and I will write a sentence that is actually true about the two states above.
>
> ---
>
> **(b) One question decides whether a written reply survives: did your Steam sounds post say you
> were "still checking" two of them?**
>
> On 09-10 you had a long sounds post for the Steam thread (C74 / C77). A **follow-up** was
> written for it the same day, to be posted **only if** your post ended by saying you were still
> checking two sounds. You cleared that item on 09-12 without saying which way, so the condition
> can no longer be evaluated — and the follow-up is now marked dead, due to be deleted at the v10
> release sweep. **Its text exists nowhere else.** (Its two *findings* are safe in
> [C74](agent/bugs/C74.md); only the written reply is at risk.)
>
> The reply says, in short: neither loose end turned out to be something players are missing — the
> Drone Hub effect was never tied to any moment in the game, and the misspelled sound is real but
> the same digging loop is already playing over that part, so fixing the spelling would just play
> it twice.
>
> ❓ **Your call, one word:** **"yes"** (your post said still checking) → it comes back as a live
> draft and you can post it whenever · **"no" / "don't remember"** → it is deleted at the sweep and
> nothing is lost but the prose. ⛔ **I have frozen the deletion until you answer** — the v10 sweep
> will not cut it in the meantime.
>
> ---
>
> **(c) The 2-minute lake check, still unrun. It is holding a reply to a player.**
>
> A player reported "Excavation too deep" blocking lakes on ordinary flat ground since the update,
> and a Paradox developer asked them for a bug report. **This is not our pack either way** — the
> check decides only whether the reply says "this is broken for everyone on 1.1.0" or "this is
> something about your map", and the reply cannot go out until it is settled. The item it was
> attached to got closed, but the check itself was never done, so it is still owed.
>
> In any 1.1.0 colony:
>
> 1. Open the build menu and choose **Lakes → Small Lake**.
> 2. Move the cursor over ordinary flat ground next to your base.
> 3. **If it places fine** — say so. It is that player's map, nothing more is owed, and the reply goes out.
> 4. **If "Excavation too deep" shows** — leave the cursor there, open the console, paste the line
>    below, press Enter, and tell me. The numbers land in the game log.
>
> ```
> local c=GetConstructionController() local o=c and c.cursor_obj if not o then print("LAKECHK", "NOCURSOR") else local x,y,z=o:GetVisualPosXYZ() local e=o:GetEntity() local m=PrefabMarkers["Gameplay.Any."..e] print("LAKECHK", e, "cursor_z", z, "ground", terrain.GetHeight(o:GetMap(), x, y), "min_z", m and m.min and m.min:z() or "NOPREFAB") end FlushLogFile()
> ```
>
> ⚠️ **One honest note about that line.** I first reported that the 09-11 version was broken and
> would have thrown, and **that was my error, caught the same day by another session**: the spelling I
> called absent is used in 19 shipped files. **The old line would have worked.** What is genuinely
> better in the line above is the `NOCURSOR` guard — if the lake cursor is not active when you press
> Enter, you get that word instead of a Lua error. Every symbol in it was traced to the shipped body.
> Details in [C87](agent/bugs/C87.md).
>
> ---
>
> **(d) Did you mean the log breadcrumb to be a separate call?**
>
> When you closed item 73 on 09-12 ("lets just close it"), one record read that as also closing
> item **133 (5)**, the ~15-line log breadcrumb, because it is the same code as 73's cheapest tier.
> A record written earlier the same day says 73's closure *implies* it but does not decide it. Both
> records carry the disagreement rather than smoothing it over, and **nothing was built either way,
> so being wrong costs nothing.**
>
> ❓ **Your call, yes/no:** **"it's closed with 73"** (recommended — it is the same work you just
> declined) → the tension note comes out of both records and nobody re-derives it · **"it was
> separate"** → 133 (5) re-opens as its own decision and stays on this list.

### ✅ 2026-09-12 — 161 CLARIFIED BY YOU: the 09-08 "we don't chase small positives" rule was **triage for the 1.1.0 emergency**, not standing policy — and it expired with the emergency. There was never a contradiction. **Nothing is owed from you; three documents stop asking.**

> **Your words (2026-09-12), on why the 09-08 ruling and the 09-09 "Leave ck126 in" never fought
> each other** — the 09-08 ruling was made
>
> > *"when we were trying to repair our mod, because our mod had the ability to do active harm. I
> > did not at the time want to concern myself with things that could do no harm and are relatively
> > minor when we was trying to get back to a functional state. I made the ruling to attempt to get
> > agents to stop focusing on [non-]game-breaking changes."*
>
> **What that settles.** The 09-08 rule (item **120**, *"we fix anything negatives, a small positive
> I am not as concerned about"*) was an **attention-routing device scoped to the 1.1.0 recovery** —
> keep agents on the things that could hurt a player while the pack itself was capable of doing harm.
> It was never a standing policy about gains versus losses. **The condition it was made under has
> lifted** — v9 is live, hotfix 2 shipped, the 1.1.0 re-verification is closed — **so the rule lifted
> with it.** Your 09-09 *"Leave ck126 in"* was ordinary judgment once the emergency framing no longer
> applied: **not a reversal, and there was never a tension for you to settle.**
>
> **What changes in practice.** Unearned-gain candidates — item 142's list is
> [C64](agent/bugs/C64.md), [C75](agent/bugs/C75.md), [C78](agent/bugs/C78.md),
> [C67](agent/bugs/C67.md), [C79](agent/bugs/C79.md) — are **ordinary candidates from now on, priced
> on cost and merit like anything else.** They are not auto-excluded by a rule, and they are not
> auto-included either. Most will still land on "file and watch", because a minor win does not justify
> provisioning a fixture — but that is a **pricing call and revisitable**, not a category ban.
> [C82](agent/bugs/C82.md) remains the one genuine player **LOSS** on that list and never depended on
> the ruling either way.
>
> ⛔ **This does not rule item 142.** You have removed the blocker; you have not said what goes on a
> hotfix-3 list. **142 stays open, now as a straight cost call.**
>
> **Where this was applied** (nothing else was touched): item **142**'s tension paragraph, item **126**'s
> "supersedes" receipt, item **120**'s scope, [F95](agent/bugs/F95.md), [C91](agent/bugs/C91.md),
> `agent/prompts/perma/HANDOFF_ORCHESTRATOR.md` §3c, and dated corrections inside
> `agent/reports/vanillahunt/HUNT_AUDIT.md` §3.4 and `agent/reports/HOTFIX_2_AUDIT.md`.
>
> ⚖️ **The lesson, and it is worth more than this case — recorded as binding authoring rule 5a in
> `agent/WORKFLOW.md`: a ruling made under a named condition expires with that condition.** Three
> separate documents (item 142, `HUNT_AUDIT.md` §3.4, `HANDOFF_ORCHESTRATOR.md` §3c) each re-derived
> this false contradiction from the record and handed it back to you as an open question — which is
> precisely the attention drain the original triage rule existed to prevent. From now on, recording an
> owner ruling means recording the **state it was made in**, and re-reading it against today's state
> before treating it as binding.

### ✅ 2026-09-12 — 160 RULED BY YOU: **(b) — let it ride with v10.** This is ordinary release-lane work, not a separate decision. **Nothing is owed from you; the original ask is kept below.**
<!-- ck:160 status:ruled owner:no -->

> **Your ruling (2026-09-12).** The store-status line is release-lane work like the five counts beside
> it — one commit, one pass, the whole page correct at once, rather than an agent making a one-line
> edit today and the same page being edited again next week.
>
> **Where it lands, and it is already staged.** All six wrong `README.md` claims — the store-status
> line included — are in `agent/prompts/perma/RELEASE_OUTBOX.md:122-138`, inside the v10 batch notes,
> with the "⛔ do NOT hand-copy these numbers, re-derive at apply time" instruction on the five counts.
> `README.md` is also `PUBLIC_SURFACE_SWEEP.md` **§3b** now, so it is on a list and cannot rot unseen
> again. ⚠️ **The `:9` line is the one of the six that needs no re-derivation** — v9 is live on both
> stores today and v10 will be by the time the pass runs — so it cannot go stale in the meantime.
>
> ⛔ **Nothing further is owed here and no agent should re-ask this.** The only remaining trigger is
> the v10 release pass itself, which is gated on checklist **158**.

> **The original ask, kept as the reasoning you ruled on. The problem, in one sentence.** `README.md` — the page anyone who clicks through from a
> Steam or Paradox comment lands on first — has never been swept, and line 9 still reads:
>
> > **Status: version 1.0.0 — prepared for first release, not yet on a store.**
>
> v9 has been live on both stores since 2026-09-12. A reporter who reads that line concludes
> the thing they are running is not the released build; **one of the two Paradox developers
> reading our fix list could conclude the same.**
>
> **Five other claims on that page are also wrong, and those are counts** — module count,
> judgment-call count, tracked findings, probe count, and the "against game version 1.0.7.396349"
> line. ⛔ Agents are **not** touching those: counts have a re-derivation protocol that belongs
> to the release lane, and they are now filed in `agent/prompts/perma/RELEASE_OUTBOX.md` under
> the v10 notes so the single v10 count pass picks them up. `README.md` is also now a numbered
> surface in `PUBLIC_SURFACE_SWEEP.md` (§3b), which is why it had rotted — it was on no list.
>
> ❓ **Your call, and it is only about line 9:**
>
> **(a) Fix it now, on its own, before v10.** ✅ **Recommended.** It is not a count, so it needs
> no re-derivation and cannot go stale between now and the upload. It is one sentence of pure
> factual error on the most-visited page we have, it costs an agent about a minute, and every
> day it stands is a day a reporter or a developer can be misled about what they are running.
> The five counts still wait for v10; nothing about this pre-empts that pass.
>
> **(b) Let it ride with the v10 sweep.** One commit instead of two, and the whole page becomes
> correct at once. The cost is that the wrong sentence stays up for however long v10 takes, and
> v10 is currently gated behind a play sitting (**158**) that needs 20–30 minutes of your time.
>
> ⚠️ Say **(a)** and an agent can do it unattended the moment you answer; nothing else on the
> page gets touched.

### ✅ 2026-09-12 — 158 RAN 09-12: all three attended in one boot; C85, C89 and C88 are `tested-attended`. **Nothing owed from you — the v10 gate is clear.**
<!-- ck:158 status:closed owner:no -->

> **THE SITTING RAN (2026-09-12, owner at the keyboard, one boot).** Log
> `agent/../archive/logs/ck158sitting_Mars.exe-20260912-21.32.07-6a91a190.log`. Boot clean: **49 of 49 modules
> applied**, **no error-shaped lines** anywhere in the session, game exited 0. Full evidence in each entry's
> **§Attended check**; the raw lines are quoted there rather than paraphrased.
>
> | leg | verdict | the artefact |
> |---|---|---|
> | **A · C85** | ✅ `tested-attended` | `released 1 building(s) stuck 'Clogged after a Dust Storm.' (load)` |
> | **B1 · C89** | ✅ `tested-attended` | same dome, 10 colonists → 0 rows changed; **9 colonists → 3 changed, GATE ACTIVE**, all `shipped=true live=false` |
> | **C · C88** | ✅ `tested-attended` | `Building Codes applied to a prefab-deployed StirlingGenerator` + `percent=-30`, maintenance 1000 → **700** |
>
> ⭐ **B1 came out stronger than the recipe asked for.** Instead of a small fixture dome it was run as a **boundary
> pair on one dome, one colonist apart** — at 10 the gate correctly does nothing, at 9 it suppresses three rows, with
> `shipped=true` on *both* sides proving the game's own rule still wanted to complain. That is a ten-colonist rule
> observed in both directions, not a blanket switch-off.
>
> ⛔ **NOT RUN, by your ruling:** **B2** (fresh colony, seated faction, `C89-PANEL total=0`). It leaves exactly one
> link unmeasured — that a `CountDome` of 0 clears the dislike from the faction's **panel** — on a vanilla path we do
> not touch. ⚖️ **Your call: ship it, reopen C89 if a field report counters it.** Also not run: C85's `(daily)` arm,
> and C88's same-type comparison, which is structurally impossible (every supplyable prefab is `require_prefab`).
>
> ⚠️ **Two things learned that were not the point of the sitting.** (1) A prefab build sets `supplied=true`, so it
> costs **no construction resources** — prefabs are free to build, and this session's source read had guessed
> otherwise. (2) `SaintBlessing` latched inactive and then **healed back to active** in this boot (:142 → :160,
> `save re-base armed for 1 preset(s) of 2`) — the first time that heal has been seen firing in play.

<details>
<summary>The recipe as it was written for the sitting (kept as the record of what was asked)</summary>


> **What is built** (all three ride v10, all three desk-checked, none of them run in a game yet):
>
> | | fix | what it does |
> |---|---|---|
> | **C85** | `Fix_CloggedBuildingRelease` | a building left "Clogged after a Dust Storm." is switched back on, including one already stuck in a save |
> | **C89** | `Fix_FactionDomeSizeGate` | ⚖️ **judgment call** — all five factions wait for ten colonists in a dome before disliking its unemployment or homelessness |
> | **C88** | `Fix_BuildingCodesPrefab` | Building Codes applies to prefab-deployed buildings, as its description says |
>
> **Cost to you.** C85 and C88 are a few minutes each on any 1.1.0 colony. **C89 needs a fresh one-shot
> colony and about 20–30 minutes of ordinary play to warm up** — a first dome with colonists, the Martian
> Assembly, and a second small dome. That is real play time, not a fixture you can load, and it is the
> leg you said you wanted to observe. If you only have ten minutes, do **A** and **C** and leave **B**.
>
> **Before you start:** open the console (`~`) once and paste this, so every line the fixes print lands in
> the log where you can read it back:
>
> ```
> FlushLogFile()
> ```
>
> After each leg, paste it again and the lines are in the log.
>
> ⚠️ **Some lines below start with `*r ` or `*g `. Type them exactly as written, prefix included.** This
> console needs that prefix for anything longer than one statement (`PLAYTEST_HELP.md`, "Console input
> forms"): `*r` runs it immediately, `*g` runs it on the game's own clock, which is what anything that
> *changes* the colony needs. A line pasted without its prefix will look like it did nothing.

---

#### A · C85 — a clogged building comes back (minutes, any colony, no storm needed)

The fix keys on the exact state the dust-storm event leaves behind, so you can put a building into that
state directly instead of waiting for a storm.

1. Load any 1.1.0 colony. Select a **Metals Extractor** (or any extractor, Polymer Plant, Fuel Factory or
   Fungal Farm).
2. Open the console and paste:

   ```
   *g SelectedObj:Setexceptional_circumstances(true, StoryBits.BuildingClogged.ActivationEffects[1].Reason)
   ```

   (The `*g ` prefix runs it on a game-time thread — the same kind of thread the
   dust-storm event uses for this exact call, so it is the faithful version.)

   **First-screen witness:** the building stops and its info panel says **"Clogged after a Dust Storm."**
   If it does not say that, stop — the rest measures nothing.
3. **Save**, quit to the main menu, and **load that save**.
4. **What you should see:** the building is working again.
5. **The control — this is the part that matters.** Paste:

   ```
   FlushLogFile()
   ```

   and find this line in the log:

   ```
   [CommunityFixPack] CloggedBuildingRelease: released 1 building(s) stuck 'Clogged after a Dust Storm.' (load)
   ```

   **No line = the fix did not do it**, and a working building proves nothing on its own. One line with
   `(load)` is the pass.
6. *Optional, same colony:* instead of saving, leave the game running at high speed until the next sol.
   The building clears and the line reads `(daily)` instead of `(load)`.

> ⚠️ **One thing this does NOT test, and it is the only claim of ours never checked in play:** that *nothing
> in the game itself* ever clears this. To see that you would have to switch the whole pack off in the Mods
> Manager, restart, do steps 1–3, and watch the building stay dead across a sol and a reload. It is a whole
> extra boot. **Say the word and it becomes its own item — I am not asking for it here.**

---

#### B · C89 — ⚖️ the judgment call you asked to watch (a fresh one-shot colony)

⚖️ **Read this first: this is not a repair of a code error.** Four factions count a dome of any size when
they judge "more than 10% unemployment"; the Justice Movement waits until a dome has ten colonists. The fix
gives the other four the Justice Movement's own rule. Nothing here says the game was wrong, and every public
surface will say "judgment call".

**B1 — the two-second version, and it is the real falsifier.** You can do this on *any* colony with a dome,
before building anything. Select a dome and paste:

```
*r SMRFixPack.FactionDomeGate.Report(SelectedObj) FlushLogFile()
```

The log gets one block. On a dome of **under ten** colonists with at least one idle or homeless, it reads:

```
[CommunityFixPack] C89-AB dome=Dome colonists=3 unemployed=1 homeless=0 threshold=10
[CommunityFixPack] C89-AB   ProsperityUnemployment   shipped=true live=false
[CommunityFixPack] C89-AB   ... six more rows ...
[CommunityFixPack] C89-AB 7 row(s), 7 where the gate changed the answer -- GATE ACTIVE on this dome
```

`shipped=true live=false` is the whole fix in one line: **the game's own rule would have complained about
this dome, and with the fix it does not.** On a dome of **ten or more** every row reads
`shipped=true live=true` — the gate changes nothing there, which is the control that we have not simply
switched the dislike off. ⛔ If it says `GATE-ABSENT` or `shipped=not-wrapped`, the fix is not applied and
nothing below is worth doing.

> ⚠️ **Why there is no "switch the fix off" leg here, since that is how we normally do an A/B.** Turning one
> module off needs a restart with the whole pack disabled, because this one edits the faction data once at
> load. The `shipped=` / `live=` pair above gives you the same comparison **in the same boot, on your actual
> dome** — `shipped=` is literally the game's own rule, kept aside so it can be asked. If you would rather
> have the real pack-off leg as well, say so and it becomes its own item.

**B2 — the colony, if you want to watch the faction itself.** This is the 20–30 minutes.

1. Start a **new colony**, any sponsor except one playing with *No Politics*. Build the first dome and get
   colonists into it as you normally would.
2. Build the **Martian Assembly** (a dome spire — 40 Concrete, 20 Metals, 20 Polymers; **no research
   needed**). Until it stands, the player factions have no seats and none of this can fire.
3. Let a sol tick over. Then paste:

   ```
   *r local n=0 for id in pairs(g_Legislature.legislature_members) do n=n+1 SMRFixPack.Log("C89-SEATS %s", id) end SMRFixPack.Log("C89-SEATS total=%d", n) FlushLogFile()
   ```

   The last line always prints a `total=`, so "no seats" reads as `total=0` rather than
   as an empty result you have to interpret.

   **You need at least one of these four to be seated:** `ProsperityForMars`, `MarsDemocraticParty`,
   `WorkersParty`, `NewSol`. ⚠️ **There is no cheat that seats a faction** — I looked, and the game has
   none. Seats come from which faction your colonists support, so if none of the four is seated, keep
   playing a sol or two, or accept that this leg cannot run today and say so. **Do not force it.**
4. Build a **second, small dome**, and here is the part that makes the reading real: **do not connect it by
   a passage, and put no workplace inside it.** Move **three adult colonists** into it. With nowhere to work
   they are genuinely unemployed, and the game will keep them that way — no console cheat needed, and
   nothing to undo itself a minute later.
5. With the small dome selected, paste the B1 line again. It should read **3 colonists, 1+ unemployed** and
   `GATE ACTIVE`. That is the control that the dome really does qualify — without it, "the faction said
   nothing" could just mean the dome never counted.
6. **Now watch, across one game hour:** the faction does **not** announce "dislikes: high unemployment", and
   its panel does not list **"Domes with more than 10% Unemployment"** — while that dome still reads three
   colonists with one or more idle.
7. **The number to quote instead of a screenshot.** Paste:

   ```
   *g g_FactionsHolder:RecalcFactionsApproval("all factions") local n=0 for fid,a in pairs(g_FactionsHolder.factions_approval) do for _,r in ipairs(a.likes_data or empty_table) do if r.id and (string.find(r.id,"Unemploy") or string.find(r.id,"Homeless")) then n=n+1 SMRFixPack.Log("C89-PANEL %s %s value=%s", fid, r.id, tostring(r.value)) end end end SMRFixPack.Log("C89-PANEL total=%d", n) FlushLogFile()
   ```

   With the fix on this should print **`C89-PANEL total=0`** and no rows. (It re-runs the game's own faction
   maths for every faction immediately, so you do not have to wait for the clock; `*g ` runs it on a
   game-time thread, which is where the game itself runs it.)
8. ⭐ **The strongest leg, and it is one click:** move **seven more colonists** into that small dome so it
   has ten. Paste the line from step 7 again — now the dislike **appears**. That shows the fix is a
   ten-colonist rule and not a blanket switch-off, which is the thing I would most want you to see.

> `tested-attended` for C89 is yours to grant after this, and nothing else grants it.

---

#### C · C88 — Building Codes reaches a prefab (minutes, needs the law)

⚖️ A Paradox developer answered the reporter's thread: excluding prefabs is wrong, it is fixed in their next
patch, and they asked us to carry the fix meanwhile.

1. On a colony that has the **Martian Assembly**, enact **Building Codes → Strict**.
2. Order a **prefab** of a building that needs maintenance, and deploy it. ⚠️ **Pick one whose info panel
   shows a maintenance figure at all** — on a building with no maintenance there is nothing to see and the
   whole leg is empty.
3. **First-screen witness**, in the log:

   ```
   [CommunityFixPack] BuildingCodesPrefab: Building Codes applied to a prefab-deployed <building>
   ```

   No line = the fix did not fire.
4. Select that building and paste:

   ```
   *r SMRFixPack.BuildingCodesPrefab.Report(SelectedObj) FlushLogFile()
   ```

   The log should show `modifier id=Policy_BuildingCodesStrict percent=-30`. If it instead says
   **"NO Building Codes modifier on this building"**, the fix did not work — the line says so on purpose, so
   a quiet log cannot read as a pass.
5. **The comparison:** build the **same building type normally** and check its maintenance. The two should
   now match. Before this fix the prefab one was higher.

> ⛔ **Buildings already standing cannot be fixed, and that is not a gap in the test.** The game does not
> record that a finished building came from a prefab, so there is nothing to find. The fix reaches buildings
> completed after it is installed, which is why step 2 deploys a fresh one.

---

#### Two things I found while building these, neither of them needing you today

- **C90 — a bug in our own pack** (`agent/bugs/C90.md`). A module whose safety self-check *fails* can still
  bypass that decision. **Measured at the desk 09-12:** Sinkhole writes both flags after a missing-target
  decline; Saint rewrites old-branch data or arms its 1.1.0 save repair. Both then report **active** again,
  clearing the failed self-check from the update warning. No field trigger is established. **Ruled and built:**
  guard the two modules; the shared core's apply-verdict contract is unchanged.
  C89 already guards its pass; neither current OnDataReady caller exposes the same data-write gap.
  **Production guards built 09-12; status `fixed`, unexercised in play.** Original measurement:
  `agent/reports/DESKBENCH_C90.md`; build controls and reset finding: `agent/reports/C90_GUARDS_BUILD.md`.
  - ✅ **RULED 2026-09-12: the bounded shape — per-module apply-success guards in `Fix_SaintBlessing` and
    `Fix_SinkholeIndestructible`.** ⛔ **NOT** the shared core's apply-verdict contract; the four DataPatch
    callers and `OnDataReady` are out of scope. ⛔ **Hard constraint, carried by both `agent/bugs/C90.md` and
    `agent/reports/DESKBENCH_C90.md`: do not gate the pass on `entry.status == "active"`** — `run_apply` sets
    status only *after* apply returns, so a legitimate live re-apply calls the pass while the previous status is
    still inactive. Any implementation must also define reset/retry behaviour rather than treating a once-true
    flag as an everlasting success verdict. **SOURCE: reset is moot on today's path** — Register applies
    once, Mod Options retries only `def.optional`, and none of these modules is optional; Lua reload
    recreates the local false flag. C89's claimed stale-verdict retry gap is refuted within that ordering;
    its attended module is unchanged. A future retry path must reset before Require.
  - ✅ **RULED 2026-09-12 — v10 CARRIES C90.** The owner pulled the build forward onto the launch path and
    asked for a prompt, now fired and removed; evidence is `agent/reports/C90_GUARDS_BUILD.md`. Scope is
    unchanged — the two modules only. ⛔ It ships **unexercised**: the guard cannot fire on a healthy 1.1.0
    install, where no target is missing, so the honest status is `fixed` on desk evidence and **never**
    `tested-attended` (the ck130 Saint-heal precedent). C90 gets **no public row** — our own bug, invisible
    to players. Both Saint and Sinkhole changed; the release outbox names both for batch accounting.
- **C91 — the game leaks the Building Codes maintenance change on repeal** (`agent/bugs/C91.md`). Repeal the
  law and every building it touched keeps the maintenance change; the developers clearly know, because they
  shipped a one-time save cleanup for it rather than fixing repeal. **Good material for the developer
  thread.** Our fix uses the law's own id precisely so it leaks the same way and is cleaned by the same
  sweep — one more building in an existing leak, not a new one.

#### One housekeeping flag for whoever uploads v10

**Resolved 09-12:** `tools/desk_migration_cluster.py` now reads F60's pre-retirement body from git.
All 16 original demands remain, including every F51 leg and both F60 harm legs. Full deskbench is green:
20 harnesses, 254/254 numbered demands plus three unnumbered harnesses. This repairs the pre-existing
failure from F60's deleted file; it is desk evidence, not release clearance or an attended playtest.

</details>

### ✅ 2026-09-12 — 159 RULED 09-12: F31 retires, F37's load-time clean-up is a loss you accept, and every sentence replacement goes in. **Nothing owed from you; the release lane carries it into v10.**
<!-- ck:159 status:ruled owner:no -->

> ✅ **LANDED 2026-09-12.** All three retirements are in: `Fix_GhostFarmOxygen`, `Fix_LayoutTechLock` and
> `Fix_AnomalyCaveInMap` are deleted from `Code/`, `items.lua` and `metadata.lua` together (module-list gate (tools/doccheck.py MODULE SETS + tools/upload_preflight.py)), and the four
> entries (F37, F43, F118, F31) are restatused. **The tree now reads 47 Code files / 46 registered modules, all
> three sets agreeing by name.** ⛔ **The count word below ("Forty-six") predates the landing — the release lane
> re-derives every count from `doccheck --emit-counts` and carries none.** The site row, the card headline and
> the fix-list rows are still to do: they are the v10 publish's job, not this landing's.
>
> **What you ruled (2026-09-12), all three as recommended:**
>
> 1. **Retire F31 — yes.** Module out (module-list gate (tools/doccheck.py MODULE SETS + tools/upload_preflight.py): `items.lua` entry), the site row off, the card headline off, the
>    count word to **Forty-six**.
> 2. **F37's load-time clean-up — accept the loss.** It does **not** move into `90_SaveSanitizer.lua`.
> 3. **All three sentence replacements approved — "3 all" — and the optional fourth (F73) with them.** All four
>    are applied verbatim to [WORDING_RULED.md](agent/reports/still-needed/WORDING_RULED.md) (2026-09-12): item 1
>    (F54), item 3 (F58), item 12 (F48), item 14 (F73). That file is the source the release lane reads.
>    ⛔ **Nothing was pushed to the live public surfaces** — `content/fix-list.md`, the card and the site are the
>    release lane's job at the v10 publish (`agent/prompts/perma/PUBLIC_SURFACE_SWEEP.md`).
>
> ⚠️ **One thing to know, not a decision anyone made for you.** The ruled batch *drops* F54's dust-storm sentence
> ("Suspensions the game imposes on itself — a dust storm, for instance — still count as before") on the grounds
> that the case was never measured. The audit found the opposite: a hub the *game* has paused does still count, on
> purpose, so **the dropped sentence was the true one** (audit D3). It has **not** been restored — say the word if
> you want it back on the row.

> **What the audit found** ([full report](agent/reports/SURFACE_AUDIT_2026-09-12.md)): the farm-oxygen fix (F37) and the
> layout fix (F43, with its F118 rider) are redundant on the current game exactly as you ruled — traced from the shipped
> code, callers and inheritors counted, nothing found that Codex missed in the other direction. The one loose end
> Codex named on F37 (a worker dying during a refab) is closed: the game kicks the workers before the building goes, and
> no farm inside a dome can run with none.
>
> **F31, the "cave-in on a map that does not exist" fix — dug to the bottom, as you asked.** Nobody ever saw the story
> stop: no save, no log, no report, on either game version — the row was written from the code. Your lead held (the
> "No Asteroids and Underground" rule is marked obsolete on 1.1.0, so a new game cannot pick it). The two routes left
> open are closed too: the audit read the map data inside all 142 map packs, which no earlier audit had done. The
> sequences that call for a cave-in exist only on the underground map itself, so the map they name is always the map
> they run on. There is no non-surface map a player can start on. And on 1.0.7 the rule removed the underground map
> and every story that could ask for a cave-in with it, so that player could not hit it either.
>
> **(1) Retire F31?** Recommended **yes**: module out, row and headline off, count word to Forty-six. The only other
> honest option is to keep the module as silent insurance for other mods with **no** public row, because there is no
> true sentence to write about a symptom nobody can have.
>
> **(2) One thing the F37 retirement also removes:** its load-time clean-up. On Steam a 1.0.7 save cannot be loaded at
> all, but on Paradox/console the game only warns and offers "Load anyway", so a player carrying an old save with a
> phantom oxygen bonus loses the clean-up. You kept the save sanitizer's passes for exactly that crowd (item 117).
> Recommended **accept the loss** — the leak needed a farm salvaged before it ever worked, and the developer could not
> reproduce it — or say "move it" and the release lane puts the clean-up into the sanitizer as a third pass.
>
> **(3) Three sentences from item 156's batch overstate what the fix does; the replacements are written to ship:**
> - Item 1 (shuttle hubs): "Only hubs that are on and able to fly count" — a hub the *game* has paused still counts, on
>   purpose. → **"a hub you switch off stops counting. Only hubs you have left switched on count."**
> - Item 3 (reserved beds): "a colonist who had died, left, or moved to another dome" — the game already frees the bed on
>   death and on moving in elsewhere; the bug is the colonist who never arrives. → **"a bed could stay reserved for a
>   colonist who was never going to arrive — one still waiting for a ride that never came, or one who set off on foot —
>   and those reservations are invisible in the interface."**
> - Item 12 (old-track repair): "that track is put back the way it was" — the game restores only the order of the pieces.
>   → **"A track it cannot sort keeps its old order, and the rest carry on."**
> - Optional, item 14 (vacuum reflex): "a colonist with a home" → "a colonist whose home is up and running", since a
>   switched-off home does not call them in.
>
> Everything else in the batch is true at the shipped line. Counts: the audit's arithmetic agrees with item 156's
> (Forty-seven, or Forty-six with F31), but the module and file totals must be re-read at release time because the
> C85/C88/C89 build is adding three modules to the same update.
>
> Required doccheck line, verbatim: `warn STATE.md is 13722 bytes, warn threshold is 12288 — copy this line VERBATIM
> into the owner report; the owner fires agent/prompts/perma/STATE_EVICTION.md` (STATE was not touched by this audit).

### ⏸ 2026-09-12 — 157 — **OFF YOUR OWED LIST 2026-09-12 under the pull-only ruling (165).** Both calls are messaging, not fixing: (a) the reporter reply is a **draft waiting in `docs/FIELD_REPORT_REPLIES.md`, pulled when you want it** · (b) the developer note is **yours to route whenever** — ⚠️ worth knowing it carries more weight than an ordinary reply, because two Paradox developers plan hotfixes from our fix list, but it is still not owed and no agent will raise it again. ⛔ **The triage underneath this item stands and is unaffected.** Original ask kept below.

### 2026-09-12 — 157 (the original ask): new Steam report, "Prosperity for Mars angry about unemployment with 0 unemployed" — triaged, not ours. **Your pushback checked out: it is an oversight, and the developers' own fix exists in one faction out of five. Three decisions: (a) post the reporter reply, (b) hand it to the developers, (c) carry a judgment-call fix ourselves. Recommendations: (a) yes, (b) yes, (c) not yet — wait for their answer.**

> **What your pushback found (added later the same day):**
> - **Five factions** carry the identical "dome with 10 % unemployed" dislike (Prosperity, Mars Democratic Party,
>   Workers' Party, New Sol, Justice Movement), and the Homeless twin on four of them. **Only the Justice Movement
>   guards it with "at least ten colonists in the dome".** The other four fire on a dome of three with one idle
>   colonist. Same on 1.0.7, so not a regression.
> - **Every like of every faction is polled the same way:** once an hour, the whole list is re-evaluated and stored;
>   the panel shows the stored list, and a dislike that was absent the hour before fires a notification. So a blip is
>   held for one hour, and a flickering one notifies every time it comes back. Not a perpetual lock.
> - **The ratchet is daily:** at hour zero the faction's tension rises if approval is below the threshold at that
>   moment and only falls on days it is above. A midnight blip costs a day of tension.
> - **Large colonies are worse for a measurable reason:** a colonist who loses a job only looks for another every
>   (colonists ÷ 300) hours, capped at twelve. At 3,600 colonists that is half a sol idle per lost job.
>
> **(c), the fix shape if you want it:** apply the Justice Movement's own "ten colonists" gate to the other four
> unemployment filters and the three homeless ones. It is the game's own rule, applied consistently — a judgment
> call under our policy, not a code error, so it would sit beside the Biorobots and asteroid-vacuum rows. The
> hourly sampling itself stays theirs. Entry: [C89](agent/bugs/C89.md). Developer note drafted below the reporter
> reply in `FIELD_REPORT_REPLIES.md`.
>
> **Gut check you asked for (same day):** an average-good player keeps Prosperity content almost regardless. One
> dome blip costs 300 and all domes together floor at 3,000, while the faction pays 1,500 for smart residences,
> 900 and 1,200 for the two extractor types, 1,500 for factories and 1,500 again for three shifts — a player who
> builds toward it has 3,000 to 6,000 of headroom and "content" needs zero. Only a player hovering near zero is
> tipped, and tension needs several bad midnights in a row. The ten-colonist guard protects the first dome and a
> dome that is still filling; a dome of ten with one idle worker trips it either way. The twelve-hour idle figure
> is the quiet-colony ceiling — any workplace change in the cluster re-sweeps the idle immediately. ⇒ the harm
> the reporter saw is the notification and the hour-stale panel, and a guard would not touch that. ~~**Revised
> recommendation for (c): no.**~~ For (b): the report came through our channel, so the route is the fix list the
> developers already plan from, or the Building Codes thread where their developer is active.
>
> **Corrected by you, and it holds (third pass):** that headroom is mid-game. In the early game — the hardest and
> longest-felt phase, most of it at 1× — smart residences and factories are far off, so Prosperity's positives are
> zero and one dome blip is the whole distance from content to not content. And the code lets the player factions
> be live from the first dome: the Assembly is a 40/20/20 spire with no research or population requirement. In
> that window every filling dome sits under ten colonists with its jobs still under construction, so the unguarded
> filter fires every hour until they exist. The developers had **two** instruments for exactly this — the Justice
> Movement's ten-colonist gate, and a per-like "MinColonists" setting that Prosperity uses on one other like — and
> applied neither here. **(c) recommendation now: yes**, as a judgment call: apply the Justice gate to the four
> unguarded unemployment filters and the three homeless ones. It can ride the C85/C88 build if you say so — I
> would add it as a third item to that prompt before you fire it.
>
> ✅ **(c) RULED YES (you, same day): "bring them to 10".** Your question — do the other unemployment-dislike
> factions have a minimum guard? **No.** Only the Justice Movement has one (its ten-colonist dome gate, on both
> unemployment and homeless). Mars Democratic Party, Workers' Party, New Sol and Prosperity have no dome gate, no
> MinColonists and no MinSols on either. **Added as the third item to `agent/prompts/C85_C88_BUILD.md`**: four
> unemployment filters brought to ten, **and the three unguarded homeless twins on the same precedent** — that
> half is my inclusion; strike it in the override slot at the top of the prompt if you want unemployment only.
> Still open here: (a) post the reporter reply, (b) the developer note's route.
>
> ⏳ **(a) and (b) STILL OPEN — reviewed with you 2026-09-12, no ruling.** You had not got to them. Both drafts
> stay live and unposted in `FIELD_REPORT_REPLIES.md` (the C89 reporter reply, gate ck157 (a); the developer note,
> gate ck157 (b)), plus the C89 follow-up line drafted for v10.
>
> 🎮 **You flagged this one for an in-game A/B you observe yourself, on a one-shot colony.** The build brief now
> requires a fresh-colony recipe: first dome, Assembly built, one of the four factions active, a small second dome
> with three idle adults, fix-off then fix-on across one game hour each, with copy-paste reads of the dome counts
> and the like's value. The build session writes it as its own checklist item; `tested-attended` for this fix is
> yours to grant after that sitting.

> **What it is:** the faction's "high unemployment" dislike is a **once-an-hour snapshot** (stored and shown on the
> panel until the next hour, and it fires a notification the first hour it appears), while the top-bar Unemployed
> number is **live**. The dislike counts any working dome where one in ten colonists who could work has no job at
> that moment — so one idle colonist in a small dome, a shift change or a switched-off building at the top of the
> hour is enough, and the bar can read 0 a minute later. Nothing in the pack touches any of it. Entry:
> [C89](agent/bugs/C89.md). It does **not** join the C85/C88 build; fire that as written.
>
> **If it persists across hours with the bar at 0** it is something else (a stale dome label), and the reporter's
> save would pin it. The reply asks for exactly that. Draft: `FIELD_REPORT_REPLIES.md`, 2026-09-12 section.

### ✅ 2026-09-12 — 156 RULED: retire the farm-oxygen and layout fixes, the frozen 1.0.7 build stays as it is, the wording goes out in your voice. **Nothing owed from you until the audit reports.**
<!-- ck:156 status:ruled owner:no -->

> ✅ **THE RETIREMENTS LANDED 2026-09-12** — see the ✅ block on item **159** for what the tree reads now. F37's
> F118 rider went with its parent, and that removes **our own** defect outright: F118 was caused by
> `Fix_LayoutTechLock`'s own teardown, so deleting the module deletes the cause. ⛔ It was never reproduced, so
> nothing there licenses a public row or a "fixed" claim.
>
> **What you ruled (this morning):** retire F37 (farm oxygen) and F43 (layout research lock, with its F118 rider); the
> frozen 1.0.7 download is untouched; the wording batch is approved with your corrections — items 1, 2, 6, 7, 9, 10,
> 11, 14 polished, items 3, 8, 12 rewritten plain (they were word salad), item 4 held. The final text is
> [WORDING_RULED.md](agent/reports/still-needed/WORDING_RULED.md); Codex's original stays on file unedited.
>
> **Your voice rule is now written down and binds every public surface** (top of that file, and in the sweep sheet):
> plain enough for the players, precise enough for the two developers, and no "no guarantees" / "unverified" hedging
> on anything public — scope is said by stating what a fix does and for whom. Word salad fails.
>
> **Item 5 (train wait time) — why it is not a retirement:** on 1.1.0 the double-counted wait still feeds the
> **"Travel time (rolling average)"** line on every train and track info panel. Only the Comfort penalty is gone from
> the game. So the fix still repairs a number you can see; the Comfort claim comes off the row and the card.
>
> **Item 13 (cave-in on a missing map) — sent to a deep audit, as you asked.** The Fable brief is
> `agent/prompts/SURFACE_AUDIT_FABLE.md`: it re-derives both retirements, digs F31 to the bottom on both game
> versions (was the stop ever observed; **your lead checks out: the No Underground rule is marked obsolete on 1.1.0,
> so that route is closed on the live game** — the audit settles the remaining routes), checks every ruled
> sentence against the code, and has your standing licence to dig into anything it thinks is closer to retirement
> than Codex thought. It touches no public surface. **Fire it in a fresh Fable session.** After its report: the
> release lane applies the batch as v10, you upload, paste if needed, and run the site job once.
>
> **The site job:** held for v10 by your choice, recorded. Until then the live fix list shows 50 entries (with the
> retired dome-housing fix) while the card says Forty-nine. Fine for days; say so if it stretches.
>
> The original item follows for the record.

Your still-needed sweep ran across **all 46 modules** on **1.1.0.403908**:
**2 retirement recommendations, 0 rebuilds, 30 keeps, 14 claim corrections or
qualifications**. [Complete evidence/table](agent/reports/STILL_NEEDED_SWEEP.md),
[exact proposed wording](agent/reports/still-needed/SURFACE_PLAN.md).
Fresh direct registry read measured **46/46 active**, including Saint's retained
healing disposition; F102's replacement entity was valid. These are installation
reads, not cure witnesses. A real Station native control also settled F46's old
unknown: disabled demand still reported target2500, with exact restoration.
All 121 original saves remained hash-identical; no temporary probe remains.

Decisions for you:

- **F37 farm oxygen:** recommend retirement for normal 1.1.0 salvage/destruction;
  vanilla now clears the modifier before removal. This reinforces item150(c).
  Choose retirement or explicit legacy/orphan-healing retention. Refab dying-worker
  and custom removal residuals are unmeasured, not verified defects.
- **F43 layout filter, with F118 rider:** recommend retirement on stable normal
  1.1.0 menu/shortcut admission; vanilla now gates research and owned prefabs
  outside it. Choose retirement or named 1.0.7/custom/cached-race retention.
  It is no longer justified as a current defect hidden only by shipped numbers.
- **Retained scope:** approve historical/dormant F40 prevention plus existing-carrier
  healing, F48 affected-save latch healing despite corrected vanilla migration,
  and F31 argument guards as insurance rather than an unconfirmed stopped-story
  account; or commission a different who-benefits decision. Saint's existing
  historical/1.0.7 ruling remains; its row only needs dome/Religious scope.
- **Wording batch:** approve the linked 14 corrections/qualifications, including
  obsolete train Comfort benefit, drones called colonists, ordinary-foot reservation
  cleanup, bounded Crystal/Extender outcomes and available-passage wording.
  The F52 headline change is an inferred precision recommendation, not a new defect.

**Nothing is retired or rewritten publicly yet. Not part of v9's F59/F60 upload.**
The review is queued in PUBLIC_SURFACE_SWEEP and RELEASE_OUTBOX as **Held after-v9**.
Takeable after that close-out and your ruling. Retiring both predicts 49 ->47 rows
and 46 ->44 modules; final release counts must be rederived. Current hidden-repair
claim supports **two** rows rather than three; judgment rows still three, Lake veto
key still ships, and seven-machine wording remains true. Broad current suite,
actual F46 unloading and named in-play/save/legacy residuals remain unmeasured.

Required owner report warning (STATE was left untouched):

```
warn STATE.md is 12991 bytes, warn threshold is 12288 — copy this line VERBATIM into the owner report; the owner fires agent/prompts/perma/STATE_EVICTION.md
```

### ✅ 2026-09-11 — 155 CLOSED 09-12: you answered the upload receipts, and the answer is standing — **the documents will stop asking.**
<!-- ck:155 status:closed owner:no -->

> **Your answer (2026-09-12), recorded as your word:** the descriptions **always auto-fill**, but the **formatting
> does not survive**. You fix it with the copy-paste backups and do a **cleanup pass on both Steam and Paradox**.
> It is minor — the auto-fill gives the page something until the cleanup lands. **The method is satisfactory.**
>
> ⇒ **"I keep getting this question."** So it is no longer a question. `UPLOAD_WORKFLOW.md` §2, §3 and §5 now
> record the known answer instead of asking whether the fill worked and whether you pasted; the same ask is
> removed from `agent/prompts/perma/RELEASE.md` §2/§3/§4/§6. What a receipt still asks for is only what varies
> per upload: the version the Paradox page shows, anything that looked wrong, and whether the site published.
> ⛔ The §3 paste backups stay REQUIRED and stay current every sweep — your answer is *why* they are, not a
> reason to drop them.

> **Update 2026-09-12 (`smr-bugfixpack-d0`): v9 is live too, and it is closed out.** The Steam changelog shows an
> update at **Sep 11, 9:11pm** (Pacific) carrying the F59/F60 note word for word, the page body says "Forty-nine
> repairs", and the pack your client downloaded at 00:25 is 337,653 bytes. The tree carries the writeback
> (`version` 10, `pdx_version` "8" — two saves in the sitting, never chased). The Mod Editor stripped the comments
> out of `metadata.lua` again and that got committed inside a card edit; they are restored, with the shipped
> change note kept exactly as you typed it in the box. The outbox is cleared to "Released in v9".
>
> **Receipts owed, for v8 and v9 together** (`UPLOAD_WORKFLOW.md` §5): 1. the version number the Paradox page
> shows now; 2. whether the descriptions filled themselves or you pasted; 3. anything that looked wrong on either
> page. The Paradox page cannot be read from here.
>
> ⛔ Nothing here needs a re-upload. The site job is held for v10 by your choice (item 156).
>
> The original item follows for the record.

> **What I found, read from the live Steam page rather than from you:** the Workshop page shows an update at
> **Sep 11, 1:50pm** carrying the F119 + C86 change note, and the page body says "Fifty repairs". Your Steam client
> downloaded the new pack at 16:55. The tree carries the upload's writeback (`version` 8), and the site published at
> 21:10Z. So **v8 is live** as far as Steam and the tree can show; nobody recorded it, and the session that was
> holding the close-out ended. I have done that close-out (the comments the Mod Editor strips from `metadata.lua`
> and `items.lua` are restored, STATE and the outbox updated). ⛔ Nothing here needs a re-upload — never re-upload to
> fix a number.
>
> **Receipt for v8 (`UPLOAD_WORKFLOW.md` §5):** 1. the version number the Paradox page shows; 2. whether the
> descriptions filled themselves or you pasted; 3. anything that looked wrong on either page. (4, the site: I can
> see it published, so only say if it looked wrong.)
>
> **v9 is READY TO UPLOAD — `UPLOAD_WORKFLOW.md`, the same steps.** In it: the **F59 repair** (our own module: Set
> Residence on a full home could overfill it; you watched it fixed, item 152) and the **F60 retirement** (module
> deleted; the card and the fix list drop to **Forty-nine**). The Mod Editor's *Last changes* box should read:
>
> ```
> Housing and migration fixes, reviewed against the 1.1.0 patch:
>
> - Freed housing notice - REPAIRED. Assigning a colonist to a residence that was already full could leave that home with more residents than it has beds, and fail to evict the colonist it displaced. That was this pack's own doing, not the game's. The notice now waits until the move that freed the bed has finished. Watched working in a running colony on 1.1.0. The same repair should also stop a colonist boarding an expedition from losing the home held for their return; that half is checked in the code only.
> - Dome housing total - RETIRED. 1.1.0 changed how a dome decides whether it has room, and it no longer uses the total this fix corrected. Rather than leave it adjusting a number that no longer feeds the decision, the fix has been removed. The fix list drops from fifty to forty-nine.
> ```
>
> The store bodies should fill themselves from `metadata.lua` ("Forty-nine repairs"); the §3 paste copies are
> current if they do not. ⚠️ Until v9 goes up, the live pages say **Fifty** and still list the retired fix — right
> for v8, wrong for the tree — so **after the upload run the site publish (step 4) in the same sitting**, so the
> fix list drops to 49 with the card. Nothing is inconsistent right now: the live site (published 21:10Z, 50 entries)
> and the live card (Fifty) agree, and both are correct for v8. Then tell me the same four things for v9.
>
> ⚠️ One caveat is IN the note on purpose: the F59 expedition half was never run in play, so it says "verified in
> the code only". ⚠️ The site's F51 and F58 rows were narrowed (`a061665`) with wording you have not approved;
> publishing the site is your approval of it — read those two rows first if you want to.
>
> ✅ **152 (b) is closed:** your v8 files were committed in `9bc4360` and F60's retirement ran on top of them.

### ✅ 2026-09-11 — 154 RULED 09-12: sweep only, the safest version. **Build prompt: `agent/prompts/C85_C88_BUILD.md` (with C88). Nothing else owed here; the attended check comes back as its own item when built.**
<!-- ck:154 status:ruled owner:no -->

> **Build prompt: `agent/prompts/CLOGGED_BUILD.md` (fireable). Entry: [C85](agent/bugs/C85.md).** This is the
> one where a Rare Metals Extractor or Polymer factory goes dead with "Clogged after a Dust Storm." and the only
> way out is demolish and rebuild — two Steam players, and a third report since.
>
> **What we now know (it was worth the dig):** the game's own code has a built-in safety net for exactly this —
> when an event switches a building off it can set a timer that switches it back on, and two other events in the
> game use it. This one doesn't set the timer. And if the popup's answer is ever lost, the event marks itself
> *finished* and never fires again, so the building is stranded permanently rather than just delayed. That
> matches "never recovered" far better than our original guess did. We also killed one theory: the player
> cannot close that popup with Escape, so that isn't the route.
>
> **Decision (a): sweep only, or sweep + timer as well?** **Recommendation: sweep only.**
> - The **sweep** notices a building stuck with that exact reason and switches it back on, with two safety
>   interlocks so it never touches one that is legitimately waiting. It writes nothing new into your save, and
>   crucially **it rescues saves that are already broken** — which is where both reporters are.
> - The **timer** version patches the event so future clogs heal themselves. It cannot help anyone already
>   stuck, it edits shipped game data, and it puts a visible countdown on the building — a UI change, which is
>   your call, not an agent's.
>
> If you don't rule, the prompt builds the sweep alone and says so in the commit. **Nothing here needs the
> keyboard.**
>
> **Decision (b): do you want the in-game A/B in the same sitting as 144 a?** It's minutes and works on any
> 1.1.0 colony at any sol — no dust storm needed. Select a producer, paste one line to force the stuck state,
> and check it stays dead with the fix off and clears with it on. ⭐ The "fix off" leg is worth having on its
> own: **it tests the entry's core claim — that nothing in the game ever clears this — which has never been
> checked in a real game.** Full recipe in the prompt's §4.

### ✅ 2026-09-11 — 153 RULED 09-12: the Reddit "160% productivity" thread is NOT a bug — **post the reply: yes.** The draft is approved; posting is yours whenever you want it.
<!-- ck:153 status:ruled owner:no -->

> **What you ruled (2026-09-12):** post it, as recommended. The draft in `FIELD_REPORT_REPLIES.md` is now
> `DRAFT`, gate discharged — nothing is holding it but the click. Tell the next session when it goes up and it
> is recorded in "What was actually posted".

> **Checked end to end against both game versions; no defect filed.** A Russia player can't get 3 extractors to
> 160 Performance and blames the update for amplification and fuel "no longer adding to it". **That's a mix-up
> between two different numbers, not a regression** — Amplify and Fueled Extractor boost *Production*, and never
> touched *Performance*, in either version. I also diffed every number that does feed Performance (traits,
> specialist penalties, the lot): **all identical, and the update actually made this goal easier twice over** —
> the old "Extractor AI pins a staffed extractor at 50" bug is now fixed in the game itself (which is why our own
> fix for it was deleted in hotfix 2), and heavy workload went from +20 to +25.
>
> **Decision: post the reply or not.** Recommendation: **post it** — it's a player who can actually finish the
> goal with the right advice, and the thread's one comment is pointing them toward filing a bug report that
> would go nowhere. Draft is in `FIELD_REPORT_REPLIES.md`. Nothing here needs the keyboard.
>
> ⚠️ **One correction landed in our own records:** `F108.md` credited its completed 3/3 run partly to the
> "Amplify upgrade". Amplify cannot affect Performance, so that attribution was wrong and is now corrected in
> the entry. The run itself and its result stand. It matters because that line was a candidate to repeat to
> Paradox.

### ✅ 2026-09-11 — 152 FULLY RULED: **F59's A2 half is `tested-attended`** (09-12) · **(e)'s three overclaiming rows sweep with the v10 site publish** (09-12) · **(c) CLOSED 09-12 — the kick button is DESIGN, not a defect. Nothing is owed from you.**
<!-- ck:152 status:ruled owner:no -->

> **What you ruled (2026-09-12), both as recommended:**
>
> - **`tested-attended` GRANTED to F59's A2 half** — the manual Set Residence overfill, the one you watched at
>   the four-click receipt on 2026-09-11. ⛔ **A1, the expedition half, stays source-derived** until an
>   expedition is actually sent. The word is yours and it covers A2 only.
> - **(e) — sweep the three overclaiming fix-list rows with the v10 site publish.** Run
>   `agent/prompts/perma/PUBLIC_SURFACE_SWEEP.md` over "A dome read as full while its power was out",
>   "Colonists stayed homeless after you built a Shuttle Hub" and "A dome sat half empty…" (its "no expiry at
>   all" line) as part of the v10 publish, not as a separate errand.
>
> ✅ **(c) CLOSED 2026-09-12 — VERDICT: DESIGN, not a defect. Nothing to build, nothing owed from you.**
> You asked for a refresher on the residence infopanel's kick button (right-click an occupant does not close
> the slot, so the freed bed can go straight back to the colonist you just kicked). A source investigation
> settled it, and the answer is that **the button does exactly what it says and closing the slot is a
> deliberate SECOND click on the same pixel.** All citations below are re-read from the live 1.1.0 tree
> (`ModTools\Src`, the `bodycheck.py` `DEFAULT_SRC`) on 2026-09-12.
>
> 1. **The button's own hint promises an eviction and nothing more.**
>    `T(12193, "<left_click> Select  <right_click> Evict")` —
>    `Data/XDef/sectionResidenceList.lua:114`, byte-identical at `Data/XDef/sectionOccupantList.lua:98`.
>    It evicts. It never claims to close the slot.
> 2. **Closing the slot is a documented second right-click on the now-empty slot.** Same file:
>    `T(8988, "<right_click> Close this residential slot")` at **`:116`**, its result
>    `T(4177, "This slot is closed. Colonists will never occupy it.")` at **`:104`**, and the reopen
>    counterpart `T(8990, "<right_click> Open this residential slot")` at `:124`. `OnAltPress`
>    (**`sectionResidenceList.lua:50-62`**) is a three-way switch on the same control:
>    occupant → `KickResident`; empty **or reserved/appointed** → `ClosePositions`; otherwise →
>    `OpenPositions`. **Evict-then-close is a two-click design, not a missing step.**
> 3. **There is no asymmetry inside housing.** All **nine** `SetResidence(false)` call sites in the shipped
>    tree were enumerated (`TraitPreset.lua:772`, `NaturalHabitat.lua:7`, `Residence.lua:85/157/265`,
>    `Colonist.lua:435/1255/1297/4995`) and **none** sets an avoidance marker; no `avoid_residence`
>    analogue exists anywhere in the tree. The workplace kick *does* blacklist — `Colonist:GetFired`
>    (`Colonist.lua:1875-1882`) stamps `avoid_workplace` + `avoid_workplace_start`, honoured for
>    `g_Consts.AvoidWorkplaceSols` (`Workplace.lua:1273-1275`, `:1294`, `:1331-1332`). So the asymmetry is
>    **across the housing/job boundary**, where the cost of a bad re-seat differs, not inside housing.
> 4. **No state leak.** After a kick the counts, the panel labels and the colonist's `residence` pointer all
>    agree; the re-home is `ChooseResidence` working as intended, on vanilla's own timetable.
>
> ⚠️ **The strongest counter-evidence, recorded so it is not lost and nobody re-derives it:**
> `Residence:KickResident` **accepts a slot index and never uses it** —
> ```lua
> function Residence:KickResident(colonist, idx)   -- Residence.lua:156-158
> 	colonist:SetResidence(false)
> end
> ```
> The `NaturalHabitatBase` override (`NaturalHabitat.lua:5-8`) ignores `idx` too, and the one internal
> caller (`Residence.lua:368`) does not pass it at all — only the UI does. That dead parameter is the best
> argument that someone once intended the kick to act on the slot. It is **not enough to overturn the hint
> text plus the documented second click**, so the verdict stands as DESIGN; if a future reader wants to
> reopen this, that parameter is where to start.
>
> (a) needed nothing and (b) closed on 2026-09-11; (d) is a note, not a decision.

> **Built tonight** (migrationfix link 01; `Code/Fix_FreedHousingNotice.lua`). The vacancy
> notification no longer fires in the middle of someone else's operation — it now runs a
> scheduler step later, after the operation that freed the bed has finished, and re-checks
> whether the bed is still free. That closes **both** harms 151 described.
> ⚠️ **CORRECTION, same day, by the session that wrote this line.** I first reported a *third*
> harm here (a colonist dragged into a residence being destroyed). **It does not exist** — it
> was an artefact of my own test fixture, and re-running the test against the real game code
> refutes it. The two real harms and the repair are unaffected and were re-checked without
> that fixture. Details in [F59](agent/bugs/F59.md)'s retraction section. **This also
> withdraws item (f) below — please do not file it.**
> ⛔ **Nothing is uploaded and nothing may be.** The upload gate is AFTER the audit
> (`agent/prompts/migrationfix/02_AUDIT_fable.md`), not between. No version number was
> touched and the Mod Editor was not opened.
>
> **⛔ ITEM B WAS STOPPED, BY ITS OWN GATE — and it needs you.** The brief's second job was
> to retire `Fix_DomeFreeSpaceMismatch` (F60). Removing a module makes the Mod Editor rebuild
> `items.lua` and `metadata.lua`, and **both of those are sitting uncommitted in your tree**
> (your v8 pack — the comments are stripped, so it is a `SaveDef` round-trip). The gate says
> ship F59 alone rather than touch or work around your files, so that is what happened. F60
> is untouched and still shipping. **To unblock it: commit or discard those two files, then
> F60's retirement can run in the next cycle.** Nothing about F59 depends on this.
>
> **YOUR RECEIPT — four clicks, any 1.1.0 colony, no expedition and no waiting.** This is the
> one thing no desk control can settle, and it also runs on 1.0.7:
> 1. Open a residence that is **full** (close spare bed slots on its panel until it reads
>    full, e.g. 2/2).
> 2. Make sure that dome has **no other free beds** — close spare slots in its other
>    residences too.
> 3. Click a colonist in that dome **who does not already live in that residence**, then the
>    full residence, and choose **Set Residence**.
>    ⛔ **EVERY ATTEMPT NEEDS A DIFFERENT COLONIST.** Repeating with the *same* colonist on
>    the *same* residence does **nothing at all** — no eviction, no assignment, no change to
>    the numbers — because the first attempt stamped `user_forced_residence` and
>    `Residence:ColonistInteract` returns immediately on it (`Residence.lua:334`, stamped at
>    `:341`), and that stamp lasts `g_Consts.ForcedByUserLockTimeout` = 3,600,000 ms of game
>    time. A repeat reads exactly like "the fix did nothing", which is a FALSE NEGATIVE, not
>    a result. (The `:331` rule above is the same trap by a different door.)
> 4. **Reads 2/2 and the evicted colonist is standing homeless = repaired. 3/2 = still
>    broken.** More generally: **the left number going above the right number is the bug.**
>    If you made the home full by closing slots on a bigger residence the pair may read
>    1/1 vs 2/1 rather than 2/2 vs 3/2 — same defect, different digits.
>
> ⛔ **IF YOU REPEAT THE CHECK, USE A DIFFERENT COLONIST EACH TIME — otherwise it
> silently does nothing.** Found at source after this was first written, so it is my
> omission and not a game bug: the first attempt stamps the colonist with that residence
> (`Residence:ColonistInteract:340`), and `:334` makes any later attempt by the **same
> colonist on the same residence** return immediately — no kick, no assignment, no change
> to the numbers. It is not transient either; that stamp lasts a sol of game time. So a
> re-click to "make sure" looks exactly like "the fix did nothing". Same silent no-op if
> the colonist you click already lives there (`:331`).
>
> ⚠️ **Step 2 is load-bearing, not belt-and-braces.** A free bed elsewhere in the dome with
> better comfort draws the evicted colonist away, and then the bug does not show even on the
> unrepaired module — so a "pass" with other free beds around proves nothing.
>
> Then one boot, and check the log says the fix applied (post-release rule). No playtest
> status is granted by the desk results — the word is yours to give.
>
> **Decisions:** (a) **nothing is owed from you on F59's code** — it is built and recorded;
> (b) **the two uncommitted release files** — land them or drop them, so F60 can be retired;
> (c) **a new lead, your call on whether it is even a bug:** the residence infopanel's own
> kick button (right-click an occupant) does *not* close the slot, so the freed bed can be
> handed straight back to the colonist you just kicked. That behaviour is **unchanged by
> tonight's repair** — the old module did the same, and vanilla re-homes them on its own
> timetable anyway — so it is filed as a lead, not a defect. Fixing it would mean deciding
> whether a kick is meant to stick; (d) `agent/bugs/F59.md` also records that the **frozen
> 1.0.7 download still carries the unrepaired module**, which ck151 (e) already ruled stays
> frozen — noted so the record does not read as if 1.0.7 were covered.
>
> **Also fixed, because the repair broke it:** the Test Kit's own `FreedHousingNotice` probe
> read the notification *inline*, so it would have reported **FAIL on the corrected module**
> at your next `RunAll()`. It now tests the real contract (committed in the Test Kit repo).
>
> ---
>
> ✅ **2026-09-11, THE AUDIT RAN (migrationfix link 02, Fable) — verdict: SHIP A.** Full report:
> [MIGRATIONFIX_AUDIT.md](agent/reports/MIGRATIONFIX_AUDIT.md). In plain terms: I re-read every line the
> repair rests on in the game's own code, ran all the desk checks, and then deliberately broke the fix three
> ways in scratch copies (put the notification back inline · removed the destroyed-home guard · silenced it
> entirely) — each break made the right checks fail, so the checks are real and the fix does what it says.
> It also holds on game 1.0.7, which matters because Steam and Paradox 1.0.7 players run this same pack.
> **What the audit could not do is boot the game**: the one thing still owed is the post-release boot with
> the `applied` line, plus the four-click receipt above if you want to see it with your own eyes.
>
> ✅ **THE FOUR-CLICK RECEIPT RAN, 2026-09-11 — YOU SAW IT, AND IT PASSED.** Your own console lines:
> `[F59] cap=20 closed=6 residents=14 reserved=0 free=0` and `[F59] dome has a spare bed:  false`.
> Effective capacity is 20 − 6 = **14** and there were **14** residents ⇒ **no overfill**. The unrepaired
> version reads **15** there. Better still, the evicted resident ended up in the *incoming* colonist's old
> bed — a bed that only frees up **after** the point where the old code fired — so the ordering was visible,
> not just the count. And the dome read `false` for spare beds, which is what stops this being a test that
> passes no matter what. **F59's manual-assign half is now observed working in a real game.**
>
> ⛔ **What that does NOT mean, so it isn't over-claimed later:** the expedition half (a crew member losing
> their held home at boarding) is **still untested** — no expedition was sent. Nobody has seen the *broken*
> behaviour in play either; that it would read 15 is desk-measured, not witnessed. And the frozen 1.0.7
> download still carries the unrepaired module.
>
> ⚠️ **One of my predictions was wrong and cost you a few minutes:** I said pausing the game would visibly
> hold the repair's notification back. It didn't — it looked instant even paused. That guess was never what
> the repair needs (it needs to run after the game's own operation finishes, which can still be instant), and
> I should not have offered it as a test. The numbers were the right check all along.
>
> **Decision: grant `tested-attended` to F59's A2 half?** That word is yours, not an agent's. Recommendation:
> **yes for A2**, and leave A1 source-derived until an expedition is actually sent.
> Retiring the fix instead of repairing it is NOT recommended — you would lose the immediate offer of every
> genuinely freed bed (up to 12 hours per bed in a big colony) and gain nothing the audit could find.
>
> **Two new decisions from the audit:**
> - **(e) The fix list's "A dome read as full while its power was out" entry is wrong on 1.1.0 whether or not
>   you retire F60** — the game no longer gates births or arrivals on that figure, so "After the fix: they
>   agree" is not true any more. Two more entries overclaim ("Colonists stayed homeless after you built a
>   Shuttle Hub", "A dome sat half empty…" — its "no expiry at all" line). These are public-surface text fixes,
>   not code. **Recommendation: run `agent/prompts/perma/PUBLIC_SURFACE_SWEEP.md` on those three rows before
>   or with the next site publish.**
> - **(f) ⛔ WITHDRAWN — nothing to file, no action from you.** This item said the game can move a homeless
>   colonist into a destroyed residence. The three code facts behind it are individually true (a destroyed
>   residence does stay in the dome's housing list, its switch does stay on, and the selector itself does not
>   test "destroyed"), **but the conclusion is wrong**: the test is there, one level down — the comfort
>   scoring the selector calls refuses a destroyed building outright, so it can never be chosen. Measured
>   against the real game code, not argued. **There is no game bug here, and the matching "unresolved lead"
>   in [F59](agent/bugs/F59.md) is now closed in the game's favour.** Withdrawn by the session that caused
>   it — the audit was reasoning from my retracted finding, not making its own mistake.
>
> Required owner-facing warning, verbatim from `doccheck` after this session's one STATE line (item 132 is yours):
> `warn STATE.md is 13240 bytes, warn threshold is 12288 — copy this line VERBATIM into the owner report; the owner fires agent/prompts/perma/STATE_EVICTION.md`

### ⚖️ 2026-09-11 — 151: migration audit complete — **(a) and (d) CLOSED 09-12 as overtaken by events · (e) RULED 09-11 · (b) and (c) still open**

> **Closed 2026-09-12 on your "use your best judgement, close it if everything is shipped", after checking that
> it is.** Three reads, none of them a quote:
> - The migration chain ran clean end to end: link 01 built the repair (`3b41d9f`), link 02's audit returned
>   **SHIP A** ([MIGRATIONFIX_AUDIT.md](agent/reports/MIGRATIONFIX_AUDIT.md)) — recorded in item 152.
> - **F59's repair shipped in v9**, read live from Steam 2026-09-12, together with F60's retirement (`9bc4360`).
>   (The Paradox page cannot be read from here; its upload ran — `pdx_version` "8" in the tree.)
> - **(e) is RULED** (2026-09-11: 1.0.7 stays frozen).
>
> ⇒ **(a)** — "repair F59 rather than retire it, and retire F60's obsolete tally override" — is answered by what
> shipped: both halves are done and live. **(d)** — "does the second harm change the priority of (a)?" — asked
> whether to treat F59 as a repair to schedule; it was scheduled, built, audited and shipped. Neither asks a live
> question any more. **Nothing is owed from you on either.**
>
> ⏳ **(b) and (c) stay OPEN**, and they are the live halves: **(b)** which sections of the
> [developer report](agent/reports/MIGRATION_DEV_REPORT.md) may be sent, and **(c)** which checks join the owed
> sitting 144 a.

> **[F59](agent/bugs/F59.md), desk-controlled, not yet reproduced in play.** At boarding, the game frees a crew member's
> bed and then reserves it for their return. Our notification can give that bed to a homeless neighbour between those
> steps. Same shipped sequence: vanilla keeps the hold; our module loses it. The ordinary vacancy gap still exists,
> so **repair is recommended, not retirement**. All 12 desk controls held, including an unbuilt idea that excludes
> the departing expedition home while keeping ordinary notifications. F58 cannot protect a hold never created.
> **No fix or release file was changed.** The owner authorized completion of checks and findings after the stop.
>
> **Decisions:** (a) prioritize repairing F59 while preserving its ordinary vacancy notification (recommended), or
> choose temporary disable/removal, and retire F60's obsolete tally override (recommended); (b) which sections of the
> [completed developer report](agent/reports/MIGRATION_DEV_REPORT.md) may be sent — recommendation: share the scoped
> mechanisms and C83 witness, identify F59/F60 as our maintenance findings, and give F80's per-track evidence as a
> candidate explanation, not a solved incident; (c) which checks should
> join owed sitting **144 a**. F52 passage/F54 hub/C83 arrival checks are cheap only if that loaded 1.1.0 fixture already
> has their layouts; F59 needs full housing, a competing homeless neighbour and a housed expedition crew member.
> Building those conditions from scratch is expensive. The agent supplies the numbered A/B recipes from the report.
>
> **TAKEABLE WHEN:** use `agent/prompts/perma/GENERAL_USE_PROMPT.md` with the owner at the keyboard and a disposable
> 1.1.0 colony meeting the chosen recipe. Back up its autosaves before loading a copy. F59's measure is at boarding;
> it does not require waiting for the crew to return. No playtest status is granted by the desk results.
>
> **Other findings:** F60 changes applicant housing estimates without repairing the migration/birth gate. F51's
> stale cache no longer proves permanent homelessness; F58/F73 still lack current organic benefit evidence.
> F61's rewritten selector omits old quarantine checks; F62's neighbours now include shared Passage Hub spokes.
> Treat those as developer policy observations. F80 has a controlled loop-boundary omission; a game loop fixture is
> expensive, and its relationship to the old waiting incident is unproved. The report supplies the exact capture.
> The one-off audit brief is consumed. **151 remains the single decision item; no implementation or game run approved
> by the instruction to continue checking.**
>
> ---
>
> ⭐ **2026-09-11, VERIFICATION (151 a): the expedition finding CHECKS OUT — and the same fix has a second,
> WORSE problem that you can see in about two minutes.** A separate session re-derived the whole thing from
> the game's own code instead of trusting the audit. Verdict on the audit's claim: **CONFIRMED** (source-level;
> still never seen in a real game). Details and every citation: [F59](agent/bugs/F59.md), last section.
>
> **The new one, in plain terms.** When you click a colonist and use **Set Residence** on a home that is
> already full, the game throws the oldest resident out and puts your colonist in. Our fix fires in the gap
> between those two steps and hands the just-emptied bed straight back to the person who was thrown out —
> and then the game puts your colonist in anyway. **You end up with more people in the home than it holds:
> the residence panel reads something like 3/2.** The colonist you wanted evicted is not evicted.
> This is NOT new in 1.1.0 — the same code is in 1.0.7, so **every released version of the pack has had it**.
> Desk-controlled 8/8 (`tools/desk_f59_interact.py`), with a control showing it does NOT happen when the dome
> has a better free bed elsewhere.
>
> **Decision (d): does this change the priority of (a)?** Recommendation: **yes — treat F59 as a repair to
> schedule rather than an open question**, because the audit's proposed expedition-home exclusion fixes the
> expedition case only and does nothing for this one. Temporary disable remains your separate call.
> *(No fix was built this session — verdict and repair were deliberately kept in separate sessions.)*
>
> **Answer to (c) — is an F59 check cheap enough for the owed sitting 144 a?** The expedition check is NOT
> (it needs full housing + a competing homeless neighbour + a housed crew member, built from scratch).
> **This new one IS** — it is the same fix and the same mechanism, and it needs no expedition and no waiting:
>
> 1. In any 1.1.0 colony, pick a dome and open a residence that is **full** (if none is full, open a residence
>    and click the little bed slots to close the spare ones until it reads full, e.g. 2/2).
> 2. Make sure that dome has **no other free beds** — close spare slots in the dome's other residences too.
> 3. Click any other colonist in that same dome, then click that full residence and choose **Set Residence**.
> 4. Look at the residence panel. **With the fix working properly you should see 2/2 and the evicted colonist
>    standing homeless. If you see 3/2 (more residents than the home holds), that is the bug.**
>
> That is the whole check. If you want the control, do the same four steps with the pack switched off — it
> should read 2/2 both before and after.
>
> ⛔ **Follow-up 2026-09-11 — this also affects the frozen 1.0.7 download, and a normal update will NOT reach it.**
> Your store card sends 1.0.7 players to the legacy page, whose download button points at the frozen
> `v5-game-1.0.7` release — and that release contains this same fix, with a byte-identical body. Checked the whole
> way along: card → legacy page → release tag → the file inside it.
>
> **Decision (e): do 1.0.7 players get a repair too?** That means cutting a NEW frozen 1.0.7 build, which is your
> release call, not a code one. Recommendation: decide it at the same time as (d), so it is not discovered later.
>
> ⚠️ What is and is not known: the code chain is definitely there on 1.0.7, and the fix is definitely in that
> download. **Nobody has seen the bug happen in a real game on either version.** The good news is that the
> four-click check above works on 1.0.7 exactly as it does on 1.1.0 — so one sitting could settle both.
>
> ✅ **RULED 2026-09-11 (owner): (e) 1.0.7 STAYS FROZEN. No new legacy build; work targets the ~99% on 1.1.0.**
> Decisions (a)–(d) stay open. One thing that ruling does NOT buy, checked rather than assumed:
> **the portals only ever serve ONE version**, so a player still on game 1.0.7 who subscribes on Steam or Paradox
> gets the LIVE pack, not the frozen one — only people who follow the card's legacy link get the frozen build.
> `Fix_FreedHousingNotice` has no version gate (its guard only checks that the methods exist), so it runs on both.
> ⇒ "1.0.7 is frozen" means *we ship them nothing new*, not *they are out of range*: a repair shipped to 1.1.0
> still reaches the Steam/Paradox 1.0.7 players, and today's defect already does.
>
> ⚖️ **2026-09-11 — (a)/(d) DIRECTION SET (not yet a final ruling): LEAN REPAIR, with both chain links free to
> stop and come back to you.** Owner: *"I'm leaning on the repair side, but let Opus consider it during the
> build — if it finds reason to retire instead of repair, let it stop and tell me. Opus can stop and report any
> concerns at any time. The Fable audit can do the same, and if it finds a concern it can recommend the repair
> shape, or retire, if it thinks it's needed."*
>
> Built into `prompts/migrationfix/` as the 2-link chain (01 Opus builds → 02 Fable audits → **you upload**).
> Both links default to repair, weigh retirement honestly, and are told that repair-vs-retire is a §4a
> who-benefits call that belongs to **you** — so either one that reaches for it stops and lands the question
> here rather than settling it quietly. Both are also told, in their own text, that a stop is cheaper than a
> wrong ship, because the "tonight" deadline biases an executor against stopping.
>
> ⇒ **(a)/(d) stay OPEN.** If the chain runs clean, repair ships and you never have to answer them. If either
> link stops, the question arrives here with the evidence attached.

### ✅ 2026-09-11 — 150 CLOSED 09-12: all three decided. **(a) you posted the developer reply · (b) built as option 1 with the law's own id · (c) retire, ruled by item 156.**
<!-- ck:150 status:closed owner:no -->

> **(a) CLOSED 2026-09-12 — done, not owed.** You posted the reply to `ivanassen` in the Building Codes thread
> and used **the majority of A+B**: the sources paragraph *and* the line naming AI-assisted research and code
> review. There is no API for a Steam comment, so it is recorded as **owner-stated, 2026-09-12** (no posting
> timestamp given) in `FIELD_REPORT_REPLIES.md` — the draft is marked POSTED and the Steam table carries the row.

> **Update 2026-09-12:** (c) is RULED by item 156 (retire). (b): you said "build it" — the build prompt
> `agent/prompts/C85_C88_BUILD.md` carries **option 1** (both laws apply to prefab buildings, as the developer
> will ship) and **the law's own id** on the modifier (so it becomes a no-op the day their patch lands, and
> repeal cleans it up). Both are the recommendations; if you want the other shape, edit the override slot at
> the top of that prompt before firing it. (a) is still yours: the reply draft in `FIELD_REPORT_REPLIES.md`.

> Their post (#7, `ivanassen [developer]`): excluding prefabs is wrong and will be fixed in their next patch, so include it
> in the mod until then. They are merging the pack's fixes into the game, and they couldn't reproduce the farm-oxygen fix.
> They asked where we collect our bugs. The reply draft is in `FIELD_REPORT_REPLIES.md`, "Reply to the developer".
>
> - **(a) The "where do you collect" line.** A: sources only (player reports, reading the game's Lua, testing), plus an
>   offer of repro steps. B: A plus one line saying we use AI-assisted research and code review. **Recommendation: A**;
>   B if you want the method named. Both are true; don't reword either toward "all by hand".
> - **(b) Prefabs ([C88](agent/bugs/C88.md)).** 1: both laws follow their text, so prefab buildings get Lax's +50% and
>   Strict's −30% like any new building. This matches the developer's words and what they'll ship. 2: repair only
>   Strict's missing −30%. **Recommendation: 1.** Either way the fix switches itself off once their patch is installed.
>   Building it is a separate step after you pick.
> - **(c) Farm oxygen ([F37](agent/bugs/F37.md)).** The developer is right: in 1.1.0 a farm only gives its dome oxygen
>   while it is working, and destroying or salvaging it turns that off before it leaves the dome, so the old leak can't
>   happen any more. Our fix is harmless but no longer does anything useful, and the fix list still claims the bug.
>   **Recommendation: remove it in the next update** (F60 is already a removal candidate).

### ✅ 2026-09-11 — 149 RAN: F119 and C86 are both TESTED-ATTENDED (you at the keyboard). **Nothing to decide here; the upload is your separate action (`agent/prompts/perma/RELEASE.md`).** The original steps are kept below.

> ✅ **What ran (09-11):** the boot check passed — both modules `applied`, no mod errors. Then more than the
> throwaway route asked for: an A/B on a real reproduction. With the fix switched off for one rocket,
> researching Advanced Martian Engines while the rocket was still fuelling left it stuck with 20 fuel to
> unload — the Reddit bug, reproduced. You saved and reloaded that stuck rocket: the heal fixed it, and you
> watched it unload the 20 and leave. With the fix on, the same trigger re-sized it at once, and you watched
> it leave. C86: the probe's own scan call left a deep-scanned sector deep and still scanned its neighbour.
> The record is in `agent/bugs/F119.md` and `agent/bugs/C86.md` → "Attended check"; the log is archived.
> **Still not covered:** the Wildfire mystery's own loop, a player's real stuck save, and a real Advanced
> Orbital Probe firing. The steps below were written before the sitting; the sitting used a stronger route.
> ⚖️ **Your call (09-11): no Beta label for either fix** — the in-play reproduction is enough. The fix-toggles
> chain (item 148) must not add one to F119 or C86.

> **What is staged:** `Fix_TradeRocketFuelRefresh` (`2c68bb1`) refreshes an
> Earth-sent Trade rocket's fuel supply/demand request when its fuel cost changes
> on the pad, and performs one selective refresh of a pre-stuck Trade rocket when
> a save loads. `Fix_ScanDowngrade` (`5ca9a0f`) rides the same update: it keeps an
> Advanced Orbital Probe from changing an already deep-scanned neighbour back to
> “Scanned.” The desk harnesses reproduce both vanilla defects from shipped
> bodies and hold **11/11** F119 plus **7/7** C86 demands. Those are desk results
> only; F119 remains `filed`, C86 remains `cand`, and this check must not be
> described as proving either repair in play.
>
> **Before the boot — agent, hard gate:** with the game fully closed, run the
> stale-probe sweep below from the fix-pack repo. Zero hits is clean. Any hit must
> be named and cleared before a result is recorded. Also confirm there is no
> packed copy staged beside the live junction (H-09). If a copy of a campaign is
> used, pre-copy **every** autosave first (EF-056).
>
> ```text
> grep -rln "TEMPORARY" Code/ ../SMR-BugFixPack-TestKit/Code/
> ```
>
> **Leg A — the post-launch bar (one boot, any 1.1.0 colony):**
>
> 1. Fully close the game, then start it normally with Relaunched Fix Pack
>    enabled. Load any disposable 1.1.0 colony; do not load a 1.0.7 campaign.
> 2. **First-screen witness:** the colony map appears and time can be paused and
>    resumed. If the load stops earlier, this leg did not run.
> 3. Read the current `Mars.exe-*.log`. Required lines:
>    `[CommunityFixPack] TradeRocketFuelRefresh: applied` and
>    `[CommunityFixPack] ScanDowngrade: applied`. Also record the total
>    applied/inactive/error line and zero new Lua errors. An absent module line,
>    any inactive reason, or any Lua error is a stop, not a partial pass.
>
> **Leg B — the live callback, only if the throwaway route is convenient:** the
> route is the shipped `PlaceAndFlyRocketTo` seam
> (`UniversalRocket.lua:3962-3969`) used by both Trade-rocket actions
> (`SA_Gameplay.lua:2851-2861`; `ClassDef-Effects.lua:215-226`). It creates the
> same exact class and `Trade` type as Wildfire, but it does **not** recreate the
> mystery or a real stuck save.
>
> 1. Pause the disposable colony. Open the console and paste the following whole
>    line. `[NEVER RUN]`
>
>    ```lua
>    SMRF119Rocket=PlaceAndFlyRocketTo("UniversalTradeRocket",{departure_loc=MarsScreenLandingSpots.Earth,arrival_loc=MarsScreenLandingSpots.OurColony,custom_id="SMRF119Check",custom_flight_time_mars=1,cargo={Food={class="Food",amount=0,requested=100000}},RocketType=g_RocketTypes.Trade,name="F119 Trade Rocket"},MainMap)
>    ```
>
> 2. Resume until **F119 Trade Rocket** is waiting in orbit. Select its pin, click
>    **Land Rocket**, choose a clear landing site inside drone range, and pause as
>    soon as it lands.
> 3. **First-screen witness:** the selected object is visibly the named Trade
>    rocket on the ground and its panel shows cargo activity. A rocket that never
>    reaches the ground leaves this leg unrun.
> 4. With that rocket still selected, paste this whole read-only identity line.
>    It must print exact class `UniversalTradeRocket`, type `TradeRocket`, command
>    `CmdLoad`, and a fuel entry. `[NEVER RUN]`
>
>    ```lua
>    SMRF119Rocket=SelectedObj local r=SMRF119Rocket local e=r and r.cargo and r.cargo[r.FuelResource] print("F119 ID",r and r.class,r and r.RocketType,r and r.command,"fuel",e and e.amount,"need",r and r:GetFuelResourceRequest()) FlushLogFile()
>    ```
>
> 5. Only if all four identity fields are present, paste this whole line while
>    still paused. It lowers the throwaway rocket's base fuel cost by 20, prints
>    the synchronous request change, then restores the old base in the same call
>    and prints the clean state. It creates no global label modifier. `[NEVER RUN]`
>
>    ```lua
>    local r=SMRF119Rocket local e=r.cargo[r.FuelResource] local b=r.base_FuelResourceAmount or r.FuelResourceAmount r:SetBase("FuelResourceAmount",b-20*const.ResourceScale) print("F119 DROP","fuel",e.amount,"need",r:GetFuelResourceRequest(),"supply",r.supply[r.FuelResource]:GetTargetAmount(),"demand",r.demand[r.FuelResource]:GetTargetAmount()) r:SetBase("FuelResourceAmount",b) print("F119 RESTORED","fuel",e.amount,"need",r:GetFuelResourceRequest(),"supply",r.supply[r.FuelResource]:GetTargetAmount(),"demand",r.demand[r.FuelResource]:GetTargetAmount()) FlushLogFile()
>    ```
>
> 6. Read those two lines from the log, not the console history. The DROP line
>    must show fuel exceeding need by exactly `20000`, supply `20000`, demand `0`.
>    RESTORED must show fuel equal to need with both request targets `0`. Then
>    resume briefly: the rocket may unload its Food and leave normally. Do not
>    save this throwaway colony.
>
> **What makes Leg B vacuous:** any missing Leg-A applied line; a selected object
> that is not exact class `UniversalTradeRocket`; a command other than `CmdLoad`;
> a fuel base too small to change by 20; a rocket that never lands; or a packed
> folder beside the live junction. Record such a case as **UNRUN**, never as a
> pass. Leg A alone permits only “applies cleanly on 1.1.0”; Leg B permits only
> “the live callback re-sized this staged Trade rocket.” Neither proves the
> Wildfire mystery or a real pre-stuck save.

### ⏳ 2026-09-11 — 148 DEFERRED 09-12 (you said **skip**; the chain is NOT started) — an on/off button for every fix. **Decisions: (a) how console players reach the buttons, (b) whether this counts as a "major overhaul" for the release gate, (c) accept that the first prompt re-checks how the chain was cut. Recommendations: (a) our own panel, proven on a controller before it is built out, falling back to the game's built-in Mod Options page; (b) no extra sweep — the chain's own final audit and its two sittings are the gate; (c) yes.**

> ⏳ **Deferred 2026-09-12, not closed.** You said skip. All three calls (a), (b) and (c) stay open exactly as
> written; nothing was fired and `docs/agent/prompts/fixtoggles/01_SPEC_fable.md` has not been started.

> **What you asked for (09-11):** a button per fix so players can switch any fix off — prompted by the ~1.5 days in which
> v5 (a 1.0.7 build) ran on 1.1.0 and several fixes did harm, while the player who reported it couldn't narrow it down
> because nothing could be switched off individually. Plus **Beta** labels for fixes released before full testing, and
> **linked** buttons where fixes depend on each other. Our own look, not a copy of the other mod's.
> **Already ruled by you today:** buttons first; the game-version selector and bringing 1.0.7 back into the main mod are
> *researched only* (link 09) and come back to you as a separate "B step" decision; each Beta fix's default (on or off)
> is decided per fix.
>
> **What the research found:** every one of the 45 fixes can get a button. About 36 switch instantly; the rest need a
> little extra (one needs a restart, four need a small undo, and the track power-tunnel fix keeps its clean-up part
> always on so tunnels can't leak into saves). Much of the switching machinery is already in the pack, unused since the
> opt-in split. The other mod's version dropdown only filters the list — nothing in it checks the real game version, so
> its 1.0.7 fixes run on 1.1.0 too. It has no licence, so we study it and copy nothing. Full record:
> `agent/reports/FIXTOGGLES_RESEARCH_2026-09-11.md`.
>
> **(a) Console players.** You asked how the other mod handles it: it mostly doesn't — its panel is mouse-first, the
> controller check in its own test plan is unticked, and it has no fallback. The game's built-in Mod Options page works
> with a controller but is a plain checkbox list. **Recommendation:** build our own-look panel, but the chain's first
> in-game test (link 03) must show it working with a controller before the full build; if it can't, everyone gets the
> built-in page. Either way, one place stores the choices. *(If you have a controller, bring it to that sitting.)*
> **(b) Release gate.** Your 08-20 rule: the big pre-release sweeps return only for a major overhaul, and this touches
> every fix. **Recommendation:** the chain's own final audit and its two sittings are enough; no extra sweep.
> **(c) Who cut the chain.** Our chain playbook says a chain this long (13 prompts) should be cut by a Fable session; an
> Opus session wrote this one. **Recommendation:** accept that the first prompt (on Fable) re-checks the cut and the model
> choices before anything is built, instead of a separate authoring session.
> **FYI, nothing to decide:** the policy line "if it needs a toggle, it isn't a fix" gets reworded, because your ask
> overrides it; "don't build a version detector" stays in force until the B step. Item 88 is overtaken — the parked
> per-fix-toggles idea is now this chain.
>
> **Your time:** two sittings (link 03 about 30 minutes; link 11 longer, priced by link 10). **To start:** fire
> `docs/agent/prompts/fixtoggles/01_SPEC_fable.md`. Link 09 (the version research) can run any time, in parallel.

### ✅ 2026-09-11 — 146 RULED + BUILT: the Wildfire cure rocket can get stuck on the pad for good. **You ruled: build it, out today. Built `2c68bb1` (`Fix_TradeRocketFuelRefresh`), desk-verified, staged for release as a Beta candidate — your check is item 149.** The original ask is kept below.
<!-- ck:146 status:ruled owner:no -->

> Two players on Reddit (one PC, one PS5): the cargo rocket Earth sends for the Wildfire cure sits loaded on the pad,
> shows "20 fuel to unload", and never leaves. **Cause (read from the game's code, not yet reproduced):** the rocket
> works out its fuel need once, when it lands. If the fuel cost changes while it waits — researching **Advanced Martian
> Engines** (−20, exactly the reported number), or, new in this update, the **Fuel Conservation** law, which also shifts
> every time the Ministry of Technology stops or starts working — the game updates *your* rockets but not Earth's. Earth's
> rocket is left with fuel it can't unload (or short of fuel no drone will bring), and the mystery waits for it forever.
> There is no button a player can use. The bug is older than 1.1.0; the new laws just add ways to hit it. Our pack neither
> causes nor fixes it today. Full record: [F119](agent/bugs/F119.md).
>
> **The fix:** when a fuel cost changes, update Earth's landed rockets the way the game already updates yours, and
> un-stick an already-stuck rocket when the save loads. It would carry a Beta label until tested in play.
> A reply for the Reddit thread is ready in `FIELD_REPORT_REPLIES.md` — post it or not, your call.

### ✅ 2026-09-11 — 147 CLOSED 09-12: **cleared by you.** The original triage is kept below. Nothing here is owed from you.
<!-- ck:147 status:closed owner:no -->

> **Closed 2026-09-12 on your word: cleared.** You did not say which replies went up, so nothing is recorded as
> posted — the drafts keep their own status lines in `FIELD_REPORT_REPLIES.md` and are yours to post or drop.
> ⛔ **The C87 lake draft stays HELD.** Its hold is on the 2-minute lake check below, which is still **unrun** —
> the check's result changes the reply. Closing this item does not discharge that hold.

> The original ask: **Decision: only whether to post the replies. Recommendation: post the clogged-building and deep-scan replies (they help players now); skip meteors.** Nothing here needs the keyboard except the optional 2-minute lake check below.

> - **Building codes vs prefabs:** ⚠️ **re-classified after your pushback (09-11).** The code deliberately skips prefab
>   buildings (both laws' maintenance handlers exit on a prefab flag new in 1.1.0), but the law text says "new buildings"
>   with no exception — so under Strict, prefab buildings miss the promised −30%. Candidate [C88](agent/bugs/C88.md),
>   **waiting on the devs' answer** in the Steam thread; nothing to decide until they reply.
> - **Clogged after a dust storm:** a one-time story event. Its "we'll fix it after the storm" answer waits for the
>   *next* storm to end, can miss that one, and never comes if storms have stopped. Filed as a candidate
>   ([C85](agent/bugs/C85.md)); the reply asks the players which answer they picked.
> - **Lakes, "excavation too deep":** ⚠️ **REOPENED after your pushback (09-11): "not a normal terrain warning, never seen
>   it, and Paradox is interested".** The check's code, and everything on its path, is identical to 1.0.7 — so if the
>   warning is new, one of its two inputs changed in 1.1.0: the lake-shape depth data (which looks re-exported for 1.1.0)
>   or the ground height the cursor reports. The player's screenshot is ordinary flat ground by the domes, so my "very
>   low ground" guess no longer fits. Candidate [C87](agent/bugs/C87.md); not our pack either way.
>   ⭐ **The 2-minute check that settles it, in any 1.1.0 colony:** build menu → Lakes → Small Lake, hover flat ground next
>   to your base. **If "Excavation too deep" shows,** it's broken for everyone on 1.1.0: keep the lake cursor there, open
>   the console, paste the line below, press Enter, then tell me — the numbers land in the game log.
>   **If the lake places fine,** it's specific to their map; say so and nothing more is owed.
>   `[NEVER RUN]` — copy-paste exactly:
>   ```
>   local c=GetConstructionController() local o=c and c.cursor_obj if not o then print("LAKECHK", "NOCURSOR") else local x,y,z=o:GetVisualPosXYZ() local e=o:GetEntity() local m=PrefabMarkers["Gameplay.Any."..e] print("LAKECHK", e, "cursor_z", z, "ground", terrain.GetHeight(o:GetMap(), x, y), "min_z", m and m.min and m.min:z() or "NOPREFAB") end FlushLogFile()
>   ```
>   ⚠️ **Line touched up 2026-09-12** (checklist 162 (c)): it now prints `NOCURSOR` instead of throwing
>   a Lua error if the lake cursor was not active when you pressed Enter, and the ground read is spelled
>   `terrain.GetHeight(map, x, y)` (`BottomlessPit.lua:23`). ⛔ **Correction, same day:** I first recorded the
>   old spelling `map:GetHeight(x,y)` as broken and said the line would have thrown. **That was wrong** — a
>   peer session enumerated it and that form is used in 19 shipped files, including the exact
>   `obj:GetMap():GetHeight(x, y)` spelling (`Landscaping.lua:225`). **The original line would have run.** I
>   had read a truncated grep and stated an absence from it. The line above is still the one to paste; only
>   the `NOCURSOR` guard is a real improvement over the 09-11 version.
> - **Deep scan finds nothing:** probes only deep-scan after researching **Adapted Probes**; Deep Scanning alone doesn't
>   change probes. While checking, a small separate bug turned up — the five-sector Advanced Orbital Probe can knock an
>   already deep-scanned neighbour back to "Scanned" ([C86](agent/bugs/C86.md), low priority).
> - **Meteors always hit the base:** nothing concerning. Strikes land at random spots across the map, picked the same way
>   as before the update, and our pack no longer touches meteors. Bigger bases simply get hit more.
>
> Details: `agent/reports/FIELD_LEADS_2026-09-11.md`.

### 2026-09-11 — 145: FR-1 cache probe v2 covers all 18 RAYS records; test normal loading first.

> ✅ **P1 RAN 2026-09-11: "That pakd mod is working" (you).** Checked here: the archive you packed (02:43, 100,411 B) holds the
> code and all 18 shaders byte for byte as the current build; only its `metadata.lua` is the earlier one, from before the store
> text, picture and optional flag. So you tested the code that ships, and the upload's own re-pack carries the new text.
> ✅ **And with Reflections Low, High and Ultra (you, same hour):** you got into a colony both after switching mid-run and on a cold
> boot with them on. That covers the one flagged store line (a save loaded straight from launch), so **the store page is ready as
> written.** You saw nothing wrong with Reflections on, but a bare colony has few reflective surfaces. As you asked, the page now
> says it loads with Reflections on but isn't properly tested that way and will very likely look glitchy, so Off is **recommended**.
> ➡️ **From now on, Linux reports go to their own prompt.** Start a fresh session with
> `agent/prompts/perma/LINUX_DISPATCH.md`; it is fully briefed on everything in this item. **Field tally so far (you, 09-11):**
> 3 working, one of them on a 10xx card; 1 not working (the GTX 1070 below; its log has been requested).
>
> ⚠️ **First field report: it did NOT work for a GTX 1070** (Manjaro, Wayland, driver 580.178.04, Proton Hotfix, Reflections Off and
> Medium). Cause unknown; details in findings §12. **Your quick test, and the first one to do:** on the laptop, move your
> hand-copied `SMR_FR1TempWorkaround` folder out of the Mods folder, **subscribe to the Workshop item**, and start a New Game. A crash
> would mean the Steam-delivered copy doesn't work for anyone; a clean load rules that out. The player's log request is drafted in chat.
> ✅ **Done (you, 09-11): "Launches via steam".** The Steam-delivered copy works on the laptop, so the mod isn't broken for everyone.
> The GTX 1070 failure is either a different shader crashing on that older card, or the mod not switching on there. The player's
> two log lines will tell which.
>
> ⭐ **LIVE on both stores, 2026-09-11 (you).** Paradox **158711**, Steam **3799500849**
> (<https://steamcommunity.com/sharedfiles/filedetails/?id=3799500849>). Steam's public API reads it as **public**, titled right,
> tagged Other; its description filled itself in as plain text, so paste the Steam BBCode block to style it. The upload wrote the
> listing numbers into the mod, and my source copy is re-synced from your Mods folder (that copy is now the master).
> Ready to paste, in `agent/reports/FR1_DEV_REPLY_2026-09-10.md`: **"CURRENT DEV NOTE"** (one post after follow-up 1, covering
> the full result plus the mod) and **"PLAYER REPLY"** (for players asking for help in the thread).
>
> ✅ **Your P1 logs are read** (`C:\Dev\Success\fr1-packed-proof.zip`: a New Game with Reflections High). They show the packed
> mod loaded (`packed from appdata`) and switched on (`ACTIVE`, plus the Reflections-on warning). The game built our stand-in for
> all 18 crashing shaders and none of the originals, built all 36 other reflection shaders, didn't crash anywhere, and quit cleanly.
> Five extra shaders were built because Reflections were on. None of them is one of the crashing shaders, and all compiled fine.
>
> **P1: the temporary mod itself, packed, launched straight into a save [RAN 09-11, steps kept as the record]. You asked for it built so you can pak it:
> it's built** and waiting in your Windows Mods folder as `SMR_FR1TempWorkaround`; the source copy is in
> `C:\Dev\SMR-FR1-TempMod-2026-09-11\`. It is the benched Q2 path with the bench parts removed: no launch option and no forced
> reload. It only switches on for NVIDIA + D3D12 + game 1.1.0.403908, and it logs one line: `[FR1 Temp Workaround] ACTIVE` or
> `INACTIVE: <why>`. After a game update it says "Please uninstall it". The desk harness passes 21/21 cases on mocks, not the game.
>
> **On Windows, to pack it (about 5 min):**
> 1. Game → main menu → **MOD EDITOR** → **TEMPORARY - Linux NVIDIA 580 Crash Workaround** → **File → Pack Mod**. You don't need to
>    enable it on Windows. Don't save anything, and don't open the fix pack in the editor (every save bumps its version).
> 2. Tell an agent it's packed. The agent checks that the archive (`%LOCALAPPDATA%\Temp\Surviving Mars Relaunched\ModUpload\Pack\ModContent.fpk`)
>    holds the code and all 18 shader records, byte for byte, before you carry it over.
>
> **On the laptop:**
> 1. With the game fully closed, make its folder:
>    ```sh
>    MODS="/home/ladmin/.steam/debian-installation/steamapps/compatdata/3215050/pfx/drive_c/users/steamuser/AppData/Roaming/Surviving Mars Relaunched/Mods"
>    mkdir -p "$MODS/SMR_FR1TempWorkaround" ~/fr1-cache-v2/P1
>    ```
>    Copy **only** `ModContent.fpk` from Windows into that folder.
> 2. Launch once with no launch options. In Mod Manager, **enable** the TEMPORARY workaround and **disable** FR-1 Cache Probe v2,
>    then quit fully.
> 3. Paste this whole line into Steam Launch Options. There is no marker any more:
>    ```text
>    PROTON_LOG=1 VKD3D_SHADER_DUMP_PATH=/home/ladmin/fr1-cache-v2/P1 %command%
>    ```
> 4. Go straight to **Load Game → a save**, with no New Game first. Play about 10 min with Reflections Off, quit through the menu,
>    and don't save.
> 5. Preserve `cp ~/steam-3215050.log ~/fr1-cache-v2/steam-P1.log` plus the newest `Mars.exe-*.log`, then zip `~/fr1-cache-v2/P1`.
>
> **Expected, stated in advance:** the game log says `TEMPORARY - Linux NVIDIA 580 Crash Workaround … packed from appdata`, then
> `[FR1 Temp Workaround] ACTIVE: 18 reflections shaders replaced`; the save loads; the dump holds `4f866e2c54fc9064.dxil` (the stand-in).
> - `INACTIVE: the shader overlay did not mount`, or a crash with the original `38121…` in the dump ⇒ **the packed form doesn't
>   work.** Plan B is the route Q2 already proved: players drop the unpacked folder into `Mods/` by hand. One more run with the
>   unpacked folder confirms it.
> - The stand-in plus a crash ⇒ something new; bring everything back.
> - `unpacked` in the mod line ⇒ the folder was copied instead of the pack.
> Optional, same sitting: turn Reflections On for a minute and look (a `WARNING` log line is expected). Afterwards, clear the launch options.
>
> ✅ **Store pages are written** (you asked, 09-11, assuming P1 passes). The copy-paste blocks (title, summary, Paradox plain
> text, Steam BBCode, change note) are in [UPLOAD_WORKFLOW → "FR-1 temporary workaround mod"](UPLOAD_WORKFLOW.md#fr-1-temporary-workaround-mod-store-pages-copy-paste).
> The same text is the mod's own description, so it should fill the page by itself on upload. The mod now also carries a preview
> picture (Paradox refuses an upload without one) and is marked optional, so a save made with it doesn't ask for it once it's
> removed. Before posting, one line needs checking against P1.

> ✅ **RESULT: you ran C2, Q2 and R2 on 2026-09-11, and the evidence is read**
> ([findings §11](agent/reports/FR1_LINUX_FINDINGS_2026-09-10.md#11--2026-09-11--cache-probe-v2-bench-ran-owner-laptop-on-580-q2-loads-worlds-with-the-rays-no-op-r2-reverses-it)).
> - **C2 (control)** crashed during the boot slides on a known reflections shader. The control is valid.
> - **Q2 (the swap, no forced reload) WORKED.** New Game loaded on driver 580, and both saves loaded after it in the same session.
>   The shader dump shows the game built our empty stand-in once for each of the 18 ray-queue reflection shaders, then built the 36
>   other reflection shaders with no crash. No original ray-queue shader was built. F2 was rightly skipped.
> - **R2 (no marker)** crashed on New Game on the original shader, 2 ms after building it. Take the swap away and the crash comes back.
> - **Not shown yet:** that the picture matches Reflections Off (nobody compared); what happens if Reflections is turned **On** with
>   the stand-in installed; a fresh launch going straight into a save (both saves loaded after a New Game, when the shaders were
>   already built).
> - ✅ **The extra 01:47:24 launch is explained** (you, 09-11): you had put the launch option in before enabling the mod, so it was
>   a setup launch and not a leg.
>
> ✅ **RULED 2026-09-11 (you):** not the main pack. It will be a one-off, clearly **temporary** mod that tells players it's a
> workaround and to uninstall it once Paradox fixes the real issue. No GitHub repo; it's stood up on a temporary basis. Astra builds it
> (the round-3 brief was held, then removed on 09-11 once the mod shipped), and your bench steps and the store text will land here. ✅ Your answers
> (09-11): **Steam for sure, possibly Paradox too**; yes, a post to the dev mentions the mod once it is live. Your directive,
> passed to Astra verbatim: **this is the LAST round**, an emergency workaround until the hotfix, not a long-term mod, and
> "Reflections Off" is an acceptable answer.
> **Can it be released? Not yet.** The bench proves the swap works; it does not prove a mod is safe to hand out. No hidden errors
> showed up: the Proton log has no graphics errors and the game log has no Lua errors (findings §11). Risks, biggest first:
> 1. **Delivery is untested.** Workshop/PDX mods arrive packed; the bench ran unpacked. A packed mod might not mount the folder
>    at all, and would then silently do nothing.
> 2. **It can't tell who needs it.** No mod can reliably detect Linux/Proton (EF-089). On Windows, or with Reflections On, the
>    ray-queue reflections become an empty shader: likely missing reflections, probably not a crash (inferred, not tested). AMD cards
>    already use the other reflections path (inferred).
> 3. **Reflections On is untested**, even on Linux 580.
> 4. **It is tied to this game build.** A patch that changes the shader cache makes it stale. It must refuse to run on a new build
>    and be rebuilt after each patch.
> 5. **One machine, about 6 minutes.** One 3070 laptop on 580.173.02, not tested on a GTX 900/1000 card (the players who can't upgrade),
>    not in a long session, and not on a cold launch into a save.
> 6. **It relies on an engine helper (`DlcMountFolder`) outside the normal mod sandbox**, and a game patch could close that route.
> **What round 3 must settle before you upload:** risks 1–6 above. That means a packed build that mounts; a build check so it switches
> itself off (and says "uninstall me") after Paradox's patch; your Windows rig with Reflections On; and one longer Linux run that
> includes a cold launch into a save.
> **Dev reply:** follow-up post 2 (the swap removes the crash, removing the swap brings it back) is drafted in
> `agent/reports/FR1_DEV_REPLY_2026-09-10.md`. Follow-up 1 is up (you, 09-11), so post 2 can go as-is whenever you like.

> **These steps RAN 2026-09-11 (result above); kept as the record. Originally: TAKEABLE WHEN you are at the laptop on NVIDIA 580, PRIME On-Demand.**
> **MEASURED:** your valid C1/N1 bench proved that the game consumed our replacement.
> V1 then crashed on a debug RAYS program I had missed. V2 covers all 18 indexed
> RAYS records; all 36 FULL records remain original. It passes 36 shader/root
> checks and 35 Lua harness cases. **V2 has NEVER RUN in the game.**
>
> **Zip:** `C:\Dev\SMR-FR1-CacheRoute-V2-2026-09-11\fr1-cache-probe-v2.zip`.
> **Report:** [round-2 findings](agent/reports/FR1_CACHE_ROUTE_2026-09-11.md#8--round-2-all-rays-coverage-and-normal-loading).
> The zip includes these steps and a classifier covering all 228 cached compute
> programs. Keep Reflections **Off** throughout: the stand-in produces no reflections.
>
> **Install v2 [NEVER RUN]**
>
> With the game fully closed, copy the zip's FR1CacheProbe folder over the existing
> FR1CacheProbe folder in:
>
> /home/ladmin/.steam/debian-installation/steamapps/compatdata/3215050/pfx/drive_c/users/steamuser/AppData/Roaming/Surviving Mars Relaunched/Mods/
>
> Overwrite existing files. Keep the same folder and mod ID; don't place v1 and
> v2 side by side. Start with no cache marker, confirm Mod Manager shows
> **FR-1 Cache Probe v2**, keep it enabled, set Reflections Off, and quit fully.
> Disable the old FR-1 Options Probe / film-grain FR-1 Test and remove their markers.
>
> Create fresh dump directories in a terminal [NEVER RUN]:
>
> ```sh
> mkdir -p ~/fr1-cache-v2/C2 ~/fr1-cache-v2/Q2 ~/fr1-cache-v2/F2 ~/fr1-cache-v2/R2
> ```
>
> Paste each whole line into Steam Launch Options. The markers use **one leading
> dash and an equals sign**. The only accepted markers are:
>
> ```
> -fr1-cache=control
> -fr1-cache=noop
> -fr1-cache=noop-noreload
> ```
>
> A typo logs MARKER ERROR and the exact accepted strings; it applies no treatment.
> Logs must say **[FR1Cache v2]**. An absent v2 log means the update is not witnessed.
>
> **C2 - unchanged-shader control [NEVER RUN]**
>
> ```text
> PROTON_LOG=1 VKD3D_SHADER_DUMP_PATH=/home/ladmin/fr1-cache-v2/C2 %command% -fr1-cache=control
> ```
>
> Expected: a boot-slides crash before the menu, as in the valid C1/D/E runs.
> The log should contain ARMED Control, reload=true, records=18, MOUNT_HELPER_OK,
> RELOAD_REQUESTED. If the menu appears, stop this control and preserve the log;
> do not infer a working control from reaching the menu. Marker/gate/setup drift
> must be checked. After exit/crash preserve [NEVER RUN]:
>
> ```sh
> cp ~/steam-3215050.log ~/fr1-cache-v2/steam-C2.log
> ```
>
> **Q2 - replacement without forced reload, try first [NEVER RUN]**
>
> ```text
> PROTON_LOG=1 VKD3D_SHADER_DUMP_PATH=/home/ladmin/fr1-cache-v2/Q2 %command% -fr1-cache=noop-noreload
> ```
>
> Expected menu, then choose New Game. This tests whether normal world loading
> reads the overlay. If it does, the world should load and the dump should contain
> the no-op. If it still builds original RAYS, it may crash at world load: that
> means this route has not replaced the program used by normal loading.
>
> Log witness: ARMED Noop, reload=false, records=18, MOUNT_HELPER_OK and
> **NO_RELOAD_REQUESTED**. Merely reaching the menu is not success. If the world
> loads, keep Reflections Off, watch for a minute, then quit and skip F2. Preserve:
>
> ```sh
> cp ~/steam-3215050.log ~/fr1-cache-v2/steam-Q2.log
> ```
>
> **F2 - only if Q2 does not load the world [NEVER RUN]**
>
> ```text
> PROTON_LOG=1 VKD3D_SHADER_DUMP_PATH=/home/ladmin/fr1-cache-v2/F2 %command% -fr1-cache=noop
> ```
>
> Expected: the boot rebuild gets past the debug RAYS shader that killed N1.
> It may still expose a different failure; all shader files and the Proton log
> matter. If the menu appears, choose New Game. Watch a loaded world for a minute
> with Reflections Off, then quit. Log witness: ARMED Noop, reload=true,
> records=18, MOUNT_HELPER_OK, RELOAD_REQUESTED. Preserve:
>
> ```sh
> cp ~/steam-3215050.log ~/fr1-cache-v2/steam-F2.log
> ```
>
> **R2 - only after Q2 or F2 loads a world [NEVER RUN]**
>
> Fully quit the successful leg, then run without a treatment marker:
>
> ```text
> PROTON_LOG=1 VKD3D_SHADER_DUMP_PATH=/home/ladmin/fr1-cache-v2/R2 %command%
> ```
>
> Expected: UNARMED, menu appears, then the original RAYS crash on New Game.
> If it keeps working, preserve that unexpected result; do not clear caches or
> call it a confirmed reversal. Preserve:
>
> ```sh
> cp ~/steam-3215050.log ~/fr1-cache-v2/steam-R2.log
> ```
>
> Use New Game throughout; do not save a valued colony. Zip the new fr1-cache-v2
> folder and bring it to Windows. Report each leg's furthest stage and anything
> visually wrong. Cleanup: clear these added Launch Options, quit fully, then
> disable the disposable probe. In-session disabling does not unmount it.
>
> **Scope decision remains yours after a successful bench:** fix pack, separate
> opt-in mod, or instructions. Recommendation remains a separate opt-in mod for
> a driver workaround. This bench does not approve shipping it. The probe writes
> no persistent settings; the game may still update its normal caches and logs.

**Earlier options work and bench history — the current steps above supersede the earlier recommendations below.**

> **What changed:** the reflections shader is now identified exactly, and it is
> already in the game's packaged cache. Changing its source alone may therefore
> do nothing. Your menu-versus-startup-settings lead remains worth testing: there
> are hidden controls the Reflections menu never touches.
>
> **Your preferred order is retained:** (1) a pure mod that prevents the bad
> shader from being built; (2) a mod that saves a setting for the next launch or
> world load; (3) a Steam launch option that changes the graphics path. After
> those come a targeted shader rewrite, a supported driver change, the built-in
> graphics chip, or the old game branch. No new workaround has passed a Linux test.
>
> **Next bench — TAKEABLE WHEN you are at the keyboard:** first collect the
> prepared read-only settings inventory on your Windows rig; then, when the
> Linux laptop is back on 580, test one real hidden switch at a time. Recommendation:
> take that short settings check first. If it finds no usable switch, try the
> launch-option tests, then the updated version of the existing shader workaround.
> The probe and exact steps are in [the report, R1/R2](agent/reports/FR1_OPTIONS_2026-09-10.md).
>
> **Scope decision:** if a workaround succeeds, should it go in this pack, a
> separate opt-in mod, or player instructions? Recommendation: a separate opt-in
> mod if Lua can carry it; player instructions for launch/driver changes. Putting
> a driver workaround into this pack needs your policy exception: it is not yet
> a verified defect in the game's shipped Lua. The two upstream drafts are ready
> for review in the report; neither has been posted.
>
> ✅ **Added the same night — your Steam reply for the Paradox dev is ready:**
> `agent/reports/FR1_DEV_REPLY_2026-09-10.md` (paste the part below the line). The crash
> log now ties the crash directly to the reflections shader: the same thread dumps
> it and crashes 2 ms later. Files to offer them: `C:\Dev\SMR-FR1-DevPackage.zip` (your
> username redacted). **One quick run would make the strongest line airtight:** Reflections
> **Off**, the same `VKD3D_SHADER_DUMP_PATH` launch option, New Game. If
> `38121decbc3eee12` is dumped again right before the crash, "the game builds it even with
> reflections off" is proven, not inferred.
>
> ⭐ **2026-09-10 night — M1 + M2 bench, READY (you asked: "start with M1 and M2"). Nothing has
> run in a game yet.** Desk results (evidence: `agent/reports/FR1_LINUX_FINDINGS_2026-09-10.md` §8):
> - **M1 is dead on your install.** The game only turns on the shader-cache reload when a DLC
>   is *newer* than the base game, and both DLCs have the same assets revision (33006) as the
>   base game. So there is nothing for a mod to switch off. The probe still reads the setting;
>   if it ever shows `true`, I'll hand you one extra leg.
> - **M2 has a strong candidate: `SSRFullTile8x8 = 1`.** The game already switches it on for
>   every AMD graphics card. It selects a simpler reflections shader that ships ready-made in the
>   game's cache. That shader doesn't have the complicated loop the crashing one has. Your
>   crashing run built only the complicated one. The unknown is whether a mod's setting lands
>   early enough; your dump will show that.
> - **Built:** probe **v3** (use this one; v2 is superseded). It fixes a hidden fault in the first
>   version that could have made a leg silently test nothing. It also carries **your design**: set the
>   switch, then force the shader-cache reload in the same launch. That covers the case where the game
>   reads the switch once at launch, before any mod runs. Zip:
>   `C:\Dev\SMR-FR1-Options-2026-09-10\fr1-options-probe-v3.zip` (Linux-safe paths; the folder
>   inside is `FR1OptionsProbe`).
>
> **Step 1 — Windows, optional, about 5 minutes (checks the probe works in the real game).**
> Unzip into `%APPDATA%\Surviving Mars Relaunched\Mods\`, replacing any earlier `FR1OptionsProbe`.
> Start the game → Mod Manager → tick **FR-1 Options Probe v3** → restart. In Steam → Surviving
> Mars: Relaunched → Properties → General → Launch Options, put `-fr1-options=SSRFullTile8x8:1`.
> Set Reflections to **High**. Start a **New Game** (not one of your colonies: loading a copy
> costs its autosaves). Once the colony appears, glance at anything shiny for a few seconds.
> Then quit through the menu. Tell me "Windows done" plus anything that looked wrong; I read the
> log myself. Afterwards clear the Launch Options field and set Reflections back to your usual level.
>
> **Step 2 — the laptop on driver 580 (the real test).** Once per laptop:
> 1. Disable the old **FR-1 Test (film grain)** mod. Copy the v3 `FR1OptionsProbe` folder to
>    `/home/ladmin/.steam/debian-installation/steamapps/compatdata/3215050/pfx/drive_c/users/steamuser/AppData/Roaming/Surviving Mars Relaunched/Mods/`
>    Then start the game (the main menu works on 580) → Mod Manager → tick **FR-1 Options Probe v3** → quit.
> 2. In the game's options set Reflections to **Off** and keep it Off for every leg (Reflections goes to High only inside a leg that loads).
> 3. In a terminal: `mkdir -p ~/fr1-mm/A ~/fr1-mm/B ~/fr1-mm/C ~/fr1-mm/D ~/fr1-mm/E`
>
> Each leg: paste the line into Launch Options → start → **New Game** → watch whether the world
> loads → close the game (or it crashes) → then in a terminal copy the Proton log:
> `cp ~/steam-3215050.log ~/fr1-mm/steam-A.log`. Use the leg's letter in that command.
> **Order:** A, then B. If B loads, run C and stop. If B crashes, run D. If D loads, run C and then E.
>
> - **Leg A — baseline, reflections Off (this is also the "one quick run" above):**
>   `PROTON_LOG=1 VKD3D_SHADER_DUMP_PATH=/home/ladmin/fr1-mm/A %command%`. Expected: the usual crash.
> - **Leg B — the treatment:**
>   `PROTON_LOG=1 VKD3D_SHADER_DUMP_PATH=/home/ladmin/fr1-mm/B %command% -fr1-options=SSRFullTile8x8:1`
>   **If the world loads:** stay a minute. Set Reflections to High and look around. Then load your
>   Intel-made 1.1.0 laptop save. Quit through the menu.
> - **Leg C — only after a leg LOADS (proves the probe made the difference):**
>   `PROTON_LOG=1 VKD3D_SHADER_DUMP_PATH=/home/ladmin/fr1-mm/C %command%`. Reflections back to Off.
>   Expected: the crash returns.
> - **Leg D — your design, only if B crashed: set the switch, THEN force the reload:**
>   `PROTON_LOG=1 VKD3D_SHADER_DUMP_PATH=/home/ladmin/fr1-mm/D %command% -fr1-options=SSRFullTile8x8:1,ForceShaderCacheReload:1`
>   (no space after the comma). If the game reads the switch only at launch, this reload at world load is
>   what makes it pick again with the new value. If it loads: same as B (a minute, Reflections High, the save).
> - **Leg E — only if D loaded (which half did it?):** the reload alone:
>   `PROTON_LOG=1 VKD3D_SHADER_DUMP_PATH=/home/ladmin/fr1-mm/E %command% -fr1-options=ForceShaderCacheReload:1`
>
> Then `cd ~ && zip -r fr1-mm.zip fr1-mm`, bring the zip to Windows as before, and put your laptop
> back how you had it (clear Launch Options). Tell me in one line which legs **loaded** and which
> **crashed**. From the dumps I'll read which reflections shader each leg built. If B and D both
> crash, the next switches (`SSRTraceHiZ:1`, `SSRForceHyperbolicDepth:1`, each also paired with the
> reload) are ready as one-line legs, at lower odds because they keep the complicated shader. After
> them come your fake-DLC shader-cache route, the launch-option routes and pyroveil.
>
> ✅ **2026-09-10 late — you ran legs A, B, D and E. None of the switches fixes it, but three
> things are now solid** (details: `agent/reports/FR1_LINUX_FINDINGS_2026-09-10.md` §9; your files
> stay at `C:\Dev\fr1-mm-complete`; leg C wasn't needed because nothing loaded):
> - **"The game builds the bad shader even with reflections Off" is now proven.** The probe read
>   reflections as off right before the world loaded, and the crash was on that shader. I've updated
>   the developer reply draft so it no longer says "not yet confirmed".
> - **The AMD switch doesn't work from a mod.** It was set early and held, and even with your reload
>   after it, the game still built the same kind of shader. The other hidden reflection switches look
>   just as disconnected (one was already "on" with no effect), so I'm not asking you to run them.
> - **Your reload experiment was the most useful leg.** It proved that a forced reload makes the game
>   rebuild its reflection shaders from the cache immediately, during startup. It also crashed on a
>   **second** version of the same shader. So driver 580 chokes on that whole shader family, not one file.
>
> **What's left — your call:**
> 1. **Mod-side, desk work for me (no time from you):** your fake-DLC idea, made concrete. A mod hands
>    the game its own small shader cache in which the crashing reflection shaders are swapped for a
>    harmless stand-in, so reflections would stay off for those players. Your reload leg shows a cache swap
>    takes effect at startup. I first have to learn the cache's file format, and I'll report whether it's
>    doable before building anything. **Completed 09-11:** see the cache-route report and current bench above.
> 2. **Two quick launch-option legs on the laptop (one line each, nothing to install):**
>    `VKD3D_CONFIG=force_static_cbv` and `PROTON_DISABLE_NVAPI=1`. These aren't mods, but they're easy
>    for players if one works.
> 3. **pyroveil** (the tool that fixed the 1.0.7 version of this bug), set up for the new shaders.
>    It needs a small build on the laptop.
>
> **Recommendation:** start 1 now (it costs you nothing), and run 2 whenever you're next at the laptop.
>
> **Still yours to decide, and it only matters once something works:** does the workaround ship in this pack,
> in a separate opt-in mod, or as player instructions? (Recommendation above: a separate opt-in mod.)

### ✅ 2026-09-10 — v7 IS LIVE on both stores (your word). Nothing to decide; three things to tell me when convenient.
<!-- ck:- status:closed owner:no -->

Body archived in [archive/PLAYTEST_ARCHIVE.md](archive/PLAYTEST_ARCHIVE.md); search `ck-` and this heading.

### ✅ 2026-09-10 — 144 CLOSED 09-12: **(b) cleared by you.** Two small asks around the v7 upload; neither blocked it.
<!-- ck:144 status:closed owner:no -->

> **Closed 2026-09-12 on your word: (b) is cleared.** You did not say which way — whether the long sounds post
> went up, or what it said — and nothing has been inferred from that. The two drafts that were gated on it
> (`HELD on ck144 (b)` in `FIELD_REPORT_REPLIES.md`: the long sounds post and its "still checking" follow-up) are
> marked **SUPERSEDED** there with the reason, because their gate can no longer be evaluated and the follow-up's
> "currently in testing" wording has gone stale across v7, v8 and v9. ⚠️ **Say the word if you want the follow-up
> back as a live draft** — its two leads are recorded in `agent/bugs/C74.md` either way.
> **(a)** was already discharged here as a decision (below); the boot it names is tracked in `agent/STATE.md`'s
> OWED line, not in this item.

> **(a) The v6 check you still owe** (one boot: a handful of hotfix-2 checks plus the first
> full run of the test kit — STATE's "OWED" line). **Decision: run it on your first v7 boot, or
> later. Recommendation: first v7 boot — one sitting covers both versions.**
>
> **(b) The Steam sounds thread:** did you post the long reply (restored / silent on purpose /
> can't fix or haven't nailed down / still checking), and which version? If it says "still
> checking", two small leads (a Drone Hub effect, one misspelled animation name) are owed a
> check and a follow-up post. Just say which you posted; the next free session does the rest.
>
> ✅ **Update 09-10 late: both leads are checked — neither is something players are missing.**
> The Drone Hub effect is never triggered by anything in the game; the misspelled sound is a
> duplicate of a loop that is already playing. A short follow-up post is ready in
> `FIELD_REPORT_REPLIES.md` — post it only if your reply said "still checking".
>
> ✅ **Answered 2026-09-12 — half of it.** The **C74 and C83 replies did go up** with the v7
> update (your word; there is no API for a Steam comment, so it is recorded as owner-stated in
> `FIELD_REPORT_REPLIES.md` → "What was actually posted" → the Steam table). **The long sounds
> post is still unanswered** — this item stays open for that half only. If your post said "still
> checking", the short follow-up is ready (`FIELD_REPORT_REPLIES.md`, marked `HELD on ck144 (b)`);
> if it did not, say so and the item closes with nothing owed. ⚠️ Either way the post's
> "currently in testing" wording has gone stale: v7, v8 and v9 have all shipped since.

### ✅ 2026-09-10 — 143 CLOSED: **FIX BUILT + TESTED-ATTENDED** — new arrivals no longer fall back into a switched-off, quarantined dome ([C83](agent/bugs/C83.md)).
<!-- ck:143 status:closed owner:no -->

Original question, kept as asked: new arrivals with nowhere to live get sent into a switched-off, quarantined dome with no life support, and suffocate. You reproduced it. **Decision: fix it for hotfix 3, or file and watch. Recommendation: fix it — colonists die, and the game already does the right thing in its elevator case.**

> **What you saw (2026-09-10, thank you):** two domes in walking range of the pad, the
> nearer one switched off, quarantined and unconnected. The rocket's colonists split — some
> into the working dome, the rest walked into the dead one — and the game raised
> Suffocation!.
>
> **Why:** each arriving colonist first looks for a working, open, supplied dome in walking
> range **with free housing**. When the working dome fills up, the rest fall back to "the
> nearest dome" — and that fallback never checks power, life support or quarantine. The
> game's own code does check it when the fallback dome is across an elevator, so this looks
> like an oversight. Once inside a quarantined dome, the game won't let them leave for a
> better one.
>
> **Our pack doesn't touch this today:** our arrival fix only redirects colonists sent to a
> dome they *can't walk to*. Yours was walkable.
>
> **The fix does:** send the overflow to the nearest dome that is actually **working, open
> and supplied** —
> they arrive homeless but alive, and move into housing when it appears — and only fall back
> to any dome at all when no working one is in reach. The build first checks everyone else
> who uses the same "nearest dome" rule, so the change only lands where it should.
>
> **Attended receipt (2026-09-10):** an ordinary landing used only safe routes and stayed
> silent. In the forced overflow leg, every arrival entered the working dome, nobody used the
> disabled station or dead Fuller #1, the repair logged one actual reroute, and nobody moved
> into the bad dome during the following sol. The archived log has 0 Lua errors.
>
> **For the reporter**, if you want to reply: *Confirmed, reproduced, and fixed for the next
> Relaunched Fix Pack update. When new colonists
> can't find free housing in a working dome within walking distance, the game sends the rest
> to the nearest dome of any kind — even one that is off, quarantined and has no life support.
> The repair redirects that overflow into the nearest powered, open and supplied dome, where
> they can wait homeless rather than suffocating. Until the update ships, keep free housing in a
> working dome near where you land, or don't leave a dead dome as the closest one to the
> landing site.*

### ✅ 2026-09-10 — 144 CLOSED: C83's homeless follow-through found a distinct intentional override, not another fix ([C84](agent/bugs/C84.md)). No decision is owed.
<!-- ck:144 status:closed owner:no -->

Later homeless resettlement can consider a switched-on, accepting dome without life support,
but only the player's must-have filter (or direct forced-dome order) can make it beat the live
home C83 chose. The shipped 1.1.0 score comment explicitly preserves that override so players
can force colonists into an unpowered dome. C84 records it `wontfix — intentional`; C83 stays
arrival-only. The attended C83 leg watched the arrivals for one sol; nobody moved into the bad dome.

### ✅ 2026-09-10 — 142 — **CLOSED 2026-09-12 by your ruling of item 163 (a)**, which dispositioned all 25 source-only candidates as four groups rather than one by one: the 12 P2s land in the four groups; **no hotfix-3 list is named**, which is what the recommendation asked for. **Nothing is owed from you; the original ask is kept below as the reasoning.** ⛔ A disposition, not a dismissal — a field report naming any candidate reopens it instantly.: the vanillahunt terminal audit re-derived every P2 candidate — which of these, if any, go to a hotfix-3 candidate list? **Decision: name any entry you want on a hotfix-3 candidate list, or accept "file and watch" for all. Recommendation: none today; take C66 and C82 as cheap organic looks and leave the rest.**
<!-- ck:142 status:closed owner:no -->

> Full verdicts: [HUNT_AUDIT.md](agent/reports/vanillahunt/HUNT_AUDIT.md) §3 (each entry
> also carries a dated `99 terminal audit` stamp). Of the 12 P2 entries re-derived from the
> two trees: 6 hold, 5 are weakened, 1 is refuted; 04's R08311 rejection stands. Per entry:
> - [C82](agent/bugs/C82.md) — NEW, found by the audit, one read only, both trees: after The
>   Incident's "Stop all Fusion Reactors" reply the reactors are never re-enabled. **Verify
>   first, then decide:** it rides the ck140 Incident fixture with one extra reload. If it
>   reproduces it is the one real loss on this list.
> - [C66](agent/bugs/C66.md) — holds: group-All ground unload dumps everything. Piles are
>   recoverable. **Cheap organic look** next time an RC Transport carries two resource
>   groups; watch, no hotfix slot unless it bites you.
> - [C63](agent/bugs/C63.md) — holds: a faction disaster runs forever after its faction loses
>   every seat, and its card is hidden. Needs the ck137 politics fixture. Watch.
> - [C69](agent/bugs/C69.md) — the AI mystery's intensified phase is now one burst; the cause
>   is the instant-research model, not the dropped branch — nothing to patch. Leave.
> - [C64](agent/bugs/C64.md), [C75](agent/bugs/C75.md), [C78](agent/bugs/C78.md),
>   [C67](agent/bugs/C67.md), [C79](agent/bugs/C79.md) — hold, but every one is an UNEARNED
>   GAIN for the player (permanent approval, free construction, +10 % extractors, extra meals,
>   a small RP refund). ✅ **The 09-08/09-09 "tension" this item used to hand you is
>   DISSOLVED — item 161, 2026-09-12:** the 09-08 rule was triage scoped to the 1.1.0
>   recovery and expired with it, and the 09-09 ask was never a reversal. **No rule
>   excludes these; each is now an ordinary cost call.** Recommendation unchanged —
>   leave, because a minor win does not pay for a fixture — but that is **pricing, and
>   revisitable**, not a category ban.
> - [C58](agent/bugs/C58.md) (4 % of a reserved portion; depot half impossible),
>   [C76](agent/bugs/C76.md) (no visible effect — 1.1.0 has no per-tech price),
>   [C68](agent/bugs/C68.md) (trigger unreachable as written) — weakened. Leave.
> - [C80](agent/bugs/C80.md) — REFUTED (the destroyed elevator evicts its traveller first).
>   Nothing to do; the entry keeps the refutation.
> - The 12 P3s (C56, C57, C59–C62, C65, C70–C73, C81) were not re-derived; unchanged, watch.
>
> **TAKEABLE WHEN** you want a hotfix-3 candidate list at all; otherwise nothing is owed.
> FR-1/2/3 stay open — the Linux sitting (136) outranks every source read for FR-1.

### ✅ 2026-09-10 — 141 — **CLOSED 2026-09-12 by your ruling of item 163 (a)**, which dispositioned all 25 source-only candidates as four groups rather than one by one: C79/C80/C81/C62 are dispositioned — C80 **REFUTED** (status flipped today), the rest source-only. **Nothing is owed from you; the original ask is kept below as the reasoning.** ⛔ A disposition, not a dismissal — a field report naming any candidate reopens it instantly. rider: vanillahunt 04 left three functional candidates and two profiling reads; none is a release gate. **Decision: take only a naturally available 1.1 fixture, or leave them source-only. Recommendation: prioritize C79; take C80 only on a disposable elevator save, and leave the profiling reads until a large colony already exists.**
<!-- ck:141 status:closed owner:no -->

> **TAKEABLE WHEN** a fresh 1.1 colony naturally reaches the named surface;
> never convert the branch-locked 1.0.7 campaign. [C79](agent/bugs/C79.md):
> immediately after an authored `SA_RevealTech` event, record the target's
> required/remaining points and all boosts (Mystery 10's 3,000 or Wildfire's
> 90,000 are strong discriminators). [C80](agent/bugs/C80.md): on a disposable
> save, order a traveler into an elevator and finish demolition during entry;
> record the log and traveler command/location. [C81](agent/bugs/C81.md): only
> with an attributable profiler and a large fragmented grid, compare the three
> per-second visibility scans with a counterfactual. [C62](agent/bugs/C62.md):
> only if Hostage Situation naturally reaches its detonation with neighboring
> buildings, profile the unused allocation. Apply each entry's vacuity test.
>
> [C78](agent/bugs/C78.md) is **not owner-takeable on this Steam install**:
> Steam blocks 1.0.7 saves before its Astrogeologist migration route. It needs
> a supported non-Steam old-save tester; do not override or convert the owner's
> campaign to manufacture it.

### ✅ 2026-09-10 — 140 — **CLOSED 2026-09-12 by your ruling of item 163 (a)**, which dispositioned all 25 source-only candidates as four groups rather than one by one: C75 + C76 need no fixture; C75 is a group B **player benefit**. **Nothing is owed from you; the original ask is kept below as the reasoning.** ⛔ A disposition, not a dismissal — a field report naming any candidate reopens it instantly. rider: The Incident can answer two source-only candidates in one fresh fixture. **Decision: test it only if a fresh 1.1 colony naturally has two working Fusion Reactors, or leave both candidates source-only. Recommendation: fold the two reads together; neither is a release gate.**
<!-- ck:140 status:closed owner:no -->

> **TAKEABLE WHEN** the fresh colony lacks Eternal Fusion and reaches The
> Incident during a dust storm; never convert the branch-locked 1.0.7 campaign.
> Save before answering. For [C75](agent/bugs/C75.md), take emergency shutdown,
> reach the no-explosion aftermath, and before researching the revealed tech
> record the Fusion Reactor build-menu entry and a pre-placed site's state. If
> convenient, reload for the explosion branch as the control. For
> [C76](agent/bugs/C76.md), record the revealed The Incident tech's research
> cost on the 10,000-RP no-explosion path and the 5,000-RP explosion path before
> any boosts. Apply each entry's vacuity/falsifier; skip the fixture if it does
> not arise naturally.

### ✅✅ 2026-09-10 — 139 BUILT + TESTED-ATTENDED: all seven silent units (C74 hammer + MOXIE, C77's five), Metatron left out. `Fix_SilentHitMomentFX.lua`; old saves heal without a power cycle; staged for the next release. Nothing is owed from you.
<!-- ck:139 status:closed owner:no -->

Body archived in [archive/PLAYTEST_ARCHIVE.md](archive/PLAYTEST_ARCHIVE.md); search `ck139` and this heading.

### ✅ 2026-09-10 — 138 — **CLOSED 2026-09-12 by your ruling of item 163 (a)**, which dispositioned all 25 source-only candidates as four groups rather than one by one: the eight caller-seam candidates are dispositioned; **C66 stays a group A organic rider**, never provisioned for. **Nothing is owed from you; the original ask is kept below as the reasoning.** ⛔ A disposition, not a dismissal — a field report naming any candidate reopens it instantly. rider: eight caller-seam candidates need fresh 1.1 fixtures; none is a release gate. **Decision: take only the naturally available fixture(s), or leave the candidates source-only. Recommendation: prioritize C66 and fold C67/C68 together if a food-service fixture is already available.**
<!-- ck:138 status:closed owner:no -->

> **TAKEABLE WHEN** a fresh 1.1 colony naturally has the named surface; never
> convert the branch-locked 1.0.7 campaign. [C66](agent/bugs/C66.md): RC
> Transport carrying resources from two displayed groups—choose one group's
> ground-unload **All** and record every resource. [C67](agent/bugs/C67.md) /
> [C68](agent/bugs/C68.md): hold a meal reservation across a workshift or a
> genuine failed service entry; record service Food, reservation/capacity and
> hunger without sacrificing a colonist. [C69](agent/bugs/C69.md): begin Number
> Six Tracing and time **En Garde** / the intensifier against research start and
> completion. [C70](agent/bugs/C70.md): with an older large tank present,
> destroy only the newly designated St. Elmo tank before 80% and identify the
> rebound target. [C71](agent/bugs/C71.md): on the unlucky first-Dredger close-
> inspection branch, record the scanning Explorer's status when the popup says
> it malfunctioned. [C72](agent/bugs/C72.md) / [C73](agent/bugs/C73.md) are
> profiler-only: attribute the Basics tutorial 40/50 ms callbacks or the Food
> infobar's discarded availability query against an otherwise identical
> counterfactual. Apply each entry's vacuity/falsifier; skip what cannot be
> reached naturally.

### ✅ 2026-09-10 — 137 — **CLOSED 2026-09-12 by your ruling of item 163 (a)**, which dispositioned all 25 source-only candidates as four groups rather than one by one: the three politics candidates stay source-only; no colony is provisioned for them. **Nothing is owed from you; the original ask is kept below as the reasoning.** ⛔ A disposition, not a dismissal — a field report naming any candidate reopens it instantly. rider: three vanilla politics candidates need a fresh 1.1 colony, never the branch-locked campaign. **Decision: provision one politics fixture when convenient, or leave all three source-only. Recommendation: provision only if the ordinary play setup can cover them together.**
<!-- ck:137 status:closed owner:no -->

> **TAKEABLE WHEN** a fresh 1.1 sponsor-faction colony has active politics and
> can naturally reach faction opportunities, a timed faction disaster and the
> first Earth Council availability. One fixture can answer [C63](agent/bugs/C63.md),
> [C64](agent/bugs/C64.md) and [C65](agent/bugs/C65.md); none is a release gate.
> Do not use or convert a 1.0.7 campaign save.
>
> Record: (1) whether an active faction can fall to zero seats while retaining
> a timed Radicalization/Renegades disaster, and whether it stops at its cap;
> (2) whether a completed Faction Opportunity's approval explanation disappears
> after 15 sols with no new active opportunity; (3) whether `EarthCouncilIntro`
> appears at first Council availability. The agent supplies counters and the
> one-seat / active-opportunity / manual-popup controls during the sitting.
> Skip a leg as vacuous if its precise state cannot be reached naturally.

### 2026-09-10 — 136: three player reports are now priority surfaces in the vanilla diff hunt. Two asks; neither needs the keyboard.

> **What changed:** the vanillahunt chain README §2b now makes three Steam
> reports the first rows every reader reads: **FR-1** every new game crashing
> under Linux/Proton since the update, **FR-2** probes / deep scan revealing no
> deep resources, **FR-3** frame skip and stutter that does not change with
> graphics settings. Links 02, 03, 04 and 99 are pointed at it, and the final
> audit answers each report for you in one paragraph. `DLC_DEEP_CHECK.md` got
> FR-1's DLC half.
>
> **Ask 1 — evidence from one affected Linux machine (FR-1). Recommended:
> yes, and it is now the most valuable item here.** The chain can only name
> Lua candidates. A second report (relayed 2026-09-10) says it is an INSTANT
> crash to desktop, it survives an uninstall and reinstall, it happens on a
> clean install with no mods, and there is no crash report or popup. That
> rules out mods and our pack. It also points below the game's Lua: the
> project has watched a vanilla Lua error throw 157 times in one session while
> the game kept running (`F114`), so a Lua error does not end the process, and
> a crash to desktop does. ⛔ "No popup" proves nothing either way: on a no-mod
> install the engine shows no popup for a Lua error (`EF-065`).
>
> **What to ask for, in order of value:**
> 1. **Proton's own log.** Add the Steam launch option `PROTON_LOG=1 %command%`,
>    then reproduce the crash. Valve's documented switch writes
>    `steam-3215050.log` in the home folder, and it records the crash on the
>    Wine side, where the game itself cannot.
> 2. **The game's `Mars.exe` log** from that same crashed attempt. ⚠️ The engine
>    writes the last stretch of its log only at a clean exit (`EF-047`), so
>    after a crash the end may simply be missing. It is useful for what it
>    shows (GPU, driver, how far startup got), not for where it stopped.
> 3. **One-line answers still open:** at exactly what moment does it crash
>    (clicking New Game, mission setup, the loading screen, or the first frame
>    of the map)? And the GPU model and driver version, because the game's log
>    lost even that (see 4). (Reporters have already answered the rest: it
>    still crashes with all DLC content disabled, in normal, sandbox and
>    challenge modes, on two distros, on X11 and Wayland, and on every Proton
>    version; every GPU named is NVIDIA.)
>    ⚠️ **"Does loading a save also crash?" can't be answered by them.** Their
>    saves are from 1.0.7, which 1.1.0 refuses, and they have never been able
>    to make a 1.1.0 save. **New ask, your call:** make a vanilla (no mods)
>    1.1.0 new game, save on Sol 1, and share the file. If it loads for them,
>    the crash is in new-game map generation; if it crashes too, it is in
>    loading any map. ⛔ Where Proton keeps the save folder isn't verified yet;
>    an agent walks that before anyone is told.
> 4. ✅ **Players ran the anti-aliasing test (2026-09-10): it's ruled out.** One
>    reply tried FXAA and then anti-aliasing and upscaling off entirely: "Still
>    crashes on 'New Game', no change." Another was already playing with
>    anti-aliasing and everything else off, on NVIDIA, and still crashes. The
>    game's code confirms those settings really do switch the upscaler off. So
>    it isn't the DLSS 4 upgrade, there's no settings workaround to post, and
>    the check on your rig is no longer needed. The agents now look first at
>    what 1.1.0 changed in new-game map generation.
>    ⭐ **That second reply included a game log, and it shows why item 1 comes
>    first:** it's the same game build as ours, but the log stops at the
>    startup banner (about 20 lines), before even the graphics card is listed. The game got as far as New
>    Game, so everything after those lines was lost in the crash. Only
>    Proton's log can show where it dies.
> 5. **Your Linux test rig (your plan, 2026-09-10):** the rarely used RTX 3070
>    laptop, set up to mirror the thread's original poster (Linux Mint 22.2
>    Cinnamon, NVIDIA 580 driver, Steam Cloud off for the game, mods left
>    disabled). Snapshot it with Timeshift once it works. **When it boots Mint,
>    tell an agent: the FR-1 sitting script is owed then** (crash moment,
>    `PROTON_LOG=1`, the built-in graphics chip as a non-NVIDIA control, the
>    1.0.7 branch as a "did it work before" control, a no-mod 1.1.0 save).
>    ✅ The script is written (2026-09-10): `agent/prompts/FR1_LINUX_SITTING.md` (it ran 09-10 and was removed 09-11; all
>    Linux work now goes to `agent/prompts/perma/LINUX_DISPATCH.md`).
>    Hand that to the agent. One thing it adds for you: on a hybrid laptop Mint's
>    graphics setting (`prime-select`) can quietly run games on the Intel chip,
>    so the script checks which GPU the game really used before it counts a
>    "works".
>    ✅ **You ran it yourself on 2026-09-10, and it pinned the crash:** NVIDIA 580's
>    shader compiler dies building the game's reflections shader at every world load,
>    even with Reflections Off (driver 595 and the Intel chip work). Film grain and the
>    extension launch option were tested and ruled out. Summary:
>    `agent/reports/FR1_LINUX_FINDINGS_2026-09-10.md`. The options exploration is
>    complete: [report](agent/reports/FR1_OPTIONS_2026-09-10.md), next bench and scope
>    decision in **145**. Its addendum corrects the earlier cache claim and keeps
>    exact faulting-pipeline attribution open.
>
> **The two controls are both in, so no test is needed from you.** ✅ A new
> game on 1.1.0 WORKS on your Windows/NVIDIA rig **with DLSS 4 on**: every save
> of the `BlankBig_02` colony, its Sol 1 start included, was created by 1.1.0,
> and your screenshots show `TAA` → `NVIDIA DLSS 4` on the RTX 4080, which is
> how you say all your testing ran. So DLSS 4 itself works on NVIDIA; the fault
> needs Proton. ✅ Steam Deck players report no problem (you've seen those
> reports), so the Deck test suggested earlier is dropped; it would only repeat
> them. ⚠️ A Deck "works" is weaker than it looks: Valve ships the Deck's shader
> caches, and SteamOS pairs its own Proton with AMD's RADV driver. It can't
> separate "NVIDIA-specific" from "Deck-specific". ⭐ **The one missing data
> point is a DESKTOP Linux player on an AMD card.** Ask in the threads; one
> such report, working or crashing, splits the two.
>
> ⛔ Before anyone posts instructions to players, an agent confirms the log
> locations and the `PROTON_LOG` step by walking them. The thread's author
> asked where logs live and nobody has answered, so that answer has to be
> right. Whether a reinstall also clears the Proton prefix and Steam's shader
> cache for this game is not verified, so don't advise deleting them until it
> is.
>
> ⭐ **The log a player already posted (2026-09-08) is useful, but it is not
> the crash.** It is `MarsDebug.exe` running the mod editor's Preset Editor,
> which ran for 8 seconds and quit normally. What it does prove: logs ARE
> written under Proton, with the same naming as ours; the engine detects
> Proton (`Proton/Wine: 11.0`) while the game's Lua still believes it is plain
> Windows (no `linux` platform flag); the GPU is NVIDIA, as in `F102`; and
> D3D12's crash diagnostics are unavailable under Proton (`Failed activating
> D3D12 Dred`).
>
> **Ask 2 — commission a code-side performance pass over the WHOLE tree for
> FR-3? Recommended: decide after the chain's audit (99).** The diff can only
> see 1.1.0 changes that add or shorten periodic work, which can make a stutter
> worse. The stutter was reported ten months before 1.1.0, so if it has a code
> cause, that cause is in code both versions share, and no diff lists it. The
> pass would inventory every game-time and real-time thread with its interval,
> every per-tick loop over all objects, and the high-frequency message
> handlers, and it would be a chain of its own. ⛔ A source read never measures
> frame time, so anything it found would still need a profiling check. FR-3's
> result will show whether the pass is needed and where to aim it.

### ✅ 2026-09-10 — 135 **RULED 2026-09-12 (ck166 c): TAKE IT IN HOTFIX 3.** Desk tool only, 0 shipped hashes, ⛔ not part of v10 — and now the only item left in the hotfix-3 batch. Original ask below. — `luafn.py`'s body delimiter over-spans one-line functions (441 declarations, 133 inventory rows). ⭐ The measurement says the fix would change **0** shipped hashes — cheaper than the chain brief assumed. **TAKEABLE WHEN you rule; recommendation: take it in hotfix 3, as a small standalone change.** Nothing here needs the keyboard.
<!-- ck:135 status:ruled owner:no -->

> **What was measured** (vanillahunt link 01, 2026-09-10, `TRIAGE.md` §0.6).
> `find_bodies` scans forward from a declaration for a bare `end` at the same
> indentation and **never checks whether the declaration line already closed
> the function**. So `function Community:GetAverageComfort() return … end`
> spans past its own `end` into whatever comes next, and its "body" swallows
> the following function. Confirmed at source, then MEASURED on the two trees:
> **441 self-closing declarations over-span**, and **133 inventory rows** carry
> the resulting `SPAN-SUSPECT` flag (one-line getters — `Community:GetAverage*`,
> `SupplyGridFragment:GetCurrent*`, `LightmodelPreset:Get*`,
> `object.GetLocalPoint*` — plus a block of `OnMsg.*` handlers in
> `CommonLua/Ged.lua`). A further 567 spans run to end-of-file.
>
> **Why link 01 did NOT fix it, deliberately.** `luafn.find_bodies` is the
> project's single canonical body delimiter: `bodycheck.py` imports it so every
> `-- SRC: … sha256=…` pin in `Code/` hashes exactly what it prints. **Changing
> the delimiter changes those hashes**, so every pinned module would report
> `BODY-CHANGED` until re-pinned. That is a pack-wide re-pin, not an inventory
> link's side effect.
>
> **What it costs us today:** a `body` verdict on one of those 133 rows is
> unreliable — the body may have "changed" only because the next function did.
> The chain's downstream links are told this and will not treat them as
> ordinary rows. ⛔ It does NOT affect any currently shipped fix, and that was
> **MEASURED, not assumed**: all **49** `SRC:` pins in `Code/` were resolved
> against the 1.1.0 tree and **0** of them target a self-closing declaration
> (the 4 seeded controls also delimit correctly, and `bodycheck --selftest`
> stays green). ⇒ option (b)'s re-pin would change 0 hashes today — its cost is
> the sweep and the re-verification, not a wave of red.
>
> ⚠️ **DRIFT, REPORTED AGAINST MY OWN BRIEF.** The chain prompt told link 01 not
> to touch `luafn.py` because "a delimiter change re-hashes every `SRC:` pin in
> `Code/`". **The measurement above says otherwise**: a narrow fix (if the
> declaration line closes its own function, the span is that line) changes the
> span of self-closing declarations ONLY, and no pin targets one — so **0
> hashes move**. I did not fix it anyway, because the fence is the fence and
> the delimiter is a pack-wide instrument; but the decision should be made on
> the real cost, not the assumed one.
>
> ⭐ **NEW INPUT, same day (`treediff` v1.1, `smr-bugfixpack-c3`).** Covering the
> indented declarations forced a span rule for them, and the correct one was
> taken: a self-closing INDENTED declaration hashes **its own line only**
> (flag `ONE-LINE`, 275 rows) — because inside a table constructor the next
> same-indent `end` belongs to the NEXT field, so the old behaviour would
> re-hash a row every time a neighbour was edited. ⇒ **`INVENTORY.tsv` now
> carries two span rules for the same syntactic shape**: an indent-0 one-liner
> keeps the over-span (`SPAN-SUSPECT`, 133 rows), an indented one gets the
> correct span (`ONE-LINE`, 275 rows). Both are flagged, so a reader can tell
> them apart, and ⛔ **it cannot collide with a shipped pin — re-measured: 0 of
> the 49 `SRC:` pins target an indented declaration**, so `luafn.py`'s
> "never a second extractor" rule is not breached where it actually binds.
> **What this adds to your decision:** option (b) now also removes an
> asymmetry inside our own instrument, and option (a) means `treediff` carries
> two rules for one shape indefinitely.
>
> **The options.** (a) **Leave it** — the flag plus this note is enough for the
> chain; the defect is disclosed and bounded, but it stays in the instrument
> every future link inherits, alongside the two-rule asymmetry above. (b) ⭐ **Fix `luafn.py` in hotfix 3**
> (recommended) — a narrow change, 0 shipped hashes affected, `bodycheck
> --selftest` + `sigcheck --selftest` + the new `treediff --selftest` (which
> PINS the current over-span behaviour on a fixture, so the change shows up as
> a deliberate RED there and nowhere else) are the gate. The one real cost is
> that the vanillahunt TSVs were generated under the OLD behaviour, so either
> the chain finishes first or the inventory is regenerated. (c) Fix it but keep
> the old behaviour behind a flag — ⛔ two extractors that can disagree, exactly
> what `luafn.py`'s own header forbids.

### ✅ 2026-09-10 — 134 CLOSED 09-12 as overtaken: the models were assigned, the chain ran end to end, and its audit closed it on 09-10. **Nothing is owed from you.**
<!-- ck:134 status:closed owner:no -->

> **Closed 2026-09-12 on your "if it's overtaken close it", after reading the chain's own manifest
> rather than a status line.** Every row in `agent/prompts/vanillahunt/README.md` is struck through
> and marked DONE: **01** (Opus) · **02** (Opus) · **03** + its three splits **03b/03c/03d** · **04**
> (Codex Sol Ultra, the assignment you made on 09-10) · **99** (Fable). The terminal audit returned
> **SOUND WITH STATED GAPS** and is the authority — `agent/reports/vanillahunt/HUNT_AUDIT.md`; its
> results are already carried in `agent/STATE.md` (12 P2s re-derived, 6 hold, 5 weakened, C80
> refuted, C82 filed) and its hotfix-3 question is item **142**, which is a separate live item.
> ⇒ The decision this item asked for — assign the models — was made and executed. There is nothing
> left to assign. *(The original brief is kept below.)*

> **What exists now:** `docs/agent/prompts/vanillahunt/` — 5 links + a README
> manifest, written from your `VANILLA_DIFF_HUNT.md` brief (consumed) and
> reshaped on your two questions this morning. It hunts for what 1.1.0 broke
> in the GAME by diffing the two archived trees at function granularity (and
> the preset data at field level), reading the changes by the risk classes the
> pack has already been bitten by. It files candidates; it adds no module, and
> it never touches the game directory or the archives. Every link is unattended.
>
> **Your two questions, answered in the tree:**
> 1. **Surface sweep — yes, added.** Every body a reader opens for any reason
>    (the changed function, its callers, its siblings, a preset's consumer) is
>    also read for a `FIX_POLICY` §4 tell, and a hit is filed `PASSING` whether
>    or not the diff caused it. Honest limit: it reaches only bodies someone
>    opened; the audit counts that reach so it is never mistaken for a sweep of
>    the unchanged tree.
> 2. **Fewer legs — 8 → 5.** The four per-system reading links and the preset
>    link were the same job on disjoint row sets; they are now ONE link (04)
>    whose parent runs an agent per system and per preset registry, verifies
>    one finding per agent from the trees, and commits every agent report
>    verbatim as the audit's evidence. The seam link (03) stays separate —
>    it is the one cross-system judgement an agent per system cannot make.
>    Queue: 01 instruments → 02 triage → 03 seam ∥ 04 hunt → 99 audit.
>
> **The decision — 134: at five links the chain method says YOU assign the
> models** (bodies are model-neutral; the table carries my recommendation).
> ✅ **04 is assigned — Codex Sol Ultra, no split (your ruling, 09-10);** its
> brief is rewritten tool-neutral, the pre-split clause is gone, and its stop
> condition is "commit the plan and reports, mark the unrun agents, stop" so a
> resumed orchestrator continues from committed state. Still yours: 01, 02, 03,
> 99. Recommended: **03 the seam and 99 the audit on Fable**, 01/02 on Opus.
>
> **Kickoff:** paste `prompts/vanillahunt/01_INVENTORY.md` into a fresh session
> any time; the chain is read-only on the game, so it does not collide with the
> owed post-upload sitting (one boot on v6) and can run alongside it. 01 also
> runs the 1.1.0 `Lua.fpk`-vs-Src parity check the release gate still owes
> since the update. **132** (the STATE warn) is still yours and is not a gate on
> this; the chain touches STATE only at 99. `DLC_DEEP_CHECK.md` fires AFTER
> this chain's 99 — its brief now says so.

### ✅ 2026-09-09 — HOTFIX 2 IS LIVE AS v6 ON BOTH STORES, AND THE SITE IS PUBLISHED. This is the receipt; nothing is owed from you tonight.

> **What is live, from your screenshots and what I could read myself:**
> * **Paradox Mods** — updated 2026-09-09 23:27, MOD VER. **5**, suggested game
>   ver. 350453, 318.92 KB, the full card auto-filled (the headliner list and the
>   new changelog are both on the page). ⚠️ "5" is expected, not a slip: the
>   page shows the number the upload was sent, and the tree moved to **6** in
>   the save that followed — the same one-behind display v5 had. ⛔ Not a reason
>   to re-upload (your ruling 71).
> * **Steam Workshop** — updated Sep 9 @ 11:22pm, 315.457 KB, the description
>   auto-filled with "Forty-six repairs" and the 1.0.7 section, and the v6 note
>   is on the Change Notes tab (both of today's sentences are on it). The copy
>   Steam delivered to your machine is **315,457 bytes**, md5
>   `57e01a71f08788be9c79393d6194690f` — that is the §0.5(f) bytes check, done
>   from the real file.
> * ⭐ **Both pages auto-filled clean. First time in three cycles** — nothing to
>   paste, and the §3 backups stay in the workflow as the fallback.
> * **The site** — published at 03:38 UTC from `dc892d1` (deployments API, not a
>   stored sha): 46 entries live, both "built against" lines read 1.1.0.403908,
>   the front page's stale "not published yet" note is gone.
>
> **What I did after:** the upload's forced save had stripped every comment
> from `metadata.lua` and `items.lua`. Restored from git in the writeback
> commit, keeping the five fields the save set (`version` 6, revision 403908,
> save stamp, code hash, Paradox version "5"). `version` was not hand-set.
> Item **129** is discharged (upload → pages → site, in that order, done).
>
> **What is still owed, and none of it is tonight:**
> 1. **The post-upload sitting** — one boot on v6, the rows the last sitting left
>    unrun, by name in "THE SITTING RAN" below: A3 (F118), A10, A5 clause 2,
>    A9 clauses 4/5, plus the F117 passenger-station recipe (`bugs/F117.md`
>    §Control — ⛔ never the old "beyond walking distance" one) and the first
>    suite run on the rebuilt kit. Batch it with the next organic play.
> 2. **132** — the STATE.md warn. This close-out evicted the pre-release
>    material from STATE, so it no longer sits against the cap; rule it when
>    convenient rather than now.
> 3. **Then the two hunts**, in this order: `VANILLA_DIFF_HUNT.md`, then
>    `DLC_DEEP_CHECK.md`. Both are authoring briefs (they write chains, they do
>    not read diffs), both trees are archived, and the installed build has not
>    changed, so no re-archive is needed.
>
> ⛔ Every "works again" in the v6 note is still a claim until that sitting; the
> note's last bullet tells players so. Field reports are the detector from here.

### ✅ 2026-09-09 — `100_DOCSWEEP` IS DONE: the words now match the pack that ships. The hotfix-2 chain is closed; the only thing left is your upload sitting.
<!-- ck:- status:closed owner:no -->

Body archived in [archive/PLAYTEST_ARCHIVE.md](archive/PLAYTEST_ARCHIVE.md); search `ck-` and this heading.

### ⚖️ 2026-09-09 — 133: six decisions from the self-check promise audit. **RULED IN PART 2026-09-12 — "do the reword". Four of the six fall with it; (2) and (4) are still yours, and they are one doc line each.**

> ⚖️ **Your ruling, 2026-09-12: "do the reword."** It reverses your 09-09 ruling on item
> **112** — that item carries the reversal, the three candidate sentences and the one that
> shipped. Recorded here because the reword decides most of this item, and because what it
> does **not** decide should not be swept up with it.
>
> | | was | after the reword |
> |---|---|---|
> | **1** pilot, then the bounded prototype | recommend yes | ❌ **NOT COMMISSIONED.** Their only purpose was to make bullet 3 true. The reword makes it true for the cost of one sentence, so the purpose is gone. |
> | **2** what a fix does when a probe answers **UNKNOWN** | open | ✅ **RULED 2026-09-12 (ck166 a) — DECLINE, with a PROPOSE-only exception door.** Only a literal `true` applies; an agent may propose an exception as a checklist item but ⛔ never self-authorise one, and none exists today. Landed in `FIX_POLICY` §2a (i). *(original note:)* **not touched by the reword.** The code already fails closed (`Code/00_Core.lua:156-167`: only literal `true` applies; a throw, nil or any other value declines). This decides whether that is written down as policy. One line in `FIX_POLICY` §2a. |
> | **3** the wording interim | hold the over-promise through the upload | ✅ **DISCHARGED BY THE REWORD ITSELF.** There is no interim left to hold. |
> | **4** `LuaRevision` as an **observation label** | open | ✅ **RULED 2026-09-12 (ck166 b) — ALLOWED as a label, ⛔ never as a guard.** It may record which build a reading came from; it may not gate whether a fix applies. Decision 118 stands unweakened. Landed in `FIX_POLICY` §2a (ii). *(original note:)* **not touched by the reword.** A `FIX_POLICY` §2a heading clarification, independent of any prototype. |
> | **5** the breadcrumb | recommend yes | ✅ **CLOSED WITH ITEM 73 — CONFIRMED BY THE OWNER 2026-09-12 on checklist 162 (d)**, which asked the question directly rather than inferring it. *"We have only had the blame issue once and it was quickly resolved. If the problem comes up more we will revisit it."* The breadcrumb is **not built**. ⚖️ Closed under a named condition (rule 5a): the rate is effectively zero — two sightings, one reporter, one day, nothing since. **More false-blame reports reopen it**, and the argument changes then: it would produce evidence in the player's log rather than save an agent derivation time. ✅ The two records that disagreed about whether 73's closure covered this are now reconciled; ⛔ do not re-derive the tension. |
> | **6** report the indirect `load` (`LuaCodeToTuple`) to the developers | conditional on the pilot | ✅ **MOOT.** It was conditional on a reading the pilot would have produced, and there is no pilot. |
>
> ⚠️ **One prompt this strands. Nothing was deleted; this is a recommendation.**
> `agent/prompts/SELFCHECK_PILOT.md` was authored for (1), was **never fired**, and nothing can
> reach it now. Under `prompts/README.md` a root one-off is `git rm`'d when it is fired or
> consumed — this one is consumed by a ruling instead of by a run. **Recommendation: remove it,
> with the commit message naming this ruling as what consumed it**, the way the other root
> one-offs are retired; git keeps it. Its row in `prompts/README.md` has been marked so nobody
> fires it in the meantime. ⛔ **The two reports stay** — `reports/SELFCHECK_PROMISE_AUDIT.md`
> and `reports/SELFCHECK_PROMISE_COMBINED.md` are the record of *why* the sentence was wrong,
> and the reword's justification cites them. Reports are not consumed by rulings.

> Raised by `smr-bugfixpack-db` and routed here so they are not lost; the
> bodies and the reasoning are in `agent/reports/SELFCHECK_PROMISE_COMBINED.md`
> §7, one line each here:
> 1. Commission the self-check **pilot**, then the bounded prototype (three
>    modules), after the upload — recommend yes.
> 2. What a fix does when its probe answers **UNKNOWN**: decline (recommended),
>    or name the exception in the wording.
> 3. HOW IT WORKS **bullet 3** stays over-promising through this upload (your
>    112 ruling); change it only when the transaction + pins ship.
> 4. Whether `LuaRevision` may serve as an **observation label** — clarify
>    `FIX_POLICY` §2a's heading, or leave it forbidden.
> 5. "Job two": a **breadcrumb** yes/no; the engine box untouched (recommended).
>    ⚠️ **2026-09-12 — this is the SAME ~15 lines as item 73 tier 0, and 73 was CLOSED that day**
>    ("we have spent more resources looking for a fix for something that has only come up once").
>    Closing 73 implies this, but **it is not ruled** — sub-decision 5 is still yours. Read 73's
>    closure before taking it: the blame mechanism, the two field sightings and the tier costs are
>    all written up there.
> 6. If the pilot confirms an indirect `load` in the engine environment
>    (`LuaCodeToTuple`), whether to **report it to the developers**. Not ours to
>    use either way.

### 🎮 2026-09-09 — THE SITTING RAN. Tier 1 is complete and green; what it still owes is below.

> **You were at the keyboard 16:55–18:10. Tier 1 finished, four of twelve Tier 2
> rows ran, and the two bugs that actually reached players were both observed
> working in play.** Logs archived: `archive/logs/sittingboot110_*`,
> `sittingsuite110_*`, `sittingplay110_*` — all three complete, all three read
> after `Mars.exe` exited.
>
> ⛔ **This is not clearance.** `H-04` stands: a green sitting is evidence, the
> upload is yours, and `100_DOCSWEEP` still has to run first.
>
> #### What ran
>
> | | reading |
> |---|---|
> | **T1.1 census** | ✅ **44 applied / 0 inactive / 0 errors — the prediction exactly**, and reproduced across **two independent boots**. First-pass 43/1 with `SaintBlessing` latching and healing, as documented |
> | **T1.2 suite** | ✅ `58 PASS / 5 FAIL / 27 SKIP / 5 ERROR`, run **twice, byte-identical**. ⭐ **Zero regressions and zero wrong removals** — all 5 FAILs and all 5 ERRORs traced to the instrument, each against shipped 1.1.0 source |
> | **T1.3 F95 line** | ⚠️ `removed 0 … left 0` — **vacuous**, and no `LEFT n … ALONE`. But `AstrogeologistExtractors` PASSed independently, so the question *is* answered |
> | **T1.4 payload** | ✅ `PayloadTemplateRefill: applied` — the module whose probe had never executed in any boot |
> | **T1.5 Saint** | ⚠️ vacuous PASS, exactly as ruling 130 predicted. Recorded as vacuous, **not** as confirmation |
> | **T2.1 trains** | ✅ ⭐ **F114 observed fixed.** The train leaves its platform, carries Waste Rock past the station that refuses it, unloads at B. No error line. *(clause 1c unrun — see below)* |
> | **T2.2 landscaping** | ✅ ⭐ **F115 observed fixed**, both halves: a flatten raised **no mod-error dialog**, and drones boarded in and out through one (F34d, never before observed). Complete log, **zero error lines** |
> | **T2.3 F-10 premise** | ✅ **READ AT LAST**: enabled `true 38000`, disabled **`false 60000`**. Positive ⇒ the 1.1.0 bug is real, our guard does work, and **F46 is NOT a REMOVE candidate** |
>
> #### ⛔ Three things that want your decision
>
> 1. **`F03` claims a fix that no longer ships.** Its entry and the public fix
>    list still read `tested` / severity `high`, but link 02 (`f707903`) deleted
>    its repair pass on 09-08 — correctly, under your ruling 117, because 1.1.0
>    ships `SavegameFixups.RemoveLeakedUpgradeModifiers` (verified at
>    `Building.lua:1313`). **The removal is right; the claim was never
>    withdrawn.** Your own rule — *a patch note saying "Fixed" is a claim, false
>    until we confirm it* — points straight at it. I have not moved the status
>    word. **Flip `F03` to retired before the upload, or decide it stays?**
> 2. **Four stale instruments, one of which lies loudly.** The kit's
>    `CaveInRubble`/`IsNearDome` stub gap prints a genuine **`[LUA ERROR]`
>    header** into every log (caught in a `pcall`, harmless to play, but it will
>    trip every future scan — including yours). The other three are
>    `LandscapeCostGuard` (stub missing `GetTargetAmount`), `LanderReturnFuel`
>    (asserts a two-value return 1.1.0's branch never makes) and
>    `SaveSanitizerUpgradeLeak` (probe outlived the pass it tested).
>    **Repair the four now, or file them for hotfix 3?**
> 3. **Two shipped modules now have no working coverage at all** —
>    `LanderEmptyLaunch` and `FreedHousingNotice`, whose `[behavior]` probes
>    ERROR on 1.1.0 methods that were removed. Not defects; blind spots.
>
> Also noted, no decision needed: **`F20` is genuinely unresolved** — its probe
> is structurally unable to pass once retired (its own title says it needs a
> screen check), so tonight's FAIL is not evidence either way. And **C47's entry
> cites Herbs at 100 seeds/hex; 1.1.0 halved it to 50.**
>
> #### ✅ 2026-09-09 (evening) — the sitting ran again: six rows exercised, six PASSED, two recipes refuted
>
> **Attended, `USA Sol 18`, game 1.1.0.403908.** Log archived as
> `archive/logs/sitting2play110_*`, read AFTER the process exited (`Debug::Done`
> present — it grew 1,282 bytes after the mid-session read, which is exactly why
> §3 forbids quoting a running log). ⛔ A clean sitting is still not clearance
> (`H-04`); the upload is yours.
>
> **Census re-confirmed on a third independent boot: `44 applied / 0 inactive`,
> and `0 error-shaped lines` across the whole session** (`tools/logscan.py`, complete
> file). Opt-in pack confirmed OFF by the correct discriminator — `Loaded mod items
> for:` lists only the pack and the kit; its `Loaded mod def` line is merely the
> folder being present.
>
> | row | fix | result |
> |---|---|---|
> | **A1** asteroid habitat trait filter | F-3 | ✅ **PASS** — Quarantined filter, 6 residents, several hours, no mod-error dialog, no error line |
> | **A4** rocket refuel toggle | F-7/F50 | ✅ **PASS**, three clauses — OFF held at `0/30` for **a full sol** (5× the asked window), ON → `30/30`, deliveries completed |
> | **A5** Edit Payload | F-6/F70 | ✅ **PASS** on both evidence-bearing clauses — the zeroed row survived a reopen **and a full manual round trip**, the clause PT-31 singled out |
> | **A6** vacuum walks | F-9/F52 | ✅ **PASS, both clauses** — took the passage; passage destroyed → surface walk returned. The falsifier makes this the strongest row of the night |
> | **A8** train with nowhere to deliver | F-10/F46 | ✅ **PASS** — both stations refusing ⇒ the module's deliberate escape hatch fired and the train unloaded instead of hanging |
> | **A9** track split ⚠️ destructive | F116 | ✅ **PASS** — merge while under construction, then a middle piece salvaged: exactly one section went, **nothing scattered on the untouched leg**, line split cleanly. **The first time F116's repair has been exercised in a game at all** |
>
> ⛔ **TWO ROWS WERE NOT RUN BECAUSE THEIR RECIPES CANNOT WORK. This is the
> sitting's most valuable output — both would have recorded a FALSE PASS.**
>
> * **A2 (F117 arrival re-choose) — recipe refuted from the shipped source.** It
>   says to land beyond walking distance of **every** dome.
>   `GetDomesReachableByColonists` (`_GameUtils.lua:390-420`) only adds domes that
>   ARE in walking distance, and `ChooseDome` (`:486-500`) iterates that list — so
>   the list is **empty**, `Community:GetScoreFor` is never called, and the throw
>   site is unreachable. A clean arrival would have proved nothing. The real
>   trigger needs the assigned dome out of walking distance **while another
>   welcoming dome is in it**, which vanilla's own landing-time assignment makes
>   hard to force; the live route looks to be the **elevator / cross-map** case.
>   ⇒ ⚠️ **F117 is probably RARER than its entry's "ordinary mid-game" claim.**
>   `bugs/F117.md` §Control and the brief both carry the wrong recipe.
> * **A7 (expedition housing) — vacuous by construction.** The sweep runs on
>   `OnMsg.NewDay` and its age branch compares against
>   `ForcedByUserLockTimeout = 3,600,000` (~5 sols). The only crewed expedition
>   this colony offers is **Project Yukon — 6 Officers, 3h**, roughly 1/40th of
>   the timeout and short enough that the daily sweep may never tick. None of the
>   branches above the exemption fire on a healthy crew either, so the row cannot
>   distinguish a fixed pack from a broken one.
>
> ⚖️ **Three of nine rows had recipes that could not run as written** (A2, A7,
> and A4 would have been vacuous had the rocket stayed at `30/30`). All three were
> written from source reads without checking whether the colony could produce the
> trigger. That is a pattern in how the brief was built, not bad luck.
>
> ✅ **You ruled three decisions during the sitting:** F03's stale claim to be
> withdrawn (see below — the word needs picking), the four stale instruments to be
> **repaired now**, and probes to be **built** for `LanderEmptyLaunch` /
> `FreedHousingNotice`. Both kit items are bench work, ship nothing to players, and
> are queued before the upload.
>
> #### 🚫 What is still owed — two rows and three clauses
>
> | # | control | why it did not run |
> |---|---|---|
> | **A3** | **F118 layout leak** | needs the `SMRFIX 1.1 testing` save (Sol 1) and an **unresearched** building confirmed there first. ⛔ Nobody has ever measured this leak, so "nothing visible" is a legitimate result |
> | **A10** | pack-OFF baseline leg | optional; never reached |
> | A5 c2 | cancel the launch prompt | the *flight* was cancelled instead of the cargo dialog's prompt — a different path (`PromptRocketCargoIssue`) |
> | A9 c4/c5 | assigned trains survive; both halves accept a train | the test line was freshly built with no train assigned to it |
> | A2 / A7 | see above | ⛔ **not deferred — their recipes are wrong.** Do not re-run as written |
>
> #### ✅ 2026-09-09 (late) — 99b ran: everything you ruled during sitting 2 has landed, and F117's recipe is re-derived. Two small calls at the bottom.
>
> **Receipts for the three rulings** (nothing ran in a game; every kit verdict below is a prediction until the next suite run):
>
> | ruling | what landed |
> |---|---|
> | **F03 withdrawn** | `closed` (`1851b1a`, done during the sitting) — nothing further |
> | **Repair the four instruments now** | kit `29fd13b` + `4f062de`. The fake `[LUA ERROR] HGE::GetDomeAtHex` header is gone: the cave-in probe now hands the shipped body a stand-in support strut that takes the game's own "cave-in prevented" branch, so the body completes without reaching the helper that raised, and the probe now FAILs if the body raises instead of discarding it. `LandscapeCostGuard`'s FAIL was backwards — the stub lacked a method the 1.1.0 refresh calls only AFTER delegating — fixed at the stub. `LanderReturnFuel` lost an assertion the 1.1.0 branch can never satisfy. `SaveSanitizerUpgradeLeak` is DELETED, not rewritten: the pass it tested went with link 02, and a rewrite would be a new probe whose PASS is vacuous on any save that has been through vanilla's own fixup. ⚠️ One beyond your four, because it was free: `MoraleComfortTooltip` now SKIPs by name on every path instead of a FAIL that read as "the REMOVE was wrong" while proving nothing |
> | **Build the two probes** | kit `4f062de`. `LanderEmptyLaunch` and `FreedHousingNotice` rebuilt against the 1.1.0 bodies, read line by line. Both falsified both ways on a desk harness — 9 of 9, including the OLD probe text reproducing the sitting's exact ERROR lines byte for byte. ⭐ One trap avoided: 1.1.0 makes an auto rocket wait an hour before its first launch, so a naive fixture reads "loaded rocket blocked" on a HEALTHY module; the fixture now pre-dates that gate. That same gate narrows F67 without fixing it — the module stays KEEP |
>
> **Still failing, by name, and why they stay:** `C47OpenFarmSeedBufferShape` (1.1.0 halved Herbs to 50 seeds/hex; re-pinning the probe without re-deriving C47's arithmetic would make it assert a number the entry does not derive from — a re-derivation, not a free fix); the three retired ERRORs `LanderCargoRatchet`, `DroneUnreachableForever`, `AutoExportPriority` (not in your ruling; an ERROR under the retired kind is evidence of nothing either way). Probe count 95 → 94.
>
> **F117's recipe: corrected — and the bug is rarer than the entry claimed.** "Land beyond walking distance of every dome" can never reach the throw (the candidate list is empty). The elevator route the sitting guessed at is where the module stands down on purpose. The one layout that reaches it: no dome walkable from the pad, a passenger train station by the pad reaching a far welcoming dome, and a trait filter or filtered residence among those domes. Shown to reach the scoring call on the shipped bodies at the desk (8 of 8 scenarios), ⛔ **untested in play**, and the entry now carries a console read that tells a vacuous run from a real one. "Ordinary mid-game" is withdrawn. Details: `agent/bugs/F117.md` §Control.
>
> **The orphaned comment list** from the doc sweep's §4 is drained (`a8e0ca2`) — comments only, no behaviour found changed.
>
> #### ✅ 2026-09-09 (later still) — you ruled 131 "promote": landed. And yes, you are good to fire `100_DOCSWEEP`.
>
> * **131 — PROMOTED.** `tools/deskbench.py` is the shared half (paths, the body
>   extractor, the loader that puts a shipped body back at its real line
>   numbers, the engine shims), and the four harnesses sit beside it:
>   `desk_f117_argshape.py` + `desk_f117_kitprobe.py` (99a's two),
>   `desk_probes_f67_f59.py` + `desk_f117_recipe.py` (99b's two). Demands
>   verbatim, only paths moved; the two "old probe text" legs are pinned to the
>   kit commit before the rebuild so they keep meaning. `python tools/deskbench.py`
>   runs all four and summarises — every demand held on promotion. The kit
>   harnesses need the local kit (`SMR_TESTKIT`), the 1.0.7 legs the archive
>   (`SMR_SRC_ARCHIVE`); both default to their rig paths.
> * **Fire 100: yes.** Every gate it names is met — 126 and 127 ruled, 99a and
>   99b consumed, the folder is `100_DOCSWEEP.md` + `README.md`, the upload
>   blockers are the sweep alone, the tree is pushed. Fresh session, docs only,
>   no game. Its inbox already carries 99b's notes, including "the §4 comment
>   list is drained — do not re-file". ⛔ It still is not clearance (`H-04`): the
>   sweep ends at the upload sitting, which is yours.
>
> #### ⛔ One thing still wants your decision
>
> 1. **132 — `STATE.md`'s warn line.** Measured now, not quoted: **12,215 bytes / 129 lines against a 12,288 warn — 73 bytes of headroom, i.e. none.** The warn was raised 9 → 12 KiB this morning as a runway; the file grew ~3.0 KiB over the last ten commits (09-09 03:28 → 21:19) and it is growing, not being suppressed. This link stayed under only by compressing four history lines into pointers (grave in the commit, named in SESSION_LOG) and then trimming its own two new lines twice — the close-out first landed 38 bytes OVER. ⛔ Not an agent's call, and the hard cap (18 KiB) stays either way: **raise the warn again (recommendation: 14 KiB, ~20 lines of runway), or accept a per-session eviction until the 1.1.0 fallout is closed?**
>
>    ✅ **RULED 2026-09-12: SKIP.** You said skip. **The warn stays at 12288 and no eviction is ordered.**
>    ⚠️ For the record, so nobody reads the silence as "it fits": `STATE.md` has sat **over** the warn
>    continuously since 2026-09-11 — every session's `doccheck` emits the warn line and every owner report has
>    been repeating it. That is the state you accepted, not a state that has gone away. The hard cap (18 KiB) is
>    untouched and still enforced.
>
> ⛔ Not clearance (`H-04`). `100_DOCSWEEP` is now the ONLY thing between the tree and the upload; it fires next.

### ✅ CLOSED 2026-09-09 — the brief that produced the block above was consumed 2026-09-15 after ck184 discharged the remaining play clauses. The historical two-tier plan stays below.
<!-- ck:- status:closed owner:no -->

> **Every in-play control the chain owes you is in one file**, one boot, on
> `BlankBig_02` — links 03, 04, 04b, 07, 08 and 99a, plus the F95 line you just
> ruled in and 131's two new rows. Paste it into a fresh session with you at the
> keyboard.
>
> * **Tier 1 (~25 min, no colony setup)** — boot, the census, `SMRTest.RunAll()`.
>   ⛔ **This is the one I would not upload without.** It catches a module that
>   silently switched itself off, and it is the **first machine check the project
>   has ever had on "vanilla fixed it"** for the 36 removals: a `retired` probe
>   that FAILs means a removal was **wrong and players lost a fix**.
>   ⛔ **No boot of this 44-module pack exists.** Predicted 44 applied / 0
>   inactive — computed, never measured, and **any `inactive` line is a finding**.
> * **Tier 2 (~60–75 min)** — twelve controls, **ordered by value, not by link
>   number**. Rows 1 and 2 are the two bugs that actually reached players (F114
>   trains, F115 landscaping). If you only get through three, do 1, 2 and 3 —
>   row 3 is a **one-minute console read** that decides whether F46 can be
>   retired.
>
> ✅ **Stopping partway is planned for, not a failure.** §5 makes every row
> `PASS` / `FAIL` / **`NOT RUN`** with no fourth option, and the session files the
> unrun rows back into this page as one "what the sitting still owes" block. The
> brief does **not** delete itself while anything is unrun.
>
> ✅ **All four preconditions verified 2026-09-09:** stale-probe sweep CLEAN
> (zero hits), the force-inactive leg DISARMED, the enable-path leg DISARMED, the
> autorun harness inert. Nothing to untick except **Passage Network**.
>
> ⛔ **Row 12 (Saint's blessing) is shelved by your own ruling 130 — do not
> attempt it**, and the suite's PASS for it is vacuous, not coverage.
> ⛔ A clean sitting is still not clearance (`H-04`), and `100_DOCSWEEP` must run
> before the upload either way.

### 2026-09-09 — 131: the F117 fix has LANDED. It is the last code in hotfix 2. One small question for you, and one thing the sitting now owes.

> **What landed** (three commits, all pushed): `777249d` the F117 repair,
> `0136af1` the two riders, `cb6415f` a hook the Test Kit reads. Plus one probe
> in the Test Kit (`c1114ed`, local as always). Only `100_DOCSWEEP` is left
> between here and the upload.
>
> **F117 turned out not to be a one-token fix, and I think that is good news.**
> The obvious repair — just always pass the colonist — would have been *worse*
> than the bug on the older game: no crash, but every dome silently scored
> wrong, which nothing would ever have caught. So the fix asks the game itself,
> at the moment it needs the answer, which of the two shapes it has, and if it
> cannot tell it does nothing at all and leaves the game's own choice alone.
> I drove that question against **both** installed game versions on the bench
> and it answered correctly on each, and refused to answer on two deliberately
> broken ones. F118 and the third rider went in as designed.
>
> ⛔ **I am not claiming either bug is fixed, and I moved no status word.** Both
> were found by reading the game's code, and both repairs were checked the same
> way. Neither has been seen happening, or seen not happening, in an actual game.
>
> **What the sitting now owes** — the same one consolidated session you already
> planned, with two things added to it:
> * **F117:** land a passenger rocket far from every dome on a colony that has a
>   nursery, retirement home, hotel, or a dome with a trait filter. Before: a
>   mod-error dialog naming us. After: arrivals just walk. (`bugs/F117.md` has
>   the full recipe.)
> * **F118:** open a layout containing a building you have not researched, save
>   with the dialog open, load. This one I genuinely cannot predict — nobody has
>   ever measured what the leak looks like, so "nothing visible" is a legitimate
>   result and worth writing down.
>
> ❓ **The one question — do you want the bench test kept?** I built a small
> harness that reads the real game code out of both your installed versions and
> re-checks the F117 fix against them. It is the evidence this fix rests on, and
> right now it lives in a temp folder that disappears with this session; the
> results are written down in `bugs/F117.md` either way. Keeping it means one
> new file in `tools/`, and it would re-check itself on every future game patch.
> I did not add it because this link's scope was fixed at four items and a new
> tool was not one of them. **Say "keep the F117 bench" and I or the next
> session will add it — otherwise it goes away and only the transcript remains.**

### ✅ 2026-09-09 — RULED: all three of link 99's calls, plus one new one (130). Every gate on the doc sweep is now satisfied. ✅ **Nothing is owed from you until the sitting.**

> **126 — the F95 residue pass STAYS IN.** Your words: *"Leave ck126 in."*
> ⚖️ This **supersedes the 09-08 ruling (ck120)** that had the cleanup OFF; the
> two-directions tension link 08 raised is settled in favour of cleaning up
> after ourselves.
>
> ⚖️ [**Corrected 2026-09-12, item 161** — "supersedes" was the wrong word and no reversal
> ever happened. The 09-08 ruling was **triage scoped to the 1.1.0 recovery** (the owner's own
> later account), so it had already expired by 09-09; this ask is ordinary judgment after the
> condition lifted, not a rule being overturned. The outcome below is unchanged.]
>
> Two reasons you gave, both recorded because they settle more than this item:
> * *"as far as people who stay on 1.0.7 we are offering them a frozen version
>   on github release that handles 1.0.7 so I am not concerned about that. If
>   they are subbed to our store page they get the current version its the
>   source of truth."* ⇒ `90_SaveSanitizer` becoming **non-removable on every
>   platform** is accepted, and item 117's platform question is answered by
>   ck118's frozen-build route rather than by dropping the pass.
> * *"if it fails it fails with no harm, because worst case if it fails they
>   just get a small bonus."*
>
> ⚠️ **One precision on "no harm", kept because it is the only direction that is
> not free.** Failing to FIND our entries is harmless — the player keeps a small
> bonus. Removing an entry that is **not ours** has no undo. That is exactly what
> link 08's narrowed match and the `LEFT n modifier(s) … ALONE` log line exist
> for. ⇒ if that line appears at the sitting, it is the one to report.
>
> ⇒ **ck128 resolves with it:** the change note's bullet 2 takes the wording that
> says the bonus IS removed on next load. Both drafts are in `100_DOCSWEEP.md`
> §3.1; it writes the one that matches this ruling.
>
> **127 — (a): FIX F117 BEFORE THE UPLOAD.** Your word: *"ck127 fix."* ⇒ a code
> link is owed that passes the colonist on the 1.1.0 body behind a per-module
> runtime discriminator (ck118 binds — read from a callee body at call time,
> never a version label), with two one-line riders: F118, and the
> `FlightPolicies` named guard. `reports/HOTFIX_2_AUDIT.md` §5 is its inbox and
> `bugs/F117.md` carries the repair sketch and the control. ⛔ Still not
> reproduced — the fix is source-derived like the defect, and the status word
> does not move on either.
>
> **129 — (after): UPLOAD FIRST, THEN PUBLISH THE SITE**, in the same sitting.
> Your word: *"ck129 after."* The live page today lists 82, which is correct for
> the v5 players actually have; the committed page lists 46, which is correct
> only once v6 is up. Publishing first would describe a pack nobody can install
> yet. ⇒ `UPLOAD_WORKFLOW` §4 runs immediately after the upload, not before it.
>
> **130 (NEW — ruled in the same conversation, recorded because it is a real
> call and lived nowhere) — the Saint's-blessing save heal SHIPS UNEXERCISED,
> and field reports are its detector.** Your words: *"we do our best to make sure
> we are right and wait for bug reports."*
>
> **Why it cannot be tested here, established rather than assumed.** On 1.1.0
> `Fix_SaintBlessing` declines the data rewrite entirely and its only remaining
> job is healing saves an EARLIER build of this pack damaged. That condition is
> **historical and unforgeable**: adding a Saint to a dome today goes through the
> live path, which 1.1.0 does correctly on its own, so a cheat tests vanilla and
> not us. You have no 1.1.0 save with a domed Saint, and the `EF-080` override
> would not help — a 1.0.7 save opened on 1.1.0 has vanilla's own
> `MigrateDomeTraitLabelModifiers` run on it and files the Saint correctly, so it
> reads `restored 0`. Manufacturing the case would mean reinstalling the broken
> v5, loading a save with a domed Saint, then swapping back.
>
> **Why shipping it unexercised is bounded, checked at the desk 2026-09-09:**
> * `SMRFixPack.WhenActive` is a **gate, not a trap** (`00_Core.lua:228`) — it
>   checks status and calls the handler directly, so a throw in that `LoadGame`
>   pass would reach the engine as a mod-error dialog, the F115 shape. It cannot:
>   the pass's one uncontrolled call is vanilla's own `AddDomeColonistsModifier`,
>   and the shipped 1.1.0 body (`Lua/TraitPreset.lua:77-95`) has **no throwing
>   path** — `if dome then`, `if not prop_meta then return`, `if not label then
>   return`; every exit is a return. ⚠️ `SetLabelModifier`'s own body was NOT
>   read; it is the same call vanilla makes on every dome join.
> * The pass only ever **ADDS**, through vanilla's own function, to colonists
>   missing the modifier, and skips any that already carry it. Worst realistic
>   failure is a silent no-op.
> ⇒ residual accepted: some players who ran v5 keep a missing +10 morale on
> Religious colonists in a Saint's dome until that Saint changes dome.
>
> ⚠️ **At the sitting this will report a PASS that proves nothing, and that is
> correct behaviour, not coverage.** The kit's `SaintBlessing` probe returns
> `PASS — … (no Saint in a dome in this save, so the re-base half had nothing to
> read)`. ⛔ Do not read it as confirmation. ⛔ And do not load the poisoned save
> to chase it: the `restored` line prints on a save's FIRST load and never again.
> ⭐ Wanted for hotfix 3, not now: a kit probe that drives the re-base against a
> **stub** colonist and dome, which exercises the path with no save at all.

### ⚖️ 2026-09-09 — LINK 99 IS DONE. VERDICT: **SHIP WITH CHANGES.** Three calls (127–129) — ✅ **ALL THREE RULED**, see the block above; the first is the reason for the verdict, and it is a real bug the pack already ships.

> **The audit in one line.** Every code change in this patch re-derived against the shipped 1.1.0 code holds up;
> the instruments were made to fail on purpose and did; the store text matches its backups to the byte. **The
> findings are in the code the patch did NOT touch:** three of the 35 modules we kept turned out to have the game
> move underneath them in a way no tool can see, and one of the three is a bug that shows a player an error.
> Full report: `docs/agent/reports/HOTFIX_2_AUDIT.md`. ⛔ Nothing here is an upload, and nothing ran in a game.
>
> **127. `Fix_ArrivalDeaths` can throw an error on 1.1.0, and it is in the pack you are about to upload — and in
> the v5 players have today.** Game 1.1.0 changed what one of its dome-picking functions expects (the colonist
> instead of the colonist's trait list); our arrival fix still hands it the old thing. The moment a new arrival's
> dome is out of walking range AND the colony has any nursery, retirement home, hotel or dome trait filter, the
> game hits a nil and raises the "error in mod" dialog naming this pack — the same shape as the landscaping error
> you reproduced on 09-08. **Source-read on both game trees, never reproduced**; entry `F117` has the control.
> * **(a) Fix it before the upload — RECOMMENDED.** One small session in `Code/` (game closed): pass the colonist
>   on 1.1.0 behind a per-module check that reads the game's behaviour, never a version number (the ck118 rule).
>   Two one-line riders ride the same session because someone is in `Code/` anyway: `F118` (a layout-dialog
>   leftover after a save/load, harmless as far as anyone can tell) and a one-line guard that makes the Edit
>   Payload fix say *why* if it ever stands down instead of going quiet. Cost: ~one session plus the usual gates.
>   This is exactly the "release a half-baked patch and immediately repatch" case you named as the bar.
> * **(b) Ship as is, fix in hotfix 3.** Players are no worse off than today; the error is live in v5 already.
>
> **128. Item 126 now also decides a sentence that ships INSIDE the mod.** The change note's second bullet tells
> players the small Astrogeologist bonus *"removing the fix cannot take back"* — written under your 09-08 ruling
> (leave it). Link 08 then built the pass that takes it back. If the pass stays, that sentence is false on
> upload; if you rule the pass out, the code comes out instead. **Rule 126 either way and the doc sweep
> (`100_DOCSWEEP.md`, written and waiting) carries both wordings** — plus the FAQ line that goes with it. It
> must run BEFORE the upload sitting, because the sentence ships in `metadata.lua`.
>
> **129. Publish the site in the SAME sitting as the upload, right after it — not before.** Link 06 asked for
> "same sitting"; the audit adds the order. The live page today still lists 82 fixes, which is correct for the
> v5 players actually have; the committed page lists 46, which is correct only once v6 is up. Publishing first
> would describe a pack nobody can install yet. **Recommendation: upload, then `UPLOAD_WORKFLOW` §4.**
>
> **What the sitting should expect from the boot log, computed rather than guessed: 44 applied / 0 inactive**
> (a first-pass read may say 43/1 — the Saint's-blessing module latches and then heals, that is normal). No boot
> of this 44-module pack has ever happened; every number in the chain so far is from the old 80-module one. Any
> `inactive` line at all is a finding, and eight modules changed their self-check since the last boot.
>
> ✅ **Nothing else is owed from you now.** The in-play controls stay batched in the one post-99 sitting as you
> ruled. Three smaller things were filed for hotfix 3 with no decision needed: a module (F60) whose target moved
> so it may be worth retiring, a vanilla track quirk (C55) to read at the sitting, and the F46 "is it even
> needed?" console read you already have on the list.

### ✅ 2026-09-09 — RULED AND DONE: you raised the `STATE.md` byte cap to 12 KiB, and item 126 is now IN it. Nothing owed; this is the receipt.

> **Your words:** *"I don't want things missing from state.md that we need to
> know. increase state.md cap by 10%."* → then, once I measured what 10% actually
> bought: *"lets go with decent for now, I can revisit it again later."*
> **Final: the warn moved 9216 → 12288.** (It passed through 10240 in the same
> sitting — that is the middle commit, not a separate decision.) This amends your
> 2026-08-18 ruling (item 42) on the number only — the byte-budget design, the
> per-line cap and the eviction procedure are untouched. The **hard** cap stays at
> 18432: it is the backstop for flags that go unread, not a budget.
>
> **Why the file was starving, which is the part worth keeping.** It had sat
> within ~15 bytes of the old warn across **36 commits over two days** of the
> 1.1.0 chain. It was **not growing** — sessions were evicting kernel content on
> every edit just to stay under, and item 126 was about to go unrecorded for
> exactly that reason. A cap a file sits *against* is not holding a budget, it is
> silently dropping content. That is the failure you spotted, and it is now
> written into `doccheck.py` beside the constant so the next reader gets it.
>
> **Where it leaves us: STATE is 9461 bytes with 2827 to spare — about 32 lines**
> at this file's density, against the ~9 that +10% would have bought. That is a
> real runway: it covers the 1.1.0 items as they close and link 99's pointer line
> without anyone budgeting bytes.
>
> **⚠️ The one thing to remember when you revisit.** This is headroom, not a new
> budget. Every byte of `STATE.md` is read by **every session at boot** — that is
> the entire reason the cap exists, and it is why I did not reach for a bigger
> number on my own. When the 1.1.0 fallout is closed, the right move is an
> eviction pass back toward 9–10 KiB rather than living at 12.
>
> ⛔ The line-ending phantom that made this look worse than it was is already
> fixed and is **not** part of this change: `.gitattributes` pins STATE to LF
> (09-09), so the count measures content, not the checkout. Verified 0 CR.

### ✅ 2026-09-09 — ITEM 126 RULED: **KEEP THE PASS IN** (see the ruling block at the top of this section). Left below as the reasoning you ruled on; link 08 wrote a pass that cleans up after **us**, and it changes what "remove the save sanitizer" means
<!-- ck:126 status:ruled owner:no -->

> **What we left behind.** One of the 36 modules link 02 deleted,
> `Fix_AstrogeologistExtractors`, did its job by adding two +10% extractor
> bonuses to the Astrogeologist commander profile. Those bonuses were written
> **into the savegame**, not just into memory — so deleting the module did not
> take them back. On 1.1.0 the game pays that bonus differently, and one of the
> two buildings (the Micro-G Auto Water Extractor) is now collecting **+30%
> water where the game intends +20%**. It is a bonus in the player's favour, so
> nothing is broken and nothing is lost — but it is a number we put there and
> the game did not.
>
> **What I did.** Added a pass to `90_SaveSanitizer` that finds those two
> entries and removes them on load. No new file, nothing about the shipped file
> list changes. ⛔ **It has never run in a game** — this is a written pass, not
> a repaired save, and I am not claiming otherwise.
>
> **⚖️ THE DECISION (this is the part that needs you).** On 2026-09-08 you were
> asked (item 117) whether to keep `90_SaveSanitizer` at all. That question was
> **entirely about players loading old 1.0.7 saves**, which only happens off
> Steam — so "Steam-only in practice ⇒ remove it" was a reasonable answer.
> **That is no longer the whole question.** This new pass has nothing to do with
> 1.0.7 saves: it cleans **1.1.0 saves that were played with our pack**, and
> those exist on every platform, Steam included. ⇒ removing the sanitizer now
> means *"leave a number we put in players' saves in there permanently"*.
> **I am not resolving this for you.** If you already leaned "remove it" on the
> platform question, this is the reason to look again.
>
> **What you will see, at the post-99 sitting (no action now).** Load a save and
> read the log for `SaveSanitizer: F95`:
>
> | the line says | it means |
> |---|---|
> | `removed 0 modifier(s), left 0 unidentified` | this save was already clean — most saves, and every save that was not an **Astrogeologist** colony |
> | `removed 2 …` plus a per-label line naming the label | this save carried our leftovers and they are now gone |
> | `LEFT n modifier(s) … ALONE` | ⚠️ something on that label looks like ours but I could not positively identify it, so I did not touch it. **Tell me if you see this line** — it most likely means another mod owns that entry, and removing someone else's is the one mistake here with no undo. |
>
> **Cross-check:** the Test Kit's `AstrogeologistExtractors` probe answers the
> same question independently — it FAILs if the loaded save still carries the
> leftovers. Probe PASS + a `removed 0` line = the save was genuinely clean.
> Probe FAIL + a `LEFT … ALONE` line = the near-miss case in the table above.
>
> **One thing I could not settle, recorded so it is not lost.** The game's own
> migration for this profile (`RefreshAstrogeologistExtractorBonus`) only
> matches old bonuses worth **20%**, and the 1.0.7 profile we have archived on
> disk pays **10%**. If those are the only two versions, that migration cleans
> nothing on a 1.0.7 save and vanilla leaves ten stale entries of its own. I
> cannot prove it — there were probably game versions between the two we hold,
> and the 20% may belong to one of those. It is **vanilla's residue, not ours**,
> and I did not touch it. Handed to the terminal audit (99) as a finding.

### ⭐ 2026-09-09 — LINK 07 IS DONE: the Test Kit now tells the truth about this build, and it can CHECK the 36 removals. ✅ **Nothing is owed from you now. One thing to read before you run the suite: the expected census below.**

> **What was wrong, in one line.** About 40 of the kit's 100 probes described a pack that no longer exists, so a
> suite run would have printed a wall of FAILs with **zero regressions in it** — the exact thing that trains a
> reader to ignore FAIL.
>
> **What changed.** 94 probes now (six were deleted, each named in its commit). **32 are a new kind, `retired`.**
> Those cover the modules link 02 removed, and they read **backwards** on purpose:
>
> | verdict | what it means for a `retired` probe |
> |---|---|
> | **PASS** | vanilla really did fix that bug ⇒ the removal is **confirmed in the game**, not just on paper |
> | **FAIL** | the bug is still there ⇒ **a removal was WRONG and players lost a fix** — a finding, not a probe bug |
> | **ERROR** | the probe's scaffolding is older than 1.1.0 ⇒ evidence of **nothing**, in either direction |
>
> ⭐ **This is the first time the pack has had a machine check on "vanilla fixed it".** Those 36 removals were
> decided by reading the game's source; until now nothing tested them in a running game.
>
> ⛔⛔ **EVERY NUMBER BELOW IS A PREDICTION UNTIL YOU RUN `SMRTest.RunAll()`. Nothing in this link was run in a
> game.** The point of writing them down is that the sitting can falsify them: **any FAIL not on this page is
> either a real regression or a probe I got wrong**, and either way it wants looking at.
>
> **What to expect from `SMRTest.RunAll()` on a 1.1.0 colony, with the pack ON:**
>
> * **94 probes: 55 `behavior`, 32 `retired`, 7 `install`.**
> * **4 named results that are NOT regressions** — please do not read these as breakage:
>   * `LanderCargoRatchet` and `AutoExportPriority` — expected **ERROR**. 1.1.0 rewrote the rocket cargo
>     allocator into a different shape; re-arming them means writing new probes, not patching stubs, and a
>     blind patch that happened to PASS would be a false "vanilla fixed it".
>   * `MoraleComfortTooltip` — expected **SKIP**. Confirming it means confirming a UI row is *absent*, which is
>     something you see on screen, not something a probe can read.
>   * `LocalizedUIText` — expected **SKIP** on an English rig (it needs a translation table to read).
> * The six `SaveRescue*` probes SKIP unless the save-rescue mod is loaded — that is by design and is normal.
> * The two `OptionsMenu*` and six opt-in probes SKIP unless the opt-in pack is ticked.
>
> **With the pack OFF** (the baseline half of the A/B): the 13 probes that guard on the pack report
> `fix pack not loaded`, which is correct and is what a baseline leg is for. ⭐ **The 32 `retired` probes should
> give the SAME verdict on both legs** — they measure the game, not us, and no module of ours is involved either
> way. **A retired probe that disagrees between the two legs is itself a finding.**
>
> ⚠️ **One row can report something real and is worth reading if it fires:** `AstrogeologistExtractors` FAILs if
> this save still carries a +10% bonus an older version of *our own pack* wrote into it. That bonus survives the
> module being deleted (it lives in the save, not the code), and repairing it needs a one-shot cleaner nobody has
> written yet. It is routed to the terminal audit as an owed item.
>
> ⛔ **Nothing here moves a status word**, and no bug entry gained "tested". The three probes links 03/04 warned
> you would false-FAIL, and the two links 04b warned would ERROR, are **rewritten and unrun** — they only become
> evidence when this sitting prints PASS for them.

### ⭐ 2026-09-09 — LINK 06 IS DONE: the store card and the site now describe the pack that actually ships. ✅ **Nothing is owed from you — but ONE thing must happen at the sitting, and it is easy to miss.**

> **What changed, in one line.** Link 02 deleted 36 of the 80 fixes because game 1.1.0 repairs those bugs itself.
> That made a lot of live public text false: **11 of the 20 bullets on your store card**, three of its four
> headline examples, its "Eighty-two repairs", and eight sentences across the site. All of it is now true.
>
> ⛔ **THE ONE THING AT THE SITTING: publish the site in the SAME sitting as the upload.** `UPLOAD_WORKFLOW` §4.
> The card now says *"Forty-six repairs"* and invites the reader to go and count them on the fix list — and the
> fix list is **committed but not published** (`publish-site.yml` is `workflow_dispatch` only, so committing
> never deploys). Until you run it, the live page still shows 82 and the card contradicts the page it points at.
>
> **Your paste backups are current.** `UPLOAD_WORKFLOW` §3 is synced with `metadata.lua` in the same commit and
> proven byte-identical, not eyeballed — the shipped string and the §3 plain block differ by zero lines, both
> BBCode blocks match, and the change-note block matches `last_changes`. If auto-fill fails again, paste and go.
>
> ⚠️ **The change note is five dashed lines rather than the usual two or three, on purpose.** This version
> retires ~36 fixes, and three of those are things a player can actually notice: the pack no longer holds an
> asteroid habitat's residents through a power cut, a line's train count stops refreshing after a salvage until
> you reopen it, and two extractor types keep a small Astrogeologist bonus **permanently in an existing save**
> (a new game is clean). Compressing to three lines meant dropping one of those, and a removal a player notices
> is not something to bury. Say the word and it gets cut back.
>
> ⛔ **No line anywhere says "Fixed".** Your rule of 2026-09-08 binds our own notes, and every in-play control
> from links 03, 04 and 04b is still owed — so the note tells players plainly that none of it has been watched in
> a running colony on 1.1.0 yet. Nothing claims 1.1.0 compatibility outright either.
>
> ✅ **112 needed no action and got none.** HOW IT WORKS bullet 3 is byte-identical to what shipped in v5,
> asserted mechanically rather than by eye. ⚠️ One wording correction, raised by the session that authored
> `prompts/SELFCHECK_PROMISE_AUDIT.md` and checked against this checklist's own item 112 before I recorded it:
> the item, its commit and my prompt all label this **"DEFERRED"**, and that label misreports what you decided.
> You did not defer it — you **rejected both options** and commissioned a third. "Deferred" reads as "we reword
> it next cycle", which is option (b), the one you turned down. The outcome for this upload is identical either
> way; only the recorded reason needed to be right, and it now is.
>
> ✅ **113 is honoured directly**, not by omission: *"updated for the new game code"*, never *"brought in line
> with"* — and it now describes this version's track-salvage work, capped at "matching the base game" because
> that repair has never been reproduced in a game.
>
> ✅ **118's store line landed.** Both cards now carry a portal-neutral pointer to the *Playing on 1.0.7* page.
>
> ⛔ **ONE THING I DECIDED THAT YOU MIGHT WANT TO OVERRULE, so it is here rather than only in an agent doc.**
> I found a **fourth** piece of live text that had gone false, and no upstream link had routed it: the Saint's
> blessing. Game 1.1.0 fixed that bug itself, and our module's own header now describes it as *"a save healer for
> damage a previous version of THIS PACK did, and nothing else"* — so the fix list's *"after the fix, the
> blessing lands"* was promising a repair the pack no longer provides. I took the clause off the store card and
> added a plain note to the fix-list entry rather than deleting the entry. The general lesson is the part worth
> keeping: the chain was watching the surfaces of the fixes it **deleted**, and a fix that was **kept** stranded
> a claim just as dead.
>
> **Not yet published anywhere.** Both commits are on `main` in their repos and pushed. No upload, no portal
> call, no site publish, and `version` is untouched — all four are yours.

### ⭐ 2026-09-08 — LINK 03 IS DONE: three repairs. ✅ **THEIR CONTROLS ARE DEFERRED TO ONE SITTING AFTER THE CHAIN, ON YOUR CALL. Nothing is owed from you now.**

> ⚖️ **RULED 2026-09-08 (owner): the sitting happens AFTER the chain, not now.** Your words: *"Can the sitting be
> done after the chain. I want to insure everything is green on this side and then we can check the live side?"*
> ⇒ these three controls are **not owed now**; they merge into ONE consolidated sitting after link 99, together
> with the in-play controls 04 and 04b owe (a first train leaving its platform, landscaping, vacuum walking).
> ⛔ **Do not re-raise them as outstanding before then** — a later session reading this block must treat the
> table below as *scheduled*, not *waiting*.
>
> **Why this is the cheaper order, not merely an acceptable one.** All of these are boot-and-play checks on the
> same colony, so running link 03's three now would buy a second sitting later for 04/04b's — which are the
> bigger half, and cover systems that have **never been exercised on 1.1.0 at all** (the 09-08 boot was
> menu-only). One sitting, one boot log, everything the chain built. The chain already has the slot for it:
> `99_TERMINAL_AUDIT` Pass G exists to list what has not been run in a game.
>
> ⛔ **TWO THINGS THAT RIDE WITH THE DEFERRAL.**
> 1. **A SHIP verdict from 99 is NOT clearance for the upload sitting.** It means the desk side is green. These
>    controls sit BETWEEN 99 and your sitting, and `H-04` binds: never treat a future release as ready.
> 2. ⚠️ **ONE PIECE OF EVIDENCE IS PERISHABLE, and it is the only one.** The `SaintBlessing` save re-base is
>    one-shot per save: the log line `SaintBlessing: restored N dome blessing(s) …` prints on the FIRST load of a
>    poisoned save and never again. If that save is loaded with a build carrying the fix during any intervening
>    work, the direct evidence is spent — you would still see the end state, but not the proof the re-base
>    produced it. ⇒ **do not load that save until the sitting.** 04/04b run nothing in a game, so this should not
>    come up on its own. ⛔ Do NOT copy the save as insurance — `EF-056`: loading a copy of a campaign runs that
>    campaign's autosave rotation and deletes your autosaves.
>
> **What was built** (`3db4984`, `f38d6d2`, `19b5aaa`). All three modules survive a 1.1.0 boot and all three were
> doing something wrong on 1.1.0. Nothing here has been run in a game: every repair is **derived from source**,
> and by your own 09-08 rule a "Fixed" is a claim until we confirm it. These three controls are the confirmation,
> and they are now scheduled rather than owed.
>
> | # | fix | what to do | time | what you should see |
> |---|---|---|---|---|
> | 1 | **Saint's blessing** (F-1) | On a save that was **loaded while the broken pack was on**, find a Saint in a dome with Religious colonists | ~5 min | those colonists show **"Blessed by a Saint"**. ⛔ It must be a *previously loaded* save — that is the half being tested |
> | 2 | **Expedition housing** (F-2) | Send an expedition, wait past 5 sols, bring the crew home | ~5 min of waiting | the returning crew **keep their own residence**, not a random one and not homeless |
> | 3 | **Asteroid habitat** (F-3) | Open an asteroid habitat and **set a trait filter** on it | ~2 min | **no error** in the log. (Before this build that threw) |
>
> They fit one sitting on the existing `BlankBig_02` colony. ✅ **Cheats are not a confound for any of these** —
> none of the three reads a quantity a cheat changes, so no clean run is needed.
> ⚠️ **Untick the Test Kit's force leg first if it is armed** (it was not, as of the 17:51 boot log).
>
> ✅ **RESOLVED 2026-09-09 by chain link `07_TESTKIT.md`** — the probes named here were REWRITTEN against the new module bodies, so they no longer report a stale verdict. ⛔ Rewritten, **UNRUN**: nothing was run in a game, and none of it is evidence until the post-99 sitting's pack-on leg prints PASS. The suite's expected reading for that sitting is the LINK 07 line below.
>
> ⚠️ **ONE THING WE GAVE UP, and you should know before the patch notes are written.** `ShelterReflex` had two
> halves; **half (a) is deleted**, not repaired. It made an asteroid habitat keep its residents through a brief
> power or air cut. On 1.1.0 it had become an outright **error** on any habitat with a trait filter, and the
> developers have since made "no life support" a deliberate design tier with the intent written into the shipped
> help text — so repairing it would mean fighting a stated design, which `FIX_POLICY` §4 bars. ⇒ **1.1.0 players
> get the vanilla behaviour back: a power blip still turns a habitat's residents out**, and they are re-homed
> automatically once life support returns. The shelter-reflex half (colonists head indoors before suffocating) is
> untouched and stays.
>
> ⛔ **This also makes a live public claim false.** The site fix list currently promises *"a habitat with a
> momentary life-support gap keeps its residents"*. That half is gone. Routed to link 06 with the exact lines —
> nothing for you to do, but it is the same shape as the F108/F107 wording link 02 already flagged.
>
> **Drafted patch-note lines** (link 06 owns the final wording; these are the honest versions and none of them
> says "Fixed" yet):
> * *A Saint's blessing works again with the pack installed. The game's own 1.1.0 fix and ours were cancelling
>   each other out; saves played in between are repaired on load.*
> * *Colonists returning from a long expedition keep the home that was held for them.*
> * *Setting a trait filter on an asteroid habitat no longer causes an error.*
> * *Removed: the pack no longer holds an asteroid habitat's residents through a power or air cut — the game now
>   handles that case deliberately, and colonists are re-homed by themselves once life support is back.*

### ⭐ 2026-09-08 — LINK 04 IS DONE: two re-copies (F-6, F-7) and the F116 edit you ruled (111 + 119). ✅ **Nothing is owed from you now; three in-play checks JOIN the post-99 sitting above.**

> **What was built** (`3f8394b` rocket refuel · `177c7b2` Edit Payload · `fc318c7` track salvage). Nothing here has
> run in a game. Every change is derived from source, cross-checked against BOTH shipped trees now that the 1.0.7
> source is back on disk, and exercised only in a desk harness (a real Lua parser on this rig, running the game's
> own bodies and ours on stubbed objects). By your 09-08 rule each of these is a **claim until the sitting confirms
> it** — that is what rows 4–6 below are for.
>
> * **Rocket refuel toggle** (F-7 / F50) — our copy of the drone fix ignored 1.1.0's new "Accept fuel" toggle, so a
>   rocket you had switched off kept asking for Fuel every hour. Re-copied with the clause. Stands down on 1.0.7.
> * **Edit Payload** (F-6 / F70) — our copy would have undone three 1.1.0 changes (the new tutorial's rocket-2
>   pre-fill, the re-template on a destination pick, a nil guard), and a **cancelled** payload prompt still counted
>   as "the player has spoken". Re-copied; the flag now lands only when you confirm. Stands down on 1.0.7.
> * **Track salvage** (F116, your rulings 111 + 119) — a piece left over by a split is now **kept on its own track**
>   instead of deleted, and a track holding both finished and under-construction pieces gets its post-split
>   processing. The load-time sweep stays as you ruled. ⚠️ This one is a behaviour change to destructive,
>   save-persistent code that has never run in a game — row 6 is the one that matters most.
>
> | # | fix | what to do | time | what you should see |
> |---|---|---|---|---|
> | 4 | **Rocket refuel toggle** (F-7) | On a landed rocket with a trip set, click **Accept fuel** to turn it OFF; wait two game hours; turn it back ON | ~3 min | while OFF: **no Fuel is requested or delivered**, and drones already heading to the rocket are **not** sent back on the hour (the old F50 fix still holds). Back ON: Fuel is requested again |
> | 5 | **Edit Payload** (F-6) | On a landed rocket: open Edit Payload, set ONE row to 0, confirm; fly the trip and return; open Edit Payload again. Then open it once more and **cancel** the launch prompt. Then **pick a new destination** for the rocket | ~10 min incl. the trip | after the trip the row you emptied is **still 0**. After the cancel, the next open shows what it showed before. After the destination pick the dialog **re-fills from the template** — that is 1.1.0's own behaviour and is exempt from our fix on purpose |
> | 6 | **Track split** (F116) | On a 1.1.0 colony with a train line: EXTEND the line while pieces are still under construction, then salvage ONE middle piece (a plain click, not Ctrl+click) | ~5 min | the line splits in two; **every remaining piece is still on a track** (nothing vanishes, nothing becomes unselectable); assigned trains survive; both halves accept a train. The log has no `TrackSalvageWipe` error |
>
> ⚠️ Row 6 needs a provisioned 1.1.0 colony with trains — the 1.0.7 fixtures cannot load (`EF-079`) — so it shares
> the colony with hotfix 1's "first train leaves its platform" control. ✅ Cheats are not a confound for rows 4–6.
>
> ✅ **RESOLVED 2026-09-09 by chain link `07_TESTKIT.md`** — the probes named here were REWRITTEN against the new module bodies, so they no longer report a stale verdict. ⛔ Rewritten, **UNRUN**: nothing was run in a game, and none of it is evidence until the post-99 sitting's pack-on leg prints PASS. The suite's expected reading for that sitting is the LINK 07 line below.
>
> ✅ **Items 111 and 119 below are LANDED** (`fc318c7`); their entries now say so. ⛔ Nothing here moves a status
> word, and a SHIP from 99 is still not clearance for the upload sitting (`H-04`).

### ⭐ 2026-09-09 — LINK 04b IS DONE: the three fixes you ruled back in (123) are RE-ARMED on their 1.1.0 bodies, gates kept. ✅ **Nothing is owed from you now; three in-play checks and one 1-minute console read JOIN the post-99 sitting above.**

> **What was built** (`799f145` landscaping · `3d4c933` train unloading · `7a401f1` vacuum walks). Nothing here has
> run in a game. Each module now carries the game's **1.1.0** function body with our one-line correction re-applied,
> checked three ways against both shipped trees (1.0.7 archived, 1.1.0 live) and exercised only in a desk harness
> that loads our module against the pack's own self-check code with the shipped bodies standing in for the game. By
> your 09-08 rule each is a **claim until the sitting confirms it**. ✅ **Every gate you approved on 09-08 is still
> there** — each is now the switch that makes the module apply on 1.1.0 and stand down on 1.0.7 (your item 118),
> with a second, behaviour-level check beside it that runs the game's own function on a dummy and applies only if
> it behaves the 1.1.0 way. ✅ F-9 did **not** need the `04c` split you pre-authorised.
>
> * **Landscaping over a boarding point** (F-8 / F34d) — back on. The game's 1.1.0 change was two lines (a new
>   `map` argument and where the landscape list lives); the bug itself is untouched in 1.1.0. ⚠️ One thing I was
>   told and found to be wrong: the fix's reach on 1.1.0 is **wider** than before, not narrower — flatten, raise,
>   lower AND clear-waste-rock sites all go through the repaired function now (the class that owns the call is the
>   parent of the flatten site; your 09-08 flatten crash proved the route). Your 2026-08-12 staging (a flatten over
>   drones boarding an RC Commander) is still the right test.
> * **Train unloading at a switched-off resource** (F-10 / F46) — back on, carrying all three of the game's 1.1.0
>   additions (the two nil-guards that caused F114, and a Black Cube bookkeeping call). ⛔ **One honest gap:**
>   whether 1.1.0 still HAS this bug is not established. The game now *suspends* a switched-off resource's request
>   instead of deleting it, and whether a suspended request still reports room is decided in C++ nobody can read.
>   If it reports 0, our guard is inert and harmless. Row 10 below settles it in one console line.
> * **Vacuum walks** (F-9 / F52) — back on. This was the big one: the game rewrote the whole function (47 → 98
>   lines: work-slot reservations, a "passages only" distance code, shuttle landing-slot checks, a train-ticket
>   discard). All of it is carried; our change is still the single line that makes a colonist in vacuum look for a
>   passage at any distance. ⚠️ Narrower on 1.1.0 by the game's own doing: a dome pair with NO outside route already
>   gets the passage lookup in vanilla, so what we repair is "an outside route exists, under 400 m, in vacuum".
>
> | # | fix | what to do | time | what you should see |
> |---|---|---|---|---|
> | 7 | **Landscaping over boarding** (F-8) | ⚠️ **Research "Dozer Rover" first** (or have the Landscaping Nanites breakthrough) — on 1.1.0 terrace/ramp/clear-waste-rock/textures are locked behind it, new since 1.0.7 (`EF-083`). Then park an RC Commander, order drones to board it, and while they are boarding drop a **flatten** over them | ~3 min + research | drones finish boarding; **no** `ExitImpassable` and **no error line** in the log; the site gets its stockpile and progresses (an RC Dozer on the job — 1.1.0 posts no landscaping work to drones) |
> | 8 | **Train unloading** (F-10) | On a line with two stations: switch a resource OFF at station A while B accepts it; send a train carrying it into A | ~5 min | the train **keeps** that resource aboard at A and unloads it at B; a train with nowhere to deliver still unloads; no `Fix_TrainCargoDumping` error line |
> | 9 | **Vacuum walks** (F-9) | Two domes under 400 m apart joined by a passage, on a non-breathable map; move a colonist between them (a home in the other dome) | ~5 min | the colonist walks **through the passage**, not across the surface. Destroy the passage and repeat: the surface walk resumes (the designed fallback) |
> | 10 | **F-10 premise** (console) | Select station A from row 8 (resource OFF), open the console, run the line below | ~1 min | a number. **Positive** ⇒ the 1.1.0 bug is real and our guard is doing work. **0** ⇒ 1.1.0 fixed it itself; our guard is inert, and F46 becomes a REMOVE candidate for the next patch |
>
> Row 10's console line, with `WasteRock` replaced by the resource you switched off:
>
> ```
> local st = SelectedObj print(st:IsResourceEnabled("WasteRock"), st.demand.WasteRock:GetTargetAmount())
> ```
>
> (expected `false <number>`; the first value confirms the switch is really off).
>
> ⚠️ Rows 7–9 need a provisioned 1.1.0 colony (the 1.0.7 fixtures cannot load, `EF-079`) — they share it with rows
> 1–6 and hotfix 1's "first train leaves its platform". ✅ Cheats are not a confound for rows 7–10. Row 8 doubles as
> the F114 control: the train must leave its platform at all.
>
> ✅ **RESOLVED 2026-09-09 by chain link `07_TESTKIT.md`** — the probes named here were REWRITTEN against the new module bodies, so they no longer report a stale verdict. ⛔ Rewritten, **UNRUN**: nothing was run in a game, and none of it is evidence until the post-99 sitting's pack-on leg prints PASS. The suite's expected reading for that sitting is the LINK 07 line below.
>
> **Drafted patch-note lines** (link 06 owns the final wording; honest versions, none says "Fixed"):
> * *Landscaping placed over colonists boarding a vehicle no longer pulls them out of it — re-enabled for 1.1.0.*
> * *Colonists moving between two nearby domes joined by a passage take the passage instead of crossing the
>   surface — re-enabled for 1.1.0.*
> * *Trains no longer unload a resource at a station where you have switched it off while another station on the
>   line accepts it — re-enabled for 1.1.0.* ⛔ This one may not be worded as a confirmed 1.1.0 bug (row 10).

### 2026-09-09 — ITEM 125 OPEN: the first checks the 1.0.7 tree makes possible were run — one real finding, one bounded reading pass to decide on, before 05 fires

> You asked what else the archived 1.0.7 tree lets us check before link 05. I ran three things nobody could run
> while the tree was gone. ⛔ Nothing here changes a module; everything is filed, not fixed.
>
> **1 · `bodycheck --src 1.0.7` over the whole stamped pack** — every pin was taken from the live 1.1.0 tree, so a
> BODY-CHANGED against 1.0.7 means "this target differs between branches". 28 rows differ. Of those, the five
> re-copies and 03's two repairs are expected. The rest are KEEP modules, and the question for each was: is our
> module a **copy** of the old body (the F116 shape, where we would silently undo a 1.1.0 change) or a **wrapper**
> that calls the live body (which carries the change)?
> * ✅ **No new F116 shape.** Every KEEP copy of a changed target is already on the 1.1.0 body (`TrackConnectorPingPong`,
>   `TrackSalvageWipe` after 111/119), unchanged across branches (`DomeFreeSpaceMismatch`'s copied function), or a
>   formatting-only span (`SinkholeIndestructible`). Two the proxy flagged as copies (`LayoutTechLock`,
>   `RocketInteractGuard`) are wrappers on a real diff — the 1.1.0 additions (water markers, mixed-pool stockpiles)
>   are carried.
> * ⚠️ **One real finding — `TrackConnectorPingPong` (F66) versus a NEW 1.1.0 forced path.** 1.1.0 added a one-shot
>   save-load fixup that rebuilds every station's track connectors with `force` and relaxed its assert to allow it.
>   Vanilla under force hands a contested hex to the station; our F66 guard leaves it with its current owner, so
>   that station gets **no connector on that hex**. This is the exact "asymmetry, unmeasured" line in F114's search
>   space, now with a call site. It fires once per save that predates the fixup, and only where such a save can
>   load — Steam blocks 1.0.7 saves, Paradox/console load them with a warning. ⛔ Not measured. **The repair is one
>   line** (honour `force` in the guard) and is written out in `bugs/F66.md`; it is code in a KEEP module, so it
>   needed your word. ⚖️ **RULED + LANDED 2026-09-09** (owner: "Go ahead and do it"): the guard now yields to `force`, done in this session, desk-controlled against both shipped bodies (`bugs/F66.md`). ⛔ Not tested in play and no rig control exists for it (Steam blocks the saves that trigger the fixup); 07 is asked to add a forced case to the kit probe.
> * ⚠️ **A bounded reading pass you may want, not a finding.** Eighteen wrapped targets differ between branches
>   (biggest: `Colonist:Idle` under `ArrivalDeaths`, 100 changed lines; `DemolishAndSplitTrack` under
>   `BrokenTrackSalvage`, 53). Wrappers carry the change, but the re-verification read those bodies without a
>   branch diff to steer it. The 1.0.7 tree turns "re-read the wrapper's assumptions" into "re-read them against
>   exactly these N lines" — a few hours of reading, best done by 99's Pass on the KEEP set or a dedicated link.
>   **Worth scheduling, or leave to 99?** (rec: give 99 the table, let it decide per module.) ⚖️ **RULED 2026-09-09 (owner: "go with your recommendation"): 99 decides per module.** The table is in 99's inbox; no separate link.
>
> **2 · `sigcheck --src 1.0.7`**: 1 MISMATCH, `LandscapeUnitFilter` — expected and correct, its body is the 1.1.0
> signature and it declines on 1.0.7. Every other replacement site has the same arity on both branches.
>
> **3 · Manifest coverage**: 11 functions the pack replaces or wraps carry no `SRC:` pin of their own (their module
> pins a neighbour instead), so `bodycheck` cannot see them move — 8 of the 11 DID change between branches. A
> tooling item; routed to 05 with the list. Nothing for you to rule.
>
> Landscaping (your two questions, same day): both new-in-1.1.0 facts are recorded (`EF-083`), row 7 above now
> says to research Dozer Rover first, and F115's "unverifiable" line is closed as verified.

### ✅ 2026-09-08 — ITEM 124 RULED: `StaleReservations` is FIXED, not removed. This was the last thing blocking chain link 03.
<!-- ck:124 status:ruled owner:no -->

> ⚖️ **124 — RULED: FIX.** Owner, verbatim: *"fix is the ruling."* ⇒ `Fix_StaleReservations` **stays** and gains
> the exemption clause; it does not go to a deletion sweep. **Link 03 is now unblocked in full** — all three of
> its modules are actionable and it can run as a single pass instead of stopping halfway.
>
> **What was wrong, and it is a real player loss — which is why FIX rather than REMOVE fits the 120 rule.**
> 1.1.0 added a legitimate long hold: boarding an expedition rocket saves `expedition_residence` before
> `SetDome(false)` clears the residence (`Colonist:EnterTransporter`, `Colonist.lua:5025-5031`) and reserves it
> back through `CanReserveResidence`/`ReserveResidence` (`:5003-5008`). Our 5-sol `NewDay` sweep cancels that
> real hold ⇒ **crew returning from a long expedition lose their home.** The lock is 3,600,000 ms while a one-way
> expedition is 1,440,000–3,000,000, so the window is ordinary, not exotic.
> ✅ Re-checked against the shipped 1.1.0 tree before recommending it, rather than taken from the brief:
> `expedition_residence` is live with 20 hits tree-wide, and both cited bodies read as described.
>
> **The repair is one clause** — skip colonists whose `expedition_residence` is truthy.
>
> ⚠️ **One honesty requirement that rides with it, and link 03 is told to put it in the module header.** 1.1.0
> bounds the ordinary shuttle-wait case this module was written for (F58) at one sol, so what the sweep still
> covers is **committed-shuttle limbo and the walk path** — NOT "F58 is still shipped". The re-verification
> report overstates this; the QA (§0.4) corrects it. The narrowed premise gets stated plainly rather than the
> module keeping its old claim.
>
> **Control this owes you (~5 min, batch it with 03's Saint control):** send an expedition, wait past 5 sols,
> and confirm the returning crew keep their residence with the pack on.
>
> ✅ **Nothing else in 03 needs a ruling from you.** Its other save-cleanup half — the `SaintBlessing` re-base —
> looks like the F-5 cleanup you ruled OFF under 120, but it is the opposite case and rule 120 already answers
> it: F-5's residue was an unearned **bonus**, whereas here vanilla's one-shot fixup already ran with our wrong
> value and will not re-run, so the Saint blesses **nobody** — a **loss**, so it gets repaired.

### ✅✅ 2026-09-08 — ITEMS 98, 117 AND 120 RULED IN-SESSION AND ACTIONED THE SAME HOUR. Nothing here is owed from you; one 3-minute control is offered at the bottom and it is optional.
<!-- ck:98 status:ruled owner:no -->

> ⚖️⚖️ **98 — RULED: DELETE, not gate. There is no 1.0.7 line in the live pack.** Your words:
> *"I am fine with the 1.0.7 issue, we are giving a path which we don't have to do. The main mod serves the
> current patch period."* ⇒ the 36 modules 1.1.0 made redundant are **deleted outright**, not carried behind
> per-module gates. This was the chain's blocking decision and it is now discharged.
> * **Done the same session** (`2dc1dbe`): 36 `Code/*.lua` files deleted, with `items.lua` and `metadata.lua`'s
>   `code` list brought to the same state — 81 → **45** in all three, which is what `module-list gate (tools/doccheck.py MODULE SETS + tools/upload_preflight.py)` exists to protect.
>   `doccheck --emit-counts` GREEN, modules 80 → **44** registered.
> * **Every row was re-derived against the shipped 1.1.0 body before its file was deleted**, rather than
>   inherited from the report. **37 rows, ZERO flips.** One needed a second look and the record was right, not
>   wrong: R-14's citation failed to reproduce only because rains use `GameTimeRepeat`, not `MapGameTimeRepeat`.
> * **Independent cross-check:** `bodycheck.py`'s NO-MANIFEST count went **46 → 10**, the exact landing point
>   link 01 predicted, which confirms the deleted set was the right set without re-reading a single row.
> * ⛔ **What this costs a 1.0.7 player, stated plainly.** They still receive hotfix 2 automatically — our
>   `lua_revision` and 1.1.0's minimums are all 350453 (`EF-077`), so nothing warns them — and 36 fixes stop
>   working for them. Their road back is the frozen v5 (item 118), and they have to notice it and walk it.
>   ⚠️ This does NOT relax item 118's binding constraint on the re-copies (F-6…F-10): those must still carry a
>   self-check that declines on 1.0.7. Delete-not-gate applies to the REMOVE set only.
>
> ⚖️ **117 — RULED: KEEP `90_SaveSanitizer`** (its F35 and F48 passes). You have ~200 Paradox users, and the
> deciding principle you gave is below. Only the **dead F03 pass** was removed (`f707903`).
> * The narrow truth about who this protects, since it is narrower than first described: `config.OldSavegameBehavior`
>   is `Platform.steam and "block" or "warn"` (`config.lua:175`). On Steam a pre-1.1.0 save **cannot load at all**;
>   off Steam the player gets a "Load anyway" prompt and brings 1.0.7 residue in with the save. And a colony
>   **started** on 1.1.0 can never carry this damage — `AppliedSavegameFixups` pre-marks every fixup as applied on
>   a new game (`SavegameFixup.lua:10-16`). So the population is: non-Steam build + an old save + Load anyway.
> * ⛔ **A record we had was WRONG and this is the correction:** F35 was retired on the grounds that a vanilla
>   fixup re-applies the buff. It does not — `WindTurbine.lua:95-105` re-applies `WindTurbine_Diffuser` only,
>   leaving the tech's `WindTurbine` and `WindTurbine_Large` labels unbuffed. 1.1.0 still ships that defect.
> * F03 went because vanilla genuinely does clean it now, on exactly the migrated saves that matter:
>   `SavegameFixups.RemoveLeakedUpgradeModifiers` (`Building.lua:1313-1345`).
>
> ⚖️ **120 — RULED: no save cleanup is built for the stranded Astrogeologist bonus.** Your principle, verbatim,
> and it is recorded because it generalises well beyond this one case:
> **_"we fix anything negatives, a small positive I am not as concerned about."_**
>
> ⚠️ [**Scope recorded 2026-09-12, item 161** — the phrase "it generalises well beyond this one
> case" above is the part that was wrong. The owner's own later account: this was **triage scoped
> to the 1.1.0 recovery**, an attention-routing device to keep agents on items that could do active
> harm while the pack was broken — **not standing policy about gains versus losses**. It expired with
> that condition and does not bind work after v9. ⛔ Do not cite ck120 as a live rule; cite item 161.
> The decision below stands exactly as made.]
>
> * The residue: `+10% production_per_day1` on AutomaticMetalsExtractors and `+10% water_production` on
>   MicroGAutoWaterExtractors, sitting in the persisted `UIColony.label_modifiers` of any 1.1.0 save that ran an
>   Astrogeologist playthrough under the pack. It is an unearned **bonus**, so it is not chased.
> * ⚠️ One correction to the reasoning that does not change the answer: the residue does **not** clear itself on
>   the next load. A **new game** is clean, because `label_modifiers` lives on `UIColony`; the existing save keeps
>   the +10% permanently. The patch note says that rather than implying it expires.
> * ✅ **Checked before accepting, because "leave it" would have been wrong if the residue were live:** the
>   persisted key is the save's own deserialised copy of a vanilla `Effect_ModifyLabel`, holding a vanilla `prop`,
>   in a vanilla container — nothing in it references our code, so the save still loads clean with the module
>   gone. The whole consequence is the bonus continuing to apply.
>
> **✅ 121 — WITHDRAWN THE SAME DAY. You were right to be suspicious, and nothing is owed from you.**
> I raised this as a decision on the claim that *"a 1.1.0 player gets no low-Food warning at all"*. **That claim
> was wrong.** You challenged it on the ground that the DLC's focus is literally food, so a silent deletion of
> food warnings made no sense — and the challenge held. My check had been **one file deep**: I grepped
> `ResourceTracking.lua`, saw only Power/Water/Air, and concluded tree-wide deletion without searching the tree.
> * **Both warnings were REPLACED, not deleted.** Food is now `StarvingColonists` — "Missed Meals", voiced
>   *"Warning! Food shortage"* — raised per dome with a reason breakdown and a severity, re-firing after
>   dismissal only when it gets worse, and driven off six colonist status-effect transitions. It is **new in this
>   branch**: there is a savegame fixup whose only job is to light it up on migrated saves. Maintenance is now
>   `MaintenanceStuckBuildings` — "Maintenance Problem", voiced *"A building is about to malfunction"* — covering
>   buildings *"about to or already"* stopped.
> * ⚠️ **The evidence was in a line I had already read.** `ResourceTracking.lua:316` is the migration off the old
>   maintenance notification — a signpost to where it went — and I logged it as "not a live warning" and drew the
>   opposite conclusion from it.
> * **The honest difference**, now derived instead of assumed: the retired warning was a *projection* ("N sols of
>   supply left"); the replacements fire on *state*. So there is no days-of-supply forecast any more, but the
>   player is warned, by dome and by building, with severity. ⇒ **Not a gap, and nothing for this pack to build.**
> * ⛔ **The removal itself is unaffected** — our module repaired arithmetic in branches that no longer exist, so
>   deleting it was right for the reason originally given. Only my description of the consequence was wrong, and
>   it is corrected on `F12` and in the patch-note brief so no store or site text repeats it.
>
> **Optional control, ~3 minutes, only if you want it** (batch it with link 03's): load an Astrogeologist save
> that ran under the pack and confirm the two extractors still carry the +10%. That is the *expected* state under
> 120 — it is a confirmation that we understood the residue correctly, not a repair to verify. Skipping it costs
> nothing.
>
> ⛔ **What none of this claims.** The removed fixes were correct on 1.0.7; what is true is that 1.1.0 fixes them
> itself. Removal is verified **in source** — nothing has been run in a game, and no status word was moved on any
> of the 43 bug entries for exactly that reason.

### 2026-09-08 — ITEM 118: how 1.0.7 players get served — Steam's branch feature is OFF, so it is one manual route

> ⚖️ **YOUR PLAN (2026-09-08):** serve 1.0.7 players a frozen build rather than carrying them in the live
> pack — Steam's own per-branch delivery if it existed, a GitHub Releases download for Paradox, and a line on
> both store cards pointing at written instructions on the site.
>
> ⛔ **STEAM'S PER-BRANCH DELIVERY DOES NOT EXIST FOR THIS GAME — REFUTED, BOTH PLACES SAMPLED.** Steam ships
> a Workshop Item Versioning feature that does exactly what you wanted (one listing; a player on an old branch is
> automatically served the matching mod version), and requirement 1 is met — the app has ordered branches,
> `Default Public Version` and `1.0.7 / Rollback version` (your screenshot). But it also needs the developer to
> tick **"Enable Game Branch Versions"**, and the author-side control that would prove it is on is absent in
> BOTH places Valve's documentation names: the item's **Change Notes** list shows only Edit / Download /
> Revert-to-this-version, and **Edit Change Note** holds only Language, Description and Save. ⇒ the feature is
> OFF for Surviving Mars: Relaunched. ⛔ **"Revert to this version" is NOT a substitute** — its own tooltip says
> it makes that version live for *subscribers*, i.e. ALL of them, 1.1.0 players included. Exactly backwards.
>
> ✅ **WHAT THIS SIMPLIFIES.** One route for everybody, Steam and Paradox alike: a GitHub Release holding the
> frozen v5, and a new **"Playing on 1.0.7"** tab on the site (`SMR-CommunityMods`, one `nav:` line + one
> `content/*.md` — a clean deletable unit when 1.0.7 dies), linked from both store cards and pointed at by a
> line in `install.md`. ✅ It also RETIRES the sequencing hazard: there is nothing to pin before the hotfix-2
> upload.
> * ⭐ **Best artifact: Steam's own `Download` button** on the v5 change note — byte-identical to what players
>   actually received, verifiable against the md5 already on record (`a1cbaad6294382068250ef390037f239`,
>   401,188 B, v5 = `bec2e06`). Better provenance than a rebuild from the tree.
> * ⛔ The instructions MUST say **unsubscribe first**. Workshop, Paradox and `AppData/Mods` all feed one dedup
>   keyed on mod `id`, higher `version` wins (`Mod.lua:1779-1783`) — a manual v5 beside a live subscription is
>   silently overridden, and the player would think they had done it right.
> * ⛔ **No console route exists**: the `AppData/Mods` scan is behind `Platform.desktop` (`Mod.lua:1706`).
>   ⚠️ Probably moot (console players cannot opt into a Steam branch, so Paradox presumably ships them 1.1.0) —
>   named because it is unverified, not because it is known to bite.
>
> ⛔ **THE FINDING THAT BEARS ON PLAYER SAFETY, AND IT IS INDEPENDENT OF YOUR ANSWER TO 98.** Nothing stops the
> hotfix-2 build reaching a 1.0.7 player: our `lua_revision` is 350453 and 1.1.0's `ModMinLuaRevision` and
> `ModRequiredLuaRevision` are BOTH 350453 (`EF-077`), so `IsTooOld()` is false on both branches and the update
> installs and loads on 1.0.7 with no warning of any kind. For the 34 deletions that is a REGRESSION (vanilla
> 1.0.7 bugs come back) — bad, not dangerous. ⛔ **For the re-copies (F-6…F-10) it is the F114 failure mode in
> reverse**: a module carrying a 1.1.0 function body, applied on top of a 1.0.7 function. ⇒ **every re-copied
> module must carry a self-check that DECLINES on 1.0.7**, whatever you rule on 98. That is now a binding
> constraint on the hotfix-2 fix prompts, not a preference.
>
> **Still yours:** decision 98 itself (delete vs gate the 34). This plan does not decide it — it only means a
> 1.0.7 player who is deleted-and-updated under has a manual road back, one they must notice and walk.

### 2026-09-08 — ITEMS 114–117 OPEN: the pack-wide 1.1.0 re-verification — 10 FIX, 35 REMOVE, 35 KEEP (QA'd)

> **The verdict, one line.** Every one of the 80 modules was opened against the shipped 1.1.0 body it wraps,
> replaces or patches (`docs/agent/reports/PACK_1_1_0_REVERIFICATION.md`). **35 modules do nothing useful on
> 1.1.0 because the developers fixed the defect themselves, and 5 modules that APPLY today do something
> wrong.** No code was written; nothing was run in a game.
>
> **114. Five modules are wrong on 1.1.0 right now — repair or remove each.** All five pass their self-check
> and apply. (a) `SaintBlessing`: 1.1.0 fixed the Saint label itself, so our patch now double-transforms it and
> **no Saint blesses anyone with the pack on** (`Lua/TraitPreset.lua:85-86`). (b) `StaleReservations`: our
> 5-sol sweep cancels 1.1.0's new "will return to this residence" expedition hold, so crew back from a long
> expedition lose their home (`Colonist.lua:5003-5008`, `Residence.lua:392-394`). (c) `ShelterReflex` half (a):
> `GetScoreFor` now takes the colonist, we pass its traits — a throw on any asteroid habitat with a trait
> filter (`Community.lua:442-453`). (d) `FirstAsteroidPrefabs`: the vanilla grant is gone; our sweep still
> hands out three free Micro-G prefabs and orphans a persisted thread (`Asteroids.lua:418-423`).
> (e) `AstrogeologistExtractors`: the profile was redesigned to a label-wide +20; we append +10% on two
> buildings on top of it (`CommanderProfilePreset.lua:335-352`). ⭐ **Recommend: (a) probe-gate, (b) one
> exemption clause, (c) delete half (a), (d) and (e) remove.** Each is a small change plus one boot log; (a)
> and (b) each want a 5-minute attended control, named in the report §2.
>
> **115. Retire the 35 REMOVE modules on 1.1.0 — as a block, delete vs gate per decision 98.** Report §1b,
> R-1…R-36, each with the shipped line that fixed it. Four are marginally WORSE than vanilla today
> (`SmallLandscapeSites` narrows drones 10→5, `TouristApplicants` rolls 0..100 vs vanilla's 0..99,
> `SpaceYDroneCapBullet` prints a duplicate bullet, `DustStormUndergroundBreaks` over-filters). One is a
> judgement, marked as such: `UniversityOvertraining` (automation is a FLOOR now, so specialists at automated
> extractors do matter). ⭐ **Recommend: retire all 35 on 1.1.0; if you keep a 1.0.7 line, they become gates,
> not deletions.** Two small re-copies (`RocketDroneChurn` ignores the new "stop refuelling" toggle;
> `PayloadTemplateRefill` breaks the new tutorial's pre-fill) ride the same prompt.
>
> **116. Accept the tooling design so the next game update is a tool run, not a week.** Report §4: a
> per-module `SRC:`/`DEFECT:` header pair plus `tools/bodycheck.py` (body hash + "is the defective expression
> still shipped?"), a behavioural `probe` form in `Require`, `sigcheck.py` over `SetGlobal` sites, and
> `logscan.py` counting heals (the "17 inactive" headline is really 16). ⭐ **Recommend yes**; no runtime
> behaviour changes, one script and header lines.
>
> ✅ **QA DONE (your ask, same day): three fresh-context readers re-derived all 46 REMOVE/FIX claims from the
> 1.1.0 code (`docs/agent/reports/VANILLA_FIX_QA.md`). No verdict flipped; no vanilla fix is a rebreak. Four
> things changed in the plan, all folded into 114/115 above:** (1) `DisasterPredictionLeak` is a SIXTH
> applies-today harm — its sweep clears the game's own normal-rain prediction flag, which has no notification,
> so a dust storm or cold wave can start during a rain warning; remove it. (2) Removing `Astrogeologist
> Extractors` needs a one-shot save cleanup of our two persisted label modifiers, or every 1.1.0 save keeps
> the +10%. (3) Repairing `SaintBlessing` needs a save re-base: vanilla's one-shot fixup already ran on saves
> loaded under the broken pack and will not run again. (4) `90_SaveSanitizer` is NOT in the REMOVE block: the
> 1.0.7-save block is Steam-only (`config.lua:174-175`) — **117. do non-Steam players matter?** If yes, keep the
> sanitizer's F35/F48 passes; if the pack is Steam-only in practice, remove. Also from the QA: `University
> Overtraining` should be a plain REMOVE, not a judgement.
>
> ⚠️ **What this does NOT cover:** nothing was played; the report §3 names every module whose verdict rests
> on a sub-reader's quoted lines rather than my own re-read. The two gated re-derivations you already know
> (`LandscapeUnitFilter` route (b), `TrainCargoDumping` F46 on the new depot base) plus `VacuumWalks` stay
> owed under decision 99.

### 2026-09-08 — ITEMS 112–113 OPEN: the hotfix-1 audit says SHIP WITH CHANGES, and both changes are wording

> **The verdict, one line.** A fresh session audited every one of the six changes against the shipped 1.1.0
> source and the boot log (`docs/agent/reports/HOTFIX_1_AUDIT.md`). **The code is clean: nothing to fix, nothing
> to gate, F116's repair should stay.** Decision 110 was actioned exactly as ruled (`00_Core.lua` byte-identical
> to v5; six files plus `metadata.lua` in the diff; nothing else). The boot log is complete and post-exit, and it
> reads what was predicted. ⛔ Still not exercised in play: trains, landscaping, track salvage.
>
> **112. The store description promises something the pack cannot do.** HOW IT WORKS, bullet 3, your own
> wording from 22d(1): *"Every fix checks the game's code before it touches anything, and stands down by itself
> if an official patch changes what it was written for."* The self-checks see whether a thing still EXISTS;
> they cannot see a same-name change of body or signature, and 1.1.0 just proved it twice (trains, landscaping —
> neither fix stood down). Every upload re-posts the description as the page body, so this upload would post that
> sentence beside a changelog that admits two fixes broke on the new version.
> * **(a) Reword it now, in this upload** — proposed: *"…and stands down by itself if the code it was written
>   for has been renamed or removed. That check cannot see every kind of change, which is why each game update
>   gets a compatibility pass. A fix that stands down does nothing at all — it never guesses."* Text only; the
>   §3 paste backups and `STORE_CARD_LIVE.md` are synced in the same commit.
> * **(b) Leave it for the next cycle.** The hotfix is a safety pass and this is a credibility line, not a
>   gameplay one.
> ⭐ **My recommendation: (a).** It is your sentence, so it is your call; the cost is one commit.
>
112. ✅ **RULED 2026-09-12 — take (a): the reword. DONE, in `metadata.lua` and both paste backups.**
> ⚖️ **This REVERSES your 2026-09-09 ruling on this item, which chose (c) — "make the sentence
> TRUE again" — and was recorded as a ruling, not an omission.** That block is left immediately
> below, verbatim and unedited, as the record. It is no longer in force: (c) is not being built,
> and item **133** records the four sub-decisions the reversal collapses.
>
> **The sentence that shipped** (HOW IT WORKS bullet 3, `metadata.lua`; the same words in the
> Paradox plain block and, in BBCode, the Steam block of `UPLOAD_WORKFLOW.md` §3 and
> `reports/STORE_CARD_LIVE.md`):
>
> > Every fix checks the game's code before it touches anything, and stands down by itself if
> > what it was written for has been renamed, removed or reshaped. A fix that stands down does
> > nothing at all — it never guesses. Every game patch is read against the pack as well, and
> > the fixes it changed are updated or retired.
>
> **What changed and why.** Only the false clause moved. *"if an official patch changes what it
> was written for"* promised something `SMRFixPack.Require` cannot do: it is an
> existence-and-surface test, so it sees a target renamed, removed or reshaped and cannot see a
> patch that keeps the name and rewrites the body — F115 was exactly that. The replacement is
> the pack's own honesty limit, already written in the code (`Code/00_Core.lua:620-625`) and
> already live on the site FAQ and in `README.md`. The second sentence was true and is untouched.
> The third states what actually covers the rest: the after-every-patch extraction diff
> (`WORKFLOW.md`), which is not a promise but a description of hotfix 1, hotfix 2 and v9 —
> 36 modules retired and 10 re-copied for 1.1.0, F60 retired.
>
> **Two candidates not taken, if you would rather swap one in.** Both are drop-in replacements
> for the whole bullet; tell me which and it is one commit.
> * **B, shortest — says what the check tests and stops there, no forward statement:**
>   *"Every fix checks the game's code before it touches anything — the functions and fields it
>   needs have to be present, and be the shape it expects — and stands down by itself if they
>   are not. A fix that stands down does nothing at all — it never guesses."*
> * **C, answers the update question first:** *"Every fix checks the game's code before it
>   touches anything, and a fix whose target a game update has renamed, removed or restructured
>   stands down by itself. A fix that stands down does nothing at all — it never guesses. Each
>   game update is read against the whole pack, and the fixes it changed are updated or retired."*
>
> **Reach.** Every live copy was found and changed; the three plain copies are byte-identical by
> script and both BBCode copies match. The site needed **no** change — `content/faq.md` and
> `content/for-modders.md` in `SMR-CommunityMods` already carry the "shape" wording *and* an
> explicit note about the body-rewrite case, and `README.md` already says "changed its shape".
> The store card was the only surface still carrying the old promise.
> ⚠️ The description grows **6,267 → 6,383** characters (+116). Both portals accepted 6,267 at v9.
> ⛔ Nothing here has been uploaded: it ships with **v10**, and `version` was not touched (`editor/version rail (agent/prompts/perma/RELEASE.md § Release rails)`).

112. ⏸️ **DEFERRED 2026-09-09 by the owner — 06 MUST SKIP IT, and this is a ruling, not an omission.**
> Neither (a) nor (b). The owner is firing a separate high-tier session on the option this item never offered:
> **(c) make the sentence TRUE again** — repair the capability rather than reword the promise down to match it.
> ⛔ **`06_TEXT.md` leaves `description` HOW-IT-WORKS bullet 3 exactly as it stands** and says so in its outbox;
> its §8 fallback already covers this, so no edit to that prompt is needed. ⛔ 99 must NOT flag this as an open
> loop or an unresolved audit finding — it is parked deliberately, with an owner-commissioned effort behind it.
> ⚠️ The sentence stays PUBLISHED AND OVER-PROMISING until that effort lands or the owner returns to (a).
> That is the accepted cost of the deferral, stated so nobody rediscovers it as a finding.
>
> ⭐ **One verified input for that session, so it does not spend its opening hours here** (link 05,
> `smr-bugfixpack-2b`, 2026-09-09, **source-read on the shipped 1.1.0 tree, NEVER executed in a game**):
> the sandbox blocks the obvious route and leaves a non-obvious one open.
> * `debug` IS blacklisted on 1.1.0, re-verified on this branch, not inherited from `EF-006`'s 1.0.7 reading
>   (`CommonLua/Modding/Mod.lua:1436`, inside `ModEnvBlacklist` which closes at `:1441`). So
>   `debug.getinfo`'s `nparams`/`isvararg` — which would have caught F115's arity change at runtime — is
>   NOT available to mod code.
> * ⭐ **`string` is NOT blacklisted, and the blacklist is checked on the TOP-LEVEL GLOBAL NAME ONLY**
>   (`ModEnvMeta.__index`, `:1558-1567`: `if env_blacklist[key] then return end` then `rawget(original_G, key)`
>   returns the real table whole). ⇒ **`string.dump` reaches mod code**, and it is the one runtime primitive
>   that can see a body change — the thing `Require` structurally cannot do and the reason bullet 3 is false.
> * ⛔ **The design question that decides whether this is usable, and it is not a detail.** A pinned dump-hash
>   makes a fix stand down when its target's body changes — but a Lua compiler or engine-build change would
>   flip EVERY hash at once and stand the WHOLE PACK down on a patch that broke nothing. That failure is worse
>   than the gap it closes. Any design must answer it before anything is built.
> * ⛔ **Even a perfect version of this does not make the sentence fully true.** Class (c) — semantics moving
>   under a wrapper whose target body is UNTOUCHED (F111, F112, F-1, F-2, F-3) — is invisible to body hashing
>   BY DEFINITION, and 6 of the 10 FIX rows in the 1.1.0 re-verification were class c. Whatever wording comes
>   out of that effort still cannot promise "any change".
> * ⚠️ `string.dump` raises on a C function, and much of the engine's global surface is C. Guard with
>   `pcall`. ⛔ And NONE of this is executed evidence: it is a source read of the sandbox, and this project's
>   standing rule is to trust runtime over source reads (`EF-078`: predicted 6, measured 13).
>
113. ✅ **RULED 2026-09-08, in-session — YES, take the proposed wording.** *"One track-salvage fix was also
> **updated for** the new game code."* Settled into `hotfix2/06_TEXT.md`; ⚠️ **ck112 is still UNRULED**, so that
> link's "leave those two strings alone" fallback now narrows to ck112 alone.
> ⚠️ Note for whoever writes the final string: items **111 and 119** now REPAIR both of the differences this
> item was hedging against, so by upload the sentence is conservative rather than merely honest. ⛔ Do not
> upgrade it to "brought in line with" on that basis — the repairs are still un-run in a game.
>
> **113. `last_changes` bullet 3 overstates the track-salvage change.** *"One track-salvage fix was also brought
> in line with the new game code"* reads as parity. Two deliberate differences from 1.1.0 remain (item 111 is one
> of them) and the repair has never run in a game. Proposed: *"One track-salvage fix was also updated for the new
> game code."* Same length. **Recommend yes**; text only, synced to `UPLOAD_WORKFLOW` §3.
>
> **Not a decision — a five-minute check worth your time before uploading.** Bullet 1 says "Fixed" for the
> trains. That is confirmed BY CONSTRUCTION (the module never installs on 1.1.0, so its throw cannot happen), but
> no colony has been played with the gated pack. On your existing BlankBig_02 colony: load, watch the first train
> leave its platform, assign the second. If it does, the note is confirmed the way you can see; if it does not,
> that is a finding and the note is wrong. ⚠️ Untick the Test Kit's force leg first if it is armed (it is not,
> per the 17:51 log).
>
> ⚠️ **Nothing here blocks the upload.** If you decline 112 and 113, the code still ships safely as it stands.

> ✅ **109 AND 110 ARE RULED, ACTIONED AND NOW MEASURED — 2026-09-08, the hotfix-1 apply leg. NOTHING IS OWED BY YOU.**
> **109 = GATE, route (a), done** (`628ea4d`). `Fix_LandscapeUnitFilter` now declines on 1.1.0. The replacement
> body is UNTOUCHED, so nothing pins us to 1.1.0's signature and the fix re-arms cleanly in a later patch.
> ⭐ The gate does not test a label. 1.1.0 moved `Landscapes` from a GameVar to a MapVar, and MapVars never
> create a global — so the check is the literal read that raised `attempt to index a nil value (global
> 'Landscapes')` in your repro. Your rule this week was "check the thing, not its label"; this is the thing.
> **110 = diagnostic only, VERIFIED not just accepted.** `Code/00_Core.lua` is byte-identical to the shipped v5
> file, `0` hits for the override symbols, and the pack's entire diff against live v5 is six files and
> nothing else — the five gate/guard changes plus F116's repair. **The pack ships ZERO diagnostic code.**
>
> ✅✅ **BOOT DONE, PREDICTION HIT EXACTLY — 2026-09-08 17:51. Nothing is owed from you on 109/110.**
> `63 applied / 17 inactive / 14 named`, **zero error-shaped lines**, and your dialog screenshot names both
> `TrainCargoDumping` and `LandscapeUnitFilter`. Predicted 17/14 before the reading; it came back 17/14.
> Canonical log archived as `archive/logs/gated110_Mars.exe-20260908-17.51.09-6a91a190.log`.
> ⭐ **Both P1s are dead, and by the strongest available route:** each module reports `inactive` with its
> gate's own reason string, so it never installed — the throws are impossible BY CONSTRUCTION, not merely
> absent from a sample. The open question about F114's hand-written `update_suspect` is answered: it works.
> ⛔ **WHAT IS STILL NOT TESTED, so the win is not overread.** That was a **menu-only** session (~2 minutes,
> no game loaded). **Trains and landscaping were never exercised.** "Zero throws" is therefore not a
> play-test result. The in-play controls — a train leaving its platform, landscaping raising no dialog, and
> the RC-Dozer separating control — remain unrun, and F116's track-salvage control (item 111) with them.
> ⚠️ Nothing about those needs to block the upload: the gates remove our code from the path entirely.
> ⚠️ **What 1.1.0 players lose, stated plainly, because it is the cost of the gates:** F34(d) is live again
> (landscaping can drag boarding colonists out) and F46 is live again (trains can dump cargo at a station
> where you switched that resource off). Both are vanilla bugs we were correcting and now are not, until the
> modules are re-derived against 1.1.0. That is decision 99's territory.
> ✅ **The patch notes are now cleared to upload** — the "Fixed for game 1.1.0" claim is confirmed, which is
> what your own "a Fixed line is a CLAIM" rule required. `metadata.lua` and the `UPLOAD_WORKFLOW` §3 paste
> backup are in sync. ⛔ Still no upload, no `version` edit, no Mod Editor from me (`editor/version rail (agent/prompts/perma/RELEASE.md § Release rails)`).

> ⚠️ **WHAT THIS PATCH DELIBERATELY DOES NOT CLAIM.** 17 of the pack's 22 full-body replacements have never been
> diffed against 1.1.0, and no instrument we own bounds body divergence — the name sweep sees names, `sigcheck`
> sees arity, the runtime self-checks see existence, and F114 was invisible to all three. That is why the notes
> say "a safety pass, not a full re-check of every fix against 1.1.0" rather than claiming 1.1.0 compatibility.
> ⭐ Not mine, so you know where it sits: **F116** (track salvage) was re-derived end to end by a parallel
> session under `prompts/F116_FIX_LEG.md`. ✅ **That is now DONE (`add94b3`) and `bugs/F116.md` is safe to
> read** — the entry was rewritten, its correction banner removed. It found a real defect and REPAIRED it in
> place, so this patch now carries **six** changes, not five. **Item 111 below is the one question it left
> you.**

### 2026-09-08 — ITEM 111 OPEN: F116 track salvage was repaired, and it left one judgement call

> **What happened, in three lines.** `Fix_TrackSalvageWipe` full-body-replaces the salvage/split function with
> a 1.0.7 copy. 1.1.0 added a step our copy does not have: it revalidates each track element's `node_idx`
> **before** sorting by it, because that number is a build-order counter and a track *merge* can leave two
> elements sharing one value. Without it our sort can be in the wrong order, and the deletion zone is then a
> **physically scattered** set of hexes instead of a contiguous run. That is the same corrupted-track outcome
> your PT-03 playtest reported back on 1.0.7 — we patched the *symptom* then; 1.1.0 fixed the *cause*, and our
> copy was throwing that fix away. ✅ **Repaired**: two additions, one call and one argument, no re-copy.
>
> ⛔ **NOT MEASURED, and unlike F114/F115 it never was.** No throw, no log line, no player report — this one
> came from reading the two bodies side by side. The repair has never run in a game either. ⚠️ A boot log
> saying `TrackSalvageWipe: applied` proves the module loaded, **not** that the repair works.
>
123. ✅ **RULED 2026-09-08, in-session — "group C": REPAIR ALL THREE.** Your words: *"All get fixed, If the work
> is really that heavy we should have a 04 and and 04b."*
> ⛔ **Filed and ruled together, because it had NO NUMBER — it existed only as "ck-C" inside a prompt and the
> chain README.** Same failure as item 119, hours apart: a real decision, blocking a live link, invisible to
> every surface you actually read. Numbered now so it has a receipt.
>
> **What it was.** Three modules are switched OFF on 1.1.0 and their game bugs are still in the game — the
> gates only take *our* code out of the path. Repairing means re-copying the 1.1.0 body with our fix
> re-applied on top:
> * **F-8 `LandscapeUnitFilter`** — landscape crash paths, reproduced 20/20 on PT-60. ⚠️ that was under the
>   OLD reach; 1.1.0 narrows it to Clear-Waste-Rock sites.
> * **F-9 `VacuumWalks`** — colonists walk ≤400m in vacuum past passages. Biggest surface in the patch;
>   1.1.0 rewrote the whole surrounding function. ⛔ Its gate is currently ACCIDENTAL (a rename broke the
>   self-check), which must become deliberate either way.
> * **F-10 `TrainCargoDumping`** — trains dump cargo at disabled stations. ⚠️ Nuisance class, and the premise
>   is UNREAD: nobody has established that a suspended request still reports a positive amount.
>
> ⚖️ **This deliberately and partly reverts ck109** ("gate, not repair" for F-8). Recorded loudly so nobody
> later reads it as drift: ck109 was ruled mid-emergency with a live P1 in players' games; this was ruled in
> a considered patch cycle. ⛔ The gates all STAY — they are what makes each module decline on 1.0.7 (118).
>
> ⭐ **Your 04/04b offer is now written into the prompt as pre-authorised**, with the chain's own rule 4 as
> the mechanism and a suggested cut (B + the F116 work in 04, group C in 04b). ⭐ **That was the right
> instinct:** 04 is the highest-risk prompt in the chain, and the failure it exists to prevent (F114) was a
> body copy written without enough room to think. My recommendation had been to repair only F-8 — you took
> the more expensive and more complete route, and splitting the link is what makes it affordable.
> ⚠️ **One thing your ruling does not make true:** F-10's defect is still unconfirmed. It will be repaired,
> but the close-out must say the premise was never established rather than implying the bug was verified.

119. ✅ **RULED ON FILING 2026-09-08** · ⭐ **LANDED the same day by hotfix2 link 04, commit `fc318c7`, in the same edit as 111** — **the SECOND F116 divergence, which had no ticket and which nobody would
> have raised until after the patch shipped.** ⛔ Filed and ruled in the same breath because you ruled it
> before it had a number; given one now so `99_TERMINAL_AUDIT.md` has something to cite when it sees the code
> change (an untracketed body edit to save-persistent code is exactly what that audit is built to catch).
> **What it is.** 1.1.0 post-processes each resulting track's **combined** element list; our 1.0.7 tail
> processes one array, and only when the other is empty — so a track holding **both** completed and
> under-construction elements gets **no post-split processing at all**. Recorded since 2026-09-08 in
> `bugs/F116.md` (claim 5, found by the structural diff) and in the module header as divergence B, but it
> never reached this checklist, STATE or the chain. ⇒ **Fixed in the same commit as item 111**, same function,
> same region, same audit. ⚠️ It is *inherited 1.0.7 behaviour*, not something we broke, and no harm has been
> observed — it ships with 111 because it is nearly free there, not because it is urgent.
>
> ⭐ **Worth noting as a process result, not just a defect:** this is the one that would have produced the
> "as soon as I patch, an agent tells me there is more to do" outcome you were trying to avoid. It was fully
> documented and still invisible, because it lived only in a bug entry and a code comment — neither of which
> is a surface anyone plans work from.

111. ✅ **RULED 2026-09-08, in-session — (b) ADOPT vanilla's policy** · ⭐ **LANDED the same day by hotfix2 link 04, commit `fc318c7` (the LINK 04 block at the top has the control, row 6).** **Your words: "fold them into whatever
> chain makes the most sense and update the audit."** Folded into **`hotfix2/04_RECOPIES.md`** (the body-copy
> link — same class of work, and it already carries `bodycheck.py` and the terminal audit), with a matching
> item in `99_TERMINAL_AUDIT.md`. ⛔ **THREE things were ruled together, not one:**
> * **(1) the orphan policy** below — rehome instead of delete;
> * **(2) a SECOND F116 divergence that had no ticket at all** — `bugs/F116.md` recorded two deliberate
>   divergences and only this one became a checklist item. The other: 1.1.0 processes each resulting track's
>   **combined** element list, our 1.0.7 tail processes one array and only when the other is empty, so a
>   track holding **both** completed and under-construction elements gets **no post-split processing**.
>   Ruled to be fixed in the SAME commit — same function, same region, same audit;
> * **(3) the load-time sweep STAYS as it is** (your "that is fine i agree"). It keeps deleting orphans,
>   because at load there is no split context to rehome into and it only fires on genuinely stranded legacy
>   debris. ⛔ Recorded as a RULING so a later reader cannot reopen it as an oversight.
>
> ⚖️ **The recommendation below was REVERSED, and the reason is not new information about the bug — the bug
> is unchanged.** It was written when this was a lone session with no reproduction, proposing untested
> changes to destructive, save-persistent code in a hotfix with nothing downstream to catch an error. The
> hotfix-2 chain removed that constraint: `bodycheck.py` now exists, link 04 is the dedicated body-copy link,
> and link 99 is an adversarial terminal audit. **The machinery changed, so the answer changed.** Left
> visible rather than rewritten, because the original reasoning is the receipt for why (a) was ever right.
>
> **111. Adopt vanilla's non-destructive orphan policy, or keep ours?** ⚖️ This is the one thing I found and
> deliberately did **not** change, because it is your call and not a hotfix decision.
> When a split leaves a track fragment attached to nothing, **1.1.0 gives it a new track and keeps it. Ours
> deletes it** — a rule your PT-03 playtest asked for, and it was right *then*, because 1.0.7 had nothing to
> rescue such a fragment and it really was unreachable debris. On 1.1.0 that is no longer true, so as it
> stands **our "don't destroy the player's track" fix can destroy track the unmodded game would have saved.**
> * **(a) Leave it (what is shipping now).** The repair above removes the thing that *creates* stray
>   fragments, so this should now be a rare corner. Zero further risk to a patch that is already written.
> * **(b) Match vanilla — rehome the fragment instead of deleting it.** Strictly kinder to the player and
>   removes a divergence. ⛔ But it is a behaviour change to destructive code, with no reproduction to test
>   it against, in a patch that is otherwise all safety.
> ⭐ **My recommendation: (a) now, (b) as its own small job once there is a 1.1.0 colony to test on.** ⚠️ Note
> the same delete-not-rehome rule also runs in the module's load-time debris sweep, so (b) would want both.
>
> ⚠️ **One more thing worth your attention, no decision needed.** `tools/sigcheck.py` rated this module **OK**
> before the defect was found and rates it **OK** now — same name, same argument count, different body. It is
> the instrument we lean on most, and this is exactly the class of problem it cannot see. That is the honest
> reason the patch notes do not claim 1.1.0 compatibility.

### 2026-09-08 — ITEMS 98–101: the game shipped **1.1.0 + the first DLC**, and the rig auto-updated. **99, 100 and 101 all CLOSED 09-12 as overtaken; 98's rig half stays open (⛔ Steam = ONE branch at a time).**

> *Services & Science* (1.1.0, Steam build 24995074) and the paid DLC *Feeding the Future* both
> landed 2026-09-08. Full reading: `docs/agent/reports/GAME_1_1_0_IMPACT.md`; facts `EF-075`
> (what the update did to our source base), `EF-076` (the target sweep), `EF-077` (the
> compatibility floor).
>
> **The headline, so you can triage in one line:** the pack is **not** broken and **not** flagged
> incompatible. 73 of 80 modules keep every self-check they declare; 6 switch themselves off
> cleanly and say so in the boot log; 1 latches benign. No crash path was found. **Nothing here
> needs shipping in a hurry** — the expensive mistake available is a rushed re-upload.
>
> ⚖️ **Your standing rule from today is written into the report and binds the whole effort:** a
> patch note that says "Fixed" is a **CLAIM, false until we confirm it ourselves.** No fix of ours
> is retired and no entry moves status on the strength of Haemimont's changelog.

⭐ **MEASURED 2026-09-08 — ITEMS 103–105, and they change the plan.** You launched, and one launch
> beat the whole desk audit. `EF-078`: **13 of 80 modules inactive (the dialog names 11), 67 active,
> pack loads unflagged, ZERO errors in the log.** ⛔ My source-read predicted **6** — wrong by 5, for
> two reasons now on the record (path specs checked by name not path; preset/DATA checks invisible to
> any symbol sweep). **Trust the game over my reading.**
>
> ⛔ **The big one: 1.0.7 saves CANNOT be loaded on 1.1.0** (`EF-079`). `USA Sol 302`, the F95/F59/F90
> fixtures, the T1/T2 uninstall pair — the whole library is **branch-locked to 1.0.7**. The game's own
> refusal dialog names the 1.0.7 branch route, which route-checks item 98's dev claim far better than
> the store announcement did.
>
> **103. How do we get a 1.1.0 train test?** ⚠️ No old save can be used, and trains are not early-game,
> so this is **hours of provisioning, not a 20-30 min warm-up** — the plan must not pretend otherwise.
> **(a)** cheat-provision a minimal 1.1.0 colony to a train (fastest, recommended); **(b)** switch the
> install to the 1.0.7 branch, which re-establishes the whole fixture library but tests the version
> players are leaving; **(c)** ask the reporter for their save first and provision nothing.
>
> **104. Force-loading old saves — you asked whether we can override it.** Yes: it is two config values
> and **the devs ship an unblocked mode** (`config.OldSavegameBehavior` is `"block"` only because we are
> on Steam; elsewhere the same build offers "Load anyway"). `EF-080` has both routes. ⛔ My
> recommendation is **triage only, never a verdict** — the supported floor sits deliberately *after* the
> research and services rewrites, so anything measured on a force-loaded colony cannot be attributed
> (mod, or half-migrated save?). And ⛔ **never in the shipped pack** — that would let players load saves
> the developers refused, and we would own the corruption. TestKit only, if at all. Do you want it built?
>
> **105. The opt-in pack is ENABLED and applying** (9 modules incl. `DroneOverhaul`) — ck43 records it
> OFF, so that record is stale. It is also a confound for any train leg. Leave it on (the 08-12
> both-mods-loaded normal config) or untick for a clean F114 A/B? I recommend untick for the first run.

> ⭐ **F114 — A SOURCE-PINNED CANDIDATE, 2026-09-08 (later), from the SAFETY_FIRST_FIXES session. ITEM 106.**
> `Fix_TrainCargoDumping` fully replaces `Train:UnloadAll` with a 1.0.7 body. 1.1.0 rewrote that function
> with two nil-guards ours lacks (`Train.lua:785-787`, `:794-795`) — and on 1.1.0 they are needed: the
> Station's depot base is now `MultiResourceDepotBase`, which creates **no demand request** for a resource
> whose lock state is not "enabled" (`MultiResourceCubeVisuals.lua:378`) while `Station:Init` still lists
> **every** transportable resource as storable (`Station.lua:110-111`). `BlackCube` and `Seeds` ship
> `LockState = "hidden"`. ⇒ on an ordinary 1.1.0 colony our copy indexes `station.demand["BlackCube"]`,
> nil, at `Fix_TrainCargoDumping.lua:89` on the first unload at any station; the command dies, the train
> idles, `NewHour` restarts it, it throws again. Pack off ⇒ vanilla's guarded body ⇒ trains move. That is
> the reporter's A/B — **as a prediction.** Full chain with every line in `bugs/F114.md`.
> ⭐ **The control costs 10 seconds and needs no provisioning**: in a 1.1.0 colony, select any station,
> console: `local st = SelectedObj; for _, r in ipairs(st.storable_resources) do if not st.demand[r] then print("no demand:", r) end end`
> — it should print `BlackCube` (and `Seeds`). Nothing printed ⇒ the candidate is dead. With the pack on
> and a train at a station, the log should carry `attempt to index a nil value` citing
> `Fix_TrainCargoDumping.lua:89`. **106. If the control confirms it: gate the module so it self-disables on
> 1.1.0 (the F113 shape — `Require` test on `MultiResourceDepotBase` existing; body in the entry), which
> restores vanilla's rewritten `UnloadAll` for every 1.1.0 player — or wait for the reporter's log first?**
> I recommend gate-on-confirmation: it is a self-disable, not a new behaviour, and the harm is a P1 field
> report. ⛔ Not done in this session — the brief forbids a train repair without a control, correctly.
> ✅ **CONFIRMED 16:25, YOUR OWN COLONY, SHIPPED CONFIG:** the log shows `Fix_TrainCargoDumping.lua:89: attempt to
> index a nil value`, locals `res = BlackCube`, stack `LoadTrain → TransferCargo → UnloadAll`, **157 throws at a 6-second cadence over the
> ~42-minute session (final count from the archived log; the live read said 30)**, and your "first train not moving at all" + "Track busy" are its two visible faces (the stalled
> train holds the spawn platform, `Station.lua:852-854`). The control is met. **106 is now live: say "gate it" and
> the `Require` test lands (with `Mars.exe` closed), restoring vanilla's guarded `UnloadAll` on 1.1.0 while 1.0.7
> keeps F46.** The pack-off half of the A/B is still worth 60 seconds of your time for a `tested-attended` word.
> ✅ **GATED on your go ("Game is closed", ~16:45).** Next boot should read **16 inactive / 13 named** with
> `TrainCargoDumping: inactive (the Station's depot base changed …)`, no `:89` throw, and the train leaving its
> platform. If any of those three is not what you see, that is a finding — say so. Cost: F46's own repair is absent
> on 1.1.0 until re-derived (decision 99); 1.0.7 untouched.
> Reply draft for the reporter (item 102) is now in `bugs/F114.md`, asking for the log (which would carry
> that exact line) and the save.

> ⭐ **THE SELF-CHECK OVERRIDE IS BUILT AND ARMED, 2026-09-08 (your ask, live sitting). ITEMS 107–108.**
> You asked to be exempted from the "11 fixes switched themselves off for safety" dialog and to have
> those modules enable anyway so their behaviour reaches a log. Both are in: `SMRFixPack_Force`,
> `SMRFixPack_NoUpdateDialog` and `SMRFixPack.ForceApply([id])` in the pack's `00_Core.lua` (commit
> `be4c99e`, pushed), armed from the Test Kit's new `Code/97_ForceInactive.lua` (`1d22835`, local-only —
> the Test Kit has no remote by design). ⛔ **All three ship INERT**: nothing in the pack ever writes the
> override, and with it unset every path is byte-for-byte the shipped behaviour. Console any time:
> `SMRFixPack.ForceApply()`, or `SMRFixPack.ForceApply("GridGlobalStorage")` for one.
> **It reaches 9 of the 11, and says so rather than pretending.** The four `DataPatch` modules
> (`SaintBlessing`, `DustSicknessDamage`, `IndependenceTerraforming`, `LastTransmissionStorage`) did not
> decline to run — their pass ALREADY RAN and found the preset data absent, so there is no withheld
> behaviour to reveal. Forcing them would relabel a module with nothing to patch, so `ForceApply`
> **refuses them by name**.
> ⚠️ **Two things that will otherwise look like discoveries and are not.**
> **(a)** Our own new 1.1.0 gates are `Require` specs, so forcing overrides them too: `LanderCargoRatchet`
> will call the deleted `GetEarthExportResPossibleReward` and **throw hourly at an Earth-landed automode
> rocket**. That is F113, already diagnosed — the tool working, ⛔ not an F113 repro, do not file it.
> **(b)** An **unforced** 1.1.0 boot from now on should read **15 inactive / 12 named**, where `EF-078`
> measured 13 / 11 — the F113 shape gate adds `LanderCargoRatchet` to both counts, the F112 content check
> adds `AutomationLawCompensation` to the inactive count only. ⛔ **That delta is OURS**; reconcile against
> it before calling a count change a game change.
> ⛔ **AND THE ONE THAT BITES: a forced rig is INVALID for any A/B, F114 included.** Forcing changes what
> the pack does, so a forced boot cannot answer "does the shipped pack cause this?" Disarm first — comment
> `"Code/97_ForceInactive.lua"` out of the Test Kit's `metadata.lua`. The peer session put that disarm
> step ahead of both F114 controls (`ce77162`).
> **107. When does the leg get disarmed?** I recommend: harvest one forced boot now, then disarm before
> anything train-related. Leaving it armed silently poisons every later reading, and the banner in the
> boot log is the only thing that would remind us.
> **108. Should the override stay in the shipped pack at all, inert, or be moved out to the Test Kit?**
> I recommend keeping it in `00_Core` inert: the Test Kit cannot reach `Require`'s failure branch from
> outside, so moving it out would mean losing the boot-time route and keeping only the weaker
> post-registration one. But it is three surfaces of dead code in a shipped mod, and that is your call.
> ⚠️ **NOT VERIFIED AT RUNTIME.** There is no Lua binary on this rig; structure was hand-reviewed and both
> files pass a block-balance check, but **your next boot log is the real syntax test**. If no
> `[CommunityFixPack]` lines appear at all, that is my error — revert to `ce77162` and tell me.

> ⛔ **F115 — A CONFIRMED, LIVE, SHIPPED P1, REPRODUCED ON DEMAND 2026-09-08. ITEM 109.**
> You hit "flatten landscaping" on a fresh 1.1.0 colony in the SHIPPED configuration and the engine's own
> mod-error dialog named **Relaunched Fix Pack**. Cause is pinned, not guessed: 1.1.0 changed the SIGNATURE of
> the global `Fix_LandscapeUnitFilter` replaces — `LandscapeForEachUnit(mark, callback, ...)` became
> `(map, mark, callback, ...)` (`Landscaping.lua:509`) — so every argument arrives one slot late. The log's own
> `Locals` block proves it (`mark | object Map`, `callback | number 51`). ⛔ **Every instrument we own missed
> it**: the self-check asks only whether the NAME exists (it does), and the F113 call-site sweep checked 106
> global names and 174 method names — **names**, which is exactly what survived a signature change. Same
> failure shape as `EF-078`'s path-checked-by-last-segment finding. **Check the thing, not its label.**
> ⚠️ **Worse than the popup**: the throw aborts `ConstructionSite:Initialize` mid-body, so
> `CreateResourceStockpile()` never runs. ⛔ How far that goes in play is UNMEASURED.
> ⚠️ **Separate from the RC Dozer rule.** 1.1.0 needs an RC Dozer (or `LandscapingNanites`) to service a
> landscaping job (`LandscapeConstructionSiteBase.lua:159`; status "You need an RC Dozer for Landscaping").
> **Drones ignoring landscaping without a dozer is vanilla, not us.** ⛔ Whether that rule is NEW is
> unverifiable — the 1.0.7 tree is gone (`EF-075`). Separating control: put a dozer on the job.
> ⭐ **The fix is still WANTED — 1.1.0 did not repair F34(d)** (`Landscaping.lua:520` still passes `callback`
> instead of its own `filter_embark`). So this is a live fix with a broken body, not an obsolete one.
> **109. Gate it, or repair it?** **(a) GATE** — self-disable on 1.1.0, the F113 shape; smallest change, stops
> the throw, costs players the F34(d) correction. **(b) REPAIR** — rewrite the body to 1.1.0's shape and get
> F34(d) back too. ⛔ A repair pins us to 1.1.0's signature and re-breaks on the next one unless a gate goes in
> as well. **I recommend (a) now and (b) considered separately with a control** — a safety-first patch should
> not carry an unverified new body. ⛔ Nothing shipped either way without your word.
> ✅ **Bounded by measurement, not hope**: `tools/sigcheck.py` (new) compared every replacement's parameter list
> against the shipped tree — **54 sites, 1 MISMATCH (this), 1 ABSENT (`TouristSatisfaction`, already off), 52
> OK.** ⛔ It does NOT cover the 15 `SetGlobal` sites or 5 anonymous function literals, and an `OK` never clears
> a same-arity BODY change. **Bounded, not cleared.**

> ⭐ **FIELD REPORT 2026-09-08 — ITEM 102, and it jumps the queue.** A player
> (*Ranger Dimitri*, Steam) reports: **"Using this mod cause them to not move between stations. When
> I turn it off they work as normal."** — trains, on 1.1.0, with their own A/B. `bugs/F114.md` has
> the verbatim text. ⛔ **No cause is claimed and none should be**: every sweep this session built
> passes CLEAN on all 11 train/track modules, `recompute_max_vehicles` is byte-identical to 1.1.0's
> own formula, and `CreateConnectorElements` matches 1.1.0 line for line bar our F66 guard. **A
> player found a breakage our instruments cannot see** — which is the honest measure of what those
> sweeps are worth. ⚠️ The reporter CANNOT narrow it for us: all 80 modules are default-active with
> no player toggle. The audit ranks this **FF-0, above all three desk findings**, and the brief
> (`prompts/SAFETY_FIRST_FIXES.md` §2A) deliberately forbids shipping a train repair — it narrows
> only. **102. Do you want the reply to the reporter sent, and the log + save requested?** A draft
> is prepared; asking costs you one message and is the fastest route to a cause.

98. **The 1.0.7 branch — pin back, or move the baseline to 1.1.0?** ⚠️ **This one gates
    everything else and it is the only time-shaped item.** The rig updated itself at 09:38 UTC
    and overwrote `ModTools\Src`, so the 1.0.7 line-number base every one of our citations was
    written against **is gone from this machine**. ⚠️ Your read was that Steam offers no way back
    unless the dev specifically authorizes multiple builds — **that authorization is exactly what
    happened**: the DLC announcement says verbatim that "Patch 1.0.7 will remain available through
    the 1.0.7 Branch" (Properties → Game Versions & Betas → 1.0.7). It is still a *dev claim about
    a store surface* and nobody has walked it here — Steam's local `appinfo.vdf` carries no branch
    block to check it against, so the dropdown is the only control, ~60 seconds. Options: **(a)** re-download 1.0.7 onto a branch install so A/B against the
    version our records describe stays possible — recommended, it is the only way to tell "1.1.0
    changed this" from "we were wrong"; **(b)** move the baseline to 1.1.0 and treat 1.0.7 as
    history, which is cheaper but makes every re-verification a fresh derivation; **(c)** both,
    if the branch route turns out to be per-install. Say which, and whether you want the branch
    route route-checked before anything else runs.

> ⚠️ **UPDATE, same day — the semantic audit started and is 2 for 2.** Two fixes whose targets all
> survived (so the sweep called them fine) turned out to be broken by 1.1.0's *meaning* changes:
> **F111** — `Fix_ExtractorStaffedPerformance` (F108) now **throws** when overtime is on, because
> 1.1.0's new `IsOvertime()` collapses `self.overtime` from a table to a boolean under it; and the
> defect F108 fixed is **gone from the shipped Lua** (vanilla now takes the same `Max` we do — read
> by us, not claimed by a note). **F112** — `Fix_AutomationLawCompensation` (C39) now **over-pays**:
> 1.1.0 deleted vanilla's automation compensation entirely while the laws still cut workers, so the
> 8 buildings C39 was written to bring up to parity are now the only ones in the game getting
> compensation at all. That one is a **player-visible balance divergence** in any colony running an
> automation law. Both are in the "body-copy of vanilla logic" class (`FIX_POLICY` §1.5) — 10
> modules carry one and they are the highest-yield place to look next. Items 98–101 stand; **99 now
> has two concrete cases in front of it.**
>
> ⛔ **SECOND UPDATE — a P1 crash, and the danger is bigger than either fix.** A full call-site sweep
> (every global, const, method and table-index in `Code/` against the 1.1.0 tree) found **F113**:
> `Fix_LanderCargoRatchet` calls `GetEarthExportResPossibleReward`, which 1.1.0 **deleted** (0 hits
> tree-wide; replaced by `GetEarthAutomodeFundingState`). Every gate it declares survives, so the module
> **applies**, and the function is re-run **hourly** while a rocket is landed ⇒ it throws every hour, after
> the cargo request is already written, so the low-funding auto-stop never fires. **Bounded good news:**
> outside the already-self-disabling modules that is the ONLY dead call in the pack, and `self.overtime`
> is the ONLY field whose table-ness 1.1.0 abandoned — so F111/F113 are the complete list of that kind.
> **Unbounded bad news, and the real danger:** **31 modules FULLY REPLACE a vanilla method** (no `orig`
> captured), so on 1.1.0 each substitutes a 1.0.7-era body for whatever the devs now ship — *anything the
> patch improved inside a replaced function, we silently undo.* F113 was caught only because one of its
> calls happened to vanish; **a replacement whose calls all still resolve is invisible to every sweep we
> have.** Those 31 are now the top audit target. F113 also carries a cheap immediate mitigation if you
> want one before the audit: add the dead method to its `Require` list so it self-disables instead of
> installing a body that throws.

99. ✅ **CLOSED 2026-09-12 as overtaken — all six are gone from the pack.** On your "if it's
    overtaken close it". Verified in the commit and on disk, not from a note: **`2dc1dbe`**
    (hotfix 2 link 02, 2026-09-08) deletes all six by name — `Fix_TouristSatisfaction`,
    `Fix_LowStorageWarning`, `Fix_GridGlobalStorage`, `Fix_RainsDeadlock`,
    `Fix_AsteroidLanderAvailable`, `Fix_DroneUnreachableForever` — and **none of the six is in
    `Code/` today**. The disposition rule this item asked for was answered in practice by option
    **(b)+(c)**, module by module, under the item-98 DELETE ruling. The three modules that were
    re-seamed rather than dropped were re-armed on their 1.1.0 bodies by link 04b, 2026-09-09:
    `Fix_LandscapeUnitFilter` `799f145`, `Fix_TrainCargoDumping` (F46) `3d4c933`,
    `Fix_VacuumWalks` `7a401f1` — all three present in `Code/` and carrying their branch guards.
    ⛔ The item's own warning still binds and is not discharged by this closure: **"its target is
    gone" is NOT "the defect is gone"** — a deleted module is not a repaired game.
    *(The original ask is kept below.)*

    **The six modules that now switch themselves off — what do you want them to be?** They are
    `Fix_TouristSatisfaction` (F09), `Fix_LowStorageWarning` (F12), `Fix_GridGlobalStorage` (F22),
    `Fix_RainsDeadlock` (F81), `Fix_AsteroidLanderAvailable` (F94), `Fix_DroneUnreachableForever`
    (F55/F57). Each declares a symbol 1.1.0 deleted, so `Require` declines and the fix does not
    apply — the designed safe failure, not a defect. ⛔ **"Its target is gone" is NOT "the defect
    is gone"** — only **F09** is settled, and settled by a *fact* (the Satisfaction stat itself
    was removed), not by the note that says so. For the other five the underlying defect may well
    still be live and simply need a different seam. The decision is the **disposition rule**:
    **(a)** leave them shipped and inert until each is re-derived on 1.1.0 — recommended, costs
    nothing and a self-disabled module is harmless; **(b)** actively retire the ones we can prove
    obsolete; **(c)** re-seam them as they are re-derived. This is a "defect or not" call, so it
    is yours under `FIX_POLICY` §4a, not an agent's.

100. ✅ **CLOSED 2026-09-12 as overtaken — the message went out with v6, and we did not decide to
     send it.** On your "if it's overtaken close it". The recommendation here was (a), say nothing;
     what actually happened is that the hotfix-2 upload carried the substance of (b) anyway,
     because the card is rewritten from `metadata.lua` on every upload. From the 2026-09-09 v6
     receipt block above: the Steam description auto-filled with the recounted headline and **the
     1.0.7 section** (ck118's line, pointing 1.0.7 players at the frozen build), the v6 note went
     on the Change Notes tab, the Paradox card auto-filled with the same body, and **the site
     republished with both "built against" lines reading 1.1.0.403908**. The live card still
     carries that section today (`metadata.lua`, "STILL PLAYING ON GAME VERSION 1.0.7?").
     ⇒ A player looking at either listing can now see where the pack stands on 1.1.0. The question
     "do we say anything yet" has no live answer left. *(The original options are kept below.)*

     **Do we say anything to players yet?** The pack is live at v5 on both portals and every
     player who auto-updated is now running it on 1.1.0. `EF-077`: we clear 1.1.0's mod floor by
     **exactly zero** (`ModMinLuaRevision = 350453`, our `lua_revision = 350453`, the test is a
     strict `<`), so no incompatibility prompt fires and saves do not mark us obsolete. So there
     is no forced action. Options: **(a)** say nothing until the re-verification has something
     true to report — recommended, and it keeps `H-04` clean; **(b)** a short "known-good on
     1.1.0, six fixes stand down pending re-check" note on the listings, which costs an upload
     cycle (`editor/version rail (agent/prompts/perma/RELEASE.md § Release rails)`: the version bumps again) and would be publishing a claim we have not measured
     yet. ⛔ Note that **any** listing edit overwrites both page bodies from `metadata.lua` and
     needs the §3 paste backups.

101. ✅ **CLOSED 2026-09-12 as overtaken — a chain ran, in a different shape, and it finished.** On
     your "if it's overtaken close it". The C1–C5 shape proposed here was never built. What ran was
     `agent/prompts/hotfix2/` — links 01, 02, 03, 04, 04b, 05, 06, 07, 08, 99, 99a, 99b, 100 — and
     **every row in that README's table is struck through and marked DONE**, which I read off the
     file rather than taking on trust. Its terminal audit returned **SHIP WITH CHANGES** and is the
     authority: `agent/reports/HOTFIX_2_AUDIT.md`. The work this item wanted done is done
     (36 modules removed, 10 re-copied, the store card and site recounted, the Test Kit rebuilt),
     so accepting or reshaping the proposal cannot change anything.
     ⛔ **It is not a clean bill.** The audit's own gaps stand, and the post-upload sitting it owes
     is still open — see the ⛔ owed rows in `agent/STATE.md`. *(The original proposal is below.)*

     **The re-verification chain — accept the shape or reshape it.** Re-checking 82 shipped fixes
     across two wholesale system rewrites (research and services) is far past the ~2-session line,
     so `CHAIN_METHOD.md` says it should be a self-consuming prompt chain with a terminal backward
     QA. Proposed in the report §5: **C1** baseline + the live `ListFixes()` read → **C2** the six
     dead modules → **C3** the redesigned systems (services, research, landscaping, supply grids,
     rockets, food decay) → **C4** the patch-note claim table, one control per row → **C5** fresh
     -context adversarial QA. Accept, reorder, or cut scope — and tell us where it sits against
     the opt-in pack (item 68), which was the named next effort before today.

### ✅ 2026-09-01 — ITEMS 89–97 **OFFLOADED to the opt-in repo 2026-09-12 (ck167).** Item **88 STAYS** — it is a fix-pack feature. **Nothing here is owed from you.**

> ⭐ **Your ruling:** *"Can we fully offload anything opt-in related to its repo, and just retain
> anything that's fact based that could be useful — and rehome those facts where they should be?"*
>
> **Where they went.** Items **89, 90, 91, 92, 93, 94, 95, 96, 97** — the drone-rebuild design spec,
> the bands-and-clean-revert report and the contamination audit — are now
> `C:\Dev\SMR-OptInPack\docs\DECISIONS_OWED.md`, **reproduced verbatim**, alongside 84 and 85.
> Nothing was deleted, nothing re-summarised, and the four source reports were already in that repo.
> ⛔ **They are that mod's launch obligations. It is not launching, so nothing is owed.**
>
> ✅ **No engine fact needed rehoming, checked rather than assumed.** Every fact those items cite —
> `EF-023`, `EF-059`, `EF-069`, `EF-072` — is **already in this repo's `agent/facts/INDEX.md`**, which
> is the canonical home for both repos (item 86). Nothing was stranded by the move.
>
> ⚠️ **Recorded on the way out, because it is the thing most likely to mislead whoever opens that file:**
> all of it was written 2026-08-31 / 09-01, **before 1.1.0 + the first DLC shipped on 09-08**. Every
> citation in it predates the patch and **none has been re-verified since.** The file says so at the top.

88. ⏸ **STAYS — it is a FIX-PACK feature parked in the wrong repo.** `FUTURE_IDEAS.md` #9,
    "per-fix player toggles for the FIX PACK", is a Mod Options page for **this** mod's fixes; it was
    routed to the opt-in repo on 2026-08-14 by analogy to #5, and has no ruling of its own.
    ⭐ **It is also no longer hypothetical: this is what checklist 148's `prompts/fixtoggles/` chain
    builds**, and you deferred that on 09-12. ⇒ **Nothing to decide here** — #9 is overtaken by 148
    and rises or falls with it. ⚠️ Its two stale riders are noted so nobody chases them: it cites
    `MOD_DESCRIPTION.md` (frozen) and a prompt that no longer exists (`COVERAGE_SWEEP_SMRCF.md`).


### ✅ 2026-08-31 — ITEM 87 RULED THE SAME DAY: drones UNFROZEN
<!-- ck:87 status:ruled owner:no -->

87. ✅ **RULED 2026-08-31 — "Un freeze drones" (verbatim).** Lifts the PT-52
    freeze and the module freeze on the opt-in mod's `Opt_DroneOverhaul` (D06)
    and `Opt_DroneStatDials` (D09): design and playtest work may resume under
    FIX_POLICY with an A/B per change. Recorded in the opt-in repo's `STATE.md`
    and `D06.md`; PT-52's status below updated. Still yours: the D06 design
    decision itself (`prompts/perma/DRONE_PROJECT_PROMPT.md` §3 — three options), and
    whether `FUTURE_IDEAS.md` #7 (gleaner / pairing policy) is un-parked too — this
    ruling was read as NOT touching that post-launch parking.

### ✅ 2026-08-31 — ITEMS 83–86: **84 and 85 OFFLOADED to the opt-in repo 2026-09-12 (ck167). 83 and 86 STAY — they bind the fix pack, not that mod.**

> Raised by the opt-in mod's readiness pass (its repo, `docs/agent/reports/READINESS_REVIEW_0831.md`).
> **84** (three unpaired wrap sites in its `Code/`) and **85** (its preview art) are that mod's launch
> obligations and now live in `C:\Dev\SMR-OptInPack\docs\DECISIONS_OWED.md`, verbatim. The two below
> did **not** move.

86. ⚠️ **STAYS — it is a rule about THIS repo's facts index, not an opt-in decision, and it is
    ALREADY IN FORCE.** `EF-###` ids are allocated **here**. After the split both repos minted their
    own numbers and collided (the opt-in repo's `EF-057`/`058` of 08-16 were different facts from
    ours). Resolved 08-31 by re-syncing its facts folder from ours @ `bec2e06`, and the rule is
    written into that repo's `WORKFLOW.md`: **a fact learned there is filed HERE first** (or its next
    id reserved here), then mirrored there at the same id. ⇒ **Nothing is owed** — it costs you
    nothing and it is running. Say "reverse" only if you ever want independent numbering with a
    prefix instead. ⭐ This is also why no engine fact needed rehoming in the 09-12 offload: every
    fact those items cite (`EF-023`, `EF-059`, `EF-069`, `EF-072`) was **already in our index**.

83. ⏸ **STAYS — the Test Kit is SHARED, so these edits land in our tree.** ⛔ **Not owed, and not
    urgent:** every item needs a real launch to verify, none was made, and the opt-in mod is not
    launching. Survey findings (`READINESS_REVIEW_0831.md` §5): the kit has **no opt-in-only run
    mode** (a standalone leg prints ~85 fix-pack FAILs around 8 real verdicts); **D06
    `DroneOverhaul` has no `RunAll` probe**; `98_EnablePathLeg.lua:54` hardcodes
    `SMR_CommunityFixPack`, so the opt-in mod's normal first-run path has never been measured by
    that leg; `99_FixtureCarry.lua` channel 5 hardcodes `SMRFixPack_F35_` and cannot see D09's dial
    modifiers; only D12 has a vanilla-control clause. **Proposed, in value order:** (1) `RunAll`
    owner filter + a `fix pack absent = expected` mode; (2) `PACK_ID` parameter on the enable-path
    leg; (3) FixtureCarry D09 channel; (4) a D06 `RunAll` probe; (5) control clauses for
    D01–D04/D07/D09. ⚠️ Items (1) and (2) would improve the kit **for us** regardless of that mod,
    which is the only reason this is still on your list at all.


### ✅ 2026-08-30 — ITEM 82 CLOSED: F110 live on both stores in v5, site deployed, delivered Steam pack verified. Nothing owed.
<!-- ck:82 status:closed owner:no -->

82. ✅ **SHIPPED — v5, both portals, 2026-08-30.** You packed and uploaded Paradox
    then Steam; you told me the store pages look good. The tree now reads `version 5`
    (up one from 4); `pdx_id`/`steam_id` unchanged and written back (Paradox rev
    `pdx_version` "4"). The release words are live: the card count moved
    **Eighty-one → Eighty-two repairs** on both store bodies, F110's change note is
    the version's changelog entry, and a headliner bullet ("A Jumbo Cave mystery
    could get stuck clearing waste rock and never complete") is on the card.

    ✅ **SITE DEPLOYED** — you ran Publish; newest run `ce3a3779` (== site HEAD),
    status success, **82** live fix-list entries. The store "Eighty-two" now matches
    the page it links to; count constraint closed.

    ✅ **Both questions answered 08-30.** **(1) Auto-fill did NOT deliver a clean
    page** — you pasted the `UPLOAD_WORKFLOW.md` §3 backup by hand. So after two
    upload cycles the auto-fill path has never once stood on its own: the §3 paste
    backups are the real delivery mechanism, **required and kept current**, not an
    optional fallback. You're treating the pasted plain text as a placeholder and
    will apply the headings/bold formatting later — cosmetic, no rush.
    **(2) No required-game-version field** was offered on either page — nothing to
    set, nothing owed.

    ✅ **DELIVERED PACK VERIFIED** (§0.5(f)) — your subscribed Steam copy downloaded
    to `steamapps/workshop/content/**3215050**/3787202810/ModContent.fpk` (Relaunched
    is app 3215050, not 464920). Read with `tools/pack_list.py`: **85 entries**
    (== `pack_predict`), **83 byte-identical** to the tree; the only 2 that differ are
    `metadata.lua` + `items.lua` (the forced-save comment strip, same as v4's 84/82).
    Extracted `metadata.lua` confirms `version 5`, count word **"Eighty-two repairs"**,
    the F110 change note, and `Fix_JumboCaveReinforcementWedge` in the code list.
    **md5 `a1cbaad6294382068250ef390037f239`, 401,188 B.** First delivered md5 this
    project has ever computed from a real portal artifact.

<details><summary>the attended-fix receipt (08-30, for the record)</summary>

    ✅ You decided to fix it, the module was written, and the attended A/B passed: on
    the re-loaded still-stuck `International Mars Mission Sol 84` the module's own
    control line fired —
    `[CommunityFixPack] JumboCaveReinforcementWedge: force-cleared 1 unreachable waste rock(s) …`
    — and the mystery auto-completed. Confound ruled out: your material cheat only
    supplied build resources (needed to *build*, not to *clear*) and you didn't
    finish-construct; the clearing is the fix's, by its own log line. `F110` flipped
    to `fixed`; log archived (`archive/f110_attended_…16.41.16.log`). One same-day
    hiccup handled: the first build required `Cities` at menu time and self-disabled
    (the dialog you saw) — Require trimmed, applied clean on the next boot.

</details>

<details><summary>original decision text (for the record)</summary>

**Confirmed, first time ever.** A Reddit reporter's save (you bought the
    Interplanetary Codex pass to load it) reproduced the month-old Jumbo Cave
    wedge on our exact build. Console read while stuck: a `JumboCaveReinforcementStructure`
    site down to its last waste rock, that rock a `WasteRockObstructor` the drones
    can't path to (in 2 drones' `unreachable_buildings`), site never clears, mystery
    soft-locks. Permanence witnessed (the unreachable flag reset on load, then
    rebuilt after ~1-2 min of run). Filed as **`F110`**; C25 is closed-promoted.

    **The decision is yours — three parts, and none is urgent:**
    - **Fix or leave?** It's a genuine soft-lock with no player recourse, which
      `FIX_POLICY` normally favours fixing — but it's niche (needs a Jumbo Cave
      *and* the geometry to strand a rock). **Rec: fix, in a future patch, not a
      hotfix.**
    - **Shape?** fredware's known repair is *reactive* (wrap the vanilla approach,
      act after a failure). A *proactive* shape would need the finer root cause
      first — WHY `Rocks_04` is unreachable (terrain vs a cleared pile vs an
      adjacent obstacle), which I did **not** measure. **Rec: characterise the
      geometry on the loaded save before choosing a shape.**
    - **Timing?** Post-launch = patch-note maintenance (your ruling); this rides a
      future patch, not its own cycle. No gate re-run for one added fix.

    ⇒ **Say the word and I'll (a) take the geometry read off the still-loaded save,
    then (b) bring you an A/B fix proposal.** Nothing is owed until you decide.

</details>

### ✅ 2026-08-29 — ITEM 81 DONE, you ran it 18:44Z and the site is fully deployed. ITEM 80 WITHDRAWN IN FULL, both halves. Nothing is owed on the site or either store.

81. ✅ **DONE — deployed `fcb2aa9`, status `success`, 2026-08-29T18:44:14Z.**
    Verified on three controls: the deployments API, the live index page (now
    reads *"six fixes are judgment calls"*), and `git log fcb2aa9..HEAD` in the
    site repo, which is **empty — every commit is now public.** Live fix list
    still 81 entries. Was: index.md said **five**, the FAQ said **six**, twice.

    The repo is already right: `fcb2aa9` corrects index.md, and it is the **only**
    commit not deployed. The two edits landed in *different* commits (`7f4bb78`
    did the FAQ, `fcb2aa9` did index.md), so deploying one and not the other left
    the public site disagreeing with itself while the repo looked consistent.

    ⇒ **one run of *Actions → Publish docs site*** on `SMR-CommunityMods` clears
    it. Low severity — nobody is misled about what the pack does — but it is the
    kind of thing a reader notices and it costs a minute.

80. ⛔ **WITHDRAWN IN FULL — both halves were wrong, and the fault was mine.**

    **(a) Steam.** I said the Steam listing had neither F105 nor F108. It had
    both. You refuted it with the Workshop change-notes page and by subscribing;
    the delivered archive settles it — 84 entries, 82 byte-identical to our tree,
    both fix modules present, packed `version` 4. I had argued from the version
    number, and `RELEASE_PORTAL_PREP.md` §0.5(c) describes a **first** upload in
    the sentence I was quoting. Recorded as `EF-068`.

    **(b) The count.** I said both stores claimed "Eighty-one repairs" while the
    site backed only 79, and called it a live falsifiable claim. **It is backed.**
    You deployed the site on 08-24 *and* 08-28; the live deployment is `7f4bb78`,
    status `success`, and it carries **81** fix-list entries. The live page itself
    renders 81. Two independent controls agree.

    **What I did wrong, both times: I read a record instead of taking a reading.**
    STATE said "deployed `a97b8b0` = 79 entries", true when written on 08-21, and
    I repeated it twice as current without checking. The deployments API answers
    it in one call and I only ran it while writing the audit prompt — which is
    precisely why that prompt now opens with it as §1.

    ⇒ **item 79 is DONE** (see below), and nothing is owed on either store.

### ✅ 2026-08-24 — ITEM 79 IS DONE. You ran it on 08-24 and again on 08-28; verified 2026-08-29 against the deployments API. The original text is kept below as the record.

79. ✅ **DONE — deployed `7f4bb78`, status `success`, 2026-08-28T22:25:18Z, carrying
    81 fix-list entries.** The gap this item was written against is closed. ⚠️ One
    later commit (`fcb2aa9`) is still undeployed — that is item 81, not this.

    <details><summary>The original item, kept for the record</summary>

    ⚠️ **Run *Actions → Publish docs site → Run workflow* on `SMR-CommunityMods`.**
    Everything is committed and pushed; **none of it is public.** The publish
    workflow is `workflow_dispatch`-only **on purpose** — publishing is your act,
    public-docs chain rule 5 — so the F105 entry has been sitting live-invisible
    since it was written.

    | | commit | fix-list entries |
    |---|---|---|
    | **what players see now** | `a97b8b0` (deployed 08-21) | **79** |
    | what the repo holds | `abe46c9` | **80** |

    Counted from the deployed commit locally, not off the web page.

    ⛔ **Why the order matters:** the store cards say **"Eighty repairs"**, and the
    only reason we allow a count on a store page at all is that the reader can
    check it on the page the card links to. Paste the cards first and the very
    first person who counts finds seventy-nine. **Deploy, then paste.**

    ✅ Nothing else about the site is owed — Pages is on, the store links are in
    the pages, the card carries the site links, and no FILL-IN markers remain.
    This is one button, and it costs you about a minute.

    </details>

### ⛔ 2026-08-24 — ITEM 78 IS WITHDRAWN. I asked you to decide something you had already done, on a tool reading that was wrong. Both reporters are answered. Nothing is owed.

78. ⛔ **WITHDRAWN — the finding was false and the fault was mine.** I reported
    that issue #1 was closed with **zero comments** and that Keelai had been left
    without any answer, and asked you to choose between reopening, commenting, or
    leaving it silent. **None of that was real.** You had already posted the reply
    and closed it, and Keelai had already thanked you.

    **What actually happened**, from the API, which I should have used first:

    | issue | what is on the thread | reporter's last word |
    |---|---|---|
    | **#1** F104 | Draft A posted 03:40Z; closed 06:01Z `completed` | *"Yeah i had a hunch that mod might be the problem but thanks for checking :)"* |
    | **#2** F105 | you asked for the save/store at 01:57Z, then posted a full explanation at 06:04Z | *"Nice and thanks :) ill try and include both save and log in the future"* |

    **The mistake, plainly:** I read the issue's web page instead of the API. It
    returned "no comments" three times — including once with a cache-busting URL
    — and I treated three agreeing reads as confirmation when they were the same
    broken method three times. The comment **count** was one field away in the
    issues list and would have caught it instantly. That control is now written
    into `agent/prompts/perma/PUBLIC_SURFACE_SWEEP.md` §4 and the reply record, and
    `F104` carries the correction in its own entry rather than quietly reading
    right.

    ✅ **F104 is now `closed`** — its stated gate was a reply *plus* the
    reporter's confirmation, and both are on the thread.

    ⭐ **Two things genuinely came out of this, and they are the only parts worth
    your attention.** Your #2 reply was written hours *before* the rig legs ran,
    so four of its sentences are stronger than what we can now back. The reporter
    is satisfied and **nothing needs correcting on the thread** — but these must
    not migrate onto the fix list, a store card or `last_changes`, where there is
    no goodwill to spend and no thread to correct them in:

    * ⛔ *"it also **repairs saves** that already have a levelling job in the
      broken state"* — we don't repair; the site stays broken and the guard makes
      it harmless. The outcome you promised is right and leg D proves it (nothing
      to demolish); the mechanism isn't. Wording that holds: **"stops it happening
      on a save it's already happening in."**
    * ⚠️ *"**only three** technologies carry the effect"* — true of the label
      sweep; a second reader route (`OnMsg.ConstructionCostChanged`) was never
      ruled out. The guard covers both, so the fix claim is fine — it's the
      *"only"* that's wider than the evidence.
    * ⚠️ *"quietly to the log with **no warning box**"* — we measured `Mod
      Flagged` = 0 with the pack off, which supports it; nobody ever *watched* a
      screen to confirm the box is absent.
    * ⚠️ *"happens with **no mods installed at all**"* — derived at source, and
      every pack-off leg still had the rig's other junctions loaded.

    **Nothing here needs an answer from you.** If you want one thing when 1.0.x
    goes live, a one-line *"this is out now"* on #2 would close it warmly — pure
    courtesy, not a debt.

### ✅ 2026-08-24 — RULED AND APPLIED. The hazard is reworded; nothing blocks the update but your sitting.
<!-- ck:- status:ruled owner:no -->

Body archived in [archive/PLAYTEST_ARCHIVE.md](archive/PLAYTEST_ARCHIVE.md); search `ck-` and this heading.

### ⭐⭐ 2026-08-24 — F105 IS FIXED ON YOUR WORD, AND BUILDING IT EXPOSED A NEW QUESTION. One receipt, one call.
<!-- ck:- status:closed owner:no -->

Body archived in [archive/PLAYTEST_ARCHIVE.md](archive/PLAYTEST_ARCHIVE.md); search `ck-` and this heading.

### ⭐⭐⭐ 2026-08-24 — F105 IS REPRODUCED ON OUR OWN RIG, AND THE FIX WAS WATCHED TO STOP IT. Nothing is owed; this is a receipt.
<!-- ck:- status:closed owner:no -->

Body archived in [archive/PLAYTEST_ARCHIVE.md](archive/PLAYTEST_ARCHIVE.md); search `ck-` and this heading.

### ✅ 2026-08-24 — F107 IS REPAIRED. **76 CLOSED 09-12 as overtaken — the module was deleted by `2dc1dbe`, so there is nothing left to revert. Nothing is owed from you.**
<!-- ck:76 status:closed owner:no -->

76. ✅ **BUILT on your item-74 (a), same session — `Fix_LandscapeCostRefresh`
    now installs ONE chained wrap on `ConstructionSite` instead of three on the
    landscape leaves.** `prev` is the real function (`ConstructionSite` is the
    only class in the tree that declares `RefreshConstructionResources`,
    `ConstructionSite.lua:665`), so the delegation half is live code again.
    → [agent/bugs/F107.md](agent/bugs/F107.md) (`built`) · `Code/Fix_LandscapeCostRefresh.lua`
    * **The `Require` block already named the pair we now install on**, which is
      what `FIX_POLICY` §2 asks for — so the three F107 rows are **deleted** from
      `tools/harvest_wrap_targets.py`'s allowlist rather than kept. `WRAP CHECK:
      0 wrap site(s) outside Require, 5 allowlisted`. doccheck **GREEN**.
    * **The widening was re-verified at Src by this session, independently**, not
      taken on the audit's word: `GatherConstructionResources` creates
      `construction_resources` and `construction_costs_at_start` together
      (`:639-640`), both class defaults are `false` (`:13`, `:32`), so the only
      ordinary-site state where the widened guard fires is the ungathered one —
      where vanilla's own body raises at `:670`. Same verdict: it can only ever
      prevent an error. That derivation is now in the module header.
    * **The header's refuted F106 premise and the banned `classes.lua:986-988`
      citation are gone**, replaced by the measured file-load ordering; the
      `Track.lua:651` "only writer" precision is in too.
    ✅ **VERIFIED ON THE RIG 2026-08-24, unattended — F107 is `fixed`, not
    `built`.** You launched; the TestKit autorun harness did the rest (boot ->
    generate a map -> start a colony -> all 100 probes -> quit itself). Log
    `docs/archive/f107_Mars.exe-20260824-13.07.00.log`.
    * **Suite `76 PASS / 0 FAIL / 24 SKIP / 0 ERROR` of 100**, gate `78/78
      applied`, `[SMRAUTO] BEGIN..END` clean. The previous leg was `75/1/24/0`
      and that single FAIL was this probe.
    * ⭐ **Clause 1 stayed PASS on all three leaves** — that is the half that
      mattered. A repair that traded one defect for another would show clause 1
      broken, and nothing else in the suite checks it.
    * ⭐ **The dispatch sweep agreed independently of the probe**: the three
      leaves went from `UNREACHED=3 (own-copy 3)` — unreached because the module
      had overwritten them itself — to `UNREACHED=0`, reach 5 -> 8. Sweep total
      `clean=97` -> **`98`**. That is the inheritance mechanism measured without
      reference to the probe's verdict.
    * ⭐ **The widening you ruled in is no longer a reading.** Clause 3 ran on
      `ConstructionSite` itself: ungathered `ok=true` (where vanilla raises at
      `:670`), gathered `ok=true set_to=90 start_cost=50` (delegated identically
      to vanilla). Two static derivations had agreed on that; now it has run.
    * **Zero unexplained error lines.** The `Flight.lua:465/:479` asserts in the
      log are the known synthetic-map ones, present in the control leg too.
    ⛔ **Still NOT established, and no run so far touches it:** the field route —
    a levelling site on a real map plus a `*_Construction` cost tech. F105 has
    never been reproduced end to end. That is unchanged by this leg and rides
    your next organic sitting if you want it.
    ❓ **One thing still open: I read your "I'd take (a)" as the ruling and
    built it.** If that was a leaning rather than a decision, say so — it is one
    `git revert`, though the tree is now measured green on it.
    ✅ **CLOSED 2026-09-12 as overtaken — there is nothing left to revert.** On
    your "if it's overtaken close it". `Code/Fix_LandscapeCostRefresh.lua` was
    **deleted** by `2dc1dbe` (hotfix 2 link 02, 2026-09-08) under the item-98
    DELETE ruling — verified in that commit's own name-status (`D
    Code/Fix_LandscapeCostRefresh.lua`) and by the file's absence from `Code/`
    today. Whether the item-74 (a) build was a ruling or a leaning no longer
    changes any byte we ship.

74. ✅ **MEASURED AND ANSWERED 2026-08-24 — and the answer is the opposite of
    the question. It cost you nothing: the run was unattended.**
    **The good news first: nothing was broken by the mechanism I was worried
    about.** I filed F106 saying that most of our ~60 fixes might be silent
    no-ops, because the game copies inherited methods into each subclass before
    our code could patch them. **That was wrong, and it is now measured wrong.**
    Our fixes are applied *earlier* in the boot than I believed — before the game
    builds its classes, not after — so the game copies **our** patched version
    down into every subclass. `Fix_SmallLandscapeSites` (F33) is fine and always
    was; the sweep checked all **105** wrap targets and 97 of them reach every
    subclass. → [agent/bugs/F106.md](agent/bugs/F106.md) (closed, refuted) ·
    report [agent/reports/F106_DISPATCH_SWEEP.md](agent/reports/F106_DISPATCH_SWEEP.md)
    · log `agent`-side `docs/archive/f106_Mars.exe-20260824-02.32.27.log`
    · suite `75 PASS / 1 FAIL / 24 SKIP / 0 ERROR` of 100, gate `78/78 applied`.

    ⛔ **The bad news, and the only thing here that needs you: the same run found
    a real defect in the F105 module you ruled on yesterday.**
    `Fix_LandscapeCostRefresh` was written to "check, then hand off to the
    game's own code". Because of the same early-apply timing, the hand-off
    captured **nothing** — it holds a nil where the game's function should be. In
    practice: **the crash you asked me to fix IS fixed** (the check fires and
    returns, which is the whole repair), but the hand-off half is dead code that
    would throw an error *inside our own file* if anything ever reached it.
    Nothing shipped is affected — this module is not on the live listings yet —
    but it is **the one module the queued 1.0.x upload exists to deliver**.
    → [agent/bugs/F107.md](agent/bugs/F107.md) (measured, not derived)

    ❓ **Your call — one question, three options.**
    * **(a) Repair it before the upload** *(my recommendation)*. The repair is
      small and, ironically, it is the shape **you** were originally offered on
      item 72: **one wrap on `ConstructionSite`** instead of three on the leaf
      classes. It is now measured to reach all 13 relevant classes. One module
      touched, one boot log to confirm, then the upload goes as planned.
      ⚠️ It widens the guard to ordinary construction sites too — harmless by
      construction, but it is a behaviour surface and that is why I am asking
      rather than deciding. (Audit-checked 08-24: in the one state where the
      widened guard changes anything, the game's own code would have crashed —
      so the widening can only ever prevent an error, never cause one.)
    * **(b) Upload as-is, repair in the next patch.** Defensible: the reported
      crash really is fixed and the dead branch is unreachable on shipped data.
      The cost is that the pack carries a latent error in its own file, and
      `EF-065`(a) means any such error names **us** in the player's popup — the
      exact misattribution F104 and F105 were both about.
    * **(c) Repair it with the minimal change** — keep the three installs, just
      take the game's function from the class that actually declares it. Smallest
      diff, no behaviour-surface change, but it leaves the shape that caused the
      bug in place.
    ✅ **RULED (a) and BUILT 2026-08-24 — receipt is item 76 above.**
    ⛔ (Historic:) the chain that found it was forbidden from writing fix code,
    deliberately, so that the finding and the fix stayed separate decisions.

    ⚠️ **One thing this run canNOT tell you, and no run so far can.** The sweep
    lists which subclasses do not receive one of our patches; it does **not**
    say which of those subclasses ever actually exist in a game. So the "audit"
    half of this item is **not complete and is not closed** — what is closed is
    the alarm that the mechanism was breaking everything.
    For the record, the leftovers it did find are the *old* known question
    (`EF-066`): 8 targets where a subclass writes its own version of the method
    we patched, so it keeps the game's behaviour instead of ours. That is
    under-coverage, never new harm. The largest is
    `Fix_ShuttleHubOffAvailable`, whose wrap on `BaseBuilding` is overridden by
    `Building` and so misses ~578 building classes; also
    `Fix_GhostFarmOxygen`'s wrap misses residences, research labs, training
    buildings and water reclamation spires. **None of these is new, none is a
    regression, and none needs you now** — they are per-fix coverage questions
    for the opt-in-era maintenance window, exactly where `EF-066` always put
    them.

### ⭐⭐ 2026-08-23 — THE FIRST FIELD REPORTS ARRIVED. Two GitHub issues, one reporter, and the pack was named in both. Neither error was ours. **73 CLOSED 09-12: not worth further resources.**
<!-- ck:73 status:closed owner:no -->

72. ✅ **RULED 2026-08-24, in-session ("number 1 fix priority") — BUILT AND
    BOOT-VERIFIED the same day; receipt in the 2026-08-24 section above.**
    ⚠️ Kept as filed for the record; note the recommendation's mechanism was
    "corrected" during the build — the single reader wrap was believed unable to
    reach the landscape classes (F106), so the fix installs per leaf class.
    ⛔ 08-24: that belief was measured WRONG (F106 refuted, item 74) — the
    single wrap you were originally offered would have worked, and the per-leaf
    shape it was traded for carries F107.
    **F105 — do we fix the landscaping crash, or leave it?**
    A real vanilla defect, no mod needed: a terrain-levelling site never
    initialises `construction_costs_at_start`, so researching any tech that
    carries a `*_Construction` cost modifier throws. Squarely in charter, and the
    reporter hit it. ⛔ **We have never reproduced it** — everything we know comes
    from reading the shipped Lua against their log.
    → [agent/bugs/F105.md](agent/bugs/F105.md)
    **Two shapes, both small.** (a) guard the reader — skip the refresh when
    `construction_costs_at_start` is not a table; covers every subclass with the
    same gap. (b) initialise the writer — narrower, only fixes what we enumerate.
    **Recommendation: (a).**
    ⛔ **Price it post-release, not with the gate** (your 08-20 ruling, item 57):
    an `items.lua` entry, one boot `applied` line, doccheck counts. Nothing else.
    **What I'd want before building it:** a rig repro. Place a levelling site,
    research a dome-cost tech, watch for `ConstructionSite.lua:673`. ~10 minutes.
    ❓ **Your call:** build it now, build it after a repro, or leave it filed.

73. ✅ **CLOSED 2026-09-12 — "lets just close it". Not worth further resources.**
    ⭐ **It also closes item 133 sub-decision (5), the breadcrumb** — recorded 2026-09-12 alongside the
    "do the reword" ruling, because (5) is the same ~15 lines as tier 0 here. See 133 for the tension
    that reading resolves. Your words:
    *"we have spent more resources looking for a fix for something that has only come up once."*
    No tier is taken, and the four options below stay on the record as the reasoning, not as work
    owed. **What was learned, so nobody re-opens this blind:**

    * **The mechanism is understood and it is not going to get better.** The engine attributes a
      crash by asking whether a mod's folder name appears in the error text or the stack
      (`Mod.lua:3001-3013`); its own comment calls that a *"rough estimation"*. Nothing we do to
      our own code changes how that question is asked.
    * **Both field sightings were pass-through frames, and neither was our defect** — F104 and
      F105. Two sightings, one reporter, one day, and the rate since has been zero.
    * **The surface already shrank about 40% for free** when hotfix 2 (`2dc1dbe`) deleted 36
      modules. The cheapest tier was overtaken by ordinary work.
    * **Tier 1 lost its only measured candidate**: `Fix_MilestoneCrash`, the module the whole
      "patch leaves, not ancestors" argument was built on, is one of the 36 deletions.
    * **Tier 3 would put us on the error path for every mod in the process** — wrapping the global
      `ReportModLuaError` means our code runs when anyone else's mod throws. That is a large,
      permanent liability bought for a symptom seen twice.
    * **The "cheap popup recipe" is dead** — the two modules it relied on to raise the engine's
      *Mod Flagged* box on demand were deleted by the same commit, so it cannot be run as
      written. ⚠️ Recorded from your ruling: the recipe itself is not written down anywhere in
      this tree, so anyone who wants it again has to re-derive it from `EF-065`.

    ⚠️ **Link, flagged and NOT decided here: item 133 sub-decision 5 (the log breadcrumb) is the
    same ~15 lines as tier 0 above.** Closing 73 implies it, but **133 is still open and you have
    not ruled it** — so it stays open. Whoever takes 133 should read this closure first; if you
    say yes to 133(5), that is the breadcrumb and tier 0 arrives with it.

    ✅ **RESOLVED 2026-09-12 — the owner was asked directly (checklist 162 (d)) and confirmed that
    closing 73 closes **133 (5)**, the log breadcrumb. It is not built.** The paragraph above and the
    one before it are left as the record of how the two readings arose; ⛔ **the disagreement itself is
    settled and must not be re-derived** — it was flagged in two records and asked in neither until 162 (d).
    ⚖️ **Closed under a named condition** (rule 5a, `agent/WORKFLOW.md:60`): the rate is effectively zero
    — two sightings, one reporter, one day, nothing since, and neither error was ours. **More false-blame
    reports reopen it**, and the case changes then: the breadcrumb would be producing evidence in the
    *player's* log rather than saving an agent the derivation, which is already written down.

    *(The original finding is kept below.)*

    **The bigger one — we get blamed for other mods' crashes, and it will keep
    happening.** The engine decides which mod to flag by asking "does this mod's
    folder name appear anywhere in the crash text" (`Mod.lua:3001-3013`, its own
    comment calls it a "rough estimation"). We wrap ~60 game functions, so any
    error thrown *underneath* one of them names us. **Two sightings in one day,
    neither our defect.** The mod that actually caused F104 can never be named,
    because its function had already returned when the error happened.
    → [agent/facts/EF-065.md](agent/facts/EF-065.md) · F104 · F105
    **Four options, cheapest first — these are not exclusive:**
    * **(0) Log breadcrumb.** One handler that logs "the throw site is not a pack
      file". Costs nothing, accuses nobody, saves the next reader a whole session
      of derivation. *I'd do this regardless.*
    * **(1) Shrink the blame surface.** Patch leaves, not ancestors.
      `Fix_MilestoneCrash` replaces `CompleteMilestone`, which sits above the
      entire milestone→research→every-construction-site fan-out — that is exactly
      why F105 named us. Patching `Milestone:GetScore` instead does the same
      repair with almost nothing running underneath. **I checked every other
      caller: zero ripple** (`Challenges.lua:58` guards `if cs then`, and `0` is
      truthy). It also deletes a 40-line verbatim copy of vanilla that could drift
      on a game patch. *Strictly better code; my first pick.*
    * **(2) Trampoline.** Route call-throughs via a separately-loaded chunk so our
      file genuinely isn't on the stack while vanilla runs. Needs two boot
      measurements first (is `load` reachable from mod code; does a custom chunk
      name reach the traceback). Only for hooks that don't rewrite arguments.
    * **(3) Own the wording.** Wrap the global `ReportModLuaError`, pass every
      other mod through untouched, and for our id alone show **our own** message
      when the throw site isn't ours: "the pack appears in a crash raised in
      `<file>`, which is not part of the pack — please send the log." **Not
      suppression** — the player is still told, and told something true.
    * ⛔ **Rejected, on the record:** `config.DisableErrorReporting` (silences
      *every* mod, including other authors'), and pre-setting `ReportedMods`
      (silences us wholesale, before any error exists). Both are the blanket
      suppression you said to avoid.
    ❓ **Your call:** which tiers, and whether (2)/(3) touching engine internals
    for self-defence is inside `FIX_POLICY` at all. That last part is a policy
    question, not an engineering one, which is why it is here.

    ℹ️ **Ruling already taken and applied (2026-08-23, yours):** we DO name the
    other mod when answering a reporter. Stating the cause plainly is not
    slander, and shielding an unmaintained mod is not our job. `FIX_POLICY` §8
    still binds for *store pages and load-order advice* — this ruling covers
    issue replies. Worth folding into §8 explicitly on its next edit.

    ⚠️ **doccheck, copied verbatim:** `STATE.md is 9505 bytes, warn threshold is
    9216 — copy this line VERBATIM into the owner report; the owner fires
    agent/prompts/perma/STATE_EVICTION.md`

### ⭐⭐⭐ 2026-08-20 — IT IS PUBLISHED, ON BOTH PORTALS. The ids are committed. One number came out differently on each store, and that was mechanical, not a mistake.
<!-- ck:- status:closed owner:no -->

Body archived in [archive/PLAYTEST_ARCHIVE.md](archive/PLAYTEST_ARCHIVE.md); search `ck-` and this heading.

### ⭐⭐ 2026-08-20 — THE AUDIT IS DONE. VERDICT: SHIP. The repo's active work ends here; the upload sitting is yours whenever you want it.

66. ⭐⭐ **SHIP.** Both fixes go in 1.0.0; the tag is moved onto this ruling's
    commit and now stands on **your attended sitting** (plus your one-time
    release-gate ruling, item 57) — not on run B, which two new modules
    outdated. I found **no launch blocker**. What I tried to break, and what
    happened:

    | challenge | what I did | result |
    |---|---|---|
    | the C50 regression warning | re-read the module: `preset.effect` is only ever **read** (one line), never written; your row-4 reading — first bullet **(40,000)** intact on both screens — is the screen proof | ✅ holds |
    | evidence provenance | traced every `tested-attended` word to who/screen/language/log; C51's claim rests on the **German** readings, never the English pass | ✅ holds |
    | module-list gate (tools/doccheck.py MODULE SETS + tools/upload_preflight.py) (ships absent) | compared `items.lua`, metadata's `code` list and disk **myself**: 78 = 78 = 78, identical order, both new modules present; `pack_predict` **82** | ✅ holds |
    | frozen things | `version` still `0` · `C52` still `parked` · no opt-in passage restored · no player surface names the other mod · **nothing published** (no portal line in any log) | ✅ holds |
    | the sitting's own wrong turn | re-derived the rocket-subclass story **from the engine's class builder at Src** — the report's marked correction is right, and the suite message *"a later mod has chained on top of ours"* is provably wrong about the cause (it's the engine composing `Init`; no later mod exists). Recorded as fact `EF-066` | ✅ report honest |

    ⚠️ **Named, not blockers:** the challenge landing-spot screen and the
    SpaceY in-game Goals panel remain unobserved (your item 59/63 skips); the
    English rocket-rollover reading predates the mid-sitting repair, so
    "English players see no change" on the final build rests on the measured
    language data, not a screen — the mechanism makes it byte-identical.

    ⭐ **The question this chain never asked (my C5):** the pack wraps ~60
    class methods, and **nobody has ever checked which of them have subclasses
    that override the wrapped method** — a subclass that does keeps vanilla,
    fix and all. C51's rocket half is the only place that question ever
    surfaced, and it cost that fix its whole working life until your tracer
    caught it. The safe part: a missed subclass means *the bug stays vanilla
    there*, never new harm. It's recorded in `EF-066` as opt-in-era
    maintenance, not a launch item.

    ⚖️ **Was five prompts for two text fixes worth it? Yes — narrowly, and
    not for the reason planned.** The builds alone didn't need a chain. But
    link 4's prep caught C50 printing a wrong number on a screen no record
    had ever named, and the sitting caught C51's rocket half having never
    worked at all. Both would have shipped broken under "just build and
    upload." The chain's cost was mostly the two build links; its value was
    the two catches. A future two-fix change should be a **two-link** chain:
    build, then attended-test-plus-audit in one.

    ⚠️ Housekeeping line, emitted after my edits and copied verbatim as it
    requires: **`warn STATE.md is 9941 bytes, warn threshold is 9216 — copy
    this line VERBATIM into the owner report; the owner fires
    agent/prompts/perma/STATE_EVICTION.md`** — fire the eviction prompt whenever
    convenient; nothing about the upload waits on it.

67. ⭐⭐ **Your upload sitting, restated — nothing else stands between you and
    the release:**

    1. **Re-tick the mods** in the Mod Manager (the junction pull cost the
       enables; restart after ticking).
    2. ⛔ Before anything is pressed: **not dirty, and `1.0.0` on screen.**
       ⇒ see item **70** for the exact command and what each answer means —
       ⚠️ **`nil` is a PASS**, and the sheet used to imply it was not.
    3. Pack via **Mods Manager → Edit (`Ctrl-E`) → File → Pack Mod** — ⛔ no
       console route exists. Expect **82 files**; a different count means
       stop, not adjust. Record the md5/bytes in §0.5(f)'s blank row **at
       pack time**.
    4. ⛔ **Paradox Mods FIRST**, Steam second.
    5. Then the sheet's §0.5(d) — game version **350453** on the portal page;
       §0.5(e) — the id-writeback commit; §0.5(f) — md5 your downloaded pack
       **against the row you filled in at step 3**.

70. ⛔ **The dirty check, exactly — asked 2026-08-20, and the sheet's expected
    value was wrong in the same way the version digit was wrong on 08-19.**

    **The command, in the in-game console (Enter, in a loaded colony):**

    ```
    print(Mods.SMR_CommunityFixPack.version, Mods.SMR_CommunityFixPack:IsDirty())
    ```

    **How to read the two values:**

    | value | meaning |
    |---|---|
    | first — `0` | ✅ **1.0.0**, which is what you ruled. ⛔ A `1` means the version already moved — **stop.** |
    | second — `nil` | ✅ **PASS.** Nothing has dirtied it, and the mod has not been opened in the Mod Editor this session. |
    | second — `false` | ✅ **PASS.** Opened and hashed, unchanged. |
    | second — `true` | ⛔ **STOP.** The upload would force a save and bump you to 1.0.1. |

    ⚠️ **Why `nil` had to be spelled out.** `IsDirty` is
    `return old_hash and (old_hash == 0 or old_hash ~= data.current_hash)`
    (`CommonLua/GedEditedObject.lua:93-98`, read at Src 08-20). If `old_hash` is
    unset — which it is until the mod is opened in the editor — the whole
    expression is **`nil`**, not `false`. The **only** archived reading this
    project has, act 1 on 08-19, is exactly that: `dirty: nil`
    (`archive/act1_Mars.exe-…15.18.19…:258`). ⛔ The sheet said *"must be
    `false`"*, so a correct `nil` would have read as a failure and stalled you —
    the same shape of error as the `1`/`0` inversion corrected on 08-19.
    ℹ️ Item 44's step 1 said *"the 08-19 console read returned `0 false`"*; no
    archived log contains that string, and the reading it cites shows `nil`.
    Corrected there too.

    ⭐ **The check that matters more, and it needs no console at all.** Whatever
    the console says, the real guard is the editor's own behaviour: **if the Mod
    Editor prompts *"The mod needs to be saved before uploading"*, STOP** — that
    prompt IS the forced save (`ValidateModBeforeUpload`,
    `GedModEditor.lua:836-844`), and it is the thing that would bump the version
    inside the package. The console read is the early warning; the prompt is the
    tripwire.

69. ⭐ **What to fire, and when — asked 2026-08-20 after the eviction.**

    ⛔ **For the upload itself: nothing.** No agent can publish, so there is no
    prompt to run. It is you, item **67**'s five steps, and
    `reports/RELEASE_PORTAL_PREP.md` §0.5 open beside you.

    ✅ **After the listing exists, fire
    `docs/agent/prompts/perma/POST_UPLOAD_CLOSE.md`** — written 08-20 for exactly that
    moment. It exists because the writeback is not a copy-paste: the forced save
    that writes `pdx_id`/`steam_id` into `metadata.lua` also **regenerates that
    file from memory and strips every hand-written comment in it**, so the ids
    have to be committed *and* the prose restored in the same commit. It also
    ⛔ forbids the tempting mistake of "correcting" `version` back to 0 — after
    Paradox the tree sits at `1` by design, and normalising it would lie about
    what is published.

    ⚠️ **Nothing else is owed by that prompt** — it does the three sheet checks
    (§0.5(d) game version, (f) delivered bytes), closes STATE and the records,
    and hands off to the opt-in. It routes **37 Q2** (Steam's number) back to you
    rather than deciding it, because that call is only decidable once Paradox is
    done.

68. ⭐ **The opt-in effort starts on your word** — your stated next priority
    (*"shift resources and start working on the opt in"*). Its first session
    must read **that repo's own STATE** and its standing pre-upload
    obligation: `reports/PARKED_OPTIN_REFERENCES.md` (~46 parked passages
    that restore only when the opt-in pack launches). I have deliberately not
    scoped it further — that's its own repo's job.

### ✅✅ 2026-08-20 — YOUR SITTING IS DONE AND BOTH FIXES WORK. Nothing here is owed from you; this is the receipt.

63. ⭐⭐ **You saw both fixes working, in two languages.** Every reading passed:

    | what you looked at | what it said |
    |---|---|
    | SpaceY rollover + summary, English | the new bullet, **(40)** — the number I predicted before you launched |
    | SpaceY rollover + summary, German | **Maximale Anzahl an Drohnen, die ein Drohnen-Hub kontrollieren kann (40)** |
    | SpaceY's first bullet, both | **(40,000)** cargo intact — the regression that mattered most didn't happen |
    | terraforming heading, English | no visible change — exactly what the site page promises |
    | terraforming heading, German | **TERRAFORMING-GESAMTFORTSCHRITT** |
    | Back to Earth rollover, German | **Zurück zur Erde** |
    | the suite | **74 PASS · 0 FAIL · 24 SKIP · 0 ERROR** of 98 |

    ⭐⭐ **The single most valuable thing you did:** the German heading. In vanilla
    that text is a raw code string with no translation attached at all — there is
    no way it becomes German by itself. It is German *because of our fix*. That
    also closes a question this project has carried since **2 August**: nobody had
    ever watched one of these repairs render in another language. Now we have,
    twice.

    ⚠️ **The suite's 24 skips are all "another mod isn't loaded"** — 8 opt-in, 6
    save-rescue, 8 retail sandbox, 2 odds and ends. **0 failures, 0 errors.** Your
    store card's "98 checks" is now a measured number instead of a claim (item 60,
    closed).

    ⛔ **Two things nobody looked at, named rather than counted as passes:** the
    challenge landing-spot screen, and the in-game Mission Profile on a SpaceY
    colony. Both are the same code seen working elsewhere; neither is a launch
    item.

64. ⚖️ **Two code changes happened while you sat there, and you should know what
    they were.**

    - **`C50`** — the double-count you ruled on (item 61). Built, and confirmed by
      both the console and the suite: the in-game panel now shows vanilla.
    - **`C51`'s rocket half was a no-op as shipped-in-progress.** It had *never*
      worked, in any session. It searched for the Back to Earth button in the
      wrong place. It now uses the engine's own lookup, and you watched the result
      in German.

    ⛔⛔ **And one thing I got badly wrong, which you should hear plainly.** I
    talked myself into a theory that rocket subclasses don't inherit the fix,
    built a change for it, and when that change looked like it failed I
    **recommended cutting the rocket half from 1.0.0**. Your very next screenshot
    showed it working. A good fix was one message away from being deleted on my
    bad inference.

    ⭐ **What saved it was your question** — *"why can't you detect it when I press
    the button and trace it back?"* That tracer answered in one shot what three
    rounds of me reading source got wrong. Recorded in the report as the method
    lesson, because it is one.

65. ⚠️ **Two small things for the record, neither needing anything from you.**

    - **The `[LUA ERROR]` in your logs is mine, not the pack's.** My console
      tracer used a function the mod sandbox doesn't have. It was contained, and
      it's flagged in the report so the audit doesn't misread it.
    - **Your autosaves are intact** — `Sol 406` and `Sol 411`, byte-identical to
      the copies I took before the first launch, reconciled by name. `C47FARM`
      untouched.

    ⭐⭐ **Next: `docs/agent/prompts/closeout-1.0.0/05_AUDIT_fable.md` — the last
    link.** It reviews everything adversarially, moves the release tag, and rules
    ship-or-revert. **It does not need you.** After it, the upload sitting is
    yours whenever you want it.

### ⛔⛔ 2026-08-20 — the sitting's prep found a real defect in `C50` (RULED: fix it). Kept as the record of the call.

61. ⛔⛔ **The thing I found, and it needs your word before the sitting.** `C50`
    was recorded — twice now, and by me — as touching **pre-game screens only**.
    While writing your script I traced the panel it patches and **it is also an
    in-game screen**, and on that screen **the number it prints is wrong**.

    **What is actually true.** The pre-game mission summary panel is not built in
    one place. The game builds the same panel again for the **in-game Mission
    Profile dialog — the Goals button on your HUD**. Both go through the exact
    function `C50` wraps. So the bullet appears in a running game too, which
    nobody intended and nothing recorded.

    ⛔ **And in a running game the arithmetic double-counts.** The base Drone Hub
    capacity is **20**. SpaceY adds **+20**. Pre-game that gives the right answer,
    **40**. But once a colony exists, the game has *already* applied SpaceY's +20
    to the live value — so the fix reads 40, adds 20 again, and prints **60**.
    The real cap is 40. ⚠️ **The safety check inside the fix cannot catch this**:
    it only asks "is the number bigger than the baseline", and 60 is bigger than
    40, so it passes happily.

    ⚖️ **How much does it matter?** Honestly: **little, but it is wrong.** You
    only ever see it if you play **SpaceY** *and* open the Goals/Mission Profile
    panel mid-game. It changes no save, breaks nothing, and every pre-game screen
    — the three the sitting is actually about — shows the correct **40**.
    ⛔ But it is a wrong number that we introduced, on a screen a player can
    reach, and the site's fix page already promises this fix is a plain repair.

    ⭐⭐ **My recommendation: fix it, and it is about six lines.** Have the fix
    **stand down when a game is running** — the bullet then appears on the
    pre-game sponsor screens exactly as designed, and the in-game Goals panel
    goes back to showing vanilla. That matches what the module already says about
    itself ("it is pre-game UI text"), it is the smallest possible change, and
    the sitting can confirm it by opening the Goals panel and seeing no bullet.

    ⚖️ **Your options:**

    | | what happens |
    |---|---|
    | **A — fix it now (recommended)** | ~6 lines + a corrected header. Adds maybe 10 minutes before your sitting, and the sitting then checks it for free (open Goals, expect no bullet). |
    | **B — ship it as-is, file the defect** | `C50` ships with a wrong number on one in-game panel for SpaceY players. Recorded as a known defect for the opt-in effort. Costs you nothing today. |
    | **C — pull `C50` out of 1.0.0** | `C51` ships alone. ⛔ Its site fix-list entry has to come out too. I do **not** recommend this — the defect is small and the pre-game repair is sound. |

    ⚠️ **Note on the fence:** link 4's brief says code changes are out *unless the
    sitting finds a fix broken*. I found this **before** the sitting, from the
    source, not from a screen — so I am asking rather than just doing it.

    ⭐ **Nothing about this blocks you from starting.** If you pick **B**, the
    script below runs unchanged, right now.

62. ⭐ **Your script — about half an hour, one launch, two language settings.**
    Everything is prepared: predictions are written down and committed *before*
    the game opens (`docs/agent/reports/04_ATTENDED_SITTING.md`), and ⚠️ **both
    your autosaves are already byte-copied out of the save directory** (`Sol 406`
    and `Sol 411`, `EF-056`) — reconcile them by name when you are done.

    ✅ **Save: `C47FARM`** — your word, 2026-08-20. Two of the readings need it
    loaded, with a **Universal Rocket sitting idle on Mars** and the **planetary
    view** available.

    ⚖️ **Item 61 is RULED and BUILT.** You chose the fix; it is in, it parses,
    doccheck is GREEN and `upload_preflight` still reads 0 FAIL with 78 entries in
    order. Step ② below carries the one check that confirms it.

    **① English, pre-game — the two free `C50` looks.**
    New game → sponsor selection → **SpaceY**.
    - ✅ Expect the summary panel's SpaceY description to carry a **new fourth
      bullet: *"Maximum number of Drones a Drone Hub can control (40)"*.**
      ⭐ **The number should be 40.** (The brief's example said 100 — that was an
      illustration, not the real value.)
    - ✅ Now **hover SpaceY in the sponsor list** — the rollover is a second,
      independent look at the same repair. Same bullet, same 40.
    - ⛔ **Read the FIRST bullet both times too:** *"Dragon Rocket - has smaller
      cargo capacity **(a number)** but is faster and requires less fuel."* If
      that number is gone, or you see raw `<cargo>`, **stop and tell me** — that
      is the failure the whole design was built to avoid.
    - ⛔ If you see literal `<drone_cap_help>`, `<CommandCenterMaxDrones>`, a
      `{#4706}` token, or an empty `()` — **tell me exactly what the screen says,
      word for word.** Do not summarise it.

    **② English, in-game — the `C51` "nothing changed" reading.**
    Load the save → open the **planetary view** (the Mars/planet button) → then
    select your idle **Universal Rocket** and hover its **Back to Earth** button.
    - ✅ Expect **no visible difference at all**, on both. That *is* the reading —
      the site page promises English players see nothing change, and this is the
      step that checks exactly that.
    - ⚠️ **If the Back to Earth button is not on the rocket's panel**, the rocket
      is busy. It only shows on a Universal Rocket that is **idle with no
      destination set** (not loading, not launching, not an asteroid Lander).
      Cancel its flight and it comes back.
    - ⭐ **And the 20-second check on the defect you just ruled** (item 61 — it is
      built, parse-clean, and in). ⚠️ **Do not just look at the Goals panel** — I
      wrote that first and it was wrong: `c47farm` is not a SpaceY colony, so the
      panel would look identical whether or not the repair works. Paste this
      instead, anywhere in the loaded game:

      ```
      *r local sp = table.find_value(MissionParams.idMissionSponsor.items, "id", "SpaceY")
         ModLog(tostring(SMRFixPack.SpaceYDroneCapBullet.bullet_for(sp, "probe")))
         ModLog(SMRFixPack.SpaceYDroneCapBullet.stats.probe.reason)
      ```

      ✅ Expect **`nil`** and then a line saying *a game is running…*. Before the
      fix this printed a bullet with the wrong number in it. That is the whole
      proof, and it cannot disturb the three real screens.

    **③ Switch the game language to German. Restart if it asks.**

    **④ German, pre-game — the same two sponsor looks.**
    - ✅ Expect the bullet's sentence **in German**: *"Maximale Anzahl an Drohnen,
      die ein Drohnen-Hub kontrollieren kann (40)"*.

    **⑤ German, in-game — ⭐ the only step that can see `C51` at all.**
    Reload the same save → planetary view → rocket rollover.
    - ✅ Expect the heading as **`TERRAFORMING-GESAMTFORTSCHRITT`** and the rocket
      rollover title as **`Zurück zur Erde`**.
    - ⭐ **This is the first time in this project's history that anyone has watched
      a shipped translation id render in another language.** Whatever it shows,
      it closes a note that has been open since 2026-08-02 — so tell me even if
      it looks boring.

    **⑥ Switch back to English, restart, confirm the screens look normal again.**

    **⑦ Optional, your call (this is item 60):** `*r SMRTest.RunAll()` — a minute
    or two, and it turns the store card's "98 checks" into a measured number.
    ⭐ **Run it if the sitting went smoothly; skip it if you are out of patience.**
    Either way I record which.

    ⚖️ **The challenge landing-spot screen is the one I recommend skipping**
    (your item 59 ruling already allows this). It is the same code on a screen
    you would otherwise never open. If you skip it I record it **by name** as an
    unobserved site, not as a pass.

    ⭐ **When you are done: tell me what you saw in your own words** — I am not
    allowed to write down any screen reading you did not report to me, and I will
    not.

### ⚠️ 2026-08-20 — THE PAGES AND THE RELEASE SHEET ARE CAUGHT UP (link 3 done). One small thing wants your word, and the next link is the one that needs your hands.

60. ⭐ **What moved, in one breath.** The site's fix list now has entries for both
    new fixes; the md5 you were told to checksum your download against is gone and
    replaced with a blank you fill in when you pack; and the counts everywhere now
    read what the emitter says. **Nothing you have to do about any of that.**

    ⛔ **The one number I could not honestly finish.** The store card says *"an
    automated suite of N checks is run against the game with the pack and without
    it."* The suite grew from 96 to **98** when the two new fixes brought a check
    each, so the card now says 98 — **but nobody has run it at 98.** The last real
    A/B measurement is `80/0/16/0` of **96**, from 08-15, and link 4's script
    makes the suite step optional on purpose because you ruled the basic-testing
    bar (item 57).

    ⚖️ **Your call, and it is genuinely small:** at the sitting, `*r
    SMRTest.RunAll()` costs a minute or two and turns the card's 98 into something
    measured — or say the word and it stays a statement about the suite the pack
    ships with, which is what it literally says and is true either way. ⭐ **My
    recommendation: run it if the sitting is going smoothly, skip it if anything
    else is eating the half hour.** The two new fixes are checked by their own
    probes inside it, so it is not wasted either way.

    ⚠️ **A trap I found and defused while sweeping:** the four `smrcf-*` chain
    folders from 08-16 still told a future session to *build* `C50` and `C51`.
    They now carry a banner saying both shipped on 08-20 and that chain B must
    not be run. `C52`'s chain is banner-fenced as frozen too. Nothing was
    deleted — chain A and the jumbo-cave chain are untouched and still owed.

    ⭐⭐ **Next: `docs/agent/prompts/closeout-1.0.0/04_TEST.md` — this is the one
    that needs you, about half an hour, one launch.** Everything in the pack right
    now is built and **unobserved**; that sitting is the only eyes either fix ever
    gets before it ships.

### ⚠️ 2026-08-20 — C50 IS BUILT, AND IT TOUCHES THREE SCREENS RATHER THAN THE TWO ITS BRIEF NAMED. Your sitting in link 4 changes slightly.
<!-- ck:- status:closed owner:no -->

Body archived in [archive/PLAYTEST_ARCHIVE.md](archive/PLAYTEST_ARCHIVE.md); search `ck-` and this heading.

### ⭐⭐ 2026-08-20 — THE PLAN CHANGED ON YOUR RULING: C50+C51 ship IN 1.0.0, C52 is frozen, and the chain that closes this repo is written and waiting.
<!-- ck:- status:closed owner:no -->

Body archived in [archive/PLAYTEST_ARCHIVE.md](archive/PLAYTEST_ARCHIVE.md); search `ck-` and this heading.

### ⚖️⚖️ 2026-08-20 — YOU RULED THE POST-RELEASE TESTING MODEL, and corrected a cost I had been quoting wrong.
<!-- ck:- status:ruled owner:no -->

Body archived in [archive/PLAYTEST_ARCHIVE.md](archive/PLAYTEST_ARCHIVE.md); search `ck-` and this heading.

### ⭐ 2026-08-20 — C49 is RETIRED on your word, and I measured how hard C50/C51 actually are. ✅ Item 34's "now or after" was ANSWERED THE SAME DAY — before launch.
<!-- ck:56 status:closed owner:no -->

56. ✅ **`C49` → `wontfix — unreachable`, done.** Your words: *"c49 wontfix -
    unreachable is right, get it off our list and retire it."* The entry keeps the
    reading and records the retirement, with the one falsifier that would bring it
    back named: non-vanilla code assigning `show_overlay = "soil_solid"` — a mod
    or the console, which is the only route there has ever been.

    ⭐ **And I stopped guessing at C50/C51 and went to the shipped language data.**
    You said these look simple and that fredware's modules should let us validate
    quickly. **Half right, and the half that isn't is the important one.** Every id
    below was looked up this session in the real `German.fpk`, extracted with our
    own tool:

    | id | who uses it | in the German pack? |
    |---|---|---|
    | `914616772802` | the terraforming heading's *unused* record | ✅ *TERRAFORMING-GESAMTFORTSCHRITT* |
    | `407456913268` / `316233855405` | *Back to Earth* title/text, unused records | ✅ *Zurück zur Erde* / full sentence |
    | `885571832096` / `807999655245` | the ids the button **actually** uses | ⛔ **absent — 0 hits, both** |
    | `880574954148` | SpaceY's shipped description | ✅ present and translated |
    | `981267450064` | **fredware's replacement SpaceY text** | ⛔ **absent — 0 hits** |

    * ✅ **`C51` is as simple as it looks, and it is loss-free.** Nothing is
      re-worded — three UI elements get pointed at ids whose translations already
      ship. I verified the two hook points at source myself: `TerraformingOverall`
      and `customUniversalRocket` are both real classes with an `Init`, and the
      rocket button carries `Id = "idBackToEarth"`, so that half needs no text
      matching at all. It writes nothing to a save. ⚠️ **Two catches, both small.**
      The terraforming heading has *no* Id, so the only handle is its literal
      English text — fine on a frozen game, fragile in principle. And **an English
      player sees no change whatsoever**, so proving it works means switching the
      game to another language for one look. Scope is exactly three strings; the
      *COLONY DATA* heading and two Options strings have no record in any pack and
      are a different, bigger job.
    * ⛔ **`C50` is the opposite: trivial defect, no free fix — and fredware's
      module is the one route we must NOT copy.** Their fix swaps the description
      for `T(981267450064, …)`, and that id is in **no** language pack, so under
      `EF-039` all eight non-English languages would render the English literal.
      Our entry predicted this; the lookup above confirms it. What is left: append
      an untranslated English sentence to the shipped translated text (safe, but
      one English line inside eight translated descriptions), or ship our own
      per-language table (`ModItemLocTable`, which overrides the shared table for
      vanilla and every other mod), or leave it. ⇒ **This one is a judgement call
      about which harm you accept, not a coding problem, and no amount of testing
      settles it.**
    * ⚠️ **`C52` — your memory is right, it is the risky one.** Three defects, and
      only one is cleanly ours: re-enabling the hyperlink path *may reinstate the
      fault the developers' comment was working around; the thumbnail cache is not
      fixable from a mod at all (it is upload discipline — bump the version when
      you swap art); and even the screenshot loop's diagnosis differs from theirs,
      because our own `EF-008`/`EF-064` refutes their stated mechanism.

    ⇒ **Still your call and unchanged in shape: `C51` is a genuinely small, safe
    module; `C50` needs a ruling from you before anyone writes a line; `C52` is
    1.0.1-or-later.** ⛔ All of them touch `Code/`, so building any of them before
    the upload breaks byte-identity with what run B packed and re-opens the gate.

    ⭐⭐ **UPDATE, same day — you asked me to go deeper on `C50`, and the deep
    reading changed the answer twice.** Full derivation in `agent/bugs/C50.md`
    ("REPAIR-ROUTE ANALYSIS"); the three things that matter to your decision:

    * ⛔ **The safe-looking fix I described this morning is NOT safe here.**
      Appending to the description turns it into a "concatenated" string, and the
      game's own text function *throws away the lookup table* when it sees one —
      so SpaceY's first bullet, which fills in its rocket's cargo number from that
      table, would lose the number it prints. **Breaking bullet 1 to complete
      bullet 3 is not a repair.** Both facts read at source this session.
    * ⭐ **But there is a route that survives, and it is better than "one English
      line".** Leave the sponsor text alone and add our bullet in the *screen* that
      shows it (two places show it). And the added bullet does **not** have to be
      English: the game already ships a translated sentence for exactly this —
      *"Maximum number of Drones a Drone Hub can control"* is a real record in all
      nine languages (I read the German). Even the number can come from the game's
      own table, so it stays right if a patch ever changes the base value. ⇒ **a
      fully translated bullet, no English anywhere, nothing rewritten.**
    * ⛔ **~~So the decision is not technical any more — it is editorial… that is a
      *judgment call* in our own sense of the word.~~ WRONG, AND YOU OVERTURNED IT
      THE SAME HOUR.** You said a genuine defect is by definition a bug, and our
      own published definition agrees with you: a judgment call is one that
      *"required deciding what the game meant"*, where *"there is no coding
      error"* or where *"we added a behaviour the game does not have"*. **Neither
      applies.** The 5-of-6 sponsor control settles what the game meant, and the
      `+20` is granted and working — the description contradicts the preset it
      lives in, which is your store card's own test. The pack also **already**
      ships a description repair (`Fix_TechDescriptionBuilding`, F25) that carries
      no judgment-call mark. ⇒ **`C50` is a plain repair, and the "five judgment
      calls" line on your store page does not move if it ships.** Correction
      recorded in `agent/bugs/C50.md`.

    ⛔ **CORRECTION 2026-09-14 (B5, archive read-back disposition) — this heading
    was STALE for 25 days.** It read *"Item 34's 'now or after' is still yours."*
    True the morning of 2026-08-20, false by that evening: the close-out chain built
    `C51` (link 1) and `C50` (link 2) the same day, and `C52` was parked on your
    ruling. **All four of item 34's defects were dispositioned on 2026-08-20** —
    `C49` `wontfix`, `C50` + `C51` `tested-attended` and shipped at launch, `C52`
    `parked`. ⇒ Item 34's question was answered by action: **before launch.**
    ⚠️ `C50`/`C51`'s modules are NOT in the tree today — both were deleted in
    `2dc1dbe` (2026-09-08, hotfix 2's 36-module REMOVE pass, 37 deletions / 0
    additions under `Code/`) when the 1.1.0 baseline landed. They shipped at launch;
    they are gone now, and that is a different fact.

    ⭐ **Your ruling 2026-09-14: no restorations.** All five leading candidates in
    `agent/reports/ARCHIVE_RECHECK.md` are discharged — that report's "Disposition"
    section carries the other four verdicts. The audit's real yield was this one
    stale line. ⚠️ The marker above was added in the same pass: this section was one
    of the 12 unmarked items, so under item **177**'s retirement rule it could never
    retire. It counts against that separate pass, it does not clear it.

### ✅ 2026-08-20 — your two rulings are carried out. Nothing owed back; this is the receipt.
<!-- ck:- status:closed owner:no -->

Body archived in [archive/PLAYTEST_ARCHIVE.md](archive/PLAYTEST_ARCHIVE.md); search `ck-` and this heading.

### ⭐⭐ 2026-08-19 — THE VERDICT REVIEW IS DONE: **UPHELD**. **53 RULED 09-12: pare the modder surface down, and the hardening queue shrinks with it — six rows go, one survives and needs your word.**

54. ⭐⭐ **I tried to break the audit's upload verdict and could not.** A second,
    independent session ruled on it as your design required — not by trusting
    the audit, but by re-checking its evidence from the primary sources before
    reading its reasoning. What was re-verified first-hand: the shipped files
    are byte-identical from the release gate's commit (and from the release
    tag) to today; the built package re-hashes to the recorded fingerprint;
    your 10-of-10 gate's log-readable results all reproduce under a freshly
    written checker (including the packed-vs-unpacked comparison, redone
    because a tool once lied "identical" on empty input); and the two console
    reads you took in act 1 — the ones that proved both core fixes — were
    found in the live game logs and re-read. **Verdict: UPHELD. Upload when
    you are ready.** Full record: `SWEEP_FINDINGS.md` (VR-1…VR-6).

    **Three things worth ten seconds each, none needing a decision:**

    * ⭐ **Your act-1 console evidence was one log-rotation from being lost** —
      the two logs holding the `suspect: nil` / `order: 75` reads were never
      archived. They are now (`docs/archive/act1_*`), copied and checksummed.
    * ⚠️ **One honesty correction to the audit's wording, not its verdict.**
      Its "no player this ships to can reach the unswept remainder" line
      quietly assumes an English-PC-solo audience; the portal also serves
      console, non-English and multi-mod players. The verdict still holds —
      each unswept item was individually bounded (the code never branches on
      platform, our text falls back to English, the hardening queue all needs
      a hostile third mod) — but that is *why* it holds, and the record now
      says so.
    * ⭐ **One new post-upload step added to the upload sheet** (§0.5(f), takes
      a minute): after the listing is live, download your own mod once and
      checksum it. Everything the chain verified stops at the file we upload;
      nothing yet confirms players receive those same bytes.

    ⚠️ Also: mid-review, the game's account state showed fix pack + TestKit
    re-ticked (21:23 log) — no launch was taken and nothing was changed on the
    rig by this session.

53. ✅ **RULED 2026-09-12 — pare the modder surface down. The scope decision was applied the
    same session; the hardening queue is disposed of row by row below, and ONE row survives the
    ruling and is still open.** Your words: *"We seem to be doing alot of work and checking for
    other modders, maybe we just need to pair that down to basic of what our mod does and how it
    does it. If they are a modder they should be able to examine it and handle it themselves."*

    **What the ruling did to the documentation.** The modder-facing text is now three things:
    what the pack does, how it does it, and the veto stated once and correctly. **Cut** from
    `README.md` and the site's `for-modders` page: the offer to narrow our patch if your mod
    conflicts, the invitation to tell us where `ListFixes()` prints, the ⛔ box about load order
    we said we could not explain, the "a small number of fixes re-read the table" detail, and the
    console-is-not-a-route aside. **Kept:** the runtime-patching description, item 50's ruled
    chain-vs-copy sentence, the stand-down check, the veto snippet, and where the ids come from.
    ⛔ `metadata.lua` is untouched — the store card was already this short and already correct, so
    it was the reference the other two surfaces were made to match, and **no upload is triggered**.
    The corrections that rode along are **item 47**.

    ⚖️ **The queue, row by row.** Canonical list: `agent/reports/99_TERMINAL_AUDIT.md` §6; line
    numbers below re-read against today's `Code/`, because hotfix 2 moved them.

    * **Rows 1 and 2 — DEPRIORITISED BY THIS RULING. Not fixed, not closed.** Their entire
      exposure is a third party writing a hostile value into our globals, which is exactly the
      surface the ruling shrinks. ⚠️ **Written down so a future session can find it rather than
      re-derive it:** `SMRFixPack_Disabled = "yes"` passes the `or {}` adoption at
      `00_Core.lua:13`, and the index at `:512` then reads nil for every id — **the modder's veto
      is silently ignored and every fix applies anyway**. `SMRFixPack_Disabled = true` throws at
      that same index instead, which **kills the whole pack log-only, with nothing the player can
      see**. Row 2 is the same shape one level up: the `SMRFixPack` adoption itself (`:19`) and
      `SMRFixPack_Optional` (`:17`, read at `OptionEnabled`, `:57`) are adopted with `or {}` and
      never type-normalised. The closing forms are derived in the audit's §6 and still apply if
      the row is ever taken — including its finding that a plain `type(x) == "table"` guard is
      **not** enough on its own.
    * ⛔ **Row 3 — STILL OPEN, and INDEPENDENT of this ruling. It needs its own word from you.**
      `Code/Fix_StaleReservations.lua:120-159` walks every Residence's reservation list on
      `OnMsg.NewDay` with no per-item `pcall`. **Its trigger is save corruption, not another
      mod**, so paring the modder surface does nothing for it: a throw mid-sweep abandons the rest
      of the list every sol with the fix still reading `active`, and it can reach the player's
      error box. The pack's own donor shape is live in `Code/90_SaveSanitizer.lua:224`.
      ⚠️ The audit's donor pointer (`Fix_TrainMinors:141`) is stale — that module was deleted by
      `2dc1dbe`.
    * **Row 4 — `OnDataReady` (`Code/00_Core.lua:433-448`) belongs to C90's build**, so it is
      tracked there rather than here. The consumer the audit named
      (`Fix_FirstAsteroidPrefabs:237`) was deleted by `2dc1dbe`; the two live consumers today are
      `Fix_BuildingCodesPrefab.lua:247` and `Fix_SilentHitMomentFX.lua:286`.
      → [agent/bugs/C90.md](agent/bugs/C90.md)
    * **Rows 5, 6 and 7 — DROPPED.** Cosmetic or latent, and none is a player-visible loss: a
      `ctx.heal()` log line plus the two silent heal sites; mark-clear completeness at
      `ApplyModOptions` and the benign-latch-after-non-benign-latch pair (both latent — the first
      needs `def.optional`, and **no shipping module declares it**); and a re-registration log on
      a title mismatch, which the audit itself filed as a candidate only.
    * **Row 8 — MOOT.** Both modules it was about are gone: `2dc1dbe` deleted
      `Fix_DustDevilSpawnGate.lua` and `Fix_DustDevilsDescrMap.lua`.

    *(The original finding is kept below.)*

    ⭐ **The audit's verdict: upload the mod exactly as it stands.** A second,
    independent session (`99b_VERDICT_REVIEW_fable.md`) will try to break that
    verdict before you act on it — that review is the next session to run, and
    the upload waits for it, not for anything below.

    **What the audit did.** Ten independent verifier sessions each tried to
    *refute* the chain's findings rather than confirm them (your fan-out
    design). Most findings survived. Three did not: one recorded "gap" turns
    out not to exist (the game combines `Done` methods, so the track-station
    reclaim works after all — the error was in our favor); one measuring tool
    was flattering itself (its "24 full replacements" number is wrong — at
    least 4 of them actually chain politely; the tool is quarantined); and one
    code comment we accused of being backwards was right all along. The two
    core fixes that paused the upload survived a hostile re-read completely.
    The full record is `docs/agent/reports/99_TERMINAL_AUDIT.md`.

    **Said plainly, because the rules require it:** the sweep chain stopped at
    its cap with territory still unswept — console platforms, non-English,
    other people's mods, long sessions. That is *"we stopped counting"*, not
    *"it is clean"*. But none of the remainder can touch a player running this
    pack alone on the current game build, which is who 1.0.0 ships to, and the
    release gate you ran covers exactly that player. That is what the YES
    rests on.

    ❓ **The one call that is yours — the recorded hardening queue.** The
    sweep recorded a short list of code guards (all in `00_Core.lua` plus one
    module): they only matter if another mod, or a modder following our README
    wrongly, writes into our globals — a player alone can never trigger them.
    Applying them now would edit the exact file your 10-of-10 gate just
    validated. Three options:

    * ⭐ **Recommended: ship 1.0.0 as validated; do the whole queue as one
      1.0.1 hardening pass** verified by one unattended launch. The gate stays
      exactly what it measured; the queue's defects need a hostile third party
      that a fresh release does not have. (Your *"clean period"* ruling was
      about a defect players would see — none of these is.)
    * **Apply now + one unattended verification launch** — run B proved packed
      behaves identically to unpacked, so the unattended launch carries over;
      cheap, but the shipped file is no longer byte-for-byte the one the gate
      ran.
    * **Apply now + re-run the full two-act gate** — the strict option; costs
      you another sitting.

    ⚠️ One queue item was *wrongly marked settled* and the audit reopened it:
    the daily stale-reservation sweep has no per-item guard (the console test
    that cleared its two siblings never covered it — it's a plain loop, not a
    map walk). It's in the same queue, same third-party gating logic... except
    corruption, not a mod, is its trigger, which is why it's queued and not
    urgent: a throw there just leaves vanilla's own stale state in place.

    ⚠️ **One check-at-upload item added** (it's in the upload sheet §0.5): after
    the Paradox upload, check the portal listing has a "required game version"
    — the game never sends one, and players who turn on the mod browser's
    "only compatible" filter would otherwise never see the pack.

### ✅ 2026-08-19 — THE RELEASE CHECK IS DONE. You ran both acts; the gate scored **10 of 10**. Nothing below is owed from you — item 52 is kept as the record of what was run.

> ⭐⭐ **DONE 2026-08-19, attended, both acts.** Both core fixes proven (fix ②
> needed a real `Reloading done in 1358 ms`), archive rebuilt (**80 files, 80
> byte-identical to the tree**), and run B scored **10/10** — including the three
> nobody had ever tested: it loads **`packed`** (66 archived sessions all said
> `unpacked`), the **preview image renders** on the packed path, and **uninstall
> holds for all 75 at once**. ⭐ The 75 module names are **set-identical** packed
> vs unpacked, so packing changes nothing.
>
> ⚠️ **What act 1 got wrong and cost you two launches:** step 5's
> `DbgPackMod(...)` at the console **cannot work** — that function is not in `_G`
> on retail at all, and neither is `ReloadLua`. The blacklist story was never
> about the console. **The route is Mods Manager → Edit (Ctrl-E) → Mod Editor →
> File → Pack Mod**, a menu item with no button, which is why you couldn't find it.
>
> ⛔ **This is not "the upload will succeed."** Nobody logged in, nothing was
> transmitted, no listing exists. Next is the terminal audit, not an upload.
> ⛔ **Your mods are all unticked** — re-tick the fix pack and Test Kit before the
> next session's numbers mean anything.

52. ⛔ **The final release check needs your hands twice, and I can now say exactly
    why nobody has ever run it.**

    **What the check is.** Run B tests the mod the way a *player* receives it:
    squeezed into one archive file and installed like a download, with our test
    kit switched off. Every reading this project owns was taken the other way —
    the mod spread out as loose files through a developer shortcut, with the test
    kit loaded. Your ruling stands: the green test suite is information, **this**
    is the gate.

    **Why it stalled.** To test the archive I first have to *build* it. The
    game's build command, `DbgPackMod`, is on a list of things mod code is
    forbidden to call — so neither our mod nor our test kit can build it — and an
    unattended session cannot type into the console. **Building the archive is a
    console line, the console is you, and the entire gate sits behind it.**

    **And it is two sittings, not one.** The archive cannot exist until you make
    it; the install cannot exist until the archive does; the Mod-Manager tick and
    the "is the picture there" look cannot happen until the install does. I had
    planned this as one visit and that was simply wrong.

    ---

    **⭐ ACT 1 — about four minutes, at the keyboard. Nothing here uploads,
    publishes, or touches either store.**

    Load any save with a real colony (`C47FARM` is fine). Press Enter for the
    console. In this order:

    1. `print(Mods.SMR_CommunityFixPack.version, Mods.SMR_CommunityFixPack:IsDirty())`
       — must print **`0  false`**.
       ⛔⛔ **CORRECTED 2026-08-19 — this line said `1  false`, and it was
       inverted on the exact thing it exists to catch.** `version` is the third
       digit only (`metadata.lua` holds `'version', 0`, which is what renders as
       1.0.**0**), and the 08-19 console read returned `0 false`. As written, a
       correct `0` would have stopped you for no reason — and a `1`, which **is**
       the 1.0.1 bump this step guards against, would have been read as fine and
       waved through to upload.
       ⇒ **`0` = 1.0.0, which is what you ruled. ⛔ A `1` means the version has
       already moved — stop.** And `IsDirty()` must be **not-`true`**: if it says
       `true`, stop too, because step 5 would force a save and bump it.
       ⛔⛔ **CORRECTED AGAIN 2026-08-20 — the second value was wrong here too.**
       This said *"must be `false`"* and cited a `0 false` console read; **no
       archived log contains that string.** The one reading on record is
       `dirty: nil` (`archive/act1_…15.18.19…:258`), and `nil` is the CORRECT
       clean answer whenever the mod has not been opened in the Mod Editor this
       session (`IsDirty` returns `old_hash and …`, and `old_hash` is unset —
       `CommonLua/GedEditedObject.lua:93-98`). ⇒ **`nil` and `false` both PASS;
       only `true` stops you.** Full reading table: item **70**.
    2. `print(SMRFixPack.fixes.SaintBlessing.update_suspect, #SMRFixPack.order)`
       — expect **`nil  75`**. *(That `nil` is core fix ① proven.)*
    3. `local n = 0 local ok = pcall(function() AllMapsForEach(true, "Colonist", function(c) n = n + 1 if n == 2 then local t t.x = 1 end end) end) print("L5 MapForEach:", ok, n)`
       — three of our repairs walk every colonist and fix what they find. If one
       object goes wrong halfway, does the game skip it and carry on, or silently
       abandon the rest of the list? That loop lives in the game's C code and
       cannot be read. This breaks the **second** item on purpose.
       *`true` and a number above 2* → it carries on, non-issue. *`false 2`* →
       it abandons the rest, and three fixes want a small change next release.
       **Neither answer blocks launch; both are worth having.**
    4. `print("L5 errbox:", config.DisableErrorReporting, ReportedMods)`
       — whether the game's own *"Mod Flagged"* pop-up is even switched on here.
       Expect `nil false` (or `nil nil`).

    ⛔ **Now quit to the MAIN MENU before the next line, and this ordering is not
    fussiness.** Step 5 reloads every script in the game, and nobody has ever
    measured what a mid-game script reload does to a live colony — the two
    sessions in our records that ever did it were both at a menu. Steps 1–4 need
    a colony; step 5 must not have one.

    5. `DbgPackMod(Mods.SMR_CommunityFixPack, false)` — **this builds the
       archive** and forces the second script load. A few seconds. It does not
       upload anything and does not touch either store.
    6. `print(SMRFixPack.fixes.SaintBlessing.status, SMRFixPack.fixes.SaintBlessing.update_suspect, #SMRFixPack.order, #SMRFixPack.UpdateSuspects())`
       — expect **`active  nil  75  0`**. *(The `75` is core fix ② proven — it
       used to become 150. The `0` is the box confirmed not to fire.)*
    7. Optional, ~30 s: `*r SMRTest.RunAll()` — a prediction nobody has tested:
       **2 false failures** after a reload. Either answer is worth having.

    **Then quit the game and paste me what 1–4, 6 and (if you ran it) 7 printed.**
    Anything other than the expected values is a launch-blocker and I want to see
    it before anything is uploaded.

    ⚠️ **Your autosaves are already copied** — both `Autosave Sol 406/411`,
    byte-verified, parked outside the save folder — so act 1 is safe to start
    whenever you like.

    ---

    **BETWEEN THE ACTS — my side, no time from you.** I check the archive holds
    exactly the 80 files it should and that packing altered none of them, then I
    install it the way a download installs and take the developer shortcut out.
    *(Both checks are already built and already proven against the archive you
    made on 08-17 — see the note at the bottom.)*

    **⭐ ACT 2 — about three minutes, and this one is looking, not typing.**

    1. Start the game → **Mods** → untick and re-tick **"Relaunched Fix Pack"** →
       ⛔ **and untick "Community Fix Pack — Test Kit" and leave it off** →
       close the dialog → **restart the game**. Unavoidable: taking the shortcut
       out costs the mod its enable and putting things back does not buy it back
       (item 45, and the same thing that bit the Opt-In pack in item 43).
       ⛔⛔ **THE TEST-KIT UNTICK WAS MISSING FROM THIS STEP UNTIL 2026-08-19 AND
       ITS ABSENCE WOULD HAVE VOIDED THE WHOLE GATE.** Run B *is* "test kit off"
       by definition (`00_CHAIN_SPEC.md` §6) — with the kit left on you get a
       packed run A, which is not the configuration a player receives and not the
       thing this gate exists to test. Steps 2 and 3 below both already say
       *"with the kit off"*, so the script assumed the untick it never asked for.
       ℹ️ The Opt-In pack needs no action — it is already off and stays off.
    2. **While you are on that screen, three looks, all free:**
       - **Is there a picture** beside the Relaunched Fix Pack entry? That image
         path was hand-written against the loose-files install and **has never
         been seen on the packed one**.
       - Does the version read **`1.00-000`**? ⚠️ **Corrected 2026-08-19 — this
         said "1.0.0", which that screen never prints.** The Mods Manager was
         seen tonight rendering `version 1.00-000`, because `GetVersionString`
         is `"%d.%02d-%03d"` (`Mod.lua:1176-1178`). `1.00-000` **is** 1.0.0 under
         that format and is the PASS; the plain `1.0.0` is a different surface.
         ⛔ A `1.00-001` means the version moved — stop.
       - **Anything of ours on screen that should not be** — a dialog, a
         notification? ⚠️ Expect the game's own *"Welcome to Mars, Commander!"*
         box when a game starts: that one is vanilla, our test kit has been
         hiding it for every unattended run, and with the kit off it is back.
         **It is not ours and not a failure.**
    3. Then load a **named** save (not an autosave), let a few sols pass, save
       under a **new** name, and load that back. That is the save round trip, and
       with the test kit off it cannot be scripted — it has to be you.
    4. Quit, tell me it is done, and I read the log and score the gate.

    ---

    ⛔ **What no part of this touches: Paradox or Steam.** The first call to
    either store's API *creates the listing* — there is no "everything but the
    last click" — so the rehearsal goes nowhere near one, by design.

    ℹ️ **What I did get done without you tonight**, so act 1 is the only thing
    standing between us and a scored gate: the pre-upload check passes all 20
    guards; the archive's expected contents are now predicted by a tool that
    reproduces your 08-17 archive exactly, 80 files out of 80; **packing was
    proven not to alter a single one of our files** (78 of 80 byte-identical to
    disk, and the 2 that differ are exactly the two files we have edited since);
    and **four of the gate's ten pass criteria were repaired before anyone scored
    them** — one asked for a number the game never prints, one had arithmetic
    that would have sent a runner hunting a module that does not exist.

### ✅ 2026-08-19 — two calls from the last sweep link. **50 RULED + APPLIED 09-12 (soften the chain-vs-copy promise) · 51 CLOSED 09-12 as overtaken, with the unrun leg re-filed as a takeable. Nothing is owed from you.**
<!-- ck:50 status:ruled owner:no -->

50. ✅ **RULED 2026-09-12 — soften it. APPLIED the same session, words only.** Your word. The
    sentence that promised an outcome for other mods now says what the code does, and the README's
    half-sentence says the same thing:

    * **`Code/00_Core.lua:4-7`** (was `:4-5`) — the design goal now reads
      *"Mod-compatible where the bug allows: a fix chains the original where the defect can be
      hooked, so another mod that hooks the same function keeps working; where the defect sits
      mid-function it copies a corrected body instead (FIX_POLICY §1.5), and those are the ones
      most likely to clash."* The old sentence was true at the chaining sites and false at the
      copying ones; the new one describes both, so it stays true whatever the split is.
      ⚠️ **The 66 / 42-chain / 24-copy count in this item is the 2026-08-19 number, taken at 80
      modules. Hotfix 2 removed 36 and re-copied 10; nobody has re-derived the split since, and
      this ruling did not.** Do not quote 42/24 as current.
    * **`README.md`, "For modders"** — *"chain rather than clobber"* → *"chain the original where
      the bug can be hooked and copy a corrected body where it cannot"*.
    * ⛔ **`metadata.lua` untouched.** The store card already carries the honest version (it was
      rewritten for hotfix 2): *"It hooks the game's functions and calls the original where it can
      … Where a bug sits in the middle of a function and cannot be hooked, the fix copies the
      corrected body instead — those are the ones most likely to clash."* Nothing to change there,
      and no upload is triggered by this.
    * ⛔ **No code behaviour changed** — comment and documentation text only; `parsecheck` 50/50,
      doccheck GREEN.

    ⚠️ **The veto-snippet rider below is NOT part of this ruling and is still open.** The README's
    *"setting a fix's identifier in that global table"* still reads as an invitation to write a
    list, and its example still names **`DustDevilSpawnGate`, a module `2dc1dbe` deleted** — the
    site's `for-modders` page was re-pointed at a live id by hotfix-2 link 100, and this README was
    missed. One word plus one half-sentence; say the word and it goes in with the next doc pass.
    *(The original finding is kept below.)*

    ⚠️ **Two sentences we publish promise other mods more than the code delivers.
    Your call on the wording; nothing else changes.**

    **What we say.** The README's "For modders" section says the pack will
    *"chain rather than clobber"*, and the top of `Code/00_Core.lua` — which ships
    inside the mod, so a curious modder reads it — says fixes *"prefer
    wrapping/chaining originals over replacement, **so other mods that hook the
    same functions keep working**."*

    **What the code does.** I counted it, mechanically, for the first time: of the
    66 places the pack patches something, **42 chain** (they call the original, so
    another mod's version of that function still runs) and **24 replace it
    outright** (they don't, so it doesn't). That is 11 of the 16 global functions
    and 13 of the 50 class methods.

    ⛔ **This is not a rule being broken.** Our own house rules explicitly allow a
    full replacement when the bug sits mid-function and can't be hooked, and they
    already warn that those are *"the fixes most likely to clash with other
    mods."* Every replacement I sampled carries the header the rule demands,
    naming the game file and lines it was copied from. These are deliberate,
    documented decisions and **I am not proposing to change any of them.**

    ⭐ **What is new is the number.** The rule says "keep the list short" and
    nobody had ever counted the list. 24 is the count. Whether 24 is short is your
    judgement, not mine.

    ⇒ **The decision is only about the two sentences.** The first ("chain rather
    than clobber") describes a preference as if it were a practice. The second is
    the one that actually matters, because it promises an **outcome for other
    mods** — and that outcome is true at 42 sites and false at 24.
    **Recommendation:** soften the `00_Core.lua` sentence to say the pack chains
    *where it can* and copies a corrected body where the bug can't be hooked. It
    costs one line, it is true, and it is the sentence a modder quotes back at us
    if something clashes. ℹ️ Same visit could carry the veto-snippet wording note
    below.

    ⚠️ **A smaller one riding along, same file.** The README says to disable a fix
    by *"setting a fix's identifier in that global table."* Read literally that
    invites `SMRFixPack_Disabled = {"DustDevilSpawnGate"}` — a **list** — which is
    a perfectly valid table, throws nothing, logs nothing, and **does not disable
    anything.** The person walks away believing they turned a fix off. The example
    directly under that sentence is correct; the sentence above it is what misleads.
    One clarifying half-sentence fixes it.

51. ✅ **THE TIMING DECISION IS CLOSED 2026-09-12 as overtaken — but ⚠️ THE LEG
    ITSELF WAS NEVER RUN, and it is re-filed so it cannot be lost.** On your
    "if it's overtaken close it". Every blocker this item names is gone, and I
    checked each rather than quoting the list: **run B ran 2026-08-19 and scored
    10 of 10** (item 52's block, "run B scored **10/10**"), **the pack launched
    2026-08-20** (item 71, both portal ids committed), and **the opt-in tick is
    done** (item 105, 09-08, 9 modules applying). There is no ordering left to
    decide, so the *"when"* has nothing to answer.
    ⛔ **What is NOT closed is the measurement.** No session has ever watched two
    independently-written patches stacked on one function. ⚠️ **Ordinary play is
    coverage-by-default, not this leg** — both mods have been loaded together for
    months (the 08-12 both-mods-loaded rule), which is why nothing has *broken*,
    but nobody has ever measured the stacked function. Re-filed as a takeable:
    **"Rider — the both-packs stacked leg"** under *Cross-cutting*, at the end of
    this file. *(The original reasoning is kept below.)*

    ⚠️ **There is one test worth running that I could not run, and my
    recommendation is to run it AFTER launch, not before. Your call on the timing.**

    **The test.** Every claim this pack makes about getting along with other mods
    is derived from reading code. Nothing has ever been *watched* — no second mod
    has ever been in the process while we measured anything. The one second mod we
    can legitimately use is **our own opt-in pack**, which patches two of the same
    functions the fix pack patches. A single unattended run with both loaded would
    be the only time this project ever sees two independently-written patches
    stacked on one function.

    **Why I did not run it.** The opt-in pack is currently switched off in your
    account, and putting a mod's folder back does **not** switch it back on — that
    takes you ticking it in the Mod Manager and restarting. That is a cost only you
    can pay, and spending it unattended is the one thing our own hazard list says
    never to do.

    ⇒ ⛔ **Recommendation: don't do it yet.** The final release test ("run B")
    needs the opt-in **off**, and it is the gate. This compatibility test is
    information, not a gate — by your own ruling. Turning the opt-in on now means
    turning it off again before run B, for a result that cannot block the launch
    either way. **Cleanest order: run B first, launch, then this.**
    ℹ️ Nothing owed today. The tick itself is still owed whenever you next open the
    Mod Manager (that is item 43); this just says what it would buy.

### ⚠️ 2026-08-19 — the SAME defect class, in the third mod. Not today's problem; do not let it be forgotten.
<!-- ck:- status:closed owner:no -->

Body archived in [archive/PLAYTEST_ARCHIVE.md](archive/PLAYTEST_ARCHIVE.md); search `ck-` and this heading.

### ⚠️ 2026-08-19 — the launch test's own first question could not fail. Already fixed; nothing owed unless you disagree.
<!-- ck:- status:closed owner:no -->

Body archived in [archive/PLAYTEST_ARCHIVE.md](archive/PLAYTEST_ARCHIVE.md); search `ck-` and this heading.

### ⛔⛔ 2026-08-19 — the upload would have shipped one fix missing, on Steam. **47 RULED + APPLIED 09-12, both halves — and a third defect was found in the same snippet. Nothing is owed from you.**
<!-- ck:47 status:ruled owner:no -->

46. ⛔⛔ **A fix would have vanished from the Steam release, and the check that
    was supposed to catch it said "pass".** ⇒ **Nothing to do — it is fixed and
    pushed.** This is the "what happened" you asked to always get.

    **What happened, in plain words.** The mod carries two lists of its own code
    files. One is the list the game reads to decide what to load; the other is
    the list the in-game Mod Editor keeps. They are supposed to be identical.
    When the automation-law fix was built on the 15th it went into the first list
    and nobody added it to the second. **The Mod Editor rebuilds the first list
    from the second every time it saves** — and *uploading* forces a save. On
    Steam that save happens **before** the mod is packed, so Steam would have
    received a mod that simply does not contain the automation-law fix. Paradox's
    very first upload would have escaped, because its save happens afterwards —
    but that save still rewrites the folder on your disk, so the Steam upload
    that follows, and every future update to either store, would have shipped
    without it.

    **Why it wasn't caught.** `tools/upload_preflight.py` has a guard for exactly
    this. It counted the words "ModItemCode" in the file — and one of those words
    is in the **comment at the top of the file explaining the guard**. 75 real
    entries plus one comment made 76, which matched, so it printed PASS. Two
    mistakes cancelling each other out. The guard now reads the actual entries
    and checks their order too, and I proved it by putting the fault back (it
    fails, and names the file that would have gone missing) and by scrambling the
    order (it fails, and says so).

    ⚠️ **The same broken arithmetic was reporting a *phantom* problem on the
    Opt-In pack**, whose list is in fact correct. That is fixed by the same
    change. And the Save Rescue mod has **no** editor list at all — probably fine
    for a different reason, but I did not verify it and it is not this chain's
    repo to touch. Worth one look before it ever uploads.

47. ✅ **RULED 2026-09-12 — "fix this". APPLIED the same session, words only, and the
    ruled paring in item 53 was applied to the same text in the same pass.** Your word on both
    halves. The store card was already right (it was rewritten for hotfix 2), so it was the
    reference the other two surfaces were made to match — and `metadata.lua` is untouched, so
    **no upload is triggered by this**.

    * **(a) the strict-globals form — done.** `README.md` published
      `SMRFixPack_Disabled = SMRFixPack_Disabled or {}`; it now publishes the same
      `rawget(_G, "SMRFixPack_Disabled") or {}` the pack's own `00_Core.lua:13` uses. The site's
      page had the same defect and is fixed too.
    * **(b) load order — done.** Both pages now say it in the card's words: *"Before the pack
      loads" means your mod has to load first.* The site's *"it does not matter whether yours or
      ours is created first"* sentence is gone, and so is the ⛔ box that said we could not tell
      you how to load first — the requirement is now stated plainly instead.
    * ⛔ **A third defect, not in the original item, and the worst of the three: the example named
      a fix that does not exist.** `DustDevilSpawnGate` was deleted by `2dc1dbe` in hotfix 2, so a
      modder following the published instruction today vetoed nothing at all. Both pages now use
      **`LakeEntombment`** (`Code/Fix_LakeEntombment.lua:41` registers it), which is the id the
      store card already used.
    * ⚠️ **Two site pages that pointed at deleted sections were repaired in the same pass**
      (`content/faq.md`, `content/install.md`): they promised *"the part of it we cannot tell you
      how to do"* and *"what we have not yet confirmed about it"*, and both of those sections were
      cut by the item-53 paring.
    * ⛔ **The site edits are in the OTHER repo (`SMR-CommunityMods`), uncommitted.** They are
      staged on disk in a clean tree for you to review and push with the next site publish.

    *(The original finding is kept below.)*

    ⚖️ **Two wording calls on the modder page — your call, ten minutes, and
    neither blocks launch.** Both are on `README.md` and the site's
    "For modders" page, which say the same thing in the same words.

    **(a) The example code we publish trips the game's own strict-globals
    check.** We tell a modder to write
    `SMRFixPack_Disabled = SMRFixPack_Disabled or {}`. Reading a name that does
    not exist yet is exactly what the game complains about — and our own code
    never does it: every place the pack reads that table it uses the safe form,
    `rawget(_G, "SMRFixPack_Disabled")`. The snippet still *works*; the cost is a
    line in the log, and I could not establish whether the retail build even
    prints it (the one time we have seen it was a debug build). **Suggested:
    publish the safe form, since it is the same one line our code already uses.**

    **(b) The page tells a modder the load order does not matter, and it does.**
    It says it *"does not matter whether yours or ours is created first — only
    that the values are set before our code runs."* Both halves are true, but
    together they require the modder's mod to load **before** this one — which is
    the player's enable order, with no priority field and no way to ask for a
    position. **Suggested: say that plainly on the modder page.** ⚠️ This is a
    *modder*-facing page, so it does not touch your standing rule that players
    never get load-order advice.

### ⚠️ 2026-08-19 — run B now has an ATTENDED moment in it. Nothing to decide; something to know.
<!-- ck:- status:closed owner:no -->

Body archived in [archive/PLAYTEST_ARCHIVE.md](archive/PLAYTEST_ARCHIVE.md); search `ck-` and this heading.

### ⛔⛔ 2026-08-17 — THE UPLOAD IS PAUSED ON YOUR OWN WORD. Two defects found at the sitting and fixed; two questions for you.
<!-- ck:- status:closed owner:no -->

Body archived in [archive/PLAYTEST_ARCHIVE.md](archive/PLAYTEST_ARCHIVE.md); search `ck-` and this heading.

### ✅ 2026-08-19 — THE VERIFICATION LAUNCH RAN: the mod is running clean in a real game. **43 CLOSED 09-12 as overtaken — the opt-in pack is enabled again. Nothing is owed from you.**
<!-- ck:43 status:closed owner:no -->

43. ✅ **CLOSED 2026-09-12 as overtaken — the opt-in pack is back on.** On your
    "if it's overtaken close it". The evidence is an observation, not a note:
    item **105** (2026-09-08) records the opt-in pack **ENABLED and applying, 9
    modules including `DroneOverhaul`**, read off a running 1.1.0 game — and
    says in its own words that ck43's "OFF" record is stale. The minute below
    was spent at some point between 08-19 and 09-08; nothing is owed.
    ⛔ **Not closed on `H-08`.** The hazard still stands exactly as written —
    `EF-055` records that pulling a junction DID cost the enable in August, and
    a folder-for-folder swap under the same id is the only shape that keeps it.
    This item closes because the enable came back, not because the risk did not.
    *(The original report is kept below.)*

    ⛔ **I broke the Opt-In pack's enable state, and I could not put it back.**
    Telling you straight, the way the autosave deletion was told to you.

    To run the suite "as a player will have it" I needed the Opt-In pack absent.
    Changing that switch properly needs the Mod Manager, which needs you — so I
    used the documented reversible trick instead: remove the folder shortcut, let
    the game not find it, put the shortcut back afterwards. **The putting-back
    did not work.** The game now sees the Opt-In pack sitting there, lists it,
    and **never runs a line of it**. I relaunched twice to be sure. Our own notes
    said this could happen; they blamed it on a Mod Manager visit in the middle,
    and there wasn't one this time, so the note was wrong about why.

    **The fix is one minute of yours and there is no other route:** open the game
    → **Mods** → untick and re-tick **"Relaunched Fix Pack: Opt-In Modules"** →
    close the dialog → **restart the game**. If it comes back, its own line in
    the log reads `opt-in pack present: 8/8 modules active`.

    ⚠️ **The Fix Pack itself is completely unaffected** — it ran perfectly in all
    three launches. And this is worth knowing before launch day for a second
    reason: **the final release check (run B) plans to pull the Fix Pack's
    shortcut exactly the same way.** If it does that, the packed mod may sit
    there not running, and the check would look like a disaster that is really
    this same switch. That is now written into the rehearsal's own notes.

44. ⭐ **Two minutes at the keyboard finishes the two core fixes — four sessions
    have now been unable to.** The two defects you paused the upload over were
    fixed on 08-17 and have **still not been proven fixed**, and I can now say
    exactly why: proving them needs the game's console, and an unattended
    session cannot type into it. Everything else about them is done.

    The good news first: **the fixed code definitely runs.** In tonight's
    launches the exact sequence that used to leave the false flag behind played
    out in the log, the repair line executed, and the module ended up healthy —
    all 75 fixes active, no error, no box on screen. What I cannot read from
    outside the game is the one leftover flag itself, and whether the second
    defect (a fix being counted twice) is gone, because that one only shows up
    when the game reloads its scripts mid-session.

    **The recipe. Any save, any colony, press Enter for the console, type these.**

    1. `print(Mods.SMR_CommunityFixPack.version, Mods.SMR_CommunityFixPack:IsDirty())`
       — must print **`1  false`**. ⛔ If it says `true`, **stop and tell me**:
       the next line would bump us to 1.0.1 and you ruled 1.0.0.
    2. `print(SMRFixPack.fixes.SaintBlessing.update_suspect, #SMRFixPack.order)`
       — expect **`nil  75`**. *(That `nil` is core fix ① proven.)*
    3. `DbgPackMod(Mods.SMR_CommunityFixPack, false)` — this is the reload. It
       does not upload anything and does not touch either store.
    4. `print(SMRFixPack.fixes.SaintBlessing.status, SMRFixPack.fixes.SaintBlessing.update_suspect, #SMRFixPack.order, #SMRFixPack.UpdateSuspects())`
       — expect **`active  nil  75  0`**. *(The `75` is core fix ② proven — it
       used to become 150. The `0` is the box confirmed not to fire.)*
    5. Optional, ~30 s, and it settles a prediction nobody has ever tested:
       `*r SMRTest.RunAll()` — link 2 predicted **2 false failures** after a
       reload. Either answer is worth having.

    **Paste me back what those four lines printed and the core fixes are closed.**
    Anything other than the expected values is a launch-blocker and I want to see
    it before you upload anything.

    ⭐ **Two extra lines, ~20 seconds, added 2026-08-19 by the failure-and-
    containment sweep — same sitting, nothing else needed.** Neither changes
    anything; both just print. They are optional, but line 6 is the only way to
    settle a question three of our fixes depend on.

    6. `local n = 0 local ok = pcall(function() AllMapsForEach(true, "Colonist", function(c) n = n + 1 if n == 2 then local t t.x = 1 end end) end) print("L5 MapForEach:", ok, n)`
       — **what it means.** Three of our repairs walk every colonist (or every
       track piece) in the colony and fix what they find. If one object goes
       wrong halfway through, does the game skip that one object and carry on, or
       does it silently abandon the rest of the list? Nobody knows, because that
       loop lives in the game's C code and cannot be read. This line deliberately
       breaks the **second** item and prints what happened.
       *`true` and a number bigger than 2* → it carries on, and this is a
       non-issue. *`false 2`* → it abandons the rest, and three of our fixes want
       a small change before the next release. **Either answer is worth having**;
       neither is a launch-blocker.
    7. `print("L5 errbox:", config.DisableErrorReporting, ReportedMods)`
       — the game has its own pop-up that says *"Mod-related problem detected…
       Mod Flagged: Relaunched Fix Pack"* whenever a script error touches our
       folder. We only found it this week and it has **never fired** in any of
       our 73 recorded sessions. This prints whether it is switched on at all on
       your machine. Expect `nil` and `false` (or `nil nil`).

### ✅✅ 2026-08-18 — STATE.md WAS EVICTED ON YOUR DIRECTION, AND YOU RULED THE CAPS THE SAME DAY. Nothing here is owed from you.
<!-- ck:- status:ruled owner:no -->

Body archived in [archive/PLAYTEST_ARCHIVE.md](archive/PLAYTEST_ARCHIVE.md); search `ck-` and this heading.

### ✅ 2026-08-18 — SWEEP CHAIN, LINK 4 REPORTED. **41 RULED + BUILT 09-12: the stand-down box names the fixes and stops blaming the game. Nothing is owed from you.**
<!-- ck:41 status:ruled owner:no -->

41. ✅ **RULED + BUILT 2026-09-12 — the box names the fixes, and it no longer blames the game for
    our own failures.** Your word: *"same shape as 39"*. Both halves went in as one text change,
    **7 lines in `Code/00_Core.lua`**, in the same thread as 39. ⛔ No new module, `items.lua` and
    `metadata.lua` untouched, apply path untouched.

    **(1) Readable names.** The list now maps each suspect id through
    `SMRFixPack.fixes[id].title` — the same plain-English title the fix list uses — and falls back
    to the id if a title is ever missing. The **log line keeps the ids**, so the diagnostic is
    unchanged. Titles go one per line behind a `·` bullet rather than comma-joined.
    ✅ **Route-checked, because this is the console surface:** the game's message box puts its
    description inside an `XScrollArea` with a scrollbar and RightThumbUp/Down gamepad bindings
    (`Lua/XDef/StdMessageDialog.generated.lua:166-209`), so a long list scrolls on a controller.
    Titles average 69 characters, so no cap was added.

    **(2) The wording.** Old: *"…found that the game code they patch has changed — usually after a
    game update — and switched themselves off for safety … if the game was recently updated, check
    for a new version."* New, in full:

    > **%d of this pack's fixes did not recognise the game code they repair, and switched
    > themselves off. A fix that switches itself off does nothing at all: the game behaves as it
    > would without it.**
    >
    > **Most often a game update has moved what the fix was written for. It can also be a fault in
    > this pack, or another mod changing the same code. Whichever it is, the repair comes in a new
    > version of the Relaunched Fix Pack.**
    >
    > **Switched off:**
    > **· <the fix titles, one per line>**

    It names our own fault and another mod as live possibilities instead of pointing at Paradox,
    and it tells the player what a switched-off fix actually costs them. The "check for a new
    version" advice survives, because it is still where the repair arrives.

    ⛔ **CORRECTION: "this box has never once appeared in any of the 57 recorded sessions" is no
    longer true.** It fired on the 1.1.0 boots of 2026-09-08 — `update report:` lines in six
    archived logs, up to **14** ids in one — and you asked to be exempted from it that same day
    (items 107–108). ⇒ Both defects this item describes have been in front of a player: the
    internal ids were on screen, and the message blamed a game update for a set that included
    modules our own re-verification had not yet re-seamed. ⚠️ **The new text has not been seen in
    play** — no boot since the change — so it is `built`, nothing stronger; the cheap check is one
    boot with any fix inactive. *(The original finding is kept below.)*

    ⭐ **Link 4 — lens 4 of 8, "player experience".** The question: **what does a
    player actually SEE and READ?** The answer should be *nothing*, and it very
    nearly is — the pack raises **no** notification, popup, banner or voice line
    of its own. Everything it can put on screen is a box the game already owns.

    **But there is one place the mod speaks in its own voice**, and it is the box
    you saw at the upload sitting: the message that appears when a fix has stood
    itself down after a game update. **Two things about its wording need you,
    because it is the mod's only voice — and on Xbox and PlayStation it is the
    only thing a player can ever see from us at all** (no log, no console there).

    * **It lists our internal file names, not the fixes.** It would say
      *"Switched off: AstrogeologistExtractors, SaintBlessing"*. Those names
      appear on **no page a player can reach** — not the mod page, not the fix
      list, not the FAQ. Meanwhile every one of the 75 modules already carries a
      plain-English title in the same style the fix list uses ("Command Center
      graph captions count maintenance, like the bars do"). We have the readable
      version and print the unreadable one. *(Same trap as the Bottomless Pit
      building that actually displays as "Experiment 1: Big Drop".)*
    * **If one of our fixes crashes, the box blames the game.** The message is
      one sentence covering every reason a fix switched off, and it says the game
      code "has changed — usually after a game update" and tells the player to go
      look for a newer version of our mod. That is right when a patch really did
      move something. It is **wrong** when the cause was a bug in **our** code or
      a clash with another mod — we would be pointing at Paradox for our own
      mistake and sending the player after a version that does not exist.

    ⛔ **Neither can happen today** — this box has never once appeared in any of
    the 57 recorded sessions, and no fix has ever crashed in one. This is about
    what it would say on the day it does.

    **Recommendation: fix both, in the terminal audit, as one small text change**
    — print the readable titles, and say "switched themselves off" without
    blaming a game update unless we actually detected one. It is words only, in a
    box no player has yet seen, so the risk of touching it is about as low as a
    code change gets. Say the word and it goes in the audit's list.

    **Nothing else needs you.** A third finding — our log never writes a line when
    a fix *recovers*, so 56 of 57 recorded logs end up saying a module is switched
    off when it is actually working — is a plain repair with no decision in it,
    and it is routed to the audit. Three other things were checked and came back
    clean: the mod-page claim that *every* fix inspects the game's code first is
    true for all 75 (checked one by one); the "five judgment calls" count matches
    on every surface; and the box's plumbing was traced through the game's own
    code for the first time and works.

    ⭐⭐ **The bigger question — and it is a real one.** Your chain has a cap of
    **five** links, and I am the fourth. **Four of the eight lenses would still be
    unasked**, and each of the remaining three owns a job with a track record:
    the "does the mod promise anything it doesn't deliver" lens (we have found
    that class of mistake **four** times now, most recently this session); the
    "packed install" lens, which covers the fact that **the mod has never once
    been loaded the way a player will load it**; and the "another mod is
    installed too" lens, which link 1 explicitly left 15 unchecked items for.

    **Recommendation: raise the cap to 8 and let the rotation finish.** Your own
    spec says stopping because you hit the cap and calling it "we found
    everything" is the worst thing this design can do — so I am saying plainly
    that I do **not** think one more link closes it. Each link is unattended and
    costs you only the moment you spend kicking it off.

### ✅ 2026-08-18 — SWEEP CHAIN, LINK 3 REPORTED. **40 RULED 09-12: `smr_shuttles` keeps its name, accepted as recorded. Nothing is owed from you.**
<!-- ck:40 status:ruled owner:no -->

40. ✅ **RULED 2026-09-12 — option (a), accept as recorded. No rename.** Your word. The
    `smr_shuttles` flag keeps its name; no shipped byte changes. Your 2026-08-01 hard rule is
    satisfied the way you wrote it: the place has a **written** decision, with reasons, in
    `agent/reports/L3_SAVE_FOOTPRINT.md`. ⚠️ **The consequence is the one option (b) would have
    bought:** a sweep keyed on the `SMRFixPack_` prefix will keep missing this one flag, so any
    future save-footprint pass has to add it by hand. That is the accepted cost, not an oversight.
    *(The original finding is kept below.)*

    ⭐ **Link 3 — lens 3 of 8, "save & exit".** The question: **not "is each fix
    save-safe" — every module was checked alone — but "what does the whole pack
    put into one savegame, and what happens to all of it at once when someone
    removes the mod?"** Nobody had added them up.

    **The one thing that needs you.** The pack keeps a small amount of its own
    bookkeeping inside your savegame — eleven named items, and our own rule says
    every one of them must be called `SMRFixPack_something` so that a sweep can
    find them all. **One does not follow that rule.** A single flag written by
    the Shuttle Hub fix is called `smr_shuttles`, and because our master list of
    "everything of ours that ends up in a save" was built by searching for the
    `SMRFixPack_` name, that one item was never on the list — the list even says
    explicitly that the place it lives contains *"nothing of ours"*.

    ⛔ **It is harmless, and I want to be plain about that before the question.**
    It is one true/false value tucked onto a cache entry. The game ignores it
    completely when the mod is gone, and the whole cache it sits in is thrown
    away and rebuilt the next time a dome is connected or a train route is
    rebuilt — so it does not even survive long. It changes nothing a player can
    see, and it does not block launch.

    ❓ **The call.** Your own hard rule from 2026-08-01 is that *every* place the
    mod can leave something in a save gets a written decision — and a place with
    no written decision blocks release by default, whichever way the decision
    goes. This one now has a written decision (it is recorded, with its reasons,
    in `agent/reports/L3_SAVE_FOOTPRINT.md`). So:

    * **(a) Accept it as recorded — RECOMMENDED.** The decision is written, the
      thing is harmless and short-lived, and nothing in the shipped code changes.
      This is the cheapest option and it satisfies the rule as you wrote it.
    * **(b) Rename it to `SMRFixPack_shuttles` first.** One word in one line of
      one file. It buys tidiness — every future sweep would find it — at the
      cost of touching the release candidate again, which is the thing you have
      been deliberately not doing.

    ⚠️ I could not make this change myself either way: from link 3 onward the
    chain only records what it finds, so that the final review sees every finding
    together before anything is edited.

    **Four smaller things found, all recorded, none needing you.** A comment in
    the meteor fix says one of our savegame flags *"stays in your save after
    uninstall"* — it does the opposite, the game drops it, so we have been
    describing more leftovers than we actually leave (the player-facing uninstall
    text already had this right). The knock-on: uninstalling and later
    reinstalling re-rolls the meteor timer once, which is bounded and arguably
    what you would want anyway. The savegame-repair module sets its "already
    done" marker *before* doing the work, so if a future game update ever moves
    the two functions it needs, it would mark the save done without having done
    it. And a comment in that same module lists 8 fixes as carrying their own
    load-time repair when the real number is 17 — one of the 8 no longer exists
    as a module at all.

    ⭐ **One genuinely good result worth telling you.** An older audit left an
    open question about three of our background timers having no "the mod is
    gone, stop cleanly" guard. All three have one now — checked by reading the
    code, not by trusting the notes — and across all six of the pack's background
    timers there is exactly one without a guard, which has a written decision
    already and cleans up after itself regardless. That question can be closed.

    ⛔ **What I could not reach, so you know what this did not cover.** Nothing
    was run in a game — no save was opened and nothing was weighed, so every
    *measured* number in this area is still the older one. Of the 18 repair
    passes that run when you load a save, I cross-checked 5 against the game's
    own 237 built-in save repairs; the other 13 are unchecked for interference.
    And nobody has ever actually walked an uninstall, let alone a reinstall.

### ✅ 2026-08-18 — SWEEP CHAIN, LINK 2 REPORTED. **39 RULED + BUILT 09-12: the stand-down box shows once per session. Nothing is owed from you.**
<!-- ck:39 status:ruled owner:no -->

39. ✅ **RULED + BUILT 2026-09-12 — the box shows once per session; the log line still writes every
    time.** Your word: *"this can be fixed if its cheap, but its also minor."* It was cheap — **4
    lines in `Code/00_Core.lua`**, inside the C1 report thread only. A flag on the `SMRFixPack`
    table (which is deliberately preserved across a Lua reload, `:19`) is checked after the log
    line and set before the box opens. ⛔ No new module, `items.lua` and `metadata.lua` untouched,
    and the `DataPatch` / `run_apply` / apply-verdict seam is not touched — this is the reporting
    surface, not the apply path.

    ⛔ **CORRECTION, and it matters more than the fix.** This item said the dialog *"has never once
    appeared in any of the 58 logs we have archived"*, and item 41 said the same. **That is no
    longer true, and the re-fire this item predicted has been OBSERVED — twice, in real sessions:**
    * `archive/logs/first110_*.log` (2026-09-08, the first 1.1.0 boot): **two** `Reloading done`
      events, each followed by its own `update report: 11 fix(es) deactivated…` line.
    * `archive/sit0817_MarsDebug*.log` (2026-08-17, your upload sitting): the same shape.

    On 2026-09-08 you asked to be exempted from that very box (items 107–108), so it was on screen,
    naming up to **14** internal module ids. ⇒ The re-fire is measured, not predicted. ⚠️ **What is
    still unexercised is the FIX**: nobody has booted the game since this change, so the guard
    itself has no in-play evidence and no status word above `built`. *(The original is kept below.)*

    ⭐ **Link 2 — lens 2 of 8, "lifecycle & idempotency".** The question: **what
    happens the second time our code runs in one session?** The game re-runs every
    mod's scripts whenever you close the Mod Manager after changing anything — so
    "the second time" is not a corner case, it is what happens to any player who
    turns on a second mod.

    ⛔ **It found a real one, and it was already sitting in your own logs.** Two
    archived sessions — both ones where you took a Mod-Manager tick — show the
    pack loading **twice**. Comparing the two halves of those sessions gives the
    same answer in both, and it is the *entire* difference between them:
    **four modules switch themselves off the second time, each giving a reason
    that is not true** — *"the shipped presets are already correct"*, *"the
    shipped tech already matches its own param1"*, and two more like it. The data
    **is** correct, because those four modules corrected it the first time round
    and the correction survived the reload. What did not survive was each module's
    memory of having made it.

    **Why it matters, and it is not the wording.** Three of our *save-repair*
    passes only run while their module reads "on". So a player with an older save
    who happens to have visited the Mod Manager that session silently does not get
    the Astrogeologist extractor bonus applied to their existing colony, does not
    get the Independent Terraforming discount corrected from 10% to the 20% it
    advertises, and does not get their dome Saints' blessing re-filed. Nothing
    errors, nothing is shown, it just quietly doesn't happen.

    ✅ **Fixed in `Code/00_Core.lua`.** The "have I already changed this data?"
    memory now lives for the whole session instead of for one script load.
    ⛔ `metadata.lua` untouched, no module added or removed, every count unchanged
    — this is still 1.0.0.

    ✅ **It is a relative of the two defects from your upload sitting, but not the
    same one, and the good news is that your dialog cannot fire from it** — all
    four of these stand-downs are the flavour the code marks "harmless", so no
    player sees a "check for a new version" box because of it.

    **Proven, not asserted:** I built a harness (`tools/l2_reload_sim.py`) that
    runs the pack's own shipped code twice in one process. Before proving anything
    it has to earn trust, so first it reproduces your two archived sessions
    exactly — all five of their first-load lines, word for word, and all four of
    the false second-load lines. Then: with the fix in, the four false lines are
    gone and all four modules stay on. And a control in the other direction — if a
    future game patch genuinely fixed this data itself, all four still correctly
    say "already correct". ⛔ **This is not a launch.** It runs our real code
    against a stand-in for the game.

    ❓ **The one call for you (it can wait, and "leave it" is a fine answer).**
    Our "some fixes switched themselves off" dialog is created fresh each time the
    game reloads scripts. So if that dialog ever *does* have something to say,
    a player who opens the Mod Manager again gets shown it **again**. The code's
    own comment calls it "a one-time dialog", so today it doesn't do what it says.
    **Recommendation: show the box at most once per session, keep writing the line
    to the log every time** — that keeps the diagnostic and drops the repeat.
    ⚠️ I did **not** just do it: it changes what a player sees, in a release
    candidate, and it is a judgment call about what the pack *should* do rather
    than a defect. Also worth knowing: that dialog has **never once appeared** in
    any of the 58 logs we have archived.

    ⛔ **What link 2 did NOT look at.** Nothing was run in a game — so the fix
    above, and both of the 08-17 fixes, still have not executed inside Surviving
    Mars even once. I have written down the shape of the single unattended run
    that would verify all three at the same time, but I did not build it. Also
    untouched: a third-and-later reload, whether a reload can happen mid-colony,
    the TestKit's own behaviour, save footprint and uninstall, what a player sees,
    failure containment, packed-vs-unpacked, and any other mod. **Two lenses of
    eight. The chain has not converged.**

### ⭐ 2026-08-17 — SWEEP CHAIN, LINK 1 REPORTED. Nothing blocks launch. One small call for you, and it can wait.
<!-- ck:- status:closed owner:no -->

Body archived in [archive/PLAYTEST_ARCHIVE.md](archive/PLAYTEST_ARCHIVE.md); search `ck-` and this heading.

### ⭐ 2026-08-17 — THE RENAME IS DONE, EVERYWHERE A PERSON LOOKS. ✅ Your two calls came back the same day; nothing is owed.
<!-- ck:- status:closed owner:no -->

Body archived in [archive/PLAYTEST_ARCHIVE.md](archive/PLAYTEST_ARCHIVE.md); search `ck-` and this heading.

### ⛔⛔ 2026-08-17 — SOLO LAUNCH: ✅ the parking work is DONE; one question left before you upload
<!-- ck:- status:closed owner:no -->

Body archived in [archive/PLAYTEST_ARCHIVE.md](archive/PLAYTEST_ARCHIVE.md); search `ck-` and this heading.

### ⭐⭐ NEW 2026-08-16 — "ONE MOD FIX ALL": I checked the other community mod against the game's code. Four real bugs we had missed. **One call from you: build them now, or after launch?**
<!-- ck:- status:closed owner:no -->

Body archived in [archive/PLAYTEST_ARCHIVE.md](archive/PLAYTEST_ARCHIVE.md); search `ck-` and this heading.

### ⭐⭐ NEW 2026-08-15 (late) — WE MEASURED YOUR OPEN FARM CASE ON YOUR OWN SAVE, AND IT DID NOT REPRODUCE. One sentence from you would explain that.
<!-- ck:- status:closed owner:no -->

Body archived in [archive/PLAYTEST_ARCHIVE.md](archive/PLAYTEST_ARCHIVE.md); search `ck-` and this heading.

### ✅ 2026-08-15 — the 54 MB leftover is DELETED (was: one word from you)

32. ✅ **RULED + DONE 2026-08-15: DELETED.** Your word: *"You can delete that
    save."* Removed and verified absent; the save directory now holds **77
    entries**, and the only non-`.sav` files left are `account.dat`,
    `account.dat.bak` and `steam_autocloud.vdf` — i.e. nothing of ours and no
    stray from the 08-12 cloud-restore batch. `EF-051`'s falsifier stands.
    ~~`U2RT1` (no file extension, 54 MB) is still in your save folder — delete
    it or leave it?~~ It is the one member of the 08-12 cloud-restore batch the
    08-14 cleanup missed: that sweep listed `*.sav` files and this artifact has
    no extension (a quirk this project's own testing produced — `EF-050`). Both
    of last night's launches were checked by creation-time window: **neither
    touched it**, so the cloud-off retirement stands and nothing is wrong. It is
    unattended-2's leftover, not a save you made, and nothing reads it.
    **Rec: DELETE** — same population, same license as the 888 MB you already
    ordered swept; it was left only because deleting it unattended felt like a
    daylight call. Say the word either way; "leave it" costs only the 54 MB.
    → `agent/facts/EF-051.md`, the 2026-08-15 bullet.

### ⛔⛔ NEW 2026-08-15 (later) — pricing your "quick playtest?" question found that the F85 dialog CANNOT BE OPENED IN THE GAME AT ALL, and two player-facing pages describe it as if you had seen it
<!-- ck:- status:closed owner:no -->

Body archived in [archive/PLAYTEST_ARCHIVE.md](archive/PLAYTEST_ARCHIVE.md); search `ck-` and this heading.

### ⭐ NEW 2026-08-15 — the C39 repair you ruled turns out to touch TWICE as many buildings as the ruling pictured. ✅ CONFIRMED THE SAME DAY.
<!-- ck:- status:closed owner:no -->

Body archived in [archive/PLAYTEST_ARCHIVE.md](archive/PLAYTEST_ARCHIVE.md); search `ck-` and this heading.

### ⭐ NEW 2026-08-14 (later) — ④ IS CUT: your launch afternoon reads ONE sheet, and the audit found one more call that comes before any paste
<!-- ck:- status:closed owner:no -->

Body archived in [archive/PLAYTEST_ARCHIVE.md](archive/PLAYTEST_ARCHIVE.md); search `ck-` and this heading.

### ⭐ NEW 2026-08-14 — the release descriptions are being written: ONE question, and it is bundled with a call you already owe
<!-- ck:- status:closed owner:no -->

Body archived in [archive/PLAYTEST_ARCHIVE.md](archive/PLAYTEST_ARCHIVE.md); search `ck-` and this heading.

### ⭐ NEW 2026-08-13 — the SITE is built (unpublished): one small question, and two things for your awareness
<!-- ck:- status:closed owner:no -->

Body archived in [archive/PLAYTEST_ARCHIVE.md](archive/PLAYTEST_ARCHIVE.md); search `ck-` and this heading.

### ⭐⭐ NEW 2026-08-13 — D13 CHAIN CLOSED; the ONE combined sitting is READY (step ② — the release line's next move is yours)
<!-- ck:- status:closed owner:no -->

Body archived in [archive/PLAYTEST_ARCHIVE.md](archive/PLAYTEST_ARCHIVE.md); search `ck-` and this heading.

### ⭐⭐ NEW 2026-08-12 — THE SHIP LINE (three rulings, decided in the process-audit review session)
<!-- ck:- status:closed owner:no -->

Body archived in [archive/PLAYTEST_ARCHIVE.md](archive/PLAYTEST_ARCHIVE.md); search `ck-` and this heading.

### ⭐⭐ NEW 2026-08-12 — THE SAVE-RESCUE ARTIFACT: three calls, and the derivation is done

The D13 chain's first prompt has finished the hard agent-side part — the
authoritative exposed-set derivation over BOTH shipped mods, from source, no
inherited count. **27 sites, every one with a disposition.** These three are
yours. Items 17 and 18 were reserved for you on the entry; item 19 is new and
is the one thing the derivation found that I will not decide alone.
Reasoning for all three: **`agent/reports/D13_EXPOSED_SET.md`** (promoted
2026-08-13 to its permanent home — the chain folder it was drafted in is
deleted when the chain closes).

17. ✅ **PUBLISH HALF RULED 2026-08-14: hold off.** Save Rescue is **not
    published at launch** — held in reserve, to be launched **if post-release
    reports show players stuck with the problem it solves** (the dial residue).
    The card stays ready (`RELEASE_DESCRIPTION_RESCUE.md`); item **28** closes
    with this ruling: **ship as built** (re-decide the dialog text before
    upload if the contingency ever fires — including the audit's save-step
    line). ✅ **DECIDED 2026-08-13, your ruling: (c) — the packs are their own
    cleaner; the artifact serves ONLY the already-uninstalled.** You first
    challenged the premise ("nobody but me has ever run the pack — why build a
    cleaner at all?") and then **reaffirmed the 2026-08-01 launch-dependency
    ruling** on the honest version of the case: the population is empty until
    launch and the residue never expires (the tool works retroactively), so
    the real reasons to build NOW are the open sequencing window (derivation
    frozen + QA'd against exactly these trees) and day-one messaging — and
    **build ≠ publish**: whether/when the rescue goes to a store stays a
    release-time call (noted for the release checklist). The ask as it stood:
    ⚖️ **What does the player actually DO with the rescue artifact?**
    (a) run-it-after-removal · (b) keep-it-installed as a permanent runtime ·
    **(c) the packs already clean themselves and the artifact serves ONLY the
    already-uninstalled case ← my recommendation, and the derivation now backs
    it with specifics rather than architecture.** Why (c): the two residues
    that ever *did* anything after uninstall are already healed on load by the
    packs themselves (the meteor thread restarts onto the game's own body; the
    rain loops migrate onto the game's own body). What is left is inert named
    data — **except one thing**: a save made with a drone dial off base keeps
    that boost **permanently** after you uninstall, and a player who has
    already uninstalled cannot run any in-pack pass. That is a real population
    and it is what the artifact is for. **Cost of each option:** (c) is the
    smallest — one load-time pass, no UI, no extra surface; (a) adds an invoke
    path that has to work on a gamepad for console players; (b) is not a
    cleaner at all but a mod you maintain forever, and it re-opens the "what
    does *it* leave in the save" question we just closed. ⭐ Under (c) the
    artifact may end up with **no thread surgery whatsoever**, which would make
    it markedly smaller and safer than every earlier sizing — one open
    question in the derivation decides that, and the QA prompt attacks it next.
    **QA update (2026-08-13): the attack ran, and the answer is "smaller, but
    not zero."** The derivation held up everywhere else, but "no thread
    surgery" only covered saves the *current* pack has touched — the rescue's
    real audience includes people who uninstalled an **older** version, whose
    saves can still carry a dead meteor timer or an old rain loop. The QA
    verdict keeps two small, one-shot repairs in the plan (both re-use the
    game's own machinery; the meteor one costs a one-time timer re-roll, which
    the tool will say out loud). **Nothing about the (a)/(b)/(c) choice
    changes — (c) is still the recommendation.**

18. ✅ **DECIDED 2026-08-13: CONFIRMED — mod-shaped.** Same day you also
    **ratified the naming proposal** (display "Save Rescue" · repo
    `SMR-SaveRescue` · mod id `SMR_CommunitySaveRescue` · log tag
    `[CommunitySaveRescue]`) and **pre-created the public remote yourself**:
    `github.com/catt144/SMR-CommunitySaveRescue`, empty — prompt 3 scaffolds
    into it (note: the remote's name differs from the proposal's repo folder
    name; prompt 3 aligns the local folder to the remote). Publishing the MOD
    to a store stays a release-time call. The ask as it stood:
    ⚖️ **Confirm the artifact is built AS A MOD (not a console procedure) —
    and that this makes the channel question stop blocking.** I verified the
    argument against your own Paradox Mods check (2026-08-01), not from
    assumption: that audience has no console, so a rescue path that means
    typing commands reaches **nobody** there — while a mod-shaped cleaner
    installs through whichever channel the player already uses, on PC and on
    Xbox/PS5 alike. Its reach is a strict superset on every platform, so
    "which channel do we publish to" no longer changes what the artifact *is*.
    **Recommendation: confirm mod-shaped**; it costs a third small repo (I have
    the scaffolding proposal ready, deliberately thinner than the opt-in
    pack's — no options page, no toggle machinery). ⚠️ Channel note, separate
    and still open from your own browse: searching Paradox Mods for `bug` or
    `fix` returned **zero** hits while searching your author name worked — a
    naming/listing problem for the store page, never re-checked, not a code
    one.

19. ✅ **DECIDED 2026-08-13: GO — build the three gates in-pack. ✅✅ DONE the
    same day** — all three gates inserted (`Fix_CrystalMysteryHang:78`,
    `Fix_ExtenderFlapChurn:96`, `Fix_TrackConnectorPingPong:179`), the four
    modules' save-footprint disclosure rewritten, parse sweep and doccheck
    GREEN, module/file/probe counts unchanged. **Nothing for you here** — no
    behaviour change while installed and nothing to look at in game; the gates
    only matter in a save the pack has been removed from. One thing found on
    the way and NOT changed, disclosed in the code and routed to the next
    prompt: after a load, the crystal repeater restored with the save cannot be
    stopped by the handler that stops the fresh one, so during that mystery the
    hourly re-announce can double up — inert (the message has exactly one
    listener, which wants it), unmeasured. The ask as it stood:
    ⚖️ **Three of our own background threads have no "the mod is gone" exit,
    and I want to fix that in the packs before building any cleaner.** The
    rule we wrote says every mod-owned background body must check whether the
    mod still exists each time it wakes. One of four does
    (`MeteorStormWedge`). The other three — the crystal-mystery repeater, the
    extender-flap debounce, the track-connector reclaim — are written entirely
    in the game's own vocabulary, which under the corrected rules is exactly
    the case that **keeps running after you uninstall** rather than stopping.
    Worst case today is small and not an error (the crystal one re-broadcasts
    a message hourly for up to 10 sols in a save we no longer occupy), but it
    is undisclosed, and a cleaner cannot reach it by construction — those
    bodies run *from* the save the moment it loads. **Recommendation: build
    the fix in-pack now — three one-line insertions, no behaviour change while
    installed, no new save state, one short prompt inserted before the build
    step.** Our own policy bars handing this to the cleaner instead ("the
    cleaner is not a scoping escape hatch" — your words). Say go and it rides
    the chain; say no and all three get recorded as accepted residue instead.

26. ~~**⚖️ ONE 15-SECOND ACTION: tick "Save Rescue" and restart**~~
    ✅✅ **DONE BY YOU 2026-08-13 at 11:16, and the tool has now been TESTED on
    the back of it. Nothing here is owed from you any more.**
    Your tick is in the game's own log (`SaveRescue: ready`), and the whole
    verification ran unattended off it: **nine launches, about eight minutes of
    machine time, zero minutes of yours.**
    ⭐ **What it actually did, on a real save carrying real leftovers:** it
    removed **1617** items across all eleven names it targets — including both
    Drone dials, the ones that otherwise keep boosting your drones forever with
    the mod gone — **kept both of the leftovers that ARE repairs** (the Wind
    Turbine buff and the track latch), restarted a stalled rain cycle and a dead
    meteor timer, and left **nothing of its own** anywhere in the save. Loading
    the cleaned save a second time it correctly did nothing at all. No errors in
    any cell.
    ⚠️ **One honest caveat, and it is small.** We claimed the tool leaves "zero
    lines" behind once removed. Measured, there is exactly one — the game itself
    notes `Savegame references Mod Save Rescue … which is not present` on the
    first load after you uninstall it. **This is not special to this tool: the
    Fix Pack and the Opt-In Modules do exactly the same**, and the note
    disappears the next time you save. It will be said plainly in the mod's
    description rather than papered over.
    ✅ **RULED 2026-08-15: the display name becomes "Community Fix Pack: Save
    Rescue" — pre-approved, applied only IF the tool ever publishes** *(the
    family prefix was renamed by your 2026-08-17 ruling, item 36, so the name
    to apply at publish is now "Relaunched Fix Pack: Save Rescue")*. Your
    words: *"This is fine for if we ever need it."* ⛔ **Deliberately NOT applied
    today:** item 17 holds the tool unpublished, so the rename rides the
    pre-upload pass that the contingency already mandates — the same pass that
    re-decides item 28's dialog text and adds the audit's missing save-step
    line. Recorded at the point of use in the rescue card's header so it cannot
    be forgotten there. One line in one file when the day comes.
    ~~the display name is **"Save Rescue"** as you ratified it, but the same day
    you renamed the opt-in mod to *"Community Fix Pack: Opt-In Modules"* so the
    family sorts together in mod lists.~~
    ⚠️ **Your rig is exactly as you left it** — both packs back at `74/74` and
    `8/8`, drone dials still `5x` / `+2`, all seven opt-in toggles still on, and
    every save you own byte-identical (the four protected ones were MD5-checked
    either side). Save Rescue itself is installed but **not** loaded, by design:
    it is a repair tool, not a standing mod, and leaving it out costs you
    nothing — measured, a pulled mod produces no log line at all.

### ⭐ NEW 2026-08-13 — public documentation: platform decided, one question back to you
<!-- ck:- status:closed owner:no -->

Body archived in [archive/PLAYTEST_ARCHIVE.md](archive/PLAYTEST_ARCHIVE.md); search `ck-` and this heading.

### ✅✅ 2026-08-13 — public documentation, part 2: ALL FOUR DECIDED, same day

The `public-docs` chain's design prompt is done and **you cleared every item it
routed, in one sitting.** Full reasoning: `agent/reports/PUBLIC_DOCS_DESIGN.md`.
⭐ **Nothing in this section is owed by you any more.** Item 24 now records the
completed preview floor and points at the separately owner-retained screenshot
follow-up; this section remains the owner-decision record.

22. ~~**⚖️ The "judgment calls" wording — DRAFTED, so you approve rather than
    compose.**~~ ✅✅ **DECIDED 2026-08-13: the five bullets SHIP as drafted
    (`PUBLIC_DOCS_DESIGN.md` §9), and the closing line is CUT.** Open since
    2026-08-04; closed after nine days.
    ⭐⭐ **AND YOU CAUGHT A FALSE CLAIM DOING IT.** You challenged the line that
    said the five could each be switched off individually on PC — *"as far as I
    know right now, we have no way to switch off parts of the fix module"* —
    and you were right. What the code says, checked in response:
    * The per-fix veto **is real** and would fully disable all five. But it is
      read at mod load (`00_Core.lua:384-388`), so it only works from **a
      companion mod that loads before ours** — a modder's tool, not a player's.
    * ⛔ **The developer console does NOT work.** By the time anyone can type,
      the fixes are already applied.
    * ⛔ The fix pack has **no Mod Options page** — everything settable moved to
      the opt-in mod at the split, and none of these five are in it.
    ⛔⛔ **The consequence, and it is bigger than the cut line.**
    `archive/MOD_DESCRIPTION.md:487-493` — the frozen text the real store page
    gets built from — tells players to set the veto *"in the console"*. **That
    is false and it would have shipped.** It is now recorded as a correction the
    chain's build prompt must make (§9.1). ⚠️ **Second false claim found in that
    one file** after the F76 explainer; everything else in it is now treated as
    unverified until re-checked.
    ⭐ The standing lesson written down from this: *a claim about what a player
    can DO needs a route check, not a source citation.* The sentence had passed
    a design pass, that file's own review and a chain QA before your instinct
    caught it.
    ⚠️ **AMENDED 2026-08-13 by the QA prompt** — you were right about the *each*,
    and the answer we wrote back was slightly too broad in the other direction.
    Re-reading all five modules: `F97` (dust devils) **can** be switched off from
    the console mid-session, because it re-checks the switch every time it runs.
    The other four cannot. **Nothing you decided changes** — the store page still
    will not offer the console route, because it works for an unpredictable few
    and a player has no way to tell which. Recorded so the file is not wrong.

22b. ~~**⚖️⚖️ ONE LINE FROM YOU — a factual error inside a sentence you already
    approved, and it points the warning at the wrong players.**~~ ✅ **DECIDED
    2026-08-13, your words in the build session: *"You can change any wordings
    to their accurate versions."* SHIPPED as the phrasing you approved on
    08-02 — "on some map settings"** — now the fifth judgment-call bullet in
    the fix pack store description (`agent/reports/STORE_FIXPACK.md`), with
    the six-row rate table recorded beside it per the process rule below.
    The terminal audit re-derived the bullet from the entry's own table
    (`agent/bugs/F97.md`: the heaviest preset is the one that does not change
    at all; the increases land on the light and middle presets; and the OG
    disassembly shows the defect spans both games, so "than the game has ever
    actually delivered" holds) and sustained the shipped wording. "Most map
    settings" was deliberately NOT used — truer-sounding, never approved.
    The original ask, kept for the record:
    ⛔ Not a
    re-litigation: the fifth judgment-call bullet's **substance is right and
    stays**. One phrase in it is backwards.
    * **What it says now:** *"On the heaviest settings that means noticeably
      more dust devils than the game has ever actually delivered."*
    * **What the numbers say** (the per-fix rate table, re-derived from our own
      entry): the **heaviest** setting is the one that does **not change at
      all**. The settings that change most are the light and middle ones — about
      half again as many devils on the common ones, and more than double on one.
    * **How it happened:** an earlier report of ours said "the default preset is
      untouched", the draft trusted it, and the wording drifted from the phrase
      that was actually approved back on 08-02 — *"on **some map settings**"*.
    * ⭐ **Recommendation: go back to "on some map settings."** It is the
      approved phrasing, it is true, and it is shorter. **Say the word and an
      agent strikes this line.**
    ⚠️ **The process point, which matters more than the sentence.** This is the
    second time in a week a decision reached you as *wording with its evidence
    left behind* — the console line was the first, and you caught that one by
    instinct. Nobody caught this one, because it sounded like the phrasing that
    had already been approved. ⇒ **From now on a wording decision comes to you
    with its evidence beside it** (here: the six-row rate table would have
    settled it in ten seconds). That is now written into the chain.

22c. ~~⚖️ **YES/NO — do we owe a page to the player whose game is broken and who
    thinks it is us?**~~ ✅ **DECIDED 2026-08-13: YES, as a small section** —
    written into prompt 5's brief (`agent/prompts/public-docs/05_BUILD_SITE.md`
    job 4). The original ask: The QA review found this is the one reader our whole
    surface plan has no home for. They arrive annoyed and want three things:
    *is it you · how do I get you out · where do I tell you*. Today the honest
    answer to the middle one is "remove the whole mod and restart", and it is
    written down nowhere a player would look.
    * **Cost:** ~1 agent hour, one short page on the site. **No cost to you**
      beyond this yes/no.
    * ⭐ **Why it may be worth more than it costs:** this is the reader who
      writes the negative review, and they write it from whatever they could
      find in five minutes.
    * **Recommendation: yes, but as a small section rather than its own page** —
      it is three answers, not a chapter.

22d. ~~⚖️ **ONE WORD APPLIES EIGHT CORRECTIONS; ITEM 9 IS A SMALL CHOICE.**~~
    ✅ **DECIDED 2026-08-13: batch APPROVED, and 9(a) chosen — all nine
    corrections are APPLIED to `STORE_FIXPACK.md` / `STORE_OPTIN.md`, doccheck
    GREEN, same session.** The terminal audit re-ran the store sweeps with
    fresh eyes and found nine claims the six build sweeps missed — none
    re-opened anything you decided; every one was a sentence saying more than
    its record supports, each re-derived from code or the entry before it went
    on this list. The list as it was put to you, kept for the record:
    1. Fix pack, twice: *"an official patch that repairs a bug retires our
       version"* — only true when the patch changes the code's shape; our core
       says self-checks **cannot** notice a same-named function edited in
       place (`00_Core.lua:492-497`). Fix: the conditional already live in
       `metadata.lua` — stands down *"if an official patch changes what it was
       written for"*.
    2. Fix pack, drones example: *"a landed rocket cancelled the orders…"* —
       `F50` scopes the defect to **automatic** rockets. Fix: one word.
    3. Fix pack, twice: *"**several** of the stamps clear themselves the next
       time you save"* — exactly **two** do (`D13_EXPOSED_SET.md` §2b D1/D2).
       Fix: "a couple".
    4. Opt-in, Nursery/Retirement policy: *"A new toggle row on **every**
       dome"* — the row deliberately does not exist on domes without cohort
       housing (`Opt_NoHomeless.lua:650-656`), and its Ctrl+click deliberately
       applies to every *such* dome, not everywhere (`:712-732`). The phrase
       is true for the Residency row; the Nursery block copied the phrase, not
       the behaviour. Fix: "on every dome that has a Nursery or Retirement
       Home", "applies it to every such dome".
    5. Opt-in, same block: the quoted row text `off (3 would move)` is not
       what the UI shows — the real title is *"Nursery / Retirement Dome
       (3 would move)"* → *"(3 moving out)"* (`Opt_NoHomeless.lua:700-702`;
       the page matched the design record, the code had moved on). Fix: quote
       the real strings.
    6. Opt-in: *"Seniors and Children stay, even while homeless"* — under
       Forever Young / "Put Them To Work", an **unemployed** Senior is
       workforce and IS movable, on purpose (`Opt_NoHomeless.lua:140-150`:
       "in such a colony a jobless Senior is not a retirement signal"). Fix:
       one clause carving out senior-work colonies.
    7. Both texts: the dial uninstall recipe never says **press Apply** — the
       dials only change on Apply or load (`Opt_DroneStatDials.lua:142-149`);
       a player who sets the dropdowns and backs out of Options has cleared
       nothing, then saves, then uninstalls, and keeps the boost the warning
       exists to prevent. Fix: "(press Apply)" inside both recipes.
    8. Opt-in, Multiple Suns: *"solar panels only ever check the first sun"* —
       the recorded defect is one-directional (`F39`: panels **built** near a
       second sun never bind; the reverse direction works). Fix: "panels
       built near a second sun never connect to it".
    9. ⚖️ Opt-in, drone dispatch overhaul — the page states *"repair and
       cleaning jobs go to the closest hub's fleet first"* as delivered
       behaviour. The only A/B (PT-52 B2) measured the gate firing **once in
       25 malfunctions** — the entry's verdict: *"the claim gate did
       essentially nothing"*, because resource-needing repairs go to the
       **delivering** drone before dispatch ever runs — and you ordered a v1
       rebuild 2026-07-31 (`D06.md:46-69`). "Experimental" is kept, but it
       discloses immaturity, not a measured null.
       * **(a) Recommended:** keep the mechanism claims, add one honest
         sentence — most repairs are decided by who delivers the parts, which
         this module leaves alone; it matters most for repairs and cleaning
         that need no resources.
       * **(b)** Leave it until the rebuild lands and rewrite then.
    ⚠️ Noted for awareness, no action owed: every console/controller route in
    both texts is source-derived, none play-verified (the build ledger says
    the same); and "back it up" names no backup route a console player can
    walk — the honest console form, if you want it, is "make an extra named
    save first".

23. ~~**⚖️ Folders in this repo that aren't part of the mod are currently going
    into what players download — including `CLAUDE.md`.**~~ ✅ **DECIDED
    2026-08-13, your ruling: YES, add the missing patterns — AT LAUNCH PREP.**
    Recorded on the release step list so it lands in the same pass that bumps
    the version and refreshes `last_changes`. ⛔ **All THREE mods**, including
    the rescue mod, whose `metadata.lua` nobody has checked for this yet.
    Nothing owed by you. The finding as it stood:
    Found while checking
    something else for item 21, and I did not fix it because it is a code change
    and outside that chain's fence.
    **What I verified, in the game's own source:** uploading a mod runs
    `CreatePackageForUpload` (`ModTools\Src\CommonLua\Classes\GedModEditor.lua`
    `:678-741`), which lists **the entire mod folder recursively** and packs
    every file that does not match one of the `ignore_files` patterns in
    `metadata.lua`. We ignore eight patterns: `.git`, `.svn`, `Source`,
    `SourceData`, `docs`, `.claude`, `README.md`, `.gitignore`.
    **What that misses today:** `tools/`, `CLAUDE.md`, `LICENSE`,
    `.gitattributes`, in every mod repo — and now that there are three mods,
    the rescue mod's own `metadata.lua` has never been checked for this at all.
    ⭐ **The docs site used to be on this list and no longer is** — it moved to
    its own repo the same evening (item 21), which is the one part of this that
    fixed itself. The rest did not.
    None of it *runs* — only files listed in `metadata.lua` execute — so
    nothing is broken and nothing is a security problem. But `CLAUDE.md` is
    agent instructions, and shipping it inside a player's download is the exact
    "player lands in our working notes" problem the whole docs-site design
    exists to prevent, just delivered to their disk instead of their browser.
    ⚠️ **One sub-case I could NOT verify:** whether `.github/` slips past the
    `.git` pattern depends on an engine function with no readable source. The
    other four match nothing under any reading.
    **Recommendation: add the missing patterns to both repos' `ignore_files` at
    launch prep** — a handful of lines, no behaviour change, no new save state.
    ⇒ **Your job: a yes.** If you would rather ship them, that is fine too and
    I will record it; I would just rather you chose it than inherited it.

24. ~~**⚖️ Preview art ×2 (×3 if the rescue tool publishes)**~~ ✅ **DECIDED
    2026-08-13, your ruling: BUILD A PLAIN TREATMENT NOW AS A FLOOR; DONE
    2026-08-14.** Final fix-pack and opt-in art lives under
    `agent/reports/preview_art/`; the selected fix-pack image shipped as root
    `preview.png` (`RELEASE_PORTAL_PREP.md`). It remains a floor, not a ceiling.
    The separate screenshot sitting is still owner-retained (2026-09-09: "we
    may get to it"), but it no longer carries preview-art work. The reasoning as
    it stood:
    Routed NOW
    because it is the only launch item with no ceiling. Everything else in
    the public-docs plan is agent hours or a decision from you; the preview
    image is neither. It does not get better with agent time, it is not a
    screenshot, and it is the first thing anyone sees on a store card.
    **Constraints already on record:** Paradox Mods ≤ 2 MB, Steam ≤ 1 MB.
    **The options, priced honestly:** make them yourself · commission them ·
    or ship a plain text-on-image treatment that is *fine* and takes an hour.
    ⚠️ There is no recommendation here because it is a taste-and-budget call,
    not a technical one. The reason it is on your list today rather than at
    launch is simply that the other three items have known endings and this one
    does not.
    ⭐⭐ **OVERTAKEN AFTER THE 2026-08-13 PLAN:** the preview floor was produced
    without a game capture, and the D13/hotfix sittings closed. The retained
    `agent/prompts/CAPTURE_SITTING.md` now owns only the still-unfired screenshot
    work and revalidates current consumers and fixtures before a launch.

25. ~~**⚖️ How one of our own research files talks about real modders**~~
    ✅✅ **DECIDED 2026-08-13, your ruling: BOTH EDITS — ✅ DONE the same
    minute.** `BUG_LIST_AUDIT.md`'s heading now reads **"Not used as sources,
    and why"**, and *"an aggregator repack"* now reads *"aggregates other
    authors' fixes"*. **Every assessment is byte-unchanged**; only the verdict
    tone went, and the reworded heading carries a short note saying why so no
    future session reads it as a softening of the findings. Nothing owed.
    ⭐ The related standing rule needed no decision and is now recorded
    (`PUBLIC_DOCS_DESIGN.md` §7): the public pages credit other authors
    generously, never say what another mod gets wrong, and never say
    "this fixes what mod X doesn't". The ask as it stood:
    `agent/reports/BUG_LIST_AUDIT.md:355-370` lists modders under a heading
    reading **"Rejected (with reasons)"** — `LukeH`, `Ayzo`, `Fizzle Fuze`,
    `Silva/Dash`, `Thorik`, `akarnokd`, `FirestormMk3`.
    **I read the whole section first, and in context it is fair and accurate.**
    "Rejected" means *rejected as a source of bug reports for our list*, not
    "bad mod" — and the surrounding text is generous (`fredware` is called "the
    one to watch"; `LukeH`'s entry credits a genuine fix mod). **Nothing in it
    is untrue and nothing in it is hostile.**
    **Three things still bother me:** the header word reads harshly to anyone
    who lands on that line without the paragraphs above it · "an aggregator
    repack" is a loaded phrase for a factual observation · and ⭐ **`Silva/Dash`
    is the author of the GitBook site you pointed me at as the model for this
    whole documentation chain.** These repos are public on purpose and we are
    about to send players to them, so "will they ever read it" is not
    hypothetical.
    ⚠️ The file is in `reports/`, not `archive/`, so it can be edited — this is
    a live decision, not an academic one.
    **Recommendation: two edits, no facts touched** — retitle *"Rejected (with
    reasons)"* → *"Not used as sources, and why"*, and change *"an aggregator
    repack"* → *"aggregates other authors' fixes"*. Every assessment stays;
    only the verdict tone goes. ⇒ **Your job: yes, no, or your own wording.**
    ⭐ Related and *not* needing a decision from you: the design also proposes a
    standing rule for how the public pages talk about other people's mods —
    credit generously, never say what another mod gets wrong, never
    "this fixes what mod X doesn't". Recorded in §7; say the word if you
    disagree.

> ⛔ **Nothing owed by you in this note — it is here so the pending change is
> visible somewhere you read.** `STATE.md` does not yet mention the public-docs
> chain, and I deliberately did not add it: that file is capped at 60 lines,
> sits at 60/60, and the D13 chain is editing it right now, so two writers means
> one of us silently deletes the other's line. **The line I want added**, once
> D13's chain is quiet: *"⑤ **public-docs chain** — design DONE 2026-08-13
> (`reports/PUBLIC_DOCS_DESIGN.md`); next `02_QA.md`. Platform Pages ✅,
> topology ⚖️ck21. Feeds ③."* **What I would drop for it if the cap binds:** the
> `⛔ Pre-split 82/75/8 … ERA-STALE` sentence — it exists only to stop someone
> quoting three superseded number triples, and both places those numbers are
> now read from re-derive them instead. The next prompt in the chain lands it.

### ⚖️ NEW 2026-08-13 — your Steam ID is scrubbed from the live docs, but NOT from git history
<!-- ck:- status:closed owner:no -->

Body archived in [archive/PLAYTEST_ARCHIVE.md](archive/PLAYTEST_ARCHIVE.md); search `ck-` and this heading.

### ⛔ NEW 2026-08-12 — I DELETED ONE OF YOUR AUTOSAVES. Telling you straight.
<!-- ck:- status:closed owner:no -->

Body archived in [archive/PLAYTEST_ARCHIVE.md](archive/PLAYTEST_ARCHIVE.md); search `ck-` and this heading.

### ⭐ NEW 2026-08-12 — asteroid Exotic-Minerals freeze (decided in-session; one owed minute)
<!-- ck:- status:closed owner:no -->

Body archived in [archive/PLAYTEST_ARCHIVE.md](archive/PLAYTEST_ARCHIVE.md); search `ck-` and this heading.

### ⭐ NEW 2026-08-12 — raised by you mid-sitting during `corun-pt60`
<!-- ck:- status:closed owner:no -->

Body archived in [archive/PLAYTEST_ARCHIVE.md](archive/PLAYTEST_ARCHIVE.md); search `ck-` and this heading.

### ⭐⭐ NEW 2026-08-11 — from the `corun-pt15` SITTING (two calls, both yours)
<!-- ck:- status:closed owner:no -->

Body archived in [archive/PLAYTEST_ARCHIVE.md](archive/PLAYTEST_ARCHIVE.md); search `ck-` and this heading.

### ⭐⭐ NEW 2026-08-10 — from the `corun-batch-2` SITTING (four calls, all yours)

**Cost, stated honestly: the brief promised 33–36 attended minutes and it took
about 75.** All seven legs ran and nothing was cut. The overrun is ours and it
is itemised — a keybinding the brief invented, three broken readers in one
function, a save witness that stopped witnessing, a leg that had to run twice
because it took no reading before its own save, an uninstall that needed a
restart nobody knew about, and one console line of mine that produced nothing.
**Your three deviations all bought evidence and none is scored against you.**

⭐ **What went right, so the list below reads in proportion:** the popup-audit
keystone is ANSWERED (a storybit popup survives a save/load *and* still applies
its outcome when you answer it afterwards), F21's fix was WITNESSED firing on a
real boarding, PT-47 passed every check it could sample, F99's last untested
cell is filled, and **`PT35FIXTURE.savegame.sav` now exists in your save folder**
— keep it, it unblocks a test that has been stuck since 2026-08-04.

5. **⚖️ `F85` — the defect is real, and the route we told you about doesn't
   exist. What do you want done?** A save **landed 39 seconds inside the open
   breakthrough-choice popup**, and reloading it **voided the choice** — popup
   gone, breakthrough never discovered. So the entry is right that the save
   system doesn't protect you. **But the entry's route is dead:** it said "rebind
   Quick Save to F9", and you established there is no save action in the
   key-bindings screen at all. The entry's own fork only has two outcomes
   ("R2-by-rebind" or "drop to I/R4, documentation") and **neither fits** — the
   defect is real and unreachable by the one route anyone had named.
   **Your call: severity, and whether anything gets built.** ⚠️ The half worth
   your attention now is the **distress-call popup** (audit §3.6) — it's the
   game's one popup that *doesn't* pause, so it's the only place a normal
   autosave could land inside a popup window with no rebind involved. That
   rider didn't run. → `agent/bugs/F85.md`.
   ⚖️ **2026-08-11 — you challenged the "no quicksave on retail" claim and the
   challenge holds: STILL OPEN by your call.** The only *sampled* fact is that
   the bindings screen has no save row. Source (including the generated
   executable) says the one Quick Save action is **Ctrl-F9** and only exists
   when `Platform.cheats` is on — but that's an inference chain, and nobody
   has ever pressed Ctrl-F9 on retail. **The 10-second check rides your PT-20
   redo sitting**: press Ctrl-F9 in a colony — a quicksave landing makes the
   default binding a live route into this defect and changes the whole
   disposition; nothing happening confirms the source read. Decision waits.
   ⭐ **Re-routed 2026-08-11 (your corun-pt15 order): the Ctrl-F9 check now
   rides the PT-15 sitting** — any colony works and it answers sooner. The
   PT-20 redo is unchanged otherwise.
   ⛔⛔ **2026-08-15 — ANSWERING YOUR "quick playtest?" QUESTION: NO, AND THERE
   CANNOT BE ONE.** The distress dialog is the last reachable surface this entry
   had, and today's route check found it is **dead-coded out of the shipped
   game** — its only caller is a button the executable compiles behind
   `local cond = false` (full derivation: item **31** above, and `F85.md`
   §2026-08-15 later). It cannot be reached by playing; the only way to put it
   on a screen is an agent console-call, which would prove the wrapper works and
   say **nothing** about retail play. So a sitting buys no knowledge here, and I
   am not proposing one.
   ⇒ ⭐ **The severity question is now answerable on evidence instead of taste,
   and every route into this entry's harm is closed:**
   * the breakthrough and Assembly popups **pause**, so no autosave can land in
     them;
   * there is **no save action on retail at all** (`idQuickSave` compiled out —
     your check, 08-11);
   * the one non-pausing popup is **dead-coded** (this finding);
   * and our wrapper pauses it anyway if a patch ever brings it back.
   ✅✅ **RULED + CLOSED 2026-08-15 with item 31: LEAVE it at `P3` / LATENT / tier U.**
   ⇒ *Recommendation as it stood:* **LEAVE it at `P3` / LATENT / tier U.**
   The label is now exactly right: the defect is real and reproducible (a save
   *was* landed inside a popup and *did* void the choice), and it is
   unreachable by any player route. Bumping it would overstate; dropping it
   would understate a reproduced fault. **One word from you closes this.**
   ✅ Item **31** is ruled and applied too — the module is removed and shelved,
   and both player-facing pages are corrected. **Nothing is owed on F85.**
   ✅✅ **THE CHECK RAN 2026-08-11 IN THE PT-15 SITTING — Ctrl-F9 IS NOT A
   ROUTE, and you were right to make us press it.** You pressed it; nothing
   happened on all three witnesses (no new save file, no `Game saved:` or
   `Save failed:` line, nothing on your screen). But three absences aren't a
   mechanism, so we took a structural read instead: **the Quick Save action is
   never built on retail.** `Platform.cheats` is falsy, so the block containing
   `idQuickSave` never runs — and `idQuickSave` reads `nil` against **437
   actions, 433 with ids, with the lookup proven working on a known-present
   id**. There is no save-the-game action in the entire set; the only
   `save`-ish entries are map/camera editor tools. ⚠️ Note the save was **not**
   refused — `CanSaveGame()` came back truthy. The action simply isn't there.
   ⇒ **your original challenge is fully vindicated and the observation is
   closed. Only the disposition is still yours** (severity, tier, whether
   anything gets built).
   ⭐ **Prep 2026-08-11 — the check now has three witnesses instead of one, so
   "nothing happened" will be a measurement rather than an impression.** (1) a
   new save file appearing in the save directory, which we list before and
   after; (2) the game's own log line — the quicksave routine prints either
   `Game saved: <name>` or `Save failed: <err>`, so **either line falsifies the
   source read**; (3) your eyes on the quicksave loading screen. Expected file
   name if one lands: `QuickSave.savegame.sav`. **Still your decision either
   way** — the sitting brings evidence, not a verdict.
   ✅✅ **DECIDED 2026-08-12 — BUILD THE `dont_pause` FLIP (your pick, on your
   own proposed fix).** You asked the question that found the better repair:
   the distress-call dialog is the game's ONLY non-pausing popup, and flipping
   it to pause like every other popup closes F85's entire remaining reachable
   surface in one property change (no autosave can land, nothing can queue
   behind it). Built as a chained wrapper, disclosed as a design-judgment
   tweak; queued into the next unattended build chain with its verification
   launch. The bigger per-site rewrite was declined; the distress-call watch
   rider below retires when the fix verifies.
   ✅✅ **BUILT AND VERIFIED 2026-08-15 (`unattended-3`, owner cost zero), and
   the terminal audit sustained it the same day.** The flag was read cleared
   in two real launches (once on a flattened tree after your own 47 MB colony
   copy loaded), an already-pausing popup untouched, a flagless popup left
   alone, the pass idempotent; the suite passed 80/0/16/0 of 96 around it. The
   §3.6 autosave rider is retired on its own condition. The entry carries
   **`tested-unattended`** under your 26b vocabulary — nothing here claims
   anyone watched a clock stop. ⚠️ **The screen-witness add-on this line once
   promised is MOOT by item 31**: the dialog is dead-coded on retail, so a
   screen witness could only be a console-raise that proves the wrapper and
   says nothing about play — item 31 owns the consequences.
   **Still yours here: severity/tier only** (rec on STATE: leave `P3`/latent-U
   — the defect's one reachable half is repaired, the rest was never reachable).
6. ~~**⚖️ Disabling a mod needs a full game restart — does `PT-20` need
   redoing?**~~ ✅ **DECIDED 2026-08-10 — REDO NOW.** A dedicated PT-20 redo
   co-run is queued (your part: the Mod-Manager disable click, a **full game
   restart**, ~10 min of ordinary play; save/reload/log reads are rig-side).
   Its result supersedes the old 98-vs-98 comparison, which may have measured
   the half-disabled middle state. → `agent/bugs/D13.md`, PT-20 section below.
7. ~~**⚖️ Our save-folder cleanup has now failed twice, and we may know
   why.**~~ ✅ **DECIDED 2026-08-11 — KEEP DELETING + VERIFY.** Agent saves
   keep dying in their recording commits; the close-out directory listing
   (now a standing WORKFLOW rule, and it held on the audit's re-check — none
   of the 15 returned) verifies each deletion stuck. The Steam-Cloud
   hypothesis stays parked: if a deleted save ever returns again, that run
   tests it. → WORKFLOW "Co-runs" close-out rule.
   ⭐⭐ **AND ONE RETURNED — 2026-08-11, so the parked hypothesis is now TESTED
   and CONFIRMED. Fourteen of them returned, at the next launch, written before
   the game process even started.** Your decision above was right about the
   listing (it is what caught this) and wrong only in what the listing could
   prove: it establishes that the deletion HAPPENED, never that it held.
   Nothing about the rule changes; a tick of yours removes the cause. See the
   two-ticks block at the top of this file and `agent/facts/EF-051`.
8. ~~**⚖️ There is uncommitted work in the repo that isn't ours, including an
   answer of yours nobody recorded.**~~ ✅ **CLOSED 2026-08-11** — the
   uncommitted work landed in the sitting's commit, and you CONFIRMED the
   typed line as your D07 ruling (item 2 above). Recorded on
   `agent/bugs/D07.md`; nothing further owed.

**⚖️ What the audit changed (2026-08-10, terminal audit of the sitting — every
verdict above SUSTAINED; four corrections to the record, none of which flips a
result):** the "unattributed modal" at ~16:02 **is in the log** — it was the
keystone test's own first storybit, whose popup was answered after a reload
(the sitting's "it's in no log" was wrong; run 1 stays void, run 2 carries the
pass). The mid-sitting instrument recorded as "produced zero output" **did
print** — the game only flushes its log tail at exit, so the check couldn't
see it (that flush behavior is now a recorded fact). The keystone's run-1 gap
was ~15 minutes, not ~8. And prep's wrong "0 defence towers" figure was NOT
inherited from batch-1 — prep re-read it live through the same broken reader.
⭐ One NEW find from reading the whole log: a single vanilla engine error line
during the bombardment window (a rocket departure hitting an invalid station
position) — filed as `C45`, one occurrence, nothing owed from you.

### ⭐ NEW 2026-08-05 — from the `corun-batch-1` sitting (four calls, all yours)

**Cost: the brief promised ~24 attended minutes and the sitting ran about two
hours — but you ruled that this one is not scored against the estimate**, since
the excess was your own deliberate deviation to chase F99 and the dev-cheat
leads (which is where `F101` came from). Recorded as an **owner override** in
the audit. The one piece it does *not* cover is still logged as a real miss:
**M1 was budgeted 3 minutes and took ~25**, because prep's measured fixture had
evaporated and it had to be built live.
→ `agent/prompts/corun-batch-1/03_FABLE_AUDIT.md` §8.

1. ~~**⚖️ Does PT-37's result unblock F48?**~~ ✅ **DECIDED 2026-08-11 — SHIP.**
   The evidence beat the criterion: case A removed a real stale connection
   from your own save lineage and survived reload; case B's assert is
   measured unreachable by meteor. The corrected pass is queued into the next
   unattended chain; PT-35's do-no-harm run covers it in the same launch.
   → `agent/bugs/F48.md`.
2. ~~**⚖️ Should pinning a colonist to a residence also pin them to their
   dome?**~~ ✅ **DECIDED 2026-08-11 — NO DOME PIN**, your 2026-08-10 line
   confirmed as the ruling: *"It should not pin them to the dome, seems like a
   risk for a bunch of weird bug cases."* The module's deliberate split
   stands; no code change. → `agent/bugs/D07.md`.
3. ~~**⚖️ How much do the two new dev-tool defects matter?**~~ ✅ **DECIDED
   2026-08-10 — OUT OF SCOPE, `F101` is `wontfix`. Nothing gets built.** Your
   ruling, in your own words: *"If it works fine from what we can tell in dev
   mode then its not in this mods scope. If a modder wants to build out a
   toolkit for users then that should be something they fix."* ⭐ **What the
   session found before you ruled, because it is the reason the question was
   answerable at all:** neither throw is *possible* on a build where those
   buttons belong — `TestMeteor` is missing precisely because `Platform.cheats`
   is false, and `GetSpotNameColor` precisely because the `DevToolsPublic`
   library is absent — so there is nothing to reproduce in dev mode. On retail
   the button only executed because the engine's own gate passed first
   (`ObjCheat CheatMeteorHit` prints one line ABOVE each throw), and that gate
   is `Platform.cheats or AreModdingToolsActive()` — so a **Ged mod-tool window
   was open**, the same state that blocks achievements. ⛔ **And it was not our
   TestKit forcing it:** the kit enables only the console, which is not part of
   that gate, and neither repo writes the cheat flags at all. Pressing them
   damages nothing (the meteor button throws before it runs anything, under
   `procall`; the spot toggle only leaves its own dev-UI state one click out of
   phase). → `agent/bugs/F101.md`, "The reachability gate".
   **The dev-tools-for-players idea is parked** in
   [FUTURE_IDEAS.md](FUTURE_IDEAS.md) as a SEPARATE post-launch mod — not this
   pack, and not work.
4. ~~**⚖️ `Opt_NoHomeless` self-deactivates at the main menu**~~ ✅ **DECIDED
   2026-08-10 — the F100 hold is LIFTED and the repair is the reason-string
   fix ONLY** (the log line stops crying wolf; the preflight target stays as
   is until D12's own review settles). Queued with the C43 TestKit fix into
   the next unattended chain, which verifies both against a live boot.
   → `agent/bugs/F100.md`.

### ⭐ NEW 2026-08-10 — from `corun-batch-2` prep (nothing needs your call; two are cleanup already done)
<!-- ck:- status:closed owner:no -->

Body archived in [archive/PLAYTEST_ARCHIVE.md](archive/PLAYTEST_ARCHIVE.md); search `ck-` and this heading.

## Do first — the campaign's ordered top (chain-12 QA, `agent/reports/CHAIN_QA_REPORT.md` §9)

1. **PT-62's remainder** (→ Colonists & domes) — D12's only gate, ⛔ NOT a
   release gate (opt-in; owner, 2026-08-03). ✅ P4/P6 PASSED 2026-08-03 (dome
   23 → 0, overpop cleared); still owed: **P12 · P13 · P14 + the landing
   check** — the PT-62 block is the truth, this line is its summary.
   *(Queue line re-synced 2026-08-11 by a doc sweep — it had frozen the
   pre-08-03 remainder while the block below moved on.)*
2. ✅✅ **The load-heal round-trip sweep — CLOSED 2026-08-12 by your call.**
   Both legs ran and passed (unattended, 2026-08-04: D1 natural-state ×3 loads
   clean, D2 forced-defect heals fire once and hold; details annotated below).
   You ruled D1+D2 close it: everything sampleable passed in both directions,
   the unsampled families (H1 astro — wrong commander; H3 biorobots — none on
   the save; H2/H4 deliberately unforced) stay recorded as unsampled, never
   clean, and return as their own findings if one ever misbehaves organically.
   Nothing further owed.
   *(Original ask, kept for the annotations that follow:)* save, reload twice, read the
   heal numbers (the Astrogeologist +10% class of defect; two-for-two
   defective on the heals actually tested is the project's worst base rate).
   Design: `CHAIN_QA_REPORT.md` §9 item 2.
   ⭐ **HALF DONE UNATTENDED, 2026-08-04, and it cost you nothing** — the
   `unattended-1` chain re-scoped this into two legs and ran the first.
   **Leg D1 (natural state) — RESULT: nothing fired, nothing repeated.** Three
   loads of a staged copy of `TEST2H TRAIN` (load 1 cold, save, reload, reload),
   pack **81/81 active as READ**, **0 `[LUA ERROR]`**, six heal families read
   identically at every load: all three `HEALDIFF VERDICT` lines say **0 of 6
   families changed**, and **not one pack heal line appears anywhere in the log**.
   Log: `docs/archive/u1c1_Mars.exe-20260804-16.46.30.log`.
   ⛔ **What that does and does not buy, because the difference is the whole
   point.** It *does* falsify the F92 shape on this save — the identity-keyed
   heal that turned 1 modifier into 2 after one save+reload would have shown as a
   growing count, and `AutomaticMetalsExtractor` read 2 on all three loads — and
   the F88 shape, the unlatched restart, which would have re-printed every load.
   It does **not** test any heal doing its job: nothing was broken, so nothing
   healed. Two families were **not sampled at all** — H1 astro (the colony runs
   the **rocketscientist** commander, not astrogeologist) and H3 biorobots (0
   biorobots on the save) — and are reported as unsampled, never as clean.
   ⇒ **The remaining hour of your time is not owed:** leg D2 forces the defect
   state and samples the heals firing. Your call is only whether the D2 result
   plus this one closes the item.
   ⭐⭐ **LEG D2 RAN TOO — DONE, and it PASSES. Nothing here is owed to you.**
   Two families were driven from their actual defect state on a staged copy and
   watched through a save/reload/save/reload cycle
   (`docs/archive/u1c6_Mars.exe-20260804-17.24.57.log`):

   | family | forced to | after the healing load | after a further save+reload |
   |---|---|---|---|
   | **H5** `Fix_MeteorFrequency` (F88) | `SMRFixPack_MeteorLatch = false` | one `one-shot heal … (latch false -> 1.0.1)` line, latch `1.0.1` | **no line**, latch `1.0.1` |
   | **H6** `Fix_RainsDeadlock` (C34) | `RainsDisasterThreads = false` | one `RainsDisasterThreads was false — recreated as an empty table` line, `type=table entries=2` | **no line**, `type=table entries=2` |

   All three PASS conditions hold: a heal line for each forced family after the
   healing load, **none** after the idempotence load, and every number back to
   **exactly** the baseline — never above it, which is the F92 compounding shape
   that would have been the failure.
   ⛔ **Ceiling and honest gaps, stated with the result rather than after it.**
   This is **MECHANISM**, not `tested` — it says how these heals behave when they
   fire, not how often a real save needs them. **H1** (Astrogeologist) stayed
   **unsampled**: the colony runs the **rocketscientist** commander, so there was
   nothing to strip. **H2 / H3 / H4** were deliberately not forced — doing so
   means editing colonist traits, dome membership or built objects, a bigger
   mutation than the measurement is worth — so they stand as leg D1 found them.
   ⭐ **A vanilla fact fell out of the forcing:** with `RainsDisasterThreads`
   set to `false`, shipped code threw `attempt to index a boolean value (upvalue
   'old_threads')` at `TerraformingDisasters.lua:411`. The state C34 repairs is
   not merely untidy — vanilla indexes that GameVar with no type check and
   raises. That error is **ours**, inside the probe's marked forcing window, and
   is reported as a consequence of the forcing, not as a new defect.
   ⇒ **Do-first item 2 is complete to its unattended ceiling.** What is left is
   your judgment call on whether that closes it, not an hour of your play.
3. **The doctrine C-sitting** — closes the one INFERRED cell in the "OFF is
   three different things" doctrine, the one the owner said we cannot be wrong
   about. Protocol ready in `CHAIN_QA_REPORT.md` §1.3; the agent builds the
   TEMPORARY probe in-sitting and it dies in the result commit.
4. After those: pick a group and clear it in one sitting. Riders are
   opportunistic — take them when their situation arises; never schedule one.

## The protocol — what a sitting is

A sitting = you at the game + a live agent session reading this file and the
entries. You supply observations **in the moment**; the agent supplies
expectations, forensics and log links. Probe-verified ≠ tested: a pass at the
keyboard is what earns a fix `tested` in `agent/bugs/`.

1. **⛔ PT-00 — the stale-probe sweep, BEFORE the game launches** (hard rule,
   owner, 2026-08-01). The agent runs
   `grep -rln "TEMPORARY" Code/ ../SMR-BugFixPack-TestKit/Code/` and reports
   **CLEAN** — zero hits, or every hit declared by this sitting's design. Not
   clean → delete the stale probe (+ its metadata/items lines), commit,
   re-sweep — or the sitting does not test. No result is recorded without it;
   the `PROBE SWEEP:` line goes in every result commit. Full rule:
   `agent/WORKFLOW.md` "Probe hygiene".
2. **Predictions BEFORE the leg.** The agent writes numbered predictions from
   the entry before anything runs — the discipline moved from this document
   into the sitting, and PT-61 is the proof it pays (ten predictions, ten
   readings, two riders closed free). A prediction that misses is the finding.
3. **Console steps come from the agent, one command per line**, drawn from the
   entry and PLAYTEST_HELP's verified command table.
4. **PT-22 — the log review, after EVERY session, together.** Newest
   `Mars.exe-*.log` under `%AppData%\Surviving Mars Relaunched\logs`: any
   `[CommunityFixPack]` error/inactive/deactivation line, any `[LUA ERROR]`
   naming pack code, any engine error you did not see vanilla,
   `SMRFixPack.ListFixes()` reading `active` for every default fix (count per
   `python tools/doccheck.py --emit-counts`; opt-ins read `inactive` unless you enabled them — and
   Mod Options survive a Mod-Manager disable, so read the list, never assume).
   ⛔ **Every unexplained line is reported verbatim with its age** — "not
   caused by our leg" is an attribution verdict, never a dismissal; every
   pushback so far has turned up a vanilla defect that was not on our list.
   Passive watch, no action: if `WATCHDOG — Meteors thread silent` ever
   appears, report it verbatim (F02).
5. **Recording (the agent, same sitting or next session):** the result goes on
   the `agent/bugs/` entry with the date and the **session uptime next to any
   error count**; a PASS flips status in front matter AND heading tag (INDEX
   is generated — never hand-edit); a FAIL files a finding and flips nothing;
   when a status flip will cite a log's numbers, the log is copied into the
   repo in the same commit (R8) — ⛔ **`.gitignore` line 2 is `*.log`, so a
   plain `git add` DROPS IT SILENTLY and the commit still looks complete; use
   `git add -f docs/archive/logs/<name>.log`** (found the hard way 2026-08-03,
   after one commit shipped claiming logs it had not committed); the completed
   section moves WHOLE to
   `PLAYTEST_ARCHIVE.md` and is **deleted from here with no stub or pointer
   left behind**. `python tools/doccheck.py` before every doc commit.

*(This section recreates the checklist's "Reporting protocol", which turned
out to have been deleted by accident in commit `22d7b36`, 2026-08-02 — the
top-of-file link had been dangling since. The original text, old paths and
all, is in git and in the snapshot.)*

---

# Trains — one sitting clears the group

> ✅ **PT-37 RAN 2026-08-05 (corun-batch-1 sitting, attended) and moved WHOLE
> to `archive/PLAYTEST_ARCHIVE.md`.** Case A PASS (better than a no-op:
> 559→558 connections, persisted through save+reload; you watched a train pass
> through every station); case B UNSAMPLED — the harness refused to run it
> because the walk cannot fail via meteor damage, which contradicts F48's
> blocking premise for its cited scenario. **The F48 ship/hold decision is
> yours — "Decisions waiting on you", item 1.**

### Rider — F80: colonists wait at platforms, or walk past working stations · Status: unrun — take it WHEN the symptom appears; never schedule it
**Bug:** trains sometimes never enumerate a valid destination from a stop —
one origin/destination pair fails inside an otherwise healthy network, so
colonists either queue forever or set off overland and suffocate. The
strongest reported-but-unpinned defect on the list; the mechanism now has an
exact source predicate but the trigger has never been proven.
→ [agent/bugs/F80.md](agent/bugs/F80.md)
**Requirements:** None / any colony where the symptom appears — colonists
queued while trains come and go, or walkers passing a working station.
**Setup:**
1. ⛔ **Tap before mitigating** — adding trains is the known workaround and it
   destroys the evidence. Open the agent session the moment you see either
   symptom.
2. Tell the agent which symptom (waiting vs walking) and the exact
   origin/destination pair that fails.
3. The agent hands the three reads (classify · enumeration tap · both-ends
   reachability test) — all read-only, all on the entry.
**Good to have:** note whether any track segment on the line was under
construction (the rival explanation the agent must exclude).

### Rider — F21: re-earn `tested` for the wait-time fix · Status: unrun — optional · ⭐⭐ **2026-08-10 THE PENALTY HALF IS MEASURED AND THE FIX WAS WITNESSED FIRING** (`corun-batch-2`): one named colonist watched across a real, unforced boarding — `start_wait 239310758 -> 239344642`, **+33,884 ms to the boarding moment**, after 205 polls reading `Waiting`. The 2026-08-05 `spent_time=nil` was our reader, not the game. ⚠️ Still NOT re-earned as `tested` — one boarding is an instance, not a keyboard pass · **mode: co-run ride-along** (routing 2026-08-04) · ⚠️ 2026-08-05 HALF measured: the platform-population read ran live (11 stations / 21 colonists waiting / 8 trains) but the penalty half is UNMEASURED — every train sampled read `spent_time=nil` (4 of 8 sampled), a reader gap, not a verdict; stays `fixed`, not re-earned
**Bug:** the fix (platform waiting no longer billed as travel time) passed
PT-43, but the Tier-2 rewrite replaced the mechanism that pass exercised, so
F21 was honestly downgraded to `fixed`. Two quick reads on any working train
line re-earn the tag; skipping costs nothing — it simply stays `fixed`.
→ [agent/bugs/F21.md](agent/bugs/F21.md)
**Requirements:** None / any colony with a working train line and commuting
colonists.
**Setup:**
1. Let someone wait long at a platform; the agent reads their Comfort log (no
   "travel time" entry from the wait) and the train's *Travel time (rolling
   average)* (excludes the wait).
**Good to have:** a long platform queue — it makes the discrimination obvious.

---

# Drones & hubs

> ⛔ **DRONE PLAYTEST FREEZE (owner decision, 2026-07-31).** No drone
> playtesting of any kind until a final drone plan is in place — half-finished
> tests of superseded designs cost sittings and produce evidence about code
> being replaced. When the rebuild lands, **ONE multi-step drone playtest
> replaces the whole PT-52 family** (one toggle, all or nothing). If a drone
> anomaly shows up organically mid-sitting, capture it on the D06 entry or as a
> new F-number — observing is not playtesting. **NOT frozen:** PT-10 below
> (dome-entrance data, untouched by any dispatch redesign) and F77's own fix
> (shipped, default-on; only its test's packaging was frozen).

### PT-52 — Drone dispatch overhaul · Status: ⚖️ UNFROZEN 2026-08-31 (item 87) — still blocked on the design decision; the test needs its rewrite from the approved plan
**Bug:** tests D06 `Opt_DroneOverhaul`'s v1 design, and that design is being
rebuilt — every result it could produce would be evidence about code that will
not exist. → [D06](agent/bugs/D06.md), [F77](agent/bugs/F77.md),
`docs/agent/reports/DRONE_OVERHAUL_OPTIONS.md`.
**Requirements:** ⛔ BLOCKED — waits on the approved drone plan; do not run any
part of it. ⚠️ For whoever rewrites this test: the old Trigger C rider's
"uninstall shape" conflated the module TOGGLE with a Mod-Manager disable —
the toggle arm is VOID as an uninstall test ("OFF is three different things",
chain-12 QA re-label, in the snapshot); the rewrite must keep the two arms as
separate steps.
**Setup:** none until the rebuild. The B2 stress protocol and the CAN/CANNOT
judging lists are preserved in the archive snapshot — the rebuild's
verification leg is derived from them.

### PT-10 — Open-roof drone observation (F55) · Status: ✅✅ **RUN 2026-08-16, ATTENDED, BY THE OWNER — ❓ OPEN QUESTION CLOSED** · **no longer needs a co-run**
> ⭐⭐ **Answered, and better than the bar.** Owner ran it twice on their own
> colony — once via `CheatOpenAllDomes()`, once by reaching breathable
> atmosphere *organically* (Atmosphere 100% / Temperature 84.09%, Open Domes law
> actually passed). Drones **enter, service and TRANSIT** open domes (they
> pathfind straight through to tasks on the far side), a `dome_required`
> Amphitheater read 9% deterioration / last serviced 17 h, and there is **no
> clustering**. ⇒ The dome-entrance PF-tunnel concern is **disproven**, not just
> un-actionable. ⛔ It did **not** exercise the fix itself (that needs a drone
> that already failed an approach), so F55 was NOT promoted to
> `tested-attended`. Full write-up + the confound argument: [F55](agent/bugs/F55.md).
> ⚖️ Nothing owed from you; the promotion question is yours if you ever want it.
**Bug:** no expected answer — either result is useful data. The forever-cache
half is fixed and probe-verified; whether opening a dome's roof destroys the
dome-entrance attaches carrying the only drone pathfinding tunnels in is engine
entity data Lua cannot read. Drones-enter-normally closes F55; drones-locked-out
is a new engine-data finding. → [F55](agent/bugs/F55.md)
**Requirements:** SAVE-A / one dome with interior buildings needing maintenance
/ a drone hub with drones parked outside.
**Setup:**
1. `CheatOpenAllDomes()` (also maxes terraforming and activates the Open Domes
   policy — the prerequisites).
2. Run 1-2 sols at ultra; the agent records the four observations (entry): do
   drones enter · does interior maintenance pile up · do drones clump at the
   entrance · does `CloseAllDomes(MainCity)` recover it, alone or only after a
   save/load.
**Good to have:** screenshots — the clustering picture is half the evidence.

### Rider — C25: Jumbo Cave waste-rock wedge · Status: ✅ DONE 2026-08-30 — CONFIRMED, promoted to F110
**Result:** ran on a Reddit field save (build 1.0.7.396349, `VINTAGE true`). A
`JumboCaveReinforcementStructure` site with `waste_rocks_underneath = 1`, the last
rock a `WasteRockObstructor` (`Rocks_04`) in 2 drones' `unreachable_buildings`,
`JCRS completed = 0`; permanence witnessed (flag reset on load, rebuilt after
~1-2 min run). **Non-zero-while-stuck → C25 earned its F-row.** → [F110](agent/bugs/F110.md).
Fix decision is item 82 above. (This rider is closed; kept as the record of how
the read was taken.)

### Rider — F77: extender-flap Idle-kick · Status: blocked (frozen with PT-52)
**Bug:** the fix ships default-on and is NOT invalidated — how big is the
fleet Idle-kick with and without it? Its check folds into the consolidated
drone PT when the rebuild lands. → [F77](agent/bugs/F77.md)
**Requirements:** ⛔ BLOCKED with the drone freeze.

---

# Disasters

### PT-27 — Biorobots and Dust Sickness (F40) · Status: unrun · **mode: co-run** (routing 2026-08-04 — `CheatDustStorm` forces the storm, HELP table; catch-lists are console reads)
**Bug:** Dust Sickness infected Biorobots — androids bled Health every storm
until cure tech. Fixed: only organic colonists catch it; a load-time heal
clears already-sick Biorobots. → [F40](agent/bugs/F40.md)
**Requirements:** SAVE-A with the Dust In The Wind rule / Biorobots obtainable
(The Positronic Brain breakthrough — provisioning route on the entry) / a dust
storm.
**Setup:**
1. The agent provisions Biorobots and confirms the trait (entry; if none can be
   produced, record "could not set up" and skip).
2. Note who is a Biorobot; wait through a dust storm with the Dust Sickness
   event active.
3. When it resolves, list who caught it — the agent reads against the entry.
**Good to have:** load a save with already-sick Biorobots — the heal log line
(entry). Run PT-28 in the same storm; same save, same sitting.

### PT-28 — Dust Sickness damage spread (F17) · Status: unrun · **mode: unattended ride-along** (routing 2026-08-04 — pure numeric pattern; rides PT-27's storm sitting)
**Bug:** the per-colonist damage roll was computed then discarded — every
carrier lost a flat 10 Health/sol instead of 5-14. Fixed: the losses spread.
→ [F17](agent/bugs/F17.md)
**Requirements:** SAVE-A (Dust In The Wind) / an active dust storm / several
Dust Sickness carriers (PT-27 gets you there).
**Setup:**
1. Pick 4-5 sick colonists in the same dome; note each one's Health.
2. One sol at ultra speed.
3. Compare the drops — the agent reads the pattern (not exact numbers) against
   the entry.

### Rider — F90: underground breaks during a surface storm · Status: unrun · **mode: co-run, STAGEABLE** (routing correction 2026-08-04 — `CheatDustStorm` is real and ungated, so the storm can be forced on a staged elevator-colony copy; the break DISTRIBUTION stays the organic measured path. An organic storm sighting still counts — take it if one arrives first)
**Bug:** surface dust storms could break cables/pipes on the underground map
through the merged elevator grid. The defect is a victim *distribution*, so
one quiet session proves nothing — the read is zero NEW underground leak
notifications during a surface-only storm, cave-ins excluded.
→ [F90](agent/bugs/F90.md)
**Requirements:** underground unlocked / at least one elevator built / a
surface dust storm running / the merged fragment holding >10 connectors
(agent checks).
**Setup:** while the storm runs and for a while after, watch the underground
map's notifications; the agent excludes cave-ins and reads per the entry
(including the known surface-rate residual that is NOT a miss).

---

# Rockets & landers

### PT-18 — Arrival deaths, including the elevator path (F53) · Status: unrun · **mode: co-run** (routing 2026-08-04 — landings staged, deaths/strandings are counters; ⚠️ SAVE-E provisioning is still yours, ~30 min)
**Bug:** newly arrived colonists could walk toward unreachable domes and
suffocate, and the reworked fix's broken case WAS the elevator path — so that
path is tested deliberately. Fixed = nobody dies on arrival: safe drop spots,
elevator riders keep their assignment, unreachable-dome arrivals wait under
"Confused Colonists" and retry. → [F53](agent/bugs/F53.md)
**Requirements:** SAVE-E / an underground dome with free housing reachable
only via the Elevator / a surface rocket landing pad.
**Setup:**
1. Case A — land colonists on the surface away from any dome; watch where they
   walk and whether anyone dies or goes Abandoned.
2. Case B (the important one) — make the underground dome the only free
   housing (fill/close the surface domes), land a rocket, follow the arrivals:
   to the Elevator, down, and in.
3. Case C — land where the nearest dome by straight line is unwalkable while a
   walkable one exists further away.

### Rider — F74 + F53(a): the never-modded fresh-colony pair · Status: unrun · **mode: co-run** (routing 2026-08-04 — the harness builds the fresh colony; you: the pack-disable click + the two UI acts)
**Bug:** two "is the vanilla harm real at all" observations that need a true
vanilla control — a pack-lineage save cannot serve (persisted thread stacks
carry pack code). F74's half no longer decides anything (two outside witnesses
answer it); it rides only because the colony is already there.
→ [F74](agent/bugs/F74.md), [F53](agent/bugs/F53.md)
**Requirements:** a FRESH ten-minute colony that has NEVER had the pack
installed / pack disabled for the sitting.
**Setup:**
1. Order an RC Transport onto a landed storybit trade rocket — does the
   original harm actually occur?
2. Land a passenger rocket flush against a Universal Depot — do arrivals
   actually strand?

### Rider — F83: is the paid Detailed Scan reachable elsewhere? · Status: unrun
**Bug:** after declining or losing a `ReconCenterDiscoveryAsteroid` popup, is
the paid Detailed Scan reachable anywhere else (planetary view)? Settles the
popup audit's verdict on F83's second site. → [F83](agent/bugs/F83.md)
**Requirements:** a Recon Center holding enough Electronics for the scan / the
asteroid popup declined or lost.

### Rider — C32: the asteroid-abandon label read · Status: unrun
**Bug:** does abandoning an asteroid desync building labels? The row was
rewritten 2026-08-01: you must ABANDON manually (asteroids never expire on
1.0.7) and destroyed buildings must be excluded or the first meteor strike
false-confirms it. Non-zero = the defect; zero still proves nothing.
→ [C32](agent/bugs/C12-C38.md)
**Requirements:** an asteroid mission you are willing to abandon
(`UIAbandonAsteroid`) / the read taken on the map whose buildings you care
about.
**Setup:** after abandoning, the agent hands the corrected membership read
(entry).

### Rider — F34(d): landscape mark over a loading rocket · Status: unrun · **mode: co-run** (routing 2026-08-04 — staging rig-side; your eyes on the yank)
**Bug:** drop a landscape mark over a rocket actively loading drones — is a
mid-"Embark" drone visibly yanked, or does it recover silently? Settles the
reachability audit's verdict. → [F34](agent/bugs/F34.md)
**Requirements:** a rocket mid drone-embark / landscaping unlocked.

---

# Colonists & domes

### PT-62 — D12 "no homeless" remainder · Status: ✅ P4/P6 PASSED 2026-08-03 (dome went 23 → 0, overpop cleared) — P12 · P13 · P14 · the landing check still owed. ⛔ NOT a release gate (opt-in; owner, 2026-08-03)
**Bug:** the module works — same colonist, same moment: vanilla answered
`false nil`, D12 supplied a reachable suitable dome — but the first sitting's
drain fought an inflow (the ping-pong finding), and the three changes built in
response are UNRUN. This remainder is D12's only gate. → [D12](agent/bugs/D12.md)
**Requirements:** a STABLE colony — the drain must not fight an inflow /
restart first (**four** unrun changes as of 2026-08-03) / Mod Manager for the
uninstall half / **a flagged dome with an open service work slot, for P14**.
⛔ **Do NOT use D03 "Closed to new residents" as a fixture control** — the old
plan said to; withdrawn 2026-08-03. It works, and that is the problem: D03 sits
on the SAME two seams D12's guards do, so it would mask the guard under test and
make the loop check trivially 0 for the wrong reason. It also blocks Seniors.
Entry (incl. the same-day correction to an earlier, wrong reason for this).
**Setup:**
1. Restart, then the suite run.
2. The loop check — ⛔ **use the SPLIT counter, not the old one** (entry,
   2026-08-03): the blind version counts cohort delivery, which a flagged dome
   is REQUIRED to keep receiving, so it cannot fail honestly. Only **inbound
   SUBJECTS** is a leak, and it must be 0 and STAY 0 **through a rocket
   landing** — a single at-rest reading does not test the `ChooseDome` half.
3. P4/P6: the drain clears the dome, **run clean — no D03 crutch** (above); a
   dome that refills anyway is a FINDING, not a fixture problem. Mind the
   entry's employed-homeless caveat before reading P6.
4. ⭐ **P14 — the free-work door** (new 2026-08-03): flag a dome that has an
   open work slot and watch whether the slot **FILLS**. ⚠️ **`0 would move` on
   a recruiting dome is the door WORKING, not a miss** — that is the reading
   most likely to be misfiled. If the slot never fills while unemployed
   homeless sit there, the door needs a dwell bound and D12 does not ship as
   built.
5. P13: the repaired `SMROptInPack_Disabled.NoHomeless` lever mid-drain.
   ⛔ **RENAMED 2026-08-12 with the opt-in split** — `Opt_NoHomeless` lives in
   the Community Opt-In Pack now and reads `SMROptInPack_Disabled`. The old
   name is inert there: setting it silently runs the module LIVE, which is the
   exact PT-61 trap this lever was written after.
6. P12: save flag-ON → Mod-Manager disable → load clean.
   (Predictions P1-P13 and the four setup traps: archive snapshot; the re-run
   musts incl. P14: entry.)

### PT-53 — Cohort housing, Trigger E (D07) · Status: ✅ NOTHING RUNNABLE REMAINS (2026-09-01: the opt-in repo's `agent/bugs/D07.md` reconciled against this block and granted `tested-attended` — A–D passed, the uninstall half CLEAN 08-10 below, the precedence half unmeasurable and its design question ruled 08-11; FIX_POLICY §8 both-config ship test owed there at launch) · was: partial (A-D passed; E owed) · **mode: co-run** (routing 2026-08-04 — two hands moments: the manual assign, the Mod-Manager disable; the load-clean read is log) · ⚠️ 2026-08-05: E's precedence half ROUTED (fixture unholdable — every slot created was consumed in seconds; a design decision went to you instead, item 2 above); in-dome pass MEASURED at colony scale (76→37); **only the uninstall half below is still runnable as written**; ⭐ **the UNINSTALL half RAN 2026-08-10 (`corun-batch-2` leg T) and is CLEAN** — `pack=0/0 active`, zero engine errors, zero new log lines after a minute of play. ⛔ **But it took two attempts: a Mod-Manager disable does NOT take effect until a full game restart** (first attempt read `pack=81/81` and would have banked a clean log of the pack RUNNING). See decision 6 above and `agent/bugs/D13.md`
**Bug:** Seniors/Children in normal housing move to free cohort slots and are
otherwise left alone — triggers A-D passed live ("it worked wonderfully").
Only E remains: player-order precedence and the uninstall shape.
→ [D07](agent/bugs/D07.md)
**Requirements:** any colony with the module on / a Senior you can manually
assign to a normal residence / Mod Manager for the uninstall half.
**Setup:**
1. Manually assign a Senior to a normal residence (player order) — they must
   STAY. ⚠️ 2026-08-05: build the pin BEFORE any free cohort slot exists —
   pin first, create the motive second (three failed attempts and the 5-sol
   pin timeout are on the entry).
2. Toggle the module off — instantly vanilla (behaviour check).
3. Save with it ON → disable the PACK in the Mod Manager → load: clean, no
   `[LUA ERROR]` naming pack code. (A toggle cannot answer an uninstall
   question — "OFF" is three different things, `agent/facts/`.)

### Rider — C40: Crowded Living capacity read · Status: unrun — take it when the law + a working Ministry of Culture exist
**Bug:** not a defect hunt — the ministry gating is intended. Open: the law's
description says +3 while possibly delivering +6, and losing the ministry may
evict people already housed. Harm unproven and deliberately not guessed.
→ [C40](agent/bugs/C40.md)
**Requirements:** Crowded Living enacted / a Ministry of Culture built and
working.
**Setup:** note a Residence's capacity → stop the ministry (off, or cut power)
→ re-read the same Residence; then watch whether anyone was actually evicted
(entry details, including why shift rotation will not trigger it).

### Rider — C42: does a passage traversal leave a stale passenger behind? · Status: unrun — **TAKEABLE WHEN** any colony has a built Passage that colonists actually walk through · ⭐ mechanism link CLOSED 2026-08-04 · ⚠️ 2026-08-05: a WITHIN-SESSION read finally ran (no save/load since traffic) and was STILL unsampled — 0 unit entries over 4 passages; the gap now needs a **traversal witness** (a colonist seen inside a passage element), not merely generated traffic · ⛔ 2026-08-10: the dedicated witness poller ran (`corun-batch-2` prep) — **90 tries × 1 s at speed 20, `units` empty every sweep** — so THIS save cannot sample it; the TAKEABLE-WHEN condition is now "a colony where passages are demonstrably a colonist route", and no zero from `TEST2H TRAIN` may be quoted against the entry (C42 entry, 2026-08-10)
**Bug:** `PassageBase:TraverseTunnel` ends with a raw `unit.holder = nil`
(`Lua/Passage.lua:1055`), which skips the call that would remove the colonist
from the last passage element's `units` list. If so, demolishing that passage
later teleports uninvolved colonists to it and cancels what they were doing.
⭐ **The untraced link is TRACED and HOLDS (unattended-1 leg F, 2026-08-04;
re-derived independently by the terminal audit):** a passage element IS a
`Holder` (`Building`→`BaseBuilding`→`Holder`) and `LeadIn` really does set
the holder, so the stale-entry mechanism is real as written — refined: **one**
stale entry per traversal (on the last element entered), not N. The rig's
post-load read was `C42STALE 0` over **0 unit entries** — UNSAMPLED, and
nothing establishes `Holder.units` survives a load at all. → [C42](agent/bugs/C42.md)
**Requirements:** a Passage with traffic. Nothing else; no cheats, no save
juggling. ⛔ **The read must be WITHIN-SESSION** — after real traversals and
**before any save or load** (a post-load zero is the F99 mistake shape).
**Setup:** one console line, any time after some colonists have crossed —

```
*r local a=0 for _, c in ipairs(Cities) do for _, p in ipairs(c.labels.Passage or empty_table) do for _, el in ipairs(p.elements or empty_table) do for _, u in ipairs(el.units or empty_table) do if u.holder ~= el then a=a+1 end end end end end ConsolePrint(print_format("C42STALE", a))
```

**The counter can fail:** ⚠️ *(corrected 2026-08-04 by the unattended-1 audit —
this line used to say "`0` refutes the entry outright", and that is wrong: a
`0` counts as a refutation ONLY if the denominator was populated — units
actually inside passage elements when the read runs, within-session.)* A `0`
over a non-zero unit-entry population refutes the entry; a `0` over zero
entries samples nothing. Non-zero confirms the desync and the follow-up is to
demolish that passage and watch whether an unrelated colonist teleports to it.

### Rider — F99: re-read the track residue BEFORE a reload · Status: **unrun — the rig RAN the recipe 2026-08-04 and the rider's own precondition never arose; ⚠️ 2026-08-05 added TWO MORE witnessed attempts (meteor repairs on one track, 201 new-build sites across three tracks with the merge confirmed) and `TrackElement.lua:805` did not fire in either, so the gate still never opened — three attempts, zero throws, rate bounds only; ⭐ 2026-08-10 a FOURTH witnessed zero (`corun-batch-2` leg Q — the 2×2's last empty cell: repair sites on 2 DISTINCT tracks completed together, sites 2→0, residue read `0 0` before any save/load) — the `:805` gate has still never opened** · **mode: unattended, STAGEABLE** (routing 2026-08-04 — the rig stages break + cheat + pre-reload read deliberately; owner-rule chain applies: Opus runs, Fable audits. The old TAKEABLE-WHEN framing — wait for a sitting to happen to use the cheat — is superseded)
⭐ **What the 2026-08-04 attempt (unattended-1 leg B) established:** one staged
break + `CheatCompleteAllConstructions()` produced **zero** `:805` throws, so
the "if `:805` appears" gate below never opened — the rider needs a run in
which the throw actually happens. Gained anyway: `F99RESIDUE 0 0` pre-reload
is the reading a *healthy* completion produces (so the fixup is no longer the
only explanation shape); the `BreakTracks({element})` instrument is confirmed
by execution (`repair_cgs` 0→1); and the counter has a liveness witness. Log:
`docs/archive/u1c3_Mars.exe-20260804-17.06.05.log`; full record on the entry.
**Bug:** the `F99RESIDUE 0 0` reading that made F99 look harmless was taken
**after** a reload, and load runs `SavegameFixups.RebuildBrokenTracksAndConnect`,
which sweeps exactly what the probe was looking for. The null result is
therefore not evidence of no damage. → [F99](agent/bugs/F99.md)
**Requirements:** the cheat, plus at least one outstanding repair group —
`repair_cgs` is only ever populated by meteor strikes and disaster damage, so on
a clean build-out there is nothing for the probe to find and `0 0` is
guaranteed regardless.
**Setup:** run the cheat, and if `TrackElement.lua:805` appears in the log,
**read this before saving or loading anything**:

```
*r local a,b=0,0 for _, c in ipairs(Cities) do for _, t in ipairs(c.labels.TrackBase or empty_table) do if #(t.elements or empty_table) == 0 then a=a+1 end if t.repair_cgs and #t.repair_cgs > 0 and #(t.elements_under_construction or empty_table) == 0 then b=b+1 end end end ConsolePrint(print_format("F99RESIDUE", a, b))
```

**The counter can fail:** a non-zero `b` is a track stuck showing damage and
refusing to be salvaged, and would move F99 off `cand` on the spot. Note the
session uptime next to the count (the 2026-08-03 convention above).

### Rider — C39: Service Automation and the four Workshops · Status: ✅ **RUN 2026-08-11 (corun-pt15 sitting) — ANSWERED**
**Bug:** the law halves staffing by LABEL while its performance compensation
keys on CLASS; the four Workshops sit on the wrong side of that line. The sign
of the harm was genuinely unclear — this was a keyboard observation, not more
reading. → [C39](agent/bugs/C39.md)

⭐⭐ **RESULT: the Workshops are MISSING AN UPLIFT, not taking a penalty.** With
the game **paused** (both readings at the same game instant, so drift cannot
explain it), your TV Studio Workshop and a Diner in the same dome **both** took
the identical −50% staffing cut — and only the Diner was paid back for it:

| | before | law on | after revert |
|---|---|---|---|
| **Workshop** performance | 127 | **131** | 129 |
| **Workshop** workers/shift | 12 | **6** | 12 |
| **Diner** performance | 114 | **268** | 124 |
| **Diner** workers/shift | 2 | **1** | 2 |

The Diner's **114 → 268 → 124** reverses when the law is deactivated, which is
what makes it a measurement rather than a coincidence. Your words, kept in the
record: *"more than double when I reverted it dropped to 124 for the dinner."*
⇒ those four buildings lose ~half their output whenever Service Automation
passes.

⚖️ **YOUR CALL — nothing is built.** The chain's scope fence makes C39 an
observation only; if you want a repair, that is a new decision. Severity is also
open: it needs a late-game Technology policy (SortKey 900, 10th of 11) to be
voted through before it can bite anyone.
⛔ **Honest limit:** only **one** of the four Workshops (`TVStudioWorkshopCCP1`)
existed in the colony. The other three share the same class chain so the same
result is expected — but it is inferred for them, not measured.

---

# Mysteries

> ✅✅ **PT-15 RAN 2026-08-11 (`corun-pt15` attended co-run) and moved WHOLE to
> `archive/PLAYTEST_ARCHIVE.md`, audit-sustained the same day.** F07 is
> **`tested`** — your trap's 95 wisps produced 95 power (43% of the grid, ~47
> Solar Panels' worth; vanilla would have given 0.095), it survived save/reload,
> and your verdict is on the entry verbatim. F15's double-grant half is
> MEASURED gone on the same trapful. Kept saves (NOT strays — do not delete):
> **`CP15PT15.savegame.sav`** and **`CP15F15.savegame.sav`**. The two decisions
> the sitting raised (C39 repair, C46) are in "Decisions waiting on you".

### PT-30 — Finished Mirror Sphere site (F16) · Status: unrun
**Bug:** a finished excavation site kept offering its actions, wasting drone
work on a site that cannot progress. Fixed: the finished site starts nothing;
cancelling still works. → [F16](agent/bugs/F16.md)
**Requirements:** a Mirror Sphere mystery game (new-game pick) / played to a
scanned excavation site with a Drone Hub in range.
**Setup:**
1. Control: while the site is part-way done, confirm its actions can start.
2. Run the excavation to 100% — the sphere launches and detaches.
3. Try each action on the finished site — the agent reads per the entry.
**Good to have:** the settling observation rides along: do drones engage a
dead request when an action is clicked?

### Rider — F06: Mystery 10 epilogue arrival · Status: unrun
**Bug:** reach the finale and ignore the corner notification for one sol at
speed — does the Epilogue really arrive minimized and unpaused? Settles the
reachability audit's verdict. → [F06](agent/bugs/F06.md)
**Requirements:** a colony at the Mystery 10 finale.

---

# Any-save & factions

### PT-35 — Save sanitizer does no harm (F35, F03) · Status: **case A COMPLETE 2026-08-11 (mechanism grade — not `tested`); B/C parked** *(status token corrected by the unattended-2 audit; it still read "unrun" beside the completion record below)* — ⭐ case A RAN unattended 2026-08-04: do-no-harm half PASSES, turbine half UNSAMPLED (fixture gap, see below) · ✅✅ **THE FIXTURE GAP IS CLOSED 2026-08-10** — `PT35FIXTURE.savegame.sav` is in your save folder (`corun-batch-2` leg S): FrictionlessComposites researched, **one Large Wind Turbine**, **one applied building upgrade** (Remote Medic on a Hospital, for the F03 half). **The turbine-half re-run is now an unblocked 2-prompt unattended chain** — nothing of yours needed. ⛔ Do not delete that save · **mode: UNATTENDED** (routing 2026-08-04 — all reads numeric + save/reload; owner-rule chain: Opus runs, Fable audits) · ✅✅ **CASE A IS COMPLETE 2026-08-11 (`unattended-2`, re-run after the pack was re-enabled): BOTH halves sampled on a real population for the first time. Three loads, two save+reload round trips, six pass calls, and **0 of 14 readings changed at every single comparison including start-to-finish**. `RepairTurbineBuff`'s zero is no longer the trivially-forced early return — the tech IS researched, so the pass walked its whole body and its already-buffed guard did the skipping; `RepairLeakedUpgradeModifiers` returned 0 with **3 live upgrade-shaped modifier ids and 144 upgraded buildings** in front of it. 0 `[LUA ERROR]` in the whole log. ⛔ Still not `tested` — unattended ceiling is MECHANISM — and cases B/C stay parked.** → `agent/bugs/F35.md`, log `archive/u2run3_Mars.exe-20260811-02.01.06.log`
**Bug:** the pack's two sanitizer passes run automatically on every load for
every player, and the F03 pass REMOVES label modifiers from persisted colony
state — this is the do-no-harm check on auto-running save-writing code, and
the only part of PT-35 that was ever about risk. Cases B and C are PARKED
(`FUTURE_IDEAS.md` entry 4). Both passes are probe-covered; this is cheap
insurance, not substitute coverage. → [F35](agent/bugs/F35.md),
[F03](agent/bugs/F03.md)
**Requirements:** None / any healthy save with a Large Wind Turbine and an
upgraded Medical Center in a dome / ~5 minutes.
**Setup:**
1. Note the turbine's Power production and the dome's birth-comfort figure.
2. Run both console calls — `SMRFixPack.Sanitizer.RepairTurbineBuff()` and
   `SMRFixPack.Sanitizer.RepairLeakedUpgradeModifiers()` — both must return
   **0** and nothing on screen may change.
3. Save, reload, check again. A bonus that GREW on the second run is the FAIL
   (the pass is not idempotent — record the exact figures).

⭐ **RAN UNATTENDED 2026-08-04 (unattended-1 leg A) — case A's do-no-harm half
PASSES; half of it is UNSAMPLED. Status stays `unrun`; this is not a `tested`
grant and cannot be (unattended ceiling is MECHANISM).**

**Run conditions.** Retail `Mars.exe` **1.0.7.396349**, cold load of a staged
COPY (`U1STAGE.savegame.sav`) of `TEST2H TRAIN`, pack **81/81 active as READ**,
speed 3, 2 loads, **0 `[LUA ERROR]` lines in the window**. FORCED: nothing but
the two calls themselves. ORGANIC: nothing. Raw lines:
`docs/archive/u1c2_Mars.exe-20260804-17.03.10.log`.

| step | reading |
|---|---|
| both calls, load 1 | `RepairTurbineBuff ok=true returned=0` · `RepairLeakedUpgradeModifiers ok=true returned=0` |
| numbers before → after, load 1 | `0 of 7 readings changed` |
| save → reload, numbers across the round trip | `0 of 7 readings changed` |
| both calls again, load 2 | both `returned=0` |
| numbers before → after, load 2 | `0 of 7 readings changed` |
| start → finish | `0 of 7 readings changed` |

⇒ **Nothing grew, nothing changed, both passes returned 0 twice.** That is
step 2's "nothing on screen may change" and step 3's FAIL condition, in the
numbers the entry's own claim is about.

⛔ **What is NOT sampled, stated before anyone quotes the PASS.** The fixture
this test asks for is **not on this save**: `FrictionlessComposites
researched=false`, **0 Large Wind Turbines**, **0 Medical Centers** (13 domes,
47 dome label modifiers).

- **`RepairTurbineBuff`'s 0 is trivially forced and samples nothing.** It
  early-returns at `Code/90_SaveSanitizer.lua:58` —
  `if not colony:IsTechResearched("FrictionlessComposites") then return 0 end` —
  so the pass never reached its body. **UNSAMPLED, not a do-no-harm result.**
  Re-running this half needs a save with that tech researched.
- **`RepairLeakedUpgradeModifiers`'s 0 is real but partial.** It ran its full
  body over the colony, every city and all 13 domes — 175 label-modifier
  entries — and removed none. So *"it does not strip live state"* is sampled on
  a real population. *"It clears leaks"* is not: whether the save held any id of
  the form `<handle>_upgrade<N>_mod_<M>` at all was not measured.

**What it would take to close case A properly:** the same leg on a save with
Frictionless Composites researched and at least one upgraded building — which is
a fixture request, not a sitting. ⇒ routed as a gap by unattended-1 prompt 2.
⚠️ 2026-08-05: the corun-batch-1 sitting re-read the fixture on every load —
still `FrictionlessComposites researched=false`, 0 Large Wind Turbines — and
the sitting ended before its optional leg-5 fixture build was reached. The
fixture request stands; no FIXTURE save exists.

### PT-42 — Last Transmission notices your reserves (F22, F75) · Status: unrun · **mode: co-run** (routing 2026-08-04 — stock/drain staged at speed; your eyes: the faction panel goals at 3–4 moments) · ⚠️ 2026-08-05 SKIP re-confirmed LIVE, not on prep's word: Last Transmission read `active=false` on the staged `TEST2H TRAIN` copy — 5 active factions, none it, 0 legislature seats — so the fixture requirement below is real and still unmet
**Bug:** the faction's stored-resource goals never cleared no matter how much
you banked, the Oxygen goal was satisfied by Power, and the penalties became
unreachable once a second map was loaded. Probes prove the reserve maths; only
play shows the approval actually moving and the UI goal clearing.
→ [F22](agent/bugs/F22.md), [F75](agent/bugs/F75.md)
**Requirements:** a game with Last Transmission as an active faction (ideally
with the Underground map opened — that is what made the old maths hopeless) /
storage you can build up and then drain.
**Setup:**
1. Open the faction panel; note approval and the listed "How to achieve"
   goals.
2. Stock Power past 2 sols' worth, let a day pass — the Power goal stops being
   listed and approval rises (reason in the approval breakdown).
3. Repeat for Water, then Oxygen — the important one: only Oxygen clears it.
4. Drain one to zero — the matching "No X stored" penalty appears and approval
   falls.
5. The agent checks the two log lines (entries).
**Good to have:** F22's settling observation rides along — where is the
corrupted number player-visible in a young politics colony, before the Martian
Assembly stage?

---

# Cross-cutting — once per era of the pack

### ~~PT-60 — The chain-8b batch leg (F90-F96 + eight conversions)~~ ✅ **RUN 2026-08-12 (`corun-pt60` co-run) — all nine predictions resolved, audit sustained.** Moved WHOLE to `archive/PLAYTEST_ARCHIVE.md` (results banner + the pre-run spec + this tracker). Highlights: the P8 decider taken on your `USA Sol 302` copy (heal fired once, zero on reload, effect persisted); suite 77/0/10/0 with every SKIP matched by name; 0 errors in the whole log; F48 repaired 3 of 7 tracks in your campaign and the repair stuck; F34(d) re-derived on your challenges and observed reachable 20/20. Your original save byte-verified untouched. Decisions that came out of it: items 12 and 13 above.

### PT-21 — Long-save soak · Status: unrun
**Bug:** the whole-pack background check — nothing drifts, leaks or degrades
over a real session of ordinary play.
**Requirements:** any healthy colony / all default fixes `active`
(`ListFixes`) / 45-60 minutes of real play, no cheats.
**Setup:**
1. Just play — mixed speeds, at least one save/reload midway; note anything
   that feels off (stuck colonists, drone clusters, flickering notifications,
   unexplained deaths).
2. At the end, the agent runs the three state reports (reservations, trains,
   broken track — Test Kit, PLAYTEST_HELP).
3. Log review per the protocol.

### PT-20 — Uninstall safety · Status: ✅✅ **REDO RAN CLEAN 2026-08-14 in state 3 — this per-era re-check is DONE for this era** · standing (re-run per era and before release) · **mode: co-run**
✅✅ **THE REDO (your decision 6, 2026-08-10) IS PAID.** Combined sitting moment A,
log `archive/cs_a1_Mars.exe-20260814-11.57.50.log`. Both packs Mod-Manager-disabled
**with a full process restart**, so this is state (3) and not the mixed state (2)
the old reading may have sampled.
* **The gate, beside every reading:** `pack=0/0 | opt-in=0/0 | save-rescue=0/0`,
  all three registries ABSENT, and `MODORDER :: 1 mod(s) loaded ::
  1:SMR_CommunityFixPackTestKit` — the kit alone.
* **All 8 pack-naming lines accounted:** three mod-**def** loads (the def loads in
  state 3, the code does not) · `Loaded mod items for: …TestKit` · the save's own
  recorded mod list · one `Unpersist missing permanent: Mod/SMR_CommunityFixPack`
  · two *"…which is present, but not loaded"*. ⚠️ The `Unpersist` line is **not
  diagnostic** — it fires in state (2) with the pack fully live; it is only
  readable next to the `pack=0/0` gate.
* **~21 minutes of the owner's ordinary play** (building, trains, workers —
  *"everything seems normal"*), then a save as `PT20REDO` and a reload, which
  printed its own gate line.
* ⭐ **Verdict: 0 `[LUA ERROR]`, 0 `[ERROR]`** in the flushed file (absence read
  only from the archived file, `EF-047`). F99 `:805` and C45 `Quantum Comet`
  watches zero.
* **The leg's own point held:** the save still carried its leftovers throughout —
  `reserved_at ×1260`, `payload_set ×4`, `closed_to_new_residents ×4`, both Drone
  dial modifiers, the F48 latch — *and it behaved normally anyway.*
* ⛔ **Recorded as SUPERSEDING the 98-vs-98, not confirming it.** That was an error
  **count** comparison from the F86 era and F86 is repaired (PT-58 measured the
  same shape at zero); a clean state-3 run replaces it, it does not reproduce it.
* ⚠️ **One deliberate deviation from the setup below:** *both* packs were disabled,
  not the fix pack only. The host save was written with both, so disabling both is
  the true "the player uninstalled our mods" configuration — and it is what the
  D13 after-sweep in the same window required. ⛔ **Save Rescue was pulled for this
  leg**: left installed it would have stripped the residue two seconds into the
  load and the leg would have sampled nothing.
Earlier framing: ⛔ **2026-08-10: a Mod-Manager disable does NOT take effect until a FULL game restart** (D13, measured) — the prior 98-vs-98 comparison may have sampled the mixed state · redo ordered by your decision 6, 2026-08-10
**Bug:** the pack must never hold a save hostage. Steps 1-4 passed 2026-07-31;
step 5's hunt found F86 (both sites since repaired — PT-58 measured the same
shape at ZERO errors against leg 5's 80). This is the per-era re-check, not an
open debt. → [F86](agent/bugs/F86.md), `agent/FIX_POLICY.md` §3.
**Requirements:** any current save with the pack on / Mod Manager / ~20
minutes.
**Setup:**
1. Play a few sols, save.
2. Quit → disable the Relaunched Fix Pack ONLY in the Mod Manager (Test Kit
   stays) → restart, load.
3. 10 minutes of ordinary play, one save/reload — the save must behave
   normally (the original bugs coming back is expected and fine).
4. Log: zero errors naming pack code. The agent pulls the full step-5 hunt and
   the 2026-07-31 method corrections from the archive snapshot before running.

### Rider — §3.6 corner (optional): the sol-change autosave under a popup · Status: unrun — was M3 in `corun-batch-2` (2026-08-10) and was NOT reached (no sol boundary came near); ⭐ **now the interesting popup half**: F85's route refutation makes this the one popup that does NOT pause, i.e. the only place a vanilla autosave can reach a save under a popup with no rebind involved (F85 entry, 2026-08-10) · **mode: co-run ride-along** (routing 2026-08-04)
**Bug:** with the distress-call popup left open, does the sol-change autosave
fire under it? → `POPUP_CONSEQUENCE_AUDIT.md` §3.6.
**Requirements:** any save approaching a sol change.

### Rider — F38: tunnel-ruin routing (vanilla read) · Status: unrun · **mode: co-run** (routing 2026-08-04 — the pack-disable click is hands; the rest stages)
**Bug:** destroy a tunnel, save/load IN VANILLA, order a colonist or rover
across — does the route still use the ruin? → [F38](agent/bugs/F38.md)
**Requirements:** a vanilla control (pack disabled is fine for this read) / a
destroyed tunnel.

### Rider — F76/C41: depot-picker recurrence · Status: unrun — ONLY if a depot click-load misbehaves again; do NOT go looking
**Bug:** the picker is vanilla and was measured CORRECT — it opens ABOVE the
cursor by its own height, which is intended; do not report that as
displacement. If a Load click ever misbehaves, capture with the two read-only
hooks BEFORE touching anything — and if the symptom is *no picker at all*,
that is the different, never-reproduced C41 witness: say so explicitly.
→ [F76](agent/bugs/F76.md), [C41](agent/bugs/C41.md)
**Requirements:** the symptom recurring — an RC Transport/Dozer depot or heap
Load click that misfires.
**Setup:** the agent hands the two hooks (entry) and records the desktop box /
multi-display geometry alongside.
**Good to have:** the known-good workaround while capturing (verified command):
`rc:SetCommand("TransferResources", depot, "load", "<Resource>", <amount*1000>, true)`.


### Rider ? vanillahunt 03 food seams ? Status: unrun ? fresh 1.1.0 fixtures only

- **C56 ranch forecast:** TAKEABLE WHEN a supplied Chicken ranch can complete
  a herd at reduced positive performance. Record active forecast before harvest
  and all producing despawns; [C56](agent/bugs/C56.md) has controls and vacuity.
- **C57 disabled ingredient:** TAKEABLE WHEN a DLC food service holds a delicacy
  that can remain stocked after its use is switched off. Observe a completed
  eligible meal before hauling/spoilage changes the amount; [C57](agent/bugs/C57.md).
- **C58 reserved food / spoilage:** TAKEABLE WHEN a raw-pile or Food-Depot meal
  reservation can remain outstanding through its actual decay tick. The agent
  reads physical, request and colonist counters; native outcome is unknown.
  The two paths have different tick timing; [C58](agent/bugs/C58.md).
- **C60 ranch UI allocation:** TAKEABLE WHEN item 136's FR-3 profiling is accepted
  or the ranch fixture already exists. Callback counts and attributed cost only;
  no source-only stutter verdict; [C60](agent/bugs/C60.md).
- **C61 death-popup wording:** TAKEABLE WHEN an isolated fresh colony has more
  than five colonists and a nonempty applicant pool, or a field report supplies
  the event. Preserve survivors and account for other pool mutations. Do not
  sacrifice the campaign; [C61](agent/bugs/C61.md).

These are candidate observations, not release gates or approvals to add fixes.
The terminal hunt audit owns any hotfix recommendation. C59/C62 have no
independently established player recipe and do not get artificial play legs.

### Rider — the both-packs stacked leg (re-filed from item 51, 2026-09-12) · Status: unrun

**What it measures:** the one thing this project has never watched — **two
independently written patches stacked on the same function**, live. Every
compatibility claim the pack makes is derived from reading code. The only
second mod we may legitimately use is our own opt-in pack, which patches
functions the fix pack also patches.

⚠️ **Ordinary play does NOT cover this.** Both mods have been loaded together
for months (the 2026-08-12 both-mods-loaded rule) and nothing has broken — that
is coverage-by-default, and it is why the leg keeps not being missed. It is not
the measurement: nobody has ever read what the stacked function actually does.

**Why it is takeable now (item 51's blockers are all gone):** run B scored 10/10
on 2026-08-19, the pack launched 2026-08-20, and the opt-in pack is enabled and
applying again (item 105, 9 modules, 2026-09-08).

⛔ **Re-derive the overlap before running it.** Item 51's "two of the same
functions" was counted at 80 fix-pack modules and 8 opt-in ones; the pack is now
49 modules and the opt-in pack has 9. The overlap set has NOT been recounted —
if it is now empty, the leg is vacuous and the finding is that, not a pass.

**Shape:** unattended, both mods enabled, ordinary boot. Read which wrapper runs
first on each shared function, whether both run, and whether either loses a
return value. `SMRFixPack.ListFixes()` on both packs is the census. Nothing here
is a release gate — it is information, by the owner's own 2026-08-19 ruling.
