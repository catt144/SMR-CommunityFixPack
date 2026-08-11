# Chain — corun-pt15 (the PT-15 mystery sitting; 3 prompts, self-consuming)

**Why this chain exists.** The owner built the PT-15 fixture themselves
(2026-08-11: *"I setup a basic save for the PT-15 with the mystery selected"*,
saved as **`PT-15.savegame.sav`**, 45.6 MB, St. Elmo's Fire picked at new-game
setup, **tech NOT cheat-researched**, colony new-ish/small) and ordered the
next chain built around it plus whatever rides well on a new-ish colony.
⭐ **Fixture state, owner report 2026-08-11 (a CLAIM, and the hedge is theirs):**
*"The save just came out of the founder stage I think."* ⇒ the mystery's
`WaitMsg("ColonyApprovalPassed")` has been released and the **10–20 sol sleep is
running**. ⛔ The game keeps NO record of when approval fired — `-1` overwrites
the timer (`ColonyViability.lua:95-97`) and `OnMsg.ColonyApprovalPassed` removes
the `FounderStageDuration` notification (`Legislature.lua:1522-1523`) — so this
claim can never be upgraded to a measurement after the fact, and the payload
carries it as `CP15.approval_claim` with that stated. The *state* is confirmable
(`g_ColonyNotViableUntil` must read `-1`) and `CP15.MysteryWhere()` prints a
refutation line if it does not. **Planning consequence: the first ~10 sols of
the march are dead time by construction** — spend them on C39 and Ctrl-F9.
Four items:

1. **PT-15 — Wisp power output (F07 + F15 bonus), THE FRONT.** Owner-attended
   co-run on a staged COPY of their fixture. Owner eyes present ⇒ a `tested`
   grant is REACHABLE here (unlike every unattended chain).
2. **C39 — the Service Automation label/class mismatch, OBSERVED at last.**
   The entry's stated next step is *"a keyboard observation, not more
   reading"*; the sign (penalty vs missing uplift) is genuinely unresolved.
   Same sitting, same save copy, forced law + infopanel reads.
3. **F85 — the 10-second Ctrl-F9 check, RE-ROUTED to this sitting.** It was
   slated to ride the PT-20 redo, but its only requirement is "press Ctrl-F9
   in a colony" — any colony. Riding here answers the owner's open decision
   sooner. (Re-route noted on the checklist; the PT-20 redo keeps everything
   else.)
4. **EF-051 confirm — the post-untick listing.** The owner unticked Steam
   Cloud 2026-08-11 and the strays were cleared to the 55-file baseline.
   This chain's FIRST launch is the falsifier: pre-launch and post-launch
   save-dir listings decide whether the WORKFLOW "never say gone" caveat
   retires. Costs one listing, already scripted into close-out.

**Facts this chain stands on, Src-verified 2026-08-11 by the authoring session**
(1.0.7.396349, `A:\SteamLibrary\steamapps\common\Project Spark\ModTools\Src`):

* **Mystery trigger** (`Lua\Scenario\Mystery 11.generated.lua:74-78`, St. Elmo
  = "Mystery 11"/LightsMystery): `WaitMsg("ColonyApprovalPassed")` then
  `Sleep(7200000 + InteractionRand(7200000, seq_id))` — founder-stage pass,
  then **10–20 sols uniform** (30,000 game-ms = 1 game hour, MEASURED,
  PLAYTEST_HELP). The wait is GAME time ⇒ ultra speed compresses it.
* **Speeds**: `SetGameSpeedState("ultra")` = 20× (`const.ultraGameSpeed`,
  `Lua\_GameConst.lua:28`; HUD state switch `Lua\X\HUD.lua:528-543`). Retail
  UI caps at 5× by button set only.
* **The C39 law is deep in its branch**: policy `Automation` is
  `PolicyCategory = "Technology"`, SortKey **900 — 10th of 11**
  (`Data\PolicyDef.lua:740-747`), which is why organic play never surfaces it
  early.
