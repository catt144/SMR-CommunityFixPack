# smrtk 07 — the documentation, the standing slot prompt, and 08's preparation

Link 07 of `smrtk`. **Codex / Sol, high** (owner's fifth ruling in the manifest; rule 22). README rules 1–22 are yours. After 03B has closed (read its outbox first — it carries the verified
button lists per page, the stubs still owed, and the owner items already consolidated into ck175).

## Job A — the rules the owner asked for ("we need rules about cheats in the documentation")

1. **`agent/WORKFLOW.md` § "Cheats on playtest saves"** — append a dated block: the toolkit replaces the vanilla menu
   for playtesting; `[SMRTK] SMRTK_<Verb>` lines are **intentional test actions, attributed by construction — never
   ask the owner about one**; a vanilla `ObjCheat`/`Cheat` marker in a NEW log is now the exception worth one
   question; the **taint** strip is the detector for a tainted save. The separate
   eligibility field is `UNAVAILABLE:sandbox` on this build (`EF-096`), never OK
   inferred from no taint. Cite `EF-095`.
2. **`agent/WORKFLOW.md` § "Writing in a shared tree"** or the reading path — one line: `80_AgentSlots.lua` is
   agent-owned, rewritten per sitting, never edited by a build link.
3. **`docs/PLAYTEST_HELP.md`** — replace § "Cheating without contaminating results" and amend § "Console: what works…"
   with the panel: plain numbered steps (memory: player-facing steps must be plain), the hotkey, each page in one
   line each, F9, the console behavior actually witnessed at 02, and the things the panel cannot do (clear an
   achievement — `EF-094`; run code from a string or read vanilla's eligibility verdict — `EF-096`). Retire the "load with the console open" workaround
   wherever it is written (grep `console` across `docs/` including `archive/` on purpose; do not edit the archive).
4. **`C:\Dev\SMR-BugFixPack-TestKit\README.md`** — the panel section, the file map, the slot contract.
5. **`prompts/perma/SMRTK_SLOTS.md`** — the standing prompt an agent fires to **pre-load a sitting**: read the sitting's
   brief, write `80_AgentSlots.lua` (legs as slots: MARK → set up → act → DUMP → MARK), write the predictions, hand
   the owner one line: "start the game; the Agent tab is loaded". Add its row to `prompts/README.md` `perma/` table.
6. **`agent/FIX_POLICY.md`** — nothing; the toolkit is not a fix. Say so in 99's inbox if you were tempted.

## Job B — 08's preparation

7. **Predictions** `reports/SMRTK_FULL_SITTING_PREDICTIONS.md` — numbered, per button class (not per button): the
   log line expected, and for the stamp (03B's outbox, from P5's for-07 section) the placed/skipped counts predicted from a dry run.
8. **08's script** into `08_FULL_SITTING_owner.md`'s inbox per rule 13: every page, one representative of each button
   class, a Delete and a Destroy on scratch buildings, a save/load round trip through slot A with the guard tripped
   once on purpose, one trigger firing, one screenshot+mark opened afterwards, one capture + stamp, a run-until.
   Price it in minutes. The fixture: a 1.1.0 colony with a dome, a depot, a drone hub and a rocket in flight.

Document **what was built** (03B's outbox carries the DEPARTURES) — never the plan's defaults where the build
differed. Your own SUGGESTIONS section is wanted too: a doc that is hard to write plainly is usually a button that
is hard to explain, and that is a finding for 99.

## Scope fence

IN: the files named above. OUT: any code (route a defect found while documenting to the link's grave + 99's inbox and
fix it only if it is a one-line label).

## What may NOT be claimed

That any documented behaviour was seen in play — 08 sees it; write "as built" not "as tested".

## Close-out

`python tools/doccheck.py` GREEN (PROMPT MAP gate: the new perma row + file land together). Commit per unit.
Outbox to 08 and 99; strike your row; `git rm` this file; push.

## Notes from upstream

- **01 correction, 2026-09-13:** `CanUnlockAchievement` is blacklisted; the
  actual strip separates CLEAN/TAINTED from eligibility unavailable. Document
  that limitation, not an invented eligibility OK. Read 01's predictions
  §DEPARTURES/§SUGGESTIONS; Ctrl-Shift-F11 is the built hotkey. 02 still owns all
  in-game verdicts. The legacy console bootstrap remains until judged after 02.

### 03B judge outbox, 2026-09-13

**Verdict PASS WITH FIXES** (`reports/SMRTK_JUDGE.md`). Every 03A gate re-ran
identically at pack `2be7c73` / TestKit `cee5bab`. All 54 P1 and all 21 P2
actions were opened against source: every one calls a clean leaf, none of
`EF-098`'s 13, no wrapper. Idle vanilla patches: **zero** (only `print_tee` and
`quiet`, both toggles with matching uninstalls). Cross-ids all resolve; no stub
is owed. Rules 6, 7, 9, 10, 11 hold, measured independently of 03A's harness.
TestKit is now `87f3130` — I changed one label, nothing else.

**Six things you must get right in the docs:**

1. **Do not write "replaces the cheat menu" unqualified.** The Selected section
   offers **22 of the 106** `Cheat*`/`AsyncCheat*` member names vanilla's
   section would offer, and vanilla's section is unreachable while the toolkit
   is loaded (`config.BuildingInfopanelCheats` is never set). On a Colonist the
   section shows only Delete. Document the real coverage. ck175 item 1 asks the
   owner whether to extend before 08; write to whichever way it is ruled.
2. **08 must prove the console with `console_control`, never with "the console
   opened."** `00_TestCore.lua:529` arms the console at mod load, so a passive
   observation attributes nothing to the toolkit. 02's discriminating A/B
   (`ConsoleEnabled` false -> rebuild -> `console=false`; arm -> `console=true`)
   is the pattern; `SMRTK_SKELETON_SITTING.md:416-439`.
3. **The 00 bootstrap edit I ruled but did not apply** (03A handed me the
   retirement question; I ruled **invert, do not retire**):
   `00_TestCore.lua:519` calls `ConsoleSetEnabled(true)` first, which is the one
   spelling rule 10 forbids, because it also calls `ShowConsoleLog` and forces
   the on-screen overlay every boot. Swap the order — plain
   `ConsoleEnabled = true` first, `ConsoleSetEnabled` as the fallback. Both
   fallbacks stay (a binding really did die once, 2026-07-25). `Mars.exe`
   closed, then re-gate.
4. **P5's stamp gate is a required 08 leg, not optional.** 03A substituted three
   synthetic zero-mutation plans for the brief's three native stamps; that was
   forced (no link before 08 may launch the game), so the gate moved rather than
   was waived. Write native fit, GameInit, dome membership, connected grids and
   upgrade state into the script as named witnesses.
5. **Fix the manifest's own control recipe.** `prompts/smrtk/README.md`
   "Derived facts" says `grep -c "NetSyncEvent"` on `CheatDef.lua` gives 13. It
   gives **26** (13 calls + 13 `Comment =` lines naming the function), so the
   recipe is vacuous as a control. Key it on the call form instead.
6. **Two `EF-096` corrections, both small, both mine.** `ModEnvBlacklist` spans
   `Mod.lua:1280-1441`, not 1280-1416. And `os` **is** blacklisted, but
   `LuaModEnv` rawsets `env.os = { time = os.time }` at `Mod.lua:1618` before
   attaching the metatable — so `os.time` is available to a mod (P4 relies on it
   for its session nonce) and nothing else on `os` is. The naive read of the
   blacklist says the opposite; record it so nobody "fixes" working code.

**A documentation-only nuance, not a defect:** `quiet` and `90_Loggers`'
DustDevils logger both wrap `_G.GenerateDustDevilIn`. Both toolkit directions
refuse the nesting (`72:130-138`, `76:117`). The unguarded path is a bare
console `SMRTest.Log.DustDevils(true)` while quiet is armed, which would strand
quiet's wrapper. Tell an operator to disarm quiet before touching loggers from
the console.

03A's own for-07 outbox (button tables, emitted registries, the P3 slot
template, P4's preflight contract, P5's 08 recipe) stands unchanged — I found
nothing wrong in it.

