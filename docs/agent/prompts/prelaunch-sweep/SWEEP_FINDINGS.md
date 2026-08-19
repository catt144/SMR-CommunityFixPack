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

---

# Link 3 — lens L3, save & exit (2026-08-18)

**Nothing found blocks launch. ZERO code changed** — link 3 is record-only
(`00_CHAIN_SPEC.md` §4) and no finding met the launch-blocking exception.
Artifact: `reports/L3_SAVE_FOOTPRINT.md`. Instrument:
`tools/l3_save_footprint.py`. Config: dev tree, unpacked, source-derived; **no
launch**, nothing read off a real save.

⚠️ **Own-instrument defects, disclosed before any count is used.** (1) The
handler regex matched only `OnMsg.X = f` and missed `function OnMsg.X() … end`,
hiding **two** `PostLoadGame` passes from the load-order table. (2) A
string-blanked scan lost **4** of the 13 `SMRFixPack_*` tokens, which live only
inside string literals. Both found by cross-checking the census against a plain
grep, both fixed and commented in the script; every count below is post-fix.
Neither changed a verdict.

---

## L3-F1 · ⭐ `smr_shuttles` — the one persisted key that breaks the naming rule, and the exposed-set row that is wrong because of it

**Severity: not harmful, not launch-blocking. It is a RECORD defect plus an
undispositioned site.** → routed, checklist item 40.

`Fix_ShuttleTransportCache:88` writes `entry.smr_shuttles = with_shuttles` onto
the cache-entry table stored at `t[pos]` inside `g_TransportationModeToCommunityCache`,
which is `GameVar(…, false)` at `Lua\Units\Colonist.lua:2478`. ⇒ a mod-authored
boolean under a mod-authored key travels in every savegame.

⛔ **`D13_EXPOSED_SET.md` §2c lists that global among those whose contents are
"indistinguishable from vanilla's own and carry nothing of ours." For this
global that is false.**

⭐ **Why the authoritative derivation could not have caught it, and the general
lesson:** §1.1 swept route-(c) persisted state with the **`SMRFixPack_*` token
as its grep key**. `FIX_POLICY` §3's naming rule is therefore **not a style
preference — it is the key the census runs on**, and the single site that breaks
it is structurally invisible to the census that is supposed to enumerate it.

**Generalised mechanically, so this is not one anecdote:** all **66** field names
the pack writes on non-local carriers were tested against the entire shipped tree
(**4,446** Src `.lua` files, **131,363** distinct tokens). **9** are absent from
Src. 6 follow the convention. Of the 3 that do not, `ever_changed` and
`update_suspect` are on mod tables (`ctx`, `SMRFixPack.fixes[id]`) and are not
persisted. **`smr_shuttles` is the only one.** ⇒ the breach is real and it is
singular; the census now exists to keep it that way.

**The cost, adjudicated rather than asserted:** vanilla reads the entry with
`table.unpack` (`Colonist.lua:2537`), which takes the array part only, so the key
is inert after uninstall — the module's own header says exactly this (`:22-24`)
and is accurate. The whole cache is dropped on `TrainRoutesRebuilt` /
`DomesConnected` / `DomesDisconnected` (`:2480-2488`), so the residue is
transient. **Three-tier ethos level 2 at worst, plausibly level 1.**

⇒ The finding is not the behaviour. It is that `FIX_POLICY` §3a says *"A site
with no recorded disposition blocks release by default; a site with one does not,
whichever way it went"* — and this site has none, because it was never on a list.
**Recording the disposition is a docs act and is what this link does**; the
owner's call is whether the recorded disposition discharges §3a or whether they
want the key renamed to `SMRFixPack_shuttles` first (a one-line code change,
which link 3 may not make).

## L3-F2 · ⭐⭐ The exit law, and the shipped header that states it backwards

**Severity: a wrong disclosure inside a shipped code comment. No player surface
repeats it.** Record-only; no route needed.

Re-derived at Src this session rather than cited: `OnMsg.PersistSave` writes
`data[k]` for every key of `PersistableGlobals`, and `OnMsg.PersistLoad` restores
only keys of `PersistableGlobals` (`CommonLua\Core\persist.lua:119-143`).
`GameVar` is what puts a name in that table, and `GameVar` only runs when our
file loads.

