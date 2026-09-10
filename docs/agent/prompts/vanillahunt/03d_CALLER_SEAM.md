# 03d — remaining base callers, services and rowless seams

ONE-SHOT: consume this file with `git rm -- <this exact file>` only on close-out,
after a full handoff and any required first-class children exist. Model: Fable
(recommendation, owner assigns). Owner needed: no. Independent of the other
03 continuations and 04; 99 waits for all of them. No game launch or module work.

## 0 · Read path and pin

`git log --oneline -10`, `git pull`, list agents, then read:
`docs/agent/STATE.md`; `docs/agent/prompts/vanillahunt/README.md` §§0–4 and chain rules;
`docs/agent/WORKFLOW.md` (probe hygiene and authoring); `docs/agent/FIX_POLICY.md` §4;
`docs/agent/reports/vanillahunt/TRIAGE.md` §§1–4 and §03 coverage / For dlccheck;
`docs/agent/reports/vanillahunt/SEAM_REPORT.md`;
`docs/agent/reports/vanillahunt/SEAM_COVERAGE.tsv`;
`docs/agent/reports/vanillahunt/INVENTORY.tagged.tsv`;
`docs/agent/reports/vanillahunt/PRESETS.tagged.tsv`;
`docs/agent/reports/vanillahunt/CALLERS.tagged.tsv`;
`docs/agent/reports/vanillahunt/NOROWS.tsv`;
`docs/agent/prompts/DLC_DEEP_CHECK.md` §§1–2;
`docs/agent/bugs/INDEX.md`; `docs/agent/facts/INDEX.md`; this inbox.
Use the indexes to open actual entries/facts relevant to a claim, not inherited
summary text. `SEAM_PLAN.md` records the original 03 scope and source pin.

Authored after filing commit `b28f133`; find the addition/close-out commit with
`git log --diff-filter=A --format=%h -- <this prompt>` and inspect later drift.
Re-read `A:/SteamLibrary/steamapps/appmanifest_3215050.acf`: buildid must still
be 24995074. Pinned source trees are `C:/Dev/SMR-SrcArchive/1.0.7.396349/Src` and
`C:/Dev/SMR-SrcArchive/1.1.0.403908/Src`. Manifest hashes/counts are in SEAM_PLAN.
A different build means archive the new tree by the standing procedure, then
stop for the chain's repin decision; do not silently compare to live changed files.
EF-085 proves shipped bytes match Src; it does not prove execution/native behavior.

## 1 · Live progress and controls

Create and commit a live todo/agent plan before the read: one checkbox per
commit-and-verify unit, exactly one in progress, updated as work finishes. Size
agents by your actual rows, not by a generic list. Parent owns instruments,
verdicts and every shared-file write; subagents read and report. README §4's
per-row return contract applies: row/file/function, class, both-tree locations,
actual change, reach, falsifier, seam and SMELL/PERF with evidence (or none).
Keep explicit read/not-reached receipts, identify hunks-only and malformed spans.
Preserve useful reports so a fresh 99 can audit the reasoning. Parent re-derives
surviving findings and a reproducible random sample; score eligible seeds honestly
(no eligible seed is not 4/4). No look-fine verdicts or stock-Lua nil assumptions.

Before recording any desk/probe/test result: run the WORKFLOW stale-probe sweep
`rg -l TEMPORARY Code/ ../SMR-BugFixPack-TestKit/Code/`. Zero hits is clean;
otherwise name every needed probe in the plan or resolve/report the stale probe
under WORKFLOW. Include `PROBE SWEEP: clean` (or the declared armed list) in the
result record and commit. This task needs no game probe or launch.

## 2 · Binding reading and filing method

Read FR rows first per README §2b, then F117-shape caller contracts, changed
bodies, guards, added/removed bodies, and assigned data. For EACH seam ask both
owner and non-owner questions: what old assumption changed, what exists when
DLC is absent, and is a named class/preset an actual dependency? Enumerate the
definition and the consumer in both directions. Names such as base FungalFarm
and DLC FungalFarmBase are not interchangeable. All base Lua shipped to non-owners.

