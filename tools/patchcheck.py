#!/usr/bin/env python3
"""After a game patch: one desk command that says none / scoped / full, and why.

Built 2026-09-19 from `docs/agent/reports/GAME_PATCH_INSTRUMENTS.md` (the design
and its 1.0.7 -> 1.1.0 backtest); build record `reports/GAME_PATCH_BUILD_20260919.md`. The
job prompt that runs it is `docs/agent/prompts/perma/GAME_PATCH_PROMPT.md`.

    python tools/patchcheck.py                       # newest older archive -> live install, Code/
    python tools/patchcheck.py --old 1.1.0.403908    # 1.1.0 -> 1.1.0: must say none
    python tools/patchcheck.py --code B:\\Dev\\SMR\\SMR-OptInPack\\Code
    python tools/patchcheck_selftest.py              # the regression test; run it first

It emits ONE block and every count in it. Paste the block; never retype a count.

WHAT EACH SECTION IS (the report's names)
  A      archive status: the new tree's build is archived and the live Src
         matches the archive manifest (EF-075). Not archived -> verdict stop.
  P      fpk parity: every Lua/, CommonLua/ and Data/ file of the new tree ships
         byte-identical in the live Packs/Lua.fpk + Data.fpk (EF-085). Decoded
         in memory; only run when the new tree IS the live build.
  T      changed hand declarations: hand-file declarations whose body or
         signature changed, that were removed, or that moved with a changed
         body; pure moves and additions excluded (the report's 4,710).
  B      base-class structure: a `DefineClass` / `__parents` line changed in a
         file some module pins, requires or cites.
  D1     one-hop dependency hash, per module, harvested from the module text:
           PIN   pinned bodies (`function C:M(`, `C.M = function`,
                 `local o = C.M`, `SetGlobal("X")`, `-- SRC:` selectors)
           REQ   `Require` targets `{class,method}` / `{global}`
           CITE  `path:line` citations -> the enclosing declaration; a Data/ or
                 generated citation -> its file
         statuses identical / body / body+sig / removed / moved / moved+body.
         A move is NOT gone (R-15): the row says where it went.
  ANON   a citation landing OUTSIDE every keyed declaration (a thread body, a
         `MapGameTimeRepeat` callback, file-level code) flags the module whenever
         that file changes (report §3.3: anonymous callbacks have no key).
  D2     the signature of every bare call the module makes, against every hand
         declaration of that name; flagged when no old signature survives.
         Ranked: gone, then incompatible (a leading parameter moved: the F117
         shape), then prefix-compatible (a trailing optional added/dropped).
  D3     D2 restricted to the D13 save-exposed sites (`D13_EXPOSED_SET.md` §2a,
         plus the `Opt_` rows of §2b for the opt-in pack). Each is a FIX row.
  D5     facts whose cited game function changed (`docs/agent/facts/*.md`).
  notes  the Steam announcement for the new version, fetched. ESCALATION ONLY:
         a note may add a module to the read list (with the line and the term)
         and so raise the verdict; it never drops a module or lowers a verdict.
         A failed fetch prints `notes: not fetched` and the run goes on.

THE VERDICT (report §2 as ruled by the owner 2026-09-18/19)
  stop    A not archived
  none    M empty, D3 empty, B empty, P holds (or n/a)
  scoped  0 < |M| <= 12, B empty, T <= 1000, P holds
  full    |M| > 12, or B not empty, or P broken, or T > 1000
  M = D1 or ANON or D2 flagged modules, then notes additions.
  ⛔ 12 and 1,000 are BUDGET DEFAULTS, not measurements. The tool reproduces
  the 1.1.0 backtest; the small-patch regime is uncalibrated until the first
  real patch. Do not quote a verdict as a calibrated one.

WHAT IT CANNOT SEE (report §4): two hops out, dynamic dispatch, `Msg` fan-out,
semantics with no text change near anything a module names, C-side behaviour,
played state. A `none` certifies the one-hop neighbourhood of what the pack
names and nothing outside it.
"""
import argparse, collections, datetime, hashlib, html, io, json, os, re, struct, subprocess, sys
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from luafn import read_lines                                   # noqa: E402
from treediff import declarations, tree_files, bucket, bare_name  # noqa: E402

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARCHIVE = os.environ.get("SMR_SRC_ARCHIVE", r"B:\Dev\SMR\SMR-Shared\SMR-SrcArchive")
ACF = os.environ.get("SMR_ACF", r"A:\SteamLibrary\steamapps\appmanifest_3215050.acf")
INSTALL = os.environ.get("SMR_INSTALL", r"A:\SteamLibrary\steamapps\common\Project Spark")
APPID = "3215050"
NEWS = ("https://api.steampowered.com/ISteamNews/GetNewsForApp/v2/"
        "?appid=%s&count=30&maxlength=0&format=json" % APPID)
D13 = os.path.join(REPO, "docs", "agent", "reports", "D13_EXPOSED_SET.md")
FACTS = os.path.join(REPO, "docs", "agent", "facts")

SCOPED_MAX_MODULES = 12      # owner ruling 2026-09-18/19: a budget default
FULL_MIN_T = 1000            # owner ruling 2026-09-18/19: a budget default
NOTES_TERM_MAX_MODULES = 5   # a notes term shared by more modules is too generic to route
NOTES_WORD_MAX_CLASSES = 5   # a one-word term in more game class names is too generic to route

KEYWORDS = set("and break do else elseif end false for function if in local nil not or repeat "
               "return then true until while".split())
