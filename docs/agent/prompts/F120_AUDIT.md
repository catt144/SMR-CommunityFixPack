# F120 audit — did the Wildfire fix miss anything?

**Authored 2026-09-16 against `aacf700`.** Game baseline **1.1.0.403908** + DLC.
⛔ Start with `git log --oneline -10` and `git pull`; the records win over this brief.

⚖️ **Cross-vendor by design.** F120 was investigated and built by **Astra (Codex)**. This audit is
fired on **Fable** so no vendor sits on both sides of the check. ⛔ Do not treat the builder's
reasoning as settled because it is written down — re-derive the route, not just the citations.

⭐ **You have the same wide licence the investigation had.** Explore freely, launch the retail game
if you want it, write throwaway probes, follow a lead this brief never mentions. **You may expand the
fix** — widen its scope, change its shape, or replace it — if the evidence takes you there. You may
also conclude it is correct as built; a clean audit that says so with its reasons is a real result.

## 1 · What is under audit

| artifact | what it claims |
|---|---|
| [`bugs/F120.md`](../bugs/F120.md) | the defect, cause, reachability, controls and repair contract |
| [`Code/Fix_WildfireCureMigration.lua`](../../../Code/Fix_WildfireCureMigration.lua) | 92 lines; `recover()` on `OnMsg.PostLoadGame`, gated by `SMRFixPack.WhenActive` / `Require` |
| [`reports/WILDFIRE_CURE_RESEARCH.md`](../reports/WILDFIRE_CURE_RESEARCH.md) | the investigation and its retained negative results |
| `items.lua` / `metadata.lua` | the module is **registered and would ship** in the next upload |

**The reported symptom (INHERITED, unverified):** Steam, **Jäger**, 2026-09-14, owner-relayed —
*"I seem to be having an issue with the Wildfire Mystery, there is no option to research the cure in
the new tech tree."* ⛔ No log, no save, no mod list, no sol count.
⛔ **Do not ask the reporter for anything.** Owner ruling 2026-09-15: players are uncomfortable
sharing saves and the request confuses non-technical users. The desk, the kit and your own game come
first; a save is the owner's call, not yours.

**The stated cause:** legacy `Research:AddTech` stored `field='Mysteries'`; the tech-point converter
preserves only BuriedWonders / Storybits / Breakthroughs, so a cure revealed before conversion stays
hidden. The repair restores **only that entrance**, **only** in a Wildfire colony with a positive
legacy discovery and an entirely hidden shipped family.

**Its own declared limits, which are the audit's starting point, not its conclusion:**
- *"This does not explain a fresh Steam colony's missing cure."*
- *"retail recovery and reporter cause unconfirmed"* — desk A/B only, never run in the retail game.
- Reach is platform-conditional: ordinary Steam **blocks** pre-402200 legacy loads; non-Steam retail
  offers Load anyway.

## 2 · The question the owner actually asked

**Did it miss anything?** Three directions, none authoritative — find your own if they are better.

⭐⭐ **A · Is the fix too narrow by its own logic?** If the converter drops `field='Mysteries'`
wholesale, then **every mystery tech discovery is dropped, not only `WildfireCure`**. There are
**16 mystery techs across 11 mysteries** (`Data/TechPreset.lua`, `group = "Mysteries"`), and **five
tech families are chained and remapped** — `WildfireCure`(10), `BottomlessPitResearchCenter`(3),
`AncientArtifactAdaptedMachine`(3), `AlienDiggersDestruction`(3), `AlienDiggersDetection`(2), matching
`MysteryTechRevealRemapping` (`Lua/Sequences/SA_Gameplay.lua:1188-1195`) exactly. The fix is named
and gated for Wildfire alone. **Is that a deliberate narrowing or a missed generalisation?** If the
other ten mysteries have the same hole, the fix is incomplete and the owner should hear it tonight,
not after a release. ⛔ Verify before believing — the converter's actual preserved set is the fact
that decides this, and this brief has not read it.

**B · Does it reach the person who reported it?** F120 says no. If the reporter is on ordinary Steam
their legacy save could not even load, so their cure is missing for a *different* reason — which
would mean **the report is still open** while a fix ships against it. Settle whether the reporter's
case is covered, partially covered, or untouched, and say so plainly. ⚠️ A fix that repairs a real
defect nobody reported is still worth shipping; the risk is *believing the report is answered.*

**C · Is the repair contract honoured?** It claims: additive synchronous handler; no new GameVar,
object field, stored function, wrapper or thread; only the game's own discovery lock state changes,
through `UnlockTech`; second load and any partial/completed/vanilla-restored family are no-ops;
`PreProcessLockablePresets` makes handler order irrelevant. **Each of those is falsifiable — test
them, do not accept them.** `FIX_POLICY.md` governs (§4a who-benefits, §3a save-safety, §2
enable-path/declaring-class, §2a behaviour probe never a version check, §2b `-- SRC:`/`-- DEFECT:`
headers).

