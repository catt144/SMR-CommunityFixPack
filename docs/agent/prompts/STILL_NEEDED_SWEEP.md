# Is each shipped fix still NEEDED on 1.1.0? — a per-module settlement

> 🚧 **NOT STARTED.** Written **2026-09-12** by `smr-bugfixpack-cb` at the owner's instruction, for a **fresh
> session** — this one's context was low. **Staleness anchor: HEAD was `8eff833`, 46 registered modules, 47
> `Code/*.lua`.** `git pull` + `git log --oneline -15` first; the records win.
> ⚠️ Live todo list from your first tool call. 🛑 Stop and ask at any point.
> ⛔ **Do NOT bundle any of this into the v9 upload.** v9 is F59 + F60 and is already written.

## ⚖️ Why the owner wants this, in their own framing

1. **"I really hate keeping things in there if they are not needed."** Dead fixes are not neutral: each one is a
   line on the public fix list, a row a player trusts, and a module that loads.
2. ⭐ **TWO PARADOX DEVELOPERS ARE USING OUR FIX LIST TO PLAN THEIR NEXT HOTFIXES** (owner, 2026-09-12). That
   changes the cost of a stale row from *our credibility* to **their wasted time** — a row claiming a defect the
   game already fixed can send a developer to repair something that is not broken. ⇒ **accuracy here is now an
   obligation to a third party**, not housekeeping.

## The question, and the only three answers

For **every** shipped module: *on game 1.1.0.403908, is this fix still needed?*

| verdict | meaning | action |
|---|---|---|
| **RETIRE** | the game's own update resolved what it was written for | delete the module + `items.lua` + the `metadata.lua` code list (H-10, all three together); remove its fix-list row; count drops |
| **REBUILD** | the defect remains but 1.1.0 moved the code the fix was built on | rework against the new body |
| **KEEP** | still needed and still does what we say | ⚠️ but check the CLAIM separately — see below |

⛔ **KEEP has a fourth failure mode that tonight's work kept hitting: the code is fine and the CLAIM is not.**
F51 and F58 both stayed, while their fix-list rows had to be narrowed because 1.1.0 changed what the fix still
buys. **Judge the row and the module separately**; a correct module with an overstated row is exactly what
misleads the developers now reading it.

## ⛔ Read these first — this is NOT a fresh sweep

**Hotfix 2 already did this once** (v6, 2026-09-09): `prompts/hotfix2/README.md`, `reports/HOTFIX_2_AUDIT.md`
— **36 modules retired, 10 re-copied** against 1.1.0's changed bodies. **Do not redo what it cleared.** Your job
is the residue it left and the cases it got wrong, and there are known examples of both:

* ⭐ **F60 — hotfix 2 KEPT a module that should have gone.** `Fix_DomeFreeSpaceMismatch` survived the cull, and
  on 2026-09-11 it was retired: 1.1.0's admission gate stopped reading the tally the fix corrected, so it only
  moved estimates — *optimistically against the gate*. **Tell:** the module still applied cleanly; what had moved
  was the **consumer**. A sweep that only asks "does the fix still apply?" misses this entirely.
  ⇒ **Always ask "does anything still READ what this fix changes?"**
