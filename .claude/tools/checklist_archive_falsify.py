"""Exercise real --apply only in a byte-preserving scratch repository.

Run from the live repo root. The live checklist and archive are read only.
The date-only group is provisionally marked closed IN THE COPY to test the
proposed operation; this is neither owner approval nor a live marking action.
"""
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile

SOURCE = Path.cwd()
SCRATCH = Path(tempfile.mkdtemp(prefix='checklist-archive-'))
REPO = SCRATCH / 'SMR-BugFixPack'
REPO.mkdir()
CK = 'docs/PLAYTEST_CHECKLIST.md'
AR = 'docs/archive/PLAYTEST_ARCHIVE.md'
TOOL = '.claude/tools/archive_settled.py'
PLAN = json.loads((SOURCE / '.claude/checklist_archive_selection.json').read_text(encoding='utf-8'))
RESULTS = {'source_head': subprocess.check_output(['git', 'rev-parse', 'HEAD']).decode().strip(),
           'scratch': str(REPO), 'checks': [], 'moves': []}


def run(*args, ok=True):
    p = subprocess.run(args, cwd=REPO, capture_output=True, encoding='utf-8', errors='replace')
    if ok and p.returncode:
        raise AssertionError((args, p.returncode, p.stdout, p.stderr))
    return p


def copy_tracked(src, dst):
    names = subprocess.check_output(['git', 'ls-files', '-z'], cwd=src).decode().split('\0')
    for name in filter(None, names):
        origin = src / name
        if not origin.is_file():
            continue
        target = dst / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(origin, target)


def commit():
    run('git', 'add', '-A')
    run('git', 'commit', '--allow-empty', '-m', 'scratch checkpoint')


def regen_green():
    run(sys.executable, '-X', 'utf8', 'tools/doccheck.py', '--regen-waiting')
    p = run(sys.executable, '-X', 'utf8', 'tools/doccheck.py')
    assert p.stdout.rstrip().endswith('doccheck: GREEN'), p.stdout


def apply(group='1'):
    return run(sys.executable, '-X', 'utf8', TOOL, '--headers-file', 'group%s.json' % group, '--apply', ok=False)


def hashes():
    return {p: hashlib.sha256((REPO / p).read_bytes()).hexdigest() for p in (CK, AR)}


def verify_move(group):
    before = (REPO / CK).read_bytes()
    old_archive = (REPO / AR).read_bytes()
    # Independently locate selected body spans from original raw lines.
    lines = before.splitlines(keepends=True)
    offsets = [0]
    for line in lines:
        offsets.append(offsets[-1] + len(line))
    selected = {it['header'] for it in PLAN[group]}
    spans = []
    for i, line in enumerate(lines):
        if line.decode('utf-8').rstrip('\r\n') not in selected:
            continue
        assert lines[i + 1].startswith(b'<!-- ck:')
        end = next((j for j in range(i + 2, len(lines))
                    if lines[j].startswith((b'### ', b'## '))), len(lines))
        spans.append((offsets[i + 2], offsets[end], line, lines[i + 1]))
    assert len(spans) == len(selected)
    p = apply(group)
    assert p.returncode == 0 and 'APPLIED:' in p.stdout, p.stdout + p.stderr
    (SCRATCH / ('move%s.txt' % group)).write_text(p.stdout, encoding='utf-8')
    after = (REPO / CK).read_bytes()
    new_archive = (REPO / AR).read_bytes()
    assert len(re.findall(rb'^### ', before, re.M)) == len(re.findall(rb'^### ', after, re.M))
    assert new_archive.startswith(old_archive)
    tail = new_archive[len(old_archive):]
    eol = b'\r\n' if b'\r\n' in before else b'\n'
    expected = before
    pointer_total = 0
    body_total = 0
    for start, end, heading, marker in reversed(spans):
        label = re.search(rb'ck:(\d+|-)', marker)[1]
        pointer = eol + b'Body archived in [archive/PLAYTEST_ARCHIVE.md](archive/PLAYTEST_ARCHIVE.md); search `ck' + label + b'` and this heading.' + eol + eol
        expected = expected[:start] + pointer + expected[end:]
        pointer_total += len(pointer)
        body_total += end - start
    assert after == expected, 'surviving bytes or pointers changed'
    for start, end, heading, marker in spans:
        label = re.search(rb'ck:(\d+|-)', marker)[1]
        status = re.search(rb'status:([a-z]+)', marker)[1]
        prefix = eol + b'---' + eol + eol + b'## ck' + label + b' -- archived '
        assert tail.startswith(prefix)
        line_end = tail.index(eol, len(prefix)) + len(eol)
        assert b'(was checklist status:' + status + b'):' in tail[:line_end]
        assert tail[line_end:].startswith(eol), 'missing archive header separator'
        tail = tail[line_end + len(eol):]
        body = before[start:end]
        assert tail.startswith(body), 'archive body differs'
        tail = tail[len(body):]
    assert not tail, 'unexpected archive delta'
    assert len(after) == len(before) - body_total + pointer_total
    assert body_total == sum(it['body_bytes'] for it in PLAN[group]), 'reviewed body byte count drifted'
    RESULTS['moves'].append(dict(group=group, items=len(spans), body_bytes=body_total,
        checklist_before=len(before), checklist_after=len(after), pointer_bytes=pointer_total,
        archive_before=len(old_archive), archive_after=len(new_archive),
        archive_delta=len(new_archive)-len(old_archive),
        archive_wrapper_bytes=len(new_archive)-len(old_archive)-body_total,
        headers_before=len(re.findall(rb'^### ', before, re.M)),
        headers_after=len(re.findall(rb'^### ', after, re.M))))
    regen_green()
    commit()


