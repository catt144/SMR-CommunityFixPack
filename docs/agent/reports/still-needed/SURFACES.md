# Whole-list surface comparison — coordinator pass

Coordinator `/root`, 2026-09-12; game 1.1.0.403908; captured site HEAD `a061665`.
This pass reads the WHOLE card and fix list together. Per-module reviews supply
the independent module/consumer leg. No public surface is edited here.

## Headline coverage

SOURCE: `metadata.lua:3` contains 21 headlines under SOME OF WHAT IT FIXES.
SOURCE: `C:/Dev/SMR-CommunityMods/content/fix-list.md` contains 49 folded rows.
Every headline maps to a current row; none points only to a removed row. Module
truth and scope qualifications remain separate, pending the per-module reviews.

| Card headline (short label) | Fix-list file:line | Module |
|---|---|---|
| Surface walks between domes | `fix-list.md:46` | `Fix_VacuumWalks.lua` |
| Rocket arrivals dying en route | `fix-list.md:56` | `Fix_ArrivalDeaths.lua` |
| Arrivals choosing disabled/quarantined domes | `fix-list.md:66` | `Fix_ArrivalDeaths.lua` |
| Half-empty dome refusing housing | `fix-list.md:105` | `Fix_StaleReservations.lua` |
| Vacant bed not offered to homeless | `fix-list.md:118` | `Fix_FreedHousingNotice.lua` |
| Night shift after midnight | `fix-list.md:130` | `Fix_NightShiftWork.lua` |
| Farm oxygen after salvage | `fix-list.md:257` | `Fix_GhostFarmOxygen.lua` |
| Lake burying its constructor | `fix-list.md:229` | `Fix_LakeEntombment.lua` |
| Extender flicker paralysing hubs | `fix-list.md:206` | `Fix_ExtenderFlapChurn.lua` |
| Salvage deleting track and trains | `fix-list.md:324` | `Fix_TrackSalvageWipe.lua` |
| Station demolition deleting trains | `fix-list.md:369` | `Fix_TrainsToVoid.lua` |
| Damaged track unsalvageable | `fix-list.md:335` | `Fix_BrokenTrackSalvage.lua` |
| Connector hex ping-pong | `fix-list.md:388` | `Fix_TrackConnectorPingPong.lua` |
| Destroyed tunnel shortcut | `fix-list.md:267` | `Fix_DestroyedTunnels.lua` |
| Automatic rockets/landers empty launch | `fix-list.md:427` | `Fix_LanderEmptyLaunch.lua` |
| Earth Trade rocket fuel wedge | `fix-list.md:477` | `Fix_TradeRocketFuelRefresh.lua` |
| Jumbo Cave waste-rock wedge | `fix-list.md:510` | `Fix_JumboCaveReinforcementWedge.lua` |
| Philosopher's Stone finale hang | `fix-list.md:498` | `Fix_CrystalMysteryHang.lua` |
| Cave-in requested on absent map | `fix-list.md:561` | `Fix_AnomalyCaveInMap.lua` |
| Gene Forging had no effect | `fix-list.md:139` | `Fix_GeneForging.lua` |
| Domes Overview missing highlights | `fix-list.md:574` | `Fix_DomeOverviewHighlight.lua` |

Paths in the second column are relative to `C:/Dev/SMR-CommunityMods/content/`.
The retired F60 housing-tally row is absent. F51's removed permanent-homelessness
headline is also absent; the retained stale-value row is `fix-list.md:82`.
The similar half-empty-dome headline above belongs to F58, not F60.

## Other card examples and aggregate claims

SOURCE surface-to-surface matches in `metadata.lua:3`:

| Card example or claim | Current supporting rows | Review dependency |
|---|---|---|
| Wisp coexistence payout ~1/1000 | `fix-list.md:524` | WispRewards |
| Wind turbine breakthrough restoration | `fix-list.md:278` | SaveSanitizer |
| Track refund based on stub | `fix-list.md:345` | TrackSalvageRefund |
| Comfort billed beyond journey | `fix-list.md:398` | TrainWaitTime |
| Seven machines with missing FX | `fix-list.md:288` | SilentHitMomentFX |
| Three latent repair rows | `fix-list.md:597`, `:605`, `:611` | DroneTransportMinors, SequenceLatents, LayoutTechLock |
| Three judgment-call rows | `fix-list.md:166`, `:189`, `:437` | DustSicknessBiorobots, ShelterReflex, PayloadTemplateRefill |
| LakeEntombment veto example | `Code/Fix_LakeEntombment.lua:41`, `metadata.lua:38` | Registered ID and code-list membership |

SOURCE: the card itself states no numeric judgment-call count; the count of
three is in the store-card editorial notes and site FAQ. Derive the latent
classification from current primary data as well as the section's prose; three
rows under a heading alone cannot prove that all three remain latent on 1.1.0.

## Whole-list mechanical coverage

SOURCE: `SURFACE_MAP.json` maps all 49 folded rows to all 46 registered modules.
ArrivalDeaths, SaveSanitizer and WispRewards each have two rows; all others have
one. No row is assigned only to a deleted/unregistered module. This is coverage
of the maintained source lists, not clearance of every row's substantive claim.

SOURCE: `SURFACE_COPY_CHECK.json` extracts the five maintained card bodies:
metadata description, plain/Steam STORE_CARD_LIVE records, plain/Steam upload
backups. All five contain the same 21 headlines, the latent count of three, and
the LakeEntombment example. Headline equality proves consistency; any shared
overclaim would remain shared until corrected through the release workflow.

## Final checks still pending

- Module-review findings integrated into the headline and aggregate conclusions.
- Named unverified routes retained, including hardware cure and live page receipt.

## Not checked

Live Steam/Paradox page bodies, deployed site content, localisation rendering,
player outcomes, affected F102 hardware, 1.0.7 runtime, and the owed 94-probe colony
sitting were not checked by this surface pass. These are committed-source claims,
not a claim that any pending wording is already published.
