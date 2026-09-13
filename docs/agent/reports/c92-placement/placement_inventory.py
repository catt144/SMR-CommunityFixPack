"""Read-only C92 source authoring census; writes evidence only beside this file.

The parser reads the generated top-level PlaceObj blocks, then first-level
assignment lines. It does not interpret Lua or execute any game function.
"""
from pathlib import Path
from collections import Counter
import csv
import hashlib
import json
import re
import subprocess

OUT = Path(__file__).resolve().parent
OLD = Path('C:/Dev/SMR-SrcArchive/1.0.7.396349/Src')
NEW = Path('C:/Dev/SMR-SrcArchive/1.1.0.403908/Src')
LIVE = Path('A:/SteamLibrary/steamapps/common/Project Spark/ModTools/Src')


def read_presets(path, kind):
    text = path.read_text(encoding='utf-8-sig')
    starts = list(re.finditer(r"^PlaceObj\('" + kind + r"', \{", text, re.M))
    rows = {}
    for i, start in enumerate(starts):
        end = starts[i + 1].start() if i + 1 < len(starts) else len(text)
        body = text[start.start():end]
        props = dict(re.findall(r'^\t(\w+) = (.*),$', body, re.M))
        ident = props['id'].strip('"')
        assert ident not in rows, ident
        props = {k: v.strip('"') for k, v in props.items()}
        props.update(line=text.count('\n', 0, start.start()) + 1, body=body)
        props['connections'] = ';'.join(re.findall(r"'To', \"([^\"]+)\"", body))
        rows[ident] = props
    assert len(rows) == text.count("\nPlaceObj('" + kind + "', {")
    return rows


