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

### 0.13 · ⭐ v1.1 re-emission (2026-09-10, the authoring session `smr-bugfixpack-c3`, AFTER 01 closed) — hole 0.11.1 MEASURED, then CLOSED for the orphans

The owner asked whether the "4,883 indented declarations covered by neither
instrument" could be repaired rather than only passed on. Measured first, on
the 1.1.0 side of the changed + added `hand` files:

| indented declarations | count | status |
|---|---|---|
| total (`INDENTED` regex, as 0.11.1 counted) | 4,142 | — |
| INSIDE an enumerated indent-0 span | 2,033 | were ALWAYS covered — the outer body's hash includes them; 0.11.1 over-stated the hole by this much |
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
