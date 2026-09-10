# 99 — the terminal audit: disbelieve the chain

⛔ ONE-SHOT: this file `git rm`s itself on close-out; the README stays as the
record with every row struck. Model: **Fable** · owner needed: raises the
kickoff · runs ONLY on a folder holding `99` + `README.md`.

> 🎯 Fresh context, trusts nothing forward. Every "done", every count, every
> `C` entry and every "nothing found" upstream is a CLAIM. Your two rulings:
> **were the instruments sound**, and **do the findings survive re-derivation
> from the two trees**. You have room to chase — use it; the audits that paid
> compound interest produced new primary evidence because they did.

## 0 · Open in this order

`git log --oneline -30` · `git pull` · `ListAgents` · `README.md` (whole) ·
`STATE.md` · `reports/vanillahunt/TRIAGE.md` (whole) · every `bugs/C##.md`
with `updated:` inside the chain's date range (list them with `git log
--diff-filter=A -- docs/agent/bugs/` over the chain's commits) · your
`## Notes from upstream` (every link's outbox lands here — read it LAST, after
you have formed a first view from the artefacts, and say which order you
actually used). Pin check (README §0): if the buildid moved during the chain,
say which links ran against which build.

## 1 · 🗒 Live todo list, from your first action — one item per pass

## 2 · Passes

### A · Instruments — re-falsify by hand, then plant something fresh

1. `python tools/treediff.py --selftest` and `python tools/presetdiff.py
   --selftest` GREEN — then read each fixture list against 01 §2.B.7 and 03
   §2.A: is every required case actually asserted, or merely printed?
