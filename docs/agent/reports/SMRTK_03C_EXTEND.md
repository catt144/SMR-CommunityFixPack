# SMRTK 03C — Selected extension

2026-09-14, Codex. Source-derived only; no game launch. Starting pack HEAD
`48f75a0`, TestKit `87f3130`. The first baseline was RED while a peer's C95
draft awaited filing; resumed after the owner requested a recheck and baseline
doccheck was GREEN. No checklist writes or pack runtime changes.

## Numbered claims and coverage

1. `73_SMRTK_Infopanel.lua` keeps the curated table and its existing dispatch
   guards, depot before/after reads, and Delete caveat. Controls now have group
   labels: Curated, More: Cheat, More: AsyncCheat, Inspection & pins.
2. More follows vanilla's instance → metatable → `__index` table walk, including
   its suffix/category resolution. It excludes every curated name, validates
   callable members, and sorts within categories. It uses one generic registry
   action, `selected_more`, with an object/method/category/valid-after record.
   Its callback re-enumerates before calling `obj[method](obj)` and refuses stale,
   unsupported, and curated methods. Curated Fill/Empty cannot bypass their
   busy-depot guard through More.
3. Installed Steam build **24995074** reproduces **106 distinct member names:
   94 Cheat + 12 AsyncCheat**, delta zero from 03B. There are 150 explicit colon
   method definitions containing 88 distinct Cheat names and 12 AsyncCheat names;
   `Building.lua:158,1949-1953` generates six additional upgrade names. All 150
   bodies and the generated upgrade body were opened in this session; none calls
   a sync/taint writer or a forbidden preset wrapper. The instrument below counts
   every live Lua file and audits these bodies rather than a truncated grep.
4. Source-name coverage is **106/106**, comprising **22 curated names + 84 More
   names (72 Cheat + 12 AsyncCheat)**. Named taint skips: **none on this build**.
   This is coverage across source-derived object-method fixtures, not a live
   colony census. The deliberately exaggerated fixture exposing all methods at
   once renders 105 method buttons: the existing Add Dust row picks `CheatAddDust`
   ahead of its `CheatAddDustRC` alternative. **Conditional omission:
   CheatAddDustRC when CheatAddDust is also present**, preserving the curated
   alias contract. An RC-only fixture exposes that member through Add Dust.
5. Ordinary clicks retain P2's game-time thread; AsyncCheat clicks use a real-time
   thread, matching vanilla's local UI-dispatch category without a sync wrapper.
   Both enter `T.Run` inside that thread, recheck selection, write one primary
   result, and run the core taint assertion after the leaf returns. This records
   leaf return, not completion of work a vanilla leaf schedules for later.
6. Colonist's exact `CheatKill` body is dispatched through More and reaches
   `SetCommand("Die")`; Drone's exact `CheatDespawn` reaches deselection and
   `DespawnNow`. The tests use the live source bodies with fake game services.
   Nothing here establishes rendering, retail debug-tool availability, in-play
   taint safety, save safety, or achievement eligibility. Eligibility remains
   `UNAVAILABLE:sandbox`; AsyncCheatProperties can open a GED editor, which is
   itself an achievement blocker while open (EF-095).

## Verification

Run the fenced instrument from the pack root:

`python -c "from pathlib import Path; import re; s=Path('docs/agent/reports/SMRTK_03C_EXTEND.md').read_text(encoding='utf-8'); exec(re.search(r'^'+chr(96)*3+r'python\n(.*?)^'+chr(96)*3,s,re.M|re.S)[1])"`

