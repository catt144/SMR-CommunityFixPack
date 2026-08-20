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

---

## Link 5 — lens L5, failure & containment (2026-08-19)

Artifact `reports/L5_CONTAINMENT_MAP.md` (full derivation for every row);
instrument `tools/l5_containment.py`. Configuration: dev tree, unpacked,
source-derived at `ModTools\Src` 1.0.7.396349 + 73 archived retail logs.
**No launch** — refusal reasoned in the artifact §7 and in the report.

⛔ **Nothing found blocks launch.** One record was corrected in place; all code
findings are RECORD ONLY per spec §4.

### L5-F1 · `SMRFixPack.OnDataReady` swallows its callback's throw — `00_Core.lua:372`, `:380`
`DataPatch` pcalls its pass and names the F87 failure mode in a comment
(`00_Core.lua:305-318`). `OnDataReady`, eleven lines later, calls `fn()` bare
inside `OnMsg` handlers, so `Msg`'s `procall` (`cthreads.lua:20`) swallows the
throw: module stays `active`, `detail` stays `""`, no log line. Consumers:
`Fix_FirstAsteroidPrefabs:237`, `Fix_TechDescriptionBuilding` x2 (the latter is
already a proven no-op, `F98`/`EF-039`, so live exposure is luck not design).
**Hard tell:** sibling contradiction, same file, same reason, same engine route.
**Fix shape:** mirror `DataPatch:309-318` — pcall, `status="error"`, log.
**Route:** record only; terminal audit.

### L5-F2 · `Register` indexes `SMRFixPack_Disabled` with no type guard — `00_Core.lua:446`
`:11`/`:15`/`:17` adopt three foreign-writable globals and keep any truthy value.
`WhenActive:187-188` and `DataPatch.run:302-303` both guard with
`type(disabled) == "table"`; `Register:446` does not, and `:24-25` indexes
`SMRFixPack` unguarded. `Register` runs at every module's file scope ⇒ a
non-table truthy `SMRFixPack_Disabled` throws in **all 75 files at once**
(75 modules ABSENT + a message box listing 75 errors); a non-table `SMRFixPack`
takes the whole pack down at `:24`, before the logger exists.
**Reachable** only by a pre-load foreign write — but the README advertises
`SMRFixPack_Disabled["<id>"] = true`, and the misreading `SMRFixPack_Disabled = true`
lands here at the next `ReloadLua` (which a player triggers by closing the Mod
Manager). **Fix shape:** three `type(...) ~= "table"` resets at `:11-25`.
⚠️ **Overlaps L8** — flagged so L8 does not re-derive it. **Route:** record only.

### L5-F3 · Three load-time repairs walk player data with no per-item guard
14 message handlers iterate; the pack already owns the correct shape
(`Fix_TrainMinors:141`, `Fix_TrackTunnelPowerBridge:164` — a per-ITEM pcall).
Without one, a throw on item k is swallowed by `procall` and items k+1..n are
abandoned with no log line and the entry still `active`.
- `Fix_SaintBlessing:151` — `AllMapsForEach(true,"Colonist",...)`, every colonist
- `Fix_TrackSalvageWipe:304` — `AllMapsForEach(true,"TrackGridElement",...)`
- `Fix_StaleReservations:61` — plain Lua `for` over every Residence x `reserved`
⚖️ **Severity is half-unmeasured:** the first two reach objects through
`map:MapForEach`, a **C export**, and whether the C loop procalls per object is
not derivable from Lua. `Fix_StaleReservations` has no such ambiguity — the
remainder is abandoned, certainly. **One console line settles all three**, routed
to checklist 44. **Not blocking:** an abandoned repair leaves vanilla state, and
72 pack-carrying logs show none of the three throwing. **Route:** record only.

### L5-F4 · Run B's criterion 3 was unsatisfiable — `98_LAUNCH_REHEARSAL.md:156` ✅ CORRECTED IN THIS COMMIT
The release gate required `0 [LUA ERROR]` and closes "Any of 1-7 failing blocks
the upload." MEASURED: 73/73 archived logs carry them; the three 08-19 legs read
**49 / 60 / 49** (`Flight.lua:465` x48/59/48 + `:479` x1). `01_LINK.md` §6 was
corrected for exactly this on 2026-08-19 and the rehearsal was not.
⭐ Also: `reports/97_VERIFICATION_LAUNCH.md` R5 calls the count "reproduced"
while disclosing 48 vs 59 in the same sentence — `Flight:Mark` fires per marked
object, so the number tracks session activity. **The stable signature is the
SHAPE (exactly two sites, both `Flight.lua`), never the count.** Criterion 3 now
says so, with the measured baseline and the `EF-065` escalation.
**Record fix, not code** — spec §4 clarification, 2026-08-19.

### L5-F5 · `FIX_POLICY` §2's both-checks rule is not met by 4 delegated handler bodies
`MeteorsWatchdogCheck:121`, `IndependenceTerraformingSweep:127`,
`StormWedgeCheck:98` test `status == "active"` but not `SMRFixPack_Disabled[id]`;
`Fix_CrystalMysteryHang:105` (`OnMsg.MysteryEnd` -> `stop_repeater`) tests
neither. §2 requires both. Pre-load vetoes ARE covered (Register latches
`status="disabled"`), so the gap is **mid-session veto only**.
⚠️ `Fix_MeteorFrequency:164-169` does both in the same file as `:157`, which does
not. **Cosmetic-to-minor. Route:** record only.

### L5-C1 · CANDIDATE, vanilla, not ours — `Lua/TerraformingDisasters.lua:411`
`[LUA ERROR] attempt to index a boolean value (upvalue 'old_threads')`, 1 of 73
logs, 2026-08-04. `UpdateRainsThreads` reads the `RainsDisasterThreads` **GameVar**
(`:323`, `false` with no live session) into an upvalue at `:376` and indexes it at
`:411`; its **one caller tree-wide** is `DelayedCall(0, UpdateRainsThreads, ...)`
(`:488`), deferred into a real-time thread (`lib.lua:1811`). Session teardown
between schedule and fire ⇒ throw. **Attribution shown:** no pack site assigns
that container; `Fix_RainsDeadlock:126-134` only *repairs* a non-table one; the
sole caller is vanilla's. ⚠️ **What I cannot show:** that our leg did not change
the timing that opened the window; 1 occurrence is not a rate.
**Deliberately NOT filed as a `bugs/` row mid-chain** — count churn before launch
for no benefit; the terminal audit files with the whole set visible.

### New record: `EF-065` — the engine's two player-facing mod-error boxes
Neither has a call site in our code, so no census of `Code/` can see them.
(a) `ReportModLuaError` (`Mod.lua:2958-2993`, live in retail — gated
`if not Platform.asserts`) pops "Mod-related problem detected ... Mod Flagged:
<title>" on any uncaught error whose message OR stack contains our
`content_path`, once per mod id per process. (b) a file-scope throw is caught by
`pdofile` (`lib.lua:242-251`), collected by `ModDef:LoadCode` (`:490-520`) and
shown by `ModsLoadCode` (`:2254-2275`). **MEASURED NEGATIVE: 0 occurrences of
either in all 73 archived logs.** ⇒ "fail safe, never loud" holds only where our
code sits inside a pcall we own.


---

## Link 6 — L6, promise vs behaviour (2026-08-19)

Artifact: `docs/agent/reports/L6_PROMISE_MAP.md`.
Extractors: `tools/l6_promise_map.py`, `tools/l6_reachability.py`.
Config: dev tree, unpacked, source-derived at Src + the 76-log archive; **no launch** (refusal reasoned, artifact §7).

### ⛔⛔ L6-F1 — LAUNCH-BLOCKING, FIXED THIS LINK (spec §4 exception) — commit `36d8817`

`items.lua` held **75** `ModItemCode` entries against `metadata.lua`'s **76**-entry `code`
list: `Code/Fix_AutomationLawCompensation.lua` had no item. It entered `code` with
`92fe101` (2026-08-15); `items.lua`'s previous touch (`0efb87e`) predates that.

