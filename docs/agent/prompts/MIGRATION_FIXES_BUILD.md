# BUILD — the migration audit's code actions: repair F59, then verify-or-drop F60

Paste into a fresh session (any model; the owner picks — this is a BUILD, so Claude per the 09-11 routing).
Written **2026-09-11** by `smr-bugfixpack-cb`. **Staleness anchor: HEAD was `33b9f8e`.**
Start with `git pull` + `git log --oneline -15`; the records win over every specific below.
⚠️ **Keep a live todo list from your first tool call** — the owner reads it to decide when to step in.

> ⚖️ **OWNER, 2026-09-11: ship tonight.** ⚖️ **ck151 (e) RULED: 1.0.7 stays frozen** — no new legacy build.

## ⛔ READ THIS FIRST — the audit does NOT contain seven fixes

`reports/MIGRATION_DEV_REPORT.md` reviews eight modules, but its own Appendix B and §-dispositions propose
exactly **TWO code actions**: **repair F59** and **retire F60**. Everything else is a *claim* change, not a
*code* change:

| Module | Report verdict | Is there code to ship? |
|---|---|---|
| F59 `FreedHousingNotice` | HARMFUL | ✅ **YES — item A below** |
| F60 `DomeFreeSpaceMismatch` | PARTIAL, retirement recommended | ⚠️ **CONDITIONAL — item B below** |
| F51 · F52 · F53 · F58 · F73 | PARTIAL | ❌ no — keep the module, narrow what we *claim* |
| F54 `ShuttleHubOffAvailable` | STILL NEEDED | ❌ no — unchanged |
| F80 | controlled loop-boundary omission | ❌ **no — capture BEFORE mitigating** (report §13) |

⇒ The PARTIAL rows change the **fix list and the store card**, not `Code/`. That is a public-surface job
(`prompts/perma/PUBLIC_SURFACE_SWEEP.md`), **out of scope here**; do not start it, do not block on it.
If the owner expected seven fixes, say this in one line and carry on — the job is smaller, not skipped.

## ⛔ GATE 0 — do not start until both are true

1. **The release lane is clear.** `items.lua` and `metadata.lua` were the owner's uncommitted Mod Editor pack
   (v8) when this was written. **H-10 makes item A require an `items.lua` entry only if you add/rename/drop a
   module — a repair inside an existing file does not.** Run `git status --short`: if either file is modified
   and uncommitted, **do not edit, stage, or work around them**; ask the owner. Item B *removes* a module and
   therefore DOES collide with H-10 — see item B's own gate.
2. **ck151 (a)/(d) is ruled, or you default and say so.** The recommendation on the checklist is *repair, not
   retire* for F59. If unruled, build the repair and note the default in one line of the commit body.

## A · Repair F59 — the committed deliverable

**Do not re-derive the diagnosis.** It has been independently derived twice (Astra `40a0c6b`, re-derivation
`45a90ca`) and every citation below is verified against **1.1.0.403908**; `bodycheck.py` read 110 OK at the time.
The full dossier is `bugs/F59.md`, last two sections. Summary of what you are fixing:

`Code/Fix_FreedHousingNotice.lua:66-79` post-hooks `Colonist:SetResidence` and calls
`left:CheckHomeForHomeless()` whenever the home just left has free space. That is correct when `SetResidence`
IS the operation, and wrong when it is a MIDDLE step of a larger one that still needs the slot:

- **A1 — expedition boarding (1.1.0 only).** `Colonist:EnterTransporter` saves `expedition_residence`
  (`Lua/Units/Colonist.lua:5029-5031`) → `SetDome(false)` `:5039` → `SetResidence(false)` `:434` → **our hook** →
  a homeless neighbour takes the bed → `Unit.EnterTransporter` `:5043` → `Unit.lua:1305` → `:1225` →
  `Colonist:OnDisappear:5003-5008` fails `CanReserveResidence` and clears the hold.
  ⛔ 1.0.7 has no `expedition_residence` at all (`EnterTransporter` is two lines there) — this harm is 1.1.0-only.
- **A2 — manual assign (BOTH branches, shipped since the module was written).**
  `Residence:ColonistInteract:342` → `KickOldestResident:368` → `KickResident:157` → `SetResidence(false)`.
  Here `self.dome` is intact, so `UpdateHomelessLabels:2893` puts the just-kicked resident into the dome's
  Homeless label **inside the same call** — the hook then hands them back the slot `:348` is about to fill, and
  `AddResident`'s `assert(GetFreeSpace() > 0)` (`Residence.lua:111-112`) does not unwind (`EF-008`)
  ⇒ **an over-capacity residence, and the player's eviction silently undone.**

