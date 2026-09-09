VERDICT: PARTLY AGREE

READ + MEASURED (desk, binary and archived logs): runtime fingerprints are a useful route to a stronger, explicitly bounded promise, but the audit does not establish that its proposed mechanism makes even the scoped sentence literally true. I refuted its F114 probe impossibility, its StaleReservations ceiling, its upper bound on bytecode false alarms, and its account of one archived blame line. I also found an indirect code-loading route omitted from its sandbox analysis. Recommend a measured capability pilot, then checks over declared dependencies and all-before-write installation, with UNKNOWN declining the affected fix. Neither today's five probes nor arity alone justifies strengthening the public claim.

## Where you differ

READ — Scope and notation: commissioned under `docs/agent/prompts/CODEX_CROSSCHECK_SELFCHECK_PROMISE.md`; the supplied nested pathname did not exist. Audit read in full, including its omissions and original brief. Repository started at `8e0f43dff20a83cb21db2b0c4e1f00597eaa47d3` after `git pull --ff-only`. Another session subsequently committed `33b3ad0`; `git diff 8e0f43d --name-only -- Code items.lua metadata.lua tools/bodycheck.py tools/sigcheck.py docs/agent/reports/SELFCHECK_PROMISE_AUDIT.md` was empty. In citations below, **S/** means `A:/SteamLibrary/steamapps/common/Project Spark/ModTools/Src/` and **O/** means `C:/Dev/SMR-SrcArchive/1.0.7.396349/Src/`. MEASURED never means an attended game result here. No game was launched, no game-directory file written, and no status or store text changed.

### D1. StaleReservations is an incomplete dependency manifest, not an impossibility proof

MEASURED — I independently compiled the complete source files with stock Lua 5.3, located function prototypes by their compiler-provided definition lines, and compared both source and normalized prototype bytes. `Residence:GetFreeSpace` and `Residence:ReserveResidence` are unchanged. **`Residence:CancelResidenceReservation` changed.** Its 1.1.0 body adds:

```lua
-- the expedition hold rides on this reservation; don't let it outlive it
unit.expedition_residence = false
```

READ — This is not a distant speculative dependency: our sweep calls that exact method at `Code/Fix_StaleReservations.lua:159` and already declares it in `Require` at `:100`. The new statements are at `S/Lua/Buildings/Residence.lua:393`; compare `O/Lua/Buildings/Residence.lua:353`. Pinning every function the module already requires would have included the changed cancellation body. That would not *explain* expedition reservations, but it would conservatively stand the module down before its destructive sweep. The audit's §4.8 and §5.3b claim that F-2 is invisible to any runtime check is refuted.

READ — A more general limit remains: unchanged checked functions can depend on unobserved state or C behavior. This case does not prove that limit; it instead demonstrates why the checked dependency set matters. F-3 also illustrates that a “signature change” can mean `traits` becoming `colonist` **at the same arity**, beyond an arity check's reach (`S/Lua/Buildings/Community.lua:442`).

### D2. A plausible 1.0.7 access trace detects F114 without inventing its failing input

MEASURED — I executed the actual two `Train:UnloadAll` bodies on a normal `Metals` resource with a **present** demand request, zero carried stock, zero target amount, and empty assignments. No nil-demand case, BlackCube-specific fixture, transfer, or engine state was involved. An uncached proxy recorded:

```text
1.0.7: station.storable_resources,stored.Metals,station.demand,demand.Metals,target
1.1.0: station.storable_resources,stored.Metals,station.demand,station.demand,demand.Metals,target
```

READ — The second `station.demand` access follows directly from `station.demand and station.demand[res]` at `S/Lua/Units/Train.lua:794`, replacing the single access in `O/Lua/Units/Train.lua:796`. Comparing the whole trace against a 1.0.7 recording would decline on 1.1.0. This refutes “no 1.0.7-era probe could catch it,” not the narrower point that an output-only test may miss it. The trace is intentionally brittle: harmless extra reads also decline. It still observes one path, requires a per-target contract, and is not universal.

### D3. Source hashes do not upper-bound normalized bytecode mismatches

MEASURED — My independent parser compiled **whole source chunks**, without executing them, to preserve surrounding lexical bindings. Of the current manifest's **47 named-function rows**, 46 resolve at the same paths on both trees: **27 normalized prototypes differ and 19 agree**; SaintBlessing's old pathname is absent. The affected set, including that absence, is **25 modules: seven FIX rows and 18 KEEP rows**. This is a same-compiler desk comparison, not a forecast of engine dumps. No source-changed named-function row became byte-identical in this experiment.

MEASURED — Two KEEP modules have equal function source after the manifest's whitespace normalization but different compiled prototypes:

| module | additional difference |
|---|---|
| `DroneTransportMinors` | `UpdateRocketsInternal` captures `rfRestrictorRocket` from enclosing local slot 11 on 1.0.7 and slot 12 on 1.1.0: upvalue descriptor bytes `01 0b 00 00` → `01 0c 00 00`. Instructions and constants match. |
| `ShuttleTransportCache` | `FindTransportationModeToCommunity` now captures a file-local `ipairs` (`S/Lua/Units/Colonist.lua:13`); the old function read the global. Its unchanged normalized source compiles to different instructions, constants and upvalue descriptors. |

MEASURED — The small control `local captured=7; return function(x) return captured+x end` versus the same text with `local spare=0;` before it also changes the captured-slot descriptor after all line numbers are zeroed. The compiler has not changed. Conversely, two closures from the **same** factory with different captured values have equal stripped dumps and return different answers: `make(1)(1)=2`, `make(2)(1)=3`. Dumping a closure does not serialize its captured values.

READ — Thus the audit's “at most 17, probably fewer,” “only the compiler changing can flip hashes without target source changing,” and five-minute “bodycheck unchanged implies recompiled” diagnoses do not hold. Parent lexical context, global-to-local binding changes, DLC overrides, or other mods can contribute. The 18 KEEP result excludes the two literal-line-span rows; it is not a full code-and-data gate count. The original 24-module source result includes Sinkhole's line-span row and excludes these two additional modules.

READ — Do not merely zero all upvalue descriptors to suppress this noise: that can conceal a changed binding. Treat full-body identity and dependency values as distinct evidence, with conservative stand-downs until re-reviewed.

### D4. “Zero authoring” is true only of the expected arity value

MEASURED — Independently extracting compiler arities at the **15 full replacement sites** gives one difference against 1.0.7, LandscapeForEachUnit: `(3, vararg)` versus `(2, vararg)`. All 15 match 1.1.0. This supports the narrow arity mechanism.

READ — The core currently receives `Register(id, def)` and `Require(id, spec)`, not pairs of original/replacement functions for every assignment. `SetGlobal` covers five sites, including wrappers; most method replacements are direct assignments to existing table keys, which a metatable `__newindex` cannot intercept. ExtenderFlapChurn installs at file scope before `Register` (`Code/Fix_ExtenderFlapChurn.lua:78`). Three modules bypass `Require` altogether. Arity comparison therefore requires an explicit install API, descriptors or an author-time rewrite/check. It is not a core-only 40-line change with zero integration work.

READ — A body pin in a `-- BYTECODE:` **comment** is not runtime data. It needs a generated Lua literal/descriptor and a checked delivery path, or an explicitly validated file-read mechanism. Prefer the literal. Selecting targets and dependency fields also costs reading; “one pin line, zero reading per future module” is not defensible.

### D5. The blacklist is not the entire reachable capability graph

MEASURED + READ — Direct `debug` is withheld; the archived Test Kit confirms that. However, `S/CommonLua/Core/ToLuaCode.lua:390` defines non-blacklisted `LuaCodeToTuple(code, env)`, which calls `load("return " .. code, nil, nil, env or _ENV)`. The function executes in the engine's own environment. The blacklist-gather handlers also do not add this name (`Mod.lua:1455`, `Core/lib.lua:3179`, `GedGameObjectEditor.lua:391`, `Libs/Paradox/ParadoxMods.lua:282`, `Platforms/steam/SteamMods.lua:68`).

MEASURED — With the real sandbox and serialization helper in stock Lua 5.3, **and an explicit pass-through stub for C-side `ChecksumRemove`**, a mod chunk read:

```text
direct debug: nil
LuaCodeToTuple with omitted env: debug table, nparams 2
LuaCodeToTuple with explicit mod _G: created function returns 42; debug still nil
```

READ — This refutes the completeness of “load is blacklisted, therefore no loading route exists.” It is **not a boot-confirmed sandbox escape**: `ChecksumRemove` and any C-side caller restrictions remain unmeasured. §Runtime supplies a harmless capability probe. Even if confirmed, do not make access to deliberately withheld engine authority the pack's compatibility foundation. An explicit mod environment is the candidate if dynamic code ever earns a legitimate use; provenance-hiding trampolines remain a poor mitigation.

READ — Other omitted helpers include `GetFuncSourceStringIndent` (`ToLuaCode.lua:781`), `GetFuncBody` (`:824`), and `ValueToLuaCode(function)` (`:146`), which call the blacklisted source helpers internally. They depend on `FuncSource`/`FetchLuaSource` and may have no source on player installs. `GetFuncBody` can return an empty fallback; `AreFuncsEquivalent` at `:845` can treat two missing bodies as equivalent. Such absence must never become permission.

### D6. One archived blame explanation is wrong

MEASURED — The four blame lines and the duplicate-prefix count are correct, but `docs/archive/act1_Mars.exe-20260819-15.18.19-6a22b86d.log:522` is not evidenced as a Test Kit `quit()` throw. At `:397` and `:416`, **vanilla** `Data/LawDef/LawDef-Welfare.lua:1892` and `:2026` throw on `ActiveLaws`, through Test Kit `40_Probes_Wave4.lua(921)` and `00_TestCore.lua` frames. The later blame line names the Test Kit. There is no logged `quit()` throw in that file.

READ — The audit's supporting `docs/archive/SESSION_LOG.md:7891` describes **July 25** legs, not this August 19 session. It cannot establish this cause. The archive therefore contains a case of a named mod with an upstream vanilla throw site. That does **not** prove the Test Kit innocent: its synthetic input may have caused the invalid call. Distinguish “throw location differs” from “causal misattribution.” I still found no archived throw-location misattribution naming the **fix pack itself** among its three blame lines (two distinct sessions).

READ — The recommendation that a breadcrumb would turn F104/F105 into one-line causal triage is too strong. A throw site narrows triage; it cannot exclude our changing an input or earlier state.

### D7. The scoped promise also requires atomic preflight and a consistent UNKNOWN policy

MEASURED — Executing the actual `run_apply` implementation from `Code/00_Core.lua:447` with an apply function that changes one local fixture target and then returns `"second pin declined"` yields **status `inactive` while the target remains changed**. `pcall` is not rollback. This is a control of the runner's semantics, not a claim that an existing module takes that exact path today.

READ — Checking each site just before its write can strand earlier sites in a multi-site module when a later check declines. File-scope wrappers and deferred data/save handlers must also be included in “before it touches anything.” Existing handlers, already-edited presets on reload, and previous save repairs do not disappear when a later status becomes inactive. Recommend collecting and validating the complete planned write set before any writes; deferred passes need their own phase-specific check and an idempotence record.

READ — The audit's “abstain” on an unavailable dumper, unfamiliar format, or mass mismatch cannot mean “continue applying unverified” while claiming unconditional stand-down. Either UNKNOWN declines the affected module, or the published claim explicitly excludes that condition. A quorum is useful diagnostics, not evidence that any one mismatched body is compatible. FNV-1a also offers a compact probabilistic fingerprint, not literal byte identity. Exact normalized-byte comparison avoids hash collisions if strict identity is actually required.

READ — Keep probes for narrowly demonstrated branches, but do not call a benign stand-down costless safety: withholding a working loss-prevention fix re-exposes its original player loss. A fix adding only an unearned bonus has a different trade-off under the owner's rule. Finally, arity-only deployment does not earn the audit's §6 “every fix ... reshaped” wording, and four no-Require modules/deferred work need route checks even for today's proposed existence-only wording.


### D8. Smaller corrections still affect implementation

READ + MEASURED — C1's fifth probe runs in SaintBlessing's deferred data pass; C2's GameVar initialization is conditional, so a live apply does not imply false globals. C7's stock header is 33 bytes plus the root-upvalue byte, and a plausible altered layout can survive structural parsing. C12's matching uses the existing converted OS path instead of checking both path forms, and dependency order can differ from enable order. C14's ordinary tail-call result does not rule out a custom engine history. C15's permitted handler appends after the engine handler and cannot annotate the box by reassigning the error string. The table below records each source location or independent measurement; none of these runtime gaps is cleared by the stock-Lua controls.

## The §3 table, answered

READ — Verdicts below distinguish observations from wider inferences. Independent programs were run through PowerShell single-quoted here-strings piped to `python -B -`, using `lupa.lua53`, never the default Lua 5.5 runtime reported by doccheck.

| claim | verdict | evidence |
|---|---|---|
| C1 | CONFIRMED, with timing correction | **MEASURED:** actual execution of all 44 module chunks in a recording Lua environment registered 44; no chunk-load errors. Intercepting real `Require` calls captured seven test modules and four apply-time probe modules. Executing SaintBlessing's deferred pass with a minimal candidate preset captured its fifth probe. Final union: 5 probe, 7 test, overlap 3, neither 35. No-Require: ExtenderFlapChurn, SequenceLatents, ShelterReflex, DustSicknessBiorobots. DataPatch: DustSicknessBiorobots, SaintBlessing, SinkholeIndestructible. `doccheck --emit-counts` independently agreed on 44/45 and manifest sets. This is not five probes running in apply. |
| C2 | PARTLY | **MEASURED:** actual LandscapeForEachUnit bodies executed with both false and table-valued old `Landscapes`. Old-shaped call on new body throws in both conditions; current map-stub probe passes new and declines old in both. **READ:** `GameVar` only resets to false on FirstLoad or missing key (`S/CommonLua/Core/lib.lua:1069`); “every GameVar is false on every apply” is false generally. Optional reconciliation can call apply live, although this pack currently has zero optional modules. No shipped `string.Landscapes` assignment found in the source search; engine string metatable still needs §Runtime. The probe observes the storage/signature correlate, not the later filter argument. |
| C3 | REFUTED | **MEASURED:** normal-resource access trace in D2 distinguishes the actual bodies with a present demand request. Unknown-axis output changes remain unbounded; the universal impossibility claim does not. |
| C4 | PARTLY | **MEASURED:** direct `debug.getinfo` absence at `archive/logs/first110_Mars.exe-20260908-15.20.28-6a91a190.log:70`. **READ + MEASURED conditional replica:** indirect LuaCodeToTuple route in D5; no direct alias found in searched engine code, safe rawget/getmetatable do not alone expose engine _G. Indirect runtime reachability is still owed. |
| C5 | PARTLY | **READ:** `Mod.lua:1559` returns the real string table for an allowed global. Whole-Src searches for `string.dump`, `dump = nil`, `strlib` and `string_dump` found no Lua removal; autorun's opening and pre-mod loading stages were read. **MEASURED:** binary registration table in C6. Registration/later C mutation still need an actual mod-context dump. |
| C6 | CONFIRMED as binary evidence | **MEASURED:** executable is 18,741,760 bytes, SHA-256 `28599c4acf318b0354969fe7e537fbcea6251e14616368a0274b7ff492293c6f`. I parsed PE section addresses and followed the `dump` string's pointer into the **registration pointer table**, not merely adjacent strings. At file offset `0xbfdcd0` it points to `dump` and code VA `0x1400c9030`. The table includes byte, **char**, dump, find, format, gmatch, gsub, len, **lower, match**, rep, reverse, sub, **upper**, pack, packsize, unpack, then null. This agrees with the [stock registration order](https://www.lua.org/source/5.3/lstrlib.c.html); missing neighbors were string placement, not missing entries. This does not prove subsequent runtime retention. |
| C7 | PARTLY | **MEASURED:** stock header is **33 bytes**, plus one root-upvalue-count byte; sizes `4/8/4/8/8`. For a stripped root, parameters start at one-based `H + 3 + 2*sizeof(int)`, where `H=17+sizeof(lua_Integer)+sizeof(lua_Number)`. This is 44 here, matching the proposed numeric offset, not universally a fixed 34-byte header. Five truncated samples were rejected. A same-header specimen with plausible parameter/vararg bytes swapped still parses and consumes exactly; consumption alone cannot certify a custom layout. Executable has LUAC_DATA and double 370.5; no contiguous eight-byte 0x5678 was found, which does not disprove an immediate constant. Actual engine layout is COULD NOT TEST. Format reference: [Lua dump implementation](https://www.lua.org/source/5.3/ldump.c.html). |
| C8 | PARTLY | **MEASURED:** chunk-name/local-name invariance holds for controlled fixtures; recursive line normalization handles line shifts. D3 proves other nonsemantic changes survive stripping, and changed captured values need not affect a dump. **READ:** ordinary comments outside strings differ from changes inside literals; normalized bytecode is not semantic equivalence. |
| C9 | PARTLY | **MEASURED:** requested tool reruns give exactly 1 MISMATCH, 27 BODY-CHANGED and 1 TARGET-ABSENT, across 24 current modules. Reconciliation against PACK_1_1_0_REVERIFICATION §1a/§1d yields seven FIX, 17 KEEP. Independent whole-chunk compiler result is D3: 25 named-function-affected modules, seven FIX and 18 KEEP. Source line-span comparisons are not function fingerprints; comparing current survivors against the old branch is not a measurement of an actual historical pinned installation. |
| C10 | PARTLY; ceiling REFUTED | **MEASURED:** the two named Residence bodies really are identical. Their already-required cancellation callee is not. Relocating Saint's old definition to `O/Lua/ClassDefs/ClassDef-PresetDefs.generated.lua:1774` finds the function, same arity 3/0 but different body from `S/Lua/TraitPreset.lua:77`. F-3's GetScoreFor body also differs at unchanged arity. Stub evaluation of both CommanderProfilePreset files finds ten per-building +10% effects versus two Extractors-wide effects, proving a data projection can detect F-5. |
| C11 | PARTLY | **MEASURED:** compiler-assisted install census, crosschecked against visible declarations/SetGlobal sites: 43 function sites = PRE-TAIL 15, POST 13, REPLACE 15; 17 module-level handlers and four data operations = 64 under the audit's counting convention. No PRE-NOTAIL found. **READ + MEASURED:** ten selected probe attempts below invalidate the classification as a hard ceiling. I did not independently certify its “30 hazards” tally or relabel all 44 modules. |
| C12 | PARTLY | **READ:** substring match, per-ID dedupe, and asynchronous title-list box confirmed at `S/CommonLua/Modding/Mod.lua:2975`. `os_paths` replaces content_path with the OS path **only if it exists**, otherwise falls back; it does not check both. Order is `ModsLoaded`/dependency loading order: `GetLoadingQueue` at `:1907` recursively queues dependencies before dependents, so it need not equal enable order. Exported `string.find_lower` docs describe substring search; C behavior with pattern punctuation remains unmeasured. `gamelib.lua:1060` only sets a configuration flag; C decides resulting stack contents. **MEASURED:** 157 F114 error headers after the session's sole pack blame line. |
| C13 | REFUTED as stated | **MEASURED:** 105 logs, four blame lines, three sessions; 14,539-byte/274-line unforced file is an exact prefix of f114repro. Act1 has vanilla throw sites through Test Kit, not evidenced quit failure (D6). Forced110 `:278/:300` is our LowStorageWarning throw; f114repro `:247/:274` is our LandscapeUnitFilter throw; unforced is its duplicate. Markdown archive hits include SESSION_LOG summaries but no additional independently identified raw session. **READ:** F104 `:66` and F105 `:384` support field pass-through cases; original reporter attachments were not opened. |
| C14 | PARTLY | **MEASURED:** separately named thrower/wrapper chunks show no WrapperSite.lua in stock traceback after a proper tail call, while a call hook observes the tail-call event. **READ:** [Lua 5.3 §3.3.7](https://www.lua.org/manual/5.3/manual.html#3.3.7) supports lost ordinary caller debug information. It does not prove a custom engine has no prior hook/history. No engine GetStack implementation was executed or fully disassembled. An outer procall/sprocall adds its own frame; it does not by itself recreate the discarded wrapper. |
| C15 | PARTLY | **READ:** OnLuaError is permitted; safe_OnMsg appends through the real handler registry (`Mod.lua:1603`; `cthreads.lua:15`, `:64`). Engine handler precedes normally loaded mod handlers. Local reassignment of an error string cannot annotate the engine's copy. ReportModLuaError constructs new text and ignores its incoming err/stack for display. Direct load names are blocked, but D5 defeats the “therefore impossible” deduction. config and ReportedMods are reachable; suppression remains rejected. Exact C message arguments still need §Runtime. |
| C16 | CONFIRMED as source reachability | **READ:** LuaRevision is initialized/read as an engine global (`autorun.lua:15`, `:269`; `Mod.lua:919`), absent from the initial and additional blacklists. **MEASURED:** archived boot prints 403908; the serializer/sandbox route does not need a version field. This does not make the mod's own 350453 metadata discriminatory or authorize a version gate. |

### Ten probe challenges, named

READ — The following treats “safe” as bounded to the source path and supplied stubs, never to every future replacement body. Function-body replicas use real source text; engine-dependent helpers are identified where modeled.

| audit class / selected module | attempt and result |
|---|---|
| UNPROBEABLE — AnomalyCaveInMap | **MEASURED:** FindCaveInLocation accepts a plain map with read-only grid fields, a stub City:Random returning a fixed seed, and GetRandomPassablePoint returning a unique marker without invoking the callback. Captured `seed,point` and marker return. **READ:** `CaveInRubble.lua:21` shows all reached operations; no SessionRandom, world RNG, rubble or thread is required on this target. At least PARTIAL is defensible; TriggerCaveIn's hazardous branch remains unprobed. |
| PARTIAL — DomeFreeSpaceMismatch | **READ:** tried a home proxy recording `working` versus `ui_working` in GatherFreeLivingSpaces. `ValidateBuilding` (`Workplace.lua:1316`) first calls C IsValid; a plain fixture cannot establish the relevant home path. An empty list returns a trivial result and is not permission. No safe discriminating production probe established. |
| UNPROBEABLE — DestroyedTunnels | **READ:** a proxy can record the linked_obj read, but cannot distinguish a later destroyed guard if C IsValid rejects that object first (`Tunnel.lua:193`). Passing a real object risks pf.AddTunnel. No adequate safe probe established. |
| PARTIAL — MirrorSphereSite | **READ:** an IsActionEnabled stub plus progress=100 reaches the old early return (`MirrorSphere.lua:836`), but removing that condition reaches InteractionRandRange **before** the next controllable object method. A pcall cannot undo that RNG change. Keep as a hazardous partial idea, not a certified probe. |
| PARTIAL — TrainWaitTime | **MEASURED:** BoardVehicle stub captures AddSpentTime=10 with start_wait=990 and clock=1000; destructor-registration/call methods are inert, holder is kept different from vehicle, and no PlayPrg runs. The real RebuildInfopanel body runs with SelectedObj=false; its scheduling/mutation helpers are tripwires. Ticket clock stays 990. **READ:** proves the limited call-order/timestamp axis (`ColonistTransport.lua:614`), not live boarding or statistics correctness. |
| PROBEABLE — DroneTransportMinors | **MEASURED:** Fuel and Metals restrictor entries, empty serviced_rockets: Fuel cleared, Metals retained. The replica supplies the captured rfRestrictorRocket constant. **READ:** candidate works on this narrow axis; zero serviced rockets is essential to avoid object/request calls (`DroneControl.lua:672`). |
| PROBEABLE — FreedHousingNotice | **MEASURED:** RemoveResident on private colonists/reserved tables calls the occupation stub and ResetFreeSpace exactly once. **READ:** table.remove_entry modeled locally; no real colonist was used. This checks the callee's vacancy behavior, not every effect of the patched Colonist:SetResidence path. |
| PROBEABLE — GhostFarmOxygen | **MEASURED:** crop=nil, captured SetModifier(air_consumption, id, 0, 0) and Notify(UpdateWorking). **READ:** the audit's one-line sketch omits Notify at `Farm.lua:643`; a complete stub must supply it. With that supplied, I found no current-body side effect on the chosen path. |
| PROBEABLE — LanderEmptyLaunch | **MEASURED:** seven private methods can make IsCargoReady return true and positively capture a cargo-status read. **READ:** CheckAutoDepart=false takes `UniversalRocket.lua:550`; this does not establish the fix's CheckAutoDepart=true branch, wait-window logic or request semantics. A returned true alone is insufficient evidence for that stronger claim. |
| PROBEABLE — StaleReservations | **MEASURED:** successful ReserveResidence changes only private reservation/unit tables, calls a private cancellation stub once and a private ResetFreeSpace. **READ:** confirms a safe reservation operation, but does not detect the new cancellation semantics. D1's callee pin is stronger for this historical failure. |

READ — No five selected PROBEABLE targets were shown inherently unsafe on a correctly completed current-body stub. I did find incomplete contracts and proxy limits, and one explicit counterexample to “UNPROBEABLE.” Therefore I retain the hazard concern, not the 13/8/23 split as a proved limit. Deferred data checks and safely intercepted dependencies also make “probeable at cold apply” different from “checkable before this fix's first mutation.”

### Reproduction record

MEASURED — These requested commands were run directly, in addition to the independent experiments:

```powershell
python -B tools/bodycheck.py --src 'C:\Dev\SMR-SrcArchive\1.0.7.396349\Src'
python -B tools/sigcheck.py --src 'C:\Dev\SMR-SrcArchive\1.0.7.396349\Src'
python -B tools/doccheck.py --emit-counts
python -B tools/sigcheck.py --all
rg -n 'Error in mod|Mod Flagged|Mod-related problem' docs/archive -g '*.log' -g '*.md'
```

MEASURED — The independent bytecode comparator below is the parser and whole-chunk comparison actually used. Run from this repository with Python 3.13/lupa.lua53; it loads source into Lua's compiler but never executes the compiled game chunks. It zeros only definition-line integers, including nested prototypes; all instructions, constants, upvalue descriptors and stack sizes remain. A declared old pathname absence remains UNKNOWN until manually relocated, as for Saint. This is an audit instrument, not a proposed production parser.

```python
import re, struct, hashlib, json
from pathlib import Path
from lupa.lua53 import LuaRuntime
NEW=Path("A:/SteamLibrary/steamapps/common/Project Spark/ModTools/Src")
OLD=Path("C:/Dev/SMR-SrcArchive/1.0.7.396349/Src")
L=LuaRuntime(encoding=None,unpack_returned_tuples=True)
compile_dump=L.eval(b"function(s) local f,e=load(s,'@audit','t',{}); if not f then error(e) end; return string.dump(f,true) end")
class Dump:
 def __init__(self,b):
  self.b=b; self.p=0; self.nodes=[]
  assert self.take(12)==b'\x1bLua\x53\x00\x19\x93\r\n\x1a\n'
  self.cint,self.szt,self.ins,self.lint,self.num=self.take(5)
  v=self.take(self.lint); self.endian='little' if int.from_bytes(v,'little')==0x5678 else 'big'
  assert int.from_bytes(v,self.endian)==0x5678
  assert struct.unpack(('<' if self.endian=='little' else '>')+'d',self.take(self.num))[0]==370.5
  self.header_len=self.p; self.nup=self.u(1); self.root=self.proto(); assert self.p==len(b)
 def take(self,n):
  assert 0<=n<=len(self.b)-self.p,(self.p,n,len(self.b))
  x=self.b[self.p:self.p+n];self.p+=n;return x
 def u(self,n=None):return int.from_bytes(self.take(n or self.cint),getattr(self,'endian','little'))
 def s(self):
  n=self.u(1)
  if n==255:n=self.u(self.szt)
  return self.take(n-1) if n else None
 def proto(self):
  start=self.p; source=self.s(); pos=self.p; first=self.u();last=self.u()
  params,vararg,stack=self.take(3)
  code=self.take(self.u()*self.ins)
  constants=[]
  for _ in range(self.u()):
   tag=self.u(1)
   if tag==0:v=b''
   elif tag==1:v=self.take(1)
   elif tag==3:v=self.take(self.num)
   elif tag==19:v=self.take(self.lint)
   elif tag in (4,20):v=self.s()
   else:raise ValueError(tag)
   constants.append((tag,v))
  up=self.take(self.u()*2)
  children=[self.proto() for _ in range(self.u())]
  assert self.u()==0 and self.u()==0 and self.u()==0
  n=dict(start=start,end=self.p,first=first,last=last,linepos=pos,params=params,vararg=vararg,stack=stack,code=code,constants=constants,up=up,children=children)
  self.nodes.append(n);return n
 def normalized(self,n=None):
  n=n or self.root; b=bytearray(self.b[n['start']:n['end']])
  for x in self.nodes:
   if n['start']<=x['start']<n['end']:
    i=x['linepos']-n['start'];b[i:i+2*self.cint]=bytes(2*self.cint)
  return bytes(b)
def function_lines(path,selector):
 lines=path.read_text(encoding='utf-8-sig').splitlines()
 if re.fullmatch(r'L\d+-\d+',selector):return None
 name=selector.replace(':',r'[:.]')
 pat=re.compile(r'^\s*(?:local\s+)?function\s+'+name+r'\s*\(|^\s*'+name+r'\s*=\s*function\s*\(')
 hits=[i+1 for i,s in enumerate(lines) if pat.search(s)]
 return lines,hits

cache={}; rows=[]
for p in sorted(Path('Code').glob('*.lua')):
 for line in p.read_text(encoding='utf-8-sig').splitlines():
  m=re.match(r'-- SRC: (\S+) (\S+) sha256=',line)
  if not m:continue
  rel,sel=m.groups()
  if re.fullmatch(r'L\d+-\d+',sel):continue
  values=[];info=[]
  for root in (OLD,NEW):
   path=root/rel
   if not path.exists():values.append(None);info.append('ABSENT');continue
   try:
    if path not in cache:cache[path]=Dump(compile_dump(path.read_bytes()))
    d=cache[path];lines,hits=function_lines(path,sel)
    assert len(hits)==1,(sel,hits)
    nn=[n for n in d.nodes if n['first']==hits[0]]
    assert len(nn)==1,(sel,hits,len(nn))
    values.append(d.normalized(nn[0]));info.append((hits[0],nn[0]['last']))
   except Exception as e:values.append(None);info.append(str(e).splitlines()[0])
  status='UNKNOWN' if None in values else 'SAME' if values[0]==values[1] else 'DIFF'
  rows.append((p.stem,rel,sel,status,info))
print('rows',len(rows),'SAME',sum(r[3]=='SAME' for r in rows),'DIFF',sum(r[3]=='DIFF' for r in rows))
for r in rows:
 if r[3]!='SAME':print(json.dumps(r))
print('diff_modules',len(set(r[0] for r in rows if r[3]=='DIFF')))

affected={r[0].removeprefix('Fix_') for r in rows if r[3]!='SAME'}
fix={'SaintBlessing','ShelterReflex','PayloadTemplateRefill','RocketDroneChurn','LandscapeUnitFilter','VacuumWalks','TrainCargoDumping'}
print('unknown_rows',sum(r[3]=='UNKNOWN' for r in rows))
print('affected_including_unknown',len(affected),'FIX',len(affected&fix),'KEEP',len(affected-fix))

```

MEASURED — Run this second block in the same Python session to reproduce D2 and the two D3 controls. The only engine helper modeled on the reached train path is `Min=math.min`; unexpected station accesses or transfers fail the fixture. All mutated tables are private.

```python
def fnbody(rel,sel,root=NEW):
 path=root/rel; lines,hits=function_lines(path,sel); d=Dump(compile_dump(path.read_bytes()));n=next(n for n in d.nodes if n['first']==hits[0])
 return n['first'], '\n'.join(lines[n['first']-1:n['last']])
for root in (OLD,NEW):
 first,s=fnbody('Lua/Units/Train.lua','Train:UnloadAll',root)
 body=s.replace('function Train:UnloadAll()', 'return function(self)')
 rt=LuaRuntime(unpack_returned_tuples=True)
 rt.execute('Min=math.min')
 fn=rt.execute(body)
 result=rt.eval("""function(fn)
 local trace={}
 local function record(x) trace[#trace+1]=x end
 local req={GetTargetAmount=function() record("target");return 0 end}
 local demand=setmetatable({}, {__index=function(_,res) record("demand."..res);return req end})
 local station=setmetatable({}, {__index=function(_,k)
   record("station."..k)
   if k=="demand" then return demand end
   if k=="storable_resources" then return {"Metals"} end
   error("unexpected station read")
 end})
 local t={current_station=station,assigned_resources={},GetStoredAmount=function(_,r) record("stored."..r);return 0 end,
  AddResource=function() error("unexpected transfer") end}
 fn(t,station)
 return table.concat(trace,","), next(t.assigned_resources)==nil
end""")(fn)
 print(root.name,first,result)
# Counterexamples: equal body source under different lexical surroundings.
for s in [b'local captured=7; return function(x) return captured+x end',
          b'local spare=0; local captured=7; return function(x) return captured+x end']:
 d=Dump(compile_dump(s));n=next(n for n in d.nodes if n['first']>0)
 print('lexical',n['up'].hex(),hashlib.sha256(d.normalized(n)).hexdigest()[:16])
# Runtime closure upvalue value omitted.
rt=LuaRuntime(encoding=None,unpack_returned_tuples=True)
print('same_dump_different_result',rt.execute(b'local function make(k) return function(x) return x+k end end; local a,b=make(1),make(2); return string.dump(a,true)==string.dump(b,true),a(1),b(1)'))

```

## Ideas

READ — All costs below are engineering estimates, not measured timings. They price the described work, not a fresh release sweep for each module. “One module” includes reading its dependency contract, a meaningful negative control and ordinary patch-note maintenance. A pack-wide install migration is a larger change and earns corresponding review. No idea authorizes a game launch, store change or code edit in this task.

| idea | reachable route and what it makes true | build / future-module cost | runtime cost | failure and house-rule assessment |
|---|---|---|---|---|
| I1 — access trace | Allowed tables/metatables, closures and pcall; D2 proves a useful new F114 route. Confirms the recorded path's reads/calls/results. | Generic recorder about half a day; target stub/branch review roughly 0.5–2 hours each, more for engine dependencies. | Linear in recorded accesses; bound traces and forbid unbounded paths. No engine timing measured. | Needs per-target inputs; proxies alter identity/type and cannot observe reads through already captured locals or C internals. New body may act before a stub stops it. Harmless extra reads cause stand-down. Survives “check the thing”; cannot support “every change.” Recommend selectively, with body preflight before execution. |
| I2 — pin callees | Explicit existing Require pairs plus static call candidates; D1 detects F-2, relocated TraitPreset detects F-1, GetScoreFor detects F-3. | Parser/candidate report 1–2 days; manually resolve dynamic dispatch, aliases, inherited methods, generated presets and C boundaries per affected module. | One dump per distinct captured function per load phase; cache by function identity within that phase. | Static names are only candidates; a trace misses untaken paths. Do not repeat EF-078 by treating name discovery as actual resolution. No finite hand-picked set proves arbitrary environmental compatibility. Recommend explicit dependency descriptors first, automated completeness lint second. |
| I3(a) — revision label | rawget(_G,"LuaRevision") after engine initialization; display “fingerprints recorded on X; running Y” alongside outcomes. | Small logging change; stamp with the owner-observed pin receipt. | Constant. | “Verified on X” overstates a pin-only boot. Revision equality is not compatibility; difference is not incompatibility. No gate. §2a's reasons address label-based gating and the mod's nondiscriminating fields; an observation-only engine label does not use either as proof. Its blanket heading warrants an explicit owner clarification before changing policy prose. |
| I3(b) — revision with mass mismatches | Same label plus actual mismatch records; helps group diagnostics. | Small extension after fingerprints exist. | Constant beyond hashing. | Unchanged revision cannot prove “another mod”; compiler/platform/DLC differences or unrevised code can also differ. Changed revision cannot prove “official patch caused this.” Honest as a clue. Using it to waive mismatches becomes a gate and conflicts with §2a. Recommend diagnostics only. |
| I4 — another mod changed target | Dump the function currently resolved at the exact install/capture slot. **MEASURED stock Lua:** another chunk's function dumps successfully; unstripped source contains `@Mod/Other/Code/a.lua`. | Half-day provenance/classification plumbing after the dumper; explicitly store expected original and installed function identity. | Linear dump cost; one identity check is cheap. | Mismatch is a justified conservative decline where our replacement assumes the original body, but not proof the other mod is broken or even identifiable. Source names can be stripped/spoofed; closure environment can differ under equal dumps; a later mod can overwrite us. Log “target differs,” not accusation or player load-order advice. Redact arbitrary absolute source paths from player-facing output. |
| I5 — data projection | DataPatch's ClassesBuilt/DataLoaded/ModsReloaded path; inspect selected scalar fields before any write. F-5's ten effect tuples versus two is measurable. | Shared canonical serializer 0.5–1 day, plus explicit projections and pre/post-state logic for each of the three DataPatch modules; ExoticDepositSign is a fourth data operation. | Linear in selected nodes/fields; cycles and unsupported types decline. | A whole preset includes translations, inherited defaults, functions and incidental data; plain tostring or unsorted pairs is not stable. Preserve array order where meaningful; sort map keys; encode type, nil/false distinction and lengths. Check known input **or our known output** on reload, not a blanket ever_changed waiver. Do not construct objects during apply. Preserves §2/F87 and flags rewritten structures without pretending to inspect every effect. |
| I6 — unstripped dump | Same dumper; source/line tables can map evidence to a human-readable region if the engine retains them. | Small diagnostic parser extension; defect-neighborhood opcode hashing is a separate, larger research task. | Larger dump and parse, only when requested. | A register allocation, constant index or jump crosses source lines; a defect-neighborhood pin misses changes elsewhere and line movement creates noise. Names may be absent in packed code. Recommend provenance/triage only, not a universal guard. |
| I7 — other reachable surfaces | LuaCodeToTuple and source-serialization helpers in D5; ordinary behavior, explicit constants/class fields, function identity and approved data projections. | Harmless capability reads first; no firm production estimate before results. | Usually small for metadata; source retrieval may read files and be unavailable. | tostring(fn) does not encode body/arity; select counts returned values; coroutine wrappers can start unsafe work; generic getmetatable exposes no closure code. Safe source wrappers may return fallbacks. Do not treat absence as equal or route around intentionally blocked authority merely to claim coverage. |
| I8 — more tolerant fixes | Existing pre/post wrappers, corrected inputs, or data patches preserve the shipped body; `SequenceLatents.lua:132` is a concrete pre-normalization route. | Usually hours to a day per suitable fix, including proof the intervention preserves unrelated behavior; not a universal engine. | Small wrapper/data cost. | Full-body mid-loop defects need an actual extension point. F114 transfers resources inside its loop, too late for a post-wrapper. Wrapping every station's methods or temporarily rewriting global inputs changes unrelated behavior. Source patching through the conditional helper route still needs the actual shipped source, validation and authority constraints. Recommend reducing copied bodies only where the semantic boundary is demonstrated; never guessed. |
| I9 — blame mitigation | Add a read-only OnLuaError log breadcrumb with err-site, first recognizable stack frame, pack-frame presence and uncertainty. Existing reporter-log/issue route: player attaches log, owner reads that event and the supporting stack. | Roughly half a day for bounded parsing, duplicate/rate control and malformed-stack fixtures; console behavior needs owner observation. | On errors only; cap bytes and duplicate output. | safe_OnMsg appends; it cannot make a normal mod handler run first. Strings are immutable and ReportModLuaError ignores passed err/stack when building its box. Wrapping it and forwarding altered err cannot annotate the original box. Changing its actual UI is an engine-diagnostic replacement and owner policy choice. A store/support explanation is possible only through the owner's existing publishing route; no such text was posted or verified live here. Console players still need a visible route; a log is not one. |
| I10(a) — checked install transaction | Register receives a plan: exact dependency references, expected evidence and planned writes. Validate **all** before mutation; compare references again before commit; wrappers capture those validated originals. | Core plan runner and adapters approximately 1–2 days; migrating/reviewing 44 heterogeneous modules several further days. New module: explicit targets and reviewed preconditions. | Preflight once per relevant phase; no blanket in-play probing. | Error mid-mutation still requires rollback of owned assignments or preparation that cannot throw. OnMsg registration and data edits need explicit handling; do not roll back someone else's subsequent write. Directly addresses “a declined fix does nothing,” which fingerprints alone cannot. Recommend this before claiming coverage. |
| I10(b) — compiler calibration witnesses | Store expected normalized dumps of small **pack-local** functions covering arity, nested closures, constants, long strings and varargs. Compare current compiled witnesses before interpreting mass target changes. | Half a day after parser; fixtures and negative controls. | Tiny fixed work per Lua load. | Better than revision for detecting an altered compiler/format; only covers witness features. Matching witnesses cannot prove all compilation rules unchanged. Failed calibration means UNKNOWN/decline under a strict promise, not automatic re-pin or pass. |
| I10(c) — target ownership and phase receipt | Record the identity checked, identity installed, load phase, reason and covered dependency names. Report “unavailable/changed/replaced later/pending” separately from “active.” | Half a day of diagnostic plumbing plus adapting deferred handlers. | Small at load and before each planned write; avoid polling every call. | Later overrides can invalidate what was checked; changing a global may not change an already captured reference. A receipt is evidence, not automatic rollback. Names belong in owner logs; no new accusation or load-order instruction on player surfaces. |
| I10(d) — exact pins or collision-resistant digest | Store canonical runtime bytes if literal identity is required; otherwise a strong digest with length, format and declared scope. | Serialization/pin receipt tooling plus file-size measurement; assess actual dumps in the pilot before choosing storage. | Linear in dumped bytes, with startup memory to measure. | FNV-1a alone admits collisions. Exact bytes still omit captured values and C behavior. This removes one mathematical hole, not the dependency problem. No user version gate. |
| I10(e) — separate compatibility from save repair | Give each one-shot repair its own preconditions and receipt when a behavior fix stands down. SaintBlessing already separates new data behavior from repairing earlier pack damage (`Code/Fix_SaintBlessing.lua:103`). | Per-module design/read where a save healer exists, not an all-module tax. | Existing one-shot pass cost plus preflight. | Blanket module stand-down can suppress necessary repair; running old repair code unchecked can damage a changed save shape. Both must be explicit. Fits “repair player losses,” avoids counting favorable bonuses as equal urgency. |

READ — Revised recommendation versus audit §5: keep the desk tools and selective safe probes; first measure capabilities and format on the real mod route. Then prototype a declarative all-before-write gate on the two full-copy failure controls and the StaleReservations callee dependency. Scale to all modules only with measured coverage. Arity is an inexpensive field of that plan, not a standalone universal solution. Do not automatically re-pin after a mass mismatch, and do not claim the scoped wording becomes true when only arity ships.

## Runtime reads still owed

READ — These snippets are **prepared only**, not installed or run. The owner can place them in a temporary Test Kit Code chunk and launch normally; use that mod environment, not an unrestricted console expression as a substitute. They neither write game files nor load a save nor call a portal. Run the capability chunk on cold load and on the owner-controlled enable/reload path, keeping the complete corresponding log. Console-platform behavior requires that platform's owner observation, not a PC-source inference.

### R1. Dumper presence, full header, independent arity controls, phase and string lookup

```lua
do
  local function say(...) print("[CodexSelfcheckRead]", ...) end
  local function inspect(tag, fn, strip)
    if type(fn) ~= "function" then say(tag, "NO_FUNCTION"); return end
    local dump = type(string) == "table" and string.dump
    if type(dump) ~= "function" then say(tag, "NO_DUMPER"); return end
    local ok, data = pcall(dump, fn, strip)
    if not ok or type(data) ~= "string" then
      say(tag, "DUMP_FAILED", tostring(data)); return
    end
    local out = {}
    for i = 1, math.min(#data, 64) do
      out[#out + 1] = string.format("%02x", data:byte(i))
    end
    say(tag, "bytes", #data, table.concat(out, " "))
  end
  local zero = function() end
  local one = function(a) return a end
  local many = function(a,b,c,...) return a,b,c,... end
  local nested = function(a)
    return function(b) return a,b end
  end
  say("revision", tostring(rawget(_G, "LuaRevision")),
      "DataLoaded", tostring(rawget(_G, "DataLoaded")),
      "Landscapes_type", type(rawget(_G, "Landscapes")),
      "debug_type", type(rawget(_G, "debug")))
  local ok, value = pcall(function() return ("CodexMarker").Landscapes end)
  say("string_Landscapes", ok, type(value))
  inspect("zero", zero, true)
  inspect("one", one, true)
  inspect("many", many, true)
  inspect("nested", nested, true)
  inspect("C_control", string.format, true)
  inspect("Landscape_current", rawget(_G, "LandscapeForEachUnit"), true)
  local residence = rawget(_G, "Residence")
  inspect("Cancellation_current",
          type(residence) == "table" and residence.CancelResidenceReservation, true)
  inspect("one_unstripped", one, false)
end
```

READ — `NO_DUMPER` ends the direct dump route on that build. Success with a Lua function and failure on the C control supports it; all four known signatures must decode correctly before any parser is trusted. The complete header, not its first 16 bytes, reveals integer/number sentinels. A non-nil string_Landscapes changes the assumed C2 exception route and requires investigation. The two current target readings **may be pack or other-mod replacements** at Test Kit load time: this establishes reachability, not pristine pins. A pristine pin collector must capture the original inside the owning fix's apply immediately before installation, or operate in a verified mod configuration established by the owner. The captured reference, source provenance and load phase must be logged with the pin.

### R2. Indirect helper capability, without retaining engine objects or loading code into the live world

```lua
do
  local helper = rawget(_G, "LuaCodeToTuple")
  print("[CodexSelfcheckRead]", "LuaCodeToTuple_type", type(helper))
  if type(helper) == "function" then
    local ok, err, result = pcall(helper,
      "(function(x) return x + 1 end)(41)", _G)
    print("[CodexSelfcheckRead]", "explicit_env", ok, tostring(err), tostring(result))
    local ok2, err2, kind = pcall(helper, "type(debug)")
    print("[CodexSelfcheckRead]", "default_env_debug_type",
          ok2, tostring(err2), tostring(kind))
  end
end
```

READ — `true, nil, 42` confirms expression loading in the explicit mod environment, including ChecksumRemove accepting this input. `true, nil, table` confirms engine-environment access through this helper; it does not justify deploying that bypass. Nil helper or either error leaves the corresponding route unavailable/unconfirmed. No debug table, engine _G, executable trampoline or function is retained. If this route fails, still read the R1 result: the direct dumper is independent.

### R3. Other function provenance and source-wrapper availability

```lua
do
  local fn = rawget(_G, "LandscapeForEachUnit")
  local helper = rawget(_G, "GetFuncBody")
  if type(fn) == "function" and type(helper) == "function" then
    local ok, body = pcall(helper, fn)
    print("[CodexSelfcheckRead]", "source_body",
          ok, type(body), type(body) == "string" and #body or -1)
  else
    print("[CodexSelfcheckRead]", "source_body", "UNAVAILABLE")
  end
  local dump = type(string) == "table" and string.dump
  if type(fn) == "function" and type(dump) == "function" then
    local ok, bytes = pcall(dump, fn, false)
    print("[CodexSelfcheckRead]", "target_unstripped",
          ok, type(bytes) == "string" and #bytes or -1)
  end
end
```

READ — Run on the owner's ordinary mod configuration and identify the actual function owner from the pin receipt; a named function is not necessarily vanilla. Nonempty source establishes retrieval for that function/configuration only. Empty/fallback/error is UNKNOWN, never equality. The helper may populate the engine's source cache; it performs no game-state mutation but is not a zero-effect read of internal cache state. To establish cross-mod dumping in-engine, select a function whose receipt shows another enabled mod defined it; do not claim that solely from its name. For unstripped source availability, the R1 local-function control proves format support; a target may still have stripped source.

### R4. Engine stack behavior and handler delivery without deliberate uncaught errors

```lua
do
  local getstack = rawget(_G, "GetStack")
  if type(getstack) == "function" then
    local observed
    local function inspect()
      observed = getstack(1)
      return observed
    end
    local function tail_wrapper() return inspect() end
    local function post_wrapper()
      local result = inspect()
      return result
    end
    local ok1, a = pcall(tail_wrapper)
    local ok2, b = pcall(post_wrapper)
    print("[CodexSelfcheckRead]", "tail_stack", ok1, tostring(a))
    print("[CodexSelfcheckRead]", "post_stack", ok2, tostring(b))
  end
end

-- Passive handler only; registration belongs in a Code load chunk.
OnMsg.OnLuaError = function(err, stack, os_paths)
  print("[CodexSelfcheckRead]", "OnLuaError",
        type(err), type(stack), tostring(os_paths))
  if type(err) == "string" then
    print("[CodexSelfcheckRead]", "err_prefix", err:sub(1, 320))
  end
  if type(stack) == "string" then
    print("[CodexSelfcheckRead]", "stack_prefix", stack:sub(1, 600))
  end
end
```

READ — Compare the logged local definition/call lines: tail_wrapper should be absent, post_wrapper present. Equal/empty/unexpected traces leave the engine claim unsettled. This probes GetStack directly, **not** the C error printer. Leave the passive handler for an owner-selected existing repro; no event means no measurement of delivery. Its output establishes exact argument types and relative log order; it cannot rewrite the original box. A later attended existing error through a known tail wrapper is still required to establish actual error-attribution behavior.

### R5. Substring semantics and remaining UI/cost observations

```lua
do
  local f = type(string) == "table" and string.find_lower
  if type(f) == "function" then
    for _, pair in ipairs({
      {"AaB", "ab"}, {"axb", "a.b"}, {"a.b", "a.b"}, {"x[y", "["}
    }) do
      local ok, result = pcall(f, pair[1], pair[2])
      print("[CodexSelfcheckRead]", "find_lower", pair[1], pair[2],
            ok, tostring(result))
    end
  end
end
```

READ — Expected plain-search outcomes are 2, nil, 1, 2. A pattern match or throw changes C12's exact interpretation. OS-path conversion for mounted/packed versus unpacked mods, exact final box rendering on consoles, and dump/hash time and memory **over all actual captured targets** remain owed. Do not call a portal or load an old save to answer these. OS-path behavior can be read from the passive handler's next natural error plus the owner-provided configuration; no artificial blame event is necessary. Performance requires the eventual parser/pin collector in the owner-run pilot; no actual implementation exists to time yet. F-10's suspended-request `GetTargetAmount` behavior is separately unmeasured and is not cleared by any of these metadata probes.

## What you did NOT check — by name

READ — These are omissions, not passes:

- `Mars.exe` and `MarsDebug.exe` were never launched. No game VM dump, C ChecksumRemove implementation, C GetStack/error-printer implementation, C IsValid behavior, C request GetTargetAmount implementation, or actual F-10 suspended-request control was executed.
- Original reporter attachments `Mars.exe-20260823-22.05.52-6a22b86d.log` and `Mars.exe-20260824-00.01.27-6a22b86d.log` were not supplied/opened as raw files. Their quoted excerpts in `bugs/F104.md` and `bugs/F105.md` were used. No live GitHub issue/comments, Steam page, Paradox page, or current store rendering was fetched.
- `docs/agent/bugs/F111.md`, `F112.md`, `F116.md`, `docs/agent/reports/VANILLA_FIX_QA.md`, `docs/agent/reports/F105_INVESTIGATION.md`, and `docs/agent/reports/FIELD_REPORT_REPLIES.md` were not opened for a new adjudication. Their verdicts are not independently endorsed here.
- Deleted `Fix_FirstAsteroidPrefabs.lua` and `Fix_AstrogeologistExtractors.lua` implementations were not recovered from Git. For F-5 I independently evaluated both shipped profile files and checked the re-verification's described failure, not the deleted patch's entire behavior.
- `C:/Dev/SMR-BugFixPack-TestKit/Code/00_TestCore.lua`, `10_Probes_Wave1.lua`, `40_Probes_Wave4.lua`, and the remainder of that Test Kit tree were not opened directly. Doccheck's own Test Kit parse/count/dirty-state reads are gate output, not my review of those files. The opt-in pack's implementation and Passage Network's shipped mod implementation were not opened.
- All 44 module chunks were opened by the compiler/recording census. **That is not a complete source review of all their paths.** Outside the ten challenge targets, the two real failure controls, and the explicitly cited install/dependency reads, I did not audit full probe contracts for `90_SaveSanitizer`, `ArrivalDeaths`, `BombardmentSpread`, `BrokenTrackSalvage`, `CrystalMysteryHang`, `DomeOverviewHighlight`, `DustSicknessBiorobots`, `ExoticDepositSign`, `ExtenderFlapChurn`, `FounderTraitNotification`, `GeneForging`, `GraphConsumedCaption`, `JumboCaveReinforcementWedge`, `LakeEntombment`, `LayoutTechLock`, `NightShiftWork`, `PayloadTemplateRefill`, `RocketDroneChurn`, `RocketInteractGuard`, `SaintBlessing`, `SequenceLatents`, `ShelterReflex`, `ShuttleHubOffAvailable`, `ShuttleTransportCache`, `SinkholeIndestructible`, `TrackConnectorPingPong`, `TrackSalvageRefund`, `TrackSalvageWipe`, `TrackTunnelPowerBridge`, `TrainsToVoid`, and `VacuumWalks`. In particular, compiler traversal does not certify thread/RNG/Msg safety.
- `S/CommonLua/SavegameFixup.lua`, the whole `S/Lua/_fixup.lua` migration chain, save serialization/uninstall paths, all DLC overrides, and other platform binaries were not independently traced. No claim is made that a single Windows dump pin works on every platform.
- The full 13/8/23 probe taxonomy and “30 hazardous modules” were not recertified. Handler/data counts use the audit's module-level convention and exclude the shared scaffold's registrations; they are not a count of live engine handlers.
- The broader repository reports, bug/fact indexes and archived session narratives were not taken as a body of passed evidence. Named citations above delimit what was opened or searched; no general “the rest passed” inference is intended.

## For the owner

READ — **Commission the capability pilot and a bounded installation prototype before a pack-wide rollout.** The strongest practical route I found is declared target/callee/data checks followed by all-before-write installation, with arity included and UNKNOWN declining the affected behavior. Start with LandscapeUnitFilter, TrainCargoDumping and StaleReservations' cancellation dependency. This improves the mechanism without using the game revision as a gate. My report does not supply or authorize new production code.

READ — **Correct the audit's load-bearing claims before routing its implementation brief.** In particular, remove “F-2 is impossible to detect,” “no old probe could see F114,” “at most 17 bytecode false stand-downs,” and the act1 quit attribution. Keep the source and bytecode measurements separately labeled. A source read does not move a bug or test status; the seven FIX/KEEP labels here are the re-verification's classifications, not newly adjudicated outcomes.

READ — **Keep mismatch/UNKNOWN fail-closed if the intended claim remains unconditional.** Quorum and revision can explain uncertainty, but cannot turn it into compatibility. That choice re-exposes players to some original bugs while a fix is off, so show which named modules lost protection and prioritize loss-prevention repairs. Do not strengthen wording when only arity lands. The current proposal cannot establish the full “what it was written for” guarantee, and even “the code it patches” requires implementation coverage, phase handling and the promised refusal semantics.

READ — **Use a bounded diagnostic breadcrumb; leave the engine's reporting intact.** Say where the error was raised and whether a pack frame appears, not who caused it. A downstream vanilla location does not acquit us, and a pack location does not always establish the root cause. Keep all errors raised/logged; do not pre-seed ReportedMods, disable reporting, swallow errors, conceal chunk ownership or tell players to reorder mods. Changing the actual console-visible box remains your separate policy decision; I recommend the log improvement first.

READ — **Treat LuaCodeToTuple as a capability finding to verify, not an invitation to build on hidden authority.** R2 can settle the omitted route with scalar results. If confirmed, it changes the audit's technical feasibility analysis, but a stable direct-dumper contract is still preferable for production. A diagnostic-only LuaRevision label is useful if worded as a recording/revision label; clarify that narrow non-gate use explicitly so it cannot later become a compatibility waiver.

## Gates

MEASURED — `python -B tools/doccheck.py` completed with:

```text
STATE + STUBS: STATE.md 9211 bytes (warn 9216, hard 18432, line 200); 3 stubs present and pointing
doccheck: GREEN
```

MEASURED — The 18 frozen-index warnings were pre-existing. The first count run reported 100 Test Kit probes and one unrelated Test Kit modification; the pre-creation gate reported 98 probes and the post-creation gate 96, both with `TESTKIT TREE: clean`, reflecting concurrent work outside this report. Code remained 45 files / 44 modules. No unrelated changes were staged or committed by this work. The report is UTF-8 without BOM with LF endings. The published Python reproduction blocks were rerun successfully; all six Lua snippets compiled under stock Lua 5.3. The final doccheck and report whitespace check passed after report creation, before the explicit-path commit.
