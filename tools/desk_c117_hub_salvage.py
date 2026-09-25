#!/usr/bin/env python3
"""C117 hub-passage salvage drain against archived 1.1.1.405907 Lua.

Run: python tools/desk_c117_hub_salvage.py

The harness loads the native demolition, drain predicate, passage traversal,
disconnect/PF-removal, cancellation, and Unit:TraverseTunnel bodies verbatim.
Its only retyped pieces are a synchronous scheduler plus movement/PF seams that
let one native traversal stay in flight while native OnDemolish runs.

It proves the module's decision logic: an in-flight colonist reaches the hub
before the busy spoke disconnects, a new entrant is refused only when a usable
sibling remains, and Unit:TraverseTunnel clears that entrant's path.  The
fixture deliberately does not inspect element holder lists or teardown; C42
owns that separate consequence.  It also does not claim a real game's reroute
or timing, save serialisation, or player reachability.
"""
import os
from pathlib import Path

import deskbench as db


BUILD = "1.1.1.405907"
db.TREES[BUILD] = os.path.join(
    os.environ.get("SMR_SRCARCHIVE", r"B:\Dev\SMR\SMR-Shared\SMR-SrcArchive"),
    BUILD,
    "Src",
)
MODULE = Path(db.REPO) / "Code" / "Fix_PassageHubSalvageDrain.lua"

# Every game decision exercised below comes from one of these bodies.  The
# fixture keeps `WaitWakeup` synchronous and pauses the unit just before its
# destructor, which is enough to model the only interleaving C117 needs.
BODIES = (
    ("Lua/Passage.lua", r"^function PassageBase:GetConnectedHub\("),
    ("Lua/Passage.lua", r"^function PassageBase:IsPFTunnelActive\("),
    ("Lua/Passage.lua", r"^function PassageBase:WouldStrandHubColonists\("),
    ("Lua/Passage.lua", r"^function PassageBase:ClearHubDraining\("),
    ("Lua/Passage.lua", r"^function PassageBase:OnSetDemolishing\("),
    ("Lua/Passage.lua", r"^function PassageBase:WakeUpDemolishThread\("),
    ("Lua/Passage.lua", r"^function PassageBase:OnDemolish\("),
    ("Lua/Passage.lua", r"^function PassageBase:TraverseTunnel\("),
    ("Lua/Passage.lua", r"^function PassageBase:DisconnectDomes\("),
    ("Lua/Passage.lua", r"^function PassageBase:DisconnectDomeFromHub\("),
    ("Lua/Passage.lua", r"^function PassageBase:RemovePFTunnel\("),
    ("Lua/Passage.lua", r"^function PassageGridElement:RemovePFTunnel\("),
    ("Lua/Units/Unit.lua", r"^function Unit:TraverseTunnel\("),
)


