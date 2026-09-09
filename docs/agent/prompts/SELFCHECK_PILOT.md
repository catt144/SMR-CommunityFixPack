# SELFCHECK PILOT — measure the sandbox in ONE real boot, read it, and author the prototype brief

Paste into a fresh Claude Code session **after hotfix-2 link 99 has returned its
verdict** and before the post-99 owner sitting, so the sitting's single boot
also serves this measurement. Do not run it while 99 is open: your one write
outside this prompt's own files is in the Test Kit, which 99 reads.

**Start with `git log --oneline -15`, `git pull`, `ListAgents`.** Read
`docs/agent/STATE.md` (mandatory), then **`agent/reports/SELFCHECK_PROMISE_COMBINED.md`
whole** (the reconciled read path; do not start from either original report),
then `agent/reports/SELFCHECK_PROMISE_CROSSCHECK_CODEX.md` → "Runtime reads
still owed" (the probes you will adapt), `agent/FIX_POLICY.md` §2/§2a, and
the Test Kit's `Code/00_TestCore.lua` (conventions), `95_AutoRun.lua`,
`96_AutoRunFlag.lua`, `98_EnablePathLeg.lua` (how a leg is armed and how the
enable path is exercised).

> 🎯 **THE JOB.** Everything the self-check work now rests on is one unmeasured
> fact: whether `string.dump` is callable from mod code inside `Mars.exe`.
> Every desk replica and binary read says yes; no boot has. You (1) build the
> measurement into the Test Kit, (2) hand the owner a five-line sitting script,
> (3) read the log they bring back, and (4) **author the next prompt** — the
> prototype brief if the route is open, the fallback brief if it is not.
> ⛔ You write NO pack code and NO store text. The pilot never touches `Code/`.

> ⚖️ **Why this is measured and not argued** (owner rule, `EF-078`): a source-read
> prediction of 6 self-disabled modules measured as 13. The whole plan is a
> source read until this boot.

## 0 · Bindings

- ⛔ `H-02` no Mod Editor, no `version` edit, no upload. `H-03` no portal API
  from a launched game. `H-04` never call a future release ready. `H-06`
  pre-copy autosaves before any save-load the sitting needs (this pilot needs
  NONE — it is menu-only). `H-09` no packed folder beside a live junction.
- ⛔ **You do not launch the game.** The owner does, in the sitting. Your
  deliverable is the chunk, the script, and the reading.
- ⛔ Read-only on `Code/`, `items.lua`, `metadata.lua`, `bugs/`, `facts/`,
  every `INDEX.md`, `STATE.md`. Your files: the Test Kit chunk (kit repo,
  local-only, no remote — commit there), `agent/reports/SELFCHECK_PILOT.md`,
  the successor prompt you author, one `PLAYTEST_CHECKLIST.md` entry under
  "Decisions waiting on you" (the sitting script; owner asks live there), and
  this prompt (delete it on close-out, chain rule 2).