NOISE_CALLS = set("pairs ipairs type tostring tonumber print assert error pcall rawget rawset next "
                  "select unpack setmetatable getmetatable table string math Max Min abs".split())

RE_CM = re.compile(r'\{\s*class\s*=\s*"([A-Za-z_]\w*)"\s*,\s*method\s*=\s*"([A-Za-z_]\w*)"')
RE_G = re.compile(r'\{\s*global\s*=\s*"([A-Za-z_]\w*)"')
RE_SETG = re.compile(r'SetGlobal\(\s*"([A-Za-z_]\w*)"')
RE_DEF = re.compile(r'^\s*function\s+([A-Za-z_]\w*)(?:[.:]([A-Za-z_]\w*))?\s*\(', re.M)
RE_WRAPASSIGN = re.compile(r'^\s*([A-Z]\w*)\.([A-Za-z_]\w*)\s*=\s*function\b', re.M)
RE_WRAPSAVE = re.compile(r'^\s*local\s+\w+\s*=\s*([A-Z]\w*)\.([A-Za-z_]\w*)\s*$', re.M)
RE_ALIAS = re.compile(r'^\s*local\s+([A-Z]\w*)\s*=\s*(?:rawget\(\s*_G\s*,\s*"([A-Z]\w*)"\s*\)|([A-Z]\w*))\s*$', re.M)
RE_SRC = re.compile(r'--\s*SRC:\s+((?:Lua|CommonLua|Data)/\S+\.lua)\s+(\S+)\s+sha256=')
RE_CITE = re.compile(r'((?:Lua|CommonLua|Data)[\\/][\w\\/ .\-]+?\.lua):(\d+)(?:-(\d+))?')
RE_CITE_BARE = re.compile(r'(?<![\w\\/])([A-Z][\w\- ]*?\.lua):(\d+)(?:-(\d+))?')
RE_CALL = re.compile(r'(?<![\w.])([A-Za-z_]\w*)\s*\(|[.:]([A-Za-z_]\w*)\s*\(')
RE_STRUCT = re.compile(r'^\s*(DefineClass\b|__parents\b)')


# --------------------------------------------------------------------------- #
# trees
# --------------------------------------------------------------------------- #
def resolve_tree(arg):
    """A version folder name under the archive, or a path to a Src directory."""
    if os.path.isdir(os.path.join(ARCHIVE, arg, "Src")):
        return os.path.join(ARCHIVE, arg, "Src")
    if os.path.isdir(arg):
        return os.path.abspath(arg)
    raise SystemExit("patchcheck: no tree at %r (neither %s\\<version>\\Src nor a directory)" % (arg, ARCHIVE))


def archived_versions():
    out = []
    if os.path.isdir(ARCHIVE):
        for v in os.listdir(ARCHIVE):
            if re.match(r"^\d+(\.\d+)+$", v) and os.path.isfile(os.path.join(ARCHIVE, v, "MANIFEST.sha256")):
                out.append(v)
    return sorted(out, key=lambda v: tuple(int(x) for x in v.split(".")))


def manifest_body(root):
    """The archive README's manifest recipe, byte for byte."""
    rows = []
    for dp, _d, fns in os.walk(root):
        for fn in sorted(fns):
            p = os.path.join(dp, fn)
            with open(p, "rb") as fh:
                h = hashlib.sha256(fh.read()).hexdigest()
            rows.append("%s  %s" % (h, os.path.relpath(p, root).replace("\\", "/")))
    rows.sort(key=lambda r: r.split("  ", 1)[1])
    return "\n".join(rows) + "\n"


def tree_version(root):
    """The version a tree claims: its archive folder name, else None."""
    parent = os.path.basename(os.path.dirname(os.path.abspath(root)))
    return parent if re.match(r"^\d+(\.\d+)+$", parent) else None


def installed_build():
    try:
        with open(ACF, encoding="utf-8", errors="replace") as fh:
            hit = re.search(r'"buildid"\s+"(\d+)"', fh.read())
        return hit.group(1) if hit else None
    except OSError:
        return None


def index(root):
    """(file, key) -> dict(hash, sig, span, line) over non-DLC .lua; plus lines per file."""
    idx, lines_map = {}, {}
    for rel, p in sorted(tree_files(root).items()):
        if not rel.endswith(".lua") or bucket(rel) == "dlc":
            continue
        lines = read_lines(p)
        lines_map[rel] = lines
        for d in declarations(lines, indented=True):
            idx[(rel, d["key"])] = dict(hash=d["hash"], sig=d["sig"], span=d["span"], line=d["line"])
    return idx, lines_map


def file_hashes(root):
    out = {}
    for rel, p in tree_files(root).items():
        if rel.startswith("DLC/"):
            continue
        with open(p, "rb") as fh:
            out[rel] = hashlib.sha256(fh.read().replace(b"\r\n", b"\n")).hexdigest()
    return out


