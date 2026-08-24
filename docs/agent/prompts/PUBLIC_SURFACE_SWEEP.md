# Public-surface sweep — every place a shipped fix must appear

**Run this whenever a fix is added, retired, or materially re-scoped.** It is the
post-release counterpart to `reports/RELEASE_PORTAL_PREP.md`: that sheet covers
*uploading*, this one covers *what the words say*. Written 2026-08-24 during the
F105 sweep, from the surfaces that actually existed rather than from memory.

⛔ **A fix is not shipped when the code is written. It is shipped when a player
can find out that it exists.** Every surface below is one a player or a reporter
reads, and a fix missing from any of them is a fix nobody knows about.

## 0 · Before you touch anything

1. `python tools/doccheck.py --emit-counts` — never hand-type a count anywhere.
2. Read the entry in `agent/bugs/<ID>.md`. The **entry is authority**; store and
   site copy are derived from it, never the other way round.
3. Decide the **player-facing symptom sentence** first — the words the player
   would use, not ours. Everything else on this list is downstream of it.
4. ⛔ **First ask whether the fix has a player surface AT ALL.** A repair to the
   pack's own code in a module that **never shipped** gets **NO entry anywhere on
   this list** — no fix-list row, no headliner, no `last_changes` line — because
   no player ever ran the broken version. F107 (2026-08-24) is the worked example:
   it is `fixed`, it is real, it changed shipping code, and it is correctly absent
   from every surface below. Writing it up would invent a bug players never had
   and inflate the count the store card stakes its credibility on. What such a fix
   *does* touch is §3's `code` list and `items.lua` if it added or renamed a
   module. Say so explicitly in the report, so the next reader does not re-open it.

---

## 1 · The site — `C:\Dev\SMR-CommunityMods` (the fix list is the spine)

`content/fix-list.md` is the canonical player-readable list, and **the store
cards' count is derived from it**, so it goes first.

* Add one entry, in the section a player would look in — not the section that
  matches our internal cause. (F105 is a landscaping bug to a player, so it sits
  with the landscaping entries in *Drones & logistics*, not in *Buildings &
  economy* where "construction costs" would put it.)
* House format, exactly:
  ```
  ??? success "<the symptom, in the player's words>"
      **What you saw:** …

      **What was wrong:** …

      **After the fix:** …

      **⚠️ Worth knowing:** …            <- only if there is a real caveat
  ```
* ⛔ **Never say "crash" for a Lua error.** Surviving Mars catches Lua errors; the
  player sees a message box or a log line, not a CTD (`EF-065`). Say *error*.
* Mark **judgment call** only if the entry required deciding what the game
  *meant*. A plain repair is not one, and the card states how many exist.
* Fixes that repair a save already in a bad state say so — that is the sentence
  players search for.

Then re-derive, do not count by hand:
```bash
grep -c '^??? ' content/fix-list.md
awk '/^## /{s=$0;order[++n]=s} /^\?\?\? /{c[s]++} END{for(i=1;i<=n;i++) if(c[order[i]]) printf "%-45s %d\n", order[i], c[order[i]]}' content/fix-list.md
```
The section tally **must** sum to the total. If it does not, an entry is
orphaned above the first `## `.

⚠️ Also check `content/index.md`, `content/faq.md`, `content/install.md`,
`content/for-modders.md` for any claim the new fix falsifies.

⛔ **CORRECTED 2026-08-24 by re-running this sweep — the first draft of this line
said "none of them states a count", and that is FALSE.** None states a *fix*
count, which is the deliberate part; but `content/faq.md` states the
**judgment-call count in three places** and they must move together:

```bash
grep -n 'judgment call' /c/Dev/SMR-CommunityMods/content/faq.md
grep -c '^??? .*judgment call\*"$' /c/Dev/SMR-CommunityMods/content/fix-list.md
```
* `faq.md:151` — *"**Five fixes are judgment calls**"*
* `faq.md:164-168` — the question *"Which fixes are judgment calls?"*, whose
  answer **names all five**; a sixth would have to be named here too
* `faq.md:28` — *"**Four other** judgment calls"*, a count relative to the one
  named above it

⇒ a new **judgment-call** fix falsifies `faq.md` in three places even though it
touches no numeral on any other page. A plain repair falsifies none of them.
Verified consistent 2026-08-24: five marked on the fix list, five on `faq.md`.

---

## 2 · The store cards — `reports/STORE_CARD_LIVE.md`

⛔ **This file has TWO blocks and they drift apart if you edit one.**

| block | line marker | format |
|---|---|---|
| Paradox Mods | `═══ PARADOX MODS — plain text` | plain |
| Steam Workshop | `═══ STEAM WORKSHOP — BBCode` | BBCode |

Both carry the same claims. Edit **both**, then diff them by eye.

