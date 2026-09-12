# Surface audit of the still-needed sweep — one session, self-consuming

**Written 2026-09-12 by `smr-bugfixpack-d0` at the owner's direction.** Fire in a
fresh session. `git rm` this file in the commit that lands the report, naming its
grave. Verify every specific here against `git log` and the tree before trusting it.

> ⚠️ **CONCURRENCY (owner, 2026-09-12): `prompts/C85_C88_BUILD.md` may be running in a sibling Claude session at the
> same time, in the same checkout.** It owns `Code/`, `items.lua`, `tools/desk_*`, the TestKit, entries C85/C88/C89 and
> the outbox's Pending section — never touch those. Shared with it: `docs/PLAYTEST_CHECKLIST.md` (claim your item number
> by message first), `docs/archive/SESSION_LOG.md`, `prompts/README.md`. `git pull` before every shared-doc write, commit
> by pathspec only, and if `doccheck` goes RED on MODULE SETS or PARSE while the build is mid-edit, that is the sibling's
> transient state — wait and re-run, do not "fix" it.

## 0 · Orient, and open a live todo list

`git pull` · `git log --oneline -15` · `git status --short` · `ListAgents` (several
sessions, Claude and Codex, commit here; Codex is invisible to `ListAgents`) ·
`docs/agent/STATE.md` · `prompts/perma/DISPATCH.md` §1 (the bindings). Then read, in
this order:

1. `reports/STILL_NEEDED_SWEEP.md` — the Codex sweep (46 modules, 09-12). Its
   per-module reports are `reports/still-needed/Fix_*.md` and `90_SaveSanitizer.md`;
   the coordinator's proposal is `reports/still-needed/SURFACE_PLAN.md`.
2. `reports/still-needed/WORDING_RULED.md` — **the owner's rulings and the exact text
   that will be applied.** Item 13 (F31) and item 4 (F52) are HELD; the voice rule
   at its top binds your own recommendations too.
3. `docs/PLAYTEST_CHECKLIST.md` item 156 — the rulings in the owner's words.

Put one todo per numbered claim below and update it the moment it changes state; the
owner reads that list to decide when to step in.

## 1 · What this is, and is not

A **surface audit**: you check that what we are about to say in public is true, and
that what we are about to remove is really redundant. It is **not** a re-run of the
46-module sweep. Two systematic module passes exist already (hotfix 2, the migration
audit) and a third (this sweep); the public surfaces have had none until now, and the
owner spotted the last overclaim on the store card himself.

**Standing licence from the owner:** wherever *you* judge a module is closer to
retirement than Codex judged, dig — the whole route, both game trees, callers and
inheritors — and say so with the evidence. The surface scope bounds the default
effort, not your reach.

⭐ **Why this matters more than it used to:** two Paradox developers are using our
fix list to plan their hotfixes (owner, 09-12). A stale or overstated row now costs a
developer's time. Treat every public sentence as an input to someone else's
engineering plan.

## 2 · The deep half — two retirements and one near-retirement

The direction that **retires a live fix** is the dangerous one (`FIX_POLICY.md` §4
"state the defect, never the phrasing": a regex pinned to syntax reports DEFECT-GONE
on a refactor). For each of the three, re-derive from the shipped 1.1.0 body without
reusing Codex's reasoning, then read Codex's report and say where you agree, where
you disagree, and what neither of you checked.

Trees: live `A:\SteamLibrary\steamapps\common\Project Spark\ModTools\Src` = 1.1.0
(`EF-075`); 1.0.7 archived at `C:\Dev\SMR-SrcArchive\1.0.7.396349\Src` (`EF-083`).
**Every citation names its game version.** Never edit either tree.

### Claim A — F37 `Fix_GhostFarmOxygen` is redundant on 1.1.0 (owner: RETIRE)
- The defect (1.0.7): a farm's keyed `air_consumption` dome modifier survived the
  farm's removal. Show the 1.1.0 line that clears it on the working transition and the
  ordinary destroy/salvage order that guarantees the transition runs first.
- **Residue:** the module also carries an `OnMsg.LoadGame` sweep that deletes orphan
  farm-keyed modifiers. Can a 1.1.0-born save carry one? Codex names dying-worker
  refab and scripted `SetDome`/`DoneObject` as unmeasured. Measure or bound them;
  1.0.7-born saves cannot load (`EF-079`), so that constituency is closed.
- External witness exists: the PDX developer could not reproduce it (checklist 150).
  That lowers the weight here — spend your time on B and C.

### Claim B — F43 `Fix_LayoutTechLock` + its F118 rider are redundant on 1.1.0 (owner: RETIRE)
- No external witness. Show the 1.1.0 outer gate (research / owned prefab) that runs
  before every ordinary menu and shortcut activation, and enumerate the activation
  callers — **count inheritors and every caller of the function the module hooks**,
  not the callee (the F59 lesson, `FIX_POLICY` §4).
- Codex names a cached-admission race, custom entry routes and live DLC overrides
  as unchecked. Check the DLC one at least: `EF-075` shipped DLC with 1.1.0.
- **F118**: the rider restores delete-on-load layout registration that F43's own
  filter disturbed (`Code/Fix_LayoutTechLock.lua:99-143`, `bugs/F118.md`). Confirm it
  has **no standalone job** once F43 is gone — i.e. vanilla keeps its registration
  without us. If F118 does something on its own, say so; it is `filed`, never
  reproduced.
