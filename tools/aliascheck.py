# -*- coding: utf-8 -*-
"""A Test Kit probe that calls a bare helper its file never bound ERRORs at run
time while parsing perfectly. Nothing else in the toolchain sees that class.

`parsecheck.py` proves a file PARSES and stops there. The kit binds `SMRTest`
helpers to file-local aliases at the top of each probe file, so a probe calling
`FixMissing(...)` in a file that never wrote `local FixMissing = SMRTest.FixMissing`
reads a nil global and dies the moment that line executes. It is the F114 shape:
a green instrument that proves the wrong thing.

Found the hard way in the kit on 2026-09-09 by link 07 (`smr-bugfixpack-ee`),
whose prototype is the ancestor of this file. The defect class already had a
precedent gate in this project, which is why it is worth a tool rather than a
habit: the arming scripts' "G1 cross-check" resolved every `C47.<name>` USED
against those DEFINED, and `tools/arm_leg.ps1` now carries that generalised.

⚠️ REPORT-ONLY OVER THE KIT, ALWAYS EXIT 0. The owner's 2026-08-04 decision is
that the Test Kit never blocks a pack commit; `testkit_tree()` and doccheck's
TestKit `PARSE:` row both follow it and so does this. A row here is routed or
fixed, never used as a gate.

Three checks, and each earned its place from a specific way the ancestor could be
wrong (the ancestor's author listed most of them against their own tool):

  UNBOUND   a bare `Helper(` call in a file that binds no `Helper`.
  MISBOUND  `local FixMissing = SMRTest.FixRetired` -- bound, but to the wrong
            member, which every "is it bound?" check passes.
  UNKNOWN   a `SMRTest.<name>` reference where `<name>` is defined by NO kit
            file (the namespace is extended by probe files too, not just the
            core). Catches the misspelling the
            UNBOUND check structurally cannot: a typo is not in any helper list,
            so a list-driven check never looks for it.

TWO THINGS THE ANCESTOR GOT WRONG THAT ARE FIXED HERE, both in the
false-negative direction, which is the one that matters:

1. ITS COMMENT STRIPPER WAS A REGEX AND LUA IS NOT REGULAR. `re.sub(r"(?m)--.*$")`
   eats a `--` that appears INSIDE a Lua string literal, truncating the line and
   hiding any real call after it. Several kit probe messages contain `--`. This
   file lexes instead: `strip_lua()` walks the source once, tracking short and
   long strings and short and long comments, and blanks only what is genuinely
   not code. Falsified on the exact case.
2. ITS HELPER LIST WAS HAND-MAINTAINED, so a helper added to `00_TestCore.lua`
   later was silently unchecked. Here the set is DERIVED, and from BOTH definition
   forms -- `function SMRTest.X` and `SMRTest.X = ...`. That matters concretely:
   `FixMissing` and `FixRetired`, the two helpers the original finding was about,
   are defined by ASSIGNMENT (`00_TestCore.lua:327`, `:361`), so deriving from the
   `function` form alone finds 17 members where the kit has 28.

Usage:
    python tools/aliascheck.py                 # report over the kit
    python tools/aliascheck.py --dir <path>    # report over another Code/ dir
    python tools/aliascheck.py --selftest      # the falsifier
"""

import argparse
import io
import os
import re
import sys

TESTKIT = os.environ.get("SMR_TESTKIT", r"C:\Dev\SMR-BugFixPack-TestKit")
CORE = "00_TestCore.lua"


# --------------------------------------------------------------------------- #
# the lexer the ancestor did not have
# --------------------------------------------------------------------------- #
def strip_lua(src):
    """Blank every comment and string body, preserving length and newlines.

    Length preservation keeps reported line numbers honest and keeps call syntax
    intact: a string becomes quotes around spaces, so `f("--")` still reads as a
    call to `f` and the `--` inside can no longer start a comment.
    """
    out = list(src)
    i, n = 0, len(src)

    def blank(start, end):
        for k in range(start, min(end, n)):
            if out[k] != "\n":
                out[k] = " "

    def long_bracket(at):
        """If a long bracket opens at `at`, return its level, else None."""
        if src[at] != "[":
            return None
        j = at + 1
        eq = 0
        while j < n and src[j] == "=":
            eq += 1
            j += 1
        if j < n and src[j] == "[":
            return eq
        return None

    while i < n:
        c = src[i]

        # comment: short or long
        if c == "-" and i + 1 < n and src[i + 1] == "-":
            level = long_bracket(i + 2)
            if level is not None:
                close = "]" + "=" * level + "]"
                end = src.find(close, i + 2)
                end = n if end < 0 else end + len(close)
                blank(i, end)
                i = end
                continue
            end = src.find("\n", i)
            end = n if end < 0 else end
            blank(i, end)
            i = end
            continue

        # long string
        level = long_bracket(i)
        if level is not None:
            close = "]" + "=" * level + "]"
            end = src.find(close, i)
            end = n if end < 0 else end + len(close)
            blank(i + 1, end)          # keep the opening [ so it is not a call
            i = end
            continue

        # short string
        if c in "'\"":
            j = i + 1
            while j < n:
                if src[j] == "\\":
                    j += 2
                    continue
                if src[j] == c or src[j] == "\n":
                    break
                j += 1
            blank(i + 1, j)            # keep the quotes
            i = min(j + 1, n)
            continue

        i += 1

    return "".join(out)