* **Direct enact path**: `LawDefs.Policy_Automation_ServiceAutomation:Activate()`
  is the EXACT call a passed vote executes (`Legislature:EnactLaw` →
  `LawDefs[law_id]:Activate`, `Lua\Factions\Legislature.lua:512-553`;
  `Activate` swaps out the policy's previous law, applies effects, fires
  `Msg("LawActivated")` — `Lua\ClassDefs\ClassDef-Factions.generated.lua:
  1778-1794`). `:Deactivate()` (`:1796-1813`) reverts and restores the policy
  default. Neither is cheat-gated; both are console-reachable. ⛔ NEVER RUN by
  this project — first-execution discipline binds (pcall printed, effect
  read either side).
* Cheat-gated alternatives, recorded so nobody reaches for them on retail:
  `CheatEnactAllLaws()` requires `CheatsEnabled()` (false on retail — F101);
  `g_AllPoliciesVisibleCheat` / `g_QuickSessionsCheat` are plain GameVars
  (console-settable) that make branches visible / sessions 10× faster — the
  VOTE-flow route if ever wanted; not needed for this chain's forced leg.

## Manifest

| # | file | owner needed? | what it does |
|---|------|---------------|--------------|
| 1 | `01_OPUS_PREP.md` | No — game closed | re-derive each item's route from its entry · Src-verify every read the sitting scripts · author + park the instruments · stage the fixture COPY · checklist riders |
| 2 | `02_OPUS_SITTING.md` | **YES — attended co-run** | the sitting: gate + fixture confirm → Ctrl-F9 → C39 leg → mystery march at ultra (owner plays) → PT-15 readings at the wisp choice → F15 rider · incremental recording, logs archived |
| 3 | `03_FABLE_AUDIT.md` | No (routes decisions) | terminal audit vs archived logs · status honesty (a PT-15 `tested` grant must quote the owner verbatim) · EF-051 caveat retire/keep · integration · folder EMPTY · kickoff |

## Binding chain rules

1. **Staleness check first, every prompt**: `git log --oneline -10` + `git pull`.
2. **Inbox/outbox in writing**; each prompt appends to the next prompt's
   `## Notes from upstream`, commits, deletes its own file in the same commit.
   Folder emptiness is prompt 3's done-condition.
3. **Route, don't drop**; unsure who owns a discovery → STOP AND ASK.
4. **Self-split at a clean commit boundary** if context runs short.
5. **Recorded facts are claims** — re-derive each item's ROUTE from entry +
   Src before acting; the summaries above cite what the authoring session
   verified, and anything else is trust-carried until checked.
6. **WORKFLOW binds in full**: the Co-runs harness-rule stack (unattended-1
   1–4, batch-1 1–6, batch-2 1–9 as amended), **R4** (state-transition claims
   carry a save/reload round trip or say PRE-RELOAD ONLY), **R7** (verdicts
   evidence the EFFECT), the run-top pack gate (**must STOP**, rehearsal mode
   exempted only with a MODE banner + VOID stamps).
7. **FIX_POLICY §3a — staged COPIES only. ⛔ THREE protected files now**:
   `TEST2H TRAIN.savegame.sav` (MD5 `103B320A1434513BC8773553096A8958`),
   `PT35FIXTURE.savegame.sav` (MD5 `D721329D1EE18604B3D6C89401F74738`), and
   **`PT-15.savegame.sav` — the owner's OWN fixture, NEW standing fixture,
   load a COPY, it SURVIVES this chain** (byte-verify all three at close-out).
   Staged saves die in the recording commit; close-out LISTS the directory
   against expected survivors — and THIS chain's listings are also the
   EF-051 post-untick confirm (item 4).
