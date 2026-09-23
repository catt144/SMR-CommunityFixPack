#!/usr/bin/env python3
"""C93 desk controls for the production Outside Ranch module.

The actual module is loaded unchanged. Engine entities, objects and messages are
minimal fixtures; this proves wrapper routing, object-preserving migration,
idempotency, veto handling and self-deactivation, not game pathfinding or art.
"""
import subprocess
import sys
from pathlib import Path

import deskbench as db


HISTORICAL_REV = "16ff1aa"
MODULE_REL = "Code/Fix_OpenPastureStockpiles.lua"


PRELUDE = db.ENGINE_SHIMS + r'''
empty_table = {}
SMRFixPack_Disabled = {}
LOGS = {}
local handlers = {}
OnMsg = setmetatable({}, {__newindex = function(_, event, fn)
  handlers[event] = handlers[event] or {}
  table.insert(handlers[event], fn)
end})
function Msg(event, ...)
  for _, fn in ipairs(handlers[event] or empty_table) do fn(...) end
end

SMRFixPack = {fixes = {}}
function SMRFixPack.Log(fmt, ...)
  LOGS[#LOGS + 1] = string.format(fmt, ...)
end
function SMRFixPack.WhenActive(id, fn)
  return function(...)
    local entry = SMRFixPack.fixes[id]
    if not (entry and entry.status == "active") then return end
    if SMRFixPack_Disabled[id] then return end
    return fn(...)
  end
end
function SMRFixPack.Require(_, requirements)
  for _, req in ipairs(requirements) do
    if req.probe and req.probe() ~= true then return req.reason end
  end
end
function SMRFixPack.Register(id, def)
  local entry = {status = SMRFixPack_Disabled[id] and "disabled" or "pending"}
  SMRFixPack.fixes[id] = entry
  if entry.status == "disabled" then return end
  local result = def.apply()
  entry.status = type(result) == "string" and "inactive" or "active"
  entry.detail = type(result) == "string" and result or ""
end

OpenPastureBase = {stockpile_spots1 = {}}
for i = 1, 9 do OpenPastureBase.stockpile_spots1[i] = "Resourcepile" .. i end
OpenAirBuilding = {}
function OpenAirBuilding:CalcOpenAirEntity(entity)
  entity = entity or self.entity
  local closed = string.match(entity, "^(.*)_Open$")
  if closed then return entity, closed end
  return entity .. "_Open", entity
end
function IsKindOf(obj, class) return obj.kind == class end
function IsValid(obj) return obj.valid ~= false end

OPEN_HAS_EXTRA = false
local function spot_number(name)
  return tonumber(string.match(name, "Resourcepile(%d+)$"))
end
function GetSpotRange(entity, _, name)
  local number = spot_number(name)
  if not number then return -1, -1 end
  if entity == "OpenPasture" then return 100 + number, 100 + number end
  if entity == "OpenPasture_Open" and (number <= 6 or OPEN_HAS_EXTRA) then
    return 100 + number, 100 + number
  end
  return -1, -1
end

RANCHES = {}
function AllMapsForEach(_, class, fn)
  assert(class == "OpenPastureBase")
  for _, ranch in ipairs(RANCHES) do fn(ranch) end
end

function MakePile(spot, amount)
  local pile = {valid = true, spot = spot, stored = amount, offset = 99}
  function pile:GetParent() return self.parent end
  function pile:GetAttachSpot() return self.spot end
  function pile:Detach()
    self.parent = nil
    self.spot = -1
    self.detaches = (self.detaches or 0) + 1
  end
  function pile:SetAttachOffset(x, y, z) self.offset = x + y + z end
  return pile
end
function MakeRanch()
  local ranch = {kind = "OpenPastureBase", entity = "OpenPasture_Open", open_air = true}
  local piles = {}
  for i = 1, 9 do
    piles[i] = MakePile(i <= 6 and 100 + i or -1, i * 1000)
    piles[i].parent = ranch
  end
  ranch.producers = {{stockpiles = piles}, {stockpiles = piles}, {stockpiles = piles}}
  function ranch:GetEntity() return self.entity end
  function ranch:GetCurrentSkin() return self.entity, "palette" end
  function ranch:ChangeSkin(entity, palette)
    assert(palette == "palette")
    self.entity = entity
    self.skin_changes = (self.skin_changes or 0) + 1
  end
  function ranch:GetSpotRange(state, name) return GetSpotRange(self.entity, state, name) end
  function ranch:Attach(pile, spot)
    pile.parent = self
    pile.spot = spot
  end
  ranch.piles = piles
  return ranch
end
'''


