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
