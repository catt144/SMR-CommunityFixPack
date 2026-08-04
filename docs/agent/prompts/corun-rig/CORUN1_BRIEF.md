# CO-RUN #1 — the sitting brief (measure moments, verdict words, probe source)

Written by chain prompt 3 (Opus, 2026-08-04) during unattended prep. **The
owner reads only §1 and §2.** §3–§5 are the agent's arming procedure and the
probe's source, parked here because probe hygiene **rule 5** says a probe file
is present in `Code/` only while its run is actually happening — a probe parked
in a doc is inert by construction, since the mod loads only the files listed in
`metadata.lua` `code`, all of which live under `Code/`.

⚖️ **The one-time armed-prep override granted to this prompt was DECLINED, on
purpose.** Reasoning and the measurement that replaces it: §6. Nothing in this
prep is armed; `doccheck.py` is green and no `--no-verify` was used.

---

## §1 What this costs you, and when

**Promised: ~15–20 min. Designed: ~7 min of your attention, in one block.**
You are needed for legs 1 and 2 only; legs 3 and 4 need no eyes and run after
you leave. I will tell you in chat when to sit down — the game will already be
loaded and warmed up, so there is nothing to wait through.

Two things about the console before we start, both from `PLAYTEST_HELP.md`:
the console auto-opens once the colony is up, and **one command per line**.

| # | moment | what you do | how long | verdict words |
|---|--------|-------------|----------|---------------|
| 1 | **F11 unload watch** (Tier A) | The camera is already on the fullest passenger train. Watch it reach a station, unload, and pull away. | ≤3 min | **"train left"** / **"train stuck"** |
| 1b | when you have seen one | type `CoRun1_Go = 1` | 5 s | — |
| 2 | ⭐ **THE ONE ASK — C41 mouse sweep** | Move the mouse around for ~60 s: over the game, to the screen edges, and **onto your second monitor and back**. That is the whole task. | 60 s | — |
| 2b | when done | type `CoRun1_Go = 2` | 5 s | — |
| 3 | **C41 picker watch** (Tier A) | I open the depot resource picker 20 times in a row. Watch whether it **appears** each time. Call out any cycle where it does not. | ~40 s | **"picker appeared"** / **"picker missing on cycle N"** |
| 4 | you are free | type `CoRun1_Go = 3` and go | 5 s | — |

**Why moment 2 is worth your 60 seconds, stated plainly so you can veto it.**
C41's only *measured* lead is that `terminal.GetMousePos()` can return
coordinates outside `desktop.box` — the F76 sitting caught it once,
`mouse (6148,2350)` against `desk (0,0)-(3840,2160)`, and an out-of-range
anchor is the one mechanism anyone has that would make the picker open where
the player is not looking. Your machine reads **two monitors** —
primary `(0,0)-(2560,1440)`, second `(2560,0)-(5120,1707)` — so a cursor
excursion onto the second monitor is exactly the condition the lead names, and
it is reproducible on demand. Nothing else in the payload can produce it, and
no amount of agent-side looping substitutes for the cursor actually being over
there. ⚠️ **Recorded, not reasoned away:** that monitor layout is *not* the one
the 2026-08-02 F76 sitting measured (`desk` was 3840×2160 then). The setup has
changed since, or the game was on a different display. §2 reads `desktop.box`
live rather than inheriting either number.

If moment 2 is not worth it to you, say so and it drops — the rest of the run
is unaffected and C41 keeps its `cand` status either way.

**If your window collapses:** finish moment 1 and leave. Moments 2–3 become a
`TAKEABLE IN a co-run` rider with the measured cost attached, not a dropped
item.

---

## §2 What is being measured, and what would falsify it

Nothing here is claimed in advance. Each leg names what was **forced** and what
stayed **organic** (`WORKFLOW.md` "Co-runs", rule 11).

### L1 — F11 pre-wrapper conversion (checklist rider "verify the pre-wrapper conversion")

The 2026-08-03 conversion from a ~30-line full copy to a 10-line pre-wrapper is
behaviour-preserving **by construction** and has never run. The rider's own
terms are three readings, and this leg takes all three:

- `TrainPlatformWedge` reads **active** — read from `SMRFixPack.fixes`, not assumed.
- **Trains unload and LEAVE.** Liveness witness: your eyes. Objective counter
  beside it: every train's `command` and `#units` are polled once a second and
  every transition is logged; a train sitting in `UnloadTrain` for >20 game-hours
  while `#units` never falls is logged as a **WEDGE CANDIDATE**.
- **Disembark stat changes still happen.** `Colonist.ChangeComfort` and
  `ChangeSanity` are counted for the two reasons the shipped body passes —
  `"travel time"` and `"seen forest"`. ⚠️ The comfort call is skipped by design
  when `LuxuriousTrains` is researched, so the leg **reads that tech first**:
  a counter that cannot fire is not a counter.

**This falsifies the conversion if:** a train wedges, or zero `"travel time"`
comfort calls arrive while `LuxuriousTrains` is *not* researched and unloads
demonstrably happened. Then the copy form comes back from `3a6512f^`.

