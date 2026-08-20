# Close-out chain — `C50` + `C51` ship IN 1.0.0, then the launch

**Owner ruling, 2026-08-20**, reversing the earlier "build after launch":

> *"C50-C51 we are going to close out and launch. With basic testing. One chain to
> do both, with a testing chain right before the fable audit. It will wrap
> everything up cleanly. Part of the reason I am doing this, is because I don't
> want to upload and move right into 1.0.1 work. I would rather shift resources
> and start working on the opt in. Get this closed until we have reports,
> problems or a new patch lands."*

⇒ **The point of this chain is not the two fixes. It is that after it, this
repo is DONE** — no queued 1.0.1, nothing owed but a reaction to player reports,
a real problem, or a game patch. The next effort is the **opt-in pack**.

⛔ **`C52` is FROZEN** (same ruling). Not in scope, not to be opened.

## The manifest

| # | file | model | owner needed? | what it drains |
|---|---|---|---|---|
| 1 | `01_BUILD_C51.md` | volume tier | no | the localization repair — 3 strings, verified ids |
| 2 | `02_BUILD_C50.md` | volume tier | no | the SpaceY bullet — route C, borrowed id |
| 3 | `03_SURFACES.md` | volume tier | no | player-facing pages, counts, release-sheet refresh |
| 4 | `04_TEST.md` | volume tier | ⭐ **YES — one attended sitting, ~30 min** | the only evidence either fix works |
| 5 | `05_AUDIT_fable.md` | ⭐ top tier | no | adversarial backward QA, the tag move, the verdict |

**5 prompts ⇒ model placement is the owner's own call** (`CHAIN_METHOD` §4.0).
The shape above is the house default: volume tier executes, top tier audits.

⭐ **The owner starts each link by hand.** Every link's closing report ends with
the next link's kickoff line; `05`'s ends with the opt-in kickoff.

## Binding rules for every link

1. **Staleness first:** `git log --oneline -15`, `git pull`, read
   `docs/agent/STATE.md`, then `python tools/doccheck.py --emit-counts`.
2. **Route-don't-drop.** Unsure, blocked, or the brief is wrong ⇒ **STOP AND
   ASK** on `docs/PLAYTEST_CHECKLIST.md`. Never silently narrow the job.
3. ⛔ **`metadata.lua`'s `version` NEVER MOVES.** It is `0` and renders 1.0.0
   (`H-02`). ⛔ **No Mod Editor save, ever** — every save runs
   `version = version + 1` (`Mod.lua:967`). The `code` list is edited **by hand**,
   exactly like the `image` field was.
4. ⛔ **`H-10` IS THIS CHAIN'S LIVE HAZARD.** A new `Code/*.lua` that is not in
   `items.lua` **ships absent**. Both build links add the module to `items.lua`
   AND to `metadata.lua`'s `code` list, same name, same order.
   `python tools/upload_preflight.py` proves the two lists agree — it is the
   automated guard and it must stay at 0 FAIL.
5. **Parse sweep before any commit touching Lua** — python + `luaparser`,
   `ast.parse(open(f, encoding='utf-8-sig').read())`, over every edited file.
6. `python tools/doccheck.py` GREEN before every commit; counts re-emitted with
   `--emit-counts`, **never hand-typed**. If STATE warns on bytes, relay the line
   verbatim to the owner (`agent/prompts/STATE_EVICTION.md`).
7. **Commit with `-F <file>`** (PowerShell 5.1 splits embedded quotes). Push.
8. ⛔ **Nothing publishes.** The first portal API call **creates the listing**
   (`H-03`). `DbgPackMod` and `tools/upload_preflight.py` are safe; the portals
   are the owner's hands only.
9. **Live todo list**, updated as each item lands — the owner reads it to decide
   whether to step in.
10. ♻️ **Self-consuming:** `git rm` your own prompt in your closing commit and
    name the grave in the message.
11. **`## Notes from upstream`** at the foot of each link — append what the next
    link needs; do not rewrite what a previous link wrote.

## What this chain must not do

⛔ Re-run the pre-launch sweep, run B, or any multi-day leg. The owner ruled the
gate **one-time** (checklist 57): a maintenance change owes an `items.lua` entry,
a boot log, and doccheck counts. ⛔ Do not price this work with `FIX_POLICY` §3a's
per-module cost. ⛔ Do not open `C52`, the 1.0.1 hardening queue, or the opt-in
repo (link 5 hands that off, it does not start it).

## The one structural fact every link must hold

⭐ **The release tag `fixpack-v1.0.0` currently marks bytes that were measured in
a running game** (run B, 10/10, packed). ⛔ **This chain invalidates that** — two
new modules change the shipping surface. The tag therefore **moves once, in link
5, after the audit**, exactly as the terminal audit moved it last time (`H-01`).
⛔ **No link before 5 touches the tag**, and link 5 moves it only if its verdict
is ship.

⚠️ The recorded artifact in STATE (`.fpk`, md5 `8dcb0692…`, 362,894 B, **80/80**)
**goes stale the moment link 1 commits.** Link 3 owns re-deriving the expected
shape (`tools/pack_predict.py` — it should read **82** files) and correcting every
place the old fingerprint is quoted, including `RELEASE_PORTAL_PREP.md` §0.5(f),
whose delivered-bytes check names that md5. The real new md5 exists only after
the owner packs at the upload sitting.
