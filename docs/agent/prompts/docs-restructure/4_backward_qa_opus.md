# 4 — Backward QA + the end-state handoff report (fresh context; trust nothing forward)

Runs from `docs/agent/prompts/docs-restructure/` (prompt 3 moved the folder).
Staleness check; read the spec + all Notes from upstream. This prompt CLOSES
the chain: the folder must end empty.

## Part A — verify, sampling against git history, not the chain's claims

1. **Conservation**: pick 5 random `agent/bugs/` entries + 5 `agent/facts/`
   entries; diff their bodies against extracts from
   `git show <pre-chain-commit>:docs/BUGS.md` and `:docs/agent/ENGINE_FACTS.md`
   — bodies must be byte-identical (front matter and heading handling per the
   split specs are the only permitted deltas).
2. **Counts**: `doccheck --emit-counts` must equal prompt 1's recorded
   baseline (98 F + 12 D + 41 C rows; 82 Code files; 81 modules; 87 probes) —
   this chain moved text, so ANY count change is a defect, not an update.
3. **Structure**: doccheck v3 green (paste output); root allowlist holds both
   directions; stubs at `docs/BUGS.md`, `docs/STATUS.md`,
   `docs/agent/ENGINE_FACTS.md` resolve; the pre-commit hook fires on a test
   commit; CLAUDE.md is accurate (REMOVE its "layout live after the chain"
   line now).
4. **Spot-usability**: as a fresh session, answer "what is F90's status and
   evidence?" using ONLY CLAUDE.md → STATE.md → bugs/INDEX.md → F90.md.
   Record the hop count and anything that felt missing.

## Part B — ⭐ THE END-STATE HANDOFF REPORT (owner-requested; this is a
## first-class deliverable, not a QA formality)

Write `docs/agent/reports/DOCS_RESTRUCTURE_REPORT.md`. **Its purpose: the
owner will feed it to a fresh top-tier (Fable) session that will REDESIGN the
project's standing prompts and authoring conventions against the new
structure. That session was deliberately NOT given this job here — prompt
redesign is compounding-risk design work, the top-tier slot — so this report
is its entire picture of reality. Write it for that reader.** Contents:

1. **The as-built tree**, complete: every directory and file the chain
   created/moved/stubbed, with one line each on role and format (front-matter
   fields, generated files, banners). Include a real `tree`-style listing.
2. **Deviations from the spec** — every place execution differed from
   `DOC_RESTRUCTURE_SPEC.md` and why (there will be some; a report that
   claims none is suspect).
