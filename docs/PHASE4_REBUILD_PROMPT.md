# ONE-OFF JOB — Audit Phase 4 rebuild (C1 + C2 + C4), with certification

**Assigned by the project owner, 2026-07-31, as a heavy-lifting session.** Paste
everything below into a fresh Claude Code session. **Delete this file as part of
the final commit when the job completes** (the popup audit's
`POPUP_AUDIT_PROMPT.md` set that precedent).

**Start with `git log --oneline -8` + `git pull`.** This file goes stale the
moment another session commits. If the log shows work after
`7c75887`, re-read `docs/STATUS.md` before trusting any number below.

**This is a long job — plan for it.** Work the phases in order and do not
truncate them to finish sooner; the verification is the deliverable, not
overhead attached to one. If you run short of room, **commit what is verified,
write down exactly where you stopped and what the last leg read, and hand over
cleanly** rather than rushing the remainder.

> *Editorial note for anyone revising this brief:* where it needs to describe
> the mod environment's supported API set, it **points at `ENGINE_FACTS.md`
> rather than restating the list here.** That is deliberate — one source of
> truth, and a brief that does not drift from it. Please keep it that way.

---

## What this job is

Rebuild the pack's internal scaffolding on shared core helpers, deepen the
self-checks that protect players after a future game patch, and add a surface
that reports fixes which deactivated themselves. Then **certify it** — with
evidence, not assurances.

The owner's reason for doing this **now rather than after launch**, in his own
words: *"I am picturing a real risk of regression after we launch a live mod and
risk introducing serious issues when we miss something during the implementation
of this."* Pre-launch a regression costs a test cycle. Post-launch it costs real
players' colonies. **You are doing this at the cheapest moment it will ever be
available. Do not waste that by being quick.**

**The single most important property of this work: it is BEHAVIOUR-PRESERVING.**
C2 and C4 must not change what any fix does, only how it is written and how
carefully it checks its target. C1 adds a read-only report. If at the end you
cannot demonstrate that nothing changed, the job has failed — regardless of how
clean the code looks.

---

## ⛔ SCOPE FENCE — read before anything else

**IN SCOPE, and nothing else:**

- **C2** — extract duplicated machinery into `Code/00_Core.lua` and migrate the
  call sites.
- **C4** — deepen the self-checks in the early-written files, **through** the C2
  helper (see "why they are one job" below).
- **C1** — a user-visible surface reporting fixes that deactivated themselves.

### ⚠️ CARVE-OUT — the three drone modules are NOT migrated by this job

**Do not migrate `Code/Opt_DroneOverhaul.lua`, `Code/Opt_DroneStatDials.lua` or
`Code/Fix_ExtenderFlapChurn.lua` onto the new helpers.** Leave them exactly as
they are.

Reason: a **drone dispatch rebuild is queued directly behind this job** (owner
decision 2026-07-31 — drones moved to the top of the list) and it will rewrite
or restructure those files. Migrating them now means writing them twice and
putting refactor churn into the files with the most pending change.

**They still count for the harness.** They must keep applying, keep their
statuses, and keep their reason strings — they appear in the fingerprint like
everything else. You are leaving them alone, not excluding them from
verification.

**Design the helper API so the drone rebuild can adopt it cleanly** — that
module will be written natively against whatever you produce. If a helper's
shape would be awkward for a large opt-in module with file-scope class hooks
and per-call `IsActive` gating, fix the shape now. `Opt_DroneOverhaul.lua` is
the reference for what that code looks like; read it as a *consumer* of your
API, not as a migration target.

**EXPLICITLY OUT OF SCOPE — do not do these, do not propose them mid-job:**

- **C3 module merges. BARRED.** They change module identity and therefore
  player-facing fix ids (`SMRFixPack_Disabled["<id>"]`), which live in players'
  configs and documentation after launch. The audit itself found **no fix
  redundant and no load-order sensitivity**, so the benefit is ≈0. The owner's
  standing decision is *never*, not *later*. If you find yourself wanting to
  merge two files, you have left the job.

  > **Scope note so this bar is not mis-cited later:** what C3 barred is an
  > **audit-driven merge with ≈0 benefit that breaks player-facing IDs for
  > nothing**. It is NOT a general ban on module identity ever changing. An
  > **owner-directed redesign** — specifically the queued drone rebuild, which
  > may consolidate the drone modules — is a different thing entirely, is
  > justified on its own merits, and pre-launch is exactly when ID changes are
  > free. Do not cite the C3 bar against it, and do not treat the drone
  > carve-out above as a C3 exception.
