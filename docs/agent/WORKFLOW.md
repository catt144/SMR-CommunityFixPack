# Development Workflow

Process rules for this repo. Code rules are `FIX_POLICY.md`; the global duties are `CLAUDE.md`'s
`Must_Read_Header`; orientation, filing, prompt writing and session close are the skills in
`.claude/skills/`. Situational procedures live in `support/`; the map is `docs/README.md`.

## Layout

- Dev repo: `B:\Dev\SMR\SMR-BugFixPack`, git-versioned, canonical.
- Game install: `A:\SteamLibrary\steamapps\common\Project Spark` ("Project Spark" is the Steam
  folder name). Shipped Lua source, read-only: `<game>\ModTools\Src` (`Lua\`, `CommonLua\`, `Data\`,
  `DLC\`). Nothing under the game folder is ever modified.
- Archived source trees, one per game version: `B:\Dev\SMR\SMR-Shared\SMR-SrcArchive\<version>\Src` with a
  `MANIFEST.sha256`; that folder's README holds the archive rule.
- Mod install point: `%AppData%\Surviving Mars Relaunched\Mods\SMR-BugFixPack`, a junction into the
  dev repo, so the checked-out tree is the running mod.
- Saves: `saves/` in the repo, git-ignored and pack-ignored (`*/saves/*`). `saves/game` is a junction
  to `C:\Users\stkot\Saved Games\Surviving Mars Relaunched\76561198020568696`, the only folder the
  game lists. `saves/backup` is a junction to `%APPDATA%\Surviving Mars\76561198020568696`, which the
  game does not list, so a save there is invisible in the load screen. `saves/reporters/` is a real
  folder for saves players send; copy one into `saves/game` to load it and keep the original. Both
  junctions reach the owner's real saves: never `Remove-Item -Recurse` on `saves/` or a junction,
  because PowerShell 5.1 deletes through it; remove a link with `cmd /c rmdir saves\game`. Read a
  save only when the owner asks — never scan or pick one on your own initiative to find a fixture.
  Owner, 2026-09-18: "I think agents should stop checking saves all together, And only check saves
  when I ask. Most of the time they are wrong anyway."
- TestKit, never shipped and local-only by decision: `B:\Dev\SMR\SMR-BugFixPack-TestKit`. Its README is
  the kit's own build-state document; the durable pack-side view is `tools/TESTKIT.md`, and the
  SMR Tool Kit plus its sitting slots are `tools/SMRTK.md`.
- Sibling mods: the opt-in pack `B:\Dev\SMR\SMR-OptInPack` (its own docs) and the save-rescue tool
  `B:\Dev\SMR\SMR-CommunitySaveRescue` (design and status in `bugs/D13.md`; unpublished, held as a
  contingency).

## Install for testing

```powershell
New-Item -ItemType Directory -Force "$env:APPDATA\Surviving Mars Relaunched\Mods" | Out-Null
New-Item -ItemType Junction -Path "$env:APPDATA\Surviving Mars Relaunched\Mods\SMR-BugFixPack" `
  -Target "B:\Dev\SMR\SMR-BugFixPack"
```

Enable "Relaunched Fix Pack" in the game's Mod Manager; restart the game after editing Lua. The
console line `SMRFixPack.ListFixes()` prints each fix's status (active / inactive+reason / disabled /
error).

## Per-fix discipline

1. Every fix links to a `bugs/` entry with file:line evidence and obeys `FIX_POLICY.md`.
2. Re-verify the target against the cited Src lines before patching; `apply()`'s self-check guards
   it at runtime and returns a reason string, never an error, if a game update moved it.
3. `python tools/parsecheck.py` before any commit that touches Lua: a syntax error in any listed
   file breaks the whole pack at load.
4. One commit per fix or tight group, with its entry and, when the change has a player surface, its
   `prompts/perma/RELEASE_OUTBOX.md` Pending entry in the same commit.
5. A fix invalidates its own tests: after changing a module's behaviour or timing, grep for every
   probe or harness that covers it and run the WHOLE suite, not just the legs the brief names,
   re-basing any harm-asserting leg on the pre-fix body extracted from git (`git show <sha>:path`,
   never retyped). Before an attended leg runs, trace its trigger to the shipped body and ask what
   would make it vacuous.

## Records and rulings

- Every console line, lever or command printed in a human doc carries `[RAN <date>, log <name>]`
  or `[NEVER RUN]`; unmarked, a never-executed snippet reads like a proven one.
- Load-bearing claims in entries, specs and briefs are tagged MEASURED / SOURCE / INFERRED /
  INHERITED / GUESS per row, never as one claim over a table. The route sentence ("therefore the
  only way is…") is tagged separately from the lines it cites.
- A routed item names its owner prompt and its precondition. An item whose precondition is a
  situation goes to the checklist as a rider, not to a prompt that will forward it again.
- A log a status flip will cite is copied into `docs/archive/` in the same commit, with
  `git add -f` (`.gitignore` drops `*.log` silently). The game keeps about 20 log files.
- A ruling is recorded with the condition it was made under; re-read it against today's state before
  treating it as binding, and never record a later ruling as a reversal without checking whether the
  earlier condition still holds.
- Player replies are pull-only (owner, 2026-09-12): never drafted unasked, never on an owed list,
  never raised as a nudge, never a gate on other work. A draft in `docs/FIELD_REPORT_REPLIES.md`
  waits by design; when the owner asks, write one and stop. Triage of the report into `bugs/`
  continues unchanged.

## After a game patch — the source-diff instruments

fpk verification: line numbers in `bugs/` and `facts/` come from `ModTools\Src`, and the game
executes `Packs\Lua.fpk` and `Data.fpk`. Parity was byte-identical for 1.1.0.403908 (`EF-085`);
re-prove it after every update, since a same-named function edited under a full replacement is
invisible to the runtime self-checks.

0. Archive first. Copy `ModTools\Src` to `B:\Dev\SMR\SMR-Shared\SMR-SrcArchive\<version>\Src` with its
   `MANIFEST.sha256` before the update lands, and whenever an unarchived version is on disk. Steam
   updates and branch switches overwrite the tree in place and unasked (`EF-075`).
1. Fire `prompts/perma/GAME_PATCH_PROMPT.md`. Its sweep is `python tools/patchcheck.py` (fpk
   parity, the one-hop dependency hash over pins, `Require` targets and citations, call signatures,
   save-exposed sites, the none/scoped/full verdict), with `python tools/bodycheck.py` for the
   defect expressions and `python tools/sigcheck.py` for arity. Each tool's header defines its
   verdicts and what each one obliges; write the REMOVE/FIX prompts from the table.
3. `tools/treediff.py` and `tools/presetdiff.py` run on trigger only: the patch notes name a system
   we fix, a `DLC_DEEP_CHECK` chain is running, or a changed body cannot be explained by hand from
   the two trees. They emit about 25k rows; never run them "to stay current".

What the instruments license (the canonical copy; `FIX_POLICY.md` §2b points here). On their output
alone you may state exactly four things: a pinned body's bytes did or did not change; a named arity
did or did not change; a stated regex is or is not present in a named body; a named function or
preset field exists in one tree and not the other. "Vanilla fixed it", "this fix is still needed",
"that change is harmless" and "nothing moved under us" each need a second source: a read of the
replacement body in both trees, or a run in the game.

- `bodycheck.py` cannot see class c, semantics moving under a wrapper whose target body is
  byte-identical (six class-c instances in the 1.1.0 response, four of them FIX rows), anything
  outside the pinned body, or a defect that is an absence. Every FIX row the pinned body misses
  (F-1, F-2, F-4, F-5), `patchcheck.py`'s `Require` hash catches. A regex pinned to phrasing yields a false `DEFECT-GONE`, the
  direction that retires a live fix; a `DEFECT-GONE` is a REMOVE candidate, never a verdict.
- `treediff.py` misses anonymous `function(` literals and hunks outside every row span;
  `presetdiff.py` reads generated files only and cannot tell `REINDEX-SWAP` from a real change.
- None of them see the engine, runtime-only behaviour, or the 1.0.7 `DLC/` subtree. Copy-vs-wrapper
  is a practice (`luafn.find_bodies` over both archives plus our `Code/`), never a name proxy.
- A clean run over every module is not evidence that every fix still works.

Artefacts: `reports/vanillahunt/` (tracked) and `reports/VANILLA_DIFF_DISPOSITION.md`.

Each instrument's own header defines its flags, its verdicts and what each verdict obliges;
`tools/README.md` routes to them, and to every other script in `tools/`. Which `--selftest` runs are
gated is what `python tools/doccheck.py` prints — read its `SELFTEST:` lines. What the output above
licenses is decided here, not there.

## Probe hygiene (owner, 2026-08-01)

No test session starts and no result is recorded until the stale-probe sweep has run clean:

```
grep -rln "TEMPORARY" Code/ ../SMR-BugFixPack-TestKit/Code/
```

CLEAN is zero hits, or every hit is a probe that this session's brief and todo list declare it
needs. Anything else: repair first (delete the file and its `metadata.lua` line, commit) or stop
and report. Stale probes are how false facts got recorded.

- Every temporary probe carries the literal word `TEMPORARY` in its header comment; that is what the
  sweep greps for. One without the marker is a defect: file it on sight.
- A probe is stale the moment its answer is recorded. Delete it in the commit that records the
  answer.
- Every commit that flips an entry status, records a MEASURED fact or reports a PASS/FAIL carries a
  `PROBE SWEEP:` line, `clean` or `armed: <files>, declared by <test>`. A result commit without one
  is re-verified before anything builds on it.
- A probe file is in `Code/` only while its run is actually happening (owner, 2026-08-04): placing
  and running are one act, deleting and recording are one commit. Until the sitting, park the
  probe's source as a fenced block in the brief, where it is inert: the mod loads only the files
  in `metadata.lua` `code` (`Mod.lua:490-521`). doccheck's `temporary_sweep()` is red on any marker
  in `Code/` and the hook blocks on red; `--no-verify` is not an alternative. Long-lived
  instrumentation belongs in the TestKit's `90_Loggers.lua` behind a toggle, never marked
  `TEMPORARY`.
- A sweep is fresh for 24 hours, or until a change touches a probe, a module a probe reads, or the
  kit's registration. A stale sweep is owed at the next playtest before its probes run, never
  between sittings. No agent, gate or kit code refuses a boot, a suite run, an upload or any other
  work over a sweep's age, and none overrides the owner (ck184, 2026-09-15: a gate, not a hard
  rule).

## Testing checklist per fix

Leg-design rules:

- An objective counter is only objective if it can fail, and it needs a liveness witness beside it.
- A probe reaches the code the way production does and computes its expectation independently
  (vanilla's algorithm or hand-derived constants), never with the fix's own logic. A guard probe
  also asserts that the guard still delegates.
- When the trigger is a selection you cannot steer, delete the lottery: invoke the shipped call site
  directly on a chosen target and settle the selection half by reconstructing the pool.
- A negative result states the condition it sampled, not just the count. Absence of a never-sampled
  condition is not a negative result.
- A gate on an owner action detects the condition; a typed token is a convenience, never the
  primary signal.

Steps:

1. Load a save or new game where the bug reproduces; confirm reproduction with the pack disabled.
2. Enable the pack; confirm the fix.
3. Confirm no error spam in `%AppData%\Surviving Mars Relaunched\logs`.
4. Save with the pack enabled, disable it in the Mod Manager, restart the process, load: the game
   must not break (PT-20 shape; `FIX_POLICY.md` §3). A Mod-Manager disable takes effect only after
   a full process restart; without one the pack is still loaded and the reading is a mixed state
   (PT-20 redo, 2026-08-14; D13's four-states rule). Never a Mod Options toggle: a toggled-off
   module keeps its hooks and reads clean by construction (`EF-002`).
5. Set the entry's status, front matter and heading tag together. `tested-attended`: the owner was
   at the keyboard. `tested-unattended`: real launches with nobody watching; full weight for what an
   instrument can read, never for a screen event. Bare `tested` is legacy and closed to new work
   (owner, 2026-08-15): it means attendance unaudited, so never promote one without re-deriving it
   from the archived record and never read it as attended.

The TestKit's `SMRTest.RunAll()` A/B pair (pack disabled, then enabled) is the regression harness.

### Log review (owner, 2026-08-01)

A flushed log covers hours of continuous play, and the owner reviews the errors with the agent;
every time they have pushed back it turned up a vanilla defect. "Not caused by our leg" is an
attribution verdict, never a reason to stop looking: report every unexplained line with its age and
let the owner decide, and stop and say so when something is out of the ordinary. Old logs hold
evidence no leg was designed to collect; mining them for `[LUA ERROR]` is cheap.

The limit (owner, 2026-09-16): "don't diagnose a problem that's not ours." When the log itself
assigns the cause to someone else — a missing-mods load, third-party mods absent from the stack —
report the line once with that evidence and stop; this does not license dismissing a line whose
cause is unclear.

Read a GitHub issue or other tracker through `api.github.com`, never its rendered page: a fetch of
the rendered page has silently returned zero comments when there were three. The issue list
endpoint's `comments` count is the free control — a non-zero count with a reader showing nothing
means the reader is wrong.

### Cheats on playtest saves (owner, 2026-08-12)

Playtest colonies are oversized and under-industrialised, so `CheatFill` on food and maintenance is
life support for the fixture and cheat markers are the normal condition.

- Count them, name them, attribute the reason, and ask for it once.
- A cheat is a confound only where the reading intersects what it changed; name the intersection or
  state there is none.
- A leg that needs a no-cheat run declares it in its brief and preps a resource-rich save in
  advance; it may not ask the owner to stop cheating on a colony that needs it.
- Toolkit `[SMRTK] SMRTK_<Verb>` records are intentional test actions: never ask the owner about
  one. A vanilla `ObjCheat`/`Cheat` marker in a new log is worth one attribution question. Taint
  and eligibility are `EF-095`/`EF-096`; no-taint never proves eligibility.

### Both mods loaded (owner, 2026-08-12)

The rig's baseline is the fix pack and the opt-in pack both enabled; a gate read shows two
registries, in the player's enable order (`EF-054`).

- Every "the pack" claim names which pack. An opt-in line in a fix-pack log is expected background,
  attributed, never flagged as foreign.
- A loaded opt-in module is a confound only where the reading intersects what it changes; name the
  intersection or state there is none.
- A leg that needs the opt-in mod off declares it in its brief and budgets a full process restart for
  the disable; the re-enable is handed back to the owner.
- The standing configuration is the compatibility soak: cross-mod interference is a named class in
  whole-log reviews, and a hit routes to both repos' records.

Single-pack gate reads predate the split and are never quoted as current.

## Co-runs

`support/CO_RUNS.md`, binding when a batch of bugs is tested attended.

## Sign-off tiers (owner, 2026-08-04)

- Tier A, witness: the owner's eyes add information the log cannot carry; they attend the measure
  moment.
- Tier B, evidence card: log-demonstrable; the owner reads a one-screen card (scenario, forced or
  organic, the raw before/after log lines, run conditions, the one-sentence falsifier) and OKs it.
  Hands-only: the owner does the named act, then reads the card as Tier B.
- Tier C, delegated: mechanically self-verifying (the probe-suite class); ships on the suite
  verdict with a one-line digest per batch; the owner keeps the veto.
- A demotion from a designed Tier A is stated on the card and applies to the next instance, never
  silently.

The tiers say what the owner reads afterwards; a status word still needs the attendance it names.

## Release

`prompts/perma/release_prompt.md` owns the lifecycle; `support/RELEASE_SURFACES.md` and
`support/POST_UPLOAD_CLOSE.md` are its procedures; the owner uploads through
`docs/UPLOAD_WORKFLOW.md`. Standing facts with no other home:

- The upload packs the whole mod folder, junctions and symlinks included, filtered only by
  `metadata.lua` `ignore_files` (`GedModEditor.lua:678-741`). Never put a link inside the mod folder
  unless a pattern covers it. `tools/upload_preflight.py` fails on a link whose contents would pack,
  on any packed file outside `Code/*.lua`, `metadata.lua`, `items.lua`, `LICENSE` and the preview
  image, and on a pack over 5 MB; doccheck's PACK IGNORE PARITY gate keeps `pack_predict.py`'s copy
  of the list equal to `metadata.lua`'s.
- `items.lua` carries one `ModItemCode` per `Code/` file in `metadata.lua` order, so the editor
  round-trip regenerates the same code list; add, remove or reorder in both, same commit.
- The TestKit is never uploaded.
- Prior art: ChoGGi (Fix Bugs) and LukeH (Martian Express), `reports/PRIOR_ART_SURVEY.md`, which
  also backs the save-safety claim in player-facing text.

## Release marking (2026-08-17)

What is live on the portal is marked with an annotated tag per mod, `fixpack-`/`optin-`/`rescue-`
plus `version_major.version_minor.version` from `metadata.lua`, pushed at upload; the tag and
`metadata.lua` must agree, and the portal version is recorded against the sha in
`reports/RELEASE_PORTAL_PREP.md`. `main` is latest verified work and normally runs ahead of what
shipped. No standing `testing` or `published` branch: the junction makes the checked-out tree the
running mod, and STATE and both generated indexes are rewritten in place, so long-lived branches
conflict on exactly those files and silently change what the rig loads. To reproduce what a player
runs, `git worktree add ../SMR-FixPack-shipped <tag>` and point the junction there for the
investigation; while it is pointed there no suite reading describes current work. A hotfix branch
is cut from the tag the day it is needed. A short-lived code-only branch per chain is justified for
code nobody is sure about; doc changes still go to `main` directly.

## Authoring a prompt

Use the `prompt-authoring` skill. R-D, self-split: depth is the cost, so legs are packed at
authoring to roughly `filesize/4 × 1.7` and about 75% fill, never to the edge of a window; a retry
is a fresh fire, not a continuation; working legs are blinded to the budget. Attended sittings are
indivisible and exempt.

## `[FAQ]` tag

Behaviour a player could mistake for a bug, or a question the design deliberately answers "no" to,
is marked with the literal `[FAQ]` on the entry that already explains it, never in a new doc;
`grep -rn "\[FAQ\]" docs/ Code/` collects them. A tag is a bookmark, not work and not a promise.
Remove it in the commit that changes the tagged behaviour.

## Verification rails

The global duties are in `CLAUDE.md`; facts with falsifiers are in the `prompt-authoring` skill. R-F: size the
verification by owner-observability. A player-visible defect is verified by one attended A/B in the
game, the owner being the cheapest verifier of "can a player actually do this"; an engine-internal
defect by desk harness plus audit, because watching would show nothing. Build legs inherit behind a
fingerprint and re-derive only what moved; zero-trust re-derivation is the terminal audit's job.
