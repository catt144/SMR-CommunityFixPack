-- F59: A home falling vacant never tells the dome's homeless colonists about it.
--
-- Defect: Residence:CheckHomeForHomeless (Lua\Buildings\Residence.lua:160-168)
-- walks the dome's Homeless label and re-runs UpdateResidence on each colonist --
-- it is the mechanism that turns "a slot opened up" into "somebody moves in".
-- The shipped code calls it from Residence:GameInit (:64), Residence:SetUIWorking
-- when switched back on (:173) and Residence:SetDome (:214), plus Hotel.lua:23.
-- Every one of those is housing becoming available because the PLAYER did
-- something.
--
-- Nothing calls it when a slot frees up on its own: Residence:RemoveResident
-- (:119-126) only updates the occupation counter and resets the dome's free-space
-- cache. So after a resident dies, retires into a different home, is kicked out
-- or emigrates, the empty bed is invisible to the homeless standing in the same
-- dome until their own heavy update comes round -- and that is throttled to one
-- pass every 12 game hours once the colony passes 3600 colonists
-- (City.lua:117-119, consumed by Colonist:Idle :2338-2358).
--
-- ############################################################################
-- REPAIRED 2026-09-11 (ck151; migration audit + two independent re-derivations).
-- The module as first shipped was HARMFUL. What follows is the whole argument,
-- because the repair's shape is the part a reviewer has to check.
--
-- THE ORIGINAL MISTAKE, in one line: the hook was moved up from
-- Residence:RemoveResident to Colonist:SetResidence on the reasoning that
-- "SetResidence is RemoveResident's only caller, so hooking one level up means
-- the notification runs when the move is FINISHED". SetResidence finishing is
-- NOT the enclosing operation finishing. SetResidence has ELEVEN shipped
-- callers (enumerated below, re-derived from the 1.1.0.403908 tree) and several
-- of them call it as a MIDDLE step of a larger operation that still needs the
-- slot it just freed. Publishing "this bed is free" inside such an operation
-- hands the bed to a neighbour the enclosing operation is about to collide with.
-- FIX_POLICY §1.4 carries this as a general rule now; it was written from here.
--
-- TWO HARMS WERE MEASURED AT THE DESK (both on shipped bodies, module off/on),
-- and both are fixed by the deferral. A third, A3, was reported on 2026-09-11 and
-- then REFUTED the same day by my own re-measurement -- the retraction is kept
-- below rather than deleted, because the way it was wrong is reusable:
--
--   A1 -- expedition boarding loses the crew member's return home (1.1.0 only).
--   Colonist:EnterTransporter saves expedition_residence (Colonist.lua:5029-5031)
--   -> SetDome(false) (:5039) -> SetResidence(false) (:435) -> the old hook ->
--   a homeless neighbour takes the bed -> Unit.EnterTransporter (:5043) ->
--   Unit.lua:1305 Disappear -> :1225 OnDisappear -> Colonist:OnDisappear:5004
--   fails CanReserveResidence and :5007 clears the hold. 1.0.7 has no
--   expedition_residence at all, so this harm is 1.1.0-only.
--
--   A2 -- manual "Set Residence" OVERFILLS a residence (BOTH branches, present
--   since this module was written). Residence:ColonistInteract:342 ->
--   KickOldestResident:368 -> KickResident:157 -> SetResidence(false) -> the old
--   hook. Here self.dome is intact, so UpdateHomelessLabels:2912 put the
--   just-kicked resident into the dome's Homeless label inside the same call;
--   the hook then handed them back the very slot :348 was about to fill, and
--   Residence:AddResident's assert(GetFreeSpace() > 0) (:111-112) does not
--   unwind (EF-008) => three residents in a capacity-2 home, infopanel 3/2,
--   and the player's eviction silently undone.
--
--   ⛔ A3 -- RETRACTED, and the retraction is the instructive part.
--   CLAIMED 2026-09-11 while building: that at Residence:OnDestroyed:81-92 the old
--   hook dragged a colonist who was never a resident into the residence being
--   destroyed (`:89 self.colonists = {}` then dropping them onto a dead home), and
--   that deferral could not fix it because after the eviction loop free space is
--   the FULL capacity. REFUTED the same day, by re-running the same legs with the
--   shipped comfort bodies instead of the harness's stub:
--     * `GetResidenceComfort` (Residence.lua:416-434) gates on `ValidateBuilding`
--       (Workplace.lua:1316-1327), which tests `destroyed` (and `demolishing`,
--       `refab_work_request`, `exceptional_circumstances`) -- so it returns NIL for
--       a destroyed residence;
--     * `ChooseResidence` then scores it `min_int` (:454-455), and the only
--       tie-break that could still select it (:459) requires
--       `best_home ~= current_home`, which is FALSE for a homeless colonist.
--   ⇒ **vanilla cannot assign anyone into a destroyed residence, and neither could
--   the old hook.** With the real bodies loaded, absent / pre-repair / repaired are
--   INDISTINGUISHABLE at this site. The whole effect came from the harness stubbing
--   `GetResidenceComfort` to a constant, which silently deleted a vanilla guard.
--   ⇒ The UNRESOLVED lead that `bugs/F59.md` carried against this site is therefore
--   CLOSED IN VANILLA'S FAVOUR, not open: vanilla's own `colonist:UpdateResidence()`
--   at `:86` re-homes nobody into the home it is about to empty either.
--   Both halves are pinned as legs in `tools/desk_f59_interact.py` (stub shows the
--   difference, real bodies refute it) so this cannot be re-derived wrongly again.
--
--   WHY THE `not home.destroyed` GUARD STAYS ANYWAY, relabelled honestly: it is
--   DEFENSIVE, not harm-driven. It changes no outcome -- it declines work on a
--   residence vanilla would refuse one level down -- but it keeps the eviction loop
--   from creating a thread per evicted resident for nothing, and it means we would
--   not start handing out beds in rubble if `ValidateBuilding` ever stopped testing
--   `destroyed`. Removing it is a legitimate simplification; keeping it is not
--   evidence of a harm. ⛔ Do not cite A3 as a reason for anything.
--
-- THE REPAIR: publish the vacancy when the ENCLOSING OPERATION has finished,
-- not when SetResidence has. The only caller-agnostic definition of "the
-- enclosing operation has finished" available to a wrapper is "after the
-- current call stack has unwound", so the notification is handed to a one-shot
-- game-time thread and the decision to notify is re-taken there, on state that
-- by then includes whatever the enclosing operation did with the slot:
--   * A1: by the time the thread wakes, OnDisappear:5005 has taken the hold, and
--     GetFreeSpace() subtracts #self.reserved (Residence.lua:232-234) => 0 free
--     => we decline. The crew keeps its home.
--   * A2: by the time the thread wakes, ColonistInteract:348 has assigned the
--     forced colonist => 0 free => we decline. 2/2, eviction stands, no assert.
--   * ordinary vacancy (death, retirement, dome change, the UI kick button):
--     nothing refilled the slot, so it is still free and we notify. The benefit
--     is intact -- that is the whole point of the module, and it is checked by
--     cross-sensitive legs in both harnesses.
-- EF-029 is what makes this sound: CreateGameTimeThread DEFERS -- the body does
-- NOT run before the creating statement continues (MEASURED 2026-08-01, owner at
-- the keyboard). The engine's Lua is cooperative, so a thread cannot resume in
-- the middle of a synchronous call stack either.
--
-- WHY NOT THE TWO NARROWER SHAPES FOR A1/A2, both of which were considered and
-- REJECTED on measured grounds (this is the part a reviewer should attack first):
--   * "Exclude self.expedition_residence" -- the migration audit's proposal, and
--     the unbuilt candidate in tools/desk_f59_expedition.py. It is NECESSARY BUT
--     NOT SUFFICIENT: it does nothing whatever for A2, which is the more
--     reachable harm (an ordinary four-click player action, on both branches).
--   * "Decline while inside Residence:KickResident" -- a caller-state-keyed
--     guard, which is the shape FIX_POLICY §1.4 points at. It is WRONG HERE, and
--     measurably so: KickResident has THREE shipped callers, and the other two
--     are the infopanel's own kick button
--     (Lua/XDef/sectionOccupantList.generated.lua:34 and
--     sectionResidenceList.generated.lua:34), where the bed genuinely frees and
--     the notification is exactly what the player should get. Keying on the
--     forced colonist's own state is no better: user_forced_residence survives
--     for g_Consts.ForcedByUserLockTimeout, one sol (__const.lua:171-177), so a
--     "somebody is forced to this home" test would suppress ordinary
--     notifications for that residence for a sol of game time. Either variant
--     buys A2 by losing the benefit in reachable cases -- a removal wearing a
--     fix's clothes. Deferral buys A2 while keeping it, and covers the callers
--     nobody has enumerated yet, which is the failure mode that produced this
--     entry in the first place.
--
-- THE ELEVEN CALLERS OF Colonist:SetResidence, and what this guard does to each
-- (grep-verified against 1.1.0.403908: eleven call sites, ONE definition at
-- Colonist.lua:2898, no subclass override anywhere in the tree):
--   Colonist.lua:435  SetDome            A1's window. CHANGED: deferred, so the
--                                        expedition hold is taken first. Ordinary
--                                        dome changes still notify.
--   Colonist.lua:1255 Erase              UNCHANGED in effect, one tick later.
--   Colonist.lua:1297 death              UNCHANGED in effect, one tick later.
--   Colonist.lua:2926 UpdateResidence    the intended case. UNCHANGED in effect,
--                                        one tick later.
--   Colonist.lua:4995 OnDisappear        a no-op on the transport path (:5039's
--                                        SetDome already cleared residence, so
--                                        self.residence == home == false returns
--                                        at :2901). Deferral also covers it if a
--                                        path ever reaches it with a live home,
--                                        since :5003-5008 is the same shape as A1.
--   Residence.lua:85  OnDestroyed        UNCHANGED in outcome. The `destroyed`
--                                        guard declines here, but vanilla refuses
--                                        the assignment anyway -- see A3's
--                                        retraction. Defensive only.
--   Residence.lua:157 KickResident       A2. CHANGED: deferred, so :348's
--                                        assignment lands first and we decline.
--                                        The infopanel kick button (same method,
--                                        two generated callers) still notifies.
--   Residence.lua:265 capacity shrink    UNCHANGED, and it never opened: the loop
--                                        runs only while #reserved + #colonists >
--                                        capacity - closed, so GetFreeSpace() is
--                                        Max(0, negative) == 0 at every hook call
--                                        and the pre-filter declines. Zero threads
--                                        are created there.
--   Residence.lua:348 ColonistInteract's  the forced colonist's OLD home genuinely
--                     own assignment     frees. UNCHANGED in effect, one tick later.
--   NaturalHabitat.lua:7                 a no-op: :6's SetDome(false) already
--                                        cleared residence via Colonist.lua:435.
--                                        That :435 call is A2's shape again on a
--                                        MicroGHabitat -- KickOldestResident ->
--                                        NaturalHabitatBase:KickResident -> SetDome
--                                        -> SetResidence -- and deferral covers it
--                                        without knowing it exists. (An
--                                        expedition_residence exclusion would not
--                                        have.)
--   Data/TraitPreset.lua:772 Youth       leaves a NurseryBase and :773 re-houses
--                                        immediately. UNCHANGED in effect, one
--                                        tick later.
--
-- SAVEGAME / §3a LAYER, stated because §3a requires anything that creates its own
-- game-time thread to say which layer it is on. This is a NEW capturable site:
-- the thread blocks in Sleep, so a save written in that window serialises the
-- thread with our body by value (EF-023 route (a)). It is LAYER-2-EQUIVALENT by
-- construction rather than by shape: the FIRST statement after the only yield is
-- the orphan gate, and no vanilla state is touched before it, so a thread that
-- comes back in a save with the mod uninstalled executes nothing, sets nothing
-- and exits at a point we chose (§3a's orphan-gate rule). With the mod present it
-- resumes correctly -- every fact it needs is re-read after the wake, nothing is
-- carried across it. The body has zero upvalues (globals and a literal id only)
-- and holds no colonist reference, which matters because two of the eleven
-- callers (Erase, death) delete the colonist inside the same operation.
-- ⚠️ This adds a row to the capturable-code set that reports/D13_EXPOSED_SET.md
-- enumerates; that document is D13's own derivation and is not edited from here.
--
-- Not hooked: Residence:CancelResidenceReservation (:385-399), the other site
-- that frees a slot without telling anyone. Residence:AddResident calls it
-- (via the colonist, :109) two lines before that same
-- assert(self:GetFreeSpace() > 0), so notifying from there reintroduces exactly
-- the race described above. The reservation case is already bounded instead by
-- F58's daily stale-reservation sweep plus the normal heavy update.
-- ############################################################################

-- MANIFEST (FIX_POLICY §2b) -- machine-read by `python tools/bodycheck.py`.
-- Pinned 2026-09-08, extended 2026-09-11 with the three bodies the REPAIR depends
-- on, against shipped game 1.1.0.403908. ⛔ These are CLAIMS about the shipped
-- tree, not a clearance: re-pin them deliberately when a target moves, never to
-- silence a BODY-CHANGED.
-- SRC: Lua/Buildings/Residence.lua Residence:RemoveResident sha256=a549068bfad65163f3513b1c70b8d895cb7c5dc3b2e51ce49745f77ea9679de9
--   (Lua/Buildings/Residence.lua:119-126 at pin time)
-- DEFECT: self\.parent_dome:ResetFreeSpace\(\)\s+end\s+end
--   ResetFreeSpace is the LAST act: the slot opens and CheckHomeForHomeless is
--   never called. ⚠️ States an absence by pinning the tail (FIX_POLICY §2b) --
--   if vanilla adds the wake call here, this stops matching, which is the
--   intended signal
-- SRC: Lua/Buildings/Residence.lua Residence:GetFreeSpace sha256=d7b7f54cb357379f029f5004b7b77e6141c5da184c43401c5c09db92e28ea67f
--   (Lua/Buildings/Residence.lua:232-234 at pin time)
-- DEFECT: #self\.reserved\s*\+\s*#self\.colonists
--   ⚠️ NOT a defect -- the load-bearing PROPERTY of the repair (the §2b absence
--   form, used here for a dependency). A reservation must count against free
--   space, or the deferred re-check cannot see that OnDisappear took the
--   expedition hold and A1 comes back
-- SRC: Lua/Units/Unit.lua Unit:EnterTransporter sha256=c76dc53be62915622e43b2661efad5dfba82dd58ad9cc651f831f17764795c62
--   (Lua/Units/Unit.lua:1292-1306 at pin time)
-- DEFECT: self:Disappear\("keep in holder"
--   ⚠️ A dependency, not a defect: boarding must reach OnDisappear SYNCHRONOUSLY
--   (:1305 -> Unit:Disappear:1225, no yield between). If a yield ever appears in
--   this leg, the deferred notification could fire before the hold is taken and
--   A1 returns
-- SRC: Lua/Buildings/Residence.lua Residence:ColonistInteract sha256=9a1c8c36ae7b2e02a9df2c6823f5c2dc708e556796f19ce9a3c77739d62cd32f
--   (Lua/Buildings/Residence.lua:330-354 at pin time)
-- DEFECT: KickOldestResident\(\)[\s\S]*SetResidence\(self\)
--   ⚠️ A dependency, not a defect: the kick and the assignment must stay in ONE
--   synchronous body. If vanilla ever splits them across a yield, the deferred
--   notification lands in the gap and A2 returns

SMRFixPack.Register("FreedHousingNotice", {
	title = "A home falling vacant is offered to the dome's homeless straight away",
	apply = function()
		-- NB: CheckHomeForHomeless/GetFreeSpace are declared on Residence
		-- itself, which is the class to check (pre-flattening).
		local err = SMRFixPack.Require("FreedHousingNotice", {
			{ class = "Colonist", method = "SetResidence" },
			{ class = "Residence", method = "CheckHomeForHomeless",
			  reason = "Residence.CheckHomeForHomeless/GetFreeSpace not found (game update changed them?)" },
			{ class = "Residence", method = "GetFreeSpace",
			  reason = "Residence.CheckHomeForHomeless/GetFreeSpace not found (game update changed them?)" },
			{ global = "CreateGameTimeThread",
			  reason = "CreateGameTimeThread/Sleep not found — the repair defers the notification out of the caller's call stack and cannot run without them" },
			{ global = "Sleep",
			  reason = "CreateGameTimeThread/Sleep not found — the repair defers the notification out of the caller's call stack and cannot run without them" },
		})
		if err then return err end
		local C = Colonist

		-- The deferred half. Declared as a named local with ZERO UPVALUES so the
		-- thread body carries nothing of ours by value except itself (§3a), and
		-- takes the home as a thread argument rather than a closure capture.
		local function notify_freed_home(home)
			Sleep(0)
			-- ⛔ orphan gate (FIX_POLICY §3a), the FIRST statement after the only
			-- yield, per the precedent at Fix_ExtenderFlapChurn:97. No vanilla
			-- state has been touched yet, so a bare return complies.
			if not SMRFixPack then return end
			-- Everything is re-read AFTER the wake. This is the repair: by now the
			-- enclosing operation has finished, so free space reflects whatever it
			-- did with the slot -- the expedition hold it reserved (A1), the forced
			-- colonist it assigned (A2), or nothing at all (an ordinary vacancy).
			if IsValid(home) and not home.destroyed and home.ui_working
				and home.parent_dome and home:GetFreeSpace() > 0
				and type(home.CheckHomeForHomeless) == "function" then
				home:CheckHomeForHomeless()
			end
		end

		local orig = C.SetResidence
		function C:SetResidence(home, ...)
			local left = self.residence
			local r1, r2 = orig(self, home, ...)
			-- FIX (F59): the home we just moved out of may now have a bed free.
			-- Offer it to the dome's homeless instead of leaving it to their next
			-- heavy update (a 12-hour wait in a large colony) -- but offer it
			-- AFTER the operation that called us has finished, never inside it.
			-- The test below is only a cheap pre-filter: it is deliberately the
			-- same one the pre-repair module used (plus `destroyed`), so no event
			-- this module used to consider is dropped here. The real decision is
			-- re-taken in notify_freed_home once the stack has unwound.
			if left and left ~= self.residence and IsValid(left)
				and not left.destroyed and left.ui_working
				and type(left.CheckHomeForHomeless) == "function"
				and left:GetFreeSpace() > 0 then
				CreateGameTimeThread(notify_freed_home, left)
			end
			return r1, r2
		end
	end,
})
