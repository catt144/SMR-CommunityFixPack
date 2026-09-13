# C92 — placement, assets and scope: should we fix the unreachable tech?

One-off, authored 2026-09-13 at the owner's ask. Tool-neutral (Claude or Codex).
`git rm` this file when it has reported. Defect truth: [C92](../bugs/C92.md).
Full working: [C92_INVESTIGATION.md](../reports/C92_INVESTIGATION.md) — read its
**"Addendum 2026-09-13"** first; it is the brief's evidence base.

## 0 · Orient

Follow `perma/DISPATCH.md` §0–§1 (orientation + bindings). Read `docs/agent/STATE.md`.
Run `ListAgents` — peers edit this tree concurrently and **Codex is invisible to it**;
check `git log` and `git status` before any write. Open a **live todo list** and update it
per item, not at the end: the owner reads that list to decide when to step in.

⛔ **Report only.** Do not build a module, do not modify shipped Lua, do not launch the
game without saying so first. The output is a report plus a recommendation the owner can
rule on.

⛔ **Marker obligation.** If your work moves a checklist item's status, you must also
update its `<!-- ck:N status:… owner:… -->` marker, or the generated
`docs/WAITING_ON_YOU.md` register goes silently wrong. Vocabulary is `open` · `ruled` ·
`closed` · `deferred` with `owner:yes|no`; invent nothing. A **checklist-only** edit is
regenerated with `python tools/doccheck.py --regen-waiting`, **not** `--regen`.

## 1 · What is already established — inherit, do not re-derive

Each of these is SOURCE or MEASURED in the addendum, with citations. Inheriting one costs
one verification command; re-deriving the set wastes the session.

- The flags are an **authoring leftover, not a deliberate bench** — five controls, plus
  ⭐ **the sibling cohort**: of the five law→tech conversions, four were finished (group,
  `RequireTech`, bespoke icon) and this is the only one that was not. `MartianDiet` landed
  in Breakthroughs where hidden + no connection is correct, which controls the flags.
- ⭐ **The conversion cohort is also a placement corpus for Q4** — `DroneHubEfficiency` →
  Logistics_2, `ShuttleFuelEfficiency` → Logistics_3, `SensorTowers` → Space_1. Where those
  three sit relative to their prerequisites is **evidence of how converted laws were
  placed**, and it is closer to this tech than any generic group-shape argument.
- The 1.0.7 **law → 1.1.0 tech** promotion, the obsoleted `LawDef`/`PolicyDef`, the
  savegame fixup, and the rewired consumer at `BuildingComponents.lua:1358-1364`.
- **One call finishes the wiring:** `UnlockTech(...)`,
  `CommonLua/Libs/Research/Research.lua:31-38`. It cannot self-heal (circular
  `CheckUnlockPrerequisites` ↔ `IsTechUnlocked`).
- **Localisation is complete in all 8 shipped languages**, ids new for 1.1.0.
- The **icon is a placeholder** borrowed from `AdvancedDroneDrive` — the only unrelated
  icon share among 312 distinct icons.
- **Double application** if simply unlocked: ≈+44% on underground water extractors
  against the advertised +20%.
- Tree geometry: the **6-around-an-empty-centre ring** is the normal motif, so an empty
  group centre is **not** evidence of a missing tech.

⚠️ **Game path trap, already paid for once.** `common\Surviving Mars` is app **464920,
the original game**. Ours is app **3215050**, `"installdir" "Project Spark"`. Resolve the
path from `appmanifest_3215050.acf`, never from the folder name. Archived trees:
`C:\Dev\SMR-SrcArchive\1.1.0.403908\Src` and `...\1.0.7.396349\Src`.

## 2 · The questions

### Q1 — Should we fix this at all?

Give the owner a ruling-ready recommendation, not a survey. The standing recommendation
is: **narrow achievement exemption mod-side, reachability + the lost bonus as a dev
report.** Either confirm it or refute it with reasons.

Weigh at minimum: the ship line (`fixed` + suite + self-checks + verified save-safety);
`FIX_POLICY` §2a's behaviour-test requirement for any 1.1.0-only body; whether a mod
restoring a 20% production bonus is a **bug fix or a balance change** — the pack's line is
that it repairs defects, and a defensible reading says the achievement is the defect while
the missing bonus is the vendor's to restore; and the risk that a vendor patch wiring the
tech properly would make our repair wrong (state the decline condition).

### Q2 — Does a dedicated icon asset already exist, hidden in the packs?

✅ **ANSWERED 2026-09-13 — do not re-run the enumeration, inherit it.** `Packs\UI.fpk`
is FLPK; parsing its directory table lists 5001 entries. `Icons/Research/` holds 371
assets; all **312** icons `Data/Tech.lua` references are present (zero missing), so the
instrument is sound and its negatives are real samples.

- ⛔ **No research-tree icon for this tech exists**, under any near spelling.
- ✅ **The LAW art exists in three variants** —
  `IconsRemaster/Laws/underground_exploitation_{1,2,3}.dds`.
