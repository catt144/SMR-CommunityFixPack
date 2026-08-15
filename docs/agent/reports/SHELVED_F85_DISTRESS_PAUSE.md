# SHELVED — `Fix_DistressPopupPause` (F85), removed 2026-08-15, ready to re-apply

⚖️ **Owner ruling, 2026-08-15, checklist item 31:** *"I think we remove it but
document it, so we can easily re apply it as a fix, if something ever player
facing comes out we already know how to fix it."*

**This file is that documentation.** It carries the module and its probe
**verbatim**, the trigger that would make them worth shipping again, and the
exact steps to re-arm. Nothing here needs re-deriving — the route, the design,
the arithmetic and the runtime readings were all completed and verified before
the module was pulled. ⛔ **Do not treat "it is in git history" as the record:**
that was the hand-wave this file exists to prevent.

---

## 1. Why it was pulled — one paragraph

The module pauses the game under any popup that declares itself non-pausing.
Exactly one popup in the shipped game does that — the distress-call
confirmation (`Lua\RivalColonies.lua:546`, sole setter of `dont_pause` in the
whole tree). **That dialog cannot be opened by a player.** Its only caller is
the `DISTRESS CALL` action, which the shipped executable compiles behind a
literal `local cond = false` (`Lua\XDef\POIAdditionalContent.generated.lua:89-111`,
from `__condition` returning `false` at `Data\XDef\POIAdditionalContent.lua:97`).
The whole feature is dead-coded. So the module's only working branch could
never execute, while its wrapper sat on `PopupNotification:Init` — the
constructor path of **every popup in the game** — forever. Non-zero cost, zero
benefit, plus one live misfire scenario: it would silently override *another
mod's* deliberate non-pausing popup. Full derivation: `agent/bugs/F85.md`
§2026-08-15 (later).

## 2. ⭐ THE RE-ARM TRIGGER — the one thing to watch for

**Re-apply this module if a popup a player can actually reach runs with the
game clock going.** Concretely, any of:

1. **A patch re-enables the distress call.** The tell is a `DISTRESS CALL`
   button appearing on the rival-colony action bar in a real game. Confirm in
   source with the grep in §3 — if `cond` is no longer a literal `false`, the
   defect is live and this module repairs it as written, unchanged.
2. **A patch or DLC adds any new popup that sets `dont_pause = true`.** The
   module is written against the *flag*, not against the distress dialog, so it
   covers a new one with no edits at all.
3. **A player reports a message window that does not stop time** — the
   symptom-side version of 1 and 2, and the one most likely to arrive first via
   the mod page comments.

⛔ **Do NOT re-apply merely because the feature's code is still present.** It
has been present and dead the whole time; presence is what fooled us.

## 3. The 30-second check that answers it

```bash
SRC="<steam>/Project Spark/ModTools/Src"
# (a) is the distress button built?  A literal `false` means NO.
grep -n -B2 -A20 'ActionId = "distress"' "$SRC/Lua/XDef/POIAdditionalContent.generated.lua"
# (b) who sets the flag now?  On 1.0.7.396349: exactly one hit, RivalColonies.lua:546.
grep -rn "dont_pause" "$SRC"
```
If (a) shows the action still wrapped in `local cond = false` **and** (b) still
returns only `RivalColonies.lua:546` plus `PopupNotification.lua:5/:11/:153`,
nothing has changed and the module stays shelved.

## 4. Re-apply checklist

1. Recreate `Code/Fix_DistressPopupPause.lua` from §6 **verbatim** — but first
   re-read its `ROUTE` block against the new build: `PopupNotification:Init`
   must still be a COMBINED method, and `XPauseLayer` must still exist. The
   module's own `SMRFixPack.Require` gate already tests all three and stands
   down on its own if a patch moved them, so a wrong guess fails safe.
2. Recreate the probe from §7 into `TestKit Code/59_Probes_Wave10.lua` (or a
   current wave file). It needs no fixtures and no save — it drives the
   module's exposed `clear_pause_flag` directly.
3. `python tools/doccheck.py --emit-counts` and update STATE's build-state block
   (module and probe counts each go back up by one).
4. Re-run the suite for a new gate baseline; the expected delta is **+1 PASS**
   and nothing else.