> ⭐ **THE LAW, stated nowhere on record until now: a persisted name of ours
> survives uninstall if and only if its CARRIER is vanilla's. The only two of the
> pack's twelve persisted keys that vanish are the two whose carrier is a
> `GameVar` we registered ourselves** — `SMRFixPack_MeteorLatch` and
> `SMRFixPack_FirstAsteroidPrefabs`. The full per-name table is artifact §7.

⛔ **`Fix_MeteorFrequency:36-37` discloses the opposite**, as an accepted
residual: *"the SMRFixPack_MeteorLatch GameVar stays in the save after uninstall
as inert data (prior art: GromGor's `MeteorsFixed` GameVar, C31)."* Repeated at
`:69-70`. Precisely: the save file the player already holds still contains the
value in its blob, but it is never restored without the pack and is omitted from
the next save. ⇒ **we disclose a residual we do not leave.**

⭐ **The pack contains both the wrong and the right statement of the same
mechanism.** `Fix_FirstAsteroidPrefabs:95-101` gets it right and cites
`persist.lua:135-142`. And the player-facing route is already correct —
`RELEASE_UNINSTALL_ASSEMBLY.md` §1 records *"the one version-stamped name is
dropped by the engine on the first load without the pack."* ⇒ **the defect is
confined to a code comment.** That bound is why this is not routed.

## L3-F3 · The meteor heal's stated invariant is not what the mechanism delivers

**Severity: bounded, arguably correct behaviour; the INVARIANT is misstated.**
Record-only.

`Fix_MeteorFrequency:42-51` promises *"one restart per save lineage per
version"* — the latch holds the last-healed pack version. By L3-F2 the latch is
erased by any save written without the pack. ⇒ on **uninstall → play → save →
reinstall**, and on the Mod-Manager disable → enable route that spans one save
(`EF-002` state (4); D13's state (4)), the latch reads `false ≠ version`, the
heal runs again, and `RestartGlobalGameTimeThread("Meteors")` **re-rolls the
35–115 h meteor timer**.

**Stated fairly:** one re-roll per reinstall cycle. F88 — the defect this design
exists to prevent — was one re-roll **per load**, which is what made it silent
and permanent. A single re-roll on a reinstall is bounded and arguably desirable
(a reinstall *should* clear persisted old bodies). ⛔ **Not harmful, not
launch-blocking.** The guarantee is per save lineage per version **per continuous
installation**, and nothing on record says so.

## L3-F4 · `90_SaveSanitizer` sets its F48 one-shot flag BEFORE the pass, so a decline latches permanently

**Severity: latent — reachable only after a game update moves two globals.**
Record-only; the one-line repair is a code change.

`:337-342` sets `colony[F48_FLAG] = true` and *then* calls
`repair_station_connectors`. That function has a deliberate decline branch
(`:249-252`) for when `ProcessTrackElements` / `ResolveMap` are no longer
globals — the design that keeps a moved API from deactivating the F35 and F03
repairs alongside it. The flag is already set by then, and it lives on
`UIColony`, so **the decline is permanent for that save**: a later pack build
that handles the moved API would find the flag set and never run. The same holds
for a raise the `pcall` swallows.

The flag's own stated contract (`:212-214`) is *"a save this pass has already
re-ordered is never re-ordered again"* — but it is also set on a save the pass
declined to re-order. F35 and F03 are unaffected (they re-derive every load).

## L3-F5 · `90_SaveSanitizer`'s scoping header is stale in both directions

**Severity: cosmetic — a factual list inside a shipped comment.** Record-only.

`:5-7` names 8 modules as carrying *"their own LoadGame pass in their own file"*
(F02, F45, F37, F58, F06, F38, F39, F40). Measured against the tree: **17** do.

* **11 unlisted:** F44, F18, F81, F78, F81b, F83, F92, F95, F102, F65, F49.
* **F39 has no module in `Code/` at all** — the id occurs in the whole shipped
  tree only inside this comment; `bugs/INDEX.md` records it `folded`.
* **F58's pass is `OnMsg.NewDay`** (`Fix_StaleReservations:59`), not a load pass.

Nothing behaves wrongly — it is a scoping note, not a coverage claim — but it is
the only place a reader is told where this module's boundary sits.

---

## Positive results, recorded because they are load-bearing and were re-derived

1. ⭐ **D13 §3's open Rule-6f routing is DISCHARGED, and nothing on record says
   so.** That routing named E5/E6/E7 (`CrystalMysteryHang`, `ExtenderFlapChurn`,
   `TrackConnectorPingPong`) as carrying **no** §3a orphan gate. All three carry
   one today — `:78`, `:96`, `:179` — read this session, not taken from the
   headers that claim the 2026-08-13 rewrite. Over all **six** game-time thread
   sites: 4 gated, 1 gate-free by construction (`Fix_RainsDeadlock:195` passes
   **vanilla's** `RainsDisasterLoop` as the entry body, so no mod code is in that
   thread), 1 un-gated with a recorded accepted disposition
   (`Fix_BombardmentSpread:137`, all-vanilla body that completes the volley and
   clears `map.g_IncomingMissiles` at `:152`).
2. ⭐ **The 11 persisted names re-derived from the tree reproduce D13's rows
   D1–D11 with ZERO membership difference**, and the two module changes since
   that derivation (`Fix_DistressPopupPause` in and out, C39
   `Fix_AutomationLawCompensation` in) **added no persisted name**. C39's header
   declares "Layer 2 by construction, nothing persisted" (`:96-102`) and the
   census agrees.
3. ⛔ **0 `OnMsg.SaveGameStart` and 0 `OnMsg.SaveGameDone` in all 76 files.**
   §3a layer 1 is entirely unused — a positive result under *"build it last, and
   only for what survives the other two layers"*. Its consequence, which is the
   honest form of "aggregate save footprint": **nothing is torn down before a
   save, so the footprint is exactly whatever is live when the player saves**,
   and the simultaneous liveness of the six game-time threads has never been
   measured by anything.
4. **`SavegameFixups` gating re-derived** (`SavegameFixup.lua:10`, `:24-50`):
   **237** shipped fixups, run in **alphabetical** order via `sorted_pairs` —
   which is why the devs prefixed `A_StationConnectorElements3` — each once,
   gated by `AppliedSavegameFixups`, which is itself a **`GameVar`**. ⇒ the
   "our `LoadGame` pass runs before a shipped fixup" hazard that
   `90_SaveSanitizer:315-324` was bitten by is live on exactly one load per save:
   the first load of a save that still owes that fixup — which is precisely the
   population the repair passes target.

## A hypothesis formed and REFUTED at source, recorded so it is not re-formed

The F48 pass calls `ProcessTrackElements` on every track, and F45 exists because
`false < number` raises in a `node_idx` sort. It looked as though F48 could trip
the F45 defect on a save where `Fix_BrokenTrackSalvage` is vetoed. **Refuted:**
`OrderTrackElements` (`Tracks.lua:520-639`) does not sort by `node_idx` at all —
it walks the hex grid and renumbers at `:632-633`. The defect is not reachable
that way.

## Stopping rule

⛔ **Not convergence.** Three lenses of eight are done; L4–L8 are untouched, and
the ledger's unreached column for this link alone lists thirteen unswept
load-time passes, the whole uninstall and reinstall walk, and every measured
figure in this territory. No clause of §5 is invoked.

---

# Link 4 — lens L4, player experience (2026-08-18)

⛔ **Record-only link** (spec §4). **Nothing blocks launch. Zero code changed.**
Counts unmoved (76/75/96/167); `metadata.lua` untouched.

**Artifact:** `docs/agent/reports/L4_PLAYER_SURFACES.md` · instrument
`tools/l4_player_surfaces.py`.
**Configuration:** dev tree, unpacked, source-derived + Src read by symbol +
the archived log corpus (all-three-mods rig). ⛔ **No launch.**

## ⚠️ Fence breach — disclosed

I ran `tail -5` on `SWEEP_FINDINGS.md` to find the append point and saw **2
lines** of link 3's closing paragraph (its non-convergence statement — coverage,
not a finding verdict). Deliberate act, so it is reportable under
`00_CHAIN_SPEC.md` §2 regardless of what the lines contained. It came after all
five censuses and every adjudication below were complete, so it cannot have
anchored them. `wc -l` alone was the correct tool and is what I should have used.

## The shape of the answer

The lens notes say the answer should be **nothing**, and it very nearly is. The
pack mints **no** notification, popup, banner or voice line of its own — all 17
screen call sites raise a surface the game already owns (artifact §1.1). It has
exactly **one designed screen surface**, and both real defects live in it.

## L4-F1 — the update-report dialog names internal identifiers, not the titles it already has

`00_Core.lua:569`, `table.concat(suspects, ", ")` over ids from
`SMRFixPack.order` (`:537`). The player reads *"Switched off:
AstrogeologistExtractors, SaintBlessing"*.

- **Measured:** all **75/75** registered modules supply a `title` — a plain
  English sentence in the same register the fix list is written in. The registry
  has it; the dialog does not use it.
- **Measured:** module ids appear on **no player-facing surface** — over the
  site's five pages they occur only in `for-modders.md` (:33 :43 :45, all
  `SMRFixPack_Disabled` examples) and the README's for-modders section. Fix list,
  FAQ, install, landing and the store card use prose only.
