"""Run from repo root after load_first_audit3.py. No retail/remote mutations.

Use archived real fetch/root/child bodies to challenge the witness at 86a2507.
Async APIs are deterministic desk stubs, not live Paradox calls.
"""
import hashlib
import importlib.util
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')
root = Path.cwd()
tree = root / 'scratch/load_first_audit3_86a2507'
sys.path.insert(0, str(tree / 'tools'))
spec = importlib.util.spec_from_file_location('branch', tree / 'tools/desk_load_first.py')
b = importlib.util.module_from_spec(spec)
spec.loader.exec_module(b)
module = (tree / b.MODULE).read_text(encoding='utf-8')
witness = (tree / b.WITNESS).read_text(encoding='utf-8')
assert hashlib.sha256(witness.encode()).hexdigest() == 'ace64b3e790a2412a813093f3760a37cfe23ba09cb01c48b4cff87c89b1c3444'
src = b.SRC / 'CommonLua/UI/ModManager.lua'
assert hashlib.sha256(src.read_bytes()).hexdigest() == '1b3cb3846d58a2263eca9d56c3d7361db821b906ad2453f7fed0b09c41198f45'
results = []
print('COMMAND python scratch/load_first_audit3_counterexamples.py')
print('IDENTITY branch=86a25078adb705d6e64b8bdd25bb4c115ada214d source=1.1.1.405907')

def emit(name, holds, **observed):
    row = {'name': name, 'holds': bool(holds), 'observed': observed}
    results.append(row)
    print('DEMAND', json.dumps(row, sort_keys=True))

def fresh():
    c = b.Case(module, [b.PACK, 'B'], [b.PACK, 'B'])
    c.run_threads()
    c.load_witness(witness)
    return c

functions = []
for pattern in [r'^function AsyncPdxGetAllSubscribedMods\(', r'^function SyncUpdatePdxMod\(', r'^local function SyncPdxMods\(']:
    body, first, last = b.shipped_body(b.ui_lines, pattern)
    functions.append(body)
    print('SOURCE_BODY', json.dumps({'file': str(src), 'first': first, 'last': last, 'sha256': hashlib.sha256(body.encode()).hexdigest()}))
setup = r'''
Pdx = {DefaultPlaysetId = 0}
REMOTE_LOG = {}
function mods_print(...)
  local t = {} for i = 1, select('#', ...) do t[i] = tostring(select(i, ...)) end
  REMOTE_LOG[#REMOTE_LOG + 1] = table.concat(t, ' ')
end
table.iappend = function(t,s) for _,v in ipairs(s) do t[#t+1]=v end end
table.ifilter = function(t,k,v) local out={} for _,x in ipairs(t) do if x[k]==v then out[#out+1]=x end end return out end
table.find_value = function(t,k,v) for _,x in ipairs(t) do if x[k]==v then return x end end end
PAGES = {}; FETCH_ERROR = false; INSTALL_ERROR = false; UNINSTALL_ERROR = false
SUBSCRIBED = {ModID = 123, VersionToInstall = 1, RepositoryPath = 'desk-only'}
INSTALLED = {}
function PdxGetInstalledMods() return INSTALLED end
function AsyncPdxGetSubscribedMods(p)
  PAGES[#PAGES + 1] = p.Page
  if p.Page == 1 then return false, {SUBSCRIBED} end
  return FETCH_ERROR, {}
end
function AsyncPdxInstallMod() return INSTALL_ERROR, {} end
function AsyncPdxUninstallMod() return UNINSTALL_ERROR end
ModUI_Entry = { FromPdxSubscribedMod = function() return {} end }
function QueueRealRoot() g_PopsDownloadModsQueue:PushTask(false, AuditRoot) end
'''

def real_case():
    c = fresh()
    c.ex(setup)
    c.ex('\n'.join(functions) + '\nAuditRoot = SyncPdxMods')
    return c

def up_to_date(c):
    c.ex("Mods['remote'] = {PdxMod={ModID=123}}; INSTALLED={{ModID=123,Version='1'}}")

