# L6 — promise vs behaviour: the five-surface map

**Pre-launch sweep chain, link 6, 2026-08-19.** Lens L6 (`00_CHAIN_SPEC.md` §3).
Extractors: `tools/l6_promise_map.py` (five censuses over the pack) and
`tools/l6_reachability.py` (patch targets vs the whole shipped tree). Every
number below is emitted by one of those two or read at `ModTools\Src` this
session. ⛔ Nothing here is inherited from a prior link's verdict.

⛔ **Configuration:** dev tree, unpacked, source-derived at Src + the 76-log
archive. **No launch this link** — the refusal is reasoned in §7.

---

## 0 · ⛔⛔ LAUNCH-BLOCKING — fixed at once (spec §4's standing exception)

**`items.lua` held 75 `ModItemCode` entries against `metadata.lua`'s 76-entry
`code` list. `Code/Fix_AutomationLawCompensation.lua` had no item.** The module
shipped into `code` with commit `92fe101` (2026-08-15); `items.lua`'s last touch
before this link was `0efb87e`, which predates it.

### The route, re-derived at Src by symbol this session

| step | site | what it does |
|---|---|---|
| ① | `UploadMod` `GedModEditor.lua:772-824` | ⓵ `prepare_fn` → ⓶ `CreatePackageForUpload` → ⓷ `upload_fn`, in that order |
| ② | `Steam_PrepareForUpload` `SteamWorkshop.lua:17-22` | first upload (`steam_id == 0`) calls `mod:SaveWholeMod()` **inside step ⓵** |
| ③ | `ModDef:SaveWholeMod` `Mod.lua:1140-1157` | `self:SaveDef()` with **no argument** ⇒ the `serialize_only` branch is not taken |
| ④ | `ModDef:SaveDef` `Mod.lua:960-993` | `self.version = self.version + 1` (`:967`), then `code_dirty = self:UpdateCode()` (`:973`), then writes `metadata.lua` to `content_path` |
| ⑤ | `ModDef:UpdateCode` `Mod.lua:816-840` | `local code = false`; one entry per **mod ITEM**; `self.code = code`. ⛔ **No disk scan anywhere in it** |
| ⑥ | `ModDef:ForEachModItem` `Mod.lua:716-728` | walks `self.items` by index ⇒ `items.lua` order *is* the resulting load order |
| ⑦ | `ParadoxMods.lua:167-173` | `mod:SaveWholeMod()` **after** the content upload |
| ⑧ | `ValidateModBeforeUpload` `GedModEditor.lua:836-844` | forces the same save on any dirty mod — the *"The mod needs to be saved before uploading"* prompt `RELEASE_PORTAL_PREP.md` §0.5(b) already warns about |

⇒ **Steam would have shipped a `code` list of 75 and the automation-law
compensation fix would never have loaded for a single player.** Paradox's *first*
package escapes only because its save runs after the upload (⑦) — but that save
still rewrites the tree on disk, so `RELEASE_PORTAL_PREP.md` §0.5(c)'s documented
sequence (**Paradox first, Steam second**) means Steam packs from an
already-truncated `code` list, and so does every later update to either portal.
**The only surface that survives untouched is the first Paradox package.**

⚠️ **What makes the cost concrete rather than theoretical:** this is the module
whose probe reads `PASS` in all three of the 2026-08-19 verification legs
(`archive/vl97a/b/c_*`, `75 applied` each, `AutomationLawCompensation: applied`
×3). It is measured working in the dev tree and would have been absent from the
package.

### And the guard for exactly this said PASS

`tools/upload_preflight.py:171` counted `re.findall(r"ModItemCode", …)` over the
**whole file** — which counts the header comment at `items.lua:16` that *explains
the guard*. 75 real entries + 1 comment = 76, against a 76-entry `code` list.
**Two errors cancelling, and the one guard between a missing module and the store
reported a clean pass.**

⚠️ It was wrong in both directions: read-only, the same arithmetic reports a
**phantom** mismatch on the sibling opt-in repo (raw 10 vs `code` 9), whose
`items.lua` is in fact correct — 9 entries, same files, same order.

