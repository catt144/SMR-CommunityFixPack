# vanillahunt — the triage ledger

⛔ **Section discipline (chain README rule 15a).** §0 is link 01's and is
CLOSED. §1–§4 are link 02's. Links 03 and 04 each APPEND one named coverage
section. ⛔ Write only inside your own section; never reflow the file.

---

## §0 · The mechanical inventory — counts only (link 01, 2026-09-10)

⛔ **Nothing in this section is a verdict.** No row here was read for meaning.
Every number is re-derivable by re-running the two instruments; every one of
them is a claim about a MEASUREMENT, not about the game.

### 0.1 · The pin, re-checked at link top

| what | read | result |
|---|---|---|
| Steam build | `appmanifest_3215050.acf` `buildid` | **`24995074`** ⇒ matches the chain pin, proceed |
| 1.0.7 tree | `C:\Dev\SMR-SrcArchive\1.0.7.396349\Src` | 4448 files, manifest digest `09d95e3448573dc3…` |
| 1.1.0 tree | `C:\Dev\SMR-SrcArchive\1.1.0.403908\Src` | 4717 files, manifest digest `a4577da25cb3fe85…` |
| working tree | `git status --short` | clean; no peer edits in flight (`smr-bugfixpack-c3` confirmed its lane closed) |

### 0.2 · ⭐ fpk parity on 1.1.0 — unit A, the control that bounds every citation

Recorded as **`EF-085`**. Extracted `Packs\Lua.fpk` and `Packs\Data.fpk` from
the LIVE install into a scratchpad with `tools/flpk_extract.py` and hashed per
file against the ARCHIVED 1.1.0 `Src`.

| pack | entries | matched Src | **byte-identical** | **DIVERGENT** | Src files absent |
|---|---|---|---|---|---|
| `Lua.fpk` (exact-path entries) | 2374 | 2373 | **2373** | **0** | **0** |
| `Lua.fpk` (flattened alias set) | 2106 | — | 2106 vs their twin | **0 stale** | — |
| `Data.fpk` | 2815 | 2191 | **2191** | **0** | **0** |

**Src-side coverage over the whole non-DLC tree: 4564 / 4564 shipped
byte-identical.**

- ⇒ **NO INVENTORY ROW CARRIES `FPK-DIVERGENT`.** There is nothing to flag.
  This is *stronger* than the 1.0.7 proof (2250/2256, 5 divergences), and it was
  measured fresh — the 1.0.7 result was never assumed to transfer.
- The single fpk entry with no Src counterpart is `Lua/Config/_LuaRevision.lua`
  (100 B), reading `LuaRevision = 403908` / `BuildVersion = '1.1.0.403908'` — an
  independent control that the extracted pack IS the archived build.
- `Data.fpk`'s 624 extra entries are assets (482 `ParticleSystemPreset/`, 142
  `MapData/`), no Src counterpart by design. DLC ships in its own
  `DLC\norman.fpk` / `DLC\thomas.fpk`, outside both packs.
- ⛔ **This proves the BYTES MATCH. It does not prove the game EXECUTES them**
  (`EF-078` stands) and says nothing about `Mars.exe` (blind spot 2).
- ⚠️ Found by the run and not predicted: `Lua.fpk` stores most files TWICE, once
  at its Src path and once flattened (`Train.lua` beside `Lua/Units/Train.lua`).
  A first pass matching by path SUFFIX read that as "2080 files only in the fpk"
  and was discarded for the exact-path match.

### 0.3 · ⭐ Manifest re-derivation — the required control (README §0)

Re-derived from the two trees, **not inherited**:

| | mine (DLC excluded) | + DLC | README §0 | |
|---|---|---|---|---|
| changed | 2437 | +7 | **2444** | ✅ |
| identical | 1963 | +5 | **1968** | ✅ |
| added | 166 | +139 | **305** | ✅ |
| removed | 36 | +0 | **36** | ✅ |

**MATCHES on all four.** The 139 DLC adds are 138 `DLC/norman` + 1
`DLC/thomas` (README §0 says "138 are DLC/norman" — exact; the 139th is the
`thomas` file). 1.0.7's `DLC/` subtree is 12 files, 5 of them byte-identical to
their 1.1.0 counterparts, which reconciles the +7/+5 split exactly.

### 0.4 · `INVENTORY.tsv` — rows per kind × bucket

| kind | generated | hand | total |
|---|---|---|---|
| `added` | 142 | 4067 | 4209 |
| `removed` | 280 | 1336 | 1616 |
| `body` | 295 | 3421 | 3716 |
| `body+sig` | 0 | 276 | 276 |
| `sig` | 0 | 15 | 15 |
| **total** | **717** | **9115** | **9832** |

Functions counted but NOT listed (identical on both sides): **22,139**.
Declarations seen: 1.0.7 **27,762**, 1.1.0 **30,355**. `dlc` bucket: 151 paths
excluded entirely.

### 0.5 · Flag counts

| flag | rows | what it means |
|---|---|---|
| `NEWFILE` | 1709 | an `added` row inside one of the 166 added files |
| `GONEFILE` | 836 | a `removed` row inside one of the 36 removed files |
| `RENAME?` | 734 | body-similarity hint, partner named (guarded — see 0.6) |
| `SPAN-SUSPECT` | 133 | the one-line-function trap — **the inventory's stated imprecision** |
| `MULTI` | 100 | duplicate declaration, ordinal-keyed (`name#2`) |
| `DECL-ONLY` | 6 | only the declaration line's own text moved |
| `FPK-DIVERGENT` | **0** | nothing diverges — see 0.2 |

⇒ **added rows NOT in a new file: 2500. removed rows NOT in a gone file: 780.**
Those two are the interesting halves; the whole-file ones belong to 04's agent D
and the class-(f) agents.

### 0.6 · ⚠️ The one-line-function trap — MEASURED, not assumed

Confirmed at SOURCE and then in the run: `find_bodies` scans forward from a
declaration for a bare `end` at the same indent WITHOUT checking whether the
declaration line already closed the function, so `function f() return 1 end`
over-spans into whatever follows.

- **441 declarations** across the two trees are self-closing and over-span.
- **133 ROWS** carry `SPAN-SUSPECT`; the full list by name is in 01's outbox to
  02 and 99. They are overwhelmingly one-line getters (`Community:GetAverage*`,
  `SupplyGridFragment:GetCurrent*`, `LightmodelPreset:Get*`,
  `object.GetLocalPoint*`) and a block of `OnMsg.*` handlers in `CommonLua/Ged.lua`.
- ⛔ **A `body` verdict on a `SPAN-SUSPECT` row is unreliable** — the "body" may
  have changed only because the NEXT function did. 02 must not treat these as
  ordinary `body` rows.
- **567 spans reach EOF**, a related over-span symptom, counted separately.
- ⛔ `luafn.py` was **NOT** changed. A delimiter change re-hashes every `SRC:`
  pin in `Code/` — a hotfix-3 decision for the owner. **Routed as a checklist
  item, TAKEABLE WHEN the owner rules on re-pinning.**

`RENAME?` is **guarded**: a partner needs ≥4 distinct non-blank body lines and
≤3 candidates. Without the guard it fired 1,328 times inside one
`LuaExportedDocs` file on bodies like `end` and `return true`. Rejected as too
trivial to be evidence: **441** added rows. Rejected as ambiguous: 0.

### 0.7 · `CALLERS.tsv` — ⭐ class (b′), the F117 shape

290 callees (every `sig` / `body+sig` row in a `hand` file), both trees.

| status | rows |
|---|---|
| **`same`** (call text unchanged against a CHANGED signature) | **2465** |
| `changed` | 682 |
| `new` | 618 |
| `gone` | 331 |

`same` rows span **660 call files**. Top by count: `Lua/Buildings/StorageDepot.lua`
39 · `CommonLua/Ged/GedPropEditors.lua` 38 · `Lua/Mysteries/Fireflies.lua` 34 ·
`Lua/Buildings/Building.lua` 31 · `Lua/Construction/Construction.lua` 30 ·
`CommonLua/Ged.lua` 29 · `Lua/Mysteries/MirrorSphere.lua` 28 ·
`CommonLua/Ged/GedPanel.lua` 26 · `Lua/UniversalRocket.lua` 25 ·
`Lua/Mysteries/Crystals.lua` 25 · `Lua/Buildings/RocketBase.lua` 22 ·
`Lua/Meteors.lua` 22 · `Lua/Units/Colonist.lua` 21 · `Lua/Units/Unit.lua` 21.
The full per-file tally is the TSV's own banner line.

⭐ **The tightest subset, and 02 should start here: 9 `same` call lines whose
callee is a PURE `sig` row** — the parameter list moved and the body is
BYTE-IDENTICAL, so every argument inside is silently one slot off:
`ParadoxModData.GetAuthor` (3) · `GridProc.GetSeedSaveDest` (2) ·
`LockablePreset.OnLockStateChanged` (2) · `collision.Collide` (1) ·
`table.farthest` (1).

⛔ Text-level only. It does not bound reach (blind spot 7): dynamic dispatch,
`Msg` handlers and preset `func` fields are outside it, it cannot tell two
classes' same-named methods apart, and it counts mentions in strings and
comments. The k-th-call-site pairing rule is stated in the TSV banner.

### 0.8 · `STORAGE.tsv` — class (c)

1155 rows: **same 1007 · added 102 · removed 36 · moved-file 9 · kind-changed 1**.

⭐ The one `kind-changed` is **`Landscapes` `GameVar` → `MapVar`**
(`Lua/Landscape/Landscaping.lua:21` both sides) — the exact class-(c) scar the
taxonomy names, found mechanically. The 9 `moved-file` rows:
`MaxModDataSize` (`Classes/Mod.lua` → `Modding/Mod.lua`) ·
`RadicalizedFactionsPolarizationDefs`, `g_FactionDisaster_Dissolution_FactionDissolved`
(`ClassDef-Factions.generated.lua` → `Factions/FactionDef.lua`) ·
`g_BuildMenuEntriesDisabledByLawEffects` (→ `Factions/LawDef.lua`) ·
`RocketMaxDrones` (two files → one) · `g_CollideLuaObjects` ·
`fastGameSpeed` / `mediumGameSpeed` / `ultraGameSpeed`
(`Lua/_GameConst.lua` → `Lua/Config/config.lua`).

⚠️ Stated holes: `GlobalVar("…")` has **0** declarations in BOTH trees (the form
exists in `CommonLua/Core/lib.lua`; the game declares through `GameVar`/`MapVar`
— zero here is a measurement, not an omission). 1 dynamic declaration per tree
(`GameVar(modified_name, …)`) cannot be named. **`ConstDef` PRESET definitions
are not covered at all** — that is where most consts are defined, and it is
`presetdiff`'s territory; `const.X =` here is the Lua-side assignment only. The
36 removed storage names include `ColonistMaxDomeWalkDist` and
`ColonistMinDistToIgnorePassage`, the walk consts of the `const.` → `g_Consts`
scar — ⛔ their new home is NOT established by this TSV.

### 0.9 · `FILES.tsv` — 166 added + 36 removed (DLC excluded)

⛔ **The method rule, mechanised.** For every removed file the PRESENCE SIDE is
enumerated: how many of its declared names are still declared somewhere in
1.1.0. **21 of the 36 removed files have a nonzero count** ⇒ "moved", not
"gone", for those.

⭐ The largest instance, and `RENAME?` found it independently: the modding
backend was **MOVED, not deleted** — `CommonLua/Classes/Mod.lua` →
`CommonLua/Modding/Mod.lua` (115 body-identical partner pairs),
`ModItem.lua` (94), plus `ModsBackend.lua`, `ModItemMap.lua`, `ModItemFolder.lua`,
`ModItemSetpiece.lua`. README §0 lists `CommonLua/Classes/Mod*.lua` among the 36
removed files as "the old modding backend"; ⛔ it was relocated.

⚠️ A surviving name can be an unrelated homonym — `CommonLua/ArtTest.lua`'s 2
survivors are `ArtTest.Start` and `OnMsg.ChangeMapDone`, and `OnMsg.*` names
recur everywhere. And a ZERO count still only proves the NAME is gone, never the
FEATURE.

### 0.10 · `PRESETS.tsv` — the field-level preset diff

Presets parsed: 1.0.7 **14,409** · 1.1.0 **14,986**. Rows: **37,512**.

| churn class | rows | sampled & READ | misses found |
|---|---|---|---|
| `none` — ⭐ **the readable pile** | **22,738** | 8 | — (makes no claim) |
| `REINDEX` | 10,462 | 20 | **0** |
| `REINDEX-SWAP` | 1,924 | (split out of REINDEX by the sampling — see below) | — |
| `added-preset` | 1,471 | 5 | — |
| `removed-preset` | 894 | 5 | — |
| `T-ID` | 22 | **22 (all)** | **0** |
| `COMMENT` | 1 | 1 (all) | 0 |
| `FORMAT` | **0** | — | ⚠️ rule never fired on real data |
| `SAVE-ID` | **0** | — | ⚠️ rule never fired on real data |
| `REORDER` | **0 by construction** | — | 0 presets in that state |

- **`T-ID`: all 22 rows read.** Every one is an id change with byte-identical
  text (`T(519, "Storage")` → `T(553023078295, "Storage")`). **0 misses.**
- **`REINDEX`: 20 rows read, and the read CHANGED THE RULE.** The `<absent>`
  half is provable — `XDef:ipTrack`'s `T(529, "Today…")` leaves `children[6]`
  and arrives at `children[5]`, two rows and one value. The value-vs-value half
  is NOT: both sides hold real values that each occur elsewhere, which is
  equally consistent with a genuine swap at that position. It was split out as
  **`REINDEX-SWAP` (1,924 rows)** and ⛔ **must be READ, not skipped**, wherever
  a list's order is semantic (`Parameters`, `likes`, `Effects`).
- ⚠️ `FORMAT` and `SAVE-ID` fire on fixtures and **never on the real trees**. An
  unfired rule is an UNFALSIFIED rule; they classify nothing here.

**Readable (`none`) pile per registry** — 90 registries, top 20:
StoryBit 6683 · XDef 5071 · TechPreset 2669 · FactionDef 1599 · LawDef 1536 ·
ActionFXParticles 505 · AssemblyChoiceDef 424 · SA_Exec 421 · PresetDef 375 ·
SponsorGoals 296 · TechFieldPreset 275 · SA_Block 243 · LightmodelPreset 242 ·
CropPreset 153 · OnScreenHint 149 · NotificationPreset 138 · PolicyDef 125 ·
ParticleSystemPreset 121 · Label 113 · CommanderProfilePreset 108.

**The generated-Lua twins** (so 04 can confirm they carry nothing extra), files
parsed: 1.1.0 `Data` 2191 · `Lua/BuildingTemplate` 292 · `Lua/XDef` 426 ·
`Lua/ClassDefs` 7 | 1.0.7 `Data` 2143 · `Lua/BuildingTemplate` 288 ·
`Lua/XDef` 400 · `Lua/ClassDefs` 9.

⭐ **Routed, not read: the tech registry exists TWICE in 1.1.0.** 1.0.7 has 264
`TechPreset` presets; 1.1.0 has **274 `TechPreset` AND 441 `Tech`**, with 258 of
1.0.7's TechPreset ids appearing under BOTH classes in the new tree. Mechanical
count only. `CLASS-RENAMED?` additionally flags 6 rows
(`StoryBitCategory`→`Trigger` ×4, `XPresetMapLabel`→`TrophyGroup` ×2).

### 0.11 · ⛔ What this inventory does NOT cover — the completeness contract

Stated as numbers so a reader can act on them, per README rule 7 (no instrument
here is a clearance):

1. **8,473 INDENTED declarations** (1.1.0 side): 4,883 in `hand` files, 3,590 in
   `generated`. `treediff` emits **indent-0 declarations only**. Sampling showed
   the indented set is overwhelmingly preset data (`Data/`, `Lua/XDef/`,
   `Lua/Scenario/*.generated.lua`, `CommonLua/Ged/`) which `presetdiff` reads at
   field level — but **the ~4,883 in hand files are covered by NEITHER
   instrument and are this inventory's largest known hole.**
2. **Every anonymous `function(` literal** (~12,200 lines) — callbacks passed as
   arguments.
3. Everything in the chain README's seven blind spots, unchanged: non-`Src`
   content, the engine, runtime-only behaviour, `DLC/`, dynamic dispatch.
4. `ConstDef` preset definitions are absent from `STORAGE.tsv` (0.8).
5. A `body` row on a `SPAN-SUSPECT` function (0.6).

### 0.12 · Instruments and their falsifiers

| tool | rows it owns | `--selftest` | broken on purpose? |
|---|---|---|---|
| `tools/treediff.py` | INVENTORY, STORAGE, FILES, CALLERS | **16 PASS / 0 FAIL**, exit 0 | ✅ yes — see 01's outbox to 99 |
| `tools/presetdiff.py` | PRESETS | **16 PASS / 0 FAIL**, exit 0 | ✅ yes — see 01's outbox to 99 |

