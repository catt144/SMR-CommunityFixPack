# Docs Restructure — end-state report (chain prompt 4, Opus, 2026-08-03)

**Verdict: CLEAR on conservation, with three findings — one fixed here, two
routed.** No byte of BUGS.md, ENGINE_FACTS.md or STATUS.md was lost, altered or
silently reinterpreted. The findings are all in the *reference sweep*, not in
the content migration.

**Who this is for.** The owner will feed this to a fresh top-tier (Fable)
session that will REDESIGN the standing prompts and authoring conventions
against this tree. That session gets no other picture of reality, so this
report states the layout, the deviations, the economics, the enforcement
boundary and the friction — and marks its own opinions **OBSERVATION**, never
decision. Authority order is unchanged: `DOC_RESTRUCTURE_SPEC.md` > the
DOC_STRUCTURE_REVIEW addenda > this report. **This report is not authority over
`agent/bugs/` or `agent/facts/`.**

Chain: prompts 1–4, commits `eb923ab`..(this one). doccheck is at **v3, GREEN**,
armed as a pre-commit hook.

---

## 1 · The as-built tree

Everything below is **tracked** — this is what a fresh clone gets. One
exception is called out in §7.

```
CLAUDE.md                          25 lines. Auto-loaded every session. Project one-liner,
                                   mandatory-read pointer, folder contract, the §4 path-translation
                                   note, doccheck + hook setup, owner-decision rule, 3 pointers.
tools/
  doccheck.py                      588 lines. THE structure checker (§4 below). --emit-counts prints
                                   the build-state block; a red run refuses to print it.
  split_bugs.py                    856 lines. The BUGS migration + the repo's ONE front-matter parser
                                   (parse_front) — facts read back through it too.
  split_facts.py                   516 lines. The ENGINE_FACTS migration.
  hooks/pre-commit                 Runs doccheck --emit-counts; blocks on red. Enable per clone with
                                   `git config core.hooksPath tools/hooks` (a git setting, not a file).
docs/
  PLAYTEST_CHECKLIST.md            HUMAN. Owner's heaviest doc. Carries "Decisions waiting on you"
                                   (prompt 1) — the R10 mirror target.
  PLAYTEST_HELP.md                 HUMAN. Console facts, command table, fixtures, ground rules.
  FUTURE_IDEAS.md                  HUMAN. Parking lot. Nothing in it is work.
  README.md                        The map. ⚠️ ALSO THE ALLOWLIST SOURCE — doccheck parses the root
                                   list out of its fenced block (§5).
  BUGS.md                          3-line stub → agent/bugs/. MOVED banner + date.
  STATUS.md                        3-line stub → agent/STATE.md. MOVED banner + date.
  agent/
    STATE.md                       60 lines, at the enforced budget. THE mandatory read. Current-only.
                                   Counts block pasted from --emit-counts, never hand-typed.
    WORKFLOW.md                    Authoring/process. Gained the §7 adopted-rules block (7 rules).
    FIX_POLICY.md                  Code rules. Gained the wrapper foreign-object inertness rule.
    ENGINE_FACTS.md                3-line stub → agent/facts/. MOVED banner + date.
    bugs/                          118 files = 116 entries + INDEX.md + _notes.md
      <ID>.md                      114 plain (F*/D*/C*) + 2 grouped (C03-C11.md, C12-C38.md).
                                   Front matter: id, seq, row, title, status, status_source,
                                   priority, evidence, row_status, updated, copies (JSON scalars).
                                   Body = byte-preserved BUGS.md slice, heading line included.
      INDEX.md                     GENERATED (line-1 banner). All 151 rows. Regenerated + diffed
                                   by doccheck; any difference is red.
      _notes.md                    Residue owned by no entry: old intro, legend, the five `##`
                                   section dividers, the "Not yet swept" backlog, and C02's row.
    facts/                         45 files = 43 facts + INDEX.md + _preamble.md
      EF-001..EF-043.md            One per top-level bullet of old ENGINE_FACTS.md, SOURCE ORDER.
                                   Front matter: id, seq, summary, updated, verified, lines.
      INDEX.md                     GENERATED (line-1 banner). 43 rows.
      _preamble.md                 The 8 lines that opened the old file.
    reports/                       17 files. Reports, plans, specs, audits, surveys. IMMUTABLE —
                                   never swept, old paths read through the translation note.
    prompts/                       DRONE_PROJECT_PROMPT.md, FABLE_NEXT_PROMPT.md (standing),
                                   PT_REDESIGN_PROMPT.md (live one-off — see §7).
  archive/                         17 files. Append-only, NEVER edited. SESSION_LOG.md,
                                   PLAYTEST_ARCHIVE.md, MOD_DESCRIPTION.md (frozen, banner per §3d),
                                   retired prompts, fingerprints.
