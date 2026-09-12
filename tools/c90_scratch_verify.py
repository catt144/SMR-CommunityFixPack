#!/usr/bin/env python3
"""External scratch-source falsifiers for DESKBENCH_C90; never edits Code/.

No harness control switch is used. Write altered Lua to a temporary Code tree,
redirect only the source read, run the unmodified harness, and require a named
FAIL plus exit 1. The union must cover every demand in the new C90 control.
"""
import contextlib
import io
import tempfile
from pathlib import Path
from unittest.mock import patch
import deskbench as db
import desk_c90_datapatch as c90
import desk_c89_faction_gate as c89
import desk_migration_cluster as migration


def demand_labels(output, prefix):
    return {line.split('  -- ', 1)[0].removeprefix(prefix)
            for line in output.splitlines() if line.startswith(prefix)}


def run(main):
    output = io.StringIO()
    with contextlib.redirect_stdout(output):
        code = main()
    return code, output.getvalue()


def main():
    code, baseline = run(c90.main)
    assert code == 0, baseline
    demands = demand_labels(baseline, '  PASS  ')
    covered = set()
    variants = [
        ('runner suppressed', 'Code/00_Core.lua',
         '\t\tlocal ok, err = pcall(opts.pass, ctx)',
         '\t\tlocal ok, err = true, nil -- scratch: callback removed',
         'Sinkhole intact: exact ordered writes and status'),
        ('veto removed', 'Code/00_Core.lua',
         '\t\tif type(disabled) == "table" and disabled[id] then return end',
         '\t\t-- scratch: veto removed', 'Sinkhole veto stops the pass'),
        ('heal removed', 'Code/00_Core.lua',
         '\tfunction ctx.heal()\n',
         '\tfunction ctx.heal()\n\t\tif true then return end -- scratch\n',
         'Sinkhole failed self-check is erased from UpdateSuspects'),
        ('Saint label-existence guard removed', 'Code/Fix_SaintBlessing.lua',
         '\t\tif type(get_label) ~= "function" then\n\t\t\tctx.patched = true',
         '\t\tif false then -- scratch: missing-label guard removed\n\t\t\tctx.patched = true',
         '1.1.0 Saint GetTraitLabel: exact writes and status'),
        ('Saint behaviour refusal removed', 'Code/Fix_SaintBlessing.lua',
         '\t\t\treturn capture_filed_label(preset, raw) == expected',
         '\t\t\treturn true -- scratch: missing-method refusal removed',
         '1.1.0 Saint TraitPreset.AddDomeColonistsModifier: exact writes and status'),
        ('Sinkhole class guard removed', 'Code/Fix_SinkholeIndestructible.lua',
         '\t\tif type(C) ~= "table" then',
         '\t\tif false then -- scratch: missing-class guard removed',
         'Sinkhole class: exact ordered writes and status'),
        ('C89 apply-success guard removed', 'Code/Fix_FactionDomeSizeGate.lua',
         '\t\tif not self_check_passed then return end',
         '\t\t-- scratch: apply-success guard removed',
         '(k2) NEGATIVE -- a module whose self-check DECLINED patches nothing, even '
         'though DataPatch\'s runner still fires its pass'),
    ]
    original_read = db.read
    with tempfile.TemporaryDirectory(prefix='c90-falsifiers-') as tmp:
        root = Path(tmp)
        for name, rel, old, new, required in variants:
            original = Path(db.REPO) / rel
            source = original_read(original)
            # The same veto line belongs to both WhenActive and DataPatch.
            expected_count = 2 if name == 'veto removed' else 1
            assert source.count(old) == expected_count, (name, source.count(old))
            scratch = root / rel
            scratch.parent.mkdir(parents=True, exist_ok=True)
            scratch.write_text(source.replace(old, new), encoding='utf-8')

            def read(path):
                return original_read(scratch if Path(path).resolve() == original.resolve() else path)

            harness = c89 if name.startswith('C89') else c90
            with patch.object(db, 'read', read):
                code, output = run(harness.main)
            failed = demand_labels(output, '  FAIL  ')
            assert code == 1 and required in failed, (name, code, output)
            if harness is c90:
                covered.update(failed)
            print('EXPECTED FAIL: %s (exit %d)' % (name, code))
            for label in sorted(failed):
                print('  ' + label)

        # F60 harm assertions must fail if its harmful argument is removed.
        source, chunk = migration.module_text('DomeFreeSpaceMismatch', migration.F60_HARMFUL_REV)
        old = 'GatherFreeLivingSpaces(self.labels.Residence, "player_enabled")'
        assert source.count(old) == 1
        scratch = root / 'Code/Fix_DomeFreeSpaceMismatch.lua'
        scratch.write_text(source.replace(old, 'GatherFreeLivingSpaces(self.labels.Residence)'),
                           encoding='utf-8')
        original_module_text = migration.module_text

        def module_text(name, rev=None):
            if name == 'DomeFreeSpaceMismatch':
                return original_read(scratch), chunk
            return original_module_text(name, rev)

        with patch.object(migration, 'module_text', module_text):
            code, output = run(migration.main)
        failed = demand_labels(output, '  FAIL  ')
        expected = {
            'F60 patched tally counts 3 but migration gate still rejects',
            'F60 patch reports all 3 applicants housed while arrival space gate rejects home',
        }
        assert code == 1 and failed == expected, output
        print('EXPECTED FAIL: F60 harmful argument removed (exit %d)' % code)
        for label in sorted(failed):
            print('  ' + label)
    assert demands <= covered, 'unfalsified C90 demands: %s' % (demands - covered)
    print('All 8 scratch variants failed as required; %d/%d C90 demands falsified.'
          % (len(demands & covered), len(demands)))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
