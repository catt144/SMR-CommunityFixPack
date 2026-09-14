# smrtk 08b — the three native stamps, re-fired

Link 08b of `smrtk`. **Claude attending, owner at the keyboard.** Created 2026-09-14 by the
orchestrator on the owner's instruction, as a self-split of 08 (README rule 4): 08's sitting
**ran and closed** at PASS WITH CORRECTIONS, but **class 18 never ran** — blocks 13–15 were
blocked by defect 21 — and 08's session is spent. This link carries the unrun remainder and
nothing else. README rules 1–22 are yours.

⛔ **08 is RETIRED. Do not look for `08_FULL_SITTING_owner.md`** — it was `git rm`'d in the
same commit that created this file. Its grave:
`git log --diff-filter=D -- docs/agent/prompts/smrtk/08_FULL_SITTING_owner.md`, and the run
it produced is `reports/SMRTK_FULL_SITTING.md`, which is the record, not the prompt.

## 0 · ⛔ THE GATE — this link does not fire until both are true

1. **Defect 21 is FIXED and verified on the desk.** `77`'s `add_building` guards on
   `field(o,"template_name")`, which **no placed building carries** —
   `SetupBuildingTemplateTables` sets it only on the template table (`Building.lua`:
   `BuildingTemplates[id] = setmetatable({ template_name = id }, g_Classes[id])`). Every
   building is therefore omitted and capture always answers *"no supported buildings or grid
   nodes in capture"*. The fix is `field(o,"template_name") or o.class` — the fallback
   `skip_capture` already uses two functions away — **plus an audit of every other
   `template_name` read**. ⛔ **Until that lands, class 18 is untestable and this sitting
   measures nothing.**
2. **The owner has said the surface is stable enough to script against.** ck183 rules a
   re-layout (task grouping + hot bar + one toggle button). ⚠️ **This brief names actions by
   FUNCTION, not by page**, precisely so a re-layout does not invalidate it — but the
   attendee must re-walk the current UI at preparation and write the actual click path into
   the script before the owner sits. ⛔ Never hand the owner a path you have not walked.

⭐ **Sequencing is the owner's call and both options are live:** fire straight after 21's
one-line fix (proves the stamper early, costs a second short sitting), or fold it in after
the ck183 re-layout (one sitting, but carries the chain's least-proven feature through a big
build). ⚖️ The stamper is the feature the owner called *"a game changer"* and **it has never
placed a single object in the game** — weigh that against a second sitting, and ASK.

## 1 · Orient

`git log --oneline -10` + `git pull` in **both** repos, `git status --short`, `ListAgents`,
then `docs/agent/STATE.md`. Authored against pack HEAD **`b937366`**.

