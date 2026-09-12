# The vanilla diff — disposition: what we do with it, how far we trust it, where it lives

**2026-09-12, session `smr-bugfixpack-b2`, firing `prompts/VANILLA_DIFF_DISPOSITION.md` (grave: the commit that lands
this file).** Desk only: no game launched; no `Code/`, `items.lua`, `metadata.lua` or public surface touched. Trees:
live `A:\SteamLibrary\steamapps\common\Project Spark\ModTools\Src` = **1.1.0.403908**; archives
`C:\Dev\SMR-SrcArchive\1.0.7.396349\Src` and `\1.1.0.403908\Src`. Verdict words: CONFIRMED / REFUTED / UNSETTLED.

**One-paragraph answer.** Keep the instruments, retire nothing. The pack-facing pair (`bodycheck` + `sigcheck`) becomes
a **binding after-every-patch step** — §3a below, now written into `WORKFLOW.md` — because the store card publishes a
recurring-process claim and the only thing that currently makes it true is a track record. The game-facing pair
(`treediff` + `presetdiff`) stays **on-trigger, not on-schedule**: its output is a 25k-row inventory that costs a chain
to read, and a chain with nobody reading it produces artefacts, not knowledge. The candidate backlog gets **one ruling
at group level**, not five open checklist items asking the same question. And the 1,281-hunk blind spot is worth
**one bounded desk session** — not because the surface is small, but because I measured which part of it touches us.

---

## 0 · What I re-derived before deciding (the brief said its numbers are claims)

| claim | source | my re-derivation | verdict |
|---|---|---|---|
| `bodycheck` exit 0, 130 rows / 48 stamped / 2 NO-MANIFEST / 1 NO-DEFECT / 7 SRC-NONE / 122 OK | brief | ran it | **CONFIRMED**, exactly |
| "all three selftests PASS" | brief | **four** tools carry `--selftest`; all four PASS (`bodycheck`, `sigcheck`, `treediff`, `presetdiff`) | **CONFIRMED and corrected** — the count is four |
| 6 of the 10 FIX rows were class c | `PACK_1_1_0_REVERIFICATION` §4 rec 3 | read it: "6 of the 10 FIX rows are wrappers or data patches (class c)" | **CONFIRMED** |
| 441 self-closing declarations, 567 spans to EOF, 79 unclassified hand rows | `HUNT_AUDIT` §1.5 | read it | **CONFIRMED** |
| "run three tools, read one table" | `PACK_1_1_0_REVERIFICATION` §4 rec 5 | the three are `sigcheck` + `logscan` + `bodycheck` — **`treediff`/`presetdiff` did not exist on 2026-09-08** | **CONFIRMED, and the brief conflates it.** The promoted rule must name today's set, not that sentence's |
| `doccheck.py` gates only `bodycheck --selftest` | brief | `tools/doccheck.py:958-992,1104` — one call, no other tool | **CONFIRMED** |
| **1,281 hunks in 368 files, 4,542 non-blank lines** | `HUNT_AUDIT` §1.4 | see below | **CONFIRMED — reproduced from scratch** |

### 0.1 The 1,281 hunks, re-derived — and why this mattered

`a4_gap.py`, the script that produced that number, **was never committed and does not exist** (`git log --all
--diff-filter=A` over `*a4_gap*`: empty; the only two mentions in the repo are the two prose references in
`HUNT_AUDIT`). The project's largest stated blind spot rested on a single session's unreproducible run.

I reimplemented the stated method from scratch (difflib opcodes over both archives, normalised CRLF→LF and trailing
whitespace, minus every `span107`/`span110` in `INVENTORY.tagged.tsv`; scratch script, nothing committed):

| | files w/ ≥1 row | files w/ unaccounted hunks | hunks | non-blank lines |
|---|---|---|---|---|
| `HUNT_AUDIT` §1.4 | 699 | 368 | 1,281 | 4,542 |
| **mine, overlap tie-break** | **699** | **378** | **1,325** | **4,653** |
| mine, strict-containment tie-break | 699 | 458 | 1,906 | 19,784 |

