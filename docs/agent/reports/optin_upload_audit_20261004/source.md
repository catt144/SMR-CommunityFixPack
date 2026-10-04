# Opt-In Paradox upload: archived-source investigation

## Must_Read_Header

Reader: parent audit worker and owner. Evidence scope: archived game Lua build
`1.1.1.406343`, repo HEAD `9dd233412ebe7babea7a6071d81db49e717d7b9f` at investigation
start. Source observations and an unrun owner diagnostic; no game/mod/source edit,
live console execution, upload, network request, or git write was performed.

## Source identity and commands

Archive root: `B:/Dev/SMR/SMR-Shared/SMR-SrcArchive/1.1.1.406343/Src`.
Source line citations below were re-derived with Git's decoded-text grep:

```powershell
& 'C:/Program Files/Git/usr/bin/grep.exe' -n '^' '<archive>/CommonLua/Libs/Paradox/ParadoxMods.lua' | Select-Object -First 178
& 'C:/Program Files/Git/usr/bin/grep.exe' -n '^' '<archive>/CommonLua/Classes/GedModEditor.lua' | Select-Object -Skip 675 -First 220
& 'C:/Program Files/Git/usr/bin/grep.exe' -n '^' '<archive>/CommonLua/console.lua' | Select-Object -First 155
& 'C:/Program Files/Git/usr/bin/grep.exe' -n '^' '<archive>/CommonLua/Modding/Mod.lua' | Select-Object -Skip 1279 -First 150
& 'C:/Program Files/Git/usr/bin/grep.exe' -n '^' '<archive>/CommonLua/Modding/Mod.lua' | Select-Object -Skip 1430 -First 220
& 'C:/Program Files/Git/usr/bin/grep.exe' -n '^' '<archive>/CommonLua/Core/lib.lua' | Select-Object -Skip 350 -First 75
& 'C:/Program Files/Git/usr/bin/grep.exe' -n '^' '<archive>/CommonLua/Core/localization.lua' | Select-Object -Skip 328 -First 142
Get-FileHash '<archive>/CommonLua/Libs/Paradox/ParadoxMods.lua' -Algorithm SHA256
Get-FileHash '<archive>/CommonLua/Classes/GedModEditor.lua' -Algorithm SHA256
```

`<archive>` abbreviates the exact archive root above; the executed commands used
the full path. Hash outputs:

```text
ParadoxMods.lua  9FAB98939528C074276A4C475FE0B76F09E9A79F0FA7FDB67D5C0970E26F3190
GedModEditor.lua 69CF418B656823D75A4439EDDCE38B5056ED98C75BE2A5B6BC47AC512BC4775F
```

## Exact pipeline and first-publish/update distinction

All references in this section name build `1.1.1.406343` in the archived tree.

`ParadoxMods.lua:382-393`: `GedOpUploadModToParadox` gets `root[1]`, validates,
asks confirmation, and passes the actual `PDX_PrepareForUpload` and `PDX_Upload`
functions as arguments to global `UploadMod`.

`GedModEditor.lua:770-822`: `UploadMod` passes those callbacks into a real-time
thread. It invokes prepare (:785), local `CreatePackageForUpload` (:791), then
the captured upload callback (:797). Packaging calls `ReloadLua()` at :711.
`Core/lib.lua:355-379` confirms a source reload between `Msg("ReloadLua")` and
`Msg("Autorun")`, via `dofile("CommonLua/Core/autorun.lua")` (:370). This establishes
that reload occurs, not that the native `AsyncPdx*` globals were replaced or that
a particular previously pasted wrapper was lost.

`ParadoxMods.lua:69-75`: choose `mod.PdxMod.ModID` or `mod.pdx_id`; request details
with the id or `0`. The details error is assigned but not checked, then shadowed
by setup's error. A valid nonempty details `Name` supplies setup's `FolderName`;
otherwise setup receives `empty_table`. Setup's returned ModName/ModFolderPath
drive subsequent staging. A details error on id `0` need not terminate a create.

