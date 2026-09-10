# 03 — the data link: 1630 generated files, read at FIELD level with a second instrument

⛔ ONE-SHOT: this file `git rm`s itself on close-out (README rule 2).
Model: Opus · owner needed: no · after 02, **before 04**.

> 🎯 The function-level differ reads `Data/`, `Lua/BuildingTemplate/`,
> `Lua/XDef/` and `Lua/ClassDefs/` as noise — 1630 of the 2444 changed files,
> `Data/StoryBit` alone 514. They are Lua-form PRESET DATA: `PlaceObj('Class',
> { key = value, … })` blocks. A field-level differ can read them, and `EF-078`
> is the precedent for why that matters: the source-read predicted 6
> self-disabled modules, the game measured 13, and the miss was *"preset/DATA
> checks invisible to any symbol sweep."* ⚠️ Expect most of it to be churn from
> a mass re-export. **Count the churn, set it aside by rule, read the rest.**

## 0 · Open in this order

`git log --oneline -10` · `git pull` · `ListAgents` · `README.md` · `STATE.md` ·
`TRIAGE.md` §0–§4 (02's ledger; your row list is §3 "03") · 01's fpk-parity fact
(does `Data.fpk` match `Data/`?) · `tools/audit_preset_fields.py` header (how
the project already derives the preset-container roster from Src at runtime —
reuse the roster derivation, never a hardcoded list) · `tools/luafn.py` ·
`DLC_DEEP_CHECK.md` §1.3 (the shared-registry list) · your inbox. Pin check.

## 1 · 🗒 Live todo list, from your first action

## 2 · Units

### A · `tools/presetdiff.py` + its falsifier — one author, in this session

Parse every `PlaceObj(` block in both trees' generated buckets into
`(file, class, id, key) → value-text`, nested tables flattened with a path
(`key.sub[3].leaf`). Emit `PRESETS.tsv`: one row per key whose value differs,
plus `added-preset` / `removed-preset` rows keyed by `class:id`. Columns:
`file · class · id · key · value107 · value110 · churn-class`. Banner as 01's.
`--selftest` on fixtures: a changed numeric value; a changed string; a key
added; a key removed; a preset added; a preset removed; a preset whose keys
were REORDERED only (**must NOT be a row**); a nested-table element change;
a `T(123, "text")` localisation-id change with the same text (its own
churn-class, `T-ID`); the same with a changed text (**a row**). Break one
assertion on purpose, see RED, restore, say so.

### B · Churn classes — a RULE per class, counted, and a sample READ per class

Classify every row by rule and count: `T-ID` (loc id churn), `REORDER`,
`FORMAT` (number formatting, quote style), `SAVE-ID` (editor-generated ids and
`save_in` fields), `COMMENT`. ⛔ Each churn class gets **20 random rows read by
you** to prove the rule is not hiding a value change; a single miss voids the
class and it goes back into the readable pile. Report per class: rows, sample
size, misses.

### C · The readable pile — what actually changed in the data

Whatever is left. Sort by the registry it lands in (`DLC_DEEP_CHECK` §1.3's
list first: `CropPreset`, `Meal`, `Resource`, `LawDef`, `PolicyDef`, `Tech`,
`Cargo`, then `BuildingTemplate`, `TraitPreset`, `StoryBit`, `XDef`,
`FactionDef`, `Scenario`, `PopupNotifications`). Fan out by registry if the
pile is large (README §4 rules; the agent gets rows, not files, and returns
per row: what the value change does to the base-game consumer that reads the
key — ⛔ **field-level, naming the CONSUMER by `file:line`**, or `consumer not
found` with the grep). ⭐ **The question for each row is the thesis's:** does
the old consumer still read the new value correctly? A new key nobody reads
(`FILES.tsv`-style presence check: grep the key name in `Lua/**`) is a
finding of the "dead validation" kind (`FIX_POLICY` §4 tell 2); a removed key
some consumer still reads is a nil where a value was.

### D · Hand-offs

Every `dlc-adjacent` row (02's word list applied to `class:id` and key) goes to
**04** in one section of `TRIAGE.md` → "For 04, from 03": rows by registry,
with the consumer named. `BuildingTemplate` rows whose consumer is a
`Lua/Buildings` class go to 05 or 06 by 02's system map. `XDef`/UI rows → 07.
Findings you can route COMPLETELY (both trees cited, consumer, who reaches it,
falsifier) are filed as `C` entries by YOU (README §3); partial ones are routed
with TAKEABLE WHEN.

## 3 · Scope fence

**In:** A–D, `PRESETS.tsv`, `TRIAGE.md` "03" coverage section (rows, churn
counts, samples, NOT-reached). **Out:** any `hand` row; `DLC/**` presets
(`dlccheck`); any C-side consumer (say `consumer not found in Lua`, never
"unused"). ⛔ Never edit `Data/` anywhere.

## 4 · Stop conditions

`Data.fpk` diverges from `Data/` for a registry you are about to read (read the
extracted one, flag rows) · the readable pile exceeds ~2,000 rows after churn
(split `03b_DATA_STORYBITS.md`: story bits are their own registry and the
biggest) · a churn rule misses twice.

## 5 · What may NOT be claimed

That churn is safe (it is RULE-classed and SAMPLED; say the sample size). That
a key is unused (say "no Lua reader found"; C-side is a blind spot). That a
value change is a balance bug (no balance opinions — `FIX_POLICY` §4 last
bullet; a value change is a finding only with a consumer that misreads it).

## 6 · Close-out

Outbox to 04 (the "For 04, from 03" section pointer), 05/06/07 (their rows), 99
(counts, samples, misses, drift, the broken-on-purpose assertion). Strike your
row. Explicit-path `git add`: `tools/presetdiff.py`, `PRESETS.tsv`,
`TRIAGE.md`, any `bugs/C##.md` + `bugs/INDEX.md`, README, 04–07, 99; `git rm`
this file. doccheck GREEN, both selftests GREEN, commit `-F`, push.

## Notes from upstream

*(authoring session, 2026-09-09)* `Data/StoryBit` 514 · `Data/BuildingTemplate`
287 (and `Lua/BuildingTemplate` 287 — the generated Lua twins; diff the `Data/`
side, and confirm on a sample that the twin carries nothing the `Data/` side
does not) · `Data/XDef` 200 (+196 twins) · `Data/` root 58 · `FactionDef` 28 ·
`Scenario` 26 · `PopupNotifications` 11. Removed data files worth a presence
check: `Data/TutorialPreset.lua`, `Data/DiscoveryGenericPreset.lua`,
`Data/FactionDef/TransHumanistMovement.lua`,
`Data/PopupNotifications/PopupNotificationPreset-Tutorial.lua` (README §0).