⭐ **The denominator matches exactly** (773 rowed hand files minus 74 that exist on only one side = 699), which is a
real control that I read the same file set. On the overlap tie-break the audit's numbers reproduce within **3%**.
⇒ **§1.4 is CONFIRMED.** Its subclass split also reproduces in rank order (table/field dominant, then other/comment,
then `GameVar`/`const`, `__parents`, `DefineClass` smallest).

⚠️ **Two corrections the re-derivation forces.**
1. The number only reproduces under **overlap**: a hunk that *partly* pokes outside a row span was counted as read.
   Under strict containment the surface is **1,906 hunks in 458 files**, so ~580 further hunks are partly outside any
   body anyone inventoried. The right statement is "**at least** 1,281", never "exactly".
2. §1.4 labels its split "916 table/field **lines**, 71 `__parents`…". Those six numbers sum to 1,281 — they are
   **hunk** counts, not line counts. Nothing downstream depends on it; the label is wrong.

### 0.2 The method note this session earned, stated narrowly

⭐ **A record that states a MEASUREMENT or a NEGATIVE cannot be tested by re-reading it.** Re-reading tells you what
the record says; only re-running tells you whether it is true. Three same-day cases, two of them mine:

* §1.4's 1,281 had been read and relayed by several documents. Re-running it **confirmed** it — and only re-running
  could have, because the script had been gone the whole time.
* A peer's correction to an unrun console recipe (checklist 147 / `C87`) asserted that a spelling was *"witnessed
  nowhere in the shipped tree"*. Re-running the search found it in **19 files**, including the recipe's own receiver
  spelling at `Landscaping.lua:225`. The original line would have run; the "repair" rested on a truncated grep.
  ⇒ ⛔ **a claim about what is ABSENT needs the presence side enumerated**, and `| head -5` is not an enumeration.
* This project's own standing git rule ("always name a pathspec", from `6ad619a`) turned out to be **half a rule** —
  a pathspec fences *other* files but takes the work-tree content of the paths it names. Found by running it, not by
  re-reading the rule. Corrected in `441cc92`.

⚠️ **The narrow form is the defensible one.** Reading records is how three of this report's findings were made at all
(the `WORKFLOW.md` procedure gap, `a4_gap.py`'s absence from git, rec 5's "three tools" being a different three). The
claim is not "records are worthless"; it is that a **number** or an **absence** in a record is a claim of the same
kind as an instrument's output, and §2.2's rule applies to it identically — including when the record is ours.

---

## 1 · Question 1 — what we do with it

### 1a · The candidate backlog — one ruling at group level, and it closes five checklist items

25 entries are open `cand` from the diff (C56–C73, C75–C76, C78–C81, C82; C74 and C77 shipped in v7). Every one is
`source-read` with no field report, no save and no log. The terminal audit already re-derived all 12 P2s and read the
12 P3s for consistency (`HUNT_AUDIT` §3), so **the expensive work is done** — what is missing is a decision.

| group | entries | what the audit found | disposition | what would change my mind |
|---|---|---|---|---|
| **A — real player-visible loss, ordinary route** | **C63, C66** (+ **C82**, filed by the audit, one read only) | C66 HOLDS (dump-one-group dumps everything); C63 HOLDS + 3 adjacent tells; C82 un-audited | **Keep `cand`. Attach as ORGANIC RIDERS** to whatever colony the owner is already playing — "if you happen to have an RC Transport carrying two resources, click one". ⛔ Never provision for them | A field report naming one; or C82 surviving a second read |
| **B — unearned GAIN (the player benefits)** | C64, C67, C75, C78, C79 | every "loss" turned out to be a gain, freedom, or a sub-percent effect | **No action, ever, absent a field report.** `FIX_POLICY` §4a's who-benefits test: fixing these takes something away for a correctness abstraction | A field report, or a save-sanitizer pass running anyway that C78 could ride along with |
| **C — weakened or refuted** | C58, C68, C69, C76, C80 | 4 WEAKENED; **C80 REFUTED** | **No fixture.** ⚠️ **C80's `status:` and its `bugs/INDEX.md` row still read `cand`** while its body carries the refutation — a status flip is owed (reported, not done: this brief is read-mostly) | — |
| **D — P3, never re-derived** | C56, C57, C59–C62, C65, C70–C73, C81 (12) | read for consistency only | **Source-only. No fixture, and no re-derivation pass either** | A field report naming one |

