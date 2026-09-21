# Preparing player-facing release surfaces

This is the surface-update procedure consumed by
`docs/agent/prompts/perma/release_prompt.md` §1. It is not a prompt or a separate
release front door.

## 1 · Inputs and scope

- The filled Pending entries in `docs/agent/prompts/perma/RELEASE_OUTBOX.md` are
  the batch. The corresponding bug entries are authority for claims.
- Run `python tools/doccheck.py --emit-counts` before writing a count. Record the
  command, filter and members that reconcile each total.
- A pack-internal repair that never shipped broken has no player surface. Do not
  invent a fix-list row, card claim or change-note line for it.
- Write the symptom in player language. Use "error", not "crash", for a caught Lua
  error. Mark a judgment call only when the entry records one.

## 2 · Site and repository surfaces

Work in `B:\Dev\SMR\SMR-CommunityMods` only after reading its status. Do not overwrite,
stash or commit another person's dirty file.

For an added, retired or materially respecified fix:

1. Update `content/fix-list.md` in the section where a player would look.
2. Search every content page for promises the change falsifies. A retirement can
   leave a named promise behind even after its fix-list row is removed.
3. Recount fix-list members from the file and reconcile the section counts to the
   total. A zero-hit count is a failure, not an empty success.
4. Update judgment-call wording in `content/index.md` and `content/faq.md` when
   applicable, and check the fix pack repo's own `README.md` — the GitHub front
   page reporters and the developers land on — for stale status and emitted
   counts. Not the site repository's: this step exists because that front page
   is the one nothing else sweeps.

Committing the site repository does not deploy it. Deployment is the owner's act.

## 3 · Store bodies and shipped strings

The card body has maintained copies that must move together:

- both blocks in `docs/agent/reports/STORE_CARD_LIVE.md`;
- `metadata.lua`'s portal-neutral `description`;
- the Paradox and Steam backup blocks in `docs/UPLOAD_WORKFLOW.md` §3.

The section order is the owner's (2026-09-19): intro, SOME OF WHAT IT FIXES,
BUGS, QUESTIONS AND MODDING, then every featured section, and HOW IT WORKS last.
A newly featured item gets its own `FEATURED:` section placed after BUGS, QUESTIONS
AND MODDING, so the route to the site stays high on the page.

Update the count word, headliners and judgment-call claim in every applicable
copy. Before editing, count the repair-word matches in each file; afterward require
the same expected number of matches and the same word everywhere. Zero hits fail.

Rewrite `metadata.lua`'s `last_changes` for this release from the Pending entries.
It is a per-version store change note, not rolling copy. Keep it terse. Update
`short_description` only if the batch changes one of its claims. Keep `items.lua`
and the `metadata.lua` code list aligned, but never edit a version field.

## 4 · Gates and handoff

Before the release prompt hands off:

1. Reconcile emitted counts with the site members and every store-card count word.
2. Run `python tools/doccheck.py` and require GREEN.
3. Run `python tools/upload_preflight.py` and require zero FAIL lines.
4. Commit each repository with exact pathspecs and report what is committed but
   not yet public.

The owner then follows `docs/UPLOAD_WORKFLOW.md`: mod upload, store-page formatting
on both portals, then site publication. Store pages precede the site because an
upload overwrites their bodies from `metadata.lua`; the same-sitting count
agreement still must be restored. The agent does not perform any of those actions.
