#!/usr/bin/env python3
"""Which modules redefine a shipped declaration outright, and which delegate to a captured original they actually call?

Written 2026-09-23 for the 1.1.1 adjudication (report FULL_BODY_PRIORITY_2026-09-23).
The stand-down design record D14 measured the copy-vs-wrapper split with a word grep
(`orig|_orig|original`), and the 1.1.1 adjudication brief's seed keyed off `-- SRC:` pins
and the `function Class:Method(` idiom. Both are name proxies. This script reads what a
module INSTALLS and what it CAPTURES, per idiom, so a reader can decide per module.

    python tools/replacecheck.py                 # every module in Code/
    python tools/replacecheck.py --only Fix_A,Fix_B
    python tools/replacecheck.py --bodies 60     # also print each install body (first N lines)

WHAT IT PRINTS, per module (00_Core is skipped: it installs nothing)
  PIN      L<n> <path> <selector>          the module's SRC: manifest rows
  CAPTURE  L<n> <var> = <expr> calls=<c>   a local that holds a shipped function value:
                                           Class.Method, `X and X.Method`, a global name,
                                           rawget(_G,"name") or OnMsg.name -- with how many
                                           times that local is INVOKED elsewhere in the file
  INSTALL  L<n> <kind> <target>            a site that writes a function into a shipped
                                           table: function X:M( / function X.M( / X.M = function
                                           / X.M = name / function Global( / SMRFixPack.SetGlobal
                                           / OnMsg.X = function / _G[...] = / rawset(_G, ...)

HOW TO READ IT. An INSTALL whose target has no CAPTURE with calls > 0 is a full-body
replacement candidate. A CAPTURE with calls > 0 is delegation -- but a capture called on
only some paths, or called with its result discarded, is a partial replacement, and only
reading the body settles that (--bodies). A module with no INSTALL is a hook, a data patch
or a migration. This is a router, never a disposition: it cannot see an install performed
through a helper it does not know, and it cannot judge what the body does with the value.

LIMITS, stated. Regex over the module text: a capture written as anything but the forms
above is missed (the 2026-09-23 first pass missed `local orig = R and R.Method`, since
added), and so is an install whose right-hand side is a call, `X.M = helper(orig, ...)`
(Fix_HabitatExpeditionDraft installs that way and prints no INSTALL row; its captures
and their calls still print). Aliases are resolved one level (`local C = Colonist`). OnMsg assignment is
reported as an install because the text cannot tell an additive handler from a
replacement -- in this engine OnMsg is additive, so treat those rows as hooks.
"""
import glob
import os
import re
import sys

PIN = re.compile(r"^-- SRC: (\S+) (\S+) sha256=")
LOCAL_TABLE = re.compile(r"^\s*local ([A-Za-z_]\w*)\s*=\s*\{")
ALIAS = re.compile(r"^\s*local ([A-Za-z_]\w*)\s*=\s*(?:rawget\(_G,\s*\"(\w+)\"\)|([A-Z]\w*))\s*$")
INSTALL = (
    (re.compile(r"^\s*function ([A-Za-z_]\w*)[:.]([A-Za-z_]\w*)\s*\("), "method-def", "match"),
    (re.compile(r"^\s*([A-Za-z_]\w*)\.([A-Za-z_]\w*)\s*=\s*function"), "method-assign-fn", "match"),
    (re.compile(r"^\s*([A-Za-z_]\w*)\.([A-Za-z_]\w*)\s*=\s*([A-Za-z_]\w*)\s*$"), "method-assign-name", "match"),
    (re.compile(r"^\s*function ([A-Za-z_]\w*)\s*\("), "global-def", "match"),
    (re.compile(r"SMRFixPack\.SetGlobal\(\s*\"(\w+)\""), "setglobal", "search"),
    (re.compile(r"^\s*OnMsg\.(\w+)\s*=\s*function"), "onmsg-assign", "match"),
    (re.compile(r"_G\[\s*\"?(\w+)\"?\s*\]\s*="), "_G-assign", "search"),
    (re.compile(r"rawset\(\s*_G\s*,\s*\"(\w+)\""), "rawset", "search"),
)
CAPTURE = re.compile(r"^\s*local ([A-Za-z_]\w*)\s*=\s*(.+?)\s*$")
CAPTURE_RHS = re.compile(
    r"^(?:[A-Za-z_]\w* and )?(?:rawget\(_G,\s*\"\w+\"\)|[A-Za-z_]\w*(?:\.[A-Za-z_]\w*)+|[A-Z]\w*|OnMsg\.\w+)$")
