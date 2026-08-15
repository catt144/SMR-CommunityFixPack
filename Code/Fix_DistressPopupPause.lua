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
