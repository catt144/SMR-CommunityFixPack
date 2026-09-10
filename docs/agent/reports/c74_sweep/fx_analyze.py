"""Analysis over census_<tree>.json + literals_<tree>.json (run fx_census.py first)."""
import json, os, re, sys, collections
OUT = os.path.dirname(os.path.abspath(__file__))
tree = sys.argv[1] if len(sys.argv) > 1 else "1.1.0"
C = json.load(open(os.path.join(OUT, "census_%s.json" % tree)))
L = json.load(open(os.path.join(OUT, "literals_%s.json" % tree)))
fx = C["fx"]

GENERIC = {"start", "end", "any", ""}

def lit(s):
    return L.get(s, [])

def near(a_hits, b_hits, win=25):
    res = []
    by = collections.defaultdict(list)
    for f, n, k in b_hits: by[f].append(n)
    for f, n, k in a_hits:
        for m in by.get(f, []):
            if abs(m - n) <= win:
                res.append((f, n, m)); break
    return res

pairs = collections.defaultdict(list)
for e in fx:
    if e["class"] == "ActionFXRemove":
        continue
    pairs[(e["Action"], e["Moment"])].append(e)

moments = collections.Counter(e["Moment"] for e in fx)
print("distinct moments:", len(moments))
rows = []
for (a, m), es in sorted(pairs.items()):
    mh = lit(m); ah = lit(a)
    colo = near(mh, ah) if mh and ah else []
    if m in GENERIC:
        cls = "generic"
    elif colo:
        cls = "colocated"
    elif mh:
        cls = "moment-literal-elsewhere"
    else:
        cls = "no-moment-literal"
    rows.append({"Action": a, "Moment": m, "n": len(es), "cls": cls,
                 "moment_hits": [f"{f}:{n}" for f, n, k in mh[:6]], "n_moment_hits": len(mh),
                 "action_hits": [f"{f}:{n}" for f, n, k in ah[:4]], "n_action_hits": len(ah),
                 "colo": [f"{f}:{n}" for f, n, _ in colo[:3]],
                 "classes": dict(collections.Counter(x["class"] for x in es)),
                 "enabled": sum(1 for x in es if not x.get("Disabled")),
                 "actors": sorted(set(x["Actor"] for x in es)), "targets": sorted(set(x["Target"] for x in es)),
                 "sites": [f'{x["file"].split("/")[-1]}:{x["line"]}' for x in es]})
json.dump({"moments": moments, "rows": rows}, open(os.path.join(OUT, "analysis_%s.json" % tree), "w"), indent=1)
print(collections.Counter(r["cls"] for r in rows))
print("moment counts:", sorted(moments.items(), key=lambda x: -x[1]))
