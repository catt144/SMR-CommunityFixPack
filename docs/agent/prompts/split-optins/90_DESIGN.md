# 90_DESIGN — the opt-in split, mapped before anything moves

Chain `split-optins`, prompt 1 (design). Written 2026-08-12, game closed, no
code moved. **Everything here is a claim** (chain rule 3); every load-bearing
one carries the file:line or command it came from so prompt 2 can re-derive it.
Numbers were re-derived from the tree, not inherited — §0 lists where the
inherited ones were wrong.

Staleness: `git log --oneline -10` + `git pull` → *Already up to date*, HEAD
`7efe1dd`, working tree clean. TestKit `C:\Dev\SMR-BugFixPack-TestKit` HEAD
`d8e1fbf`, tree clean.

---

## §0 — corrections to inherited claims (rule 3, applied to this chain's own README)

| claim (source) | verdict | derived value |
|---|---|---|
| `00_Core.lua` is 504 lines (chain README) | **wrong** | **527** (`wc -l`) |
| "the 74 Fix files" (prompt 1 job 1) | **misleading** | there are **73** `Code/Fix_*.lua`. The **74** is *registered fix-pack modules* = 73 `Fix_*` + `90_SaveSanitizer.lua`. README invariant 6e's arithmetic (74 registered / 75 `Code/*.lua`) is **right**; only prompt 1's phrasing is off |
| Core usage counts `IsActive ×13 · Register ×8 · OptionEnabled ×7 · SetGlobal ×5 · ListFixes ×5 · Require ×5 · WhenActive ×3 · fixes ×3 · OnDataReady ×2 · Log ×1` | **reproduced exactly** — but they are **raw text counts including comments** | executable-only counts differ materially: `ListFixes` is **0** executable uses (5 comment mentions); `IsActive` is **7** files / 7 call sites, and **`Opt_MultipleSuns` does not call it at all** (it reads `SMRFixPack.fixes[FIX_ID].status` directly, `Opt_MultipleSuns.lua:72-75`); `OnDataReady` 1; `Log` 1 |
| `items.lua` header: "then the six `Opt_` in their current order" (`items.lua:38`) | **stale** | there are **8** `Opt_` `ModItemCode` entries |
| `docs/README.md` prose: "116 entry files", "43 fact files", "151 index rows" | **stale** (doccheck parses only the fenced map, so it does not catch this) | **125** entry files / **160** rows (`bugs/INDEX.md:4`), **53** fact files |
| TestKit `OptionsMenu` probe asserts "6 toggles" | **incomplete** | there are **7** `ModItemOptionToggle`s; `NoHomeless` is absent from the probe's `WANT` list (`60_Probes_Opt.lua:879-880`) |
| chain README + prompt 4 predict cell (a) opt-in gate reads **`8/8`** | ⛔ **wrong, and it matters** | at fresh account defaults the opt-in gate reads **`1/8`** — see §6.2. `8/8` is only reachable after an explicit activation |

Everything else in the README reproduced.

---

## §1 — JOB 1: the authoritative coupling map

### 1.1 Method

Patch primitives were derived from `00_Core.lua` first, then grepped for across
all 83 `Code/*.lua`:

| primitive | Core site | how it is found |
|---|---|---|
| global replacement | `SMRFixPack.SetGlobal` (`00_Core.lua:169-174`) — plain `_G[name] = value` + rawget read-back | `grep "SetGlobal("` |
| class-method wrap | no Core helper — sites capture `local orig = C.M` then `function C:M(...)` | `function <sym>[:.]<method>` with local-alias resolution (script in scratchpad `patchmap.py`) |
| preset/template data write | `SMRFixPack.DataPatch` (`:241`) / `OnDataReady` (`:330`) drive them; the write itself is a plain field assignment | `grep "BuildingTemplates\|Presets\|TechDef"` |
| label modifier | vanilla `LabelContainer:SetLabelModifier`, keyed by a string id | `grep "SetLabelModifier"` |
| additive message handler | `OnMsg.X = fn` — **not** a patch point (the engine appends handlers; `WhenActive` `:180` exists to gate them) | `grep "OnMsg\."` |
| object-field write | plain `obj[FLAG] = …` — save contract, see §2 | `grep "SMRFixPack_"` |

Not patch primitives, confirmed: `Require` (`:114`, validation only, writes
nothing), `Register` (`:378`, registry only), `IsActive`/`OptionEnabled`
(reads), `Log` (`:26`).

### 1.2 Per-module symbol table (executable uses only; comments excluded)

`Reg` = `Register`, `OE` = `OptionEnabled`, `IA` = `IsActive`, `Req` =
`Require`, `SG` = `SetGlobal`, `WA` = `WhenActive`, `ODR` = `OnDataReady`,
`fx` = direct `SMRFixPack.fixes` read, `Opt`/`Dis` = the two pre-load config
globals.

| module | Reg | OE | IA | Req | SG | WA | ODR | Log | fx | Opt | Dis | module-owned public surface |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `Opt_ClassicRockets` | 1 | 1 | 1 | 1 | – | – | – | – | – | ✓ | – | – |
| `Opt_AcknowledgedWarnings` | 1 | 1 | 1 | 1 | **3** | – | – | – | – | ✓ | – | – |
| `Opt_ResidencyControl` | 1 | 1 | 1 | 1 | 1 | – | – | – | – | ✓ | – | – |
| `Opt_MultipleSuns` | 1 | 1 | – | – | – | 1 | 1 | 1 | **3** | ✓ | – | – |
| `Opt_DroneOverhaul` | 1 | 1 | 1 | – | – | – | – | – | – | ✓ | – | `DroneReport`, `DroneOverhaulStats` |
| `Opt_CohortHousing` | 1 | 1 | 1 | 1 | – | 1 | – | – | – | ✓ | – | – |
| `Opt_NoHomeless` | 1 | 1 | 1 | 1 | 1 | 1 | – | – | – | ✓ | 1 | – |
| `Opt_DroneStatDials` | 1 | – | 1 | – | – | – | – | – | – | – | **3** | – |
| **totals** | **8** | **7** | **7** | **5** | **5** | **3** | **1** | **1** | **3** | 7 | 4 | 2 |

Two consequences the raw counts hid:

* ⚠️ **`Opt_MultipleSuns` reads `SMRFixPack.fixes` directly** (`:73-74`,
  `:157`, `:164`) instead of `IsActive`. The ported copy must keep that
  shape — it is the same registry object under a new name, but a "just call
  IsActive" tidy-up would be a behaviour edit (invariant 6d).
* `ListFixes`, `PackVersion`, `DataPatch`, `UpdateSuspects` have **zero**
  executable uses in the 8 modules. `PackVersion` and `DataPatch` are used
  only by `Fix_*` files (`Fix_MeteorFrequency.lua:171`,
  `Fix_RainsDeadlock.lua:175`; 9 `DataPatch` sites, all `Fix_*`).

### 1.3 Core port-disposition table

