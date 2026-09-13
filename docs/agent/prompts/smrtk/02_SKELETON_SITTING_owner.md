# smrtk 02 — the skeleton in the real game (attended) — ⛔ KILL GATE

Link 02 of `smrtk`. A **Claude** session attending (rule 22: the non-building vendor scores the builder's
predictions), the owner at the keyboard. README rules 1–22 are yours; rule 13 shaped the script
below (01 writes it). Score every step against `reports/SMRTK_SKELETON_PREDICTIONS.md`, prediction by prediction.

## The four premises this sitting decides

| # | premise | PASS reads as | FAIL means |
|---|---|---|---|
| P1 | a leaf action leaves `CheatsUsed` empty | `SMRTK_TAINT_READ used=false` AFTER a Fill on a selected depot, and the status strip says CLEAN; the Mod Manager is CLOSED throughout | the chain's requirement (A) is false at the source level — KILL, reduced 99 |
| P2 | `ConsoleEnabled` gives the console with mod tools closed | after a fresh load with the Mod Manager never opened, **Enter** opens the console | the load-time hook is wrong or the arm is too late — 01 re-fires with 02's log; not a kill unless a second try fails |
| P3 | the tap sees console lines | Copy-since-mark pastes the `[SMRTK]` lines AND at least one vanilla `print` line from the same window | the tee fallback carries it (02 records which); a kill only if neither path carries lines |
| P4 | the panel survives a save/load | after Save then Load, the panel is open on the same tab | persistence route wrong — 01 re-fires; not a kill |

The stale-probe gate binds: `grep -rln "TEMPORARY" Code/ ../SMR-BugFixPack-TestKit/Code/` → 0 before any reading,
and the line goes in the todo list.

## Pre-declared control (so PASS cannot be vacuous)

Before P1, the agent reads the same thing the vanilla way in a **scratch branch that is then discarded**: open the Mod
Manager, use the vanilla menu to show infopanel cheats, press `Fill` once, read `CheatsUsed` — it must show one entry. That is the RED the
toolkit's GREEN is compared against. ⛔ That scratch save is never loaded again for a reading (`EF-051`: a stray save
is the falsifier's own hazard) — the owner names it `SMRTK_SCRATCH_TAINTED` and the agent records its deletion.

## Verdict

PASS / PASS WITH CORRECTIONS (strike-and-supersede the predictions doc, section by section) / KILL. Written to
`reports/SMRTK_SKELETON_SITTING.md` with the archived log path, and in plain language to ck175. A KILL is the gate
working: 99 runs its reduced form.

## What may NOT be claimed

Anything the log does not show. "Works on gamepad" (not tested here). That any page beyond the skeleton exists.

## Close-out