2. **Plant a fresh change.** Copy ONE archived file pair into your scratchpad
   (⛔ never write under `SMR-SrcArchive\`), edit a body, a signature, and a
   preset value, run both tools on the scratch pair, confirm three rows.
3. **Banner integrity:** the digests in every TSV banner equal the two
   `MANIFEST.sha256` tree digests recomputed now.
4. **Soundness sample.** Pick 5 random `hand` changed files (seeded RNG, seed
   in the report) and 2 random `generated` ones; run a raw `diff` between the
   two archived copies; account for EVERY hunk with an inventory/preset row or
   with a stated imprecision (`SPAN-SUSPECT`, non-function-level text, a
   churn rule). An unaccounted hunk that changes behaviour ⇒ the instrument
   missed a class; rule **SOUND / SOUND WITH STATED GAPS / UNSOUND** and say
   which gaps.
5. The one-line-function trap: 01 measured it or did not — which, and what
   did the count do to the links' coverage claims?

### B · The controls

Seeds hit rate and self-sample agreement as the ledger states them — re-derive
both from `INVENTORY.tagged.tsv` (are the four seed rows classed right NOW?),
then **blind-reclassify 20 random `WORTH-READING`/`CHURN` rows yourself** from
the two trees and compare. A `CHURN` that was a value change is a triage miss;
count them and say what it does to every link's "reached" claim.

### C · The findings — re-derive a sample from scratch

Every `C` entry the chain filed: re-derive **at least a third, minimum 5, and
ALL rated P1/P2**, from the two trees and never from the entry's text. Per
entry: route holds / route wrong / citation wrong / recipe does not fire the
trigger / falsifier missing or non-executing / severity mis-stated / non-owner
question unanswered where DLC-adjacent. ⭐ **Try to REFUTE each** the way C54
was refuted — count the presence side, check `facts/INDEX.md`, run the
executing falsifier the other way. A refuted entry stays filed with the
refutation (C54's precedent: the reasoning error is the reusable part).

### D · Coverage — what the chain did NOT reach

Collect every link's NOT-reached section; add what the links did not admit:
03's churn classes by sample size, 07's tooling table by loader citation, 02's
`other` rows, `SPAN-SUSPECT`/`MULTI`/fpk-divergent rows, `DLC/` (by design),
and README's blind-spot list re-read in the light of the run — did the chain
learn a new one? State it. ⛔ A "nothing found" in a system is reported with
its row count and its agent count, never alone.

### E · Consistency

Ledger counts vs TSV counts; README rows struck vs prompts consumed (`git
log --diff-filter=D`); every inbox item landed, routed with TAKEABLE WHEN, or
named as dropped (a dropped item is a finding about the chain); **no status
word moved** (`git log -p` over the chain's commits on `bugs/` shows no
`status:` change except new `cand` files); **`Code/` untouched** (`git diff
--stat <chain-start>..HEAD -- Code/` empty); `items.lua`/`metadata.lua`
untouched; both archives' manifests re-hash identical (nobody wrote there);
STATE/checklist/SESSION_LOG say what the chain did and nothing more.

### F · The rulings and the owner report — `reports/vanillahunt/HUNT_AUDIT.md`

1. Instruments: SOUND / WITH GAPS / UNSOUND, with A.4's table.
2. Controls: the numbers, re-derived.
3. Findings: ranked by **player severity**, each with the non-owner sorter,
   the falsifier's state (executing / source-only / needs a game), and your
   verdict (holds / weakened / refuted). ⛔ Not a fix list — what becomes a fix
   is `FIX_POLICY` §4 + the owner: route ONE checklist decision item
   ("which of these, if any, go to a hotfix-3 candidate list") with a
   recommendation per finding, and say plainly that most will be "file and
   watch".
4. Coverage, from D, verbatim into the owner report — ⭐ *state up front what
   this hunt could not see* was part of the brief's deliverable.
5. Drift ledger: every upstream mistake the links captured (rule 5), plus
   yours.
6. **The kickoff line for `prompts/DLC_DEEP_CHECK.md`** (CHAIN_METHOD §4.6),
   pointing it at `TRIAGE.md` → "For dlccheck" as its inherited base-game
   result, and naming anything this chain learned that changes ITS shape
   (e.g. if 04 found the DLC patches base behaviour more than "mostly
   additive" allows, say so — that brief's §6 asks for exactly that signal).

## 3 · Scope fence

**In:** A–F, `HUNT_AUDIT.md`, refutation edits to chain-filed `C` entries
(with the refutation dated, never a deletion), the routed decision item,
STATE/SESSION_LOG close-out, emptying the folder. **Out:** new hunting beyond
what a re-derivation needs (a new finding you stumble on is filed as `cand`
with "found by the audit, un-audited" on it); any `Code/` edit; any status
word; the DLC chain's authoring (you write its kickoff LINE, not its chain).

## 4 · Stop conditions

Pass A rules UNSOUND — STOP after writing the ruling and route "re-run the
inventory with the fixed instrument" as an owner decision; do not audit
findings built on an unsound inventory as if they stood · a seed row is
misclassed in the tagged TSV NOW (the control was scored on something else —
say so, re-score) · the folder holds more than `99` + README (a link did not
close; STOP AND ASK).

## 5 · What may NOT be claimed

That the game is clean in any system. That a source-read finding is
reproduced. That coverage exceeds the sampled fraction (say the fraction).
That a refutation of one entry generalises. That the instrument is sound
beyond the sampled files and the stated regex. `tested`, ever.

## 6 · Close-out

`HUNT_AUDIT.md` committed; every chain-filed entry it touched updated;
checklist decision item routed with recommendation; STATE.md one line (measure
the cap — rule 13), SESSION_LOG entry (`tags:` line, pointers, the grave
`git show <sha>:docs/agent/prompts/vanillahunt/99_TERMINAL_AUDIT.md`); README
row 99 struck with the verdict word and the report path; `git rm` this file;
explicit-path `git add`; doccheck GREEN; commit `-F`; push. The owner report
ends with the `DLC_DEEP_CHECK.md` kickoff line, or says why it should not fire.

## Notes from upstream

*(authoring session, 2026-09-09/10)* Placed on the top tier per README §1's
placement note. Nothing has run; the three seeds and their expected classes
are in README §4 and their pins in 01's inbox. The authoring session's own
numbers (README §0 shape table) were produced by a declaration-line regex and
a manifest comparison, not by `treediff` — if 01's inventory disagrees with
them, 01 is right and the README table is the drift.
