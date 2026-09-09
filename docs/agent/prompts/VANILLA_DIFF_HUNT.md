# VANILLA DIFF HUNT — what the 1.1.x update BROKE in the game itself

Paste into a fresh Claude Code session. Written **2026-09-08**, to fire **after
the current fix pack is patched, pushed and stable** (owner instruction).
**Start with `git log --oneline -15` + `git pull`.** Read `docs/agent/STATE.md`
(mandatory), `docs/agent/FIX_POLICY.md`, `docs/agent/reports/CHAIN_METHOD.md`.

> 🎯 **YOUR JOB IS TO AUTHOR A CHAIN, NOT TO RUN THE HUNT.** This is a handoff
> brief in the shape of `HOTFIX_2_HANDOFF.md`: it carries the preconditions, the
> method and the risk taxonomy, and you decompose it into `prompts/vanillahunt/`
> with a terminal audit. ⛔ Do not start reading diffs in this session — you will
> run out of context in the inventory and leave nothing behind.

> ⚖️ **THE THESIS, in the owner's words:** *"when they patch things they usually
> create 2 new bugs for every one they fix … they are famous for not correctly
> judging how old features will interact with new ones."*
> ⭐ **So the target is NOT "read the changelog and check it". It is the
> unannounced change and the interaction seam.** A patch note is a claim about
> intent; the diff is what actually happened.

⛔ **SCOPE: VANILLA DEFECTS, NOT OUR MODULES.** This hunt finds bugs in the
GAME. It is not a re-verification of the fix pack — that is
`PACK_1_1_0_REVERIFICATION.md` and it is done. ⚠️ A finding here is a
**candidate defect**, filed; it is **not** automatically a module. The bar for
adding a fix is `FIX_POLICY`, and it is a separate decision the owner makes.

## 0 · Preconditions — one is DONE, one is the owner's

**✅ DONE 2026-09-08: the 1.1.0 tree is archived.**
`C:\Dev\SMR-SrcArchive\1.1.0.403908\Src` — 4717 files, tree digest
`a4577da25cb3fe8586bb7388b9b557d3dfd343938e453382e65d066f1945b3b2`, Steam build
`24995074`. Manifest and the standing archive rule are in that folder's
`README.md`.

**✅ DONE 2026-09-08: the 1.0.7 tree is archived too — THIS EFFORT IS UNBLOCKED.**
`C:\Dev\SMR-SrcArchive\1.0.7.396349\Src` — 4448 files, tree digest
`09d95e3448573dc378fa0bed5fc987fead3aafb70bf2ecf6a2cddef3f1ff9921`, Steam build
`23584660`. Captured by branch-switch, copy, switch back; the game was never
launched on the old branch. ⭐ **`EF-075`'s loss is reversed** — but do NOT
renumber any existing citation; an entry records a defect in a STATED version.

⚠️ **The 1.0.7 archive's `DLC/` subtree is NOT trustworthy for diffing.** It has
12 files against 1.1.0's 151, 5 of them byte-identical — a Steam artefact of the
branch switch, not a clean 1.0.7 fact. Exclude `DLC/` from the base-game diff
and get DLC-vs-DLC facts from `DLC_DEEP_CHECK.md` instead.

**⭐ THE DIFF IS ALREADY MEASURED — start from these numbers, do not re-derive
them.** From the two manifests: **2444 files changed**, 1968 identical, **305
added**, 36 removed.

⛔ **2444 changed files is the whole argument of §1.** At ~10 seconds a file
that is a week of reading with no triage, and most of it is generated data and
churn. **The inventory is not optional.**

⭐ **THREE CLAIMS THE PROJECT COULD NEVER VERIFY ARE NOW CONFIRMED**, checked
against the archive the hour it landed. They are worth knowing because each was
load-bearing for a shipped gate or repair, and each was explicitly marked
unverifiable while the tree was gone:
- `ProcessAllElements` appears **0 times** in 1.0.7's `TrackElement.lua` and is
  called at `:475` in 1.1.0 ⇒ **`F116`'s pre-sort revalidation really is NEW**,
  which its own entry said could not be established (`EF-075`).
