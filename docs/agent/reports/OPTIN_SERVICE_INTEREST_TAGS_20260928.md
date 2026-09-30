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
5. If you own the norman DLC: a Diner's popout also lists Foodie (+5 Comfort with delicacies),
   a Barista Café's lists Coffee Enthusiast (+10 / −10 Comfort). Enact Food Tours and a Diner's
   popout gains Tourist (+10 Morale per meal, 3× meals); repeal it and the line goes.
6. Toggle OFF, Apply, reselect: all views are vanilla again. Log: no `ServiceInterestTags` line
   other than `applied` / `deactivated` / `re-activated`.

A missing section, two Interests sections, or a changed vanilla line fails it. Icon, wording and
placement are the owner's to adjust by eye; the desk check cannot see the rendered look. Desk
result: PASS, 12 buildings × 4 toggle passes (Opt-In
`tools/deskchecks/service_interest_tags_deskcheck.py`). No game was launched by this task.
Executed model: Claude Fable 5.1 (`claude-fable-5-1`).

## 2026-09-30 — look passed; two legs left

The owner's sitting passed steps 1–6 above (log clean; archived in the Opt-In repo at
`docs/archive/d15_sitting_20260930/`, evidence in D15). Two legs remain before `tested-attended`:

1. **Uninstall.** Save with the toggle ON. Disable the Opt-In mod in the Mod Manager, then **fully
   quit and restart the game**; a return to the main menu is not enough (Opt-In WORKFLOW,
   PT-20 redo). Load that save. Pass: it loads and plays with no error; the panels are vanilla.
2. **Enable path.** With the Opt-In mod disabled, start the game. At the main menu, enable it in the
   Mod Manager, turn "Service interest tags" on in Mod Options, load a colony and open a service
   building. Pass: the Interests section and popout appear as in the first look.

Flush the log after each. The two can share one restart: do 1, then from its main menu do 2.

## 2026-09-30 — closed: tested-attended

Both remaining legs are done. The enable path passed. The uninstall leg ran on an older save of the
same colony, and the owner accepted it (*"2 is fine, this mod is not that complicated"*). Opt-In
D15 is `tested-attended`; ck220 is deleted. Both FIX_POLICY §8 configurations are done: the sitting
ran the released fix pack v1.00-026, and nothing in the fix pack touches this module's surfaces.
