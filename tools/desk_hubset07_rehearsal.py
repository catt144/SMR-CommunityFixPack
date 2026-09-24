#!/usr/bin/env python3
"""hubset 07 sitting instruments: a declared-VOID desk rehearsal.

Run: python tools/desk_hubset07_rehearsal.py

Loads the TestKit's sitting-owned Code/80_AgentSlots.lua whole, under a stub
SMRTK and stub engine objects, then drives each instrument's own step
functions, triggers and slots through two fixtures per prediction:

  * as-predicted: the state the prediction expects, which must read HELD;
  * scratch variant: the state that refutes it, which must read REFUTED.

VOID by declaration: nothing here ran in a game. Object state, positions, hex
grids and IsUnitInDome answers are desk fixtures, so a pass shows only that
each instrument CAN return its refuting verdict from the fields it reads. It
says nothing about what the colony will do. Sitting 07 supplies that.
"""
import os
import sys

import deskbench as db

SLOTS = os.path.join(db.TESTKIT, "Code", "80_AgentSlots.lua")

PRELUDE = r'''
empty_table = {}
const = { HourDuration = 30000 }
g_Consts = { DefaultOutsideWorkplacesRadius = 20 }
OnMsg = {}
LoadedMaps = {}
local clock = 0
function GameTime() return clock end
function advance(ms) clock = clock + ms end
function GetTimeFactor() return 0 end
function IsValid(o) return type(o) == "table" and o.handle ~= nil and o.valid ~= false end
function IsKindOf(o, k) return type(o) == "table" and o.kinds ~= nil and o.kinds[k] == true end
function table.find(t, v) for i, x in ipairs(t or empty_table) do if x == v then return i end end end
function WorldToHex(a, b) if type(a) == "table" then return a.q, a.r end return a, b end
function HexGridGetObject(grid, q, r, cls) return grid[tostring(q) .. "," .. tostring(r)] end
function HexAxialDistance(a, b) return a.dist and a.dist[b] or 0 end
function IsUnitInDome(c) return c.at_dome end
function TGetID(t) return t.id end
function _InternalTranslate(t) return t.text end
selected = false
function SelectObj(o) selected = o end
function ViewObjectMars(o) end
SMRFixPack = { fixes = {} }
function set_build(b)
  SMRFixPack.fixes = {}
  if b == "hubset" then
    for _, id in ipairs({ "HubLocalAccess", "HubMarkerDeparture", "ObsoleteHomeRescue",
        "PassageHubSalvageDrain", "PassageStaleHolder", "RescueReturnText" }) do
      SMRFixPack.fixes[id] = { status = "active" }
    end
  end
end

-- stub SMRTK: records registrations; arming at load would show in `armed_log`
local armed_log, logs = {}, {}
SMRTK = { error_count = 0, bound = {}, triggers = {}, armed_log = armed_log, logs = logs }
local T = SMRTK
function T.Bind(n, label, fn, opts) local d = { id = "slot_" .. n, label = label, fn = fn }; T.bound[n] = d; return d end
function T.BindScratch(label, fn, opts) local d = { id = "slot_scratch", label = label, fn = fn }; T.bound.scratch = d; return d end
function T.Trigger(spec) T.triggers[spec.id] = spec; return spec end
function T.Log(verb, kv) logs[#logs + 1] = { verb = verb, kv = kv } end
function T.Arm(id, ...) armed_log[#armed_log + 1] = id; return true, {} end
function T.ArmedCount() return #armed_log end
function T.Mark() return 1 end
function T.ConsoleControl() end
function T.TaintRead() end
function T.Run() return true end

-- world
local next_handle = 100
function obj(t) next_handle = next_handle + 1; t.handle = next_handle; t.valid = true; return t end
map = { object_hex_grid = {}, objs = { Colonist = {}, PassageHubBase = {}, PassageBase = {} } }
function map:MapGet(scope, class) return self.objs[class] end
LoadedMaps[1] = map
function grid_put(q, r, o) map.object_hex_grid[tostring(q) .. "," .. tostring(r)] = o end
function new_hub(q, r)
  local h = obj { class = "PassageHub", q = q, r = r, hub_domes = {}, connected_passages = {},
    draining_passages = {}, units = {}, dist = {} }
  function h:GetMap() return map end
  grid_put(q, r, h)
  return h
end
function new_dome(name) return obj { class = "Dome", name = name, labels = { Homeless = {} } } end
function new_passage(hub)
  local p = obj { class = "Passage", traversing_colonists = {}, elements = {}, active = true,
    hub_draining = false }
  function p:IsPFTunnelActive() return self.active end
  function p:ToggleDemolish() self.demolishing = true end
  hub.connected_passages[p] = true
  return p
end
function new_colonist(home)
  local c = obj { class = "Colonist", dome = home, q = 50, r = 50, vq = 50, vr = 50,
    command = "Work", holder = false, passage_hub = false, traversing_passage = false,
    outside_start = false, transport_task = false, workplace = obj { class = "Workplace" } }
  function c:IsDying() return false end
  function c:IsInWorkCommand() return self.command == "Work" end
  function c:GetVisualPosXYZ() return self.vq, self.vr end
  function c:GetFired() self.workplace = false end
  return c
end
function at(c, q, r) c.q, c.r, c.vq, c.vr = q, r, q, r end
'''

