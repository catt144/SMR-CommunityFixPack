# 04 · The re-copies — five modules that take a 1.1.0 body, plus one scoped edit (§7)

Chain: `prompts/hotfix2/README.md` (its binding rules are yours). Runs after 02.
Independent of 03 — either order.

⛔ **This is the highest-risk prompt in the chain, and the risk has a name.**
Every module here replaces a game function with a copied body. F114 shipped
exactly this way: a 1.0.7 body copied into the pack, the game rewrote the
function under it, and every instrument the project owned said OK — the name
sweep saw a name, `sigcheck` saw arity, the runtime check saw existence. You now
have `bodycheck.py` (link 01), which is the first instrument that can see this
class. **Use it, and do not treat any other GREEN as a clearance.**

## 0 · Start

`git log --oneline -10` · `git pull` · `ListAgents`. Todo list first, one item
per module — each is its own commit-and-verify unit.

**Read path:** `agent/STATE.md` · `VANILLA_FIX_QA.md` §0.5 and Reader A's rows
F-6…F-10 (**the shapes are pinned there; a departure must say why**) ·
`PACK_1_1_0_REVERIFICATION.md` §1a · `agent/FIX_POLICY.md` §1.4b · `bugs/F114.md`
and `bugs/F115.md` (how this goes wrong) · `docs/PLAYTEST_CHECKLIST.md` items
109, 115, 118 — **and 111 + 119, the two rulings behind §7** · `bugs/F116.md`
(§7's record; its claim 5 and "What did NOT land" are the two divergences) ·
your inbox — **01's Job D answer is your branch-guard design,
read it verbatim before writing any gate.**

## ✅ 1 · Group C is RULED — all three are IN

⚖️ **Owner ruled ck123 on 2026-09-08: REPAIR ALL THREE.** Verbatim: *"All get
fixed, If the work is really that heavy we should have a 04 and and 04b."*
**Nothing in this prompt is blocked any more** — B, C and §7 are all yours.

⛔ **This partly and DELIBERATELY reverts ck109** ("gate, not repair" for F-8).
That is not drift and it is not yours to re-litigate: ck109 was ruled mid-
emergency with a live P1 in players' games, and the owner has now re-ruled it in
a considered patch cycle. ⚠️ **KEEP the gates** in every case — they are correct
and measured, and they are what makes the module decline on 1.0.7 (ck118). You
are re-arming the fix ON TOP of a gate, not removing it.

⭐ **A 04b SPLIT IS PRE-AUTHORISED — use it rather than rushing.** The owner
offered it unprompted, so taking it is a success, not an admission. Chain rule 4
is the mechanism: commit what is done, write `04b_RECOPIES_C.md` as a first-class
chain member with a full inbox, add its row to `README.md`, and hand off. ⛔ **Do
NOT push all six modules to the edge of one context** — this is the highest-risk
prompt in the chain and the failure it guards against (F114) was a body copy
written without enough room to think. **Suggested cut if you need one: B + §7
here, group C in 04b** — B is two small edits and §7 is scoped, while C is three
1.1.0 body copies of which F-9 is the largest surface in the patch.

⚠️ **Do them in this order, hardest last:** F-8 (most player value, confirmed
20/20 on PT-60 — ⛔ though under 1.1.0's NARROWED reach, Clear-Waste-Rock sites
only), then F-10, then F-9. ⛔ **F-10 carries an unread premise** — whether a
`rfSuspended` request still reports a positive `GetTargetAmount` is C-side and
nobody has established it. Say so in your close-out; do not let the re-copy imply
the defect was confirmed. ⛔ **F-9's gate is currently ACCIDENTAL** (a
`const.` → `g_Consts` rename broke its path spec). Whatever else you do with
F-9, that gate must end up DELIBERATE — an accidental gate is one rename away
from silently re-arming a 1.0.7 body.

## 2 · Group B — unblocked

### F-7 `RocketDroneChurn` — one clause
`UpdateCargoResourceRequests` still brackets with unconditional
`Disconnect`/`Connect` (`CargoTransporterNew.lua:1431-1433`, `:1460-1462`), so
F50 persists. One line changed inside the loop:
`additional_amount = is_refuel_resource and not self.refuel_disabled and
self:GetFuelResourceRequest()` (`:1442`). `refuel_disabled` is a new player
toggle (`UniversalRocket.lua:70`, `:3320`); our copy lacks the clause.
⇒ **re-copy the 1.1.0 body carrying `not self.refuel_disabled`.**

### F-6 `PayloadTemplateRefill` — three reverts to avoid
The refill is unchanged (`CargoRequestNew.lua:221-234`), so F70 persists. Our
copy would revert three 1.1.0 changes:
1. `resolve_loc_cargo_template` gained a **tutorial branch** (`:183-189`,
   `AsteroidTutorialExpectedCargo`) and a `CmdLoad` exemption for destination
   picks (`:174`);
