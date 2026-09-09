# CROSS-VENDOR CHECK — re-examine the self-check promise audit, and look for what it missed

You are Codex. You have never run in this repository, you have no shared memory
with the sessions that work here, and nobody will answer questions mid-task.
**Everything you need is in this file or in the files it names.** Read this
file to the end before you open anything else.

The owner commissioned this because a Claude session (`smr-bugfixpack-db`,
2026-09-09) produced an audit they are inclined to believe and want checked by a
vendor that shares none of its priors. Your job is two-fold: **(1) try to
refute the audit's load-bearing claims by your own methods, and (2) come up with
ideas it did not have.** Agreeing with it is a valid result only if you tried to
break it and could not; disagreeing is a valid result only with evidence.

---

## 0 · The environment, and the rules that bind you (read every line)

**Machine.** Windows 11. Repository at `C:\Dev\SMR-BugFixPack` (git, remote
configured, pushing is standing-allowed). Python 3.13 is `python` on PATH, with
`lupa 2.8` installed (embedded Lua runtimes: `lupa.lua53` gives a stock Lua
5.3, also 5.1/5.2/5.4/LuaJIT). No standalone `lua` binary. Two shells: Windows
PowerShell 5.1 (no `&&`; `Set-Content`/`Out-File` re-encode files — do NOT use
them on repo files) and Git Bash (`grep`, `sed`, `cmp`, POSIX paths `/c/...`).
Prefer Python for any file edit; write UTF-8 **without BOM**, LF line endings,
and preserve a file's existing endings if you edit one.

