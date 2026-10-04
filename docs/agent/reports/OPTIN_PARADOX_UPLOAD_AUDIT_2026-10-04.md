# Opt-In first Paradox upload audit — 2026-10-04

## Must_Read_Header

Audience: the owner and the Opt-In release orchestrator. This report records
upload inputs, the shipped upload route, and diagnostic evidence. Corrections
belong to the Opt-In session; the owner performs any upload. No mod behavior,
Opt-In file, launch-tree file, or game file was changed by this audit.

## Verdict and authority

**The strongest candidate is an oversized short summary.** The Opt-In
`short_description` decodes to **276 characters / 283 UTF-8 bytes**; the game's
PDX summary property declares **200**. The fix pack's summary is **184 characters**.
This is a **wrong input relative to the editor's declared constraint**, and a
**suspected upload cause**, not a proven server rejection. The old failure logs
do not identify the failed API or retain its error text.

The required next-attempt verdict is conditional: **after the corrections below,
the next attempt is set up the same way as the fix pack's proven upload, except
for the listed first-publication, product-content, launch-copy, gallery, and
game-build differences.** This audit cannot say that it will upload.

Owner authority preserved from the consumed brief, 2026-10-04:
*"I want an audit before we do anything else, and a fix pack agent is going to
run it."* No further upload was attempted before this report. The audit itself
does not perform the next upload or require a new ruling to finish ordinary
preparation. Existing Opt-In owner decisions remain in force.

**MEASURED identity.** Both requested pulls returned “Already up to date.”
Fix pack: `9dd233412ebe7babea7a6071d81db49e717d7b9f`.
Opt-In: `b1d139d6aa9682f85fac0453d0ceb4b41a744b85`.
Batch `2026-10-04-01` is pinned to `e75cfe2c19c2cd6c21328ebd30923f078870ea8c`,
the owner's newer store template; repo and launch metadata are byte-identical
and match its manifest. Earlier brief baselines describe older states.
Existing unrelated work in both checkouts was preserved.

All game-source citations below refer to **archived build 1.1.1.406343** at
`B:/Dev/SMR/SMR-Shared/SMR-SrcArchive/1.1.1.406343/Src`.
The failed logs identify that build; the live Steam manifest reads build
`25579348`. Named upload-source fingerprints match the live source and the
previous successful-upload build's archived `1.1.1.405907` copies
([evidence](optin_upload_audit_20261004/evidence.txt),
[rig receipt](optin_upload_audit_20261004/rig.txt)). This is a statement about
those Lua files, not equivalence of native SDKs or server state.

## Ranked candidates and one-attempt falsifiers

| Rank / classification | Evidence | What the next captured owner attempt can falsify |
|---|---|---|
| 1 — **Wrong input; suspected cause:** oversized `short_description` | MEASURED 276 decoded characters; SOURCE `CommonLua/Modding/Mod.lua:246` declares 200. `ParadoxMods.lua:29-32` tests only nonempty; :154 sends the value unchanged at publication. The native limit is unavailable. | Use the corrected summary below. Success supports this candidate but does not exclude a transient service fault. A failure before publication establishes that the new failure occurs before this field is submitted. A publication failure with the corrected summary means length correction is insufficient. |
| 2 — **Suspect:** first-create setup or publication rejection | SOURCE no Opt-In id means details lookup with id 0, setup without an existing folder name, and `AsyncPdxPublishMod`; fix-pack updates use its existing id and `AsyncPublishNewModVersion` (`ParadoxMods.lua:69-75,139-164`). Owner confirms no listing exists. | A successful setup return rules out setup rejection. A successful create return rules out final-create rejection. If capture stops at asset/content before create, do not call it a create rejection. An empty create error still does not identify the rejected field. |
| 3 — **Suspect:** remote asset/content staging or transfer rejection | SOURCE thumbnail, each gallery image, and content upload all precede metadata publication (:86-115). Valid local files and normal web/login DNS do not prove these native transfers succeed. The Opt-In uses a larger gallery and a different content payload. | Successful asset and content returns rule out those stages for that attempt. The first checked failing stage identifies the next investigation; preserve its quoted error. A details lookup error alone is not terminal: :70-73 discards it before testing setup. |