- ⛔ **Sharpened by `FIX_POLICY` §7:** on Xbox / PlayStation / MS Store there is
  no log, no console and no file access ⇒ **this dialog is the pack's only
  player-facing surface on console**, and the id list is the one form of the
  information a console player cannot resolve.
- Same class as this project's own recorded trap — `BottomlessPitResearchCenter`
  renders as *"Experiment 1: Big Drop"* on every player surface (08-15).

**Not blocking. Owner-shaped (the pack's voice) ⇒ routed, batched with F2, as
checklist item 41.** Recommended shape: id + title, or title alone.

## L4-F2 — the dialog's sentence is false for the `error` case, and it blames the game

`UpdateSuspects` makes `status == "error"` a suspect unconditionally
(`:527-528`). `error` means `def.apply` **threw under `pcall`**
(`run_apply`, `:388-392`) — our own defect, or another mod's interference (the L8
shape). It is never evidence of a game update. The dialog nevertheless says, in
one undifferentiated sentence, that the fixes *"found that the game code they
patch has changed — usually after a game update"* and invites the player to
*"check for a new version of the Relaunched Fix Pack."* The log line at `:570`
carries the same wording.

⇒ on a crash of ours we would **attribute it to a Paradox patch** and send the
player after a version that does not exist, instead of reporting the bug. This is
the house rule *"'not caused by our leg' is an attribution verdict, not a
dismissal"* pointed outward at the game.