```python
from pathlib import Path
import hashlib, re, runpy, subprocess
root = Path.cwd()
kit = root.parent / 'SMR-BugFixPack-TestKit'
src = Path('A:/SteamLibrary/steamapps/common/Project Spark/ModTools/Src')
acf = Path('A:/SteamLibrary/steamapps/appmanifest_3215050.acf').read_text()
build = re.search(r'"buildid"\s+"(\d+)"', acf)[1]
assert build == '24995074', ('live build moved', build)
methods, bodies, classes = set(), {}, {}
files = list(src.rglob('*.lua'))
for p in files:
    text = p.read_text(encoding='utf-8-sig')
    for match in re.finditer(r'^function\s+([\w.]+):((?:AsyncCheat|Cheat)\w*)\s*\(', text, re.M):
        end = re.search(r'^end\b', text[match.end():], re.M)
        assert end is not None, (p, match[2])
        body = text[match.start():match.end()+end.end()]
        assert not re.search(r'NetSyncEvent|LogCheatUsed|\bdef\s*:\s*(?:run|Exec)\s*\(', body), (p, match[2])
        methods.add(match[2])
        bodies[match[1], match[2]] = body
        classes.setdefault(match[1], set()).add(match[2])
building = (src / 'Lua/Buildings/Building.lua').read_text(encoding='utf-8-sig')
upgrades = int(re.search(r'DefineConstInt\("Building", "MaxUpgrades", (\d+)', building)[1])
assert upgrades == 6
assert re.search(r'Building\["CheatUpgrade" \.\. i\] = function\(self\)\s+self:ApplyUpgrade\(i, true\)\s+end', building)
methods.update('CheatUpgrade'+str(i) for i in range(1, upgrades+1))
assert len(bodies) == 150 and len(methods) == 106
assert sum(n.startswith('Cheat') for n in methods) == 94
assert sum(n.startswith('AsyncCheat') for n in methods) == 12
toolkit = sorted((kit / 'Code').glob('7*_SMRTK*.lua')) + [kit / 'Code/80_AgentSlots.lua']
assert len(toolkit) == 9
lines = [line for p in toolkit for line in p.read_text(encoding='utf-8-sig').splitlines()]
assert sum(bool(re.search(r'NetSyncEvent|LogCheatUsed', line)) for line in lines) == 0
assert sum(bool(re.search(r'^\s*print\(', line)) for line in lines) == 0
presence = (src / 'Data/CheatDef.lua').read_text(encoding='utf-8-sig').splitlines()
assert sum(bool(re.search(r'NetSyncEvent|LogCheatUsed', line)) for line in presence) == 26
assert sum(bool(re.search(r'\bNetSyncEvent\s*\(', line)) for line in presence if not re.search(r'Comment\s*=', line)) == 13
print('03C LIVE:', build, len(files), 'Lua files;', len(bodies), 'explicit bodies; 94 + 12 = 106 names')
print('03C GATES: 9 toolkit files; rule 6 = 0; rule 7 = 0; presence = 26 lines / 13 calls')
scope = runpy.run_path(str(root / 'docs/agent/reports/SMRTK_P2_SMOKE.py'))
lua = scope['lua']
lua.globals().live_names = lua.table_from(sorted(methods))
lua.globals().colonist_names = lua.table_from(sorted(classes['Colonist'] | classes['CObject']))
lua.execute('Colonist = {}; Drone = {}')
lua.execute(bodies['Colonist', 'CheatKill'])
lua.execute(bodies['Drone', 'CheatDespawn'])
lua.execute(r'''
taint=false
function AreCheatsUsed() return taint end
local T=SMRTK
local function object(names)
  local base={}
  for _,name in ipairs(names) do base[name]=function(self) self.called=name end end
  local derived=setmetatable({}, {__index=base})
  return setmetatable({class='Fixture',handle=31}, {__index=derived}),base,derived
end
local all,base,derived=object(live_names)
local rows=T.SelectedActions(all)
local curated,more,async,seen=0,0,0,{}
for _,row in ipairs(rows) do
  if row.method then
    assert(not seen[row.method]); seen[row.method]=true
    if row.id=='selected_more' then more=more+1; if row.async then async=async+1 end
    else curated=curated+1 end
  end
end
assert(curated==21 and more==84 and async==12 and #rows==109)
assert(seen.CheatKill and seen.CheatDespawn and not seen.CheatAddDustRC)
local rc=object({'CheatAddDustRC'})
assert(T.SelectedActions(rc)[1].method=='CheatAddDustRC')
local c=object(colonist_names)
local curated_colonist=0
for _,row in ipairs(T.SelectedActions(c)) do
  if row.method and row.id~='selected_more' then curated_colonist=curated_colonist+1; assert(row.method=='CheatDelete') end
end
assert(curated_colonist==1)
SelectedObj=all
for _,name in ipairs(live_names) do
  if seen[name] then
    for _,row in ipairs(rows) do
      if row.method==name and row.id=='selected_more' then
        local count=#records
        local ok,result=T.Run(row.id,all,name)
        assert(ok and all.called==name and result.method==name and result.category==(row.async and 'AsyncCheat' or 'Cheat'))
        assert(#records==count+1 and not taint)
      end
    end
  end
end
for _,name in ipairs({'CheatFill','CheatEmpty','CheatAddDustRC','NotACheat','CheatMissing'}) do
  local ok,result=T.Run('selected_more',all,name)
  assert(not ok and result.status=='REFUSED')
end
assert(not T.Run('selected_more',all))
assert(not T.Run('selected_more',rc,'CheatKill'))
SelectedObj=nil; assert(not T.Run('selected_more',all,'CheatKill'))
SelectedObj=all
base.CheatKill=nil; assert(not T.Run('selected_more',all,'CheatKill'))
derived.CheatKill=function(self) self.called='override' end
assert(T.Run('selected_more',all,'CheatKill') and all.called=='override')
all.CheatKill=function(self) self.called='instance' end
assert(T.Run('selected_more',all,'CheatKill') and all.called=='instance')
all.CheatKill=function() error('leaf failure') end
local ok,result=T.Run('selected_more',all,'CheatKill')
assert(not ok and result.status=='ERROR')
all.CheatKill=function() taint=true end
local count=#records; T.Run('selected_more',all,'CheatKill')
assert(#records==count+2 and records[#records]:find('SMRTK_TAINT action=selected_more',1,true))
taint=false
local col=object({'CheatKill'})
col.CheatKill=Colonist.CheatKill; col.SetCommand=function(self,command) self.command=command end
SelectedObj=col; assert(T.Run('selected_more',col,'CheatKill') and col.command=='Die')
local drone=object({'CheatDespawn'})
drone.CheatDespawn=Drone.CheatDespawn; drone.DespawnNow=function(self) self.deleted=true end
function SelectObj(value) SelectedObj=value end
SelectedObj=drone
ok,result=T.Run('selected_more',drone,'CheatDespawn')
assert(ok and not result.valid_after and SelectedObj==false)
-- Real and game-time threads are distinguished; selection is checked after queuing.
local real,game=0,0
function CreateRealTimeThread(fn) real=real+1; queued[#queued+1]=fn end
function CreateGameTimeThread(fn) game=game+1; queued[#queued+1]=fn end
local click=object({'CheatKill','AsyncCheatInspect'})
SelectedObj=click
local dlg=InfopanelDlg:new({IdNode=true},interface,click)
XWindow:new({Id='idContent'},dlg,click)
assert(T.Run('section_attach',dlg))
local function find(win,text)
  for _,child in ipairs(win) do
    if child.class=='XButton' and child[1] and child[1].Text==text then return child end
    local match=find(child,text); if match then return match end
  end
end
local kill,inspect=find(dlg,'Kill'),find(dlg,'Inspect')
assert(kill and inspect and kill.MinWidth==296 and inspect.MinWidth==296)
count=#records; kill:OnPress(); assert(game==1 and real==0); run_queued()
assert(click.called=='CheatKill' and #records==count+1)
count=#records; inspect:OnPress(); assert(game==1 and real==1); run_queued()
assert(click.called=='AsyncCheatInspect' and #records==count+1)
inspect:OnPress(); SelectedObj=col; count=#records; run_queued()
assert(#records==count+1 and records[#records]:find('status=REFUSED',1,true))
''')
print('03C DESK: PASS — source-union 106/106 (RC alias separately), 84 More / 12 async, exact Kill/Despawn bodies, inheritance/overrides, refusals, errors, taint control, thread categories, queued selection race')
print('03C SOURCE SHA256:', hashlib.sha256((kit / 'Code/73_SMRTK_Infopanel.lua').read_bytes()).hexdigest())
```

