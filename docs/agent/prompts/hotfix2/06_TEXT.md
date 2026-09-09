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

## 2 · ck113 — `last_changes` bullet 3 overstates F116

*"One track-salvage fix was also brought in line with the new game code"* reads
as parity. Two deliberate divergences from 1.1.0 remain (ck111 is one) and the
repair has never run in a game. **Proposed:** *"One track-salvage fix was also
updated for the new game code."*

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

- ck112 or ck113 unruled ⇒ do everything else, leave those two strings alone,
  say so. They are the owner's sentences.
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
