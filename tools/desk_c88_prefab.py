#!/usr/bin/env python3
"""C88 Building Codes vs prefabs, over the shipped LawDef ConstructionComplete handlers.

⭐ THE TWO SHIPPED HANDLERS ARE EXTRACTED FROM THE PRESET, NEVER RETYPED, and loaded
under their real file name and line offset, so an error inside one reads
`Data/LawDef/LawDef-Efficiency.lua:700: ...` exactly as a game log line would. They
are located by their law's own `id = "..."` line rather than by line number, so the
harness does not rot when the preset moves. The module is loaded whole through a stub
SMRFixPack.Register/Require/WhenActive seam.

⛔ WHAT IS STUBBED, AND WHY NONE OF IT DECIDES ANYTHING (the F59 rule in deskbench's
header). `IsKindOf` and `IsValid` are stood in — they are the engine's type and
validity tests, and each fixture states its own class list and validity explicitly
rather than being handed a constant, so both the true and the false branch are
exercised (legs e and the invalid-building leg). `SetModifier` is the real shipped
body, extracted from Lua/Modifiers.lua, NOT a stub -- which is the point of leg (f):
the no-op-on-equal-amounts behaviour that makes double application safe is vanilla's
own code, not an assumption. The law presets carry their real Parameters values read
through a retyped 6-line GetParameterValue (named below), and `ActiveLaws` is a plain
table exactly as the GameVar is.

⭐ FALSIFIED 2026-09-12 against guard-reverted copies of the module, because a harness
that cannot fail is not a falsifier and the builder's own APPLY_MODULE switch is not
independent. Each row is one replacement in a scratch copy of
Code/Fix_BuildingCodesPrefab.lua with MODULE pointed at it; the named legs FAILED, and
all nine guards were caught.

    reverted (1 hit each, verbatim)                       -> legs that failed
    "if not from_prefab then return end" -> ""                      (c3)
    "if laws[law_id] then" -> "if true then"                        (b), (b2)
    'if not IsKindOf(bld, "RequiresMaintenance") then return 0 end' -> ""   (e)
    "bld:SetModifier(PROP, law_id, ...)" -> ""                      (b), (b2)
    ... -> our OWN id instead of the law's                          (b), (b2)
    "if guard ~= true then return end" -> ""                        (h2)
    "return laws == nil or laws == false" -> "return laws == nil"
                                     (b), (b2), (f), (f1b), (h3)
    "SMRFixPack.OnDataReady(check_shape)" -> "check_shape()"
                                     (b), (b2), (f), (h), (h3)
    "local percent = law:GetParameterValue(PARAM)" -> "local percent = -30"  (b2)

⭐ THE LAST TWO ARE THE BUGS THIS BUILD ACTUALLY HAD, kept as variants on purpose.
`GameVar` rawsets its global to **false**, not nil, so a "no game loaded" test written
as `~= nil` would have declined the module on every boot; and running the guard at
apply time would have found an EMPTY preset map on every cold boot (the F75 lesson).
An earlier draft of this harness modelled `ActiveLaws = nil` and populated LawDefs
before loading the module, and so passed both bugs. It now models the real menu value
and the real cold-boot order, which is why those two rows fail loudly.

⚠️ Leg (c3) exists because of a falsification miss: removing the prefab gate changes no
END STATE, since our write carries the law's own id and coalesces with vanilla's inside
the shipped SetModifier. Only the CALL COUNT shows that our handler stayed out of a
normally-built building, and "this only ever acts on prefabs" is a claim the entry and
the release note make, so a leg has to hold it.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import deskbench as db  # noqa: E402

MODULE = os.path.join(db.REPO, "Code", "Fix_BuildingCodesPrefab.lua")
LAW_FILE = "Data/LawDef/LawDef-Efficiency.lua"
LAWS = ("Policy_BuildingCodesLax", "Policy_BuildingCodesStrict")
EXPECTED = {"Policy_BuildingCodesLax": 50, "Policy_BuildingCodesStrict": -30}


def law_handler(law_id, tree="1.1.0"):
    """-> (handler body text, 1-based first line) for one law's ConstructionComplete
    Handler, found by walking back from that law's own `id = "<law_id>",` line to the
    Handler above it inside the same PlaceObj('LawDef', ...)."""
    from luafn import read_lines
    lines = read_lines(os.path.join(db.TREES[tree], LAW_FILE))
    id_at = [i for i, l in enumerate(lines)
             if re.match(r"^\ttid = \"%s\",\s*$".replace("\\t\\t", "\t") % re.escape(law_id), l)
             or re.match(r"^\tid = \"%s\",\s*$" % re.escape(law_id), l)]
    assert len(id_at) == 1, "%s -> %d id lines for %s" % (LAW_FILE, len(id_at), law_id)
    # the Handler sits AFTER the id line, inside msg_reactions of the same LawDef
    start = None
    for i in range(id_at[0], min(id_at[0] + 20, len(lines))):
        if re.match(r"^\s*Handler = function \(self, bld, dome, from_prefab\)\s*$", lines[i]):
            start = i
            break
    assert start is not None, "%s: no Handler within 20 lines after id %s" % (LAW_FILE, law_id)
    end = None
    for i in range(start + 1, min(start + 20, len(lines))):
        if lines[i].strip() in ("end,", "end"):
            end = i
            break
    assert end is not None, "%s %s: Handler has no closing end," % (LAW_FILE, law_id)
    return "\n".join(lines[start:end + 1]).rstrip(","), start + 1


def law_param(law_id, tree="1.1.0"):
    """The shipped maintenance_change value for one law, read from its Parameters."""
    from luafn import read_lines
    lines = read_lines(os.path.join(db.TREES[tree], LAW_FILE))
    id_at = [i for i, l in enumerate(lines) if re.match(r"^\tid = \"%s\",\s*$" % re.escape(law_id), l)]
    assert len(id_at) == 1
    # Parameters sit ABOVE the id line in the same PlaceObj
    for i in range(id_at[0], max(id_at[0] - 40, -1), -1):
        if "'Name', \"maintenance_change\"" in lines[i]:
            m = re.search(r"'Value',\s*(-?\d+)", lines[i + 1])
            assert m, "no Value line after maintenance_change for %s" % law_id
            return int(m.group(1))
    raise AssertionError("no maintenance_change parameter for %s" % law_id)


PRELUDE = db.ENGINE_SHIMS + r'''
-- table.find_value(list, field, value) -> the first element whose [field] == value.
-- A C export the shipped Modifiable:FindModifier calls (Lua/Modifiers.lua:175); a
-- convention the shipped code depends on to RUN, not something it uses to DECIDE.
table.find_value = function(list, field, value)
	for _, v in ipairs(list or {}) do
		if type(v) == "table" and v[field] == value then return v end
	end
end

-- The engine's type/validity tests. Each fixture declares its own class list and
-- validity, so both branches are reachable (see the note in the docstring).
function IsKindOf(obj, class)
	if type(obj) ~= "table" or type(obj.classes) ~= "table" then return false end
	for _, c in ipairs(obj.classes) do if c == class then return true end end
	return false
end
function IsValid(obj) return type(obj) == "table" and obj.valid ~= false end

-- ⛔ ActiveLaws is a GameVar (Legislature.lua:1). GameVar rawsets the global to
-- **false** at declaration and OnMsg.DoneGame sets it back to false
-- (CommonLua/Core/lib.lua:1061-1093), so "no game loaded" is FALSE, not nil. The
-- harness models false, because modelling nil hid a bug that would have made the
-- module decline on every boot.
ActiveLaws = false
LawDefs = {}

-- Preset:GetParameterValue, retyped (CommonLua/Preset.lua:544) -- the only shipped
-- body in this harness that is not extracted, because it walks a Parameters list the
-- fixtures build by hand. Named here per the deskbench contract.
local function GetParameterValue(self, key)
	for _, p in ipairs(self.Parameters or empty_table) do
		if p.Name == key then return p.Value end
	end
end

function add_law(id, display_name, maintenance_change, handler)
	LawDefs[id] = {
		id = id,
		display_name = display_name,
		Parameters = { { Name = "maintenance_change", Value = maintenance_change } },
		GetParameterValue = GetParameterValue,
		msg_reactions = {
			{ Event = "ConstructionComplete", Handler = handler },
		},
	}
	return LawDefs[id]
end

-- A building carrying the REAL shipped Modifiable:SetModifier (loaded below), so the
-- no-op-on-equal-amounts behaviour in leg (f) is vanilla's, not an assumption.
function building(classes, valid)
	local b = {
		classes = classes or { "Building", "RequiresMaintenance" },
		valid = valid ~= false,
		modifications = false,
		maintenance_resource_amount = 100,
		updates = 0,
		setmodifier_calls = 0,
	}
	-- SetModifier CALLS are counted separately from modifier CHANGES, because a
	-- second call with identical amounts is a no-op inside the shipped body -- so the
	-- end state cannot tell you whether our handler ran. The call count can, and that
	-- is what holds the "this handler only ever acts on prefab buildings" claim.
	b.SetModifier = function(self, ...)
		self.setmodifier_calls = self.setmodifier_calls + 1
		return Modifiable.SetModifier(self, ...)
	end
	b.FindModifier = Modifiable.FindModifier
	function b:UpdateModifier(op, modifier, amount_change, percent_change)
		self.updates = self.updates + 1
		self.modifications = self.modifications or {}
		local list = self.modifications[modifier.prop]
		if not list then list = {} self.modifications[modifier.prop] = list end
		if op == "add" then
			list[#list + 1] = modifier
		elseif op == "remove" then
			for i = #list, 1, -1 do if list[i] == modifier then table.remove(list, i) end end
		end
	end
	return b
end

function mods_of(bld, prop)
	local out = {}
	local list = bld.modifications and bld.modifications[prop]
	for _, m in ipairs(list or empty_table) do
		out[#out + 1] = { id = m.id, percent = m.percent, amount = m.amount }
	end
	return out
end

SMRFixPack = { fixes = {} }
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
	else
		SMRFixPack.fixes[id].status = "inactive"
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
-- SMRFixPack.OnDataReady: fires once the classes are built AND the presets are
-- loaded. Exposed here as FIRE_DATA_READY so the legs can fire it deliberately, the
-- way the engine would at ClassesBuilt / DataLoaded / ModsReloaded / DataChanged.
function SMRFixPack.OnDataReady(fn)
	DATA_READY_FNS = DATA_READY_FNS or {}
	DATA_READY_FNS[#DATA_READY_FNS + 1] = fn
end
function FIRE_DATA_READY()
	for _, fn in ipairs(DATA_READY_FNS or {}) do fn() end
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

-- The game's own dispatch, reduced to what this measures: vanilla's MsgReaction
-- handlers for the active laws, then our additive OnMsg handler.
function construction_complete(bld, dome, from_prefab)
	for _, id in ipairs({ "Policy_BuildingCodesLax", "Policy_BuildingCodesStrict" }) do
		local law = LawDefs[id]
		if law then
			for _, r in ipairs(law.msg_reactions) do
				if r.Event == "ConstructionComplete" then
					r.Handler(law, bld, dome, from_prefab)
				end
			end
		end
	end
	if OnMsg.ConstructionComplete then
		OnMsg.ConstructionComplete(bld, dome, from_prefab)
	end
end
'''


def make_runtime(apply=True, active=("Policy_BuildingCodesStrict",),
                 patched_vanilla=False, at_menu_for_probe=True, tree="1.1.0"):
    """patched_vanilla: drop the `if from_prefab then return end` line from the
    shipped handlers, i.e. simulate Paradox's coming fix."""
    rt = db.lua_runtime()
    rt.execute(PRELUDE)
    # the real shipped Modifiable:SetModifier / FindModifier
    for pat in (r"^function Modifiable:SetModifier", r"^function Modifiable:FindModifier"):
        body, lo, _ = db.body("Lua/Modifiers.lua", pat)
        rt.execute("Modifiable = Modifiable or {}")
        db.load_at(rt, body, "=Lua/Modifiers.lua", lo)
    for law_id in LAWS:
        text, line = law_handler(law_id, tree)
        if patched_vanilla:
            text = text.replace("\t\t\t\tif from_prefab then return end\n", "")
            assert "if from_prefab then return end" not in text
        db.load_at(rt, "HOLDER = {" + text + "\n}", "=" + LAW_FILE, line)
        rt.execute('add_law("%s", "%s", %d, HOLDER.Handler)'
                   % (law_id, law_id, law_param(law_id, tree)))
    # ActiveLaws must be ABSENT while apply() runs (the menu), which is what arms the
    # probe's discriminator; it is then installed for the legs.
    # ⭐ THE COLD-BOOT ORDER, which is what caught the second bug: mod code loads
    # while the preset GlobalMap is still EMPTY, and only then do the presets arrive
    # and OnDataReady fire. `SAVED_LAWDEFS` holds them across the module load.
    rt.execute("SAVED_LAWDEFS = LawDefs LawDefs = {}")
    if not at_menu_for_probe:
        rt.execute("ActiveLaws = {}")      # a game already loaded: probe cannot discriminate
    rt.globals().APPLY_MODULE = apply
    db.load_at(rt, db.read(MODULE), "=Code/Fix_BuildingCodesPrefab.lua", 1)
    rt.execute("LawDefs = SAVED_LAWDEFS")
    rt.eval("FIRE_DATA_READY")()
    rt.eval("FIRE_DATA_READY")()           # idempotent: it may fire several times
    if active:
        rt.execute("ActiveLaws = {}")
        for law_id in active:
            rt.execute('ActiveLaws["%s"] = { id = "%s" }' % (law_id, law_id))
    return rt


