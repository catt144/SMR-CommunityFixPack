"""Owner-authorized two-group execution; verification from raw snapshots."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile

group = sys.argv[1]
expected = {'1': (761372, 718296, 44288, 1212),
            '2': (718296, 605603, 115333, 2640)}[group]
ck = Path('docs/PLAYTEST_CHECKLIST.md')
ar = Path('docs/archive/PLAYTEST_ARCHIVE.md')
tool = [sys.executable, '-X', 'utf8', '.claude/tools/archive_settled.py',
        '--headers-file', '.claude/checklist_archive_group%s.json' % group]


def command(args):
    p = subprocess.run(args, capture_output=True, encoding='utf-8', errors='replace')
    assert p.returncode == 0, p.stdout + p.stderr
    return p.stdout


def check_tally(output):
    fields = ['checklist live before', 'checklist live after (built)',
              'archived (sum of MOVE body)', 'stub pointers added']
    values = tuple(int(re.search(re.escape(field) + r'\s*:\s*(\d+)', output)[1]) for field in fields)
    assert values == expected, (values, expected)
    assert re.search(r'^balance check:.* -> True$', output, re.M), output
    print(output[output.index('---- TALLY'):], flush=True)


assert not command(['git', 'status', '--porcelain']).strip(), 'tree dirty before planning'
head = command(['git', 'rev-parse', 'HEAD']).strip()
before, archive_before = ck.read_bytes(), ar.read_bytes()
assert len(before) == expected[0]
check_tally(command(tool))
snapshot = Path(tempfile.mkdtemp(prefix='checklist-live-group%s-' % group))
(snapshot / 'checklist.before').write_bytes(before)
(snapshot / 'archive.before').write_bytes(archive_before)
selected = set(json.loads(Path(tool[-1]).read_text(encoding='utf-8')))
lines = before.splitlines(keepends=True)
offsets = [0]
for line in lines:
    offsets.append(offsets[-1] + len(line))
spans = []
for i, line in enumerate(lines):
    if line.decode('utf-8').rstrip('\r\n') not in selected:
        continue
    assert lines[i+1].startswith(b'<!-- ck:')
    end = next((j for j in range(i+2, len(lines))
                if lines[j].startswith((b'### ', b'## '))), len(lines))
    spans.append((offsets[i+2], offsets[end], line, lines[i+1]))
assert len(spans) == len(selected)
assert ck.read_bytes() == before and ar.read_bytes() == archive_before
assert not command(['git', 'status', '--porcelain']).strip(), 'tree dirty immediately before apply'
output = command(tool + ['--apply'])
(snapshot / 'apply.txt').write_text(output, encoding='utf-8')
check_tally(output)
after, archive_after = ck.read_bytes(), ar.read_bytes()
assert len(after) == expected[1]
headers_before = len(re.findall(rb'^### ', before, re.M))
headers_after = len(re.findall(rb'^### ', after, re.M))
assert headers_before == headers_after == 160
eol = b'\r\n' if b'\r\n' in before else b'\n'
rebuilt = before
for start, end, heading, marker in reversed(spans):
    label = re.search(rb'ck:(\d+|-)', marker)[1]
    pointer = eol + b'Body archived in [archive/PLAYTEST_ARCHIVE.md](archive/PLAYTEST_ARCHIVE.md); search `ck' + label + b'` and this heading.' + eol + eol
    rebuilt = rebuilt[:start] + pointer + rebuilt[end:]
assert after == rebuilt, 'surviving bytes or pointer mismatch'
assert archive_after.startswith(archive_before)
tail = archive_after[len(archive_before):]
for start, end, heading, marker in spans:
    label = re.search(rb'ck:(\d+|-)', marker)[1]
    status = re.search(rb'status:([a-z]+)', marker)[1]
    prefix = eol + b'---' + eol + eol + b'## ck' + label + b' -- archived '
    assert tail.startswith(prefix)
    line_end = tail.index(eol, len(prefix)) + len(eol)
    assert b'(was checklist status:' + status + b'):' in tail[:line_end]
    assert tail[line_end:].startswith(eol)
    tail = tail[line_end+len(eol):]
    body = before[start:end]
    assert tail.startswith(body), 'archive body differs'
    tail = tail[len(body):]
assert not tail, 'unexpected archive delta'
print(command(['git', 'status', '--short']), flush=True)
command([sys.executable, '-X', 'utf8', 'tools/doccheck.py', '--regen-waiting'])
doccheck = command([sys.executable, '-X', 'utf8', 'tools/doccheck.py'])
assert doccheck.rstrip().endswith('doccheck: GREEN'), doccheck
marker_line = next(line for line in doccheck.splitlines() if line.startswith('MARKER INTEGRITY:'))
counts = re.search(r'(\d+) on disk, (\d+) parsed', marker_line)
assert counts[1] == counts[2]
result = dict(group=group, source_head=head, snapshot=str(snapshot),
    checklist_before=len(before), checklist_after=len(after),
    items=len(spans), body_bytes=sum(end-start for start,end,_,_ in spans),
    pointer_bytes=expected[3], archive_before=len(archive_before), archive_after=len(archive_after),
    archive_delta=len(archive_after)-len(archive_before), headers_before=headers_before,
    headers_after=headers_after, marker_integrity=marker_line, balance=True,
    surviving_bytes='identical', archive_bodies='identical; only declared wrappers added', doccheck='GREEN',
    checklist_after_sha256=hashlib.sha256(after).hexdigest(),
    archive_after_sha256=hashlib.sha256(archive_after).hexdigest())
(snapshot / 'doccheck.txt').write_text(doccheck, encoding='utf-8')
Path('.claude/checklist_archive_live_group%s.json' % group).write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
Path('.claude/checklist_archive_live_group%s_commit.txt' % group).write_text(
    'Archive checklist group %s after owner all-clear\n\n' % group
    + '%d bodies / %d bytes; checklist %d -> %d bytes.\n' % (len(spans), expected[2], expected[0], expected[1])
    + '160 headings retained; surviving bytes and archive bodies verified.\n'
    + 'Pointers balance; all markers parsed; doccheck GREEN.\n'
    + 'Owner approved both moves 2026-09-14. Executed by Codex (GPT-6).\n', encoding='utf-8')
print(json.dumps(result, indent=2), flush=True)
