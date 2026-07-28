# Fable continuation prompt — playtest reports / playtest QA (rewritten 2026-07-27)

Paste everything below into a fresh Claude Code session (Fable). This is the ONE
live prompt: the old OPUS_BUILD / FABLE_QA / FABLE_PLAYTEST prompts are retired
(git history has them). Build state: **67 registered modules, 66/67 active
(ClassicRockets opt-in), F10 retired and deleted, latest clean A/B pair
2026-07-27 (logs 11.45.34 / 11.47.09), everything pushed.** The 2026-07-26/27
sessions were a long live-playtest run: 16 fixes now carry playtest status
(F36, F08, F74 via PT-24/06/39 post-wrap; F61 closed wontfix → D03 filed
same day; NEW vanilla F76 found live — depot resource picker off-cursor),
two of the three decision gates are cleared, and one new defect (F12's
"Food"-key collision) was found live, repaired, and A/B-verified same day.
What remains is playtest-driven plus one unblocked build item (D02).

---

You are continuing the Surviving Mars: Relaunched "Community Fix Pack" — this
session is most likely **processing the user's playtest reports** (or answering
playtest questions; queued build work is listed at the end).

**First, read (in order) from `C:\Dev\SMR-BugFixPack`:**
1. `docs\STATUS.md` — the "Playtest marathon — 2026-07-26/27" section AND the
   whole engine-facts list.
2. `docs\PLAYTEST_CHECKLIST.md` — the un-run tests, their save fixtures, and the
   "Reporting protocol" section at the end. Completed tests + their result
   evidence live in `docs\PLAYTEST_ARCHIVE.md` (completed sections move there,
   protocol step 8).
3. `docs\BUGS.md` — the tracker you will be updating.
4. `docs\FIX_POLICY.md` — binding rules for any code you write.

Game source (read-only, NEVER modify):
`A:\SteamLibrary\steamapps\common\Project Spark\ModTools\Src`.
Both mods load through junctions from `C:\Dev\SMR-BugFixPack` and
`C:\Dev\SMR-BugFixPack-TestKit` — confirm the user is not mid-playtest before
any edit the game could load (mod code loads at LAUNCH only; doc edits are
always safe; A/B legs need the game to be free).

## Processing playtest reports

