# 01 — the inventory: one instrument, its falsifier, and the raw rows

⛔ ONE-SHOT: this file `git rm`s itself on close-out (README rule 2).
Model: Opus · owner needed: no · **strictly first** — 02 reads your TSVs.

> 🎯 You build the two-tree function differ and emit the raw inventory. **You do
> not hunt.** Every row you read beyond what the falsifier needs is context the
> hunt links were sized to spend, not you. ⛔ One tool, one author, in THIS
> session — do not fan the instrument out (README §4).

## 0 · Open in this order

```
git log --oneline -10 · git pull · ListAgents
```
Read `README.md` (binding), `docs/agent/STATE.md`, `tools/luafn.py` whole,
`tools/bodycheck.py` lines 1–120 (how a body is hashed) and its `--selftest`
(the falsifier discipline to copy), `tools/sigcheck.py` lines 1–60 (how it reads
a parameter list), `tools/flpk_extract.py` header, `WORKFLOW.md` "fpk
verification", `C:\Dev\SMR-SrcArchive\README.md`, your `## Notes from upstream`.

**Pin check (README §0):** read `A:\SteamLibrary\steamapps\appmanifest_3215050.acf`
`buildid`. `24995074` ⇒ proceed. Anything else ⇒ archive the new tree per the
archive README, then **STOP AND ASK** — the diff base is a chain decision.

## 1 · 🗒 Live todo list, from your first action

One item per unit below; expand the moment a unit turns out to be several.

## 2 · Units

### A · fpk parity on 1.1.0 — does the game execute the Src we read?

The 1.0.7 proof (2,250/2,256 byte-identical) does not transfer. Extract
`…\Project Spark\Packs\Lua.fpk` with `tools/flpk_extract.py` **into your
scratchpad** (⛔ never into the install, never into the archive), and diff
against the ARCHIVED 1.1.0 `Src` by sha256 per file. Report: files in the fpk,
files matched, byte-identical count, divergent list BY NAME, files only in one
side. Record the result as a fact (`facts/EF-###.md`, `split_facts` route) —
it bounds every citation the chain makes. ⚠️ If a gameplay file diverges, that
file's rows in the inventory carry a `FPK-DIVERGENT` flag and the hunt reads
the EXTRACTED body for it, not Src. ⚠️ If `Data.fpk` exists and extracts,
repeat for `Data/` — link 03 needs the same bound.

### B · `tools/treediff.py` — the differ

Given two `Src` roots, emit one row per top-level function that is
**added / removed / body-changed / signature-changed**, keyed by
`file:function`. Requirements, each of which the falsifier must exercise:

1. ⛔ **Import `luafn.find_bodies` and `luafn.read_lines`. Never re-implement
   the delimiter.** Enumerate declaration lines with your own regex (`function
   X`, `local function X`, `X = function(`, `X.Y = function(`, `X:Y`), then get
   each body span by calling `find_bodies(lines, "^" + re.escape(line) + "$")`
   on the declaration's own line — the span rule stays luafn's. Where the
   escaped line matches more than once in a file, key the duplicates by ordinal
   (`file:function#2`) and flag `MULTI`.
2. **Normalise exactly as `bodycheck.py` does before hashing** — `\r\n`→`\n`,
   trailing whitespace stripped per line, leading indentation and comments
   KEPT. A whitespace-only diff must NOT be a row. State in the banner that
   comments count (a changed comment in a shipped body is a signal).
3. **Signature** = the parameter list text between the declaration's
   parentheses, whitespace-normalised. `signature-changed` when it differs;
   `body-changed` when the hash differs and the signature does not; a row can
   be both. Read `sigcheck.py`'s parameter reader first and reuse its rule if
   it is importable; otherwise say why not in the header.
4. ⚠️ **The one-line-function trap — MEASURE it, do not assume it.** As read
   at authoring (SOURCE, not run): `find_bodies` scans FORWARD from the
   declaration for a bare `end` at the same indent without checking whether
   the declaration line itself closes the function, so `function f() return 1
   end` would span to the NEXT same-indent `end`. If the run confirms it, mark
   such rows `SPAN-SUSPECT` and count them; ⛔ do not "fix" `luafn.py` in this
   link — a delimiter change re-hashes every `SRC:` pin in `Code/` and that is
   a hotfix-3 decision, filed to the checklist as TAKEABLE WHEN the owner rules.
   The same count is the inventory's stated imprecision.
