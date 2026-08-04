# Chain prompt 2 — the run: prove, execute, record

**Read `README.md` in this folder first — binding chain rules apply.**
Unattended once launched — **confirm with the owner in chat that the machine
is free before the first launch; that word is the only attendance in this
prompt.** Start with `git log --oneline -10` + `git pull`. Todo list up
front: one item per cycle plus one per recording commit — the owner reads
the list to see where the run is without a transcript.

**Read path**: this folder's README + the cycle plan in "Notes from
upstream" below · `docs/PLAYTEST_HELP.md` "The co-run rig" (the mechanics —
staging, arming at the run per rule 5, launch command, timing discipline) ·
the parked probe sources beside this file · the entries each leg records to
(`F99.md`, `C42.md`, `F35.md`, `F03.md`, the heal entries prompt 1 names).

## Jobs

**Job 1 — probe-hygiene sweep, then stage.** Sweep first (hard gate).
Stage the copy game-closed per the HELP procedure; the campaign save is
never written.

**Job 2 — cycle 0: the proof cycle.** Fixture confirms (all label reads) +
the SAVE-primitive proof exactly as prompt 1 wrote it. ⛔ Nothing that
leans on an unproven read or primitive runs before its proof passes. A
failed confirm turns its legs into `SKIP <reason>` lines and routed gaps —
continue with the rest.

**Job 3 — the leg cycles, per the plan.** For every cycle: arm at the run
(file + metadata line via a script FILE — C11), parse sweep, launch, read
the log after flush, disarm in the commit that records the answers, staged
saves and throwaway saves deleted, `PROBE SWEEP:` line, `git add -f` every
cited log. Every recorded number carries the run-conditions header.
Per-line watchdog discipline: if a cycle hangs, the probe's own watchdog
quits; **if the process must be killed from outside, that is an
unforeseen-issue finding — record how it presented before killing.**

**Job 4 — record as you go, not at the end.** Each leg's verdict goes on
its entry (or checklist rider line) in the commit that archives its log:
what was forced, what stayed organic, the falsifier, `SKIP` reasons
verbatim. Leg E flips the two `[NEVER RUN]` table rows to
`[RAN 2026-MM-DD, log <name>]` — only if the log actually shows the storm
start/stop and the electro devil (the fx class or an equivalent readable
mark; if nothing readable confirms the electro variant, say so and leave
the row marker honest).

**Job 5 — the unforeseen-issues ledger.** This run is the co-run program's
test bed. Keep a running list IN THE OUTBOX of every deviation, however
small: unexpected log lines (report verbatim with age — never discount),
timing surprises against predictions, retries, tool quirks, anything that
would have needed a hand. An uneventful run reports "none observed over N
cycles", which is itself the measurement.

**Job 6 — close out.** Append to `03_FABLE_AUDIT.md` "Notes from upstream":
per-leg verdicts with log names, the actuals-vs-predictions table, the
unforeseen-issues ledger, every routed gap, and anything owed. Update the
README manifest row; commit (doccheck green, push); delete this file in the
same commit.

## Stop conditions

- README chain-wide stops bind (modal/picker/hang → record, quit, route).
- A leg needs eyes or hands after all → chain rule 14: route it with the
  offer to author `02b_OPUS_CORUN.md` before the audit (measure-moments
  list, prep per rule 5, cost stated). Owner yes → build it, add its
  manifest row, append its handoff needs to the audit's inbox. No answer
  by your close-out → checklist rider, chain continues.
- The owner interrupts or needs the machine → finish the current cycle's
  disarm + recording commit, then stop cleanly; the chain resumes later
  from the todo list.
- Any leg's world-mutation leaks into a later read on the same cycle →
  void that read, note it, re-run the read on a fresh cycle.

## ⛔ What you may not claim

- Not `tested` for anything — unattended ceiling is MECHANISM /
  probe-verified (WORKFLOW triage mode 1).
- Not a refutation from any zero — state the CONDITION sampled and the
  count (leg C especially: zero `:805` under organic repair is a rate bound
  on the sampled configuration, not proof of unreachability).