**Latent** — 0 `error` statuses in the 57 archived logs — but it is exactly the
case the dialog exists for. **Not blocking. Batched into checklist item 41.**

## L4-F3 — `ctx.heal()` is the pack's only status transition that writes no log line

Every other transition logs: apply success `:412`, apply threw `:392`, apply
declined `:396`, pre-load veto `:448`, `ctx.latch` `:279`, and all four Mod
Options transitions (`:474` `:483` `:487` `:500`). `ctx.heal()` (`:281-294`)
logs nothing.

**Measured, and not hypothetical: 56 of the 57 pack-carrying logs in
`docs/archive/*.log` carry `SaintBlessing: inactive (no dome-colonists trait
presets)`, which is false by the end of the same load.** In `c48pair2` the module
heals **642 ms later** (Lua `0:00:18:398` → `0:00:19:040`, lines 171 → 185) and
the recovery is implied only by a *different* line (`corrected 1 …`). Nothing in
the log ever states the module is active again.

Two heal sites log nothing at all — `Fix_DustDevilSpawnGate:308`,
`Fix_DustDevilsDescrMap:112` — so on a `DataChanged` re-fire after a latch those
modules' logs would end on `inactive` with no counterpart line whatever.

The FAQ asks players to attach a log to a bug report and the owner reads logs for
triage. ⛔ **Not cosmetic** — it corrupts triage and has already contaminated 56
archived logs — but **nothing a player experiences in game changes.**
**Not blocking. Not owner-shaped** ⇒ terminal audit: one `log()` inside
`ctx.heal()`.