```

**Formats worth knowing before you redesign anything.**

- **Two INDEX.md files are generated and byte-diffed.** Hand-editing one is a
  red build. Edit the entry or fact file.
- **`row_status:` is the frozen old index-row cell, verbatim.** On heavy
  entries it is a multi-hundred-word paragraph *inside* the front matter. It is
  the reason nothing was lost; it is also why front matter is no longer
  skimmable. See the OBSERVATION in §6.
- **`status:` and the heading tag both live inside the entry file**, and
  doccheck goes RED if they disagree. The old row↔tag drift class is dead
  because the row is no longer a hand-written artifact.
- **`seq` is old-file position, not meaning.** Same for `EF-###` — see §7.

---

## 2 · Deviations from the spec

Prompt 3 recorded five (verified accurate); this prompt adds two.

1. **`PLAYTEST_ARCHIVE.md` → `archive/` was not in prompt 3's Moves list.** Spec
   §1 puts it there and the root allowlist leaves no room for it, so it moved.
   Its inbound checklist link was repointed.
2. **The WHOLE of STATUS.md went to SESSION_LOG**, not "everything STATE.md does
   not restate". Deciding which sentences a summary had *consumed* is a
   judgment call inside a conservation job; a verbatim whole-file block makes
   conservation provable. **Expect deliberate duplication between STATE.md and
   the archive** — the banner says so.
3. **`updated:` on facts is git-blame MAX over the fact's line range**, not the
   brief's "blame of the first line" — same semantics as the bugs schema (spec
   §2, "last substantive edit"). 6 of 43 differ between the two readings.
4. **`verified:` on facts is a mechanical EXTRACTION**, not an adjudication: an
   observation word within 24 chars of an ISO date, first match over the joined
   fact text. 21 of 43 carry one. ⚠️ **Several facts carry their own ⚖️ "what is
   MEASURED and what is NOT" paragraphs that are strictly more authoritative
   than this field. Do not let the field launder them.** INDEX.md says so.
5. **Spec §3b said "original file becomes a stub"; §1's allowlist has no room
   for `ENGINE_FACTS.md` at `docs/` root** — it was already under `docs/agent/`,
   where the stub now sits. Not a conflict, but the spec's two sections read
   differently and prompt 3 chose correctly.
6. **This prompt's own brief was wrong about CLAUDE.md.** Part A step 3 ordered
   the removal of a "layout live after the chain" line. `git log -S` over
   CLAUDE.md's whole history shows **that line never existed**. Nothing was
   removed. Prompt 3 flagged this in advance and was right.
7. **This prompt made one content edit, which its own "do NOT patch" rule
   arguably fences.** See finding F1 in §5 — 9 dangling directory references in
   a living standing prompt. The rule fences *conservation* diffs; these were
   references this chain broke by moving the directories. Fixed, scripted,
   9 tokens, line count unchanged. The judgment call is disclosed, not hidden.

---

## 3 · Read-path economics

Bytes are measured; token figures are bytes/4 and are indicative. "OLD" is the
pre-chain repo at `5b374eb`/`2112892`.

| | OLD | NEW | |
|---|---|---|---|
| `BUGS.md` | 12,726 lines / 960,446 B | — | split to 116 files |
| `ENGINE_FACTS.md` | 713 lines / 50,926 B | — | split to 43 files |
| `STATUS.md` | 1,581 lines / 119,837 B | — | 60-line STATE.md + verbatim archive |