**Route, re-derived at Src by symbol** (full table, artifact §0):
`UploadMod` runs `prepare_fn` → `CreatePackageForUpload` → `upload_fn`
(`GedModEditor.lua:772-824`); `Steam_PrepareForUpload` calls `SaveWholeMod()` inside
step 1 on a first upload (`SteamWorkshop.lua:17-22`); `SaveWholeMod` → `SaveDef()` with
no argument (`Mod.lua:1140-1157`) → `UpdateCode()` (`:973`), which rebuilds `self.code`
**solely** by walking the mod items in index order and **never scans disk**
(`:816-840`, `ForEachModItem` `:716-728`).

⇒ **Steam would have packed a 75-entry `code` list and the automation-law fix would
never have loaded for any player.** Paradox's *first* package escapes (its save runs
after the upload, `ParadoxMods.lua:167-173`) but still rewrites the tree, so the
documented Paradox-then-Steam order (`RELEASE_PORTAL_PREP.md` §0.5(c)) loses the module
on Steam and on every later update to either portal.

⚠️ Cost is evidenced, not argued: this is the module reading `applied` + probe `PASS` in
all three 2026-08-19 retail legs (`archive/vl97a/b/c_*`, `75 applied` each).

**Fixed:** the item, at metadata's own position. Falsifiers in the artifact.

### ⛔ L6-F2 — the guard for exactly this reported PASS — FIXED, same commit

`tools/upload_preflight.py:171` counted the bare string `"ModItemCode"` over the whole
file, which counts the **header comment at `items.lua:16` that explains the guard**.
75 real + 1 comment = 76 = `code`. Two errors cancelling. Wrong in both directions:
the same arithmetic reports a **phantom** mismatch on the sibling opt-in repo, whose
`items.lua` is correct (9/9, same order — checked read-only).
**Fixed:** parses the entries, compares the **ordered** list (order is load-bearing via
`ForEachModItem`). Falsified three ways; restored tree = 20 checked, 0 FAIL.

### ⚠️ L6-F3 — the published veto snippet reads a global that does not exist yet — ROUTED, record-only

`README.md:75-78` and the site's `for-modders.md:31-34` both publish
`SMRFixPack_Disabled = SMRFixPack_Disabled or {}`. The right-hand read is a **bare read
of a name that by construction is not in `_G` yet**; it routes through
`ModEnvMeta.__index` and falls to the `assert` at `Mod.lua:1553`, which — unlike
`__newindex`'s at `:1560` — carries **no `Loading` guard**.
⭐ The pack's own five reads all use `rawget(_G, "SMRFixPack_Disabled")` precisely to
avoid this (`00_Core.lua:11,187,302`, `Fix_DustDevilSpawnGate:333`,
`Fix_MeteorFrequency:168`). **We publish the one shape our own code is written to avoid.**
Functionally harmless (nil is returned after the assert); the cost is a log line whose
loudness is build-dependent — measured in MarsDebug (`C43`), ⛔ **UNMEASURED in retail**,
and the archive is **not** a control (artifact §4: the condition was never sampled).
**Route:** one-word doc fix on two public pages, owner's to apply. Checklist 45.

### ⚠️ L6-F4 — `EF-008` is unqualified about builds — NOTE ADDED, not reversed

`EF-008` says `error()`/`assert()` in mod code *"REPORT AND CONTINUE"*, with no build
qualifier and no `verified` date; `FIX_POLICY` §6 rests on it. `autorun.lua:243` —
*"Platform.asserts is set in all debug builds"* — and `Mod.lua:2951`'s
`if not Platform.asserts` both indicate the behaviour is build-specific. The advice is
right either way; the fact's **scope** exceeds its evidence. A dated scope note was
added to the fact. ⛔ Nothing reversed — this is a reading, not a measurement.

### ⚠️ L6-F5 — `F98`'s INDEX row states the dev route; the retail route is one step earlier — NOTE ADDED

⚠️ **Corrected mid-link against the entry itself.** I first wrote that `F98` had the
route wrong; it does not. Its **body already carries the retail measurement** (probe
`SKIP` on `Mars.exe`, reason *"the tech has no description T"*, vs `PASS` on
`MarsDebug.exe`). What is one-sided is its **`row_status`** — the line that reaches
`INDEX.md` and that a future session reads first — which says the no-op is
`tech.description = T(id, CORRECTED)` writing back the same id. **That assignment never
executes in retail:** `localization.lua:270-272` returns light userdata whenever
`TranslationTable[id]` exists, so `Fix_TechDescriptionBuilding.lua:66`'s
`type(desc) == "table"` is **false** and the module returns at its own guard.
⚠️ **The actionable part neither row nor body states:** the queued repair is a
`ModItemLocTable` entry chosen against the row's route — **any repair that keeps that
guard is dead in retail regardless of the loc table.** Appended to the entry body;
nothing built.

### ⚠️ L6-F6 — two exact limits on the veto promise — RECORDED, deliberately not fixed

(a) **`GameVar` declarations are not vetoed** (`Fix_MeteorFrequency:76`,
`Fix_FirstAsteroidPrefabs:115`) — a save made with a fully vetoed pack still carries two
persisted names. "Vetoed" and "absent" are not the same thing in the save and nothing
says so. (b) **6 of the 7 ungated `function OnMsg.X()` handlers check registry status
only, not the veto table**, where `FIX_POLICY` §2 requires both. For the **pre-load**
veto — the only advertised route — `Register` has already latched `"disabled"`, so the
outcome is identical. ⛔ Not fixed: seven edits to a release candidate for zero
behaviour change is the wrong trade at link 6.

### ⚠️ L6-F7 — the modder page's ordering claim omits that the order is not settable — ROUTED

`for-modders.md:36-38` says it *"does not matter whether yours or ours is created
first — only that the values are set before our code runs."* Both halves true; together
they require the modder's mod to **load before ours**, which is the player's enable
order with no priority field and no way to request a position (`EF-054`,
`FIX_POLICY` §8). The page does not say so. ⚖️ Owner's wording call. Checklist 45.

### ✅ Negatives worth inheriting (each mechanical, each stated with its method)

- **75 of 75 Register ids match the published filename rule**, alias-resolved. Zero
  mismatches, so the modder-facing derivation is exactly true.
- **The veto route holds for all 75.** Every file-scope site was read: 19 go through
  `WhenActive`, the rest self-check status or are vacuous state resets (artifact §3.2).
- **A foreign mod's write DOES reach us.** `ModEnvMeta.__newindex`'s
  `rawset(original_G, …)` (`Mod.lua:1562`) runs in every branch, and `ModsLoadCode()`
  sits between `Loading = true` and `Loading = false` (`autorun.lua:1, 423, 560`) so the
  create-assert is suppressed for all mod code, ours and theirs.
- **No second F85.** All 13 global replacements carry live shipped references (the four
  thinnest read to their callers and one level up); no member is dead.
- **The fix list tracks the current module set** — both 2026-08-15 changes are
  reflected — carries **exactly five** judgment-call entries as four surfaces promise,
  and carries **no** entry for the one module recorded as a retail no-op.
- ⛔ **Three own-instrument defects were found and fixed before any count was taken**
  (artifact §5.2), one of which would have inverted the veto verdict. A fourth is
  disclosed as a limit: the member census is blind to string dispatch.


---

## Link 7 — L7 environment & namespace (2026-08-19)

Artifact: `docs/agent/reports/L7_ENVIRONMENT_MAP.md`. Instrument:
`tools/l7_env_map.py` (new) — the global map taken from the **compiler**
(Lua 5.3 bytecode, `SETTABUP`/`GETTABUP` on `_ENV`), control battery 23/23
before any count was taken. Configuration: dev tree, unpacked, source-derived
at Src by symbol + all archived logs; **no launch** (refusal reasoned,
artifact §7).

### L7-F1 — ⛔ THE RELEASE GATE'S CRITERION 1 COULD NOT FAIL. **FIXED THIS LINK.**

