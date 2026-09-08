# VANILLA-FIX QA — is what we say the developers fixed actually fixed?

Written **2026-09-08** for a FRESH context, on the owner's instruction: *"I
would rather double check the devs' work … a dedicated agent to examine what we
are saying the devs fixed, look at their code and see if it seems accurate."*
The patch that follows must not be half-baked; this QA is the gate on the
desk evidence behind it.

> 🎯 **ONE JOB.** For every claim in `reports/PACK_1_1_0_REVERIFICATION.md` of
> the form "1.1.0 changed / fixed / removed X" that a REMOVE or FIX verdict
> rests on, open the shipped 1.1.0 code yourself, form your OWN read, and say
> whether the claim holds. Then say whether the vanilla replacement is itself
> correct or a rebreak. **You write no code. You edit no `Code/` file.**

## 0 · Rules

- Shipped 1.1.0 Lua: `A:\SteamLibrary\steamapps\common\Project Spark\ModTools\Src`
  (`Lua/`, `CommonLua/`, `Data/`, `DLC/`). The 1.0.7 tree is GONE (`EF-075`);
  every "old" line is a claim from our module header or a bug entry.
- ⛔ **Form your own read BEFORE reading the report's evidence column.** Take
  the row's module name and defect id, open our module (`Code/Fix_<id>.lua`)
  to learn what defect it claims and what it targets, open the 1.1.0 target,
  decide, THEN compare with the report's row and §1h. Disagreement is the
  product; agreement is only worth something if it was independent.
- ⛔ Check the THING, not its label. A name that is gone may have been RENAMED
  (`daily_update_func` → `DailyUpdate` was nearly retired as "gone"); a
  contradiction may have been resolved the OTHER way (dead line deleted, wrong
  value kept). "grep found nothing" is not evidence until you have grepped for
  where it went.
- A helper prints a whole top-level function with line numbers:
  `python "<scratchpad>\luafn.py" "Lua/Units/Drone.lua" "^function Drone:MarkUnreachable"`
  (copy `tools/`-free helper from the scratchpad path in the launch message, or
  use `grep -n` + `sed -n a,bp`).
- Quote every line you rely on with `file:line`. Never write "looks fine".
- Untested is not clean: list what you did not open per row.

## 1 · The claims to check

Read `reports/PACK_1_1_0_REVERIFICATION.md` §1a (FIX, F-1…F-10) and §1b
(REMOVE, R-1…R-36). For each row answer, in this order:

1. **Our defect claim** — one line: what our module says was wrong and where.
2. **Your read of 1.1.0** — what the shipped code does at that site NOW, with
   `file:line`. If the target is absent, where did it go (renamed, moved,
   inlined, deleted with its feature)?
3. **Is the report's claim accurate?** `CONFIRMED` / `DISPUTED` / `PARTIAL`,
   with the reason. A DISPUTED row must quote the line that contradicts it.
4. **Is the vanilla replacement correct?** Trace it: does it produce the right
   behaviour, or is it a rebreak (the same defect in a new shape, a new defect,
   or a contradiction resolved by keeping the wrong value)? Name residuals.
5. **What does a 1.1.0 player get if we act on the verdict?** For REMOVE: what
   vanilla behaviour returns; for FIX: whether the proposed shape in the row is
   the right repair or would itself pin us to something fragile.
6. **Not opened** — named.

## 2 · Deliverable

`reports/VANILLA_FIX_QA.md` (or the section file named in the launch message
if you are one of several readers):

- one `##` per row with the six answers;
- a **summary table**: `row | module | claim | replacement correct? | patch
  impact | evidence`;
- a **final section, "what would make the patch half-baked"**: every row where
  acting on the verdict would ship something wrong, ranked, with the line that
  proves it. If there are none, say so and say what you opened to know it.

⛔ Do not inflate: a row that holds is one sentence plus its lines. ⛔ Do not
soften: a DISPUTED row is the reason this QA exists.
