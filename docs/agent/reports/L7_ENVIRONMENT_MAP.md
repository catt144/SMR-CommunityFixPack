# L7 — environment & namespace: the global map, taken from the compiler

**Link 7 of the pre-launch sweep chain** (`agent/prompts/prelaunch-sweep/`),
2026-08-19. Lens **L7 — environment & namespace**. Configuration: dev tree,
unpacked, source-derived at Src by symbol + all 76 archived retail logs;
⛔ **no launch** (refusal reasoned, §7).

Instruments: `tools/l7_env_map.py` (new, this link). Findings and their routes
are in `SWEEP_FINDINGS.md`; this file is the derivation.

---

## 0 · The question this lens turned out to be about

The brief's L7 block opens *"enumerate every global the pack creates or writes"*
and expects three names. Every census this project has ever run has been a
**regex over source text**, and a regex is structurally unable to answer this
particular question — because whether `x = 1` is a global or a local is decided
by **scope**, not by shape. The same eight characters are a local write inside
`local x` and a global write outside it. Link 6's own extractors were wrong
three times in one sitting on strictly easier questions, and one of those errors
would have inverted a verdict.

⭐ **So this link did not ask a pattern. It asked the compiler.** In Lua 5.2+
every global access compiles to an indexed access on the `_ENV` upvalue, which
puts the answer in the bytecode with no ambiguity at all:

```
SETTABUP A B C   -- UpValue[A][RK(B)] := RK(C)   ... A names _ENV  =>  global WRITE
GETTABUP A B C   -- R(A) := UpValue[B][RK(C)]    ... B names _ENV  =>  global READ
```

`tools/l7_env_map.py` compiles each shipped file with Lua 5.3 (`lupa.lua53`),
dumps the prototype tree unstripped, parses it, and emits every global read and
write with `file:line`. Shadowing, nested closures, method definitions,
for-loop variables, parameters and `local _ENV` rebinding are handled **by the
compiler**, not by the tool.

### 0.1 · The control, run before any number below was taken

`--selftest` is a battery of 23 snippets whose correct answer is written out by
hand, including every shape that would fool a regex: `local x x = 1`,
`do local z = 1 end z = 2`, `local x = 1 do local x = 2 x = 3 end x = 4`,
`function Cls:m() self.x = 1 end`, `OnMsg.Ready = function() end`,
`local _ENV = {} w = 1`, and a global created inside a `pcall`'d closure.

```
$ python tools/l7_env_map.py --selftest
selftest: 23/23 cases pass
```

⛔ **The battery is not decoration.** A harness that cannot reproduce known
answers is not evidence about the pack.

### 0.2 · What the instrument structurally CANNOT see — disclosed, then closed

The bytecode census sees `NAME = value`. It does **not** see three other routes
by which this pack reaches the real `_G`, so each was enumerated separately and
is folded into every total below:

| route | why bytecode misses it | sites | closed by |
|---|---|---|---|
| `SMRFixPack.SetGlobal(name, v)` | the write executes at `00_Core.lua:173` as `_G[name] = v` — a `SETTABLE` on the `_G` value, and the *name* is an argument | **13** call sites | `grep -rn "SetGlobal(" Code/`, each name read at its line |
| `_G[expr] = v` directly | same shape, no helper | **2** (`00_Core.lua:173`, `Fix_FirstAsteroidPrefabs.lua:130`) | `grep -rn "_G\[" Code/` |
| `GameVar("name", …)` | the global is created inside **engine** code (`lib.lua:1040-1055`), not ours | **2** (one alias-resolved: `GameVar(FLAG, false)`, `FLAG` a file-local) | `grep -rn "GameVar(\|MapVar(" Code/` |

⚠️ This is L3's *"ask what the census key cannot see"* pointed at my own
instrument, and it is the reason the count of names the pack owns is **5** and
not the **3** the brief expected.

---

## 1 · The mod environment, re-derived at Src this session

Read at `CommonLua/Classes/Mod.lua:1546-1611`, not cited from record:

```lua
ModEnvMeta.__newindex = function(env, key, value)
    if env_blacklist[key] then return end
    if not Loading and PersistableGlobals[key] == nil and rawget(original_G, key) == nil then
        assert(false, "Attempt to create a new global '" .. tostring(key) .. "'", 1)
    end
    rawset(original_G, key, value)
end
```

