# Chain 5b — F86 Tier 2: run the leg, then unlock what the leg unlocks

**One-off; delete this file in your final commit. Read `README.md` in this
folder first.** Continuation of prompt 5 (self-split, chain rule 3): **the four
Tier-2 builds and the design pass are DONE and committed.** What is left is the
one thing that needs the owner at the keyboard, plus everything gated behind it.

**Staleness check: `git log --oneline -10` + `git pull`.** Authority for shapes:
`docs/reports/SAVE_SAFETY_REDESIGN.md` §5/§6 + `FIX_POLICY.md` §3a.

## Jobs (todo list first; one item per commit-and-verify unit)

1. **Run PT-58** (`PLAYTEST_CHECKLIST.md`) — the single Tier-2 leg, **attended,
   owner at the keyboard**. PT-00 sweep first (it was clean at `ef7d49c`; run it
   again anyway). **The seven predictions P1-P7 are already written down** — do
   NOT rewrite or soften them; read the leg against them and record what each
   one actually returned. Loggers are per-session: arm them AFTER every restart.
2. **Record the leg** — readings into PT-58's `Result:` line, the F86 entry's
   Site 2 block, and STATUS. If P5 reads zero, **F86 Site 2 is CLOSED** and says
   so in the index row, the heading tag and STATUS.
3. **Status flips the leg earns, and only those.** `F53` and `F55` are `fixed`;
   flip to `tested` only against live readings, **index row AND heading tag
   both**. `F21` is `fixed` (downgraded from `tested` in `44e6af2` — PT-43
   measured a body that no longer ships); it re-earns `tested` only via PT-58's
   optional train re-take, **never on the probe alone**.
4. **The D10/D12 UNHOLD — gated, and this is the gate.** The owner's condition
   was "repairs land AND verify". They have landed; this leg is the verify.
   **After** the leg's numbers are quoted: record the unhold in STATUS and on
   **both** D-entries. Prompts 9/10 become runnable at that moment and not
   before. ⛔ If the leg fails a prediction, the unhold does not happen — stop,
   report, the chain waits.
5. **MOD_DESCRIPTION's no-precedent sentence — the unlock is yours now.** The
   `[DRAFT NOTE — CONDITIONAL]` at `MOD_DESCRIPTION.md:59` is intact and the
   sentence is **unchanged and unsoftened** — it ships whole or not at all. Its
   gate reads **Tier 2**, and it names Site 2's 80 orphan errors as the specific
   blocker. **If PT-58 reads clean across the whole pack on uninstall, delete
   the note and keep the sentence verbatim.** If it does not, leave both alone
   and say why. ⚠️ The note carries a do-not-delete-on-the-old-reading warning
   because its gate was already corrected once — respect it.

## Scope fence

**In:** the leg, its records, the flips it earns, the unhold, the
MOD_DESCRIPTION unlock, the outbox. **Out:** re-litigating any Tier-2 shape
(they are built and reasoned on their entries — challenge them with a *reading*,
not an opinion); layer 1 (⛔ the four own-thread modules + `BombardmentSpread`
are the accepted residual — do not re-propose); the §5.4-A conversions (prompt
8); anything drone beyond what already landed; D10/D12 themselves.

## Stop conditions

- Any prediction misses → stop, report, chain waits. **A missed prediction is
  the finding** — record it, do not explain it away.
- The leg cannot run this session (owner unavailable) → do the *records* work
  that does not depend on it, then hand this file forward unchanged.
- Context pressure → self-split (`5c_…_opus.md`).

## What may not be claimed

The unhold may not be recorded before the leg's numbers are quoted. No entry may
flip to `tested` on a probe result alone. "Site 2 closed" requires the orphan
count from an actual uninstall load, not the absence of one.

## On completion

Outbox → `6_audit_candidate_sweeps_opus.md` (state) AND, if anything is left
owed, → prompt 12's inbox. Delete this file, commit, push.

---

## Notes from upstream

### From chain prompt 5 (Tier-2 build, 2026-08-01) — BUILT, NOT VERIFIED

**What landed, with commits.** `88f3154` (F55 drone half → the sync consumer),
`44e6af2` (F21 → the sync `AddSpentTime`; F21 downgraded `tested`→`fixed`),
`6f0cb95` (F53 both halves, off `Colonist:Arrive`), `ef7d49c` (F86 Site 2 →
the sync `Drone:CleanUnreachables`), `e197190` (PT-58 + the per-site disposition
table + STATUS). TestKit `6eb3c0b`, `7bfa274` (probe realigns), local-only.

