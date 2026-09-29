# Opt-In service interest tags — first look, 2026-09-28 (section rebuild 2026-09-29)

Checklist ck220 routes the owner's first in-game look here because the owner plays one game with
both mods loaded. This is an Opt-In module (`Opt_ServiceInterestTags`, D15); no Fix Pack runtime
behaviour changed. The record, hooks, rulings, trait research and desk check are in
[the Opt-In entry](B:/Dev/SMR/SMR-OptInPack/docs/agent/bugs/D15.md).

It shows each service building's interests (Gaming, Social, …) in two places. The build-menu
hover gets one line under "Service <category>". A placed building gets an **Interests** section
straight below Visitors (for a Diner or Grocer, below the food block), and hovering that section
pops out the building's description, category, visitor filter and the traits that gain or lose
something there. Display only. This is the owner's 2026-09-29 layout.

Steps, any running colony, after installing the Opt-In working tree:

1. Toggle OFF (default). Hover an Electronics Store in the build menu, and select a placed
   Casino Complex, a Diner and an Open Air Gym: all look as they do today. This is the control.
2. Options → Mod Options → "Service interest tags" ON, Apply. Reopen the build menu category and
   hover the Electronics Store: `Interests  Gaming, Shopping` under `Service  Stores`.
3. Reselect the Casino Complex: an Interests section below Visitors reads
   `Social, Gaming, Luxury / Gambling`. Hover it: description, `Service Indulgence`,
   `Visitors Adults`, then Gamer and Party Animal at +10 Sanity per visit and Gambler at
   −20 Sanity with a 50% chance.
4. Reselect the Diner (section below the food block; Party Animal, Glutton, Vegan) and the Open
   Air Gym (popout carries "Visitors may become Fit" and the Fit chance; its top description block
   is gone, which the owner accepted).
5. Toggle OFF, Apply, reselect: all views are vanilla again. Log: no `ServiceInterestTags` line
   other than `applied` / `deactivated` / `re-activated`.

A missing section, two Interests sections, or a changed vanilla line fails it. Icon, wording and
placement are the owner's to adjust by eye; the desk check cannot see the rendered look. Desk
result: PASS, 12 buildings × 4 toggle passes (Opt-In
`tools/deskchecks/service_interest_tags_deskcheck.py`). No game was launched by this task.
Executed model: Claude Fable 5.1 (`claude-fable-5-1`).
