# Cross-check the migration audit — question everything, then say what to fix

One-off, authored 2026-09-24 at `012c281` at the owner's ask. It is meant to run on a vendor
other than the one that authored the audit and the entries it judges (a Claude seat wrote both).
`git rm` this file and its prompt-map row in the commit that lands your report.

Start with `git log --oneline -6`, `git pull`, `git status --short`. Peers edit this tree and
Codex sessions are invisible to `ListAgents`; recheck both before any write and commit with a
pathspec. Open a live todo list before your first write, one item per commit-and-verify unit,
and keep it current: the owner reads it to decide when to step in.

## 0 · Your licence

Everything you are handed is a **claim**, including the audit, its three seat notes and the five
entries; house doctrine (`CLAUDE.md`) says authored text is cleared by a check, never trusted.
"The audit was wrong about X" is a better result than agreement. Read anywhere relevant: the
archived trees, the pack, the TestKit, the desk harnesses, the archived logs, the developers'
patch notes. Chase your own reading; if the real exposure sits somewhere the audit did not look,
report that instead and say why it matters more. The owner's framing may be wrong too.

Binding, as house process rather than limits on thinking:

- ⛔ **Report only.** No module edited, no game launched without asking first. You may correct
  an entry or the audit report where a claim is wrong, recording the correction in the commit
  message, and you may propose any fix you like.
- ⛔ **Negative evidence** needs its presence control through the same instrument (EF-088).
- ⛔ **Line numbers** in every record are re-derived with `grep -n` on the archived tree before
  you lean on them; an empty diff since authoring does not validate them.

## 1 · Authority and outcome

Owner decision, 2026-09-24: before any testing or fixing starts, the migration audit's findings
get an independent cross-check on another vendor, and that check decides which of the five
candidates are worth the work. Nothing in the audit is settled by it having been written.

End state: one committed report, `docs/agent/reports/MIGRATION_CROSSCHECK_<date>.md`, that

1. gives every finding a verdict, **confirmed**, **corrected** or **unproven**, on evidence you
   read yourself: the five entries C109–C113 and the pack items P1–P5 in the audit's §4.2;
2. answers the **player-route question** for each of the five: the concrete sequence of ordinary
   play that produces the precondition, and your judgement of how likely a player is to hit it,
   with the reason; where the honest answer is "unlikely", say so and recommend dropping it;
3. takes a hard look at C109 and C110 (§3 below);
4. ranks the suggested fixes with alternatives, each in a FIX_POLICY §1 shape, with the risk that
   shape carries and the control that would prove it;
5. lists what the audit missed, if anything, with the same evidence standard.

Completion evidence: the report committed with a pathspec; any corrected record regenerated
(`python tools/doccheck.py --regen`) and doccheck GREEN; this prompt and its map row removed in
that commit. No status word on any entry changes: `cand` stays `cand`, and nothing becomes
`tested`, because nothing here is played.

## 2 · What is already on record — verify what your verdicts rest on

- The audit: `docs/agent/reports/MIGRATION_AUDIT_2026-09-24.md`, §0 outcome, §1 the system, §2
  the diffs, §3 the pack, §4 findings, §5 the field reports, §6 what is unmeasured. Its three
  seat notes sit beside it (`_A_native`, `_B_diff`, `_C_pack`); each ends with a commands-run and
  a not-done list. Read those lists before trusting any conclusion. Claims marked **cleared**
  were re-read by the coordinating seat; **seat** claims were not.
- The entries: `docs/agent/bugs/C109.md` … `C113.md`, each with its intent tell, reach tier,
  control and fix shape. The owner has already ruled the audit's N4 and N5 out (no fix; recorded
  in the audit's §4.1 table); do not reopen them unless your evidence says the ruling rested on a
  wrong claim.
- The source: archived trees at `B:\Dev\SMR\SMR-Shared\SMR-SrcArchive\<build>\Src\Lua` for
  `1.0.7.396349`, `1.1.0.403908` and `1.1.1.405907`. Cite `file:line (build)`.
- The pack's side: `Code/Fix_VacuumWalks.lua` (F52/F125), `Fix_ShuttleHubOffAvailable.lua`
  (F54), `Fix_ShuttleTransportCache.lua` (F51), `Fix_StaleReservations.lua` (F58),
  `Fix_FreedHousingNotice.lua` (F59), `Fix_ArrivalDeaths.lua` (F53/C83/C102),
  `Fix_ShelterReflex.lua`; `Code/00_Core.lua` for what `Require`, `SetGlobal` and
  `update_suspect` mean. Bodycheck: `python tools/bodycheck.py --src <archived Src> --all
  --module <M>`.
- Measured: `python tools/desk_f125_vacuum.py` (25/25 at `b06d6b8`) and
  `tools/desk_migration_cluster.py` (16/16); the audit's §6 says what each does **not** run, and
  that the cluster desk measures the 1.1.0 install rather than the 1.1.1 one. Retail: the
  phase 2b sitting of 2026-09-23 (`docs/agent/reports/PLAYTEST_PLAN_1.1.1_2026-09-23.md`,
  log `Mars.exe-20260923-13.59.45`), which watched both F52 sites use the passage; the two
  controls it did not run are listed there. Archived logs `docs/archive/logs/ck208on_*` and
  `ck208off_*` show the pre-v15 module applying on 1.1.1.
