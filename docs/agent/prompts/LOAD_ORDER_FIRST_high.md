# Load order: the pack puts itself first (option B), then a canary for option C

**One-off, authored 2026-09-25 on `main` at `9833cca`.** Build and desk-verify, then a separate
audit. The retail sitting is planned here, not run. The audit deletes this file and its map row
when it closes.

**Start:** run `git log --oneline -10`, `git pull` and `git status --short`, and compare every
input with `9833cca..HEAD`.

## Authority and outcome

**Owner rulings, verbatim:**

- 2026-09-24, the goal: vanilla repairs should run first, and a content mod that changes the game
  in areas we fix "would be best, if it did its alterations after we ran". This is recorded in
  [LOAD_ORDER_CROSSCHECK_2026-09-24.md](../reports/LOAD_ORDER_CROSSCHECK_2026-09-24.md).
- 2026-09-25, the choice: *"I want B or C, the rest of those are just more bandaides for the
  problem"*, then *"Can we go with B first, and if it works and we upload it, can we test the shap
  of C, put something harmless in the metadata that we can easily check for to see if it
  survives"*.

B is the cross-check's lever "Pack promotes its saved seed through public helpers". C is its
"Custom metadata `SetupEnv` wrapping the selector". Per-fix guard hardening (option A) is **not**
this job: the owner rejected it as a bandaid.

**End state:**

1. **B built, on a short-lived code branch** per WORKFLOW's branch rule. When the pack starts and
   is not first in the player's saved enable order, it moves itself to the front and keeps every
   other mod's relative order. It then tells the player once to restart. Once it is first, it
   writes nothing.
2. **A player opt-out.** A player who turns B off gets their own order left alone.
3. **Desk verification.** The harness must fail with the promotion removed, and must cover the
   cases under "Must hold".
4. **A retail sitting plan for the owner's approval.** Write it; do not run it; do not fire a
   sitting.
5. **A C canary designed and placed** for the release that ships B, with a written check procedure
   for after the owner uploads.

Records go on `main`: a dated report, and a note in the cross-check report's recommendation.
doccheck must be GREEN. Open a live todo list before the first write.

## Evidence (re-derive each line with `grep -n` on the archived 1.1.1.405907 tree before relying on it)

- **Load order is the saved enable order.** `AccountStorage.LoadMods`, copied in order into the
  queue ([EF-054](../facts/EF-054.md)). The alphabetical mod-manager list is display only
  (cross-check, "The visible manager sort is cosmetic").
- **The public helpers.** `TurnModOn` appends and `TurnModOff` removes
  (`CommonLua/UI/ModManager.lua:35-41`). `GetModsEnabledByUser` returns a copy of that list, **or
  every installed mod when `LoadAllMods` is set** (`CommonLua/Modding/Mod.lua:1995-2000`). B cannot
  control that branch; detect it and say so.
- **Saving.** A changed own persistent-data write calls `SaveAccountStorage(1000)`
  (`Mod.lua:1487-1503`). The cross-check desk-measured the save *request*, not a completed disk
  write. Direct `AccountStorage` and `SaveAccountStorage` are blacklisted in the mod sandbox.
- **The mod manager.** Each toggle writes through at once (`ModUI_Entry:SetEnabledAndSync`,
  `ModManager.lua:1532`). On close, the manager compares the list with its opening state, order
  included, and saves on any difference (`ModsUIDialogEnd`, `:123`). Read on 2026-09-25.
- **The existing desk probes.** The cross-check's
  [reorder probe](../../archive/load_order_crosscheck_2026-09-24/load_order_reorder_probe.py)
  changed `B,PACK,C` to `PACK,B,C` for the next queue, while the running `ModsLoaded` stayed as it
  was. Start there.
- **The acceptance case already in the field.** Passage Network 1.38 temporarily replaces the
  global `Dome` while mods load. When it loads before us, `Fix_VacuumWalks` and
  `Fix_HubLocalAccess` switch off (player report 2026-09-26, GitHub issue on
  `SMR-CommunityMods`). With the pack first, both must apply.
- **Why C is doubtful, measured.** The Workshop `.fpk`'s `metadata.lua` is the Mod Editor's
  regenerated file. On 2026-09-23 it had 0 comment lines against the repo's 312 (`pack_list.py`
  plus `flpk_extract.py` on `A:\SteamLibrary\steamapps\workshop\content\3215050\3787202810\ModContent.fpk`).
  The cross-check expects a resave to strip an undeclared `SetupEnv` method. Trap 3 in
  `perma/HANDOFF_ORCHESTRATOR.md` covers the writeback.

## Must hold (desk)

1. **Promotion.** A saved list `X, PACK, Y` becomes `PACK, X, Y` for the next launch, and the
   running session is untouched. The same holds when the pack is already last.
