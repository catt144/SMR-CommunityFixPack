"""Desk control for archived shipped mod-loading queue bodies. No game or storage writes."""

import hashlib
import sys
from pathlib import Path

from lupa import LuaRuntime


sys.path.insert(0, str(Path.cwd() / "tools"))  # Run from repository root.
from luafn import find_bodies  # noqa: E402


ROOT = Path("B:/Dev/SMR/SMR-Shared/SMR-SrcArchive")
SOURCES = (
    ("1.0.7.396349", "CommonLua/Classes/Mod.lua", 1860, 1980),
    ("1.1.0.403908", "CommonLua/Modding/Mod.lua", 1873, 1993),
    ("1.1.1.405907", "CommonLua/Modding/Mod.lua", 1873, 1993),
)
CASES = {
    "independent B,A": ("", "{'B','A'}"),
    "required A->B, list A,B": ("Mods.A.dependencies={{id='B',required=true,ModFits=ModDependency.ModFits}}", "{'A','B'}"),
    "required A->B, B disabled": ("Mods.A.dependencies={{id='B',required=true,ModFits=ModDependency.ModFits}}", "{'A'}"),
    "optional A->B, B disabled": ("Mods.A.dependencies={{id='B',required=false,ModFits=ModDependency.ModFits}}", "{'A'}"),
    "optional A->missing": ("Mods.A.dependencies={{id='missing',required=false,ModFits=ModDependency.ModFits}}", "{'A'}"),
    "required A->missing": ("Mods.A.dependencies={{id='missing',required=true,ModFits=ModDependency.ModFits}}", "{'A'}"),
    "optional A->B, incompatible": ("Mods.A.dependencies={{id='B',required=false,version_major=2,ModFits=ModDependency.ModFits}}", "{'A','B'}"),
    "required A->B, incompatible": ("Mods.A.dependencies={{id='B',required=true,version_major=2,ModFits=ModDependency.ModFits}}", "{'A','B'}"),
    "required A<->B cycle": ("Mods.A.dependencies={{id='B',required=true,ModFits=ModDependency.ModFits}}; Mods.B.dependencies={{id='A',required=true,ModFits=ModDependency.ModFits}}", "{'A','B'}"),
}
EXPECTED = {
    "independent B,A": ("B,A", ""),
    "required A->B, list A,B": ("B,A", ""),
    "required A->B, B disabled": ("<empty>", "not loaded"),
    "optional A->B, B disabled": ("B,A", ""),
    "optional A->missing": ("ERROR", "attempt to index a nil value (local 'mod')"),
    "required A->missing": ("<empty>", "not found"),
    "optional A->B, incompatible": ("B,A", ""),
    "required A->B, incompatible": ("B", "not compatible"),
    "required A<->B cycle": ("<empty>", "circular dependency cycle"),
}


def body(lines, pattern):
    hits = find_bodies(lines, pattern)
    assert len(hits) == 1, (pattern, hits)
    start, end = hits[0]
    return "\n" * start + "\n".join(lines[start : end + 1])


for build, relative, start, end in SOURCES:
    path = ROOT / build / "Src" / relative
    lines = path.read_text(encoding="utf-8").splitlines()
    queue_body = "\n".join(lines[start - 1 : end]) + "\n"
    source = "\n" * (start - 1) + queue_body + "\nreturn GetLoadingQueue"
    print(f"{build} {relative}:{start}-{end} sha256={hashlib.sha256(queue_body.encode()).hexdigest()}")
    checked = 0
    for label, (setup, list_literal) in CASES.items():
        lua = LuaRuntime(unpack_returned_tuples=True)
        lua.execute("""
            function table.find(t, value)
                for i, entry in ipairs(t) do if entry == value then return i end end
            end
            messages = {}
            function ModMessage(message) messages[#messages+1] = message end
            ModDef={}; ModDependency={}
            Mods = {
                A={id='A',version=1,version_major=1,version_minor=0,dependencies={},GetModLabel=function(self) return self.id end},
                B={id='B',version=1,version_major=1,version_minor=0,dependencies={},GetModLabel=function(self) return self.id end},
            }
        """)
        lua.execute(body(lines, r"^function ModDef:CompareVersion\(other_mod, ignore_revision\)"))
        lua.execute(body(lines, r"^function ModDependency:ModFits\(mod_def\)"))
        lua.execute("Mods.A.CompareVersion=ModDef.CompareVersion; Mods.B.CompareVersion=ModDef.CompareVersion")
        lua.execute(setup)
        queue_function = lua.execute(source)
        expected_ids, expected_detail = EXPECTED[label]
        try:
            queue = queue_function(lua.eval(list_literal))
            ids = ",".join(queue[i] for i in range(1, len(queue) + 1)) or "<empty>"
            messages = lua.globals().messages
            message = " | ".join(messages[i] for i in range(1, len(messages) + 1))
            assert expected_ids != "ERROR", f"{label}: missing expected error"
            assert ids == expected_ids, (label, ids, expected_ids)
            assert expected_detail in message, (label, message, expected_detail)
            print(f"  {label}: [{ids}] {message}")
        except Exception as exc:
            if isinstance(exc, AssertionError) or expected_ids != "ERROR":
                raise
            first = str(exc).splitlines()[0]
            assert expected_detail in first, (label, first, expected_detail)
            expected_line = 1864 if build == "1.0.7.396349" else 1877
            assert f":{expected_line}:" in first, (label, first, expected_line)
            print(f"  {label}: ERROR {first}")
        checked += 1
    assert checked == len(CASES) == len(EXPECTED)
    print(f"{build} PASS {checked}/{len(EXPECTED)} named cases")
