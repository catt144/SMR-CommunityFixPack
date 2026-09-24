# Train hub audit: owner sitting handoff

The Opt-In Modules audit, requested by the owner 2026-09-23, found a source
defect in the train hub dev mod's global WaitWakeup hook and fixed it in Opt-In
commit `3a0faff`. The archive-based regression fails on the old hook and passes
on the repair. No native save ran and the reported train lock-up's cause is OPEN.
This is not a fix-pack defect or a TestKit serializer verdict.

Canonical evidence, remaining audit gaps and the one-at-a-time console reads:
[Opt-In audit](B:/Dev/SMR/SMR-OptInPack/docs/agent/reports/TRAIN_HUB_AUDIT_111_20260923.md).
The active sitting is Opt-In `03_Drones/5_SMOKE_medium.md`; start with its audit
handoff rather than another meteor. Preserve the stalled save, restart the
process for the corrected code, then read train commands/routes, cross-map mouths,
hub jobs, track repairs and crossing locks. The agent reads the newest file log.

Owner checklist `ck212` lives here because the owner plays one game with both
mods loaded (Opt-In owner ruling 2026-09-18). The separate cross-map drone policy
question is Opt-In `OI-27`; it does not bind this mod. No code changed in this repo.

Executed model from the transcript: GPT-6 (Codex), no subagents. The native result
and remaining source checks must be recorded at the canonical Opt-In report.
