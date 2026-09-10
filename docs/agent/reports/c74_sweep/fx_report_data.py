"""Tasks 3/5/6 data: tracker attribution, orphan names, tree diff. Run after fx_census.py."""
import json, os, collections
OUT = os.path.dirname(os.path.abspath(__file__))
def load(t):
    return json.load(open(os.path.join(OUT, "census_%s.json" % t))), json.load(open(os.path.join(OUT, "literals_%s.json" % t)))

C, L = load("1.1.0")
cls = C["classes"]; tmpl = {t["id"]: t for t in C["templates"]}; ents = set(C["entities"])

def chain(name, seen=None):
    seen = seen or set()
    if name in seen: return seen
    seen.add(name)
    c = cls.get(name)
    if c:
        for p in c["parents"]: chain(p, seen)
    t = tmpl.get(name)
    if t and t.get("template_class"): chain(t["template_class"], seen)
    return seen

# ---- tracker-using classes -> templates
TRACK = {"ElectrolyzerBase": "Lua/Buildings/Electrolyzer.lua:5 (true -> hit-moment1..2)",
         "MOXIEBase": "Lua/Buildings/MOXIE.lua:5 (true -> hit-moment1..2)",
         "MicroGExtractorBase": "Lua/Buildings/MicroGExtractor.lua:123 ({1,2,3})",
         "PreciousMetalsExtractorBase": "Lua/Buildings/MetalsExtractor.lua:25 ({1,2,3})",
         "PreciousMineralsExtractorBase": "Lua/Buildings/PreciousMineralsExtractor.lua:17 ({1,2,3})"}
print("== tracker classes -> templates (1.1.0)")
tmap = {}
for base, why in TRACK.items():
    ts = sorted(t for t in tmpl if base in chain(t))
    for t in ts: tmap[t] = base
    print(" ", base, "|", why, "| templates:", [(t, tmpl[t].get("entity"), tmpl[t].get("template_class")) for t in ts])
print("== Working hit-moment* entries by tracker building")
for e in C["fx"]:
    if e["Action"] == "Working" and e["Moment"].startswith("hit-moment"):
        a = e["Actor"]
        base = tmap.get(a) or ("(Actor=any: matches every tracker)" if a == "any" else "NONE")
        print(" ", e["file"].split("/")[-1] + ":" + str(e["line"]), e["class"], e["Moment"], "Actor=" + a, "Target=" + e["Target"], "->", base)

# ---- orphan names
SPECIAL = {"any", "ignore", ""}
ACTORCLASSDEF = set()
def known(name, L):
    if name in SPECIAL: return "special"
    if name in cls: return "class"
    if name in tmpl: return "template"
    if name in ents: return "entity"
    hits = [h for h in L.get(name, [])]
    if hits: return "literal:" + "%s:%d" % (hits[0][0], hits[0][1])
    return None

print("== orphan Actor/Target names (1.1.0), non-Remove entries")
orph = collections.defaultdict(list)
for e in C["fx"]:
    for k in ("Actor", "Target"):
        n = e[k]
        if known(n, L) is None:
            orph[(k, n)].append(e)
for (k, n), es in sorted(orph.items()):
    print("  %s=%s n=%d en=%d classes=%s sites=%s actions=%s" % (k, n, len(es), sum(1 for x in es if not x.get("Disabled")),
          dict(collections.Counter(x["class"] for x in es)), [x["file"].split("/")[-1] + ":" + str(x["line"]) for x in es[:3]],
          sorted(set(x["Action"] for x in es))[:4]))
# control: a known-live name must classify as known
for ctrl in ("PreciousMetalsExtractor", "UniversalExtractorHammer", "MOXIE", "MirrorSphere", "Metatron"):
    print("  CONTROL", ctrl, "->", known(ctrl, L))
# control for the orphan method itself: a fabricated name must be reported orphan
print("  CONTROL fabricated 'ZzNoSuchClass' ->", known("ZzNoSuchClass", L))

print("== ActionFXRemove entries (design, not defects)")
for e in C["fx"]:
    if e["class"] == "ActionFXRemove":
        print(" ", e["file"].split("/")[-1] + ":" + str(e["line"]), e["Action"], e["Moment"], "Actor=" + e["Actor"], "Target=" + e["Target"], "FxId=" + str(e.get("FxId")))

# ---- tree diff
C7, L7 = load("1.0.7")
def key(e):
    return (e["class"], e["Action"], e["Moment"], e["Actor"], e["Target"], str(e.get("Sound") or e.get("Particles") or e.get("Object") or e.get("Light") or ""), bool(e.get("Disabled")))
k1 = collections.Counter(key(e) for e in C["fx"]); k7 = collections.Counter(key(e) for e in C7["fx"])
only7 = k7 - k1; only1 = k1 - k7
print("== diff: only in 1.0.7: %d, only in 1.1.0: %d" % (sum(only7.values()), sum(only1.values())))
def summarize(cnt, label):
    by = collections.Counter()
    for k, v in cnt.items(): by[(k[0], k[1])] += v
    print("  ", label, "by (class,Action) top:", by.most_common(25))
summarize(only7, "only-1.0.7")
summarize(only1, "only-1.1.0")
# entries whose identity (class, Action, Moment, Actor, Target, asset) exists in both but Disabled flipped
dis = collections.Counter()
for k in set(k.__class__(k[:-1]) for k in list(only7) + list(only1)):
    a = sum(v for kk, v in only7.items() if kk[:-1] == k); b = sum(v for kk, v in only1.items() if kk[:-1] == k)
    if a and b: dis[k] = (a, b)
print("  identity present in both but multiset differs (Disabled flip or count):", len(dis))
for k, v in list(dis.items())[:20]: print("    ", k, v)
m7 = set(e["Moment"] for e in C7["fx"]); m1 = set(e["Moment"] for e in C["fx"])
print("  moments only 1.0.7:", sorted(m7 - m1), " only 1.1.0:", sorted(m1 - m7))
for e in C7["fx"]:
    if e["Moment"] in (m7 - m1):
        print("    1.0.7", e["file"].split("/")[-1] + ":" + str(e["line"]), e["class"], e["Action"], e["Moment"], e["Actor"], e["Target"], "Dis" if e.get("Disabled") else "")
json.dump({"only7": [list(k) + [v] for k, v in only7.items()], "only1": [list(k) + [v] for k, v in only1.items()]},
          open(os.path.join(OUT, "treediff.json"), "w"), indent=0)
