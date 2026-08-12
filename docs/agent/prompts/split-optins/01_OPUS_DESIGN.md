# Chain prompt 1 — the design: map everything before anything moves

**Read `README.md` first — binding chain rules apply, especially rule 6 (the
standalone invariants) and rule 3 (everything below is a claim).** Staleness
check, live todo list. Game closed; no code moves in this prompt. Your output
is a design the fresh-context QA (prompt 2) will try to break — write it so an
adversary with no shared context can check every claim.

## Job 1 — the authoritative coupling map

For EACH of the 8 `Opt_*.lua` files: every `SMRFixPack.*` symbol it touches
(the README's counts are a starting claim, re-derive them), every global it
reads or writes, every vanilla function it patches (exact site), every
`Require`/`WhenActive` target. Then the closure inside `00_Core.lua`: which
Core internals those 12 public functions drag along (`defs`, `fixes`,
`UpdateSuspects`, the self-check/report machinery, the options bridge, the
boot sequencing). Deliverable: a table — symbol · used by · Core dependency ·
port disposition (copy / adapt / drop-with-reason).

⛔ **The disjointness proof (stop-condition input):** enumerate every vanilla
patch point in the 8 Opt files AND in the 74 Fix files (a grep over patch
primitives is the tool — derive the primitive list from Core, don't assume).
If any site appears in both sets, STOP per README; if none does, record the
proof (it is invariant 6b's evidence).

⚠️ Known couplings to rule on explicitly: `Opt_ClassicRockets` vs
`Fix_LanderReturnFuel` (both touch parked-rocket fuel — the suite's two probes
print near-identical messages); `Opt_DroneOverhaul`'s `DroneReport`/
`DroneOverhaulStats` surface (who consumes it — TestKit? console? checklist
docs?); `Opt_NoHomeless`'s two-pass boot self-check (the known first-pass
`inactive` artifact — its wording lives in logs and records, keep behaviour
identical); anything the SaveSanitizer (stays in the fix pack) reads that an
Opt module writes.

## Job 2 — ⛔⛔ the persisted-name inventory (invariant 6c's evidence)

Every string the 8 modules ever wrote into a savegame or account storage, with
the writing line cited: label-modifier ids (D09 dials write
`SMRFixPack_*`-shaped ids? READ the code), instance fields, GameVars, thread
names, `CurrentModOptions` keys, anything `Register`/`SetGlobal` persists.
For each: keeps-exact-bytes (default) or provably-never-persisted (cite why).
⚠️ Include what OLD pack versions wrote (the owner's saves span every era —
`git log` the Opt files for renamed ids). ⚠️ Mod Options account state is
keyed by MOD ID: a new mod id means the owner's toggles reset — confirm from
Src (`Mod.lua`, `CurrentModOptions` seeding) and record the one-minute owner
cost; the DIAL values must read as base defaults on first load, not nil.

## Job 3 — the new repo + namespace design

Working names (owner may rename at launch prep — rule 9): repo
`C:\Dev\SMR-OptInPack` · mod id `SMR_CommunityOptInPack` · global
`SMROptInPack` · log prefix `[CommunityOptInPack]`. Design: folder layout
mirroring this repo (`Code/`, `docs/agent/{bugs,facts,reports,prompts}`,
`docs/archive/`, `tools/`), junction install
(`%AppData%\…\Mods\SMR-OptInPack`), own `metadata.lua` (default_options =
the 6 toggles + 2 dials, byte-identical value strings) + `items.lua`, git
init + hooks. The fix-pack side: what leaves `metadata.lua`/`items.lua`
(file list rows 125-132, toggle entries, default_options keys), what its
doccheck expects afterwards. ⚠️ `optional = true` markers: in the new mod
these 8 are the PRODUCT — decide (and justify) whether they stay opt-in
(default OFF, as today) or default ON in a mod whose whole point is opting
in. ⭐ Recommend, don't decide: that is a one-line owner call for the report;
build proceeds with today's defaults (OFF) unless the owner has already
answered.

## Job 4 — TestKit strategy

One TestKit serves both mods (it is local-only, never shipped). Design: the 8
modules' probes re-pointed at `SMROptInPack`'s registry; `OptionsMenu` splits
into per-mod expectations (today it expects everything in one place); the
suite's gate line (`fix pack present: n/n`) learns two registries; the tally
baseline re-derivation plan (what replaces `77/0/10/0` for each matrix cell —
numbers DERIVED at verify time, predicted here).

## Job 5 — the doc/tooling migration inventory (rule 7)

Name every artifact that moves, is copied, or is adapted — file by file:
* MOVE: the 8 modules' entries (map each Opt file to its entry id — derive
  the mapping from the entries themselves, do not guess) + their INDEX rows
  → tombstone rows here.
* COPY WHOLE: `docs/agent/facts/` (all engine facts + INDEX).
* ADAPT: CLAUDE.md · FIX_POLICY · WORKFLOW (harness stacks included — mark
  N/A rather than delete) · CHAIN_METHOD · docs/README map · doccheck +
  hooks (its counts/paths re-pointed).
* NEW: the new repo's STATE.md (its own 60-line contract) · a PROVENANCE page
  (what came from where, at which commit — the no-retraining test leans on
  it) · README.md (mod-facing).
* STAYS: `docs/archive/` (append-only, history stays here); PLAYTEST material
  for the 8 (checklist sections reference across).

## Job 6 — the verification-matrix design (prompt 4 runs it)

Three cells + one witness, unattended-harness style (resurrect the u2-run
pattern: parked .txt instruments, ARM gate, self-firing on load, no console):
(a) BOTH mods: gate reads expected `74/74` + `8/8`, suite tally predicted,
options pages both present; (b) OPT-IN ALONE (fix pack disabled + FULL
RESTART — D13's four-states rule): loads, `8/8`, zero `SMRFixPack`-named
lines beyond the save's own mod-list echo; (c) FIX PACK ALONE: `74/74`,
suite re-baselined. Plus (d) SAVE-COMPAT WITNESS: a staged COPY of
`CP15PT15` (KEPT save — copy only, EF-051 rules) which ran with opt-ins ON:
load under (a), the persisted-name inventory read back live (dials, modifier
ids), zero errors. Write the expected reading for every cell BEFORE the run
(prediction-set discipline).

## Close

Write the design doc as `90_DESIGN.md` in this folder (it dies with the
folder at prompt 5; its content is integrated into both repos' records by
then). Append Notes-from-upstream to `02_FABLE_QA.md`: the design's weakest
claims, the places you chose convenience over caution, and every number QA
should re-derive. doccheck green, commit (`-F`), push, delete this file in
the same commit.