class Compare:
    """Both trees indexed once; every instrument reads from here."""

    def __init__(self, old_root, new_root, overlay=None, base=None):
        """`base`: another Compare over the same two roots whose indexes are reused."""
        self.old_root, self.new_root, self.overlay = old_root, new_root, overlay
        if base is not None:
            self.raw = base.raw
        else:
            self.raw = (index(old_root), index(new_root), file_hashes(old_root), file_hashes(new_root))
        (self.old, self.oldlines), (self.new, self.newlines), oldf, newf = self.raw
        if overlay is not None:
            # SYNTHETIC control: the old tree everywhere except the named files,
            # which take their new content; an empty set is the identity control.
            # Say "synthetic" wherever its numbers are quoted.
            real_new, real_newlines, real_newf = self.new, self.newlines, newf
            self.new = {rk: d for rk, d in self.old.items() if rk[0] not in overlay}
            self.new.update({rk: d for rk, d in real_new.items() if rk[0] in overlay})
            self.newlines = {r: l for r, l in self.oldlines.items() if r not in overlay}
            self.newlines.update({r: real_newlines[r] for r in overlay if r in real_newlines})
            newf = {r: h for r, h in oldf.items() if r not in overlay}
            newf.update({r: h for r, h in real_newf.items() if r in overlay})
        self.file_changed = {}
        for rel in set(oldf) | set(newf):
            if rel not in oldf:
                self.file_changed[rel] = "added"
            elif rel not in newf:
                self.file_changed[rel] = "removed"
            else:
                self.file_changed[rel] = "changed" if oldf[rel] != newf[rel] else "identical"
        self._statuses()

    def _statuses(self):
        self.old_bykey = collections.defaultdict(list)
        for rk in self.old:
            self.old_bykey[rk[1].split("#")[0]].append(rk)
        self.new_bykey = collections.defaultdict(list)
        for rk in self.new:
            self.new_bykey[rk[1].split("#")[0]].append(rk)
        self.basenames = collections.defaultdict(list)
        for rel in set(self.oldlines) | set(self.newlines):
            self.basenames[rel.rsplit("/", 1)[-1]].append(rel)
        # status per OLD declaration; a key gone from its file but present in
        # another is `moved` (same hash) or `moved+body` -- never "removed".
        self.status, self.moved_to = {}, {}
        for rk, d in self.old.items():
            n = self.new.get(rk)
            if n is None:
                alt = [a for a in self.new_bykey.get(rk[1].split("#")[0], []) if a[0] != rk[0]]
                if alt:
                    same = [a for a in alt if self.new[a]["hash"] == d["hash"]]
                    self.status[rk] = "moved" if same else "moved+body"
                    self.moved_to[rk] = (same or alt)[0]
                else:
                    self.status[rk] = "removed"
            elif n["hash"] == d["hash"]:
                self.status[rk] = "identical"
            elif n["sig"] != d["sig"]:
                self.status[rk] = "body+sig"
            else:
                self.status[rk] = "body"
        self.added = [rk for rk in self.new if rk not in self.old]
        self.old_sigs = collections.defaultdict(set)
        for (rel, k), d in self.old.items():
            if bucket(rel) == "hand":
                self.old_sigs[bare_name(k)].add(d["sig"])
        self.new_sigs = collections.defaultdict(set)
        for (rel, k), d in self.new.items():
            if bucket(rel) == "hand":
                self.new_sigs[bare_name(k)].add(d["sig"])
        self.spans_by_file = collections.defaultdict(list)
        for (r, k), d in self.old.items():
            self.spans_by_file[r].append((d["span"], (r, k)))

    def enclosing(self, rel, line):
        best = None
        for (s, e), rk in self.spans_by_file.get(rel, ()):
            if s <= line - 1 <= e and (best is None or (e - s) < best[1]):
                best = (rk, e - s)
        return best[0] if best else None

    def where(self, rk):
        """`old file:line -> new file:line` for a declaration row."""
        o = "%s:%d" % (rk[0], self.old[rk]["line"])
        st = self.status[rk]
        if st == "removed":
            return o + " -> (none)"
        nk = self.moved_to.get(rk, rk)
        return "%s -> %s:%d" % (o, nk[0], self.new[nk]["line"])

    def sig_note(self, rk):
        if "sig" not in self.status[rk] and self.status[rk] != "moved+body":
            return ""
        nk = self.moved_to.get(rk, rk)
        o, n = self.old[rk]["sig"], self.new[nk]["sig"]
        return "" if o == n else " (%s)->(%s)" % (o, n)

    def counts(self):
        st = collections.Counter(self.status.values())
        hand = collections.Counter(s for rk, s in self.status.items() if bucket(rk[0]) == "hand")
        hand_added = sum(1 for rk in self.added if bucket(rk[0]) == "hand")
        # T, the report's definition (§2: 4,710 on 1.0.7 -> 1.1.0): body or signature
        # changed, removed, or moved with a changed body; pure moves and additions excluded
        t = hand["body"] + hand["body+sig"] + hand["removed"] + hand["moved+body"]
        fc = collections.Counter(self.file_changed.values())
        return st, hand, hand_added, t, fc


# --------------------------------------------------------------------------- #
# modules
# --------------------------------------------------------------------------- #
def strip_lua_comments(text):
    out, i, n = [], 0, len(text)
    while i < n:
        if text.startswith("--", i):
            m = re.match(r"--\[(=*)\[", text[i:i + 8])
            if m:
                close = "]" + m.group(1) + "]"
                j = text.find(close, i)
                i = n if j < 0 else j + len(close)
            else:
                j = text.find("\n", i)
                i = n if j < 0 else j
            out.append("\n")
            continue
        out.append(text[i])
        i += 1
    return "".join(out)


def call_names(code):
    names = set()
    for line in code.splitlines():
        for a, b in RE_CALL.findall(line):
            n = a or b
            if n and n not in KEYWORDS and n not in NOISE_CALLS:
                names.add(n)
    return names


