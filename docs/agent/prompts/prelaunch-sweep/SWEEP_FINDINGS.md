# Sweep findings — ⛔ NOT FOR THE NEXT LINK

⛔⛔ **IF YOU ARE RUNNING `01_LINK.md`, CLOSE THIS FILE NOW.** Reading it
contaminates you, and contamination is the one thing this chain is built to
prevent — the owner's whole design is that each session sweeps without knowing
what the last one found, so that a fresh pair of eyes stays fresh.

**Readers, and only these:** the **owner**, and the **terminal audit**
(`99_TERMINAL_AUDIT_fable.md`).

⚠️ If you opened this by accident, **say so in your report.** A contaminated link
is still useful. A contaminated link that hides it corrupts the chain's only
convergence signal.

---

## Format — append, never rewrite

```
### Link N · lens <name> · <commit>

| # | finding | severity | route | disposition |
|---|---|---|---|---|
| N.1 | one sentence | launch-blocking / real / cosmetic / unmeasured | where it went | fixed <sha> / recorded / routed to checklist NN |

**Evidence per finding** — the ROUTE re-derived, not citations inherited.
**What I could NOT reach** — mirrors this link's ledger row.
```

**Severity words, used strictly:**

| word | meaning |
|---|---|
| **launch-blocking** | a player would hit it, or it would ship something false. ⛔ Fixed immediately at any link |
| **real** | a genuine defect that is not launch-blocking |
| **cosmetic** | comments, naming, tidiness — ⚠️ two consecutive cosmetic-only links trip stopping-rule clause 2 |
| **unmeasured** | you found the question but could not answer it. ⛔ Legitimate, and it must ALSO appear in the ledger's *NOT reached* column |

---

## Pre-chain findings — 2026-08-17, before the chain existed

Recorded here so the terminal audit has the full body of work in one place.

### Seed · the upload sitting · `7824cbc`, `2f077e8`

| # | finding | severity | disposition |
|---|---|---|---|
| S.1 | `metadata.lua` had **no `image` field**; `PDX_PrepareForUpload` rejects on `mod.image == ""` before packing anything | **launch-blocking** | fixed `7824cbc`; `tools/upload_preflight.py` now guards it permanently |
| S.2 | Every Mod Editor save runs `version = version + 1`, and the upload forces a save when dirty ⇒ 1.0.1 against the ruled 1.0.0 | **launch-blocking** | fenced: `image` hand-written so the mod loads clean; `IsDirty()` measured **false** in game |
| S.3 | Paradox saves AFTER upload, Steam saves BEFORE packing ⇒ **Paradox must upload first** or it ships 1.0.1/1.0.2 | **launch-blocking** | recorded, `RELEASE_PORTAL_PREP.md` §0.5(c); Steam's own number routed to checklist 37 Q2 |
| S.4 | `update_suspect` never cleared on success, at **two** sites ⇒ a false *"the game code changed"* dialog on a brand-new release | **launch-blocking** | fixed `2f077e8`; ⛔ **unverified in a running game** |
| S.5 | `Register` appended to `order` unconditionally while state survives `ReloadLua` ⇒ every module double-listed | **real** | fixed `2f077e8`; ⛔ **unverified in a running game** |
| S.6 | ④ sheet claimed the sitting never opens the game; the upload route **is** the in-game Mod Editor ⇒ `EF-056` was live and unguarded | **real** | corrected; pre-copy taken |
| S.7 | ④ sheet's held-saves list named `Autosave Sol 311`, absent from disk (old rotation, ~100 sols back) | **cosmetic** | list corrected |
| S.8 | TestKit's own title still reads *"Community Fix Pack — Test Kit"* | **cosmetic** | ⛔ never player-visible, never uploaded; noted so it is not later mistaken for a rename miss |

**What the seed could NOT reach:** everything in the ledger's seed row — no module
was read, nothing was run in a game, and the mod has never been loaded packed.


---

