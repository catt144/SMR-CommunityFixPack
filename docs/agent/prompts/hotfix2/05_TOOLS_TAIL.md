# 05 · Tools tail — make the next update a tool run, not a week

Chain: `prompts/hotfix2/README.md` (its binding rules are yours). Needs 01 only;
independent of 02, 03, 04 — run it whenever. Small, low-risk, and it lands in
**this** patch cycle rather than after it (owner acceptance, ck116).

## 0 · Start

`git log --oneline -10` · `git pull` · `ListAgents`. Todo list first.

**Read path:** `PACK_1_1_0_REVERIFICATION.md` §1c (the AUGMENT rows) and §4
items 4–5 · `tools/sigcheck.py` · `tools/logscan.py` · `Code/00_Core.lua`
`:99-165` · `archive/logs/gated110_Mars.exe-20260908-17.51.09-6a91a190.log`
(the canonical boot log you test against) · your inbox.

## 1 · A-4 — `sigcheck.py` over `SetGlobal` sites

`sigcheck.py` reads `function Name(...)` definitions only. The pack has **15
`SetGlobal` sites** and anonymous function literals that it cannot see at all.
Extend it to resolve the local named in `SetGlobal("Name", <expr>)` and check
that function's signature like any other.

⚠️ Remember what `sigcheck` is and stays: an **arity** bound. It never clears a
body. Do not let the extension's wording imply otherwise — that implication is
how F114 shipped.

## 2 · A-3 — `logscan.py` counts heals

"Last verdict wins" misses a `DataPatch` heal. `SaintBlessing` logs `inactive` at
`:166`, then `corrected …` at `:186`, and **ends the boot ACTIVE**. So the
headline "17 inactive" is really **16**, and the module that was actively
breaking the Saint blessing was hiding inside the number that was supposed to
reassure us.

Make `logscan.py` heal-aware: a module that logs a later `corrected`/applied line
ends ACTIVE regardless of an earlier `inactive`. Re-run it against the canonical
log and report the corrected census.

⛔ **Verify against the archived log, not a fresh one.** A log copied while
`Mars.exe` is running is a PARTIAL log and has already cost this project two
wrong counts.

## 3 · A-2 — the benign latch is a RETIRE signal

Today a `DataPatch` pass that finds data "already correct" is filed as HEALTHY.
R-13 (`LastTransmissionStorage`) shows that is exactly backwards: **it is the
REMOVE signal.** The pack had no bucket for "vanilla fixed it", which is why 32
modules survived an audit they should not have.

- Rename it in the boot log: `inactive (already correct — RETIRE candidate)`.
- Have `logscan.py` list benign latches as retire candidates.
- Have `bodycheck.py`'s `DEFECT-GONE` output feed the same bucket, so the two
  instruments agree on one list.

## 4 · A-1 — `GeneForging` reads the legacy map

The module works (K-4) but reads `TechDef.GeneForging.param1` — the **legacy stub
map**. Prefer `Techs.GeneForging:ResolveValue("param1")`.

⚠️ This is the one code change in this prompt. It is a KEEP module, so it already
carries 01's `SRC:`/`DEFECT:` manifest — **re-stamp it after the edit**, and run
`bodycheck.py` before and after so the change is visible to the instrument.

## 5 · Scope fence

**In:** `tools/sigcheck.py`, `tools/logscan.py`, `Fix_GeneForging.lua`, and the
log-line wording in `00_Core.lua` **if and only if** the rename requires it —
if it does, keep that diff to the string alone.
**Out:** `bodycheck.py` (01 owns it — extend only its *output consumption* here,
not the tool); every other module; `items.lua`; store text.
Found something out of fence? **File it, do not fix it.**

## 6 · Stop conditions

- The heal-aware change would alter a count this project has already published
  or cited ⇒ report the delta explicitly rather than quietly correcting it. A
  silently-corrected number is destroyed evidence (chain rule 5).
- The `00_Core.lua` log-string rename turns out to touch control flow ⇒ **STOP
  AND ASK.** That file is not yours to improvise in.

## 7 · What may NOT be claimed

- ⛔ Not "the tooling now catches game updates". It catches classes a, b, d, e.
  Class c — semantics moving under a wrapper — is still seen by nothing, and 6 of
  the 10 FIX rows this audit were class c.
- ⛔ Not "the log census is verified" beyond the one archived boot log you ran
  against.
- ⛔ No status moves.

## 8 · Close-out

Green gates. Outbox to `06` (if any wording changes) and `99` — 99 needs the
corrected census number and what changed to produce it. Strike your README row,
`git rm` this file, commit together, push.

## Notes from upstream

*(From the authoring session, `smr-bugfixpack-91`, 2026-09-08.)*

- `tools/logscan.py --build <id>` is the safe read; a hand-rolled grep
  undercounted throws 30 vs 157 on 2026-09-08 because the engine writes the
  `[LUA ERROR]` header in two forms and only one carries the file path.
