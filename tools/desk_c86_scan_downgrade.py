#!/usr/bin/env python3
"""C86 scan-downgrade control over the shipped MapSector:Scan body.

The 1.1.0 body is extracted by the same function delimiter used by bodycheck and
loaded under its real path and line offset. The module is loaded whole through
its Register/Require seam. Engine callbacks are inert stubs so the assertions
measure only status transitions; this is a desk model, not an in-game scan.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import deskbench as db  # noqa: E402

MODULE = os.path.join(db.REPO, "Code", "Fix_ScanDowngrade.lua")

PRELUDE = db.ENGINE_SHIMS + r'''
MapSector = { status = "unexplored" }
RevealedMapSector = {}
function RevealedMapSector:new(props, map)
	props.map = map
	return props
end

function DelayedCall() end
function RevealDeposits() return 0 end
function Msg() end
function OnDepositsSpawned() end
function GetMissionSponsor() return { id = "IMM" } end
function IsExplorationAvailable_Queue() return false end
function DeleteThread() end
function AddSectorScannedNotification() end
function RefreshSectorInfopanel() end

SMRFixPack = {}
APPLY_MODULE = true
function SMRFixPack.Register(_, def)
	if APPLY_MODULE then SMRFixPack.apply_error = def.apply() end
end
function SMRFixPack.Require(_, specs)
	for _, spec in ipairs(specs) do
		if spec.class and spec.method then
			local class = _G[spec.class]
			if type(class) ~= "table" or type(class[spec.method]) ~= "function" then
				return "missing method"
			end
		elseif spec.test and not spec.test() then
			return spec.reason or "shape declined"
		end
	end
end

function sector(status, class)
	local s = setmetatable({
		class = class or "MapSector",
		status = status,
		scan_progress = 17,
		city = { CheckScanAvailability = function() end },
		markers = { block = {}, surface = {}, subsurface = {}, deep = {} },
		deposits = { block = {}, surface = {}, subsurface = {}, deep = {} },
	}, { __index = MapSector })
	function s:RemoveFromQueue() self.removed = true end
	function s:HasBlockers() return false end
	function s:GetMap() return {} end
	function s:UpdateDecal() self.updated = true end
	return s
end
'''


def make_runtime(apply=True, class_default="unexplored"):
    rt = db.lua_runtime()
    rt.execute(PRELUDE)
    rt.globals().MapSector["status"] = class_default
    body, lo, hi = db.body("Lua/Exploration.lua", r"^function MapSector:Scan")
    db.load_at(rt, body, "=Lua/Exploration.lua", lo)
    rt.globals().APPLY_MODULE = apply
    db.load_at(rt, db.read(MODULE), "=Code/Fix_ScanDowngrade.lua", 1)
    return rt, lo, hi


def main():
    bench = db.Bench("C86 scan downgrade -- shipped MapSector:Scan and module")
    check = bench.check

    vanilla, lo, hi = make_runtime(False)
    print(f"extracted Lua/Exploration.lua:{lo}-{hi} ({hi - lo + 1} lines)")
    vanilla.execute('V = sector("deep scanned"); V:Scan("scanned", "probe")')
    check("vanilla reproduces deep scanned -> scanned",
          vanilla.globals().V["status"] == "scanned")

    fixed, _, _ = make_runtime(True)
    check("module shape guard accepts the shipped status schema",
          fixed.globals().SMRFixPack["apply_error"] is None)
    fixed.execute('''
	DOWN = sector("deep scanned")
	DOWN:Scan("scanned", "probe")
	UP1 = sector("unexplored")
	UP1:Scan("scanned", "probe")
	UP2 = sector("scanned")
	UP2:Scan("deep scanned", "probe")
	FOREIGN = sector("deep scanned", "ForeignMapSector")
	FOREIGN:Scan("scanned", "probe")
	''')
    g = fixed.globals()
    check("module preserves an already deep-scanned MapSector",
          g.DOWN["status"] == "deep scanned" and g.DOWN["removed"] is None)
    check("unexplored -> scanned is unchanged",
          g.UP1["status"] == "scanned" and g.UP1["removed"] is True)
    check("scanned -> deep scanned is unchanged",
          g.UP2["status"] == "deep scanned" and g.UP2["removed"] is True)
    check("foreign sector subclasses delegate unchanged",
          g.FOREIGN["status"] == "scanned" and g.FOREIGN["removed"] is True)

    declined, _, _ = make_runtime(True, "unknown")
    check("shape drift declines the module fail-closed",
          declined.globals().SMRFixPack["apply_error"] is not None)

    return bench.finish(
        "ALL DEMANDS HELD -- vanilla downgrades; the module blocks only the "
        "known downward transition on exact shipped sectors."
    )


if __name__ == "__main__":
    sys.exit(main())