Both import `luafn.find_bodies` (the delimiter) rather than re-implementing it;
`treediff` also imports `sigcheck.params` (the parameter reader). Both selftests
exit **1** on failure — verified by inverting an assertion and watching the
exit code, so the green gate is a real gate. ⛔ Neither is wired into
`doccheck.py` (01's fence); 99 re-runs them.

⭐ **The seeded-positive control (README §4), scored BY THE TOOL:**

| seed | expected | `treediff` says | |
|---|---|---|---|
| F114 `Train.lua Train:UnloadAll` | body-changed | `body` [1.0.7 :783 → 1.1.0 :779] | ✅ |
| F115 `Landscaping.lua LandscapeForEachUnit` | sig `(mark,callback,...)`→`(map,mark,callback,...)` | `body+sig`, exactly that parameter move [455 → 509] | ✅ |
| F116 `TrackElement.lua TrackGridElement:DemolishAndSplitTrack` | body-changed | `body` [448 → 467] | ✅ |
| F117 `_GameUtils.lua ChooseDome` | sig-changed | `body+sig`, `traits`→`colonist` [426 → 486] | ✅ |

**4 / 4.** ⛔ This scores the INSTRUMENT, not any agent — 02 still owes the
agent-pool score.

### 0.13 · ⭐ v1.1 re-emission (2026-09-10, the authoring session `smr-bugfixpack-c3`, AFTER 01 closed) — hole 0.11.1 MEASURED, then REDUCED (not closed: the orphans are now rows; in-span declarations are covered only THROUGH their outer function's hash, and anonymous `function(` literals stay outside)

The owner asked whether the "4,883 indented declarations covered by neither
instrument" could be repaired rather than only passed on. Measured first, on
the 1.1.0 side of the changed + added `hand` files:

| indented declarations | count | status |
|---|---|---|
| total (`INDENTED` regex, as 0.11.1 counted) | 4,142 | — |
| INSIDE an enumerated indent-0 span | 2,033 | were ALWAYS covered — the outer body's hash includes them; 0.11.1 over-stated the hole by this much. ⚠️ Covered THROUGH the outer row only: a `body` verdict on the outer function does not say which nested function moved — the reader finds that in the diff of the outer span |
| OUTSIDE every indent-0 span | 2,109 | the real hole: table-field methods in `DefineClass{}`/metatables, `Run = function(seq_state)` steps in `Lua/Scenario/*.generated.lua` (player-facing mystery code), file-level nested locals |
| of those, nested inside ANOTHER orphan | ~1,059 | covered once the enclosing orphan is enumerated |
| ⇒ orphans enumerated by v1.1, `hand`, 1.1.0 side | **1,050** | plus 1,885 in `generated` (613 one-line); 1,377 identical across the trees |

`tools/treediff.py` **v1.1** enumerates the orphans (`_orphans`), keys them
`name@<anchor>` (anchor = the nearest preceding indent-0 line, hashed — a
locality, because `Run` repeats dozens of times per scenario file), matches
them by HASH inside their group before pairing leftovers in file order
(`_diff_orphans` — an inserted sibling therefore cannot cascade into a column
of false `body` rows), and flags every such row **`INDENTED`**. ⚠️ **One
deliberate deviation, stated:** a self-closing orphan (`X = function(self)
return … end,`) hashes ITS OWN LINE ONLY, flag **`ONE-LINE`** — `find_bodies`
would run it to the next same-indent `end`, which inside a table constructor
is the next field's `end,`, so every neighbour's edit would re-hash it. The
indent-0 pass keeps the delimiter's over-span untouched (checklist **135** is
the owner's); this pass never had a `SRC:` pin to protect, and an orphan row's
`hash` is NOT comparable to a pin.

**Re-emitted, same command, same digests.** `INVENTORY.tsv` 9,832 → **11,742**
rows (+1,910, all `INDENTED`). `STORAGE.tsv`, `FILES.tsv`, `CALLERS.tsv`:
banner lines only, row counts unchanged (4,096 callers — no orphan produced a
`hand` signature change, so class (b′) gained nothing here). The 0.4 table and
0.5 counts above are 01's v1 numbers and stand as its record; the v1.1 delta:

| INDENTED rows | added | removed | body | body+sig | sig | total |
|---|---|---|---|---|---|---|
| `hand` | 177 | 52 | 66 | 0 | 0 | **295** |
| `generated` | 965 | 342 | 208 | 97 | 3 | **1,615** — overlaps `PRESETS.tsv` at field level; 04's registry agents own both views |

`hand` INDENTED rows by file, top: `Lua/GameOverlays.lua` 15 ·
`CommonLua/PresetTemplate.lua` 14 · `CommonLua/VolumetricLighting.lua` 14 ·
`Lua/TechTree.lua` 12 · `CommonLua/Ged/GedPropEditors.lua` 10 ·
`Lua/TutorialsNew.lua` 9 · `ModItem.lua` 8+8 (old and new modding paths) ·
`Lua/_StoryBits.lua` 7. ⭐ The scenario `Run` steps came out overwhelmingly
IDENTICAL across the trees (the files changed elsewhere), which is itself a
result the v1 inventory could not state.

**Falsifier extended** (`--selftest`, fixture `Lua/T.lua`, 6 new assertions,
22 PASS / 0 FAIL): a changed one-line field → `body` + `INDENTED` + `ONE-LINE`;
a new field → `added`; ⛔ the unchanged sibling below the insertion is NOT a
row; a declaration nested inside an orphan is NOT a row; a change inside a
nested local surfaces as the OUTER function's row and the local is not its own
row; an inserted `Run` step among same-named steps → exactly ONE `added` row.
**Broken on purpose:** the sibling was given a third parameter in memory and
the "NOT a row" assertion went RED naming it as `sig .self,b → .self,b,c`;
restored, GREEN. Seeds still 4/4.

**A known labelling limit, MEASURED:** the `@anchor` key is a locality
heuristic — when the nearest indent-0 line above an orphan changed between the
trees, the orphan lands in a new group and appears as `removed` + `added`
rather than `body`. Counting `INDENTED` added/removed pairs that share a file
and an `ihash`: **11, all in `generated`, 0 in `hand`.** A labelling error of
that size, not a coverage one.

**What is STILL not covered after v1.1:** every anonymous `function(` literal
passed as an argument (0.11.2, ~12,200 lines); everything in 0.11.3–5. ⛔ And
the drift this section records for 99: the instrument gained a second author
after its link closed — with a measurement, a falsifier and a stated
deviation, but a second author nonetheless.

---

## §1 · Counts — link 02 (triage), 2026-09-10, `smr-bugfixpack-b6`

⛔ **Nothing in §1–§4 is a finding.** A class is a sort key, `WORTH-READING` is a routing flag, a `SMELL` is a PASSING *candidate* for the owning link to derive, and every `CHURN` row is an agent's claim that NO ONE ELSE READ. Every number below is re-derivable from the three `*.tagged.tsv` files with the `awk` lines given; none was hand-typed.

### 1.1 · The partition — every row has exactly one link (disjoint by construction)

| link | INVENTORY rows | of which fan-out classified | PRESETS rows (read) | CALLERS `same` rows |
|---|---|---|---|---|
| 03 (seam) | 1289 | 320 | 1618 | 30 |
| 04 agent A — turf | 1199 | 696 | 0 | 449 |
| 04 agent B — colony | 2408 | 1230 | 0 | 577 |
| 04 agent C — engine | 2871 | 1453 | 0 | 1000 |
| 04 agent D — storage + removed/added | 2003 | 0 | 0 | 0 |
| 04 agents E — presets, one per registry | 1972 | 0 | 25409 | 409 |
| NOT-READ (preset churn: `REINDEX`, `T-ID`, `COMMENT`) | — | — | 10485 | — |
| **total** | **11742** | **3699** | **37512** | **2465** |

`UNASSIGNED` rows: INVENTORY **0**, CALLERS **0** — every `other` file was placed by hand (1.4). Filter: `awk -F'\t' '!/^#/ && $<link column>=="04-A"'` on the tagged file (INVENTORY `link` is column 12, PRESETS `link` column 11, CALLERS `caller_link` column 13).

### 1.2 · The `dlc-adjacent` set (unit B) — 03's whole fence

| | tagged `dlc-adjacent` (→ 03) | brief's list matched LITERALLY (not applied) |
|---|---|---|
| INVENTORY rows | **1289** | 2918 |
| of which fan-out pool | 320 | 884 |
| PRESETS rows (read classes) | **1618** | 8209 |
| CALLERS `same` rows (callee tagged) | 30 | — |

⚖️ **DEVIATION, stated for 99 — the tag is two-tier, not the brief's literal list.** T1 (literal substring): `Food Meal Crop Farm Fungal Bakery Replicator Restaurant Insect Animal Hunger Starv Consumption FoodService norman thomas IsDlcAvailable AssemblyOfPlanets LawOffice ServiceBuilding` + the **51** class/global names declared in `DLC/norman/Code` + `DLC/thomas/Code` (word-bounded; the one read of `DLC/`, a declaration-line grep, 109 names of which 51 are un-dotted). T2 (`Tech` `Resource` `Law` `Policy` `Cargo`, the five generic words): matched only in their qualified sense (registry and walk forms — `TechPreset`, `Presets.Tech*`, `AllResourcesList`, `Resources[`, `ActiveLaws`, `Legislat*`, `\bPolicy\b`, `\bCargo\b` …; exact regexes in the INVENTORY.tagged banner and `tri_tag_rx.py`), and on presets never on the CLASS NAME. **Why:** a tagged row LEAVES 04 and 03 is one session with a ~400-row stop line; literal matching tags 2918 Lua rows and 8209 readable preset rows (all of `TechPreset` and `LawDef` by class name), so over-tagging makes rows UNREAD, while an under-tagged seam row is still read by 04 and noted to 03 (03/04 fence clauses). ⛔ Nothing is hidden: every row carries `dlc_literal` (all 25 terms, applied or not). ⛔ A name match is not a dependency — the tag says "03 looks", never "03 files".

### 1.3 · Fan-out classification — class × link (hand `body` / `body+sig` / `sig` rows, SPAN-SUSPECT excluded)

| class | 03 | 04-A | 04-B | 04-C | total |
|---|---|---|---|---|---|
| (b′) | 1 | 0 | 9 | 1 | 11 |
| (b) | 21 | 50 | 89 | 113 | 273 |
| (a) | 202 | 493 | 767 | 1059 | 2521 |
| (c) | 48 | 58 | 157 | 91 | 354 |
| (d) | 10 | 9 | 45 | 72 | 136 |
| (i) | 11 | 27 | 50 | 30 | 118 |
| (g) | 9 | 14 | 15 | 23 | 61 |
| (f) | 13 | 40 | 53 | 59 | 165 |
| (e) | 5 | 5 | 45 | 4 | 59 |
| unsure | 0 | 0 | 0 | 1 | 1 |
| `WORTH-READING` | 301 | 596 | 1074 | 1255 | 3226 |
| `CHURN` (UNREAD by anyone else) | 19 | 100 | 156 | 198 | 473 |
| `GUARD+` (guard added) | 51 | 111 | 166 | 182 | 510 |
| `GUARD-` (guard removed) | 8 | 13 | 10 | 30 | 61 |
| `SMELL` | 44 | 64 | 90 | 191 | 389 |
| seam flagged | 166 | 230 | 499 | 385 | 1280 |
| no verdict | 0 | 0 | 0 | 0 | 0 |

**Per system** (fan-out rows · WORTH-READING · SMELL; system is the path/class partition, link column shows where `dlc-adjacent` rows went):

| system | rows | WORTH-READING | SMELL | of which → 03 |
|---|---|---|---|---|
| commonlua | 1232 | 1065 | 158 | 15 |
| story | 440 | 396 | 51 | 89 |
| services | 353 | 308 | 20 | 88 |
| ui | 246 | 213 | 39 | 10 |
| rockets | 229 | 199 | 18 | 28 |
| drones | 210 | 173 | 12 | 4 |
| logistics | 193 | 168 | 20 | 27 |
| colonists | 181 | 164 | 16 | 21 |
| disasters | 128 | 112 | 5 | 10 |
| construction | 119 | 109 | 8 | 3 |
| domes | 112 | 100 | 5 | 7 |
| landscape | 108 | 100 | 11 | 1 |
| trains | 63 | 49 | 16 | 2 |
| saveload | 44 | 38 | 8 | 14 |
| depots | 41 | 32 | 2 | 1 |

**Rows NOT in the fan-out, classed by KIND (`*`, mechanical, unread):** added generated 1107 · added hand 4244 · body generated 503 · body hand 74 · body+sig generated 97 · body+sig hand 3 · removed generated 622 · removed hand 1388 · sig generated 3 · sig hand 2.

### 1.4 · `other` — placed BY FILE, by hand, with the reason (unit A)

The path/class rules (brief §2.A) left **243 files** holding rows unmatched (every row now placed: `UNASSIGNED` = 0); unit D added **14** caller-only files (unchanged files seen only as call sites) and the NOROWS bucketing (1.8) **32** NOROWS-only files — **289 files placed by hand in total**. Each group's reason is the argument. `Building.lua` and its mixins go to colony because 04 §3.B names `Building.lua` by class prefix as B's.

- **services → 04-B** — building core: 04 brief §3.B names Building.lua by class prefix as colony; its base/mixin classes follow it: `Buildings/Building.lua`, `Buildings/BaseBuilding.lua`, `Buildings/BuildingComponents.lua`, `Buildings/UpgradableBuilding.lua`, `Demolishable.lua`, `CityObject.lua`, `PinnableObject.lua`, `Renamable.lua`, `RequiresMaintenance.lua`, `HasConsumption.lua`, `Buildings/Workforce.lua`, `Buildings/ShiftsBuilding.lua`, `Buildings/Factory.lua`, `Buildings/OutsideBuildingWithShifts.lua`, `Buildings/UIRangeBuilding.lua`, `Buildings/AutoMode.lua`, `Buildings/SpawnsOnCityInit.lua`, `Buildings/BuildingSigns.lua`, `Buildings/Banner.lua`, `Buildings/ColdSensitive.lua`, `UpgradeUnlocks.lua`, `Modifiers.lua`, `LabelContainer.lua`
- **services → 04-B** — in-dome service/habitat buildings (Service*/Residence* family by function, not by name): `Buildings/Community.lua`, `Buildings/MicroGHabitat.lua`, `Buildings/Arcology.lua`, `Buildings/OpenCity.lua`, `Buildings/Hotel.lua`, `Buildings/MedicalCenter.lua`, `Buildings/School.lua`, `Buildings/MartianUniversity.lua`, `Buildings/TrainingBuilding.lua`, `Buildings/Sanatorium.lua`, `Buildings/SecurityStation.lua`, `Buildings/NetworkNode.lua`, `Buildings/MegaMall.lua`, `Buildings/OpenAirGym.lua`, `Buildings/OpenAirBuilding.lua`, `Buildings/SpireBase.lua`, `Buildings/SchoolSpire.lua`, `Buildings/BioroboticsWorkshop.lua`, `Buildings/ArtWorkshop.lua`, `Buildings/TVStudioWorkshop.lua`, `Buildings/GameDeveloper.lua`, `Buildings/CloningVats.lua`, `Buildings/NaturalHabitat.lua`, `Buildings/ResearchLab.lua`, `Buildings/CorporateOffice.lua`, `Buildings/Farm.lua`, `Buildings/FungalFarm.lua`, `Crop.lua`, `Units/Animals.lua`, `Buildings/Plant.lua`, `Buildings/ThreeHarvestTypesBuilding.lua`, `Units/RCSafari.lua`, `SafariRouteInteractionHandler.lua`, `SafariRouteInsertWaypointHandler.lua`, `SafariRouteMoveWaypointHandler.lua`, `SafariSight.lua`, `HolidayRating.lua`, `Interests.lua`, `StatusEffects.lua`
- **domes → 04-B** — dome-to-dome passages (colonist walking between domes): `Passage.lua`, `Buildings/UndergroundPassage.lua`, `Buildings/SurfacePassage.lua`
- **colonists → 04-B** — colony-wide population/meta state read by colonists and domes: `Colony.lua`, `City.lua`, `ColonyViability.lua`, `ApplicantsPool.lua`, `MarsGameEffects.lua`, `Names.lua`, `_GameUtils.lua`
- **story → 04-B** — research, exploration and progression (scripted colony progression; no turf/engine owner): `Research.lua`, `Tech.lua`, `SpecialProjects.lua`, `Exploration.lua`, `Discoveries.lua`, `Buildings/Anomaly.lua`, `Buildings/PlanetaryAnomaly.lua`, `PlanetaryView.lua`, `Asteroids.lua`, `OrbitalProbe.lua`, `Buildings/SensorTower.lua`, `Buildings/ReconCenter.lua`, `RevealDarkness.lua`, `Units/ExplorerRover.lua`, `Buildings/AsteroidCatcher.lua`, `Buildings/OmegaTelescope.lua`, `Buildings/LowGLab.lua`, `Buildings/BottomlessPit.lua`, `Buildings/BottomlessPitResearchCenter.lua`
- **story → 04-B** — factions, laws, elections, rivals, negotiations (the politics layer): `Factions/Legislature.lua`, `Factions/Laws.lua`, `Factions/Factions.lua`, `Factions/Elections.lua`, `Factions/Independence.lua`, `Factions/FactionsBuildings.lua`, `RivalColonies.lua`, `Negotiations.lua`, `CovertOps.lua`, `Buildings/MartianAssembly.lua`, `Buildings/MarsReservation.lua`, `Buildings/MonumentOfMarsLiberty.lua`
- **story → 04-B** — story bits, scripts, tutorials, special artefacts: `_StoryBits.lua`, `_StoryBitsRemaster.lua`, `MarsStoryBits.lua`, `ClassDef-StoryBits.lua`, `ScriptBlocks.lua`, `Tutorial.lua`, `Buildings/AncientArtifact.lua`, `Buildings/AncientArtifactInterface.lua`, `Buildings/CrystalStatue.lua`, `Units/AttackRover.lua`, `Radio.lua`
- **story → 04-B** — mission setup, sponsors, rules, goals, scoring: `PreGameMission.lua`, `MissionProfileDlg.lua`, `MissionLogo.lua`, `GameRules.lua`, `Challenges.lua`, `Achievements.lua`, `Milestones.lua`, `Funding.lua`, `ResupplyItems.lua`
- **disasters → 04-B** — disasters, terraforming hazards and meteor defence: `TerraformingDisasters.lua`, `Marsquake.lua`, `Bombardment.lua`, `ToxicPool.lua`, `Buildings/DefenceTower.lua`, `Buildings/MDSLaser.lua`, `MapSettings.lua`
- **disasters → 04-B** — terraforming parameters and their buildings/vegetation (colony-wide climate; hazards live beside them): `Terraforming.lua`, `Buildings/TerraformingBuilding.lua`, `Heat.lua`, `Buildings/ArtificialSun.lua`, `Vegetation.lua`, `VegetationFocus.lua`, `VegetationObstructor.lua`, `Soil.lua`, `TerraformingParamsBar.lua`
- **rockets → 04-B** — space elevator / pods / map-to-map transport (Earth and orbit trade): `Buildings/SpaceElevator.lua`, `UniversalPod.lua`
- **saveload → 04-B** — savegame plumbing by content (rule matched only _fixup/SavegameFixup/Persist names): `Savegame.lua`
- **drones → 04-A** — rovers, shuttles and flying units (unit movement and command, the drone/shuttle family): `Units/Unit.lua`, `Units/RCRover.lua`, `Buildings/BaseRover.lua`, `Buildings/RoverBuilding.lua`, `Units/FlyingDrone.lua`, `Units/JumperShuttle.lua`, `Flight.lua`, `Units/RCDriller.lua`, `Units/RCSolar.lua`, `Units/RCHarvester.lua`, `UnitControl.lua`, `Buildings/RechargeStation.lua`, `Buildings/Tunnel.lua`, `Pathfinding.lua`, `_TaskRequest.lua`, `Buildings/BuildingWayPoints.lua`
- **logistics → 04-A** — resource transport rovers and route managers: `Units/RCTransport.lua`, `LRManager.lua`, `LRTransport.lua`
- **construction → 04-A** — construction rovers, the buildable grid and placement: `Units/RCConstructor.lua`, `Units/RCConstructorBase.lua`, `BuildableGrid.lua`, `GridObject.lua`, `hex.lua`, `UnderconstructionSign.lua`, `MultiSelection.lua`
- **landscape → 04-A** — terrain shaping, waste rock and rubble: `Units/RCTerraformer.lua`, `WasteRock.lua`, `Buildings/CaveInRubble.lua`, `Buildings/RubbleBase.lua`, `Buildings/TunnelBlockerRubble.lua`, `Elevation.lua`
- **logistics → 04-A** — deposits and extractors (where resources enter the network): `Buildings/Deposit.lua`, `Buildings/SubsurfaceDeposit.lua`, `Buildings/TerrainDeposit.lua`, `Buildings/EffectDeposit.lua`, `Buildings/BaseExtractor.lua`, `Buildings/RegolithExtractor.lua`, `Buildings/WaterExtractor.lua`, `Buildings/MicroGExtractor.lua`, `Buildings/Mine.lua`, `Buildings/MoholeMine.lua`, `Buildings/TheExcavator.lua`, `DepositRevealer.lua`, `Buildings/DepositMarker.lua`, `Buildings/RegolithMineVisualCP3.lua`
- **logistics → 04-A** — power and life-support grids and their producers/consumers/storage (the Supply* grid family): `ElectricityGrid.lua`, `LifeSupportGrid.lua`, `ElectricityStorage.lua`, `ElectricityConsumer.lua`, `ElectricityProducer.lua`, `LifeSupportConsumer.lua`, `LifeSupportProducer.lua`, `LifeSupportStorage.lua`, `Buildings/SolarPanel.lua`, `Buildings/WindTurbine.lua`, `Buildings/StirlingGenerator.lua`, `Buildings/AdvancedStirlingGenerator.lua`, `Buildings/MoistureVaporator.lua`, `Buildings/WaterReclamation.lua`, `Buildings/TriboelectricScrubber.lua`
- **depots → 04-A** — shared storage / stockpiles / map-shared depots (Depot* family by function): `Buildings/StockpileController.lua`, `Buildings/SharedStorageBaseVisualOnly.lua`, `Buildings/Elevator.lua`, `Buildings/BaseElevator.lua`
- **ui → 04-C** — presentation, camera, overlays, notifications, input — engine-side game Lua (04-C decides tooling by route): `GameOverlays.lua`, `Hints.lua`, `MarsNotifications.lua`, `Config/camera.lua`, `Camera.lua`, `FollowCamera.lua`, `PhotoMode.lua`, `Lightmodel.lua`, `Decor.lua`, `FadingDecal.lua`, `NightLightObjects.lua`, `SelectionParticle.lua`, `GamepadTerrainObjects.lua`, `MarsMarkers.lua`, `RichPresence.lua`
- **commonlua → 04-C** — dev/tooling, boot, map generation and platform plumbing in Lua/ — 04-C owns the tooling gate by ROUTE: `Cheats.lua`, `Dev/GameTests.lua`, `Dev/MapTools.lua`, `Dev/fixup.lua`, `Telemetry.lua`, `CrashTest.lua`, `ProjectOptions.lua`, `Mod.lua`, `ModItemAttachment.lua`, `ModItemTech.lua`, `_init.lua`, `init.lua`, `Stubs.lua`, `_GameConst.lua`, `GameRandom.lua`, `MapData.lua`, `MapSwitch.lua`, `RandomMap/RandomMapGenerator.lua`, `RandomMap/RandomMapGenerator_Picard.lua`, `RandomMap/RandomMapGenerator_Asteroids.lua`, `RandomMap/RandomMapGeneratorEdit.lua`
- **services → 04-B** — caller-only: ambient life / in-dome service buildings: `AmbientLife/Visitslide.lua`, `AmbientLife/WorkArtWorkshop.lua`, `AmbientLife/WorkVRWorkshop.lua`, `Buildings/CasinoComplex.lua`, `Buildings/Playground.lua`
- **story → 04-B** — caller-only: exploration points of interest: `AsteroidPoI.lua`, `PlanetaryAnomalies.lua`
- **drones → 04-A** — caller-only: drone recharge / sensor rover: `Buildings/AttachedRechargeStations.lua`, `Units/RCSensor.lua`
- **logistics → 04-A** — caller-only: deposits and grid tunnels: `Buildings/SurfaceDeposit.lua`, `GridTunnelConnector.lua`
- **landscape → 04-A** — caller-only: terrain features: `Geysers.lua`
- **ui → 04-C** — caller-only: visual-only rendering: `HexGridRender.lua`, `VehicleSandTrace.lua`
- **services → 04-B** — NOROWS-only: ambient life / in-dome decoration: `AmbientLife/Visittable1.lua`, `Buildings/Decoration.lua`
- **logistics → 04-A** — NOROWS-only: extractors and refineries (where resources enter the network): `Buildings/AutomaticMicroGExtractor.lua`, `Buildings/MetalsExtractor.lua`, `Buildings/PreciousMineralsExtractor.lua`, `Buildings/RareMetalsRefinery.lua`, `Buildings/Refinery.lua`
- **construction → 04-A** — NOROWS-only: the constructable base: `Buildings/Constructable.lua`
- **domes → 04-B** — NOROWS-only: underground habitation cave: `Buildings/JumboCave.lua`
- **rockets → 04-B** — NOROWS-only: resupply definitions: `Resupply.lua`
- **disasters → 04-B** — NOROWS-only: vegetation objects (terraforming group): `VegetationObject.lua`
- **ui → 04-C** — NOROWS-only: localisation text tables: `LocalizationTexts.lua`
- **services → 04-B** — NOROWS-only, link 03 by the dlc tag: food ambient life and the diner: `AmbientLife/VisitFastFoodRestaurant.lua`, `AmbientLife/VisitFoodStand.lua`, `AmbientLife/VisitGourmetRestaurant.lua`, `AmbientLife/WorkFarmInsect.lua`, `AmbientLife/WorkFarmSmall.lua`, `AmbientLife/WorkFoodStand.lua`, `Buildings/Diner.lua`
- **construction → 04-A** — NOROWS-only, link 03 by the dlc tag: refab: `Refabable.lua`
- **colonists → 04-B** — NOROWS-only, link 03 by the dlc tag: the game-wide const table read by every colony system: `__const.lua`
- **commonlua → 04-C** — NOROWS-only, link 03 by the dlc tag: engine entity data (generated outside the four generated prefixes; an FR-1(c) surface — entities first spawned at new game) and the game config: `_EntityData.generated.lua`, `Config/config.lua`
- **commonlua → 04-C** — NOROWS-only: boot / config / platform / modding plumbing in Lua/ — 04-C decides tooling by route; render.lua is an FR-1 surface: `Config/Libs/Network.lua`, `Config/_config.lua`, `Config/_libs.lua`, `Config/_pfclasses.lua`, `Config/pathfind.lua`, `Config/render.lua`, `EpicDlcIds.lua`, `error.lua`, `Buildings/ModItemBuildingTemplate.lua`

**Mixed files split by CLASS prefix** (brief §2.A): the class prefix is tried before the basename, so a file splits whenever its functions carry different prefixes. Files whose rows landed in more than one system: `Lua/Asteroids.lua` (saveload/story), `Lua/BuildableGrid.lua` (construction/saveload), `Lua/Buildings/Anomaly.lua` (saveload/story), `Lua/Buildings/AsteroidCatcher.lua` (rockets/saveload/story), `Lua/Buildings/BaseRover.lua` (drones/saveload), `Lua/Buildings/BottomlessPit.lua` (saveload/story), `Lua/Buildings/Building.lua` (saveload/services), `Lua/Buildings/BuildingComponents.lua` (logistics/saveload/services), `Lua/Buildings/CaveInRubble.lua` (landscape/saveload), `Lua/Buildings/Community.lua` (saveload/services), `Lua/Buildings/ConstructionSite.lua` (construction/saveload), `Lua/Buildings/CrystalStatue.lua` (saveload/story), `Lua/Buildings/DefenceTower.lua` (disasters/rockets), `Lua/Buildings/Deposit.lua` (logistics/saveload), `Lua/Buildings/Dome.lua` (domes/saveload), `Lua/Buildings/DroneControl.lua` (drones/saveload), `Lua/Buildings/EffectDeposit.lua` (colonists/logistics/saveload), `Lua/Buildings/Elevator.lua` (depots/saveload), `Lua/Buildings/Factory.lua` (saveload/services), `Lua/Buildings/Farm.lua` (saveload/services), `Lua/Buildings/LandscapeLake.lua` (landscape/saveload), `Lua/Buildings/MicroGHabitat.lua` (saveload/services), `Lua/Buildings/NaturalHabitat.lua` (saveload/services), `Lua/Buildings/OpenAirBuilding.lua` (saveload/services), `Lua/Buildings/OpenCity.lua` (saveload/services), `Lua/Buildings/RocketUtilities.lua` (rockets/saveload), `Lua/Buildings/SensorTower.lua` (saveload/story), `Lua/Buildings/ShiftsBuilding.lua` (saveload/services), `Lua/Buildings/ShuttleHub.lua` (drones/rockets), `Lua/Buildings/SolarPanel.lua` (logistics/saveload), `Lua/Buildings/SpaceElevator.lua` (rockets/saveload), `Lua/Buildings/Station.lua` (saveload/trains), `Lua/Buildings/StockpileController.lua` (depots/saveload), `Lua/Buildings/StorageDepot.lua` (depots/saveload), `Lua/Buildings/SubsurfaceDeposit.lua` (logistics/saveload), `Lua/Buildings/TerraformingBuilding.lua` (disasters/saveload), `Lua/Buildings/Track.lua` (saveload/trains), `Lua/Buildings/TrackElement.lua` (saveload/trains), `Lua/Buildings/TradePad.lua` (rockets/saveload), `Lua/Buildings/TunnelBlockerRubble.lua` (landscape/saveload), `Lua/Buildings/UndergroundPassage.lua` (domes/saveload), `Lua/Buildings/Workplace.lua` (saveload/services), `Lua/CargoTransporterNew.lua` (rockets/saveload), `Lua/City.lua` (colonists/saveload), `Lua/Colony.lua` (colonists/saveload), `Lua/Dev/MapTools.lua` (commonlua/drones), `Lua/Dev/fixup.lua` (commonlua/saveload), `Lua/DustDevils.lua` (disasters/saveload), `Lua/DustStorm.lua` (disasters/saveload), `Lua/ElectricityGrid.lua` (logistics/saveload), `Lua/ElectricityStorage.lua` (logistics/saveload), `Lua/Factions/Factions.lua` (saveload/story), `Lua/Factions/Laws.lua` (saveload/story), `Lua/Factions/Legislature.lua` (saveload/story), `Lua/FadingDecal.lua` (saveload/ui), `Lua/Flight.lua` (drones/saveload), `Lua/GameRules.lua` (saveload/story), `Lua/GridObject.lua` (construction/saveload), `Lua/HasConsumption.lua` (saveload/services), `Lua/Hints.lua` (saveload/ui), `Lua/LRTransport.lua` (colonists/logistics/saveload), `Lua/MapData.lua` (commonlua/saveload), `Lua/MapSettings.lua` (disasters/saveload), `Lua/MarsGameEffects.lua` (colonists/saveload), `Lua/Marsquake.lua` (disasters/saveload), `Lua/Meteors.lua` (disasters/saveload), `Lua/Passage.lua` (domes/saveload), `Lua/RandomMap/RandomMapGenerator_Picard.lua` (commonlua/saveload), `Lua/RequiresMaintenance.lua` (saveload/services), `Lua/Research.lua` (saveload/story), `Lua/ResourceTracking.lua` (logistics/saveload), `Lua/Resources.lua` (logistics/saveload), `Lua/RevealDarkness.lua` (saveload/story), `Lua/RocketCompatibility.lua` (rockets/saveload), `Lua/SupplyGrid.lua` (logistics/saveload), `Lua/SupplyGridBreakable.lua` (logistics/saveload), `Lua/Terraforming.lua` (disasters/saveload), `Lua/TerraformingDisasters.lua` (disasters/saveload), `Lua/Units/Animals.lua` (saveload/services), `Lua/Units/Colonist.lua` (colonists/saveload), `Lua/Units/ColonistTransport.lua` (colonists/saveload), `Lua/Units/Drone.lua` (drones/saveload), `Lua/Units/DroneBase.lua` (drones/saveload), `Lua/Units/ExplorerRover.lua` (saveload/story), `Lua/Units/RCRover.lua` (drones/saveload), `Lua/Units/RCSafari.lua` (saveload/services), `Lua/Units/RCTransport.lua` (logistics/saveload), `Lua/UniversalRocket.lua` (rockets/saveload), `Lua/UpgradeUnlocks.lua` (saveload/services), `Lua/Vegetation.lua` (disasters/saveload), `Lua/WasteRock.lua` (landscape/saveload), `Lua/_StoryBits.lua` (saveload/story), `Lua/hex.lua` (construction/saveload).

### 1.5 · `CALLERS.tagged.tsv` — the (b′) pass (unit D)

| verdict | rows |
|---|---|
| benign | 2455 |
| F117-SHAPE | 8 |
| unsure | 2 |

**F117-SHAPE candidates (8)** — ⛔ candidates, not `C` entries; TAKEABLE WHEN the owning link reads the caller's body:

- `C00766` `CommonLua/Classes/ActionFX.lua:2052` (1.0.7 :1958) → 04-C — `local obj = self:GetLocObj(actor, target)` — appended action_pos feeds a NEW `Source == "ActionObj"` branch (ActionFX.lua:1329-1330, absent in 1.0.7); the three play-path callers were updated to pass it, this unchanged 2-argument call gets obj=false for an ActionObj-sourced FX (flagged by fan-out agent B16, parent re-read both bodies)
- `C00767` `CommonLua/Classes/ActionFX.lua:2821` (1.0.7 :2723) → 04-C — `local obj = self:GetLocObj(actor, target)` — appended action_pos feeds a NEW `Source == "ActionObj"` branch (ActionFX.lua:1329-1330, absent in 1.0.7); the three play-path callers were updated to pass it, this unchanged 2-argument call gets obj=false for an ActionObj-sourced FX (flagged by fan-out agent B16, parent re-read both bodies)
- `C00769` `CommonLua/Classes/ActionFX.lua:3967` (1.0.7 :3853) → 04-C — `local obj = self:GetLocObj(actor, target)` — appended action_pos feeds a NEW `Source == "ActionObj"` branch (ActionFX.lua:1329-1330, absent in 1.0.7); the three play-path callers were updated to pass it, this unchanged 2-argument call gets obj=false for an ActionObj-sourced FX (flagged by fan-out agent B16, parent re-read both bodies)
- `C00771` `Lua/_fixup.lua:1335` (1.0.7 :1231) → 04-B — `local obj = IsKindOf(fx, "ActionFX") and fx:GetLocObj(actor, target) or actor or target` — appended action_pos feeds a NEW `Source == "ActionObj"` branch (ActionFX.lua:1329-1330, absent in 1.0.7); the three play-path callers were updated to pass it, this unchanged 2-argument call gets obj=false for an ActionObj-sourced FX (flagged by fan-out agent B16, parent re-read both bodies)
- `C01139` `Lua/Units/ColonistTransport.lua:114` (1.0.7 :90) → 04-B — `local station, remote = GetTransportRoute(self, building, true, false, remote_stations)` — slot 4 renamed find_nearest->allow_reachable and this unchanged call still passes a boolean there: same value, new meaning
- `C01140` `Lua/Units/ColonistTransport.lua:123` (1.0.7 :99) → 04-B — `station, remote = GetTransportRoute(self, building, true, true, remote_stations)` — slot 4 renamed find_nearest->allow_reachable and this unchanged call still passes a boolean there: same value, new meaning
- `C01141` `Lua/Units/ColonistTransport.lua:136` (1.0.7 :112) → 04-B — `station, remote = GetTransportRoute(self, building, true, false, new_stations)` — slot 4 renamed find_nearest->allow_reachable and this unchanged call still passes a boolean there: same value, new meaning
- `C01142` `Lua/Units/ColonistTransport.lua:141` (1.0.7 :117) → 04-B — `return GetTransportRoute(self, building, true, true, new_stations)` — slot 4 renamed find_nearest->allow_reachable and this unchanged call still passes a boolean there: same value, new meaning

**unsure (2):**

- `C00203` `CommonLua/Camera.lua:801` → 04-C — LuaExportedDocs stub of a C function: the documented contract shrank to (map, ...) — whether C changed or only the doc did is not readable from Lua
- `C00694` `Lua/X/Infobar.lua:582` → 04-C — this caller passes a CITY (Infobar.lua:582, reached with UICity from :661 — agent B24); the benign ruling for GetEnvironment rests on ResolveMap taking a game object, and City.lua defines no GetMap/GetMapSlot in either tree, so whether ResolveMap(city) resolves is untraced — if not, ShouldShowDiscoveredDeposits is always false

Measured on the way: **0 of the 15 pure-`sig` rows** have a byte-identical body that still reads a parameter name the signature dropped (the dangling-name risk of a rename). The appended-parameter heuristic found **0** callee bodies that index a new parameter without a guard — ⛔ **and that heuristic was FALSIFIED once by the fan-out**: agent B16 showed `ActionFX:GetLocObj`'s appended `action_pos` feeds a NEW `Source == "ActionObj"` branch the four unchanged callers can never reach; the parent re-read both bodies and flipped them to F117-SHAPE (agent B10 likewise corrected three `from_ui` rows to benign — a sibling-class override the call-form test cannot see; agent B24 showed one of `GetEnvironment`'s nine callers, `Infobar.lua:582`, passes a CITY, not the game object the benign ruling assumed — flipped to `unsure`). ⇒ **three of unit D's per-callee rulings were corrected by the fan-out**; a per-callee verdict needs each call's ARGUMENT kind, not only the callee's contract. ⇒ every appended-parameter `benign` is **benign BY SHAPE only** (nil arrives, the pre-1.1.0 behaviour is kept); whether that caller NEEDED the new behaviour was not read. ⚠️ A shape unit D cannot see at all: a SAME signature whose body starts to need an argument (R08311 `CalcBaseExportFunding(amount, res_id)`, `RocketBase.lua:966` omits `res_id` — agent B12); those arrive as agent (b′) row verdicts, not CALLERS rows. Benign verdicts otherwise rest on the call-form homonym test (632 rows) and the signature shape; the text-level table cannot see dynamic dispatch (blind spot 7).

