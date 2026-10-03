#!/usr/bin/env python3
"""C122 source/log receipt: re-read cargo loss and booking arithmetic; not a gameplay control.

Run: python tools/desk_c122_train_spoilage.py
Uses archived 1.1.1.406343 (Steam build 25579348) and the sibling's archived
34b log. Prints direct spoilage-name matches with members and total, source
spans, and primary log records. Assertions fail when the cited evidence moves.
This does not establish absence of indirect/native cargo writers, validate the
trap's instrumentation, or replace the missing earlier unload-witness log.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT.parent / 'SMR-Shared/SMR-SrcArchive/1.1.1.406343/Src'
ARCHIVE = ROOT.parent / 'SMR-OptInPack/docs/archive'
LOG = ARCHIVE / 'train_34b_pass_20261002/Mars.exe-20261002-17.41.30-6aba6e65.log'


def main():
    print('SOURCE 1.1.1.406343 / build 25579348')
    train = (SRC / 'Lua/Units/Train.lua').read_text(encoding='utf-8').splitlines()
    cube = (SRC / 'Lua/Buildings/MultiResourceCubeVisuals.lua').read_text(encoding='utf-8').splitlines()
    assert 'station:AddResource(amount, res)' in train[779]
    assert 'train:AddResource(-amount, res)' in train[780]
    assert 'unload_cargo(self, station, res, amount)' in train[814]
    assert 'Max((self.stockpiled_amount[resource] or 0) + amount, 0)' in cube[431]
    for name, lines, lo, hi in [('Lua/Units/Train.lua', train, 779, 831),
                                ('Lua/Buildings/MultiResourceCubeVisuals.lua', cube, 422, 435)]:
        for n in range(lo, hi + 1):
            print(f'{name}:{n}: {lines[n-1]}')
    matches = []
    for path in sorted(SRC.rglob('*.lua')):
        for n, line in enumerate(path.read_text(encoding='utf-8-sig').splitlines(), 1):
            if 'CalcResourceSpoilage' in line or 'FoodDecay' in line:
                matches.append((str(path.relative_to(SRC)), n, line.strip()))
    assert any(p == 'Lua\\Spoilage.lua' or p == 'Lua/Spoilage.lua' for p, _, _ in matches)
    for p, n, line in matches:
        print(f'MATCH {p}:{n}: {line}')
    print(f'DIRECT-NAME MATCH TOTAL={len(matches)} MEMBERS={len(matches)}')
    lines = LOG.read_text(encoding='utf-8', errors='replace').splitlines()
    assert 'Build version: 1.1.1.406343' in lines
    drops = [(n, line) for n, line in enumerate(lines, 1)
             if line.startswith('[mod] [SMRTK]') and 'leg=unattributed_change' in line]
    assert len(drops) == 3
    expected = [('before=105', 'after=101', 'resource=Food'),
                ('before=17', 'after=16', 'resource=Sugar'),
                ('before=13', 'after=12', 'resource=Food')]
    for (_, line), fields in zip(drops, expected):
        assert all(field in line for field in fields)
    for n, line in drops:
        print(f'{LOG.name}:{n}: {line}')
    summaries = [(n, line) for n, line in enumerate(lines, 1)
                 if line.startswith('[mod] [SMRTK]') and 'action=slot_8' in line
                 and 'bracketed_writes=293' in line]
    assert len(summaries) == 1
    for n, line in summaries:
        assert 'unattributed_changes=3' in line
        print(f'{LOG.name}:{n}: {line}')
    print(f'DROP TOTAL={len(drops)} MEMBERS={len(expected)} SUMMARY=3')
    witnesses = list(ARCHIVE.rglob('Mars.exe-20261002-15.30.19-6aba6e65.log'))
    print('EARLIER WITNESS ARCHIVE PATHS:', [str(p) for p in witnesses])
    print('SOURCE/LOG RECEIPT PASS; no defect confirmation or native-cause attribution')


if __name__ == '__main__':
    main()