Three consequences, and the third is the one no previous lens has used:

1. ⛔ **There is no such thing as a mod-private global.** `rawset(original_G, …)`
   runs in **every** branch that is not blacklisted. Every global this pack
   writes is visible to the game, to the console, and to every other mod. An
   "accidental" global is a cross-mod collision, not a private slip.
2. ⛔ **A blacklisted key is dropped SILENTLY on write** and reads back nil
   through `__index` (`:1547`), which returns no value for a blacklisted name.
3. ⭐ **The create-assert is suppressed only while `Loading` is true.** All mod
   code loads inside that window (`autorun.lua:1`/`:423`/`:560`, the `EF-064`
   route link 6 re-derived). ⇒ **A global created at FILE SCOPE is silent; the
   identical slip inside a wrapper body that runs in-game is NOT** — it raises
   the engine's strict-global assert, which by `EF-008` reports and continues and
   then rawsets the name anyway.

⇒ **The census must split writes by WHEN THEY RUN, not by what they look like.**
That question appears never to have been asked here, and it is what §2.2 tests.

---

## 2 · Census 1 — every global the pack creates or writes

`python tools/l7_env_map.py` over all **76** `Code/*.lua` in `metadata.lua`
order: **17** global write sites over **12** names, **1,618** global read sites
over **187** names.

### 2.1 · The five names this pack OWNS

| name | route | where | scope |
|---|---|---|---|
| `SMRFixPack` | bare assignment | `00_Core.lua:23` | chunk |
| `SMRFixPack_Disabled` | bare assignment | `00_Core.lua:11` | chunk |
| `SMRFixPack_Optional` | bare assignment | `00_Core.lua:15` | chunk |
| `SMRFixPack_MeteorLatch` | `GameVar` + write | `Fix_MeteorFrequency.lua:76`, `:184` | nested |
| `SMRFixPack_FirstAsteroidPrefabs` | `GameVar(FLAG,…)` + `_G[FLAG]=` | `Fix_FirstAsteroidPrefabs.lua:115`, `:130` | nested |

⚠️ **The brief expected three and there are five.** The two extra are the
`GameVar`s, both deliberate, both documented in their own module headers, and
both already counted by L3's persisted-state census — they are new only to *this
lens's stated expectation*, which is what needed correcting. ⛔ **No sixth name
exists**: 12 written names minus these 5 leaves 7, all vanilla (§2.2), and the
three indirect routes of §0.2 add no further name of ours.

### 2.2 · ⭐ Can any write trip the create-assert? — the new question, and it is a clean NO

The 8 vanilla names written by bare assignment are all written from **nested**
scope, i.e. potentially after `Loading` goes false. For each, the assert fires
only if **both** `PersistableGlobals[key] == nil` **and** the name is currently
nil in the real `_G`. Every one was looked up at its Src declaration:

| name written | Src declaration | assert possible? |
|---|---|---|
| `g_MeteorStorm` | `GameVar("g_MeteorStorm", false)` — `Lua/Meteors.lua:38` | ⛔ no — in `PersistableGlobals` |
| `g_MeteorStormStop` | `GameVar(…)` — `Lua/Meteors.lua:39` | ⛔ no |
| `g_RainDisaster` | `GameVar(…)` — `Lua/MapSettings.lua:125` | ⛔ no |
| `g_TransportationModeToCommunityCache` | `GameVar(…)` — `Lua/Units/Colonist.lua:2478` | ⛔ no |
| `RainsDisasterThreads` | `GameVar("RainsDisasterThreads", {})` — `Lua/TerraformingDisasters.lua:323` | ⛔ no |
| `FindTransportationModeToCommunity` | file-scope global function | ⛔ no — never nil |
| `LandscapeForEachUnit` | file-scope global function | ⛔ no |
| `SetLightTrapMode` | file-scope global function | ⛔ no |

And our own two nested writes are `GameVar`-declared, which puts them in
`PersistableGlobals` *and* rawsets them non-nil at declaration
(`lib.lua:1049-1055`).

⇒ ⭐ **Zero of the pack's global writes can raise the engine's strict-global
assert, on any path, at any time.** This is a re-derivation, not an inheritance:
the five `GameVar` lookups and the `__newindex` body were each read at their
lines this session.