Additional gates: `python tools/parsecheck.py --dir C:/Dev/SMR-BugFixPack-TestKit/Code --quiet`
and `python tools/doccheck.py`. Rule 9 review: the change registers only toolkit
functions/actions and creates toolkit controls; it introduces zero real-global
writes or vanilla function replacements. No probes were registered.

Measured at pack `48f75a0` / TestKit parent `87f3130`, edited P2 SHA256
`b8105bf58f0e3fae59a58fe200328567381855d4f5f1a6fa31c36bdc49010daa`:
live census **4715 Lua files**, **150 explicit bodies**, **94+12 names**;
03C DESK **PASS**, existing P2 DESK **PASS**, parsecheck **34 files / 0 errors**;
rule 6 **0 lines in 9 files**, rule 7 **0 lines**, presence **26 lines / 13 calls**.
Final doccheck/commit checks are recorded by the close-out git commands.

## DEPARTURES

- More buttons use one full-width column (296 px), with the exact method in the
  rollover; curated/inspection controls retain two columns. Longer discovered
  names need the extra width. No new UI hook or input route was introduced.
- Async clicks use a real-time thread rather than the curated game-time thread.
  This keeps local debug/editor actions in vanilla's async category while retaining
  the proven leaf dispatch and core logging/taint assertion. It adds no wrapper.
