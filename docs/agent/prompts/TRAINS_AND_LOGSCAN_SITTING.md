# TRAINS + LOG SCAN — the first 1.1.0 sitting (handoff, written 2026-09-08)

Paste into a fresh Claude Code session. **This is a LIVE PLAYTEST at the
keyboard** — the owner is present. Staleness anchor: **written 2026-09-08**, the
day 1.1.0 shipped. **Start with `git log --oneline -10` + `git pull`.**

> 🎯 **TWO JOBS, NEITHER DONE BEFORE ON 1.1.0.**
> **(1) TRAINS** — reproduce and narrow `F114`, a player-reported breakage.
> **(2) A FULL LOG SCAN** — the first systematic one on the new build.
> ⛔ Nothing else. No fixes shipped, no uploads, no retirements.

> ⚖️ **THE EVIDENCE RULE (owner, 2026-09-08).** A dev "Fixed" line is a **CLAIM,
> false until we confirm it.** ⭐ **And this session already proved the rule cuts
> both ways: a desk audit predicted 6 modules would self-disable on 1.1.0; the
> game measured 11.** Trust the log over any document here, including this one.

## 0 · What you already know — do NOT re-derive this

Read `docs/agent/STATE.md` (mandatory). Everything below is **measured**, from
`docs/archive/logs/first110_Mars.exe-20260908-15.20.28-6a91a190.log`.

- **Game is 1.1.0.403908**, `LuaRevision` **403908**, build hash `6a91a190`.
  Both DLCs load (`norman` = Feeding the Future, `thomas` = Interplanetary
  Codex). The pack loads **unflagged** (`EF-077`, `EF-078`).
- ⭐ **13 of 80 modules are inactive; 67 active.** The in-game dialog names
  **11** of them ("switched themselves off for safety") — the 13 minus
  `SaintBlessing` and `LastTransmissionStorage`, which latch benignly.
  Full list with the engine's own reasons: **`EF-078`**. ⛔ Do not re-count from
  source; read `SMRFixPack.ListFixes()` or the boot lines.
- ⭐ **ALL 11 TRAIN/TRACK MODULES REPORT `applied`.** None self-disabled. So
  `F114`'s candidate set is fully live.
- ⛔ **1.0.7 SAVES CANNOT BE LOADED ON 1.1.0** (`EF-079`). The whole fixture
  library — `USA Sol 302`, the F95/F59/F90 saves, the T1/T2 uninstall pair — is
  **branch-locked to 1.0.7**. This is the single biggest constraint on this
  sitting; §2 is built around it.
- ⚠️ **THE OPT-IN PACK IS ENABLED AND APPLYING** (9 `[CommunityOptInPack]`
  lines, incl. `DroneOverhaul`). `STATE`/ck43 said OFF — **that record was
  stale**. A second pack touching drones is a **confound for a train leg**;
  §2 says what to do about it.
- ⛔ **There is no `fix pack present: N/N` line at boot** — that is the TestKit's
  and only appears when the suite runs. The per-module `applied`/`inactive`
  lines are the boot read.
- Known open defects of ours, none yet reproduced live: `F111`, `F112`, `F113`
  (see `reports/GAME_1_1_0_AUDIT.md` §3). ⛔ **Not this sitting's job** — but if
  the log scan surfaces one firing, that is a finding worth everything.

## 1 · Bindings

- ⛔ **Never modify the game directory.** `ModTools\Src` is read-only truth and
  is now 1.1.0 source; ⛔ never "correct" a 1.0.7 citation in an old entry.
