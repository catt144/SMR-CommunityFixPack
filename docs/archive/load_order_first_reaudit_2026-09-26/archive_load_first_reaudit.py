"""Append fresh re-audit receipts; never rewrite an existing archive path."""
from pathlib import Path
import difflib
import hashlib
import re
import subprocess

root = Path.cwd()
source = root / 'scratch/load_first_reaudit_results'
dest = root / 'docs/archive/load_order_first_reaudit_2026-09-26'
assert not dest.exists(), dest
branch = subprocess.check_output(['git', 'show', '8ea5449:metadata.lua']).decode('utf-8')
decoded = (source / 'decoded_nosave/metadata.lua').read_text(encoding='utf-8')
expected = branch.replace("'title', \"Relaunched Fix Pack\"", "'title', \"LoadFirst canary scratch (delete me)\"").replace("'id', \"SMR_CommunityFixPack\"", "'id', \"SMR_LoadFirstCanaryScratch\"")
expected = re.sub(r"^\s*'(?:pdx_id|pdx_version|steam_id)',[^\n]*\n", '', expected, flags=re.M)
assert expected == decoded, 'Unexpected scratch metadata transformation'
comparison = 'COMMAND: python scratch/archive_load_first_reaudit.py\n'
comparison += 'AUDITED_CODE: 8ea54494362a2d0cf2e8a49225870fcf5245774e\n'
comparison += 'CONTROL: decoded no-save metadata equals branch after only title/id substitution and removal of pdx_id/pdx_version/steam_id\n'
comparison += ''.join(difflib.unified_diff(branch.splitlines(True), decoded.splitlines(True), fromfile='8ea5449:metadata.lua', tofile='decoded_nosave/metadata.lua'))
dest.mkdir()
for path in sorted(source.glob('*.txt')):
    (dest / path.name).write_text(path.read_text(encoding='utf-8'), encoding='utf-8', newline='\n')
for name in ['load_first_reaudit.py', 'load_first_reaudit_counterexamples.py', 'archive_load_first_reaudit.py']:
    (dest / name).write_text((root / 'scratch' / name).read_text(encoding='utf-8'), encoding='utf-8', newline='\n')
(dest / 'metadata_comparison.txt').write_text(comparison, encoding='utf-8', newline='\n')
print(comparison)
print('ARCHIVED', dest)
