# Chain 8b-2 — finish the PT-60 batch leg and close chain 8b

> ## ⛔ SEALED: `docs/reports/BLIND_AUDIT.md` — DO NOT OPEN
>
> **This prompt is FORBIDDEN from reading, grepping, summarising, or acting on
> `docs/reports/BLIND_AUDIT.md` or any part of its contents.** It is a **blind
> control**: a fresh session produced it having deliberately read no project docs,
> and its whole evidential value is that it was written without the project's own
> conclusions in view. **Only chain prompt 12, at job 6b, may open it.**
> If a broad search surfaces its contents by accident: stop, discard, do not use
> it, and record that it happened in your handoff notes.
> ⚠️ **Name your paths when you `git add`.** A `git add -A` in the 8b session
> staged this file once; it was amended out before any push, but the seal is
> enforced by prose alone — there is no `.gitignore` entry and no hook.

**One-off; delete this file in your final commit. Read `README.md` in this folder
first.** Written at **`8267386`**. Staleness check: `git log --oneline -12` +
`git pull` before anything.

---

## Why this prompt exists

Chain 8b built all seven approved fixes (F90-F96), wrote seven probes, specced
**PT-60**, and then ran **most of the leg at the keyboard with the owner**. It
split under chain rule 3 with the leg **partly run**: five of the seven fixes have
real in-play evidence, two remain, and **one defect in our own new code was found
by the leg and fixed but NOT re-verified**.

**Everything below is state you inherit. Do not re-derive it. Do not rebuild
anything.**

---

## 1 · What is already verified, with evidence

⭐ **Two fixes have a complete before/after A/B taken on the same colony.** That is
stronger evidence than anything else in this batch and must not be re-run.

| fix | status | evidence |
|---|---|---|
| **F95** extractors | ⭐ **defect AND fix observed** | Astrogeologist colony, pack OFF: `MetalsExtractor=1 WaterExtractor=1 AutomaticMetalsExtractor=0 MicroGAutoWaterExtractor=0`. Pack ON: **all four `=1`**. The two vanilla labels are the positive control. **Both** the preset patch and the load-time heal logged. ⚠️ **But see §2 — the heal had a defect found immediately after.** |
| **F90** grid breaks | ⭐ **DEFECT OBSERVED IN PLAY — a project first** | Constructed fixture (save `f90`): a 1668-connector electricity fragment that is **100% underground** yet sits on the MAIN city's list, plus a pure-surface 424-connector fragment as control. Pack OFF, one dust storm: `underground 0 → 15`, monotonic, **plateaus the moment the storm ends**. Surface `0 → 7`. Owner swept the map: **no cave-in or marsquake debris and no such notification**, so attribution is clean. **Pack-ON leg NOT YET RUN.** |
| all 15 changes | ✅ **install verified on the ENABLE PATH** | `ListFixes()`: **79 rows, all 79 `[active]`**, zero `[LUA ERROR]`. Enabled at the main menu of a running process (in-place `ReloadLua`), which is the path F87 exists for and the harder of the two FIX_POLICY §2 requires. All five new modules and all seven converted modules active. |

**PT-60 prediction outcomes so far:**

- **P1 ❌ MISSED, no defect behind it** — predicted `73/79`, read **`79/79`**.
  Cause: **Mod Options survive a Mod Manager disable** and six opt-in modules were
  on in that profile. Recorded in `ENGINE_FACTS.md` beside the three-switches
  table; P1 corrected in place in PT-60.
  ⭐ **Consequence worth keeping: this is the all-toggles-ON run F87's residual
  asked for**, so the five `Opt_` probes execute instead of SKIPping.
- **P2 ✅** five new modules active, clean details.
- **P3 ✅** all seven converted modules active. **The eight conversions are no
  longer unrun on the install axis** — but see §4 for what is still owed.
- **A1 ✅** (F90 defect climbs). **A2 ❌ missed** — predicted surface breaks would
  fluctuate as drones repaired them; they accumulated monotonically instead. Cause:
  no drone coverage on the cheat-built surface cables. Harmless; it makes surface a
  cumulative counter too.

---

## 2 · ⛔ THE DEFECT THIS PROMPT MUST VERIFY FIRST

