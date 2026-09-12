# BUILD C85 + C88 + C89 — one session, three modules, all for v10

**Written 2026-09-12 by `smr-bugfixpack-d0` at the owner's ask.** Paste into a fresh **Claude** session
(owner ruling 09-11: builds stay with Claude; hunts go to Codex). **Staleness anchor: HEAD was `d537c12`.**
`git pull` + `git log --oneline -15` + `git status --short` + `ListAgents` first; the records win over every
specific here. Open a **live todo list** from the first tool call, one item per S-step below, and keep it
current — the owner reads it to decide when to step in. 🛑 Stop and report a concern at any point; a stop is
cheaper than a wrong ship.

> ⚠️ **CONCURRENCY (owner, 2026-09-12): `prompts/SURFACE_AUDIT_FABLE.md` may be running in a sibling session at the same
> time, in the same checkout.** It owns `reports/SURFACE_AUDIT_2026-09-12.md` and touches no `Code/`, `items.lua` or
> outbox. Shared: `docs/PLAYTEST_CHECKLIST.md` (claim your item number by message first), `docs/archive/SESSION_LOG.md`,
> `prompts/README.md`. `git pull` before every shared-doc write, commit by pathspec only, and keep each `Code/` module and
> its `items.lua` entry in the SAME commit so the sibling never sees a MODULE SETS mismatch. Its F31 verdict does not
> change anything you build.

## ⚖️ The rulings this prompt carries (owner, 2026-09-12)