### 1.6 · Preset readable pile per registry (04-E) and 03's preset share

04-E: **25409 rows over 123 registries** (`none` + `REINDEX-SWAP` + `added-preset` + `removed-preset`). By registry, all of them: StoryBit 6689 · XDef 5500 · TechPreset 2574 · LawDef 1696 · FactionDef 1606 · BuildingTemplate 556 · PresetDef 532 · ActionFXParticles 529 · Tech 433 · SA_Exec 432 · AssemblyChoiceDef 424 · SponsorGoals 293 · TechFieldPreset 287 · ActionFXSound 280 · SA_Block 258 · OnScreenHint 254 · LightmodelPreset 253 · PopupNotificationPreset 221 · NotificationPreset 168 · TerrainObj 166 · ParticleSystemPreset 133 · SA_CheckExpression 111 · PolicyDef 107 · CheatDef 105 · Label 103 · TraitPreset 99 · CommanderProfilePreset 96 · RandomMapPreset 88 · SA_WaitMessage 76 · MissionSponsorPreset 74 · ConditionDef 65 · Milestone 60 · EffectDef 58 · ClassDef 57 · TutorialStep 51 · EncyclopediaArticle 50 · TechGroup 48 · XPresetMapLabel 46 · CargoBuildingPrefab 39 · Challenge 38 · ColoredSectionProps 32 · SA_CheckResearch 31 · Resource 30 · SA_WaitChoiceCheck 30 · MsgDef 25 · SA_WaitChoice 25 · ParentNotificationPreset 24 · SA_GrantResearchPts 24 · SA_PlaceObject 24 · Vegetation 24 · Trigger 22 · SA_GrantTechBoost 20 · SA_StopSequence 20 · BuildMenuSubcategory 19 · SA_WaitResearch 19 · GameRuleDef 18 · FlightPolicyDef 17 · TextStyle 16 · UILocationsPreset 16 · MapSettings_Meteor 15 · SA_GrantTech 15 · ScriptConditionDef 15 · StatsImpactRest 15 · StatusEffectPreset 15 · GameStateDef 14 · ScenarioSequence 12 · DiscoveryGenericPreset 11 · SA_SpawnAnomaly 11 · Achievement 10 · HUDNotificationPreset 10 · MapSettings_Marsquake 9 · MissionParamsDef 9 · Negotiation 9 · POI 9 · ScriptConditionList 9 · SA_AddChoiceEntry 8 · SA_AppendToLog 8 · CargoResource 6 · SA_CustomNotification 6 · WorkTypeDef 6 · FrostDef 5 · SA_GameplayConstModifier 5 · TutorialPreset 5 · AutoAttachPreset 4 · DiscoveryAsteroidPreset 4 · PFClassDef 4 · SA_WaitExpression 4 · SoundPreset 4 · StatsImpactWorkEnd 4 · Tutorial 4 · WindDef 4 · Cargo 3 · ColonyControlCenterCategory 3 · PopupEvent 3 · BuildCategory 2 · CargoUnit 2 · DumbAIDef 2 · FactionPolarizationDef 2 · IndependenceProgressDef 2 · PlayStationActivity 2 · SA_AddApplicants 2 · SA_CallTradeRocketWithCargo 2 · SA_DamageDrones 2 · SA_DestroyObjects 2 · StoryBitCategory 2 · AmbientLife 1 · AppendClassDef 1 · Camera 1 · ConstructionVisuals 1 · FFXDenoiserParameters 1 · NRDReblurParameters 1 · SA_BumpTechDiscover 1 · SA_ChangeFunding 1 · SA_ChangeStat 1 · SA_Comment 1 · SA_Repeat 1 · SA_ResuppyInventory 1 · SA_WaitChoiceEntries 1 · SA_WaitMarsTime 1 · SA_WaitTradeRocket 1 · ShadeShaderVars 1 · TimeOfDayVisuals 1 · TrophyGroup 1.

