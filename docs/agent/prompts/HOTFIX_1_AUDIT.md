# HOTFIX 1 — AUDIT (link 2 of 2, TERMINAL; link 1 was `HOTFIX_1_APPLY.md`)

Paste into a **fresh** Claude Code session that did NOT do the implementation.
**Start with `git log --oneline -15` + `git pull`.** Read `docs/agent/STATE.md`
(mandatory), `docs/agent/FIX_POLICY.md`, and `bugs/F111`–`F116`.

> 🎯 **YOU ARE THE GATE. Your verdict decides whether the owner uploads.**
> ⛔ You do not fix, you do not upload, you do not open the Mod Editor. You
> **audit, and you are allowed — expected — to say NO.**
>
> ⚖️ **The standing rule, and it points at US now:** a "Fixed" claim is FALSE
> UNTIL CONFIRMED. Every sentence the apply link wrote is a claim, including its
> measurements. ⭐ **This project has been wrong in BOTH directions in one week**
> — a desk audit said 6 self-disabled modules and the game measured 13; a sweep
> called every train module "clean" and two live P1s were sitting in them.

## 0 · Why this patch exists, in one paragraph you must not take on trust

Game 1.1.0 + the first DLC shipped 2026-09-08. Two of our own fixes broke
**visibly in players' games**: `F114` (trains never move between stations — 157
throws in a 42-minute session) and `F115` (landscaping raises the engine's
mod-error dialog naming our pack). Three more were gated or guarded from a
source read (`F111`, `F112`, `F113`). ⛔ **The pack's self-checks did not catch
any of it**, because they ask whether the target still EXISTS. That is the
defect behind the defects, and it is the thing you are auditing.

## 1 · The five changes under audit

Everything since live tree `version` **5**:

| file | defect | shape |
|---|---|---|
| `Fix_LanderCargoRatchet.lua` | F113 | gate (`{class, method}` on a deleted method) |
| `Fix_ExtractorStaffedPerformance.lua` | F111 | **guard, not a gate** — a `type()` test inside the body |
| `Fix_AutomationLawCompensation.lua` | F112 | gate (`test` content check, deliberately NOT named in the dialog) |
| `Fix_TrainCargoDumping.lua` | F114 | gate (`MultiResourceDepotBase` exists ⇒ decline) |
| `Fix_LandscapeUnitFilter.lua` | F115 | gate (added by the apply link) |
| `00_Core.lua` | — | ⛔ **UNCHANGED from shipped v5.** The +151-line override surface was reverted per owner ruling 110; verify that in §2c. |

## 2 · What you must actually do (not a checklist to tick — findings to produce)

### 2a · Re-derive every gate's ROUTE, not its citations

⛔ **`EF-081`/the recorded-facts lesson binds hardest here:** the project has
twice inherited a cited line, re-checked the citation, stamped it verified, and
been wrong — because the citation was right and the ROUTE was not. For each of
the five: open the shipped 1.1.0 source yourself and answer **"does this
discriminator actually separate 1.1.0 from 1.0.7, and does the module decline on
the tree the owner is running?"**

Specific traps already known:
- **F115's discriminator** may be a `MapVars` membership test. ⚠️ Is `MapVars`
  populated at MOD LOAD time? If not the module declines always — safe, but dead
  on 1.0.7 forever, and the apply link was told to verify it and may not have.
- **F112 is a `test` content check and is inactive but NOT named in the dialog.**
  That is correct by design (`00_Core` exempts content checks from
  `update_suspect`). ⛔ Do not "fix" it into the dialog.
- **F111 is a GUARD, not a gate** — the module still applies and runs a patched
  body on 1.1.0. It is the only change here that leaves our code live. Give it
  the hardest look: `type(self.overtime) == "table"` must be correct on BOTH
  shapes, and the module's own header admits an assumption it could not verify
  because the 1.0.7 tree is gone (`EF-075`).

### 2b · Reconcile the boot log against the prediction

The apply link predicted **17 inactive / 14 named**, zero
`Fix_TrainCargoDumping.lua:89`, zero `Fix_LandscapeUnitFilter.lua:63`.
⛔ **A difference is a FINDING, not a nuisance.** Run
`python tools/logscan.py --build 6a91a190` over every 1.1.0 log and read the
errors verbatim. ⚠️ Confirm the log you are reading was copied **after
`Mars.exe` exited** — mid-session copies produced a wrong count twice on
2026-09-08 (a "1" that was 6; a "30" that was 157).

### 2c · Verify decision 110 was actioned cleanly