**Every Tier-2 module is off its blocking body.** The per-site disposition table
is in STATUS; each entry carries its own reasoning. In one line each:

| site | seam it sits on now | disposition |
|---|---|---|
| `Fix_DroneUnreachableForever` | pre-wrapper on the sync `Drone:CleanUnreachables`; `ts > GameTime()` → `ts - max_int` recovers the exact failure time | layer 3, no residue |
| `Fix_TrainWaitTime` | wrapper on the sync `TransportStatistics:AddSpentTime`, keyed `IsKindOf(self,"Station")`; boarding colonist found by `command_thread == CurrentThread()` | layer 3, no residue |
| `Fix_ArrivalDeaths` (a) | pre-wrapper on the sync `Colonist:OnArrival` | layer 3, no residue |
| `Fix_ArrivalDeaths` (b) | pre-wrapper on `Colonist:Idle` keyed `self.arriving`; `return orig_idle(...)` with nothing after | layer 2 — **one inert captured frame, accepted and disclosed** |
| `Opt_DroneOverhaul` (**Site 2**) | post-wrapper on the sync `Drone:CleanUnreachables` gated `self.command == "Idle"` | layer 3, no residue |

**⭐ The half-(a) design pass §6.2 booked as owed was RUN, and it found a route
— so it was built, not deferred.** The plan's warning was that the raw `SetPos`
sits in a destructor after a `Sleep`, on an upvalue captured at `Colonist.lua:1281`
that nothing outside can change. The answer is that the fix never needed to
change `pos`: it needs the colonist to *end up* somewhere walkable, and
`Colonist:OnArrival` is a shipped, arrival-specific, **verified synchronous**
seam that runs after the placement — and, on the walking path, inside
`SetCommand`'s destructor pass *before* `TransportByFoot` starts
(`CommandObject.lua:225-235`). Nothing was routed to prompt 12; the stop
condition did not fire.

**⚠️ Three things the leg should be read against, because they are the places
this build could be wrong:**
1. **`Fix_TrainWaitTime`'s colonist identification** is the cleverest thing in
   the tier and the likeliest to be subtly wrong. It scans
   `station.waiting_for_train` for `command_thread == CurrentThread()`. The
   reasoning is sound (`BoardVehicle` is a command, `Train.lua:967`; the colonist
   is removed from that list later, in the destructor at `:517`) but it has never
   run against a live station. **P3 and the optional train re-take are what test
   it.** A silent miss looks like F21 simply not being fixed — not like an error.
2. **`Fix_ArrivalDeaths` (b) checks from the ROCKET's position**, not the
   colonist's, because the colonist is not placed until Arrive's disembark
   destructor. That is the same reference point the original assignment used
   (`RocketBase.lua:1981`, `:2029`), but it is a change from the old body, which
   checked from the disembark point. A cross-map/elevator arrival is the case to
   watch (SAVE-E sitting, PT-18 covers the shape).
3. **`Opt_DroneOverhaul`'s gate is `self.command == "Idle"`.** Verified against
   `CommandObject:DoSetCommand` (`:341`, sets `self.command` before the thread
   starts) and against the other two `CleanUnreachables` call sites, which are
   under commands `Deliver` (`Drone.lua:1247`) and the recharge path (`:1287`).
   If moonlighting silently stops happening, this gate is where to look —
   `SMRFixPack.DroneReport()` prints the `moonlighted` counter.

**Two recorded claims were corrected rather than quietly dropped** (both are the
"recorded facts are claims too" failure mode):
- `Opt_DroneOverhaul`'s header said *"saves made with the module enabled load
  identically without it"*. **False** — Site 2 is the counter-example. The header
  now carries the measurement and the repair.
- F21's entry said *"no wrapper can run in time"*. Right about `BoardVehicle`,
  wrong about the repair — it only ever asked whether that one body could be
  wrapped. Struck with the reason.

**`ChooseDome` was deliberately NOT wrapped**, though §6.2's route line names it
and it is where F53's bad fallback is born. Eight shipped call sites
(`DroneFactory.lua:224`, `RocketBase.lua:1985/:2068/:2105`,
`CargoTransporterNew.lua:907/:951/:975`, `Colonist.lua:1149`); only the arrival
ones are F53's subject, and suppressing the fallback globally would change
android spawning and the "Abandoned" path (which has its own oldest-failed-dome
fallback and its own walking-distance test at `:1149-1163`). No evidence stands
behind either change — FIX_POLICY §4 — and §5.3 requires the narrowest key that
separates the sites, which is `self.arriving`. **The sweep's route was followed
in substance: the re-choose still runs on `ChooseDome`/`GetDomesReachableByColonists`,
it is just invoked from a keyed seam instead of from a global wrapper.** If a
later session wants the global version, it needs evidence for the other six
sites first.