⛔ `Colonist.ExitVehicle` is deliberately **not** wrapped — it is the fix's own
target, and instrumenting the function under test would put a TestKit frame on
the measured path. The leg reads effects only.

### L2 — C41 picker (`cand`; instrument = the F76MISS shape)

Two halves. **L2A** polls `terminal.GetMousePos()` against `terminal.desktop.box`
five times a second for 60 s and counts excursions — this needs no picker at
all and is a direct amplification of the F76 pass-#8 anomaly. **L2B** opens the
shipped picker 20 times with F76's own M2 instrument re-installed (anchor, box,
container, scale, live mouse, desktop box — all on one line, which is what the
2026-07-27 forensics never had).

**Forced:** the open — `OpenResourceSelector` is called directly with
`RCTransport:InteractWithObject`'s own context (`RCTransport.lua:419-424`)
rather than reached by a click. **Organic:** the anchor, which
`ResourceItems:Init` reads from the live mouse either way — and the anchor is
the only quantity the lead is about.

**The false positive this leg is built to exclude:** `ResourceItems:GetItems`
closes the dialog when it has nothing to show (`ResourceItems.lua:80`), which
looks exactly like C41's symptom. The item count is logged per cycle, so
"missing with 0 items" (a data condition) can never be reported as "missing".

⛔ **0/20 will not be reported as a refutation.** Absence under 20 forced
cycles is a rate bound; the number gets said.

### L3 — F11 cross-map `OnTransferToMapDone` timing (ride-along)

Co-run #0's pair was same-map, so Done never fired and routes (a)/(b) were
untouched. This leg **selects for cross-map** — an off-`MainMap` train rider
plus a landed surface rocket — and **asserts `cross_map == true` before driving
anything**; if the pair is same-map the leg aborts rather than repeat #0.

**The instrument is ORDER, not a stack trace.** `debug` is on
`ModEnvBlacklist`, so "print the caller" is not available from mod code. Four
wraps stamp one shared sequence number — `Unit.EnterTransporter`,
`Unit.OnTransferToMapDone`, `Holder.OnExitHolder` — so a `Holder.OnExitHolder`
landing *between* Done's ENTER and EXIT is route **(a)**, and one landing
inside `EnterTransporter` with no Done bracketing it is route **(b)**. That
closes the gap the F11 entry names: *"a post-hoc `find == nil` cannot exclude
an ordinary unload having removed the rider first."*

