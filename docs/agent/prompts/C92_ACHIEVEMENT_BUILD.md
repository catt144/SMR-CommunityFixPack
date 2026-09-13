# C92 — restore the technology (BUILD + TEST; ⛔ SHIPPING IS HELD)

One-off, reshaped 2026-09-13 on the owner's direction. Tool-neutral (Claude or Codex).
`git rm` this file when it has reported. Defect truth: [C92](../bugs/C92.md).
Evidence: [C92_PLACEMENT.md](../reports/C92_PLACEMENT.md) (current),
[C92_INVESTIGATION.md](../reports/C92_INVESTIGATION.md) "Addendum 2026-09-13",
and [`EF-093`](../facts/EF-093.md) (the self-healing residue seam).

## 0 · ⛔ THE HOLD — read before anything else

**Owner ruling, 2026-09-13:**

> *"We will be holding it open as a fix, I want to test it, and then we may ship it,
> but shipping is on hold until I lift the hold. Right now I want to finish it,
> because even if we never ship it I think we will gain valuable knowledge attempting
> it along with the poison pill part of the testing."*

⛔ **SHIPPING IS HELD.** No release, no `RELEASE_OUTBOX` Pending entry, no public row,
no store text, no version bump, no site copy. The module lands in `Code/`; it does not
reach a player until the owner lifts the hold **in words**.

✅ **Building and testing ARE authorised** — that is the point of this brief.

⭐ **KNOWLEDGE IS A FIRST-CLASS DELIVERABLE HERE, not a consolation prize.** The owner
has said outright this may never ship. So when something cannot be done, or behaves
unexpectedly, or costs more than it looked — **that finding is the product**. Write it
down as carefully as you would a working module. A brief that comes back "we tried,
here is precisely where it breaks and why" has succeeded.

⚠️ This supersedes the earlier shape of this brief (a narrow achievement exemption,
option A under checklist 171). The owner has chosen to **finish the technology**.
Decision 171 is not thereby ruled — it remains the owner's, and the hold is what keeps
that true.

## 1 · Your licence

Everything handed to you below is a **claim**, including the confident parts — house
doctrine (`CLAUDE.md`). Three passes have now corrected themselves on this defect
(a wrong game install; an overstated "no cross-version diff"; a wrong ≈44% bonus).
**Assume a fourth error is in here and go looking for it.**

- ⭐ **Go anywhere, question anything.** If the design below is wrong, refuting it is
  a better outcome than implementing it.
- ⭐ **Chase your own hypotheses.** The structure below is a starting point, not a
  syllabus.
- ⛔ This brief authorises a **build**. It does not authorise a release, a save edit,
  or a game launch without asking the owner first.
- ⛔ **Shared tree.** Peers edit concurrently and **Codex is invisible to
  `ListAgents`**. `git log` / `git status` before any write; commit with a pathspec;
  ⚠️ a pathspec protects every *other* file but commits the working-tree content of
  any path you name.
- ⛔ **H-10:** a new `Code/*.lua` module MUST be added to `items.lua` or it ships
  absent. ⛔ **H-02:** never open the Mod Editor, never hand-set `version`.

## 2 · What we are building, and why it is defensible

`UndergroundExploitation` (`Underground_1`) is `LockState="hidden"` with no
`RequireTech` and no reveal route, so it can never be researched. Two consequences:
the tech's +20% underground-extractor bonus is unobtainable by anyone on 1.1.0 (it
shipped and worked in 1.0.7 as a law), and `ResearchedAllTechs` counts it, so the
achievement is unobtainable too.

⭐ **Restoring reachability repairs BOTH, and repairs the achievement through
vanilla's own path** — the player researches the tech, vanilla's own listener fires on
that first completion, and no exemption, no faked predicate and no manufactured award
is involved anywhere. That is a real argument for this route that the earlier
recommendation did not make, and it is worth stating in your report either way.

⛔ **Withdrawn — do not reason from them:** the ≈44% water-bonus claim (the two
production paths serve separate output systems, each applying 20%), "never-drawn
icon", and "unremovable residue".

## 3 · Reachability — the design decisions that are genuinely open

