# GAME_PATCH_INSTRUMENTS — the surface sweep, its instruments, and the 1.0.7 → 1.1.0 backtest

**2026-09-18, firing `prompts/GAME_PATCH_INSTRUMENTS_high.md` (grave: this commit).** Started at `ba838b9`;
a sibling landed `6f421fd` mid-session (owner ruling: the perma prompt **runs in the fix pack first,
always** — at patch time players cannot switch off individual fix modules — and opt-in findings go to
an outbox in the fork, §5 step 8) and `a92cc62` (SMRTK.md only); both folded in. `git diff --stat
c823e5b..HEAD -- docs/agent/WORKFLOW.md docs/agent/reports/ tools/` empty, so the brief's facts held.
Desk only: no game launched, no `Code/`, TestKit or perma prompt written. Trees:
`C:\Dev\SMR-SrcArchive\1.0.7.396349\Src` (manifest digest `09d95e3448573dc3…`) and
`…\1.1.0.403908\Src` (`a4577da25cb3fe85…`), the pair `reports/vanillahunt/CALLERS.tsv` line 1 names.
Executed model: Claude Fable 5.1 (`claude-fable-5-1`); two read-only survey subagents, same model.

> ⚖️ **Headline.** The sweep that makes the none/scoped/full call is one desk command over the two
> archived trees plus the module text, no header stamps needed: hash **everything a module names**
> one hop out (its pinned body, its `Require` targets, the functions and data files its header cites,
> and the signature of every call it makes). Backtested on the 80-module pre-patch pack against the
> 1.1.0 re-verification's verdicts, that union flags **10/10 FIX, 34/35 REMOVE, 32/35 KEEP** — which
> is the correct answer for 1.1.0: 76 of 80 modules moved, verdict **full**. The same union on a
> synthetic one-file patch flags **2 of 80** (one of them the real F-2), verdict **scoped**. The
> bodycheck-shaped check on the pinned body alone sees **6/10 FIX and none of the four class-c rows**;
> the four are caught by the *`Require` targets*, not by adjacency. Adjacency (callers/callees) was
> measured and is cut. The one instrument that would have found F117 on 09-08 instead of by hand on
> 09-09 — a signature check over every call a module makes — runs in a second and is not built.

## 0 · Two claims in the brief that did not survive re-derivation

1. **"6 of the 10 FIX rows were class c"** (`WORKFLOW.md:97-98`, `tools/bodycheck.py:94-95`, the brief).
   `PACK_1_1_0_REVERIFICATION.md:307` lists class (c) as *F111, F112, F-1, F-2, F-3, F-5*: six instances,
   of which **four** are FIX rows (F111 and F112 are R-24 and R-4). By module header, the ten FIX rows are
   six full-body copies (F-3a, F-6, F-7, F-8, F-9, F-10), two data patches (F-1, F-5), one wrapper
   (F-2) and one additive load sweep (F-4). The defensible sentence is "six class-c instances in the
   1.1.0 response, four of them FIX rows". Out-of-scope finding; not edited here.
2. **"Adjacency is the class-c proxy."** Measured below: CALLER flags 10/10 FIX but also 30/35 KEEP on
   1.1.0 and 10 of 80 modules on the one-file control; CALLEE flags 3/10 FIX. Both are dominated by
   the `Require`-target hash. Cut.

## 1 · The instrument set, ranked by value per cost

Per-patch cost is **runtime + tokens to read the output + owner minutes**. Build costs are estimates
from the scratch prototypes (§7). "Opt-in" = serves `C:\Dev\SMR-OptInPack` (6 modules, same
`Register/Require/DataPatch/SetGlobal` API, **zero** `SRC:` lines, no bodycheck in its tools).