2. `RetrieveRequests` reads `prev_flight_data` and ignores stored cargo on a
   destination pick (`:215-217`);
3. the automode branch nil-guards `cargo_items[id]` (`:199-213`).

**Shape, pinned by the QA:** gate as `not from_destination_pick and
transporter.SMRFixPack_payload_set`; ⛔ **the tutorial return (`:183-189`) must
precede the gate** so rocket 2 is still pre-filled; ⛔ **stamp the flag on the
CONFIRMED path** (`:376-379`, `SetCommand("CmdLoad")`), **not** on `Apply` entry
— `Apply` is now an async prompt (`:368-385`) and our pre-wrapper would suppress
the template even when the player cancels (`CancelFlight`, `:382`).

## 3 · Group C — RULED IN (ck123); keep every gate

### F-8 `LandscapeUnitFilter`
Body still passes `callback` at `Landscaping.lua:522` while `filter_embark`
(`:516-521`) is unused — the sibling `LandscapeForEachStockpile` passes its
filter (`:503`). Signature is now `(map, mark, callback, ...)` reading
`map.Landscapes[mark]` (`:509-510`; `MapVar("Landscapes", {})` `:21`).
⇒ repair the body on the new signature, passing `filter_embark`.
⚠️ **Reach is now Clear-Waste-Rock sites only** (`ClearWasteRockConstructionSite
.lua:79-85`); `LandscapeConstructionSite` no longer defines `GetUnitsUnderneath`.
⛔ Half-baked if the repair re-pins the old signature or the bare `Landscapes`
global. **Keep the F115 gate** — it is correct and measured, and the `sigcheck`
MISMATCH there is CORRECT because the body is deliberately untouched.

### F-9 `VacuumWalks`
The defect line is byte-for-byte the same (`Colonist.lua:1903`), but everything
around it was rewritten: slot reservation (`:1894-1896`, `:1920-1926`,
`:1943-1949`, `:1972-1978`), `DiscardTransportTicket` (`:1918`), the `-1`
passage-only convention → `max_int` (`:1904-1907`), a `transport_task.shuttle`
guard (`:1898`), `HasShuttleLandingSlots`/`IsSameMap` (`:1932-1957`), a new
`src_dome` search (`:1959-1968`). Our copy has none of it.
⇒ **re-copy the 1.1.0 body with `min_dist = 0` in vacuum; read `g_Consts` at
call time** (the consts moved from `const.`, which is why the module is
inactive-by-accident today).
⛔ **NEVER a distance pre-wrapper.** `transport_mode_dist` also drives `:1914`
(walk-vs-shuttle) and the `-1` branch at `:1904` — inflating it changes both.
Make the gate deliberate rather than accidental.

### F-10 `TrainCargoDumping`
`UnloadAll` (`Train.lua:779-805`) gained nil-guards (`:785`, `:794-795`) and a
**BlackCube hook (`:800-802`)**, but still has no enabled check. `Station` is now
a `MultiResourceDepotBase` (`Station.lua:48-56`); `IsResourceEnabled` =
`IsStoring` = demand exists and not `rfSuspended` (`MultiResourceDepot.lua
:242-247`).
⇒ **re-copy `:779-805` with `station:IsResourceEnabled(res)`; carry the BlackCube
hook.** ⛔ Half-baked if the copy drops `:800-802`. Keep the F114 gate for the
next change.
⚠️ Whether a suspended request still reports a positive `GetTargetAmount` is
C-side and unread — "plausibly persists", not established. Say so.

## 4 · Non-negotiable for every module here

1. **`SRC:` / `DEFECT:` manifest lines** per 01's spec, so the next game update
   is a tool run and not a week. Stamp after the edit.
2. **`bodycheck.py` GREEN** on the module, and you saw it go RED on a
   deliberately wrong pin at least once. An instrument you never watched fail is
   not an instrument.
3. ⛔ **Declines on 1.0.7.** These modules carry a 1.1.0 body; applied over a
   1.0.7 function that is the F114 failure in reverse, and nothing stops this
   build reaching a 1.0.7 player (ck118). Use 01's Job D design — the
   per-module probe, **never a game-version detector**.
4. **A parse sweep** of every touched `.lua`, with `Mars.exe` closed.

## 5 · Scope fence

**In:** the five modules, their headers/manifests/gates, their bug entries, their
drafted patch-note lines — **plus the SIXTH module in §7 (`Fix_TrackSalvageWipe`,
F116), scoped to two ruled divergences only.** **Out:** `items.lua`,
`metadata.lua`, store text, `00_Core.lua`, the rest of the KEEP set, the harms (03).
⚠️ **F116 moved from Out to In on 2026-09-08** when the owner ruled ck111 and
ck119. ⛔ The rest of F116 is still Out: **do not re-derive it** — its `K-11`
KEEP verdict stands and only the two named divergences are yours.
Found something out of fence? **File it, do not fix it.**

