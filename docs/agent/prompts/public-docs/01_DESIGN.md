# Chain prompt 1 — the public-docs design: who reads what, where it lives, and how to beat TL;DR

**Read `README.md` first — binding chain rules apply, especially rule 4 (player
language) and the ⛔⛔ exposure hazard.** Staleness check across all three repos,
live todo list updated per item.

**You are DESIGNING, not writing the pages.** The deliverable is decisions with
reasons, an honest inventory, and a seed of each surface — enough that prompts 3
and 4 assemble rather than invent. ⛔ **Do not draft 74 fix blurbs here.** Draft
FIVE as specimens and prove the format works on the hardest cases.

---

## Job 0 — read the constraints before deciding anything

`STATE.md` · `docs/README.md` (the folder contract) ·
`docs/archive/MOD_DESCRIPTION.md` (748 lines, FROZEN, the existing tone) ·
`docs/PLAYTEST_CHECKLIST.md` "Decisions waiting on you" (the relabel package,
decisions 14/15/17/20) · a sample of 10 `docs/agent/bugs/` entries across F/D/C ·
the opt-in repo's `README.md` + `PROVENANCE.md` §3 (placeholder display names).

⛔ **Re-derive the counts with `python tools/doccheck.py --emit-counts` in both
repos.** The prose numbers in this chain's README are claims.

---

## Job 1 — the audience split, and it is the whole design

Three readers arrive by different doors and want different things. Name them,
then decide what each surface owes each one:

* **The scroller** — sees the Paradox Mods card, gives you ~15 seconds. Wants:
  what is this, is it safe for my 300-sol save, will it change my game's balance.
  **If they do not get all three in the first screen, they leave.**
* **The searcher** — has a specific bug and wants to know if it is fixed. This is
  the biggest group after launch and the store page CANNOT serve them: 74 fixes
  is not a readable list, it is a database.
* **The evaluator** — a careful player or another modder. Wants the reasoning,
  the compatibility story, the uninstall truth. Small group, high influence,
  writes the forum replies that everyone else reads.

⭐ **Reframe the owner's question deliberately.** They asked "do we need a
separate FAQ, like the big mod creators?" The FAQ is not the interesting surface.
Those creators split docs off because the store description is one unformatted
blob with a length limit and no search — the split is forced by the *platform*,
not by having many mods. Our shape is the opposite (two large mods), and our real
problem is **the searcher**: a 74-item list nobody can scan. Say so plainly, and
decide the surface set on that basis rather than by copying the pattern.

---

## Job 2 — ✅ PLATFORM DECIDED; what is left is TOPOLOGY

⭐ **The owner ruled GitHub Pages on 2026-08-13. Do not re-open it.** A working
scaffold already exists at `public-site/` (MkDocs + Material, deploy workflow at
`.github/workflows/publish-site.yml`, manual-trigger only). Your job is the
question the scaffold deliberately left open.

⛔ **Re-read the README's exposure hazard first.** The scaffold enforces it two
ways — `docs_dir: content` in `mkdocs.yml`, and a build step that FAILS if that
line changes or any path escapes `public-site/`. Keep both. `docs/` root
membership is separately enforced by doccheck against `docs/README.md`'s map,
which is why the site sits at repo root rather than inside `docs/`.

**⚖️ THE OPEN QUESTION — which repo hosts the site?** It is genuinely open and it
is the owner's:

* **Stay in the fix pack repo** (where the scaffold is now). Zero new repos.
  ⚠️ But this repo IS the mod — the junction points the game's Mods folder at it,
  so the site ships inside the fix pack's folder and counts toward what gets
  packaged for the portal. And the URL reads
  `catt144.github.io/SMR-CommunityFixPack/` for a site that also documents the
  opt-in pack, which is lopsided.
* **Its own repo** (e.g. `SMR-CommunityMods`) — ⭐ **the recommendation.** One
  site serving BOTH shipped mods and the D13 rescue artifact when it lands; a
  neutral URL; nothing ships inside either mod; and the exposure gate becomes
  structural rather than configured, because a docs-only repo has no agent
  corpus to leak. This is also the peer pattern: "Dash's Vault" is one site with
  a mod tree under it, not a site per mod. Cost: 15 seconds of owner time, and
  the scaffold moves with a `git mv` — it was built self-contained for exactly
  this.

