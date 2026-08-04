# DERIVATION — independent reading of F11 and F99

Written 2026-08-03 under the chain seal (prompt 1). Everything below is derived
from `ModTools\Src` (game 1.0.7.396349), the archived logs, and the raw readings
quoted in the prompt. Nothing here owes anything to the 2026-08-03 write-ups;
those were not read before this file was committed. **Seal attestation is at the
bottom and it is not clean — read it.**

Line numbers are shipped-Src lines unless prefixed with a repo path.

---

## Seal attestation (stated up front because it is not clean)

**I did not hold the seal completely, and it was not possible to.** Two of the
sealed items are forced into context by rules that outrank my discretion:

1. **`docs/agent/STATE.md`** is a mandatory every-session read (`CLAUDE.md`,
   first paragraph). The seal puts its F11 and F99 paragraphs off-limits. I read
   the file — the whole file, as instructed — before reading this prompt, because
   `CLAUDE.md` is read before any task file. Exposure: STATE.md:39-47.
2. **`git log --oneline -10`** is chain rule 1 and the prompt's own first
   instruction. It prints the subject lines of `787ebcf` and `9ef9efa`, whose
   message bodies the seal puts off-limits. Subject lines are message bodies'
   first line.

**What I was anchored with, exactly**, so the reader can discount accordingly:
that the rider ran and was called settled; the triple `table.find` nil / `#units`
6 / `holder == rocket` true (also quoted in the prompt, so no extra exposure);
the phrase "no demonstrated producer"; that a `TransferToMap` hypothesis was
called refuted by measurement; that the old F11 entry "cited the wrong class in
the wrong file"; that F99 is `cand` with no-cheat reachability unproven; and
787ebcf's subject "the state its fix guards against has no producer".

I did **not** open `F11.md` below `**Fix:**`, `F99.md`, the `PLAYTEST_ARCHIVE.md`
rider section, or `git show` on either commit.

**Honest effect on this document.** The F11 conclusion I reach (no enumerable
producer) is the same one I was anchored toward, so **discount my F11 agreement
heavily** — it is not an independent confirmation and I will not claim it as one.
The parts of this file I do claim as independent are the ones that go *against*
the anchor or were never mentioned by it: the route defect in point 7, the
alternative-states enumeration in point 4, the `OnTransferToMapDone` mechanism in
point 2, the whole of F99, and the counting error in point 9. F99 I had no useful
anchor for beyond "cheat-correlated, unproven" — that derivation is clean.

**Design finding for the chain method itself:** rule 1 (staleness) and the
mandatory STATE.md read structurally defeat rule 11 (the seal). A future sealed
prompt must either name a `git log` form that hides subjects, or seal STATE.md by
extracting the relevant paragraphs into a sealed file before the chain starts.
This is filed as a `CHAIN_METHOD.md` item in the outbox.

---

# F11

## 1. What the stale-passenger branch is, when it runs, what happens if it throws

`Colonist:ExitVehicle` — `Lua\Units\ColonistTransport.lua:540-571`:

```lua
function Colonist:ExitVehicle(vehicle)
	if not self.holder or self.holder ~= vehicle or not IsSameMap(self, vehicle) then
		--abducted by CargoTransporter?
		TrainsLogging.warn(self, "not in train", self.command)
		table.remove(vehicle.units, self)          -- :544
		self:DiscardTransportTicket()
		return
	end
	...
```

`table.remove(list, pos)` takes an integer position. `self` is an object. The
engine does not override `table.remove` — `CommonLua/Core/types.lua` aliases the
stock one (`local remove = table.remove`, used at :146/:157/:163/:175), and the
only redefinitions anywhere are local aliases
(`CommonLua/Classes/CommandObject.lua:8`, `Lua/Buildings/DroneControl.lua:10`,
`CommonLua/Libs/MapGen/BiomeFiller.lua:270`). So the call raises
`bad argument #2 to 'remove' (number expected, got table)`.

The intended API is one line away in the same file:
`table.remove_entry(array, field, value)` — `CommonLua/Core/types.lua:143-148`,
which in its two-argument form is `find(array, value)` then `remove(array, i)`.
The engine itself uses the correct call for exactly this list:
`Holder:OnExitHolder` does `table.remove_entry(self.units, unit)`
(`Lua\Buildings\Holder.lua:37`).

**When it runs.** `ExitVehicle` has exactly one shipped caller:
`Lua\Units\Train.lua:447`, inside `Train:UnloadTrain`'s destructor —
`colonist:SetCommand("ExitVehicle", self)`. **It is a command, not a direct
call.** (This matters for point 13; I verified it rather than assuming it.)

**What happens if it throws.** The throw is inside the colonist's command thread,
so it kills that thread, not the train's. Two consequences, and the second is the
player-visible one:

- `self:DiscardTransportTicket()` (:545) never runs → the colonist keeps a
  `transport_ticket` forever.
- The colonist is never removed from `vehicle.units`. `Train:UnloadTrain`
  (`Train.lua:441-453`) has already decremented its optimistic
  `remaining_passengers` for this colonist (:448) and then blocks:

```lua
while #self.units > remaining_passengers do
	Sleep(100)
end
```

`#self.units` can never fall to `remaining_passengers`, because the only thing
that would have removed this colonist is the call that just raised. **The
destructor spins forever and the train never leaves the platform.** That is the
reported symptom, and the mechanism is exact.

Note the fix's own removal is not what unblocks the loop in the *repaired* world:
`table.remove_entry` at :544 does it directly. So the fix is sufficient.

## 2. What actually happens to `vehicle.units` on `SetCommand("EnterTransporter", holder)`

Full chain, followed step by step:

1. `Colonist:EnterTransporter(transporter)` — `Lua\Units\Colonist.lua:4163-4166`
   — `self:SetDome(false)` then `Unit.EnterTransporter(self, transporter)`.
