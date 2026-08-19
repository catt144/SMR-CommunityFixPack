# L8 — adversarial / hostile modder: the input surface, the deference census, and who gets blamed

**Link 8 of the pre-launch sweep chain** (`agent/prompts/prelaunch-sweep/`),
2026-08-19. Lens **L8 — adversarial / hostile modder**. ⭐ **The last lens: this
link exhausts the pool of eight.** Configuration: dev tree, unpacked,
source-derived at Src by symbol + shipped source executed under Lua 5.4;
⛔ **no launch** (§8 — and the refusal here is a *scoped ask*, not a decline).

Instruments, both new this link: `tools/l8_hostile_input.py`,
`tools/l8_deference_map.py`. Findings and their routes are in
`SWEEP_FINDINGS.md`; this file is the derivation.

⛔ **No third-party mod was installed.** Baseline protection is standing policy
and the `smr-community-fixes` coverage sweep adjudicated seven leads at source
with that mod never installed. Every foreign-mod result below is **source-derived
by construction** — that is the method, not a limitation this link failed to
overcome. Where a claim genuinely needs a second mod in the process, it is in §7,
not in the findings.

---

## 0 · The question this lens turned out to be about

The brief's L8 block asks *"another mod wraps what we wrap, loads before or after
us — what breaks?"* That framing has an assumption inside it: **that a foreign mod
reaches us through the functions we patch.** It does, and §3 measures it. But it
is not the widest door, and it is not the first one.

⭐ **The pack has a PUBLISHED INPUT SURFACE, and nothing has ever fed it anything
but a well-formed table.** `00_Core.lua:11`/`:15`/`:17` each read a global with
`rawget(_G, "…") or {}`, which is not a defensive idiom — it is a **contract**:
*another mod may create this before we load and we will adopt it.* `README.md:71`
publishes that contract to modders under a "For modders" heading, and `EF-064`'s
route (`ModEnvMeta.__newindex` rawsets into the real `_G` in every branch,
`Mod.lua:1562`) means a foreign mod's write really does arrive.

⇒ **Three globals are an API whose values are supplied by code this project does
not control and has never seen.** A hostile modder does not need to out-think our
wrappers; they need to hand us a value that is not a table. That is §1, it is
where this lens's largest blast radius lives, and it is the question the lens
block did not ask.

⇒ **The second thing the framing hides** is that "wrap" is doing unexamined work.
`00_Core.lua:4-6` states the pack's first design goal as *"fixes prefer
wrapping/chaining originals over replacement, so other mods that hook the same
functions keep working"*, and `README.md:66` publishes it as *"chain rather than
clobber."* That is a claim about all 75 modules. **Nothing has ever counted it**
— §2.

---

## 1 · Census 1 — hostile input to the three public globals

`tools/l8_hostile_input.py` runs the **real shipped source** of `00_Core.lua` and
three real modules under Lua 5.4 (`lupa`), once per seeded value, with the
engine's containment reproduced: **each file executes inside its own `pcall`**,
which is `pdofile` (`lib.lua:242-251`), so a file-scope throw kills exactly that
file and the others still load (`EF-065` (b)).