**The carve-out was honoured, not stretched.** The `Opt_DroneOverhaul` change
moved the hook's call position and nothing else — vanilla has no statement
between `self:CleanUnreachables()` and the end of `Idle`, so the trigger
condition, the ordering and the code that runs are identical. No drone-design
judgement was required, so nothing needed asking. PT-52 stays frozen; the D06
rebuild decision is untouched.

**Instruments and facts a leg author needs.**
- **Probe sweep CLEAN** (zero `TEMPORARY` hits, both repos) at `ef7d49c`.
- **Three probes were realigned** because they asserted behaviour the pack no
  longer replaces: `ArrivalDeaths` (drove `FromFixPack(Colonist.Arrive)` — now
  the thing that must be **false**), `DroneUnreachableForever` (drove
  `Drone:ApproachWrapper`, vanilla's again — it now drives ApproachWrapper *and*
  CleanUnreachables in vanilla's own order), `TrainWaitTime` (its stand-in
  station now borrows the **real** wrapped `AddSpentTime`).
- **`TrainWaitTime` and the realigned `ArrivalDeaths` need a thread context** —
  a bare console `RunAll` has none. Use `*r SMRTest.RunAll()`; the probe SKIPs
  with that pointer rather than failing.
- **`tools/blocking_analysis.py`** is the instrument every "verified synchronous"
  claim in this tier cites. It takes a JSON list of `[label, name]` pairs. Every
  seam used here reports `clear`; `BoardVehicle` and `Arrive` report `BLOCKS`,
  which is the control.
- Everything Tier 1 recorded still applies: per-env specials refuse
  `SetGlobal`/`WithGlobals` (`Msg`, `OnMsg`, `rawget`, `getmetatable`, `os`,
  `_G`); `IsValidThread` returns NO value on load — read liveness via
  `SMRTest.FixtureCarry()`; FixtureCarry cannot see label modifiers and says so;
  loggers are per-session and a restart clears them; F89 is open and its
  event-spawn caveat stretches meteor detection latency by design.

**➡️ ONE DISCOVERED ITEM, ROUTED (chain rule 2).** Asked at the keyboard before
the run: would an asserts build let the `[install]` probes read? Answer recorded
in PT-58 — it needs MarsDebug **plus** `SMRTest.EnableIntrospection(debug)` typed
into the un-sandboxed console, because the mod sandbox applies on all builds
(verified 2026-07-26). Not done for PT-58, for a stated reason. **But it would
clear the EIGHT `[install]` probes that SKIP on every retail run — coverage this
project has never had.** It is TestKit coverage, not F86 work and not chain work,
so it does not belong to any numbered prompt: **carry it to prompt 12's inbox as
a standing follow-up** unless PT-58 gives it a home sooner.

**Lineage:** every Tier-1 leg ran on test-2 (`save_game_id HdmSxGs6kyd0uz6-`),
and the re-cut uninstall article is `T1-UNINSTALL` / `t10uninstall-r`. PT-58's
P5 comparison figure (**80**) comes from that lineage, log
`Mars.exe-20260801-19.14.11`. Compare like with like or say that you did not.

### Carried forward from chain prompt 4b, still live

- **F89 (`94cfa46`) is filed and open** — vanilla's drain loop wedges the
  *Meteors* thread on ordinary strikes; covered by the F02 watchdog, no direct
  fix routable. Two caveats: event-spawned meteors **re-arm** the watchdog's
  liveness clock (accepted by design), and leg 5's extra vanilla sighting is
  **uninstrumented** — do not upgrade it to a measurement.
- **The natural storm's 74h UI countdown was read with the pack ON.** A Tier-2
  sitting seeing storm warnings near ~90h means the wrapper key is leaking;
  F02's entry says where to look.
- **⛔ Do not read the per-site release gate as permission to descope.** Build
  every reachable repair now; a cleaner hand-off is a valid disposition only
  *after* the in-pack attempt has been made and the route proven absent. D13's
  target list is the **output** of the builds, which is why it cannot be specced
  first — and D13 derives the exposed set itself, so **no count recorded in these
  docs is authoritative**, including the ones prompt 5 left behind.
