# Post-upload close — fire this AFTER the listing exists, never before

♻️ **SELF-CONSUMING.** `git rm` this file in your closing commit, naming its grave.

⛔⛔ **PRECONDITION: the owner has already uploaded.** If nothing is published,
**STOP** — there is nothing here to do and `H-03` still binds: the first portal
API call **creates the listing**, and no agent makes it.

⛔ **You do not upload, re-pack, or call a portal.** Every portal action in this
document is the owner's; your job is the repo work that follows theirs.

## 0 · Read path

```
git log --oneline -10 && git pull
git diff -- metadata.lua
python tools/doccheck.py --emit-counts
```

`docs/agent/STATE.md` · `reports/RELEASE_PORTAL_PREP.md` **§0.5(c)(d)(e)(f)** ·
checklist **67** · `EF-014`.

## 1 · 🗒 Live todo list — one item per job below

## 2 · Job 1 — the writeback commit, and the damage that rides with it

The forced saves write `pdx_id` / `PdxMod` / `pdx_version` (and `steam_id` if
Steam ran) into `metadata.lua`. ⭐ **Commit them: they are how every future update
finds the published listings.** Losing them means a future release cannot target
the mod.

⚠️ **But the same save REGENERATES `metadata.lua` from memory, so every
hand-written comment in it is gone** (`Mod.lua:967` and §0.5(b)). ⇒ **Restore the
stripped comments from git in the SAME commit**, keeping the new id fields.
`git diff -- metadata.lua` is the whole job: what you keep is the ids, what you
put back is the prose.

⛔⛔ **DO NOT "CORRECT" `version` BACK TO 0.** After a Paradox upload the tree
sits at `version = 1` **by design** — Paradox saves *after* the upload returns,
so the listing got 1.0.0 and the tree moved on. Normalising it would be a silent
lie about what is published. ⇒ **Record what `version` actually reads** and
whether Steam has run yet.

⚖️ **Route to the owner, do not decide:** checklist **37 Q2** — Steam's number.
Steam saves *before* packing, so a straight second upload ships **1.0.1**; the
sheet's §0.5(c) has the one-restart route to 1.0.0. That call is theirs and it is
only decidable now.

## 3 · Job 2 — the three checks the sheet owes

- **§0.5(d)** — the portal's required-game-version field, **350453**. The owner
  sets it if the page offers one; **you record which happened.** If the field does
  not exist, write that on the sheet and move on — nothing else to do.
- **§0.5(f)** — the delivered-bytes check. The blank row was filled **at pack
  time** with the real md5/bytes/entry count. If the owner gives you the path to
  the downloaded pack, md5 it yourself and compare; expect **82 entries**.
  ⛔ **Never write an md5 you did not compute from a real file.** ⚠️ File-level
  only — `H-09` makes a behavioural check on this rig measure the junction.
- **The tag does NOT move.** `fixpack-v1.0.0` marks the bytes that were packed and
  uploaded; the writeback commit happens after that and must not drag it along.
  ⛔ Say so if anyone later asks why the tag is behind `HEAD`.

## 4 · Job 3 — close the records, then hand off

- `STATE.md`: strike the ④ hold and the *NOTHING IS PUBLISHED* line — ⭐ **this is
  the one moment in this project's history when striking them is correct**
  (`H-04` exists to stop it happening early; the owner's completed upload is the
  word it waits for). Record what is live, on which portal, at which number.
  Re-emit counts; if `doccheck` warns on bytes, relay the line **verbatim**.
- `docs/PLAYTEST_CHECKLIST.md`: the owner's receipt — what is published, what the
  ids are, what §0.5(d)/(f) found, and 37 Q2 if still open.
- `docs/archive/SESSION_LOG.md`: the day's entry, newest first.
- ⭐ **Hand off to the opt-in pack** (checklist 68, the owner's stated next
  priority). Its first session reads **that repo's own STATE** and its standing
  pre-upload obligation, `reports/PARKED_OPTIN_REFERENCES.md` — ~46 parked
  passages that restore only when that mod launches, several of them in **this**
  repo and on the site. ⛔ Do not scope that effort here.

## 5 · ⛔ What you may not claim

- ⛔ That anything is published unless the owner said so **in their own words**.
- ⛔ An md5, byte count or entry count you did not compute.
- ⛔ That the store page looks right — you cannot see it.
- ⛔ Any count you did not emit with `doccheck --emit-counts`.
- ⚠️ ⛔ **Do not report the launch as finished while Steam is undecided.** Name
  what is live and what is not, by portal.

## 6 · Close-out

One commit (or two, if Steam follows later): the writeback with its restored
comments · sheet updates · STATE · checklist · SESSION_LOG · `doccheck` GREEN ·
`git rm` this file · push.

**Owner report:** what is live and where · the ids now in `metadata.lua` · what
`version` reads and why · §0.5(d)/(f) outcomes · 37 Q2 if open · the opt-in
kickoff line.
