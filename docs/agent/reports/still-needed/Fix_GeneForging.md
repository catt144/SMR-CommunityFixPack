# GeneForging — one-module review

Agent `/root` (coordinator's local review), 2026-09-12, anchor `2983fac`.
**KEEP.** The current vanilla rare-weight helper still ignores Gene Forging.
Record freshness: F41's historical "have only" limit is no longer the current
call topology; 1.1.0 GetRandomTrait itself calls the helper for its default rare weight.
This broadens the helper's consumers and does not make the module redundant.

| module | entry | applies? | consumer still reads it? | row true? | bullet true? | verdict | evidence file:line on 1.1.0.403908 | basis | what I did NOT check |
|---|---|---|---|---|---|---|---|---|---|
| Fix_GeneForging.lua | F41 | yes, final registry active | yes, GenerateTraits and GetRandomTrait consume bonus | yes, Gene Forging is still omitted by vanilla | yes, same current defect | KEEP | 1.1.0.403908 Lua/Units/Colonist.lua:4399; Lua/Traits.lua:1049 | SOURCE | current colony bonus ladder/distribution, data-map runtime value, exact gain callers, save/load, legacy runtime |

Primary source root `C:/Dev/SMR-SrcArchive/1.1.0.403908/Src`:

- `Lua/Units/Colonist.lua:4399` reads only GeneSelection, `:4400` resolves its
  param1. The GeneForging term is still absent. `Data/Tech.lua:8975` names param1
  and `:8976` supplies 50, with the explicit rare-trait-bonus comment at `:8977`.
- `Lua/Units/Colonist.lua:4419` reads GetRareTraitChance and `:4422` passes its
  result to the ordinary generated-trait draw. `Lua/Traits.lua:1049` also calls
  the helper when no explicit rare weight is supplied. That current fallback
  replaces the historical expression which used zero instead. `:1064` passes
  the resulting modifier to CalcTraitWeight and `:1035` applies it to rare
  weights. The game still reads precisely the value the wrapper adds.
- `Code/Fix_GeneForging.lua:116` onward reads the live Techs preset's ResolveValue
  at call time, falls back to legacy TechDef, and its global wrapper delegates
  the original result/arguments before adding Forging only when researched.
  It keeps vanilla's GeneSelection contribution rather than replacing it.
- Direct registry archive
  `docs/archive/logs/stillneeded_registry_Mars.exe-20260912-00.29.01-6a91a190.log:244`
  measures GeneForging active. This does not measure the live researched-tech
  bonus ladder; that is a separate runtime limitation.
- `C:/Dev/SMR-CommunityMods/content/fix-list.md:139` and `metadata.lua:3` describe
  Gene Forging doing nothing before the repair; both remain supported. The site's
  additive statement matches the wrapper. No current row correction is required.

Not checked by name: 1.1.0 live bonus values with neither/each/both techs,
probabilistic outcomes, exact school/sanity/newborn callers and their explicit
rare-weight arguments, current Techs.GeneForging runtime value, menu-enable,
save/load/uninstall, and fresh 1.0.7 runtime. Historical witnessed values in F41
remain historical; no test status is upgraded.