5. **Rename candidates (class (d) hint):** an added function whose normalised
   body hash equals a removed function's, or whose body is ≥ 90 % identical by
   line set, gets `RENAME?` with the partner named. A hint, never a verdict.
6. **Buckets, as a column, never as a filter:** `generated` (`Data/`,
   `Lua/BuildingTemplate/`, `Lua/XDef/`, `Lua/ClassDefs/`) — rows still emitted
   but link 03 owns them; `dlc` (`DLC/`) — ⛔ excluded from the base diff
   entirely (README blind spot 5); everything else `hand`. ⛔ Do NOT add a
   "tooling" bucket by path — 04's engine agent decides that by route.
7. **`--selftest` — the falsifier, mandatory, and it must fail first.** Build
   two tiny trees in a temp dir from fixtures and assert the tool reports:
   a planted body change (name+arity same); a planted leading parameter
   (`F115`'s shape); a planted removal; a planted addition; a planted rename
   with identical body (`RENAME?`); a CRLF + trailing-space-only change
   (**must NOT be a row**); a changed comment (**must be a row**); a one-line
   function followed by another function (documents whatever the delimiter
   does — the test pins the behaviour so a future change is visible); and a
   duplicate declaration (`MULTI`). ⭐ Then the real-tree control: the four
   seeded positives in README §4 must come out as `Train:UnloadAll`
   body-changed, `LandscapeForEachUnit` signature-changed `(mark, callback,
   ...)`→`(map, mark, callback, ...)`, `TrackGridElement:DemolishAndSplitTrack`
   body-changed, `ChooseDome` signature-changed. Print each. ⛔ An instrument
   you never watched fail is not an instrument: make one assertion wrong on
   purpose, see RED, put it back, say so in the commit.
8. **Banner line 1** on every TSV: tool + version, both tree digests (from the
   manifests), the command line, the date. Deterministic output (sorted).

⛔ Do not wire `treediff --selftest` into `doccheck.py`; this is a one-effort
instrument and doccheck already carries `bodycheck --selftest`. 99 re-runs it.

### B2 · `tools/presetdiff.py` — the second instrument, same author, same discipline

The 1630 generated files are `PlaceObj('Class', { key = value, … })` blocks —
Lua-form preset data the function differ reads as noise. Parse every block in
both trees' `generated` bucket into `(file, class, id, key) → value-text`,
nested tables flattened with a path (`key.sub[3].leaf`). Emit `PRESETS.tsv`:
one row per key whose value differs, plus `added-preset` / `removed-preset`
rows keyed by `class:id`. Columns: `file · class · id · key · value107 ·
value110 · churn-class`. **Churn classes are RULES the tool applies**, one
column: `T-ID` (a `T(123, "text")` localisation-id change with identical
text), `REORDER` (keys reordered, values equal — ⛔ must NOT be a row at all),
`FORMAT` (number formatting, quote style), `SAVE-ID` (editor-generated ids,
`save_in`), `COMMENT`, or `none` (the readable pile). `--selftest` on
fixtures: a changed numeric value; a changed string; a key added; a key
removed; a preset added; a preset removed; a reorder-only preset (no row); a
nested element change; a `T-ID` change with the same text (`T-ID`) and with a
changed text (`none`). Break one assertion on purpose, see RED, restore, say so.
⭐ **Then falsify the rules on the real trees:** 20 random rows per churn
class READ BY YOU against both files — a single row where the rule hid a value
change voids that class (it becomes `none`) and the miss is recorded. Report
per class: rows, sample, misses. Both `Data/` and its generated Lua twins
(`Lua/BuildingTemplate`, `Lua/XDef`) are parsed; the banner states the twin
row count so 04's registry agents can confirm the twins carry nothing extra.

### C · the five TSVs (README §6)

- `PRESETS.tsv` — from B2, as specified there.

- `INVENTORY.tsv` — columns: `file · function · kind(added|removed|body|sig|body+sig) · bucket · line107 · line110 · sig107 · sig110 · flags(MULTI,SPAN-SUSPECT,RENAME?<partner>,FPK-DIVERGENT)`. Identical functions COUNTED in the banner, not listed.
- `STORAGE.tsv` — every `GlobalVar(`, `MapVar(`, `GameVar(`, `PersistableGlobals`, `const.<X> =` / `g_Consts` declaration line in both trees, with `same / moved-file / added / removed / kind-changed` — class (c)'s raw material.
- `FILES.tsv` — the 305 added and 36 removed files, bucket, and for a removed file the count of its declared names that still appear ANYWHERE in the 1.1.0 tree (the presence side, mechanically — a nonzero count says "moved", not "gone").
- `CALLERS.tsv` — ⭐ **class (b′)'s instrument.** For every `sig`/`body+sig` row in a `hand` file: every call site of that name in BOTH trees (`Name(` and `:Name(`/`.Name(` for methods, by text), with the call line's hash `same / changed / new / gone`. ⛔ A `same` call line against a changed signature is the F117 shape and is the single highest-yield row class in this chain — say so in the banner. Text-level; dynamic dispatch is outside it (README blind spot 7).

### D · counts + the mechanical classes

In `TRIAGE.md`'s **§0 (you create the file; 02 owns the rest)**: rows per kind
× bucket; the manifest re-derivation (2444/1968/305/36 — must match the README
or STOP); `SPAN-SUSPECT` and `MULTI` counts; `CALLERS.tsv`'s `same`-against-
changed-signature count by file; `STORAGE.tsv` moved/added/removed counts;
`PRESETS.tsv` rows per churn class with the sample results and the readable
pile per registry; the fpk parity result. Numbers only — no reading for
meaning, no verdicts.

## 3 · Scope fence

**In:** units A–D, `tools/treediff.py`, `tools/presetdiff.py`, the five TSVs,
`TRIAGE.md` §0, one fact for the fpk result. **Out:** reading any diff for
meaning (02–04); touching `luafn.py`, `bodycheck.py`, `sigcheck.py`,
`doccheck.py`; anything in `DLC/`; `Code/`. Something interesting in a row you
happened to see ⇒ one line in 02's inbox, not a read. ⚠️ If the two tools do
not both fit this context with their falsifiers, split at the boundary:
`01b_PRESETDIFF.md` takes B2 and the `PRESETS.tsv` counts, full inbox, own row.

## 4 · Stop conditions (permission, not failure)

The buildid is not `24995074` · the manifest re-derivation disagrees with the
README · `find_bodies` behaves differently from its docstring in a way the
falsifier cannot pin · the fpk extracts to something that is not Lua files ·
the context is half spent before unit C — split per rule 4 (`01b_TSVS.md`).

## 5 · What may NOT be claimed

That the inventory is COMPLETE (it is complete for top-level declarations the
regex recognises; say what the regex does not recognise). That a `body` row is
meaningful (02 decides). That `CALLERS.tsv` bounds reach (text-level). That fpk
parity proves the game runs Src (it proves the bytes match; `EF-078` still says
trust runtime).

## 6 · Close-out

Outbox to `02_TRIAGE.md` (the TSV paths, the counts, the `SPAN-SUSPECT` and
`MULTI` lists by name, what the regex missed, the fpk divergences by name) and
to `99_TERMINAL_AUDIT.md` (the same, plus every drift you caught, plus the one
assertion you broke on purpose and its RED output). Strike your README row.
`git add` by explicit path: `tools/treediff.py`, `tools/presetdiff.py`, the
five TSVs, `TRIAGE.md`, the fact file + `facts/INDEX.md`, README, 02, 99, and
`git rm` this file. `python tools/doccheck.py` GREEN, both `--selftest`s
GREEN. Commit `-F`, push.

## Notes from upstream

*(from the authoring session, 2026-09-09)* The diff shape in README §0 is
MEASURED from the manifests plus a declaration-line count; the 28,250 figure
counts `function`/`local function`/`= function` lines with a simple regex and is
an upper bound, not a row count. Nothing has read a body. The four seed
selectors are the `SRC:` pins in `Code/Fix_TrainCargoDumping.lua:112`,
`Code/Fix_LandscapeUnitFilter.lua:109`, `Code/Fix_TrackSalvageWipe.lua:90`, and
F117's callee `ChooseDome` at 1.1.0 `Lua/_GameUtils.lua:486` (`bugs/F117.md`).