| Core symbol | site | used by the 8? | disposition |
|---|---|---|---|
| `SMRFixPack` table (`fixes`/`order`/`defs`) | `:17-22` | yes (all) | **COPY** → `SMROptInPack` |
| `SMRFixPack_Disabled` | `:11` | `DroneStatDials`, `NoHomeless` | **COPY** → `SMROptInPack_Disabled` (runtime-only, safe to rename — §2.3) |
| `SMRFixPack_Optional` | `:15` | 7 files | **COPY** → `SMROptInPack_Optional` (runtime-only) |
| `Log` | `:26-33` | `MultipleSuns` + Core internals | **ADAPT**: prefix `[CommunityFixPack]` → `[CommunityOptInPack]`. The `%%` double-escape comment stays verbatim |
| `IsActive` | `:39-42` | 7 | **COPY** verbatim |
| `OptionEnabled` | `:51-55` | 7 | **COPY** verbatim (reads `CurrentModOptions`, which is per-mod-env — no id inside) |
| `PackVersion` | `:62-68` | no | **COPY** + adapt the id literal `"SMR_CommunityFixPack"` → new id. Kept unused: see §1.5 |
| `find_declaring_ancestor` | `:79-94` | via `Require` | **COPY** verbatim |
| `Require` | `:114-163` | 5 | **COPY** verbatim (its FIX_POLICY §2 log line names no mod) |
| `SetGlobal` | `:169-174` | 3 | **COPY** verbatim |
| `WhenActive` | `:180-188` | 3 | **ADAPT**: reads `rawget(_G,"SMRFixPack_Disabled")` → new name |
| `DataPatch` | `:241-319` | no | **COPY** verbatim (unused; §1.5) |
| `OnDataReady` | `:330-346` | `MultipleSuns` | **COPY** verbatim |
| `run_apply` | `:350-366` | via `Register` | **COPY** verbatim |
| `Register` | `:378-391` | 8 | **COPY** verbatim |
| `OnMsg.ApplyModOptions` | `:400-449` | the live-toggle contract | ⛔ **ADAPT**: `if mod_id ~= "SMR_CommunityFixPack" then return end` (`:401`) → new id. **This is the single line that, if missed, silently kills every live toggle in the new mod** |
| `UpdateSuspects` | `:459-479` | Core's own dialog | **COPY** verbatim |
| C1 dialog thread | `:498-516` | player surface | **ADAPT**: `Untranslated("Community Fix Pack")` and the body text name the mod → new display name. See §1.6 hazard 3 |
| `ListFixes` | `:519-527` | console + 5 doc references | **COPY** verbatim |

**Ruling — copy `00_Core.lua` WHOLE rather than trimming to the used surface.**
Cost is ~90 lines of currently-unreachable framework (`DataPatch`,
`PackVersion`). Bought: (a) minimum diff = minimum risk, the chain's whole
posture; (b) a future opt module gets the same scaffold with the same F75/F87/B3
lessons baked in, instead of re-learning them; (c) prompt 5's byte-compare
becomes a mechanical diff of two files that should differ ONLY in the namespace
lines listed above — an auditable acceptance test rather than a judgement call;
(d) a game update that changes the engine facts the two copies encode changes
both identically. **Rejected alternative:** trim to the used surface — saves
nothing that matters and makes (c) impossible.

### 1.4 ⛔ The disjointness proof — and it does NOT come out clean

Complete enumeration of vanilla patch points (class-method wraps + `SetGlobal`
+ preset writes), both sets:

**Fix-pack set — global replacements (13 sites, 12 files):** `TriggerCaveIn`,
`FindCaveInLocation`, `PlanetaryAsteroidVisitPossible`, `WaitBombard`,
`OverrideDisasterDescriptor`, `GetDustDevilsDescr`, `GetRareTraitChance`,
`GetGridGlobalStorage`, `GetDisasterWarningTime`, `CompleteMilestone`,
`RainsDisasterActivation`, `IsLRTransportAvailable`, `ExpandTrackFromElement`.
**Opt set — global replacements (5 sites, 3 files):** `SuppressNotification`,
`AddObjectToNotification`, `RemoveObjectFromNotification` (all
`Opt_AcknowledgedWarnings`), `ChooseDome` (`Opt_ResidencyControl:228` **and**
`Opt_NoHomeless:906`).
⇒ **Global-replacement intersection: EMPTY.**

**Class-method wraps.** 47 sites in the fix-pack set, 9 in the Opt set (full
list in the scratchpad run; per-file resolution is reproducible with the alias
script). Intersections:

| site | fix pack | opt-in | verdict |
|---|---|---|---|
| `Colonist:Idle` | `Fix_ArrivalDeaths:171` + `Fix_ShelterReflex:58` | – | intra-set |
| `TrackBase:*` | 4 fix files | – | intra-set |
| `Colonist:FindEmigrationDome` | – | `Opt_CohortHousing:168` + `Opt_NoHomeless:449` | **intra-Opt** — moves together |
| `sectionDome:Init`, `sectionMicroGHabitat:Init` | – | `Opt_ResidencyControl:237/245` + `Opt_NoHomeless:911/919` | **intra-Opt** |
| `ChooseDome` | – | `Opt_ResidencyControl` + `Opt_NoHomeless` | **intra-Opt** |
| ⛔ **`UniversalRocketBase:GetFuelResourceRequest`** | `Fix_LanderReturnFuel:38` | `Opt_ClassicRockets:81` | **CROSS-SET** |
| ⛔ **`Drone:CleanUnreachables`** | `Fix_DroneUnreachableForever:80` | `Opt_DroneOverhaul:220` | **CROSS-SET** |

**Preset/label writes.** Opt side: `BuildingTemplates.ArtificialSun.build_once`
(`Opt_MultipleSuns:168/184`) and two `UIColony` label modifiers
(`SMRFixPack_DroneSpeedDial` on label `Drone`, `SMRFixPack_DroneCarryDial` on
label `Consts`, `Opt_DroneStatDials:128-137`). Fix side touches
`BuildingTemplates` only for `Sinkhole` (`Fix_SinkholeIndestructible:97`) and
`entry.template` lookups (`Fix_LayoutTechLock:73`, read-only), and its label
modifiers are on `WindTurbine*` (`90_SaveSanitizer:84`), trait labels
(`Fix_SaintBlessing:168`) and colony labels keyed by effect object
(`Fix_AstrogeologistExtractors:204`). ⇒ **empty intersection.**
Specifically answering the prompt's SaveSanitizer question: **no.**
`sweep_leaked_upgrade_modifiers` matches ids against
`^(%d+)_upgrade%d+_mod_%d+$` (`90_SaveSanitizer.lua:117`) — the dial ids start
with a letter and can never match; `repair_turbine_buff` only walks
`label_modifiers[label]` for the three `WindTurbine*` labels the tech names
(`:64-70`) and only compares `mod.prop == "electricity_production"`. The dials
live on `Drone`/`Consts` with props `move_speed`/`DroneResourceCarryAmount`.
Disjoint on both axes.

#### 1.4a RULING on the two cross-set sites — NOT a chain stop, and why