⚠️ **Verify before recommending:** whether extra root folders actually reach the
uploaded package. `Mod.lua:490-521` proves they cannot be LOADED (only files
listed in `metadata.lua` `code` execute), but "inert at load" and "not in the
upload" are different claims and only the first is proven.

---

## Job 3 — the honest content inventory

Table, one row per surface, with **what already exists vs what must be written**:
the frozen `MOD_DESCRIPTION.md` is real raw material in the right voice, but it
is 748 lines, dated 2026-08-03, and its counts and F76 explainer are stale.
`docs/agent/bugs/` holds the truth per fix but in agent language.

⛔ **Size it in hours honestly, and say which parts are agent-cheap and which are
owner-expensive.** The owner's time is the scarce resource: their expensive items
here are the relabel wording, the display name, screenshots (in-game, their
hands) and the preview art. Everything else is agent work.

---

## Job 4 — the TL;DR problem, solved concretely

The owner named this directly. Design the answer, do not gesture at it:

* **Progressive disclosure in three tiers** — one sentence, then ~10 lines, then
  everything. Each tier must stand alone; a reader who stops at tier 1 should not
  be misled by what they missed.
* **Answer the install-gating questions FIRST**, above any feature list. For this
  mod they are: *is it safe for my existing save · does it change balance · do I
  need anything else · what happens if I remove it.* Three of those four have
  strong, earned answers — lead with them.
* **The searcher never scrolls a list.** Whatever the fix list becomes, the entry
  point is search or category, never "read 74 bullets".
* **Kill the count as a headline.** "74 fixes" impresses nobody and invites
  "which ones?"; a player cares whether *their* bug is in there.
* ⛔ **Rule 6 applies to phrasing, not just facts:** the frozen evidence bar is
  `fixed` + suite + self-checks + verified save-safety. Words like "proven",
  "guaranteed", "fully tested" upgrade that bar silently. Propose the vocabulary
  the surfaces are allowed to use, and the words they are not.

---

## Job 5 — the screenshot plan, for a mod that is invisible when it works

⚠️ **This is genuinely hard and the plan must admit it.** A bug fix looks like
nothing happening. Peer mods screenshot new buildings; we mostly cannot.

Derive the actually-capturable surface from the entries and name each shot's
job. Candidates to assess (verify each against its entry before promising it):
* **Mod Options** — the opt-in pack's toggles and dials. Real, visual, and it
  shows the product is configurable.
* **`ListFixes()` console output** — appeals to the evaluator, proves liveness.
  ⚠️ Decide whether a console screenshot reads as "technical and trustworthy" or
  "this mod is for programmers". It may belong on the site, not the store card.
* **Fixes with visible output** — the F102 deposit signs (new art renders), the
  dome infopanel policy rows the opt-in modules add, multiple Artificial Suns,
  command-centre numbers, graph captions. These are the only true before/after
  pairs; confirm which survived the split and which repo they now belong to.
* **The preview image** is an ART problem, not a writing one. Name it, size it,
  route it — do not pretend a screenshot substitutes.