- ⭐ **19 orphan research icons name techs that exist nowhere in the 1.1.0 tree**, and
  they have **no loc strings** — art-only, the opposite shape to this tech. ⚠️ Tested
  against 1.0.7: only **2** are genuinely techs dropped in the rebuild
  (`AdvancedLandingTechniques`, `UndergroundTrains`, both `ReconAndExpansion`); **17 match
  no tech in either version** and their origin is **NOT ESTABLISHED** — possibly
  original-game (app 464920) legacy art. Do not describe the set as rebuild debris.

⭐ **ANSWERED FURTHER — the law art is NOT the answer.** All **356** `Icon` values in
`Data/Tech.lua` point into `UI/Icons/Research/`; **zero** into `IconsRemaster/Laws/`. And
of the **five** law→tech conversions, the four finished ones each received a **brand-new
bespoke research icon under a new name** — the law art was abandoned every time. ⇒
Proposing the existing law art breaks a 356/356 convention; the expected finished state is
a bespoke research icon **that has never been drawn**.

**What is left for you on Q2**, and it is small: given the above, does a repair use the
current breakthrough placeholder, or is "no suitable icon exists" itself part of the dev
report's ask? Do the three law `.dds` variants differ in art or only in tier decoration
(never extracted or viewed)? Answer from the assets, not taste.

### Q3 — What do the tech's own code and data say about where it belongs?

Hunt for authoring hints not yet read: `Comment` / `TODO` fields on this preset and its
`Underground_1` neighbours; `SortKey`; any `Condition`; the `Effect_ModifyLabel` vs the
hardcoded consumer disagreement (the description says "underground extractors" while the
declarative effect targets only `UndergroundWaterExtractor` — which is the intended
scope?); whether the 1.0.7 law's `Prerequisite`
(`not IsGameRuleActive("NoUndergroundAndAsteroids")`) should have become a tech
`Condition` and was dropped in the port; and whether any DLC preset references it.

Also settle **what a finished wiring would have to look like**: a `RequireTech`
connection is what makes a node reachable through the tree, and a `MapPos` alone changes
nothing. Say which technology should connect **to** it.

### Q4 — Where in the web is the hole? (owner's leads — test, do not assume)

The owner read the tech-tree screen directly and offered two candidates. Both deserve a
real answer.

- **Hi-Tech I** — *"a 1 tier and the circle isn't completed."* **SOURCE: correct.**
  Hi-Tech_1 is the only group in the game whose node count equals its ring occupancy and
  is exactly one short — all 5 techs sit in the ring and the slot at **(7768, 2816)** is
  empty.
- **Industry V** — *"the final one of the industry techs and the circle doesn't look like
  it could be completed in general."* **SOURCE: correct.** Industry_5 has 4 live nodes and
  **two** empty ring slots, `(10062, 2944)` and `(9988, 2816)`, plus the obsolete
  `ClosedLoopExtraction` parked outside the ring.
- **Owner's theme reading, 2026-09-13:** Hi-Tech follows power and science; Industry is
  production. Member names bear it out, so an extractor-output buff is **Industry
  flavour**. ⇒ Hi-Tech_1's empty slot is very likely **a different missing thing** — treat
  it as a separate lead, not as this tech's home.
- ⭐ **The bridge slot.** `(9914, 3200)` is empty and touches three live techs across two
  groups: `Underground_1/UndergroundDeepMining`, `Industry_5/FactoryAI` and
  `Industry_5/ThermalCyclingDampeners`. It is not an Industry_5 ring slot.
- The preset declares `group = "Underground_1"`, whose ring is **complete (6/6)** with
  three satellites; the y=3200 satellite row has empty hexes at 9470, 9618 and 9914.

⛔ **A slot is not a placement.** Reachability comes from `RequireTech`, not position.
⛔ Do not let Q4 expand into redesigning the tech tree.

#### ⭐ Q4 is the owner's priority, and the bar is EVIDENCE, not inference

**Owner, 2026-09-13:** *"I would much prefer it find some sort of evidence over inference
of its location."* Everything offered above is geometry — a shape argument, and the
previous pass labelled it INFERRED for that reason. **Geometry alone is not an answer to
this question.** If you can only produce more inference, say so plainly and rank the
candidates with your reasoning exposed; do not dress a shape argument as a finding.

Routes that would be **actual evidence**, none of them tried yet:

- **`Packs\Data.fpk`** — the shipped preset blob. It may not be byte-identical to
  `ModTools\Src\Data\Tech.lua`; a difference, a stale field, or a leftover connection
  would be direct evidence. FLPK, so `tools/flpk_extract.py` reads it.
- **Asset ordering / mtimes inside `UI.fpk`**, and the DLC packs `norman.fpk` /
  `thomas.fpk`.
- **Any `Comment`, `TODO` or editor-metadata field** surviving on the preset or its
  neighbours (see Q3).
- **The 19 orphan research icons** (Q2): if one of them can be tied to a real cut feature,
  it may explain a hole and, by elimination, sharpen where this tech goes.

⛔ **A cross-version COORDINATE diff is impossible.** 1.0.7 has no `MapPos` on anything;
the `Tech` class, the hex grid and the group rings are all new in 1.1.0.

