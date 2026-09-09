# SELFCHECK PROMISE AUDIT — can the store's self-check sentence be made literally true?

**VERDICT: YES BUT SCOPED.** The sentence can be made true for *the code the fix
patches*: the sandbox leaves `string.dump` reachable, so every module can read
the shipped target's compiled signature at boot with no per-module authoring
(this alone would have caught F115 with zero false positives on the 1.1.0 patch)
and its compiled body against a pin (this would have caught F114 and six of the
other seven surviving FIX rows). It cannot be made true for *what the fix was
written for* in the sentence's broad reading: a patch that changes the meaning
of code around an untouched target — measured here on `StaleReservations`, whose
two pinned bodies are byte-identical on 1.0.7 and 1.1.0 — is invisible to any
runtime check by construction, and hand-written behaviour probes only test the
axes their author already knew about (F114's axis was unknown to its author).
So the honest sentence is "stands down by itself if an official patch changes
the code it patches", built on a universal fingerprint, not on 44 probes. The
cost is real and is stated in §5: on a patch the size of 1.1.0 a body
fingerprint would have stood down 24 modules on day one, 17 of them working.

Audited 2026-09-09 by `smr-bugfixpack-db` under `prompts/SELFCHECK_PROMISE_AUDIT.md`.
Tree read at HEAD `3fdde36`, clean, `git pull` up to date. Game trees: 1.1.0 at
`A:\SteamLibrary\steamapps\common\Project Spark\ModTools\Src` (mtime 2026-09-08),
1.0.7 archived at `C:\Dev\SMR-SrcArchive\1.0.7.396349\Src`. ⛔ Nothing was run in
a game. Every "measured" below is one of: a tool run on both trees, a string
read of `Mars.exe`, an archived log, or the engine's own sandbox Lua executed on
a desk Lua 5.3 (`lupa 2.8`, this rig). Each is labelled. ⛔ No code, no store
text, no status moved; `Code/`, `metadata.lua`, `bugs/`, `STATE.md` and the
checklist are untouched. Proposed checklist and STATE text is in §9 for the
chain's owners to land.

**Size decision (brief §3).** One session, not a chain. The sandbox question
turned out to be desk-measurable (§4), and the 44-module classification was
fanned out to four read-only subagents under one written brief (§3 says what I
spot-checked myself). Checkpoints were committed after §2, §4, §7 and §3.

**Framing correction, from the prompt's own author (peer message 2026-09-09).**
ck112 is recorded in commit `e1095d5` as "DEFERRED". It was not deferred: the
owner rejected both recorded options and commissioned this audit as a third
route. This report cites it that way.

---

## 1 · The coverage table, re-derived

Counted by script over `Code/*.lua` (comment lines stripped first; a `{ probe =`
inside a helper counts, a commented-out one does not), then reconciled by hand
against the four modules the script found with no `Require` block at all.

| strongest check a module carries | modules | what it proves at boot |
|---|---|---|
| `probe` (behaviour on a stub) | **5** | the shipped body behaves as the module assumes *on the probed axis* |
| `test` only (a content or shape verdict, no probe) | **4** | a discriminating shape or datum is present |
| existence only (`global` / `class` / `path`) via `Require` | **31** | the target EXISTS |
| existence only, inline `rawget`/`type` with no `Require` block | **3** | the target EXISTS (`ExtenderFlapChurn`, `SequenceLatents`, `ShelterReflex`) |
| `DataPatch` with no `Require` block | **1** | the preset shape the pass reads (`DustSicknessBiorobots`) |
| **total** | **44** | |

Cross-counts: modules carrying at least one `test` = 7, at least one `probe` = 5
(three modules carry both: `LandscapeUnitFilter`, `TrainCargoDumping`,
`VacuumWalks`); modules with NEITHER = 35; `SetGlobal` sites = 5; `DataPatch`
modules = 3 (`SaintBlessing` and `SinkholeIndestructible` also have `Require`).

**Delta against the prompt's seed table**, which its author says came from a
bare `grep` and asked me to treat as a claim: the pack has **44** registered
modules, not 43 (`90_SaveSanitizer` registers like any other, `items.lua`
agrees, doccheck's module-set gate agrees); "39 existence" was 43 minus the
probe count and so double-counted the three probe+test modules — the true
"existence-only" figure is **35 of 44**. A second peer's "probes ship in
exactly two modules" predates link 04b and is stale by three. None of the
deltas changes the verdict's shape: **the promise holds, at best, for 5 of 44.**

What the other instruments cover, for the record (desk-time, players never run
them): `bodycheck.py` 97 manifest rows over 43 stamped modules (2 with no
manifest, 3 `SRC: none`, 1 pinned with no `DEFECT`), `sigcheck.py` 43
replacement sites of which 12 carry no `SRC` pin of their own function.

---

## 2 · §1a — would today's mechanism have caught the two real failures?

"Today's mechanism" is the `probe` form (`00_Core.lua:151-166`): the shipped
function is called on a stub under `pcall`; only literal `true` applies; a throw
is a decline. Probes run inside `apply()`, i.e. at the main menu before any game
is loaded, so a decline always precedes the first in-play call.

### 2a · F115 (`LandscapeUnitFilter`) — the control

**The probe as it ships** (`Fix_LandscapeUnitFilter.lua:150-177`, commit
`799f145`): a stub map whose `Landscapes` table records which key is asked for;
`fn(stub_map, PROBE_MARK, cb)`; `true` iff the key asked was `PROBE_MARK`.

**Would a 1.0.7-era equivalent have declined on 1.1.0 before the throw?** Yes,
and I measured the mechanism rather than reasoning about it. A 1.0.7-shaped
probe calls `fn(PROBE_MARK, cb)`; on the 1.1.0 body that binds `map` to a
string, and `("string").Landscapes` resolves through the string metatable to
`string.Landscapes` = nil, so `nil[mark]` throws — desk Lua 5.3, same shapes:
`attempt to index a nil value (field 'Landscapes')` ⇒ pcall false ⇒ decline.
The reverse direction (the shipped 1.1.0-shaped probe on a 1.0.7 body) also
declines: at the main menu the 1.0.7 GameVar holds `false`, so `false[mark]`
throws (`attempt to index a boolean value`); once a game is loaded the global is
a table, the probe's stub is used as the *key*, nothing is asked, `asked == nil`
⇒ decline. Three-valued as the module header claims.

**What the probe actually detects — verified, not repeated.** The 1.1.0 body
(`Landscaping.lua:509-523`) reads `map.Landscapes[mark]` at `:510` and returns
at `:512` when it is nil. Every line the probe can reach is therefore lines
509–512. The F34(d) defect line — `callback` passed where `filter_embark` was
built, `:523` — is **unreachable on any stub**: reaching it needs a real
landscape object and calls `Landscape_ForEachObject`, which is C. So the probe
detects the **signature change and the storage move**, which shipped together,
and says **nothing about the defect line**. A future patch that keeps
`(map, mark, callback, ...)` and `map.Landscapes[mark]` but rewrites the sweep
passes the probe. That is a correlate, exactly as the prompt feared; the
correlate happens to be the thing that broke this time.

### 2b · F114 (`TrainCargoDumping`) — the harder case

**The probe as it ships** (`Fix_TrainCargoDumping.lua:148-185`, `3d4c933`): a
stub station listing one storable resource with no `demand` entry — the exact
F114 input; `true` iff the shipped body asked for that resource's stored amount,
moved nothing, and replaced `assigned_resources`. On the 1.0.7 body
(`Train.lua:783-803` archived) `station.demand[res]:GetTargetAmount()` indexes
nil and throws ⇒ decline. On 1.1.0 (`:794-795`) the nil-guard yields cap 0 ⇒
`true`. So **today's probe would catch a reversion of the guard.**

**Would an equivalent probe have caught F114 at the time?** No, and this is the
finding that bounds Option 1. A 1.0.7-era author would have had to write a
probe that feeds a storable resource with no demand request and expects the
shipped body to *throw* — but the 1.0.7 author did not know that input could
exist (that a station lists lock-hidden resources with no request is a 1.1.0
fact, `Station.lua:110-111`). A probe tests the assumptions its author holds.
F114 was a change on an axis nobody had a assumption about. Only a check that
sees the body *as a whole* — the desk `bodycheck.py`, or a runtime fingerprint
(§4) — sees an unknown-axis change.

Corollary the owner should hear plainly: **full probe coverage does not deliver
the sentence.** It delivers "stands down if the code stops behaving the way the
fix assumed on the axes we thought of", which is weaker than "if a patch changes
what it was written for" and is not what a player reads.

### 2c · Against the current failures, per instrument

| instrument | F115 (signature) | F114 (body) | when |
|---|---|---|---|
| existence checks (what shipped) | no | no | boot |
| `probe`, as a 1.0.7 author would have written it | **yes** (via the storage correlate) | **no** (unknown axis) | boot |
| `probe`, as it ships now | yes | yes (guard reversion only) | boot |
| runtime arity read (§4, buildable) | **yes** | no | boot |
| runtime body fingerprint (§4, buildable) | yes | **yes** | boot |
| `sigcheck.py` / `bodycheck.py` | yes | yes | desk, after the patch |

---

## 4 · §1c — what the mod sandbox actually permits

Evidence classes: **[tree]** a read of the shipped 1.1.0 Lua; **[exe]** a
string read of `Mars.exe` (18,741,760 bytes, mtime 2026-09-08); **[log]** an
archived boot log; **[desk]** the engine's own sandbox lines executed on Lua
5.3; **[not measured]** stated as such.

1. **`debug` is blacklisted for mods, and it is absent in ONE context, not from
   the engine.** [tree] `ModEnvBlacklist` carries `debug = true`
   (`CommonLua/Modding/Mod.lua:1436`); the table closes at `:1441`. [log] The
   Test Kit's own runtime read on 1.1.0 prints `no debug.getinfo (mod sandbox)`
   (`archive/logs/first110_…-6a91a190.log:70`, 2026-09-08) — a measurement
   inside the sandbox on the shipped build. [tree] 16 shipped files call
   `debug.getinfo` (`CommonLua/Core/lib.lua`, `cthreads.lua`, …), and [exe] the
   binary carries `getinfo`, `nparams`, `isvararg`, `istailcall`, `getupvalue`,
   `sethook`. So arity via `debug.getinfo` exists for the engine and the console
   and is withheld from mod code only. ⚠️ A console read of `debug` measures the
   wrong environment; the TestKit is the right instrument because it IS a mod.

2. **`string` is not blacklisted, and the gate is on the top-level name only.**
   [tree] `ModEnvMeta.__index` (`Mod.lua:1559-1568`): `if env_blacklist[key]
   then return end` then `rawget(original_G, key)`, the whole real table.
   [desk] I executed `Mod.lua:1280-1441` (the blacklist) and `:1551-1627`
   (`ModEnvMeta` + `LuaModEnv`) verbatim on Lua 5.3 with four one-line stubs
   (`FirstLoad`, `Loading`, `PersistableGlobals`, `empty_table`), built an env
   with `LuaModEnv()` and ran a chunk inside it. Results: `debug` nil, `io` nil,
   `load` nil, `loadstring` nil, `os` = `{time}`, `getmetatable` the safe
   wrapper, `setmetatable` real, **`string` the real table, `string.dump` a
   function, `string.byte` a function.** The replica enforced the blacklist on
   my first attempt (my test used `load` and it was nil), which is the
   falsifier for the replica itself.

3. **`string.dump` is compiled into the engine.** [exe] `Mars.exe` carries the
   literal `unable to dump given function` (the error text of Lua's `str_dump`)
   and `Lua 5.3` once. ⛔ **Not a runtime proof** that the engine registers
   `dump` under `string` — an engine may strip it at registration. This is the
   one measurement left for a game boot, and it is a 5-line TestKit probe:
   `type(string.dump)`, `pcall(string.dump, LandscapeForEachUnit, true)`, print
   the length and the first 16 bytes in hex. Everything in §5's Option 3 is
   conditional on that line reading `function`.

4. **What `string.dump` returns, and how stable it is.** [desk, Lua 5.3, this
   rig — NOT the engine's build]
   - A C function refuses: `unable to dump given function`. The engine's
     C-side surface (`Landscape_ForEachObject`, `GetTargetAmount`, …) can never
     be fingerprinted; every target the pack replaces is a Lua function in a
     shipped `.lua`, so the pack's 43 replacement sites are all dumpable *if*
     item 3 holds.
   - A stripped dump (`string.dump(f, true)`) is byte-identical across chunk
     names, local-variable renames and comment edits, and **differs across line
     positions**: two dumps of the same body five lines apart differ in exactly
     the bytes holding `linedefined`/`lastlinedefined` (positions 36 and 40 of
     the outer proto, 129 and 133 of its nested closure). So a raw hash flips on
     any edit *above* the target in its file. Those ints sit at fixed places in a
     self-describing format (header 34 bytes: signature, version, format,
     `LUAC_DATA`, five size bytes, `LUAC_INT`, `LUAC_NUM`; then upvalue count;
     then per proto: source, two ints, `numparams`, `is_vararg`, `maxstacksize`,
     code, constants, upvalues, nested protos, debug). A ~80-line Lua walker can
     zero the two ints in every proto and must land exactly on the last byte of
     the dump — if it does not, the format is not what it assumed and the check
     **abstains** rather than declines. That is the built-in falsifier the
     peer's "flips every hash" hazard needs.
   - **Arity needs no pin at all.** `numparams` and `is_vararg` are single bytes
     at offset `36 + 2 × sizeof(int)` of a stripped dump. [desk, inside the
     sandbox replica] the 1.1.0-shaped shipped function reads `3, vararg`; the
     1.0.7-shaped replacement reads `2, vararg`; mismatch = true. The expected
     value is our own replacement's dump, so the check is self-describing:
     `arity(shipped) == arity(ours)`, computed at install, per site, forever.
   - Cost: FNV-1a in pure Lua over 43 × 200 bytes ran in 1 ms on the desk; real
     targets are 0.5–5 KB, so tens of milliseconds per boot at most.

5. **Bytecode can be hashed but never loaded.** [tree] `load`, `loadstring`,
   `dofile`, `pdofile`, `dostring` are all blacklisted (`Mod.lua:1424-1432`).
   This kills the ck73 "trampoline" idea (no separately-loaded chunk, no custom
   chunk name) and removes the only injection route a `string.dump` capability
   could otherwise open.

6. **Body-versus-source comparison is desk-only, by two independent bars.**
   [tree] `io` is blacklisted (`:1437`), and players do not have `ModTools/Src`
   in the first place — the shipped game carries packed `.hpk` code. So the
   `SRC:` sha256 pins and `bodycheck.py` cannot reach runtime in their present
   form; what CAN reach runtime is a second pin of the *compiled* body, taken
   from the engine itself (item 4).

7. **The two-branch measurement of what a fingerprint would have done on
   1.1.0.** [tool, both trees] With the current 1.1.0 pins compared against the
   archived 1.0.7 tree, `bodycheck.py --src <archive>` reports **27 BODY-CHANGED
   rows + 1 TARGET-ABSENT across 24 of 44 modules**; `sigcheck.py --src
   <archive>` reports **1 MISMATCH** (`LandscapeUnitFilter`, F115) and 42 OK.
   Reconciled against the re-verification's verdicts:

   | | modules |
   |---|---|
   | pinned body differs between branches | 24 |
   | … of which the re-verification ruled FIX (F-1, F-3, F-6, F-7, F-8, F-9, F-10) | 7 |
   | … of which it ruled KEEP (fix still correct on the new body) | 17 |
   | FIX rows whose pinned bodies are identical on both branches | **1 — `StaleReservations` (F-2)** |
   | replacement signatures that differ | 1 (F115) |

   ⇒ A body fingerprint pinned on 1.0.7 would have stood down 24 modules at the
   first 1.1.0 boot: 7 correctly (the ones that were broken or reverting 1.1.0
   improvements, F114 among them) and 17 needlessly (a source edit that left the
   fix correct). An arity read would have stood down exactly F115 and nothing
   else. Neither sees F-2, because nothing in the code we pin changed — 1.1.0
   added a new reservation *kind* elsewhere. ⚠️ Source hashes are the proxy
   here; a stripped bytecode hash is invariant to comment and rename edits, so
   its false-positive count is at most 17 on this patch and probably lower.
   1.1.0 was the largest patch this title has had; a hotfix touches fewer files.

8. **Class (c) is the ceiling, and the prompt's count of it is off.** The
   re-verification's own table (`PACK_1_1_0_REVERIFICATION.md` §4) lists six
   class-(c) instances in total — F111, F112, F-1, F-2, F-3, F-5 — of which
   **four**, not six, are among the ten FIX rows. Of those four, two are
   caught by fingerprinting a *callee* the module depends on rather than its
   target (F-1: `AddDomeColonistsModifier`'s body changed; F-3:
   `Community:GetScoreFor`'s signature changed), one is data (F-5, a rewritten
   profile preset — a data hash on the fields a `DataPatch` reads would see it),
   and one is genuinely invisible (F-2). So "class (c)" as the audit uses it
   mixes "we pinned the wrong function" with "no function changed"; only the
   latter is the hard ceiling, and it is one module of 44 on this patch.

9. **The "whole pack stands down at once" hazard, sized.** The Lua compiler is
   inside `Mars.exe`; hashes flip pack-wide only if its code generator changes
   (a Lua version bump, an optimisation change). The header carries the version
   and format bytes, so a version bump makes the walker abstain, not decline;
   an optimisation change under the same version would flip every hash and is
   the one case that decline-all reaches. It is discriminable after the fact in
   five minutes — desk `bodycheck.py` OK on the same targets while every runtime
   pin mismatches means "recompiled, not changed" — and recoverable with one
   boot to re-pin plus one upload. Whether the pack should decline-all or
   abstain-all on a quorum of simultaneous mismatches is an owner call (§9).
