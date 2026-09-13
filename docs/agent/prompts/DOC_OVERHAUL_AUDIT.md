# DOC_OVERHAUL_AUDIT — backward QA on the context-economics doc/process overhaul

**Fire with:** a FRESH session rooted at `C:\Dev\SMR-BugFixPack`. Any model, any tool. One session,
docs + tools only, **no shipped Lua**. Written 2026-09-13 by `smr-bugfixpack-da` at the owner's ask.
`git rm` this file when it has fired; its grave is the commit that lands its report.

**The job:** the overhaul below was designed and built across ~30 commits by several sessions, most of
them under time pressure, with the plan itself living in gitignored `.claude/` files. Nobody has ever
looked at the whole of it at once. **Decide whether the loose ends are actually tied** — and say what
should have been in scope and was not.

⛔ **REPORT-ONLY.** Change nothing except this file's README row and your own report. Every finding is
a recommendation with a command behind it. The one thing you may not do is quietly fix something and
report it as fine.

---

## 0 · Your standing, and your licence

**Trust by source** (`CLAUDE.md`): the owner's instruction is authority · tool output carrying its
command and HEAD is a derived fact · **everything else authored is a claim — this prompt included.**
Every claim in §3 was written by the session being audited. Several of its predecessors' claims turned
out wrong in exactly this way, so the base rate here is not low.

⭐ **You are explicitly licensed to say "you missed a thing."** §5 is not a courtesy section. The
overhaul's whole premise — that read cost is the binding constraint here — was adopted from a sister
repo's measurements and never re-argued locally. If the premise is wrong, or if the set of moves it
generated has a hole in it, that finding is worth more than every item in §3. Rank it first.

You may also rule an item **NOT WORTH AUDITING** and say why. A cheap "this can't break" beats a
thorough answer to a question nobody needed.

## 1 · Anchor — run these, quote none of them from here

```
git -C C:/Dev/SMR-BugFixPack status -sb | head -1
git log --oneline -1
python tools/doccheck.py | tail -1
python tools/doccheck.py | grep -E 'WAITING|PUSH SET|STATE \+ STUBS'
git worktree list
```

⚠️ **The tree is busy** — five or more interactive peers work this checkout at once (`ListAgents`), and
they commit under **one git identity**, so `git log --author` attributes nothing. Expect files to change
under you; re-check `git status` immediately before any write, not at the top of your session. The
pre-commit hook can go RED on a peer's in-flight `TEMPORARY` probe; that is not yours to fix and it is
⛔ never a reason for `--no-verify`.

## 2 · What the overhaul was