def runtime(open_has_extra=False, veto=False):
    rt = db.lua_runtime()
    rt.execute(PRELUDE)
    rt.globals().OPEN_HAS_EXTRA = open_has_extra
    if veto:
        rt.execute('SMRFixPack_Disabled.OpenPastureStockpiles = true')
    db.load_at(rt, db.git_show(db.REPO, HISTORICAL_REV, MODULE_REL),
               "=%s:%s" % (HISTORICAL_REV, MODULE_REL))
    return rt


def main():
    print("COMMAND python tools/desk_c93_open_pasture.py")
    print("HISTORICAL MODULE " + HISTORICAL_REV + ":" + MODULE_REL)
    bench = db.Bench("C93 historical module desk controls; engine objects are fixtures")

    rt = runtime()
    check = bench.check
    check("exact entity mismatch activates the module",
          rt.eval('SMRFixPack.fixes.OpenPastureStockpiles.status == "active"'))
    check("foreign OpenAirBuilding receivers delegate byte-for-byte",
          rt.eval('''
            (function()
              local o, c = OpenAirBuilding.CalcOpenAirEntity({kind="Dome", entity="DomeBasic"})
              return o == "DomeBasic_Open" and c == "DomeBasic"
            end)()
          '''))
    check("Outside Ranch callers resolve the nine-anchor entity in both positions",
          rt.eval('''
            (function()
              local o, c = OpenAirBuilding.CalcOpenAirEntity({kind="OpenPastureBase", entity="OpenPasture_Open"})
              return o == "OpenPasture" and c == "OpenPasture"
            end)()
          '''))

    rt.execute('''
      ranch = MakeRanch()
      RANCHES = {ranch}
      before = 0
      identities = {}
      for i, pile in ipairs(ranch.piles) do before = before + pile.stored; identities[i] = pile end
      Msg("LoadGame")
      after = 0
    anchors_ok = true
    identities_ok = true
    detaches_ok = true
    for i, pile in ipairs(ranch.piles) do
      after = after + pile.stored
      anchors_ok = anchors_ok and pile.spot == 100 + i
      identities_ok = identities_ok and pile == identities[i]
      detaches_ok = detaches_ok and (pile.detaches or 0) == (i >= 7 and 1 or 0)
    end
    ''')
    check("affected load restores the closed ranch entity",
          rt.eval('ranch.entity == "OpenPasture" and ranch.skin_changes == 1'))
    check("migration preserves every pile object and every stored amount",
          rt.eval('identities_ok and before == after and after == 45000'))
    check("invalid piles are reattached to Resourcepile7..9 with zero offsets",
          rt.eval('anchors_ok and detaches_ok and ranch.piles[7].offset == 0 and ranch.piles[8].offset == 0 and ranch.piles[9].offset == 0'))
    rt.execute('Msg("LoadGame")')
    check("second load pass is idempotent",
          rt.eval('ranch.skin_changes == 1 and before == after and anchors_ok'))

    fixed = runtime(open_has_extra=True)
    check("vendor-corrected open entity makes the module decline",
          fixed.eval('SMRFixPack.fixes.OpenPastureStockpiles.status == "inactive"'))
    check("declined module leaves the vanilla entity selector intact",
          fixed.eval('''
            (function()
              local o, c = OpenAirBuilding.CalcOpenAirEntity({kind="OpenPastureBase", entity="OpenPasture"})
              return o == "OpenPasture_Open" and c == "OpenPasture"
            end)()
          '''))

    vetoed = runtime(veto=True)
    vetoed.execute('ranch = MakeRanch(); RANCHES = {ranch}; Msg("LoadGame")')
    check("explicit veto installs no wrapper and performs no migration",
          vetoed.eval('''
            SMRFixPack.fixes.OpenPastureStockpiles.status == "disabled"
            and ranch.entity == "OpenPasture_Open" and ranch.skin_changes == nil
          '''))

    return bench.finish(
        "DESK CONTROLS HOLD; game entity mutation, visuals and drone pathfinding remain for checklist 191.")


if __name__ == "__main__":
    sys.exit(main())
