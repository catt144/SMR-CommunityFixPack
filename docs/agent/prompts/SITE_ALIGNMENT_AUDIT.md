# Site alignment audit — find and FIX every promise the pack no longer keeps (one-off, model-agnostic)

**Written 2026-09-13 by `smr-bugfixpack-c2` at the owner's ask. Lifecycle: `git rm` when fired.**
**This one AUDITS AND FIXES.** It is not `perma/SITE_AUDIT.md` (which only reads the live site) and not
`perma/PUBLIC_SURFACE_SWEEP.md` (which authors for ONE change). It clears an accumulated backlog.

> ⛔⛔ **YOU MAY NOT FIRE THE SITE DEPLOY.** Publishing is the owner's act — `publish-site.yml` is
> `workflow_dispatch` only, by design. You report that the deploy is ready. You never take it, and never
> propose automating it.

> ⭐ **v10 IS ALREADY LIVE ON BOTH STORES** (uploaded 2026-09-12, owner confirmed, cards checked). The
> store cards are **verified correct** for v10 — count word, headliners, judgment calls, retired bullets.
> ⛔ Do not re-derive the v10 release numbers; that verification is done. You are looking for something else.

---

## 0a · ⛔⛔ RUN `perma/POST_UPLOAD_CLOSE.md` FIRST — this audit is SECOND

**As of 2026-09-13 the v10 upload's Mod Editor writeback is sitting UNCOMMITTED in
`C:\Dev\SMR-BugFixPack`, and it has STRIPPED EVERY COMMENT from `metadata.lua` and `items.lua`**
(319 → 0 and 51 → 0; `version` 10 → 11, `pdx_version` "8" → "9", new `code_hash` — all the normal
auto-bump, H-02, never chase it). That is the documented post-upload state and
`perma/POST_UPLOAD_CLOSE.md` is the prompt that restores the comments and writes back the ids.

⛔ **This audit may edit `metadata.lua` (§3a). If it commits that file before the close-out has restored
the comments, ~396 lines of load-bearing commentary are silently lost in a commit about website wording.**

⇒ **Check first:** `grep -c '^\s*--' metadata.lua items.lua`. **If either reads 0, STOP** — the close-out
has not run. Either run `perma/POST_UPLOAD_CLOSE.md` first, or do the audit while touching **neither**
file and hand the card fixes to the owner as paste text plus a note that the repo copies still need
updating after the close-out. ⛔ Never "restore" the comments yourself as a side quest.

## 0 · Orient

`git pull` · `git log --oneline -10` · `git status --short` · `ListAgents` in **both**
`C:\Dev\SMR-BugFixPack` **and** `C:\Dev\SMR-CommunityMods` — an unpushed site commit can never deploy.
Read `docs/agent/STATE.md`. **Open a live todo list and keep it current** — one entry per numbered check;
the owner reads it to decide when to step in. This audit launches no game, so the stale-probe gate does not apply.

---

## 1 · ⭐ THE DEFECT THIS EXISTS TO FIND — read this before anything else

`PUBLIC_SURFACE_SWEEP.md` §1 already says to check the site pages "for any claim **the new fix**
falsifies". Every check it teaches runs in that one direction. **A retirement falsifies in the opposite
direction: the pack quietly STOPS doing something a page still promises**, and the sweep has no worked
example, no grep and no prompt for that case. So retirements have never been swept for orphaned promises.

**The proven instance** (found 2026-09-12, still unfixed — fix it in §3):
`C:\Dev\SMR-CommunityMods\content\faq.md:117` tells players the save-repair pass looks for and undoes
**"phantom farm oxygen"**. That was F37's LoadGame sweep. F37 is **retired**, and ck159 (2) ruled the
clean-up an **accepted loss** that does **not** move into `90_SaveSanitizer.lua`. Verified: nothing in
`Code/` touches `farm_id`, farm oxygen or `air_consumption` any more; the sanitizer repairs F35, F48 and
F95 only. ⇒ **The sentence is false today.**

⭐ **It is almost certainly not alone.** Since hotfix 2 (2026-09-08) **40 module files have been deleted
from `Code/`** — derive the set yourself, do not trust that number:

```
git log --diff-filter=D --name-only --pretty=format:"%h %ad" --date=short --since=2026-09-08 -- 'Code/*.lua'
```

