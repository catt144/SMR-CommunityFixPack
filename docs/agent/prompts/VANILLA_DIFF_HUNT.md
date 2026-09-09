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

**⏳ OWED: the 1.0.7 tree.** ⛔ **Without it there is no diff and this whole
effort collapses to a cold read of 1.1.x**, which is a far weaker exercise — say
so plainly rather than quietly doing the weaker thing. The owner can download
1.0.7 — it is a branch switch, a copy and a switch back, and **nothing in the
mod setup notices because nothing launches** (`EF-055`: the enable is lost only
when a launch runs with the id unresolvable, and the junction lives outside the
Steam directory anyway). Procedure and the `EF-075` caveat — the 1.0.7 branch is
a store-surface claim, not route-checked — are in `SMR-SrcArchive\README.md`
§"Recovering 1.0.7". ⚠️ **Confirm the 1.0.7 archive actually exists before you
author a chain that assumes it**, and check which build the flip-back landed on:
if a newer one shipped meanwhile, archive it and re-pin the diff base.

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

⛔ **State up front what this hunt CANNOT see** — data/preset changes outside
Lua, C-side behaviour, engine changes, and anything only a running game would
show. Naming that is part of the deliverable, not a caveat to bury.
