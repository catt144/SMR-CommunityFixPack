# Closing a confirmed upload

This is the close procedure consumed by
`docs/agent/prompts/perma/release_prompt.md` §4. It is not a prompt and it never
uploads, repacks, opens the Mod Editor or calls a portal.

## Preconditions and receipts

Do not begin until the owner confirms the upload. The current receipt asks only:

1. the version shown on the Paradox page;
2. anything that looked wrong on either store;
3. whether the site published.

Description auto-fill and the formatting paste are settled and are not asked per
release.

## 1 · Verify from the tree

In a fresh session, run `git log --oneline -10`, `git pull`, and
`git status --short`, then read STATE and the outbox. Inspect:

```text
git diff -- metadata.lua items.lua
```

The writeback should expose the new version/id fields. Compare them with STATE,
Released history and the owner's receipt. When readable, the newest Steam change
note is another receipt. A handoff sentence alone is not proof of an upload.

Count leading comment lines in both files before any commit. Zero means the editor
serializer stripped them and restoration is owed. A zero-hit command never proves
the comments are safe.

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
- Move each outbox Pending entry under `Released in v<N>`, newest first, and leave
  Pending empty. Do this only after owner confirmation.
- Update any release status whose existing policy is satisfied; do not infer play
  evidence from publication.
- Append the release leg to `docs/archive/SESSION_LOG.md` without rewriting older
  archive text.
- Re-run `python tools/doccheck.py --emit-counts`, then `python tools/doccheck.py`.
  Report counts only from that run and copy any warning verbatim.

Commit the writeback, restored comments and record changes with exact pathspecs.
Report the store versions, live count, site status and empty Pending ledger. Do not
claim a portal result the owner did not confirm.
