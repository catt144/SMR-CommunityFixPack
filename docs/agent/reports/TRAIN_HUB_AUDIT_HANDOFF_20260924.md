# Train hub audit: owner sitting handoff

The save guard `102f5f0` and siding departure fix `f556ee8` now pass their native
controls in the owner's fixture. No fix-pack runtime code changed.

Canonical evidence, protected input locations and remaining audit work:
[Opt-In audit](B:/Dev/SMR/SMR-OptInPack/docs/agent/reports/TRAIN_HUB_AUDIT_111_20260923.md),
§§8–12. The withdrawn `3a0faff`, exact rollback `2035dbb`, failed ck212 loads and
successful ck213/ck214 rollback controls remain recorded there. The owner then
confirmed, "They are now unstuck." Physical contact/clearance was not explicitly
confirmed (§9).

The owner completed ck215: legacy autosave load, 128× play through a new
autosave/reload, then a new manual save and full restart/manual reload. The
closed `12.06.00-6aad2d75.log` has no persistence/load/assert/crash failure
markers. The flushed `12.35.05` prefix confirms the fresh-process load; its game
time matches the marked manual save. §§11–12 preserve the logs, hashes, member
counts and protected artifacts. Existing ArtSpec startup and Braze network
errors remain. The completed ask leaves the checklist.

Test-shape clarification: the autosave reload was in the writer process; the
independent cold-load control used the new manual save. Both use the same
guarded snapshot/load mapping. An autosave-specific cold reload was not
separately performed. This result does not certify ambiguous pre-wrapper hub
saves, drone adoption mid-flight or the both-configuration/toggle ship matrix.
The guard preserves the old wrapper mapping for unmarked existing hub saves
and selects the native mapping for explicitly marked new saves (§10).

The active sitting remains Opt-In `03_Drones/5_SMOKE_medium.md`: resume its
remaining drone smoke and later QA. D14 stays open for the other audit findings.
The owner checklist lives here because the owner plays one game with both
mods loaded (Opt-In owner ruling 2026-09-18). Cross-map policy question Opt-In
`OI-27` does not bind this mod.

Executed model from the transcript: GPT-6 (Codex), no subagents.
