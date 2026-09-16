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

Body archived in [archive/PLAYTEST_ARCHIVE.md](archive/PLAYTEST_ARCHIVE.md) under the heading "## ck191 -- archived 2026-09-16 (was checklist status:closed):" followed by this heading.

### ✅ 2026-09-16 — 190 RULED: C93 diagnosis excludes the mall-mod targets
<!-- ck:190 status:ruled owner:no -->

Owner ruling archived in [C93 diagnosis scope](archive/PLAYTEST_ARCHIVE.md#c93-diagnosis-scope-2026-09-16).
The ranch result is in [C93's diagnosis report](agent/reports/C93_RANCH_ORIGIN_DIAGNOSIS.md);
no further in-game diagnostic window is owed for this fired brief.

### 2026-09-16 — 188: Wildfire rider RAN — the fresh 1.1.0 path is healthy; one attribution question for you
<!-- ck:188 status:open owner:yes -->

✅ **RAN 2026-09-16, both legs, with you at the keyboard — no defect in the fresh 1.1.0 path.**
**Leg A:** the scenario's own reveal enabled `WildfireCure_1` from a 0-point baseline, the node was on
screen when you opened the tree, and the eleven-node chain opened link by link. The `14,580` on its
tooltip is a 20% research refund, not a price. **Leg B:** the organic chain ran to
`MysteryEnd "resolved"` — infection on Sol 33, cure revealed on Sol 53 against a predicted Sol 48-53
window. The only unbounded player gate is scanning the mystery's surface anomaly. Full record:
[Wildfire report](agent/reports/WILDFIRE_CURE_RESEARCH.md), Leg A and Leg B. A reply to the reporter
is pull-only — yours to request.

⚖️ **ONE QUESTION — whose report was this?** This item and F120 name Jäger (the brief at `03023c4`:
*"Same reporter as C99, different bug"*). On 2026-09-16 you showed Jäger's comment #8, which is C99's
tunnel bug, and said *"jager was completely different"*. Either Jäger also posted a Wildfire comment,
or another player did and the name is wrong in F120, the Wildfire report, this item and the handoff.
Say which and the attribution is corrected or confirmed; this item then closes.

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

Body archived in [archive/PLAYTEST_ARCHIVE.md](archive/PLAYTEST_ARCHIVE.md) under the heading "## ck189 -- archived 2026-09-16 (was checklist status:closed):" followed by this heading.

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

Body archived in [archive/PLAYTEST_ARCHIVE.md](archive/PLAYTEST_ARCHIVE.md) under the heading "## ck187 -- archived 2026-09-16 (was checklist status:ruled):" followed by this heading.

### 2026-09-16 — A prompt's citation does not keep evidence in the checklist
<!-- ck:- status:closed owner:no -->

Owner ruling archived in [Citations do not hold evidence](archive/PLAYTEST_ARCHIVE.md#citations-do-not-hold-evidence-2026-09-16).

### 2026-09-16 — Checklist archival: four answers on held items
<!-- ck:- status:closed owner:no -->

Owner ruling archived in [Checklist archival answers](archive/PLAYTEST_ARCHIVE.md#checklist-archival-answers-2026-09-16). Steam's branch-delivery finding is now `agent/facts/EF-105.md`. Item 22b's wording-evidence rule was then cut: [Wording-evidence rule cut](archive/PLAYTEST_ARCHIVE.md#wording-evidence-rule-cut-2026-09-16).

### 2026-09-16 — A release empties the outbox into the archive
<!-- ck:- status:closed owner:no -->

Owner ruling archived in [Release closes empty the outbox](archive/PLAYTEST_ARCHIVE.md#release-closes-empty-the-outbox-2026-09-16). Release history now lives in `archive/RELEASE_HISTORY.md`.

### 2026-09-16 — The tree is LF, and a mixed line ending is RED
<!-- ck:- status:closed owner:no -->

Owner ruling archived in [LF tree and RED mixed line endings](archive/PLAYTEST_ARCHIVE.md#lf-tree-and-red-mixed-line-endings-2026-09-16). Landed in `.gitattributes`, `tools/doccheck.py`'s EOL section, `tools/split_bugs.py` and `.claude/tools/archive_settled.py`.

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

Body archived in [archive/PLAYTEST_ARCHIVE.md](archive/PLAYTEST_ARCHIVE.md) under the heading "## ck185 -- archived 2026-09-16 (was checklist status:ruled):" followed by this heading.

### 2026-09-14 — 184 RULED + CLOSED 09-15: the probe-sweep gate is an age, never a refusal; the ck144 (a) boot ran and is DISCHARGED; the toolkit chain has nothing hanging

<!-- ck:184 status:ruled owner:yes -->

Body archived in [archive/PLAYTEST_ARCHIVE.md](archive/PLAYTEST_ARCHIVE.md) under the heading "## ck184 -- archived 2026-09-16 (was checklist status:ruled):" followed by this heading.

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
- **✅ DISCHARGED 2026-09-16 — the archiver is fixed; the 35 landed headers are left alone.**
  New archive headings carry the checklist heading whole, date included, and each new stub
  quotes the exact archive heading it points at; a trial apply found all 18 bodies that way.
  The 35 older stubs keep the old wording, which is the next bullet. It drops the leading
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

Body archived in [archive/PLAYTEST_ARCHIVE.md](archive/PLAYTEST_ARCHIVE.md) under the heading "## ck179 -- archived 2026-09-16 (was checklist status:ruled):" followed by this heading.

### ✅ 2026-09-14 — 178 RULED: STATE's warn cap is TEMPORARILY +25% — ⚠️ you end it, and only you

<!-- ck:178 status:ruled owner:yes -->

Body archived in [archive/PLAYTEST_ARCHIVE.md](archive/PLAYTEST_ARCHIVE.md) under the heading "## ck178 -- archived 2026-09-16 (was checklist status:ruled):" followed by this heading.

### ✅ 2026-09-14 — 177 RULED: retirement now covers EVERYTHING in this file, not just tests — ⚠️ one gate still yours
<!-- ck:177 status:ruled owner:no -->

Body archived in [archive/PLAYTEST_ARCHIVE.md](archive/PLAYTEST_ARCHIVE.md) under the heading "## ck177 -- archived 2026-09-16 (was checklist status:ruled):" followed by this heading.

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

Body archived in [archive/PLAYTEST_ARCHIVE.md](archive/PLAYTEST_ARCHIVE.md) under the heading "## ck175 -- archived 2026-09-16 (was checklist status:ruled):" followed by this heading.

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

Body archived in [archive/PLAYTEST_ARCHIVE.md](archive/PLAYTEST_ARCHIVE.md) under the heading "## ck174 -- archived 2026-09-16 (was checklist status:ruled):" followed by this heading.

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

Body archived in [archive/PLAYTEST_ARCHIVE.md](archive/PLAYTEST_ARCHIVE.md) under the heading "## ck170 -- archived 2026-09-16 (was checklist status:ruled):" followed by this heading.

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

### ✅ 2026-09-12 — 168 RULED BY YOU (batch 2): **98 → baseline moves to 1.1.0 · hardening row 3 → BUILT into v10 · 151 (c) → the three cheap checks join the owed boot.** ✅ **151 (b) came back as a question and is answered below; CLOSED 2026-09-16 — send nothing (ruling recorded at item 151).**
<!-- ck:168 status:ruled owner:no -->

Body archived in [archive/PLAYTEST_ARCHIVE.md](archive/PLAYTEST_ARCHIVE.md) under the heading "## ck168 -- archived 2026-09-16 (was checklist status:ruled):" followed by this heading.

### ✅ 2026-09-12 — 167 RULED BY YOU: **the opt-in mod's decisions move to the opt-in mod's repo.** Eleven items off your list; three stay because they bind the fix pack. **Nothing is owed from you.**
<!-- ck:167 status:ruled owner:no -->

Body archived in [archive/PLAYTEST_ARCHIVE.md](archive/PLAYTEST_ARCHIVE.md) under the heading "## ck167 -- archived 2026-09-16 (was checklist status:ruled):" followed by this heading.

### ✅ 2026-09-12 — 166 RULED BY YOU (batch 1 of the decision sweep): **133 (2) as a hybrid · 133 (4) label-only · 135 into hotfix 3.** All three landed the same session. **Nothing is owed from you.**
<!-- ck:166 status:ruled owner:no -->

Body archived in [archive/PLAYTEST_ARCHIVE.md](archive/PLAYTEST_ARCHIVE.md) under the heading "## ck166 -- archived 2026-09-16 (was checklist status:ruled):" followed by this heading.

### ✅ 2026-09-12 — 165 RULED BY YOU: **replies to players are PULL-ONLY from now on.** Nothing is owed from you, and no agent will raise one at you again unless you ask.
<!-- ck:165 status:ruled owner:no -->

Body archived in [archive/PLAYTEST_ARCHIVE.md](archive/PLAYTEST_ARCHIVE.md) under the heading "## ck165 -- archived 2026-09-16 (was checklist status:ruled):" followed by this heading.

### ✅ 2026-09-12 — 164 RULED BY YOU: **KEEP** — "fine as long as we are sure it won't cause issues." **The condition was checked, not assumed; it holds, and the check closed a gap.** Nothing further is owed.
<!-- ck:164 status:ruled owner:no -->

Body archived in [archive/PLAYTEST_ARCHIVE.md](archive/PLAYTEST_ARCHIVE.md) under the heading "## ck164 -- archived 2026-09-16 (was checklist status:ruled):" followed by this heading.

### ✅ 2026-09-12 — 163 RULED BY YOU: **all four — (a) accept · (b) yes · (c) confirm · (d) yes.** Items 137/138/140/141/142 CLOSE with (a); **(b) RAN AND FOUND NOTHING** (`reports/PINNED_PARENTS_PASS.md`); (d) is BUILT and surfaced a new call (**164**). **Nothing is owed from you here.**
<!-- ck:163 status:ruled owner:no -->

Body archived in [archive/PLAYTEST_ARCHIVE.md](archive/PLAYTEST_ARCHIVE.md) under the heading "## ck163 -- archived 2026-09-16 (was checklist status:ruled):" followed by this heading.

### ✅ 2026-09-12 — 162 FULLY RULED: **(a) leave dropped · (b) cut · (c) declined on cost, C87 is file-and-watch · (d) closed with item 73.** **Nothing is owed from you; all four §4 loose ends are shut.**
<!-- ck:162 status:ruled owner:no -->

Body archived in [archive/PLAYTEST_ARCHIVE.md](archive/PLAYTEST_ARCHIVE.md) under the heading "## ck162 -- archived 2026-09-16 (was checklist status:ruled):" followed by this heading.

### ✅ 2026-09-12 — 161 CLARIFIED BY YOU: the 09-08 "we don't chase small positives" rule was **triage for the 1.1.0 emergency**, not standing policy — and it expired with the emergency. There was never a contradiction. **Nothing is owed from you; three documents stop asking.**
<!-- ck:161 status:ruled owner:no -->

Body archived in [archive/PLAYTEST_ARCHIVE.md](archive/PLAYTEST_ARCHIVE.md) under the heading "## ck161 -- archived 2026-09-16 (was checklist status:ruled):" followed by this heading.

### ✅ 2026-09-12 — 160 RULED BY YOU: **(b) — let it ride with v10.** This is ordinary release-lane work, not a separate decision. **Nothing is owed from you; the original ask is kept below.**
<!-- ck:160 status:ruled owner:no -->

Body archived in [archive/PLAYTEST_ARCHIVE.md](archive/PLAYTEST_ARCHIVE.md) under the heading "## ck160 -- archived 2026-09-16 (was checklist status:ruled):" followed by this heading.

### ✅ 2026-09-12 — 158 RAN 09-12: all three attended in one boot; C85, C89 and C88 are `tested-attended`. **Nothing owed from you — the v10 gate is clear.**
<!-- ck:158 status:closed owner:no -->

Body archived in [archive/PLAYTEST_ARCHIVE.md](archive/PLAYTEST_ARCHIVE.md) under the heading "## ck158 -- archived 2026-09-16 (was checklist status:closed):" followed by this heading.

### ✅ 2026-09-12 — 159 RULED 09-12: F31 retires, F37's load-time clean-up is a loss you accept, and every sentence replacement goes in. **Nothing owed from you; the release lane carries it into v10.**
<!-- ck:159 status:ruled owner:no -->

Body archived in [archive/PLAYTEST_ARCHIVE.md](archive/PLAYTEST_ARCHIVE.md) under the heading "## ck159 -- archived 2026-09-16 (was checklist status:ruled):" followed by this heading.

### ⏸ 2026-09-12 — 157 — **OFF YOUR OWED LIST 2026-09-12 under the pull-only ruling (165).** Both calls are messaging, not fixing: (a) the reporter reply is a **draft waiting in `docs/FIELD_REPORT_REPLIES.md`, pulled when you want it** · (b) the developer note is **yours to route whenever** — ⚠️ worth knowing it carries more weight than an ordinary reply, because two Paradox developers plan hotfixes from our fix list, but it is still not owed and no agent will raise it again. ⛔ **The triage underneath this item stands and is unaffected.** Original ask kept below.
<!-- ck:157 status:closed owner:no -->

Body archived in [archive/PLAYTEST_ARCHIVE.md](archive/PLAYTEST_ARCHIVE.md) under the heading "## ck157 -- archived 2026-09-16 (was checklist status:closed):" followed by this heading.

### 2026-09-12 — 157 (the original ask): new Steam report, "Prosperity for Mars angry about unemployment with 0 unemployed" — triaged, not ours. **Your pushback checked out: it is an oversight, and the developers' own fix exists in one faction out of five. Three decisions: (a) post the reporter reply, (b) hand it to the developers, (c) carry a judgment-call fix ourselves. Recommendations: (a) yes, (b) yes, (c) not yet — wait for their answer.**
<!-- ck:157 status:closed owner:no -->

Body archived in [archive/PLAYTEST_ARCHIVE.md](archive/PLAYTEST_ARCHIVE.md) under the heading "## ck157 -- archived 2026-09-16 (was checklist status:closed):" followed by this heading.

### ✅ 2026-09-12 — 156 RULED: retire the farm-oxygen and layout fixes, the frozen 1.0.7 build stays as it is, the wording goes out in your voice. **Nothing owed from you until the audit reports.**
<!-- ck:156 status:ruled owner:no -->

Body archived in [archive/PLAYTEST_ARCHIVE.md](archive/PLAYTEST_ARCHIVE.md) under the heading "## ck156 -- archived 2026-09-16 (was checklist status:ruled):" followed by this heading.

### ✅ 2026-09-11 — 155 CLOSED 09-12: you answered the upload receipts, and the answer is standing — **the documents will stop asking.**
<!-- ck:155 status:closed owner:no -->

Body archived in [archive/PLAYTEST_ARCHIVE.md](archive/PLAYTEST_ARCHIVE.md) under the heading "## ck155 -- archived 2026-09-16 (was checklist status:closed):" followed by this heading.

### ✅ 2026-09-11 — 154 RULED 09-12: sweep only, the safest version. **Build prompt: `agent/prompts/C85_C88_BUILD.md` (with C88). Nothing else owed here; the attended check comes back as its own item when built.**
<!-- ck:154 status:ruled owner:no -->

Body archived in [archive/PLAYTEST_ARCHIVE.md](archive/PLAYTEST_ARCHIVE.md) under the heading "## ck154 -- archived 2026-09-16 (was checklist status:ruled):" followed by this heading.

### ✅ 2026-09-11 — 153 RULED 09-12: the Reddit "160% productivity" thread is NOT a bug — **post the reply: yes.** The draft is approved; posting is yours whenever you want it.
<!-- ck:153 status:ruled owner:no -->

Body archived in [archive/PLAYTEST_ARCHIVE.md](archive/PLAYTEST_ARCHIVE.md) under the heading "## ck153 -- archived 2026-09-16 (was checklist status:ruled):" followed by this heading.

### ✅ 2026-09-11 — 152 FULLY RULED: **F59's A2 half is `tested-attended`** (09-12) · **(e)'s three overclaiming rows sweep with the v10 site publish** (09-12) · **(c) CLOSED 09-12 — the kick button is DESIGN, not a defect. Nothing is owed from you.**
<!-- ck:152 status:ruled owner:no -->

Body archived in [archive/PLAYTEST_ARCHIVE.md](archive/PLAYTEST_ARCHIVE.md) under the heading "## ck152 -- archived 2026-09-16 (was checklist status:ruled):" followed by this heading.

### ✅ 2026-09-11 — 151: migration audit complete — **(a) and (d) CLOSED 09-12 as overtaken by events · (e) RULED 09-11 · (c) RULED 09-12 at item 168 · (b) CLOSED 2026-09-16: send nothing. Nothing is owed from you.**
<!-- ck:151 status:closed owner:no -->

Body archived in [archive/PLAYTEST_ARCHIVE.md](archive/PLAYTEST_ARCHIVE.md) under the heading "## ck151 -- archived 2026-09-16 (was checklist status:closed):" followed by this heading.

### ✅ 2026-09-11 — 150 CLOSED 09-12: all three decided. **(a) you posted the developer reply · (b) built as option 1 with the law's own id · (c) retire, ruled by item 156.**
<!-- ck:150 status:closed owner:no -->

Body archived in [archive/PLAYTEST_ARCHIVE.md](archive/PLAYTEST_ARCHIVE.md) under the heading "## ck150 -- archived 2026-09-16 (was checklist status:closed):" followed by this heading.

### ✅ 2026-09-11 — 149 RAN: F119 and C86 are both TESTED-ATTENDED (you at the keyboard). **Nothing to decide here; the upload is your separate action (`agent/prompts/perma/RELEASE.md`).** The original steps are kept below.
<!-- ck:149 status:ruled owner:no -->

Body archived in [archive/PLAYTEST_ARCHIVE.md](archive/PLAYTEST_ARCHIVE.md) under the heading "## ck149 -- archived 2026-09-16 (was checklist status:ruled):" followed by this heading.

### ⏳ 2026-09-11 — 148 DEFERRED 09-12 (you said **skip**; the chain is NOT started) — an on/off button for every fix. **Decisions: (a) how console players reach the buttons, (b) whether this counts as a "major overhaul" for the release gate, (c) accept that the first prompt re-checks how the chain was cut. Recommendations: (a) our own panel, proven on a controller before it is built out, falling back to the game's built-in Mod Options page; (b) no extra sweep — the chain's own final audit and its two sittings are the gate; (c) yes.**
<!-- ck:148 status:deferred owner:no -->

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

Body archived in [archive/PLAYTEST_ARCHIVE.md](archive/PLAYTEST_ARCHIVE.md) under the heading "## ck146 -- archived 2026-09-16 (was checklist status:ruled):" followed by this heading.

### ✅ 2026-09-11 — 147 CLOSED 09-12: **cleared by you.** The original triage is kept below. Nothing here is owed from you.
<!-- ck:147 status:closed owner:no -->

Body archived in [archive/PLAYTEST_ARCHIVE.md](archive/PLAYTEST_ARCHIVE.md) under the heading "## ck147 -- archived 2026-09-16 (was checklist status:closed):" followed by this heading.

### 2026-09-11 — 145: FR-1 cache probe v2 covers all 18 RAYS records; test normal loading first.
<!-- ck:145 status:ruled owner:no -->

Body archived in [archive/PLAYTEST_ARCHIVE.md](archive/PLAYTEST_ARCHIVE.md) under the heading "## ck145 -- archived 2026-09-16 (was checklist status:ruled):" followed by this heading.

### ✅ 2026-09-10 — v7 IS LIVE on both stores (your word). Nothing to decide; three things to tell me when convenient.
<!-- ck:- status:closed owner:no -->

Body archived in [archive/PLAYTEST_ARCHIVE.md](archive/PLAYTEST_ARCHIVE.md); search `ck-` and this heading.

### ✅ 2026-09-10 — 144 CLOSED 09-12: **(b) cleared by you.** Two small asks around the v7 upload; neither blocked it.
<!-- ck:144 status:closed owner:no -->

Body archived in [archive/PLAYTEST_ARCHIVE.md](archive/PLAYTEST_ARCHIVE.md) under the heading "## ck144 -- archived 2026-09-16 (was checklist status:closed):" followed by this heading.

### ✅ 2026-09-10 — 143 CLOSED: **FIX BUILT + TESTED-ATTENDED** — new arrivals no longer fall back into a switched-off, quarantined dome ([C83](agent/bugs/C83.md)).
<!-- ck:143 status:closed owner:no -->

Body archived in [archive/PLAYTEST_ARCHIVE.md](archive/PLAYTEST_ARCHIVE.md) under the heading "## ck143 -- archived 2026-09-16 (was checklist status:closed):" followed by this heading.

### ✅ 2026-09-10 — 144 CLOSED: C83's homeless follow-through found a distinct intentional override, not another fix ([C84](agent/bugs/C84.md)). No decision is owed.
<!-- ck:144 status:closed owner:no -->

Body archived in [archive/PLAYTEST_ARCHIVE.md](archive/PLAYTEST_ARCHIVE.md) under the heading "## ck144 -- archived 2026-09-16 (was checklist status:closed):" followed by this heading.

### ✅ 2026-09-10 — 142 — **CLOSED 2026-09-12 by your ruling of item 163 (a)**, which dispositioned all 25 source-only candidates as four groups rather than one by one: the 12 P2s land in the four groups; **no hotfix-3 list is named**, which is what the recommendation asked for. **Nothing is owed from you; the original ask is kept below as the reasoning.** ⛔ A disposition, not a dismissal — a field report naming any candidate reopens it instantly.: the vanillahunt terminal audit re-derived every P2 candidate — which of these, if any, go to a hotfix-3 candidate list? **Decision: name any entry you want on a hotfix-3 candidate list, or accept "file and watch" for all. Recommendation: none today; take C66 and C82 as cheap organic looks and leave the rest.**
<!-- ck:142 status:closed owner:no -->

Body archived in [archive/PLAYTEST_ARCHIVE.md](archive/PLAYTEST_ARCHIVE.md) under the heading "## ck142 -- archived 2026-09-16 (was checklist status:closed):" followed by this heading.

### ✅ 2026-09-10 — 141 — **CLOSED 2026-09-12 by your ruling of item 163 (a)**, which dispositioned all 25 source-only candidates as four groups rather than one by one: C79/C80/C81/C62 are dispositioned — C80 **REFUTED** (status flipped today), the rest source-only. **Nothing is owed from you; the original ask is kept below as the reasoning.** ⛔ A disposition, not a dismissal — a field report naming any candidate reopens it instantly. rider: vanillahunt 04 left three functional candidates and two profiling reads; none is a release gate. **Decision: take only a naturally available 1.1 fixture, or leave them source-only. Recommendation: prioritize C79; take C80 only on a disposable elevator save, and leave the profiling reads until a large colony already exists.**
<!-- ck:141 status:closed owner:no -->

Body archived in [archive/PLAYTEST_ARCHIVE.md](archive/PLAYTEST_ARCHIVE.md) under the heading "## ck141 -- archived 2026-09-16 (was checklist status:closed):" followed by this heading.

### ✅ 2026-09-10 — 140 — **CLOSED 2026-09-12 by your ruling of item 163 (a)**, which dispositioned all 25 source-only candidates as four groups rather than one by one: C75 + C76 need no fixture; C75 is a group B **player benefit**. **Nothing is owed from you; the original ask is kept below as the reasoning.** ⛔ A disposition, not a dismissal — a field report naming any candidate reopens it instantly. rider: The Incident can answer two source-only candidates in one fresh fixture. **Decision: test it only if a fresh 1.1 colony naturally has two working Fusion Reactors, or leave both candidates source-only. Recommendation: fold the two reads together; neither is a release gate.**
<!-- ck:140 status:closed owner:no -->

Body archived in [archive/PLAYTEST_ARCHIVE.md](archive/PLAYTEST_ARCHIVE.md) under the heading "## ck140 -- archived 2026-09-16 (was checklist status:closed):" followed by this heading.

### ✅✅ 2026-09-10 — 139 BUILT + TESTED-ATTENDED: all seven silent units (C74 hammer + MOXIE, C77's five), Metatron left out. `Fix_SilentHitMomentFX.lua`; old saves heal without a power cycle; staged for the next release. Nothing is owed from you.
<!-- ck:139 status:closed owner:no -->

Body archived in [archive/PLAYTEST_ARCHIVE.md](archive/PLAYTEST_ARCHIVE.md); search `ck139` and this heading.

### ✅ 2026-09-10 — 138 — **CLOSED 2026-09-12 by your ruling of item 163 (a)**, which dispositioned all 25 source-only candidates as four groups rather than one by one: the eight caller-seam candidates are dispositioned; **C66 stays a group A organic rider**, never provisioned for. **Nothing is owed from you; the original ask is kept below as the reasoning.** ⛔ A disposition, not a dismissal — a field report naming any candidate reopens it instantly. rider: eight caller-seam candidates need fresh 1.1 fixtures; none is a release gate. **Decision: take only the naturally available fixture(s), or leave the candidates source-only. Recommendation: prioritize C66 and fold C67/C68 together if a food-service fixture is already available.**
<!-- ck:138 status:closed owner:no -->

Body archived in [archive/PLAYTEST_ARCHIVE.md](archive/PLAYTEST_ARCHIVE.md) under the heading "## ck138 -- archived 2026-09-16 (was checklist status:closed):" followed by this heading.

### ✅ 2026-09-10 — 137 — **CLOSED 2026-09-12 by your ruling of item 163 (a)**, which dispositioned all 25 source-only candidates as four groups rather than one by one: the three politics candidates stay source-only; no colony is provisioned for them. **Nothing is owed from you; the original ask is kept below as the reasoning.** ⛔ A disposition, not a dismissal — a field report naming any candidate reopens it instantly. rider: three vanilla politics candidates need a fresh 1.1 colony, never the branch-locked campaign. **Decision: provision one politics fixture when convenient, or leave all three source-only. Recommendation: provision only if the ordinary play setup can cover them together.**
<!-- ck:137 status:closed owner:no -->

Body archived in [archive/PLAYTEST_ARCHIVE.md](archive/PLAYTEST_ARCHIVE.md) under the heading "## ck137 -- archived 2026-09-16 (was checklist status:closed):" followed by this heading.

### 2026-09-10 — 136: three player reports are now priority surfaces in the vanilla diff hunt. Two asks; neither needs the keyboard.
<!-- ck:136 status:open owner:yes -->

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

Body archived in [archive/PLAYTEST_ARCHIVE.md](archive/PLAYTEST_ARCHIVE.md) under the heading "## ck135 -- archived 2026-09-16 (was checklist status:ruled):" followed by this heading.

### ✅ 2026-09-10 — 134 CLOSED 09-12 as overtaken: the models were assigned, the chain ran end to end, and its audit closed it on 09-10. **Nothing is owed from you.**
<!-- ck:134 status:closed owner:no -->

Body archived in [archive/PLAYTEST_ARCHIVE.md](archive/PLAYTEST_ARCHIVE.md) under the heading "## ck134 -- archived 2026-09-16 (was checklist status:closed):" followed by this heading.

### ✅ 2026-09-09 — HOTFIX 2 IS LIVE AS v6 ON BOTH STORES, AND THE SITE IS PUBLISHED. This is the receipt; nothing is owed from you tonight.
<!-- ck:- status:closed owner:no -->

Body archived in [archive/PLAYTEST_ARCHIVE.md](archive/PLAYTEST_ARCHIVE.md) under the heading "## ck- -- archived 2026-09-16 (was checklist status:closed):" followed by this heading.

### ✅ 2026-09-09 — `100_DOCSWEEP` IS DONE: the words now match the pack that ships. The hotfix-2 chain is closed; the only thing left is your upload sitting.
<!-- ck:- status:closed owner:no -->

Body archived in [archive/PLAYTEST_ARCHIVE.md](archive/PLAYTEST_ARCHIVE.md); search `ck-` and this heading.

### ✅ 2026-09-09 — 133: six decisions from the self-check promise audit. **RULED IN PART 2026-09-12 — "do the reword". Four of the six fall with it; (2) and (4) were RULED the same day (ck166 a + b) and landed in `FIX_POLICY` §2a (i) + (ii). CLOSED 2026-09-16 — nothing is owed from you.**
<!-- ck:133 status:ruled owner:no -->

Body archived in [archive/PLAYTEST_ARCHIVE.md](archive/PLAYTEST_ARCHIVE.md) under the heading "## ck133 -- archived 2026-09-16 (was checklist status:ruled):" followed by this heading.

### 🎮 2026-09-09 — THE SITTING RAN. Tier 1 is complete and green; what it still owes is below.
<!-- ck:- status:closed owner:no -->

Body archived in [archive/PLAYTEST_ARCHIVE.md](archive/PLAYTEST_ARCHIVE.md) under the heading "## ck- -- archived 2026-09-16 (was checklist status:closed):" followed by this heading.

### ✅ CLOSED 2026-09-09 — the brief that produced the block above was consumed 2026-09-15 after ck184 discharged the remaining play clauses. The historical two-tier plan stays below.
<!-- ck:- status:closed owner:no -->

Body archived in [archive/PLAYTEST_ARCHIVE.md](archive/PLAYTEST_ARCHIVE.md) under the heading "## ck- -- archived 2026-09-16 (was checklist status:closed):" followed by this heading.

### 2026-09-09 — 131: the F117 fix has LANDED. It is the last code in hotfix 2. One small question for you, and one thing the sitting now owes.
<!-- ck:131 status:closed owner:no -->

Body archived in [archive/PLAYTEST_ARCHIVE.md](archive/PLAYTEST_ARCHIVE.md) under the heading "## ck131 -- archived 2026-09-16 (was checklist status:closed):" followed by this heading.

### ✅ 2026-09-09 — RULED: all three of link 99's calls, plus one new one (130). Every gate on the doc sweep is now satisfied. ✅ **Nothing is owed from you until the sitting.**
<!-- ck:- status:ruled owner:no -->

Body archived in [archive/PLAYTEST_ARCHIVE.md](archive/PLAYTEST_ARCHIVE.md) under the heading "## ck99 -- archived 2026-09-16 (was checklist status:ruled):" followed by this heading.

### ⚖️ 2026-09-09 — LINK 99 IS DONE. VERDICT: **SHIP WITH CHANGES.** Three calls (127–129) — ✅ **ALL THREE RULED**, see the block above; the first is the reason for the verdict, and it is a real bug the pack already ships.
<!-- ck:- status:closed owner:no -->

Body archived in [archive/PLAYTEST_ARCHIVE.md](archive/PLAYTEST_ARCHIVE.md) under the heading "## ck99 -- archived 2026-09-16 (was checklist status:closed):" followed by this heading.

### ✅ 2026-09-09 — RULED AND DONE: you raised the `STATE.md` byte cap to 12 KiB, and item 126 is now IN it. Nothing owed; this is the receipt.
<!-- ck:- status:ruled owner:no -->

Body archived in [archive/PLAYTEST_ARCHIVE.md](archive/PLAYTEST_ARCHIVE.md) under the heading "## ck12 -- archived 2026-09-16 (was checklist status:ruled):" followed by this heading.

### ✅ 2026-09-09 — ITEM 126 RULED: **KEEP THE PASS IN** (see the ruling block at the top of this section). Left below as the reasoning you ruled on; link 08 wrote a pass that cleans up after **us**, and it changes what "remove the save sanitizer" means
<!-- ck:126 status:ruled owner:no -->

Body archived in [archive/PLAYTEST_ARCHIVE.md](archive/PLAYTEST_ARCHIVE.md) under the heading "## ck126 -- archived 2026-09-16 (was checklist status:ruled):" followed by this heading.

### ⭐ 2026-09-09 — LINK 07 IS DONE: the Test Kit now tells the truth about this build, and it can CHECK the 36 removals. ✅ **Nothing is owed from you now. One thing to read before you run the suite: the expected census below.**
<!-- ck:- status:closed owner:no -->

Body archived in [archive/PLAYTEST_ARCHIVE.md](archive/PLAYTEST_ARCHIVE.md) under the heading "## ck7 -- archived 2026-09-16 (was checklist status:closed):" followed by this heading.

### ⭐ 2026-09-09 — LINK 06 IS DONE: the store card and the site now describe the pack that actually ships. ✅ **Nothing is owed from you — but ONE thing must happen at the sitting, and it is easy to miss.**
<!-- ck:- status:closed owner:no -->

Body archived in [archive/PLAYTEST_ARCHIVE.md](archive/PLAYTEST_ARCHIVE.md) under the heading "## ck6 -- archived 2026-09-16 (was checklist status:closed):" followed by this heading.

### ⭐ 2026-09-08 — LINK 03 IS DONE: three repairs. ✅ **THEIR CONTROLS ARE DEFERRED TO ONE SITTING AFTER THE CHAIN, ON YOUR CALL. Nothing is owed from you now.**
<!-- ck:- status:closed owner:no -->

Body archived in [archive/PLAYTEST_ARCHIVE.md](archive/PLAYTEST_ARCHIVE.md) under the heading "## ck3 -- archived 2026-09-16 (was checklist status:closed):" followed by this heading.

### ⭐ 2026-09-08 — LINK 04 IS DONE: two re-copies (F-6, F-7) and the F116 edit you ruled (111 + 119). ✅ **Nothing is owed from you now; three in-play checks JOIN the post-99 sitting above.**
<!-- ck:- status:closed owner:no -->

Body archived in [archive/PLAYTEST_ARCHIVE.md](archive/PLAYTEST_ARCHIVE.md) under the heading "## ck4 -- archived 2026-09-16 (was checklist status:closed):" followed by this heading.

### ⭐ 2026-09-09 — LINK 04b IS DONE: the three fixes you ruled back in (123) are RE-ARMED on their 1.1.0 bodies, gates kept. ✅ **Nothing is owed from you now; three in-play checks and one 1-minute console read JOIN the post-99 sitting above.**
<!-- ck:- status:closed owner:no -->

Body archived in [archive/PLAYTEST_ARCHIVE.md](archive/PLAYTEST_ARCHIVE.md) under the heading "## ck123 -- archived 2026-09-16 (was checklist status:closed):" followed by this heading.

### 2026-09-09 — ITEM 125 OPEN: the first checks the 1.0.7 tree makes possible were run — one real finding, one bounded reading pass to decide on, before 05 fires
<!-- ck:125 status:closed owner:no -->

Body archived in [archive/PLAYTEST_ARCHIVE.md](archive/PLAYTEST_ARCHIVE.md) under the heading "## ck125 -- archived 2026-09-16 (was checklist status:closed):" followed by this heading.

### ✅ 2026-09-08 — ITEM 124 RULED: `StaleReservations` is FIXED, not removed. This was the last thing blocking chain link 03.
<!-- ck:124 status:ruled owner:no -->

Body archived in [archive/PLAYTEST_ARCHIVE.md](archive/PLAYTEST_ARCHIVE.md) under the heading "## ck124 -- archived 2026-09-16 (was checklist status:ruled):" followed by this heading.

### ✅✅ 2026-09-08 — ITEMS 98, 117 AND 120 RULED IN-SESSION AND ACTIONED THE SAME HOUR. Nothing here is owed from you; one 3-minute control is offered at the bottom and it is optional.
<!-- ck:98 status:ruled owner:no -->

Body archived in [archive/PLAYTEST_ARCHIVE.md](archive/PLAYTEST_ARCHIVE.md) under the heading "## ck98 -- archived 2026-09-16 (was checklist status:ruled):" followed by this heading.

### 2026-09-08 — ITEM 118: how 1.0.7 players get served — Steam's branch feature is OFF, so it is one manual route
<!-- ck:118 status:ruled owner:no -->

Body archived in [archive/PLAYTEST_ARCHIVE.md](archive/PLAYTEST_ARCHIVE.md) under the heading "## ck118 -- archived 2026-09-16 (was checklist status:ruled):" followed by this heading.

### 2026-09-08 — ITEMS 114–117 OPEN: the pack-wide 1.1.0 re-verification — 10 FIX, 35 REMOVE, 35 KEEP (QA'd)
<!-- ck:- status:closed owner:no -->

Body archived in [archive/PLAYTEST_ARCHIVE.md](archive/PLAYTEST_ARCHIVE.md) under the heading "## ck114 -- archived 2026-09-16 (was checklist status:closed):" followed by this heading.

### 2026-09-08 — ITEMS 112–113 OPEN: the hotfix-1 audit says SHIP WITH CHANGES, and both changes are wording
<!-- ck:- status:closed owner:no -->

Body archived in [archive/PLAYTEST_ARCHIVE.md](archive/PLAYTEST_ARCHIVE.md) under the heading "## ck112 -- archived 2026-09-16 (was checklist status:closed):" followed by this heading.

### 2026-09-08 — ITEM 111 OPEN: F116 track salvage was repaired, and it left one judgement call
<!-- ck:111 status:ruled owner:no -->

Body archived in [archive/PLAYTEST_ARCHIVE.md](archive/PLAYTEST_ARCHIVE.md) under the heading "## ck111 -- archived 2026-09-16 (was checklist status:ruled):" followed by this heading.

### 2026-09-08 — ITEMS 98–101: the game shipped **1.1.0 + the first DLC**, and the rig auto-updated. **99, 100 and 101 all CLOSED 09-12 as overtaken; 98's rig half stays open (⛔ Steam = ONE branch at a time).**
<!-- ck:- status:closed owner:no -->

Body archived in [archive/PLAYTEST_ARCHIVE.md](archive/PLAYTEST_ARCHIVE.md) under the heading "## ck98 -- archived 2026-09-16 (was checklist status:closed):" followed by this heading.

### ✅ 2026-09-01 — ITEMS 89–97 **OFFLOADED to the opt-in repo 2026-09-12 (ck167).** Item **88 STAYS** — it is a fix-pack feature. **Nothing here is owed from you.**
<!-- ck:- status:closed owner:no -->

Body archived in [archive/PLAYTEST_ARCHIVE.md](archive/PLAYTEST_ARCHIVE.md) under the heading "## ck89 -- archived 2026-09-16 (was checklist status:closed):" followed by this heading.

### ✅ 2026-08-31 — ITEM 87 RULED THE SAME DAY: drones UNFROZEN
<!-- ck:87 status:ruled owner:no -->

Body archived in [archive/PLAYTEST_ARCHIVE.md](archive/PLAYTEST_ARCHIVE.md) under the heading "## ck87 -- archived 2026-09-16 (was checklist status:ruled):" followed by this heading.

### ✅ 2026-08-31 — ITEMS 83–86: **84 and 85 OFFLOADED to the opt-in repo 2026-09-12 (ck167). 83 and 86 STAY — they bind the fix pack, not that mod.**
<!-- ck:- status:ruled owner:no -->

Body archived in [archive/PLAYTEST_ARCHIVE.md](archive/PLAYTEST_ARCHIVE.md) under the heading "## ck83 -- archived 2026-09-16 (was checklist status:ruled):" followed by this heading.

### ✅ 2026-08-30 — ITEM 82 CLOSED: F110 live on both stores in v5, site deployed, delivered Steam pack verified. Nothing owed.
<!-- ck:82 status:closed owner:no -->

Body archived in [archive/PLAYTEST_ARCHIVE.md](archive/PLAYTEST_ARCHIVE.md) under the heading "## ck82 -- archived 2026-09-16 (was checklist status:closed):" followed by this heading.

### ✅ 2026-08-29 — ITEM 81 DONE, you ran it 18:44Z and the site is fully deployed. ITEM 80 WITHDRAWN IN FULL, both halves. Nothing is owed on the site or either store.
<!-- ck:- status:closed owner:no -->

Body archived in [archive/PLAYTEST_ARCHIVE.md](archive/PLAYTEST_ARCHIVE.md) under the heading "## ck81 -- archived 2026-09-16 (was checklist status:closed):" followed by this heading.

### ✅ 2026-08-24 — ITEM 79 IS DONE. You ran it on 08-24 and again on 08-28; verified 2026-08-29 against the deployments API. The original text is kept below as the record.
<!-- ck:79 status:closed owner:no -->

Body archived in [archive/PLAYTEST_ARCHIVE.md](archive/PLAYTEST_ARCHIVE.md) under the heading "## ck79 -- archived 2026-09-16 (was checklist status:closed):" followed by this heading.

### ⛔ 2026-08-24 — ITEM 78 IS WITHDRAWN. I asked you to decide something you had already done, on a tool reading that was wrong. Both reporters are answered. Nothing is owed.
<!-- ck:78 status:closed owner:no -->

Body archived in [archive/PLAYTEST_ARCHIVE.md](archive/PLAYTEST_ARCHIVE.md) under the heading "## ck78 -- archived 2026-09-16 (was checklist status:closed):" followed by this heading.

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

Body archived in [archive/PLAYTEST_ARCHIVE.md](archive/PLAYTEST_ARCHIVE.md) under the heading "## ck76 -- archived 2026-09-16 (was checklist status:closed):" followed by this heading.

### ⭐⭐ 2026-08-23 — THE FIRST FIELD REPORTS ARRIVED. Two GitHub issues, one reporter, and the pack was named in both. Neither error was ours. **73 CLOSED 09-12: not worth further resources.**
<!-- ck:73 status:closed owner:no -->

Body archived in [archive/PLAYTEST_ARCHIVE.md](archive/PLAYTEST_ARCHIVE.md) under the heading "## ck73 -- archived 2026-09-16 (was checklist status:closed):" followed by this heading.

### ⭐⭐⭐ 2026-08-20 — IT IS PUBLISHED, ON BOTH PORTALS. The ids are committed. One number came out differently on each store, and that was mechanical, not a mistake.
<!-- ck:- status:closed owner:no -->

Body archived in [archive/PLAYTEST_ARCHIVE.md](archive/PLAYTEST_ARCHIVE.md); search `ck-` and this heading.

### ⭐⭐ 2026-08-20 — THE AUDIT IS DONE. VERDICT: SHIP. The repo's active work ends here; the upload sitting is yours whenever you want it.
<!-- ck:- status:closed owner:no -->

Body archived in [archive/PLAYTEST_ARCHIVE.md](archive/PLAYTEST_ARCHIVE.md) under the heading "## ck- -- archived 2026-09-16 (was checklist status:closed):" followed by this heading.

### ✅✅ 2026-08-20 — YOUR SITTING IS DONE AND BOTH FIXES WORK. Nothing here is owed from you; this is the receipt.
<!-- ck:- status:closed owner:no -->

Body archived in [archive/PLAYTEST_ARCHIVE.md](archive/PLAYTEST_ARCHIVE.md) under the heading "## ck- -- archived 2026-09-16 (was checklist status:closed):" followed by this heading.

### ⛔⛔ 2026-08-20 — the sitting's prep found a real defect in `C50` (RULED: fix it). Kept as the record of the call.
<!-- ck:- status:closed owner:no -->

Body archived in [archive/PLAYTEST_ARCHIVE.md](archive/PLAYTEST_ARCHIVE.md) under the heading "## ck- -- archived 2026-09-16 (was checklist status:closed):" followed by this heading.

### ⚠️ 2026-08-20 — THE PAGES AND THE RELEASE SHEET ARE CAUGHT UP (link 3 done). One small thing wants your word, and the next link is the one that needs your hands.
<!-- ck:- status:closed owner:no -->

Body archived in [archive/PLAYTEST_ARCHIVE.md](archive/PLAYTEST_ARCHIVE.md) under the heading "## ck- -- archived 2026-09-16 (was checklist status:closed):" followed by this heading.

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

Body archived in [archive/PLAYTEST_ARCHIVE.md](archive/PLAYTEST_ARCHIVE.md) under the heading "## ck34 -- archived 2026-09-16 (was checklist status:closed):" followed by this heading.

### ✅ 2026-08-20 — your two rulings are carried out. Nothing owed back; this is the receipt.
<!-- ck:- status:closed owner:no -->

Body archived in [archive/PLAYTEST_ARCHIVE.md](archive/PLAYTEST_ARCHIVE.md); search `ck-` and this heading.

### ⭐⭐ 2026-08-19 — THE VERDICT REVIEW IS DONE: **UPHELD**. **53 RULED 09-12: pare the modder surface down, and the hardening queue shrinks with it. ✅ CLOSED 2026-09-16: row 3 was built 09-12 (ck168, shipped v10) and rows 1 + 2 were built 09-16 on your word. Nothing is owed from you.**
<!-- ck:53 status:closed owner:no -->

> ✅ **Your word, 2026-09-16, on rows 1 + 2:** *"If you can easily enact C without needing any
> play testing i am fine with that"* — option C was "build them", against leaving them on the watch
> list or marking them won't-fix. Built as a desk-only change in `Code/00_Core.lua`, **not
> playtested, by that condition**: a non-table `SMRFixPack_Disabled`, `SMRFixPack_Optional` or
> `SMRFixPack` is replaced with an empty table and named in the log; `SMRFixPack`'s four
> sub-tables are refilled when missing or mistyped; every veto and override read goes through a
> `pcall`, so a throwing `__index` no longer takes a module down. ⚖️ **One departure from the
> audit's closing form:** it named `rawget`; the `pcall` closes the same throwing case while
> keeping a metatable default working, which `rawget` would have silently dropped. Control:
> `python tools/desk_ck53_hostile_globals.py` — 13/13 on the new core, and on the pre-fix core all
> 8 hostile cases FAIL while the 5 controls PASS. No public row: nothing a player sees changes.

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

    * ✅ **Rows 1 and 2 — BUILT 2026-09-16 on your word (see the top of this item).** Kept as
      written on 09-12 below. **Rows 1 and 2 — DEPRIORITISED BY THIS RULING. Not fixed, not closed.** Their entire
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
    * ✅ **Row 3 — BUILT 2026-09-12 (ck168, `5665ee2`), shipped in v10:** a per-colonist `pcall`
      in the daily sweep. Kept as written before that: ⛔ **Row 3 — STILL OPEN, and INDEPENDENT of this ruling. It needs its own word from you.**
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
<!-- ck:52 status:closed owner:no -->

Body archived in [archive/PLAYTEST_ARCHIVE.md](archive/PLAYTEST_ARCHIVE.md) under the heading "## ck10 -- archived 2026-09-16 (was checklist status:closed):" followed by this heading.

### ✅ 2026-08-19 — two calls from the last sweep link. **50 RULED + APPLIED 09-12 (soften the chain-vs-copy promise) · 51 CLOSED 09-12 as overtaken, with the unrun leg re-filed as a takeable. Nothing is owed from you.**
<!-- ck:50 status:ruled owner:no -->

Body archived in [archive/PLAYTEST_ARCHIVE.md](archive/PLAYTEST_ARCHIVE.md) under the heading "## ck50 -- archived 2026-09-16 (was checklist status:ruled):" followed by this heading.

### ⚠️ 2026-08-19 — the SAME defect class, in the third mod. Not today's problem; do not let it be forgotten.
<!-- ck:- status:closed owner:no -->

Body archived in [archive/PLAYTEST_ARCHIVE.md](archive/PLAYTEST_ARCHIVE.md); search `ck-` and this heading.

### ⚠️ 2026-08-19 — the launch test's own first question could not fail. Already fixed; nothing owed unless you disagree.
<!-- ck:- status:closed owner:no -->

Body archived in [archive/PLAYTEST_ARCHIVE.md](archive/PLAYTEST_ARCHIVE.md); search `ck-` and this heading.

### ⛔⛔ 2026-08-19 — the upload would have shipped one fix missing, on Steam. **47 RULED + APPLIED 09-12, both halves — and a third defect was found in the same snippet. Nothing is owed from you.**
<!-- ck:47 status:ruled owner:no -->

Body archived in [archive/PLAYTEST_ARCHIVE.md](archive/PLAYTEST_ARCHIVE.md) under the heading "## ck47 -- archived 2026-09-16 (was checklist status:ruled):" followed by this heading.

### ⚠️ 2026-08-19 — run B now has an ATTENDED moment in it. Nothing to decide; something to know.
<!-- ck:- status:closed owner:no -->

Body archived in [archive/PLAYTEST_ARCHIVE.md](archive/PLAYTEST_ARCHIVE.md); search `ck-` and this heading.

### ⛔⛔ 2026-08-17 — THE UPLOAD IS PAUSED ON YOUR OWN WORD. Two defects found at the sitting and fixed; two questions for you.
<!-- ck:- status:closed owner:no -->

Body archived in [archive/PLAYTEST_ARCHIVE.md](archive/PLAYTEST_ARCHIVE.md); search `ck-` and this heading.

### ✅ 2026-08-19 — THE VERIFICATION LAUNCH RAN: the mod is running clean in a real game. **43 CLOSED 09-12 as overtaken — the opt-in pack is enabled again. Nothing is owed from you.**
<!-- ck:43 status:closed owner:no -->

Body archived in [archive/PLAYTEST_ARCHIVE.md](archive/PLAYTEST_ARCHIVE.md) under the heading "## ck43 -- archived 2026-09-16 (was checklist status:closed):" followed by this heading.

### ✅✅ 2026-08-18 — STATE.md WAS EVICTED ON YOUR DIRECTION, AND YOU RULED THE CAPS THE SAME DAY. Nothing here is owed from you.
<!-- ck:- status:ruled owner:no -->

Body archived in [archive/PLAYTEST_ARCHIVE.md](archive/PLAYTEST_ARCHIVE.md); search `ck-` and this heading.

### ✅ 2026-08-18 — SWEEP CHAIN, LINK 4 REPORTED. **41 RULED + BUILT 09-12: the stand-down box names the fixes and stops blaming the game. Nothing is owed from you.**
<!-- ck:41 status:ruled owner:no -->

Body archived in [archive/PLAYTEST_ARCHIVE.md](archive/PLAYTEST_ARCHIVE.md) under the heading "## ck41 -- archived 2026-09-16 (was checklist status:ruled):" followed by this heading.

### ✅ 2026-08-18 — SWEEP CHAIN, LINK 3 REPORTED. **40 RULED 09-12: `smr_shuttles` keeps its name, accepted as recorded. Nothing is owed from you.**
<!-- ck:40 status:ruled owner:no -->

Body archived in [archive/PLAYTEST_ARCHIVE.md](archive/PLAYTEST_ARCHIVE.md) under the heading "## ck40 -- archived 2026-09-16 (was checklist status:ruled):" followed by this heading.

### ✅ 2026-08-18 — SWEEP CHAIN, LINK 2 REPORTED. **39 RULED + BUILT 09-12: the stand-down box shows once per session. Nothing is owed from you.**
<!-- ck:39 status:ruled owner:no -->

Body archived in [archive/PLAYTEST_ARCHIVE.md](archive/PLAYTEST_ARCHIVE.md) under the heading "## ck39 -- archived 2026-09-16 (was checklist status:ruled):" followed by this heading.

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
<!-- ck:- status:closed owner:no -->

Body archived in [archive/PLAYTEST_ARCHIVE.md](archive/PLAYTEST_ARCHIVE.md) under the heading "## ck54 -- archived 2026-09-16 (was checklist status:closed):" followed by this heading.

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
<!-- ck:- status:ruled owner:no -->

Body archived in [archive/PLAYTEST_ARCHIVE.md](archive/PLAYTEST_ARCHIVE.md) under the heading "## ck- -- archived 2026-09-16 (was checklist status:ruled):" followed by this heading.

### ⭐ NEW 2026-08-13 — public documentation: platform decided, one question back to you
<!-- ck:- status:closed owner:no -->

Body archived in [archive/PLAYTEST_ARCHIVE.md](archive/PLAYTEST_ARCHIVE.md); search `ck-` and this heading.

### ✅✅ 2026-08-13 — public documentation, part 2: ALL FOUR DECIDED, same day
<!-- ck:- status:ruled owner:no -->

Body archived in [archive/PLAYTEST_ARCHIVE.md](archive/PLAYTEST_ARCHIVE.md) under the heading "## ck- -- archived 2026-09-16 (was checklist status:ruled):" followed by this heading.

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
<!-- ck:- status:ruled owner:no -->

Body archived in [archive/PLAYTEST_ARCHIVE.md](archive/PLAYTEST_ARCHIVE.md) under the heading "## ck- -- archived 2026-09-16 (was checklist status:ruled):" followed by this heading.

### ⭐ NEW 2026-08-05 — from the `corun-batch-1` sitting (four calls, all yours)
<!-- ck:- status:ruled owner:no -->

Body archived in [archive/PLAYTEST_ARCHIVE.md](archive/PLAYTEST_ARCHIVE.md) under the heading "## ck- -- archived 2026-09-16 (was checklist status:ruled):" followed by this heading.

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
