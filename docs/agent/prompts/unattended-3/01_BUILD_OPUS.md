# Chain prompt 1 — build the two ruled fixes, with their probes

**Read `README.md` first — binding chain rules apply.** Staleness check across
the fix pack and the TestKit, live todo list updated per item.

## Job 0 — re-derive before building (rule 3)

Both entries carry dated corrections precisely because inherited citations went
stale before. Re-read at Src (`A:\SteamLibrary\steamapps\common\Project
Spark\ModTools\Src`), 1.0.7.396349:

* F85: `RivalColonies.lua:535-555` (the distress-call confirmation; `:546` the
  `dont_pause` flag) and confirm it is still the flag's SOLE user
  (`grep dont_pause` over Src). `PopupNotification:Init` shape.
* C39: the three-class gate `Workplace.lua:205-217` + dev comment `:209-210`;
  the two law defs (`LawDef-Technology.lua:227-234` Service, `:70-76` Factory);
  hunt the expected Research sibling; the label memberships (the sweep below).

## Job 1 — the C39 static label sweep (it sets the build's coverage list)

Enumerate the members of all three automation labels in Src templates and
classify each by the compensation gate (`IsKindOf` Factory / ResearchBuilding /
Service). **The mismatch list is the build's coverage contract** — record it in
the entry (the four known Workshops are the floor, not the ceiling). A mismatch
the ruled shape cannot cover is ROUTED, not improvised (README stop condition).

## Job 2 — settle C39's design and build both modules

* **C39 design:** the entry's §2026-08-12 records the two candidates (chained
  post-wrapper on `Workplace:GetWorkshiftPerformance` recomputing `law_scale`
  for mismatched buildings — degrades gracefully, ⚠️ scales the overtime
  additive too, disclose; vs a §1.5 body copy widening the gate — exact, but
  patch-rot on a hot method). Settle against `FIX_POLICY.md` §1 and record the
  reasoning on the entry. The runtime discriminator is recorded there too
  (carries the law's `modifications.max_workers{percent=50}` while failing all
  three gates).
* **F85 build:** chained wrapper on `PopupNotification.Init`; flip `dont_pause`
  only for the distress-call popup's preset/route; everything else untouched.
  Layer/shape per `FIX_POLICY.md`; self-check (`Require`) on the shapes the
  wrapper assumes; stands down if the game changes.
* Both modules: register in `metadata.lua` `code` (order rules in the file),
  headers in house style (what/why/route/disclosure), **save-safety tier stated
  explicitly** — neither build should write anything persisted; if that turns
  out false, stop and route.
* **Disclosure language:** the F85 module header says design-judgment tweak
  (the game's code is not wrong; the owner chose the behavior). C39's header
  cites the dev comment as intent (this one IS a plain repair).

## Job 3 — TestKit probes

Probes for both, in the suite's house pattern (name, `[install]`/`[behavior]`
split, skip-with-reason when the site is unreachable retail):

* F85: read the effective `dont_pause` through the wrapper on the distress
  popup's route, with a negative control (an untouched popup still
  `dont_pause`-false by default). Design so 02 can sample it unattended; if a
  live popup spawn is needed, prefer constructing the popup object over
  simulating the rival flow.
* C39: the discriminator logic (mismatch detection), and a compensation reading
  that 02's bracket can compare against the control.

## Job 4 — close the prompt

`python tools/doccheck.py --emit-counts` (new module/file/probe counts land in
STATE's block, emitted never typed) · entries updated (build recorded; status
stays short of `fixed` until 02's suite evidence — follow the house vocabulary,
tag + index row together) · commit at boundaries, push · **append Notes from
upstream to `02_VERIFY_OPUS.md`** (what was built, where every new line lives,
the C39 coverage list, what 02 must re-emit rather than inherit) · delete this
file in the closing commit.