03 (presets): **1618 rows over 49 registries**: FactionDef 285 · PresetDef 251 · ResourcePreset 181 · CropPreset 153 · XDef 135 · StoryBit 127 · TechPreset 107 · LawDef 78 · Animal 26 · SA_Exec 23 · BuildingTemplate 22 · PolicyDef 21 · OnScreenHint 20 · CommanderProfilePreset 15 · Label 13 · Vegetation 13 · SA_WaitMessage 11 · AppendClassDef 10 · SoundPreset 10 · ClassDef 9 · EffectDef 8 · NotificationPreset 8 · PopupNotificationPreset 8 · Tech 8 · BuildMenuSubcategory 7 · EncyclopediaArticle 7 · Resource 7 · FlightPolicyDef 6 · AmbientLife 5 · GameRuleDef 5 · MissionSponsorPreset 5 · Challenge 4 · ParticleSystemPreset 4 · SA_GrantTechBoost 4 · CargoResource 3 · SponsorGoals 3 · Milestone 2 · MsgDef 2 · SA_WaitChoice 2 · Achievement 1 · BugReportTag 1 · DumbAIDef 1 · ScriptConditionList 1 · StatsImpactRest 1 · StatusEffectPreset 1 · TechFieldPreset 1 · TraitPreset 1 · Trigger 1 · TutorialStep 1.

Per churn class × link: COMMENT→NOT-READ(churn) 1 · REINDEX→NOT-READ(churn) 10462 · REINDEX-SWAP→03 217 · REINDEX-SWAP→04-E 1707 · T-ID→NOT-READ(churn) 22 · added-preset→03 55 · added-preset→04-E 1416 · none→03 1321 · none→04-E 21417 · removed-preset→03 25 · removed-preset→04-E 869.

### 1.7 · Field-report tags (README §2b) — BY FUNCTION

Rule (full text in the INVENTORY.tagged banner, column `fr`): FR-1(a) — **58 entry functions** on the New Game → first sol path, + one hop of their CHANGED callees (text-level; a callee name declared by >3 changed rows is NOT followed — skipped: `NewMapLoaded`, `CityStart`, `NewGame`, `ChangeMapDone`, `GetProperty`, `Activate`, `DoneMap`, `set`, `ModsReloaded`, `PostLoad`); FR-1(b) — an FR-1 row branching on `IsDlcAvailable`/`norman`, routed to 03; FR-1(c) — the render-setup files README §2b names + bodies naming an upscaler/AA feature; FR-1(d) — a changed line assigning `hr.*`; FR-2 — **45 entry functions** (deep-scan / probe / exploration / reveal / subsurface names or deep-scan body terms) + one hop (skipped: `RemoveNotification`, `GameInit`, `set`, `OnApplyEffect`, `GetIPDescription`, `GetDescription`, `OnPinClicked`, `PlayFX`, `GetProperty`, `GetError`); FR-3 — an added or changed line that creates or shortens periodic work. ⛔ Tagging by FILE was measured by link 01 at 800–1,400 rows per report; by function it is the counts below. ⛔ A tag is a SURFACE to read first, never a cause.

| tag | INVENTORY rows | 03 | 04-A | 04-B | 04-C | 04-D | 04-E | PRESETS rows |
|---|---|---|---|---|---|---|---|---|
| FR-1(a) | 142 | 10 | 6 | 33 | 78 | 15 | 0 | 0 |
| FR-1(b) | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| FR-1(c) | 61 | 0 | 0 | 0 | 61 | 0 | 0 | 948 |
| FR-1(d) | 15 | 0 | 1 | 0 | 12 | 2 | 0 | 0 |
| FR-2 | 107 | 7 | 17 | 53 | 21 | 9 | 0 | 102 |
| FR-3 | 308 | 21 | 35 | 122 | 59 | 71 | 0 | 0 |

**FR-1(b) = 0, MEASURED:** FR-1-path rows (entry or one hop) containing `IsDlcAvailable` or `norman`. The FR-1 rows already in 03 are there by the dlc-adjacent tag and are FR-1(b)'s surface for 03. ⚠️ FR-1's likeliest cause is native (README §2b, and since 8f8a73a a clean-install crash-to-desktop with no popup — a vanilla Lua error does not end the process, `F114`), so these rows are the Lua-visible surface only; 03/04 read new native calls, new assets and engine settings first. ⚠️ **FR-3 `PERF` gap, named for 99:** batches **B01–B15** were briefed BEFORE README §2b landed and were not asked for the `PERF` tell; **B16–B24** were. 04's agents re-open every WORTH-READING body with PERF in their briefs, so the gap is in 02's first pass — 99 should check 04 covered B01–B15's rows.

⛔ **FR-1 coverage hole, ROUTED as a text-diff item, not rows (README §2b after ce06307 — the DLSS 2 → DLSS 4 temporal-upscaler lead).** Top-level DATA TABLES in hand files produce no INVENTORY row (treediff enumerates functions) and no PRESETS row (presetdiff reads `generated` files only), so there is nothing to tag. MEASURED by the parent, both trees: `CommonLua/Core/options.lua` changed, 35 diff lines (5 function rows; `OptionsData` + the DLSS pick at 1.1.0 :219-224 are not rows) · `CommonLua/Core/GlobalStorageTables.lua` 4 (1 row) · `CommonLua/Classes/RenderFeaturesParams.lua` 410 (7 rows) · `CommonLua/Core/Postprocessing.lua` 25 (1 row) · `Lua/ProjectOptions.lua` 24 (2 rows) · `Lua/Config/` — `_config.lua`, `_libs.lua`, `config.lua`, `pathfind.lua`, `render.lua` changed with **0 rows**, `_pfclasses.lua` + `Libs/` new with 0 rows. ⇒ 04 agent C reads these as raw `diff` of both trees under FR-1, first. The same blind class (a changed top-level table in a hand file) exists tree-wide and is unmeasured here.

### 1.8 · `NOROWS.tsv` — changed hand files NO instrument lists, bucketed by the same partition (treediff v1.2, 6d95f45)

`reader=NONE` + `content=yes` + `bucket=hand`: **123 files, 4507 changed lines** — top-level data/config/const tables, preset data outside the four `generated` prefixes, anonymous `function(` literals. ⛔ They are NOT rows (no `rid`); each goes to its system's reader as a TEXT-DIFF item (04 §2 point 7), placed by the same path/basename rules + hand table as the rows, and routed to 03 where the file's CHANGED lines meet the two-tier dlc tag. By link: 04-C 90 · 03 18 · 04-A 9 · 04-B 6. `UNASSIGNED`: 0.

## §2 · The control

### 2.1 · The seeded-positive control — the AGENT POOL's score (01 scored the instrument, §0.12)

The four seeds went into ordinary batches with nothing marking them: F114 and F116 in B01 (trains), F115 in B02 (landscape + construction), F117 in B07 (colonists + domes + services). Trains were cut into their own batch so the four sat in three agents, not two. ⛔ The briefs' verbatim taxonomy had two "our scar" cells that NAME seeds (`map` prepended to `LandscapeForEachUnit`; `ChooseDome(traits…)` → `ChooseDome(colonist…)`); those two cells were redacted to `[example withheld]` in every brief, the one stated departure from verbatim, and agents were told not to open `docs/` (where `bugs/F11x.md` would name them).

| seed | expected (README §4) | agent returned | the real change named? | score |
|---|---|---|---|---|
| F114 `Train:UnloadAll` (R10714, B01) | (a) — the two nil-guards (+ `MultiResourceDepotBase`) | **(i)+(g)**, `GUARD+ dest.demand and dest.demand[res]` / `station.demand and station.demand[res]`, "cap becomes `demand and demand:GetTargetAmount() or 0`", new `BlackCube` branch; B01's NOTES separately name the Station → `MultiResourceDepotBase` migration | ✅ both guards, verbatim | content HIT · label: (i) not (a) |
| F115 `LandscapeForEachUnit` (R08560, B02) | (b) — `map` prepended | **(b)**, "leading map param; map.Landscapes"; ⭐ its SMELL independently found the dead `filter_embark` (tell 2, both trees) — the known F34(d) defect (REVERIFICATION F-8) | ✅ | HIT |
| F116 `TrackGridElement:DemolishAndSplitTrack` (R06991, B01) | (a) — pre-sort `ProcessAllElements` + `skip_track_process` | **(a)**, "adds a `ProcessAllElements()` pre-pass unless `skip_track_process`" + the orphan-track loop | ✅ | HIT |
| F117 `ChooseDome` (R11621, B07) | (b′) — argument-type change, callers enumerated | **(b)**, "`traits` → `colonist` passed to `GetScoreFor`/`HasFreeLivingSpaceFor`"; callers enumerated and the one odd one traced (`DroneFactory.lua:230` passes a colonist-data table, safe — only `.traits` read); also caught `best_eval` −1 → `CommunityEvalNone` (−700) | ✅ | content HIT · label: (b) not (b′) |

