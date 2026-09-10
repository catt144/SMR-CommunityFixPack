# 03c research, laws, missions and progression seam report

## Scope, source and method

This is the durable close-out record for `03c_PROGRESS_SEAM.md`. It compares
Steam build `24995074` in the archived `1.0.7.396349` and `1.1.0.403908` source
trees. The dated `SEAM_COVERAGE.tsv` snapshot was not edited. Its `owner=03c`
partition reconciles to **286 items**: 284 INVENTORY rows in 19 files plus two
CALLERS rows. The prompt's initial reader split was corrected from 50/156/78 to
45+2 / 158 / 81 without changing the total.

Every present body below was read in full in both trees; added/removed rows were
read on their present side and against the replaced behavior path. Supporting
definitions, literal callers, shipped base instances and consumers were opened
only as needed. The parent re-derived all filed findings and the six-row random
sample. No game, module, archived source or DLC/norman interior was changed or
launched.

## Exact coverage receipt

**READ 286; NOT-REACHED 0.** The only HUNKS-ONLY inventory surfaces are CALLERS
`C03016 C03021`; their complete caller and callee bodies were nevertheless read.
`R09783` is a comment-only lexical false positive. `R09791 R09792 R09793 R09794`
are overlapping SPAN-SUSPECT rows; each real one-line compatibility getter was
read separately. No other malformed span or coverage overlap was found.

Exact READ keys by file:

- `Lua/Factions/Elections.lua` (2): `R07833 R07834`
- `Lua/Factions/FactionDef.lua` (28): `R07862 R07881 R07911 R07912 R07913 R07914 R07940 R07941 R07942 R07943 R07944 R07945 R07946 R07947 R07952 R07953 R07954 R07955 R07956 R07957 R07958 R07959 R07966 R07967 R07968 R07969 R07970 R07971`
- `Lua/Factions/Factions.lua` (14): `R07986 R07988 R07989 R07990 R07991 R07992 R07998 R07999 R08000 R08003 R08007 R08012 C03016 C03021`
- `Lua/Factions/FactionsBuildings.lua` (3): `R08016 R08017 R08021`
- `Lua/Factions/LawDef.lua` (49): `R08032 R08034 R08035 R08037 R08038 R08039 R08040 R08041 R08042 R08043 R08044 R08045 R08046 R08047 R08048 R08049 R08050 R08051 R08052 R08053 R08054 R08055 R08056 R08057 R08058 R08059 R08060 R08061 R08062 R08063 R08064 R08065 R08066 R08067 R08068 R08069 R08070 R08071 R08072 R08079 R08080 R08081 R08082 R08083 R08084 R08085 R08086 R08088 R08090`
- `Lua/Factions/Laws.lua` (31): `R08092 R08095 R08097 R08106 R08109 R08110 R08111 R08112 R08113 R08114 R08115 R08116 R08120 R08121 R08122 R08133 R08134 R08135 R08136 R08137 R08140 R08141 R08147 R08153 R08154 R08156 R08157 R08158 R08159 R08162 R08163`
- `Lua/Factions/Legislature.lua` (78): `R08166 R08168 R08169 R08170 R08174 R08180 R08181 R08182 R08183 R08185 R08186 R08187 R08188 R08189 R08190 R08191 R08192 R08193 R08194 R08195 R08196 R08197 R08198 R08199 R08200 R08201 R08202 R08203 R08204 R08205 R08206 R08207 R08208 R08209 R08210 R08211 R08212 R08213 R08214 R08215 R08216 R08217 R08218 R08219 R08220 R08221 R08222 R08223 R08224 R08225 R08226 R08227 R08228 R08229 R08230 R08231 R08232 R08233 R08234 R08235 R08236 R08237 R08238 R08239 R08240 R08241 R08242 R08243 R08244 R08245 R08246 R08247 R08248 R08249 R08250 R08251 R08252 R08253`
- `Lua/MarsGameEffects.lua` (4): `R08645 R08646 R08655 R08660`
- `Lua/MissionProfileDlg.lua` (2): `R08749 R08751`
- `Lua/PreGameMission.lua` (2): `R08957 R08966`
- `Lua/RandomMap/RandomMapGenerator.lua` (1): `R08997`
- `Lua/RandomMap/RandomMapGeneratorEdit.lua` (2): `R09000 R09001`
- `Lua/Research.lua` (11): `R09062 R09073 R09075 R09076 R09106 R09107 R09111 R09114 R09123 R09146 R09153`
- `Lua/ResupplyItems.lua` (2): `R09240 R09242`
- `Lua/Sequences/SA_Gameplay.lua` (8): `R09449 R09450 R09452 R09457 R09459 R09474 R09476 R09479`
- `Lua/Tech.lua` (5): `R09673 R09674 R09675 R09677 R09678`
- `Lua/TechTree.lua` (38): `R09683 R09688 R09691 R09692 R09693 R09696 R09700 R09709 R09715 R09759 R09760 R09762 R09773 R09774 R09776 R09777 R09780 R09783 R09785 R09786 R09787 R09788 R09789 R09790 R09791 R09792 R09793 R09794 R09795 R09796 R09797 R09798 R09799 R09800 R09801 R09802 R09822 R09826`
- `Lua/Traits.lua` (3): `R09915 R09921 R09922`
- `Lua/_GameUtils.lua` (3): `R11625 R11633 R11636`

