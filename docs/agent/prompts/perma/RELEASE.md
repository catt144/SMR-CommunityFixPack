# Release — the one prompt to run for EVERY update (reusable, not self-consuming)

Paste this into a fresh session whenever the owner says "let's do an update / put
out a patch / ship it." It ties together the three existing sub-prompts and is
driven by `RELEASE_OUTBOX.md`, which it clears at the end. **Any model.**

> ♻️ **REUSABLE — do NOT `git rm` this file.** Unlike `POST_UPLOAD_CLOSE.md`, this
> is the standing entry point; it runs again next update.

> ⛔ **The agent never packs, never uploads, never calls a portal** (H-03). Every
> portal action is the owner's. The agent does the words and the repo work around
> them; the owner does the pack + upload in the middle.

> ⭐⭐ **THIS PROMPT SPANS THE OWNER'S UPLOAD — it does not end at the handoff**
> (owner ruling, 2026-09-13). §1 writes the words, **§2 HOLDS and waits for the
> owner**, then §4–§5 close out: ids written back, `metadata.lua`'s stripped
> comments restored, counts re-emitted, STATE updated, **outbox cleared**. The
> close-out is **part of this prompt's job**, never a separate errand the owner has
> to remember to fire. ⚠️ A different session usually resumes at §4 — §2 leaves the
> marker that lets it. **The release is finished at §6, not at §2.**

> 🔧 **Updated 2026-09-10:** the count-word grep no longer assumes "Eighty" (v6 made it
> Forty-six, and the old pattern matched nothing — a vacuous gate).
> 🔧 **Updated 2026-09-12:** auto-fill is settled, not tracked (owner, checklist 155) —
> §2, §3, §4 and §6 record the answer instead of asking for it.

## 0 · Orient
1. `git log --oneline -10` + `git pull` + `git status --short` (other sessions commit here).
2. Read `agent/STATE.md` and `agent/prompts/perma/RELEASE_OUTBOX.md`.
3. `python tools/doccheck.py --emit-counts` — every count comes from here, never
   hand-typed.
4. Read the live count word: `grep -oE '[A-Z][a-z]+(-[a-z]+)? repairs' metadata.lua`.
   Exactly ONE hit expected. ⛔ **Zero hits is a FAIL, never a pass** — a pattern that
   matches nothing proves nothing.
5. ⛔ **Was the LAST release closed?** (Added 2026-09-11: v8 had gone live that afternoon,
   nobody ran `POST_UPLOAD_CLOSE.md`, and the outbox still held its entries as Pending.)
   Three reads, all free: (a) `metadata.lua` `version` vs STATE's "tree version" — a bump
   STATE does not know about is an upload; (b) `grep -c '^\s*--' metadata.lua items.lua` —
   **0 means the Mod Editor writeback was committed with the comments stripped**, and the
   restore is owed; (c) the Steam changelog page, readable with curl:
   `https://steamcommunity.com/sharedfiles/filedetails/changelog/<steam_id>` — its newest
   `Update:` entry and text say what is live. If any of the three says an upload happened
   that the outbox's *Released* section does not carry, run §4–§5 for THAT version first
   (owner's word still owed — ask for the §5 receipt in the checklist), then continue.

## 1 · Agent — apply the outbox to every surface (this is `PUBLIC_SURFACE_SWEEP.md`)
For **each `### Pending` entry** in the outbox, do that entry's row of the
public-surface sweep — open `PUBLIC_SURFACE_SWEEP.md` and follow it; it is the
authority on *which* surfaces and *how*. In short, per pending fix:
- **Site fix list** (`content/fix-list.md` in `SMR-CommunityMods`) — one row in
  the player-facing section, house format.
- **Store card ×3, in lockstep** (the [[store-card-backups-required-not-polish]]
  rule): `reports/STORE_CARD_LIVE.md`, `metadata.lua`'s `description`, and
  `docs/UPLOAD_WORKFLOW.md` §3 backups (Paradox plain + Steam BBCode). Bump the
  **count word** by the outbox's total count impact in all three.
- **`metadata.lua` `last_changes`** — rewrite it as THIS version's change note
  from the pending entries' change-note lines (H-02: never touch `version`).
- **FAQ / judgment-call count** if any pending entry is a judgment call.
- **Reporters** (`PUBLIC_SURFACE_SWEEP.md` §4, `docs/FIELD_REPORT_REPLIES.md`) —
  any pending entry that answers a field report gets its reply updated.
**Gate:** the count word must now match across `metadata.lua`, `STORE_CARD_LIVE.md`
and `UPLOAD_WORKFLOW.md` — `grep -oE '[A-Z][a-z]+(-[a-z]+)? repairs'` on all three
(every hit the same word, and the same number of hits as before the edit), plus the
site fix-list row count. ⛔ Zero hits anywhere is a FAIL. `doccheck` GREEN. Commit
("release words for vNEXT") with `git commit -F <msg> -- <paths>`.

## 2 · Agent — hand off, then ⛔ **HOLD. THE RELEASE IS NOT FINISHED HERE.**
Tell the owner **"ready to upload"** and point them at `UPLOAD_WORKFLOW.md`. Say
plainly what the new count and change note are. ✅ **Settled, do not raise it as a
question** (owner, 2026-09-12, checklist 155): the store bodies **always** auto-fill
from `metadata.lua`; what does not survive is the **formatting**, which the owner
restores from the §3 blocks in a cleanup pass on both stores. ⇒ the §3 backups stay
REQUIRED and are kept current in step 1 — they are NOT "optional polish".

⛔⛔ **THIS IS A PAUSE, NOT AN ENDING (owner ruling, 2026-09-13).** §4 and §5 are part of
THIS prompt's job, not a separate errand the owner has to remember to fire. A release
that stops here leaves the outbox uncleared, the ids unwritten and `metadata.lua`'s
comments stripped — which is exactly what happened on v10 (2026-09-12), where the
close-out went unrun until a later session noticed the writeback sitting uncommitted.

**Three things you MUST do before you stop talking:**

1. ⭐ **Tell the owner in plain words how to resume you**, e.g.: *"When both stores show
   it, say **'uploaded'** and I'll run the close-out — the ids, the comment restore, the
   counts, STATE and the outbox."* ⛔ Do not leave them holding a step they were never
   told is owed.
2. ⭐ **Leave a resumable marker**, because the session that runs §4 is very often a
   DIFFERENT one: put **"v<N> UPLOAD OWED → then `RELEASE.md` §4 close-out"** on
   `STATE.md`'s ⏭ NEXT line. ⚠️ Keep it to one line — replace, never add (STATE is
   byte-capped).
