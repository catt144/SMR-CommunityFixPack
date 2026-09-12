# One-module review contract

Coordinator `/root` owns the sweep and git. Each task reviews ONE named registered
module. Write only `<module-stem>.md` and `<module-stem>.json` in this directory.
Never edit code, registration, metadata, cards, entries, indexes, release files,
STATE, checklist, progress, or other reports. Never stage, commit, pull, push,
regenerate indexes, launch the game, or spawn another agent. No live game is needed.

Read `docs/agent/STATE.md` (mandatory), `docs/agent/facts/INDEX.md` before engine
claims, the relevant individual facts, `docs/agent/FIX_POLICY.md` sections 2b and
4/4a, and `docs/agent/prompts/STILL_NEEDED_SWEEP.md`. Then read the assigned module,
its relevant entry files found via `docs/agent/bugs/INDEX.md` or `rg`, its site
row(s) at `C:/Dev/SMR-CommunityMods/content/fix-list.md`, and its card bullet(s)
in `metadata.lua` description. Primary game evidence is READ ONLY:
`C:/Dev/SMR-SrcArchive/1.1.0.403908/Src` (1.0.7 archive for necessary comparisons).

`CENSUS.json` contains the captured inputs, module hashes and fresh runtime status
for all 46 modules. Its `boot_log` is archived verbatim and complete after graceful
WM_QUIT. Its last status-shaped lines are 45 applied and SaintBlessing inactive;
Saint subsequently calls ctx.heal without another applied line. A THIRD retail
launch explicitly read the final menu registry: `CENSUS.json` `registry_log` and
`final_registry` contain MEASURED 46/46 active including SaintBlessing. This later
direct registry read supersedes the raw boot-message mapping. Read your module's
line and any later data/heal message. Applies means installation, never proof of
the cure or of reachable benefit. Both packs and TestKit were enabled; no colony
loaded, no suite run, no screen claim. The first launch was closed while data
loaded; the second (archived) was allowed to settle. Use only the archived second
boot, or the final registry log (third launch, temporary reader removed and
TestKit metadata restored byte-for-byte). `BODYCHECK.txt` records the whole-pack
check; falsifier passed all ten cases.
This check found no changed body or gone expression but is blind to consumer drift.

Answer all four questions: applies on 1.1.0? consumer still reads every value/path
changed? fix-list row true? card bullet true if present? Trace the PRIMARY game
consumer/caller (including sibling subfixes), rather than trusting the module's
own prose. Keep the cheap pass bounded; investigate expensive details only when
something disagrees. Start existing migration decisions from
`MIGRATION_DEV_REPORT.md` + `MIGRATIONFIX_AUDIT.md`; F59 was subsequently repaired,
F60 removed, F51/F58 rows narrowed. F52/F53/F73 retain named residuals; F54 was not
actually independently swept. Hotfix 2 retired 36 and recopied 10: don't redo it.
Saint is correctly kept for historical healing/1.0.7; verify that caveat rather than
reopening the known decision. Do not read fenced prelaunch sweep verdict reports.

Markdown: state your task/agent name and anchor `2983fac`, put disagreements first,
then a SINGLE fixed-schema row, primary evidence bullets with exact file:line on
1.1.0.403908, and an explicit list of what you did NOT check by name. Suggested
verdicts are RETIRE, REBUILD, KEEP, KEEP-BUT-FIX-CLAIM. These are recommendations;
the owner decides any retirement/who-benefits. Lack of runtime cure verification
alone is a LIMIT, never proof vanilla fixed it. `INFERRED` is not a filed defect.

JSON object (no markdown fences) with keys:
`module` (filename), `entry` (ids string), `applies` (string), `consumer` (string),
`row_true` (string), `bullet_true` (string), `verdict` (one of the four above),
`evidence` (list of exact versioned file:line strings), `basis` (SOURCE or INFERRED),
`not_checked` (list), `findings` (list of concise disagreement strings).
Use yes/no/partial/n/a/unknown prefixes in the strings; describe conditions.
Do not use a pipe inside a cell or an unescaped pipe inside a Markdown row.
Do not manufacture certainty to fit the schema. At least one 1.1.0 primary
file:line citation is REQUIRED, even for heal-only/uncertain benefit modules.

Finish by reporting the recommendation, any disagreement, and the two saved paths
to the coordinator. Reports will be committed verbatim for later independent audit.
