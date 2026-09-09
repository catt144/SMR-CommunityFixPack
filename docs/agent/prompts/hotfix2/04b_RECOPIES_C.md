# 04b · Group C — the three re-armed fixes (F-8, F-9, F-10)

Chain: `prompts/hotfix2/README.md` (its binding rules are yours). Runs after 02.
Independent of 03 and of 04 — any order. ⚠️ **04 may still be in flight; it owns
group B and the F116 edit. Check `ListAgents` and `git log` before you write.**

⛔ **THIS IS THE HIGHEST-RISK WORK IN THE PATCH, and the risk has a name.**
All three modules replace a game function with a copied body. F114 shipped
exactly this way: a 1.0.7 body copied into the pack, the game rewrote the
function under it, and every instrument the project owned said OK — the name
sweep saw a name, `sigcheck` saw arity, the runtime check saw existence. You have
`bodycheck.py` (link 01), the first instrument that can see this class. **Use it,
and do not treat any other GREEN as a clearance.**

> ⭐ **Why this link exists.** `04` was split on 2026-09-08 under chain rule 4,
> **before it ran**, because six modules at this discipline do not fit one
> context. The owner pre-authorised the split and asked for the judgement to be
> made up front rather than discovered mid-link: *"A chain cannot tell what its
> current context is. If you think it should be split, split it now."*
> ⛔ **So do not treat a further split as failure** — see §6.

## 0 · Start

`git log --oneline -10` · `git pull` · `ListAgents`. Todo list first, **one item
per module** — each is its own commit-and-verify unit.

**Read path:** `agent/STATE.md` · `VANILLA_FIX_QA.md` §0.5 and Reader A's rows
F-8, F-9, F-10 (**the shapes are pinned there; a departure must say why**) ·
`PACK_1_1_0_REVERIFICATION.md` §1a · `agent/FIX_POLICY.md` §1.4b and §2a/§2b ·
`bugs/F114.md` and `bugs/F115.md` (**how this exact work goes wrong**) ·
`docs/PLAYTEST_CHECKLIST.md` items **123** (your ruling), 109, 115, 118 ·
your inbox below — **01's Job D answer is your branch-guard design, read it
verbatim before writing any gate.**

## ✅ 1 · Your mandate — ck123, and what it does and does not settle

⚖️ **Owner ruled ck123 on 2026-09-08: REPAIR ALL THREE.** Verbatim: *"All get
fixed, If the work is really that heavy we should have a 04 and and 04b."*

⛔ **This partly and DELIBERATELY reverts ck109** ("gate, not repair" for F-8).
Not drift, and not yours to re-litigate: ck109 was ruled mid-emergency with a
live P1 in players' games; ck123 was ruled in a considered patch cycle.

⚠️ **KEEP EVERY GATE.** You are re-arming a fix **on top of** its gate, not
removing it. The gates are correct, measured (`archive/logs/gated110_*`), and
they are what makes each module decline on 1.0.7 (ck118). ⛔ **A gate quietly
removed to make a repair work is a finding**, and 99 is told to look for it.

⛔ **A ruling settles what we DO, never what is TRUE.** ck123 did not confirm any
of these defects. In particular F-10's premise is unread — see §4.

**Order — hardest last, and this order is deliberate:**

| # | module | why here |
|---|---|---|
| 1 | **F-8** `LandscapeUnitFilter` | most player value, cleanest repair |
| 2 | **F-10** `TrainCargoDumping` | contained (`Train.lua:779-805`) |
| 3 | **F-9** `VacuumWalks` | ⛔ largest surface in the patch — do it with room, or split it out (§6) |

## 2 · F-8 · `LandscapeUnitFilter`

Body still passes `callback` at `Landscaping.lua:522` while `filter_embark`
(`:516-521`) is unused — the sibling `LandscapeForEachStockpile` passes its
filter (`:503`). Signature is now `(map, mark, callback, ...)` reading
`map.Landscapes[mark]` (`:509-510`; `MapVar("Landscapes", {})` `:21`).
⇒ **repair the body on the new signature, passing `filter_embark`.**

