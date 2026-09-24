# hubset 07: verify every member in the game (attended)

Chain rules: [README.md](README.md). Read them, then `## Notes from upstream` below, first.
**Attended:** the owner plays; the session relays and records. Fire only after 06 has closed.

## Authority and outcome

Run the script link 06 appended below, exactly as written. End state: an archived log per run
segment, a verdict against every prediction, each member's entry updated on `main` with what the owner
watched (`tested-attended` only where the owner watched the fix work), the junction restored to the
main tree and read back, and 99's inbox holding every verdict and every drift from the script.

## Rules for the sitting

- Relay the owner's words into the log as they are spoken (`docs/agent/support/CO_RUNS.md`).
- A prediction that fails is a finding, not a retry. Record it, then carry on with the script unless it
  says the failure voids later steps.
- A member refuted here has no standing drop-or-hold rule. Record the facts, what the member still
  covers and what dropping or holding would ship, and give them to the owner.
- Restore the junction before closing, even on an aborted run, and read back where it points.

## Close-out

Archive the logs in the citing commit. Append the verdicts to 99's inbox, strike your row, `git rm`
this file, commit on `main`.

## Notes from upstream