def harvest(path):
    raw = open(path, "rb").read().decode("utf-8", "replace")
    code = strip_lua_comments(raw)
    alias = {a: (g or c) for a, g, c in RE_ALIAS.findall(code)}

    def q(c, m):
        return alias.get(c, c) + "." + m
    pins, reqs = set(), set()
    for c, m in RE_CM.findall(code):
        reqs.add(c + "." + m)
    reqs.update(RE_G.findall(code))
    pins.update(RE_SETG.findall(code))
    for c, m in RE_DEF.findall(code):
        pins.add(q(c, m) if m else c)
    for c, m in RE_WRAPASSIGN.findall(code) + RE_WRAPSAVE.findall(code):
        pins.add(q(c, m))
    for _f, sel in RE_SRC.findall(raw):
        pins.add(sel.replace(":", "."))

    def ours(t):
        return t.startswith(("SMRFixPack", "OnMsg", "SMRTest"))
    pins = {t for t in pins if not ours(t)}
    reqs = {t for t in reqs if not ours(t) and t not in pins}
    cites = set()
    for f, a, b in RE_CITE.findall(raw):
        cites.add((f.replace("\\", "/"), int(a), int(b) if b else int(a)))
    bare = set()
    for f, a, b in RE_CITE_BARE.findall(raw):
        bare.add((f, int(a), int(b) if b else int(a)))
    # Calls to a name the module binds itself are KEPT: a module-local copy of a
    # vanilla file-local (PayloadTemplateRefill's resolve_loc_cargo_template) is
    # the stale-copy FIX signal, and a filter on locals loses it (measured
    # 2026-09-19: §3.1 SIGCALL FIX 3 -> 2). The price is a false match such as
    # CloggedBuildingRelease's `local setter`; a D2 read settles those.
    return dict(pins=pins, reqs=reqs, cites=cites, bare=bare, calls=call_names(code))


def module_files(code_dir):
    return sorted(f for f in os.listdir(code_dir) if f.endswith(".lua") and f != "00_Core.lua")


def module_name(fn):
    return re.sub(r"^(Fix_|Opt_)", "", fn[:-4])


def sig_class(old, new):
    """D2 rank for one call name whose old signatures all vanished."""
    if not new:
        return "gone"
    for o in old:
        for n in new:
            op, np_ = [p for p in o.split(",") if p], [p for p in n.split(",") if p]
            k = min(len(op), len(np_))
            if op[:k] == np_[:k]:
                return "prefix-compatible"
    return "incompatible"


RANK = {"gone": 0, "incompatible": 1, "prefix-compatible": 2}


def analyse(cmp, code_dir):
    """-> list of per-module dicts with every flagged row."""
    rows = []
    for fn in module_files(code_dir):
        h = harvest(os.path.join(code_dir, fn))
        r = dict(file=fn, module=module_name(fn), pins=sorted(h["pins"]), reqs=sorted(h["reqs"]),
                 PIN=[], REQ=[], CITE=[], ANON=[], SIGCALL=[], pin_unresolved=[], files=set())
        for kind in ("pins", "reqs"):
            col = "PIN" if kind == "pins" else "REQ"
            for t in sorted(h[kind]):
                hits = cmp.old_bykey.get(t, [])
                if not hits and kind == "pins":
                    r["pin_unresolved"].append(t)
                for rk in hits:
                    r["files"].add(rk[0])
                    st = cmp.status[rk]
                    if st in ("identical", "moved"):
                        continue
                    r[col].append("%s  %s%s  %s" % (t, st, cmp.sig_note(rk), cmp.where(rk)))
        cites = set(h["cites"])
        for f, a, b in h["bare"]:
            rels = cmp.basenames.get(f, [])
            if len(rels) == 1:
                cites.add((rels[0], a, b))
        seen, anon_files = set(), set()
        for f, a, _b in sorted(cites):
            fc = cmp.file_changed.get(f)
            if fc is None:
                continue
            r["files"].add(f)
            if f.startswith("Data/") or bucket(f) == "generated":
                if fc != "identical":
                    r["CITE"].append("%s  file %s  (cited :%d)" % (f, fc, a))
                continue
            enc = cmp.enclosing(f, a)
            if enc is None:
                if f.endswith(".lua") and f not in anon_files:
                    anon_files.add(f)
                    if fc != "identical":
                        r["ANON"].append("%s  file %s  (cited :%d is outside every keyed declaration)" % (f, fc, a))
                continue
            if enc in seen:
                continue
            seen.add(enc)
            st = cmp.status[enc]
            if st not in ("identical", "moved"):
                r["CITE"].append("%s  %s%s  %s  (cited :%d)" % (enc[1], st, cmp.sig_note(enc), cmp.where(enc), a))
        for n in sorted(h["calls"]):
            if n not in cmp.old_sigs:
                continue
            o, nw = cmp.old_sigs[n], cmp.new_sigs.get(n, set())
            if o & nw:
                continue
            cls = sig_class(o, nw)
            r["SIGCALL"].append((RANK[cls], n, cls, "|".join("(%s)" % s for s in sorted(o)),
                                 "|".join("(%s)" % s for s in sorted(nw)) or "(none)"))
        r["SIGCALL"].sort()
        r["D1"] = bool(r["PIN"] or r["REQ"] or r["CITE"])
        r["flagged"] = bool(r["D1"] or r["ANON"] or r["SIGCALL"])
        rows.append(r)
    return rows


