# 03 · The applies-today repairs — modules that survive and are wrong right now

Chain: `prompts/hotfix2/README.md` (its binding rules are yours). Runs after 02
(which owns `items.lua`). Independent of 04 — either order.

Three modules. All three **pass their self-check and apply today**, and all three
do something wrong on 1.1.0. That is the F112 shape: a correct 1.0.7 transform
landing on top of a vanilla redesign, silently.

## 0 · Start

`git log --oneline -10` · `git pull` · `ListAgents`. Todo list first, one item
per commit-and-verify unit.

**Read path:** `agent/STATE.md` · `VANILLA_FIX_QA.md` **§0 and Reader A's rows
F-1/F-2/F-3** (the QA pinned these shapes and its reasoning is the checklist you
work to) · `PACK_1_1_0_REVERIFICATION.md` §1a · `agent/FIX_POLICY.md` ·
`docs/PLAYTEST_CHECKLIST.md` items 114, 118 · your inbox (01 gave you the probe
form; use it).

## 1 · F-1 `SaintBlessing` — probe-gate **and** a save re-base

**What is wrong.** 1.1.0's `TraitPreset:AddDomeColonistsModifier` now does the
label lookup itself (`Lua/TraitPreset.lua:86-87`: `local label = (trait == "")
and "Colonist" or GetTraitLabel(trait)` / `if not label then return end`). Our
DataPatch has already rewritten `Saint.modify_trait` from `Religious` to
`TraitReligious`, so vanilla computes `GetTraitLabel("TraitReligious")`, gets
`false` (`Lua/Traits.lua:1325-1328`), and returns without registering anything.
⇒ **with the pack on, no Saint blesses anyone.** With it off, 1.1.0 works.

**Half one — the probe.** In the `DataPatch` pass, after DataLoaded, call the
real `AddDomeColonistsModifier` on a stub unit/dome that captures the label:

- captures `Religious` ⇒ 1.0.7 shape ⇒ **apply**;
- captures `TraitReligious` ⇒ already handled ⇒ **decline**;
- captures nothing, returns nil, or throws ⇒ **decline** (fail closed).

⛔ The third case is not pedantry. `AddDomeColonistsModifier` returns silently
when the stub's `GetPropertyMetadata(modify_property)` is nil
(`TraitPreset.lua:80-84`), so "nothing captured" is UNKNOWN — and reading that
silence as "1.0.7" would reproduce the exact bug you are fixing.

**Half two — the save re-base, and it is the half that is easy to miss.**
1.1.0 ships a one-shot `SavegameFixups.OrphanedDomeColonistsTraitModifiers`
(`Lua/_fixup.lua:2143-2170`) that strips every dome-colonists trait modifier and
rebuilds it through the same function. On any save loaded while the broken pack
was on, **that fixup already ran, with our wrong value, and registered nothing.**
Fixups do not re-run. `label_modifiers` is persisted. Nothing re-applies until
the Saint changes dome.

⛔ And our existing heal (`Fix_SaintBlessing.lua:151-181`) will NOT cover it: it
is keyed on `rebased_from`, which is EMPTY when the pass declines. So the patch
must carry its own one-shot re-base for the 1.1.0 shape — re-apply through
`AddDomeColonistsModifier` for every dome-colonists trait carrier missing its
label entry.

**Control (owner, ~5 min):** a Saint in a dome with Religious colonists shows
"Blessed by a Saint", on a save that was loaded under the broken pack.

## 2 · F-2 `StaleReservations` — ⛔ BLOCKED on the owner

**Do not start this module until the owner has ruled FIX or REMOVE.** If it is
REMOVE, it belongs to a deletion sweep, not here — route it and say so.

**What is wrong if it stays.** 1.1.0 added a legitimate long hold: boarding an
expedition rocket saves `expedition_residence` (`Colonist.lua:5027-5031`) and
reserves it through `Residence:ReserveResidence` (`:5003-5005`), so our
post-wrapper stamps it; the colonist stays valid while away. Our `NewDay` age
branch then cancels a real hold ⇒ **crew back from a long expedition lose their
home.** Lock is 3,600,000 ms (`__const.lua:174-176`); one-way expedition time is
1,440,000–3,000,000 (`Data/POI.lua`).

**The shape, if kept:** skip colonists with `expedition_residence` truthy. One
clause.

⚠️ **State the narrowed premise in the module header, honestly.** 1.1.0 bounds
the ordinary shuttle-wait case F58 was written for at one sol
(`_GameConst.lua:144`, `LRTransport.lua:47-49`, `LRManager.lua:55-57`). What the
sweep still covers is **committed-shuttle limbo and the walk path** — not "F58 is
still shipped". The report's row overstates this and the QA (§0.4) corrects it.