- **Any behaviour change to any fix.** If a fix looks wrong while you are in it,
  **file it in `BUGS.md` and keep going.** Do not fix it. That is the mission
  creep this project is actively fighting (`docs/FUTURE_IDEAS.md`).
- **Anything in `docs/FUTURE_IDEAS.md`.** Nothing in that file is work.
- **D08 / D06 structural.** Undecided, pending a dedicated owner conversation.
- **New fixes, new modules, new opt-in toggles.**

**If the scope grows, stop and report. A half-done in-scope job is recoverable;
an out-of-scope surprise in a 75-file refactor is not.**

---

## Why C2 and C4 are ONE job, not two

C4 means deepening the self-checks in the early files. C2 means consolidating
the self-check boilerplate. **They operate on the same code.** Measured
2026-07-31: **194 reason-return self-check sites** across the pack.

- C4 alone → you hand-write deeper checks into 194 duplicated sites, multiplying
  the duplication C2 exists to remove.
- C2 first → you write the deeper check **once** in the shared helper and every
  site inherits it.

**C2 before C4 is the only sequencing that is not self-defeating.** C1 is
independent and additive; it can land last.

---

## Read first, in this order

1. `docs/ENGINE_FACTS.md` — **the whole file.** Several behaviours here are the
   opposite of what the code suggests, and at least three of them can silently
   break this specific job (declaring-class flattening, `error()` not unwinding,
   `rawset` vs plain assignment inside the mod environment).
2. `docs/FIX_POLICY.md` — **§2 in full** (this job rewrites §2 compliance
   everywhere), plus §5, §6, §8.
3. `docs/archive/AUDIT_FINDINGS.md` — findings **C1, C2, C4** and the PLAN.
   ⚠️ Its counts are a 2026-07-29 snapshot and are **stale**; measure the
   current numbers yourself.
4. `docs/FUTURE_IDEAS.md` — the hard rule at the top, and the Phase 4 entry
   (which carries the measured duplication and the risk analysis).
5. `docs/STATUS.md` — current counts, the A/B table, the account-state warning.
6. `Code/00_Core.lua` — the file you are extending.
7. Donor patterns you will be generalising: `Fix_LastTransmissionStorage.lua`
   (the `patch()` prologue FIX_POLICY §2 names as the veto donor, and the F75 +
   B3 latch lessons in comments), `Opt_DroneOverhaul.lua` (file-scope install),
   `Fix_CrystalMysteryHang.lua` (status-gated OnMsg handlers),
   `Fix_FirstAsteroidPrefabs.lua` (the newest file — closest to the standard the
   early files should be raised to).

Game source, read-only, **never modify**:
`A:\SteamLibrary\steamapps\common\Project Spark\ModTools\Src`.

**Check `Mars.exe` is NOT running (`tasklist`) before touching loadable code.**

---

# PHASE 0 — PREFLIGHT. Certify the plan BEFORE writing any code.

**You have standing authority to conclude that part or all of this job should
not proceed.** Saying so with evidence is a successful outcome. Building
something you had doubts about is not.

## 0a. Capture the behavioural fingerprint — this is your control

Before touching a single file, run a **fixed leg** and capture, verbatim:

- the leg's own `fix pack present: N/74 fixes active` line;
- the full probe summary (`N PASS, N FAIL, N SKIP, N ERROR`) **and the
  per-probe verdict lines**;
- the complete `[CommunityFixPack]` load-time output — every `applied` and every
  `inactive (<reason>)` line, **with reason strings verbatim**.

Save it to the scratchpad as `fingerprint_before.txt` and **commit it to the
repo** under `docs/archive/` so the certification is auditable later.

**This fingerprint is the acceptance criterion for the whole job.** Not "no
FAILs" — **identical**. Every reason string, every status, every count. Any
divergence at any stage is a regression until you have explained it in writing
and the owner has accepted the explanation.

Note which configuration you measured (read the `N/74` line — the account
toggles are player state and have gone stale on this project twice).

