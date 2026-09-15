# support/ — prompt-supporting documents

Protocols and references used by prompts live here when they are not themselves
fired to make a session do a job. Prompts keep explicit pointers to the support
they consume; this map is updated when a supporting document lands.

| file | purpose |
|---|---|
| `README.md` | this purpose and destination map |
| `CO_RUNS.md` | binding situational protocol for co-runs: route, prepare, conduct and close attended experiment legs |
| `LIVE_SITE_READ.md` | read-only route for identifying the newest successful Pages deployment and checking live content without publishing |
| `POST_UPLOAD_CLOSE.md` | non-fireable procedure for verifying an owner-confirmed upload, preserving writeback and restoring stripped comments |
| `RELEASE_SURFACES.md` | non-fireable procedure for applying an outbox batch to player-facing surfaces and passing pre-upload gates |
| `SMRTK_SLOTS.md` | pull-only TestKit slot-construction and sitting-handoff reference |
