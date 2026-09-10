#!/usr/bin/env python3
"""Do the kit probes for F67 (LanderEmptyLaunch) and F59 (FreedHousingNotice) discriminate on the 1.1.0 bodies?

Written 2026-09-09 by hotfix2 link 99b Unit B (session scratchpad); promoted to
tools/ the same day on the owner's ruling (checklist 131). The demands are
verbatim; the OLD-probe legs now pin the kit commit that preceded the rebuild
(`c1114ed`) so they keep meaning after the working copy moved on.

The shipped 1.1.0 bodies are extracted with tools/luafn.find_bodies and loaded
under their REAL file names with their REAL line offsets, so an error message
here is byte-comparable to the sitting's log line -- and legs L0 demand exactly
that: the pre-rebuild probe text must reproduce the two ERROR lines the
2026-09-09 suite run printed. The module files are loaded whole through a stub
SMRFixPack.Register (with an APPLY switch, so "registered active but the wrapper
never installed" is a leg); the probe files are loaded whole through a mini
SMRTest mirroring 00_TestCore's contracts. Nothing is retyped except the L4
vanilla-gate demonstration, which says so.

Demands, per probe:
  L0  OLD probe text vs the 1.1.0 body -> the sitting's exact ERROR line
  L1  module registered `active`, apply NOT run -> FAIL on the defect clause
  L2  module applied -> PASS
  L3  an over-broad wrapper -> FAIL on the over-broad clause
  L4  (F67 only) vanilla alone: a LOADED fixture reads false inside its first
      automode hour and true two hours in -- the :554 gate a naive fixture trips

Usage: python tools/desk_probes_f67_f59.py   (needs the local Test Kit, SMR_TESTKIT)
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import deskbench as db  # noqa: E402

KIT_BEFORE_REBUILD = "c1114ed"   # the kit commit before 99b's 29fd13b/4f062de

PRELUDE = db.ENGINE_SHIMS + r'''
GAME_TIME = 1000000
function GameTime() return GAME_TIME end
const = { HourDuration = 2500 }
function IsValid(o) return type(o) == "table" end
function RebuildInfopanel() end
UniversalRocketBase = {}
AutoMode = { IsAutoModeEnabled = function() return true end }
Colonist = {}
Residence = {}

SMRTest = { probes = {}, order = {}, last = {} }
function SMRTest.Register(id, def) SMRTest.probes[id] = def end
function SMRTest.FromFixPack() return true end
local function with_globals(vars, fn)
	local saved = {}
	for k, v in pairs(vars) do saved[k] = rawget(_G, k); rawset(_G, k, v) end
	local ok, res = pcall(fn)
	for k in pairs(vars) do rawset(_G, k, saved[k]) end
	return ok, res
end
-- the real WithGlobals defers an ERROR verdict; re-raising gives Run the same verdict
function SMRTest.WithGlobals(vars, fn) local ok, res = with_globals(vars, fn); if not ok then error(res, 0) end; return res end
function SMRTest.TryWithGlobals(vars, fn) return with_globals(vars, fn) end
function SMRTest.FixStatus(id) local f = rawget(_G, "SMRFixPack") and SMRFixPack.fixes[id]; if f then return f.status, f.detail end end
function SMRTest.FixMissing(id)
	if not rawget(_G, "SMRFixPack") then return "FAIL", "fix pack not loaded (bug reproduces)" end
	local status, detail = SMRTest.FixStatus(id)
	if not status then return "FAIL", "fix '" .. id .. "' not registered" end
	if status ~= "active" then return "FAIL", "fix '" .. id .. "' is " .. status end
end
function SMRTest.FixRetired(id) if SMRTest.FixStatus(id) then return "FAIL", "registered" end end
function SMRTest.Print() end
function SMRTest.Defer() end
function SMRTest.Run(id)
	local ok, status, msg = pcall(SMRTest.probes[id].run)
	if not ok then return "ERROR", tostring(status) end
	return status or "SKIP", msg
end

APPLY = true
SMRFixPack = { fixes = {}, order = {}, Require = function() return nil end }
function SMRFixPack.Register(id, def)
	SMRFixPack.fixes[id] = { status = "active" }
	SMRFixPack.order[#SMRFixPack.order + 1] = id
	if APPLY then
		local err = def.apply()
		if err then SMRFixPack.fixes[id].status = "inactive"; SMRFixPack.fixes[id].detail = err end
	end
end
'''

SHIPPED = {
    "Lua/UniversalRocket.lua": [
        r"^function UniversalRocketBase:IsCargoReady\(",
        r"^function UniversalRocketBase:WaitsForManualLaunch\(",
        r"^function UniversalRocketBase:GetArrivalLocType\(",
    ],
    "Lua/Units/Colonist.lua": [r"^function Colonist:SetResidence\("],
    "Lua/Buildings/Residence.lua": [r"^function Residence:GetFreeSpace\("],
}


def runtime():
    rt = db.lua_runtime()
    rt.execute(PRELUDE)
    return rt


def load_shipped(rt):
    spans = []
    for rel, pats in SHIPPED.items():
        for pat in pats:
            text, s, e = db.body(rel, pat)
            db.load_at(rt, text, "=" + rel, s)
            spans.append((rel, pat.strip("^\\("), s, e))
    return spans


def leg(module_rel, kit_rel, kit_text, apply, probe_id, rewrap=None):
    rt = runtime()
    load_shipped(rt)
    rt.globals().APPLY = apply
    db.load_at(rt, db.read(os.path.join(db.REPO, module_rel)), "=" + module_rel)
    if rewrap:
        rt.execute(rewrap)
    db.load_at(rt, kit_text, "=" + kit_rel)
    return rt.eval("function(id) return SMRTest.Run(id) end")(probe_id)


def main():
    bench = db.Bench("F67 / F59 kit-probe falsifier -- shipped bodies at their real lines, module + probe text verbatim")
    expect = bench.check

    kit2_new = db.read(os.path.join(db.TESTKIT, "Code", "20_Probes_Wave2.lua"))
    kit3_new = db.read(os.path.join(db.TESTKIT, "Code", "30_Probes_Wave3.lua"))
    kit2_old = db.git_show(db.TESTKIT, KIT_BEFORE_REBUILD, "Code/20_Probes_Wave2.lua")
    kit3_old = db.git_show(db.TESTKIT, KIT_BEFORE_REBUILD, "Code/30_Probes_Wave3.lua")

    rt = runtime()
    for rel, name, s, e in load_shipped(rt):
        print(f"extracted {rel} {name} :{s}-{e}")
    print()

    # ---------------- B1 LanderEmptyLaunch ----------------
    print("== LanderEmptyLaunch (F67) ==")
    st, msg = leg("Code/Fix_LanderEmptyLaunch.lua", "Code/20_Probes_Wave2.lua", kit2_old, True, "LanderEmptyLaunch")
    expect("[F67 L0] pre-rebuild probe text vs 1.1.0 body reproduces the sitting's ERROR line",
           st == "ERROR" and "Lua/UniversalRocket.lua:544: attempt to call a nil value (method 'WaitsForManualLaunch')" in msg,
           f"{st}: {msg}")
    st, msg = leg("Code/Fix_LanderEmptyLaunch.lua", "Code/20_Probes_Wave2.lua", kit2_new, False, "LanderEmptyLaunch")
    expect("[F67 L1] module registered active, apply NOT run (vanilla body) -> FAIL on the empty clause",
           st == "FAIL" and "empty auto rocket reports ready" in msg, f"{st}: {msg}")
    st, msg = leg("Code/Fix_LanderEmptyLaunch.lua", "Code/20_Probes_Wave2.lua", kit2_new, True, "LanderEmptyLaunch")
    expect("[F67 L2] module applied -> PASS", st == "PASS", f"{st}: {msg}")
    st, msg = leg("Code/Fix_LanderEmptyLaunch.lua", "Code/20_Probes_Wave2.lua", kit2_new, True, "LanderEmptyLaunch",
                  rewrap="local o = UniversalRocketBase.IsCargoReady; function UniversalRocketBase:IsCargoReady(...) return false end")
    expect("[F67 L3] over-broad wrapper (always false) -> FAIL on the loaded clause",
           st == "FAIL" and "LOADED auto rocket is blocked" in msg, f"{st}: {msg}")
    # L4: the vanilla :554 gate on a FRESH automode fixture -- retyped minimal fixture, demonstration only
    rt = runtime()
    load_shipped(rt)
    got = rt.execute(r'''
		local R = UniversalRocketBase
		local function fx(start)
			return {
				cargo = { Metals = { class = "Metals", requested = 5000, amount = 5000 } },
				departures = {}, boarded = {}, FuelResource = "Fuel",
				arrival_loc = { spot_type = "asteroid" }, automode_start_time = start,
				HasMember = function(self, k) return rawget(self, k) ~= nil end,
				GetLaunchIssue = function() return "waiting_cargo" end,
				HasEnoughFuelToLaunch = function() return true end,
				WaitsForManualLaunch = R.WaitsForManualLaunch, GetArrivalLocType = R.GetArrivalLocType,
				AreEarthDepartColonistsReady = function() return true end,
				GetCargoResourcesStatus = function() return "ready" end,
				IsAutoModeEnabled = function() return true end, IsSpecialAutomode = function() return false end,
				IsPlayerControlled = function() return true end, CheckAutoDepart = function() return true end,
			}
		end
		return tostring(R.IsCargoReady(fx(GameTime()))) .. "/" .. tostring(R.IsCargoReady(fx(GameTime() - 2 * const.HourDuration)))
	''')
    expect("[F67 L4] vanilla alone: LOADED fixture reads false inside its first automode hour, true two hours in (the :554 gate; retyped fixture)",
           got == "false/true", got)

    # ---------------- B2 FreedHousingNotice ----------------
    print("\n== FreedHousingNotice (F59) ==")
    st, msg = leg("Code/Fix_FreedHousingNotice.lua", "Code/30_Probes_Wave3.lua", kit3_old, True, "FreedHousingNotice")
    expect("[F59 L0] pre-rebuild probe text vs 1.1.0 body reproduces the sitting's ERROR line",
           st == "ERROR" and "Lua/Units/Colonist.lua:2914: attempt to call a nil value (method 'UpdateLowComfortNotification')" in msg,
           f"{st}: {msg}")
    st, msg = leg("Code/Fix_FreedHousingNotice.lua", "Code/30_Probes_Wave3.lua", kit3_new, False, "FreedHousingNotice")
    expect("[F59 L1] module registered active, apply NOT run (vanilla body) -> FAIL: nobody told",
           st == "FAIL" and "does not offer itself" in msg, f"{st}: {msg}")
    st, msg = leg("Code/Fix_FreedHousingNotice.lua", "Code/30_Probes_Wave3.lua", kit3_new, True, "FreedHousingNotice")
    expect("[F59 L2] module applied -> PASS", st == "PASS", f"{st}: {msg}")
    st, msg = leg("Code/Fix_FreedHousingNotice.lua", "Code/30_Probes_Wave3.lua", kit3_new, True, "FreedHousingNotice",
                  rewrap=r'''
		local o = Colonist.SetResidence
		function Colonist:SetResidence(home, ...)
			local left = self.residence
			local r1, r2 = o(self, home, ...)
			if left and left ~= self.residence then left:CheckHomeForHomeless() end   -- no free-space test
			return r1, r2
		end''')
    expect("[F59 L3] over-broad wrapper (notifies without the free-space test) -> FAIL on the no-slot clause",
           st == "FAIL" and "no usable slot still walks" in msg, f"{st}: {msg}")

    return bench.finish("ALL DEMANDS HELD -- both probes fail without the module, pass with it, fail on an\n"
                        "over-broad wrapper, and the pre-rebuild text reproduces the sitting's ERROR lines.")


if __name__ == "__main__":
    sys.exit(main())