⚠️ **Reach is now Clear-Waste-Rock sites only** (`ClearWasteRockConstructionSite
.lua:79-85`); `LandscapeConstructionSite` no longer defines `GetUnitsUnderneath`.

> ⭐ **RE-CHECKED 2026-09-08 against the shipped tree, and the CONCLUSION HOLDS
> but the EVIDENCE ABOVE IS THE WRONG KIND.** Read this before you rely on it.
> * ✅ **Reach really is Clear-Waste-Rock only** — but the sound evidence is a
>   CALLER grep, not a class-declaration claim: `LandscapeForEachUnit` has
>   **exactly one caller in the whole tree**,
>   `ClearWasteRockConstructionSite.lua:81`.
> * ⛔ **`GetUnitsUnderneath` HAS NOT GONE ANYWHERE.** It is declared on the base
>   `ConstructionSite` (`ConstructionSite.lua:1909`) and overridden on
>   `ClearWasteRockConstructionSite` (`:79`). `LandscapeConstructionSite` still
>   exists (`LandscapeConstructionSite.lua:3`) and **inherits it.** "Class X no
>   longer defines Y" is a statement about SELF-DECLARATION (the F64 lesson), and
>   a reader who takes it as "the capability is gone" is wrong.
> * ✅ **The defect is REAL and present**, read directly rather than inferred:
>   `filter_embark` is built at `Landscaping.lua:516-521` and **never used** —
>   `callback` is passed at `:522`, and `filter_embark` has exactly ONE hit in
>   the entire tree, its own definition. ⇒ **the repair is passing
>   `filter_embark` instead of `callback` at `:522`.**
>
> ⚠️ **Why this note exists rather than a silent correction** (link 02's rule,
> proven in this chain the same day): *"grep found 0 hits" can only prove the old
> NAME is gone, never that the FEATURE was removed.* A `Landscapes`-style
> name-absence claim already produced one false conclusion in this chain (the
> withdrawn "1.1.0 deleted the low-Food warning" — it was RENAMED to
> `StarvingColonists`). ⛔ **If any other disposition you meet here rests on
> "vanilla deleted X" backed by a name grep, search for the CAPABILITY — the
> preset, the UI string, the overriding subclass — not the old identifier.**
⭐ The underlying defect (F34(d)) reproduced **20/20 on PT-60** — ⛔ but that was
under 1.1.0's *wider* pre-narrowing reach, so do not restate 20/20 as this
patch's expected hit rate.

⛔ Half-baked if the repair re-pins the old signature or the bare `Landscapes`
global. **Keep the F115 gate** — it is correct and measured, and the `sigcheck`
MISMATCH there is CORRECT because the body is deliberately untouched... ⚠️ **and
that stops being true the moment you edit the body.** Re-read what `sigcheck`
reports afterwards and say in your outbox whether the MISMATCH is now expected to
clear; a silent change in that signal is exactly what nobody notices.

## 3 · F-10 · `TrainCargoDumping`

`UnloadAll` (`Train.lua:779-805`) gained nil-guards (`:785`, `:794-795`) and a
**BlackCube hook (`:800-802`)**, but still has no enabled check. `Station` is now
a `MultiResourceDepotBase` (`Station.lua:48-56`); `IsResourceEnabled` =
`IsStoring` = demand exists and not `rfSuspended` (`MultiResourceDepot.lua
:242-247`).
⇒ **re-copy `:779-805` with `station:IsResourceEnabled(res)`; carry the BlackCube
hook.** ⛔ Half-baked if the copy drops `:800-802`. **Keep the F114 gate** for the
next change.

## ⛔ 4 · F-10's premise is UNREAD — the one thing ck123 did not fix

Whether a `rfSuspended` request still reports a positive `GetTargetAmount` is
**C-side and nobody has opened it**. The re-verification's own words are
"plausibly persists", not established.

⇒ You will repair it anyway, because that is the ruling. **But:**
- ⛔ your close-out must say the premise was never established;
- ⛔ **no patch-note line may imply the defect was confirmed**, and 06 must not be
  handed wording that does;
- ⭐ if you can cheaply establish it (a control on a station with a disabled
  resource, or a read that settles `GetTargetAmount`), that is worth more than
  the repair itself — **route it to the checklist either way.**