`ParadoxMods.lua:78-115`: check content size against 5 GiB, copy packaged content
to the returned staging folder, check thumbnail/screenshot sizes against 2 MiB,
upload thumbnail, upload each screenshot, then upload content. Every checked
native error here returns through `upload_failed`; the copy error is replaced by
the literal `Failed to copy mod`. Screenshots use `mod:GetScreenshots()`, not the
`params.screenshots` staging list prepared by the common package helper.

`ParadoxMods.lua:118-164`: build required Pdx dependencies, external links and
forum link, then select publish API. A truthy Pdx id selects
`AsyncPublishNewModVersion`, clears `ModName`, and sends `ModId` + `ChangeLog`.
No id selects `AsyncPdxPublishMod`, sends `ModName`, and omits those update values.
Both branches send the same title, summary, description, revision display,
required-game-version string, assets, tags, links, and dependencies.

`ParadoxMods.lua:165-176`: on success, store `res.ModId`/`res.Version` in both
PdxMod and scalar fields, save the mod, delete the staging directory, return
true. Therefore a first-publish failure before this point does not assign a new
local Paradox listing id through this path.

## Validation and version meaning

`ParadoxMods.lua:13-53`: prepare checks login, then exact empty string for title,
short description, long description, preview image, and lua_revision. It requires
last_changes only for updates. It does not enforce lengths, numeric ranges,
first-publish version numbering, number of lines, or semantic-version syntax.
`GedModEditor.lua:825-843`: common validation checks active upload/unpublish
threads and saves a dirty mod after confirmation/CanSaveMod. `Mod.lua:949-965`
CanSaveMod checks item availability and potential external/source overwrite.

`Mod.lua:243-246`: editor metadata sets title max_len=60, description
max_len=8000, short_description max_len=200; the source comment ties the long
description limit to Steam/PDX upload failures. These are editor declarations,
not proved backend rules. The independent metadata agent's decoded short
description observation exceeds this declaration; I did not independently
measure the repo's metadata values in this source investigation.

`Mod.lua:266-270`: version_major/version_minor/version/lua_revision all default
to 0; version is the read-only Revision field. `Mod.lua:973-982` sets
lua_revision to ModRequiredLuaRevision, saved_with_revision to LuaRevision, and
increments version when saving. `ParadoxMods.lua:153-156` sends
`tostring(mod.lua_revision)` and `tostring(mod.version)`, not GetVersionString()
and not major.minor. There is no source-derived obligation to reset a first
publish's revision to 1.

Native setup/upload/publish implementations are not supplied in the scanned Lua
tree. Absence check used the exact native names with a positive presence side:

```powershell
& 'C:/Program Files/Git/usr/bin/grep.exe' -rnc -E 'AsyncPdxSetupModForPublish|AsyncPdxUploadModAsset|AsyncPdxUploadModContent|AsyncPdxPublishMod|AsyncPublishNewModVersion' --include='*.lua' '<archive>' | Select-String -NotMatch ':0$'
& 'C:/Program Files/Git/usr/bin/grep.exe' -rn -E 'function[[:space:]]+(AsyncPdxSetupModForPublish|AsyncPdxUploadModAsset|AsyncPdxUploadModContent|AsyncPdxPublishMod|AsyncPublishNewModVersion)[[:space:](]|(AsyncPdxSetupModForPublish|AsyncPdxUploadModAsset|AsyncPdxUploadModContent|AsyncPdxPublishMod|AsyncPublishNewModVersion)[[:space:]]*=' --include='*.lua' '<archive>'
```

The presence command returned only `CommonLua/Libs/Paradox/ParadoxMods.lua:6`.
Reconciliation: setup :72 (1), asset :93/:104 (2), content :113 (1), new-version
:143 (1), new-mod :146 (1), total 6. The definition command printed nothing and
exited 1; the six named occurrence lines reconcile with its positive control.
No native API's backend field validation, wire error details, or current server
behavior was checked.

## Error conversion and current log evidence limits

