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

- **From the orchestrator (`smr-bugfixpack-8f`), owner notes raised DURING the 02 sitting, 2026-09-13.**
  Three display findings and one scope addition. All are requirements, not mechanisms — pick the shapes yourself
  (README § "What is FIXED"), and say under DEPARTURES if you choose differently.

  **(1) UI chrome must stop competing with evidence on screen.** The owner's console during step 1–8 is dominated by
  `SMRTK_TAB` (six lines from cycling the tabs), `SMRTK_MOVE`, `SMRTK_PANEL` toggles and duplicate `SMRTK_SHORTCUT` /
  `SMRTK_PANEL_RESTORE` pairs, while the lines that matter (`TAINT_READ`, `SCRATCH_DISCARDED`, `FLUSH`) scroll among
  them. ⇒ **Requirement:** rule 7 stays exactly as it is — every action still emits exactly one tagged line — but each
  action additionally declares **whether that line reaches the SCREEN**. Pure chrome (tab switch, panel move, panel
  open/close, clear) is log-and-ring only; world changes and sitting evidence keep the screen. Requirement (B) is
  untouched: the line still exists everywhere an agent reads. ⭐ **The lever, read at source after
  `smr-bugfixpack-51` pointed at it — this is cheaper than it looks.** `T.Log` (`70_SMRTK_Core.lua:50-76`) makes
  three separate emissions per line: `append("toolkit", line)` to the ring, `ModLog(line)` to the log file (the game
  prefixes it `[mod]`), and `ConsolePrint(line)` to the console. ⇒ **skipping the `ConsolePrint` call for chrome
  verbs is the whole change** — one condition in one place, not per-action plumbing — and the log file still
  carries the line through `ModLog`, so requirement (B) is untouched rather than merely argued. The requirement is
  still yours to shape (per-verb flag, per-call argument, a chrome set); I am only recording that the lever exists.

  **(2) This subsumes the CLEAR fix.** If chrome does not print to screen, `SMRTK_CLEAR` never lands on the freshly
  cleared screen and no ordering change is needed. `smr-bugfixpack-51` verified the mechanism at source
  (`70_SMRTK_Core.lua:194` logs after the pcall; `:258` is a bare `cls()`), so the "reorder inside the action" idea I
  first proposed is impossible and logging before the callback for ALL actions would empty `before=`/`after=` on every
  action. Its `log_first` per-action opt-in is the right **fallback** if the destination split proves impossible.

  **(3) ⛔ RESOLVED — there is NO duplicated log record. This item is corrected, not open.** I raised a
  duplicate-line suspicion from the owner's screen; `smr-bugfixpack-51` read the log FILE and settled it (`843a508`),
  and my baseline was one emission too low. **Two lines per Log call is BY DESIGN** — `ModLog` and `ConsolePrint`
  are separate emissions (see the lever in item 1). **The same id appearing twice is the console echoing a return
  value**: `T.Log` ends `return line`, and a typed console expression is re-printed by `uiConsole.lua:362`, so it
  affects console-typed `SMRTK.Log` calls only. ⭐ **Counting toolkit actions by `id` is therefore SOUND** — my
  warning that later counts would be wrong was itself wrong; do not act on it.
  **What IS real, and 51 carries it to you with CLEAR:** `PANEL_RESTORE` logs more than once per load because
  `restore_panel()` is registered on **three** messages — `OnMsg.InGameInterfaceCreated`, `OnMsg.PostLoadGame` and
  `OnMsg.CurrentMapChangeDone` (`71_SMRTK_Panel.lua:207-209`) — and a savegame load fires the first two. It is
  **not** a second panel: `T.OpenPanel` reuses a live instance, and 51 confirmed behaviourally (one drag → one
  `SMRTK_MOVE`, one keypress → one `panel_toggle`; two panels would have doubled both). ⇒ a **logging-precision**
  item: log `PANEL_RESTORE` only when the panel was actually created or made visible, so an agent counting restores
  is not misled — ids 9/10 are P4's persistence evidence. ⚠️ Note the **third** registration when you fix it; a map
  change is a path 02 did not exercise.

  **(4) ⭐ SUPERSEDED AND ENLARGED — the owner RE-RULED THE WHOLE SURFACE later in the 02 sitting.** What was a
  request for an icon is now a **ranked ladder that replaces the floating panel as the default**; the ruling, the
  three rungs and the proven/plausible/uncosted state of each are in this README's ⚖️ **THE SURFACE** block — read it
  there, it is canonical, and all three rungs are pre-approved so you descend rather than ask. Your spike therefore
  covers **three** techniques, not two: infopanel injection (route proven), map-click capture, and **the dock icon +
  vanilla popout menus** (`reports/SMRTK_UI_HOOKS.md` §3). Rule 9 binds hardest on the new one — append a button when
  the HUD opens, never patch a vanilla HUD method while idle. Three consequences the ruling creates, which are mine
  to flag across payloads and yours to resolve:

  - ⚠️ **P2 grows, and its seat may no longer fit.** P2 was sized at difficulty 4 *because the spike carried its only
    hard part*. It now owns the per-object section **and** the entire second surface (dock icon, popouts, and
    whatever of rungs 2–3 is needed). That is closer to a 6–7. The owner seated P2 at **Sol, high** when it was a 4;
    if you agree it has outgrown that, say so in DEPARTURES and re-seat it — you have the licence, and the owner's
    difficulty read was explicitly the authoring session's estimate, not a measurement.
  - ⛔ **A popout menu cannot carry every page, and this is the likeliest way rung 1 fails LATE.** Vanilla popouts
    are menus: excellent for World's one-shot actions and P2's per-object list. But the Agent page needs an
    `XTextEditor` note field and stateful slot buttons, and the Kit page needs a scrolling log-tail pane — none of
    which is a menu item. ⇒ **Decide this at the spike, not after five payloads have built against it.** A legitimate
    outcome is a per-page split: menus for action lists, and rung 2 or rung 3 for the stateful pages. Cost that
    before committing the ladder's rung, and say in your report which pages landed on which surface.
  - **The status strip has no home on rung 1, and `smr-bugfixpack-51` deliberately left this undecided.** The
    at-a-glance CLEAN/TAINTED · eligibility · armed-count · errors read is the owner's safety glance, and a popout
    that is shut most of the time cannot show it. Requirement (B) does **not** bite — the log carries all of it
    regardless — so this is purely the human's glanceable read. ⇒ **Requirement:** an at-a-glance safety read must
    exist somewhere the owner can see **without opening anything**; the form is yours. Noted for your shaping:
    a badge or colour on the dock icon is the only option that survives rungs 1 and 2 as well as 3, since rung 3's
    panel already has the strip — but do not treat that as the decision.