## 0b. Answer these before proposing a design

Write the answers down. They are seeded because they are the ways this job goes
wrong quietly.

1. **The declaring-class hazard.** FIX_POLICY §2 and ENGINE_FACTS both say a
   self-check must test the class that **declares** the method — mod code runs
   before class flattening, so an inherited method reads as nil on a subclass.
   **F64 shipped broken exactly this way.** A generic `Require{}` helper makes
   it *easier* to write a check that looks right and targets the wrong class.
   **How does your design make the right thing the easy thing?** If your answer
   is "the caller passes the right class", that is not an answer.
2. **Reason strings are an interface.** 194 sites return distinct strings that
   surface in the log and in `SMRFixPack.ListFixes()`. Does your helper preserve
   them exactly? If it generates them instead, the fingerprint will diverge —
   is that divergence acceptable, and who decided?
3. **The `DataPatch` runner must reproduce two hard-won lessons**, both
   documented in `Fix_LastTransmissionStorage.lua`: the **F75 false-inactive**
   (do not latch `inactive` before `DataLoaded` has fired — the GlobalMap exists
   EMPTY beforehand) and the **B3 re-fire branch** (the engine posts
   `DataChanged(false)` right after every `DataLoaded`; finding nothing left to
   do on that pass is **SUCCESS**, not "shipped data already correct"). Show
   where each lives in your design.
4. **Veto semantics.** Verified 2026-07-31: 13 files gate an `OnMsg` handler on
   `status == "active"` without a separate `SMRFixPack_Disabled` read, and
   **none of them heal status** — so the status read already honours the veto
   (Register sets `"disabled"`). **There is no live gap.** Does your
   `WhenActive` helper preserve that, and does it still refuse to overwrite
   `"disabled"` where a handler *does* heal status?
5. **File-scope vs apply-time.** FIX_POLICY §5 requires class-method hooks in
   `Opt_` modules to install at **file scope**. Your helpers live in `00_Core`,
   which loads first — verify that ordering actually holds for every helper used
   at file scope, and say how you verified it.
6. **⚠️ C1 — can it honestly deliver what its name promises?** The audit's own
   C1 text says self-checks catch *renamed or removed* targets but **not an
   edited same-named function** — and the edited-in-place case is precisely the
   dangerous one: the pack would go on applying its `1.0.7.396349` copies to a
   game whose own code has moved, and nothing in the present design would tell
   the player that had happened. **So a "N fixes deactivated after game update" surface can
   only report what the self-checks were able to notice.** Decide and state
   plainly: what can this surface truthfully claim? If the honest version is
   narrower than the audit implies, say so — and consider whether the honest
   narrow version is still worth shipping. **Do not ship a surface that implies
   coverage it does not have.**
7. **C1 on console platforms.** FIX_POLICY §7: consoles have no developer
   console and no log access; **Mod Options is the only universal surface**.
   Where does this report actually appear for an Xbox/PlayStation/MS Store
   player? If the answer is "nowhere", say so.
8. **C4 scope.** Which files actually have shallow self-checks? Enumerate them
   before deepening anything, and state the criterion you used. "Early files" is
   not a file list.
9. **Staging.** 194 sites is a lot for one pass. Propose a staging that keeps
   every intermediate state shippable and every A/B leg meaningful. Per-wave?
   Per-helper? Justify it.
10. **Anything else that worries you.** This is the point of preflight.

## 0c. Report and hold

Post the preflight findings, the proposed design, the staging plan, and any
recommendation to reduce scope. **If a concern is serious, stop and wait for the
owner.** Otherwise proceed to Phase 1.

---

# PHASE 1..N — THE BUILD. Meticulous, staged, verified at every step.

For **each** stage in your approved staging plan, in this order, no shortcuts:

1. **Build the stage.** One helper or one coherent group of call sites.
2. **Verify statically.** Parse every touched file
   (`python` + `luaparser`, `ast.parse(open(f,encoding='utf-8-sig').read())`).
   Re-read your own diff before running anything — a refactor's bugs are the
   ones you read past.
