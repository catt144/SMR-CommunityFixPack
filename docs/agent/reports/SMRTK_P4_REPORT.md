# SMRTK 03A P4 — Saves and Kit build

2026-09-13, Codex payload seat Sol/high. Desk evidence only; no game leg,
save/load success, achievement eligibility or UI rendering is claimed.
Coordinator owns commits and metadata. Payload made no commits, removals,
metadata/version edits, pack runtime edits or changes to frozen core/panel.
Mandatory STATE/orientation, chain README, both P4 inboxes, EF-095–099,
skeleton sitting/predictions API and all UI-hook sections were read.

## Numbered claims

1. **Saves built:** `75_SMRTK_Saves.lua` registers Save, Load and explicit
   LOAD_OVERRIDE actions for A/B/C. Buttons queue real-time threads; the real
   callback enters Run inside that thread. Direct UI/game-time invocation,
   SavingGame, another toolkit operation and a live native SavegameRunningThread
   refuse before mutation. Save uses display name SMRTK_A/B/C and stable
   `savename = "SMRTK_<slot>" .. config.SaveGameExt`. Native errors release the
   toolkit lock. **Verified:** smoke cases 2–6, including actual coroutine
   yielding and a new-save race during metadata read. **Stopped:** real native
   round trip belongs to 08. **OWNER-ROUTED:** retain a disposable current-branch
   fixture for the load leg, never a 1.0.7 fixture. **For-07:** Saves tab buttons
   are labelled Save A, Load A, Override load A (and B/C).

2. **Guard/provenance built:** before LoadGame, Savegame.Load mounts the native
   save and a callback calls LoadMetadata, the read helper used by vanilla's
   metadata routes. Missing/corrupt metadata refuses even Override. Missing or
   foreign `smrtk.session` refuses normal Load. Process session is a timestamp,
   precise-tick and two native AsyncRand nonce components, retained in SMRTK
   across map loads rather than a colony GameVar. GatherGameMetadata writes only
   copied scalars: session, actions and last. Here **actions means completed
   toolkit callback attempts before the save**, from T.fires (including
   callbacks that return refusal/error; the in-progress save has not returned).
   **last means the last toolkit ring record**, which can be a lifecycle DISARM
   or auxiliary record with action unavailable. It is not proof of a successful
   preceding mutation. GameMetadataLoaded logs PROVENANCE and the Saves page
   shows the loaded block. **Verified:** smoke cases 3–6; no destructive
   LoadMetadataCallback call. **Pending merge:** coordinator agreed to add
   T.saves.status to the shared strip, sanitized to one line and capped at 48
   characters; full status remains on Saves and in the action result. **For-07:**
   override is explicit triage and logs LOAD_OVERRIDE; it does not skip native
   metadata validation or vanilla compatibility checks.

3. **Honest probe gate built:** RunAll and run-one default-refuse; their buttons
   remain disabled until explicit desktop preflight evidence is provisioned for
   the loaded sitting. T.ProbePreflight(evidence) records PROBE_PREFLIGHT through
   Run. The evidence must carry current session/sitting/LuaRevision, full 40-hex
   desktop pack/TestKit HEADs, checked_at, brief, exact command, stdout, exit,
   hit names and explicitly needed names. Zero hits requires exit=1/empty
   stdout; nonzero hits require exit=0, exact stdout/name agreement and every
   hit explicitly declared needed. A stamp expires on load/new-game/map/change/
   DoneGame, or loaded probe order/build changes. The order check is additional
   expiry detection, never a substitute for the desktop sweep. The Kit page
   prints stamp evidence before enabling runs and colours each live SMRTest.last
   verdict. **Verified:** cases 7–9 and page callback case 16. **Stopped:** the mod
   cannot independently inspect source files or verify desktop HEADs; this API
   accepts an explicit attestation, not a computed cleanliness verdict.
   **For-07:** provision the next loaded sitting after the real desktop sweep;
   no runtime file I/O or stale persisted stamp exists.

4. **Logger controls built:** T.EnsureKitLoggers resolves SMRTest.Log after 90
   loads, registering `logger_<exact name>` actions with menu="arm". Buttons
   light according to native installed state. Arm refuses an already manually
   enabled logger and any active quiet arm; it captures the actual toggle
   function and owns only its installation. Core lifecycle disarm uses the
   captured toggle to restore. **Verified:** cases 10–11 exercise actual
   90_Loggers Meteors implementation, state-copy isolation, manual refusal,
   quiet refusal and SavegameSaved restoration. **For-07:** manually enabled
   loggers remain the operator's responsibility and are not adopted. Probes
   and existing logger bodies retain their native TestKit output; each toolkit
   control itself has one primary SMRTK result.

