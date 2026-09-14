# SMRTK full sitting — smrtk 08

**Status: PREPARED, NOT YET RUN.** The attendee's preparation is complete and
the gates pass; the owner's boot has not happened. Nothing below the
"Preparation" section is a play result, and no status moves until the sitting
runs. Attendee: Claude (rule 22 — the non-building vendor scores the builder's
predictions). Brief `prompts/smrtk/08_FULL_SITTING_owner.md`; predictions
`reports/SMRTK_FULL_SITTING_PREDICTIONS.md`, classes 1–18.

## Preparation — 2026-09-14

### HEADs and gates

| | |
|---|---|
| pack HEAD at the desk sweep | `3ae67dea1e4fe3355dc1bb905254f8649f4b54fd` |
| TestKit HEAD at the desk sweep | `c886fb7049cf50a149938f9515eae78d039af33b` |
| TestKit runtime the docs describe | `f093e3b` (README successor `c886fb7`) |
| slots commit (TestKit) | `8a576a5` — `Code/80_AgentSlots.lua` |
| `Mars.exe` at the time of the `Code/` write | not running (`tasklist`) |

Gates, all run after the final edit to `80_AgentSlots.lua`:

```text
python tools/parsecheck.py --dir C:/Dev/SMR-BugFixPack-TestKit/Code --quiet
PARSE: 34 file(s) in ..\SMR-BugFixPack-TestKit\Code, 0 error(s) [Lua 5.5]   exit 0

rule 6:  rg -n 'NetSyncEvent|LogCheatUsed' .../Code -g '7*_SMRTK*.lua' -g '80_AgentSlots.lua'
         (no output)  exit 1
rule 6 presence side: rg -c 'NetSyncEvent|LogCheatUsed' ModTools/Src/Data/CheatDef.lua
         26           exit 0
rule 7:  rg -n '^\s*print\(' (same file set)
         (no output)  exit 1

python tools/doccheck.py → GREEN
```

**⚠️ The HEADs above are the sweep-time HEADs, which are the parents of the
slots commit itself.** The sweep ran against the working tree *including* the
final `80_AgentSlots.lua`, so it covered the code that will boot; the only
difference between the embedded HEADs and the boot-time HEADs is my own commit
of that same file. Naming the post-commit HEAD would require a commit made
after it, which does not terminate. If a **peer** commits to either tree before
the owner boots, the evidence is stale and slot 2 must be re-swept and rebuilt
before any probe runs.

Doccheck WARNs, verbatim (all pre-existing; none introduced here):

```text
STATE + STUBS: STATE.md 12504 bytes (warn 15360 TEMPORARY, hard 18432, line 200); 3 stubs present and pointing
MARKER INTEGRITY: 88 on disk, 88 parsed; WARN
  warn duplicate ck:144 at lines 2733, 2807 (agree)
    smr-bug-library           3622 B  ⚠ over the 3072 B target
    smr-orientation           3248 B  ⚠ over the 3072 B target
TESTKIT TREE: 1 uncommitted change(s) — report-only  [WARN  M Code/80_AgentSlots.lua, since committed]
ALIASCHECK: 9 finding(s) (report-only) — SMRTest.order/probes/last "defined by no kit file", 76_SMRTK_Kit.lua
  (the 19 frozen index-row status warns listed in the predictions' close-out are unchanged)
```

### The slots, as bound

`Code/80_AgentSlots.lua` at TestKit `8a576a5`. Every leg is MARK → set up →
act → DUMP → MARK, every dispatch result is checked, no leg arms at mod load
(`SMRTK_SLOTS armed_at_load=0`), and refusals are `false, reason`.

| slot | label | what it does |
|---|---|---|
| 1 | Console and status | brackets `console_control` + `taint_read` + `eligibility`; one attributed DUMP carrying all three plus `ConsoleEnabled`, `Platform.cheats`, arms, errors, session/sitting/build/map/sol |
| 2 | Probe preflight | embeds the desk sweep verbatim; reads session/sitting/`LuaRevision` live at invocation and attests through `SMRTK.ProbePreflight` |
| 3 | Check after load | read-only: arms, pins, click owner, stamper target lifecycle + layouts held, loaded provenance vs current session, attestation state, map/sol/errors |
| 4 | Read map click | armed shared `on_click` reader, `once_click=true`, explicit `on_disarm` cleanup, `mutation=none` on every record |
| 5 | Short breakpoint | arms `smrtk08_break` (registered disarmed at load; target `GameTime()+5000`, predicate read-only, effects mark+sound, **`pause=false`**) then arms `run_until` with that id |
| 6 | Dump selected | checked `dump_selected` → scalar state → `selected_fill` **with the expected-object guard** → scalar state → `dump_selected`, bracketed by two MARKs |
| Scratch | Read sitting | sol/map/error delta **plus the fixture-fitness census** (below) |

