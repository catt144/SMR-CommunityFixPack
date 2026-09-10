# HUNT_AUDIT — the vanillahunt chain's terminal audit (link 99)

Run 2026-09-10 by `smr-bugfixpack-f8` (Fable) on a folder holding `99_TERMINAL_AUDIT.md`
+ `README.md`, chain commits `c0e8bc8..f8bdb2b`, both archives re-hashed. Nothing here
is `tested`; every verdict below is a source verdict about a source claim.

> ⚖️ **Rulings in one line each.** Instruments: **SOUND WITH STATED GAPS** — and one gap
> the chain did not state is now measured (§1.4). Controls: re-derived, the parent's 4/4
> ruling stands, my blind sample agrees 17/20 on routing with 0 hidden value changes.
> Findings: of the 12 P2 entries re-derived from the trees, **see §3** (holds / weakened /
> refuted per entry). Coverage: the chain read 46 % of the changed hand rows at row level,
> 0 % of the unchanged tree on its own account, and its file-level skim is the only read
> the 1,281 table-level hunks ever got. Yield for a player: §3.5, plainly.

## 0 · How it was read, and the pin

- **Order actually used:** `git log -30` · `git pull` (up to date) · `ListAgents` (9 peers,
  none in this lane; the one unstaged peer file, `bugs/C77.md`, was never touched) ·
  README (whole) · STATE · TRIAGE (whole, §0–§04) · the six `agents/*.md` (whole) · all 24
  chain-filed entries (C56–C73, C75–C76, C78–C81) · the seven consumed prompts recovered
  with `git show <sha>^:…`. ⚠️ **Deviation:** the `## Notes from upstream` section was read
  FIRST, not last — it is appended to the same file as the brief and `cat` showed it before
  any artefact. My first view therefore formed with the links' own claims in context; the
  passes below were run against the artefacts and the trees, not against those notes.
- **Pin:** every TSV banner carries `09d95e3448573dc3…` / `a4577da25cb3fe85…`; both
  `MANIFEST.sha256` files re-hashed byte-for-byte to those digests (4,448 / 4,717 files),
  and every manifest line matched its file. The buildid did not move during the chain
  (STATE, TRIAGE §0.1, §04 all read `24995074`); every link ran against the same trees.
- **Stop conditions:** folder held exactly `99` + README; the four seed rows are classed in
  `INVENTORY.tagged.tsv` NOW exactly as §2 records (checked, §2.1); instruments not UNSOUND.
- **Tools used beyond the shipped ones:** seven scratch scripts (soundness sample, gap
  measurement, blind set, planted trees, pair recount, reach, reopen); four re-derivation
  subagents for pass C, each given only a one-sentence claim and both trees, ordered to
  derive before opening the entry (brief kept in the scratchpad; their returns are quoted
  in §3, and I spot-read C76, C79, C80 and the `ResolveMap(City)` rejection myself).

## 1 · Instruments — SOUND WITH STATED GAPS

### 1.1 Selftests, and what they assert versus print
- `treediff --selftest`: **24 PASS / 0 FAIL, exit 0** — 19 planted (PART 1) + 5 real-tree
  seed checks (PART 2). Every case 01 §2.B.7 required is a `check()` call that gates the
  exit code: body, leading parameter, removal, addition, rename, CRLF-only not-a-row,
  comment-is-a-row, one-line over-span pinned, `SPAN-SUSPECT` flagged, `MULTI`; v1.1's six
  and v1.2's three are asserted the same way. PART 2 asserts, not prints.
- `presetdiff --selftest`: **16 PASS / 0 FAIL, exit 0**, every 01 §2.B2 fixture case
  asserted (numeric, nested string, key added/removed, preset added/removed, reorder-only
  no-row, `T-ID` same-text vs changed-text, plus FORMAT, SAVE-ID, unchanged key, embedded
  function, pair form, REINDEX). ⚠️ **PART 2 ("falsify each churn RULE on the real trees")
  is PRINT-ONLY**: it prints 5 of 20 sampled rows per class and contains no `check()`; the
  real-tree churn control is a human read, never a gate. 01 said so ("printed for a human")
  but §0.12's "16 PASS" line reads as if the real-tree part were asserted. It is not.
