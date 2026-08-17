# C·02 — build only what 01 approved · UNATTENDED

Read `README.md`, then `STATE.md`, then `FIX_POLICY.md` §3a, then this, then
`## Notes from upstream` — 01 writes the approved spec there.

## 0 · Staleness check
```
git log --oneline -10
git pull
```
⛔ **Do not build anything 01 did not approve**, and do not revive anything it
declined. If 01 routed a decision to the owner and the owner has not answered,
build only the unblocked items.

## 1 · 🗒 Live todo list from your first action — one item per approved defect.

## 2 · Job 1 — re-verify the route, even though the design is settled

`CHAIN_METHOD` §2.3: **"do not re-derive the design" never means "do not verify
the route."** Every route failure in this project sat above individually-correct
citations. Before writing a line, confirm at `ModTools\Src` by symbol that each
approved target is still where the spec says.

⛔ If a target has moved, **stop** — the spec's shape may survive but its detail
did not, and that is exactly the failure mode `CHAIN_METHOD` §3 names.

## 3 · Job 2 — build

Per module, non-negotiable (`FIX_POLICY` §3a): self-check in `apply()` returning
a **reason string, never erroring**; restore-on-disable that preserves a later
third-party wrapper; no saved object, timer or marker; a TestKit probe; parse
sweep before any commit touching Lua.

**If a §1.5 replacement was approved:**
- capture the vanilla body **byte-verified** against `Packs\Lua.fpk`, not just
  `Src` (`WORKFLOW` fpk discipline — the pack's ~29 replacements are its
  patch-rot exposure)
- the self-check must detect a changed target and stand down cleanly rather than
  running a stale copy
- add it to the fpk re-verification list in the same commit

**If the hyperlink re-enable was approved:** it is *re-enable and observe*. Wire
the falsifier so 03 can actually run it — if XText misbehaves, the module must be
disable-able without a restart.

## 4 · Job 3 — write the sitting
Fill in `03_SITTING_owner.md`: which browser screens, which mod to open (**one
with screenshots**, or the check is vacuous), what correct looks like, and what
the failure signature would be. Order it decider-first. **Re-confirm the fixture
exists at handover time**, not at authoring time.

## 5 · Scope fence
**IN:** the approved modules, their probes, the sitting script.
**OUT:** ⛔ anything 01 declined · ⛔ formatting, fonts, caching policy, or any
capability the vanilla path did not already have · ⛔ chains B and D · ⛔ owner
time.

## 6 · Stop conditions
- A target moved → stop, route back.
- The re-enable cannot be made revertible at runtime → **do not ship it**; the
  falsifier is not optional.
- Suite or gate reads wrong at run top → STOP; do not bank readings about code
  that did not execute.

## 7 · ⛔ What may not be claimed
- ⛔ **`tested-unattended`.** Every one of these is a screen event; that word is
  closed to screen events.
- ⛔ **"Screenshots now download."** You can show the concat is repaired and the
  downloader is reached. Whether an image lands and renders is 03's, with eyes.
- ⛔ **"Links are clickable."** Same boundary.
- ⛔ **"No XText regression."** Absence of a crash in your run is not absence of
  the fault the comment may have been hiding.

## 8 · Close-out
One commit: modules + probes + `C52` updated · `03_SITTING_owner.md` filled in ·
the sitting on the **checklist** (R10) · counts re-emitted by the tool · fpk list
updated if a §1.5 shipped · manifest row struck · `git rm` this file · doccheck
GREEN · grave named · push.

## Notes from upstream