**SOURCE / MEASURED eliminations.** `lua_revision=350453` is equal in both
mods and was retained by successful fix-pack writeback `be06b4d5`; it is not a
requirement to equal running LuaRevision 406343. The title and long description
fit their declared limits. Missing title/summary/description/image and the
not-logged-in prepare branch give specific errors (`ParadoxMods.lua:13-53`),
which differ from the owner's reported “Unknown error.” Packaging alone does
not prove prepare passed: manual Pack Mod bypasses prepare (`GedModEditor.lua:742-747`).
Current account state and later SDK authorization were not inspected. Image sizes pass
the source checks. Package size is excluded by the owner's instruction and was
not pursued as a cause.

## What the retained logs and package establish

**MEASURED; full original logs preserved:** [00.19.10](../../archive/optin_upload_audit_20261004/MarsDebug.exe-20261004-00.19.10-6aba6e9d.log)
and [00.32.43](../../archive/optin_upload_audit_20261004/MarsDebug.exe-20261004-00.32.43-6aba6e9d.log).
The collector records each member and independently reconciles line and
substring counts in [evidence.txt](optin_upload_audit_20261004/evidence.txt).

| Log | Failure-line members | Compression-assert members | Diagnostic control |
|---|---|---|---|
| 00.19.10 | :390, :496 — two different table addresses | :380, :384, :488, :492 | No `[PDXDBG]`; failure lines and reload lines present |
| 00.32.43 | :391, :573 — two different table addresses | :387 | No `[PDXDBG]`; failure lines and reload lines present |

Thus the brief's “two failures” identifies two log sessions, while the files
contain the additional failure entries named above. The first log also contains
the additional assert pair at :488/:492. These are not a reconstruction of the
owner's button presses or proof of which portal each generic line represents.
The later failure at :573 follows a reload without another compression assert.

**SOURCE:** `CommonLua/Classes/GedModEditor.lua:779-781` formats the localized
message through `%s`, then displays the original message. Concatenation produces
a translation table (`CommonLua/Core/localization.lua:342-347,377-416`);
`CommonLua/Modding/Mod.lua:115-130` does not translate it for the log.
The desk control reproduces `Error: table: …` while the error text is lost.
The pointer does not mean the SDK returned a table. Empty error strings become
“Unknown error” in `ParadoxMods.lua:15-17,57-64`. Success uses `ModMessage`
rather than `ModLog` (`GedModEditor.lua:801-803`), so an absent success line in
these disk logs is not proof of absent successful publication elsewhere.

**MEASURED package:** the surviving `%TEMP%/Surviving Mars Relaunched/ModUpload/Pack/ModContent.fpk`
has SHA256 `75604e5cd607439cd214fccd19657a53e37294c782416ccf05bec8347a5d28f3`.
Its decoded contents match the launch tree **75/75, byte-identical, EXACT MATCH**.
The named members and another reconciliation appear in the committed
`pack_list.py --tree … --names` output. Its bucket reconciliation is:
root 4 + Code 19 + Data 2 + Entities 5 + Fallbacks 17 + Materials 4 +
Meshes 5 + Textures 17 + UI 2 = 75. The root members are `metadata.lua`,
`items.lua`, `LICENSE`, and `preview.png`.
The 22,606,788-byte package is reported solely for identity, not as a size theory.

The fix pack's current prediction is root 4 + Code 47 = 51, with full member
lists in the same evidence artifact. This comparison describes current inputs;
it does not recertify those inputs as an already delivered fix-pack release.
The current Opt-In repo's predicted members also match the launch payload by
name and bytes ([asset/payload receipt](optin_upload_audit_20261004/assets.txt)).
That is a present comparison, not recovery of the first attempt's old package;
the working-tree route remains wrong for the existing pinning procedure, without
evidence that it caused these failures.

**INFERRED disposition of the assert:** suspect engine diagnostic, downgraded as
a package-corruption explanation for the retained artifact. Decoding and byte
comparison succeeded, and another failure is logged without a new assert.
The native C++ assertion and why Ignore allows continuation are not explained
by shipped Lua. No attempt was made to “fix” it or to certify all future packs.

## Metadata field comparison

