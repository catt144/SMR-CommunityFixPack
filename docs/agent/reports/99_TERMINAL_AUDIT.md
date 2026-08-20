# Terminal audit — the chain's backward QA (2026-08-19)

Brief: `99_TERMINAL_AUDIT_fable.md` (self-consumed in this commit; this file is
its grave-side record). Spec: `00_CHAIN_SPEC.md`. Config at audit time: fix pack
+ TestKit ticked, opt-in off (run-A shape); tree at `91a444b`; doccheck GREEN;
`upload_preflight` 20 checked / 0 FAIL; TEMPORARY sweep 0 hits.

⭐ **Part A ran as the owner-designed fan-out** (spec `28f90a4`, brief §2): ten
independent verifier sessions, one per link plus one for the chain's own
corrections and one for the run-B evidence, each instructed to REFUTE rather
than confirm, to default to *refuted* when uncertain, and to re-derive every
route at Src without opening the report that produced the finding. Their raw
reports are the provenance for every verdict below; each row names its verifier
evidence inline.

---

## 1 · Part A — every link's findings, adversarially re-verified

Verdict words: **HOLDS** (route re-derived independently, same conclusion) ·
**REFUTED** (conclusion wrong; what is actually true is stated) · **NARROWED**
(substance holds, a stated clause does not).

### Link 1 — L1 structure & collision

| finding | verdict |
|---|---|
| L1-F1 double-wrap order + doccheck guard | **HOLDS**, every step: list order = install order (`Mod.lua:498-517`, `ipairs(self.code)`); ArrivalDeaths outer and always-delegating (`:200` single exit); ShelterReflex's `SetCommand("Rest")` kills the thread (`CommandObject.lua:372`); the guard detects a swap, correct direction, hook blocks |
| L1-F2 IsSuitable misses NaturalHabitatBase/NaturalistHabitat | **HOLDS** (declare-wins at `classes.lua:609`; cited :608 is one-line drift) |
| L1-F3 F66 reclaim never runs when a Station dies | ⛔ **REFUTED.** `Done` is a **CombineMethods** entry — `DefineCombinedMethod("Done", "procall_parents_last", ...)` at `PropertyObject.lua:1664`, generated in `OnMsg.ClassesPreprocess` (`classes.lua:1602-1676`) from the classdefs, which at that point already hold our wrapper (mod load precedes `Msg("Autorun")`, `lib.lua:370-371`). Station's own `Done` and our wrapped `TrackConnectedObjBase:Done` **both** run, each in its own procall. The recorded coverage gap is phantom — link 1 checked `AutoResolveMethods` (58 members) and never the second combining registry. Error in the mod's favor; no shipped code was ever changed over it |
| L1-F4 OnMsg additive, store not FirstLoad-preserved | **HOLDS** (`cthreads.lua:7` outside the FirstLoad block) |
| refuted-list spot-checks (RCTransport overrides; 16 globals/16 symbols) | **HOLD** (nuance: `RCTerraformer:InteractWithObject` is a plain double-call, not a tail call — coverage conclusion unaffected) |

### Link 2 — L2 lifecycle & idempotency