- Not F99 severity — the discriminator's RESULT routes to the owner's
  existing decision line either way.
- Not rig capabilities beyond what this run exercised.

## Notes from upstream

*(Appended by prompt 1, 2026-08-04. Everything below is Src-verified or
derived this session; nothing here is a measurement — no game was launched.)*

### 1 · The SAVE primitive — BINNED (README rule 10), still UNPROVEN

`SaveGame(display_name, params)` — ⚠️ the file is **`CommonLua/Savegame.lua`**,
not `Lua/Savegame.lua` (that one is 103 lines and has no `SaveGame`); the
prompt's `:1071`, `:295-318` and `:337-344` all resolve in `CommonLua`.

| question | answer, with the line that says so |
|---|---|
| plain global? | yes, `CommonLua/Savegame.lua:1071` |
| blacklisted? | **no** — not a key of `ModEnvBlacklist`, `CommonLua/Classes/Mod.lua:1267-1428`, **re-derived this session** rather than inherited from the corun-rig S2 grep. Also checked: no game-side `ModBlacklistPrefixes` handler exists in `Lua/` or `DLC/`, so the runtime prefix sweep at `:1445-1459` adds nothing |
| does it yield? | **yes, three ways** — `WaitRenderMode("ui")` `:1079`; `DoSaveGame`'s `WaitChangeMapDone()` / `WaitSaveGameDone()` `:1038-1039`; and `Savegame._WrappedSave` = `_Wrap(_InternalSave)` `:874`, whose wrapper does `WaitThread` → `CreateRealTimeThread` → `WaitThread` (`:337-344`). ⇒ **call it from a REAL-TIME thread**, the same conclusion that forced a thread for `LoadGame` (S2) |
| what `params`? | `savename` → routes to `Savegame.WithName` (`:1051` → `:895`), bypassing `_UniqueName`, so the filename is **exactly** what we pass · `silent` → skips `LoadingScreenOpen/Close` (`:1075-1077`, `:1088-1090`) · `no_screenshot` → skips the scene render-mode round trip (`:1010-1023`) · `force_overwrite` is read only by `_UniqueName` and is irrelevant on the `savename` route |
| ⛔ what NOT to pass | **`save_as_last`**. It writes `LocalStorage.last_save` (`:1057-1059`) — i.e. it would repoint the owner's *Continue* button at our throwaway. A do-no-harm hazard, not a preference. `U1.Load` also passes `{}` to `LoadGame` for the same reason |
| filename on disk | with `savename`: verbatim, in `GetPCSaveFolder()`. Without: `CanonizeSaveGameName(display) .. ".savegame" .. ".sav"` (`config.SaveGameExt = ".sav"`, `CommonLua/Core/config.lua:21`), `(N)`-disambiguated if it exists (`:302-312`). **No `.bak`** — both `WithName` and `WithTag` set `params.backup = false` (`:908`/`:890`) |
| listing it back | `Savegame.ListForTag("savegame")` = `_Wrap(_InternalListForTag)` (`:941`/`:469`). The tag is parsed back **out of the filename** by `^.*%.([%w_]+)%.sav$` (`:477`) — which is why every throwaway name in this chain ends `.savegame.sav` |
| returns | `err, name, meta` |

**⛔ DELETION ROUTE — DECIDED: agent-side `Remove-Item`, game closed.** Three
reasons, and the first is the one that settles it rather than merely preferring
it: **the mod environment has no file-delete primitive at all** — `io`, `os`
*and* `AsyncFileDelete` are all keys of `ModEnvBlacklist`
(`Mod.lua:1424`, `:1425`, `:1329`). Second, `Savegame.Delete` does exist
(`_Wrap(_InternalDeleteWithBackup)`, `:938`/`:454`) and the `Savegame` table is
not blacklisted — but it is a **second unproven primitive**, and it deletes a
`.bak` we never create; adding it to the risk surface buys nothing. Third,
agent-side deletion with the game closed is the shape already proven four times
on staged copies. ⇒ **throwaway saves die in the same `Remove-Item` step as the
staged copy, in the recording commit.**

