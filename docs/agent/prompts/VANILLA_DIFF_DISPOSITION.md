# The vanilla diff — what we do with it, how far we trust it, and where it lives

**Filed by:** orchestrator, 2026-09-12, owner-asked. **For:** tool-neutral — a Claude session or
Astra. The reading is broad but the deliverable is a judgment, not a census; whoever takes it must be
willing to write "we do not know" and to recommend RETIRING an instrument if that is the honest answer.
**Lifecycle:** root one-off — `git rm` in the landing commit and add a grave row to
`docs/agent/prompts/README.md` ("Root — live one-offs").

⛔ **Keep a live todo list, one item per question below, updated as each resolves.** The owner reads it.

---

## The question

We own four instruments that read the game's shipped Lua. They work, they are falsified, and after
2026-09-10 not one of them has a scheduled next use. The owner asks:

1. **What do we DO with the vanilla diff information** we already have?
2. **How much do we TRUST it?**
3. **Where does information about it need to live** — and where should it live going forward?

This is a disposition decision, not an investigation. Every fact below is already in the record; your
job is to decide what it means and write the answer down where it will be found.

## What we have (verified 2026-09-12 — re-verify, these are claims)

**Two pairs, two different subjects.** They are commonly conflated, including by the session that
wrote this brief:

| pair | asks | origin | output |
|---|---|---|---|
| `tools/treediff.py` + `tools/presetdiff.py` | *what did the GAME change between 1.0.7 and 1.1.0?* | written inside vanillahunt as its instruments | `INVENTORY.tsv`, `FILES.tsv`, `NOROWS.tsv`, `PRESETS.tsv`; the C-candidates |
| `tools/bodycheck.py` + `tools/sigcheck.py` | *what moved under the code WE patch?* | hotfix 2 / `reports/PACK_1_1_0_REVERIFICATION.md` | per-module class verdicts; arity mismatches |

Layered, not redundant: `Require` sees **existence**, `sigcheck` **arity**, `bodycheck` **the body and
the defect expression**, `treediff` **the game's whole change set with no reference to our pack**.

Both archives are on disk with `MANIFEST.sha256`: `C:\Dev\SMR-SrcArchive\1.0.7.396349` and
`\1.1.0.403908`. A 2026-09-12 read-only run had `bodycheck` at exit 0 (130 manifest rows over 48
stamped modules: 122 OK, **2 NO-MANIFEST**, 1 NO-DEFECT, 7 SRC-NONE) and all three selftests PASS.

## Question 1 — what do we do with it

**(1a) The candidate backlog.** C56–C73, C75–C76, C78–C81 were chain-filed by the diff; C82 came from
the terminal audit. Every one is source-read with **no field report, no save, no log** behind it — which
is why checklist items 137/138/140/141 all reduce to "provision a fixture or leave it source-only", and
why the owner's standing read is that provisioning colonies to chase source-only readings is a poor use
of their play time. **Is that the right disposition for all of them, or does some subset deserve better?**
Give a recommendation per group, not per entry, and say what would change your mind.

**(1b) The 1,281 unread hunks.** `HUNT_AUDIT.md` §1.4: of 699 changed hand files with ≥1 row, **368
carry 1,281 hunks (4,542 non-blank lines) that fall outside every row span on both sides** — 916
table/field lines, 71 `__parents`, 47 `GameVar`/`MapVar`/`const`, 12 `DefineClass` openers. `NOROWS.tsv`
lists a file only when it has *zero* rows, so this class is invisible to the row partition, and its only
read was a file-level skim. **This is the largest known unexamined surface in the project.** Decide: is
it worth a reading pass, a targeted pass on the high-risk subclasses only, or nothing? Price each.

**(1c) Whether the diff pair is ever re-run.** Nothing says run `treediff` on the next patch; nothing
says it is retired. Recommend one, explicitly. If "re-run", say on what trigger and who does it.

## Question 2 — how far do we trust it

Enumerate the stated limits and **assign each a trust level a future session can act on** — not prose,
a table with a verdict per instrument. The record already carries these; verify and add any you find:

- **`bodycheck` GREEN IS NOT A CLEARANCE** (`FIX_POLICY` §2b). It cannot see **class c** — semantics
  moving under a wrapper whose target body is byte-identical. ⚠️ **6 of the 10 FIX rows in the 1.1.0
  re-verification were class c**, so the instrument is blind to the majority case. A `DEFECT-GONE` is a
  REMOVE **candidate, never a verdict**. A defect that is an ABSENCE cannot be expressed as a regex, and
  a regex pinned to today's phrasing yields a **false** `DEFECT-GONE` — the direction that retires a
  live fix.
- **`sigcheck` is an arity bound and stays one** (its own header).
- **`treediff` SPAN-SUSPECT:** 441 self-closing declarations, 567 spans reaching EOF, and **79 changed
  hand rows never classified by any agent**.