Read both complete present bodies, their relevant callers/inheritors and the
actual runtime data reader. An added body has no old counterpart: compare its
old behavior path without inventing an old file. Surface sweep every opened
body for FIX_POLICY §4 intent tells, including PASSING and PERF. Runtime-only
timing, rendering and native behavior remain unmeasured. Added cost is not the
original cause of the pre-1.1.0 FR-3 report.

For every surviving finding, falsify first using actual archived Lua bodies in
the deskbench pattern when suitable; name every shim and include a negative or
counterfactual control. Do not fake native semantics to produce an alleged proof.
File a C entry yourself: fresh seq/row from the generated index, `cand`,
`source-read`, DIFF-CAUSED or PASSING, explicit tell, separately tagged ROUTE,
old/new citations, R1–R4/U reach, non-owner severity, falsifier, and independently
derived recipe with its vacuity condition. New findings never become modules.
Use `python tools/doccheck.py --regen`; never edit generated indexes or AGENTS.
Runtime/owner decisions go in PLAYTEST_CHECKLIST → Decisions waiting on you,
with TAKEABLE WHEN a specific fresh fixture/observation exists. 1.0.7 saves do
not load normally on 1.1.0; do not use the owner's campaign as a destructive fixture.

## 3 · Fence, stops and prohibited claims

IN: the exact receipt owner below, plus the minimum supporting definitions and
callers needed to judge those rows. OUT: other links' queues, fixes/modules,
metadata/version edits, game/archived-file writes, and DLC/norman reads beyond
the single function directly called by a base row. A needed DLC interior route
goes to TRIAGE → For dlccheck, TAKEABLE WHEN that chain reads the named class.
Record useful out-of-fence reads as incidental, not coverage or silent retagging;
send an untagged seam to 04 with a drift note for 99. If ownership is unclear,
finish independent work and request the missing decision.

Stop/split at a clean commit boundary if context cannot hold the remaining
rows or a registry exceeds a comfortable read. First finish authorized filing,
write a FULL child inbox and exact remaining keys, add its README row and 99 gate.
Never erase a remainder by marking the parent done. Runtime falsifier needed
means file a checklist rider, not launch the game. Guard-count drift is recorded
and work continues. Broken chain gates block the commit until repaired/reported.

Do not claim tested, non-owner-safe from a name match, preset coverage from a
callee excerpt, exhaustive dynamic caller reach, native crash proof, frame-time
measurement, or that DLC is/is not mostly additive. Do not close FR-1/2/3 from
source alone. Anonymous/dynamic callers, native data consumers, absent assets,
consoles, incomplete old DLC and actual execution remain blind spots.

## 4 · Deliverables and close-out

Append a named section for this link to TRIAGE (do not alter §§0–4 or 03's
historical receipt): exact read/not-reached keys, seed/random-sample scores,
findings with routes, FR-1(b), FR-2 and FR-3 outcomes even when the answer is
not reached, and For dlccheck's per-seam owner/non-owner boundary. Save a durable
report and any desk outputs; report limits and ALL caught drift, including quick
corrections. A read label is an attestation, not automatic behavior clearance.

Send full outboxes to every open affected sibling, 04 if needed and
99_TERMINAL_AUDIT.md. State any child queue and TAKEABLE WHEN condition. Update
STATE's NEXT and the README queue; strike only completed work, `git rm` this
prompt at close-out. Keep the original tagged inputs and SEAM_COVERAGE snapshot
unchanged. Before EVERY commit run `python tools/doccheck.py`,
`python tools/treediff.py --selftest`, `python tools/presetdiff.py --selftest`;
repeat applicable desk controls after relevant edits. WARN goes VERBATIM in
your summary, even if a standalone rerun resolves it. Explicit FILE paths on
both `git add` and `git commit -F <message-file> -- <paths>`; no directory or
blanket staging. Push and verify your commit plus worktree state.

## Notes from upstream · 03 close-out, 2026-09-10

The original task's ~400-row stop was mandatory: 1,289 INVENTORY + 1,618 PRESETS,
30 CALLERS, 18 NOROWS. 03 read 396 complete present spans in 25 core-food files,
six full caller/contract items, and incidental supporting excerpts. It filed
C56-C62 (five DIFF-CAUSED, two PASSING). The desk discriminates C56/C57/C59;
C58 native reservation outcomes, C60 profiling and C61 death/popups remain
unobserved. C59 and C62 have no established natural recipe. Do not duplicate them.

