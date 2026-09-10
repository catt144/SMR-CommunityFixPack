# SELFCHECK PROMISE — COMBINED FINDINGS (Claude audit + Codex cross-check, reconciled 2026-09-09)

**This is the read path.** It supersedes, as the thing to cite, both
`reports/SELFCHECK_PROMISE_AUDIT.md` (Claude, `smr-bugfixpack-db`, with its
§10 corrections) and `reports/SELFCHECK_PROMISE_CROSSCHECK_CODEX.md` (Codex,
`397bf15`). Both originals are kept unedited as the record of what each
claimed and why; where they disagree, this document states the reconciled
position and the evidence that settled it. Reconciled by the Claude session
after re-verifying every Codex refutation against the two game trees and the
archived logs. ⛔ Nothing in either report ran in a game.

---

## 1 · Verdict, reconciled

**YES BUT SCOPED — and the scope, the preconditions and the cost are now all
different from the first audit's.**

The store sentence — *"Every fix checks the game's code before it touches
anything, and stands down by itself if an official patch changes what it was
written for. A fix that stands down does nothing at all — it never guesses."* —
can be made literally true with this scope and these preconditions, and not
otherwise:

- **Scope:** "changes **the code it patches or declares it depends on**". Not
  "what it was written for" in the broad reading. The one module the first
  audit called invisible (`StaleReservations`, F-2) turned out to be visible
  through a callee it already declares (§3, X1), so the known residue of
  changes no runtime check can see is, on the 1.1.0 patch, **zero modules that
  we know of** — but "that we know of" is the honest limit: unchanged code can
  still depend on unobserved state or C behaviour.
- **Precondition A — an install transaction.** "Before it touches anything"
  and "does nothing at all" require every check for every site of a module to
  run BEFORE any write; the pack's runner does not do that today (`run_apply`,
  `00_Core.lua:447`, has no rollback; `AnomalyCaveInMap` installs at `:99`
  before it can decline at `:120`).
- **Precondition B — UNKNOWN declines.** A missing dumper, an unfamiliar
  format, a mass mismatch: under an unconditional sentence each must stand
  the affected fix down, or the sentence must name the exception.
- **Precondition C — one runtime measurement.** Every mechanism below rests on
  `string.dump` being callable from mod code in the real engine. Desk replica
  and binary reads say yes; no boot has. The pilot (`prompts/SELFCHECK_PILOT.md`)
  measures it in one owner sitting.

What is NOT achievable and must be left out of any wording: a guarantee about
changes outside the declared code and data set, captured closure values,
C-side behaviour, or another mod overwriting our target after we checked it.

---

## 2 · The evidence ledger — what is measured, what is read