- Both headers were read for overstated justification (01's own drift #5): `presetdiff`'s
  is corrected as 01 says; `treediff`'s makes no measured claim it does not carry.

### 1.2 Churn rules re-sampled, 10 per class, seed 99
| class | rows | read | result |
|---|---|---|---|
| `REINDEX` | 10,462 | 10 | every row one-sided `<absent>`; two traced in the trees (`CommandCenterRow` `Shape="InHHex"` moved line 106→115; `Mystery 7` `TensionReduction` count 20 both sides) — **0 hidden value changes** |
| `REINDEX-SWAP` | 1,924 | 10 | **10/10 are real value-vs-value differences** (`DormantLife_FollowUp4 Parameters[5].Value 6→20`, `Policy_ResearchFocus_Engineering FactionLikes[3].Faction NASA→IMM`, `MarsDemocraticParty tasks[9].__class …`) — correctly routed as READ (03: 217 rows per row; 04-E: 1,707 rows at registry level only, §4) |
| `T-ID` | 22 | 10 | identical text, id only — 0 misses |
| `COMMENT` | 1 | 1 | a double space inside a `params` string — inert |
| `added-preset` / `removed-preset` | 1,471 / 894 | 10+10 | make no claim; sampled for shape only |
| `FORMAT` / `SAVE-ID` | 0 | — | unfalsified on real data (01's own statement stands) |
No class is voided.

### 1.3 Planted fresh changes (A.2) — one row each, no cascade
Copies of four REAL 1.1.0 files into scratch `old/` and `new/` (⛔ nothing written under
the archive), then both tools on the pair:
| planted | tool said |
|---|---|
| body edit inside `HotelBase:SetTouristOnly` | `body` row, `hand` |
| leading parameter on `HotelBase:GetUITouristOnlyStatus()` | **pure `sig`** row (body byte-identical) — the F115 shape |
| `Data/Animal.lua` `herd_size` 25→26 | one `PRESETS` row, churn `none`; file listed in NOROWS as `reader=presetdiff` |
| one-line table-field method `Key = function(entry) … end,` edited in `Lua/GameOverlays.lua` | one `body` row flagged `INDENTED,ONE-LINE` (also `MULTI`, `DECL-ONLY`); the unchanged sibling fields produced **no** rows |
| new one-line field `PlantedNew` inserted above it | one `added` row `INDENTED,ONE-LINE` |
| a `Run = function(seq_state)` step inserted among same-named steps in `Mini_Mystery 1.generated.lua` | **one** `body` row on the enclosing `Create@…` (INDENTED) — in the real scenario files the steps sit INSIDE `Create`, so an inserted step surfaces as the outer function's body row, exactly as 0.13 states; no per-step rows, no cascade |
Six planted changes → six rows. Banner integrity (A.3): both digests equal the fresh
re-hash (§0).

### 1.4 Soundness sample (A.4) — seed `2026091099`, 5 `hand` + 2 `generated` changed files
| file | hunks | accounted by | unaccounted |
|---|---|---|---|
| `Lua/X/ItemsMenu.lua` | 7 | 5 rows R11141–R11145, every hunk inside a span | 0 |
| `Lua/Buildings/MonumentOfMarsLiberty.lua` | 2 | R06242 (H2) | **H1: `__parents` gains `"Decoration"` — a class-parent change, no row, and NOT in NOROWS because the file has a row** |
| `Lua/Buildings/AutomaticMicroGExtractor.lua` | 1 | NOROWS `NONE/yes/2` (04-A skimmed it) | 0 |
| `Lua/UI/SaveLoad.lua` | 5 | R10223–R10225 | 0 |
| `Lua/Buildings/Hotel.lua` | 7 | R06157–R06160 | 0 |
| `Data/StoryBit/IncreaseResourceCost_Politician.lua` | 1 | 1 PRESETS row `none` | 0 |
| `Data/XDef/CommandCenterBuildingsOverview.lua` | 8 | 8 PRESETS rows `none` (text changed, so correctly not `T-ID`) | 0 |
One behaviour-changing hunk in seven files escaped both instruments. ⭐ **Measured
tree-wide (my `a4_gap.py`, both archives, difflib opcodes vs the tagged spans):** of the
**699** changed hand files that have ≥1 inventory row, **368 files carry 1,281 hunks
(4,542 non-blank lines) that lie outside every row span on both sides** — 916 table/field
lines, 71 `__parents`, 47 `GameVar`/`MapVar`/`const`, 12 `DefineClass` openers, 76
comments, 159 other. NOROWS lists a file only when it has ZERO rows, so this class is
invisible to 02's row partition and to the 03 family; **the only read it ever got was 04's
file-level skim**, whose unit was the file's changed hunks (§4). 02 §1.7 admitted the class
exists "tree-wide and unmeasured"; it is now measured. ⇒ **SOUND WITH STATED GAPS**: the
stated ones (indent-0 + orphan declarations only, anonymous `function(` literals,
`SPAN-SUSPECT`, generated-only preset scope) plus this one, which was stated as a hole and
is now a number.

### 1.5 The one-line-function trap (A.5)
01 MEASURED it (banner line 7: 441 self-closing declarations, 567 spans reaching EOF; 133
rows flagged `SPAN-SUSPECT`). Effect on coverage claims: 02 excluded the 79 hand
body/sig `SPAN-SUSPECT` rows from the fan-out (§4 lists them by name), so **79 changed
hand rows were never classified by any agent**; 03c read its 4 as one-line getters; the
rest reached 04 only through the file skim. The `ONE-LINE` deviation of v1.1 (hash the
declaration line alone) was sampled 10 rows against the raw files: all 10 are genuinely
one-line (9 `added`, 1 `body` where 1.0.7's multi-line `GetObjectItem` became a one-liner)
— it hid nothing in the sample. The v1.1 `@anchor` labelling limit re-derived: **11**
INDENTED added/removed pairs share a file and an ihash (mine: 9 `generated`, all
`TraitPreset.lua` `apply_func→OnApply`-style renames, + 2 `hand` `preset_filter` fields
whose anchor line moved; c3 reported 11 / all generated — the total matches, the bucket
split differs by two rows; a labelling matter either way).

## 2 · The controls, re-derived

### 2.1 Seeds — classed NOW in `INVENTORY.tagged.tsv`
| seed | rid | class | verdict | matches ledger |
|---|---|---|---|---|
| F114 `Train.UnloadAll` | R10714 | `(i)+(g)` | WORTH-READING, `GUARD+` both guards named | ✅ |
| F115 `LandscapeForEachUnit` | R08560 | `(b)` | WORTH-READING, "leading map param"; smell = the known dead `filter_embark` | ✅ |
| F116 `DemolishAndSplitTrack` | R06991 | `(a)` | WORTH-READING, `ProcessAllElements` pre-pass named | ✅ |
| F117 `ChooseDome` | R11621 | `(b)` | WORTH-READING, `traits→colonist`, callers enumerated, `DroneFactory.lua:230` traced | ✅ |
**Content 4/4, strict label 2/4 — the parent's 4/4 ruling is UPHELD.** (i) is README §2's
own derived form of a body change and F114's change is two guards; (b′) needs a same-tree
stale caller and vanilla has none (`CALLERS.tsv`: 8 changed + 1 new + 0 same), so (b) is
the right class for the vanilla row. Nothing was re-scored; no stop condition fired.

### 2.2 Blind reclassification, 20 random fan-out rows, seed 99 (my verdicts written before the key was opened)
| measure | agreement |
|---|---|
| `WORTH-READING` vs `CHURN` | **17/20** — the 3 splits (R10251, R01453, R07157) are all *mine = CHURN, agent = WORTH-READING*, i.e. the agent routed MORE to reading, never less |
| agent-`CHURN` rows that were actually a value change | **0 of 4** (R06480 dead local, R02210 helper rename, R07822 equivalent accessor, R08795 restructure) |
| primary class | 16/20 (splits on (a)/(i), (a)/(d), (b′)-follower vs (a) — the same soft edges §2.2 reported) |
⇒ 02's "reached" claims are not inflated by mislabelled churn on this sample; the 473
`CHURN` rows remain read by exactly one agent each (§4). ⚠️ One convention drift worth
naming: `table.ifilter` callback followers were classed `CHURN` by B09 and `WORTH-READING`
by B24 — a cross-agent inconsistency in the 20-row sample, harmless to routing.

### 2.3 The 03 family's and 04's controls
- 03/03b/03c/03d each report a parent random sample with 6/6–8/8 agreement and **0
  eligible seeded positives** (their rows held no seed). Not reproduced here (each used a
  `.NET Random` the audit would only be re-running); instead every P2 entry they filed was
  re-derived from the trees (§3), which is the stronger check.
- 04: the four seed FILES are flagged in `04-A` (Train, Landscaping, TrackElement) and
  `04-B` (`_GameUtils`) — **4/4 verified in the reports**. 04's "10/10 reopen" is its own;
  **my reopen of 6 random `nothing odd` units (2 per skim agent, seed 99): 6/6 agree at
  skim depth — but 2 needed a chase to agree**: `MartianAssembly.lua` lost `AssemblyBase:
  ClearSession` (0 callers in 1.0.7, dead code removed) and `locutils.lua:48` changed
  `string.concat`'s first argument (the contract `(sep, …)` is identical in both trees —
  1.0.7 had passed the path as the separator; 1.1.0 FIXED it). And `Construction.lua`'s
  `nothing odd` covers a **1,711-line diff**: a one-line skim verdict on a diff that size
  is a statement about what was noticed, not what is there.

## 3 · The findings

Sample: **all 12 P2 entries** the chain filed (C58, C63, C64, C66, C67, C68, C69, C75, C76, C78,
C79, C80 — 12 of 24, the brief's "at least a third, all P1/P2"; there are no P1s) plus 04's
strongest REJECT (R08311) and its `GetEnvironment(City)` correction. Each was re-derived from
the two trees by an agent given only a one-sentence claim, ordered to derive and attempt a
refutation BEFORE opening the entry; I re-read C76, C79, C80's cited bodies, the C80
refutation chain and the `ResolveMap(City)` question myself (rule 14). The 12 P3 entries
(C56, C57, C59–C62, C65, C70–C73, C81) were read for consistency only and are unchanged.

### 3.1 Ranked by player severity
| # | entry | what a player would see | sorter | cause | falsifier state | verdict |
|---|---|---|---|---|---|---|
| 1 | **C82** (new, filed by this audit, un-audited) | after The Incident's "Stop all Fusion Reactors" reply, every reactor stays off for good | base/non-owner | PASSING (both trees) | needs a game (ck140 fixture, one extra reload) | found, one read only |
| 2 | **C66** | asking an RC Transport to dump one resource group dumps everything it carries | base | DIFF-CAUSED | needs a game (UI click; recoverable piles) | **HOLDS** |
| 3 | **C63** | a Radicalization/Renegades disaster never ends once its faction loses every seat — and its card is hidden, so nothing shows | base | DIFF-CAUSED | executing desk (`desk_progress_seam.py`) + game | **HOLDS** (+3 adjacent tells, §3.2) |
| 4 | **C69** | Number Six's "attacks intensify" phase is one 3-drone burst behind two popups | base | DIFF-CAUSED (via the instant-research model) | recipe vacuous by construction | **WEAKENED** — loss real, stated cause wrong |
| 5 | **C64** | a Faction Opportunity's +0.6 approval bonus can last forever — a gain | base | PASSING | executing desk + game | **HOLDS** |
| 6 | **C75** | new Fusion Reactors stay buildable while the story says they are suspended — a freedom | base | PASSING | needs a game | **HOLDS** |
| 7 | **C78** | migrated Astrogeologist saves keep +10 % on four extractor labels on top of the new bonus — a gain; not loadable on Steam | base | DIFF-CAUSED | source-only (non-Steam build needed) | **HOLDS**, gain not loss; one UNSETTLED build-generation question |
| 8 | **C67** | a diner can admit a few extra meals past its per-shift cap — a gain | base | new-code defect (the "removed kick" is not the cause) | executing desk (`desk_caller_seam.py`) | **HOLDS**, severity overstated |
| 9 | **C79** | scenario tech reveals refund 20 % of one tech point's RP whatever the authored cost — a small uniform gain, direction inverted | base | DIFF-CAUSED (research model) | source-only | **WEAKENED** — dead argument real, the "requirement" no longer exists |
| 10 | **C58** | 4 % of a starving colonist's reserved pile portion can spoil in transit; the Food-Depot half cannot happen (depots are `dome_forbidden`) | base | DIFF-CAUSED | needs a game (native request semantics) | **WEAKENED**, one citation wrong |
| 11 | **C76** | nothing visible: 1.1.0 has no per-tech price for the 26 authored costs to set | base | DIFF-CAUSED | recipe vacuous by construction | **WEAKENED** — real only if the 13 techs were meant to be initiatives (UNSETTLED) |
| 12 | **C68** | a colonist whose entry fails still eats its reserved meal — but the named cross-map trigger is gated out before the body | base | DIFF-CAUSED | executing desk proves the body, not reachability | **WEAKENED** |
| 13 | **C80** | nothing: demolishing an elevator mid-lead-in evicts the traveller to Idle before the read | base | PASSING | source-only | **REFUTED** (`Holder:Done` kick; entry keeps the refutation) |
| — | R08311 (04 REJECT) | none: legacy rocket classes were already dead in 1.0.7 (`UpdateOldRockets` ships there too) | — | — | source-only | rejection **HOLDS** |
| — | `GetEnvironment(City)` (04 REJECT) | none: `City` inherits `Object→CObject→MapObject`, uses its own `GetMap()` at `City.lua:150,153,616,625`; `GetEnvironment` falls back to `""` anyway (`MapData.lua:86-90`) | — | — | source | rejection **HOLDS** |

### 3.2 Per-entry notes (the audit stamps are in each entry; the new evidence, briefly)
- **C58:** pile leg holds; Food-Depot leg unreachable (`GetClosestFoodPile` scans the dome
  label, every depot template is `dome_forbidden = true`, 21/21); `Lua/BuildingTemplate/
  StorageFood.generated.lua` does not exist — `Data/BuildingTemplate/StorageFood.lua:25-29`.
- **C63:** writers of `factions_disaster` are 3, no other clearing site; adjacent and
  unfiled: the hidden politics card, Radicalization walking ALL colonists, the same
  never-stop for INACTIVE factions in both trees, `RadicalizedFactionsPolarizationDefs`
  never cleared.
- **C64/C66/C75:** every citation resolves; presence sides counted (no second lock of
  `FusionReactor`; 9 `DumpCargo` sites; `RemoveEffect` has one caller). C75 also showed the
  1.0.7 explosion lock was permanent (no `DiscoverTech` named the tech) and 1.1.0 repaired it.
- **C67:** `ServiceWorkplace.OnChangeWorkshift` runs BEFORE the counter reset, so the
  removed visitor kick cannot be the cause; shift-change `InterruptVisit` still fulfils, so
  the late-return population is small.
- **C68:** `Colonist:SetCommand` (`ColonistTransport.lua:381-460`) routes cross-map targets
  by train/`GoToDome`/`Stranded` before `VisitService` runs; food services come from
  `connected_domes`; same-map entry force-places (`Unit.lua:392-404`).
- **C69/C76/C79 share one root the entries never name:** 1.1.0 research is instant at a
  flat 1 tech point (`TechTree.lua:1200-1240`, `_GameConst.lua:22`), `Research:TechCost`
  returns 0, `ResearchQueueChange` is raised 0× in 1.1.0 (8× in 1.0.7). A per-tech cost has
  no surface; boosts are RP refunds. Reinstating C69's branch would fix nothing; C76/C79's
  recipes read a constant.
- **C78:** the predicate matches nothing in either tree's data, so it also cannot strip a
  tech bonus wrongly; the +10 % survives; whether a ≥402200 intermediate build authored 20 %
  is unanswerable from the archives.
- **C80:** refuted by the `Holder:Done → KickUnitsFromHolder → KickFromBuilding →
  SetCommand("Idle")` chain, verified at `Elevator.lua:568`, `Elevator.lua:636-637`,
  `Unit.lua:288-304`, `PropertyObject.lua:1744`.
- **R08311:** 16 non-overriding inheritors enumerated; every creation site is Universal
  except `RocketExpeditionBase:Unload`'s `"SupplyRocket"`, gated behind an object the fixup
  converts; and the fixup plus `GetRocketClass → "UniversalRocket"` already ship in 1.0.7.

### 3.3 Chain-level pattern in the sample
Of 12 re-derived P2s, **every "loss" the entries described turned out, on the trees, to be
either an unearned gain (C64, C67, C75, C78, C79), a sub-percent effect (C58), a lost
flourish (C69), nothing visible (C76), unreachable as written (C68, C80), or a real
player-visible misbehaviour with a cheap organic check (C66, C63).** The entries' citations
were right in 11 of 12 (C58's one path); the ROUTES were the weak part — six of twelve
stopped one hop short of the mechanism that decides severity (the research model ×3, the
transport gate, the holder kick, the depot placement rule). That is the same failure shape
this project recorded for F117 and C54: correct lines, incomplete route.

### 3.4 Not a fix list — the decision, routed
`FIX_POLICY` §4 and the owner decide what becomes a fix. Routed as **checklist item 142**
("which of these, if any, go to a hotfix-3 candidate list"), with a recommendation per
finding there. Plainly: **none of the 24 earns a hotfix-3 slot on today's evidence**; two
are worth a cheap organic look (C66 in any play session with an RC Transport carrying two
resource groups; C82 in the Incident fixture ck140 already owns, one extra reload), one
needs the politics fixture ck137 already owns (C63), and the rest are file-and-watch —
most are gains, not losses, and the owner's 09-08 rule and its 09-09 reversal both bear on
whether an unearned bonus is ever chased (surfaced in 142, not resolved here).

### 3.5 What the chain's findings are worth to a player — the owner's yield question
Twenty-four candidates from a diff of 2,437 files: after this audit, the player-facing
LOSSES on an ordinary route number **three** (C82 if it holds, C66, C63), none observed in
play, each needing a fixture the checklist already lists. The rest are gains, cosmetics,
invisible accounting or unreachable as written. Relative to the chain's cost, the yield is
low, and it says one true thing about 1.1.0's Lua that the owner's thesis did not predict:
the developers' changes in this patch mostly broke *promises* (text, authored costs,
flourishes) rather than *state* — the two state defects (C63, C66) are both new-code seams
where an old contract (`max_duration`, `DumpCargo`'s one-id API) met a new feature. The
FR-1 crash, the one report that is "leaving players completely unplayable", is below Lua
and only the Linux sitting can reach it.

## 4 · Coverage — what this hunt could not see, stated up front

### 4.1 Reach of the reading, by system (hand rows; declarations counted in the 1.1.0 files each system's rows touch, mixed files counted in each system they touch)
| system | changed rows | rows opened at row level (02 fan-out + 03 family) | unchanged declarations in those files, never opened |
|---|---:|---:|---:|
| commonlua | 2,496 | 1,235 | 9,201 |
| removed-added (04-D) | 2,279 | 276 | 0 (whole files) |
| story | 764 | 520 | 1,065 |
| services | 717 | 450 | 896 |
| ui | 416 | 259 | 763 |
| logistics | 395 | 224 | 877 |
| rockets | 394 | 247 | 902 |
| drones | 331 | 210 | 843 |
| saveload | 327 | 89 | 5,386 |
| colonists | 318 | 198 | 425 |
| domes | 214 | 125 | 239 |
| disasters | 212 | 139 | 455 |
| construction | 191 | 119 | 538 |
| landscape | 171 | 108 | 184 |
| depots | 98 | 44 | 200 |
| trains | 87 | 65 | 261 |
| **all hand rows** | **9,410** | **4,308 (46 %)** | **~22,000 in the changed files; 23,516 identical functions tree-wide; 0 of 1,963 identical files opened on their own account** |
The `PASSING` surface sweep reached only those 4,308 opened bodies (plus whatever callers
and siblings an agent opened incidentally, which no ledger counts). It is not a sweep of
the unchanged tree and must not be read as one.

### 4.2 Not reached, collected
- **01:** anonymous `function(` literals (~12,200 lines); `ConstDef` presets absent from
  STORAGE; `FORMAT`/`SAVE-ID` unfalsified; churn classes read at 20 rows (REINDEX) / 22
  (T-ID) / 5+5 (added/removed) / 1 — plus my 10 per class (§1.2).
- **02:** 79 hand `SPAN-SUSPECT` body rows never classified; every `added`/`removed`/
  `generated` row classed by kind only; 473 `CHURN` rows read by one agent; 289 files
  placed by hand into systems (unit A) — a routing judgement, unaudited beyond the rule
  text; `B12.r2` issued and never ingested (not re-issued here — a second read that only
  adds coverage, and the chain's reading of those rows is already merged from round 1);
  batches **B01–B15 were never asked for the `PERF` tell** and 04's file skim did not read
  their rows, so FR-3's per-row tell coverage on those ~2,300 rows is absent.
- **03 family:** every assigned row read (396 + 1,984 + 286 + 283 receipts); the 1,618
  preset rows read by 03b were the only per-row preset read in the chain; 24 pending
  caller records; the DLC bodies behind every seam (by fence).
- **04 (audited as the SKIM the owner ruled it):** 944/944 units each carry one line
  (counted: 121 / 237 / 454 / 9 / 123 in the five reports); the four seed files are
  flagged; the parent verified every FILE verdict in `drill-01.md` (4 FILE, 1 amendment, 8
  REJECT, 1 LEAD — and §3 re-derives them); every `NOROWS` `NONE+yes` file has exactly
  one owner line (123/123, none double-owned); the five loader-route citations in 04-C
  resolve to the quoted `autorun.lua`/`Dlc.lua` lines. ⛔ **Not row coverage, and never
  claimed as such:** `nothing odd` is a file-level statement; the **338 `DROP` SMELL rows**
  (A 62, B 87, C 189, all named in the reports) are the complete flagged-not-drilled
  list; 25,409 preset rows were skimmed per registry, so the 1,707 `REINDEX-SWAP`
  value-vs-value rows routed to 04-E were never read per row.
- **Instrument-level, by construction:** `DLC/` (151 paths); 0 `FPK-DIVERGENT` rows
  (EF-085); 133 `SPAN-SUSPECT` and 100 `MULTI` rows carry unreliable body verdicts; and
  the **1,281 table-level hunks in 368 files with rows** (§1.4) — the blind spot the chain
  learned and had only half-stated.

### 4.3 README's blind-spot list, re-read
Spots 1–7 stand unchanged. **New, learned by this run and now measured:** *a changed
top-level table, class definition or `__parents` list in a hand file that ALSO has function
rows* is listed by neither instrument nor NOROWS (§1.4). 04's skim saw these hunks at file
level; no row reader did. The `DLC_DEEP_CHECK` chain inherits this: a DLC that patches base
behaviour through `__parents` or table fields would show up exactly there.

### 4.4 The three field reports, for the owner
**FR-1 — Linux new-game crash.** What the chain read: 142 FR-1(a) rows, 61 FR-1(c), 15
FR-1(d) and 948 FR-1(c) preset rows were tagged by function and put first in every reading
list; 03 read its 10 FR-1 rows (3 in 03, 6 in 03c, 1 in 03d), 04-C skimmed every render,
config and MapGen file including the 90 rowless ones (`options.lua`, `GlobalStorageTables`,
`RenderFeaturesParams`, `Postprocessing`, `Lightmodel*`, `MapGen-*`, `Config/*`) and drilled
MapGen's new `ApplyPass` (its double `ResumePartialPassEdits` is idempotent — reason-set
semantics, `map.lua:641-652`, verified in the report). What it found: no Lua route to a
process death; the temporal-upscaler lead was refuted by players crashing with AA off; the
strongest Lua-visible LEAD remains the new native-facing map-generation path. What it could
not see: the crash itself (native, below Lua — README blind spots 1, 2, 4); FR-1(b) has 0
rows by measurement and the DLC-off reports make a DLC branch unlikely. What would settle
it: **a `PROTON_LOG=1` log from one affected machine, or the owner's RTX 3070 Linux rig
sitting (`prompts/FR1_LINUX_SITTING.md`, checklist 136)** — nothing a source read can do
now outranks that. Not closed.

**FR-2 — deep scanning reveals nothing.** Read: 107 FR-2 rows + 102 preset rows tagged by
function; 03c read its 4, 03d its 3, 04-B/A skimmed the exploration, probe and deposit
files and 04-E the Tech/TechPreset registries (the doubled registry 01 flagged). Found: in
both trees sector deep-scan status connects to deep-marker reveal (`Exploration.lua`
old `:251-262` / new `:256-267`) and orbital probes separately require `AdaptedProbes`
(`OrbitalProbe.lua:66,94-97` both trees) — the route is internally consistent; no rowreached broke it. Could not see: per-map reveal STATE on a real save (the "intermittent /
reinstall fixed it" shape points at state or ordering, which source cannot observe). Would
settle it: one affected save, or a fresh 1.1 colony taken through a probe scan with the
deep-scan tech (a play leg, not a read). Not closed.

**FR-3 — stutter, unchanged by graphics settings.** Read: 308 FR-3 rows tagged; 03 read
11 of its 21, 03c/03d theirs; 04 skimmed every file and filed the only new periodic-work
candidate (C81, three per-second all-grid scans) beside C60/C62/C72/C73 from the 03
family — all `PERF` tells with profiling falsifiers, none measured. Could not see: the
ORIGINAL cause of a report that predates 1.1.0 lives in code both trees share or in the
engine, which no diff lists; batches B01–B15 were never asked for the tell. Would settle
it: a profiler session on a large colony (checklist 136), which decides C81 and C60 in the
same sitting. Not closed.

## 5 · Consistency (E)
- Ledger vs TSV: INVENTORY 11,742 · PRESETS 37,512 · CALLERS 4,096 · STORAGE 1,155 ·
  FILES 202 · NOROWS 1,537 (1,413 presetdiff + 123 NONE/yes + 1 ws-only) — all equal the
  files' own data-row counts; §1.1's partition (03 1,289 / 04-A 1,199 / 04-B 2,408 / 04-C
  2,871 / 04-D 2,003 / 04-E 1,972; presets 1,618 / 25,409 / 10,485; callers 30 / 449 / 577
  / 1,000 / 409 + 1,631 non-`same`) re-derived by `awk` exactly; §1.7's FR counts
  (142/0/61/15/107/308; presets 948/102) and §1.3's SMELL counts (44/64/90/191) re-derived
  exactly.
- README rows struck vs prompts consumed: 01, 02, 03, 03b, 03c, 03d, 04 deleted in their
  close-out commits; 03_DATA/05/06/07 retired by the consolidation (`6ad619a`, a peer's
  commit that swept the chain's staged rename — recorded in README rule 1). Seven struck
  rows, seven consumed prompts, 99 left.
- **No status word moved by a chain link**: `git log -p c0e8bc8..HEAD -- docs/agent/bugs/`
  shows `status:` lines only in new files, except `C77` `cand→filed` in `75f162d` — the
  owner's attended sound-sweep commit, not a chain link. C74/C77 are the owner's, not the
  chain's.
- `Code/` and `items.lua` untouched over the chain (empty diff). `metadata.lua` gained 4
  lines in `6ad619a`/`9619181` (the AGENTS.md pack-exclusion, a peer/owner change, not a
  chain link). Both archives re-hash identical (§0). STATE's NEXT line, checklist items
  137/138/140/141 and the SESSION_LOG legs describe what the chain did and nothing more.
- Inbox items: every upstream ask is dispositioned in §7; none dropped.

## 6 · Drift ledger — every mistake the links captured (rule 5), plus mine
Upstream, as recorded by the links themselves and re-read here: 01's v0 whole-span hash
(caught by its own fixture); `RENAME?` firing 1,328× unguarded; three `presetdiff` parser
defects found only by real data (78,243→37,512 rows); the `REINDEX` split after reading;
`presetdiff`'s overstated header justification; `FORMAT`/`SAVE-ID` unfalsified; 01's
completeness statement missing the data-table class (found by 02 via DLSS, fixed as
NOROWS v1.2 — and still half-stated, §1.4); `treediff` gaining a second author after 01
closed (measured, falsified, stated); 02's three parent CALLERS rulings corrected by
agents (B10, B16, B24); 02's two-tier dlc tag, redacted taxonomy cells, agents writing
scratch files; B01–B15 briefed without the PERF tell; B12.r2 never ingested; 03's wrong
task slash, DLC-lookup fence breach, ranch prediction corrected by the desk, hook WARN
(resolved by the dispatch session: a leaked `GIT_INDEX_FILE`, not the kit); 03c's count
drift 50/156/78→47/158/81 and a corrected parser; 03d's first desk run missing a shim;
04's R08311 lead killed by its own route read, and its correction of the
`GetEnvironment(City)` concern. **Mine:** the inbox read first (§0); my soundness script
first matched INVENTORY on a column it does not have (`path` vs `file`) and would have
reported four hand files with zero rows — caught because three of them were absent from
NOROWS, which cannot be; my first planted-change script targeted a class name (`Hotel:`)
that does not exist (`HotelBase:`) and a preset field (`food`) the 1.1.0 preset no longer
has (`amount`/`herd_size`) — both corrected before any row was read; my INDENTED-pair
recount first paired one-line orphans by an empty body hash (13 pairs) before hashing
them on their own line as the tool does (11).

## 7 · Inbox — every routed ask and its disposition
| from | ask | done |
|---|---|---|
| 01 | re-run both selftests | ✅ §1.1 |
| 01 | weigh the indented hole hardest; re-falsify it | ✅ §1.3 (planted), §1.5 (pairs, ONE-LINE sample) |
| 01 | check the other headers for an overstated claim | ✅ §1.1 — none found |
| c3 | Pass A.2 with an INDENTED table-field method and an inserted `Run` step | ✅ §1.3 — one row each; the `Run` step surfaces on the enclosing `Create` |
| c3 | sample 10 `ONE-LINE` rows against the raw diff | ✅ §1.5 — hid nothing |
| c3 | re-derive the 11 anchor pairs | ✅ §1.5 — 11, bucket split differs by 2 |
| 04-session | re-derive the 123 NOROWS files | ✅ 123 `NONE+yes` (+1 ws-only) |
| 04-session | did 04 assign every `NONE+yes` file | ✅ 123/123, one owner each |
| 04-session | should `presetdiff` scope become "every file holding `PlaceObj`" | **Recommendation: yes, for the next chain**, as a bucket flag not a filter — §1.4 shows 12 `DefineClass` + 916 table/field hunks outside spans, and the 54 `CommonLua/Data` + `Libs/*/Data` files are `PlaceObj` data no field-level reader saw; it could not change mid-chain (02's tagged PRESETS would be invalidated) |
| 02 | overturn or uphold the seeds ruling | ✅ upheld, §2.1 |
| 02 | re-derive a sample of appended-parameter callees whose new param gates a new branch | ✅ 10 callees (seed 99): every appended parameter either defaults, is passed through, or gates a branch that is OFF when nil (`skip_finalize`, `dont_drop`, `reason ~= nil`, `no_scroll`, `spot`, `map or self:GetMap()`); **none has the `GetLocObj` shape** (a branch existing callers now NEED). One rests on an engine fact: `ParsedParamsToList` calls `Min(#meta_list, max_count)` with `max_count` nil from its 6 unchanged callers — benign only if native `Min` tolerates nil (the desk-harness shim note suggests it does; unverified, editor/scripting code only) |
| 02 | B01–B15 PERF gap — did 04 cover it | ✅ §4.2 — no: 04 skimmed files, not rows |
| 02 | B12.r2 | not re-issued, stated §4.2 |
| 03 | audit SEAM_REPORT/desk/controls; hook WARN verbatim | ✅ read; WARN resolved upstream (`testkit_tree()` env strip), recorded §6 |
| 03b/03c/03d | re-derive C75/C76, C63–C65, C66–C73 samples | ✅ §3 (all P2 among them re-derived; P3s not sampled beyond consistency) |
| 04 | re-derive R08311's rejection, the `GetEnvironment(City)` correction, C78–C81 | ✅ §3 |
| 04 | FR-1/2/3 remain open | ✅ §4.4 |

## 8 · Kickoff — `prompts/DLC_DEEP_CHECK.md`

**Fire it.** Kickoff line for the owner (paste into a fresh session):

> `Author prompts/dlccheck/ from docs/agent/prompts/DLC_DEEP_CHECK.md. Inherit the base-game seam result from docs/agent/reports/vanillahunt/TRIAGE.md → "For dlccheck" (03's section plus 03b/03c/03d's), read docs/agent/reports/vanillahunt/HUNT_AUDIT.md §1.4 and §4.3 first, and size the chain from the DLC's function count as the brief's banner says.`

What this chain learned that changes ITS shape (the brief's §6 asks for exactly this):
1. **The "mostly additive" premise was NOT ruled on here** — 03 declined it by fence
   ("no broad claim about DLC being mostly additive was made") and 04's skim never read
   `DLC/`. It is still the shallow-instrument claim of 2026-09-08; re-derive it first.
2. **Where a DLC patch of base behaviour would hide from these instruments:** §1.4's
   class — `__parents` edits (71 in the base diff alone), table-field and `DefineClass`
   changes in files that also have function rows. `treediff` will not list them and
   `NOROWS` will not either. The DLC chain needs a hunk-level read of every base file the
   DLC's code touches, not a function inventory, for that class — or `treediff` gains a
   `TABLE-HUNK` list (the `a4_gap.py` method: difflib opcodes outside every span).
3. **`presetdiff`'s scope should widen to every file holding `PlaceObj`** (the
   04-session's question, §7): 54 `CommonLua/Data` + `Libs/*/Data` files were preset data
   no field-level reader saw. Do it as a bucket column before link 1 of the DLC chain, not
   mid-chain.
4. **What "yield" looked like here, so the DLC chain sizes honestly:** 24 source-read
   candidates from ~4,300 opened bodies; after this audit's re-derivation of the 12 P2s
   (§3) the ones with a plain player LOSS on an ordinary route are few and every one is
   still unobserved in play. The DLC brief's deep-and-bounded framing is the right one.
5. The rowless-file fix (NOROWS v1.2) and the orphan enumeration (v1.1) both happened
   AFTER their link closed; the DLC chain should run its instrument's completeness
   statement past a fresh reader before link 2 partitions rows on it.