- ⚠️ **STALE-PROBE GATE binds — you are launching the game.**
  `grep -rln "TEMPORARY" Code/ ../SMR-BugFixPack-TestKit/Code/` must be **zero**
  (or every hit declared by this session's design). Put it in your todo list.
- `tasklist | grep -i Mars` — **`Mars.exe` must not be running** before you edit
  loadable code, in a step of its own.
- ⛔ `H-08`: **never pull a mod's junction** — it costs the enable and only the
  owner can restore it (tick + restart). Bisect by other means.
- ⛔ `H-09`: never stage a packed folder beside a live junction.
- ⛔ `H-06`/`EF-056`: loading a COPY of a campaign runs its autosave rotation and
  **deletes the owner's autosaves**. Pre-copy first. ⚠️ Now sharper: the 1.0.7
  fixtures are irreplaceable (`EF-079`).
- ⛔ `H-02`: no Mod Editor, no `version` edit, **no upload**.
- **Cheats are normal on this rig** — the colonies are oversized and
  underindustrialised and cheats are life support. Expect the markers; a cheat is
  a confound only where a reading intersects what it changed.
- `python tools/doccheck.py` GREEN before any doc commit; `STATE.md` is
  byte-capped — adding a line means evicting one in the same commit.
- Commits: `git commit -F <file>`, then **push**.

## 2 · JOB 1 — trains (`F114`)

**The report, verbatim** (Steam, 2026-09-08, *Ranger Dimitri*):

> "Think something broke in the update when it came to the Train's with this mod.
> Using this mod cause them to not move between stations. When I turn it off they
> work as normal."

### 2a · The provisioning problem, and the decision it forces

⛔ **You cannot load an old colony to test this.** `EF-079`. And trains are not
an early-game feature — a fresh 1.1.0 colony needs real provisioning before a
train even exists. The project's rule stands: **hours of solo provisioning for a
NEW heavy setup**, not a 20-30 min warm-up. ⛔ Never describe this leg as short.

⭐ **A deduction that helps, flagged as a deduction:** because 1.0.7 saves cannot
load at all, the reporter must be on a colony **created on 1.1.0**. So the repro
target is a fresh 1.1.0 game and save-conversion is excluded as a confound. (The
one alternative not excluded: a save they made earlier on 1.1.0.)

**Ask the owner, before burning hours** — this is the sitting's first decision:
- **(a)** Cheat-provision a minimal 1.1.0 colony to a train — fastest, and the
  train subsystem is what matters, not colony realism.
- **(b)** Switch the install to the 1.0.7 branch and confirm the fixture library
  still loads — does not test 1.1.0, but re-establishes the A/B base and
  route-checks decision 98.
- **(c)** Ask the reporter for their save first and provision nothing.

### 2b · The confound to remove first

⚠️ The **opt-in pack is currently enabled** and applies `DroneOverhaul` among
others. Both-mods-loaded is the rig's normal config (08-12 ruling) — but for a
first train A/B, **untick the opt-in pack** so a positive result names one mod.
⚠️ Also untick **Passage Network** before any clean leg. ⛔ Untick via the Mods
Manager (owner action), **never** by pulling a junction (`H-08`).

### 2c · The run

1. **Reproduce.** Build/reach two stations plus track, trains assigned, and watch
   whether they move. Pack ON, then pack OFF. ⛔ Record the exact steps — a
   **failure to reproduce is a result** and must be written up as one.
2. **If it reproduces, bisect the 11 train/track modules** agent-side:
   `TrainMinors` · `TrackConnectorPingPong` · `TrackTunnelPowerBridge` ·
   `TrackSalvageWipe` · `TrackSalvageRefund` · `TrainCargoDumping` ·
   `TrainWaitTime` · `TrainsToVoid` · `BrokenTrackSalvage` ·
   `TrainPlatformWedge` · `DestroyedTunnels`.
3. ⛔ **DO NOT RE-DERIVE WHAT IS ALREADY CLEARED** (2026-09-08, source-read):
   - `Fix_TrainMinors`' `recompute_max_vehicles` — **cleared**, byte-identical to
     1.1.0's own formula (`Lua/Buildings/Track.lua:65`).
   - `Fix_TrackConnectorPingPong`'s `CreateConnectorElements` — **cleared as a
     copy**, matches 1.1.0's `TrackConnectedObjBase:CreateConnectorElements`
     (`Lua/TrainTransport.lua`) line for line bar its own F66 guard.
   ⚠️ **The one thread left OPEN, and it is a place to instrument, not an
   answer:** our F66 guard declines a hex owned by a live other station, and in
   that branch `el` stays valid so the creation block is skipped ⇒ **that station
   gets no connector element at that spot**, where vanilla always destroys and
   recreates. 1.1.0 changed station↔dome connection, and `TrackBase:GameInit`
   ends with `self:Notify("TryConnectStations")` (`Track.lua:62-67`). Whether
   that branch is reached more often is **unmeasured**.
4. **Write the result into `bugs/F114.md`** — including "did not reproduce".
   ⛔ Claim no cause you have not pinned with a control.

## 3 · JOB 2 — the full log scan

The first systematic scan on 1.1.0. Logs live in
`%AppData%\Surviving Mars Relaunched\logs`, named `Mars.exe-<date>-<time>-<hash>.log`
(1.1.0 hash = `6a91a190`; 1.0.7 = `6a22b86d`, which makes the build trivially
greppable).

**Scan every 1.1.0 log, not just this sitting's**, and report:
1. `[CommunityFixPack]` lines — every `applied` / `inactive`, reconciled against
   `EF-078`'s measured 13. ⛔ **A difference is a finding**, not a nuisance.
2. `[CommunityOptInPack]` lines — the opt-in pack's own state.
3. `[LUA ERROR]`, `assert`, `attempt to`, traceback — ⭐ **the whole point.**
   `EF-065`(a) puts a blame line on any throw under a wrapped target. `F111` and
   `F113` are *predicted* throws that have never been seen; this is how they get
   seen. Their triggers: a staffed automated metals extractor with overtime
   (`F111`); an automode rocket landed at Earth (`F113`).
4. ⛔ **Never silently discount a log line.** "Not caused by our leg" is an
   attribution verdict, not a dismissal — report unexplained lines **verbatim**
   with their age. The project's pushbacks on this have all found real defects.
5. Archive anything load-bearing to `docs/archive/logs/`. ⚠️ `.gitignore` line 2
   is `*.log` — the archive copy needs **`git add -f`**.

⭐ **Consider writing `tools/logscan.py`** if you scan more than a couple by hand:
this will be run again on every game update, and a tool beats a habit. Route it
by `docs/README.md` "Where new things go".

## 4 · If the owner asks about force-loading old saves

They already have. The answer is `EF-080`, in one line: **it is two config
values, the devs ship an unblocked mode, and we still must not rely on it.**
`config.OldSavegameBehavior = "warn"` turns the refusal into a "Load anyway"
prompt; `config.SupportedSavegameLuaRevision <= 396349` removes the gate. Both
are runtime, no game file touched. ⛔ But a force-loaded save is an
**unattributable substrate** — the floor sits deliberately after the research and
services rewrites — so: triage only, **never a verdict**, **never in the shipped
pack** (TestKit is local-only by design), **never save over a fixture**.

## 5 · Close out

- `bugs/F114.md` — the result, whatever it is.
- New facts to `agent/facts/` (`EF-081`+), regenerating the INDEX via
  `split_facts.load_from_dir()` + `render_index()`; `lines:` must equal body
  length. ⛔ The INDEX is GENERATED — never hand-edit it.
- ⚠️ **Correct `STATE`/ck43's stale "opt-in pack OFF"** to whatever is true after
  this sitting.
- Owner decisions → `PLAYTEST_CHECKLIST.md` → "Decisions waiting on you", never
  only an agent doc. A `doccheck` WARN is copied **verbatim** into your summary.
- A leg in `archive/SESSION_LOG.md` (append-only, newest first).
- Status words: `tested-attended` needs an attended witness — the owner is here,
  so a screen claim CAN be made, but only for what was actually watched.
- `doccheck` GREEN → commit → **push**.

## 6 · What "done" is

Trains either reproduced-and-narrowed or written up as not-reproduced, with the
provisioning route the owner chose recorded; every 1.1.0 log scanned with errors
reported verbatim; `EF-078`'s measured 13 either confirmed or corrected against a
live `ListFixes()`. ⛔ No fix shipped, no upload, no retirement, no status moved
on anything that was not actually witnessed.