2. **Already first.** No write, no save request and no notice, on every launch.
3. **`LoadAllMods` on.** No write; the player is told B cannot apply.
4. **Opt-out on.** No write. Turning it back on promotes again.
5. **The pack's own persistent data is preserved.** If B uses it, it must not clobber anything
   the pack already stores there.
6. **Dependencies.** If the pack ever has a prerequisite, it stays ahead. A mod that declares the
   pack as a prerequisite is unaffected.
7. **Passage Network.** The saved order `PN, PACK` becomes `PACK, PN`, and at the next load
   both guards pass. Replay the cross-check's control with PN's lines 45-51.

Each case needs a control that fails with the promotion removed.

## The retail sitting plan (write it; the owner approves it before anyone prepares it)

The sitting must decide:

- whether a promoted order survives a full restart;
- whether a Paradox-account sync keeps it or rewrites it;
- what a hot enable and a disable/re-enable of the pack do;
- that a second launch writes nothing;
- the Passage Network case end to end.

Build it as a preloaded SMRTK sitting, per the attended-sitting rails. Price it in owner minutes.

## The C canary (owner's design; ships with B's release, checked after upload)

It must copy **C's shape**, meaning hand-written code in `metadata.lua` beyond the declared
metadata properties. A comment is not enough: comments are already measured as stripped. It must
be **inert whether it survives or not**, and whether it runs or not: no override of a native method
and no effect on loading. Make it easy to find: a unique literal findable in the extracted
`metadata.lua`, plus, if it can run, one log line.

Before it ships, prove on the desk that the Mod Editor still loads and packs the mod with it in.
After the owner's upload, the check has three parts:

- extract the Workshop `.fpk` and search it;
- search the post-upload local writeback;
- search a fresh boot log.

**Result:** if it survives, C reopens as a separate design question. If it's gone, C closes with
that evidence. Coordinate with `perma/release_prompt.md`: this job changes `metadata.lua`, so name
the canary in the release outbox.

## Scope

- **In:** B's code in the pack core or its own module, the opt-out, the notice text, the desk
  harness, the sitting plan, the canary and its check procedure, and the records.
- **Out:** changes to any fix module's guards (option A); option C's bootstrap itself; public
  load-order advice beyond B's own notice; an upload.

## Stops (report instead of continuing)

- The helpers are not reachable from pack code in the retail sandbox (EF-096 blacklist, or a
  missing global).
- B cannot keep the others' relative order, or cannot avoid writing on every launch.
- The canary cannot be shown inert at the desk. In that case ship B without it and say so.

## Do not claim

"The pack loads first" is desk-verified only until the sitting runs. A save request is not a disk
write. The canary shows only that code of that shape survives packaging. It does not show that C's
hook would work.

## Routing

Owner's routing, 2026-09-25: *"I am going to build with fable since this is going to be critical to
get right, and audit with astra."* It is recorded here as the owner's choice; neither seat checks
it.

Tag `_high`: a design-sensitive build. Skills: `doc-editing`, `smr-bug-library`, and `subagents`
before any delegation. House rules: `CLAUDE.md`; process: `docs/agent/WORKFLOW.md`; code:
`docs/agent/FIX_POLICY.md` §2 (`Require` checks, manifest pins) wherever B touches game code.

## Build close-out

Commit the branch and the `main` records. Write a dated report at
`docs/agent/reports/LOAD_ORDER_FIRST_BUILD_<date>.md` with:

- each "Must hold" case, its control and its result;
- the sitting plan;
- the canary's design and inertness proof;
- DEPARTURES from this brief, each with its reason;
- SUGGESTIONS.

Do **not** merge, and do **not** delete this file. Leave it for the audit. End with the audit's
kickoff line.

## Audit (a separate seat, fresh context)

Disbelieve the build. Check it against the branch diff, the archived source and re-run harnesses,
never against the report's summary.

1. **Controls.** Re-run each "Must hold" control, then revert the promotion in a scratch copy and
   require each one to FAIL. A control that passes with the promotion removed is vacuous.
2. **Relative order.** Confirm, for lists of different shapes, that other mods' relative order is
   preserved. Include a list with `PACK` absent, first, middle and last, and one with duplicate or
   stale IDs.
3. **Writes.** Confirm B writes and requests a save only when the order changes, the opt-out
   holds, and the `LoadAllMods` branch is left alone.
4. **The canary.** It must be inert: read its code, and confirm the Mod Editor load and pack step
   still work in the build's evidence.
5. **The sitting plan.** Read it from the owner's chair: clicks, not typing; a real-time cost; and
   predictions that can fail.
6. **Overclaims.** Check the report against "Do not claim".

**Verdict:** SHIP-TO-SITTING, CHANGES (each change named) or NO. Then commit the audit report on
`main`, give the owner the verdict and the sitting plan for approval, `git rm` this file and delete
its map row in the same commit.
