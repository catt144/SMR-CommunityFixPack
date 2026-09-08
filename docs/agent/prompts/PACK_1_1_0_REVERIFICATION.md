# PACK-WIDE 1.1.0 RE-VERIFICATION — what to FIX, REMOVE, or AUGMENT

Paste into a fresh Claude Code session. Written **2026-09-08** by the session
that found `F115`/`F116` and built `sigcheck.py`/`logscan.py`.
**Start with `git log --oneline -10` + `git pull`.** Read `docs/agent/STATE.md`
(mandatory), `docs/agent/FIX_POLICY.md`, `docs/agent/WORKFLOW.md`.

> 🎯 **ONE JOB: go through the whole pack against game 1.1.0 and produce a
> prioritised list of what must be FIXED, what should be REMOVED, and what needs
> its self-check AUGMENTED — with evidence for each.**
>
> ⛔ **YOU WRITE NO CODE.** This is an audit. You do not edit `Code/`, you do not
> gate, you do not repair, you do not upload, you do not open the Mod Editor.
> ⭐ **At the END you may OFFER to write fix prompts. Do not write them unless
> the owner asks** — that is their call, not yours.

## 0 · Why this exists, and the one lesson that governs it

Game 1.1.0 + the first DLC landed 2026-09-08. Within hours the pack produced
**two player-visible P1s**, and every instrument the project owned missed both:

| instrument | what it checks | why it missed |
|---|---|---|
| the modules' own `Require` self-checks | does the target **exist** | `F114`/`F115` targets still exist |
| the 1.1.0 call-site sweep | 106 global **names**, 174 method **names** | a name survives a signature change |
| `tools/sigcheck.py` (written after) | replacement **arity** | `F114` was a BODY change at matching arity |

`F114` was found by a **player report**. `F115` by the owner **hitting a button**.
`F116` by someone finally diffing a body by hand.

⚖️ **THE RULE: check the THING, not its LABEL.** This project has now been burned
by label-checking three times in one week — `EF-078` (path specs verified by
their last segment's name), the name sweep, and `F116` (filed off a `grep -c`
whose count was right and whose inference was wrong, by its own author). ⛔ **If
your method is "grep for a name and see if it's there," you are repeating the
failure this audit exists to end.**

## 1 · What is ALREADY DONE — do not redo, do not re-derive

⛔ Read these; they are the pattern and the precedent:

- **`F111`** `Fix_ExtractorStaffedPerformance` — **guard** (`type(self.overtime) == "table"`; 1.1.0 collapses it to a boolean). ⚠️ The only one of the six that leaves our code LIVE on 1.1.0.
- **`F112`** `Fix_AutomationLawCompensation` — gate via a `test` CONTENT check. Correctly inactive and correctly NOT named in the dialog.
- **`F113`** `Fix_LanderCargoRatchet` — gate on a deleted method.
- **`F114`** `Fix_TrainCargoDumping` — gate; body divergence at matching arity. **MEASURED: 157 throws in a 42-minute session.**
- **`F115`** `Fix_LandscapeUnitFilter` — gate; SIGNATURE change (`(mark, callback, ...)` → `(map, mark, callback, ...)`). **MEASURED.**
- **`F116`** `Fix_TrackSalvageWipe` — handled by its own leg; read its final state, do not reopen it.
- **Cleared:** `Fix_TrackSalvageRefund`, `Fix_TrackConnectorPingPong`.

**Measured baseline:** the gated 1.1.0 boot reads **17 inactive / 14 named, 0
errors** (`archive/logs/` — use the newest gated boot log). `EF-078`'s 13/11 is
the pre-gate baseline and is SUPERSEDED. Facts `EF-078`–`EF-081`+.

**Tools, use them rather than hand-rolling:**
- `python tools/sigcheck.py --src "A:\SteamLibrary\steamapps\common\Project Spark\ModTools\Src"` — replacement arity vs shipped. ⛔ An `OK` is NOT a clearance.
- `python tools/logscan.py --build 6a91a190` — every 1.1.0 log, errors verbatim.
- `python tools/doccheck.py --emit-counts` — never hand-type a count.

⛔ **The 1.0.7 tree is GONE from disk (`EF-075`).** You cannot diff against it.
Any claim of the form "1.1.0 changed X" needs support that is not a 1.0.7
comparison. Our module headers cite 1.0.7 lines — those are **claims**, not
references you can open.

## 2 · The three buckets — every module lands in exactly one

For each module you examine, decide and record:

- **FIX** — it is broken or will break on 1.1.0. Say gate or repair, and why.
- **REMOVE** — ⭐ **the bucket nobody has used, and it matters.** The defect is
  gone: 1.1.0 repaired it, or the feature/target no longer exists. A module that
  fixes nothing is **pure risk with zero benefit** — it can still misfire, and it
  is one more body to re-verify every patch. ⚠️ Seed example:
  `LastTransmissionStorage` latches *"the shipped presets are already correct"* —
  that is 1.1.0 having fixed it, i.e. a REMOVE candidate, not a healthy latch.
  ⛔ REMOVE needs the same evidence bar as FIX. "It's inactive" is not evidence
  the defect is gone — it may be a broken self-check.
- **AUGMENT** — the fix still works, but its self-check cannot see the failure
  mode that actually bit us. ⇒ what should the check test instead?
