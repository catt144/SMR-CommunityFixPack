#!/usr/bin/env python3
"""Falsify STATE's generated region on disk copies, including regen itself."""
import hashlib
from pathlib import Path
import tempfile
import types

from repair_pass_selftest import ROOT, load_copy

COUNTS = dict(modules=46, default_active=46, optional=0, files=47,
              probes=97, rows_F=119, rows_D=13, rows_C=93)
MARKER = b"BUILD STATE (emitted by tools/doccheck.py)"


def fixture(ending=b"\n"):
    prefix = "# Hand-authored é\n```python\nexample\n```\n\n```\n".encode()
    suffix = b"```\nKeep this prose.\n"
    return (prefix.replace(b"\n", ending),
            (MARKER + b"\n- stale\n").replace(b"\n", ending),
            suffix.replace(b"\n", ending))


def region_cases(m, root):
    path = root / "STATE.md"
    m.STATE = str(path)
    for ending in (b"\n", b"\r\n"):
        before, stale, after = fixture(ending)
        # The surrounding prose deliberately has different line endings.
        after += b"Mixed ending tail.\n"
        original = before + stale + after
        wanted = before + m.counts_block(COUNTS).encode().replace(b"\n", ending) + ending + after
        generated = m.state_counts_bytes(original, COUNTS)
        assert generated == wanted, "generation changed surrounding bytes or missed counts"
        assert m.state_counts_bytes(generated, COUNTS) == generated, "not byte-idempotent"
        path.write_bytes(original)
        out = []
        assert not m.check_state_counts(COUNTS, out), "stale region passed"
        assert any("STATE BUILD STATE: RED" in line for line in out), out
        assert any("--regen" in line for line in out), out
        assert path.read_bytes() == original, "freshness check wrote STATE"
        path.write_bytes(generated)
        assert m.check_state_counts(COUNTS, []), "fresh region failed"
    before, stale, after = fixture()
    for label, broken in (
        ("missing marker", before + b"- stale\n" + after),
        ("duplicate marker", before + stale + stale + after),
        ("duplicate region", (before + stale + after) * 2),
        ("missing opening fence", before[:-4] + stale + after),
        ("missing closing fence", before + stale + after[4:]),
        ("duplicate opening fence", before + b"```\n" + stale + after),
        ("duplicate closing fence", before + stale + b"```\n" + after),
        ("non-bare fence", before[:-4] + b"```text\n" + stale + after),
    ):
        path.write_bytes(broken)
        try:
            m.state_counts_bytes(broken, COUNTS)
        except m.StateCountsError:
            pass
        else:
            raise AssertionError(label + " was accepted")
        out = []
        assert not m.check_state_counts(COUNTS, out), (label, out)
        assert any("STATE BUILD STATE: RED" in line for line in out), out
        assert path.read_bytes() == broken
    total, line = m.STATE_MAX_BYTES, m.STATE_MAX_LINE_BYTES
    for ending in (b"\n", b"\r\n"):
        before, stale, after = fixture(ending)
        data = before + stale + after
        generated = m.state_counts_bytes(data, COUNTS).replace(b"\r\n", b"\n")
        for label, caps in (("total", (len(generated) - 1, line)),
                            ("line", (total, max(map(len, generated.split(b"\n"))) - 1))):
            m.STATE_MAX_BYTES, m.STATE_MAX_LINE_BYTES = caps
            try:
                m.state_counts_bytes(data, COUNTS)
            except m.StateCountsError:
                pass
            else:
                raise AssertionError(label + " cap was ignored")
            finally:
                m.STATE_MAX_BYTES, m.STATE_MAX_LINE_BYTES = total, line
    absent = dict(COUNTS, probes=None)
    assert b"not counted (TestKit absent)" in m.state_counts_bytes(data, absent)
    print("PASS region: LF/CRLF, mixed surrounding bytes, idempotence, RED drift, delimiters, caps")


def regen_cases(m, root):
    root.mkdir(exist_ok=True)
    m.STATE = str(root / "STATE.md")
    m.BUGS_DIR, m.FACTS_DIR = str(root / "bugs"), str(root / "facts")
    m.CLAUDE_MD, m.AGENTS_MD = str(root / "CLAUDE.md"), str(root / "AGENTS.md")
    m.WAITING_MD = str(root / "WAITING.md")
    def write_lines(path, lines):
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        Path(path).write_bytes(("\n".join(lines) + "\n").encode())
    sb = types.SimpleNamespace(load_from_dir=lambda: {}, render_index=lambda model: ["index"],
                               write_lines=write_lines)
    m.splitter = m.facts_splitter = lambda: sb
    m.recount = lambda model, out: COUNTS
    m.regen_skills = lambda: None
    m.checklist_items = lambda: []
    m.render_waiting = lambda items: ["waiting"]
    Path(m.CLAUDE_MD).write_bytes(b"entry\r\n")
    state = Path(m.STATE)
    original = b"".join(fixture())
    state.write_bytes(original)
    m.regen([])
    expected = m.state_counts_bytes(original, COUNTS)
    assert state.read_bytes() == expected, "regen failed to refresh STATE"
    assert m.check_state_counts(COUNTS, [])
    digest = hashlib.sha256(state.read_bytes()).hexdigest()
    m.regen([])
    assert hashlib.sha256(state.read_bytes()).hexdigest() == digest
    assert Path(m.AGENTS_MD).read_bytes() == Path(m.CLAUDE_MD).read_bytes()
    state.write_bytes(original.replace(MARKER, b"missing"))
    snapshots = {p: p.read_bytes() for p in root.rglob("*") if p.is_file()}
    try:
        m.regen([])
    except m.StateCountsError:
        pass
    else:
        raise AssertionError("regen accepted a missing delimiter")
    assert snapshots == {p: p.read_bytes() for p in root.rglob("*") if p.is_file()}
    state.write_bytes(expected)
    m.regen([])
    assert hashlib.sha256(state.read_bytes()).hexdigest() == digest
    print("PASS regen: refresh, byte-identical second pass, invalid region writes nothing")
    print("RESTORED STATE fixture SHA256", digest)


def main():
    live = ROOT / "tools/doccheck.py"
    original = live.read_bytes()
    source = original.decode("utf-8-sig")
    with tempfile.TemporaryDirectory(prefix="state-counts-") as directory:
        root = Path(directory)
        scratch = root / "doccheck.py"
        m = load_copy(scratch, source)
        region_cases(m, root)
        regen_cases(m, root / "regen")
        for label, mutant, cases in (
            ("region replacement", source.replace("    return result\n", "    return data\n"), region_cases),
            ("regen write", source.replace("    if state_before != state_after:", "    if False:"), regen_cases),
        ):
            assert mutant != source
            broken = load_copy(scratch, mutant)
            try:
                cases(broken, root / "regen")
            except AssertionError:
                print("PASS instrument mutant FAILS:", label)
            else:
                raise AssertionError(label + " mutant survived")
        restored = load_copy(scratch, source)
        region_cases(restored, root)
        regen_cases(restored, root / "regen")
        assert scratch.read_bytes() == source.encode()
        print("RESTORED doccheck copy SHA256", hashlib.sha256(scratch.read_bytes()).hexdigest())
    assert live.read_bytes() == original
    print("UNCHANGED live doccheck SHA256", hashlib.sha256(original).hexdigest())


if __name__ == "__main__":
    main()