**The count is a WORD, not a numeral** — *"Eighty repairs"*, spelled out — and it
is derived from §1's `grep -c`, never from the last value written here (this line
itself said *"Seventy-nine"* one sweep after that stopped being true). Update it
in both blocks. ⭐ The count is only safe
because the reader can check it on the page the card links to; if that link ever
breaks, the count must come out.

Also check, in both blocks:
* the **headliner list** — does this fix belong in it? The bar is *player-facing
  and recognisable*, not *most work*. A fix nobody could notice stays in the
  "… and a good deal more" tail.
* the **judgment-call sentence** — the count of those is stated separately.
* ⛔ **The card must not imply the pack fixes a client crash.** Recorded ruling;
  re-read §"What this pays off" before touching claim wording.

⚠️ These are our *record* of what is pasted. Changing this file does not change
the live pages — **the owner pastes them at a sitting.** Say so in the report;
never write as though the page is updated.

---

## 3 · `metadata.lua` — the strings that ship INSIDE the mod

* **`last_changes`** — ⛔⛔ **CORRECTED 2026-08-24 by the owner: this is not "the
  changelog a player reads", it is the PER-VERSION CHANGE-NOTE ENTRY on BOTH
  storefronts**, and both are surfaces players expect to see move when you ship.
  Sent automatically at upload, archived there permanently:

  | portal | code | surface |
  |---|---|---|
  | Paradox Mods | `ChangeLog = last_changes` (`ParadoxMods.lua:151`) | the **CHANGELOG** panel on the mod page |
  | Steam Workshop | `change_note = mod.last_changes` (`SteamWorkshop.lua:114`) | the **Change Notes** tab |

  Nothing is pasted — but three rules follow and the first draft of this sheet
  had none of them:
  1. ⛔ **Rewrite it before EVERY upload.** It is not rolling copy. Leave it alone
     and the next upload files a *duplicate* note under a new version number.
  2. ⛔ **Keep it terse.** The field is `editor = "text", lines = 3`
     (`Mod.lua:254`), and the observed house style on both stores is a dashed
     line or two. A paragraph renders as a wall in those panels.
  3. ⛔ **It is HISTORICAL.** It describes the version it ships with, forever —
     never write it in the present tense of the pack as a whole.
  ⛔ And do not let it keep saying `"Initial release."` after the first patch.
* **`description` / `short_description`** — only if the fix changes a *claim*
  (e.g. the judgment-call count, or a promise about save safety). Most fixes do
  not touch these.
* **`code` list** — `H-10`: a module absent from `items.lua` **ships absent**.
  `python tools/upload_preflight.py` proves the two lists match, in order.

⛔ **Version numbers are the sitting's, never yours** (`H-02`). Hand-editing these
strings is ordinary agent work; hand-editing `version` is not.

⚠️ **PACKING IS NOT SAVING — measured 2026-08-24.** After File → Pack Mod the
tree was untouched: `git status` clean, `version` still `2`, all 135 comment
lines intact. The force-save that bumps the version and regenerates
`metadata.lua` from memory is `ValidateModBeforeUpload`, which runs at **upload**
(`GedModEditor.lua:836-844`). ⇒ the `git diff metadata.lua` check for stripped
comments belongs **after the upload**, not after the pack.

---

## 4 · The reporter — `reports/FIELD_REPORT_REPLIES.md`

If the fix answers an open field report, the reply is part of shipping it.

* ⛔ **Promise "the next update", never a date** — the tree runs ahead of the live
  listings and the upload is the owner's.
* ⛔ **Only assert what has been observed.** Each draft carries its own list of
  derived-not-witnessed sentences; when a leg witnesses one, strike the caveat
  and say so with the log name. When nothing has witnessed it, cut the sentence
  rather than soften it.
* Name the other mod plainly if one is the cause — owner ruling 2026-08-23.
  `FIX_POLICY` §8 binds store pages and load-order advice, not issue replies.
* ✅ **Issue numbers CAPTURED 2026-08-24 — #1 = F104 "Colonist stuck homeless",
  #2 = F105 "Error when completing milestone"** (both `github.com/catt144/SMR-CommunityFixPack/issues`,
  reporter Keelai, owner assigned). Tie a number to an entry by its **attached
  log name**, not its title: #2's `Mars.exe-20260824-00.01.27-6a22b86d.log` is the
  log F105 was derived from.
* ⛔ **CORRECTED 2026-08-24: record the number in `row_status`, NOT in a new
  front-matter key.** `split_bugs.render_entry` writes only the eleven
  `FRONT_FIELDS`, so an added `issue:` key is **silently dropped** the next time
  entries are rendered — the earlier wording here would have created a fact that
  evaporates. `row_status` is rendered *and* carried into `INDEX.md`. After
  editing it, regenerate the index (`load_from_dir` + `render_index`), never by
  hand.