Reader reconciliation: factions/core 47/47, laws/legislature 158/158, and
progression/misc 81/81. There were no unread remainders or child queues.

## Read-group dispositions

### Factions, laws and legislature

The registry/storage migrations (`FactionDefs`, `PolicyDefs`, `Game`, active-law
helpers), deterministic preset enumeration, VoteOnly filtering, new policy
preparation/action state and quest split are internally connected for their
ordinary base routes. Editor getters/validation stay R4. Two appended optional
parameters are benign F117-shaped changes: `C03016` deliberately keeps hourly
approval scoped by omitting `all_factions`, while `C03021` deliberately keeps
the daily full disaster pass by omitting `stop_only`.

Three defects survive and are filed separately: the new zero-seat disaster
guard (R08000), the pre-existing completed-opportunity expiry gate (R08193), and
the newly orphaned first-session popup (R08236). R07986/R07990 expose a real
activation-versus-recap mismatch only if an assembly choice contains an obsolete
initial law; the shipped 1.1 base choices do not, so the lead is vacuous today.
R08012's unknown-faction fixup omits persisted disasters, but no supported
official removable-faction disaster instance was established; that is a
conditional DLC handoff, not a base verdict. R07913's late validation is an
editor/mod-data smell with no malformed shipped instance.

### Research, map generation, missions and traits

The live DeepScanning definition is `Data/Tech.lua:3934-3961`, not the inert
legacy `Data/TechPreset.lua:847-852` stub. Its `DeepScanAvailable` modifier and
`Effect_UnlockDeeperDeposits` flow through Tech effect application to
`Exploration.lua` and `MarsGameEffects.lua`; orbital probes separately require
AdaptedProbes. This source route refutes the player-report hypothesis that the
DeepScanning effect was disconnected. Actual runtime progression remains
unmeasured, and old saves cannot normally supply a 1.1 fixture.

R09073's EasyResearch loop also selects seven non-researchable initiatives. The
initiative prerequisite comment says they stay locked until their completion
conditions, but the game-rule data deliberately promises to "unlock all
technologies" and the loop discovers rather than completes them. With intent and
final UI behavior unresolved, this is recorded for runtime/owner adjudication,
not filed as a verified defect. R09675's lowercase documentation assertions are
satisfied by Tech's lowercase compatibility getters. R09801 depends on editor
numeric semantics. Neither is a player defect on this evidence.

R08997 repairs old dead/incorrect map-generation paths (the calculated effects
border is now consumed and anomaly marking happens after capacity acceptance).
R08751 removes an unused mission-profile context and fixes signed percent
formatting. R09449/R09450 correctly exclude non-researchable Tech placeholders.
These are PASSING findings, not live defects. R09822 predicts roughly 85 refresh
wakes/minute while the Tech Tree is open, but it has no hard intent tell and no
profile; R09921 does not add a periodic loop. No frame-time claim is made.

## Filed findings and controls