**The proof step for you** is written and parked as `98_U1C0.lua.txt`, step
`P-save-primitive`: (1) read `type(SaveGame)` from the mod env — this is the
cheap *runtime* settle of the blacklist question, and it is needed because
`ModEnvBlacklist` is itself blacklisted (`:1385`) and cannot be read directly;
(2) list before; (3) `SaveGame` under `U1C0PROOF.savegame.sav`; (4) list after —
the file must appear; (5) `LoadGame` it back and confirm the world comes live.
It prints `SAVEPROOF PASS` or `SAVEPROOF FAIL` and sets `U1.save_proven`.

⛔ **Ceiling until you run it: Src-verified. Not PROVEN.** Legs A, D1 and D2
each check `U1.save_proven` and abort themselves to routed gaps; leg A
additionally still yields a real result from its first half.

### 2 · Leg D — RE-DERIVED, and it is now two legs

⚠️ **The old design is not inherited.** `CHAIN_QA_REPORT.md` §9 item 2 is one
sentence — *"save, reload twice, read the numbers (Astrogeologist +10% class of
defect)"* — written for the owner driving their own campaign. Re-derived from
the code the entries point at:

**Which heal lines print on load.** Exactly six pack modules print a heal line
from a load handler, and **every one prints only when it actually healed
something** (`if healed > 0 then log(...)`), so silence is a result, not missing
instrumentation:

| # | module | line | latch / idempotence mechanism |
|---|---|---|---|
| H1 | `Fix_AstrogeologistExtractors` (F92) | `applied %d Astrogeologist extractor bonus(es)…` / `removed %d duplicate…` (`:174`) | property test, not identity — that swap **was** the 2026-08-02 defect |
| H2 | `Fix_SaintBlessing` (F95) | `re-based %d dome blessing(s)…` (`:151`) | presence test on `dome.label_modifiers` |
| H3 | `Fix_DustSicknessBiorobots` | `cleared Dust Sickness from %d Biorobot(s)` (`:167`) | the state is cleared, so a rerun finds none |
| H4 | `Opt_MultipleSuns` | `reconnected %d solar panel(s)…` (`:206`) | reconnection persists |
| H5 | `Fix_MeteorFrequency` (F88) | `one-shot heal … (latch %s -> %s)` (`:164`) | **`GameVar("SMRFixPack_MeteorLatch")` — persisted, i.e. it lives in the save** |
| H6 | `Fix_RainsDeadlock` (C34) | C34 structure-repair + migration lines (`:210`) | version latch + structure checks |

`90_SaveSanitizer` (F35/F03) prints **nothing** from `PostLoadGame` unless a
pass throws — it is leg A's subject, driven directly, not watched here.

**On which loads they must appear once and then not repeat.** Every one of these
heals writes **persisted** state (colony/dome `label_modifiers`, colonist
traits, the latch GameVar, the rains structures). So a heal that fires on load 1
is *in* the save written immediately after, and loads 2 and 3 of that file must
print nothing. A line that reappears is the defect — F92's shape exactly (1
modifier became 2 after one save+reload) and F88's shape exactly (unlatched
restart every load).

**What numbers get compared.** Not the lines — the counts behind them, read
identically at every load by `U1.ReadAllHeals()`, diffed by `U1.CompareHeals()`
which prints one `HEALDIFF` line per family and a `VERDICT` count.

⚠️ **The problem the old design could not have seen, and the fix for it.** The
staged copy is `TEST2H TRAIN`, not the owner's campaign. **A family whose
condition does not exist on that save is UNSAMPLED, not clean** — and reporting
it as clean would be the exact error the 2026-08-03 refuted/unsampled correction
was about. So:

- **Leg D1** (cycle 1, `98_U1C1`) measures the save as it actually is: load
  staged → read → save → reload → read → reload → read. Every reader prints its
  own `APPLICABLE` verdict.