⭐ **The recommendation that actually saves owner time.** Checklist items **137, 138, 140, 141 and 142** are five open
questions that all reduce to "provision a fixture or leave it source-only", each with its own rider. Rule the table
above once and all five close together. The base rate argues for it: of 12 P2s re-derived at the cost of a chain link,
**zero became fixes**, and the audit's own routed recommendation was "none earns a hotfix-3 slot on today's evidence".

⛔ **What I am NOT saying.** Not that the entries are wrong — the audit found their *citations* right in 11 of 12. The
weak part was the ROUTE, and a route is settled by reading the next hop, not by playing. That is why "leave them
source-only" is a disposition and not a dismissal: the entries stay, and a field report reopens any of them instantly.

### 1b · The 1,281 unread hunks — a targeted pass, and I measured the target

Confirmed at ≥1,281 hunks / ≥368 files (§0.1). A full reading pass is **several sessions** and the base rate above says
its yield would be low. But "the largest unexamined surface" is the wrong frame for a pack that only patches 51 files.
So I asked the question that decides priority: **does it land where we patch?**

I intersected the unaccounted-hunk set with the distinct shipped files the pack's own `-- SRC:` / `-- DEFECT@` lines
pin (51 files, harvested from `Code/*.lua`):

> ⭐ **29 of the 51 files the pack pins carry unaccounted hunks — 157 of them.** `bodycheck` cannot see one, by
> construction: it hashes the pinned function *body*, and these hunks lie outside every body anyone inventoried.

Narrowing to the subclasses with a known mechanism (`__parents` / `DefineClass`), and verifying each against both trees
rather than trusting the classifier:

| pinned file | 1.0.7 → 1.1.0 | why it is not noise |
|---|---|---|
| `Lua/Units/Unit.lua:3` | `__parents` **gains `"ReactionObject"`** | the base class of every colonist, drone and rover |
| `Lua/Buildings/BaseBuilding.lua:10` | `__parents` **gains `"ReactionObject"`** | the base class of every building |
| `Lua/Buildings/WaterExtractor.lua:3` | gains `"ContinuousOps"` | a whole operating-mode component |
| `Lua/Buildings/Farm.lua` | `FarmBase` **loses `"InteriorAmbientLife"`**; a new `EntityClass, AutoAttachObject` class appears at `:3` | a parent removed, not added |
| `Lua/Mysteries/Fireflies.lua:650` | `Service` → **`DecorationService`** | a re-parent, not an addition |
| `Lua/Buildings/Residence.lua` | two `__parents` hunks in the changed block | ⚠️ UNSETTLED — the block shifted; I did not resolve which parents actually moved |
| `Lua/Buildings/Station.lua` | new `DefineClass.TrainStationDepotCCP3`, `__parents = {"Door"}` | additive on today's read |

This is the shape `EF-058` and `EF-066` say re-routes method lookup and re-composes `Init` down every descendant — and
the pack declares **105 (class, method) targets**. ⛔ **This is not a defect finding and I filed nothing.** It is an
unexamined intersection: whether any of these changes our behaviour is unread, and the pack *was* re-pinned by hand
against 1.1.0 at hotfix 2, so the modules were read once by a human even if not for this.

**Priced, three options:**

| pass | scope | cost | recommendation |
|---|---|---|---|
| **(i) pinned-file `__parents`/`DefineClass`** | the ~8 rows above | **one desk session**, both archives already on disk | ⭐ **DO IT.** It is the only slice with a release consequence, and it is bounded |
| (ii) all 157 hunks in the 29 pinned files | +`GameVar`/`const`/table-field in our own files | 1–2 desk sessions | optional; do it only if (i) finds anything |
| (iii) the full ≥1,281 | tree-wide | several sessions | ⛔ **NO.** Same yield profile as the P2 re-derivation, at ten times the cost |

⚠️ **Prerequisite either way:** the extractor must be rebuilt, because `a4_gap.py` does not exist. `HUNT_AUDIT` §8
item 2 already names the durable version — **`treediff` gains a `TABLE-HUNK` list** — and that is where it belongs, so
the next run is a flag and not an archaeology project.