2. `Unit:EnterTransporter(transporter)` — `Lua\Units\Unit.lua:1198-1212`:
   - `SelectionRemove` if selected;
   - **`if transporter:GetMap() ~= self:GetMap() then self:TransferToMap(transporter) end`** (:1202-1204);
   - `SetPos` fallback if the position is invalid;
   - **`self:SetHolder(transporter)`** (:1209);
   - `UpdateOutside`, `Disappear("keep in holder", ...)`.
3. `Unit:SetHolder(building)` → `Unit:SetHolderOnMap(building, self:GetMap())` —
   `Unit.lua:702-721`:

```lua
local holder = self.holder
if holder == building or building and not building:IsKindOf("Holder") then return end
if holder then holder:OnExitHolder(self) end
self.holder = building
if building then building:OnEnterHolder(self) end
```

4. `Holder:OnExitHolder(unit)` — `Holder.lua:36-41` —
   `table.remove_entry(self.units, unit)`.

**So yes: something removes the colonist from `train.units`, and it uses the
correct API — `table.remove_entry`, via `Holder:OnExitHolder`.**

**But in the cross-map case that is not the call that does it.** `TransferToMap`
(:1203) runs *first*, and the C-side transfer fires
`Unit:OnTransferToMapDone` — `Unit.lua:846-851`:

```lua
function Unit:OnTransferToMapDone(old_map)
	-- Some holders move together will its contents
	if self.holder and not IsSameMap(self.holder, self) then
		self:SetHolder(false)
	end
end
```

`SetHolder(false)` → `SetHolderOnMap(false, ...)` → `holder:OnExitHolder(self)` →
removed. By the time `Unit:EnterTransporter` reaches its own `SetHolder` at
:1209, `self.holder` is already `false` and the train's list is already clean.

**This is the mechanically important finding of point 2, and it is the thing that
makes the F11COUNTER reading weaker than it looks: the cross-map abduction and
the same-map abduction clean `train.units` by two *different* calls.** The
measured sitting was cross-map (step 4 printed `col:GetMap() == MainMap -> false`
against `rocket:GetMap() == MainMap -> true`), so it exercised the
`OnTransferToMapDone` path. The same-map path — `SetHolder(transporter)` at
:1209 doing the removal — was **not** measured. Both are correct by reading; only
one was observed.

`OnEnterHolder` (`Holder.lua:27-34`) then appends to the rocket's `units`, which
is where `holder == rocket` in step 6 comes from.

## 3. Whether the cross-map case differs from the same-map case, and why

Yes, in three ways:

| | same map | cross map |
|---|---|---|
| removal call site | `EnterTransporter:1209` `SetHolder(transporter)` | `OnTransferToMapDone:849` `SetHolder(false)` |
| `self.holder` when :1209 runs | the train | already `false` |
| city labels | unchanged | `CityObject:OnTransferToMap` → `AutoRemoveFromCityLabels`; `OnTransferToMapDone` → `self.city = new_map.City` + `AutoAddToCityLabels` (`Lua\CityObject.lua:70-81`) |

Both end with the colonist absent from `train.units` and `holder == transporter`.
The *reason* they differ is `SetHolderOnMap`'s `assert(not building or
building:GetMap() == map)` (:705): a holder and its unit must agree on the map,
so the engine has to break the old holder link during the transfer rather than
after it.

**Consequence for the guard:** `not IsSameMap(self, vehicle)` — the third
disjunct — is precisely the state `OnTransferToMapDone` exists to prevent. Any
map transfer of a colonist whose holder is a train self-heals into
`not self.holder` instead, and `not self.holder` also cannot coexist with
membership in `train.units`, because the same `SetHolder(false)` call did both.

## 4. ⚠️ Whether `F11COUNTER nil 6 true` supports "the branch cannot fire"

**It does not, and this is the point I want to be loudest about.**

The triple is a *necessary* consequence of "this particular abduction left no
stale entry". It is not *sufficient* for "the branch cannot fire", for reasons
that fall into three groups.

### (a) It is one negative instance of one of two paths

Per points 2 and 3, the same-map abduction removes via a different call. The
measurement is silent on it. It is also silent on every non-abduction route
(point 8). A single negative instance of one path cannot support a universal.

### (b) Other states of the world that produce exactly `nil 6 true`

Enumerated deliberately, since the prompt asks for this specifically. All of
these print the same triple:

1. **The intended state** — `OnExitHolder`/`OnTransferToMapDone` removed the
   colonist. (What everyone assumes.)
2. **`SMRF11_train.units` is a different table than the one step 2 read.**
   `Holder:KickUnitsFromHolder` (`Holder.lua:11-25`) sets `self.units = nil`, and
   `OnEnterHolder` then rebuilds it as a fresh `{unit}`. If the train reached a
   station, unloaded and reloaded between step 2 and step 7 — the sitting spanned
   at least 6 console commands of wall-clock — `table.find` is `nil` trivially and
   proves nothing about the abduction. `#units == 6` is consistent with a busy
   line refilling. **Nothing in the printed evidence excludes this.** A print of
   the table's identity, or of `#units` immediately before step 6, would have.
3. **The colonist was removed by the destructor of the interrupted `BoardVehicle`
   command rather than by the abduction.** `SetCommand` interrupts `BoardVehicle`
   (`ColonistTransport.lua:503-528`); its `while self.holder == vehicle` loop at
   :525 exits on its own once the holder changes. Same visible triple, different
   cause; distinguishing them matters because the interrupted-command route is
   not available to non-`SetCommand` producers.
4. **`SMRF11_col` was aboard a train other than `SMRF11_train`** by step 7. Step 1
   boarded it onto `SMRF11_train`, but `#units == 6` is the only evidence tying
   the two together at step 7, and 6 is not an identifier.
