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

- **2026-08-20, link 1 (`C51`, built and consumed).** Counts after link 1, emitted:
  **76 registered modules · 77 `Code/*.lua` · 97 probes**. You make it **77 / 78**;
  the probe count moves only if you add one.
- ⛔ **`python tools/split_bugs.py --write` ABORTS** ("no entry headings found — is
  this the pre-split file?") — it is the one-time migration tool, not the
  regenerator, despite what `INDEX.md`'s line-1 banner says. A status flip DOES
  change the index row (the status column is derived, not the frozen `row_status`
  cell), so `doccheck` goes RED until you rewrite it. What works, and produces
  exactly the bytes `doccheck` compares against:
  ```python
  import sys, io; sys.path.insert(0, 'tools')
  import split_bugs as sb
  lines = sb.render_index(sb.load_from_dir())
  io.open('docs/agent/bugs/INDEX.md','w',encoding='utf-8',newline='\n').write('\n'.join(lines)+'\n')
  ```
  Then `git diff --stat` it: **one row should change.** Expect a new
  `warn C50: the frozen index-row cell says 'filed', entry says 'fixed'` — that
  warn is the house pattern for every flipped entry (`C43`, `F100`), not a problem.
- **Insertion point in both lists:** immediately before `Code/90_SaveSanitizer.lua`,
  which must stay LAST. `upload_preflight` proves the two lists agree; it read
  **0 FAIL, 77 entries in order** after link 1.
- ⭐ **Your `EF-039` ground is firmer than the entry says, and it is worth reading
  before you pick route C.** Link 1 re-derived the packs and went one step past the
  citations: `TranslationTable` is populated for **every row in a pack, in every
  language**, because `csv_load_fields` maps CSV col 2 → `text` / col 3 →
  `translated_new` (`CommonLua/Core/localization.lua:920`) and `ProcessLoadedTables`
  (`:938-960`) resolves **English** as `{ translated_new, TEXT, translated }`. So an
  empty `Translation` column in `English.fpk` (22,266 of 23,090 rows have one) is
  **not** a missing record — it falls back to the English source. ⇒ any id present in
  the pack resolves in all nine languages, and `shipped_T .. Untranslated("…")`
  concatenation therefore appends to real translated text everywhere, not just where
  a translator filled a cell. Full derivation: `agent/bugs/C51.md`, the
  *RE-DERIVED 2026-08-20* section.
- **The extractor is seconds, use it:** `sys.path.insert(0,'tools'); import
  flpk_extract as fx; fx.extract(r'A:\SteamLibrary\steamapps\common\Project Spark\Local\German.fpk', out)`.
  ⚠️ `Game.csv` is **43,110 physical lines but 23,090 CSV records** — quoted fields
  carry newlines. Do not quote the line count as a record count; the entry used to.
- ⚠️ **`Src` is under the install dir literally named `Project Spark`** (`EF-014`);
  the `Surviving Mars` folder's `ModTools` has no `Src` and is a decoy. Confirmed
  again this session.
- **The TestKit is a SEPARATE REPO** (`C:\Dev\SMR-BugFixPack-TestKit`), so a probe is
  its own commit and its own push — `doccheck` only report-warns on its dirty tree.
  Link 1 took wave **12** (`Code/62_Probes_Wave12.lua`, registered in that repo's
  `metadata.lua` `code` list); you are wave **13** if you add one.
- **House shape for a class-method wrap, now proven out in `Fix_LocalizedUIText`:**
  mod code loads while `_G.<Class>` is still the **classdef** (`classes.lua:71`,
  swapped for the built class at `:1085`), so an `apply()`-time wrap is a
  classdef-time install and propagates through flattening — which is what makes it
  reach subclasses. ⛔ Do not assume a target has one implementor:
  `customUniversalRocket` turned out to have **five subclasses** that declare no
  `Init` of their own, and the brief's "one caller each" note did not mention them.
