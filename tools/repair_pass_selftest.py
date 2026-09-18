#!/usr/bin/env python3
"""Repair-pass falsifiers; mutants execute only in a temporary directory.

Run: python tools/repair_pass_selftest.py
Each demand is paired with a control and rerun against a reverted scratch copy.
"""
import hashlib
from pathlib import Path
import shutil
import sys
import tempfile
import types
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))


def load_copy(path, source):
    path.write_bytes(source.encode("utf-8"))
    module = types.ModuleType("repair_scratch")
    module.__file__ = str(path)
    exec(compile(source, str(path), "exec"), module.__dict__)
    return module


def fingerprint_cases(module):
    module.facts_splitter = lambda: types.SimpleNamespace(
        load_from_dir=lambda: {"facts": [{"derived_at": "game 1.1.0 build 24995074"}]})
    for build, expected in (("24995074", "HOLDS"), ("2499507", "MOVED"),
                            ("249950740", "MOVED"), (None, "cannot check")):
        module.installed_build = lambda: build
        out = []
        module.emit_fingerprints(out)
        assert any(expected in x for x in out), (build, out)


def parity_cases(module, root):
    """Drift real list copies without ever mutating the live metadata."""
    metadata = root / "metadata.lua"
    predictor = root / "tools/pack_predict.py"
    predictor.parent.mkdir(exist_ok=True)
    metadata.write_bytes((ROOT / "metadata.lua").read_bytes())
    predictor.write_bytes((ROOT / "tools/pack_predict.py").read_bytes())
    originals = {p: p.read_bytes() for p in (metadata, predictor)}
    original_repo = module.REPO
    module.REPO = str(root)
    try:
        out = []
        assert module.pack_ignore_parity(out), out
        print("CONTROL " + out[0])
        source = predictor.read_text(encoding="utf-8-sig")
        for label, drift in (
            ("membership", source.replace('    "*.rgignore",\n', "")),
            ("order", source.replace('    "*.git/*",\n    "*.svn/*",',
                                     '    "*.svn/*",\n    "*.git/*",')),
        ):
            assert drift != source
            predictor.write_bytes(drift.encode("utf-8"))
            out = []
            result = module.pack_ignore_parity(out)
            assert not result and any("PACK IGNORE PARITY: RED" in x for x in out), out
            print(label.upper() + " " + out[0])
            predictor.write_bytes(originals[predictor])
        out = []
        assert module.pack_ignore_parity(out), out
        print("RESTORED " + out[0])
        for path, content in originals.items():
            assert path.read_bytes() == content
            print("RESTORED %s SHA256 %s" % (path.name, hashlib.sha256(content).hexdigest()))
    finally:
        module.REPO = original_repo
        for path, content in originals.items():
            path.write_bytes(content)


def compile_cases(module, root):
    """TOOLS COMPILE over a scratch copy of every live tools/*.py.

    Control: the clean copy passes. Demand: a syntax error planted at the end
    of one copy goes RED and names that file and line.
    """
    tools = root / "compile-tools"
    shutil.rmtree(tools, ignore_errors=True)
    tools.mkdir()
    for path in sorted((ROOT / "tools").glob("*.py")):
        shutil.copyfile(path, tools / path.name)
    original_dir = module.TOOLS_DIR
    module.TOOLS_DIR = str(tools)
    try:
        out = []
        assert module.tools_compile(out), out
        assert out[0].startswith("TOOLS COMPILE: PASS"), out
        print("CONTROL " + out[0])
        planted = tools / "pack_list.py"
        good = planted.read_bytes()
        assert good.endswith(b"\n")
        line = good.count(b"\n") + 1
        planted.write_bytes(good + b"def broken(:\n")
        out = []
        assert not module.tools_compile(out), out
        assert out[0].startswith("TOOLS COMPILE: RED"), out
        assert any("tools/pack_list.py:%d:" % line in x for x in out), out
        print("PLANTED " + out[0] + " | " + out[1].strip())
        planted.write_bytes(good)
        out = []
        assert module.tools_compile(out), out
        print("RESTORED " + out[0])
    finally:
        module.TOOLS_DIR = original_dir


def flpk_cases(module, root):
    """FLPK SELFTEST: present passes; absent, unspawnable or failing is RED."""
    tree = root / "flpk-tree"
    tool = tree / "tools" / "flpk_extract.py"
    tool.parent.mkdir(parents=True, exist_ok=True)
    live = (ROOT / "tools" / "flpk_extract.py").read_bytes()
    tool.write_bytes(live)
    original_repo = module.REPO
    module.REPO = str(tree)
    try:
        out = []
        assert module.flpk_selftest(out), out
        print("CONTROL " + out[0])
        tool.unlink()
        out = []
        assert not module.flpk_selftest(out), out
        assert out[0].startswith("FLPK SELFTEST: RED") and "absent" in out[0], out
        print("ABSENT " + out[0])
        tool.write_bytes(live)
        with patch.object(module.subprocess, "run", side_effect=OSError("spawn refused")):
            out = []
            assert not module.flpk_selftest(out), out
        assert out[0].startswith("FLPK SELFTEST: RED") and "could not run" in out[0], out
        print("UNSPAWNABLE " + out[0])
        tool.write_bytes(b"import sys\nsys.exit(1)\n")
        out = []
        assert not module.flpk_selftest(out), out
        assert out[0].startswith("FLPK SELFTEST: RED") and "FAILED" in out[0], out
        print("FAILING " + out[0][:60])
        tool.write_bytes(live)
        out = []
        assert module.flpk_selftest(out), out
        print("RESTORED " + out[0])
    finally:
        module.REPO = original_repo


