# BUILD C88 — Building Codes must apply to prefab-deployed buildings

Paste into a fresh session (any model; the owner picks). Written **2026-09-11** by `smr-bugfixpack-e6`.
**Staleness anchor: HEAD was `18fd4ce`.** Start with `git pull` + `git log --oneline -15`; the records win over
every specific below.

> ⚖️ **WHY.** A Paradox developer (`ivanassen`), in the reporter's Steam thread, 2026-09-11:
> *"Excluding prefabs is wrong, and will be fixed in the next patch - until then, please include it in your mod."*
> So the exemption is a confirmed defect by the game's own developers, and they have asked us to carry the fix
> until their patch ships. Entry: `docs/agent/bugs/C88.md`.
>
> ⚖️ **Owner ruling 2026-09-11: this build runs in a CLAUDE session** — broad hunts go to Codex/Astra, builds stay
> with Claude. The brief is still tool-neutral; nothing in it depends on a particular tool set.

## ⛔ GATE 0 — do not start until these two are true

1. **The release lane is clear.** `items.lua` and `metadata.lua` were the owner's uncommitted Mod Editor pack
   (v8) when this was written, owned by the release session. **H-10 makes this build require an `items.lua`
   entry**, so it collides head-on. Run `git status --short`: if either file is modified and uncommitted,
   **STOP and ask the owner / message the release session** (`ListAgents`). Do not edit them, do not stage them,
   do not work around them.
2. **The owner has ruled checklist 150 (b), or you default and say so.** Option **1** = both laws apply to prefab
   buildings (Lax's +50% and Strict's −30%), matching the developer's words and their coming patch — **this brief
   is written for option 1**. Option **2** = repair only Strict's missing −30%. If 150 (b) is unruled, build
   option 1, and say in one line in the commit body that you defaulted.

## 1 · The dossier — established 2026-09-11, all re-checkable on 1.1.0.403908

**The defect.** Both laws apply their maintenance change in a `ConstructionComplete` handler that opens by
discarding prefab-deployed buildings:
- Lax `Policy_BuildingCodesLax` — `Data/LawDef/LawDef-Efficiency.lua:696-706`; `maintenance_change` **+50**
  (`:687-690`); handler `:699-704`, first line `:700` `if from_prefab then return end`.
- Strict `Policy_BuildingCodesStrict` — `:904-914`; `maintenance_change` **−30** (`:895-898`); handler
  `:907-912`, first line `:908`, identical.
- Both then read `if not ActiveLaws[self.id] then return end`, require `IsKindOf(bld, "RequiresMaintenance")`,
  and call `bld:SetModifier("maintenance_resource_amount", self.id, 0, self:GetParameterValue("maintenance_change"), self.display_name)`.
- The flag: `local from_prefab = self.prefab` (`Lua/Buildings/ConstructionSite.lua:1729`), passed as
  `Msg("ConstructionComplete", bld, dome, from_prefab)` (`:1786`), declared `Data/MsgDef.lua:280`.
- Neither description mentions prefabs (`:692`, `:900`).

**⭐ The registration semantics decide the fix shape.** A preset's handlers are registered **by function
reference** into a global dispatch table: `RegisterMsgReactions` walks `self.msg_reactions` and calls
`RegisterMsgReaction(self, reaction.Event, reaction.Handler)` (`CommonLua/Reactions.lua:130-137`), which appends
the instance and the handler into `MsgReactions[event_id]` (`:469-479`). ⇒ **Editing
`LawDefs.Policy_BuildingCodesStrict.msg_reactions[1].Handler` after registration changes nothing** — the old
reference is already in the dispatch table. Re-registering means `ReloadMsgReactions()` (`:516-530`), which
**clears and rebuilds the table for every preset in the game**: far too wide a blast radius for this defect.

**⇒ RECOMMENDED SHAPE: an additive handler — `FIX_POLICY` §1 technique 2.** Vanilla's handler is a **verified
no-op for exactly the case we care about** (it returns at `:700`/`:908` before doing anything when
`from_prefab` is true), which is the precise shape §1's technique-2 note describes. So add our own
`OnMsg.ConstructionComplete(bld, dome, from_prefab)` that does nothing unless `from_prefab` is true, and then,
for each of the two laws, mirrors vanilla's own three conditions and its `SetModifier` call **with the law's own
id and its own `GetParameterValue`** — never a hard-coded 50 or −30.

**⭐ It degrades harmlessly when Paradox ships their fix.** `Modifiable:SetModifier` is keyed by `(id, prop)`:
it finds an existing modifier by id and, when the amounts are unchanged, does nothing at all
(`Lua/Modifiers.lua:181-204`). Both handlers would write the same id, prop and value, so double application is a
no-op in either order. ⛔ This is the argument for using **the law's own id**, not ours — but see §4, it has a
cost.

