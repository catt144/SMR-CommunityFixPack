# docs/ — the map

Restructured 2026-08-03 (DOC_RESTRUCTURE_SPEC, owner-delegated). **Human docs
are at the root; everything an agent reads is under `agent/`; everything spent
is under `archive/`.** `python tools/doccheck.py` enforces this map — the root
list below is an allowlist checked in BOTH directions, so a new file at
`docs/` root is a red build until it is added here too.

```
docs/
  PLAYTEST_CHECKLIST.md   what waits on the owner's word or hands, nothing else;
                          entrance gate in its header, shape enforced by doccheck
  UPLOAD_WORKFLOW.md      owner's step-by-step for putting an update live:
                          pack, upload, store pages, publish the site
  FIELD_REPORT_REPLIES.md  replies to player reports (Steam, Reddit, GitHub):
                          drafts the owner posts, and the record of what went
                          up — agents draft them and keep them current
  FUTURE_IDEAS.md         parking lot, NOT a backlog. Nothing in it is work
  README.md               this map
  BUGS.md · STATUS.md     3-line stubs pointing at where they went
  agent/
    STATE.md              Pull-only current status, byte-budgeted (doccheck)
    WORKFLOW.md           process rules — layout, patches, probe hygiene, testing, release
    FIX_POLICY.md         what may be built, and how
    bugs/                 defect truth — one file per entry
    facts/                engine behaviour — one file per fact
    reports/              reports, plans, specs, audits, surveys
    prompts/              README.md = the map · perma/ = standing prompts · root = live one-offs · live chains only
    support/              protocols and references used by prompts, but not themselves fired
  archive/                spent. SESSION_LOG.md, PLAYTEST_ARCHIVE.md, RELEASE_HISTORY.md,
                          MOD_DESCRIPTION.md (frozen), retired prompts and closed prompt chains,
                          code/ = replaced shipped modules, byte-for-byte as `<name>.<release>-<sha>.lua.txt`
```

## The archive boundary

`docs/archive/` is append-only history — spent reports, retired prompts, session
logs, settled decision bodies. A root **`.rgignore`** keeps it out of a *default*
ripgrep, which is what the agent `Grep` tool runs, so an ordinary search returns
only what is **live**. This is a search boundary, not a deletion: the record is
whole, and sometimes it is exactly what you want — *"we may already have learned
this in an archived report."*

Two ways to search it **on purpose**:

```
rg <term> docs/archive/     the archive alone — naming the path defeats the filter
rg --no-ignore <term>       live + archive in one pass
```

`grep -r`, `git grep` and `git log` never consult `.rgignore` and always see
everything. If a default search comes back empty on something you are sure this
project once knew, that is the boundary working — re-run with one of the two forms
above before concluding it was never here. It is not a bug and not a missing file.

Closed prompt chains live under `archive/prompts/`. The pre-launch sweep's H-05
fence remains authoritative at `archive/prompts/prelaunch-sweep/00_CHAIN_SPEC.md`.

## The two split folders

**`agent/bugs/` — 125 entry files** (`F*.md`, `D*.md`, `C*.md`), **2 of them
grouped** (`C03-C11.md`, `C12-C38.md` — several candidates share one body, and
the file name states what it holds). `INDEX.md` is **generated** and carries
all 160 index rows. ⚠️ **Nine of the `D` entries are TOMBSTONES** (D01–D07, D09,
D12, since 2026-08-12): their modules moved to the Community Opt-In Pack and so
did their records — `B:\Dev\SMR\SMR-OptInPack\docs\agent\bugs\`. The stubs stay
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
- A **prompt** → reusable: `agent/prompts/perma/`; one-off: the `agent/prompts/` root, deleted when consumed. Update the
  map, `agent/prompts/README.md`, either way.
- A **supporting document used by a prompt** → `agent/support/`; keep the prompt's pointer and
  update `agent/support/README.md` when the document lands.
- A **session leg** → `archive/SESSION_LOG.md` (append-only, newest first).
- **Working files** (agent/subagent scratch, never cited) → `scratch/` at the repo root
  (git-ignored, swept at 14 days by the eviction prompt).
- **Durable material that must not be committed** (large binaries, logs, evidence a
  report links to) → `local/` at the repo root (git-ignored, never swept, entry-gated
  by `local/README.md` — see "Outside the repo" below for what belongs OUTSIDE the
  repo entirely instead).
- A **decision the owner must make** → `PLAYTEST_CHECKLIST.md`, if it passes that file's
  entrance gate; old bodies are in `archive/PLAYTEST_ARCHIVE.md` under `## ck<n>`. The ruling,
  once made, goes to the doc of the role that obeys it, never only to an agent's memory.
- A **reply to a player's report** (Steam, Reddit, GitHub) → `FIELD_REPORT_REPLIES.md`
  at the root. The owner posts; agents draft, record what went up, and update a
  draft in the same commit that changes the fact it states.
- **Spent** anything → `archive/`, which is append-only and never edited.

⚠️ **Reports are not authority.** When a report disagrees with `agent/bugs/` or
`agent/facts/`, the entry wins — or the report is wrong and is corrected in the
same change that discovers it.