## Verified positives — four things nobody had checked

1. ⭐ **The never-executed dialog's mechanism holds, re-derived at Src.**
   `update report:` (`:570`, logged *before* the dialog) has **0 occurrences in
   all 57 pack-carrying archived logs** — counted, not inherited. Four checks,
   none previously made: signature `WaitMessage(parent, caption, text, …)`
   matches our `(nil, caption, text)` (`StdDialogs.lua:617`) · `parent = nil`
   resolves via `parent or terminal.desktop` (`:596`) · our `Untranslated(…)` is
   **double-wrapped** by `CreateMessageDialog` (`:542-543`) and that is a
   **no-op**, because `Untranslated` returns any `IsT` value unchanged
   (`localization.lua:339`) · the OK action carries `ActionGamepad = "ButtonA"`
   (`:570`), so `FIX_POLICY` §7's console reasoning holds.
2. ⭐ **The verdict-string fence does not leak.** All **181** strings that can
   become an entry `detail` were censused and crossed with `UpdateSuspects`' four
   substring tests (`:532-535`). **72 match, and every one is a genuine
   target-shape failure that also sets the `update_suspect` mark — the two routes
   agree on all 72.** No benign verdict trips a substring, so no working module
   can fire the false-update dialog by wording alone. This is the aggregate check
   the 2026-08-17 defect earned.
3. ⭐ **The card's blanket claim holds — checked per row, not asserted.** *"Every
   fix checks the game's code before it patches anything"*: 69 modules route
   through `SMRFixPack.Require`; the other **7** each carry a bespoke
   precondition check, read at source individually
   (`DustSicknessBiorobots:122` · `ExtenderFlapChurn:73-75` ·
   `IndependenceTerraforming:72` · `LastTransmissionStorage:108` ·
   `SequenceLatents:136` · `ShelterReflex:79` · `StorageRateModifiers:75`).
4. ⭐ **`F98`'s player-surface consequence is contained**, which only this lens
   could confirm: the store card does not promise the tech-description fix (0
   hits in `RELEASE_DESCRIPTION_FIXPACK` / `STORE_FIXPACK`) and the site fix list
   deliberately omits it ⇒ **the pack never promises a player something `F98`
   fails to deliver.** The only residue is an `applied` log line.
   Separately, `Fix_GraphConsumedCaption`'s `T{8979, …}` was verified
   **byte-for-byte** against `Lua/X/ColonyControlCenter.lua:181-186` — same id,
   same literal — so localised builds are unaffected.
   And the **tag-vs-name route does not break**: no player-facing page names
   `[CommunityFixPack]`; the FAQ asks players to *attach* a log, never to find
   our lines in one.

## Log noise, measured

**82** `[CommunityFixPack]` lines in a full load (`c48pair2`, all-three-mods rig)
= **75** `<id>: applied` + **7** substantive (6 repair reports + the one stale
`inactive` of F3). Nothing alarming, nothing false but that line.

## ⛔ Convergence — NOT reached, and the cap is the wrong reason to stop

Four lenses of eight are done. **L5–L8 are untouched**, no §5 clause is invoked,
and the ledger's unreached column is longer than this link's findings list.

⛔ **I am link 4 of a cap of 5, and I do not believe one more link closes this.**
The three remaining lenses after link 5 each own a named, never-swept job with a
live precedent:

- **L6** — dead-coded targets, *"is F85 the only one?"*, still unswept; the
  `player-route ≠ source citation` shape has been the finding **three** times,
  and `F98` is a fourth instance of the same family found from a different angle.
- **L7** — packed-vs-unpacked, and **configuration B has never been run in the
  history of this project**.
- **L8** — the **15** global replacements link 1 explicitly did **not** sweep for
  the save/restore discipline `Fix_DustDevilSpawnGate:250-258` demonstrates.

⇒ **Recommendation to the owner: raise the cap to 8 so the rotation completes.**
Stopping at 5 would leave three lenses unasked, and `00_CHAIN_SPEC.md` §5 names
reporting a cap as convergence as the worst outcome this design can produce.

---

