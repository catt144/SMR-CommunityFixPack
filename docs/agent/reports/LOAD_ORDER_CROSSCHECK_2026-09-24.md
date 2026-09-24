# Load-order crosscheck — 2026-09-24

## Must_Read_Header

Report for the owner and the Claude review seat, executing the one-off
`LOAD_ORDER_CROSSCHECK_high.md` from `680c279`. The task reserves implementation
to the owner and entry changes until Claude checks this report. This commit
changes neither production Lua nor the fact entries, policy or player advice.

The owner's clarification during this investigation supplies the objective:
“Basically we only fix things in vanilla, so if a content mod needs to alter the
game in areas we fix, it would be best, if it did its alterations after we ran.”

## Answer

**Loading the vanilla repair pack first is a useful compatibility default, and
the old claim that its position cannot be influenced is too strong.** There is
a source-verified, desk-tested route for the pack to move itself to the front
of the saved enable order for the next cold boot. Cooperative content mods can
also declare the pack as a prerequisite. A more invasive metadata bootstrap
is a candidate for intervening before the first cold queue is built; its desk
prototype assumes native class/property behavior that still needs a retail
check. None of these requires editing game files; none was shipped
or tested in a new retail launch during this investigation.

**MEASURED, desk; SOURCE-VERIFIED, 1.1.1.405907:** the saved-order route uses
public game helpers even though direct account storage is blacklisted. It
preserves the other mods' relative order. The current launch has already chosen
its queue, so this route takes effect on a subsequent cold boot. Actual account
file persistence and platform sync remain **HYPOTHESIS** until a retail run
confirms them; the desk control records the real writer's save request.

**SOURCE-VERIFIED, scope of the benefit:** early vanilla function repairs can
become the base that later content mods wrap or replace. That matches the
owner's intent. File order does not impose the order of every later event,
preset edit or deferred patch. There is no measured basis for “nearly every
load-order issue”; the counterexamples below identify specific remaining
classes without estimating their frequency.

## Evidence and scope

`SOURCE-VERIFIED` means the cited source settles the stated mechanism, including
explicitly identified deductions from its control flow. `MEASURED` identifies
a command, desk fixture or existing game log. `HYPOTHESIS` identifies a result
still requiring the named measurement. Desk Lua is Lua 5.5 through lupa 2.8;
it is not the retail engine.

Game source abbreviations below always mean archived trees under
`B:/Dev/SMR/SMR-Shared/SMR-SrcArchive/<build>/Src/`:

| Label | Build | `Mod.lua` means |
|---|---|---|
| 107 | 1.0.7.396349 | `CommonLua/Classes/Mod.lua` |
| 110 | 1.1.0.403908 | `CommonLua/Modding/Mod.lua` |
| 111 | 1.1.1.405907 | `CommonLua/Modding/Mod.lua` |

Other relative source paths retain that same build prefix. Pack source is
pinned to `680c2799282dc6c60079691f1e201974a8a006e8`. The concurrent
`bddb5aa` commit files hub findings and changes the separate migration prompt;
its diff does not change the pack Lua examined here.

**MEASURED:** the identity instrument checks the named source files against
their archived manifests, and the 111 files against the live installation.
Steam's installed build read from `appmanifest_3215050.acf` is `25390750`.
The exact file members and hashes are in the evidence receipt. This is scoped
source parity, not a new whole-game `Lua.fpk` parity claim.

**[RAN 2026-09-24, archived receipt]** The exact commands, script hashes, input
hashes and outputs are in
[`measurements.txt`](../../archive/load_order_crosscheck_2026-09-24/measurements.txt).
The archived instruments were executed from the repository root and all exited
successfully:

| Instrument | What it establishes |
|---|---|
| [Identity and decoded sample](../../archive/load_order_crosscheck_2026-09-24/load_order_inventory.py) | Named source manifests/live parity and decoded metadata presence/absence controls. |
| [Dependency queues](../../archive/load_order_crosscheck_2026-09-24/load_order_loader_probe.py) | Shipped queue and version-fit behavior across the archived builds, including optional dependencies. |
| [Saved-order helpers](../../archive/load_order_crosscheck_2026-09-24/load_order_reorder_probe.py) | Real sandbox visibility, account-list mutation and save-request boundary. |
| [Pack and class controls](../../archive/load_order_crosscheck_2026-09-24/load_order_pack_controls.py) | VacuumWalks ordering, warning-list entry, canonical declaration recovery, veto timing and copied inheritance. |
| [Metadata bootstrap](../../archive/load_order_crosscheck_2026-09-24/load_order_metadata_probe.py) | Callback-to-selector prototype under native class/property shims; real queue shape and disabled-pack controls. |

No game was launched, no save was inspected, and no account settings,
subscriptions or installed mod files were changed. Native engine/SDK source,
console execution, packaged metadata acceptance and a Mod Editor round trip
were not tested. The metadata harness uses a selector fixture around the
shipped dependency queue; it does not run the full native initialization or
every filter in `GetModsToLoad`.

## Re-verdict of the task's starting claims

| Starting claim | Verdict and evidence |
|---|---|
| EF-054: normal order is the player's enable order, with prerequisites first | **Confirmed with qualification — SOURCE-VERIFIED + MEASURED.** DFS preserves root order but visits dependencies first; filtering can remove roots. 111 `Mod.lua:1907-2060,2135-2146,2285-2297`; extracted queue controls agree across 107, 110 and 111. |
| `LoadAllMods` uses alphabetical mod IDs | **Confirmed — SOURCE-VERIFIED.** 107 `Mod.lua:1988-1990` explicitly sorts keys; 110/111 `Mod.lua:1995-2000` uses `table.keys(Mods, true)`, whose sort flag is documented in 111 `CommonLua/LuaExportedDocs/Global/table.lua:213-224`. Dependencies still run first; titles and Workshop numbers are not the sort keys. |
| Neither branch is influenceable by mod code | **Corrected — MEASURED + SOURCE-VERIFIED.** The helpers below alter the normal branch's saved seed. Accessible loader functions and tables also permit invasive runtime intervention. Directly blocked globals do not establish that all indirect routes are blocked. |
| No mod can declare or request a position | **Corrected — SOURCE-VERIFIED.** There is no ordinary global-priority property in the inspected loader, but `ModDependency` expresses a pairwise prerequisite. The declaration belongs in the dependent content mod, not in the pack. 111 `Mod.lua:260-262,1966-1983,2802-2823`. |
| No mod can detect its position ahead of its own load | **Corrected — SOURCE-VERIFIED.** Its first code can inspect the already-complete `ModsLoaded` queue and locate `CurrentModId`; 111 `Mod.lua:2135-2146,1559-1567,1628-1638,2285-2297`. This detects earlier positions before applying a fix, not before those earlier mods execute. |
| Intra-mod file order is simply `ipairs(self.code)` | **Corrected detail — SOURCE-VERIFIED.** 111 `Mod.lua:492-523` makes two passes: generated/non-`Code/` files first, excluding `__const.lua`, then `Code/` files, preserving list order within each pass. This does not move the whole mod before another mod. |
| First means innermost and gives content mods precedence | **Confirmed conditionally — SOURCE-VERIFIED.** It holds when the pack installs the function before the other mod captures/wraps it. An outright later replacement wins by erasing the earlier wrapper. Different patch phases and earlier captured references need separate reasoning. Pack `00_Core.lua:529-559` applies ordinary fixes during registration; its `DataPatch` instead waits for later triggers at `:399-456`. |
| Nothing breaks at any position | **Corrected — MEASURED, desk.** The current VacuumWalks guard declines after Passage Network's global clobber and succeeds before it. That demonstrates an order-sensitive guard; it does not yet reproduce the reporter's exact v19 launch. |
| The visible manager sort is cosmetic | **Confirmed — SOURCE-VERIFIED.** 111 `Mod.lua:1687-1696` sorts `ModsList` for editing; `CommonLua/UI/ModManager.lua:1618-1682` sorts display lists/settings. Neither is the saved enable sequence consumed by the queue. |
| Players cannot verify a reorder | **Corrected — SOURCE-VERIFIED + MEASURED log.** They cannot use that display sort as proof, but the loaded-ID log line exposes the queue. An explicit order display could make verification easier; no such feature was built here. Existing policy against public load-order advice remains unchanged pending review/owner decision. |
| The 2026-08-23/24 observations establish pack-first on two rigs | **Unproven by this crosscheck as a renewed measurement.** EF-054/F104 record it; the exact original raw logs named there were not recovered in the archive search. Those historical records are not refuted. The task's current example is independently readable and has a narrower result below. |
| EF-025: enable-path reload differs from cold boot; ClassesBuilt works on both, DataLoaded does not repeat on enable | **Confirmed — SOURCE-VERIFIED.** 111 `CommonLua/Dlc.lua:551-557,600-604`, `Mod.lua:2163-2178`, `CommonLua/Core/lib.lua:355-374`, `CommonLua/Core/classes.lua:1327-1453`. `LoadData` belongs to the cold DLC path, not the hot `ReloadLua` path. “Every player's first run” is broader than this mechanism proves; sync/programmatic enablement was not exhaustively tested. |
| Class globals are bare declarations while mod code runs | **Confirmed with clobber caveat — SOURCE-VERIFIED.** 111 `CommonLua/Core/classes.lua:58-74,1327-1352,1436-1453`: declarations are kept separately, later built and republished. A mod can replace the global temporarily without replacing the retained declaration. |
| Passage Network has stray `Dome` functions that explain VacuumWalks' warning | **Confirmed mechanism, reporter attribution still HYPOTHESIS.** Archive `PassageNetwork_1.38_Code_PassageNetwork.lua:45-51`; pack `Fix_VacuumWalks.lua:67-72,143-151`; real core/module desk control below. The deciding retail observation is PN-before-pack with the same guard failure and warning, then reversed order with success. |