**`Fix_AstrogeologistExtractors`' load-time heal was NOT idempotent, and the fix is
committed but UNTESTED.**

**Observed at the keyboard:** load `f95 baseline` with the pack on → correct
(`…=1 …=1`). Save, reload → **`AutomaticMetalsExtractor=2 MicroGAutoWaterExtractor=2`**.
The heal re-applied. **Every load added another +10%, without bound.**

**Root cause, established:** `Effect_ModifyLabel:OnApplyEffect` keys the modifier by
the **effect object** — `colony:SetLabelModifier(self.Label, self, …)`.
`label_modifiers` is a **persisted** field, so a save deserialises its **own copy**
of that key. The original presence check compared object identity, which can never
match across a save/load, so it re-applied every time. Vanilla's own ten entries
never hit this because `EffectsApply` runs once at game start and nothing re-applies
them on load.

**The fix (committed, see `git log`):** test by **property** (`m.prop == effect.Prop`
on that label) instead of identity, and additionally **remove duplicates** already
present, so saves inflated by the broken version are repaired.

### ✅ JOB 1 IS DONE — VERIFIED 2026-08-02, SKIP IT

Verified at the keyboard after a **full game exit and restart** (a Mod Manager
re-enable was not enough — the edited Lua only loads on a real reload; an
in-session file edit is invisible to a running game). Fixture `f95 healed`, which
carried the duplicates:

- after restart + load → **`MetalsExtractor=1 WaterExtractor=1 AutomaticMetalsExtractor=1 MicroGAutoWaterExtractor=1`** (duplicates cleaned, 2 → 1)
- after save + reload → **still all `=1`** — no re-application, no growth

**The property-keyed test is idempotent across a save boundary and the duplicate
repair works.** Nothing further owed on F95's heal.

⚠️ **Method note for anyone re-running this:** editing a `Code/*.lua` file while
the game is open changes nothing in the running session. Exit fully and relaunch.

### Original job-1 instructions, kept for reference only

Fixture already exists: **`f95 healed`** (an Astrogeologist save carrying the
duplicates). Load it with the pack on and run:

```
*r local c=rawget(_G,"UIColony") local out={} for _,L in ipairs{"MetalsExtractor","WaterExtractor","AutomaticMetalsExtractor","MicroGAutoWaterExtractor"} do local m=c and c.label_modifiers and c.label_modifiers[L] local n=0 if m then for _ in pairs(m) do n=n+1 end end out[#out+1]=L.."="..n end ConsolePrint(table.concat(out," "))
```

- **Expect all four `=1`**, and a log line `removed N duplicate extractor modifier(s)`.
- **Save and reload again → still all `=1`, and NO heal or removal line.** That is
  the idempotence proof the first attempt failed.
- ⚠️ If it still climbs, **stop and report** — do not paper over it. It would mean
  the property test is also wrong and the heal must be redesigned.

⚠️ **This is the second idempotence defect in this batch.** `Fix_SaintBlessing`'s
heal had the same class of bug (re-applied every load; fixed in `991c5dc` with a
presence check). **Both heals were written by the same session and both were wrong
in the same way.** Treat every load-time heal in this pack as suspect until proven:
**the general lesson is that "idempotent" and "one-shot" are different properties,
and an identity-keyed presence test is worthless across a save boundary.**

---

## 3 · Remaining leg work, in cheapness order

Fixtures all exist and are saved. **Do not rebuild any of them.**

| # | save | what to run | predictions |
|---|---|---|---|
| 1 | `f95 healed` | §2 above | all `=1`, duplicates removed, second load silent |
| ~~2~~ | ~~fresh Astrogeologist game~~ | ✅ **DONE 2026-08-02** — fresh game read **all four `=1`** with no `LoadGame` involved. `EffectsApply` applies our `PlaceObj` entries. **F95 is now verified on every path; nothing further owed** | — |
| ~~3~~ | ~~same throwaway~~ | ✅ **F96 DONE 2026-08-02** — `placed: true indestructible: true` → `survived meteor-path destroy: **true**` → `survived CheatDestroy: **false**`. Control held. **F96 verified; nothing further owed** | — |
| 4 | `F59 TEST1` | **F91** | `deleted 1 invisible track shell(s)`, shell count → **0**; then Ctrl+click another track **with the pack on** → count stays **0** (half A in play); save as `F59 TEST2`, reload → **no** heal line |
| 5 | `f90` | **F90 pack-ON leg** | **B1** underground stays **0** · **B2** zero `[LUA ERROR]`, especially none from the empty filtered list · **B3** surface still breaks (control — frag 2 is pure surface, takes the fast path) · **B4** after the storm frag 1 still reports `connectors 1668` (the §3a restore, on a real persisted fragment) · **B5** no `SMRFixPack` orphan error |
| 6 | `TEST 2H` | **the main PT-60 run** | `*r SMRTest.RunAll()` for P4/P5 · Saint heal line for **10** blessings · then unpaused play for P6/P7 |

