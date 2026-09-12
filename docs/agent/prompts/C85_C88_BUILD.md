# BUILD C85 + C88 — one session, two modules, both for v10

**Written 2026-09-12 by `smr-bugfixpack-d0` at the owner's ask.** Paste into a fresh **Claude** session
(owner ruling 09-11: builds stay with Claude; hunts go to Codex). **Staleness anchor: HEAD was `d537c12`.**
`git pull` + `git log --oneline -15` + `git status --short` + `ListAgents` first; the records win over every
specific here. Open a **live todo list** from the first tool call, one item per S-step below, and keep it
current — the owner reads it to decide when to step in. 🛑 Stop and report a concern at any point; a stop is
cheaper than a wrong ship.

## ⚖️ The rulings this prompt carries (owner, 2026-09-12)

| item | ruling | where the detail lives |
|---|---|---|
| **C85** clogged producer | **Build the SWEEP ONLY — the safest version.** No `Duration` DataPatch, no UI. Checklist 154 is settled by this line. | `prompts/CLOGGED_BUILD.md` (dossier, fix shape, interlocks, A/B) · `bugs/C85.md` |
| **C88** Building Codes vs prefabs | **Build it.** Shape = **option 1** (both laws apply to prefab buildings, Lax +50 % and Strict −30 %, exactly as their text says and as the developer will ship). Modifier id = **the law's own id** (degrades to a no-op the day Paradox's patch lands; repeal and the savegame fixup see it as theirs). ⚠️ Both are the brief's recommendations, adopted by the owner's "build it"; **if the owner has written a different choice at the top of this file before you start, that wins.** | `prompts/C88_PREFAB_BUILD.md` (dossier, registration semantics, S1–S7, §4 trade) · `bugs/C88.md` · checklist 150 |
| release | Both ride **v10**, behind `prompts/SURFACE_AUDIT_FABLE.md` and the still-needed batch (`perma/RELEASE_OUTBOX.md` → Held). Each gets its own `### Pending` entry; count impact **+1 each**. | `perma/RELEASE.md` |

> **Owner override slot (edit before firing, or leave blank):**
> C88 shape: `option 1` · C88 modifier id: `the law's id`

## 0 · Gates — all three were TRUE at `d537c12`; re-check, do not assume

1. **The release lane is clear.** `git status --short` shows `items.lua` and `metadata.lua` unmodified (v9 closed
   out 09-12, comments restored). If either is modified and uncommitted, **stop and ask** — H-10 makes both
   builds need an `items.lua` entry, and a peer's writeback is not yours to touch.
2. **No peer is editing `Code/`, `items.lua` or the outbox.** `ListAgents` + `git status`; message overlapping
   peers before shared-doc writes; commit by pathspec only.
3. **Stale-probe gate** binds only if you launch the retail game (`DISPATCH.md` §0.4). The desk work here
   launches nothing.

## 1 · Order of work — C85 first, then C88

C85 is the smaller module and both reporters are stranded in it today; C88 has an open sub-question (S1, the
repeal path) that may need the owner. Finish, verify and record C85 before opening C88, so a stop on C88 still
ships C85.

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

## 2 · Verify (both modules, one pass)

`python tools/parsecheck.py` · `python tools/bodycheck.py` (both modules) · `python tools/sigcheck.py` ·
`python tools/deskbench.py` · `python tools/doccheck.py` GREEN, counts from `--emit-counts` (expect modules
46 → 48, `Code/*.lua` 47 → 49 **before** the still-needed retirements land; the release lane re-derives).
Check `git status docs/agent/bugs/` for a peer's files before any `--regen`.

## 3 · Record and route

- Entries `bugs/C85.md` and `bugs/C88.md`: status word only as far as the evidence goes (`fixed`, desk-
  controlled; never a playtest word), a dated build section each, C88's cannot-repair-existing limitation and
  the repeal answer.
- `items.lua` entries (H-10). ⛔ H-02: never `version`, never the Mod Editor.
- `perma/RELEASE_OUTBOX.md`: **two `### Pending` entries** (the shape of the *Released in v8* entries), each
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
  It can share the owed ck144 (a) boot.
- `docs/FIELD_REPORT_REPLIES.md`: a line for the Building Codes thread (the developer's own thread) saying the
  fix is in the next update and stands down when their patch lands; a line for the clogged-producer reporters
  saying already-stuck buildings recover on load. **Drafts only; the owner posts.**
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