## The loader across builds

**MEASURED:** the normalized helper-plus-queue slice is identical in 110 and
111: `Mod.lua:1873-1993`, SHA-256
`749348d898cbef2fd42a426c357bfd960903ea4928b0b9e2111c19be31da249e`.
The corresponding 107 slice is `Mod.lua:1860-1980`. Its queue behavior matches
the exercised cases; the later queue adds the `silent` argument and suppresses
diagnostics when requested. The 110-to-111 whole `Mod.lua` diff changes
warning scheduling and conflict-report handling, not this ordering algorithm.
Identity is not assumed from shifted line numbers.

**SOURCE-VERIFIED, 111:** cold boot loads definitions and selects the queue in
`CommonLua/Dlc.lua:551-555`; `ModsReloadItems` populates `ModsLoaded`, handles
entity setup and loads options (`Mod.lua:2135-2164`). Lua reload then loads
vanilla `Lua/`, DLC code and mod code in that sequence
(`CommonLua/Core/autorun.lua:431-434`). Class building follows; cold data loading
and item loading follow through `Dlc.lua:600-604` and `Mod.lua:2181-2222`.
Ordinary options data, entities and items provide no earlier execution turn for
an ordinary `Code/` file.

**SOURCE-VERIFIED, 111:** an order-only change is invisible to the normal hot
reload gate: `Mod.lua:2104-2112` sorts the old and new IDs and compares sets.
A cold restart is therefore part of the saved-order proposal. The mutable
`ModsReloading(queue)` event at `:2115-2117` is fired only when `first_load` is
false. A code-installed handler cannot establish first-launch cold ordering.

**MEASURED, extracted queue on 107/110/111:** declaring a required prerequisite
orders it first when enabled and compatible; a missing, disabled or incompatible
required prerequisite excludes the dependent; a required cycle excludes its
members. Optional dependencies have a material trap: an installed but disabled
optional prerequisite is still queued, and an absent optional prerequisite
reaches a nil `mod` in `GetModAllDependencies` (107 `:1864`; 110/111 `:1877`).
An incompatible optional prerequisite is also visited. Source: 111
`Mod.lua:1966-1976` ignores an optional dependency error but still recurses.
This is desk evidence of the queue body, not a new claim that the full retail
UI always exposes every fixture. It prevents treating “optional” as a proven
safe compatibility recommendation.

