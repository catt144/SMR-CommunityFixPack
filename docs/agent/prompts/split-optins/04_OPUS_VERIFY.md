# Chain prompt 4 — the verification matrix: three cells and a witness

**Read `README.md` first — binding chain rules apply.** Staleness check, todo
list. **Precondition: prompt 3's Notes below carry both HEAD shas and the
predicted readings — verify the shas match the working trees before anything
launches.** The game/Steam must be free (coordinate via the todo list; the
owner is NOT needed at the keyboard — this is the unattended-harness pattern:
parked .txt instruments landed in TestKit `Code/` only for the run, ARM gate
(a script FILE with resolution cross-check) before every launch, instruments
fire on load, no console typing; resurrect the u2-run pattern per WORKFLOW).

**Every cell's reading was PREDICTED upstream. You record readings against
predictions — a miss is a finding, chase its mechanism before filing.**

## The matrix (fresh launch per cell — D13's rule: a Mod-Manager toggle needs
## a FULL PROCESS RESTART to take effect; sequence the cells to minimize
## toggles and note every toggle + restart in the log via the harness)

* **(a) BOTH mods installed+enabled:** opening gate reads both registries
  (predicted `74/74` fix pack + `8/8` opt-in — the emitted numbers from
  prompt 3 are the prediction); suite runs; tally vs predicted; both Mod
  Options pages present (harness-readable or screenshot-free log evidence per
  design); zero `[LUA ERROR]`; zero cross-mod lines. ⭐ **This cell is the
  rig's standing configuration from here on (README rule 12)** — its measured
  numbers are the baseline every future leg quotes, so read them with that
  weight.
* **(b) OPT-IN ALONE** (fix pack disabled + full restart): loads clean,
  `8/8`, its options seed from its own `default_options`; ⛔ zero
  `SMRFixPack`-named lines beyond a loaded save's own recorded-mod-list echo
  (grep the archived log, EF-047); the 8 modules' probes run against its
  registry.
* **(c) FIX PACK ALONE** (opt-in disabled + full restart): `74/74`, suite
  tally re-baselined (this number replaces `77/0/10/0` in the records — it is
  measured HERE, quoted forever), zero references to the opt-in mod.
* **(d) SAVE-COMPAT WITNESS** (runs inside cell (a)): stage a byte COPY of
  `CP15PT15` (a KEPT save that ran with opt-ins ON under the old single-mod
  world; MD5 the original first — protected for this chain), load it, read
  back EVERY item on the persisted-name inventory live (D09 dial modifiers
  by exact id, fields, options state), then save/reload once (R4) and read
  again. Predicted: every name present where the old world wrote it, no
  duplicates, no orphans, zero errors. ⚠️ Mod-id change resets Mod Options
  account state — the dials are expected at BASE here, and that expectation
  is part of the prediction, not a miss (the owner re-ticks once; report it).

## Discipline

- One archived log per launch, copied + MD5'd at close (R8 `git add -f`).
- EF-047: absence claims only from archived files. EF-050: savenames
  verbatim. Staged saves: "deleted, listing verified" (EF-051 HOLD), listing
  BY NAME; the `CP15PT15` original byte-verified untouched at close.
- Any cell missing its prediction: record verbatim, keep independent cells
  running, route per README stop conditions. DISARM at end: TestKit `Code/`
  clean, PROBE SWEEP line in the result commit.

## Close

Append Notes-from-upstream to `05_FABLE_AUDIT.md`: per-cell verdicts with log
names/lines, the measured new baselines (both suite tallies, both gate
reads), the save-compat readings, every unexplained log line verbatim with
age, owner-time actually consumed (predicted: zero), and anything the audit
must settle. doccheck green ×2, commit (`-F`), push what has a remote, delete
this file in the same commit.

---

## Corrections from prompt 2 (QA, 2026-08-12) — these OVERRIDE the body above

The body predates the design. Where it disagrees with `90_DESIGN.md` §6.2,
the design (as amended by the QA block at its top) wins:

* **Cell (a) is TWO sub-cells.** At fresh account defaults the opt-in gate
  reads **`1/8`**, not `8/8` (mod id change resets Mod Options — design
  §2.4): that is cell (a1), 72 PASS / 0 FAIL / 16 SKIP of 88. Cell (a2)
  activates the 7 toggles in-session via the design §4.4 instrument (which
  must fire AFTER ClassesBuilt) and predicts `8/8` and **78/0/10/0 of 88**
  with the SAME 10 SKIP names as u2run3 (read BY NAME).
* **Cell (b)'s `8/8` likewise holds only after activation** — at defaults it
  is `1/8`; match whichever (a) sub-cell you pair it with.
* **Cell (d): the D09 dial modifiers are expected ABSENT after load** — the
  new mod id means base dials, and `PostLoadGame` reconcile REMOVES our ids
  (design §6.2's per-row table). Absence there is the PASS; "every name
  present where the old world wrote it" applies to the POLICY/ACK FIELDS
  (rows 1–3), not the dials. Report population sizes per row, and confirm
  the staged copy actually carries stamps/flags BEFORE the run (QA weak
  claim 2).

---

## Notes from upstream (prompt 3 — the build, 2026-08-12)

**THE SPLIT IS BUILT. Nothing was launched.** Every number below is STATIC —
parse sweeps, greps, byte diffs and `--emit-counts`. The game was closed for the
whole session, so this prompt owns every claim about a running game.

### Shas — verify these against the working trees before anything launches

| repo | HEAD at close | remote |
|---|---|---|
| `C:\Dev\SMR-BugFixPack` | see `git log -1` after this file's own commit | `origin` (pushed) |
| `C:\Dev\SMR-OptInPack` | `0c855d7` | ⛔ none — LOCAL git only (rule 9) |
| `C:\Dev\SMR-BugFixPack-TestKit` | the dial-probe follow-up commit (2 commits after `d8e1fbf`) | none |

Donor shas the port was taken from: pack `33d69f5`, TestKit `d8e1fbf`.
Junction: `%AppData%\Surviving Mars Relaunched\Mods\SMR-OptInPack` →
`C:\Dev\SMR-OptInPack`, created and listed beside the other two.
**The new mod is NOT enabled in the Mod Manager** — enabling it is a
full-restart act and is part of your cell sequencing.

### The emitted post-split counts (both sides, never hand-typed)

```
FIX PACK — python tools/doccheck.py --emit-counts
- modules: 74 registered (74 default-active, 0 optional-gated files)
- Code/*.lua files: 75
- TestKit probes: 88
- BUGS index rows: 102 F + 12 D + 46 C

OPT-IN MOD — python tools/doccheck.py --emit-counts
- modules: 8 registered (1 default-active, 7 optional-gated files)
- Code/*.lua files: 9
- TestKit probes: 88 (shared kit — serves both mods)
- BUGS index rows: 0 F + 9 D + 0 C
```

⭐ **Every one of these matched the design's prediction exactly** (§3.5: here
75/74/0/74, there 9/8/7/1; §4.3: 87 → 88 probes; §5.1: rows unchanged). The
doccheck arithmetic repair was made FIRST and re-run against the pre-split tree
as a control — it reproduces the old 75, so the numbers above are not an
artifact of the repair. ⛔ The pre-split `82/75/8` and the `81/81` gate read are
ERA-STALE; the fix pack's gate now reads `74/74` in every configuration,
because nothing in it is option-gated any more.

### ⛔ The persisted-name inventory, verbatim — read these back live in cell (d)

**These bytes are the save contract. They kept the `SMRFixPack_` prefix on
purpose; it is not a stale rename waiting to happen.**