| item | ruling | where the detail lives |
|---|---|---|
| **C85** clogged producer | **Build the SWEEP ONLY — the safest version.** No `Duration` DataPatch, no UI. Checklist 154 is settled by this line. | `prompts/CLOGGED_BUILD.md` (dossier, fix shape, interlocks, A/B) · `bugs/C85.md` |
| **C88** Building Codes vs prefabs | **Build it.** Shape = **option 1** (both laws apply to prefab buildings, Lax +50 % and Strict −30 %, exactly as their text says and as the developer will ship). Modifier id = **the law's own id** (degrades to a no-op the day Paradox's patch lands; repeal and the savegame fixup see it as theirs). ⚠️ Both are the brief's recommendations, adopted by the owner's "build it"; **if the owner has written a different choice at the top of this file before you start, that wins.** | `prompts/C88_PREFAB_BUILD.md` (dossier, registration semantics, S1–S7, §4 trade) · `bugs/C88.md` · checklist 150 |
| **C89** faction unemployment dislike on tiny domes | **Build it — a JUDGMENT CALL** (owner, 09-12, third item added the same day). Apply the Justice Movement's own `#obj.labels.Colonist >= 10` dome gate to the four unguarded **unemployment** dislikes (Prosperity, Mars Democratic Party, Workers' Party, New Sol) **and the three unguarded homeless twins** (MDP, Workers', New Sol). ⚠️ The homeless half is this brief's inclusion on the same precedent — the owner ruled on unemployment; if the owner strikes homeless at the top of this file, build unemployment only. | §1 C89 below · `bugs/C89.md` (all lines, both trees) · checklist 157 |
| release | All three ride **v10**, behind `prompts/SURFACE_AUDIT_FABLE.md` and the still-needed batch (`perma/RELEASE_OUTBOX.md` → Held). Each gets its own `### Pending` entry; count impact **+1 each**; C89 is a **judgment-call row** (FAQ count three → four). | `perma/RELEASE.md` |

> **Owner override slot (edit before firing, or leave blank):**
> C88 shape: `option 1` · C88 modifier id: `the law's id` · C89 scope: `unemployment + homeless`

## 0 · Gates — all three were TRUE at `d537c12`; re-check, do not assume

1. **The release lane is clear.** `git status --short` shows `items.lua` and `metadata.lua` unmodified (v9 closed
   out 09-12, comments restored). If either is modified and uncommitted, **stop and ask** — H-10 makes both
   builds need an `items.lua` entry, and a peer's writeback is not yours to touch.
2. **No peer is editing `Code/`, `items.lua` or the outbox.** `ListAgents` + `git status`; message overlapping
   peers before shared-doc writes; commit by pathspec only.
3. **Stale-probe gate** binds only if you launch the retail game (`DISPATCH.md` §0.4). The desk work here
   launches nothing.

## 1 · Order of work — C85, then C89, then C88

C85 is the smaller module and both reporters are stranded in it today; C89 is a data-only gate with no open
question; C88 has an open sub-question (S1, the repeal path) that may need the owner. Finish, verify and record
each before opening the next, so a stop on a later one still ships the earlier ones.

### C85 — the sweep (follow `CLOGGED_BUILD.md` §1–§3 and §5; §2's Duration paragraph is moot)
- **S1** Read `bugs/C85.md`'s dated 2026-09-11 "mechanism resolved" section — the entry is the truth.
- **S2** Module: on load + daily, `AllMapsForEach` producers with `exceptional_circumstances` true **and**
  `TGetID(exceptional_circumstances_reason) == 789863173059`; repair with the game's own
  `Setexceptional_circumstances(false)`. **Two interlocks**, both read-only `GameVar`s: skip a building whose
  `BuildingClogged` story bit is active now (`g_StoryBitActive`) or whose `BuildingClogged_1_FixAfterStorm` is
  armed and pending (`g_StoryBitStates`). ⛔ Key on this one reason id; do not generalise.
- **S3** The three desk checks in `CLOGGED_BUILD.md` §3 (reason survives save/load as a `T`; the exact pending
  `g_StoryBitStates` shape; the narrow key).
- **S4** Desk harness `tools/desk_c85_clogged.py` on the `deskbench` contract, with at least: stuck building →
  cleared; popup-active building → untouched; fix-after-storm-pending building → untouched; a different
  reason id → untouched; a negative leg that FAILS if the module registers but never applies.
- **S5** Kit probe (`behavior` kind; an `install` probe SKIPs on retail, `00_TestCore.lua:77-80`).
- **S6** Branch guard `FIX_POLICY` §2a: a behaviour/shape probe, never a version check. Manifest §2b
  (`SRC:` + `DEFECT:` via `tools/bodycheck.py --pin`).

### C89 — the dome-size gate on seven faction dislikes (dossier: `bugs/C89.md`, every line on both trees)
- **S1 — read the entry**, all three dated sections. The defect: five factions carry the identical per-dome
  test `#obj.labels.Unemployed * 100 >= 10 * #obj.labels.Colonist` (Homeless twin on four), and only the Justice
  Movement gates it with `#obj.labels.Colonist >= 10 and …` (`Data/FactionDef/JusticeMovement.lua:104`, `:129`
  @1.1.0). Unguarded: `ProsperityForMars.lua:225`, `MarsDemocraticParty.lua:88` + `:107`, `WorkersParty.lua:114`
  + `:133`, `NewSol.lua:47` + `:66`. Like ids: `ProsperityUnemployment`, `UtopiaUnemployment`,
  `CollectiveUnemployment`, `NewSolUnemployment`; `UtopiaHomeless`, `CollectiveHomeless`, `NewSolHomeless`.
- **S2 — the registration semantics decide the shape, and here they are favourable.** `FactionLikeDomes:CountDome`
  reads `self.DomeFilter.eval` **at call time** (`Lua/Factions/FactionDef.lua:857`), so replacing that field on the
  live like object takes effect at the next hourly recalc — unlike C88's message reactions, which are captured by
  reference. ⇒ Shape: a `DataPatch` (`Code/00_Core.lua`, the seam the C88 dossier cites) that, for each of the
  seven likes found by `Id` under `FactionDefs[<faction>].likes`, wraps the existing `DomeFilter.eval`:
  `local orig = like.DomeFilter.eval; like.DomeFilter.eval = function(obj) return #obj.labels.Colonist >= 10 and orig(obj) end`.
  Keep the original in a closure; never rewrite the expression; never touch Justice. **Verify the call-time read
  on the shipped body before writing** (that is the module's §2a probe: the like exists, `DomeFilter.eval` is a
  function, and Justice's own eval still carries the guard text — the precedent this fix copies).
- **S3 — branch guard and manifest.** `FIX_POLICY` §2a: no version check; decline if any of the seven likes is
  missing or its `DomeFilter` is not a `ScriptConditionList` with an `eval` function. §2b: `SRC: none` +
  **seven `DEFECT@Data/FactionDef/<file>.lua:` pins**, one per unguarded expression, on the bare
  `return (#obj.labels.Unemployed * 100 >= 10 * #obj.labels.Colonist)` / `Homeless` line **without** a
  `Colonist >= 10` prefix — so `bodycheck` prints DEFECT-GONE the day the developers add the gate, and the module
  stands down per like (a like whose shipped eval already carries `>= 10` is skipped, not double-gated).
- **S4 — save-safety** (`FIX_POLICY` §3a): nothing is persisted; the wrapped eval lives only in the preset object;
  removal of the mod restores the shipped behaviour at the next recalc. A dislike that disappears fires no
  notification (`Factions.lua:672-678` notifies additions only). Say so in the entry.
- **S5 — desk harness** `tools/desk_c89_faction_gate.py` on the `deskbench` contract, with fake dome objects
  carrying `labels.Colonist` / `labels.Unemployed` / `labels.Homeless` arrays: (a) dome of 3 with 1 idle: shipped
  eval true, patched false — the defect, reproduced; (b) dome of 10 with 1 idle: both true; (c) dome of 30 with 2
  idle: both false; (d) Justice's eval byte-for-byte untouched (control); (e) each of the seven ids patched,
  none other; (f) a simulated post-patch vanilla (guard already present) → the module skips that like; (g) a
  negative leg that FAILS if the module registers but never applies.
- **S6 — kit probe**, `behavior` kind: call each patched `DomeFilter.eval` on a fake 3/1 dome and a 10/1 dome.
- **S7 — 🎮 OWNER-FLAGGED FOR IN-GAME A/B, OBSERVED AT THE KEYBOARD (09-12): "I want to observe it; simple enough
  to spin up a one-shot colony."** Write the recipe for a **fresh one-shot colony**, not the owner's large saves:
  1. What the colony needs before the read: a first dome with colonists, the Martian Assembly built (40 Concrete /
     20 Metals / 20 Polymers, a dome spire, no research), and **one of the four factions active** — name the
     console read (`g_FactionsHolder.active_factions`) and what to do if none of the four is active (which sponsor
     or founder choices push supporters toward Prosperity / Workers' Party; or the cheat that seats a faction, if
     one exists — find it, do not guess).
  2. The A/B object: a **second, small dome** with three adult colonists moved in and **no workplace inside it**
     (or a first dome kept under ten colonists with one worker made idle). Give the copy-paste line that makes a
     selected colonist idle (`SelectedObj:SetWorkplace(false)` — verify it sticks past `UpdateWorkplace`, or give
     the line that does) and one that reads the dome's counts (`#SelectedObj.labels.Colonist`,
     `#SelectedObj.labels.Unemployed`).
  3. **Fix-off leg first, then fix-on, same save**, across one game hour each: fix-off — at the hour the faction
     panel lists "Domes with more than 10% Unemployment" and the dislike notification fires; fix-on — neither,
     while the dome still reads 3 colonists / 1+ idle (the control that proves the read is not vacuous). Name how
     the owner turns the one module off for the A leg (the precedent is the F119 fix-off leg, checklist 149).
  4. One copy-paste read of the like's current value from the stored approval data, so the owner can quote a
     number, not a screenshot (memory rule: read console output from the flushed log, prefixed).
  ⚠️ Trace the whole recipe for vacuity before it goes in the checklist: the faction must be **active**, the idle
  colonists must be adults who `CanWork()`, and the hour boundary must actually pass with the panel open. Say
  the warm-up cost plainly (a one-shot colony is a 20–30 minute organic warm-up, not a saved fixture).
  `tested-attended` for C89 is the owner's to grant after this leg; nothing else grants it.
- ⚖️ **FLAGGED AS A JUDGMENT CALL EVERYWHERE (owner, 09-12) — this is not a repair of a code error, and every
  surface must say so the way F40 (Biorobots) and F73 (asteroid vacuum) do:** the site row uses the
  `??? question` block with "— *judgment call*" in the headline and the "⚠️ Worth knowing: this one is a judgment
  call" paragraph; the FAQ judgment-call count goes three → four in all three places
  (`PUBLIC_SURFACE_SWEEP.md` §6); the entry heading, the outbox entry, the `last_changes` bullet and the module's
  in-game registered title all carry "judgment call"; the card's judgment-call sentence is updated if it lists
  them by name. Nothing here may be worded as "the game was wrong".
- **Public surface, in the voice rule:** a **judgment-call** row (the FAQ count goes three → four): what you saw —
  a faction turning on you over "unemployment" in a dome of a handful of colonists that was still being built,
  with no unemployed in the colony; what was wrong — four factions count any dome however small, while the
  Justice Movement's identical dislike waits until a dome has ten colonists; after the fix — all five use the
  same ten-colonist rule, for homelessness too. No hedging words; the hourly sampling is not ours and is not
  mentioned on the row.

### C88 — the additive handler (follow `C88_PREFAB_BUILD.md` §1–§3; §4 is ruled above)
- **S1 — settle the repeal question first** (`C88_PREFAB_BUILD.md` §1, last paragraph): what removes the
  Building Codes maintenance modifier when the player repeals the law mid-game? Read `Lua/Factions/Laws.lua`
  and `Legislature.lua`. **If vanilla leaks it on repeal: file a new candidate entry, put it in the checklist
  item, and CONTINUE the build** — with the law's id our modifier follows vanilla's exactly, so we add no new
  leak shape; say so in the entry. (This softens the brief's "stop" into "file and tell", because the id
  ruling removes the reason for the stop.)
- **S2** Module per `C88_PREFAB_BUILD.md` S2: fires only when `from_prefab` is truthy; mirrors vanilla's three
  conditions per law; reads `GetParameterValue("maintenance_change")` (⛔ never hard-code 50/−30);
  `SetModifier` with the law's id on `maintenance_resource_amount`. Manifest: `SRC: none` +
  `DEFECT@Data/LawDef/LawDef-Efficiency.lua:` pinned on `if from_prefab then return end` — the DEFECT-GONE pin
  is this module's retirement signal for the day Paradox's patch lands.
- **S3** Desk harness `tools/desk_c88_prefab.py` with the seven legs listed in the brief (a)–(g), including
  the simulated post-patch vanilla leg that must yield exactly one modifier.
- **S4** Kit probe, `behavior` kind.
- **S5** ⛔ State plainly in the entry, the outbox entry and the reply draft: **buildings already standing
  cannot be repaired** — `from_prefab` is not stored on the finished building; the fix applies to buildings
  completed after install. No heuristic.

## 2 · Verify (all three modules, one pass)

`python tools/parsecheck.py` · `python tools/bodycheck.py` (all three) · `python tools/sigcheck.py` ·
`python tools/deskbench.py` · `python tools/doccheck.py` GREEN, counts from `--emit-counts` (expect modules
46 → 49, `Code/*.lua` 47 → 50 **before** the still-needed retirements land; the release lane re-derives).
Check `git status docs/agent/bugs/` for a peer's files before any `--regen`.

## 3 · Record and route

- Entries `bugs/C85.md`, `bugs/C88.md` and `bugs/C89.md`: status word only as far as the evidence goes (`fixed`,
  desk-controlled; never a playtest word), a dated build section each, C88's cannot-repair-existing limitation and
  the repeal answer, C89's judgment-call marker.
- `items.lua` entries (H-10). ⛔ H-02: never `version`, never the Mod Editor.
- `perma/RELEASE_OUTBOX.md`: **three `### Pending` entries** (the shape of the *Released in v8* entries), each
  with its one-line `last_changes` bullet in the owner's list style — plain, one line per fix, tagged
  `NEW`. ⚖️ **Voice rule** (top of `reports/still-needed/WORDING_RULED.md`): plain for players, precise for
  the developers, no hedging words; C88's "applies to buildings completed after this update" is a scope
  statement, not a hedge — keep it.
- **One checklist item** (claim the number by message first): the attended recipes for both, **one boot**,
  numbered clicks, copy-paste console lines fenced, a control per fix that fails when the fix is absent:
  - C85: `CLOGGED_BUILD.md` §4 **A/B #1** (force the end state on a selected producer; fix-off stays dead
    across a sol + save/reload; fix-on clears it). A/B #2 is optional and must not gate anything.
  - C88: `C88_PREFAB_BUILD.md` S5 (enact Strict, deploy a prefab, compare maintenance against the same
    building built normally; pick a building whose maintenance is non-zero or the read is vacuous).
  - C89: S7 above (a new small dome with three idle adults, fix-off vs fix-on across one game hour).
  It can share the owed ck144 (a) boot.