5. **Console/tail/fingerprint built:** console_open calls only ShowConsole(true)
   on the core's existing ConsoleEnabled=true arm and refuses if it is missing.
   Its result says requested, with console visibility as the attended witness.
   Kit includes cls, a live last-12-ring-record tail, red error-event/error-result
   rows and errors since mark. Fingerprint reads LuaRevision, live loaded
   SMR_CommunityFixPack ModDef version, dynamic active/registered counts from
   public order/fixes, loaded mod ids, save and sol. It never calls printing-only
   ListFixes and labels unavailable/absent reads. **Verified:** cases 12,15–16.
   **Pending merge:** generic core T.after_record[verb](fields), after successful
   Run/Fire primary record and taint check, with guarded callback errors and
   recursion. P4 installs .MARK to dispatch fingerprint, covering ordinary mark
   and P3 screenshot_mark without rewriting either definition. The standalone
   smoke directly tests this callback's screenshot_mark contract; it does not
   pretend the frozen dispatcher invokes the still-pending hook. **For-07:**
   a missing console is STOP; never widen the enable.

6. **Dump/snapshot/watch built:** dump_selected is P2's requested action id and
   returns class/handle/template/valid/pos/hex/dome/workers/shifts/storage/
   modifiers and malfunction/destroyed/demolishing flags. Missing fields are
   explicit; false remains false. World snapshots create detached scalar
   records and retain the latest 20 ids; DIFF compares supplied ids or the
   latest two and reports numeric deltas or before/after values. Buildings and
   colonist status/command counts are current-city/current-map label reads;
   funding/sol and resources are colony reads, disasters use live main-map/
   colony g_* active state plus main-map dust-devil count. Scope, map and sitting
   are included rather than representing a scheduler countdown as a disaster.
   Serialization is bounded to depth 3/80 keys and explicitly marks truncation.
   watch_field dynamically calls P3 TriggerField to create the owned DISARMED
   watch_selected_field; a separate button arms/disarms. It watches the original
   object and never retargets when selection changes. **Verified:** cases 13–14
   use actual P3 trigger code, repeated field change, selection change and
   lifecycle cleanup. **For-07:** configure watch, then arm it; table/function
   fields refuse through P3's scalar prepare. Snapshot is a scoped read, not an
   exhaustive all-map colony inventory.

7. **Authorized extra-file accessor:** exactly seven additive lines in
   `Code/90_Loggers.lua`, directly after local installed declaration:

   ```lua
   -- Read-only toolkit coordination; callers cannot mutate installation state.
   function SMRTest.LoggerState(name)
       if name ~= nil then return not not installed[name] end
       local copy = {}
       for key in pairs(installed) do copy[key] = true end
       return copy
   end
   ```

   **Verified:** independent parse and native logger tests. **Coordinator:** gate/
   commit this separately as the settled inbox requires. P1 quiet can dynamically
   refuse any entry in LoggerState() and toolkit `logger_` arms. No 00_TestCore
   bootstrap edit was made.

## Commands and emitted results

Pack HEAD `e245d8028e9d648f02453b5b4230b52155439bd9`; TestKit HEAD
`965fb0869caca2b84d0782bb5da3d909cbfcb30f` at verification. Shared peers'
pending files were preserved. Initial predictions/report paths supplied by the
dispatch were translated to their actual pack docs/agent/reports locations.

| command | output |
|---|---|
| `tasklist /FI "IMAGENAME eq Mars.exe"` | `INFO: No tasks are running which match the specified criteria.` |
| `python tools/doccheck.py --emit-fingerprint` | installed game build 24995074; 1.1.0 group HOLDS; `doccheck: GREEN` |
| `python docs/agent/reports/SMRTK_P4_SMOKE.py` | three per-file `PARSE ...: 0 errors [Lua 5.5]`; 75/76 NO SYNC, NO BARE PRINT and PROBE TOKEN each 0 lines; 17 named PASS cases; `P4 DESK: 17 falsifiers PASS; fake natives/UI, no save/load or rendering play claim` |
| `python tools/parsecheck.py --dir C:/Dev/SMR-BugFixPack-TestKit/Code --quiet` | `PARSE: 34 file(s) in ..\SMR-BugFixPack-TestKit\Code, 0 error(s) [Lua 5.5]` |
| `rg -n 'NetSyncEvent|LogCheatUsed' ../SMR-BugFixPack-TestKit/Code/75_SMRTK_Saves.lua ../SMR-BugFixPack-TestKit/Code/76_SMRTK_Kit.lua` | 0 lines, exit 1 |
| `rg -n '^\s*print\(' ../SMR-BugFixPack-TestKit/Code/75_SMRTK_Saves.lua ../SMR-BugFixPack-TestKit/Code/76_SMRTK_Kit.lua` | 0 lines, exit 1 |
| `python tools/doccheck.py` | `TEMPORARY SWEEP: 0 hit(s) in Code/ + TestKit Code/`; `doccheck: GREEN` |

Doccheck retained existing entry/marker/skill warnings and reported nine
ALIASCHECK UNKNOWN uses of SMRTest.order/probes/last. Those members exist in
00_TestCore's namespace initializer (lines 19–21); the report-only detector
does not recognize the initializer's table fields. No gate was inferred from
a failed path search, suppressed stderr or a non-existent source path.

