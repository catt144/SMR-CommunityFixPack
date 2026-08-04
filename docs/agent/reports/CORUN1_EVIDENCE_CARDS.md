# Co-run #1 — the evidence cards

Four cards in `CORUN_RIG_SPEC.md` §4's Tier B template, produced 2026-08-04 by
chain prompt 3. ⭐ **Cards were written for the Tier A items too, on purpose:**
prompt 4 is asked to audit whether the card alone would have sufficed *without*
the owner's eyes, and it cannot audit that unless the card exists. Each card
ends with the honest answer to that question rather than a flattering one.

**Run conditions, shared by all four.** Retail `Mars.exe` **1.0.7.396349**,
launched `steam.exe -applaunch 3215050` with **no** `-smrautorun`. **COLD load**
of `CORUN1.savegame.sav`, a `Copy-Item` copy of `TEST2H TRAIN` staged with the
game closed; the campaign save was never written and read the same 55,667,524
bytes / 2026-08-03 22:21 afterwards. Fix pack read **81/81 active, 0 inactive,
0 disabled, 0 error** in both runs. Game speed set to **3** by script (a loaded
save arrives paused — correction C4). **Zero** `[LUA ERROR]`, **zero**
`Assert failed`, **zero** modals across both runs.

**Session uptime at measurement: ~6 min (run 1), ~1 min (run 2).** ⚠️ These are
*short* sessions by this project's standards — the owner's own logs span 1–6
hours — so a zero-error count here is weaker evidence than a zero in a campaign
log, not stronger. Stated because the convention requires uptime next to a count.

**Raw logs, archived in the commit that cites them** (`git add -f`; `.gitignore`
line 2 is `*.log`):
`docs/archive/corun1_Mars.exe-20260804-12.42.47.log` (run 1) ·
`docs/archive/corun1b_Mars.exe-20260804-12.54.14.log` (run 2) ·
`docs/archive/corun1c_Mars.exe-20260804-13.23.08.log` (run 3, 64 s cycle —
closes card 3's corner case at the owner's request).

**PROBE SWEEP:** clean before, `armed: TestKit Code/97_CoRun1.lua` (run 1) and
`Code/97_CoRun1b.lua` (run 2) during, clean after — both files and their
`metadata.lua` lines deleted in the recording commits, staged save deleted.
⚖️ The one-time armed-prep override was **declined**; see `CORUN1_BRIEF.md` §6.

---

## CARD 1 — F11: does the pre-wrapper conversion behave like the copy it replaced?

**Scenario.** Cold load of the staged copy, pack ON, speed 3. 8 trains, 59
riders aboard. For 238 s of real time the leg polled every train's `command`
and `#units` once a second and logged every transition, while counting
`Holder.OnExitHolder` calls whose holder was a `Train`. The owner watched the
camera-selected train reach a station, unload and leave. ⛔ `Colonist.ExitVehicle`
was deliberately **not** wrapped — it is the fix's own target, and instrumenting
the function under test would have put a TestKit frame on the measured path.

**Forced:** nothing. The trains ran their own schedules.
**Organic:** the whole leg — this is ordinary train traffic on a provisioned save.

**Raw log, the readings:**

```
READ fixpack: 81/81 active
READ F11 module TrainPlatformWedge status=active detail=
READ L1 branch liveness: LuxuriousTrains researched=1 (true => the 'travel time' comfort call is SKIPPED by design)
READ L1 fixture: 8 train(s), 59 rider(s) aboard, 0 train(s) on a seen_forest track
L1 TRAIN Train#2000016863 GotoStation(12) -> UnloadTrain(5) station=StationSmall#12472
L1 TRAIN Train#2000016863 UnloadTrain(5) -> LoadTrain(5) station=StationSmall#12472
L1 TRAIN Train#2000016863 LoadTrain(5) -> GotoStation(5) station=StationSmall#12472
L1 COUNTERS over the window: train-holder removals=340, 'travel time' comfort calls=0, 'seen forest' sanity calls=0, wedge candidates=0
```

**Owner verdict (Tier A):** *"I saw everything"* — the watched train unloaded
and left. Console `CoRun1_Go = 1` at +257 s.

**What it establishes.** Two of the rider's three readings.
`TrainPlatformWedge` is **active**, read from `SMRFixPack.fixes` rather than
assumed. Trains **unload and leave**: seven distinct trains completed full
`GotoStation → UnloadTrain → LoadTrain → GotoStation` cycles in ~2 s each,
**340** passengers were removed from train holders, and **0** wedge candidates
fired (the detector needs a train to sit in `UnloadTrain` for >20 game-hours
with `#units` not falling). The pre-wrapper's structural claim follows: the
normal path *must* be tail-calling the captured original, because `orig`'s
destructor is what runs `DiscardTransportTicket` and drops `#self.units`, and
`UnloadTrain` spins until it does (`Train.lua:451-453`).