`98_LAUNCH_REHEARSAL.md` criterion 1 is *"the mod loads **packed**"* and its
evidence column read *"`[CommunityFixPack]` lines exist at all"*. Those lines
are equally present when the mod loads **unpacked** — so the one criterion whose
job is to certify that run B measured the player's configuration would have
scored GREEN on the dev tree, and the other nine criteria would have inherited
that false premise.

The engine prints the fact directly: `ModPrint("once", "Loaded mod def %s (id
%s, v%s) %s from %s", …, mod.packed and "packed" or "unpacked", …)`
(`Mod.lua:1849`), off the `def.packed` flag set at `:1734`.

⭐ **MEASURED over `docs/archive/*.log`: 66 sessions carry that line for
`id SMR_CommunityFixPack`; ALL 66 say `unpacked from appdata`. `packed` has
never appeared once.** The seed note's *"never loaded packed"* is now a named,
greppable witness instead of an assertion.

**Disposition: FIXED IN PLACE** — a record, which spec §4's 2026-08-19
clarification explicitly permits (record-only means `Code/`, `metadata.lua`,
`items.lua`). Criterion 1 now reads the mode line; `[CommunityFixPack]` lines
existing is returned to criterion 2, where it belongs.
⚖️ **Not launch-blocking today** — nothing is published and B has not run. It
would have produced a false pass the first time B ran, which is why it was not
left for the terminal audit.

### L7-F2 — ⛔ AND THE CONFIGURATION HAZARD THAT WOULD HAVE TRIGGERED IT. **RECORDED IN STAGE 4.**

If the junction and a packed folder are **both** present, both defs load and
collide on `new_mods[def.id]`; the tie-break is `if cmp < 0 or (cmp == 0 and
old.packed and not def.packed)` (`Mod.lua:1770`) ⇒ **at equal version the
UNPACKED copy wins.** Both are 1.0.0, so an incomplete junction pull hands run B
the dev tree with **no warning and no error**.

Two free witnesses: the id enters `multiple_sources` and raises
`ModMessage("Mod %s loaded from %s (%s)")` (`:1800`); and criterion 1's mode line
says `unpacked`. ⚠️ The packed/unpacked branches are `if`/`elseif` on ONE folder
(`:1724`/`:1748`), so a single folder is never ambiguous — the hazard is strictly
**two folders carrying one id**. Route: written into `98_LAUNCH_REHEARSAL.md`
stage 4 step 2, where the gate runner will actually read it.

⚠️ Rig state read this session: `AppData/…/Mods/` holds three junctions
(`SMR-BugFixPack`, `SMR-BugFixPack-TestKit`, `SMR-OptInPack` — the last restored
2026-08-19 00:30, still owing an owner tick per `H-08`). **No packed build of
this mod exists anywhere on disk**, so stage 2 packaging is outstanding, not
merely unverified.

### L7-F3 — ⚠️ Three global FUNCTION replacements bypass the pack's own §1.4b read-back. **RECORD ONLY.**

`SMRFixPack.SetGlobal` exists to carry the read-back `FIX_POLICY` §1.4b makes
mandatory. 13 sites use it; three replace a vanilla global function by bare
assignment instead:
`Fix_ShuttleTransportCache.lua:52` (`FindTransportationModeToCommunity`) ·
`Fix_LandscapeUnitFilter.lua:62` (`LandscapeForEachUnit`) ·
`Fix_WispRewards.lua:30` (`SetLightTrapMode`).

⚖️ **Severity stated with the condition SAMPLED, not assumed.** The only way
`ModEnvMeta.__newindex` can fail to land a write is a **blacklisted key**, and
this link mechanically proved `writes ∩ ModEnvBlacklist = ∅` over all 149
blacklist entries. ⇒ the failure mode §1.4b guards against is **excluded here**,
not merely unobserved. **Policy-consistency finding, not a behaviour defect;
⛔ not launch-blocking.** Route: terminal audit, with the whole finding set
visible — it is three one-line changes, and it is exactly the kind of edit spec
§4 says has plausibly negative expected value on a release candidate.

### L7-F4 — ⚠️ The lens brief expected three pack globals. There are five. **CALIBRATION.**

`02_LENS_NOTES.md` L7 says *"Expected: `SMRFixPack`, `SMRFixPack_Disabled`,
`SMRFixPack_Optional`"*. The complete set is those three **plus two `GameVar`s**:
`SMRFixPack_MeteorLatch` (`Fix_MeteorFrequency.lua:76`) and
`SMRFixPack_FirstAsteroidPrefabs` (`Fix_FirstAsteroidPrefabs.lua:115`, declared
through the alias `GameVar(FLAG, false)` that a plain grep cannot join).

Both are deliberate, headered, and already counted by L3's persisted-state
census — they are new only to **this lens's stated expectation**, which is what
needed correcting. ⛔ **No sixth name exists.** Route: the lens-notes L7 block is
corrected this link, so link 8 and any re-take inherit the right number.

### L7-F5 — ⭐⭐ NEGATIVE WORTH INHERITING: the TestKit has NOT been holding the pack up.

Six consecutive links ended *"TestKit tree excluded"*. It is swept here for
namespace, with the same instrument (20 files, 7 write sites, 2,062 read sites):

| question | answer |
|---|---|
| pack **reads** a global only the TestKit creates | ⛔ **NONE** |
| pack **writes** a name the TestKit also writes | ⛔ **NONE** |
| TestKit **writes** a name the pack also writes | ⛔ **NONE** |

The kit adds 6 session globals (`SMRTest`, `SMRAutoRun`, `SMRTest_AutoRunEnabled`,
`SMRTest_EnablePathLeg`, `SMRTest_EnablePathRunning`,
`SMRTest_EnablePathSawPackOff`), neuters `ShowStartGamePopup` outright for
autorun legs (`95_AutoRun.lua:265` — so **every archived leg ran with a vanilla
popup suppressed**), and swaps three vanilla globals around specific probes,
restoring each (`MeteorsDisaster` `90_Loggers.lua:76`/`:83`; `RequestAssignUnit`
and `RequestUnitFulfill` `91_Stress.lua:366`/`:372`, restored `:383-384`).

⚠️ **Scope, so it is not over-read:** this is a **static namespace** result. It
does not say run B will pass. It says the specific failure mode *"the pack
silently depends on something only the instrument supplied"* is **excluded** —
previously unmeasured and unexcludable, and the single most useful thing to know
before B.

### L7-F6 — ⭐ NEGATIVES WORTH INHERITING: neither engine assert can be reached by this pack.

All re-derived at Src this session (`Mod.lua:1546-1611`), not inherited:

* **No write can trip the strict-global create-assert.** The assert needs
  `not Loading` AND `PersistableGlobals[key] == nil` AND the name currently nil.
  All 8 vanilla names the pack writes from nested scope are `GameVar`s
  (`Lua/Meteors.lua:38`/`:39`, `Lua/MapSettings.lua:125`,
  `Lua/Units/Colonist.lua:2478`, `Lua/TerraformingDisasters.lua:323`) or
  file-scope global functions; our own two nested writes are `GameVar`-declared,
  which puts them in `PersistableGlobals` and rawsets them non-nil at declaration
  (`lib.lua:1049-1055`).
* **No read can trip the undefined-global assert.** All **187** distinct global
  names the pack reads were crossed against the whole shipped tree (4,446 Src
  files, 10,956 definitions, plus a second indentation-tolerant pass — the first
  pass under-detected 11 names and that is disclosed in the artifact). Every one
  resolves: Lua base library, documented engine C exports (`EF-014`'s
  `GatherTransportableResources` among them), or engine-managed env keys
  (`CurrentModOptions`, `EF-004`; `TechDef`, a preset `GlobalMap` container,
  read only inside a wrapper gated on a researched tech).
  ⭐ The reason is structural, not luck: every possibly-absent name
  (`Mods`, `WaitMessage`, `GetPreGameMainMenu`, `ModLog`, `FlushLogFile`) is read
  through `rawget(_G, "…")` and appears in the bare-read set **not at all**.