### Both fixes, and their falsifiers

1. `items.lua` — the missing `ModItemCode`, inserted at metadata's own position.
2. `tools/upload_preflight.py` — parses the entries and compares the **ordered**
   list, because ⑤+⑥ make sequence load-bearing too.

| falsifier, run against the real tree | result |
|---|---|
| re-drop the entry | **FAIL**, exit 1, naming `Code/Fix_AutomationLawCompensation.lua` as the file that would stop loading |
| same set, swapped order | **FAIL**, naming the reorder |
| restored | 20 checked · **0 FAIL** |

---

## 1 · Census 1 — identity: the id a player is told to derive

`README.md:80-83` and the site's `for-modders.md` tell a modder the veto id is
*"the fix file names minus the `Fix_` prefix"*, with `90_SaveSanitizer.lua`
registering `SaveSanitizer`.

**Tested mechanically over all 76 files, resolving the id through file-local
aliases first** (13 modules pass `FIX_ID`, not a literal — a plain grep cannot
join those):

- 76 `Code/*.lua` · **75 register** · 1 does not (`00_Core.lua`, correctly)
- ⭐ **75 of 75 ids match the published rule. Zero mismatches.**
- 3 modules carry no `title = "…"` on the line the extractor reads
  (`CaveInsNoDisasters`, `LowStorageWarning`, `WispRewards` — each supplies it
  another way; a `ListFixes` cosmetic, not a promise defect).

## 2 · Census 2 — package: `code` ↔ `items.lua` ↔ disk

After the §0 fix: **76 = 76 = 76, same files, same order.** Nothing in `code` is
absent from disk; nothing on disk is absent from `code`.

## 3 · Census 3 — the veto route, walked rather than cited

`README.md:71-74`: *"Setting a fix's identifier in that global table **before the
fix pack loads** vetoes the fix — the pack registers it, marks it disabled, and
never applies it."* ⭐ *"You can X" needs a route check* — a citation proving the
mechanism exists is a different check, and the owner has overturned a line three
reviews passed on exactly this.

### 3.1 The three gates `00_Core` actually owns

| gate | site | reads the veto? |
|---|---|---|
| `Register` | `00_Core.lua:446-450` | yes — latches `status = "disabled"` and returns **before** `run_apply` |
| `DataPatch`'s `run()` | `:302-303` | yes — re-reads the table before **every** pass |
| `WhenActive` | `:186-188` | yes — status **and** a live re-read of the table |

### 3.2 Everything that runs OUTSIDE those three

Census over all 76 files, file-scope vs inside the `Register` call (balanced-paren
scan, string- and comment-aware):

