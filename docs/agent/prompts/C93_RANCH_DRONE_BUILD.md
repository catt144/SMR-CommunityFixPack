# C93 — the ranch drone stall: identify the entity-less approach target, then guard it

One-off, authored 2026-09-16 from the owner's own reproducing save. Tool-neutral
(Claude or Codex). `git rm` this file **and its `prompts/README.md` row in the same
commit** when it has reported. Defect record: [C93](../bugs/C93.md).

Start with `git log --oneline -6`, `git pull`, `git status --short`. The job was
authored at `981f6b2`; find this file's own commit with
`git log -1 --format=%h -- docs/agent/prompts/C93_RANCH_DRONE_BUILD.md` and compare every
input named in §7 through HEAD, re-deriving only the groups that moved.

⭐ **The owner reproduces this on demand and is holding the save.** This is not an
inherited field report any more. Reach check (the `fe6df03` rule): the defect fires on a
live 1.1.0.403908 Steam colony at save load, so every platform the pack serves can reach
it and the owner can test the fix. It clears the bar that pulled `F120`.

## 0 · How to work this

**Open a live progress list before you touch anything**, one item per
commit-and-verify unit, exactly one in progress. Expand a stage the moment it splits,
tick each unit as it lands, rewrite the list when reality changes. The owner reads that
list to decide when to step in. Minimum shape:

1. Orient + staleness check (§7).
2. **Leg A** — name the entity-less object (§3). ⛔ **Gate: the fix is not designed until
   this returns.**
3. **Leg B** — design the guard against what Leg A actually found (§4).
4. Desk falsifier suite (§4c).
5. Owner sitting + acceptance (§5).
6. Entry + report + close-out (§6, §8).

**This brief hands you measurements and one hypothesis, not a conclusion.** Everything
below except §1 is a claim, ours included. Overturning it is a better result than
confirming it. Read anywhere; write only where §6 says.

## 1 · What is MEASURED (owner's save, 2026-09-16)

Log `%APPDATA%\Surviving Mars Relaunched\logs\Mars.exe-20260916-11.11.22-6a91a190.log`,
game 1.1.0.403908, build `6a91a190`, 57 196 lines, mods: Fix Pack v1.00-011, Opt-In Pack,
Test Kit, FR-1 workaround.

- `python tools/logscan.py <log>` → **2810 error-shaped lines**, and
  `grep -o "\[LUA ERROR\].*" <log> | sed 's/[0-9]\+/N/g' | sort | uniq -c` →
  **one single message, 2809 of it**, nothing else in the log:
  `HGE::l_HasSpot: The object given has no entity`.
- Two stack sites, same path both times:
  `Unit.lua(526) IsNearUnreachableBuildingSpot` and `Unit.lua(511) FaceBuildingSpot`,
  under `Unit.lua(604)/(620)` ← `Drone.lua(920) ApproachWrapper` ← `Drone.lua(1446)` ←
  `sprocall` ← `CommandObject.lua(250)`.
- ⭐ **The first error is at line 277, 0.4 s after `Game Loaded in 19562 ms`.** The stall
  resumes from the save; play does not create it. A save-load reproduces on demand.
- `grep -c "doesn't have spot" <log>` → **0** (see §2's correction — this does *not*
  refute C93's recorded mechanism the way C93's control table says it does).
- Toolkit screenshot `C:\Dev\SMR-ScreenCaptures\SMRTK_0008.png`: selected object
  **`OpenPasture(4396)`** (Outside Ranch), Stored Resources **0/2,000** with Food, Meat and
  Cheese all 0, produce bar reading 152.2 food / 121.8 meat, `errors since mark: 2802`,
  work shifts 204 %.

⚠️ The screenshot shows what the owner had selected, **not** what the drones were failing
to approach. Do not treat `OpenPasture(4396)` as the identified target — that is Leg A's job.

### ⭐ Second sample, same session: an end-to-end production run (owner, 2026-09-16 11:34)

The owner ran a full production cycle in the same ranch and flushed again. Same log, grown to
129 843 lines:

- **6472 error lines, still exactly one message shape** — nothing else has appeared.
  Split by stack site: **4485 `IsNearUnreachableBuildingSpot`, 1987 `FaceBuildingSpot`**.
