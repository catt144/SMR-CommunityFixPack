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

**Owner-present PASS, 2026-10-02:** brief 34b Fix 1 (Export reserves) and Fix 2 (hub refusal /
ordinary-station train spawning), log `Mars.exe-20261002-20.42.08-6aba6e65.log`. Completed
ck222 is in `docs/archive/PLAYTEST_ARCHIVE.md`. Opt-In gameplay build `2e9cf77`, TestKit
`8408566`; commands, hashes, reconciled counts and PASS scope are in the
[34b report](B:/Dev/SMR/SMR-OptInPack/docs/agent/reports/TRAIN_34B_PLAN_20261002.md),
section "Sitting 2 PASS". STREAM's zero below-Desired pickups covers its armed windows;
the witness's eight flags fall in the autosave gap and remain a save-leg finding for brief 35.
They are not reservation-only flags. The report judges the bounded retry cost without
proposing a trim. Matcher rule candidate [EF-120](../facts/EF-120.md) is allocated here and
mirrored to Opt-In. Slot 7 cargo trap and slot 9 STREAM stay preloaded for brief 35, which
owns the full shipping battery and both configurations. The orchestrator closes 34b.
No Fix Pack runtime change in this close-out. Executed model: GPT-6 (Codex); no subagents.