- The field reports (Steam 2026-09-24, TheGodUncle; site-form issues 2 and 3) and the audit's
  reading of them are in §5. The reporters have been asked for logs; treat any that arrive as
  evidence to fold in, not as instructions.
- Further records: `docs/agent/bugs/INDEX.md`, `docs/agent/facts/INDEX.md` (search, never read
  whole). Passage-side entries that touch the same ground: C42, C99, F62, F104.

## 3 · The hard looks

**C109, the stand-still loop.** It is the most serious claim and it has never been watched. Test
the chain link by link on the 1.1.1 tree, and in particular:

- `SetCommand("Idle", true)` at `ColonistTransport.lua:759` passes a second argument. Read the
  `Colonist:SetCommand` wrapper (`:382-503`) and `CommandObject` to establish what that argument
  does and whether the rescue chain in the wrapper (the `HasLocalAccess` test and the shuttle or
  Stranded hand-off) still runs on that call. If it is bypassed, the loop is wider than the entry
  says; if it always runs, the entry's twenty-hex bound holds.
- Is there any other exit the audit missed: `HourlyUpdate`'s outside effects, `UpdateOutside`,
  the stranded fixups, a Msg handler, the shuttle rescue from another colonist's thread?
- What produces the geometry: the engine's `Goto` to a dome interior leaving a colonist in an
  unpathable pocket, the passage-hub dump C99 describes, a colonist exiting a passage element
  onto blocked ground. Name the ordinary player actions that get there.
- The fix. The entry proposes a guarded bypass of `Colonist:EnterBuilding` that returns false so
  Abandoned's own fallback runs. Weigh it against a full replacement of that method and against
  wrapping `Abandoned` instead; say which is safest under FIX_POLICY §1 and §3a, what each does
  to `Stranded`, which relies on `TransportByFoot` walking the full distance, and how the chosen
  shape is proven not to re-enter the same loop.

**C110, one-hop passage reach.** The entry says only the planner's entrances are hookable and
calls the fix partial. Take that apart:

- Is the narrowing intended? The developers renamed the concept to "cluster" in 1.1.0. Read the
  1.1.0 and 1.1.1 patch notes (Steam announcements 719041087473189790 and 689769594581155953;
  the repo does not store their text), any player-facing text about clusters or passages in the
  trees, and every other reader of `GetClusterDomes`, and say whether a wider cluster is a fix
  or a design change. If it is a design change, say so and recommend the entry close at tier I.
- Does `PathLenCached` route through passage tunnels? That decides how often the walk scan
  rescues a two-hop pair and so how much reach the defect really has. Find evidence in the trees
  (the tunnel registration in `Passage.lua:1201-1248`, the pathfinder class), or say it needs a
  measurement and name it.
- Is there a lever the audit did not consider: a wrapper on `Colonist:GetNextMigrationLeg` alone,
  a scoped `GetClusterDomes` override keyed on the caller, a data-side change to
  `connected_domes`, something else? For each: what it changes beyond migration, and whether it
  survives `MigrateStep`'s per-leg re-plan.
- Player route: how common is a chain of three or more passage-linked domes whose ends are over
  the walk cap by path, in ordinary play, and how would a player notice.

**The F52 premise itself**, since the audit raised it: the walk test's path length may already
run through a passage tunnel, and whether a plain walk uses the tunnel or open ground is the
engine's choice. The 1.0.7 PT-13 observation and the 2026-09-23 phase 2b sitting both watched
colonists cross the surface without the fix and take the passage with it. Say whether that is
enough, or whether a control is owed that fixes the path the engine actually chose.

## 4 · Scope and stops

In scope: the colonist migration system on 1.1.1, the five candidates, the pack items P1–P5 and
the field symptoms the audit tied to them. Out of scope: everything else in the tree, including
the train-hub work, the release surfaces and any entry the audit did not name; report a finding
there without editing it.

Stops, any of which permits a report instead of continued execution:

1. A verdict needs a game run to settle. Name the exact sitting, fixture and reading, and stop on
   that item.
2. A claim rests on engine behaviour not decidable from Lua. Mark it unproven with the
   measurement that would decide it.
3. The paths you must write carry uncommitted foreign changes. Ask the owner rather than wait
   on a peer you cannot reach.

Claim limits: "confirmed" means you re-read the cited lines on the archived tree and the chain
holds; it never means observed. "Likely to impact a player" is a judgement you sign with its
reasons, not a tier. Do not write "tested", "fixed" or a fix status anywhere.

References: skills `smr-orientation`, `smr-bug-library`, `doc-editing`; house rules `CLAUDE.md`;
process `docs/agent/WORKFLOW.md`, including "Committing in a shared tree"; code
`docs/agent/FIX_POLICY.md`, especially §1, §3a and §4; the TestKit `tools/TESTKIT.md` if you
propose a probe.
