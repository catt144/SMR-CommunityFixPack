# C74 sound sweep — every FX that waits on an animation moment (desk, both trees) — 2026-09-10

Handoff `HANDOFF_DISPATCH_2026-09-10.md` §3. Desk only: 1.1.0.403908 and 1.0.7.396349
source trees, read-only. Two sub-agents did the census; the coordinator re-derived
every claim below that this report relays (see "Re-verified here"). Raw agent reports,
verbatim: `c74_sweep/sweep_A_consumers.md`, `c74_sweep/sweep_B_fxcensus.md` (NOT
authority; where they disagree with this file, this file was re-checked).
⛔ Nothing here is witnessed in play except the two C74 rows (hammer, MOXIE).

## The mechanism (one sentence)

Every Lua moment reader ends in `GetEntityAnimMoments`, which reads only
`Presets.AnimMetadata[<anim entity>][<anim name>]` (1.1.0 `CommonLua/Classes/AnimMoment.lua:5-16`,
`EF-086`); only 5 groups ship; so an FX that only an animation moment can fire is
dead on every other entity, whatever tracker drives it.

## Two trackers, one shared failure

| tracker | anim argument | preset needed | users |
|---|---|---|---|
| `BaseBuilding:TrackMultipleHitMoments` (1.1.0 `Lua/Buildings/BaseBuilding.lua:1037-1079`) | raw INDEX (`:1045-1046`, `:1053`, `:1065`) — broken even with a preset | yes | 5 classes set `track_multiple_hit_moments_in_work_state` (below) |
| `TrackAllMoments` (1.1.0 `Lua/Buildings/Building.lua:3364`) | NAME (`GetAllAnimMoments` `:3347`, `TypeOfMoment`→`GetChannelData` `AnimMoment.lua:107`) — correct | yes | RCDriller, TheExcavator, ShuttleHub, WaterExtractor, RCTerraformer (via RCTransport) |
| `Metatron:StartAnimMomentsThread` (`Lua/Mysteries/Metatron.lua:50-88`) | raw INDEX (`:52-53`, `:57`, `:69`) | yes | Monolith (Mystery 12) |

With no preset, `TrackAllMoments` reads `GetAllAnimMoments` = `{}`, `TypeOfMoment(1,1)` =
`""`, and its thread exits at once (`Building.lua:3369-3379`): silent, no error, no cost.

### The five tracker-enabled classes (`TrackMultipleHitMoments`)

| class (1.1.0) | tracked attach | Working `hit-moment*` FX keyed to it | player loss |
|---|---|---|---|
| `PreciousMetalsExtractorBase` (`MetalsExtractor.lua:25`) | `UniversalExtractorHammer` | 11 (C74) | yes — C74 |
| `MOXIEBase` (`MOXIE.lua:5`) | `MoxiePump` | 5 (C74) | yes — C74 |
| `ElectrolyzerBase` (`Electrolyzer.lua:5`) | not traceable from Lua | 0 | none |
| `MicroGExtractorBase` (`MicroGExtractor.lua:123`) | not traceable from Lua | 0 | none |
| `PreciousMineralsExtractorBase` (`PreciousMineralsExtractor.lua:17`) | — | — | dead code: 0 inheritors/templates, both trees |

## Candidates (FX authored, samples ship, never fire) — 1.1.0, all also dead in 1.0.7

| # | entity (tracked object) | route | dead FX | filed |
|---|---|---|---|---|
| 1 | The Excavator arm `ExcavatorShovel` (`TheExcavator.lua:47`, `:120`) | TrackAllMoments | 24 `ExcavatorDigging` Hit1-12 / Out1-12 dust particles (`ActionFXParticles.lua:115-530`) | C77 |
| 2 | Rare Metals hammer | TrackMultipleHitMoments | 11 | C74 |
| 3 | Metatron `Monolith` | own thread | 7 `MetatronRotation` `End1..7` particles | C74 |
| 4 | MOXIE pump | TrackMultipleHitMoments | 5 | C74 |
| 5 | Shuttle at a Shuttle Hub (`ShuttleHub.lua:1632`, `:1649`) | TrackAllMoments | `ShuttleHubEnter` Hit sound `Unit Shuttle LandHub` (`ActionFXSound.lua:13480`), `ShuttleHubExit` Hit sound `Unit Shuttle Takeoff` (`:13519`) + 2 particles (`ActionFXParticles.lua:8404`, `:8421`) | C77 |
| 6 | Water Extractor pump `WaterExtractorPump` (`WaterExtractor.lua:112-116`; MicroGAutoWaterExtractor inherits) | TrackAllMoments | 3 `working` Hit sounds (`ActionFXSound.lua:20276`, `:20286`, `:20296`) | C77 |
| 7 | RC Terraformer (`RCTerraformer.lua:35`, `:96-102` → `RCTransport.lua:133-134`) | TrackAllMoments | `Construct`/`Load` Hit1: 2 particles + sound `Unit RoverDozer Shovel` (`ActionFXSound.lua:7031`) | C77 |
| 8 | RC Driller (`RCDriller.lua:105`) | TrackAllMoments | `Drill` Hit particles (`ActionFXParticles.lua:6999`) + sound `Unit RoverDriller DrillHit` (`ActionFXSound.lua:5568`) | C77 |