# The first page succeeds. The next page fails empty; the REAL fetch checks
# page length before error and silently returns the partial first page.
c = real_case(); up_to_date(c)
c.ex("FETCH_ERROR='Timeout'; QueueRealRoot()")
state = c.drive()
emit('R5D partial enumeration cannot PASS', not c.passes(), state=state, verdict=c.verdict(), passes=c.passes(),
     pages=c.ev("table.concat(PAGES, ',')"), api_error=c.ev('FETCH_ERROR'), children=c.ev('#mod_env.LoadFirstSync.W.current.children'),
     remote_log=c.ev("table.concat(REMOTE_LOG, ' | ')"))
c = real_case(); up_to_date(c)
c.ex('QueueRealRoot()'); c.drive()
emit('control successful enumeration and up-to-date child PASS', c.passes(), verdict=c.verdict(), pages=c.ev("table.concat(PAGES, ',')"))

# The REAL child logs an install failure and returns nil; the wrapper sees no error.
c = real_case()
c.ex("INSTALL_ERROR='Timeout'; QueueRealRoot()")
state = c.drive()
emit('R5D shipped install failure cannot PASS', not c.passes(), state=state, verdict=c.verdict(), passes=c.passes(),
     remote_log=c.ev("table.concat(REMOTE_LOG, ' | ')"), queue_errors=c.ev('#SPRO_ERRORS'))

# A known installed but unsubscribed mod: real uninstall fails, then returns nil.
c = real_case()
c.ex("function AsyncPdxGetSubscribedMods(p) return false, {} end; INSTALLED={{ModID=123, Version='1'}}; UNINSTALL_ERROR='Timeout'; QueueRealRoot()")
state = c.drive()
emit('R5D shipped uninstall failure cannot PASS', not c.passes(), state=state, verdict=c.verdict(), passes=c.passes(),
     remote_log=c.ev("table.concat(REMOTE_LOG, ' | ')"), queue_errors=c.ev('#SPRO_ERRORS'))

# The original in-flight counterexample is fixed before logout. With only that
# child in flight, Clear drops no queued records, so the finished attempt passes.
c = fresh()
c.ex("SIM.children=1; SIM.behaviour[1]='async'")
c.login(); c.drive()
emit('control zero-queue in-flight child does not PASS', c.verdict() == 'IN-FLIGHT' and not c.passes(), queued=c.queued(), verdict=c.verdict())
c.logout(); state = c.drive()
emit('R5D logout during sole in-flight child cannot PASS', not c.passes(), state=state, verdict=c.verdict(), passes=c.passes(),
     queued=c.queued(), clear_line=c.log_has('CLEAR clears=1 cancelled_unstarted=0'))

# Actual set payload loaded AFTER the already-first pack, as section 14 E says.
# Its writer here belongs to the fixture pack, not a retail kit slot; the check
# concerns ordering, no final option click, and the deferred set/quit driver.
captured = ['SMR_CommunityFixPackTestKit', 'SMR_TrainHubDev_20260918', b.PACK,
            'SMR_CommunityOptInPack', 'SMR_RailShaftDev_20260923']
post = [b.PACK] + [x for x in captured if x != b.PACK]
c = b.Case(module, post, post)
c.run_threads()
c.ex('AUDIT_QUITS=0; function quit() AUDIT_QUITS=AUDIT_QUITS+1 end')
c.load_pack_file('tools/arming/payloads/98_LoadFirstSet.lua.txt')
c.run_threads()
emit('R5E control actual late-veto set payload restores after final option click',
     c.raw() == ','.join(captured) and c.saves() == 1 and c.questions() == 0 and c.ev('AUDIT_QUITS') == 1,
     saved=c.raw(), saves=c.saves(), questions=c.questions(), quits=c.ev('AUDIT_QUITS'),
     option=c.ev("Mods[%r].options.LoadFirst" % b.PACK))
print('DEMAND_TOTAL', json.dumps({'members': len(results), 'held': sum(r['holds'] for r in results),
    'failed_names': [r['name'] for r in results if not r['holds']]}, sort_keys=True))
assert [r['holds'] for r in results] == [False, True, False, False, True, False, True]
print('ESTIMATE_ARITHMETIC', json.dumps({'legs': {'A':3,'B':4,'C':3,'D':3,'E':0}, 'sum':sum([3,4,3,3,0]), 'optional_PN':4,'with_PN':sum([3,4,3,3,0,4]), 'timed':False}))
