# The hotfix-2 sitting, part 2 — what the first evening did not reach

Paste into a fresh Claude Code session **with the owner at the keyboard**. This
supersedes the original brief, which ran on 2026-09-09 (`1480953`). **Tier 1 is
complete and green and is NOT repeated here.** What remains is nine in-play
controls, one optional leg, and three decisions.

**Staleness anchor: `1480953`.** `git log --oneline -15` · `git pull` ·
`ListAgents` before you touch anything.

> ⚖️ **WHAT CHANGED, and why this is a much smaller evening than the last one.**
> The pack has now **run in a game**. 44 modules install on two independent
> boots, the 95-probe suite reports no regression and no wrong removal, and the
> two bugs that reached players — F114 trains, F115 landscaping — were watched
> working. The catastrophic class is ruled out. **Everything below is a repair
> that is believed-correct-by-source and has never been observed**, which is a
> different and lesser risk. Nothing here blocks the upload on its own.

> ⛔ **`H-04` BINDS THIS WHOLE FILE.** A clean sitting is not clearance and this
> session never calls the release ready. It produces **readings**; the owner
> decides what they mean.

## 0 · Read this before planning the evening

⭐ **The single biggest saving available: rockets fly while you do other things.**
Rows **A2 (F117)**, **A4 (refuel toggle)** and **A5 (Edit Payload)** all need a
rocket. Their travel time is dead time. **Start A2's passenger rocket and A5's
trip FIRST, then work the cheap ground rows while they fly.** Done serially
these nine rows are ~50 minutes; overlapped they are closer to 30.

⇒ **Run §5 in the order given.** It is sorted by value, then by what can be put
in flight early. ⛔ **`A9` (track split) is LAST and that is deliberate** — it is
destructive and save-persistent, and running it earlier contaminates the colony
for every other row. The original brief had it fourth; that was a mistake.

Whatever is left when the owner stops gets **filed, not faked** (§7).

## 1 · Live todo list — REQUIRED, and the owner reads it to decide when to stop

Build it **before the first row**, one item per control, in §5's order. Mark each
the moment it completes; keep exactly one in progress. Put the **reading** in the
item text as you go, so the list answers "where are we" without re-reading the
transcript.

⚠️ **If a control turns out to be two things, split it in the list at that
moment.** Row 1 did exactly this last time — it was three clauses and only two
ran, and a single checkbox would have hidden that.

⚠️ There may be **no `TodoWrite` tool** in the session. If not, keep the list as
a visible block in each message. Same function, different surface — do not skip
it.

## 2 · Preconditions

| gate | how to check | last reading (`1480953`) |
|---|---|---|
| **Stale-probe gate** (mandatory, `WORKFLOW` element 7) | `grep -rln "TEMPORARY" Code/ ../SMR-BugFixPack-TestKit/Code/` — CLEAN is zero lines | ✅ CLEAN. ⛔ **Refuse to record any result without re-running it.** Put it in the todo list |
| **Force-inactive leg** `97_ForceInactive.lua` | commented out of the kit's `metadata.lua` code list | ✅ DISARMED — it must stay so. A forced module is a body pinned to an older build; it changes what the pack does (`EF-081`) |
| **Enable-path leg** `98_EnablePathLeg.lua` | same list | ✅ DISARMED |
| **Autorun harness** `95_AutoRun.lua` | `96_AutoRunFlag.lua` absent from the code list, no `-smrautorun` | ✅ armed but INERT. An attended launch behaves normally. Leave it |
| **`Mars.exe` not running** | `tasklist` — its own step | ⛔ before anyone edits loadable code |
| **`H-09` no packed folder beside the junction** | `ls "$APPDATA/Surviving Mars Relaunched/Mods"` | ✅ three junctions only. At equal version the unpacked one wins silently and the leg measures nothing |
| **Passage Network** | mod manager | ✅ unticked 09-09 — confirm it stayed that way |
| **Opt-in pack** | boot log line `Loaded mod items for:` | ✅ not enabled. ⚠️ **That line is the discriminator, not `Loaded mod def`** — the def line appears for any folder present |

