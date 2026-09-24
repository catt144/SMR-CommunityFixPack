"""Narrow desk probe for the 1.1.1.405907 metadata SetupEnv bootstrap.

Runs selected shipped Lua function bodies with explicit engine shims. Never reads
or writes the live game, Workshop packages, account storage, or repo code.
"""
from pathlib import Path
from lupa import LuaRuntime

ROOT = Path(r"B:/Dev/SMR/SMR-Shared/SMR-SrcArchive/1.1.1.405907/Src/CommonLua")


def span(rel, first, last):
    lines = (ROOT / rel).read_text(encoding="utf-8").splitlines()
    return "\n".join(lines[first - 1:last])


lua = LuaRuntime(unpack_returned_tuples=True)
lua.execute("""
PropertyObject = {}
InitDone = {}
ModEnvMeta = {}
PersistableGlobals = {}
Loading = true
safe_getmetatable = getmetatable
safe_rawget = rawget
safe_Msg = function() end
safe_OnMsg = {}
dbg = function(value) return value end
CreateModPersistentStorageTable = function() return {} end
g_Classes = {}
-- SetObjPropertyList, class construction and HasMember are the explicit shims.
-- The test checks post-construction per-instance method assignment, not setters.
SetObjPropertyList = function(obj, props)
  for i = 1, #props, 2 do obj[props[i]] = props[i + 1] end
end
""")
lua.execute(span("Modding/Mod.lua", 1280, 1441))
lua.execute("assert(ModEnvBlacklist.AccountStorage and not ModEnvBlacklist.GetModsToLoad)")
lua.execute(span("PropertyObject.lua", 65, 67))
lua.execute(span("PropertyObject.lua", 78, 87))
lua.execute("""
ModDef = { class = 'ModDef', StoreAsTable = false, id = false,
  env = false, content_path = false, options = false,
  HasMember = function(self, key) return self[key] ~= nil end,
  Init = function(self) self.options = {} end,
}
ModDef.__index = ModDef
ModDef.__newindex = PropertyObject.__newindex
setmetatable(ModDef, { __index = PropertyObject })
ModDef.new = InitDone.new
g_Classes.ModDef = ModDef
""")
lua.execute(span("PropertyObject.lua", 1746, 1751))
# The exact shipped __fromluacode and PlaceObj bodies, with the setter shim above.
lua.execute("local SetObjPropertyList = SetObjPropertyList\n" + span("PropertyObject.lua", 1317, 1326))
lua.execute("local delayed_place_objs = {}\n" + span("PropertyObject.lua", 1271, 1295))
# Captures original_G and env_blacklist as the shipped env metatable does.
lua.execute("local original_G = _G\nlocal env_blacklist = ModEnvBlacklist\n"
            + span("Modding/Mod.lua", 1559, 1576))
lua.execute(span("Modding/Mod.lua", 1612, 1626))
lua.execute(span("Modding/Mod.lua", 1628, 1645))
lua.execute(span("Modding/Mod.lua", 1873, 1993) + "\nShippedGetLoadingQueue = GetLoadingQueue")
lua.execute("""
local save_original = ModDef.SetupEnv
ModDef.SetupEnv = function(self)
  original_setup_calls = (original_setup_calls or 0) + 1
  save_original(self)
end

local metadata_env = { PlaceObj = function(class, ...) return PlaceObj(class, ...) end }
local chunk = assert(load([[
  local def = PlaceObj('ModDef', {'id', 'PACK'})
  local original = def.SetupEnv
  def.SetupEnv = function(self)
    original(self)
    local env = self.env
    local prior = env.GetModsToLoad
    env.GetModsToLoad = function(...)
      local queue = prior(...)
      if queue[self.id] then
        for i = 1, #queue do
          if queue[i] == self.id then
            for j = i, 2, -1 do queue[j] = queue[j - 1] end
            queue[1] = self.id
            break
          end
        end
      end
      return queue
    end
  end
  return def
]], '@metadata.lua', 't', metadata_env))

local def = chunk()
assert(def.id == 'PACK')
assert(rawget(def, 'SetupEnv') and def.SetupEnv ~= ModDef.SetupEnv)
assert(not metadata_env.GetModsToLoad)
local a, b = {id = 'A', dependencies = {}}, {id = 'B', dependencies = {}}
rawset(def, 'dependencies', {})
Mods = {A = a, B = b, PACK = def}
local seed = {'A', 'B', 'PACK'}
local before = ShippedGetLoadingQueue(seed, true)
assert(before[1] == 'A' and before[2] == 'B' and before[3] == 'PACK')
assert(before.A == a and before.B == b and before.PACK == def)
local mutant = ShippedGetLoadingQueue(seed, true)
local me = mutant.PACK
for i = 1, #mutant do
  if mutant[i] == me then
    for j = i, 2, -1 do mutant[j] = mutant[j - 1] end
    mutant[1] = me
    break
  end
end
assert(mutant[1] == 'A' and mutant[2] == 'B' and mutant[3] == 'PACK')
print('PASS falsifier: old object comparison fails on shipped string-array queue')
GetModsToLoad = function() return ShippedGetLoadingQueue(seed, true) end
def.env = LuaModEnv()
def.content_path = 'Mod/PACK/'
def:SetupEnv()
assert(original_setup_calls == 1)
assert(def.env.CurrentModId == 'PACK')
assert(rawget(def.env, 'GetModsToLoad') == nil and rawget(_G, 'GetModsToLoad') ~= nil)
local got = GetModsToLoad()
assert(got[1] == 'PACK' and got[2] == 'A' and got[3] == 'B')
assert(got.PACK == def and got.A == a and got.B == b)
print('PASS metadata per-instance SetupEnv overrides and wraps global queue selector')
print('PASS shipped queue numeric IDs PACK,A,B; object hash members preserved')

GetModsToLoad = function() return ShippedGetLoadingQueue({'A', 'B'}, true) end
local disabled_def = chunk()
disabled_def.env = LuaModEnv()
disabled_def.content_path = 'Mod/PACK/'
disabled_def:SetupEnv()
local absent = GetModsToLoad()
assert(absent[1] == 'A' and absent[2] == 'B' and absent[3] == nil)
assert(absent.A == a and absent.B == b and absent.PACK == nil)
print('PASS disabled pack absent from queue: numeric order A,B unchanged')
""")