- `grep -c "doesn't have spot"` → **still 0**.
- Screenshot `SMRTK_0009.png`, Sol 327 (was 320), same `OpenPasture(4396)`: Stored Resources
  **81/2,000 — Food 46, Meat 35, Cheese 0** (was 0/2,000, all zero), breeds now Pig and
  Ostrich, `errors since mark: 3543`.
- ⭐ **The produce crates are visible as a stack in the dead centre of the pasture**, inside
  the fenced footprint, in both screenshots.
- ⭐ **`SMRTK_0010.png` (11:37, Screenshot + Mark, so it is in the records)** is the close-up
  and the best single image of the defect: the crate stack on its platform in the middle of
  the grass, animals grazing around it, and **a line of drones queued along the outside of
  the pasture wall** — the owner's words, *"the drones are actively trying to get into it to
  collect resources."* Taken after a fresh MARK, it reads `errors since mark: 126`, so the
  throw is still firing at a steady rate while nothing moves.
- ⭐ **Stored Resources held at 81/2,000 (Food 46, Meat 35) across `SMRTK_0009` and
  `SMRTK_0010`** — the ranch is not being emptied at all between the two captures.

⇒ Two facts the first sample could not give you: **production itself works** (the ranch fills
normally), and the failure is entirely on the **collection** side. The error rate scales with
the attempt rate, and the drones are visibly massed at the footprint edge.

Two readings follow directly from that close-up, and together they are the reason this brief
gates its fix:

- **The pile object is healthy.** The crates stand on a rendered `ResourcePlatform` — visible
  under them — so the pile is *not* the thing throwing `has no entity`. That matches the desk
  (`ResourceStockpile.lua:109`) and is now visually confirmed.
- **What the player sees is pure reachability.** The pile sits inside a footprint the drones
  cannot enter — `OpenPastureBase` declares no `efWalkable` (C93), so the centre is enclosed
  — and they queue at its edge.

⇒ ⚠️ **So treat this as possibly TWO defects, and make Leg A decide which you are fixing:**
(i) a pile placed where drones cannot path — the symptom both reporters describe and the one
the owner can see; and (ii) an entity-less object throwing on the approach path — the 6472
log lines. A pile attached at `Origin` would sit exactly where this one sits, which is why
they may well be one story; but a pile carries an entity, so (i) alone cannot produce (ii).
⛔ **Do not ship a fix that quiets the log while the crates stay put**, and do not write the
tidy single-cause version until Leg A names the object and §5 step 5 has read
`GetAttachSpot()`.

## 2 · The mechanism as traced, and the one hole in it

Read on the live tree `A:\SteamLibrary\steamapps\common\Project Spark\ModTools\Src`:

1. `Drone:Deliver` (`Lua/Units/Drone.lua:1366`) takes its target from
   `local building = d_request:GetSource(self)` (`:1401`) — so every one of the 2810
   throws is a **delivery**, not a pickup.
2. Its retry loop is `while true do ... if self:ApproachWrapper(building, resource)`
   (`:1444-1446`), `Sleep(1000)` per turn.
3. `Drone:ApproachWrapper` (`:919-933`) guards `IsValid(building)` and
   `building:IsValidPos()`, then calls `building:DroneApproach(self, resource)`.
4. The generic `TaskRequester:DroneApproach` (`Lua/_TaskRequest.lua:252-254`) is
   **unguarded**: `return drone:GotoBuildingSpot(self, drone.work_spot_task)`.
5. `Unit:GotoBuildingSpot` (`Lua/Units/Unit.lua:571`) reaches
   `Unit:FaceBuildingSpot` (`:508-519`) and `Unit:IsNearUnreachableBuildingSpot`
   (`:522-535`). Both do `spot and building:HasSpot(state, spot)`. `HasSpot` is an engine
   call that **throws when the object has no entity** — the guard tests the *spot*, never
   the *entity*.
6. `sprocall` catches it (`CommonLua/Classes/CommandObject.lua:249-260`), sleeps 1 s and
   lets the command restart. ⇒ **`MarkUnreachable` (`Drone.lua:924`) never runs**, so the
   drone never marks the target unreachable and `must_change` (`:1455`) never trips. The
   recovery path that exists for unreachable targets is defeated by the throw itself.

