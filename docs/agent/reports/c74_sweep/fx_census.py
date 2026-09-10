"""FX census for Surviving Mars: Relaunched (read-only over C:/Dev/SMR-SrcArchive).

Loads every ActionFX* preset, AnimMetadata preset and BuildingTemplate with lupa
(a real Lua runtime) using a PlaceObj stub that records (class, props, file, line).
Builds a string-literal index over all non-FX Lua (code + data) for call-site search,
and a DefineClass index (brace-matched) for class existence / parents / entity.

Outputs JSON to <scratch>/census_<tree>.json and prints summaries.
Re-run:  python fx_census.py
"""
import json, os, re, sys, glob, collections
from lupa import LuaRuntime

ARCH = r"C:/Dev/SMR-SrcArchive"
TREES = {"1.1.0": ARCH + "/1.1.0.403908/Src", "1.0.7": ARCH + "/1.0.7.396349/Src"}
OUT = os.path.dirname(os.path.abspath(__file__))

LUA_PRELUDE = r"""
RECORDS = {}
local function norm(t)
  -- PlaceObj props come either as {k=v} or as positional {'k', v, 'k2', v2}
  if type(t) ~= 'table' then return {} end
  local out = {}
  local n = #t
  if n > 0 and n % 2 == 0 and type(t[1]) == 'string' then
    local ok = true
    for i = 1, n, 2 do if type(t[i]) ~= 'string' then ok = false end end
    if ok then
      for i = 1, n, 2 do out[t[i]] = t[i+1] end
      for k, v in pairs(t) do if type(k) ~= 'number' then out[k] = v end end
      return out
    end
  end
  return t
end
function PlaceObj(class, t, ...)
  local info = debug.getinfo(2, 'Sl')
  local o = norm(t)
  o.__class = class
  o.__line = info.currentline
  o.__src = CURFILE
  RECORDS[#RECORDS+1] = o
  return o
end
function point(...) return {__point = {...}} end
function set(...) local s = {} for _, v in ipairs({...}) do s[v] = true end return s end
function T(a, b, ...) if type(a) == 'table' then return a end if b ~= nil then return b end return a end
function range(a, b) return {a, b} end
function RGB(r,g,b) return 0 end
function RGBA(r,g,b,a) return 0 end
function box(...) return {} end
guim = 100; const = setmetatable({}, {__index=function() return 1 end})
setmetatable(_G, {__index = function(_, k) return function(...) return {...} end end})
"""

def new_lua():
    lua = LuaRuntime(unpack_returned_tuples=True)
    lua.execute(LUA_PRELUDE)
    return lua

def lua_to_py(v, depth=0):
    if depth > 6:
        return None
    if hasattr(v, "items") and not isinstance(v, dict):
        d = {}
        for k, x in v.items():
            d[k if isinstance(k, str) else str(k)] = lua_to_py(x, depth + 1)
        return d
    return v

def load_presets(root, files, keep):
    lua = new_lua()
    recs = []
    for f in files:
        rel = os.path.relpath(f, root).replace("\\", "/")
        lua.globals().CURFILE = rel
        lua.globals().RECORDS = lua.table()
        src = open(f, encoding="utf-8-sig", errors="replace").read()
        fn = lua.eval("function(s, name) local f, e = load(s, '@'..name) if not f then error(e) end return f() end")
        fn(src, rel)
        for r in lua.globals().RECORDS.values():
            cls = r["__class"]
            if keep(cls):
                recs.append(lua_to_py(r))
    return recs

FX_KEYS = ["Action", "Moment", "Actor", "Target", "Spot", "Sound", "Particles", "Object", "Light", "FxId",
           "Disabled", "Chance", "GameStatesFilter", "Source", "AttachToObj", "Attach", "EndMoment", "Behavior",
           "Time", "Delay", "Solo", "id", "group", "DetailLevel", "OverrideBaseClass"]

