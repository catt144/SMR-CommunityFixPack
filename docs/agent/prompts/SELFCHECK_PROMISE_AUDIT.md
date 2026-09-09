# CAN WE MAKE THE PROMISE TRUE? — the self-check honesty audit
#### (and: stop being blamed for other mods' faults)

Paste into a fresh Claude Code session. **Runs in PARALLEL with the hotfix-2
chain** — read §5 before writing anything.
**Start with `git log --oneline -15` + `git pull`.** Read `docs/agent/STATE.md`
(mandatory), `docs/agent/FIX_POLICY.md` §2/§2a/§2b, and `Code/00_Core.lua`'s
`Require`.

> 🎯 **TWO JOBS, both about whether the pack's claims about itself are true.**
>
> **JOB ONE.** The store description promises:
>
> > *"Every fix checks the game's code before it touches anything, and stands
> > down by itself if an official patch changes what it was written for."*
>
> **Audit whether that can be made LITERALLY TRUE, and recommend how.**
>
> **JOB TWO (§1B).** Find a way for this pack to stop being blamed for OTHER
> mods' faults. Owner ask, and related: both jobs are about the gap between what
> the pack says about itself and what is so.
>
> ⛔ **You write NO code and NO store text.** You produce a report with costed
> options and a recommendation. The owner decides.

> ⚖️ **THE OWNER HAS REJECTED THE OBVIOUS TWO (ck112).** They do not want the
> sentence watered down to match a weak mechanism, and they do not want it
> deferred. They asked for a third option: **make the mechanism strong enough
> that the sentence is simply true.** Treat "reword it smaller" as a FALLBACK you
> must justify, not a default. ⛔ But if the honest answer is that it cannot be
> made fully true, **say so plainly with the evidence** — a scoped sentence the
> project can defend beats a bold one it cannot. That is a real result, not a
> failure.

## 0 · Why the promise is currently false, and by exactly how much

Game 1.1.0 broke two shipped fixes **in players' games** in one week. Both
reported `applied` and then threw:
- **`F114`** `Fix_TrainCargoDumping` — a BODY change at matching arity. 157
  throws in a 42-minute session. Found by a **player report**.
- **`F115`** `Fix_LandscapeUnitFilter` — a SIGNATURE change
  (`(mark, callback, ...)` → `(map, mark, callback, ...)`). Found by the owner
  **pressing a button**.

Neither "stood down." The runtime self-checks ask whether a target **exists** —
and in both cases it did. ⛔ **This is the defect behind the defects.**

⭐ **The mechanism the promise describes now EXISTS but is barely deployed.**
`Require` gained a behavioural **`probe`** form (`Code/00_Core.lua`; `FIX_POLICY`
§2a — the probe IS the branch guard, never a version check). Measured coverage as
of 2026-09-09, **re-derive these numbers yourself, do not inherit them**:

| check form | modules | what it actually proves |
|---|---|---|
| `probe` | **5** of 43 | the shipped body BEHAVES as the fix assumes ⇒ the promise is TRUE here |
| `global` / `class` / `path` | 39 | the target EXISTS ⇒ what over-promised |
| `test` | 7 | a content verdict about DATA, not about the target's behaviour |

⇒ **The promise holds for roughly 5 of 43 modules.** That is the gap. It is a
coverage problem with a working mechanism, not a wording problem — which is why
the owner's instinct to close it rather than soften it deserves a real answer.

## 1 · What you must establish (findings, not a checklist)

### 1a · Would today's mechanism have caught the two real failures?

⛔ **This is the load-bearing question and it must be answered from the code,
not from confidence.** `F115` now HAS a probe (link 04b, `799f145`) — a
behaviour probe of the shipped `LandscapeForEachUnit` on a stub map. That is
your CONTROL: it is a real probe against a real historical failure.
- Read it. Would it have declined on the 1.1.0 tree **before** the throw?
- Would an equivalent probe have caught `F114`'s nil-`demand` body change?
- ⚠️ Is `F115`'s probe detecting the SIGNATURE change, the STORAGE move, or the
  BEHAVIOUR? Those shipped together in 1.1.0; a probe that only catches the
  correlate would not catch the next one. The entry and the audit already flag
  this — verify it rather than repeating it.

### 1b · Can every surviving module get a probe? What does it cost?

For each of the 43, classify:
- **PROBEABLE** — a cheap, side-effect-free call on a stub can distinguish a
  body that behaves as assumed from one that does not. Sketch the probe in one
  line; do not write it.