⭐ **But a cross-version THEME + TIER mapping is possible, and it is the best untaken
evidence route — the owner proposed it and it survives scrutiny.** 1.0.7's
`Data/TechPreset.lua` holds 264 presets carrying a `group` **theme** (`Biotech`,
`Engineering`, `Physics`, `Robotics`, `Social`, `Terraforming`, `ReconAndExpansion`,
`BuriedWonders`, `Independence`) and, on 153 of them, `position = range(a, b)` — a **tier
band**, not a coordinate — plus `SortKey` on 233.

Map 1.0.7 theme + tier band onto the 1.1.0 group each surviving tech landed in. That
recovers the **rebuild's actual placement convention from data**, and lets converted
content be placed by analogy with how other converted content was placed. ⚠️ It will not
locate this tech directly — in 1.0.7 it was a law, not a `TechPreset`, so it carries no
theme or tier forward. It constrains the answer rather than handing it over. **Say which
it did.**

⛔ **Do not try to invert `MapPos` itself.** `Data/Tech.lua` is
`GENERATED BY Tech Editor (Ctrl-Alt-T)`; `MapPos` is a `point2d` editor property
(`CommonLua/X/XPresetMap.lua:9`) that engine code only ever reads, and `Tech:SnapPos` is
an editor drag-snap helper. There is no generator or layout rule to reverse — positions
were dragged by hand, and the tree's semantics live in `RequireTech`, not in pixels.

⇒ **An honest "no positive evidence exists, here is the ranked inference and what would
falsify it" is an acceptable and useful answer.** A confident placement built on geometry
alone is not.

### Q5 — Residue risk, and clean failure when the vendor patch lands

⚠️ **Largely ANSWERED 2026-09-13 — inherit the analysis, then do the two jobs below.**
Full working in the addendum's "Residue risk, and whether each route can fail cleanly".
In short: **Route A (bypass) writes nothing to the save and declines on four behaviour
tests; Route B (finishing the work) writes self-sustaining vanilla state that neither
uninstalling the pack nor patching the game removes.** The unlock persists via
`PresetLockStates` on the `Player`; research completion persists in `tech_researched`;
and the +20% consumer is **vanilla code**, so the bonus keeps applying with our pack gone.
Worst case is a vendor *retirement*, where the tech vanishes from the tree while the bonus
silently continues forever. (An obsolete retirement does **not** crash — checked.)

**What is left for you:**

1. ⛔ **Specify the decline test as a build requirement**, in the words a builder will
   implement. It is **not optional**: if the devs wire the tech and we keep exempting, we
   award the achievement to players who have not researched a now-reachable tech — the
   inverse defect. Behaviour test only, never a version or `LuaRevision` label
   (`FIX_POLICY` §2a). Confirm all four shapes are detectable at the seam the fix actually
   uses, and say what the fix does if the preset is **absent** rather than merely changed.
2. **Give Route B its per-site residue disposition** if you recommend it at all — §3a
   requires one per exposed site, and a layer-3 harmful residual is accepted only **paired
   with its remedy** (D13). ⛔ Do not defer a site to the cleaner in advance; that is
   explicitly not a scoping escape hatch.

⇒ Fold this into **Q1**: the residue asymmetry is an argument for the bypass that stands
independently of the reachability and loc evidence. Say whether it changes your ruling.

## 3 · Deliverable

A report at `docs/agent/reports/C92_PLACEMENT.md`, and a **decision block for the owner in
`docs/PLAYTEST_CHECKLIST.md` → "Decisions waiting on you"** (with its marker) — never only
in agent docs. Update [C92](../bugs/C92.md) if a finding changes the entry; leave its
status `cand` unless you have the evidence to move it, and if you move it, change the
front matter **and** the body heading tag.

Label every claim SOURCE / MEASURED / INFERRED, keep a **Not opened** list (it is how the
next reader finds your blind spots), and state what each refutation depends on. Run
`python tools/doccheck.py` before committing; it must be GREEN. Commit with a pathspec —
`git commit -F <msgfile> -- <paths>` — after checking `git status` for a peer's
uncommitted work on the same files.

**Open the second lead** if Q4 confirms it: Hi-Tech_1's empty ring slot may be a missing
technology in its own right. File it as its own candidate rather than folding it into C92.

## 4 · Live todo list

- [ ] 1. Orient; inherit §1 rather than re-deriving it
- [ ] 2. Q1 — should we fix it: confirm or refute the standing recommendation
- [ ] 3. Q2 — icon asset: answer with a presence control, or declare unanswerable
- [ ] 4. Q3 — authoring hints, dropped `Condition`, effect-vs-description scope
- [ ] 5. Q4 — test the owner's two leads and the bridge slot
- [ ] 5b. Q5 — decline test specified as a build requirement; Route B residue disposition
- [ ] 6. Report written; owner decision block + marker added to the checklist
- [ ] 7. Second lead (Hi-Tech_1's hole) filed or explicitly dismissed
- [ ] 8. doccheck GREEN; committed with a pathspec; this prompt `git rm`'d
