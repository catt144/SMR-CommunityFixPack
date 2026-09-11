# FR-1 cache route — 2026-09-11

**Current verdict: v1's replacement was consumed; v2 covers all 18 indexed RAYS
records and is ready for the laptop bench, not yet a verified fix.** See
[§8](#8--round-2-all-rays-coverage-and-normal-loading) for the correction,
evidence and v2 artifact. The text before §8 is the retained round-1 snapshot:
its six-record coverage and untested-consumption statements are superseded.

**Verdict: BETTER-ROUTE-FOUND; feasible to bench, not a verified fix.**
Use the shipped `DlcMountFolder` helper to layer six replacement records over
`ShaderCache`, then request one reload. The fake-DLC helper **unmounts the base
cache first**; a partial pack through that helper cannot assume base-file fallback.
The directory route preserves the base index and other records and reports mount
failure. Its actual precedence and native cache consumption remain **NEVER RUN**.

**MEASURED:** all 6,453 numeric cache records now parse to EOF; the two other
files are indexes. A stored FLPK writer reconstructs the complete stock directory
byte for byte. An empty 8×8 compute shader retains the original root signature,
passes DXIL validation, and is inserted into all six RAYS records with their
metadata unchanged. The disposable probe passes 27 mocked-Lua cases.

**NEVER RUN:** game mount, replacement pipeline creation on NVIDIA 580, world
load and visual checks. The owner bench is [checklist 145](../../PLAYTEST_CHECKLIST.md).
No game/editor launch, shipping-code change, persistent-config write or public post
was made. The owner's ranking remains pure mod → persistent config → launch option;
this investigation develops the mod-carried cache intervention, without deciding
whether it belongs in the fix pack.

## Evidence keys and boundaries

- **G:** `C:\Dev\SMR-SrcArchive\1.1.0.403908\Src\`. Every G citation below names
  this version; line numbers are from the read-only archived tree.
- **S:** shader sources at `C:\Dev\SMR-FR1-Evidence\shaders-1.1.0-extracted\`;
  decoded cache at `C:\Dev\SMR-FR1-Options-2026-09-10\shadercache-extracted\`.
  Original pack: `A:\SteamLibrary\steamapps\common\Project Spark\Packs\ShaderCached3d12.fpk`.
- **B:** `C:\Dev\fr1-mm-complete\fr1-mm\`, owner A/B/D/E dumps and Proton logs.
  Reclassified read-only this session; no new gameplay measurement.
- **D:** `C:\Dev\SMR-FR1-CacheRoute-2026-09-10\` (scratch retains its start date).
  Tools, disassembly, compiler argv/output, record manifests, harness and zip.
  Prior compiler/tools: `C:\Dev\SMR-FR1-Options-2026-09-10\`.
- **MEASURED native bytes:** installed `Mars.exe`, SHA256
  `28599c4acf318b0354969fe7e537fbcea6251e14616368a0274b7ff492293c6f`.
  Addresses below are preferred-image virtual addresses, base `0x140000000`;
  no native game code was executed. Disassembly is evidence, proposed function
  purposes are separately marked inferences.
- **MEASURED receipt:** [desk JSON](../../archive/fr1-cache-route-desk-2026-09-11.json).
  Orientation HEAD was `f4e5409`; earlier findings §8–§9 and the current brief were
  checked against that tree. Original archives/evidence were not modified.

## 1. Record format and lookup

**1.1 — MEASURED:** `D/cache_records.py` parses every numeric S record using this
layout. `corpus-parsed.json` records offsets, sizes and SHA256s. The same parser
accepts the six replacements with exactly their original metadata.

| grade | part | decoded structure |
|---|---|---|
| MEASURED | stream header | eight bytes `72 70 68 73 18 00 01 00`; native reader requires version 24 |
| MEASURED | types | u32 count; each has u16 id, interned name, u16 base field, u32 count/stride, counted members, u32 size |
| MEASURED | type members | u16 type field, u32 byte offset, interned name |
| MEASURED | interned strings | tag 0 empty; tag 1 + u32 previous index; tag 2 + u32 length + UTF-8 bytes; one record-local pool |
| MEASURED | resources | u32 count; each has interned name and five u16 fields |
| MEASURED | parameters | counted `(u32,u32)` pairs, then counted `(u32,u32,u32)` triples |
| MEASURED | layout and pass map | length-prefixed layout bytes; counted length-prefixed pass names with u64 values |
| MEASURED | shader slots | exactly six length-prefixed byte blobs; empty slots have length zero; EOF follows slot six |

**MEASURED:** 6,225 records contain vertex + pixel DXBC (DXIL stage ids 1,0);
228 contain compute DXBC (stage id 5) in slot 5, counting from zero. There is no
unparsed record trailer or separate checksum field in this decoded grammar.
That does **not** establish that an upper native layer never verifies content
against its filename. Scalar/base-field semantics and all parameter enums have
not been named; the replacement preserves them instead of reconstructing them.

**MEASURED:** all six RAYS records contain 42 types ending at byte 8,102. Their
resource lists differ with defines. The decoded bindings include Frame/Scene/Main
CBVs, samplers, textures and reflection outputs. The queue's `TileCounter` is
not listed there although the original DXIL uses it: this table is not a complete
enumeration of every DXIL binding. Compute parameter pairs are `145→8`, `146→8`,
`147→1`, `149→0`; dimensions agree with the shader, but assigning semantics to the
last enum remains unproved. Native serializer/reader: `0x14089da40` / `0x14089d6d0`,
type-table reader `0x14089dea0`, six-slot reader loop `0x14089da00`.

| grade | RAYS variant | record key | DXBC offset | original DXBC bytes |
|---|---|---|---|---|
| MEASURED | default | 14281071190732923386 | 8549 | 16584 |
| MEASURED | importance | 6121468085666728083 | 8574 | 19600 |
| MEASURED | hyperbolic | 3532759928818375094 | 8543 | 16628 |
| MEASURED | hyperbolic + importance | 12556516658419309610 | 8568 | 19644 |
| MEASURED | HiZ | 14433279818421691317 | 8522 | 17420 |
| MEASURED | HiZ + importance | 7464541473171016648 | 8547 | 20772 |

**1.2 — MEASURED:** `index.bin` is 1,269,962 bytes, header `XDIS 02 00 01 00`.
Tag 1 stores a u64 binary key; tag 2 stores a u32-length string and u64 key;
tag 3 stores a source filename and u64 hash; tag 4 terminates the stream.
There are 6,453 tag-1, 7,177 tag-2 and 288 tag-3 entries. Re-encoding is byte
identical to the binary; rendering references produces `index.txt` byte for byte.
`[b]` counts in the text are derived reference counts, not fields beside tag 1.
`[k]Reflections.fx|REFLECT_RAYS` maps to the default key; debug aliases and some
define combinations share records. Native code opens `ShaderCache/index.bin`
at `0x1408898ef` and checks index version 2 at `0x1408899a7`.

**INFERRED:** retain the original complete index and filenames to change the
payload behind existing lookups. A partial replacement index risks excluding
unrelated programs. `index.txt` looks like a diagnostic rendering; its necessity
was not tested. The directory probe supplies neither index, so both remain
available from the base mount.

**1.3 — MEASURED / unresolved:** keys are not vkd3d shader hashes. Across all
six records, 72 comparisons of FNV-1a64, seed-zero xxHash64 and xxHash3-64 over
whole records, post-header bodies, metadata and DXBC produced no key match
(`key-hash-candidates.json`). This rejects those exact recipes only. Native key
derivation and any upper-layer content verification remain unknown. **Falsifier
for the unchanged-key substitution:** a mounted replacement is rejected or the
original shader still reaches the driver; the runtime witness is owed.

## 2. FLPK writing and the partial-pack catch

**2.1 — MEASURED:** the stock pack is 140,187,936 bytes. Header words after `FLPK`
are `32,1,32,0,228555,228555,4`. Its flat directory is a balanced binary search
tree in preorder, ordered by filename. Each entry stores file offset, packed
flags/name length, stored size, name bytes, then **left-subtree byte length**.
That last word is not reserved zero: stock values include 35,36,70,72 and much
larger subtree sizes. `D/flpk_write.py` reconstructs all 228,555 directory bytes
exactly, including all 6,455 entries and subtree offsets.

**MEASURED:** the writer emits a six-record stored (`0x10`) FLPK, 61,676 bytes,
and the independently existing `tools/flpk_extract.py` extracts byte-identical
payloads. The writer supports flat ASCII files only. The public
[nickelc/hpk implementation](https://github.com/nickelc/hpk/blob/master/src/hpk/mod.rs)
uses the older `BPUL` header and is not this FLPK writer.
**NEVER RUN:** engine mounting of our emitted FLPK; extraction alone is not a
native compatibility verdict. The pack is a desk artifact, excluded from the mod zip.

**2.2 — SOURCE:** G/CommonLua/Dlc.lua:406–414 calls `UnmountByPath("ShaderCache")`
**before** mounting a newer DLC cache with `seethrough,in_mem,priority:high`.
`MountPack`'s return is ignored and the reload flag is set regardless. Therefore
flag readback cannot certify mount success. `seethrough` means continue searching
lower-priority mounts (G/CommonLua/LuaExportedDocs/Global/AsyncOp.lua:53–60);
it cannot restore a mount already removed.

**INFERRED:** using that helper for only six records needs an additional base
mount or a complete replacement cache including the full index. Retained native
objects might mask missing files, but that is not a dependable overlay contract.
**Falsifier:** a controlled native mount/lookup trace proving the old base remains
reachable despite this unmount. No such trace was run.

## 3. The mod route and timing

**3.1 — SOURCE:** G/CommonLua/Dlc.lua:379–385 takes `{folder=...}`, checks
`io.exists(folder .. "/" .. requested_folder)`, calls
`MountFolder(requested_folder,path,"seethrough")`, and returns `not err`.
It performs no unmount. It is absent from the examined mod blacklist, while direct
MountFolder/MountPack and AsyncFileToString are blocked
(G/CommonLua/Modding/Mod.lua:1347,1366–1367,1559–1595).

**SOURCE:** mod content is mounted before code runs. `CurrentModPath` is the
virtual `content_path` (:1630), not necessarily an OS folder. Both unpacked
folder mounts and packed ModContent.fpk mounts feed that namespace (:866–883,
1733–1771). The packed-material path itself calls MountFolder on content inside
the mounted mod pack (:881–883): an existing analogy for a directory overlay
from packed virtual content, without nesting another pack.

**INFERRED route, NEVER RUN natively:** the probe calls the helper with
`CurrentModPath .. "Noop"` or `.. "Control"` and folder `ShaderCache`, then sets
ForceShaderCacheReload once. The base cache/index remain mounted. Equal-priority
ordering, a possibly higher-priority base mount, native in-memory retention, and
record validation can still defeat it. The initial package is **unpacked only**.
Nested FLPK acceptance via fake-DLC and packed-mod runtime behavior remain open.

**3.2 — MEASURED B:** reclassification finds A/B faulting on thread 013c after
`38121decbc3eee12.spv`; D on 013c and E on 0140 after `271ec9634b1ab87b.spv`.
Each preceding SPIR-V dump is 1 ms before that thread's access violation. Counts:
A/B 115 DXIL files, D 119, E 123. D/E establish immediate boot-time rebuild after
the flag, despite G/CommonLua/Dlc.lua:412's next-map comment. They do **not** establish
that a newly mounted replacement will be consumed. API `d3d12` was measured by
the existing probe. A's before-LoadBinAssets SSR value was zero.

**SOURCE:** InitRenderEngine precedes ModsLoadCode
(G/CommonLua/Core/autorun.lua:332–341,434). **INFERRED:** mount before requesting
the reload, at mod-code load, with no wait until ChangingMap. The instrument
does that synchronously and never re-arms in its diagnostic hooks.

**MEASURED desk:** 27/27 harness cases use the actual shipped DlcMountFolder body,
blacklisted direct APIs, a mod namespace that rejects unknown globals, and the
game's double-stage ModLog/ModPrint formatting behavior. Percent strings, missing
helpers, failed/throwing mounts, wrong adapter/API/revision, SSR On, existing
reload, duplicate/bad markers and wrapper argument/return preservation are covered.
All three Lua files parse with Lua through lupa. Mock VFS success proves no native
precedence. After a successful mount followed by a setter failure, the mount remains
until process exit; the probe logs that limitation and requests no further reload.

## 4. Replacement choices and validation

**4.1 — MEASURED:** all six original RAYS RTS0 chunks are the same 536 bytes,
SHA256 `3ff5c9b85551833d481d786ea535d6135089532ddee3f53e3a3f09a8a2aa44f3`.
The game-matched compiler builds `void ComputeShaderMain(){}` with
`[numthreads(8,8,1)]`, cs_6_6, HLSL 2021 and row-major layout. We compile with
validation enabled, extract the original root signature, attach it using DXC,
verify root compatibility, and run Microsoft's `dxv`: both verification and
validation succeed. Full commands/output: `D/payload-commands.json`.

**MEASURED:** final container size 1,688 bytes; DXIL payload SHA256
`516fc3836f468850495bceefbc0d9417f5dceae6ec106f9e72ca299e27e2bac9`.
Its only executable instruction is `ret void`. Every original prefix up to the
slot-5 length is preserved; length and complete DXBC are replaced. Fresh DXC
HASH/container checksum fields travel with the new shader; the old HASH is not
copied. Root ABI is identical, while PSV0 correctly declares **no resource use**.
This is not a shader that still reads/writes the original bindings.

**SOURCE:** Microsoft's [DXIL specification](https://github.com/microsoft/DirectXShaderCompiler/blob/main/docs/DXIL.rst)
describes the container/validation contract; [root-signature documentation](https://learn.microsoft.com/en-us/windows/win32/direct3d12/specifying-root-signatures-in-hlsl)
describes binding layout. Local pinned vkd3d-proton
`0bd10357df3f6b65e0a7c4d272acdd6c46249ff8`, `libs/vkd3d-shader/dxbc.c:98–145`,
checks container structure but explicitly ignores its DXBC checksum at :124.
That does not license carrying stale hashes or establish native D3D12 acceptance.
**NEVER RUN:** PSO creation by the game, translation of this payload by the owner's
vkd3d, or its compilation by NVIDIA 580. DXIL validation does not test NVVM.

**4.2 — SOURCE / INFERRED:** substituting FULL tile-8 bytecode is not a safe
semantic replacement just because the thread size matches. S/Reflections.fx:440–513
uses a queue/TileCounter so a worker group can process many tiles; :515–529 uses
dispatch-thread coordinates directly. A RAYS worker-grid dispatch need not cover
the image for FULL. It could leave much of the output unwritten. All twelve
distinct FULL tile-8/tile-16 records were compared (`D/full-comparison.json`);
their presence is not dispatch equivalence. No FULL transplant is packaged.

**NEVER RUN:** a queue-loop restructure that preserves rendering, or a GLSL
round-trip for all six current variants. These remain alternatives if an Off-only
no-op proves too restrictive. A shader from another pass has the same binding,
output and dispatch obligations; no interchangeable donor was established.

## 5. Does Reflections Off skip dispatch?

**5.1 — MEASURED native bytes:** the `hr.EnableScreenSpaceReflections` constructor
at `0x140027340` names the object at `0x1411c8a48` and initializes its value at
`0x1411c8a68`. In routine `0x14070fbb0`, old resource handles are released/cleared;
the value is compared against zero at `0x14070fe20`, with a zero branch to the
epilogue at `0x140710214`. The subsequent resource-creation section is skipped.
Separately, `0x14070f7b0` iterates shader-selection values and calls the loader at
`0x14070f8f6`; its examined body does not read that main SSR variable.

**INFERRED:** Off disables reflection resources while pipeline preparation remains
separate. This fits B's measured Off crash. It supports an Off-only no-op experiment;
it is not a proof that every dispatch caller is gated. The complete dispatch graph,
indirect references and screen output were not established. **NEVER RUN:** a frame
capture confirming no RAYS dispatch while Off. If dispatch still occurs, the no-op
leaves outputs unchanged/unwritten; stale or undefined reflections are possible.
Do not claim no visible cost, and do not turn Reflections On during this bench.

## 6. Blast radius and the actual gate

**SOURCE / INFERRED:** the Windows executable under Proton cannot be identified
with Platform.linux (EF-089). No reliable exclusive Wine or driver-580 detector was
established. The honest boundary is a deliberate owner marker and an Off-only test.

**MEASURED desk:** the instrument requires PC, `d3d12`, NVIDIA vendor 4318,
LuaRevision 403908, AssetsRevision 33006, SSR zero, reload Boolean false, and
the required APIs. These revision checks pin this disposable binary artifact's
ABI; they are not proposed shipping fix guards under FIX_POLICY §2a. It refuses
AMD/Intel, other APIs/builds and malformed/duplicate markers. With no marker it
logs diagnostics and mounts/writes nothing. It also refuses old `-fr1-options`
treatment markers; the owner disables the old diagnostic mods for isolation.

**INFERRED:** an explicitly armed Windows NVIDIA machine meets the same gates and
would receive the same replacement. The no-op does no GPU writes, but engine
acceptance and visual equivalence remain untested there too. AMD/Intel are untouched
by this instrument; forcing it past that gate would replace any requested RAYS
program regardless of the AMD FullTile preference. No broad compatibility claim.

**NEVER RUN owner legs:** C1 unchanged six-record overlay + reload; N1 no-op
overlay + reload; if N1 loads, R1 full restart without marker. Fresh dump directories,
Proton log saved after each leg, New Game and Reflections Off throughout. The zip's
README and checklist 145 give copyable steps. A positive N1 requires **new no-op
DXIL in the dump plus a loaded world**, followed by the expected original failure
in R1. C1 controls the reload and mount procedure. A mount log alone is not success.

**MEASURED desk:** `D/classify_dump.py` matches DXIL bytes, accepts folders/zips,
and correlates each faulting process/thread with its last dump. It reproduces
A/B/D/E and identifies a no-op control sample with an arbitrary filename. All six
replacement records deliberately contain the same program, so a no-op dump proves
program identity, not which of the six record keys supplied it. Preserve unknown
shader crashes as new evidence; do not label them another RAYS failure.

## 7. Other routes and remaining work

**7.1 — SOURCE:** source overlays are possible in principle through DlcMountFolder,
and developer configuration sets `hr.EnableShaderCompilation=1`
(G/CommonLua/Ged/__config.lua:17). G/CommonLua/Core/luadebugger.lua:478–497 sends
shader compilation requests to an external debugger service and mounts overloads;
it is not evidence of a retail in-process fallback. **NEVER RUN:** deliberately
missing/corrupt records, turning on retail compilation, or overriding
Shaders/Reflections.fx. Compiler DLL presence and an exported variable name do
not establish a functioning retail fallback. None of these destructive-to-the-
lookup experiments is combined with the initial mount test.

**7.2 — INFERRED:** changing rphs parameters to suppress a shader risks invalid
pipeline state; no decoded parameter was established as a registration-disable
switch. Changing index mappings or using a donor shader also requires the contract
checks in §4. The exact-root no-op is the smallest constructed payload with a
clear byte witness; it is still a workaround for a driver/compiler failure.

**7.3 — MEASURED correction to the brief:** only **two** distinct RAYS programs
were observed faulting, default and hyperbolic+importance. A family-wide compiler
problem is an inference; all six being independently measured crashing is false.
Covering six keys avoids simply exposing an untested variant after the first fix.
Likewise D/E prove immediate rebuild scheduling, not replacement mount consumption.

## Not opened / not established

- Native filename-key derivation, upper-layer hash verification and the complete
  cache invalidation/lookup graph. The 72 rejected hash recipes are not exhaustive.
- Native FLPK mount of the generated pack; packed-mod and nested-pack bench;
  the directory overlay's priority relative to the actual base cache mount.
- Full RAYS dispatch call graph, frame capture, no-op NVVM compilation and visible
  behavior on Linux 580, Windows NVIDIA, AMD or Intel.
- Retail HLSL fallback after a missing/invalid record; AddRemotelyCompiledShader's
  retail reach; shader queue rewrite and launch-option interventions.
- Shipping scope/policy exception. This remains the owner's checklist 145 decision.

## Delivered artifacts

**MEASURED desk:** `D/fr1-cache-probe-v1.zip`, 138,670 bytes, Linux-safe zip paths,
SHA256 `7b44ac6e36ab9b8d4ba364eee5ecdc29d1f1fadbca8dc9de8da2af06b8b297d4`.
It contains `FR1CacheProbe/`: code, metadata/items, both six-record folders, README
and standalone classifier/hash identities. Zip CRC and every extracted member's
SHA256 were checked against the staged files. The partial FLPK is excluded.

**MEASURED desk:** scripts and receipts remain in D; `cache-route-desk-tools.zip`
preserves the tools without game executables. The committed receipt stores compiler
output, record hashes, format checks, harness results and bench reclassification.
STATE was 12,248 bytes against its 12,288-byte warning threshold, so the permitted
optional NEXT addition would not fit and was omitted. The existing holds stay intact.

## 8 · Round 2: all RAYS coverage and normal loading

**Verdict — MEASURED / NEVER RUN:** the owner proved that the directory overlay
can supply our replacement to the game. V1 then exposed a debug RAYS program
that I had omitted. V2 covers all 18 RAYS records, with a separate treatment that
does not request a reload. All desk checks pass; v2 gameplay, world-load success
and visual equivalence remain **NEVER RUN**. Owner steps replace v1 in
[checklist 145](../../PLAYTEST_CHECKLIST.md).

Additional evidence keys: **B2** is `C:\Dev\fr1-cache\fr1-cache\`, read-only
owner C1/N1 evidence; **D2** is `C:\Dev\SMR-FR1-CacheRoute-V2-2026-09-11\`,
external build, classifier, full compute disassembly and validation receipts.
The committed evidence is
[`fr1-cache-route-v2-desk-2026-09-11.json`](../../archive/fr1-cache-route-v2-desk-2026-09-11.json).
G and S retain the exact version and paths defined above.

### 8.1 · Coverage correction and replacement validation

**MEASURED:** independently filtering the binary index and the text index by
the exact `Reflections.fx` and `REFLECT_RAYS` tokens produces the same 18 keys.
The full Reflections set contains 54 records: 18 RAYS and 36 FULL. V1's manually
selected six were only the non-debug RAYS subset; my earlier claim that they
covered all RAYS was wrong. The missing 12 are debug builds, including N1's
`5519638363063710019`. V2 derives coverage from the index rather than a key list.

**MEASURED:** all 18 RAYS roots are byte-identical, 536 bytes, SHA256
`3ff5c9b85551833d481d786ea535d6135089532ddee3f53e3a3f09a8a2aa44f3`;
all declare 8×8×1 threads. Original PSV0 sizes differ (356, 380, 404, 428, 452
and 476 bytes), so matching only one debug program's root was insufficient.
Each replacement preserves that record's metadata prefix, replacing only its
compute-slot length and DXBC. Each actual replacement was validated by `dxv`
and checked against its root by game-matched `dxc`: **36 successful checks**.
The 1,688-byte no-op DXBC retains DXIL SHA256
`516fc3836f468850495bceefbc0d9417f5dceae6ec106f9e72ca299e27e2bac9`.

**MEASURED:** a separate ZIP audit uses the text index as its oracle and checks
the exact file set and bytes of both folders. V2 passes with 18 original Control
and 18 replacement Noop records. The real v1 ZIP is the negative control: it
fails with exactly the 12 missing keys, including N1's crasher. All three Lua
files parse; the game-shaped harness passes **35/35 cases**, using the actual
G `DlcMountFolder` body, ModEnv restrictions and ModLog formatting behavior.

**MEASURED owner evidence, reclassified:** C1's 123 DXIL dumps include 23
identified cached compute programs. Thread `013c` last dumps
`271ec9634b1ab87b.spv` at 19222.239, 1 ms before its fault: original
hyperbolic+importance RAYS, key `12556516658419309610`.
N1 has 260 DXIL dumps and 31 identified compute programs, including our no-op
in `4f866e2c54fc9064.dxil`. Its thread `0140` last dumps
`a26e0bbfe7751fbf.spv` at 19285.776, again 1 ms before the fault: debug RAYS
key `5519638363063710019`, DXIL SHA256
`9aca6902d7e5f825828bf90a7145cbe04e8b553f0ec4c0826b567fc9ff2bc069`.
Its aliases include `USE_HYPERBOLIC_DEPTH|REFLECTION_DEBUG|REFLECTION_ITERATIONS|REFLECT_RAYS`
with and without `TRACE_HIZ`. The logs contain the armed, successful-mount and
reload witnesses. Repeated trace/print copies of those messages do not establish
multiple reload requests.

**MEASURED / INHERITED:** the N1 no-op bytes prove replacement consumption on
this unpacked probe setup. N1 also dumps FULL tile 16 (`c2aacc1919769303`, key
`10965947805870513868`); no FULL fault was observed. A dump is not an independently
instrumented successful pipeline return. The owner's pre-menu screen/hang result
is inherited from FINDINGS §10: `N1/N1-result.txt` was not present in B2 when
re-read. Three distinct original RAYS programs have now been attributed to faults;
18 independently crashing programs have not been measured.

### 8.2 · Looking past Reflections.fx

**MEASURED desk:** disassembled all 228 cached compute programs with the
game-matched DXC. A control-flow scan finds cycles in 149. Exactly 18 have both
barrier and atomic calls inside the **same strongly connected cyclic region**;
that set equals the entire indexed RAYS set. Each has eight barrier calls and
four atomic operations in such regions (static instructions, not execution
counts). Three synthetic controls check that an out-of-loop barrier, and barriers
and atomics in separate cycles, cannot create a false match. All pass.

**SOURCE:** S `Reflections.fx:440–513` contains the shared queue, synchronization
and atomic tile counter; `:515–529` is the FULL path. Other large compiled cycles
provide a watch list, not evidence of additional defective programs:

| Program | Compiled structure and evidence |
| --- | --- |
| VolumetricLighting INTEGRATE / INTEGRATE_INJECTION | **MEASURED:** largest cyclic region 68 blocks each; no barrier or atomic inside a cycle. |
| VolumetricShadows EXTINCTION_VOLUMES | **MEASURED:** largest cycle 20 blocks; no barrier or atomic inside a cycle. |
| TerrainSplatMask PASS_DEFER | **MEASURED:** largest cycle 13 blocks; four cyclic atomic operations, no cyclic barrier. |
| AtmosphereMultipleScattering | **MEASURED:** largest cycle 11 blocks; neither operation inside a cycle; present in N1 dumps. |
| AutoExposure PASS_BUILD_LUMINANCE_HISTOGRAM | **MEASURED:** largest cycle nine blocks; two cyclic atomics, no cyclic barrier; present in N1 dumps. |
| SinglePassDownsample variants | **MEASURED:** cyclic barriers without cyclic atomics; several present in N1 dumps. |

**SOURCE, upstream:** [vkd3d-proton #2701](https://github.com/HansKristian-Work/vkd3d-proton/issues/2701)
reports the older NVIDIA 580 failure, valid SPIR-V and successful RADV/NVK
replay. Its [workaround comment](https://github.com/HansKristian-Work/vkd3d-proton/issues/2701#issuecomment-3541285729)
links a pyroveil GLSL round trip; the [following comment](https://github.com/HansKristian-Work/vkd3d-proton/issues/2701#issuecomment-3541297064)
says it was reported to NVIDIA. The two published comments provide no exact
bad opcode, loop shape or NVIDIA fix identifier. The older report's quality
setting boundary is not the owner's current 1.1.0 Off behavior.
The pinned [hack configuration](https://github.com/HansKristian-Work/pyroveil/blob/e1f547372cf1b9d14da56621716d2137088d0061/hacks/surviving-mars-relaunched-nv-580-stable/pyroveil.json)
selects an old shader hash, requests the round trip and disables
`VK_NV_raw_access_chains`; its [compiler](https://github.com/HansKristian-Work/pyroveil/blob/e1f547372cf1b9d14da56621716d2137088d0061/compiler/compiler.cpp)
uses shaderc optimization level zero. These change several inputs, so their
success does not isolate a queue-loop mechanism.

**INFERRED:** the structural signature supports replacing all RAYS before the
next bench. It cannot predict every NVIDIA compiler failure: DXIL is upstream
of SPIR-V lowering and the closed compiler. A fault attributed to another family
would falsify the working completeness hypothesis. To identify that immediately,
the packaged classifier now recognizes all 228 cached compute records plus the
no-op by DXIL bytes. A sample ZIP with arbitrary filenames correctly identifies
both the no-op and the newly observed debug crasher.

### 8.3 · Separate normal-loading treatment

**SOURCE / MEASURED desk:** render initialization precedes mod code, but that
alone does not tell us when native code reads each cache record. The new
`-fr1-cache=noop-noreload` branch mounts all 18 replacements and returns without
calling the engine setter. Its witness is `NO_RELOAD_REQUESTED`, with
`reload=false`. It declines an already-set reload flag to avoid a confounded leg;
the harness also proves this branch works when the setter is unavailable.

**INFERRED route / NEVER RUN game:** try Q2 after the unchanged-shader C2
control. Q2 reaching the menu is expected even if the treatment did nothing;
the useful result is New Game loading with replacement consumption evidence.
If Q2 succeeds, skip the forced F2 rebuild. If normal loading retains an original
program already in memory, Q2 may reproduce the original world-load crash;
F2 then tests coverage with the previously demonstrated forced route. A missing
dump can also reflect cache reuse, so the full evidence matters.

### 8.4 · Marker ergonomics and first-screen witness

**MEASURED desk:** the accepted strings are exactly `-fr1-cache=control`,
`-fr1-cache=noop` and `-fr1-cache=noop-noreload`. A typo emits `MARKER ERROR`,
the received marker and all three accepted forms. The harness covers the owner's
dash form, double leading dash, spaces, case, underscore and duplicate markers;
all refuse treatment. Missing markers log `UNARMED` and the accepted strings.
V2 logs also identify the version, mode, reload choice and 18-record coverage.

**INFERRED / NEVER RUN v2:** C2 should reproduce the boot-slides crash, before
the menu. Reaching the menu is a reason to stop that control and examine its log
for marker/gate/setup drift, not evidence of a valid control or proof of one
specific typo. Checklist 145 and the ZIP README supply whole copy-paste launch
lines, per-leg expected results and log-preservation commands.

### 8.5 · Better route and scope

**INFERRED route:** prefer Q2's normal loading if the bench proves it consumes
the replacement; this avoids deliberately rebuilding unrelated/debug pipelines.
Forced F2 remains a fallback whose mount/reload mechanism is already observed.
No persistent-config step is required by either probe mode. This moves the
owner's first-choice mod route forward without claiming that a shipping mod is
approved or that an engine cache replacement meets the pack's Lua-fix policy.

**MEASURED implementation / INFERRED scope:** all 36 FULL records and every
other shader remain untouched. No measured fault requires replacing them, and
preemptive no-ops could suppress unrelated rendering. Generic loop complexity
does not justify expanding the treatment. A resource-preserving queue rewrite
or a SPIR-V round trip might retain reflections, but neither has been built or
bench-validated here. Keep Reflections Off throughout this disposable test.

### Not opened / not established in round 2

- **NEVER RUN:** any v2 game launch, Q2 normal-path consumption, F2 full-coverage
  success, loaded-world visuals, or R2 reversal; packed-mod behavior.
- **UNRESOLVED:** native preload/lookup/invalidation graph and whether Q2's
  overlay can supersede an already-loaded original without forcing reload.
- **UNRESOLVED:** exact NVIDIA NVVM defect; no native replay or compiler safety
  verdict across the 228 programs. The cyclic-region scan is a triage heuristic.
- **UNRESOLVED:** complete Off dispatch graph, persistence effects of the game's
  own normal caches, automatic driver/Proton gate and shipping scope (owner ck145).

### Round-2 delivered artifacts

**MEASURED desk:** `D2/fr1-cache-probe-v2.zip`, **403,169 bytes**, SHA256
`3a67dcd6721814d1d3cdf523f19ef76ff91d3f519b01a463e6da72d6f50ea6d4`.
The authoritative hash is also recorded in the committed receipt. It contains
the same `FR1CacheProbe` folder/mod ID, v2 Lua/metadata, both 18-record folders,
owner README and the full-compute classifier. Install by overwriting v1 while
the game is fully closed, never by enabling both versions side by side.
`D2/cache-route-v2-desk-tools.zip` preserves the build/audit/classifier scripts;
the receipt preserves per-record checks, corpus metrics, harness outcomes,
upstream comments and C1/N1 reclassification. V1 artifacts and earlier archive
records remain unchanged. No game/editor launch, shipping-code change or
persistent engine-setting write was made in this session.
