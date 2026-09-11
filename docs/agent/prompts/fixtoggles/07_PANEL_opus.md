# fixtoggles 07 — the panel, in our own look

Link 07 of `fixtoggles`. README binding rules 1–18 are yours — **rule 9 above all**: the reference mod is inspiration
for WHAT a panel can do, never HOW it is written or worded. The owner: *"I do not want to rip off his code, I would want
our UI to have its own feel and look."* Runs after a 03 PASS; independent of 04–06b; your final check reads 06b's links.

## Job

Build the surface ck148(a) ruled, on the route 03 proved, to the spec §6 visual direction:
- one row per registered module: its **stable id** (never a positional number — ids are what players quote in bug
  reports), title, one-paragraph description (08 writes the text; use placeholders that 08 replaces), a **Beta** tag,
  a **restart-required** mark where the spec says next-load, an **always-on part** note where there is one (e.g.
  TrackTunnelPowerBridge's teardown), and the **link** relation from 06b;
- search; shown / total / on counters; staged changes with Apply, **Back discards**, and a **Restore defaults** action
  (defaults, not all-off);
- reachable and fully usable by gamepad (03's proof, repeated on the full panel), keyboard and mouse;
- ⛔ no version dropdown, no version filter (rule 10). The data model may reserve the field the spec names; the UI
  shows nothing for it.
- All new player-visible strings are `Untranslated(...)` (`FIX_POLICY` §6); layout from relative sizes, not fixed pixels.

⛔ **No live UI-internals prototyping in a play session** (PLAYTEST_HELP ground rule 5): build desk-side from the shipped
UI sources; the in-game verification is 11's.

## Scope fence

IN: the surface files, `items.lua`/`metadata.lua` only if the route requires, the harness (what can be desk-tested:
state model, staging, defaults, search filter). OUT: module semantics, text content (08), version UI.

## Stop conditions

A needed engine name is blacklisted · the gamepad model needs something the skeleton did not prove · the panel would
have to write the store outside the spec's one-writer rule.

## What may NOT be claimed

That the panel works or looks right in the game (11). Gamepad usability beyond what 03 witnessed.

## Close-out

Green gates, `Mars.exe` closed. Outbox to 08 (every string slot), 10 (every UI check 11 must run) and 99; strike your
row; `git rm` this file; push.

## Notes from upstream

- (links 01–06b append here)