* **Zero env-table shadows.** `safe_rawget` prefers an own key over real `_G`, so
  a `rawset(_G, k, v)` would make our reads diverge from the game's. The pack has
  exactly one `rawset(_G, …)` site (`Fix_FirstAsteroidPrefabs.lua:129`) and it
  writes **nil** — it clears a shadow rather than creating one.
* **No blacklist collision.** `writes ∩ ModEnvBlacklist = ∅`; the four
  blacklisted names the pack reads (`Msg`, `OnMsg`, `_G`, `rawget`) all have
  own-key overrides installed by `LuaModEnv` (`Mod.lua:1600-1607`). This upgrades
  `EF-006`'s hand-checked *"uses no blacklisted API"* to mechanical over 76 files.
* **No platform-conditional code at all** — `Platform` is never read by any of
  the 76 files, so `FIX_POLICY` §7's constraints cannot be violated by a platform
  branch. ⚠️ That is a different claim from "it behaves correctly on console."

### L7-F7 — ⭐ `content_path` is configuration-INVARIANT. **CLOSES AN INHERITED OPEN ITEM.**

Link 5's row left open: *"`content_path` in the PACKED case was not compared to
the unpacked one, so the engine's mod-flag match may behave differently in
configuration B — the gate."* `EF-065`'s player-facing *"Mod Flagged"* box is
keyed on it.

Re-derived: **both branches converge on one line.** `Mod.lua:1755` sets
`def.content_path = ModContentPath .. def.id .. "/"` and `ModContentPath = "Mod/"`
is a constant (`Mod.lua:6`); the packed/unpacked branches (`:1724-1740`/`:1748`)
differ only in where the def is read from, and `MountContent` (`:857-862`) mounts
either the pack or the folder **at that same path**.
⇒ `content_path` is `"Mod/SMR_CommunityFixPack/"` in both configurations, and
`ReportModLuaError`'s match behaves identically in run B. **Answered by source; it
does not need the gate to settle it.** Route: `EF-065` may carry this at the
terminal audit's discretion — not amended here, because that fact's text is not
wrong, only silent on the packed case.

### L7-F8 — observation, logged so it is not re-discovered as alarming

63 archived logs name the pack `v1.00-001`; the 3 newest name it `v1.00-000`,
which matches the frozen `metadata.lua` (`version 0`, `version_major 1`,
`version_minor 0`). The revision was reset 1 → 0 before the freeze.
⛔ **No consequence**: nothing is published, so no player has ever seen `-001`,
and `CompareVersion` only matters between two installed copies. Recorded per the
house rule that a log line is never silently discounted. **No route needed.**

### L7-F9 — cosmetic, not edited

`docs/PLAYTEST_HELP.md:26` heads an item *"Achievements stay ON with mods on PC"*
— a bare "PC" of the kind `FIX_POLICY` §7 warns about — but qualifies it in the
same sentence (*"they are mod-blocked only on console/MS Store"*), so the claim
is accurate. It is an owner-facing doc, not a player surface, and `README.md:51`
words the player-facing version correctly (*"Steam and other PC versions"*).
⇒ **Loose, not wrong. Left alone** — a human doc is not edited on a cosmetic.

---

## Link 8 — lens L8, adversarial / hostile modder (2026-08-19)

⛔ **Nothing here blocks launch.** Every finding below needs a third party — a
foreign mod, a fork, or a console line before our load — to supply the condition.
The shipping configuration is green in both controls of the harness.

Derivation: `reports/L8_ADVERSARIAL_MAP.md`. Instruments (both new, both
control-tested before use): `tools/l8_hostile_input.py` (2 controls pass),
`tools/l8_deference_map.py` (`--selftest` 11/11).
⛔ **No third-party mod was installed** — standing baseline policy; every
foreign-mod result is source-derived by construction.

### L8-F1 — `SMRFixPack_Disabled` is indexed with no type guard at the one site that runs 75 times at file scope

`00_Core.lua:446` — `if SMRFixPack_Disabled[id] then` — runs inside `Register`,
and `Register` is called at **column 0 in all 75 fix files** (measured: 75 of 76
`SMRFixPack.Register(` occurrences are at column 0; the 76th is the definition).
`:11` adopts whatever a foreign mod left in the global (`rawget(...) or {}`), so a
non-table value reaches `:446` intact.

MEASURED on the shipped source under Lua 5.4, with `pdofile`'s per-file pcall
reproduced (`lib.lua:242-251`):

| seeded value | modules lost |
|---|---|
| `SMRFixPack_Disabled = true` | **75 of 75** |
| `SMRFixPack_Disabled` with a throwing `__index` | **75 of 75** |

⭐ **And the pack's own health surface reports nothing true.** `Register` reaches
`:440-443` before it throws, so all 75 ids sit in `fixes`/`order` with status
`pending` — a status no other path produces. `UpdateSuspects` (`:521-541`) tests
only `error` and `inactive`, so `pending` is **not suspect**, the stand-down
dialog never fires, and `ListFixes()` prints 75 `[pending]` lines. The engine is
loud (75 collected load errors); we are silent and wrong.

⛔ The same guard is present and correct at **four** other sites
(`00_Core.lua:187-188`, `:302-303`, `Fix_DustDevilSpawnGate.lua:333-334`,
`Fix_MeteorFrequency.lua:168-169`) — all four run *inside* a pcall someone owns.
The two unguarded sites (`:446` and `:55`) are the two that run **outside** every
pcall the pack owns.

`00_Core.lua:55` (`SMRFixPack_Optional[id]`, same shape) is **latent, not live**:
its only caller is the `def.optional` branch at `:467` and there are 0
optional-gated files today.

**ROUTE:** terminal audit. The repair is a two-line type guard at `:446` and `:55`
(or a normalising `type(...) == "table" or {}` at `:11`/`:15`). ⛔ Record-only at
link 8; `Code/` is barred and this is not launch-blocking.

### L8-F2 — the `SMRFixPack` sub-table defence is inverted

`00_Core.lua:24-25` re-fills `defs` and `data_edited` (`SMRFixPack.defs =
SMRFixPack.defs or {}`), but `fixes` and `order` get no such line — and
**`fixes`/`order` are the two indexed at file scope** (`:439`, `:443`).

MEASURED, same harness:

| seeded value | result |
|---|---|
| `SMRFixPack = true` | ⛔ **all 76 files dead, including `00_Core` itself** (`:24`) |
| `SMRFixPack = {}` — a fork, a second copy, a shim | ⛔ **75 of 75 dead** at `:439`; `00_Core` survives *because* of `:24-25` |
| `SMRFixPack = {fixes={}, order={}}` | ✅ loads and registers normally |

⇒ The two sub-tables that were defended are the two that did not need it at file
scope; the two that needed it have nothing. The last row is the proof.

**ROUTE:** terminal audit, alongside L8-F1 — same file, same class of repair.

### L8-F3 — two well-formed veto values fail silently

`SMRFixPack_Disabled = "DustDevilSpawnGate"` (a string is indexable via the string
metatable) and `SMRFixPack_Disabled = {"DustDevilSpawnGate"}` (a list, keyed `[1]`)
both throw nothing, log nothing, and **veto nothing**. The modder believes the fix
is off; it is running.

⚠️ `README.md:71` says *"Setting a fix's identifier in that global table"*, which
is a fair reading of the list form. This is a **wording + robustness** pair, and it
sits beside link 6's separate finding about the same published snippet.

**ROUTE:** terminal audit (code) + owner (README wording). Not filed as a defect
against the code alone.

### L8-F4 — the deference census: 24 of 66 patch sites are full replacements, and nobody had a number

`tools/l8_deference_map.py`, alias-resolved (five forms). The sound direction: a
module with **no textual reference anywhere** to the prior value of its target
**cannot** chain, so the tool emits a lower bound on replacements and never an
upper bound on chaining; `reads-prior` rows are candidates and were read by hand.