**⛔ EXISTING BUILDINGS CANNOT BE REPAIRED.** `from_prefab` occurs in exactly eight places in the whole tree
(the two handlers, `MsgDef.lua:280`, `ConstructionSite.lua:1729`/`:1786`, `Data/Trigger.lua:11`) and **nothing
stores it on the finished building**. A building already standing cannot be identified as prefab-deployed. ⇒ The
fix applies to buildings completed after it is installed, and that limitation must be stated in the entry, the
release note and the dev report. Do not invent a heuristic (shape, template, missing construction cost) to guess
— a wrong guess silently changes maintenance on buildings the law never touched.

**⚠️ AN OPEN QUESTION, AND POSSIBLY A VANILLA DEFECT.** The only clear-down of this modifier found is a
**savegame fixup**, `SavegameFixups.RemoveRepealedBuildingCodesMaintenance` (`Lua/Factions/Laws.lua:465-473`),
which sweeps `maintenance_resource_amount` by law id when the law is not active. `OnMsg.LawDeactivated`
(`:463`) only recalculates faction approval. **So: what removes the modifier when a player repeals Building
Codes mid-game?** Answer this before building. If nothing does, vanilla leaks the modifier on repeal — that is a
separate candidate to FILE (and a good thing to hand the developers), and our added modifiers would leak the
same way, which the owner must know before this ships.

## 2 · Scope fence

**IN:** one new module (`Code/Fix_<Name>.lua`), its `items.lua` entry (H-10) once Gate 0 clears, a desk harness,
a kit probe, the C88 entry update, the release-outbox entry, and a checklist item.
**OUT:** ⛔ the release lane (`items.lua`/`metadata.lua` while uncommitted, `RELEASE_OUTBOX.md` edits that
collide with a close in progress), the version number (H-02 — an agent NEVER sets it and NEVER opens the Mod
Editor), FR-1, the migration cluster (`MIGRATION_CLUSTER_CHECK.md`), and the repeal-leak question beyond FILING
it. Anything else interesting: **file it, do not fix it.**

## 3 · Build it

