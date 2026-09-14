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

## Sitting

_Not yet run. Per-block PASS / REFUSED / UNAVAILABLE / NOT RUN verdicts, the
archived boot log path, the screenshot path, captured layouts and every drift
go here after the owner's boot._

## Verdict

_Not yet reached._