def fx_census(root):
    files = sorted(glob.glob(root + "/Data/FXPreset/*.lua") + glob.glob(root + "/DLC/*/Presets/FXPreset/*.lua"))
    recs = load_presets(root, files, lambda c: c.startswith("ActionFX") and c != "ActionFXEndRule")
    out = []
    for r in recs:
        e = {"file": r["__src"], "line": r["__line"], "class": r["__class"]}
        for k in FX_KEYS:
            if k in r and r[k] is not None:
                v = r[k]
                e[k] = v if isinstance(v, (str, int, float, bool)) else json.dumps(v, default=str)[:80]
        er = r.get("EndRules")
        if er:
            e["EndRules"] = [(x.get("EndAction"), x.get("EndMoment")) for x in er.values()] if isinstance(er, dict) else str(er)
        # PlaceObj defaults (ActionFX props default to "any"; Target "any")
        for k in ("Action", "Moment", "Actor", "Target"):
            e.setdefault(k, "any")
        out.append(e)
    return out

def animmeta(root):
    files = sorted(glob.glob(root + "/Data/AnimMetadata.lua") + glob.glob(root + "/DLC/*/Presets/AnimMetadata.lua"))
    recs = load_presets(root, files, lambda c: c == "AnimMetadata")
    out = []
    for r in recs:
        m = r.get("Moments") or {}
        types = [x.get("Type") for x in m.values()] if isinstance(m, dict) else []
        out.append({"file": r["__src"], "line": r["__line"], "group": r.get("group"), "id": r.get("id"),
                    "moments": types, "FXInherits": r.get("FXInherits")})
    return out

def templates(root):
    files = sorted(glob.glob(root + "/Data/BuildingTemplate/*.lua") + glob.glob(root + "/DLC/*/Presets/BuildingTemplate/*.lua"))
    recs = load_presets(root, files, lambda c: c == "BuildingTemplate")
    out = []
    for r in recs:
        d = {"file": r["__src"], "line": r["__line"], "id": r.get("id"), "template_class": r.get("template_class"),
             "entity": r.get("entity")}
        for k, v in r.items():
            if isinstance(k, str) and re.match(r"entity\d|.*_entity$|palette", k) and isinstance(v, str):
                d[k] = v
        out.append(d)
    return out

# ---------------- Lua source indexes (Python) ----------------
STR_RE = re.compile(r'"((?:[^"\\\n]|\\.)*)"|\'((?:[^\'\\\n]|\\.)*)\'')

def strip_comment(line):
    # remove '--' comments that are not inside a string (approximate but adequate)
    out, i, q = [], 0, None
    while i < len(line):
        c = line[i]
        if q:
            out.append(c)
            if c == "\\":
                if i + 1 < len(line): out.append(line[i + 1]); i += 1
            elif c == q:
                q = None
        else:
            if c in "\"'":
                q = c; out.append(c)
            elif line.startswith("--", i):
                break
            else:
                out.append(c)
        i += 1
    return "".join(out)

def is_fx_data(rel):
    return "/FXPreset/" in rel or rel.endswith("AnimMetadata.lua")

def lua_files(root):
    fs = []
    for sub in ("Lua", "CommonLua", "DLC", "Data"):
        fs += glob.glob(root + "/" + sub + "/**/*.lua", recursive=True)
    return sorted(fs)

def literal_index(root):
    """literal -> list of (rel, line, kind) where kind in code/data; FX preset files and AnimMetadata excluded."""
    idx = collections.defaultdict(list)
    lines_by_file = {}
    for f in lua_files(root):
        rel = os.path.relpath(f, root).replace("\\", "/")
        if is_fx_data(rel):
            continue
        kind = "data" if rel.startswith("Data/") or "/Presets/" in rel else "code"
        try:
            text = open(f, encoding="utf-8-sig", errors="replace").read().split("\n")
        except Exception:
            continue
        lines_by_file[rel] = text
        for n, line in enumerate(text, 1):
            s = strip_comment(line)
            for m in STR_RE.finditer(s):
                v = m.group(1) if m.group(1) is not None else m.group(2)
                idx[v].append((rel, n, kind))
    return idx, lines_by_file

DEF_RE = re.compile(r'^\s*DefineClass\.([A-Za-z_][A-Za-z_0-9]*)\s*=\s*\{|^\s*DefineClass\(\s*"([A-Za-z_][A-Za-z_0-9]*)"(.*)$')
APP_RE = re.compile(r'^\s*AppendClass\.([A-Za-z_][A-Za-z_0-9]*)\s*=')

def brace_block(text, start):
    depth, i, q = 0, start, None
    while i < len(text):
        c = text[i]
        if q:
            if c == "\\": i += 1
            elif c == q: q = None
        elif c in "\"'":
            q = c
        elif text.startswith("--", i):
            j = text.find("\n", i); i = j if j >= 0 else len(text); continue
        elif c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                return text[start:i + 1]
        i += 1
    return text[start:]

