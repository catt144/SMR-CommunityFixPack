# DLC deep check — new bugs in the food DLC and the sponsor pack

Chain-authoring job, standing owner instruction: once the fix pack is patched, pushed and stable,
deep-check the DLC's own new code and the base-game changes made to accommodate it. Root one-off;
`git rm`'d with its prompt-map row in the commit that lands the mapped chain. Fire only after
`docs/archive/prompts/vanillahunt/README.md`'s link 99 has run — satisfied: its report,
`docs/agent/reports/vanillahunt/HUNT_AUDIT.md` §8, carries this job's kickoff line and the base-game
seam handoff this job inherits. That kickoff also names `HUNT_AUDIT.md` §1.4 and §4.3 as reads:
§4.3 records that a base change made through `__parents` or a table field is invisible to both row
readers, which is exactly how the additive premise below could be wrong and still re-confirm.

## Start

`git log --oneline -15`, `git pull`, `git status --short`. Authored at `fd6a9e6`; an empty
`git diff --stat fd6a9e6..HEAD -- docs/agent/support/CHAIN_METHOD.md
docs/archive/prompts/vanillahunt/README.md docs/agent/reports/vanillahunt/SEAM_REPORT.md
docs/agent/reports/vanillahunt/TRIAGE.md docs/agent/reports/vanillahunt/HUNT_AUDIT.md
docs/agent/FIX_POLICY.md` means these facts hold; re-derive whichever path changed.

## The job

Author a chain under `docs/agent/prompts/dlccheck/` per `docs/agent/support/CHAIN_METHOD.md` that
deep-checks the DLC's own new code (`ModTools\Src\DLC\norman\`, `…\thomas\`) and the base-game changes
made to accommodate it, then consumes itself without firing a link. Deep, not an exhaustive per-row
census of the whole tree — the owner rejected that shape once already for the vanilla hunt's own skim.
Size the chain and state its budget from a re-emitted inventory, never a stale one.

## Link shape

The investigation links (the seams, each preset group, the non-owner-path enumeration) get the
evidence below, the question and the hard rules (`FIX_POLICY`, the bindings), then free rein: no
prescribed read order, no fence on what to open or run, no prescribed hypothesis. Rails belong only on
the job-shaped links — the inventory re-emit, the scripted play leg, the terminal audit's checklist.

## What already holds

- Both DLCs are installed and their Lua and presets are extracted into the ModTools tree — a source
  effort, not reverse-engineering. The old file/line counts for `norman` and `thomas` are an authoring-
  pass seed, not a current total: re-walk both trees with a PowerShell-safe Python file/line inventory,
  pair it with `git rev-parse HEAD` and the installed game build, and reconcile every total against its
  members.
- `thomas` is small enough to read in full — do not let it fall off the end behind `norman`.
- The DLC's own Lua reads as almost entirely additive: new classes, and only four `OnMsg` hooks in the
  whole of `norman/Code`. That is an authoring-pass sweep, not settled — the chain's shape rests on it,
  so re-derive it before building on it with an instrument that can see a `__parents` or table-field
  change, and if DLC code turns out to patch base behaviour more than it appears to, say so and
  rebuild the chain shape. Two of the four hooks are `GatherLawTraitWeights` and
  `PersistGatherPermanents`; weight save/load hardest, since a save-breaking DLC bug is the worst
  class for a player.
- The thesis, standing: a new core feature ships under-tested, and nobody checked what it does to an
  existing player's game. Assume that here.
- The old-meets-new breakage is mostly NOT inside the DLC folder. It sits in the base-game changes
  shipped to every player, DLC or not (shared territory with the vanilla hunt — inherit, do not redo);
  the non-owner path (base Lua referencing DLC content — a name match alone is not a genuine
  dependency); and presets/data mutating shared registries no symbol sweep sees (`EF-078`'s precedent:
  a source read predicted 6 disabled modules, the game measured 13 — preset/data checks invisible to
  any symbol sweep).

## Inherit, do not redo

Vanillahunt's link 03 wrote the base-game food seam's full per-seam contract:
`docs/agent/reports/vanillahunt/SEAM_REPORT.md` → "For dlccheck". Links 03b/03c/03d wrote the
remaining presets/generated, research/laws/missions and base-caller seams into
`docs/agent/reports/vanillahunt/TRIAGE.md` under their own "For dlccheck" sections. Use those
citations and limits; do not re-read what they already settled, and do not extend them to DLC
overrides they did not inspect. `README.md` §2b and `TRIAGE.md`'s FR-1 rows carry the Linux/Proton
new-game-crash field report and its FR-1(b) result — DLC content disabled still crashes — read that
before spending effort on a DLC-internal cause for it.

## What a source read cannot settle