**Q1 — "what do I read at session start?"**
OLD: WORKFLOW's reading path put `ENGINE_FACTS.md` (50,926 B) first, then
`STATUS.md` (119,837 B) = **170,763 B ≈ 43k tokens before touching a defect.**
NEW: `CLAUDE.md` (1,530 B, auto-loaded) → `agent/STATE.md` (3,121 B) =
**4,651 B ≈ 1.2k tokens.** ≈ **37× cheaper**, and STATE.md is current-only, so
the tokens are also *live* rather than 1,581 lines of history.

**Q2 — "what is F90's status and evidence?"** (the Part A4 probe, run as a
fresh session using only the sanctioned path)
Hops: `CLAUDE.md` → `agent/STATE.md` → `agent/bugs/INDEX.md` → `agent/bugs/F90.md`.
**Answered at hop 3** — the INDEX row carries `fixed` / `P2` /
`SOURCE-VERIFIED` — for **25,545 B ≈ 6.4k tokens**. Hop 4 (the 355-line entry,
25,254 B) is only needed for the evidence *narrative*: **50,799 B ≈ 12.7k**.
OLD: the same answer sat in an index table at lines 1–176 of a 960,446 B file.
Grep was cheap then and is cheap now; the difference is that **the cheap path is
now the default path** instead of a trick you had to already know.

**Q3 — "what does the engine actually do here?"** (e.g. EF-014, fpk parity)
OLD: 50,926 B ≈ 12.7k tokens, and `FABLE_NEXT_PROMPT` said *read the whole file*.
NEW: `agent/facts/INDEX.md` (7,293 B) + one fact (EF-014, 1,699 B) =
**8,992 B ≈ 2.2k tokens**. ≈ **5.7× cheaper** — **but only if the reader stops
reading the whole thing. The standing prompt currently still tells them not
to.** See §6, item 1. This is the single highest-value thing the redesign can
fix.

**What the probe felt like, honestly.** The one friction point: `STATE.md`
points at `agent/bugs/` — a *folder*. A fresh session lands on a 118-file
directory listing and has to infer that `INDEX.md` is the entry point.
`CLAUDE.md` does name INDEX.md, so it is recoverable at hop 1, but the
mandatory read itself does not. One word would fix it. Second, "evidence" is
ambiguous: the INDEX column is a *confidence label* (`SOURCE-VERIFIED`), while
a reader asking for "the evidence" usually wants the call chain in the body.

---

## 4 · What doccheck v3 enforces — and deliberately does not