5. **A transient window closed before the read.** The triple is a post-hoc
   snapshot. Between `TransferToMap` (:1203) and `SetHolder` (:1209) there is a
   window in which the colonist is on the rocket's map with — if
   `OnTransferToMapDone` had not fired — `holder == train`. I believe
   `OnTransferToMapDone` closes it, but a post-hoc read cannot demonstrate that;
   it would look identical either way.
6. **`table.find` returning `nil` for a reason unrelated to removal.**
   `table.find(list, value)` on a list that has had `nil` holes punched in it by a
   raw `table.remove` elsewhere would stop early. No such producer found, but the
   triple does not exclude it.

### (c) The strongest form the evidence supports

> *In one observed cross-map `SetCommand("EnterTransporter", <rocket>)` on a
> colonist aboard a train, `train.units` was not left with a stale entry.*

Everything beyond that sentence is inference. In particular **"the branch cannot
fire" is not supported and the prompt is right to forbid claiming it.** What the
reading *does* legitimately do is refute the specific hypothesis that this
abduction is a producer — that is a real result and it is worth having.

## 5. Whether the hand call is a faithful stand-in for crew-gathering

**Faithful for the last leg, not for the selection.** The real path is
`CargoTransporter:ExpeditionLoadCrew` — `Lua\Buildings\CargoTransporter.lua:298-302`:

```lua
function CargoTransporter:ExpeditionLoadCrew(crew)
	for _,unit in ipairs(crew) do
		unit:SetCommand("EnterTransporter", self)
	end
end
```

That is *literally the same call*, so from `SetCommand` onward the stand-in is
exact — same command, same argument kind (the transporter itself), same
interrupt semantics. Confirmed by reading, not assumed.

What the hand call skips is everything **before** it:

- `GatherAvailableColonists` (`CargoTransporter.lua:237-296`) does the selection,
  including the `thread_running_destructors` filter (:252-260) and the
  idle-before-busy ordering (:262-285). A hand call bypasses all of it, so it
  cannot tell you whether *this* colonist would ever be picked.
- The loop calls `SetCommand` on **many** colonists in immediate succession, in
  one thread, with no `Sleep` between. The hand call does one. If a producer
  needs two colonists off the same train in the same tick — e.g. an interleaving
  with `Train:UnloadTrain`'s `ripairs(self.units)` walk over a list being mutated
  — a single hand call cannot reproduce it. **This is the one substantive
  fidelity gap and it is not closed by the reading.**

## 6. Whether the step-3 pool rebuild reproduces `GatherAvailableColonists`' pool

Shipped, `CargoTransporter.lua:237-251`:

```lua
local colonists = self.city.labels.Colonist
local connected_cities = GetConnectedCitiesForColonists(self.city)
local copied = false
for _, city in ipairs(connected_cities) do
	local city_colonists = city.labels.Colonist
	if not copied then colonists = table.copy(colonists); copied = true end
	table.iappend(colonists, city_colonists)
end
```

Console:

```lua
local pool = table.copy(MainCity.labels.Colonist)
for _, c in ipairs(GetConnectedCitiesForColonists(MainCity) or empty_table) do
	table.iappend(pool, c.labels.Colonist)
end
```

**Diff:**