**From 03C (Codex, 2026-09-14), TestKit `f093e3b`:** Selected extension BUILT,
source-derived only; no launch. Report + executable source-census/desk instrument:
`reports/SMRTK_03C_EXTEND.md`. This supersedes 03B's item-1 coverage wording:
installed build 24995074 still has 106 names (94 Cheat + 12 AsyncCheat); coverage
is 22 curated names + 84 More names (72 Cheat + 12 AsyncCheat), source-name
capacity **106/106**. Named taint skips: none on this build. Conditional omission:
`CheatAddDustRC` when `CheatAddDust` is also supported, because the preserved
curated Add Dust row selects its first alternative; the all-methods fixture has
105 method buttons, while an RC-only fixture exposes AddDustRC. Do not claim
106 simultaneous buttons, in-play safety, retail debug availability, or that the
section replaces the whole cheat menu.

More mirrors vanilla's instance/metatable/__index table walk and calls the leaf
through `T.Run("selected_more", expected_obj, method)`. The callback re-enumerates
and refuses curated methods (no depot-guard bypass), unsupported methods and
changed selection. More Cheat uses P2's existing game-time thread; More AsyncCheat
uses a real-time thread. Both check selection after queuing and retain the core
result logger and post-leaf taint assertion. Labels are grouped; More buttons
use one full-width column and method rollovers. No global writes, vanilla function
patches, probes, pack runtime edits or checklist writes were added.

Verification: P2 desk PASS + 03C desk PASS (exact Colonist Kill / Drone Despawn
source bodies with fake services, 84 More/12 async, inheritance/overrides,
refusals, errors, taint-positive control, category threads and queued races).
Parse: 34 TestKit files, 0 errors; pack doccheck GREEN. Rule 6: **0 lines across
9 toolkit files**; rule 7: **0 lines**; source presence **26 lines / 13 calls**.

OWNER-ROUTED for 07: ck175 item 1 is built on the proven P2 leaf route. No new
owner decision or extra boot requested; 08 is first contact. Include More Cheat
(Kill/Despawn), More AsyncCheat (Inspect), stale-selection refusal, long labels /
scrolling and taint witnesses in the existing sitting. Properties opens an editor:
close it and distinguish transient editor eligibility blocking from taint.
Eligibility remains `UNAVAILABLE:sandbox`. Deferred vanilla work is not proved
complete by the dispatch return record.

DRIFT for 99: a colon-method-only census misses six generated upgrades; P2's old
CATALOG proxy has a function __index, so its 21+4 output cannot measure More;
README Ordering omitted 03C (corrected). My first report-fence command matched
its own inline marker and executed no code with exit 0; the fixed, line-anchored
extractor emitted every census/PASS witness. Prior upstream messages are historical;
use this outbox for the resulting Selected surface. No RE-FIRE or new sitting.