8. **Probe hygiene binds unchanged** — parked .txt sources, files in TestKit
   `Code/` only while a run happens, ARM GATE before every launch (C11: a
   script FILE, resolution cross-check included), `PROBE SWEEP:` line in
   every result commit, R8 `git add -f` for every cited log.
   Resurrect, don't rewrite: unattended-2's harness survives at
   `git show e5dca6f:docs/agent/prompts/unattended-2/97_U2Common.lua.txt`
   (gate, Load/Save with EF-050's verbatim-savename guard, Applicable,
   Try/TryYield, ErrorWatch); batch-2's at `7110384`, batch-1's at `530df63`.
9. **doccheck green before every doc commit**; STATE 60-line cap; commits via
   `git commit -F <file>`; parse sweep before any commit touching Lua; push.
   PS 5.1 hazards (no-BOM UTF-8 via `[System.IO.File]`; `.ps1` needs BOM);
   ⚠️ the Python sibling: text-mode Python rewrites convert stray CR — Edit
   tool or binary mode only.
10. **⛔ NO ASSUMED CAPABILITY** — first execution of `LawDef:Activate`/
    `:Deactivate`, the sequence-player countdown read, and every wisp/trap
    read follows first-execution discipline (pcall printed, liveness witness,
    effect read). EF-047 (absence only from archived logs) · EF-048
    (truthiness/type, never `== true`) · EF-049 (save witness = disk bytes +
    load-back) · EF-050 (savename VERBATIM — full `.savegame.sav` names).
11. **Forced-vs-organic per reading.** The mystery march and the owner's play
    are ORGANIC; the staged copy, ultra speed, the C39 law enact, and any
    setup cheats are FORCED and disclosed per reading. ⭐ **Owner eyes are
    present: `tested` grants are REACHABLE for PT-15** — a grant must quote
    the owner's verdict verbatim (Tier A/B per WORKFLOW sign-off rules) and
    name what was forced anyway.
12. **Cheat the setup, never the mechanism** (PLAYTEST_HELP): sanctioned
    accelerators fine for C39's workshop setup (research/build); NOTHING
    injected into wisps, traps, or the mystery sequence itself — the mystery
    is played, not forced. Disclose every cheat in the reading it enabled.
13. **⛔ D10 stays parked** (C39 entry warning): no capacity-dial work rides
    this chain; the C39 leg holds everything else at base.
14. **⭐ Kickoff + next-chain handoff.** Prompt 3's owner report ENDS with the
    next kickoff (expected front: the **PT-20 redo co-run** — pack-off run
    condition, deliberately NOT folded into this sitting; unauthored, say
    what authoring takes).

## Scope fence — the whole chain

**In:** PT-15 to the free-the-wisps reading (+ F15 destroy rider if a second
trapful exists); the C39 observation (enact → read → deactivate → record sign
and size); the F85 Ctrl-F9 check (evidence only — the decision stays the
owner's); EF-051 post-untick listings; the standing F02/F78/F81 organic watch;
whole-log review (F99 `TrackElement.lua:805` passive watch · C45
`invalid pos with no holder`).
**Out:** the PT-20 redo (next chain); any code change to pack or TestKit
(C39 is an OBSERVATION — if it confirms, the repair is a NEW owner decision);
D10; mystery content beyond the wisp choice; changing any owner decision.

## Stop conditions (chain-wide)

- `PT-15.savegame.sav` missing or its fixture confirm fails (mystery not
  St. Elmo, colony state unreadable) → sitting legs that need it SKIP with
  the failed read named; C39 + Ctrl-F9 still run (any colony works).
- Pack not loaded at the run-top gate → STOP (the gate stops the run; the
  re-enable is the owner's, handed back explicitly).
- Any `[LUA ERROR]` naming pack/TestKit code → stop that leg, record
  verbatim, continue independent legs.
- The mystery march stalls (trigger read shows the countdown never armed —
  founder stage unpassed and unpassable in sitting time) → bank Ctrl-F9 +
  C39, record the mystery state read, route PT-15 continuation to a
  follow-up sitting; the fixture copy's progress may be SAVED under a chain
  name for that follow-up (full `.savegame.sav` name, EF-050).
- Context runs short → self-split at a clean commit boundary (rule 4).
