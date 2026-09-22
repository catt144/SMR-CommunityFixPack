#!/usr/bin/env python3
"""Exercise ck170 gates on disk copies; never corrupt the shared checkout."""
import hashlib
from pathlib import Path
import tempfile

from repair_pass_selftest import ROOT, load_copy


def byte_cases(m, root):
    path = root / "STATE.md"
    m.STATE = str(path)
    m.STUBS = {}
    m.GENERAL_USE = str(root / "absent.md")
    m.PUSH_SET = [("fixture", lambda: m._file_size_or_none(str(path)))]
    m.STATE_MAX_BYTES, m.STATE_WARN_BYTES, m.STATE_MAX_LINE_BYTES = 12, 10, 5
    m.PUSH_BUDGET = 12
    good = b"abcde\nabcde\n"
    readings = []
    for data in (good, good.replace(b"\n", b"\r\n")):
        path.write_bytes(data)
        out = []
        assert m.check_state_and_stubs(out), out
        m.push_set_report(out)
        readings.append(out)
    assert readings[0] == readings[1], readings
    for label, data, expected in (
        ("total cap", good + b"x\n", "hard cap"),
        ("line cap", b"abcdef\n", "per-line cap"),
    ):
        for ending in (b"\n", b"\r\n"):
            path.write_bytes(data.replace(b"\n", ending))
            out = []
            assert not m.check_state_and_stubs(out), (label, out)
            assert any(expected in x for x in out), out
        print("PASS byte broken copies FAIL: " + label + " (LF and CRLF)")
    # Multi-byte UTF-8 measures bytes, not characters.
    path.write_bytes("é\r\n".encode())
    assert m.lf_bytes(path) == b"\xc3\xa9\n"
    path.write_bytes(good)
    assert m.check_state_and_stubs([])
    assert path.read_bytes() == good
    print("RESTORED STATE SHA256 " + hashlib.sha256(path.read_bytes()).hexdigest())


def skill_cases(m, root):
    m.SKILLS_DIR = str(root / "skills")
    m.CODEX_SKILLS_DIR = str(root / "mirror")
    m.SKILL_HARD, m.SKILL_WARN = 12, 10
    m.IMPORTED_SKILLS = ()   # user-level imports are machine-global; the fixture
                             # tests mirror identity and the caps, not imports
    paths = [Path(base) / "fixture/SKILL.md"
             for base in (m.SKILLS_DIR, m.CODEX_SKILLS_DIR)]
    good = b"abcde\nabcde\n"
    readings = []
    for ending in (b"\n", b"\r\n"):
        for p in paths:
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_bytes(good.replace(b"\n", ending))
        out = []
        assert m.check_skills(out), out
        readings.append(out)
        for p in paths:
            p.write_bytes((good + b"x\n").replace(b"\n", ending))
        assert not m.check_skills([])
    assert readings[0] == readings[1], readings
    for p in paths:
        p.write_bytes(good)
    assert m.check_skills([])
    paths[1].write_bytes(good.replace(b"\n", b"\r\n"))
    assert not m.check_skills([])  # mirror identity is still RAW bytes
    paths[1].write_bytes(good)
    assert m.check_skills([])
    # the size gate itself: oversize bytes against the test cap FAIL. (Until
    # 2026-09-20 this was gated by SKILL_CAPS_DOWN, torn down 09-14 while the
    # skill set was being built; the teardown ended by owner ruling and the
    # switch is gone, so the gate is unconditional now.)
    for p in paths:
        p.write_bytes(good * 2)          # 24 B against the 12 B test cap
    assert not m.check_skills([]), "size cap should gate"
    for p in paths:
        p.write_bytes(good)
    for p in paths:
        assert p.read_bytes() == good
    print("PASS skill cap FAILS both endings; raw mirror mismatch FAILS")
    print("RESTORED skill copies SHA256 " + hashlib.sha256(good).hexdigest())


def main():
    live = ROOT / "tools/doccheck.py"
    original = live.read_bytes()
    source = original.decode("utf-8-sig")
    with tempfile.TemporaryDirectory(prefix="ck170-") as directory:
        root = Path(directory)
        scratch = root / "doccheck.py"
        m = load_copy(scratch, source)
        byte_cases(m, root)
        skill_cases(m, root)
        # Falsify the measuring instrument itself: raw-byte counting must lose
        # LF/CRLF equivalence. The unchanged LF control still passes.
        mutant = source.replace('.replace(b"\\r\\n", b"\\n")', '')
        assert mutant != source
        broken = load_copy(scratch, mutant)
        try:
            byte_cases(broken, root)
        except AssertionError:
            print("PASS raw-byte instrument mutant FAILS equivalence")
        else:
            raise AssertionError("raw-byte mutant survived")
        restored = load_copy(scratch, source)
        byte_cases(restored, root)
        skill_cases(restored, root)
        assert scratch.read_bytes() == source.encode()
        print("RESTORED doccheck copy SHA256 " + hashlib.sha256(scratch.read_bytes()).hexdigest())
    assert live.read_bytes() == original
    print("UNCHANGED live doccheck SHA256 " + hashlib.sha256(original).hexdigest())


if __name__ == "__main__":
    main()
