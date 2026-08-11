# Chain prompt 2 — the sitting (ATTENDED co-run; owner at the keyboard)

**Read `README.md` first — binding chain rules apply.** Staleness check, todo
list. This brief is a PRIORITY QUEUE, not a schedule (batch-1 lesson): a
truncated sitting still banks the deciders first, owner deviation is absorbed
(witness whatever runs), and once the owner overrides onto a lead, state the
plan's position once and keep the ledger — no nagging.

**Honest cost.** Owner time: **~45–90 min**, dominated by the mystery march
(open-ended, and it is the owner PLAYING THEIR OWN COLONY — organic time, not
overhead). Legs 1–2 alone: ~15 min. Estimates have missed before; the queue
order is what protects the sitting, not the estimate.

## Before launch

ARM via `CP15_ARM.ps1` (gate GREEN or no launch). Confirm the three protected
MD5s and `CP15STAGE.savegame.sav`. Take the pre-launch save-dir listing if
prompt 1's is stale. Console: TestKit loaded → Enter (or Alt-Shift-C) once in
a colony.

## The queue

**Leg 0 — gate + fixture confirm.** Load `CP15STAGE.savegame.sav` (a COPY —
say so in the log). `RequirePackLoaded` — a 0/0 STOPS the sitting (owner
re-enable + full restart, D13). `CP15.MysteryWhere()`: founder approval
state + trigger countdown, raw values printed. Record run conditions
(build, map, speed read-back, pack count AS READ).

**Leg 1 — F85's Ctrl-F9 check (10 seconds, highest value per second).**
Owner presses **Ctrl-F9** in the colony. Read: did a quicksave land — on-disk
file (name recorded verbatim, EF-050 eyes) + any notification. Either answer
is a finding: landing = a live default-keybind route into F85's defect
(changes the whole disposition); nothing = the source read confirmed on
retail. **Route the evidence to the checklist F85 item; the decision stays
the owner's.** FORCED (a keypress on request); say so.

**Leg 2 — C39, observed at last.** All readings by the parked instruments,
FORCED and disclosed; D10 stays parked; everything else at base.
1. Setup (setup-cheats sanctioned, disclosed): a staffed Workshop + an
   in-family Service control (Diner/Spacebar) in one dome. If the new-ish
   colony lacks them: `CheatResearchAll` + place + `CheatCompleteAllConstructions`
   + `CheatSpawnNColonists`/`CheatUpdateAllWorkplaces` as needed. ⚠️ Cheats
   AFTER leg 0's fixture confirm and AFTER leg 1, never before; they are
   setup for THIS leg only, and `CheatResearchAll` is fine for PT-15 (the
   mystery grants its own tech — but state it in the record).
2. `CP15.C39Before()` — the full read set on both buildings.
3. `CP15.C39Enact()` — first execution of
   `LawDefs.Policy_Automation_ServiceAutomation:Activate()`, pcall printed,
   `ActiveLaws` read back (EF-048: truthiness/type).
4. Readings per prompt 1's shift-boundary answer (if a shift change is
   needed, take it at ultra — the same fast sols advance the mystery
   countdown; label every reading with its game time).
5. `CP15.C39After()` → the entry's question: do the four-Workshop
   `max_workers` drop, does `performance`/Comfort move, WHICH DIRECTION, and
   does the Diner control behave per the compensated path. The owner LOOKS
   at both infopanels — their observation is the attended half; quote it.
6. `CP15.C39Revert()` — `:Deactivate()`, read the policy default restored,
   full read set again (do-no-harm on the revert).
   R4: if any C39 claim is about persisted state, round-trip it; otherwise
   stamp PRE-RELOAD ONLY explicitly.

**Leg 3 — the mystery march (ORGANIC; the owner plays).**
`SetGameSpeedState("ultra")` through the dead time; the owner plays the
beats: founder approval if not yet passed → trigger (10–20 sols) → sinkhole
popup → anomaly scan → tech → build Light Traps → wisps caught over the
following nights. The rig's part: `CP15.MysteryWhere()` on request, periodic
condition reads, the standing F02/F78/F81 organic watch, and NOTHING forced
into the sequence. Every popup/beat gets a one-line timestamped record.

**Leg 4 — PT-15, the reading it all exists for.** At the free-the-wisps
choice: `CP15.TrapRead()` BEFORE (wisp count per trap, trap output, grid
production), owner makes the choice (their click, their observation), read
AFTER. The fix's claim: ~1000× wisp count of power, a real source — against
the broken trickle. R7: the effect is grid numbers, not a popup. R4: save +
reload (chain-named save, full `.savegame.sav`) and re-read — the power must
survive serialization. **Owner verdict verbatim** — with owner eyes this can
earn `tested` (Tier per WORKFLOW sign-off; package the raw lines for their
quick read).

**Leg 5 — F15 rider (good-to-have).** If a second trapful exists: destroy
mode, research-points read either side. N/A is a fine answer; say why.

## Recording (incremental, per leg)

Bank each leg's readings to the entries/checklist AS THEY LAND (self-split
safe). Every reading: FORCED/ORGANIC label + what was cheated for setup.
Logs archived with R8 `git add -f`, `cmp`-verified, named
`cp15_<exe>-<stamp>.log`. `PROBE SWEEP:` in every result commit.

## Close-out

Disarm (gate GREEN), delete staged saves EXCEPT the three protected files +
any save the owner asks to keep (list them), **save-dir listing = the EF-051
post-untick confirm** — compare against prompt 1's baseline + this sitting's
known writes; a returned stray REOPENS EF-051, a clean listing is the
evidence that retires the WORKFLOW caveat (the audit rules on it). Byte-verify
the three protected files. Whole-log review: 0 `[LUA ERROR]` expected;
F99/C45 greps; unexplained lines verbatim with age. Outbox to
`03_FABLE_AUDIT.md` (`## Notes from upstream`): per-leg verdicts with their
log line numbers, what was forced, what the owner said verbatim, misses.
Commit, delete this file in the same commit, push.

## Stop conditions

README's chain-wide set, plus: the owner ends the sitting → bank what ran,
inventory the remainder as TAKEABLE riders, still hand prompt 3 a clean
close-out.