**MEASURED** literal values and decoded strings come from
[measure_metadata.py](optin_upload_audit_20261004/measure_metadata.py) and its
[output](optin_upload_audit_20261004/metadata.txt). **SOURCE** omitted defaults
come from archived `CommonLua/Modding/Mod.lua:243-289`, Paradox properties
`ParadoxMods.lua:258-275`, Steam properties `SteamMods.lua:54-58`, and tag
generation `Lua/Mod.lua:7-52`. Each row's disposition is **INFERRED** from
those inputs and the traced upload consumer. “Harmless” is scoped to the stated
difference, not a promise of portal acceptance. Full code/entity/ignore members
are in the measured output; they are not replaced by a count here.

| Field | Fix pack | Opt-In repo and launch | Classification / consequence |
|---|---|---|---|
| title | Relaunched Fix Pack | Relaunched Fix Pack: Opt-In Modules | MEASURED/SOURCE inputs; Harmless; 19 / 35 decoded chars, editor limit60 |
| description | Current bug-fix body; 4909 decoded chars | Latest owner-template body; 6165 decoded chars | MEASURED/SOURCE inputs; Harmless within8000; backend create acceptance untested |
| short_description | Bug-fix single paragraph; 184 chars | Latest owner bullet summary; 276 chars | MEASURED/SOURCE inputs; Wrong relative to declared200; suspected rejection cause |
| tags | omitted→empty string | omitted→empty string | MEASURED/SOURCE inputs; Harmless legacy field; booleans determine current tags |
| image | Mod/SMR_CommunityFixPack/preview.png | Mod/SMR_CommunityOptInPack/preview.png | MEASURED/SOURCE inputs; Harmless same mounted path form; both1024×1024 PNG,44322 /41743 bytes |
| external_links | omitted→{} | omitted→{} | MEASURED/SOURCE inputs; Harmless; no typed-link validation discrepancy; site URL in free description |
| last_changes | Current release note,972 decoded chars/5 LF | First release note,377 decoded chars/no LF | MEASURED/SOURCE inputs; Harmless; first publish does not require note but provides one |
| ignore_files | Shared exclusions plus zz-owner,saves | Shared exclusions plus staging | MEASURED/SOURCE inputs; Harmless product/workspace boundary; differences named below |
| dependencies | omitted→false | omitted→false | MEASURED/SOURCE inputs; Harmless true standalone; do not add sibling dependency |
| id | SMR_CommunityFixPack | SMR_CommunityOptInPack | MEASURED/SOURCE inputs; Harmless distinct persistent product identity |
| content_path | omitted→false property default; runtime-populated | same | MEASURED/SOURCE inputs; Harmless dont_save field; not a missing path setting |
| author | catt144 | catt144 | MEASURED/SOURCE inputs; Equal |
| version_major |1|1|Equal |
| version_minor |omitted→0|explicit0|Harmless equivalent; serializer omits defaults |
| version |26|0|Harmless released vs first publish; editor owns future bumps |
| lua_revision |350453|350453|Equal; required revision, not current full build number |
| saved_with_revision |405907|omitted→0|Harmless historical serializer bookkeeping; don't hand-fill |
| restart_on_unload |omitted→auto|omitted→auto|Equal |
| optional_mod |true|false|Harmless approved native missing-mod warning policy OI-43 |
| entities |omitted→false|SMROptInTrainHub6, SMROptInTrainHub6Glass, SMROptInTrainHub6DomeGlass, SMROptInElevatorDepot, SMROptInElevatorDepotReceiver|Harmless shipped train models; SourceData editor input accompanies launch |
| code |Fix-pack core/load-first/hub scaffold, fix modules, sanitizer (full members measured by script below)|Opt-In core, seven registrars, train parts and generated templates/entity data (full members measured below)|Harmless different products; load order preserved, do not transplant |
| loctables |omitted→false|omitted→false|Equal |
| default_options |LoadFirst=true|AcknowledgedWarnings=false; MultipleSuns=false; ServiceInterestTags=false; DroneSpeedDial="1x (base)"; DroneCarryDial="+0 (base)"; StationRows=false; TrainHub=false; ElevatorDepot=false|Harmless distinct options; exact option values retained |
| has_data |omitted→false|true|Harmless native templates vs runtime fix code |
| saved |1790618041|omitted→false|Harmless editor timestamp; don't hand-fill |
| code_hash |-7946660084903740849|omitted→false|Harmless editor dirty-check bookkeeping; don't transplant |
| screenshot1 |store_screenshots/1_rare_metals_drill_skin.jpg|store_screenshots/1_hub_day.jpg|Harmless chosen gallery; paths prefixed Mod/product-id/ |
| screenshot2 |store_screenshots/2_rare_metals_hammer_skin.jpg|store_screenshots/2_hub_panel.jpg|Harmless chosen gallery |
| screenshot3 |store_screenshots/3_moxie_skins.jpg|store_screenshots/3_depot_pair.jpg|Harmless chosen gallery |
| screenshot4 |omitted→empty string|store_screenshots/4_station_rows.jpg|Harmless supported gallery slot |
| screenshot5 |omitted→empty string|store_screenshots/5_interests_popout.jpg|Harmless supported gallery slot |
| affected_resources |omitted→false|omitted→false|Equal conflict-descriptor field |
| pdx_id |156049|omitted→false|Harmless updates vs first-create; wrong to copy donor id |
| pdx_version |"17"|omitted→false|Harmless portal return value, not our version |
| steam_id |"3787202810"|omitted→0|Harmless updates vs first-create; wrong to copy donor id |
| TagGameplay |true|true|Equal supported category |
| TagBuildings |omitted→false|true|Harmless approved building content category |
| TagCommanderProfiles |omitted→false|omitted→false|Equal |
| TagMissionSponsors |omitted→false|omitted→false|Equal |
| TagColonyLogos |omitted→false|omitted→false|Equal |
| TagResearch |omitted→false|omitted→false|Equal |
| TagCrops |omitted→false|omitted→false|Equal |
| TagTraits |omitted→false|omitted→false|Equal |
| TagRadio |omitted→false|omitted→false|Equal |
| TagLightmodels |omitted→false|omitted→false|Equal |
| TagTranslations |omitted→false|omitted→false|Equal |
| TagCosmetics |omitted→false|omitted→false|Equal |
| TagInterface |omitted→false|omitted→false|Equal |
| TagTools |omitted→false|omitted→false|Equal |
| TagOther |omitted→false|omitted→false|Equal |
| TagTerraforming |omitted→false|omitted→false|Equal |
| TagLandscaping |omitted→false|omitted→false|Equal |
| TagVegetation |omitted→false|omitted→false|Equal |
| TagFaction |omitted→false|omitted→false|Equal |
| TagLaw |omitted→false|omitted→false|Equal |
| PdxMod (runtime cache, not serialized property) |not authored; id fallback present|not authored|Harmless; nil until native publish sets cache |

