# smrtk 09 — the architecture rebuild, the two blockers, and the More trace

Link 09 of `smrtk`. **Codex — Sol, xhigh or max.** Created 2026-09-14 by the orchestrator after
08 ran. README rules 1–22 are yours. This is a **build + desk** link: ⛔ **it launches nothing.**

Authored against pack HEAD **`525d435`** / TestKit HEAD **`8a576a5`**. ⚠️ Several peers share the
pack checkout under one git identity — `git log --author` attributes nothing, identify by sha +
diff, re-check `git status` before every write.

## 0 · Orient, and the ruling you are building to

`git log --oneline -10` + `git pull` in **both** repos, `git status --short`, `ListAgents`, then
`docs/agent/STATE.md`.

⚖️ **`ck183` is the owner's ruling and it is the spec.** Read it whole before you touch code —
`docs/PLAYTEST_CHECKLIST.md`, item 183. Its core, in the owner's words: *"Related actions and
items should be on one page. And if an item is used in conjunction with multiple items it should
be on the top hot bar."* ⛔ **Do not redesign it, and do not treat the current layout as a
constraint** — it is what you are replacing.

⛔ **No stale-probe gate, no launch, no play claim.** Everything you build is source-derived
until **08b** runs it. ⛔ Never move a status you did not witness (rule 17).

## 1 · Three strands — A and B are yours, C is a subagent running beside you

### Strand A — the architecture (ck183)

**Group by task, not by taxonomy.** The measured cause, which is why this is not a renaming job:
all four triggers are registered on **Agent** (`74`) and the only thing that consumes a trigger,
`run_until`, is registered on **World** (`72`), so every "run until X" task is two pages before
anything else happens. `watch_field` adds a third and gives one feature two names — *"Watch
selected field"* on Kit, *"Selected field changed"* on Agent.

1. ⭐ **A `Run` grouping holding `run_until` AND all four triggers** (`trigger_sol`,
   `trigger_error`, `trigger_rocket`, `trigger_field`). **Highest-value single change — it
   collapses four of the seven measured cross-page flows.**
2. ⭐ **A persistent hot bar**, for things that are never the task itself: clean/tainted status ·
   `mark` · flush + copy log · pause/speed · `screenshot_mark` · **and the armed-slot indicator
   naming the armed slot and its escape** (defect 20 — `AcquireClick` installs a `TerminalTarget`
   at priority 10001 returning `"break"`, so an armed slot silently eats **all** map selection and
   right-click-to-cancel appears nowhere).
3. ⭐ **One SMR button that toggles the whole panel** (defect 3, RULED): *"Just open and close the
   panel on click, opens it next click closes it."* Drop the popout menu. Keep a compact
   clean/tainted colour on the button so requirement (A) stays visible while closed.
4. **Put that button on `HUDMiddle → idMiddleList`** (defect 4) — an `XWindow` with
   `LayoutMethod = "HList"` holding the vanilla `HUDButtonNoFrame` buttons. **Zero vertical cost,
   and it fixes defect 1 by construction.** ⚠️ Source-read only, never built: if the route fails,
   fall back to parenting as a **sibling** of `idBottom` (the level holding `idHintPanel`, which
   sets no `LayoutMethod` and defaults to `"Box"`, so children overlap instead of displacing).
   ⛔ Do **not** leave it parented into `idBottom` — that is defect 1, and it inflates `idBottom`
   by ~168 px, permanently shoving MapSwitch/`idLeft` and the pinned shuttle/dome/rover row.
5. ⛔ **An action that operates on the selection belongs on Selected.** Move `watch_field`
   ("Watch selected field", registered on Kit) and confirm `dump_selected`'s placement. The
   precedent is already in your own code: `73_SMRTK_Infopanel.lua:29-32` surfaces `dump_selected`
   (Kit) and `pin_A/B/C` (Agent) as buttons **on Selected**. **That is the mechanism for the hot
   bar too — register anywhere, surface where the work is.** Re-use it; do not invent a second.