SCENARIOS = r'''
local T, H = SMRTK, SMRTK.H7
local rows = {}
local function row(id, build, variant, expected, got)
  rows[#rows + 1] = { id = id, build = build, variant = variant, expected = expected, got = tostring(got) }
end
local function ctx() return { mark = function() end, log = function(v, kv) T.logs[#T.logs + 1] = { verb = v, kv = kv } end, state = {} } end

-- shared fixture: a far dome (Brussels shape) attached to a hub 24 hexes from its centre
local home = new_dome("Brussels")
local hub = new_hub(10, 10)
hub.hub_domes[1] = home; hub.hub_domes[home] = 1; hub.dist[home] = 24

------------------------------------------------ P1 / P2: C115 rescue follow
local function rescue_case(build, home_at_arm, script)
  local c = new_colonist(home)
  local task = obj { class = "ColonistTransportTask", colonist = c, dest_dome = home, source_dome = false,
    migration_dest = false, state = "new", shuttle = false }
  c.transport_task = task
  c.at_dome = home_at_arm and home or nil
  local rec = { c = c, task = task, home_at_arm = home_at_arm }
  script(c, task)
  H.rescue_step(rec)
  local f = H.rescue_facts({ rec })
  return f
end
for _, b in ipairs({ "hubset", "main" }) do
  -- cleaned while home
  local cleaned = rescue_case(b, true, function(c, task) c.transport_task = false end)
  -- walked back out: leaves home, then ready_for_pickup
  local walked = rescue_case(b, true, function(c, task) c.at_dome = nil end)
  local pred, scratch = cleaned, walked
  if b == "main" then pred, scratch = walked, cleaned end
  row("P1", b, "as-predicted", "HELD", H.judge.P1(b, pred))
  row("P1", b, "scratch", "REFUTED", H.judge.P1(b, scratch))
  local served = rescue_case(b, false, function(c, task) task.state = "ready_for_pickup" end)
  local dropped = rescue_case(b, false, function(c, task) c.transport_task = false end)
  row("P2", b, "as-predicted", "HELD", H.judge.P2(b, served))
  row("P2", b, "scratch", "REFUTED", H.judge.P2(b, dropped))
end

------------------------------------------------ follow: C114, P5, P6, R4, R5, R6
-- steps: list of functions applied before each follow_step poll
local function follow_case(build, kind, steps)
  local c = new_colonist(home)
  if kind == "hub" then at(c, 10, 10); c.holder = hub; c.passage_hub = hub
  else
    local p = new_passage(hub)
    p.traversing_colonists[1] = c
    c.traversing_passage = p; c.holder = hub; c.passage_hub = hub
  end
  local s = { c = c, hub = hub, kind = kind, build = build, fired = true }
  if kind == "flight" then s.mid_flag = true; s.mid_listed = true end
  for _, step in ipairs(steps) do
    step(c, s)
    if H.follow_step(s) then break end
  end
  return H.follow_facts(s, build), s
end
local function dump(c) c.holder = false end
local function book(c) c.transport_task = obj { class = "ColonistTransportTask", colonist = c, dest_dome = home,
  source_dome = false, migration_dest = false, state = "new" } end
local function into_spoke(c)
  local p = new_passage(hub); p.traversing_colonists[1] = c; c.traversing_passage = p
end
local function land_home(c)
  local p = c.traversing_passage
  if p then table.remove(p.traversing_colonists, 1) end
  c.traversing_passage = false; c.passage_hub = false; at(c, 30, 30); c.at_dome = home
end
local function ready(c) c.transport_task.state = "ready_for_pickup" end
local function walk_open(c) at(c, 14, 10); c.at_dome = nil end

-- C114 on the hub (P3) and mid-spoke (P4)
local safe_hub = { dump, into_spoke, land_home }
local booked_hub = { function(c) dump(c); book(c) end, walk_open, ready }
local safe_flight = { land_home }
local booked_flight = { book, land_home, walk_open, ready }
for _, b in ipairs({ "hubset", "main" }) do
  for _, k in ipairs({ { "P3", "hub", safe_hub, booked_hub }, { "P4", "flight", safe_flight, booked_flight } }) do
    local safe = follow_case(b, k[2], k[3])
    local booked = follow_case(b, k[2], k[4])
    local pred, scratch = safe, booked
    if b == "main" then pred, scratch = booked, safe end
    row(k[1], b, "as-predicted", "HELD", pred.c114)
    row(k[1], b, "scratch", "REFUTED", scratch.c114)
  end
end

-- P5: first standing off-hub moment on open ground
local function open_case(build, marker_kept, timer)
  local f = follow_case(build, "hub", { dump, function(c)
    walk_open(c)
    if not marker_kept then c.passage_hub = false end
    c.outside_start = timer and 12345 or false
  end, function(c) c.transport_task = false end, land_home })
  return f
end
row("P5", "hubset", "as-predicted", "HELD", open_case("hubset", false, true).p5)
row("P5", "hubset", "scratch", "REFUTED", open_case("hubset", true, false).p5)
row("P5", "main", "as-predicted", "HELD", open_case("main", true, false).p5)
row("P5", "main", "scratch", "REFUTED", open_case("main", false, true).p5)

-- P6: marker kept across a spoke vs dropped mid-flight
local kept = follow_case("hubset", "hub", { dump, into_spoke, land_home })
local lost = follow_case("hubset", "hub", { dump, into_spoke, function(c) c.passage_hub = false end, land_home })
row("P6", "hubset", "as-predicted", "HELD", kept.p6)
row("P6", "hubset", "scratch", "REFUTED", lost.p6)

-- R4: the dump stays on the hub hex vs walked off the footprint
local on = follow_case("main", "hub", { dump, into_spoke, land_home })
local off = follow_case("main", "hub", { function(c) dump(c); at(c, 13, 10) end, into_spoke, land_home })
row("R4", "main", "as-predicted", "HELD", on.r4)
row("R4", "main", "scratch", "REFUTED", off.r4)

-- R5: flag live mid-passage and cleared from the list on arrival
local good = follow_case("hubset", "flight", { function() end, land_home })
local stuck = follow_case("hubset", "flight", { function() end, function(c)
  c.traversing_passage = false; c.passage_hub = false; at(c, 30, 30); c.at_dome = home  -- left listed
end })
row("R5", "hubset", "as-predicted", "HELD", good.r5)
row("R5", "hubset", "scratch", "REFUTED", stuck.r5)
local flagless = follow_case("hubset", "flight", { function(c, s) s.mid_flag = false end, land_home })
row("R5", "hubset", "scratch-flag", "REFUTED", flagless.r5)

-- R6: no overland walk vs an open-ground walk
row("R6", "hubset", "as-predicted", "HELD", kept.r6)
row("R6", "main", "scratch", "REFUTED", open_case("main", true, false).r6)

------------------------------------------------ R3: the arrival trigger itself
local function arrival_case(land_on_hub)
  local c = new_colonist(home)
  local p = new_passage(hub)
  p.traversing_colonists[1] = c; c.traversing_passage = p
  map.objs.PassageHubBase = { hub }
  local trig = T.triggers.h7_hub_arrival
  local cx = ctx()
  trig.prepare(cx)
  local fired = trig.when(cx)
  table.remove(p.traversing_colonists, 1)
  c.traversing_passage = false; c.holder = hub; c.passage_hub = hub
  if land_on_hub then at(c, 10, 10) else at(c, 12, 10) end
  local ok, fields = trig.when(cx)
  hub.connected_passages[p] = nil
  map.objs.PassageHubBase = {}
  return fired, ok, fields
end
local f0, ok1, fields1 = arrival_case(true)
row("R3", "any", "first-poll-silent", "false", f0)
row("R3", "any", "as-predicted", "HELD", ok1 and fields1.r3)
local _, ok2, fields2 = arrival_case(false)
row("R3", "any", "scratch", "REFUTED", ok2 and fields2.r3)

------------------------------------------------ P7 / P8 / P9: drain
local function drain_case(build, opts)
  local h = new_hub(20, 20)
  local p = new_passage(h)
  local sib = new_passage(h)
  local a, b2 = new_colonist(home), new_colonist(home)
  p.traversing_colonists = { a, b2 }
  a.traversing_passage, b2.traversing_passage = p, p
  local el = obj { class = "PassageGridElement", units = {} }
  p.elements = { el }
  local stray = new_colonist(home); at(stray, 60, 60)
  if opts.stale then el.units[1] = stray end
  local s = { p = p, hub = h, build = build, name = "p", t0 = 0 }
  H.drain_step(s)                  -- countdown: not yet draining
  p.hub_draining = h
  H.drain_step(s)                  -- drain starts: snapshot a, b2
  if opts.fresh then
    local late = new_colonist(home); late.traversing_passage = p
    table.insert(p.traversing_colonists, late)
    H.drain_step(s)
    table.remove(p.traversing_colonists)
    late.traversing_passage = false
  end
  for _, c in ipairs({ a, b2 }) do
    c.traversing_passage = false; at(c, 20, 20)
    c.holder, c.passage_hub = h, h
  end
  if opts.unmarked then b2.holder, b2.passage_hub = false, false end
  p.traversing_colonists = {}
  H.drain_step(s)
  p.active = false; p.valid = false
  if opts.kick then at(stray, 20, 20) end
  H.drain_step(s)
  return H.drain_facts(s, build)
end
row("P7", "hubset", "as-predicted", "HELD", drain_case("hubset", {}).p7)
row("P7", "hubset", "scratch", "REFUTED", drain_case("hubset", { unmarked = true }).p7)
row("P7", "main", "as-predicted", "HELD", drain_case("main", { unmarked = true }).p7)
row("P7", "main", "scratch", "REFUTED", drain_case("main", {}).p7)
row("P8", "hubset", "as-predicted", "HELD", drain_case("hubset", {}).p8)
row("P8", "hubset", "scratch", "REFUTED", drain_case("hubset", { fresh = true }).p8)
row("P9", "hubset", "as-predicted", "HELD", drain_case("hubset", { stale = true }).p9)
row("P9", "hubset", "scratch", "REFUTED", drain_case("hubset", { stale = true, kick = true }).p9)
row("P9", "hubset", "no-stale", "NOT_SAMPLED", drain_case("hubset", {}).p9)

------------------------------------------------ census: R1, R2, P10
local function census_case(opts)
  local h = new_hub(30, 30)
  local c = new_colonist(home); at(c, 30, 30); c.holder = h
  h.units = { c }
  if opts.mismatch then c.holder = false end
  if opts.wander then at(c, 45, 45) end
  local p = new_passage(h)
  local el = obj { class = "PassageGridElement", units = {} }
  p.elements = { el }
  if opts.stale then el.units[1] = new_colonist(home) end
  map.objs.PassageHubBase, map.objs.PassageBase, map.objs.Colonist = { h }, { p }, { c }
  local out = H.census()
  map.objs.PassageHubBase, map.objs.PassageBase, map.objs.Colonist = {}, {}, {}
  return out
end
row("R1", "any", "as-predicted", "HELD", H.judge.R1(nil, census_case({}).r1))
row("R1", "any", "scratch", "REFUTED", H.judge.R1(nil, census_case({ mismatch = true }).r1))
row("R2", "any", "as-predicted", "HELD", H.judge.R2(nil, census_case({}).r2))
row("R2", "any", "scratch", "REFUTED", H.judge.R2(nil, census_case({ wander = true }).r2))
row("P10", "any", "as-predicted", "HELD", H.judge.P10(nil, census_case({}).c42))
row("P10", "any", "scratch", "REFUTED", H.judge.P10(nil, census_case({ stale = true }).c42))

------------------------------------------------ slot 6: C111 text and R7, through the bound slot
local function slot6(build, tid_home, text_home, tid_reloc, r7_open_timer)
  set_build(build)
  local rescue = new_colonist(home); rescue.command = "Transport"
  rescue.transport_task = obj { class = "ColonistTransportTask", colonist = rescue, dest_dome = home,
    source_dome = false, migration_dest = false }
  function rescue:Getui_command() return { id = tid_home, text = text_home } end
  local other = new_dome("Tesla")
  local mover = new_colonist(home); mover.command = "TransportByFoot"; mover.emigration_dome = other
  function mover:Getui_command() return { id = tid_reloc, text = "Moving to a new Dome: Tesla" } end
  local open = new_colonist(home); open.passage_hub = hub; at(open, 40, 40)
  function open:UpdateOutside() self.outside_start = r7_open_timer and 777 or false end
  map.objs.Colonist = { rescue, mover, open }
  local fn = T.bound[6].fn
  local r1 = fn(ctx())
  local r2 = fn(ctx())
  local cx = ctx()
  local r3, why3 = fn(cx)
  local r7
  for _, l in ipairs(T.logs) do
    if l.kv and l.kv.leg == "r7" and l.kv.class == "open" then r7 = l.kv.verdict end
  end
  map.objs.Colonist = {}
  return r1, r2, r3, why3, r7
end
local a1, a2 = slot6("hubset", 0, "Returning to Dome: Brussels", 4333, true)
row("P11", "hubset", "as-predicted", "HELD", a1.verdict)
row("P12", "hubset", "as-predicted", "HELD", a2.verdict)
local b1, b2 = slot6("hubset", 4333, "Moving to a new Dome: Brussels", 9999, true)
row("P11", "hubset", "scratch", "REFUTED", b1.verdict)
row("P12", "hubset", "scratch", "REFUTED", b2.verdict)
local c1, _, _, _, r7a = slot6("main", 4333, "Moving to a new Dome: Brussels", 4333, true)
row("P11", "main", "as-predicted", "HELD", c1.verdict)
row("R7", "main", "as-predicted", "HELD", r7a)
local _, _, r3b, why3b = slot6("hubset", 0, "Returning to Dome: Brussels", 4333, true)
row("R7", "hubset", "refused-on-hubset", "false", r3b)
T.logs = {}
local _, _, _, _, r7b = slot6("main", 4333, "Moving to a new Dome: Brussels", 4333, false)
row("R7", "main", "scratch", "REFUTED", r7b)

------------------------------------------------ load-time contract
row("LOAD", "any", "armed-at-load", "0", #T.armed_log)
local n = 0 for k in pairs(T.bound) do n = n + 1 end
row("LOAD", "any", "bindings", "7", n)
local t = 0 for k in pairs(T.triggers) do t = t + 1 end
row("LOAD", "any", "triggers", "6", t)
return rows
'''


def main():
    rt = db.lua_runtime()
    rt.execute(PRELUDE)
    src = db.read(SLOTS)
    db.load_at(rt, src, "=Code/80_AgentSlots.lua")
    armed_at_load = len(list(rt.globals().SMRTK.armed_log.values()))
    rows = rt.execute(SCENARIOS)
    failures = 0
    total = 0
    for i in range(1, len(rows) + 1):
        r = rows[i]
        total += 1
        ok = str(r.expected) == str(r.got)
        failures += 0 if ok else 1
        print("%s %-4s %-7s %-18s expected=%-11s got=%s" % (
            "PASS" if ok else "FAIL", r.id, r.build, r.variant, r.expected, r.got))
    print("armed at load (before scenarios): %d" % armed_at_load)
    print("%d of %d rehearsal demands held" % (total - failures, total))
    print("VOID: desk fixtures only; no game ran. See the module docstring.")
    if failures or armed_at_load:
        print("REHEARSAL FAILED")
        return 1
    print("ALL DEMANDS HELD")
    return 0


if __name__ == "__main__":
    sys.exit(main())
