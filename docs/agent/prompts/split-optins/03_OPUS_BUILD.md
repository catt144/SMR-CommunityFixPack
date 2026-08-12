# Chain prompt 3 — the build: execute the split, both repos, no launch

**Read `README.md` first — binding chain rules apply.** Staleness check, todo
list. Game closed. **Precondition: prompt 2's verdict at the top of
`90_DESIGN.md` is BUILD — if it is not there or not BUILD, stop.** Work the
MUST-FIX list into the plan before the first file moves. The design doc is
your spec; where reality disagrees with it mid-build, STOP AND RECORD before
improvising (rule 3 cuts both ways — a design claim failing IS a finding).

## Order of work (each step is a commit boundary — rule 4)

1. **Scaffold the new repo** (`C:\Dev\SMR-OptInPack` per design): git init,
   folder layout, hooks (`git config core.hooksPath tools/hooks`), ported
   doccheck re-pointed at its own counts, junction install. Commit 1 is the
   empty-but-teaching repo: CLAUDE.md, docs/README map, STATE.md (its own
   60-line contract, honest "mid-split" state), WORKFLOW + FIX_POLICY +
   CHAIN_METHOD adapted copies (N/A-marked, never silently dropped),
   `docs/agent/facts/` copied whole, the PROVENANCE page (source repo +
   commit sha for every ported artifact — this session's shas, kept current
   as you go).
2. **Port the framework:** `00_Core.lua` copied → new namespace per the
   design's disposition table (global `SMROptInPack`, log prefix, own
   version). ⛔ Persisted-name inventory pinned open beside you: any string
   on it keeps its exact bytes. Parse sweep (luaparser) green before commit.
3. **Move the 8 modules:** `Opt_*.lua` → new repo `Code/`, namespace edits
   ONLY (invariant 6d); their probes re-pointed in TestKit per design;
   `metadata.lua` + `items.lua` + `default_options` written on BOTH sides
   (new mod gains, fix pack loses rows 125-132 + toggles + option keys).
   ⚠️ Boot-order: preserve the Core-loads-first property under the new repo's
   file naming. ⚠️ The NoHomeless two-pass self-check keeps its wording
   byte-identical (its `inactive`-then-`applied` boot shape is recorded in
   logs and entries).
4. **Doc migration (rule 7):** the 8 entries MOVE (tombstone rows here —
   INDEX regenerates, edit entries only), checklist cross-references updated,
   both repos' doccheck GREEN. The fix-pack side of this chain's records
   stays here; the new repo's STATE says what it is and what is owed.
5. **Static acceptance (no launch):** parse sweep both repos + TestKit ·
   doccheck both repos (`--emit-counts` re-emitted; fix-pack counts move to
   their derived post-split values, and the design's predicted counts are
   compared against the emitted ones — a mismatch is a finding, not a
   retype) · grep-proof of invariant 6a (zero `SMRFixPack` in new repo's
   executable code) · the persisted-name inventory diffed against the moved
   files byte-for-byte · PROBE SWEEP line in every commit touching TestKit.

## What you may NOT do

