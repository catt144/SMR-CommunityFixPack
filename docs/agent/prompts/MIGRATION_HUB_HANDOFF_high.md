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
3. Entries filed from them: C109 to C113 (`docs/agent/bugs/`), each corrected by the cross-check.

Causation, as the owner has it: every defect on the migration and hub surface is vanilla 1.1.1,
unchanged since 1.1.0; Passage Network 1.38 adds exposure only (jobs and services network-wide,
so more hub crossings) and its residue hypothesis is refuted. Overturn only on evidence.

## Remaining work, in order

1. **Codex resweep of the cross-check with the new facts.** The prompt to paste into that seat
   is in the last section of this file. It reports only; it does not file. Wait for its report
   before item 2, so one seat edits the entries.
2. **File the hub audit's S1, S2, S3 and S5 as candidates** and fold its §7 corrections into
   C42, C99, C109 and C111. Use `smr-bug-library` and `doc-editing`; copy C109's shape; continue
   `seq` from the index. S1 is the centre-measured local access (help text at
   `Lua/__const.lua:1944-1949` says "outside their Dome", code measures to the centre); S2 the
   rescue pickup anchored where the interrupt landed; S3 the hub marker cleared only on a dome
   exit; S5 salvage disconnecting a hub passage with colonists inside. Cite the archived
   `1.1.1.405907` tree; the hub note's line numbers are 1.1.1 (its header explains the one-line
   offset from the brief's 1.1.0 anchors).
3. **Decide with the owner whether P1 to P6** (the pack's own items, audit §4.2 and cross-check
   ranking) become F entries. Owner has not ruled; they are tracked only in the reports.
4. **Reporter reply** for the Steam thread, when the owner asks: not his mods, not ours; the
   game measures reach from the centre of a radius-19 dome, rescue rides home are what the
   status shows, deaths come from the pickup anchored back at the hub. Do not call Passage
   Network abandoned; it was updated 2026-09-18. `docs/FIELD_REPORT_REPLIES.md` holds the
   reply rules and the standing ruling on naming other mods.
5. **Fix order, owner-approved in principle, nothing built yet:** S1 first (wrap
   `Colonist:HasLocalAccess` to grant access when the colonist stands on a hub or in a passage
   whose `dome_network` contains the destination's dome; check what it changes for work range,
   services and stations before building); then P3 (manifest pins for the two wrapped bodies)
   and P2 (the arrival reroute's orphan reservation) per the cross-check; then a C109 diagnostic
   sitting before any bypass; C110 and C113 wait on an intent ruling; C111 is cosmetic and the
   owner may still want it since it is the whole of symptom (a).
6. **Owed measurements**, all on the reporter's save (the owner holds it; do not ask the
   reporter for anything more): the S4 hex-footprint test (35 of 45 held units stood beyond hub
   2692's collision radius); the S2 anchor read on a dying colonist
   (`transport_task.source_landing_site[1]` on a passage hex); the two phase 2b controls in
   `PLAYTEST_PLAN_1.1.1_2026-09-23.md`.
7. **Still open, unexplained:** site-form issues 2 and 3 (the "switched itself off" dialog
   naming the vacuum-walk fix). The Dome-global hypothesis is refuted (`SMRDOME` read). It needs
   the reporters' logs; the module's decline reasons are tabled in the pack seat note's field
   section. Range-changing mods tripping the threshold-gap test remain the lead.
8. **Owner's side idea, not filed:** a foreign-mod probe kit that on load checks class globals
   are tables, lists which mod replaced which pack target, and dumps residue like the `SMRNET`
   line. Route to `docs/FUTURE_IDEAS.md` if the owner wants it kept.

## Stops

Report instead of continuing when: a verdict needs a game run (name the sitting); an
engine-side claim cannot be decided from Lua (mark unproven with its measurement); the paths
you must write carry uncommitted foreign changes (ask the owner).

## The resweep prompt for the Codex seat

Paste verbatim:

```
Resweep your migration cross-check (docs/agent/reports/MIGRATION_CROSSCHECK_2026-09-24.md, baseline c8a4aef) with facts measured since it was written. Start with git log --oneline -8, git pull, git status --short; the tree is at 536db7d or later and peers commit concurrently, so commit only by pathspec.

Read first, in this order:
1. docs/agent/reports/HUB_FIELD_FINDINGS_2026-09-24.md — live console readings taken by the owner on the reporter's save (TheGodUncle), mods-off and then with Passage Network 1.38 on. This is measured, not source-read. The two logs are docs/archive/logs/reporter_TheGodUncle_modsoff_*.log and reporter_TheGodUncle_modson_*.log; the SMR* tagged lines are the readings.
2. docs/agent/reports/MIGRATION_AUDIT_2026-09-24_D_hubs.md — a tier-2 source audit of passage hubs and traversal on 1.1.1, written after your report. Its claims are cleared only where HUB_FIELD_FINDINGS says so.
3. docs/archive/PassageNetwork_1.38_Code_PassageNetwork.lua — the mod's entire code, read against the archived 1.1.1 tree.

What changed since your report:
- The field symptoms are now explained by a measured chain: an interrupt on a hub or in a passage, a dump onto the hub surface, HasLocalAccess failing because it measures 20 hexes to the DOME CENTRE (ColonistTransport.lua:19-28, :293-299) against a radius-19 Geoscape dome, a rescue shuttle to the colonist's own home booked at the colonist's own position, and a one-sol wait outside. One colonist was watched dying on it. Every line is vanilla and unchanged from 1.1.0; Passage Network touches none of it and its residue hypothesis is refuted (connection tables clean in both runs).
- Your C111 drop recommendation now meets a measured instance: the rescue-ride path is what the reporter sees, on every ride.
- Your C109 verdict holds: no colonist in the save had an entry failure; access failing is its own "vacuous if", and the rescue chain runs instead.
- Hub occupancy: 71 units all with holder == hub, none stale, high turnover; but 35 of 45 held units stood beyond the hub's collision radius (the audit's S4, holder carried off the hub, is not refuted).

Do, report-only, no code, no status change:
1. Re-verdict every finding of your report against these facts: confirmed / corrected / unproven, with what changed.
2. Judge the hub audit's S1-S12 the way you judged the migration candidates: re-read the cited lines, mark each SOURCE-VERIFIED or HYPOTHESIS yourself, answer the player-route question for each, and rank fixes with shapes and controls. Take S1 hardest: it is proposed as the fix to build first (wrap Colonist:HasLocalAccess to grant access when the colonist stands on a hub or in a passage whose dome_network contains the destination's dome). Say whether that wrapper is correct, what it changes beyond migration (work range, services, stations), and what would falsify it.
3. Answer the causation question in one paragraph: vanilla defect, mod defect, or vanilla triggered by the mod. The owner's working answer is "vanilla on every item; the mod adds exposure only". Overturn it if the evidence does.
4. Write your result as a dated section appended to your existing report, or a new report beside it; commit by pathspec; do not edit entries (the coordinating seat files C-entries for S1, S2, S3 and S5 after your resweep).

Stops: a verdict that needs a game run names the sitting and stops; an engine-side claim (hub footprint, pathfinder door-versus-tunnel choice, MapHasAny on detached units) is marked unproven with its measurement.
```