The metadata's Lua wrapper differs: fix pack returns a local `def` around an
inert local canary; Opt-In directly returns `PlaceObj`. **Harmless, SOURCE /
INFERRED:** both return the ModDef consumed by the same serializer.

The ignore-list differences are named, not treated as a count discrepancy:
fix-pack-only `*/zz-owner/*` and `*/saves/*`; Opt-In-only `*/staging/*`.
The remaining patterns and their order are recorded in the measured output.
The SourceData and screenshot exclusions are shared. Screenshot files are
uploaded separately from their mounted paths (`ParadoxMods.lua:96-108`), so
excluding their directory from ModContent.fpk is expected.

The remembered long-description figure is replaced by the decoded measurement:
**6165 characters / 6192 UTF-8 bytes**, not the brief's 6212. The current preflight
parser reports 6206 because it retains Lua newline escapes; it also reports 283
for the 276-character summary. Its checks test nonempty, not maximum length
(Opt-In `tools/upload_preflight.py:209-219`). The independent
`store_parity.py` result agrees with the decoded lengths. A green preflight was
therefore not evidence that the summary fit the editor declaration.

**INHERITED historical comparison, checked against the dated receipt:**
`STORE_CARD_LIVE.md:395-399,500-502` records successful fix-pack updates with
longer descriptions than the current Opt-In body. The original first-create
body was much shorter (`RELEASE_PORTAL_PREP.md:538-564`). These are historical
acceptance receipts, not fresh portal measurements or proof that the create
endpoint and update endpoint enforce identical limits.

## Workflow, package, and rig differences