# --------------------------------------------------------------------------- #
def defined_members(code):
    """Every SMRTest member this source defines, both forms."""
    names = set()
    for m in re.finditer(r"(?m)^\s*function\s+SMRTest\.([A-Za-z_]\w*)", code):
        names.add(m.group(1))
    for m in re.finditer(r"(?m)^\s*SMRTest\.([A-Za-z_]\w*)\s*=", code):
        names.add(m.group(1))
    return names


def bindings(code):
    """alias -> SMRTest member, for `local a, b = SMRTest.x, SMRTest.y` too."""
    found = {}
    plain = set()
    for m in re.finditer(r"(?m)^\s*local\s+([A-Za-z_][\w\s,]*?)\s*=\s*([^\n]+)", code):
        names = [x.strip() for x in m.group(1).split(",") if x.strip()]
        rhs = m.group(2)
        values = [v.strip() for v in rhs.split(",")]
        for idx, name in enumerate(names):
            val = values[idx] if idx < len(values) else ""
            mem = re.match(r"^SMRTest\.([A-Za-z_]\w*)", val)
            if mem:
                found[name] = mem.group(1)
            else:
                plain.add(name)          # a legitimate file-local of that name
    return found, plain


def scan(directory):
    core_path = os.path.join(directory, CORE)
    if not os.path.isfile(core_path):
        return None, "no %s in %s" % (CORE, directory)

    files = sorted(f for f in os.listdir(directory) if f.endswith(".lua"))

    # Members are the union over EVERY kit file, not just 00_TestCore. Measured
    # 2026-09-09: deriving from the core alone produced 16 false UNKNOWN rows,
    # because probe files legitimately EXTEND the namespace - 90_Loggers.lua
    # defines SMRTest.Log and SMRTest.Loggers, 91_Stress.lua SMRTest.Stress,
    # 97_ForceInactive.lua SMRTest.ForceInactive, 99_FixtureCarry.lua
    # SMRTest.FixtureCarry. The core is still required to exist, as proof the
    # directory really is a kit and not an arbitrary folder of Lua.
    codes = {}
    members = set()
    for name in files:
        with io.open(os.path.join(directory, name), encoding="utf-8",
                     errors="replace") as fh:
            codes[name] = strip_lua(fh.read())
        members |= defined_members(codes[name])
    if not defined_members(codes[CORE]):
        return None, "%s defines no SMRTest members - refusing to guess" % CORE

    rows = []
    for name in files:
        if name == CORE:
            continue
        code = codes[name]
        bound, plain = bindings(code)

        for m in re.finditer(r"SMRTest\.([A-Za-z_]\w*)", code):
            if m.group(1) not in members:
                rows.append(("UNKNOWN", name, m.group(1),
                             "SMRTest.%s is defined by no kit file" % m.group(1)))

        for alias, member in sorted(bound.items()):
            if alias in members and member != alias:
                rows.append(("MISBOUND", name, alias,
                             "bound to SMRTest.%s, not SMRTest.%s" % (member, alias)))

        for helper in sorted(members):
            if not re.search(r"(?<![\w.:])%s\s*\(" % re.escape(helper), code):
                continue
            if helper in bound or helper in plain:
                continue
            rows.append(("UNBOUND", name, helper,
                         "calls %s() but never binds it - nil at run time" % helper))

    return {"files": files, "members": sorted(members), "rows": rows}, None


def report(result, out):
    for kind, name, sym, detail in result["rows"]:
        out.append("  %-9s %-26s %s" % (kind, name, detail))
    out.append("ALIASCHECK: %d file(s), %d SMRTest member(s) derived, %d finding(s)"
               % (len(result["files"]), len(result["members"]), len(result["rows"])))