PRELUDE = r'''
PassageBase = {hub_draining = false, traversing_colonists = false}
PassageGridElement = {}
Unit = {}
empty_table = {}
WAIT_CALLS, WAKEUPS, PF_ADVANCES, PF_REMOVES = 0, 0, 0, 0

function IsKindOf(obj, class)
  return type(obj) == "table" and (obj.kind == class or (obj.parents and obj.parents[class]))
end
function IsValid(obj) return type(obj) == "table" and obj.valid == true end
function IsValidThread() return false end
function DeleteThread() error("fixture has no PF thread to delete") end
function ret_false() return false end
function Wakeup() WAKEUPS = WAKEUPS + 1 end
function WaitWakeup(ms)
  assert(ms == 1000, "native demolition waits one second")
  WAIT_CALLS = WAIT_CALLS + 1
  local f = ON_WAIT
  ON_WAIT = false
  if f then f() end
end
function ResolveMap(map) return map end
function GetPassageAttachedBuilding(el) return el.owner end

table.remove_entry = function(t, value)
  for i = #t, 1, -1 do if t[i] == value then table.remove(t, i) end end
end
table.remove_value = function(t, value)
  for i = #t, 1, -1 do if t[i] == value then table.remove(t, i) end end
end

pf = {}
function pf.GetTunnelEntrance() return false end
function pf.GetTunnelExit() return false end
function pf.RemoveTunnel() PF_REMOVES = PF_REMOVES + 1 end
function pf.GetPathTunnel(unit)
  return unit.pf_tunnel, unit.pf_param, unit.pf_end_point, unit.pf_end_point_map
end
function pf.AdvancePathTunnel(unit) PF_ADVANCES = PF_ADVANCES + 1; unit.advanced = true end

function Unit:PushDestructor(fn) self.destructor = fn end
function Unit:PopAndCallDestructor()
  local fn = self.destructor
  self.destructor = false
  if self.defer then self.pending_destructor = fn; return end
  if fn then fn(self) end
end
function Unit:FinishTraversal()
  local fn = self.pending_destructor
  self.pending_destructor = false
  assert(fn, "fixture expected a native traversal destructor")
  fn(self)
end
function Unit:GetMoveSpeed() return 10 end
function Unit:SetMoveSpeed(speed) self.move_speed = speed end
function Unit:GetMoveAnim() return "walk" end
function Unit:SetState(state) self.state = state end
function Unit:SetHolder(holder) self.holder = holder end
function Unit:UpdateOutside() self.outside_updates = self.outside_updates + 1 end
function Unit:ClearPath() self.clear_paths = self.clear_paths + 1 end

function make_unit(name, defer)
  return setmetatable({kind = "Colonist", valid = true, name = name, defer = defer,
    holder = false, passage_hub = false, outside_updates = 0, clear_paths = 0}, {__index = Unit})
end

function PassageBase:TryConnectDomes() self.reconnects = self.reconnects + 1 end
function PassageBase:DestroyAttaches() self.destroyed_attaches = self.destroyed_attaches + 1 end
function PassageBase:GetEndElement() return self.elements[#self.elements] end

function make_case(with_sibling)
  local hub = {kind = "PassageHub", valid = true, connected_passages = {},
    draining_passages = {}, hub_domes = {}, units = {}}
  local map = {MapHasAny = function() return false end}
  function hub:GetMap() return map end
  function hub:GetRadius() return 1 end
  local dome = {kind = "Dome", valid = true, connected_passages = {}}
  local passage = setmetatable({kind = "PassageBase", valid = true, demolishing = false,
    hub_draining = false, traversing_colonists = {}, elements = {},
    elements_under_construction = {}, domes_connected = {hub, dome}, reconnects = 0,
    destroyed_attaches = 0}, {__index = PassageBase})
  local element = setmetatable({kind = "PassageGridElement", valid = true,
    owner = dome, is_pf_tunnel = hub, leads = 0, destroyed_attaches = 0},
    {__index = PassageGridElement})
  function element:BuildWaypointChains() self.waypoint_chains = true end
  function element:GetEntrance() return {"waypoint"} end
  -- Movement seam only.  Archived Passage.lua:819 assigns
  -- PassageGridElement.OnEnterUnit = empty_func, so no synthetic element
  -- holder transition belongs here.  C42 remains outside this fixture; C117's
  -- native exit branch decides only from is_pf_tunnel.
  function element:LeadIn(unit, entrance)
    assert(type(entrance) == "table")
    self.leads = self.leads + 1
  end
  function element:DestroyAttaches() self.destroyed_attaches = self.destroyed_attaches + 1 end
  passage.elements = {element}
  hub.connected_passages[passage] = true
  dome.connected_passages[passage] = true
  hub.hub_domes[dome] = 1
  hub.hub_domes[1] = dome

  local sibling = false
  if with_sibling then
    sibling = setmetatable({kind = "PassageBase", valid = true, demolishing = false,
      hub_draining = false, elements = {{kind = "PassageGridElement", valid = true,
      is_pf_tunnel = hub}}}, {__index = PassageBase})
    hub.connected_passages[sibling] = true
  end
  return passage, hub, dome, sibling, element, make_unit("in-flight", true)
end

SMRFixPack = {result = false}
function SMRFixPack.Register(id, spec)
  SMRFixPack.id = id
  SMRFixPack.result = spec.apply()
end
function SMRFixPack.Require(_, specs)
  for _, item in ipairs(specs) do
    local ok, name
    if item.class then
      local cls = _G[item.class]
      ok = type(cls) == "table" and type(cls[item.method]) == "function"
      name = item.class .. "." .. item.method
    elseif item.global then
      ok = type(_G[item.global]) == "function"
      name = item.global
    elseif item.test then
      ok = item.test() and true or false
      name = "(custom check)"
    elseif item.probe then
      local ran, result = pcall(item.probe)
      ok = ran and result == true
      name = "(behaviour probe)"
    end
    if not ok then return item.reason or (name .. " not found (game update changed it?)") end
  end
end
'''


