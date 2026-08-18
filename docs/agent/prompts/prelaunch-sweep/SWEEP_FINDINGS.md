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
