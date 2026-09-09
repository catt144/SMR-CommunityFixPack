# 08 · The save residue our own deleted module left behind

Chain: `prompts/hotfix2/README.md` (its binding rules are yours). **Runs after
07, before 99.** Independent of everything else — it touches ONE module.

⚖️ Authored 2026-09-09 by link 07's session (`smr-bugfixpack-ee`) on the owner's
instruction — *"Can you author a quick 08 to fix the AstrogeologistExtractors
residue so it can be folded into the 99?"* — after link 07 found the residue was
owed, filed it, and could not fix it inside its own fence (the kit).

## 0 · Start

`git log --oneline -10` · `git pull` · `ListAgents` (several sessions edit this
tree at once; message any peer whose lane you enter). Staleness anchor: pack
`d254b88` (link 07 closed). Todo list first, one item per commit-and-verify unit.

**Read path.** `agent/STATE.md` (mandatory) · `reports/VANILLA_FIX_QA.md` **§0
first**, then its "What would make the patch half-baked" **item 1** — that item
IS this job · `reports/PACK_1_1_0_REVERIFICATION.md` rows **F-5** and **R-36** ·
`Code/90_SaveSanitizer.lua` in full (it is the host) · `agent/FIX_POLICY.md` §3
(absence-tolerant passes) · your inbox below, which carries every line of source
I verified so you do not re-derive them — ⛔ but **re-derive the ROUTE** (chain
rule 6): every route failure this project has had sat on top of individually
correct citations.

## 1 · ⛔ THE FIRST JOB IS TO TRY TO KILL THIS PROMPT

**Do not start by writing a sanitizer. Start by proving the residue exists.**

If `UIColony.label_modifiers` turns out to be rebuilt from the current presets on
load, there is no residue, this prompt is unnecessary, and the right close-out is
a one-paragraph finding that says so. That outcome is a SUCCESS, not a failure,
and it is worth more than a pass that cleans nothing.

The evidence that it does NOT get rebuilt is strong but it is all source-derived
and none of it has been run:

* `VANILLA_FIX_QA.md` item 1 states it outright and names the mechanism
  (`LabelContainer.lua:59-77`).
* ⭐ Our own deleted module says so in its own words, and this is the best line
  we have: *"Vanilla's own ten entries never hit this because EffectsApply runs
  once at game start and nothing re-applies them on load."*
  (`git show 2dc1dbe^:Code/Fix_AstrogeologistExtractors.lua`, the comment above
  its heal.) That module then built its heal on exactly that premise and shipped.
* Nothing in `Data/CommanderProfilePreset.lua` or the effects code re-applies a
  profile's effects on load; `OnApplyEffect` is driven by `EffectsApply`.

⇒ **A cheap empirical check exists and you should take it**: link 07 already
wrote one. The kit's `AstrogeologistExtractors` probe (`57_Probes_Wave8.lua`)
FAILs if the loaded save carries the residue and PASSes if it does not. Running
`SMRTest.AstrogeologistExtractors()` on a save that ran under the pack answers
this in one console line — ⚠️ but that needs the owner's rig and a save with the
right history, so it belongs to the post-99 sitting, not to you. **If you cannot
run it, say the premise is unverified and build the pass to be inert when the
residue is absent** (which is the FIX_POLICY §3 contract anyway).

## 2 · What the residue is, exactly

Our deleted `Fix_AstrogeologistExtractors` appended two `Effect_ModifyLabel`s the
shipped profile does not have:

| Label | Prop | Percent |
|---|---|---|
| `AutomaticMetalsExtractor` | `production_per_day1` | 10 |
| `MicroGAutoWaterExtractor` | `water_production` | 10 |

(from the module's own `MISSING` table at `2dc1dbe^` — read it, do not retype it
from here.)

Applying one calls
`colony:SetLabelModifier(self.Label, self:GetLabelModifierId(parent), Modifier:new{…})`
(`Lua/MarsGameEffects.lua:277-283`), and `label_modifiers` is persisted. So every
1.1.0 save that loaded with the pack on carries them, **and deleting the module
does not take them back**: `MicroGAutoWaterExtractor` also carries vanilla's
`Extractors` label, so it is getting **+30% water where 1.1.0 intends +20%**.

⛔ **THE KEY IS A PERSISTED TABLE YOU HAVE NO HANDLE TO.**
`Effect_ModifyLabel:GetLabelModifierId` returns **`self`** — the effect object —
when the effect is not `Stackable` (`MarsGameEffects.lua:248-254`). Our effect
objects were created at apply time by a module that no longer exists, so on a
later load the key is a table nobody can reconstruct. ⇒ **You must find the entry
by its VALUE, not by its key**: iterate the label's modifier table and match on
the stored `m.prop`.

## 3 · The job

### Unit A — the pass, in `90_SaveSanitizer.lua`

⭐ **Host it there, and add NO new file.** That module is already registered,
already `Require`s the exact API this needs
(`{ class = "LabelContainer", method = "SetLabelModifier" }`), already runs on
`PostLoadGame` with a written reason, and already carries the one-shot-per-save
flag pattern (`F48_FLAG` on `UIColony`). ⇒ **`H-10` never fires**: no new
`Code/*.lua`, so `items.lua` and `metadata.lua`'s `code` list are NOT touched,
and nothing about the shipped file set changes.

