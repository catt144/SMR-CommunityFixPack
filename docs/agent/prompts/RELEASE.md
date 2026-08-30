# Release — the one prompt to run for EVERY update (reusable, not self-consuming)

Paste this into a fresh session whenever the owner says "let's do an update / put
out a patch / ship it." It ties together the three existing sub-prompts and is
driven by `RELEASE_OUTBOX.md`, which it clears at the end. **Any model.**

> ♻️ **REUSABLE — do NOT `git rm` this file.** Unlike `POST_UPLOAD_CLOSE.md`, this
> is the standing entry point; it runs again next update.

> ⛔ **The agent never packs, never uploads, never calls a portal** (H-03). Every
> portal action is the owner's. The agent does the words and the repo work around
> them; the owner does the pack + upload in the middle.

## 0 · Orient
1. `git log --oneline -10` + `git pull`.
2. Read `agent/STATE.md` and `agent/prompts/RELEASE_OUTBOX.md`.
3. `python tools/doccheck.py --emit-counts` — every count comes from here, never
   hand-typed.
4. Read the live count word: `grep -o 'Eighty[a-z-]* repairs' metadata.lua`.

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
**Gate:** the count word must now match across `metadata.lua`, `STORE_CARD_LIVE.md`
and `UPLOAD_WORKFLOW.md` — `grep -o 'Eighty[a-z-]* repairs'` on all three, plus
the site fix-list row count. `doccheck` GREEN. Commit ("release words for vNEXT").

## 2 · Agent — hand off
Tell the owner **"ready to upload"** and point them at `UPLOAD_WORKFLOW.md`. Say
plainly what the new count and change note are, and that the store bodies should
auto-fill from `metadata.lua` (⚠️ still UNTESTED — the §3 backups are the paste
fallback, kept current in step 1; they are NOT "optional polish").

## 3 · Owner — pack + upload (`UPLOAD_WORKFLOW.md`)
The owner packs (Mod Editor → Pack Mod, version auto-bumps), uploads **Paradox
then Steam**, checks the pages, and reports back the four things
`UPLOAD_WORKFLOW.md` §5 asks for (each store's version, whether the descriptions
auto-filled or needed a paste, anything that looked wrong, whether the site
published).

## 4 · Agent — close out (`POST_UPLOAD_CLOSE.md`)
AFTER the owner confirms the listing exists: run `POST_UPLOAD_CLOSE.md` — the
`pdx_id`/`steam_id` writeback commit with the stripped `metadata.lua` comments
restored, counts re-emitted, `STATE.md` updated, entries flipped to their live
status. Record whether auto-fill worked (the open question UPLOAD_WORKFLOW §2/§5
tracks).

## 5 · Agent — CLEAR THE OUTBOX (the step that makes this repeatable)
In the same close-out commit, rewrite `RELEASE_OUTBOX.md`:
- Move every `### Pending` entry into **Released in v<the new version>**, newest
  first, keeping its one-line summary.
- Leave *Pending* empty.
This is what stops a fix shipping twice or being forgotten. ⛔ The outbox is not
cleared until the upload is CONFIRMED — never on "ready", only after step 4.

## 6 · Done
Summarise to the owner: version each store shows, the count now live, whether the
paste auto-filled, the site status, and that the outbox is clear. Route any
lesson to its home (`WORKFLOW.md`/`FIX_POLICY.md`), append the leg to
`archive/SESSION_LOG.md`.