The executable record is `PROGRESS_SEAM_DESK.txt`, produced by
`tools/desk_progress_seam.py` after an explicit clean stale-probe sweep. It loads
the actual archived Lua bodies with named shims for game time, messages, reverse
iteration, faction storage and legislature storage. The zero-seat/one-seat
disaster pair and no-active/active-task expiry pair are discriminating controls.
The popup check is lexical because runtime UI/native dispatch is outside the
deskbench; it proves the old literal caller was removed and no new literal caller
exists, not that dynamic/native dispatch is impossible.

- R08000: 1.0.7 and the 1.1 one-seat control stop/remove an expired disaster;
  1.1 with zero seats retains it and continues its daily update.
- R08193: an expired completed task remains when there is no active task; adding
  a non-expired active-task control lets the same body remove it.
- R08236: old has declaration plus `BeginSession` call; new has only the retained,
  modified declaration. The `EarthCouncilIntro` preset still ships.

The desk does not prove live scheduling, UI rendering, persistence, native
dispatch or a player-visible outcome. Each candidate therefore remains
`cand`/`source-read` with a fresh-1.1 runtime recipe and explicit vacuity.

## FR-1(b), FR-2 and FR-3

All 16 unique tagged rows were read first:
`R08047 R08187 R08188 R08197 R08223 R08232 R08250 R08997 R09001 R09073 R09449 R09452 R09474 R09786 R09822 R09921`.

**FR-1(b).** All six 03c FR-1 rows are base code. Their non-owner paths remain
present: law UI threads/state, base new-game map/research setup and editor-only
resource/Tech actions as applicable. None has a literal norman/thomas dependency.
Source review found no new-game/native crash mechanism and does not close FR-1.
`GameRules.lua:167` is stale-looking but harmless: `PersistLoad` invokes
`LoadGameSettingFixup` before save fixups and already copies `idGameRules` into
`Game`; the later `MoveGamerulesToGame` read is redundant compatibility code.

**FR-2.** The four 03c rows and supporting live Tech/effect/Exploration route are
connected as described above. Editor-only registry migrations are not runtime
proof. The report's “DeepScanning but probes do not deep scan” symptom is
consistent with probes separately requiring AdaptedProbes, not a missing
DeepScanning effect. Source cannot close the field report.

**FR-3.** Seven tagged rows were read. R09822 is the only added short-cadence
work: a 700 ms Tech Tree refresh waiter, profiling-only and not the cause of the
pre-1.1 report. R09921 preserves one real-time thread per passenger launch.
Other tagged rows are editor, one-shot new-game, map-generation or ordinary UI
state work. No frame-time measurement or field-report closure is claimed.

## Reader control and drift

Deterministic random sample seed `31003` selected `R09683 R09762 R08060 R08116
R09787 R08054`. Parent reread each complete body and re-derived the literal or
virtual route: cleanup utility (R4/no literal caller), research preview lock diff
(R1), law-effect stop lifecycle (R1), DataChanged faction table rebuild (R2),
Tech editor display (R4), and law-effect detail text (R1). Score: **6/6 change
classification/body description; 6/6 route precision after re-derivation**.
Eligible positive seeds: **0**, so the positive-seed score is **N/A**, not 4/4.

Caught drift is retained rather than erased: reader counts corrected from
50/156/78 to 47/158/81; the first DeepScanning parser used the first surrounding
Tech block instead of the nearest one and failed, then was corrected to `rfind`
before the recorded passing run; the first plan commit's HEAD was followed by
independent 03b/03d pin commits, with no source-pin change.

## DLC and successor outbox

Base/non-owner routes are established only for the files and shipped base data
named above. `dlccheck` should open the actual official DLC definitions before
answering either conditional seam:

1. R08012: can a supported DLC-disabled save retain a removed faction in
   `factions_disaster`, and can that faction own a persisted disaster? The fixup
   cleans standings, active factions and legislature seats but not this store.
2. R07992: does an official mission sponsor have `.faction` equal to the Assembly
   of Planets, enabling the thomas-specific weight branch? Base data did not.
3. R08645/R08646: identify actual DLC crop/vegetation augmentation effect
   instances before claiming owner-only output changes.
4. R09449/R09450/R09452: confirm DLC Tech groups/placeholder data through the
   real `Tech` registry; do not infer it from the legacy TechPreset stub.

Successors must retain these limits: anonymous/dynamic/native callers, actual
execution, native timing/rendering, consoles, missing assets and incomplete old
DLC remain blind spots. There is no child queue from 03c.
