# docs/ — the map

Restructured 2026-08-03 (DOC_RESTRUCTURE_SPEC, owner-delegated). **Human docs
are at the root; everything an agent reads is under `agent/`; everything spent
is under `archive/`.** `python tools/doccheck.py` enforces this map — the root
list below is an allowlist checked in BOTH directions, so a new file at
`docs/` root is a red build until it is added here too.

```
docs/
  PLAYTEST_CHECKLIST.md   the PT tests, the reporting protocol, and
                          "Decisions waiting on you" — the owner's file
  PLAYTEST_HELP.md        playtest reference: console facts, commands, fixtures
  UPLOAD_WORKFLOW.md      owner's step-by-step for putting an update live:
                          pack, upload, store pages, publish the site
  FUTURE_IDEAS.md         parking lot, NOT a backlog. Nothing in it is work
  README.md               this map
  BUGS.md · STATUS.md     3-line stubs pointing at where they went
  agent/
    STATE.md              READ FIRST. Current-state kernel, byte-budgeted (doccheck)
    WORKFLOW.md           process rules — commits, probe hygiene, todo discipline
    FIX_POLICY.md         what may be built, and how
    bugs/                 defect truth — one file per entry
    facts/                engine behaviour — one file per fact
    reports/              reports, plans, specs, audits, surveys
    prompts/              the standing prompts + any live one-off
  archive/                spent. SESSION_LOG.md, PLAYTEST_ARCHIVE.md,
                          MOD_DESCRIPTION.md (frozen), retired prompts
```

## The two split folders

**`agent/bugs/` — 125 entry files** (`F*.md`, `D*.md`, `C*.md`), **2 of them
grouped** (`C03-C11.md`, `C12-C38.md` — several candidates share one body, and
the file name states what it holds). `INDEX.md` is **generated** and carries
all 160 index rows. ⚠️ **Nine of the `D` entries are TOMBSTONES** (D01–D07, D09,
D12, since 2026-08-12): their modules moved to the Community Opt-In Pack and so
did their records — `C:\Dev\SMR-OptInPack\docs\agent\bugs\`. The stubs stay
because `INDEX.md` is generated from contiguous `seq`, and because hundreds of
references resolve through them. *(These counts are prose, and doccheck does not
check prose — they read 116/151 until 2026-08-12, an era stale. Re-derive from
`INDEX.md` before quoting them.)* `_notes.md` is the residue that belonged to no entry: the
old intro, the five `##` section dividers, the "Not yet swept" backlog, and
C02's row, which points at entry text that never existed.

**`agent/facts/` — 54 fact files** (`EF-001` … `EF-054`; the first 43 are one
per top-level bullet of the old ENGINE_FACTS.md, in source order, ids stable).
`INDEX.md` is **generated**; `_preamble.md` is the prose that opened the old
file. ⭐ **This folder was COPIED WHOLE into the Community Opt-In Pack on
2026-08-12** — engine facts describe the GAME and both mods need them. The two
copies **diverge from that date**: a fact learned here should usually be carried
across, and one learned there will not appear here by itself.

⚠️ **`INDEX.md` is generated in both folders and is never hand-edited.** Edit
the entry or fact file; doccheck regenerates the index and fails on any
difference. Generated files say so on line 1.

## Where new things go

- A **defect** → a new file in `agent/bugs/`. Never a report, never FUTURE_IDEAS.
- An **engine fact** → a new `EF-###.md` in `agent/facts/`, with its date.
- A **rule that binds future work** → `agent/WORKFLOW.md` or `agent/FIX_POLICY.md`,
  not buried in a report.
- A **report, plan, spec, audit or survey** → `agent/reports/`.
- A **prompt** → `agent/prompts/`; one-offs delete themselves when consumed.
- A **session leg** → `archive/SESSION_LOG.md` (append-only, newest first).
- A **decision the owner must make** → `PLAYTEST_CHECKLIST.md` →
  "Decisions waiting on you". Never only in an agent doc.
- **Spent** anything → `archive/`, which is append-only and never edited.

⚠️ **Reports are not authority.** When a report disagrees with `agent/bugs/` or
`agent/facts/`, the entry wins — or the report is wrong and is corrected in the
same change that discovers it.

## Path translation

> 2026-08-03 restructure: `docs/BUGS.md` → `docs/agent/bugs/<ID>.md`;
> `docs/STATUS.md` → `docs/agent/STATE.md`; `docs/reports/` →
> `docs/agent/reports/`; `docs/prompts/` → `docs/agent/prompts/`;
> `docs/agent/ENGINE_FACTS.md` → `docs/agent/facts/`. Pre-restructure
> documents cite the old paths; translate mentally, do not edit records.
> Renamed 2026-08-03: `FABLE_NEXT_PROMPT.md` → `agent/prompts/GENERAL_USE_PROMPT.md`.

`MOD_DESCRIPTION.md` and `PLAYTEST_ARCHIVE.md` moved from `docs/` to
`docs/archive/` in the same change.