NOT_SHIPPED_OWNERS = {"SMRFixPack", "self", "ctx", "entry", "M", "mod", "fix", "def", "spec", "probe", "t", "tbl"}


def strip_comment(line):
    i = line.find("--")
    if i >= 0 and line.count('"', 0, i) % 2 == 0 and line.count("'", 0, i) % 2 == 0:
        return line[:i]
    return line


def block_end(lines, i):
    indent = len(lines[i]) - len(lines[i].lstrip("\t "))
    for j in range(i + 1, len(lines)):
        m = lines[j]
        if len(m) - len(m.lstrip("\t ")) == indent and m.strip().startswith("end") \
                and not m.strip().startswith("end)"):
            return j
    return len(lines) - 1


def scan(path):
    lines = open(path, encoding="utf-8", errors="replace").read().splitlines()
    pins, aliases, local_tables, installs, captures = [], {}, set(), [], []
    for n, raw in enumerate(lines, 1):
        m = PIN.match(raw)
        if m:
            pins.append((n, m.group(1), m.group(2)))
        line = strip_comment(raw)
        if not line.strip():
            continue
        m = LOCAL_TABLE.match(line)
        if m:
            local_tables.add(m.group(1))
        m = ALIAS.match(line)
        if m:
            aliases[m.group(1)] = m.group(2) or m.group(3)
        for rx, kind, how in INSTALL:
            m = rx.search(line) if how == "search" else rx.match(line)
            if not m:
                continue
            if kind in ("method-def", "method-assign-fn", "method-assign-name"):
                owner, meth = m.group(1), m.group(2)
                if owner in local_tables or owner in NOT_SHIPPED_OWNERS:
                    continue
                if kind == "method-assign-name" and m.group(3) in ("nil", "true", "false"):
                    continue
                target = "%s.%s" % (aliases.get(owner, owner), meth)
                if kind == "method-assign-name":
                    target += "  <= " + m.group(3)
            elif kind == "global-def":
                if line.lstrip().startswith("local "):
                    continue
                target = "GLOBAL " + m.group(1)
            elif kind == "onmsg-assign":
                target = "OnMsg." + m.group(1)
            else:
                target = kind.upper() + " " + m.group(1)
            installs.append((n, kind, target))
            break
        m = CAPTURE.match(line)
        if m and CAPTURE_RHS.match(m.group(2)) and m.group(2) not in ("true", "false", "nil"):
            captures.append((n, m.group(1), m.group(2)))
    rows = []
    for n, var, rhs in captures:
        rest = "\n".join(l for i, l in enumerate(lines, 1) if i != n)
        calls = len(re.findall(r"(?<![\w.:])%s\s*\(" % re.escape(var), rest))
        passed = len(re.findall(r"(?<![\w.:])%s\s*[,)]" % re.escape(var), rest))
        if re.match(r"^[a-z_]\w*\.", rhs) and not calls:
            continue  # a plain data read (self.x, building.y); not a function capture
        rows.append((n, var, rhs, calls, passed))
    return lines, pins, rows, installs


def main(argv):
    root = "Code"
    only = None
    max_body = 0
    args = list(argv)
    while args:
        a = args.pop(0)
        if a == "--only":
            only = set(x.replace(".lua", "") for x in args.pop(0).split(","))
        elif a == "--bodies":
            max_body = int(args.pop(0))
        else:
            root = a
    out = sys.stdout
    if hasattr(out, "reconfigure"):
        out.reconfigure(encoding="utf-8", errors="replace")
    for path in sorted(glob.glob(os.path.join(root, "*.lua"))):
        name = os.path.basename(path)
        if name == "00_Core.lua":
            continue
        if only and name.replace(".lua", "") not in only:
            continue
        lines, pins, caps, installs = scan(path)
        print("=== %s ===" % name)
        for n, p, s in pins:
            print("  PIN     L%-4d %s %s" % (n, p, s))
        for n, var, rhs, calls, passed in caps:
            print("  CAPTURE L%-4d %-16s = %-45s calls=%d passed=%d" % (n, var, rhs, calls, passed))
        for n, kind, target in installs:
            print("  INSTALL L%-4d %-18s %s" % (n, kind, target))
            if max_body and "function" in lines[n - 1]:
                j = block_end(lines, n - 1)
                seg = lines[n - 1:j + 1]
                for k, l in enumerate(seg[:max_body], n):
                    print("      %5d  %s" % (k, l.replace("\t", "    ")))
                if len(seg) > max_body:
                    print("      ..... %d more lines to L%d" % (len(seg) - max_body, j + 1))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
