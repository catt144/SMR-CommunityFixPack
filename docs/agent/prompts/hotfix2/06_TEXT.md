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