6. **Controls at the TOP of every page, above any growing readout** (defect 13), and ⭐ **a clear
   control above every list that grows** (defect 6 — owner, 2026-09-14: *"clean button means clean
   the on screen log"*, ⛔ **not** `Clean & Fix`; 08 read it wrong and flagged the reading).
7. **Size rows to their text and shrink the font** (defect 7): `selected_button` hard-codes
   `MinWidth/MaxWidth = 146` (296 for More) at `MinHeight = 30`, `TextStyle = "ConsoleLog"`. Owner:
   *"far denser than now"*, but **not as small as vanilla's cheat menu**.
8. **Make a disabled button look disabled** (defect 8) and **relabel Kit** so the words match how
   the work is described (defect 9 — the owner could not find "Run all probes").

### Strand B — the two blockers, plus the relabels and semantics

⛔ **21 and 22 ship regardless of how far strand A gets.** 21 blocks **08b** outright.

- **21 ⛔⛔ The Stamper cannot capture ANY building.** `77`'s `add_building` guards on
  `field(o,"template_name")`, which **no placed building carries**:
  `SetupBuildingTemplateTables` sets it only on the template table
  (`BuildingTemplates[id] = setmetatable({ template_name = id }, g_Classes[id])`). **Fix:**
  `field(o,"template_name") or o.class` — the fallback `skip_capture` already uses, two functions
  away — **and audit every other `template_name` read.**
- **22 ⛔⛔ `spawn_*` mutates and reports `REFUSED`.** It verifies same-tick
  (`before = #labels.Colonist` → spawn → `after`), but a colonist joins that label in
  `Colonist:GameInit() → AddToCityLabels()`, which the engine defers to end of tick. Measured:
  `REFUSED reason="spawn count mismatch; before=701 after=701"`, census seconds later **711**.
  ⛔ **An action that has mutated must never report REFUSED** — it is a lying log line and
  breaches requirement (B). All twelve `spawn_<kind>_<n>` buttons share the body.
- **25 → dissolve it, do not patch it.** "Finish selected rocket flight" needs a selected
  in-flight rocket, and an in-flight rocket **cannot be selected** — the only route was the
  console. ⭐ **Make it world-wide — "finish all in-transit arrivals", no selection** — which
  matches the row it already sits in and beats ultra speed instead of tying it. ⛔ Do not build a
  rocket picker.
- **23 Rocket transit skip is mislabelled and one-directional.** Relabel *(a)* to "Skip remaining
  transit (inbound)". *(b)* Shipped `spot_type`s are earth/our_colony/anomaly/asteroid/project/
  rival and only `our_colony` is accepted, so **the return leg to Earth cannot be skipped**.
  ⚠️ **Do NOT assume widening is one line** — arrival at Earth or an expedition site runs a
  different completion path. **Cost it; do not promise it.**
- **19 `fix_all`'s `changed` does not mean changed.** The repair branch increments for every
  building that merely *has* the method; `malfunction_all` compares before/after. Same field name,
  two meanings, one `register()` pair. Measured: `fix_all visited=1333 changed=1333 skipped=0` vs
  `malfunction_all visited=1305 changed=740 skipped=564`. **Make the field mean one thing.**
- **18 "Complete constructions" already does "Complete wires / pipes"** —
  `CheatCompleteAllConstructions` calls `CheatCompleteAllWiresAndPipes()` first. The grids button
  is **not** useless (grids-only is a real want) but nothing says so. **Relabel both.**
- **15 The speed ladder skips rungs.** `config.lua:117-122` — pause 0, normal 1, **medium 3**,
  **fast 5**, **fastest 20**. We expose 1, 5, 128 and skip 3 and 20, which is why *"smr's fast
  button is vanillas fastest button"*. **Label by the constant we set, not vanilla's captions, and
  fill the missing rungs.** ⛔ Supersedes defect 14.
- **12 Make the cursor-targeted meteor hit the cursor.** `72` calls `MeteorsDisaster(descr, kind,
  pos)` with three args; the **fourth, `forced_pos`**, switches `SpawnMeteor` from
  `GetRandomPassableAroundOnMap(map, pos, storm_radius)` to the exact point
  (`Meteors.lua:107-111`). `storm_radius` defaults to `500 * guim` and **no shipped preset
  overrides it**, so every intensity scatters identically — the owner's *"fired but very
  inaccurate"*. ⭐ **Vanilla's own cheat never passes `forced_pos`, so the vanilla menu cannot
  place a meteor precisely and we can.** Keep scattered mode as a separate row.
- **11 `print_tee` is an orphaned action** (`70:276`). Wire it or cut it; do not leave it.
- **2** is moot once 4 lands (`XWindow.FoldWhenHidden` defaults **false**, so hiding alone never
  freed the space). **5** move the Delete caveat out of the section body (`73:181`) into the Delete
  button's `RolloverText` — ⛔ do not delete it, 03B wrote it to make the label honest about units.
- **10** dissolves when `watch_field` and `trigger_field` are co-located — verify that it does,
  rather than patching the affordance separately.

### Strand C — SUBAGENT, concurrent: trace the 84 More names (defect 16)

⚖️ **Owner ruling, 2026-09-14:** *"I mean that not as play testing I want the next build section
to answer that. Trace them and determine if the old imported ones work and are relevant."* ⛔ 08's
sizing (84 in-game presses, a dedicated sitting) is **SUPERSEDED** — this is a **desk trace of the
84 leaf bodies in the 1.1.0 source**, and the owner asked for it as *"a good job for a sub agent
while it builds"*.

✅ **Safe to parallelise, structurally:** 03C built the More group by **dynamic metatable walk**,
not a fixed list, so strand A arranges a *group* and never the entries. The prune lands as a
filter on the walk at close-out and cannot collide with the re-layout.

**Output: a keep / cut / needs-rollover list**, every name assigned. For each leaf ask: does it
still exist on 1.1.0 · is its body a no-op · does it reference a system 1.1.0 removed · would a
playtester ever want it. ⚠️ **What a desk trace cannot settle:** runtime behaviour (`EF-078`,
trust runtime over source). ⛔ Anything the body cannot resolve is a **named `needs-rollover`
residue** — never a silent keep, and never a claim that it was tested.

## 2 · Every one of 08's 25 defects is assigned — ⛔ none may be silently dropped

**Strand A:** 1 · 2 · 3 · 4 · 5 · 6 · 7 · 8 · 9 · 10 · 13 · 20.
**Strand B:** 11 · 12 · 15 · 18 · 19 · 21 · 22 · 23 · 25.
**Strand C:** 16.
**Record only, NOT build items:** **14** (superseded by 15) · **17** (the attendee's own
source-derived prediction was wrong — a correction to the record) · **24** (attendee drift).
⇒ If you cut anything from a strand, say so in your report **with a reason**; silence is a finding
against you, not a decision.

## 3 · Read path — these files, not their folders

TestKit `Code/`: `70_SMRTK_Core.lua`, `71_SMRTK_Panel.lua`, `72_SMRTK_World.lua`,
`73_SMRTK_Infopanel.lua`, `74_SMRTK_Agent.lua`, `75_SMRTK_Saves.lua`, `76_SMRTK_Kit.lua`,
`77_SMRTK_Stamper.lua`, `80_AgentSlots.lua` · `reports/SMRTK_FULL_SITTING.md` (the defects and the
Surface section) · `reports/SMRTK_UI_HOOKS.md` §1–2 (the proven injection routes) ·
`docs/PLAYTEST_CHECKLIST.md` **item 183 only** · `prompts/smrtk/README.md` rules 1–22 and
§ "What is FIXED" · facts `EF-095`–`EF-099` and **`EF-102`** (the depot class tree — a
`UniversalStorageDepotBase` guard misses 5 shipped classes; `73`'s `depot_read` has this bug).
Game source: `Lua/X/Infopanel.lua`, `Data/XDef/HUD.lua`, `Lua/Buildings/Building.lua`
(`SetupBuildingTemplateTables`), `Meteors.lua:16,107-111`, `config.lua:117-122`. More via
`facts/INDEX.md` — ⛔ grep it, never read it whole.

## 4 · Derived facts (R-C) — every number is a CLAIM; re-derive before building

| fact | measured | at | re-check (scoped so it CAN fail) |
|---|---|---|---|
| all 4 triggers on Agent, `run_until` on World | registration sites | `525d435` | grep `trigger_` in `74` and `run_until` in `72` |
| the dock inflates `idBottom` by ~168 px | 62 px + `Margins = box(8,0,0,106)` | 08 | read `73`'s dock parenting |
| `idMiddleList` is an `HList` of `HUDButtonNoFrame` | source read, **never built** | 08 | read `Data/XDef/HUD.lua`; ⛔ if it fails, use the sibling fallback |
| 84 More names, 22 curated, 106/106 | 03C | TestKit `f093e3b` | re-walk; report the delta rather than inheriting it |
| spawn: 701 → 711 across the tick | census vs same-tick check | 08 | re-read `AddToCityLabels`'s deferral |
| `storm_radius` = `500 * guim`, no preset overrides | `Meteors.lua:16` | 1.1.0.403908 | grep the Meteor presets for `storm_radius` |

## 5 · Scope fence

**IN:** the nine TestKit `Code/` files, your report, the smrtk README queue row, ck183's build
items, the More trace.

**OUT:** ⛔ launching the game — **08b is first contact for everything you change**. ⛔ the pack's
`Code/`, `items.lua`, `metadata.lua` (rule 11). ⛔ `docs/PLAYTEST_CHECKLIST.md` — owner items go in
your report as `OWNER-ROUTED` and the orchestrator consolidates. ⛔ re-running 02's kill gate.
⛔ redesigning ck183.

Found something interesting out of scope: **file it, do not fix it** (rule 3).

## 6 · Gates — green before every commit (rule 15)

`python tools/parsecheck.py` on every `.lua` touched · **rule 6's grep** (no `NetSyncEvent`,
`NetSyncEvents.*`, `LogCheatUsed`, no vanilla wrapper) and **rule 7's grep** (one `SMRTK_` tag,
one logger) — **presence side counted, a zero from a truncated grep proves nothing** ·
`python tools/doccheck.py` GREEN in the pack repo · **rule 9: idle = zero patched vanilla
functions** — every write to a real global inside a toggle's install with a matching uninstall.
⭐ **Rule 9 is the one this link is most likely to break**, because a hot bar and a dock button
are new persistent UI: 08 measured **zero surviving arms**, and that must stay true.