Samples ship (byte search of `Packs/Sounds.fpk`, 90,324,753 B, 2026-09-10):
`shuttletransport_enter1`, `shuttletransport_takeoff1`, `roverdriller_drillhit1`,
`roverdozer_shovel1`, `extractorWater_workpeak1` all FOUND; control
`extractorUniversal_workpeak5` (C74's known sample) FOUND; fabricated
`zz_fabricated_c74_sample` ABSENT. The six sound presets exist (`Data/SoundPreset.lua`
`:11444`, `:15742`, `:19323`, `:19414`, `:20133`, `:20161`).

## Unreachable even WITH presets (no code fires the moment) — noted, not filed

- **Metatron `hit-moment1..7`** — 7 `MetatronRotation` sounds. The thread is created
  only with `"Start"`/`"End"` (`Metatron.lua:86`) and fires `moment .. i` (`:78`), so
  `hit-moment<i>` is never emitted. Corrects C74's "7 sounds, predicted".
- **Rare Metals `hit-moment3`/`hit-moment4`** — the tracker's list for this class is
  `{"hit-moment1","hit-moment2","hit-moment3"}` (`MetalsExtractor.lua:25`), cycled over
  the hit COUNT (`BaseBuilding.lua:1054`, `:1074`): with the proven 2-hit preset only
  1 and 2 fire; `hit-moment4` (2 sounds) never can. Bears on C74's build (preset hit
  count), not a separate defect.
- **HydroponicFarm Lift/Spray/Rotate** — 10 sounds; `FarmHydroponic:StartAnimThread`
  is empty (`Farm.lua:1033-1034`, both trees). Looks like a deliberate stub; a design
  question, not filed.
- **DroneHub ConstructingDrones Hit1-4** — 4 particles (agent B; not re-derived here).
- **`dig-reveerse`** — 1 sound keyed to a typo of `dig-reverse` (agent B; not re-derived).

## Settled

- **The 13 actor-less `hit-moment*` entries are code-fired, fine:** 12 ElectrostaticStorm
  (`DustStorm.lua:267`, table-form PlayFX; a nil actor matches `any`, `ActionFX.lua:4109-4145`)
  + 1 MysteryDream (`Colonist.lua:4960`/`:4965` via `Unit.lua:89`). (Agent B; the peer
  session's caveat that these decide the Electrolyzer/MicroG question is answered: they
  resolve to neither.)
- **Moment consumers classed NAME vs INDEX:** INDEX callers are only
  `TrackMultipleHitMoments`, `Metatron`, and an unreachable `PairMarker:TriggerAfter`
  fallback (`ClassDef-PresetDefs.generated.lua:1286`, no other file names PairMarker).
  `TimeToMoment`/`TypeOfMoment` convert internally via `GetChannelData` — their callers
  are safe regardless.
- **No game class overrides the moment readers:** the only other definitions of
  `GetAnimMoments` are the Animation Moments Editor's (`CommonLua/Editor/AnimationMomentsEditor.lua:378`,
  `:593`); the same regex hits all six `CObject` definitions (control).
- **1.0.7 → 1.1.0:** same candidate set (1.0.7 has one extra Water Extractor sound);
  every candidate was already dead in 1.0.7. Presets: 4 groups → 5 (BakeryHands, DLC).

## Re-verified here (coordinator, from the primary source)

TrackAllMoments route (`Building.lua:3346-3379`, `AnimMoment.lua:35-37`, `:100-111`,
`:127-138`, `:304-331`); the six `TrackAllMoments` call sites (grep, 7 hits incl. the
definition); RCTransport `:122-135`; the five tracker classes (grep); Metatron `:50-88`;
`FarmHydroponic:StartAnimThread` empty; the sound presets and ActionFXSound rows
cited above; the Sounds.fpk sample search with both controls; the override control.
NOT re-derived: the particle row line numbers (agent B's), DroneHub and `dig-reveerse`,
the 35 "code-fired by proximity" rows agent B marked without per-row tracing, and the
340 `start`/`end` rows (agent B did not trace them per Action).

## Open, for the live check

- `GetAnimEntity` is engine-side; the census assumes it does not redirect these
  entities onto one of the 5 preset groups. The live readout below measures the result
  directly.
- Moments in entity XML: `LuaExports.lua:204-211` documents a native `GetStateMoments`;
  the Lua one (`AnimMoment.lua:334`) overrides it and reads presets only (`EF-086`).
  The C74 live count (0 with the Lua path) already sampled this on the hammer.

**Live readout (one line, parse-checked + desk-run against stubs for the absent /
no-attach / found cases, 2026-09-10):** `scratchpad`-built, carried in checklist 139.
It prints `C74 sweep: <class>[n]:<tracked class>/<state>/<moment count>` per candidate
present on the map; a count of 0 on a working unit, with the unit visibly animating,
samples the claim.
