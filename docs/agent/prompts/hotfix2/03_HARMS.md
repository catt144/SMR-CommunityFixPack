# 03 · The applies-today repairs — modules that survive and are wrong right now

Chain: `prompts/hotfix2/README.md` (its binding rules are yours). Runs after 02
(which owns `items.lua`). Independent of 04 — either order.

Three modules. All three **pass their self-check and apply today**, and all three
do something wrong on 1.1.0. That is the F112 shape: a correct 1.0.7 transform
landing on top of a vanilla redesign, silently.

## 0 · Start

`git log --oneline -10` · `git pull` · `ListAgents`. Todo list first, one item
per commit-and-verify unit.

**Read path:** `agent/STATE.md` · `VANILLA_FIX_QA.md` **§0 and Reader A's rows
F-1/F-2/F-3** (the QA pinned these shapes and its reasoning is the checklist you
work to) · `PACK_1_1_0_REVERIFICATION.md` §1a · `agent/FIX_POLICY.md` ·
`docs/PLAYTEST_CHECKLIST.md` items 114, 118 · your inbox (01 gave you the probe
form; use it).

## 1 · F-1 `SaintBlessing` — probe-gate **and** a save re-base

**What is wrong.** 1.1.0's `TraitPreset:AddDomeColonistsModifier` now does the
label lookup itself (`Lua/TraitPreset.lua:86-87`: `local label = (trait == "")
and "Colonist" or GetTraitLabel(trait)` / `if not label then return end`). Our
DataPatch has already rewritten `Saint.modify_trait` from `Religious` to
`TraitReligious`, so vanilla computes `GetTraitLabel("TraitReligious")`, gets
`false` (`Lua/Traits.lua:1325-1328`), and returns without registering anything.
⇒ **with the pack on, no Saint blesses anyone.** With it off, 1.1.0 works.

**Half one — the probe.** In the `DataPatch` pass, after DataLoaded, call the
real `AddDomeColonistsModifier` on a stub unit/dome that captures the label:

- captures `Religious` ⇒ 1.0.7 shape ⇒ **apply**;
- captures `TraitReligious` ⇒ already handled ⇒ **decline**;
- captures nothing, returns nil, or throws ⇒ **decline** (fail closed).

⛔ The third case is not pedantry. `AddDomeColonistsModifier` returns silently
when the stub's `GetPropertyMetadata(modify_property)` is nil
(`TraitPreset.lua:80-84`), so "nothing captured" is UNKNOWN — and reading that
silence as "1.0.7" would reproduce the exact bug you are fixing.

**Half two — the save re-base, and it is the half that is easy to miss.**
1.1.0 ships a one-shot `SavegameFixups.OrphanedDomeColonistsTraitModifiers`
(`Lua/_fixup.lua:2143-2170`) that strips every dome-colonists trait modifier and
rebuilds it through the same function. On any save loaded while the broken pack
was on, **that fixup already ran, with our wrong value, and registered nothing.**
Fixups do not re-run. `label_modifiers` is persisted. Nothing re-applies until
the Saint changes dome.

⛔ And our existing heal (`Fix_SaintBlessing.lua:151-181`) will NOT cover it: it
is keyed on `rebased_from`, which is EMPTY when the pass declines. So the patch
must carry its own one-shot re-base for the 1.1.0 shape — re-apply through
`AddDomeColonistsModifier` for every dome-colonists trait carrier missing its
label entry.

**Control (owner, ~5 min):** a Saint in a dome with Religious colonists shows
"Blessed by a Saint", on a save that was loaded under the broken pack.

## 2 · F-2 `StaleReservations` — ⛔ BLOCKED on the owner

**Do not start this module until the owner has ruled FIX or REMOVE.** If it is
REMOVE, it belongs to a deletion sweep, not here — route it and say so.

**What is wrong if it stays.** 1.1.0 added a legitimate long hold: boarding an
expedition rocket saves `expedition_residence` (`Colonist.lua:5027-5031`) and
reserves it through `Residence:ReserveResidence` (`:5003-5005`), so our
post-wrapper stamps it; the colonist stays valid while away. Our `NewDay` age
branch then cancels a real hold ⇒ **crew back from a long expedition lose their
home.** Lock is 3,600,000 ms (`__const.lua:174-176`); one-way expedition time is
1,440,000–3,000,000 (`Data/POI.lua`).

