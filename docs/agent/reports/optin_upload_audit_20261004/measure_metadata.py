"""Read-only metadata comparison for the 2026-10-04 upload audit."""
from pathlib import Path
import hashlib, json, re, subprocess, sys

fix = Path('B:/Dev/SMR/SMR-BugFixPack')
opt = Path('B:/Dev/SMR/SMR-OptInPack')
launch = Path('B:/Dev/SMR/SMR-OptInPack-launch')
sys.path.insert(0, str(opt / 'tools'))
import store_parity as parity
import upload_preflight as preflight

for root in (fix, opt):
    print(root, subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=root).decode().strip())

for root in (fix, opt, launch):
    path = root / 'metadata.lua'
    data = path.read_bytes()
    src = data.decode('utf-8')
    parsed = preflight.parse_metadata(str(path))
    print('metadata', str(path), 'bytes', len(data), 'sha256', hashlib.sha256(data).hexdigest())
    explicit = re.findall(r"^\t'(\w+)',", src, re.M)
    print('explicit_fields', explicit)
    for key in ('title', 'short_description', 'description', 'last_changes'):
        raw_match, value = parity.metadata_field(src, key)
        print('length', key, 'codepoints', len(value), 'control_sum', sum(1 for c in value),
              'utf8_bytes', len(value.encode('utf-8')), 'utf16_units', len(value.encode('utf-16-le')) // 2,
              'LF', value.count('\n'), 'raw_preflight_length', len(parsed[key]),
              'non_ascii', sorted(set(c for c in value if ord(c) > 127)))
    for key in ('code', 'ignore_files', 'entities'):
        members = parsed.get(key, [])
        print('list', key, 'length', len(members), 'unique_length', len(set(members)), 'members', members)
        assert len(members) == len(set(members)), (str(path), key, 'duplicate member')
    option_match = re.search(r"^\t'default_options',\s*\{(.*?)^\t\},", src, re.M | re.S)
    options = re.sub(r'--[^\n]*', '', option_match.group(1)) if option_match else ''
    print('default_options', options.strip())

batch = json.loads((opt / 'docs/agent/support/RELEASE_BATCH.json').read_text(encoding='utf-8'))['batch']
print('batch', batch['id'], batch['base'], batch['kind'], batch['pre_upload'], batch['portals'])
manifest = batch['manifest']['metadata.lua']
print('manifest_metadata', manifest)
assert hashlib.sha256((launch / 'metadata.lua').read_bytes()).hexdigest() == manifest['sha256']
assert (opt / 'metadata.lua').read_bytes() == (launch / 'metadata.lua').read_bytes()

summary = '\n'.join([
    'Off/base until enabled in Mod Options:',
    '- Acknowledged warnings', '- Multiple Artificial Suns', '- Drone speed/carry dials',
    '- Service interest tags', '- Station import/export rows', '- Train Hub', '- Elevator Depot',
])
print('proposed_summary', repr(summary), len(summary), len(summary.encode('ascii')))
assert summary.isascii() and len(summary) <= 200
