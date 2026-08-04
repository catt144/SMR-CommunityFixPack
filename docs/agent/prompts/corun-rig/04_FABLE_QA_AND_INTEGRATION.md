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

- ***⚙️ C5 — `doccheck.py` and `WORKFLOW.md` disagree about probe hygiene, and
  the tool is the stricter one. Yours to fix (job 5, integration).***
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

- ***📋 A vanilla defect found in our own run log, reported not filed — the
  owner's disposition is pending and may be waiting when you run.*** Two
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
  binary asset, and we patch Lua at runtime; we cannot ship an `.hgacl`. So the
  only question is whether the record carries it (a `C`-row, `wontfix — not
  Lua-fixable`, so a future *"the Law Office door is stuck"* report has an answer
  waiting) or not. **Asked on the checklist 2026-08-04; if the owner has since
  answered, execute their answer — if not, leave it asked, do not decide it.**

- ***🔍 Drift evidence for your job-2 audit, not mine to resolve.*** The TestKit
  repo (`C:\Dev\SMR-BugFixPack-TestKit`, own git repo, local-only) carries an
  **uncommitted working-tree edit to `Code/96_AutoRunFlag.lua`** that predates
  co-run #0 — a comment-only block added by the **2026-08-03 MarsDebug session**
  recording that the SETUP-ONLY procedure is EXECUTED ONCE (87 PASS / 0 FAIL /
  0 SKIP, log `MarsDebug.exe-20260803-23.14.05`) and warning about the modal
  asserts from the synthetic map. Prompt 2 deliberately did **not** sweep it into
  the co-run #0 commit: it is not a probe, not this chain's work, and quietly
  absorbing another session's uncommitted change into an unrelated commit is
  exactly the provenance smearing the drift-evidence rule exists to stop.
  **Two things worth your attention, and they are separate.** (1) The content
  itself is good and load-bearing — an `EXECUTED ONCE` marker per authoring rule
  R2, sitting uncommitted where a `git clone` of the TestKit would lose it; it
  should be committed **to the TestKit repo, on its own, with its own message**.
  (2) The interesting question is the one behind it: **the TestKit is a second
  repo that nothing checks.** `doccheck.py` reads its `Code/` for the TEMPORARY
  sweep and its probe count, but nothing anywhere verifies the TestKit's working
  tree is clean, so a session can leave work stranded there indefinitely and no
  gate notices. This one sat for a day and was found only because a co-run
  happened to run `git status` in that repo. **Worth a line in whatever you
  integrate into `WORKFLOW.md`** — a co-run touches both repos by construction,
  so the rig makes this more likely, not less.