⇒ A drone holding a resource for an entity-less destination stalls **permanently**,
carrying its load, at roughly one error per second, and re-enters the stall on every load.
That is consistent with "drones circling the ranch but can't pick anything up": enough
stuck carriers and the ranch's own produce is never collected. ⛔ **That last step is a
shape argument, not a measurement.** Leg A and §5 decide whether the ranch symptom and this
throw are the same defect or two that happen to share a save.

**Vanilla already guards this elsewhere** — `BaseRover:DroneApproach` tests
`if not self:HasSpot(self:GetState(), drone.work_spot_task)` before the goto
(`Lua/Buildings/BaseRover.lua:299-303`), and `RocketBase` does the same
(`Lua/Buildings/RocketBase.lua:1818`). The generic requester path has no such test. The fix
is a missing guard on a path vanilla guards on its siblings, not new behaviour.

### ⛔ A correction C93 needs, and the brief that inherits it must carry

C93's control table reads *"log line absent ⇒ this entry's mechanism is refuted."* **That
control is too strong, and this save is why.** The `print("once", ... "doesn't have spot")`
at `Lua/Buildings/StockpileController.lua:103-105` only fires **when piles are created**,
in the session that creates them. The pasture re-pooling fixup
`SavegameFixups.SharePastureStockpilePools2` (`Lua/Units/Animals.lua:1388`) carries **the
same `Origin` fallback at `:1430-1432` with no print at all**. So zero hits proves only
that no pile was created *in this session* — not that no pile sits at `Origin`.
⇒ Report the Origin question as **open and separately testable** (read the piles'
`GetAttachSpot()` on the live ranch), never as refuted.

## 3 · Leg A — name the object. Nothing is designed before this returns

⛔ **Do not guess the class.** The desk narrowed it and could not close it:

- Piles are **not** the obvious answer: `ResourceStockpileBase` declares
  `entity = "ResourcePlatform"` (`Lua/Buildings/ResourceStockpile.lua:109`) and no stockpile
  class clears it (`grep -n "ChangeEntity\|DestroyEntity\|SetEntity\|entity"` over
  `MixedPoolStockpile.lua`, `MultiResourceCubeVisuals.lua`, `ResourceStockpile.lua` returns
  nothing that removes one).
- **Leading candidate, unconfirmed:** `SingleResourceProducer`
  (`Lua/Buildings/BuildingComponents.lua:1082-1083`, `__parents = { "Object",
  "StockpileController", "Modifiable" }`) is built with `:new()` at `:514`, never placed
  with an entity. `StockpileController` itself is a bare `Object`
  (`Lua/Buildings/StockpileController.lua:7-8`). Whether either can ever own a demand
  request that `GetSource` hands a drone is **not traced** — trace it or refute it.

**Build a log-only probe** (TestKit, not the pack) that wraps the approach path and, on an
object failing `HasEntity()`, prints: class, handle/id, `GetEntity()`, `IsValid`, position,
`GetAttachSpot()` if attached, the attach parent and its class, the request's resource and
amount, and whether the parent is the ranch in the screenshot. `obj:HasEntity()` and
`IsValidEntity()` are the engine idioms in use (`Lua/Buildings/BaseBuilding.lua:900,970`).
⛔ Log-only: the probe must not change what any drone does — a stub for a call that can
refuse is a behaviour change (`F59` A3).

Deliver from Leg A, in the report: **what the object is, how it came to exist without an
entity, and whether it is reachable-by-design or garbage.** The fix shape depends entirely
on the answer — a legitimately entity-less requester wants a tolerant approach path; a
corpse that should never have been a request source wants the corpse dealt with.

## 4 · Leg B — the fix

⛔ **Design against Leg A's finding, not against this section.** Read
`docs/agent/FIX_POLICY.md` for seam and hooking rules before writing a line.

### 4a · The default shape, if Leg A finds a legitimately entity-less requester