5. Flip `agent/bugs/F85.md` off `wontfix` and restore the store-card judgment
   bullet + site fix-list entry (both deleted 2026-08-15; their exact text is in
   `STORE_FIXPACK.md`'s trace table and this file's §5). ⚠️ **The judgment-call
   count on the card, in `metadata.lua`'s description and on the site FAQ goes
   back from FIVE to SIX** — it moved with the removal.
6. ⛔ **Rewrite the player-facing text before shipping it.** The struck version
   said *"What you saw:"* and described the clock running behind a window
   nobody could raise. If the feature is genuinely live at that point the
   sentence is finally true — but check it, do not restore it on faith.

## 5. What is already proven, so you never redo it

| claim | status when shelved | evidence |
|---|---|---|
| `dont_pause = true` has exactly ONE setter in the whole tree | re-derived twice at Src, 08-12 and 08-15 | `RivalColonies.lua:546`; others are the class default `:5`, the `if not self.dont_pause` test `:11`, the constructor hand-off `:153` |
| the wrapper must install BEFORE class flattening | derived | `Init` is a combined method; composite generated at `ClassesPreprocess` from `classdefs[class].Init` (`classes.lua:1636-1652`, `PropertyObject.lua:1663`) — an after-flattening install is invisible to descendants |
| the flip works at runtime | **MEASURED**, two real launches 2026-08-15 | distress flag `true → false`; already-pausing popup `false → false`; no-flag popup **stays `nil`**; idempotent; install witness `active` ×3. Logs `archive/u3suite_Mars.exe-20260815-01.32.33.log`, `archive/u3c39_Mars.exe-20260815-01.36.41.log`, 0 `[LUA ERROR]` |
| save-safety tier | Layer 3, nothing persisted | synchronous, no blocking call, stores no function value, lives in a class table; savegames do not serialise it |
| ⛔ the popup *visibly* pauses on screen | **NEVER CLAIMED** | a flag read through the wrapper is a measurement; a paused screen is a screen event. No one watched one, by construction |

## 6. `Code/Fix_DistressPopupPause.lua` — verbatim as removed