## Practical saved-order route

**SOURCE-VERIFIED, 111; MEASURED in 110 and 111:**

1. `GetModsEnabledByUser()` returns a copy of the normal seed
   (`Mod.lua:1995-2000`).
2. `TurnModOff` and `TurnModOn` remove/append IDs in real account storage
   (`CommonLua/UI/ModManager.lua:35-45`). Their function bodies retain their
   engine environment even when called by a mod.
3. Those helpers are accessible through the mod environment. Direct
   `AccountStorage` and `SaveAccountStorage` are blacklisted
   (`Mod.lua:1280-1297,1559-1567`).
4. A changed own persistent-data write calls `SaveAccountStorage(1000)`
   (`Mod.lua:1487-1503`); `SetupEnv` exposes the per-mod writer at `:1636-1638`.

The fixture changed `B,PACK,C` to `PACK,B,C`; the current `ModsLoaded` stayed
`B,PACK,C`. The next computed queue was `PACK,B,C`. Rewriting identical
persistent data did not request another save. The fixture's save service is a
recording stub, so it establishes the request rather than a completed disk write.

**SOURCE-VERIFIED deduction:** in normal mode, if the pack has no prerequisite
and is the first surviving seed entry, DFS appends it before visiting any later
root. Later mods, even newly appended mods with their own dependencies, cannot
retroactively precede it. Relevant exceptions are changes to that saved seed,
the pack acquiring a prerequisite, `LoadAllMods`, filtering out the pack, or
another component rewriting the loader/queue.

**HYPOTHESIS, implementation and retail persistence:** a pack-controlled
“apply vanilla repairs first” setting could do this once, preserve the other
IDs, and report that a restart is needed. A real implementation would preserve
the pack's own persistent data, avoid repeatedly changing account state, and
verify the asynchronous save before claiming success. Retail cold restart,
repeated launch, hot enable, disable/re-enable and Paradox sync tests would
decide it. This report does not choose the default or add a settings UI.

## First-cold-load metadata route

**SOURCE-VERIFIED timing, 111:** metadata's restricted environment supplies
`PlaceObj` and `box` (`Mod.lua:1715-1724`). The definition loader later assigns
the returned `ModDef` its mod environment and calls `def:SetupEnv()`
(`:1769,1790-1797`), before `ModsReloadItems` invokes `GetModsToLoad`
(`:2099-2102`).

**HYPOTHESIS, native object behavior:** metadata can attach an instance
`SetupEnv` method after construction. The Lua assignment path calls the native
member check through `PropertyObject.__newindex`
(`111 CommonLua/PropertyObject.lua:78-87`); the probe substitutes that check
and class construction. The proposed access path is the returned instance,
rather than a free global inside the metadata sandbox. The prototype therefore
does not by itself establish that the retail object accepts the override.

**MEASURED, isolated Lua prototype:** a custom instance `SetupEnv` calls the
original method, captures `self.env.GetModsToLoad`, and replaces that global
through the ordinary mod environment. Its wrapper calls the original selector,
then moves the pack's **string ID** to numeric index one if the pack survived
selection. The queue's `queue[id]=ModDef` lookup entries remain intact. Numeric
queue entries are strings, not mod objects (`111 Mod.lua:1954-1955`); the
prototype's falsifier distinguishes those shapes. An absent pack leaves the
queue unchanged.

The desk harness loads the shipped constructor/property/environment bodies and
the shipped dependency queue; native property membership, engine class setup
and persistent-storage initialization are named shims. It does not execute a
packaged retail mod. **HYPOTHESIS:** real packaging and engine initialization
accept the bootstrap and carry its selected queue into the first code load.
An isolated packaged cold boot with code-entry witnesses, followed by a
main-menu enable/reload, would decide that remaining claim.