* ⚠️ **`Fix_SaintBlessing` — self-disables on 1.1.0 and is CORRECTLY kept.** `EF-078` measured it inactive
  ("no dome-colonists trait presets"), and vanilla did fix the bug (`Lua/TraitPreset.lua:86` now uses
  `GetTraitLabel(trait)`; 1.0.7's `ClassDef-PresetDefs.generated.lua:1783` used the raw name). It stays because it
  (a) heals saves damaged while the two repairs collided and (b) still works for 1.0.7 players, who get the LIVE
  pack from the portals. **Its fix-list row already explains all of this.** ⇒ **an inactive module is not
  automatically a retirement**, and the 1.0.7-on-the-portals population is a real constituency (`ck151 e`: the
  frozen build is only for players who follow the card's legacy link).
* ⚠️ **`Fix_ExoticDepositSign` (F102) — NEVER re-checked for 1.1.0.** Entry last touched 2026-08-14, no 1.1.0
  section; it simply survived the cull. Its class default is unchanged on 1.1.0 (`SubsurfaceDeposit.lua:517`) and
  it self-gates on `IsValidEntity("SignRareMineralsDeposit")` (`Code/Fix_ExoticDepositSign.lua:76`), so it is safe
  either way — but **whether it is active or silently stood down on 1.1.0 is unknown**, and its cure was never
  verified. ⇒ **a module nobody re-opened is not a module that was cleared.**
* **The migration eight** (`reports/MIGRATION_DEV_REPORT.md`, cross-checked `reports/MIGRATIONFIX_AUDIT.md`):
  F59 repaired, F60 retired, F51/F58 rows narrowed, F52/F53/F73 **PARTIAL with open residuals**, and **F54 was
  never swept at all** (audit §4, "not swept, by name"). ⇒ start from that table, do not re-derive it, and
  **F54 is an outright gap**.

## ⛔ A SECOND axis, added 2026-09-12 after the owner caught a live drift: SURFACE CONSISTENCY

The owner spotted that the store card still read **"Colonists stayed homeless after you built a Shuttle Hub"** —
the exact F51 overclaim that had just been removed from the site fix list. Cause: a session applied
`PUBLIC_SURFACE_SWEEP` **§1 (the site) without §2/§3 (the store cards)**. Fixed on the spot, but the class is open.

**Nobody has ever diffed the card's ~22 headline bullets against the 49 fix-list rows.** Both are hand-maintained,
they live in different repos, and only the *count word* is checked mechanically. ⇒ **add to this sweep: for every
card bullet, does a fix-list row still support it, and does that row still match the module?** Three surfaces, and
a claim can rot on any one of them independently.

Also unverified on the card, and cheap to settle while you are there:
* **"And three of them repair things you cannot see at all today"** — is it still three after F60's retirement?
* **The judgment-call count (3)** — the v8 close-out said unchanged, but it was not re-derived after F60.
* **The `SMRFixPack_Disabled["LakeEntombment"]` example in the modders' section** — verify that id still ships.

✅ **One class that IS clean, checked 2026-09-12 — do not re-open it.** Of the 13 modules `EF-078` measured going
inactive on the 1.1.0 baseline, **11 were removed by hotfix 2**, `SaintBlessing` is correctly kept (above), and
`Fix_VacuumWalks` was **re-copied and repaired** by hotfix 2 (`7a401f1`; its header at `:78` names the
`{ path = {"const","ColonistMaxDomeWalkDist"} }` spec that had failed). ⇒ no shipping module is silently inactive
for that reason. ⚠️ That is a *source-and-log* read of the 09-08 baseline plus hotfix 2's commits — **a fresh boot
log supersedes it**, which is why §3 of the Method asks for one early.

## Method — the parts that are binding

1. **Both sides, always.** A REMOVE verdict needs the **replacement traced**: name the vanilla body that now does
   the job, name every residual the module still changes, and grep where a vanished name *went* — a rename reads
   as "gone" and has nearly retired a live fix. (`AddDomeColonistsModifier` moving from a generated file to
   `Lua/TraitPreset.lua` is tonight's worked example.)
2. **Check `facts/INDEX.md` BEFORE deriving any engine claim.** Tonight a session re-derived `EF-019` from source
   without reading it first. The index is 92 rows and cheap.
3. **A runtime read is the only thing that measures a preset/data check** (`EF-078`): `SaintBlessing`,
   `DustSicknessDamage` and `IndependenceTerraforming` all fail on the *shape of shipped preset data*, invisible
   to any grep. ⇒ **the boot log's active/inactive list is evidence no source read can replace.** Getting one
   costs a single launch and settles the whole "is it actually applying?" axis in one shot — do that early.
4. **Two of the inactive modules are NOT named in the player-facing "switched themselves off" dialog**
   (`SaintBlessing`, `LastTransmissionStorage` — they do not set `update_suspect`). ⇒ absence from that dialog is
   not evidence a module is active.
5. `FIX_POLICY` §4a who-benefits and the retire-vs-keep call are **the owner's**, not yours. Produce verdicts with
   evidence; route the decisions to `PLAYTEST_CHECKLIST.md`.

## Size, and how to run it

46 modules is more than ~2 sessions ⇒ **propose a chain** (`reports/CHAIN_METHOD.md`), do not start swinging.
A sensible cut: a cheap mechanical pass over all 46 first (does it still apply? does anything still read what it
changes? is its fix-list row still true?), which triages into a short list that gets the expensive treatment.
⚖️ Owner routing: **broad hunts and censuses go to Codex/Astra; builds stay with Claude.** A 46-module census is a
hunt. ⛔ Write the brief tool-neutral and make the coordination git-visible — Codex sessions are invisible to
`ListAgents`.

## Deliverables

- A per-module table: **RETIRE / REBUILD / KEEP**, each with `file:line` on 1.1.0.403908 and `SOURCE` or
  `INFERRED`, **plus a separate column for whether its fix-list row is still true.**
- **Disagreements first**, then an ideas list kept separate from findings.
- **What you did not check, by NAME.**
- The owner's decisions to `PLAYTEST_CHECKLIST.md`; nothing retired without their ruling.
- ⚠️ Any row correction feeds `PUBLIC_SURFACE_SWEEP` and `RELEASE_OUTBOX`, not a direct edit — that shortcut was
  taken on 2026-09-11 and the owner caught it.
