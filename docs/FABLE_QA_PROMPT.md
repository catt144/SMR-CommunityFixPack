# Fable QA-session prompt — after wave 3 (sessions 3+4)

Paste everything below into a fresh Claude Code session (Fable). It follows the
Opus build leg that finished the wave-3 queue; the build-session prompt is in
`docs/OPUS_BUILD_PROMPT.md`.

---

You are doing the **QA leg** for the Surviving Mars: Relaunched "Community Fix
Pack". The implementation leg is done: the wave-3 queue is complete, 48 tracked
defects are fixed across 47 registered modules, and **18 of them have never been
run in-game at all**. Your job is to find out which of them actually work, and to
audit the ones that are most likely to be wrong.

**First, read these (in order) from `C:\Dev\SMR-BugFixPack`:**
1. `docs\STATUS.md` — snapshot, the blocked table, the wave-4 queue, and the
   hard-won engine facts (read the WHOLE facts list; several were learned the
   hard way and re-deriving them costs a day)
2. `docs\FIX_POLICY.md` — the patching rules the fixes are audited against
3. `docs\BUGS.md` — the tracker. Every fix has an entry; the wave-3 entries carry
   an "*Implemented differently, on better evidence:*" or "*Blocked:*" paragraph
   explaining any divergence from the original sketch. Those paragraphs are the
   claims you are auditing.
4. `docs\TESTING.md` + `docs\PLAYTEST_CHECKLIST.md`, and the Test Kit repo
   `C:\Dev\SMR-BugFixPack-TestKit` (probe conventions in `Code\00_TestCore.lua`,
   wave-3 probes in `Code\30_Probes_Wave3.lua`, autorun harness in
   `Code\95_AutoRun.lua`)

The game's Lua source (read-only, NEVER modify) is at
`A:\SteamLibrary\steamapps\common\Project Spark\ModTools\Src`.

## Task 1 — the A/B RunAll pair (do this FIRST, before any audit)

It has not been run since wave 2. Nine files of fix-pack Lua and eleven probes
have been written since, **and none of it has ever been parsed by a Lua
interpreter** — there is no `lua` binary on this machine, so the build leg
reviewed the syntax by eye and nothing more.

That makes the first question blunt: **does every file load, and does every fix
report `applied`?** A syntax error inside `apply` is caught by the registry's
`pcall` and shows up as `error`; a *parse* error in the file itself is not caught
at all — the file simply never loads, `SMRFixPack.fixes` is missing that id, and
its probe reports "not registered". Check for both.

