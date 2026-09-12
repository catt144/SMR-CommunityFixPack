# FounderTraitNotification — one-module review

Agent `/root`, 2026-09-12, anchor `2983fac`. No disagreement found.

| module | entry | applies? | consumer still reads it? | row true? | bullet true? | verdict | evidence file:line on 1.1.0.403908 | basis | what I did NOT check |
|---|---|---|---|---|---|---|---|---|---|
| Fix_FounderTraitNotification.lua | F23 | yes, final registry active | yes, trait grants emit message and notification consumes founder/trait | yes, eligible Founder grants remain silent in vanilla | n/a | KEEP | 1.1.0.403908 Lua/ColonyViability.lua:300 and :309; Lua/Units/Colonist.lua:527; Data/NotificationPreset.lua:313 | SOURCE | current live render/grant, save/load, legacy runtime |

Primary root: `C:/Dev/SMR-SrcArchive/1.1.0.403908/Src`.

- `Lua/ColonyViability.lua:300` still defines an array containing the three group
  names. `:309` indexes it with the group string, so the original handler cannot
  reach `:312` for the eligible grants. No vanilla replacement repaired this body.
- `Lua/Units/Colonist.lua:527` emits the same message after adding a trait.
  `Lua/Buildings/OpenAirGym.lua:10` remains one ordinary caller. The additive
  handler's event path is live; initial traits are intentionally excluded.
- `Data/NotificationPreset.lua:313` reads founder and trait from the notification
  parameters, and `:316` defines the same notification ID. This is an actual
  shipped consumer of the handler's output, beyond the module's counter.
- `Code/Fix_FounderTraitNotification.lua:52` uses a set for the same three groups;
  its handler preserves the initial-grant and duplicate-notification gates.
- Registry archive `docs/archive/logs/stillneeded_registry_Mars.exe-20260912-00.29.01-6a91a190.log:255`
  measures active. The pinned vanilla body and defect pass `BODYCHECK.txt`.
- `C:/Dev/SMR-CommunityMods/content/fix-list.md:181` describes the missing
  notification and matches this retained path. No dedicated metadata headline.

Not checked: a current live Founder trait grant or rendered/clicked notification,
organic grant frequency, current TestKit behavior firing, menu enable/reload,
save/load/uninstall, or 1.0.7 runtime. The entry's historical PT-44 evidence is
preserved with its original date and is not relabelled as a current-game run.
