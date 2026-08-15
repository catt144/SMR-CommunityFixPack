# Chain prompt 3 — the terminal audit: re-derive both builds, make every count true everywhere, empty the folder

**Read `README.md` first — binding chain rules apply.** Staleness check, live
todo list. This is the **last** prompt: folder emptiness is your done-condition.

## Job 1 — backward QA, firewalled where it counts

* Re-derive both builds against their entries AND against Src — the route, not
  the citations (`recorded-facts-are-claims`; this project has been wrong in
  both directions in one week with every cited line right).
* ⛔ Run **"which shipped module delivers this?"** over every player-facing
  sentence this chain produced (module headers exempt; fix-list entries, card
  edits, metadata wording NOT exempt) — **before reading the builders' own
  reasoning about those sentences.** The last three chains' controls each
  caught a miss the builder had passed; the streak is the argument.
* Re-verify the C39 coverage list independently (your own label sweep), and
  that the F85 wrapper touches nothing but the distress route (negative
  control: another popup's `dont_pause` unchanged).
* The evidence bar (README rule 4): confirm both entries claim exactly what
  their logs hold and nothing more — the screen-claim boundary from 02's Job 3
  especially.

## Job 2 — the release-surface count sweep (the README's named list, executed)

Every count that moved, made true at its surface, with `--emit-counts` as the
only source: STATE's build-state block · the fix-pack card's suite sentence ·
the judgment-call sentence (card + `metadata.lua` `description` + site FAQ +
fix-list markers — settle whether the F85 flip makes it six, ONE way,
reasoning recorded) · two new fix-list entries in player language (rule 4: no
paths, no ids, no house words) · the fix-list's own count sentences · packaged
file count (re-simulate `ignore_files` over the real tree, the release-3 audit
method) · `RELEASE_PORTAL_PREP.md` §2 body sizes / §3 strings if touched / §4
packaging table · **both card edits land in the STORE file AND the RELEASE
copy, and the verbatim diff is re-proven** (only marker/HOLE lines may differ).
Site changes: `mkdocs build --strict` GREEN, ledger note in
`SITE_BUILD_AUDIT.md` style. ⛔ No claim past the frozen bar by word choice; no
count from prose.

## Job 3 — route and close

* Anything unresolved is ROUTED to `PLAYTEST_CHECKLIST.md` "Decisions waiting
  on you", never absorbed. Expected routings if their conditions fire: an F85
  screen-witness ask (minutes-scale, bundled with any next sitting); any C39
  mismatch outside the ruled shape.
* Checklist item 5's queue note → built/verified state; the ④ block gets one
  line: the chain is closed, ④ is unblocked again (the owner ordered this
  chain ahead of ④ on 2026-08-14).
* STATE: the ∥ `unattended-3` marker resolves; NEXT returns to ④ (owner);
  keep STATE at its checked line count. SESSION_LOG entry, newest-first.
* `python tools/doccheck.py` GREEN · closing commit **deletes this file AND
  `README.md`** — the folder is empty when you are done · push.

## Notes from upstream (prompt 02, 2026-08-15 — the verification)

**Commits:** fix pack `92fe101` (build) → `6f07e5c` (handoff) → **this prompt's
closing commit** (both entries `fixed`, INDEX, EF-051, STATE, the two logs).
⚠️ **The TestKit repo has NO git remote** (`git remote -v` empty, branch
`master` has no upstream); its build commit `5113cca` is local-only — that is
not a push failure, but do not call it a push. **The kit is DISARMED and its
tree is clean**: both temporary files deleted, `metadata.lua` restored via
`git checkout` (the arm script had also stripped the kit's own *commented*
`96_AutoRunFlag` template line, which the restore puts back).

**Staleness at my moment:** fix pack `6f07e5c` clean + `git pull` "Already up to
date"; TestKit `5113cca` clean. Src re-read at **1.0.7.396349**.

### ⭐ COUNTS AT MY MOMENT — emitted, never typed (`--emit-counts`, doccheck GREEN)

```
- modules: 76 registered (76 default-active, 0 optional-gated files)
- Code/*.lua files: 77
- TestKit probes: 96
- BUGS index rows: 103 F + 12 D + 46 C
```
⛔ **Re-emit these yourself.** Nothing I did moved them — prompt 01's build did,
and STATE's block already carried the moved values. **Your Job 2 still owns
every OTHER surface** (cards, `metadata.lua` description, site, sheet).

### The two launches, and what each is evidence for

| | launch 1 — the suite | launch 2 — the bracket |
|---|---|---|
| log (archived, byte-verified) | `archive/u3suite_Mars.exe-20260815-01.32.33.log` | `archive/u3c39_Mars.exe-20260815-01.36.41.log` |
| shape | autorun, fresh colony | staged `CP15PT15` copy, self-driving payload |
| gate | `fix pack present: 76/76` · `opt-in pack present: 8/8` · rescue absent by design | same, read 3× (menu / after load / close) |
| result | **`80 PASS, 0 FAIL, 16 SKIP, 0 ERROR`** of 96 | the C39 paused bracket + the F85 flip reading |
| `[LUA ERROR]` | **60**, see below | **0** |

⭐ **The suite counts were read by counting the log's own verdict lines**
(deduped — every mod line is written twice, `[mod]`-prefixed and plain), and
they agree with the suite's own summary line. **Baseline was `78/0/16/0` of 94
(`archive/rs_r0_*`); the delta is EXACTLY the two new probes** — and the
**SKIP set is byte-identical to the baseline's**, diffed by name, not by count:
`AnomalyCaveInMap · BrokenTrackSalvage · CaveInsNoDisasters · GhostFarmOxygen ·
LakeEntombment · LowStorageWarning · MilestoneCrash · SaveRescueCleanPass ·
SaveRescueHealBounds · SaveRescueIdempotent · SaveRescueResidueTable ·
SaveRescueSelfClean · SaveRescueStandDown · TechDescriptionBuilding ·
TrackSalvageWipe · TrainsToVoid`.

### ⚠️ THE 60 ERROR LINES IN LAUNCH 1 — reported, with what is and is not proven

Two distinct texts only: `Lua/Flight.lua:465 objects_to_mark` ×59 and
`Lua/Flight.lua:479 objects_to_unmark` ×1. **All 60 fall BEFORE the suite began**
(last at line 957, `[SMRAUTO] BEGIN` at 981) — they are map-generation, not
probe execution. Already a known line class (`F49`, `F87`, `PLAYTEST_HELP`
"vanilla synthetic-map noise"), and the only archived log that carries them is
the 2026-08-03 **MarsDebug new-colony** run. Source reading:
`Flight.objects_to_mark` has the class default `false` (`Flight.lua:42`) and is
replaced by a real table later (`:181`), so a `Flight:Mark` before that init
indexes `false` — a vanilla start-up race. Neither pack touches `Flight`.
⛔ **What is NOT proven: that they are not ours.** That is an attribution
verdict from source, not a control — no no-mod run of this shape exists, and
**this is the first archived RETAIL new-colony autorun**, so there is no
same-shape precedent to diff against. The baseline `rs_r0_*` has zero of them
because it is a save-LOAD leg, not a new colony. If you want it closed, the
control is one Mod-Manager-disabled autorun, which costs an owner click.

### C39 — the headline, and the negative result that carries it

All four reads at `GameTime()=61108784`, `speed=0x`, day 86 hour 2 —
**including the revert**, which closes the 08-11 bracket's one recorded gap.

| | subject `TVStudioWorkshopCCP1#1526` | control `Diner#1475` |
|---|---|---|
| before | 12 posts, 10/10/10, perf **102**, our delta **0** | 2 posts, 2/2/2, perf **130**, our delta **0** |
| law on | 6 posts, 6/6/6, perf **253**, our delta **+127** | 1 post, 1/1/1, perf **228**, our delta **0** |
| reverted | 12 posts, 6/6/6, perf 64, our delta **0** | 2 posts, 2/2/2, perf 115, our delta **0** |

* **126 → 253 = 2.008×.** 126 is the log's own `vanilla-would-have-said` (live
  answer minus our delta). Unfixed on 08-11 the same subject went 127 → 131.
