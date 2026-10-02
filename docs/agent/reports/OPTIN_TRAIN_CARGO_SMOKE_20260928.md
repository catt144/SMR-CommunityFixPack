# Opt-In train cargo smoke — shared sitting, 2026-09-28

Checklist ck219 routes the next owner action here because the owner plays one game
with both mods loaded. This is an Opt-In dev-hub check; no Fix Pack runtime behavior
was changed. This local receipt satisfies the checklist's pull-only Home gate.

The implementation, evidence, Mod Editor step and five-step attended smoke are in
the [Opt-In build report](B:/Dev/SMR/SMR-OptInPack/docs/agent/reports/TRAIN_CARGO_UPGRADE_20260928.md).
Re-save the Train Hub dev mod in the Mod Editor to generate the cargo upgrade's class
and code hash, restart, and use a copy of the hub/bay save. Slot 6 streams trains and
stations; slot 3 reads both upgrades, capacities and nominal speed. The sitting checks
cargo/speed, toggles and spent ownership, salvage/rebuild, save/load, and legacy bay
cargo/passengers. The report preserves each step and its falsifier.

The full desk smoke set has the known pre-existing traffic failure; desk success
does not establish native movement or old-save compatibility. Actual Mod Editor
output and attended acceptance are owed. Shared TestKit slot update: `19824ae`.
No game was launched by this task. Executed model: GPT-6 (Codex), as identified by
the session instructions; no more specific executed model ID was exposed.

## Brief 34b — Export depot reserves and station-side train spawning, 2026-10-02

Checklist ck222 routes this separate smoke here. The current TestKit slots are preloaded
for 34b; the older slot numbers above are historical. Opt-In code `2e9cf77` is desk-verified.
The owner still needs to run the source-floor and continued-traffic check, the hub's
AssignTrain refusal, and vanilla Send out Train at an ordinary station. Predictions and
click steps are in the [34b report](B:/Dev/SMR/SMR-OptInPack/docs/agent/reports/TRAIN_34B_PLAN_20261002.md),
section "Pairing-filter smoke, preloaded". That report owns the results; brief 35 owns both
configurations. No Fix Pack runtime change. Executed model: GPT-6 (Codex); no subagents.