- **`presetdiff` scope is generated files only** — the 54 `CommonLua/Data` + `Libs/*/Data` `PlaceObj`
  files had no field-level reader. "Yes for the next chain" was recommended and **not done**.
- **`REINDEX-SWAP`** is flagged by the tool itself as the class it **cannot** distinguish from a real change.
- **Blind spots inherited by every link:** anything outside `ModTools\Src`, the engine itself
  (`Mars.exe` changed builds), runtime-only behaviour, and the 1.0.7 `DLC/` subtree (excluded).
- **Copy-vs-wrapper is a PRACTICE, not a tool flag** — no tool emits a three-way diff; a session
  assembles it from `luafn.find_bodies` across both archives plus our `Code/`. ⛔ Never classify by name
  proxy.

⭐ **Then answer the question that matters:** given these limits, **what claim may a session legitimately
make on this tooling's output alone**, and what needs a second source? Write that as a rule, not an essay.

## Question 3 — where the information lives, and should live

**The live gap, and it now has a public consequence.** `WORKFLOW.md` carries exactly two after-every-
patch rules — `:139` fpk verification (re-extract `Packs\Lua.fpk`, diff against the new Src, re-verify
replacement targets byte-for-byte) and `:974` the five-shape exposure enumeration. **Neither names any of
the four tools.** `bodycheck` appears only as a per-module authoring rule (`FIX_POLICY` §2b;
`perma/DISPATCH.md` §1), and `doccheck.py` gates only `bodycheck --selftest` — the falsifier, not the
check. `perma/RELEASE.md` names none of them. The one procedural sentence that exists is a
**recommendation inside a report** and was never promoted: `PACK_1_1_0_REVERIFICATION.md` §4 rec 5 —
*"The update-day checklist becomes: run three tools, read one table, write the REMOVE/FIX prompts from it."*

⚠️ **Why this is now urgent.** The store card, reworded 2026-09-12 (`2e919b5`, checklist 112/133),
publishes: *"Every game patch is read against the pack as well, and the fixes it changed are updated or
retired."* That is a claim about a **recurring process**. It is true of hotfix 1, hotfix 2 and v9 — but
it currently rests on a **track record plus the fpk rule**, and the instruments that actually perform it
are in no procedure. We spent 2026-09-12 correcting a different published sentence for exactly this
shape of over-claim. **Do not let the fix for that one create another.**

Decide and implement:
- **(3a)** Should the "run three tools, read one table" recommendation be **promoted into `WORKFLOW.md`
  as a binding after-every-patch step**? If yes, write it — including which tools, in what order, what
  each verdict obliges, and ⛔ what a GREEN does NOT license. If no, say what makes the published card
  sentence true instead.
- **(3b)** Where should the **trust table** from question 2 live so a session hits it before relying on a
  verdict? Candidates: `FIX_POLICY` §2b (already carries part of it), a fact under `docs/agent/facts/`
  (check `facts/INDEX.md` first — one may already exist), or the tool headers. Pick one home and make the
  others point at it. ⛔ Do not scatter the same content into three places.
- **(3c)** Where do the **artefacts** live — the TSVs, the archives, the manifests — and is that
  documented anywhere a new session would find it? Note `docs/README.md` is the doc map.
- **(3d)** The **2 NO-MANIFEST modules** `bodycheck` reports: FIX_POLICY §2b says every module carries
  `SRC:` + `DEFECT:` headers or it does not ship. Name them and say whether that is a real violation or a
  legitimate exemption. Do not fix them here — report.

## Constraints

⛔ Read-mostly. The only writes authorised: the disposition record itself, the `WORKFLOW.md` procedure if
you rule (3a) yes, the trust-table home from (3b), pointer updates, and this brief's own removal.
**Do not fix any module, do not re-run a hunt, do not file new candidates** — if you find a defect while
reading, file it as `cand` and move on.
⛔ `git status` before and during; sibling sessions edit this tree. Commit with an explicit pathspec.
No `doccheck.py --regen`. `python tools/doccheck.py` GREEN before committing.
⛔ Recorded facts are claims: re-derive the route, not just the citation. Several numbers in this brief
were read on 2026-09-12 by one session — check them.
⛔ Where the record does not settle a question, say so. Do not fill a gap with a plausible story.

## Deliverable

One report at `docs/agent/reports/VANILLA_DIFF_DISPOSITION.md`, committed verbatim, answering the three
questions in order, plus whatever you landed under (3a)/(3b). End with an explicit
**"what I did not check"** list — an unchecked-artefacts list is where the next reader looks for the
wrong conclusion, so write it even if it is short. Then put the owner-facing decisions on
`docs/PLAYTEST_CHECKLIST.md` as a numbered item — recommendation first, cost stated, one line each.
