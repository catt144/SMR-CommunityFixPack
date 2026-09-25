#!/usr/bin/env python3
"""hubset 07B second-pass instruments: a declared-VOID desk rehearsal.

Run: python -B tools/desk_hubset07b_rehearsal.py

Loads the TestKit's sitting-owned Code/80_AgentSlots.lua whole, under a stub
SMRTK and stub engine objects, and drives the pass's own slots, triggers and
pure steps through two fixtures per prediction:

  * as-predicted: the state the prediction expects, which must read HELD;
  * scratch variant: the state that refutes it, which must read REFUTED.

C114's subject selection is also driven through every input that would let
native access succeed: each one alone must make the subject ineligible, so a
pass shows the selection reads the inputs the archived HasLocalAccess reads
(ColonistTransport.lua:270-299, 1.1.1.405907), never the answer under test.

VOID by declaration: nothing here ran in a game. Object state, positions,
ranges and routes are desk fixtures, so a pass shows only that each instrument
CAN return its refuting verdict from the fields it reads. It says nothing about
what the colony will do. The attended 07B pass supplies that.
"""
import os
import sys

import deskbench as db

SLOTS = os.path.join(db.TESTKIT, "Code", "80_AgentSlots.lua")

PRELUDE = r'''
empty_table = {}
const = { HourDuration = 30000, MaxSaneTimeFactor = 128000, DefaultTimeFactor = 1000 }
g_Consts = { DefaultOutsideWorkplacesRadius = 20 }
OnMsg = {}
LoadedMaps = {}
local clock = 0
function GameTime() return clock end
function advance(ms) clock = clock + ms end
factor = 0
function GetTimeFactor() return factor end
function IsValid(o) return type(o) == "table" and o.handle ~= nil and o.valid ~= false end
function IsKindOf(o, k) return type(o) == "table" and o.kinds ~= nil and o.kinds[k] == true end
function table.find(t, v) for i, x in ipairs(t or empty_table) do if x == v then return i end end end
function WorldToHex(a, b) if type(a) == "table" then return a.q, a.r end return a, b end
function HexGridGetObject(grid, q, r, cls) return grid[tostring(q) .. "," .. tostring(r)] end
function HexAxialDistance(a, b) return (a.dist and a.dist[b]) or (b.dist and b.dist[a]) or 0 end
function IsUnitInDome(c) return c.at_dome end
function TGetID(t) return t.id end
function _InternalTranslate(t) return t.text end
-- range helpers: fixtures name what is in reach
function IsBuildingInDomeRange(bld, dome) return bld.reach and bld.reach[dome] or false end
function IsUnitInDomeRange(unit, dome) return unit.reach and unit.reach[dome] or false end
function FindNearestObject(list, pt) return list[1] end
function IsLRTransportAvailable(city) return city.shuttles end
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

-- stub SMRTK: records registrations, arms and runs
local armed_log, logs, runs = {}, {}, {}
SMRTK = { error_count = 0, bound = {}, triggers = {}, armed_log = armed_log, logs = logs, runs = runs, arm_ok = true }
local T = SMRTK
function T.Bind(n, label, fn, opts) local d = { id = "slot_" .. n, label = label, fn = fn }; T.bound[n] = d; return d end
function T.BindScratch(label, fn, opts) local d = { id = "slot_scratch", label = label, fn = fn }; T.bound.scratch = d; return d end
function T.Trigger(spec) T.triggers[spec.id] = spec; return spec end
function T.Log(verb, kv) logs[#logs + 1] = { verb = verb, kv = kv } end
function T.Arm(id, ...) armed_log[#armed_log + 1] = { id = id, arg = select(1, ...) }; return T.arm_ok, { reason = "stub" } end
function T.ArmedCount() return #armed_log end
function T.ConsoleControl() end
function T.TaintRead() end
function T.Run(id, n) runs[#runs + 1] = { id = id, n = n }; if id == "speed" then factor = n * 1000 end; return true, {} end

-- world
local next_handle = 100
function obj(t) next_handle = next_handle + 1; t.handle = next_handle; t.valid = true; return t end
map = { object_hex_grid = {}, objs = { Colonist = {}, PassageHubBase = {}, PassageBase = {} } }
function map:MapGet(scope, class) return self.objs[class] end
LoadedMaps[1] = map
function grid_put(q, r, o) map.object_hex_grid[tostring(q) .. "," .. tostring(r)] = o end
function new_dome(name) return obj { class = "Dome", name = name, kinds = { Dome = true }, dist = {} } end
city = { labels = { Community = {} }, shuttles = true }
function new_hub(q, r)
  local h = obj { class = "PassageHub", q = q, r = r, hub_domes = {}, connected_passages = {},
    units = {}, dist = {}, reach = {}, city = city }
  function h:GetMap() return map end
  grid_put(q, r, h)
  return h
end
function new_passage(hub)
  local p = obj { class = "Passage", traversing_colonists = {}, active = true, hub_draining = false }
  function p:IsPFTunnelActive() return self.active end
  function p:ToggleDemolish() self.demolishing = true end
  hub.connected_passages[p] = true
  return p
end
function new_colonist(home)
  local c = obj { class = "Colonist", dome = home, q = 50, r = 50, city = city, command = "Work",
    holder = false, passage_hub = false, traversing_passage = false, transport_task = false,
    workplace = obj { class = "Workplace" }, work_route = false, reach = {}, dist = {}, train = false }
  function c:IsDying() return false end
  function c:IsInWorkCommand() return self.command == "Work" end
  function c:GetFired() self.workplace = false; self.command = "Idle" end
  function c:GetTransportRoute(b, cmd) if self.train then return 1, 2 end end
  return c
end
function at(c, q, r) c.q, c.r = q, r end
'''