`ParadoxMods.lua:57-64` wraps an SDK error in Untranslated and concatenates
`Upload failed:` with it. The common ReportError sends this localized value
directly to `ModLog("... Error: %s", ..., message)` and to ShowMessage
(`GedModEditor.lua:779-781`). `Mod.lua:115-130` formats the log via string.format
and passes the formatted string to ModPrint. `localization.lua:342-347` wraps
Untranslated text with T; :377-416 returns a TConcatMeta table for concatenation.
Its visible source defines concat but no tostring conversion in this span.

The desk fixture extracts these shipped bodies and reproduces logging a table
identity while losing the SDK text. The localized message still contains its
text; the UI receives that localized message. A `table: 0x...` log is therefore
compatible with a useful UI error, and its pointer cannot identify the failed
stage or underlying SDK error. It is not evidence that the SDK itself returned
a table error.

Success takes ModMessage rather than ModLog (`GedModEditor.lua:801-803`), so this
success route by itself does not send a success receipt through ModPrint.

## Wrapper seam and console readiness

`ParadoxMods.lua:70/:72/:93/:104/:113` resolves each Async function through the
upload function's global environment at call time. Publish selection captures
the then-current global function in local upload_func (:139-148), immediately
before invocation. There is no preexisting file-local native binding in this
caller that would make a wrapper installed before invocation invisible.
`PdxSDK.lua:52-69` does capture its prior GetModDetails implementation locally,
but the upload caller calls the outer global, so an outer wrapper intercepts it.

`console.lua:36-44`: asserts/cmdline console environment reads and writes real
globals. :45-56: release console uses LuaModEnv and filters ModEnvBlacklist.
`ParadoxMods.lua:288-293` contributes PDX/AsyncPdx prefixes; `Mod.lua:1455-1472`
materializes those prefixes into blacklisted names. Ordinary mod code likewise
cannot read/write those globals (`Mod.lua:1559-1575`, :1612-1625).
`uiConsole.lua:355-364` recognizes statement execution, including *r threading.
The parent reports asserts enabled in both audited logs. This source account
does not substitute a sandbox cause for those runs.

Nothing here proves the earlier paste executed, installed correctly, or survived
reload. Missing capture markers cannot decide paste failure versus hook loss.
Source-local references are ruled out for the named caller; native replacement
by reload is a tested adversarial fixture, not an established live cause.

The proposed temporary capture installs a one-attempt UploadMod wrapper. Its
replacement callback is captured by the live thread before packaging, then
installs stage hooks at upload callback entry after packaging. It reads current
native functions then, so it does not require their identities to survive the
reload. It restores the native functions after success, refusal, or Lua throw.
It removes the outer dispatch hook when the target attempt begins, and no
permanent mod/source edit or new event handler is needed.

The initial visible `CONTROL arity=3 r1=nil r2=false r3=nil` and `READY armed`
markers witness installer execution; `READY after-pack stages` witnesses stage
hook installation after reload. Any NOT_READY or missing marker makes that
attempt unsuitable for attributing an SDK stage. No native/network function is
called by the installer or its local positive control. The native error return
is quoted, other string returns are lengths, tables are only types. It dumps no
arguments, response tables, account objects, credentials, paths or URLs from
requests. A caught Lua error is quoted. Those error strings are whatever the
SDK/runtime already exposes; opaque native internals were not audited for
whether an error string itself might embed a sensitive diagnostic.

## Ranked hypotheses and a future falsifier

1. Invalid create metadata, with the decoded summary exceeding its declared
   editor max_len as the concrete observed candidate supplied by the metadata
   agent. Both publish APIs receive it, but their native/server validation may
   differ. Source alone does not prove a 200-character backend limit or that
   this field caused the existing failures.
2. A staging/asset/content refusal before metadata publication. The old log's
   table identity cannot distinguish this from publish rejection. A single
   captured attempt discriminates setup, thumbnail, screenshots and content.
