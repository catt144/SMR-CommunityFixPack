# The hotfix-2 sitting — one boot, two tiers, and an honest shelf

Paste into a fresh Claude Code session **with the owner at the keyboard**. This
is the consolidated in-play sitting the owner ruled on 2026-09-08 (*"Can the
sitting be done after the chain. I want to insure everything is green on this
side and then we can check the live side?"*) — every control from links 03, 04,
04b, 07, 08 and 99a, in one session, on one colony.

**Staleness anchor: `7ccfe93`.** `git log --oneline -15` · `git pull` ·
`ListAgents` before you touch anything.

> ⚖️ **WHY THIS EXISTS, in one sentence.** **Nothing in this patch has ever run
> in a game.** No boot of the 44-module pack exists; every census in the chain
> describes the old 80-module pack; no status word has been moved on anything,
> deliberately. Six days ago F114 and F115 both reported `applied` and both broke
> visibly in players' games, with every instrument green.

> ⛔ **`H-04` BINDS THIS WHOLE FILE.** A clean sitting is not clearance and this
> session never calls the release ready. It produces **readings**; the owner
> decides what they mean.

## 0 · The shape — read this before planning your evening

**Tier 1 (~25 min, no colony setup)** is the boot, the census and the suite. It
catches the catastrophic class: a module silently off, or a removal that was
wrong. ⛔ **The owner should not upload without it.**

**Tier 2 (~60–75 min + research/setup)** is twelve in-play controls. Each one
turns a source-derived claim into an observation. **These can be shelved.**

⇒ **Run Tier 1 first, complete. Then work Tier 2 in the order given** — it is
sorted by value, not by link number. Whatever is left when the owner stops gets
**filed, not faked** (§5).

## 1 · Live todo list — REQUIRED, and the owner reads it to decide when to stop

Build it **before the boot**, one item per control, in the order below. Mark each
the moment it completes; keep exactly one in progress. Put the **reading** in the
item text as you go (`T1.2 suite: 88 PASS / 2 FAIL / 4 SKIP — FAIL list …`), so
the list answers "where are we" without anyone re-reading the transcript.

⚠️ **If a control turns out to be two things, split it in the list at that
moment.** A checkbox coarser than the work is a wrong answer to "how much is
left".

## 2 · Preconditions — ✅ ALL FOUR VERIFIED 2026-09-09 at `7ccfe93`, re-verify anyway

| gate | reading when this was written | how to re-check |
|---|---|---|
| **Stale-probe gate** (mandatory, `WORKFLOW` element 7) | ✅ **CLEAN — zero hits** | `grep -rln "TEMPORARY" Code/ ../SMR-BugFixPack-TestKit/Code/` — CLEAN is zero lines. ⛔ **Refuse to record any result without it.** Put it in the todo list. |
| **Force-inactive leg** (`97_ForceInactive.lua`) | ✅ **DISARMED** (commented out of the kit's `metadata.lua` code list) | ⛔ It must stay disarmed. A forced module is a body pinned to an older build installed over changed code — throws are EXPECTED and it **changes what the pack does**. It would make the census and every A/B meaningless (`EF-081`). |
| **Enable-path leg** (`98_EnablePathLeg.lua`) | ✅ **DISARMED** | same list |
| **Autorun harness** (`95_AutoRun.lua`) | ✅ armed but **INERT** — `96_AutoRunFlag.lua` is not in the code list and no `-smrautorun` switch | An attended launch behaves normally. Leave it. |

**Also before the boot:**
- ⛔ **`Mars.exe` not running** when anyone edits loadable code. `tasklist`, its
  own step.
- ⚠️ **Passage Network is ENABLED on the rig — untick it** before any clean leg.
- ⛔ **`H-06`: pre-copy every autosave** before loading anything. Loading a COPY
  of a campaign still runs that campaign's autosave rotation and **deletes the
  owner's autosaves** (`EF-056`).
- ⛔ **`H-09`: no packed folder beside the live junction** — at equal version the
  unpacked one wins silently and the leg measures nothing.
- ✅ **Cheats are NOT a confound** for any control here — this was checked per
  row by links 03/04/04b. The colony is oversized and cheat-provisioned by
  design; that is normal, not a defect.

**The colony:** `BlankBig_02` (the owner's fresh 1.1.0 NASA colony, `F114.md:201`).
⛔ **1.0.7 saves cannot load on 1.1.0** (`EF-079`) — the whole fixture library is
branch-locked, so every in-play row shares this one colony.

⛔ **DO NOT load a save that ran under the BROKEN pack** unless a row below says
to. The `SaintBlessing: restored …` line prints on a poisoned save's **FIRST**
load and never again — any boot spends that evidence. (Per ck130 no row needs it;
this is here so nobody spends it by accident.)

## 3 · TIER 1 — the boot, the census, the suite

⚠️ **A log copied while the game is RUNNING is a PARTIAL log.** This produced two
wrong counts on 09-08 (a "1" that was 6; a "30" that was 157). **Re-copy after
`Mars.exe` exits before quoting any count or rate.**

### T1.1 · Boot with the pack ON, and read the census

Use `tools/logscan.py` — ⛔ **never a hand-rolled grep**. The engine writes the
`[LUA ERROR]` header two ways and only one carries a file path; a hand grep
undercounted 30 against 157.

- **PREDICTION: 44 applied / 0 inactive.** ⛔ Computed, never measured — this is
  the first boot of this pack.
- ⚠️ A **first-pass read may say 43/1** and that is normal: `SaintBlessing`
  latches and then heals. `logscan` is heal-aware; a raw read is not.
- ⭐ **ANY `inactive` line is a finding.** **Eight modules changed their
  self-check since the last boot.** A module that declines silently ships as a
  no-op and nobody hears about it.
- **0 `[LUA ERROR]` expected.** ⛔ **Never silently discount a log line** — "not
  caused by our leg" is an attribution verdict, not a dismissal. Report every
  unexplained line with its timestamp.

### T1.2 · `SMRTest.RunAll()`, pack ON

**Expect 94 probes: 55 `behavior`, 32 `retired`, 7 `install`.**

⭐ **The 32 `retired` probes are the point of this run** — the first machine
check the project has ever had on *"vanilla fixed it"*. Those 36 removals were
decided by reading source. They read **backwards**:

| verdict | meaning |
|---|---|
| **PASS** | vanilla really did fix it ⇒ the removal is confirmed in a running game |
| **FAIL** | ⛔ **the bug is still there — a removal was WRONG and players lost a fix.** A finding, not a probe bug |
| **ERROR** | the probe's scaffolding predates 1.1.0 ⇒ evidence of nothing, either way |

**Four named results that are NOT regressions** — do not file them:
`LanderCargoRatchet` and `AutoExportPriority` → expected **ERROR** (1.1.0 rewrote
the rocket cargo allocator; a blind patch that happened to PASS would be a false
"vanilla fixed it"). `MoraleComfortTooltip` → **SKIP**. `LocalizedUIText` →
**SKIP** on an English rig. The six `SaveRescue*` SKIP unless that mod is loaded;
the two `OptionsMenu*` and six opt-in probes SKIP unless the opt-in pack is
ticked — all by design.

⛔ **Any FAIL not named above is either a real regression or a probe someone got
wrong, and either way it wants looking at.**

### T1.3 · The `SaveSanitizer: F95` line (ck126 — the owner ruled the pass IN)

Load the colony and read the log:

| the line says | it means |
|---|---|
| `removed 0 modifier(s), left 0 unidentified` | already clean — most saves, and **every save that was not an Astrogeologist colony** |
| `removed 2 …` plus a per-label line | this save carried our leftovers and they are gone |
| `LEFT n modifier(s) … ALONE` | ⚠️ **REPORT THIS ONE.** Something looked like ours but could not be positively identified, so it was left. It most likely belongs to another mod, and removing someone else's is the one mistake here with **no undo** |

⚠️ **If the colony's commander profile is not Astrogeologist this reads `removed
0` and proves nothing.** That is a vacuous pass, not coverage — record it as
such. Cross-check: the kit's `AstrogeologistExtractors` probe answers the same
question independently.

### T1.4 · `PayloadTemplateRefill: applied` must appear in the log

That module's probe has **never executed in any boot** and it indexes
`FlightPolicies`, a global created on `ClassesBuilt`. Safe on both real boot
paths today, but that is a boot-order dependency, not a contract. 99a added a
named `Require` guard so a failure is now **named** rather than silent — if the
module stood down, the log says why. Its absence from the log is a finding.

### T1.5 · `SaintBlessing` — expect a PASS that proves nothing

Per **ck130** the owner ruled this heal ships unexercised. The probe will return
`PASS — … (no Saint in a dome in this save, so the re-base half had nothing to
read)`. ⛔ **Record it as vacuous. Do NOT read it as confirmation**, and do not
go hunting a poisoned save to make it fire.

### T1.6 · (optional, ~10 min) The pack-OFF baseline leg

Worth it if the retired probes produced anything surprising. 13 probes report
`fix pack not loaded`, which is correct. ⭐ **The 32 `retired` probes should give
the SAME verdict on both legs** — they measure the game, not us. **A retired
probe that disagrees between the two legs is itself a finding.**

## 4 · TIER 2 — the in-play controls, ordered by value

⚠️ **Rows 1–2 are the two bugs that actually reached players.** If the owner has
time for three things, do **1, 2 and 3**.

| # | control | fix | ~time | what to do | PASS looks like |
|---|---|---|---|---|---|
| **1** | **Train unloading** ⭐ doubles as the **F114** control | F-10 / F46 | 5 min | Line with two stations: switch a resource OFF at station A while B accepts it; send a train carrying it into A | The train **keeps** that resource at A and unloads at B; a train with nowhere to deliver still unloads; no `Fix_TrainCargoDumping` error. ⭐ **And the train leaves its platform at all** — that is F114 |
| **2** | **Landscaping over boarding** ⭐ the **F115** control | F-8 / F34d | 3 min + research | ⚠️ **Research "Dozer Rover" first** (or the Landscaping Nanites breakthrough) — 1.1.0 locks terrace/ramp/clear-waste-rock behind it, new since 1.0.7 (`EF-083`). Park an RC Commander, order drones to board it, drop a **flatten** over them | Drones finish boarding; **no** `ExitImpassable`, **no error line**; the site gets its stockpile and progresses |
| **3** | **F-10 premise** (console, cheapest real answer here) | F46 | 1 min | Select station A from row 1 (resource still OFF), console: `local st = SelectedObj print(st:IsResourceEnabled("WasteRock"), st.demand.WasteRock:GetTargetAmount())` (substitute your resource) | Expect `false <number>`. **Positive** ⇒ the 1.1.0 bug is real and our guard works. **0** ⇒ 1.1.0 fixed it itself, our guard is inert, and **F46 becomes a REMOVE candidate** |
| **4** | **Track split** ⚠️ destructive + save-persistent, never run | F116 | 5 min | EXTEND a train line while pieces are still under construction, then salvage ONE middle piece (plain click, **not** Ctrl+click) | The line splits; **every remaining piece is still on a track** (nothing vanishes or becomes unselectable); assigned trains survive; both halves accept a train; no `TrackSalvageWipe` error |
| **5** | **F117 arrival re-choose** — repaired today, never observed | F117 | ~8 min | Colony needs a nursery, retirement home, hotel **or** a dome with a trait filter. Land a **passenger rocket beyond walking distance of every dome**, no elevator route | Arrivals just walk to a re-chosen dome. **Before the fix this raised the mod-error dialog naming the pack.** Full recipe in `bugs/F117.md` |
| **6** | **Vacuum walks** | F-9 / F52 | 5 min | Two domes under 400 m apart joined by a passage, non-breathable map; move a colonist between them (home in the other dome) | Walks **through the passage**, not across the surface. Destroy the passage, repeat: the surface walk resumes (the designed fallback) |
| **7** | **Edit Payload** | F-6 / F70 | 10 min incl. trip | Landed rocket: open Edit Payload, set ONE row to 0, confirm; fly the trip and return; reopen. Then open again and **cancel** the launch prompt. Then **pick a new destination** | After the trip the emptied row is **still 0**. After the cancel, the next open shows what it showed before. After the destination pick the dialog **re-fills from the template** — that is 1.1.0's own behaviour and is exempt on purpose |
| **8** | **Rocket refuel toggle** | F-7 / F50 | 3 min | Landed rocket with a trip set: click **Accept fuel** OFF; wait two game hours; back ON | While OFF: **no Fuel requested or delivered**, and drones already heading there are **not** sent back on the hour. Back ON: Fuel requested again |
| **9** | **Expedition housing** | F-2 | 5 min | Send an expedition, wait past 5 sols, bring the crew home | The returning crew **keep their own residence** — not a random one, not homeless |
| **10** | **Asteroid habitat trait filter** | F-3 | 2 min | Open an asteroid habitat and **set a trait filter** | **No error** in the log. Before this build that threw |
| **11** | **F118 layout leak** ⚠️ unpredictable by design | F118 | 5 min | Open a layout containing a building you have **not researched**; save with the dialog open; load | ⛔ **Nobody has ever measured what this leak looks like**, so **"nothing visible" is a legitimate result and worth writing down.** Record what you see either way |
| **12** | **Saint's blessing** | F-1 / F92 | — | ⛔ **SHELVED BY RULING (ck130).** The condition is historical and unforgeable; a cheat would test vanilla, not us. **Do not attempt.** See T1.5 | — |

## 5 · ⛔ The shelf — how to stop without lying

The owner will stop when they stop. **That is planned for, not a failure.**

1. **Nothing half-observed is recorded as observed.** A row is `PASS`, `FAIL`, or
   **`NOT RUN`**. There is no fourth option, and "looked fine while I was doing
   something else" is `NOT RUN`.
2. ⛔ **Never move a status word you did not witness.** A source read is never
   `tested`; `tested-attended` needs an attended witness at the screen. A row
   that ran and passed earns `tested-attended` on **that entry only**.
3. ⛔ **SKIPs BY NAME, never a total.** "9 of 12 done" is not a report; the three
   names are the report.
4. **At close-out, write the unrun rows into `PLAYTEST_CHECKLIST.md`** as ONE
   block under "Decisions waiting on you" titled *what the sitting still owes* —
   each row with its fix id, its recipe, and why it did not run (no time / no
   setup / blocked / shelved by ruling). ⛔ That block is the successor; do not
   invent a new prompt for it.
5. **Update `STATE.md`** with what was measured, in the kernel's one-fact-per-line
   style. ⚠️ Byte-capped (warn **12288**; it was 10746 at `ab7e0f5`) — if you
   cross it, evict in the same commit per `prompts/STATE_EVICTION.md`. ⛔ Evict,
   never compress.
6. ⭐ **A measured reading that contradicts a prediction in this file is the most
   valuable thing the sitting can produce.** Record it loudly, do not reconcile
   it away. The predictions exist to be falsified.

## 6 · Stop conditions — permission, not failure

- **A `[LUA ERROR]` naming the pack** ⇒ stop the leg, copy the FULL log after the
  process exits, record which control was running. That is a finding, and it
  outranks finishing the list.
- **A `retired` probe FAILs** ⇒ a removal may have been wrong and players may
  have lost a fix. Record it and keep going; do not attempt a repair in the
  sitting.
- **`LEFT n modifier(s) … ALONE`** ⇒ report it; do not touch the save.
- **The owner is out of time** ⇒ §5. Stop cleanly, file honestly.
- **A row needs setup the colony cannot provide** ⇒ `NOT RUN`, with the missing
  precondition named. ⛔ Do not cheat a substitute into place and call it the
  control.

## 7 · What may NOT be claimed

- ⛔ **Not "hotfix 2 is ready."** `H-04`. A green sitting is evidence, not
  clearance, and the upload is the owner's.
- ⛔ **Not "the pack works on 1.1.0"** from a clean Tier 1. Tier 1 says the pack
  **loads and installs**; the controls say whether the repairs are right.
- ⛔ **Not "F117/F118 are fixed."** Both were found by source read and both
  repairs were checked the same way. Row 5 and row 11 are the first observation.
- ⛔ **Not "vanilla fixed it" from an ERROR** on a retired probe — that is
  evidence of nothing in either direction.
- ⛔ **Not a `tested` grant on any row that did not run.**
- ⛔ **Never re-quote a count from a partially-copied log.**

## 8 · Read path — files, not folders

`agent/STATE.md` (mandatory) · `docs/PLAYTEST_CHECKLIST.md` — the link 03/04/04b
control blocks and items **126–131** · `agent/reports/HOTFIX_2_AUDIT.md` **§4
(what would make this half-baked) and §6 (what the sitting owes)** ·
`agent/bugs/F117.md`, `F118.md`, `F95.md`, `F116.md`, `F46.md` ·
`docs/PLAYTEST_HELP.md` (console facts, the verified command table, kit helpers) ·
`agent/facts/EF-079.md` (why the fixtures are branch-locked), `EF-081.md` (why
forcing is never evidence), `EF-083.md` (the Dozer Rover gate) ·
`agent/bugs/INDEX.md` / `agent/facts/INDEX.md` to find more. ⛔ Check
`facts/INDEX.md` before deriving any engine claim.

## 9 · Close-out

Green `python tools/doccheck.py` before any doc commit; **WARNs verbatim** in the
summary (18 standing `frozen index-row cell` warns are expected — report, do not
"fix"). Commit by **explicit individual file paths** on `add` AND `commit`
(peers share this worktree and a directory pathspec has swept a stranger's work
into a commit twice), `git commit -F <file>`, then push.

⚠️ **This brief does NOT delete itself while any row is `NOT RUN`** — the
remainder is a real second sitting and this is its recipe. **`git rm` it only
when every row in §3 and §4 is PASS, FAIL, or shelved by an owner ruling**, and
say so in the close-out with the deleting commit named.

⛔ **The upload is NOT part of this sitting** unless the owner says so at the
keyboard. If they do: `UPLOAD_WORKFLOW.md`, Paradox before Steam (`H-03`), §3
paste backups are the real delivery path, and **§4 publish the site immediately
AFTER the upload** — ck129, ruled. ⛔ `100_DOCSWEEP.md` must have run first.
