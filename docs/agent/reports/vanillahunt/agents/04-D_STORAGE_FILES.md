# 04-D skim — storage and removed/added lists

Banner: plan brief `41672f1`; units given: `STORAGE.tsv` status lists and `FILES.tsv` status/bucket lists; date: 2026-09-10.

This is a list-level address/name skim, not a declaration-by-declaration clearance.

## Skim table

- `STORAGE · same (1007)` — nothing odd at list depth; addresses are unchanged.
- `STORAGE · added (102)` — nothing odd; these are new stored names, with no old address to strand.
- `STORAGE · removed (36)` — nothing odd after old-address searches. Apparent hits are compatibility readers or deliberate replacements: `ColonistMaxDomeWalkDist` / `ColonistMinDistToIgnorePassage` moved to `g_Consts`; `LoadedRealTime` / `SavegameMeta` moved under persisted save metadata; lockable-preset globals moved to player fields; `g_DisastersSettings` survives only in migration reads; `g_StoryBitsScopeStack` and `state_growing_vegetation_info` survive as non-persisted compatibility globals.
- `STORAGE · kind-changed (1)` — FLAG control: `Landscapes` changed `GameVar` to `MapVar`; old `Lua/Landscape/Landscaping.lua:455` becomes map-explicit current `:509`. Drilled through F115/F34(d); no separate storage candidate.
- `STORAGE · moved-file (9)` — nothing odd after reader checks. `MaxModDataSize`, faction globals, rocket drone limits and game-speed constants retain the same names at their new files.
- `FILES · removed hand (18)` — nothing odd: each removed path was traced as relocated/split or retired with no surviving old-path loader/name reference. The old CommonLua mod files moved to `CommonLua/Modding`; tutorial code was split into its current files.
- `FILES · removed generated (18)` — nothing odd: generated monoliths were replaced by per-registry generated/data folders; surviving declared names were found in 1.1.0.
- `FILES · added hand (72)` — nothing odd at list depth; new loader-visible files are covered by the system skims, especially 04-C's MapGen/render notes.
- `FILES · added generated (94)` — nothing odd at list depth; registry content is covered by 04-E.

## Ranked flags and limits

- One flag, `Landscapes`, drilled and already represented by F115/F34(d). No FILE verdict and no undrilled flag.
- NOT skimmed: none of the 9 list units.
- Parent reopen sample: removed `CommonLua/Classes/Mod.lua` relocation and removed generated faction monolith, 2/2 still accounted for by current paths/names.
- No F114–F117 control beyond the `Landscapes` calibration was assigned here.
