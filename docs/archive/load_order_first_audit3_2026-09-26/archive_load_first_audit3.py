"""Append this audit's evidence without rewriting any existing archive."""
from pathlib import Path
root = Path.cwd()
out = root / 'docs/archive/load_order_first_audit3_2026-09-26'
assert not out.exists(), out
out.mkdir()
for path in (root / 'scratch/load_first_audit3_results').glob('*.txt'):
    (out / path.name).write_text(path.read_text(encoding='utf-8'), encoding='utf-8', newline='\n')
for name in ['load_first_audit3.py', 'load_first_audit3_counterexamples.py', 'archive_load_first_audit3.py']:
    (out / name).write_text((root / 'scratch' / name).read_text(encoding='utf-8'), encoding='utf-8', newline='\n')
(out / 'receipt.txt').write_text((root / 'scratch/load_first_audit3_receipt.txt').read_text(encoding='utf-8'), encoding='utf-8', newline='\n')
print('APPENDED', out)