def main():
    bench = db.Bench("C88 Building Codes vs prefabs -- shipped LawDef handlers and module")
    check = bench.check

    for law_id in LAWS:
        _, line = law_handler(law_id)
        print("extracted %-42s %-28s Handler at :%d  maintenance_change=%+d"
              % (LAW_FILE, law_id, line, law_param(law_id)))
    print()
    for law_id in LAWS:
        if law_param(law_id) != EXPECTED[law_id]:
            print("NOTE: %s maintenance_change is %+d, the record said %+d"
                  % (law_id, law_param(law_id), EXPECTED[law_id]))
    print()

    rt = make_runtime()
    check("the module applies and the behaviour probe accepts the shipped handlers",
          rt.globals().SMRFixPack["apply_error"] is None,
          rt.globals().SMRFixPack["apply_error"] or "")

    # ---- (a) THE DEFECT REPRODUCED: vanilla alone does nothing for a prefab ---
    vanilla = make_runtime(apply=False)
    vanilla.execute('B = building() construction_complete(B, nil, true)')
    check("(a) THE DEFECT REPRODUCED -- with the law ACTIVE, the shipped handler "
          "applies no maintenance modifier to a prefab building",
          len(dict(vanilla.eval("mods_of(B, 'maintenance_resource_amount')") or {})) == 0)
    vanilla.execute('N = building() construction_complete(N, nil, false)')
    vmods = dict(vanilla.eval("mods_of(N, 'maintenance_resource_amount')") or {})
    check("(a2) ... while the SAME handler does apply it to a normally-built one "
          "(so the fixture is not vacuous)",
          len(vmods) == 1 and dict(vmods[1])["percent"] == -30, [dict(v) for v in vmods.values()])

    # ---- (b) our handler applies the correct modifier to a prefab ------------
    rt.execute('P = building() construction_complete(P, nil, true)')
    pmods = [dict(v) for v in dict(rt.eval("mods_of(P, 'maintenance_resource_amount')") or {}).values()]
    check("(b) the module applies exactly one modifier to a prefab building, under "
          "the LAW'S OWN id, with the shipped -30",
          len(pmods) == 1 and pmods[0]["id"] == "Policy_BuildingCodesStrict"
          and pmods[0]["percent"] == -30, pmods)

    lax = make_runtime(active=("Policy_BuildingCodesLax",))
    lax.execute('P = building() construction_complete(P, nil, true)')
    lmods = [dict(v) for v in dict(lax.eval("mods_of(P, 'maintenance_resource_amount')") or {}).values()]
    check("(b2) Lax too, with its shipped +50 -- both laws, as the owner ruled "
          "(option 1), and neither value hard-coded",
          len(lmods) == 1 and lmods[0]["id"] == "Policy_BuildingCodesLax"
          and lmods[0]["percent"] == 50, lmods)

    # ---- (c) a non-prefab building is vanilla's job, untouched ---------------
    rt.execute('NP = building() construction_complete(NP, nil, false)')
    npmods = [dict(v) for v in dict(rt.eval("mods_of(NP, 'maintenance_resource_amount')") or {}).values()]
    check("(c) a normally-built building gets exactly ONE modifier (vanilla's) -- our "
          "handler adds nothing and cannot double it",
          len(npmods) == 1 and npmods[0]["percent"] == -30, npmods)
    check("(c2) ... and it took exactly one modifier write on that building",
          rt.eval("NP.updates") == 1, rt.eval("NP.updates"))
    check("(c3) ... and SetModifier was CALLED exactly once -- our handler returned at "
          "the prefab gate and never touched a normally-built building. ⚠️ The end "
          "state alone cannot show this: a second call with identical amounts no-ops "
          "inside the shipped body, so the call count is what holds the claim",
          rt.eval("NP.setmodifier_calls") == 1, rt.eval("NP.setmodifier_calls"))

    # ---- (d) no law active: nothing happens ---------------------------------
    off = make_runtime(active=())
    off.execute('P = building() construction_complete(P, nil, true)')
    check("(d) with NO Building Codes law active, a prefab gets no modifier",
          len(dict(off.eval("mods_of(P, 'maintenance_resource_amount')") or {})) == 0)

    # ---- (e) not RequiresMaintenance: nothing happens ------------------------
    rt.execute('NM = building({ "Building" }) construction_complete(NM, nil, true)')
    check("(e) a building that is not RequiresMaintenance gets no modifier",
          len(dict(rt.eval("mods_of(NM, 'maintenance_resource_amount')") or {})) == 0)
    rt.execute('DEAD = building(nil, false) construction_complete(DEAD, nil, true)')
    check("(e2) an invalid building is skipped before anything is read",
          len(dict(rt.eval("mods_of(DEAD, 'maintenance_resource_amount')") or {})) == 0)

    # ---- (f) SIMULATED POST-PATCH VANILLA: exactly one modifier -------------
    # Their fix removes the prefab exit. Our handler and theirs then both write the
    # same id/prop/value, and the SHIPPED SetModifier makes the second a no-op.
    post = make_runtime(patched_vanilla=True, at_menu_for_probe=True)
    check("(f) simulated post-patch vanilla: the module STANDS ITSELF DOWN -- the "
          "discriminator is that ActiveLaws carries no law table with no game loaded, "
          "so their repaired handler throws; no version check anywhere",
          isinstance(post.eval("SMRFixPack.BuildingCodesPrefab.Guard()"), str)
          and post.eval("SMRFixPack.fixes.BuildingCodesPrefab.status") == "inactive",
          post.eval("SMRFixPack.BuildingCodesPrefab.Guard()"))
    check("(f1b) ... and it says RETIRE candidate in the log, for logscan",
          any("RETIRE candidate" in str(v) for v in dict(post.globals().LOG).values()),
          list(dict(post.globals().LOG).values()))
    post.execute('P = building() construction_complete(P, nil, true)')
    fmods = [dict(v) for v in dict(post.eval("mods_of(P, 'maintenance_resource_amount')") or {}).values()]
    check("(f2) ... and a prefab still gets EXACTLY ONE modifier with the right value, "
          "applied by THEIR repaired handler alone",
          len(fmods) == 1 and fmods[0]["id"] == "Policy_BuildingCodesStrict"
          and fmods[0]["percent"] == -30, fmods)
    check("(f3) ... in exactly one modifier write -- no churn",
          post.eval("P.updates") == 1, post.eval("P.updates"))

    # And the belt-and-braces case the owner's id ruling rests on: if BOTH handlers
    # run (our module active AND their patch landed, e.g. a stale probe), the shipped
    # SetModifier coalesces them because the id and the amounts are identical.
    both = make_runtime(patched_vanilla=True)
    both.execute('''
	SMRFixPack.fixes.BuildingCodesPrefab.status = "active"   -- force the handler on
	P = building()
	construction_complete(P, nil, true)
	''')
    bmods = [dict(v) for v in dict(both.eval("mods_of(P, 'maintenance_resource_amount')") or {}).values()]
    check("(f4) ⭐ BOTH handlers running -- theirs and ours -- still yields ONE "
          "modifier and ONE write, because the LAW'S id makes the second call a no-op "
          "in vanilla's own SetModifier (Lua/Modifiers.lua:181-204)",
          len(bmods) == 1 and bmods[0]["percent"] == -30 and both.eval("P.updates") == 1,
          (bmods, both.eval("P.updates")))

    # ---- (g) NEGATIVE: registered but never applied --------------------------
    never = make_runtime(apply=False)
    never.execute('P = building() construction_complete(P, nil, true)')
    check("(g) NEGATIVE -- a module registered but never applied leaves the prefab "
          "with no modifier (the defect stands)",
          len(dict(never.eval("mods_of(P, 'maintenance_resource_amount')") or {})) == 0)

    veto = make_runtime()
    veto.execute('''
	SMRFixPack_Disabled["BuildingCodesPrefab"] = true
	P = building()
	construction_complete(P, nil, true)
	''')
    check("(g2) NEGATIVE -- a mid-session veto stops the handler (FIX_POLICY §2, A1)",
          len(dict(veto.eval("mods_of(P, 'maintenance_resource_amount')") or {})) == 0)

    # ---- (h) the probe must not read a vacuous clean return as permission ----
    vac = make_runtime(patched_vanilla=False, at_menu_for_probe=False, active=())
    check("(h) with a game already loaded the probe CANNOT discriminate, so the module "
          "stays UNDECIDED rather than banking a verdict either way",
          vac.eval("SMRFixPack.BuildingCodesPrefab.Guard()") is None,
          vac.eval("SMRFixPack.BuildingCodesPrefab.Guard()"))
    vac.execute('ActiveLaws = { Policy_BuildingCodesStrict = { id = "Policy_BuildingCodesStrict" } }'
                ' P = building() construction_complete(P, nil, true)')
    check("(h2) ... and while undecided it applies NOTHING -- an undecided guard is not "
          "permission (fail closed)",
          len(dict(vac.eval("mods_of(P, 'maintenance_resource_amount')") or {})) == 0)

    # ---- (h3) the F75 trap: loading before the presets exist ----------------
    # If the guard had run at apply time it would have found an EMPTY LawDefs on every
    # cold boot and declined this module for the whole session. It runs from
    # OnDataReady instead, and make_runtime models that order deliberately.
    check("(h3) the module loaded with an EMPTY LawDefs (the cold-boot order) and was "
          "still armed once the presets arrived -- the F75 trap",
          rt.eval("SMRFixPack.BuildingCodesPrefab.Guard()") is True)

    # ---- (i) the 1.0.7 branch: these laws do not exist ----------------------
    try:
        law_handler(LAWS[0], "1.0.7")
    except (AssertionError, OSError, KeyError) as exc:
        check("(i) the 1.0.7 tree has no Building Codes Lax/Strict handler at all, so "
              "there is nothing for this module to find (1.0.7 had only the old "
              "cost-only law, now Obsolete)", True, str(exc)[:90])
    else:
        check("(i) the 1.0.7 tree unexpectedly carries these handlers -- re-read C88 "
              "before trusting the branch claim", False)

    return bench.finish(
        "ALL DEMANDS HELD -- the shipped handler applies nothing to a prefab while "
        "applying -30 to the same building built normally; the module supplies it for "
        "both laws at their shipped values, under the law's own id, and adds nothing "
        "to a normal build, an inactive law, a non-maintenance building or an invalid "
        "one; and once vanilla's exit is gone the module declines while a prefab still "
        "ends up with exactly one modifier."
    )


if __name__ == "__main__":
    sys.exit(main())