**Control (owner, only if kept):** send an expedition, wait past 5 sols, confirm
the returning crew keep their residence with the pack on.

## 3 · F-3 `ShelterReflex` — delete half (a), keep half (b)

**What is wrong.** The signature changed: `IsSuitable(colonist)` became
`GetScoreFor(colonist)` (`MicroGHabitat.lua:173-175`), and `GetScoreFor` reads
`colonist.traits` itself (`Community.lua:442-445`). Our body hands it
`colonist.traits`; inside, `traits.traits` is nil and `FilterObjectAttributes`
indexes `obj_attributes[attrib]` for every filter key (`Filter.lua:113-121`)
⇒ **a throw on any asteroid habitat with a trait filter.** Default filter is `{}`
(`Community.lua:43`), so it is silent until a player sets one.

**The shape:** delete half (a) — the `IsSuitable` replacement
(`Fix_ShelterReflex.lua:43-47`). **Keep half (b)**; its reads all still exist
(`Colonist.lua:94`, `:3015-3020`, `:2212`, `:2572`, `:2666`;
`__const.lua:1756`).

⚖️ **Why deletion and not repair.** No-life-support is now a deliberate −400
tier, not a missing +100 (`Community.lua:436-437`, `:443`, with help text at
`:437`). `FIX_POLICY` §4 bars fighting a stated design. ⚠️ **Name the cost in
the notes**: dropping (a) returns F73(a)'s blip-eviction to 1.1.0 players.

**Control (owner, ~2 min):** an asteroid habitat with a trait filter set — no
throw.

## 4 · Every module you touch here

- Carries its `SRC:` / `DEFECT:` manifest lines per 01's spec, stamped **after**
  your edit, never before.
- Passes `bodycheck.py` and `sigcheck.py`.
- ⛔ **Declines on 1.0.7** if it gains any 1.1.0 body shape (README, ck118).
  F-1's probe does this for free — a probe that captures `TraitReligious` on
  1.1.0 captures `Religious` on 1.0.7 and correctly applies there. Say so in the
  header rather than leaving it implicit.

## 5 · Scope fence

**In:** `Fix_SaintBlessing.lua`, `Fix_StaleReservations.lua` (if kept),
`Fix_ShelterReflex.lua`, their bug entries, their drafted patch-note lines.
**Out:** `items.lua` and `metadata.lua` (02 and 06 own them); the re-copies (04);
`00_Core.lua` (01); every KEEP and REMOVE module.
Found something out of fence? **File it, do not fix it.**

## 6 · Stop conditions

- F-2 unruled ⇒ skip it, do the other two, say so.
- The F-1 probe cannot be made to fail closed on a stub, or
  `AddDomeColonistsModifier` turns out not to be side-effect-free on one ⇒
  **STOP AND ASK.** Do not ship a probe you cannot bound.
- The F-1 re-base would need to touch saves in a way `FIX_POLICY` does not
  already sanction ⇒ stop and report.
- You find a fourth applies-today harm ⇒ file it, tell 99, do not absorb it.

## 7 · What may NOT be claimed

- ⛔ Not "F-1 is fixed" until the owner's control has been seen. A source-derived
  repair is a claim; the owner's rule of 2026-09-08 binds our own notes too.
- ⛔ Not "saves are healed" — the re-base is untested until a save that loaded
  under the broken pack has been loaded again with the repair on.
- ⛔ Not "F-3 is now correct" — it is now *absent*, and 1.1.0 players get the
  vanilla behaviour, which still evicts on a blip.
- ⛔ No status moves on source reads.

## 8 · Close-out

Green gates. Append your outbox to `04`, `06` and `99` — 99 needs, per module,
what you changed, what the probe decides, and **what has not been exercised in
play**. The three controls above go to the checklist as a batched owner ask
(they fit in one sitting on the existing `BlankBig_02` colony). Strike your
README row, `git rm` this file, commit together, push.

## Notes from upstream

*(From the authoring session, `smr-bugfixpack-91`, 2026-09-08.)*

- ⛔ Read `VANILLA_FIX_QA.md` §0 before the main report's §1a. The QA promoted a
  sixth harm, added the F-1 re-base and the F-5 cleanup, and narrowed F-2's
  premise. The main report says in its own rows that the QA supersedes it.
- The owner's standing rule: **cheats are normal on the playtest saves** — a
  confound only where a reading intersects what they change. Do not ask for a
  clean run for these three controls; none of them touches a cheated quantity.
- ⚠️ Untick the Test Kit's force leg before any attended control if it is armed
  (it was not, per the 17:51 boot log).