| # | shipped | console | matters? |
|---|---|---|---|
| 1 | `self.city` (the rocket's city) | `MainCity` hard-coded | **Unverified.** `rocket.city == MainCity` was never printed. Step 4 printed `rocket:GetMap() == MainMap -> true`, and `CityObject:Init` asserts `self.city:GetMap() == map`, so `rocket.city == MainMap.City`; that equals `MainCity` only if `MainCity == MainMap.City`, which is conventional but is an assumption, not a reading. |
| 2 | copies only when there is a connected city | always copies | no |
| 3 | `or empty_table` guard | shipped has none | no (cosmetic) |
| 4 | **then filters** `thread_running_destructors` (:252-260) | absent | **yes** |
| 5 | **then partitions idle/`Abandoned` before busy** (:262-285) | absent | **yes** |
| 6 | **then `FilterColonistsByTrait` and truncates to `amount`** (:270-291) | absent | **yes** |

So the console line reproduces **the raw pool only, not the selection.** Rows
4-6 are the entire selection logic. A colonist with `command == "BoardVehicle"`
is in the *busy* bucket (:274-279) and is reached only when the idle bucket is
short of `amount`.

**Verdict: the rebuild is a faithful reproduction of steps 1-2 of a six-step
function.** Membership in the raw pool is established. Selectability is not, and
`#pool 1543 / find 1513` says nothing about selectability — the index is a
position in an unfiltered concatenation, and the shipped code never uses that
ordering.

## 7. ⚠️ The unverified premise: can an underground colonist be in `MainCity.labels.Colonist`?

**The premise is TRUE. The route offered for it is WRONG. Both halves matter.**

### The premise is true

`Lua\CityObject.lua`:

```lua
function CityObject:Init()          -- :11-17
	local map = self:GetMap()
	if not self.city then self.city = map.City end
	assert(self.city:GetMap() == map)
end
function CityObject:OnTransferToMap(old_map)      -- :79-81
	self:AutoRemoveFromCityLabels()
end
function CityObject:OnTransferToMapDone(old_map)  -- :70-77
	local new_map = self:GetMap()
	assert(self.city ~= new_map.City)
	self.city = new_map.City
	self:AutoAddToCityLabels()
end
```

`Colonist:AddToCityLabels` / `RemoveFromCityLabels`
(`Lua\Units\Colonist.lua:272-311`) both act on `self.city`, and `city:AddToLabel
("Colonist", self)` is the only route into the label. So label membership tracks
`self.city`, which tracks the map, maintained on both edges of every transfer.
An underground colonist has `city == <underground map>.City ~= MainCity` and is
therefore not in `MainCity.labels.Colonist`.

**Caveats I will not suppress.** (a) `SavegameFixups.FixCityLabels2`
(`CityObject.lua:89-116`) exists specifically to repair objects whose `city` does
not match `map.City`, and prints a per-class count when it finds any — the
invariant has demonstrably been violated in shipped saves. (b) `ManualCityLabels`
(:83-87) opts subclasses out of the automatic maintenance entirely; `Colonist` is
not one, but the mechanism exists. (c) `Unit:EnterTransporter` passes
`transporter.keep_cargo_in_labels and "keep_in_labels"` to `Disappear`
(`Unit.lua:1211`), so cargo can deliberately stay in labels after boarding. None
of these overturn the premise for the measured colonist; all three mean it is a
*maintained* invariant rather than a structural impossibility, so "cannot" is
too strong. "Does not, unless a known-buggy state exists" is right.

### The route is wrong

The inference offered was:

> index 1513 in a pool of 1543 ⟹ it came from the connected-cities append ⟹ the
> colonist is underground.

**That inference requires `#MainCity.labels.Colonist < 1513`, and that number was
never printed.** The console line printed `#pool` and `table.find(pool, col)` and
nothing else. If MainCity held 1520 colonists, index 1513 sits inside MainCity's
own block and the conclusion reverses. The reading does not contain the quantity
its own argument depends on.

The conclusion survives anyway, because **step 4 already measured it directly**:
`SMRF11_col.city == MainCity -> false`. Combined with the label invariant above,
`col ∉ MainCity.labels.Colonist` follows immediately, with no reference to index
positions at all.

**This is the project's signature failure exactly as `CLAUDE.md` and chain rule 6
describe it: every cited number is correct, the conclusion is correct, and the
route from one to the other is unsupported.** The index argument should be struck
and replaced with the step-4 argument. Anyone who later re-uses "1513 proves
underground" as a lemma will be reasoning from nothing.

## 8. Anything OTHER than crew-gathering that can leave a stale entry in `vehicle.units`

### What I searched

- Every write to `.units` in the tree: `grep -rn "\.units"` across `Lua/` and
  `CommonLua/`, then every hit in `Train.lua`, `ColonistTransport.lua`,
  `Holder.lua`, `Unit.lua`.
- Every direct assignment to a unit's holder that bypasses `SetHolderOnMap`:
  `grep -rn "\.holder = "` across `Lua/` and `CommonLua/`.
- Every `SavegameFixups.*` touching holders or city labels.
- `Holder`, `Unit:KickFromBuilding`, `Unit:ExitBuilding`, `Unit:Disappear`,
  `Unit:OnTransferToMap`/`Done`.

### What I found

**The list is maintained in exactly two places** —
`Holder:OnEnterHolder`/`OnExitHolder` (`Holder.lua:27-41`) — and both are reached
only through `Unit:SetHolderOnMap` (`Unit.lua:702-717`). So a stale entry
requires either a direct holder write or a direct `units` write.

**Direct holder writes that bypass `OnExitHolder` — four in the tree:**

| site | what it does | is it an F11 producer? |
|---|---|---|
| `Lua\Passage.lua:1055` `unit.holder = nil` | comment: *"last el would be holder, no need to exit we are already out"* | **No — but it is a real defect of the identical shape.** See below. |
| `Lua\Units\Colonist.lua:4305` `u.holder = false` (`SavegameFixups.UnitsInInvalidHolder`) | guarded by `if not u.holder or IsValid(u.holder) then return end` — only ever clears an **invalid** holder | No. An invalid holder has already run `Holder:Done` → `KickUnitsFromHolder` → `self.units = nil`, so there is no list to be stale in. |
| `Lua\Units\Train.lua:390` `self.holder = nil` | the **train's own** holder, not a passenger's | No. |
| `Lua\Buildings\SurfaceDeposit.lua:154/426` `group.holder` | unrelated field on a deposit group | No. |

**Direct `units` writes:** only `Holder:KickUnitsFromHolder` (`self.units = nil`,
`Holder.lua:13`) and `Holder:OnEnterHolder`'s lazy create (:32). `KickUnitsFromHolder`
produces the *opposite* desync — holder points at a train whose list is gone —
which would make `Train:UnloadTrain`'s `#self.units` throw, not `ExitVehicle`'s.

**`Unit:ExitBuilding` (`Unit.lua:385-392`)** is worth naming because it is the
only place the engine explicitly repairs the `IsSameMap` disjunct:

```lua
assert(IsSameMap(building, self))
if not IsSameMap(building, self) then
	if self.holder == building then
		self:SetHolder(false)   -- "The unit is in invalid state so we want to remove the holder"
	end
	return
end
```

The assert plus the comment are the developers documenting that
`holder == building` with different maps **does occur**. They repair it here.
`ExitVehicle` does not get that treatment; it gets the broken `table.remove`
instead.

### Verdict

**I found no producer of a stale `train.units` entry in the shipped source.**
Every path that changes a colonist's holder or map routes through
`SetHolderOnMap` or `OnTransferToMapDone`, and both call `OnExitHolder`.

I say that as *"I looked here and found none"*, listing where I looked, exactly
as the prompt permits. I explicitly do **not** conclude the branch is
unreachable, and I note three things that keep the question open:

1. **The devs wrote the guard.** `--abducted by CargoTransporter?` is someone
   describing a state they had seen. It may have been reachable in an earlier
   build and closed since — `Unit:OnTransferToMapDone` reads exactly like the
   closing patch. That is a hypothesis about history, not a reading.
2. **Savegame carry-over.** `Holder.units` is a persisted class member
   (`Holder.lua:3`). A save written by an older build, or by another mod, can
   carry a desync that no current code path can create. `SavegameFixups.UnitsInInvalidHolder`
   and `FixCityLabels2` both exist because that has happened before.
3. **Other mods.** Any mod that assigns `.holder` directly — as the shipped
   `Passage.lua:1055` does — creates the state.

### ⚠️ Discovered en route: `Passage.lua:1055` is the same defect on a different Holder

`PassageBase:TraverseTunnel` (`Lua\Passage.lua:1037-1066`) walks a colonist
through passage elements via `el:LeadIn(unit, entrance)`, then does
`unit.holder = nil` directly. The last element's `units` list still contains the
unit. That is a genuine stale-`units` entry on a live Holder, produced by shipped
code every time a colonist traverses a passage.

Consequence: when that element is destroyed, `Holder:KickUnitsFromHolder`
(`Holder.lua:11-25`) iterates the stale entry and calls
`unit:KickFromBuilding(self)` on a colonist who left long ago —
`Detach`, `ClearPath`, `SetPos(<passage exit>)`, `SetHolder(false)`,
`SetCommand("Idle")` (`Unit.lua:276-286`). **Teleporting an unrelated colonist to
the demolished passage and cancelling whatever they were doing.** It also fires
`assert(IsValid(unit))` and the "Probable destructor interuption" assert (:18-19).

This is not F11 and this chain does not own it. **Routed as a new `cand`
entry — see the outbox.** I have not verified it against a live game and it is a
reading only.

---

# F99

## 9. What exactly is nil at `TrackElement.lua:805`, and why

`TrackConstructionSite:Complete(quick_build)` — `Lua\Buildings\TrackElement.lua:744-822`.
The failing block, verbatim:

```lua
789		DoneObject(self)
790		element:ApplyToGrids()
...
795		ExpandTrackFromElement(element.track_obj, element)
796
797		if #element.track_obj.elements_under_construction == 0 then
798			local track_obj = element.track_obj
799			g_ConstructedTracksQueue[track_obj] = GameTime() + 500
800			if not self.broken then
801				local el1, el2 = self.track_obj.start_el, self.track_obj.end_el
802				ProcessTrackElements(ResolveMap(self.track_obj), self.track_obj.elements)
803				local start_el = self.track_obj.elements[1]
804				local end_el = self.track_obj.elements[#self.track_obj.elements]
805				start_el:AutoConnectTracks()
806				end_el:AutoConnectTracks()
807				track_obj = start_el.track_obj
808			end
```

### What is nil

`start_el`, i.e. `self.track_obj.elements[1]`.

**`self.track_obj.elements` is a live table with `#elements == 0`.** This is
forced by the error message, not assumed: if `elements` were `nil` or `false`,
line **803** would have thrown on indexing it and the message would name
`field 'elements'`. It names `local 'start_el'` at **805**, so 803 and 804 both
completed and returned `nil`. (F48 records that `#nil == 0` is true in this
engine at `Tracks.lua:808`, which is why `ProcessTrackElements` at 802 returns
immediately and does not throw either way.)

### Why it is empty — the part I can prove

The block mixes two different track objects. **797-799 use
`element.track_obj`. 801-804 use `self.track_obj`.**

For a **new build** they are the same object and the list *cannot* be empty:

- `element` is created at :762 as `TrackGridElement:new({ ..., track_obj = track, ... }, track)` where `track = self.track_obj` (:761/:767);
- `TrackGridElement:Init` (:176-180) runs during `:new()` and does
  `table.insert_unique(self.track_obj.elements, self)` — `element.is_construction_site`
  is false, so it lands in `elements`, not `elements_under_construction`;
- `DoneObject(self)` at :789 removes only *self* and only from
  `elements_under_construction` (`:181-192`; the auto-delete at :203 is skipped
  because `self.is_construction_site` is true);
- `ExpandTrackFromElement` (:714-742) only ever **adds** to
  `element.track_obj.elements` (:731) — its `found` set is by construction the
  elements whose `track_obj ~= element.track_obj` (:699-701).

So `element` itself is in the list at 803. **The new-build path cannot produce
this error.** That is a proof by construction and it is the load-bearing step.

⟹ **The failure requires `self.track_obj ~= element.track_obj`.**

⟹ And `element` is something other than a fresh element on `self.track_obj` in
exactly one place — :762:

```lua
local element = IsValid(self.broken) and self.broken or TrackGridElement:new({...}, track)
```

**the repair-of-a-broken-element branch.**

### The dead guard — the root cause

Line 800 is `if not self.broken then`. That guard exists to skip 801-807 for
repair completions. **It never does**, because :772-774 already cleared it:

```lua
772	if IsValid(self.broken) then
773		element.broken = nil
774		self.broken = nil          -- <-- the guard at :800 is now always true
775		element:SetVisible(true)
776	else
```

After the `if/else`, `self.broken` is `nil` in the repair branch and `false` in
the new-build branch. **`not self.broken` is unconditionally true at line 800.**

So repair completions fall into a block written on the assumption that
`self.track_obj` still owns `element` — and in the repair case `element` is a
pre-existing element that may since have been reassigned to another track, while
`self.track_obj` is left holding nothing once the repair site is removed at
:789.

Corroborating fingerprint: **`el1, el2` at line 801 are computed and never
used.** Dead locals that capture `start_el`/`end_el` *before* `ProcessTrackElements`
— almost certainly what 805-806 were originally meant to call. This block is a
half-finished refactor.

### How the two tracks diverge — hypothesis, NOT proven

`TrackBase:BreakTrackElement` (`Lua\Buildings\Track.lua:618-659`) sets
`params.track_obj = self`, so the repair site and the broken element start on the
same track. They diverge later, when a merge reassigns `track_obj` —
`AutoConnectTracks` (`TrackElement.lua:394-409`) or `ExpandTrackFromElement`
(:720-741), both of which walk the **object hex grid** via
`HexGetTrackGridElement`. The broken element and its repair site occupy the *same
hex* (`PlaceConstructionSite(..., element:GetPos(), ...)`, `Track.lua:636`), and
the hex grid returns one object per hex — so a merge can reassign one of the pair
and not the other.

**I cannot verify `HexGetTrackGridElement`'s tie-break from source (it is a C
binding), so I am naming this as the leading hypothesis and not as a finding.**
The proven part — repair branch required, guard dead — stands without it.

