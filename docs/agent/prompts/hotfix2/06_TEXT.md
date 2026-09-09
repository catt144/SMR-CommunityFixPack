# 06 · Text — every player-facing surface, brought true

Chain: `prompts/hotfix2/README.md` (its binding rules are yours). Runs LAST
before the terminal audit — it consumes the drafted patch-note lines from 02, 03
and 04, so it cannot start until those are done or explicitly skipped.

⚖️ **The rule that governs this whole prompt** (owner, 2026-09-08): *a patch note
that says "Fixed" is a **CLAIM**, false until we confirm it ourselves.* That binds
our own notes, not just Haemimont's changelog.

## 0 · Start

`git log --oneline -10` · `git pull` · `ListAgents`. Todo list first.

**Read path:** `docs/UPLOAD_WORKFLOW.md` §3 (the paste backups — **the real
delivery path**, not polish) · `agent/reports/STORE_CARD_LIVE.md` ·
`metadata.lua` (`description`, `short_description`, `last_changes` — read the
comment blocks above each; they carry rulings) · `docs/PLAYTEST_CHECKLIST.md`
items 112, 113, 118 · `agent/FIX_POLICY.md` §8 · your inbox from 02/03/04/05.

## 1 · ck112 — the store description promises something the pack cannot do

HOW IT WORKS, bullet 3, currently: *"Every fix checks the game's code before it
touches anything, and stands down by itself if an official patch changes what it
was written for."*

The self-checks see whether a thing still EXISTS. They cannot see a same-name
change of body or signature — and 1.1.0 proved it twice (trains, landscaping;
neither fix stood down). Every upload re-posts the description as the page body,
so leaving it would post that sentence beside a changelog admitting two fixes
broke.

**Proposed (owner leaning yes, their sentence to rule on):** *"…and stands down
by itself if the code it was written for has been renamed or removed. That check
cannot see every kind of change, which is why each game update gets a
compatibility pass. A fix that stands down does nothing at all — it never
guesses."*

⭐ **This patch makes it MORE true, and you may say so honestly**: `bodycheck.py`
plus the `SRC:`/`DEFECT:` manifest is exactly the "compatibility pass" the new
wording promises. ⛔ But do not upgrade the claim back — the manifest is a
**repo-side** instrument the player's game never runs, and class c (semantics
moving under a wrapper) is still seen by nothing.

## 2 · ck113 — RULED: `last_changes` bullet 3 says "updated for"

✅ **The owner ruled this 2026-09-08: take the proposed wording.**
*"One track-salvage fix was also brought in line with the new game code"* read as
parity, which it was not. Write: *"One track-salvage fix was also **updated for**
the new game code."*

⚠️ This bullet describes the **hotfix-1** change and this prompt rewrites
`last_changes` wholesale for hotfix 2 (§3) — so unless the F116 line survives into
the new note, the ruling is satisfied by not reintroducing the old phrasing.
Check which applies before you edit; do not paste a hotfix-1 bullet into a
hotfix-2 changelog.

## 3 · `last_changes` for hotfix 2 — rewrite it, do not append

⛔ **It is the per-version CHANGELOG entry on BOTH storefronts** (`ChangeLog`,
`ParadoxMods.lua:151`; `change_note`, `SteamWorkshop.lua:114`), sent
automatically at upload and archived there forever. Three consequences:

1. **Rewrite before every upload** or the next one posts a duplicate entry.
2. **Keep it terse** — the field is `lines = 3` (`Mod.lua:254`); house style on
   both stores is a dashed line or two.
3. **It is historical** — it describes the version it ships with, forever. Never
   write it in the present tense of the pack as a whole.

**What this version actually is, and the honest way to say it.** Roughly 36 of 80
fixes were REMOVED because the game's own 1.1.0 update fixed those bugs itself;
a handful were repaired because they were doing the wrong thing on the new
version. ⛔ No fix ids, no counts that will drift, no load-order advice, no other
mod named (`EF-054`, `FIX_POLICY` §8).

⚠️ **A removal is not nothing to a player** — it is fixes disappearing from a
mod they installed. Say why in their words: the game fixed these itself, and a
fix that duplicates the game's own is a risk with no benefit.

## 4 · The surfaces that go stale when 02 lands

Route from 02's outbox and fix each:

- **`ExtractorStaffedPerformance` (F108)** and **`LandscapeCostRefresh` (F107)**
  are named on live store surfaces and the site. Their removal makes those
  claims stale.