Procedure (from STATUS.md's harness notes):
- baseline = fix pack `metadata.lua` `code` list emptied; B = full pack;
- unattended: add `"Code/96_AutoRunFlag.lua"` to the **Test Kit's** metadata
  `code` list (or pass `-smrautorun`), launch via Steam, diff the two logs in
  `%AppData%\Surviving Mars Relaunched\logs`;
- `SMRFixPack.ListFixes()` in the console is the quick manual equivalent.

Expected: **47/47 applied** (46 fixes + the sanitizer), one deliberate exception —
`ClassicRockets` must report `inactive` with an opt-in reason, because it is an
opt-in module (see Task 4).

Then run the pair a second time with `SMRFixPack_Optional = { ClassicRockets = true }`
set before load, so D01's probe stops SKIPping and actually asserts.

## Task 2 — probes that may not be discriminating

The last A/B pair reported "19/19 FAIL→PASS". At least one of those 19 was not
testing anything: the F51 `ShuttleTransportCache` probe compared only the value
returned and PASSed in **both** halves. It has been rewritten this session to
count calls into `GetTransportationModeToCommunity` instead.

**Assume there are more like it.** Sweep every probe for the same weakness: a
probe that only compares a return value is non-discriminating whenever the fixed
and unfixed paths can produce the same value. The reliable pattern is to assert
on the *mechanism* — was the underlying function called again, did the guard
fire, did the filter run — the way `ShuttleTransportCache`, `RocketDroneChurn`
and `MirrorSphereSite` now do.

For each probe, state plainly: does it fail in the baseline run? If it passes
both halves, it is not evidence and should be reported as such, not counted.

## Task 3 — audit these fixes specifically (highest risk first)

Every one of these diverges from its original sketch, on evidence written up in
the BUGS.md entry. Check the evidence, not just the code.

1. **F59 `Fix_FreedHousingNotice.lua`** — hooks `Colonist:SetResidence` instead of
   the sketched `Residence:RemoveResident`. The argument is that `RemoveResident`
   runs mid-way through `SetResidence`, before `home:AddResident(self)` and
   before `self.residence` is updated, so notifying there lets a homeless
   colonist take the slot the mover is about to occupy — one line before
   `assert(self:GetFreeSpace() > 0)`, which does not unwind in this engine.
   Verify that reasoning, and verify the post-hook cannot recurse (a homeless
   colonist has `residence == false`, so its own `SetResidence` should not
   re-trigger the notification).
2. **F71 in `Fix_LanderCargoRatchet.lua`** — that file now serves TWO tracker
   entries (F68 + F71) and its copy of `CreateAutoCargoRequest` drops the shipped
   `assert(res_type == "Resource")`. Re-verify the header's source line
   citations against `UniversalRocket.lua`, and confirm the `pcall`-wrapped
   flight-policy lookup degrades to the shipped alphabetical order rather than
   erroring when a rocket is in an unexpected state (the F68 probe drives it with
   a rocket that has no `GetDepartureLocType`, which is exactly that case).
3. **`Code/90_SaveSanitizer.lua`** — this WRITES TO SAVEGAMES. The F35 pass adds
   a label modifier under `SMRFixPack_F35_<label>`. Confirm: it cannot double-buff
   (any existing percent modifier for that prop on that label must make it skip);
   it is idempotent across repeated loads; and the F03 sweep's handle-matching
   cannot strip a live building's bonus. Then re-run **PT-20 (uninstall safety)** —
   it matters more now than it did.
4. **F72 `Fix_AsteroidLanderAvailable.lua`** — a permissive post-wrapper. Confirm
   it never *blocks* anything the shipped predicate accepted, and that its added
   scan really does mirror `GetRocketsForExpedition`'s predicate including the
   supply-pod exclusion.
5. **F54 `Fix_ShuttleHubOffAvailable.lua`** — this one makes a predicate STRICTER,
   the only fix in the wave that does. Confirm the enumeration in the BUGS entry
   is complete: are `"TurnedOff"`, `"DomeNotWorking"`,
   `"ExceptionalCircumstancesDisabled"` and `"ExceptionalCircumstancesMaintenance"`
   really the only states the shipped tolerant clause admits? If there is a fifth,
   a hub could stop counting when it should count.
6. **F34(d) `Fix_LandscapeUnitFilter.lua`** — reproduces the file-local
   `foreach_params_unit` table. Confirm the engine's `Landscape_ForEachObject`
   does not cache or mutate that table in a way that makes a private copy behave
   differently from the shipped one.

## Task 4 — the opt-in module

`Code/Opt_ClassicRockets.lua` (D01) is the pack's first opt-in module and the
first file using the `Opt_` prefix rather than `Fix_`. It ships only the *fuel*
half of D01 (a parked rocket keeps its launch ration requested); the standing
Rare Metals export half is deliberately unwritten.

Check: it stays inactive by default; `SMRFixPack_Optional = { ClassicRockets = true }`
turns it on; with it on, a parked rocket is refuelled and there is no
"RocketRefueled" notification spam (both notification branches in
`UpdateCargoResourceRequests` require `arrival_loc`, which is exactly what a
parked rocket lacks — verify that claim); and F69's asteroid-lander reserve still
works, since the two wrappers chain.

## Task 5 — still open from the previous QA session

- **F68 capacity cap, in-game** — the requested floor does not debit remaining
  hold capacity, so with multiple exports a request can exceed what is left and
  the rocket can stick at "loading" and never depart. F71's reordering changes
  *which* resource hits the capacity wall first, so the symptom may present
  differently now. **PT-17 case B and PT-32 together.** If it sticks at
  "loading", that is a real FAIL needing a code change — record the export pair,
  hold contents and status text.
- **F44 curve-ended remainder track visuals** — in-game check.
- **F55** — the open question in PT-10: do drones still enter a dome after the
  roof is opened? The Lua half turned out not to be actionable; only play answers
  this.

## Task 6 — bring four decisions back to the user

These are parked as `blocked` in BUGS.md and are NOT waiting on code. Read each
entry's write-up, sanity-check the reasoning, and put a recommendation in front
of the user:

- **F32** — the shipped data already carries the fix for the only preset the
  described mechanism applies to. Close as `wontfix`?
- **F48** — needs one in-game test (a save with a healthy multi-station network
  **and** a meteor-damaged track) before the repair can ship.
- **F62 / F63** — the remedies are behavior changes, not defect repairs. In scope
  at all, and if so, as an opt-in module alongside D01?

## Task 7 — repo hygiene

**The Test Kit repo has no git remote and its branch is `master`, so it has never
been pushed** — 48 local commits, 10 of them from the last build session. Decide
with the user whether it becomes its own GitHub repo or an orphan branch on
`github.com/catt144/SMR-CommunityFixPack`, then wire it up. (`gh` is not
installed on this machine.) The fix pack itself is pushed and clean.

Also: three `[DRAFT NOTE]` markers remain in `docs/MOD_DESCRIPTION.md`. The one on
the ClassicRockets module is load-bearing — the released text must not promise
the unwritten Rare Metals export half.

## Hard rules — engine facts that shipped real bugs when violated

- **Mods run in a SANDBOX on all platforms** (unpacked dev mods too): no `debug`,
  no `io`, `os` is `{time}` only, no `Async*` file APIs, no load/dofile/require.
  `rawget(_G, "X")` works (safe wrapper). New globals you assign land in the real
  `_G` — but **`rawset(_G, k, v)` writes to an invisible shadow table: never
  rawset onto _G** (plain assignment instead; in the Test Kit use
  `SMRTest.SetGlobal` / `WithGlobals`).
- **`error()` and `assert()` do NOT unwind mod code** — the engine prints and
  execution CONTINUES with the next statement. Never use them for control flow;
  `pcall` still catches genuine runtime errors. This cost four bogus FAILs and
  ten ERRORs in the first A/B pair.
- Mod code loads BEFORE classes are flattened: an inherited method reads nil on a
  subclass classdef — `apply()` self-checks must look methods up on their
  DECLARING class.
- **Presets do not exist when mod code loads** (`LoadData` → `Msg("DataLoaded")`,
  `CommonLua\Dlc.lua:640-662`). Data patches run from `OnMsg.DataLoaded`.
- `g_Consts`, `Landscapes`, `MarsScreenLandingSpots`,
  `g_TransportationModeToCommunityCache` are GameVars — read them inside patched
  functions, never at apply time. `const` is fine at apply time.
- `IsValid()` rejects the plain tables probes use as stand-ins; probes swap it via
  `WithGlobals`.
- `/` truncates (integer division). `#nil` / `next(nil)` / `ipairs(false)` are
  tolerated; boolean relational compares are not.
- Never modify anything under the game directory. No balance changes, no
  refactors beyond the verified defect.
- **Do NOT mark anything `tested`** — that status is earned only by the human
  playtest (`docs\PLAYTEST_CHECKLIST.md`, 35 tests). If the user reports playtest
  results, flip each PASSed fix's BUGS.md index row + heading tag to `tested`, and
  file each FAIL as a new finding with their notes.
- If an audit finds a fix is wrong, do NOT redesign it in place: record the defect
  with file:line evidence and put it in front of the user, the way the F53 and F12
  audit findings were handled in the wave-2 QA session.

**End of session:** update STATUS.md (A/B results, audit verdicts, anything newly
broken), commit with
`git -c user.name="SMR-BugFixPack" -c user.email="154917955+catt144@users.noreply.github.com"`,
push, and give a table of: fixes verified / fixes that failed / probes that don't
discriminate / decisions still needed.
