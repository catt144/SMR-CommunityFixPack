# Chain prompt 1 — rig spec: what a co-run can actually do, proven or flagged

**Read `README.md` in this folder first — its binding chain rules apply,
especially rule 10 (NO ASSUMED CAPABILITY).** Unattended: no game, no owner.
Start with `git log --oneline -10` + `git pull`.

You are writing the spec that prompts 2–4 execute. The owner's stated worry is
a hasty plan that needs 3 days of rework; your job is to make the plan
un-hasty by sorting every needed primitive into PROVEN (cite the
EXECUTED-ONCE record) / VERIFIED-IN-SRC (cite file:line, flag for skeleton
proof) / UNKNOWN (must be answered by co-run #0 or descoped). A primitive you
cannot place in one of those three bins does not go in the spec.

## Read path (element 8)

`docs/agent/STATE.md` · this folder's README · `docs/agent/WORKFLOW.md`
("Co-runs", probe hygiene, testing checklist) · `docs/PLAYTEST_HELP.md` (the
unattended A/B leg procedure, the enable-path leg, the MarsDebug `[install]`
pass — these carry the EXECUTED-ONCE provenance) · `docs/PLAYTEST_CHECKLIST.md`
(the co-run convention block + the four tagged candidates) ·
`C:\Dev\SMR-BugFixPack-TestKit` `Code/95_AutoRun.lua`, `96_AutoRunFlag.lua`,
`98_EnablePathLeg.lua`, `00_TestCore.lua` (the harness that already exists) ·
`docs/agent/bugs/F11.md`, `F99.md`, `C41.md` (the first payloads) ·
`agent/facts/INDEX.md` (open EF-008/EF-010/EF-012 and any fact your jobs
touch) · shipped Src for every primitive you verify.

## Jobs

**Job 1 — todo list up front** (WORKFLOW element 1), one item per deliverable
below, updated immediately.

**Job 2 — capability inventory with provenance.** For each primitive the rig
needs, bin it PROVEN / VERIFIED-IN-SRC / UNKNOWN with citations:

- process launch by the agent (retail `Mars.exe` direct / `-applaunch
  3215050`; who launched the EXECUTED-ONCE legs — check the record, do not
  guess); MarsDebug's Steam-picker preference and its modal assert dialogs
  (attended by construction — envelope limit, not a problem to solve);
- loading a SPECIFIC save programmatically (console/autorun path; verify the
  actual function in Src — nothing in the record has ever done this);
- staging a save COPY (where saves live on disk, what copying one entails,
  whether the game sees a renamed copy);
- game-speed control, pause behavior for real-time threads (the MarsDebug
  pass's pause note), programmatic quit, the autorun watchdog;
- log round-trip (`FlushLogFile`, log location, rotation cap ~20);
- what executes where: mod/TestKit code vs. console on retail (sandbox,
  `ConsoleExec` blacklist — EF-010) vs. asserts-build console;
- detecting "game is ready" from outside (poll the log? the autorun harness's
  own signals?); abort/timeout when the game hangs and the agent is blind.

**Job 3 — the capability envelope** (the owner's "the most it can do"). Three
lists with reasons: what an UNATTENDED agent run can settle · what a CO-RUN
adds (owner eyes/hands at measure moments) · what stays ORGANIC-ONLY
(reachability, feel, UI judgment). Name examples from the live backlog for
each. This document is what future sessions cite when routing work.

**Job 4 — risk register + effort model.** Wall-clock per launch cycle
(estimate from the record's legs, then co-run #0 measures it); iteration cost
when a script is wrong (relaunch? reload?); token cost per prompt; the
owner-attended minutes per candidate. Name the top 3 ways this rig could eat
3 days, and what in the spec prevents each.

**Job 5 — sign-off tiers, DRAFT** (owner request, on the record in the
README). Design:

- **Tier A — WITNESS:** owner eyes add information the log cannot carry
  (visible behavior). Owner attends the measure moment.
- **Tier B — EVIDENCE CARD:** log-demonstrable defects. The agent produces a
  compact card; the owner quick-reads and OKs. Define the card template —
  MUST contain: the scenario (one paragraph), RAW log lines before/after
  (never summaries), what was forced vs. organic, build pin, `PROBE SWEEP:`
  line, and the falsifier ("this card is wrong if …"). Cap it at one screen.
- **Tier C — DELEGATED:** mechanically self-verifying (A/B probe suite class).
  Ships on the suite verdict; owner gets a digest line, retains veto, is not
  asked per item.
- The classification RULE, stated so a future session can apply it without
  judgment: (a) would owner eyes at the screen add information? → A; else
  (b) can a probe falsify it without human judgment? → C; else B.
- ⛔ You may draft, not adopt: tiers change the `tested` policy, which is the
  owner's. Prompt 4 finalizes against real evidence cards and routes it.

**Job 6 — define co-run #0** (prompt 2 executes it verbatim). The CHEAPEST
end-to-end proof: staged save copy → launch → load → one trivial scripted
read → `FlushLogFile` → quit → agent reads the log back → record. Include:
step list, predicted wall-clock, what the owner does (expected: launch click
and stand by — ~10 min), the ride-along (the F11 `OnTransferToMapDone`-timing
trace from `F11.md` — wrap the binding, print the ordering verdict), and the
ABORT CRITERIA that trip the kill-gate (each UNKNOWN that fails, each step
that exceeds its predicted cost by 3×).

**Job 7 — route to the owner** (checklist "Decisions waiting on you", with
recommendations): the designated experiment save (name what it must contain:
at minimum a working passenger train line for the F11 watch; ideally
underground track for tie-break work) and the GO for co-run #0 scheduling.

**Job 8 — write `CORUN_RIG_SPEC.md` in this folder** holding jobs 2–6's
output, then close: append your outbox to prompt 2's `## Notes from
upstream`, update the manifest row, delete this file, commit (doccheck
green), push.

## Stop conditions

- A primitive the skeleton cannot proceed without lands UNKNOWN with no
  Src-verifiable path → STOP, route to the owner with options; do not write a
  spec on top of it.
- The effort model says even the skeleton needs owner time beyond ~15 min →
  STOP and re-scope with the owner (the entire point is buying their time
  back).

## ⛔ What you may not claim

- Not that any primitive "should work" — bins and citations only.
- Not that the tiers are adopted — drafted and routed only.
- Not any wall-clock number as fact before co-run #0 measures it — predictions
  are labeled predictions.

## Notes from upstream

*(2026-08-04, chain author — Fable, the session that adopted co-runs. Context
you should not re-derive: the four tagged candidates and their entries are
current as of `c731d4a`; the F11 Done-timing question and the F99 hex
tie-break are written up in `F11.md` ("Route claim narrowed") and `F99.md`
("Mechanism settled by reading") — the probes themselves are one-liners, the
rig is the work. The owner's sign-off pain, verbatim shape: "I only hit
flushed logs and said ok" — design Tier B so that sentence stops being true.)*