- 1.0.7 declares `function LandscapeForEachUnit(mark, callback, ...)` — **no
  leading `map`** ⇒ **`F115` confirmed**.
- `MultiResourceDepotBase` appears **0 times** in 1.0.7's `Station.lua` ⇒
  **`F114`'s gate discriminator is sound** on the branch it discriminates.

⇒ ⭐ **The archive paid for itself in three checks.** Treat that as the standard
for this effort: a 1.0.7-vs-1.1.x claim is now CHEAP to settle, so **never ship
one as an inference again.**

⚠️ **Version drift.** The owner refers to "1.1.1"; what is installed and
archived is **1.1.0.403908**. Do not assume a version — read the appmanifest,
pin whatever is actually there, and if a newer build has landed, ⛔ **archive it
first** (the standing rule) before doing anything else.

## 1 · Why a raw diff is the wrong instrument, and what to build instead

`Src` is 4715 `.lua` files / 36 MB. A textual diff of two trees is enormous,
mostly noise (generated files, whitespace, data churn), and **unreadable at the
altitude the owner asked for**. ⛔ Do not produce one and start reading it.

⇒ **Build a CHANGE INVENTORY at function granularity, then triage by risk
class.** The instruments already exist and were built for exactly this shape:

- **`tools/luafn.py`** — `find_bodies()` is the project's **single canonical
  body delimiter**. ⛔ A two-tree differ MUST import it, never re-implement it,
  or the two extractors disagree and every result is unfalsifiable. Its own
  header says so.
- **`tools/bodycheck.py`** — already accepts `--src <path>`, so it can be aimed
  at an archived tree. Read how it hashes a body before writing anything new.
- **`tools/sigcheck.py`** — arity only. ⛔ Never a clearance.

**The tool to write** (its own chain link): given two `Src` trees, emit one row
per top-level function that is **added / removed / body-changed / signature-
changed**, keyed by `file:function`. ⚠️ **Falsify it before trusting it** — make
it report a change you planted and miss nothing you know changed. `bodycheck.py`
has a `--selftest` falsifier; copy that discipline. *An instrument you never
watched fail is not an instrument.*

## 2 · The risk taxonomy — triage the inventory by THESE classes

Every class below is one this project has **already been bitten by in a single
update**. That is the whole argument for using them as the sort order.

| class | shape | our scar |
|---|---|---|
| **(a) body changed, name + arity identical** | invisible to every instrument we own | `F114` (157 throws, a player found it), `F116` |
| **(b) signature changed** | a parameter added, usually leading | `F115` (`map` prepended to `LandscapeForEachUnit`) |
| **(c) storage moved** | same concept, new home | `Landscapes` GameVar → MapVar; walk consts `const.` → `g_Consts` |
| **(d) RENAMED, not removed** | the name is gone, the feature is not | low-Food warning → `StarvingColonists`; `daily_update_func` → `DailyUpdate` |
| **(e) removed outright** | genuinely gone | 36 of our modules retired against this |
| **(f) new function / new call site** | new code, least-tested code | — |
| **(g) ⭐ OLD × NEW SEAM** | existing system meets new feature | **the owner's thesis — weight this highest** |

⛔ **THE METHOD RULE, learned three separate times on 2026-09-08 and it governs
every row you triage:**

> **A claim about what is ABSENT needs the presence side ENUMERATED.**
> *"grep found 0 hits"* can only prove the old **NAME** is gone — never that the
> **FEATURE** was removed. Search for the capability (the preset, the UI string,
> the voiced line, the overriding subclass), not the identifier.

The three instances, so nobody re-learns it: a "1.1.0 deleted the low-Food
warning" claim that was a rename (`C54`/ck121); a "class X no longer defines Y"
claim where the method was **inherited** from the base class and entirely intact
(F-8); and an asymmetry argument counting 36 guarded sites while never counting
the 46 unguarded ones, which inverted the conclusion (`C54`, refuted same day).