3. **Verify the invariants by inspection**, per stage:
   - no reason string changed unless deliberately approved;
   - no self-check moved off its declaring class;
   - no handler lost its status gate, or its refusal to overwrite a
     `"disabled"` status;
   - no `%` escaping lost from any log path (`msg:gsub("%%", "%%%%")`);
   - no `rawset(_G, ...)` where an assignment is required, and vice versa;
   - `metadata.lua` `code` and `items.lua` `ModItemCode` still identical in
     content **and order** if any file was added or removed.
4. **Run an A/B leg.** Unattended, ~75 s once Mars.exe appears.
5. **Diff against `fingerprint_before.txt`.** Counts, per-probe verdicts, and
   reason strings. **Expected result: no diff at all.**
6. **If it diverges:** stop. Do not proceed to the next stage. Diagnose, and
   either fix it or report it. A divergence you cannot explain is a stop
   condition, not a curiosity.
7. **Commit the stage** with the identity below, stating what moved and what the
   leg read. **One stage per commit** — a regression in a 75-file refactor must
   stay bisectable. Push.

**Never batch stages to save time.** A leg costs ninety seconds unattended; a
regression buried in a combined commit costs a session.

---

# FINAL PHASE — RE-CERTIFY EVERYTHING, TOGETHER

Per-stage legs prove each step. This phase proves the **assembled result**, from
scratch. Do all of it even though it feels redundant — that redundancy is the
product.

