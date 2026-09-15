# smrtk 08b — changed-surface acceptance, attended

2026-09-14. **Verdict: PASS WITH CORRECTIONS.** Items 1–8 and 10 PASS, item 9 PARTIAL.
Attended by `smr-bugfixpack-c2` (Claude Opus 5), owner at the keyboard. Fixture
`SMRTK_490.savegame.sav` (sol 490, `BlankBig_04`), `fix_pack_present=46/46`,
`game=403908`, `pack_version=11`, all three mods loaded — read live from the boot, not
carried. Pack input `5f16199`; TestKit ran from `d80fb5e` and closed at `2c3d05c`.

⚠️ **THIS SITTING DEPARTED FROM ITS OWN SCOPE FENCE, BY OWNER LICENCE.** 08b says a
defect found here is **FILED, not repaired**. The owner lifted that in words —
*"If its a simple fix and you think you know how to fix it you I am ok with either you
fixing it or firing up a subagent"* — so the attendee also built. **Eleven repairs came
out of an attendee link.** ⛔ 99 is told rather than left to infer it from the commits.

**Logs archived beside this report** (`archive/logs/smrtk08b_Mars.exe-20260914-*.log`):
`18.49.40` (caption evidence) · `19.01.16` (item 2) · `19.08.05` (items 3–5) ·
`20.03.09` (items 6–10, RunAll, the requirement-(A) sample). ⚠️ Evidence spans FOUR
boots because three fixes needed relaunches; a single-log re-derivation will miss half.

⛔ **Reading these logs: every record appears TWICE** (file + console tap) **except
chrome verbs, which appear once.** `SMRTK_TAB` tallies an odd 13 for that reason.
**Never quote a raw verb count as an action count** — dedup by `id=`.

---

## The headline — requirement (A) re-established

08 proved (A) on the OLD surface; 09's rebuild invalidated that for changed code.
Re-measured in play: **19 unique vanilla cheat leaves dispatched, then
`SMRTK_TAINT_READ ... used=false`.** Zero ERROR, zero REFUSED, the `SMRTK_TAINT` assert
never fired, every record `valid_after=true`.

| leaf | n |
|---|---|
| `CheatCleanAndFix` | 7 |
| `CheatFill` | 4 |
| `CheatMalfunction` | 3 |
| `CheatEmpty` | 3 |
| `CheatLightningStrike` | 1 |
| `CheatAddDust` | 1 |

⛔ **This is a 19-dispatch SAMPLE, not 08's 844, and NOT universal proof.** It
re-establishes (A) on the current tree and nothing more. The eligibility half stays
**unmeasurable** (`CanUnlockAchievement` blacklisted, `EF-096`) — ⛔ CLEAN must never be
read as "achievements are safe".

## Per-item verdicts

| # | class | verdict |
|---|---|---|
| 1 | navigation / chrome | **PASS** — 8 defects found and repaired |
| 2 | evidence, copy / clear | **PASS** — witnessed |
| 3 | status / ownership | **PASS** — arms 3/3, zero survivors |
| 4 | Selected + depots | **PASS** — caught the `EF-102` defect |
| 5 | More | **PASS** — real leaf dispatch |
| 6 | World | **PASS** — incl. `rocket_arrive` and fix-all idempotence |
| 7 | cursor disasters | **PASS** — `forced_pos` splits exactly as designed |
| 8 | speed / run-until | **PASS** — full ladder, self-stopping run-until |
| 9 | Agent + field watch | ⚠️ **PARTIAL** — configure/arm witnessed, trigger NOT RUN |
| 10 | hot bar + Kit | **PASS** — plus an unplanned full RunAll |

**Item 2** — `COPY flushed=true from=42 lines=5 truncated=false` scoped to `MARK mark=42`,
then `CLEAR`, then a NEW `TAINT_READ`, with records 36–41 **still in the file**.
⇒ Clear screen clears PRESENTATION ONLY and destroys no evidence.

**Item 3** — `ARM slot_4 mutation=none once_click=true` → `FIRE clicks=1 mutation=none
object=FusionReactor(8179)` → `DISARM reason="click complete"`; second cycle ended
`DISARM clicks=0 reason="right click"`. Arms balance **3 armed / 3 disarmed / 2 fired**,
last event a DISARM. The right-click escape releases exclusive input, not just the banner.

