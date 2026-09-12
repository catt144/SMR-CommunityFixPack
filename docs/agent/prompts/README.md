# prompts/ — the map (reorganised 2026-09-11, owner ask)

| where | what | lifecycle |
|---|---|---|
| **`perma/`** | reusable, standing prompts: fire any time | never `git rm`; update in place |
| root `*.md` | live one-off prompts, not yet fired or kept by an owner ruling | `git rm` when fired or consumed |
| chain folders | multi-link efforts; finished ones are records that other docs cite | keep; each README says its state |

## `perma/` — standing prompts

| prompt | use it for |
|---|---|
| `DISPATCH.md` | **start here for ad-hoc work:** orientation, bindings, and the route table to the others |
| `LINUX_DISPATCH.md` | **FR-1**: the Linux/NVIDIA 580 crash and the TEMPORARY workaround mod; every report, feedback item or patch |
| `HANDOFF_ORCHESTRATOR.md` | ⏳ temporary: the current handoff and pending outbox; removed once the outbox is empty |
| `GENERAL_USE_PROMPT.md` | a live playtest at the keyboard (a 09-09 handoff called parts of it pre-1.1.0; verify before relying on it) |
| `RELEASE.md` | an update, end to end; uses `RELEASE_OUTBOX.md` (the staged-changes ledger) and `POST_UPLOAD_CLOSE.md` (the close-out) |
| `PUBLIC_SURFACE_SWEEP.md` | making every player-facing surface match a shipped change |
| `SITE_AUDIT.md` | auditing what the LIVE Pages site says, as opposed to what is committed |
| `STATE_EVICTION.md` | when STATE is over its byte budget |
| `DRONE_PROJECT_PROMPT.md` | drone work |
| `COMBINED_SITTING.md` | the PT-20 per-era re-check recipe (it ran 08-14; nothing owed) |

## Root — live one-offs

| prompt | state |
|---|---|
| `C88_PREFAB_BUILD.md` | **LIVE (09-11)**: build the Building-Codes-vs-prefabs fix the PDX dev asked us to carry; gated on the release lane + checklist 150 (b); deletes itself |
| `CLOGGED_BUILD.md` | ✅ **LIVE (09-11), fireable**: unstick a producer left "Clogged after a Dust Storm." (C85) — read-only sweep + two interlocks, acceptance conditions and the owner's A/B; dossier lives in the entry. Fold-in slot CLOSED empty; one open owner decision (ck154) with a stated default; deletes itself |
| ~~`migrationfix/`~~ | **CONSUMED 09-11, both links.** Link 01 (`3b41d9f`) repaired F59 by deferring the notification (a THIRD harm found while building) and stopped F60's retirement on the uncommitted-release-file gate; link 02's terminal audit ruled **SHIP A** — `reports/MIGRATIONFIX_AUDIT.md`. Link 01's HANDOFF lives in git: `git show 3b41d9f:docs/agent/prompts/migrationfix/README.md` |
| `DLC_DEEP_CHECK.md` | desk NEXT, after the fix pack is stable |
| `HOTFIX2_SITTING.md` | closed 09-09; kept for the recipes the owed v7 sitting uses |
| `SELFCHECK_PILOT.md` | rides the owed v7 sitting's boot |
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

**Removed 2026-09-11** (git history keeps them): `FR1_LINUX_SITTING.md` (ran 09-10; superseded by `perma/LINUX_DISPATCH.md`),
`FR1_TEMP_MOD_R3.md` (held, then overtaken by the live mod), `ONCALL_HANDOFF.md` (09-09; duplicated DISPATCH and nothing cited it),
`SELFCHECK_PROMISE_AUDIT.md` and `CODEX_CROSSCHECK_SELFCHECK_PROMISE.md` (both delivered their reports). Find any of them with
`git log --diff-filter=D -- docs/agent/prompts/<name>`.

**New prompts:** a reusable one goes in `perma/`; a one-off goes in the root and deletes itself when consumed.
