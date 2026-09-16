# Wildfire Cure — find the cause, build the fix

**Authored 2026-09-16 against `481bbd7`.** Game baseline **1.1.0.403908** + DLC.
⛔ Start with `git log --oneline -10` and `git pull`. Every specific below is dated to that
commit; if a cited file moved, the record wins and this brief is stale.

> ⛔ **FIRING FREEZE.** `prompts/README.md` carries the owner's 2026-09-15 freeze on this folder.
> **Do not fire this brief until the owner lifts it in words.** No agent lifts, narrows or
> excepts it — not even for this.

---

## 0 · The job, in the owner's words

> *"I want you to write up a research prompt for wildfire, minimal restrictions, give it the
> evidence… Let it explore freely and creatively, it is also allowed to launch the game if it
> wants to. I would prefer it find the cause and the fix end to end. We have so much on our
> plate right now that playtesting is a luxury if we can avoid it and be reasonably sure we did
> our job that is the best outcome."*

**You have unusual licence here.** Explore however you think best. Launch the retail game if it
helps. Write throwaway probes. Follow a hunch this brief never mentions. The deliverable is a
**cause and a fix**, not a tour of the evidence below.

⭐ **Reaching a confident answer WITHOUT an owner playtest is the best outcome**, and is
explicitly what the owner is asking for. Owner attention is the scarce resource. Desk proof,
a TestKit probe, or your own launched session all beat booking a sitting. ⛔ But do not buy
that by overclaiming — see §6.

## 1 · The report (INHERITED, not verified)

Steam, **Jäger**, 2026-09-14, owner-relayed. Same reporter as [C99](../bugs/C99.md), different bug:

> *"I seem to be having an issue with the Wildfire Mystery, there is no option to research the
> cure in the new tech tree."*

⛔ No log, no save, no mod list, no sol count, no statement of how far the mystery had run.
⛔ **Do not ask the reporter for a save.** Owner ruling 2026-09-15: players are uncomfortable
sharing saves and non-technical users find the request confusing. Exhaust source, the kit and
your own game first; a save is a last resort and is the owner's call to make, not yours.

## 2 · Already established — ⛔ DO NOT RE-DERIVE

All measured 2026-09-15/16 on **1.1.0.403908**, live tree
`A:\SteamLibrary\steamapps\common\Project Spark\ModTools\Src`, archived 1.0.7 tree
`C:\Dev\SMR-SrcArchive\1.0.7.396349\Src` (`EF-083`).