- **`TrainMinors`** removal leaves two displays stale (QA §0.8).
- The description's **"Eighty-two repairs"** and its SOME OF WHAT IT FIXES list
  both shrink. ⛔ **Recount from the deployed fix list**, never from a comment in
  `metadata.lua` and never from memory — that count has drifted every time
  anyone typed it from the wrong source.
- The site's `content/fix-list.md` and `faq.md` judgment-call count.

## 5 · The 1.0.7 line (ck118)

Both store cards gain a line pointing at the site's **Playing on 1.0.7** page
(`https://catt144.github.io/SMR-CommunityMods/legacy-1-0-7/`), which carries the
frozen v5 download for players who stayed on the old branch. The page and the
GitHub release already exist. ⛔ Portal-neutral wording — the same string is
posted to both stores.

## 6 · `UPLOAD_WORKFLOW` §3 paste backups

⛔ **These are the real delivery path, not optional polish.** Auto-fill has never
produced a clean page in two cycles. Sync the §3 paste backups and
`STORE_CARD_LIVE.md` with `metadata.lua` **in the same commit** as any text
change. Only styling (headings, bold, BBCode) is optional.

## 7 · Scope fence

**In:** `metadata.lua`'s `description` / `short_description` / `last_changes`,
`UPLOAD_WORKFLOW` §3, `STORE_CARD_LIVE.md`, the site's `fix-list.md` / `faq.md` /
`index.md`. **Out:** ⛔ `version`, `version_major`, `version_minor`, `lua_revision`
— `H-02`, the sitting's, never an agent's, never by hand. ⛔ No Mod Editor. ⛔ No
upload, no portal API call (`H-03`). ⛔ No running `publish-site.yml`.
Found something out of fence? **File it, do not fix it.**

## 8 · Stop conditions

- **ck112 unruled** ⇒ do everything else and leave that one string alone, say so.
  It is the owner's sentence. ✅ ck113 IS ruled (2026-09-08) — §2 is settled, not
  pending.
- A count you need is only available from a source you were told not to trust
  ⇒ stop and ask rather than typing a number from memory.
- The description exceeds a portal limit on upload ⇒ that is the sitting's
  finding, not yours; note the length is UNVERIFIED against the upload API.

## 9 · What may NOT be claimed

- ⛔ **Not "Fixed"** for anything no one has watched work. Every in-play control
  from 03 and 04 is still owed at the time you write.
- ⛔ Not a fix count you did not recount from the deployed fix list.
- ⛔ Not "the pack is 1.1.0 compatible" outright — 17 of 22 full-body
  replacements have never been diffed against 1.1.0 by anyone.
- ⛔ Nothing about another mod, and no load-order advice.

## 10 · Close-out

Green gates, and `doccheck --emit-counts` re-emitted if any count moved. Outbox
to `99` naming every string you changed and every claim you deliberately did NOT
make. Strike your README row, `git rm` this file, commit together, push.

⛔ Do not upload. The sitting is the owner's, and it is where `version` moves.

## Notes from upstream

*(From the authoring session, `smr-bugfixpack-91`, 2026-09-08.)*

- ⚠️ `metadata.lua`'s comment claiming "`PackVersion` renders
  version_major.version_minor.version" describes something with **zero hits in
  the 1.1.0 tree**. Comments in that file are claims; several are superseded and
  say so about each other. Verify before quoting one.