- **Leg D2** (cycle 6, `98_U1C6`) **creates** the defect state for the two
  families whose pre-heal state is exactly and reversibly definable, so they get
  sampled instead of assumed: `SMRFixPack_MeteorLatch = false` (H5, applicable
  on every save), and stripping the two labels the astro heal owns —
  `AutomaticMetalsExtractor`/`production_per_day1` and
  `MicroGAutoWaterExtractor`/`water_production`, taken from the module's own
  `MISSING` list (`Fix_AstrogeologistExtractors.lua:67-70`), profile id
  `astrogeologist` (`:62`) — then save → reload (must heal, **exactly once**,
  landing at exactly the baseline and **never above it**) → save → reload (must
  **not** heal, numbers identical). FORCED: the removal. ORGANIC: nothing.
  Ceiling: MECHANISM.
  H2/H3/H4/H6 are deliberately **not** forced — doing so means editing colonist
  traits, dome membership or disaster structures, a bigger mutation than the
  measurement is worth and not reversible by the heal alone. They are reported
  as cycle 1 found them, sampled or unsampled, said plainly.

### 3 · The cycle plan

Fixed cost model from `PLAYTEST_HELP` "The co-run rig": **~30 s overhead per
cycle** (menu poll 2.5 s, load 9.5–10 s, settle 15 s, flush/quit 1.5 s) **+ ~25 s
per additional load** + payload. ⚠️ **The one cost nobody has measured is
`SaveGame` itself** — predicted 10–20 s on the 56 MB save by analogy with the
load, and that prediction is itself a thing to record.

**Ordering.** Reads first, mutations last (README). ⚠️ Worth saying plainly so
nobody thinks it is superstition: cross-cycle contamination is impossible by
construction — each cycle is a fresh process that loads an unmodified staged
copy, and loading never writes it. The *one* real cross-cycle channel is the
throwaway files on disk, which is why **every throwaway name carries its cycle
number**.

| cycle | probe | legs | mutates world? | loads | saves | prediction | watchdog (3× / worst case) |
|---|---|---|---|---|---|---|---|
| 0 | `98_U1C0` | **save-primitive proof** + all fixture confirms + **leg F** (C42) | no | 2 | 1 | ~1.5 min | **6 min** (floor) |
| 1 | `98_U1C1` | **leg D1** | no | 3 | 1 | ~1.7 min | **6 min** (floor) |
| 2 | `98_U1C2` | **leg A** (PT-35) | no | 2 | 1 | ~1.5 min | **6 min** (floor) |
| 3 | `98_U1C3` | **leg B** (F99 pre-reload residue) | **yes** | 1 | 0 | ~1.7 min | **6 min** (> 60 s site wait + overhead) |
| 4 | `98_U1C4` | **leg C** (F99 no-cheat discriminator) | **yes** | 1 | 0 | ~6 min | **18 min** (> the 16.5 min worst case: 4 rounds × 4 min) |
| 5 | `98_U1C5` | **leg E** (the two `[NEVER RUN]` rows) | **yes, most** | 1 | 0 | ~3 min | **9 min** (> two 3 min storm waits + overhead) |
| 6 | `98_U1C6` | **leg D2** | **yes** | 4 | 2 | ~2.5 min | **8 min** |

Total predicted machine time ≈ **18 min** across 7 launches; worst case ≈ 59 min.
Owner attendance: **the kickoff word only.**

**Cycle 0's fixture confirms — all label reads, nothing mutates:**