**Game.** Surviving Mars: Relaunched, Haemimont "Sol" engine, Lua 5.3-based.
Installed build **1.1.0.403908** (auto-updated 2026-09-08). Shipped Lua source:
`A:\SteamLibrary\steamapps\common\Project Spark\ModTools\Src` (`Lua/`,
`CommonLua/`). The previous build's tree is archived at
`C:\Dev\SMR-SrcArchive\1.0.7.396349\Src`. The executable is
`A:\SteamLibrary\steamapps\common\Project Spark\Mars.exe` (18,741,760 bytes).
⛔ **Never write anything under `A:\SteamLibrary\`.** Read-only truth.

**⛔ Never launch `Mars.exe` or `MarsDebug.exe`.** The owner runs the game.
Reasons you must not: the Mod Editor auto-bumps the mod's version on any save;
the first call to a portal API creates a store listing; loading a copied
campaign deletes the owner's autosaves; an agent-run boot has no witness. If a
question can only be settled by a boot, WRITE the probe (a Lua snippet, a Test
Kit stub, or a console line) into your report and say what it would show.

**⛔ Files you must not edit:** anything under `Code/`, `items.lua`,
`metadata.lua`, `docs/agent/STATE.md`, `docs/PLAYTEST_CHECKLIST.md`, anything
under `docs/agent/bugs/`, `docs/agent/facts/`, `docs/archive/`, and every
`INDEX.md` (generated). Your deliverable is ONE new file (§8). Anything that
needs an owner decision goes in that file under its own heading; the owner
routes it.

**Concurrent sessions.** Several Claude sessions commit to this tree at the same
time and you cannot message them. Therefore: `git pull --ff-only` before you
start; run `git status` before every commit and **never touch a file that
shows modified and is not yours**; `git add` and `git commit` only your own
file by explicit path (never `-A`, never a directory); push immediately after
committing. If the push is rejected because the remote moved, run
`git pull --rebase` and push again — never `--force`. Commit messages via
`git commit -F <file>` (embedded quotes break under PowerShell 5.1). Put
"Codex" in the commit subject so the owner can tell vendors apart.

**Doc gate.** Before any commit run `python tools/doccheck.py`; the last line
must read `doccheck: GREEN`. It prints ~18 lines of the form
`warn <id>: the frozen index-row cell says 'filed', entry says ...` — those are
pre-existing and normal. If it prints a line about `STATE.md` bytes, copy that
line verbatim into your report. New files live under `docs/agent/reports/`
(reports) or `docs/agent/prompts/` (briefs); the `docs/` root is a closed list.

**House rules that shape what counts as evidence here** (owner rulings; you are
bound by them, and you may argue against one only with evidence):
- **Trust runtime over source reads.** A source-read prediction of 6
  self-disabled modules measured as 13 on the real boot (fact `EF-078`). Label
  every claim you make as MEASURED (a tool run, a binary read, an archived log,
  an executed replica) or READ (a source read). Never present a read as a
  measurement.
- **A recorded fact is a claim.** Bug entries, fact files and the audit itself
  can be wrong; re-derive routes, not just citations.
- **Check the thing, not its label.** A name sweep cannot see an arity change; a
  version number cannot see a body change. `FIX_POLICY` §2a forbids a
  game-version detector as a GATE (two reasons, both stated there).
- **"You can X" needs a route check.** Any sentence about what a player or the
  pack does must be walkable step by step on the real platform.
- **Fix negatives, not small positives.** A player LOSS gets repaired; an
  unearned bonus is not chased. Relevant to any "stand down more often"
  trade-off you cost.
- **Post-launch work is patch-note maintenance**, not a release gate; do not
  price a one-module change with a release-sweep's cost.
- **Skips by name, never a total.** If you did not open something, name it.
- **A source read never moves a status; nothing here is "tested".**

---

## 1 · The project, in one page

The **Relaunched Fix Pack** (mod id `SMR_CommunityFixPack`, published on
Paradox Mods `156049` and Steam Workshop `3787202810`, tree version 5) is a
runtime Lua mod that repairs defects in the game's shipped Lua. No game files
are modified. Each fix is one file `Code/Fix_<Name>.lua` (44 registered
modules, 45 files including `00_Core.lua`). A module calls
`SMRFixPack.Register(id, { title, apply })`; `apply()` runs at the main menu
(inside `ModsLoadCode()`, before class flattening and before presets load),
under `pcall`. It first calls `SMRFixPack.Require(id, { ...checks... })`
(`Code/00_Core.lua:142-215`); any failing check returns a reason string and the
module logs `<id>: inactive (<reason>)` and installs nothing; otherwise it
patches (a wrapper around the original, a full replacement body, an `OnMsg`
handler, or a data edit) and logs `<id>: applied`.

**Check forms** (`00_Core.lua:100-141`): `{ global = }`, `{ class = , method = }`,
`{ path = }` prove a target EXISTS; `{ test = fn }` is a content verdict;
`{ probe = fn }` (added 2026-09-08) calls the SHIPPED function on a stub under
`pcall` and applies only on literal `true` — a throw, nil, false or any other
value declines. The probe contract: only for targets shown synchronous and
side-effect-free on a stub, with the stub contract written beside it. Five
modules carry one. A failing existence check also sets `update_suspect`, which
feeds a one-time in-game dialog ("N of this pack's fixes found that the game
code they patch has changed … and switched themselves off for safety").

**Mods run in a sandbox** (`CommonLua/Modding/Mod.lua`, 1.1.0 line numbers):
`ModEnvBlacklist` `:1280-1441` lists top-level global names a mod cannot see
(`debug`, `io`, `os` except `time`, `package`, `load`, `loadstring`, `dofile`,
`rawget`/`getmetatable` replaced by safe wrappers …); `ModEnvMeta.__index`
`:1559-1568` returns `rawget(original_G, key)` for any name NOT on that list
— the real table, whole; `LuaModEnv()` `:1612-1626` builds the env.

**Desk-time tools** (Python, `tools/`, players never run them):
`bodycheck.py` (per-module `-- SRC: <path> <selector> sha256=…` pins of the
shipped body plus a `-- DEFECT:` regex; reports BODY-CHANGED / DEFECT-GONE /
TARGET-ABSENT), `sigcheck.py` (arity of every replacement site vs the shipped
declaration), `parsecheck.py`, `logscan.py`, `doccheck.py`. Both accept
`--src <path>` to point at the archived 1.0.7 tree.

**The two failures that started this** (game 1.1.0 broke two shipped fixes in
players' games; both reported `applied` then threw):
- `F114` `Fix_TrainCargoDumping` — a body change at unchanged arity. 1.1.0 lets
  a station list a resource with no demand request; our copied 1.0.7 body
  indexed it unguarded. 157 throws in 42 minutes; found by a player.
- `F115` `Fix_LandscapeUnitFilter` — a signature change
  (`LandscapeForEachUnit(mark, callback, ...)` → `(map, mark, callback, ...)`).
  Found by the owner pressing a button.
Neither stood down: the checks asked whether the target existed, and it did.

**The store sentence** (HOW IT WORKS bullet 3, live on both stores):
> Every fix checks the game's code before it touches anything, and stands down
> by itself if an official patch changes what it was written for. A fix that
> stands down does nothing at all — it never guesses.

**The owner's ruling (checklist item 112, 2026-09-09):** they rejected both
"reword it smaller" and "leave it"; they asked for a third route — make the
mechanism strong enough that the sentence is simply true — and accepted that
"it cannot be made fully true, here is the strongest thing that is" is a valid,
evidenced answer. The sentence stays published and over-promising until then.

---

## 2 · What the Claude audit concluded (treat every line as a claim)

Report: `docs/agent/reports/SELFCHECK_PROMISE_AUDIT.md` (read it whole; its §8
"What I did NOT check" is where to start looking for holes). Brief it ran
under: `docs/agent/prompts/SELFCHECK_PROMISE_AUDIT.md`.

**Verdict: YES BUT SCOPED.** The sentence can be made literally true for *the
code the fix patches*, never for *what the fix was written for*.

Its argument, compressed:
1. Today the promise holds for at most 5 of 44 modules (the probed ones), and
   a probe only sees the axis its author thought of: a 1.0.7-era probe would
   have caught F115 (through a correlate, the storage move) but not F114
   (unknown axis).
2. `string.dump` is reachable from mod code; `debug` is not. Measured by
   executing the engine's own blacklist + `LuaModEnv` lines on stock Lua 5.3,
   and by strings inside `Mars.exe`. Not measured in a running game.
3. From a stripped dump, `numparams`/`is_vararg` are readable at a fixed
   offset, so a replacement's arity can be compared with the shipped function's
   at install with ZERO per-module authoring. Against the archived 1.0.7 tree
   this flags exactly F115 and nothing else.
4. A normalised bytecode hash (zero the per-proto `linedefined` fields) pinned
   in each module header would see body changes. Against the archived tree the
   equivalent source-hash pins flag 27 rows in 24 of 44 modules — 7 that the
   humans ruled FIX, 17 that they ruled KEEP (fix still correct). So it would
   have stood down 17 working modules on 1.1.0's first boot.
5. `StaleReservations` (F-2) is the measured ceiling: its two pinned bodies are
   byte-identical on both branches; 1.1.0 changed its meaning elsewhere. No
   runtime check can see that.
6. Probes cannot deliver "every fix": of 44 modules, 13 are probeable (5 done),
   8 partially, 23 not (handlers, data patches, thread-spawning or
   state-mutating targets); 30 carry a stated side-effect hazard for a naive
   probe.
7. Recommendation: a 5-line Test Kit probe to confirm `string.dump` at runtime;
   then the arity check; then the body pin with a quorum policy; scope the
   sentence to "the code it patches".
8. Job two (being blamed for other mods' errors): the engine names any mod whose
   content path is a substring of the error or the stack (`Mod.lua:3019-3031`),
   once per mod per session (`:2980-2983`), in enable order. Zero
   misattributions in the archived logs; two in the field (F104, F105), both
   pass-through frames. Every pre-wrapper in the pack already ends in
   `return orig(...)` (a proper tail call, which removes the frame), so the
   tail-call remedy is a rule, not an edit. A breadcrumb via our own
   `OnMsg.OnLuaError` handler is recommended; swallowing errors is forbidden.

---

## 3 · The load-bearing claims, numbered — refute each by your own method

For each: say CONFIRMED / REFUTED / PARTLY / COULD NOT TEST, label your evidence
MEASURED or READ, and cite `file:line` or the command you ran. Do not reuse the
audit's scripts as proof; re-derive with your own (its scripts are in §7 so you
can critique them, not so you can re-run them and call it independent).

| # | claim | how the audit established it | how you might break it |
|---|---|---|---|
| C1 | 44 registered modules; 5 carry a `probe`, 7 a `test`, 35 neither; 3 modules (`ExtenderFlapChurn`, `SequenceLatents`, `ShelterReflex`) have no `Require` block at all, 1 (`DustSicknessBiorobots`) is a DataPatch with none | a Python census over `Code/*.lua` with comment lines stripped, reconciled by hand | count differently (a real Lua parser via lupa; `items.lua`; `doccheck --emit-counts`); find a probe or test built from a variable that a regex misses |
| C2 | a 1.0.7-shaped probe `fn(PROBE_MARK, cb)` on the 1.1.0 `LandscapeForEachUnit` throws (string-indexed `map`), so it would have declined before the throw | desk Lua 5.3 with both shapes; body read `Landscaping.lua:509-523` vs archive `:452-469` | check whether the engine's string metatable differs (does `("x").Landscapes` resolve to nil there, or could a string method table shadow it?); check whether `apply` could run with a game loaded (the enable path) so that the 1.0.7 GameVar is a table, not `false` |
| C3 | no 1.0.7-era probe would have caught F114, because the failing input (a storable resource with no demand request) did not exist on 1.0.7 and a probe tests only known assumptions | reading of both `Train:UnloadAll` bodies and `Station.lua:110-111` | design a probe a 1.0.7 author could plausibly have written that declines on 1.1.0's body; consider a generic access-trace comparison (record which fields/methods the shipped body touches on a minimal stub, compare to a recorded trace) and say whether it distinguishes the two bodies WITHOUT a stub that anticipates the change |
| C4 | `debug` is blacklisted (`Mod.lua:1436`) and absent inside the sandbox at runtime on 1.1.0 | READ + a Test Kit log line `no debug.getinfo (mod sandbox)` in `docs/archive/logs/first110_Mars.exe-20260908-15.20.28-6a91a190.log:70` | find any path by which mod code reaches `debug` (an alias in `_G`, a non-blacklisted table holding a reference, `getmetatable` on something, `coroutine`, the safe `rawget` wrapper's semantics at `Mod.lua:1591-1596`) |
| C5 | `string` is the real table and `string.dump` resolves for a mod chunk | the engine's `Mod.lua:1280-1441` + `:1551-1627` executed verbatim on stock Lua 5.3 (§7.1); the blacklist gates only the top-level name | find a place where the engine strips or replaces `string.dump` (grep the whole `Src` tree for `string.dump`, `dump = nil`, `strlib`, `string_dump`; look at `CommonLua/Core/autorun.lua` and anything run before mods load); read the exe (§7.4) more carefully than the audit did |
| C6 | `string.dump` is compiled into `Mars.exe`: the string table holds `unable to dump given function`, `Lua 5.3`, the `LUAC_DATA` magic `\x19\x93\r\n\x1a\n`, and `dump` sits in the string-library registration cluster (`byte dump find format gmatch gsub len rep reverse sub pack packsize unpack`) | binary string reads | note that `char`, `lower`, `upper`, `match` are NOT in that cluster — does that mean a modified `strlib`, and could `dump` be registered yet removed later? Is there a second cluster? Is the cluster order the stock `lstrlib.c` order? |
| C7 | from a stripped 5.3 dump, `numparams` and `is_vararg` sit at byte offset `36 + 2*sizeof(int)` (1-based), sizes self-described in the 34-byte header | measured on stock Lua 5.3 (§7.2) | check the engine's format: does the exe carry stock header constants (`LUAC_VERSION` 0x53, `LUAC_FORMAT` 0, `LUAC_INT` 0x5678, `LUAC_NUM` 370.5)? Could Haemimont's build change `Instruction` size, integer size, or the dump layout? What would a parser see, and would the audit's "abstain on any surprise" rule actually catch a layout change that keeps the header bytes? |
| C8 | stripped dumps are invariant to chunk name, local renames and comments, and differ across line shifts only in `linedefined`/`lastlinedefined` per proto | measured on stock 5.3 (§7.3) | find another field that survives `strip` and varies without a semantic change (upvalue names? source? constants ordering? `maxstacksize` under a different register allocation for an equivalent expression?) |
| C9 | against the archived 1.0.7 tree, `sigcheck.py --src` reports exactly 1 MISMATCH (F115) and `bodycheck.py --src` reports 27 BODY-CHANGED + 1 TARGET-ABSENT across 24 modules; 7 of those 24 were FIX rows, 17 KEEP | tool runs + reconciliation against `docs/agent/reports/PACK_1_1_0_REVERIFICATION.md` §1a | re-run both tools yourself; recount the FIX/KEEP split against the report's table; check whether source-hash pins over-count relative to what a stripped bytecode hash would flag (a pure rename or comment edit flips the source hash, not the bytecode) — the audit says "at most 17, probably fewer" without measuring |
| C10 | `StaleReservations`' pinned bodies are identical on both branches — class (c) proper, one module of 44 on this patch | `bodycheck --src` did not list it | verify by diffing `Residence:GetFreeSpace` and `Residence:ReserveResidence` across the trees yourself; then ask whether any OTHER module's failure on 1.1.0 was also outside its pinned code (F-1 `SaintBlessing`, F-3 `ShelterReflex`, F-5 `AstrogeologistExtractors` — the audit says a callee or data pin would catch those; would it?) |
| C11 | the per-module classification (13 / 8 / 23; 30 hazards; 64 install sites = PRE-TAIL 15, PRE-NOTAIL 0, POST 13, REPLACE 15, HANDLER 17, DATA 4) | four subagent reads, spot-checked on four shipped bodies | pick any five modules the audit's §3 table calls UNPROBEABLE or PARTIAL and try to write a safe probe; pick five PROBEABLE ones and try to show the sketched probe has a side effect or reads silence as permission; recount the site shapes with a script |
| C12 | the engine names every mod whose `content_path` is a substring of `err` or `stack`; once per mod id per session; enable order | READ `Mod.lua:2968-3031`, `:2137-2143`, `:2003-2009`; `CommonLua/UI/ModManager.lua:35-40`; MEASURED dedupe from `docs/archive/logs/f114repro110_…log` (one `Error in mod` at `:274`, then 157 `Fix_TrainCargoDumping.lua:89` throws with no second line) | check what `os_paths` does (`:3022-3025`, `ConvertToOSPath`) — could the OS-path form match something the content path does not? Is `string.find_lower` a plain find (no patterns)? Does `SetSpecialLuaErrorHandling("Mods", …)` (`:3015`, `gamelib.lua:1060`) change what `stack` contains? |
| C13 | zero misattributions in the archive: every `Error in mod` line (4 lines, 3 sessions; `unforced110_…` is a 274-line prefix of `f114repro110_…`) names the mod whose code threw | `grep` + reading each stack | grep yourself over `docs/archive/` including `.md` files; check for the box's other strings (`Mod Flagged`, `Mod-related problem`); check the reporter stacks quoted in `docs/agent/bugs/F104.md` and `F105.md` |
| C14 | a Lua proper tail call (`return f(...)` exactly) removes the caller's frame so no stack walker can print it; measured with `debug.traceback` on stock 5.3; `Mars.exe` carries `(...tail calls...)` | Lua 5.3 manual §3.3.7 + desk + binary string | the engine's `GetStack` is a custom C printer (`file(line):  method Name`); could it reconstruct a tail-called caller from anything (`istailcall`, a shadow stack, its own hooks)? Is `procall`/`sprocall` (`CommonLua/Core/…`) wrapping calls in a way that defeats the tail call? Does `pcall`/`sprocall` at `CommandObject.lua:244` matter? |
| C15 | `OnLuaError` is not in `ModMsgBlacklist` (`Mod.lua:1443-1452`), so a mod may register `OnMsg.OnLuaError(err, stack)`; `load`/`loadstring` ARE blacklisted so a "trampoline" chunk is impossible; `config` and `ReportedMods` are reachable (and using them is rejected) | READ | check `safe_OnMsg`'s `__newindex` (`:1607-1613`) and whether `OnLuaError` arrives at mod handlers before or after the engine's; check whether `Msg("OnLuaError")` is raised from C with the same args |
| C16 | `LuaRevision` (the game's Lua revision, 403908 on 1.1.0) is a plain global, not blacklisted, read by the engine at `Mod.lua:919` — so a runtime version LABEL is reachable even though the house rule forbids using it as a gate | READ (the audit checked the blacklist for it; it never used it) | confirm reachability; then see I3 below |

---

## 4 · Ideas the audit did NOT pursue, or ruled out — evaluate each, and add your own

The owner's actual question is *"does another vendor come up with different
ideas?"* Spend real effort here. For each idea: is it reachable inside the
sandbox (cite), what does it make true, how does it fail, what does it cost, and
does it survive the house rules in §0 (say which rule it strains).

- **I1 · Access-trace fingerprint.** Instead of a hand-written probe per module,
  a generic harness calls the shipped function on an instrumented stub (a proxy
  that records every field read, method call and argument) and compares the
  trace to one recorded at pin time. Universal for probeable targets? Does it
  need a per-target stub anyway? Does it see F114 (the audit says only if the
  stub omits `demand[res]`, which a 1.0.7 author would not have thought to do)?
- **I2 · Pin callees, not just targets.** Two of the four "class (c)" failures
  (F-1, F-3) were changes in functions the module CALLS, not the one it
  replaces. Is there a mechanical way to enumerate a module's callees for
  pinning (static parse of the module body; or a runtime trace of a dry call)?
- **I3 · `LuaRevision` as a discriminator, not a gate.** The house rule forbids
  a version detector as a gate (`FIX_POLICY` §2a; read its two reasons — one is
  "it would be a label check", the other is "unbuildable from the mod's own
  fields", and the second is about the mod's metadata, not the engine's
  global). Evaluate a NON-gate role: (a) stamp the revision the pack was pinned
  on and tell the player "verified on build X, you are on Y" without changing
  what applies; (b) use it as the quorum discriminator for a body-hash mass
  mismatch (hashes flipped AND revision unchanged ⇒ something other than a
  patch, e.g. another mod replacing the function). Say whether either is
  honest, and whether the owner's rule as written actually excludes it.
- **I4 · Another mod replacing our target.** The audit's body pin would decline
  a module whose target another mod has already replaced (the dump is of the
  other mod's function). Is that correct behaviour, a false stand-down, or a
  new signal (the pack could say "another mod already changed this function")?
  Does `string.dump` on a function defined by ANOTHER mod succeed, and does the
  dumped chunk name (unstripped) reveal which mod? Does that open a privacy or
  attribution question?
- **I5 · Data hashing for `DataPatch` modules.** Three modules patch preset
  data, not code. Can the fields a pass reads be serialised deterministically
  and hashed at apply time so a rewritten preset (F-5's class) declines?
- **I6 · The unstripped dump.** `string.dump(f)` without `strip` keeps line
  info, local names and the source name. Is there a USE for the line info —
  e.g. hashing only the instructions that map to the DEFECT line's neighbourhood
  — or does it just add brittleness?
- **I7 · Where else could a body change be visible?** `tostring(fn)` is an
  address (useless); `select('#', …)` on a call cannot see arity; `getmetatable`
  is the safe wrapper; `coroutine` and `utf8` are not blacklisted; `Msg`
  filtering is by name. Is there anything else in the reachable surface that
  varies with a function's body or signature?
- **I8 · The other direction: make the fix itself tolerant instead of making it
  stand down.** For full-body copies, could the pack ship the DIFF (the one
  `-- FIX` line) and apply it to whatever body ships, rather than a frozen copy?
  `load` is blacklisted so source patching is out — but is there any runtime
  way to compose behaviour that survives a body edit, and would it be in
  charter (the pack must never guess)?
- **I9 · Job two, other mitigations.** Beyond a breadcrumb and a tail-call rule:
  is there a way for the engine's box to carry the throw site? Could the pack
  register its handler to run FIRST and annotate `err` (it cannot mutate the
  string the engine already holds — check)? Is there a Paradox/Steam-side
  surface where misattribution is cheaper to correct?
- **I10 · Anything you think of that is not on this list.** That is the point.

---

## 5 · Numbers you will need, and where they come from

| item | value | source |
|---|---|---|
| modules / files | 44 / 45 | `python tools/doccheck.py --emit-counts` |
| replacement sites (`sigcheck`) | 43, of which 5 via `SetGlobal`; 12 carry no `SRC` pin of their own function | `python tools/sigcheck.py --coverage` |
| manifest rows | 97 over 43 stamped modules; 2 NO-MANIFEST, 3 SRC-NONE, 1 NO-DEFECT | `python tools/bodycheck.py` |
| two-branch deltas | 27 BODY-CHANGED + 1 TARGET-ABSENT (24 modules); 1 MISMATCH | `… --src "C:\Dev\SMR-SrcArchive\1.0.7.396349\Src"` |
| 1.1.0 re-verification verdicts | 10 FIX / 35 REMOVE / 35 KEEP over the pre-deletion 80 | `docs/agent/reports/PACK_1_1_0_REVERIFICATION.md` §1a–1d, QA'd in `VANILLA_FIX_QA.md` §0 |
| archived logs | `docs/archive/*.log` (95) and `docs/archive/logs/*.log` (10, the 1.1.0 ones end `-6a91a190.log`) | |
| the four `Error in mod` lines | `act1_Mars.exe-20260819-15.18.19-6a22b86d.log:522`, `logs/forced110_…:300`, `logs/f114repro110_…:274`, `logs/unforced110_…:274` | `grep -rn "Error in mod" docs/archive/` |
| store sentence, live | `metadata.lua`, key `description`, HOW IT WORKS bullet 3 | |
| the pack's own dialog text | `Code/00_Core.lua:581-640` (`UpdateSuspects` + the `WaitMessage`) | |

---

## 6 · Read path, in order

1. This file, to the end.
2. `docs/agent/STATE.md` — the project's one mandatory read (kernel of current
   state and hazards; you already have the hazards that bind you in §0).
3. `docs/agent/FIX_POLICY.md` §2, §2a, §2b (self-checks, branch guards, the
   manifest) — ~200 lines starting at line 79.
4. `Code/00_Core.lua:100-230` (`Require` and its doc block) and `:581-640`.
5. `docs/agent/reports/SELFCHECK_PROMISE_AUDIT.md` — the thing you are
   checking. Read §8 first, then §4, §2, §3, §7, §5, §6, §9.
6. `Code/Fix_LandscapeUnitFilter.lua` and `Code/Fix_TrainCargoDumping.lua` —
   the two probes and their headers, which record both branches' bodies.
7. `docs/agent/facts/EF-006.md`, `EF-065.md`, `EF-078.md` (sandbox; the blame
   box; why runtime beats source reads).
8. `docs/agent/bugs/F114.md`, `F115.md`, `F104.md`, `F105.md` — long; read
   the top matter and the quoted stacks.
9. The 1.1.0 `CommonLua/Modding/Mod.lua` at the line ranges cited above, and
   the archived 1.0.7 counterpart when a claim compares branches.

---

## 7 · What the audit ran, verbatim — so you can critique it (do not cite a re-run of these as independent confirmation)

### 7.1 The sandbox replica (Python + lupa, stock Lua 5.3)

```python
import io, lupa.lua53 as L
M = "A:/SteamLibrary/steamapps/common/Project Spark/ModTools/Src/CommonLua/Modding/Mod.lua"
lines = io.open(M, encoding="utf-8").read().split("\n")
bl  = "\n".join(lines[1279:1441])   # Mod.lua:1280-1441  ModEnvBlacklist + ModMsgBlacklist + OnMsg.Autorun
env = "\n".join(lines[1550:1627])   # Mod.lua:1551-1627  ModEnvMeta, safe_* wrappers, LuaModEnv
prelude = "FirstLoad = true\nLoading = true\nPersistableGlobals = {}\n" \
          "empty_table = setmetatable({}, {__newindex = function() error('empty_table write') end})\n"
code = prelude + bl + "\n" + env + r'''
SMRProbeShipped = function(map, mark, callback, ...) end   -- a "shipped" Lua function in the real _G
local env = LuaModEnv()
local chunk = load([[
  local out = {}
  out.debug_type = type(debug); out.io_type = type(io); out.load_type = type(load)
  out.string_type = type(string); out.dump_type = type(string.dump); out.byte_type = type(string.byte)
  local ok, res = pcall(string.dump, string.format); out.dump_c = tostring(ok) .. " " .. tostring(res)
  local function arity(fn) local d = string.dump(fn, true); local int = d:byte(13)
    return d:byte(36 + 2*int), d:byte(36 + 2*int + 1) end
  local a1, v1 = arity(rawget(_G, "SMRProbeShipped"))
  local a2, v2 = arity(function(mark, callback, ...) end)
  out.arity = a1 .. "/" .. v1 .. " vs " .. a2 .. "/" .. v2
  return out
]], "=Mod/SMR_Test/Code/x.lua", "t", env)
local out = chunk(); local keys = {}
for k in pairs(out) do keys[#keys+1] = k end; table.sort(keys)
local s = {} for _, k in ipairs(keys) do s[#s+1] = k .. " = " .. tostring(out[k]) end
return table.concat(s, "\n")
'''
print(L.LuaRuntime().execute(code))
```
Result the audit got: `debug_type = nil`, `io_type = nil`, `load_type = nil`,
`string_type = table`, `dump_type = function`, `byte_type = function`,
`dump_c = false unable to dump given function`, `arity = 3/1 vs 2/1`.

### 7.2 / 7.3 Dump offsets and stability (stock Lua 5.3 via lupa)

Two loads of the same function body, one shifted five lines down;
`string.dump(f, true)` on each; byte positions that differ: `36, 40, 129, 133`
(the outer proto's `linedefined`/`lastlinedefined` and the nested closure's).
Stripped dumps equal across chunk names and local renames; NOT equal across a
comment insertion that changes line numbers. `string.dump(print)` and
`string.dump(string.format)` → `unable to dump given function`.

### 7.4 Binary reads of `Mars.exe`

```python
b = open("A:/SteamLibrary/steamapps/common/Project Spark/Mars.exe", "rb").read()
for s in (b"unable to dump given function", b"(...tail calls...)", b"Lua 5.3", b"\x19\x93\r\n\x1a\n"):
    print(s, b.count(s))                      # 1, 1, 1, 1
import re
for m in re.finditer(rb"\x00dump\x00", b):    # NUL-separated string-table neighbours
    seg = b[max(0, m.start()-120):m.end()+120].split(b"\x00")
    print([x.decode("latin1") for x in seg if 2 < len(x) < 12])
# -> byte, dump, find, format, gmatch, gsub, len, rep, reverse, sub, pack, packsize, unpack
```

### 7.5 The census

Regexes over `Code/*.lua` with comment lines removed: `\{\s*(global|class|path)\s*=`,
`\{\s*test\s*=`, `\{\s*probe\s*=`, `SMRFixPack\.DataPatch\(`, `SMRFixPack\.SetGlobal\(`;
then the four zero-`Require` modules opened by hand.

### 7.6 The two-branch runs

```
python tools/bodycheck.py --src "C:\Dev\SMR-SrcArchive\1.0.7.396349\Src"
python tools/sigcheck.py  --src "C:\Dev\SMR-SrcArchive\1.0.7.396349\Src"
```

### 7.7 The tail-call measurement

`xpcall` with `debug.traceback` around three wrappers of a thrower:
`return thrower(...)` (traceback shows the thrower, then `(...tail calls...)`,
no wrapper line), `thrower(...)` then `end` (wrapper line present),
`local r = thrower(...) return r` (present).

---

## 8 · Deliverable

Write ONE file: `docs/agent/reports/SELFCHECK_PROMISE_CROSSCHECK_CODEX.md`.

Required shape, in this order:
1. **First line: `VERDICT: AGREE / DISAGREE / PARTLY AGREE`** with the audit's
   "YES BUT SCOPED", then one paragraph of why.
2. **Where you differ** — before anything else. Every disagreement with a
   claim in §3 or a recommendation in the audit's §5, with your evidence and
   its label (MEASURED / READ). If you differ nowhere, say what you tried.
3. **The §3 table, answered** — one row per claim, verdict + evidence.
4. **Ideas** — §4's list evaluated, plus your own, each costed against the four
   questions (what it makes true, build cost, runtime cost, how it fails) and
   checked against the §0 house rules.
5. **Runtime reads still owed** — every question you could only settle by a
   boot, with the exact probe you would run and what each outcome would mean.
6. **What you did NOT check — by name.** A file you did not open is not a file
   that passed.
7. **For the owner** — anything needing a decision, in plain language, one
   paragraph each, with your recommendation first.
8. **Gates** — the `doccheck` last line, and any `STATE.md` byte line verbatim.

Then `python tools/doccheck.py` (GREEN), `git add` your file by path,
`git commit -F <msgfile>` with "Codex" in the subject, `git push`; if the push
is rejected, `git pull --rebase` then push again.

Bindings, restated: read-only everywhere except your one file; no game launch;
no game-directory write; no store text; no status moved; a source read is never
"tested"; skips by name. If a step is blocked, finish every other step and say
exactly what was blocked and why.