- **02's OUTBOX, appended by the orchestrator (`smr-bugfixpack-8f`, 2026-09-13) — verbatim from `reports/SMRTK_SKELETON_SITTING.md`.** ⚠️ 02 wrote both outboxes into its report and struck its row and consumed its prompt, but did not append them to the inboxes; chain rule 2 requires both, and a pointer is weaker than an append because this is the file you actually read. Nothing below is my wording. The full verdict, the five superseding corrections and the archived logs are in that report.

  > P1-P4 all PASS on build 24995074; the core, the logger, the taint assert, the
  > `ConsoleEnabled` arm, the ring, the clipboard and LocalStorage persistence are
  > all confirmed in play, so build on them. The native console tap **and** the print
  > tee both carry real output, so either is a valid capture route. Five things to
  > carry: **(a)** per-object code must target `UniversalStorageDepotBase` and
  > `#storable_resources`, never `StorageDepot.resource` — 01's leaf refused on every
  > depot in the game; **(b)** `AsyncCheat*` infopanel entries bypass `ObjCheat` and
  > never taint even in vanilla (`ClassHierarchy`, `ClipPlane`, `Gizmo`, `Inspect`,
  > `Properties`, `Screenshot`), so they need no re-implementation; **(c)** `CLEAR`
  > logs onto the screen it just wiped, and the fix is a per-action opt-in honoured
  > by `dispatch`, never moving `T.Log` before the callback, which would empty
  > `before`/`after` on every action; **(d)** `PANEL_RESTORE` logs once per
  > registration and there are **three** (`InGameInterfaceCreated`, `PostLoadGame`,
  > `CurrentMapChangeDone`) though only one panel results — log on actual
  > create/make-visible; **(e)** `CopySince` is destroyed by the operator's next
  > copy, so it must be the last command of a block, and the panel **button** form is
  > immune. The owner's surface ruling and ranked fallback ladder are in ck175.

  ⚠️ **Overlap, so you do not count them twice:** its **(c)** CLEAR and **(d)** PANEL_RESTORE are the same two items as my numbered notes (2) and (3) above — 02's text is the authoritative version and mine was the early flag from the owner's screen. Its **(a)** is new and build-blocking for P1/P2, **(b)** removes work, and **(e)** is procedural and matters to 07/08.