Two things are worth naming because they are easy to get wrong:

- **Slot 5's trigger does not pause.** `pause=false` is deliberate: `run_until`
  watches for the firing from a *game-time* poll, so a trigger that stopped the
  clock itself would freeze the poll that is watching it. `run_until` owns the
  pause. Block 8 must still restore Normal speed afterwards — `run_until`'s arm
  sets ultra.
- **Slot 2 assembles its sweep token** rather than writing it whole, for the
  same reason `76_SMRTK_Kit.lua:40` does: a literal would make
  `80_AgentSlots.lua` its own probe hit and the sweep would never come back
  clean again.

### The desk stale-probe sweep, as embedded in slot 2

```text
command : grep -rln "<token>" Code/ ../SMR-BugFixPack-TestKit/Code/   (run from the pack repo root)
exit    : 1
stdout  : (empty)
hits    : none      needed: none
scope   : 47 pack Code files + 34 TestKit Code files
```

The zero reading is a **sample, not a silence**: the same grep against a
scratch file containing the token returned that file and exit 0, so the
instrument fires when there is something to find. `doccheck` agrees from its
own code path — `TEMPORARY SWEEP: 0 hit(s) in Code/ + TestKit Code/`.

⛔ **76 expires the attestation on every load and map change.** The script has
three load transitions (blocks 10, 11, 15), so **slot 2 must be pressed again
after each one** before any probe runs. Slot 3 reports `attestation=expired`
whenever it has lapsed.

### Desk verification of the slots

`reports/SMRTK_SLOTS08_DESK.py` — lupa, shimmed native services in the style of
`SMRTK_P5_DESK.py`, loading the real `70`/`74`/`75`/`76`/`80`. It writes no
code and launches no game. **46 legs PASS**, covering: all seven slots bind and
nothing is armed at load; slot 2's embedded evidence is accepted and the
`run_all` gate refuses by name without it; a load expires it; slot 5 arms both
and the trigger fires without pausing, auto-disarming; slot 4 fires once and
releases its click target, and right-click cancels; slot 6 brackets a mutation
and refuses cleanly on an unsupported object; slot 3 and Scratch are read-only;
every emitted line carries the `[SMRTK] SMRTK_` tag; no TAINT, no ERROR, zero
arms left.

**The harness was falsified before its PASS was believed** — redirected at
one-guard-reverted copies of `80`:

| reverted guard | leg that must fail | result |
|---|---|---|
| slot 5's cleanup `T.Disarm("smrtk08_break", …)` on a run-until refusal | "breakpoint NOT left armed" | **FAILED**, as required |
| slot 2's assembled sweep token changed by one word | slot 2 accepts the evidence | **FAILED** (8 legs), as required |

⛔ **What this desk does NOT establish:** anything about the game. Stubs stand
in for `72`'s `run_until` and `73`'s `selected_fill` (each exercised in both its
accepting and its refusing form, since a stub for something that can refuse is
itself a behaviour change). Native fit, GameInit, dome membership, grid
connectivity, screenshot files and every button class in the predictions remain
entirely owed to the owner's boot.

### Fixture