- The playtest is the ONLY thing that flips a fix from `fixed` (probe-verified)
  to `tested` (ships in the release text). Partial reports are fine — process
  what was reported, leave the rest untouched. Record results in the checklist
  (preserve the user's own words; add dated evidence notes), flip BUGS statuses
  in BOTH places (index row + heading tag), move the completed section to
  `PLAYTEST_ARCHIVE.md`, and keep STATUS's session record current.
- FAILs: diagnose from the logs in `%AppData%\Surviving Mars Relaunched\logs`
  before touching code — and when the log can't see it, instrument LIVE from
  the console by wrapping the relevant globals with ConsolePrint taps (the F12
  churn hunt in the archived PT-07 + the F12 BUGS entry is the worked example:
  five wrong hypotheses were killed by timestamps, not speculation). Mechanical
  repairs land with a re-verified A/B pair; redesigns go to the user.
- **One decision gate remains:**
  * **PT-37** → F48: PASS = build the corrected fixup behind a one-shot flag;
    FAIL = `wontfix`. (PT-36 → F10 CLOSED `wontfix` + file deleted 2026-07-27;
    PT-38 → D02 measured, corrected, and unblocked 2026-07-27; PT-14 → F61
    CLOSED `wontfix` 2026-07-27, deletion staged, ask re-filed as D03.)

## Playtest state as of 2026-07-27 (evidence in PLAYTEST_ARCHIVE.md)

- **Done → `tested`:** F03 (PT-02), F05 (PT-05), F08 (PT-06 — 5★ +23/$544.5M
  vs tanked ≤2★ +7/$94.5M), F12 (PT-07 — whose FIRST run
  caught a second F12 defect, repaired + A/B same day), F13 (PT-08),
  F74 (PT-39 — trade rocket refused by cursor AND route; found F76 en route),
  F36 (PT-24 — geologist demand 11→0 on the ExtractorAI grant; 38 engineers +
  2 medics + zero geologists graduated), F44+F45
  (PT-03), F47 (PT-45), F50 (PT-04), F51 (PT-12), F54 (PT-34), F66 (PT-41);
  F52 `tested*` (PT-13). F49(b) resolved as no-defect (PT-46). F10 CLOSED
  `wontfix` (PT-36, both-ways evidence incl. a real $544.5M read). F61 CLOSED
  `wontfix` (PT-14 — quarantine by design; deletion staged, ask re-filed as
  D03). D02 gate
  done (PT-38): the dismiss window is **120,000 GAME-ms = 4 game hours**, not
  wall-clock — corrected in the checklist cautions and the D02 entry.
- **PT-06 (F08) DONE 2026-07-27 → `tested`:** 5★ half "+23 applicants,
  $544.5M"; tanked half (stripped dome, Earthsick early leavers counted)
  "+7 applicants, $94.5M" — the clear split. Evidence + the Src mechanics
  notes (no sols/reason filter on departure rewards; stat<30 caps rating at
  the 2★ tier) are in the PT-06 archive section and on the F08 entry.
- **Passive:** PT-01's silence-watch — the watchdog self-reports (`WATCHDOG —
  Meteors thread silent … last phase 'X', thread ALIVE|DEAD`); THAT log line is
  the F02 root-cause evidence if it ever fires. The F18 savegame sweep
  announces itself on load of an affected save (`corrected the
  already-researched tech's stored discount from 10% to 20%`) — worth capturing.
- **Everything else is un-run:** PT-09..PT-11, PT-15..PT-19 (fixture saves
  B/D/E per the checklist's fixture table; PT-14 DONE 2026-07-27 — premise
  falsified, see the F61 gate above), PT-23 + PT-25 + PT-27..33 + PT-35
  (wave-3; PT-24 DONE 2026-07-27 → F36 `tested`; PT-26 resolved-unrunnable →
  D04 filed),
  PT-37 (last gate, attended), PT-40/42/43/44 (wave-4; PT-39 DONE 2026-07-27
  → F74 `tested`), PT-47 (wave-5),
  PT-46's untested tail (F49(d) train cap, F49(a) instant-track palette),
  PT-20/21/22 (uninstall / soak / log hygiene).

## Queued build work (each unblocks on its trigger)

- **D02 `Opt_AcknowledgedWarnings` — UNBLOCKED, next build leg.** Spec on the
  D02 entry with the corrected cadence (4 game hours; at ultra the nag is every
  few REAL seconds, so the case is stronger than premised). Per-object
  acknowledgment, opt-in module, own probe; suppression is per notification id
  (`SuppressedNotifications[id]`) — verified live.
- **F61 retirement mechanics (decision DONE 2026-07-27, same leg):** delete
  `Code/Fix_HomeDomeMigrationGate.lua` + its metadata line, drop/repurpose the
  TestKit probe, re-verify A/B (expected numbers shift by one probe; F10
  precedent — the doc side is already recorded).
- **D03 `Opt_ResidencyControl` (user decision 2026-07-27, build queued):** new
  per-dome "closed to new residents" policy — UI row appended by post-wrapping
  `sectionDome:Init` (+ `sectionMicroGHabitat:Init`), flag
  `SMRFixPack_closed_to_new_residents` on the Dome object, gates on
  `Community:CanAcceptNewColonists` + the arrival path; quarantine untouched.
  Full spec + the move-in-path survey list on the D03 entry.
- **D04 `Opt_MultipleSuns` (user decision 2026-07-27, build queued, same leg):**
  PT-26 found F39's second sun is impossible in the unmodded game (build-once
  wonder, colony-wide). The module lifts the limit
  (`BuildingTemplates.ArtificialSun.build_once = false`, preset-patch timing)
  and absorbs `Fix_SecondArtificialSun.lua` unchanged; the standalone fix file
  is deleted in the same leg and its probe reworked to the ClassicRockets
  SKIP-unless-opted pattern (expected A/B numbers shift again — combine with
  the F61 renumbering). Spec on the D04 entry; single-sun baseline for its
  future playtest is in the PT-26 archive section.
- **F02 root cause:** if the watchdog line ever appears, pull last-phase +
  alive/dead from the log and design the real repair (an alive-stuck Sleep
  points at how save/persist re-schedules persisted game-time thread wake-ups;
  the MeteorStorm thread — NOT restarted by our fix — wedged identically).