## Verification launch (interlude, no lens) — 2026-08-19

Full derivation and every raw line: `reports/97_VERIFICATION_LAUNCH.md`.
Legs: `archive/vl97a/b/c_Mars.exe-20260819-*.log`. Predictions pushed first
(`1844095`). **Record-only; nothing was fixed, and nothing found blocks launch.**

**VL-1 · ⛔ The two core fixes are still NOT verified, and the reason is a
readability limit, not a missing launch.** `2f077e8`'s code ran three times in
retail. Fix ①'s failing sequence executed in full — `Fix_SaintBlessing.lua:121`
non-benign latch (sets the mark, `00_Core.lua:277`) → `:113 ctx.heal()`, one of
the two lines the fix added — and the entry ended **`active`** (`75/75`). But
`UpdateSuspects` reads only `error`/`inactive` entries (`:527-536`), so a stale
mark on an `active` entry is **invisible to the probe that would report it**.
⇒ `PASS UpdateReport` is true and **uninformative** for fix ①. **One console
read settles it:** `print(SMRFixPack.fixes.SaintBlessing.update_suspect)` → `nil`.
Fix ② and L2's reload prediction and link 2's `data_edited` fix **all three**
need the same single second Lua load. ⛔ Unreachable unattended (`ConsoleExec`
and `debug` blacklisted, `Mod.lua:1285`).

**VL-2 · ⚠️⚠️ `98_LAUNCH_REHEARSAL.md`'s procedure has a hole that would have
read as a catastrophic B failure.** Pulling the **opt-in** junction disabled that
mod in account state; **restoring the junction did not bring it back** across two
relaunches (def loads, code never runs, `opt-in pack NOT loaded`). Run B pulls
the **fix pack's** junction the same way. ⇒ **B must budget an owner Mod-Manager
tick after the swap and read the gate line before believing any other number.**
Not a defect in the pack — a defect in the planned procedure, found in advance.

**VL-3 · `EF-055` refined twice by measurement.** Its recorded cause (a round
trip *"spanning an owner Mod-Manager visit"*) is **not** necessary — there was no
visit here. And its *"skipped with a non-modal log line"* did not happen: the mod
vanished **silently**. Fact amended in place; `account.dat` rewritten at 00:30.

**VL-4 · No regression from `2f077e8` is visible in the suite, by name.** 96
probes diffed against `c47suite4` (the last suite before the core fixes, same
harness, same build): **8 verdict changes, all PASS → SKIP, all opt-in-family**.
The other **88 hold exactly**. `72/0/24/0` in the opt-in-absent configuration,
reproduced identically three times.

**VL-5 · The opt-in-absent SKIP set, BY NAME** (answers what `98` needs):
`AcknowledgedWarnings` · `ClassicRockets` · `CohortHousing` · `DroneStatDials` ·
`MultipleSuns` · `NoHomeless` · `OptionsMenuOptIn` · `ResidencyControl`.
⭐ **`OptionsMenuFixPack` PASSES** — the pack's own options page does not depend
on the opt-in mod. Pre-registration named the wrong 8 (predicted
`60_Probes_Opt.lua`'s list); the count was right, two names were not.

**VL-6 · First aggregate runtime cost this project has ever measured.** All 75
modules register and apply in **≈0.57 s**; the data-patch/heal work completes by
**≈1.3 s** (`Lua` clock markers, `EF-045`-safe). The pack writes **81 log lines
at load**, 90 across a session, of a 1,070-line log.

**VL-7 · Positive control on H-02.** The running game reports the pack at
**1.0.0** (`RainsDeadlock: … version 1.0.0`, where the 08-15 baseline said
`1.0.1`). `metadata.lua` was never opened and no editor save occurred.

**VL-8 · cosmetic / non-finding, recorded so nobody re-derives it.** 48×
`Flight.lua:465` + 1× `:479` `[LUA ERROR]` — **the identical split to the 08-15
baseline**, documented as vanilla synthetic-map noise since 2026-08-03.
Attribution: vanilla, aged ≥16 days, count reproduced — reported, not dismissed.
`MeteorFrequency: WATCHDOG` likewise present identically in the baseline and
probe-driven.