⚠️ **If you add a `SMRTest.Register(` call anywhere in the TestKit tree it moves the pack repo's
probe count and REDs `STATE BUILD STATE` for every session.** Cure, same commit:
`python tools/doccheck.py --regen`, then commit `docs/agent/STATE.md` by pathspec. ⛔ `--no-verify`
is never the answer. (The nine toolkit pages currently register zero, so this binds only if you
add one.)

⛔ `Code/` edits only with `Mars.exe` closed — `tasklist` first, in a separate command (rule 16).

## 7 · Stop conditions — permission, not failure

Stop and report if: the `idMiddleList` route does not exist as read **and** the sibling fallback
also fails · a hot-bar or dock button cannot be built without patching a vanilla function while
idle (rule 9) · defect 22's fix cannot be made without changing what a `spawn_*` action does ·
widening 23's rocket skip turns out to need a second completion path (**cost it, do not build
it**) · the More trace finds the metatable walk itself is wrong · doccheck is RED before you start.

## 8 · What may NOT be claimed

- ⛔ **Never claim any of this works.** Nothing here launches the game; **08b is first contact**.
  Source-derived is the honest word.
- ⛔ **Never claim requirement (A) survives your changes.** 08 proved it on the OLD surface. Your
  job is to not break it; only 08b can say whether you did.