The three modules are chosen for shape, not convenience: `Fix_DustDevilSpawnGate`
(a global replacement, and the pack's own restore donor), `Fix_MeteorFrequency`
(a `GameVar` owner with an `OnMsg` heal path), `Fix_ExtenderFlapChurn` (the one
module that installs outside apply's pcall).

### 1.0 · The controls, run first, and they are not decoration

| control | result |
|---|---|
| `SMRFixPack_Disabled = { DustDevilSpawnGate = true }` — `README.md:76-77` verbatim | 4/4 files load; **exactly one** module `disabled`; the documented log line `DustDevilSpawnGate: disabled by user/mod setting` |
| nothing set at all — the shipping case | 4/4 files load; **zero** modules vetoed |

⛔ A harness that cannot reproduce the documented behaviour is not evidence about
anything else. Both controls pass, so the rows below are measurements.

### 1.1 · The matrix

| seeded value | why a real person writes it | files lost | registry left as |
|---|---|---|---|
| `SMRFixPack_Disabled = true` | the natural misreading of *"set `SMRFixPack_Disabled` to disable a fix"* | ⛔ **3 of 3 modules** (⇒ **75 of 75** shipped) | 75 ids present, **all `pending`** |
| `SMRFixPack = true` | a mod squatting the namespace, or a crude *"is the pack installed"* flag | ⛔⛔ **4 of 4, including `00_Core` itself** (⇒ **76 of 76**) | nothing exists |
| `SMRFixPack = {}` | a **fork**, a second copy of the pack, or a shim reserving the table | ⛔ **3 of 3** (⇒ **75 of 75**); `00_Core` survives | nothing registered |
| `SMRFixPack_Disabled` with a throwing `__index` | a dynamic veto policy, or simply a buggy proxy table | ⛔ **3 of 3** (⇒ **75 of 75**) | 75 ids, all `pending` |
| `SMRFixPack_Disabled = "DustDevilSpawnGate"` | *"name the fix directly"* | none | ⚠️ **veto silently does nothing** |
| `SMRFixPack_Disabled = {"DustDevilSpawnGate"}` | the **list** form — *"setting a fix's identifier in that table"* reads as a list | none | ⚠️ **veto silently does nothing** |
| `SMRFixPack_Optional = true` | the same misreading on the pack's other published surface | none *(today)* | — |
| `SMRFixPack = {fixes={}, order={}}` | a shim that knows the two documented sub-tables | none | 3/3 registered normally |

### 1.2 · Why the blast radius is the whole pack, and it is structural

`SMRFixPack.Register` is called at **column 0 in all 75 fix files** — measured,
`grep -c "^SMRFixPack\.Register("` returns 75 against 76 total occurrences (the
76th is the `function` definition itself). So `00_Core.lua:446`

```lua
if SMRFixPack_Disabled[id] then          -- ⛔ no type guard
```

executes at **file scope, 75 times.** A non-table value there is not one module's
problem; it is every module's, simultaneously, and by `EF-065` (b) each throw
makes its module **ABSENT** rather than `inactive`.

⭐ **And the pack's own health surface reports nothing true about it.** Register
reaches `:440-443` before it throws, so the id **is** in `fixes` and `order` with
status `pending` — a status no other path in the pack can produce.
`UpdateSuspects` (`:521-541`) tests only `error` and `inactive`, so `pending` is
**not suspect**, the stand-down dialog never fires, and `ListFixes()` prints 75
lines of `[pending]`. The engine is loud (75 collected load errors →
`ModsLoadCodeErrorsMessage`, `Mod.lua:2254-2275`); **we are silent and wrong.**

### 1.3 · ⭐ The guard exists three times in this file and is missing at the two sites that matter

| site | shape | guarded? |
|---|---|---|
| `00_Core.lua:187-188` (`WhenActive`) | `rawget` + `type(disabled) == "table"` | ✅ |
| `00_Core.lua:302-303` (`DataPatch` run) | `rawget` + `type(disabled) == "table"` | ✅ |
| `Fix_DustDevilSpawnGate.lua:333-334` | `rawget` + `type(...) == "table"` | ✅ |
| `Fix_MeteorFrequency.lua:168-169` | `rawget` + `type(...) == "table"` | ✅ |
| ⛔ `00_Core.lua:446` (`Register`) | **bare index** | ❌ |
| ⛔ `00_Core.lua:55` (`OptionEnabled`) | **bare index** | ❌ |

⇒ **This is not an unknown hazard — it is a known one applied everywhere except
the one place that runs 75 times at file scope.** The four guarded sites all run
*inside* a pcall the pack or the engine owns (`WhenActive` under `procall`,
`DataPatch` under its own `pcall`, the two module sites inside wrappers). The two
unguarded sites are the two that run **outside** every pcall the pack owns.
⇒ The guard is present exactly where it is cheapest and absent exactly where it
is load-bearing.

⚠️ `00_Core.lua:55` is currently **unreachable**: `OptionEnabled`'s only caller is
`OnMsg.ApplyModOptions`'s `def.optional` branch (`:467`) and `doccheck` emits
**0 optional-gated files**. It is a latent site, not a live one, and is recorded
as such.

### 1.4 · The two quiet failures are the ones a modder actually hits

`SMRFixPack_Disabled = "DustDevilSpawnGate"` does not throw — Lua strings carry a
metatable, so `("x")["y"]` is `nil`. `{"DustDevilSpawnGate"}` does not throw
either — it is a table, keyed `[1]`, and we look up `["DustDevilSpawnGate"]`.
**Both produce no error, no log line, and no veto.** The modder believes they
turned a fix off; the fix is running. Given `README.md:71`'s wording — *"Setting a
fix's identifier in that global table"* — the list form is a natural reading of
our own sentence.

⚖️ **Severity, stated honestly.** ⛔ **None of §1 is launch-blocking.** Every row
needs a third party (a foreign mod, a fork, or a console line before load) to
supply the value; nothing on a clean install produces one, and the shipping
control is green. This is a **robustness and blast-radius** finding about a
surface we publish, not a defect that fires for a player on their own.

---

## 2 · Census 2 — the DEFERENCE census: does the pack chain, or clobber?

`tools/l8_deference_map.py`, alias-resolved per link 1's rule (five alias forms;
the fifth — a bare `local C = Community` inside apply — was **missing from the
first pass** and is §6's first disclosed instrument defect).

**The one sound direction, and it is why these numbers can be trusted:** if a
module contains **no textual reference anywhere** to the prior value of the symbol
it patches, the patch **cannot** chain — a call-through needs the prior value to
be nameable. The tool therefore emits a **lower bound on replacements** and never
an upper bound on chaining. `reads-prior` is a *candidate* and is read by hand.

```
$ python tools/l8_deference_map.py --selftest
selftest: 11/11 cases pass
```

### 2.1 · The result

| kind | sites | ⛔ REPLACES (cannot chain) | reads-prior |
|---|---|---|---|
| global function | 16 | **11 (69%)** | 5 |
| class method | 50 | **13 (26%)** | 37 |
| table slot | 1 | — | *(reclassified, §6)* |
| **total patch sites** | **66** | ⛔ **24 (36%)** | 42 |

**The 11 global replacements:** `TriggerCaveIn` · `PlanetaryAsteroidVisitPossible`
· `WaitBombard` · `GetRareTraitChance` · `GetGridGlobalStorage` ·
`LandscapeForEachUnit` · `CompleteMilestone` · `IsLRTransportAvailable` ·
`FindTransportationModeToCommunity` · `ExpandTrackFromElement` ·
`SetLightTrapMode`.

**The 13 method replacements:** `Dome.RefreshFreeLivingSpaces` ·
`Community.UICommandCenterStatUpdate` · `UniversalRocketBase.CreateAutoCargoRequest`
· `ResourceTracking.GatheredResourcesOnHourlyUpdate` ·
`CargoTransporterNew.UpdateCargoResourceRequests` · `HolidayRating.RewardApplicants`
· `Colonist.UpdateSatisfaction` · `TrackConnectedObjBase.CreateConnectorElements` ·
`TrackBase.GetRefundResources` · `TrackGridElement.DemolishAndSplitTrack` ·
`Train.UnloadAll` · `City.GetNeededSpecialist` · `Colonist.TryToEmigrateToDome`.

### 2.2 · ⚖️ What this is, and — carefully — what it is not

⛔ **It is not a policy violation.** `FIX_POLICY` §1.5 *sanctions* full
replacement (*"only when the defect is mid-function and unhookable"*) and names
this exact consequence itself: *"These are the fixes most likely to clash with
other mods."* Every replacement sampled carries the §1.5-mandated header naming
its Src file and lines (`Fix_DomeOverviewHighlight.lua:14`,
`Fix_ShuttleTransportCache.lua:20`, and the six others read). ⇒ **The
"accidental clobber" hypothesis is refuted, not merely unobserved.** These are
deliberate, documented, classified decisions.

⭐ **What it is: §1.5 sets a budget — *"keep the list short"* — and nobody has
ever emitted the number.** 24 of 66, and 11 of 16 globals, is the first count
this project has of its own clobber surface. A rule with a soft bound and no
measurement is a rule that cannot be checked, which is the same shape as L6's
*"a guard is a claim too."*

⚠️ **And the published wording describes the preference as the practice.**
`README.md:66` — *"chain rather than clobber"* — and `00_Core.lua:4-6` — *"so
other mods that hook the same functions keep working"* — are both stated flat.
The second is the load-bearing one: it asserts an **outcome for other mods**, and
that outcome holds for 42 sites and does not hold for 24. ⇒ **owner-shaped
wording item, routed to the checklist, not edited here.**

### 2.3 · What a replacement does to a foreign mod, precisely

`EF-054` records the owner's design intent: load first, be innermost, *"a mod
that REPLACES the function outright simply wins — our fix vanishes cleanly, which
is the correct outcome."* ⭐ **That symmetry only exists for the 42 chaining
sites.** At the 24 replacements the same event runs the other way: if the player's
enable order puts us **after** a foreign mod that patched the same symbol, our
body-copy overwrites theirs with **no call-through, no log line and no residue** —
their fix is gone and nothing anywhere records that it was. And inter-mod order is
the player's enable order, which appends on enable (`ModManager.lua:36`) and which
no mod can declare, request or detect (`EF-054`). ⇒ **the position that makes the
intent true is not ours to hold.**

---

## 3 · The restore discipline link 1 assigned here — and the benchmark is half right

Link 1 nominated `Fix_DustDevilSpawnGate:250-258` as the pack's correct
save/restore shape and left the sweep of the rest to this lens. The sweep:
**exactly two** of the 16 global replacements have any restore path at all
(`grep -rn "_G\.[A-Za-z_]* *="` over `Code/` returns 4 lines in 2 files), and
both use the same helper:

```lua
local function set_installed(want)
    if not orig then return end
    local cur = rawget(_G, "OverrideDisasterDescriptor")
    if want and cur ~= wrapper then
        _G.OverrideDisasterDescriptor = wrapper      -- ⛔ the re-install
    elseif not want and cur == wrapper then
        _G.OverrideDisasterDescriptor = orig         -- ✅ the polite restore
    end
end
```
(`Fix_DustDevilSpawnGate.lua:250-258`; `Fix_DustDevilsDescrMap.lua:73-81` is the
same shape on `GetDustDevilsDescr`.)

### 3.1 · ⭐⭐ The restore is polite. The RE-INSTALL is not — and it fires on every cold boot

The `not want` branch is exactly the discipline link 1 praised: re-read the live
value, and **only** swap back if it is still ours, so a replacement installed
after us is left alone.

⛔ **The `want` branch has no such check.** `cur ~= wrapper` is not a safety test
— it is a *"has our wrapper been displaced"* test, and its answer is **"then put
ours back."** Whatever `cur` held is overwritten, **never captured** (`orig` still
holds the pre-us value), and nothing is logged.

**And this is not an exotic path.** `set_installed(true)` is called from the
`DataPatch` pass (`:307`), which the shared runner fires on `ClassesBuilt` /
`DataLoaded` / `ModsReloaded` / `DataChanged` (`00_Core.lua:334-354`). Traced on
an ordinary cold boot:

```
ModsLoadCode()          -- every mod's file scope, in the player's enable order
  ...our apply installs `wrapper`
  ...a foreign mod enabled AFTER us installs its own function  <- we are displaced
Msg("ClassesBuilt")     -- presets still empty -> pass returns early
Msg("DataLoaded")       -- presets up -> pass runs -> set_installed(true)
                        --   cur = foreign fn ~= wrapper  =>  OVERWRITTEN, silently
```

⇒ ⭐ **The module the chain has been holding up since link 1 as the correct
save/restore discipline defeats a foreign mod on the ordinary startup path, and
it is the only shape in the pack that can.** The other 14 global replacements
install once and never touch the name again — which is *why* they cannot do this.
The two modules that gained a re-install path to be robust against **their own**
latch/heal cycle gained, with it, the only mechanism in the pack that
un-does someone else's patch after they installed it.

⚖️ **Blast radius: 2 globals** (`OverrideDisasterDescriptor`,
`GetDustDevilsDescr`), both dust-devil surfaces. ⛔ **Not launch-blocking** — it
needs a foreign mod patching one of those two names. It is recorded because it
**inverts a benchmark this chain has carried for seven links** and because it
contradicts `EF-054`'s stated design intent on the one path where the pack can
contradict it.

---

## 4 · `EF-058` — the flattened-class trap does NOT bite the pack, and the reason is a timing one

`EF-058` is unqualified in its own summary — *"⛔⛔ THE FLATTENED-CLASS TRAP BITES
METHOD WRAPPERS TOO"* — and it has bitten this project four times, so it is named
in this lens's block as a known shape. Whether the pack's 50 method patches are
exposed comes down to one thing, and it was **re-derived at Src this session
rather than inherited**:

| step | Src | when |
|---|---|---|
| mod code executes (`ModDef:LoadCode` → every `Code/*.lua`) | `autorun.lua:423` — a **direct call** to `ModsLoadCode()` | ① |
| classes are built and flattened | `classes.lua`'s `function OnMsg.Autorun()`, whose own header says *"class tables for which `hierarchy_cache` is true are 'flattened', containing directly the inherited values from all parents… This isn't done for all classes to save memory"* | ② |

`Msg("Autorun")` is posted after the `autorun.lua:423` block, so ① strictly
precedes ②.

⇒ ⭐ **Every one of the pack's 50 method patches is installed BEFORE flattening**
— all of them run either at file scope or inside `apply`, which `Register` calls
synchronously at file scope (§1.2's 75/75 column-0 measurement). **Flattening
therefore copies OUR function down into the subclasses, not vanilla's.** The trap
is keyed on *install time relative to `Msg("Autorun")`*, and the pack is on the
safe side of it by construction.

⇒ **`EF-058` is amended in place** with that scope clause (a record correction,
which spec §4's 2026-08-19 clarification permits). ⛔ The amendment does **not**
weaken it: the four bites were all *runtime-installed instruments* — a log wrapper
installed mid-session from a probe or the console — and for those the trap is
exactly as live as the fact says.

⚠️ **What this does NOT close, and it is L8's own limit.** Link 1's **C1** check —
for every `Parent:Method` we patch, which subclasses declare their own override
and therefore never see our repair — was run against `ModTools\Src` (4,446 files).
⛔ **A foreign mod's subclass is not in that tree and is structurally invisible to
that check.** The inheritance-shadow result is complete against vanilla and
unbounded against foreign mods. §7.

---

## 5 · Whose fault does it look like? — two surfaces, and both point at us

### 5.1 · The engine's mod-flag box: a substring match on the call stack

Re-derived at Src this session (`CommonLua/Classes/Mod.lua:3001-3015`), not cited
from `EF-065`:

```lua
-- inform the player about a problematic mod (rough estimation based on call stack)
function OnMsg.OnLuaError(err, stack, os_paths)
    for _, mod in ipairs(ModsLoaded) do
        local path = mod.content_path
        ...
        if string.find_lower(err, path) or string.find_lower(stack, path) then
            ReportModLuaError(mod, err, stack)
        end
    end
end
```

⭐ **The engine's own comment calls it a "rough estimation."** Three consequences
this lens needs and no previous link has drawn:

1. ⛔ **It flags every mod on the stack, not the mod that threw.** The 42 chaining
   wrappers are *designed* to sit on the stack of the function they wrap. If a
   foreign mod loaded **before** us, our wrapper called theirs, so when theirs
   throws **our path is in the stack** and the box names us. We did nothing wrong
   and there is no surface anywhere that says so.
2. **The message is built as a LIST.** `mods_str = table.concat(mods, "\n")` under
   `T(796336029093, "Mod Flagged")` (`:2981-2992`) — so the box is designed to name
   several mods at once, **with no ordering, no blame and no way for the player to
   tell which one threw.** `EF-065` describes the single-mod rendering; the
   multi-mod one is the case this lens actually produces.
3. ⚠️ **The more we chain, the more of the game's call tree carries our name.**
   That is the price of §2's 42 good citizens, and it is worth stating plainly
   because it runs against the intuition that chaining is strictly safer.

⛔ **Not actionable pre-launch** — it is the engine's behaviour, we have no call
site in it, and `config.DisableErrorReporting` is its only switch. Recorded so
that a wild report of *"the fix pack broke my game"* is read correctly.

### 5.2 · Our own stand-down dialog blames the game for a foreign mod's action

`SMRFixPack.Require`'s shape checks — `{global=…}` → `type(v) == "function"`,
`{class=…, method=…}` → `type(C[m]) == "function"`, `{path=…}` — fail with
`"<name> not found (game update changed it?)"` and set `entry.update_suspect`
(`00_Core.lua:157-163`). `UpdateSuspects` then feeds the pregame dialog, whose
text is:

> *"…found that the game code they patch has changed — usually after a game
> update — and switched themselves off for safety… if the game was recently
> updated, check for a new version of the Relaunched Fix Pack."*

Counted over `Code/`: **113 `global=` + 106 `class=` + 19 `path=` = 238 shape
checks, against 7 `test=` content checks**, in 69 modules.

⇒ ⛔ **A foreign mod that removes, renames or nils a symbol we depend on produces
a player-facing box blaming a game update and sending the player to look for a
fix-pack version that will not exist.** 238 of 245 checks can reach that sentence;
the 7 `test` entries deliberately cannot (`:160-162`, *"a content check owns its
own meaning"*), which is correct design.

⭐ **A negative that cuts the other way and is worth inheriting:** a foreign
*wrapper* does **not** trip any of the 238, because wrapping preserves the type.
⇒ The pack is blind to being wrapped — no false stand-down — and only a
**destructive** foreign action reaches the dialog.

⚠️ **L4 already found this sentence dishonest** for a different cause (it covers
`status == "error"`, so a crash of *ours* is announced as a game update). This is
a **third** cause of the same sentence, from a direction L4's lens could not see.
Recorded as a third input to a wording decision already open, ⛔ not as a new
defect and not as a rediscovery.

---

## 6 · ⛔ My own instruments were wrong three times — disclosed before any count above

Per the house standard. All three were fixed **before** any number in this file
was taken, and each has a selftest case that now fails without the fix.

1. ⛔ **`function C:Idle()` scored as a chaining wrapper.** The "does the file
   reference the prior value" test used a call-shaped pattern `C[.:]Idle(`, which
   the **install site itself** matches. Left in, it would have scored **every**
   replacement as chaining — i.e. it would have inverted §2 completely. Caught by
   the selftest case written for exactly that shape, before the first real run.
2. ⛔ **`function OnMsg.PostLoadGame()` counted as a method patch.** An `OnMsg`
   registration is **additive** (`cthreads.lua:6`'s `__newindex` appends), not a
   patch of anything. Six message handlers were scored as full replacements and
   inflated the headline count from 24 to 30.
3. ⛔ **A fifth alias form was missing.** Several modules alias by a bare global
   read inside apply (`local C = Community`, `Fix_DomeOverviewHighlight.lua:25`),
   which the first pass could not resolve — it printed unresolved holders
   (`C.UICommandCenterStatUpdate`) that cannot be joined across files. **That is
   link 1's exact failure, reproduced here**, and it is why the lens notes put
   alias resolution first.

⚠️ **One limit KEPT and disclosed rather than closed:** the `C.M = expr` shape
cannot distinguish a method install from a **data-field write on an aliased
table**. It produced exactly one hit —
`Fix_MeteorStormWedge.lua:197`, `flags.DisasterMeteorStorm = nil`, which is a
prediction flag being cleared, not a patch — read at its lines and reclassified
out of the method total (51 → 50). One hit, adjudicated, not silently dropped.

---

## 7 · ⛔ What this link did NOT reach

Territory, not findings — the canonical list is the ledger row.

1. ⛔ **No foreign mod exists in any measurement.** Every §2–§5 verdict is
   source-derived; installing one is barred by standing baseline policy and the
   whole lens is built to work without it. **The veto route, the wrapper
   interleave and the mod-flag box have never been exercised by an actual second
   mod that is not ours.**
2. ⛔ **The one available second mod is not loadable right now.** The opt-in pack
   wraps two of the same methods we wrap (`UniversalRocketBase:GetFuelResourceRequest`,
   `Drone:CleanUnreachables`, `EF-054`) and is the **only** foreign-wrapper
   observation this project can make. Its junction is present but it is disabled
   in account state and needs an **owner Mod-Manager tick** (`H-08`, checklist 43).
   ⇒ **Asked, not assumed** — §8.
3. ⛔ **`ReportModLuaError`'s batching is underived.** Whether the multi-mod case
   renders **one box listing several mods** or **one box per mod** depends on
   `CreateRealTimeThread`'s start semantics (does the thread body run to its first
   yield synchronously?), and `CreateRealTimeThread` is **not defined in
   `cthreads.lua`** — it is a C export. Neither box has ever been rendered
   (`EF-065`: 0 occurrences in 73 logs), so the wording as seen is unobserved
   either way.
4. ⛔ **Link 1's C1 inheritance-shadow check cannot see a foreign subclass** (§4).
   Complete against 4,446 Src files, unbounded against mods.
5. ⛔ **`SMRFixPack_Optional`'s unguarded index is latent, not live** — 0
   optional-gated files today, so §1.3's second row has no current caller and was
   not exercised even in simulation.
6. ⛔ **The hostile-input results are Lua-semantic, taken under `lupa` 5.4, not in
   the retail engine.** They are the strongest form available (real shipped
   source, real containment shape, controls green), and they are still not a
   retail observation.
7. ⛔ **Preset-FIELD patches are unswept from this lens too.** L1 left the preset
   half non-mechanical, L6 left it unswept for dead targets, and the adversarial
   question — *does a later mod's preset edit overwrite ours, or ours theirs* — is
   a third lens asking about the same surface and getting no further. ⭐ **This is
   now the largest unswept CODE surface in the whole chain** (§9).
8. ⛔ **Warm-save territory entirely** — no save opened; the adversarial questions
   about a save written with a foreign mod present and loaded without it (or the
   reverse) were not touched.
9. ⛔ **TestKit tree**: swept for namespace by L7 only; its own containment and
   second-load behaviour are unswept after eight links.
10. ⛔ **Packed install, TestKit-off, junction-pulled — run B, the gate, still
    unrun**, and no packed build exists on disk.

---

## 8 · ⛔ The launch obligation (spec §6.5) — an ASK, not a refusal

**Links 5, 6 and 7 all refused, each for the same structural reason. This link
does not repeat that, because its answer is different.**

⭐ **There IS a launch worth taking for this lens, and I can name it exactly.**
The opt-in pack is a real second mod that wraps two of the same methods we wrap.
A leg with **both packs loaded** would be the only observation this project can
ever make of two independently-authored wrappers on one method in a live process —
the direct falsifier for §2.3 and §3.1, and the only evidence that any part of
this lens could ever have that is not source-derived.

⛔ **It is blocked on a cost that is not mine to spend.** The opt-in is disabled
in account state; restoring the folder does **not** buy the enable back
(`EF-055`), and recovery is an **owner Mod-Manager tick plus a restart**, never an
agent's (`H-08`). Spending it unattended is exactly the hazard H-08 exists to
forbid.

⇒ **So this link asks instead of declaring** — the ask is on
`docs/PLAYTEST_CHECKLIST.md`, scoped to one tick and one unattended leg, with the
two method names and the two predictions written down in advance. ⚖️ That is the
distinction §6.5 was created to force: *"turn a silent default into a declared
decision."* A gap that is **asked, costed and scheduled** is closed as far as an
agent can close it.

⚠️ **What I did NOT do, and why:** take another run-A leg. Fix pack + TestKit with
the opt-in absent is the configuration the 08-19 verification launch already ran
**three times**. For L8 it contains exactly zero foreign wrappers, so it would
re-confirm 75 registrations and measure **nothing this lens asks**. An honest ask
beats a launch that measures a different question.

---

## 9 · ⭐⭐ The last-lens duty: what the ledger says is left, across all eight rows

⛔ **This section rules on nothing.** Convergence is the terminal audit's call.
What it owes the audit is the one input the audit cannot get from any single row:
**a straight answer, read across all eight `NOT reached` columns, on whether
unswept territory of consequence remains.**

### 9.1 · The answer is YES, and it is not close

Eight lenses are used and the lens pool is exhausted. **The territory is not.**
Reading every `NOT reached` cell in `SWEEP_LEDGER.md`, the residue sorts into
three buckets, and only the third is small:

**A · Configurations nothing has ever entered** *(the largest, and it is not a
lens problem — no lens can reach it)*
- ⛔⛔ **Run B — packed install, TestKit off, junction pulled — has NEVER run**,
  and it is **the** release gate by owner ruling. It appears in the `NOT reached`
  column of rows 3, 5, 6, 7, the interlude **and** this one. **No packed build of
  this mod exists on disk anywhere** — stage 2 packaging is outstanding work, not
  merely unverified — and `CheckModPackSignature` was never read, so whether the
  packed branch is even taken on this rig is open.
- ⛔ **Warm-save territory, entire.** In eight links and four launches **no save
  has ever been opened.** The aggregate save footprint is censused but never
  weighed; the uninstall was derived and never walked; the **reinstall** route
  (uninstall → play → save → reinstall) has never been exercised **by anything in
  this project**, and Paradox Mods replaces the folder on update, so it is a real
  player action.
- ⛔ **No console platform, ever. No non-English run, ever.** `FIX_POLICY` §7
  makes the stand-down dialog the *only* player-facing surface on console, and
  that dialog **has never executed in any archived session**.

**B · Code surfaces a lens flagged and no lens swept** *(small, specific, and the
one place another link could still pay)*
- ⛔ **Preset-FIELD patches.** L1 left them non-mechanical, L6 left them unswept
  for dead targets, L8 leaves them unswept for foreign contention. ⭐ **Three
  lenses have now named the same surface and none has swept it** — that is the
  clearest signal in the ledger, and it is the only unswept *code* surface with
  three independent nominations.
- ⛔ **The 53 method wrappers were never traced to their callers individually**
  (L5's own #1 re-take item; a concrete ~53-row job).
- ⛔ **13 of the 18 load-time passes were never cross-read against the game's 237
  shipped `SavegameFixups`** (L3's #1; the hazard is documented and bit
  `90_SaveSanitizer` once already).
- ⛔ **The TestKit**: swept for namespace only, after being excluded six times. Its
  own containment and second-load behaviour are unswept, and it is the one
  component **measured** to emit `[LUA ERROR]` lines of its own.

**C · Questions that need a capability the spec bars** *(deliberately parked)*
- the runtime `_G` enumeration (L7's #1 — needs a console line or a 97th probe,
  both barred; **parked post-launch on purpose**);
- a second Lua load in one process (four separate open questions need it);
- a real foreign mod (this link — barred by baseline policy by design).

### 9.2 · What the audit should weigh, stated as evidence and not as a verdict

- ⭐ **The lens rotation kept paying to the last link.** Link 6 found a launch
  blocker, link 7 found a release-gate criterion that could not fail, and link 8
  found an input surface with a 75-file blast radius and a restore benchmark that
  is half wrong. ⛔ **No link returned only cosmetic findings, including this one.**
- ⚠️ **The refusals converged, and that is the real signal.** Links 5, 6 and 7 each
  declined a launch for structurally the same reason — the remaining questions
  need an instrument, a console, or the terminal gate. Link 8 declines for a
  *different* reason (an owner-owned cost) and asks. ⇒ **What the source can
  answer is close to exhausted; what a configuration can answer is barely
  started.**
- ⛔ **The stopping-rule arithmetic, laid out without choosing:** clause 1 requires
  *"the ledger shows no unswept area of consequence remaining"* — §9.1 A and B are
  the direct evidence on that clause. Clause 2 requires **two consecutive links
  returning only cosmetic findings** — neither link 7 nor link 8 did. Clause 3 is
  the cap, and **the spec itself says clause 3 is not convergence.**
- ⇒ ⛔ **The one outcome the spec names as the worst this design can produce — "a
  chain that stops on the cap and gets written up as convergence" — is the outcome
  the facts above make available.** Naming it is this link's last duty; choosing
  is not.
