# SMR Community Fixes follow-up — the two retained descendants

> ⚖️ **OWNER RULING 2026-09-09: KEEP FOR NOW.** This grouped entry stays with
> `smrcf-verify/` and `smrcf-modbrowser/`. The ruling retains the work; it does
> not fire either descendant and does not unpark `C52`.

This is a work-order front door, not reusable chain-authoring guidance. The
general method is `docs/agent/reports/CHAIN_METHOD.md`. Historical chains B and
D and their old dependencies are consumed; their graves remain in git.

## Current set

| descendant | current job | authority and start condition | close-out |
|---|---|---|---|
| `smrcf-verify/` | one fireable `C35_DETECTOR.md`; build a permanent, log-only TestKit detector for the still-`cand` C35 | owner retained the rewritten detector; no further start condition | delete its prompt, remove its name from the grouped map row and update this file; do not claim the set closed while C52 remains |
| `smrcf-modbrowser/` | README plus four fireable links for the three C52 browser findings | owner retained it but C52 remains `parked`; link 01 may start only after an explicit owner unpark | terminal link archives its README, empties the folder and removes its name from the grouped map row |

The descendants are independent. The C35 detector no longer answers whether
`AsyncPopsDownloadFile` exists; that removed job cannot gate C52. If the owner
later unparks C52, its own link 01 performs the runtime-symbol preflight. An
absent symbol drops screenshot defect 1 with evidence but does not silently
decide defects 2 or 3.

## Binding controls

1. Start with `git log --oneline -10`, `git pull`, `git status --short`; compare
   named inputs with the descendant's authoring anchor and re-check moved groups.
2. Read `docs/agent/STATE.md` only because these jobs call for current status,
   then the relevant bug entry through `docs/agent/bugs/INDEX.md`,
   `docs/agent/FIX_POLICY.md`, the descendant manifest/prompt and its inbox.
3. Keep a live todo list, one commit-and-verify unit per item. Recheck shared
   paths before writing; use exact pathspec commits. A doccheck warning is copied
   verbatim into the close-out.
4. Do not lift C52's `parked` status, alter an owner hold or infer a release
   gate.
5. Test-bearing work follows `docs/agent/WORKFLOW.md` probe hygiene: run the
   exact TEMPORARY sweep and apply the current STATE age/change obligation at
   the next playtest. Probe age never lets an agent refuse owner-directed work.
6. Every descendant removes or updates its live map membership when it closes.
   When the last descendant closes, delete this root prompt and its one-off map
   row in the same commit. Never leave a tombstone in the live prompt tree.

## Derived facts and falsifiers

| fact | measured | falsifier |
|---|---|---|
| only the C35 detector and parked C52 chain remain in this grouped set | exact recursive inventory and current bug-index read at `eec864d` | enumerate both folders and read C35/C52 through `docs/agent/bugs/INDEX.md` |
| the former chain-A Async job no longer exists | `smrcf-verify/` contains only `C35_DETECTOR.md`, whose retained job is C35 | search the live detector for an executable Async deliverable and inspect its git history |
| C52 is parked and the keep ruling is not an unpark | current C52 entry plus the verbatim ruling above | only a later owner instruction in words can change either condition |
| this grouped entry is not a release gate | surviving jobs and owner rulings | compare against the current release prompt and checklist before claiming otherwise |

## Kickoff lines — after their separate gates clear

- `docs/agent/prompts/smrcf-verify/C35_DETECTOR.md` — “build the C35 detector.”
- `docs/agent/prompts/smrcf-modbrowser/01_SPEC_fable.md` — “run the mod-browser chain”; valid only after the owner explicitly unparks C52.