| confirm | for | what makes it OK | what a failure means |
|---|---|---|---|
| `PT35 fixture` — `FrictionlessComposites` researched, Large Wind Turbine count, dome count, dome modifier count | leg A | ≥1 Large Wind Turbine **and** ≥1 dome | leg A's turbine half is `SKIP <no Large Wind Turbine on the staged copy>` |
| `PT35 fixture MedCenter` — Medical Centers and how many carry applied upgrades | leg A | ≥1 Medical Center | leg A still runs; the F03 half becomes a read over whatever upgrades exist, stated as such |
| `HEAL SWEEP` × 6 families with `APPLICABLE` verdicts | legs D1/D2 | ≥1 applicable family | see §5 — this is the routed decision, not a stop |
| `TRACKS` + `DRONES` + first break candidate | legs B, C | ≥1 element matching `BreakTracks`' own filter, ≥1 drone, ≥1 hub | that leg is `SKIP <what was missing>` + routed gap. ⛔ Never a re-choice of save |
| `C42STALE` | leg F | ≥1 Passage | `SKIP <no Passage on the staged copy>` — the README already anticipates this |
| `LEG E fixture` — presets, map settings, function reachability | leg E | the presets and both functions resolve | the `[NEVER RUN]` row stays `[NEVER RUN]`, with the reason recorded |

⛔ **Fixture presence on `TEST2H TRAIN` is NOT claimed by this prompt.** The
record shows what the co-run #1 *sitting* had, not what the save captured. Cycle
0's reads decide, and they are the first thing you should paste into the outbox.

### 4 · Run-conditions header — every recorded number carries it

The probe emits this itself as a `CONDITIONS` line at every load
(`U1.ReadConditions(note)`), so the log is self-describing. When you write a
number into an entry, carry it in this shape:

> **Run conditions.** Retail `Mars.exe` **1.0.7.396349**, cold load of a staged
> COPY (`U1STAGE.savegame.sav`) of `TEST2H TRAIN`, pack **N/M active as READ**
> (never assumed — the owner's campaign runs every opt-in ON, which is not
> default config), speed `S`, session uptime ~`T`, load `L` of this process,
> `K` `[LUA ERROR]` lines in the window. Raw lines:
> `docs/archive/u1c<N>_<logname>.log`.

Plus, on every finding: **what was FORCED and what stayed ORGANIC** (README
rule 11), and the leg's own falsifier sentence.

### 5 · Falsifiers — one sentence per leg, to be quoted in the record

- **Leg A is wrong if** either sanitizer call returns non-zero on a save whose
  automatic `PostLoadGame` pass has already run, or if any read-back number
  differs before vs after a call, or grows across the save/reload.
- **Leg B is wrong if** the pre-reload `F99RESIDUE` read is taken after any save
  or load (which would let `RebuildBrokenTracksAndConnect`,
  `TrackElement.lua:824-837`, sweep exactly what it looks for — the mistake that
  made the original `0 0` reading meaningless).
- **Leg C is wrong if** any completion on the measured path was cheated, or if
  a round that timed out is counted as a zero rather than as unsampled.
- **Leg D1 is wrong if** a family's `APPLICABLE=false` reading is reported as a
  clean result rather than as an unsampled condition.
- **Leg D2 is wrong if** the forced state was not actually written before the
  save (check the post-force read), or if the "heal fired once" claim rests on
  the absence of a line rather than on the line's presence after load 2 **and**
  its absence after load 3.
- **Leg E is wrong if** a `[NEVER RUN]` row is flipped on the strength of the
  call returning without error — the storm needs a start **and** a stop reading,
  the devil needs `fx_actor_class == "DustDevilElectro"` (or the Major variant)
  or a non-nil `drone_battery`.
- **Leg F is wrong if** `C42STALE 0` is reported where `passages == 0` — that is
  zero passages, not zero stale entries.

### 6 · Parked sources (probe hygiene rule 5 — parse sweep GREEN, 8/8, 2026-08-04)

`97_U1Common.lua.txt` is the shared harness and **starts nothing on its own**;
each cycle arms it **together with exactly one** `98_U1C<N>.lua.txt`, which sets
`U1.tag` / `U1.watchdog`, defines `U1.Payload` and calls `U1.Boot()`. All eight
carry the literal `TEMPORARY` marker. Arm with a **script FILE**, never an
inline PowerShell one-liner (C11), and list the harness **before** the payload
in `metadata.lua` `code`.

