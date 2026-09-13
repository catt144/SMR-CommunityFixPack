# smrtk payload P3 — the Agent page: slots, pins, triggers, note, screenshot+mark

Payload P3 of link 03A (`smrtk`). README rules 1–22 are yours, **21 especially: you write, you never commit.**
Independent of P1/P2/P4/P5.

## Job — `Code/74_SMRTK_Agent.lua` + the `Code/80_AgentSlots.lua` contract

1. **The slot contract.** `80_AgentSlots.lua` is the file an agent rewrites before a sitting. Ship it as a
   commented template with six slots: `SMRTK.Bind(1, "label", function(ctx) ... end, { mode = "once" })` and
   `{ mode = "armed", on_click = function(ctx, pos, obj) ... end, on_disarm = ... }`. `ctx` carries `sel` (SelectedObj),
   `pin` (A/B/C), `cursor` (`GetTerrainCursor()`), `mark`, `log`. **Console rebinding for mid-sitting** is the same
   call typed once. ⛔ `EF-096`: no string-to-code; the slot IS a function in a mod file or a console line.
2. **The Agent page UI:** six slot buttons showing label, fire count and armed state (lit when armed); a scratch
   seventh; pins A/B/C (click an object, press Pin; shows `Class(handle)`; logs `SMRTK_PIN A=Class(handle)`); the
   trigger list (armed/disarmed, fire count); the **note field** (`XTextEditor`; Enter → `SMRTK_NOTE "<text>"` with
   game time, then clears); **Screenshot+Mark** (`WriteScreenshot` into `C:\Dev\SMR-ScreenCaptures\SMRTK_<markid>.png`
   — if the engine confines the path, write where it allows and log the path; and `SMRTK_MARK` with the same id).
3. **Click-to-target** for armed slots: **the capture route is decided** — 03A's spike (`reports/SMRTK_UI_HOOKS.md` §2,
   in your inbox). Build on it or its declared fallback; a better route you see goes in SUGGESTIONS for the coordinator to re-spike
   on, not into your file (parallel payloads cannot negotiate — README § "What is FIXED"); re-read the cited lines
   first (rule 12) and report DRIFT if they disagree. The position and any object under it go to `on_click`. Rule 9: armed
   only, uninstalls on disarm.
4. **Triggers:** `SMRTK.Trigger{ id, label, when = function() ... end, do = { mark = true, pause = true, screenshot =
   false, sound = true }, once = true }` — a game-time polling thread (cadence configurable, default 1 s game time),
   each firing logged `SMRTK_TRIGGER <id>`; the built-ins: `sol >= N`, `first Lua error since mark`, `selected field
   changed` (P4's watch reuses this), `rocket landed`. Auto-disarm on load/map change (rule 9).
5. **Auto-disarm + per-fire log** for every armed slot and trigger (rule 9), visible in the status strip's armed count.

## Scope fence

IN: `74_SMRTK_Agent.lua`, `80_AgentSlots.lua`, their `metadata.lua` lines. OUT: World/Saves/Kit content, the stamper.

## Stop conditions

The spike's click route does not hold on re-read · `XTextEditor` cannot take focus inside an `XDialog` from a mod ·
`WriteScreenshot` has no writable path. Report; do not force.

## What may NOT be claimed

That a trigger fires at the right moment in play (08). That a screenshot landed (08 opens one).

## Close-out (payload — rule 21)

Do NOT commit, do NOT `git rm`. Parse-check both files; rule 6's and rule 7's greps, counts quoted. Return a
**numbered-claims report** to 03A: per unit (contract · page · click-to-target · triggers · disarm) — built · verified
how (command + output) · stopped · OWNER-ROUTED · for-07 (the slot contract, verbatim, for `perma/SMRTK_SLOTS.md`) · DRIFT. Plus **DEPARTURES** (every default you changed, why, which invariant you checked) and
**SUGGESTIONS** (better ways, things the plan missed — wanted, not tolerated; README § "What is FIXED").

## Notes from upstream

- (03A pastes 02's outbox and `SMRTK_UI_HOOKS.md` §2 here before launch)