| finding | verdict |
|---|---|
| L2-F1 reload false-inactive + `data_edited` fix | **HOLDS**, strongest verification in the set: sim control 5/5 verbatim, pre-fix 4/4 repro (verifier re-ran `git show 2f077e8:` source), post-fix 0/4, negative control clean; archive delta re-derived in both two-load logs; memo is process-scoped (not persisted — `SMRFixPack` registers no GameVar); a real patch between loads cannot be masked (`LoadData` never re-runs in-process; target-loss latches sit before the ever_changed branch). ⚠️ Instrument caveat: `l2_reload_sim.py` exits 0 even when latches reproduce — regression use needs `--expect-clean-second-load` |
| cross-fix thrash check (the design's accepted risk) | **CLEAN** — the L2 fix and both `2f077e8` fixes compose; walked, not asserted |
| L2-F2 thread-per-reload | **HOLDS** (bound verified: silent exit at 0 suspects) |
| L2-F3 surviving closure | **HOLDS** (upvalue inventory re-derived) |
| L2-F5 false suite FAILs on a reloaded session | **NARROWED — undercount:** the true prediction is **3**, not 2; the IndependenceTerraforming probe also routes a status check (`40_Probes_Wave4.lua:981-1014` → `"fix not active"` verdict) |
| L2-F6 nothing wraps its own wrapper | **HOLDS** (3 of 13 globals spot-checked at Src declarations; classes.lua mechanics re-derived) |

### Link 3 — L3 save & exit

| finding | verdict |
|---|---|
| L3-F1 `smr_shuttles` convention breach | **HOLDS**, incl. the inert-after-uninstall bound (`table.unpack` array-part-only; `pairs` loops touch only `elevator_validation`); a 4th cache-drop route exists (elevator-validation reset, `Colonist.lua:2526-2527`) — omission, not error |
| L3-F2 exit law | **law HOLDS** (re-derived at `persist.lua:119-143`); ⛔ the charge that `Fix_MeteorFrequency:36-37` "states it backwards" is **REFUTED** — the comment describes the save the player already holds, and for that save it is correct; at worst it omits drop-on-resave. Link 3 overstated |
| L3-F3 reinstall re-roll | **HOLDS** (with the load-bearing precondition made explicit: a save must be written while uninstalled) |
| L3-F4 F48 flag set before the pass | **HOLDS** (UIColony is a vanilla GameVar ⇒ the premature flag persists and survives uninstall; console repair path deliberately ignores the flag — a mitigant on record) |
| L3-F5 stale scoping header | **HOLDS** (17 modules re-counted by name, F39 nonexistent, F58 is NewDay) |

### Link 4 — L4 player experience

| finding | verdict |
|---|---|
| L4-F1 dialog prints ids, ignores 75 titles | **HOLDS** (75/75 titles re-counted) |
| L4-F2 `error` status blamed on a game update | **HOLDS**; the sweep's *"never evidence of a game update"* is over-absolute (an apply CAN throw because of an update) — the defect stands on "not established evidence", which the dialog asserts anyway |
| L4-F3 `ctx.heal()` silent | **HOLDS**; archive recount 60-of-61 pack-tag logs carry the false-inactive line (sweep said 56/57 — off by one at sweep time under the natural definition; shape exactly right) |
| no benign wording fires the dialog | **SURVIVES** attack (all four substrings grepped across Code/; every carrier is a genuine failure string). ⭐ NEW adjacent latent found by the verifier: a **non-benign latch followed directly by a benign latch** (no intervening heal) leaves `update_suspect` set on a benign-detail entry — same mark-outlives-verdict class as `2f077e8`. Speculative reachability; queued (item 53) |
| `update report:` 0 occurrences | **HOLDS** (0 in all 74) |

### Link 5 — L5 failure & containment

| finding | verdict |
|---|---|
| L5-F1 `OnDataReady` swallows | **NARROWED:** mechanism holds, but the exposed-consumer list is wrong — `Fix_TechDescriptionBuilding`'s one call site pcalls its own work (`:86`); the genuinely exposed consumer is **one** (`Fix_FirstAsteroidPrefabs:237`), not three. Whether the C-side procall logs is not Lua-derivable (disclosed) |
| L5-F2 unguarded `SMRFixPack_Disabled[id]` at Register | **HOLDS** (whole-tree read census: exactly 2 unguarded / 4 guarded sites) |
| L5-F3 three unguarded sweeps | **HOLDS — and ⛔ the AUDIT BRIEF's queue note is REFUTED on it.** The act-1 `AllMapsForEach true 2085` measurement discharges `Fix_SaintBlessing:151` and `Fix_TrackSalvageWipe:304` (all their work is inside MapForEach callbacks) and says **nothing** about `Fix_StaleReservations:61`, which is a **plain-Lua `ipairs` sweep on `OnMsg.NewDay`** (not load-time — the finding's own label was also wrong). A mid-loop throw abandons the remainder every sol with no log and status still `active`. **Reopened; queued (item 53)** |
| L5-F5 mid-session veto gap | **HOLDS** (all four sites re-read) |
| L5-C1 vanilla `old_threads` candidate | **NARROWED:** the error, the GameVar, the upvalue and the single caller all hold; the **teardown-window trigger story is refuted** — `_fixup.lua:11-17` makes the DelayedCall thread map-owned, and `DoneGame` unloads maps (`Game.lua:46`) *before* the GameVar flips (`:51`), so the ordinary teardown cannot produce it. The one observed throw is real; its mechanism is open. Filed as C53 with exactly that status |
| EF-065 | **(a) HOLDS** Lua-side; **(b) REFUTED in part:** the LoadCode error box is **dead code on this title** (display gated on `ModsPreGameMenuOpen`, never set, or `Msg("PreGameMenuOpen")`, never raised) ⇒ a file-scope throw is **log-only and the player sees nothing**. Fact amended. This also corrects L8-F1's clause "the engine is loud" — the engine is loud in the log, silent on screen |