3. **Do not clear the outbox and do not touch any version field.** The Pending entries
   staying put IS the signal that an upload is unconfirmed (§0.5 reads it that way).

⏳ **Then wait.** When the owner says it is up, continue at §3/§4 — do not re-run §1, and
⛔ do not re-derive the counts you already derived and they already shipped.

## 3 · Owner — pack + upload (`UPLOAD_WORKFLOW.md`)
The owner packs (main menu → MOD EDITOR → File → Pack Mod; the version auto-bumps),
uploads **Paradox then Steam**, checks the pages, and reports back the **three** things
`UPLOAD_WORKFLOW.md` §5 asks for (the version the Paradox page shows, anything that
looked wrong, whether the site published). ⛔ **Never ask again whether the
descriptions auto-filled or whether the owner pasted** — both are permanently answered
in §5 (owner, 2026-09-12; "I keep getting this question").

## 4 · Agent — close out (`POST_UPLOAD_CLOSE.md`) — ⭐ **part of THIS prompt, not an errand**
AFTER the owner confirms the listing exists: run `POST_UPLOAD_CLOSE.md` — the
`pdx_id`/`steam_id` writeback commit with the stripped `metadata.lua` comments
restored, counts re-emitted, `STATE.md` updated, entries flipped to their live
status. ⛔ Auto-fill is **no longer an open question** — do not record a per-cycle
result for it (UPLOAD_WORKFLOW §5, owner 2026-09-12).

⚠️ **If a FRESH session is doing this** (the usual case — §1 and §4 are rarely the same
session): orient first (`git pull`, `git log`, `git status --short`, `STATE.md`), then
read the upload off the tree rather than trusting a handoff line — §0.5's three free
reads are exactly that check.

⛔⛔ **THE WRITEBACK IS SITTING IN THE WORKING TREE AND IT HAS STRIPPED EVERY COMMENT.**
Packing rewrites `metadata.lua` and `items.lua` from the Mod Editor's own serialiser:
`version` auto-bumps (H-02, never chase it), `code_hash` changes, `pdx_version` moves —
and **all the `--` commentary is gone** (on v10: 319 → 0 and 51 → 0). Restoring it is
this step's job.

⇒ **Until this step has run, NO session may commit `metadata.lua` or `items.lua` for any
other reason.** A commit that names either file takes its working-tree content, so an
unrelated edit would silently bury ~400 lines of load-bearing commentary. Check with
`grep -c '^\s*--' metadata.lua items.lua` — **0 means the restore is still owed.**

## 5 · Agent — CLEAR THE OUTBOX (the step that makes this repeatable)
In the same close-out commit, rewrite `RELEASE_OUTBOX.md`:
- Move every `### Pending` entry into **Released in v<the new version>**, newest
  first, keeping its one-line summary.
- Leave *Pending* empty.
This is what stops a fix shipping twice or being forgotten. ⛔ The outbox is not
cleared until the upload is CONFIRMED — never on "ready", only after step 4.

## 6 · Done
Summarise to the owner: version each store shows, the count now live, the site
status, and that the outbox is clear. Route any
lesson to its home (`WORKFLOW.md`/`FIX_POLICY.md`), append the leg to
`archive/SESSION_LOG.md`.