3. **The read-path economics**: for three representative agent questions
   (a bug's status; an engine fact; "what do I read at session start"), the
   actual hop sequence and rough token cost under the new layout vs the old.
4. **What doccheck enforces as of v3**, exactly, and what it deliberately
   does not.
5. **Friction log**: everything that was awkward, ambiguous, or surprising
   during migration — parser edge cases hit, references that had no good
   home, judgment calls made under rule pressure. This is the raw material
   for the redesign.
6. **The standing-prompts inventory for the redesigner**: current state of
   `agent/prompts/FABLE_NEXT_PROMPT.md` and `DRONE_PROJECT_PROMPT.md` (which
   paths were mechanically fixed by prompt 3, which content now reads stale
   against the new structure), plus WORKFLOW elements 1–7 and the spec §7
   adopted-rules block — with this prompt's own observations on what the
   redesign should reconsider, marked as OBSERVATIONS, not decisions.
7. **Open items** routed onward (anything discovered but out of scope).

## Close-out

Verdict (CLEAR or findings — a findings report is a fully successful
outcome), update STATE.md's pointers, add one line to the checklist's
"Decisions waiting on you": *"feed DOCS_RESTRUCTURE_REPORT.md to a Fable
session to redesign the standing prompts"*. Strike the last README rows,
delete README + this file (folder EMPTY), commit with doccheck output in the
body, push.

Stop: any conservation diff → headline finding, finish the sweep, do NOT
patch content. May not claim CLEAR with any unexplained byte, and may not
skip Part B regardless of Part A's outcome.

## Notes from upstream

**From prompt 3 (Opus, 2026-08-03).** Seven commits, `ef5d314`..`776bde0`, all
pushed. doccheck is at **v3 and GREEN**; the hook runs it on every commit.

### The two commands your Part A conservation sweep should run first

```
python tools/doccheck.py --verify-split 5b374eb          # BUGS, pre-split parent
python tools/doccheck.py --verify-facts-split 2112892    # ENGINE_FACTS, pre-split parent
```

Both re-run the FULL migration accounting from the git blob and compare it to
the files on disk, line by line. ⚠️ **Pass the shas.** `--verify-split`'s
`HEAD~1` default stopped being the pre-split commit seven commits ago;
`--verify-facts-split` deliberately has no default for that reason. This does
not replace your own random-sample diff — it is a second, independent one.

### What prompt 3 built

- **`agent/facts/`** — 43 `EF-001`..`EF-043` + generated `INDEX.md` +
  `_preamble.md`, by `tools/split_facts.py`. 705 fact lines + 8 preamble = 713
  source lines, every line claimed exactly once. Front matter: `id`, `seq`,
  `summary`, `updated`, `verified`, `lines` (JSON scalars, read back by
  `split_bugs.parse_front` — there is ONE front-matter parser in this repo).
- **`agent/STATE.md`** — 60 lines, exactly at the budget doccheck now enforces.
  The counts block is pasted from `--emit-counts`.
- **The moves**, all `git mv`. `docs/` root is now exactly the allowlist.
- **README + CLAUDE.md**, the sweep, the WORKFLOW block, FIX_POLICY's
  foreign-object rule, doccheck v3.

### Deviations from the spec/brief — your §2 asks for these, here they are

1. **PLAYTEST_ARCHIVE.md → `archive/` was NOT in this prompt's Moves list.**
   Spec §1 puts it there and the root allowlist leaves no room for it, so it
   moved. Its inbound checklist link was repointed in the sweep.
2. **The WHOLE of STATUS.md went into SESSION_LOG**, not "everything STATE.md
   does not re-state". Deciding which sentences a summary had "consumed" is a
   judgment call inside a conservation job; a verbatim whole-file block makes
   conservation provable. Expect duplication between STATE.md and the archive —
   it is deliberate and the banner says so.
3. **`updated:` on facts is git-blame MAX over the fact's line range**, not the
   brief's "blame of the fact's first line". Same semantics as the bugs schema
   (spec §2, "last substantive edit"). 6 of 43 differ between the two readings.
4. **`verified:` is a mechanical EXTRACTION** — an observation word within 24
   chars of an ISO date, first match over the joined fact text. 21 of 43. It is
   not an adjudication and INDEX.md says so. ⚠️ Several facts carry their own
   ⚖️ "what is MEASURED and what is NOT" paragraphs that are strictly more
   authoritative than this field; do not let the field launder them.
5. **CLAUDE.md's "layout live after the chain" line is ALREADY GONE** (job 4).
   Your Part A step 3 asks you to remove it; there is nothing to remove.
   CLAUDE.md is 25 lines against spec §6's ≤25.
6. **Four instruction sites that told authors to hand-edit the now-generated
   index were rewritten** (WORKFLOW ×2, FABLE_NEXT_PROMPT, PLAYTEST_CHECKLIST).
   Strictly this is content, not a path reference — but leaving them would have
   been a live defect this chain introduced.

### Friction log material (your Part B §5) — the four worth recording

- ⛔ **A mechanical path sweep destroys the translation note.** The note is a
  sentence made entirely of the OLD paths; the first sweep run rewrote it into
  `docs/agent/bugs/` → `docs/agent/bugs/<ID>.md`. Caught, reverted from HEAD,
  and CLAUDE.md + README dropped from the target list. **Generalisable: exclude
  the documents that quote old paths on purpose.**
- **Bare-name references are the long tail.** `BUGS.md` came in five shapes
  (`docs/BUGS.md`, backticked, bare, `BUGS F35` with no extension, and
  `docs\agent\ENGINE_FACTS.md` with backslashes). Two passes plus two hand
  fixes. A third pass found nothing, which is the only reason this is closed.
- **Article agreement**: "a `BUGS.md` entry" → "a agent/bugs/ entry" ×3. Any
  future rename script should check the word before its match.
- **The allowlist source question.** v3 PARSES the root list out of README's
  fenced map rather than hard-coding it, so the folder and the map are the only
  two things that can disagree. Consequence worth knowing: **deleting a row from
  README does not widen the allowlist, it makes that file undeclared.**

### What doccheck v3 enforces (your Part B §4), and what it does not

Enforces: entry + fact front matter; `status:` vs heading tag (RED); both
INDEX.md files regenerate byte-identically; the root allowlist both directions
against README's map; STATE.md ≤60 lines; the three stubs exist, say MOVED, and
point; no `TEMPORARY` in shipped or TestKit Lua; and it prints the counts block,
which a red run refuses to hand out. All ten new checks were negative-controlled
(mutate → RED → restore → GREEN); so were the splitter's six.

Does NOT enforce: anything about `docs/archive/` or `agent/reports/` contents;
link validity (a `[text](path)` pointing nowhere is invisible to it); prose
staleness; the `copies:` field; that `verified:` is true. The 10 `warn` lines on
C-row dispositions are by design, documented in `c_status()`, and are not drift.

### Open items routed to you (Part B §7)

- `PT_REDESIGN_PROMPT.md` was NOT swept — §3f names "the two standing prompts"
  and it is a one-off. Check whether it is still live; if it is, its paths are
  stale.
- Bare prose mentions of `MOD_DESCRIPTION.md` were not path-qualified (it is
  not in §3f's replacement list); its move is recorded in README's translation
  section. Same for bare report filenames, which still resolve inside
  `agent/reports/`.
- `SESSION_LOG.md`'s own preamble still cites `docs/STATUS.md`,
  `docs/BUGS.md` and `docs/agent/ENGINE_FACTS.md`. **Correct — `archive/` is
  never edited and the translation note covers it.** Do not "fix" it.
- `docs/PLAYTEST_CHECKLIST.md:6` links `#reporting-protocol`; no such heading
  exists in that file. Pre-existing, not caused here — worth one line in your
  report.
- The facts split assigned ids by source order, so `EF-###` numbers carry no
  meaning beyond "where it was in the old file". If the redesign wants topical
  ids, now (before anything cites them) is the cheap moment to say so.
