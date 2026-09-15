# ck144 (a) close-out sitting — 2026-09-15, owner at the keyboard, one boot

Attended by `smr-bugfixpack-d1` (Fable). Log read AFTER the process exited, from
`%APPDATA%`, archived as `docs/archive/logs/ck144a_Mars.exe-20260915-11.11.26-6a91a190.log`
(756 lines; `Debug::Done` present). A first launch the owner closed before the
sweep was stamped is `ck144a_prelaunch_Mars.exe-20260915-11.08.19-6a91a190.log`
(8 toolkit lines, mod-load only, nothing pressed). Pack `819526f`, TestKit `fd9bd47`
(the stamp names `f5fa650`; the only change between the two is the stamp itself).
Game 1.1.0.403908, build 24995074, fixture `SMRTK_490` (Sol 490, all three mods).

## Why this sitting is small

The owner ruled 2026-09-15 that the play clauses ck144 (a) still carried
(A5 c2 / A9 c4–c5 / F117's station recipe) are closed by FIELD EVIDENCE — fixes
that fail loudly, live for weeks with thousands of daily players and no report —
and that A3 (F118, module deleted 09-12) and A10 (optional pack-off boot) are
struck. What remained was the first `RunAll()` on the rebuilt kit under a fresh
sweep (ck184 b) plus witnessing TestKit `f5fa650` by hand. ⛔ The ruling itself
is the documentation agent's to home; this file is the evidence, not the ruling.

## Boot health (`tools/logscan.py`, verbatim shape)

46 modules seen, applied 46 (heal-aware; `SaintBlessing` inactive at :144, healed
ACTIVE by :165 — the documented shape). Opt-in pack 8/8. **16 error-shaped lines,
all inside the RunAll block, all `[SMRTest]` probe verdicts** — the six ERROR
names twice each (file + console tap), `AnomalyCaveInMap` FAIL twice, and
`ArrivalDeathsChooseDomeArg` PASS twice (its message quotes the throw it proves).
No `[LUA ERROR]` outside the probes. Age: all this boot.

## What ran, by the log line

| step | line(s) | reading |
|---|---|---|
| console bootstrap (C-6) | :129 `console enable requested (flag set, no overlay)` | ✅ the `set_global` route landed first; no `ShowConsoleLog` overlay at load |
| slot 1 status | :286 `slot_1 discriminates=true taint=false eligibility=UNAVAILABLE:sandbox` | ✅ |
| slot 2 preflight | :293 `PROBE_PREFLIGHT clean=true hits=0 checked_at=2026-09-15T15:08:24Z pack=819526f… kit=f5fa650…` | ✅ **fresh stamp, same-day, current HEADs** — the ck184 shape did not recur |
| RunAll | :697 `counts={ERROR:6,FAIL:4,PASS:69,SKIP:18}` under that stamp | ✅ **ck184 (b) served: the owed first RunAll ran under a fresh sweep** |
| depot fill (C-1) | :702 `selected_fill before=1497117 after=4000000 object=MechanizedDepotFood(7128) resource=Food` | ✅ the mechanized branch now carries numbers |
| depot empty (C-1) | :705 `selected_empty before=4000000 after=0` | ✅ |
| watch on `bogus` (C-5) | :710 `watch_field field=bogus … status=OK` — configure only, **never armed** | ⚠️ **NOT RUN.** The refusal lives at ARM time (`74` `field_prepare`); the attending script said "Configure", which only stores the name. Attendee's error, not a defect |
| watch on `working` (08b item 9) | :718 `ARM baseline=false` → :721 `TRIGGER before=false after=true object=Spacebar(6173)` | ✅ **08b's one unrun leg fired** |
| end-of-boot reads | :726 `TAINT_READ used=false` · :729 `ELIGIBILITY UNAVAILABLE:sandbox` | ✅ requirement (A) taint half CLEAN after fill/empty; eligibility as always |
| editor colour (C-3) | owner, on screen: *"The text is still white"* — in `76`'s field box AND `74`'s editors (`491`, `trigger_sol`) | ❌ **NOT FIXED; 99 §9's mechanism is REFUTED in play.** See below |

## RunAll, by name — identical to 08b's, now under a fresh stamp

**FAIL (4):** `DomeFreeSpaceMismatch` · `LayoutTechLock` (fix not registered — module
retired 09-12, probe not) · `AnomalyCaveInMap` · `C47OpenFarmSeedBufferShape` (Herbs 100→50).
**ERROR (6):** retired `LanderCargoRatchet` / `DroneUnreachableForever` / `AutoExportPriority`
(`GetAutoModeThresholds` / `MarkUnreachable` nil) · `ClassicRockets` (`IsSpecialAutomode` nil,
`UniversalRocket.lua:1894`) · `CohortHousing` + `NoHomeless` (`GetRadius` nil, `Colonist.lua:3268`).
**SKIP (18):** `FactionFundingCheck` · `TrainsToVoid` · `ShelterReflex` · `BrokenTrackSalvage` ·
`TrackSalvageWipe` · `LakeEntombment` · `GhostFarmOxygen` (introspection unavailable on retail) ·
`MoraleComfortTooltip` · `IndependenceTerraforming` · `TechDescriptionBuilding` ·
`SpaceYDroneCapBullet` (retired) · `DroneTransportMinors` · the six `SaveRescue*` (mod not installed).
⇒ **Zero change from 08b's run.** The 4 FAIL + 6 ERROR are the probe-maintenance list
STATE already names; nothing new regressed and nothing was cleared.

## Findings

1. **C-3 refuted.** 99 §9 said an editor that sets its own `TextColor` wins over
   `ConsoleLog`'s white, citing `491` going dark in `74`'s editor during 08b. In this
   boot `74`'s editors are white again (owner's screenshot: `491`, `trigger_sol`) and so
   is `76`'s box after the same pair was added. **Lead, not a verdict:** `174a601`
   registered the control TextStyle LAZILY after 08b's "491 went dark" observation; a
   style applied after construction would overwrite the per-control `TextColor`
   (`XFontControl:SetTextStyle` copies the style's colour, `XControl.lua:432-438`).
   ⚖️ **Owner 2026-09-15: low priority, do not address unless another issue needs it.**
   Recorded; not routed.
2. **"Way less logs on screen"** (owner). Expected from C-6: the persistent console-log
   overlay `ShowConsoleLog(true)` forced at every boot is gone, so prints now show
   briefly and fade instead of stacking. The full overlay is one key away (F9, per 03B
   D2). Nothing is lost — the file and `SMRTK_COPY` (:739, 206 lines, `truncated=false`)
   carry everything.
3. **C-5 unwitnessed by attendee error** — arm, not configure, is where the refusal
   fires. One press at any later sitting; no dedicated leg.

## What this does NOT claim

No play claim for C-5. No eligibility PASS. No probe-maintenance progress. The
A5/A9/F117 clauses were not run — they were closed by the owner's field-evidence
ruling, and the entries keep their recipes for a countering report.

## DRIFT (mine)

- The attending script sent the owner to "Configure field watch" for the `bogus`
  witness; the refusal is at ARM. Read the code path before writing a witness step.
- The sweep was run while the owner's first launch was still up; I asked for a
  relaunch rather than writing the kit under a running game (SLOTS rule), which
  cost two minutes and produced the honest stamp.