## 5 · F-9 · `VacuumWalks` — the largest surface, do it last

The defect line is byte-for-byte the same (`Colonist.lua:1903`), but everything
around it was rewritten: slot reservation (`:1894-1896`, `:1920-1926`,
`:1943-1949`, `:1972-1978`), `DiscardTransportTicket` (`:1918`), the `-1`
passage-only convention → `max_int` (`:1904-1907`), a `transport_task.shuttle`
guard (`:1898`), `HasShuttleLandingSlots`/`IsSameMap` (`:1932-1957`), a new
`src_dome` search (`:1959-1968`). **Our copy has none of it** — re-arming as-is
would revert all of that.

⇒ **re-copy the 1.1.0 body with `min_dist = 0` in vacuum; read `g_Consts` at call
time** (both walk constants moved from `const.`, which is why the module is
inactive today).

⛔ **NEVER a distance pre-wrapper.** `transport_mode_dist` also drives `:1914`
(walk-vs-shuttle) and the `-1` branch at `:1904` — inflating it changes both.
⚠️ The QA explicitly **did not derive** the semantics of a wrapper passing a
modified distance. If you find yourself reaching for one, that is the signal to
stop and ask, not to improvise.

⛔ **ITS GATE IS CURRENTLY ACCIDENTAL AND MUST END UP DELIBERATE.** The module is
inactive today only because a `const.` → `g_Consts` rename broke its path spec.
⚠️ **"Still inactive" is NOT an acceptable end state** — an accidental gate is one
rename away from silently re-arming a stale 1.0.7 body into a rewritten function,
which is the F114 mechanism precisely. Give it a real probe (§7 item 2).

## 6 · Stop conditions — and a further split is PRE-AUTHORISED