**Forced:** the abduction (`col:SetCommand("EnterTransporter", rocket)`,
verbatim `CargoTransporter:ExpeditionLoadCrew`'s body, on a chosen target).
**Organic:** the cleanup ordering under measurement. MECHANISM evidence only —
it does not upgrade F11's evidence label.

### L4 — F99 hex tie-break (ride-along; runs LAST because it mutates track)

`F99.md`'s last unsettled link: *"`HexGetTrackGridElement`'s per-hex tie-break
between the hidden element and its site."* The tie-break is real — the repair
site **is** a `TrackGridElement` (`TrackConstructionSite.__parents =
{ "ConstructionSite", "TrackGridElement" }`, `TrackElement.lua:580-584`), the
broken element is only hidden and stays on its hex (`BreakTrackElement`,
`Track.lua:636-639`), so both match the class filter in
`hex_grid:GetObject(q, r, "TrackGridElement")` (`TrackElement.lua:1-3`).

⚠️ **The break is forced by a better route than the spec named.** The spec says
`CheatMeteors`. `BreakTracks` (`Meteors.lua:599-607`) — the code `CheatMeteors`
eventually reaches — calls `track:BreakTrackElement(element, cg)` on each
element that is neither `start_el` nor `end_el` and has no station. This leg
calls **that** call site directly on one chosen element: same mechanism, no
disaster, no collateral, and the lottery removed. That is the technique
`WORKFLOW.md`'s leg-design rule 2 already endorses.

A control read runs **before** the break (the hex must return the element when
it is the only candidate) and the post-break read is taken twice, 2 s apart, in
case placement is deferred. ⚠️ F99's own constraint is untouched: the **break**
may be forced, the **repair** must stay organic — and no repair is measured
here. The no-cheat discriminator is explicitly out of scope for this run.

---

## §3 Arming procedure (agent, at the sitting)

1. Write §5's block to `C:\Dev\SMR-BugFixPack-TestKit\Code\97_CoRun1.lua`.
2. Add `"Code/97_CoRun1.lua",` to the `code` list in the TestKit's
   `metadata.lua`.
3. Parse sweep the real file (python + `luaparser`, `utf-8-sig`).
4. Launch: `& "c:\program files (x86)\steam\steam.exe" -applaunch 3215050`
   — **no `-smrautorun`**, so `95_AutoRun` stands down by itself.
5. ⛔ Stage the TestKit **by path, never `git add -A`**: an uncommitted
   comment-only change sits in `Code/96_AutoRunFlag.lua` and is under
   investigation by prompt 4 by the owner's explicit instruction.
6. Result commit deletes the file AND the metadata line, carries a
   `PROBE SWEEP:` line, and archives the log with `git add -f`
   (`.gitignore` line 2 is `*.log` and a plain `git add` drops it silently).

**Staged save:** `CORUN1.savegame.sav`, a `Copy-Item` copy of `TEST2H TRAIN`
(55,667,524 bytes) made with the game closed. The campaign save is never
written. The copy is deleted in the result commit.

## §4 Cost accounting (⛔ correction C1 binds)

`RealTime()` deltas do **not** advance across a loading screen — they
under-reported co-run #0's load 11.5× (864 ms vs 9,968 ms; `facts/EF-045`). The
probe's own `STEP … END Nms` lines are honest for non-loading steps only. **The
load is timed from the engine's own `Game loaded on map … in Nms` line**, the
whole cycle from `Time (ms)` at shutdown, and the launch from OS timestamps.

## §5 The probe source

```lua
--8<-- Code/97_CoRun1.lua (TestKit) — written at the sitting, deleted in the commit that records the answers
```

The source is held in [97_CoRun1.lua.txt](97_CoRun1.lua.txt) beside this file —
a `.txt`, so it is not a Lua file in `Code/` and cannot arm anything, and so
this brief stays readable. Parse sweep **GREEN** on that exact text, run during
prep (see §6).

## §6 ⚖️ The armed-prep override: declined, and what was measured instead

The owner granted this prompt a one-time override of probe-hygiene rule 5 for
its prep, with `--no-verify` authorised for one named commit. **It was not
used.** The reasoning, and the measurement prompt 4 actually asked for:

- **What the override buys is exactly the cost of arming at the sitting** —
  writing one file and adding one `metadata.lua` line. That cost is measured at
  the sitting and reported in the outbox. Declining the grant and timing the
  alternative is a *control*; using the grant would have measured nothing.
- **`--no-verify` has a real price**: a red `doccheck` in the history and a
  bypassed hook, against a saving of seconds of agent time and zero owner time.
- **The disarm deadline is a live risk.** The grant rests on the sitting
  happening in the same session; declining removes that failure mode entirely.
- ⭐ **Prompt 2's "known weak spot" in rule 5 does not exist.** The claim is
  that rule 5 pushes syntax errors to the sitting, and the proposed mitigation
  was to paste the file into `Code/`, sweep it, and delete it again. That round
  trip is unnecessary: the parse sweep is `ast.parse(open(f,
  encoding='utf-8-sig').read())` and **does not care where the file lives**. It
  ran GREEN during this prep on the source at its parked path, with nothing ever
  placed in `Code/`. Rule 5 costs the parse sweep nothing at all.
- ⭐ **MEASURED AT THE SITTING: arming cost 0.4 s** of machine time (file write
  + `metadata.lua` line + parse sweep) and **zero owner time**. That is the
  whole of what the override would have bought. **Recommendation: rule 5 stands,
  no permanent hatch is needed.**
- ⚠️ **A real rule-5 cost, which did bite:** co-run #0's probe source exists
  **nowhere** — created in `Code/`, run, deleted, never committed — so this
  session re-authored the harness from `95_AutoRun.lua`. Rule 5's own
  prescription would have preserved it; co-run #0 simply predates the rule.

## §7 RUN 2 — the two gaps run 1 left

Run 1 settled payload items 1 and 2 and left two things open, both cheap, so a
second launch was authored from its own log and run in the same sitting:

- **L2C — the C41 discriminator.** Run 1 proved both halves of the lead
  *separately* and never made them coincide: 29/300 mouse reads out of range,
  and 20/20 picker opens with 0/51 out-of-range anchors, because by then the
  cursor was back over the game. L2C waits until the cursor **actually reads**
  out of range and only then opens the picker. ⭐ **The condition is DETECTED,
  not typed** — see the gate lesson below.
- **L3 — the cross-map trace.** Run 1's selector sampled once and found no
  off-map rider aboard anything, 345 s of speed-3 play after the census had read
  12. It needed to *wait* for the fixture, not sample for it. The retry version
  found it on its first sweep.

⛔ **The gate lesson, and the owner found it, not me.** §1's table told the owner
to type `CoRun1_Go = 2`. **No such gate existed in run 1's code** — it was only
an early exit from a fixed 60 s timer, so the run proceeded without them. They
noticed and asked whether that was correct. No evidence was lost, but the brief
and the probe disagreed and **the brief was the one lying**. Run 2 fixes the
class rather than the instance: it polls for the condition it needs instead of
asking for a token. **A detected condition cannot be mis-documented and cannot
be missed.** (Typed gates do work — `GATE 1 RELEASED by owner` — they are just
one more thing to keep in sync.)

Run 2's source is parked beside this file as
[97_CoRun1b.lua.txt](97_CoRun1b.lua.txt); parse sweep GREEN on that exact text.
Both probe files and their `metadata.lua` lines were deleted, and the staged
save with them, in the commits that record the answers.