**The shape, if kept:** skip colonists with `expedition_residence` truthy. One
clause.

⚠️ **State the narrowed premise in the module header, honestly.** 1.1.0 bounds
the ordinary shuttle-wait case F58 was written for at one sol
(`_GameConst.lua:144`, `LRTransport.lua:47-49`, `LRManager.lua:55-57`). What the
sweep still covers is **committed-shuttle limbo and the walk path** — not "F58 is
still shipped". The report's row overstates this and the QA (§0.4) corrects it.

**Control (owner, only if kept):** send an expedition, wait past 5 sols, confirm
the returning crew keep their residence with the pack on.

## 3 · F-3 `ShelterReflex` — delete half (a), keep half (b)

**What is wrong.** The signature changed: `IsSuitable(colonist)` became
`GetScoreFor(colonist)` (`MicroGHabitat.lua:173-175`), and `GetScoreFor` reads
`colonist.traits` itself (`Community.lua:442-445`). Our body hands it
`colonist.traits`; inside, `traits.traits` is nil and `FilterObjectAttributes`
indexes `obj_attributes[attrib]` for every filter key (`Filter.lua:113-121`)
⇒ **a throw on any asteroid habitat with a trait filter.** Default filter is `{}`
(`Community.lua:43`), so it is silent until a player sets one.

**The shape:** delete half (a) — the `IsSuitable` replacement
(`Fix_ShelterReflex.lua:43-47`). **Keep half (b)**; its reads all still exist
(`Colonist.lua:94`, `:3015-3020`, `:2212`, `:2572`, `:2666`;
`__const.lua:1756`).

⚖️ **Why deletion and not repair.** No-life-support is now a deliberate −400
tier, not a missing +100 (`Community.lua:436-437`, `:443`, with help text at
`:437`). `FIX_POLICY` §4 bars fighting a stated design. ⚠️ **Name the cost in
the notes**: dropping (a) returns F73(a)'s blip-eviction to 1.1.0 players.

**Control (owner, ~2 min):** an asteroid habitat with a trait filter set — no
throw.

## 4 · Every module you touch here

- Carries its `SRC:` / `DEFECT:` manifest lines per 01's spec, stamped **after**
  your edit, never before.
- Passes `bodycheck.py` and `sigcheck.py`.
- ⛔ **Declines on 1.0.7** if it gains any 1.1.0 body shape (README, ck118).
  F-1's probe does this for free — a probe that captures `TraitReligious` on
  1.1.0 captures `Religious` on 1.0.7 and correctly applies there. Say so in the
  header rather than leaving it implicit.

## 5 · Scope fence

**In:** `Fix_SaintBlessing.lua`, `Fix_StaleReservations.lua` (if kept),
`Fix_ShelterReflex.lua`, their bug entries, their drafted patch-note lines.
**Out:** `items.lua` and `metadata.lua` (02 and 06 own them); the re-copies (04);
`00_Core.lua` (01); every KEEP and REMOVE module.
Found something out of fence? **File it, do not fix it.**

## 6 · Stop conditions

- F-2 unruled ⇒ skip it, do the other two, say so.
- The F-1 probe cannot be made to fail closed on a stub, or
  `AddDomeColonistsModifier` turns out not to be side-effect-free on one ⇒
  **STOP AND ASK.** Do not ship a probe you cannot bound.
- The F-1 re-base would need to touch saves in a way `FIX_POLICY` does not
  already sanction ⇒ stop and report.
- You find a fourth applies-today harm ⇒ file it, tell 99, do not absorb it.

## 7 · What may NOT be claimed

- ⛔ Not "F-1 is fixed" until the owner's control has been seen. A source-derived
  repair is a claim; the owner's rule of 2026-09-08 binds our own notes too.
- ⛔ Not "saves are healed" — the re-base is untested until a save that loaded
  under the broken pack has been loaded again with the repair on.
- ⛔ Not "F-3 is now correct" — it is now *absent*, and 1.1.0 players get the
  vanilla behaviour, which still evicts on a blip.
- ⛔ No status moves on source reads.

## 8 · Close-out

Green gates. Append your outbox to `04`, `06` and `99` — 99 needs, per module,
what you changed, what the probe decides, and **what has not been exercised in
play**. The three controls above go to the checklist as a batched owner ask
(they fit in one sitting on the existing `BlankBig_02` colony). Strike your
README row, `git rm` this file, commit together, push.