| evidence | class | who |
|---|---|---|
| Engine's own `ModEnvBlacklist` + `LuaModEnv` (Mod.lua 1.1.0 `:1280-1441`, `:1551-1627`) executed verbatim on stock Lua 5.3: `debug`/`io`/`load` nil, `string` real, `string.dump` a function | MEASURED (desk replica) | both, independently |
| `Mars.exe`: `unable to dump given function`, `Lua 5.3`, `(...tail calls...)`, `LUAC_DATA` magic present; `dump` in the string-library **registration pointer table** with `byte char dump find format gmatch gsub len lower match rep reverse sub upper pack packsize unpack` in stock order | MEASURED (binary) | Claude (strings), Codex (pointer table) |
| Stripped dumps: `numparams`/`is_vararg` at one-based `36 + 2*sizeof(int)`; line shifts change only `linedefined` fields; C functions refuse | MEASURED (desk) | both |
| Arity across the branches: exactly F115 differs (`(2,vararg)` → `(3,vararg)`), all 15 replacement sites match 1.1.0 | MEASURED (tools + Codex's independent extraction) | both |
| Body deltas across the branches: `bodycheck --src archive` 27 BODY-CHANGED + 1 TARGET-ABSENT over 24 modules (source hashes); Codex whole-chunk compile 27 differing prototypes over **25 modules, 7 FIX / 18 KEEP** | MEASURED (desk) | both |
| Bytecode flips on edits OUTSIDE the function: `Colonist.lua:13` `local ipairs = ipairs` (1.1.0 only) changes `FindTransportationModeToCommunity`'s compiled form with its text unchanged; `DroneControl.lua` gained 4 top-level locals above `UpdateRocketsInternal` (upvalue slot moved); closures with different captured values dump identically | MEASURED (desk), re-verified on both trees | Codex, confirmed by Claude |
| `Residence:CancelResidenceReservation` gained `unit.expedition_residence = false` on 1.1.0 (`:393`); `Fix_StaleReservations.lua:100` declares it, `:159` calls it | MEASURED (both trees) | Codex, confirmed |
| Two `Train:UnloadAll` bodies leave different access traces on an ORDINARY input (1.1.0 indexes `station.demand` twice, `Train.lua:794`) | MEASURED (desk) / READ | Codex / Claude |
| `LuaCodeToTuple(code, env)` (`CommonLua/Core/ToLuaCode.lua:390`) is not blacklisted and calls `load(..., env or _ENV)` in the engine's environment; C-side `ChecksumRemove` in front of it is unmeasured | READ + desk replica with the C gate stubbed | Codex, source confirmed by Claude |
| Archived blame lines: 4 lines, 3 sessions (one log archived twice as a 274-line prefix); the pack is named only where its own body threw; the act1 line names the Test Kit as CALLER of two vanilla throw sites (`LawDef-Welfare.lua:1892/:2026`, `ActiveLaws` false at the menu) | MEASURED (logs) | both; Claude's first explanation of act1 was wrong |
| Dedupe: F115 drew the 15:57 session's one blame line at `0:01:03`; F114's 157 throws from `0:25:42` drew none | MEASURED (log) | both |
| Box order = `GetLoadingQueue` dependency order (`Mod.lua:1907`), not strictly enable order; `os_paths` substitutes the OS path only if it exists | READ | Codex (corrects Claude) |
| Tail call removes the caller's frame (Lua 5.3 §3.3.7; desk traceback); engine `GetStack` rendering unmeasured | MEASURED (desk) / not in engine | both |
| Census: 44 modules; 5 probe (one runs in a deferred data pass, not at apply), 7 test, 35 neither; 3 no-`Require` + 1 DataPatch-only; 64 install sites = PRE-TAIL 15, PRE-NOTAIL 0, POST 13, REPLACE 15, HANDLER 17, DATA 4 | MEASURED (scripts; Codex executed all 44 chunks in a recording env) | both |
| `LuaRevision` is a plain engine global, not blacklisted, read at `Mod.lua:919` | READ | both |

---

## 3 · The claims that changed, and why (the reconciled table)

| # | first-audit claim | final state | settled by |
|---|---|---|---|
| X1 | F-2 is invisible to any runtime check (the "ceiling") | **REFUTED.** Its declared callee changed. A pin over the module's `Require` set catches it. | both trees |
| X2 | No 1.0.7-era probe could have caught F114 | **REFUTED for trace probes**, holds for output probes (the pack's five). A whole-access-trace comparison on an ordinary input distinguishes the bodies without foreseeing the input. Brittle, per-target. | source of both bodies |
| X3 | Bytecode false stand-downs ≤ 17 on 1.1.0; "source same + bytecode differs ⇒ recompiled" | **REFUTED.** 18 KEEP modules affected at least; lexical context outside the function flips hashes; captured values are invisible. The diagnosis needs calibration witnesses, not desk `bodycheck`. | both trees |
| X4 | act1 blame line = Test Kit `quit()` artefact | **REFUTED.** Two vanilla throw sites provoked by the kit's synthetic call; the kit was named as caller. Citation was to a different session. | the log |
| X5 | Arity check ≈ 40 lines in core, zero authoring | **UNDER-COSTED.** Zero authoring for the expected value only; needs an install API or per-site edits; 3 modules bypass `Require`; pins must be Lua literals. | code read |
| X6 | (not examined) "does nothing at all" | **NEW GAP.** Multi-site modules can decline on a later site with an earlier one installed. Install transaction required. | `00_Core.lua:447`, `Fix_AnomalyCaveInMap.lua:99-121` |
| X7 | Abstain on dumper/format/quorum surprises | **CONFLICTS with the wording.** UNKNOWN must decline, or the wording names it. Owner policy. | reasoning |
| X8 | "`load` is blacklisted, therefore no loading route" | **INCOMPLETE.** `LuaCodeToTuple` is an indirect route behind an unmeasured C gate. Not to build on; to know. | source |
| X9 | Box order = enable order; our `OnLuaError` handler could annotate | Corrected: dependency order; handler runs after the engine's and cannot alter the box. | source |
| — | `string.dump` reachable; arity flags exactly F115; 4 archive lines; dedupe; tail call; census; PRE-NOTAIL 0 | **HELD**, several strengthened by Codex's independent method. | |

---

## 4 · The mechanism, as it now stands (design, not code)

1. **Capability pilot** (one owner boot, Test Kit chunk): dumper present;
   full dump header; four arity controls decode; C function refuses; the
   `LuaCodeToTuple`/`ChecksumRemove` gate; `GetStack` on a tail call;
   `find_lower` semantics; whether an explicit `error()` unwinds under `pcall`
   in mod code (the kit records that it does not — `00_TestCore.lua:41-49` —
   which bears on every "a throw is a decline" rule). Exact chunks:
   `prompts/SELFCHECK_PILOT.md`.
2. **Install transaction in core**: a module hands `Register` a PLAN — the
   exact dependency references (every function it replaces, wraps, or
   declares it calls; every data node a `DataPatch` reads), the expected
   evidence for each, and the writes it intends. Core validates ALL before ANY
   write, re-checks identity at commit, and records a receipt (what was
   checked, what was installed, in which load phase). Deferred handlers and
   data passes carry their own phase checks. No rollback is needed if nothing
   is written before validation completes.
3. **Checks, in order of cost and certainty:**
   - **Arity**, self-describing: `numparams`/`is_vararg` of the shipped
     function versus our replacement's own dump. Zero pins. Catches the F115
     class; on 1.1.0 it flags exactly F115.
   - **Dependency pins**: exact normalised dump bytes (not FNV) of every
     function in the module's declared set, pinned from the engine itself
     (a pin collector that captures the ORIGINAL inside the owning module's
     apply, before install), stored as Lua literals. Catches the F114 class
     and F-2's callee. Cost: on a 1.1.0-size patch, ~25 modules stand down at
     first boot, 18 of them working — recoverable by a re-pin boot plus the
     upload the patch already needs.
   - **Calibration witnesses**: pack-local functions with known dumps
     (arity, nested closures, constants, varargs) compared first; if they
     differ the compiler or format changed and every pin is UNKNOWN.
   - **Data projections** for the three `DataPatch` modules: a canonical
     serialisation of the fields the pass reads, compared before the pass.
   - **Trace probes**, selectively, where a target's safe stub is already
     shown: the pack's existing probe form extended to record accesses.
4. **Policy:** UNKNOWN declines the affected module; the C1 dialog names the
   declined modules; a re-pin is a deliberate desk+boot act, never automatic.
   `LuaRevision` only ever as an observation label in the log, if the owner
   clarifies `FIX_POLICY` §2a to permit that narrow use.
5. **What it still cannot see, and the wording must not claim:** code outside
   the declared set, captured closure values, C behaviour, a later overwrite
   by another mod, and any semantic change that leaves every declared byte
   intact.

---

## 5 · Job two (being blamed for other mods' faults), reconciled

- Measured: zero misattributions of the pack in the archive; two in the field
  (F104, F105), both pass-through frames, both naming us alone; the act1 kit
  line is a "caller named" case, not a pack case.
- The engine names every mod whose content path appears in the error or the
  stack, once per mod per session, in dependency loading order. The dedupe
  hides our own later faults as well as un-naming us.
- Every pre-wrapper already tail-calls (PRE-NOTAIL 0). The remedy is a
  `FIX_POLICY` §2 rule for new wrappers. POST and REPLACE sites stay named,
  correctly. F104's call was mid-body; no tail-call rewrite could have helped.
- Recommended: a read-only `OnMsg.OnLuaError` breadcrumb logging the throw
  site and whether a pack frame is present — **it narrows triage and cannot
  acquit** (Codex's caution stands). No engine-box changes; no suppression; no
  catch-and-drop; no load-order advice to players. Console players still see
  only the box.

---

## 6 · Runtime reads owed — the pilot

Codex's R1–R5 (`SELFCHECK_PROMISE_CROSSCHECK_CODEX.md` → "Runtime reads still
owed") plus R0 (`error()` unwinding) are the measurement set; the pilot prompt
carries them adapted to the Test Kit's conventions and the decision table for
each outcome. The three most consequential outcomes: `NO_DUMPER` kills the
fingerprint route; a `ChecksumRemove` that passes arbitrary text means an
indirect `load` exists (a sandbox fact for the owner to decide what to do
with); a `GetStack` that prints a tail-called frame changes job two.

---

## 7 · Owner decisions, consolidated (LANDED as `PLAYTEST_CHECKLIST.md` item **133** by link 100, 2026-09-09, one line each pointing here; on STATE's open-decisions line)

1. **Commission the pilot, then the bounded prototype** (three modules:
   `LandscapeUnitFilter`, `TrainCargoDumping`, `StaleReservations`' callee),
   both after 99. Recommend yes.
2. **UNKNOWN policy:** decline (recommended) or name the exception in the
   wording.
3. **Wording interim:** bullet 3 stays over-promising through hotfix-2's
   upload (accepted on ck112); change it only when the transaction + pins
   ship. Arity alone earns no change.
4. **`LuaRevision` as an observation label** — clarify §2a's heading or leave
   it forbidden.
5. **Job two:** breadcrumb yes/no; engine box untouched (recommended).
6. **`LuaCodeToTuple`:** if the pilot confirms an indirect `load` in the
   engine environment, whether to report it to the developers. Not ours to
   use either way.

---

## 8 · Files

- `reports/SELFCHECK_PROMISE_AUDIT.md` — Claude, with §10 corrections (commits
  `5f595bc` → `3ab4900`).
- `reports/SELFCHECK_PROMISE_CROSSCHECK_CODEX.md` — Codex (`397bf15`).
- `prompts/CODEX_CROSSCHECK_SELFCHECK_PROMISE.md` — the brief Codex ran under.
- `prompts/SELFCHECK_PILOT.md` — the continuation (this document's §6).
- 99's inbox carries the original block and its correction.