# --------------------------------------------------------------------------- #
# D3, B, D5, parity, notes
# --------------------------------------------------------------------------- #
def d3_sites():
    """Module -> E/D id, parsed from D13_EXPOSED_SET.md each run (never a copy)."""
    sites, section = {}, None
    try:
        text = open(D13, encoding="utf-8").read().splitlines()
    except OSError:
        return None
    for line in text:
        if line.startswith("### 2a."):
            section = "2a"
        elif line.startswith("### 2b."):
            section = "2b"
        elif line.startswith("### ") or line.startswith("## "):
            section = None
        m = re.match(r"^\|\s*([ED]\d+)\s*\|\s*(?:FP|OP)\s*`((?:Fix_|Opt_)?\w+)`", line)
        if m and section and (section == "2a" or m.group(2).startswith("Opt_")):
            mod = module_name(m.group(2) + ".lua")
            sites.setdefault(mod, [])
            if m.group(1) not in sites[mod]:
                sites[mod].append(m.group(1))
    return sites


def structure_rows(cmp, files):
    out = []
    for rel in sorted(files):
        if not rel.endswith(".lua") or cmp.file_changed.get(rel) in (None, "identical"):
            continue
        a = [l.strip() for l in cmp.oldlines.get(rel, []) if RE_STRUCT.match(l)]
        b = [l.strip() for l in cmp.newlines.get(rel, []) if RE_STRUCT.match(l)]
        if collections.Counter(a) != collections.Counter(b):
            gone = sorted((collections.Counter(a) - collections.Counter(b)).elements())
            came = sorted((collections.Counter(b) - collections.Counter(a)).elements())
            out.append((rel, gone, came))
    return out


def facts_moved(cmp):
    n_facts = n_cited = 0
    flagged = []
    if not os.path.isdir(FACTS):
        return None
    for fn in sorted(os.listdir(FACTS)):
        if not fn.endswith(".md") or fn == "INDEX.md":
            continue
        n_facts += 1
        raw = open(os.path.join(FACTS, fn), encoding="utf-8", errors="replace").read()
        cites = set((f.replace("\\", "/"), int(a)) for f, a, _b in RE_CITE.findall(raw))
        for f, a, _b in RE_CITE_BARE.findall(raw):
            rels = cmp.basenames.get(f, [])
            if len(rels) == 1:
                cites.add((rels[0], int(a)))
        fns = {cmp.enclosing(f, a) for f, a in cites if f in cmp.oldlines} - {None}
        if not fns:
            continue
        n_cited += 1
        moved = sorted(rk[1] for rk in fns if cmp.status[rk] not in ("identical", "moved"))
        if moved:
            flagged.append((fn[:-3], moved))
    return n_facts, n_cited, flagged


def fpk_entries(path):
    """-> {path: bytes} for every file entry in an FLPK pack, decoded in memory."""
    import zstandard
    from flpk_extract import parse_table
    buf = open(path, "rb").read()
    if buf[:4] != b"FLPK":
        raise ValueError("%s: not an FLPK pack" % path)
    dir_off = struct.unpack_from("<I", buf, 0x0C)[0]
    dir_size = struct.unpack_from("<I", buf, 0x14)[0]
    files = []
    parse_table(buf, dir_off, dir_size, dir_off, "", files)
    dctx, out = zstandard.ZstdDecompressor(), {}
    for rel, flags, off, size in files:
        if flags == 0x10:
            data = buf[off:off + size]
        elif flags == 0x30:
            region = buf[off:off + size]
            want = struct.unpack_from("<I", region, 4)[0]
            hdrlen = struct.unpack_from("<I", region, 12)[0]
            nb = (hdrlen - 16) // 4
            starts = [hdrlen] + list(struct.unpack_from("<%dI" % nb, region, 16)) if nb else [hdrlen]
            parts = []
            for s, e in zip(starts, starts[1:] + [len(region)]):
                blob = region[s:e]
                parts.append(dctx.stream_reader(io.BytesIO(blob)).read() if blob[:4] == b"\x28\xb5\x2f\xfd" else blob)
            data = b"".join(parts)[:want]
        else:
            continue
        out[rel.replace("\\", "/")] = data
    return out


def parity(new_root):
    """EF-085's measurement: exact-path entries of Lua.fpk + Data.fpk vs the new tree."""
    # Lua.fpk carries Src-relative paths; Data.fpk's entries are relative to Data/
    packs = {"Lua.fpk": (("Lua/", "CommonLua/"), ""), "Data.fpk": (("Data/",), "Data/")}
    src = tree_files(new_root)
    res, revision = [], None
    for pack, (prefixes, root) in packs.items():
        path = os.path.join(INSTALL, "Packs", pack)
        ent = {root + k: v for k, v in fpk_entries(path).items()}
        if "Lua/Config/_LuaRevision.lua" in ent:
            revision = ent["Lua/Config/_LuaRevision.lua"].decode("utf-8", "replace")
        want = {r: p for r, p in src.items() if r.startswith(prefixes)}
        same = diverge = absent = 0
        bad = []
        for rel, p in sorted(want.items()):
            if rel not in ent:
                absent += 1
                bad.append("absent " + rel)
                continue
            if open(p, "rb").read() == ent[rel]:
                same += 1
            else:
                diverge += 1
                bad.append("divergent " + rel)
        res.append((pack, len(want), same, diverge, absent, bad))
    return res, revision


def live_version():
    """BuildVersion from the live Lua.fpk's _LuaRevision.lua (EF-085's control)."""
    try:
        ent = fpk_entries(os.path.join(INSTALL, "Packs", "Lua.fpk"))
        m = re.search(r"BuildVersion\s*=\s*'([^']+)'", ent["Lua/Config/_LuaRevision.lua"].decode("utf-8", "replace"))
        return m.group(1) if m else None
    except (OSError, KeyError, ValueError, ImportError):
        return None


