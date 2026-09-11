# Per-fix buttons — the research the `fixtoggles` chain was authored on (2026-09-11)

Written by `smr-bugfixpack-24` at the owner's ask (*"gather all the information. And then author a chain"*).
Three read-only research agents ran in parallel; their findings are condensed here WITH their citations so the
chain and its terminal audit can check them. Nothing here was run in a game.

**Provenance tags, binding for every reader.** `[A]` = re-read by the authoring session itself (the file:line was
opened) · `[R]` = a research agent's source read, cited, NOT re-opened by the author · `[I]` = inference. ⛔ Chain
rule 6 applies to all of it: `[R]` rows are leads for link 01 to re-derive, never permission to skip the read.

## 1 · What we already have (the pack)

- `[A]` The live-toggle machinery EXISTS and is DORMANT: `optional` flag, `SMRFixPack.OptionEnabled` (reads
  `CurrentModOptions`), the `OnMsg.ApplyModOptions` reconciler (live on/off, `on_activate`/`on_deactivate`), and the
  per-call gate read `SMRFixPack.IsActive` — `Code/00_Core.lua:39-58`, `:519-575`. Built for the `Opt_` modules; dormant
  since they moved to `SMR-OptInPack` on 2026-08-12 (`FIX_POLICY.md` §5 banner, `:590-598`).
- `[R]` No module sets `optional`. Only `Fix_ExtenderFlapChurn` gates its installed hook per call on `IsActive`
  (`Fix_ExtenderFlapChurn.lua:79-105`). Every other installed wrapper/replacement runs unconditionally, so today a
  mid-session veto stops only `WhenActive` handlers and `DataPatch` passes, never call-path fixes.
- `[R]` The pack has NO options surface: no `default_options` in `metadata.lua` (`:298-306`), no option items in
  `items.lua` (`:3-14`). The engine lists a mod in Options → Mod Options only when `default_options` is non-empty
  (1.1.0 `CommonLua/Modding/Mod.lua:475-476`).
