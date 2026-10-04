"""Desk fixture for the adjacent upload_capture.lua. No game or uploads.

Extracts archived UploadMod and PDX_Upload; stubs packaging and native SDK APIs.
Controls record which native names were reached, not actual network behavior.
"""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[4] / 'tools'))
import deskbench as db
from luafn import find_bodies

ROOT = Path(__file__).resolve().parents[4]
SRC = Path('B:/Dev/SMR/SMR-Shared/SMR-SrcArchive/1.1.1.406343/Src')
capture_multiline = (Path(__file__).with_name('upload_capture.lua')).read_text(encoding='utf-8')
capture_lines = [line.strip() for line in capture_multiline.splitlines() if line.strip() and not line.lstrip().startswith('--')]
assert all('--' not in line for line in capture_lines), 'Inline comments cannot safely join'
capture_oneline = ' '.join(capture_lines)
(Path(__file__).with_name('upload_capture.oneline.lua')).write_bytes((capture_oneline + '\n').encode('utf-8'))
CAPTURE = capture_oneline
PREPARE_INPUT = 'dlgConsole.idEdit.MaxLen=8192; ModLog("[PDXCAP] INPUT_LIMIT=%d",dlgConsole.idEdit.MaxLen)'
RESTORE_INPUT = 'dlgConsole.idEdit.MaxLen=2048'

def extract(rel, name):
    lines = (SRC / rel).read_text(encoding='utf-8').splitlines()
    hits = find_bodies(lines, '^function ' + name + r'\(')
    assert len(hits) == 1, (rel, name, hits)
    lo, hi = hits[0]
    return '\n'.join(lines[lo:hi + 1])

UPLOAD = extract('CommonLua/Classes/GedModEditor.lua', 'UploadMod')
PDX = extract('CommonLua/Libs/Paradox/ParadoxMods.lua', 'PDX_Upload')
PREPARE = extract('CommonLua/Libs/Paradox/ParadoxMods.lua', 'PDX_PrepareForUpload')

SETUP = '''
logs, native_calls = {}, {}
function ModLog(fmt, ...) logs[#logs+1] = string.format(fmt, ...) end
dlgConsole={idEdit={MaxLen=2048}}
function ModMessage(...) end
function T(id, s) return s end
function Untranslated(v) return type(v)=='string' and v or v[1] end
function CreateRealTimeThread(fn, ...) return fn(...) end
function PauseInfiniteLoopDetection() end
function ResumeInfiniteLoopDetection() end
function GedSetUiStatus() end
function insideHG() return false end
function ConvertToOSPath(p) return p end
function AsyncDeletePath() end
function AsyncCopyFile() end
io.getsize = function() return 1 end
ModsPackFileName = 'ModContent.fpk'
Mods, empty_table = {}, {}
g_Pdx = {account = true}
local function stub(name)
  return function(...)
    native_calls[#native_calls+1] = name
    if fault == name then return 'UnknownError', nil, false, nil end
    return nil, {Name = '', ModName='staging', ModFolderPath='staging', FileName='asset', ModId=9, Version='1'}, nil
  end
end
names = {'AsyncPdxGetModDetails','AsyncPdxSetupModForPublish','AsyncPdxUploadModAsset','AsyncPdxUploadModContent','AsyncPdxPublishMod','AsyncPublishNewModVersion'}
function set_natives()
  fresh = {}
  for _, name in ipairs(names) do
    local fn = stub(name)
    _G[name], fresh[name] = fn, fn
  end
end
set_natives()
function CreatePackageForUpload(mod, params)
  -- Simulates the observable global-redefinition effect of packaging ReloadLua.
  set_natives()
  if replacement then UploadMod = replacement end
  return true, nil
end
socket = {ShowMessage = function() end}
mod = {id='SMR_CommunityOptInPack', title='title', short_description='summary', description='long', image='thumb', lua_revision=1, version=179, last_changes='changes', dependencies={}, external_links={}}
function mod:GetPropertyMetadata(id) return {name=id} end
function mod:GetModLabel() return 'target' end
function mod:GetScreenshots() return {'shot'} end
function mod:GetTags() return {} end
function mod:SaveWholeMod() end
'''

def case(label, setup='', fault=None, expected=None):
    rt = db.lua_runtime()
    rt.execute(SETUP)
    rt.execute(PREPARE)
    rt.execute(PDX)
    rt.execute(UPLOAD)
    rt.execute('replacement = UploadMod')
    rt.execute(setup)
    rt.globals().fault = fault
    rt.execute(PREPARE_INPUT)
    assert rt.eval('dlgConsole.idEdit.MaxLen') == 8192
    assert len(CAPTURE) <= rt.eval('dlgConsole.idEdit.MaxLen')
    rt.execute(CAPTURE)
    rt.execute(RESTORE_INPUT)
    assert rt.eval('dlgConsole.idEdit.MaxLen') == 2048
    rt.execute('UploadMod(socket, mod, {os_pack_path="pack"}, PDX_PrepareForUpload, PDX_Upload)')
    calls = [v for _, v in rt.globals().native_calls.items()]
    logs = [v for _, v in rt.globals().logs.items()]
    assert expected == calls, (label, expected, calls)
    assert any('READY after-pack' in s for s in logs), (label, logs)
    assert any('restored=true' in s for s in logs), (label, logs)
    assert rt.eval('UploadMod == replacement'), label
    assert rt.eval('(function() for _,name in ipairs(names) do if _G[name]~=fresh[name] then return false end end return true end)()'), label
    print(label + ': ' + ' -> '.join(calls))
    for s in logs:
        if 'CONTROL' in s or 'END '+str(fault) in s or 'END upload' in s:
            print('  ' + s)
    return rt