| kind | file scope | inside apply |
|---|---|---|
| `OnMsg.X = SMRFixPack.WhenActive(…)` | **19** | 0 |
| `OnMsg.X = <bare>` | 8 (all `00_Core`'s own runners) | 4 |
| `function OnMsg.X()` | **7** | 0 |
| `SMRFixPack.DataPatch(…)` | 13 | 0 |
| `SMRFixPack.OnDataReady(…)` | 2 | 1 |
| class/table method installs | 10 | 49 |
| game-time / real-time threads | 5 / 2 | 2 / 1 |
| `GameVar(…)` | 2 | 0 |

Apply-scope sites are covered by definition — under a veto `apply` never runs.
That leaves the **file-scope** sites, and every one was read:

| site | what stops it under a veto | verdict |
|---|---|---|
| 19 × `WhenActive` handlers | the wrapper itself | ✅ |
| `Fix_ExtenderFlapChurn:81` file-scope wrapper | **first statement** is `if not SMRFixPack.IsActive(…) then return orig(self) end` | ✅ pure pass-through |
| `Fix_CrystalMysteryHang:105` `OnMsg.MysteryEnd` | no check — but its whole body is `stop_repeater()`, which bumps a file-local generation counter that no vetoed module ever started | ✅ vacuous |
| `Fix_IndependenceTerraforming:171` `OnMsg.LoadGame` | `IndependenceTerraformingSweep` opens `if not (entry and entry.status == "active") then return` | ✅ |
| `Fix_MeteorFrequency:157` `OnMsg.NewDay` | `MeteorsWatchdogCheck` opens `if not fix or fix.status ~= "active" then return` | ✅ |
| `Fix_MeteorFrequency:164` `OnMsg.PostLoadGame` | status **and** a `rawget(_G,"SMRFixPack_Disabled")` re-read (`:166-169`) | ✅ the §2 donor shape |
| `Fix_MeteorStormWedge:209` `OnMsg.NewHour` | `StormWedgeCheck:98-99` status gate | ✅ |
| `Fix_MeteorStormWedge:217` `OnMsg.PostLoadGame` | no check — body is a per-save state reset of our own table | ✅ vacuous |
| `Fix_FirstAsteroidPrefabs:237` `OnDataReady` | `if not entry or entry.status == "disabled" then return end` | ✅ names the veto status explicitly |
| `00_Core.lua:462` `OnMsg.ApplyModOptions` | `:469-475` skips `disabled` entries and logs the ignored toggle | ✅ |

⭐ **Verdict: the advertised veto route holds for all 75 modules.** No file-scope
site does work for a vetoed module.

### 3.3 Two exact limits on that promise — scope, not defects

1. ⛔ **`GameVar` declarations are not vetoed.** `Fix_MeteorFrequency:76`
   (`SMRFixPack_MeteorLatch`) and `Fix_FirstAsteroidPrefabs:115` declare their
   persisted var at file scope regardless. A save made with a **fully vetoed**
   pack still carries those two names, initialised and never written. The README
   promises the *fix* will not apply, and it does not — but "vetoed" and "absent"
   are not the same thing in the save, and nothing says so.
2. ⚠️ **Only 1 of the 7 ungated handlers re-reads the veto table itself.**
   `FIX_POLICY` §2 requires **both** the registry status and the table
   (*"the A1 lesson"*); six check status alone. For a **pre-load** veto — the only
   route any surface advertises — `Register` has already latched
   `status = "disabled"`, so the outcome is identical and the promise holds. The
   gap is real only for a **mid-session** veto, which `README.md:83-84` explicitly
   says is not a route. ⇒ A policy-conformance gap with no player-reachable
   consequence today. ⛔ Recorded, not fixed: seven edits to a release candidate
   for zero behaviour change is the wrong trade at link 6.

### 3.4 ⭐ The mod-env question nobody had asked, settled at Src

Does a **foreign** mod's write to `SMRFixPack_Disabled` even reach the table our
env reads? Each mod runs in its own sandbox (`EF-006`), and `CurrentModOptions`
is per-mod-env (`EF-004`), so this is not rhetorical.

`ModEnvMeta`, `Mod.lua:1546-1563`, read this session:

```lua
ModEnvMeta.__index = function(env, key)
    if env_blacklist[key] then return end
    local value = rawget(original_G, key)          -- :1548
    if value ~= nil then return value end
    …
    assert(false, "Attempt to use an undefined global '" … "'", 1)   -- :1553
end

ModEnvMeta.__newindex = function(env, key, value)
    if env_blacklist[key] then return end
    if not Loading and PersistableGlobals[key] == nil
       and rawget(original_G, key) == nil then
        assert(false, "Attempt to create a new global '" … "'", 1)   -- :1560
    end
    rawset(original_G, key, value)                 -- :1562, UNCONDITIONAL
end
```

Three consequences, each load-bearing:

1. ⭐ **`rawset(original_G, …)` runs in every branch**, so a foreign mod's write
   lands in the **real** `_G` whether or not the name existed — and `__index`
   reads back out of the real `_G`. **The route works.** (Same shape as `EF-064`:
   the assert does not stop the line after it.)
2. ⭐ **`ModsLoadCode()` runs at `autorun.lua:423`, between `Loading = true`
   (`:1`) and `Loading = false` (`:560`)** — so *all* mod code, ours and theirs,
   loads with `Loading` truthy and the `__newindex` assert at `:1560` suppressed.
   That is why `00_Core.lua:11`'s own global creation has never produced a log
   line in 74 retail logs.
3. ⛔ **`__index`'s assert at `:1553` has no `Loading` guard** — see §4.

## 4 · The published veto snippet reads a global that does not exist yet

`README.md:75-78` and the site's `for-modders.md:31-34` publish, identically:

```lua
SMRFixPack_Disabled = SMRFixPack_Disabled or {}
SMRFixPack_Disabled["DustDevilSpawnGate"] = true
```

The right-hand `SMRFixPack_Disabled` is a **bare read of a name that by
construction is not in `_G` yet** — that is the whole point of the `or {}`. It
routes through `ModEnvMeta.__index` and falls to the `assert` at `Mod.lua:1553`,
which carries **no `Loading` guard**.

⭐ **The pack's own code never does this.** All four in-code reads use the safe
form — `00_Core.lua:11`, `:187`, `:302`, `Fix_DustDevilSpawnGate:333`,
`Fix_MeteorFrequency:168` — `rawget(_G, "SMRFixPack_Disabled")`, which
`safe_rawget` (`Mod.lua:1577-1583`) resolves out of the real `_G` with no assert.
**The instruction we publish is the one shape our own code is written to avoid.**

⚠️ **Functionally the route still works** (`__index` returns nil after the
assert; `or {}` supplies the table). The cost is a log line — and how loud that
line is depends on the build:

| build | evidence |
|---|---|
| **MarsDebug** | measured: `C43`, `logs/MarsDebug.exe-20260803-23.14.05-6a22b8b3.log:489,504` — the sibling `__newindex` assert printing `[LUA ERROR] Attempt to create a new global`, with the mod's `content_path` in the stack |
| **retail** | ⛔ **UNMEASURED — and the archive is not a control** |

⛔ **The negative I nearly recorded and did not.** `Attempt to create a new
global` appears in **0 of 74 retail logs** and `Attempt to use an undefined
global` in **0 of 76**. That is not evidence: the only code that ever produced
the first line was the TestKit's pre-fix `set_global`, and **every retail log
that touches those probes is already post-fix** (`u2run3`, 2026-08-11, carries
the *refusal* line). ⇒ **The condition was never sampled in retail.** Per the
standing rule, a zero over an unsampled condition refutes nothing.

`autorun.lua:243`'s own comment — *"Platform.asserts is set in all debug builds"*
— makes retail silence the likely reading. **It is a reading, not a measurement.**

⚠️ **And `EF-008` is unqualified about this.** It states flatly that `error()`
and `assert()` in mod code *"REPORT AND CONTINUE"*, with no build qualifier and
no `verified` date, and `FIX_POLICY` §6's first bullet rests on it. The advice
stays right either way — silent failure is worse than reported failure — but the
fact's **scope** is wider than its evidence. Noted in the fact, not reversed.

⚠️ **A second, separate wording point on the same two pages.** `for-modders.md:36-38`
says it *"does not matter whether yours or ours is created first — only that the
values are set before our code runs."* Both halves are true, and together they
require the modder's mod to **load before ours** — which is the player's enable
order, with no priority field and no way to request a position (`EF-054`,
`FIX_POLICY` §8). The pages do not say so. ⚖️ Owner's wording call; routed.

## 5 · Census 4/5 — dead-coded targets, and the fix list

### 5.1 Is F85 the only one?

`tools/l6_reachability.py`: **13 global replacements + 55 class/table members**,
alias-resolved over 75 modules, counted against **4,446** Src files.

- **All 13 globals carry live shipped references.** The four thinnest were read
  at every site *and one level up*: `WaitBombard` → `StartBombard` → Mystery 7's
  generated sequence (`Mystery 7.generated.lua:941`); `RainsDisasterActivation` →
  `RainsDisasterLoop` (`TerraformingDisasters.lua:313`) → `:419`;
  `GetRareTraitChance` → `TraitPreset.lua:748` + `Colonist.lua:3559`;
  `PlanetaryAsteroidVisitPossible` → the generated XDef at `:37`.
- **No member is dead.** The one row reading zero of both kinds
  (`MirrorSphere.max_progress`) is a **field**, read as `self.max_progress`
  (`MirrorSphere.lua:69`) — a shape neither column can see, and already cited in
  the module's own header.

⇒ ⭐ **No second F85 was found among globals and members.** ⛔ That is not "no
dead targets" — see §6.

### 5.2 Three own-instrument defects, each found and fixed before any count above

This lens's extractors were wrong three times, in three different ways, and the
numbers in this report are the post-fix ones:

1. **A call-shaped pattern cannot see a function used as a VALUE.**
   `RainsDisasterActivation` read **zero** uses; it is handed whole to
   `CreateGameTimeThread(RainsDisasterActivation, settings)`. A dead-code sweep
   blind to that is blind to exactly the shape it hunts.
2. **A negative lookahead behind `\s*` is not a negative lookahead.**
   `=\s*(?!SMRFixPack\.WhenActive)` backtracks to zero width and tests at the
   space, so **all 19** `WhenActive` handlers counted as ungated — 27 ungated
   sites where the truth is 7. The veto verdict would have been the opposite one.
3. **A census over raw text counts quotations.** This project's headers reproduce
   the shipped defect verbatim; `Fix_RainsDeadlock:11` is vanilla's own
   `CreateGameTimeThread` line **inside a comment**, counted as our thread.

⭐ And a fourth, disclosed as a **limit** rather than fixed silently: the member
census was blind to **string dispatch**. `Colonist:ExitVehicle` read zero callers
and is reached from `colonist:SetCommand("ExitVehicle", self)`
(`Train.lua:447`) — which `Fix_TrainPlatformWedge:27` had said all along. The
census now counts quoted names in a separate column.

### 5.3 The fix list and the five judgment calls

| claim | surface | check |
|---|---|---|
| "75 fix modules" | `README.md:14` | ✅ `doccheck --emit-counts` |
| "a suite of 96 checks" | `README.md:54` | ✅ same |
| "167 tracked findings" | `README.md:23-24` | ✅ same |
| "**Five** of the fixes are judgment calls … the mod page says which and why" | `metadata.lua` `description` (**ships inside the mod**), `README.md:16-18`, card `:123`, `faq.md:142` | ✅ the fix list carries **exactly five** `judgment call` entries — `fix-list.md:95, 283, 323, 344, 698` — and the card names them |
| the fix list matches the **current** module set | site `content/fix-list.md` | ✅ both 2026-08-15 module-set changes are reflected: the automation-law entry was **added** (`f87e78a`) and the distress-popup entry **removed** (`a8b0995`) when its module left the pack |
| no entry promises a fix that does not work | — | ✅ the site carries **no** entry for `F25` / `Fix_TechDescriptionBuilding`, the one module recorded as a retail no-op (`F98`). The F24/F28 class does not recur. |

### 5.4 ⚠️ `F98`'s headline mechanism is the DEV route; the retail route is one step earlier

⚠️ **Corrected mid-link against the entry itself.** My first reading was that
`F98` had the route wrong. It does not: its **body already carries the retail
measurement** — the probe `SKIP` on `Mars.exe` with reason *"the tech has no
description T"*, against `PASS` on `MarsDebug.exe`, same pack, same day. What is
one-sided is the entry's **`row_status`**, the line that reaches `INDEX.md` and
that a future session reads first.

That line says the no-op is
*"`tech.description = T(841885693955, CORRECTED)` writes back exactly the id that
was already there."* **That assignment never executes in retail.**

`localization.lua:270-272`, read this session:

```lua
if not dev and not Platform.ged and TranslationTable[id] then
    return LocIdToLightUserdata(id)
end
return setmetatable({T, Ttext}, TMeta)
```

⇒ in retail a shipped preset's `description` is **light userdata**, not a table —
which `F98`'s own live control already measured (`type(T(8821,"ZZZ"))` →
`userdata`). The module's guard is `Fix_TechDescriptionBuilding.lua:66`:

```lua
if type(desc) == "table" then … end
if not found then return nil, "description does not carry the literal …" end
```

⇒ **in retail it returns at its own guard, one step before the assignment** —
which is precisely what the entry's own retail `SKIP` reason reported, read from
the other end.

⚠️ **The part neither the row nor the body states, and it is the actionable
part:** `F98`'s queued repair is a `ModItemLocTable` entry, chosen against the
row's stated route. **Any repair that keeps this `type(desc) == "table"` guard is
dead in retail regardless of the loc table** — the guard is false before a new id
is ever reached, so the module would decline exactly as it does now. The
post-release work needs that in writing. Appended to the entry body; nothing
built (record-only, and the owner parked the repair with D10).

## 6 · ⛔ What this link did NOT reach

- ⛔ **Nothing was run in a game — sixth link, and the refusal is reasoned (§7).**
- ⛔ **Preset-FIELD patches are unswept for dead targets.** §5.1 covers globals
  and class/table members. A preset field we write that nothing reads is the same
  defect class, and link 1 left the preset half non-mechanical for the same
  reason. **This is the largest unswept surface in this lens.**
- ⛔ **Whether the engine's `ModEnvMeta` asserts report in a RETAIL build** — §4.
  Settling it needs code that reads an undeclared global, which every route this
  chain leaves open forbids.