**⛔ The report's proposed expedition-home exclusion is NECESSARY BUT NOT SUFFICIENT** — it does nothing for A2.

**What the repair must satisfy — these are the acceptance conditions, not a design:**
1. A1 and A2 both stop. The crew keeps the hold; manual assign lands exactly one colonist and stays in capacity.
2. **The ordinary benefit is provably intact.** That is the module's entire reason to exist: a freed bed is
   offered immediately instead of after `Clamp(#Colonist/300, 0, 12)` hours (`City.lua:117-119`, consumed by
   `Colonist:Idle` `:2338-2358`) — up to 12 h at 3,600+ colonists. A repair that quietly disables the
   notification is a removal wearing a fix's clothes; if that is where you land, STOP and say so.
3. **Enumerate all 11 shipped callers of `Colonist:SetResidence` and state, per caller, whether your guard
   changes its behaviour** (`FIX_POLICY.md` §4, the rule this module's failure produced):
   `Colonist.lua:435` (SetDome — A1) · `:1255` (Erase) · `:1297` (death) · `:2926` (UpdateResidence — the
   intended case) · `:4995` (OnDisappear, a no-op by then) · `Residence.lua:85` (OnDestroyed) · `:157`
   (KickResident — A2) · `:265` (capacity shrink) · `:348` (ColonistInteract's own assignment) ·
   `NaturalHabitat.lua:7` · `Data/TraitPreset.lua:772`.
   Already settled, do not redo: `:265` is SAFE (its loop only runs while `GetFreeSpace()` is 0, so the guard
   never opens). `Residence:OnDestroyed:81-92` is an **UNRESOLVED lead** — vanilla's own `:86` has the same
   exposure, so do not "fix" it here; if your guard changes it, say which way and file separately.
4. `FIX_POLICY` §1 fix-shape (prefer a chained wrapper), §2b `SRC:`/`DEFECT:` manifest re-pinned if a target
   moved, §3a save-safety.

**Regression bar — both existing harnesses must still pass, plus new legs for what you add:**
`python tools/desk_f59_expedition.py` (12/12) and `python tools/desk_f59_interact.py` (8/8).
⛔ Add a leg that FAILS on the unrepaired module for each harm you claim to fix — a harness that cannot fail is
not evidence. The unbuilt candidate inside `desk_f59_expedition.py` (`candidate=True`) is an **idea, not a
design**: it only covers A1.

## B · F60 retirement — VERIFY FIRST, and it must NOT block A

Report §7 recommends retiring `Fix_DomeFreeSpaceMismatch`. **That verdict is single-sourced from the audit and
nobody has checked it.** A REMOVE verdict needs the replacement traced (house rule): name the vanilla body that
now does the job, name every residual the module still changes, and grep where any vanished name went — a rename
reads as "gone" and has nearly retired a live fix before.

**Gate:** removing a module is an H-10 change (`items.lua` + `metadata.lua` `code` list rebuilt by `SaveDef`) and
collides with the owner's uncommitted v8 pack. If that lane is not clear, **ship A alone tonight and leave B**.
**If the trace does not hold cleanly, ship A alone and say why.** Do not bundle an unverified removal into a
release to make the set look complete.

## Ship checklist (post-launch is patch-note maintenance, NOT the pre-release gate — owner ruling)

- `python tools/parsecheck.py` · `python tools/bodycheck.py` · `python tools/doccheck.py` GREEN (counts from
  `--emit-counts`, never hand-typed; `--regen` for the generated indexes).
- Update `bugs/F59.md` (and F60 if B ships) with what was built — status words per the project's vocabulary;
  `tested-attended` is **not** yours to stamp, it is the sitting's.
- ⛔ **H-02: never touch `version`/`version_major`/`version_minor`, and never open the Mod Editor.** The bump is
  the owner's sitting. ⛔ **H-03: no portal API from a launched game.**
- Commit by pathspec (`git commit -F <msg> -- <paths>`), push. Peers edit this tree; Astra is invisible to
  `ListAgents`, so `git pull` + `git status` immediately before every write.

## The owner's receipt — four clicks, works on any 1.1.0 colony

This is the cheap in-play check the verdict unlocked (checklist 151), and it is the only thing no desk control
can settle. Hand it to the owner with the build; it needs no expedition and no waiting:

1. Open a residence that is **full** (close spare bed slots on its panel until it reads full, e.g. 2/2).
2. Make sure that dome has **no other free beds** — close spare slots in its other residences too.
3. Click another colonist in that dome, then the full residence, and choose **Set Residence**.
4. **2/2 and the evicted colonist standing homeless = repaired. 3/2 = still broken.**

Then one boot with an `applied` log line, per the post-release rule.