| # | exact bytes | kind | where it lives now |
|---|---|---|---|
| 1 | `SMRFixPack_ack_notworking` | field on `Building` objects | `Opt_AcknowledgedWarnings.lua` (opt-in mod) |
| 2 | `SMRFixPack_closed_to_new_residents` | field on `Dome`/`MicroGHabitatBase` | `Opt_ResidencyControl.lua` (opt-in mod) |
| 3 | `SMRFixPack_no_homeless` | field on `Dome`/`MicroGHabitatBase` | `Opt_NoHomeless.lua` (opt-in mod) |
| 4 | `SMRFixPack_DroneSpeedDial` | label-modifier id in `UIColony.label_modifiers["Drone"]` | `Opt_DroneStatDials.lua` (opt-in mod) |
| 5 | `SMRFixPack_DroneCarryDial` | label-modifier id, label `Consts` | `Opt_DroneStatDials.lua` (opt-in mod) |
| 6 | `"1x (base)"` `"2x"` `"3x"` `"5x"` | dial choice values | opt-in `metadata.lua` + `items.lua` + the module's map |
| 7 | `"+0 (base)"` `"+1"` `"+2"` | dial choice values | as above |
| 8 | `ClassicRockets` `AcknowledgedWarnings` `ResidencyControl` `MultipleSuns` `DroneOverhaul` `CohortHousing` `NoHomeless` | option keys **and** Register ids | opt-in `metadata.lua`/`items.lua`/modules |
| 9 | `DroneSpeedDial` `DroneCarryDial` | option choice keys (NOT Register ids) | opt-in `metadata.lua`/`items.lua` |

**Byte-diffed at the port, donor `33d69f5` vs the moved files:** occurrences
2/3/3/2/2 before → 2/3/3/2/2 after, all five, and all 8 module files kept their
exact line counts. **All 12 surviving `SMRFixPack` occurrences in the new
repo's `Code/` are exactly these five names** (5 definitions, 7 comment
mentions) — zero references to the fix pack's namespace. The kit keeps them
byte-identical too, in `60_Probes_Opt.lua` and `99_FixtureCarry.lua`.

### The matrix cells' predicted readings, updated for what the build learned

| cell | predicted, and what the build changed about it |
|---|---|
| **(a1)** both mods, fresh account defaults | fix pack **`74/74`**, opt-in **`1/8`**; **72 PASS / 0 FAIL / 16 SKIP / 0 ERROR of 88**. Unchanged by the build. 7 × `<id>: inactive (opt-in module, off by default …)`; ⛔ no `NoHomeless` F100 first-pass line — a toggle-state effect, not a port regression |
| **(a2)** both mods, 7 activated in-session | `74/74` + **`8/8`**; **78 / 0 / 10 / 0 of 88**, the frozen baseline with its 10 SKIPs BY NAME plus the one new probe passing. ⭐ `OptionsMenuOptIn` now asserts **7** toggles + 2 dials (NoHomeless was added to `WANT` — it was missing while it shipped), so an (a2) PASS is a slightly stronger claim than the design costed |
| **(b)** opt-in alone | as its matching (a) sub-cell for the 8 opt probes; every other probe FAIL or SKIP and NONE PASS. ⛔ zero `[CommunityFixPack]`/`SMRFixPack` lines — ⚠️ **and the qualifier is now demonstrated, not hypothetical: `CP15PT15`'s own header contains the literal string `SMR_CommunityFixPack` twice** (its `active_mods` block, read off disk this session). Grep with the FULL bracketed token and expect the save's mod-list echo |
| **(c)** fix pack alone | **`74/74`**; **70 / 0 / 18 / 0 of 88**, the 8 opt probes SKIPping via `OptMissing`; `OptionsMenuFixPack` PASSes. ⭐ **New in the kit and it is the probe to watch here**: it asserts the NEGATIVE — the fix pack declares no `default_options`, ships no option items, and holds none of the 8 moved ids. ⛔ The fix pack no longer appears in Options → Mod Options at all; that is the intended shape, not a missing page |
| **(d)** save witness inside (a) | dials expected **ABSENT after load** (new mod id ⇒ base dials ⇒ `PostLoadGame` removes our ids — absence is the PASS); policy/ack fields **present exactly where the old world wrote them**; `SMRFixPack_F48_StationConnectors` on `UIColony` as the positive control. Report POPULATION SIZES per row |

