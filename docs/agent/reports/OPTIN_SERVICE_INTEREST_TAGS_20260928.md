# Opt-In service interest tags — first look, 2026-09-28

Checklist ck220 routes the owner's first in-game look here because the owner plays one game with
both mods loaded. This is an Opt-In module (`Opt_ServiceInterestTags`, D15); no Fix Pack runtime
behaviour changed. The record, hooks, calls and desk check are in
[the Opt-In entry](B:/Dev/SMR/SMR-OptInPack/docs/agent/bugs/D15.md).

It shows each service building's interests (Gaming, Social, …): a line in the build-menu hover
under "Service <category>", and an "Interests" row at the end of a placed building's Visitors
section (for a Diner or Grocer, in the food block under "Meals served last Sol"). Display only.

Steps, any running colony, after installing the Opt-In working tree:

1. Toggle OFF (default). Hover an Electronics Store in the build menu and select a placed
   Casino Complex and a Diner: all three look as they do today. This is the control.
2. Options → Mod Options → "Service interest tags" ON, Apply. Reopen the build menu category and
   hover the Electronics Store: `Interests  Gaming, Shopping` under `Service  Stores`.
3. Reselect the Casino Complex: the Visitors section ends with
   `Interests  Social, Gaming, Luxury` / `Gambling`. Reselect the Diner: its food block shows
   `Interests  Social, Dining, Food`. A Medical building shows `Medical Checks`.
4. Toggle OFF, Apply, reselect: all three are vanilla again.
5. Log: no `ServiceInterestTags` line other than `applied` / `deactivated` / `re-activated`.

A missing line, a doubled row or a changed vanilla line fails it. Layout, wording and placement
are the owner's to adjust by eye; the desk check cannot see the rendered look. Desk result: PASS,
10 buildings × 4 toggle passes (Opt-In `tools/deskchecks/service_interest_tags_deskcheck.py`).
No game was launched by this task. Executed model: Claude Fable 5.1 (`claude-fable-5-1`).