### Corroboration from the logs

`CaveIn` appears in both `Mars.exe-20260803-*.log` files and
`BreakTrackElement` appears in `MarsDebug.exe-20260803-23.14.05-*.log`. Cave-ins
break track elements underground, which is exactly what creates repair sites in a
cheat-built underground setup. **The repair-branch thesis is consistent with the
same sitting's own log**, which is as close to a control as this chain can get
without a keyboard.

### ⚠️ The count is wrong: 7 throws, not 14

`grep -c "TrackElement.lua:805"` on
`Mars.exe-20260803-21.18.38-6a22b86d.log` returns 14, and that is where the
figure came from. The 14 lines are **7 pairs**:

```
333:[LUA ERROR] Lua/Buildings/TrackElement.lua:805: ...
363:Error calling Lua function "exec" from C: Lua/Buildings/TrackElement.lua:805: ...
364:[LUA ERROR] ...
393:Error calling Lua function "exec" from C: ...
   (…425/454, 456/485, 486/515, 517/546)
```

Seven `[LUA ERROR]` headers, seven matching C-side `Error calling Lua function
"exec" from C` reports of the same throw. The other two archived logs contain
zero.

**The correct figure is 7.**

### Bonus, and it changes the picture: the errors came out of the CONSOLE

`Error calling Lua function "exec" from C` means each throw propagated out of a
console `exec`. Combined with the stack (`Cheats.lua(126): global
CheatCompleteAllConstructions`), that is seven separate console invocations, each
aborted. See point 10.