SCENARIOS = r'''
local T, H = SMRTK, SMRTK.H7B
local rows = {}
local function row(id, build, variant, expected, got)
  rows[#rows + 1] = { id = id, build = build, variant = variant, expected = expected, got = tostring(got) }
end
local function ctx() return { mark = function() end, log = function(v, kv) T.logs[#T.logs + 1] = { verb = v, kv = kv } end, state = {} } end

-- Brussels shape: home 26 hexes from a hub, nearest community is home itself, out of range.
local home = new_dome("Brussels")
local hub = new_hub(10, 10)
hub.hub_domes[1] = home; hub.hub_domes[home] = 1; hub.dist[home] = 26
city.labels.Community = { home }

local function subject_on_hub()
  local c = new_colonist(home)
  at(c, 10, 10); c.holder = hub; c.passage_hub = hub; c.dist[home] = 26
  return c
end

------------------------------------------------ C114 selection: every native-true input excludes
local base = H.access_inputs(subject_on_hub(), hub)
row("SEL", "any", "exposed-fixture", "true", base.exposed)
local flips = {
  { "nearest-in-reach", function(c) hub.reach[home] = true end, function() hub.reach[home] = nil end },
  { "unit-in-range", function(c) c.reach[home] = true end, function() end },
  { "in-a-dome", function(c) c.at_dome = home end, function() end },
  { "hub-within-radius", function(c) hub.dist[home] = 20 end, function() hub.dist[home] = 26 end },
  { "unit-within-radius", function(c) c.dist[home] = 19 end, function() end },
  { "train-route", function(c) c.train = true end, function() end },
  { "work-route", function(c) c.work_route = { 1, 2, 3 } end, function() end },
  { "no-shuttles", function(c) city.shuttles = false end, function() city.shuttles = true end },
  { "unlinked", function(c) hub.hub_domes[home] = 0 end, function() hub.hub_domes[home] = 1 end },
}
for _, fl in ipairs(flips) do
  local c = subject_on_hub()
  fl[2](c)
  row("SEL", "any", fl[1], "false", H.access_inputs(c, hub).exposed)
  fl[3]()
end
-- a nearer community in reach (another dome) also excludes
local near = new_dome("Nearby")
city.labels.Community = { near, home }
hub.reach[near] = true
row("SEL", "any", "other-community-in-reach", "false", H.access_inputs(subject_on_hub(), hub).exposed)
hub.reach[near] = nil
city.labels.Community = { home }

------------------------------------------------ C114 arrival trigger
local function arrival(exposed, stay_in_flight)
  local c = new_colonist(home); c.dist[home] = 26
  local p = new_passage(hub)
  local sib = new_passage(hub)
  p.traversing_colonists[1] = c; c.traversing_passage = p
  map.objs.PassageHubBase = { hub }
  local trig = T.triggers.h7b_exposed
  local cx = ctx()
  trig.prepare(cx)
  local first = trig.when(cx)
  if not stay_in_flight then
    table.remove(p.traversing_colonists, 1)
    c.traversing_passage = false; c.holder = hub; c.passage_hub = hub; at(c, 10, 10)
    if not exposed then c.train = true end
  end
  local ok, f = trig.when(cx)
  hub.connected_passages[p] = nil; hub.connected_passages[sib] = nil
  return first, ok, f, cx, c
end
local first, ok1, f1, _, subj = arrival(true)
row("ARR", "any", "first-poll-silent", "false", first)
row("ARR", "any", "exposed-landing-fires", "true", ok1 and f1.found)
row("ARR", "any", "subject-selected", "true", selected == subj)
local _, ok2, _, cx2 = arrival(false)
row("ARR", "any", "native-true-landing-ignored", "false", ok2)
row("ARR", "any", "rejects-counted", "1", cx2.state.rejects)
advance(24 * 30000 + 1)
local ok3, f3 = T.triggers.h7b_exposed.when(cx2)
row("ARR", "any", "day-timeout", "NOT_SAMPLED", ok3 and f3.verdict)
map.objs.PassageHubBase = {}

------------------------------------------------ C114 slot 3 (fire) and the follow judge
local function fire_case(build, mutate_after_pause)
  set_build(build)
  factor = 0
  local c = subject_on_hub()
  H.paused.c114 = { c = c, hub = hub }
  if mutate_after_pause then c.train = true end
  local before = #T.armed_log
  local ok, why = T.bound[3].fn(ctx())
  local s
  for i = before + 1, #T.armed_log do
    if T.armed_log[i].id == "h7b_follow" then s = T.armed_log[i].arg end
  end
  return ok, why, c, s
end
local okf, _, cf, sf = fire_case("main")
row("FIRE", "main", "fires-and-follows", "true", okf and not cf.workplace and sf ~= nil and sf.exposed)
local okr, whyr = fire_case("main", true)
row("FIRE", "main", "refuses-on-changed-inputs", "false", okr)
factor = 1000
H.paused.c114 = { c = subject_on_hub(), hub = hub }
row("FIRE", "main", "refuses-unpaused", "false", (T.bound[3].fn(ctx())))
factor = 0

local function follow(build, steps)
  local c = subject_on_hub(); c.workplace = false
  local s = { c = c, hub = hub, build = build, exposed = true, fired = true }
  for _, step in ipairs(steps) do step(c) if H.follow_step(s) then break end end
  return H.follow_facts(s, build)
end
local function dump(c) c.holder = false end
local function book(c) c.transport_task = obj { class = "Task", colonist = c, dest_dome = home,
  source_dome = false, migration_dest = false, state = "new" } end
local function ready(c) c.transport_task.state = "ready_for_pickup" end
local function walk_home(c) at(c, 30, 30); c.at_dome = home end
local rescued = { function(c) dump(c); book(c) end, ready }
local walked = { dump, walk_home }
row("C114", "main", "as-predicted", "HELD", follow("main", rescued).verdict)
row("C114", "main", "scratch", "REFUTED", follow("main", walked).verdict)
row("C114", "hubset", "as-predicted", "HELD", follow("hubset", walked).verdict)
row("C114", "hubset", "scratch", "REFUTED", follow("hubset", rescued).verdict)
row("C114", "any", "not-exposed", "NOT_SAMPLED", H.judge.C114("hubset", { exposed = false, fired = true }))

------------------------------------------------ C111 through slot 1
local function slot1(build, tid, text)
  set_build(build); factor = 0
  local c = new_colonist(home); c.command = "Transport"; c.emigration_dome = false
  c.transport_task = obj { class = "Task", colonist = c, dest_dome = home, source_dome = false, migration_dest = false }
  function c:Getui_command() return { id = tid, text = text } end
  map.objs.Colonist = { c }
  local f = T.bound[1].fn(ctx())
  map.objs.Colonist = {}
  return f and f.verdict or f
end
row("C111", "hubset", "as-predicted", "HELD", slot1("hubset", 0, "Returning to Dome: Brussels"))
row("C111", "hubset", "scratch", "REFUTED", slot1("hubset", 4333, "Moving to a new Dome: Brussels"))
row("C111", "main", "as-predicted", "HELD", slot1("main", 4333, "Moving to a new Dome: Brussels"))
row("C111", "main", "scratch", "REFUTED", slot1("main", 0, "Returning to Dome: Brussels"))

------------------------------------------------ C117 busy trigger and slot 5
local function busy_case(n, sibling)
  local h = new_hub(40, 40)
  local p = new_passage(h)
  if sibling then new_passage(h) end
  for i = 1, n do p.traversing_colonists[i] = new_colonist(home) end
  map.objs.PassageHubBase = { h }
  local cx = ctx()
  T.triggers.h7b_busy.prepare(cx)
  local ok, f = T.triggers.h7b_busy.when(cx)
  map.objs.PassageHubBase = {}
  return ok, f, h, p
end
row("BUSY", "any", "five-with-sibling", "true", (busy_case(5, true)))
row("BUSY", "any", "four-with-sibling", "false", (busy_case(4, true)))
row("BUSY", "any", "five-no-sibling", "false", (busy_case(5, false)))

set_build("hubset"); factor = 0
local okb, _, bh, bp = busy_case(6, true)
local runs_before = #T.runs
local ok5 = T.bound[5].fn(ctx())
local last = T.runs[#T.runs]
row("SALV", "hubset", "salvages-at-1x", "true", ok5 and bp.demolishing and #T.runs > runs_before and last.id == "speed" and last.n == 1)
factor = 0
local _, _, bh2, bp2 = busy_case(6, true)
bp2.traversing_colonists = { bp2.traversing_colonists[1] }
row("SALV", "hubset", "refuses-thinned", "false", (T.bound[5].fn(ctx())))

------------------------------------------------ C117 drain judge
local function drain(build, opts)
  local h = new_hub(60, 60)
  local p = new_passage(h)
  local sib = new_passage(h)
  local a, b = new_colonist(home), new_colonist(home)
  p.traversing_colonists = { a, b }
  a.traversing_passage, b.traversing_passage = p, p
  p.demolishing = true
  local s = { p = p, hub = h, build = build, name = "p" }
  H.drain_step(s)                          -- countdown: not draining yet
  local early_speed = s.speed_up
  if opts.cancel then p.demolishing = false; H.drain_step(s); return H.drain_facts(s, build), s end
  p.hub_draining = h
  H.drain_step(s)                          -- drain starts: snapshot a, b
  local speed_once = s.speed_up
  if opts.fresh then
    local late = new_colonist(home); late.traversing_passage = p
    table.insert(p.traversing_colonists, late); H.drain_step(s)
    table.remove(p.traversing_colonists); late.traversing_passage = false
  end
  for _, c in ipairs({ a, b }) do
    c.traversing_passage = false
    if opts.elsewhere then at(c, 1, 1) else at(c, 60, 60) end
    c.holder, c.passage_hub = h, h
  end
  if opts.unmarked then b.holder, b.passage_hub = false, false end
  p.traversing_colonists = {}
  local done = H.drain_step(s)
  local f = H.drain_facts(s, build)
  f.early_speed, f.speed_once, f.done = early_speed, speed_once, done
  return f, s
end
row("C117", "hubset", "as-predicted", "HELD", drain("hubset", {}).verdict)
row("C117", "hubset", "scratch", "REFUTED", drain("hubset", { unmarked = true }).verdict)
row("C117", "main", "as-predicted", "HELD", drain("main", { unmarked = true }).verdict)
row("C117", "main", "scratch", "REFUTED", drain("main", {}).verdict)
row("C117", "any", "no-hub-landing", "NOT_SAMPLED", drain("hubset", { elsewhere = true }).verdict)
row("C117", "any", "cancelled", "salvage cancelled", drain("hubset", { cancel = true }).ended)
local df = drain("hubset", {})
row("C117", "any", "no-speedup-before-drain", "nil", df.early_speed)
row("C117", "any", "speedup-at-drain", "true", df.speed_once)
row("C117", "any", "ends-when-all-landed", "true", df.done)
row("ENTRY", "hubset", "as-predicted", "HELD", drain("hubset", {}).entry_verdict)
row("ENTRY", "hubset", "scratch", "REFUTED", drain("hubset", { fresh = true }).entry_verdict)

------------------------------------------------ load-time contract
row("LOAD", "any", "armed-at-load", "0", T.load_armed)
local n = 0 for k in pairs(T.bound) do n = n + 1 end
row("LOAD", "any", "bindings", "6", n)
local t = 0 for k in pairs(T.triggers) do t = t + 1 end
row("LOAD", "any", "triggers", "4", t)
return rows
'''


def main():
    rt = db.lua_runtime()
    rt.execute(PRELUDE)
    src = db.read(SLOTS)
    db.load_at(rt, src, "=Code/80_AgentSlots.lua")
    g = rt.globals()
    armed_at_load = len(list(g.SMRTK.armed_log.values()))
    g.SMRTK.load_armed = armed_at_load
    rows = rt.execute(SCENARIOS)
    failures = 0
    total = 0
    for i in range(1, len(rows) + 1):
        r = rows[i]
        total += 1
        ok = str(r.expected) == str(r.got)
        failures += 0 if ok else 1
        print("%s %-5s %-7s %-28s expected=%-17s got=%s" % (
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