| Difference | Disposition and evidence |
|---|---|
| First publication versus updates | **Harmless required difference; SOURCE / owner receipt.** Missing Opt-In ids are correct. Fix-pack first-create succeeded at revision 0; `RELEASE_PORTAL_PREP.md:131-173,384-399` records that initial route and downloaded artifact. `V10_RELEASE_RECORD.md` is a later update receipt. No donor id or fabricated id belongs in Opt-In metadata. Backend create remains a suspect branch as ranked above. |
| Working tree versus pinned launch tree | **Harmless intentional difference once linked; MEASURED.** The fix pack Mods junction targets its working repo. Opt-In's targets `B:/Dev/SMR/SMR-OptInPack-launch`; the workbench has its own sibling junction into `SMR-OptInPack/staging`. The owner-reported first working-tree route was wrong relative to Opt-In's existing pinned-release procedure; its earlier package is not retained. The surviving package establishes the launch route now. |
| Links inside the source | **Harmless with the measured filter.** Predictor found fix-pack `saves/backup`, `saves/game`, `zz-owner/all-claude-memory`, and `zz-owner/claude-memory` under their matching exclusions. Neither Opt-In tree exposed a reparse point to that walk. The launch's positive decoded package member list establishes what actually packed. |
| Native models/templates versus Lua-only fixes | **Harmless intended product difference; MEASURED/SOURCE.** Opt-In adds the named Data/Entities/Fallbacks/Materials/Meshes/Textures/UI members. `has_data`, `entities`, code order and `items.lua` describe them. Removing them to mimic the fix pack would change the mod. SourceData is retained for the editor but excluded from the package. |
| Gallery and preview | **Harmless local-input difference; MEASURED/SOURCE.** Fix pack uses its three chosen screenshots; Opt-In uses its five approved screenshots. Every inspected image is readable and under the per-image threshold, with names/sizes in the companion asset receipt. Slots 1–5 are supported; the create/upload consumer sends each. Remote acceptance remains unmeasured. |
| Editor route and saving | **Harmless shared route; SOURCE / recorded procedure.** Main menu → Mod Editor/restart → correct mod → Pack Mod → Paradox first, then Steam. Upload itself packages again and reloads Lua (`GedModEditor.lua:676-741,770-822`). Manual Save is not a required cure. Common dirty validation can request a save (:835-843); Paradox saves after success (:167-173); Steam's create-only pre-pack save remains distinct from updates. |
| Opt-In batch receipts | **Wrong/incomplete audit bookkeeping; MEASURED.** Current batch has no snapshots or receipts for either portal despite the retained failed-attempt evidence. This cannot cause native rejection. Opt-In session should preserve these failures and future per-portal snapshots using its existing release procedure, without treating a failed pack as a publication receipt. |
| Latest store text | **Harmless owner-directed difference.** Owner commit `e75cfe2` chose a shorter lede, no console section, no credit line, and a bullet summary. The re-pinned launch metadata matches it. Preserve that decision while shortening the summary; do not restore older store prose. |
| MarsDebug and game build | **Suspect only where native behavior differs.** Failed logs identify asserts/debug build 406343. The latest fix-pack upload receipt retained saved-with 405907. The archived Paradox and GED upload Lua files are byte-identical across those builds. The earlier successful uploader executable and native SDK state are not established by the receipt; do not label either binary difference harmless on the Lua hash alone. |
| Braze DNS and login/mods DNS | **Harmless as a demonstrated new differentiator; INFERRED with a limit.** Current DNS sinks Braze to `::`/0.0.0.0 and resolves the named mods/login hosts normally. The same Braze resolution-failure symptom occurs in archived fix-pack logs before its successful Sept 28 upload. Exact DNS answers at that upload instant were not recorded, so historical sinkhole identity is unproved. Nothing in the traced upload Lua calls Braze. Native transfer endpoints remain untested. Do not change DNS on this evidence. |
| Platform approval and later portal styling | **Harmless separate owner work.** Opt-In's existing OI-44 holds its platform choice/approval question. The fix pack's approval does not transfer. Auto-fill and formatting cleanup are settled owner receipts; neither is a reason to re-ask about descriptions or change the current release procedure. |

Braze reference control: `docs/archive/logs/f128_Mars.exe-20260928-13.25.51-6aad2d75.log:195-206`;
the successful release writeback is `be06b4d5` and the owner's receipt in
`docs/archive/RELEASE_HISTORY.md`, “Released in v18.” These establish an older
recurring symptom and later success, not a packet capture of that upload.

No new owner policy decision is required for the proposed corrections. OI-44
remains the existing owner question; this audit did not add or edit Opt-In
checklist items.