def load_body(rt, rel, pattern):
    text, first, last = db.body(rel, pattern, tree=BUILD)
    db.load_at(rt, text, "=" + rel, first)
    return first, last


OLD_COUNT = "#self.traversing_colonists > 0"
NEW_COUNT = "has_valid_traverser(self.traversing_colonists)"


def runtime(patched=True, missing_traverse=False, broken_probe=False, chained=False,
            old_count=False):
    """A fresh Lua process is also the harness's no-mod-state reload model.

    old_count loads the module with the played 7f6e6bf wait predicate (an
    unfiltered `#traversing_colonists` count) as the old-shape mutant.
    """
    rt = db.lua_runtime()
    db.load_at(rt, PRELUDE, "=c117_fixture")
    for rel, pattern in BODIES:
        load_body(rt, rel, pattern)
    if missing_traverse:
        rt.execute("PassageBase.TraverseTunnel = nil")
    if broken_probe:
        rt.execute("function PassageBase:WouldStrandHubColonists() return true end")
    if chained:
        rt.execute(r'''
          local prior = PassageBase.TraverseTunnel
          function PassageBase:TraverseTunnel(...)
            CHAIN_CALLS = (CHAIN_CALLS or 0) + 1
            local result = prior(self, ...)
            return result, nil, "third"
          end
        ''')
    if patched:
        text = db.read(str(MODULE))
        if old_count:
            assert text.count(NEW_COUNT) == 1, "valid-count predicate not found"
            text = text.replace(NEW_COUNT, OLD_COUNT)
        db.load_at(rt, text, "=Code/Fix_PassageHubSalvageDrain.lua")
    return rt


def busy_spoke(patched):
    """Start traversal, then let native demolition run while it is in flight."""
    rt = runtime(patched)
    rt.execute(r'''
      P, H, D, S, E, INFLIGHT = make_case(true)
      STARTED = P:TraverseTunnel(INFLIGHT, false, false, false, E)
      assert(STARTED and #P.traversing_colonists == 1)
      ON_WAIT = function() INFLIGHT:FinishTraversal() end
      P:OnDemolish()
      ON_HUB = INFLIGHT.holder == H and INFLIGHT.passage_hub == H
    ''')
    g = rt.globals()
    return {
        "applied": g.SMRFixPack.result is None,
        "waits": g.WAIT_CALLS,
        "on_hub": g.ON_HUB,
        "outside_updates": g.INFLIGHT.outside_updates,
        "pf_removed": g.E.is_pf_tunnel is None,
        "traversers": len(g.P.traversing_colonists),
    }


def last_exit(patched):
    rt = runtime(patched)
    rt.execute(r'''
      P, H, D, S, E, INFLIGHT = make_case(false)
      assert(P:TraverseTunnel(INFLIGHT, false, false, false, E))
      ON_WAIT = function() INFLIGHT:FinishTraversal() end
      P:OnDemolish()
      ON_HUB = INFLIGHT.holder == H and INFLIGHT.passage_hub == H
    ''')
    g = rt.globals()
    return {
        "waits": g.WAIT_CALLS,
        "on_hub": g.ON_HUB,
        "pf_removed": g.E.is_pf_tunnel is None,
    }


