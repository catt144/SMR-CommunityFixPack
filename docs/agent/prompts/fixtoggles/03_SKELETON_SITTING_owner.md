# fixtoggles 03 — the skeleton sitting (ATTENDED · KILL GATE)

Link 03 of `fixtoggles`. **Needs the owner at the keyboard** (and a game controller if they have one). README binding
rules 1–18 are yours; the live-sitting rules of `prompts/perma/GENERAL_USE_PROMPT.md` bind too (one command per line,
readings from the LOG FILE, cheat discipline, no live UI-internals prototyping). Staleness: `git log` + `git pull`.

## Before the owner touches anything

- ⛔ **Stale-probe gate** (WORKFLOW "Probe hygiene"): `grep -rln "TEMPORARY" Code/ ../SMR-BugFixPack-TestKit/Code/` →
  todo list; not clean ⇒ repair or stop. Every result commit carries a `PROBE SWEEP:` line.
- Re-confirm the fixture AT SITTING TIME (a 1.1.0 colony; `EF-079`). Read the save's metadata header first
  (memory `savegame-metadata-is-readable`).
- Read 02's predictions (`reports/FIXTOGGLES_SKELETON_PREDICTIONS.md`) and the script in your inbox. Every step names
  its prediction and its abort threshold BEFORE it runs.
- ⭐ Offer the owner a co-run with the owed v7 sitting (checklist 144 a) if it is still owed — one boot, their call.
  If accepted, keep the two sets of readings separate in the record.

## The legs (priority order — a truncated sitting banks the decider first)

1. **Enable path + cold boot** (`FIX_POLICY` §2 F87): the pack loads, every module's line reads as before, the
   converted module's switch line appears, 0 `[LUA ERROR]`.
2. **The surface opens** by mouse; every registered module listed; unconverted ones visibly not switchable.
3. **Live switch** of the converted module: off → its behaviour stops (the spec's positive control); on → returns.
   An objective counter that CAN fail, read from the log (WORKFLOW leg-design rules).
4. **Persistence:** quit, relaunch, the choice held. **Deviation-only storage:** the prediction doc's default-change
   check.
5. **Gamepad:** reach a row, switch it, apply, leave — with a controller if the owner has one. No controller ⇒ record
   UNSAMPLED (never PASS) and route it to 11 as a TAKEABLE-WHEN.
6. Relay every owner verbatim through the harness note primitive (`*.Note(...)`) the moment it is spoken (WORKFLOW
   "Attended-sitting classes from `corun-pt15`", item 3).

## Verdict — one of three, written into the checklist (148) and 99's inbox

- **PASS** → 04, 05, 06, 07 unblock.
- **PASS WITH CORRECTIONS** → strike-and-supersede the spec §-by-§ (`CHAIN_METHOD` §5 D), then unblock.
- **KILL** → the route is not viable as specced. Apply ck148(a)'s fallback if it covers the failure (e.g. gamepad fails
  ⇒ built-in Mod Options page) and re-queue 02 as `02b`; otherwise 99 runs in its reduced form.

## Scope fence

IN: running the skeleton, reading logs, recording, archiving the logs this verdict cites into `docs/archive/logs/` in
the SAME commit (evidence rotation, `CHAIN_METHOD` §3). OUT: fixing code mid-sitting beyond a mechanical repair with a
re-verified A/B; any other module.

## What may NOT be claimed

A gamepad PASS without a controller in the owner's hands. A PASS on a step whose prediction was not written first.
Anything about the other 44 modules.

## Close-out

Commit the verdict, the archived logs, checklist 148's update and the SESSION_LOG entry; outbox to 04, 05, 06, 07
and 99; strike your row; `git rm` this file; push.

## Notes from upstream

- (link 02 appends the script and predictions pointer here)
