# C92 — placement, assets and scope: should we fix the unreachable tech?

One-off, authored 2026-09-13 at the owner's ask. Tool-neutral (Claude or Codex).
`git rm` this file when it has reported. Defect truth: [C92](../bugs/C92.md).
Prior working: [C92_INVESTIGATION.md](../reports/C92_INVESTIGATION.md), "Addendum
2026-09-13".

## 0 · Your licence — read this before the rest

**This brief is a starting point, not a cage.** A previous session did a desk pass and
found a lot; all of it is offered so you don't repeat it, **not to fence you in**.

- ⭐ **Go anywhere and look at anything.** The game trees, the shipped packs, the loc
  exports, the save files, our own tooling, the archive, the web. Nothing is out of bounds
  because this brief failed to mention it.
- ⭐ **Form and chase your own hypotheses.** The five questions below are the owner's
  framing, not a syllabus. If you find a better question, answer that one too and say why
  it is better. If the real story turns out to be something nobody here considered, that
  finding is worth more than a tidy answer to Q1–Q5.
- ⭐ **Everything in §1 and every "answered" note below is a CLAIM, including the parts
  written confidently.** House doctrine (`CLAUDE.md`): authored text — a peer's report,
  your own earlier output, or this brief — is a claim, not a derived fact. **Test what
  matters to your conclusion; overturn what is wrong.** The previous pass corrected itself
  twice (wrong game install; an overstated "no cross-version diff is possible"). Assume a
  third error is in here and go looking for it.
- ⭐ **Disagreement is a deliverable.** If you refute something here, lead the report with
  it. "The prior pass was wrong about X" beats five confirmed answers.
- ⭐ **Re-derive anything you doubt.** §1 exists to save you time *if you want it saved*.
  It is not an instruction to trust it. Checking a load-bearing claim is the house rule,
  not a deviation from it.

**The few genuinely binding things** are house process, not limits on thinking:

- ⛔ **Report only.** No module built, no shipped Lua modified, no game launched without
  asking first — it is the owner's rig and their time. You may *propose* any of them.
- ⛔ **Negative-evidence discipline** (`EF-088`): "not found" inside a compressed pack is
  **no sample** unless a presence control resolved through the same instrument. This has
  already cost this investigation real time twice.
- ⛔ **Shared tree.** Peers edit it concurrently and **Codex is invisible to `ListAgents`**.
  Check `git log` / `git status` before any write; commit with a pathspec.
- ⛔ **Marker obligation.** If you move a checklist item's status, update its
  `<!-- ck:N status:… owner:… -->` marker or the generated `docs/WAITING_ON_YOU.md` goes
  silently wrong. Vocabulary is `open` · `ruled` · `closed` · `deferred` with
  `owner:yes|no`. A **checklist-only** edit regenerates with
  `python tools/doccheck.py --regen-waiting`, not `--regen`.

## 0.5 · Orient

`perma/DISPATCH.md` §0–§1 is the orientation and the bindings. Read `docs/agent/STATE.md`.
Open a **live todo list** and update it per item — the owner reads it to decide when to
step in. §4 has a starting list; **change it as your understanding changes**, and add
items for hypotheses of your own.

## 1 · What a previous pass found — all of it a claim, offered to save you time

⚠️ **Game path, worth having before you start:** `common\Surviving Mars` is app **464920,
the ORIGINAL game**, not ours. Relaunched is app **3215050**, `"installdir"
"Project Spark"` — resolve it from `appmanifest_3215050.acf`, never from the folder name.
Archived trees: `C:\Dev\SMR-SrcArchive\1.1.0.403908\Src` and `...\1.0.7.396349\Src`. The
previous pass burned six commands on this and produced confident, meaningless negatives.

Claims, each with citations in the addendum:

- The hidden/`Unknown` flags are an **authoring leftover, not a deliberate bench** — five
  controls, plus **the sibling cohort**: of five law→tech conversions, four were finished
  (group, `RequireTech`, bespoke icon) and this is the only one that was not. `MartianDiet`
  landed in Breakthroughs where hidden + no connection is *correct*, which controls the
  flag reading.
- That cohort is also a **placement corpus**: `DroneHubEfficiency` → Logistics_2,
  `ShuttleFuelEfficiency` → Logistics_3, `SensorTowers` → Space_1.
- The 1.0.7 **law → 1.1.0 tech** promotion, the obsoleted `LawDef`/`PolicyDef`, the
  savegame fixup, and the rewired consumer at `BuildingComponents.lua:1358-1364`.
- **One call finishes the wiring:** `UnlockTech(...)`,
  `CommonLua/Libs/Research/Research.lua:31-38`. It cannot self-heal —
  `CheckUnlockPrerequisites` and `IsTechUnlocked` are circular for a tech with no
  `RequireTech`.
- **Localisation is complete in all 8 shipped languages**, with ids new for 1.1.0.
- The icon is a **placeholder** borrowed from `AdvancedDroneDrive` — the only unrelated
  icon share among 312 distinct icons.
