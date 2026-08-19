# Project State — the one mandatory read

Kernel only: status + pointer, never derivation.
Eviction procedure: `agent/prompts/STATE_EVICTION.md` (byte-budgeted by doccheck; owner ruling, checklist 42).
History newest-first in `docs/archive/SESSION_LOG.md`; full pre-eviction STATE = `git show d30a10d:docs/agent/STATE.md`.
Defect truth `agent/bugs/INDEX.md` · facts `agent/facts/INDEX.md` · doc map `docs/README.md`.
Authoring `agent/WORKFLOW.md` · code `agent/FIX_POLICY.md` · chains `agent/reports/CHAIN_METHOD.md`.

## Now
- ⭐⭐ **Release = the fix pack ALONE at 1.0.0 (owner 08-17).**
- ⭐⭐ **④ upload sitting PAUSED mid-sitting on the owner's word — NOTHING IS PUBLISHED.** Upload is owner-attended.
- **Active: pre-launch sweep chain `agent/prompts/prelaunch-sweep/`.**
  - Links 1–4 consumed: L1 structure · L2 lifecycle · L3 save/exit · L4 player experience.
  - **97 verification-launch interlude consumed 08-19** (no lens, rotation intact): 3 retail autorun legs,
    `reports/97_VERIFICATION_LAUNCH.md`, logs `archive/vl97a/b/c_*`.
  - **Link 5 consumed 08-19: L5 failure/containment**, no launch (refusal reasoned: every open
    question needs the pack to throw, and `Code/` edits, probes and the console are all barred).
  - **Link 6 consumed 08-19: L6 promise vs behaviour**, no launch (refusal reasoned: its two open
    questions need mod code that reads an undeclared global, and a second mod loading in an
    order nobody can set). ⛔ **It found and FIXED the chain's first launch blocker** (`36d8817`).
  - **Link 7 consumed 08-19: L7 environment & namespace**, no launch (refusal reasoned: the live `_G`
    is the only remaining evidence and console/probe/instrument are all barred; the packed case IS run B).
    Global map taken from the COMPILER (`tools/l7_env_map.py`, Lua 5.3 bytecode, control 23/23).
  - **Link 8 consumed 08-19: L8 adversarial/hostile modder — ⛔ THE CAP; the lens pool is EXHAUSTED.**
    No launch, and the refusal is an owner-costed **ask**, not a decline: the only foreign-wrapper
    observation available is a both-packs leg needing an owner tick (`H-08`); recommended AFTER run B.
    Instruments `tools/l8_hostile_input.py` (2 controls) + `tools/l8_deference_map.py` (selftest 11/11).
    Amended `EF-058` in place (the trap is keyed on install time; mod load precedes flattening).
  - ⛔ **Launch blockers found so far: 1, fixed.** Artifacts `reports/L1..L8_*.md`; fact `EF-065`.
  - Findings `SWEEP_FINDINGS.md` (⛔ forbidden to links) · coverage `SWEEP_LEDGER.md`.
  - ⛔⛔ **Next = the TERMINAL AUDIT (`99_TERMINAL_AUDIT_fable.md`), NOT another lens.** Link 8's §9
    reads all 8 ledger rows for it: **unswept territory of consequence REMAINS** — run B/packed,
    warm-save + uninstall/reinstall, preset-FIELD patches (3 lenses named it, none swept it),
    the 53 wrappers' callers, 13 of 18 load passes vs the 237 SavegameFixups, the TestKit's own
    containment. ⛔ **A link never ruled on convergence and none may; the audit does.**
- ⛔ **Gate B criterion 1 could not fail; FIXED 08-19** — it read "packed" off `[CommunityFixPack]` lines,
  true unpacked too. Now reads `Mod.lua:1849`'s mode line. **MEASURED: 66 of 66 archived sessions say
  `unpacked`, zero `packed`.** ⚠️ Junction + packed folder both present ⇒ **unpacked WINS** at equal
  version (`Mod.lua:1770`), silently. No packed build exists on disk; stage 2 packaging is outstanding.
- **Namespace settled 08-19 (source):** the pack owns **5** globals (3 + 2 `GameVar`s), writes 21 vanilla
  names, trips **neither** engine assert, creates **zero** env shadows, never reads `Platform`; pack and
  TestKit are **disjoint on writes both ways** and the pack reads nothing the kit provides (first such
  evidence in 7 links). `content_path` is `Mod/<id>/` **packed and unpacked alike** — closes an L5 worry.
- ⛔ **`items.lua` is a RELEASE GATE, not bookkeeping** (08-19): `SaveDef` rebuilds `metadata.lua`'s
  `code` list SOLELY from its items (`Mod.lua:816-840`, `:973`) and BOTH portals force that save on a
  first upload — Steam's runs BEFORE packing. A module absent from `items.lua` ships absent.
  `upload_preflight` now compares the ordered lists; its old guard counted its own header comment.
