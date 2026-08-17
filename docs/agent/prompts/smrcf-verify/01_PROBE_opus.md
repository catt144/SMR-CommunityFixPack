# A·01 — the verification probe · UNATTENDED · owner cost ZERO

**Read `README.md` in this folder first — its chain rules bind you.** Then
`docs/agent/STATE.md` (mandatory every session), then this.

## 0 · Staleness check, before anything else

```
git log --oneline -10
git pull
```

This brief was written 2026-08-16 by the coverage sweep that filed `C49`–`C52`.
If commits have landed since, **the entries are authoritative and this brief is
not** — `CHAIN_METHOD` §3, *"briefs cite entries; sessions act on the ENTRY, and
the brief says so."*

## 1 · 🗒 Live todo list, from your first action

One item per job below, updated **the moment each moves**. The owner reads that
list to decide whether to step in; a list updated at the end is useless to them.

## 2 · The job — four answers and two detectors, one launch

### Job 1 — is the dust-devil marker path REACHABLE?

**The finding it decides** (source-verified 2026-08-16, unfiled): the marker
thread checks only `HasDustStorm` —

```lua
		if not HasDustStorm(map) and SessionRandom:Random(100) < descr.marker_spawn_chance then
```
`Lua/DustDevils.lua:169`

— while the natural scheduler checks **both** `HasDustStorm(map) or
DustStormsDisabled`, at `:209` **and** `:220`. Same file, same author. That is
`FIX_POLICY` §4 tell (3), sibling contradiction. And after the roll, `:172-176`
spawns, sleeps out the warning, and starts the devil re-checking only
`IsValid(devil)` — no gate re-check across the delay.

`DustStormsDisabled` is a `GameVar` set by terraforming progress
(`Lua/TerraformingDisasters.lua:16`, `DustStormsDisabled = reached`).

**Read, on the owner's most-terraformed save:**
- `DustStormsDisabled` — true or false, and the terraforming parameters behind it
- a `MapForEach` count of `PrefabFeatureMarker` with `FeatureType == "Dust Devils"`,
  **per map** (surface AND underground — the marker thread is created per map at
  `:201-205`)
- for each such marker, whether `marker.thread` is live
- the active dust-devil descriptor's `marker_spawntime` / `marker_spawn_chance`

⛔ **This is the whole verdict.** Markers present + `DustStormsDisabled` true ⇒
the defect is reachable and chain B files and fixes it. **Zero markers ⇒ it is
`C49` again** — real in source, unreachable — and it gets recorded as such
rather than built.

### Job 2 — does `AsyncPopsDownloadFile` exist?

`C52`'s screenshot repair reaches `AsyncPopsDownloadFile(url, temp)`
(`CommonLua/Libs/Paradox/ParadoxMods.lua:260`), which has **zero definitions in
all of `ModTools\Src`**. Either a native export Lua cannot see, or absent.

Print `type(rawget(_G, "AsyncPopsDownloadFile"))`. Do the same for
`AsyncWebRequest`, `AsyncStringToFile` and `AsyncFileRename` (the neighbours the
same function uses) as a control — if those are `function` and this one is
`nil`, that is a much stronger reading than the bare answer.

⛔ **Do not call it.** A `type()` read only. Calling an unknown network function
unattended is out of scope and out of bounds.

### Job 3 — is map generation drivable from Lua, and what does one cost?

Chain D's seed search rests entirely on this. Establish, without starting a real
game if you can avoid it:

- do `GenerateRandomMap` and the `RandomMapGenerator_Picard` entry points exist
  and are callable in the mod sandbox? (`type()` first, same as job 2)
- is there any Lua route to start a new game with a chosen seed, or does it need
  the menus? Name the route or name its absence.
- **if and only if a safe route exists**: time ONE generation and read
  `UndergroundMap.City.labels.JumboCave` immediately after.

⛔ **Do not loop.** One generation, timed, is the deliverable. A seed sweep is
chain D's job and only if this says yes.
⛔ **Do not touch the owner's saves.** Any generation happens in a throwaway
state; nothing is written to the save directory. If you cannot guarantee that,
**answer the `type()` half and stop** — that alone unblocks D's planning.

### Job 4 — does any existing save hold a Jumbo Cave?

Across the owner's saves (read-only, headers and a load if needed on a **staged
copy**, never the originals):

- any `JumboCave` object, per save, per map
- any `JumboCaveReinforcementStructure`, built or under construction
- any `WasteRockObstructor` whose `parent_construction` includes one
- **`UndergroundRework106`** — false in saves begun before 1.0.6, which decides
  whether the save runs `BuriedWonder_Jumbo_Cave` or `..._106`
  (`Lua/Buildings/UndergroundDome.lua:16-19`)
- ⭐ and the one that would be a live bug: is any such rock **already sitting in
  a drone's `unreachable_buildings` table**?