- **Double application** if simply unlocked: ≈+44% on underground water extractors against
  the advertised +20%.
- Tree geometry: a **ring of six around an empty centre** is the normal motif, so an empty
  group centre is not by itself evidence of a missing tech.

## 2 · The owner's questions

*Five questions the owner asked. Answer them — and if your own line of enquiry is better,
follow it and say so.*

### Q1 — Should we fix this at all?

The owner wants a ruling-ready recommendation, not a survey. The standing recommendation
is **narrow achievement exemption mod-side, reachability + the lost bonus as a dev
report** — confirm it, refute it, or replace it with a third option nobody has proposed.

Worth weighing: the ship line (`fixed` + suite + self-checks + verified save-safety);
`FIX_POLICY` §2a's behaviour-test requirement for a 1.1.0-only body; whether restoring a
20% production bonus is a **bug fix or a balance change**, given the pack repairs defects;
and what a vendor patch does to whatever we ship.

### Q2 — Does a dedicated icon asset already exist in the packs?

**Answered as far as the previous pass got — re-run it if you doubt it.** `Packs\UI.fpk`
is FLPK; `tools/flpk_extract.py` parses its directory table (5001 entries) without
extracting payloads. `Icons/Research/` holds 371 assets and all **312** icons
`Data/Tech.lua` references are present, so that instrument's negatives were real samples.

- No research-tree icon for this tech was found, under any near spelling.
- The **law art exists** in three variants:
  `IconsRemaster/Laws/underground_exploitation_{1,2,3}.dds`.
- All **356** `Icon` values in `Data/Tech.lua` point into `UI/Icons/Research/`; **zero**
  into `IconsRemaster/Laws/`. The four finished conversions each got a **new bespoke
  research icon** — the law art was abandoned every time. ⇒ The expected finished state
  is a bespoke icon **that has never been drawn**.
- **19 orphan research icons name techs absent from the 1.1.0 tree** and carry no loc
  strings. Tested against 1.0.7: only **2** are genuinely dropped techs
  (`AdvancedLandingTechniques`, `UndergroundTrains`, both `ReconAndExpansion`); **17 match
  no tech in either version** and their origin is **NOT ESTABLISHED**.

Open: does a repair use the placeholder, or is "no suitable icon exists" itself part of
the dev report's ask? Do the three law `.dds` variants differ in art or only in tier
decoration (never extracted or viewed)? **And the orphan set is an unexplored thread in
its own right** — where did 17 icons with no tech in either version come from?

### Q3 — What do the tech's own code and data say about where it belongs?

Hints not yet read: `Comment` / `TODO` fields on this preset and its `Underground_1`
neighbours; `SortKey`; any `Condition`; the `Effect_ModifyLabel`-vs-description
disagreement (the text says "underground extractors" while the declarative effect targets
only `UndergroundWaterExtractor` — which is intended?); whether the 1.0.7 law's
`Prerequisite` (`not IsGameRuleActive("NoUndergroundAndAsteroids")`) should have become a
tech `Condition` and was dropped in the port; whether any DLC preset references it.

Also worth settling: what a finished wiring would actually look like. Reachability comes
from `RequireTech`, not from `MapPos` — so **which technology should connect to it?**

### Q4 — Where in the web is the hole?

**The owner's priority, and their bar is evidence over inference:** *"I would much prefer
it find some sort of evidence over inference of its location."* Everything the previous
pass produced here is geometry — a shape argument, labelled INFERRED for that reason. An
honest *"no positive evidence exists; here is ranked inference and what would falsify it"*
is a good answer. A confident placement resting on geometry alone is not.

The owner's two leads, read off the tech-tree screen, both confirmed as real shapes:

- **Hi-Tech I** — *"a 1 tier and the circle isn't completed."* Hi-Tech_1 is the only group
  whose node count equals its ring occupancy **and** is exactly one short; the slot at
  **(7768, 2816)** is empty.
- **Industry V** — *"the circle doesn't look like it could be completed in general."*
  Industry_5 has 4 live nodes and **two** empty ring slots, `(10062, 2944)` and
  `(9988, 2816)`, plus obsolete `ClosedLoopExtraction` outside the ring.
- **Owner's theme reading:** Hi-Tech follows power and science, Industry is production;
  member names bear it out, so an extractor buff is Industry flavour. That suggests
  Hi-Tech_1's hole is **a different missing thing** — a suggestion, not a finding, and you
  may read the themes differently.
- **The bridge slot** `(9914, 3200)` is empty and touches
  `Underground_1/UndergroundDeepMining`, `Industry_5/FactoryAI` and
  `Industry_5/ThermalCyclingDampeners`.
- The preset declares `group = "Underground_1"`, whose ring is complete (6/6) with three
  satellites; the y=3200 satellite row has empty hexes at 9470, 9618 and 9914.

**Evidence routes nobody has taken yet** — add your own:

- **`Packs\Data.fpk`** — the shipped preset blob, which may not be byte-identical to
  `ModTools\Src\Data\Tech.lua`. A difference, a stale field or a leftover connection would
  be direct evidence. FLPK, so our extractor reads it.
- **Asset ordering or mtimes inside `UI.fpk`**; the DLC packs `norman.fpk` / `thomas.fpk`.
- **A 1.0.7 theme + tier mapping.** `Data/TechPreset.lua` holds 264 presets with a `group`
  theme (`Biotech`, `Engineering`, `Physics`, `Robotics`, `Social`, `Terraforming`,
  `ReconAndExpansion`, `BuriedWonders`, `Independence`), `position = range(a, b)` — a tier
  band, not a coordinate — on 153, and `SortKey` on 233. Mapping old theme+tier onto the
  1.1.0 group each surviving tech landed in recovers the rebuild's **actual placement
  convention from data**. It cannot locate this tech directly (a law in 1.0.7 carries no
  theme forward), but it constrains the answer.
- **The orphan icons**, if any can be tied to a real cut feature.

**Two walls the previous pass hit — reported so you can judge whether they are real:**

- A cross-version **coordinate** diff found nothing to diff: 1.0.7 has no `MapPos` on
  anything, and the `Tech` class, hex grid and group rings are all new in 1.1.0.
- **Inverting `MapPos` looked futile:** `Data/Tech.lua` is
  `GENERATED BY Tech Editor (Ctrl-Alt-T)`, `MapPos` is a `point2d` editor property
  (`CommonLua/X/XPresetMap.lua:9`) that engine code only reads, and `Tech:SnapPos` is a
  drag-snap helper — so positions appear hand-placed with no rule to reverse.

If you see a way past either, take it and say what the previous pass missed.

### Q5 — Residue risk, and clean failure when the vendor patch lands

Owner's question: if we **finish** the tech rather than bypass it, what is left behind when
the devs eventually fix it, and can our fix fail cleanly? The previous pass found the two
routes have opposite shapes — full working in the addendum:

- **Bypass** writes nothing to the save; residue is an achievement flag on the account. It
  can decline on four behaviour tests (tech gains `RequireTech` · stops being hidden · goes
  `Obsolete` · disappears).
- **Finishing the work** persists `PresetLockStates` on the `Player` and `tech_researched`,
  and the +20% consumer is **vanilla code** — so the bonus keeps applying with our pack
  uninstalled. Nothing undoes it. Worst case is a vendor *retirement*: the tech vanishes
  from the tree while the bonus continues silently and permanently. (An obsolete retirement
  does **not** crash — that was checked and the crash hypothesis refuted.)

Left open:

1. **Specify the decline test in the words a builder will implement**, if you recommend the
   bypass. The previous pass argues it is not optional — if the devs wire the tech and we
   keep exempting, we award the achievement to players who have not researched a
   now-reachable tech. Behaviour test, never a version or `LuaRevision` label
   (`FIX_POLICY` §2a). Confirm the shapes are detectable at the seam the fix actually uses,
   and say what happens if the preset is **absent** rather than changed. **If you think
   that argument is wrong, say so.**
2. **A per-site residue disposition** for the finish route if you recommend it — §3a wants
   one per exposed site, and a layer-3 harmful residual is accepted only paired with its
   remedy (D13), not deferred to the cleaner in advance.

## 3 · Deliverable

A report at `docs/agent/reports/C92_PLACEMENT.md`, and a **decision block for the owner in
`docs/PLAYTEST_CHECKLIST.md` → "Decisions waiting on you"** with its marker — owner
decisions never live only in agent docs. Update [C92](../bugs/C92.md) if a finding changes
it; leave `cand` unless the evidence moves it, and if it moves, change the front matter
**and** the body heading tag.

Label claims SOURCE / MEASURED / INFERRED, keep a **Not opened** list (it is how the next
reader finds your blind spots), and say what each refutation depends on. `doccheck` GREEN
before committing; commit with a pathspec after checking `git status` for a peer's
uncommitted work.

**Threads worth opening as their own candidates** rather than folding into C92, if your
work supports them: Hi-Tech_1's empty ring slot as a separate missing technology, and the
17 orphan icons with no tech in either version.

## 4 · Live todo list — change it as you go

- [ ] 1. Orient; decide which §1 claims are load-bearing for you, and test those
- [ ] 2. Q1 — confirm, refute, or replace the standing recommendation
- [ ] 3. Q2 — the open icon questions, and the orphan-set thread
- [ ] 4. Q3 — authoring hints, the dropped `Condition`, effect-vs-description scope
- [ ] 5. Q4 — the owner's leads, the untaken evidence routes, the two reported walls
- [ ] 6. Q5 — decline test in builder's words; residue disposition if recommending the finish
- [ ] 7. Your own hypotheses — add them here as you form them
- [ ] 8. Report written; owner decision block + marker on the checklist
- [ ] 9. doccheck GREEN; committed with a pathspec; this prompt `git rm`'d