- ⛔ **Never claim a More name works because it exists.** The metatable walk proves exposure, not
  behaviour.
- ⛔ **A mechanism-only PASS is not a pass** (ck183): if something works but loses to the vanilla
  workaround, say both. That test is the reason this link exists.
- ⛔ Never state an absence from a truncated grep.

## 9 · Close-out

1. Report at `reports/SMRTK_09_REBUILD.md`: what you built per strand, **every one of the 25
   defects with its disposition**, the More trace's keep/cut/needs-rollover list, DEPARTURES with
   reasons, SUGGESTIONS, DRIFT for 99, and `OWNER-ROUTED` lines.
2. ⭐⭐ **NAME WHAT YOU INVALIDATED, and append it to `08b`'s `## Notes from upstream`.**
   08 scored **block 1 (dock, status, navigation — classes 1, 2, 4) PASS** against the OLD
   surface. A re-layout **invalidates that verdict**, and 08b is currently written to re-run
   nothing from classes 1–17. ⛔ **List every 08 verdict your changes put out of date so 08b can
   cover them** — a fix invalidates its own tests, and an uncorrected PASS is worse than no test.
3. Append your outbox to **99's** `## Notes from upstream` (rule 2).
4. Strike this link's row in `prompts/smrtk/README.md`'s queue.
5. ⛔ **`git rm` this file** in the same commit. One-off; it does not re-run. ⚠️ `prompts/README.md`
   carries ONE folder row for `smrtk/` — do not touch it beyond repointing its "next is" sentence.
   Re-run doccheck after.
6. Commit by pathspec in each repo; push the pack repo. ⛔ TestKit is local-only by design.

## 10 · Required — a live progress list

Create it before you start, **one item per commit-and-verify unit**, marked the moment each
completes, exactly one in progress. ⚠️ **Three strands means three parallel tracks in one list** —
name the strand in each item, and expand a strand the moment it turns out to be more units than
this brief anticipated. The owner reads this list to decide when to step in.

## Notes from upstream

**From 08 (`reports/SMRTK_FULL_SITTING.md`, PASS WITH CORRECTIONS, 2026-09-14):** requirement (A)
is **PROVEN** — `cheats_count=0`, 844 records, zero TAINT, zero ERROR, zero surviving arms. Classes
1–17 pass on the old surface; class 18 is blocked by defect 21. 08 also flagged that
`DomeFreeSpaceMismatch` needs triage as a candidate defect, and that three attendee drifts are
recorded in its own report — weigh its readings knowing that.

**From the orchestrator (2026-09-14):** ck183 is an owner ruling, not a suggestion, and the
rocket case is its proof: `rocket_arrive` was filed on World because it is a "completion thing"
while acting on the selection, and the owner would rather *"hit ultra speed and wait the 30
seconds"* than use it. ⭐ **The test to apply to every control you touch: does it beat the vanilla
workaround? If not, it should not exist.** ⚠️ `EF-102` was filed today because a false claim about
the depot class tree survived in STATE as prose with no falsifier — `73`'s `depot_read` still
carries that bug, and Fill/Empty currently log no before/after on five shipped depot classes.