⭐ **If F-9 will not fit comfortably after F-8 and F-10, split it to `04c` and
hand off.** The owner authorised the split principle for exactly this, and rule 4
is the mechanism: commit what is done, write `04c_RECOPIES_F9.md` as a
first-class chain member **with a full inbox** (⛔ not a pointer — this file is
`git rm`'d on close-out), add its README row, hand off. **A single-module link is
a legitimate shape**, and F-9 is the one module in the patch that earns it.

- A 1.1.0 body cannot be copied without also importing a change you cannot
  justify ⇒ **STOP AND ASK.** A re-copy you do not fully understand is the F114
  shape with a new date on it.
- A module cannot be made to decline on 1.0.7 without a version check ⇒ **STOP.**
  Do not build the detector; report it.
- `bodycheck.py` disagrees with your read of the body ⇒ believe the tool until
  you have proven it wrong, and record which of you was right for 99.
- You are reaching for a pre-wrapper on F-9 ⇒ **STOP AND ASK** (§5).

## 7 · Non-negotiable for every module here

1. **`SRC:` / `DEFECT:` manifest lines** per 01's spec, so the next game update is
   a tool run and not a week. **Stamp after the edit.**
2. ⛔ **Declines on 1.0.7.** These modules carry a 1.1.0 body; applied over a
   1.0.7 function that is the F114 failure in reverse, and nothing stops this
   build reaching a 1.0.7 player (ck118). Use 01's Job D design — the per-module
   **probe**, ⛔ **never a game-version detector.**
3. **`bodycheck.py` GREEN** on the module, and **you saw it go RED on a
   deliberately wrong pin at least once.** An instrument you never watched fail
   is not an instrument.
4. **A parse sweep** of every touched `.lua`, with `Mars.exe` closed.
5. ⛔ **A body diff, never a grep.** F116 was filed off a keyword grep; two of its
   four claims did not survive a real structural diff and a fifth divergence
   appeared only when the bodies were diffed properly.

## 8 · Scope fence

**In:** these three modules, their headers/manifests/gates/probes, their bug
entries, their drafted patch-note lines. **Out:** `items.lua`, `metadata.lua`,
store text, `00_Core.lua`, the KEEP set, the harms (03), group B and the F116
edit (both `04`'s). Found something out of fence? **File it, do not fix it.**

## 9 · What may NOT be claimed

- ⛔ **Not "tested".** Nothing here has run in a game. Trains, landscaping and
  vacuum walking have never been exercised on 1.1.0 at all — the 09-08 boot was
  menu-only, and a `applied` log line proves the module loaded, nothing more.
- ⛔ Not "matches vanilla" unless `bodycheck.py` says the pin matches; your
  reading of a diff is not the control.
- ⛔ Not "F-10 is fixed" — its premise rests on an unread C-side function (§4).
- ⛔ Not "the gates are unnecessary now". They are measured and correct; you are
  adding repairs beside them, not replacing them.
- ⛔ Not "20/20" for F-8 on 1.1.0 — that figure predates the reach narrowing.

## 10 · Close-out

Green gates. Your outbox to `06` and `99` must name, **per module**: the 1.1.0
lines you copied, what you deliberately did NOT carry over, the gate's decline
condition, whether its probe is deliberate, and **what has not been exercised in
play** — which here is everything. Route the in-play controls (first train leaves
its platform, a landscaping site progresses, a colonist does not cross vacuum) to
the checklist; they have been owed since hotfix 1. Strike your README row,
`git rm` this file, commit together, push.

## Notes from upstream
*(⚠️ This inbox is CARRIED VERBATIM from `04_RECOPIES.md`, which is `git rm`'d
on its own close-out. It is a full copy, not a pointer — chain rule 4. Link 01's
probe spec below is the one you cannot work without.)*

*(From the authoring session, `smr-bugfixpack-91`, 2026-09-08.)*

- ⚠️ From `smr-bugfixpack-a5`, which ran the F116 leg: F116 was filed off a
  keyword grep, **two of its four claims did not survive a real structural
  diff**, and a FIFTH divergence nobody had listed only appeared when the two
  bodies were diffed properly. `sigcheck.py` rated that module OK throughout.
  If your method for any module here is a grep rather than a body diff, it will
  inherit exactly that failure.
- The owner ruled ck109 as "gate, not repair" for F-8 on 2026-09-08 and then said
  "take up everything we can". Those pull in opposite directions, which is why
  group C is an explicit ask rather than an inference.

### From link 01 — core, tooling and the manifest

⚠️ **For you specifically:** item 2 is Job D's answer verbatim — it is the reply to "how does a 1.1.0 body decline on 1.0.7?", and it is already written into `FIX_POLICY §2a`, so do not re-invent it and do not build a version detector. Item 1 is the form to use. Each re-copy pins its own `SRC:`/`DEFECT:` after the edit (item 3).

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

### From link 02 — the REMOVE block (36 deleted, 1 half-edited, 1 kept)

*(Link 02, `smr-bugfixpack-11`, 2026-09-08. Commits `2dc1dbe` the 36 deletions ·
`f707903` R-7 + the F03 pass · `9b0b82c` 43 bug entries · site `7cef4f3`.
⛔ Nothing was run in a game; no status moved.)*

**The three rulings that unblocked this link, because they bind you too.**

* ⚖️ **ck98 = DELETE, not gate.** Owner, verbatim: *"I am fine with the 1.0.7
  issue, we are giving a path which we don't have to do. The main mod serves the
  current patch period."* There is no 1.0.7 line in the live pack.
  ⛔ **This does NOT relax ck118's constraint on the re-copies.** Our
  `lua_revision` and 1.1.0's minimums are all 350453 (`EF-077`), so hotfix 2
  installs on a 1.0.7 rig with no warning of any kind. Delete-not-gate is a
  ruling about the REMOVE set only; a re-copied 1.1.0 body applied on a 1.0.7
  function is still the F114 failure mode in reverse.
* ⚖️ **ck117 = KEEP `90_SaveSanitizer`** (F35 + F48). It is NOT in the deletion
  set and its `items.lua` entry stays. Only the dead F03 pass was removed.
* ⚖️ **ck120 = the owner's general principle, and it is worth applying to your
  own calls:** *"we fix anything negatives, a small positive I am not as
  concerned about."* That is what killed the F-5 save cleanup — the stranded
  Astrogeologist +10% is an unearned bonus, so it is not chased. A **loss** is a
  different matter and gets fixed.

**What is now true of the tree.** `Code/*.lua` 81 → **45**; `items.lua` 81 → 45;
`metadata.lua`'s `code` list 81 → 45 (all three, per `H-10`); modules 80 → **44**
registered. `bodycheck.py` NO-MANIFEST **46 → 10**, which is link 01's predicted
landing point and is your free cross-check that the right set left.

**For you specifically.** ck98 = delete settles the delete-vs-gate question you
inherit, but ⛔ **your declining self-check requirement is untouched** — see the
ck98 note above. It comes from ck118 and it is independent of ck98.

* **The `probe` form is the right instrument and link 01 built it**, but note the
  direction. For a re-copy you probe FOR the 1.1.0 body shape, so a 1.0.7 body
  declines. That is the easy direction. (The REMOVE set would have needed the
  opposite — a probe that detects the OLD body — which is part of why gating 36
  modules was the expensive road and delete was the cheap one.)
* **A precedent you may want**, from the R-7 half-edit: when you delete half a
  module, its `Require` entries go with it, and you must re-check what the
  surviving half's failure path does. `Fix_DroneTransportMinors`' half (a) had a
  miss-path that returned quietly on the stated grounds that "(b) is installed
  and useful on its own" — with (b) gone that would have made the module silently
  no-op instead of declining. I converted (a)'s two targets into the module's
  `Require`. Retitle too: the old title described (b), and the title is a log
  surface.
* `Fix_SaintBlessing.lua:146` carries a comment citing
  `Fix_AstrogeologistExtractors`' heal, which no longer exists. `SaintBlessing`
  is your module, so the dangling citation is yours to correct or leave.
### From link 03 — the applies-today repairs (F-1, F-2, F-3)

*(Link 03, `smr-bugfixpack-91`, 2026-09-08. Commits `3db4984` F-1 SaintBlessing ·
`f38d6d2` F-2 StaleReservations · `19b5aaa` F-3 ShelterReflex. ⛔ Nothing was run
in a game; no status moved. `Code/*.lua` is still 45 files / 44 modules — this
link added and removed none.)*

**1 · ⛔ THE TRAP THAT WILL BITE YOU IF YOUR MODULE HAS A SAVE-REPAIR PATH.**
`ctx.latch()` sets `entry.status = "inactive"` (`00_Core.lua`, `DataPatch`), and
`SMRFixPack.WhenActive` returns early unless the status is exactly `"active"`.
⇒ **a latching pass silently kills that module's own `OnMsg.LoadGame` heal.** F-1
needed the module to DECLINE its data patch on 1.1.0 and STILL run a save re-base,
so the probe lives *inside the pass* (link 01 said `Require` is a plain function
and may be called from a pass — it is, and this is the case that needs it) and the
1.1.0 branch does **not** latch. Latching is reserved for the UNKNOWN verdict,
where failing both halves closed is the point. If you gate a module off and it
owns a heal, check what you just switched off.

**2 · The `probe` form works exactly as 01 specced it, and here is the shape that
came out.** Two probes rather than one, because a boolean verdict cannot carry
three outcomes:

* probe A: "does the shipped body file under the RAW value?" → true ⇒ 1.0.7 ⇒ apply
* probe B: "does it file under the RESOLVED label?" → true ⇒ 1.1.0 ⇒ decline, and
  arm the save re-base
* neither ⇒ **UNKNOWN**, which is not permission ⇒ do nothing at all and latch.

Both go through `SMRFixPack.Require` so the `pcall` trap, the strict-`true` rule
and the decline logging are the shared ones and not re-implemented. ⚠️ If your
module's branches are also three-valued, do this rather than inverting one probe —
`not A` silently folds UNKNOWN into the wrong branch, which is the F-1 bug itself.

**3 · Two authoring details worth copying.**
* **Collect first, mutate later.** A probe that reads the shipped value back out
  of the shipped function must run against UNTOUCHED data. F-1's pass now builds
  its candidate set, probes, and only then writes.
* **Pick the probe subject deterministically.** `pairs` order is not stable, so
  the boot log would otherwise vary run to run. F-1 takes the lowest trait id.

**4 · The manifest, on three modules that are not plain body copies.**
* **DataPatch shape** (F-1): `-- SRC: none <reason>` + `-- DEFECT@Data/TraitPreset.lua: modify_trait\s*=\s*"Religious"`.
  Works exactly as `bodycheck.py`'s docstring advertises (it names this very
  example) and reports `SRC-NONE` + `OK`.
* **A second `SRC:` with NO `DEFECT:` is a legitimate, deliberate row** (F-1 pins
  `TraitPreset:AddDomeColonistsModifier` for class (b) because the probe and the
  re-base both call it — but on 1.1.0 that body is CORRECT, so there is no defect
  to state). Say so in the file; do not invent a defect to fill the line.
* **Absence defects** (F-2, F-3): §2b's rule held up. F-2 pins `#self\.reserved`
  in `Residence:GetFreeSpace` (a reservation costing a real slot is what is wrong
  *because* nothing expires it); F-3 pins `self:SetCommand\("Roam"\)`, `Idle`'s
  unconditional outdoor exit. **Both carry their limit in the file**: if vanilla
  adds the missing guard elsewhere, `DEFECT-GONE` will not fire and the module is
  watched for class (b) only.

**5 · Discharged, from 02's note to you.** `Fix_SaintBlessing.lua`'s comment citing
`Fix_AstrogeologistExtractors`' heal is corrected in `3db4984` — kept as history
with the deletion named, rather than deleted, because it is where that check's
shape came from.

**6 · Filed, not fixed (out of my fence — yours only if you touch these).**
* `00_Core.lua:304` cites `Fix_AstrogeologistExtractors:174` (deleted by 02) and
  `Fix_SaintBlessing:151` (moved by `3db4984`). Historical, explanatory, harmless —
  but stale. Routed to 99.
* `tools/harvest_wrap_targets.py:173-175`'s parenthetical explains why
  `Fix_ShelterReflex`'s `MicroGHabitatAutoResolve.IsSuitable` replacement is
  outside the wrap check. That replacement no longer exists. Routed to 05 and 99.

⛔ **What may NOT be claimed from this link.** Not "F-1/F-2/F-3 are fixed" — all
three are source-derived and **none has been seen in play**; three owner controls
are on the checklist, unrun. Not "saves are healed" — the F-1 re-base is untested
until a save that loaded under the broken pack is loaded again with this build.
Not "F-3 is now correct" — half (a) is now **absent**, and 1.1.0 players get the
vanilla blip-eviction back.
#### ⚖️ ADDENDUM from link 03 — the owner RULED the controls deferred (2026-09-08)

Ruled after 03 closed, so it postdates the block above and changes how you route
your own in-play controls. Owner, verbatim: *"Can the sitting be done after the
chain. I want to insure everything is green on this side and then we can check
the live side?"*

⇒ **ALL in-play controls merge into ONE consolidated sitting after link 99.**
Link 03's three (Saint blessing, expedition housing, asteroid habitat trait
filter) are on the checklist as **scheduled, not owed**. Route yours the same
way: file them in the checklist as usual, but present them as **joining the
post-99 sitting**, not as something owed now. ⛔ Do not open a second sitting.

Two things ride with it and both bind you:

1. ⛔ **A SHIP verdict from 99 is NOT clearance for the upload sitting.** It means
   the desk side is green; the controls sit BETWEEN 99 and the owner's sitting.
   `H-04` binds — never treat a future release as ready.
2. ⚠️ **⛔ DO NOT LOAD A SAVE THAT RAN UNDER THE BROKEN PACK.** The
   `SaintBlessing` save re-base is one-shot per save: the log line
   `SaintBlessing: restored N dome blessing(s) …` prints on the FIRST load of a
   poisoned save and never again. Any boot you take with a build carrying
   `3db4984` spends that evidence. 04/04b run nothing in a game, so this should
   not come up on its own — but if a leg of yours ever does load a save, **capture
   the full log** and say which save it was. ⛔ Do NOT copy a save as insurance
   (`H-06`: loading a copy runs that campaign's autosave rotation and deletes the
   owner's autosaves).