- Cross-module consumers: none in `Code/` (the one `IsLockedOut` mention outside the
  module is a comment in `Fix_ArrivalDeaths.lua:343`). TestKit probes retire with it.

### Claim C — F31 `Fix_AnomalyCaveInMap` — **DIG. The owner wants this one settled, not swept.**
Codex's finding: the inspected No Underground trigger/precondition route "cannot
produce the stated stopped-story account"; the cheap guards still have callers. That
puts F31 on the edge of retirement, and the public row currently tells players a story
stopped. Settle it:
1. Read `bugs/F31.md` first. Was the stop ever **observed** (a save, a log, a report),
   or was it derived? Name the artefact or say there is none.
2. ⭐ **The owner's lead, confirmed 09-12 (`smr-bugfixpack-d0`) — start from it:** on
   1.1.0 the "No Asteroids and Underground" rule is **`Obsolete = true`**
   (`Data/GameRuleDef.lua:55-62` @1.1.0; the 1.0.7 definition has no such flag), and
   `Lua/GameRules.lua:71` @1.1.0 says obsolete rules survive only "still active in
   loaded games" — which 1.0.7 saves cannot be (`EF-079`). So **no 1.1.0 game can run
   under that rule**, and the missing-map half of F31 has lost its only known route.
   Confirm the generic `ForEachPreset` Obsolete skip in `CommonLua` and that the
   new-game rules screen builds from it; then check the **other** route the engine
   itself names: `Lua/AgentPlayTest.lua:4` @1.1.0 says the underground map is absent
   "with the NoUndergroundAndAsteroids rule **or a non-Surface map**". What is a
   non-Surface map on 1.1.0, can a player start on one, and can an anomaly/Buried
   Wonder sequence run there?
3. **The other half of F31 is not the missing map at all** (read the entry): eight
   story steps pass the global `UndergroundMap` where every sibling action uses the
   sequence-local `map` (`UndergroundAnomalies.generated.lua:240`, the three Jumbo
   Cave files, Cave of Wonders `:430`). On which maps can those sequences run on
   1.1.0? If only on the underground map itself, the global and the local are the
   same object and the "wrong-map rubble" half is unreachable too. If any can run
   elsewhere, name the map and what the player sees.
4. Walk the eight call sites on **both** trees and quote what `TriggerCaveIn` does with
   `false` (`CaveInRubble.lua:95-101` @1.0.7 per the entry; re-cite @1.1.0).
5. If neither half is reachable on 1.1.0, the row claims a symptom nobody can have on
   the live branch → recommend **RETIRE** (module out under H-10, row and headline
   off, counts re-derived); state separately whether 1.0.7 players under the rule
   ever could have hit it (the frozen v5 build keeps the module regardless).
6. If a guard with a real player-visible reach survives, write the plain row for it
   in the voice rule and say what the headline should be, if any.
Do not soften an unconfirmed sentence into a different invented symptom.

## 3 · The surface half — the ruled wording, items 1–12 and 14

For each replacement in `WORDING_RULED.md`, one claim: **the new sentence is true on
1.1.0 and no stronger than what was measured**, and it satisfies the voice rule. Check
it against the entry (`agent/bugs/<ID>.md` is the authority), the module's
`-- SRC:`/`-- DEFECT:` header, and the shipped 1.1.0 line. Where a sentence is true
but you can say it plainer, offer the plainer sentence — the owner is the author and
rejects word salad on sight.

Two are pre-settled, do not redo them unless you find them wrong:
- **F21 stays** (item 5): the double-counted duration still feeds the "Travel time
  (rolling average)" line on train and track panels on 1.1.0
  (`ColonistTransport.lua:671`, `:696-697`; `ipTrain.generated.lua:85`,
  `ipTrack.generated.lua:186`); only the Comfort charge is gone.
- **F52 held** (item 4): no change.

Then the whole-list arithmetic at the bottom of `WORDING_RULED.md`: re-derive the
counts from the actual list once and say whether they hold.

## 4 · Output

- `reports/SURFACE_AUDIT_2026-09-12.md`: **disagreements first**, then every claim
  numbered with verdict CONFIRMED / REFUTED / UNMEASURED and its evidence
  `file:line@version`; a "what I did not check" list by name; an ideas list kept
  separate from findings.
- Checklist: one item under "Decisions waiting on you" carrying **only** what the
  owner must decide (F31's fate; anything you moved toward retirement; any wording you
  want changed), in the owner's plain register.
- ⛔ **Touch no public surface, no `Code/`, no `items.lua`, no `metadata.lua`.** The
  release lane (`perma/RELEASE.md` → `PUBLIC_SURFACE_SWEEP.md`, the outbox's
  **Held after-v9** batch) applies the rulings after this report.
- Commit by pathspec (`git commit -F <msg> -- <paths>`), `python tools/doccheck.py`
  GREEN first, push, `git rm` this prompt in the same commit. Append the leg to
  `archive/SESSION_LOG.md`.

## 5 · What you may not do

Retire anything yourself. Launch the game to "just check" without the stale-probe gate
(`DISPATCH.md` §0.4). Quote a count you did not emit. Rest a verdict on Codex's
agreement with itself — three agents under one coordinator are one instrument.