⛔ **What it does NOT establish, and why `tested` is not claimed.** The rider's
third reading — that disembark comfort/sanity still move — **cannot be taken on
this save**. `LuxuriousTrains` is researched, so the `"travel time"` comfort
call is skipped by design (`ColonistTransport.lua:555-557`), and **0** trains
run a `seen_forest` track, so the sanity call cannot fire either
(`:558-560`). **`0` and `0` are what a correct fix and a broken one both
produce here**, so they are not evidence in either direction.

**This card is wrong if:** a train is later seen wedged at a platform with the
pack on, or a save where either stat branch is live shows the call missing.

⚖️ **Would the card alone have sufficed without the owner's eyes?** **Yes, and
the eyes added nothing this time.** The 340 removals and the transition log are
strictly stronger than a human watching one train: they cover seven trains over
238 s and they can fail. The owner's value here was assurance, not information
— which is exactly what the Tier A/B split is supposed to detect. **Recommend
reclassifying this rider A → B.**

---

## CARD 2 — F11: which call cleans `train.units` on a CROSS-MAP abduction?

**Scenario.** Run 2, cold load, speed 3. The leg **selected for cross-map** —
an off-`MainMap` train rider plus a landed surface `UniversalZeusRocket` — and
asserted `cross_map == true` before driving anything. Co-run #0's pair was
same-map, so `OnTransferToMapDone` never fired and routes (a)/(b) were
untouched; this leg refuses to run at all unless the pair is genuinely cross-map.

**Forced:** the abduction — `col:SetCommand("EnterTransporter", rocket)`,
verbatim the body of `CargoTransporter:ExpeditionLoadCrew`
(`CargoTransporter.lua:300-302`), driven on a chosen target instead of one the
gatherer picked. **Organic:** the cleanup ordering under measurement.

**Instrument.** ⚠️ The upstream note asked for a wrap of `Holder.OnExitHolder`
"printing its caller". **That is not available:** `debug` is on
`ModEnvBlacklist`, so no stack can be read from mod code. The instrument is
**order** instead — `Unit.EnterTransporter`, `Unit.OnTransferToMapDone`,
`Unit.SetHolder` and `Holder.OnExitHolder` all stamp one shared sequence
counter, so nesting is directly readable. `OnTransferToMapDone` is a COMBINED
method (`_cobject.lua:158`), so its wrap sits on the classdef at mod-file scope.

**Raw log, the whole transfer:**

```
L3 FIXTURE found after 1 sweep(s): rider=Colonist#2000029925 train=Train#2000035273 rocket=UniversalZeusRocket#1061
L3 cross_map=true
L3 BEFORE find=1/4 holder=Train#2000035273 #units=4
L3 FORCED: col:SetCommand("EnterTransporter", rocket)
TRACE #1 EnterTransporter ENTER unit=Colonist#2000029925 holder=Train#2000035273 find=1/4 cross_map=true
TRACE #2 OnTransferToMapDone ENTER unit=Colonist#2000029925 holder=Train#2000035273 find=1/4
TRACE #3 SetHolder ENTER unit=Colonist#2000029925 new_holder=nil old_holder=Train#2000035273
TRACE #4 Holder.OnExitHolder holder=Train#2000035273 unit=Colonist#2000029925 find_before=1 #units=4
TRACE #5 SetHolder EXIT  unit=Colonist#2000029925 holder=nil
TRACE #6 OnTransferToMapDone EXIT  unit=Colonist#2000029925 holder=nil find=no-holder
TRACE #7 SetHolder ENTER unit=Colonist#2000029925 new_holder=UniversalZeusRocket#1061 old_holder=nil
TRACE #8 SetHolder EXIT  unit=Colonist#2000029925 holder=UniversalZeusRocket#1061
L3 AFTER find=1/1 holder=UniversalZeusRocket#1061 holder_is_rocket=true Done_fired=1
```