**`H-06` — autosaves.** ✅ Already pre-copied 09-09 to
`C:\Dev\SMR-SaveBackup\20260909-hotfix2-sitting\` (five saves, including the
colony). ⛔ **Re-copy anything created since**, and note that loading a campaign
runs its autosave rotation and deletes the owner's autosaves (`EF-056`).

**The colony: `USA Sol 18`** — `BlankBig_02` / NASA / Sol 18 / `lua_revision
403908`, cheat-provisioned by design (not a confound). **All research is done on
this map**, so no row below is gated behind a tech.

> ⭐ **Verify the save rather than asking.** A `.savegame.sav` carries plain-text
> metadata in its first ~2 KB — `displayname`, `map`, `mission_sponsor_id`,
> `commander_profile_id`, `elapsed_sols`, `orig_lua_revision`, `active_mods`.
> Read it with a short Python ASCII-run scan. ⚠️ Match **`orig_lua_revision`** —
> a bare `lua_revision` match hits the *mods'* revisions first and reads wrong.

⛔ **1.0.7 saves cannot load on 1.1.0** (`EF-079`) — the whole fixture library is
branch-locked, so every row shares this one colony.

## 3 · ⛔ THE LOG DISCIPLINE — read this or you will record a false negative

This bit is not boilerplate. **Both traps below fired during the last sitting.**

1. ⚠️ **A log copied while the game is RUNNING is a PARTIAL log.** It produced
   two wrong counts on 09-08 (a "1" that was 6; a "30" that was 157). Re-read
   after `Mars.exe` exits before quoting any count or rate.
2. ⛔ **`FlushLogFile()` DID NOT WORK on 09-09.** After the landscaping rows the
   file was **byte-identical** — same size, same mtime, and no `>` console echo,
   while every other console command *had* echoed. A "0 errors" read at that
   moment would have covered nothing after the console work and would have been
   recorded as a pass. ⇒ **Treat only an exited-process log as authoritative.**
   The pack's `[CommunityFixPack]` lines are buffered; only `[SMRTest]` lines
   flush per line.
3. **Quit to desktop between phases** if a row's result depends on the log. Exit
   always flushes and writes `*** Debug::Done()` — that string is the proof the
   file is complete.
4. Use `tools/logscan.py` — ⛔ **never a hand-rolled grep.** The engine writes
   the `[LUA ERROR]` header two ways and only one carries a file path.

## 4 · ⛔ Known instrument noise — do NOT re-file any of this

The last sitting triaged all ten suite failures to the instrument. **If you
re-run `SMRTest.RunAll()`, you will see them again. They are not findings.**

| you will see | it is |
|---|---|
| `FAIL LandscapeCostGuard` `[retired]` | stub lacks `GetTargetAmount`, which 1.1.0's `InterruptExcessDeliveries` now calls (`ConstructionSite.lua:1385`). **Reaching that line proves the body delegated** — the message is backwards, the F105/F107 removal is confirmed |
| `FAIL LanderReturnFuel` `[retired]` | asserts a two-value return the no-destination branch never makes (`UniversalRocket.lua:1891-94`). Its meaningful clause passed at 3500 |
| `FAIL MoraleComfortTooltip` `[retired]` | structurally unpassable once retired — its PASS condition is the masking we removed. Its own title says *"expected SKIP … needs a screen check"* |
| `FAIL SaveSanitizerUpgradeLeak` `[behavior]` | outlived the pass it tested (deleted `f707903` under ck117) |
| `FAIL C47OpenFarmSeedBufferShape` `[behavior]` | 1.1.0 halved Herbs to 50 seeds/hex |
| 5 × `ERROR` | probe scaffolding on 1.1.0 methods that were removed. **No shipped `Code/` line calls any of them** |
| 7 × `SKIP [install]` | no `debug.getinfo` in a retail mod sandbox — by design |
| `[LUA ERROR] HGE::GetDomeAtHex` | the kit's `CaveInRubble`/`IsNearDome` stub gap, caught in a `pcall`. **A real header from a fake problem** |

⛔ **Any FAIL or ERROR *not* in this table is new and wants looking at.**

**Baselines to compare against:** `44 applied / 0 inactive / 0 errors`;
`58 PASS / 5 FAIL / 27 SKIP / 5 ERROR` = 95 probes. A different census is a
finding.

## 5 · The rows

⭐ **Start A2 and A5 in flight first**, then work downward while they travel.

| # | control | fix | ~time | what to do | PASS looks like |
|---|---|---|---|---|---|
| **A1** | **Asteroid habitat trait filter** ⭐ cheapest real result left | F-3 | 2 min | Open an asteroid habitat and **set a trait filter** | **No error line.** Before this build this threw. Bank it first |
| **A2** | **F117 arrival re-choose** ⭐ highest value | F117 | 8 min, mostly flight | Colony needs a nursery, retirement home, hotel **or** a dome with a trait filter (free space). Land a **passenger rocket beyond walking distance of every dome**, no elevator route | Arrivals just walk to a re-chosen dome. **Unfixed** = mod-error dialog + `attempt to index a nil value` at `Filter.lua:116` or `Stats.lua:193-196` with `Fix_ArrivalDeaths.lua:201` in the stack. Recipe: `bugs/F117.md` §Control |
| **A3** | **F118 layout leak** ⚠️ unpredictable by design | F118 | 5 min | Needs a layout containing a building you have **NOT researched**. ⛔ **All research is done on `USA Sol 18`, so this row cannot run there.** ⭐ **Try `SMRFIX 1.1 testing`** — the same colony at **Sol 1**, in the same save folder. ⚠️ **Unverified**: its research state was never read, and this colony is cheat-provisioned, so confirm something IS still locked there before relying on it; if not, this row is `NOT RUN — no unresearched building available`. Open the layout, **save with the dialog open**, then load that save | ⛔ **Nobody has ever measured what this leak looks like**, so **"nothing visible" is a legitimate result and worth writing down.** No probe exists. Record what you see either way. ⛔ Do **not** open the Mod Editor to manufacture a locked entry — every save there bumps `version` (`H-02`) |
| **A4** | **Rocket refuel toggle** | F-7 / F50 | 3 min | Landed rocket with a trip set: click **Accept fuel** OFF; wait two game hours; back ON | While OFF: **no Fuel requested or delivered**, and drones already heading there are **not** sent back on the hour. Back ON: Fuel requested again |
| **A5** | **Edit Payload** | F-6 / F70 | 10 min incl. trip | Landed rocket: open Edit Payload, set ONE row to 0, confirm; fly the trip and return; reopen. Then open again and **cancel** the launch prompt. Then **pick a new destination** | After the trip the emptied row is **still 0**. After the cancel, the next open shows what it showed before. After the destination pick the dialog **re-fills from the template** — that is 1.1.0's own behaviour and is exempt on purpose |
| **A6** | **Vacuum walks** | F-9 / F52 | 5 min | Two domes under 400 m apart joined by a passage, non-breathable map; move a colonist between them (home in the other dome) | Walks **through the passage**, not across the surface. Destroy the passage, repeat: the surface walk resumes (the designed fallback) |
| **A7** | **Expedition housing** | F-2 | 5 min | Send an expedition, wait past 5 sols, bring the crew home | The returning crew **keep their own residence** — not a random one, not homeless |
| **A8** | **Train with nowhere to deliver** — row 1's unrun third clause | F-10 / F46 | 2 min | Switch the resource OFF at **both** stations, send a train carrying it | The train **still unloads** rather than hanging. *(The other two clauses PASSED 09-09 — the train runs, and it carries past a station that refuses the resource.)* |
| **A9** | **Track split** ⛔ **DESTRUCTIVE, SAVE-PERSISTENT — DO THIS LAST** | F116 | 5 min | EXTEND a train line while pieces are still under construction, then salvage ONE middle piece (plain click, **not** Ctrl+click) | The line splits; **every remaining piece is still on a track** (nothing vanishes or becomes unselectable); assigned trains survive; both halves accept a train; no `TrackSalvageWipe` error. ⚠️ Silent by construction — there is no throw, so **look, do not wait for a log line**. Restore from the backup afterwards if the colony is wanted intact |
| **A10** | *(optional, ~10 min)* pack-OFF baseline leg | — | 10 min | Boot with the fix pack off | 13 probes report `fix pack not loaded`, which is correct. ⭐ The 32 `retired` probes should give the **same** verdict on both legs — they measure the game, not us. A retired probe that disagrees between legs is itself a finding |

**Not runnable, and not deferrable:**

- ⛔ **T1.3 (the F95 sanitizer pass, non-vacuously) is BLOCKED.** It needs an
  Astrogeologist colony; this one is `rocketscientist` and 1.0.7 saves cannot
  load. It reads `removed 0` and proves nothing. It cannot be run without
  provisioning a new colony from scratch (hours). The kit's
  `AstrogeologistExtractors` probe already answers the question independently
  and PASSed.
- ⛔ **Saint's blessing — SHELVED BY RULING (ck130).** The condition is
  historical and unforgeable; a cheat would test vanilla, not us. **Do not
  attempt.** Its probe PASSes vacuously and that is not coverage.

## 6 · ⛔ Three decisions the owner owes, and they are cheap

These are already written up in `PLAYTEST_CHECKLIST.md` → "Decisions waiting on
you". **Ask them at the keyboard while the rockets fly** — none needs research.

1. **`F03` claims a fix that no longer ships.** Its entry and the public fix list
   read `tested` / `high`, but link 02 (`f707903`) deleted its repair pass on
   09-08 — correctly, under ruling 117, because 1.1.0 ships
   `SavegameFixups.RemoveLeakedUpgradeModifiers` (verified at
   `Building.lua:1313`). The removal is right; the **claim** was never withdrawn.
   ⛔ **No agent moves this status word.** → *Flip `F03` to retired before the
   upload, or does it stay?*
2. **Four stale instruments**, one of which prints a genuine `[LUA ERROR]` header
   every single run and will trip every future scan. → *Repair now, or file for
   hotfix 3?*
3. **Two shipped modules have no working probe** (`LanderEmptyLaunch`,
   `FreedHousingNotice`). Blind spots, not defects. → *Accept for this release?*

## 7 · ⛔ The shelf — how to stop without lying

The owner will stop when they stop. **That is planned for, not a failure.**

1. **Nothing half-observed is recorded as observed.** A row is `PASS`, `FAIL`, or
   **`NOT RUN`**. There is no fourth option, and "looked fine while I was doing
   something else" is `NOT RUN`. ⚠️ **"Done" from the owner is not an
   observation** — ask what they saw, by clause. This came up twice on 09-09.
2. ⛔ **Never move a status word you did not witness.** A source read is never
   `tested`; `tested-attended` needs an attended witness at the screen. A row
   that ran and passed earns `tested-attended` on **that entry only**.
3. ⛔ **SKIPs BY NAME, never a total.** "6 of 9 done" is not a report; the three
   names are the report.
4. **At close-out, update the existing block** in `PLAYTEST_CHECKLIST.md` →
   "Decisions waiting on you" → *what the sitting still owes*. ⛔ Do not create a
   second block; edit the one that is there.
5. **Update `STATE.md`** in the kernel's one-fact-per-line style. ⚠️ Byte-capped
   (warn **12288**; it was **12262** at `1480953`, so there is almost no
   headroom) — if you cross it, evict in the same commit per
   `prompts/STATE_EVICTION.md`. ⛔ **Evict, never compress**, and remember the
   rule that does the work: *if a sentence needs "superseded by", the superseded
   half is history.*
6. ⭐ **A measured reading that contradicts a prediction in this file is the most
   valuable thing the sitting can produce.** Record it loudly, do not reconcile
   it away. Last time three predictions fell — the probe count was 94 and is 95,
   two rows were vacuous by construction, and a `retired` FAIL meant the exact
   opposite of what it said.

## 8 · Stop conditions — permission, not failure

- **A `[LUA ERROR]` naming the pack, not in §4's table** ⇒ stop the leg, copy the
  FULL log after the process exits, record which control was running. That is a
  finding, and it outranks finishing the list.
- **`LEFT n modifier(s) … ALONE`** from the sanitizer ⇒ report it; do not touch
  the save. It means something looked like ours but could not be identified, and
  removing another mod's modifier is the one mistake here with **no undo**.
- **The owner is out of time** ⇒ §7. Stop cleanly, file honestly.
- **A row needs setup the colony cannot provide** ⇒ `NOT RUN`, with the missing
  precondition named. ⛔ Do not cheat a substitute into place and call it the
  control. (A3 is the likely one — all research is done here.)

## 9 · What may NOT be claimed

- ⛔ **Not "hotfix 2 is ready."** `H-04`. A green sitting is evidence, not
  clearance, and the upload is the owner's.
- ⛔ **Not "F117/F118 are fixed"** from a source read. Both repairs were checked
  the same way the defects were found. A2 and A3 are the first observation, and
  **F118 has no probe at all**.
- ⛔ **Not a `tested` grant on any row that did not run.**
- ⛔ **Never re-quote a count from a partially-copied log**, and ⛔ never treat a
  `FlushLogFile()` as having worked without checking the file actually grew.
- ⛔ **Not "the suite is clean"** — it has five standing false FAILs (§4). Say
  *"no new failures beyond the four stale instruments"*.

## 10 · Read path — files, not folders

`agent/STATE.md` (mandatory) · `docs/PLAYTEST_CHECKLIST.md` — "what the sitting
still owes" · `agent/reports/HOTFIX_2_AUDIT.md` §4, §6 ·
`agent/bugs/F117.md` **§Control**, `F118.md`, `F116.md`, `F46.md`, `F03.md` ·
`docs/PLAYTEST_HELP.md` (console facts, verified command table, kit helpers) ·
`agent/facts/EF-079.md` (branch-locked fixtures), `EF-081.md` (why forcing is
never evidence), `EF-056.md` (autosave rotation) ·
`archive/logs/sitting{boot,suite,play}110_*` — the 09-09 evidence ·
`agent/bugs/INDEX.md` / `agent/facts/INDEX.md`. ⛔ Check `facts/INDEX.md` before
deriving any engine claim.

## 11 · Close-out

Green `python tools/doccheck.py` before any doc commit; **WARNs verbatim** in the
summary (18 standing `frozen index-row cell` warns are expected — report, do not
"fix"). Archive every log to `docs/archive/logs/` with a `sitting2*` prefix and
⚠️ **`git add -f`** — `*.log` is gitignored and the tracked archive is all
force-added. Commit by **explicit individual file paths** on `add` AND `commit`
(peers share this worktree and a directory pathspec has swept a stranger's work
into a commit twice), `git commit -F <file>`, then push.

⚠️ **This brief does NOT delete itself while any row is `NOT RUN`.** **`git rm`
it only when every row in §5 is PASS, FAIL, or shelved by an owner ruling** —
and say so in the close-out with the deleting commit named. If rows remain,
rewrite this file for what is left rather than adding a third brief.

⛔ **The upload is NOT part of this sitting** unless the owner says so at the
keyboard. If they do: `UPLOAD_WORKFLOW.md`, Paradox before Steam (`H-03`), §3
paste backups are the real delivery path, and **§4 publish the site immediately
AFTER the upload** — ck129, ruled. ⛔ `100_DOCSWEEP.md` must have run first, and
it is now the **only** thing blocking the upload.
