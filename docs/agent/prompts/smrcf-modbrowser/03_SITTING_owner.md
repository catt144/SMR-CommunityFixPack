# C·03 — the browser sitting · ⚠️ OWNER AT THE KEYBOARD · ~15 min

**The only place these defects are observable at all.** Read `README.md`, then
`STATE.md`, then this, then `## Notes from upstream` — 02 fills in §2.

## 0 · Staleness check
```
git log --oneline -10
git pull
```
⛔ Do not start if 02 has not filled in §2, or if the fixture (a Paradox mod
**with screenshots**) has not been re-confirmed today.

## 1 · 🗒 Live todo list, and keep the sent/checked/outstanding ledger.

## 2 · The queue — decider first

*(02 fills in specifics.)*

1. ⭐ **Screenshots** — open the detail page of a mod that has them. **Correct =
   the screenshot strip appears below the main image and clicking a thumbnail
   selects it.** Failure signature: empty strip, or a `[LUA ERROR]` naming the
   concat.
2. **Hyperlinks** — a mod whose description contains a link. **Correct =** it
   renders as a link and opens externally. ⚠️ **Watch for XText misbehaviour**,
   not just for the link: garbled glyphs, missing text, a wrong font, anything
   odd anywhere on that page. **That is the falsifier**, and it is the reason
   this item is being observed rather than assumed.
3. **Thumbnails** — only if 01 approved it. Correct = a changed preview appears
   without a version bump.

## 3 · Rules for the sitting

1. ⭐⭐ **Relay every owner verbatim through the log-note primitive as spoken.**
   A transcript-only quote is unreadable to the audit forever.
2. **Judge by the log, flushed** — but here the *screen is also evidence*, and it
   is the only evidence for items 1–2. **Screenshots, one per claim.**
3. The owner may reorder live; deviation is never scored against the estimate.
4. ⚠️ **Requires Paradox Mods reachable.** If the service is down or the account
   is not signed in, **stop** — nothing here is observable offline, and that is a
   precondition, not a failure.

## 4 · Scope fence
**IN:** the three checks, screenshots, owner verbatims, the log.
**OUT:** ⛔ fixing anything mid-sitting · ⛔ granting statuses (04 weighs them) ·
⛔ installing or enabling any third-party mod — including
`smr-community-fixes`, which would invalidate every gate baseline.

## 5 · Stop conditions
- Paradox Mods unreachable → stop, reschedule; record it as a precondition miss.
- Any XText misbehaviour on item 2 → **stop that item, disable the module,
  record.** The falsifier has fired and that is a real result.
- A module reads `inactive` or errors → bank the rest, record the failure.

## 6 · ⛔ What may not be claimed
- ⛔ **`tested-attended`** without a screenshot per claim.
- ⛔ **"No regression"** from one page. Say how many pages, which mods.
- ⛔ **"The cache is fixed"** without actually having replaced an image and
  reloaded — otherwise it is untested, however plausible.
- ⛔ Anything about mods you did not open.

## 7 · Close-out
One commit: readings on `C52` with provenance per row · screenshots referenced ·
**owner verbatims in the archived log** · log archived `git add -f` · outbox to
`04_AUDIT` · checklist line struck · manifest row struck · `git rm` this file ·
doccheck GREEN · grave named · push.

## Notes from upstream
