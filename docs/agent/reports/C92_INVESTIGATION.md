# C92 investigation - hidden Underground Exploitation requirement

2026-09-13. Investigation only; no fix module, achievement award, research
mutation or shipped Lua change. Defect truth: [C92](../bugs/C92.md).

**MEASURED:** The supplied Sol 490 save fails the vanilla achievement predicate
solely on `UndergroundExploitation`, a hidden, unresearched ordinary Tech in
`Underground_1`. Both repeatables have completed once and retain `researched`.
Excluding repeatables still fails; excluding that one hidden preset passes.

## Provenance and limits

- **Owner authority:** The owner personally loaded the reporter's original,
  verified all non-repeatable technologies complete in the tree, and verified
  a clean original save with no mods on the current patch. This is accepted,
  not re-derived. A hidden requirement reconciles that check with the failure.
- **MEASURED:** Original: `C:\Users\stkot\Downloads\Autosave Sol 490.savegame.sav`;
  SHA256 `68d340ad0f1a2b13047034e21a7fc84199c66f069858f190be1e9f38d0ff9bb7`.
  Only a byte copy named `C92READ.savegame.sav` was loaded.
- **MEASURED:** Retail `1.1.0.403908`, DLCs norman + thomas, day 490, Japan,
  3 tech points, no game rules. These reads ran with the normal rig's Test Kit,
  Fix Pack and Opt-In Pack loaded. They establish live state and the predicate
  barrier, not an unmodded in-game award attempt on the reporter's account.
- **MEASURED:** Owner account `GetAchievementFlags("ResearchedAllTechs")=true`.
  This is account state, not save state or evidence the reporter was awarded it.
  The diagnostic never called the achievement handler or `AchievementUnlock`.
- **SOURCE + desk control:** `python tools/desk_c92_achievement.py` executes
  shipped preset data, iterator, completion/state methods, `Player:UIResearch`
  and the achievement listener. The unlock sink only records requests.
  It prints HEAD, version, body locations and hashes. Synthetic completion
  flags are declared; no claim it recreates the reporter's colony.
  [Retained desk output](../../archive/c92_desk_20260913.txt): all named demands
  held, including the incomplete-ordinary and never-completed-repeatable controls.

## Retained game transcripts

| leg | result | transcript |
|---|---|---|
| MEASURED r1, prep `1053bf3` | save loaded; census stopped at a diagnostic formatting error | [r1](../../archive/c92_read_r1_Mars.exe-20260913-03.49.24.log) |
| MEASURED r2, prep `2a7e596` | census completed; hidden Tech was the sole failed counted requirement | [r2](../../archive/c92_read_r2_Mars.exe-20260913-03.50.53.log) |
| MEASURED r3, prep `4586e9d` | confirmed failed normal reveal/research route; compared proposed filters read-only | [r3](../../archive/c92_read_r3_Mars.exe-20260913-03.53.17.log) |

**MEASURED r1 diagnostic error**, at process Lua age 45.353 s, caught by pcall:

```text
[mod] [C92READ] CENSUS ok=false result=CommonLua/Core/localization.lua:501: invalid value (table) at index 1 in table for 'concat'
```

Cause pinned: `ModsLoaded` contains mod tables; the diagnostic tried to
`table.concat` them. r2/r3 log each `mod.id` and complete. This error invalidates
r1's unfinished census, not r2/r3's successful independent loads.

**MEASURED unexplained boot diagnostics**, recurring before the save census,
around Lua age 19-20 s in each transcript (wording below from r3):

```text
[Braze] SessionStart error The server name or address could not be resolved
[Braze] Failed sending launcher ev The server name or address could not be resolved
[Braze] Failed to init
```

No attribution of these lines to C92 or dismissal as harmless. The archived logs
retain both repetitions and their timestamps. The existing Opt-In NoHomeless
self-check warning is also retained with its subsequent `applied` line; it was
not changed in this investigation.

## Solution options for the fix agent

| option | evidence and tradeoff |
|---|---|
| INFERRED recommendation: exempt only this unreachable hidden preset in the achievement's predicate | r3's read-only comparison passes. Preserve all other requirements, including each repeatable's first completion, and the existing tracked-group list. Scope the exemption to the shipped orphan shape; decline when a vendor change supplies a normal route. |
| INFERRED alternative: make Underground Exploitation a normal accessible tech | Repairs reachability instead of the achievement filter, but exposes the authored 20% underground-production benefit and changes gameplay. It needs a real placement/prerequisite design; simply setting a researched flag is not a repair. |
| SOURCE rejected: exempt repeatables | r3 still fails on the hidden ordinary Tech. It also drops their existing first-completion requirement. |
| SOURCE risk: ignore every currently hidden tech, or set this preset Obsolete | Hidden ordinary techs can be legitimate future requirements. Obsolete changes the shared preset iterator and all its consumers, rather than the achievement alone. Avoid these broad changes. |

**SOURCE patch seam:** The vanilla filter and group list are file locals in
`Lua/Achievements.lua`; a mod cannot assign that local filter by name. A focused
additional achievement listener can evaluate the existing groups with the narrow
exemption and call the engine's normal `AchievementUnlock`, preserving the vanilla
listener and other sponsor achievements. Do not globally redefine
`IsTechResearched` or `Research:IsTechGroupResearched` to manufacture completion.
The declaring class for the latter is `Research`, not `Colony`.

**SOURCE recovery trap:** The vanilla listener returns on `not first_time`
(`Achievements.lua:21-23`). In this save both repeatables have already completed
once. Merely correcting a filter while retaining that event gate leaves the
reporter without a remaining ordinary first completion. A fix must specify its
recovery trigger: a repeat research event may re-evaluate the corrected predicate,
and/or a properly ordered post-load check may award already eligible colonies.
The engine's own account/platform/tutorial/rule restrictions still apply.

**INFERRED acceptance demands:** On a copy, confirm that the corrected predicate
accepts this completed save; still refuses a never-completed repeatable and a
missing ordinary tech; and re-evaluates an already-completed colony without
forcing a tech flag. Check behavioral decline on the frozen 1.0.7 branch and on
a hypothetical vendor repair that connects/reveals this preset. A live award
outcome needs an eligible account; the owner's already-unlocked account cannot
witness a first award for this achievement.

Terraforming's omission from the vanilla list is separate scope. Adding it
would strengthen the requirement and does not repair this blocker. No scope
decision or player reply is requested by this investigation.

## Close-out

**MEASURED:** Each process quit normally before log capture and disarm. The kit
returned to its original metadata bytes; the arming helper's removal of the
existing disarmed ForceInactive comment was explicitly reversed after verifying
that it was the only delta. The temporary Code payload and staged save are gone.

**MEASURED:** Before any load, all autosaves were backed up to
`C:\Dev\SMR-C92-Evidence-20260913`. SHA256 comparisons after the final run show
`Autosave Sol 490.savegame.sav`, `Autosave Sol 56.savegame.sav` and
`Autosave Sol 6.savegame.sav` unchanged. The Downloads original and its pre-existing
import in Saved Games remain byte-identical. No save was written by the diagnostic.