**SOURCE-VERIFIED deduction, 111:** the cold path calls `ModsReloadDefs`, selects
mods, then reloads Lua (`CommonLua/Dlc.lua:551-557`). Lua reload can overwrite
the selector wrapper with its vanilla definition, but `ModsLoaded` is already
built and is only initialized under `FirstLoad` (`Mod.lua:1-4,2135-2146`).
`ModsLoadCode` uses that chosen array (`:2285-2297`). Thus overwriting the
wrapper during reload does not by itself undo the selected cold order.

Costs matter here. Definition enumeration also visits disabled installed mods,
so the wrapper can be installed while the pack is disabled; the membership
guard makes its queue change inert, not its registration nonexistent. Repeated
definition loading can nest wrappers. A future pack prerequisite must remain
ahead of it. Later enable/reload paths may need reinstallation after the
vanilla selector returns. These are design obligations, not tested guarantees.

**SOURCE-VERIFIED serialization path; HYPOTHESIS for an actual editor round
trip:** `111 Mod.lua:973-993` saves generated `ModDef` metadata through the
property serializer (`CommonLua/PropertyObject.lua:1444-1466`). `SetupEnv` is a
method, not a declared metadata property. An editor resave is expected to strip
handwritten bootstrap code; an actual save/package/upload inspection must
verify preservation if this route is ever chosen. This is an unsupported
runtime loader patch, considerably broader than fixing a vanilla gameplay
target or moving the normal saved preference.

A custom `LoadOptions` instance method is another **HYPOTHESIS** for touching
`ModsLoaded` before code (`111 Mod.lua:2157-2164`), but it would change the array
currently being traversed for options. It was not implemented or measured; the
selector wrapper is the stronger first-cold-load lead. The `ModsReloading`
message alternative was ruled out for cold boot by its `not first_load` guard.

## Lever inventory

The evidence labels belong to the stated mechanism; proposed product behavior
is not thereby retail-tested.