Exactly **one** of those 40 has ever been checked for an orphaned promise, and it was found wrong.
That is the whole job.

---

## 2 · The audit — what to check, and how

### 2a · Build the retired set

From the command above plus the four v9/v10 retirements (**F60**, **F37**, **F43** + its **F118** rider,
**F31**). For each, get what it USED to promise: read the deleted body from git
(`git show <sha>^:Code/<file>`) and its entry in `docs/agent/bugs/`. ⛔ An entry's own words are a claim —
what matters is what a **player-facing page** says the pack does.

### 2b · Sweep every player-facing surface against that set

| surface | where |
|---|---|
| site pages | `C:\Dev\SMR-CommunityMods\content\` — `fix-list.md`, `index.md`, `faq.md`, `install.md`, `for-modders.md`, `legacy-1-0-7.md` |
| **live store cards** | both portals, **already published** — plus their sources: `metadata.lua` `description`, `reports/STORE_CARD_LIVE.md`, `docs/UPLOAD_WORKFLOW.md` §3 |
| repo front page | `README.md` |
| reporter drafts | `docs/FIELD_REPORT_REPLIES.md` — ⛔ **read-only here**, replies are PULL-ONLY (ck165). Note a stale promise; never draft or send one. |

**The highest-risk shape is a named list of specific repairs**, because each item is a separate promise
and one can go stale without the sentence looking wrong. `faq.md`'s save-repair list is exactly that
shape; find the others before assuming it is unique.

### 2c · Also settle these known items

1. **The farm-oxygen sentence** (§1) — fix it.
2. **Judgment-call count.** The fix list has **4** `??? question` rows. Committed `faq.md` says "Three
   judgment calls"; the **working tree** already says "Four" (the v10 release pass edited it but could not
   commit — see §4). Confirm the working-tree text is right and that nothing else states a judgment-call
   count. ⚠️ `PUBLIC_SURFACE_SWEEP` §1 records that a judgment-call change falsifies `faq.md` in **three**
   places — check all three.
3. **Live-vs-committed row count.** The deployed site is a **claim with a date on it**. ⛔ Never quote a
   stored "deployed = <sha>" — read the deployments API (`perma/SITE_AUDIT.md` §1) and compare to the
   committed tree.

---

## 3 · The fixes — you apply them

**Fix what is factually wrong.** ⛔ This is not a rewrite pass: do not restyle, re-voice or "improve"
anything that is merely not to your taste. A sentence that is TRUE stays exactly as it is.

⚖️ **The VOICE RULE binds every word you write**: plain enough for the players, precise enough for the two
Paradox developers who plan hotfixes from our fix list. ⛔ **No "no guarantees" / "unverified" / "not
witnessed" hedging on a public surface.** Scope is said by stating what a fix does and for whom. If the
owner could not follow a sentence, it is word salad and it fails.

### 3a · ⛔ THE TWO-PLACE RULE for anything on a store card

The owner **can** hand-edit both store pages, so a card finding is fixable now. **But every upload
OVERWRITES both page bodies from `metadata.lua` — the `description` IS the card.** So a hand-edit made
only on the live page **silently reverts at the next upload**.

⇒ **Any card fix lands in BOTH places or it is not done:** the live page (the owner, by hand) **and**
`metadata.lua` + `reports/STORE_CARD_LIVE.md` + `docs/UPLOAD_WORKFLOW.md` §3 backups (you, in the repo).
Give the owner the exact replacement text to paste, per portal. ⛔ **You never touch a portal yourself**
(H-03) and ⛔ **never hand-set any version field** (H-02) — a card text fix needs no version change.

### 3b · ⛔ THE OWNER'S THREE PARED FILES — separate factual fixes from their editorial paring

`content/faq.md`, `content/for-modders.md` and `content/install.md` carry the owner's **uncommitted**
modder-doc paring, which they have **not ruled on** (related: open decision **47**). `faq.md` additionally
carries the v10 release pass's judgment-call edit. Your farm-oxygen fix goes into that same file. Three
authors, one working tree.

**Do this:**

1. Make your factual corrections in the working tree as normal.
2. **Stage only YOUR hunks and the release pass's** — `git add -p` (or `hash-object` + `update-index`).
3. **Leave every hunk of the owner's paring UNCOMMITTED.**
4. ⛔ **Verify the split before committing:** `git diff --cached` must show only factual corrections, and
   `git diff` must show only the paring. If you cannot cleanly separate a hunk, **stop and ask the owner** —
   do not commit it either way, and do not "tidy" the paring to make separation easier.
5. ⛔ **Never revert, resolve, rewrite or rule on the paring.** It is the owner's editorial decision and
   decision 47's business, not this audit's. ⛔ Never `git checkout`, `stash` or `restore` in that repo.

This matters because it **unblocks the deploy**: the factual fixes can go live without the owner being
forced to rule on an editorial rewrite first.

### 3c · Close the hole permanently

Add the missing direction to `perma/PUBLIC_SURFACE_SWEEP.md` §1 — a short **"When a fix is RETIRED"**
check, in the same shape as the judgment-call check it already carries: what to grep, which files, and the
reason (a retirement orphans a promise rather than falsifying one). ⛔ Keep it tight; that file is already
long, and the sweep is run under time pressure.

---

## 4 · Gates before you commit

- `python tools/doccheck.py` **GREEN** — red blocks. Counts from `--emit-counts`, ⛔ never hand-typed.
- If you changed `metadata.lua`: `python tools/parsecheck.py` and `python tools/upload_preflight.py`
  (expect **0 FAIL**). ⛔ A card text change must NOT move `version`, `version_major`, `version_minor` or
  `pdx_version` (H-02).
- ⚠️ **`STATE.md`'s hard cap is TEMPORARILY 24 KiB** and reverting it is an owed post-launch task
  (`perma/HANDOFF_ORCHESTRATOR.md` §1a). ⛔ Do not spend that headroom: replace lines, never add them, and
  do not fire `STATE_EVICTION.md`.
- ⭐ **THE MARKER OBLIGATION:** checklist items carry a status marker (`<!-- ck:159 status:ruled owner:no -->`)
  and a register is generated from them. **Changing an item's status ALSO means updating its marker** —
  nothing in `WORKFLOW.md` or `CLAUDE.md` says so yet, which is why it is said here. Vocabulary is
  `open` · `ruled` · `closed` · `deferred` with `owner:yes|no`; ⛔ do not invent a status word.
- **Checklist-only edit ⇒ `--regen-waiting`. Touched an entry too ⇒ full `--regen`.** ⛔ `--regen` rebuilds
  the indices from every entry **on disk, a peer's uncommitted ones included** — run
  `git status docs/agent/bugs/` first and coordinate if you see foreign ` M`/`??`.
- ⛔ **All sessions share ONE git identity** — `git log --author` attributes nothing. Identify by **sha +
  diff**. ⛔ **A pathspec is only HALF a commit fence**: for a path you name, git commits that path's
  **working-tree** content, a peer's unstaged edits included. On a shared file, stage your own hunks and
  commit **without** a pathspec. Never `git add -A`, never a bare `git commit`. `-F <file>` for the message
  (embedded quotes split under PS 5.1). Then **push** — pushing is standing-allowed.

---

## 5 · Report — and the one thing the owner is waiting for

Close with a **plain verdict on whether the site deploy is safe to fire**, because that is the question
they asked. Say one of:

- ✅ **"Fire the deploy"** — everything factual is fixed, committed and pushed; name the shas.
- ⛔ **"Do not fire yet"** — and say exactly what is outstanding and whose it is.

Also give them:

1. **The findings, most serious first.** For each: the surface, the exact sentence, which retired module
   orphaned it, and what you changed it to. ⛔ If you found nothing beyond the farm-oxygen sentence, **say
   so plainly** — a short honest list beats a padded one, and "I checked 40 and one was wrong" is a result.
2. **Any store-card fix, as paste-ready text per portal**, with the §3a warning restated: the repo copy is
   updated, and the live page needs their hand-edit or it stays wrong until v11.
3. **The state of the three pared files**, precisely: what you committed out of them, what remains
   uncommitted, and that ruling on the paring is still theirs and still open (decision 47).
4. ⛔ **SKIPs BY NAME, never a total.** Anything you did not check, say which and why.
5. Anything you think is wrong that you did **not** act on — tell them, do not fix it unasked.
