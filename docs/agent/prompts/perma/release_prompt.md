# Release — prepare, hold for the owner, then close

Run this prompt when the owner asks to ship an update. It owns the whole release
lifecycle, including the work after the owner's upload. A release is not finished
at the handoff.

> ⛔ The agent never packs, uploads, opens the Mod Editor, or calls a portal API.
> The owner performs every portal action through `docs/UPLOAD_WORKFLOW.md`.

## Release rails

- Tag `fixpack-v1.0.0` marks the bytes that were packed. Never move it without an
  equivalent gate.
- Never hand-set `metadata.lua`'s `version`, `version_major` or `version_minor`.
  An editor save bumps the version, and upload validation force-saves a dirty mod;
  a hand-set value can double-bump. Other deliberate edits to `metadata.lua`, such
  as descriptions, `last_changes` and the gated code list, are ordinary work.
- A zero-hit verification is a failure. Record the expected presence count before
  an edit and require the post-edit command to find the expected members.
- Do not track, report or ask for the version number either store page shows.
  Owner ruling, 2026-09-23: those numbers tick on a bare editor save as well as on
  an upload, so they track nothing. `metadata.lua`'s `version` is the only version
  this project tracks, and the newest `Update:` entry on the Steam changelog is
  what confirms an upload happened.

## 0 · Orient and expose the full lifecycle

1. Run `git log --oneline -10`, `git pull`, and `git status --short`.
2. Read `docs/agent/STATE.md`, `RELEASE_OUTBOX.md`,
   `docs/agent/support/RELEASE_SURFACES.md`,
   `docs/agent/support/POST_UPLOAD_CLOSE.md`, and `docs/UPLOAD_WORKFLOW.md`.
3. Start a live five-item list: derive batch; prepare and verify surfaces; hand
   off and HOLD; verify and close after upload; clear records and finish. Exactly
   one unfinished item is in progress.
4. Run `python tools/doccheck.py --emit-counts`; carry no stored count.
5. Check whether the preceding upload is already closed. A tree version ahead of
   STATE, an upload newer than the outbox's `Last released` line, or zero comment lines in
   `metadata.lua`/`items.lua` means close-out may still be owed. Resolve that
   release through §4 before preparing another one. Before any "what is live" claim, also curl
   the Steam changelog page (`steamcommunity.com/sharedfiles/filedetails/changelog/3787202810`);
   its newest `Update:` entry is the control, since the Paradox page is JavaScript-only and
   unreadable.

## 1 · Derive the batch and prepare every required surface

The batch is exactly the filled `### Pending` entries in `RELEASE_OUTBOX.md`.
Use `docs/agent/support/RELEASE_SURFACES.md` to update the player-facing surfaces,
derive and reconcile counts, rewrite this version's change note, and run the
preflight gates. There is no standing reply, comment, discussion or tracker step.

Commit the prepared release words with exact pathspecs. Do not touch version
fields. Do not continue while doccheck or `tools/upload_preflight.py` reports a
failure.

## 2 · Hand off, then HOLD

Tell the owner "ready to upload", state the derived count and change note, and
point to `docs/UPLOAD_WORKFLOW.md`. The owner uploads Paradox first and Steam
second, restores the store formatting, then publishes the site.

Before yielding:

1. Say exactly how to resume: **"When both stores show the update, say 'uploaded'
   and I will verify the writeback, restore the comments, update STATE and clear
   the outbox."**
2. Replace STATE's NEXT line with one resumable marker:
   `v<N> UPLOAD OWED → then release_prompt.md §4 close-out`.
3. Leave Pending intact and do not touch a version field.

This is a pause, not completion. Wait for the owner's confirmation.

## 3 · Owner upload

The owner follows `docs/UPLOAD_WORKFLOW.md`. The current receipt is only: anything
that looked wrong on either store, and whether the site published. The description
auto-fill and formatting paste are settled facts, not questions to ask again, and
neither is a store page's version number (Release rails).

## 4 · Resume, often in a fresh session

After the owner confirms the upload, read
`docs/agent/support/POST_UPLOAD_CLOSE.md` and execute it. In a fresh session, run
§0's Git commands and read the tree, outbox and owner receipt again. Verify the
upload from the writeback and receipts; do not trust a handoff claim by itself.

The Mod Editor writeback strips the comments from `metadata.lua` and `items.lua`.
Until the close procedure restores them while preserving the new ids and version
fields, no session may commit either file for another reason.

## 5 · Clear the outbox only after confirmation

Only after the owner confirms the upload and §4 verifies it, append every Pending
entry to `docs/archive/RELEASE_HISTORY.md` under `### Released in v<N> (date)`,
set the outbox's `Last released` line to v<N>, and leave Pending empty. The outbox
holds only what has not shipped; this prevents a change shipping twice. Never clear the outbox at "ready to upload".

## 6 · Finish

Re-emit counts, finish the release records, remove the STATE marker, run doccheck,
and commit the close-out with exact paths. Report what the Steam change note
confirms, the live count, site status and that Pending is empty. Do not claim a
release step the owner did not confirm.
