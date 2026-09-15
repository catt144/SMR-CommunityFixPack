# smrtk 99 — the terminal adversarial audit

2026-09-14. Link 99 of `prompts/smrtk/`, executed on **Fable 5.1** (R-G), session
`smr-bugfixpack-3d`, fresh context. Audited at pack `459bbe4` (HEAD when the reads
closed) and TestKit `2c3d05c`; game build **24995074** (1.1.0.403908). No game ran
in this audit; every claim below is a re-derivation from the archived logs, the
TestKit source, the installed `ModTools\Src`, or `git`. Where the brief asked for a
live measurement this audit could not take, the item says **NOT RUN**.

## Verdict — SHIP WITH CHANGES

**"Ship" means the owner uses it. The TestKit never uploads (H-04 binds the word).**

Nothing found blocks use. Requirement (A)'s taint half holds by measurement across
all three sittings; its eligibility half is unmeasurable from inside the mod and is
adjudicated below by closed source enumeration, never as an observed PASS.
Requirement (B) holds on every archived toolkit line. The changes are small, listed
in §11 with an owner and a TAKEABLE-WHEN each, and none needs a boot of its own.

## 1 · Inbox audit — did every outbox land where it said, in one commit?

| link | close-out commit | successor inbox | 99 inbox | README row struck | one commit |
|---|---|---|---|---|---|
| 01 | `320d359` | 02 ✓ | ✓ | ✓ | ✓ |
| 02 | `44a3585` | ✗ | ✗ | ✓ | ✗ — repaired by the orchestrator in `c74855b` (03A + 99 appended, separate commit) |
| 03A | `966e0c5` | 03B ✓ | ✓ | ✓ | ✓ (payloads consumed in the same commit) |
| 03B | `4624ec2` | 07 ✓ | ✓ | ✓ | ✓ |
| 03C | `cf7263c` | 07 ✓ | ✓ | ✓ | ✓ |
| 07 | `72ed20e` | 08 ✓ | ✓ | ✓ | ✓ |
| 08 | `d0fbd11` | 08b (new file) ✓ | **✗ never appended** | ✓ | ✗ |
| 09 | `86f0006` | 08b ✓ | ✓ | ✓ | ✓ |
| 08b | `046ba6f` | — | ✓ (+ `ab1c2d9`, `01beba3` routed items) | ✓ | ✓ |

**Finding I-1.** 08's outbox to 99 exists only at `reports/SMRTK_FULL_SITTING.md`
"Outbox to 99" (eight items) and was never appended to this prompt. Read there and
adjudicated here: (1) taint re-derived from the log, §3; (2) RunAll vs ck144 (a) is
**ck184 (b)**, unruled; (3) both refuted STATE lines are gone — the depot line became
`EF-102`, `GhostFarmOxygen` no longer appears in STATE; (4) `DomeFreeSpaceMismatch`
is now named in STATE's owed list; (5) defect 22 (`spawn_*` REFUSED after mutation)
was repaired by 09 and **witnessed** in 08b item 6; (6) 08's three attendee drifts
were weighed — the `[mod]` de-dup trap did not recur here (this audit de-duplicates
by `id=`); (7) the surface ruling was built and ruled again in ck183; (8) 08's prompt
was retired by `d0fbd11`, as the orchestrator's call. Nothing in it changes the verdict.

## 2 · Owed-work sweep — every routed item, its owner, its TAKEABLE-WHEN