## 10. Where execution stops, what is left undone, and the `F99RESIDUE 0 0` reconciliation

### Left undone inside `Complete`

- :806 `end_el:AutoConnectTracks()`
- :807 `track_obj = start_el.track_obj`
- :809-813 — `if #track_obj.elements_under_construction == 0 then table.clear(element.track_obj.repair_cgs); Msg("TrackBroken", element.track_obj, false) end`
- :815-820 the reselect thread
- :821 `return element` → the caller gets nothing

### Left undone outside `Complete`

The throw is **not** caught. It unwinds through `ConstructionSite:Complete`
(`ConstructionSite.lua:2483`), through `[C] MapForEach`, out of
`CheatCompleteAllConstructions` (`Cheats.lua:126`) and out of the console `exec`.
Therefore:

- **every remaining construction site in that `MapForEach` pass is never
  completed**, and the second `for i=1,2` pass never runs;
- **`CurrentMap:ResumeTerrainInvalidations("cheat_all_constructions")`
  (`Cheats.lua:128`) never runs**, leaving a suspend leaked — seven times over
  the sitting. This is tag-scoped to the cheat, so it cannot affect a player who
  does not use it, but within the sitting it is real engine state left wrong.

### Is there persistent damage?

**Mostly no, and the reason is a genuinely lucky ordering.**
`g_ConstructedTracksQueue[track_obj] = GameTime() + 500` is set at **:799**,
*before* the throw. The `ConstructedTracksCheck` repeater
(`TrackElement.lua:677-693`) then runs 500 ms later and does the *same work* with
the guards this block is missing:

```lua
if IsValid(track) and GameTime() > time and #track.elements_under_construction == 0 then
	if #track.elements > 0 then
		track.elements[1]:AutoConnectTracks()
		if #track.elements > 0 then -- because AutoConnectTracks can delete these
			track.elements[#track.elements]:AutoConnectTracks()
		end
		track:TryConnectStations()
	end
```

**The auto-connect self-heals.** That the engine's own repeater is a correctly
guarded copy of lines 803-806 is also the clearest possible statement of what the
fix should be.

What does **not** self-heal is `table.clear(element.track_obj.repair_cgs)` and
`Msg("TrackBroken", element.track_obj, false)` at :811-812. `repair_cgs` is a
persisted class member (`Track.lua:41`) and a non-empty one means:
`TrackBase:CanDelete`-style check at `Track.lua:372` returns false (**the track
cannot be deleted**), `Track.lua:382` reports it as damaged in the UI,
`UnderconstructionSign.lua:168` and `Station.lua:708` keep flagging it, and
`ipTrack.generated.lua:34` keeps listing repair groups. **A track stuck showing
damage forever and refusing to be salvaged.**

### Reconciling with `F99RESIDUE 0 0`

The probe:

```lua
for _, c in ipairs(Cities) do for _, t in ipairs(c.labels.TrackBase or empty_table) do
  if #(t.elements or empty_table) == 0 then a=a+1 end
  if t.repair_cgs and #t.repair_cgs > 0 and #(t.elements_under_construction or empty_table) == 0 then b=b+1 end
end end
```

Three reasons `0 0` is the *expected* reading even if the damage were real, so it
must not be read as "harmless":

1. **It ran after a reload.** `SavegameFixups.RebuildBrokenTracksAndConnect`
   (`TrackElement.lua:824-837`) walks every track on load doing precisely
   `elements[1]:AutoConnectTracks()` / `elements[#elements]:AutoConnectTracks()`
   / `TryConnectStations()` — with `#track.elements > 0` guards. Probe (a) is
   measuring a world that has already been swept.
2. **Probe (a) measures the wrong object.** An emptied `self.track_obj` is a
   `TrackBase` with no elements; whether such a husk survives a save/load round
   trip is untested. If it does not, `a == 0` is guaranteed regardless.
3. **Probe (b)'s damage only exists in the repair case, and `repair_cgs` is only
   ever populated by `Meteors.lua:609` and `TrainDisasterHandling.lua:58-59`.**
   In a cheat-built underground setup with cave-ins but no meteor repair groups,
   `repair_cgs` was empty to begin with, so :811-812 were no-ops and there is
   nothing for probe (b) to find.