### 1c · Is the diff pair ever re-run — RECOMMENDATION, explicitly

**Split the answer, because the two pairs answer different questions.**

* **`bodycheck` + `sigcheck`: RE-RUN ON EVERY PATCH, BINDING.** Cost is seconds, they read our own pins, and their
  output is a table a session acts on immediately. Written into `WORKFLOW.md` — §3a.
* **`treediff` + `presetdiff`: ON TRIGGER, NOT ON SCHEDULE — and NOT retired.** Triggers: (a) a patch whose notes claim
  changes to a system we fix; (b) the `DLC_DEEP_CHECK` chain firing; (c) a `BODY-CHANGED`/`DEFECT-GONE` row whose
  replacement a session cannot explain from the two trees by hand. Who: whoever is running that chain. ⛔ Never run
  them "to stay current" — `treediff` emits ~25,000 rows and the vanillahunt chain is what reading them costs.
* ⭐ **What IS binding on every patch is the ARCHIVE**, and it is the cheapest, most irreversible step we own: if
  `ModTools\Src` is not copied **before** the update, that build's tree is gone (`EF-075`: Steam overwrote it in
  place, unasked) and every future comparison across that boundary is impossible. Recovery exists — the Steam 1.0.7
  branch, which is how the loss was reversed — but it is vendor-dependent and may simply not be offered next time.
  ~48 MB per version.

---

## 2 · Question 2 — how far we trust it

### 2.1 The trust table (⭐ **canonical copy now lives in `WORKFLOW.md` → "After a game patch"** — §3b)

| instrument | what its output LICENSES a session to state | what it CANNOT see | trust |
|---|---|---|---|
| `bodycheck.py` | the pinned body's bytes changed / did not change (class b); a stated regex is / is not present in that body (class d); the selector resolves to nothing (class e) | ⛔ **class c — semantics moving under a wrapper whose target body is byte-identical.** 6 of the 10 FIX rows in the 1.1.0 re-verification were class c ⇒ blind to the majority case. Nothing outside the pinned body: a `__parents` change one line above is invisible (§1b). A defect that is an **absence** cannot be a regex. A regex pinned to today's phrasing yields a **false** `DEFECT-GONE` — the direction that retires a live fix | **GREEN IS NOT A CLEARANCE.** `DEFECT-GONE` = REMOVE **candidate**, never a verdict |
| `sigcheck.py` | a named function's arity changed / did not change | everything else. It is an arity bound and stays one (its own header) | bound only |
| `treediff.py` | a named function exists in one tree and not the other; its body/signature differ | **SPAN-SUSPECT**: 441 self-closing declarations, 567 spans reaching EOF, 133 rows flagged; **79 changed hand rows never classified by any agent**. Anonymous `function(` literals (~12,200 lines). **≥1,281 hunks in ≥368 rowed files fall outside every row span** (§0.1) — `NOROWS.tsv` lists a file only when it has *zero* rows, so this class is invisible to the row partition | inventory, not coverage |
| `presetdiff.py` | a preset field's value differs between trees, **in generated files only** | 54 `CommonLua/Data` + `Libs/*/Data` `PlaceObj` files have no field-level reader — widening was recommended and **not done**. **REINDEX-SWAP** is flagged by the tool as the class it cannot distinguish from a real change; 1,707 such rows were never read per row | scoped |
| **all four** | — | ⛔ anything outside `ModTools\Src`; the engine (`Mars.exe` changed builds); runtime-only behaviour; the 1.0.7 `DLC/` subtree (excluded, and its branch DLC state is a Steam artefact, not a 1.0.7 fact) | — |
| **copy-vs-wrapper** | nothing — **it is a PRACTICE, not a tool flag.** No tool emits a three-way diff; a session assembles it from `luafn.find_bodies` across both archives plus our `Code/` | ⛔ never classify by name proxy | manual |

### 2.2 ⭐ The rule — what a session may claim on this tooling alone