# LINK 1 — lens L1 (structure & collision) — 2026-08-17

**Artifact:** `docs/agent/reports/L1_COLLISION_MAP.md` (the symbol->patchers map,
plus the C1/C2/C3 analyses and the five exposure shapes).
**Launch-blocking: NO.** **Code changed: NONE** — reasons in the artifact, section 5.

## L1-F1 — `Colonist:Idle` is wrapped twice; the order is load-bearing and unrecorded

The only same-symbol double-wrap in the pack, found mechanically (C2 over 50
class-method targets). `Fix_ShelterReflex:57-58` and `Fix_ArrivalDeaths:170-171`.

Load order = `metadata.lua` `code` list order: ShelterReflex at line 130,
ArrivalDeaths at line 138 => **ArrivalDeaths is OUTER, which is the safe order**,
because ArrivalDeaths only assigns fields and always delegates (`:200`) while
ShelterReflex can `self:SetCommand("Rest")`, which by its own comment "kills this
thread; never returns" (`:70`). Swap the two `metadata.lua` lines and the F53b
dome re-choice is skipped for any colonist meeting the shelter precondition.

Nothing records the dependency: neither header names the other, `FIX_POLICY` 8
covers only "00_Core first", and the `metadata.lua` list carries no note.

- Route: verified at source both ways. Order verified in `metadata.lua`.
- UNMEASURED: whether one colonist can satisfy both preconditions at once
  (`self.arriving` + valid working residence + outside >= half oxygen budget +
  non-breathable atmosphere). No game was run. The order dependency is real
  regardless of whether the overlap is.
- Routed to the owner as checklist item 38 (a decision about whether to pin the
  order before launch or after).

## L1-F2 — F73(a) does not reach `NaturalistHabitat`

`Fix_ShelterReflex` replaces `MicroGHabitatAutoResolve:IsSuitable`.
`NaturalHabitatBase:IsSuitable` (`NaturalHabitat.lua:33`) declares the identical
un-fixed vanilla body, and `classes.lua:608` skips parents' values for a member a
class declares itself -- including the `AutoResolveMethods.IsSuitable = "and"`
combination (`Building.lua:14`). `NaturalistHabitat.__parents = {"NaturalHabitatBase"}`.

Of the 4 descendants: `MicroGHabitat` covered, `MicroGHabitatBase` covered,
`NaturalHabitatBase` NOT, `NaturalistHabitat` NOT.

- Coverage gap, not a defect in shipped code. No fix written: a new fix needs a
  `FIX_POLICY` 4 entry with intent + reachability tier, which is a build.
- UNMEASURED: whether the F73(a) harm is actually reachable on a Naturalist
  Habitat (does it depend on life support the same way?). Not investigated.

## L1-F3 — F66's recovery reclaim does not run when a `Station` dies

`Fix_TrackConnectorPingPong` wraps `TrackConnectedObjBase:Done`. `Station:Done`
(`Station.lua:134-153`) declares its own body and does NOT call the parent, and
`Done` is absent from the 58-member `AutoResolveMethods` list (enumerated in full).

Of `TrackConnectedObjBase`'s 6 descendants, `Station` is the only shadowed one;
`StationBig`, `StationSmall`, `TrackTunnel`, `TrackTunnelBase`, `UniversalTunnel`
all reach the reclaim.

- The PRIMARY F66 fix is unaffected: it replaces `CreateConnectorElements`, which
  no descendant declares. Stations do get the ping-pong repair itself.
- UNMEASURED: how much the reclaim matters for a station in practice.

## L1-F4 — three engine routes re-derived that nothing here records

Candidates for `agent/facts/`:
1. `OnMsg` is additive (`cthreads.lua:64-72`, appends to `message_to_staticfuncs`)
   AND `message_to_staticfuncs` is a plain file-local, NOT under `FirstLoad`, so
   handlers do NOT survive `ReloadLua` -- the exact opposite of `SMRFixPack.order`,
   which does, and which is why it double-listed every module until `2f077e8`.
