"""Audit 86a2507 without checkout or game/account writes. Run from repo root."""
import hashlib
import importlib.util
import io
import json
import re
import subprocess
import sys
import zipfile
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
ROOT = Path.cwd().resolve()
REV = '86a25078adb705d6e64b8bdd25bb4c115ada214d'
TREE = ROOT / 'scratch/load_first_audit3_86a2507'
OUT = ROOT / 'scratch/load_first_audit3_results'
OUT.mkdir(exist_ok=True)
if not TREE.exists():
    with zipfile.ZipFile(io.BytesIO(subprocess.check_output(['git', 'archive', '--format=zip', REV]))) as z:
        z.extractall(TREE)

def emit(kind, data):
    print(kind, json.dumps(data, sort_keys=True))

def sha(data):
    return hashlib.sha256(data).hexdigest()

def run(name, args):
    p = subprocess.run([sys.executable, '-X', 'utf8', *args], cwd=TREE, capture_output=True)
    txt = (p.stdout + p.stderr).decode('utf-8').replace('\r\n', '\n')
    (OUT / (name + '.txt')).write_text(txt, encoding='utf-8', newline='\n')
    emit('RUN', {'command': ['python', *args], 'cwd': str(TREE), 'exit': p.returncode, 'name': name, 'tail': txt.splitlines()[-2:]})
    assert p.returncode == 0, name
    return txt

emit('IDENTITY', {'branch': REV, 'records': subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip()})
files = ['Code/00_Core.lua', 'Code/01_LoadFirst.lua', 'metadata.lua', 'items.lua', 'tools/desk_load_first.py',
         'tools/arming/payloads/98_LoadFirstSync.lua.txt', 'tools/arming/payloads/98_LoadFirstSet.lua.txt',
         'tools/arming/payloads/98_LoadFirstRead.lua.txt']
for rel in files:
    data = (TREE / rel).read_bytes()
    assert data == subprocess.check_output(['git', 'show', REV + ':' + rel]), rel
    emit('INPUT', {'file': rel, 'sha256': sha(data)})
assert (TREE / 'Code/01_LoadFirst.lua').read_bytes() == subprocess.check_output(['git','show','8ea5449:Code/01_LoadFirst.lua'])
txt = run('baseline_and_mutants', ['tools/desk_load_first.py'])
run('killers', ['tools/desk_load_first.py', '--list'])
sys.path.insert(0, str(TREE / 'tools'))
spec = importlib.util.spec_from_file_location('audited', TREE / 'tools/desk_load_first.py')
b = importlib.util.module_from_spec(spec)
spec.loader.exec_module(b)
members = [s for s in txt.splitlines() if s.startswith(('  PASS ', '  FAIL '))]
held = sum(s.startswith('  PASS ') for s in members)
assert 'BASELINE %d of %d demands held' % (held, len(members)) in txt
rows = []
for name in [*b.MUTANTS, *b.WITNESS_MUTANTS]:
    mutated = run('mutant_' + name, ['tools/desk_load_first.py', '--mutant', name])
    demands = [s for s in mutated.splitlines() if s.startswith(('  PASS ', '  FAIL '))]
    failed = [s for s in demands if s.startswith('  FAIL ')]
    assert len(demands) == len(members) and failed, name
    summary = next(s for s in txt.splitlines() if re.match(r'^  ' + re.escape(name) + r'\s+fails ', s))
    assert re.search(r'fails\s+%d of\s+%d demands' % (len(failed), len(demands)), summary), name
    rows.append({'name': name, 'failed': len(failed), 'total': len(demands), 'summary': summary.strip()})
emit('MUTANT_MEMBERS', rows)
emit('MUTANT_TOTAL', {'members': len(rows), 'with_failures': sum(r['failed'] > 0 for r in rows), 'baseline_held': held, 'baseline_demands': len(members)})
run('parsecheck', ['tools/parsecheck.py'])
repair = ROOT / 'docs/archive/load_order_first_repairs2_2026-09-26'
receipt = (repair / 'measurements.txt').read_text(encoding='utf-8')
for line in receipt.splitlines():
    m = re.fullmatch(r'  ([0-9a-f]{64})  (.+)', line)
    if m:
        data = (repair / m[2]).read_bytes()
        actual = sha(data)
        match = 'RAW' if actual == m[1] else 'PREARCHIVE_CRLF' if sha(data.replace(b'\n', b'\r\n')) == m[1] else 'MISMATCH'
        assert match != 'MISMATCH', m[2]
        emit('BUILDER_HASH', {'file': m[2], 'recorded_sha256': m[1], 'actual_sha256': actual, 'match': match})
witness = (TREE / b.WITNESS).read_text(encoding='utf-8')
unattended = witness.replace('MODE = "sitting"', 'MODE = "unattended"')
assert sha(unattended.encode()) == 'b2a5da7f3653efeedc9d5881a8622652002e4489e9a2f3c2e4d3e0806caf7285'
emit('UNATTENDED_HASH', sha(unattended.encode()))
log = next(repair.glob('L12*.log'))
lines = log.read_text(encoding='utf-8').splitlines()
filters = ['Lua revision: 405907', 'Loaded mod items for:', '[LOADFIRST-SYNC]', '[LUA ERROR]', 'Failed to get subscribed', 'PdxSDKMods']
counts = {}
for filt in filters:
    hits = [{'line': i, 'text': s} for i, s in enumerate(lines, 1) if filt in s]
    counts[filt] = len(hits)
    emit('LOG_FILTER', {'filter': filt, 'count': len(hits), 'members': hits})
assert counts['[LOADFIRST-SYNC]'] == 9 and counts['Lua revision: 405907'] == 1
assert counts['Loaded mod items for:'] == 1
emit('LOG_TOTAL', {'file': log.name, 'lines': len(lines), 'sha256': sha(log.read_bytes()), 'counts': counts})