`SMRTK08 Fixture Sol 490.savegame.sav`, present in
`C:\Users\stkot\Saved Games\Surviving Mars Relaunched\<id>\`, 38,643,956 B,
dated 2026-09-14 10:33. Chosen and measured at pack `3ae67de`: the C92
reporter's Sol 490 colony, 1.1.0.403908, `orig_lua_revision` 403908, Japan,
`active_mods = {}`, `platform` table with no `cheats` key, `CheatsUsed` read
**scalar / 0 method names** from disk against a positive control that read
**TABLE / 20 method names**. That reading is inherited, not re-derived here.
⛔ Owner instruction: take an immediate manual save on load, and load only this
copy — never the other three byte-identical copies.

**The one thing preparation could NOT settle: the colony's object inventory.**
The brief hands the attendee "provision what is missing, or record that leg NOT
RUN by name", and neither half is available at a desk — it is a stranger's
colony, it can only be inspected by loading it, and loading it is the owner's
act. Reading it from disk does not work either: the skeleton sitting already
measured that class names in a decoded save come from the interned
template/class table, **not** from instances, so a class-name hit proves
nothing about what the colony actually holds.

So the check was **built into the sitting instead of guessed at**: the Scratch
slot answers it in one read-only press at block 1, using for the rocket the
*exact* predicate `72`'s `rocket_arrive` will apply, not a weaker one —

```text
sol · map · errors · errors_since_mark · buildings · colonists · drones ·
constructions · depots_universal · depots_mechanized · domes · drone_hubs ·
rockets · rockets_ready · rocket_detail (per rocket: class(handle):command:READY|not-ready)
```

⛔ **Grid patches (cable/pipe) are deliberately not counted.** No colony-wide
enumeration of grid elements exists in the installed source that I could find,
and inventing one would be worse than admitting the gap: they stay an on-screen
check by the owner at block 15.

⇒ **Any requirement that census reports as zero makes its block NOT RUN by
name.** The most likely casualty is **block 12 (rocket landing)**, which needs
a universal rocket already travelling to our colony and sitting in its
`SleepFlight` wait — a stranger's save may simply not have one. The brief
already anticipates this: the custom trigger in block 8 is the required firing
even if the landing is unavailable.

## The sitting — RAN 2026-09-14, one boot, owner at the keyboard

Boot `Mars.exe-20260914-11.42.49-6a91a190`, started 11:42:49 local, eleven
minutes after the slots were final — so this process loaded them
(`SMRTK_SLOTS armed_at_load=0`, id=2). Attendee scored each block from the file
log; the owner supplied every screen witness.

**Archive.** Complete boot log `archive/logs/smrtk08_Mars.exe-20260914-11.42.49-6a91a190.log`
(242,117 B, sha256 `2fda1dcbc925fb181e5b910d…`). Owner's clipboard extract
`archive/logs/smrtk08_clipboard_partial.txt` (54,981 B). ⚠️ The clipboard copy
is **partial by design** — the final `SMRTK_COPY from=92 lines=300
truncated=true` hit the 300-record ring against 844 records produced. 07
predicted this; **the boot log is the authoritative record, not the clipboard.**
Screenshot `C:/Dev/SMR-ScreenCaptures/SMRTK_0001.png`, verified independently on
disk (19,170,902 B, valid PNG header, 3840×2160) rather than trusted from the
action's "native accepted".

### Fixture as actually used

⛔ **The fixture's file was renamed but its metadata was not.** The prepared copy
carries `savename = "Autosave Sol 490.savegame.sav"`, `displayname = "Autosave
Sol 490"` and `autosave = true`, so the game listed it under the ORIGINAL name
and the owner could not find "SMRTK08 Fixture Sol 490". Any future fixture prep
must rename the metadata or record the display name in the brief.
Verified byte-identical to the protected C92 original, sha256
`68d340ad0f1a2b13047034e21a7fc84199c66f069858f190be1e9f38d0ff9bb7`.

