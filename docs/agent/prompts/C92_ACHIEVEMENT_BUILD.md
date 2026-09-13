# C92 — build the achievement repair (HARD-GATED TO PLAYTESTING)

One-off, authored 2026-09-13 at the owner's ask. Tool-neutral (Claude or Codex).
`git rm` this file when it has reported. Defect truth: [C92](../bugs/C92.md).
Evidence: [C92_PLACEMENT.md](../reports/C92_PLACEMENT.md) (current) and
[C92_INVESTIGATION.md](../reports/C92_INVESTIGATION.md) "Addendum 2026-09-13".

## 0 · ⛔ THE HARD GATE — read before anything else

⛔ **NOTHING SHIPS WITHOUT A PLAYTEST. This is the owner's gate, not a preference.**
Build it, desk-control it, and then **STOP**. No release, no `RELEASE_OUTBOX` entry,
no public row, no version bump, no store text. The module may land in `Code/` with
its status short of `fixed`; it may **not** reach a player until the owner has
watched it in the game.

⚠️ **And be honest about what the playtest can and cannot show.** The owner's account
already reports `ResearchedAllTechs` unlocked, so **a first award cannot be witnessed
on this rig**. Say in your report exactly which legs the sitting can settle and which
are structurally unavailable — do not let "playtested" imply "award observed".

⛔ **Decision 171 is still formally OPEN** (`docs/PLAYTEST_CHECKLIST.md`, option A
repair / B finish / C defer, recommendation A). Firing this brief presumes **A**. If
the owner has not ruled, say so in your first todo update and ask rather than assume.

## 1 · Your licence

The evidence below is **claims**, including the confident parts — house doctrine
(`CLAUDE.md`). Two passes have already corrected themselves on this defect; assume a
third error and look for it.

- ⭐ **Go anywhere, and question anything here.** If the design below is wrong, say so
  and propose better. Refuting this brief is a good outcome.
- ⭐ **If you find a cleaner seam than the one in §3, take it** and explain why.
- ⛔ Report-only constraints do **not** apply here — this brief authorises a **build**.
  It does not authorise a release, a game launch without asking, or a save edit.
- ⛔ **Shared tree**: peers edit concurrently, **Codex is invisible to `ListAgents`**.
  `git log` / `git status` before any write; commit with a pathspec.
- ⛔ **H-10**: a new `Code/*.lua` module MUST be added to `items.lua`, or it ships
  absent — `SaveDef` rebuilds `metadata.lua`'s `code` list from items alone.
- ⛔ **H-02**: never open the Mod Editor, never hand-set `version`.

## 2 · What the defect is, in one paragraph

`ResearchedAllTechs` ("The Boundaries of Knowledge") counts every non-obsolete tech in
nine tracked groups. `UndergroundExploitation` (`Underground_1`) is `LockState="hidden"`
with no `RequireTech` and no reveal route, so it can never be researched — and the
preset iterator skips obsolete techs but **not** hidden ones
(`CommonLua/Preset.lua:1802-1815`). A player who completes the entire visible tree
still fails. MEASURED on the reporter's Sol 490 save: excluding only that one preset
makes the all-group predicate pass.

⛔ **Withdrawn, do not reason from them:** the ≈44% water-bonus claim (the two
production paths serve **separate** output systems and each apply 20%), the
"never-drawn icon" claim, and "unremovable residue".

## 3 · The seam, and the traps around it

**SOURCE, the patch seam.** The vanilla filter and the tracked-group list are **file
locals** in `Lua/Achievements.lua` — a mod cannot assign them by name. The route is a
**focused additional achievement listener** that evaluates the existing groups with
the narrow exemption and calls the engine's normal `AchievementUnlock`, leaving the
vanilla listener and every other sponsor achievement untouched.

⛔ **Do NOT globally redefine `IsTechResearched` or `Research:IsTechGroupResearched`
to manufacture completion.** The declaring class for the latter is `Research`, not
`Colony` (the §2 self-check-on-the-declaring-class rule, the F64 lesson).

⭐ **The recovery trap — a filter fix alone does not repair the reporter.** The
vanilla listener returns on `not first_time` (`Achievements.lua:21-23`), and in that
save both repeatables have already completed once, so **there is no ordinary first
completion left to trigger anything**. Your fix must state its recovery trigger: a
repeat-research event re-evaluating the corrected predicate, and/or a properly ordered
post-load check that awards an already-eligible colony. Engine account/platform/
tutorial/game-rule restrictions still apply and must not be bypassed.

## 4 · ⛔ The decline test is REQUIRED, not optional

If the vendor wires the tech and we keep exempting it, we award the achievement to
players who have **not** researched a now-reachable technology — the inverse defect,
and worse than the bug. Any build must carry a stand-down.

