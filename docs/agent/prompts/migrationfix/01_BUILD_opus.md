# 01 · BUILD (opus) — the migration audit's code actions: repair F59, then build F60's retirement

**Link 1 of 2 in the `migrationfix` mini chain** (map: `migrationfix/README.md`). Written **2026-09-11** by
`smr-bugfixpack-cb`. **Staleness anchor: HEAD was `33b9f8e`.**
Start with `git pull` + `git log --oneline -15`; the records win over every specific below.
⚠️ **Keep a live todo list from your first tool call** — the owner reads it to decide when to step in.

> ⚖️ **OWNER, 2026-09-11: ship tonight, as a mini chain — Opus builds, Fable audits after.**
> ⚖️ **ck151 (e) RULED: 1.0.7 stays frozen** — no new legacy build.

> 🔗 **YOU ARE THE EXECUTOR, NOT THE CERTIFIER.** `02_AUDIT_fable.md` is an adversarial backward QA with fresh
> context that trusts nothing you write, and **the owner's upload happens AFTER it, not between**. That ordering
> is what makes "build from the report as-is" safe: a refuted build costs a revert, not a shipped defect. So
> **build, record, and hand over — do not grade your own work**, and do not soften a finding to make the set look
> complete. Your close-out feeds link 02 (see "Handoff" at the foot of this file).

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

## ⛔ "Build it as Astra wrote it" holds for F60 — NOT for F59

The owner's instruction is to build from the audit's report as-is. That is correct for **F60**, whose retirement
is exactly what the report proposes, and link 02 checks it after.

**It is NOT correct for F59, and this is measured, not an opinion.** The report proposes an *expedition-home
exclusion*. That fixes A1 below and **does nothing at all for A2** — a second harmful caller the report never
saw, desk-controlled 8/8 in `tools/desk_f59_interact.py`, reachable by an ordinary player action, and present on
both game branches since the module was written. Building the report's shape as-is would ship a fix that leaves
the more reachable of the two harms in place. **So: build F59 against the dossier below (`bugs/F59.md`, last two
sections), which is the report PLUS the independent re-derivation that found A2.**

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

## B · F60 retirement — build it as the report proposes, and SHOW YOUR TRACE

Report §7 recommends retiring `Fix_DomeFreeSpaceMismatch`. **Build that.** The verdict is single-sourced from the
audit and nobody has checked it — which is precisely what link 02 is for, so do not re-audit it yourself and do
not stall the night on it.

**What you must produce alongside the removal, because link 02 will be checking exactly this** (house rule: a
REMOVE verdict needs the replacement traced): name the vanilla body that now does the job, name every residual
the module still changes, and grep where any vanished name went — a rename reads as "gone" and has nearly
retired a live fix before. Write the trace into `bugs/F60.md` as claims link 02 can falsify, not as a summary.

**Two hard gates, and both stop B without touching A:**
1. **H-10 / release lane.** Removing a module rebuilds `items.lua` + `metadata.lua`'s `code` list via `SaveDef`,
   which collides head-on with the owner's uncommitted v8 pack. If that lane is not clear, **ship A alone and
   leave B for the next cycle.**
2. **If the trace collapses in your own hands** — the replacement is not there, or the module still does
   something live — **stop, ship A alone, and say why.** Do not bundle a removal you cannot trace into a release
   to make the set look complete. Link 02 is a check, not a safety net you can lean on.

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

## Handoff — what link 02 needs from you (self-consuming queue)

Append a **HANDOFF** section to `migrationfix/README.md` in your close-out commit, then `git rm` **this file**
(`01_BUILD_opus.md`) in the same commit — the chain consumes its own prompts. The handoff carries, in this order:

1. **Disagreements first.** Anything in Astra's report you found wrong, stale or unsupported WHILE building —
   including "I could not build B's trace". Say it plainly; link 02 starts from your disagreements.
2. **What you built**, per item, as claims link 02 can falsify — not a summary. For A: the guard's shape, and the
   per-caller answer for all 11 call sites. For B: the replacement trace.
3. **What you did NOT do and why** — skipped items by NAME, never a total.
4. **Every command whose output a fresh session would need to re-read**, with its result (harness pass counts,
   `doccheck --emit-counts`, `bodycheck`, `parsecheck`).
5. **The one thing you are least sure of.** The executor is the wrong person to certify their own rewrites —
   naming your weakest point is worth more to link 02 than a clean bill of health.

⛔ **Do not stamp a playtest status word.** `tested-attended` is the sitting's. ⛔ **Do not upload, and do not
tell the owner it is ready to upload** — the upload gate is AFTER link 02.