⚠️ `EF-056` — loading a COPY of a real campaign still runs that campaign's
autosave rotation and can delete the owner's autosaves. **Pre-copy every autosave
first.** This has fired before and eaten a file.

### Job 5 — arm two standing detectors

Log-only. No behaviour change. Both go in `Code/` as ordinary modules with
self-checks, or as TestKit probes if that is cleaner — **your call, stated in the
close-out with the reason.**

- **`C25` detector** — wrap `WasteRockObstructor:DroneApproach`; on a falsy
  return log the rock, its `parent_construction` classes, its position, **and
  what occupies the neighbouring hexes** (terrain vs other rocks — this is
  chain D's pre-registered discriminator and it must be captured at failure
  time or it is lost).
- **`C35` detector** — wrap `TaskRequester:InterruptDrones`
  (`Lua/_TaskRequest.lua:290`); log any drone that passes the filter while
  `drone.command == "Embark"`, with the caller. That is the exact condition
  `assert(drone.command ~= "Embark")` at `:305` forbids and `EF-008` guarantees
  does not stop the `SetCommand("Reset")` that follows.

⛔ **`EF-058` — the flattened-class trap has bitten this project four times.** A
wrapper on a base class watches nothing while the built copies do the work
(`classes.lua:988`). **Patch every class that actually carries the method and
prove the wiring off live instances before trusting a single line of output.**

## 3 · Predictions — committed and pushed BEFORE the launch

Write numbered predictions for jobs 1–4 with a falsifier each, commit, push,
**then** launch. `git log` timestamps are what make the result falsifiable
(precedent: `3f1856f` at 15:12:37 vs its launch at 15:13:27).

## 4 · Scope fence

**IN:** the payload, the launch(es), the four answers, the two detectors, the
records.
**OUT:** ⛔ any fix for any of `C25`/`C35`/`C50`/`C51`/`C52`/the marker gate.
⛔ Any owner time. ⛔ Anything on the release front. ⛔ Installing
`smr-community-fixes` on the rig — a third mod invalidates every gate baseline
(`STATE.md`).

## 5 · Stop conditions

- Pack/opt-in gate wrong at run top → **STOP** (unattended-2: six steps once
  banked readings about code that never ran).
- A detector cannot be installed log-only → don't install it; hand the question
  to `02_AUDIT`.
- Job 3 needs the menus → that is the **answer**. Record it, move on.
- Any `[LUA ERROR]` naming our code → void the run, fix, re-arm, **archive the
  voided log beside the good one** (the unattended-1 practice that makes a
  post-hoc audit possible at all).

## 6 · ⛔ What may not be claimed

- ⛔ **`tested-unattended` for anything with a screen component.** Closed to
  screen events by the 2026-08-15 vocabulary ruling.
- ⛔ **"The marker defect is real" from source alone.** Job 1 decides
  reachability; without markers it is LATENT and must be written that way.
- ⛔ **"`AsyncPopsDownloadFile` is missing."** A `nil` from `type()` in the mod
  sandbox is evidence, not proof — the sandbox does not see everything.
- ⛔ **"The detectors work"** until you have shown them firing on a live
  instance, or have stated plainly that they are armed and unwitnessed.
- ⛔ **A blanket verification claim over a table.** Provenance per row —
  MEASURED / SOURCE / INFERRED / INHERITED / GUESS — and the ROUTE sentence
  tagged separately from its citations (`WORKFLOW` R3).

## 7 · Close-out — how this file disappears

One commit: findings integrated into the entries (`C25`, `C35`, `C52`, and a
NEW entry for the marker gate **if and only if** job 1 clears it — regenerate
the index with the tool, never by hand) · outbox appended to `02_AUDIT` ·
log archived with `git add -f` · manifest row struck · `git rm` this file ·
`python tools/doccheck.py` GREEN · commit naming the grave
(`git show <sha>:docs/agent/prompts/smrcf-verify/01_PROBE_opus.md`) · push.

## Notes from upstream

*(From the coverage sweep, 2026-08-16 — the session that filed `C49`–`C52`.)*

- Every source citation in this brief was derived at `ModTools\Src` by symbol on
  2026-08-16 and is SOURCE-tagged. **Re-derive the route anyway** — this project
  has been wrong about a route twice while every cited line was right.
- `EF-063` is new and relevant if you touch anything text-shaped: the nine
  shipped language packs and how to read one with our own `tools/flpk_extract.py`.
- `EF-064` is new and is what refuted fredware's stated mechanism for `C52`:
  `ProtectedPropertyObject` asserts and then `rawset`s anyway, so it protects
  nothing in retail.
- The owner's standing framing for this whole set: *"stack the deck in our
  favor"* — accelerate the sampling of a rare event, but only ever by turning a
  parameter **the game itself uses**, never by placing the evidence ourselves.