def top_field(block, name):
    # string-valued field at nesting depth 1
    depth, i, q = 0, 0, None
    pat = re.compile(r'\b' + name + r'\s*=\s*("([^"]*)"|false|true)')
    while i < len(block):
        c = block[i]
        if q:
            if c == "\\": i += 1
            elif c == q: q = None
        elif c in "\"'": q = c
        elif c == "{": depth += 1
        elif c == "}": depth -= 1
        elif depth == 1 and block.startswith(name, i) and (i == 0 or not (block[i-1].isalnum() or block[i-1] == '_')):
            m = pat.match(block, i)
            if m:
                return m.group(2) if m.group(2) is not None else m.group(1)
        i += 1
    return None

def class_index(root):
    classes = {}
    for f in lua_files(root):
        rel = os.path.relpath(f, root).replace("\\", "/")
        if is_fx_data(rel):
            continue
        text = open(f, encoding="utf-8-sig", errors="replace").read()
        lines = text.split("\n")
        offs = [0]
        for l in lines: offs.append(offs[-1] + len(l) + 1)
        for n, line in enumerate(lines, 1):
            m = DEF_RE.match(line)
            if not m:
                continue
            if m.group(1):
                name = m.group(1)
                start = offs[n - 1] + line.index("{")
                block = brace_block(text, start)
                pm = re.search(r'__parents\s*=\s*\{([^}]*)\}', block)
                parents = re.findall(r'"([^"]+)"', pm.group(1)) if pm else []
                classes.setdefault(name, {"file": rel, "line": n, "parents": parents,
                                          "entity": top_field(block, "entity"),
                                          "fx_actor_class": top_field(block, "fx_actor_class")})
            else:
                name = m.group(2)
                rest = m.group(3)
                parents = re.findall(r'"([^"]+)"', rest.split("{")[0])
                ent = None
                if "{" in rest:
                    block = brace_block(text, offs[n - 1] + line.index("{"))
                    pm = re.search(r'__parents\s*=\s*\{([^}]*)\}', block)
                    if pm: parents = re.findall(r'"([^"]+)"', pm.group(1))
                    ent = top_field(block, "entity")
                classes.setdefault(name, {"file": rel, "line": n, "parents": parents, "entity": ent, "fx_actor_class": None})
    # ClassDef presets (Data/ClassDef-*.lua)
    return classes

def entity_names(root):
    names = set()
    for f in glob.glob(root + "/**/_EntityData*.lua", recursive=True) + glob.glob(root + "/**/EntityData*.lua", recursive=True):
        for m in re.finditer(r'EntityData\["([^"]+)"\]\s*=', open(f, encoding="utf-8-sig", errors="replace").read()):
            names.add(m.group(1))
    return names

def run(tree):
    root = TREES[tree]
    fx = fx_census(root)
    am = animmeta(root)
    bt = templates(root)
    cls = class_index(root)
    ents = sorted(entity_names(root))
    json.dump({"fx": fx, "animmeta": am, "templates": bt, "classes": cls, "entities": ents},
              open(os.path.join(OUT, "census_%s.json" % tree), "w"), indent=0, default=str)
    idx, _ = literal_index(root)
    json.dump({k: v for k, v in idx.items()}, open(os.path.join(OUT, "literals_%s.json" % tree), "w"))
    c = collections.Counter(e["class"] for e in fx)
    print("==", tree, "FX total", len(fx), dict(sorted(c.items())))
    print("   per file", dict(collections.Counter(e["file"] for e in fx)))
    print("   animmeta groups", sorted(collections.Counter(a["group"] for a in am).items()))
    print("   templates", len(bt), "classes", len(cls), "entities", len(ents), "literals", len(idx))
    # CONTROL: 8 sounds + 3 particles targeting UniversalExtractorHammer
    hs = [e for e in fx if e["Target"] == "UniversalExtractorHammer"]
    print("   CONTROL hammer:", collections.Counter(e["class"] for e in hs), [(e["file"].split("/")[-1], e["line"], e["Moment"]) for e in hs])
    return fx

if __name__ == "__main__":
    for t in (sys.argv[1:] or TREES):
        run(t)