- `docs/FIELD_REPORT_REPLIES.md`: a line for the Building Codes thread (the developer's own thread) saying the
  fix is in the next update and stands down when their patch lands; a line for the clogged-producer reporters
  saying already-stuck buildings recover on load; a line added to the C89 reporter draft (2026-09-12 section)
  saying the next update applies the same ten-colonist rule to all five factions. **Drafts only; the owner posts.**
- `prompts/README.md`: remove the three rows (this file, `CLOGGED_BUILD.md`, `C88_PREFAB_BUILD.md`).
- Commit `git commit -F <msg> -- <explicit paths>`; push. **`git rm` all three prompts in the final commit,**
  naming their graves in the SESSION_LOG entry.

## 4 · What may NOT be claimed

Not `tested` without a run · not "works on existing saves" for C88 · not "vanilla fixed it" until `bodycheck`
prints DEFECT-GONE · no version check anywhere · no status word here is a playtest grant.

## 5 · Stop conditions

`items.lua`/`metadata.lua` uncommitted → stop at Gate 0 · C88 needs more than an additive handler (the cost half
matters, or `ReloadMsgReactions` looks necessary) → report, do not escalate · a probe cannot be shown
side-effect-free → shape `test`, say so, continue · anything else interesting → **file it, do not fix it.**

## 6 · Read path

`docs/agent/STATE.md` · `docs/agent/FIX_POLICY.md` §1 §2 §2a §2b §3a §4 · the two dossier prompts named above ·
`bugs/C85.md`, `bugs/C88.md` · `Code/00_Core.lua` (`Register`, `Require`, `WhenActive`) ·
`Code/Fix_ScanDowngrade.lua` + `tools/desk_c86_scan_downgrade.py` (the most recent build + harness pair) ·
`Code/Fix_TradeRocketFuelRefresh.lua` (the most recent load-heal precedent, for C85's sweep) ·
`../SMR-BugFixPack-TestKit/Code/00_TestCore.lua` · `perma/RELEASE_OUTBOX.md` · game source per the two briefs.