`git log --oneline 1a487c0..HEAD` is the window; the C92 defect work interleaved in it is a peer's and
out of scope. The plan is `.claude/BLUEPRINT.md` (§8 = the owner's D1–D10 rulings) and the live board is
`.claude/PLAN_TODO.md`. **Both are gitignored claims, not authority.**
⛔ Do **not** read `.claude/CONTEXT_ECONOMICS_REVIEW.md` (53 KB), `IMPLEMENT_PROMPT.md` (spent, wrong four
times, kept only as a record), `REPORTS_CUT_LIST.md` (premise refuted), `SWEEP_RESULTS.md`, or
`OPTIN_INVENTORY.md` whole. Grep them. Opening one "to be thorough" is the reflex this overhaul exists
to cut, and doing it inside its audit would be funny exactly once.

Landmarks, for orientation only — verify each against the tree, not against this table:

| sha | what it claims to have done |
|---|---|
| `1a487c0` | `.rgignore` keeps `docs/archive/` out of a default `rg`; `docs/README.md` says how to search it on purpose |
| `739b7a0` `8f02d68` `2b1fd91` | `docs/WAITING_ON_YOU.md` — the generated owner register, `ck:-` support, `--regen-waiting` |
| `007a078` `635f28a` | `derived_at:` backfilled on every fact; `--emit-fingerprint`; the push set as one number |
| `d797978` | `row_status` eviction across the entry set |
| `ddfbab6` | two skills, mirrored byte-identical to `.agents/skills/` |
| `d56293a` | co-runs out to `perma/CO_RUNS.md` (D5) **as a split**, + the R-A…R-G verification rails |
| `8d059da` | `CLAUDE.md` admission pass (D2 + D3) |
| `35848a1` | checklist markers (D6) |
| `c820c7f` `536a585` | STATE back to a kernel; the 24 KiB release cap reverted to 18 KiB |
| `9726389` | `*/.agents/*` pack-ignored in `metadata.lua` + `tools/pack_predict.py` |
| `efeff52` | `STATE_EVICTION.md` steps 2b + 5 — the register check |
| `0c6fd1f` | `WORKFLOW.md` § "Writing in a shared tree" — three rules homed out of a retiring handoff |

## 3 · The claims to falsify — disagreements first

Work these in order; each names the falsifier, and **a check that cannot fail is not a check.** Ask what
would make each one pass for the wrong reason before you trust it.

1. **The marker system is load-bearing and it is silently lossy.** ⚠️ Two defects were found 09-13 and
   are recorded nowhere but this prompt and `.claude/PLAN_TODO.md`. **Verify both, then look past them
   for the third:** (a) `MARKER_RE` (`tools/doccheck.py:382`) matches `status:([a-z]+)`, so the live
   marker `status:part-ruled` on checklist item 169 does not match *at all* and is dropped with no
   warning — `grep -cE '<!-- ck:' docs/PLAYTEST_CHECKLIST.md` vs doccheck's `marked` count. (b) Nothing
   rejects a duplicate `ck` number, so 169's superseded heading — collapsed inside a `<details>` block —
   wins its register row over the current one; `ck:144` is duplicated the same way. **Then ask the
   question neither defect answers: what else does the register drop without saying so?** Feed it a
   deliberately malformed marker and see whether anything at all complains.
2. **⛔ The marker OBLIGATION is documented nowhere live.** "Changing an item's status ALSO means
   updating its marker" exists only in `prompts/perma/HANDOFF_ORCHESTRATOR.md` — a prompt whose own
   retirement trigger has fired — and in the gitignored handoff. `0c6fd1f` homed three *other* rules out
   of that same file and missed this one. Falsifier:
   `grep -rn "updating its marker" --include=*.md . | grep -v docs/archive`. **Recommend a home.** The
   permitted vocabulary is the same problem: `MARKER_STATUSES` (`doccheck.py:383`) is defined and
   **never referenced**, so the vocabulary is documented in a comment and enforced by nothing.
3. **The register is a pure function of its sources.** doccheck claims `WAITING: fresh` means regen
   reproduces it byte for byte. Test the claim, not the report: perturb a marker, re-run
   `--regen-waiting`, confirm the row moves, revert. Then ask whether `fresh` can be true while the
   register is *wrong* — it can, if the source is wrong, and item 169 is the proof.
4. **The `.rgignore` boundary is discoverable, not just present.** ⛔ A test that names the archive
   tests nothing. The real question is whether an agent who does NOT know about the boundary is told
   before it matters: is the escape hatch (`rg <term> docs/archive/`, `grep -r`, `git grep`) stated
   where a session actually reads, or only in `docs/README.md`? Count the live docs that mention
   `docs/archive/` without mentioning that a default `rg` misses it.
5. **The co-runs move was a SPLIT, and the sign-off tiers survived it.** `WORKFLOW.md`'s
   `## Sign-off tiers` should still carry the owner's 2026-08-04 "standing policy for every leg"
   wording. `.claude/PLAN_TODO.md` claims the move needed no entry edit because `bugs/C44.md:108`'s
   citation still resolves — note that :108 cites WORKFLOW's *"never silently discount a line"* rule,
   which never moved, so that line proves nothing about the co-runs span. **Find the citations that
   DO point at the moved material** and check both directions: anything citing `CO_RUNS.md` for a
   **tier** rule, or `WORKFLOW.md` for a **co-run** rule, is now pointing at the wrong file.
6. **`derived_at:` and `--emit-fingerprint` changed behaviour, rather than decorating the facts.**
   92 facts carry the field. Name a live consumer: which prompt or doc tells a session to run
   `--emit-fingerprint` and *inherit* behind it? If the answer is only `WORKFLOW.md` R-A, is R-A cited
   by anything that a working leg actually reads?
7. **The R-A…R-G rails are in force.** Adoption is not force. `grep -rn "R-[A-G]"` across live docs
   and prompts: if the rails are cited by nothing that fires, they are a section, not a rail set.
   ⚖️ If so, say it plainly — they were owner-adopted, so the remedy is the owner's, not yours.
8. **STATE is a kernel again and its budget measures something real.** `STATE + STUBS` emits the live
   bytes against warn/hard. Two things to separate: is STATE actually status+pointer (apply
   `STATE_EVICTION.md`'s own admission test to every Hazard line), and does the byte count measure
   content or a checkout artefact? `grep -c $'\r'` the push-set files. `.gitattributes:18` pins STATE
   `text eol=lf` because doccheck counts raw bytes; a pin governs checkout, not a session writing the
   file back. Measured 09-13 the CR load was 122 on STATE alone, then 0 hours later — so the artefact
   is intermittent, which is worse than constant. ⚖️ The durable fix (doccheck normalising before it
   counts) gates every commit, so it is an owner call; your job is to price it.
9. **STATE's open-decisions enumeration matches the checklist.** Found 09-13: STATE's `STILL OPEN:` line
   names 47 and 152 c, both of which carry `status:ruled owner:no` markers and headers reading
   *"Nothing is owed from you."* Re-derive the whole enumeration item by item, both directions —
   in STATE but settled in the checklist, **and** owed in the checklist but absent from STATE.
   ⛔ Report; a status is the owner's word and no agent flips one.
10. **The retired things are actually unreachable.** `REPORTS_CUT_LIST.md` (premise refuted) and the
    66-file report-move list (owner ruled option A: **retired, not deferred**) — does any live doc still
    point a future session at either? Same question for `prompts/SELFCHECK_PILOT.md` (unreachable 09-12,
    removal recommended, awaiting the owner under ck133) and `IMPLEMENT_PROMPT.md` ("do not fire again" —
    is that stated **inside** the file, or only in a gitignored board?).
11. **`.agents/` no longer ships, and the pack model is honest.** `python tools/pack_predict.py .`
    should model 52. The two `SKILL.md` files were **never** the v10 "56 delivered vs 54 modelled" gap —
    they were tracked and already inside the 54 — so **that 2-entry gap is still unexplained** and
    `STATE.md` now says so. Closing it needs a re-downloaded `ModContent.fpk`; none is on disk (checked
    both Steam libraries' workshop content and the game's user folder, 09-13). Is there a cheaper route,
    or does the model have a second blind spot? Also: `.agents/` is now pack-ignored but still mirrored
    and equality-checked — confirm both still hold and that nothing else in the repo root ships unasked.
12. **`archive_settled.py` is safe to run.** `.claude/tools/archive_settled.py`, `--apply` never
    exercised end to end; its gates (git-clean, tally-must-balance, atomic temp+replace) are written and
    read, not run. Its ARCHIVE-OLD bucket reports **18** items where `BLUEPRINT.md` D4 ruled **17** —
    unreconciled. Its first build matched header TEXT and marked five owner-pinned bodies MOVE, which
    would have destroyed decision records. ⛔ **Do not run `--apply`.** Audit the code and the
    one-item drift on paper, and say whether the ruling can be executed as ruled.
13. **The push-set budget is the right instrument.** It is over, and it moved 46,633 → 48,031 → 43,062
    in two days. Ask whether a budget on five files is measuring the thing that costs — or whether the
    real cost moved somewhere the budget does not look (skills, `.agents/`, the register, prompt bodies
    a session is told to read).

## 4 · What may not be claimed

- **"Archived" is not closed or retired.** A pointer that resolves is not a pointer that is read.
- **No checklist item changes status by your hand.** A marker records the status an item already
  states; a flip is the owner's act. Same for a hazard's wording and where a rule is filed.
- **No count is hand-typed** — `python tools/doccheck.py --emit-counts`, and every count carries the
  command *and the filter* that produced it.
- **Never state an absence from a truncated grep.** `| head` is not an enumeration; a claim that
  something is *nowhere* needs the presence side counted.
- **A grep count is not a finding** — check where each hit LANDED.
- "Done" needs its diff-stat and its doccheck line. A measurement quoted before its run is not a
  measurement.

## 5 · ⭐ The question the overhaul never asked itself

Answer this one even if §3 comes back clean, and rank it above §3 if it bites:

**What should have been in this overhaul and was not?** The plan was assembled from a sister repo's
measured rails and the owner's D1–D10 rulings, under release pressure, by sessions that each saw one
slice. Candidate shapes, not a menu — find your own:

- a class of document nobody costed (entry bodies? fact bodies? prompt bodies a session is *told* to
  read? the skills, which are over their byte target and load every session?),
- a cost that is not bytes (a read that forces three more reads; a number that must be emitted and so
  costs a tool call every time; a doc whose *shape* makes a session open the wrong thing first),
- a rule adopted for a failure that cannot recur, still being paid for,
- a generated file with no falsifier — the register was built because hand-kept ledgers drift, but a
  generator that is wrong is *worse* than a ledger that is stale, because `fresh` reads as `correct`
  (item 169 is the live proof, and it went unnoticed for a day),
- something the owner has to do by hand every cycle that nobody proposed automating,
- or the premise itself: is read cost really the binding constraint in this repo, or was that
  inherited? ⛔ Do not re-measure the sister repo's numbers — port or reject the rails on this repo's
  own evidence.

## 6 · Stop conditions — report, never push through

A file you are about to write is dirty or named by a running chain · doccheck RED for a reason outside
your lane · a rewrite would change a sentence's meaning · **anything that looks like an owner decision**
· the anchor names a file you were about to rely on. ⚠️ Editing `CLAUDE.md` drifts `AGENTS.md` and turns
doccheck RED — don't, while peers are running.

## 7 · Deliverable

1. **Keep a live todo list from your first minute**, one entry per §3 item plus §5, updated as each
   lands — the owner reads that list to decide whether to step in.
2. `docs/agent/reports/DOC_OVERHAUL_AUDIT.md`: findings **ranked by what they cost if left**, each with
   its verdict (`CONFIRMED` / `REFUTED` / `NOT WORTH AUDITING`), the command that settled it, and a
   one-line recommendation. Items you could not settle go in a **"not opened"** list with the reason —
   that list is where your report is most likely to be wrong, so make it explicit.
3. Anything needing the owner's word goes in `docs/PLAYTEST_CHECKLIST.md` → "Decisions waiting on you",
   **with its marker**, never only in your report.
4. Update this file's row in `prompts/README.md` to FIRED with its grave, then `git rm` this file.
5. Close-out test: *"nothing load-bearing exists only in my conversation."* If false, write it down first.