**SOURCE:** `UnlockTech(...)` (`CommonLua/Libs/Research/Research.lua:31-38`) clears
both `hidden` and `locked` reasons, giving state `enabled`, which `IsVisibleOnMap`
and `Player:CanResearch` both accept. It cannot self-heal because
`CheckUnlockPrerequisites` needs `IsTechUnlocked` when `RequireTech` is empty.

What the placement pass could **not** recover, so these are **design choices you are
making, not intent you are restoring** — say so plainly in the report:

- **Seat.** Underground I's ring is complete; the satellite row at y=3200 has empty
  hexes at 9470, 9618, 9914, and `(9914,3200)` bridges to Industry V. The two other
  underground law conversions landed at `(9766,3200)` and `(9322,3200)`.
- **Prerequisite.** `RequireTech` connections are **OR**, not AND — connecting two
  siblings means either one opens it. That is a progression decision.
- **Art.** No dedicated research icon exists. The best retired candidate found is
  `closed_loop_extraction.png`. All 356 tech icons come from `UI/Icons/Research/`;
  **zero** use law art, so the law's own `underground_exploitation_*.dds` would break
  a 356/356 convention.
- **The dropped `Condition`.** The 1.0.7 law carried
  `not IsGameRuleActive("NoUndergroundAndAsteroids")`. Restoring it is plausible;
  decide and justify.

⛔ **The decline is still required.** If the vendor wires the tech and we keep forcing
it, we are fighting their fix. Behaviour/shape test, never a version label
(`FIX_POLICY` §2a — `LuaRevision` may be an observation label, never a guard): stand
down when `RequireTech` is non-empty, when `LockState` is no longer `"hidden"`, when
the preset is `Obsolete`, or when it is absent. §2a: an **UNKNOWN answer DECLINES**.

## 4 · Residue and the poison-pill work — an explicit learning goal

⭐ **[`EF-093`](../facts/EF-093.md) is the centrepiece and the owner wants it
exercised.** Vanilla runs `PreProcessLockablePresets()` on **every** load
(`OnMsg.PostLoadGame`), re-seeding any `LockablePreset` missing from the owner's
persisted `ProcessedLockablePresets` with that preset's **declared** `LockState`. So a
mod that clears the lock reason *and* drops the preset from that set leaves a save
**vanilla repairs by itself** — no mod code left behind, no cleanup artifact, no
player action.

**Prove or disprove it.** It is SOURCE-derived and has **never been observed in play**.
It carries an unverified ordering dependency: our `PostLoadGame` handler must run
**after** vanilla's re-seed for the suppression to hold while installed.
⇒ **Either outcome is a good result.** If the seam works, the pack gains a residue
class it has never had. If it does not, say exactly where it fails — that is worth as
much.

**What `EF-093` does NOT cover:** if the player actually researches the tech,
`tech_researched` is written and the vanilla consumer keeps paying the bonus with our
pack gone. Decide and state the contract: leave it (player-earned progress), or add a
`90_SaveSanitizer`-style reversal with a tech-point refund. ⚠️ A reversal is
**destructive code you cannot test against the future patch that triggers it** — desk
controls with scratch variants are the honest substitute, and its trigger should be
the *shape fingerprint*, not a version compare.

⚠️ **Save-footprint claim required.** State exactly what this module writes to a
savegame and what remains if a player deletes the pack. `FIX_POLICY` §3a wants a
recorded disposition per exposed site.

## 5 · ⭐ Testing achievements — the owner asked, and here is the answer

**The flag is exactly what the owner assumed:**
`AccountStorage.achievements.unlocked["ResearchedAllTechs"]`, a plain boolean
(`CommonLua/Classes/Achievement.lua:39-40`).

**It persists to** `C:\Users\stkot\Saved Games\Surviving Mars Relaunched\76561198020568696\account.dat`
— written by `SaveLuaTableToDisk(AccountStorage, folder .. "account.lua", g_encryption_key)`
(`CommonLua/AccountStorage.lua:104-110`), i.e. **encrypted**, so hand-editing is not
a route.

⭐ **Sync is ONE-WAY, local → Steam.** `SynchronizeAchievements` pushes local unlocked
keys up (`Platforms/steam/SteamAchievements.lua:98-115`); **nothing reads Steam back
into `AccountStorage`.** Consequences:

- ✅ **Clearing the local flag STICKS** — Steam will not restore it, so the game can be
  made to behave as if the achievement were unearned.