def main():
    source = (ROOT / "tools/doccheck.py").read_text(encoding="utf-8-sig")
    digest = hashlib.sha256(source.encode()).hexdigest()
    with tempfile.TemporaryDirectory(prefix="smr-repair-") as directory:
        root = Path(directory)
        scratch = root / "doccheck.py"
        fixed = load_copy(scratch, source)
        fingerprint_cases(fixed)
        print("PASS A2 control and demands on repaired copy")
        start = source.index('            elif re.search(r"\\bbuild')
        end = source.index('\n                verdict =', start)
        mutant = source[:start] + '            elif build in bare:' + source[end:]
        broken = load_copy(scratch, mutant)
        try:
            fingerprint_cases(broken)
        except AssertionError as error:
            assert error.args[0][0] == "2499507", error
            print("PASS A2 reverted scratch: exact control passes, prefix demand FAILS")
        else:
            raise AssertionError("A2 mutant survived")
        # Restore and run the WHOLE check, then hash the restored scratch copy.
        restored = load_copy(scratch, source)
        fingerprint_cases(restored)
        if hasattr(restored, "pack_ignore_parity"):
            parity_cases(restored, root)
            # Prove a missing parity gate cannot satisfy either drift demand.
            start = source.index("def pack_ignore_parity(")
            end = source.index("def main():", start)
            mutant = source[:start] + (
                'def pack_ignore_parity(out):\n'
                '    out.append("PACK IGNORE PARITY: PASS (mutant)")\n'
                '    return True\n\n\n'
            ) + source[end:]
            broken = load_copy(scratch, mutant)
            try:
                parity_cases(broken, root)
            except AssertionError:
                print("PASS B2 reverted scratch: control passes, drift demand FAILS")
            else:
                raise AssertionError("B2 mutant survived")
            restored = load_copy(scratch, source)
            fingerprint_cases(restored)
            parity_cases(restored, root)
        # C1: every tools/*.py byte-compiles. A gate that always passes must
        # not satisfy the planted-error demand.
        compile_cases(restored, root)
        start = source.index("def tools_compile(")
        end = source.index("def counts_block(", start)
        mutant = source[:start] + (
            'def tools_compile(out):\n'
            '    out.append("TOOLS COMPILE: PASS (mutant)")\n'
            '    return True\n\n\n'
        ) + source[end:]
        try:
            compile_cases(load_copy(scratch, mutant), root)
        except AssertionError:
            print("PASS C1 reverted scratch: clean control passes, planted error FAILS")
        else:
            raise AssertionError("C1 mutant survived")
        # C2: the FLPK gate cannot vanish green. Each mutant is the pre-fix
        # body of one branch ("not checked", passing).
        restored = load_copy(scratch, source)
        flpk_cases(restored, root)
        for label, needle, replacement in (
            ("absent",
             '        out.append("FLPK SELFTEST: RED — tools/flpk_extract.py is absent "\n'
             '                   "(pack_list.py imports its parser)")\n'
             '        return False\n',
             '        out.append("FLPK SELFTEST: not checked (tools/flpk_extract.py absent)")\n'
             '        return True\n'),
            ("unspawnable",
             '        out.append("FLPK SELFTEST: RED — could not run (%s)" % exc)\n'
             '        return False\n',
             '        out.append("FLPK SELFTEST: not checked (%s)" % exc)\n'
             '        return True\n'),
        ):
            assert source.count(needle) == 1, label + " mutation is ambiguous"
            try:
                flpk_cases(load_copy(scratch, source.replace(needle, replacement)), root)
            except AssertionError:
                print("PASS C2 reverted scratch (%s): control passes, demand FAILS" % label)
            else:
                raise AssertionError("C2 %s mutant survived" % label)
        restored = load_copy(scratch, source)
        fingerprint_cases(restored)
        compile_cases(restored, root)
        flpk_cases(restored, root)
        assert hashlib.sha256(scratch.read_bytes()).hexdigest() == digest
        print("RESTORED doccheck.py SHA256 " + digest)
    assert (ROOT / "tools/doccheck.py").read_text(encoding="utf-8-sig") == source


if __name__ == "__main__":
    main()