### 2.3 · The sandbox blacklist — clean, and now mechanically clean

`ModEnvBlacklist` extracted from `Mod.lua:1267-1428` (**149** entries) and
crossed against the census:

- **writes ∩ blacklist = ∅.** Nothing the pack assigns is silently dropped.
- **reads ∩ blacklist = `{Msg, OnMsg, _G, rawget}`**, and all four have an
  **own-key override** installed by `LuaModEnv` (`Mod.lua:1600-1607`:
  `env._G = env`, `env.rawget = safe_rawget`, `env.Msg = safe_Msg`,
  `env.OnMsg = safe_OnMsg`). An own key is found before `__index` is consulted,
  so all four resolve. ⛔ No blacklisted name reaches the pack as nil.

This upgrades `EF-006`'s *"the fix pack Code/ uses no blacklisted API
(verified)"* from a hand check to a mechanical one over all 76 files.

### 2.4 · Env-table shadows — none, and the one site that could have made one doesn't

`safe_rawget` (`Mod.lua:1577-1583`) returns the env's **own** key in preference
to the real `_G`. A `rawset(_G, k, v)` from mod code writes only the env table
(`EF-009`), so it would create a shadow: our reads would then diverge from what
every other mod and all game code sees.

The pack has exactly **one** `rawset(_G, …)` site — `Fix_FirstAsteroidPrefabs.lua:129`
— and it writes **`nil`**, i.e. it *clears* a shadow before the real write on the
next line. ⇒ **The pack creates zero env-table shadows.**

### 2.5 · ⚠️ Three global FUNCTION replacements bypass the pack's own verified route

