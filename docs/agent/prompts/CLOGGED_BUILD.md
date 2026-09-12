# BUILD — unstick a producer left "Clogged after a Dust Storm." (C85)

> ✅ **FIREABLE — the fold-in slot was closed empty on 2026-09-11 (see the foot).** Written by
> `smr-bugfixpack-cb`. **Staleness anchor: HEAD was `15c6ea6`.**
> ⚠️ Start with `git pull` + `git log --oneline -15`; records win over every specific here.
> ⚠️ Keep a live todo list from your first tool call. 🛑 **Stop and report a concern at any point** — the owner
> granted that standing on 2026-09-11; the house wording is in `prompts/migrationfix/README.md`
> ("Both links can stop at any time"). A stop is cheaper than a wrong ship.

Entry: `bugs/C85.md`. Field reports: two Steam players on 1.1.0 — a Rare Metals Extractor and a Polymer
factory, both saying destroy-and-rebuild was the only way out.

> ⛔ **ONE OWNER DECISION IS OPEN AND IT CHANGES WHAT YOU BUILD (checklist 154): sweep only, or sweep + a
> `Duration` DataPatch as well?** §2 has the trade. **If it is unruled when you start, build the SWEEP ALONE**
> — it is the half that rescues the players who already reported this, the Duration cannot, and the Duration
> also adds a visible countdown, which is a UI addition and `FIX_POLICY` §4's call, not yours. Say in one line
> of the commit body that you defaulted.

## 1 · Dossier — DO NOT RE-DERIVE IT; it is in the entry

⭐ **`bugs/C85.md` now carries the whole mechanism** (landed `15c6ea6`, dated section "mechanism resolved"),
all SOURCE on **1.1.0.403908**. Read it rather than this prompt: **the entry is the truth, a prompt is not
authority.** In one breath, so you know what you are building against:

* `BuildingClogged` disables the producer **before** the player answers, with `Reason` = `T(789863173059, …)`
  and **no `Duration`** — while `SetBuildingEnabledState` has a `Duration` branch that auto-re-enables and two
  other shipped events use it. The engine's own safety net, unused here.
* A **lost reply is permanent**: the outcome path is inside `if reply then`, and the fall-through runs
  `Complete()`, which never re-registers a `OneTime` bit. That predicts the reporters' permanence.
* The stuck state is **two saved fields** on the building, so detection is exact and the cure is the game's own
  setter.
* Already **refuted**, do not re-check: the player cannot Escape that popup.

⚠️ The entry's older `H1`/`H2` sections and its first "Fix sketch" are **superseded but preserved** — read the
dated 2026-09-11 section as current.

## 2 · Fix shape — PROPOSED, and the owner has not chosen it

**A read-only sweep (on load + daily) that clears the flag the game forgot to clear.** Detect
`exceptional_circumstances` true **and** `TGetID(exceptional_circumstances_reason) == 789863173059`; repair with
the game's own setter, `building:Setexceptional_circumstances(false)` (`BaseBuilding.lua:470-480`, which runs
`UpdateWorking`/`UpdateConsumption`/`AttachSign` and whose `:474` already guards the reason-clear behind
`exceptional_circumstances_maintenance`). Enumerate with the shipped idiom `AllMapsForEach` (as the devs' own
fixups do, `Residence.lua:634-642`).

