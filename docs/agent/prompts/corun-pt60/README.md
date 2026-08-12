# Chain — corun-pt60 (the chain-8b batch leg; 3 prompts, self-consuming)

**Why this chain exists.** Owner order 2026-08-12 (*"Lets build the pt-60
one"*), picked from the attended-backlog breakdown. PT-60 is the one leg that
covers the whole 2026-08-02 batch: **seven approved fixes (F90–F96)** and
**eight technique-only conversions** that carry byte-equivalence arguments —
and an argument is not an observation. Its prediction set was written
2026-08-02 BEFORE any run and is preserved in `archive/PLAYTEST_ARCHIVE.md`
(section "PT-60 — The chain-8b batch leg", ~line 3822): **P1–P9, read
2026-08-12 by the authoring session.** A prediction that misses is the finding.

**What is honestly left of PT-60, stated so nobody re-tests settled things:**
* F92 / F93 / F95 are already **`tested`** (post-batch sittings; PT-61 closed
  F93's live half). This leg does NOT re-litigate them.
* Every launch since 08-02 has run the batch live (e.g. the corun-pt15 sitting:
  81/81 active, ~3h20m, 0 `[LUA ERROR]`) — quotable as partial P6-class
  evidence, but nobody has ever taken the LEG: the suite + ListFixes readings
  against the prediction set, the **heal + idempotence reads that only a save
  predating 2026-08-02 can give (P8)**, and the **P9 rocket-fuel-key
  clearance**. That is what this chain buys, plus execution evidence for
  F90/F91/F94/F96 and the eight conversions.

**Facts this chain stands on (authoring session, 2026-08-12; provenance per
claim, and rule 5 still applies to every one of them):**

* MEASURED (disk listing 2026-08-12): fixture = **`USA Sol 302.savegame.sav`**,
  LastWriteTime **2026-08-01 17:55:48**, 52.3 MB — the owner's own campaign
  lineage, the latest save predating the batch. Fallback: `USA Sol 298`
  (08-01 17:41). ⛔ Do NOT use the `T1/T2-UNINSTALL*` saves (uninstall-test
  lineage). The original is the owner's campaign save — **protected file #4
  for this chain**: MD5 at prep, load a COPY only, byte-verify at close-out.
* INHERITED (archive, prep verifies vs git): batch commits — fixes `a5b9db0`
  `eb4c6d6` `b22dda5` `3966fb3` `125783e` `08b5d84` `b5628a7`; conversions
  `69c02b9` `26f0b57` `ab7d432` `388c72a` `21990fb` `1471533` `8f58f30`.
* READ 2026-08-12: the archived prediction set's COUNT arithmetic is **stale**
  (written at 79 registered / 85 probes; today: **81 registered / 74
  default-active / 87 probes, retail runs 78/87** — eight `[install]` probes
  SKIP in the retail sandbox). Prep re-derives every expected number;
  the predictions' CONTENT is the 08-02 record and does not change.
* INDEX 2026-08-12: F90 `fixed` · F91 `fixed` · F92 `tested` · F93 `tested` ·
  F94 `fixed` · F95 `tested` · F96 `fixed`.
* Harness to resurrect, not rewrite: corun-pt15's, at
  `git show f289b11:docs/agent/prompts/corun-pt15/97_CP15Common.lua.txt` and
  `…/98_CP15Sitting.lua.txt` (gate that STOPS, Load/Save with EF-050 verbatim
  savename guard, Note relay, CLOCK lines, forced/organic labels).

⚠️⚠️ **STEAM CLOUD IS BACK ON (owner, 2026-08-12, deliberately — their own
independent test; they will inform an agent when it goes off again).** EF-051's
restore mechanism is therefore ARMED for the life of this chain: deleted
staged saves may reappear at the next launch. Binding consequences are rule 12
below. Do not file a returning stray as a finding.

## Manifest

| # | file | owner needed? | what it does |
|---|------|---------------|--------------|
| 1 | `01_OPUS_PREP.md` | No — game closed | re-derive the prediction set's numbers for today's build · verify fixture + stage the COPY · resurrect + park the instruments · pre-flight every console line · checklist banner |
| 2 | `02_OPUS_SITTING.md` | **YES — attended co-run, ~40–60 min** (15–20 min is their ordinary play) | load the pre-batch copy (heal lines land) → ListFixes + suite vs predictions → save/reload idempotence + P9 → owner plays → riders if their situation arises → log archived |
| 3 | `03_FABLE_AUDIT.md` | No (routes decisions) | byte-compare + read the whole log · per-prediction re-derivation · status honesty · ledger · integrate · folder EMPTY · kickoff |

## Binding chain rules

1. **Staleness check first, every prompt**: `git log --oneline -10` + `git pull`.
2. **Inbox/outbox in writing**; each prompt appends to the next prompt's
   `## Notes from upstream`, commits, deletes its own file in the same commit.
   Folder emptiness is prompt 3's done-condition.
3. **Route, don't drop**; unsure who owns a discovery → STOP AND ASK.
4. **Self-split at a clean commit boundary** if context runs short.
5. **Recorded facts are claims** — re-derive each item's ROUTE from entry +
   Src/archive before acting; everything above is what the authoring session
   verified, and anything else is trust-carried until checked.
6. **WORKFLOW binds in full**: the Co-runs harness-rule stacks (unattended-1
   1–4, batch-1 1–6, batch-2 1–9 as amended, **corun-pt15 1–3** — especially
   rule 3: **every owner verbatim spoken at a measure moment goes through
   `CP60.Note(...)` the moment it is spoken**), **R4** (state-transition claims
   carry a save/reload round trip or say PRE-RELOAD ONLY), **R7** (verdicts
   evidence the EFFECT), the run-top pack gate (**must STOP**).
7. **FIX_POLICY §3a — staged COPIES only. ⛔ FOUR protected files**:
   `TEST2H TRAIN.savegame.sav` (MD5 `103B320A1434513BC8773553096A8958`),
   `PT35FIXTURE.savegame.sav` (`D721329D1EE18604B3D6C89401F74738`),
   `PT-15.savegame.sav` (`5D0D81A3D66CA7BABFCA85D6AC118C06`), and
   **`USA Sol 302.savegame.sav` — the owner's CAMPAIGN save, this chain's
   fixture source** (prep records its MD5; byte-verify all four at close-out).
   Staged saves die in the recording commit; close-out LISTS the directory
   BY NAME against expected survivors.
8. **Probe hygiene binds unchanged** — parked .txt sources, files in TestKit
   `Code/` only while a run happens, ARM GATE before every launch (a script
   FILE, resolution cross-check over payload and brief), `PROBE SWEEP:` line
   in every result commit, R8 `git add -f` for every cited log.
9. **doccheck green before every doc commit**; STATE 60-line cap; commits via
   `git commit -F <file>`; parse sweep before any commit touching Lua; push.
   PS 5.1 hazards (no-BOM UTF-8 via Edit tool / `[System.IO.File]`; `.ps1`
   needs BOM; text-mode Python rewrites forbidden on repo docs).
10. **⛔ NO ASSUMED CAPABILITY** — first execution of anything follows
    first-execution discipline (pcall printed, liveness witness, effect read).
    EF-047 (absence only from archived logs — mid-session reads are for
    PRESENCE) · EF-048 (truthiness/type, never `== true`) · EF-049 (save
    witness = disk bytes + load-back) · EF-050 (savename VERBATIM, full
    `.savegame.sav` names).
11. **Forced-vs-organic per reading.** The staged copy, suite runs, saves and
    any staged rider setup are FORCED and disclosed; the owner's 15–20 min of
    play is ORGANIC. ⭐ Owner eyes are present: `tested` grants are REACHABLE —
    a grant must quote the owner's verdict verbatim (relayed via `CP60.Note`
    in the moment, rule 6) and name what was forced anyway.
12. **⚠️ STEAM CLOUD IS ON (owner, 2026-08-12, temporary).** Close-outs record
    **"deleted, listing verified" — NEVER "gone"** for the life of this chain.
    A staged save returning at a later launch is EF-051's measured mechanism
    working, owner-armed: attribute it, inventory it for the post-untick
    cleanup, and do NOT file it as a finding or a close-out failure. The
    WORKFLOW clause carries the same dated hold.
13. **F92/F95 change real morale/production numbers on load** (Saint +10
    morale to Religious colonists in-dome; +10% on two extractor types for an
    Astrogeologist commander). ⛔ No morale/production A/B across this leg may
    read them as drift; say so beside any such reading.
14. **⭐ Kickoff + next-chain handoff.** Prompt 3's owner report ENDS with the
    next kickoff (expected front: the **`unattended-3` build chain** — F85
    `dont_pause` flip + C39 compensation + the three-label sweep, verify on a
    `CP15PT15` staged copy — **not authored**; say what authoring takes. The
    PT-20 redo co-run queues behind it).

## Scope fence — the whole chain

**In:** PT-60's P1–P9 against the 2026-08-02 prediction set (numbers
re-derived for today's build); the P8 heal/idempotence reads on the pre-batch
copy; the P9 key clearance; execution evidence for F90/F91/F94/F96 + the eight
conversions; opportunistic riders ONLY if their situation arises during the
owner's play — **F21** re-earn (working train line), **F34(d)** (rocket mid
drone-embark, staged), **F90** (surface storm + elevator colony), **C42**
(within-session traversal witness if passages are demonstrably a route); the
standing F02/F78/F81 organic watch; whole-log review (F99
`TrackElement.lua:805` · C45 `invalid pos with no holder`).
**Out:** any code change to pack or TestKit; re-testing F92/F93/F95's
`tested` grants; F90/F93/F96's live halves beyond the riders' own reads; the
F97 rate question (chain prompt 12's job 8); everything under the drone
freeze; changing any owner decision.

## Stop conditions (chain-wide)

- `USA Sol 302.savegame.sav` missing or its fixture confirm fails → try
  `USA Sol 298`; if that also fails, bank what ran, record the failed read
  verbatim, and route the fixture question to the owner.
- Pack not loaded at the run-top gate → STOP (the gate stops the run; any
  re-enable is the owner's, handed back explicitly).
- Any `[LUA ERROR]` naming pack/TestKit code → stop that leg, record verbatim,
  continue independent legs.
- Context runs short → self-split at a clean commit boundary (rule 4).
