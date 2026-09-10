# The hotfix-2 sitting, part 3 — two rows, three clauses, and one recipe that has to be rebuilt

Paste into a fresh Claude Code session. **Parts 1 and 2 are complete and are NOT
repeated.** Six of the nine part-2 rows passed; two were refused because their
recipes cannot work, and rebuilding one of them is now the largest item here.

**Staleness anchor: the commit that rewrote this file.** `git log --oneline -15`
· `git pull` · `ListAgents` before you touch anything — several sessions share
this worktree.

> ⚖️ **WHAT IS ALREADY KNOWN, so you do not re-measure it.** The pack has run in
> a game three times. `44 applied / 0 inactive` on three independent boots,
> `0 error-shaped lines` across a full attended session, the 95-probe suite with
> no regression and no wrong removal, and **six repairs watched working**:
> F114 trains, F115 landscaping, plus A1 habitat filter, A4 refuel toggle,
> A5 Edit Payload (incl. a manual round trip), A6 vacuum walks (both clauses),
> A8 train-with-nowhere-to-deliver, A9 track split. Full record:
> `PLAYTEST_CHECKLIST.md` → the 2026-09-09 (evening) block, and `SESSION_LOG`.

> ⛔ **`H-04` BINDS THIS FILE.** A clean sitting is not clearance. This session
> produces **readings**; the owner decides what they mean.

## 0 · ⛔ Read this before planning anything

**Three of part 2's nine rows had recipes that could not run as written.** All
three were written from source reads without checking whether the colony could
produce the trigger. ⇒ **Before every row below, ask what would make it vacuous,
and check that first.** That single habit was worth more than any row last time.

⛔ **DO NOT RE-RUN A2 (F117) OR A7 (expedition housing) AS WRITTEN.** They are
not deferred — they are refuted. §4 says why, and what is owed instead.

## 1 · Live todo list — REQUIRED

Build it before the first row, one item per row/clause. Mark each the moment it
completes; keep exactly one in progress; put the **reading** in the item text.
⚠️ If a control turns out to be two things, split it at that moment. There may be
no `TodoWrite` tool — then keep the list as a visible block in every message.

## 2 · Preconditions

| gate | how to check | last reading |
|---|---|---|
| **Stale-probe gate** (mandatory) | `grep -rln "TEMPORARY" Code/ ../SMR-BugFixPack-TestKit/Code/` — CLEAN is zero | ✅ CLEAN 09-09 eve. ⛔ Re-run; doccheck's `TEMPORARY SWEEP` is an independent second read |
| `97_ForceInactive` / `98_EnablePathLeg` | commented out of the kit's `metadata.lua` code list | ✅ both DISARMED — keep them so (`EF-081`) |
| `95_AutoRun` harness | `96_AutoRunFlag` absent from the code list | ✅ armed but INERT; an attended launch behaves normally |
| `Mars.exe` not running | `tasklist` | ⛔ before anyone edits loadable code |
| **H-09** no packed folder beside the junctions | `ls "$APPDATA/Surviving Mars Relaunched/Mods"` | ✅ three junctions only |
| **Opt-in pack OFF** | ⛔ the discriminator is **`Loaded mod items for:`**, NOT `Loaded mod def` | ✅ OFF 09-09 eve — `items` line listed only the pack and the kit |