`SMRFixPack.SetGlobal` exists specifically to carry the read-back that
`FIX_POLICY` §1.4b makes mandatory (*"read the name back with `rawget(_G, name)`
in apply() to confirm the write landed — F22 does"*). Thirteen sites use it.
Three replace a vanilla global **function** by bare assignment instead:

| module | line | name |
|---|---|---|
| `Fix_ShuttleTransportCache.lua` | `:52` | `FindTransportationModeToCommunity` |
| `Fix_LandscapeUnitFilter.lua` | `:62` | `LandscapeForEachUnit` |
| `Fix_WispRewards.lua` | `:30` | `SetLightTrapMode` |

⚖️ **Severity, stated honestly and with the condition SAMPLED rather than
assumed.** The only way `__newindex` can fail to land a write is a blacklisted
key, and §2.3 mechanically proves none of the three is blacklisted — so the
failure mode §1.4b guards against is **excluded here**, not merely unobserved.
⇒ This is a **policy-consistency** finding, not a behaviour defect, and it is
⛔ **not launch-blocking.** It is recorded because the pack's own donor pattern
exists and three sites silently sit outside it.

*(The separate question of whether these replacements RESTORE safely when another
mod has replaced them after us — link 1's `Fix_DustDevilSpawnGate:250-258`
benchmark — is explicitly **L8's**, and is left there.)*

---

## 3 · Census 2 — every global the pack READS, tested for existence

⭐ **This is the inverse of L6's dead-code sweep and nobody has run it.** L6
asked *"does anything read what we write?"*. The environment question is the
other way round: *"does anything DEFINE what we read?"* — because a read of an
undefined global hits `ModEnvMeta.__index` (`Mod.lua:1554`), which asserts
`Attempt to use an undefined global 'X'` and returns nil.

**187** distinct read names, crossed against a walk of the whole shipped tree
(**4,446** Src `.lua` files, **10,956** column-0/registrar definitions), then a
second indentation-tolerant pass over the residue — ⛔ **the first pass was
column-0-anchored and under-detected 11 names** (`Presets` at `Dlc.lua:312`,
`empty_table` at `lib.lua:15`, `g_Tutorial`, `weak_keys_meta`, … all indented
inside `if FirstLoad then` blocks), which is disclosed here rather than left in
the total.

**Result: every one of the 187 resolves.** The residue after both passes sorts
into three known-good classes and nothing else:

- **Lua base library** — `type` (238 sites), `ipairs` (82), `tostring` (35),
  `pairs`, `pcall`, `rawget`, `rawset`, `next`, `assert`, `setmetatable`,
  `tonumber`. C-provided, not Lua-defined; my definition patterns cannot see them
  by construction.
- **Engine C exports** — `HexToWorld`, `WorldToHex`, `HexGetDirection`,
  `sincos`, `guim`, `hr`, `ripairs`, `Landscape_ForEachObject`, and
  `GatherTransportableResources`, which `EF-014` already names as *"called but
  defined in neither Src nor the shipped Lua — a genuine engine C export"*.
- **Engine-managed env keys and preset containers** — `CurrentModOptions`
  (rawset per-mod-env by the engine, `EF-004`, and `00_Core.lua:56` reads it by
  plain indexing with that fact cited in its comment) and `TechDef`, a preset
  `GlobalMap` container created at runtime by the preset system
  (`Dlc.lua:315`, `:830`). ⚠️ `TechDef` is read once, at
  `Fix_GeneForging.lua:63`, inside a wrapper gated on
  `colony:IsTechResearched("GeneForging")` — i.e. only in a running colony, long
  after presets exist.

⇒ ⭐ **No name the pack reads is undefined, and no read can raise the engine's
undefined-global assert.**

### 3.1 · The negative that explains why — and it is a design property, not luck

The census shows `Mods`, `GetPreGameMainMenu`, `WaitMessage`, `ModLog`,
`FlushLogFile` and every other possibly-absent name as **not read bare**. They
do not appear in the bare-read set at all, because the pack reaches every one of
them through `rawget(_G, "Name")`. ⇒ **The names that might be absent are
exactly the names the pack never reads bare.** That discipline — visible in
`00_Core.lua:35`, `:66`, `:187`, `:564`, `:571` — is what makes §3's result
structural rather than fortunate.

---

## 4 · Census 3 — the TestKit tree, excluded by all six previous links

Every ledger row from link 1 to link 6 ends with *"TestKit tree excluded"*
(*"a SIXTH time"* by link 6). L7 has the specific reason to break that: the kit
**mutates `_G`**, and ⛔ **every gate reading this project owns was taken with it
loaded.** `tools/l7_env_map.py --tree ../SMR-BugFixPack-TestKit` runs the same
instrument over its **20** files: **7** write sites, **2,062** read sites.

**What the TestKit adds to the real `_G` for a whole session (6 names):**
`SMRTest` · `SMRAutoRun` · `SMRTest_AutoRunEnabled` · `SMRTest_EnablePathLeg` ·
`SMRTest_EnablePathRunning` · `SMRTest_EnablePathSawPackOff`.

**What it changes about vanilla:**

- ⭐ **`ShowStartGamePopup` is neutered outright** for autorun legs
  (`95_AutoRun.lua:265`, `ShowStartGamePopup = function() end`) — an unattended
  session has nobody to close *"Welcome to Mars, Commander!"*. ⇒ **Every
  archived autorun leg ran with a vanilla popup suppressed.** Deliberate,
  headered, dev-only; recorded here because it is a real difference between
  every measurement we own and what a player gets.
- **Three vanilla globals are swapped and restored around specific probes** —
  `MeteorsDisaster` (`90_Loggers.lua:76`, restored `:83`), `RequestAssignUnit`
  and `RequestUnitFulfill` (`91_Stress.lua:366`/`:372`, restored `:383-384`),
  all through the kit's own `set_global`, which refuses to CREATE a name
  (`00_TestCore.lua:228-244`) and is deliberately narrower than the engine's
  guard.

### 4.1 · ⭐⭐ The cross that has never been run, and it is the one run B needs

| question | answer |
|---|---|
| Does the fix pack **read** any global only the TestKit creates? | ⛔ **NONE** |
| Does the fix pack **write** any name the TestKit also writes? | ⛔ **NONE** |
| Does the TestKit **write** any name the fix pack also writes? | ⛔ **NONE** |
| Does the TestKit **read** names the pack replaces? | yes — 10, all read-only probe verification (`CompleteMilestone`, `GetDisasterWarningTime`, `GetRareTraitChance`, `SetLightTrapMode`, `SMRFixPack`, …) |

⇒ ⭐ **The two namespaces are disjoint on writes in both directions, and the
pack depends on nothing the kit provides.**

⚠️ **Scope, stated precisely so it is not over-read.** This is a **static
namespace** result over both shipped trees. It does **not** say run B will pass.
It says one specific failure mode — *the pack silently depending on something
only the instrument supplied* — is **excluded**, and that mode was previously
unmeasured and unexcludable. It is the first evidence of any kind that the
TestKit's `_G` mutation has not been holding the pack up.

---

## 5 · Census 4 — packed vs unpacked, and console platforms

### 5.1 · ⭐ `content_path` is configuration-INVARIANT — closing an inherited open item

Link 5's ledger row left this open: *"`content_path` in the PACKED case was not
compared to the unpacked one, so the engine's mod-flag match may behave
differently in configuration B — the gate."* That matters because `EF-065`'s
player-facing *"Mod-related problem detected … Mod Flagged"* box is keyed on our
`content_path`.

Re-derived at Src: **both branches converge on the same line.**
`Mod.lua:1755` sets `def.content_path = ModContentPath .. def.id .. "/"`, and
`ModContentPath = "Mod/"` is a constant (`Mod.lua:6`). The packed and unpacked
branches (`:1724-1740` / `:1748`) differ only in where the def is *read from*;
`MountContent` (`:857-862`) then mounts either the pack or the folder **at that
same `content_path`**.

⇒ **`content_path` is `"Mod/SMR_CommunityFixPack/"` in both configurations**, so
`ReportModLuaError`'s match behaves identically in run B. ⛔ The open item is
answered by source; it does not need the gate to settle it.

### 5.2 · ⛔⛔ The gate's own criterion 1 could not fail — FIXED THIS LINK

`98_LAUNCH_REHEARSAL.md`'s criterion 1 is **"the mod loads packed"**, and its
evidence column read *"`[CommunityFixPack]` lines exist at all"*.

⛔ **Those lines are equally present when the mod loads UNPACKED.** The
criterion whose whole job is to certify that run B measured the player's
configuration would have scored GREEN on the dev tree.

The engine prints the fact directly:
`ModPrint("once", "Loaded mod def %s (id %s, v%s) %s from %s", …, mod.packed and "packed" or "unpacked", …)`
(`Mod.lua:1849`), off the `def.packed` flag set at `:1734`.

⭐ **MEASURED over `docs/archive/*.log`: 66 sessions carry that line for
`id SMR_CommunityFixPack`, and all 66 say `unpacked from appdata`. `packed` has
never appeared once.** That converts the seed note's *"the mod has never been
loaded packed"* from an assertion into a named, greppable witness — and hands
run B a one-line self-check on its own configuration.

**Fixed in place** (a record, which spec §4's 2026-08-19 clarification permits):
criterion 1 now reads the mode line, and `[CommunityFixPack]` lines existing is
returned to criterion 2, where it belongs.

### 5.3 · ⛔ And the hazard that would produce a false pass — recorded in stage 4

If the junction and a packed folder are **both** present, both defs load and
collide on `new_mods[def.id]`. The tie-break is
`if cmp < 0 or (cmp == 0 and old.packed and not def.packed)` (`Mod.lua:1770`)
⇒ **at equal version the UNPACKED copy wins.** Both are 1.0.0, so an incomplete
junction pull hands run B the dev tree with no warning and no error.

Two free witnesses: the id enters `multiple_sources` and raises
`ModMessage("Mod %s loaded from %s (%s)")` (`:1800`), and criterion 1's mode line
says `unpacked`. ⚠️ The packed/unpacked branches are `if`/`elseif` on **one**
folder (`:1724`/`:1748`), so a single folder is never ambiguous — the hazard is
strictly **two folders carrying one id**. Written into stage 4 step 2.

*(State of the rig as read this session: `AppData/…/Mods/` holds three junctions
— `SMR-BugFixPack`, `SMR-BugFixPack-TestKit`, `SMR-OptInPack`, the last restored
2026-08-19 00:30 and still owing an owner tick per `H-08`. **No packed build of
this mod exists anywhere on disk**, so stage 2 packaging is genuinely
outstanding, not merely unverified.)*

### 5.4 · Console platforms — satisfied by construction

`FIX_POLICY` §7 constrains behaviour on playstation / xbox / windows_store.
The census answers the environment half outright: ⛔ **`Platform` is never read
by any of the 76 files.** The pack contains **no platform-conditional code at
all**, so its Lua behaviour is platform-invariant and §7's *"fail-safe behaviour
must never DEPEND on the player seeing a message"* cannot be violated by a
platform branch, because there are none.

⚠️ Wording, checked not assumed: `README.md:51-52` says *"Steam and other PC
versions"* — correct per §7. `docs/PLAYTEST_HELP.md:26` heads an item
*"Achievements stay ON with mods on PC"* but qualifies it in the same sentence
with *"(they are mod-blocked only on console/MS Store)"* — accurate, and it is
an owner-facing doc, not a player surface. ⇒ **Recorded as loose, not as a
defect**, and not edited.

---

## 6 · ⛔ What this link did NOT reach

Territory, not findings — see the ledger row for the canonical list.

1. ⛔ **Nothing was run in a game — seventh link.** Every result above is
   source-derived or read out of archived logs.
2. ⛔ **The runtime `_G` has never been enumerated.** §2 proves what the pack's
   *source* writes; nobody has ever listed the actual globals present in a live
   process and diffed them against vanilla. That is the direct falsifier for
   §2.1's "no sixth name" and it does not exist.
3. ⛔ **The packed load path is still entirely underived-by-execution.** §5.1
   settles `content_path` at Src; `MountPack`, `def.packed`, reading
   `metadata.lua` from inside the archive, and the `Mod/<id>/` preview path have
   never executed for this mod — measured, 66/66 `unpacked`.
4. ⛔ **`CheckModPackSignature` was not read**, so whether the packed branch is
   even taken on this rig is still the open question stage 4.2 already flags.
5. ⛔ **The TestKit's own second-load / containment behaviour** is still unswept;
   this link swept its **namespace** only.
6. ⛔ **No console platform has been touched** — §5.4 proves the pack does not
   branch on platform, which is a different claim from "it behaves correctly
   there."
7. ⛔ **Whether the engine's `ModEnvMeta` asserts report at all in a RETAIL
   build** is still unmeasured (link 6's item; §2.2 makes it moot for this pack,
   since no write can reach the assert).
8. ⛔ L8 (adversarial / hostile modder) — **entire**, including the restore
   discipline of the 21 vanilla global writes, which link 1 explicitly assigned
   there.

---

## 7 · ⛔ The launch obligation (spec §6.5) — refused, and here is the reasoning

**This is the third consecutive reasoned refusal, and the reason has become
structural rather than incidental — that is itself worth the terminal audit's
attention.**

This lens's open questions are items 2 and 3 of §6. Each needs one of exactly
three capabilities, and the spec bars all three:

| what would answer it | why it is barred |
|---|---|
| enumerate live `_G` from a running game | needs the **console**; unattended sessions cannot type, and `ConsoleExec`/`debug` are blacklisted from mod code (`Mod.lua:1285`) |
| a TestKit probe that dumps `_G` | ⛔ spec §4: the **96-probe count is a player-facing claim** on the store card; a 97th puts a wrong number on a count already corrected twice |
| an instrument in `Code/` | ⛔ spec §4: it contaminates the exact tree under test |
| load the mod **packed** | ⛔ that is **run B**, and spec §6 keeps B terminal — *"it must test the final tree"*. It is not this link's to take, and taking it early would spend the gate on a non-final tree |

⚠️ **A launch was available and would have measured the wrong thing.** I could
have taken another run-A leg on the autorun harness; it would have re-confirmed
75 registrations and told me **nothing about globals**, because no surface in run
A prints `_G`. An honest refusal beats a launch that measures a different
question.

⭐ **What I did instead of launching**, since §6.5's real complaint is links
discharging duty by *declaring* a gap: I took the two measurements that were
available without a launch — the 66-log packed/unpacked witness (§5.2) and the
full TestKit namespace cross (§4.1) — and I fixed the gate criterion that would
have made the eventual launch lie (§5.2). ⇒ **The next launch is better
instrumented than it was before this link, without a launch being taken.**

⚖️ **The pattern the terminal audit should rule on:** links 5, 6 and 7 all
refused, all for the same reason — the chain's remaining questions have
converged on precisely the two capabilities the spec forbids (an instrument, and
the terminal gate). That is not three lazy sessions; it is the sweep having
exhausted what source can answer. ⇒ **The remaining value is concentrated in run
B**, and run B's criteria are therefore worth more scrutiny than another lens.