**Verdict: `F99RESIDUE 0 0` is consistent with the defect being real and is not
evidence that it is harmless.** It is a null result from a probe run after the
one event most likely to erase what it was looking for. If it is to mean
anything it must be re-run **before** a reload, in a colony that has meteor or
cave-in repair groups outstanding.

## 11. Is `quick_build` / the cheat load-bearing?

**`quick_build` is not.** It is consumed once, at :748-750
(`if quick_build then self:OnQuickBuild() end`), hundreds of lines above the
failing region, and nothing in 761-822 reads it.

**The cheat is not load-bearing for the code path.** `TrackConstructionSite:Complete`
is the same method a drone-built site reaches; `CompleteBuildConstructionSite`
(`Cheats.lua:113-117`) calls `site:Complete("quick_build")` on construction-group
leaders, and normal completion calls the same `ConstructionSite:Complete`.

**The cheat is load-bearing for the frequency, and plausibly for the
configuration.** `MapForEach("map", "ConstructionSite", ...)` completes every
site on the map in **map order, in one tick, with objects being created and
destroyed during the iteration**, twice over. Normal play completes sites one at
a time in build order with drone work between them. The repair/merge interleaving
the failure needs is far likelier under the cheat.

**What a non-cheat path would need:** a repair construction site
(`self.broken` valid, from a meteor strike or a cave-in) completing normally, at
a moment when its `track_obj` no longer holds the element being repaired. I can
point at no shipped line that guarantees that arises, and I cannot rule it out.

**Per the prompt's own instruction: UNPROVEN. I will not claim either way.**
What I *will* claim, and this is stronger than what the cheat correlation
suggests, is that **the branch is entered on every repair completion, cheated or
not** — because the guard at :800 is dead. Whether it *throws* depends on the
track configuration; whether it is *entered* does not.

## 12. Is this already covered by an existing entry?

Checked, not assumed. `grep -rln "TrackConstructionSite:Complete" docs/agent/bugs/`
returns only `F99.md` and the generated `INDEX.md`.

- **F44** — *One-hex track salvage can delete the entire track.*
  `Construction.lua:2910` → `DemolishAndSplitTrack` (`TrackElement.lua:444-578`),
  whole-track `OnDemolish` fallbacks. Same file, different function, salvage not
  completion. **Not a duplicate.**
- **F45** — *Damaged tracks can't be salvaged (sort crash).*
  `BreakTrackElement` fails to copy `node_idx` → `table.sort` comparison error at
  `TrackElement.lua:458-464`. **Adjacent and worth noting**: F45 is about the
  *same* `BreakTrackElement` that creates the repair site my F99 route depends on,
  and F45's fix stamps `element.broken.node_idx`. Different symptom, different
  line, no overlap in the fix. **Not a duplicate**, but F99 and F45 should
  cross-reference: both are consequences of the repair-site construction being
  under-specified.
- **F48** — *Station-connector savegame fixup no-op (paren misplaced),*
  `Station.lua:1346`. Different file. **Not a duplicate.** Its recorded finding
  that `#nil == 0` holds at `Tracks.lua:808` is load-bearing for my point 9 and I
  have used it as such — flagged here because chain rule 6 says recorded facts are
  claims too, and I did not re-derive it.
- **`C12-C38.md`** — no hit for `805`, `start_el`, or
  `TrackConstructionSite:Complete`.

**F99 is not covered by an existing entry.**

---

# The proposed code change

## 13. Is the pre-wrapper conversion behaviour-preserving and safe here?

**Yes on all three counts, and it is the better shape. One caveat and one
correction to how it should be built.**

### Shape

```lua
local orig = Colonist.ExitVehicle
function Colonist:ExitVehicle(vehicle)
	if not self.holder or self.holder ~= vehicle or not IsSameMap(self, vehicle) then
		TrainsLogging.warn(self, "not in train", self.command)
		table.remove_entry(vehicle.units, self)
		self:DiscardTransportTicket()
		return
	end
	return orig(self, vehicle)
end
```

### Is it behaviour-preserving?

**Yes.** Condition true → we run the repaired branch and return; `orig` is never
entered. Condition false → `orig` re-evaluates the identical condition, finds it
false again, and proceeds down the untouched shipped path.

### What breaks if the condition is evaluated twice?

**Nothing.** The three clauses read `self.holder`, compare it to `vehicle`, and
call `IsSameMap(self, vehicle)`. All pure reads, no side effects, no allocation,
no message. The wrapper's call to `orig` is a direct Lua call with no yield
between the two evaluations, so no other thread can run and no value can change.
`IsSameMap` is a realm query (`CommonLua/LuaExportedDocs/Game/realm.lua:95`) —
observational.

The cost is two extra table reads and one C call on the normal path, once per
passenger per station stop. Irrelevant.

### Is a pre-wrapper safe on *this* method specifically? — `EF-012`

**`EF-012` applies and it is the reason the wrapper must be a PRE-wrapper.** It
records: *"A post-wrapper on a command method (anything ending in `SetCommand`)
never runs — `DoSetCommand` kills the calling thread. `Colonist:Idle` must be
pre-wrapped (F73)."*

**`ExitVehicle` is a command method, and I verified that rather than assuming
it.** Its sole shipped invocation is `colonist:SetCommand("ExitVehicle", self)`
at `Lua\Units\Train.lua:447` — I grepped `ExitVehicle` across the whole tree and
that is the only call site. And its normal path ends in
`self:PopAndCallDestructor()` (:570) whose destructor tail is
`CommandObject.SetCommand(self, ticket.reason, ...)` or
`self:SetCommand("Idle", true)` (:562/:564) — self-directed `SetCommand`, which
per `EF-012` does not return.

Two consequences:

1. **A post-wrapper would be silently dead here.** Anyone converting this module
   later must not reach for one. Worth a sentence in the module header.
2. **`return orig(self, vehicle)` never returns in the delegated case** — and
   that is fine, because a pre-wrapper puts nothing after the call. It is also a
   proper Lua tail call, so no frame is retained.

### The caveat: idempotence

The full-copy form is idempotent — applying twice re-assigns the same closure. A
pre-wrapper is **not**: a second `apply` would capture the first wrapper as
`orig` and nest. Functionally harmless (the branch returns before delegating, and
a false condition just costs a second identical evaluation), but it is a real
difference in a property the current file has for free. **Prompt 2 should confirm
how `SMRFixPack.Register`/`apply` guarantees single application before shipping
the conversion** — I did not audit the loader and will not assert it is safe.

### The correction: `Require` must change with it

`Code/Fix_TrainPlatformWedge.lua:23-27` currently requires
`{ path = { "const", "Scale", "Stat" } }`. The pre-wrapper does not use
`stat_scale`, so that requirement — and the `local stat_scale = const.Scale.Stat`
line — should be dropped, or it will keep gating the fix on a symbol the fix no
longer touches. `table.remove_entry` and the `Colonist:ExitVehicle` method check
both stay.

### One thing the conversion does *not* fix

`table.remove_entry(vehicle.units, self)` is correct, but the branch still
assumes `vehicle.units` exists. If the train ran `KickUnitsFromHolder`
(`Holder.lua:13` sets `self.units = nil`) the call is `find(nil, self)` — which
per F48's recorded `#nil` behaviour may or may not be tolerated here. Cheap
insurance: `if vehicle.units then table.remove_entry(...) end`. Not required for
the defect; noted for prompt 2's judgement.

## 14. What the full-copy form costs today

The copy at `Code/Fix_TrainPlatformWedge.lua:32-63` freezes shipped
`ColonistTransport.lua:548-570` — every line below the guard. Named, with a
patch-risk read on each:

| shipped line | what it is | could a game patch plausibly change it? |
|---|---|---|
| :548-549 | `station`/`ticket` locals from `self.transport_ticket` | low |
| :550 | `DiscardTransportTicket()` before the destructor | low |
| :551 | `travel_time = GameTime() - ticket.start_wait` | low |
| :553-554 | `SetHolder(station)` + `ExitBuilding(station)` | low, but this is the pair that removes the passenger from `train.units` — a change here is a change to the F11 mechanism itself |
| :555-557 | `if not UIColony:IsTechResearched("LuxuriousTrains")` → `ChangeComfort(0 - MulDivRound(stat_scale, travel_time, const.HourDuration), "travel time")` | **HIGH.** A tuning line: a tech gate, a stat scale and a rate, in one expression. Exactly what balance patches touch. |
| :558-560 | `if vehicle.track and vehicle.track.seen_forest` → `ChangeSanity(TechDef.GreenView.param1, "seen forest")` | **HIGH.** Same reason, plus it reads a `TechDef` param that is itself data-driven. |
| :561-565 | ticket-destination dispatch → `CommandObject.SetCommand(self, ticket.reason, ...)` else `SetCommand("Idle", true)` | medium — plausible place to add a case |
| :567 | `RebuildInfopanel(vehicle.track)` | low |
| :568-569 | `AddSpentTime` on vehicle and track | medium — accounting is a common bug-fix target |

Plus one hazard the table does not show: the copy **recreates the file-local
`stat_scale = const.Scale.Stat`** (`Code/Fix_TrainPlatformWedge.lua:30`,
mirroring `ColonistTransport.lua:1`). If a patch redefines that local's value or
meaning, the copy silently keeps the old one. A file-local is invisible to any
`Require` check — there is no symbol to guard on.

**The concrete cost, then: two balance expressions (comfort penalty, forest
sanity) and one invisible file-local, all frozen at 1.0.7.396349, all of which a
patch could change without any error, warning or `Require` failure. The mod would
quietly serve stale numbers.**

The pre-wrapper's frozen surface is the three-clause condition plus the three-line
branch body — and the branch body is the thing we are deliberately overriding, so
the only *unwanted* freeze is the condition. **That is a strictly smaller and
strictly more visible risk. The conversion is worth doing on these grounds
alone**, independently of anything about reachability.

---

## Summary of what I would tell the owner

1. **F11's fix is right and should ship**, on the merits already decided: the
   shipped call is unambiguously wrong (`table.remove` with a value), the failure
   mode is a permanently wedged train, and the correct API is used for the same
   list four lines away in `Holder.lua:37`.
2. **Convert it to a pre-wrapper.** Behaviour-preserving, `EF-012`-compliant
   (pre, never post), and it un-freezes two balance expressions and a file-local
   that the full copy pins to 1.0.7.396349. Drop the `const.Scale.Stat` require
   with it, and confirm apply-once first.
3. **Do not carry "the branch cannot fire" anywhere.** The measurement supports
   one sentence about one cross-map abduction. I looked for other producers and
   found none *in this build*, which is a different and weaker statement.
4. **Strike the index-1513 argument** and replace it with `col.city ~= MainCity`
   plus the `CityObject` label invariant. The conclusion is right; the route is
   not, and the route is what gets re-used.
5. **F99 is real and is more specific than "a cheat crash".** The guard at line
   800 is dead — killed by line 774 — so every repair completion enters a block
   written to exclude it. Count is 7, not 14. The auto-connect self-heals via
   `g_ConstructedTracksQueue`; the un-run `repair_cgs` clear does not, and that
   one leaves an undeletable permanently-damaged track. `F99RESIDUE 0 0` was
   taken after a reload and cannot see it.
6. **Two things routed out** (details in the outbox): the `Passage.lua:1055`
   holder desync, and the TestKit creating globals `IsNearDome` / `AddAreaRubble`
   from `00_TestCore.lua:172`.