⛔ **Every shot is owner time in-game.** Produce a shot LIST with framing notes
so one sitting captures all of them, and ⚠️ **that sitting must respect
`EF-056`** (loading a campaign copy runs its autosave and the rotation eats the
owner's autosaves — pre-copy every autosave first).

---

## Job 6 — seed the FAQ from real questions, not imagined ones

⛔ **Mine, do not invent.** Sources: `PLAYTEST_CHECKLIST.md` (every question the
owner actually asked is a question a player will ask), the `docs/agent/bugs/`
entries' own caveats, `FUTURE_IDEAS.md`, and the split's own consequences.

Questions known to be real, each with a short earned answer or a marked hole:
* Is it safe on my existing save? Can I remove it mid-game?
* What is the opt-in pack, do I need it, and does the fix pack need it?
  (⚠️ Neither needs the other — measured 2026-08-12, both directions.)
* Why did my drone dials/toggles reset? (Mod id changed at the split.)
* ⛔ **If I remove the mod with a drone dial off base, the boost stays in my
  save permanently.** Real, known, and the single most important uninstall
  caveat — checklist 17 names it as the reason the rescue artifact exists.
* Does this change balance? Why is *X* not fixed / why is *X* optional?
* Load order, and does it work with other mods?
* Console/gamepad players — anything different?
* Which game version, and what happens when the game updates?

⭐ **Then ask the harder question:** which of these belong in the store
description because they gate installation, and which belong in an FAQ because
they only matter afterwards? That split is the deliverable, not the list.

---

## Job 7 — draw the D13 seam explicitly

One short section listing, item by item: **safe to write now · write the skeleton
and mark the hole · do not touch until D13 closes.** The README states the seam;
your job is to make it operational so prompts 3 and 4 never guess.

---

## Job 9 — the third-party roster: one wording call, and it is about real people

⚠️ **Surfaced by the 2026-08-13 exposure audit** (result summarised in the
README — inherit it, but re-derive before acting on any of it).

`docs/agent/reports/BUG_LIST_AUDIT.md:355-370` is a competitive-landscape roster
that names real modders under a heading reading **"Rejected (with reasons)"** —
`Ayzo` (*"an aggregator repack"*), `Thorik` (*"AI redesigns, not defect repair,
no source"*), `Fizzle Fuze`, `akarnokd`, `FirestormMk3`, `LukeH`, and
**`Silva/Dash`** (*"content-only, both games"*).

**Read it in full before judging it.** In context it is fair and technical:
"rejected" means *rejected as a SOURCE of bug reports for our list*, not "bad
mod". Nothing there is untrue or hostile. But the header word is harsh out of
context, "repack" is loaded, and ⭐ **`Dash` is the author of the GitBook site
the owner cited as the model for this very chain** — so the odds of one of these
people reading it are not hypothetical.

* ⛔ **This is a wording call about other people's work, and it belongs to the
  owner.** Recommend, do not rewrite unasked; a recommendation already on the
  table is retitling to something like *"Not used as sources, and why"* and
  dropping "repack", which keeps every assessment and drops the verdict tone.
* ⚠️ The file is in `reports/`, **not** `archive/`, so it CAN be edited — the
  append-only rule does not protect it. That makes the decision live rather than
  academic.
* ⭐ **And it points at a rule this chain needs anyway:** the public surfaces
  will inevitably touch compatibility with other mods. Propose the standing line
  on **how we talk about other people's mods in public** — naming, comparisons,
  and whether "this fixes what mod X doesn't" is ever something we say. Get that
  right once here rather than per-page later.

## Job 8 — route the owner decisions, block on none

Expected: ✅ platform is DECIDED (Pages) — **site TOPOLOGY is not** (Job 2, and
it is already checklist item 21) · the opt-in mod's DISPLAY NAME (open since
08-12, placeholders in the opt-in repo's `PROVENANCE.md` §3) · the relabel
wording (ADOPTED 08-04, wording still owed — ⭐ draft it here so they approve
rather than compose) · **the Job 9 roster wording** · preview art.
**Each goes to `PLAYTEST_CHECKLIST.md` → "Decisions waiting on you"** (rule R10:
a decision recorded only in a report has not been asked), each with a
recommendation so the owner rules rather than designs.

---

## Close

Append Notes-from-upstream to `02_QA.md`: every decision with its reason, the
inventory with its sizing, the specimen blurbs, the FAQ seed, the screenshot
list, the D13 seam, and every hole you marked. Update `STATE.md` (this chain
becomes a real line item on the release front) and the checklist. doccheck GREEN,
commit (`-F`), push what has a remote, delete this file in the same commit.

## ⛔ What you may not do

- Publish anything, anywhere, or create an external account.
- Generate a site from `docs/` — re-read the README's exposure hazard.
- Lift the `MOD_DESCRIPTION.md` freeze or overturn STATE's release sequencing.
- Write a claim the frozen evidence bar does not support.
- Decide the display name, the relabel wording, or the platform **for** the
  owner. Recommend, with reasons, and let them rule.