Guard the entity where the engine call is made, in the two `Unit` bodies at `Unit.lua:511`
and `:526`, so a missing entity takes the **path the code already has for a missing spot**:
`FaceBuildingSpot` falls through to `self:Face(building, 100)`, and
`IsNearUnreachableBuildingSpot` falls through to `building:GetPosXYZ()` plus
`GetRadius()`. Both already handle `spot_idx == nil`. ⭐ **That is why this is a repair and
not a redesign: the fallback exists, the throw just prevents reaching it.**

⚠️ **State explicitly whether the guard makes the delivery SUCCEED or merely makes it fail
quietly.** They are different products. If the drone now reaches the object and unloads,
the produce moves. If it still cannot, at least `MarkUnreachable` runs, the request is
re-targeted and the drone stops burning a slot — say which one the test showed, and do not
let a silenced log stand in for a fixed colony.

### 4b · What the fix may not do

- ⛔ No change to vanilla's spot data, entity assignment or pile placement.
- ⛔ Do not "fix" the Origin fallback in the same module — it is a separate, unproven
  mechanism (§2's correction). Route it to C93 as an open question.
- ⛔ No pack file may be edited outside `Code/` plus its `items.lua`/`metadata.lua`
  registration. Check `grep -c '^\s*--' metadata.lua items.lua` is non-zero before you
  commit either (trap 3 — a stripped writeback buries ~400 comment lines).

### 4c · Desk falsifier suite

Before the owner sees it, run the module at the desk (`tools/desk_*.py` precedent, lupa
shims per house practice) with legs that must FAIL on the pre-fix body and PASS on the
fixed one: an entity-less approach target, a normal building with the spot, a normal
building **without** the spot (the existing nil-spot path must be unchanged), an invalid
object, and a nil spot. ⭐ **A fix invalidates its own tests:** base the harm legs on the
pre-fix body and run the whole suite, not only the changed leg.

## 5 · Leg C — the owner sitting

Run the **probe-sweep step** first per `docs/agent/WORKFLOW.md` § Probe hygiene, and put its
evidence in the progress list. The ck184 ruling in STATE makes freshness an age satisfied at
the next playtest, never a refusal to work.

The fixture is **the owner's existing save** — warmed, no provisioning. Do not ask them to
build a new colony. Name every setup action; reject any that touches drone assignment, the
ranch's shifts or stockpile state, since those intersect the mechanism.

Acceptance, in order:

1. **Before.** Load the save with the pack as shipped, note the error count from the toolkit
   status line and the ranch's Stored Resources. This is the control and it already exists.
2. **After.** Load with the fix, confirm the module's `applied` line, and read the whole log
   for new errors — not only for the absence of the old one.
3. **The colony reading.** Three witnesses, all visible without instrumentation: does
   **Stored Resources fall** from its pre-fix figure; does the **centre crate stack drain**;
   does the **cluster of drones on the pasture wall disperse**. Record the colony's scarcity,
   drone fleet size, density and layout, and report *that* colony's measurement — do not
   generalise from it. ⚠️ Production works already (§1) — a ranch that keeps filling proves
   nothing; only collection is under test.
4. **Removal.** Save with the fix, disable the pack in Mod Manager, restart fully, reload:
   vanilla behaviour returns and the save is not damaged.
5. ⭐ **Free reading while you are there:** read the ranch piles' `GetAttachSpot()` and settle
   §2's Origin question one way or the other.

## 6 · What may NOT be claimed

- ⛔ Not *"C93 is fixed"* unless Leg A's object is the one stranding the ranch's produce
  **and** §5 step 3 shows the produce moving. Otherwise the true, narrower statement is:
  *a drone-stall defect measured in the owner's save is repaired; whether it is the whole of
  the reporters' ranch symptom is not established.*
- ⛔ Nothing about either **field reporter's** install is settled by this save. Their mod
  lists and logs remain unknown, and C93's attribution stays open.
- ⛔ Do not claim the Origin fallback is refuted (§2).
- ⛔ Replies to players are **PULL-ONLY** (`WORKFLOW.md` rule 5b, ck165). However this lands,
  draft nothing to the reporters and put nothing on the owner's owed list.

Write the result to `docs/agent/reports/` and fold the measured evidence into
[C93](../bugs/C93.md) — including the §2 control correction, which stands whatever the fix
does. Record the owner's decisions in `docs/PLAYTEST_CHECKLIST.md` under "Decisions waiting
on you" (a new `### <date> — <n>: <title>` plus its `<!-- ck:n ... -->` marker; sub-headings
`####`), then verify `python tools/doccheck.py | grep WAITING:` has not fallen (traps 11
and 12).