Native source routes read at the inherited game build: CommonLua/Savegame.lua
295–318 (unique-name behavior),337–344 (wrapped native operation),789–796
(LoadMetadata),1035–1118 (save/load), CommonLua/SavegameMetadata.lua195–214,
285–305 (destructive load callback/provenance message), Modding/Mod.lua1620
(safe os.time), exported LuaSharedLib.lua18–24 (AsyncRand), Lua/Funding.lua80,
ResourceOverview.lua956–966, Buildings/Building.lua450–460, StorageDepot.lua
544–546, Workplace active/current shift reads, disaster g_* state reads and
CommonLua/X/XCombo.lua31–52 (Items/DefaultValue/OnValueChanged).

## For-07 preflight contract and sitting witnesses

Exact desktop command remains WORKFLOW's command, run from the pack root:

```text
grep -rln "TEMPORARY" Code/ ../SMR-BugFixPack-TestKit/Code/
```

07 should compile the captured evidence into the sitting-owned AgentSlots
binding, including full desktop HEADs and raw stdout/exit/hit lists. Once the
intended sitting has loaded, its binding supplies current SMRTK.session,
SMRTK.kit.sitting and LuaRevision to SMRTK.ProbePreflight(evidence). This binds
the explicitly attested desktop read to that loaded sitting. Do not provision
while loading or reuse after a map/load transition. The mod cannot validate
that an attestor told the truth or that desktop bytes match loaded code; normal
closed-game edits and the sitting's boot witness remain necessary.

08 needs first-screen witnesses for: disabled run buttons before provisioning,
gate text after provisioning, coloured verdict row, logger lit then off after
save, foreign-session refusal, normal same-process load and explicit override,
loaded provenance, console visibility, fingerprint after both MARK routes,
false dump flags, changed snapshot diff, watch field change without retargeting.
Abort on 3 repeated native save/load/console failures; keep the exact action
records and name each unrun leg. No fabricated play prediction is a result.

Coordinator metadata request, in order after 74 and before 77:

```lua
"Code/75_SMRTK_Saves.lua",
"Code/76_SMRTK_Kit.lua",
```

## DRIFT

- A first draft mistook the pack's log tag for its id; native metadata reads
  corrected it to SMR_CommunityFixPack before fingerprint verification.
- A first draft used disaster scheduler existence; source distinguished active
  g_* state from warning/countdown threads before snapshot verification.
- A first draft's method `and/or` fallback lost false; it now preserves false,
  and the falsifier includes a false native funding-method return.
- Draft provenance wording said successful actions; implementation/readout now
  explicitly say callback attempts and last toolkit record. No success coverage
  follows from counters or a lifecycle tail record.
- The sweep token in a command literal would have made 76 a hit. The command is
  composed from two adjacent token fragments; exact evidence still has to match
  the full native desktop command. The final actual source sweep is clean.
- Source searches hit wrong install/predictions paths and PowerShell glob-path
  errors; they were rerun with the installed A: source and explicit filenames.

## DEPARTURES

- Deterministic savename extends the payload's display-name-only save call:
  the native API otherwise creates unique files, breaking reusable slots.
- Metadata preflight uses LoadMetadata inside Savegame.Load rather than calling
  destructive LoadMetadataCallback. No manual parse/file read or vanilla wrap.
- Probe preflight is an explicit sitting-bound attestation. The sandbox has no
  honest runtime desktop sweep; default refusal preserves WORKFLOW's hard gate.
- Snapshot scoping/bounded records and provenance attempt semantics are stated
  above; unavailable/truncated reads stay unavailable/truncated.
- Tiny 90 accessor is the separately authorized seven-line extension; original
  toggle behavior is unchanged. Frozen core/panel integration is coordinator
  work and remains explicitly pending in this report.

## SUGGESTIONS / OWNER-ROUTED

- Have 07's compiled preflight evidence include its brief/todo's needed-probe
  names even for a clean zero-hit run, so a later stale-hit dispute has context.
- Have 08 verify the scoped snapshot fields on a colony with two loaded maps;
  if whole-colony building/colonist inventory is wanted, extend the read over
  native Cities with explicit per-map totals rather than silently widening it.
- Keep the legacy console-bootstrap redesign with 03B, as upstream ruled;
  this payload relies on the settled core arm and changes no legacy route.
- If native metadata read is denied in the retail mod environment or the load
  route wedges, stop and capture that boundary for the coordinator; never add
  file I/O, sync wrappers, account mutations or a wider console enable.

## Coordinator post-release editor correction

Native XTextEditor.Init clears lines; constructor Text does not initialize
the editor. Coordinator explicitly calls SetText after construction in this
payload, independently gated/committed by file. Source: XTextEditor171-175,
221-228 and XControl624-634. The stricter combined merge model discards
constructor Text and the specific missing-setter counterfeit goesRED. The
original payload smoke did not establish this native initialization behavior.