- Launch the game (that is prompt 4's job, under its harness).
- Rename any persisted string, change any behaviour, "improve" any module.
- Create a public remote (rule 9) — the new repo stays local git.
- Delete anything from `docs/archive/` here, or move history.

## Close

Append Notes-from-upstream to `04_OPUS_VERIFY.md`: both repos' HEAD shas, the
emitted post-split counts (both sides), the persisted-name inventory verbatim
(prompt 4 reads it back live), the matrix cells' predicted readings from the
design (updated for anything the build learned), and every deviation from the
design with its ruling. doccheck green ×2, commit (`-F`), push what has a
remote, delete this file in the same commit.

---

## Notes from upstream (prompt 2 — QA, 2026-08-12, HEAD `1c00819`)

**VERDICT: BUILD.** The full findings block is at the top of `90_DESIGN.md` —
read it with the design; it is part of the spec. Staleness was clean in both
repos; nothing was launched. The QA closed the design's one open Src hole
itself: `GetFuelResourceRequest` is argument-free at declaration
(`UniversalRocket.lua:1639`) and at all 17 shipped call sites.

### MUST-FIX-IN-BUILD (each one line, each checkable)

1. ⛔ **Core port procedure = whole-file token rename FIRST** (`SMRFixPack` →
   `SMROptInPack`, `SMRFixPack_Disabled` → `SMROptInPack_Disabled`,
   `SMRFixPack_Optional` → `SMROptInPack_Optional`), THEN the design's listed
   literal adaptations (prefix `:27`, id `:64`/`:401`, dialog `:512-514`, log
   text `:412`) — the §1.3 table's "COPY verbatim" for `Register`/`DataPatch`
   is WRONG at `:384`/`:270` (fix-pack-absent = nil-index crash at every
   Register). Check: `grep -c SMRFixPack <new>/Code/00_Core.lua` → 0 outside
   comments; prompt 5's byte-compare diff-list includes `:270`, `:384`, `:412`.
2. ⛔ **Do NOT add varargs to `Fix_LanderReturnFuel`** — the §1.4a "repair if
   false" branch is dead (Src-verified argfree); the only edit owed is the
   citation into the design record, which the QA block already carries.
3. **TestKit `99_FixtureCarry.lua`:** add `SMRFixPack_no_homeless` to
   `INSTANCE_FIELDS` (third Opt-written persisted field, pre-existing gap),
   exact bytes, "(opt-in mod)" comment — alongside the design's two-prefix
   scan change.
4. **The §4.4 activation instrument fires AFTER ClassesBuilt** (RunAll-time
   or a late OnMsg like LoadGame/CityStart), else NoHomeless's F100
   second-pass Require fails again in (a2)/(b); restore original option
   values in every branch (the DroneStatDials probe's shape).
5. **Tombstones are NINE entries, explicitly:** D01 D02 D03 D04 D05 D06 D07
   D09 D12 (§5.1's "D01.md…D05.md, D09.md, D12.md" shorthand drops D06/D07).
   Index rows here stay `102 F + 12 D + 46 C`; §3.5's "102 F + 4 D"
   alternative is the rejected shape.
6. **The new repo carries its own copies of the bans:** the §2.1
   persisted-name inventory verbatim (FIX_POLICY §3 addendum or PROVENANCE)
   and a repo-local "how to run the suite" pointer (TestKit path, OptStatus
   surface, gate-line shapes) — rule 8's "what is banned?" and "how do I run
   the suite?" must cite new-repo files.
7. **Record the load-order fact** (QA-pinned): inter-mod order =
   `AccountStorage.LoadMods` enable order (`Mod.lua:1992`, `:2110-2114`,
   `:2256`) — new-repo facts copy gains it dated from the copy; prompt 4
   still logs the observed order.
8. **Record the two extra fix→opt consumer edges** beside §1.5's
   `IsLRTransportAvailable`: `Fix_ArrivalDeaths:192` → `ChooseDome`;
   `Fix_LowStorageWarning`/`Fix_BombardmentSpread` →
   `AddObjectToNotification`/`RemoveObjectFromNotification`. Call-time global
   reads; order-independent; record-only, no code change.

### The three weakest claims that still passed (attack order for prompts 4/5)

1. **"The other 80 probes are state-independent between legs"** (§6.2's
   arithmetic rests on it) — assumption, not measurement; prompt 4 diffs all
   88 verdicts BY NAME against u2run3's rows (the C43 precedent), never
   totals.
2. **`CP15PT15`'s witness value is unverified** — if it carries no ack
   stamps, no policy flags and base dials, cell (d) samples far less than it
   claims; report population sizes per row (the "close cases completely"
   rule) and stage a second save BEFORE the run if the copy proves thin.
3. **The doccheck count-fix** (`optional` = anchored def-field count;
   `default_active = modules - optional`) — arithmetic verified today
   (7 def-fields; 75/74/0/74 predicted here, 9/8/7/1 new repo), but the
   emitted `--emit-counts` is the adjudicator; a mismatch is a finding, not a
   retype.