## 6 · Stop conditions

- ⛔ Group C is RULED IN (ck123) — there is no "unruled" stop here any more.
  If the six modules will not fit comfortably, **split to `04b` (pre-authorised by
  the owner) rather than rushing or dropping one.**
- A 1.1.0 body cannot be copied without also importing a change you cannot
  justify ⇒ **STOP AND ASK.** A re-copy you do not fully understand is the F114
  shape with a new date on it.
- A module cannot be made to decline on 1.0.7 without a version check ⇒ **STOP.**
  Do not build the detector; report it.
- `bodycheck.py` disagrees with your read of the body ⇒ believe the tool until
  you have proven it wrong, and record which of you was right for 99.

## 7 · The sixth module — `Fix_TrackSalvageWipe` (F116), two ruled divergences

⚖️ **Owner ruled ck111 + ck119 on 2026-09-08 and folded them here** ("fold them
into whatever chain makes the most sense and update the audit"). This module is a
`KEEP` (`K-11`) and its 1.1.0 re-derivation is DONE — ⛔ **do not redo it.** You
are landing two specific, already-decided changes and nothing else.

**Both are in `TrackGridElement:DemolishAndSplitTrack`, in the split branch, in
the region our F44 fixes already occupy.**

### ck111 — rehome the orphan instead of deleting it
Ours DELETES any element still carrying `track_obj == false` after both
expansions (`Fix_TrackSalvageWipe.lua:335-339`); 1.1.0 REHOMES it into a fresh
track (`TrackElement.lua:580-595`). ⇒ as it stands **our "don't destroy the
player's track" fix can destroy a fragment the unmodded game would have saved.**
Take vanilla's loop. ⚠️ Our body has no `tracks` array (1.1.0 introduced one), so
collect the new tracks in a local and extend the three tail blocks at `:344-365`
— `UpdateEndElements`/`UpdatePos`, and the four `ProcessTrackElements` calls — to
cover them. ⭐ Termination is not in doubt: each pass assigns at least the orphan
itself a track, so the `track_obj == false` count strictly decreases.

### ck119 — post-split processing for mixed tracks
1.1.0 processes each resulting track's **combined** element list (`:609-613`);
our 1.0.7 tail processes one array and only when the other is empty, so a track
holding **both** completed and under-construction elements gets none. Inherited
1.0.7 behaviour, no observed harm — it rides with ck111 because it is nearly free
in the same edit, not because it is urgent.

### ⛔ Ruled, so do not reopen
- **The `OnMsg.LoadGame` sweep KEEPS deleting orphans.** Owner ruled it: at load
  there is no split context to rehome into, and it only fires on genuinely
  stranded legacy debris. It is NOT an oversight and NOT yours to change.
- The `K-11` KEEP verdict stands. Everything in F116 except these two is Out.

### ⚠️ Two traps specific to this module
1. ⛔ **It is ALREADY STAMPED.** Link 01 stamped the `SRC:`/`DEFECT:` manifest
   across all 35 KEEP modules at `e2490f3`, and this module is in that set — so
   its pinned `SRC:` hash was taken BEFORE your edit and your edit makes it a
   lie. **Run `bodycheck.py` before AND after, and re-stamp the `SRC:` hash**, so
   the change is visible to the instrument rather than surfacing as an
   unattributable `BODY-CHANGED` in 99's Pass A.
2. ⛔ **99's Pass D treats any unexplained change to a KEEP module as a finding.**
   This module is named there as an expected exception — confirm that note is
   present and accurate when you close out, and if you touch anything beyond the
   two divergences, say so explicitly or the audit will correctly flag it.

⭐ **What you may NOT claim here, beyond §8's list:** F116 has never been
reproduced in a log and produces no throw — it is silent by construction. Neither
the existing repair nor these two changes has ever run in a game. ⛔ A boot log
reading `TrackSalvageWipe: applied` proves the module loaded, nothing more.

## 8 · What may NOT be claimed

- ⛔ **Not "tested".** Nothing here has run in a game. Trains and landscaping
  have never been exercised on 1.1.0 at all — the 09-08 boot was menu-only.
- ⛔ Not "matches vanilla" unless `bodycheck.py` says the pin matches; your
  reading of a diff is not the control.
- ⛔ Not "F-10 is fixed" — its premise rests on an unread C-side function.
- ⛔ Not "the gates are unnecessary now". They are measured and correct; you are
  adding repairs beside them, not replacing them.

## 9 · Close-out

Green gates. Your outbox to `06` and `99` must name, per module: the 1.1.0 lines
you copied, what you deliberately did NOT carry over, the gate's decline
condition, and **what has not been exercised in play** — which for these five is
everything. Route the in-play controls (first train leaves its platform, a
landscaping site progresses) to the checklist; they have been owed since
hotfix 1. Strike your README row, `git rm` this file, commit together, push.

## Notes from upstream

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
