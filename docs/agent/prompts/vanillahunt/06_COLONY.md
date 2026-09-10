# 06 — the colony: colonists, domes, services, rockets, disasters, story, save/load

⛔ ONE-SHOT: this file `git rm`s itself on close-out (README rule 2).
Model: Opus · owner needed: no · after 02; independent of 03, 04, 05, 07.

> 🎯 The largest hand-written files in the diff live here — `Colonist.lua`
> (~298 declarations), `Dome.lua` (~281), `Building.lua` (~254),
> `UniversalRocket.lua` (~239), `_fixup.lua` (~165), `SA_Gameplay.lua` (~182)
> — and the two 1.1.0 defects in our KEEP modules (`F117`, `F118`) were both
> here. ⚠️ **`_fixup.lua` / `SavegameFixups` is weighted highest inside this
> link**: a save-breaking change is the worst class for a player, `EF-079`
> already says 1.0.7 saves cannot load at all, and the fixups the developers
> wrote for the migration are the least-tested code in the tree.

## 0 · Open in this order

`git log --oneline -10` · `git pull` · `ListAgents` · `README.md` (§2, §3, §4)
· `STATE.md` · `TRIAGE.md` §3 "06" · `CALLERS.tsv` rows in your files ·
`PACK_1_1_0_REVERIFICATION.md` §1 REMOVE rows for your systems ·
`VANILLA_FIX_QA.md` §0 · `bugs/F117.md`, `F118.md`, `C54.md` (a refuted filing —
the reasoning error to not repeat) · `facts/INDEX.md` (`EF-005`, `EF-009`,
`EF-017`, `EF-056`, `EF-079`, `EF-080`) · your inbox. Pin check.

## 1 · 🗒 Live todo list, from your first action

## 2 · Order of reading — binding

1. **Save/load first.** Every changed or added function in `_fixup.lua`,
   `SavegameFixups.*`, `Persist*`, and every `PersistGatherPermanents` /
   `OnMsg.LoadGame` / `PostLoad` body in your files. For each fixup: what
   state does it rewrite, what did 1.0.7 write there, is it idempotent, does
   it run once (`SavegameFixups` are versioned — read the mechanism in
   `CommonLua`, cite it) or every load, and what does it do to a save that
   never had the field (a colony started on 1.1.0). ⭐ The hotfix-2 link 08
   found the developers' own `RefreshAstrogeologistExtractorBonus` fixup
   narrowing on `Percent == 20` where the archived 1.0.7 pays 10 — a vanilla
   observation noted inside OUR entry (`bugs/F95.md`, grep `Percent == 20`)
   and in `prompts/hotfix2/README.md` row 08 ("NOT established, an
   intermediate branch is likely"), never filed as its own entry: file it as a
   `C` entry with the route, or refute it, first.
2. **(h)** retired-module targets in your systems, neighbourhood read (05's
   rule 1, same discipline).
3. **(b′)** rows — `F117`'s own family: `ChooseDome`'s vanilla callers were
   enumerated by 02's `CALLERS.tsv`; read each `same` caller's body. Then every
   other changed-signature function in `Colonist`, `Dome`, `Residence`,
   `Workplace`, `Service*`, `*Rocket*`, `Cargo*`.
4. **(a)/(b)** `WORTH-READING` rows, biggest files first; then **(i)** guards;
   then **(f)** new functions; then a 30-row `CHURN` spot check.
5. **Story/scenario/mystery Lua** last — `Lua/Mysteries` 11 files,
   `Lua/Scenario` 26, `Sequences/SA_Gameplay.lua`: the Lua side only; the 514
   `StoryBit` presets are 03's, and 03's hand-off names the consumers you
   should cross-check.

## 3 · Method

As 05 §3. The executing-falsifier template closest to this link is
`tools/desk_f117_argshape.py` (a two-tree run of `Community:GetScoreFor` on a
stub) — reuse its harness shape for any scoring/choice body. Recipe derived
separately from the diagnosis (README §3): F117's own first control was wrong
for exactly the reason that rule exists. ⛔ `C54`'s lesson: before filing any
unguarded read, count the unguarded siblings and check `EF-005`.

## 4 · Scope fence

**In:** 02's "06" rows, (h) seeds, save/load, filing, `TRIAGE.md` "06"
coverage. **Out:** `dlc-adjacent` rows (04 — and the colonist-consumption /
service-building seam is mostly there, so your colonist set is the NON-food
remainder; say so in coverage); trains/landscaping/construction rows in
`Building.lua` (05 by class prefix); `CommonLua` persistence machinery itself
(07 — you cite it, 07 reads it); any `Code/` edit or module.

## 5 · Stop conditions

Above ~500 `WORTH-READING` rows at the START, split up front
(`06b_COLONY_ROCKETS.md`: rockets/cargo/trade/disasters) · a fixup finding
that needs a 1.1.0-started save AND a migrated save to settle — route as a
checklist rider (`EF-079`: a migrated 1.0.7 save does not exist on 1.1.0;
say what CAN be tested) · a finding implies a KEEP module is wrong (hotfix-3
checklist item, not yours).

## 6 · What may NOT be claimed

`tested`. That a fixup is safe because it ran on the rig (the rig's 1.1.0
colonies are fresh; nothing migrated). That an unread `CHURN` row is safe.
That a story-bit consumer is unaffected without 03's row for the preset it reads.

## 7 · Close-out

Outbox to 05/07 (rows that turned out theirs), 04 (seams found), 99 (findings
with routes, NOT-reached, spot check, drift). Strike your row. Explicit-path
`git add`: `TRIAGE.md`, `bugs/C##.md` + `bugs/INDEX.md`, README, 05, 07, 99
(and 04 if not yet consumed); `git rm` this file. doccheck GREEN, commit `-F`,
push.

## Notes from upstream

*(authoring session, 2026-09-09)* `F118`'s mechanism — 1.1.0's
`LayoutConstructionController:Activate` registering the layout controller in
`s_ConstructionControllerDeleteOnLoad` — is a class (f)+(c) change in
construction whose side effect reached OUR module; the vanilla question nobody
asked is whether any VANILLA `Deactivate` caller resets that flag the same
way. It sits on the 05/06 boundary (construction × save/load); 06 owns it
because the effect is on load. Route to 05 if the read goes the other way.
