# Chain prompt 1 — resolve the §10.5 gap, then assemble the release descriptions

**Read `README.md` first — binding chain rules apply.** Staleness check across
all four repos; live todo list updated per item.

## Job 0 — ⛔ FIRST, the §10.5-vs-code gap (nothing below may quote either side until this is settled)

The combined sitting's finding, recorded at `agent/bugs/D13.md` ("The gap the
eyes found — owned by step ③"): **frozen spec §10.5 promises** the removal
dialog says `Removed: 2 drone stat dials (drone speed and carry capacity are
back to the game's own values) · …` — **the build prints** bare `N noun` pairs
(`10_SaveRescue.lua:512-514`, rescue repo). The player is told "2 drone stat
dials" and nothing else, for the one residue that keeps changing their game
after uninstall.

Re-derive both sides at their sources, then decide **spec-amend vs code-fix**
with these constraints on the table:

* The dialog as it prints today was **witnessed by the owner in the sitting**
  (D13 `tested` partly rides that reading). A code change re-opens the witnessed
  claim and needs a re-witness — an owner cost.
* The rescue artifact's **publish is itself conditional** (checklist 17,
  "build ≠ publish"), so the gloss's audience may never exist on a store.
* The gloss is genuinely better player text for exactly the residue the
  artifact exists for.

Decide it with evidence, write the resolution into the spec or the code (a code
change also updates the spec's §10.5 and flags the re-witness need explicitly
on the D13 entry), and if the trade grows an owner dimension — it plausibly
does, since it prices an owner re-witness — route it as one crisp checklist
line and proceed on the no-cost branch (spec-amend) marked provisional.

## Job 1 — the final description files, one per product

The frozen `docs/archive/MOD_DESCRIPTION.md` is superseded; build its
replacements as release deliverables the owner pastes from at ④:

* **Fix pack** and **opt-in**: the player text between the `═══` rules of
  `STORE_FIXPACK.md` / `STORE_OPTIN.md` is the audited source — do not re-author
  it; assemble it into the per-product release file with the holes each card's
  notes enumerate resolved to their current state (site links: exist only when
  Pages is on; store cross-links: exist only after upload — keep them as marked
  holes with the fill-in instruction beside them).
* **Rescue (+1, conditional):** draft only if it costs nothing beyond assembly,
  clearly marked with checklist 17's "build ≠ publish" — a description that may
  never be posted. If it wants new claims, stop at the skeleton.
* ⚠️ **A string drafted from the same source as a page inherits the page's
  defects** (`STORE_METADATA_STRINGS.md`'s recorded lesson). Anything you write
  that is NOT verbatim card text gets the "which shipped module delivers this?"
  question before it lands, and prompt 2 re-runs it regardless.

## Job 2 — the uninstall / disposition assembly

③ inherits, by name: D13's uninstall text, the engine-notice sentence, the
version-skew statement, the §10.5 dialog texts (as resolved by Job 0), the
27-site disposition table (`D13_EXPOSED_SET.md`), F102's disclaimer + its
now-MEASURED uninstall revert, and the suite numbers — **every one re-derived
from its source, none quoted from STATE.** Assemble the player-facing uninstall
story per product; the agent-side disposition table is referenced, never pasted
onto a player surface (rule 4).

## Job 3 — the portal-prep sheet for ④

One file the owner reads top-to-bottom at the launch sitting: per product —
what to paste where, the `metadata.lua` string state (strings applied
`1ac1187`; ⚠️ **portal character limits still unchecked** — count them now
against the limits you can verify without an account, and mark the rest as
check-at-paste), the preview-art hole (routed, commission), which links go live
in which order (upload → store links into pages → Pages on → site links into
store cards), and the EF-051 note if the Steam-Cloud untick intersects.

## Outbox

Append `## Notes from upstream` to `02_AUDIT.md`: what is DONE by file and
section, what is NOT started, every count to re-emit, the Job 0 resolution and
its evidence, anything routed. Commit, delete this file in the same commit.