def fetch_notes(version):
    """-> (title, date, text) of the announcement naming `version`, or raise."""
    short = ".".join(version.split(".")[:3])
    req = urllib.request.Request(NEWS, headers={"User-Agent": "patchcheck"})
    with urllib.request.urlopen(req, timeout=20) as fh:
        items = json.load(fh)["appnews"]["newsitems"]
    hits = [i for i in items if i.get("feedname") == "steam_community_announcements"
            and re.search(r"(?<![\d.])%s(?![\d])" % re.escape(short), i.get("title", "") + " " + i.get("contents", "")[:400])]
    if not hits:
        return None
    it = sorted(hits, key=lambda i: i["date"])[-1]
    text = re.sub(r"\[/?[a-z0-9*]+(=[^\]]*)?\]", " ", it.get("contents", ""))
    text = html.unescape(re.sub(r"<[^>]+>", " ", text))
    day = datetime.datetime.fromtimestamp(it["date"], datetime.timezone.utc).strftime("%Y-%m-%d")
    return it.get("title", ""), day, text


def words(ident):
    return [w.lower() for w in re.findall(r"[A-Z]+(?![a-z])|[A-Z]?[a-z]+|\d+", ident)]


def class_word_df(cmp):
    """How many of the new tree's class/global names contain each CamelCase word."""
    names = {k.split("@")[0].split("#")[0].split(".")[0] for (_r, k) in cmp.new}
    return collections.Counter(w for n in names for w in set(words(n)))


def notes_terms(rows, class_df):
    """Per module, the phrases a player-facing note could use for what it names.

    A phrase of two or more words routes; a single word routes only when it is
    specific: in at most NOTES_WORD_MAX_CLASSES game class names ('habitat',
    'sinkhole' yes; 'building', 'service', 'residence' no). A phrase shared by
    more than NOTES_TERM_MAX_MODULES of our modules routes nowhere."""
    terms = {}
    for r in rows:
        ts = set()
        for t in r["pins"] + r["reqs"] + [r["module"]]:
            for part in t.split("."):
                w = words(part)
                if len(w) >= 2:
                    ts.add(" ".join(w))
                elif len(w) == 1 and len(w[0]) >= 5 and class_df.get(w[0], 0) <= NOTES_WORD_MAX_CLASSES:
                    ts.add(w[0])
        terms[r["module"]] = ts
    df = collections.Counter(t for ts in terms.values() for t in ts)
    return {m: {t for t in ts if df[t] <= NOTES_TERM_MAX_MODULES} for m, ts in terms.items()}


def notes_hits(rows, text, class_df):
    flat = re.sub(r"\s+", " ", text)
    hits = {}
    for mod, ts in notes_terms(rows, class_df).items():
        for t in sorted(ts):
            rx = re.compile(r"\b%ss?\b" % r"[\s\-]?".join(re.escape(w) for w in t.split()), re.I)
            m = rx.search(flat)
            if m:
                a, b = max(0, m.start() - 70), min(len(flat), m.end() + 70)
                hits.setdefault(mod, []).append((t, "…" + flat[a:b].strip() + "…"))
    return hits


# --------------------------------------------------------------------------- #
# verdict and the block
# --------------------------------------------------------------------------- #
def verdict(archived, parity_ok, m_count, d3_count, b_count, t):
    if archived is False:
        return "stop", ["A: the new build is not archived (WORKFLOW.md step 0, EF-075)"]
    why = []
    if m_count > SCOPED_MAX_MODULES:
        why.append("|M| = %d > %d" % (m_count, SCOPED_MAX_MODULES))
    if b_count:
        why.append("B = %d" % b_count)
    if parity_ok is False:
        why.append("P broken")
    if t > FULL_MIN_T:
        why.append("T = %d > %d" % (t, FULL_MIN_T))
    if why:
        return "full", why
    if m_count or d3_count:
        return "scoped", ["|M| = %d (<= %d), D3 = %d, B = 0, T = %d" % (m_count, SCOPED_MAX_MODULES, d3_count, t)]
    return "none", ["M = 0, D3 = 0, B = 0, T = %d" % t]


def git_head():
    try:
        return subprocess.run(["git", "-C", REPO, "rev-parse", "--short", "HEAD"], capture_output=True,
                              text=True, check=True).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return "(no git)"