## Exact corrections and owners

1. **Opt-In orchestrator — shorten the maintained short-summary block and its
   matching `metadata.lua short_description`.** This ASCII candidate measures
   **197 characters/bytes**, including its line breaks, preserves the latest
   owner bullet format, and retains each module group:

   ```text
   Off/base until enabled in Mod Options:
   - Acknowledged warnings
   - Multiple Artificial Suns
   - Drone speed/carry dials
   - Service interest tags
   - Station import/export rows
   - Train Hub
   - Elevator Depot
   ```

   Opt-In `store_parity.py --write-metadata` writes description/last_changes,
   not the summary; the orchestrator must synchronize that pair explicitly.
   This is a proposed edit, not an edit made here.

2. **Opt-In tooling owner — add decoded-length validation** for title 60, summary
   200, and description 8000, using the decoder already exercised by store parity.
   Identify these as declared editor constraints; do not claim coverage of all
   backend limits. Preserve the passing parity check as a separate check.

3. **Opt-In release orchestrator — commit and re-pin/rebuild the launch batch
   under the existing procedure**, verify the new manifest/summary and junction,
   and retain the failed-attempt evidence. A change to the working repo alone
   does not change a commit-pinned launch. Leave the currently absent listing
   ids and authored revision to the editor; do not fabricate ids or reset a
   revision. Dirty validation may save and increment it even before an upload
   fails. Preserve genuine editor-generated save/hash/revision/writeback values.

4. **Audit handoff supplies the capture; Opt-In session prepares it; owner runs
   the next attempt.** Use the method below, then preserve the fresh main
   MarsDebug log and the package before another pack can overwrite them.
   Per-portal success still needs the existing owner receipt and writeback.

## Capture and the owner's next sitting

**SOURCE conclusion about the failed wrapper:** the named upload caller does
not hold inaccessible file-local AsyncPdx bindings. It looks up the stage
globals at invocation; its local publish choice is made immediately before the
call (`ParadoxMods.lua:70-73,93-114,139-148`). Packaging reloads Lua before the
upload callback. Source and logs do not show whether the old paste ran, whether
it installed correctly, or whether any particular native hook survived reload.
Thus “local references hid every wrapper” is ruled out for this caller;
“the paste failed” is still unproved.

Both audited runs have `Platform.asserts`, for which
`CommonLua/console.lua:36-44` gives the console real-global access. The retail
mod console is different: `console.lua:45-56` and
`ParadoxMods.lua:288-293` filter PDX/AsyncPdx names. A sandbox diagnosis is not
established for these debug runs. The console declares `MaxLen=2048`
(`CommonLua/UI/Dev/uiConsole.lua:20-25`). Its editor removes line breaks and
refuses an oversized insertion (`CommonLua/X/XTextEditor.lua:375-386`). The old
paste text is unavailable, so length or comment collapse is a candidate for the
missing marker, not a proved explanation. The supplied comment-free one-line
capture measures 3678 ASCII characters and needs the temporary input-limit
change below; the fixture checks this exact string.

The supplied diagnostic wraps `UploadMod` for the target Opt-In attempt and
passes a replacement callback into the live upload thread. That callback
installs the stage hooks **after packaging**, then calls the original upload
callback and restores the hooks on return or Lua error. The initial control
and READY marker establish execution before any upload; the after-pack marker
proves hook installation/readback, and each stage's `BEGIN` proves that its
intercepted call was reached. Raw
first-return error strings are quoted; argument/response tables are not dumped.

**DESK VERIFIED; NOT RUN LIVE.** The companion fixture executes the archived
prepare/upload/common-thread functions with explicit SDK, filesystem, scheduling,
and packaging stubs, including a package step that replaces the globals.
It checks create/update dispatch, ignored details errors, terminal stage errors,
return arity with trailing nils, yield through the protected call, restoration,
and missing-global refusal. This tests the diagnostic logic, not the native
SDK, server, or real console paste. The owner checks the readiness marker before
committing an upload attempt.

**Owner sequence — [NEVER RUN LIVE]; after the Opt-In corrections are ready:**