**`H-06` — autosaves.** Backup dir `C:\Dev\SMR-SaveBackup\20260909-hotfix2-sitting\`.
⛔ **Re-copy anything created since**, and note that loading a campaign runs its
autosave rotation and deletes the owner's autosaves (`EF-056`) — that was
observed happening on 09-09, not merely cited.

⭐ **Identify a save from its header, do not ask.** A `.savegame.sav` carries
plain-text metadata in its first ~2 KB. ⚠️ Match **`orig_lua_revision`** (reads
`403908`) — bare `lua_revision` reads **350453**, a *mod's* revision. Confirmed
live on all four saves.

⛔ **1.0.7 saves cannot load on 1.1.0** (`EF-079`).

## 3 · ⛔ Log discipline — short version, and it fired again

1. ⛔ **Only an exited-process log is authoritative.** On 09-09 evening a log read
   mid-session reported *"no error-shaped lines"* — then **grew 1,282 bytes**
   (12,103 → 13,385) before exit. Presence in a partial log is usable evidence;
   **absence never is.**
2. `Debug::Done` in the file is the proof it is complete. Quit to desktop.
3. ⛔ `FlushLogFile()` is not to be trusted — on 09-09 it left the file
   byte-identical. Check the file actually grew.
4. Use `tools/logscan.py` — ⛔ never a hand-rolled grep.
5. Known instrument noise (5 FAIL + 5 ERROR + 7 install SKIPs) is triaged and
   listed in `PLAYTEST_CHECKLIST.md`. ⛔ Do not re-file it. Baselines:
   `44 applied / 0 inactive / 0 errors`; `58 PASS / 5 FAIL / 27 SKIP / 5 ERROR` = 95.

## 4 · ⛔ The two refuted rows — what is owed instead

**These are desk work, not sitting rows. Neither needs the owner.**

### 4a · F117's control recipe is wrong and must be re-derived

Both `bugs/F117.md` §Control and part 2's brief said: *land a passenger rocket
beyond walking distance of **every** dome*. Refuted from the shipped source:

* `GetDomesReachableByColonists` (`_GameUtils.lua:390-420`) adds a dome to the
  candidate list **only** if it IS in walking distance (and welcoming), or sits
  behind a reachable elevator.
* `ChooseDome` (`:486-500`) is `for _, dome in ipairs(domes) do dome:GetScoreFor(colonist)`.

⇒ land beyond walking distance of everything and the list is **empty**,
`Community:GetScoreFor` is never called, and the throw site
(`Community.lua:442` / `:449`) is unreachable. The row would have shown a clean
arrival **whether or not the bug were present**.

The branch actually needs: **the assigned dome out of walking distance while
another welcoming dome is in it.** Vanilla assigns `emigration_dome` at landing
from that same list (`RocketBase.lua:2064`, `:2103`), falling back to
`safety_dome` — the nearest foot-reachable dome — which makes the mismatch hard
to force by landing position alone. The live route looks to be the
**elevator / cross-map** case the module itself singles out
(`cross-map arrivals are never "in walking dist"`).

**OWED:** (1) derive a recipe that provably reaches `GetScoreFor`, or record that
none is forceable and say so in the entry; (2) fix `bugs/F117.md` §Control;
(3) ⚠️ **re-examine the entry's frequency claim** — it says the trigger is
"ordinary mid-game", and this analysis suggests **rarer**. ⛔ That is a claim
about player impact and it is currently unsupported in the entry.

### 4b · A7 (F-2 / F58 expedition housing) is vacuous on this colony

The sweep is `OnMsg.NewDay`; its age branch compares against
`ForcedByUserLockTimeout = 3,600,000` (~5 sols). The only crewed expedition the
colony offers is **Project Yukon — 6 Officers, 3h**: ~1/40th of the timeout, and
short enough that the daily sweep may never tick. None of the three branches
above the exemption (`IsValid`, `reserved_residence` desync, `IsDying`) fires on
a healthy crew.

**OWED:** either wait for a crewed expedition longer than 3,600,000 to appear, or
record A7 as **not exercisable on this colony** and stop carrying it as a row.
⛔ Do not shorten the wait and call it a pass. ⛔ Do not manufacture one — §8.

## 5 · The rows that remain

| # | control | fix | ~time | what to do | PASS looks like |
|---|---|---|---|---|---|
| **A3** | **F118 layout leak** ⚠️ unpredictable by design | F118 | 5 min | ⛔ **Not runnable on `USA Sol 18` — all research is done there.** Try **`SMRFIX 1.1 testing`** (same colony at **Sol 1**, header-verified). ⚠️ **First confirm something IS still locked there** — it is cheat-provisioned; if nothing is, the row is `NOT RUN — no unresearched building available`. Then open a layout containing an unresearched building, **save with the dialog open**, load that save | ⛔ **Nobody has ever measured this leak**, so **"nothing visible" is a legitimate result and worth writing down.** No probe exists. ⛔ Do **not** open the Mod Editor to manufacture a locked entry — every save there bumps `version` (`H-02`) |
| **A5 c2** | **Edit Payload — cancel the launch prompt** | F-6/F70 | 2 min | ⚠️ **Part 2 got this wrong:** the *flight* was cancelled, which cleared the destination and ran `CmdUnload`. That is a different path. What is wanted is the **cargo dialog's** prompt — `CargoRequestNew:PromptRocketCargoIssue`, which is in the module's `Require` list. Zero a row, confirm, reopen, and **cancel that prompt** | The next open shows **what it showed before** — the stamp is on `Apply`'s CONFIRMED path (`if not res or res == 1`), deliberately **not** the cancel branch, so cancelling must neither refill nor stamp |
| **A9 c4/c5** | **Track split — the train clauses** | F116 | 5 min | Part 2's test line was freshly built with **no train assigned**, so these could not be observed. Needs a line with an **assigned train**, split as in part 2 (extend while pieces are under construction, then salvage a middle piece with a plain click) | **Assigned trains survive** the split, and **both halves accept a train**. ⚠️ Silent by construction — look, do not wait for a log line |
| **A10** | *(optional)* pack-OFF baseline leg | — | 10 min | Boot with the fix pack off | 13 probes report `fix pack not loaded`, which is correct. ⭐ The 32 `retired` probes should give the **same** verdict on both legs — they measure the game, not us. A retired probe that disagrees between legs is itself a finding |

**Still blocked, and not deferrable:**

- ⛔ **T1.3 (the F95 sanitizer pass, non-vacuously) is BLOCKED.** Needs an
  Astrogeologist colony; this one is `rocketscientist` and 1.0.7 saves cannot
  load. It reads `removed 0` and proves nothing. The kit's
  `AstrogeologistExtractors` probe answers the question independently and PASSed.
- ⛔ **Saint's blessing — SHELVED BY RULING (ck130).** Its probe PASSes vacuously
  and that is not coverage. **Do not attempt.**

## 6 · ⛔ Bench work the owner ruled on 2026-09-09, all pre-upload

None of these needs the owner or a running game. ⛔ **Do not do kit work while a
game is running** — the kit on disk would stop matching the kit in the session,
and any suite result would be unattributable.

1. **Repair the four stale instruments** (owner ruled: *now*, not hotfix 3).
   One prints a genuine `[LUA ERROR]` header every run (the kit's
   `CaveInRubble` / `IsNearDome` stub gap) and will trip every future scan.
2. **Build probes for `LanderEmptyLaunch` and `FreedHousingNotice`** (owner ruled:
   *build*, not accept). Two shipped modules currently have no working coverage.
3. **F03's status word** — the owner ruled the stale `tested` claim is to be
   withdrawn. ⚠️ **`retired` is NOT in doccheck's `STATUS_WORDS`**
   (`tools/doccheck.py:115-124`). `F21` is the precedent for a downgrade with the
   reason stated in the heading tag. ⭐ Scope is smaller than part 2 assumed: the
   **site fix list is already clean** (link 02's `7cef4f3`, 82 → 46 entries) and
   `metadata.lua` never mentioned it — only the entry, its heading tag and the
   generated INDEX row still read `tested`. ⛔ **INDEX.md is GENERATED** — edit the
   entry and regenerate; never hand-edit the index.
4. **F117's recipe + frequency claim** — §4a.
5. ⚠️ **`STATE.md` sits at exactly 12,288 B, its warn threshold, with zero
   headroom.** The warn was raised 9 KiB → 12 KiB on 2026-09-09 for exactly this
   reason and the runway was consumed the same day. ⇒ **owner decision: raise the
   warn again, or accept per-session eviction.** ⛔ Not an agent's call.

## 7 · ⛔ The shelf — how to stop without lying

1. **Nothing half-observed is recorded as observed.** `PASS`, `FAIL`, or
   **`NOT RUN`** — there is no fourth option. ⚠️ **"Done" from the owner is not an
   observation** — ask what they saw, **by clause**. This mattered repeatedly on
   09-09; one report of *"it loads"* turned out to mean *"it **un**loads"*, which
   inverted the verdict.
2. ⛔ **Never move a status word you did not witness.** A source read is never
   `tested`; `tested-attended` needs an attended witness at the screen.
3. ⛔ **SKIPs BY NAME, never a total.**
4. **At close-out, update the existing block** in `PLAYTEST_CHECKLIST.md` →
   "Decisions waiting on you". ⛔ Do not create a second block.
5. **Update `STATE.md`** in the kernel's one-fact-per-line style — see §6.5
   before you add anything.
6. ⭐ **A measured reading that contradicts a prediction in this file is the most
   valuable thing the sitting can produce.** Record it loudly, do not reconcile it
   away. Part 2's best output was two refuted recipes, not its six passes.

## 8 · Stop conditions — permission, not failure

- **A `[LUA ERROR]` naming the pack, not in the triaged noise list** ⇒ stop the
  leg, copy the FULL log after the process exits, record which control was
  running. That outranks finishing the list.
- **`LEFT n modifier(s) … ALONE`** from the sanitizer ⇒ report it; do not touch
  the save. Removing another mod's modifier is the one mistake here with no undo.
- **A row needs setup the colony cannot provide** ⇒ `NOT RUN`, precondition
  named. ⛔ Do not cheat a substitute into place and call it the control.

## 9 · What may NOT be claimed

- ⛔ **Not "hotfix 2 is ready."** `H-04`. The upload is the owner's.
- ⛔ **Not "F117 is fixed."** Its repair is source-derived, it has never been
  observed in either direction, and **its control recipe is currently wrong**.
- ⛔ **Not "F118 is fixed"** — no probe exists and it has never been measured.
- ⛔ **Not a `tested` grant on any row that did not run.**
- ⛔ **Never re-quote a count from a partially-copied log.**
- ⛔ **Not "the suite is clean"** — say *"no new failures beyond the triaged
  instrument noise"*.

## 10 · Read path — files, not folders

`agent/STATE.md` (mandatory) · `docs/PLAYTEST_CHECKLIST.md` — the 2026-09-09
(evening) block · `archive/SESSION_LOG.md` newest two entries ·
`agent/bugs/F118.md`, `F117.md` (⚠️ its §Control is WRONG — §4a), `F116.md`,
`F70.md`, `F03.md` · `docs/PLAYTEST_HELP.md` (console facts, salvage-cursor
reading, kit helpers) · `agent/facts/EF-079.md`, `EF-081.md`, `EF-056.md` ·
`archive/logs/sitting{boot,suite,play}110_*` + `sitting2play110_*` ·
`agent/bugs/INDEX.md` / `agent/facts/INDEX.md`. ⛔ Check `facts/INDEX.md` before
deriving any engine claim.

## 11 · Close-out

Green `python tools/doccheck.py` before any doc commit; **WARNs verbatim** in the
summary (18 standing `frozen index-row cell` warns are expected — report, do not
"fix"). Archive every log to `docs/archive/logs/` with a `sitting3*` prefix and
⚠️ **`git add -f`** — `*.log` is gitignored. Commit by **explicit individual file
paths** on `add` AND `commit` (peers share this worktree and a directory pathspec
has swept a stranger's work into a commit twice), `git commit -F <file>`, push.

⚠️ **This brief does NOT delete itself while any row is `NOT RUN`.** `git rm` it
only when §5 is fully resolved and §6's bench items are done — and say so in the
close-out with the deleting commit named. If items remain, rewrite this file for
what is left rather than adding a fourth brief.

⛔ **The upload is NOT part of this sitting** unless the owner says so at the
keyboard. If they do: `UPLOAD_WORKFLOW.md`, Paradox before Steam (`H-03`), §3
paste backups are the real delivery path, and **§4 publish the site immediately
AFTER the upload** — ck129, ruled. ⛔ `100_DOCSWEEP.md` must have run first, and
it is still the only thing blocking the upload.