**`TEST 2H` facts already established** (NASA / rocketscientist / sol 285,
`save_game_id HdmSxGs6kyd0uz6-`): **10 Saints, all 10 in domes** — F92's heal has
ten live targets. **No track shells, no `rocket_fuel_key`, not astrogeologist**, so
P8's other two halves and **P9 are not readable there** — record them as
"preconditions absent", not as passes.

### Console commands you will need

```
*r local un,ub,sn,sb=0,0,0,0 AllMapsForEach(true,"BreakableSupplyGridElement",function(e) if e:GetMap()~=MainMap then un=un+1 if e.auto_connect==true then ub=ub+1 end else sn=sn+1 if e.auto_connect==true then sb=sb+1 end end end) ConsolePrint("underground "..ub.."/"..un.." | surface "..sb.."/"..sn.." | sol "..tostring(UIColony and UIColony.day))
```
```
*r for _,res in ipairs{"electricity","water"} do for i,f in ipairs(MainCity[res] or empty_table) do local u=0 for _,c in ipairs(f.connectors or empty_table) do local b=c.building if b and IsValid(b) and b:GetMap()~=MainMap then u=u+1 end end ConsolePrint(res.." frag "..i..": connectors "..#f.connectors.." underground "..u.." breakable "..tostring(f:IsBreakable())) end end
```
```
*r local n=0 AllMapsForEach(true,"TrackBase",function(t) if t.elements==false and t.elements_under_construction==false and t.assigned_vehicles==false and t.demolishing then n=n+1 end end) ConsolePrint("shells: "..n)
```

---

## 4 · Things that are NOT what they look like — read before interpreting any log

1. ⛔ **`[LUA ERROR] attempt to index a nil value (global 'SMRFixPack')` from
   `Fix_MeteorFrequency.lua(95)` on a PACK-OFF load is EXPECTED and is NOT ours to
   fix.** It is a **pre-Tier-1** captured body — proven by its locals (`meteors`,
   `spawn_time`, `warning_time`), which exist only in the old §1.5 Meteors-thread
   copy (`d28bf4c`) and not in the current wrapper. Tier 1 stopped *new* saves
   capturing it; it cannot reach into a save already carrying one. **This is live
   evidence that the shipped "update, load, save, then uninstall" procedure is
   necessary, and it is D13 material.** Do not count it against this batch.
2. **`Unpersist missing permanent: Mod/SMR_CommunityFixPack`** on a pack-off load is
   **already documented** in `ENGINE_FACTS.md`'s three-switches table. Not a finding.
3. ⛔ **A pack-OFF session cannot establish a disaster baseline in general.** F81's
   defect defers dust storms and cold waves forever, and **the pack is what clears
   it** (`OnMsg.MeteorStormEnded` + the `PostLoadGame` sweep). The `f90` fixture is
   safe only because `DisastersPredicted set: 0` was verified on its stored state.
   **Re-check that flag before any future pack-off disaster leg.**
4. **`FlushLogFile()` lags console output by ~5-10 s.** Wait before flushing; a
   missing reading is usually this, not a failed command.
5. **`SMRFixPack.Log` writes via `ModLog` only** (`00_Core.lua:32`), so
   `ListFixes()` output **never echoes on screen** — read it in the log file.

---

## 5 · F96's live test — designed, never run

Both saves in the campaign are `mystery: none`, so no Sinkhole instance exists
anywhere and the probe's instance half reads zero. The test below manufactures one
using only shipped globals. **No debug build is needed** — the retail console has
everything (a MarsDebug session would only add `debug.getinfo` for the eight
standing `[install]` probe SKIPs, which is a separate sitting).