The README's stop condition is *"shared state that **cannot be duplicated** (a
vanilla patch point both mods would own …)"*. A chained wrapper is not shared
state and both mods **can** own it — that is the pack's founding design goal
(`00_Core.lua:4-6`: *"fixes prefer wrapping/chaining originals over
replacement, so other mods that hook the same functions keep working"*). Both
sites already coexist today **inside one mod** and are shipped. The split
changes one thing: wrap order stops being decided by the `metadata.lua` `code`
list and starts being decided by engine mod-load order. So the question that
actually decides this is **order-independence**, and both sites are
order-independent:

**Site 1 — `UniversalRocketBase:GetFuelResourceRequest`.** The two conditions
are mutually exclusive on the departure-location type:
F69 fires on `not arrival_loc and RocketType == LanderRocket and
GetDepartureLocType() == "asteroid"` (`Fix_LanderReturnFuel.lua:42-43`);
D01 fires on `(amount or 0) <= 0 and IsActive and not arrival_loc and
IsPlayerControlled() and GetDepartureLocType() == "our_colony"`
(`Opt_ClassicRockets.lua:87-90`). `"asteroid" ≠ "our_colony"`, so at most one
body ever acts, in either nesting order, and the other is a pass-through.
⚠️ **One residual asymmetry, and it is QA's to rule on**: F69's wrapper is
declared `function R:GetFuelResourceRequest()` with **no varargs** and calls
`orig(self)` (`:38`, `:47`), while D01's takes and forwards `...`. If the fix
pack loads *after* the opt-in mod, F69 wraps D01 and drops any extra argument.
This is inert **iff** the shipped `GetFuelResourceRequest`
(`UniversalRocket.lua:1639-1650`) and all its callers pass no arguments —
believed true (both wrappers' headers describe it as argument-free, and
`CargoTransporterNew.lua:1249-1265` calls `self:GetFuelResourceRequest()`), but
it is a **Src claim this session did not open the file to confirm**. Prompt 2
must confirm it against Src; if it is false, the build fixes it by giving F69
`(...)`/`orig(self, ...)` — which is a **fix-pack-side** edit and therefore
outside invariant 6d's freeze on module behaviour.

**Site 2 — `Drone:CleanUnreachables`.** F55 is a **pre**-wrapper (normalise
poisoned `unreachable_buildings` stamps, then `orig_clean`,
`Fix_DroneUnreachableForever.lua:80-94`); D06 is a **post**-wrapper (`orig_clean`
first, then the moonlight scan, gated `self.command == "Idle"`,
`Opt_DroneOverhaul.lua:220-271`). Either nesting produces the same execution
sequence — normalise → vanilla expiry → moonlight — because each wrapper puts
its own work strictly on one side of the call it forwards. The moonlight scan
reads `self.unreachable_buildings` (`:248`) and therefore sees normalised
stamps in both orders. Save-safety is unaffected: both frames sit inside
`Drone:CleanUnreachables`, which `tools/blocking_analysis.py` reports `clear`
(cited by both files' headers, F86 Tier 2).

⇒ **Recorded as invariant 6b's evidence: the strict disjointness claim is
FALSE (2 cross-set sites), and the weaker property that actually protects the
split — order-independent chained composition — HOLDS at both.** Prompt 2 is
asked to attack this ruling first; prompt 4 must exercise both sites in cell
(a) (§6.2). It is **not** routed to the owner as a decision: nothing about
today's behaviour changes, and no owner input would alter the answer.

### 1.5 Cross-mod runtime dependencies (the other half of the stop condition)

One found, and it is a **consumer** relationship, not a patch collision:
`Fix_ShuttleHubOffAvailable.lua:68` **replaces the global**
`IsLRTransportAvailable`; `Opt_CohortHousing` (`:137`, `:191`) and
`Opt_NoHomeless` (`:832`, `:562`) **call and `Require`** it. Consequence, stated
so nobody discovers it in a log: **with the fix pack absent, the opt-in mod
calls vanilla's `IsLRTransportAvailable`; with it present, it calls the fixed
one.** That is true today too (the fix is independently vetoable), it changes
no interface, and it is exactly the composition the owner wants. Recorded, not
repaired. No `Require` breaks: every Opt `Require` target is a **vanilla**
name — confirmed by reading all five `Require` blocks; not one names a
`SMRFixPack` symbol.

### 1.6 Both-installed hazards (invariant 6b, beyond patch points)

1. **Global namespace.** The 8 modules create exactly three global names
   (`SMRFixPack_Optional`, `SMRFixPack_Disabled` — both renamed — and the flag
   fields, which are object members, not globals). `grep "^function [A-Za-z_]"`
   over the Opt files returns only `SMRFixPack.DroneReport` and the two
   forward-declared locals in `Opt_MultipleSuns` (`lift_build_limit`,
   `restore_build_limit`, both `local` at `:114`). **No bare global function is
   defined by any module.** ⇒ zero collision after the two renames.
2. **Two boot log streams.** Prefixes `[CommunityFixPack]` vs
   `[CommunityOptInPack]`. ⚠️ Neither string is a substring of the other, so
   `grep CommunityFixPack` stays clean in cell (b) — but `grep "Pack]"` matches
   both. **Every log grep in prompts 4/5 must use the full bracketed token.**
3. **Two C1 dialogs.** Each Core copy runs its own 5-minute polling
   `CreateRealTimeThread` (`00_Core.lua:498`) and can raise its own
   `WaitMessage`. With both mods installed and both having suspects, the player
   sees two sequential modals. Reachable only under patch rot. **Kept
   (behaviour-conservative); the new copy's text must name the opt-in mod so
   the two are distinguishable.**
4. **Two `OnMsg.ApplyModOptions` handlers**, each id-guarded. Additive by
   engine design; each early-returns on the other's `mod_id`. Note there are
   already **two** in the fix pack today (`00_Core.lua:400` and
   `Opt_DroneStatDials.lua:142`) — the second moves with its module and needs
   the same id edit.
5. **Load order between the two mods is not controlled by us.** Since §1.4a
   establishes order-independence, this is acceptable — but prompt 4 must
   **record the observed order** from the boot log so a future change has a
   datum instead of an assumption.

---

## §2 — JOB 2: the persisted-name inventory (invariant 6c evidence)

### 2.1 The inventory — every string the 8 modules can put into a save or account storage

| # | exact bytes | kind | written at | read at | disposition |
|---|---|---|---|---|---|
| 1 | `SMRFixPack_ack_notworking` | field on `Building` objects | `Opt_AcknowledgedWarnings.lua:105` (`obj[FLAG] = true`), cleared `:127` | `:115`, `:125` | ⛔ **KEEPS EXACT BYTES** |
| 2 | `SMRFixPack_closed_to_new_residents` | field on `Dome`/`MicroGHabitatBase` | `Opt_ResidencyControl.lua:135` via `building:TogglePolicy(FLAG, broadcast)` → shipped `Community:SetPolicyState` | `:74`, `:89` | ⛔ **KEEPS EXACT BYTES** |
| 3 | `SMRFixPack_no_homeless` | field on `Dome`/`MicroGHabitatBase` | `Opt_NoHomeless.lua:735` (`TogglePolicy`) and `:730` (`SetPolicyState`, the bespoke broadcast) | `:227`, `:484`, `:511`, `:565`, `:714`, `:729` | ⛔ **KEEPS EXACT BYTES** |
| 4 | `SMRFixPack_DroneSpeedDial` | **label-modifier id** in `UIColony.label_modifiers["Drone"]`, holding a vanilla `Modifier` object | `Opt_DroneStatDials.lua:128` | `:128` (replace/remove by id) | ⛔ **KEEPS EXACT BYTES** — the hardest one: the object is vanilla, only the key is ours, so a rename orphans a live boost permanently |
| 5 | `SMRFixPack_DroneCarryDial` | as above, label `Consts` | `:133` | `:133` | ⛔ **KEEPS EXACT BYTES** |
| 6 | `"1x (base)"` `"2x"` `"3x"` `"5x"` | dial choice values (account storage + the maps that decode them) | `metadata.lua:46`, `items.lua` `ChoiceList`, `Opt_DroneStatDials.lua:72` | `:107` | ⛔ **KEEPS EXACT BYTES in all three places** |
| 7 | `"+0 (base)"` `"+1"` `"+2"` | as above | `metadata.lua:47`, `items.lua`, `Opt_DroneStatDials.lua:73` | `:107` | ⛔ **KEEPS EXACT BYTES in all three places** |
| 8 | `ClassicRockets` `AcknowledgedWarnings` `ResidencyControl` `MultipleSuns` `DroneOverhaul` `CohortHousing` `NoHomeless` | Mod-Options toggle keys **and** `Register` ids | `metadata.lua:39-45`, `items.lua`, each module's `Register` | `OptionEnabled` (`00_Core.lua:54`) | **KEEP** (see §2.4 — the values reset regardless, but keeping the keys keeps every doc, probe and console line correct) |
| 9 | `DroneSpeedDial` `DroneCarryDial` | Mod-Options choice keys (**not** Register ids) | `metadata.lua:46-47`, `items.lua` | `Opt_DroneStatDials.lua:107` | **KEEP** |

**Provably never persisted** (cited): `SMRFixPack_Optional` /
`SMRFixPack_Disabled` — plain `_G` tables built with `rawget(_G,…) or {}` at
load, never written to an object, never in `PersistableGlobals`; the engine
persists declared globals and object members, and these are neither declared
nor attached. `Opt_DroneOverhaul`'s `strikes`/`cover_cache`/`hub_miss` — module
locals with `__mode = "k"` weak keys (`:115-118`), and its own header states
"all state … is transient module-local with weak keys; no flags on objects, no
GameVars, no long-lived threads". `Opt_MultipleSuns`' `we_lifted`/`data_loaded`
/`lifted_logged` — file locals; the `build_once` write is on a **preset**, which
is rebuilt from data every load (its header: "Savegame footprint: none").
`rawset(self, "ProcessToggle", …)` in both UI rows — written on an
`InfopanelActiveSection` **window instance**, not a game object.
**No thread names**: no `Opt_*` file creates a named thread; the only
`CreateRealTimeThread` in the framework is Core's unnamed C1 poller.
**No GameVars**: `grep "GameVar"` over the Opt files → zero hits.

### 2.2 History sweep — were any of these ever named something else?

```
git log --all -p -- Code/Opt_*.lua | grep -oE "SMRFixPack_[A-Za-z0-9_]+" | sort -u
```
returns exactly seven names across the whole history: the five persisted ones
above plus `SMRFixPack_Optional` and `SMRFixPack_Disabled`. The same sweep over
`git log --all -p -- Code/` returns eleven more, **all fix-pack-side**
(`SMRFixPack_F35_`, `SMRFixPack_F48_StationConnectors`,
`SMRFixPack_FirstAsteroidPrefabs`, `SMRFixPack_MeteorLatch`,
`SMRFixPack_fixed_loop`, `SMRFixPack_loop_version`, `SMRFixPack_payload_set`,
`SMRFixPack_reserved_at`, `SMRFixPack_rocket_fuel_key`,
`SMRFixPack_shelter_try`, `SMRFixPack_spawn_gate`) — none written by an Opt
module, none moving.
`git log --all -p` over `metadata.lua` shows the nine `default_options` keys and
the mod id `SMR_CommunityFixPack` have **never** had another value; over
`items.lua`, the nine option `name`s likewise; over the Opt files, the eight
`Register` ids likewise.
⇒ **No renamed id exists in any era of the owner's saves.** The owner's oldest
save and today's write the same bytes.

### 2.3 What the namespace rename may and may not touch

| string class | rename? | why |
|---|---|---|
| the global table `SMRFixPack` and every `SMRFixPack.<fn>` call | **YES** | runtime only; invariant 6a requires it |
| `SMRFixPack_Optional` → `SMROptInPack_Optional` | **YES** | never persisted (§2.1). ⚠️ documented in `PLAYTEST_HELP.md:499` — update |
| `SMRFixPack_Disabled` → `SMROptInPack_Disabled` | **YES** | never persisted. ⚠️ it is PT-62's documented A/B lever (`PLAYTEST_CHECKLIST.md:914`, `Opt_NoHomeless.lua:207-224`) — **the checklist and the module header both need the new name in the same commit**, or the next A/B leg silently runs with the module live, which is the exact PT-61 trap that header was written about |
| log prefix `[CommunityFixPack]` | **YES** → `[CommunityOptInPack]` | log text |
| the mod id `SMR_CommunityFixPack` (Core `:401`, `:64`; `Opt_DroneStatDials:143`) | **YES** → `SMR_CommunityOptInPack` | see §2.4 |
| rows 1–7 of §2.1 | ⛔ **NO** | save contract |
| rows 8–9 of §2.1 | **NO** (kept unchanged by choice) | §2.4 |

⚠️ **The engine permits creating `SMROptInPack*` as new globals** for the same
reason it permits `SMRFixPack*` today: `ModEnvMeta.__newindex`'s strict-global
assert (`Mod.lua:1556-1562`) is skipped while `Loading` is true, which it is
during `ModsLoadCode` (`autorun.lua:423`) — the mechanism the TestKit's
`96_AutoRunFlag.lua:8-11` documents. No new hazard.

### 2.4 ⚠️ The mod-id change: what it costs the owner, exactly

Mod Options values live in `AccountStorage.ModOptions` **keyed by mod id**, are
loaded before mod code, and are exposed per-mod-env as `CurrentModOptions`
(`Mod.lua:2128-2131`, cited at `00_Core.lua:46-50`; the per-mod-env point is
proven in the TestKit at `60_Probes_Opt.lua:773-778`). A new mod id is a new
key, so:

* the owner's seven toggles come up **OFF** and both dials at **base** on the
  first load of the new mod;
* the base dial values must read as **the base defaults, not nil** — they do,
  because the engine seeds `CurrentModOptions` from `default_options` before
  mod code loads (`ModDef:HasOptions` / seeding, `Mod.lua:473-475`, cited in
  `metadata.lua:32-37`), and `Opt_DroneStatDials.lua:107` falls back to `0` for
  an unknown value anyway — so **base is reached by two independent routes**;
* the stale entries under `SMR_CommunityFixPack` stay in account storage and
  become inert (the fix pack will no longer declare those names);
* **owner cost: one visit to Options → Mod Options, ~1 minute, once.** Already
  recorded on the checklist under item 15; no new decision is owed.

⭐ **And this is a prediction, not a miss** — §6.2's cell (a) and cell (d)
expected readings both assume it.

---

## §3 — JOB 3: the new repo, the namespace, and what the fix pack loses

### 3.1 Working names (owner may rename at launch prep — rule 9)

| thing | value |
|---|---|
| repo | `C:\Dev\SMR-OptInPack` (local git only — rule 9 forbids a remote unasked) |
| mod id | `SMR_CommunityOptInPack` |
| global | `SMROptInPack` (+ `SMROptInPack_Optional`, `SMROptInPack_Disabled`) |
| log prefix | `[CommunityOptInPack]` |
| junction | `%AppData%\Surviving Mars Relaunched\Mods\SMR-OptInPack` → the repo |
| display name | owner call at launch prep; build uses `"Community Opt-In Pack"` as a placeholder and marks every site |

### 3.2 Folder layout (mirrors this repo; doccheck's root allowlist is parsed from `docs/README.md`, so the map and the folder must agree)

```
C:\Dev\SMR-OptInPack\
  CLAUDE.md · LICENSE · README.md · metadata.lua · items.lua
  Code\  00_Core.lua + the 8 Opt_*.lua
  docs\  PLAYTEST_CHECKLIST.md? (see §5) · PLAYTEST_HELP.md? · FUTURE_IDEAS.md · README.md
         agent\ STATE.md · WORKFLOW.md · FIX_POLICY.md · PROVENANCE.md
                bugs\  D01 D02 D03 D04 D06 D07 D09 D12 + INDEX.md (generated)
                facts\ EF-001…EF-053 + INDEX.md + _preamble.md (copied whole)
                reports\ CHAIN_METHOD.md (+ DRONE_OVERHAUL_OPTIONS.md, see §5)
                prompts\
         archive\  (new, empty except SESSION_LOG.md — history stays in the fix pack)
  tools\ doccheck.py · split_bugs.py · split_facts.py · hooks\pre-commit
```

⚠️ **`docs/` root allowlist**: `check_root` (`doccheck.py:372-391`) compares
`os.listdir(docs)` against the names parsed out of `docs/README.md`'s **first
fenced block**, rows indented exactly two spaces. The new repo's map must list
exactly what it ships — and the three `STUBS` (`doccheck.py:55-59`) must be
**dropped from the ported checker**, not faked: they exist here to make
pre-restructure references resolve, and the new repo has no such history.
Faking them would be a lie the tool then enforces.

### 3.3 `metadata.lua` for the new mod

* `id` = `SMR_CommunityOptInPack`; `author` `catt144`; `version`/`version_major`
  /`version_minor` = `0`/`1`/`0` (pre-release; launch prep sets the ship value);
  `lua_revision` copied (`350453`).
* `optional_mod = true` — same rationale as the fix pack (`metadata.lua:16-18`):
  saves made with it load fine without it, so don't nag with the missing-mods
  prompt. ⚠️ True with one documented caveat that already exists and does not
  change: a **non-base D09 dial persists its boost** into a save loaded without
  the mod (`Opt_DroneStatDials.lua:46-52`) — the mod-page instruction "set both
  dials to base before uninstalling" moves to the new mod's description.
* `ignore_files` copied verbatim (it is what keeps `docs/` and `.claude/` out of
  the `.hpk`).
* `default_options` = **the same 9 keys with the same 9 values, byte-identical**
  to today's `metadata.lua:38-48`.
* `code` list, **in this exact order** (see §3.6):
  `00_Core.lua`, `Opt_ClassicRockets`, `Opt_AcknowledgedWarnings`,
  `Opt_ResidencyControl`, `Opt_MultipleSuns`, `Opt_DroneOverhaul`,
  `Opt_CohortHousing`, `Opt_NoHomeless`, `Opt_DroneStatDials`.

### 3.4 `items.lua` for the new mod

Nine `ModItemCode` entries **in `code`-list order** (the A3 rule: the Mod
Editor regenerates `metadata.lua`'s `code` solely from these,
`items.lua:31-39`), then the 7 `ModItemOptionToggle` and 2
`ModItemOptionChoice` entries moved **verbatim** — `name`, `DisplayName`,
`Help`, `DefaultValue`, `ChoiceList` unchanged. The file's header rules are
copied with the mod name adapted and the "six" → "seven/eight" arithmetic
corrected (§0).

### 3.5 What the fix pack loses (and what it must NOT lose)

| file | change |
|---|---|
| `Code/Opt_*.lua` ×8 | **deleted** |
| `metadata.lua` | delete `code` rows `126-133` **and their preceding comment line `125`**; delete the whole `default_options` block (`38-48`) — with no options the pack stops appearing in Options → Mod Options at all (`ModDef:HasOptions`, `Mod.lua:473-475`), which is correct and is a §6.2 cell (c) expected reading; update `description` / `short_description` / `last_changes` to stop advertising the modules (minimal truth edit; final wording belongs to launch prep, which already owns a wording item) |
| `items.lua` | delete the 8 `ModItemCode` `Opt_` entries, the 7 toggles and the 2 dials; adapt the header rules to say the pack has no options |
| `Code/00_Core.lua` | ⛔ **UNCHANGED.** The `optional` machinery (`Register`'s `def.optional`, the `ApplyModOptions` reconciler, `OptionEnabled`, `SMRFixPack_Optional`) becomes dormant, not wrong. Deleting it would be an unforced edit to the one file every remaining fix depends on |
| `tools/doccheck.py` | ⛔ **must change** — see §5.3 |
| `docs/` | see §5 |

**Derived post-split fix-pack counts** (predictions for prompt 3's
`--emit-counts` to confirm, never to retype — and ⛔ **only after §5.3's
`doccheck.py` repair, without which the emitted default-active reads 67**):
`Code/*.lua` **75** (73 `Fix_` + `00_Core` + `90_SaveSanitizer`); registered
modules **74**; `optional = true` files **0**; default-active **74**; index rows unchanged at 102 F + 12 D + 46 C
until the 8 entries move (§5.1), then **102 F + 4 D + 46 C** with 8 tombstone
rows — see §5.1 for which of the two shapes doccheck will accept.
**New-repo counts**: `Code/*.lua` **9**; registered **8**; `optional = true`
**7**; default-active **1**.

### 3.6 ⛔ Load order is a build requirement, not a nicety

`ModDef:LoadCode` iterates `ipairs(self.code)` and scans no directory
(`Mod.lua:490-521`, source-verified and quoted in `WORKFLOW.md:209-213`). So
order is the **list's** order, not the filename's. Two properties must survive:

1. `00_Core.lua` first — every module calls `SMRFixPack.Register` at file scope.
2. **The existing relative order of the 8** — because two intra-Opt shared sites
   are wrap-order-sensitive in principle: `Colonist:FindEmigrationDome`
   (`Opt_CohortHousing` then `Opt_NoHomeless`, so NoHomeless is outermost) and
   `ChooseDome` (`Opt_ResidencyControl` then `Opt_NoHomeless`). `Opt_NoHomeless`
   is written to be order-independent w.r.t. D07 (`:165-171`: it acts only when
   the composed answer is empty), but preserving the order is free and
   invariant 6d says behaviour does not change. **Preserve it.**

### 3.7 ⭐ RECOMMENDATION (owner call, non-blocking): the 8 stay **OFF by default**

The question: in a mod whose whole point is opting in, should the 7 toggles
default ON?

**Recommend: keep `DefaultValue = false` and `default_options = false`, and
keep both dials at base.** Reasons, in order of weight:

1. Flipping the default **is** a behaviour change at the mod level, and the
   chain's scope fence puts "ANY behaviour change to any module" out of scope.
   A default flip also breaks the byte-identical `default_options` the
   save/account contract in §2.1 rows 6–9 is built on.
2. Three of the eight are not "quality of life you'd want on": `DroneOverhaul`
   is labelled *experimental* on its own toggle (`items.lua`) and carries PT-52's
   freeze; `NoHomeless` moves colonists between domes and its overpopulation
   unwind is explicitly **unverified** (`Opt_NoHomeless.lua:29-30`);
   `CohortHousing` re-homes Seniors and Children. Default-ON ships those to
   everyone who installs.
3. `ResidencyControl` and `NoHomeless` add **infopanel rows**; default-ON puts
   two new rows on every dome panel unasked.
4. The Mod Options page is the product. Installing buys the *choice*; the page
   costs one visit, which the owner must make once anyway (§2.4).

**Counter-argument, recorded rather than buried:** every player who installs
this mod has already opted in once, so a second opt-in per module is friction,
and a default-ON build would make cell (a)'s gate read `8/8` without ceremony.
If the owner prefers ON, the change is two lines per module in `items.lua` +
`metadata.lua` and **nothing in `Code/`** — cheap to revisit after release, and
cheaper than shipping it on and pulling it back.

**Build proceeds with OFF.** Routed to the owner on the checklist under item 15
(where the question was already logged), not as a new blocking item.

---

## §4 — JOB 4: TestKit strategy (one kit, two registries)

Facts derived: 87 probes across 11 files (`SMRTest.Register(` occurrences minus
the definition, matching `doccheck.py:485` and the STATE block). **8 probes
touch the opt-in modules**: `ClassicRockets` (`30_Probes_Wave3.lua:85`),
`AcknowledgedWarnings`, `ResidencyControl`, `MultipleSuns`, `CohortHousing`,
`NoHomeless`, `DroneStatDials`, `OptionsMenu` (all `60_Probes_Opt.lua`).
⚠️ **`DroneOverhaul` has no probe at all** — `91_Stress.lua` is its only
harness. That is a pre-existing gap; the split does not create it and must not
be blamed for it.

### 4.1 The five re-pointings

1. **`00_TestCore.lua` — a second registry accessor.** `SMRTest.FixStatus(id)`
   (`:133-137`) reads `_G.SMRFixPack` only. Add `SMRTest.OptStatus(id)` reading
   `_G.SMROptInPack`, and a `SMRTest.OptMissing(id)` mirroring `fix_missing`
   (`:282-294`) — with one deliberate difference (§4.2).
2. **`00_TestCore.lua` — `SMRTest.FromFixPack`** (`:123-130`) matches source
   paths `SMR%-BugFixPack`, `SMR_CommunityFixPack`, `CommunityFixPack`,
   `Fix_[%a]+%.lua`. **None of those matches `SMR-OptInPack` / `Opt_*.lua`.**
   Add `SMRTest.FromOptInPack(fn)` with the mirror patterns; keep
   `FromFixPack` narrow so a cross-mod mix-up reads FALSE rather than
   accidentally true.
3. **The RunAll gate line** (`:346-354`) prints one registry. Make it print
   both, on **two lines**, so existing greps for `fix pack present:` keep
   working and a new `opt-in pack present:` line is unambiguous:
   `fix pack present: %d/%d fixes active` · `opt-in pack present: %d/%d modules active`.
   An absent registry prints the existing "NOT loaded" form for that mod.
4. **`60_Probes_Opt.lua` + the `ClassicRockets` probe:** `opt_gate` (`:18-25`)
   and `ClassicRockets`' inline copy (`30_Probes_Wave3.lua:87-93`) call
   `SMRTest.FixStatus` → switch to `OptStatus`. The three `SMRFixPack_*` FLAG
   literals inside probes (`:48`, `:104`, `:396`) and the two dial ids (`:786`)
   ⛔ **stay byte-identical** — they are §2.1 names, and a probe that "helpfully"
   renamed them would pass against a broken build.
5. **`99_FixtureCarry.lua`**: `PREFIX = "SMRFixPack"` (`:34`) and the KNOWN list
   (`:40-52`) — scan **both** prefixes; the two Opt-written field names in the
   list keep their bytes and gain an "(opt-in mod)" comment.
   **`91_Stress.lua`**: `P.DroneOverhaulStats` (`:445`) and
   `P.IsActive("DroneOverhaul")` (`:453`) → the opt-in registry.

### 4.2 ⛔ The rule that keeps cells (b) and (c) honest

`SMRTest.FixMissing` returns **FAIL** when a fix is not registered
(`00_TestCore.lua:287-289`). Today that is right — a missing fix *is* a failure.
After the split it is wrong for the opt modules: in **cell (c)** (fix pack
alone) the opt-in registry does not exist, and eight probes would report FAIL
for a mod that is legitimately not installed. ⇒ **`OptMissing` returns SKIP
("opt-in mod not installed"), never FAIL, when the whole registry is absent**;
it keeps FAIL for a module that IS registered but errored. Same treatment for
`DroneStatDials` (`60_Probes_Opt.lua:761`, currently `SMRTest.FixMissing`) and
for `OptionsMenu`.

### 4.3 `OptionsMenu` splits into two expectations

Today it asserts one mod owns everything (`:875-955`): the registry, the
`ModDef`, `default_options`, and the option items. Rewrite as **two probes**:

* `OptionsMenuOptIn` — the whole of today's body, re-pointed at
  `Mods["SMR_CommunityOptInPack"]` and the `SMROptInPack` registry, with
  **`NoHomeless` added to `WANT`** (the §0 gap) so it asserts **7** toggles + 2
  dials. SKIP if the opt-in mod is absent.
* `OptionsMenuFixPack` — asserts the *negative* that the split creates: the fix
  pack's `ModDef` exposes **no** `default_options` and **no** option items, so
  it no longer lists in Mod Options, and no `Opt_*` id appears in `SMRFixPack.fixes`.
  This is the probe that would catch a half-done subtraction. SKIP if the fix
  pack is absent.

Probe count goes **87 → 88**. That is the only intended change to the count and
it is folded into every prediction in §6.2.

### 4.4 The activation instrument (needed by cell (a2) and (b))

The documented pre-load lever (`SMROptInPack_Optional = {…}` before the mod
loads) **cannot be used from a companion mod** — inter-mod load order is not
ours to set. Use instead the path D05 already proves live in both directions
(`00_Core.lua:400-449`, PT-51):

```lua
local def = Mods["SMR_CommunityOptInPack"]
for _, id in ipairs{ "ClassicRockets", "AcknowledgedWarnings", "ResidencyControl",
        "MultipleSuns", "DroneOverhaul", "CohortHousing", "NoHomeless" } do
    rawset(def.options, id, true)
end
Msg("ApplyModOptions", "SMR_CommunityOptInPack")
```

`Mods[id].options` is the object the engine itself rawsets values onto
(`Mod.lua:679-683`), and writing there — not to `CurrentModOptions` — is the
lesson `60_Probes_Opt.lua:773-778` records from the failed 2026-07-29 leg.
⚠️ It writes **no account storage** (nothing calls `SaveAccountStorage`), so the
owner's real toggles are untouched; the instrument restores the originals in
every branch, exactly as the `DroneStatDials` probe does.

---

## §5 — JOB 5: the doc, policy and tooling migration inventory

### 5.1 MOVE — the 8 modules' entries

Mapping **derived from the entries themselves** (each entry's heading tag names
its file):

| entry | module | index row | status today |
|---|---|---|---|
| `D01.md` | `Opt_ClassicRockets` | row 64 | `opt-in` |
| `D02.md` | `Opt_AcknowledgedWarnings` | row 65 | `tested` |
| `D03.md` | `Opt_ResidencyControl` | row 66 | `tested` |
| `D04.md` | `Opt_MultipleSuns` | row 67 | `tested` |
| `D06.md` | `Opt_DroneOverhaul` | row 104 | `built` |
| `D07.md` | `Opt_CohortHousing` | row 105 | `built` |
| `D09.md` | `Opt_DroneStatDials` | row 106 | `tested` |
| `D12.md` | `Opt_NoHomeless` | row 109 | `speced` |

**`D05` (the Mod Options enable surface) moves too** — it is the opt-in
modules' enable surface and, after the split, the fix pack has no options page
at all. **`D13` stays here** (it covers both mods by owner ruling; one
artifact) and **`D10`/`D11` stay** (parked/candidate, not built, not opt-in
files). `D08` has no entry file.

⚠️ **The tombstone problem, and it is a real tooling constraint, not a
preference.** `check_entries` requires the file name to equal the id, the body
to open with `### <ID>`, front matter to carry every field, and `seq` to be
**1..N contiguous** (`doccheck.py:210-216`); `check_index` regenerates
`INDEX.md` from those entries and requires a byte-identical diff. So a
"one-line tombstone row" cannot be hand-added to the generated index. **Two
shapes work; the design picks the first:**

* ⭐ **Tombstone ENTRY files** — keep `D01.md`…`D05.md`, `D09.md`, `D12.md` in
  place, each reduced to its heading + front matter + a 3-line MOVED body
  pointing at `C:\Dev\SMR-OptInPack\docs\agent\bugs\<ID>.md` and naming the
  commit sha it left in. `seq` stays contiguous, `INDEX.md` regenerates
  unchanged in shape, every historical `D03` reference still resolves one hop
  away — the same pattern `docs/BUGS.md` already uses for the restructure.
  Status word: keep the current one (the record did not change; it moved), and
  add the MOVED note to the heading tag **after** the status word so
  `status_word()` still parses it (`doccheck.py:97-103` reads the FIRST
  vocabulary word after stripping leading non-letters).
* Full deletion + `seq` renumbering of everything after — touches 100+ files
  and rewrites `INDEX.md` wholesale for no gain. **Rejected.**

⇒ predicted post-split index rows here: **unchanged, 102 F + 12 D + 46 C**,
with 9 D entries reduced to tombstones. The *new* repo's index is 9 rows
(D01–D05, D06, D07, D09, D12) with fresh `seq` 1..9 and `row` 1..9.
⚠️ `split_bugs.py` derives `seq`/`row` from front matter; the new repo's entries
must be renumbered on arrival or its `check_entries` will red on
non-contiguous `seq`. **Build step, not an afterthought.**

### 5.2 COPY WHOLE

* `docs/agent/facts/` — all **53** `EF-*.md` + `INDEX.md` + `_preamble.md`.
  Engine facts describe the game; both repos need them. Divergence is accepted
  and **dated from the copy** (rule 7) — the new repo's `_preamble.md` gains one
  line saying so, naming the sha.
* `tools/split_facts.py` (needed to regenerate the facts index).

### 5.3 ADAPT — and what "adapt" costs, file by file

| artifact | adaptation | ⛔ traps found |
|---|---|---|
| `CLAUDE.md` | rewrite for the new mod (26 lines); keep the folder contract and the "STATE.md is mandatory every session" rule; drop the 2026-08-03 restructure note (that history is not the new repo's), replace with a pointer to `PROVENANCE.md` | — |
| `docs/agent/FIX_POLICY.md` (540 ln) | §4 ("the pack stays a pure bug-fix mod") **inverts** in a mod whose product is opinionated modules — rewrite that section rather than delete it, and keep the original text quoted as the reason the modules were `Opt_` in the first place. §5's dial addendum, §3's save-footprint rules and §3a's disposition-table rule all apply unchanged | a clause that does not apply is **kept and marked N/A**, never deleted (rule 7) |
| `docs/agent/WORKFLOW.md` (975 ln) | keep ALL harness stacks verbatim: probe hygiene (`:134-224`), the ARM gate + resolution cross-check (`:494-528`), leg-design rules, log-review rule (`:277`), cheats rule (`:314`), co-run protocol. Re-point Layout/Install (`:77-104`) at the new repo + junction. `fpk verification` (`:118-133`) applies unchanged (same game). Mark the fix-pack-specific release steps N/A-or-adapted | ⭐ **install the twin of the BOTH-MODS-LOADED clause (`:359-391`) here**, per README rule 12 — prompt 5 activates both |
| `docs/agent/reports/CHAIN_METHOD.md` (287 ln) | copy; it is method, not content | — |
| `docs/agent/reports/DRONE_OVERHAUL_OPTIONS.md` | **move** — it is D06/D09's design study and both entries cite it (`Opt_DroneOverhaul.lua:5`, `Opt_DroneStatDials.lua:5`) | leave a one-line pointer here |
| `docs/README.md` | new map for the new tree | ⛔ doccheck **parses** this file for the root allowlist — the map is the source of truth, so an unparseable or incomplete map is a red build (`doccheck.py:339-369`) |
| `tools/doccheck.py` | port + re-point | ⛔⛔ **three real defects the port must fix, all found by reading the code:** (1) `counts["default_active"] = counts["modules"] - 7` (`:475`) is a hard-coded 7 — **on the fix-pack side after the split it would report 67 instead of 74**. ⚠️ And the obvious generalisation `modules - optional` is **also wrong**, because `counts["optional"]` is a plain substring count (`files_containing(…, "optional = true")`, `:472`) that reports **8** — it matches `Opt_DroneStatDials.lua:56`, where the string appears **inside a comment** saying the module registers *without* it. Verified: `grep -nE "^\s+optional = true,\s*$" Code/*.lua` → **7**. So the hard-coded 7 is accidentally right today and the substring count is silently wrong. **Fix both**: count the def-field form only, then `default_active = modules - optional`. Yields 82−7=75 today, 74−0=**74** post-split here, 8−7=**1** in the new repo. (2) `STUBS` (`:55-59`) must be dropped in the new repo (§3.2). (3) `TESTKIT`/`SMR_TESTKIT` (`:33`) points both repos at the same kit, so **both would count the same 88 probes** — the new repo's copy reports the count as shared and says so, or the ported checker drops the probe count entirely. Also: `--verify-split` / `--verify-facts-split` reference *this* repo's git history — keep them, mark N/A in the new repo's `--help` text |
| `tools/hooks/pre-commit` | copy; `git config core.hooksPath tools/hooks` in the new repo | — |
| `tools/blocking_analysis.py` | **copy** — `Opt_DroneOverhaul`'s F86 Tier-2 record depends on its verdict being re-runnable (`Opt_DroneOverhaul.lua:91-93`) | — |
| `tools/split_bugs.py` | copy (the new repo's index is generated the same way) | see §5.1 renumbering |

### 5.4 NEW in the new repo

* `docs/agent/STATE.md` — its own ≤60-line contract, honest "post-split, matrix
  not yet run" state at commit 1, updated at every chain step.
* `docs/agent/PROVENANCE.md` — **every ported artifact: what came from where, at
  which sha, on which date, adapted-or-verbatim.** This is the page rule 8's
  no-retraining test leans on hardest, and it is the only new document with no
  precedent here.
* `README.md` (mod-facing) and `LICENSE` (copied).
* `docs/archive/SESSION_LOG.md` — starts at the split; ⛔ **this repo's archive
  does not move** (rule 7).

### 5.5 STAYS in the fix pack

`docs/archive/` **whole** (append-only; every log, every retired prompt, the
frozen `MOD_DESCRIPTION.md`). The `split-optins/` chain folder itself — it is a
fix-pack-side record until prompt 5 empties it. `PLAYTEST_CHECKLIST.md` and
`PLAYTEST_HELP.md`: ⭐ **recommend they stay single-sourced here** rather than
splitting the owner's two human files across two repos — the owner plays one
game with both mods loaded (README rule 12), and two checklists is the exact
overhead the co-run model exists to avoid. The new repo's `docs/README.md` says
where they live and why. **This is the one place the design deliberately fails
rule 8's letter** (a fresh session in the new repo cannot read the playtest
checklist without this repo) **and it is called out rather than hidden**: rule
8's questions are about *build state, policies, module records, suite, bans,
provenance* — none of which is in the checklist. Prompt 2 should rule on
whether that reading holds.

---

## §6 — JOB 6: the verification matrix (prompt 4 runs it)

### 6.1 Harness shape (unattended, owner not at the keyboard)

Per WORKFLOW probe hygiene rule 5 (`:170-224`) and the ARM-gate rule
(`:494-506`), resurrecting the u2-run pattern:

* every instrument is **parked as a fenced code block in prompt 4's own Notes**,
  written into TestKit `Code/` at the run, deleted in the commit that records
  the answer. `Code/` is swept clean before and after; every result commit
  carries its `PROBE SWEEP:` line.
* arming is a **script FILE** (never an inline PowerShell one-liner, never
  piped — C11 and its corollary), and the launcher **reads `metadata.lua` and
  the instrument files back off disk and refuses to launch unarmed**.
* a **resolution cross-check** runs before every launch: names used vs names
  defined (unattended-1 defect class 1).
* instruments fire from `OnMsg` on load; **no console typing**;
  `95_AutoRun` + `96_AutoRunFlag` drive the colony, `SMRTest.RunAll()` and quit.
* one archived log per launch, copied + MD5'd, `git add -f` (R8).

### 6.2 The cells, with expected readings written BEFORE the run

**Baseline being displaced.** `u2run3_Mars.exe-20260811-02.01.06.log:983` reads
`77 PASS, 0 FAIL, 10 SKIP, 0 ERROR` at gate `81/81`. ⭐ **Re-derived here from
the archived log rather than assumed: the 10 SKIPs are `AnomalyCaveInMap`,
`TechDescriptionBuilding`, and eight `[install]` probes SKIPping on
"introspection unavailable (retail sandbox)" — NOT the opt-in probes.** All 8
opt-module probes **PASSed**, which proves every opt-in module was **active**
in that leg (the owner's account toggles are ON). The gate denominator is 81
because `Fix_ExoticDepositSign` (F102) landed 2026-08-12, after that leg — today
the same run would read **82/82**.

**The arithmetic every cell below is derived from, stated once so it can be
checked:** 87 probes → 88 (the `OptionsMenu` split, §4.3, adds one that PASSes
whenever the fix pack is loaded). The only verdicts the split can move are the
**8 opt-in probes**; the other 80 are untouched, which is why (a2) must
reproduce the frozen baseline exactly. `78 = 77 + 1`; `72 = 78 − 6`;
`70 = 78 − 8`. SKIPs are the complement in each case, and ⛔ **the 10 baseline
SKIPs must still be the same 10 names** — read them BY NAME, never as a total
(STATE's standing rule).

| cell | config | expected gate | expected suite | expected log |
|---|---|---|---|---|
| **(a1)** | both mods, opt-in toggles at **fresh account defaults** (§2.4) | fix pack **`74/74`**, opt-in ⛔ **`1/8`** (only `DroneStatDials` is active at base; the 7 toggles are OFF) | **72 PASS / 0 FAIL / 16 SKIP / 0 ERROR** of 88 — (a2) minus the 6 `opt_gate` probes, which flip PASS→SKIP | 7 × `<id>: inactive (opt-in module, off by default — enable it in Options → Mod Options)`; ⛔ **no `NoHomeless` F100 first-pass line** — `apply()` returns at the opt-in gate before reaching `Require`, so the two-pass artifact does not appear at all. **That is a toggle-state effect, not a port regression** |
| **(a2)** | both mods, all 7 activated in-session (§4.4) | `74/74` + **`8/8`** | ⭐ **78 PASS / 0 FAIL / 10 SKIP / 0 ERROR** of 88 — i.e. **the frozen 77/0/10/0 baseline with its 10 SKIPs unchanged, plus the one new probe passing**. This is the falsifiable claim that the port changed nothing | `NoHomeless: applied` (via the reconciler, after classes are built — the F100 first-pass line may legitimately be absent on this path); `MultipleSuns: Artificial Sun build-once limit lifted` |
| **(b)** | opt-in **alone** (fix pack disabled + ⛔ **FULL PROCESS RESTART**, D13's four-states rule) | opt-in only; `1/8` or `8/8` per activation | rule, not a list: **the 8 opt-in probes report exactly what they reported in the matching (a) sub-cell; every other probe reports FAIL or SKIP and NONE reports PASS** | ⛔ **zero `CommunityFixPack` and zero `SMRFixPack` occurrences** beyond a loaded save's own recorded-mod-list echo — grep the archived file (EF-047), full bracketed token (§1.6 hazard 2) |
| **(c)** | fix pack **alone** (opt-in disabled + full restart) | **`74/74`** | **70 PASS / 0 FAIL / 18 SKIP / 0 ERROR** of 88 — (a2) minus the 8 opt-in probes, all SKIPping via §4.2; `OptionsMenuFixPack` still PASSes. ⭐ **this number replaces `77/0/10/0` as the fix-pack-alone record** | fix pack **absent from Options → Mod Options** (no `default_options`) — asserted by `OptionsMenuFixPack`, not by a screenshot; zero `CommunityOptInPack` lines |
| **(d)** | save-compat witness, **inside cell (a)** | — | not tallied against the baseline (a real save exercises different `[state]` probes; comparing it to a new-colony leg would be a category error) | see below |

**Cell (d) — the save witness.** Stage a **byte copy** of `CP15PT15` (KEPT save,
EF-051 copy-only; MD5 the original before and after and record both). Load it
under (a), and read back **live**, by exact id, every row of §2.1:

| read | expected |
|---|---|
| `UIColony.label_modifiers["Drone"]["SMRFixPack_DroneSpeedDial"]` | ⚠️ **present iff the save was made with a non-base speed dial** — and since the mod id changed, the dials now read **base**, so the module's `PostLoadGame` reconcile **removes** it. ⭐ **Expected: absent after load, and the removal is the correct behaviour** (`Opt_DroneStatDials.lua:42-44`: "loaded saves may carry a previous session's persisted modifiers under our ids — replaced or removed to match the CURRENT dial positions"). Absence here is a **PASS**; presence of a *stale* one after the reconcile is the failure |
| same for `…["Consts"]["SMRFixPack_DroneCarryDial"]` | as above |
| every `Dome`/`Habitat`: `SMRFixPack_closed_to_new_residents`, `SMRFixPack_no_homeless` | **present exactly where the old world wrote them**, same values — these are plain persisted fields and nothing reconciles them. ⛔ **This is the single strongest test of invariant 6c**: if the port renamed a field, the row's on/off state silently resets and the policy stops applying |
| `Building` objects: `SMRFixPack_ack_notworking` | present where stamped; ⚠️ may legitimately be zero if no building was acknowledged in that save — **report the population size, not just the count**, so a zero is distinguishable from an unsampled zero (the "close cases completely" rule) |
| `SMRFixPack_F48_StationConnectors` on `UIColony` | present (fix-pack side, unmoved) — a control: it proves the read method works when the answer should be yes |
| then **save + reload once (R4)** and read every row again | identical |
| `[LUA ERROR]` count | **zero** |

⚠️ The dial expectation is the one most likely to be misread as a break. It is
written here **as a prediction** so prompt 4 records it as a hit, not a miss.

### 6.3 Stop conditions live in this matrix

Any cell showing cross-mod interference, a persisted-id break, or a
`[LUA ERROR]` naming either mod's code → stop that leg, record verbatim, keep
the independent legs running, route (README stop conditions). A tally that
misses its prediction is a **finding with a mechanism to chase**, not a retype.

---

## §7 — the residual risk register (what this design knows it has not proven)

1. **Src claim not opened this session:** that
   `UniversalRocketBase:GetFuelResourceRequest` takes no arguments (§1.4a).
   Only place the two cross-set wrappers could differ by order.
2. **Order-independence at both cross-set sites is derived by reading, not
   measured.** Cell (a) exercises them; cell (a)'s instruments should log the
   observed mod-load order.
3. **`CP15PT15`'s actual contents are unknown to this session** (game closed,
   save not opened). If it happens to carry no `ack_notworking` stamps and no
   policy flags, cell (d) samples less than it claims — §6.2 requires the
   population sizes to be reported for exactly that reason. Prompt 3 or 4
   should confirm the save is a useful witness **before** the run, and stage a
   second one if not.
4. **The 88-probe predictions assume no other probe is state-dependent between
   legs.** The archived per-probe list from `u2run3` is the control; prompt 4
   diffs all 88 rows, not just the totals (the C43 precedent).
5. **`docs/README.md`'s prose counts are already stale here** (§0) and doccheck
   does not catch prose. The new repo will inherit the habit unless its map is
   written with derived numbers or none.
6. **Rule 8's letter is deliberately not met for `PLAYTEST_CHECKLIST.md` /
   `PLAYTEST_HELP.md`** (§5.5). Named, not hidden; prompt 2 rules.

---

*Design complete. Prompt 2 is the gate — it may return BUILD, REVISE or STOP,
and prompt 3 may not run on anything but BUILD.*