The owner loaded it, took an immediate manual save as **`SMRTK_490`** and worked
from that copy — protecting the fixture and removing the autosave-rotation risk.
`SMRTK_490` verified from disk: `elapsed_sols 490`, `map BlankBig_04`,
`orig_lua_revision 403908`, and a live toolkit provenance block
(`smrtk = { actions = 2, session = "1789400587:…" }`).
⚠️ **Three mods active, not two**: `SMR_CommunityFixPack` v11,
`SMR_CommunityFixPackTestKit`, **and `SMR_CommunityOptInPack`**. The Opt-In pack
being live is a variable beyond the default module set; it is irrelevant to
taint but 99 should see it stated. No double mount (the `3787202810` seen on a
first read was the fix pack's own `steam_id` field, not a second copy — H-09 clear).

### Fixture census — the check preparation could not make

Scratch, pressed at block 1: **1147 buildings · 663 colonists · 939 drones ·
77 universal depots · 13 mechanised · 13 domes · 12 drone hubs · 0 constructions
· 8 rockets, 0 ready.** Rich enough for every block. Two gaps caught before they
wasted owner time:

- `constructions=0` ⇒ the completion sweeps would have passed vacuously. The
  owner placed scratch buildings and grid runs before block 7.
- `rockets_ready=0` ⇒ block 12 looked unrunnable. **The owner refused to accept
  that** ("there is no reason to leave things undone if they are doable and just
  needs a button press"), launched a rocket from Earth, and the block ran. The
  attendee's NOT RUN was premature; the owner's instinct was right.

### Per-block verdicts

| block | classes | verdict |
|---|---|---|
| 1 dock, status, navigation | 1, 2, 4 | **PASS** |
| 2 console control | 3 | **PASS** — `discriminates=true negative=false positive=true`, `platform_cheats=nil` |
| 3 probe gate + Kit views | 16, 17 | **PASS** — incl. the first `RunAll()` |
| 4 world, targeting, quiet, speed | 9, 10, 11 | **PASS** |
| 5 curated Selected rows | 5 | **PASS** |
| 6 Delete, Destroy, More | 6, 7, 8 | **PASS** |
| 7 spawn, traits, repair, completion | 9 | **PASS with two defects found** |
| 8 slots, click, note, trigger | 11, 12, 13 | **PASS** |
| 9 screenshot + clipboard | 2, 14 | **PASS** |
| 10 Save A + same-session load | 15 | **PASS** |
| 11 foreign-session guard + Override | 15 | **PASS** |
| 12 rocket transit + landing trigger | 9, 13 | **PASS** (ran after the owner provisioned a rocket) |
| 13–15 the three native stamps | 18 | ⛔ **BLOCKED — see defect 21** |
| 16 whole-sitting control + archive | 2, 4, 17 | **PASS** |

**NOT RUN, by name:** Research `research_all` / `unlock_buildings` (inspected,
legible, deliberately unfired per the brief) · "First error since mark"
(deliberately not provoked) · AsyncCheat `ClassHierarchy`, `ClipPlane`, `Gizmo`
(not required once Inspect passed; see defect 17) · all of class 18.

### ⭐ Requirement (A): no taint — PROVEN

```text
SMRTK_MARK        label=SMRTK08_END mark=811 status=OK
SMRTK_TAINT_READ  used=false status=OK
SMRTK_ELIGIBILITY reason=UNAVAILABLE:sandbox status=OK
SMRTK_DUMP        cheats_used="" cheats_count=0 arms=0 errors=0
```

`cheats_count=0` is the **`CheatsUsed` table enumerated by name**, not
`AreCheatsUsed()`. Across **844 records: 0 TAINT, 0 ERROR, 0 arms surviving.**
The sitting fired CheatKill, CheatDespawn, CheatDelete, CheatDestroy, CheatFill,
CheatEmpty, CheatMalfunction, CheatCleanAndFix, CheatAddDust,
CheatAddMaintenancePnts, CheatAddPrefab, CheatSpawnDrone, CheatUpgrade1,
`malfunction_all` over 1,305 buildings, trait add/remove, funding, tech points,
applicants, colonist spawns, a cold wave, a cursor-targeted meteor and a rocket
transit skip. Requirement (A) holds where it matters, not only on reads.

⚠️ **Eligibility remains `UNAVAILABLE:sandbox` (`EF-096`).** No-taint is
necessary, NOT proven sufficient. No eligibility claim is made.

### ⭐ The first `RunAll()` — owed and VOID since 09-09

```text
SMRTK_RUNALL counts={ERROR:6,FAIL:4,PASS:69,SKIP:18} status=OK
```

69+4+18+6 = **97**, reconciling exactly against the registered probe count.

**FAIL, by name** — `DomeFreeSpaceMismatch` · `LayoutTechLock` ·
`AnomalyCaveInMap` · `C47OpenFarmSeedBufferShape`.
**ERROR, by name** — `LanderCargoRatchet` · `DroneUnreachableForever` ·
`AutoExportPriority` (all `[retired]`) · `ClassicRockets` · `CohortHousing` ·
`NoHomeless`.

Against STATE's predicted set:
- **Confirmed**: C47OpenFarmSeedBufferShape, LayoutTechLock, AnomalyCaveInMap,
  and the three retired ERRORs.
- ⛔ **Refuted**: STATE lists `GhostFarmOxygen` as a FAIL. It is
  `SKIP GhostFarmOxygen [install] introspection unavailable (retail sandbox)`.
  **STATE's line needs correcting.**
- ⚠️ **Four unpredicted**: `DomeFreeSpaceMismatch` (FAIL) plus `ClassicRockets`,
  `CohortHousing`, `NoHomeless` (ERROR). The three ERRORs are stale-probe rot
  against 1.1.0 — nil `IsSpecialAutomode`, and nil `GetRadius` twice on the same
  line `Colonist.lua:3268`, so likely one stale helper not three problems.
- ⭐ **`DomeFreeSpaceMismatch` is candidate-defect material**: *"a residence
  whose power is out counts as zero free space — the dome reads as full for
  births and immigration while ChooseResidence keeps assigning colonists into
  it."* Coherent, found on a mature colony, predicted by nobody. Owed triage.

⚖️ **Not claimed:** whether this discharges STATE's ck144 (a) RunAll item. STATE
says 08 is a SEPARATE boot and not a combine; this ran on a stranger's Sol 490
colony with the Opt-In pack active. **Owner's or 99's ruling, not the attendee's.**

## Defects found — the reason the sitting was worth the owner's time

Every one is in `71`/`72`/`73`/`76`/`77` — build-link files, outside 08's fence
— so all are **routed, not patched**. The owner directed them live, so they are
instructions, not suggestions. Items 1–7 are the owner's UI findings recorded
further down this file under "Owner UI findings"; the numbering is continuous.

### Blocking

**21. ⛔⛔ The Stamper cannot capture ANY building.** `77`'s `add_building`
guards on `field(o,"template_name")`, but placed buildings do not carry it —
`Building.lua`'s `SetupBuildingTemplateTables` sets it only on the template
table (`BuildingTemplates[id] = setmetatable({ template_name = id },
g_Classes[id]) -- !!! temp onlys`), and adjacent commented-out debug code
resolves it as `self.class`. So every building is omitted and capture always
answers "no supported buildings or grid nodes in capture".
Measured four ways: the capture refusal; `CAPTURE_SKIP
object=StorageMachineParts(7078) reason="template unavailable"
template=StorageMachineParts` — **the skip logger's own `or o.class` fallback
prints the valid key the guard just rejected**; and `dump_selected
template=unavailable` on two unrelated buildings.
**Fix:** `field(o,"template_name") or o.class`, the fallback `skip_capture`
already uses two functions away. Audit every other `template_name` read.
**Consequence:** class 18 untestable — blocks 13, 14, 15 and the whole P5
feature the owner called *"a game changer"*.

**22. ⛔⛔ `spawn_colonists_*` mutates the colony and reports `REFUSED`.**
It verifies on the same tick: `before = #labels.Colonist` →
`CheatSpawnNColonists(...)` → `after = #labels.Colonist`. But a colonist joins
that label in `Colonist:GameInit() → AddToCityLabels()`, which the engine defers
to end of tick, while `Dome:SpawnColonist` is fully synchronous.
**PROVEN by measurement, not inference:**

```text
SMRTK_ACTION action=spawn_colonists_10 status=REFUSED reason="spawn count mismatch; before=701 after=701"
Scratch census, seconds later:  colonists=711
```

701 + 10 = 711 exactly. This is worse than a dead button — it is a **lying log
line**, breaching requirement (B), and all twelve `spawn_<kind>_<n>` buttons
share the body. **An action that has mutated must never report REFUSED.**

**25. ⛔ "Finish selected rocket flight" targets a state its own selection
requirement makes unreachable.** It needs the SELECTED object to be a rocket in
`CmdFlyToLocation`, but an in-transit rocket cannot be selected — owner, at the
keyboard: *"I cannot select a rocket in flight, if i click it it does nothing."*
Census read `UniversalRocket(4080):CmdFlyToLocation:READY, rockets_ready=1`
while the action answered `REFUSED reason="select an in-flight universal
rocket"`. Only route found: console `SelectObj(HandleToObject[<handle>])`, which
then worked (`outcome=travel_wait_finished skipped_time=159114`).
**Fix:** drive it from a rocket picker (same shape as the working trait picker),
or accept a handle argument.

### Evidence integrity

**19. `fix_all`'s `changed` does not mean changed.** The repair branch
increments for every building that merely *has* the method; the paired
`malfunction_all` branch compares before/after. Same field name, two meanings,
one `register()` pair. Measured contrast in one sitting:
`fix_all visited=1333 changed=1333 skipped=0` vs
`malfunction_all visited=1305 changed=740 skipped=564`.
⚠️ **And that set does not reconcile**: 740 + 564 = 1304 against `visited=1305`.
A building already malfunctioned takes the `elseif`, fails `not before`, and
increments neither counter — a silent third category the counts never name.
**Fix:** compare state in the repair branch too, or rename the field `dispatched`.

**11. `print_tee` is an orphaned action.** Registered in `70:276` with
`page = "Kit"` and a label, rendered by nothing — `76`'s tools row is a
hard-coded list that omits it. The owner found it by looking for a button I told
them to press. **The general fix is to render page-registered actions instead of
hard-coding rows**, so an action can never again exist with no control.

### Surface — the owner's UI findings and ruling

**1. ⛔ The dock inflates the HUD** — the owner's first complaint, and the one
that started the surface conversation. `73` parents `idSMRTKDock` into
`idBottom`, the window commented `"determine vertical size"`, at 62 px tall with
`Margins = box(8, 0, 0, 106)`. That inflates `idBottom` by ~168 px, so
everything anchored off it — MapSwitch/`idLeft` and the pinned
shuttle/dome/rover row — is permanently pushed up. Owner: *"its broken the UI
layout its kicked up all of the things that usually sit right above the doc."*
`73`'s own comment claims the separate row "preserves MapSwitch/idLeft layout" —
**false**: it preserves `idLeft`'s *internal* layout while inflating `idLeft`'s
*parent*. **Fix:** parent as a **sibling** of `idBottom` (the level that holds
`idHintPanel`), which sets no `LayoutMethod` and so defaults to `"Box"` —
children overlap instead of displacing. Owner wants it **bottom-right**.

**2. Hiding alone does not free space** (owner asked directly: *"does hiding it
still mean its shoved up because its still technically there?"*).
`XWindow.FoldWhenHidden` defaults **false**; only `true` zeroes the measure and
invalidates the parent's layout (`XWindow.lua:751`). Vanilla sets it on
`idOverview`. So the owner's instinct was right — a hidden window still reserves
its box unless that flag is set. Recorded because it was asked and answered; the
sibling fix in item 1 makes it unnecessary here.

**3. ⭐ RULED BY THE OWNER, 2026-09-14: one SMR button that toggles the whole
panel.** *"Just open and close the panel on click, opens it next click closes
it."* Drop the popout menu entirely. This bounds the permanent footprint to one
button, and `71`'s panel already carries a **fuller** status strip than the dock
does — it includes `quiet:`, which the dock strip omits. Keep a compact
clean/tainted colour on the button so requirement (A) stays visible with the
panel closed.

**4. A true dock icon IS available** — previously recorded as "plausible but
unverified". `HUDMiddle → idMiddleList` is an `XWindow` with
`LayoutMethod = "HList"`, `LayoutHSpacing = 10`, holding the vanilla buttons
`idOverview`, `idColonyControlCenter`, `idGoals`, `idBuild`, `idResearch`,
`idResupply`, `idElections`, `idPlanetaryView` as `HUDButtonNoFrame` instances
with `Image`, `ImageShine`, rollover title/text/hint and `OnPress`. Appending one
puts SMR in that row at **zero vertical cost**, which would fix item 1 by
construction. Needs an image asset; a text button is the fallback.
⚠️ **Container and class verified by source read; NOT built, NOT run.**

**5. Drop the Delete caveat from the section body** (`73:181`, `MaxHeight = 40`).
Owner: *"I don't need this info here."* ⚠️ It exists because 03B corrected it to
be honest about units, so **move it to the Delete button's `RolloverText`** —
`selected_button` already sets a rollover — rather than deleting it.

**6. Promote Clean & Fix to the top of the Selected list** as a quick action.
⚠️ **UNCONFIRMED READING.** The owner wrote *"add a clean button at the top of
these lists, that gives me the easy quick way to clean"*; I read that as Clean &
Fix and asked for confirmation, but the answer was overtaken by the sitting.
**Confirm before building.**

**7. Size the rows to their text, and shrink the font.** Today `selected_button`
hard-codes `MinWidth/MaxWidth = 146` (296 for More) in a 2-column grid at
`MinHeight = 30`, `TextStyle = "ConsoleLog"`. Owner: *"they don't need to be so
big… we could fit so much more together if they were minimally sized for what
they actually say. And we can make the font smaller as well"* — not as small as
vanilla's cheat menu, but far denser than now.

⭐ **The ruling, restated:** *"Just open and close the panel on click,
opens it next click closes it."* **One SMR button toggling the whole panel; drop
the popout menu entirely.** `71`'s panel already carries a fuller status strip
than the dock does (it includes `quiet:`, which the dock strip omits). Keep a
compact clean/tainted colour on the button so requirement (A) stays visible when
the panel is closed.

**8.** A disabled button is not visibly disabled — `RunAll`/`Run one` are
`SetEnabled(false)` until hygiene is ready and still look normal; only the gate
label says so.

**9.** Kit labels are terse and do not match how the work is described
(`RunAll`, `Run one`, an unlabelled probe combo). The owner could not find
"Run all probes".

**10.** "Arm / disarm configured watch" is pressable before a watch exists and
answers `status=NOT_BUILT` (ids 167, 168). Correct refusal, bad affordance.

**13.** Put controls at the **top** of every page, above any growing readout. On
Kit the verdict list grows with every run and pushes the buttons down, so the
page gets worse the more you use it.

**20.** ⭐ **An armed click slot blocks ALL map selection, with no warning.**
`AcquireClick` installs a `TerminalTarget` at priority 10001 returning `"break"`,
so while slot 4 (or `layout_target`, or a cursor-armed disaster) is armed,
clicking an object feeds the slot instead of selecting it. Measured: the owner
armed slot 4, then tried to select a drone; the click fired slot 4
(`object=FlyingDrone(2000244981)`) and the drone was never selected. The only
cue is a green caption on a panel they may not be looking at, and the escape
(right-click) appears nowhere on screen. **Suggest** a cursor change or a
persistent banner naming the armed slot and "right-click to cancel".
⚠️ Also a **script rule** for any future sitting: select objects and configure
watches BEFORE arming a click slot.

### Behaviour and scope

**12. ⭐ Make the cursor-targeted meteor actually hit the cursor.** `72` calls
`CheatMeteors(kind, setting, pos)` → `MeteorsDisaster(descr, kind, pos)` with
three args. The fourth, `forced_pos`, switches `SpawnMeteor` from
`GetRandomPassableAroundOnMap(map, pos, storm_radius)` to the exact point
(`Meteors.lua:107-111`). `storm_radius` defaults to `500 * guim`
(`Meteors.lua:16`) and **no shipped Meteor preset overrides it**, so every
intensity scatters identically and widely — the owner's *"fired but very
inaccurate"*. Vanilla's own cheat never passes `forced_pos`, so **the vanilla
cheat menu cannot place a meteor precisely and we can**. Keep scattered mode as
a separate row; real storms scatter.

**15. ⭐ The speed ladder skips rungs and our labels collide with vanilla's.**
`config.lua:117-122` — pause 0, normal 1, **medium 3**, **fast 5**,
**fastest 20**. The retail UI shows three buttons topping out at the `fast`
constant (5) while calling it "Fastest"; `const.GameSpeeds.fastest` (20) is not
exposed in the UI at all. Measured: our normal `requested=1`, our fast
`requested=5`, our ultra `requested=128`. So we expose 1, 5, 128 and skip 3 and
20 — which is why the owner reports *"smr's fast button is vanillas fastest
button"*. **Fix:** label by the constant we set, not vanilla's captions, and
fill in the missing rungs. (Supersedes the earlier item 14 note, which wrongly
treated the caption clash as ours.)

**18. Owner finding, confirmed in source: "Complete constructions" already does
"Complete wires / pipes".** `CheatCompleteAllConstructions` calls
`CheatCompleteAllWiresAndPipes()` as its first action. The grids button is not
useless (grids-only, leaving buildings to build normally, is a real want) but
nothing says so. **Relabel** both.
⚠️ **Attendee script defect:** block 7 ordered constructions before grids, so
the grids press ran against already-completed grids and measured nothing new.

**23. Rocket transit skip — mislabelled and one-directional.** *(a)* "Finish
selected rocket flight" is not the landing: `SleepFlight` is called with
`rocket.flight_time`, the interplanetary transit. A rocket already in orbit is
past it and correctly reads not-ready. The owner read the label as "make the
landing faster" — relabel to "Skip remaining transit (inbound)".
*(b)* Shipped `spot_type` values are earth / our_colony / anomaly / asteroid /
project / rival, and `rocket_arrive` refuses all but `our_colony`. **The return
leg to Earth — half of every supply cycle — cannot be skipped**, nor expedition
transits. ⚠️ Do NOT assume widening is one line: arrival at Earth or an
expedition site runs a different completion path. Cost it; do not promise it.

**16. ⭐ OWNER-REQUESTED WORK ITEM: a working/useful audit of the More section.**
03C migrated 84 More names by metatable walk, so they are "what the object
exposes" — but nothing says each still does something in 1.1.0, or that the
something is useful. Owner: *"I want a full round of checking in the games logic
to see if the stuff migrated over is actually working and if it is, is it
useful."* **Size it honestly: 84 names, each needing a press, an observation and
a keep/cut judgement — a dedicated link, not a sitting step.** Output should be
a keep / cut / needs-rollover list so the section can be pruned to what earns
its place.

### Corrections to the record

**17. ⛔ A source-derived prediction of mine was WRONG.** I predicted
`AsyncCheatInspect` would be UNAVAILABLE in retail because `Inspect` calls
`OpenGedApp("GedInspector", object)`. **Measured: it works** — a full live
inspector on `FlyingDrone`, owner screenshot, `status=OK`. The same reasoning
was my basis for doubting `ClassHierarchy`, `ClipPlane` and `Gizmo`; that basis
is refuted and those three must be measured, not assumed. 07's caution
("inspectors can depend on retail-unavailable debug services") is a sound
caution but must not be read as a verdict.

**⛔ STATE is wrong that "every depot is `UniversalStorageDepotBase`".**
`UniversalIngredientsDepot` has `__parents = { "MultiResourceDepotBase" }`, and
`MultiResourceDepotBase` (`{ "StorageDepot", "MultiResourceCubeVisuals" }`) is a
**sibling** of `UniversalStorageDepotBase` (`{ "StorageDepot" }`), not a
descendant. `73`'s `depot_read` guards on the wrong class and bails, so Fill and
Empty succeed **with no before/after evidence**. Witness:
`selected_fill method=CheatFill object=UniversalIngredientsDepot(8590) status=OK
valid_after=true` — no `before`/`after`/`resource`. **5 shipped classes** are on
the uncovered branch — `UniversalFarmPlantStorageDepot`,
`UniversalFungiStorageDepot`, `UniversalIngredientsDepot`,
`UniversalMeatStorageDepot`, `UniversalProcessedFoodStorageDepot` — against 22
covered. They *do* carry `storable_resources`; the guard tests the wrong class.
⚠️ **Not "all food depots"**: `StorageFood` is on the covered branch and reported
correctly (`before=113988 after=180000 resource=Food resources=1`).

**24. Attendee drift:** I told the owner the Scratch census applies the
"identical" predicate to `rocket_arrive`. It does not — I omitted
`IsKindOf(o, "UniversalRocketBase")`, assuming membership of the label of that
name implied the class. It does not: `UniversalSupplyPod` derives from
`UniversalSupplyPodBase` yet sits in that label. The census can report a supply
pod READY where the real action refuses on the class check.

**Attendee drift: my Scratch slot logs `map=[table]`** — `CurrentMap.map_id` is
nil, so my `scalar()` fell through. The fingerprint's `save=` covers the gap,
but the field is useless as written.

**Attendee instrument defect (method note for 99):** I twice reported a verb
absent when it was present, because I filtered `^\[mod\]` to de-duplicate.
Chrome verbs (`CLEAR`, `TAB`, `PANEL`, `MENU`, `COLLAPSE`) are deliberately NOT
echoed to the console by `T.Log`, so they appear **once**, with that prefix —
the filter deleted exactly the rows being counted. `CLEAR` fired 11 times, not
zero. **Any log audit of chrome verbs must not de-duplicate on `[mod]`.**

### Minor, recorded rather than dismissed

- **Double `SMRTK_SHORTCUT console=true key=Ctrl-Shift-F11` at mod load**
  (ids 4 and 5, same `t`) — a double primary result.
- **Building count fell 1333 → 1305** between the two `fix_all` sweeps. Block
  6's demolition accounts for some, not all 28. Unexplained.
- **`trigger_rocket` fired on `UniversalLanderRocket(3702)`, not on the rocket
  we skipped** — it listens for any `RocketLanded`, and 4080 went to orbit
  rather than landing. The trigger works; the firing was incidental, not causal.

## Verdict — PASS WITH CORRECTIONS

**Classes 1–17: PASS.** Every button class in 07's predictions was exercised and
scored against its prediction. Requirement (A) proven by an enumerated empty
`CheatsUsed` after the most destructive actions the toolkit offers. Requirement
(B) held for 844 records — every line tagged, one logger, attributable —
**except where defect 22 makes a line actively false.**

**Class 18: BLOCKED**, not merely unexercised — defect 21 prevents any capture,
so the three stamps could not be attempted.

**Corrections owed before class 18 can be scored:** defect 21 (blocking), then a
short follow-up boot for blocks 13–15. Defects 22, 25, 19 and 11 are independent
of the stamps and should ride the same fix link.

⛔ **The panel is the owner's to use from now on, with two caveats they must
know:** the Stamper does nothing until 21 is fixed, and **any `spawn_*` button
that reports REFUSED has still spawned** until 22 is fixed.

## Outbox to 99

1. The taint invariant is measured, not asserted — re-derive it against the
   archived boot log, not this prose.
2. `RunAll` ran; whether it discharges ck144 (a) is **unruled**. Do not assume.
3. STATE carries two refuted lines: `GhostFarmOxygen` as a FAIL, and "every
   depot is `UniversalStorageDepotBase`".
4. `DomeFreeSpaceMismatch` needs triage as a candidate defect.
5. Defect 22 means **the log lies** on one action class. Any audit that treats
   `status=REFUSED` as "no mutation" is wrong for `spawn_*`.
6. Three attendee drifts are recorded above — census predicate, `map=[table]`,
   and the `[mod]` filter. Weigh my other readings knowing that.
7. The owner ruled the surface live: **one SMR button, toggling the panel, no
   popout menu.** Item 6 (Clean & Fix placement) is an **unconfirmed reading**
   and must be confirmed before building.
8. 08's prompt is **deliberately not `git rm`'d** and its row is **not struck** —
   blocks 13–15 still need it. Closing 08 is the orchestrator's call.