* ⛔⛔ **READ THE TRACKER THROUGH THE JSON API, NEVER THROUGH THE ISSUE PAGE.**
  ```
  api.github.com/repos/catt144/SMR-CommunityFixPack/issues?state=all      # state + COMMENT COUNT
  api.github.com/repos/catt144/SMR-CommunityFixPack/issues/<n>/comments   # the comments
  ```
  This sweep's own first run fetched issue #1's rendered HTML **three times**,
  once with a cache-busting URL, and got **zero comments** every time. There were
  three — including the posted reply and the reporter thanking us for it. On that
  reading it reported to the owner that a reporter had been left unanswered, and
  wrote that into four documents. ⭐ **The control is free and it was skipped:**
  the list endpoint's `comments` count. If it is non-zero and your reader shows
  nothing, **your reader is wrong**, not the tracker. Generalise it — a rendered
  page is a derived surface, and this file's whole doctrine is that derived
  surfaces are checked against the record, not trusted.
* ⛔ **A drafted reply is not a posted one — and a posted one may not be the
  draft.** Check what is actually on the thread before planning anything. On
  2026-08-24 #1 had Draft A verbatim, while **#2 had a different, earlier reply
  that was never in this repo at all**, written before the verifying legs ran and
  carrying four claims stronger than the tree could support. ⇒ When the owner has
  already answered, your job is not to draft — it is to **diff what was said
  against what is now measured**, and record any sentence that must not migrate
  onto the fix list, a store card or `last_changes`.

---

## 5 · Close the loop

1. `python tools/doccheck.py` — GREEN, and re-emit counts if modules changed.
2. `python tools/upload_preflight.py` — 0 FAIL.
3. Commit **both repos**. ⛔ The site repo is `C:\Dev\SMR-CommunityMods`; the
   TestKit repo is local-only by design and is not part of this sweep.
4. ⛔⛔ **COMMITTING THE SITE IS NOT PUBLISHING IT — AND THIS SHEET MISSED THAT
   UNTIL 2026-08-24.** `publish-site.yml` is **`workflow_dispatch` only, by
   design** (public-docs chain rule 5: publishing is an owner act); the `push:`
   trigger is commented out. So a committed, pushed fix-list entry is **still
   invisible to every player** until the owner runs *Actions → Publish docs site
   → Run workflow*. ⭐ That collides head-on with §2: the store card's count is
   only safe *"because the reader can check it on the page the card links to."*
   Paste a card claiming **eighty** while the deployed site still lists
   **seventy-nine** and the card is falsifiable by the first person who counts.
   ⇒ **The site deploy MUST precede the card paste.** Check it, do not assume:
   ```bash
   # what is actually deployed = head_sha of the newest successful run
   #   api.github.com/repos/catt144/SMR-CommunityMods/actions/runs?per_page=5
   git -C /c/Dev/SMR-CommunityMods log --oneline <deployed_sha>..HEAD -- content/
   git -C /c/Dev/SMR-CommunityMods show <deployed_sha>:content/fix-list.md | grep -c '^??? '
   ```
   ⭐ Derive the live count from the **deployed commit locally** — never by
   counting a rendered page. Found live on 2026-08-24: deployed `a97b8b0` = 79
   entries, repo HEAD `abe46c9` = 80, the one undeployed commit being F105's.
4. In the owner report, separate **what is now true in the tree** from **what
   still needs the owner's hands** (pasting cards, posting the reply, uploading).

## 6 · The checklist, condensed

```
[ ] does this fix have a player surface at all? (unshipped pack defect => none)
[ ] fix-list.md entry added, in the player's section
[ ] grep -c '^??? ' re-derived; section tally sums
[ ] other site pages checked for falsified claims
[ ] STORE_CARD_LIVE.md — Paradox block: count word, headliners, judgment count
[ ] STORE_CARD_LIVE.md — Steam BBCode block: same, edited separately
[ ] metadata.lua last_changes rewritten for THIS version
[ ] metadata.lua description/short_description checked (usually untouched)
[ ] items.lua / code list — upload_preflight 0 FAIL
[ ] field-report reply updated; caveats struck only where a leg witnessed them
[ ] issue number recorded in the entry's row_status (NOT front matter), index regenerated
[ ] tracker read via the JSON API, NOT the issue page; comment count used as the control
[ ] what was ACTUALLY posted diffed against what is now measured; overreaches recorded
[ ] faq.md judgment-call count still true (3 places) if this fix is a judgment call
[ ] doccheck GREEN, both repos committed
[ ] site DEPLOY checked, not just committed — publish-site.yml is manual-only
[ ] deployed entry count == card's count word BEFORE the card is pasted
[ ] owner report separates "true in the tree" from "needs your hands"
```