* ⭐ **The control never moved on our account** — delta 0 at all four reads.
  Double-paying a building the shipped gate already pays was the failure mode
  this design was chosen over, and it did not happen on a live object.
* **Delta 127, not the probe's 100** — predicted in writing before the run; the
  constant assumes six *identical* workers and this shift averages ~127.
* **⛔ 1 of 8 families sampled.** `ServiceBuildings` = 6 members (5 gated, 1 not);
  **`FactoryBuildings` = 0 and `ResearchBuildings` = 0 in this colony**, so the
  two Factory-label families could not be sampled at all. The other seven stay
  SOURCE. ✅ One *excluded-by-construction* member WAS sampled and reads as
  predicted: `OpenAirGym#1476` → `IsKindOf("Workplace") = false`, all three
  worker fields `nil`.

### F85 — sampled twice, and the boundary held

Flag **true → false**; already-pausing popup **false → false**; **no-flag popup
stays `nil`** (the field is not created); second pass idempotent. Live class
state: `dont_pause` class default `false` (boolean), `XPauseLayer` present.
Install witness `status = active`, `detail = ''`, read 3×. The second sample ran
**after a 47 MB campaign save had loaded**, i.e. on a fully flattened tree.
⛔⛔ **NO SCREEN CLAIM WAS MADE OR IMPLIED**, and the live call site was
deliberately not called — the payload's header records that the alternative was
weighed and rejected, not overlooked. **The §3.6 rider is RETIRED** on its
stated condition, with the entry stating exactly what retiring does not assert.