| Lever | Verdict / reach | Player cost and risks |
|---|---|---|
| Controlled enable sequence: pack first, then content mods | **SOURCE-VERIFIED.** Native normal-branch ordering; requires the pack to have no earlier prerequisite. | Setup work and cold restart; display sort is no confirmation. Re-enabling only the pack moves it last. Disable/re-enable others or rebuild the enabled sequence to move the pack first. |
| Pack promotes its saved seed through public helpers | **MEASURED desk + SOURCE-VERIFIED; retail persistence HYPOTHESIS.** Next cold boot, normal mode. | Potential single restart; changes a player preference and needs clear ownership, persistence handling and reversibility. Cannot repair the already-running order. |
| Content mod declares pack as required `ModDependency` | **MEASURED desk + SOURCE-VERIFIED.** Orders the pair in either seed mode. | Author cooperation; makes pack installation/enabling/version compatibility a prerequisite for that content mod. Does not order unrelated mods. |
| Content mod declares pack optional | **MEASURED desk, problematic.** Present dependency moves first, but the current DFS mishandles missing/disabled cases as described above. | Avoid assuming harmless absence; requires retail controls and resolution of loader behavior before recommending. |
| Pack declares content mods as dependencies | **SOURCE-VERIFIED; opposite direction.** Content mods would run before the pack. | Adds unwanted prerequisites and does not meet the objective. |
| Priority/load-before property, display name, code filename, folder or Workshop ID | **SOURCE-VERIFIED scope: no such priority input in the traced native selector/DFS.** Renaming `00_Core.lua` only orders pack files. | Renaming the persistent internal mod ID disrupts identity and references; title/folder changes do not implement normal-branch priority. |
| `LoadAllMods` plus a lexically early internal ID | **SOURCE-VERIFIED + MEASURED mode control.** Can precede current other IDs if no prerequisite precedes it. | Enables the all-mods mode and changes expected selection; no reserved earliest ID; identity migration cost. Saved enable-order promotion does not control this branch. |
| Inspect `ModsLoaded` and choose a fallback | **SOURCE-VERIFIED.** Complete positions are visible when pack code starts. | No reorder or restart by itself; diagnostics/fallback must be specific enough to avoid unnecessary warnings. |
| Change `ModsLoaded` from the pack's ordinary code | **SOURCE-VERIFIED deduction.** Too late for preceding code; mutates the array currently traversed by `ModsLoadCode`. | Can skip/repeat mod execution and desynchronize code/items. Not a first-load solution. |
| `ModsReloading(queue)` hook from previously loaded code | **SOURCE-VERIFIED.** Mutable queue on the hot path only, after the order-insensitive early-return gate. | Cannot guarantee first cold load; disappears/re-registers with Lua lifecycle. |
| Custom metadata `SetupEnv` wrapping the selector | **MEASURED desk; SOURCE-VERIFIED timing; native/retail capability HYPOTHESIS.** Prototype intervenes before code under native-object shims; could cover the first cold load and either seed mode. | Global loader patch, disabled-definition side effects, reinstallation/idempotence and dependency preservation; editor resave may strip it. |
| Options, entities, item scripts, a “load-first” companion or library | **SOURCE-VERIFIED for ordinary paths.** Options data/entities do not grant an ordinary code turn; item code runs later; a companion is another mod requiring its own position. | Extra install/dependency or altered lifecycle, without an automatic global guarantee. Special metadata callbacks are a separate lever above. |
| Steam Workshop “required items” | **SOURCE-VERIFIED platform scope.** Valve describes ordinary item dependencies as soft web/API relations; no Lua-order guarantee follows. | Subscription/install convenience; still needs native `ModDependency` or enabled-order handling. |
| Paradox Mods requirements / playsets | **SOURCE-VERIFIED game Lua; native SDK ordering unproven.** Required native dependencies export to the backend; enable/sync calls feed the native enabled list. | Backend selection/sync is not an established user reorder control for this title. Other Paradox games' launcher behavior is not evidence here. |
| Edit account state with a privileged console/external utility | **SOURCE-VERIFIED destination, end-to-end tooling HYPOTHESIS.** The seed is account storage; the account save is a packaged/encrypted table, not a supported plain text order file (`111 CommonLua/AccountStorage.lua:45-58,105-108`). | Manual technical work, backup and restart; platform access differs. Public helper route is narrower than inventing an account-file editor. |
| Engine-supported priority or official loader change | **HYPOTHESIS, requires game developer work.** The selector/queue is the correct insertion point for an explicit order feature. | Best first-launch authority if shipped; outside the mod author's control. |
| External preloader, patched Lua pack, native injection or DLC-style bootstrap | **HYPOTHESIS, not implemented or retail-tested.** Earlier execution could control the queue. | Installation/update/platform burden; game-file replacement conflicts with this pack's contract. No claim that hidden native hooks are impossible. |
| Resolve class declarations directly / apply at an appropriate later phase | **SOURCE-VERIFIED + targeted desk controls.** Can remove a transient-global dependency without changing overall order. | Per-fix design, inheritance and conflict checks; does not meet the broader “all repairs before content edits” objective by itself. |

## Platforms and prior art