- ⛔ **Steam's own copy is permanent** and there is no route from inside the game to
  clear it. A test can never un-earn it on the platform.

⛔ **No mod can clear it.** `ModEnvBlacklist` (`CommonLua/Modding/Mod.lua:1281-1291`)
blocks `AccountStorage`, `SetAccountStorage`, `SaveAccountStorage` and
`InitDefaultAccountStorage`; `AsyncAchievementUnlock` is blocked at `:1336`. So
neither the fix nor the Test Kit can reset anything. ✅ `AchievementUnlock` and
`GetAchievementFlags` are **not** blacklisted — the fix can unlock and query.

⭐ **The clean testing lever:** `AchievementUnlock(achievement, dont_unlock_in_provider)`
— a **truthy second argument sets the local flag without calling Steam at all**
(`Achievement.lua:140-152`). Exercise the whole award path with zero platform side
effects.

**The safe reset procedure — propose it to the owner, do not perform it unasked:**

1. **Back up `account.dat`** before any test. This is the whole remedy: restoring the
   copy restores every achievement exactly, with no decryption and no partial edits.
2. Clear **one key only**, never the table — the console is the likely route (it runs
   outside the mod sandbox, and the Test Kit already has a console-enable path;
   ⚠️ **verify that** rather than assuming it).
3. Restore the backup when testing is done.

⛔ **HAZARD, state it to the owner before they touch anything:** because sync is
one-way, a local wipe is **permanent for the in-game list** — nothing restores
`AccountStorage` from Steam. Clearing the whole `unlocked` table would erase the
owner's entire in-game achievement record with no recovery except the `account.dat`
backup.

## 6 · Acceptance

On a **copy** of the reporter's save (⛔ `H-06`/`EF-056`: loading a copy runs that
campaign's autosave rotation and can delete the owner's autosaves — pre-copy every
autosave first):

- the tech becomes visible and researchable, and researching it awards the achievement
  **through vanilla's own listener**;
- the bonus applies at the authored rate, on the right buildings, once;
- the decline fires on each of §3's four shapes (synthetic is fine — say it is);
- behavioural decline on the frozen `v5-game-1.0.7` branch (`FIX_POLICY` §2a / ck118);
- **the `EF-093` seam**: with the module removed, the next load restores `hidden` by
  vanilla's own hand — measured, not assumed;
- a clean boot: `applied` line present, no error-shaped lines, exit 0.

## 7 · Deliverable

Module in `Code/`, registered via `SMRFixPack.Register`, gated via `SMRFixPack.Require`
with **every `(class, method)` pair it installs on or captures from** in its own
`Require` block (the F107 rule). `items.lua` updated (H-10). Build report at
`docs/agent/reports/C92_RESTORATION_BUILD.md` — and it must carry the knowledge, not
just the outcome: what the `EF-093` seam did, what the residue contract is, what could
not be done and why.

⛔ **Status may NOT reach a shipped state.** `fixed` implies the ship line is met and
the hold says otherwise — keep C92 at `cand` (or move to a held status only with the
owner's word), and change the front matter **and** the body heading tag together.
Put the playtest recipe on `docs/PLAYTEST_CHECKLIST.md` with its marker, and put the
**achievement backup/reset procedure in front of the owner there** before any sitting.

Label claims SOURCE / MEASURED / INFERRED, keep a **Not opened** list, say what each
refutation depends on. `doccheck` GREEN before committing; commit with a pathspec
after checking `git status` for a peer's uncommitted work.

## 8 · Live todo list — change it as you go

- [ ] 1. Orient; confirm the hold is understood and nothing ships
- [ ] 2. Seat / prerequisite / art / `Condition` — decide each, justify as a choice
- [ ] 3. Reachability built; decline test, all four shapes, behaviour-only
- [ ] 4. `EF-093` seam exercised — prove it or show where it fails
- [ ] 5. Residue contract for a researched tech; refund question answered
- [ ] 6. Desk controls incl. the 1.0.7 decline and the removal leg
- [ ] 7. Achievement backup/reset procedure written for the owner, not performed
- [ ] 8. Module + `items.lua` + build report + entry update (no shipped status)
- [ ] 9. Playtest recipe on the checklist with its marker — then **STOP**
- [ ] 10. Your own findings, including everything that did not work