### ⚠️ TWO FINDINGS YOU INHERIT — both already written into the record

1. **A harness defect in this leg's own instrument.** The payload's per-family
   tally used `rawget(b, "class")`, which is `nil` for a class field on the
   metatable ⇒ **all eight `C39SCAN family … :: 0 present` lines are wrong**,
   including the subject's own family, three lines above a full reading of it.
   Disclosed on `C39.md`; ⛔ **do not quote those lines.** It changed no verdict
   only because a second independent reading of the same fact was in the log —
   which is the argument for the redundancy, not for the defect.
2. **`EF-051`'s 08-14 close-out listing was incomplete.** The extensionless
   **`U2RT1`** (54,311,838 bytes) is present and always was: the sweep globbed
   `*.sav` and `EF-050` lets this project write savegames with no extension. Its
   `CreationTime` is **2026-08-12 12:29:59** (the 08-12 restore window), and
   **nothing at all was created in the save directory during either launch
   tonight** — so the falsifier did NOT fire and the retirement stands. Fact
   amended + `updated` bumped. **Left in place deliberately**: it is
   unattended-2's artifact, and deleting 54 MB of someone else's close-out is a
   daylight call. Route it or leave it, but do not re-list "zero strays" from
   a `.sav` glob.

### EF-056 discipline, both launches

All four autosaves byte-copied with MD5 **before** launch 1 and reconciled
**by name and by hash after each** — `Autosave Sol 311`, `311(2)`, `311(3)`,
`316`, all four present and **identical** at both close-outs; no new autosave
was written (launch 1 never reached a sol change, launch 2 was paused
throughout). Save dir **76 `.sav` → 77 (the staged copy) → 76** after the copy
was deleted with the game closed. The staged `U3C39BR` was byte-identical to
`CP15PT15` **after** the run as well as before — that leg never calls `SaveGame`.

### What is NOT sampled, so your QA does not have to rediscover it

* No organic enactment — `LawDefs.…:Activate()` was called directly (the vote
  flow skipped; the effect path is identical and the log labels it **FORCED**).
* No keyboard witness of anything, no screen event, `tested` NOT granted for
  either entry.
* No save/reload of a colony carrying either repair, and no uninstall pass.
* Seven of eight C39 families, and both Factory-label families entirely.
* The `AssemblyChoicePopup` and breakthrough-choice halves of F85 — closed by
  the pause, not repaired at their own sites.

### Open, for you

* ✅ **Checklist item 30 is CLOSED — ruled 2026-08-15, the day it was raised:
  C39 SHIPS AS BUILT, all eight families, no list.** Owner's principle: *"true
  to the code… a true to code bugfix as much as possible"*, which selects the
  shipped build because the module carries **no building list** and restricting
  it would have meant ADDING one. **Your Job 2 therefore writes card and
  fix-list text against the real eight-family footprint** — ⛔ do not describe
  the fix as "the four Workshops" anywhere.
  ⛔ **The ruling settles SCOPE ONLY.** It is NOT permission to describe the
  change quietly: the card and site must still say this moves gameplay-visible
  numbers (security, drone throughput, research), and it does NOT upgrade the
  seven SOURCE families to measured. ⭐ Carry the mitigating fact into the text
  if it helps a player: all three Automation laws share the `Automation` policy
  slot, so at most one is active at a time — four Workshops + two Security
  buildings, **or** the Drone Assembler + Bottomless Pit, never all eight.
* ⚖️ **Checklist item 5 (F85 severity/tier) is still OPEN**; its queue note now
  needs updating to *verified*, which your Job 3 owns.
* **An F85 screen-witness ask is OPTIONAL, not owed** — `fixed` was granted
  without it and the bar does not require it. If you route it, route it as a
  minutes-scale add-on, and say plainly that it upgrades nothing about `fixed`.
* The 60 `Flight.lua` lines above, if you want that control closed.
* **The parked harness is in git, not on disk** — `97_U3Common.lua.txt`,
  `98_U3Bracket.lua.txt` and `U3_ARM.ps1.txt` were committed **with** the run and
  deleted in the **next** commit (probe hygiene rule 5), so they exist in exactly
  one tree. `git show <run commit>:docs/agent/prompts/unattended-3/98_U3Bracket.lua.txt`
  is what was actually executed, character for character.
