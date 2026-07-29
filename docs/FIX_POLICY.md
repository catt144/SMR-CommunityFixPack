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

   **4b. Global-function replacement** (its own technique, between 4 and 5 in
   preference; numbered 4b so existing §1.4/§1.5 citations stay valid) —
   assigning `_G[name] = replacement` for an existing global. Works because
   `ModEnvMeta.__newindex` rawsets non-blacklisted existing names into the
   real `_G`, and generated closures (script conditions, sequence code)
   resolve the name at call time (ENGINE_FACTS.md). Rules: plain assignment,
   NOT `rawset(_G, ...)` (that writes only the mod's own env); read the name
   back with `rawget(_G, name)` in apply() to confirm the write landed (F22
   does); prefer a chained wrapper (capture `orig`, delegate) over a body
   copy whenever the defect is hookable.
5. **Full replacement** — only when the defect is mid-function and unhookable
   (F04, F09, F11, F12...). Rules:
   - Copy the shipped body **byte-identical except the minimal fix**, marked with
     `-- FIX:` comments on changed lines only.
   - Header comment must name source file + lines + game version the copy came from
     (the pinned build number, e.g. `1.0.7.396349` — not a date).
   - These are the fixes most likely to clash with other mods and rot on game
     patches — keep the list short and re-verify each game update (the fpk
     extraction diff is a release gate, WORKFLOW.md).
   - **"Reconstruction" sub-category:** a replacement whose body is NOT a
     byte-copy — the original is rebuilt from its observable contract (a
     file-local was inlined, a helper re-derived; F03/F04/F09 are of this
     kind). Allowed only when a byte-copy is impossible (file-local upvalues,
     generated code); the header must SAY it is a reconstruction and name
     what was re-derived, because the extraction-diff re-verify cannot
     compare it byte-for-byte — it needs a behavioral re-check instead.

## 2. Fail safe, never loud

Every fix goes through `SMRFixPack.Register(id, {title, apply})` (Code/00_Core.lua):

- `apply` runs under `pcall`; an error deactivates only that fix.
- Before patching, sanity-check the target still looks like the bug (function
  exists, table layout as expected). If not — the game likely hotfixed it —
  **return a string** (reason) instead of patching. Never assume; never error.
- **Self-check on the DECLARING class** (the F64 lesson): mod code runs before
  classes are flattened, so a classdef exposes only members it declares
  ITSELF — checking an inherited method on a subclass finds nil and silently
  deactivates the fix. Verify where the method is declared in Src and check
  that class.
- Respect `SMRFixPack_Disabled["<id>"]` so users/other mods can veto single fixes.
- **Every `OnMsg` handler must re-check BOTH the registry status AND the veto
  itself** (the A1 lesson, audit 2026-07-29): handlers are installed at file
  scope unconditionally — Register's veto only skips apply() — so a handler
  that mutates state without re-checking `SMRFixPack_Disabled[id]` (and,
  where it heals status, without refusing to overwrite `"disabled"`) defeats
  the veto. Donor pattern: Fix_LastTransmissionStorage's patch() prologue.
- If the target can legitimately be absent before `DataLoaded` (presets,
  templates), track a `data_loaded` flag and only latch `inactive` after it
  has fired — before that, absence just means "not loaded yet" (the F75
  false-inactive lesson); after it, silence means reporting `active` forever
  on a target a future update removed (the B3 lesson).

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

## 5. Optional modules (`Opt_*`)

Not bug fixes: opt-in behavior changes, off by default, one Mod Options
toggle each (`ModItemOptionToggle.name` == the Register id == the
`default_options` key — all three are load-bearing).

- **Install pattern (mandatory — the A2 lesson, audit 2026-07-29):** hooks on
  class methods are installed at FILE SCOPE (classdef time, so they propagate
  through class flattening) and gate per call on `SMRFixPack.IsActive(id)`.
  An apply()-time install runs AFTER flattening on a first mid-session enable
  and is invisible to derived classes until restart. Donor:
  Opt_DroneOverhaul. Wraps that resolve at call time (a global function, a
  UI-template Init) may stay in apply() — say so in the header.
- Guard each file-scope install with the same existence checks apply() uses,
  so a missing target degrades to apply()'s reason string instead of erroring
  at classdef time.
- `apply()` keeps only self-checks and the opt-in check; it returns the same
  reason strings whether or not the hooks installed.
- `on_activate` / `on_deactivate` (both optional) run after a LIVE toggle
  flip only — use them exclusively for STATE that is not a call path (e.g.
  MultipleSuns' template flag); call-path behavior must come from the
  per-call gate, never from these hooks. They must be idempotent; failures
  are logged by the reconciler (B1 fix), not swallowed.
- Header must state the real toggle semantics (both directions, including
  the first mid-session enable) — and be updated when they change.
- Savegame footprint per §3; a module OFF must be byte-for-byte vanilla
  behavior.

## 6. Engine semantics that bind every fix

- **`error()` and `assert()` in mod code REPORT AND CONTINUE** — they do not
  unwind (ENGINE_FACTS.md). Never use them for control flow or guards; use
  early returns and reason strings. `pcall` still catches genuine runtime
  errors.
- **Localization stance:** a T value is a TABLE (`Untranslated(s)` →
  `T{s, untranslated = true}`). Copied shipped bodies keep their `T(id, ...)`
  calls byte-identical; NEW player-visible strings from this pack use
  `Untranslated("...")` — the pack ships no loc tables, and a raw Lua string
  where the UI expects a T value renders wrong or crashes (the F14 probe
  lesson). Log/console text stays plain strings.
- **Logging:** every ModLog call escapes `%` (`msg:gsub("%%", "%%%%")`) —
  ModLog's print path formats the message a second time (00_Core.lua:24-30).

## 7. Console platforms (Xbox / PlayStation / MS Store)

- No developer console, no file access, no companion-mod path: the per-fix
  `SMRFixPack_Disabled` veto and every log/console surface (`ListFixes()`,
  reason strings, "report this log") are **invisible on console**. Fail-safe
  behavior must therefore never DEPEND on the player seeing a message —
  self-deactivation must be safe silently.
- Mod Options is the one universal surface (gamepad-native) — anything a
  console player must be able to steer goes there or nowhere.
- Any enabled mod blocks ALL achievements on those platforms (not on
  Steam/PC) — a storefront disclosure, not a code concern, but never write
  player-facing text that contradicts it.

## 8. Release hygiene

- One fix per `Code/Fix_*.lua` file; file name matches the Register id; every
  file listed explicitly in `metadata.lua` `code`.
- `00_Core.lua` must load first (list order in metadata controls load order).
- Before release: verify each target against the shipping `Packs\Lua.fpk`
  (see WORKFLOW.md), test each fix in-game, update BUGS.md statuses, credit
  prior art (ChoGGi's Fix Bugs mod documented several of these bug families
  for the original game).
