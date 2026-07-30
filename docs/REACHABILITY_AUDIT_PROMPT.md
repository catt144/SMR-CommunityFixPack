# One-off prompt — REACHABILITY AUDIT of the fix pack

Paste everything below into a **fresh session**, any Claude model (this project
is model-agnostic; the user picks per task). This is a **game-free, read-only
investigation** — the user is not at the keyboard in the game, and nothing here
requires it. Written 2026-07-30, out of the F24 close.

**Delete this file when the audit is done and its findings are recorded.**

---

## The question

**For every fix in this pack: can a player reach the defective state by playing
the shipped game — no mods, no console, no developer tooling?**

Not "is the defect real." That is already established per fix, with file:line
evidence. The question is whether the broken code path is *reachable in normal
play*, and therefore whether fixing it buys a player anything.

## Why this is being asked now — the F24 precedent

On 2026-07-30 the owner sat down to run PT-44's F24 half and found the test
**impossible to perform**. What followed is the template for this whole audit.

F24 was a genuine defect: `LifeSupportGridObject:MoveInside` passes `dome` to
`WaterGrid.DestroyConnection` where its electricity twin passes `self`
(`LifeSupportGrid.lua:304` vs `ElectricityGrid.lua:291`) — the two functions are
otherwise line-for-line identical. It had file:line evidence, it satisfied
FIX_POLICY §4, and it shipped as a 34-line full-function replacement.

Then the reachability question was asked, and it died in three steps:

1. **Enumerate every call site.** `MoveInside` has exactly two in all of `Src`.
2. **Eliminate the ones that cannot execute the defective body.**
   `MartianAssembly.lua:60` is live in play, but `SpireBase.__parents =
   { "Building" }` and the template declares no water or air — so
   `LifeSupportGridObject:MoveInside` is not in that class chain at all.
3. **Interrogate the survivor's precondition.** `Dome:OnLoad`
   (`Dome.lua:896-899`) needs a *pipe-connected life-support building inside a
   dome's interior hexes whose `parent_dome ~= self`, still holding live
   connections*. Vanilla cannot produce that: a dome refuses to place over
   existing buildings ("Objects underneath are blocking construction",
   confirmed in play across dome types, sizes and angles); **no dome template
   carries any upgrade** (every `Data/BuildingTemplate/*Dome*.lua` checked, zero
   `upgrade*_id`); and nothing mutates a dome's interior shape at runtime.

Verdict: real defect, unreachable in vanilla, carried at the cost of the
most fragile patch class in the policy. The user closed it `wontfix` and
deleted it (`dd72923`). Full write-up is on the F24 entry in `BUGS.md`.

**Also note where the defect came from: it was never a player report.** It was
found by diffing the water grid against its electricity twin. That provenance
is the strongest single predictor of this failure mode.

## Why the existing policy does not catch this

`FIX_POLICY.md` §4 says: *"Only fix proven defects. Every fix links to a BUGS.md
entry with file:line evidence."*

F24 satisfied that completely. **The policy has never required proof that a
player can reach the defect.** Closing that gap is part of this audit's
deliverable (see "Deliverable 3").

## Scope

`Code/` currently holds **66 `Fix_*` modules** plus 7 `Opt_*` (opt-in behavior
changes — **out of scope**, they are preferences, not defect repairs) plus
`00_Core.lua` and `90_SaveSanitizer.lua` (the sanitizer's two passes ARE in
scope). Read `docs/STATUS.md` for the authoritative counts before starting;
they change.

**Audit all of them**, but spend effort in this order:

1. **Fixes implemented as FIX_POLICY §1.5 full replacements or
   reconstructions.** These are the expensive ones — they rot on every game
   patch and are the most likely to clash with other mods. An unreachable §1.5
   fix is pure liability. F24 was one.
2. **Fixes whose BUGS.md entry shows no player report** — the tell is language
   like "confirmed by comparing with the sibling", "the twin passes `self`",
   "dead validation", "never inserted", "never called". Source-diff provenance.
3. **Fixes already classified latent** — `F28`, `F43`, `F25` are recorded in
   STATUS.md as "correctly untestable in play". Confirm or correct those
   classifications with the same rigour; they were asserted, not proven.
4. Everything else.

**A `tested` status does NOT automatically prove reachability.** It proves it
only if the playtest reached the state *by playing* — if the PT manufactured the
state with console surgery, `g_Consts` compression, or a `Cheat*` call, the
reachability question is still open. Check what the PT actually did in
`PLAYTEST_ARCHIVE.md` before crediting it.

## Method — per fix

1. Read the BUGS.md entry. Note the **implementation technique** (which
   FIX_POLICY §1 tier) and the **provenance** (player-reported vs source-diff).
2. Identify the exact defective function and, where it matters, the defective
   *branch* inside it.
3. **Enumerate every call site in `Src`.** Grep the whole tree; exclude
   definitions and delegating overrides. Do not trust the BUGS entry's own list
   — it may be incomplete or stale.
4. For each call site, ask whether it can actually execute the defective body:
   class chain (is the patched class even in it?), guards, early returns,
   template data that gates it.
5. For every survivor, ask: **what player action produces the precondition?**
   Name it concretely — a building, a game rule, a sponsor, a mystery, a
   disaster, a milestone, a map-generation path, a savegame fixup.
6. Try to **falsify unreachability**. Look for the mechanic that WOULD produce
   the state: search building templates, game rules, `Cheats.lua`, map presets,
   `SavegameFixups`, mystery scripts. Absence of evidence is only worth
   recording if you actually went looking.
