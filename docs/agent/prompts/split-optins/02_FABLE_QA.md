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

---

## Notes from upstream (prompt 1 — design, 2026-08-12, HEAD `7efe1dd`)

`90_DESIGN.md` is written. Staleness clean in both repos (pack `7efe1dd`,
TestKit `d8e1fbf`, both trees clean). Nothing was moved, edited or launched.
The one non-chain edit this prompt made outside the folder is a
recommendation line under checklist item 15 (§3.7's owner call, already logged
there — no new decision was opened).

### ⛔ The single thing to attack first — the disjointness proof does NOT come out clean

**It found TWO cross-set vanilla patch points, not zero**, and the design rules
that this is not a chain stop. That ruling is the load-bearing judgement of the
whole design; if you overturn it, the verdict is STOP, not REVISE.

* `UniversalRocketBase:GetFuelResourceRequest` — `Fix_LanderReturnFuel.lua:38`
  vs `Opt_ClassicRockets.lua:81` (the pair the README flagged).
* `Drone:CleanUnreachables` — `Fix_DroneUnreachableForever.lua:80` vs
  `Opt_DroneOverhaul.lua:220`. ⚠️ **The README did not anticipate this one.**

The argument is §1.4a: both are *chained* wraps, neither replaces, and each
site's two bodies compose order-independently (mutually exclusive conditions on
`GetDepartureLocType()` for the first; pre-wrapper vs post-wrapper around the
same forwarded call for the second). Attack it on: is "order-independent
chained composition" really what invariant 6b protects, or does the README mean
the strict thing it says? Does the *engine* give any ordering guarantee we
should be recording anyway? And is there a third shared site my primitive list
was blind to — I derived primitives from `00_Core.lua` and enumerated
class-method wraps by resolving `local <alias> = <Class>` bindings, so a patch
installed through a shape I did not model (a `rawset` on a class table, a
metatable, a write into a shipped table by index) would be invisible to me.

### The claims I would break first, in the order I would break them

1. **§1.4a residual, and it is the one hole I left open on purpose.**
   `Fix_LanderReturnFuel`'s wrapper is `function R:GetFuelResourceRequest()`
   with **no varargs**, forwarding `orig(self)` — so if the fix pack loads
   *second* it drops any extra argument before D01's wrapper sees it. I asserted
   this is inert because the shipped method takes none, and **I did not open
   `UniversalRocket.lua:1639-1650` to confirm it.** That is a Src read you
   should do. If it is wrong, the repair is fix-pack-side and legal.
2. **The tally predictions (§6.2) are arithmetic on one archived log.** I
   re-derived the baseline's 10 SKIP names from
   `docs/archive/u2run3_Mars.exe-20260811-02.01.06.log` and concluded that all 8
   opt-module probes PASSed there, i.e. the owner's toggles are ON. Everything
   downstream (`78 = 77 + 1`, `72 = 78 − 6`, `70 = 78 − 8`) rests on that
   reading and on "the other 80 probes are state-independent between legs". Both
   are checkable; the second is the weaker.
3. **⛔ The README's and prompt 4's `8/8` prediction is wrong and I changed it.**
   Mod Options state is keyed by MOD ID, so a new id means the 7 toggles come up
   OFF: the opt-in gate reads **`1/8`** at fresh defaults. I introduced a cell
   (a2) with an in-session activation instrument (§4.4) to reach `8/8` without
   touching account storage. If you think that instrument is illegitimate — it
   fires `Msg("ApplyModOptions", …)` after rawsetting `Mods[id].options`, the
   path the `DroneStatDials` probe already uses — say so, because cell (a2) is
   the only cell that proves the modules still WORK after the port.
4. **Cell (d)'s dial expectation inverts the obvious reading.** I predict the
   D09 modifiers are **absent** after loading `CP15PT15` under the new mod,
   because the dials reset to base and `PostLoadGame` removes stale modifiers by
   id. Absence = PASS there. If that is wrong, the save witness is measuring
   nothing at the exact place invariant 6c is most exposed.
5. **§5.1's tombstone shape is driven by tooling, not taste.** `doccheck.py`
   requires contiguous `seq` and regenerates `INDEX.md` byte-for-byte, so a
   hand-added "one-line tombstone row" in the index is impossible. I chose
   reduced tombstone *entry files*. Check that this actually keeps
   `check_entries` and `check_index` green, especially the heading-tag status
   parse (`doccheck.py:97-103` takes the FIRST vocabulary word).
6. **§5.5 deliberately fails rule 8's letter** by leaving
   `PLAYTEST_CHECKLIST.md` / `PLAYTEST_HELP.md` single-sourced in this repo.
   Named, not hidden. Rule on it.

### Numbers to re-derive yourself (I got different answers from the README on all of these)

* `00_Core.lua` is **527** lines, not 504.
* There are **73** `Fix_*.lua`; the "74" is registered fix-pack modules
  (73 + `90_SaveSanitizer`). README invariant 6e's arithmetic is right; prompt
  1's phrasing was not.
* The README's Core usage counts are **raw text counts including comments**.
  Executable-only: `ListFixes` **0**, `IsActive` **7** (⛔ `Opt_MultipleSuns`
  does not call it — it reads `SMRFixPack.fixes` directly at `:73-74`),
  `OnDataReady` 1, `Log` 1. `PackVersion`/`DataPatch`/`UpdateSuspects` have
  **zero** uses in the 8 modules.
* `Opt_DroneOverhaul` has **no probe** in the TestKit (`91_Stress.lua` is its
  only harness). Pre-existing gap; not the split's doing.
* The `OptionsMenu` probe asserts **6** toggles; there are **7** (`NoHomeless`
  missing from its `WANT`, `60_Probes_Opt.lua:879-880`).
* `doccheck.py:475` hard-codes `default_active = modules - 7`; after the split
  that reports **67** instead of 74 on the fix-pack side. ⚠️ And the obvious
  generalisation is a trap I walked into and backed out of: `counts["optional"]`
  is a substring count (`:472`) reporting **8**, because
  `Opt_DroneStatDials.lua:56` says the words *inside a comment*. The real
  def-field count is **7**. §5.3 names two more tooling defects the port must
  fix.
* `docs/README.md`'s prose counts (116 entries / 43 facts / 151 rows) are stale;
  the real ones are 125 / 53 / 160.

### Persisted names — my inventory, for you to reproduce independently

Five, and **no rename exists in any era** (`git log --all -p` over
`Code/Opt_*.lua` returns exactly seven `SMRFixPack_*` identifiers ever, five
persisted + the two runtime config globals; the mod id, the 9 option keys and
the 8 `Register` ids have never had another value):
`SMRFixPack_ack_notworking` · `SMRFixPack_closed_to_new_residents` ·
`SMRFixPack_no_homeless` · `SMRFixPack_DroneSpeedDial` ·
`SMRFixPack_DroneCarryDial`, plus the dial VALUE strings in three places each.
The SaveSanitizer question is answered NO with two independent reasons
(§1.4). **A name I missed is a REJECT — hunt for one in the UI rows'
`rawset`, in `TogglePolicy`/`SetPolicyState`'s writes, and in anything
`Opt_MultipleSuns` leaves on a `SolarPanelBase`.**
