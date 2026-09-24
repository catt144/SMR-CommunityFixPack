# Train hub audit: owner sitting handoff

The Opt-In Modules audit's save repair `3a0faff` is **withdrawn**. On 2026-09-24
the owner acted on ck212: the stalled autosave and older known-good templates
asserted in `luaSPersist.cpp:1272` and crashed after Ignore All. The change had
replaced the old Lua closure at permanent `cthread.WaitWakeup` with a C function;
its source test missed old-save compatibility. This is the leading regression
hypothesis, pending native rollback confirmation, not a recovered-save verdict.
The exact pre-audit dwell closure is restored in Opt-In commit `2035dbb`. Its original
save defect and train lock-up cause remain OPEN. No fix-pack code changed.

Canonical evidence, remaining audit gaps and the one-at-a-time console reads:
[Opt-In audit](B:/Dev/SMR/SMR-OptInPack/docs/agent/reports/TRAIN_HUB_AUDIT_111_20260923.md).
The active sitting is Opt-In `03_Drones/5_SMOKE_medium.md`. Start with audit §8:
enable the original mods, fully restart, load `train_hub_base`, do not overwrite it, and exit if an assertion
appears. The agent reads the new log. Only after rollback loading is confirmed
should a compatibility repair and old→new→save→reload test proceed. Preserve the
stalled save; its command/route/job/track/lock reads and the remaining L5 smoke
are still owed. Backups outside autosave rotation and crash logs are recorded in §8.

ck212's attempted load is recorded above; the narrower rollback check is ck213.
The owner checklist lives here because the owner plays one game with both
mods loaded (Opt-In owner ruling 2026-09-18). The separate cross-map drone policy
question is Opt-In `OI-27`; it does not bind this mod. No code changed in this repo.

Executed model from the transcript: GPT-6 (Codex), no subagents. The native result
and remaining source checks must be recorded at the canonical Opt-In report.
