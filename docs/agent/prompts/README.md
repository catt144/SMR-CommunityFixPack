# prompts/ — the map (reorganised 2026-09-11, owner ask)

| where | what | lifecycle |
|---|---|---|
| **`perma/`** | reusable, standing prompts: fire any time | never `git rm`; update in place |
| root `*.md` | live one-off prompts, not yet fired or kept by an owner ruling | `git rm` the file **and delete its row here, in the same commit**, when fired or consumed |
| chain folders | multi-link efforts; finished ones are records that other docs cite | keep; each README says its state |

⛔ **This map lists LIVE prompts only — no tombstones** (owner ruling 2026-09-13, checklist 174).
A fired one-off leaves here entirely: no struck-through row, no "removed/consumed" prose. The outcome
already lives in its report or entry, and the grave is one command away —
`git log --diff-filter=D -- docs/agent/prompts/` (append `<name>` for one file). doccheck's
**PROMPT MAP** gate holds both directions: every prompt file has a row, every row names a file that
exists, and a struck row is RED. A row that outlives its file is how a next session fires spent work.

## `perma/` — standing prompts

| prompt | use it for |
|---|---|
| `DISPATCH.md` | **start here for ad-hoc work:** orientation, bindings, and the route table to the others |
| `LINUX_DISPATCH.md` | **FR-1**: the Linux/NVIDIA 580 crash and the TEMPORARY workaround mod; every report, feedback item or patch |
| `HANDOFF_ORCHESTRATOR.md` | ⭐ **LIVE — the owner OVERRODE its retirement 2026-09-13** ("too many loose ends"). It carries the loose ends `DISPATCH.md` and `WAITING_ON_YOU.md` cannot hold. ⛔ **No session may retire it**; when its §2 list is empty a session may **ASK** the owner and nothing more. |
| `GENERAL_USE_PROMPT.md` | ⭐ **RESCOPED 2026-09-13, owner ask.** Minimal catch-all for ad-hoc questions and player-report triage; playtest sittings are now agent-authored at sitting time from `WORKFLOW.md`/`PLAYTEST_HELP.md`/`PLAYTEST_CHECKLIST.md`, not scripted here |
| `RELEASE.md` | an update, end to end; uses `RELEASE_OUTBOX.md` (the staged-changes ledger) and `POST_UPLOAD_CLOSE.md` (the close-out) |
| `RELEASE_OUTBOX.md` | the ledger `RELEASE.md` draws from: every player-facing change landed since the last upload |
| `POST_UPLOAD_CLOSE.md` | the close-out, fired by `RELEASE.md` §4 **after** the listing exists — never before |
| `PUBLIC_SURFACE_SWEEP.md` | making every player-facing surface match a shipped change |
| `SITE_AUDIT.md` | auditing what the LIVE Pages site says, as opposed to what is committed |
| `STATE_EVICTION.md` | when STATE is over its byte budget |
| `DRONE_PROJECT_PROMPT.md` | drone work |
| `COMBINED_SITTING.md` | the PT-20 per-era re-check recipe (it ran 08-14; nothing owed) |
| `CO_RUNS.md` | the attended co-run protocol (labor-inverted experiment legs); binding when it applies |
| `SMRTK_SLOTS.md` | preload a sitting into TestKit's agent-owned slots, write predictions, then hand off to the owner |

## Root — live one-offs

| prompt | state |
|---|---|
| `C92_ACHIEVEMENT_BUILD.md` | ⛔ **LIVE, NOT FIRED — SHIPPING HELD** (owner, 2026-09-13). **Reshaped:** the owner chose to **finish the technology**, not the narrow exemption — build + test authorised, shipping held until they lift it **in words**, and **knowledge is a first-class deliverable even if it never ships**. Carries the seat/prerequisite/art choices (none are recovered intent), the four-shape behaviour decline, and `EF-093`'s self-healing residue seam as an explicit prove-or-disprove. §5 answers the achievement-reset question: the flag is `AccountStorage.achievements.unlocked[id]`, sync is one-way local→Steam, **no mod can clear it** (blacklisted), and the remedy is an `account.dat` backup. Decision **171** stays the owner's; the hold is what keeps that true. |
| `STANDDOWN_AUDIT.md` | **LIVE, authored 2026-09-13** (owner ask): can our full-body replacements stand down when vanilla fixes the defect? 21 of 45 modules do not delegate; `bodycheck` is at full coverage but declares a **class-c** blind spot (semantics moving under an unchanged body), and `debug.getinfo` is unavailable in the mod sandbox so only behaviour probes are buildable. Design record [D14](../bugs/D14.md). |
| `RULES_HEADERS.md` | ⭐ **LIVE, FIRING 2026-09-15.** The owner's 2026-09-14 design ruling: **N scattered rules become N local header blocks plus ONE kernel rule**, so a session that never opens a doc never carries that doc's rules. ⛔ **REVISED `9229434` onto ck179 and the 2026-09-15 rulings — read §2's GOVERNING BLOCK first; it overrides anything earlier in the brief.** Census and inventory every rule, classify each as doc-local / task-local / global / redundant / **dead**, record a rule-test verdict per rule, **determine the writing style and restyle the whole corpus to it** (the executing agent's call, no sign-off gate; one constraint — **no emoji in a rule**), land the headers byte-capped one commit per source doc, **empty `STATE.md` of rules**, move `WORKFLOW.md`'s 10 globals and the single kernel line into **`CLAUDE.md`** (with its `--regen`'d `AGENTS.md` mirror in the same commit), and build the structural doccheck check. Delivery is a **two-half report** whose asks are **batched by question, not by file**. ⚠️ Carries the definition that keeps it tractable: the checklist's **319 `⛔` are 317 records and 2 rules** — an inventory that counts every `⛔` is useless. ⛔ The old **OWNER GATE is discharged**; the owner reads the report, not a blocking checkpoint. ⛔ Must not fold in checklist **177**'s open marker gate. |
| `DLC_DEEP_CHECK.md` | desk NEXT, after the fix pack is stable |
| `HOTFIX2_SITTING.md` | closed 09-09; kept for the recipes the owed v7 sitting uses |
| `CAPTURE_SITTING.md` | owner ruling 09-09: KEEP ("we may get to it") |
| `SMRCF_CHAIN_SET.md` | owner ruling: keep for now (it goes with `smrcf-modbrowser/` and `smrcf-verify/`) |

## Chain folders

- `fixtoggles/`: **LIVE** (authored 09-11): an on/off button per fix, Beta labels, linked buttons; link 09 researches
  versioning for a B step. Its README is the manifest; checklist 148.
- `arming/`: the unattended-leg harness (`tools/arm_leg.ps1` reads it). Infrastructure, not a prompt.
- `hotfix2/`: done (v6 shipped 09-09); STATE and the entries cite its manifest.
- `vanillahunt/`: done (CLOSED 09-10).
- `prelaunch-sweep/`: done 08-20. ⛔ H-05 sweep fence: never read `SWEEP_FINDINGS.md` to reach a verdict.
- `smrcf-modbrowser/`, `smrcf-verify/`: see `SMRCF_CHAIN_SET.md`.

**New prompts:** a reusable one goes in `perma/`; a one-off goes in the root and, when consumed,
deletes **both** itself and its row above in the commit that lands its result.
