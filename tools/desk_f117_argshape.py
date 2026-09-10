#!/usr/bin/env python3
"""F117 desk falsifier -- does the module's argument-shape probe actually discriminate?

Written 2026-09-09 by hotfix2 link 99a (session scratchpad); promoted to tools/
the same day on the owner's ruling (checklist 131) with only its paths moved
into deskbench. The demands below are verbatim.

Runs OUR probe, extracted verbatim from Code/Fix_ArrivalDeaths.lua between the
F117-PROBE-BEGIN/END markers, against the SHIPPED `Community:GetScoreFor` body,
extracted verbatim from each game tree with the project's own body delimiter
(tools/luafn.find_bodies -- the same one bodycheck.py hashes with). Nothing here
is retyped: if the shipped body or our probe changes, this re-extracts it.

Four demands, and the run FAILS unless all four hold:

  A. the probe answers "colonist" on the 1.1.0 body               (leg FIRES)
  B. the probe answers "traits"   on the 1.0.7 body               (leg does NOT fire)
  C. the DEFECT is real: ChooseDome(traits_table, ...) THROWS on the 1.1.0 body
     and ChooseDome(colonist, ...) does not
  D. the OTHER-DIRECTION defect ck118 forbids is real: ChooseDome(colonist, ...)
     on the 1.0.7 body does not throw but MIS-SCORES -- so "pass self on both
     branches" really would have been silently wrong

  E. (control on the falsifier itself) a deliberately-broken body that indexes
     NEITHER table must be answered UNKNOWN, not guessed; so must one that
     indexes BOTH.

Usage: python tools/desk_f117_argshape.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import deskbench as db  # noqa: E402

MODULE = os.path.join(db.REPO, "Code", "Fix_ArrivalDeaths.lua")


def body(tree, rel, pattern):
    """The shipped body, verbatim, by the project's own delimiter."""
    return db.body(rel, pattern, tree)[0]


def probe_source():
    """Our probe, verbatim, from the shipped module -- markers only, no retyping."""
    src = db.marker_span(MODULE, "F117-PROBE-BEGIN", "F117-PROBE-END")
    assert "choose_dome_arg" in src and "discriminate" in src, "marker span is empty/wrong"
    return src


# --- the minimum environment the two shipped bodies name, and nothing more ----
PRELUDE = """
Community = {}
Max = function(a, b) if a > b then return a end return b end
const = { Scale = { Stat = 100 } }
-- 1.1.0 reads these; the 1.0.7 body uses literals instead. Real DefineConstInt
-- defaults, Lua/Buildings/Community.lua:436-440.
g_Consts = {
  CommunityEvalLifeSupport = 100,
  CommunityEvalNoLifeSupport = -400,
  CommunityEvalNone = -700,
}
ValidateBuilding = function(o) return o end
IsValid = function(o) return o and true or false end
GetResidenceComfort = function() return 0 end
"""

# `SMRFixPack.Require`'s probe form, reproduced here ONLY so the extracted probe
# can run outside the game: pcall trap + strict-true, its two load-bearing
# properties (00_Core.lua:117-140). Everything else about it is irrelevant here.
SHIM = """
SMRFixPack = {
  Log = function(fmt, ...) LOGGED[#LOGGED + 1] = string.format(fmt, ...) end,
  Require = function(id, spec)
    for _, c in ipairs(spec) do
      local pok, res = pcall(c.probe)
      if not (pok and res == true) then
        return c.reason or "declined"
      end
    end
  end,
}
LOGGED = {}
"""


def make_runtime(getscorefor_body, traitfilter_body, filter_body):
    L = db.lua_runtime(unpack_returned_tuples=False)
    L.execute(PRELUDE)
    L.execute(SHIM)
    L.execute(filter_body)        # FilterObjectAttributes  (Lua/Filter.lua)
    L.execute(traitfilter_body)   # TraitFilterColonist     (Lua/Traits.lua)
    L.execute(getscorefor_body)   # Community:GetScoreFor   (Lua/Buildings/Community.lua)
    return L


def run_probe(L):
    """Execute the extracted probe and return its verdict + the log lines."""
    L.execute("do\n" + probe_source() + "\nRESULT = choose_dome_arg(PROBE_COLONIST)\nSHAPE = arg_shape\nend")
    return L.eval("SHAPE"), list(L.eval("LOGGED").values())


