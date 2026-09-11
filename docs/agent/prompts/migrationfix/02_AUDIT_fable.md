# 02 · TERMINAL AUDIT (fable) — grade the build, and surface-sweep Astra's findings

**Link 2 of 2, the terminal adversarial backward QA** of the `migrationfix` mini chain
(map: `migrationfix/README.md`). Written **2026-09-11** by `smr-bugfixpack-cb`; **staleness anchor: HEAD was
`33b9f8e`** — `git pull` + `git log --oneline -20` first, and read `migrationfix/README.md`'s **HANDOFF** section,
which link 01 wrote for you.
⚠️ **Keep a live todo list from your first tool call.**

> ⚖️ **OWNER, 2026-09-11.** Opus builds from the audit's report; you check **both** the build **and** Astra's
> findings underneath it. ⚖️ Explicitly scoped: **a surface sweep / logic check, NOT a re-run of Astra's deep
> dive.** You are not being asked to re-derive the migration audit. You are being asked whether its conclusions
> follow from what it cites.

> 🔒 **YOU ARE THE UPLOAD GATE.** The owner ships after this link, not before. A refutation here costs a revert,
> which is cheap — a refutation after upload costs a release. So **refuse to be reassuring**: this tier's value
> on a self-correcting executor is *certification plus residue*, not rescue, and a clean bill of health you
> cannot defend is worse than an honest list of open points.
>
> 🛑 **You may STOP at any point and report a concern — and you may recommend the repair shape, or recommend
> retirement, if the evidence says so. See "Stop authority" at the foot of this file BEFORE you start.**

## 0 · Trust nothing forward

Link 01's close-out, `bugs/F59.md`, `bugs/F60.md`, the report, and this prompt are all **claims**. So is the
re-derivation in `bugs/F59.md`'s last two sections — written by a Claude session, and it too can be wrong.
Verify from the shipped tree, `1.1.0.403908`, not from any document's citation of it.
⛔ `git status` before any write: peers edit this tree and Astra (Codex) is invisible to `ListAgents`.

## 1 · Grade the build (primary job)

**A · F59's repair.** The acceptance conditions are in link 01 §A; judge against those, not against how neat the
diff looks.
1. **Do both harms actually stop?** Run `python tools/desk_f59_expedition.py` and
   `python tools/desk_f59_interact.py`. ⛔ **A harness that cannot fail is not evidence** — for each harm the
   build claims to fix, confirm there is a leg that FAILS on the unrepaired module, and check it by actually
   reverting the guard in memory or in a scratch copy. A suite that passes with and without the fix has measured
   nothing.
2. **Is the ordinary benefit intact?** This is the trap. The module exists to offer a freed bed immediately
   instead of after `Clamp(#Colonist/300, 0, 12)` hours (`City.lua:117-119` → `Colonist:Idle` `:2338-2358`). A
   guard that is slightly too wide turns the fix into a silent removal that still passes a "no harm" test.
   **Find the widest input that now suppresses a notification vanilla would have wanted**, and say whether it is
   reachable.
