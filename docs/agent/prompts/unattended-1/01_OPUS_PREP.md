# Chain prompt 1 — prep: re-scope, bin, author, predict

**Read `README.md` in this folder first — binding chain rules apply.**
Unattended. Start with `git log --oneline -10` + `git pull`. Todo list up
front, one item per commit-and-verify unit.

**Read path** (files, not folders): this folder's README ·
`docs/agent/WORKFLOW.md` "Co-runs" (envelope + routing triage + probe
hygiene rule 5) · `docs/PLAYTEST_HELP.md` "The co-run rig" + the verified
command table rows for `CheatMeteors`, `CheatDustStorm`, `CheatDustDevil`,
`CheatCompleteAllConstructions` · `docs/agent/bugs/F99.md` (mechanism +
"What would settle it") · `docs/agent/bugs/C42.md` ·
`docs/agent/bugs/F35.md` + `F03.md` (leg A's claims) ·
`agent/reports/CHAIN_QA_REPORT.md` §9 item 2 (leg D's source design) ·
`agent/facts/EF-045` (timing discipline). Indexes find more.

## Jobs

**Job 1 — bin the SAVE primitive properly (README rule 10).** From Src:
`SaveGame(display_name, params)` (`Savegame.lua:1071`) — confirm it is a
plain global reachable from a game-time thread, what `params` it wants, what
filename lands on disk (`Savegame._UniqueName`, `:295-318`), and whether it
yields (the `_Wrap` pattern, `:337-344`, forced a thread for LoadGame — S2).
Also decide the DELETION route for throwaway saves (agent-side file delete
with the game closed is the proven shape). Write the proof step for prompt
2: save under a throwaway name → `Savegame._InternalListForTag` sees it →
`LoadGame` it back → delete it. ⛔ Do NOT plan any leg on the primitive
until prompt 2's proof passes; author legs A and D so they abort cleanly to
routed gaps if it fails.

**Job 2 — re-derive leg D (the load-heal sweep) in rig terms.** The §9
item 2 design assumed the owner drove. Re-derive from the entries it cites:
which heal lines print on load, on WHICH loads they must appear once and
then not repeat, and what numbers get compared. Deliverable: a per-launch
script of reads with predictions. Do not inherit the old step list.

**Job 3 — author every probe as parked source** (`.lua.txt` beside this
README, rule 5), copying the proven harness patterns
(`git show 93088ba:docs/agent/prompts/corun-rig/97_CoRun1.lua.txt` and
siblings): real-time thread, own watchdog, per-line `ModLog` markers, speed
set after load (a loaded save arrives PAUSED), settle 15 s, engine-line
timing only (EF-045 — never print `RealTime()` step lines across loads).
One probe file per launch cycle. Parse sweep GREEN on each parked source.

**Job 4 — the cycle plan.** Assign legs to launch cycles honouring the
README ordering rule (reads first, mutations last; mutating legs never share
a cycle with a read that could be contaminated). Include cycle 0 = the save
primitive proof + fixture confirms (leg A's turbine/MedCenter, leg C's
drones-near-track and repair resources, leg F's passages) — all label reads,
before anything mutates. Predictions + 3× abort thresholds per cycle, in
the corun-rig table shape.

**Job 5 — write the run conditions header template** every recorded number
will carry (build, pack count as READ, cold load, staged copy name, speed,
session uptime) and the per-leg falsifier sentences ("this leg is wrong
if…").

**Job 6 — close out.** Append the full handoff (cycle plan, predictions,
parked-source list, open risks) to `02_OPUS_RUN.md` "Notes from upstream";
update this chain's README manifest row; commit (doccheck green, push);
delete this file in the same commit.

## Stop conditions

- The save primitive turns out blacklisted or gated after all → legs A and D
  become routed gaps NOW; say so in the outbox; the chain continues.
- Leg D's re-derivation finds the old design unsound in a way reading cannot
  settle → route the question, park the leg, do not guess.

## ⛔ What you may not claim

- Not that anything "will work" — predictions are labeled predictions.
- Not the save primitive as PROVEN — Src-verified is its ceiling until
  prompt 2 executes the proof.
- Not fixture presence on `TEST2H TRAIN` — the record shows what the sitting
  had, not what the save captured; cycle 0 reads decide.

## Notes from upstream

*(The authoring session appends nothing — this is the chain's first prompt.
Known inputs: the SAVE primitive is Src-verified not blacklisted (corun-rig
S2 grep of `Mod.lua:1267-1428`); `CheatDustStorm`/`CheatDustDevil`-electro
are `[NEVER RUN]` table rows with source citations; the owner's kickoff of
this chain is the "say the word" for F99's discriminator — the severity
DECISION stays the owner's.)*