Literal guard counts are 3 norman / 1 thomas in base Lua, 10/1 including Data; original
brief conflated the scopes. The inherited count of 12 reference files number is not a
dependency proof. Base services/resources execute without DLC; normal base Food
does not populate the ingredient mask. Recipe classes exist in base without a
proved constructible base recipe processor. See SEAM_REPORT for every reviewed
seam, exact counterevidence, conditional DLC handoff and corrected mistakes.

Random parent sample:6/6 change descriptions agree, 5/6 route precision before
GetCropName was narrowed to no literal caller. Seeded positives eligible: 0.
The final Building.Destroy/GetUIWarning rereads resolve earlier truncation;
malformed/overlapping inventory spans remain rows, not distinct functions.
No original row was reassigned to/from 04. The close-out receipt's `pending`
includes incidental reads and shape-only caller checks; it means you still owe
the declared read. `python tools/seam_coverage.py` checks the dated partition,
not your future coverage.

The initial commit hook repeatedly emitted this warning despite standalone
doccheck reporting the kit clean; retain the precise wording if it recurs:
`  WARN kit-tree state is UNKNOWN on this run — re-run doccheck before trusting a clean kit tree`
03 rechecked its desk result after an explicit clean probe sweep because its
initial two commit messages omitted the required PROBE SWEEP line.

## 5 · Your exact queue and specific inbox

Filter SEAM_COVERAGE.tsv `owner == 03d`: **249 hand INVENTORY** rows in 105 files,
**16 CALLERS** items, **18 NOROWS** files, no PRESETS. This is all original 03 hand
work outside the completed 25 core-food files and 03c's progression set. The
receipt lists every key and path, including the 18 exact NOROWS from TRIAGE §3.
Diff both whole files for NOROWS; a one-line lookup is not completion. Group
agents around caller/service/maintenance/resource relationships, not one per row.

FR rows FIRST: R05283(FR-1),R05697(FR-2),R07155(FR-3),R09340(FR-2),
R09347(FR-3),R10122(FR-3),R10168(FR-2). Write FR-1(b) for the new-game row's
owner/non-owner path; write FR-2/FR-3 even where reach/native behavior is unresolved.
Lua/Config/config.lua is a 03 NOROWS item that 04's FR-1 temporal-upscaler list also
names as supporting evidence. You own its whole-file coverage; coordinate the
finding with 04 instead of claiming two independent complete audits. Other Config
files in 04's list stay with 04.

Four CALLERS entries C00595/C00596/C00597/C03968 have line-only checks:
ResourceStockpile calls resolve to its own GetCubePosRelative, not Station's
homonym; WasteRock omits an optional trailing resource with a default. Their
surrounding-body/contract audit is still owed. Other 12 caller items are pending;
explicitly trace ColonistTransport, prefabs/cargo, exceptional circumstances and
rocket notification receiver/argument types, including inherited overrides.

Follow-ups from bodies already read: enumerate whether any real caller still
services Farm directly after service moved to piles. Trace FoodService capacity
reservation/return across workshift changes (new :853-856, :877-884); no outcome was
proved. Trace VisitService's EnterBuilding-failure/destructor route before alleging
consumption without entry. Global AssignMeals has no explicit base caller found;
dynamic/DLC dispatch is not cleared. C58 raw-food fallback can be reached by
Hungry with a truthy fallback flag; do not require the Starving status effect.
Actual recipe-input double-consumption remains DLC-chain work pending a concrete
Food-input recipe/building/pile route, not an invented base fixture.

C62: base BuildingBlowUp plus four wrappers exists but instantiated scenario
reach is U. ScriptStatements.lua wrappers :723/:743 need authored scenario
context; generated effect wrappers go to 03b if in its receipt, otherwise 04-E.
Supporting reads do not silently transfer their queues. C56-C62 are already filed;
extend evidence if warranted, do not make duplicate entries.

TAKEABLE WHEN this prompt runs on the pinned sources. 18 NOROWS include ambient
food-service/work routines, research metadata, Diner/RocketTrade, Refabable and
constants/entity data. Existing partial references are not their full text diff.