3. **The caller enumeration** (`FIX_POLICY.md` §4, the rule this module's own failure produced). Link 01 owes a
   per-caller answer for all 11 sites. Spot-check at least `Colonist.lua:435`, `Residence.lua:157`, `:265`,
   `:348` and `Residence:OnDestroyed:81-92`. `:265` was ruled SAFE and `OnDestroyed` was left as an UNRESOLVED
   lead — check both rulings rather than inheriting them.
4. `parsecheck`, `bodycheck`, `doccheck` GREEN; `FIX_POLICY` §2b manifest re-pinned if a target moved; §3a
   save-safety; H-02 untouched (no `version` edit, no Mod Editor).

**B · F60's retirement, if link 01 shipped it.** This is the least-checked thing in the release: a REMOVE whose
verdict is single-sourced from Astra and whose trace link 01 wrote while building. **Grade the trace, not the
recommendation.** Is the named replacement body actually reached on the live path? Are the residuals complete —
what does the module still change that nothing else now does? Did a name that reads as "gone" merely move?
⛔ If you cannot sustain the trace, say **revert B, ship A** — that is a normal outcome, not a failure of the night.

## 2 · Surface-sweep Astra's findings (secondary job, deliberately bounded)

`reports/MIGRATION_DEV_REPORT.md`, eight module verdicts. **Do not re-derive them.** For each, three questions
only, and a row of the same shape for each:

1. **Does the cited line say what the report says it says?** Open the citation on `1.1.0.403908`. This is a
   read, not a derivation.
2. **Does the conclusion follow from it?** The known failure mode is a sound measurement carrying an unsound
   inference — a cross-vendor check of a Claude audit refuted four such claims on 09-09 while every measurement
   under them was correct. Mark each claim `SOURCE` or `INFERRED` yourself and disagree with the report's own
   labelling where it is wrong.
3. **Is any claim about an absence one-sided?** "Nothing calls X", "no live caller", "expired by nothing" need
   the presence side enumerated. The report has already corrected itself once on exactly this (F58's residual).

**Where the marginal value actually is, so you spend the sweep well:**
- **F60 §7 and the five PARTIAL rows (F51, F52, F53, F58, F73) are single-sourced and unchecked.** The PARTIAL
  rows are about to change what the **fix list and store card** claim to players, so a wrong one reaches the
  player surface. This is the highest-value part of your sweep.
- **F59 §1/§1a is the LOWEST value** — two independent derivations already agree and the second extended the
  first. Confirming it a third time buys little. Spend your effort on §1's *residue* instead: the in-play trigger
  frequency (nobody has reproduced either harm in a real game, on either branch) and the `OnDestroyed` lead.
- **F80 §13 is capture-before-mitigate.** Confirm nothing in this build mitigated it.

## 3 · Deliver

A report in `agent/reports/`, and **checklist 151 gets whatever the owner must decide** (never only an agent
doc). Structure:

- **Disagreements first**, as a numbered list of falsifiable claims — each with `CONFIRMED` / `REFUTED` /
  `UNRESOLVED`, a `file:line` on `1.1.0.403908`, and `SOURCE` or `INFERRED`.
- **The upload verdict, stated plainly:** ship A+B · ship A only · ship nothing. Say which, and why.
- **An ideas list**, separate from the findings, so a suggestion is never mistaken for a defect.
- **What you did not check, by NAME.** A sweep's unchecked list is where the next session's answer lives.

Then update the entries your findings touch, `doccheck` GREEN, commit by pathspec, push — and `git rm` **this
file** and `migrationfix/README.md` in the same commit if the chain is finished, or say what remains.

⛔ **Do not build the repairs you recommend.** Your job ends at the verdict; a fix for something you found goes
back to the owner as a decision, not into this commit.

## 🛑 Stop authority, and the design input the owner asked you for

⚖️ Owner, 2026-09-11: **you have the same stop-any-time authority as link 01** — *"Fable audit can do the same,
and if it finds a concern it can recommend the repair shape, or retire, if it thinks it's needed."*

So this link is **not** limited to grading. Two things are explicitly yours to say:

1. **Recommend the repair SHAPE.** If link 01's guard is wrong, too wide, or aimed at the wrong seam, say what
   shape would be right and why — at the level of *what it must key on*, not a diff. A shape you can defend from
   the shipped bodies is worth more to the owner than a bare "insufficient".
2. **Recommend RETIREMENT instead.** The owner is leaning repair and link 01 defaults to it, but that lean is not
   a ruling and you are not bound by it. If the evidence says the module cannot be guarded without gutting the
   benefit it exists to provide, **say retire, and show the reasoning.** ⚠️ The bar: `FIX_POLICY` §4a who-benefits
   — name what players lose by retiring (a freed bed offered immediately instead of after up to 12 h at 3,600+
   colonists) against what they lose by keeping it. That trade is the OWNER's to settle, so route it to
   `PLAYTEST_CHECKLIST.md` → "Decisions waiting on you" as a recommendation, never as a decision you took.

**Stop at any point** — you do not have to finish the sweep to raise something. If you find a reason the release
should not go out, say so immediately rather than banking it for the report; the owner is waiting on this link,
and a late-arriving blocker is worth less than an early one. A partial audit with an honest "I stopped here and
why" is a legitimate deliverable; so is "ship A only", or "ship nothing".