**Hit rate — both numbers, and the ruling:**
- **By content: 4 / 4.** Every seed came back with a sentence naming the real change.
- **By strict label: 2 / 4** (F115, F116 exact).
- ⚖️ **Parent's ruling: 4 / 4**, on these grounds, for 99 to overturn. **F114:** README §2 defines (i) as the derived shape "a guard added or removed"; F114's change *is* two added nil-guards, so (i) is the more specific form of a body change, not a misread (the agent also set `GUARD+` naming both). **F117:** README §2's (b′) needs "a call site in the SAME tree [that] still passes the old shape". F117's stale caller was OUR module in `Code/`, which is not in the vanilla tree; in vanilla, `CALLERS.tsv` shows 8 `changed` + 1 `new` + **0 `same`**, and the agent enumerated and traced them — so (b) is the correct class for the vanilla row. ⚠️ The ruling is the parent grading its own control, so it was not left to stand alone: a random **3 of the 21 non-seed batches** (B05, B06, B12 — `random.Random(20260910)`) were re-issued as round 2 to independent agents told not to open round 1, and the 20-row self-sample was done BLIND (the parent wrote its verdicts before reading the agents'). Both numbers are in 2.2.
- ⛔ The seeds' hit rate covers `hand` rows only — never `generated` rows, presets, or `DLC/` (README §4).

### 2.2 · The second numbers: the parent's BLIND self-sample, and round 1 vs round 2

**(a) Self-sample, n = 20, BLIND.** Twenty fan-out rows were drawn at random (`python tri_ledger.py sample 20 20260910` — R00182 R01348 R01462 R01763 R01857 R02123 R02188 R02262 R03422 R03444 R05673 R05864 R06350 R08352 R09174 R09656 R09666 R10727 R11104 R11129), read by the parent from the raw two-tree listing, and its verdicts WRITTEN DOWN before any agent verdict for those rows had been read (the parent's file predates every one of those batches' returns).

| measure | agreement |
|---|---|
| `WORTH-READING` vs `CHURN` — the routing decision 04 sizes from | **20 / 20** |
| `GUARD±` flag | **19 / 20** (R01348: the parent flagged `LoadedMaps[slot]` → `Maps[slot]` as a guard; the agent did not) |
| primary class | **15 / 20** |
| any class shared | **16 / 20** |

The five class splits are not misreads: three are one CONVENTION (R01763, R06350, R09666 — a body that adds a new call site; the parent wrote (a), the agent (f), and README §2 defines (f) as "new function / **new call site**", so the agent reads the taxonomy more literally than the parent did); R03422 shares (i), primary order differs; R01348 is a genuine judgement split ((c) storage-moved vs (a)). ⭐ **The agents found SMELLs the parent missed on 4 of the 20** (R01348 tell 3, R01462 tell 2, R02262 tell 3, R09656 tell 5 — a dev comment "will not work for split shapes") and matched the parent's one (R01857, tell 4). ⇒ the pool reads at least as closely as the parent on this sample.

**(b) Round 1 vs round 2** — **Round 1 vs round 2.** A random 3 of the 21 non-seed batches were re-issued (`random.Random(20260910)` → B05, B06, B12) to fresh agents told not to open round 1. B05.r2 + B06.r2 returned (**295 rows**): WORTH-READING vs CHURN **99 %** (291/295) · smell presence **94 %** · guard flag **92 %** · any class shared **89 %** · primary class **77 %**. The class splits cluster on the (a)/(c) and (a)/(f) boundaries — whether a changed data source is 'storage moved', whether a new call is a 'new call site' — the same soft edge the self-sample showed; the ROUTING decision 04 sizes from is stable. ⚖️ Re-read rows are MERGED so a second reading can only ADD coverage: round 1's class, WORTH-READING if EITHER round says so (**2** rows upgraded), round 2's SMELL where round 1 had none (**10** added); both rounds are kept in the parent's scratch record. ⚠️ **B12.r2 was issued and had NOT returned at commit time** (the owner flagged context budget); it is not part of this ledger — 99 may re-issue it.



## §3 · Row lists per link — POINTERS into the tagged TSVs, never copied rows

Each list is a filter on the tagged files; the order below is the reading order (b′)/(b)/(a) first, then (h) seeds, then `SMELL` rows, then the `WORTH-READING` count 04 sizes from. ⭐ **These counts are exact** — they are the files' own.

### 03 (seam)

- **INVENTORY.tagged.tsv:** 1289 rows (`$12=="03"`) — fan-out classified 320, `WORTH-READING` **301**, `CHURN` 19, `SMELL` 44, `GUARD±` 59, unsure 0; not fanned out: added/generated 99, added/hand 526, body+sig/generated 21, body/generated 121, body/hand 2, removed/generated 119, removed/hand 81.
- **PRESETS.tagged.tsv:** 1618 rows (`$11=="03"`) over 49 registries.
- **CALLERS.tagged.tsv:** 30 `same` rows (`$13=="03"`): benign 30.
- **by system:** removed-added 276 (WR 0) · services 185 (WR 77) · story 169 (WR 88) · preset:ClassDef 92 (WR 0) · preset:XDef 82 (WR 0) · saveload 59 (WR 14) · logistics 58 (WR 25) · preset:FactionDef 51 (WR 0) · rockets 46 (WR 28) · colonists 38 (WR 19) · preset:Tech 32 (WR 0) · preset:LawDef 29 (WR 0) · ui 23 (WR 10) · disasters 21 (WR 10) · domes 20 (WR 7) · commonlua 18 (WR 13) · preset:TechPreset 14 (WR 0) · preset:PolicyDef 12 (WR 0) · preset:FlightPolicyDef 6 (WR 0) · preset:StatsImpact 6 (WR 0) · preset:StatusEffectPreset 6 (WR 0) · preset:BuildingTemplate 4 (WR 0) · preset:CheatDef 4 (WR 0) · preset:NotificationPreset 4 (WR 0) · preset:TutorialStep 4 (WR 0) · drones 4 (WR 3) · trains 4 (WR 2) · depots 4 (WR 1) · preset:ClassDef-Conditions 3 (WR 0) · preset:SponsorGoals 3 (WR 0) · construction 3 (WR 3) · preset:Challenge 2 (WR 0) · preset:Event 2 (WR 0) · preset:GameRuleDef 2 (WR 0) · preset:ClassDef-PresetDefs 1 (WR 0) · preset:TraitPreset 1 (WR 0) · landscape 1 (WR 1).
- **NOROWS text-diff items — 18 files, 3097 changed lines** (no `rid`; `diff` both trees): `CommonLua/Libs/Research/ClassDefs/ClassDef-Conditions.generated.lua` (4), `CommonLua/Libs/Research/ClassDefs/ClassDef-PresetDefs.generated.lua` (5), `CommonLua/Libs/Research/Data/ClassDef-Conditions.lua` (10), `CommonLua/Libs/Research/Data/ClassDef-Effects.lua` (4), `CommonLua/Libs/Research/Data/ClassDef-PresetDefs.lua` (5), `Lua/AmbientLife/VisitFastFoodRestaurant.lua` (40), `Lua/AmbientLife/VisitFoodStand.lua` (27), `Lua/AmbientLife/VisitGourmetRestaurant.lua` (29), `Lua/AmbientLife/WorkFarmInsect.lua` (43), `Lua/AmbientLife/WorkFarmSmall.lua` (56), `Lua/AmbientLife/WorkFoodStand.lua` (26), `Lua/Buildings/Diner.lua` (4), `Lua/Buildings/RocketTrade.lua` (2), `Lua/Config/config.lua` (40), `Lua/Refabable.lua` (2), `Lua/UI/CreditsData.lua` (704), `Lua/_EntityData.generated.lua` (1749), `Lua/__const.lua` (347)
- ⭐ **FR rows FIRST (README §2b) — 36** (filter: `fr` column non-empty): **FR-1(a)** R05283 R05598 R07544 R08047 R08223 R09001 R09073 R09786 · **FR-1(a),FR-2** R08997 · **FR-1(a),FR-3** R07542 · **FR-2** R05697 R09340 R09449 R09452 R09474 R10168 · **FR-3** R06031 R06137 R06138 R06516 R06525 R07155 R07535 R08187 R08188 R08197 R08232 R08250 R08387 R09347 R09822 R09921 R10122 R10277 R10279 R10335
- ⭐ **FR preset rows — 6:** FR-1(c) ParticleSystemPreset 4, FR-2 EffectDef 1, FR-2 StoryBit 1 (filter `fr` column).
- **(b′)/(b) first — 22 rows** (filter: `class` starts `(b`): R05337 R05448 R05739 R05995 R06504 R06803 R06844 R07699 R07834 R07999 R08000 R08199 R08217 R08681 R10241 R10260 R10317 R10337 R10477 R10892 R10983 R11633
- **(h) seeds — 0 retired modules whose vanilla fix lands here:** —
- **SMELL rows — 44 (PASSING candidates; the tell and its line are in the `smell` column):** R02393 R02394 R05996 R06000 R06025 R06927 R07002 R07699 R08141 R08158 R08193 R08198 R08201 R08202 R08216 R08218 R08231 R08236 R08237 R08248 R08751 R08822 R08997 R09186 R09208 R09221 R09335 R09336 R09347 R09349 R09352 R09355 R09675 R10241 R10273 R10276 R10333 R10335 R10383 R10699 R10831 R11004 R11109 R11616

### 04 agent A — turf

- **INVENTORY.tagged.tsv:** 1199 rows (`$12=="04-A"`) — fan-out classified 696, `WORTH-READING` **596**, `CHURN` 100, `SMELL` 64, `GUARD±` 124, unsure 0; not fanned out: added/hand 381, body/hand 11, removed/hand 111.
- **CALLERS.tagged.tsv:** 449 `same` rows (`$13=="04-A"`): benign 449.
- **by system:** logistics 337 (WR 143) · drones 327 (WR 170) · construction 188 (WR 106) · landscape 170 (WR 99) · depots 94 (WR 31) · trains 83 (WR 47).
- **NOROWS text-diff items — 9 files, 38 changed lines** (no `rid`; `diff` both trees): `Lua/Buildings/AutomaticMicroGExtractor.lua` (2), `Lua/Buildings/Constructable.lua` (7), `Lua/Buildings/MetalsExtractor.lua` (12), `Lua/Buildings/PreciousMineralsExtractor.lua` (5), `Lua/Buildings/RareMetalsRefinery.lua` (2), `Lua/Buildings/Refinery.lua` (2), `Lua/Buildings/SurfaceDeposit.lua` (2), `Lua/Geysers.lua` (2), `Lua/Units/RCSensor.lua` (4)
- ⭐ **FR rows FIRST (README §2b) — 57** (filter: `fr` column non-empty): **FR-1(a)** R06178 R07650 R07665 R07668 R08267 · **FR-1(a),FR-2** R07688 · **FR-1(d)** R08571 · **FR-2** R05566 R05572 R05693 R06497 R06899 R06900 R06903 R06904 R06905 R06909 R06965 R07736 R07737 R10539 R10648 · **FR-2,FR-3** R06908 · **FR-3** R05565 R05614 R05621 R05627 R05628 R06582 R06703 R06709 R06710 R06830 R06862 R06978 R06987 R07010 R07709 R08261 R08270 R08277 R08279 R08282 R09201 R09631 R09665 R10233 R10534 R10598 R10600 R10610 R10650 R10652 R10660 R10690 R10693 R10702
- **(b′)/(b) first — 49 rows** (filter: `class` starts `(b`): R05372 R05537 R05562 R05568 R05896 R05941 R05942 R05946 R05952 R05953 R06497 R06511 R06795 R06837 R06839 R06847 R06900 R06990 R06996 R07013 R07644 R07704 R08264 R08277 R08288 R08479 R08493 R08552 R08554 R08558 R08559 R08560 R08561 R08563 R08566 R08765 R08916 R09652 R09897 R10499 R10512 R10519 R10533 R10604 R10608 R10651 R10678 R10681 R11669
- **(h) seeds — 9 retired modules whose vanilla fix lands here:** R-1 `LowStorageWarning` → Lua/ResourceTracking.lua:222-310 (Food + maintenance branches deleted) — agent B05 found no replacement for the maintenance-supply warning; R-6 `SmallLandscapeSites` → Lua/Landscape/LandscapeConstructionSiteBase.lua:171-177, :204-208 GetClosestDests / GetTopClosestDests; R-7 `DroneTransportMinors (b)` → Lua/Units/Drone.lua:73, :935-937, :943-945 passability handler; R-8 `DroneUnreachableForever` → Lua/Units/Drone.lua:889-911, :971-976 MarkUnreachable; Building.lua:546; Landscaping.lua:328; R-23 `DustStormUndergroundBreaks` → Lua/SupplyGrid.lua:1097-1138, :1520 RandomBreakConnection; R-26 `LandscapeCostRefresh` → Lua/Buildings/ConstructionSite.lua:721 construction_costs_at_start guard; R-31 `StorageRateModifiers` → Lua/ElectricityStorage.lua:55-56, :240-249; Lua/LifeSupportStorage.lua:9-10, :109-110; R-34 `TrainMinors` → Lua/Buildings/Track.lua:62-67, :423-426, :596 GetTrainsOnRoute; Lua/TrainTransport.lua:492-537; R-35 `TrainPlatformWedge` → Lua/Units/ColonistTransport.lua:660-667; Lua/Units/Train.lua:424-451
- **SMELL rows — 64 (PASSING candidates; the tell and its line are in the `smell` column):** R05485 R05537 R05542 R05563 R05568 R05624 R05637 R05890 R05929 R05943 R06205 R06503 R06511 R06678 R06694 R06703 R06788 R06799 R06800 R06802 R06804 R06808 R06820 R06823 R06853 R06965 R06979 R06980 R06987 R06991 R06996 R07644 R07647 R07680 R07717 R08275 R08277 R08460 R08464 R08468 R08470 R08479 R08487 R08497 R08516 R08530 R08560 R08584 R08586 R08589 R08593 R09159 R09653 R09654 R09656 R09890 R10232 R10506 R10534 R10651 R10711 R10713 R10755 R11667

### 04 agent B — colony

- **INVENTORY.tagged.tsv:** 2408 rows (`$12=="04-B"`) — fan-out classified 1230, `WORTH-READING` **1074**, `CHURN` 156, `SMELL` 90, `GUARD±` 176, unsure 0; not fanned out: added/hand 929, body/hand 11, removed/hand 238.
- **CALLERS.tagged.tsv:** 577 `same` rows (`$13=="04-B"`): benign 572, F117-SHAPE 5.
- **by system:** story 595 (WR 308) · services 532 (WR 231) · rockets 348 (WR 171) · colonists 280 (WR 145) · saveload 268 (WR 24) · domes 194 (WR 93) · disasters 191 (WR 102).
- **NOROWS text-diff items — 6 files, 44 changed lines** (no `rid`; `diff` both trees): `Lua/AmbientLife/Visittable1.lua` (13), `Lua/Buildings/Decoration.lua` (17), `Lua/Buildings/JumboCave.lua` (4), `Lua/Mysteries/TheMarsBug.lua` (6), `Lua/Resupply.lua` (2), `Lua/VegetationObject.lua` (2)
- ⭐ **FR rows FIRST (README §2b) — 199** (filter: `fr` column non-empty): **FR-1(a)** R07534 R08006 R08346 R08636 R08785 R08948 R08954 R08955 R08963 R08964 R08965 R08967 R08970 R08977 R08978 R08979 R08980 R09071 R09091 R09122 R09136 R09672 R09859 R09864 R09870 R10248 R11643 R11644 · **FR-1(a),FR-2** R08740 R08953 R09132 R10414 · **FR-1(a),FR-3** R08982 · **FR-2** R05284 R05285 R05286 R05293 R05294 R05296 R05297 R05298 R05299 R05300 R05473 R05530 R05832 R05923 R05926 R06347 R06459 R06902 R07021 R07213 R07823 R07824 R07826 R07827 R07829 R07830 R07831 R08685 R08835 R08836 R09070 R09083 R09089 R09121 R09244 R09245 R09247 R09248 R09337 R09475 R09671 R10488 R10579 R10847 R10914 · **FR-2,FR-3** R05295 R07825 R08124 R08815 · **FR-3** R05249 R05254 R05255 R05258 R05262 R05263 R05316 R05317 R05318 R05328 R05341 R05380 R05383 R05554 R05560 R05576 R05657 R05658 R05683 R05684 R05735 R05801 R05815 R05958 R05969 R05970 R06184 R06328 R06559 R06665 R06674 R06676 R06712 R06757 R06774 R06793 R06869 R07016 R07017 R07142 R07152 R07154 R07167 R07526 R07537 R07554 R07555 R07557 R07558 R07567 R07735 R07764 R07765 R07766 R07774 R07776 R07778 R07792 R07797 R08094 R08164 R08631 R08652 R08686 R08687 R08713 R08725 R08726 R08736 R08737 R08743 R08773 R08776 R08781 R08782 R08783 R08789 R08795 R08798 R08802 R08803 R08804 R08807 R08812 R08816 R08819 R08821 R08871 R08881 R08899 R08939 R09294 R09297 R09298 R09458 R09478 R09862 R09871 R09872 R09876 R09881 R09882 R09883 R09913 R09946 R10283 R10410 R10491 R10584 R10635 R10894 R10898 R10905 R10906 R10959 R11637 R11659
- **(b′)/(b) first — 95 rows** (filter: `class` starts `(b`): R05243 R05284 R05385 R05422 R05473 R05476 R05556 R05576 R05586 R05592 R05595 R05677 R05704 R05725 R05733 R05734 R06183 R06206 R06212 R06320 R06335 R06470 R06557 R06609 R06623 R06625 R06931 R06956 R07053 R07070 R07093 R07094 R07122 R07147 R07158 R07207 R07784 R07785 R07794 R07798 R07839 R07995 R08119 R08131 R08171 R08311 R08466 R08690 R08786 R08788 R08789 R08790 R08817 R08828 R08829 R08833 R08835 R08841 R08858 R08874 R08875 R08926 R08930 R09080 R09086 R09319 R09478 R09502 R09670 R09882 R09932 R09946 R10265 R10304 R10306 R10322 R10341 R10365 R10422 R10443 R10495 R10809 R10829 R10837 R10842 R10844 R10846 R10849 R10859 R10869 R10878 R10921 R10925 R11621 R11688
- **(h) seeds — 21 retired modules whose vanilla fix lands here:** R-2 `LanderCargoRatchet` → Lua/UniversalRocket.lua:2046, :2069-2086, :2537-2546; R-3 `TouristSatisfaction` → Colonist Satisfaction stat removed (UpdateSatisfaction / ChangeSatisfaction gone); R-4 `AutomationLawCompensation` → Lua/Buildings/Workplace.lua:269-294; R-5 `UpgradeModifierLeak` → Lua/Buildings/Building.lua:1303-1311 StopUpgradeModifiers; CommonLua/Classes/Modifiers.lua:479-484; R-9 `MeteorFrequency` → Lua/Meteors.lua:293-322, :388, :390-412 (MapGameTimeRepeat scheduler); R-10 `MeteorStormWedge` → Lua/Meteors.lua:267-270, :329-386, :390-412; R-11 `AsteroidLanderAvailable` → Lua/PlanetaryView.lua:245-265; Lua/UI/PlanetUI.lua:1701-1710; R-12 `GridGlobalStorage` → Lua/ScriptBlocks.lua:387-419 ScriptFunc_DomesGridStorage; R-14 `RainsDeadlock` → Lua/TerraformingDisasters.lua:142, :191-194, :363-395; R-15 `DustSicknessDamage` → Data/TraitPreset.lua:80-84 (preset) + Lua/TraitPreset.lua:36 DailyUpdate rename; R-17 `UniversityOvertraining` → Lua/Buildings/Workplace.lua:249, :283-287, :433-434; Lua/City.lua:636-661; R-18 `CaveInsNoDisasters` → Lua/Marsquake.lua MapGameTimeRepeat("UndergroundMarsquake") condition; R-20 `DisasterPredictionLeak` → Lua/Meteors.lua:1204-1212 EndMeteorStorm; Lua/MapSettings.lua:223-236; Lua/TerraformingDisasters.lua:256, :349; R-21 `DustDevilSpawnGate` → Lua/DustDevils.lua:235-237, :256 scheduler; R-22 `DustDevilsDescrMap` → Lua/DustDevils.lua:59-64 GetDustDevilsDescr; R-24 `ExtractorStaffedPerformance` → Lua/Buildings/Workplace.lua:270-287; Lua/Units/Colonist.lua:794-796; R-25 `LanderReturnFuel` → Lua/UniversalRocket.lua:436, :441, :1891-1895; R-28 `MilestoneCrash` → Lua/Milestones.lua:116, :125-159; R-29 `MoraleComfortTooltip` → Lua/Units/Colonist.lua:3851-3855, :4862-4884; Lua/Stats.lua:814-925; R-33 `TouristApplicants` → Lua/HolidayRating.lua:87-106; R-36 `90_SaveSanitizer` → Lua/Config/config.lua:174-175; CommonLua/SavegameFixup.lua:10-16; WindTurbine.lua:98; Station.lua:1504
- **SMELL rows — 90 (PASSING candidates; the tell and its line are in the `smell` column):** R05259 R05282 R05294 R05385 R05430 R05456 R05678 R05749 R05750 R05798 R06143 R06325 R06328 R06331 R06439 R06480 R06548 R06561 R06652 R06668 R06791 R06923 R07061 R07085 R07130 R07134 R07139 R07141 R07142 R07147 R07530 R07531 R07831 R07985 R08311 R08436 R08444 R08745 R08746 R08754 R08830 R08832 R08853 R08866 R08925 R09035 R09079 R09089 R09100 R09130 R09264 R09265 R09271 R09329 R09331 R09462 R09463 R09465 R09466 R09467 R09478 R09524 R09526 R09530 R09533 R09892 R09916 R09927 R09932 R09973 R10309 R10324 R10327 R10387 R10388 R10393 R10396 R10479 R10483 R10788 R10809 R10837 R10858 R10871 R10931 R10942 R11637 R11638 R11657 R11676

### 04 agent C — engine

- **INVENTORY.tagged.tsv:** 2871 rows (`$12=="04-C"`) — fan-out classified 1453, `WORTH-READING` **1255**, `CHURN` 198, `SMELL` 191, `GUARD±` 212, unsure 1; not fanned out: added/hand 994, body+sig/hand 3, body/hand 50, removed/hand 369, sig/hand 2.
- **CALLERS.tagged.tsv:** 1000 `same` rows (`$13=="04-C"`): benign 995, F117-SHAPE 3, unsure 2.
- **by system:** commonlua 2478 (WR 1052) · ui 393 (WR 203).
- **NOROWS text-diff items — 90 files, 1328 changed lines** (no `rid`; `diff` both trees): `CommonLua/Classes/GameEffect.lua` (2), `CommonLua/Classes/ObjContainer.lua` (2), `CommonLua/Classes/Particles/ParticleBehavior.lua` (1), `CommonLua/Connectivity.lua` (2), `CommonLua/Core/ProceduralMeshShaders.lua` (2), `CommonLua/Core/config.lua` (6), `CommonLua/Core/const.lua` (3), `CommonLua/Core/error.lua` (4), `CommonLua/Core/terminal.lua` (8), `CommonLua/Data/LightmodelFeaturePreset.lua` (37), `CommonLua/Data/MsgDef.lua` (50), `CommonLua/Data/PersistedRenderVars.lua` (11), `CommonLua/Data/PropertyCategory.lua` (16), `CommonLua/Data/TerrainObj.lua` (1), `CommonLua/Data/XDef/AmountControl.lua` (13), `CommonLua/Data/XDef/BugReport.lua` (17), `CommonLua/Data/XDef/CommonMessageDialog.lua` (9), `CommonLua/Data/XDef/CommonShortcuts.lua` (20), `CommonLua/Data/XDef/EULADialog.lua` (2), `CommonLua/Data/XDef/EditorShortcuts.lua` (2), `CommonLua/Data/XDef/GedArtSpecEditor.lua` (13), `CommonLua/Data/XDef/GedAutoAttachEditor.lua` (4), `CommonLua/Data/XDef/GedCharacterBrowser.lua` (2), `CommonLua/Data/XDef/GedPopupList.lua` (3), `CommonLua/Data/XDef/GedPropRollover.lua` (2), `CommonLua/Data/XDef/GedPropertyButton.lua` (1), `CommonLua/Data/XDef/GedScriptEditor.lua` (8), `CommonLua/Data/XDef/GedShortcuts.lua` (15), `CommonLua/Data/XDef/GedStatusBar.lua` (57), `CommonLua/Data/XDef/ModEditor.lua` (14), `CommonLua/Data/XDef/PresetEditor.lua` (1), `CommonLua/Data/XDef/PrgEditor.lua` (2), `CommonLua/Data/XDef/PropChoice.lua` (2), `CommonLua/Data/XDef/SelectionEditorDlgUI.lua` (27), `CommonLua/Data/XDef/StdItemChoiceDialogBase.lua` (1), `CommonLua/Data/__SceneParamDef.lua` (29), `CommonLua/Data/__const.lua` (17), `CommonLua/Editor/XEditor/XAreaCopyTool.lua` (4), `CommonLua/Editor/XEditor/XClutterDensityBrush.lua` (2), `CommonLua/Editor/XEditor/XEnrichTerrainTool.lua` (1), `CommonLua/Editor/XEditor/XPlaceMultipleObjectsToolBase.lua` (4), `CommonLua/Ged/XDefClasses/GedPropertyButton.generated.lua` (1), `CommonLua/Libs/DevToolsPublic/Data/XDef/DevToolsShortcuts.lua` (54), `CommonLua/Libs/MapGen/Data/MapGen/MapGen-Default.lua` (12), `CommonLua/Libs/MapGen/Data/MapGen/MapGen-SubProc.lua` (42), `CommonLua/Libs/MapGen/Data/MapGen/MapGen-Tools.lua` (2), `CommonLua/Libs/MapGen/Data/__const.lua` (6), `CommonLua/Libs/Notifications/Data/XDef/DefaultNotification.lua` (23), `CommonLua/Libs/Notifications/LabelNotificationPreset.lua` (4), `CommonLua/Libs/Objectives/Data/MsgDef.lua` (24), `CommonLua/Libs/Objectives/Data/__load.lua` (1), `CommonLua/Libs/Paradox/Data/XDef/ParadoxAccountDialog.lua` (4), `CommonLua/Libs/Paradox/Data/XDef/ParadoxAccountLogIn.lua` (9), `CommonLua/Libs/Paradox/Data/XDef/ParadoxAccountSignUp.lua` (9), `CommonLua/Libs/Paradox/Data/XDef/ParadoxUIActionBars.lua` (3), `CommonLua/Libs/Research/Research.lua` (1), `CommonLua/Libs/TriggersAndEvents/Data/XDef/XEventDialog.lua` (14), `CommonLua/Libs/Tutorial/Data/XDef/TutorialHintPopup.lua` (268), `CommonLua/Libs/Tutorial/Data/XDef/TutorialListEntry.lua` (94), `CommonLua/Libs/Tutorial/Data/__load.lua` (1), `CommonLua/Libs/__DebugAdapter.lua` (2), `CommonLua/Libs/__DevToolsPrivate.lua` (3), `CommonLua/Libs/__DevToolsPublic.lua` (3), `CommonLua/NonDevStubs.lua` (5), `CommonLua/Patterns.lua` (2), `CommonLua/ThreePointLighting.lua` (31), `CommonLua/UI/PluginUIs.lua` (3), `CommonLua/X/XButton.lua` (1), `CommonLua/X/XLabel.lua` (1), `CommonLua/X/XShaderEffect.lua` (1), `CommonLua/X/XTemplate.lua` (2), `CommonLua/_EntityData.generated.lua` (32), `CommonLua/_Stubs.lua` (2), `Lua/Buildings/ModItemBuildingTemplate.lua` (3), `Lua/Config/Libs/Network.lua` (1), `Lua/Config/_config.lua` (5), `Lua/Config/_libs.lua` (4), `Lua/Config/_pfclasses.lua` (63), `Lua/Config/pathfind.lua` (55), `Lua/Config/render.lua` (10), `Lua/EpicDlcIds.lua` (1), `Lua/LocalizationTexts.lua` (53), `Lua/UI/LoadingScreen.lua` (2), `Lua/X/XLayers.lua` (2), `Lua/XTemplates/ModsUIDialog.lua` (10), `Lua/XTemplates/ModsUIMainContent.lua` (14), `Lua/XTemplates/ModsUIModDetails.lua` (2), `Lua/XTemplates/ModsUIPCGamepadSearch.lua` (6), `Lua/XTemplates/PGMainMenu.lua` (2), `Lua/error.lua` (18)
- ⭐ **FR rows FIRST (README §2b) — 214** (filter: `fr` column non-empty): **FR-1(a)** R00280 R00357 R01173 R01216 R01220 R01291 R01292 R01311 R01333 R01439 R01442 R01487 R01563 R01743 R01744 R01745 R01746 R01747 R01748 R01753 R01754 R01755 R01756 R01757 R02038 R02196 R02207 R02208 R02237 R02238 R02245 R02246 R02247 R02248 R02249 R02250 R02251 R02261 R02263 R02283 R02421 R02554 R03056 R03340 R03366 R03368 R03541 R07099 R08620 R08664 R08920 R08992 R08995 R08996 R08998 R08999 R09005 R09006 R09008 R09009 R09842 R09843 R10149 R10191 R10217 R11052 R11053 R11054 R11730 R11731 · **FR-1(a),FR-1(c)** R00572 · **FR-1(a),FR-1(d)** R09002 · **FR-1(a),FR-2** R01365 R02154 R02553 R08616 R08618 R10194 · **FR-1(c)** R00529 R00530 R00532 R00533 R00534 R00535 R00536 R00537 R00538 R00539 R00540 R00541 R00542 R00543 R00544 R00545 R00546 R00547 R00553 R00554 R00555 R00556 R00557 R00558 R00559 R00560 R00562 R00563 R00564 R00565 R00566 R00567 R00568 R00569 R00573 R00574 R00575 R00576 R00577 R00578 R00579 R01130 R01131 R01132 R01133 R01134 R01135 R01136 R01252 R02043 R03348 · **FR-1(c),FR-1(d)** R00531 R00548 R00549 R00550 R00551 R00552 R00561 R00570 · **FR-1(c),FR-3** R00571 · **FR-1(d)** R03449 R03451 R03452 · **FR-2** R00222 R00350 R01313 R01525 R02548 R03055 R08343 R08411 R08413 R08415 R08430 R10203 R11061 R11068 R11157 · **FR-3** R00012 R00213 R00320 R01232 R01236 R01330 R01387 R01404 R01553 R01762 R01765 R01855 R02047 R02254 R02267 R02358 R02425 R03049 R03082 R03094 R03095 R03305 R03362 R03473 R03553 R03557 R03624 R07169 R07179 R07181 R07738 R08255 R08334 R08425 R08612 R08613 R08676 R08677 R10145 R10166 R10170 R10172 R10182 R10201 R10213 R10214 R10215 R10216 R10996 R11127 R11139 R11150 R11151 R11153 R11156 R11184 R11187 R11195
- **(b′)/(b) first — 100 rows** (filter: `class` starts `(b`): R00013 R00021 R00025 R00140 R00153 R00182 R00190 R00195 R00239 R00240 R00256 R00257 R00271 R00280 R00325 R00330 R00354 R00373 R00392 R00405 R00520 R00572 R01023 R01080 R01082 R01084 R01094 R01097 R01138 R01176 R01243 R01258 R01270 R01290 R01301 R01358 R01384 R01487 R01540 R01542 R01588 R01592 R01615 R01621 R01623 R01720 R01722 R01724 R01758 R01760 R01778 R01779 R01832 R01923 R01932 R01953 R01954 R01957 R02001 R02106 R02113 R02130 R02213 R02216 R02221 R02223 R02238 R02366 R02411 R02429 R03028 R03033 R03061 R03140 R03141 R03229 R03231 R03240 R03241 R03252 R03253 R03277 R03299 R03301 R03329 R03399 R03522 R03524 R03533 R03584 R03593 R03608 R03609 R03610 R07176 R08616 R10186 R10987 R11012 R11125
- **(h) seeds — 0 retired modules whose vanilla fix lands here:** —
- **SMELL rows — 191 (PASSING candidates; the tell and its line are in the `smell` column):** R00025 R00030 R00125 R00163 R00256 R00257 R00267 R00278 R00320 R00323 R00365 R00369 R00531 R01023 R01082 R01094 R01196 R01216 R01233 R01239 R01247 R01261 R01276 R01280 R01287 R01296 R01299 R01317 R01322 R01339 R01348 R01362 R01418 R01421 R01438 R01450 R01457 R01462 R01466 R01469 R01470 R01472 R01491 R01499 R01507 R01557 R01597 R01623 R01624 R01628 R01629 R01693 R01731 R01759 R01790 R01810 R01811 R01814 R01832 R01833 R01857 R01863 R01866 R01875 R01904 R01906 R01925 R01936 R01938 R01939 R01940 R01948 R01949 R01967 R01968 R02011 R02038 R02041 R02043 R02047 R02064 R02100 R02109 R02122 R02130 R02131 R02142 R02143 R02144 R02152 R02153 R02162 R02178 R02180 R02182 R02183 R02193 R02194 R02202 R02209 R02224 R02231 R02247 R02262 R02263 R02278 R02302 R02385 R02388 R02390 R02415 R02446 R03024 R03060 R03198 R03200 R03201 R03209 R03224 R03243 R03261 R03274 R03280 R03297 R03305 R03318 R03322 R03344 R03345 R03346 R03367 R03373 R03398 R03499 R03501 R03505 R03543 R03544 R03545 R03550 R03554 R03558 R03559 R03560 R03561 R03562 R03574 R03612 R03627 R03628 R07748 R08429 R08430 R08992 R09002 R09008 R10157 R10167 R10188 R10209 R10216 R10225 R10979 R10984 R10985 R10990 R10991 R10993 R10997 R11002 R11005 R11014 R11016 R11019 R11020 R11026 R11046 R11048 R11066 R11068 R11075 R11082 R11086 R11087 R11127 R11143 R11145 R11150 R11157 R11158 R11166
- **unsure — 1:** `R02189` no_edit@550220 — unsure: row′s own one-line no_edit is identical; span over-runs into the property table an

### 04 agent D — storage + removed/added

- **INVENTORY.tagged.tsv:** 2003 rows (`$12=="04-D"`) — fan-out classified 0, `WORTH-READING` **0**, `CHURN` 0, `SMELL` 0, `GUARD±` 0, unsure 0; not fanned out: added/hand 1414, removed/hand 589.
- **CALLERS.tagged.tsv:** 0 `same` rows (`$13=="04-D"`): none.
- **by system:** removed-added 2003 (WR 0).
- **NOROWS text-diff items — 0 files, 0 changed lines** (no `rid`; `diff` both trees): —
- ⭐ **FR rows FIRST (README §2b) — 95** (filter: `fr` column non-empty): **FR-1(a)** R00010 R00433 R00508 R00510 R01573 R01574 R01575 R01577 R01579 R02481 R03135 R09590 R09591 R09804 · **FR-1(a),FR-2** R02695 · **FR-1(d)** R02051 · **FR-1(d),FR-3** R02747 · **FR-2** R00607 R02464 R06303 R09417 R09435 R09745 R09805 R09993 · **FR-3** R01572 R02343 R02448 R02452 R02453 R02454 R02455 R02478 R02484 R02485 R02488 R02489 R02499 R02501 R02505 R02506 R02508 R02516 R02517 R02522 R02592 R02597 R02598 R02605 R02608 R02609 R02680 R02683 R02757 R02768 R02772 R02773 R02854 R02891 R02968 R02969 R02971 R02981 R05240 R06234 R06299 R08641 R09396 R09412 R09413 R09426 R09436 R09536 R09537 R09566 R09712 R09713 R09769 R09817 R09821 R09998 R10002 R10013 R10034 R10046 R10058 R10065 R10070 R10080 R10096 R10099 R10100 R10106 R10108 R10126
- **(b′)/(b) first — 0 rows** (filter: `class` starts `(b`): —
- **(h) seeds — 0 retired modules whose vanilla fix lands here:** —
- **SMELL rows — 0 (PASSING candidates; the tell and its line are in the `smell` column):** —

### 04 agents E — presets, one per registry

- **INVENTORY.tagged.tsv:** 1972 rows (`$12=="04-E"`) — fan-out classified 0, `WORTH-READING` **0**, `CHURN` 0, `SMELL` 0, `GUARD±` 0, unsure 0; not fanned out: added/generated 1008, body+sig/generated 76, body/generated 382, removed/generated 503, sig/generated 3.
- **PRESETS.tagged.tsv:** 25409 rows (`$11=="04-E"`) over 123 registries.
- **CALLERS.tagged.tsv:** 409 `same` rows (`$13=="04-E"`): benign 409.
- **NOROWS text-diff items — 0 files, 0 changed lines** (no `rid`; `diff` both trees): —
- ⭐ **FR rows FIRST (README §2b) — 0** (filter: `fr` column non-empty): —
- ⭐ **FR preset rows — 1044:** FR-1(c) ActionFXParticles 509, FR-1(c) LightmodelPreset 242, FR-1(c) ParticleSystemPreset 120, FR-1(c) ActionFXSound 73, FR-2 StoryBit 69, FR-2 TechPreset 20, FR-2 SponsorGoals 6, FR-2 Tech 2, FR-2 XDef 2, FR-2 CheatDef 1 (filter `fr` column).
- **(b′)/(b) first — 0 rows** (filter: `class` starts `(b`): —
- **(h) seeds — 6 retired modules whose vanilla fix lands here:** R-13 `LastTransmissionStorage` → Data/FactionDef/LastTransmission.lua:104-260 (preset); R-16 `IndependenceTerraforming` → Data/Tech.lua:3557-3577 (preset); R-19 `CommandCenterNumbers` → Data/XDef/CommandCenterCategories.lua:226-244 (preset); R-27 `LocalizedUIText` → Lua/XDef/TerraformingOverall.generated.lua:56-57 etc. (XDef preset twins); R-30 `SpaceYDroneCapBullet` → Data/MissionSponsorPreset.lua:631, :702-705 (preset); Lua/PreGameMission.lua:261, :284; R-32 `TechDescriptionBuilding` → Data/Tech.lua:6737-6747; Data/TechPreset.lua:512-515 (preset)
- **SMELL rows — 0 (PASSING candidates; the tell and its line are in the `smell` column):** —

### 04's sizing line (04 §2.1: ~250 WORTH-READING rows per agent)

| 04 agent | WORTH-READING (fan-out) | + not-fanned rows it also owns | preset rows |
|---|---|---|---|
| 04 agent A — turf | 596 | 503 | 0 |
| 04 agent B — colony | 1074 | 1178 | 0 |
| 04 agent C — engine | 1255 | 1418 | 0 |
| 04 agent D — storage + removed/added | 0 | 2003 | 0 |
| 04 agents E — presets, one per registry | 0 | 1972 | 25409 |

### 3.x · The fan-out agents' cross-row NOTES, VERBATIM (leads for 03/04 — claims, not findings)

Each agent ended with a NOTES line: contract shifts it saw outside its rows, caller tables that misled, rows it could not settle. They are reproduced unedited because several are tree-wide (the `table.ifilter` callback contract, the `OnSetWorking` move to `RecursiveCallMethods`) and a paraphrase would drop the citation. ⛔ Every one is an agent's claim; the parent re-checked only the two that touched unit D (B10, B16 — see 1.5).

- **B01** (brief `2be60bc2c636`) — COUNTS: given 63, returned 63, WORTH-READING 49, CHURN 14, SMELL 16, unsure 0 — NOTES: No span was wrong. (1) Caller tables mislead through homonyms. R06803 lists ResourceStockpile.lua lines, which belong to ResourceStockpileBase; Station's real callers are MultiResourceCubeVisuals.lua:154/181/271/307, and 154 and 307 are unguarded against the new nil return. R06996's "same" rows at TrackElement.lua:241/783 call TrackBase, not the element. R06990's table is mostly GameShortcuts strings. R06807's table is empty although dome/community GetScoreFor callers exist, all passing colonist, so nothing is stale. (2) I withdrew a candidate smell on R06988 (`#self.fallback_elements` while the field is false). The dev comment at Tracks.lua:350 ("#nil/false is valid") says this engine allows # on false or nil. Any smell built on #false or #nil needs that fact first. (3) Four new Msgs (TrainStationOperational, StationStorageChanged x2, TrainLoadedUnloaded) have no in-tree listener; I flagged them as tell 2, but they may be modding hooks. (4) Recurring seams for links 03/04: Station migrated from UniversalStorageDepotBase to MultiResourceDepotBase (rows R06797/R06799/R06800/R06803/R06810/R06819/R06820/R06823); the new g_ClusterWorkplacesVersion GameVar is bumped from trains, stations and routes; OpenCity was added to station linking. (5) R06788: the UndergroundTrains lock is gone, but a mission-payload UI still reads `needs_underground_trains`. (6) R10718's `end--]]` has no opening `--[[` in either tree; it is a stray line comment and the function is live.
- **B02** (brief `e5488a6c2dce`) — COUNTS: given 175, returned 175, WORTH-READING 162, CHURN 13, SMELL 15, unsure 0 — NOTES: (1) Engine callee contract moved: table.ifilter calls filter(i,obj,...) in 1.0.7 (CommonLua/Core/types.lua:346) but filter(obj,...) in 1.1.0 (types.lua:363); a single-line grep of 1.1.0 found no caller still writing function(_, x) or function(i, x), multi-line callers not checked, so this is a (b′) lead for 03/04 (R07639 is an adapted caller). (2) RecursiveCallMethods.OnSetWorking = "call" is new in 1.1.0 (Buildings/Building.lua:3), absent from all of 1.0.7; it explains R06177/R05615, and no explicit X.OnSetWorking(self...) call remains in 1.1.0. (3) R08496 `#self.city.labels.RCTerraformer` is unguarded; LabelContainer:Init makes plain {} and only AddToLabel (RCTerraformer:GameInit) creates the label. The same unguarded # pattern ships since 1.0.7 at ConstructionSite.lua 110:3045 (AncientArtifactInterface), while BuriedWonder_Ancient_Artifact.generated.lua:85 treats a label as possibly nil; the engine-side base AddToLabel was not opened, so not filed as a smell. (4) R10651's caller table (27 same) is homonym Drone/rover ContinuousTask calls; the named params replace the old varargs in the same positions, so no caller shape moved. The double-scaling reading traces LandscapeConstructionSite.lua:421-423 (t = GetTimeToWork()/2) into RCTerraformer.lua:98; TopologyAI (Data/Tech.lua:10433) modifies the Drone const. (5) R08558's 3 'gone' callers are the ClearWasteRock sites switched to LandscapeForEachClearedObstructor. (6) R07642 judged from hunks only (LONG BODY, no --full). (7) R05568's tell-2 line (110:18) is a file-level local outside the span. (8) No span looked wrong. (9) Departure from rule 1, stated: I wrote the rowdump output to scratchpad\work_B02\dump.txt to read it in chunks; it is deleted after this file.
- **B03** (brief `a23585ff1d07`) — COUNTS: given 163, returned 163, WORTH-READING 129, CHURN 34, SMELL 12, unsure 0 — NOTES: No span was wrong. Six (b′) checks came back negative: no stale 1.1.0 caller of table.ifilter (dropped the leading index arg), ChooseDome (traits->object), PathLenCached, GetHeightAround, Flight_Free, or parent OnSetWorking calls (OnSetWorking is now RecursiveCallMethods "call"). The ifilter grep was single-line only. R05896's caller table is empty because the helper is passed as a callback. R07704's table lists homonyms (laws); its real new-shape caller is ConstructionController:Done at Construction.lua:888.
- **B04** (brief `7045ba3f0609`) — COUNTS: given 197, returned 197, WORTH-READING 170, CHURN 27, SMELL 10, unsure 0 — NOTES: (1) Engine dispatch change behind 10 rows (R05279 R06241 R06453 R06708 R06829 R06970 R07031 R07033 R07812 R07817): 1.0.7 Building.lua:8 `AutoResolveMethods.OnSetWorking = true` became 1.1.0 Building.lua:3 `RecursiveCallMethods.OnSetWorking = "call"`. Grep finds no explicit `X.OnSetWorking(self` left in 1.1.0 Lua, so vanilla has no double call. Any override that relied on NOT calling a parent now gets it anyway. Mods with explicit super-calls now double-call. (2) `table.ifilter` callback changed from `(i, obj, ...)` to `(obj, ...)` (CommonLua/Core/types.lua 342 -> 359); that is a (b′) source. Five 1.1.0 two-parameter callers (CargoTransporterNew.lua:200, ConstructionSite.lua:1446, StatusObject.lua:273, AnimMoment.lua:11, ClassDef-PresetDefs.generated.lua:1635) look value-first by their parameter names, but I did not read them. (3) Caller tables that misled: GoHome and DoesAcceptResource came back `{}` because their callers go through `SetCommand("GoHome", ...)` strings or method calls; the real GoHome callers are RCRover.lua:351/680. PickUp's only 'same' caller (ShuttleHub.lua:979) is a homonym, and the Service 'same' rows are other classes' Service methods. (4) R06511's dead table-exclude has an identical copy at MixedPoolStockpile.lua:262. The only text caller passing an exclude (ColonyControlCenter.lua:930) passes a string, so no live defect was found. (5) No span looked wrong. R10755 (INDENTED) was clean. R07808 (LONG BODY) has a single hunk.
- **B05.r2** (brief `332c34da488b`) — COUNTS: given 136, returned 136, WORTH-READING 119, CHURN 17, SMELL 13, unsure 0 — NOTES: No span was wrong and there were no over-spans. R06839's caller table is almost all homonyms (other classes' GetStoredAmount), so only StockpileController was judged. The text-level caller tables are empty for R10678, R10681, R05942 and R06847; a grep found no old-shape `(amount, bool)` AddResourceAmount call. The OnSetWorking super-call removals (R08601, R08597, R08609, R08605, R05939) all trace to 1.1.0 Building.lua:3 `RecursiveCallMethods.OnSetWorking = "call"`, which replaces 1.0.7 Building.lua:8 AutoResolveMethods. The table.ifilter callback contract changed from `(i, obj)` to `(obj)` (types.lua 346 -> 363), and no 1.1.0 caller still uses the old shape. Unresolved and not filed: MixedPoolStockpile has no Lua-visible `auto_rovers` default, yet RCTransport.lua:1043 compares `d.auto_rovers < rovers_needed` for auto-gather targets; StorageDepot shows no Lua default either, although 1.0.7 compared it the same way, so the default's source was not located. LeafResourceIds has an entry for every non-obsolete resource, leaves included (CommonLua Resources.lua:396), so LRManager's unguarded `ipairs(LeafResourceIds[res])` is safe except for obsolete ids. Research.lua:559 GetEstimatedRP_Outsource survives beside the new GetEstimatedRP_Outsourcing (754) and may be dead code; not checked further.
- **B05** (brief `fe124731e2a2`) — COUNTS: given 136, returned 136, WORTH-READING 121, CHURN 15, SMELL 11, unsure 0 — NOTES: (1) Callee contract change outside the batch: `table.ifilter` callbacks changed from `filter(i, obj, ...)` (1.0.7 types.lua:346) to `filter(obj, ...)` (1.1.0 types.lua:363). R09177 was updated, and single- and two-line greps found no stale index-first callers, but it is a (b′) surface for mods. `table.icount` kept (key, value). (2) `RecursiveCallMethods.OnSetWorking = "call"` is new in 1.1.0 (Building.lua:3), which explains the five removed super-calls (R08601, R08597, R08609, R08605, R05939); grep finds no explicit `X.OnSetWorking(self` left in 1.1.0 Lua. (3) Caller tables: the "same" rows for SetAcceptResource/SetAcceptResourceState/CreateResourceRequests/GetStoredAmount are mostly homonyms (Station, StorageDepot, rockets), not callers of the changed method. Old-shape callers checked and harmless: WasteRock.lua:553/557 (defaults resolve), Train.lua:1026 (13 args). (4) R09208: food warning moved to StarvingColonists (d). No replacement found for the maintenance-supply InsufficientResources warning; it is only migrated by the FixupObjectNotification at ResourceTracking.lua:316. (5) No span problems; no over-span or LONG BODY rows in this batch.
- **B06.r2** (brief `582ef826cd74`) — COUNTS: given 159, returned 159, WORTH-READING 146, CHURN 13, SMELL 10, unsure 0 — NOTES: CHURN was also used for identical-behaviour changes outside the enumerated reasons: upvalue→thread-arg (R07542 R07537 R09913), order-independent sorted_pairs→pairs (R09925 R09931 R09928 R09926), reordered short-circuit (R10311); reclassify if strict. Colonist.traits is now a hybrid array+map (AddTrait appends ids), which explains every pairs→ipairs flip. status_effects is now nil when empty: pairs(self.status_effects) is unguarded at Colonist.lua 1300/2166/3041/5158 and next() at 2295 — safe only if the engine's pairs/next accept nil; not verified. R09921 dump crashed on a cp1252 console (Cyrillic char); I reran it with PYTHONIOENCODING=utf-8. All spans looked correct; no over-spans seen.
- **B06** (brief `f11d8d0f9374`) — COUNTS: given 159, returned 159, WORTH-READING 144, CHURN 15, SMELL 9, unsure 0 — NOTES: (1) Two smells depend on engine semantics I did not verify: R10333/R10393 `#log` where the log is the class default `false` or nil'd by AddToLog, and R10383 `next(self.status_effects)` on nil. Both throw in stock Lua; the project's shims only cover pairs/ipairs-on-false. Needs a desk or keyboard check before filing. (2) The R09932 (b′) claim rests on LanderRocketCargoRequest (parent CargoRequest) and on ResupplyPassengers.generated.lua:16 still admitting it; I did not walk the lander UI route into ResupplyPassengers. (3) Caller tables: R07207 'gone' 3 and R10337 'gone' 3 re-grepped; no live caller passes the old shape. The sorted_pairs→pairs swaps (R09925-R09928) coincide with colonist.traits gaining a numeric array part; R09927 now writes numeric keys into approved_per_trait. (4) No span problems. R10365: only the text-level caller list was checked for other GetUIInfo users.
- **B07** (brief `02a34338a50e`) — COUNTS: given 156, returned 156, WORTH-READING 134, CHURN 22, SMELL 7, unsure 0 — NOTES: No spans were wrong and no caller table misled. Contract shifts seen across several rows that sibling batches should know: (1) `table.ifilter` callback lost its index arg (types.lua:363), and no 1.1.0 caller still uses the (i, obj) shape. (2) `IsInWalkingDist` now returns dist -1 for no foot route; R10478, R11627, R05822 and R05824 each handle it, other truthy-dist callers were not audited. (3) `connected_domes` is now an array (self first) plus a count hash. (4) `RecursiveCallMethods` now auto-calls BuildingUpdate, BuildingDailyUpdate and OnSetWorking (Building.lua:1-3), which is why the explicit base calls vanished tree-wide. (5) `pf.AddTunnel` has a new 4th arg, and TunnelMarker.lua:77 still uses the old form for table targets; I did not decide whether that is valid. (6) The DomeInPeril notification is gone from the whole tree. The R05856, R08890 and R08875 TraverseTunnel caller tables are empty because the engine calls them. R11633 callers marked 'same' now pass a second arg that the new signature consumes.
- **B08** (brief `7a551f79ee3d`) — COUNTS: given 228, returned 228, WORTH-READING 208, CHURN 20, SMELL 12, unsure 0 — NOTES: No span was wrong (R06036 DECL-ONLY is correct). The caller tables were incomplete in places: R07053 ValidateBuilding showed 4 of 19 changed callers, so I grepped (no 1.1.0 call passes a 2nd arg), and R07094 ToggleOvertime listed 2 callers, so I grepped (all UI/XDef/LawDef callers pass only broadcast). R05448 is a (b′): Lua/Buildings/CargoTransporter.lua:1463 (1.1.0) still calls GetAccessiblePrefabs with 2 args, so the old CargoTransporter skips the earth bypass and needs the PrefabRefab tech. Storage seam behind R05414/R05388: the four upgrade tables now default to `false` (Building.lua:281-290) and are created lazily in ApplyUpgrade. Not in this batch, but found while tracing it: RequiresMaintenance.lua:845-846 `local mods = bld.upgrade_modifiers and bld.upgrade_modifiers[upgrade_id]; if #mods == 0` takes `#` of a possibly nil value after HasUpgrade passes. OnSetWorking dispatch moved from AutoResolveMethods (1.0.7 Building.lua:8) to RecursiveCallMethods "call" (1.1.0 Building.lua:3); that is why R05419/R06020/R06030 dropped their explicit super calls, so those rows want one check that each parent still runs exactly once. Trait effects gone rather than moved: Introvert/Loner (R06481) has zero references in 1.1.0 Lua, and the StatsChange class (R06482/R06616) is gone. Extrovert moved to Colonist.lua:2472. R06197: the Rejuvenation comfort gain was removed while IsRejuvenationTreatment still makes medical buildings relaxation services. Unit changes: GetGrowthDuration/GetHarvestRemaining now return ms instead of Sols (R05994/R05996); both callers reformat, but the variable is still named remainingSols.
- **B09** (brief `6002418184af`) — COUNTS: given 205, returned 205, WORTH-READING 161, CHURN 44, SMELL 13, unsure 0 — NOTES: (1) Rule breach: rowdump stdout was too large to read, so I wrote it to scratchpad\B09_dump.txt to read it in chunks, then deleted it. (2) table.ifilter changed its callback shape: 1.0.7 types.lua:346 called filter(i, obj), 1.1.0 types.lua:362 calls filter(obj, ...). A grep found no 1.1.0 ifilter call with the old (_, x) shape. table.icount is C-side and its (_, x) callers are fine. The rows that only adapt to this are marked CHURN. (3) ChooseDome now takes the colonist (_GameUtils.lua:486). Every 1.1.0 caller passes an applicant or unit, including DroneFactory.lua:230, which passes a GenerateColonistData table of the same shape. (4) R06560 is unresolved and is the top pick. I found no GetStored_Fuel for expedition rockets in 1.1.0, yet customRocketExpedition.generated.lua:435 still reads Stored_Fuel (shown when HasExtraFuel). (5) R06561 is high value: non-black-market funding trade routes stopped debiting the rival AI. (6) R08922 is not a defect: 1.1.0 AddTrait adds an array part (Colonist.lua:493-494). Other trait writers were not checked. (7) Not opened: GetStarImage, GetPastureAnimalsInfo, GetSafariRouteCursorText/IsSafariRouteValid, HasAssignedMaintenanceDrone, RecreateResourceRequest, UpdateMaintenanceStuckNotification. Also not opened: the nil handling of CalculateRouteLength callers at SafariRouteInteractionHandler.lua:38/57. (8) The caller tables did not mislead. All spans looked right; R06767 DECL-ONLY is a comment-only change.
- **B10** (brief `77ceb3a7e656`) — COUNTS: given 209, returned 209, WORTH-READING 192, CHURN 17, SMELL 16, unsure 0 — NOTES: (1) CommonLua table.ifilter changed its callback contract from filter(i, obj, ...) to filter(obj, ...) (types.lua 1.0.7:346 vs 1.1.0:363). This is a tree-wide (b') surface outside this batch. My single-line regex found no unconverted (i/_, v) callback in 1.1.0 Src, but multi-line callbacks were not swept. (2) OnSetWorking became RecursiveCallMethods "call" (Building.lua:3); 1.0.7 had 22 explicit super-calls and 1.1.0 has 0, so R05315, R05914 and R06185 follow that mechanism change. (3) Caller tables misled on homonyms: R10859 and R10846 list customLanderRocket ToggleAutoMode(nil, "from_ui"), which resolves to the LanderRocketBase override. The switch_to_mode readers for R10869 belong to LanderRocketCargoRequest. (4) Nothing sets g_LaunchMode "elevator" in 1.1.0, but XDef templates (PGMissionPayloadRemastered, PGChallengePayloadRemastered, ResupplyPassengers, RocketRightTitlePart) still test it. These are dead checks outside this batch. (5) R07147: OnWaypointStartGoto has no caller left anywhere in 1.1.0 Src. (6) Every span was correct and no ONE-LINE or LONG BODY rows occurred. (7) Rule deviation: I also wrote one scratch file, the rowdump output at scratchpad\work10\dump.txt; no other files were written.
- **B11** (brief `31354ab6b033`) — COUNTS: given 175, returned 175, WORTH-READING 154, CHURN 21, SMELL 10, unsure 0 — NOTES: R08031 span over-runs in both trees (the closing ` end` is space-indented), so the listing includes the neighbouring function; judged only UpdateIndependenceProgress. R07215 is an INDENTED no_edit@ row whose span covers the rest of the StoryBit class def plus later functions (ChooseColor etc.); judged the whole listed region. R09882's caller table was empty; the real callers are DelayedCall sites TerraformingDisasters.lua:480 (passes "from_load") and :666. table.ifilter changed contract (callback receives value first, types.lua:363); grep found no 1.1.0 call site still passing function(_, x). R05385: the `(type(exclude)=="table" and not exclude[r] or r ~= exclude)` idiom, shared with siblings ResourceStockpile.lua:502 and MixedPoolStockpile.lua:262, falls through to `r ~= exclude` (true) when a table excludes r, so table-exclusion never excludes; this spans siblings outside this batch, so it is not counted as a row smell. R05255: the 1.0.7 FirstAsteroid callback granted 3 MicroG extractor prefabs; I did not find where 1.1.0 grants them (AutomaticMicroGExtractor.lua:17/25 is a fixup), so this is a candidate player loss for a link-03 trace.
- **B12** (brief `50191d178a39`) — COUNTS: given 216, returned 216, WORTH-READING 202, CHURN 14, SMELL 22, unsure 0 — NOTES: No span looked wrong. The only (b′) is R08311: RocketBase.lua:966 still calls CalcBaseExportFunding with no res_id, so that rocket export pays 0; is it still reached (exported_amount set at RocketBase.lua:795)? Caller tables: R08199's missed the LawVotingCard XDef callers; R08217's was truncated (4 of 9 shown); R08817 and R08835 mix homonyms (EULADialog, RocketBase/RocketExpedition). Contract changes to sweep outside my rows: table.ifilter now calls filter(obj) not filter(i, obj) (CommonLua/Core/types.lua:359), and a single-line grep found no old-shape callback; OnSetWorking moved from AutoResolveMethods to RecursiveCallMethods "call" (Building.lua:3), so an override still calling its super explicitly would double-call. I checked only R08772, R08794 and R08818. Most legacy Research methods are now stubs, but tech_status/tech_field are still read in TechTree.lua:1299/1456/1491, LandscapeConstructionSite.lua:92, Research.lua:343/431/486/540/901 and CheatStartMystery. OpenFirstLegislatureSessionPopup and AddExplorerResearchPoints have no caller in 1.1.0.
- **B13** (brief `419296a28556`) — COUNTS: given 65, returned 65, WORTH-READING 58, CHURN 7, SMELL 16, unsure 0 — NOTES: Rule 1 departure: I piped the rowdump output to a scratch file (scratchpad\b13_dump.txt) to read it in chunks, then deleted it; returns\B13.txt is the only remaining file. The 26 Scenario rows were read as LONG BODY hunks only (no --full); no span over-ran and none had caller tables (all rows are kind=body). Cross-row facts to route: (1) SA_WaitResearch "In Progress" is still in the dropdown but SAExec dropped the branch, and Mystery 5.generated.lua:375 still passes it (R09478/R09352). (2) SA_GrantResearchPts still declares Percent/Absolute but ignores both; every Research-set caller targets a tech with _N variants, so no live misroute found. (3) The old tech field ids (Engineering/Physics/Robotics/Social/ReconAndExpansion/Mysteries/BuriedWonders) are still defined in 1.1.0 TechFieldPreset.lua, so any unremapped Field silently boosts an empty field. (4) table.ifilter changed from filter(i,obj) to filter(obj) in CommonLua; my regex over 1.1.0 found no remaining `(_|i|idx|k|key, v)` callbacks, but other parameter names were not searched. (5) IsTechDiscovered and SetTechDiscovered are compat aliases of IsTechUnlocked/UnlockTech in 1.1.0 (Research.lua:94,140). (6) GetStored_WasteRock and CountDomeLabel still exist in 1.1.0, so those swaps are voluntary, not renames.
- **B14** (brief `04a768a32103`) — COUNTS: given 74, returned 74, WORTH-READING 62, CHURN 12, SMELL 13, unsure 0 — NOTES: (1) table.ifilter's callback contract changed from filter(i, obj, ...) (1.0.7 CommonLua/Core/types.lua:346) to filter(obj, ...) (1.1.0 types.lua:363). Rows R08013/R08014/R08634/R11692 are callers that adopted it. A single-line grep of 1.1.0 for `ifilter(... function(_,` found no caller still on the old shape; multi-line callbacks were not checked. (2) R09670's caller table (30 gone, 1 new) overstates the risk: the only live-text 1.1.0 caller, RivalColonies.lua:906, is inside a `--[[` comment, and nil player defaults to UIPlayer. (3) R11676 depends on whether the engine's `next` tolerates nil; not verified. (4) Laws smells (R08141/R08158) rest on LawDef:Deactivate/Activate asserting `not self.Obsolete` (1.1.0 LawDef.lua:49,67). (5) R11684/R11685 [MULTI]: the two OnMsg.LoadGame handlers swapped contents (MapUpdateMaxObjSurfRadius moved from #1 to #2), and UpdateTerrainStats now lives in a third handler at 1.1.0 _fixup.lua:1995. No span looked wrong.
- **B15** (brief `be45e828d13f`) — COUNTS: given 135, returned 135, WORTH-READING 115, CHURN 20, SMELL 16, unsure 0 — NOTES: No span problems; none of the rows needed --full. Callee contract changes found while reading rows that are not in B15: (1) table.ifilter now calls filter(obj, ...) instead of filter(i, obj, ...) (CommonLua/Core/types.lua 1.0.7:346 vs 1.1.0:363). A grep for `table.ifilter(..., function(_,` in 1.1.0 found 0 hits, but predicates with a named index parameter were not enumerated, so this is a (b′) candidate. (2) GetEnvironment changed from obj:GetMapSlot()->g_MapSlotEnvironments to ResolveMap(map).mapdata:GetEnvironment() (MapData.lua 1.0.7:60 vs 1.1.0:86); the ResolveMap docs say it accepts objects. (3) The XCreateRolloverWindow and CreateMarsRenameControl signatures are the same in both trees, so the 1.0.7 3-argument rollover calls and the SaveLoad options slot were caller-side bugs that 1.1.0 fixed. (4) BuildMenuPrerequisiteOverrides is a GameVar; 1.1.0 nil-guards it at BuildMenu.lua:336 while 12 other reads stay unguarded. The guard claims the value can be nil before a game exists, so the reach of those unguarded reads is worth deriving (EF-005 sibling count). Caller tables: R10983's `same` caller (BuildMenu.lua:826) and R10987's three `same` callers are benign because the new parameters are trailing and defaulted. R10186's table omits Cheats.lua:277, which also passes AsyncRand(). 20 CHURN rows are the systematic change from thread-closure upvalues to explicit thread arguments, apparently for thread persistence.
- **B16** (brief `3a7cba479fa9`) — COUNTS: given 146, returned 146, WORTH-READING 129, CHURN 17, SMELL 25, unsure 0 — NOTES: (1) R11026: 1.1.0 dropped `or empty_table`, so a filter that is off (the default: drone_hubs on, the rest nil) passes nil/false to `#tbl`. UICity.labels is a plain `{}` (LabelContainer.lua:11). BUT R00023's `#self.behaviors` on the class default `behaviors = false` (ActionFX.lua:952) runs on every tracked FX, which suggests the engine tolerates `#nil`/`#false` like its known ipairs shim. That tolerance is NOT verified; settle it before calling R11026 a crash. (2) R00021: the caller table's 4 `same` rows are real (b′) sites: ActionFX.lua:2052, 2821, 3967 and _fixup.lua:1335. All sit in classes whose SourceItems include "ActionObj". (3) R00066 (INDENTED items@04c38a) spans many functions from the CameraShake class through ActionFXObjectAnimationHelp; I judged the whole span. R00055 is MULTI (#1) and I judged that body only. (4) R11166: the new `alt` contract is honoured by DroneControl, OrbitalProbe, UniversalRocketBase, RCRover and PinnableObject, but not by RocketBase.lua:1478 or RocketExpedition.lua:1021. (5) XCreateRolloverWindow has had `(control, gamepad, immediate, context)` in both trees, so the 1.0.7 HexMenuButton and ItemsMenu calls misplaced context; 1.1.0 fixes HexMenuButton and passes a boolean in ItemsMenu. (6) table.ifilter's predicate lost its index argument (R11090, R00014, R00071). A single-line grep of 1.1.0 for `table.ifilter(... function(_/i/idx/k, ...` found no leftover old-shape predicates; multi-line predicates were not swept. (7) R11012 caller table showed only gone/new, no `same`; individual callers were not opened.
- **B17** (brief `1c5b74be759e`) — COUNTS: given 204, returned 204, WORTH-READING 183, CHURN 21, SMELL 14, unsure 0 — NOTES: Spans: R00278, R00323, R01067 are INDENTED spans covering whole class blocks; only the changed lines were judged, and R00278 repeats R00275's change. R00531's span ends at the inner if's end (110:1545); the real function end is 110:1546. Caller tables: R00256/R00257 list 144/26 "same" XPropControl and editor homonyms, but the real dispatcher TerminalTarget passes (pt, button) in both trees (terminal.lua 244/252), so 1.0.7 was the broken side. R00520's 222 "same" callers are other classes' Send. R00140's arg-less callers are ScriptConditionDef/ScriptEffectDef test_obj homonyms. R00392 looks like a nil-instance crash but is not: CreateInstance is DefineCombinedMethod "modify" (PropertyObject.lua:1470). table.ifilter's contract changed to a value-only callback plus extra args (types.lua:359); four 1.1.0 two-param callbacks remain (CargoTransporterNew.lua:200, AnimMoment.lua:11, ClassDef-PresetDefs.generated.lua:1635, StatusObject.lua:273), each passing the second value as an extra ifilter argument, so they are correct. R01023's (b′) rests on Lua table_add (types.lua:860-874) being the live table.add; if an engine table.add exists first (table.add = table.add or table_add), its semantics are unverified. R00347 dropped string method names; no string-func callers remain in 1.1.0.
- **B18** (brief `42187c0421c7`) — COUNTS: given 133, returned 133, WORTH-READING 119, CHURN 14, SMELL 21, unsure 0 — NOTES: R01413 span is wrong in 1.0.7 (518-1335 swallows ~40 EntitySpec methods; 1.1.0 486-652); judged only the property table. R01213 and R01215 print the same body (Autorun wraps the nested DoneMapObjects). R01261 caller table empty, correct. R01290 caller table flags 7 'changed' calls that are only other MapVar lines (moved or renamed). Callee smell outside the batch: EarlyClassDescendantsListInclusive (classes.lua:1300-1301) guards `classdefs` instead of `classdef`, so it cannot fire; its name says descendants but it walks parents. `config.MapLoadingHookInterval` (R01339) is set nowhere in Lua but compared with `> 0`. PlaceAndInitPromotedCObjects (R01220) is filled outside Lua in both trees, so the set->array switch cannot be traced in Lua.
- **B19** (brief `409cb221e9b4`) — COUNTS: given 144, returned 144, WORTH-READING 120, CHURN 24, SMELL 18, unsure 0 — NOTES: No span was wrong. Long bodies (R01731, R01771, R01782, R01783, R01786, R01788, R01794, R01795) were read as changed hunks with context; every changed line was seen. XEditorUndo lazy capture (R01469, R01470, R01462) is dormant: lazy_obj_data is only the class default false anywhere in 1.1.0, so the map-patch path cannot serialize lazy stubs today, but would if the flag were ever enabled (CaptureLazyData runs only on Undo). The table.ifilter callback contract (filter(i,obj) to filter(obj)) was migrated tree-wide: about 70 old-shape callers in 1.0.7, 0 in 1.1.0, so there is no b-prime for R01489. The R01540 caller table lists FXSource.lua:592 still passing "game_state_changed" as `same`; it is truthy and harmless. The R01523 FXSourceStates layout seam rests on it being a MapVar in both trees with no fixup; I did not check whether SMR saves actually carry FXSource objects. The LockablePreset storage move is migrated by a fixup body at LockablePreset.lua:785; I did not trace when that runs. Player inherits LockablePresetOwner (Player.lua:10). The R01623 caller table shows Research.lua:9 passing player plus a dropped notify. Unverified engine facts: whether next(nil) raises (R01465, R01629, R01785, R01790), create-on-nil for the C-side table.set (R01549), and InterpolateRGB's hsv_space flag (R01473).
- **B20** (brief `08936b3004d7`) — COUNTS: given 137, returned 137, WORTH-READING 123, CHURN 14, SMELL 24, unsure 0 — NOTES: (1) Outside-batch contract change: `table.ifilter` predicate went from `filter(i, obj, ...)` (1.0.7 types.lua:346) to `filter(obj, ...)` (1.1.0 types.lua:363); any 1.1.0 caller still written as `function(i, obj)` is a (b′). A single-line grep found none, but multi-line lambdas and game Lua/ were not exhaustively checked. (2) R01949 `#only_item`/`#items` on false/nil assumes stock Lua `#`; the engine tolerates ipairs(false), and its `#` semantics were not verified. (3) Label getters: only the first 60 of the LabelCount/GetFirst/GetRandom callers were sampled, all map=nil; map-passing callers are unchecked. (4) LONG BODY rows R01915/R01917/R02043 were judged from hunks only, and no span looked wrong. (5) Caller tables: R01832's SA_Filters/UniversalRocket rows are homonyms; R01953/R01954 show no text caller because they are invoked by Op name.
- **B21** (brief `1d093f9486c1`) — COUNTS: given 117, returned 117, WORTH-READING 76, CHURN 41, SMELL 26, unsure 1 — NOTES: R02189 span is wrong. The INDENTED one-line no_edit over-spans the SIE_ImportItemSelector property table and runs into the GetParentCollider/GetError method; the own function is identical, so it is returned unsure. R02171 is a param rename only (errList to err_list), and its caller-table rows are base-class and other-class homonyms. R02130's self:ResolveSelectors caller rows are a method homonym, not the local function. Not a row but seen here: MapGen:ApplyPass calls ResumePartialPassEdits("MapGen") twice (MapGen.lua:1160-1161) against one Suspend in RunInit. Engine contract moves in this batch were checked only for Lua call-site completeness, not semantics: GetResource(id, true), GetWaterHeight(obj), pf.ForEachEntrance/ForEachTunnel exit_map_slot, SceneDesc.ExportAnimation. table.ifilter's callback moved from (idx, item) to (item, ...), with no stale (_, v) callers in 1.1.0. table.create_add/create_set are gone; create_add_unique is still defined. The R02138 caller GedGameObjectEditor.lua:370-371 is itself new in 1.1.0. Almost all rows are DevTools/MapGen editor code.
- **B22** (brief `334e1b2a6c39`) — COUNTS: given 176, returned 176, WORTH-READING 151, CHURN 25, SMELL 16, unsure 0 — NOTES: (1) No row span was wrong; the INDENTED/MULTI class-body spans (R02283, R02394, R02426, R02447, R03093, R03091) were judged whole. (2) Caller tables misled on R02429 (every hit is a homonym Done or a string) and R03231 (the Sounds/SurfaceDeposit Refresh hits are homonyms); I disregarded both. (3) No (b′) found. The contracts that moved in this batch were checked against every 1.1.0 caller. table.ifilter's callback went from (i, v) to (v, ...) in Core/types.lua:359, and no inline old-shape callback remains (the named filters in CargoTransporterNew are one-argument). TraverseTunnel gained end_point_map before param, and all 5 overrides and callers use the new arity. GetClassPropMeta and GetPropPresetClass went from a class name to a class object, and their 2+2 callers are updated. (4) table.create_add and table.create_set have no definition in 1.1.0 CommonLua. Their replacements table.add and table.set (types.lua:855/874) were verified to have the same create-if-nil semantics. Mods that still call the old names would break (no row covers this). (5) R02399: RevalidateDelivery has no Lua definition in either tree, so the change from res to res_set is probably inert in SM. (6) Several 1.1.0 bodies read `#x` right after `x and x[k]` (the four CallReactions variants, CycleItems, and AddNotification's `#parent.objects` on a parent just created with nil objects, R02290 @ 110:76). None is flagged, because each relies on the engine returning 0 for `#nil`, which I did not verify. If it does not, R02290 throws when a child removes itself in OnInit. (7) R02411: the base CreateInstance dispatch that now hands in `instance` was not traced. (8) Outside this batch's rows, ParadoxModManager.lua in 1.1.0 has two suspect functions: line 221 GetAuthorThirdPartyAccountLink reads an undefined global `mod_details`, and line 384 AsyncResolveThirdPartyAccountLink uses `self` in a function that is not a method. (9) R02349/R02350/R02351 are counted CHURN as styling-only XTemplate constants. R02301 is counted WORTH-READING although it only adds a dev assert.
- **B23** (brief `dd80f76eecec`) — COUNTS: given 142, returned 142, WORTH-READING 125, CHURN 17, SMELL 17, unsure 0 — NOTES: (1) Spans wrong: R03254 and R03310 are one-line INDENTED field functions whose spans over-run about 230 and 551 lines; their diffs belong to R03244 and R03308, and I returned them as CHURN for the row's own unchanged function. (2) Out-of-batch (b′) root: 1.1.0 table.ifilter (CommonLua/Core/types.lua:359) now calls filter(obj, ...) instead of filter(i, obj, ...). A grep of 1.1.0 found no in-tree callback still written as (i/idx/_/k, obj), but every mod callback in the old shape now gets obj as its first argument; five rows here are only callers adapted to the new shape. (3) Removed/renamed helpers: table.create_set and table.create_add are gone in 1.1.0 (replaced by the native table.set/table.add); the global CanBeSetpieceActor was removed. (4) The resource-group task-request rows (R03345, R03344, R03346) are the strongest old×new seam in this batch; the RemoveBuilding/_InternalRemoveRequest nil-request guard is self-contradictory. (5) The R03329 caller table: 17 "same" one-arg callers now silently get the narrower default path; I judged this intended, so it is class (b), not (b′). (6) The R03399 caller table is 252 OnShortcut homonyms; signature varargs are preserved.
- **B24** (brief `653ead9df253`) — COUNTS: given 144, returned 144, WORTH-READING 137, CHURN 7, SMELL 20, unsure 0 — NOTES: (1) table.ifilter's callback contract changed between trees: filter(i, obj) in 1.0.7 types.lua:346, filter(obj, ...) in 1.1.0 types.lua:363. The row edits R03524 and R08995 are migrations to it. Of the 84 ifilter call sites in 1.1.0, none keeps (i, obj); the five 2-parameter callbacks take the extra `...` arg. (2) R08616 caller table: Lua/X/Infobar.lua:582 calls GetEnvironment(city) and is reached from :661 with UICity. Lua/City.lua defines no GetMap or GetMapSlot in either tree, so it is untraced whether ResolveMap resolves a City. If it does not, ShouldShowDiscoveredDeposits is always false. This is a (b′) candidate for 03/04. (3) Leftover of the g_CurrentMissionParams move (R08998 and Telemetry rows): Lua/GameRules.lua:167 still reads `g_CurrentMissionParams and g_CurrentMissionParams.idGameRules`, and that global is now only ever false. The read is not in this batch; listed for 03. (4) R03541's loss of EditorCustomActions depends on the PresetOnMap/Preset method resolution, which I did not open. (5) No span looked wrong. The CALLERS table for R03524 mixes in ged:SetSelection homonyms from other classes; I did not use them.

## §4 · NOT reached by triage

- **`SPAN-SUSPECT` hand `body`/`body+sig`/`sig` rows — 79, NOT batched** (their body verdict is unreliable, §0.6; checklist 135): `R00206` AutoAttach.lua:OnMsg.GameEnterEditor, `R00207` AutoAttach.lua:OnMsg.GameExitEditor, `R00231` AutoAttach.lua:TransformGizmo.EditorCallbackMove, `R00232` AutoAttach.lua:TransformGizmo.EditorCallbackRotate, `R00233` AutoAttach.lua:TransformGizmo.EditorCallbackScale, `R00360` Common.lua:is_deposition_not_editable, `R00361` Common.lua:is_terrain_chuck_deposition, `R00367` Components.lua:NoCollider, `R00576` Lightmodel.lua:custom_sun_ro, `R00577` Lightmodel.lua:shadow_range_ro, `R00579` Lightmodel.lua:tod_ro, `R01282` lib.lua:DebugPrintNL, `R01293` lib.lua:OutputDebugStringNL, `R01352` options.lua:ApplyProjectAccountOptions, `R01410` ArtSpecEditor.lua:editor_artset_no_edit, `R01411` ArtSpecEditor.lua:editor_category_no_edit, `R01412` ArtSpecEditor.lua:editor_subcategory_no_edit, `R01742` Ged.lua:OnMsg.Autorun#2, `R01743` Ged.lua:OnMsg.ChangeMap, `R01744` Ged.lua:OnMsg.ChangeMapDone, `R01745` Ged.lua:OnMsg.DataReload, `R01746` Ged.lua:OnMsg.DataReloadDone, `R01747` Ged.lua:OnMsg.DebuggerBreak, `R01748` Ged.lua:OnMsg.DebuggerContinue, `R01751` Ged.lua:OnMsg.LuaFileChanged, `R01754` Ged.lua:OnMsg.PreSaveMap, `R01755` Ged.lua:OnMsg.SaveMapDone, `R01756` Ged.lua:OnMsg.ValidatingPresets, `R01757` Ged.lua:OnMsg.ValidatingPresetsDone, `R02233` GridOps.lua:GridOpParam.SetB, `R02234` GridOps.lua:GridOpParam.SetG, `R02235` GridOps.lua:GridOpParam.SetR, `R02257` MapGen.lua:no_flow, `R02258` MapGen.lua:no_noise, `R02534` GameObject.lua:object.GetLocalPoint#1, `R02535` GameObject.lua:object.GetLocalPoint#2, `R02536` GameObject.lua:object.GetLocalPointXYZ#1, `R02537` GameObject.lua:object.GetLocalPointXYZ#2, `R02539` GameObject.lua:object.GetRelativePoint#1, `R02540` GameObject.lua:object.GetRelativePoint#2, `R02541` GameObject.lua:object.GetRelativePointXYZ#1, `R02542` GameObject.lua:object.GetRelativePointXYZ#2, `R02577` collision.lua:collision.Collide, `R02578` point.lua:ResolvePos#1, `R02579` point.lua:ResolvePos#2, `R02580` point.lua:ResolvePosXYZ#1, `R02581` point.lua:ResolvePosXYZ#2, `R02582` point.lua:ResolveVisualPos#1, `R02583` point.lua:ResolveVisualPos#2, `R02584` point.lua:ResolveVisualPosXYZ#1, `R02585` point.lua:ResolveVisualPosXYZ#2, `R05507` BuildingComponents.lua:SingleResourceProducer.CheatEmpty, `R05512` BuildingComponents.lua:SingleResourceProducer.GetAmountStored, `R05520` BuildingComponents.lua:SingleResourceProducer.IsStorageFull, `R05581` Community.lua:Community.GetAverageComfort, `R05582` Community.lua:Community.GetAverageHealth, `R05583` Community.lua:Community.GetAverageMorale, `R05584` Community.lua:Community.GetAverageSanity, `R05744` Dome.lua:Dome.GetColonistCount, `R05867` DroneControl.lua:DroneControl.GetBrokenDronesCount, `R05870` DroneControl.lua:DroneControl.GetDronesCount, `R05880` DroneControl.lua:DroneControl.GetMiningDronesCount, `R07559` Colony.lua:OnMsg.PostLoadGame, `R07731` Decor.lua:DecimateObjects, `R07732` Decor.lua:DecimateParticles, `R08317` GameOverlays.lua:CycleElectricityOverlay, `R08321` GameOverlays.lua:CycleWaterOverlay, `R08901` Passage.lua:ret_false, `R09163` ResourceOverview.lua:ResourceOverview.GetAverageComfort, `R09164` ResourceOverview.lua:ResourceOverview.GetAverageHealth, `R09165` ResourceOverview.lua:ResourceOverview.GetAverageMorale, `R09166` ResourceOverview.lua:ResourceOverview.GetAverageSanity, `R09642` SupplyGrid.lua:SupplyGridElement.GetProductionEstimate, `R09643` SupplyGrid.lua:SupplyGridElement.GetStoragePercent, `R09646` SupplyGrid.lua:SupplyGridFragment.GetCurrentConsumption, `R09647` SupplyGrid.lua:SupplyGridFragment.GetCurrentProduction, `R09648` SupplyGrid.lua:SupplyGridFragment.GetCurrentReserve, `R09649` SupplyGrid.lua:SupplyGridFragment.GetCurrentStorage, `R11634` _GameUtils.lua:TFormat.FormatDuration. They keep their system/link; the owning link reads them as one-line functions.
- **`other` rows left unplaced: 0**; NOROWS files unplaced: 0 (1.4 places all 289 files by hand).
- **`FPK-DIVERGENT` rows: 0** — none exist (`EF-085`).
- **Preset churn-classed rows — 10485, UNREAD here:** `REINDEX` 10462 · `T-ID` 22 · `COMMENT` 1 (rule-classed and sampled by 01, §0.10).
- **Not fanned out, classed by kind only (`*`):** every `added`/`removed` row and every `generated` row — their links read them (04-D the whole-file ones; 04-E the generated twins with their presets).
- **Agent `unsure` rows — 1:** listed per link in §3.
- **CALLERS `unsure` — 2**, listed in 1.5.
- **Fan-out rows with NO verdict — 0.**
- ⛔ **Every `CHURN` row (473) is UNREAD by anyone but the one agent that labelled it** — the self-sample (§2) is the only second read, and it is a sample.
- The chain blind spots (README "What this hunt CANNOT see") are inherited unchanged; the seeds' hit rate says nothing about `generated` rows or `DLC/`.



## §03 coverage — core food seam close-out, 2026-09-10

MEASURED: original 03 =1,289 INVENTORY (929 hand/360 generated),1,618 PRESETS,
30 CALLERS,18 NOROWS. Complete present-span reads:396 hand rows; six full
caller/contract checks. All remaining items have disjoint owners in
`SEAM_COVERAGE.tsv`:03b360 generated + 1,618 presets + 6 callers;
03c284 hand + 2 callers;03d249 hand + 16 callers + 18NOROWS. Four03d callers are
line-checked only, still pending. No tagged input was changed. The ~400-row
stop was taken;396 is not clearance of the entire DLC-adjacent set.

`SEAM_REPORT.md` is the parent's synthesis with read-group verdicts, both-tree
routes/counterevidence, incidental-vs-complete limits, native gaps, FR subsections,
all caught drift and control scores. `tools/seam_coverage.py` reproduces the
2,955-item snapshot from original row keys and declared file groups; it does
not infer reading. Later links retain this receipt and append their own.

Filed C56-C62: ranch quantization/forecast, disabled ingredient consumption,
reserved-food spoilage, bounded next-crop slot error (PASSING), unused ranch
panel allocation (PERF), stale death-penalty popup, discarded explosion list
(PASSING). All cand/source-read; no module or game changes. C56/C57/C59 have
executing desk controls in `tools/desk_seam_food.py` / `SEAM_DESK.txt`; native
and runtime outcomes remain unobserved. Runtime riders are in the owner checklist.

Reader control:0 eligible seeded positives; random six-row parent sample agrees
6/6 on actual changes,5/6 on initial route precision. GetCropName's generic UI
route was narrowed to no literal caller. Two initially truncated Building spans
were fully reread before completion. Overlapping/one-line spans are rows, not
distinct functions. See report for the random seed, keys and detailed controls.

### FR-1(b)

Read3 of10 FR-1 rows: R05598,R07542,R07544. Base underfed/colony/funding code
does not require DLC; non-owner execution remains in scope. Seven pending rows
are explicit in 03c/03d. No new-game/native crash conclusion;04 owns the temporal
upscaler lead. A zero count of explicitly DLC-guarded FR-1 rows is not clearance
of the changed base paths. See `SEAM_REPORT.md` FR-1(b).

### FR-2 and FR-3

FR-2:0/7 read here;03c has4,03d3,03b relevant tech fields. FR-3:11/21 tagged
rows read; C60's dead allocation has a profiling falsifier. Other periodic-work
shapes and unchanged cadences are listed in SEAM_REPORT; none measures frame time
or establishes the original 2025 stutter cause. No field report is closed.

### For dlccheck

The full per-seam contract is `SEAM_REPORT.md` → For dlccheck and its five
read-group sections: services/ingredients, recipes/input reservations, crops and
producer hooks, FungalFarm/insect names, ranch output/panel, spoilage, colonist/dome
assignment, Building fixups/UpgradeUnlocks and death/applicant behavior. Use the
base citations and limits; do not redo them as if unseen or extend them to
uninspected DLC overrides. Remaining research/law/policy/cargo and preset seams
are TAKEABLE WHEN 03b/03c/03d finish their rows, before 99's DLC kickoff.

TAKEABLE WHEN DLC deep-check opens the named actual definitions/callers:
recipe input debit versus reserved portions needs a concrete recipe + template+
colonist pile route; crop augmentation needs an instantiated effect; ingredient
toggle and meal behavior needs actual registration/overrides; specialized dining,
AssignMeals and death handlers require their DLC bodies. No ordinary base recipe
processor was established simply from the existence of its class. No broad
claim about DLC being mostly additive was made.

Guard re-derivation: base Lua3 norman/1 thomas, base Lua + Data10/1. Exact files/lines
in SEAM_REPORT; brief's3/1 used a narrower scope. Names in 12 files is an inherited
count, not a reproducible dependency test. Base FungalFarm exists; missing
FarmInsect/PanoramicRestaurant classes are guarded in Building's fixup; upgrade
literal keys are not preset dereferences. The food chaser's broader-than-allowed
DLC definition/excerpt lookup is disclosed as scope drift, not DLC clearance.

99 waits for 03b/03c/03d/04 and any declared children. Blind spots unchanged:
assets absent from Src, native/timing/console behavior, actual execution,
incomplete old DLC, anonymous/dynamic callers and C-consumed presets.
