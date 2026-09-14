#!/usr/bin/env python3
"""Exercise ck170 gates on disk copies; never corrupt the shared checkout."""
import hashlib
from pathlib import Path
import tempfile

from repair_pass_selftest import ROOT, load_copy


def marker_cases(m, root):
    path = root / "checklist.md"
    m.CHECKLIST = str(path)
    good = b"<!-- ck:1 status:closed owner:no -->\n"
    path.write_bytes(good)
    assert m.check_marker_integrity([])
    for label, broken in (
        ("unknown", good.replace(b"closed", b"bogus")),
        ("hyphenated", good.replace(b"closed", b"part-ruled")),
        ("malformed", good.replace(b"ck:1", b"ck:oops")),
        ("unterminated", good.replace(b" -->", b"")),
        ("status disagreement", good + good.replace(b"closed", b"open")),
        ("owner disagreement", good + good.replace(b"owner:no", b"owner:yes")),
    ):
        path.write_bytes(broken)
        out = []
        assert not m.check_marker_integrity(out), (label, out)
        assert any("; RED" in x for x in out), out
        print("PASS marker broken copy FAILS: " + label)
    path.write_bytes(good + good)
    out = []
    assert m.check_marker_integrity(out) and any("(agree)" in x for x in out), out
    path.write_bytes(good)
    assert m.check_marker_integrity([])
    assert path.read_bytes() == good
    print("RESTORED checklist SHA256 " + hashlib.sha256(path.read_bytes()).hexdigest())


def byte_cases(m, root):
    path = root / "STATE.md"
    m.STATE = str(path)
    m.STUBS = {}
    m.GENERAL_USE = str(root / "absent.md")
    m.PUSH_SET = [("fixture", lambda: str(path))]
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
    # ⏳ The live caps are TORN DOWN (owner 2026-09-14, SKILL_CAPS_DOWN). The cap
    # MACHINERY is still falsified here so that rebuilding it inherits a proven gate
    # rather than an untested one. The teardown itself is falsified at the end.
    m.SKILL_CAPS_DOWN = False
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
    # the teardown's own positive control: with caps DOWN an oversize skill PASSES,
    # and with them UP the same bytes FAIL. Proves the switch does what it claims.
    for p in paths:
        p.write_bytes(good * 2)          # 24 B against the 12 B test cap
    m.SKILL_CAPS_DOWN = True
    assert m.check_skills([]), "caps down should not gate on size"
    m.SKILL_CAPS_DOWN = False
    assert not m.check_skills([]), "caps up should gate on size"
    for p in paths:
        p.write_bytes(good)
    for p in paths:
        assert p.read_bytes() == good
    print("PASS skill cap FAILS both endings; raw mirror mismatch FAILS")
    print("RESTORED skill copies SHA256 " + hashlib.sha256(good).hexdigest())


def owner_cases(m):
    m.state_owed_lines = lambda: []
    for status in m.MARKER_STATUSES:
        for owner in (False, True):
            item = dict(status=status, owner=owner, num=999, date="2026-09-13",
                        source="marker", header="### fixture", line=1)
            rendered = m.render_waiting([item])
            assert any(x.startswith("| 999 |") for x in rendered) == owner, rendered
    item.update(status="ambiguous", source="inferred", owner=True)
    assert not any(x.startswith("| 999 |") for x in m.render_waiting([item]))


def main():
    live = ROOT / "tools/doccheck.py"
    original = live.read_bytes()
    source = original.decode("utf-8-sig")
    with tempfile.TemporaryDirectory(prefix="ck170-") as directory:
        root = Path(directory)
        scratch = root / "doccheck.py"
        m = load_copy(scratch, source)
        marker_cases(m, root)
        byte_cases(m, root)
        skill_cases(m, root)
        owner_cases(m)
        mutant = source.replace('waiting = [i for i in items if i["status"] in MARKER_STATUSES and i["owner"]]',
                                'waiting = [i for i in items if i["status"] == "open" and i["owner"]]')
        assert mutant != source
        try:
            owner_cases(load_copy(scratch, mutant))
        except AssertionError:
            print("PASS status-filter instrument mutant FAILS owner-action independence")
        else:
            raise AssertionError("owner-action mutant survived")
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
        marker_cases(restored, root)
        byte_cases(restored, root)
        skill_cases(restored, root)
        owner_cases(restored)
        assert scratch.read_bytes() == source.encode()
        print("RESTORED doccheck copy SHA256 " + hashlib.sha256(scratch.read_bytes()).hexdigest())
    assert live.read_bytes() == original
    print("UNCHANGED live doccheck SHA256 " + hashlib.sha256(original).hexdigest())


if __name__ == "__main__":
    main()