| # | item | owner | TAKEABLE-WHEN |
|---|---|---|---|
| O-1 | stale preflight attestation accepted (08b) | owner — **ck184 (a)** | now; recommendation in §11 C-4 |
| O-2 | does 08b's RunAll discharge ck144 (a) | owner — **ck184 (b)** | now |
| O-3 | text status bar vs the icon ck175 asked for | owner — **ck184 (c)** | now |
| O-4 | mechanized depot guard | 99 — **verdict §8** | a builder applies one token, next Code link with `Mars.exe` closed |
| O-5 | white editor text | 99 — **mechanism §9** | a builder adds one property, same link as O-4 |
| O-6 | field watch arms on a field the object lacks (`baseline=nil`, 08b #4) | builder | same link |
| O-7 | `00_TestCore.lua:519` `ConsoleSetEnabled`-first bootstrap (03B D2) | builder — **no link owned it until now** | same link; 08b's auto-open-off removed the visible half |
| O-8 | `EF-096` line corrections (03B, 07 item 6) | **99 — amended in this commit** | done |
| O-9 | TestKit README page table describes the pre-09 surface | **99 — corrected in this commit** | done |
| O-10 | PLAYTEST_HELP steps 2/7/9 describe the pre-09 surface | **99 — corrected in this commit** (ck182 may dissolve the file later) | done |
| O-11 | 08b item 9 (watch trigger) NOT RUN | first slot-served sitting | kickoff §12 |
| O-12 | three probe ERRORs + `DomeFreeSpaceMismatch` | probe maintenance, named in STATE | ck144 (a) boot |
| O-13 | Stamper | ⛔ parked, `FUTURE_IDEAS.md` entry 5, **not agent-tracked** — not counted | — |

Nothing else routed by 01–09 or 08b lives only in a session's memory: ck175 carries
the 03B six-item append and the item-1 ruling, ck183 the design half, ck184 the three
08b leftovers, and the reports carry the rest.

## 3 · The taint invariant, re-derived

**3.1 Rule 6, with the presence side.**
`grep -n "NetSyncEvent\|LogCheatUsed" Code/7*_SMRTK*.lua Code/80_AgentSlots.lua`
→ **0 lines** over 8 files (3,042 lines). Presence: the same grep on the installed
`Data/CheatDef.lua` → **26 lines**, of which **13** are call lines
(`grep -cE '\bNetSyncEvent\s*\('`). `grep -rn LogCheatUsed <Src> | wc -l` → **4**
(the definition at `Network.lua:242` plus its three callers at `Network.lua:212`,
`:234` and `ClassDef-PresetDefs.generated.lua:947`). Extended sweep for the rule-10
spellings (`NetSyncEvents`, `:run()`, `Platform.cheats`, `BuildingInfopanelCheats`,
`ConsoleSetEnabled`, `AccountStorage`, `AreCheatsEnabled`) → one line,
`80_AgentSlots.lua:57`, a **read** of `Platform.cheats` into a DUMP field. Allowed.

**3.2 The closed set of taint entry points, enumerated tree-wide.** Every
`NetSyncEvent("Cheat"|"ObjCheat"|"CheatDef", …)` call site in the installed source:
**18** — `CheatDef:Exec` (`:909`), the **13** preset `run` bodies `EF-098` names
(`CheatDef.lua:154–294, :711, :725`), vanilla's infopanel button (`Infopanel.lua:49`),
two DevTools lightmodel shortcuts, and an animation-editor test. Scripted over the
whole tree: 28 sync/log call sites in 14 enclosing functions, and **no function the
toolkit dispatches encloses one** (126 toolkit-referenced leaf names checked by
enclosing-function name). The toolkit never calls `def:run`, `CheatDef:Exec`, or
vanilla's `XAction`; it calls `obj[method](obj)` (`73:97`, `73:227`) and bare leaf
globals looked up with `rawget(_G, leaf)` (`72:51`).

**3.3 Every registered action's `run`, read line by line.** All eight files were
read whole (`70`–`76`, `80`); 03B's declared gaps (`71`'s rendering path, 25 of the
P3–P5 actions) are closed by this read. World (`72`): `CheatStopDisaster`,
`CheatDustStorm`/`CheatDustDevil`/`CheatColdWave`/`CheatTriggerMarsquake`/
`CheatRainsDisaster` via `rawget`, `MeteorsDisaster` direct with a cursor position
(`EF-098`'s route), `CheatTriggerUndergroundCaveIn`/`…Marsquake`, `SetGameSpeed`,
`o:CheatCleanAndFix()`/`o:SetMalfunction()`, `CheatCompleteAllConstructions`/
`…WiresAndPipes`, `o:AddFlightTime`+`Wakeup`, `o:CheatFill()`, `CheatSpawnNColonists`,
`CheatGenerateApplicants`, `CheatAddFunding`, `UIPlayer:GainTechPoint`/`UIResearch`,
`CheatUnlockAllBuildings`, `OpenAllDomes`/`CloseAllDomes`/`UnpinAll`, `AddTrait`/
`RemoveTrait` — every one a leaf. Selected (`73`): 22 curated names and **77 More
names (10 async)** in `more_policy`, dispatched only after `member()` and
`allowed_more()`; the walk mirrors `CreateCheatActions` (`Infopanel.lua:22–40`) but
replaces its `NetSyncEvent("ObjCheat", …)` with the direct call. Agent (`74`),
Saves (`75`), Kit (`76`) and the 08 slots (`80`) call no cheat leaf at all except
`80:232`'s `selected_fill` through the dispatcher.

**3.4 `CheatsUsed` reads, located by line in the archived logs.**
- `smrtk02_…19.58.32`: `:260` `used=false` (id 15), `:289` `used=false` (id 23),
  `:301` **`ObjCheat CheatFill`** — the vanilla wrapper fired on purpose in the
  scratch save — `:303` `used=true` (id 26), **`:305` `SMRTK_TAINT action=taint_read
  used=true`** — the assert fired. That is the control's RED. `smrtk02_…20.40.33`
  `:258` `SMRTK_SCRATCH_DISCARDED name=SMRTK_SCRATCH_TAINTED`; on disk today the
  saves folder holds no `SMRTK_SCRATCH_*` file (ls, 2026-09-14).
- `smrtk08_…11.42.49`: `:448` `used=false` (id 82), `:579` (id 137), `:583` DUMP
  `taint_used=false platform_cheats=nil`, `:2112` `used=false` (id 578), `:2122`
  DUMP `cheats_count=0 cheats_used=""` — `CheatsUsed` enumerated by name, empty,
  after 490 OK dispatches.
- `smrtk08b_…19.01.16` `:309`, `:320` `used=false`; `smrtk08b_…19.08.05` `:492`
  `used=false` (id 114) after the 19-leaf sample (`CheatCleanAndFix` 7, `CheatFill`
  4, `CheatMalfunction` 3, `CheatEmpty` 3, `CheatLightningStrike` 1, `CheatAddDust`
  1 — counted from `method=` de-duplicated by id).
- ⚠️ **`smrtk08b_…20.03.09` carries NO `TAINT_READ`** — the World boot
  (`malfunction_all` over 1,299 buildings, `fix_all` ×4, four meteor fires,
  `rocket_arrive`, `spawn_colonists_10`, `complete_constructions`, RunAll) ended
  without the explicit read. Its negative rests on the **per-dispatch assert**
  (`70:202` runs after every dispatch): 116 dispatches (110 OK, 6 REFUSED), **zero**
  `SMRTK_TAINT` and zero `TAINT_UNAVAILABLE` lines, and the assert path is proven
  live by 02 `:305`. Sound, but a protocol gap: **a sitting boot should end with the
  read**, so the negative is a sample and not an absence.

**3.5 The eligibility read, adjudicated against requirement (A).** 08's end: `:2118`
`SMRTK_ELIGIBILITY reason=UNAVAILABLE:sandbox`; 08b `19.01.16:312`, `19.08.05:502`
the same. `CanUnlockAchievement = true` sits in `ModEnvBlacklist` (`Mod.lua:1403`)
and the reasons message in `ModMsgBlacklist`, so **no toolkit read can observe
eligibility**, and the panel's honest `UNAVAILABLE:sandbox` is the correct output.
What CAN be established is the reason set, because it is closed:
`grep -rn "OnMsg.UnableToUnlockAchievementReasons" <Src>` → **5 handlers** — cheats
used (`Network.lua:251`), modding tools active (`GedModEditor.lua:23`), a game rule
(`Lua/GameRules.lua:154` **and** `CommonLua/Features/GameRules.lua:75` — `EF-095`
says four; it is five, two of them game-rule handlers), and the tutorial
(`init.lua:44`). The toolkit persistently touches only the first, and that one is
measured CLEAN. The second is **transient by construction** (`AreModdingToolsActive`
= a live GED window, `Mod.lua:146–148`) and the More `AsyncCheat` Inspect/Properties
buttons DO open such a window — the 03C/07 caveat "close the editor" stands.
⇒ **Ruling: (A) holds — the taint half by measurement, the eligibility half by
closed enumeration. It is NOT an observed eligibility PASS and no document may say
so.** The panel's CLEAN must keep reading as "no cheat taint", never "achievements
safe" (already the wording at `71:180–186`).

## 4 · The tag invariant

| log | lines containing `SMRTK` | lines shaped `[SMRTK] SMRTK_` | untagged |
|---|---|---|---|
| 02 `19.58.32` | 69 | 69 | 0 |
| 02 `20.40.33` | 196 | 193 | 3 — `SMRTK_NATIVE_PRINT_100%`, `SMRTK_NATIVE_CONSOLE_100%`, `SMRTK_TEE_WITNESS_100%`: the sitting's owner-typed console witnesses, not toolkit writes |
| 08 `11.42.49` | 844 | 844 | 0 |
| 08b ×4 | 70 / 60 / 176 / 211 | 70 / 60 / 176 / 211 | 0 |

Every record appears twice (file + console tap) except chrome verbs, once — the 08b
report's warning holds, and every count above is de-duplicated by `id=`.

**A total is not a set — reconciled.** 08's record ids run **1..582 with no gap**.
The panel's fire counters are persisted as `PROVENANCE actions=` on load. Counting
callback **attempts** exactly as `75:103` defines them (OK dispatches plus callback
refusals, excluding pre-check refusals and `NOT_BUILT`) strictly before `SAVE`
id 439 gives **363**; the two loads of that save report **`actions=363`** (ids 456
and 485). Exact. A naive OK-only count gives 361; the difference is two callback
refusals (`run_all` "not provisioned", `selected_more` "selection changed"), which
the counter is documented to include. Arm/disarm balance per action, per log: 08 —
`logger_DustDevils` 1/1, `print_tee` 2/2, `meteor_single` 2/2, `quiet` 2/2, `slot_4`
5/5, `smrtk08_break` 1/1, `run_until` 1/1, `watch_selected_field` 3/3,
`trigger_rocket` 1/1; 08b — `slot_4` 3/3, four meteor kinds 5/5, `trigger_sol` 3/3,
`run_until` 2/2, `watch_selected_field` 1/1. **Zero survivors in every boot.**

## 5 · The idle invariant (rule 9)

**Source enumeration (this audit).** Writes to a vanilla FUNCTION slot in the eight
files: `_G.print = tee` (`70:307`, print-tee arm) restored at `70:310`; `_G[name] =
wrapper` for the seven quiet routes (`72:164`) restored at `72:170` **only if the
slot still holds our wrapper**. Both are toggles, off by default, logged ARM/DISARM,
and every armed thing auto-disarms on `PreLoadGame`/`SavegameSaved`/`SaveGameStart`/
`LoadGame`/`ChangeMap`/`CurrentMapChange`/`DoneGame` (`70:367–380`). No top-level
`function Name(` in any toolkit file; 23 distinct `OnMsg` listeners, all listen-only.
Two idle writes to vanilla **tables** (not functions): `ConsoleEnabled = true`
(`70:364`, mandated by rule 10) and a `TextStyles.SMRTKControls` preset registered
at first button build (`71:46–50`). UI hosts gain children (an `XAction`, an
`InfopanelSection`, a HUD button); nothing is replaced. ⇒ **idle = 0 replaced
vanilla functions**, by source.

**Live arm → count → disarm → count 0: NOT RUN by this audit** (no game). The logs
witness the pairs (§4) and 02 witnessed `TEE_RESTORE` ×3, but no boot enumerated
replaced functions `SourceOf`-style, because **the toolkit has no such button** —
see C-8. The 09 desk instrument re-ran at HEAD: PASS, `NO SYNC 0`, `NO BARE PRINT 0`,
`ONE LOGGER 1`, `PRESENCE 26`.

## 6 · Falsifiers — each RED, by line

- **Session-id guard refusing a foreign slot:** 08 `:1842` id 475 `SMRTK_LOAD
  action=load_A status=REFUSED reason="foreign session: 1789400587:…"`, then `:1911`
  id 490 `LOAD_OVERRIDE … override=true status=OK`. The nonce regenerates per
  process: the 08 process was `1789400587:3032022245:…`; the 08b `20.03.09` boot's
  preflight DUMP (`:530`) carries `session=1789430606:3062041685:…`.
- **A stamp skipping an unbuildable hex:** ⛔ VOID — the Stamper is cut.
- **Auto-disarm after a load:** 08 `:1744` id 447 `DISARM action=slot_4
  reason=ChangeMap` (the load path); 08b `20.03.09:495–501` three
  `DISARM … reason=SaveGameStart`.
- **`SMRTK_TAINT` on a deliberate sync call in a scratch save, then the save
  deleted:** 02 `19.58.32:301–316` and `20.40.33:258`; absent from disk (§3.4).

## 7 · Docs vs built

- **PLAYTEST_HELP buttons exist** (Fill, Empty, Delete, Destroy (blow up), Run all
  probes, Ctrl-Shift-F11, F9, "Kit → Open console" = the `Console` button). Three
  lines described the pre-09 surface and are corrected in this commit: step 2
  ("Click the SMR icon on the game's dock **for its menus**" — there are no menus;
  the button toggles the panel, ck183 ruling), step 7 (triggers are on **Run**), step
  9 (field watches are on **Selected/Run**), and the **Run** page was missing from
  the page walk. ck182 may dissolve the file; until it does, it must not misdescribe.
- **TestKit README page table** listed six pages; the panel registers **seven**
  (`71:331`: Sitting, Run, Selected, Agent, World, Saves, Kit) and the table's "SMR
  dock icon for native menus" sentence was false. Corrected in this commit. The
  toolkit **file map** ↔ `metadata.lua` `code` list: all nine toolkit rows listed
  (H-10 ✓); the chain README's layout table ✓ including the struck `77`.
- `perma/SMRTK_SLOTS.md` has its row (`prompts/README.md:33`) ✓.
- **08b's probe picker (owner ask, no play witness).** `SMRTest.order` is read
  unsorted by `orderkey` (`76:37`), the hidden-verdict sweep (`:325`) and the verdict
  rows (`:359`); only the two combo sites (`:328`, `:357`) take `probe_items()`, which
  copies element-by-element (`:47–49`) **before** `table.sort` (`:50`). **Run order
  unchanged, by source.** Rendering: NOT RUN (no boot since `2c3d05c`); the aliascheck
  WARNs it adds are the same `SMRTest.order/probes/last` false positives 03A/09
  recorded.

## 8 · Routed deliverable — the mechanized depot readout

**Verdict: WORTH THE GUARD CHANGE.** One token at `73:58`: `"StorageDepot"` →
`"ResourceStockpileBase"`. It activates the scalar fallback already committed at
`73:76–79` (TestKit `8e25f6b`), which today is dead code because the guard above it
rejects every `MechanizedDepot`. Safety of the wider guard: `depot_read` is called
only from the fill/empty branch (`73:92–93`, `:100`) and only after `method_for`
found `CheatFill`/`CheatEmpty` on the object (`:87–88`), so no object without those
leaves can reach it; `MechanizedDepot` has no `GetStoredAmount` (`EF-102`), so it
takes the scalar branch by construction. **No other toolkit code guards on
`StorageDepot`**: `72:314` is vanilla's own `FillAllStorages` recipe and names
`MechanizedDepot` explicitly (correct), `80:268–269` counts by class on purpose.
`EF-102`'s falsifier re-run: 11 / 22 / 7 files — holds. ⛔ Not a second fallback.

## 9 · Routed deliverable — the white editor text, in one line

**Mechanism:** `XFontControl:SetTextStyle` (`XControl.lua:432–438`) copies the
style's `TextColor` into the control, and `ConsoleLog`'s `TextColor` is `-1` — white
(`CommonLua/Data/TextStyle.lua:87`) — over `XTextEditor`'s default light `Background`
(`XTextEditor.lua:47`); properties apply in declaration order
(`PropertyObject.lua:928–937`), `TextStyle` before `TextColor`, so an editor that
sets its own `TextColor` wins (that is why `491` went dark in `74`'s editor) and one
that does not is white-on-light.

**The `command` field is that editor, and it is REAL TEXT, not a hint:**
`76:292–294` creates it with `TextStyle="ConsoleLog"` and no `TextColor`, then
`SetText(K.field)` with `K.field = "command"` (`76:3`). `74`'s `editor()` sets both
colours (`:346–347`); its hint path (`XTextEditor.lua:1267`, `self.HintColor`) is
untouched by the style, so **`HintColor` at `74:347` is KEEP** — correct on paper,
harmless. `trigger_sol` (`74:410`) is also real text in the fixed editor; if it still
reads white after `174a601`, that is not explained by this read and one boot settles
it. `72:431`'s `editor` local appears unused. **Fix (C-3):** give `76:292` the same
`TextColor`/`Background` pair or share `74`'s editor. Corroboration from 08b: a watch
was configured as `field=command` — the unreadable default submitted as a value.

## 10 · The 03A / 03B cross-vendor split, adjudicated

- **D1 (22 fixed names vs vanilla's 106).** 03B's frame — *an unstated gap in the
  headline deliverable*, not "built to spec" — was right on the evidence: 03A's
  DEPARTURES named neither the ratio nor the dropped `AsyncCheat` category. The owner
  ruled "extend before 08"; 03C built the metatable walk on P2's route
  (`73:227` is the same `obj[method](obj)` shape as `73:97`), so ck175's rule-5a
  condition ("must ride P2's proven route") **holds**; 09 then pruned by traced body
  to 77 More / 10 async with named caveats. **Closed.** 08b item 5 dispatched real
  More leaves in play.
- **Spike before payloads:** `reports/SMRTK_UI_HOOKS.md` first committed
  2026-09-13 22:23:11; the payload files first committed 22:42–22:55 (TestKit) and
  their reports 23:10 ✓. `payloads/` consumed in 03A's close-out `966e0c5` ✓.
- **D2 (`00_TestCore` console bootstrap: retire vs invert).** 03B's *invert, not
  retire* is right and **still open**: `00_TestCore.lua:519` still calls
  `ConsoleSetEnabled(true)` first. 08b's `f58b3b2` turned the auto-open OFF, which
  removed the pop-up; the `ShowConsoleLog` overlay at load remains the residual
  symptom, cleared by F9. Routed as O-7 / C-6 with an owner.
- **03B's `EF-096` corrections, verified in one command each:** `ModEnvBlacklist`
  spans `Mod.lua:1280–1441` (not 1416); `CanUnlockAchievement = true` at `:1403`;
  `os = true` at `:1438`; `env.os = { time = os.time }` is rawset at **`:1620`**
  (03B said 1618). Amended in `EF-096` this commit.
- **Instrument caution:** `SMRTK_FANOUT_GATES.py` was not falsified against a known-
  bad tree by anyone. This audit's independent grep agrees with it, and the presence
  side (26 lines) proves the same regex matches real sync lines.

## 11 · SHIP WITH CHANGES — the list

| # | change | owner | TAKEABLE-WHEN |
|---|---|---|---|
| C-1 | `73:58` guard → `ResourceStockpileBase` (§8) | builder, next Code link, `Mars.exe` closed | now |
| C-2 | end every sitting boot with `TAINT_READ` + `ELIGIBILITY` (§3.4) | `perma/SMRTK_SLOTS.md` — **added this commit** | done |
| C-3 | `76:292` editor gets `TextColor`/`Background` (§9) | builder, same link as C-1 | now |
| C-4 | preflight staleness: (a) `perma/SMRTK_SLOTS.md` now says the sweep is re-run after **every** TestKit or pack commit and the slot rewritten before boot — **added this commit**; (b) recommendation for ck184 (a): the gate at `76:59` cannot see the tree's HEAD, but it can refuse a `checked_at` older than the current boot (`os.time` is open, `Mod.lua:1620`) — a builder's one-condition change | owner rules (a) is enough or (b) is built — ck184 (a) | now |
| C-5 | `74:249–258` field watch refuses a field the object does not have (08b #4) | builder, same link | now |
| C-6 | `00_TestCore.lua:519` invert to plain assignment first, `ConsoleSetEnabled` as fallback (D2) | builder, same link | now |
| C-7 | docs: TestKit README table + PLAYTEST_HELP steps (§7) | **99 — this commit** | done |
| C-8 | suggestion, not owed: a Kit button that enumerates replaced vanilla functions (`SourceOf` over the quiet routes and `print`) so the idle invariant is a button, not a source read | builder, when convenient | — |

C-1, C-3, C-5, C-6 are one Code link of perhaps thirty lines; none needs a boot of
its own, and the first slot-served sitting (§12) witnesses all four.

## 12 · Kickoff — the first real sitting the panel serves

**Yes, the owed ck144 (a) boot is the natural candidate**, with the RunAll half
subject to ck184 (b). Fire `perma/SMRTK_SLOTS.md` against it: the ck144 (a) recipes
(A3 / A10 / A5 c2 / A9 c4–c5 / F117's station recipe) as slots, a **fresh** preflight
for that tree, the 08b item-9 watch trigger on a field the object has, and C-1/C-3/
C-5/C-6 witnessed on the way. Nothing else is queued.

## What this audit does NOT claim

No play by this audit. No eligibility PASS. Nothing about the no-taint property on
any build other than 24995074. The probe picker's rendering. 08b item 9's trigger.
The `trigger_sol` field's colour after `174a601`.

## DRIFT (mine)

- Three heredoc-fed regexes lost their backslashes silently (the rig hazard,
  re-triggered) — rewritten through the Write tool before any number was read.
- A `cd` inside a compound command drifted the shell into `archive/logs/`, and one
  batch of reads failed on relative paths before I noticed.
- My first fires-vs-provenance count (361) used "OK only"; the code's own definition
  of an attempt (`75:103`) reconciled it to 363 exactly. The instrument was wrong
  before the toolkit was.
- Started the write-up before the owner's read-only hold; everything was drafted in
  the scratchpad and landed only after the all-clear.
