# Closing a confirmed upload

This is the close procedure consumed by
`docs/agent/prompts/perma/release_prompt.md` §4. It is not a prompt and it never
uploads, repacks, opens the Mod Editor or calls a portal.

## Preconditions and receipts

Do not begin until the owner confirms the upload. The current receipt asks only:

1. anything that looked wrong on either store;
2. whether the site published.

Description auto-fill and the formatting paste are settled and are not asked per
release. Neither is a store page's version number: the owner ruled on 2026-09-23
that those numbers tick on a bare editor save as well as on an upload, so they
track nothing. `metadata.lua`'s `version` is the only version tracked, and the
Steam changelog confirms the upload.

## 1 · Verify from the tree

In a fresh session, run `git log --oneline -10`, `git pull`, and
`git status --short`, then read STATE and the outbox. Inspect:

```text
git diff -- metadata.lua items.lua
```

The writeback should expose the new version/id fields. Compare them with STATE and
the outbox's `Last released` line. The newest `Update:` entry on the Steam changelog
is the upload's confirmation; read it every time. A handoff sentence alone is not
proof of an upload.

Count leading comment lines in both files before any commit. Zero means the editor
serializer stripped them and restoration is owed. A zero-hit command never proves
the comments are safe.

If the outbox's Pending names a **canary** in `metadata.lua`, run its check now, on the
stripped working-tree copy and the downloaded Workshop package, before §2 restores the
comments: the restore brings the canary back from git and would erase the reading. The
first such check is `docs/agent/reports/LOAD_ORDER_FIRST_BUILD_2026-09-25.md`, "The C canary".

## 2 · Preserve writeback, restore comments

Keep the upload's actual `version`, `pdx_id`, `pdx_version`, `steam_id` and other
serializer writeback fields. Never normalize or hand-set a version. Restore the
hand-written comments from the pre-upload tree in the same commit, in both
`metadata.lua` and `items.lua`.

Until this restoration is complete, no session may commit either file for another
reason. A commit naming a path takes the stripped working-tree copy and can bury
the commentary. Review the whole diff after restoration. The `fixpack-v1.0.0` tag
does not move with this post-upload commit.

## 3 · Finish the records

- Update STATE with what is live and remove the one-line UPLOAD OWED marker.
- Append each outbox Pending entry to `docs/archive/RELEASE_HISTORY.md` under
  `### Released in v<N> (date)`, set the outbox's `Last released` line, and leave
  Pending empty. Do this only after owner confirmation.
- Update any release status whose existing policy is satisfied; do not infer play
  evidence from publication.
- Append the release leg to `docs/archive/SESSION_LOG.md` without rewriting older
  archive text.
- Re-run `python tools/doccheck.py --emit-counts`, then `python tools/doccheck.py`.
  Report counts only from that run and copy any warning verbatim.

Commit the writeback, restored comments and record changes with exact pathspecs.
Report what the Steam change note confirms, the live count, site status and the
empty Pending ledger. Do not claim a portal result the owner did not confirm.