try:
    copy_tracked(SOURCE, REPO)
    copy_tracked(SOURCE.parent / 'SMR-BugFixPack-TestKit', SCRATCH / 'SMR-BugFixPack-TestKit')
    for rel in (TOOL,):
        (REPO / rel).parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(SOURCE / rel, REPO / rel)
    for group, items in PLAN.items():
        (REPO / ('group%s.json' % group)).write_text(json.dumps([i['header'] for i in items]), encoding='utf-8')
    raw = (REPO / CK).read_bytes()
    eol = b'\r\n' if b'\r\n' in raw else b'\n'
    for it in PLAN['2']:
        header = it['header'].encode() + eol
        assert raw.count(header) == 1
        at = raw.index(header) + len(header)
        if not raw[at:].startswith(b'<!-- ck:'):
            raw = raw[:at] + b'<!-- ck:- status:closed owner:no -->' + eol + raw[at:]
    (REPO / CK).write_bytes(raw)
    run('git', 'init')
    run('git', 'config', 'user.name', 'Archive falsification')
    run('git', 'config', 'user.email', 'archive-falsification@example.invalid')
    run('git', 'config', 'core.autocrlf', 'false')
    regen_green()
    commit()
    baseline = {p: (REPO / p).read_bytes() for p in (CK, AR, 'AGENTS.md', 'README.md')}
    for dirty in (CK, AR):
        (REPO / dirty).write_bytes(baseline[dirty] + b'\nScratch dirty rail probe.\n')
        captured = hashes()
        p = apply()
        assert p.returncode != 0 and 'write-path cleanliness rail' in p.stdout and dirty in p.stdout, p.stdout
        assert hashes() == captured
        (REPO / dirty).write_bytes(baseline[dirty])
        RESULTS['checks'].append('PASS dirty write path refusal: ' + dirty)
    (REPO / 'AGENTS.md').write_bytes(baseline['AGENTS.md'] + b'\nScratch RED probe.\n')
    captured = hashes()
    p = apply()
    assert p.returncode != 0 and 'doccheck.py is not GREEN' in p.stdout, p.stdout
    assert hashes() == captured
    (REPO / 'AGENTS.md').write_bytes(baseline['AGENTS.md'])
    RESULTS['checks'].append('PASS whole-repo RED doccheck refusal')
    # A peer commit lands precisely after git cleanliness was measured, before
    # either atomic write. It is a real commit; the path is clean again.
    for race in (CK, AR):
        wrapper = '''import importlib.util,sys,subprocess
from pathlib import Path
s=importlib.util.spec_from_file_location('a',%r);a=importlib.util.module_from_spec(s);s.loader.exec_module(a)
original=a.git_is_clean
def race():
    result=original()
    p=Path(%r);p.write_bytes(p.read_bytes()+b'\\nCommitted peer edit.\\n')
    subprocess.check_call(['git','add','--',str(p)],stdout=subprocess.DEVNULL)
    subprocess.check_call(['git','commit','-m','peer edit'],stdout=subprocess.DEVNULL)
    assert original()[0]
    return result
a.git_is_clean=race
sys.argv=['archive_settled.py','--headers-file','group1.json','--apply']
sys.exit(a.main())
''' % (TOOL, race)
        p = run(sys.executable, '-X', 'utf8', '-c', wrapper, ok=False)
        assert p.returncode != 0 and 'SHA256 load-to-write rail' in p.stdout, p.stdout + p.stderr
        for path in (CK, AR):
            assert (REPO / path).read_bytes() == baseline[path] + (b'\nCommitted peer edit.\n' if path == race else b'')
        (REPO / race).write_bytes(baseline[race])
        commit()
        RESULTS['checks'].append('PASS SHA256 abort after clean peer commit: ' + race)
    # Dirty unrelated path must not block a legitimate, doccheck-GREEN move.
    (REPO / 'README.md').write_bytes(baseline['README.md'] + b'\nScratch unrelated edit.\n')
    verify_move('1')
    RESULTS['checks'].append('PASS unrelated dirty path allowed with GREEN doccheck')
    captured = hashes()
    p = apply('1')
    assert p.returncode != 0 and 'selection rail' in p.stdout, p.stdout
    assert hashes() == captured
    RESULTS['checks'].append('PASS already archived selection refuses; no pointer re-archival')
    verify_move('2')
    RESULTS['checks'].append('PASS both moves: headers, surviving bytes, exact archive delta, pointer tally, final doccheck')
    RESULTS['result'] = 'PASS'
finally:
    output = json.dumps(RESULTS, indent=2)
    (SCRATCH / 'results.json').write_text(output, encoding='utf-8')
    print(output, flush=True)