# --------------------------------------------------------------------------- #
def selftest():
    """Every check seen to fire, and seen NOT to fire. 10 legs."""
    import shutil
    import tempfile

    core = (
        "function SMRTest.WithGlobals(t, f) end\n"
        "SMRTest.FixMissing = fix_missing\n"
        "SMRTest.FixRetired = fix_retired\n"
    )
    bad = []
    n = [0]

    def leg(label, src, want_kinds, core_src=core, extra=None):
        n[0] += 1
        d = tempfile.mkdtemp(prefix="aliascheck_")
        try:
            with io.open(os.path.join(d, CORE), "w", encoding="utf-8") as fh:
                fh.write(core_src)
            for fname, fsrc in (extra or {}).items():
                with io.open(os.path.join(d, fname), "w", encoding="utf-8") as fh:
                    fh.write(fsrc)
            with io.open(os.path.join(d, "50_Probe.lua"), "w", encoding="utf-8") as fh:
                fh.write(src)
            res, err = scan(d)
            got = sorted(set(r[0] for r in (res["rows"] if res else [])))
            ok = got == sorted(want_kinds) and (err is None)
            print("  %-46s got=%-22s want=%-22s %s"
                  % (label, ",".join(got) or "-", ",".join(sorted(want_kinds)) or "-",
                     "PASS" if ok else "*** FAIL ***"))
            if not ok:
                bad.append(label)
                if err:
                    print("        err: %s" % err)
        finally:
            shutil.rmtree(d, ignore_errors=True)

    print("aliascheck --selftest - every check must be seen to fire")
    print("")

    # 1 clean file
    leg("clean: bound and called",
        "local FixMissing = SMRTest.FixMissing\nFixMissing('x')\n", [])

    # 2 the original defect
    leg("UNBOUND: calls FixMissing, binds nothing",
        "FixMissing('x')\n", ["UNBOUND"])

    # 3 fully-qualified use needs no alias (64_Probes_Wave14's convention)
    leg("clean: fully-qualified SMRTest.FixMissing(...)",
        "SMRTest.FixMissing('x')\n", [])

    # 4 THE ANCESTOR'S FALSE NEGATIVE, in the ONLY shape that actually triggers
    # it: a `--` inside a string with the call LATER ON THE SAME LINE. Measured
    # 2026-09-09 - the ancestor's `re.sub(r"(?m)--.*$")` truncates from the `--`
    # to end of line and cannot see this call; strip_lua can. A first draft of
    # this leg put the string on the PREVIOUS line, where both tools see the
    # call, so it passed while proving nothing. Same-line or it is not a test.
    leg("`--` in a string hides a SAME-LINE call from a regex",
        "local s = 'a -- b'; FixMissing('x')\n", ["UNBOUND"])

    # 5 a call named only in a comment is not a call
    leg("call named only in a comment (no fire)",
        "-- FixMissing('x') was here\nlocal a = 1\n", [])

    # 6 a call named only inside a string is not a call
    leg("call named only inside a string (no fire)",
        "local s = \"FixMissing('x')\"\n", [])

    # 7 long comment
    leg("call inside a --[==[ long comment ]==] (no fire)",
        "--[==[\nFixMissing('x')\n]==]\nlocal a = 1\n", [])

    # 8 long string
    leg("call inside a [[ long string ]] (no fire)",
        "local s = [[\nFixMissing('x')\n]]\n", [])

    # 9 wrong member
    leg("MISBOUND: alias bound to the wrong member",
        "local FixMissing = SMRTest.FixRetired\nFixMissing('x')\n", ["MISBOUND"])

    # 10 typo on the qualified side - what a helper list can never catch
    leg("UNKNOWN: SMRTest.FixMissng typo",
        "SMRTest.FixMissng('x')\n", ["UNKNOWN"])

    # 11 multi-name binding line
    leg("clean: local a, b = SMRTest.x, SMRTest.y",
        "local FixMissing, WithGlobals = SMRTest.FixMissing, SMRTest.WithGlobals\n"
        "FixMissing('x')\nWithGlobals({}, function() end)\n", [])

    # 12 a legitimate file-local function of the same name is not unbound
    leg("clean: file-local function shadows a helper name",
        "local FixMissing = function() end\nFixMissing('x')\n", []),

    # 13 method-call syntax must not be read as a bare call
    leg("clean: obj:FixMissing() is not a bare call",
        "local o = {}\no:FixMissing()\n", [])

    # 14 a member defined by ANOTHER kit file is not UNKNOWN. Deriving
    # members from 00_TestCore alone produced 16 false rows on the real kit
    # (90_Loggers defines SMRTest.Log, 91_Stress SMRTest.Stress, and so on),
    # so this leg holds the union behaviour in place.
    leg("clean: member defined by another kit file",
        "SMRTest.Log('x')\n", [],
        extra={"90_Loggers.lua": "function SMRTest.Log(s) end\n"})


    # 15 the converse must still fire, or leg 14 has merely disabled the check
    leg("UNKNOWN: member defined by NO file still fires",
        "SMRTest.Nope('x')\n", ["UNKNOWN"],
        extra={"90_Loggers.lua": "function SMRTest.Log(s) end\n"})


    print("")
    if bad:
        print("SELFTEST FAILED on: %s" % ", ".join(bad))
        return 1
    print("SELFTEST: ALL %d LEGS PASS" % n[0])
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--dir", default=os.path.join(TESTKIT, "Code"))
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()

    if args.selftest:
        return selftest()

    out = []
    if not os.path.isdir(args.dir):
        print("ALIASCHECK: not checked (no directory at %s)" % args.dir)
        return 0                          # report-only: never a block
    result, err = scan(args.dir)
    if err:
        print("ALIASCHECK: not checked (%s)" % err)
        return 0
    report(result, out)
    print("\n".join(out))
    return 0                              # report-only, ALWAYS 0


if __name__ == "__main__":
    sys.exit(main())