**Behaviour/shape test, never a version or `LuaRevision` label** (`FIX_POLICY` §2a;
`LuaRevision` may be an observation label, never a guard). Any one of these means
stand down:

1. `next(Techs.UndergroundExploitation.RequireTech)` is non-empty — it got connected;
2. its `LockState` is no longer `"hidden"` — it got revealed;
3. the preset reports `Obsolete` — retired, so vanilla's iterator skips it and the
   achievement passes unaided;
4. the preset is **absent** entirely.

Confirm all four are detectable at the seam your fix actually uses, and say what the
fix does in case 4 specifically. ⛔ §2a: an **UNKNOWN probe answer DECLINES**; only a
literal `true` applies, and an agent never self-authorises an exception.

⚠️ **If you think this argument is wrong, say so** — it is the previous pass's
reasoning, not a measurement.

## 5 · The poison-pill option — evaluate, do not assume you need it

⭐ **A self-healing residue seam was found 2026-09-13: [`EF-093`](../facts/EF-093.md).**
Vanilla runs `PreProcessLockablePresets()` on **every** load (`OnMsg.PostLoadGame`),
re-seeding any `LockablePreset` missing from the owner's persisted
`ProcessedLockablePresets` with that preset's **declared** `LockState`. So a mod that
clears a lock reason *and* drops the preset from that set leaves a save **vanilla
itself repairs** on the next load — no mod code left behind, no cleanup artifact, no
player action.

**How it bears on this build:**

- **If your design writes nothing to the save** — which the standing recommendation
  believes of a listener-only repair — **you need no pill at all.** Say so explicitly
  and show it; a demonstrated zero-footprint fix is the best outcome here.
- **If any variant you choose touches lock state**, `EF-093` is the residue answer,
  and it is better than a self-destruct or a rescue artifact because it leaves nothing
  to recall or patch.
- ⚠️ `EF-093` is **SOURCE-derived and never observed in play**, and carries an
  unverified ordering dependency (our `PostLoadGame` handler must run after vanilla's
  re-seed). ⛔ Do not build on it without your own controls.

⚠️ **Save-footprint claim required either way.** State what this module writes to a
savegame, and what remains if a player deletes the pack. `FIX_POLICY` §3a wants a
recorded disposition per exposed site — "nothing" is a fine disposition, but it has to
be shown, not asserted.

## 6 · Acceptance demands

On a **copy** of the reporter's save, with autosaves pre-backed-up (⛔ `H-06`/`EF-056`:
loading a copy still runs that campaign's autosave rotation and can delete the owner's
autosaves):

- the corrected predicate **accepts** this completed save;
- it still **refuses** a never-completed repeatable and a missing ordinary tech;
- it re-evaluates an already-eligible colony **without forcing a tech flag**;
- the decline fires on each of §4's four shapes (synthetic is fine — say it is);
- behavioural decline on the frozen `v5-game-1.0.7` branch (`FIX_POLICY` §2a / ck118);
- the module applies cleanly in a full boot: `applied` line present, no error-shaped
  lines, exit 0.

⛔ **A live first-award outcome needs an eligible account and this rig does not have
one.** Record that as unavailable, never as passed.

## 7 · Deliverable

Module in `Code/`, registered via `SMRFixPack.Register`, gated via
`SMRFixPack.Require` with **every `(class, method)` pair it installs on or captures
from** in its own `Require` block (the F107 rule, §2). `items.lua` updated (H-10). A
build report at `docs/agent/reports/C92_ACHIEVEMENT_BUILD.md`. Update
[C92](../bugs/C92.md) — status may move to `fixed` **only** if the ship line is met,
and `tested-attended` **only** after the owner has watched it; change the front matter
**and** the body heading tag together. Add the playtest recipe to
`docs/PLAYTEST_CHECKLIST.md` with its marker so the owner can run the sitting.

⛔ **No `RELEASE_OUTBOX` Pending entry, no public row, no store text** — those belong
to the release after the playtest gate clears.

Label claims SOURCE / MEASURED / INFERRED, keep a **Not opened** list, state what each
refutation depends on. `doccheck` GREEN before committing; commit with a pathspec after
checking `git status`.

## 8 · Live todo list — change it as you go

- [ ] 1. Orient; confirm decision 171 is ruled A (ask if not)
- [ ] 2. Design the listener seam; confirm it needs no local-filter assignment
- [ ] 3. Recovery trigger for an already-complete colony — named and justified
- [ ] 4. Decline test, all four shapes, behaviour-only
- [ ] 5. Save-footprint claim; `EF-093` only if anything is written
- [ ] 6. Desk controls incl. the refusal cases and the 1.0.7 decline
- [ ] 7. Module + `items.lua` + build report + entry update
- [ ] 8. Playtest recipe on the checklist with its marker — then **STOP**
- [ ] 9. doccheck GREEN; committed with a pathspec; this prompt `git rm`'d