⚠️ **And check `docs/agent/facts/INDEX.md` BEFORE filing any engine-semantics
claim.** `EF-005` already answered one of the above and two sessions derived
past it. The index exists so a question is asked once.

## 3 · Where to aim first — we have a map nobody else has

⭐ **80 modules' worth of deeply-understood defect sites, plus a just-completed
read of all 80 against 1.1.0** (`PACK_1_1_0_REVERIFICATION.md`). That is a map
of this codebase's historically fragile areas — trains and tracks, landscaping,
drones and logistics, colonists and domes, construction, save/load.

⛔ **Use it to PRIORITISE, never to BOUND.** The 1.1.0 update's worst surprise
(`F114`) was in a system we knew well; that is an argument for looking there
first, not for looking there only. A hunt that only revisits our own turf will
miss everything the DLC touched.

⭐ **Cross-link with the DLC effort.** `prompts/DLC_DEEP_CHECK.md` establishes
something that matters here: the DLC's own Lua is mostly **new classes**, so
**DLC-integration bugs surface in the BASE-GAME diff, not in the DLC folder** —
the base changes made to accommodate food ship to *everyone*, DLC owner or not.
⇒ **Tag every inventory row that touches a DLC-adjacent system** (food,
farming, colonist consumption, service buildings, resources, laws, tech) and
give that set its own pass. That set is class (g), and it is where the owner's
thesis predicts the yield.

## 4 · What a finding must contain

A candidate defect entry (`docs/agent/bugs/`, `C`-series unless it is clearly
player-visible) with:

- the **route**, re-derived — ⛔ not the citation, the reasoning above it. Every
  route failure this project has had sat on individually-correct citations.
- **1.1.x file:line**, and the 1.0.7 counterpart if the archive supports it;
- **who reaches it** — a real player action, or "no reachable caller found";
- ⛔ **the falsifier**: what observation would prove this is NOT a bug. A finding
  with no falsifier is a hunch with citations.
- **severity in player terms**, and honestly: *"silent, no throw"* and
  *"cosmetic"* are real and common answers.

⛔ **Nothing is `tested`. A source read is never `tested`** — these are all
source-derived until something is reproduced in a game, and most never will be.

## 5 · Bindings

- ⛔ **Never modify the game directory.** Read-only, always. The archive exists
  so you never need to.
- ⛔ Never "correct" a 1.0.7 citation in an existing entry (`EF-075`) — an entry
  records a defect in a STATED version.
- ⛔ `H-02` no Mod Editor, no `version` edit, **no upload**. `H-08` never pull a
  junction. `H-09` never stage a packed folder beside a live one.
- ⛔ Do not add a module. This effort FILES; `FIX_POLICY` and the owner decide
  what becomes a fix, and the pack has just shed 36 modules for good reasons.
- `python tools/doccheck.py` GREEN before any doc commit; a WARN goes
  **verbatim** into your summary. `git commit -F <file>`, then push.
- ⚠️ **Several sessions edit this tree at once.** Explicit FILE paths on every
  `git add` — ⛔ never `add -A`, never a directory pathspec; both swept a peer's
  work on 2026-09-08 and a `git status` pre-check cannot close the race.

## 6 · Your deliverable

`prompts/vanillahunt/` — a chain per `CHAIN_METHOD.md`, with a README manifest,
the binding rules inherited, an inbox/outbox per link, and a **terminal
adversarial audit**. ⭐ Size the links against **one context each** and split up
front rather than mid-link: *"a chain cannot tell what its current context is"*
(owner, 2026-09-08) — that judgement is yours to make now, from outside.

A defensible first cut, to argue with rather than accept:
1. the two-tree differ + its falsifier, and the raw inventory;
2. triage into the classes in §2, counted;
3. class (g) — the DLC seam — its own link;
4. classes (a)/(b) — the invisible ones — their own link;
5. the rest, by system;
99. terminal audit: **re-derive a sample of findings from scratch**, and rule on
    whether the inventory itself was sound.

⭐ **Build the subagent fan-out of §7 into the links themselves** — the triage
link especially is a parent orchestrating agents, not a session reading rows.