- `[A]` The player cannot switch off a single fix by any route today: the `SMRFixPack_Disabled` veto is read at
  `Register` (`00_Core.lua:510`), so only a companion mod that loads first can use it; the console is too late.
  (`SMR-OptInPack/docs/FUTURE_IDEAS.md` #9, `:337-383`, parked 2026-08-16.)
- `[A]` **"Off" is not an uninstall** (`EF-002`): a toggled-off module is still installed and still capturable into
  a save; only a Mod Manager disable/removal keeps our frames out. Mod Options survive a Mod Manager disable.
- `[A]` `CurrentModOptions` is per-mod-env; runtime writes to `Mods[id].options` are session-only — AccountStorage is
  saved only by the options dialog's Apply (`EF-004`). `SaveAccountStorage` is a ModEnvBlacklist key
  (`CHAIN_METHOD.md` §3, unattended-2 row).

### Engine routes `[R]` (1.1.0 unless noted; 1.0.7 has the same machinery, `SrcArchive/.../CommonLua/Classes/Mod.lua:684, :746, :1621, :2170, :2708`)

| route | what it gives | cites |
|---|---|---|
| Mod Options (`ModItemOptionToggle`/`Choice`/`Number`) | gamepad-native built-in page; values load BEFORE mod code as `CurrentModOptions`; **Apply fires `Msg("ApplyModOptions")` and saves, no restart** | `Mod.lua:2725-2788`, `:2157-2160`, `:680-698`, `:1634`, `:753-772`, `:2197-2201` |
| Options category (`OptionsCategories` entry with `run`) | a custom entry under Main Menu → Options that opens our own window | `CommonLua/Core/options.lua:775-790`; `run` honoured at `Lua/XDef/OptionsContentWindow.generated.lua:89-90`, `CommonLua/Data/XDef/OptionsDialog.lua:77-78` |
| Mod persistent storage | `CurrentModStorageTable` + `WriteModPersistentStorageTable` → `AccountStorage.ModPersistentData[id]` + `SaveAccountStorage(1000)` inside the engine; per ACCOUNT; capped by `const.MaxModDataSize` | `Mod.lua:1496-1502`, `:1520`, `:1524-1533` |
| `OnMsg.ModUnloadLua` | fires when the mod is switched off | `Mod.lua:2169-2170` |

`[I]` Consequence: a custom panel cannot persist into Mod Options (no Apply, `SaveAccountStorage` blacklisted), so
custom panel ⇒ mod persistent storage; built-in page ⇒ Mod Options. Two surfaces ⇒ two stores unless one is designed
to be the only writer. **ONE store is a design requirement** (the README says so).

## 2 · The reference mod (fredware's "SMR Community Fixes") — design only

Local clone `C:\Dev\_ref\smr-community-fixes`, `main` = `82c7ca4` = remote head `[R]`. **15 fixes** at HEAD.
- `[R]` **NO LICENSE** (API `"license": null`, `/license` 404, no file, no terms in the tree) ⇒ default copyright:
  study, never copy code, identifiers or wording. ⛔ Do not reuse `SMRCommunityFixesPending`,
  `SharedModEnv.SMRCF_*Hooks`, the `set_enabled`/`quiesce`/`events` contract names, his layout constants or his text.
- `[R]` Panel: an `OptionsCategories` entry after Credits (`Code/SMRCommunityFixes.lua:880-924`, removed on unload
  `:929-941`); a hand-built modal `XWindow` on `terminal.desktop` (`:1510-1806`), `XEdit` search, `XCombo` version
  picker, `XList` + `XScrollBar`, rows = `XCheckButton` + `%03d` number + `[Beta]` + title + description
  (`:1265-1361`); staged changes (`Panel.pending`), Back discards; Apply is transactional with rollback (`:686-805`);
  Reset = **all off**, not defaults (`:1474-1508`); Select/Unselect act on visible rows.
- `[R]` Off = live restore of the captured original **only if the global still points at his wrapper**, else the
  wrapper stays as a pass-through (`templates/smrcf_TEMPLATE.lua:189-225`); save repairs are not undone
  (`TEMPLATE:40-41`). Re-applies at code load, `ClassesBuilt`, `CityStart`/`LoadGame`, `ModsReloaded` (`:1863-1893`).
- `[R]` Storage: mod persistent storage, `{schema=3, target_version="1.0.7", fixes={[id]=bool}}` (`:197`, `:228-245`);
  a stored value always wins ⇒ **promoting a fix from Beta/off to on-by-default never reaches existing players** `[I]`.
- `[R]` **Version selector is a display filter only.** `Config.GAME_VERSIONS = {"1.0.7"}` (`:92-97`); the runtime target
  is a separate stored value the dropdown never changes; nothing reads `LuaRevision`/`GetVersion` ⇒ his 1.0.7-tagged
  fixes run on 1.1.0 too `[I]`, contradicting his own `CONTRIBUTING:118-122`.
- `[R]` Beta = label + search term; `IsRuntimeEnabled` never reads it (`:552-558`); off-by-default only because every
  Beta fix also sets `default_enabled=false`.
- `[R]` No dependencies/linked toggles (fixes may not reference each other; CI enforces, `tools/sync_mod.lua:260-296`).
- `[A]` **Gamepad/console:** not handled beyond B-to-close (`:1541`) and focus colours; the list sets
  `GamepadInitialSelection = false` and clears any selection on select (`:1690-1697`) `[I: may block gamepad row
  focus]`; his gamepad check is an unticked manual test line (`DESCRIPTION.md:909-911`); no Mod Options items, no
  `default_options`, no console tag (grep of `metadata.lua`/`items.lua`/`README`/`DESCRIPTION`: zero hits).
- `[R]` Row numbers are positional and shift when a fix is removed (`README:55-57`) — we show stable ids instead.

## 3 · Per-module feasibility (all 45 registered modules) `[R]`

Legend — shape: **a** wrap+call-through · **b** full shipped-body copy · **c** data/class/preset edit · **d**
message handler/thread · **e** save repair. Live: **now** = a registry flip already works · **gate** = needs a per-call
gate to the captured original (b needs the original captured first) · **undo** = needs `on_deactivate` for state ·
**load** = safe only on next load/restart. All install inside `apply` at file load unless noted.

⛔ **The mechanism must be the per-call gate, NEVER restoring originals** `[R]`: (1) the engine copies a patched
method into every subclass at class build (`EF-058`), so a later base-class restore misses the copies; (2) two of our
modules chain on `Colonist:Idle`, so restoring either original clobbers the other; (3) the pattern already exists
(`FIX_POLICY` §5 install rule `:613-622`; `Fix_ExtenderFlapChurn`).

| module | shape · targets | live / obstacle / save | links | branch |
|---|---|---|---|---|
| 90_SaveSanitizer (F35,F48,F95) | d+e PostLoadGame `WhenActive` (`:431`); F48 one-shot flag (`:187`,`:449`) | now; repairs made are permanent | F95 fights v5's AstrogeologistExtractors (`:323-392`) — only matters with 1.0.7 back | F35/F48 pre-1.1.0 saves; F95 1.1.0 |
| AnomalyCaveInMap (F31) | a globals `TriggerCaveIn`,`FindCaveInLocation` (`:100`,`:122`) | gate | – | both |
| ArrivalDeaths (F53,C83,F117) | a `Colonist:OnArrival` (`:232`), `Colonist:Idle` (`:370`) | gate | **shares `Colonist:Idle` with ShelterReflex**; calls opt-in-wrapped `ChooseDome` | both (probe `:315-340`) |
| BombardmentSpread (F26) | b global `WaitBombard` (`:202`) | gate; in-flight volley finishes on our copy | – | both |
| BrokenTrackSalvage (F45) | a `TrackBase:BreakTrackElement` (`:57`); e LoadGame stamps `node_idx` (`:71`) | gate | track group (TrackSalvageWipe also stamps, `:183-188`) | both |
| CrystalMysteryHang (F06) | d `CrystalFlyAway`+LoadGame `WhenActive`; game-time repeater (`:72`); `MysteryEnd` not gated (`:117`) | now; `on_deactivate` should stop the repeater | – | both |
| DestroyedTunnels (F38) | a `TunnelBase:AddPFTunnel` (`:54`) + LoadGame sweep (`:67`) | gate | – | both |
| DomeFreeSpaceMismatch (F60) | b `Dome:RefreshFreeLivingSpaces` (`:61`, original not captured) | gate | – | both |
| DomeOverviewHighlight (F14) | b `Community:UICommandCenterStatUpdate` (`:36`) | gate | – | both |
| DroneTransportMinors (F57a) | a `DroneControl:UpdateRocketsInternal` (`:176`) | gate | – | both (half b deleted on 1.1.0) |
| DustSicknessBiorobots (F40) | c appends StoryBit filters via DataPatch (`:79-104`); e LoadGame cure (`:175`) | **undo** (remove appended filters; reset runner `patched` on re-enable `[I]`) | – | both |
| ExoticDepositSign (F102) | c class `entity` default pre-build (`:81`); LoadGame `UpdateEntity` sweep (`:93`) | **load** (value baked into built class; live re-sign on an asteroid touches the suspected freeze trigger) | – | both |
| ExtenderFlapChurn (F77) | a file scope, **already gates on `IsActive`** (`:83`) | now | – | both |
| FounderTraitNotification (F23) | d `ColonistAddTrait` `WhenActive` (`:49`) | now | – | both |
| FreedHousingNotice (F59) | a `Colonist:SetResidence` (`:67`) | gate | leans on StaleReservations (`:32-37`) | both |
| GeneForging (F41) | a global `GetRareTraitChance` (`:143`) | gate | – | both |
| GhostFarmOxygen (F37) | a `Building:SetDome` (`:45`); e LoadGame (`:60`) | gate | – | both |
| GraphConsumedCaption (F19) | a `City:GetColonyStatsButtons` (`:87`) | gate | – | both |
| JumboCaveReinforcementWedge (F110) | d NewHour+LoadGame `WhenActive` (`:141-143`) | now | – | both |
| LakeEntombment (F30) | a `LandscapeLake:PlacePrefab` (`:52`) | gate | – | both |
| LanderEmptyLaunch (F67) | a `UniversalRocketBase:IsCargoReady` (`:69`) | gate | – | both |
| LandscapeUnitFilter (F34d) | b global `LandscapeForEachUnit` (`:218`) | gate | – | 1.1.0 only (`:181-196`) |
| LayoutTechLock (F43,F118) | a `LayoutConstructionController:Activate` (`:91`) | gate | – | both |
| MirrorSphereSite (F16) | a `MirrorSphereBuildingBase:StartAction` (`:57`) | gate | – | both |
| NightShiftWork (F04) | a `Colonist:ShouldLeaveForWork` (`:60`) | gate | – | both |
| PayloadTemplateRefill (F70) | b `CargoRequestNew:Apply`,`:RetrieveRequests` (`:237`,`:263`) | gate; saved `SMRFixPack_payload_set` inert while off | – | 1.1.0 only (`:169-196`) |
| RocketDroneChurn (F50) | b `CargoTransporterNew:UpdateCargoResourceRequests` (`:102`) | gate | – | 1.1.0 only (`:91-97`) |
| RocketInteractGuard (F74) | a `RCTransport:CanInteractWithObject`,`:InteractWithObject` (`:130`,`:138`) | gate | – | both |
| SaintBlessing (F92) | c rewrites `TraitPresets` `modify_trait` on 1.0.7 path (`:269`); e LoadGame re-base (`:329`) | **load**; on 1.0.7 off mid-save leaves blessings stuck `[I]`; on 1.1.0 save-repair only | – | both (probe `:262-291`) |
| SequenceLatents (F29) | a `SA_GetLabelToRegister:SAExec`,`AlienDigger:GameInit` (`:106`,`:132`) | gate | – | both |
| ShelterReflex (F73b) | a `Colonist:Idle` (`:97`); saved `SMRFixPack_shelter_try` inert while off | gate | shares `Colonist:Idle` | both |
| ShuttleHubOffAvailable (F54) | a global `IsLRTransportAvailable` (`:78`) | gate | feeds VacuumWalks (`:251`) | both |
| ShuttleTransportCache (F51) | b global `FindTransportationModeToCommunity` (`:61`); `smr_shuttles` key in a saved cache (`:97`) | gate; vanilla ignores the key | loose link to ShuttleHubOffAvailable | both |
| SilentHitMomentFX (C74,C77) | a `CObject:GetAnimMoments` (`:307`), `BaseBuilding:UpdateWorkingStateAnim` (`:324`); c anim-moment presets (`:286`); e LoadGame (`:263`) | gate + **undo** for presets (`:24-26`) | – | both (probe `:306-321`) |
| SinkholeIndestructible (F96) | c class flag via DataPatch (`:101-108`) | **undo** (write flag back) | – | both |
| StaleReservations (F58) | a `Residence:ReserveResidence` (`:107`); d NewDay `WhenActive` (`:120`); saved `SMRFixPack_reserved_at` | gate; old stamps may release early after re-enable `[I]` | FreedHousingNotice | both |
| TrackConnectorPingPong (F66) | b `TrackConnectedObjBase:CreateConnectorElements` (`:144`); a `:Done` (`:225`); game-time threads (`:208`) | gate | track group | both |
| TrackSalvageRefund (F47) | b `TrackBase:GetRefundResources` (`:124`); a `TrackGridElement:Demolish` (`:195`) | gate | track group (reaches TrackSalvageWipe's replacement, `:72-89`) | both |
| TrackSalvageWipe (F44,F91,F116) | b `TrackGridElement:DemolishAndSplitTrack` (`:111`); e LoadGame deletions (`:426`) | gate; deletions permanent | track group; carries the F45 sort guard | both |
| TrackTunnelPowerBridge (F65) | a `TrackBase:Done` (`:153`); d `StationsConnected`,`PostLoadGame` in apply, **not gated** (`:160`,`:166`) | **split**: tunnels persist; the `Done` teardown must stay ON while any exist (`:56-69`) — gate only the bridging | – | both |
| TrainCargoDumping (F46) | b `Train:UnloadAll` (`:247`) | gate | – | 1.1.0 only (`:186-205`) |
| TrainsToVoid (F64) | a `Building:OnDemolish` (`:51`) | gate | – | both |
| TrainWaitTime (F21) | a `TransportStatistics:AddSpentTime` (`:108`) | gate | – | both |
| VacuumWalks (F52) | b `Colonist:TryToEmigrateToDome` (`:218`) | gate | calls `IsLRTransportAvailable` | 1.1.0 only (`:177-201`) |
| WispRewards (F07,F15) | b global `SetLightTrapMode` (`:39`) | gate | – | both |

**Tally `[R]`:** ~36 live with a per-call gate or already live; ~9 need undo, next-load or a split. ⇒ The owner's
"all is preferable" looks reachable; no module was found that cannot be made switchable. Shared targets: one method
hooked twice (`Colonist:Idle`); same-class clusters (track group on `TrackBase`/`TrackGridElement`, `Building`, six
`Colonist` methods); cross-mod: ArrivalDeaths ↔ opt-in pack's `ChooseDome`/`CanAcceptNewColonists`.

## 4 · The 1.1.0 incident — why this is being built now `[R]`

v5 (a 1.0.7 build) reached every 1.1.0 player 2026-09-08 → v6 live 2026-09-09 23:22 (Steam) / 23:27 (Paradox) ≈ 1.5
days (`SESSION_LOG.md:824-825`, `:1408-1411`). Threw: F114 trains (157 throws in one log), F115 landscaping (the
engine's own box named us), F111, F117. Applied-and-harmful: SaintBlessing, StaleReservations, ShelterReflex (a),
FirstAsteroidPrefabs, AstrogeologistExtractors, DisasterPredictionLeak (`SESSION_LOG.md:1125-1154`). No self-check
caught any of them (class c, "semantics moved under a wrapper"). `F114.md:27-30`: the reporter *could not* bisect,
because nothing could be switched off individually. `[I]` A per-fix switch would have let a player drop one module
instead of the pack; it is a **mitigation, not a detector**.

## 5 · Rules the design must honour `[A]` unless tagged

- `FIX_POLICY` §5 `:596-598`: *"If a proposal here needs a toggle, it is not a fix"* — written to keep opt-in behaviour
  changes out; the owner's 2026-09-11 ask overrides its letter (ck148 records it); the chain rewords it.
- `FIX_POLICY` §2a `:185`: *"DO NOT BUILD A GAME-VERSION DETECTOR"* — **stays in force**; versioning is the B step
  (owner, 2026-09-11), researched by link 09 only. Open twin: checklist 133(4) ("`LuaRevision` as an observation label").
- `FIX_POLICY` §8 + `EF-054`: never name fredware's mod on a player surface; no load-order advice.
- `FIX_POLICY` §7: Mod Options is the one universal (gamepad) surface; every log/console surface is invisible on console.
- `FIX_POLICY` §3a + `EF-002`: toggles decide behaviour, never persistence. Player text must not promise "off = clean save".
- `FIX_POLICY` §2 F87: every change works on the enable path (tick at the menu → in-place `ReloadLua`) and cold boot.
- `STATE` H-02/H-03/H-10: no Mod Editor, no `version`, no portal API; `items.lua` is the source of `metadata.lua`'s code
  list (and, for Mod Options, of the option items — `ModItemOptionToggle.name` == Register id == `default_options` key,
  `FIX_POLICY` §5 `:600-602`).
- Status vocabulary `tested-attended`/`tested-unattended`; "Fixed" is a claim until confirmed (owner, 2026-09-08).
- `[R]` Beta candidates today (shipped unexercised or source-derived): F116, F117, F118, the Saint heal
  (`STATE.md:20-22`); F119 if built (peer `smr-bugfixpack-0d`, ck146). No rule maps Beta to status words yet.
  ⚖️ **Superseded for F119 and C86 (later 2026-09-11):** both went `tested-attended` in play (checklist 149), and the
  owner cut the Beta label for both. Do not tag either Beta.

## 6 · The owner's rulings in this session (2026-09-11, verbatim where quoted)

- Scope: *"making it to where users can turn on or off each fix"*; *"I am willing to setting only giving the option to
  turn off full body replacement fixes if there is a good reason we cannot do them all (but all is preferable)"*.
- Look: *"I do not want to rip off his code, I would want our UI to have its own feel and look, but we can use his for
  inspiration."*
- Beta: *"issue beta fixes that we haven't fully tested but we want to get a fix out to people because its game
  breaking And we can mark it beta."* Default: **decide per fix** (answered 2026-09-11).
- Links: *"if we do [have fixes that rely on each other] we should make sure thier button is linked."*
- Order: *"I want to focus on the buttons first, and then we can swing back around to the versioning as a B step if we
  proceed with that."* (Both the version-model and the 1.0.7-import questions.)
- Surface: asked how fredware handles gamepad/console; answered in session (§2, gamepad bullet) — ⇒ routed as ck148(a).
