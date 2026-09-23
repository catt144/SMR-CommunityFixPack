#!/usr/bin/env python3
"""Reconcile the 1.1.1 build response by name, including companion probe removal.

    python tools/gamepatch_111_census.py
    python tools/gamepatch_111_census.py --live-source

Checks the actual code/metadata/items sets, source Register declarations,
and TestKit Register declarations. The fixed
baseline is git 16ff1aa. Prints members beside totals and a second set equation;
the expected retirement set is the owner-invoked build brief, not a glob count.
The optional live-source check reads the installed pack's build and compares the
live and archived source manifests. No game launch or save access.
"""
import argparse
import collections
import hashlib
import os
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
BASE = '16ff1aa'
KIT = Path(os.environ.get('SMR_TESTKIT', str(ROOT.parent / 'SMR-BugFixPack-TestKit')))
RETIRED = set('BrokenTrackSalvage FounderTraitNotification BuildingCodesPrefab '
              'DestroyedTunnels DomeOverviewHighlight GeneForging GraphConsumedCaption '
              'MirrorSphereSite NightShiftWork OpenPastureStockpiles SinkholeIndestructible '
              'TradeRocketFuelRefresh TrainCargoDumping TrainsToVoid TrainWaitTime WispRewards'.split())


def at_base(path):
    return subprocess.check_output(['git', '-C', str(ROOT), 'show', BASE + ':' + path]).decode('utf-8')


def names(label, members):
    ordered = sorted(members)
    print(label + ' (' + str(len(ordered)) + '): ' + ', '.join(ordered))


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--live-source', action='store_true')
    args = ap.parse_args()
    failures = []

    def check(label, condition, difference=''):
        print(('PASS ' if condition else 'FAIL ') + label + (' ' + difference if difference else ''))
        if not condition:
            failures.append(label)

    print('command: python tools/gamepatch_111_census.py' + (' --live-source' if args.live_source else ''))
    print('HEAD: ' + subprocess.check_output(['git', '-C', str(ROOT), 'rev-parse', 'HEAD']).decode().strip())
    metadata = (ROOT / 'metadata.lua').read_text(encoding='utf-8')
    items = (ROOT / 'items.lua').read_text(encoding='utf-8')
    loaded = re.findall(r'^\s*"(Code/[^"\n]+\.lua)",?\s*$', metadata, re.M)
    editor = re.findall(r"'CodeFileName',\s*\"([^\"]+)\"", items)
    files = sorted(str(p.relative_to(ROOT)).replace('\\', '/') for p in (ROOT / 'Code').glob('*.lua'))
    baseline = set(re.findall(r'^\s*"(Code/[^"\n]+\.lua)",?\s*$', at_base('metadata.lua'), re.M))
    retired_paths = {'Code/Fix_' + n + '.lua' for n in RETIRED}
    names('retired modules', RETIRED)
    names('loaded files', loaded)
    names('disk files', files)
    names('editor files', editor)
    check('disk = metadata = editor by name', set(files) == set(loaded) == set(editor),
          'differences=' + repr(sorted(set(files) ^ set(loaded) | set(editor) ^ set(loaded))))
    check('load order matches editor', loaded == editor)
    check('no duplicate file loads', len(loaded) == len(set(loaded)) == len(editor))
    check('baseline minus final is exactly authorized retirements', baseline - set(loaded) == retired_paths
          and not set(loaded) - baseline,
          'missing=' + repr(sorted(retired_paths - (baseline - set(loaded))))
          + ' unexpected=' + repr(sorted((baseline - set(loaded)) - retired_paths)))
    print('file reconciliation: baseline ' + str(len(baseline)) + ' = surviving ' + str(len(loaded))
          + ' + retired ' + str(len(retired_paths)))

    # Literal IDs and local FIX_ID aliases are the pack's
    # actual Register shapes; unsupported shapes fail instead of disappearing.
    registrations = []
    for path in loaded:
        raw = (ROOT / path).read_text(encoding='utf-8')
        fixed = re.search(r'local\s+FIX_ID\s*=\s*"([^"]+)"', raw)
        calls = re.findall(r'SMRFixPack\.Register\(\s*("[^"]+"|FIX_ID)\s*,', raw)
        for call in calls:
            registrations.append(call.strip('"') if call != 'FIX_ID' else fixed[1] if fixed else '?')
    names('registered fixes', registrations)
    expected = {Path(p).stem.removeprefix('Fix_') for p in loaded} - {'00_Core', '90_SaveSanitizer'} | {'SaveSanitizer'}
    check('registration census matches source files with positive controls',
          set(registrations) == expected and len(registrations) == len(set(registrations)) and bool(registrations),
          'differences=' + repr(sorted(set(registrations) ^ expected)))
    check('retired registrations absent', not RETIRED.intersection(registrations),
          'hits=' + repr(sorted(RETIRED.intersection(registrations))))
    print('registration reconciliation: files ' + str(len(loaded)) + ' = registered fixes '
          + str(len(registrations)) + ' + core 1')

    probes = []
    retired_probe_hits = []
    for p in sorted((KIT / 'Code').glob('*.lua')):
        raw = p.read_text(encoding='utf-8')
        for m in re.finditer(r'^SMRTest\.Register\("([^"\n]+)",\s*\{[\s\S]*?^\}\)', raw, re.M):
            probes.append(m[1])
            ids = set(re.findall(r'fix\s*=\s*"([^"]+)"', m[0]))
            if RETIRED.intersection(ids) or m[1] in RETIRED:
                retired_probe_hits.append(p.name + ':' + m[1])
        for line in raw.splitlines():
            if any('"Fix_' + n + '"' in line for n in RETIRED):
                retired_probe_hits.append(p.name + ':' + line.strip())
    names('TestKit probes', probes)
    check('retired probe registrations and capture rows absent; surviving positive controls present',
          not retired_probe_hits and {'CloggedBuildingRelease', 'VacuumWalks', 'TrackShellLeak'}.issubset(probes),
          'hits=' + repr(retired_probe_hits))
    check('probe IDs unique', len(probes) == len(set(probes)))
    probe_calls = sum(len(re.findall(r'^SMRTest\.Register\(', p.read_text(encoding='utf-8'), re.M))
                      for p in (KIT / 'Code').glob('*.lua'))
    print('probe reconciliation: parsed members ' + str(len(probes)) + ' = Register call lines ' + str(probe_calls))
    check('every probe declaration parsed', probe_calls == len(probes))

    # Only the load-list changes in metadata are authorized. Ignore rules and
    # public/release strings deliberately retain the preceding release state.
    old_metadata = at_base('metadata.lua')
    normalized = old_metadata
    for path in retired_paths:
        normalized = re.sub(r'^\s*"' + re.escape(path) + r'",?\s*\n', '', normalized, flags=re.M)
    check('metadata differs only by retired load entries', metadata == normalized)

    if args.live_source:
        import patchcheck as pc
        version = pc.live_version()
        print('live game=' + str(version) + '; Steam build=' + str(pc.installed_build()))
        check('live game still target build', version == '1.1.1.405907')
        archive = Path(pc.ARCHIVE) / '1.1.1.405907'
        pinned = (archive / 'MANIFEST.sha256').read_text(encoding='utf-8')
        live = pc.manifest_body(str(Path(pc.INSTALL) / 'ModTools/Src'))
        archived = pc.manifest_body(str(archive / 'Src'))
        check('live and archive source match manifest', pinned == live == archived)
        print('manifest sha256=' + hashlib.sha256(pinned.encode('utf-8')).hexdigest())

    names('failed checks', failures)
    return bool(failures)


if __name__ == '__main__':
    sys.exit(main())