- ⭐ **The pack HAS now run post-`2f077e8`:** 72/0/24/0 of 96 opt-in-absent, `75/75` active, 0 FAIL, 0 dialog;
  88 of 96 probes hold their exact verdict vs the pre-fix baseline `c47suite4`. Apply cost 75 modules ≈0.57 s.
- ⛔ **Still UNVERIFIED (needs ONE console sitting, checklist 44):** `2f077e8` fix ① (mark unreadable while the
  entry ends `active`) · fix ② and L2's reload prediction and link 2's `data_edited` memo (all need one `ReloadLua`).
- ⛔⛔ **Gate B has NEVER run** (packed install, junction pulled, TestKit+opt-in off) — THE release gate
  (owner: A = information, B = the gate). ⚠️ **B must budget an owner Mod-Manager tick after the junction swap
  and read the gate line first** — see H-08, or B reads as a catastrophic failure that is account state.
  - ⚖️ B's criterion 3 was `0 [LUA ERROR]`, **unsatisfiable** (48–60 vanilla `Flight.lua` lines every launch);
    corrected 08-19 to no NEW/UNATTRIBUTED, **compare the SHAPE (2 sites) never the count**.
  - Every suite number ever taken is unpacked, TestKit-on, single-load (L2).
  - Baseline `80/0/16/0` of 96 (`archive/c47suite4_*`), gates `75/75`+`8/8`; rig runs cheats.
- **Owner decisions open** (bodies in `docs/PLAYTEST_CHECKLIST.md` → "Decisions waiting on you"):
  34 (C49–C52 timing; QA owed first) · 37 Q1 (mirror core fixes to opt-in) · 37 Q2 (Steam version, after Paradox) ·
  39 (dialog re-fire) · 40 (`smr_shuttles` name) · 41 (dialog wording + sweep cap 5→8).
- Watches: C47 speed thread (descending ladder, unrun) · C48 CANDIDATE (opt-in territory; no seed-family fix code here,
  08-16) · F02/F78/F81 organic · riders C42/F99/F80/F96-R2 post-release · EF-051 falsifier = any stray save at next launch.

## Hazards — each names an action an agent could take unattended; never do it
- **H-01** Tag `fixpack-v1.0.0` sits at `7824cbc`, one commit behind HEAD, **ON PURPOSE** (fixes unverified).
  Never move, re-push, or "fix" it.
- **H-02** `metadata.lua` is **FROZEN** at 1.0.0 — no version bump, no Mod Editor save
  (every editor save runs `version = version + 1`, `Mod.lua:967`).
- **H-03** No script/console in a launched game may touch a portal API — the FIRST call **creates the listing**
  (`SteamWorkshop.lua:17-22`). Safe: `DbgPackMod`, `tools/upload_preflight.py`. Paradox before Steam.
- **H-04** Never strike ④/release holds or call the pack ready — ④ is not imminent without the owner's word.
- **H-05** Sweep fence: links never read `SWEEP_FINDINGS.md` or link reports; boring chain commit subjects;
  links 3+ RECORD ONLY except launch-blocking. STATE carries no link verdicts.
- **H-06** `EF-056`: loading a COPY of a campaign still runs that campaign's autosave rotation and
  **deletes the owner's autosaves** — pre-copy every autosave first.
- **H-07** The opt-in pack does **NOT** publish and gates nothing; ~46 parked references restore via
  `reports/PARKED_OPTIN_REFERENCES.md` at ITS launch (obligation in that repo).
- **H-08** ⛔ **Pulling a mod's junction COSTS its enable and restoring the folder does NOT buy it back**
  (`EF-055`, settled 08-19 with no Mod-Manager visit anywhere). Recovery = owner tick + restart, never an agent's.
  Never pull one to reach a configuration without booking that cost. **The opt-in pack is in that state now**
  (checklist 43).

## Rules in force (owner rulings; bodies in checklist/SESSION_LOG)
- Ship line FROZEN (08-12): `fixed` + suite + self-checks + verified save-safety IS the bar.
- A green suite does NOT authorise an upload — config B is the gate (08-17).
- Both-mods-loaded is the rig's normal config (08-12); AMENDED inside the sweep chain only:
  A/B readings are re-derived, never compared to three-mod baselines.
- Status words: `tested-attended`/`tested-unattended`; bare `tested` = legacy, closed to new work,
  never bulk-upgraded (08-15). Screen claims need an attended witness.
- ⛔ SKIPs BY NAME, never a total.
- Display name Relaunched Fix Pack; `id` + `[CommunityFixPack]` log tag KEPT (08-17).
- Never name fredware's mod on a player surface; no player load-order advice (`EF-054`, FIX_POLICY §8).
- STATE.md format: most efficient and safest — one fact per line, byte caps do the read job (08-18, item 42).

## Build state — `python tools/doccheck.py --emit-counts`, never hand-typed
```
BUILD STATE (emitted by tools/doccheck.py)
- modules: 75 registered (75 default-active, 0 optional-gated files)
- Code/*.lua files: 76
- TestKit probes: 96
- BUGS index rows: 103 F + 12 D + 52 C
```
Re-emit after any change; game pinned **1.0.7.396349** (`EF-014`).