## Notes from upstream

*(From the authoring session, `smr-bugfixpack-91`, 2026-09-08.)*

- ⛔ Read `VANILLA_FIX_QA.md` §0 before the main report's §1a. The QA promoted a
  sixth harm, added the F-1 re-base and the F-5 cleanup, and narrowed F-2's
  premise. The main report says in its own rows that the QA supersedes it.
- The owner's standing rule: **cheats are normal on the playtest saves** — a
  confound only where a reading intersects what they change. Do not ask for a
  clean run for these three controls; none of them touches a cheated quantity.
- ⚠️ Untick the Test Kit's force leg before any attended control if it is armed
  (it was not, per the 17:51 boot log).

### From link 01 — core, tooling and the manifest

⚠️ **For you specifically:** F-1's probe-gate is the first real use of the `probe` form (item 1). Its fail-closed rule is exactly your bug: `AddDomeColonistsModifier` returns silently when the stub's `GetPropertyMetadata` is nil, and "captured nothing" must decline. Stamp the modules you keep with a manifest (item 3) — I deliberately left the FIX set unstamped so you pin AFTER your edit, not before.

*(From link 01, `smr-bugfixpack-25`, 2026-09-08. Commits `6d452a3` probe form ·
`401f8a0` bodycheck.py · `6db7457` FIX_POLICY §2a/§2b · `e2490f3` KEEP set
stamped. ⛔ Nothing was run in a game; no status moved.)*

**1 · The `probe` form — exact signature and semantics** (`00_Core.lua`,
`SMRFixPack.Require`). `{ probe = function() … end, reason = "…" }`, a sibling of
`test`:

* The probe takes **no arguments** and runs under `pcall`.
* **ONLY the literal boolean `true` applies.** A throw, `nil`, `false`, or any
  other value (a captured table included) **declines**. "Captured nothing" is
  UNKNOWN and UNKNOWN is not permission.
* A throw is a DECLINE, never propagated. It is logged as
  `<id>: behaviour probe declined (threw: …)` so an authoring error in the probe
  cannot hide inside a silent decline.
* A probe failure returns `c.reason`, exactly like every other form, and does
  **NOT** set `update_suspect` — it is a behaviour verdict, not patch rot, and on
  the other branch a decline is the CORRECT outcome.
* Write the **stub contract beside it**: a comment naming what the stub must
  provide and why the target is safe to call on one. ⛔ Only for targets you can
  show, from the shipped 1.1.0 body, to be **synchronous and side-effect-free on
  a stub**. If you cannot show both, the module gets no probe and keeps its
  existing check — that is a permitted outcome, not a failure.
* Two shared lines were touched and both are identity for every existing form:
  `local ok, name` → `local ok, name, why`, and the return → `c.reason or why or
  (name .. " not found …")`. No existing reason string was reworded.
* `Require` is a plain function, so a `DataPatch` module may call it from inside
  its pass, after `DataLoaded`, for a preset-bound probe.

