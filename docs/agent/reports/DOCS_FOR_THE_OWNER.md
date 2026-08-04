# What the documentation restructure actually did — for the owner (2026-08-04)

**Plain-language, written for you.** The technical spec is
`DOC_RESTRUCTURE_SPEC.md` and the migration audit is
`DOCS_RESTRUCTURE_REPORT.md`; this is the "so what" — what changed, how it
works, what it does for you and for agents, and why the drift problem should
stay solved this time.

---

## 1 · What it was, and what it is now

**Before:** three enormous files did almost everything. `BUGS.md` was 12,726
lines — every defect, every piece of evidence, every status, in one document
where a fact's copies were kept in sync by hand and by memory. `STATUS.md` was
1,581 lines, mostly history, and every session was told to read it first.
`ENGINE_FACTS.md` was 713 lines of hard-won engine truth that sessions were
told to read whole. Your handful of working documents shared a folder with a
dozen agent files. And the whole thing was held together by rules like
"always update both places" — rules that failed roughly forty recorded times
in three days, always silently.

**Now:**

```
docs/                          ← YOUR folder: 4 files you actually use
  PLAYTEST_CHECKLIST.md          your work list, redesigned to how you test
  PLAYTEST_HELP.md               your reference
  FUTURE_IDEAS.md                your parking lot
  README.md                      the one-screen map
  agent/                       ← everything agents work from
    STATE.md                     ONE screen of current truth (60-line hard cap)
    bugs/                        one file per defect (116) + a generated index
    facts/                       one file per engine fact (43) + a generated index
    WORKFLOW / FIX_POLICY        the rules
    reports/ · prompts/          records and standing prompts
  archive/                     ← history, append-only, never edited
```

Nothing was lost in the move: every byte of the old files was either carried
into the new ones or preserved verbatim in the archive, and that claim was
verified twice, by two independent programs, line by line.

## 2 · How it works — the four moving parts

1. **Each defect and each fact is its own file, with a label block on top**
   (status, priority, evidence grade — the machine-readable "front matter").
   The narrative below the label is untouched history; the label is the part
   tools can read.
2. **The indexes are GENERATED, never written by hand.** The old bug index —
   the table that kept drifting out of sync with the entries below it — no
   longer exists as something a person maintains. A script rebuilds it from
   the labels, byte-for-byte, every check. You cannot forget to update a copy
   that is derived.
3. **A checker (`doccheck`) runs on every single commit**, automatically, via
   a git hook. It verifies: every label agrees with its entry's heading, both
   indexes regenerate identically, the counts are what the files say, your
   root folder contains exactly your documents and nothing else, and no
   leftover test probe is in shipped code. If anything disagrees, **the
   commit is refused** — by machine, before the mistake can enter the record.
4. **Every session auto-loads a 25-line `CLAUDE.md`** that tells it where
   everything lives and what the rules are — so the system's conventions no
   longer depend on any session remembering to go read them.

## 3 · What it does for you

- **Your folder is yours.** Four documents, no sorting through agent files.
- **Things that need YOUR decision land where you actually look** — the
  "Decisions waiting on you" section at the top of your checklist. (We
  discovered mid-audit that owner questions used to be filed in reports you
  never read — which is why some reminders "kept surviving." That routing
  failure is structurally closed.)
- **The checklist matches how you really test**: short setup blocks grouped
  by system so one sitting clears a cluster, with the expectations and
  forensics supplied live by the agent from the entries — because you told
  us the in-the-moment flow finds more than pre-written scripts, and the
  document now agrees with you.
- **You never need to read the bug tracker.** Ask any session anything; it
  can find the answer cheaply (see below) and translate. When it explains
  poorly, that's the agent's failing, not a document you're obliged to parse.

## 4 · What it does for agents — and why that helps you

The old session-start reading was about **43,000 tokens** before an agent
touched a defect. The new one — auto-loaded map plus the one-screen STATE —
is about **1,200**. A status question that used to mean opening a
960-kilobyte file is now three small hops (map → state → index row), with the
full narrative one more hop away *only if needed*. The engine-facts question
that used to cost the whole file now costs the index plus the one fact.

That matters to you for three reasons: **speed** (less reading before
working), **cost** (tokens you were paying for re-reading history every
session now go to actual work), and — the important one — **accuracy**. An
agent burning context on boilerplate has less room to think about your
problem; an agent that reads precisely makes fewer of the inherited-claim
mistakes this project kept cataloguing. The restructure is, at bottom, an
error-reduction measure that happens to also be faster and cheaper.

## 5 · How it keeps drift from happening again

The old drift had one root shape: **the same fact stored in several places,
synced by hand, failing silently.** The fix attacks all three words:

- **"Several places" → one place.** The status lives in the entry's label;
  the index is generated from it. The most-bitten duplicate pair in the
  project's history (index row vs heading tag) no longer *can* drift,
  because one side is no longer hand-written.
- **"By hand" → by script.** The counts in STATE are pasted from the
  checker's own output, never typed. The root-folder listing is enforced
  against the map, both directions.
- **"Silently" → loudly.** This is the heart of it. Every drift instance in
  the forty-case ledger was silent — discovered days later, by accident, by
  a human. Now the remaining ways to drift hit a **red pre-commit error at
  the moment of the mistake**, whoever makes it, in whatever session, on
  whatever model. The proof came on day one: the checker's very first
  baseline run caught a stale status — one introduced *by the session that
  designed the checker*. It has run green through every commit since,
  including the ones your live playtest sittings are making right now.

And for the drift the checker can't see (prose going stale, claims without
provenance), the rules changed from folklore to written requirements:
sessions must label whether a claim was measured, read from source, or
inferred; console snippets carry "has this ever been run" markers; routed
work states the condition it's waiting on; and anything only a save/load
round-trip can falsify is queued for your keyboard rather than assumed.

## 6 · What it deliberately does NOT do — honest limits

- It cannot tell a fluent false sentence from a true one. Prose staleness is
  slowed (single sources, declared read paths), not abolished.
- It doesn't validate links or check the archive — the archive is
  *intentionally* frozen history, old paths and all, with a translation note.
- It cannot test code. The two defective load-heals were caught by you
  reloading a save, and the untested heal backlog is still the queue's item
  two. No document structure substitutes for the keyboard.
- The public-facing docs (mod page, FAQ, README) are deliberately dormant
  until launch prep, when they get rebuilt *from* this structure — which is
  most of why the structure is machine-readable at all.

## 7 · Living with it — the thirty-second guide

Use your four documents; ignore `agent/` entirely if you like. When you make
a decision, say so in any session — the agent strikes the line. If you ever
see a commit refused with red `doccheck` output, nothing is broken: that is
the system catching a mistake at the door, which used to be the moment drift
began. And if a document ever confuses you, ask the session — making it make
sense to you is now explicitly the agent's job, not yours.

*Written 2026-08-04 by the chain-12 session, as the owner-facing companion to
`CHAIN_RETROSPECTIVE.md`.*