### `CP15PT15` — what this session could and could not settle about the witness

Read-only, EF-051-safe (opened for reading; nothing written, nothing deleted):

```
C:\Users\stkot\Saved Games\Surviving Mars Relaunched\76561198020568696\CP15PT15.savegame.sav
MD5   D2887D754C44134141B6CCC4C9020446
bytes 47,370,762   mtime 2026-08-11 18:06:22
container BPUL — the game state is COMPRESSED; only the header is plaintext
active_mods (from the header): "SMR_CommunityFixPackTestKit", "SMR_CommunityFixPack" (optional = true)
active_game_rules: "UnlockedPolicies", "EasyResearch", "MoreApplicants"
```

⇒ **SETTLED:** the save exists, is the size/date the records expect, was made
under the OLD single-mod world with the fix pack + TestKit enabled, and its
header string is the mod-list echo cell (b) must tolerate.
⇒ ⚠️ **NOT SETTLED, and it is QA weak-claim 2 verbatim:** whether it carries
`ack_notworking` stamps or policy flags. The payload is compressed, so no
static read can answer it — **the first thing cell (d) should do after loading
is print the population size of each row, and if rows 1–3 are all zero the save
is a thin witness and a second one must be staged before the reading is
quoted.** Candidates visible in the same folder, newest first: `CP60RT`,
`Autosave Sol 311`, `Autosave Sol 306` (⛔ all three are HELD by the owner —
copy only, never move or delete), `TEST2 AST`, `CP15F15`, `PT-15 post save`.

### The §4.4 activation instrument, corrected per MUST-FIX 4 — park this, don't re-derive it

