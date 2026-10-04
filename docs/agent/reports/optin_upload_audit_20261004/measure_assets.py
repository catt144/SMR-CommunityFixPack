"""Read-only image and current predicted payload comparison for this audit."""
from pathlib import Path
import hashlib
import importlib.util
import json
import subprocess
from PIL import Image

root = Path(__file__).resolve().parents[4]
opt = root.parent / 'SMR-OptInPack'
launch = root.parent / 'SMR-OptInPack-launch'
print('COMMAND python docs/agent/reports/optin_upload_audit_20261004/measure_assets.py')
for repo in (root, opt):
    print('HEAD', repo, subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=repo).decode().strip())
for tree in (root, opt, launch):
    members = [tree / 'preview.png', *sorted((tree / 'store_screenshots').glob('*'))]
    assert members[1:]
    for path in members:
        with Image.open(path) as img:
            dimensions, format_name = img.size, img.format
            img.verify()
        size = path.stat().st_size
        print('IMAGE', json.dumps({'tree': str(tree), 'member': path.relative_to(tree).as_posix(),
              'bytes': size, 'dimensions': dimensions, 'format': format_name, 'below_2MiB': size < 2 * 1024 * 1024}))
        assert size < 2 * 1024 * 1024
    print('IMAGE_MEMBERS', tree, len(members), 'preview_plus_gallery', 1 + len(members[1:]))

spec = importlib.util.spec_from_file_location('audit_asset_predict', opt / 'tools/pack_predict.py')
predictor = importlib.util.module_from_spec(spec)
spec.loader.exec_module(predictor)
packed, _, links = predictor.predict(str(launch))
same, different = [], []
for name, _ in packed:
    a, b = opt / name, launch / name
    if a.is_file() and a.read_bytes() == b.read_bytes():
        same.append(name)
    else:
        different.append(name)
print('CURRENT_REPO_LAUNCH', json.dumps({'equal': same, 'different': different, 'compared': len(packed),
      'member_control': len(same) + len(different)}))
assert len(same) + len(different) == len(packed)