create = ['AsyncPdxGetModDetails','AsyncPdxSetupModForPublish','AsyncPdxUploadModAsset','AsyncPdxUploadModAsset','AsyncPdxUploadModContent','AsyncPdxPublishMod']
update = create[:-1] + ['AsyncPublishNewModVersion']
print('DESK ONLY: ' + db.lua_version() + '; source=1.1.1.406343')
print('console input fixture: prepare/readback=8192; capture bytes=' + str(len(CAPTURE.encode('utf-8'))) + '; chars=' + str(len(CAPTURE)) + '; ASCII=' + str(CAPTURE.isascii()) + '; restore=2048')
case('create success', expected=create)
case('update success', 'mod.pdx_id = 9', expected=update)
case('create publish refusal', fault='AsyncPdxPublishMod', expected=create)
case('content refusal', fault='AsyncPdxUploadModContent', expected=create[:-1])
case('ignored details refusal', fault='AsyncPdxGetModDetails', expected=create)

# Sandbox negative control: same installer has no Paradox globals available.
rt = db.lua_runtime()
rt.execute(SETUP)
rt.execute(UPLOAD)
rt.execute('original = UploadMod; PDX_PrepareForUpload=nil; PDX_Upload=nil')
rt.execute(CAPTURE)
assert rt.eval('UploadMod == original')
assert any('NOT_READY' in v for _, v in rt.globals().logs.items())
print('restricted/no-PDX globals: NOT_READY; UploadMod untouched')

# Yield/arity control: a native-style function yields inside protected upload.
rt = db.lua_runtime()
rt.execute(SETUP)
rt.execute('''
function UploadMod(s,m,p,prep,up) return up(s,m,p) end
function PDX_PrepareForUpload() return true end
function PDX_Upload() return AsyncPdxPublishMod() end
function AsyncPdxPublishMod() coroutine.yield('waiting'); return nil,false,nil end
''')
rt.execute(CAPTURE)
rt.execute('''
co=coroutine.create(function() return UploadMod(socket,mod,{},PDX_PrepareForUpload,PDX_Upload) end)
ok, marker = coroutine.resume(co)
assert(ok and marker=='waiting')
result=table.pack(coroutine.resume(co))
assert(result.n==4 and result[1]==true and result[2]==nil and result[3]==false and result[4]==nil)
''')
print('yield + trailing-nil return: resumed; arity preserved (nil,false,nil)')

# Thrown errors propagate and hooks restore; this does not emulate engine errors.
rt = db.lua_runtime()
rt.execute(SETUP)
rt.execute('''
function UploadMod(s,m,p,prep,up) return up(s,m,p) end
function PDX_PrepareForUpload() return true end
function PDX_Upload() return AsyncPdxPublishMod() end
throw_native = function() error('fixture-only', 0) end
AsyncPdxPublishMod = throw_native
''')
rt.execute(CAPTURE)
rt.execute('''
ok, err = pcall(UploadMod, socket, mod, {}, PDX_PrepareForUpload, PDX_Upload)
assert(not ok and err=='fixture-only')
assert(AsyncPdxPublishMod==throw_native)
''')
print('thrown fixture error: propagates unchanged; native function restored')

# Run the actual Untranslated, concat and ModLog bodies with small explicit shims.
rt = db.lua_runtime()
rt.execute('''
ModMessageLog={}
function ObjModifiedDelayed() end
function ModPrint(s) printed=s end
TMeta, TConcatMeta = {}, {}
function T(v) return setmetatable(v, TMeta) end
function IsT(v) return type(v)=='table' and (getmetatable(v)==TMeta or getmetatable(v)==TConcatMeta) end
function IsTCompatible(v) return IsT(v) end
function IsLookupTag() return false end
table.copy = function(t) local r={} for i,v in ipairs(t) do r[i]=v end return r end
''')
rt.execute(extract('CommonLua/Core/localization.lua', 'Untranslated'))
loclines = (SRC / 'CommonLua/Core/localization.lua').read_text(encoding='utf-8').splitlines()
assert loclines[376].startswith('TMeta.__concat = function')
assert loclines[416]=='end'
rt.execute('\n'.join(loclines[376:417]))
rt.execute('TConcatMeta.__concat = TMeta.__concat')
rt.execute(extract('CommonLua/Modding/Mod.lua', 'ModMessage'))
rt.execute(extract('CommonLua/Modding/Mod.lua', 'ModLog'))
rt.execute('''
message=Untranslated('Upload failed:') .. Untranslated('UnknownError')
ModLog('Error: %s',message)
assert(type(message)=='table')
assert(string.find(printed,'table: ',1,true))
assert(not string.find(printed,'UnknownError',1,true))
''')
print('shipped localization + ModLog: localized concatenation logs table identity; SDK error text lost')
