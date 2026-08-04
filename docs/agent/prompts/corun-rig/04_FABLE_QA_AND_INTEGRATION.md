# Chain prompt 4 — adversarial QA, the economics audit, and integration

**Read `README.md` in this folder first — binding chain rules apply. You are
the terminal prompt: this folder must be EMPTY when you finish.** Unattended.
Start with `git log --oneline -10` + `git pull`. Read `CORUN_RIG_SPEC.md`
(with all corrections), both outboxes below, and the entries/checklist rows
prompts 2–3 touched.

Every "done", "PASS" and "measured" upstream is a claim. Sample against
primary evidence: the archived run logs, the raw evidence cards, Src for any
route sentence, and git for the commit discipline (probe sweeps present,
TEMPORARY probes actually deleted, riders actually struck).

**If the kill-gate fired at prompt 2:** your job shrinks to auditing what was
learned, writing the post-mortem INTO `CHAIN_METHOD.md` (the gate working is a
method success — record it as one), routing the respec/descope/abandon
decision to the owner, and emptying the folder. Skip jobs 3–4 below.

## Jobs

**Job 1 — todo list up front.**

**Job 2 — audit the run record.** Verdict-by-verdict: does the cited log line
say what the entry now says? Are forced/organic labels present and honest?
Did any recorded number get rounded into a lie? Was the F11 `tested` grant
inside its rider's terms? Drift-evidence rule: corrections visible, never
silent.