⚠️ **THE STALE-PROBE GATE BINDS — this link launches the retail game.**
`grep -rln "TEMPORARY" Code/ ../SMR-BugFixPack-TestKit/Code/` must be **zero hits** (or every
hit declared by this session's design). Put that line in your todo list and ⛔ **refuse to
record any result without it.**

## 2 · What 08 already PROVED — ⛔ never re-run any of it

- ⭐ **Requirement (A) is PROVEN, not asserted:** `cheats_count=0`, `CheatsUsed` enumerated by
  name after every destructive action, 844 records, zero TAINT, zero ERROR, zero surviving
  arms. ⛔ **Do not re-derive the taint invariant.** Take one after-taint read per stamp block
  because the blocks below call for it, and stop there.
- **Classes 1–17 PASS.** Blocks 1–12 and 16 ran. ⛔ Do not re-run them.
- The first `RunAll()` ran. ⚠️ Whether it discharges **ck144 (a)** is **UNRULED** — do not
  assume it either way.

## 3 · The job — blocks 13, 14, 15 verbatim from 08, then 08's close

⛔ **These are transcribed unchanged from the retired brief.** They were priced and ordered by
07 and never run; do not re-price or re-order them.

**13. Native stamp 1: ordinary depot — 2 minutes (class 18).** First screen: surviving source
depot and empty level target. Name `smrtk08_depot`, Capture selected, Copy layout; agent
opens/preserves literal text. Plan at click on the new target, freeze numeric
ready/skipped/buildings/grid prediction before placement. While paused, try Stamp at click
there once: require REFUSED and zero mutation. Resume, re-arm and stamp at the same target
after a fresh plan if anything changed. Require final native STAMP, owned-site completion,
`left_sites=0`, actual stockpile/functionality and after-taint read.

**14. Native stamp 2: dome/interior and upgrades — 3 minutes (class 18).** First screen:
selected source dome with supported upgraded interior. Name `smrtk08_dome`, Capture selected.
Plan first over the original occupied fixture: skips and zero mutation. Re-plan at empty level
space; freeze numeric counts and PENDING_DOME interiors, then stamp at that same target while
running. Inspect native fit, completed dome **GameInit**, each interior's actual dome
membership and operation. Apply captured upgrades separately: check the affected new
building's built state and colony unlock disclosure; queue success alone does not pass. Keep
source objects unchanged.

**15. Native stamp 3: flat connected grids, capture lifecycle — 3 minutes (class 18).** First
screen: source flat connected cable/pipe patch. Name `smrtk08_grids`, Capture rectangle; first
click sets one corner without CAPTURE, second emits it and disarms. Copy literal layout.
Plan/stamp at fresh level space using frozen native numeric counts, and inspect **connected**
grids supplying their scratch consumers. Include a passage/suspended/switch row only if
present: require its named skip, not replay. Inspect Capture map on the small clean fixture
with a fresh name `smrtk08_map`; record a cap refusal as unavailable if over-cap. Next saved,
Copy layout and Cancel target/work exercise their distinct controls. Arm a rectangle and Save A
then Load A once: require DISARM/no retained corners, pins cleared and Slot 3's lifecycle dump.
This final round trip also demonstrates target cleanup; native waits may extend the priced
block, within the save/load abort threshold.

⚠️ **The separate follow-ups (Fill storages all maps, Add 10 colonists on the intended selected
dome, Funding +500M) may be fired after base inspection** — check actual World results and
scope, not just `STAMP_FOLLOWUP`. ⛔ They do **not** establish a complete colony duplication
feature, and see the defect-22 warning below before believing any spawn result.

**Close:** re-run 08's block 16 shape only as a close-out — editors/Mod Manager closed, no
arms, CLEAN taint, archive the boot log. ⛔ Not as a re-test of classes 2/4/17.

## 4 · ⚠️ Three defects are live while you run this — they change what you may believe

- **22. `spawn_colonists_*` mutates and reports `REFUSED`.** Measured: `status=REFUSED
  reason="spawn count mismatch; before=701 after=701"`, then a census seconds later read
  **711**. The label join is deferred to end of tick; the check is same-tick. ⛔ **If 22 is
  unfixed, a `REFUSED` on any `spawn_*` does NOT mean "no mutation"** — block 15's "Add 10
  colonists" follow-up is exactly that class. Verify by census, never by the log line.
- **20. An armed click slot blocks ALL map selection**, with right-click-to-cancel shown
  nowhere. ⇒ **Script rule, mandatory here:** blocks 13–15 arm click targets constantly, so
  **select every object and configure every watch BEFORE arming anything**, and disarm before
  the next selection.
- **25. "Finish selected rocket flight" is unreachable by selection** — irrelevant to these
  blocks, listed so it is not rediscovered as new.

## 5 · Scope fence

**IN:** blocks 13–15, the close-out, `reports/SMRTK_08B_STAMPS.md`, this link's row in
`prompts/smrtk/README.md`, the boot log.

**OUT:** ⛔ re-running anything in classes 1–17. ⛔ Building or fixing anything — you are the
attendee, not the builder; a defect found here is FILED, not repaired. ⛔ `docs/PLAYTEST_CHECKLIST.md`
— owner-facing items go in your report as `OWNER-ROUTED` and the orchestrator consolidates
them into ck183, exactly as 08's were. ⛔ The ck183 re-layout itself.

Found something interesting out of scope: **file it, do not fix it** (rule 3).

## 6 · Stop conditions — permission, not failure

Stop and report if: defect 21's fix is not actually in the loaded TestKit (check before the
owner sits, not after) · capture still answers *"no supported buildings or grid nodes"* ·
the fixture lacks a supported dome interior with a built upgrade, or two flat connected
cable/pipe patches with room for duplicates — **provision or record NOT RUN by name, never
substitute a fake desk object** · a stamp mutates the SOURCE objects · the stale-probe sweep
is not clean · the owner's time runs out mid-block (report the block as partial with its
first-screen witness, never as a pass).

