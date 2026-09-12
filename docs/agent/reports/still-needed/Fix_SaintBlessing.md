# Fix_SaintBlessing review

Task/agent: `/root/module_c`, one-module fan-out review. Sweep anchor: `2983fac`.
Captured census anchor: `8469ae453b3d6312128ab187f38305f62fa41b92`.
Game/source: **1.1.0.403908**. Recommendation only; the owner decides retention.

## Disagreements first

- **SOURCE — small public claim error:** `C:/Dev/SMR-CommunityMods/content/fix-list.md:148`
  calls Saint's effect “colony-wide.” It benefits Religious colonists in the
  Saint's dome, as the shipped description and target state at
  `C:/Dev/SMR-SrcArchive/1.1.0.403908/Src/Data/TraitPreset.lua:396` and `:405`.
  Recommend replacing “colony-wide effect” with “blessing for Religious colonists
  in its dome.” The row's explicit vanilla-repair/historical-healing caveat at
  `fix-list.md:159`–`:165` is correct and should remain.
- **MEASURED — raw-status parser disagreement, now resolved:** the archived second boot logs `applied` at
  `docs/archive/logs/stillneeded_Mars.exe-20260912-00.25.42-6a91a190.log:123`,
  then `inactive (no dome-colonists trait presets)` at `:141`, then **save re-base
  armed for 1 preset of 2, data left untouched** at `:158`. The latter message
  follows `ctx.heal()` at `Code/Fix_SaintBlessing.lua:281`; the core explicitly
  restores registry status to `active` at `Code/00_Core.lua:348` and clears the
  suspect flag at `:356`. `CENSUS.json` preserves the raw last explicit status
  message (`inactive`) separately from its final registry measurement. The
  coordinator's settled direct read at
  `docs/archive/logs/stillneeded_registry_Mars.exe-20260912-00.29.01-6a91a190.log:264`
  measures **SaintBlessing active** (`:270`: 46/46 active). That measurement
  supersedes the stale parser status and confirms the source interpretation.
  Active installation and arming a healer do not verify a cure.

| module | entry | applies? | consumer still reads it? | row true? | bullet true? | verdict | evidence file:line on 1.1.0.403908 | basis | what I did NOT check |
|---|---|---|---|---|---|---|---|---|---|
| Fix_SaintBlessing.lua | F92 | yes — direct settled registry active; 1.1.0 data rewrite correctly declined and historical healer armed | yes — dome modifier affects current members and newcomers, contributes to the current morale rest target, and is removed through the matching label rule | partial — version/healing caveat sound; colony-wide scope is inaccurate | n/a — no Saint headline bullet in metadata.lua description | KEEP-BUT-FIX-CLAIM | C:/Dev/SMR-SrcArchive/1.1.0.403908/Src/Lua/TraitPreset.lua:86; C:/Dev/SMR-SrcArchive/1.1.0.403908/Src/Lua/LabelContainer.lua:73; C:/Dev/SMR-SrcArchive/1.1.0.403908/Src/Lua/Units/Colonist.lua:2563 | SOURCE | damaged-save cure; visible infopanel; heal reload/idempotence; fresh 1.0.7 boot; affected-player population; mod-added presets; whole-list card claims |

## Primary evidence

- **SOURCE — vanilla fixes the original defect:**
  `C:/Dev/SMR-SrcArchive/1.1.0.403908/Src/Lua/TraitPreset.lua:86` resolves the raw
  trait through `GetTraitLabel`, and `:88` registers the resulting dome modifier.
  Removal resolves the same label at `:100` and removes it at `:102`.
  `C:/Dev/SMR-SrcArchive/1.1.0.403908/Src/Lua/Units/Colonist.lua:442` files arriving
  colonists under the trait label; `:445` applies the dome modifier, while `:431`
  removes it from the previous dome. The ordinary trait apply/unapply callers
  still pass `modify_trait` at `Lua/TraitPreset.lua:117` and `:126`.
- **SOURCE — the changed state retains real consumers:**
  `C:/Dev/SMR-SrcArchive/1.1.0.403908/Src/Lua/LabelContainer.lua:62` stores the
  modifier by label and source; `:73`–`:75` applies it to current label members.
  `:21`–`:24` applies stored modifiers to newcomers. The remodeled stat system
  still adds `base_morale` into `GetRestStatTarget` at
  `C:/Dev/SMR-SrcArchive/1.1.0.403908/Src/Lua/Units/Colonist.lua:2563`; rest reads
  that target at `:2610` and changes the stat toward it at `:2624`.
  `C:/Dev/SMR-SrcArchive/1.1.0.403908/Src/Lua/Stats.lua:898` reads these same
  property modifiers and obtains the trait's infopanel text at `:902`.
- **SOURCE — historical healing caveat remains valid:**
  `C:/Dev/SMR-SrcArchive/1.1.0.403908/Src/Lua/Traits.lua:1326` rejects a string
  which is not a trait preset id. Thus the former pack's `TraitReligious` value
  fails the current add/remove body's label guard; leaving shipped `Religious`
  untouched is necessary. The vanilla migrations strip/rebuild through this
  same function at `Lua/_fixup.lua:2132` and `:2167`; the additional inspiring
  architecture label fixup caller remains at `:2083`.
  `C:/Dev/SMR-SrcArchive/1.1.0.403908/Src/CommonLua/SavegameFixup.lua:34` skips
  already-applied fixups, and `:38` records their completion. The pack's
  `Code/Fix_SaintBlessing.lua:383` presence check and `:384` vanilla application
  therefore add a missing registration without changing 1.1.0 data.
- **SOURCE — sibling and legacy branch:** Empath still uses the same dome
  modifier function, with an empty target trait default
  (`C:/Dev/SMR-SrcArchive/1.1.0.403908/Src/Lua/TraitPreset.lua:52`,
  `Data/TraitPreset.lua:255`–`:269`), so its `Colonist` label branch remains
  untouched. The 1.0.7 add and remove bodies still use the raw label at
  `C:/Dev/SMR-SrcArchive/1.0.7.396349/Src/Lua/ClassDefs/ClassDef-PresetDefs.generated.lua:1783`
  and `:1796`; the current module retains the matching data correction and
  legacy re-base branch. This supports the already-recorded KEEP rationale for
  1.0.7 players receiving the live portal pack; this review does not reopen it.
- **MEASURED input identity / LIMIT:** the assigned module's SHA256 matches
  `CENSUS.json` (`1b4e04679e886672030fe47c7c323e9afbfc10ec1a1866917348d63c572e63a5`).
  The archived settled second boot and coordinator's direct final registry read
  are used. No colony loaded, no suite ran, and
  no save-state restoration or screen result was measured.

## Not checked, by name

- Historical 1.1.0 damaged-save healing cure.
- Visible “Blessed by a Saint” infopanel and morale change in a running colony.
- 1.1.0 healed-save reload silence and idempotence in play.
- A fresh 1.0.7 boot of the current live pack.
- Number or continued presence of players with affected saves.
- Mod-added trait preset behavior.
- Whole-list card consistency and generic card claims, assigned to the coordinator.