- ck118 is ruled and its artifacts are live: GitHub release `v5-game-1.0.7`
  (asset verified byte-identical to Steam's v5 delivery) and the site page. Only
  the store-card line is left, and it is yours.

### From link 02 — the REMOVE block (36 deleted, 1 half-edited, 1 kept)

*(Link 02, `smr-bugfixpack-11`, 2026-09-08. Commits `2dc1dbe` the 36 deletions ·
`f707903` R-7 + the F03 pass · `9b0b82c` 43 bug entries · site `7cef4f3`.
⛔ Nothing was run in a game; no status moved.)*

**The three rulings that unblocked this link, because they bind you too.**

* ⚖️ **ck98 = DELETE, not gate.** Owner, verbatim: *"I am fine with the 1.0.7
  issue, we are giving a path which we don't have to do. The main mod serves the
  current patch period."* There is no 1.0.7 line in the live pack.
  ⛔ **This does NOT relax ck118's constraint on the re-copies.** Our
  `lua_revision` and 1.1.0's minimums are all 350453 (`EF-077`), so hotfix 2
  installs on a 1.0.7 rig with no warning of any kind. Delete-not-gate is a
  ruling about the REMOVE set only; a re-copied 1.1.0 body applied on a 1.0.7
  function is still the F114 failure mode in reverse.
* ⚖️ **ck117 = KEEP `90_SaveSanitizer`** (F35 + F48). It is NOT in the deletion
  set and its `items.lua` entry stays. Only the dead F03 pass was removed.
* ⚖️ **ck120 = the owner's general principle, and it is worth applying to your
  own calls:** *"we fix anything negatives, a small positive I am not as
  concerned about."* That is what killed the F-5 save cleanup — the stranded
  Astrogeologist +10% is an unearned bonus, so it is not chased. A **loss** is a
  different matter and gets fixed.

**What is now true of the tree.** `Code/*.lua` 81 → **45**; `items.lua` 81 → 45;
`metadata.lua`'s `code` list 81 → 45 (all three, per `H-10`); modules 80 → **44**
registered. `bodycheck.py` NO-MANIFEST **46 → 10**, which is link 01's predicted
landing point and is your free cross-check that the right set left.

**⛔ THREE PATCH-NOTE ITEMS THAT ARE CONSEQUENCES, NOT LINE ITEMS — they must not
be dropped quietly, and two of them contradict text that is live right now.**

1. **`ExtractorStaffedPerformance` (F108) and `LandscapeCostRefresh` (F107/F105)
   are NAMED ON LIVE STORE SURFACES AND ON THE SITE.** Both modules are deleted,
   so those claims are now false. This is the highest-priority text item I hand
   you.
2. **`TrainMinors` (F49) removal leaves two displays stale** — the x/max train
   number stops refreshing after a salvage. Cosmetic, but it is a real change a
   player can see, so it is a patch-note line rather than a silent drop.
3. **`LowStorageWarning` (F12) — ⛔ READ THE CORRECTION BEFORE YOU WRITE A WORD
   ABOUT THIS ONE.** An earlier version of this outbox told you to write that a
   1.1.0 player gets **no low-Food warning at all**. **That is FALSE. Do not
   print it anywhere.** The owner challenged it (the DLC's focus is food, so
   silent deletion made no sense) and the re-derivation reversed it: 1.1.0
   **replaced** both warnings rather than deleting them — Food is now
   `StarvingColonists` ("Missed Meals", voiced *"Warning! Food shortage"*), new
   in this branch, and maintenance is now `MaintenanceStuckBuildings`
   ("Maintenance Problem"). Full evidence on the `F12` entry and checklist 121,
   which is WITHDRAWN.
   ⇒ **What to actually say, if anything:** nothing more than that the fix is
   retired because the game now handles it. ⛔ Do NOT claim a player-facing loss
   here, and do not offer a restored warning as a future feature — there is no
   gap. The only real difference is that the old warning was a days-of-supply
   *projection* and the new ones fire on *state*, which is not worth a
   patch-note line and is certainly not worth a store line.

**Four removals are a small IMPROVEMENT, not a neutral drop**, because our module
had become marginally worse than vanilla. Worth one honest sentence rather than
burying them in a list: `SmallLandscapeSites` (narrowed drones to 5 destinations
against vanilla's default of 10), `TouristApplicants` (rolled 0..100 against
vanilla's 0..99), `SpaceYDroneCapBullet` (printed a duplicate bullet),
`DustStormUndergroundBreaks` (over-filtered).

**`FirstAsteroidPrefabs` needs a note, not an apology:** prefabs already granted
on a 1.1.0 save cannot be taken back, and the `SMRFixPack_FirstAsteroidPrefabs`
GameVar is absent-tolerant, so nothing breaks.

**`AstrogeologistExtractors` needs one careful sentence.** The stranded +10% on
two extractor types stays in an existing save **permanently** — not "until the
next load". A new game is clean. Do not write it as self-clearing.

**⚠️ SITE TEXT I REMOVED, AND SITE TEXT I DELIBERATELY DID NOT.** I removed 36
`content/fix-list.md` entries (82 → **46**, commit `7cef4f3` in
`SMR-CommunityMods`). My fence was that file only, so these are yours and every
one of them is now factually wrong:
* `content/index.md:35` — "**six fixes are judgment calls**" is now **three**
  (Biorobots · colonists sheltering in vacuum · Edit Payload). The same sentence's
  "one of those changes how the game feels — dust devil waves" describes a fix
  that is GONE; the whole clause should go.
* `content/faq.md:24-32` — the "More dust devils" bullet and the "Five other
  judgment calls" bullet both name removed fixes.
* `content/faq.md:33-38` — the "Some buildings produce more under an Automation
  policy" bullet describes C39, removed.
* `content/faq.md:152-163` — "Six fixes are judgment calls", plus the dust-devil
  and Automation notes.
* `content/faq.md:165-171` — "Which fixes are judgment calls?" names six; three
  are gone.
⚠️ Committing in that repo does NOT publish — `publish-site.yml` is
`workflow_dispatch` only.

⚖️ **The owner's rule that should shape your wording** (ck120): *"we fix anything
negatives, a small positive I am not as concerned about."*
### From link 03 — one live public claim is now FALSE, and four drafted patch-note lines

*(Link 03, `smr-bugfixpack-91`, 2026-09-08. Commits `3db4984` F-1 SaintBlessing ·
`f38d6d2` F-2 StaleReservations · `19b5aaa` F-3 ShelterReflex. ⛔ Nothing was run
in a game; no status moved.)*

**1 · ⛔ THE SITE FIX LIST NOW PROMISES SOMETHING THE PACK NO LONGER DOES.** This is
the F108 / F107 shape link 02 already routed to you, on a fourth entry. The F73
card (`SMR-CommunityMods/content/fix-list.md:172-187`, rendered at
`site/fix-list/index.html:988-1000`) reads:

* *"What you saw: … and a brief power or air interruption turning every resident of
  a habitat out of their home for as long as it lasted."*
* *"What was wrong: **two things.** A habitat counts as unsuitable housing the
  instant its life support dips, so its residents are un-homed; and the game has no
  reflex for a colonist with nowhere to be…"*
* *"After the fix: **a habitat with a momentary life-support gap keeps its
  residents**, and a colonist idling in vacuum heads home before their oxygen runs
  out."*

**Only the second half survives.** Half (a) was deleted in `19b5aaa`: on 1.1.0 it
had become an outright throw on any asteroid habitat with a trait filter, and
1.1.0 made "no life support" a deliberate scoring **tier** with the intent written
into the shipped help text — so repairing it would mean fighting a stated design
(`FIX_POLICY` §4). ⇒ the card needs to become **one thing, not two**, and the
"keeps its residents" promise has to go. The entry keeps its *judgment call* flag
for the surviving half, which is still a behaviour the game does not have.

**2 · Drafted patch-note lines.** Yours to word finally; these are the honest
versions and ⛔ **none of them may say "Fixed" yet** — all three repairs are
source-derived and none has been seen in play (owner rule, 2026-09-08). The three
owner controls are batched on the checklist and unrun.

* *A Saint's blessing works again with the pack installed. The game's own 1.1.0 fix
  and ours were cancelling each other out; saves played in between are repaired on
  load.*
* *Colonists returning from a long expedition keep the home that was held for them.*
* *Setting a trait filter on an asteroid habitat no longer causes an error.*
* *Removed: the pack no longer holds an asteroid habitat's residents through a power
  or air cut — the game now handles that case deliberately, and colonists are
  re-homed by themselves once life support is back.*

⚠️ The fourth is a **removal**, not a repair, and it is the one a player could
notice as a loss. It reads better next to the third (same module, same sitting)
than buried in a removals list.

⚖️ Note for the Saint line specifically: the honest framing is **"our fix and the
game's fix were cancelling each other out"**, not "we fixed a bug". 1.1.0 fixed F92
itself; what hotfix 2 does is stop our data patch from breaking their fix, and heal
the saves that were played in between.

### From link 04 — the re-copies (F-6, F-7) and the F116 edit (§7)

*(Link 04, `smr-bugfixpack-ba`, 2026-09-08. Commits `3f8394b` F-7 RocketDroneChurn ·
`177c7b2` F-6 PayloadTemplateRefill · `fc318c7` F116 ck111+ck119. ⛔ Nothing was run
in a game; no status moved. `Code/*.lua` is still 45 files / 44 modules — nothing
added or removed, so `items.lua` and `metadata.lua` were not opened.)*

**Drafted patch-note lines — CLAIMS until the post-99 sitting confirms them (owner
rule 09-08). Word them as "updated for 1.1.0", never "fixed", and never mention the
branch mechanics (probes, gates) on a player surface.**

* *Updated for 1.1.0: the landed-rocket drone fix now respects the game's new
  "Accept fuel" toggle. A rocket you have told not to refuel no longer keeps asking
  for Fuel.*
* *Updated for 1.1.0: the Edit Payload fix now works with the new tutorial and with
  destination picks. Emptying a row still sticks; cancelling the launch prompt no
  longer counts as confirming it; the tutorial's second rocket is still pre-filled;
  picking a new destination suggests the template again, as the game intends.*
* *Track salvage: a piece left over when a line is split is now kept on its own
  track instead of being removed, matching the base game; a line holding both
  finished and under-construction pieces is now processed correctly after a split.*

⚠️ The first two are "our fix no longer undoes a 1.1.0 improvement", not new
repairs — the honest frame is **compatibility**, and they are evidence FOR the
store card's "compatibility pass" sentence (ck112), not for a new bug fixed. The
third (F116) is a behaviour change to destructive code that has never run in a
game: if it is listed at all, say "matches the base game's behaviour", nothing
stronger, and do not say "fixed a bug that deleted track" — F116 was never
reproduced.

* **On 1.0.7 the two re-copied modules stand down** (F-6 by a behaviour probe, F-7
  by a shape test); the F116 edits behave the same on either branch and carry no
  gate. If 06 writes any 1.0.7 line, it is "1.0.7 players: stay on v5" (ck118),
  never "works on both".
* Public surfaces checked for these three: the site fix-list entries for F50 and
  F70 describe the 1.0.7 behaviour and are still true on 1.1.0 (the defects
  persist); F44/F91's entry is still true. **No public claim became false in this
  link.** The store card's HOW IT WORKS bullet 3 (ck112) is the only surface these
  touch, and only as supporting evidence.

### From link 04b — group C: F-8, F-9, F-10 re-armed on their 1.1.0 bodies (2026-09-09)

*(Link 04b, `smr-bugfixpack-94`, 2026-09-09. Commits `799f145` F-8 `LandscapeUnitFilter`
· `3d4c933` F-10 `TrainCargoDumping` · `7a401f1` F-9 `VacuumWalks`. ⛔ Nothing ran in a
game; no status moved. `Code/` still 45 files / 44 modules — nothing added or removed, so
`items.lua` and `metadata.lua`'s `code` list were not opened.)*

**What changed on the player surface.** Three fixes that were switched OFF on 1.1.0 since
2026-09-08 (F115's gate, F114's gate, and an accidental decline) are back on, each carrying
the game's 1.1.0 function body with our one-line correction. Their store/site fix-list
entries were TRUE on 1.0.7, FALSE between 09-08 and now, and are true again as *what the
code does* — never as something seen in play on 1.1.0.

**Drafted lines** (owner-reviewed wording in the checklist, LINK 04b block; these are the
same, for your `last_changes` and the notes):
* *Landscaping placed over colonists boarding a vehicle no longer pulls them out of it —
  re-enabled for 1.1.0.*
* *Colonists moving between two nearby domes joined by a passage take the passage instead
  of crossing the surface — re-enabled for 1.1.0.*
* *Trains no longer unload a resource at a station where you have switched it off while
  another station on the line accepts it — re-enabled for 1.1.0.*

⛔ **Wording constraints that bind you:**
1. **"Re-enabled", never "Fixed"** (owner rule 09-08: a "Fixed" is a claim, false until
   confirmed). None of the three has run in a game on 1.1.0.
2. ⛔ **F-10 may NOT be worded as a confirmed 1.1.0 defect.** Whether 1.1.0 still has the
   train-dumping bug is UNESTABLISHED (C-side `GetTargetAmount` on a suspended request,
   unread; checklist row 10 is the control). "Re-enabled" is exactly right: it says what
   we did, not what the game does.
3. If you touch the F34/F46/F52 site entries, "re-enabled for 1.1.0" is the only new
   fact; do not add reach claims. ⚠️ For F34 specifically the reach on 1.1.0 is WIDER
   (all landscaping site kinds), so an old "flatten" wording is still true, not stale.

**Nothing for `metadata.lua`'s `code` list** — no module was added, renamed or dropped.
