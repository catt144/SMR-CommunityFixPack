---
name: prompt-authoring
description: Write or revise a Relaunched Fix Pack prompt or job brief for another session, with a live work list, scoped execution, evidence checks and a declared lifecycle.
---

# Author a prompt or job brief

Package the job so its next session can execute it and the owner can tell when
to step in. Include the elements below in every brief for another session.

## Work and operating boundaries

1. Require a live progress list covering the whole job before execution: one
   item per commit-and-verify unit, exactly one in progress. Expand a stage as
   soon as it splits, mark each unit complete when it finishes, and rewrite
   the list when reality changes. Put useful stable state in item text. Do not
   carry several commits behind one checkbox or update it only at the end.
2. Start execution with `git log` and `git pull`, and name the authoring commit
   against which the worker checks staleness.
3. Declare what is in and out of scope. Route an out-of-scope finding to its
   proper record; finding it does not authorize fixing it.
4. State concrete stop conditions as permission to report rather than push on.
5. If the result is a verdict or certification, name what may not be claimed.
   Require the narrower true statement when evidence cannot support the claim.
6. Declare the lifecycle: a completed one-off is consumed; a reusable prompt
   remains. Preserve an owner's explicit retention instruction. Review changed
   map descriptions through doc-editing; existence checks cannot judge meaning.
7. For a job that tests or records a test, include the probe-sweep step before
   testing and its evidence in the progress list. Apply the current attendance
   and age protocol in `docs/agent/WORKFLOW.md` under Probe hygiene. The owner's
   ck184 ruling recorded in STATE makes age/change a trigger satisfied at the
   next playtest; an agent does not refuse work or override the owner over it.
8. Declare the read path by file, not folder. Include the relevant bug/fact
   INDEX lookup route for discovering additional records; do not prescribe a
   whole-folder read.
9. Supply the derived-facts block below. It is the brief's element 9 and R-C,
   with one statement of the procedure.
10. For a one-off check, never write "play for a while first": a warmed-up save is
    the default, so state only a required deviation such as reading immediately
    after load.

## Derived facts and falsifiers

For each inherited fact, give the fact, how it was measured, its HEAD or game
build, and one command that could falsify it. Keep the phrasing bare. An empty
`git diff --stat <sha>..HEAD -- <paths>` means none of those sources needs reading;
changed groups require the appropriate re-check. A fix invalidates its own
tests: rebase harm legs on the pre-fix body and rerun the whole suite, not only
the changed leg.

Before handing off, read the brief as its next worker: can they identify the
inputs, scope, evidence, stop conditions and completion condition without
recovering this conversation? This review does not prove future invocation.
