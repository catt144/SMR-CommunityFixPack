# Chain prompt 2 — fresh-context adversarial QA of the design (the gate)

**Read `README.md` first — binding chain rules apply.** Staleness check, todo
list. You are a FRESH context reviewing `90_DESIGN.md` adversarially — the
owner ordered a "very good and cautious chain", and this prompt is the
caution. **The build (prompt 3) may not run unless your verdict is BUILD.**
Precedent: the house fresh-context-QA rule (adopted 2026-08-04 after a design
error survived its own author's review; recorded in WORKFLOW).

**Everything in the design is a claim (rule 3). Your job is to re-derive the
load-bearing ones from Src/code yourself, not to read the design for tone.**

## The audit, hardest first

1. **⛔⛔ The persisted-name inventory (invariant 6c).** Re-derive it
   independently: grep the 8 Opt files (and their `git log -p` history) for
   every write that can reach a save or account storage — modifier ids,
   fields, GameVars, thread names, options keys. Compare against the design's
   inventory. **A name the design missed is a REJECT by itself** — this is
   the one place the split can corrupt the owner's saves. Check the D09 dial
   ids byte-for-byte against `Opt_DroneStatDials.lua`'s maps and
   `metadata.lua`'s default_options strings.
2. **The disjointness proof (invariant 6b).** Re-run the patch-point
   enumeration with your own method (derive the patch-primitive list from
   `00_Core.lua` yourself first). Any site in both mods' sets that the design
   missed → REJECT. Rule explicitly on the ClassicRockets/LanderReturnFuel
   adjacency the README flags.
3. **Fix-pack-absent completeness (invariant 6a).** Walk the design's Core
   port-disposition table: for every symbol an Opt file uses, is the ported
   copy self-sufficient? Hunt the implicit couplings the table format hides —
   boot ORDER (Core loads first by filename today; does the new repo's file
   naming preserve that?), `OnDataReady`/preset-postprocess timing, the
   two-pass NoHomeless self-check, anything reading `SMRFixPack.fixes`
   directly.
4. **Both-installed hazards.** Two registries, two options pages, two log
   streams: check the design for name collisions in GLOBALS beyond the two
   namespaces (helper functions promoted to `_G`? `SetGlobal` targets?), and
   for double-boot lines that would poison future log greps (the corun-pt60
   audit found a third heal look-alike this way — same failure class).
5. **The doc migration (rule 7) and the no-retraining spec (rule 8).** Does
   the inventory name every entry the 8 modules map to (re-derive the mapping
   yourself from `docs/agent/bugs/`)? Does the adapted-WORKFLOW plan keep the
   harness stacks (marked N/A where N/A) rather than dropping them? Is the
   PROVENANCE page speced? Would a fresh session in the new repo pass rule
   8's question list on the design's scaffolding — walk each question against
   the spec.
6. **The verification matrix (job 6).** Are the four cells' expected readings
   written as PREDICTIONS with derivable numbers? Does cell (b) carry the
   full-restart rule (D13's four states)? Does cell (d) stage a COPY of
   `CP15PT15` and read back the inventory LIVE? Is every instrument in the
   parked-.txt/ARM-gate pattern (probe hygiene)?
7. **Scope-fence sweep.** Anything in the design that changes behaviour,
   renames a persisted string, or grows a feature → strike it, cite the
   fence.

## Verdict

One of: **BUILD** (design sound; list any conditions as MUST-FIX-IN-BUILD
items, each one-line and checkable) · **REVISE** (name the defects; prompt 1
is re-run against your findings — write its corrective Notes-from-upstream
yourself) · **STOP** (a stop-condition fired; route to the owner per README).

## Close

Record the verdict + findings at the top of `90_DESIGN.md` (dated, signed
"prompt 2 QA"). Append Notes-from-upstream to `03_OPUS_BUILD.md`: the verdict,
the MUST-FIX list, and the three claims you found weakest even if passing.
doccheck green, commit (`-F`), push, delete this file in the same commit.
