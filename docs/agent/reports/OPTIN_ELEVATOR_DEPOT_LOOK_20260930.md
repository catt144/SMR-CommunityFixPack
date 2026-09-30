# Opt-In Elevator Depot: attended look, 2026-09-30

ck221 routes the shared-game sitting here because the owner plays with both mods loaded.
The implementation and detailed handoff live in the Opt-In pack:
[Elevator Depot report](B:/Dev/SMR/SMR-OptInPack/docs/agent/reports/ELEVATOR_DEPOT_LOOK_20260930.md).

Owner, 2026-09-30: **"approved"** in reply to the rendered rounded portal at Assets `7f087ce`.
That approves its shape and placement. Final in-game acceptance and train movement remain open.
The prepared export retains that shell; static verification passes and the conditional motion
study clears the owner's approximately 20 m train envelope. Native motion is untested.

Next owner action: the existing EntitySpec's mesh import and mod save, then restart and a fresh
placement. The Opt-In report gives the short first batch. After the import, the agent checks
generated entity spots and the metadata code list before the train batch. Surface cabin/sound,
the vanilla train entering, descending and returning, and underground ceiling/rope checks are
still owed. A refusal, teleport, clip or stuck train is reported under brief 25's stop; no custom
train movement is authorized. No fix-pack behavior changes are part of this sitting.