Balance, UI, localisation, art and progression sit outside a Lua read. 1.0.7 saves cannot load on
1.1.0 (`EF-079`), so a play fixture is provisioned fresh — hours, not a warm-up. End the chain with a
short, scripted play leg the owner can run in one sitting: a numbered list of what to build and watch,
predictions written first so a difference is a finding rather than something adjusted afterward.

## The finding contract

Per `docs/archive/prompts/vanillahunt/README.md` §3, plus one item specific here: does it affect
players who do NOT own the DLC — the question the developers are least likely to have tested, and the
one that sorts severity here. Nothing is "tested" from a source read; a finding is a candidate defect,
filed through `smr-bug-library`, never automatically a fix-pack module — `FIX_POLICY` and the owner
decide.

## Fan-out

Where a link is large enough to warrant subagent control (`norman` by seam, each preset group, the
non-owner enumeration), keep it one link tagged `_fanout_level_<x>` per `CHAIN_METHOD.md` rule 2, not
split. Keep judgement central: ruling on the additive premise, designing the play leg and the verdict
are not fan-out work, and no subagent writes to a shared file. A subagent's return is evidence, never a
verdict alone — file:line, what the new content does, which existing system it touches, the route
re-derived, who reaches it, the falsifier, and the do-players-without-the-DLC question. "Looks fine"
without a route is the shallow-instrument failure this job exists to catch. An agent that only locates code
cannot judge it — use a judgement-capable agent for the review itself.

Unlike the vanilla diff, this content has no catalogue of known defects to seed as controls. Derive two
or three real positives by hand before fanning out, use them as the calibration, and report the hit
rate in the chain's output — a fan-out that cannot be falsified is not evidence.

## Bindings

Never modify the game directory, including the DLC `.fpk` files. Editor/version rail
(`docs/agent/prompts/perma/release_prompt.md` § Release rails): no Mod Editor, no `version` edit, no
upload. `H-08`: never pull a junction. `H-09`: never stage a packed folder beside a live one. Archive
`ModTools\Src` before any game update (`C:\Dev\SMR-SrcArchive\`, standing rule in its README) — a DLC
patch overwrites the DLC source too. Explicit file paths on every `git add`; never `add -A`, never a
directory pathspec.

## Deliverable

`docs/agent/prompts/dlccheck/` — a chain per `CHAIN_METHOD.md`: README manifest, inbox/outbox per
link, terminal adversarial audit that re-derives a sample and rules on whether the additive premise
held. A defensible first cut, to argue with: `thomas` in full; the non-owner path; presets and data;
`norman` by seam, hardest last; the scripted play leg; terminal audit last. Owner decisions this job or
its links surface go to `docs/PLAYTEST_CHECKLIST.md` in its item format, not only into a brief.

## Live progress and lifecycle

Mark the first work-list row `IN PROGRESS`, later rows `PENDING`, one unfinished commit-and-verify unit
at a time: re-emit the inventory and reconcile the vanillahunt handoff against current source; author
the mapped `dlccheck/` manifest and links, including the play leg's probe-sweep gate and this brief's
subagent design; run doccheck, add the chain's map row, and in the same commit delete this prompt and
its own map row without firing any link. The root one-off is consumed when the mapped chain lands, not
when the DLC audit itself finishes. If a prerequisite or owner decision is missing, stop and keep this
prompt rather than leaving a half-transition.

## Scope

In: authoring the `dlccheck/` chain and its map row. Out: firing any of its links, the vanilla hunt,
game code, any other prompt.

## Stops

A file you must write is dirty with a peer's change; doccheck is RED outside this job and was before
you started; or a cited handoff (`SEAM_REPORT.md` / `TRIAGE.md` "For dlccheck" sections,
`HUNT_AUDIT.md` §8) does not say what this brief claims.

## Do not claim

That the DLC has been checked, or that any finding is confirmed — this job authors a chain, it does
not run one.

## Derived facts and falsifiers

| fact | measured | falsifier |
|---|---|---|
| both DLC trees are installed with source extracted into ModTools | `appmanifest_3215050.acf` dlcappid 3889420/3889430, both under `ModTools\Src\DLC\` | re-check the manifest and re-list both tree roots |
| the DLC's own Lua is almost entirely additive, four `OnMsg` hooks in `norman/Code` | authoring-pass function-name/`OnMsg` sweep | re-run the sweep against current source; a materially different count changes the chain shape |
| vanillahunt's terminal link 99 ran and its report carries this job's kickoff line | `reports/vanillahunt/HUNT_AUDIT.md` §8 | read that section; confirm it still names this file |
| the base-game food/preset/research/caller seams are handed off, not open | `SEAM_REPORT.md` and `TRIAGE.md`'s "For dlccheck" sections | read each section; confirm none has reopened |
