"""Append measurements and bind measured bytes to the repair commit."""
from pathlib import Path
import hashlib
import json
import subprocess
root = Path.cwd()
src = root/'scratch/load_first_repair3_results'
dest = root/'docs/archive/load_order_first_repairs3_2026-09-26'
assert not dest.exists(),dest
receipt=(root/'scratch/load_first_repair3_receipt.txt').read_text(encoding='utf-8')
rev='1325db54a0ec2a835b694eed8b1034817d08f948'
inputs=[json.loads(line[6:]) for line in receipt.splitlines() if line.startswith('INPUT ')]
binding=[]
for row in inputs:
    data=subprocess.check_output(['git','show',rev+':'+row['file']])
    assert hashlib.sha256(data).hexdigest()==row['sha256'],row['file']
    binding.append('COMMIT_INPUT_MATCH '+json.dumps(row,sort_keys=True))
receipt+='\nCOMMITTED_CODE '+rev+'\n'+'\n'.join(binding)+'\n'
dest.mkdir()
for p in src.glob('*.txt'):
    (dest/p.name).write_text(p.read_text(encoding='utf-8'),encoding='utf-8',newline='\n')
for name in ['measure_load_first_repair3.py','archive_load_first_repair3.py']:
    (dest/name).write_text((root/'scratch'/name).read_text(encoding='utf-8'),encoding='utf-8',newline='\n')
(dest/'receipt.txt').write_text(receipt,encoding='utf-8',newline='\n')
print('APPENDED',dest)
print('COMMIT INPUTS MATCH',rev)
