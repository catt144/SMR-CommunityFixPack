"""Desk control for a mod reordering its next cold load through shipped public helpers."""

import hashlib
import sys
from pathlib import Path

from lupa import LuaRuntime


REPO = Path.cwd()  # Run from repository root, including the archived copy.
sys.path.insert(0, str(REPO / "tools"))
from luafn import find_bodies  # noqa: E402


ROOT = Path("B:/Dev/SMR/SMR-Shared/SMR-SrcArchive")
SOURCES = (
    ("1.1.0.403908", "CommonLua/Modding/Mod.lua"),
    ("1.1.1.405907", "CommonLua/Modding/Mod.lua"),
)


def shipped_body(lines, pattern):
    hits = find_bodies(lines, pattern)
    assert len(hits) == 1, (pattern, hits)
    first, last = hits[0]
    return "\n" * first + "\n".join(lines[first : last + 1])


for build, relative in SOURCES:
    mod_lines = (ROOT / build / "Src" / relative).read_text(encoding="utf-8").splitlines()
    ui_lines = (ROOT / build / "Src/CommonLua/UI/ModManager.lua").read_text(encoding="utf-8").splitlines()
    lua = LuaRuntime(unpack_returned_tuples=True)
    lua.execute("""
        FirstLoad=true; ModMsgBlacklist={}; Loading=true; PersistableGlobals={}
        const={MaxModDataSize=32768}; IsPStr=function() return false end
        AccountStorage={LoadMods={'B','PACK','C'}, ModPersistentData={}}
        LocalStorage={}; config={}; save_calls=0
        function SaveAccountStorage(delay) save_calls=save_calls+1; last_save_delay=delay end
        function table.icopy(t) local out={} for i,v in ipairs(t) do out[i]=v end return out end
        function table.keys(t, sorted)
            local out={} for k in pairs(t) do out[#out+1]=k end
            if sorted then table.sort(out) end
            return out
        end
        function table.find(t, value)
            for i,v in ipairs(t) do if v==value then return i end end
        end
        function table.insert_unique(t, v) if not table.find(t,v) then table.insert(t,v) end end
        function table.remove_entry(t, v)
            local i=table.find(t,v); if i then table.remove(t,i) end
        end
        function Msg() end
        function ModMessage() end
        function IsUserCreatedContentAllowed() return true end
        function GetModBlacklistedReason() return nil end
        function CreateModPersistentStorageTable() return {} end
        function ReadModPersistentData() end
        function WriteModPersistentStorageTable() end
        Mods={}
        for _,id in ipairs({'A','B','C','PACK'}) do
            Mods[id]={id=id,version=1,dependencies={},code={},entities={},options={},
                GetModLabel=function(self) return self.id end,
                IsTooOld=function() return false end}
        end
        ModsLoaded={Mods.B, Mods.PACK, Mods.C}
    """)

    # The actual blacklist literal and environment machinery, with only unrelated
    # engine services stubbed above. These bodies stay at their archived lines.
    blacklist_start = next(i for i, line in enumerate(mod_lines) if line == "ModEnvBlacklist = {")
    blacklist_end = next(i for i, line in enumerate(mod_lines[blacklist_start + 1 :], blacklist_start + 1) if line == "}")
    blacklist = "\n" * blacklist_start + "\n".join(mod_lines[blacklist_start : blacklist_end + 1])
    lua.execute(blacklist)
    env_start = next(i for i, line in enumerate(mod_lines) if line == "if FirstLoad then" and i > 1450)
    env_end = find_bodies(mod_lines, r"^function LuaModEnv\(env\)")[0][1]
    lua.execute("\n" * env_start + "\n".join(mod_lines[env_start : env_end + 1]))

    # Load the shipped storage writer and SetupEnv in one chunk to keep the
    # writer local, exactly as it is in the game file.
    storage = shipped_body(mod_lines, r"^local function WriteModPersistentData\(mod, data\)")
    setup = shipped_body(mod_lines, r"^function ModDef:SetupEnv\(\)")
    lua.execute("ModDef={}\nlocal max_data_length=const.MaxModDataSize\n" + storage + "\n" + setup)

    for name in ("TurnModOn", "TurnModOff"):
        lua.execute(shipped_body(ui_lines, rf"^function {name}\(id\)"))
    lua.execute(shipped_body(mod_lines, r"^function GetModsEnabledByUser\(\)"))

    queue_start = find_bodies(mod_lines, r"^local function GetModAllDependencies\(mod\)")[0][0]
    queue_end = find_bodies(mod_lines, r"^local function GetLoadingQueue\(list(?:, silent)?\)")[0][1]
    queue_code = "\n" * queue_start + "\n".join(mod_lines[queue_start : queue_end + 1])
    queue = lua.execute(queue_code + "\nreturn GetLoadingQueue")

    lua.execute("mod_env=LuaModEnv(); Mods.PACK.env=mod_env; ModDef.SetupEnv(Mods.PACK)")
    env = lua.globals().mod_env
    assert env.AccountStorage is None
    assert env.SaveAccountStorage is None
    assert lua.eval("type(mod_env.TurnModOff)") == "function"
    assert lua.eval("type(mod_env.TurnModOn)") == "function"
    assert lua.eval("type(mod_env.GetModsEnabledByUser)") == "function"
    assert lua.eval("type(mod_env.WriteModPersistentData)") == "function"
    print(build, "visibility", "AccountStorage", env.AccountStorage,
          "SaveAccountStorage", env.SaveAccountStorage,
          "TurnModOff", lua.eval("type(mod_env.TurnModOff)"),
          "TurnModOn", lua.eval("type(mod_env.TurnModOn)"),
          "WriteModPersistentData", lua.eval("type(mod_env.WriteModPersistentData)"))

    lua.execute("local seed=GetModsEnabledByUser(); table.remove(seed,1); assert(AccountStorage.LoadMods[1]=='B')")

    def result(label, expected_seed, expected_queue, expected_saves):
        seed = lua.eval("GetModsEnabledByUser()")
        selected = ",".join(seed[i] for i in range(1, len(seed) + 1))
        order = queue(seed)
        final = ",".join(order[i] for i in range(1, len(order) + 1))
        loaded = lua.globals().ModsLoaded
        fixed = ",".join(loaded[i].id for i in range(1, len(loaded) + 1))
        assert selected == expected_seed, (build, label, "seed", selected, expected_seed)
        assert final == expected_queue, (build, label, "queue", final, expected_queue)
        assert fixed == "B,PACK,C", (build, label, "current loaded", fixed)
        assert lua.globals().save_calls == expected_saves, (build, label, "save calls", lua.globals().save_calls)
        print(build, label, "seed", selected, "queue", final,
              "current_loaded", fixed, "save_calls", lua.globals().save_calls)

    result("before", "B,PACK,C", "B,PACK,C", 0)
    lua.execute("""
        local prior=GetModsEnabledByUser()
        for _,id in ipairs(prior) do if id ~= CurrentModId then mod_env.TurnModOff(id) end end
        mod_env.TurnModOff(CurrentModId)
        mod_env.TurnModOn(CurrentModId)
        for _,id in ipairs(prior) do if id ~= CurrentModId then mod_env.TurnModOn(id) end end
        assert(mod_env.WriteModPersistentData('loader-probe-v1') == nil)
    """.replace("CurrentModId", "mod_env.CurrentModId"))
    assert lua.globals().AccountStorage.ModPersistentData.PACK == "loader-probe-v1"
    assert lua.globals().last_save_delay == 1000
    result("after helper reorder", "PACK,B,C", "PACK,B,C", 1)
    lua.execute("mod_env.WriteModPersistentData('loader-probe-v1')")
    result("same persistent payload", "PACK,B,C", "PACK,B,C", 1)
    lua.execute("AccountStorage.LoadAllMods=true")
    result("LoadAllMods", "A,B,C,PACK", "A,B,C,PACK", 1)
    lua.execute("AccountStorage.LoadAllMods=false; Mods.PACK.dependencies={{id='A',required=true,ModFits=function() return true end}}; table.insert(AccountStorage.LoadMods,'A')")
    result("own required A prerequisite", "PACK,B,C,A", "A,PACK,B,C", 1)
    queue_digest = hashlib.sha256((queue_code[queue_start:] + "\n").encode()).hexdigest()
    print(build, "PASS 5/5 named states", "helper_queue_sha256", queue_digest)