```
*r local s=PlaceBuildingIn("Sinkhole", MainMap) SMRTest.sink=s ConsolePrint("placed: "..tostring(IsValid(s)).." indestructible: "..tostring(s and s.indestructible))
*r local s=SMRTest.sink DestroyBuildingImmediate(s,{dont_notify=true,reason="SMRTest"}) ConsolePrint("after meteor-path destroy, still valid: "..tostring(IsValid(s)))
*r local s=SMRTest.sink s:CheatDestroy() ConsolePrint("after CheatDestroy, still valid: "..tostring(IsValid(s)))
```

`DestroyBuildingImmediate` is **the exact call the large-meteor branch makes**
(`Meteors.lua:821`). `CheatDestroy` is the **positive control** — it opens with
`self.indestructible = false` (`Building.lua:1813-1820`), so it must succeed;
without it, "survived" could mean the call did nothing.

⚠️ **Trap for the tester:** because `CheatDestroy` clears the flag first, **the
in-game destroy-building cheat will always kill a sinkhole regardless of our fix.**
That is by design and must not be read as F96 failing.

⚠️ A full meteor end-to-end via `CheatMeteors` is **not** worth it: only
`BaseMeteorLarge:Explode` destroys buildings and the cheat takes a *type*, not a
size, so it is an RNG wait with no guarantee of hitting the hex.

⚠️ If `PlaceBuildingIn` errors (SinkholeBase has firefly logic that may expect
mystery state), **paste the error** — that is a finding about testability, not an
obstacle to route around.

---

## 6 · On completion

1. Flip the seven entries from `built` to `fixed` **only where the leg supports
   it** — both places (index row + heading tag), never one without the other.
   ⚠️ **F90 and F93's live halves are NOT takeable on the current fixtures** and
   stay as needs-eyes riders; F96's live half rides §5. Say the narrower true thing.
2. STATUS: batch results + remaining tail. **Counts are already re-derived and
   correct** (79 registered / 73 default-active, 85 probes, 108 rows = 96 F + 12 D,
   38 C) — do not re-increment, and note the standing false positive: both
   `SMRFixPack\.Register\(` and `SMRTest\.Register\(` also match their own
   definition lines.
3. Outbox → `9_d10_workshops_build_opus.md`. Anything C23-touching → `8c` (already
   has its gate note).
4. **Append the §2 lesson to prompt 12's job-7 seed list** — two heals by one
   session, both non-idempotent, both caught only by a keyboard reload. That is a
   **new shape**: the existing corpus is about docs drifting; this is *code* whose
   defect is invisible to source review and to the probe, and only a save/load
   round trip exposes it.
5. Delete this file, commit, push.

## What may not be claimed

No fix is `fixed` without its probe existing **and** the leg passing for it.
**No converted module may be called verified beyond `active`** until §3 item 5/6
run — install is not behaviour. Counts are claims: recount, never increment.
Every result commit carries its `PROBE SWEEP:` line.
⚠️ **Do not describe F90 or F95's evidence as "the leg passed"** — they are
before/after pairs taken on constructed fixtures, and the F90 fixture is
deliberately extreme (a 1668-connector all-underground fragment). That is fix
verification, **not** evidence about how often either defect arises in real play.

## Notes from upstream

### From chain 8b (2026-08-02) — the two things that cost the most time

- **Five of prompt 7's six approved specs had a defect in their supporting
  detail** — a wrong line citation, a method name that does not exist (`__exec`
  for `OnApplyEffect`), a self-check placed where running it would have deactivated
  the fix on every cold boot, two writes described as equivalent when only one was
  load-bearing, and an overclaimed `pcall` equivalence. Every *shape* survived;
  every *detail* had to be re-derived. All corrected on their entries and listed on
  prompt 12. **Treat "you should not need to re-derive this" as falsified.**
- **The owner's pushback repeatedly beat the agent's analysis.** The F81 pack-off
  confound, the "we can build the preconditions" call that produced F90's first
  in-play observation, and the reload that exposed the F95 duplicate were all owner
  catches. **When the owner challenges a stand-down, re-examine before defending
  it.**