7. Assign a tier and a recommendation.

**Stance: argue to SAVE each fix, not to kill it.** The failure mode of this
audit is over-pruning — declaring something unreachable because you did not
find the path, when it exists. A verdict of R4 requires you to state *what you
searched* and why the search was exhaustive. When genuinely unsure, use `U`.
`U` is a perfectly good answer and much cheaper than a wrong deletion.

## Reachability tiers

| Tier | Meaning |
|---|---|
| **R1 — Live** | Ordinary play reaches it. Most players will hit it. |
| **R2 — Conditional** | Reachable, but needs specific real conditions: a game rule, a sponsor, a mystery, a breakthrough, a legacy save, a specific map. Still a genuine player experience. |
| **R3 — Latent by data** | The code path is reachable in principle, but no shipped data exercises it (the F43 shape: the one shipped layout has no tech-locked entry). Would become live if a patch or another mod added the data. |
| **R4 — Unreachable** | No path in the shipped game produces the precondition. The F24 shape. |
| **U — Unknown** | Could not be settled from source alone; say exactly what observation would settle it. |

## Decision rules (recommendations only — every deletion is the user's call)

- **R1 / R2** → keep, no action.
- **R3** → keep if the patch is cheap (data/preset patch, additive handler,
  chained wrapper — policy §1.1-§1.4). **Flag for the user** if it is a §1.5
  full replacement: latent benefit, permanent maintenance cost.
- **R4** → **deletion candidate.** Weigh the patch cost the way F24 was
  weighed: a one-line data patch that guards modded or legacy saves may be
  worth keeping (the F28/F43 precedent); a full-function replacement almost
  certainly is not.
- **U** → keep, and record the observation that would settle it. Some of these
  will become playtest items.

## Deliverables

**1. `docs/REACHABILITY_AUDIT.md`** — a new file. One row per fix:

| Fix | Technique (§1 tier) | Provenance | Call sites | Tier | Recommendation |

Plus a per-fix paragraph for anything not R1, giving the actual reasoning —
call sites enumerated, preconditions named, what you searched. This file has to
be good enough that nobody re-derives it in six months (the F24 entry is the
model for the level of detail expected).

**2. A short DELETE-candidate list** at the top of that file — the R4 fixes
with expensive patches, each with a one-line cost/benefit. This is what the
user actually decides from. Do not delete anything yourself.

**3. A proposed FIX_POLICY §4 amendment** — draft wording that requires
reachability to be established and recorded before a fix ships, with the tier
vocabulary above. Put the draft in the audit file; do not edit `FIX_POLICY.md`
without the user's go-ahead.

**4. Any new findings** the audit turns up (defects noticed en route, entries
whose evidence does not survive re-reading) go on their BUGS.md entries as
normal, flagged clearly as audit output.

## Hard constraints

- **Game source is READ-ONLY and never modified:**
  `A:\SteamLibrary\steamapps\common\Project Spark\ModTools\Src`. The shipped
  build IS Src (fpk parity proven, `ENGINE_FACTS.md`) — you can trust file:line.
- **Do not delete, disable or edit any fix.** This audit produces a report.
- **Do not run the game.** Nothing here needs it.
- **Do not trust `BUGS.md`'s own claims** — several entries have been corrected
  by re-reading (the F24 QA correction, the PT-38 premise inversion, the
  `GetCameraLookAtPassable` withdrawal). Verify against `Src`.
- Read `docs/ENGINE_FACTS.md` first — several behaviors are the opposite of
  what the code suggests, and misreading them will produce wrong verdicts
  (mod code loads before class flattening; `error()`/`assert()` do not unwind;
  `IsValid()` is falsy for pure-Lua objects; presets exist EMPTY before
  `DataLoaded`).
- Commit with
  `git -c user.name="SMR-BugFixPack" -c user.email="154917955+catt144@users.noreply.github.com"`,
  and push.

## Two method notes earned the hard way, same day

- **Do not inject UI internals to manufacture a test state.** While trying to
  run PT-46's F49(a) half, the assistant handed the user
  `GetInGameInterface():SetMode("track_grid", {grid_elements_require_construction = false})`
  to force the instant track-placement path. There is **no player-facing
  control that does this**; cancelling out of the injected mode left an orphan
  `Track` object with invisible elements blocking grid hexes on a 305-sol
  colony. The debris was an artifact of an unreachable entry path — not a bug
  in anything — and the project already had a hard rule against exactly this
  (the F76 lock-up lesson). It was violated anyway. **If a state can only be
  produced by injection, that is itself evidence for R4.**
- **F49(a) is an open item for this audit.** Its trigger is instant-placed
  track (`place_track`, `Tracks.lua:386`), documented as used by "map setup,
  cheats, and the instant-build rule". **Nobody has verified that any of those
  three is player-reachable.** If no shipped map pre-places track and no
  player-facing rule or cheat does either, F49(a) is in F24's category — with
  the extra mitigation that it self-corrects the moment the player changes
  colour scheme (`ColonyColorScheme.lua:120-121` repaints every
  `TrackGridElement`). Settle this one first; it is the live example.

## Starting context

Read in this order: `docs/ENGINE_FACTS.md` (all of it), `docs/STATUS.md`
(current counts and state), `docs/FIX_POLICY.md` (§1 technique tiers and §4 —
the clause this audit amends), then `docs/BUGS.md` per fix as you go. The F24
entry is the worked example of both the method and the write-up standard.
`docs/archive/SESSION_LOG.md`'s newest legs carry the 2026-07-30 context.