- ⛔ **The veto has never been exercised end to end by an actual foreign mod.**
  Every verdict in §3 is source-derived. No second mod setting
  `SMRFixPack_Disabled` has ever existed, and its load position is not
  controllable (`EF-054`).
- ⛔ **`ListFixes()` output has never been observed** — the one surface that
  renders id, status and title together, and the surface the README points a
  modder at. 0 occurrences in the archive.
- ⛔ **The store/portal pages as RENDERED** stay check-at-paste; the site is not
  live, so no published surface has been read by anyone at its destination.
- ⛔ **The other two mods' `items.lua`/`code` agreement** was checked read-only
  and the opt-in is clean; `SMR-CommunitySaveRescue` has **no `items.lua` at
  all**, which `UpdateCode`'s `if not self.items then return end` (`Mod.lua:817`)
  suggests is safe by a different route — ⛔ **not verified, and not this chain's
  repo to touch.** Routed.
- ⛔ **TestKit tree excluded a SIXTH time** (`Code/` only).
- ⛔ **Packed install, TestKit-off, junction-pulled — run B, the gate, still unrun.**
- ⛔ L7 (environment & namespace), L8 (adversarial) — entire. §3.4's mod-env
  reading is L7-adjacent and is left as a finding for L7 to re-derive, not a
  verdict; the load-order half of §4 belongs to L8.

## 7 · ⛔ The launch decision — refused, and here is why

Spec §6.5 obliges a link with *"needs a running game"* items to launch **or** say
why not. This lens accumulated two. Neither is reachable:

1. **The retail-assert question (§4)** needs mod code that *reads an undeclared
   global*. Every route to write that code is barred: `Code/` is record-only and
   under the no-instrument rule; a TestKit probe moves the **96** count that is a
   player-facing claim on the store card (§4 of the spec, and that count has
   already survived two corrections); and an unattended session cannot type at a
   console.
2. **The end-to-end veto test (§3, §6)** needs a *second mod* that does not exist,
   loading *before* ours in an order no one can set (`EF-054`) — on a rig where
   reaching a mod configuration by junction costs that mod's enable and an owner
   Mod-Manager tick to recover (`EF-055`, `H-08`, and the opt-in pack is in that
   state now).

⇒ A launch this link could measure nothing this lens asks. ⚠️ And unlike link 5,
one of my questions **was** already answered by a running game: the module the
§0 blocker would have dropped is measured applying and passing its probe in all
three 2026-08-19 retail legs — so the blocker's cost is evidenced, not argued.