| # | instrument | where | catches (class) | build | per patch | opt-in | evidence |
|---|---|---|---|---|---|---|---|
| D1 | **One-hop dependency hash, archive-as-manifest.** For each module, harvest from its text: pinned bodies (indented `function C:M(` inside `apply`, `C.M = function`, `local o = C.M`, `SetGlobal("X")`, local class aliases resolved), `Require` `{class,method}`/`{global}` targets, every `path:line` citation (mapped to its enclosing declaration; `Data/` and generated cites to the file), and hash each in the archived pinned tree vs the live tree with `luafn.find_bodies`. Statuses: identical / body / body+sig / removed / **moved** / moved+body (a move is not "gone" — the R-15 trap). | desk | a, b, d, e, f, and **c one hop out** (measured 4/4 on the answer key) | ~300 lines; the prototype is `backtest.py` §7, reusing `luafn`, `treediff.declarations`, `sigcheck.params` | 46 s cold / 35 s cached; ~3k tokens to read; **0 owner min** | **yes**, with no stamping | §3 tables |
| D2 | **Signature of every call.** Every bare call name in the module vs the parameter lists of every declaration of that name in hand files; flag when no old signature survives. Rank *incompatible* (a leading parameter renamed/reordered — the F117 shape, `traits→colonist`) above *prefix-compatible* (a trailing optional added or dropped: `PlaceResourceStockpile_Delayed(+tall_piles)`, `ValidateBuilding(−for_story_bits)`, both benign). | desk | a′ (callee contract moved, our call text did not) | ~60 lines on `sigcheck.py` | seconds; 14 rows on 1.1.0 | yes | 3/10 FIX, 7/35 REMOVE, 4/35 KEEP — one of the four KEEP hits is **F117** (`ArrivalDeaths`, `ChooseDome`), found by hand a day later (`HOTFIX_2_AUDIT.md`) |
| D3 | **W42 save-exposure re-check** = D2 restricted to the D13 capturable-code sites (`D13_EXPOSED_SET.md` §2a, E1–E12) : a frozen closure in an old save calls the old contract. | desk | the save half of a′ | ~20 lines (a site list) | seconds | yes (E-sites include `Opt_` rows) | on the pre-patch pack: `ArrivalDeaths` (F117) and `ShelterReflex` (`GetScoreFor`, = F-3); nothing else |
| D4 | **Triage runner** that emits the whole surface sweep in one block: build id from the `.acf`, archive status (`EF-075`), fpk parity (`flpk_extract` + byte diff, `EF-085`), tree size (changed hand declarations), D1/D2/D3 tables, the fact list (D5), base-class structure changes (`DefineClass`/`__parents` lines changed in any file a module pins or cites — the seven `VANILLA_DIFF_DISPOSITION.md:118-134` found), and the §2 verdict. No count typed by hand. | desk | — (the surface) | ~150 lines around D1–D3, D5 | < 2 min; **~5k tokens**; 0 owner min | yes | — |
| D5 | **Fact-level re-derive list.** Each `facts/*.md` citation mapped to its function; flag the facts whose cited function moved. Finer than `--emit-fingerprint`, which moves a whole build group. | desk | stale facts | ~50 lines (`facts_cite.py` §7) | 20 s; a list | n/a | 61 of the 107 fact files carry a resolvable game citation; 42 of those cite a function that moved on 1.0.7→1.1.0 |
| G1 | **Boot census** (exists). Boot to the main menu with pack + kit; `logscan.py` reads applied / inactive / heal-with-count / `behaviour probe declined` per module. Unattended via `-smrautorun`. | in game | e at runtime; c on the 15 modules with a behaviour probe; data-patch heals carry counts (F-5's `added 2 missing` was in `gated110_*.log:181`) | 0 | **~3 owner min** attended, 0 unattended; ~2k tokens | yes | the 1.1.0 record |
| G2 | **Wiring and reach sweep** (exists: `DispatchReach`, `64_Probes_Wave14.lua:233`): every `{class,method}` target on every descendant, chain-vs-copy, multi-parent paths. Its `DISPATCH_TARGETS` is hand-kept → regenerate from `harvest_wrap_targets.py --lua` in the sweep. The desk half (REDECL: a new 1.1.0 declaration carrying a pin's method name on another class) is a D1 column. | in game | the EF-058/EF-066 reach traps | 0 (+ manifest regen) | inside G1's boot; 0 extra | yes | EF-066: 105 targets, 97 reach all descendants |
| G3 | **Suite A/B, unattended** (exists: `95_AutoRun.lua`: boot → new colony → `RunAll` → quit, twice). PASS/FAIL/ERROR diff vs the pre-patch run. An ERROR is usually the probe's stub meeting a changed body — noisy, but a class-c signal. | in game | c where a probe computes its expectation independently; probe rot | 0 | **~2 owner min** to launch + ~10 machine min; ~3k tokens | yes (one kit, three mods) | **recall on the answer key UNMEASURED** — the only 1.1.0 suite run (`sittingsuite110_*.log`, 09-09 17:30) is after all ten repairs (last at `7a401f1`, 00:37). Settling test: §3.4 |
| G4 | **Fire-rate counters** (new). `SMRFixPack.Tick(id[, branch])` on each wrapper's fix branch, counts in `SMRFixPack.counts`, dumped by the kit's `fingerprint()` and at autorun quit; baseline = the same autorun on the pre-patch build. | in game | c that leaves the boot log clean and no probe sees | ~40 one-line edits in `Code/` + ~15 core + ~10 kit | 0 owner min inside G3 | yes | **designed; untested in game.** On the answer key no FIX row is one a rate change would have shown that G1 does not: F-1/F-5 heal counts are in the log, F-2's wrapper fired normally, F-3 threw. Rank last |
| — | Patch notes → systems we fix | desk | pointers only | 0 | ~2k tokens | — | 1 of 13 note rows agreed with a fact (`GAME_1_1_0_IMPACT.md:146-168`); silent on every breakage of ours |
| — | `treediff` + `presetdiff` (exist) | desk | the full tier's raw material | 0 | 30 s + 9 s runtime; **reading** is the cost: 56k rows, 24 agents tagged 3,699 of them on 1.1.0 for zero shipped fixes | yes | `HUNT_AUDIT.md:246`, `VANILLA_DIFF_DISPOSITION.md:146` |
| ✗ | Adjacency (callees of an identical pin / changed callers of a pin) | desk | claimed c | — | — | — | measured; dominated by D1; cut (§0) |
| ✗ | Dependency manifest stored per build | desk | — | — | — | — | realised by D1 with no stored file: the archived tree is the manifest once the selectors are harvested |
| ✗ | Preset census in game vs a stored manifest | in game | — | — | — | — | dominated by `presetdiff` + fpk parity (the game loads the archived `Data/` byte-identical, `EF-085`); the only residue is runtime-modified presets, out of scope |
| ✗ | Self-check census block | in game | — | — | — | — | exists as the boot log + `logscan.py`; one addition worth 3 lines: `SMRFixPack.ListFixes()` at autorun quit |

Modules with no hashable body (19 of the 80 pre-patch modules: data patches, additive handlers, the
sanitizer) are covered by D1's `Require`/cite/preset columns only; on the answer key that was enough
for F-1, F-4, F-5 and every data-patch REMOVE row except MeteorFrequency (§3.3).

## 2 · The recommendation rule

Inputs, all emitted by D4: **P** fpk parity; **A** archive status; **M** the moved set = modules
flagged by D1 ∪ D2, with D3 hits marked; **B** base-class structure changed under a pinned/cited
file; **T** changed hand declarations.

| verdict | condition | what it buys | expected cost |
|---|---|---|---|
| **stop** | A unarchived | archive first (`WORKFLOW.md` step 0) | 5 min |
| **none** | P holds, **M = ∅**, D3 = ∅, B = ∅ | nothing to read; G1 at the next sitting (a 24 h / next-playtest gate, never a block) | the run: ~5k tokens, 0 owner min |
| **scoped** | 0 < \|M\| ≤ **12** (¼ of 50 modules), B = ∅ | per flagged module: the 1.1.0 method — read the flagged rows in both trees, verdict FIX/REMOVE/KEEP, a REMOVE traces the replacement (R-15); D3 hits are FIX rows regardless; G1 + G3 unattended | ≈ \|M\| × 15k tokens (estimate, unmeasured: one module row of the 1.1.0 audit) + 2 owner min |
| **full** | \|M\| > 12, or B ≠ ∅, or P broken, or T > 1,000 | the 1.1.0 shape: every module re-verified, `treediff`/`presetdiff` seam reads on the flagged systems, G1/G3, one attended control per FIX | no token figure was recorded for 1.1.0 anywhere; proxies: 457 commits 09-08→09-13, ~43 subagent legs, 2,972 report lines, 21.6 MB of `vanillahunt/` |

The 12 and the 1,000 are budget choices, not measurements (§6 ask 1). On 1.1.0: \|M\| = **76 of 80**
by D1 ∪ D2 (10 FIX, 34 REMOVE, 32 KEEP), T = **4,710** (hand-file declarations whose body, signature
or existence changed, moves excluded), B = 7 (recorded, `VANILLA_DIFF_DISPOSITION.md:118-134`; D4 is
not built) → **full** by three triggers. Identity control:
\|M\| = 0 → **none**. One-file control (`Lua/Buildings/Residence.lua` at its 1.1.0 content, everything
else 1.0.7): \|M\| = 2 → **scoped**, cost two module reads.

## 3 · The backtest

**Setup.** Pre-patch pack = `Code/` at `f7bd288` (2026-09-01, the last commit before `ff39228`, the
first 1.1.0 response; 80 `Fix_*`/sanitizer modules, no `SRC:` lines — bodycheck did not exist). Answer
key = `PACK_1_1_0_REVERIFICATION.md` §1a/1b/1d: FIX 10, REMOVE 35, KEEP 35 (`DroneTransportMinors`
counted once, as KEEP). Both trees indexed with `treediff.declarations(indented=True)`: 30,063 and
33,404 declarations (the banner's 27,762 / 30,355 exclude orphans; same delimiter, different
aggregation); status counts identical 23,451 · body 4,126 · body+sig 470 · removed 1,124 · moved 672 ·
moved+body 220 · added 5,357; files changed 2,437 / identical 1,963 / added 166 / removed 36 —
matching `CALLERS.tsv` line 5. The scoring is per module: does the instrument flag it.

### 3.1 The table (`python backtest.py`, cached index, 35 s)

```
instrument                       FIX  REMOVE    KEEP | flagged
PIN                            6/10   21/35   16/35  | 43     bodycheck's reach: the pinned body
REQ                            6/10   14/35   17/35  | 37     Require targets hashed
SIGCALL                        3/10    7/35    4/35  | 14     D2
CITE                          10/10   34/35   28/35  | 72     header citations → functions / data files
CALLEE                         3/10    8/35   17/35  | 28     adjacency, out
CALLER                        10/10   26/35   30/35  | 66     adjacency, in
REDECL                         3/10    2/35    5/35  | 10     new same-named declaration elsewhere
ANCHOR                        10/10   31/35   28/35  | 69     tree lines around a module's string literal changed
PRESET                         3/10   16/35    6/35  | 25     PRESETS.tsv row for a literal id changed
PIN+REQ                       10/10   26/35   26/35  | 62
PIN+REQ+SIGCALL               10/10   27/35   27/35  | 64     = D1 ∪ D2 without the cite column
PIN+REQ+CITE                  10/10   34/35   32/35  | 76     = D1
PIN+REQ+CITE+ANCHOR           10/10   35/35   33/35  | 78
ALL                           10/10   35/35   35/35  | 80
```

### 3.2 The FIX rows, and what PIN alone sees

```
  AstrogeologistExtractors   c    PIN=0 REQ=1 SIGCALL=0 CITE=1   no body to pin; Effect_ModifyLabel.OnApplyEffect and
                                                                 GetCommanderProfile (Required) changed; Data/CommanderProfilePreset.lua changed
  FirstAsteroidPrefabs       c/d  PIN=0 REQ=1 SIGCALL=0 CITE=1   RemoveNotification, ShowPopupNotification (Required) changed;
                                                                 OnMsg.SpawnedAsteroid (cited) changed; the Asteroid popup preset changed
  SaintBlessing              c    PIN=0 REQ=1 SIGCALL=0 CITE=1   DEFECT expression still shipped (modify_trait = "Religious"), so a
                                                                 DEFECT-GONE would NOT fire; TraitPreset.AddDomeColonistsModifier (Required)
                                                                 is moved+body (generated ClassDef → Lua/TraitPreset.lua) and GetTraitLabel changed
  StaleReservations          c    PIN=0 REQ=1 SIGCALL=0 CITE=1   pin Residence.ReserveResidence IDENTICAL; Residence.CancelResidenceReservation
                                                                 (Required) changed — the function that broke F-2
  ShelterReflex              c    PIN=1 REQ=0 SIGCALL=1 CITE=1   both pins changed (MicroGHabitatAutoResolve.IsSuitable, Colonist.Idle):
                                                                 half (a) is class b, not c; GetScoreFor(traits→colonist) is the sig hit
  LandscapeUnitFilter        a    PIN=1 (body+sig)               F115
  PayloadTemplateRefill      b    PIN=1  RocketDroneChurn b PIN=1  TrainCargoDumping b PIN=1  VacuumWalks b PIN=1
```

**Claimed only what was measured:** on the four class-c FIX rows, the pinned body (where one exists)
was identical and the `Require` target hash flagged 4/4. The mechanism is that every one of those
modules *reads* the function that moved and declares it in `Require`. Nothing here says a class-c
case whose moved function is not Required or cited would be caught — that is §4.

### 3.3 Misses, by name

- **D1 (PIN+REQ+CITE) misses one answer-key row: R-9 `MeteorFrequency`** (REMOVE). Its dependency is
  the body of the `Meteors` global game-time thread, an anonymous `function(` literal — the shape
  `treediff` cannot key (its header says so). ANCHOR flags it (the lines around `"restarted"` and
  `"NoDisasters"` changed) and so does CALLER; a file-level "cited file changed" column would too.
  `CaveInsNoDisasters` (R-18, the same anonymous-callback shape via `PeriodicRepeatInfo`) is caught by
  a bare `lib.lua:1538` cite resolving to a changed function, which is luck, not design: treat
  anonymous-callback modules as **always flagged when their file changes**.
- **PIN alone misses F-1, F-2, F-4, F-5** — the class-c rows; and today's `Fix_StaleReservations.lua:4-6`
  pins `GetFreeSpace` and `ReserveResidence` but not `CancelResidenceReservation`, so the shipped
  manifest would miss a repeat of F-2. `Fix_SaintBlessing.lua:5` does pin its consumer. The rule that
  closes this is D1's: hash the `Require` targets, do not rely on the author to stamp them.
- **KEEP false positives: 32 of 35 on 1.1.0.** Not a defect of the instrument — 2,437 of 4,436 files
  changed; that is the fact that makes the verdict *full*. The instrument discriminates on a small
  patch (one-file control: 2 flagged, 1 true), not on a rewrite.
- **F117 is not in the answer key** and D2 finds it (`ArrivalDeaths`, `ChooseDome(traits,…)→(colonist,…)`).
  D2's other KEEP hits: `ShuttleTransportCache` and `TrackSalvageRefund` (prefix-compatible, benign),
  `DustSicknessBiorobots` (`Affect`, unread — one body read owed if D2 is built).
- **Not tested at the desk:** G3's recall (§3.4); G4 entirely; whether G2 at the main menu enumerates
  the same descendants as in a colony (it reads `g_Classes`, built by then, but unmeasured).

### 3.4 The test that would settle G3

Check out `SMR-BugFixPack` at `f7bd288` and the TestKit at `a293db0` (2026-08-24, its last pre-patch
commit; all ten FIX modules had a `behavior` probe then) against the live 1.1.0 game; `-smrautorun` A/B;
read FAIL/ERROR rows against the ten FIX rows. About ten owner minutes and one PC cycle. Not asked
(brief stop 1); listed in §6.

### 3.5 Controls

- **Identity** (every file 1.0.7): every instrument 0/80. Command: `python backtest.py --overlay __none__`.
- **One-file** (`Lua/Buildings/Residence.lua` at 1.1.0, rest 1.0.7 — SYNTHETIC): D1 flags
  `StaleReservations` (FIX, true) and `FreedHousingNotice` (KEEP; its cited `Colonist.SetResidence`
  changed — a read owed, correctly); CALLER flags 10. Command: `python backtest.py --overlay Lua/Buildings/Residence.lua`.
- **W42 on the pre-patch pack** (`python w42.py pre107/Code`): E9 `ArrivalDeaths` `ChooseDome`,
  `ValidateBuilding` sig; E10 `ShelterReflex` `GetScoreFor` sig; E11 `LastTransmissionStorage`
  `GetGridGlobalStorage` gone (R-12/R-13, both retired); every other E-site clean.

### 3.6 Caveats on the backtest itself

The answer key is an authored claim (three fresh-context QA readers, 0 flips, `VANILLA_FIX_QA.md:13-17`).
PIN is a harvest of the pre-patch modules, not the shipped `bodycheck` (61 of 80 resolved a pin; 3
pins named functions absent from 1.0.7, our own helpers). CITE depends on header citation discipline:
78 of 80 modules cite at least one resolvable game line. The index counts differ from the `treediff`
banner by the orphan rows, stated above. Everything is one patch pair plus two synthetic controls; the
scoped regime has no real-patch evidence until the next patch lands.

## 4 · What cannot be instrumented

- **Anonymous function literals** — thread bodies, `MapGameTimeRepeat` callbacks, preset `func`
  fields. No key, no hash; only a file-level or string-anchor flag, which says "read this file", not
  "this moved". (`MeteorFrequency`, `CaveInsNoDisasters`, and every `Msg` handler.)
- **Two hops and dynamic dispatch.** A callee's callee, `self[name]`, `Msg` fan-out, a preset's
  `func` field — the CALLERS blind spot 7. CALLEE on identical pins found 3/10; the second hop is the
  seam sweep, i.e. the full tier.
- **A vendor fix that leaves our DEFECT expression in place and moves its consumer** (F-1). Caught
  only if the consumer is Required or cited. Rule for authors: a data patch names the function that
  reads the field it edits (`Fix_SaintBlessing.lua:5` does).
- **Semantics with no text change near anything we name.** A constant's meaning, a C-side
  behaviour (`GetTargetAmount` on `rfSuspended`, F-10 "plausibly persists"), engine dispatch order.
- **Runtime body identity.** No `debug.getinfo`, no `string.dump`, no `load`
  (`00_TestCore.lua:674`, `EF-094`/`EF-096`): a probe compares behaviour on a stub, and the stub is a
  claim about the body — the 09-09 suite's five ERRORs were stubs meeting 1.1.0 bodies.
- **Played state.** F-2 needs an expedition past the 5-sol lock; F-4 needs a save with the
  first-asteroid popup unanswered. The autorun's new colony reaches neither. Attended controls only.
- **What a player finds first.** F114 was clean on every sweep that existed; PIN sees its shape
  today (body changed), but the class "our copy meets a new sibling class" has no general detector
  beyond REDECL + G2.

That is the irreducible risk: a scoped verdict certifies the one-hop neighbourhood of what the pack
names, and nothing outside it.

## 5 · `GAME_PATCH_PROMPT.md` — sketch

1. Archive the on-disk `Src` with its manifest if unarchived (`EF-075`). Stop until done.
2. `python tools/patchcheck.py` (D4) → one block: build id, parity, T, B, the D1/D2/D3 tables, D5 list,
   the verdict. Paste the block into the report verbatim; every count comes from it.
3. Read the D3 rows first (save safety): each is a FIX row whatever the verdict.
4. **none**: file the D5 list as one checklist rider; done. **scoped**: per flagged module, read the
   flagged rows in both trees, verdict FIX/REMOVE/KEEP; a REMOVE traces the replacement. **full**:
   every module; then `treediff`/`presetdiff` seam reads on the flagged systems only.
5. Patch notes: read once, map to systems, use as pointers for step 4's order. Never as evidence.
6. In game, unattended: `-smrautorun` A/B (G1 census + G2 reach + G3 suite in one boot pair) when
   scoped or full; the boot census alone at the next sitting when none.
7. Write the FIX/REMOVE prompts from the `WORKFLOW.md` table; put the deep-sweep decision and its
   cost line in the checklist; record tokens spent per step in the prompt's todo list (the 1.1.0
   response recorded none).
8. **The opt-in outbox** (owner, 2026-09-18: this prompt runs here first; the fork's
   `gamepatch/` folder under its perma prompts, with a README, is where its findings go). Step 2
   already runs D1–D3 over the opt-in `Code/` (`--code C:\Dev\SMR-OptInPack\Code`; its E-sites are
   the `Opt_` rows of `D13_EXPOSED_SET.md` §2a/2b). One entry per patch,
   `gamepatch/<new build>_<date>.md`, written even when nothing is flagged, carrying what an agent
   there needs to act cold with no other context:
   - the build pair (old and new build ids, both archive digests) and the fix-pack commit the sweep
     ran at, so the entry is a claim they can re-run in a minute;
   - the exact command that produced it, so they can;
   - the fix-pack verdict tier and its three inputs (P, T, B), so they know how big the patch is;
   - per opt-in module: the flagged rows verbatim — function, status (body / sig `old→new` /
     removed / moved), `file:line` in both trees — and, for a clean module, the line `no row`;
   - what is asked per flagged module: a body read in both trees and a FIX / REMOVE / KEEP verdict
     filed in the fork's `bugs/`, a REMOVE tracing the replacement (R-15); nothing else;
   - the stops: no edits outside the fork, no boot unless the owner asks, questions to the fork's
     checklist.
   The README says: read the newest entry, run its command, act per verdict, move the entry to
   `gamepatch/done/`. The build brief creates the folder.

**Drop order when budget runs out:** seam reads (4-full) → patch notes (5) → the suite half of 6 →
the D5 filing → G2. D1/D2/D3, the boot census and the outbox entry are never dropped: they are the
sweep, and the entry is the only route the fork has to it.

## 6 · Asks for the owner

1. The scoped ceiling (12 modules) and the size trigger (1,000 changed hand declarations) — both
   budget rulings; the backtest only fixes the extremes (0 → none, 64 → full).
2. Does the unattended A/B (G3) run on every patch (~2 owner min + ~10 machine min) or only on
   scoped/full? Recommendation: scoped/full only; on none, the boot census at the next sitting.
3. Fire-rate counters (G4): 40 one-line edits to shipped `Code/`. Recommendation: not now — no
   answer-key row needed them; revisit after the first scoped patch shows a clean-log class-c case.
4. The ten-minute boot in §3.4 that would measure G3's recall. Not owed; named.
5. Manifest policy: adopt D1 (archive-as-manifest, harvested `Require` targets) as bodycheck's
   mode, or require an `SRC:` line per `Require` target. Recommendation: D1 — it also serves the
   opt-in pack, which has no stamps.
6. `prompts/STANDDOWN_AUDIT.md`: its product 1 (a desk class-c detector) is superseded by D1 + this
   backtest; product 2 (per-module runtime decline via behaviour probes) stands and belongs to the
   build brief. Coordinator's call whether to cut the prompt to product 2 or retire it; [D14](../bugs/D14.md)
   keeps its design record either way.

## 7 · Scratch scripts (in the session scratchpad, not `tools/`; described so a builder can re-derive)

- `backtest.py` (~330 lines). `sys.path` → `tools/`; imports `luafn.read_lines`,
  `treediff.declarations/tree_files/bucket/bare_name`. Indexes both trees (pickled, 85 MB). Harvests
  per module with six regexes: `{ class = "C", method = "M" }`, `{ global = "G" }`, `SetGlobal("G"`,
  `^\s*function C[:.]M(`, `^\s*C.M = function`, `^\s*local x = C.M$`, plus `local A = C` /
  `local A = rawget(_G, "C")` alias resolution, `(Lua|CommonLua|Data)[\\/]…\.lua:N(-N)?` and bare
  `File.lua:N` (unique basename) citations, and `"Identifier"` literals. Comments stripped before
  harvesting code, kept for citations. Status per (file, key) as in §3. `--overlay f1,f2` builds the
  synthetic control. Output: the §3.1 table, per-row detail, `backtest_rows.tsv`.
- `w42.py` (~60 lines): D3 over the E-site modules of a given `Code/`.
- `facts_cite.py` (~60 lines): D5 over `docs/agent/facts/*.md`.
- Timings on this rig: `sigcheck.py` 0.8 s, `bodycheck.py` < 1 s, `treediff.py` 30 s, `presetdiff.py`
  9 s, `backtest.py` 46 s cold / 35 s cached (ANCHOR is the slow column).

## 8 · Out-of-scope findings

- The "6 of the 10 FIX rows" sentence (§0) in `WORKFLOW.md:97-98` and `tools/bodycheck.py:94-95`.
- `Fix_StaleReservations.lua:4-6` does not pin `CancelResidenceReservation` (§3.3).
- F117 was desk-detectable on 09-08 by a one-second signature check over module calls; it was found
  09-09 by hand in a KEEP module.
- `DustSicknessBiorobots` calls `Affect`, whose signature changed 1.0.7→1.1.0; unread here.
- The opt-in pack: 6 modules, zero `SRC:` lines, no `bodycheck`/`sigcheck` in its `tools/`.
- No token, wall-clock or owner-minute figure exists for the 1.1.0 response; the only cost statement
  is the brief's "expensive in tokens". The perma prompt's todo list should carry per-step tokens.
- `python tools/doccheck.py --emit-fingerprint` routes 54 facts as one MOVED group on a build change;
  D5 names 42 facts and their functions.