1. **Re-read `git log`** between assembling conclusions and publishing them
   (standing rule, earned in the reachability audit's challenge review).
2. **Run all three legs fresh:**
   - all six toggles ON — expect **`74/74`**, `67 / 0 / 10 / 0`;
   - default config, six toggles OFF — expect **`68/74`**, `62 / 0 / 15 / 0`
     (**needs the owner to flip the toggles by hand** — the opt-in bridge is
     one-way, ON only. Ask; do not fake it);
   - **baseline**, `code` list emptied, `default_options` kept — expect
     `1 / 61 / 15 / 0`. Restore `metadata.lua` **from a saved copy, not
     `git checkout`**, and **never `git commit -a` while that edit is in the
     tree**.
   - Adjust the expected numbers only for probes you deliberately added.
3. **Full fingerprint diff** against `fingerprint_before.txt`, all three legs.
4. **Re-verify the packaging invariant**: `metadata.lua` `code` list and
   `items.lua` `ModItemCode` list identical, same order, same length.
5. **Re-run the probe-authoring audit**: every `Register(` has a matching
   explicit `return "PASS"`. A probe whose `run` falls off the end returns nil
   and `SMRTest.Run` turns that into a **SKIP with an empty message** — it looks
   deliberate. Baseline legs cannot catch it; only a fixed leg can.
6. **Mod-environment API re-check**: confirm the helpers introduced no calls
   outside the set the mod environment supports. The supported set, and the
   reasons behind it, are recorded in `ENGINE_FACTS.md` — consult it rather than
   guessing, and note that the pack's existing `Code/` was verified clean
   against it. If a helper needs something the pack has never used before, that
   is a design question, not a detail: raise it.
7. **Write the certification** (next section).
8. **Update the docs**: `STATUS.md` counts and A/B table, `docs/archive/SESSION_LOG.md`
   leg (newest first), `FUTURE_IDEAS.md` Phase 4 entry, `AUDIT_FINDINGS.md`
   C1/C2/C4 statuses, and `FABLE_NEXT_PROMPT.md` (rewrite stale blocks, no
   banner stacking). **Delete this file.** Commit, push.

---

# THE CERTIFICATION — what you must and must not claim

Write it as a section in `SESSION_LOG.md` and summarise it to the owner. Every
claim carries its evidence inline. **A certification with no named evidence is
worse than none, because it will be believed.**

**Claim only what you measured:**

- Which legs ran, which log files, what each read.
- The fingerprint diff result, stated exactly — "identical" or the itemised
  divergences with explanations.
- Which invariants you checked and how.
- What C1 can truthfully report, and what it cannot.

**You must NOT claim:**

- **"No behaviour changed."** You cannot know that from probes and legs. Probes
  drive **planted globals** (`WithGlobals`), and a stand-in cannot reach a game
  file that localised a global at load time (`local IsValid = IsValid`,
  `Colonist.lua:5`). What you *can* claim is that every fix still applies, still
  reports the same status and reason, and every probe still returns the same
  verdict. **Say the narrower true thing.**
- **Anything about a real colony or a real save.** Nothing in this job is
  playtested. Say what remains owed.
- **That C4's deeper checks work against a future patch.** They are untestable
  today by construction. Say what they would catch and what they would not.

**State the residual risk plainly.** The honest residual: a consolidated
multi-map sweep or latch whose behaviour differs only on a real colony, which
the harness cannot see. Name it. Recommend what would close it.

---

# HARD RULES AND HARNESS FACTS

**Policy**
- `FIX_POLICY.md` governs everything you write. §4a: this pack never fixes other
  mods' problems, and "for modder benefit" is not a valid reason to ship
  anything. Overridable only by asking the owner, per case.
- **Only the playtest flips a status to `tested`.** This job flips nothing.
- Mechanical repairs may land same-day **with a re-verified A/B**; redesigns go
  to the owner.

**Engine (all in `ENGINE_FACTS.md` — read it, do not re-derive)**
- Mod code loads **before** classes are built; a classdef exposes only what it
  declares itself. Self-check the **declaring** class.
- Runtime patches on a base class do not reach already-built subclasses;
  pre-build patches propagate.
- `error()`/`assert()` **report and continue** — never use them for control
  flow. Use early returns and reason strings.
- `rawset(_G, k, v)` from mod code writes only the mod's own env; plain
  assignment `_G[k] = v` reaches the real `_G`. `rawget(_G, "X")` for reads is
  fine.
- `g_Consts` and `UIColony` are GameVars — read them inside patched functions,
  never in `apply()`. `const` IS populated at mod-load time.
- Presets only exist after `DataLoaded`; the GlobalMap exists **EMPTY** before
  it, and `DataLoaded` can fire **more than once**.
- Every `ModLog` call escapes `%` — the print path formats a second time.

**Harness**
- Launch: `& "c:\program files (x86)\steam\steam.exe" -applaunch 3215050 -smrautorun`.
  A leg takes ~75 s; **Mars.exe may take minutes to appear — never kill on a
  short timeout.**
- Logs: `%AppData%\Surviving Mars Relaunched\logs`. **Capture the newest log
  name BEFORE launching** — the game creates its log immediately, so a naive
  "wait for a new file" poll waits forever on a file that already exists.
- **Read the leg's own `fix pack present: N/74 fixes active` line** to learn
  which configuration you measured. Account toggles and dials are
  player-persistent and have gone stale on this project twice in one day.
- Known-benign noise: ~48-60 `Flight.lua objects_to_mark` errors, a few GameInit
  nil-call lines, two `ResManager` `LawOfficeDoor` missing-animation lines, and
  a `[mod] Error in mod … Test Kit` line at quit (shutdown artifact).
- Parse sweep: `python` + `luaparser`.
- Docs: never round-trip through PowerShell 5.1 `Get-Content` without
  `-Encoding UTF8` at both ends. Prefer the editor's file tools.

**Git**
- Commit with
  `git -c user.name="SMR-BugFixPack" -c user.email="154917955+catt144@users.noreply.github.com"`.
- Push the fix pack; the **TestKit stays local-only**.
- Commit messages via `git commit -F <file>` — embedded double quotes split
  arguments under PowerShell 5.1.

---

# STOP CONDITIONS — report, do not push through

- Preflight concludes the plan is unsound, or question 6 (C1's honesty) has no
  good answer.
- Any fingerprint divergence you cannot explain.
- Scope growth of any kind.
- A defect discovered in an existing fix — **file it, do not fix it**.
- The owner is needed for the default-config leg and is unavailable — do the
  rest, report the gap, do not fabricate the numbers.

**Report honestly at the end even if the news is bad.** A refactor that was
attempted and backed out with a clear explanation is a good outcome. A refactor
that shipped on an unverified claim is the failure this whole job exists to
avoid.

---

## Note for the owner (not for the agent)

**Sequencing SETTLED 2026-07-31: Phase 4 runs first**, with the drone modules
carved out of the migration (see the carve-out in the scope fence). The drone
dispatch rebuild follows immediately behind it and is written natively against
the helpers this job produces, so no file is written twice. D10 and D12 also
land on the finished substrate. PT-59 (F83's keyboard A/B) is short,
independent, and owed regardless of ordering.