## 7 · Derived facts, and how to falsify each

Everything here was derived this session against game build **6a91a190 / 1.1.0.403908** and
repo HEAD **`981f6b2`**. `git diff --stat 981f6b2..HEAD -- <path>` empty ⇒ that input needs
no re-read.

| fact | how measured | falsifier |
|---|---|---|
| 2810 errors, one message only | `python tools/logscan.py <log>`; `grep -o "\[LUA ERROR\].*" <log> \| sed 's/[0-9]\+/N/g' \| sort \| uniq -c` | re-run on the same log; a second message shape breaks it |
| the stall resumes 0.4 s after load | `sed -n '255,280p' <log>` | read the lines around the first `[LUA ERROR]` |
| `HasSpot` unguarded on entity | `sed -n '508,535p' Lua/Units/Unit.lua` | read the two bodies; a `HasEntity`/`IsValidEntity` test would refute it |
| the target is a *delivery* source | `sed -n '1366,1410p' Lua/Units/Drone.lua` (`:1401`) | read `Drone:Deliver`'s binding of `building` |
| the throw defeats `MarkUnreachable` | `sed -n '919,933p' Lua/Units/Drone.lua` + `sed -n '235,262p' CommonLua/Classes/CommandObject.lua` | show a path where the catch still reaches `:924` |
| vanilla guards the same call on rovers/rockets | `sed -n '294,305p' Lua/Buildings/BaseRover.lua`; `RocketBase.lua:1818` | read both |
| piles keep `entity = "ResourcePlatform"` | `ResourceStockpile.lua:109` + the three-file entity grep in §3 | find a body that clears a pile's entity |
| the pasture fixup's silent `Origin` fallback | `sed -n '1388,1440p' Lua/Units/Animals.lua` (`:1430`) | find a print on that branch |
| the pack does not touch pastures | C93's own word-boundary grep over `Code/` | re-run `grep -riE "\b(ranch\|pasture\|OpenPasture)\b" Code/` |

⛔ Volatile values — the error count, the live log path, `doccheck`'s numbers, STATE's byte
size — are read with a command **every time**. Never quote one from this file.

## 8 · Read path, scope and stop conditions

**Read these files, not these folders:** `docs/agent/bugs/C93.md` ·
`docs/agent/FIX_POLICY.md` · `docs/agent/WORKFLOW.md` (rules 5a/5b and § Probe hygiene and
§ Writing in a shared tree) · `docs/agent/prompts/perma/HANDOFF_ORCHESTRATOR.md` § 5 traps ·
`CLAUDE.md`. For anything else, look it up: `grep` `docs/agent/bugs/INDEX.md` and
`docs/agent/facts/INDEX.md` by id or keyword — ⛔ never read either INDEX whole. Related
records worth one lookup each: `C42` (stale containers), `C99` (hub passage), `EF-104`.
Archived material needs `rg <term> docs/archive/` on purpose; a default `rg` cannot see it.

**In scope:** Leg A's probe, one pack module plus its registration, the desk suite, the
owner sitting, the C93 update, one report, one checklist item.

**Out of scope, and finding it does not authorise fixing it:** the Origin/`GetAttachSpot`
mechanism (→ C93), `C99`/`C42`, anything in the C95 or C96 lane, any other error class. File
it and move on.

**Stop and report instead of pushing on** when: Leg A cannot identify the object from the
owner's save; the guard's desk suite cannot be made to fail on the pre-fix body (your
falsifier is broken — say so rather than shipping a suite that always passes); the fix
silences the log but the produce does not move; or the owner's save turns out to carry a
second, unrelated cause. ⭐ **A report saying "this brief was wrong about X" is a successful
outcome**, not a failure to deliver.

⚠️ **Peers share this tree and commit every few minutes.** Re-check `git log` and
`git status` before every write, stage exact paths, and commit with a pathspec
(`git commit -F <msgfile> -- <paths>`) — never `-a`, never a bare `-m`. doccheck must be
GREEN before you push.
