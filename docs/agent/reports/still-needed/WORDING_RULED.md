# Still-needed wording batch — OWNER-RULED text (2026-09-12)

This is the text the public-surface sweep applies. It supersedes the phrasing in
`SURFACE_PLAN.md` (Codex's verbatim proposal, kept unedited as the record) wherever
the two differ. Rulings by the owner, 2026-09-12, in `smr-bugfixpack-d0`:

- **Retire F37 and F43 (with its F118 rider).** The frozen 1.0.7 build (`v5-game-1.0.7`)
  stays exactly as it is.
- **F21 stays.** On 1.1.0 the inflated duration still feeds `AddSpentTime` on the
  train and the track (`Lua/Units/ColonistTransport.lua:671`, `:696-697`), and that
  number is the **"Travel time (rolling average)"** line on every train and track
  info panel (`Lua/XDef/ipTrain.generated.lua:85`, `ipTrack.generated.lua:186`,
  `Lua/Buildings/Track.lua:601`). Only the Comfort charge is gone from `ExitVehicle`
  (no `ChangeComfort` in `:665-700`). The Comfort claim goes; the fix does not.
- **F31 RETIRES.** ✅ Ruled by the owner **2026-09-12** (checklist 159 (1)) on the deep
  audit's RETIRE verdict (`reports/SURFACE_AUDIT_2026-09-12.md` §2 C1–C6). Was HELD for
  that audit; the hold is discharged. Module out under module-list gate (tools/doccheck.py MODULE SETS + tools/upload_preflight.py), row and headline off, count
  word to **Forty-six**. See item 13 below.
- **F37's load-time clean-up is not rehomed.** ✅ Ruled 2026-09-12 (checklist 159 (2)):
  accept the loss; it does **not** move into `90_SaveSanitizer.lua`.
- **Items 1, 3, 12 and 14 carry replacement text ruled 2026-09-12** (checklist 159 (3),
  "3 all" plus the optional fourth). Each replaced line names its audit finding inline.
- **F52 is HELD** as already ruled (Codex marked it inferred; the row is right).

## ⚖️ Voice rule (owner, 2026-09-12) — binds every public surface from now on

> We are trying to be more dev-friendly, but the public has to understand what we
> are talking about too. Two developers use the fix list; two thousand players and
> rising use the mod. We are not held to a developer's disclosure standard: the
> mod cannot be full of "no guarantees" and "unverified", because that reads as
> no confidence in the product and nobody will want it. If the wording confuses
> the author, it is word salad and it fails.

How to apply it: state scope by saying **what the fix does and for whom**, never by
disclaiming what it does not do. Plain sentences a player would use; precise enough
that a developer reading the row finds the right code. The dated entry in
`agent/bugs/<ID>.md` keeps every limit and caveat; the public row does not carry them.

## The batch — replacement text per item

Line numbers are `content/fix-list.md` in `SMR-CommunityMods` at `a061665`. Only the
lines quoted change; everything else in the row stays.

### 1 · F54 Shuttle hub switched off (`:94`) — approved, polished; **After line replaced 2026-09-12**
- **After the fix:** a hub you switch off stops counting. Only hubs you have left
  switched on count.
- (drops the "Suspensions the game imposes on itself — a dust storm, for instance —
  still count as before" sentence)
- ⚠️ **Replaced on the owner's 2026-09-12 ruling of checklist 159 (3)**, from the
  surface audit's D3/§3 item 1: "on and able to fly" was stronger than the module.
  The strict test is `hub.working or (hub.ui_working and permitted-reason and not
  possible-reason)` (`Code/Fix_ShuttleHubOffAvailable.lua:86`), so a hub the **game**
  has paused — maintenance, exceptional circumstances — still counts, on purpose.
- ✅ **SETTLED 2026-09-12 — it stays dropped, and the audit was wrong about it.**
  The audit (D3) recorded the dropped dust-storm sentence as the **true** one and the
  handoff carried that forward as an open restore-or-drop call. Re-derived from the
  shipped tree instead of inherited: **a dust-stormed Shuttle Hub does not count as
  available transport, before or after this fix.** A storm sets `self.suspended`
  (`Building.lua:518-521` → `BaseBuilding:SetSuspended`), which
  `GetWorkNotPossibleReason` returns (`BaseBuilding.lua:635-637`) — a not-POSSIBLE
  reason — while `GetWorkNotPermittedReason` (`:657-663`) returns only `"TurnedOff"` or
  `"ExceptionalCircumstancesDisabled"`. The lax clause fails on both conjuncts. The two
  states the module really does keep are the two exceptional-circumstances ones, which no
  player would call a dust storm, so **no replacement sentence is offered.** Full route in
  `agent/bugs/F54.md` (2026-09-12 section); owner's word on checklist **162 (a)**.
  ⛔ **Do not restore it** — it would publish a false sentence.

### 2 · Saint's blessing (`:142`) — approved, polished
- **What you saw:** nothing, which is the problem — the blessing meant for the
  Religious colonists in the Saint's dome had never applied to a single one of them.
- (replaces "the trait's colony-wide effect had never applied to a single colonist")

### 3 · F58 stale reservations (`:105`) — rewritten plain (owner: word salad)
- **Headline:** Beds stayed reserved for colonists who were never going to take them
- **What you saw:** free beds in a dome, homeless colonists outside it, and nothing
  happening. *(unchanged)*
- **What was wrong:** a bed could stay reserved for a colonist who was never going to
  arrive — one still waiting for a ride that never came, or one who set off on foot —
  and those reservations are invisible in the interface.
- ⚠️ **"What was wrong" replaced on the owner's 2026-09-12 ruling of checklist 159 (3)**,
  from the surface audit's D2/§3 item 3: two of the three original cases are vanilla's
  own release paths. Death releases it (`Colonist:Die` → `ClearTransportRequest` →
  `CancelResidenceReservation`, `Lua/Units/Colonist.lua:1288`, `:2037`; `Erase` at
  `:1250`), and moving in elsewhere releases it (`Residence:AddResident`,
  `Lua/Buildings/Residence.lua:110`). The defect is the colonist who never arrives —
  committed-shuttle limbo and the walk path (`Code/Fix_StaleReservations.lua:73-82`).
- **After the fix:** reservations held by a colonist who can no longer use the bed are
  released, and stale ones expire. A bed held for a colonist away on an expedition
  is kept for their return.
- **Card, all five copies:** headline bullet "A dome sat half empty and still refused
  to house anyone." → "Beds stayed reserved for colonists who were never going to
  take them."

### 4 · F52 vacuum walks (`:46`) — HELD, no change

### 5 · F21 train wait time (`:398`) — approved; Comfort claim removed, fix stays
- **Headline:** Waiting on the platform was counted again as time on the train
- **What you saw:** the Travel time figure on trains and tracks reading larger than
  the journeys actually were.
- **What was wrong:** *(unchanged)*
- **After the fix:** the ride is timed from boarding, so the platform wait is counted
  once, at the station.
- **Card intro, all five copies:** "a Comfort penalty billed for longer than the
  journey actually took" → "a train travel-time figure that counted the platform
  wait twice".
- Record note for the entry, not the row: on 1.0.7 the same wait also charged
  Comfort; 1.1.0 removed that charge.

### 6 · F34 landscaping vs boarding (`:242`) — approved, polished (factual error: drones, not colonists)
- **Headline:** Starting a landscaping job yanked drones out of the RC Commander they
  were boarding
- **What you saw:** drones pulled back out of an RC Commander they were climbing into
  — sometimes more than once — when you started a landscaping job nearby.
- **After the fix:** the exclusion is used, and boarding drones are left alone.
- In-game registered title: same correction (colonists → drones).

### 7 · F77 extender flapping (`:206`) — approved, polished
- **After the fix:** changes within two seconds of each other are handled as one, so
  a flickering Extender costs the fleet one interruption instead of one per flicker.
- In-game registered title: "Nearby Extender changes share one hub rebuild".

### 8 · F30 lake entombment (`:229`) — rewritten plain (owner: word salad)
- **What was wrong:** the pass that clears units off a construction site skips the
  constructor doing the clearing, and it runs *before* the basin is dug, so anything
  still standing there (including units that had been moved and wandered back) was
  sealed under the new terrain and ran out of power.
- **After the fix:** the moment the basin exists, anything standing in it is sent to
  solid ground nearby, so the rover drives out instead of being sealed in.

### 9 · F06 Philosopher's Stone hang (`:498`) — rewritten plain
- **After the fix:** the departure is re-announced every hour for ten sols, so
  answering the popup any time in that window lets the mystery finish.
- In-game registered title: drop "can no longer hang forever".

### 10 · F50 rocket drone churn (`:219`) — approved, polished
- **What was wrong:** once every game hour the rocket re-issued its work requests,
  cancelling the orders of every drone already walking towards it.
- **After the fix:** requests that have not changed are left alone, so the drones
  arrive.
- (drops "so any trip that took longer than an hour could never finish")

### 11 · F40 Biorobots dust sickness (`:166`) — approved, polished; judgment marker stays
- **After the fix:** Biorobots do not catch it, and Biorobots already suffering from
  it are cured when you load the save. The current game has retired these
  dust-sickness events; the fix stays for saves that still carry the illness.

### 12 · F48 old-track migration pass (`:408`) — rewritten plain (owner: word salad)
- **What was wrong:** one of the game's own repair passes for saves from an earlier
  version was written so that it did nothing. The current game has corrected that,
  but a save that already recorded the repair as done will never run it.
- **After the fix:** the pass runs properly, once, when you load. A track it cannot
  sort keeps its old order, and the rest carry on.
- ⚠️ **"After the fix" replaced on the owner's 2026-09-12 ruling of checklist 159 (3)**,
  from the surface audit's D4/§3 item 12: "put back the way it was" overstates it. On
  failure the engine restores only the element **order** (`Lua/Tracks.lua:617-620`
  @1.1.0 copies `all_elements` back); `connections` and `node_idx`, rewritten at
  `:578-579`, `:602`, `:610`, stay rewritten, and the failure is an `assert` that does
  not unwind, so the sanitizer's `pcall` (`Code/90_SaveSanitizer.lua:224`) sees no
  error on that path.
- **Worth knowing:** keep the first two sentences ("we cannot tell you this fixes a
  symptom you have. It puts your save into the state the game's own migration
  intended, and on our test save it corrected several tracks and stayed corrected.");
  drop the rest, which the new After line now says.

### 13 · F31 cave-in on a missing map (`:561`) — ✅ **RETIRE** (owner, 2026-09-12)
- **No replacement text.** The row at `:561-570` comes **off**, and the card's
  stopped-story headline bullet comes off all five copies. Module out under module-list gate (tools/doccheck.py MODULE SETS + tools/upload_preflight.py)
  (`items.lua` entry), and the TestKit's `AnomalyCaveInMap`
  (`50_Probes_Wave5.lua:400`) plus its `64_Probes_Wave14.lua` census row retire with it.
- Why: the deep audit (`reports/SURFACE_AUDIT_2026-09-12.md` §2 C1–C6) found neither
  half reachable on 1.1.0 and no observation on either branch — no save, no log, no
  report. The owner's lead held (`NoUndergroundAndAsteroids` is `Obsolete = true` on
  1.1.0, `Data/GameRuleDef.lua:53-63`), and the two routes it left open closed: the
  eight cave-in sequences run only on the underground map, so the map they name is the
  map they run on, and the new-game picker admits no non-Surface start (map data read
  out of all 142 `Packs/Maps/*.fpk`).
- The frozen `v5-game-1.0.7` build keeps the module; that build is untouched (ck156).

### 14 · F73 asteroid vacuum reflex (`:189`) — approved, polished; judgment marker stays; **After line replaced 2026-09-12**
- **After the fix:** a colonist whose home is up and running, idling out in vacuum, is
  sent home once half their oxygen time is gone.
- ⚠️ **Replaced on the owner's 2026-09-12 ruling of checklist 159 (3) — "3 all", the
  optional fourth included**, from the surface audit's D7/§3 item 14: "a colonist with
  a home" is one word short. The reflex requires `IsValid(self.residence) and
  self.residence.working` (`Code/Fix_ShelterReflex.lua:101-108`), so a switched-off
  home does not call them in.

## Whole-list arithmetic after the batch (derive once, at apply time — never carry)

- Card count word: Forty-nine → **Forty-six** — F37 + F43 + F31 all retire (owner,
  2026-09-12; F31 no longer conditional).
- Headlines on the card: 21 → **19** (F37's farm-oxygen line and F31's stopped-story
  line gone); F58's headline keeps its slot with the new words.
- "Real defects you cannot see today" count on the card: three → **two** (F57a and
  F29; F43 leaves that set).
- Judgment calls: **three** in this batch — but ⚠️ **C89 adds a fourth** in the same
  v10 (checklist 158). Re-read the `??? question` rows at apply time.
- ⛔ **Module and file totals: DO NOT carry the old 46 → 44 / 47 → 45 line.** Three new
  modules (C85, C88, C89) land in the same v10, so the retirements' arithmetic no
  longer stands alone. Derive from `python tools/doccheck.py --emit-counts` at apply
  time. TestKit probes: `GhostFarmOxygen`, `LayoutTechLock`, `AnomalyCaveInMap` and the
  already-loose `DomeFreeSpaceMismatch` retire with their modules, plus the
  `64_Probes_Wave14.lua` census rows (local kit, not part of the release).
