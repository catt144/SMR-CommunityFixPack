# Link 1 — build `C51`: three UI strings that can never be translated

♻️ **SELF-CONSUMING.** `git rm` this file in your closing commit, naming its grave.
📋 Read `README.md` in this folder first — its binding rules govern you.

## 0 · Read path

```
git log --oneline -15 && git pull
python tools/doccheck.py --emit-counts
```

`docs/agent/STATE.md` · `agent/bugs/C51.md` (**the whole entry**) ·
`agent/facts/EF-039.md` (**the localization mechanism — this fix lives or dies by
it**) · `agent/FIX_POLICY.md` §1 (least invasive technique), §2 (fail safe), §6
(engine semantics) · an existing module for house shape, e.g.
`Code/Fix_TechDescriptionBuilding.lua` (the pack's other text repair).

## 1 · 🗒 Live todo list — one item per numbered step below

## 2 · What you are building

Three player-visible strings render untranslated in nine languages **while their
translations sit in the shipped language packs**. Nothing is re-worded; the fix
points the UI at ids that already exist.

| what | the id the UI uses now | the enrolled id to use |
|---|---|---|
| *OVERALL TERRAFORMING PROGRESS* heading | ⛔ **no id at all** — a raw Lua literal | `914616772802` |
| *Back to Earth* rollover **title** | `885571832096` — ⛔ in no language pack | `407456913268` |
| *Back to Earth* rollover **text** | `807999655245` — ⛔ in no language pack | `316233855405` |

⭐ **This was measured, not inherited** (2026-08-20, this repo's own
`tools/flpk_extract.py` against `Local\German.fpk`): the three replacement ids
return German text; the two the button uses return **zero hits**. ⚠️ **Re-derive
it anyway if you touch the claim** — `recalled facts are claims too`, and the
extractor takes seconds:

```python
import sys; sys.path.insert(0, 'tools')
import flpk_extract as fx
fx.extract(r'A:\SteamLibrary\steamapps\common\Project Spark\Local\German.fpk', r'<scratch>')
```

⚠️ **`Src` is under the install dir literally named `Project Spark`** — the old
`Surviving Mars` folder has a `ModTools` with **no `Src`** and is a decoy
(`EF-014`). Both hook points, verified at Src 2026-08-20:

- `TerraformingOverall` — class, `Init` at `Lua/XDef/TerraformingOverall.generated.lua:18`;
  the literal is at `:56`.
- `customUniversalRocket` — class, `Init` at `.../customUniversalRocket.generated.lua:11`;
  the button carries `Id = "idBackToEarth"` at `:25`.

## 3 · The build

1. **`Code/Fix_LocalizedUIText.lua`** (name it as you see fit; `items.lua` and the
   `code` list must match whatever you choose). House header: the defect, the
   source citations, the route, and **why the repair cannot regress anything** —
   under `EF-039` a `T()` on an *enrolled* id returns the light userdata and
   rendering reads `TranslationTable[id]`, so no English literal is anywhere in
   the path.
2. **Technique: chain, never replace** (`FIX_POLICY` §1). Wrap the two `Init`
   methods, call the original first, then correct the built controls. ⚠️ If
   another mod has already replaced one, capture *that* version as the original
   so their work stays in the chain.
3. **Handles.** The rocket button has an `Id` — use it, never a text match. The
   terraforming heading has **none**, so its only handle is its literal English
   text. ⛔ Say so in the header, and make the failure **loud in our log and
   silent on screen** (`FIX_POLICY` §2): if the control is not found, the module
   stands down with a reason line, it does not guess.
4. **Self-check before patching** (`Require`-style shape checks): both globals
   exist, both are tables, `Init` is a function. A failed shape check ⇒
   `inactive` with a reason, never an error.
5. **Save safety: this writes NOTHING.** UI text only, no persisted state, no
   `GameVar`, no game-time thread. State that explicitly in the header — it is
   what makes this fix free to add to any save (`FIX_POLICY` §3a).
6. ⛔ **`items.lua` + `metadata.lua`'s `code` list** — same filename, same order,
   by hand. Then `python tools/upload_preflight.py` must still read **0 FAIL**
   with the two lists agreeing.
7. **Probe:** add one to the TestKit **only if it can fail honestly.** A probe
   that asserts our wrapper is installed and that `T(914616772802)` resolves is
   worth having; a probe that cannot distinguish a working fix from a broken one
   is worse than none. ⛔ Do not invent a screen reading — link 4 owns that.
8. **Parse sweep**, `doccheck` GREEN, counts re-emitted (`75` modules becomes
   `76` here; link 2 makes it `77`).

## 4 · Scope fence

**IN:** the three strings above · the module · `items.lua` + `code` list · a probe
if it can fail · the entry updated with what you built.

**OUT:** ⛔ `C50` (link 2 — do not "while I'm here" it) · ⛔ the *COLONY DATA*
heading and the two `OptionsContentWindow` strings (**no record in any pack**;
they need a `ModItemLocTable`, which is a different decision and is not ruled) ·
⛔ the tag · ⛔ `metadata.lua`'s `version` · ⛔ any portal call · ⛔ the site repo.

## 5 · ⛔ What you may not claim

- ⛔ **"Verified"** on anything you did not run. **Nothing in this link is
  observed on screen** — link 4 is the first eyes. Your report says *built,
  unobserved*.
- ⛔ **"It renders in German"** — no leg in this project's history has ever
  watched a shipped-id string render in a non-English language (`EF-039`'s own
  closing note). You are not the leg that changes that.
- ⛔ A probe result you did not read in a log.
- ⛔ Any count you did not emit with `doccheck --emit-counts`.

## 6 · Close-out

One commit: the module · `items.lua` + `code` list · probe if any ·
`agent/bugs/C51.md` updated (what was built, and that it is unobserved) ·
`STATE.md` touched only if a fact of record changed · `doccheck` GREEN ·
`git rm` this file · push.

**Owner report:** what you built in three sentences · what is unobserved · the
`upload_preflight` line · **the kickoff line for `02_BUILD_C50.md`**.

## Notes from upstream

- 2026-08-20, chain author: the two `Init` methods are **global classes with one
  caller each** across the whole Src tree — this is the pack's ordinary wrap
  shape, not a special case.