Outbox to 03A (one paragraph: what P1–P4 read, which tap path carries lines, the hotkey that stuck — 03A pastes
it into every payload's inbox) and 99; strike your row; `git rm` this file; push.

## Notes from upstream

- **01 outbox, 2026-09-13:** cut re-validated **with corrections**, detailed in
  `reports/SMRTK_SKELETON_PREDICTIONS.md` (disagreements, DEPARTURES, SUGGESTIONS,
  actual API, desk gates). TestKit commits: core `774b55a`, panel `b400683`,
  metadata `5d8d3b3`. Everything remains untested in play. Hotkey is now
  **Ctrl-Shift-F11**; Ctrl-Shift-K collides with the developer collision action.
- **Eligibility is UNAVAILABLE, not OK.** `CanUnlockAchievement` is blacklisted
  (`Mod.lua:1403`); no read here proves full eligibility. Requirement (A) remains
  binding. Measure no added cheat taint; retain the eligibility limitation for
  03B/99 and ck175. No achievement mutation is authorized as a surrogate read.
- The old TestKit already enables/rebuilds/auto-opens the console. Step 2 isolates
  shortcut creation; step 1 alone cannot credit this toolkit with enabling it.
- **DEPARTURES:** current-mark labels or absolute ring indices (no saved mark
  catalogue); toolkit records enter the ring directly and do not prove native
  delivery; Fill is a sitting-only registration, keeping the page payloads empty.
  **SUGGESTIONS:** after this evidence, let 03B decide whether to retire the old
  console bootstrap; budget clean fixture provisioning separately from the sitting.

### Fixture and timing — read before starting

Any **1.1.0 colony whose current `AreCheatsUsed()` is false**, with a partially
empty **single-resource depot** (e.g. Metals, not a Universal Depot). Pause it
using the game's normal speed control. Save a clean baseline as
`SMRTK_BASELINE_CLEAN` before the control. A normal already-cheated playtest save
cannot serve this leg. If none is clean, report fixture preparation owed; do not
clear the flag or load a 1.0.7 save. The estimated 20–30 minutes excludes provisioning.

Claude attends; the owner drives the game. Do not launch it unattended. Before
launch, run the fingerprint, parse/gate commands from 01's report and:

```powershell
rg -n TEMPORARY Code ../SMR-BugFixPack-TestKit/Code
```

Zero matches (rg exit 1) is the expected stale-probe result, not a missing-path
error. Archive the game log at the end; every result cites its lines. **The LOG
is the echo contract**; screen observations below only orient the owner. Each
Lua fence below is pasted into the game console **one line at a time**. Never
paste the entire block or a trailing comment. For each UI/read step allow 5 s,
abort at 15 s; for initial UI restoration 10/30 s; for save/load 30/90 s, with
an update at 30 s. Unexpected taint/error/refusal stops the clean leg immediately.

### 0 — clean baseline, then the deliberately RED scratch branch

First screen: the paused colony and selected partly empty depot. Read and record
these lines before saving the clean baseline:

```lua
SMRTK.TaintRead()
SMRTK.Run("eligibility")
SMRTK.Log("PLATFORM_READ",{cheats=tostring(Platform.cheats),eligibility_api=type(CanUnlockAchievement),mod_tools=AreModdingToolsActive()})
```

Expected: TAINT_READ used=false; eligibility reason=UNAVAILABLE:sandbox;
eligibility_api=nil. Record the actual `cheats` value; it was unverified at
authoring. If used=true, this is the wrong fixture. Preserve the clean save.

Now branch to the control. Open Mod Manager, use the vanilla cheat menu's
infopanel-cheats toggle, select the same depot, and press its vanilla **Fill**
once. First screen: its resource count increases. Then:

```lua
SMRTK.TaintRead()
SMRTK.Log("SCRATCH_READ",{entries=CheatsUsed and #CheatsUsed or 0})
```

Expected used=true and entries=1, plus the SMRTK_TAINT alarm. Save this branch
under **SMRTK_SCRATCH_TAINTED**, never over the clean baseline. Quit the game.
Delete just that named scratch save through the normal load/save UI when next
available; record its name/deletion in the log and report. Never load it again
for a reading. If the vanilla control cannot be reached, report an unrun RED;
do not fake it by writing the flag.

### 1 — fresh boot, Mod Manager never opened this boot

Load **SMRTK_BASELINE_CLEAN**. Let the legacy TestKit's console auto-open finish,
close the console, then press **Enter**. First screen: it opens again. Close it,
press **Ctrl-Shift-F11** twice: the floating panel hides and returns. If initially
hidden, reverse those two observations. The LOG must contain CONSOLE_ARM
hook=PreLoadGame and the SHORTCUT registration for Ctrl-Shift-F11. Then:

```lua
SMRTK.TaintRead()
SMRTK.Log("SCRATCH_DISCARDED",{name="SMRTK_SCRATCH_TAINTED"})
```

Only paste SCRATCH_DISCARDED **after the owner actually deleted it**; the line
records the owner's act, never performs deletion. Expected used=false.

### 2 — isolate the shortcut creation gate

First screen: console open, Mod Manager closed. This diagnostic synchronously
sets ConsoleEnabled false, rebuilds, reads DE_Console, sets it true through the
toolkit arm, rebuilds and reads again. It always restores the flag to true.

```lua
SMRTK.ConsoleControl()
```

Prediction: `discriminates=true negative=false positive=true status=OK`. Close
and reopen console with Enter after this line. If negative=true, another gate
(retail cheats/devtools) already creates the shortcut; log that non-discriminating
result and the platform read. Do not blame or credit our hook for that negative
leg. Positive=false or Enter still dead returns this leg to 01; do not claim P2.

### 3 — one leaf action through the toolkit wrapper

First screen: a selected, partly empty single-resource depot, colony paused.
Paste this **one line** (the registration is session-only):

```lua
*r SMRTK.Action{id="skeleton_fill",needs="selected",run=function(c) local o=c.selected; if not IsKindOf(o,"StorageDepot") or type(o.resource)~="string" or not o.supply or not o.supply[o.resource] then return false,"select a single-resource depot" end; local before=o.supply[o.resource]:GetActualAmount(); if before>=o["max_amount_"..o.resource] then return false,"depot already full" end; o:CheatFill(); return {object=o,before=before,after=o.supply[o.resource]:GetActualAmount()} end}; SMRTK.Run("skeleton_fill")
SMRTK.TaintRead()
SMRTK.Run("eligibility")
```

Expected ACTION action=skeleton_fill status=OK with after > before and the
depot's Class(handle); visually it fills. The next read must be used=false and
the strip CLEAN. Eligibility remains unavailable. Any new taint KILLS P1.

### 4 — native tap and clipboard, with the tee OFF

First screen: panel expanded; press MARK once to locate it, then in the console:

```lua
SMRTK.Mark("native")
print("SMRTK_NATIVE_PRINT_100%")
ConsolePrint("SMRTK_NATIVE_CONSOLE_100%")
*r SMRTK.Action{id="tap_read",verb="TAP_READ",run=function() local n,p=0,0; for _,r in ipairs(SMRTK.ring) do if r.n>=SMRTK.mark_index and r.source=="console" then if r.text=="SMRTK_NATIVE_PRINT_100%" then p=p+1 elseif r.text=="SMRTK_NATIVE_CONSOLE_100%" then n=n+1 end end end; return {native_console=n,native_print=p} end}; SMRTK.Run("tap_read")
SMRTK.CopySince("native")
```

Paste into a local text editor. Expected: the two actual witness **outputs**
carry source=console; toolkit records carry source=toolkit; TAP_READ logs
native_console=1 native_print=1. Typed command echoes containing these strings
do not count. If exact counts fail because native delivery includes decorations
or chunks, preserve that clipboard text, mark the exact prediction false and
identify the actual output chunks. If no native output arrives, test step 5's
fallback; our own ring lines alone never PASS P3.

### 5 — fallback tee fires and uninstalls

First screen: strip says Armed: 0. Paste:

```lua
SMRTK.Mark("tee")
*r SMRTK.sitting_original_print=print; SMRTK.PrintTee(true)
print("SMRTK_TEE_WITNESS_100%")
SMRTK.CopySince("tee")
SMRTK.PrintTee(false)
SMRTK.Log("TEE_RESTORE",{same=print==SMRTK.sitting_original_print,armed=SMRTK.ArmedCount()})
```

Expected ARM, FIRE action=print_tee text=SMRTK_TEE_WITNESS_100%, DISARM,
TEE_RESTORE armed=0 same=true. Paste clipboard: witness has source=print.
The strip goes 0→1→0. At least one of the native/fallback routes must carry
the actual print output, and clipboard must paste it, to PASS P3.

### 6 — mouse frame, fixed controls and persistence choices

First screen: panel open. Click each tab, end on **Kit**, drag by its status
strip, collapse with **[_]**, expand again. The same footprint is used by all
tabs; collapse retains the strip and top row. Click **Flush**, **Clear**,
**Pause / Resume**, **Stop disaster**. Expected FLUSH/CLEAR status=OK;
ACTION action=pause and action=stop_disaster status=NOT_BUILT. These two are
stubs. Clear calls cls; the new CLEAR log line may immediately appear after it.
TAB/MOVE/COLLAPSE logs record each choice. No page content is expected.

### 7 — stack/counter handler witness (synthetic, explicitly)

First screen: expanded panel. This invokes our handler, not a native error:

```lua
SMRTK.Mark("error-handler")
SMRTK.OnLuaError("SMRTK_ERROR_WITNESS","SMRTK_STACK_WITNESS")
SMRTK.Log("ERROR_READ",{since_mark=SMRTK.error_count-SMRTK.mark_errors})
SMRTK.CopySince("error-handler")
```

Expected ERROR kind=lua with both witnesses; ERROR_READ since_mark=1; strip
increases to 1 and clipboard retains the stack. This does **not** prove native
OnLuaError/OnThreadError delivery; leave that limitation explicit.

### 8 — auto-disarm and a save/load round trip

First screen: expanded **Kit** tab at its moved position, armed=0. Paste:

```lua
SMRTK.Mark("roundtrip")
SMRTK.PrintTee(true)
```

Use the game's save UI to create **SMRTK_ROUNDTRIP_CLEAN**, then load it. Expected
DISARM action=print_tee reason=SavegameSaved status=OK before the load. The panel
returns open, expanded, on Kit at the moved position; armed=0. Then:

```lua
SMRTK.TaintRead()
SMRTK.Run("eligibility")
SMRTK.Log("ROUNDTRIP_READ",{armed=SMRTK.ArmedCount(),collapsed=SMRTK.PanelState().collapsed,open=SMRTK.PanelState().open,same_print=print==SMRTK.sitting_original_print,tab=SMRTK.PanelState().tab,x=SMRTK.PanelState().x,y=SMRTK.PanelState().y})
SMRTK.CopySince("roundtrip")
```

Expected used=false; eligibility unavailable; ROUNDTRIP_READ armed=0
collapsed=false open=true same_print=true tab=Kit and the MOVE coordinates.
Archive the log and clipboard evidence. Restore the clean baseline if desired;
retain the clean roundtrip only as an explicitly named fixture. Finish with the
game closed. Write the prediction-by-prediction report and ck175 outcome before
03A can run.