⛔ It must fire **after `ClassesBuilt`**, or `Opt_NoHomeless`'s F100 second-pass
`Require` fails again and (a2)/(b) miss their predictions for a reason that is
not a port regression. It writes NO account storage, and restores the originals
in every branch (the `DroneStatDials` probe's proven shape).

```lua
-- park as .txt; land in TestKit Code/ for the run; delete in the result commit
local IDS = { "ClassicRockets", "AcknowledgedWarnings", "ResidencyControl",
              "MultipleSuns", "DroneOverhaul", "CohortHousing", "NoHomeless" }
local function activate_all()
    local mods = rawget(_G, "Mods")
    local def = type(mods) == "table" and mods["SMR_CommunityOptInPack"]
    local opts = def and def.options
    if type(opts) ~= "table" then
        SMRTest.Log("OPTIN-ACTIVATE: options object unreachable — NOT armed")
        return
    end
    local orig = {}
    for _, id in ipairs(IDS) do orig[id] = rawget(opts, id) end
    for _, id in ipairs(IDS) do rawset(opts, id, true) end
    Msg("ApplyModOptions", "SMR_CommunityOptInPack")
    -- read the gate back BEFORE restoring, so the log records what was armed
    local P = rawget(_G, "SMROptInPack")
    local active = 0
    for _, id in ipairs(P and P.order or {}) do
        if P.fixes[id].status == "active" then active = active + 1 end
    end
    SMRTest.Log("OPTIN-ACTIVATE: %d/%d modules active after in-session enable",
        active, #(P and P.order or {}))
    return function()   -- the restore, called in EVERY branch at leg end
        for _, id in ipairs(IDS) do rawset(opts, id, orig[id]) end
        Msg("ApplyModOptions", "SMR_CommunityOptInPack")
    end
end
-- ⛔ AFTER ClassesBuilt. RunAll-time is the simplest correct hook; a late
-- OnMsg (LoadGame / CityStart) also qualifies. NOT at file scope.
```

⚠️ **`Mods[id].options`, never `CurrentModOptions`** — the latter is per-mod-env
and the TestKit's copy is the TestKit's (the failed 2026-07-29 leg). The build
had to repair exactly this in the D09 dial probe, which still wrote to the fix
pack's options object after the split; see the kit's follow-up commit.

### Every deviation from the design, with its ruling

1. **§1.3's "COPY verbatim" for `Register`/`DataPatch` was not followed** —
   applied as MUST-FIX 1 said: whole-file token rename first. `:270` and `:384`
   are in the diff. **Ruling: the QA was right and the design line was wrong.**
2. **`metadata.lua` version fields.** §3.3 said `version`/`version_major`/
   `version_minor` = `0`/`1`/`0`, which under its own field order reads
   **1.0.0** — not the "pre-release" the same sentence asks for. **Built as
   0.1.0** (major 0, minor 1, revision 0). `PackVersion` has zero executable
   callers among the eight modules, so nothing depends on it. Launch prep sets
   the ship value.
3. **Three sites the design's disposition table did not list**, all found by
   reading the files rather than trusting the table, all adapted:
   `Opt_DroneOverhaul` carries its OWN cloned logger with its own
   `[CommunityFixPack]` literal (`:280` in the donor); `Opt_ResidencyControl`
   and `Opt_NoHomeless` each name the mod in a player-visible infopanel
   **rollover title**. Not persisted (window instances) ⇒ display strings ⇒
   they carry the placeholder name. **Had the logger been missed, cell (b)'s
   "zero CommunityFixPack occurrences" would have failed for a non-port
   reason.**
4. **`docs/PLAYTEST_HELP.md` / `PLAYTEST_CHECKLIST.md` were edited** — design
   §2.3 requires the lever rename in the SAME commit. P13's lever is now
   `SMROptInPack_Disabled.NoHomeless`; the `ListFixes` row reads `74/74`; the
   toggles-OFF instrument recipe now drops into the OTHER repo.
5. **EF-054 was written into BOTH repos**, not only the new one (MUST-FIX 7 asked
   for the new repo's copy). An engine fact describes the game; leaving the fix
   pack without one the chain proved would be a silent drop. It also gained a
   branch the QA's citation chain did not carry: with `LoadAllMods` set the
   order is alphabetical, not enable-order. Both deterministic.
6. **Two pre-existing defects repaired en route**, both named as pre-existing:
   `99_FixtureCarry`'s `INSTANCE_FIELDS` never listed `SMRFixPack_no_homeless`
   (MUST-FIX 3), and the `OptionsMenu` probe's `WANT` never listed `NoHomeless`.
   ⇒ ⚠️ **Consequence for your (a2) comparison: `OptionsMenuOptIn` asserts more
   than the probe u2run3 ran did.** A PASS is stronger, not different; a FAIL
   there could be the newly-checked seventh toggle rather than a port break —
   check which before filing.
7. **MUST-FIX 2 honoured: no varargs were added to `Fix_LanderReturnFuel`.** The
   file is untouched. The Src citation lives in the QA block at the top of
   `90_DESIGN.md`.
8. **MUST-FIX 8's two extra fix→opt consumer edges** are record-only and were
   not changed: `Fix_ArrivalDeaths:192` → `ChooseDome`;
   `Fix_LowStorageWarning`/`Fix_BombardmentSpread` →
   `AddObjectToNotification`/`RemoveObjectFromNotification`. Call-time global
   reads, order-independent. **Expect the composition to differ between cells
   (b)/(c) and (a) at these sites and do not read that as interference.**

### Three things to carry into the run

* **Two gate lines now, not one.** `fix pack present: %d/%d fixes active` and
  `opt-in pack present: %d/%d modules active`, printed separately so old greps
  survive. A leg quoting one number describes half the rig.
* **`OptMissing` SKIPs, never FAILs, on an absent registry** — that is why cell
  (c) predicts 18 SKIPs rather than 8 FAILs. If you see FAILs there, the guard
  did not take, not that the mod broke.
* **The owner owes exactly one minute, AFTER you report clean**: enable the new
  mod (full restart) and re-tick 7 toggles + 2 dials. It is on checklist item
  15 with the reassurance that their saves are untouched. **Do not spend their
  time before the matrix says the mod is sound.**