**⭐ What it establishes — ROUTE (a), and route (b) is excluded.** The
`table.remove_entry` that cleans `train.units` runs at **#4**, strictly inside
the `OnTransferToMapDone` bracket (#2…#6), reached through the `SetHolder(false)`
at `Unit.lua:849`. By the time `EnterTransporter`'s own `SetHolder(transporter)`
runs (#7), `old_holder` is already `nil` — **`Unit.lua:1209` does not do the
removal in the cross-map case.** This is the exact discrimination `F11.md`'s
2026-08-03 correction block called unprovable from Lua, and it closes the gap
that block names: *"a post-hoc `find == nil` cannot exclude an ordinary unload
having removed the rider first"* — nothing is post-hoc here, the removal is
observed in place.

**Bonus fact, MEASURED:** `OnTransferToMapDone` fires **synchronously inside**
`EnterTransporter`, i.e. from within `self:TransferToMap(transporter)`
(`Unit.lua:1202-1203`), not deferred to a later frame.

⚠️ **Honest limits.** One instance, one pair, forced upstream — MECHANISM
evidence, and it does **not** upgrade F11's evidence label (rule 11).
`find=1/1` afterwards is an index in the **rocket's** list, not the train's; the
train-side proof is `find_before=1 #units=4` at #4. A wrap on
`Unit.TransferToMap` did not install (`wrap_transfer=nil` — it is not a plain
`Unit` Lua method), so the transfer's own boundary is inferred from the Done
bracket rather than bracketed directly.

**This card is wrong if:** a cross-map abduction is ever observed where
`Holder.OnExitHolder` fires outside the `OnTransferToMapDone` bracket.

⚖️ **Would the card alone have sufficed?** **Yes — this leg never needed eyes
and never had them.** It is the clearest Tier B/C case in the payload.

---

## CARD 3 — C41: can an out-of-range mouse anchor displace the resource picker?

**Scenario.** Two halves across both runs. **L2A (run 1):** poll
`terminal.GetMousePos()` against `terminal.desktop.box` 5×/s for 60 s while the
owner moved the cursor across both monitors. **L2C (run 2):** wait until the
cursor actually *reads* out of range for 3 consecutive polls — the condition is
**detected, not typed** — then open the shipped picker 20 times with F76's own
M2 instrument re-installed (anchor, box, container, scale, live mouse, desktop
box, all on one line). ⛔ The prediction was **written into the log before the
loop ran**, so the leg could not rationalise toward whatever arrived.

**Forced:** the open — `OpenResourceSelector` called directly with
`RCTransport:InteractWithObject`'s own storage-branch context
(`RCTransport.lua:419-424`) rather than reached by a click; and in L2C, the
cursor being parked off-window (the owner's 60 s).
**Organic:** the anchor, which `ResourceItems:Init` reads from the live mouse
either way (`ResourceItems.lua:11`) — the only quantity the lead is about.

**Raw log, run 1 (the excursion is real and frequent):**

```
READ C41 env: desk=(0, 0)-(3840, 2160) scale=(1900, 1900) screen=(3840, 2160) mouse=(6710, 2294)
L2A ⭐ OUT-OF-RANGE mouse=(4075, 1459) desk=(0, 0)-(3840, 2160) (hit 1 of 109 reads)
L2A ⭐ OUT-OF-RANGE mouse=(6226, 1262) desk=(0, 0)-(3840, 2160) (hit 5 of 113 reads)
L2A RESULT 29/300 reads outside desktop.box | x range 0..7665 | y range 0..2559 | desk=(0, 0)-(3840, 2160)
L2B RESULT 20/20 opened, 0/20 missing | layouts logged=51, of which anchor outside desktop.box=0
```

**Raw log, run 2 (the two halves made to coincide):**

```
L2C PREDICTION: safe area 0 0 3840 2160. If the anchor is out of range to the right/bottom, the clamps must put
the dialog at x = 3840 - width ... i.e. hard into the BOTTOM-RIGHT corner, far from where the cursor appears to be.
If instead the box tracks the anchor as usual, the clamps are innocent and C41's M5 lead does NOT produce the symptom.
L2C ARMED — cursor is out of range at (6027, 1266) (3 consecutive reads)
L2C LAYOUT #14 anchor=(6021, 1259) ANCHOR_OUT=true box=(2224, 830)-(3840, 1259) cont=(2096, 830)-(3968, 1202) scale=(1425, 1425) mw=1616 mh=429 mouse=(6021, 1259) desk=(0, 0)-(3840, 2160)
L2C cycle 5/20 dialog=ALIVE mouse=(6021, 1259) mouse_in_range=false anchor=(6021, 1259) box=(2224, 830)-(3840, 1259) AT_BOTTOM_RIGHT_CORNER=false items=9
L2C ⭐ RESULT 20/20 opened, 0/20 missing | cycles whose ANCHOR was out of range=20 | cycles whose box landed in the BOTTOM-RIGHT CORNER=0 | layouts logged=58
```

**⭐ What it establishes, and the prediction was half right — which is the
useful half.**

1. **`terminal.GetMousePos()` returns VIRTUAL-DESKTOP coordinates while
   `terminal.desktop.box` is window-local.** MEASURED: `x` up to **7665**
   against a box that ends at **3840**, `29/300` on an ordinary sweep and
   `20/20` with the cursor parked. F76's M5 was **one** reading and was
   explicitly weakened as *"what an ordinary cursor excursion looks like"*; it
   is now a reproducible, on-demand property of this machine.
2. ⭐ **The safe-area clamp DOES fire for an out-of-range anchor, and F76's
   "the clamps are innocent" holds only for in-range ones.** With
   `anchor=(6021,1259)` and `mw=1616`, the x clamp produced exactly
   `x = 3840 - 1616 = 2224`, `maxx = 3840` — **the dialog pinned to the right
   screen edge while the cursor is 2181 px further right, on the other
   monitor.** That is *"renders far from the cursor"* with a measured mechanism
   behind it, on the very entry whose headline claim was falsified for the
   in-range case.
3. ⭐⭐ **BOTH clamps fire, and the bottom-right corner slam is CONFIRMED to the
   pixel** (run 3). ⛔ **This card first recorded the corner half as REFUTED,
   on the false reason "the second monitor is not tall enough".** Display 2 is
   **3840×2560**, 400 px taller than the game's box; run 2's parked cursor sat
   at `y≈1259` and never sampled the case. **"Refuted" was "unsampled".** Run 3
   sampled it, against a prediction computed from the measured dialog size and
   written to the log *before* any picker opened:

   ```
   PREDICTED  box (2224,1731)-(3840,2160)          x = 3840-1616,  y = 2160-429
   MEASURED   cycle 1/12 anchor=(5305, 2269) x_out=true y_out=true
              box=(2224, 1731)-(3840, 2160)  CORNER=true  items=9  ALIVE
   ```

   All four edges match. The flip branch correctly did not fire. ⚠️ **n = 1**
   (the cursor returned to display 1 afterwards) — but `UpdateLayout` is
   deterministic arithmetic, not a stochastic effect, so the open question is
   whether the *anchor* recurs, not whether the *layout* does. ⭐ F76's pass-#8
   `mouse (6148, 2350)` is exactly this anchor class: `y=2350` is past 2160 and
   inside 2560.

⛔ **What may NOT be claimed.** **The picker appeared 20/20 in both runs**, so
C41's OG symptom — *"the icon does not appear"* — **did not reproduce**, and
`0/40` is a rate bound across 40 forced opens, not a refutation. Nothing here
identifies what the OG witness saw; their monitor layout is unknown. And the
owner would have to be clicking a depot *while their cursor is over a second
monitor*, which is not an ordinary action — reachability for a real player is
**unproven** and is not claimed.

⭐ **ENVIRONMENT RESOLVED (owner's display readouts, 2026-08-04) — and the
"unexplained disagreement" this card first reported was MY measurement error.**
Both displays are natively **3840** wide: Odyssey G7 **3840×2160** at `(0,0)`,
BenQ RD280UG **3840×2560** at `(3840,0)`, so the real virtual desktop is
`0..7680 × 0..2560`. My PowerShell `Screen` read returned `2560×1440` /
`2560×1707` because the process was **not DPI-aware** and Windows is at 150%.
The game's `desktop.box (0,0)-(3840,2160)` is **exactly display 1's native
pixels**, the measured `x` max of **7665** is inside 7680, and the `y` max of
**2559** is display 2's 2560. **Everything closes to the pixel**, which upgrades
the finding: `GetMousePos` returns raw virtual-desktop coordinates while
`desktop.box` covers the game's display only, so **every** cursor position on
display 2 is out of range by construction. ⛔ Also withdrawn: the claim that the
setup differs from the 2026-08-02 F76 sitting — it is identical.

**This card is wrong if:** a repeat with the cursor parked shows the box
tracking the anchor past `3840`, or if `desktop.box` and `GetMousePos` are ever
measured in the same coordinate space on this setup.

⚖️ **Would the card alone have sufficed?** **For half of it, no.** L2C's
*measurement* needs no eyes — but it needs the cursor physically parked on
another monitor, which is a human hand, not a human eye. The Tier A/B rule asks
"would eyes add information the log cannot carry"; the honest answer here is
that **eyes added nothing and hands added everything**, which is a distinction
the draft tier rule does not make. ⭐ **Recommend prompt 4 add it.**

---

## CARD 4 — F99: on a hex holding a hidden broken element and its repair site, what does `HexGetTrackGridElement` return?

**Scenario.** Run 1, last leg, deliberately ordered after everything else
because it mutates the world it measures. The save carried **926** track
elements and **0** broken ones, so the break had to be staged.

**Forced:** the break — `track:BreakTrackElement(element)`.
**Organic:** nothing; and ⚠️ **no repair is measured here at all**, so F99's own
constraint (the break may be forced, the **repair** must stay organic) is
untouched. The no-cheat discriminator was explicitly out of this run's scope.

⚠️ **The break used a better route than the spec named, and this is a spec
correction.** `CORUN_RIG_SPEC.md` §6 says `CheatMeteors` at a position.
`BreakTracks` (`Meteors.lua:599-607`) — which is what that cheat eventually
reaches — calls `track:BreakTrackElement(element, cg)` on each element that is
neither `start_el` nor `end_el` and carries no station. The leg calls **that
site directly** on one chosen element matching the same filter: same mechanism,
no disaster thread, no collateral damage, and the lottery removed. That is
`WORKFLOW.md`'s own leg-design rule 2 ("delete the lottery"), and it is how the
F11 sitting was run.

**Why there is a tie-break at all, re-derived rather than inherited.** The
repair site **is** a `TrackGridElement` — `TrackConstructionSite.__parents =
{ "ConstructionSite", "TrackGridElement" }` (`TrackElement.lua:580-584`) — and
`BreakTrackElement` only *hides* the broken element, leaving it on its hex
(`element:SetVisible(false)`, `Track.lua:636-639`). So both objects genuinely
match the class filter in `hex_grid:GetObject(q, r, "TrackGridElement")`
(`HexGetTrackGridElement`, `TrackElement.lua:1-3`). ⚠️ `F99.md` calls this link
a "C binding"; the Lua wrapper is one line and the C part is `GetObject` — the
question is answerable by one runtime call, which is what this leg is.

**Raw log, before and after:**

```
READ L4 fixture: 17 track(s), 926 element(s), 0 already broken
L4 CONTROL (before the break) hex=(129,450) HexGetTrackGridElement -> TrackGridElement#4573 | is the element itself=true
L4 FORCED: track:BreakTrackElement(element) — the shipped call site BreakTracks uses (Meteors.lua:604), on a chosen element. track=TrackBase#4569 element=TrackGridElement#4573
L4 STATE after break: element=TrackGridElement#4573 visible=false | site=TrackConstructionSite#14605 site.broken==element=true | site is a TrackGridElement=true
L4 both candidates occupy the same hex: element q,r=(129,450) site q,r=(129,450)
L4 ⭐ TIE-BREAK READ: HexGetTrackGridElement(hex_grid, 129, 450) -> TrackGridElement#4573  ==> THE HIDDEN ELEMENT
L4 CONFIRM (2 s later): -> TrackGridElement#4573 | same as first read=true
```

**⭐ What it establishes.** The hex grid returns **the hidden broken element**,
not the repair site, with both alive on hex `(129,450)` and both of the
qualifying class. `F99.md` closes its mechanism block with *"The one link not
readable from Lua: `HexGetTrackGridElement`'s per-hex tie-break… The seven live
throws are the evidence it resolves to the element."* **That inference is now a
measurement, taken directly rather than back-inferred from a crash.** The
consequence the entry draws stands: `process_alien_elements`' neighbour walk
(`TrackElement.lua:705-711`) sees the broken element, absorbs it into the
completing neighbour's track (`:729`, `:737`), and leaves the original track a
husk — which is the drain that empties `elements` before `TrackElement.lua:803`.

**Controls that make it honest.** The pre-break read returned the same object
when it was the *only* candidate, so the post-break read is a comparison, not a
bare assertion; `site.broken == element` and `element:GetVisible() == false`
confirm the two are the paired break state and not unrelated neighbours; and
the read was repeated 2 s later in case placement was deferred — same answer.

⛔ **What may NOT be claimed.** One hex, one break, one save. This settles the
*tie-break*, not F99's reachability: no-cheat reachability remains UNPROVEN,
FIX_POLICY §4 still bars building, and the entry stays `cand`.

**This card is wrong if:** the same read on a hex where the site was placed
*before* the element was hidden returns the site — i.e. if the tie-break is
insertion-ordered rather than class-ordered. Not tested.

⚖️ **Would the card alone have sufficed?** **Yes — no eyes, and none were
asked for.** This is the ride-along class the spec predicted would be free, and
it was: it cost 3 s of a 398 s cycle.