def main():
    assert MODULE.is_file(), MODULE
    bench = db.Bench("C117 busy hub-spoke salvage drain -- archived 1.1.1.405907")
    check = bench.check
    print("extracted shipped bodies:")
    for rel, pattern in BODIES:
        _, first, last = db.body(rel, pattern, tree=BUILD)
        print(f"  {rel}:{first}-{last}  /{pattern}/")

    fixed = busy_spoke(True)
    absent = busy_spoke(False)
    check("module applies through its real Require probe", fixed["applied"])
    check("busy spoke with a live sibling waits for its in-flight colonist",
          fixed["waits"] == 1 and fixed["traversers"] == 0,
          f"waits={fixed['waits']}, remaining={fixed['traversers']}")
    check("in-flight colonist arrives on the hub before disconnect",
          fixed["on_hub"] is True
          and fixed["outside_updates"] == 1 and fixed["pf_removed"],
          "holder/marker are hub; native disconnect removes the PF endpoint after arrival")
    check("fix-removed control takes the native outside branch after the same disconnect",
          absent["waits"] == 1 and absent["on_hub"] is False
          and absent["outside_updates"] == 0 and absent["pf_removed"],
          f"waits={absent['waits']}, on_hub={absent['on_hub']}")

    native_last = last_exit(False)
    fixed_last = last_exit(True)
    check("last exit retains native pre-disconnect wait with the module installed",
          fixed_last["waits"] == native_last["waits"] == 1
          and fixed_last["on_hub"] is True and native_last["on_hub"] is True,
          f"native/fixed waits={native_last['waits']}/{fixed_last['waits']}")

    entrant = runtime(True)
    entrant.execute(r'''
      P, H, D, S, E, INFLIGHT = make_case(true)
      P.demolishing = true; P.hub_draining = H; H.draining_passages[P] = true
      FRESH = make_unit("fresh", true); FRESH.pf_tunnel = P
      FRESH.pf_end_point, FRESH.pf_end_point_map, FRESH.pf_param = false, false, false
      FRESH_RESULT = FRESH:TraverseTunnel()
    ''')
    eg = entrant.globals()
    check("fresh entrant on a draining spoke with a usable sibling is refused",
          eg.FRESH_RESULT is False and len(eg.P.traversing_colonists) == 0)
    check("refused entry uses native Unit:TraverseTunnel ClearPath contract",
          eg.FRESH.clear_paths == 1 and eg.PF_ADVANCES == 0,
          f"ClearPath={eg.FRESH.clear_paths}, AdvancePathTunnel={eg.PF_ADVANCES}")

    last_entry = runtime(True)
    last_entry.execute(r'''
      P, H, D, S, E, INFLIGHT = make_case(false)
      P.demolishing = true; P.hub_draining = H; H.draining_passages[P] = true
      FRESH = make_unit("last-exit entrant", true); FRESH.pf_tunnel = P
      FRESH.pf_end_point, FRESH.pf_end_point_map, FRESH.pf_param = false, false, false
      LAST_ENTRY_RESULT = FRESH:TraverseTunnel()
    ''')
    lg = last_entry.globals()
    check("with no safe sibling, fresh last-exit traffic tail-delegates to native traversal",
          lg.LAST_ENTRY_RESULT is True and lg.FRESH.clear_paths == 0
          and lg.PF_ADVANCES == 1 and len(lg.P.traversing_colonists) == 1)

    simultaneous = runtime(True)
    simultaneous.execute(r'''
      P, H, D, S, E, INFLIGHT = make_case(true)
      P.demolishing = true; P.hub_draining = H; H.draining_passages[P] = true
      S.demolishing = true; S.hub_draining = H; H.draining_passages[S] = true
      FRESH = make_unit("simultaneous-salvage entrant", true); FRESH.pf_tunnel = P
      FRESH.pf_end_point, FRESH.pf_end_point_map, FRESH.pf_param = false, false, false
      SIMULTANEOUS_RESULT = FRESH:TraverseTunnel()
    ''')
    sg = simultaneous.globals()
    check("a simultaneous draining sibling is not treated as a safe exit (C99 remains native)",
          sg.SIMULTANEOUS_RESULT is True and sg.FRESH.clear_paths == 0
          and sg.PF_ADVANCES == 1 and len(sg.P.traversing_colonists) == 1)

    cancel = runtime(True)
    cancel.execute(r'''
      P, H, D, S, E, INFLIGHT = make_case(true)
      P.demolishing = true; P.hub_draining = H; H.draining_passages[P] = true
      table.insert(P.traversing_colonists, INFLIGHT)
      P.demolishing = false
      P:OnSetDemolishing(false)
      FRESH = make_unit("after-cancel", true); FRESH.pf_tunnel = P
      FRESH.pf_end_point, FRESH.pf_end_point_map, FRESH.pf_param = false, false, false
      CANCEL_ENTRY_RESULT = FRESH:TraverseTunnel()
    ''')
    cg = cancel.globals()
    check("native cancellation clears hub_draining and the hub drain registration",
          cg.P.hub_draining is False and cg.H.draining_passages[cg.P] is None
          and cg.P.reconnects == 1)
    check("a fresh entrant after cancellation is no longer refused",
          cg.CANCEL_ENTRY_RESULT is True and cg.FRESH.clear_paths == 0 and cg.PF_ADVANCES == 1)

    # A fresh runtime intentionally receives only the native fields that a
    # native demolish/traversal thread already carries.  No process-local mod
    # marker or saved mod callback is supplied.
    reloaded = runtime(True)
    reloaded.execute(r'''
      P, H, D, S, E, INFLIGHT = make_case(true)
      assert(P:TraverseTunnel(INFLIGHT, false, false, false, E))
      P.demolishing = true; P.hub_draining = H; H.draining_passages[P] = true
      RELOAD_BLOCKS = P:WouldStrandHubColonists()
      ON_WAIT = function() INFLIGHT:FinishTraversal() end
      P:OnDemolish()
      RELOAD_DELIVERED = INFLIGHT.holder == H and INFLIGHT.passage_hub == H
      RELOAD_RELEASES = #P.traversing_colonists == 0 and E.is_pf_tunnel == nil
    ''')
    rg = reloaded.globals()
    module_text = db.read(str(MODULE))
    check("fresh-runtime reload reconstructs the drain solely from native fields",
          rg.RELOAD_BLOCKS is True and rg.RELOAD_DELIVERED is True and rg.RELOAD_RELEASES is True
          and rg.SMRFixPack.result is None)
    check("module declares no save handler or persisted game variable",
          "OnMsg.Save" not in module_text and "GameVar" not in module_text)

    # An invalid leftover traverser (a colonist that died mid-passage) must not
    # hold the pre-disconnect wait this module adds. Native decides by the
    # sibling shortcut (false), so the disconnect proceeds as shipped.
    STALE_CASE = r'''
      P, H, D, S, E, INFLIGHT = make_case(true)
      P.demolishing = true; P.hub_draining = H; H.draining_passages[P] = true
      DEAD = make_unit("dead", true); DEAD.valid = false
      table.insert(P.traversing_colonists, DEAD)
      STALE_ONLY = P:WouldStrandHubColonists()
      table.insert(P.traversing_colonists, INFLIGHT)
      STALE_AND_LIVE = P:WouldStrandHubColonists()
    '''
    stale = runtime(True)
    stale.execute(STALE_CASE)
    sg = stale.globals()
    check("an invalid leftover traverser alone does not hold the pre-disconnect wait",
          sg.STALE_ONLY is False,
          f"stale_only={sg.STALE_ONLY}")
    check("a live traverser beside an invalid entry still holds the wait",
          sg.STALE_AND_LIVE is True,
          f"stale_and_live={sg.STALE_AND_LIVE}")
    old_shape = runtime(True, old_count=True)
    old_shape.execute(STALE_CASE)
    og = old_shape.globals()
    check("old-shape control: the played unfiltered count held the wait on the invalid entry alone",
          og.STALE_ONLY is True and og.STALE_AND_LIVE is True,
          f"old stale_only={og.STALE_ONLY}")
    native_stale = runtime(False)
    native_stale.execute(STALE_CASE)
    ng = native_stale.globals()
    check("native control: the sibling shortcut disconnects regardless of the stale entry",
          ng.STALE_ONLY is False and ng.STALE_AND_LIVE is False)

    missing = runtime(True, missing_traverse=True)
    check("missing PassageBase:TraverseTunnel shape declines before wrapper install",
          "PassageBase.TraverseTunnel" in str(missing.globals().SMRFixPack.result))
    probe_drift = runtime(True, broken_probe=True)
    check("behaviour-probe control declines when the sibling shortcut no longer returns false",
          probe_drift.globals().SMRFixPack.result == "hub sibling shortcut changed")

    chained = runtime(True, chained=True)
    chained.execute(r'''
      P, H, D, S, E, INFLIGHT = make_case(true)
      CHAIN_UNIT = make_unit("chain", true)
      R1, R2, R3 = P:TraverseTunnel(CHAIN_UNIT, false, false, false, E)
      P.kind = "ForeignPassage"
      FOREIGN_UNIT = make_unit("foreign", true)
      F1, F2, F3 = P:TraverseTunnel(FOREIGN_UNIT, false, false, false, E)
    ''')
    hg = chained.globals()
    check("accepted PassageBase traversal preserves all chained returns, including nil",
          hg.R1 is True and hg.R2 is None and hg.R3 == "third")
    check("first IsKindOf gate passes a foreign receiver through with chained returns intact",
          hg.F1 is True and hg.F2 is None and hg.F3 == "third" and hg.CHAIN_CALLS == 2)
    return bench.finish("ALL DEMANDS HELD -- C117's drain decisions discriminate from the native race.")


if __name__ == "__main__":
    raise SystemExit(main())
