# Handoff: migration and hub work after TheGodUncle's save (2026-09-24)

Single use. Authored at `536db7d` by the session that ran the migration audit, its cross-check,
the hub audit and the two sittings on the reporter's save. `git rm` this file and its map row in
the commit that lands the last item below, or earlier if the owner retires it. Start with
`git log --oneline -8`, `git pull`, `git status --short`; peers commit concurrently and Codex
seats are invisible to `ListAgents`, so commit by pathspec only. Open a live todo list before
your first write.

## Where the facts are

Read in this order, only as far as the item you take needs:

1. [HUB_FIELD_FINDINGS_2026-09-24.md](../reports/HUB_FIELD_FINDINGS_2026-09-24.md): the
   measured chain on the reporter's save, both runs, with the archived logs and the mod's code.
   This is the settled explanation of the Steam report.
2. [MIGRATION_AUDIT_2026-09-24.md](../reports/MIGRATION_AUDIT_2026-09-24.md), its four seat
   notes (`_A_native`, `_B_diff`, `_C_pack`, `_D_hubs`), and the Codex
   [cross-check](../reports/MIGRATION_CROSSCHECK_2026-09-24.md). Owner rulings live in the
   audit's §4 table: N4 no fix, N5 intended.
3. Entries filed from them: C109 to C113 (migration audit) and C114 to C117 (hub audit), each
   corrected by the cross-check or the resweep.

Causation, as the owner has it: every defect on the migration and hub surface is vanilla 1.1.1,
unchanged since 1.1.0; Passage Network 1.38 adds exposure only (jobs and services network-wide,
so more hub crossings) and its residue hypothesis is refuted. Overturn only on evidence.

## Remaining work, in order

1. **Done.** The Codex resweep landed at `032dd0d`:
   [MIGRATION_CROSSCHECK_HUB_RESWEEP_2026-09-24.md](../reports/MIGRATION_CROSSCHECK_HUB_RESWEEP_2026-09-24.md).
   It holds the causation answer, narrows S1's wrapper to four guards, reverses the C111 drop, and
   corrects four statements in the field findings (appended there as §7).
2. **Done.** S1, S2, S3 and S5 are filed as [C114](../bugs/C114.md), [C115](../bugs/C115.md),
   [C116](../bugs/C116.md) and [C117](../bugs/C117.md). §7 and resweep corrections are folded into
   C42, C99, C109 and C111 as dated sections.
3. **Decide with the owner whether P1 to P6** (the pack's own items, audit §4.2 and cross-check
   ranking) become F entries. P2 and P3 ruled 2026-09-24: both fixed in the hub set (P2 filed as F127,
   P3 tracked in item 5). P1, P4, P5 and P6 are unruled and tracked only in the reports.
4. **Reporter reply** for the Steam thread, when the owner asks: not his mods, not ours; the
   game measures reach from the centre of a radius-19 dome, rescue rides home are what the
   status shows, deaths come from the pickup anchored back at the hub. Do not call Passage
   Network abandoned; it was updated 2026-09-18. `docs/FIELD_REPORT_REPLIES.md` holds the
   reply rules and the standing ruling on naming other mods.
5. **One release for the hub set (owner ruling, 2026-09-24).** C114, C115, C116, C117, C42,
   C111, [F127](../bugs/F127.md) (was P2) and the P3 pins ship together, never one at a time. The owner's words: "If possible and we are going to fix
   them all I would like to do the fixes and get them out all at once. They all touch surfaces near
   the same thing so if we push one part people read that as fixed, and then if they hit the surface
   of one of the other parts then they say 'well you said it was fixed but X is still borken'". The
   release process ships whatever is in the tree, so no part of the set may reach `Code/` or
   `metadata.lua` on `main` before the whole set is ready. How to hold it (a branch, or files kept
   out of the code list) is the building seat's call. Membership, owner 2026-09-24: P2 and P3 are
   in ("if p3 is just makeing something better we already ship or correcting it and its ready to go
   we shoul,d just add it same with p2"); C99 is out, never reproduced in game. F127 needs its
   full-destination branch validated before the repair. P3 is the two missing `SRC:` pins in
   `Fix_VacuumWalks` (`GetNextMigrationLeg`, `IsInWalkingDistDome`), header metadata only. If a
   sitting refutes a member, there is no standing rule (owner, 2026-09-24: "it depends on the
   circumstances and information"): stop and bring the owner the sitting's facts, what the member
   still covers, and what dropping or holding would ship; the owner decides case by case.
   Build order: the owner approved S1 first; the resweep ranks C114, C115, C117, C116, then C42, with
   F127 and P3 inside the set and the C109 sitting diagnostic only. The owner has not chosen
   between the two orders. C114 and C116 cannot be built before the hub-footprint measurement
   (item 6); C115 needs the anchor read; C117 needs its salvage control. C110 and C113 still wait on
   an intent ruling.
6. **Owed measurements**, all on the reporter's save (the owner holds it; do not ask the
   reporter for anything more): the S4 hex-footprint test (35 of 45 held units stood beyond hub
   2692's collision radius); the S2 anchor read on a dying colonist
   (`transport_task.source_landing_site[1]` on a passage hex); the two phase 2b controls in
   `PLAYTEST_PLAN_1.1.1_2026-09-23.md`.
7. **Site-form issues 2 and 3** (the "switched itself off" dialog naming the vacuum-walk fix).
   **Corrected 2026-09-24: the Dome-global hypothesis is not refuted.** `SMRDOME` was read in game,
   after the class rebuild, and in the mods-on run the pack's code ran before Passage Network's (ON:95
   before ON:136; queue at ON:186); the mods-off run did not load it. If Passage Network loads first, its stray `function Dome()` is the live global
   when VacuumWalks' `has_110_helpers` runs, so the fix declines and flags itself; VacuumWalks is
   the only module that reads `Dome` at load. Code load order is the enable order
   (`Mod.lua:1907-1994`, `ModManager.lua:35-37`, archived 1.1.1.405907). Owner sitting pending:
   turn the pack and Passage Network off, enable Passage Network first, then the pack. Expect
   `VacuumWalks: inactive (the shipped emigration code has no work-slot reservation or shuttle
   landing slots; …)` and the dialog; `applied` refutes it. Range-changing mods tripping the
   threshold-gap test remain the second lead. Codex's load-order cross-check
   ([LOAD_ORDER_CROSSCHECK_2026-09-24.md](../reports/LOAD_ORDER_CROSSCHECK_2026-09-24.md), `4361a55`)
   reproduced the decline on the desk in both orders and names the narrow repair: look up the
   retained `Dome` declaration through `ProcessClassdefChildren` (`CommonLua/Core/classes.lua:1265`,
   1.1.1.405907) instead of the transient global. Its load-order levers (saved-order promotion,
   metadata bootstrap) are not in any release: the owner will ship a load-order change with fixes
   only if its route is low risk with minimal testing (2026-09-24). Owner, 2026-09-24: "For the load order we
   will decide how and what we implement after the fixes are done." Nothing on load order before
   the hub set is built.
8. **Owner's side idea, not filed:** a foreign-mod probe kit that on load checks class globals
   are tables, lists which mod replaced which pack target, and dumps residue like the `SMRNET`
   line. Route to `docs/FUTURE_IDEAS.md` if the owner wants it kept.

## Stops

Report instead of continuing when: a verdict needs a game run (name the sitting); an
engine-side claim cannot be decided from Lua (mark unproven with its measurement); the paths
you must write carry uncommitted foreign changes (ask the owner).