- **UNPROBEABLE** — and say WHY, concretely. The probe form's own contract
  requires a stub that is both safe and discriminating; a target needing live
  game state, a map, a colonist, or a running thread may have neither.
- ⚠️ **Probes have real costs**: they run at load, inside `pcall`, on every
  boot, for every player. A probe with a side effect is a shipped bug. A probe
  that is wrong in the SAFE direction silently disables a working fix — ⭐ that
  failure mode already nearly happened (`EF-078`: a name-checked path spec made
  a desk audit wrong by 5, in the direction that disables).

### 1c · Is there a UNIVERSAL mechanism, cheaper than 43 hand-written probes?

⛔ **Establish what the mod sandbox actually permits — measure, do not assume.**
The boot log records `no debug.getinfo (mod sandbox)`, which is why arity cannot
be read at runtime. Check, from the shipped engine source and from
`ModEnvBlacklist`:
- Is `debug.getinfo` genuinely absent, or just absent in one context?
- Is `string.dump` reachable? If a function's bytecode can be hashed at runtime,
  a **fingerprint of the shipped body** baked in at authoring time and compared
  at load would make the promise true for EVERY module in one stroke.
  ⚠️ Bytecode is not stable across engine builds — would a mismatch mean "the
  game changed" or "the game recompiled"? A fingerprint that false-positives on
  every patch is worse than no check.
- The pack already carries a **`SRC:`/`DEFECT:` manifest** on all surviving
  modules and `tools/bodycheck.py` compares bodies at DESK time. Can any of that
  reach runtime, or is desk-time the only place body comparison can live?
- ⭐ **If body comparison can only ever be desk-time, that is itself the answer**
  — and it reframes the promise: the honest claim becomes about what the project
  does every patch, not what the code does at boot. Cost that route too.

### 1c-bis · ⚠️ A PEER AGENT'S SPOT CHECK — be aware of it, do NOT trust it

Another session ran a quick source read of this exact question and reached a
provisional position. ⛔ **It is a SOURCE READ, never executed in a game**, and
this project's standing rule is to trust runtime over source reads. Treat it as
a starting point and a set of claims to falsify — **not** as a finding, and not
as a reason to skip §1c. The owner passed it on precisely so you are not
surprised by it. Its claims, verbatim in substance:

- **The obvious route is closed.** `debug` is blacklisted on 1.1.0
  (`Mod.lua:1436`), re-verified on THIS branch rather than trusting `EF-006`'s
  1.0.7 reading. So `debug.getinfo`'s `nparams`/`isvararg` — which would have
  caught `F115`'s arity change automatically, at runtime, in the player's game —
  is unavailable.
- **But a non-obvious one may be open.** The blacklist is checked on the
  TOP-LEVEL GLOBAL NAME only: `ModEnvMeta.__index` does
  `if env_blacklist[key] then return end` and otherwise returns
  `rawget(original_G, key)` — the real table, whole. `string` is not on that
  list. ⇒ **`string.dump` may reach mod code**, and it is the one runtime
  primitive that can see a BODY change, which `Require` structurally cannot.
- **Two things it says you must confront up front or you will build the wrong
  thing:**
  1. ⛔ **A pinned dump-hash could stand the WHOLE PACK down at once.** If a Lua
     compiler or engine-build change flips every hash simultaneously, the pack
     self-disables on a patch that broke nothing. **That failure is worse than
     the gap it closes.**
  2. ⛔ **Even a perfect version does not make the sentence fully true.** Class
     (c) — semantics moving under a wrapper whose target BODY is untouched — is
     invisible to body hashing **by definition**, and **6 of the 10 FIX rows in
     the 1.1.0 re-verification were class (c)**.

⭐ **What THIS session adds, and it is existence-only:** the citations were
spot-checked and are real — the blacklist table does contain `debug = true`,
`env_blacklist[key]` gating exists (`Mod.lua:1560`, `:1571`), and `string` does
not appear in that table. ⛔ **That verifies the citations EXIST. It verifies
NOTHING about the conclusion** — whether `string.dump` actually resolves inside
a loaded mod's environment, and what it returns for an engine C function versus a
Lua function, is exactly the kind of thing this project has been wrong about
from source reads twice this week. **Measure it in a running game or say you
could not.**

### 1d · What can the sentence honestly say under each route?

