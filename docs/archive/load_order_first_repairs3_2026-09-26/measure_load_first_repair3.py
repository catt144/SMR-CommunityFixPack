"""Measure the isolated repair worktree. Never arm the real kit or launch a game."""
from pathlib import Path
import hashlib
import importlib.util
import json
import re
import subprocess
import sys

sys.stdout.reconfigure(encoding='utf-8')
tree = Path('B:/Dev/SMR/SMR-LoadFirst-Repair')
out = Path('B:/Dev/SMR/SMR-BugFixPack/scratch/load_first_repair3_results')
out.mkdir(exist_ok=True)

def emit(name, data):
    print(name, json.dumps(data, sort_keys=True))

def run(name, command):
    p = subprocess.run(command, cwd=tree, capture_output=True)
    txt = (p.stdout+p.stderr).decode('utf-8', errors='replace').replace('\r\n','\n')
    (out/(name+'.txt')).write_text(txt,encoding='utf-8',newline='\n')
    emit('RUN', {'name':name,'cwd':str(tree),'command':command,'exit':p.returncode,'tail':txt.splitlines()[-2:]})
    assert p.returncode == 0, name
    return txt

emit('IDENTITY', {'worktree':str(tree),'parent':subprocess.check_output(['git','rev-parse','HEAD'],cwd=tree,text=True).strip(),
    'records':subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()})
for path in ['Code/01_LoadFirst.lua','tools/desk_load_first.py','tools/arming/payloads/98_LoadFirstSync.lua.txt','tools/arming/legs/load-first-sync.json']:
    data = (tree/path).read_bytes()
    emit('INPUT', {'file':path,'sha256':hashlib.sha256(data).hexdigest()})
    if path.startswith('Code/'):
        assert data == subprocess.check_output(['git','show','86a2507:'+path],cwd=tree)
baseline = run('baseline_and_mutants',['python','-X','utf8','tools/desk_load_first.py'])
run('killers',['python','-X','utf8','tools/desk_load_first.py','--list'])
sys.path.insert(0,str(tree/'tools'))
spec=importlib.util.spec_from_file_location('repair',tree/'tools/desk_load_first.py')
b=importlib.util.module_from_spec(spec); spec.loader.exec_module(b)
members=[s for s in baseline.splitlines() if s.startswith(('  PASS ','  FAIL '))]
held=sum(s.startswith('  PASS ') for s in members)
assert 'BASELINE %d of %d demands held' % (held,len(members)) in baseline
rows=[]
for name in [*b.MUTANTS,*b.WITNESS_MUTANTS]:
    text=run('mutant_'+name,['python','-X','utf8','tools/desk_load_first.py','--mutant',name])
    demands=[s for s in text.splitlines() if s.startswith(('  PASS ','  FAIL '))]
    failed=[s for s in demands if s.startswith('  FAIL ')]
    assert len(demands)==len(members) and failed,name
    summary=next(s for s in baseline.splitlines() if re.match(r'^  '+re.escape(name)+r'\s+fails ',s))
    assert re.search(r'fails\s+%d of\s+%d demands' % (len(failed),len(demands)),summary),name
    rows.append({'name':name,'failed':len(failed),'total':len(demands),'summary':summary.strip()})
emit('MUTANT_MEMBERS',rows)
emit('MUTANT_TOTAL',{'members':len(rows),'with_failures':sum(r['failed']>0 for r in rows),'baseline_held':held,'baseline_demands':len(members)})

# Redirect ONLY the fixture kit. The committed relative park is resolved against
# the same branch cwd used by the real command, and its payload bytes checked.
fixture = tree/'scratch/load_first_repair3_arm_fixture'
assert fixture.resolve().is_relative_to((tree/'scratch').resolve())
fixture.mkdir(parents=True,exist_ok=True)
kit = fixture/'kit'
(kit/'Code').mkdir(parents=True,exist_ok=True)
(kit/'metadata.lua').write_text("return PlaceObj('ModDef', {\n 'code', {\n  \"Code/00_TestCore.lua\",\n  \"Code/99_FixtureCarry.lua\",\n },\n})\n",encoding='utf-8',newline='\n')
for name in ['00_TestCore.lua','99_FixtureCarry.lua']:
    (kit/'Code'/name).write_text('-- fixture only\n',encoding='utf-8',newline='\n')
manifest = json.loads((tree/'tools/arming/legs/load-first-sync.json').read_text(encoding='utf-8'))
manifest['kit']=str(kit)
path = fixture/'manifest.json'
path.write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8',newline='\n')
args=['powershell','-NoProfile','-File','tools/arm_leg.ps1','-Manifest',str(path)]
run('arm_fixture',args+['-Mode','arm'])
assert (kit/'Code/98_LoadFirstSync.lua').read_bytes()==(tree/b.WITNESS).read_bytes()
run('verify_fixture',args+['-Mode','verify'])
run('disarm_fixture',args+['-Mode','disarm'])
assert not (kit/'Code/98_LoadFirstSync.lua').exists()
emit('ARM_FIXTURE',{'target':str(kit),'payload_byte_match':True,'disarmed':True,'real_kit_touched':False})
run('parsecheck',['python','-X','utf8','tools/parsecheck.py'])
run('doccheck_branch',['python','-X','utf8','tools/doccheck.py'])