**2 · The branch guard, and it is not negotiable** (`FIX_POLICY §2a` — link 04,
this is Job D's answer verbatim). ⛔ **Do not build a game-version detector.** It
would be a LABEL check, against the rule that made the F115 gate correct; and it
is unbuildable anyway, because `lua_revision`, `ModMinLuaRevision` and
`ModRequiredLuaRevision` are ALL 350453 on both branches (`EF-077`) — which is
precisely why nothing warns a 1.0.7 player. There is no field to read. ✅ **The
per-module `probe` IS the branch guard**: a probe confirming the 1.1.0 body shape
a module was written for necessarily declines on a 1.0.7 body, per module, with
no version arithmetic anywhere and nothing global to keep in sync.

**3 · The manifest grammar** (`FIX_POLICY §2b` has the authoring rule;
`tools/bodycheck.py`'s docstring has the machine half). Header-block comments:

```lua
-- SRC: <path> <selector> sha256=<64 hex>      -- or:  -- SRC: none <reason>
-- DEFECT: <python regex>                      -- or:  -- DEFECT@<path>: <regex>
```

* `<path>` slash-separated, relative to `ModTools/Src` (`\` accepted).
* `<selector>`, no spaces: `Class:Method` (separator is a hint — both declaration
  forms and `Class.Method = function(` match), a bare `Name` for a global or
  `local function`, or `L<first>-<last>` for a literal span where there is no
  function to name.
* Body = declaration line → first bare `end` at the same indentation. The
  delimiter is `luafn.py:find_bodies`, **imported** by `bodycheck.py`, so there is
  never a second extractor. Line endings normalised, trailing whitespace stripped
  per line; indentation and comments kept; sha256 of the utf-8.
* `-- DEFECT:` searches the body of the `SRC:` above it. `-- DEFECT@<path>:`
  searches that whole file — the **DataPatch shape**: no body to hash, so declare
  `SRC: none` and state the defect against the shipped DATA.
* Several `SRC:` lines per module are fine; each `DEFECT:` binds to the nearest
  above it. Regexes are Python `re`, ONE line, **not** `re.MULTILINE` (`^`/`$`
  will not do what you want — use `\s+` to cross a line break). Shipped Lua
  indents with **tabs**: write `\s+`, never a literal space.
* ⛔ **State the DEFECT, never the PHRASING.** See item 5.
* ⛔ Never hand-type a hash: `python tools/bodycheck.py --pin <path> <selector>`
  emits the line and the range it hashed.

**4 · `tools/bodycheck.py` — CLI and what its falsifier proved.**

```
python tools/bodycheck.py                 # the pack against the live 1.1.0 tree
python tools/bodycheck.py --src <path>    # another ModTools/Src
python tools/bodycheck.py --code <path>   # another Code/ tree
python tools/bodycheck.py --all           # also print OK / NO-MANIFEST rows
python tools/bodycheck.py --module NAME   # one module
python tools/bodycheck.py --pin <path> <selector>
python tools/bodycheck.py --selftest      # ⛔ the falsifier
```

Exit 1 on `BODY-CHANGED`, `DEFECT-GONE`, `TARGET-ABSENT`, `TARGET-MULTI`,
`MALFORMED`; counts only for `NO-MANIFEST`, `NO-DEFECT`, `SRC-NONE`, `OK`.
⚠️ Deviation from the prompt, stated: `TARGET-ABSENT`, `TARGET-MULTI` and
`MALFORMED` also exit non-zero, not just the two named. A stamped module whose
target vanished, resolves ambiguously, or whose manifest does not parse cannot be
re-verified, and a manifest that merely *looks* like coverage is worse than none.

`--selftest` asserts ten legs, permanently, because a tool that returns GREEN on
everything is indistinguishable from a broken one. **Two legs are real game-side
events**: `DEFECT-GONE` fires on one of the actual 32 (`MinDaysFoodSupply
BeforeNotification` is gone from the whole 1.1.0 tree while
`ResourceTracking:GatheredResourcesOnHourlyUpdate` still exists with our arity —
invisible to `Require` and to `sigcheck`), and `TARGET-ABSENT` fires on
`Colonist:UpdateSatisfaction`, which 1.1.0 deleted. `BODY-CHANGED` fires on a
**real body edit** — F116's in-body repair at `add94b3`, pinning the pre-repair
body against the repaired tree — plus a hash negative control and the converse
leg, so it cannot pass by being always red.
⛔ **ONE HONEST LIMIT, in the file itself:** the 1.0.7 tree is GONE from disk
(`EF-075`), so no true 1.0.7-vs-1.1.0 **game** body pair exists to hash. The
mechanism is proven on a pack-side edit and a negative control, not on a
game-side branch pair.

**5 · The finding that will bite you if you skip it.** Writing the tool's OK
control walked straight into the trap. F46's 1.0.7 phrasing was
`station.demand[res]:GetTargetAmount()`; 1.1.0 hoisted it to
`local demand = station.demand and station.demand[res]` / `demand:GetTargetAmount()`
(`Train.lua:794-795`) — a pure **refactor**, defect untouched. A `DEFECT:` pinned
to phrasing therefore reports `DEFECT-GONE` for a bug that is still shipped: a
FALSE "vanilla fixed it", the direction that **retires a live fix** (R-15's
shape). The right expression states the fault — `Min\(carried,\s*station_cap\)`,
the unload computed from the cap alone. Locked in as fixture `Fix_Selftest
RefactorTrap`. ⚠️ **A `DEFECT-GONE` is a REMOVE candidate, never a verdict.**

**6 · What is stamped, and what "verified" means here.** All 35 KEEP rows (§1d),
76 manifest rows, 73 `OK` / 1 `NO-DEFECT` / 2 `SRC-NONE`, exit 0. ⛔ The FIX and
REMOVE sets are deliberately **unstamped** — 46 `NO-MANIFEST`, which is a count,
not a failure, until the pack is whole. Every hash was taken from the live tree,
so "the hash matches" is true by construction and proves nothing; its value is
future. What IS evidence: each target was resolved in the shipped tree and its
DEFECT expression written against the 1.1.0 body and confirmed to match there.
Three targets had moved far enough that the module's own 1.0.7 header no longer
describes them (`GetRareTraitChance` is now 5 lines through
`Techs.GeneSelection:ResolveValue`; `TunnelBase:AddPFTunnel` guards
`self.linked_obj`; `AlienDigger:GameInit` sits at `:87-96`).
⛔ **NOT a claim that the KEEP set is verified** — I pinned bodies the
re-verification read and re-read only what a defect expression needed. No KEEP
verdict was re-derived; K-9 and K-10 stay "on record, not re-read".

**7 · The named exceptions — a defect that is an ABSENCE cannot be stated
directly**, because a regex matches what is present:

| module | why | what was pinned instead |
|---|---|---|
| `Fix_SinkholeIndestructible` | missing `indestructible` / `disasters_strike_immunity` on a generated class table | the whole classdef by span (`L4-25`), so vanilla ADDING the flag reads as `BODY-CHANGED`. The one `NO-DEFECT` row |
| `Fix_BrokenTrackSalvage` (1st target) | `node_idx` missing from the parameters copied onto the repair site | the consequence, against the sort that raises (`a.node_idx < b.node_idx`) |
| `Fix_GeneForging` | `GeneForging` is unknown to `GetRareTraitChance` | the half that IS present. `DEFECT-GONE` will not fire if vanilla adds the tech alongside `GeneSelection` |
| `Fix_FreedHousingNotice` | `RemoveResident` wakes nobody | its tail (`ResetFreeSpace` as the last act), so adding the wake call stops the match |

**8 · Filed, not fixed (out of my fence).**
* **→ link 05:** `bodycheck.py --selftest` is NOT wired into `doccheck.py`; it is
  a manual gate today. Wiring it (alongside `harvest --check`) is the tools-tail
  fence, not mine.
* **→ link 06:** the inherited `metadata.lua` comment claiming "`PackVersion`
  renders version_major.version_minor.version" describes nothing that exists in
  the 1.1.0 tree (zero grep hits). Passed on from link 01's own inbox, still
  unfixed.
* `sigcheck.py` rated `Fix_TrackSalvageWipe` OK both before and after F116's
  defect was found. `bodycheck.py` is the instrument that closes that, and F116
  is now one of its falsifier legs — but only pack-side (see item 4's limit).

**9 · Drift caught in my own work (chain rule 5 — evidence, not shame).**
* The first block-balance checker counted a `for … ipairs({` whose `do` sits on a
  later line as **two** openers and flagged `Fix_RocketInteractGuard`, which is
  byte-identical at HEAD. Caught by checking HEAD before believing it. Fixed to
  pair each loop head with its own `do`, re-falsified against a deliberately
  broken copy; all 81 `Code/*.lua` balance 0. ⚠️ There is no Lua binary on this
  rig — block balance is the whole desk syntax check, so a wrong checker is a
  wrong gate.
* My first `EXPECT` sets in `--selftest` were wrong twice (a stamped fixture
  yields a row per manifest LINE, not one per module). The tool was right both
  times; I corrected the assertions, not the tool.
* Stamping wrote the 35 files LF where the working tree is CRLF. Content in git
  is unaffected (`git diff` = 35 files, 353 insertions, 0 deletions), but the
  repair pass converted **39 files I had not touched**; they had zero content
  diff and were restored with `git checkout --`. ⚠️ If you see EOL-only churn in
  `Code/`, that is where it came from, and it is not in any commit.

⛔ **What may NOT be claimed from this link.** Not "the pack is update-proof" —
class (c), semantics moving under a wrapper, is still seen by **nothing**. Not
"the KEEP set is verified". Not "probes are safe" in general. No status moved: a
tool run is not a test.
