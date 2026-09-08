# SAFETY_FIRST_FIXES — get the pack safe on game 1.1.0 (one-off build brief, written 2026-09-08)

Paste into a fresh Claude Code session. **Any model; the owner picks.**
Staleness anchor: **written 2026-09-08**, the day 1.1.0 shipped. **Start with
`git log --oneline -10` + `git pull`** and verify every specific below against
the tree before trusting it.

> 🎯 **SCOPE, AND IT IS NARROW ON PURPOSE.** Stop the pack doing active harm on
> game 1.1.0. Four items, below. ⛔ **NOTHING ELSE.** You are not re-deriving
> defects, not retiring fixes, not auditing the body-copies, not uploading.
> Everything outside §2 is decision **99**/**101** and the "fix later" tier in
> `reports/GAME_1_1_0_AUDIT.md` §4.

> ⚖️ **THE EVIDENCE RULE (owner, 2026-09-08), which binds you too.** A patch note
> that says "Fixed" is a **CLAIM, false until we confirm it ourselves.** And the
> same applies to *this document*: it was written by the session that found these
> defects, so it is an interested party. **Re-derive each claim before you act on
> it** — every one has its file and line below precisely so you can.

## 0 · Orient (before you touch anything)

1. `git log --oneline -10` + `git pull`.
2. Read `docs/agent/STATE.md` (mandatory), then
   `reports/GAME_1_1_0_AUDIT.md` §2–3 and `reports/GAME_1_1_0_IMPACT.md` §6b.
3. Entries: `bugs/F111.md`, `bugs/F112.md`, `bugs/F113.md`, `bugs/F114.md`.
   Facts: `EF-075`, `EF-076`, `EF-077`.
4. **Put every §2 item in your todo list as its own entry, immediately, and
   update it as you go** — the owner reads that list to decide when to step in.
5. ⚠️ **STALE-PROBE GATE** binds only if you launch the retail game (item A may
   want to): `grep -rln "TEMPORARY" Code/ ../SMR-BugFixPack-TestKit/Code/`,
   CLEAN = zero hits. It was clean at writing.
6. `tasklist | grep -i Mars` — **`Mars.exe` must NOT be running** before you edit
   loadable code, checked in a step of its own.

## 1 · The bindings you cannot bend

- ⛔ **Never modify the game directory.** `ModTools\Src` is read-only truth —
  and it is now **1.1.0** source (`EF-075`); the 1.0.7 base is gone from disk, so
  ⛔ **never "correct" a 1.0.7 citation in an existing entry to match it.**
- **Parse-sweep every Lua change**: `python` + `from luaparser import ast;
  ast.parse(open(p,encoding='utf-8').read())`. A change that does not parse does
  not get committed.
- **`python tools/doccheck.py` GREEN before any doc commit.** Counts come from
  `--emit-counts`, never hand-typed. `STATE.md` is byte-capped and currently
  ~10 bytes under the warn line — **adding a line means evicting one** in the
  same commit (`prompts/STATE_EVICTION.md`).
- ⛔ **`H-02`** — never open the Mod Editor, never hand-set `version`.
  **No upload. No version bump.** Three gated modules do not justify a release
  cycle, and the owner has ruled post-release is patch-note maintenance.
- ✅ **`H-10` is NOT engaged**: no module is added, renamed or dropped, so
  `items.lua` is untouched. Confirm that stays true.
- **Commits**: `git commit -F <file>` (embedded quotes split under PS 5.1),
  then **push** — standing-allowed.
- ⛔ **PS 5.1 mangles the repo's no-BOM UTF-8 docs.** Use the Edit tool or
  `[System.IO.File]` with `UTF8Encoding($false)`; never
  `Get-Content`/`Set-Content` on a doc.

## 2 · The work

### A · F114 — the live field report. **DO THIS FIRST.**

⭐ The only item here a **real player has actually hit.** Steam comment,
2026-09-08, reporter *Ranger Dimitri*, verbatim:

> "Think something broke in the update when it came to the Train's with this mod.
> Using this mod cause them to not move between stations. When I turn it off they
> work as normal."

That is a **player-run A/B naming our mod as the difference** — the strongest
evidence class short of our own repro. Read `bugs/F114.md` for the full entry.

⚠️ **Three constraints, so you do not waste the session:**
1. **The reporter cannot narrow it and must not be asked to.** All 80 modules are
   **default-active**; `SMRFixPack.OptionEnabled` gates only *optional* ones
   (`Code/00_Core.lua:54-58`, `doccheck`: "0 optional-gated files"). There is no
   player toggle to bisect with.
2. **Game version is 1.1.0 by the reporter's framing only** ("broke in the
   update") — not confirmed. No save, no log, no mod list yet.
3. ⛔ **DO NOT RE-DERIVE WHAT IS ALREADY CLEARED.** Two suspects were chased on
   2026-09-08 and eliminated; re-doing them is the obvious time sink:
   - `Fix_TrainMinors`' `recompute_max_vehicles` — **cleared**, its formula is
     byte-identical to 1.1.0's own (`Lua/Buildings/Track.lua:65`).
   - `Fix_TrackConnectorPingPong`'s `CreateConnectorElements` — **cleared as a
     copy**, it matches 1.1.0's `TrackConnectedObjBase:CreateConnectorElements`
     (`Lua/TrainTransport.lua`) line for line apart from its own F66 guard.
   ⚠️ One thread left explicitly OPEN there, and it is where to start
   instrumenting rather than the answer: our F66 guard declines to take a hex
   owned by a live other station, and in that branch `el` stays valid so the
   creation block is skipped — meaning **that station gets no connector element
   at that spot**, where vanilla always destroys and recreates. Whether 1.1.0
   reaches that branch more often (it changed station–dome connection, and
   `TrackBase:GameInit` ends with `self:Notify("TryConnectStations")`,
   `Track.lua:62-67`) is **unmeasured**.

⛔ Every sweep this project owns — `EF-076` existence, the call-site sweep — is
**CLEAN on all 11 train/track modules.** A player found a breakage our
instruments cannot see. Treat "the sweeps are clean" as saying nothing about
behaviour.

⛔ **DO NOT SHIP A REPAIR FOR THIS IN THIS SESSION.** No cause is known, every
desk sweep passed clean on the train/track modules, and a speculative fix would
be exactly the "plausible story instead of a control" the project forbids. Your
job is **narrowing**, and stopping when you have it:

1. **Try to reproduce on 1.1.0** — two stations, a track, trains assigned; run
   with the pack on, then off. Cheap, needs no reporter. Record what you did
   precisely enough that a failure to reproduce is itself informative.
2. If it reproduces, **bisect the 11 train/track modules** (listed in `F114.md`)
   agent-side. ⛔ `H-08`: never bisect by pulling the junction — that costs the
   enable and only the owner can restore it.
3. **Write up whatever you find in `bugs/F114.md`** — including "did not
   reproduce", which is a result. ⛔ Claim no cause you have not pinned.
4. Draft (do **not** send) a reply asking for their **log** and **save + mod
   list**, for the owner to send. The boot block lists applied fixes and any
   self-disable; `EF-065`(a) blames any throw. Route the tracker via
   `api.github.com/.../issues/<n>/comments`, never the HTML page.

### B · F113 — stop the hourly throw (P1)

**Re-derive first:** `GetEarthExportResPossibleReward` absent tree-wide;
1.1.0's tail is `if self:GetEarthAutomodeFundingState() == "blocked" then`
(`Lua/UniversalRocket.lua:2028+`); our call sits at
`Code/Fix_LanderCargoRatchet.lua:186` inside a **full body replacement**
installed at `:130`.

**Change — add one spec to that module's `Require` list (`:78-93`):**

```lua
{ class = "UniversalRocketBase", method = "GetEarthExportResPossibleReward",
  reason = "the Earth export-reward query is gone (game update changed it?)" },
```

**Why this and not a repair of the call.** It restores the pack's designed
failure mode: decline to install rather than install a body that raises — and it
also stops the module reverting a function 1.1.0 rewrote, which a targeted call
repair would leave in place. ⛔ **Do not swap in `GetEarthAutomodeFundingState`.**
⚠️ Use the `{class, method}` form, **not** `{ test = … }`: `Require` sets
`update_suspect` on shape failures and deliberately not on `test` entries, and
this *is* patch rot that should be flagged.

### C · F111 — stop the boolean-index throw (P2)

**Re-derive first:** `Workplace:IsOvertime` collapses `self.overtime` from a
per-shift table to a boolean (`Lua/Buildings/Workplace.lua:718-729`);
`GetWorkersPerformance` calls it (`:263`); our `staffed_performance` still writes
`self.overtime[shift]` and runs **after** `orig`.

**Change — one line, `Code/Fix_ExtractorStaffedPerformance.lua:68`:**

```lua
-- was:  if self.overtime and self.overtime[shift] then
if type(self.overtime) == "table" and self.overtime[shift] then
```

⭐ **Assumption-free** — correct whether `self.overtime` is a table (1.0.7) or a
boolean (1.1.0), needs no version detection, changes no outcome on either.
⛔ Do **not** also retire the module here, even though the audit confirms 1.1.0
fixed F108's defect upstream (`Max(GetWorkersPerformance(shift),
auto_performance)`, `:283-287`). Retirement is decision 99.

### D · F112 — stop the silent over-payment (P2)

**Re-derive first:** `law_scale` has **0 hits tree-wide**;
`automation_workforce_reduction` survives only in `Data/LawDef/`; the three
automation laws still carry `Prop = "max_workers"`
(`LawDef-Technology.lua:14`, `:107`, `:194`); and C39 still returns 0 for
Factory/ResearchBuilding/Service as "already paid by the shipped gate"
(`Code/Fix_AutomationLawCompensation.lua:179-182`) — a gate that no longer
exists.

**Change — add to that module's `Require` list so it self-disables on 1.1.0:**

```lua
{ test = function()
        -- C39 corrects an asymmetry in vanilla's law_scale compensation.
        -- 1.1.0 deleted that compensation outright while the laws still cut
        -- max_workers, so paying the out-of-class families would CREATE the
        -- asymmetry this fix exists to remove.
        local W = rawget(_G, "Workplace")
        return not (type(W) == "table" and type(W.GetWorkersPerformance) == "function")
    end,
  reason = "vanilla no longer compensates the automation-law worker cut for anyone (1.1.0) — nothing to correct" },
```

`test` is right here (unlike B): this is an "already handled?" content check,
which is what `Require` reserves `test` for, and it correctly does **not** raise
`update_suspect` — the module going quiet is healthy, not rot.

⚠️ **THE ONE ASSUMPTION IN THIS BRIEF, AND YOU MUST CARRY IT FORWARD.** The
discriminator assumes 1.1.0 *extracted* the per-worker loop into
`Workplace:GetWorkersPerformance` and that 1.0.7 had it inline — inferred from
our own F108 header (which cites the loop inline at 1.0.7's
`Workplace.lua:219-228`) and **not verifiable, because the 1.0.7 source is gone**.
Bounded downside if wrong: C39 also self-disables on 1.0.7, returning those
players to vanilla's known asymmetry — the pre-fix state, not a new harm.
**Write this assumption into the module's comment block** and re-check it the
moment a 1.0.7 branch exists (decision 98).

## 3 · Verify

1. **Parse-sweep** all three changed files.
2. **`python tools/doccheck.py` GREEN**, and `--emit-counts` unchanged — 80
   modules / 81 files / 100 probes. **A count that moved means you did something
   outside scope; stop and say so.**
3. ⚠️ **The real control is runtime and it is worth asking the owner for:** boot
   1.1.0 with the pack and read the `fix pack present: N/N` line +
   `SMRFixPack.ListFixes()`. Expect `Fix_LanderCargoRatchet` and
   `Fix_AutomationLawCompensation` to report **inactive with their reasons**, and
   the six already-predicted self-disables (F09, F12, F22, F81, F94, F55/F57) to
   join them ⇒ **8 inactive**. ⛔ Counts are READ, never assumed — if the live
   number disagrees with 8, the source-read model is wrong and that is a finding,
   not a nuisance.
4. If you cannot get a runtime read, say so plainly and do not imply otherwise.

## 4 · Close out

- `bugs/F111.md`, `F112.md`, `F113.md`: record what landed. ⛔ Status stays
  **`filed`** unless you got the runtime read — a source-read repair is not
  `fixed`, and `tested-*` needs an attended witness.
- `bugs/F114.md`: your narrowing result, whatever it is.
- `STATE.md` only if the kernel changed — and **evict in the same commit**.
- A leg in `archive/SESSION_LOG.md` (append-only, newest first).
- **Owner-facing:** anything needing a ruling goes to `PLAYTEST_CHECKLIST.md` →
  "Decisions waiting on you", never only an agent doc. A `doccheck` WARN is
  copied **verbatim** into your summary.
- `doccheck` GREEN → `git commit -F <file>` → **push**.

## 5 · What "done" is

Trains investigated and written up (**not** speculatively fixed); three modules
gated or guarded so the pack's failure mode on 1.1.0 is silence rather than
throwing or silently rebalancing; counts unchanged; nothing shipped; the fix-later
tier untouched and still listed in `reports/GAME_1_1_0_AUDIT.md` §4.

⛔ **If you find yourself re-deriving a defect, retiring a fix, editing
`metadata.lua`, or preparing an upload — stop. That is not this brief.**
