# smrtk 03A — the pages, fanned out (build; cross-vendor primary)

Link 03A of `smrtk`. **Codex / Sol, xhigh or max** (owner's fifth ruling in the manifest; a Claude session with subagents may run it if the
owner says so). README rules 1–22 are yours, and README § "What is FIXED" is the licence: the five-payload cut,
who runs the spike, the API you inherit from 01 — defaults. Re-cut, re-spike or extend the core when you see a
better way; record it under DEPARTURES. Runs only after 02 PASSed — read 02's outbox first (which console tap
carries lines, the hotkey that stuck). 03B (Claude) judges your output before 07 documents it: write for a judge.

## Job 0 — the spike: settle the two shared techniques BEFORE launching anything

Two payloads (P2 infopanel injection, P3 map-click capture) each need "the least invasive way a mod hooks the
vanilla UI". Decided twice, they diverge; decided once, both inherit. Spend the short spike yourself:

1. **Infopanel section injection** — read how `sectionCheats` is composed (`Data/XDef/sectionCheats.lua`,
   `Lua/XDef/sectionCheats.generated.lua`) and how `InfopanelObj` builds sections (`Lua/X/Infopanel.lua`). Pick the
   route that needs no Mod Editor, never writes `config.BuildingInfopanelCheats` (rule 10), and wraps no vanilla
   function while idle (rule 9: a section spawned from a message or a template-list append is fine; a replaced
   `Open` is not). Write the decision + the two rejected routes with line numbers into `reports/SMRTK_UI_HOOKS.md` §1.
2. **Map-click capture while armed** — read how the construction cursor takes a click (`Lua/Construction/Construction.lua`)
   and how `UndergroundCaveIn` reads the cursor (`Data/CheatDef.lua:315-326`). Pick a route that installs only while
   armed and uninstalls to the original on disarm (rule 9). §2 of the same report.
3. Both decisions are **inherited facts for the payloads** — paste each into the matching payload's `## Notes from
   upstream` before launch. If either has no clean route, say so there and the payload builds its declared fallback.

## Job — launch, gate, merge

4. `tasklist` shows no `Mars.exe` (rule 16) — once, before launch, in its own command.
5. **Launch the payloads as subagents** (five is the default cut; merge or split them if the work says so — a
   re-cut payload gets a full inbox), in parallel, each with its own brief (`payloads/P1_WORLD.md` …
   `P5_STAMPER.md`) plus this README, `EF-095`–`EF-099`, 02's outbox and your spike report as its read path.
   **Top tier of your vendor on P5** (the capture format is a contract). Payloads write files and return a
   **numbered-claims report**; they never commit and never `git rm` (README rule 21).
6. **Per result, the gates yourself, never inherited from the report:** `python tools/parsecheck.py` on each file the
   payload names; rule 6's grep (`NetSyncEvent|LogCheatUsed` → 0 on that file, presence side quoted once for the
   run); rule 7's grep (bare `print(` → 0); the file is in `metadata.lua`'s `code` list (H-10); `python
   tools/doccheck.py` GREEN (it parses the TestKit tree). A payload that fails a gate gets **one re-fire** with the
   gate output in its inbox; a second failure is reported, not forced.
7. **Commit per file, by pathspec, sequentially** in the TestKit repo (`git commit -F <msg> -- <that file> metadata.lua`);
   the pack repo gets the spike report and your outbox. No remote on the TestKit; push the pack.
8. **Merge check:** all five files load together — one parse sweep of the whole `Code/` list in order, and the
   cross-payload ids (P2's Dump → P4's registry id; P2's Pin and P4's watch → P3's) resolve or stub as their briefs
   say. Record which stubbed.

## Your report — the input 03B judges (`reports/SMRTK_FANOUT_REPORT.md`)

Numbered, falsifiable, one command each: per payload — built (file, function names, line count), verified how
(the exact gate commands and their output, copied), stopped (what and where), OWNER-ROUTED (each with a
recommendation), DRIFT (anything a payload corrected in its brief or found wrong upstream), **DEPARTURES** (every
default you or a payload changed, with the reason and the invariant it was checked against), **SUGGESTIONS**
(what the plan missed — yours and the payloads', merged, deduplicated, the ones you disagree with kept and marked). **Disagreements
first**: anything a payload claimed that your gate contradicted. Then the outbox: what 07 must document (the final
button list per page) and what 99 must re-derive.

## Scope fence

IN: the spike, the launches, the gates, the commits, the report, **and the core** — 01 was your vendor's work and the
core is yours to extend between the spike and the launch or after the merge (never while payloads run in parallel
against it; the diff goes in your report). OUT: writing payload code yourself while a payload owns that file (re-fire
it instead), docs (07).

## Stop conditions

The spike finds no idle-clean route for BOTH shared techniques · two payloads need the same core change · a
payload's second re-fire fails · `Mars.exe` is running and the owner is unreachable. Report; do not force.

## What may NOT be claimed

That any page works in play (08). That a payload's self-report is true (your gates are the evidence, its report is
a claim). A GREEN whose command output you did not paste.

## Close-out

Consume the five payload files (`git rm payloads/*.md` — they are spent) and this file in the same commit as the
report; outbox to 03B and 99; strike your row; push the pack repo.

## Notes from upstream

- (02 appends here)

- **01 API outbox, 2026-09-13 — still HELD behind 02:** TestKit core `774b55a`,
  panel `b400683`, metadata `5d8d3b3`. Read `reports/SMRTK_SKELETON_PREDICTIONS.md`
  §API frozen for 03A and §DEPARTURES/§SUGGESTIONS before the spike. Actions use
  `Run/Arm/Disarm/Fire(id, ...)`; callbacks take `(ctx, ...)`, return fields or
  false/reason; `ctx.state` carries toggle state and disarm must restore it.
  Payloads do not log a second primary result; delayed work dispatches **inside**
  its thread. `Page(id,label,build)` builds under the supplied host; `Button`
  dispatches a registered id. Slots are `slot_1`..`slot_6`. P1 must register
  `pause`, `stop_disaster`, and use `quiet` for the armed strip.
- **DEPARTURES:** Ctrl-Shift-F11 avoids the wider collision; eligibility returns
  `UNAVAILABLE:sandbox` because CanUnlockAchievement is blacklisted. Never turn
  a clean taint read into eligibility=OK. Copy uses current-mark labels or
  absolute ring indices and discloses eviction. Native/print/toolkit ring
  sources are separate; our own lines do not prove native tap delivery.
- **SUGGESTIONS:** after 02, route retirement of 00_TestCore's old console
  bootstrap through 03B; build P3/P4 delayed mutations on Fire/Run and preserve
  unknown readings. A clean fixture is a separate provisioning requirement.
  No payload content or infopanel technique was built ahead of your spike.