**⛔ Two interlocks — do NOT unstick a building that is legitimately waiting.** Both are `GameVar`s, so both are
in the save, and both are read-only to us:
1. `g_StoryBitActive` — `BuildingClogged` is running for that building right now (popup up, unanswered).
2. `g_StoryBitStates` — `BuildingClogged_1_FixAfterStorm` is armed and pending for it ("we'll fix it after the
   storm", working as intended).

**Why this shape over a `Duration` DataPatch** (record the trade, don't re-litigate it silently): the sweep
rescues **already-stuck saves** and the Duration cannot — it is spawned at trigger time, so a player already
stranded has no thread to resume, and both reporters are in exactly that state. The sweep also writes **nothing**
new to the save, touches no shipped preset data, adds no UI, and no-ops if Paradox patches the bit. The Duration
patch's one advantage is that it matches vanilla's own idiom. ⚠️ A Duration also fires
`AddEventOnScreenNotification`, i.e. a visible countdown — a UI addition, which is `FIX_POLICY` §4 and the
**owner's** call, not the builder's.

## 3 · Resolve these at build time — three desk checks, not an investigation

1. `exceptional_circumstances_reason` still reads as a `T` after a save/load round trip (`TGetID` handles both
   forms, so low risk — but confirm rather than assume).
2. The exact shape of a pending `g_StoryBitStates` entry, so interlock 2 keys on the right field.
3. **Key narrowly to this one reason id.** The evidence covers this story bit, not "any story-bit-disabled
   building". ⛔ Do not generalise the sweep.

## 4 · The owner's A/B — the sitting recipe, and the cheap half is the one that matters

**A/B #1 — does the FIX work? Minutes, any 1.1.0 colony, any sol, no storm needed.** The repair keys on an end
state of two fields, so force the end state directly. Select a producer, then:

```lua
SelectedObj:Setexceptional_circumstances(true, StoryBits.BuildingClogged.ActivationEffects[1].Reason)
```

That is the *identical call* the story bit makes (the no-Duration `else` branch), with the preset's own `Reason`
object — same setter, same UpdateWorking/AttachSign path, same panel text.
- **Control (fix off):** dead across a sol **and** a save/reload. ⭐ This leg independently tests C85's core
  claim — that nothing in vanilla ever clears it — which has never been checked in play.
- **Test (fix on):** the sweep clears it and the building resumes.

**A/B #2 — does the BUG strand it in play? Optional, expensive, MUST NOT gate the fix.**
`CheatDustStorm(storm_type, setting)` (`Lua/DustStorm.lua:667`) and
`ForceActivateStoryBit("BuildingClogged", CurrentMap, SelectedObj, "immediate")` (`_StoryBits.lua:915-929`;
`force` does not block on failed prerequisites, so it works past the sol-80 window).
⚠️ **VACUITY TRAP:** it will probably NOT clog the building you selected — `PickFromLabel:__eval`
(`Lua/Conditions.lua:353-366`) does `context.object = obj`, a *random* eligible producer, overwriting your
selection. Read back which building actually went dead. And reaching the *stuck* state needs the reply lost,
which (Escape being blocked) means save/load or quit-to-menu with the popup open — it may not reproduce.

⚠️ This launches the retail game, so the **STALE-PROBE GATE** binds: `grep -rln "TEMPORARY" Code/
../SMR-BugFixPack-TestKit/Code/` must be clean, or every hit declared by the session's design.

## 5 · Ship checklist

`parsecheck` · `bodycheck` (`--pin` for the `SRC:`/`DEFECT:` manifest, `FIX_POLICY` §2b) · `doccheck` GREEN with
counts from `--emit-counts` · **H-10: a new `Code/*.lua` needs an `items.lua` entry or it ships absent** ·
⛔ **H-02: never touch `version`, never open the Mod Editor** · record what you built on `bugs/C85.md` and move
its status word only as far as the evidence goes · commit by pathspec, push.
⚠️ **`items.lua`/`metadata.lua` may still be the owner's uncommitted v8 writeback** — H-10 makes a NEW module
collide with it head-on. `git status --short` first; if either is modified and uncommitted, **do not edit, stage
or work around them** — ask the owner. That gate stopped `migrationfix`'s item B the same night, which is the
precedent for stopping rather than improvising.
⛔ No status word here is a playtest grant; `tested-attended` is the sitting's.

---

## 🧩 FOLD-IN SLOT — CLOSED EMPTY, 2026-09-11

The owner reserved this for a second fix. The candidate was the Reddit "160% productivity" thread, and it was
**checked and is not a defect** — the extractor upgrades boost Production, never Performance, in either game
version, and 1.1.0 actually made that sponsor goal easier twice over (`bugs/F108.md`, dated 2026-09-11;
checklist 153). So nothing folds in and **this prompt ships one item.**

**Status: CLOSED — this prompt is fireable.**