**Job 3 — the economics audit (the owner's actual question).** From recorded
actuals: fixed cost per sitting, marginal cost per payload item,
owner-minutes used vs. the old all-owner way, and the honest verdict — does
the rig buy the owner's time back, at what batch size, and where is the
break-even? If the answer is "not really", say so plainly; the owner asked
for effort/usage/risks, not advocacy.

**Job 4 — finalize the sign-off tiers and ROUTE them.** Against the real
evidence cards from prompt 3: would the cards alone have settled the Tier A
items (prompt 3's honest note bears on this)? Is the classification rule
applicable without judgment? Then package the tier system as an owner
decision on the checklist — recommendation, what changes (which future items
stop needing per-item sign-off; what the owner reads instead; the veto
surface), and what does NOT change without their word (`tested` still means
what WORKFLOW says until they adopt the tiers). ⛔ You may not adopt the
tiers yourself; routing with a recommendation is the whole of your authority.

**Job 5 — integrate.** `CORUN_RIG_SPEC.md`'s surviving content moves to its
permanent homes: the run procedure to `PLAYTEST_HELP.md` (with EXECUTED-ONCE
markers on what actually ran — the standing rule), the envelope + tier
material to `WORKFLOW.md` "Co-runs" (amend, don't duplicate), rider-class
conventions to the checklist if prompts 2–3 changed them. STATE.md: chain
CLOSED line (cap 60, evict in-commit). SESSION_LOG: the chain's record,
newest-first. `CHAIN_METHOD.md`: what this chain teaches (a kill-gated
build chain is a new shape — §5 candidate).

⛔ **ANTI-SPRAWL RULE (owner, 2026-08-04 — the restructure was hard-won).**
This chain may create NO new standing document, folder, or document class.
Evidence cards are TRANSIENT sign-off artifacts: their surviving content is
the entry's citation of raw log lines plus the archived log (R8), never a
cards/ collection. Tier C digests live on existing surfaces (the checklist or
`ListFixes`-style output), not a new doc. The owner-facing surface remains
exactly `PLAYTEST_CHECKLIST.md` + `PLAYTEST_HELP.md`. If something genuinely
seems to need a new home, that is an owner decision — ROUTE it, do not create
it.

**Job 6 — close the chain.** Delete `CORUN_RIG_SPEC.md`, this file and
`README.md`; folder gone. Same commit carries the outcome where it will be
found. Then report to the owner: what ran, what it cost them vs. promised,
what the rig can and cannot do, the tier recommendation awaiting their word,
and what is owed (unrun riders, the F99 discriminator pricing).

## Stop conditions

- A recorded verdict fails its audit and the discrepancy is load-bearing →
  correct visibly, and if the correction changes a rider outcome or a
  `tested` grant, re-route that item to the owner rather than re-granting it
  yourself.
- Prompts 2–3 disagree with the spec on a cost or capability and you cannot
  settle it from the logs → route both readings; do not average them.

## ⛔ What you may not claim

- Not that the tiers are in force — routed is the terminal state this chain
  can reach.
- Not rig capabilities beyond what actually ran (the envelope's
  VERIFIED-IN-SRC bins stay unproven until a run exercises them; say which
  still are).
- Not owner-time savings beyond the measured sittings — one data point is a
  data point; call it that.

## Notes from upstream

*(Prompts 2 and 3 append here. On a kill, prompt 2's post-mortem lands here
directly and this prompt runs in its reduced form.)*

*(2026-08-04, prompt 2 — Opus. **The gate did NOT fire: co-run #0 is PASS WITH
CORRECTIONS**, so you run in full. Your primary evidence is `CORUN_RIG_SPEC.md`
§8 and `docs/archive/corun0_Mars.exe-20260804-10.51.15.log`; prompt 3's outbox
will follow. Three items are handed to you directly — the first two are yours to
FIX or ROUTE, the third is yours to ADJUDICATE.)*

- ***⚖️ C5 — DECIDED AND IN FORCE, BUT THE OWNER HAS EXPLICITLY ASKED YOU TO
  RECHECK IT. This is a named job, not permission to bikeshed.*** Owner,
  2026-08-04, on being shown the decision as committed: ***"flag probe gate
  issue for 04 QA to recheck your findings, my decision, but let it know I am
  open to recommendations."*** So **both layers are in scope for your audit**:
  prompt 2's *diagnosis*, and the *rule* adopted on top of it. The rule stays in
  force while you work — it is not suspended pending your verdict — and if you
  find something better you **ROUTE it with a recommendation**, which the owner
  has pre-committed to reading.

  **What was decided.** The tool was NOT loosened: no declared-probe hatch in
  `doccheck.py`, sweep stays absolute, `--no-verify` explicitly rejected
  (its documented meaning would be a false statement). The protocol tightened
  instead — **`WORKFLOW.md` probe hygiene rule 5: a probe file is present in
  `Code/` only while its run is actually happening.** Prep commits the probe's
  source as a fenced block in the brief; the file lands in `Code/` at the
  sitting and dies in the commit recording its answer. Rejected alternatives, so
  you can see the space rather than just the winner: (a) a declared-probe
  manifest the sweep reads; (b) an explicit `--declare <file>` argument the
  commit body must quote.

  ***RECHECK 1 — is the diagnosis even right?*** Verify from primary sources,
  not from prompt 2's summary: that `temporary_sweep()`
  (`tools/doccheck.py:501-517`) really has no conditional path; that
  `tools/hooks/pre-commit` really blocks on red; that `WORKFLOW.md`'s CLEAN
  definition really carries the "or declared" clause prompt 2 quoted. If any of
  those is misread, the whole decision rests on nothing and the owner needs to
  know that first.

  ***RECHECK 2 — the load-bearing claim prompt 2 did NOT verify, and says so.***
  The rule's entire safety argument is that a probe parked in a doc is **inert by
  construction** because the mod loads only files listed in `metadata.lua`
  `code`. Prompt 2 asserted this from `95_AutoRun.lua`'s header (mod code cannot
  test for a file's existence — the sandbox removes every `Async*` file API) plus
  the items.lua/metadata sync rule, and **did not confirm from `Mod.lua` that
  `ModsLoadCode` reads only the `code` list.** ⚠️ Tagged as a ROUTE claim per R3.
  Note the narrower version is much safer and may be all that is needed: a file
  **outside `Code/` entirely** is not loaded by anything, whatever the loader
  does with `Code/`. Confirm which version the rule actually needs, and say so.

  ***RECHECK 3 — the strongest objections to the rule, found by prompt 2 against
  its own recommendation. Do not treat these as settled.***
  - **It moves probe authoring next to the attended window.** The parse sweep is
    binding before every launch and can only run on a real file, so a syntax
    error in the committed *text* is now discovered at the sitting rather than in
    prep. ⭐ Candidate mitigation worth testing: during prep, paste the file in,
    run the parse sweep, delete it again, and record `parse sweep GREEN on the
    committed source at <sha>`. That restores the check to prep at zero risk —
    but it is untested and adds a step someone can skip.
  - **It forbids a class of instrument the project actually uses.** An
    instrument meant to ride along through the owner's ORGANIC play for days
    (C41's `F76MISS` hook is this shape) cannot exist as a `TEMPORARY` file
    under rule 5. Prompt 2's reading is that this is the rule working, not
    failing — armed instrumentation running during organic play IS the
    2026-07-31 contamination — and that such instruments belong in
    `90_Loggers.lua` behind an explicit on/off toggle, permanent and
    non-`TEMPORARY` by design. **Test that reading.** If it holds, say it in
    `WORKFLOW.md` so the next session does not read rule 5 as banning
    long-lived instruments outright.
  - **Nothing verifies the TestKit working tree afterwards.** A probe placed and
    deleted leaves that repo clean, but no gate checks — same blind spot as the
    stranded `96_AutoRunFlag.lua` edit below. The two items may share one fix.

  ***RECHECK 4 — integration hygiene, regardless of your verdict.*** Rule 5 and
  the amended co-run bullet must say the same thing; nothing else in the docs may
  still imply prep can commit an armed probe; **and every `--no-verify` since
  2026-08-04 must be accounted for** — see the override below, which is the only
  authorised one.

  ***RECHECK 5 — the override, and the natural experiment it creates.*** The
  owner granted **prompt 3 a one-time override of rule 5 for its prep only**
  (2026-08-04), letting it commit armed probes under five conditions: one named
  commit, `--no-verify` authorised for that commit alone with a body stating
  exactly what is red and why, **a hard disarm-before-session-end deadline**,
  a `PROBE SWEEP: armed: …, owner override 2026-08-04` line, and rule 2
  untouched. **Audit every condition against git** — especially the disarm
  deadline, which is the condition the grant's safety rests on. ⛔ The grant is
  **not precedent** (FIX_POLICY §4a procedure: never inferred, never carried to
  a second case); if any later work cites it as one, that is a finding.
  ⭐ **And it hands you evidence you would otherwise have had to guess at:**
  prompt 3 is the only session ever to work under the override, and is required
  to report whether armed prep actually bought anything over committing the
  scripts as fenced blocks and pasting them at the sitting. **That report is a
  direct input to RECHECK 3 — use it rather than reasoning about it.** Little
  bought → rule 5 stands as written. A lot bought → the case for a permanent,
  accident-proof hatch is real, and routing it is what the owner opened the door
  for.

  ⛔ **Tiebreak if you are torn:** the owner's stated priority was **safety over
  convenience**, in their own words *"I do not want to get back into the
  situations where armed probes start giving us false problems or issues."* A
  recommendation that is more convenient and slightly less safe is not
  responsive to what was asked. One that is *equally* safe and less awkward is
  exactly what they opened the door for.
  `WORKFLOW.md` "Probe hygiene" defines CLEAN as *"zero hits, **or** every hit is
  a probe that THIS session's test design explicitly declares it needs — named in
  the brief and in the todo list."* `doccheck.py`'s `temporary_sweep()`
  (`tools/doccheck.py:501-517`) implements **only the first half** — any hit is
  RED, unconditionally — and `tools/hooks/pre-commit` blocks on RED. **Net
  effect: a session may legitimately arm a declared probe, but may not commit
  anything while it is armed.** Co-run #0 is the first job to arm a probe since
  doccheck landed (2026-08-03), so it is the first to hit this; it survived only
  because the owner was free immediately, letting prep and results land in one
  commit with the probe already deleted. **Any co-run whose sitting is scheduled
  rather than immediate is blocked today** — which is precisely the shape the
  co-run protocol is built around ("all prep is unattended and happens BEFORE the
  owner sits down"). ⛔ **`--no-verify` is NOT the answer**: the hook documents
  its meaning as *"the docs are inconsistent, I know"*, which would be a false
  statement in the record. Options as they look from here, unranked — **audit
  them, do not inherit them**: (a) a declared-probe manifest the sweep reads
  (a `PROBE SWEEP:` line's own syntax already exists — reuse it rather than
  invent); (b) an explicit `--declare <file>` argument the commit body must
  quote; (c) accept the constraint and make "prep and run land in one commit" a
  binding rule of the co-run protocol, which is arguably the safer discipline and
  costs nothing when the sitting is same-session. ⚠️ Whatever you choose, the
  hatch must not be openable by accident — the sweep exists because probes were
  armed for days in 2026-07-31, and a hatch that a hurried session can reach
  without saying so re-creates that failure.

- ***📋 A vanilla defect found in our own run log — FILED AND CLOSED as `C44`
  (`wontfix`) on the owner's word, 2026-08-04. Nothing is owed; it is listed
  here only so you do not mistake it for an open thread.*** Two
  `[ResManager Error] Cannot find file with base path:
  Animations/LawOfficeDoor_idle.hgacl` / `_opening.hgacl` lines. **MEASURED
  scope: universal, once per process, independent of the save.** Across all 19
  `Mars.exe`/`MarsDebug.exe` logs on this machine the correlation is exact —
  **2 lines in every session that enters a game map, 0 in every session that does
  not**, and always exactly 2 no matter how many maps load. They fire inside the
  engine's own `*** Reloading assets from folder 'BinAssets/'` pass, in the
  MarsDebug synthetic-map session as well as retail campaign ones, so it is
  **not** save-specific and does not require a Law Office to exist. Source:
  `LawOffice` is a building of the sole `DLC/thomas` content pack with
  `entity = "LawOffice"` (`DLC/thomas/Code/BuildingTemplate/LawOffice.generated.
  lua:33`); the two clips are for its attached `LawOfficeDoor` entity and are
  referenced by the shipped asset manifest but absent from the shipped packs.
  ⛔ **Not fixable by this pack under any circumstances** — it is a missing
  binary asset, and we patch Lua at runtime; we cannot ship an `.hgacl`.
  **Owner's answer, 2026-08-04: file it with a wontfix tag and a reason "so
  another agent doesn't get distracted by it again."** Done — `agent/bugs/C44.md`
  opens with a STOP HERE banner saying exactly that. ⚠️ **Your only job here is
  to make sure that banner works**: if anything in the docs still reads as an
  open investigation, kill it. The failure mode this row exists to prevent is a
  future session re-deriving a universal, unfixable, cosmetic asset error.

- ***🔍 AN ORPHANED EDIT IN THE TESTKIT REPO — the owner has explicitly ASKED
  YOU to investigate it rather than have it committed.*** Owner, 2026-08-04:
  *"I don't know what this … is or where it came from and if you don't either I
  would be more comfortable having 04 investigate instead of committing and
  forgetting."* Prompt 2 had offered to commit it standalone; **that offer was
  declined and the item is yours.** ⛔ **Do not commit it as housekeeping.**

  **The thing:** `C:\Dev\SMR-BugFixPack-TestKit\Code\96_AutoRunFlag.lua` carries
  an uncommitted working-tree change — a comment-only block stating the
  SETUP-ONLY procedure is EXECUTED ONCE (87 PASS / 0 FAIL / 0 SKIP, log
  `MarsDebug.exe-20260803-23.14.05`) plus a warning that the synthetic map throws
  modal asserts (`Flight.lua:465/:479`) that retail swallows.

  **Provenance, MEASURED by prompt 2 so you do not re-derive it** (all four
  independently checkable):
  1. File `LastWriteTime` **and** `CreationTime` are both **2026-08-03
     23:20:03** — identical, so the file was written whole, not edited in place.
  2. The MarsDebug log it cites last wrote at **23:19:43** — the edit landed
     **20 seconds** after that session went quiet.
  3. That log genuinely contains `---- 87 PASS, 0 FAIL, 0 SKIP, 0 ERROR ----`.
     **The comment's factual claim is TRUE**, verified against the primary
     source, not against the comment.
  4. The **pack** repo was committing right through that window — `0dec7f0` at
     23:22:16 and `b1d2c3d` at 23:24:55, both recording that same MarsDebug
     pass — while the **TestKit** repo's HEAD is still `ab3111b` from **13:25**
     the same day. No stash, no other refs, exactly one modified file.
  5. ⭐ **The tally itself identifies the run, with no timestamp involved — the
     OWNER spotted this, not prompt 2** (2026-08-04): *"thats a 0 fail 0 skip 0
     error. That must mean it was from our final testing run of the night last
     night when we did the debug mode test. otherwise we would have skips."*
     **Verified across the whole log corpus and it is exact:** every retail
     `Mars.exe` RunAll caps at **78 PASS / 0 FAIL / 9 SKIP**, and the single
     MarsDebug run is the only **0 SKIP** result anywhere. **78 + 9 = 87.** The
     9 are the `[install]` probes needing `debug.getinfo`, which the retail
     sandbox never exposes (EF-006/EF-010; `00_TestCore.lua` header) — so
     `0 SKIP` is reachable *only* by a human typing
     `SMRTest.EnableIntrospection(debug)` into an asserts-build console. The
     comment could not have come from any other run.

  **⚠️ What (5) adds beyond confirming the run.** A MarsDebug `[install]` pass
  is **attended by construction** (§1 P9: modal `Assert failed` dialogs, and the
  introspection bridge cannot be automated from mod code), so **the owner was at
  the keyboard when that marker was written.**

  ⛔ **CORRECTION, and it cuts against prompt 2's own argument — the owner caught
  it** (2026-08-04): *"when I say last run of the night I mean last run of my
  play sitting, this chain build out was running and prepping after that."*
  Prompt 2 had written that the session *"kept committing for another three
  hours … without ever returning to the TestKit"* and read that as strong
  evidence of oversight. **That was wrong, because it assumed one continuous
  session where there were at least three separate efforts**, and the commit
  messages say so plainly:
  - **The play sitting closes at ~23:25.** `0dec7f0` (23:22:16) records the
    87/87 result itself; `b1d2c3d` (23:24:55) is literally titled *"The sitting
    closes…"*. **That ~5-minute window — not three hours — is the only one in
    which forgetting the TestKit is meaningful.**
  - `28c253f` (23:26) → `4898757` (00:01) is the **f11-f99-review chain**, a
    different job.
  - `c731d4a` (01:04) → `39c5dfe` (02:39) is the **corun-rig chain build-out**,
    a third.

  **Those later phases had no reason to be in the TestKit at all, so their
  silence is not evidence of anything.** The honest inference is therefore
  narrower and weaker than prompt 2 first wrote it: *the play sitting's own
  close-out commit went in without the TestKit, about five minutes after the
  marker was written.* Still consistent with an oversight, no longer the strong
  case it was presented as. **Weigh it at that strength, not the one it was
  first given.**

  **ROUTE claim, tagged separately from those citations per R3 — and it is the
  only thing left open:** the play sitting that ran the `[install]` pass wrote
  the marker immediately after its run, then closed itself out ~5 minutes later
  by committing the **pack** repo only — i.e. it forgot the second repo. Timing
  and tally are solid; **the session-shape argument is much weaker than prompt 2
  first claimed and has been corrected above.** None of it establishes intent —
  nothing rules out a deliberate deferral, and no session note anywhere mentions
  the file.
  **That adjudication is your job**, and it is the reason the owner declined a
  quiet commit. ⚠️ **Note what the alternative would have cost:** committing it
  as housekeeping would have made all five facts above unrecoverable from git in
  a single stroke — the mtime, the 20-second gap, the orphan state itself. The
  owner's *"I would be more comfortable having 04 investigate instead of
  committing and forgetting"* is why the evidence still exists for you to weigh.

  ⭐ **Nothing is at risk while you decide.** The fact itself is already recorded
  in `PLAYTEST_HELP.md` ("The MarsDebug `[install]` pass") and in `STATE.md`'s
  FIRST COMPLETE PROBE COVERAGE line. Only the in-file R2 marker is orphaned, so
  there is no urgency pushing you toward a hasty answer.

  **⚠️ And the systemic finding is now MEASURED, not hypothetical: the TestKit
  is a second repo that nothing checks.** `doccheck.py` reads its `Code/` for the
  TEMPORARY sweep and the probe count, but **no gate anywhere verifies its
  working tree is clean**, so a session can strand work there indefinitely. This
  one sat for a day and surfaced only because a co-run happened to run
  `git status` in that repo. **A co-run touches both repos by construction, so
  the rig makes this likelier, not less** — worth a line in whatever you
  integrate into `WORKFLOW.md`, and possibly a doccheck check, which would also
  close the override-audit gap above.