**SOURCE-VERIFIED, primary mod source:** ChoGGi's Expanded Cheat Menu declares
`ChoGGi_Library` as a native dependency; the library's ID matches. At commit
`36e8e82cd08372e14b241eac38b163f23c764129`, both metadata files target original
Surviving Mars (`lua_revision=1007000`), with the Relaunched revision commented
out. This is dependency-pattern prior art, not proof of a tested Relaunched
bootstrap. [Menu metadata](https://github.com/ChoGGi/SurvivingMars_Mods/blob/36e8e82cd08372e14b241eac38b163f23c764129/Expanded%20Cheat%20Menu/metadata.lua),
[library metadata](https://github.com/ChoGGi/SurvivingMars_Mods/blob/36e8e82cd08372e14b241eac38b163f23c764129/ChoGGi%27s%20Library/metadata.lua).

**SOURCE-VERIFIED:** Valve's `ISteamUGC::AddDependency` does not itself promise
game load ordering. The 111 Steam discovery/uploader paths
(`CommonLua/Platforms/steam/SteamMods.lua:13-28`,
`CommonLua/Platforms/steam/SteamWorkshop.lua:107-119`) find Workshop content
and publish fields, not a priority consumed by `GetLoadingQueue`.
[Valve's API documentation](https://partner.steamgames.com/doc/api/isteamugc#AddDependency).

**SOURCE-VERIFIED, 111:** Paradox publishing includes installed **required**
native dependencies as `ModDependencies`
(`CommonLua/Libs/Paradox/ParadoxMods.lua:117-127,148-164`). The manager enables
native IDs via `TurnModOn` alongside calls for `Pdx.DefaultPlaysetId`
(`CommonLua/UI/ModManager.lua:1544-1565,1939-1952`). These paths establish
enabled-state integration, not an independent priority override. Paradox's
[Cities: Skylines II playset description](https://www.paradoxinteractive.com/zh-CN/games/cities-skylines-ii/modding/dev-diary-1-paradox-mods)
describes another game's integration; its capabilities were not imported into
this report's conclusions about Relaunched.

**MEASURED, named local sample:** the inventory instrument decodes and lists
each metadata file before searching for literal `dependencies`, with title and
internal-ID positive controls. Archived package members are `3675370940`,
`3676027320`, `3717125029`, `3730839706`, `3745475097`, `3775120166`; installed
members are `3607071753` (Passage Network), `3787202810` (this pack),
`3799500849` (Linux workaround). None of these decoded metadata files contains
that literal field. The output reconciles file members and positive controls;
it is not a census of public Workshop mods. Installed Passage Network's code
matches the archived 1.38 text after newline normalization.

## Passage Network worked example and alternatives

**SOURCE-VERIFIED:** Passage Network's archived `:45-51` defines global `Dome`
functions after adding methods to the original declaration at `:8-14`.
111 `Mod.lua:1570-1576` forwards ordinary global writes to real `_G`.
111 `CommonLua/Core/classes.lua:58-74` keeps the declaration separately;
`:1436-1438` restores the built class global before `ClassesBuilt`.

**MEASURED, desk:** the pack control loads the pinned real core and whole
VacuumWalks module. It executes the extracted offending PN definitions and
the shipped `StartShuttleLeg` probe target. Unused target functions/constants
are declared fixtures; it does not execute all of PN, the engine class builder
or the warning dialog. Results:

| Sequence | Observed result |
|---|---|
| Pack, then PN definitions | `VacuumWalks=active`; PN subsequently changes the global to a function. |
| PN definitions, then pack | `VacuumWalks=inactive`, `update_suspect=true`; `UpdateSuspects()` returns `VacuumWalks`. |
| Restore the global and fire `ClassesBuilt` after that decline | Status stays inactive: no automatic retry was registered for this fix. |
| Restore the global before the module's first application | Active and absent from `UpdateSuspects()`. This tests timing, not a production deferred implementation. |

The decline text blames missing work-slot/shuttle helpers even though the
fixture retains them and only the global `Dome` reference was replaced. This
is sufficient for the core's warning list; `00_Core.lua:628-647,667-694` routes
that list to the startup report. The current dialog itself already mentions
another mod as one possible cause, so “it claims only a game update” would be
an overstatement.

**MEASURED, existing retail log:**
[`reporter_TheGodUncle_modson_Mars.exe-20260924-13.07.16-6aad2d75.log`](../../archive/logs/reporter_TheGodUncle_modson_Mars.exe-20260924-13.07.16-6aad2d75.log)
has Lua revision `405907` at line 51, `VacuumWalks: applied` at line 95 and the
loaded order at line **186**, not 136:
`TestKit, TrainHubDev, FixPack, OptInPack, RailShaftDev, iooW34Y` (labels
shortened here; raw IDs remain in the log). Thus **pack before PN**, not pack
first overall. The reported v19 reversed-order warning still needs the planned
owner sitting; this report did not manufacture a new live reproduction.

**SOURCE-VERIFIED + MEASURED alternative:**
`111 CommonLua/Core/classes.lua:1265-1292`, `ProcessClassdefChildren`, passes
the retained declaration to a callback before rebuilding. The desk control
recovers the intact `Dome` declaration and its `ReserveWorkplace` while the
global remains a function. The helper is not excluded by the inspected 111
blacklist or its Steam/Paradox prefix additions. A narrowly changed guard could
use that declaring table without restoring someone else's global. Whether
that is the preferred pack behavior is **HYPOTHESIS/design choice**, requiring
both orders, cold/hot reload and relevant target-shape regression checks. This
is specifically a pre-build lookup: `classdefs` becomes nil at `:1442`, so it
is not a general runtime lookup or a reason to retain old class declarations
across reloads.

**MEASURED warning against a blanket late-apply change:** the shipped
`111 CommonLua/Core/classes.lua:980-1061` copies inherited members into built
classes. A fixture using that real resolver produced `Parent=new, Child=old`
after a post-build parent-method replacement. Moving all fixes to
`ClassesBuilt` can therefore miss inherited copies and reverse deference by
wrapping content mods after their file-scope changes. A targeted
`ClassesGenerate`/`ClassesPreprocess` design can access declarations before
flattening (`:1345-1352`), but still runs after ordinary mod code and is not a
substitute for first file execution.

## What first improves, and what it cannot promise

| Conflict shape | Assessment |
|---|---|
| Content mod wraps a function repaired at pack file scope | **SOURCE-VERIFIED deduction:** it captures the repair and controls the outer behavior. This is the desired default. |
| Content mod fully replaces that function | **SOURCE-VERIFIED deduction:** its replacement wins; the pack's repair may disappear. That is consistent with the owner's stated precedence, not evidence the repair still operates. |
| Earlier mod temporarily clobbers a class global | **MEASURED:** first avoids the demonstrated VacuumWalks guard failure. A targeted canonical-declaration lookup could solve that guard independently. |
| Two noncommuting wrappers, captured old references, or incompatible assumptions | **SOURCE-VERIFIED deduction:** sequencing selects a composition; it does not prove that composition correct. Specific targets still require compatibility analysis. |
| Deferred data repairs versus a content mod's earlier data edit | **SOURCE-VERIFIED:** first file load does not imply first data write. Pack `00_Core.lua:399-456` waits for classes/data and can re-run on `DataChanged`. |
| A later mod wants to veto an immediate pack repair using `SMRFixPack_Disabled` | **MEASURED:** a veto set before registration disables VacuumWalks; the same flag set after successful installation does not undo it. Pack-first therefore requires a compatible veto/stand-down arrangement where that interface is needed. Source: `00_Core.lua:549-559`. |
| A content mod has an independent defect or overwrites a global again later | **SOURCE-VERIFIED deduction:** first position cannot correct arbitrary later code. The pack's vanilla-only scope is preserved by declining or yielding where appropriate. |

## Recommendation

Treat **vanilla repairs first, content changes afterward** as the intended
compatibility order. The owner's premise is sound for immediate repairs; the
report's limits concern how to deliver it reliably and how far its protection
extends.

The next-build candidate is a deliberate saved-order feature using the tested
public helpers, with its initial-launch limitation stated plainly. Before
choosing it, complete the retail persistence/restart/sync controls described
above. If first-launch priority is essential, evaluate the metadata bootstrap
as a separate, explicitly broader loader change, with packaged cold/hot and
editor-round-trip controls. Cooperative native
dependencies are useful for specific authors, but the optional-dependency
trap makes them unsuitable as an untested universal recommendation.

For the immediate Passage Network report, finish the already-planned reversed
order observation, then choose between earlier pack execution and the narrow
canonical-declaration guard. Do not globally move function patches to
`ClassesBuilt`: it loses the desired timing and has a measured inheritance
hazard. Keep per-fix deference and accurate conflict diagnostics even if first
position becomes the default. Claude review and the owner's implementation
decision are the remaining actions reserved by the task; no entry changes or
production feature are included here.