Throwaway save names, one per cycle so no two can collide:
`U1C0PROOF` · `U1C1HEAL` · `U1C2PT35` · `U1C6FORCED` · `U1C6HEALED`
(all `.savegame.sav`). Staged copy: `U1STAGE.savegame.sav`. **All six files die
in the same `Remove-Item` step, game closed, in the recording commit.**

### 7 · Corrections this prompt is making in the open (chain rule 5)

1. **This chain's own README, leg B.** It prescribes
   `CheatMeteors("single", nil, pos)` "because the meteor path is what populates
   `repair_cgs` (`Meteors.lua:609`)". The citation and the `repair_cgs` point
   are right; the instrument is wrong. `BaseMeteor:HitTracks`
   (`Meteors.lua:615-621`) collects elements and calls the **plain global**
   `BreakTracks(elements)` (`:599-613`) — and it is `BreakTracks`, not the
   meteor, that applies the neither-endpoint/no-station filter (`:601`), calls
   `BreakTrackElement` (`:603`), does `table.insert(track.repair_cgs, cg)`
   (`:609`) and fires `Msg("TrackBroken", track, true)` (`:610`). So
   `BreakTracks({element})` **is** the meteor's own funnel with the lottery,
   the disaster thread and the collateral removed (WORKFLOW leg-design rule 2).
   ⚠️ And it is specifically **not** co-run #1's `BreakTrackElement` call, which
   does *not* populate `repair_cgs` — and `repair_cgs` is half of what leg B
   reads. README updated.
2. **`PLAYTEST_HELP.md`, the `CheatDustDevil` row.** It says the electro roll is
   `Random(100) < descr.electro_chance`. Read this session at
   `DustDevils.lua:138` it is **`SessionRandom:Random(100)`**. Conclusion
   unchanged (0..99 `< 100` is always true) but the row named a function that is
   not on the line. Row corrected. Two further things the row does not say and
   an unattended run needs: `GetTerrainCursorClamped()` is **useless without a
   mouse**, and `GenerateDustDevilIn` **returns nil early** on a vegetated point
   (`:129-131`), so a silent nothing is a documented outcome — the leg uses
   `GetRandomPassable` and retries, and reports the attempt count.
3. **The prompt's own citation.** `SaveGame` is in `CommonLua/Savegame.lua`, not
   `Lua/Savegame.lua`. Noted here, not edited into a consumed prompt.

### 8 · Open risks and routed items

- ⚖️ **ROUTED, on the checklist (not a stop):** if cycle 0 finds **no** heal
  family applicable on `TEST2H TRAIN`, leg D1's result is six unsampled
  families. The offer put to the owner is to stage a copy of the **campaign**
  save for leg D only. If they have not answered by the time you reach cycle 1,
  **run it anyway on `TEST2H TRAIN`**, report the unsampled families as
  unsampled, and let leg D2 carry the sampling — do not wait.
- **No leg needs eyes or hands** (README rule 14 checked leg by leg, and this is
  a finding, not an omission): leg C's organic completion is read from object
  state, not watched; leg E's storm and electro devil are read from GameVars and
  the devil object, not from the screen. **No `02b_OPUS_CORUN.md` offer is
  raised by this re-scope.** If one appears during the run, rule 14 applies to
  you.
- **`SaveGame` cost is unmeasured** — if a save takes minutes rather than
  seconds, cycles 1, 2 and 6 will crowd their 6–8 min watchdogs. That is a
  finding for the ledger, and re-running with a raised watchdog is the fix, not
  a redesign.
- **Leg C may simply not get an organic repair done** on this save (no
  resources reachable, drones committed elsewhere). The probe reports attempted
  / completed / timed-out separately for exactly that reason. A zero-completed
  run is a **fixture** result, not an F99 result.
- **Leg E is the most destructive cycle in the chain.** It runs last among the
  mutating cycles, on a copy, and `CheatDustStorm` ends any running disaster
  before it starts (`DustStorm.lua:541`) — worth knowing before reading its log.
- **Nothing in this prompt was executed.** No game launched, no save written, no
  `[NEVER RUN]` row flipped.