def main():
    bench = db.Bench("F117 desk falsifier -- shipped bodies verbatim, our probe verbatim, real Lua")
    check = bench.check

    # ------------------------------------------------------------ A and B ----
    for tree, expected in (("1.1.0", "colonist"), ("1.0.7", "traits")):
        gsf = body(tree, "Lua/Buildings/Community.lua", r"^function Community:GetScoreFor")
        tfc = body(tree, "Lua/Traits.lua", r"^function TraitFilterColonist")
        foa = body(tree, "Lua/Filter.lua", r"^function FilterObjectAttributes")
        print(f"[{tree}] Community:GetScoreFor extracted, {len(gsf.splitlines())} lines; "
              f"first line: {gsf.splitlines()[0].strip()}")
        L = make_runtime(gsf, tfc, foa)
        # a colonist-shaped object, for the probe's own return value
        L.execute("PROBE_COLONIST = { traits = { Nerd = true } }")
        shape, logged = run_probe(L)
        check(f"[{tree}] probe answers {expected!r}", shape == expected, f"got {shape!r}")
        check(f"[{tree}] no decline logged", not logged, repr(logged))

    print()

    # --------------------------------------------------------------- C -------
    # The defect itself, on the 1.1.0 body, through the SHIPPED ChooseDome.
    gsf = body("1.1.0", "Lua/Buildings/Community.lua", r"^function Community:GetScoreFor")
    L = make_runtime(gsf,
                     body("1.1.0", "Lua/Traits.lua", r"^function TraitFilterColonist"),
                     body("1.1.0", "Lua/Filter.lua", r"^function FilterObjectAttributes"))
    L.execute(body("1.1.0", "Lua/_GameUtils.lua", r"^function ChooseDome"))
    L.execute("""
-- one candidate dome with a trait filter and no residences: the cheapest colony
-- shape that reaches the differing line
DOME = setmetatable({
  traits_filter = { Nerd = 10 },
  labels = { Residence = {} },
  free_spaces = { traits = {} },
  overpopulated = false,
}, { __index = Community })
DOME.HasLifeSupport = function() return true end
DOME.HasFreeLivingSpaceFor = function() return true end
COLONIST = { traits = { Nerd = true } }
TRAITS = COLONIST.traits
ok_traits, err_traits = pcall(ChooseDome, TRAITS, { DOME }, false, nil)
ok_col, err_col = pcall(ChooseDome, COLONIST, { DOME }, false, nil)
""")
    check("[1.1.0] the OLD call ChooseDome(self.traits, ...) THROWS",
          L.eval("ok_traits") is False, str(L.eval("err_traits")))
    check("[1.1.0] the NEW call ChooseDome(colonist, ...) does not throw",
          L.eval("ok_col") is True, str(L.eval("err_col")))

    # --------------------------------------------------------------- D -------
    # ck118's forbidden shortcut, on the 1.0.7 body: no throw, silent mis-score.
    gsf7 = body("1.0.7", "Lua/Buildings/Community.lua", r"^function Community:GetScoreFor")
    L7 = make_runtime(gsf7,
                      body("1.0.7", "Lua/Traits.lua", r"^function TraitFilterColonist"),
                      body("1.0.7", "Lua/Filter.lua", r"^function FilterObjectAttributes"))
    L7.execute("""
DOME = setmetatable({
  traits_filter = { Nerd = 10 },
  labels = { Residence = {} },
  free_spaces = { traits = {} },
  overpopulated = false,
}, { __index = Community })
DOME.HasLifeSupport = function() return true end
COLONIST = { traits = { Nerd = true } }
score_right = DOME:GetScoreFor(COLONIST.traits)
ok_wrong, score_wrong = pcall(DOME.GetScoreFor, DOME, COLONIST)
""")
    sr, okw, sw = L7.eval("score_right"), L7.eval("ok_wrong"), L7.eval("score_wrong")
    check("[1.0.7] passing the COLONIST does not throw (so no instrument would see it)",
          okw is True, str(sw))
    check("[1.0.7] ... but MIS-SCORES: correct=%s, with-colonist=%s" % (sr, sw),
          okw is True and sr != sw,
          "ck118's 'pass self on both branches' really is silently wrong")

    # --------------------------------------------------------------- E -------
    # Control on the falsifier: a body that indexes NEITHER table must be UNKNOWN.
    print()
    LE = make_runtime(
        "function Community:GetScoreFor(x)\n\treturn 42\nend",
        body("1.1.0", "Lua/Traits.lua", r"^function TraitFilterColonist"),
        body("1.1.0", "Lua/Filter.lua", r"^function FilterObjectAttributes"))
    LE.execute("PROBE_COLONIST = { traits = { Nerd = true } }")
    shape_e, logged_e = run_probe(LE)
    check("[control] a body that indexes neither table is answered UNKNOWN, not guessed",
          shape_e is False, "shape=%r" % (shape_e,))
    check("[control] ... and the decline is NAMED in the log",
          len(logged_e) == 1 and "stands down" in logged_e[0],
          repr(logged_e))

    # A second control: a body that indexes BOTH must also be UNKNOWN.
    LB = make_runtime(
        "function Community:GetScoreFor(x)\n"
        "\treturn TraitFilterColonist(self.traits_filter, x)\n"
        "\t\t+ TraitFilterColonist(self.traits_filter, x.traits or {})\n"
        "end",
        body("1.1.0", "Lua/Traits.lua", r"^function TraitFilterColonist"),
        body("1.1.0", "Lua/Filter.lua", r"^function FilterObjectAttributes"))
    LB.execute("PROBE_COLONIST = { traits = { Nerd = true } }")
    shape_b, _ = run_probe(LB)
    check("[control] a body that indexes BOTH tables is answered UNKNOWN too",
          shape_b is False, "shape=%r" % (shape_b,))

    return bench.finish("ALL DEMANDS HELD -- the probe fires on 1.1.0, does not fire on 1.0.7,\n"
                        "both defects it guards against are real, and UNKNOWN is not guessed.")


if __name__ == "__main__":
    sys.exit(main())
