#!/usr/bin/env python3
"""Does the KIT probe for F117 actually discriminate, on both branches?

Written 2026-09-09 by hotfix2 link 99a (session scratchpad); promoted to tools/
the same day on the owner's ruling (checklist 131) with only its paths moved
into deskbench. The demands below are verbatim.

Same method as desk_f117_argshape.py: shipped bodies extracted verbatim from
each game tree, the module's published discriminator extracted verbatim from
the module, and the kit probe's own registration extracted verbatim from
20_Probes_Wave2.lua. Nothing retyped.

Demands:
  A. 1.1.0 tree -> PASS, and its message names the still-throwing old call
  B. 1.0.7 tree -> PASS, and its message names the mis-score
  C. a module that publishes no ReadArgShape  -> FAIL (not a quiet PASS)
  D. an UNKNOWN verdict                       -> FAIL (not a quiet PASS)
  E. a stub that stopped discriminating       -> SKIP (not a PASS)

Usage: python tools/desk_f117_kitprobe.py   (needs the local Test Kit, SMR_TESTKIT)
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import deskbench as db  # noqa: E402

MODULE = os.path.join(db.REPO, "Code", "Fix_ArrivalDeaths.lua")
KITFILE = os.path.join(db.TESTKIT, "Code", "20_Probes_Wave2.lua")
PROBE_ID = "ArrivalDeathsChooseDomeArg"


def body(tree, rel, pattern):
    return db.body(rel, pattern, tree)[0]


def module_probe_src():
    return db.marker_span(MODULE, "F117-PROBE-BEGIN", "F117-PROBE-END")


def kit_probe_src():
    """The Register(...) call verbatim: from its first line to the `})` at col 0."""
    lines = db.read_lines(KITFILE)
    start = [i for i, l in enumerate(lines) if l.startswith(f'SMRTest.Register("{PROBE_ID}"')][0]
    end = next(i for i in range(start + 1, len(lines)) if lines[i] == "})")
    return "\n".join(lines[start:end + 1])


PRELUDE = """
Max = function(a, b) if a > b then return a end return b end
const = { Scale = { Stat = 100 } }
g_Consts = {
  CommunityEvalLifeSupport = 100, CommunityEvalNoLifeSupport = -400,
  CommunityEvalNone = -700, CommunityEvalOverpopulated = -200,
}
IsValid = function(o) return false end            -- a plain table is not a CObject
ValidateBuilding = function(o) return false end   -- ... so the shipped guard rejects it
GetResidenceComfort = function() return 0 end
Community = {}; Community.__index = Community
Residence = {}; Residence.__index = Residence
SMRFixPack = {
  fixes = { ArrivalDeaths = { status = "active", detail = "" } },
  Log = function() end,
  Require = function(id, spec)
    for _, c in ipairs(spec) do
      local pok, res = pcall(c.probe)
      if not (pok and res == true) then return c.reason or "declined" end
    end
  end,
}
SMRTest = {
  registered = {},
  Register = function(id, def) SMRTest.registered[id] = def end,
  FixMissing = function(fix_id)
    if not rawget(_G, "SMRFixPack") then return "FAIL", "fix pack not loaded (bug reproduces)" end
    local f = SMRFixPack.fixes[fix_id]
    if not f then return "FAIL", "fix '" .. fix_id .. "' not registered" end
    if f.status ~= "active" then return "FAIL", "fix is " .. f.status end
  end,
}
"""


def build(tree, install_module=True, break_shape=None, break_stub=False):
    L = db.lua_runtime(unpack_returned_tuples=False)
    L.execute(PRELUDE)
    L.execute(body(tree, "Lua/Filter.lua", r"^function FilterObjectAttributes"))
    L.execute(body(tree, "Lua/Traits.lua", r"^function TraitFilterColonist"))
    L.execute(body(tree, "Lua/Buildings/Community.lua", r"^function Community:GetScoreFor"))
    L.execute(body(tree, "Lua/Buildings/Community.lua", r"^function Community:HasFreeLivingSpaceFor"))
    L.execute(body(tree, "Lua/Buildings/Residence.lua", r"^function Residence:IsSuitable"))
    L.execute(body(tree, "Lua/_GameUtils.lua", r"^function ChooseDome"))
    # the shipped predicate table (Stats.lua on 1.1.0, Stats.lua on 1.0.7 too)
    L.execute("ColonistFilterFunc = { Children = function(traits) return traits.Child end }")
    if install_module:
        L.execute("do\n" + module_probe_src() + "\nend")
    if break_shape is not None:
        L.execute("SMRFixPack.ArrivalDeaths = { ReadArgShape = function() return %s end }" % break_shape)
    if break_stub:
        # the failure this probe exists to refuse: a body that no longer reaches
        # the differing line, so BOTH arguments behave identically
        L.execute("function Community:GetScoreFor(x) return 7 end")
    L.execute(kit_probe_src())
    return L


def run(L):
    L.execute('VERDICT, WHY = SMRTest.registered["%s"].run()' % PROBE_ID)
    return L.eval("VERDICT"), L.eval("WHY")


def main():
    bench = db.Bench("F117 KIT PROBE falsifier -- shipped bodies + module + kit probe, all verbatim")
    check = bench.check

    for tree, expect_in_msg in (("1.1.0", "throws"), ("1.0.7", "mis-score")):
        v, w = run(build(tree))
        check(f"[{tree}] the kit probe PASSes", v == "PASS", f"{v}: {w}")
        check(f"[{tree}] ... and its message says why it is not vacuous", expect_in_msg in (w or ""), str(w))

    print()
    v, w = run(build("1.1.0", install_module=False))
    check("[C] no published ReadArgShape -> FAIL, not a quiet PASS", v == "FAIL", f"{v}: {w}")

    v, w = run(build("1.1.0", break_shape="nil"))
    check("[D] an UNKNOWN verdict -> FAIL, not a quiet PASS", v == "FAIL", f"{v}: {w}")

    v, w = run(build("1.1.0", break_shape='"colonist"', break_stub=True))
    check("[E] a stub that stopped discriminating -> SKIP, not a PASS", v == "SKIP", f"{v}: {w}")

    return bench.finish("ALL DEMANDS HELD -- the kit probe passes on both branches for the right\n"
                        "reason, and refuses to pass when it cannot tell the arguments apart.")


if __name__ == "__main__":
    sys.exit(main())