2. `classes.lua:608` -- a class that declares a member itself never takes a
   parent's value for it, auto-resolve included.
3. `AutoResolveMethods` has 58 members; `Done`/`Init`/`GameInit` are NOT among
   them, and `IsSuitable` is the ONLY one of the 58 that any of our 50
   class-method targets touches.

## Refuted, each with its route (recorded so a later link does not re-spend the time)

- `Building:OnDemolish` (Fix_TrainsToVoid, gated to Station): 10 subclasses
  declare `OnDemolish`, NONE on Station's ancestor chain. Header claim re-derived,
  holds.
- `Building:SetDome` (Fix_GhostFarmOxygen, gated to FarmBase): `Residence` and
  `TrainingBuilding` shadow it, neither is a FarmBase ancestor.
- `CargoTransporterNew:UpdateCargoResourceRequests` (Fix_RocketDroneChurn):
  `UniversalRocketBase` overrides BUT calls the parent explicitly at
  `UniversalRocket.lua:1684`. Landers reach the patch.
- `RCTransport:CanInteractWithObject` / `:InteractWithObject`
  (Fix_RocketInteractGuard): all three subclasses override and all tail-call the
  parent (`RCHarvester:127`/`:139`, `RCConstructorBase:353`/`:372`,
  `RCTerraformer` via `RCConstructorBase`).
- `OnModifiableValueChanged` on `ElectricityStorage`/`WaterStorage`/`AirStorage`
  (Fix_StorageRateModifiers): nothing shadows it across 2+4+4 descendants. This
  was the static map's one blind spot (runtime `TARGETS` loop) -- closed by
  reading the module, not waived.
- Track family: `TrackBase` / `TrackGridElement` / `TrackConnectedObjBase` are
  SIBLINGS, not a chain. No cross-module fight.
- 16 global replacements, 16 distinct symbols -- no two modules replace the same
  global.
- Preset fields: no two modules write the same one. The one shared preset GROUP
  (`Presets.MapSettings.DustDevils`, two modules) is clean -- SpawnGate copies,
  DescrMap reads.
- Own threads: 7 sites, 6 modules, no shared handle.
- POSITIVE: `Fix_DustDevilSpawnGate:250-258` restores its swapped global only
  `if cur == wrapper`, so it cannot clobber a later replacement by another module
  or another mod. The right shape; the benchmark for lens L8.

## L1-F1 — RESOLVED SAME DAY (2026-08-17), and the resolution corrected the finding's own routing

The owner asked whether the fix was link 1's or the terminal audit's. It was
link 1's (spec section 4: links 1-2 may fix), and the question exposed that the
recommendation attached to L1-F1 above was priced against the WRONG remedy:
"a comment in metadata.lua / the module headers", i.e. a change to the shipped
tree, which is why it was recommended for after launch.

`*/tools/*` is in `metadata.lua`'s `ignore_files` (re-derived at source; the
chain seed's real `.fpk` listing had already measured tools/ at zero files), so
a guard in `tools/doccheck.py` ships nothing at all.

APPLIED: `LOAD_ORDER_RULES` + `load_order()` in `tools/doccheck.py`. Reordering
the two `Colonist:Idle` wrappers in `metadata.lua`'s code list now fails doccheck
RED and exits 1, so the commit hook blocks it, and the failure prints the reason.
Written as a general table so later links append constraints rather than
special-casing.

FALSIFIER: entries swapped -> RED, exit 1, reason printed. Restored ->
`metadata.lua` byte-identical to HEAD (`git diff --quiet` clean), doccheck GREEN,
`upload_preflight` still 20 checked / 0 FAIL.

ZERO shipped files changed. The release candidate is the same bytes it was.

The generalisable lesson, for the terminal audit: "this fix would touch the
shipped tree" was true of the remedy I had in mind and false of the problem. The
scoping question is not "fix or don't" but "is there a form of this fix that
lands outside the package" -- and for anything enforcement-shaped, `tools/` is
that form.