**S1 — settle the repeal question** (§1's open question). Read the enact/repeal path in `Lua/Factions/Laws.lua`
and `Lua/Factions/Legislature.lua`. Record the answer in C88; if vanilla leaks, file a new candidate entry.

**S2 — write the module.** `FIX_POLICY` §1 technique 2, §2 fail-safe, §2b manifest. Requirements:
- Fires only when `from_prefab` is truthy; returns immediately otherwise. Costs a live game nothing on the
  ordinary path.
- Mirrors vanilla's conditions per law: `ActiveLaws[law_id]`, `IsKindOf(bld, "RequiresMaintenance")`.
- Reads the percentage from the preset (`GetParameterValue("maintenance_change")`) so a balance change or
  another mod's edit is respected. ⛔ Never hard-code 50/−30.
- Uses `SetModifier` with the **law's** id, prop `maintenance_resource_amount` (see §4 before committing to it).
- **Branch guard, `FIX_POLICY` §2a — the probe IS the guard, and there is NO version check.** The module must
  decline where the shape it was written for is absent. Candidate `Require`/`test` shapes: both `LawDefs` entries
  exist, each carries a `msg_reactions` entry for `ConstructionComplete` whose `Handler` is a function, and
  `ConstructionSite.Complete` still passes a third argument. ⚠️ A behaviour probe that CALLS the shipped handler
  must be shown synchronous and side-effect-free on a stub first, and the `ActiveLaws` gate makes that awkward —
  if you cannot show it, use a shape `test` and say so in the header.
- **Manifest (`FIX_POLICY` §2b), machine-read by `tools/bodycheck.py`.** `SRC:` has no function body to hash
  here — follow `Fix_DustSicknessBiorobots.lua:158-164`'s `SRC: none` + `DEFECT@<file>:` form, and pin the
  DEFECT pattern on the shipped `if from_prefab then return end` **in the preset file**. ⭐ That pin is what makes
  `bodycheck` print DEFECT-GONE the day Paradox's patch lands — the retirement signal for this module.

**S3 — desk harness** `tools/desk_c88_prefab.py`, on the `deskbench` contract: extract the shipped handlers with
`tools/luafn.py`, load them under their real file name and line offset, load our module whole through the
Register/Require seam. Demands must include at least: (a) the shipped handler does nothing for a prefab building
while the law is active — the defect, reproduced; (b) our handler applies the correct modifier for a prefab
building; (c) it does nothing for a non-prefab building (vanilla's job); (d) it does nothing when the law is not
active; (e) it does nothing for a building that is not `RequiresMaintenance`; (f) **a simulated post-patch
vanilla** (handler without the early exit) plus ours yields exactly one modifier with the right value — the
graceful-degradation leg; (g) a negative leg that FAILS if the module is registered but never applied. A harness
with no leg that can fail is not a falsifier.

**S4 — kit probe** in the TestKit (a new wave file or the current one; follow `00_TestCore.lua`'s
`SMRTest.Register` contract). Prefer `behavior` kind — ⛔ **an `install` probe would SKIP on the retail game**
(`00_TestCore.lua:77-80`) and buy the owner nothing. An explicit `return "PASS", …` is required.

**S5 — the in-game recipe** for the owner's sitting (checklist 144 a): numbered clicks, plain language, one
copy-paste console line if any, and a control that would fail if the fix were absent. Draft shape: enact
Building Codes (Strict), place a building from a prefab, let it deploy, open its maintenance and compare against
the same building type built normally. Trace it to the shipped bodies first and ask **"what makes this
vacuous?"** — e.g. a building whose maintenance is 0 anyway proves nothing.

**S6 — verify.** `python tools/parsecheck.py` · `python tools/bodycheck.py --module <name>` ·
`python tools/sigcheck.py` · `python tools/deskbench.py` · `python tools/doccheck.py` GREEN (check
`git status docs/agent/bugs/` for a peer's files before any `--regen`).

**S7 — record and route.** C88 (status, a dated build section, the cannot-repair-existing limitation, the repeal
answer) · `items.lua` per H-10 **only once Gate 0 is clear** · a `### Pending` entry in
`perma/RELEASE_OUTBOX.md` (coordinate with the release session first) · a checklist item for the owner
(claim the number by message first) · a line for the developer reply in `docs/FIELD_REPORT_REPLIES.md` saying the
fix is in and will stand down when their patch lands. Commit `git commit -F <file> -- <explicit paths>`, push.

## 4 · The one design decision to put to the owner, not to settle quietly

**Which id does the modifier carry — the law's, or ours?**
- **The law's id** (recommended): identical to what vanilla writes, so their future patch and the existing
  savegame fixup (`Laws.lua:465-473`) both see it as their own, and repeal cleans it up.
  ⚠️ **Cost:** it is then indistinguishable from vanilla's, so the uninstall/save-rescue path cannot identify it
  as ours — check `FIX_POLICY` §3a and the rescue mod's residue list before choosing.
- **Our own id:** cleanly identifiable and removable, but it would **stack** with vanilla's modifier once
  Paradox ships their fix (two modifiers, two ids, double effect), and neither the repeal path nor the savegame
  fixup would clear it. ⛔ That is a player-visible harm, and it is the same failure shape as F-2.

State the recommendation, name the cost, and let the owner rule.

## 5 · What may NOT be claimed

- Not "tested" without a run; desk demands are **desk-controlled**, and only an attended sitting yields
  `tested-attended` (status words: `FIX_POLICY` / STATE "Rules in force").
- Not "works on existing saves" — §1 establishes it cannot; say "applies to buildings completed after install".
- Not "vanilla fixed it" until `bodycheck` prints DEFECT-GONE against the shipped preset.
- ⛔ No version check anywhere (`FIX_POLICY` §2a). The probe is the guard.
- Do not claim the repeal path is clean until S1 answers it. If unresolved, say **unverified** and file it.

## 6 · Stop conditions

- `items.lua`/`metadata.lua` still uncommitted → stop at Gate 0 and report.
- S1 finds vanilla leaks the modifier on repeal → stop, file it, and put it to the owner before shipping.
- The probe cannot be shown side-effect-free → fall back to a shape `test`, say so, and carry on.
- The fix needs more than an additive handler (e.g. the law's cost half turns out to matter) → report; do not
  escalate to a replacement or to `ReloadMsgReactions()` without the owner.

## 7 · Read path (file granularity)

`docs/agent/STATE.md` · `docs/agent/FIX_POLICY.md` (§1, §2, §2a, §2b, §3a, §4) · `docs/agent/bugs/C88.md` ·
`docs/FIELD_REPORT_REPLIES.md` ("Building codes vs prefabs", "Reply to the developer") ·
`docs/PLAYTEST_CHECKLIST.md` → item 150 · `Code/00_Core.lua` (`Register`, `Require`, `WhenActive`, `DataPatch`
at `:142`, `:228`, `:315`) · `Code/Fix_DustSicknessBiorobots.lua` (manifest + preset-patch precedent) ·
`Code/Fix_ScanDowngrade.lua` + `tools/desk_c86_scan_downgrade.py` (the most recent build+harness pair) ·
`../SMR-BugFixPack-TestKit/Code/00_TestCore.lua` · game source `Data/LawDef/LawDef-Efficiency.lua`,
`Lua/Buildings/ConstructionSite.lua`, `Lua/Factions/Laws.lua`, `Lua/Factions/Legislature.lua`,
`Lua/Modifiers.lua`, `CommonLua/Reactions.lua`, `Data/MsgDef.lua`, `Data/Trigger.lua`.

## 8 · The live todo list — required, and required to stay current

Build it before starting, **one item per commit-and-verify unit** (S1 the repeal read; S2 the module; S3 the
harness; S4 the probe; S5 the recipe; S6 the verification run; S7 the records). Mark each complete the moment it
completes, one in progress at a time, and rewrite the list when reality diverges. The owner reads it to decide
when to step in. ⚠️ **Stale-probe gate:** if you end up recording any in-game result,
`grep -rln "TEMPORARY" Code/ ../SMR-BugFixPack-TestKit/Code/` must be zero, in the list, before results.

## 9 · This brief deletes itself

One-off. When the module is built, verified, recorded and the checklist item filed, `git rm` this file in the
same commit and remove its row from `prompts/README.md`. Git history keeps it.