## 3 · Inherited facts — confirm cheaply, do not re-derive from scratch

Established 2026-09-15/16 on 1.1.0.403908; each is falsifiable by one command.

- `Data/Tech.lua` **did not exist in 1.0.7**; the cure was **one** tech there and is **eleven** now.
- All 11 carry `LockState = "hidden"`, `Unknown = true`, `group = "Mysteries"`, a `MapPos`.
- Reveal path: `Mystery 8.lua:112-115` → remap to `WildfireCure_1` → `SetTechDiscovered`
  (`Lua/Research.lua:140`) → `UnlockTech` (`Lua/TechTree.lua:1275`) → `UnhideTech` + clears both lock
  reasons.
- Map visibility is `GetTechState(id, UIPlayer) ~= "hidden"` (`TechTree.lua:434`);
  `GamePresetLockStateAndText` (`CommonLua/Features/LockablePreset.lua:339`) is a pass-through and is
  **not overridden anywhere**.
- ⭐ `Research:ChangeResearchCost(tech_id, points)` **never reads `points`** — its body is
  `BoostTech(tech_id, 20)` (`Lua/Research.lua:225-227`). Owned by [C79](../bugs/C79.md).
- ⭐ 1.1.0 has **no "in progress" research state**; research is instant at 1 tech point; the dead
  `"In Progress"` wait is used **exactly once** tree-wide (Mystery 5). Owned by [C69](../bugs/C69.md).
- **9 of 11 mysteries** gate on `SA_WaitResearch`; **39** `"Researched"` waits tree-wide.
- `SA_GrantTechBoost` special-cases **exactly one** tech in the whole file — `WildfireCure`
  (`SA_Gameplay.lua:824`) — completing the next unresearched `_N` per medical building.

**Already refuted — ⛔ do not re-run:** the chain head's forward link is bypassed by the reveal;
`UnlockTech` does not early-return on a hidden tech; the rewiring is complete (5 chained = 5
remapped); the research-model change did not silently break nine mysteries' gating.

## 4 · Scope

**IN:** F120's cause, completeness, contract and reach; expanding or reshaping the fix; whether the
class spans other mysteries.

**OUT, route rather than fix:** [C79](../bugs/C79.md), [C69](../bugs/C69.md), [C92](../bugs/C92.md),
[C97](../bugs/C97.md) §Finding 5 own their own defects — ⛔ finding something there does not
authorize fixing it; add evidence to that entry and say so.

## 5 · What you may not claim

- ⛔ **Never state the fix works because the source says so.** Say what you ran; otherwise it is
  "desk-exercised, retail unexercised" — which is what it already says.
- ⛔ **"Not reproduced" is not "refuted."** Refuted requires the condition was SAMPLED.
- ⛔ **No absence claim from a truncated grep**; count the presence side.
- ⛔ **Do not certify it safe to ship** unless you exercised save-safety; the narrower true statement
  wins.
- ⭐ If you widen the fix, the widened body **invalidates its own prior tests** — rebase the harm legs
  on the pre-fix body and rerun the whole suite, not only the changed leg.

## 6 · Deliverable

A verdict — **SHIP AS IS / SHIP WITH CHANGES / DO NOT SHIP** — with the changes enumerated, plus:
amendments to `F120.md` for anything it overclaims or missed; a new entry if you find a separate
defect (route via the `smr-bug-library` skill; ⛔ archived numbers in `docs/archive/bugs/` must never
be reused); and a short report of negative results, which are what stop the next session repeating
you. `python tools/doccheck.py` GREEN before any commit; `python tools/parsecheck.py` before trusting
any Lua; commit with an explicit pathspec, never `-a`.

⚠️ **A peer may be in this tree.** Re-check `git log` + `git status` before every write and never
touch another session's unstaged work.

## 7 · Stop conditions — permission to report rather than push on

- You have a verdict and the changes are enumerated. **Done.**
- The fix is correct but incomplete, and widening it is a **design call** → say so and route the call
  to `docs/PLAYTEST_CHECKLIST.md` → "Decisions waiting on you".
- The remaining question needs a live colony your own launched game cannot reach.
- ⛔ You are about to ask the reporter for anything → stop and report instead.

⚠️ **Time matters tonight:** the module is registered and would ship in the next upload, and the
owner has reporters waiting. **If you find a reason it must not ship, say that first and loudly**,
before the rest of the audit.

## 8 · Progress list — required before you execute

Open a live list covering the whole job, one item per commit-and-verify unit, exactly one in progress.
Split a stage when it splits; rewrite when reality changes; keep useful state in the item text.
⛔ Do not carry several commits under one item or update it only at the end. The owner reads this list
to decide whether to step in.

## 9 · Lifecycle

⛔ **One-off. When consumed, `git rm` this file AND delete its row from `prompts/README.md` in the
same commit** (owner ruling 2026-09-13, checklist 174 — the map lists live prompts only, no
tombstones). The outcome lives in the verdict, the entry and the report.