⛔ **State up front what this hunt CANNOT see** — data/preset changes outside
Lua, C-side behaviour, engine changes, and anything only a running game would
show. Naming that is part of the deliverable, not a caveat to bury.

## 7 · ⭐ USE SUBAGENTS — this effort is big enough to warrant it (owner instruction)

⚖️ **Owner, 2026-09-08: where the work is large enough to warrant it, the hunts
should split it across subagents.** This one qualifies: **2444 changed files**,
and a function-level inventory over them will run to thousands of rows.

### The principle: fan out the READING, keep the JUDGEMENT central

⭐ Each agent burns a large context reading source and returns a small
structured result. That is the whole economic argument — one session cannot hold
2444 files, but it can hold 2444 *verdicts*. Design every fan-out so the parent
never has to re-read what an agent read.

### ✅ WHERE IT WORKS HERE — genuinely independent, fan out freely

- **Inventory triage.** Each changed function is independent: read the 1.0.7
  body and the 1.1.x body, classify into §2's classes, return the row. This is
  the big one and it is embarrassingly parallel.
- **A named subsystem sweep** — trains, landscaping, colonists, construction —
  one agent per subsystem, working from the inventory rows for its files.
- **Chasing one candidate to ground**: who calls this, is it reachable, what is
  the falsifier. Bounded, independent, returns a paragraph.

### ⛔ WHERE IT DOES NOT — do these yourself, in the parent

- **Building the two-tree differ and its falsifier.** One tool, one author. Two
  agents writing extractors is how you get two disagreeing body delimiters,
  which `luafn.py`'s header exists to prevent.
- **Setting or amending the taxonomy.** A classification scheme decided in
  parallel is not a scheme.
- **Synthesis, prioritisation and the verdict.** The value is in seeing the
  whole; that cannot be delegated in pieces.
- ⛔ **ANY WRITE TO A SHARED FILE.** Subagents READ and REPORT; **the parent
  writes.** Several sessions edit this tree at once and the git index is shared
  — on 2026-09-08 a directory pathspec swept a peer's untracked file. Do not add
  concurrent writers to that.

### ⛔ WHAT A SUBAGENT MUST RETURN — evidence, never a verdict alone

A row is worthless unless the parent can act on it without re-reading. Require:
**file:function · class from §2 · the 1.0.7 and 1.1.x line numbers · what
actually changed, in one sentence · who reaches it · the falsifier.**

⛔ **"Looks fine" is a rejected result.** So is "no issues found" with nothing
behind it. This project's whole method is *re-derive the route, not the
citation* — an agent that returns a conclusion without its route has produced
exactly the shallow-instrument failure the hunt exists to catch.

### ⛔ THE CONTROL — a fan-out that cannot be falsified is not evidence

**"Twelve agents found nothing" is indistinguishable from "twelve agents read
badly."** You must be able to tell those apart:

- ⭐ **Seed known positives.** `F114`, `F115` and `F116` are documented changes
  in this exact diff, with known classes. Put their functions into the fan-out
  **without telling the agent they are seeded**, and check they come back
  correctly classified. An agent pool that misses `F115`'s added `map` parameter
  is not reporting on the other 2000 rows either.
- Re-run a sample of rows in the parent and compare.
- ⚠️ **Report the control's result in the chain's output.** A hit rate on seeded
  positives is the only number that makes a "nothing found" pass meaningful.

### Practical notes

- ⛔ **`Explore` is the WRONG agent type for classification.** It reads excerpts
  to LOCATE code; it does not review it. Use it to find call sites, never to
  judge whether a body changed meaningfully. Using the wrong instrument is this
  project's recurring failure — do not commit it in the tooling itself.
- Batch sensibly: one agent per file or per subsystem, not one per function —
  spawn overhead will dominate and the parent drowns in results.
- ⚠️ **Subagents are parallelism WITHIN a link. They are not a substitute for
  splitting the chain** (`CHAIN_METHOD` rule 4) and ⛔ **not a substitute for the
  terminal audit** — a fan-out is many shallow reads, an audit is one
  adversarial fresh context. You need both.