⚖️ **Owner ruled 2026-09-08: the override surface does NOT ship — "that's a
diagnostic tool only."** `Code/00_Core.lua` was reverted to `ce77162` (the
shipped v5 file) and the mechanism moved wholly into the Test Kit's
`Code/97_ForceInactive.lua`.

⛔ **Verify, do not assume:**
- `Code/00_Core.lua` is byte-identical to the shipped v5 file. `git diff` it
  against the last commit that touched it before 2026-08-30.
- The pack's diff vs live v5 contains **only** the five gate/guard files.
- The Test Kit replacement actually works from outside — it swaps
  `SMRFixPack.Require` around a re-apply and replicates `run_apply`'s verdict
  handling **by hand**. ⚠️ That hand-copy can drift from `00_Core`. Check it
  matches, and say so if it does not.
- ⚠️ The Test Kit is NOT in the shipped artifact, so a bug there cannot reach a
  player — weigh your effort accordingly and do not spend the patch's time on it.

### 2d · Audit the PATCH NOTES as hard as the code

`metadata.lua`'s `last_changes` is a player surface and it is where an
overclaim would do real damage.
- ⛔ Must NOT imply the pack is verified on 1.1.0. **17 of 22 full-body
  replacements are still undiffed**, and NO instrument we own bounds body
  divergence — the name sweep sees names, `tools/sigcheck.py` sees arity, the
  runtime self-checks see existence, and **F114 was invisible to all three until
  a player reported it.**
- ⛔ Never name fredware's mod on a player surface (`EF-054`, `FIX_POLICY` §8).
  No load-order advice.
- ⛔ No save-safety claim for 1.1.0 — uninstall safety (PT-20) was verified on
  1.0.7 only.
- ⚠️ **Route-check every "you can X"**: the project overturned a line three
  reviews had passed because nobody walked the steps a real player would.

### 2e · The one thing nobody has done, and you must decide whether it blocks

**17 of the 22 full-body replacements have never been diffed against 1.1.0.**
Five were: `TrainCargoDumping` (F114, broken), `LandscapeUnitFilter` (F115,
broken), `TrackSalvageWipe` (F116, source-read finding), `TrackSalvageRefund`
(clean), `TrackConnectorPingPong` (clean). **That is a 3-in-5 hit rate on the
only subset anyone has checked.**

⇒ **Ask yourself plainly: is it responsible to ship a "safety" hotfix while 17
untested copies of that same shape remain?** There is a real answer either way —
the two known-visible breakages are fixed now and players are hitting them
today; against that, the next player report may already be in the queue.
**State your position and your reasoning.** The remaining 17 are a bounded,
mechanical job (one body diff each against `ModTools\Src`). If you judge the
patch should ship first, say what the follow-up commitment is.

## 3 · Bindings

- ⛔ `Mars.exe` must not be running before any loadable-code edit — but **you
  should not be editing code at all**; report instead.
- ⛔ `H-02` no Mod Editor, no `version` edit, **no upload**. `H-03` no portal API
  from a launched game — the first call CREATES the listing.
- ⛔ `H-04` never call a future release ready, and never treat "published" as
  covering anything the owner has not done.
- ⛔ `H-08` never pull a junction · `H-09` never stage a packed folder beside one.
- ⛔ Never modify the game directory. ⛔ Never "correct" a 1.0.7 citation
  (`EF-075`).
- `python tools/doccheck.py` GREEN before any doc commit; a WARN is copied
  **verbatim** into your summary. `STATE.md` is byte-capped — additions need an
  eviction in the same commit.
- ⛔ **Never silently discount a log line.** "Not caused by our leg" is an
  attribution verdict, not a dismissal — report unexplained lines verbatim with
  their age. Every pushback the project has had on this found a real defect.

## 4 · Your deliverable

A report at `agent/reports/HOTFIX_1_AUDIT.md` with, in this order:

1. **VERDICT: SHIP / SHIP WITH CHANGES / DO NOT SHIP.** One line, first line.
2. **Findings**, most severe first, each with: the file and line, what is wrong,
   how you know (the route you re-derived, not the citation you inherited), and
   what it costs a player.
3. **What you verified and what you could NOT** — explicitly. ⛔ A thing you did
   not check is not a thing that passed. Name the gaps.
4. **Decision 110** ruled, with reasoning.
5. **Your position on 2e**, with reasoning.
6. Anything for `PLAYTEST_CHECKLIST.md` → "Decisions waiting on you".

Then: `doccheck` GREEN → commit → **push** → hand back to the owner.

⛔ **Do not soften a real finding to avoid delaying the patch, and do not
manufacture one to look thorough.** If it should ship, say so plainly — a clean
audit that says SHIP is a real result, and the owner's time is the scarce
resource here. If it should not, say that just as plainly and say exactly what
would change your mind.