**Item 4** — measured change on three classes across BOTH `EF-102` branches:
`StorageFuel` 25018→180000→0 · `MechanizedDepotFood` 1490000→3950000→0 ·
`UniversalStorageDepot` ten resources →30000→0.

**Item 6** — `spawn_colonists_10` reported `outcome=spawn_dispatched`,
`before=689 after_same_tick=689`, `verification="deferred GameInit; census required"` —
dispatch, not a post-mutation REFUSED (defect 22's repair, witnessed). Both sweeps
reconcile against their own total, and the idempotence pair is decisive:

| id | action | changed | unchanged | skipped | = visited |
|---|---|---|---|---|---|
| 46 | malfunction_all | 741 | 1 | 557 | 1299 ✓ |
| 47 | fix_all | 741 | 558 | 0 | 1299 ✓ |
| 48 | fix_all | **0** | 1299 | 0 | 1299 ✓ |

⇒ `changed` measures real state, not visits. 09's claim *"unchanged calls do not count as
changed"* is now witnessed rather than asserted.
`rocket_arrive`: `visited=9 changed=1 skipped_time=438405`,
`landing="native policy; orbit/landing waits unchanged"` — it skips TRANSIT and leaves the
orbit wait native. ⛔ A rocket left in orbit is the CORRECT result, not a partial one.

**Item 7** — `forced_pos=true` for both "at click" variants, `false` for both scattered.
⛔ Multispawn stacking every meteor on the clicked point is the CONTRACT ("at click"), not
a defect; it was nearly filed as one before the owner caught a misclick.

**Item 8** — full speed ladder each logging `before`→`factor` (1000→3000→5000→20000→
128000→0→1000). Run-until armed at 128x, **stopped itself on the sol**, paused, marked,
and both it and the trigger self-disarmed. `FIRE run_until paused=true` covers 09's
specific worry: a trigger that pauses game time must still stop run-until immediately.
⭐ **Four `ARM run_until ... status=REFUSED reason="target sol must be a future integer"`**
— pre-mutation refusal holding under real misuse, which a scripted run never exercises.

**Item 9 — PARTIAL.** Configure and arm both witnessed
(`ARM watch_selected_field field=storage cadence=1000 once=false`), but the watch never
fired: **`baseline=nil`**, because the field was `storage` on a `MoistureVaporator`, which
has none. ⛔ **NOT RUN, not an inferred pass.** Risk assessed low — the polling machinery
is the same code `trigger_sol` exercised twice — but that is a prediction, not evidence.
Also witnessed: `DISARM ... reason=SaveGameStart` on all three arms, the documented
save-disarms-everything lifecycle.

**Item 10** — Screenshot + Mark OK. The owner then ran the **full probe suite**
unprompted (*"it literally can't hurt and its better to know if something else we did
broke them"*): **69 PASS / 4 FAIL / 18 SKIP / 6 ERROR = 97**, matching the registered
count. ⇒ **No regression from this sitting's eleven repairs.**

## Defects FOUND AND REPAIRED (11, all TestKit, 0 shipped hashes)

| # | defect | commit |
|---|---|---|
| 1 | ⭐ **every button caption invisible** across the whole toolkit | `5a281f1` |
| 2 | status strip clipped by a fixed `MaxHeight 50` | `f58b3b2` |
| 3 | dock jammed against the game's dock | `f58b3b2` |
| 4 | dock carried no status at a glance | `f58b3b2` |
| 5 | quiet state ambiguous (shown only when on) | `f58b3b2` |
| 6 | eligibility as permanent always-on noise | `f58b3b2` |
| 7 | console auto-opened on every load | `f58b3b2` |
| 8 | status bar 106 logical units too high | `78305d4` |
| 9 | TextStyle declared too early to register | `e7226f8` |
| 10 | tab row could not wrap; clipped at size 20 | `174a601` |
| 11 | probe picker in wave order, not alphabetical | `2c3d05c` |

⭐ **Defect 1 is the one to remember.** `T.Button` passed a mod-declared TextStyle that
never resolved, so EVERY caption drew blank while every plain label rendered. It was
**defect 7's own partial fix** — the size-20 style invented to answer the font complaint
is what blanked the UI. ⇒ **A surface cannot be design-judged while a render bug is live.**
The owner was one message away from commissioning a full redesign sweep of a panel whose
buttons had no labels.

⭐ **Three of these are ONE class** (2, 8, 10 — and the dock's `MaxWidth`): **a fixed cap
that clips once content grows.** The tab row was fixed by making it WRAP rather than by
re-tuning a width, because a re-tuned number only postpones the next break.

⭐ **Defect 7 (font) is RULED at 16** — see ck183. It supersedes the original
"stay larger than vanilla Cheats (18)" premise rather than satisfying it. ⛔ **A font
verdict is worthless unless the log proves which font rendered**: the first verdict would
have been passed on the 13pt fallback, and only `SMRTK_TEXTSTYLE_FALLBACK` disappearing
from the log showed the real typography was on screen.

## Defects FOUND AND NOT REPAIRED — routed, with causes pinned

1. ⚠️ **The preflight attestation was accepted 5 hours stale, from a different tree.**
   The RunAll recorded `preflight="DESKTOP sweep CLEAN: 2026-09-14T15:20:31Z
   pack=3ae67dea… kit=c886fb70…"` while the running tree was `8e25f6b` — **several
   commits later**. ⛔ The gate exists to assert the sweep matches the code and it passed
   a sweep of different code, which quietly weakens every verdict riding on it.
   ⇒ **Highest-value item here. Unrouted — needs an owner or builder decision.**
2. **Mechanized depot fill/empty carry no `before`/`after`** — `depot_read` guards on
   `IsKindOf(obj,"StorageDepot")` and `MechanizedDepot` is not one. ⇒ **99** (owner's
   word). ⛔ The FEATURE WORKS; only the evidence is missing. A scalar fallback is
   already committed (`8e25f6b`) and correct but **unreachable** — the repair is the
   GUARD, not another fallback. `EF-102` amended with the third family.
3. **Editor hint renders white** (`command`, `trigger_sol`) — the hint draws through its
   own `HintColor` (`XTextEditor.lua:38`, used `:1267`), untouched by `TextColor`. ⇒ **99**
   (owner's word: *"geniunely minor and not something you need to hunt for endlessly"*).
   ⚠️ **Corroboration found later:** a watch was configured as `field=command` — the
   unreadable placeholder submitted as a value. The cosmetic defect caused a real
   misconfiguration.
4. **A field watch arms on a nonexistent field** with `baseline=nil` and can never fire.
   Same shape as #2: a record reading `status=OK` while the thing it describes cannot
   work. ⇒ should refuse, naming the field.
5. **Three probe ERRORs STATE does not name** — `ClassicRockets`, `CohortHousing`,
   `NoHomeless`, all `attempt to call a nil value` on game methods
   (`UniversalRocket.lua:1894`, `Colonist.lua:3268`). Shape matches 1.1.0 API drift and is
   inconsistent with this sitting's UI-only edits. ⛔ **Cannot be proven pre-existing** —
   STATE says kit verdicts are predictions until the first `RunAll()`, so there is no
   baseline to diff. This may BE that first run.
6. `DomeFreeSpaceMismatch` FAIL — already flagged by 08 as needing triage. Unchanged.

⛔ **Expected failures, matched exactly** — `C47OpenFarmSeedBufferShape`, `LayoutTechLock`,
`AnomalyCaveInMap`, and the three retired `LanderCargoRatchet`/`DroneUnreachableForever`/
`AutoExportPriority`. Six of ten non-passing probes are the names STATE already lists.

## OWNER-ROUTED

All five UI rulings and the defect-7 ruling are consolidated into **ck183** — dock to the
right corner, status at a glance, quiet as an indicator, console auto-open off, eligibility
off the strip (recommendation implemented, reversible), font 16 + wrap.

⚖️ **UNRULED and NOT decided here — does this RunAll discharge ck144 (a)?** 08b is explicit
that it is unruled, and the **stale preflight is a reason for caution**. Recorded as *run,
under a stale attestation*; the call is the owner's.

## DRIFT for 99

- The sitting **built**, against its own scope fence, under owner licence (top of file).
- Evidence spans **four boots**, not one.
- The **probe picker sort (`2c3d05c`) has NO play witness** — built after the last boot.
  The owner asked explicitly that 99 audit it. ⛔ `SMRTest.order` is the RUN order; verify
  only `:328`/`:357` take the sorted copy and that `probe_items` copies before sorting.
- `EF-102` was **amended**, not just cited: its own FIX SHAPE bullet said "guard on
  `StorageDepot`", which is what caused the failed repair. The true common ancestor is
  `ResourceStockpileBase`.
- Item 9's trigger half and `PLAYTEST_HELP`'s accuracy are the only things this sitting
  leaves genuinely open.
