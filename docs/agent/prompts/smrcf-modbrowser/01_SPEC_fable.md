# C·01 — the spec · decide what may be built, and route what is not ours

**This prompt exists because a wrong call here poisons every build downstream.**
Read `README.md`, then `STATE.md`, then `FIX_POLICY.md` (§3a, §4, §365-368),
then this.

## 0 · Staleness check
```
git log --oneline -10
git pull
```
⛔ **Gated on chain A job 2.** Without the `AsyncPopsDownloadFile` answer,
defect 1 cannot be specced. If A is unconsumed, **stop and say so.**

## 1 · 🗒 Live todo list from your first action — one item per defect.

## 2 · Job 1 — re-derive all three, adversarially

Do not inherit `C52`'s citations, including the ones this brief repeats. Derive
at `ModTools\Src` by symbol, and for each defect answer:

- **Is the tell real?** Name it: (1) player harm, (2) dead code / discarded
  value, (3) sibling contradiction, (4) self-contradiction, (5) dev comment.
- **Is it reachable, and by what player action?** Enumerate call sites, eliminate
  the ones that cannot execute, name the route for each survivor. Record the
  tier: R1 · R2 · R3 · R4 · U.
- **What is the minimal repair**, and does it stay inside §1.1–§1.4, or does it
  need §1.5?

⚠️ `C52` was **already corrected once** — defect 2 was first closed as *"a
deliberate deactivation, not a defect"* and that was wrong. The owner's
distinction is what broke it: **a design choice and a planned-but-deferred fix
are different things.** Hold that distinction; it cuts both ways, and defect 3 is
where it might cut the other way.

## 3 · Job 2 — the decision each defect needs

**Defect 1 (screenshots).** Two gates: does `AsyncPopsDownloadFile` exist
(chain A), and is a **§1.5 full replacement** of a 63-line function acceptable
here? `FIX_POLICY` §365-366 requires an explicit user decision for a §1.5 on an
R3; this is R1/R2, so the letter does not bind — but the *reason* does, and the
pack's ~29 existing full replacements are its patch-rot exposure.
⇒ **Package this as an owner decision with a recommendation**, per
`CHAIN_METHOD` §4.3, optionally with provisional go-ahead ("build, not locked,
the audit reviews it").

**Defect 2 (hyperlinks).** The repair is to stop suppressing a path the engine
already supports. Specify it as **re-enable and observe**, with a named
falsifier: *if XText misbehaves in any observed state, revert and record.*
⛔ Do not specify a font cascade, a formatter, or anything fredware's §5N
contains. That is reimplementation.

**Defect 3 (thumbnail cache).** Decide honestly whether it clears §4 at all. No
dev comment, no sibling, and "cache keyed on version" is a defensible
simplification. **A behaviour found intentional is tier I: record it, close it,
write no fix.** Declining this is a full, successful outcome.

## 4 · Job 3 — write the build brief and the sitting

Fill in `02_BUILD_opus.md` with only what survived, and `03_SITTING_owner.md`
with what the owner must actually look at. **Tag every spec detail with
provenance** — `CHAIN_METHOD` §3: *specs are authoritative on design, unreliable
on detail*; 7 of the prompt-7-era specs had a defective supporting detail while
all 7 shapes survived. Say plainly in the build brief: **re-verify the route even
though the design is settled.**

## 5 · Scope fence
**IN:** derivation, tiering, minimal-repair specs, the owner decision package,
filling in 02 and 03.
**OUT:** ⛔ writing fix code · ⛔ launching the game · ⛔ any of chain B's or D's
subjects · ⛔ anything resembling fredware's formatter.

## 6 · Stop conditions
- `AsyncPopsDownloadFile` absent → defect 1 is **not buildable**; record and drop.
- A defect turns out tier I or R4 → **decline it in writing.** A reasoned
  rejection is a successful outcome for that item.
- All three decline → the chain ends here; hand `04_AUDIT` the reduced form and
  delete 02 and 03. **That is the gate working.**

## 7 · ⛔ What may not be claimed
- ⛔ **A defect is real because the sweep said so.** The sweep is upstream and
  was wrong once already, in this exact entry.
- ⛔ **"Minimal repair"** for anything that adds capability rather than restoring
  it.
- ⛔ **Any reachability tier without the enumeration behind it.** An unenumerated
  R1 is exactly as unproven as an unstated R4, and more dangerous.
- ⛔ Provenance per row; ROUTE tagged separately from citations.

## 8 · Close-out
One commit: `C52` updated with the three tiers and dispositions · owner decision
package **on the checklist** (R10) · 02 and 03 filled in or deleted · manifest
row struck · `git rm` this file · doccheck GREEN · grave named · push.

## Notes from upstream
