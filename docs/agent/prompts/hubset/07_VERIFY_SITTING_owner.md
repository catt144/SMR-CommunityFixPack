# hubset 07: verify every member in the game (attended, the chain's one sitting)

Chain rules: [README.md](README.md). Read them, then `## Notes from upstream` below, first.
**Attended:** the owner clicks preloaded SMRTK slots; the session relays, reads the log and records.
Fire only after 06 has closed. Owner ruling 2026-09-24: **"One sitting only."**

## Authority and outcome

Run the script link 06 appended below, exactly as written. End state:

- an archived log per run segment;
- a verdict against every prediction;
- each member's entry updated on `main` with what the owner watched (`tested-attended` only where the
  owner watched the fix work);
- the junction restored to the main tree and read back;
- 99's inbox holding every verdict and every drift from the script.

## Before the owner sits (this session, with the game closed)

You are the second seat on 06's script. Check it from the owner's chair before asking them to
start. If a check fails, stop and route it to the owner; do not start the sitting.

- **Clicks only.** Every owner step is a slot, trigger or panel button. Any typed line carries 06's
  stated reason. No step asks the owner to wait in real time or to watch for a state among many
  objects.
- **The slots are in place.** The TestKit HEAD and slot labels match 06's outbox. Re-run
  [tools/SMRTK.md](../../../../tools/SMRTK.md)'s "Gates" commands and require their stated results.
- **The predictions can fail.** Each prediction names its refuting result, and 06's rehearsal shows
  a scratch variant producing it.
- **The price holds.** The owner-minute total at the top of the script is the one you will quote.

Then give the owner one line: *"start the game; the Slots & notes tab is loaded"*, plus the save to
load.

## Rules for the sitting

- Relay the owner's words into the log as they are spoken (`docs/agent/support/CO_RUNS.md`).
- Read results from the log yourself. Never ask the owner to read back or paste output.
- A prediction that fails is a finding, not a retry. Record it, then carry on with the script
  unless it says the failure voids later steps.
- A slot that errors is recorded and skipped as the script directs. Do not write replacement console
  code on the spot. If the owner asks for one anyway, record its exact text in the entry that cites
  its result.
- A member refuted here has no standing drop-or-hold rule. Record the facts, what the member still
  covers and what dropping or holding would ship, and give them to the owner.
- Restore the junction before closing, even on an aborted run, and read back where it points.

## Close-out

Archive the logs in the citing commit. Append the verdicts to 99's inbox, strike your row, `git rm`
this file, and commit on `main`.

## Notes from upstream