| kind | sites | REPLACES | reads-prior |
|---|---|---|---|
| global function | 16 | **11 (69%)** | 5 |
| class method | 50 | **13 (26%)** | 37 |
| **total** | **66** | ⛔ **24 (36%)** | 42 |

⛔ **This is NOT a policy violation and must not be written up as one.**
`FIX_POLICY` §1.5 sanctions full replacement and names this exact consequence
itself (*"the fixes most likely to clash with other mods"*). Every replacement
sampled carries the §1.5-mandated Src-file-and-lines header — **the "accidental
clobber" hypothesis is refuted, not merely unobserved.**

⭐ **What it IS:** §1.5 says *"keep the list short"* and **the list has never been
counted.** A soft bound with no measurement cannot be checked — L6's *"a guard is
a claim too"*, pointed at a budget.

⚠️ **And two published surfaces state the preference as the practice:**
`README.md:66` *"chain rather than clobber"*, and `00_Core.lua:4-6` *"so other
mods that hook the same functions keep working"* — the second asserts an outcome
for other mods that holds at 42 sites and does not hold at 24.

**ROUTE:** owner (wording, on the checklist). The 24 replacements themselves are
correct §1.5 decisions and are **not** proposed for change.

### L8-F5 — the pack's own restore benchmark re-installs rudely, on the ordinary cold-boot path

Link 1 nominated `Fix_DustDevilSpawnGate:250-258` as the correct save/restore
discipline and assigned the sweep of the rest here. Result: **exactly two** of the
16 global replacements have any restore path (`Fix_DustDevilSpawnGate`,
`Fix_DustDevilsDescrMap:73-81`), both the same helper.

The **restore** branch is exactly as praised — re-read the live value, swap back
only `if cur == wrapper`, so a later replacement is left alone. ⛔ **The
re-install branch has no such check:**

    if want and cur ~= wrapper then _G.OverrideDisasterDescriptor = wrapper end

`cur ~= wrapper` is not a safety test — it is *"have we been displaced"*, and its
answer is *"put ours back."* Whatever `cur` held is **overwritten, never captured**
(`orig` still holds the pre-us value) and **nothing is logged**.

`set_installed(true)` is called from the `DataPatch` pass (`:307`), which the
shared runner fires on `ClassesBuilt` / `DataLoaded` / `ModsReloaded` /
`DataChanged` (`00_Core.lua:334-354`). Cold boot, traced:

    ModsLoadCode()   ...our apply installs `wrapper`
                     ...a foreign mod enabled AFTER us installs its own  <- displaced
    Msg("ClassesBuilt")  presets empty -> pass returns early
    Msg("DataLoaded")    pass runs -> set_installed(true) -> OVERWRITTEN, silently

⇒ The two modules that gained a re-install path to survive **their own** latch/heal
cycle gained, with it, the **only mechanism in the pack that un-does someone
else's patch after they installed it** — and it contradicts `EF-054`'s recorded
design intent (*"a mod that replaces the function outright simply wins… the
correct outcome"*) on the one path where the pack can contradict it.

⚖️ Blast radius **2 globals** (`OverrideDisasterDescriptor`, `GetDustDevilsDescr`).
⛔ Not launch-blocking — needs a foreign mod on one of those two names.

**ROUTE:** terminal audit. Candidate repair: capture in the `want` branch too, or
decline to re-install when `cur` is neither `wrapper` nor `orig`. ⚠️ Both change
behaviour of a working module, which is exactly the risk spec §4 switched to
record-only for.

### L8-F6 — under a foreign conflict, both blame surfaces point at us

**(a) The engine's box.** Re-derived at Src this session
(`Mod.lua:3001-3015`), whose own comment reads *"rough estimation based on call
stack"*: `OnMsg.OnLuaError` flags **every** mod whose `content_path` appears in the
error **or the stack**. Our 42 chaining wrappers are *designed* to be on the stack
of what they wrap ⇒ **a foreign mod that loaded before us and throws inside its own
wrapper puts our path on the stack and the box names us.** The message is built as
a **list** (`mods_str = table.concat(mods, "\n")`, `:2981-2992`), so the surface
names several mods at once with no ordering and no blame. ⛔ Not actionable — the
engine owns it, we have no call site, `config.DisableErrorReporting` is the only
switch. Recorded so a wild *"the fix pack broke my game"* report is read correctly.

**(b) Our own dialog.** Counted over `Code/`: **238 shape checks** (113 `global=` +
106 `class=` + 19 `path=`) against **7 `test=`** content checks, in 69 modules.
Shape checks fail with *"…not found (game update changed it?)"* and set
`update_suspect` (`00_Core.lua:157-163`) ⇒ **a foreign mod that removes, renames
or nils a symbol we depend on produces a player box blaming a game update and
sending the player to look for a fix-pack version that will not exist.** The 7
`test` entries deliberately cannot reach it (`:160-162`) — correct design.

⭐ **Negative worth inheriting:** a foreign *wrapper* trips none of the 238,
because wrapping preserves the type. The pack is blind to being wrapped — no false
stand-down — and only a **destructive** foreign action reaches the dialog.

⚠️ L4 already found this sentence dishonest for a different cause (`status ==
"error"` announced as a game update). This is a **third** cause of the same
sentence. **Recorded as a third input to an open wording decision, not as a new
defect.**

### L8-R1 — record correction (not a finding): `EF-058` amended in place

The flattened-class trap is keyed on **install time relative to `Msg("Autorun")`**.
Re-derived at Src: `ModsLoadCode()` is a direct call at `autorun.lua:423`, and
flattening happens in `classes.lua`'s `function OnMsg.Autorun()` ⇒ mod load
strictly precedes flattening, so the pack's **50** method patches (all at file
scope or inside a synchronous `Register` apply) are copied **down** into subclasses
and are safe by construction. ⛔ The amendment weakens nothing: all four recorded
bites were **runtime-installed instruments**, where the trap is exactly as live as
before. Permitted by spec §4's 2026-08-19 clarification (records, not code).

### L8-A1 — the launch ask (spec §6.5), routed to the owner

⛔ **Not a refusal.** There is a launch worth taking for this lens and it is named
exactly: **a leg with the opt-in pack loaded.** It wraps two of the same methods we
wrap (`UniversalRocketBase:GetFuelResourceRequest`, `Drone:CleanUnreachables`,
`EF-054`) and is the only two-independently-authored-wrappers-on-one-method
observation this project can ever make. It is blocked on an **owner Mod-Manager
tick** (`EF-055`, `H-08`) which an agent may not spend. **Asked on the checklist,
with predictions written in advance.**

⚠️ What was NOT done and why: another run-A leg. Fix pack + TestKit with the opt-in
absent ran **three times** on 08-19 and contains **zero** foreign wrappers — it
would measure nothing this lens asks.


---

# ⛔ LAUNCH REHEARSAL (`98_LAUNCH_REHEARSAL.md`) — 2026-08-19

⛔ **NOT A LINK. No lens taken, rotation undisturbed.** This is the A/B gate
runner reporting from a run that **stopped at stage 2**. Findings are numbered
`LR-Fn` so they cannot collide with a link's `Ln-Fn`.

⛔ **LAUNCH-BLOCKING FINDINGS: NONE.** Nothing here is a defect in the shipped
mod. LR-F1, LR-F2 and LR-F10 block **the gate**, which is a different thing, and
they are procedural rather than in `Code/`.

