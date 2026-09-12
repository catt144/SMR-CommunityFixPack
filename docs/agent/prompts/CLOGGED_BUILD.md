# SKELETON BUILD — unstick a producer left "Clogged after a Dust Storm." (C85)

> 🚧 **SKELETON, NOT YET FIREABLE.** Written **2026-09-11** by `smr-bugfixpack-cb`.
> **Staleness anchor: HEAD was `bb50f5d`.** The owner may **fold a second fix into this prompt** before it runs —
> see the FOLD-IN SLOT at the foot. Do not fire it until the owner says the slot is closed.
> ⚠️ Start with `git pull` + `git log --oneline -15`; records win over every specific here.
> ⚠️ Keep a live todo list from your first tool call. 🛑 Stop and ask at any point — see the house rule in
> `prompts/migrationfix/01_BUILD_opus.md`, which applies here too.

Entry: `bugs/C85.md`. Field reports: two Steam players on 1.1.0 (a Rare Metals Extractor and a Polymer factory),
both saying destroy-and-rebuild was the only way out. ⚠️ **C85 does not yet carry the findings below** — they were
established after it was written, and landing them in the entry is part of this build's job.

## 1 · Dossier — all SOURCE on 1.1.0.403908, re-checkable

**What "Clogged" is.** Not maintenance: the story bit `Data/StoryBit/BuildingClogged.lua`, fired at dust-storm
start, `OneTime`. Its ActivationEffects disable the building **before the player answers** (`:4-8`) with
`Reason` = `T(789863173059, "Clogged after a Dust Storm.")` — **and no `Duration`**.

**Why no Duration matters.** `SetBuildingEnabledState` (`Lua/ClassDefs/ClassDef-Effects.generated.lua:2770-2785`)
has two branches: with a `Duration` it spawns a game-time thread that sleeps and **re-enables automatically**;
without one it takes the permanent `else`. Two other shipped events DO pass a duration —
`DLC/norman/Presets/Event/BugAppetit.lua:26` (3 sols) and `KitchenRescue_Reopening.lua:44` (5 sols).
⇒ **the engine already has the safety net and this story bit simply does not use it** — the strongest available
argument that this is an oversight, and the one to give Paradox.

**Those vanilla durations survive a save/load** (checked, because it decides the fix shape):
`CreateGameTimeThread` threads are persistable **by default** — `OnMsg.PersistSave` serialises every thread with
`threadPersist`, with its sleep state (`CommonLua/Core/cthreads.lua:481-517`), `PersistLoad` restores them
(`:519-524`), and `permanents` registers `Sleep`/`WaitWakeup`/`WaitMsg` as resumable stack functions (`:470-478`).
Real-time threads must opt in via `MakeThreadPersistable`; the engine's own branching shows the asymmetry
(`Libs/Notifications/Notifications.lua:245-251`, `Classes/ActionFX.lua:1186-1191`).

**Why a lost reply is permanent, not delayed.** In `Lua/_StoryBits.lua` the whole outcome path sits inside
`if reply then`; with no reply it falls through to `ProcessOutcomeEffects(storybit)` + `Complete()`, and because
the bit is `OneTime`, `Complete()` does not re-register it. ⇒ the story bit is **finished and gone** while the
building stays disabled and no follow-up was ever armed. This predicts the reporters' *permanence*, which C85's
H1 (a delayed follow-up) does not.

**Refuted, so nobody re-derives it:** the player cannot Escape the popup. `disallow_escape = #choices > 1`
(`Lua/MarsStoryBits.lua:79`) and all four replies are always present (none carries `HideIfDisabled`,
`BuildingClogged.lua:51/88/98/113`), so `#choices` is 4.

**The stuck state is two saved fields** (`Lua/Buildings/BaseBuilding.lua:30-31`):
`exceptional_circumstances = true` and `exceptional_circumstances_reason` = that `T`. Read the id with `TGetID`
(`CommonLua/Core/localization.lua:48`), which handles both the packed-userdata and table forms.

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
⛔ **H-02: never touch `version`, never open the Mod Editor** · land the §1 findings in `bugs/C85.md` and route
the §2 fix-shape choice to `PLAYTEST_CHECKLIST.md` → "Decisions waiting on you" · commit by pathspec, push.
⛔ No status word here is a playtest grant; `tested-attended` is the sitting's.

---

## 🧩 FOLD-IN SLOT — reserved by the owner, 2026-09-11

A second fix may be folded into this build. **Nothing is assigned yet.** When it is, add it here as its own
lettered item with the same shape as §1–§4 (dossier → fix shape → open checks → A/B), and say explicitly whether
the two items are **independent** — if they are, each must be able to ship without the other, exactly as
`migrationfix/01_BUILD_opus.md` keeps its A and B separable. ⛔ Do not let a second item's uncertainty hold up a
first item that is ready.

**Status: OPEN — do not fire this prompt while this slot is open.**
