#!/usr/bin/env python3
"""Repair-pass falsifiers; mutants execute only in a temporary directory.

Run: python tools/repair_pass_selftest.py
Each demand is paired with a control and rerun against a reverted scratch copy.
"""
import hashlib
from pathlib import Path
import sys
import tempfile
import types

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))


def load_copy(path, source):
    path.write_bytes(source.encode("utf-8"))
    module = types.ModuleType("repair_scratch")
    module.__file__ = str(path)
    exec(compile(source, str(path), "exec"), module.__dict__)
    return module


def marker_cases(module, demand=None):
    control = ["<!-- ck:1 status:closed owner:no -->"]
    out = []
    module.marker_integrity(control, out)
    assert not any("warn " in x or "; WARN" in x for x in out), out
    demands = (
        (["<!-- ck:2 status:part-ruled owner:yes -->"],
         ("1 on disk, 0 parsed; WARN", "line 1: unparsed", "unknown status part-ruled")),
        (["<!-- ck:3 status:bogus owner:yes -->"],
         ("1 on disk, 1 parsed; WARN", "unknown status bogus")),
        (control + control, ("duplicate ck:1 at lines 1, 2",)),
        (["<!-- ck:oops status:closed owner:no -->"], ("line 1: unparsed",)),
    )
    selected = demands if demand is None else (demands[demand],)
    for lines, needles in selected:
        out = []
        module.marker_integrity(lines, out)
        assert all(any(n in x for x in out) for n in needles), out


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


def main():
    source = (ROOT / "tools/doccheck.py").read_text(encoding="utf-8-sig")
    digest = hashlib.sha256(source.encode()).hexdigest()
    with tempfile.TemporaryDirectory(prefix="smr-repair-") as directory:
        scratch = Path(directory) / "doccheck.py"
        fixed = load_copy(scratch, source)
        marker_cases(fixed)
        fingerprint_cases(fixed)
        print("PASS A1/A2 controls and all demands on repaired copy")
        # Revert integrity reporting to its pre-repair silence.
        a1 = source.index("def marker_integrity(")
        end = source.index("def check_marker_integrity(", a1)
        mutant = source[:a1] + (
            'def marker_integrity(lines, out):\n'
            '    pass\n\n\n'
        ) + source[end:]
        broken = load_copy(scratch, mutant)
        for demand in range(4):
            try:
                marker_cases(broken, demand)
            except AssertionError:
                print("PASS A1 reverted scratch demand %d: control passes, demand FAILS" % demand)
            else:
                raise AssertionError("A1 mutant survived")
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
        marker_cases(restored)
        fingerprint_cases(restored)
        if hasattr(restored, "pack_ignore_parity"):
            parity_cases(restored, Path(directory))
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
                parity_cases(broken, Path(directory))
            except AssertionError:
                print("PASS B2 reverted scratch: control passes, drift demand FAILS")
            else:
                raise AssertionError("B2 mutant survived")
            restored = load_copy(scratch, source)
            marker_cases(restored)
            fingerprint_cases(restored)
            parity_cases(restored, Path(directory))
        assert hashlib.sha256(scratch.read_bytes()).hexdigest() == digest
        print("RESTORED doccheck.py SHA256 " + digest)
    assert (ROOT / "tools/doccheck.py").read_text(encoding="utf-8-sig") == source


if __name__ == "__main__":
    main()