- **KEEP** — verified fine. ⛔ Only with a stated reason; silence is not a pass.

## 3 · Passes, in value order. CHECKPOINT AFTER EACH ONE.

⚠️ **This is bigger than one session.** Commit and push after every pass so the
work survives, and if you run low on budget **stop and write a handoff prompt**
naming exactly which modules are done and which are not (`CHAIN_METHOD.md`).
⛔ Never leave a half-finished pass uncommitted.

### Pass 1 — the 17 undiffed full-body replacements (**highest value, start here**)

~21 modules declare a full-body replacement; **5 have been diffed and 3 of those
5 were defective.** A 3-in-5 hit rate is the single best reason this audit
exists. Derive the current list yourself (`grep -rln 'full replacement\|fully
replaces\|a copy of' Code/Fix_*.lua`), subtract the 5 already done, and **diff
each remaining body against the shipped 1.1.0 function.**

For each: extract both bodies, diff them properly (⛔ **not** keyword counts —
that is exactly how `F116` was mis-filed), and answer:
1. Does the shipped function still exist, and with what signature?
2. What did 1.1.0 add, remove, or change inside it?
3. Does our copy's behaviour still make sense against that?
4. Is the ORIGINAL defect still present in 1.1.0? **If not → REMOVE.**

### Pass 2 — the 17 modules that self-disable on 1.1.0

From the gated boot log. For each, the check nobody has run: **is the
self-disable CORRECT?**
- Target genuinely **gone** ⇒ is the defect gone too? (REMOVE) or is the fix
  still wanted and merely unreachable? (record it; a later patch may re-arm it)
- Target **renamed or moved**, not deleted ⇒ the module is a **false negative**:
  it could still work. ⭐ **Nobody has checked this for any of them**, and
  `EF-078` showed the project guesses this badly.
- Latched *"already correct"* ⇒ almost certainly **REMOVE**.

### Pass 3 — wrappers, `SetGlobal`, and `DataPatch` sites

The ~15 `SetGlobal` sites and ~9 `DataPatch` modules are NOT covered by
`sigcheck.py`, and wrappers have their own failure mode: the wrapped function
still exists and still takes the same arguments, but its **semantics** changed —
a post-wrapper that "corrects" a value 1.1.0 now computes differently is a
silent gameplay bug with no throw. ⛔ `F111` is exactly this shape and is the
only live-code change we shipped; give it a second, independent look.

### Pass 4 — the meta-defect: the self-check design itself

⭐ **This may be the most valuable output of the whole audit.** The self-checks
answer *"does the target exist?"* and cannot answer *"is the target still what
we assumed?"* — which is what actually broke. `00_Core`'s own header admits this
("HONESTY LIMIT"). Recommend concretely:
- What could a `Require` spec cheaply test that would have caught `F114` or
  `F115`? (⚠️ `debug.getinfo` is absent in the mod sandbox — a real constraint.)
- Should full-body replacements carry a **content fingerprint** of the body they
  were copied from, checked at load?
- Should the pack prefer wrapping over replacement as policy? What does that
  cost? ⛔ Some defects are mid-function and cannot be wrapped (`F115`'s was).
- What belongs in `tools/`, so the next game update is a tool run and not a
  week of player reports?

## 4 · Bindings

- ⛔ **Read-only on `Code/`.** If you find something urgent, WRITE IT UP and tell
  the owner; do not fix it. ⚠️ Other sessions may be editing `Code/` — check
  `git log` and `ListAgents` before assuming a file is idle.
- ⛔ `H-02` no Mod Editor, no `version` edit, **no upload**. `H-03` no portal API
  from a launched game. `H-04` never call a future release ready.
- ⛔ Never modify the game directory; never "correct" a 1.0.7 citation.
- ⛔ **Never move a status you did not witness.** A source read is never
  `tested`. `tested-attended` needs an attended witness.
- ⛔ **Never silently discount a log line** — "not caused by our leg" is an
  attribution verdict, not a dismissal.
- `doccheck` GREEN before any doc commit; a WARN goes **verbatim** into your
  summary. `STATE.md` is byte-capped — additions need an eviction in the same
  commit. Commits `git commit -F <file>`, then push.
- ⛔ **Do not price this as a release gate.** The gate was ONE-TIME, not a
  per-change tax (owner 08-20, ck57). This is an audit; it produces findings,
  not a re-certification.

## 5 · Deliverable

`agent/reports/PACK_1_1_0_REVERIFICATION.md`:

1. **The four buckets as tables** — FIX / REMOVE / AUGMENT / KEEP, every module
   accounted for, each row with its evidence and the file:line behind it.
2. **Ranked recommendations** — most severe first, each with what a player
   actually experiences and what it costs to act.
3. ⛔ **What you did NOT check, named explicitly.** A module you did not open is
   not a module that passed. This section is as important as the findings; the
   project's habit of treating silence as a pass is what let `F114` ship.
4. **Pass 4's design recommendation** for the self-checks and the tooling.
5. Anything for `PLAYTEST_CHECKLIST.md` → "Decisions waiting on you".
6. **A one-line offer**: which fix prompts you would write if the owner asks.
   ⛔ Do not write them unprompted.

⛔ **Do not inflate the list to look thorough, and do not trim it to look
reassuring.** "This module is fine and here is why" is a real result. So is
"31 modules need work" — if that is what the evidence says, say it.
