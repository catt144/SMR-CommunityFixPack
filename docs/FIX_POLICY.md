# Fix Policy — how we patch

Rules for every fix in this pack, in priority order. The goal: maximum
compatibility with other mods and future game patches, zero edits to game files.

## 1. Choose the least invasive technique that works

Ranked from most to least preferred:

1. **Data/preset patch** — mutate the preset field in place (e.g.
   `TraitPresets.DustSickness.daily_update_func = ...`,
   `TechDef.X[i].Amount = -20`). Do it in `OnMsg.ClassesPostprocess` (presets built)
   or at code load if the object already exists. Most compatible: other mods see the
   corrected data.
2. **Additive handler** — a new `OnMsg.<X>` alongside the broken one (OnMsg is
   additive; a dead original handler can stay). Used when the original can't fire at
   all (F23).
3. **Registry/table surgery** — adjust the stored entry another system reads
   (e.g. wrap slot FUNC of `PeriodicRepeatInfo["UndergroundMarsquake"]`). Leaves the
   scheduling machinery and any other wrappers intact.
4. **Wrap (chain) the original function** —
   ```lua
   local orig = Colonist.BoardVehicle
   function Colonist:BoardVehicle(...)
       local r1, r2 = orig(self, ...)
       if self.transport_ticket then self.transport_ticket.start_wait = GameTime() end
       return r1, r2
   end
   ```
   Always capture at apply time, always call `orig`, always pass through returns.
   If another mod wrapped first, we chain onto theirs — and vice versa.
5. **Full replacement** — only when the defect is mid-function and unhookable
   (F04, F09, F11, F12...). Rules:
   - Copy the shipped body **byte-identical except the minimal fix**, marked with
     `-- FIX:` comments on changed lines only.
   - Header comment must name source file + lines + game version the copy came from.
   - These are the fixes most likely to clash with other mods and rot on game
     patches — keep the list short and re-verify each game update.

## 2. Fail safe, never loud

Every fix goes through `SMRFixPack.Register(id, {title, apply})` (Code/00_Core.lua):

- `apply` runs under `pcall`; an error deactivates only that fix.
- Before patching, sanity-check the target still looks like the bug (function
  exists, table layout as expected). If not — the game likely hotfixed it —
  **return a string** (reason) instead of patching. Never assume; never error.
- Respect `SMRFixPack_Disabled["<id>"]` so users/other mods can veto single fixes.

## 3. Savegame discipline

- No new persisted classes or GameVars unless unavoidable; if needed, name them
  `SMRFixPack_*` and tolerate their absence (loading a save made with the mod,
  after the mod is removed, must not break).
- Fixes must be sane on existing saves. If a bug left corrupt state behind
  (e.g. F03's leaked modifiers), the cleanup is a **separate, clearly marked
  one-shot `OnMsg.LoadGame` sweep**, conservative by default.
- Never break saves for players who later disable the mod.

## 4. Only fix proven defects

Every fix links to a BUGS.md entry with file:line evidence. No balance changes,
no "improvements", no opinions — those belong in other mods. When intent is
ambiguous, prefer the reading proven by sibling code in the same file
(the F07/F08/F02 pattern: the same author wrote it correctly elsewhere).

## 5. Release hygiene

- One fix per `Code/Fix_*.lua` file; file name matches the Register id; every
  file listed explicitly in `metadata.lua` `code`.
- `00_Core.lua` must load first (list order in metadata controls load order).
- Before release: verify each target against the shipping `Packs\Lua.fpk`
  (see WORKFLOW.md), test each fix in-game, update BUGS.md statuses, credit
  prior art (ChoGGi's Fix Bugs mod documented several of these bug families
  for the original game).
