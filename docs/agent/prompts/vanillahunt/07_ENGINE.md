# 07 — the engine layer: CommonLua, UI, storage moves, and the removed/added files

⛔ ONE-SHOT: this file `git rm`s itself on close-out (README rule 2).
Model: Opus · owner needed: no · after 02; independent of 03, 04, 05, 06.

> 🎯 Three jobs nobody else has: (1) `CommonLua/**` (~365 changed files) and
> the UI trees, where a change is felt by EVERY system above it; (2) class (c)
> from `STORAGE.tsv` — a concept that moved home (`Landscapes` GameVar→MapVar
> was one; `const.`→`g_Consts` another) breaks every reader that kept the old
> address, silently; (3) the 36 removed and 305 added files, each a (d)/(e)/(f)
> question that must be answered with the PRESENCE side enumerated. ⚠️ Much of
> `CommonLua` is editor/dev tooling — but that is decided **by route** (loaded
> only under `Platform.developer`, `Platform.ged`, an editor-only `OnMsg`, a
> `DevToolsPublic` path that the shipped `.fpk` may not even contain — 01's
> parity list says), never by directory name. A "tooling" verdict without the
> loader cited is a path-name proxy, and this project's rule is check the
> thing, not its label.

## 0 · Open in this order

`git log --oneline -10` · `git pull` · `ListAgents` · `README.md` (§2, §3, §4)
· `STATE.md` · `TRIAGE.md` §3 "07" · `STORAGE.tsv`, `FILES.tsv`, `CALLERS.tsv`
rows in your files · 01's fpk-parity fact (which `CommonLua` files are NOT in
the shipped fpk — those are not shipped code and say so) ·
`PACK_1_1_0_REVERIFICATION.md` §1 REMOVE rows in `CommonLua` ·
`facts/INDEX.md` (`EF-005`, `EF-009`, `EF-017`, `EF-066`) · `FIX_POLICY.md` §6
(engine semantics) · your inbox. Pin check.

## 1 · 🗒 Live todo list, from your first action

## 2 · Units, in order

### A · The tooling gate — by route, once, in the parent

For every `CommonLua` subtree in your rows, cite the loader: how does the file
get `dofile`d/`require`d, and under what platform/flag? Three verdicts:
`shipped-runtime` (read in full), `shipped-dev-only` (loaded only under a
developer flag — read the gate, sample 10 rows for anything that leaks past
it), `not-in-fpk` (01's list — not read, counted). Write the table into
`TRIAGE.md` "07" before reading a body. ⛔ `CommonLua/Libs/MapGen` and
`Lua/RandomMap` are RUNTIME (map generation) until the loader says otherwise.

### B · Class (c) — `STORAGE.tsv`

Every `moved-file`, `kind-changed`, `removed` storage row: grep both trees for
every READER of that name (the `FILES.tsv` presence discipline), and classify
each reader `updated / still-old-address / dynamic`. A `still-old-address`
reader in a `shipped-runtime` file is a finding: name what it now reads (nil,
a stale copy, a per-map value where a per-game one was). The `Landscapes`
move — 1.1.0 `MapVar("Landscapes", {})` at `Landscaping.lua:21` where 1.0.7
had a GameVar (`bugs/F115.md` §"what was read", line ~46) — is the worked
example: do it first as your own calibration and check your result against
that entry.

### C · Removed and added files — (d)/(e)/(f) with the presence side

The 36 removed (README §0 lists them): for each, the declared names that still
appear in 1.1.0 (01 counted them) — a nonzero count is a RENAME/MOVE (find
where; that is class (d) and the feature is not gone), zero is a candidate (e)
that still needs the CAPABILITY searched (the UI string, the preset, the
`XTemplate` that instantiated it). ⭐ Five removed `XDef` dialogs
(`ResearchDlg`, `CommandCenterLifeSupportGridsOverview` + `Row`, `ipFirefly`,
`sectionStorage`) and five tutorial files are the obvious (d)-or-(e) cases;
the old modding backend (`CommonLua/Classes/Mod*.lua`, `ModsBackend.lua`) is
the one with the widest reach — what replaced it, and does every
`ModsBackend` caller resolve? The 305 added, minus `DLC/norman` (04/dlccheck):
class (f), grouped by what they plug into; a new file whose names have ZERO
callers is dead-on-arrival code (tell 2) or a hook by name (`OnMsg`,
`XTemplate` id) — say which, with the search.

### D · `commonlua` and `ui` rows

(b′) first, then (a)/(b) `WORTH-READING` in `shipped-runtime` files —
`CommonLua/Classes` 76, `Core` 25, `Libs` (runtime part), `X` 30, `UI` 18,
`Lua/UI` 17, `Lua/X` 20, `XTemplates` 5 — then (i), (f), then a 30-row `CHURN`
spot check. ⚠️ A `CommonLua` body change is felt above it: for every real
change, name ONE consumer in `Lua/**` and read whether it still holds
(`EF-066`'s composed-`Init` lesson: a change in `classes.lua` reaches every
descendant).

## 3 · Method

As 05 §3. Engine-semantics claims go through `facts/INDEX.md` first and become
`EF-###` facts, not `C` entries, unless a shipped reader misbehaves. UI
findings: `FIX_POLICY` §4 says hit-testing/input-mode wrongness is a
hypothesis until a keyboard sees it — file as `cand` with the observation
named, tier U.

## 4 · Scope fence

**In:** A–D, filing, `TRIAGE.md` "07" (the tooling table, storage table,
removed/added table, coverage). **Out:** `dlc-adjacent` rows (04);
`Lua/Buildings`, `Lua/Units` (05/06); `Data/` (03); `DLC/**`; any tool edit
beyond a fact about one.

## 5 · Stop conditions

`shipped-runtime` `CommonLua` rows above ~500 `WORTH-READING` at the START —
split up front (`07b_ENGINE_UI.md`: the `ui` system + `Lua/X`) · the tooling
gate cannot be settled for a subtree from the loader (route as `unsure`, do
not guess `dev-only`) · a storage move whose readers are all dynamic (fact,
not finding).

## 6 · What may NOT be claimed

`tested`. That a subtree is tooling by its name. That a removed file's feature
is gone without the capability search on the entry. That a `CommonLua` change
is harmless without one named consumer read.

## 7 · Close-out

Outbox to 05/06 (rows that turned out theirs), 04 (seams), 99 (findings,
the three tables, NOT-reached, spot check, drift). Strike your row.
Explicit-path `git add`: `TRIAGE.md`, `bugs/C##.md` + `bugs/INDEX.md`,
`facts/EF-###.md` + `facts/INDEX.md`, README, 05, 06, 99 (and 04 if not yet
consumed); `git rm` this file. doccheck GREEN, commit `-F`, push.

## Notes from upstream

*(authoring session, 2026-09-09)* The removed-file list is in README §0
verbatim from the manifests. Calibration case, already answered at the FILE
level: `CommonLua/Classes/Mod.lua` is in the removed list and
`CommonLua/Modding/Mod.lua` exists in 1.1.0 (checked 2026-09-10 against the
archive) — a MOVE, class (d), which is what `FILES.tsv`'s presence count must
say for it; the `H-02` citations in `STATE.md` (`Mod.lua:967`,
`GedModEditor.lua:836-844`) were re-read on 1.1.0 by hotfix 2 and hold. The
vanilla question is every OTHER declared name of the six removed `Mod*.lua`
files and whether each still resolves.
