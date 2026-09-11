# fixtoggles 05 — convert the full-body replacements

Link 05 of `fixtoggles`. README binding rules 1–18 are yours. Runs only after a 03 PASS; independent of 04 and 06.
Staleness: `git log` + `git pull`; the spec is the contract.

⚖️ The owner accepted excluding full-body replacements only *"if there is a good reason we cannot do them all (but all
is preferable)"*. The research found no module that cannot be switched. Your job is to make that true, or to write down
precisely why it is not for a given module and route it (ck148) — never to exclude one quietly.

## The set (shape b rows; the spec §3 table is authoritative)

BombardmentSpread · DomeFreeSpaceMismatch · DomeOverviewHighlight · LandscapeUnitFilter · PayloadTemplateRefill ·
RocketDroneChurn · ShuttleTransportCache · TrackConnectorPingPong · TrackSalvageRefund · TrackSalvageWipe ·
TrainCargoDumping · VacuumWalks · WispRewards

## Job, per module

1. Open the module and BOTH the shipped body and our copy. A body copy today installs without keeping the original
   (e.g. DomeFreeSpaceMismatch, research `:61`). **Capture the shipped original from the DECLARING class before the
   replacement is assigned** (`FIX_POLICY` §2 F107 rule), and add that `(class, method)` pair to the module's `Require`
   block so `harvest_wrap_targets.py --check` can see it.
2. Gate: off ⇒ the captured original, byte-for-byte vanilla behaviour; on ⇒ our copy. No restore (rule 7).
3. Keep the module's existing branch guard (probe / shape test) exactly as it is (rule 10); `bodycheck.py` stays OK
   (the `SRC:` hash is of the SHIPPED body and does not move).
4. Threads the copy starts (TrackConnectorPingPong `:208`): state what happens to one already running when the switch
   goes off (spec §7).
5. Header + harness case (falsifier seen RED), as in 04.

One module per commit for the five 1.1.0-only bodies (LandscapeUnitFilter, PayloadTemplateRefill, RocketDroneChurn,
TrainCargoDumping, VacuumWalks — the hotfix-2 re-copies); batch the rest. Self-split to `05b` if needed.

## Scope fence

IN: the listed module files, the harness. OUT: core, links (06b), text, version work.

## Stop conditions

The original cannot be captured (a file-local, generated code — a "reconstruction", `FIX_POLICY` §1.5) ⇒ record what an
off switch can honestly do for it and route · a gate changes on-path behaviour.

## What may NOT be claimed

"Off = vanilla" for a module whose original you could not capture. Anything in-game.

## Close-out

Green gates, `Mars.exe` closed. Outbox to 06b (the track cluster) and 99; strike your row; `git rm` this file; push.

## Notes from upstream

- (links 01–03 append here)
