# Chain A — `smrcf-verify` · the gate for the whole follow-up set

**One unattended launch answers four open questions and arms two standing
detectors. Owner cost: ZERO.** Map: `agent/prompts/SMRCF_CHAIN_SET.md`.

## Manifest

| # | file | model | owner needed? | what it drains |
|---|---|---|---|---|
| 01 | `01_PROBE_opus.md` | volume tier | **no** | builds the payload, runs it, records the four answers + arms two detectors |
| 02 | `02_AUDIT_fable.md` | top tier | no | adversarial backward QA against the archived log; integrates; empties the folder |

Strike a row the moment its prompt self-consumes.

## What this chain is for

Four questions currently block or weaken other work. All four are answerable
from one launch, none needs the keyboard:

1. **Is the dust-devil marker path reachable?** Does map generation actually
   place `PrefabFeatureMarker`s with `FeatureType == "Dust Devils"`, and is
   `DustStormsDisabled` true on a terraformed save? Without this the marker-gate
   finding is `C49` all over again — a real sibling contradiction nobody can hit.
2. **Does `AsyncPopsDownloadFile` exist at runtime?** `C52`'s screenshot repair
   is pointless if the downloader it reaches is absent. Zero Lua definitions in
   all of Src; only a live `type()` settles it.
3. **Is map generation drivable from Lua, and how expensive is one?** Chain D's
   entire seed-search design rests on this. If it needs the menus, D gets
   re-planned rather than half-built.
4. **Does any existing save contain a Jumbo Cave?** Plus `UndergroundRework106`,
   which decides *which* Jumbo Cave script a save runs.

And two log-only detectors get armed, because they cost nothing and can only
ever pay: `WasteRockObstructor:DroneApproach` failures (`C25`) and
`TaskRequester:InterruptDrones` calls that filter a drone in `Embark`
(`C35` — the exact state the engine's own assert forbids).

## Binding chain rules

1. **Staleness check first.** `git log --oneline -10` + `git pull` before
   anything. This folder goes stale the moment another session commits.
2. **Inbox / outbox.** Nothing owed lives in a session's memory. Append every
   handoff to the successor's `## Notes from upstream` **and** to `02_AUDIT`, in
   the same commit that deletes your own file.
3. **Route, don't drop.** Unsure whether something belongs to you? **STOP AND
   ASK.** A discovered item goes to a named owner (a later prompt, an entry, or
   the checklist) before you close.
4. **Self-split at a clean commit boundary** rather than pushing a job to the
   edge of a context window. A shrinking folder is progress.
5. **File defects you trip over**, including in our own instruments. ⛔ **A
   silently-corrected instance is destroyed evidence** — disclose it on the
   entry or in the close-out.
6. **`WORKFLOW.md` elements 1–7 bind**, plus the co-run rules for anything that
   launches the game.
7. **Predictions before runs.** Commit and push the predicted answers BEFORE the
   launch, so results are falsifiable. `git log` timestamps are the proof.
8. **Archive the log in the same commit** that cites it (`git add -f` — the
   `.gitignore` drops `*.log` silently).
9. ⛔ **This chain writes NO fix code.** It measures and it arms detectors. Any
   temptation to fix something you find goes to a chain, not to `Code/`.

## Scope fence for the whole chain

**IN:** probe payload authoring, one unattended launch (more if a run is voided
and re-armed), the four answers, two standing detectors, record integration.

**OUT:** any `Code/` change that is not a detector; any fix for `C25`, `C35`,
`C50`, `C51`, `C52` or the dust-devil marker; any owner time; anything touching
the release front.

## Stop conditions

- The pack or opt-in gate reads wrong at run top → **STOP**, do not bank
  readings about code that did not execute (the unattended-2 lesson).
- A detector cannot be installed without changing behaviour → **do not install
  it**; record why and hand the question to `02_AUDIT`.
- Map generation turns out to need the menus → that is an **answer, not a
  failure**; record it and let chain D re-plan.
