# smrtk 08 — the full attended sitting

Link 08 of `smrtk`. A **Claude** session attending (rule 22), the owner at the keyboard. README rules 1–22; 07 wrote the script below and the
predictions (`reports/SMRTK_FULL_SITTING_PREDICTIONS.md`). The stale-probe gate binds before any reading.

## Job

Run the script; score every step against its prediction; **read `CheatsUsed` at the end of the sitting** (the
whole-sitting taint control — one read, after everything) and the toolkit's
eligibility read with the Mod Manager closed. On build 24995074 that read is
`UNAVAILABLE:sandbox` (`EF-096`): CanUnlockAchievement is blacklisted. Do not
claim full eligibility was measured. Write `reports/SMRTK_FULL_SITTING.md` with the archived log path, per-step verdicts, and every drift
(a button that logged twice, a line without the tag, an armed thing that survived a load) as evidence for 99.

## Verdict classes

PASS · PASS WITH CORRECTIONS (list them; the fixing link is named in 99's inbox as owed) · FAIL (name the button
class; 99 decides SHIP WITH CHANGES vs NO SHIP).

## What may NOT be claimed

Anything the log does not show. A gamepad path. Behaviour of a button class the script did not reach.

## Close-out

Outbox to 99; strike your row; `git rm` this file; push. Tell the owner in one line whether the panel is theirs to
use from now on (it is, in whatever state 99 confirms — the TestKit never ships).

## Notes from upstream

- **01 correction, 2026-09-13:** no eligibility verdict is available to the
  mod on build 24995074. 07 must script the honest unavailable read separately
  from taint. Use a clean 1.1.0 baseline; normal already-cheated fixtures cannot
  prove no added taint. See 01's predictions §Disagreements/§DEPARTURES.

- (07 writes the script here.)