**Fence note (declared, per spec §2's surviving clause):** `SWEEP_FINDINGS.md`
was **not** opened and no sweep commit body was read. `L5-F3`'s console line was
obtained from `reports/L5_CONTAINMENT_MAP.md` §4/§7 and `PLAYTEST_CHECKLIST.md`
item 44, both of which the brief pointed at.

## LR-F1 ⛔⛔ Stage 2 cannot be executed by an agent — `DbgPackMod` is blacklisted, and the whole gate is behind one console line

`ModEnvBlacklist` carries **`DbgPackMod = true`** (`Mod.lua:1322`, in the
"file operations" block) and **`ReloadLua = true`** (`:1274`).
`ModEnvMeta.__index` opens `if env_blacklist[key] then return end`
(`:1546-1547`), so a blacklisted name reads **`nil`** in every mod environment —
`safe_rawget` repeats the test at `:1577-1583`. ⇒ **no mod code can call it**:
not `Code/` (barred anyway), not a TestKit probe (barred by the 96-count rule),
not a TestKit autorun step (which is the one route nothing had ruled out, and it
is closed by the engine, not by policy). The console is the only route and an
unattended session cannot type into it — the same wall `checklist 44` hit and the
same one links 5, 6 and 7 each refused a launch over.

⇒ **The brief's instruction *"No packed build of this mod exists anywhere on
disk … You are building it"* is not executable.** Routed: `PLAYTEST_CHECKLIST.md`
item 52, act 1.

## LR-F2 ⛔ The single-owner-visit plan is impossible; the gate is two game sessions with an agent step between

The brief loads four jobs onto one visit — the Mod-Manager tick, the two
core-fix console reads, L5-F3's `MapForEach` line, criterion 7's look at the
preview. **They cannot share a visit.** The packed install cannot exist until
the owner packs (LR-F1); the tick and criterion 7 are *about* the packed
install. ⇒ act 1 (pack + all console reads) → agent reconciles and stages →
act 2 (tick + the looks + the save round trip). Rewritten in §4 of the brief and
scripted as one walk-through in item 52.

## LR-F3 ⚠️ A packed build DOES exist on disk, and it was built by the Mod Editor, not by a console `DbgPackMod`

`%LOCALAPPDATA%\Temp\Surviving Mars Relaunched\ModUpload\Pack\ModContent.fpk`
— **359,353 bytes, 2026-08-17 19:34:59, md5 `458801c65cc9d4e12eb941517c6918bb`,
80 entries.** The brief says none exists anywhere; the correct statement is that
none exists **that is current**.

⭐ **And its provenance matters more than its existence.** The session that
produced it is `logs/MarsDebug.exe-20260817-19.30.31`, whose only Lua line is
**`Initializing ged app: ModEditor`** — the owner clicked *pack* in the Mod
Editor. ⇒ the **Ged route is PROVEN and the console route has never been run**,
which is the opposite of what stage 2 assumed, and it is why item 52 warns about
`IsDirty()` and the mid-game reload rather than treating the line as routine.

## LR-F4 ⭐ MEASURED: the engine's packer is byte-faithful — a packed-vs-unpacked worry class retired without a launch

All 80 entries extracted (through `flpk_extract.py`'s own `extract()`) and
byte-compared to the working tree: **78 byte-identical, 2 differ**, and the two
are exactly `git diff 7824cbc..HEAD` — `Code/00_Core.lua` and `items.lua`.

⇒ packing applies **no transformation**: no line-ending rewrite, no minify, no
re-encode, and zstd round-trips exactly. Whatever else differs between the
packed and unpacked cases, **it is not the bytes of our Lua** — which is a
result stage 5 explicitly asked this rehearsal to hunt for and nothing else in
the project would have produced. It also makes the existing artifact's staleness
**exact**: a rebuild changes those two files and nothing else.

## LR-F5 ⭐ The file-list prediction is now controlled, not asserted

`tools/pack_predict.py` reimplements `GedModEditor.lua:716-732` (recursive list
minus `ignore_files`, `*` crossing `/`) and reproduces the real engine-built
archive **80/80 by name**. Run against the current tree it also predicts 80 —
76 `Code/*.lua` + `items.lua` + `metadata.lua` + `LICENSE` + `preview.png`, with
`.git` (260 files), `docs/` (403), `tools/` (20), `.claude` (1), `README.md`,
`CLAUDE.md`, `.gitignore`, `.gitattributes` all excluded. Three patterns match
nothing (`*.svn/*`, `*/Source/*`, `*/SourceData/*`) — harmless, recorded so the
next reader does not treat them as coverage. `tools/pack_list.py` reads a real
archive and reconciles by name **and by content**.

⛔ **One own-instrument defect found and disclosed.** `pack_list`'s content
reconcile was first written as a hand-rolled "scan the region for zstd frame
magics" pass; it reported **7** files differing where the project's own
extractor reports **2** — the magic bytes occur inside compressed data, so the
naive split silently truncated multi-chunk files. Fixed by routing through
`flpk_extract.extract()` before any number above was taken.

## LR-F6 ✅ `CheckModPackSignature` answered — stage 4.2's flag and link 7's open item 4 both close

`CheckModPackSignature` opens `if not AreModSignaturesRequired() then return
false, true end` (`Mod.lua:87-89`), and `AreModSignaturesRequired` is
`return Platform.playstation` (`:49-52`). ⇒ on PC it returns `false`
immediately, so `io.exists(pack_path) and not CheckModPackSignature(pack_path)`
(`:1724`) **takes the packed branch**. Mod signing is a PlayStation-only
concern; no `.sign` file is needed and none is produced.

## LR-F7 ⛔ Criterion 2's derivation is wrong twice and yields the wrong number

The cell says *"the 75 ids in `metadata.lua`'s `code` list minus
`00_Core`/`90_SaveSanitizer`"*. The `code` list holds **76** entries, not 75;
and `90_SaveSanitizer` **does** emit an `applied` line
(`vl97a_…:152` — `[CommunityFixPack] SaveSanitizer: applied`). That recipe
computes **74** and would send a runner hunting a module that does not exist.
**MEASURED: exactly 75 `applied` lines per load.** The number was right, the
route to it was not — the same failure mode the chain has caught three times.

## LR-F8 ⛔ Criterion 6 asks for a token its own evidence line never prints

`ModDef:GetVersionString()` is `string.format("%d.%02d-%03d", version_major,
version_minor, version)` (`Mod.lua:1176-1178`), so the mode line at `:1849`
reads **`v1.00-000`** and the string `1.0.0` appears nowhere on it. A runner
told to confirm "1.0.0" there cannot distinguish a pass from a missing line.
**PASS is the literal `v1.00-000`.** *(The player-facing `1.0.0` is
`PackVersion`, a different surface, which is why the Mod-Manager look stays in
act 2.)*

## LR-F9 ⚠️ Criterion 3's "any third site is the real failure" is refuted by the corpus it cites

Re-measured over all 73 `docs/archive/*.log`: `Flight.lua … objects_to_mark`
**418**, `objects_to_unmark` **7** — **plus four non-`Flight` sites already
present and already attributed**: `TrackElement.lua … 'TestMeteor'` (3),
`GedGameObjectEditor.lua … 'GetSpotNameColor'` (2), `GridObject.lua …
'GetShapePoints'` (1), `upvalue 'old_threads'` (1). ⇒ a third site is an
**attribution job**, not an automatic gate failure; the decisive test is the one
the cell already names — our content path in the message or stack.

✅ **Both of the owner's 08-19 numbers re-measured and confirmed:** 21 of 73 logs
carry ≥1 `LUA ERROR`, **52 carry none**; and 66 of 66 mode lines for
`id SMR_CommunityFixPack` say `unpacked`, `packed` never once.

## LR-F10 ⛔⛔ Run B has no driver — four of its ten criteria are owner work, not log reading

Every unattended primitive this rig owns — staged-copy load by filename, in-run
`SaveGame`, scripted state reads, speed control, the watchdog — runs from a
`CreateRealTimeThread` **inside the TestKit**, and Mod-Manager / main-menu
driving is **descoped by owner rule** (`WORKFLOW.md` capability envelope: *"the
enable click stays human"*). **Run B turns the TestKit off.** ⇒ B cannot load a
save, cannot save, cannot read a variable and cannot quit itself.

| criteria | who |
|---|---|
| 1 · 2 · 3 · 4 · 6 · 10 | agent, from a boot-and-close leg + the log |
| 5 · 7 | ⛔ owner — screen events |
| 8 · 9 | ⛔ owner end to end — UI driving, not log reading |

⚠️ The brief's *"everything below is readable from the log file and the screen"*
is literally true and smuggles a human in through the word **screen**. *"B looks;
it does not poke"* stands; **who does the looking** was never stated.

## LR-F11 ⭐ Criterion 5 is half log-decidable and never said so

The pack's one designed screen surface logs at `00_Core.lua:540` **before** it
draws — the same mechanism criterion 4 leans on — and L4's census measured that
the pack raises no notification, popup, banner or voice line of its own. ⇒
absence of that line is a positive log-side negative covering everything the
pack can author; the attended half is only *"was anything else on screen"*.

## LR-F12 ⚠️ The 08-17 upload sitting's logs are not in the archive corpus

`logs/Mars.exe-20260817-19.26.13`, `…-19.29.38` and five
`MarsDebug.exe-20260817-*` live only in
`%APPDATA%\Surviving Mars Relaunched\logs`. ⇒ every *"all 73 archived logs"*
count in this chain — link 5's error census, link 6's build table, link 7's
66-log packed/unpacked witness — **excludes the one sitting in which the mod was
packed and an upload was attempted.** Not a defect in any link, which counted
what was there; but the corpus should absorb them before the terminal audit
calls the log evidence complete.

## LR-F13 ⚠️ `ipairs(mod_def.entities)` is safe, and only a measurement says so

`ModDef.entities` declares `default = false` (`Mod.lua:273`) and our
`metadata.lua` carries no `entities` field, yet `CreatePackageForUpload` runs
`for _, entity in ipairs(mod_def.entities)` (`GedModEditor.lua:707`) — which
throws on a boolean. It evidently does not, and the reason is **measurable
rather than derivable**: `ModsReloadItems` runs `next(mod.entities)` unguarded
for **every** enabled mod on every launch (`:2101-2102`, `:2114-2115`), and 66
archived launches carry no such error. ⇒ the field is a table at runtime.
Recorded because the owner's act-1 line 5 depends on it and nothing had checked.

## LR-F14 ⚠️ The owner recipe's own ordering runs the one risky step in the one place nobody has measured

`checklist 44` says *"Any save, any colony"* and puts `DbgPackMod` at step 3 —
but `DbgPackMod` → `CreatePackageForUpload` calls **`ReloadLua()`**
(`GedModEditor.lua:713`) **before** it packs, and a **mid-game** `ReloadLua` is
exactly L2's unmeasured territory (its ledger row: every caller it found is
main-menu or Ged). Meanwhile `L5-F3`'s line needs a **loaded colony**
(`AllMapsForEach(true, "Colonist", …)`). ⇒ the reads split: colony-dependent
lines first, then **back to the main menu** for the reload. Item 52 orders them
that way and says why.

## What this rehearsal did NOT reach

* ⛔ **Run B, entirely.** Not one criterion was scored. The gate is unrun and
  this session did not change that — it made the block explicit and costed it.
* ⛔ **No launch, and no `EF-056` exposure.** Nothing was pulled, staged,
  enabled or disabled; the rig is exactly as found. Both autosaves were
  nonetheless pre-copied (MD5-verified, `_ref/EF056_precopy_20260819_gate`) with
  a name census, so act 1 can start without a preparation step.
* ⛔ **Run A's falsifier block** — console, therefore owner. A's suite half was
  deliberately **not** re-run: `Code/` and `metadata.lua` are byte-identical to
  the tree the 08-19 legs ran, and `items.lua` is not read at game load
  (`ModDef:LoadCode` iterates `self.code`, `Mod.lua:498-517`; `LoadItems` is
  Mod-Editor-only, `:590-591`). A re-run is the same experiment at the cost of a
  real save exposure.
* ⛔ **Criteria 7 and 8 remain the two nobody has evidence for at all** — the
  preview image has never been *seen* on the packed path (though it is now
  source-settled to *resolve* there in all three folder-name cases), and no save
  round trip has ever been taken with this pack packed.
* ⛔ **Whether the packed branch behaves as derived** — `MountPack`, `def.packed`,
  `metadata.lua` read from inside the archive. LR-F6 says the branch is *taken*;
  nothing has watched it run.

---

# RUN B — RAN AND SCORED 2026-08-19 (attended). ⭐⭐ 10 of 10.

⚖️ **Everything in the "did NOT reach" block above is now reached**, except where
noted below. The rehearsal is consumed in the same commit as this entry.

## LR-F15 ⛔⛔ The park's premise was wrong: the console was NEVER the route

The park (and `checklist 44`/`52` act 1 step 5) rested on *"`DbgPackMod` is
`ModEnvBlacklist`'d, so only the console can call it, and the console is the
owner."* **MEASURED on retail `Mars.exe`: `DbgPackMod` AND `ReloadLua` are both
`nil` in `_G` at the console** — direct call, not just `rawget`. Both ship inside
`Packs/Lua.fpk` with **unconditional top-level definitions** (extracted and read
with the project's own `flpk_extract`), so "stripped retail build" is *also*
wrong as an explanation. ⛔ `ModEnvBlacklist` only ever governed **mod code**; it
never said anything about the console, and three sessions inherited that
conflation. ⚠️ **Two owner launches were spent on it before it was measured.**

⭐ **The route that works is the Ged UI:** Mods Manager → **Edit** (`Ctrl-E`) →
Mod Editor → **File → Pack Mod** (`ModEditor.lua:62-69` → `GedOpPackMod` →
`DbgPackMod`, `GedModEditor.lua:863`). It is a **menu item with no icon and no
toolbar button**, which is exactly why it read as "no pack option".
⚠️ It loads a **scratch colony**, so act 1's "pack at the main menu" ordering is
**unreachable by this route**. Accepted rather than worked around: that rule
existed to protect the owner's *live* colony, and none is loaded on the editor
map. ⇒ **`LR-F14`'s ordering fix is right for a console route that does not exist.**

⚠️ `MarsDebug.exe` is the **Ged host process**, not a different build the owner
must launch — three `MarsDebug` processes were alive while `Mars.exe` ran the game.

## LR-F16 ⭐⭐ PACKED ≡ UNPACKED at module level — the result the rehearsal existed for

The 75 `applied` module names in run B (packed) are **set-identical** to
`vl97a`'s (unpacked junction): **0 names only-packed, 0 only-unpacked**. Stage 5
called a packed/unpacked behavioural difference *"the single most valuable thing
this rehearsal can produce."* **There is none**, and that is now measured rather
than assumed.

## LR-F17 The ten criteria, by name

`1` **`packed from appdata`** — ⭐ first in project history; 66 archived sessions all
say `unpacked` · `2` **75 `applied` by name**, `SaveSanitizer` among them (confirming
`75 = 76 − 00_Core`), `SaintBlessing`'s pre-registered benign cycle intact ·
`3` ⭐ **ZERO `[LUA ERROR]`** · `4` 0 `update report:` (+ act 1's `#UpdateSuspects()==0`
as the decisive read) · `5` two screen events, **both vanilla and attributed**
(`Welcome to Mars`; *"missing or outdated: …Test Kit"*, caused by our own untick) ·
`6` `v1.00-000` on the mode line **and** the Mods screen · `7` ⭐ **preview RENDERS
packed** — first ever test of a path hand-written against the unpacked install ·
`8` `C47FARM` → `c47farmreload` → reload, witnesses reappear, 0 new errors ·
`9` ⭐ **uninstall holds for all 75 at once**: all three defs *"present, but not
loaded"*, **0 `[CommunityFixPack]` output**, 0 errors across load/sols/save/reload
into `c47farmnomod` · `10` saves 81→83 (both new files the owner's own), autosaves
MD5-identical throughout.

## LR-F18 ⚠️ A LOG TRAP: that mod line prints two DIFFERENT objects

`ModDefPersist` (`Mod.lua:1195-1208`) has two branches and they do not print the
same thing:
* *"present, but not loaded"* → `mod_def:GetModLabel()` = **the INSTALLED def**.
* *"loaded with a different version"* → `mod_info:GetModLabel()` = **the SAVE's
  record**, then the installed version.

⇒ The same unmodified save printed `Community Fix Pack … v1.00-001` in one log and
`Relaunched Fix Pack … v1.00-000` in the next. ⛔ **That reads as "the save was
silently rewritten" and it is not** — `C47FARM`'s mtime is unchanged (2026-08-15
14:47:46). Only the first branch tells you anything about the save.

## LR-F19 `EF-055`/`H-08` is narrower than recorded — a swapped id KEEPS its enable

Pulling the fix-pack junction did **not** cost the enable, because the packed
folder carried the **same mod id**. ⇒ *"a junction pull costs the enable"* holds
for an id that **vanishes**, not one that is **replaced folder-for-folder**. The
budgeted owner re-tick was unnecessary. ⚠️ `H-08`'s hazard still stands as written
for the opt-in case that produced it.

## LR-F20 ⚠️ An instrument lied during scoring, and it lied GREEN

The first packed-vs-unpacked name comparison used `grep -P`, which this locale
rejects (`-P supports only unibyte and UTF-8 locales`). **Both name lists came
back empty and the equality check compared nothing to nothing and reported
"identical".** Caught and redone with `sed`; `LR-F16` is the real measurement.
⇒ **A comparison that can pass on empty input is not a comparison.** Same family
as `pack_list`'s disclosed defect and `upload_preflight`'s old guard that counted
its own header comment — the third self-flattering instrument in this chain.

## What run B still did NOT reach

* ⛔ **The portal-shaped folder name.** Run B used the **id-matching** folder
  (`SMR_CommunityFixPack`) to keep *packed* the only new variable. Stage 4 step 3's
  second case — a `pdx_<id>_<version>`-shaped name — is **unrun**; it is
  source-settled to land on the same `content_path` (all three cases), so this is a
  confirmation, not a discovery.
* ⛔ **Nothing was uploaded, transmitted, or logged in.** No portal API was touched.

---

# TERMINAL AUDIT — 2026-08-19. Part A ran as the owner-designed fan-out: ten adversarial verifiers, refute-by-default.

Full record with per-verdict evidence: `reports/99_TERMINAL_AUDIT.md`. This
entry is the findings-format summary. **Verdict: UPLOAD — the tree run B
validated is fit to ship as it stands. Convergence: clause 3 (the cap), stated
as such — we stopped counting, not because there was nothing left.**
The verdict awaits `99b_VERDICT_REVIEW_fable.md` before it is acted on.

| # | finding | severity | route | disposition |
|---|---|---|---|---|
| TA-1 | ⛔ L1-F3 is REFUTED: `Done` is a CombineMethods entry (`PropertyObject.lua:1664`, `procall_parents_last`) — the F66 reclaim DOES run when a Station dies; the recorded coverage gap is phantom (link 1 never checked the second combining registry) | record | re-derived at Src by the L1 verifier | corrected here; no code was ever changed over it |
| TA-2 | ⛔ The audit brief's queue note "the three colonist-walking fixes need no change" is REFUTED for `Fix_StaleReservations:61` — a plain-Lua `OnMsg.NewDay` sweep with no MapForEach; the act-1 measurement never covered it | real, third-party/corrupt-object-gated | read + containment walked by the L5 verifier | REOPENED; queued, checklist 53 |
| TA-3 | ⛔ L8-F4's deference census is REFUTED as stated: `l8_deference_map.py` misses `local orig = Name` captures; ≥4 of 11 global REPLACES rows actually chain; tool prints 67 sites vs recorded 66 | record / instrument | re-run + spot-reads by the L8 verifier | census quarantined — may not be cited until the tool is repaired; the fourth self-flattering instrument this chain has caught |
| TA-4 | ⛔ The console-story correction's mechanism was INVERTED: the retail console IS `ModEnvBlacklist`-governed (`console.lua:45-56` wraps a LuaModEnv); "nil in `_G`" conflated the console env with `_G`; both functions ship gated true in retail `Lua.fpk` (extracted) | record | corrections verifier, mechanism + artifact extraction | re-recorded in the artifact §1; Ged route stands on measurement AND mechanism |
| TA-5 | EF-065 half-refuted: the LoadCode error box is DEAD CODE on this title (`ModsPreGameMenuOpen` never set; `Msg("PreGameMenuOpen")` never raised) ⇒ a file-scope module loss is silent on screen; also `pending`-not-absent nuance; also `content_path` config-invariant | record | L5 + L8 verifiers | EF-065 amended in place |
| TA-6 | L3-F2's charge against `Fix_MeteorFrequency:36-37` is REFUTED — the comment correctly describes the already-written save; link 3 overstated | record | L3 verifier | corrected here |
| TA-7 | Two NEW latent mark-outlives-verdict sites: `ApplyModOptions` re-activation (`00_Core.lua:481-483`, needs `def.optional` — 0 ship) and benign-latch-directly-after-non-benign-latch (no intervening heal) | latent | Part B + L4 verifier | queued, checklist 53 |
| TA-8 | L2-F5's prediction undercounts: a reloaded pre-fix suite shows 3 false FAILs, not 2 (IndependenceTerraforming probe routes a status check) | record | L2 verifier | corrected here; moot post-fix |
| TA-9 | Run B evidence re-verified from primary logs: all log-decidable criteria HOLD; "first packed load ever" narrowed to "first in the B configuration" (the 17:11 setup leg loaded packed 9 min earlier, cleanly); c9's log was scored but never archived | record | run-B verifier, python comparisons | logs absorbed: `runBprep_*`, `runBc9_*`, `sit0817_*` (4 of LR-F12's 7 — the other 3 rotated away); corpus now 80 |
| TA-10 | "66 of 66 unpacked" under-counted the corpus: precise recount = 69 unpacked + 7 sessions with no fix-pack mode line (+ run B packed); operative fact (zero packed before run B) unchanged | record | L7 + run-B verifiers | corrected here |
| TA-11 | ⭐ Part C census: preset-field writes = 9 rows / 6 modules, ZERO cross-module collisions, ZERO mod-invented field names (`tools/audit_preset_fields.py`, selftest 8/8; own instrument defect — rawget-idiom blindness — found and fixed before any count) | positive | terminal audit's own sweep | the surface three lenses named and none swept is now swept |
| TA-12 | ⭐ The question no lens asked: build-version gating. `IsTooNew` is never called on the load path — an older-build player loads the pack engine-ungated, shape-checks-only; and the in-game browser's "only compatible" filter keys on a portal-side `RequiredGameVersion` the upload never sends | real, low reach | re-derived at Src (`Mod.lua:902-906`, `ModManager.lua:224/230/908`) | recorded; check-at-upload item in `RELEASE_PORTAL_PREP.md` §0.5 |
| TA-13 | EF-055's narrowing was unpropagated (STATE only) and carries a bundled variable (same-id vs no-launch-while-absent coincide in all experiments) | record | corrections verifier | fact amended in place, caveat disclosed |
| TA-14 | L5-C1's teardown-window trigger story is refuted (`_fixup.lua` makes the thread map-owned; maps unload before the GameVar flips); the observed error is real, mechanism open | record | L5 verifier | filed as C53 with exactly that status |

**Everything else HOLDS** — links 2, 6, 7 in full (L2's fix earned the
strongest verification in the set, including the cross-fix thrash check the
design accepted as its residual risk; L6-F1's launch-blocking call was correct
and understated; L7 23/23 controls), links 1/3/4/5/8 with the corrections
above, all six chain corrections audited (C-a inverted mechanism aside, all
hold), and both `2f077e8` core fixes survive the hostile re-read — the
clear-on-success provably hides no genuine rot.

**What the terminal audit could NOT reach** mirrors the ledger's closing row:
console platforms · non-English · foreign-mod interleaving (policy) · TestKit
containment/second-load · the 53 wrappers' callers per-site · StaleReservations
per-item guard (reopened) · long-session cost.