The removal primitive is already proven in our own shipped code — the deleted
module used it to clean up after an earlier version of itself:

```lua
colony:SetLabelModifier(label, key, nil)
```

Passing `nil` as the modifier makes `LabelContainer:SetLabelModifier` **first
un-apply the old modifier from every object in the label** (`f(obj, "remove",
old_mod, -old_mod.amount, -old_mod.percent)`) **and then delete the entry**
(`Lua/LabelContainer.lua:63-77`). One call does both halves. ⚠️ Read that
function yourself before you rely on this sentence.

Four things the pass must get right, each of which the record shows is easy to
miss:

1. **Remove EVERY match, not the first.** ⛔ The deleted module's own heal
   removed *duplicates* it had left in earlier saves — an identity-keyed version
   of it added a fresh +10% on each load, "growing without bound". So a save can
   carry MORE than one entry per label, and a pass that removes one leaves the
   rest. Count them and log the count.
2. **Collect the keys first, then remove.** Do not call `SetLabelModifier` while
   iterating the same table with `pairs`. The deleted module collected into a
   list and removed afterwards; copy that shape.
3. **Match narrowly and say what you matched.** `m.prop == <the prop for that
   label>`, inside those two labels only. ⚠️ Vanilla's astrogeologist effects are
   on the `Extractors` label, NOT on these two, so there is no vanilla entry to
   hit — but another mod could put one there. Consider `m.display_text == nil` as
   a second tell (our effects set no `Reason`, so `display_text` stays nil, while
   vanilla's carry one) — ⛔ verify that before relying on it, do not take it
   from me.
4. ⭐ **LOG WHAT WAS REMOVED, by label and count, and log nothing when there was
   nothing.** This is the only way the sitting can tell "this save was clean"
   from "this save was cleaned" — the kit probe runs *after* `PostLoadGame`, so a
   silent pass makes the probe's PASS ambiguous. That log line IS the evidence
   for this fix.

One-shot per save, on the `F48_FLAG` model. ⚠️ But think about the flag's
meaning: it is stored on `UIColony`, so it travels with the save. A save cleaned
once cannot re-acquire the residue (the module is gone), so one-shot is right.

### Unit B — the record

* `agent/bugs/` — the F95 entry (and F112 if it names this) gets a dated section:
  what the residue was, that the module is gone, what the pass does, and ⛔ that
  it is **unrun**. Do not move a status word.
* `docs/PLAYTEST_CHECKLIST.md` → the sitting: **one line** telling the owner what
  the `90_SaveSanitizer` log line will say if their save carried the residue, and
  that the kit's `AstrogeologistExtractors` probe is the cross-check.

### Unit C — ⚠️ the open decision this changes, which is the part to get right

⛔ **This pass makes `90_SaveSanitizer` non-removable, and that is an answer to a
question the owner has not yet been asked.**

`R-36` pulled `90_SaveSanitizer` OUT of the REMOVE block as
**PLATFORM-CONDITIONAL** (`VANILLA_FIX_QA.md` §0.6): REMOVE if the pack is
Steam-only in practice, KEEP if console/other players load 1.0.7 saves. That
reasoning rests entirely on **1.0.7 saves**.

**The residue is in a different population.** It is in **1.1.0 saves that ran
under the pack** — which exist on *every* platform, Steam included. So once this
pass lands, "remove the sanitizer" stops being a platform question and becomes
"leave a known wrong number in players' saves". ⇒ **Put this in
`PLAYTEST_CHECKLIST.md` → "Decisions waiting on you"**, next to the existing
platform item, in the owner's terms: *the sanitizer now has a job that has
nothing to do with 1.0.7 saves.* Do not resolve it yourself.

## 4 · Scope fence

**In:** `Code/90_SaveSanitizer.lua`; the F95 bug entry; the two checklist
additions; 99's inbox; this file's own `git rm`.
**Out:** every other module · `items.lua` and `metadata.lua` (nothing here adds
or renames a file, so `H-10` has nothing to check — if you find yourself opening
them, stop and re-read Unit A) · `tools/*` · **the Test Kit** (link 07 closed it;
its `AstrogeologistExtractors` probe already reports this residue and needs no
change — if you think it does, that is a finding for 99, not an edit) ·
`SaintBlessing`'s re-base, which is QA item 2 and **already landed** at link 03's
`3db4984` — do not re-open it.
Found something out of fence? **File it, do not fix it.**

## 5 · Stop conditions

- The residue turns out not to exist (§1) ⇒ **STOP and report that.** Close the
  prompt with the finding; do not write a pass for a problem you disproved.
- `SetLabelModifier(label, key, nil)` turns out NOT to un-apply the modifier from
  the objects — only to delete the bookkeeping ⇒ **STOP AND ASK.** Removing the
  record while leaving the effect applied is worse than doing nothing, and it
  would be invisible.
- The match would need to be widened beyond `prop` within those two labels to
  catch real residue ⇒ **STOP AND ASK.** A save-mutating pass that removes
  something another mod owns is the one failure mode with no undo.
- `Mars.exe` is open ⇒ do not touch `Code/` (`H-09`, chain rule 10).

## 6 · What may NOT be claimed

- ⛔ **Not "the residue is repaired"** — nothing here runs in a game. The honest
  form is "a pass is written and unrun".
- ⛔ **Not "saves are clean"** — the pass fires on the next load of each affected
  save, one save at a time, and no save has been loaded with it.
- ⛔ **No status word moves**; no bug entry gains `tested`.
- ⛔ **Not "the platform decision is settled"** — Unit C *raises* it, and the
  owner rules it.

## 7 · Close-out

One commit for the module + record (or two: pass, then record). `git rm` this
file, strike your row in `prompts/hotfix2/README.md`, append your outbox to
`99_TERMINAL_AUDIT.md`'s `## Notes from upstream`. This prompt is a ONE-OFF and
deletes itself. Gates: `python tools/doccheck.py` GREEN with `TESTKIT TREE:
clean`, `sigcheck`, `bodycheck`, `parsecheck` over `Code/`, and the `TEMPORARY`
sweep (`grep -rln "TEMPORARY" Code/ ../SMR-BugFixPack-TestKit/Code/`) in the todo
list and in the commit message. `git commit -F <file>`, then push.

## Notes from upstream

*(From link 07's session, `smr-bugfixpack-ee`, 2026-09-09. ⛔ Nothing below ran in
a game. Every line citation was read in the shipped 1.1.0 tree or in git on
2026-09-09 — but they are CLAIMS, and chain rule 6 asks you to re-derive the
route, not just re-check the citations.)*

**1 · Why this is owed at all.** Link 07 retired the kit's
`AstrogeologistExtractors` probe and, while doing it, turned `VANILLA_FIX_QA`
item 1 into a machine check: the probe's third clause FAILs when the loaded save
still carries our +10% entries, with a message naming the owed sanitizer. That
clause is the only automated report of this anywhere, and it reports — it cannot
repair. Hence 08.

**2 · The three source facts the pass rests on**, with what I actually read:

* `Lua/LabelContainer.lua:63-77` — `SetLabelModifier(label, id, modifier)`. With
  `modifier` nil it removes the old modifier's effect from every object in the
  label and then clears the entry. **One call does both halves.**
* `Lua/MarsGameEffects.lua:248-254` — `GetLabelModifierId` returns `self` for a
  non-`Stackable` effect. **This is why the key is unreachable and you must match
  on the value.**
* `Lua/MarsGameEffects.lua:277-283` — the stored `Modifier` shape:
  `{ id, prop, amount = Amount*scale*count, percent = Percent*count, display_text }`.
  Ours had `Percent = 10` and no `Amount` and no `Reason`.

**3 · ⭐ Read the deleted module's own heal before you write anything.**
`git show 2dc1dbe^:Code/Fix_AstrogeologistExtractors.lua`, the block just after
its "Test by PROPERTY instead" comment. It is ~20 lines and it is *this job
already written*, inverted: it matches `m.prop == effect.Prop` inside the label,
collects extras into a list, and calls `colony:SetLabelModifier(label, key, nil)`
on each. It also documents the duplicate-growth failure that makes "remove every
match" mandatory. Reusing its shape is not laziness; it is the shape that already
survived review, and re-deriving a different one is how the two diverge.

**4 · What I could NOT settle, named so you do not inherit it as fact.**

* **Whether any save actually carries the residue.** No save has been loaded
  with the pack on 1.1.0 (`STATE`), so the population is inferred, not observed.
  §1 is written to make disproving it a legitimate outcome.
* **Whether `display_text == nil` is a reliable second tell.** I reasoned it from
  `MarsGameEffects.lua:270-276` (no `Reason` ⇒ `display_text` stays nil) and did
  not test it. Treat it as a hypothesis.
* **How many entries a real affected save carries** — one per label, or several
  from the identity-keyed era. The module's own comment says "growing without
  bound" was possible. Count and log; do not assume one.

**5 · Two prompt-shape warnings from my own link, which cost me real time.**

* ⛔ **A bare helper name that is not aliased in its file parses fine and ERRORs
  at run time.** `parsecheck` cannot see it. If you add any `SMRFixPack.*` or
  local-alias call to `90_SaveSanitizer.lua`, check the file's own alias/`local`
  lines. This bit me three times in one session and once *after* I had committed.
* ⚠️ **The chain README's read path still says the 1.0.7 tree is "GONE
  (`EF-075`)".** It is ARCHIVED and on disk at
  `C:\Dev\SMR-SrcArchive\1.0.7.396349\Src` — `STATE` says so and link 04b used it
  for three-way diffs. You will want it if you check what our effects looked like
  when they were first written.

**6 · Do not scope-creep into the sibling item.** `VANILLA_FIX_QA` item 2 (the
F-1 `SaintBlessing` 1.1.0 re-base) reads like a twin of this one and is **already
landed** — link 03, `3db4984`, "a SECOND one-shot save re-base for the 1.1.0
branch". I checked. It is not yours.
