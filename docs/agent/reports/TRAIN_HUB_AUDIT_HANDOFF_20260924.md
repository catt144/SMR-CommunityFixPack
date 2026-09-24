# Train hub audit: owner sitting handoff

The Opt-In Modules audit's save repair `3a0faff` is **withdrawn**. On 2026-09-24
the owner acted on ck212: the stalled autosave and older known-good templates
asserted in `luaSPersist.cpp:1272` and crashed after Ignore All. The change had
replaced the old Lua closure at permanent `cthread.WaitWakeup` with a C function;
its source test missed old-save compatibility. This is the leading regression
hypothesis, supported by the successful template and autosave rollback controls below.
The exact pre-audit dwell closure is restored in Opt-In commit `2035dbb`. Its original
save defect remains OPEN. The train lock-up is corrected below. No fix-pack code changed.

Canonical evidence, remaining audit gaps and runnable diagnostic reads:
[Opt-In audit](B:/Dev/SMR/SMR-OptInPack/docs/agent/reports/TRAIN_HUB_AUDIT_111_20260923.md).
The owner completed ck213: after enabling mods and restarting, the version-15
template loaded without assertions and exited normally (`10.45.34-6aad2d75.log`,
archived with the canonical report). This supports the template rollback; the
original save defect remains open. The owner also completed ck214: `Autosave Sol
31(3)` loaded without assertions with Train Hub and Rail Shaft enabled; the closed
`10.49.56-6aad2d75.log` records the load and normal exit. Native reads found
opposite siding reservations mutually blocking departures, with sound tracks and
a clear crossing. HubExitClear now recognizes completed siding parking, retaining
moving/incoming/crossing and native outgoing-track exclusions. After restarting
with that correction the owner reported, "They are now unstuck." See audit §9;
physical contact/clearance was not explicitly confirmed.

The active sitting remains Opt-In `03_Drones/5_SMOKE_medium.md`. New autosaves
still log "Attempt to persist a C function" in the post-guard process; the owner
was told the error can still affect autosaves. The next blocking work is the
agent's compatible save repair, with old→new→save→reload controls. The remaining
L5 drone smoke is also owed. Input backups outside autosave rotation and crash
logs are recorded in §8; the partial post-guard log and stall probes are in §9.

ck212's failed loads, ck213/ck214's successful rollback controls and the native
departure result are recorded above; completed asks leave the checklist.
The owner checklist lives here because the owner plays one game with both
mods loaded (Opt-In owner ruling 2026-09-18). The separate cross-map drone policy
question is Opt-In `OI-27`; it does not bind this mod. No code changed in this repo.

**New candidate awaiting ck215:** the owner proposed a save-boundary guard.
Opt-In now restores the native waiter only around PersistGame and marks new
metadata so the loader selects the matching mapping. It restores the hub wrapper
after save success/failure and after load; unmarked existing hub saves retain
the old mapping. Local tests pass, including deliberately broken snapshot/load
controls, but native saving/reloading is not yet verified. The original autosave
rotated out during play and was restored byte-for-byte from the protected copy
without overwrite; the owner's named post-stuck save was also backed up. See
audit §10. Pre-wrapper unmarked hub saves remain an ambiguous older case.

Executed model from the transcript: GPT-6 (Codex), no subagents. The native result
and remaining source checks must be recorded at the canonical Opt-In report.