---

# Link 2 — lens L2, lifecycle & idempotency (2026-08-18)

**Nothing here blocks launch.** One defect fixed (`00_Core.lua`), four recorded,
one positive benchmark, one owner decision routed (checklist 39).
Artifact: `reports/L2_LIFECYCLE_MAP.md`. Harness: `tools/l2_reload_sim.py`.
Coverage and the unreached column: `SWEEP_LEDGER.md`.

⚠️ **Fence note:** the fence held on `SWEEP_FINDINGS.md` and on every
`sweep: link …` commit body. But `docs/agent/STATE.md` — a MANDATORY read for
every link — carries a full prose summary of link 1's L1-F1/F2/F3 findings, so
**a link is contaminated on the previous link's verdicts by the brief's own read
path.** That is not a rule I broke; it is a hole in the design, and the terminal
audit should decide whether STATE gets a chain-quarantine section or whether the
"blind on verdicts" claim should be narrowed to what it actually is.

---

## L2-F1 — ⭐ FIXED. Four modules declare themselves inactive over a false reason on the second Lua load, and three save-repairs stop running

**Reachable by:** opening the Mod Manager, changing anything, closing it.
`ModsUIDialogEnd` (`ModManager.lua:123-165`) → `ModsReloadItems` →
`if reload_lua then ReloadLua() end` (`Mod.lua:2145-2147`), and `reload_lua` is
set by ANY loaded mod having code (`:2100`, `:2115`). Not an edge case.

**MEASURED, twice, in this project's own archive.** Counting
`[CommunityFixPack] …: applied` across all 58 pack-carrying logs in
`docs/archive/`: 56 show one line per module; **2 show 148 = 2 × 74** —
`spowner_Mars.exe-20260812-18.30.09` and `rs_ownertick_Mars.exe-20260813-11.16.44`,
both owner-Mod-Manager sessions. Diffing their two load blocks gives the same
answer in both, and it is the pack's **entire** second-load delta:

```
LOAD 2 only (4):  LastTransmissionStorage:  inactive (the shipped presets are already correct)
                  IndependenceTerraforming: inactive (the shipped tech already matches its own param1)
                  SaintBlessing:            inactive (every dome-colonists trait preset already names a real label)
                  AstrogeologistExtractors: inactive (the shipped profile already pays every buildable extractor)
```

Every one of those four sentences is false. The data is correct because **we**
corrected it on load 1 — and `ReloadLua` re-executes mod code
(`lib.lua:353-382` → `autorun.lua:423-424`) while **not** re-running `LoadData`,
so presets persist (`Preset.lua:1339-1340`, `Dlc.lua:636-668`) and the pass's
`ctx.ever_changed` does not.

⛔ **The cost is not the wording.** Three save-repair paths gate on `active`:

| repair | gate | what a player loses |
|---|---|---|
| `Fix_AstrogeologistExtractors:174` | `WhenActive` | a pre-fix save never gets the two extractor modifiers |
| `Fix_IndependenceTerraforming:126-128` | own `status == "active"` test | a researched save keeps the wrong −10% discount |
| `Fix_SaintBlessing:151` | `WhenActive` | dome Saints stay filed under the raw label (also blocked a 2nd way: `rebased_from` is per-load) |

⚠️ **Sibling of `2f077e8`, not a duplicate of it.** All four latches pass
`benign`, so `update_suspect` is never set and the "check for a new version"
dialog **cannot** fire from this. `2f077e8` fixed the mark; the status flip itself
was left standing.