- `selected_more` has no page/menu annotation: it is a parameterized section
  dispatcher, not an independently executable menu command. More rows pass both
  expected object and exact method; callers cannot enter curated methods with it.

## SUGGESTIONS

- In 08 measure long labels, scrolling and debug/editor availability by name.
  Editor-opening async methods can temporarily block achievements without taint;
  do not equate a clean taint read with eligibility.
- Consider a future audit gate against changed/new vendor method bodies. Dynamic
  discovery alone does not certify a future leaf's call graph.

## DRIFT for 99

- A naive colon-definition census found 100 names; the generated upgrades are
  required to reproduce 106. Read the `DefineConstInt` and generation loop.
- The preserved curated contract is 21 registry actions over 22 method names,
  with Add Dust choosing its first supported alternative. An all-methods fixture
  therefore has 105 method buttons; reporting 106 simultaneous buttons is false.
- P2's old CATALOG line exercises only its curated all-members proxy, whose
  `__index` is a function. Vanilla's chain walk stops there. Its 21+4 output is
  still valid for that fixture but cannot measure the new dynamic coverage.
- The README Ordering line omitted 03C although its queue had inserted it;
  corrected with this close-out. Prior 03B inbox wording is historical and is
  superseded by the 03C outbox, not silently rewritten.
- Rule 6's presence control is 26 matching lines, of which 13 are actual calls;
  no zero/13 claim was inherited from the stale recipe.
- My first report-fence extraction matched the fence marker inside its own
  instruction and executed an empty string with exit 0. Anchoring the marker at
  line start fixed the instrument; the run then printed the full census, gates,
  P2 PASS and 03C PASS. An exit code without witnesses was insufficient.

## OWNER-ROUTED / for 07

OWNER-ROUTED: ck175 item 1's extension is built on P2's existing leaf route;
08 remains the first sitting. No new owner decision or additional boot requested.

OWNER-ROUTED: 07 must include a More Cheat leg (Colonist Kill or Drone Despawn),
a More AsyncCheat leg (Inspect, and Properties only with editor closure/eligibility
context), stale-selection refusal, long-label/scroll inspection, and clean/tainted
read witnesses. These are named parts of the already-owed 08 sitting.

For 07: document 106/106 source-name capacity with the conditional AddDustRC alias
omission, not a claim that the section replaces the whole cheat menu or that every
debug/editor feature is available in retail. Keep eligibility UNAVAILABLE:sandbox.

## Close-out

TestKit commit **`f093e3b`**, local-only, contains only
`Code/73_SMRTK_Infopanel.lua`. Pack close-out is identified by git log for this
report and the handoff files. 03C is consumed; NEXT Codex 07, then 08, 99.