### Link 6 — L6 promise vs behaviour

| finding | verdict |
|---|---|
| L6-F1 items.lua missing module (launch-blocking, fixed `36d8817`) | **HOLDS end to end**; the launch-blocking call was **correct** by the spec's definition, and understated — the Paradox post-upload save (`ParadoxMods.lua:173`) would have propagated the 75-entry list to every later upload on both portals. Fix verified by three independent derivations (stored CodeFileName, name-derived filename per `ModItem.lua:164-168` — the invariant the game actually uses, which the sweep never checked — and disk), 76/76 ordered-equal |
| L6-F2 preflight guard rebuilt | **HOLDS**; two residual holes recorded, both currently benign: the parser is Lua-comment-blind (a fully commented-out entry still counts), and it compares stored `CodeFileName` strings while `UpdateCode` derives from `name` — recorded as post-launch guard work (item 53) |
| L6-F3 README veto snippet asserts | **HOLDS** (assert at `:1554`, not :1553 — drift; asymmetry vs `__newindex`'s `Loading` guard real) |
| L6-F5 F98 retail no-op | **HOLDS and worse:** even past its guard, the replacement `T(TRANSLATION_ID, ...)` re-resolves to the TranslationTable in retail — the module can only ever work in dev builds, structurally |
| L6-F6/F7 veto limits, ordering wording | **HOLD** (two of the "6 of 7" handlers check nothing at all — slight overstatement, operative claim intact) |

### Link 7 — L7 environment & namespace

All findings **HOLD**; instrument control battery re-run, 23/23. Mode-line
recount now 69 unpacked + 1 packed (run B) + 7 sessions with no fix-pack mode
line — see §4 note on the "66/66" figure. Tie-break re-derived in both
encounter orders (unpacked wins at equal version either way). Blacklist count
explained exactly (151 keys − 2 false-valued = 149 truthy). TestKit
disjointness spot-checks clean in both directions. `content_path`
configuration-invariance re-derived (`Mod.lua:1755-1758`); EF-065 now carries it.

### Link 8 — L8 adversarial / hostile modder

| finding | verdict |
|---|---|
| L8-F1 `SMRFixPack_Disabled = true` loses 75/75, silently | **HOLDS** (harness re-run: controls pass, hostile rows reproduce; per-file pcall walked at `lib.lua:242-251`), with one precision fix: Register **stores the entry before throwing** (`:440-443` precede `:446`), so all 75 ids sit `pending` — present, dead, and invisible to `UpdateSuspects`. Strengthened by the EF-065 correction: the engine's collected load errors are also **never shown** on this title — the loss would be fully silent on screen |
| L8-F2 refill defends the wrong two sub-tables | **HOLDS** (all three harness rows reproduce) |
| L8-F3 string/list veto values silently no-op | **HOLDS** (string metatable indexing non-throwing; both rows in harness) |
| L8-F4 deference census: 24/66 full replacements | ⛔ **REFUTED as stated.** `l8_deference_map.py` misses captures written as a **plain environment read** (`local orig = Name`) while catching `rawget` and method-table captures; ≥4 of the 11 global "REPLACES" rows actually chain (`Fix_GeneForging:53`, `Fix_AnomalyCaveInMap:67`, `Fix_ShuttleHubOffAvailable:66`, `Fix_TrainMinors:90`); true global replacements ≈ 7/16, and the tool today prints 67 sites vs the recorded 66. Its selftest (11/11) lacks the missed pattern — a fourth self-flattering instrument for this chain's collection. ⛔ **The census may not be cited in any decision** until the tool is repaired and every REPLACES row hand-read. The direction of the finding survives weakened: genuine full replacements exist (`Fix_TouristApplicants:23` confirmed), §1.5's "keep the list short" still has no trustworthy number |
| L8-F5 DustDevil re-install clobbers a foreign patch at DataLoaded | **HOLDS** (cold-boot trace verified: `set_installed(true)` runs on every completed DataLoaded pass; DescrMap variant is worse — a body copy). Boundary noted: a foreign replacement made *after* DataLoaded survives until the next DataChanged |
| L8-F6 both blame surfaces point at us | **HOLDS** (counts imprecise: ~234 shape entries, 6 real `test=` checks in 5 files — the recorded 238/7 don't survive recount; substance intact) |
| EF-058 amendment | **HOLDS** (`Msg("Autorun")` raised at exactly one site, `lib.lua:371`, after `autorun.lua` completes) |

### The chain's own corrections (the two known-wrong ones had successors — audited too)

| correction | verdict |
|---|---|
| Console story (LR-F15) | **Operational conclusion HOLDS; recorded mechanism INVERTED — and now solved.** The retail console evaluates against `g_ConsoleFENV`, which on retail (`config.Mods` branch, `console.lua:45-56`) is a `LuaModEnv` whose `__index` applies **`ModEnvBlacklist`** — the retail console **is** blacklist-governed, the exact inverse of the recorded *"the blacklist only ever explained mod code, never the console."* Both functions ship gated true in the retail `Lua.fpk` (extracted; `console.lua` hash-identical to Src; `config.Mods = true` unconditional); "nil in `_G` at the console" conflated the console's environment with `_G`. The Ged route stands on measurement AND mechanism now. Re-recorded here before it seeds a third wrong correction |
| EF-055 narrowing (LR-F19) | **HOLDS** as an operational rule; ⚠️ bundled variable disclosed (same-id and no-launch-while-absent coincide in every experiment); the fact FILE had not been amended (only STATE carried it) — **amended this session** |
| Criterion-3 recount (`2afe502`) | **HOLDS** — re-counted: 73 logs at correction time = 21 with `[LUA ERROR]` / 52 without, exactly as corrected; current corpus 74 = 21/53 (run B adds a zero-error log) |
| v1.00-000 format (LR-F8, `b895eb0`) | **HOLDS** at Src `:1176-1178`, in the run-B log, and in the Mods Manager render route (`ModManager.lua:1386`) |
| Act-1 step-1 inversion (`e69a006`) | **HOLDS** — checklist now expects `0 false` with the reasoning attached |
| Act-2 TestKit untick (`b895eb0`) | **HOLDS** — item 52 act 2 step 1 now names the untick, the leave-off, and the restart unambiguously |

## 2 · Part B — hostile re-read of the `2f077e8` core fixes

**B1 (`update_suspect` clear).** The brief's sinking question — does clearing
on success hide genuine patch rot? — answers **no, constructively**: rot
manifests in the next process as a failed shape check (mark set + `inactive`,
suspect), a non-benign latch (sets its own mark, `:277`), or `error` status
(unconditionally suspect). Success never occurs in the rot scenario, so the
clear removes only the false positive. `nil` vs `false` immaterial at the
truthiness read (`:531`); empty `detail` cannot trip the substring fallback
(inactive-only). ⛔ **A third site exists:** `OnMsg.ApplyModOptions`'s
re-activation path (`00_Core.lua:481-483`) restores `active` without clearing
the mark. Latent — requires `def.optional`, and 0 optional modules ship —
queued (item 53). The fan-out added a fourth sibling: benign-latch-after-
non-benign-latch never clears (L4 verifier). Both are the same class the
2026-08-17 fix repaired at two sites; the class outlived the fix at two more.

**B2 (`order` guard).** The planted criticism is real and bounded: a genuine
cross-module id collision is now quieter (one `order` entry, silent overwrite
of `fixes[id]`/`defs[id]`). Reload vs collision cannot be distinguished by
table identity (defs are rebuilt per load); a `title` comparison could log the
cross-module case without reload noise. Third-party-gated (our 75 ids are
unique and doccheck-counted) — queued as a candidate log line, not fixed.
`fixes[id]` **can** be pre-set by a foreign partial-`SMRFixPack` (L8-F2's
shape), which makes `reregistered` read true and silently drops the module
from `order` — recorded as part of the same queue family.

**B3 (the rest of the pre-chain work).**

| claim | verdict |
|---|---|
| `image` resolves packed | **PROVEN ATTENDED** — run B c7, preview rendered on the first-ever packed load; `content_path` invariance closes the mechanism |
| Paradox before Steam | **HOLDS**, re-derived (`SteamWorkshop.lua:17-22` saves before packing; `ParadoxMods.lua:167-173` after; `ValidateModBeforeUpload` forces the save on dirty) |
| every editor save bumps `version` | **HOLDS** (`SaveDef` `:960-994`, `+1` at `:967`; metadata holds `0/1/0`) |
| the package is 80 files | **HOLDS, re-measured**: `ModContent.fpk` 362,894 B, md5 `8dcb0692…`, 80 entries, **80/80 byte-identical to the tree at `91a444b`**, 0 missing / 0 extra |
| update report never fired | **HOLDS**: 0 occurrences in all 74 archived logs |

## 3 · Part C — the audit's own sweep

### 3a · Preset-FIELD patches — the surface three lenses named and none swept

New instrument `tools/audit_preset_fields.py` — container roster derived from
Src at runtime (121 `GlobalMap` names + `Presets`), alias- and loop-variable-
tracked, selftest 8/8. ⚠️ Own-instrument defect found and fixed before any
count: the first version was blind to the pack's dominant
`local x = rawget(_G, "Container")` idiom and printed **0 rows with a passing
selftest** — the selftest now covers the idiom. Disclosed limits kept:
call-site dataflow (function params) and container-through-table-field are not
tracked; the census is a lower bound, same soundness direction as the L8 tool.

**Result: 9 preset-field writes across 6 modules** (AstrogeologistExtractors
:137 append · DustSicknessDamage :60 `daily_update_func` ·
IndependenceTerraforming :84 `Amount` · LastTransmissionStorage :122/:123/:130/
:134 · SaintBlessing :103 `modify_trait` · TechDescriptionBuilding :75
`description`). The three questions the lenses owed:

1. **Collisions (L1's non-mechanical claim): zero.** No field name is written
   by two modules; the one shared preset GROUP (DustDevils) is written by
   neither of its two readers. L1's hand-read claim is now extractor-backed.
2. **Dead targets (L6's gap): zero foreign fields.** Every written field name
   occurs in the shipped Src tree; per-row: `description` is the known F98
   retail no-op (already recorded — the write never executes in retail), the
   other eight are fields vanilla reads on live paths, each covered by its
   module's own falsifier history.
3. **Foreign contention (L8's gap):** the pack invents **no key** on any
   preset, so a foreign mod walking presets sees only vanilla-shaped fields
   with corrected values — value-level contention identical to any data mod,
   no new crash surface. (The one mod-invented persisted key anywhere remains
   L3-F1's `smr_shuttles`, on a cache table, not a preset.)

Divergence noted, not resolved: L2's ledger row says "9 in-place preset edits
in **7** modules"; the census reads 9 writes in **6** — definition drift
(L2's category vs container-rooted writes), no verdict rests on it.

### 3b · The question none of the eight lenses asked

**What happens on a game build other than the pinned one?** Nobody asked, and
the answer has three parts, all re-derived at Src this session:

* `metadata.lua` declares `lua_revision = 350453`; the engine's floor
  (`ModMinLuaRevision`, `Mod.lua:15`) is **the same number** on this build, so
  on the pinned build the pack is neither too old nor too new.
* On an **older** build (GOG/Epic behind, rolled-back installs):
  `ModDef:IsTooNew()` exists (`:905`) but the **load path never calls it** —
  only the Mod-Manager UI does, and its branch merely warns
  *"Check for a game update!"* (`ModManager.lua:224`) without blocking. ⇒ an
  older-build player **loads the pack ungated by the engine**, protected only
  by our ~234 shape checks, which were derived against 1.0.7.396349 alone. A
  symbol that exists on the old build with different internals applies a
  pinned body to a build it was never derived against — the exact blind spot
  the C1 dialog's honesty-limit comment already concedes in-process.
  Reachability low (Steam auto-updates; final SM patch is years old) but real.
* The in-game browser's *"only compatible"* filter (`ModsUIIsModCompatible`,
  `ModManager.lua:230-234`) keys on a **portal-side `RequiredGameVersion`**
  that the upload code never sends — absent ⇒ the pack counts *incompatible*
  and is hidden for any player who enables that filter (default off,
  `:908`). ⇒ **check-at-upload item**: after the Paradox upload, verify the
  portal listing carries a RequiredGameVersion (portal web field), else set it
  there. Routed to `RELEASE_PORTAL_PREP.md` §0.5.

### 3c · Corrections to the audit's own evidence base

* **"66 of 66 archived say unpacked"** (STATE, gate criterion 1's witness): my
  fan-out's precise recount over the same corpus reads **69 unpacked + 7
  sessions with no fix-pack mode line** (+ run B's 1 packed). The 66 figure
  under-counted the corpus; the operative fact — *zero* packed loads before
  run B in the archive — survives unchanged.
* **"First packed load ever"** (run B c1): refuted in the strict sense — the
  unarchived same-day setup log (`17.11.44`, now archived as `runBprep_*`)
  loaded packed nine minutes earlier, cleanly (150 applied, TestKit still on,
  0 errors). Run B is the first packed load **in the B configuration**, which
  is what the gate means; the wording is amended here.
* **LR-F12's log absorption**: done this session — `sit0817_*` (4 files; LR-F12
  named 7, the other 3 had already rotated out of the live logs dir and are
  gone), `runBprep_*` (the 17:11 packed setup leg), `runBc9_*` (criterion 9's
  own log, which was scored but never archived). Corpus now 80 logs.
* **STATE's "all three mods unticked" was stale** — a 21:23 live log shows fix
  pack + TestKit re-ticked and loading unpacked (junction restored). STATE
  updated to the observed rig state.
* The `Welcome to Mars` popup (run B c5) has **no log line at all** — that
  criterion half rests wholly on the owner's attended word, stated as such in
  §5. The missing-or-outdated dialog's TestKit-only listing (it names neither
  of the other two equally not-loaded mods) is recorded as consistent-but-
  unexplained; no criterion rests on it.

## 4 · Part D — the convergence ruling

⛔ **The chain stopped on clause 3 — the hard cap. That is not convergence,
and this report will not launder it into one.** Eight links exhausted the lens
pool; link 8's own §9 said unswept territory of consequence remained, and it
was right. Since then, two of its named items closed — **run B/packed** (the
gate ran, 10/10, re-verified here) and **preset-field patches** (§3a, swept
clean) — and **warm-save round trip + uninstall-of-75** closed inside run B's
c8/c9. What remains unreached, named per §8's obligation:

* **console platforms** — no Xbox/PlayStation/MS Store run, ever; the C1
  dialog is the pack's only surface there and it has never been seen anywhere;
* **non-English** — no localized run; the two re-used translation ids are
  source-verified only;
* **foreign-mod interleaving** — every L8 verdict is source-derived or
  simulated by design (standing no-third-party-mod policy); the one available
  observation (opt-in both-packs leg, H-08 ask) remains on the checklist;
* **the TestKit's own containment and second-load behaviour** — swept for
  namespace only, in eight links; it ships to nobody, but every gate number
  depends on it;
* **the 53 method wrappers' callers, per-site** — answered structurally, never
  per caller;
* **`Fix_StaleReservations`' per-item guard** — reopened by this audit (§1
  L5-F3): the one queue item that was wrongly marked discharged;
* **long-session / performance behaviour** — apply cost is measured (≈0.57 s),
  a colony's steady-state cost is not.

Clause 1 is unavailable while that list is non-empty. Clause 2 never fired
(no two consecutive cosmetic-only links). **Ruling: clause 3 — we stopped
counting, not because there was nothing left** — with the honest rider that
the two largest named items were closed after the cap by the gate and by this
audit, and that nothing in the remainder is reachable by a player running this
pack alone on the pinned build in English on PC, which is the configuration
1.0.0 ships into.

## 5 · The verdict, and what it rests on

**Upload it.** The tree run B validated is fit to ship as it stands:

* the gate ran in the player's configuration — packed, TestKit off, opt-in
  off — and scored 10/10; this audit re-verified every log-decidable criterion
  from primary evidence (`runB_*`, `runBc9_*` logs) and re-did the
  packed-vs-unpacked name comparison in python (75/75 set-identical, both
  directions);
* criteria 5 and 7, and the visual halves of 8 and 9, rest on the owner's
  attended word — named plainly, per the sign-off rule; everything else stands
  on logs this repo now archives;
* both `2f077e8` core fixes are **proven in a running game** (act 1 attended:
  `update_suspect` read `nil`; `#order` read 75 after a real reload), not
  merely not-falsified;
* every code defect the chain recorded and this audit verified is gated behind
  a hostile third party absent from the shipping configuration, and the
  whether-to-apply decision is the owner's (checklist 53, §6 below);
* the packed artifact on disk reconciles 80/80 by content against the tree the
  release tag now marks.

⛔ Not claimed: that the mod is *clean* (see §4's unreached list); that it is
compatible with other mods (run A tested exactly one other mod, ours, and run
B tested none); any count not re-emitted this session.

**The tag.** `fixpack-v1.0.0` moves to the close-out commit. Argument, stated
per §9: the shipped surface (`Code/` 76 files, `metadata.lua`, `items.lua`,
`LICENSE`, `preview.png`) is byte-identical between `91a444b` — the tree the
verified `.fpk` reconciles 80/80 against — and the close-out commit, whose
diff is entirely `docs/` and `tools/`, both excluded by `ignore_files`
(measured by the seed's real `.fpk` listing at zero files each). The tag marks
what actually gets packed.

## 6 · The queue, corrected (input to checklist 53)

All items remain **third-party-gated except none** — no player running the
pack alone reaches any of them. The fan-out corrected the repair shapes:

1. `Register:446` + `OptionEnabled:55` veto-table guards — ⛔ a plain
   `type(x)=="table"` guard does **not** close the measured throwing-`__index`
   case (a hostile table passes the type check and the plain index still fires
   the metamethod); the closing form is `rawget(disabled, id)` after the type
   check. The same latent pattern exists at the four "correct" sites.
2. `SMRFixPack` adoption at `:17` — the `:24-25` refill cannot save
   `SMRFixPack = true` (dies at `:24` first); the closing form type-normalises
   at `:17` (`type(x)=="table" and x or {…}`) plus `or {}` refills for
   `fixes`/`order`. Verifier confirmed the guards are behavior-neutral in the
   shipping configuration.
3. `Fix_StaleReservations:61` per-item pcall — **reopened** (§1 L5-F3); the
   pack's own donor shape exists (`Fix_TrainMinors:141`).
4. `OnDataReady` pcall — one exposed consumer (`Fix_FirstAsteroidPrefabs:237`).
5. `ctx.heal()` log line (L4-F3) + the two silent heal sites.
6. Mark-clear completeness: `ApplyModOptions:481-483` (B2's third site) and
   benign-latch-after-non-benign-latch (L4 verifier's fourth) — both latent.
7. Register re-registration log on title mismatch (B2) — candidate only.
8. DustDevil/DescrMap re-install politeness (L8-F5) — behaviour change to a
   working module; weakest expected value on the list.
9. NOT on the queue: anything citing the deference census (L8-F4 refuted);
   the three SetGlobal-bypass sites (L7-F3 — failure mode excluded by the
   blacklist cross, policy-consistency only).

**Recommendation to the owner: apply nothing before 1.0.0; ship the validated
tree; take items 1-6 as a single 1.0.1 hardening pass verified by one
unattended run A, using §5a's carry-over argument** (run B proved packed ≡
unpacked at module level; none of these edits touches the packaging surface,
so a future run A verifies them for the packed case too — re-check that clause
per change at apply time). The owner's *"clean period"* ruling was about a
defect players would see; every queue item needs a hostile third party the
shipping configuration does not contain. Options and the ruling stay the
owner's: checklist 53.

## 7 · Was the chain worth its cost? (the owner asked for a verdict, not a compliment)

**Yes for this release, with two design lessons proven by its own record.**
The chain found one genuine launch-blocker (L6-F1 — a fix silently missing
from every Steam install; nothing else would have caught it before upload),
built the gate that then failed honestly twice (criteria 1 and 3 were
unfalsifiable/unsatisfiable until links 5 and 7 repaired them), and produced
the coverage ledger without which this audit could not have ruled on
convergence at all. Against that: eight links produced **zero player-reachable
code defects in the shipped tree** — the pack was already clean at that bar
when the chain started — and the chain's most expensive failures were its own:
two wrong corrections cost two owner launches (the console conflation, now
mechanistically solved) and a gate script that omitted its own defining untick.
The fan-out audit earned its cost concretely: three findings refuted (L1-F3,
L3-F2's charge, L8-F4's census), one queue item wrongly marked discharged
reopened, and a fourth self-flattering instrument caught. Lesson 1: the lens
rotation converges, but **corrections need the same adversarial treatment as
findings** — this chain's error rate lived in its corrections, not its sweeps.
Lesson 2: **instruments lie green** — four of them here; every future census
needs a control that can fail, and "0 rows + passing selftest" is a fire
alarm. For a future effort of this size: keep the sequential sweep + terminal
fan-out shape (CHAIN_METHOD 5a), and add a standing rule that any session
correcting a prior session's claim must show the mechanism, not just the
measurement.