> **On these instruments' output alone, a session may state exactly four things:**
> **(1)** a pinned body's bytes did or did not change; **(2)** a named arity did or did not change; **(3)** a stated
> regex is or is not present *in a named body*; **(4)** a named function or preset field exists in one tree and not
> the other.
>
> **Everything else needs a second source.** "Vanilla fixed it", "this fix is still needed", "that change is harmless",
> "nothing moved under us", "this file is behaviourally unchanged" — none of those is in the list. The second source
> is one of: a read of the **replacement body** in both trees, or a run **in the game**.
>
> ⛔ A GREEN is a statement about those four things and nothing else. It is not a clearance, and a clean run over 49
> modules is not evidence that 49 fixes still work.

---

## 3 · Question 3 — where the information lives, and should live

### 3a · Promote the procedure — **RULED YES, WRITTEN**

**Why yes.** `WORKFLOW.md` carries exactly two after-every-patch rules (`:139` fpk verification, `:974` the five-shape
exposure enumeration) and **neither names any of the four tools** — CONFIRMED by reading both. `bodycheck` appears
only as a per-module *authoring* rule (`FIX_POLICY` §2b; `perma/DISPATCH.md` §1); `perma/RELEASE.md` names none of
them; `doccheck.py` gates `bodycheck --selftest` — the **falsifier**, not the check. The one procedural sentence that
existed was a recommendation inside a report and was never promoted.

And the store card, reworded today, now publishes *"Every game patch is read against the pack as well, and the fixes
it changed are updated or retired."* That is a claim about a **recurring process** resting on a track record. A track
record is not a procedure; the next update-day session inherits nothing. Landed as **`WORKFLOW.md` → "After a game
patch — the source-diff instruments"**, immediately after the fpk rule, with the order of operations, what each
verdict obliges, and what a GREEN does not license.

⚠️ **One thing I corrected while there:** the fpk rule's body still said *"Parity is PROVEN for the current build
(1.0.7.396349, extraction diff 2026-07-29)"*. `EF-085` re-proved parity for **1.1.0.403908** on 2026-09-10 — perfect,
0 divergent, 0 absent. The rule was citing a build that is no longer installed. Updated in place (a pointer fix; the
discipline itself is unchanged).

### 3b · The trust table's home — **one home: `WORKFLOW.md`**

`WORKFLOW.md` → "After a game patch", beside the procedure that uses it. Reasoning, since three homes were candidates:

* ⛔ **Not a new fact.** `facts/INDEX.md` is the **engine** facts index (92 entries, and I checked: none covers this).
  The trust table is a statement about *our instruments*, not about the game. Filing methodology as an engine fact
  would be the first of its kind and would make the index mean two things.
* ⛔ **Not `FIX_POLICY` §2b as the canonical copy.** §2b is the *authoring* rule for one tool's manifest; `treediff`
  and `presetdiff` have nothing to do with per-module authoring and would sit there as a category error. §2b keeps
  its own ⚠️ class-c paragraph (it is the warning at the moment of authoring) and gains **one pointer line**.
* ⛔ **Not the tool headers.** They already carry the machine half, accurately, and four copies drift four ways.

⇒ one canonical table, one pointer from `FIX_POLICY` §2b. `perma/DISPATCH.md` §1 already routes to §2b, so an ad-hoc
session reaches it in two hops.

### 3c · Where the artefacts live — documented, but not from the doc map