## Outside the repo

Owner decision, 2026-09-21: material that belongs to ONE tree lives IN that
tree (`local/` above, or the tree itself). These are the exceptions — things
every SMR mod uses, so no one tree owns them:

- `C:\Dev\SMR-BugFixPack-TestKit` — shared test kit, its own repo.
- `B:\Dev\SMR\SMR-Shared` — one shared repo, pull-only, for long-term material both mods
  reference; local-only, no remote. It holds `SMR-SrcArchive\` (both archived game trees plus
  `MANIFEST.sha256`) and `workshop_fpk_archive\` (six third-party Workshop mods by Steam id,
  prior-art reference).
- `C:\Dev\SMR-ScreenCaptures` — the owner's screenshot drop folder.
- `B:\Dev\SMR\SMR-FR1` — the FR-1 workaround mod as its own local-only repo (no remote):
  `SMR-FR1-TempMod-2026-09-11\` and `SMR-FR1-CacheRoute-V2-2026-09-11\` (the source copy and
  its desk tools, run by `perma/LINUX_DISPATCH.md`; they go when that mod is retired),
  `SMR-FR1-DevPackage\` and its `.zip` (what went to the Paradox devs).

## Path translation

> 2026-09-21 (owner ask): the trees that sat directly under `C:\Dev` moved under `B:\Dev\SMR`, keeping
> their own names. `C:\Dev\SMR-SrcArchive` and `C:\Dev\workshop_fpk_archive` →
> `B:\Dev\SMR\SMR-Shared\<same name>` (one repo); the three `C:\Dev\SMR-FR1-*` folders and
> `SMR-FR1-DevPackage.zip` → `B:\Dev\SMR\SMR-FR1\<same name>` (one local-only repo);
> `C:\Dev\SMR-CommunityMods` and `C:\Dev\SMR-CommunitySaveRescue` → `B:\Dev\SMR\<same name>`; and,
> in the first pass, `C:\Dev\SMR-OptInPack` and `C:\Dev\SMR-Assets` → `B:\Dev\SMR\<same name>`.
> Live pointers were rewritten. Source-line citations in `agent/reports/`, `agent/bugs/`, `agent/facts/`,
> the archive and the `Code/Fix_*.lua` comments still name the `C:\Dev` path: translate them, the build
> named beside the path is what finds the file. The `<name>__MOVED_20260921` originals stay in `C:\Dev`
> until the owner deletes them.

> 2026-09-15: `docs/PLAYTEST_HELP.md` was dissolved by owner ruling ck182.
> Prompt-writing hazards moved to the `prompt-authoring` skill; toolkit helpers
> and the MarsDebug recipe moved to `agent/support/SMRTK_SLOTS.md`, and from
> there into `tools/SMRTK.md` on 2026-09-17; co-run
> launch mechanics moved to `agent/support/CO_RUNS.md`; F87 keeps the
> ENABLE-PATH evidence and points to its executable TestKit leg. The command
> table, central save recipes and archived-`TESTING.md` do-not-use list were cut.
> Treat older references to the former file as historical citations and use the
> owning entry, fact, skill or prompt above for current instructions.

> 2026-08-03 restructure: `docs/BUGS.md` → `docs/agent/bugs/<ID>.md`;
> `docs/STATUS.md` → `docs/agent/STATE.md`; `docs/reports/` →
> `docs/agent/reports/`; `docs/prompts/` → `docs/agent/prompts/`;
> `docs/agent/ENGINE_FACTS.md` → `docs/agent/facts/`. Pre-restructure
> documents cite the old paths; translate mentally, do not edit records.
> Renamed 2026-08-03: `FABLE_NEXT_PROMPT.md` → `agent/prompts/perma/GENERAL_USE_PROMPT.md`.

> 2026-09-11 (owner ask): the standing prompts moved into `agent/prompts/perma/` (DISPATCH, GENERAL_USE_PROMPT, RELEASE,
> RELEASE_OUTBOX, POST_UPLOAD_CLOSE, PUBLIC_SURFACE_SWEEP, SITE_AUDIT, STATE_EVICTION, DRONE_PROJECT_PROMPT, COMBINED_SITTING).
> Live references were rewritten; the archive and `metadata.lua` comments still cite `agent/prompts/<name>.md`, so translate them.

> 2026-09-11 (owner ask): `agent/reports/FIELD_REPORT_REPLIES.md` → `FIELD_REPORT_REPLIES.md` at the root, a human file (the
> owner posts, agents draft). Live references were rewritten; the archive and the committed Codex report still cite the
> old path, so translate them.

> 2026-08-17: the pack was renamed **Community Fix Pack → Relaunched Fix Pack** (display name only; the mod
> `id` and the `[CommunityFixPack]` log tag are UNCHANGED). Earlier records use the old name — translate
> mentally, do not edit records. The old name is still live in `agent/bugs/`, `agent/facts/EF-054.md` and
> several reports.

`MOD_DESCRIPTION.md` and `PLAYTEST_ARCHIVE.md` moved from `docs/` to
`docs/archive/` in the same change.
