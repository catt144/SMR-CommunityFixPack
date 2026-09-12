#!/usr/bin/env python3
"""C85 clogged-building release over the shipped Setexceptional_circumstances body.

The cure is the game's OWN setter, so the harness extracts that body by the same
delimiter bodycheck hashes with and loads it under its real path and line offset;
the module is loaded whole through its Register/Require seam. Every leg drives
the module's real sweep against fake buildings whose two saved fields are the
only thing that decides the outcome.

⛔ WHAT IS STUBBED, AND WHY EACH IS A TOLERANCE AND NOT A DECISION (the F59 rule
in deskbench's header). The shipped setter calls exactly three methods on self --
UpdateWorking, UpdateConsumption, AttachSign (BaseBuilding.lua:470-480). None of
them can refuse, validate or return a value the setter reads: the setter ignores
their results entirely and has already written both fields before the first call.
So no-op stubs remove nothing the shipped body uses to DECIDE. The one field that
does decide -- exceptional_circumstances_maintenance, read at :474 -- is set per
fixture, never stubbed, and leg (h) exercises both of its values.

⭐ FALSIFIED 2026-09-12 against guard-reverted copies of the module, because a
harness that cannot fail is not a falsifier and the builder's own control switch
(APPLY_MODULE) is not independent. Each row below is one replacement made in a
scratch copy of Code/Fix_CloggedBuildingRelease.lua, with MODULE pointed at it;
the named leg(s) must FAIL. Re-run this whenever a guard moves.

    reverted (1 hit each, verbatim)                      -> must fail
    "and not clogged_popup_running(building)"  -> "and true"      (b)
    "and not fix_after_storm_pending(building)" -> "and true"     (c), (c3)
    "and not a_storybit_popup_is_pending()"    -> "and true"      (e3)
    "return TGetID(reason) == CLOGGED_REASON_ID" -> "return true" (d)
    "local gone = shipped_defect_gone()"      -> "local gone = nil"
                                                  (g), (g2), (g3), (g4)
    "building:Setexceptional_circumstances(false)" -> "local _ = building"
                                 (a), (b2), (c2), (e2), (f), (h)

⚠️ ONE reversion is EXPECTED to change nothing, and that is a finding, not a gap:
reverting the sweep's whole-pass early-out ("if a_storybit_popup_is_pending() then
return end" -> "if false then ...") fails no leg, because should_release checks the
same thing per building. The early-out is an optimisation and the module says so.
Leg (e3) exists because the two sites otherwise mask each other through OnMsg.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import deskbench as db  # noqa: E402

MODULE = os.path.join(db.REPO, "Code", "Fix_CloggedBuildingRelease.lua")
CLOGGED = 789863173059
FOLLOW_UP = "BuildingClogged_1_FixAfterStorm"

PRELUDE = db.ENGINE_SHIMS + r'''
BaseBuilding = {}

-- TGetID, retyped from CommonLua/Core/localization.lua:47-64 for the two table
-- forms a saved T can take. LightUserdataToLocId is a C export with no desk
-- equivalent, so the packed-userdata form is out of this harness's reach and is
-- stated as such rather than faked.
function TGetID(T)
	if T == "" then return false end
	if type(T) ~= "table" then return false end
	if type(T[1]) == "number" then return T[1] end
	return false
end

-- The two GameVars and the popup queue, as the game shapes them
-- (_StoryBits.lua:129-130; Lua/UI/PopupNotification.lua).
g_StoryBitActive = {}
g_StoryBitStates = {}
g_PopupQueue = {}

BUILDINGS = {}
function AllMapsForEach(_, class, cb)
	SWEPT_CLASS = class
	for _, bld in ipairs(BUILDINGS) do cb(bld) end
end

SMRFixPack = { fixes = {}, data_edited = {} }
SMRFixPack_Disabled = {}
LOG = {}
function SMRFixPack.Log(fmt, ...) LOG[#LOG + 1] = string.format(fmt, ...) end
APPLY_MODULE = true
function SMRFixPack.Register(id, def)
	SMRFixPack.fixes[id] = { title = def.title, status = "pending", detail = "" }
	if APPLY_MODULE then
		local res = def.apply()
		SMRFixPack.apply_error = res
		SMRFixPack.fixes[id].status = type(res) == "string" and "inactive" or "active"
	end
end
function SMRFixPack.Require(_, specs)
	for _, spec in ipairs(specs) do
		if spec.probe then
			local ok, res = pcall(spec.probe)
			if not (ok and res == true) then return spec.reason or "probe declined" end
		elseif spec.test then
			if not spec.test() then return spec.reason or "shape declined" end
		elseif spec.class and spec.method then
			local class = _G[spec.class]
			if type(class) ~= "table" or type(class[spec.method]) ~= "function" then
				return (spec.class .. "." .. spec.method .. " not found")
			end
		elseif spec.global then
			if type(_G[spec.global]) ~= (spec.kind or "function") then
				return (spec.global .. " not found")
			end
		end
	end
end
function SMRFixPack.WhenActive(id, fn)
	return function(...)
		local f = SMRFixPack.fixes[id]
		if not (f and f.status == "active") then return end
		if SMRFixPack_Disabled[id] then return end
		return fn(...)
	end
end
OnMsg = {}

-- The shipped story bit's activation effect, as the preset loads it
-- (Data/StoryBit/BuildingClogged.lua:4-8): a Reason and NO Duration.
StoryBits = {
	BuildingClogged = {
		ActivationEffects = {
			{ Reason = { CLOGGED_ID, "Clogged after a Dust Storm." }, Duration = 0 },
		},
	},
}

function building(ec, reason_id, maintenance)
	local b = {
		exceptional_circumstances = ec,
		exceptional_circumstances_reason = reason_id and { reason_id, "some reason" } or false,
		exceptional_circumstances_maintenance = maintenance or false,
		updated_working = 0,
		signs = 0,
	}
	function b:UpdateWorking() self.updated_working = self.updated_working + 1 end
	function b:UpdateConsumption() end
	function b:AttachSign(on) self.signs = self.signs + 1 self.sign_on = on end
	setmetatable(b, { __index = BaseBuilding })
	BUILDINGS[#BUILDINGS + 1] = b
	return b
end
'''


def make_runtime(apply=True, duration=0, reason_id=CLOGGED, drop_setter=False):
    rt = db.lua_runtime()
    rt.execute("CLOGGED_ID = %d" % CLOGGED)
    rt.execute(PRELUDE)
    body, lo, hi = db.body("Lua/Buildings/BaseBuilding.lua",
                           r"^function BaseBuilding:Setexceptional_circumstances")
    if drop_setter:
        # A shape-drift leg: the setter stops clearing the two saved fields, so
        # the behaviour probe must decline. Not the shipped body -- deliberately.
        rt.execute("function BaseBuilding:Setexceptional_circumstances() end")
    else:
        db.load_at(rt, body, "=Lua/Buildings/BaseBuilding.lua", lo)
    rt.execute("StoryBits.BuildingClogged.ActivationEffects[1].Duration = %d" % duration)
    rt.execute("StoryBits.BuildingClogged.ActivationEffects[1].Reason = { %d, 'r' }" % reason_id)
    rt.globals().APPLY_MODULE = apply
    db.load_at(rt, db.read(MODULE), "=Code/Fix_CloggedBuildingRelease.lua", 1)
    return rt, lo, hi


def main():
    bench = db.Bench("C85 clogged release -- shipped Setexceptional_circumstances and module")
    check = bench.check

    # ---- the module applies, and the probe is a real gate -------------------
    rt, lo, hi = make_runtime()
    print(f"extracted Lua/Buildings/BaseBuilding.lua:{lo}-{hi} ({hi - lo + 1} lines)")
    check("the behaviour probe accepts the shipped setter",
          rt.globals().SMRFixPack["apply_error"] is None)

    drifted, _, _ = make_runtime(drop_setter=True)
    check("a setter that no longer clears the fields declines the module fail-closed",
          drifted.globals().SMRFixPack["apply_error"] is not None)

    # ---- (a) the stuck building is released --------------------------------
    rt.execute('''
	STUCK = building(true, CLOGGED_ID)
	OnMsg.LoadGame()
	''')
    g = rt.globals()
    check("(a) a building stuck with the clogged reason is released",
          g.STUCK["exceptional_circumstances"] is False
          and g.STUCK["exceptional_circumstances_reason"] is False
          and g.STUCK["updated_working"] == 1)
    check("(a2) the sweep enumerates BaseBuilding, the devs' own reconcile class",
          g.SWEPT_CLASS == "BaseBuilding")
    check("(a3) the release is logged so the owner can read it back",
          any("released 1 building" in str(v) for v in dict(g.LOG).values()))

    # ---- (b) popup up right now: g_StoryBitActive interlock ----------------
    rt2, _, _ = make_runtime()
    rt2.execute('''
	RUNNING = building(true, CLOGGED_ID)
	OTHER = building(true, CLOGGED_ID)
	g_StoryBitActive[1] = { id = "BuildingClogged", object = RUNNING }
	OnMsg.LoadGame()
	''')
    g2 = rt2.globals()
    check("(b) a building whose BuildingClogged is still running is untouched",
          g2.RUNNING["exceptional_circumstances"] is True)
    check("(b2) ... while a different stuck building in the same pass IS released",
          g2.OTHER["exceptional_circumstances"] is False)

    # ---- (c) fix-after-storm armed: g_StoryBitStates interlock -------------
    rt3, _, _ = make_runtime()
    rt3.execute('''
	WAITING = building(true, CLOGGED_ID)
	OTHER = building(true, CLOGGED_ID)
	g_StoryBitStates["%s"] = { id = "%s", object = WAITING }
	OnMsg.LoadGame()
	''' % (FOLLOW_UP, FOLLOW_UP))
    g3 = rt3.globals()
    check("(c) a building with the fix-after-storm follow-up armed is untouched",
          g3.WAITING["exceptional_circumstances"] is True)
    check("(c2) ... and an unrelated stuck building is still released",
          g3.OTHER["exceptional_circumstances"] is False)

    rt3b, _, _ = make_runtime()
    rt3b.execute('''
	ANY = building(true, CLOGGED_ID)
	g_StoryBitStates["%s"] = { id = "%s", object = false }
	OnMsg.LoadGame()
	''' % (FOLLOW_UP, FOLLOW_UP))
    check("(c3) a follow-up armed with NO object stands the sweep down (fail closed)",
          rt3b.globals().ANY["exceptional_circumstances"] is True)

    # ---- (d) a different reason id is not ours -----------------------------
    rt4, _, _ = make_runtime()
    rt4.execute('''
	LAW = building(true, 374137718365)          -- LawEffectTurnOffBuildings
	ELECTRONICS = building(false, 149427596640) -- the drones reply's end state
	PLAIN = building(true, false)               -- disabled, no reason at all
	OnMsg.LoadGame()
	''')
    g4 = rt4.globals()
    check("(d) a law-disabled building (different reason id) is untouched",
          g4.LAW["exceptional_circumstances"] is True)
    check("(d2) the drones reply's end state is untouched (ec already false)",
          g4.ELECTRONICS["exceptional_circumstances"] is False
          and g4.ELECTRONICS["updated_working"] == 0)
    check("(d3) a building disabled with no reason at all is untouched",
          g4.PLAIN["exceptional_circumstances"] is True)

    # ---- (e) queued story-bit popup: whole-pass stand-down -----------------
    rt5, _, _ = make_runtime()
    rt5.execute('''
	QUEUED = building(true, CLOGGED_ID)
	g_PopupQueue[1] = { is_storybit = true, title = "Building Clogged" }
	OnMsg.LoadGame()
	''')
    check("(e) a queued or open story-bit popup stands the whole pass down",
          rt5.globals().QUEUED["exceptional_circumstances"] is True)

    rt5b, _, _ = make_runtime()
    rt5b.execute('''
	OK = building(true, CLOGGED_ID)
	g_PopupQueue[1] = { title = "some other popup" }
	OnMsg.LoadGame()
	''')
    check("(e2) a non-story-bit popup does NOT stand the sweep down",
          rt5b.globals().OK["exceptional_circumstances"] is False)

    # (e3) The sweep has TWO popup checks -- should_release's clause and the
    # whole-pass early-out -- and via OnMsg they mask each other, so leg (e)
    # cannot say which one works. Drive the exposed predicate directly: this is
    # the exact entry point the kit probe uses, and it isolates the real guard.
    rt5c, _, _ = make_runtime()
    rt5c.execute('''
	SUBJECT = building(true, CLOGGED_ID)
	BEFORE = SMRFixPack.CloggedRelease.ShouldRelease(SUBJECT)
	g_PopupQueue[1] = { is_storybit = true }
	DURING = SMRFixPack.CloggedRelease.ShouldRelease(SUBJECT)
	''')
    g5c = rt5c.globals()
    check("(e3) the exposed predicate itself refuses while a story-bit popup is pending",
          g5c.BEFORE is True and g5c.DURING is False)

    # ---- (f) the daily pass reaches the same end state --------------------
    rt6, _, _ = make_runtime()
    rt6.execute('''
	MIDSESSION = building(true, CLOGGED_ID)
	OnMsg.NewDay(7)
	''')
    check("(f) the daily pass releases a mid-session loss with no load",
          rt6.globals().MIDSESSION["exceptional_circumstances"] is False)

    # ---- (g) simulated post-patch vanilla: the module stands down ---------
    rt7, _, _ = make_runtime(duration=2160000)
    rt7.execute('''
	STILL_STUCK = building(true, CLOGGED_ID)
	OnMsg.LoadGame()
	''')
    g7 = rt7.globals()
    check("(g) a Duration on the shipped effect latches the module inactive",
          g7.SMRFixPack["fixes"]["CloggedBuildingRelease"]["status"] == "inactive")
    check("(g2) ... and it touches nothing in that pass",
          g7.STILL_STUCK["exceptional_circumstances"] is True)
    check("(g3) ... and says RETIRE candidate in the log, for logscan",
          any("RETIRE candidate" in str(v) for v in dict(g7.LOG).values()))

    rt7b, _, _ = make_runtime(reason_id=111222333444)
    rt7b.execute('OTHER_REASON = building(true, CLOGGED_ID) OnMsg.LoadGame()')
    check("(g4) a changed shipped reason id also latches inactive, and releases nothing",
          rt7b.globals().SMRFixPack["fixes"]["CloggedBuildingRelease"]["status"] == "inactive"
          and rt7b.globals().OTHER_REASON["exceptional_circumstances"] is True)

    # ---- (h) the maintenance field decides, and is never stubbed away -----
    rt8, _, _ = make_runtime()
    rt8.execute('''
	WITH_MAINT = building(true, CLOGGED_ID, true)
	OnMsg.LoadGame()
	''')
    g8 = rt8.globals()
    check("(h) a coexisting maintenance state is released but keeps its reason field "
          "(shipped :474 -- vanilla's own behaviour for this call)",
          g8.WITH_MAINT["exceptional_circumstances"] is False
          and g8.WITH_MAINT["exceptional_circumstances_reason"] is not False
          and g8.WITH_MAINT["exceptional_circumstances_maintenance"] is True)

    # ---- (i) NEGATIVE: registered but never applied ------------------------
    rt9, _, _ = make_runtime(apply=False)
    rt9.execute('''
	NEVER = building(true, CLOGGED_ID)
	OnMsg.LoadGame()
	''')
    check("(i) NEGATIVE -- a module registered but never applied releases nothing",
          rt9.globals().NEVER["exceptional_circumstances"] is True)

    # ---- (j) NEGATIVE: the user veto is honoured in the handler ------------
    rt10, _, _ = make_runtime()
    rt10.execute('''
	VETOED = building(true, CLOGGED_ID)
	SMRFixPack_Disabled["CloggedBuildingRelease"] = true
	OnMsg.LoadGame()
	''')
    check("(j) NEGATIVE -- a mid-session veto stops the sweep (FIX_POLICY §2, A1)",
          rt10.globals().VETOED["exceptional_circumstances"] is True)

    return bench.finish(
        "ALL DEMANDS HELD -- the shipped setter clears the stuck pair; the module "
        "releases only buildings carrying THIS reason id with no story bit running, "
        "no follow-up armed and no story-bit popup pending, and stands down when "
        "the shipped effect gains a Duration or changes its reason."
    )


if __name__ == "__main__":
    sys.exit(main())