- Several sessions edit the pack tree: `git status` before every commit,
  never touch a stranger's unstaged file, commit by explicit path, `git
  commit -F <file>`, push straight after. `python tools/doccheck.py` GREEN
  before any pack-doc commit; a WARN goes verbatim into your summary; the 18
  frozen-index `warn` lines are standing. STATE is at its byte warn — you do
  not write it; put the one-line STATE text in your report for its owner.
- ⛔ Never move a status; a source read is never `tested`; skips by name.
- **Live todo list**, one item per commit-and-verify unit; the owner reads it.

## 1 · Build the measurement chunk (the Test Kit)

The kit is a mod (`C:\Dev\SMR-BugFixPack-TestKit`, id
`SMR_CommunityFixPackTestKit`), so its code runs INSIDE the mod sandbox — the
only environment whose answer counts. ⚠️ A console line runs in the real `_G`
and would measure the wrong thing.

Create ONE new kit file (name it in the kit's numbering, e.g.
`Code/66_SelfcheckReads.lua`; check `items.lua` / whatever the kit uses to
list code files and follow it exactly — link 07 just reshaped the kit, so read
its close-out in `prompts/hotfix2/99_TERMINAL_AUDIT.md` "From link 07" first).
Register ONE probe via `SMRTest.Register(id, {title, kind = "behavior", fix,
run})` whose `run` prints every reading with `SMRTest.Print` under a fixed
prefix `[SelfcheckPilot]` and returns `"PASS"` when every reading printed (the
verdict is the log, not the status), plus a file-scope passive
`OnMsg.OnLuaError` handler that only prints. Adapt Codex's R1–R5 verbatim
logic (its report, "Runtime reads still owed") and add **R0**:

```lua
-- R0: does an explicit error() unwind under pcall inside mod code? The kit
-- recorded that error() REPORTS and continues (00_TestCore.lua:41-49). Every
-- "a throw is a decline" rule in the pack relies on pcall returning false.
local ok_err, msg_err = pcall(function() error("SelfcheckPilot-R0") return "continued" end)
SMRTest.Print("[SelfcheckPilot] R0 explicit_error_under_pcall ok=%s value=%s", tostring(ok_err), tostring(msg_err))
local ok_vm, msg_vm = pcall(function() local t = nil; return t.x end)
SMRTest.Print("[SelfcheckPilot] R0 vm_error_under_pcall ok=%s value=%s", tostring(ok_vm), tostring(msg_vm))
```

Rules for the chunk, all binding:
- **No game-state mutation, no thread, no `Msg` you raise, no file write, no
  portal call.** Every reading is a `type()`, a `pcall` of a pure call, or a
  `string.dump` of a function you hold. `LuaCodeToTuple` (R2) is called ONLY
  with scalar expressions and its results are printed, never retained.
- **Print, never return, the evidence.** Long hex goes out in chunks of ≤ 64
  bytes per line so the log stays readable; print the FULL dump header (the
  first 34 bytes) not 16.
- **Dump four pack-local controls** (zero-arg, one-arg, vararg, nested
  closure) before any engine function, so a parser can be validated against
  known shapes; then `LandscapeForEachUnit` and
  `Residence.CancelResidenceReservation` as reachability samples — and print
  `SMRTest.SourceOf(fn)` next to each if the kit's introspection works, or
  state that the sample may be a pack or other-mod replacement at kit load
  time (Codex's caveat: this proves reachability, never a pristine pin).
- **Run on BOTH paths**: cold boot with the kit and pack ticked, and the
  enable path (`98_EnablePathLeg.lua` shows how the kit exercises it). Print
  which path each reading came from (`DataLoaded`, `Loading`, and whether
  `GetPreGameMainMenu()` is up are cheap discriminators).
- `python tools/parsecheck.py` on the kit file; then run doccheck in the PACK
  repo (it parses the kit tree report-only) and quote its kit lines.

## 2 · Hand the owner the sitting (checklist entry, ≤ 6 lines)

Write ONE "Decisions waiting on you" entry: what to tick (pack + kit, opt-in
pack unticked per ck43), that it is menu-only (no save load, no autosave
risk), that the kit's autorun flag is armed (say exactly how, per
`96_AutoRunFlag.lua`), that they launch once cold and once via the enable path
(spell out the clicks), then exit and archive the two logs under
`docs/archive/logs/selfcheckpilot_<timestamp>.log` — and what they will SEE:
`[SelfcheckPilot]` lines in the log, nothing on screen except possibly one
engine box if R2's expression trips anything (it should not). Batch it with
the post-99 sitting's other asks; do not create a second sitting.

## 3 · Read the logs (after the owner's boot)

Write `agent/reports/SELFCHECK_PILOT.md`, verdict first. For each reading,
the decision table:

| reading | outcome → meaning |
|---|---|
| R1 `string.dump` type | `function` ⇒ route open. `nil` ⇒ **the fingerprint route is dead on this build**; the honest sentence is the process one (ck112(a)-shaped) and the successor prompt is the FALLBACK below. |
| R1 controls | all four decode to the expected `(numparams, is_vararg)` and the C control refuses ⇒ the arity check is buildable. Any control mis-decoding ⇒ the engine's dump layout is not stock; the successor must budget a format study before any parser. |
| R1 header | signature `\x1bLua`, version `0x53`, format `0`, `LUAC_DATA`, sizes, `0x5678`, `370.5` ⇒ stock 5.3. Anything else ⇒ record the bytes; parser design changes. |
| R0 | `explicit_error_under_pcall ok=false` ⇒ normal Lua; `ok=true value=continued` ⇒ the kit's fact holds for `error()` and every pack rule that reads "a throw is a decline" must be re-audited for explicit `error`/`assert` calls in shipped bodies (VM errors still unwind if the second line reads `ok=false`). |
| R2 `LuaCodeToTuple` | `true, nil, 42` with the explicit env ⇒ an indirect `load` exists inside the sandbox; `default_env_debug_type … table` ⇒ engine-environment access through it. **Owner decision** whether to report it to the developers; ⛔ never a foundation for the pack. Error or nil ⇒ route closed; say which. |
| R3 | source retrieval availability on a player-shaped install; empty/fallback is UNKNOWN, never equality. |
| R4 `GetStack` | tail wrapper absent, post wrapper present ⇒ the tail-call property holds in the engine's printer; otherwise job two's rule needs re-deriving. |
| R4 `OnLuaError` handler | only fires if an error happens; no event = no measurement. Record argument types if it did. |
| R5 `find_lower` | `2, nil, 1, 2` ⇒ plain substring; else the attribution mechanism is pattern-based and `EF-065` needs an addendum. |

Every line of the log with the prefix goes into the report verbatim (they are
short). Anything unexpected is a finding, not noise (`never silently discount a
log line`).

## 4 · Author the successor — this prompt's last act (chain rule: the next link is written by the one that has the data)

**If R1 says `function` and the header is stock:** write
`prompts/SELFCHECK_PROTOTYPE.md`, a bounded code link (post-99, its own
release cycle, on a feature branch), scoped to THREE modules —
`Fix_LandscapeUnitFilter` (F115), `Fix_TrainCargoDumping` (F114),
`Fix_StaleReservations` (F-2's callee) — implementing in `00_Core.lua`: (a) a
declarative install plan validated ALL-before-ANY-write with a receipt; (b)
the self-describing arity check; (c) exact-byte dependency pins over each
module's declared `Require` set, captured by a pin collector INSIDE the owning
module's apply before install, stored as Lua literals; (d) calibration
witnesses; (e) UNKNOWN declines. With: a desk harness through the REAL
`Require` (link 04b's pattern), `bodycheck`/`sigcheck`/`parsecheck` green, a
`--selftest` falsifier for the dump parser, the 1.0.7-tree false-stand-down
proxy (Codex's whole-chunk comparator, its report §Reproduction record) stated
as a proxy because 1.0.7 engine dumps cannot be collected, and NO wording
change in that link. Inbox: the R-readings, the seven X-corrections, the
`LuaCodeToTuple` result, and the three D7 multi-site modules
(`AnomalyCaveInMap`, `RocketInteractGuard`, `ArrivalDeaths`) as the
transaction's test cases.

**If R1 says `nil` (or the header is not stock and no cheap format study is
possible):** write `prompts/SELFCHECK_FALLBACK.md` for the text lane: the
process promise (Option 4) plus ck112(a)'s wording as the strongest true
sentence, the desk tools as the guarantee, and the owner decision that the
runtime route is closed on this build — with the evidence lines quoted.

Either way, close out: `git rm` this prompt, commit the report + the successor
+ the checklist entry by path, push; put the proposed STATE line in your
report; message any live sibling whose lane you touched.

## 5 · What "done" is

The kit chunk committed (kit repo) and parse-clean; the sitting entry on the
checklist; after the boot, `SELFCHECK_PILOT.md` with every reading verbatim
and each row of §3's table answered; the successor prompt authored on the
evidence; nothing run by you in a game; no pack code, no store text, no status
moved.

## Notes from upstream

*(From the Claude audit session, 2026-09-09, after the Codex cross-check.)*

- The four refutations and the D7 gap are in `SELFCHECK_PROMISE_COMBINED.md`
  §3; do not re-derive them, do carry them into the successor's inbox.
- The kit's own engine fact — `error()` reports and continues — was measured
  on 1.0.7 (`00_TestCore.lua:41-49`); R0 re-measures it on 1.1.0 because the
  probe form's "throw = decline" rule (`00_Core.lua:151-166`) and the
  prototype's UNKNOWN rule both depend on `pcall` semantics.
- Link 07 closed at `d254b88` and re-shaped the kit (probe count 100→94);
  read its outbox before adding a file, and follow whatever it settled for
  file listing and probe kinds.
- Peer sessions on 2026-09-09 were `smr-bugfixpack-26`, `-05`, `-0e`
  (on-call), `-ee` (07); `ListAgents` will show who is live when you start.
- The owner's open decisions from this work are consolidated in
  `SELFCHECK_PROMISE_COMBINED.md` §7; the pilot adds one (R2's report-to-devs
  question) only if R2 confirms the route.
