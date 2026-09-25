#!/usr/bin/env python3
"""C42 passage-element stale-holder teardown over archived 1.1.1.405907 Lua.

Run: python tools/desk_c42_passage_stale.py

Loads the shipped Holder:KickUnitsFromHolder body and the whole C42 module under
a real Lua interpreter. The control omits the module and requires a stale member
to be kicked; the repaired leg requires that same member to survive while a
genuine occupant is still kicked. A second control checks invalid-member assert
avoidance, foreign-holder behavior, shape decline, and chained return forwarding.

IsValid, IsKindOf, CurrentThread and KickFromBuilding are narrow engine seams.
KickFromBuilding's effects are recorded because this test is about whether it
is called, not the movement it performs. It cannot reject or validate a call in
the shipped Holder body. No game, save, or traversal thread is exercised.
"""
import os
from pathlib import Path

import deskbench as db

BUILD = "1.1.1.405907"
db.TREES[BUILD] = os.path.join(os.environ.get(
    "SMR_SRCARCHIVE", r"B:\Dev\SMR\SMR-Shared\SMR-SrcArchive"), BUILD, "Src")
MODULE = Path(db.REPO) / "Code" / "Fix_PassageStaleHolder.lua"

PRELUDE = r'''
Holder = {}
PassageGridElement = {Done = function() end}
PassageBase = {TraverseTunnel = function() end}
function IsKindOf(obj, class) return obj.kind == class end
function IsValid(obj) return type(obj) == "table" and obj.valid == true end
function CurrentThread() return "teardown" end
function unit(holder, valid)
  return {holder = holder, valid = valid, command_thread = "other",
    kicks = 0, KickFromBuilding = function(self, building)
      self.kicks = self.kicks + 1; self.last_kick = building
    end}
end
SMRFixPack = {result = nil}
function SMRFixPack.Register(id, spec)
  SMRFixPack.id = id
  SMRFixPack.result = spec.apply()
end
function SMRFixPack.Require(_, specs)
  for _, item in ipairs(specs) do
    if item.class then
      local cls = _G[item.class]
      if type(cls) ~= "table" or type(cls[item.method]) ~= "function" then
        return item.class .. "." .. item.method .. " missing"
      end
    elseif item.global and type(_G[item.global]) ~= "function" then
      return item.global .. " missing"
    end
  end
end
'''


def runtime(patched=True, missing_traverse=False, chained=False):
    rt = db.lua_runtime()
    rt.execute(PRELUDE)
    shipped, lo, hi = db.body("Lua/Buildings/Holder.lua",
        r"^function Holder:KickUnitsFromHolder\(", tree=BUILD)
    db.load_at(rt, shipped, "=Lua/Buildings/Holder.lua", lo)
    if missing_traverse:
        rt.execute("PassageBase.TraverseTunnel = nil")
    if chained:
        rt.execute('''
          local prior = Holder.KickUnitsFromHolder
          function Holder:KickUnitsFromHolder(...)
            prior(self, ...)
            return "first", nil, "third"
          end
        ''')
    if patched:
        db.load_at(rt, MODULE.read_text(encoding="utf-8"),
                   "=Code/Fix_PassageStaleHolder.lua", 1)
    return rt, lo, hi


def main():
    bench = db.Bench("C42 stale passage occupants at element teardown")
    check = bench.check
    bare, lo, hi = runtime(False)
    print(f"extracted Lua/Buildings/Holder.lua:{lo}-{hi}")
    bare.execute('''
      el = setmetatable({kind="PassageGridElement"}, {__index=Holder})
      stale = unit(false, true); genuine = unit(el, true)
      el.units = {stale, genuine}; el:KickUnitsFromHolder()
    ''')
    check("control: without the fix, the stale member is kicked",
          bare.globals().stale.kicks == 1)
    check("control: vanilla also kicks a genuine member",
          bare.globals().genuine.kicks == 1)

    rt, _, _ = runtime()
    rt.execute('''
      el = setmetatable({kind="PassageGridElement"}, {__index=Holder})
      stale = unit(false, true); genuine = unit(el, true)
      el.units = {stale, genuine}; el:KickUnitsFromHolder()
    ''')
    g = rt.globals()
    check("module applied through Register and Require", g.SMRFixPack.result is None)
    check("stale member is not kicked", g.stale.kicks == 0)
    check("genuine member still reaches shipped kick", g.genuine.kicks == 1)
    check("vanilla clears the element list", g.el.units is None)

    invalid, _, _ = runtime()
    invalid.execute('''
      el = setmetatable({kind="PassageGridElement"}, {__index=Holder})
      bad = unit(false, false); el.units = {bad}; el:KickUnitsFromHolder()
    ''')
    check("invalid member is removed before shipped assertion", invalid.globals().bad.kicks == 0)

    foreign, _, _ = runtime()
    foreign.execute('''
      other = setmetatable({kind="OtherHolder"}, {__index=Holder})
      stale = unit(false, true); other.units = {stale}; other:KickUnitsFromHolder()
    ''')
    check("foreign holder goes unchanged to shipped method", foreign.globals().stale.kicks == 1)

    drift, _, _ = runtime(missing_traverse=True)
    check("missing traversal shape declines before installing wrapper",
          "PassageBase.TraverseTunnel" in str(drift.globals().SMRFixPack.result))

    chain, _, _ = runtime(chained=True)
    chain.execute('''
      el = setmetatable({kind="PassageGridElement", units={}}, {__index=Holder})
      r1, r2, r3 = el:KickUnitsFromHolder("arg")
      other = setmetatable({kind="OtherHolder", units={}}, {__index=Holder})
      f1, f2, f3 = other:KickUnitsFromHolder("arg")
    ''')
    cg = chain.globals()
    check("all chained returns, including a nil middle, pass through on passage",
          cg.r1 == "first" and cg.r2 is None and cg.r3 == "third")
    check("all chained returns pass through on foreign holder",
          cg.f1 == "first" and cg.f2 is None and cg.f3 == "third")
    return bench.finish()


if __name__ == "__main__":
    raise SystemExit(main())
