# Link 2 — build `C50`: the sponsor bonus SpaceY grants and never mentions

♻️ **SELF-CONSUMING.** `git rm` this file in your closing commit, naming its grave.
📋 Read `README.md` in this folder first — its binding rules govern you.

## 0 · Read path

```
git log --oneline -15 && git pull
python tools/doccheck.py --emit-counts
```

`docs/agent/STATE.md` · `agent/bugs/C50.md` — ⭐ **especially its
"REPAIR-ROUTE ANALYSIS" section and the correction under it** · `agent/facts/EF-039.md` ·
`FIX_POLICY` §1, §2, §4 · link 1's module, which is your shape template.

## 1 · 🗒 Live todo list — one item per numbered step below

## 2 · What you are building, and why it is a repair

SpaceY's preset grants two modifiers and describes one:

```lua
Effect_ModifyLabel{ Label = "Consts", Prop = "CommandCenterMaxDrones", Amount = 20 }
Effect_ModifyLabel{ Label = "DroneHub", Prop = "starting_drones",      Amount = 4  }
-- effect: "…<bullet> Drone Hubs start with additional Drones\n<bullet> 50% cheaper advanced resources"
```

**16 sponsors, 6 carry modifiers, 5 of the 6 describe every one of theirs** —
three with the exact number. SpaceY is the only miss. ⚖️ **Owner ruling
2026-08-20: this is a plain repair, not a judgment call** — nothing had to be
decided about intent, and no behaviour is being added. ⛔ The store card's *"Five
of the fixes are judgment calls"* line **does not move**.

## 3 · ⛔ The two routes that are already dead — do not rediscover them

1. ⛔ **Replacing `preset.effect` with new text.** `EF-039`: the engine discards
   your literal and renders `TranslationTable[id]`. A new id is in no pack ⇒
   English for eight languages. *(This is what the other mod does. `FIX_POLICY`
   §8 credit still applies — the omission was theirs to spot first — but the
   route is not ours to copy.)*
2. ⛔ **Concatenating onto `preset.effect`.** Both render sites wrap the field as
   `T{sponsor.effect, context}` (`Lua/MissionProfileDlg.lua:42`,
   `Lua/PreGameMission.lua:623`) and the `T` constructor short-circuits on a
   concatenation — `if getmetatable(T[1]) == TConcatMeta then return T[1] end`
   (`CommonLua/Core/localization.lua:224-227`) — **returning it without the
   context**. SpaceY's *first* bullet resolves `(<cargo>)` out of that context.
   ⛔ Breaking bullet 1 to complete bullet 3 is not a repair.

## 4 · Route C — the one that survives

**Leave `preset.effect` untouched** so the game keeps binding its own context, and
append at the UI:

- `GetSponsorSummary(sponsor)` — global, `Lua/PreGameMission.lua:574`, returns
  `{title=…, text=TList(texts, "\n")}`. One caller.
- `GetMissonProfileText()` — global, `Lua/MissionProfileDlg.lua:25` (**the typo is
  vanilla's — do not "fix" it**), returns `table.concat(texts, Untranslated("\n"))`.
  One caller.

⭐ **Both already return a concatenation in vanilla**, so appending one element is
structurally what that path does on every draw. That is the safety argument, and
it is why this route is sound where route 2 is not.

⭐ **The bullet is fully translated, and the number is the game's own.**

- Text: reuse **`4706`** — *"Maximum number of Drones a Drone Hub can control"*,
  the `ConstDef` help for `CommandCenterMaxDrones` itself (German verified:
  *Maximale Anzahl an Drohnen, die ein Drohnen-Hub kontrollieren kann*).
  ⚠️ `887279699046` (the `DroneHubEfficiency` policy description) is the
  alternative and is **less** defensible — it would follow that policy's wording
  if a patch reworded it. **Prefer `4706`; if you choose otherwise, say why.**
- Number: `GetModifiedConsts` writes `t[mod.Prop] = base + Amount` from the
  sponsor's own modifiers (`PreGameMission.lua:519-536`), so
  **`CommandCenterMaxDrones` is already in the context with the modified value**.
  Build your piece as `T{…, context}` with the tag, and the bullet stays correct
  if a patch ever changes the base const.
- ⛔ **Gate on `sponsor.id == "SpaceY"`.** This is a repair to one preset, not a
  new house style for every sponsor.
- ⚠️ **Disclose the borrow in the header:** the sentence belongs to another
  object. That is a real, small cost and it is the honest reason we get a
  translated bullet at all.

## 5 · The rest of the build

Same as link 1, in one line each: house header with citations · chain, never
replace · shape self-check, stand down loudly-in-log/silently-on-screen · **writes
nothing to a save** · ⛔ `items.lua` **+** `metadata.lua` `code` list by hand ·
`upload_preflight` 0 FAIL · probe only if it can fail honestly (this one *can*:
call `GetSponsorSummary` on the SpaceY preset and assert the returned text
contains our piece) · parse sweep · `doccheck` GREEN, counts re-emitted (**77**).

## 6 · Scope fence

**IN:** the SpaceY bullet, both render sites · the module · lists · probe · the
entry updated.

**OUT:** ⛔ the other five modifier-carrying sponsors (**they are already
correct** — do not "harmonise" them) · ⛔ any change to `Effect_ModifyLabel`
values, ever — this is text only, the +20 is not ours to touch · ⛔ `C52` (frozen)
· ⛔ the tag, the version, the portals, the site repo.

## 7 · ⛔ What you may not claim

- ⛔ **"Verified"** — nothing here is observed on screen until link 4.
- ⛔ **"It renders translated"** — you have read a CSV, not a screen.
- ⛔ That the append is invisible to other consumers of those two globals without
  having **counted the callers yourself** (there is one each; prove it again).
- ⛔ Any count you did not emit.

## 8 · Close-out

One commit: module · lists · probe · `agent/bugs/C50.md` updated · `doccheck`
GREEN · `git rm` this file · push.

**Owner report:** what you built · what is unobserved · `upload_preflight` line ·
**the kickoff line for `03_SURFACES.md`**.

## Notes from upstream

- *(link 1 appends here)*