| artefact | where | documented? |
|---|---|---|
| the two `ModTools\Src` trees + `MANIFEST.sha256` | `C:\Dev\SMR-SrcArchive\1.0.7.396349\` and `\1.1.0.403908\` | ✅ `C:\Dev\SMR-SrcArchive\README.md` — thorough: the standing archive-first rule, the layout, a manifest regenerator, the 2444-changed-file summary, the 1.0.7 recovery route, and the DLC-subtree caveat. ⚠️ It is **outside the repo**, so a session sees it only via `perma/DISPATCH.md` §1 |
| `INVENTORY*.tsv`, `FILES.tsv`, `NOROWS.tsv`, `PRESETS*.tsv`, `CALLERS*.tsv`, the seam reports | `docs/agent/reports/vanillahunt/` | ✅ all **tracked in git** (21 MB, verified with `git ls-files`) — durable, not scratch |
| the tools | `tools/{treediff,presetdiff,bodycheck,sigcheck}.py` | ✅ each has a full header; all four carry `--selftest` |

**Gap:** `docs/README.md` (the doc map, 100 lines) mentions **none** of them — the new section in `WORKFLOW.md` now
names all three rows, which is the one place an update-day session is looking anyway. I did not add a fourth pointer
to `docs/README.md`; one home plus the map already in `WORKFLOW.md` is enough, and scatter is what the brief forbade.

### 3d · The 2 NO-MANIFEST modules — **named, and they are NOT the same case**

`bodycheck --all` names them: **`00_Core.lua`** and **`90_SaveSanitizer.lua`**. Reported, not fixed, per the brief.

* **`00_Core.lua` — legitimate in substance, undeclared in form.** It is the pack's own registry; it replaces no
  shipped body, so there is nothing to hash. But §2b provides `-- SRC: none <reason>` precisely for this, and
  `bodycheck` counts `SRC-NONE` separately from `NO-MANIFEST` *so that an undeclared module stays visible*. One line
  closes it. **Not a violation; an omission.**
* ⚠️ **`90_SaveSanitizer.lua` — a real gap, and the one module whose own header proves it.** Its prose already states
  exactly what a manifest would encode: *"F35 STAYS. 1.1.0 still ships the defect — `WindTurbine.lua:95-105` re-applies
  `WindTurbine_Diffuser` only"*; *"F48 STAYS. The paren is still misplaced upstream"*; *"F03 REMOVED. vanilla now
  cleans this itself — `SavegameFixups.RemoveLeakedUpgradeModifiers` (`Lua/Buildings/Building.lua:1313-1345`)"*.
  That F03 line **is a class-d `DEFECT-GONE`, caught by a human reading prose.** It has pinnable shipped targets and
  no machine-readable line, so the next "vanilla fixed it" for F35 or F48 has to be caught the same expensive way.
  ⛔ Its passes are not inert: F35/F48 are pre-1.1.0-save-only and Steam-unreachable, but the F95 pass cleans residue
  **this pack wrote into 1.1.0 saves on every platform**. Recommendation: `-- DEFECT@` lines per repair. Whoever owns
  the module decides; I did not touch it.

---

## 4 · What I did NOT check

1. **I did not run `treediff` or `presetdiff` for real** — only their `--selftest`. My hunk re-derivation used the
   committed `INVENTORY.tagged.tsv` spans plus difflib, not a fresh `treediff` run. If those spans are themselves
   wrong, my re-derivation inherits it — and it would inherit it *identically* to the audit's, so §0.1's agreement is
   not independent of the spans.
2. **The 157 pinned-file hunks are counted, not read.** I opened seven `__parents` rows against both trees. The other
   ~150 — `GameVar`/`const`/table-field changes inside files we patch — I have not looked at. ⚠️ **This is the list
   most likely to hold a wrong conclusion in this report**: I priced a pass on a sample of eight.
3. **`Lua/Buildings/Residence.lua`'s two `__parents` hunks are UNSETTLED** — the diff showed the whole block shifted
   and I did not resolve which parents actually moved. Residence is a file we patch (F59 territory).
4. **`ReactionObject` and `ContinuousOps` are names, not read components.** I did not open either class, and I did not
   check whether any pack method resolves through them. That *is* the pass I am recommending, not something I did.
5. **I did not verify the 25-entry candidate backlog against the entry bodies** — statuses and priorities come from
   `bugs/INDEX.md` and the audit's §3 table. C80's stale `cand` row is the one I did open.
6. **`logscan.py`** — named in the report recommendation I quote, never run or read here. If the binding step should
   also carry a runtime half, that is the tool, and I did not evaluate it.
7. **`presetdiff`'s 54 unread `PlaceObj` files** — I confirmed the recommendation exists and was not done. I did not
   check how hard widening it would be, so §1c gives that no cost.
8. **The engine.** `Mars.exe` changed builds between 1.0.7 and 1.1.0 and nothing in this report or these instruments
   reads it. Every conclusion here is about Lua source.
9. **I did not re-run the full 1.1.0 re-verification** — `bodycheck`'s 122 OK rows are its verdict, and per §2.2 that
   licenses four statements and not "the pack is fine on 1.1.0".