3. An opaque first-publish SDK/backend or account-specific failure: distinct
   native create/update APIs make this possible, but there is no verified server
   evidence. A first-publish revision restriction is unsupported by this source:
   it merely stringifies the saved revision and imposes no first-publish number.

One future owner upload of the same prepared target with this capture can falsify
the metadata-publish-stage explanation if it terminates at setup/asset/content
before AsyncPdxPublishMod begins. A details error followed by successful setup
does not count as a terminal failure. A final AsyncPdxPublishMod rejection places
the fault in publication but generic UnknownError still does not identify which
field. Shortening the summary before that same attempt and seeing success would
support its candidacy while leaving transient server failure as a confounder;
it is not a controlled proof of sole cause. No such attempt ran here.

## Desk artifact and exact observations

The ordinary console input is limited to 2048 characters (`uiConsole.lua:20-25`,
build `1.1.1.406343`). `XTextEditor.lua:375-386` removes CR/LF for single-line
controls and inserts text only if the final length fits MaxLen. A multiline
paste with Lua line comments can therefore change meaning after newline removal;
an oversized paste can fail to insert. Neither was checked against the original
owner paste because that text was not supplied to this source investigation.
`uiConsole.lua:416-420` establishes the live console global name `dlgConsole`.

The generated capture is ASCII: 3678 characters/bytes, measured by the desk
command below. Its saved artifact adds one LF, accounting for the 3679-byte file.
The complete code line exceeds the normal input limit. The exact future-owner
sequence, using the same assertions-enabled console path as the audited logs:

1. With the mod editor ready, execute this short line and require the visible
   `[PDXCAP] INPUT_LIMIT=8192` receipt:
   `dlgConsole.idEdit.MaxLen=8192; ModLog("[PDXCAP] INPUT_LIMIT=%d",dlgConsole.idEdit.MaxLen)`
2. Paste the single code line from `docs/agent/reports/optin_upload_audit_20261004/upload_capture.oneline.lua`, then
   require `[PDXCAP] CONTROL arity=3 r1=nil r2=false r3=nil` and `READY armed`.
3. Restore the transient input setting with `dlgConsole.idEdit.MaxLen=2048`.
4. Perform the intended target upload through the normal editor workflow. A
   valid capture includes DISPATCH, prepare, and READY after-pack markers before
   its stage receipts. Do not reload/restart Lua between arming and dispatch;
   arm again if the console/editor is reopened or callbacks change.

This adds no persistent file/config modification. The setter/readback/restore
sequence was executed on the desk's explicit dlgConsole.idEdit fixture, and the
source shows that the insertion guard reads self.MaxLen directly. Real UI
property access, paste insertion, and engine logging remain NOT RUN LIVE.

Command: `python docs/agent/reports/optin_upload_audit_20261004/upload_capture_desk.py`. It generates the exact
single-line paste artifact from the readable Lua by removing full-line comments,
rejecting inline comments, and joining code lines with spaces. The fixture
executes that exact generated string, not an independently rewritten probe.
Interpreter identity measured with `python -c "import lupa; r=lupa.LuaRuntime();
print(r.eval('_VERSION'), lupa.__version__)"`: Lua 5.5, lupa 2.8.

The extracted archived prepare/upload/common-thread functions run with explicit
stubs for scheduling, filesystem sizes/copy/delete, package creation/reload,
native SDK functions, minimal mod properties, socket, and localization. Native
stubs can refuse; packaging deliberately replaces every native binding and the
outer upload function to test the worst case. Additional controls exercise
trailing-nil arity, yield under pcall, a thrown Lua error and restoration,
missing Paradox globals, and source-derived localization/log text loss. They do
not exercise engine async scheduling, real reload internals, SDK validation,
game UI paste/length handling, live logging, or server behavior. NOT RUN LIVE.

The exact executed output is in [upload_capture_desk.out](upload_capture_desk.out).
The [fixture](upload_capture_desk.py) generates and tests the exact
[single-line paste](upload_capture.oneline.lua) from the [readable source](upload_capture.lua).
These inert evidence files live outside the shipped mod code and are excluded from packaging.