**Enforces** (all ten new checks negative-controlled: mutate → RED → restore →
GREEN; so were the splitter's six):

- entry front matter and fact front matter, schema and types;
- **`status:` vs the heading tag** inside each entry — RED on disagreement;
- **both INDEX.md files regenerate byte-identically** from front matter;
- **the `docs/` root allowlist in BOTH directions**, parsed out of README's map;
- **STATE.md ≤ 60 lines**;
- the three stubs exist, say MOVED, and point;
- no `TEMPORARY` in shipped or TestKit Lua;
- and it **prints the counts block, which a red run refuses to hand out**.

Re-verified live by this prompt, both directions:

```
undeclared file at docs/ root  → ROOT: RED  1 undeclared, 0 declared-but-absent  → commit BLOCKED, HEAD unchanged
row added to README's map only → ROOT: RED  0 undeclared, 1 declared-but-absent
restored                       → ROOT: ... exactly the 8 entries ... → doccheck: GREEN
```

**Does NOT enforce** — know these before you rely on it:

- **anything about `docs/archive/` or `agent/reports/` contents** (both are
  immutable by rule, not by check);
- **link validity — a `[text](path)` or a backticked path pointing nowhere is
  invisible to it.** This is how finding F1 (§5) survived three sweep passes;
- **prose staleness** — a sentence can be fluent, well-formed and false;
- the `copies:` field (fill-forward, never backfilled);
- **that `verified:` is true** — it is an extraction, see §2.4;
- the 10 `warn` lines on C-row dispositions are **by design**, documented in
  `c_status()`, and are not drift.

---

## 5 · Friction log — the raw material

Prompt 3's four, verified and kept:

- ⛔ **A mechanical path sweep destroys the translation note.** The note is a
  sentence made entirely of the OLD paths; the first run rewrote
  `docs/agent/bugs/` → `docs/agent/bugs/<ID>.md` inside it. Caught, reverted,
  CLAUDE.md + README dropped from the target list. **Generalisable: exclude the
  documents that quote old paths on purpose.**
- **Bare-name references are the long tail.** `BUGS.md` came in five shapes:
  `docs/BUGS.md`, backticked, bare, `BUGS F35` with no extension, and
  backslashed. Two passes plus two hand fixes; a third pass found nothing.
- **Article agreement**: "a `BUGS.md` entry" → "a agent/bugs/ entry" ×3. Any
  future rename script should check the word before its match.
- **The allowlist source question.** v3 PARSES the root list out of README's
  fenced map rather than hard-coding it, so the folder and the map are the only
  two things that can disagree. ⚠️ Consequence: **deleting a row from README
  does not widen the allowlist, it makes that file undeclared.**

This prompt's additions:

- ⛔ **F1 — FIXED HERE. The sweep missed backslash-form directory paths, and a
  third clean pass certified it anyway.** `DRONE_PROJECT_PROMPT.md` — a LIVING
  standing prompt, explicitly inside spec §3f's scope — still carried **9
  dangling references**: 3 × `docs\prompts\` and 6 × `docs\reports\`, both
  directories that no longer exist. Prompt 3's friction note says backslashes
  *were* handled, and they were — **for `ENGINE_FACTS.md` only**; the finding
  generalised to one filename, not to the shape. Fixed by scripted token
  replacement (`docs\prompts\` → `docs\agent\prompts\`, `docs\reports\` →
  `docs\agent\reports\`), 9 replacements, line count 338 → 338, no other word
  touched. **Root cause worth carrying: the sweep's own verification used the
  same forward-slash vocabulary as the sweep, so a clean pass proved only that
  the sweep was self-consistent.**
- **A grep for the paths you replaced cannot find the paths you forgot.** F1 was
  found by a *different* instrument: resolving every backticked
  `` `docs/...` ``/`` `docs\...` `` token in the living docs against the actual
  filesystem. That sweep now reads **3 dangling**, all disclosed in §7 — down
  from 12. A markdown-link sweep over the 16 living docs (which also resolves
  all 151 INDEX rows to their entry files) reads **1 broken**, pre-existing.
- **Mechanical replacement silently converts true sentences into false ones
  when a FILE becomes a FOLDER.** Not dangling, so no instrument catches it:
  - `FABLE_NEXT_PROMPT.md:163` — "`docs/agent/facts/` — whole file". A folder
    has no whole file, and the instruction now means "read all 43", which
    spends the exact tokens the split was meant to save.
  - `DRONE_PROJECT_PROMPT.md:10-11` — "`docs/` root = daily truth (`STATUS`,
    `agent/bugs/`, … `MOD_DESCRIPTION`)". All three are now false: STATUS is a
    stub, `agent/bugs/` is not at root, MOD_DESCRIPTION is frozen in `archive/`.
  - ~8 sites read `agent/bugs/ F97` (was `BUGS.md F97`) where the path is
    `agent/bugs/F97.md` — checklist ×3, FUTURE_IDEAS, FIX_POLICY ×3, DRONE ×1.
  **Deliberately NOT fixed here**: these are content, they still tell a reader
  where to look, and rewriting them is the redesign's job. F1 was fixed because
  a reader *following* it finds nothing.
- **Grouped entries have no per-ID anchors, and the filenames say so.**
  `C03-C11.md` and `C12-C38.md` each own one row and adopt the rest into front
  matter (8 + 26 = 34 adopted). INDEX.md states that per-ID anchors inside them
  do not exist and are not invented.
- **C02 is an index row whose entry text never existed** — verified against the
  pre-split blob. It is recorded as an orphan in `_notes.md` and INDEX.md
  rather than fabricated. 116 own a file + 34 adopted + 1 orphan = 151.
- **`git ls-files` and `ls` disagree about `prompts/project/`** — see §7.

---

## 6 · Standing-prompts inventory, for the redesigner

**`FABLE_NEXT_PROMPT.md`** (10,711 B). Paths mechanically fixed by prompt 3 and
verified correct here: `agent/STATE.md`, `agent/bugs/`, `agent/facts/`,
`agent/reports/…`, `agent/prompts/…`. Zero dangling. Content now stale:

1. ⭐ **Reading-list item 1 says "`docs/agent/facts/` — whole file".** The
   single most expensive stale sentence in the repo — see §3 Q3.
2. Item 3 says "`docs/agent/bugs/` — the entries the sitting touches", with no
   mention of `INDEX.md` as the way to find them.
3. Line 8 says the project chain is complete and `docs/agent/prompts/project/`
   is empty — true, but that directory does not exist in git (§7).
4. Its close-out step says "update `agent/STATE.md`" — correct, and STATE.md is
   now line-budgeted at 60. **A prompt that tells a session to add to a
   hard-capped file should say what to evict.** Nothing says that today.

**`DRONE_PROJECT_PROMPT.md`** (19,281 B). Nine dangling paths fixed here (F1).
Content now stale: the whole `DOCS LAYOUT (reorganised 2026-08-01)` block at
lines 8–14 describes the pre-chain tree in prose. Its remaining dangling
reference is the shared `prompts/project/README.md` (§7).

**`PT_REDESIGN_PROMPT.md`** (4,197 B) — **a live one-off, and this commit
unblocks it.** Its gate is *"`docs-restructure/` must be EMPTY before this
runs"*, because both efforts edit `PLAYTEST_CHECKLIST.md`. That folder is empty
as of this commit. Prompt 3 warned its paths were stale; **verified, and they
are not** — it already cites `agent/bugs/<ID>.md` and
`docs/archive/PLAYTEST_ARCHIVE.md`. Its one old-path mention self-qualifies
with the post-move location. It self-deletes on completion.

**WORKFLOW elements 1–7** (the required-elements block for any brief) — live
and unchanged by this chain: 1 live progress list (with the granularity rule),
2 `git log`+`git pull` staleness anchor, 3 scope fence, 4 stop conditions,
5 what may NOT be claimed, 6 whether the brief self-deletes, 7 the stale-probe
gate. **The spec §7 adopted-rules block** is now binding in WORKFLOW:
R2 execution markers, R3 provenance words (route tagged separately from
citations; blanket table claims banned), R5 TAKEABLE-WHEN, R8 archive
load-bearing logs, R10 owner-decision mirroring — plus two mechanical rules
(INDEX is generated; run doccheck before committing).

### OBSERVATIONS — not decisions, and not verified as good ideas

- **O1. Nothing in elements 1–7 requires a brief to state its READ PATH, and
  the restructure just made read paths cheap and specific.** Every stale item
  above is a reading instruction. An element 8 — "name the files this brief
  requires, at file granularity, and the index to find more" — would have made
  §6.1 impossible to write.
- **O2. `row_status:` in front matter is doing two jobs.** It is the
  conservation receipt for the old index cell *and* the field a reader's eye
  hits first. Consider whether the receipt belongs somewhere a skimmer does not
  pay for. **⚠️ It is load-bearing for conservation — do not delete it without
  moving it.**
- **O3. The mandatory read points at folders, not at their indexes** (§3).
- **O4. Nothing tells an author which of `status:` / heading tag to edit
  first.** doccheck catches disagreement but the ordering is folklore.
- **O5. A link/path resolver would have caught F1 in prompt 3.** doccheck
  deliberately omits link validity (§4); F1 is the first evidence of what that
  costs. The two throwaway sweeps this prompt used are the shape of it. This is
  an OBSERVATION because the omission was deliberate and the cost of the check
  (false positives on prose, on `<ID>` placeholders, on the archive's
  intentionally-stale paths) is real and unmeasured.
- **O6. `EF-###` ids carry no meaning beyond old-file position.** Nothing cites
  them yet. If topical ids are ever wanted, **now is the cheap moment** — the
  cost rises with the first citation.
- **O7. STATE.md's 60-line cap is enforced but has no eviction rule** (§6.4).

---

## 7 · Open items routed onward

1. ⚠️ **`docs/agent/prompts/project/` exists on disk but not in git** — it is
   empty, and git does not track empty directories. A fresh clone does not have
   it. Two live docs point at a `README.md` inside it that does not exist:
   `FIX_POLICY.md:317` and `DRONE_PROJECT_PROMPT.md:28` (both now agree on the
   post-move path). **Either that README should be written or both references
   retired** — an owner/redesign call, not a QA fix.
2. **`docs/PLAYTEST_CHECKLIST.md:6` links `#reporting-protocol`; no such
   heading exists in that file.** Pre-existing, not caused here, and the only
   broken markdown link in the living docs. `PT_REDESIGN_PROMPT` rewrites this
   file — cheapest to fix there.
3. **`PT_REDESIGN_PROMPT.md:3` cites `docs/prompts/docs-restructure/`**,
   self-qualified with the post-move location. Harmless; the prompt
   self-deletes. Left alone deliberately.
4. **The ~8 half-migrated `agent/bugs/ F97` citations** and the two stale prose
   blocks in §5. Content, routed to the redesign.
5. **`SESSION_LOG.md`'s preamble still cites `docs/STATUS.md`, `docs/BUGS.md`
   and `docs/agent/ENGINE_FACTS.md`. ⛔ This is CORRECT — `archive/` is never
   edited and the translation note covers it. Do not "fix" it.** The same
   applies to all 17 files in `agent/reports/` and all 17 in `archive/`.
6. **Bare prose mentions of `MOD_DESCRIPTION.md`** were not path-qualified (not
   in §3f's replacement list); its move is recorded in README's translation
   section. Same for bare report filenames, which still resolve inside
   `agent/reports/`.
7. **O6's window** — topical fact ids, cheap only until something cites `EF-###`.

---

## Appendix — the verification actually run

Conservation was checked **twice, independently**.

1. **The chain's own accounting, re-run from the git blobs** (⚠️ pass the shas;
   `--verify-split`'s `HEAD~1` default stopped being the pre-split commit
   several commits ago, and `--verify-facts-split` has no default for that
   reason):

```
python tools/doccheck.py --verify-split 5b374eb
  12320 entry + 155 consumed + 251 notes = 12726 == 12726 source lines  OK
  every source line is claimed exactly once (checked line by line)
  116 entry files re-read and compared line-by-line to their source slices — identical

python tools/doccheck.py --verify-facts-split 2112892
  705 fact + 8 preamble = 713 == 713 source lines  OK
  DERIVATIONS: shape and block derivations both yield the same 43 starts
```

2. **This prompt's own parser, sharing no code with doccheck or the
   splitters** — re-deriving entry and fact boundaries from
   `git show 5b374eb:docs/BUGS.md` and `git show 2112892:docs/agent/ENGINE_FACTS.md`
   and byte-comparing a random sample (seeded, not cherry-picked):

```
BUGS  F93, F01, F13, F50, F63     — 159 / 37 / 6 / 10 / 32 body lines, byte-identical
FACTS EF-023, EF-005, EF-020, EF-042, EF-024 — 68 / 4 / 23 / 14 / 24 body lines, byte-identical
```

Corroborations that fell out of the independent derivation: the section-divider
positions (666, 932, 1327, 10122) reproduce **from shape alone**, without being
told; 144 `### ` headings in the source and 144 on disk; 116 of those are
ID-shaped and there are exactly 116 entry files.

⚠️ **The first run of the independent sample reported F93 as a mismatch. It was
my parser, not the migration** — entries legitimately contain `## ` subsections
mid-body, and only a `## ` at the *end* of a span is a divider. Recorded because
the next person to write a checker will hit it.

**Counts, against the spec's pre-chain baseline** — this chain moved text, so
any change would be a defect, not an update:

```
BUILD STATE (emitted by tools/doccheck.py)
- modules: 81 registered (74 default-active, 8 optional-gated files)
- Code/*.lua files: 82
- TestKit probes: 87
- BUGS index rows: 98 F + 12 D + 41 C
```

Baseline 98 F + 12 D + 41 C / 82 / 81 / 87 — **equal on every figure.**