**Fix:** `00_Core.lua` — `ctx.ever_changed` is seeded from and written back to a
per-process memo `SMRFixPack.data_edited[id]`, which rides the one table that
survives a reload (`:17-25`, `:268`, `:323`). The B3 branch ("nothing left to
change is SUCCESS") now spans the reload, which is the lifetime it always meant.
A new process starts with an empty memo, so a game patch that genuinely fixes the
shipped data still latches benign on its first load. **No shipped-file-list
change; `metadata.lua` untouched; counts unmoved (76/75/96/167).**

**Falsifier — `tools/l2_reload_sim.py`**, which runs the pack's own shipped
`00_Core.lua` + the four modules under Lua 5.4 (`lupa`) twice in one process,
reproducing §2's persistence rules:

| run | result |
|---|---|
| control — reproduce the archive | **load 1 emits all 5 archived load-1 lines verbatim and in order, and nothing else** |
| pre-fix | load 2 reproduces **4/4** archived false-`inactive` lines; 4 modules not `active` |
| post-fix | **0/4**; **0** modules not `active`; load 1 byte-identical to pre-fix |
| negative control (`--negative-control`) | fixtures rewritten to the state a future game patch would ship ⇒ all four still latch benign on **both** loads, exit 0 |

⛔ **Scope, stated plainly:** the harness executes our real source against stub
engine globals. **It is not a launch.** The fix has not run inside Surviving Mars
— and neither have the two `2f077e8` core fixes beside it (STATE has said so
since 08-17). See "the one launch that would close three things at once" below.

## L2-F2 — recorded, not fixed. One extra update-report thread per Lua load

`00_Core.lua:560` creates its pregame-menu poll thread at **file scope**, and
`ReloadLua` never touches `ThreadsRegister` (`lib.lua:353-382`;
`ClearGameThreads` runs only on `NewGame`/`DoneGame`, `cthreads.lua:82-113`). So
each Lua load adds a thread and the old one keeps its 5-minute deadline.
⭐ The engine guards its own equivalent with `if FirstLoad` (`autorun.lua:353-357`)
— the convention exists and we are the ones not following it.

**Bounded, which is why it is recorded rather than fixed:** with 0 suspects each
thread exits silently, and a mod-list change reloads only when the Mod Manager
dialog CLOSES (`ModManager.lua:123-165`) — ticking five mods is one reload, not
five. With suspects present the player sees the modal once per Mod-Manager visit.
⛔ **Never observed:** `update report:` has **0 occurrences in all 58 archived
logs**; its only witness anywhere is the 08-17 upload sitting.

**Design if the terminal audit wants it:** keep computing and LOGGING the report
every load (the B gate reads the log for the absence of `update report:`), and
gate only the `WaitMessage` on a latch on the surviving table —
`if not SMRFixPack.reported then SMRFixPack.reported = true; wait_message(…) end`.
That delivers the "one-time dialog" the code's own comment (`:528`) already
promises. ⚠️ It is a change to modal behaviour in a release candidate, and it is
a judgment call about what the pack SHOULD do ⇒ **routed, checklist 39.**

## L2-F3 — recorded. The pack's one mod closure that outlives the Lua load that made it

`Fix_LastTransmissionStorage:134` installs `like.Condition.eval = function() … end`
onto a `FactionDefs` entry — a surface that survives `ReloadLua`. On load 2 the
retarget is already done, so the closure from load 1 stays installed and the game
evaluates load-1 code in a load-2 world.

**Harmless today, and checked rather than assumed:** its upvalues are a local
comparison function, a number, and a resource-name string, and its one global read
(`GetGridGlobalStorage`) resolves at call time through `ModEnvMeta.__index` to the
freshly re-executed function (`Mod.lua:1546-1556`). It is the pack's **only**
instance of the shape, and it is the shape that would bite hardest if it ever
captured a class, a preset object, or a wrapper. Worth a `FIX_POLICY` line;
⛔ whether it enters a save is **L3's** question, not answered here.

## L2-F4 — recorded, latent. Wrapper installs inside `apply` carry no identity guard

`run_apply` can be called a second time **within one Lua load** only from
`OnMsg.ApplyModOptions` → `def.optional` (`00_Core.lua:432-481`). doccheck emits
**0 files carry `optional = true`** and the pack has no Mod Options page, so the
route is dead today. But sites like `Fix_TrackTunnelPowerBridge:143`
(`local orig_done = T.Done; function T:Done…`) would wrap their own wrapper if it
ever opened. ⇒ a `FIX_POLICY` §1.4 note ("a wrapper installed inside `apply` must
be identity-guarded, because `apply` is not once-per-process"), not code.

## L2-F5 — recorded, PREDICTED not measured. A reloaded session would report 2 false suite FAILs

`SMRTest.FixMissing` returns **`FAIL`**, not SKIP, for a fix whose status is not
`active` (`00_TestCore.lua:314-326`), and the `SaintBlessing`
(`57_Probes_Wave8.lua:128`) and `AstrogeologistExtractors` (`:320`) probes open
with it. Under L2-F1 a suite run after a reload would have shown 2 false FAILs.
⛔ **Never observed** — neither two-load session ran the suite (14 `SMRTEST` lines
each against 96 probes). ⇒ ⚠️ **every `80/0/16/0` reading this project owns is a
SINGLE-LOAD reading**, and "single-load" now belongs in the configuration label
beside "all three mods, unpacked". L2-F1's fix removes the mechanism.

## L2-F6 — ⭐ positive benchmark. Nothing in the pack wraps its own wrapper, anywhere

The lens's headline question, answered mechanically rather than by assurance —
each of the three ways it could have happened was closed by a different engine
route, and each was looked up rather than assumed:

- **13/13 global replacements** — every target is a plain top-level `function F()`
  under `Lua/`, re-executed by `dofolder("Lua")` before our code re-wraps. Each
  name was located at its Src declaration (list in the artifact §4).
- **50 class-method targets** — class globals are cleared (`classes.lua:37-38`),
  classdefs rebuilt (`:57-72`), `g_Classes` tables cleared and refilled
  (`:1006-1013`, `:1083-1085`).
- **No stale env shadow** — `rawget(_G, …)` from mod code reads the REAL global
  (`env.rawget = safe_rawget`, `Mod.lua:1576-1582`) and mod writes go straight to
  the real `_G` leaving no copy behind (`:1557-1563`), so no module can be holding
  a load-1 function.

Also clean and each checked, not inherited: **23** module `OnMsg` registrations
(+8 in core) — the store is a plain file-local discarded per load
(`cthreads.lua:6`), and all 14 distinct message names miss `ModMsgBlacklist`
(`Mod.lua:1430-1440`), so none is silently dropped; the **`PeriodicRepeatInfo`**
slot (`Fix_CaveInsNoDisasters:35`) is clean twice over — the table is rebuilt
(`lib.lua:1532`) and a live repeat re-reads its body every iteration
(`:1568-1594`); the **`GameVar` once-flag** (`Fix_FirstAsteroidPrefabs:115`)
is correctly NOT reset by a reload (`lib.lua:1049-1051`).
⇒ **71 of 75 modules are byte-identical across the two real loads.**

## The one launch that would close three things at once

An unattended run that performs a `ReloadLua` at the pregame menu and then reads
the four statuses would verify **L2-F1's fix, and both 2026-08-17 core fixes**
(`order` de-duplication and the `update_suspect` clear), all of which are
currently source-verified only. Shape: a temporary TestKit leg on the existing
`95_AutoRun` harness — record statuses → `ReloadLua()` → record again → quit,
with `SMRAutoRun` latched so the second load's harness thread stands down.
⛔ Not built this link. Binding if it is: `EF-056` byte-copies first, predictions
pre-registered in a pushed commit, probe-hygiene sweep after.

## Routed to the owner

- **Checklist 39** — should the deactivation dialog re-fire after a Mod Manager
  visit, or show once per process? (recommendation: **once per process, keep the
  log line every load**; it is what `00_Core.lua:528` already promises.)