def write_tsv(name, fields, rows):
    with (OUT / name).open('w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fields, delimiter='\t', extrasaction='ignore')
        writer.writeheader()
        writer.writerows(rows)


old = read_presets(OLD / 'Data/TechPreset.lua', 'TechPreset')
new = read_presets(NEW / 'Data/Tech.lua', 'Tech')
dlc = read_presets(NEW / 'DLC/norman/Presets/Tech.lua', 'Tech')
assert 'AdvancedDroneDrive' in old and 'UndergroundExploitation' in new
assert new['UndergroundExploitation']['group'] == 'Underground_1'
assert new['UndergroundDeepMining']['connections']
common = sorted(old.keys() & new.keys())
mapping = [dict(id=ident, old_group=old[ident].get('group', ''),
                old_position=old[ident].get('position', ''),
                old_SortKey=old[ident].get('SortKey', ''),
                new_group=new[ident].get('group', ''),
                new_MapPos=new[ident].get('MapPos', ''),
                new_Obsolete=new[ident].get('Obsolete', ''),
                old_line=old[ident]['line'], new_line=new[ident]['line']) for ident in common]
write_tsv('placement_old_to_new.tsv', list(mapping[0]), mapping)
details = [row for ident, row in sorted(new.items())]
fields = ['id', 'group', 'MapPos', 'SortKey', 'LockState', 'Unknown', 'Obsolete',
          'Condition', 'Comment', 'TODO', 'connections', 'line']
write_tsv('placement_new_authoring.tsv', fields, details)
conversion_ids = {
    'Policy_DroneHubEfficiency': 'DroneHubEfficiency',
    'Policy_ShuttleFuelEfficiency': 'ShuttleFuelEfficiency',
    'Policy_SensorTowers_ExtraScanning': 'SensorTowers',
    'Policy_MartianDiet': 'MartianDiet',
    'Policy_UndergroundExploitation': 'UndergroundExploitation',
    'Policy_UndergroundMiningPermits': 'UndergroundDeepMining',
    'Policy_UndergroundWaterPermits': 'UndergroundWaterExtraction',
    'Policy_AsteroidDeepMining': 'DeepAsteroid_Extraction',
    'Policy_SpaceFarming': 'Space_Farming',
}
old_laws, new_laws = {}, {}
for root, dest in [(OLD, old_laws), (NEW, new_laws)]:
    for path in (root / 'Data/LawDef').glob('*.lua'):
        for ident, row in read_presets(path, 'LawDef').items():
            assert ident not in dest
            dest[ident] = dict(row, file=str(path.relative_to(root)))
conversion_rows = []
for law_id, tech_id in conversion_ids.items():
    assert law_id in old_laws and new_laws[law_id].get('Obsolete') == 'true'
    assert tech_id in new, tech_id
    conversion_rows.append(dict(old_law=law_id, old_group=old_laws[law_id]['group'],
                               old_file=old_laws[law_id]['file'], old_line=old_laws[law_id]['line'],
                               new_law_line=new_laws[law_id]['line'],
                               old_prerequisite_no_underground='NoUndergroundAndAsteroids' in old_laws[law_id]['body'],
                               tech_id_existed_in_old=tech_id in old,
                               **{k:new[tech_id].get(k, '') for k in fields}))
write_tsv('placement_conversion_controls.tsv', list(conversion_rows[0]), conversion_rows)
live_nodes = {ident:row for ident,row in new.items()
              if row.get('LockState') != 'hidden' and row.get('Obsolete') != 'true'
              and row.get('MapPos')}
for row in live_nodes.values():
    row['xy'] = tuple(map(int, re.fullmatch(r'point\((\d+), (\d+)\)', row['MapPos']).groups()))
slots = {'Hi-Tech I gap': (7768,2816), 'Industry V right gap': (10062,2944),
         'Industry V upper-right gap': (9988,2816), 'Underground-Industry bridge': (9914,3200),
         'Underground sibling-row west': (9470,3200), 'Underground sibling-row east': (9618,3200)}
slot_rows = []
for slot, (x,y) in slots.items():
    neighbours = [(ident,row) for ident,row in live_nodes.items()
                  if (abs(row['xy'][0]-x), abs(row['xy'][1]-y)) in [(148,0),(74,128)]]
    occupied = [ident for ident,row in live_nodes.items() if row['xy'] == (x,y)]
    slot_rows.append(dict(slot=slot, x=x, y=y, occupied=';'.join(occupied),
                          adjacent_ids=';'.join(ident for ident,row in neighbours),
                          adjacent_groups=';'.join(row['group'] for ident,row in neighbours)))
write_tsv('placement_slots.tsv', list(slot_rows[0]), slot_rows)
transitions = Counter((r['old_group'], r['old_position'], r['new_group'], r['new_Obsolete']) for r in mapping)
write_tsv('placement_mapping_summary.tsv', ['old_group', 'old_position', 'new_group', 'new_Obsolete', 'count'],
          [dict(old_group=a, old_position=b, new_group=c, new_Obsolete=d, count=n)
           for (a,b,c,d), n in sorted(transitions.items())])
fingerprints = {}
for relative in ['Data/Tech.lua', 'Data/TechGroup.lua', 'Data/XPresetMapLabel.lua', 'DLC/norman/Presets/Tech.lua']:
    a = hashlib.sha256((NEW / relative).read_bytes()).hexdigest()
    b = hashlib.sha256((LIVE / relative).read_bytes()).hexdigest()
    assert a == b, relative
    fingerprints[relative] = a
manifest = Path('A:/SteamLibrary/steamapps/appmanifest_3215050.acf').read_text()
manifest_ids = {key: re.search(r'"' + key + r'"\s+"([^"]+)"', manifest).group(1)
                for key in ['appid', 'installdir', 'buildid']}
summary = dict(command='python docs/agent/reports/c92-placement/placement_inventory.py',
               head=subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip(),
               old_version='1.0.7.396349', new_version='1.1.0.403908',
               appmanifest=manifest_ids,
               archive_matches_live_sha256=fingerprints,
               old_presets=len(old), new_presets=len(new), dlc_presets=len(dlc),
               shared_ids=len(common),
               old_only=sorted(old.keys() - new.keys()),
               new_only=sorted(new.keys() - old.keys()),
               new_sortkey_present=sum('SortKey' in v for v in new.values()),
               old_positions=sum('position' in v for v in old.values()),
               old_MapPos_present=sum('MapPos' in v for v in old.values()),
               old_sortkeys=sum('SortKey' in v for v in old.values()),
               conversion_controls=len(conversion_rows),
               compared_new_tech_ids=sum(not r['tech_id_existed_in_old'] for r in conversion_rows),
               compared_preexisting_tech_ids=[r['id'] for r in conversion_rows if r['tech_id_existed_in_old']],
               new_group_counts=dict(Counter(v.get('group') for v in new.values())),
               dlc_ids=list(dlc))
(OUT / 'placement_inventory.json').write_text(json.dumps(summary, indent=2) + '\n', encoding='utf-8')
print(json.dumps({k:v for k,v in summary.items() if k not in ['appmanifest', 'new_only']}, indent=2))
for group in ['Underground_1', 'Hi-Tech_1', 'Industry_5']:
    print('\nGROUP', group)
    for ident, v in new.items():
        if v.get('group') == group:
            print(json.dumps({k: v.get(k, '') for k in fields}))
print('\nCONVERSIONS')
for ident in conversion_ids.values():
    print(json.dumps({k:new[ident].get(k, '') for k in fields}))