```lua
-- F85: the distress-call confirmation is the game's ONE popup that leaves game
-- time running, so it is the only popup window a save can land inside.
--
-- ⚖️ DISCLOSURE — THIS IS A DESIGN-JUDGMENT TWEAK, NOT A PLAIN REPAIR. The
-- game's code is not wrong here: `PopupNotification` ships a `dont_pause` flag
-- (Lua\UI\PopupNotification.lua:5) and the distress dialog deliberately sets it
-- (Lua\RivalColonies.lua:546). The devs chose non-pausing for that one dialog;
-- this module overrides that choice on F85 grounds, on the project owner's
-- ruling of 2026-08-12 (their own proposed fix: "change the dont_pause = true
-- flag to dont_pause = false"). Full record: docs/agent/bugs/F85.md.
--
-- WHY IT MATTERS. Every other popup adds an `XPauseLayer` in
-- `PopupNotification:Init` (:8-14), so game time stops and no timer-driven save
-- can fire while one is open. The distress dialog does not, which makes it the
-- only place where:
--   * a sol-change autosave can land under an open popup, and
--   * a no-click popup (an `immediate` storybit, or a storybit notification
--     whose timeout expired, `_StoryBits.lua:564/:574-579`) can silently queue
--     behind an open dialog in `g_PopupQueue` — a queue the engine does NOT
--     persist (`PopupNotification.lua:347-355` saves only sync popups), so its
--     game-time waiter is left blocked forever after a reload.
-- Pausing it closes F85's entire remaining reachable surface: with this module
-- active, no save can exist inside ANY popup window on retail.
--
-- ROUTE, re-derived at Src 1.0.7.396349 (2026-08-15, chain unattended-3):
--   * `dont_pause = true` has exactly ONE setter in the whole tree —
--     `RivalColonies.lua:546`. The only other occurrences are the class default
--     `false` (:5), the `if not self.dont_pause` test in Init (:11), and the
--     constructor hand-off `PopupNotification:new({... dont_pause =
--     context.dont_pause}, parent, context)` (:153). Nothing else READS the
--     flag, which is why flipping it is inert everywhere else.
--   * `Init` is a COMBINED method (`DefineCombinedMethod("Init", "procall",
--     "InitDone")`, CommonLua\PropertyObject.lua:1663). The composite is
--     generated at `ClassesPreprocess` from `classdefs[class].Init`
--     (CommonLua\Core\classes.lua:1636-1652), so a wrapper installed while our
--     mod file loads — always BEFORE flattening, on the cold-boot path and on
--     the main-menu enable path alike (FIX_POLICY §2, the F87 rule) — is baked
--     into the composite for `PopupNotification` and every descendant. The same
--     wrapper installed AFTER flattening would replace only the already-built
--     composite and be invisible to descendants; that is why this lives in
--     apply(), which Register calls at file scope.
--   * `InitDone.new(class, obj, ...)` calls `obj:Init(...)`
--     (PropertyObject.lua:1666-1671), so Init receives `(parent, context)`.
--     This module needs neither, but passes both through unchanged.
--
-- FIX_POLICY §1.4 chained wrapper, in its §3a **Layer 3** form: it patches what
-- the shipped body READS and keeps vanilla's body. We do not construct the
-- pause layer ourselves — we clear the flag and let `Init` build its own
-- `XPauseLayer`, in vanilla's own order relative to the camera-lock and
-- input-suppress layers. Degrades gracefully: if a future patch stops setting
-- `dont_pause`, or drops the flag entirely, this wrapper becomes a no-op that
-- costs one falsy field read per popup.
--
-- ⚠️ SCOPE, stated because two house sources word it differently. The test is
-- `self.dont_pause` — i.e. "this popup would open with game time running" —
-- NOT a fingerprint of the distress dialog's title or image. On the pinned
-- build 1.0.7.396349 the two are the SAME SET: `RivalColonies.lua:546` is the
-- flag's sole user, so chain prompt 01's "flip it only for the distress-call
-- popup, everything else untouched" and F85's ruling section ("so ALL popups
-- pause … closes the defect-CLASS") describe identical behaviour here. The
-- flag test was chosen over a fingerprint because a title/image fingerprint
-- rots silently on any text or art change, and because the flag IS the defect's
-- mechanism. Consequence, disclosed: a popup created by a future patch — or by
-- another mod — that sets `dont_pause` would also be paused by this module.
--
-- §3a SAVE-SAFETY TIER: **Layer 3, nothing persisted.** The wrapper is
-- synchronous and has no blocking call, so no frame of ours can sit below a
-- `Sleep`/`WaitMsg` on a game-time thread (route (a) closed by construction);
-- it stores no function value anywhere (route (c)); and it lives in a class
-- table, which savegames do not serialise. The popup dialog itself is an
-- XWindow — UI windows are not persisted — and `OnMsg.PersistSave` stores only
-- sync-popup CONTEXT tables, never dialogs. This module writes nothing new into
-- a savegame and needs no uninstall step.

-- The whole decision, lifted out so the TestKit can read it without opening a
-- modal dialog (the F97 donor pattern — `SMRFixPack.defs.<id>.<helper>`).
-- Returns the object so a probe can chain; the flag it clears is the only
-- state it touches.
local function clear_pause_flag(self)
	if self.dont_pause then
		self.dont_pause = false
	end
	return self
end

SMRFixPack.Register("DistressPopupPause", {
	title = "The distress-call confirmation pauses the game like every other popup, so no save can land inside an open popup window",
	clear_pause_flag = clear_pause_flag,
	apply = function()
		local err = SMRFixPack.Require("DistressPopupPause", {
			-- the DECLARING class (FIX_POLICY §2): PopupNotification.lua:8
			{ class = "PopupNotification", method = "Init" },
			-- the layer vanilla's own body constructs when the flag is clear
			{ class = "XPauseLayer" },
			-- the flag mechanism itself still exists and still defaults off
			{ test = function()
					local C = rawget(_G, "PopupNotification")
					return type(C) == "table" and rawget(C, "dont_pause") == false
				end,
			  reason = "PopupNotification.dont_pause is no longer a class default of false (game update changed the pause mechanism?)" },
		})
		if err then return err end

		local orig = PopupNotification.Init
		function PopupNotification:Init(parent, context)
			-- FIX (F85): decide before touching anything (FIX_POLICY §2) — a
			-- popup that already pauses is handed straight to the original.
			clear_pause_flag(self)
			return orig(self, parent, context)
		end

		if PopupNotification.Init == orig then
			return "could not install the PopupNotification.Init wrapper"
		end
	end,
})
```