1. Finish the normal Mod Editor **Pack Mod** step first. In the **main game's
   MarsDebug console**, enter the short line below and require
   `[PDXCAP] INPUT_LIMIT=8192` in the main log. It changes this console widget's
   input length only; it makes no upload call.

   ```lua
   dlgConsole.idEdit.MaxLen=8192; ModLog("[PDXCAP] INPUT_LIMIT=%d",dlgConsole.idEdit.MaxLen)
   ```

2. Paste the entire [single-line capture](optin_upload_audit_20261004/upload_capture.oneline.lua)
   as one console command. Require both
   `[PDXCAP] CONTROL arity=3 r1=nil r2=false r3=nil` and
   `[PDXCAP] READY armed` in the main log. Missing markers or `NOT_READY` mean
   stop here. The [readable source](optin_upload_audit_20261004/upload_capture.lua)
   is for review; do not paste its multiline comments into the single-line editor.
3. Restore the widget with `dlgConsole.idEdit.MaxLen=2048`, close the console,
   and make **one Paradox upload attempt**. Do not manually pack, save, or restart
   between arming and that attempt: another reload can replace the outer hook.
4. Preserve the whole fresh main log and the resulting package before another
   pack. Expect `DISPATCH branch=create`, `BEGIN/END prepare`, then
   `READY after-pack stages` and the native `BEGIN/END` lines. If the after-pack
   marker never appears, do not attribute an SDK stage from that attempt.
5. Hand the receipt to the Opt-In session. It reads the first **checked** failing
   return, the corresponding UI error and final `END upload` restoration marker.
   A failed id-0 details lookup followed by successful setup is not the cause.
   `AsyncPdxUploadModAsset#1` is the thumbnail; subsequent ordinals follow the
   metadata screenshot order. A fresh process removes any remaining temporary
   console hook if the attempt is abandoned.

The next attempt can therefore locate a failing stage even when the UI repeats
“Unknown error.” If no readiness marker appears, stop before uploading and fix
the capture setup. If the final create still returns an empty error, preserve
that precise result as an unresolved SDK/server refusal; do not turn it into a
specific field diagnosis.

## Reproduction, checks, and limits

The report's measured outputs are committed beside it. Commands below are
**[RAN 2026-10-04]** with the stated checkout/build, not prospective checks:

- `git log --oneline -5`, `git pull`, and `git status --short` in each repo:
  identities above, both pulls current; unrelated changes preserved.
- `python docs/agent/reports/optin_upload_audit_20261004/collect_evidence.py`:
  [log members, positive controls, pack filters/members, and source hashes](optin_upload_audit_20261004/evidence.txt).
  This includes Opt-In's `pack_list.py` decode and comparison, not a raw compressed-file grep.
- `python docs/agent/reports/optin_upload_audit_20261004/measure_metadata.py`:
  [decoded lengths, literal fields, list members, and batch-manifest controls](optin_upload_audit_20261004/metadata.txt).
- Exact PowerShell DNS, junction, build and cross-build hash commands:
  [rig.txt](optin_upload_audit_20261004/rig.txt).
- `python docs/agent/reports/optin_upload_audit_20261004/measure_assets.py`:
  [image members, dimensions, sizes, and current repo/launch payload comparison](optin_upload_audit_20261004/assets.txt).
- Scoped decoded-source `grep -n`: [source evidence](optin_upload_audit_20261004/source.md).
  `python docs/agent/reports/optin_upload_audit_20261004/upload_capture_desk.py`:
  [fixture](optin_upload_audit_20261004/upload_capture_desk.py) and
  [output](optin_upload_audit_20261004/upload_capture_desk.out), independently rerun
  after promotion from scratch. Source line numbers name the archived build.
- Probe sweep: decoded `grep -rln TEMPORARY Code/ B:/Dev/SMR/SMR-BugFixPack-TestKit/Code/`
  returned no matches, exit 1; each tree's core file was present. No live probe
  was installed. Required repository validation is recorded in the commit.

**Not opened or exercised:** no saves, native SDK/C++ implementation, live
account-management API, new upload, source mutation, DNS mutation, or game
launch. The first attempt's old package and an execution record of its console
paste are unavailable. No current portal absence claim replaces the owner's
existing check. The exact historical DNS sinkhole at successful upload time is
unrecorded. These limits prevent a proven root-cause verdict.

The reusable source findings are filed in [EF-122](../facts/EF-122.md).
The one-off brief and its live map row are consumed with this report.