Draft the wording that would be TRUE under each option — full probe coverage,
partial coverage, fingerprinting, desk-time-only. ⛔ Draft, do not commit; `06_TEXT`
owns store wording and `metadata.lua`. ⚠️ Route-check every claim: "every fix
checks" must be true of EVERY fix, or the word "every" goes. The project
overturned a player-facing line three reviews had passed because nobody walked
the steps.

## 1B · JOB TWO — stop OUR mod being blamed for OTHER mods' problems

⚖️ **Owner ask, 2026-09-09: "find a way for our mod to not be blamed for other
mods' problems. We have seen that a few times."** The owner judges this related
to job one, and it is: both are about whether the pack's claims about itself are
true. ⛔ Treat it as a first-class job, not an appendix.

⭐ **A STARTING POINT, source-read by the session that wrote this brief — verify
it, do not inherit it.** The engine's attribution is a SUBSTRING MATCH over the
call stack (`CommonLua/Modding/Mod.lua:3018-3028`), and its own comment calls it
a *"rough estimation based on call stack"*:

```lua
function OnMsg.OnLuaError(err, stack, os_paths)
    for _, mod in ipairs(ModsLoaded) do
        local path = mod.content_path
        ...
        if string.find_lower(err, path) or string.find_lower(stack, path) then
            ReportModLuaError(mod, err, stack)
```

⇒ **ANY mod whose content path appears ANYWHERE in the error or the stack is
flagged.** We wrap ~39 game functions, so a throw originating in another mod
that passes through one of our wrappers puts our path in the stack and names us.
That is `EF-065`(a) with a mechanism attached. Two aggravating details to check:
- `ReportedMods[mod.id]` (`:2980-2983`) means a mod is reported **once per
  session** — so the FIRST such error names us for the whole session, and
  nothing later can un-name us.
- `ModsToReport` is a LIST and `mods_str` joins titles with newlines, so the
  dialog can name several mods at once. ⇒ Is being named ALONE actually common,
  or do we usually appear beside the real culprit? **That changes how bad this
  is, and it is measurable from the archived logs.**

**What to establish:**
1. **How often is this real?** Search the archived logs for `Error in mod` lines
   naming us, and for each decide from the stack whether the fault was ours.
   ⛔ "Not caused by our leg" is an attribution verdict, not a dismissal — show
   the reasoning per line. ⚠️ If every historical instance WAS ours (`F114`,
   `F115` both were), say so: the owner's "we have seen that a few times" would
   then be about a risk rather than a measured harm, and that changes the
   priority. Do not tell them what they expect to hear.
2. **Can our frame leave the stack?** ⭐ A hypothesis from this brief's author,
   UNVERIFIED and possibly wrong: Lua's proper tail call (`return orig(...)`)
   REPLACES the caller's frame, so a wrapper that tail-calls the original may
   not appear in a downstream stack at all. If that holds it is a cheap,
   mechanical mitigation for every PRE-wrapper. ⛔ It cannot help a POST-wrapper
   (one that does work after the original returns), and most of the pack's
   wrappers are post-wrappers — establish the split before recommending it.
3. **What else is available?** Does the engine expose anything that scopes
   attribution? Does load order change who is named first? Does the dedupe make
   an early benign appearance costly?
4. ⛔ **What must NOT be done.** Swallowing another mod's error to keep our name
   out of the stack would hide a real fault from the player and is off the
   table. Any mitigation must leave the error reported and the real culprit
   nameable. Say so in your report so nobody later reads your recommendation as
   permission to catch-and-drop.
5. **Is there a player-facing half?** If we cannot stop being named, can we make
   it cheap to tell — a log line the owner or a player can point at that says
   what our wrapper saw? ⚠️ Route-check it: who would actually read it, on which
   platform, and how would they be told to.

## 2 · The options to cost, and you may propose others

1. **Probe everything probeable, and scope the sentence to that.**
2. **Probe everything, accepting some probes are weak.** ⛔ A weak probe that
   passes is worse than no probe: it converts "we do not check" into "we
   checked", which is exactly the failure `F114` shipped under.
3. **A universal runtime fingerprint**, if §1c finds one is possible.
4. **Move the guarantee to process** — the compatibility pass every update,
   backed by `bodycheck`/`sigcheck`/`parsecheck` — and make the sentence a
   promise about the project rather than the code.
5. **Reword smaller** (the rejected ck112(a)). ⛔ Only with evidence the others
   cannot work.

