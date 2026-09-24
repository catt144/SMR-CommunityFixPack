# prompts/ — the map (reorganised 2026-09-11, owner ask)

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
| `release_prompt.md` | `prompt` | the complete release lifecycle: prepare surfaces, HOLD for the owner's upload, then resume—often fresh—to verify and close |
| `RELEASE_OUTBOX.md` | `ledger-exception` | the one owner-exempt ledger; `release_prompt.md` derives the batch from Pending and clears it into `docs/archive/RELEASE_HISTORY.md` only after confirmed upload |
| `STATE_EVICTION.md` | `prompt` | requested STATE cleanup or a size warning; apply the complete four-part admission door to every section and verify refused content's homes; also the checklist sweep that purges or archives items 30 days old |
| `GAME_PATCH_PROMPT.md` | `prompt` | a new game build is on disk: `tools/patchcheck.py` sweeps both packs to a none/scoped/full verdict, then reads, in-game legs, FIX/REMOVE prompts, the opt-in `gamepatch/` outbox entry and a limits review |

## Root — live one-offs

| prompt | declared class | state |
|---|---|---|
| `C92_ACHIEVEMENT_BUILD.md` | `prompt` | ⛔ **LIVE, NOT FIRED — SHIPPING HELD** (owner, 2026-09-13). **Reshaped:** the owner chose to **finish the technology**, not the narrow exemption — build + test authorised, shipping held until they lift it **in words**, and **knowledge is a first-class deliverable even if it never ships**. Carries the seat/prerequisite/art choices (none are recovered intent), the four-shape behaviour decline, and `EF-093`'s self-healing residue seam as an explicit prove-or-disprove. §5 answers the achievement-reset question: the flag is `AccountStorage.achievements.unlocked[id]`, sync is one-way local→Steam, **no mod can clear it** (blacklisted), and the remedy is an `account.dat` backup. Decision **171** stays the owner's; the hold is what keeps that true. |
| `STANDDOWN_AUDIT.md` | `prompt` | **LIVE, authored 2026-09-13** (owner ask): can full-body replacements stand down when vanilla fixes a defect? The old 21-of-45 split is an explicitly re-derived seed, not a current total; scoped 2026-09-19 to the runtime decline for players (the desk class-c detector is `tools/patchcheck.py`'s D1). Design record [D14](../bugs/D14.md). |
| `DLC_DEEP_CHECK.md` | `prompt` | live one-off chain-authoring job after the fix pack is stable; re-emits the DLC inventory, writes a mapped `dlccheck/` chain, then consumes itself without firing a link |
| `SMRCF_CHAIN_SET.md` | `prompt` | owner ruling: keep the C35 detector plus parked C52 chain; descendants are independent and update this grouped entry as they close |
| `MIGRATION_HUB_HANDOFF_high.md` | `prompt` | **LIVE, single use, authored 2026-09-24** (owner ask): remaining work after the migration audit, cross-check, hub audit and the two sittings on TheGodUncle's save; resweep and S1/S2/S3/S5 filing done (C114-C117); carries the one-release ruling for the hub set, the reporter reply, the build order and the owed measurements; consumed when its last item lands |
| `LOAD_ORDER_CROSSCHECK_high.md` | `prompt` | **LIVE, single use, authored 2026-09-24** (owner ask): open-scope Codex exploration of whether the pack can load before other mods at any level, and whether that would solve load-order issues; rechecks EF-054, EF-025 and FIX_POLICY §8 on 1.1.1; report-only; consumed by the report commit |

## Chain folders

| chain | declared class | state |
|---|---|---|
| `fixtoggles/` | `live` | authored 09-11: on/off controls per fix; its README is the manifest, checklist 148 |
| `smrcf-modbrowser/`, `smrcf-verify/` | `live` | grouped entry: C35 detector is fireable only after the root freeze; C52 stays parked until an explicit owner unpark |

**New prompts:** a reusable one goes in `perma/`; a one-off goes in the root and, when consumed,
deletes **both** itself and its row above in the commit that lands its result.