## 7. The probe — verbatim as removed from `59_Probes_Wave10.lua`

```lua
---- F85 — the distress-call popup no longer runs the game clock --------------
-- The defect: `dont_pause = true` on exactly one popup in the whole game
-- (Lua\RivalColonies.lua:546) means `PopupNotification:Init` skips its
-- XPauseLayer (Lua\UI\PopupNotification.lua:8-14), so the distress dialog is
-- the only window where game time runs — the only place a timer-driven save can
-- land inside an open popup, and the only place a no-click popup can silently
-- queue behind an open dialog into a `g_PopupQueue` the engine never persists.
--
-- The repair clears the flag before the shipped Init reads it, so vanilla's own
-- body builds the pause layer. The three cases below are the whole contract:
-- the flag is cleared when set, and NOTHING else about the object moves —
-- including the `nil` case, which must stay nil rather than becoming `false`
-- (writing to every popup would be a behaviour change for every popup).
SMRTest.Register("DistressPopupPause", {
	title = "F85 the one non-pausing popup gets a pause layer, and no other popup is touched",
	kind = "behavior",
	fix = "DistressPopupPause",
	run = function()
		local missing_status, missing_msg = FixMissing("DistressPopupPause")
		if missing_status then return missing_status, missing_msg end

		local defs = SMRFixPack.defs
		local def = type(defs) == "table" and defs.DistressPopupPause
		local clear = type(def) == "table" and def.clear_pause_flag
		if type(clear) ~= "function" then
			return "SKIP", "the fix does not expose clear_pause_flag (build changed?)"
		end

		-- 1. THE SUBJECT — the distress dialog's own state. `OpenPopupNotification`
		--    hands the flag to the constructor (PopupNotification.lua:153), so by
		--    the time Init runs, `self.dont_pause` is the context's `true`.
		local subject = { dont_pause = true, marker = "subject" }
		clear(subject)
		if subject.dont_pause ~= false then
			return "FAIL", string.format("a dont_pause popup came out of the repair as %s — the pause layer would still be skipped",
				tostring(subject.dont_pause))
		end
		if subject.marker ~= "subject" then
			return "FAIL", "the repair touched a field other than dont_pause"
		end

		-- 2. THE NEGATIVE CONTROL — every other popup in the game. The class
		--    default is `false` (PopupNotification.lua:5), and it must come back
		--    false, having taken the same code path.
		local control = { dont_pause = false, marker = "control" }
		clear(control)
		if control.dont_pause ~= false then
			return "FAIL", "an ordinary (already pausing) popup was modified"
		end

		-- 3. THE ABSENT-FLAG CONTROL. A popup object built before the class
		--    default exists — or by another mod that never sets the field — must
		--    come back with the field still absent. `false` would read the same
		--    to Init but is a write we have no business making, and it is how a
		--    wrapper starts being "a behaviour change for everyone else"
		--    (FIX_POLICY §2, the foreign-object rule).
		local absent = { marker = "absent" }
		clear(absent)
		if absent.dont_pause ~= nil then
			return "FAIL", "the repair created a dont_pause field on a popup that had none"
		end

		-- 4. IDEMPOTENCE. Init runs once per dialog, but the wrapper must be
		--    safe if a future engine path re-runs it (or if another mod chains
		--    on top and calls through twice).
		clear(subject)
		if subject.dont_pause ~= false then
			return "FAIL", "a second pass changed the result"
		end

		return "PASS", "the game's one dont_pause popup is cleared so vanilla's Init builds its XPauseLayer, already-pausing popups and popups with no flag at all are untouched, and the pass is idempotent — the wrapper's INSTALLATION is evidenced by apply()'s own read-back (this fix reports inactive if the class write does not land). ⛔ NOT claimed: that the game visibly pauses on screen — that is a screen event, not a value read"
	end,
})
```

⚠️ The probe depends on `local FixMissing = SMRTest.FixMissing` at the top of
the wave file, which stays in place for the C39 probe.