For each: what it makes true, what it costs to build, what it costs at runtime,
what it costs per future module, and how it fails.

## 3 · Deliverable

`agent/reports/SELFCHECK_PROMISE_AUDIT.md`:
1. **VERDICT, first line: CAN the sentence be made literally true — YES / YES
   BUT SCOPED / NO.** Then one paragraph of why.
2. The measured coverage table, re-derived.
3. §1a answered against both real failures, with the `F115` probe as the control.
4. The 43-module PROBEABLE / UNPROBEABLE classification.
5. §1c's sandbox findings, with the evidence for each.
6. Costed options and **a recommendation**.
7. Draft wordings, one per route.
8. **JOB TWO, as its own section:** how often we have actually been misblamed
   (from the archived logs, per line, with the reasoning shown), whether a
   tail-call or anything else can keep our frame out of a downstream stack, what
   is available beyond that, and a recommendation. ⛔ Include the "what must NOT
   be done" line so nobody later reads it as permission to swallow errors.
9. ⛔ **What you did NOT check, named.** A module you did not open is not a
   module that passed — treating silence as a pass is precisely how `F114`
   shipped.

⚠️ **ON SIZE — decide this after §1a/§1b and say what you decided.** A peer
suggested `CHAIN_METHOD` rather than one session, and two jobs over 43 modules
plus a sandbox measurement may well exceed one. **Checkpoint (commit + push)
after each of: §1a, §1b, §1c, §1B.** If you run low, ⛔ do NOT rush a thin
verdict — stop, and author the continuation prompt naming exactly what is done
and what is not (`reports/CHAIN_METHOD.md`). A partial audit that says so is
worth more than a complete-looking one that guessed the rest.

## 4 · Bindings

- ⛔ **Read-only on `Code/`, `metadata.lua`, and all store text.** You recommend;
  you do not implement. If you find something urgent, write it up and say so.
- ⛔ `H-02` no Mod Editor, no `version` edit, **no upload**. `H-03` no portal API
  from a launched game. `H-04` never call a future release ready.
- ⛔ Never modify the game directory. 1.1.0 truth is
  `A:\SteamLibrary\steamapps\common\Project Spark\ModTools\Src`; the 1.0.7 tree
  is ARCHIVED at `C:\Dev\SMR-SrcArchive\1.0.7.396349\Src` — ⭐ **you CAN diff the
  branches now**, which earlier sessions could not.
- ⛔ Never move a status you did not witness; a source read is never `tested`.
- ⛔ Never silently discount a log line.
- `python tools/doccheck.py` GREEN before any doc commit; a WARN goes **verbatim**
  into your summary. Commits `git commit -F <file>`, then push.
- Use the tools rather than hand-rolling: `sigcheck.py` (arity, `--coverage`),
  `bodycheck.py` (body drift), `parsecheck.py`, `logscan.py`. ⛔ An instrument
  being green never means the code was checked — that conflation is what `F114`
  shipped under.

## 5 · Parallel-running rules — the chain is LIVE

Hotfix-2 links **06, 07, 99** are pending and other sessions are active.
⛔ **`ListAgents` and `git log` before you write anything.**

**Yours alone:** `agent/reports/SELFCHECK_PROMISE_AUDIT.md`, and this prompt.
**⛔ NOT yours:** any `Code/*.lua`, `items.lua`, `metadata.lua`, `bugs/*.md`,
`prompts/hotfix2/*`, `STATE.md`, `PLAYTEST_CHECKLIST.md`.

If your findings need a checklist decision or a STATE line, ⛔ **do not write
them** — put the proposed text in your report and tell the owner, so the chain's
owners land it in their own files. `git pull` before your commit and push
straight after. Message overlapping sessions rather than assuming a file is idle.

⚠️ **You may be recommending work on modules the chain is actively editing.**
Say what you read and at which commit, so a later reader can tell whether your
classification predates a change.

## 6 · What "done" is

A verdict the owner can act on, coverage re-derived rather than inherited, both
real failures tested against the current mechanism, a per-module classification,
sandbox limits established by measurement, **job two answered with its own
evidence**, costed options with a recommendation, and an explicit list of what
you did not check. ⛔ No code, no store text, no
status moved. ⭐ **"It cannot be made fully true, and here is the strongest thing
that is" is a valid and useful verdict** — provided it is evidenced, not assumed.