## 7 · What may NOT be claimed

- ⛔ **Never claim the stamper works from a queue success.** Blocks 14 and 15 say it: queue
  success alone does not pass; the built state, dome membership and grid connection are the
  reading.
- ⛔ **Never claim "complete colony duplication."** v1 is flat cables and pipes with named
  skips for passages, switches and special buildings.
- ⛔ **Never re-assert requirement (A) from this sitting.** 08 proved it; you are not
  re-proving it and a second proof from a smaller sample is weaker, not stronger.
- ⛔ **A mechanism-only PASS is not a pass.** 08 scored block 12 PASS while the owner would
  rather have hit ultra speed (ck183). If a stamp block works but is unusable, **say both**,
  and score the usability half explicitly.
- ⛔ Never state an absence from a truncated grep or a truncated log read.

## 8 · Close-out

1. Report at `reports/SMRTK_08B_STAMPS.md`: per-block verdicts, the frozen numeric predictions
   against actuals, every named skip, defects found, `OWNER-ROUTED` lines, and DRIFT for 99.
2. **Force-add the boot log** — `*.log` is gitignored and 24 prior sitting logs are tracked by
   force-add under the `<tag>sitting_` convention. ⛔ 99 re-derives against the archived log,
   so a dropped log silently breaks the terminal audit.
3. Append your outbox to **99's** `## Notes from upstream` (rule 2).
4. Strike this link's row in `prompts/smrtk/README.md`'s queue.
5. ⛔ **`git rm` this file** in the same commit. One-off; it does not re-run.
   ⚠️ `prompts/README.md` carries ONE folder row for `smrtk/`, not a row per link — do not
   touch that map beyond repointing its "next is" sentence at **99**. Re-run doccheck after.
6. Commit by pathspec in each repo; push the pack repo. ⛔ TestKit is local-only by design.

## 9 · Required — a live progress list

Create it before you start, **one item per commit-and-verify unit**, marked the moment each
completes, exactly one in progress. The owner reads it to decide when to step in — and this is
an attended sitting, so a stale list wastes their time directly.

## Notes from upstream

**From 08 (`reports/SMRTK_FULL_SITTING.md`, PASS WITH CORRECTIONS, 2026-09-14):** 25 defects,
of which 21 blocks you outright and 22 makes one follow-up's log untrustworthy. 08's own
outbox flagged that STATE carries two refuted lines (`GhostFarmOxygen` as a FAIL, and "every
depot is `UniversalStorageDepotBase`"), that `DomeFreeSpaceMismatch` needs triage, and that
three attendee drifts are recorded — weigh its other readings knowing that.

**From the orchestrator (2026-09-14):** 08 is retired because its context was spent, not
because it failed — it closed cleanly and proved the invariant the chain existed to prove.
⚖️ **ck183 is the live design ruling** (group by task, hot bar, one toggle button) and it is
the owner's, not yours: if the surface has moved by the time you run, re-walk it and rewrite
the click path, but ⛔ do not redesign it and do not treat a layout you dislike as a defect.
