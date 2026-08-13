# Chain prompt 6 — the terminal audit: read every surface as a player would, empty the folder

**Read `README.md` first — binding chain rules apply.** Staleness check across
all four repos, live todo list updated per item. This is the **last** prompt in
the chain: folder emptiness is your done-condition (rule 2).

## The job

The chain's manifest gives you three things to do, and the upstream notes below
add a fourth that is now the most important of them.

* **Job 1 — read every surface as a player would.** All five pages of
  `C:\Dev\SMR-CommunityMods\content\`, plus both store cards
  (`reports/STORE_FIXPACK.md`, `STORE_OPTIN.md`), in the order a real person
  meets them: card → landing page → the page that answers their question. ⛔ Not
  a rule sweep — a reading. Does a scroller decide in fifteen seconds; does a
  searcher find their bug; does an evaluator find the limits; does anyone hit a
  sentence that assumes what they do not know yet.
* **Job 2 — re-check the exposure gate.** `docs_dir: content` intact, the CI
  guard intact, nothing in the site repo that came out of a mod repo's `docs/`.
* **Job 3 — route what is left to the owner** and close the chain: the folder is
  empty when your own file is deleted.
* ⭐ **Job 4 — the CONTROL, and this chain has now been wrong twice in the same
  place.** Prompt 4's audit found nine defects six sweeps had missed; prompt 5's
  build found three more that every prior surface had carried — two of them
  fixes that **do not exist** and one causal claim that runs backwards. **Both
  were found the same way: by asking "which shipped module delivers this?"
  instead of trusting a record.** ⛔ **Run that question over everything prompt 5
  wrote that a sweep did not already re-derive**, and over the two store cards
  again. Ledger: `reports/SITE_BUILD_AUDIT.md`; ⛔ **do not open it until your own
  pass has returned**, the way prompt 4 firewalled its control.

## ⛔ What you may not do

- Publish anything, anywhere; enable Pages; create an external account.
- Upgrade any claim past `fixed` + suite + self-checks + verified save-safety
  tier by word choice. If a sentence needs evidence we do not have, cut it.
- Put an exposed-set count on any player surface, in any form.
- Lift the `MOD_DESCRIPTION.md` freeze or overturn STATE's release sequencing.
- Name or link the rescue artifact on any player surface (checklist 17,
  "build ≠ publish").

---

# Notes from upstream — prompt 5, the site build (`05_BUILD_SITE.md`, consumed 2026-08-13)

## What EXISTS now — go and look, do not take my word

Everything is in `C:\Dev\SMR-CommunityMods`, committed and pushed, **unpublished**
(`workflow_dispatch` only, Pages OFF).

| what | where | commit |
|---|---|---|
| the searchable fix list | `content/fix-list.md` — nine sections, 76 folded entries, five labelled *judgment call* | `ccc3985`, corrected `6cd015b` |
| the FAQ, **opening with job 4's hostile-reader section** | `content/faq.md` §"Something is broken and you think it might be us" — three answers, in the 22c order | `0c6c26a`, corrected `7f7feec` |
| the for-modders page (job 3) | `content/for-modders.md` — the veto with its identifier, and design hole 3 answered by refusing to invent a method | same |
| landing + installing, rewritten off the specimens | `content/index.md`, `content/install.md` | `9c027ce`, corrected `7f7feec` |
| ⭐ the sweep + arbitration ledger | `docs/agent/reports/SITE_BUILD_AUDIT.md` (this repo) | `9380783`, `d7b5059` |
| the fixture check (job 5) | `agent/prompts/CAPTURE_SITTING.md` (amended in place) + `COMBINED_SITTING.md` moment C | `9539ac0` |
| the owner ask + two awareness notes | `docs/PLAYTEST_CHECKLIST.md` item **27** | `8a8d6ce` |

## What is NOT done, explicitly

* **Nothing is published**, and no store link exists on any page. ✅ The "where do
  I send a bug report" answer WAS routed (checklist 27) and **the owner decided in
  the same session**: mod-page comments first, the project's issue tracker named
  once for reports carrying a save or a log. It is written into `faq.md`. ⛔ The
  store-page half stays a hole until upload. ⚠️ Re-check that both trackers are
  still open — the page now points a player at one.
* **No opt-in module page exists on the site.** The eight modules are described on
  their store card and reachable in the game; the site describes them only where a
  question needs them. ⚖️ Prompt 6 may rule that this is a gap.
* **`F22` has no fix-list entry of its own** (folded into the Last Transmission
  entry) — ledger R5.
* **The fix list covers 73 of the 74 registered modules, deliberately** — see the
  ledger's S1. ⛔ Do not "restore" the missing one without reading `F98` first.
* The store cards were **not edited**. One finding against them is routed to you:
  ledger **R1**.

## ⛔ RE-DERIVE THIS — inherit nothing from me

* Every count — `--emit-counts` in both mod repos at your moment.
* Checklist **27**'s state, and whether 26b's sitting has run (STATE ②). Several
  page sentences are pitched at source-tier because it had not: the console
  listing command's on-screen behaviour, the opt-in toggle flip, D13's `tested`.
* The five judgment calls, from the entries.
* **The site build itself.** `python -m pip install mkdocs-material` then
  `python -m mkdocs build --strict` in the site repo. It took one YAML fix to
  build at all; do not assume it still does.
* Whether the two GitHub issue trackers are still open (checklist 27 rests on it).

## ⛔ The one thing I would tell a successor above all else

**Ask "which shipped module delivers this?" of every player sentence.** Three of
this build's findings — two fixes that no longer exist and one that exists but
cannot reach a retail player — were invisible to prose review and obvious to that
one question. Two of the three were sitting in the frozen description, and one was
in the design report's own worked example.

## Disclosure

Eight subagent sweeps were run, each on one rule, each firewalled from the others
and from the ledger. Two were pointed at the code rather than the entries, which is
where the terminal audit said the store build under-swept, and both of those found
real defects. I re-derived every accepted finding myself before applying it; the
refusals are listed with their reasons in the ledger. The site was built locally
and its search index read to settle one design assumption by measurement rather
than by assertion.