- **D01 export half** (user decision 2026-07-26: match the ORIGINAL game; the
  legacy loader `RocketBase.lua:1729-1736` is the spec — standing
  PreciousMetals demand to `max_export_storage`, any-drone flags, per-rocket
  `allow_export` toggle). Three research items on the D01 entry, incl. whether
  the original auto-offloaded RC transports (decides if F56 rides along). Own
  probe + playtest item; same `ClassicRockets` flag; extend MOD_DESCRIPTION's
  side-by-side when it ships.
- **F48** per PT-37's gate above.
- **F76 (NEW 2026-07-27, wave-6 candidate): depot resource picker off-cursor +
  unclickable** — vanilla P1 found live in PT-39 setup; full forensics + fix
  sketch (anchor-space conversion in `ResourceItems:Init`) on the entry. Still
  to capture from the user: `terminal.desktop.box`/`scale`, resolution + UI
  scale. MOD_DESCRIPTION false-report explainer flagged (draft note in place).
- MarsDebug attended `[install]` pass for the wave-4/5 fixes (SetupOnly mode;
  procedure + modal-dialog warning in STATUS's wave-3 QA section).
- Release checklist (STATUS): statuses to `tested` as reports come in, fpk
  target verification, MOD_DESCRIPTION final pass (only `tested` fixes ship in
  the list).

## Harness facts (hard-won — do not re-derive)

- Launch: `& "c:\program files (x86)\steam\steam.exe" -applaunch 3215050 -smrautorun`.
  A leg takes ~75 s; watch for Mars.exe to appear (up to 4 min) then exit.
  **Never kill on a short timeout** — no-kill watcher (25 min guard); harness
  watchdog 15 min.
- Baseline = overwrite fix pack `metadata.lua` with an emptied `code` list;
  restore with `git checkout -- metadata.lua`. **NEVER `git commit -a` while
  that edit is in the working tree.**
- Expected healthy numbers (2026-07-27, unchanged by the F10 deletion — its
  probe stays as a canary on the shipped function and is the baseline's 1
  PASS): baseline **1 PASS / 58 FAIL / 11 SKIP / 0 ERROR**; full pack
  **59 PASS / 0 FAIL / 11 SKIP / 0 ERROR**, 66/67 active (ClassicRockets
  opt-in inactive). The 11 SKIPs: 9 `[install]` probes, ClassicRockets,
  TechDescriptionBuilding (F25 rides its playtest item). Synthetic-map noise
  unchanged: ~49 Flight.lua `objects_to_mark` errors + a few GameInit `attempt
  to call a nil value` lines in BOTH legs; a `[mod] Error in mod … Test Kit`
  line at quit is a shutdown artifact.
- **Retail console gotchas (cost us a day — in the checklist command table):**
  infopanel cheat buttons render but NO-OP without `Platform.cheats = true`
  (`NetSyncEvents.ObjCheat` gate), their presses ride the game-time sync queue
  (dead-looking while PAUSED, fire on unpause; `ObjCheat <method>` console
  print = delivered), and direct `SelectedObj:Cheat*()` calls bypass all of it.
  `SMRTest.Cls` wipes the on-screen console overlay. The TestKit console
  auto-enable works on NEW games too since the 2026-07-26 repair
  (InGameInterfaceCreated + WaitLoadingScreenClose; CityStart fires at map-GEN
  time and must not be used for UI-ready work).
- Parse sweep: python + luaparser,
  `ast.parse(open(f,encoding='utf-8-sig').read())`.
- Docs tooling: never round-trip a doc through PowerShell 5.1 `Get-Content`
  without `-Encoding UTF8` on both ends; prefer the editor's file tools.
  Git commit messages via single-quoted here-strings; no embedded double quotes
  (PS 5.1 native-arg quoting eats them).

## Hard rules

Same as ever (STATUS.md engine facts govern): sandbox on all platforms;
`error()`/`assert()` report-and-continue; self-checks read the DECLARING class;
presets only after DataLoaded (GlobalMaps exist EMPTY before it;
DataChanged(false) re-fires right after); GameVars only inside patched
functions; post-wrappers on command methods never run; `IsValid()` is falsy for
ALL pure-Lua objects; never modify the game directory; only the playtest flips
statuses to `tested`; mechanical repairs land with a re-verified A/B, redesigns
go to the user. Commit with
`git -c user.name="SMR-BugFixPack" -c user.email="154917955+catt144@users.noreply.github.com"`,
push the fix pack (TestKit stays local-only).

**End of session:** update STATUS.md and this prompt, commit, push, summarize.