| # | fact | how measured | falsifier |
|---|---|---|---|
| F1 | Wildfire is **Mystery 8**, class `TheMarsBug` (`Lua/Mysteries/TheMarsBug.lua`, 21 lines, data only — no tech/lock/research code) | read whole file | `grep -niE "tech\|lock\|research" Lua/Mysteries/TheMarsBug.lua` returns a hit |
| F2 | **1.0.7 had ONE `WildfireCure` tech; 1.1.0 has ELEVEN** (`WildfireCure`, `_1`…`_10`) | `grep -c WildfireCure` both trees; `Data/Tech.lua` **does not exist** in 1.0.7 (that tree has `TechFieldPreset`/`TechGroup`/`TechPreset`) | find `Data/Tech.lua` in the 1.0.7 archive |
| F3 | All 11 carry `LockState = "hidden"`, `Unknown = true`, `group = "Mysteries"`, and a `MapPos` | `grep -B24 'id = "WildfireCure' Data/Tech.lua` | a family member without `LockState = "hidden"` |
| F4 | The chain is authored as neighbour links: `_1`→`_2`, middles→both sides, `_10`→`_9` **and** →`WildfireCure`; the final's only link is back to `_10` | read each `RequireTech` block | a `RequireTech` that contradicts that shape |
| F5 | Reveal path: `Data/Scenario/Mystery 8.lua:112-115` `SA_RevealTech{tech="WildfireCure", cost=90000}` → `MysteryTechRevealRemapping` (`Lua/Sequences/SA_Gameplay.lua:1188-1195`) rewrites the target to **`WildfireCure_1`** → `SA_RevealTech:SAExec` (`:1197`) → `Research:SetTechDiscovered` (`Lua/Research.lua:140`) → `UnlockTech` (`Lua/TechTree.lua:1275`) → `baseUnlockTech` (captured `:1274`) → CommonLua `UnlockTech` (`CommonLua/Libs/Research/Research.lua:31`) → `UnhideTech` + clears both `locked` reasons | read each hop | any hop resolving elsewhere |
| F6 | Map visibility is `GetTechState(id, UIPlayer) ~= "hidden"` (`Lua/TechTree.lua:434`); `GetTechState` returns the **stored** lock state via `GetPresetLockStateAndText`, and `GamePresetLockStateAndText` (`CommonLua/Features/LockablePreset.lua:339`) is a pass-through that **is not overridden anywhere** | `grep -rn GamePresetLockStateAndText` — only its definition and 4 call sites | an override anywhere in the tree |
| F7 | `Tech:CheckUnlockPrerequisites` (`Lua/TechTree.lua:443`) needs at least one **connected** tech researched for any tech with links and no `StartingNode`; **only ONE tech in all of `Data/Tech.lua` has `StartingNode`**, and no Wildfire tech does. It gates `UnhideUnlockedTechs` (`:182`, bound to `LockablePresetsStateInit` + `PostLoadGame`) and the lock re-evaluation (`LockablePreset.lua:165`) — **but the scenario reveal bypasses it** by clearing the reasons directly | read both call sites | a third caller, or a `StartingNode` in the family |
| F8 | ⭐ **`Research:ChangeResearchCost(tech_id, points)` NEVER READS `points`** — its whole body is `BoostTech(tech_id, 20)` (`Lua/Research.lua:225-227`). Wildfire's authored `cost = 90000` is discarded | read the function | the body doing anything with `points` |
| F9 | ⭐ **1.1.0 has no "in progress" research state.** `Player:UIResearch` spends `const.TechPointResearchCost = 1` and completes instantly; `ResearchQueueChange` fires 8× in 1.0.7 and **0×** in 1.1.0; `research_queue` is never written | inherited from [C69](../bugs/C69.md)'s terminal audit (`reports/vanillahunt/HUNT_AUDIT.md` §3) | a 1.1.0 write to `research_queue` |
| F10 | **The chain rewiring is COMPLETE.** Exactly five tech families have `_N` chains — `WildfireCure`(10), `BottomlessPitResearchCenter`(3), `AncientArtifactAdaptedMachine`(3), `AlienDiggersDestruction`(3), `AlienDiggersDetection`(2) — and `MysteryTechRevealRemapping` holds exactly those five | enumerated both sets | a chained family absent from the table, or vice versa |
| F11 | **9 of 11 mysteries gate on `SA_WaitResearch`** (Mysteries 1,2,3,4,5,6,8,10,11); **39** `"Researched"` waits tree-wide, and only **ONE** `"In Progress"` wait exists (Mystery 5 = C69's scope) | `grep -rc` over `Data/Scenario/` | a different count |
| F12 | ⭐ **`SA_GrantTechBoost` special-cases exactly one tech in the whole file** — `if self.Research == "WildfireCure"` (`SA_Gameplay.lua:824`) — completing the next unresearched `_N` outright via `UIColony:SetTechResearched`. This is the "medical buildings advance the cure" mechanic | `grep -n 'self.Research == ' SA_Gameplay.lua` → 3 hits, one is this | a second tech-specific branch |
| F13 | **Nothing in our pack touches this.** `grep -rilE "UnlockTech\|UnhideTech\|SetTechDiscovered\|GetTechState\|RevealTech\|TechTree\|CheckUnlockPrerequisites\|MysteryTechReveal" Code/` → one file, `Fix_GeneForging.lua:70`, and the hit is **inside a comment** | rerun the grep | a hit outside a comment |

⛔ **`git diff --stat 481bbd7..HEAD -- docs/agent/bugs/ Code/`** empty ⇒ none of the repo-side
facts needs re-reading. The game-tree facts re-verify only if the game updated (`EF-075` route).

## 3 · Hypotheses already RAISED AND KILLED — ⛔ do not re-run

1. **"The chain head's prerequisites are inverted."** `WildfireCure_1`'s only link points *forward*
   to `_2`, so `CheckUnlockPrerequisites` can never pass for it. **Killed:** the scenario reveal
   clears both lock reasons directly (F5), bypassing that gate entirely. The forward link is by
   design — the reveal is meant to be the only opener.
2. **"The reveal fails silently because `UnlockTech` early-returns."** `UnlockTech` returns false
   when `IsTechUnlocked` is already true, and `SA_RevealTech` swallows that in a retail-disabled
   `assert`. **Killed:** `IsTechUnlocked` is `state == "enabled" or "researched"` (`Lua/Tech.lua:504-507`)
   and a hidden tech is neither, so it does not early-return.
3. **"Wildfire was missed when the devs rewired mysteries for the new tree."** **Killed by F10** —
   five chained families, five remapping entries, exact match.
4. **"The research-model change silently broke every mystery's gating."** **Killed by F11** — the
   dead `"In Progress"` state is used exactly once, in Mystery 5.

⭐ Each refutation states what it depends on; if you overturn one, say which dependency broke.

## 4 · The open question

**The reveal path reads as sound, yet the player reports no researchable cure.** Pick it up
wherever you like. Leads, in no order and none authoritative:

- **Upstream — does the sequence ever reach the reveal?** `SA_RevealTech` sits behind
  `SA_RunSequence "Rocket To Earth"`, `SA_RunSequence "Earth Infected Timeout"` and an
  `SA_WaitMarsTime` of `10800000` + `rand 3600000` (`Mystery 8.lua:100-111`). A stuck prior step,
  or a player simply looking early, both produce the symptom.
- **The `Field` mismatch.** `Mystery 8.lua:147-151` waits with `'Field', "Special"` while the 1.1.0
  techs carry `group = "Mysteries"`. Does anything still read `Field`?
- ⭐ **The bespoke advancement (F12) against the new research model (F9).** A 10-step chain whose
  steps are completed by building medical buildings, authored when research took time, now running
  where research is instant and costs one tech point. What happens to `_1` when the player has no
  tech point? What does `Unknown = true` render as on the map?
- **`SetTechResearched` → `UIResearch(tech_id, "force")`** (`Lua/Research.lua:147`) — does forcing a
  *hidden* tech researched leave the chain in a state the UI will not offer?
- **The tech-point economy itself.** If the cure node is visible but unaffordable, "no option to
  research" is what a player would say.
- ⭐ **Consider that the player may be right about the symptom and wrong about the cause**, exactly
  as the C98 reporter was. The absence of an *option* may be an absence of a *point*, a hidden node,
  a node off-screen at its `MapPos`, or a node the UI filters.

## 5 · Scope

**IN:** the Wildfire cure's availability, end to end — cause, and a fix if one is ours to make.
Neighbouring mystery-research defects if your route runs through them.

**OUT, and route rather than fix:** [C79](../bugs/C79.md) already owns F8 (reveal costs discarded);
[C69](../bugs/C69.md) owns F9; [C92](../bugs/C92.md) owns a hidden unreachable tech;
[C97](../bugs/C97.md) §Finding 5 owns the orphaned-contract shape. ⛔ **Finding something there does
not authorize fixing it** — add evidence to that entry and say so in your report.

⭐ **If the cause turns out to be a CLASS** spanning those entries, say so loudly and propose where
the class should live. The owner surfaced that possibility and it is a live reading, not a tidy-up.

## 6 · Evidence bar — what you may NOT claim

- ⛔ **Never state a fix works because the source says so.** Say what you ran. If you did not run it,
  the claim is "source-derived, unexercised" — the project ships those (F116/F117/F118) but labels
  them honestly.
- ⛔ **"Not reproduced" is not "refuted."** "Refuted" requires the condition was SAMPLED.
- ⛔ **No absence claim from a truncated grep.** Count the presence side.
- ⛔ **A count is not a finding** — check where each hit landed.
- ⛔ **Do not claim the player's specific game is explained** unless you can tie your mechanism to
  their words. A plausible mechanism that produces the same sentence is a candidate, not a cause.
- ⭐ **The owner wants confidence without a playtest. Earn it or say you could not.** A narrower true
  statement beats a broad claim you cannot support — and "I found the mechanism, it needs one sitting
  to confirm" is a perfectly good result.

## 7 · Deliverable

1. **A defect entry** in `docs/agent/bugs/` (or amendments to the existing entries in §5 if it turns
   out to be theirs). Route: the `smr-bug-library` skill. Derive the next id/seq/row **from the files
   on disk**, and note `docs/archive/bugs/` holds archived numbers that must never be reused.
2. **A fix**, if the defect is ours to repair — `FIX_POLICY.md` governs: §4a who-benefits, §3a
   save-safety, §2 enable-path/declaring-class, §2a behaviour probe never a version check, §2b
   `-- SRC:`/`-- DEFECT:` headers. `python tools/parsecheck.py` before you trust any Lua.
3. **A short report** in `docs/agent/reports/` if the investigation is worth more than the entry holds
   — especially the negative results, which are what stop the next session repeating you.
4. `python tools/doccheck.py` **GREEN** before any commit; commit with an explicit pathspec
   (`git commit -F <msgfile> -- <paths>`), never `-a`, never a bare `-m`.

## 8 · Stop conditions — permission to report instead of pushing on

Stop and write up when any of these is true. None is a failure.

- You have the cause and the fix. **Done — that is the target.**
- You have the cause but the fix is a **design call** (restore content? change pacing?) → file it and
  route the call to the owner via `docs/PLAYTEST_CHECKLIST.md` → "Decisions waiting on you".
- The cause needs evidence only a live colony can give, and your own launched game cannot reach it.
- The trail leads wholly into C69/C79/C92's territory → add evidence there and stop.
- ⛔ You find yourself about to ask the reporter for anything → stop and report instead (§1).

## 9 · Read path — by file, not folder

**Game:** `Data/Scenario/Mystery 8.lua` · `Lua/Sequences/SA_Gameplay.lua` · `Data/Tech.lua`
(WildfireCure family) · `Lua/TechTree.lua` · `Lua/Research.lua` · `Lua/Tech.lua` ·
`CommonLua/Libs/Research/Research.lua` · `CommonLua/Features/LockablePreset.lua` ·
`Lua/Mysteries/TheMarsBug.lua`.

**Repo:** this brief · `bugs/C69.md`, `C79.md`, `C92.md` (read the sections you need, not the files
whole) · `FIX_POLICY.md` · `agent/WORKFLOW.md`.

**Discovery:** `rg -n <term> docs/agent/bugs/INDEX.md` and `docs/agent/facts/INDEX.md` — ⛔ grep the
fact index, never read it whole (43 KB). Archived 1.0.7-era records are behind the root `.rgignore`:
`rg <term> docs/archive/bugs/` reaches them on purpose.

## 10 · If you launch the game

You may. ⛔ **Never modify the game directory or the source archives** — read-only truth.
Check `Mars.exe` is not running (`tasklist`) before touching loadable code, as a separate step from
the edit. Before a run that records a reading, sweep for temporary probe code:
`grep -rln "TEMPORARY" Code/ ../SMR-BugFixPack-TestKit/Code/` — CLEAN is zero hits, or every hit
declared by your own design. Per ck184 this is an age/warranting-change trigger, **not** a refusal
gate: it does not block you and no agent overrides the owner with it.
Console reads: check names against the retail sandbox (`EF-096`); `ConsolePrint` silently rejects
multiple or non-string arguments; prefer a bare expression for a simple read, `*r` for real-time or
multi-statement work, `*g` for game-time work that yields. TestKit is local-only by design.

## 11 · Progress list — required before you execute

Open a live list covering the **whole** job, one item per commit-and-verify unit, exactly one in
progress. Split a stage the moment it splits; rewrite the list when reality changes; keep useful
state in the item text. ⛔ Do not carry several commits under one item or update it only at the end.
The owner reads this list to decide whether to step in.

A starting shape, not a constraint:

1. Orient: `git log`/`git pull`, read §2–§4, confirm the §2 facts still hold.
2. Reproduce the player's view — decide whether the cure node is hidden, visible-but-locked, or
   visible-but-unaffordable. Say which, with evidence.
3. Trace the cause to a named line.
4. Decide ours / not ours / class, and route per §5.
5. File the entry.
6. Build the fix, parse-check, desk-exercise it.
7. Report — including every negative result.

## 12 · Lifecycle

⛔ **One-off. When fired and consumed, `git rm` this file AND delete its row from
`prompts/README.md` in the same commit** (owner ruling 2026-09-13, checklist 174: the map lists live
prompts only, no tombstones). The outcome lives in the entry and the report; the grave is
`git log --diff-filter=D -- docs/agent/prompts/`.
