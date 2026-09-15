# prompts/ — the map (reorganised 2026-09-11, owner ask)

> ## ⛔⛔ FIRING FREEZE — owner ruling, 2026-09-15. Read before you fire anything here.
>
> > *"the prompts folder is rot, and its deep rot. It needs the same treatment as the other docs
> > we are doing. And all other work is on hold until its done. No prompts in the prompts folder
> > are allowed to fire until its done"*
>
> **No prompt in `docs/agent/prompts/` may be fired** — `perma/`, the root one-offs, and the chain
> folders alike — until the prompts overhaul is finished and the owner lifts this in words.
> ⛔ **No agent lifts it, narrows it, or grants itself an exception.** If a job seems to need a
> prompt from here, the answer is to ask the owner, not to fire it.
>
> **Not covered by this freeze:** triaging a player report into `docs/agent/bugs/`, reading any
> file here as a record, and work driven by a task document outside this folder.
>
> The overhaul's own brief is the one thing that runs, and it does not live here.

## Must_Read_Header
<!-- RULES -->
Rule: Keep `docs/agent/prompts/` to mapped prompts, its README map, mapped live-chain evidence and README files, and the owner-exempt `RELEASE_OUTBOX.md` ledger; put supporting documents in `docs/agent/support/`. [A3: pass]
<!-- /RULES -->

**Rule-placement answer — a guard.** `tools/doccheck.py`'s **PROMPT MAP** gate checks
the declared class and both directions of the mapped structure. It cannot decide whether prose
actually makes a session do a job: the human classification and map-description review remain.


| where | what | lifecycle |
|---|---|---|
| **`perma/`** | reusable standing prompts, plus only the exact declared migration/ledger exceptions below | update prompts in place; consuming legs remove their exact migration debt |
| root `*.md` | live one-off prompts, not yet fired or kept by an owner ruling | `git rm` the file **and delete its row here, in the same commit**, when fired or consumed |
| chain folders | live multi-link efforts; mapped evidence and README files may stay while live | leave `prompts/` when closed |

⛔ **This map lists LIVE prompts only — no tombstones** (owner ruling 2026-09-13, checklist 174).
A fired one-off leaves here entirely: no struck-through row, no "removed/consumed" prose. The outcome
already lives in its report or entry, and the grave is one command away —
`git log --diff-filter=D -- docs/agent/prompts/` (append `<name>` for one file). doccheck's
**PROMPT MAP** gate holds both directions: every prompt file has a row, every row names a file that
exists, and a struck row is RED. A row that outlives its file is how a next session fires spent work.

The `declared class` values below are gate inputs, not conclusions inferred from filenames.

## `perma/` — standing prompts

| prompt | declared class | use it for |
|---|---|---|
| `LINUX_DISPATCH.md` | `prompt` | **FR-1**: the Linux/NVIDIA 580 crash and the TEMPORARY workaround mod; every report, feedback item or patch |
| `HANDOFF_ORCHESTRATOR.md` | `prompt` | ⭐ **LIVE — the owner OVERRODE its retirement 2026-09-13** ("too many loose ends"). It carries loose ends not held by `WAITING_ON_YOU.md`. ⛔ **No session may retire it**; when its §2 list is empty a session may **ASK** the owner and nothing more. |
| `GENERAL_USE_PROMPT.md` | `prompt` | Minimal idle orientation for a session opened before the owner is ready to give it a task |
| `RELEASE.md` | `prompt` | an update, end to end; uses `RELEASE_OUTBOX.md` (the staged-changes ledger) and `POST_UPLOAD_CLOSE.md` (the close-out) |
| `RELEASE_OUTBOX.md` | `ledger-exception` | the one owner-exempt ledger; `RELEASE.md` draws every player-facing change landed since the last upload |
| `POST_UPLOAD_CLOSE.md` | `prompt` | the close-out, fired by `RELEASE.md` §4 **after** the listing exists — never before |
| `PUBLIC_SURFACE_SWEEP.md` | `prompt` | making every player-facing surface match a shipped change |
| `SITE_AUDIT.md` | `prompt` | auditing what the LIVE Pages site says, as opposed to what is committed |
| `STATE_EVICTION.md` | `prompt` | when STATE is over its byte budget |

## Root — live one-offs

| prompt | declared class | state |
|---|---|---|
| `C92_ACHIEVEMENT_BUILD.md` | `prompt` | ⛔ **LIVE, NOT FIRED — SHIPPING HELD** (owner, 2026-09-13). **Reshaped:** the owner chose to **finish the technology**, not the narrow exemption — build + test authorised, shipping held until they lift it **in words**, and **knowledge is a first-class deliverable even if it never ships**. Carries the seat/prerequisite/art choices (none are recovered intent), the four-shape behaviour decline, and `EF-093`'s self-healing residue seam as an explicit prove-or-disprove. §5 answers the achievement-reset question: the flag is `AccountStorage.achievements.unlocked[id]`, sync is one-way local→Steam, **no mod can clear it** (blacklisted), and the remedy is an `account.dat` backup. Decision **171** stays the owner's; the hold is what keeps that true. |
| `STANDDOWN_AUDIT.md` | `prompt` | **LIVE, authored 2026-09-13** (owner ask): can our full-body replacements stand down when vanilla fixes the defect? 21 of 45 modules do not delegate; `bodycheck` is at full coverage but declares a **class-c** blind spot (semantics moving under an unchanged body), and `debug.getinfo` is unavailable in the mod sandbox so only behaviour probes are buildable. Design record [D14](../bugs/D14.md). |
| `DLC_DEEP_CHECK.md` | `prompt` | desk NEXT, after the fix pack is stable |
| `HOTFIX2_SITTING.md` | `prompt` | closed 09-09; kept for the recipes the owed v7 sitting uses |
| `CAPTURE_SITTING.md` | `prompt` | owner ruling 09-09: KEEP ("we may get to it") |
| `SMRCF_CHAIN_SET.md` | `prompt` | owner ruling: keep for now (it goes with `smrcf-modbrowser/` and `smrcf-verify/`) |

## Chain folders

| chain | declared class | state |
|---|---|---|
| `fixtoggles/` | `live` | authored 09-11: on/off controls per fix; its README is the manifest, checklist 148 |
| `smrcf-modbrowser/`, `smrcf-verify/` | `live` | grouped chain entry; see `SMRCF_CHAIN_SET.md` |

**New prompts:** a reusable one goes in `perma/`; a one-off goes in the root and, when consumed,
deletes **both** itself and its row above in the commit that lands its result.