def run(args, out=print, cmp=None):
    versions = archived_versions()
    live_src = os.path.join(INSTALL, "ModTools", "Src")
    new_root = resolve_tree(args.new) if args.new else live_src
    is_live = os.path.normcase(os.path.abspath(new_root)) == os.path.normcase(os.path.abspath(live_src))
    lv = live_version() if (is_live or not args.no_parity) else None
    new_ver = tree_version(new_root) or (lv if is_live else None)
    if args.old:
        old_root = resolve_tree(args.old)
    else:
        below = [v for v in versions if new_ver and tuple(map(int, v.split("."))) < tuple(map(int, new_ver.split(".")))]
        if not below:
            raise SystemExit("patchcheck: no archived build older than %s; pass --old" % new_ver)
        old_root = os.path.join(ARCHIVE, below[-1], "Src")
    old_ver = tree_version(old_root)

    # A: the new build is archived, and (for the live tree) the live Src is that archive
    archived, a_line = None, ""
    if new_ver and new_ver in versions:
        man = open(os.path.join(ARCHIVE, new_ver, "MANIFEST.sha256"), "rb").read().decode("utf-8")
        digest = hashlib.sha256(man.encode()).hexdigest()
        if is_live:
            same = manifest_body(live_src) == man
            archived = same
            a_line = ("archived: live Src == %s\\MANIFEST.sha256 (digest %s…)" % (new_ver, digest[:16]) if same else
                      "NOT archived: live Src differs from the %s archive manifest" % new_ver)
        else:
            archived, a_line = True, "archived: %s (digest %s…)" % (new_ver, digest[:16])
    elif is_live:
        archived, a_line = False, "NOT archived: live build %s has no folder under %s" % (new_ver, ARCHIVE)
    else:
        a_line = "n/a: the new tree is a directory, not an archived build"

    head = git_head()
    out("== patchcheck · %s · fix pack HEAD %s ==" % (datetime.date.today().isoformat(), head))
    out("command: python tools/patchcheck.py %s" % " ".join(sys.argv[1:] if args.argv is None else args.argv))
    out("old: %s  %s" % (old_ver or "(dir)", old_root))
    out("new: %s  %s%s" % (new_ver or "(dir)", new_root,
                           ("  [live install, Steam build %s]" % installed_build()) if is_live else ""))
    if args.overlay is not None:
        out("⚠️ SYNTHETIC OVERLAY: the old tree except %s at new content" % (",".join(sorted(args.overlay)) or "nothing (identity)"))
    out("A %s" % a_line)
    if archived is False:
        v, why = verdict(False, None, 0, 0, 0, 0)
        out("verdict: STOP — %s" % why[0])
        return dict(verdict=v)

    # P
    parity_ok, p_lines = None, []
    same_build = new_ver is not None and lv is not None and new_ver == lv
    if args.no_parity:
        p_lines.append("P not run (--no-parity)")
    elif not same_build or args.overlay is not None:
        p_lines.append("P n/a: the new tree (%s) is not the live build (%s)" % (new_ver, lv))
    else:
        try:
            res, rev = parity(new_root)
            parity_ok = all(d == 0 and a == 0 for _p, _n, _s, d, a, _b in res)
            p_lines.append("P %s — %s" % ("holds" if parity_ok else "BROKEN", "; ".join(
                "%s %d/%d byte-identical, %d divergent, %d absent" % (p, s, n, d, a) for p, n, s, d, a, _b in res)))
            for p, _n, _s, _d, _a, bad in res:
                for b in bad[:20]:
                    p_lines.append("  %s  %s" % (p, b))
        except Exception as e:                       # noqa: BLE001 -- a parity failure must not kill the run
            parity_ok = False
            p_lines.append("P BROKEN: could not read the packs (%s)" % e)
    for l in p_lines:
        out(l)

    if cmp is None:
        cmp = Compare(old_root, new_root, overlay=args.overlay)
    st, hand, hand_added, t, fc = cmp.counts()
    out("index: old %d declarations, new %d; %s; added %d" % (
        len(cmp.old), len(cmp.new), " · ".join("%s %d" % (k, st[k]) for k in
                                              ("identical", "body", "body+sig", "removed", "moved", "moved+body")),
        len(cmp.added)))
    out("files (non-DLC): changed %d · identical %d · added %d · removed %d" % (
        fc["changed"], fc["identical"], fc["added"], fc["removed"]))
    out("T %d changed hand declarations = body %d + body+sig %d + removed %d + moved+body %d (moved %d, added %d excluded)" % (
        t, hand["body"], hand["body+sig"], hand["removed"], hand["moved+body"], hand["moved"], hand_added))

    sites = d3_sites()
    results = []
    all_files = set()
    for code_dir in args.code:
        rows = analyse(cmp, code_dir)
        results.append((code_dir, rows))
        for r in rows:
            all_files |= r["files"]
    b_rows = structure_rows(cmp, all_files)
    out("B %d file(s) with a DefineClass/__parents line changed under a pinned/required/cited file" % len(b_rows))
    for rel, gone, came in b_rows:
        users = sorted({r["module"] for _c, rows in results for r in rows if rel in r["files"]})
        out("  %s  -%d +%d  used by %s" % (rel, len(gone), len(came), ", ".join(users)))
        for l in gone[:6]:
            out("      - %s" % l[:140])
        for l in came[:6]:
            out("      + %s" % l[:140])

    notes = None
    if args.no_notes:
        out("notes: not fetched (--no-notes)")
    elif args.overlay is not None:
        out("notes: n/a (synthetic overlay; notes describe a real patch)")
    elif not (fc["changed"] or fc["added"] or fc["removed"]):
        out("notes: n/a (no file changed between the trees)")
    else:
        try:
            notes = fetch_notes(new_ver or "")
            if notes is None:
                out("notes: fetched; no announcement names %s" % new_ver)
            else:
                out("notes: fetched — %r (%s)" % (notes[0], notes[1]))
        except Exception as e:                       # noqa: BLE001 -- the run goes on
            out("notes: not fetched (%s)" % e.__class__.__name__)

    summary = []
    for code_dir, rows in results:
        rel_code = os.path.relpath(code_dir, REPO) if os.path.abspath(code_dir).startswith(REPO) else code_dir
        out("")
        out("── code: %s — %d modules ──" % (rel_code, len(rows)))
        m_set = [r for r in rows if r["flagged"]]
        cols = ["PIN", "REQ", "CITE", "ANON", "SIGCALL"]
        out("columns: " + " · ".join("%s %d" % (c, sum(1 for r in rows if r[c])) for c in cols) +
            " · D1 %d · M %d" % (sum(1 for r in rows if r["D1"]), len(m_set)))
        pinless = [r["module"] for r in rows if not (set(r["pins"]) - set(r["pin_unresolved"]))]
        out("modules with no resolvable pin (covered by REQ/CITE/ANON only): %d" % len(pinless))
        # D3
        d3 = []
        if sites is None:
            out("D3 NOT RUN: %s unreadable" % D13)
        else:
            for r in rows:
                if r["module"] in sites:
                    d3.append((r, sites[r["module"]]))
            out("D3 save-exposed sites in this Code/: %d; flagged %d" % (len(d3), sum(1 for r, _s in d3 if r["SIGCALL"])))
            for r, ids in d3:
                if r["SIGCALL"]:
                    for _k, n, cls, o, nw in r["SIGCALL"]:
                        out("  D3 %-6s %-26s %s %s %s -> %s" % ("/".join(ids), r["module"], n, cls, o, nw))
        d3_count = sum(1 for r, _s in d3 if r["SIGCALL"])
        # D2 ranked
        d2 = sorted((k, r["module"], n, cls, o, nw) for r in rows for (k, n, cls, o, nw) in r["SIGCALL"])
        out("D2 %d call(s) in %d module(s), ranked gone > incompatible > prefix-compatible" % (
            len(d2), len({x[1] for x in d2})))
        for _k, mod, n, cls, o, nw in d2:
            out("  %-17s %-26s %s  %s -> %s" % (cls, mod, n, o[:70], nw[:70]))
        # D1 / ANON per module
        out("M — flagged modules (%d):" % len(m_set))
        for r in m_set:
            tags = [c for c in cols if r[c]]
            out("  %s  [%s]" % (r["module"], " ".join(tags)))
            for c in ("PIN", "REQ", "CITE", "ANON"):
                for row in r[c][:args.rows]:
                    out("      %-4s %s" % (c, row))
                if len(r[c]) > args.rows:
                    out("      %-4s … %d more (--rows N)" % (c, len(r[c]) - args.rows))
        clean = [r["module"] for r in rows if not r["flagged"]]
        out("no row (%d): %s" % (len(clean), ", ".join(clean) if clean else "—"))
        # notes: escalation only
        added = []
        if notes is not None:
            hits = notes_hits(rows, notes[2], class_word_df(cmp))
            for r in rows:
                if r["module"] in hits and not r["flagged"]:
                    added.append(r["module"])
                    for term, ctx in hits[r["module"]][:2]:
                        out("  notes adds %-24s term %r: %s" % (r["module"], term, ctx))
            out("notes: %d module(s) matched, %d added to the read list" % (len(hits), len(added)))
        summary.append((rel_code, len(rows), len(m_set), len(added), d3_count))

    # verdict over the FIRST code dir (the fix pack); later dirs report, never decide
    rel_code, n_rows, m_count, added_count, d3_count = summary[0]
    v, why = verdict(archived, parity_ok, m_count, d3_count, len(b_rows), t)
    if added_count:
        v2, why2 = verdict(archived, parity_ok, m_count + added_count, d3_count, len(b_rows), t)
        order = ["none", "scoped", "full"]
        if order.index(v2) > order.index(v):
            why = why2 + ["raised by notes: +%d module(s)" % added_count]
            v = v2
    out("")
    d5 = facts_moved(cmp)
    if d5 is None:
        out("D5 not run: %s missing" % FACTS)
    else:
        n_facts, n_cited, flagged = d5
        out("D5 facts: %d files, %d with a resolvable game-function citation, %d cite a function that changed" % (
            n_facts, n_cited, len(flagged)))
        if not args.no_d5_list:
            for fid, moved in flagged:
                out("  %-8s %s" % (fid, ", ".join(moved[:4]) + (" …+%d" % (len(moved) - 4) if len(moved) > 4 else "")))
    out("")
    for rel_code2, n2, m2, a2, d32 in summary:
        out("summary %s: modules %d · M %d · notes-added %d · D3 %d" % (rel_code2, n2, m2, a2, d32))
    out("verdict: %s — %s  (limits %d modules / %d declarations are budget defaults; "
        "the small-patch regime is uncalibrated until the first real patch)" % (
            v.upper(), "; ".join(why), SCOPED_MAX_MODULES, FULL_MIN_T))
    return dict(verdict=v, results=results, t=t, b=b_rows, parity=parity_ok, cmp=cmp)


def parse(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--old", help="archived version (folder under %s) or a Src path; default: newest archive older than new" % ARCHIVE)
    ap.add_argument("--new", help="archived version or a Src path; default: the live install's ModTools\\Src")
    ap.add_argument("--code", action="append", help="a Code/ directory; repeatable; the first decides the verdict (default Code/)")
    ap.add_argument("--overlay", help="SYNTHETIC control: comma-separated tree paths taking new content over old; "
                    "__none__ = the identity control")
    ap.add_argument("--no-notes", action="store_true", help="skip the patch-notes fetch")
    ap.add_argument("--no-parity", action="store_true", help="skip fpk parity")
    ap.add_argument("--no-d5-list", action="store_true", help="print the D5 count only")
    ap.add_argument("--rows", type=int, default=8, help="rows per column per module (default 8)")
    args = ap.parse_args(argv)
    args.argv = argv
    args.code = args.code or [os.path.join(REPO, "Code")]
    args.overlay = (set() if args.overlay == "__none__" else set(args.overlay.split(","))) if args.overlay else None
    return args


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    run(parse())
