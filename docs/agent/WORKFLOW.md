# Development Workflow

Process rules for this repo. Code rules are `FIX_POLICY.md`; the global duties are `CLAUDE.md`'s
`Must_Read_Header`; orientation, filing, prompt writing and session close are the skills in
`.claude/skills/`. Situational procedures live in `support/`; the map is `docs/README.md`.

## Layout

- Dev repo: `C:\Dev\SMR-BugFixPack`, git-versioned, canonical.
- Game install: `A:\SteamLibrary\steamapps\common\Project Spark` ("Project Spark" is the Steam
  folder name). Shipped Lua source, read-only: `<game>\ModTools\Src` (`Lua\`, `CommonLua\`, `Data\`,
  `DLC\`). Nothing under the game folder is ever modified.
- Archived source trees, one per game version: `C:\Dev\SMR-SrcArchive\<version>\Src` with a
  `MANIFEST.sha256`; that folder's README holds the archive rule.
- Mod install point: `%AppData%\Surviving Mars Relaunched\Mods\SMR-BugFixPack`, a junction into the
  dev repo, so the checked-out tree is the running mod.
- TestKit, never shipped and local-only by decision: `C:\Dev\SMR-BugFixPack-TestKit`. Its README is
  the agent home for what the kit is, its probes and the SMR Tool Kit; sitting slots are
  `support/SMRTK_SLOTS.md`.
- Sibling mods: the opt-in pack `C:\Dev\SMR-OptInPack` (its own docs) and the save-rescue tool
  `C:\Dev\SMR-CommunitySaveRescue` (design and status in `bugs/D13.md`; unpublished, held as a
  contingency).

## Install for testing

```powershell
New-Item -ItemType Directory -Force "$env:APPDATA\Surviving Mars Relaunched\Mods" | Out-Null
New-Item -ItemType Junction -Path "$env:APPDATA\Surviving Mars Relaunched\Mods\SMR-BugFixPack" `
  -Target "C:\Dev\SMR-BugFixPack"
```

Enable "Relaunched Fix Pack" in the game's Mod Manager; restart the game after editing Lua. The
console line `SMRFixPack.ListFixes()` prints each fix's status (active / inactive+reason / disabled /
error).

## Per-fix discipline

1. Every fix links to a `bugs/` entry with file:line evidence and obeys `FIX_POLICY.md`.
2. Re-verify the target against the cited Src lines before patching; `apply()`'s self-check guards
   it at runtime and returns a reason string, never an error, if a game update moved it.
3. `python tools/parsecheck.py` before any commit that touches Lua: a syntax error in any listed
   file breaks the whole pack at load.
4. One commit per fix or tight group, with its entry and, when the change has a player surface, its
   `prompts/perma/RELEASE_OUTBOX.md` Pending entry in the same commit.

## Records and rulings

- Every console line, lever or command printed in a human doc carries `[RAN <date>, log <name>]`
  or `[NEVER RUN]`; unmarked, a never-executed snippet reads like a proven one.
- Load-bearing claims in entries, specs and briefs are tagged MEASURED / SOURCE / INFERRED /
  INHERITED / GUESS per row, never as one claim over a table. The route sentence ("therefore the
  only way is…") is tagged separately from the lines it cites.
- A routed item names its owner prompt and its precondition. An item whose precondition is a
  situation goes to the checklist as a rider, not to a prompt that will forward it again.
- A log a status flip will cite is copied into `docs/archive/` in the same commit, with
  `git add -f` (`.gitignore` drops `*.log` silently). The game keeps about 20 log files.
- A ruling is recorded with the condition it was made under; re-read it against today's state before
  treating it as binding, and never record a later ruling as a reversal without checking whether the
  earlier condition still holds.
- Player replies are pull-only (owner, 2026-09-12): never drafted unasked, never on an owed list,
  never raised as a nudge, never a gate on other work. A draft in `docs/FIELD_REPORT_REPLIES.md`
  waits by design; when the owner asks, write one and stop. Triage of the report into `bugs/`
  continues unchanged.

## After a game patch — the source-diff instruments

fpk verification: line numbers in `bugs/` and `facts/` come from `ModTools\Src`, and the game
executes `Packs\Lua.fpk` and `Data.fpk`. Parity was byte-identical for 1.1.0.403908 (`EF-085`);
re-prove it after every update, since a same-named function edited under a full replacement is
invisible to the runtime self-checks.

0. Archive first. Copy `ModTools\Src` to `C:\Dev\SMR-SrcArchive\<version>\Src` with its
   `MANIFEST.sha256` before the update lands, and whenever an unarchived version is on disk. Steam
   updates and branch switches overwrite the tree in place and unasked (`EF-075`).
1. Re-extract `Packs\Lua.fpk` (`tools/flpk_extract.py`) and diff it against the new Src tree.
2. `python tools/bodycheck.py` (pinned body, defect expression, target: classes b, d, e), then
   `python tools/sigcheck.py` (arity, class a). Each tool's header defines its verdicts and what
   each one obliges; write the REMOVE/FIX prompts from the table.
3. `tools/treediff.py` and `tools/presetdiff.py` run on trigger only: the patch notes name a system
   we fix, a `DLC_DEEP_CHECK` chain is running, or a changed body cannot be explained by hand from
   the two trees. They emit about 25k rows; never run them "to stay current".

What the instruments license (the canonical copy; `FIX_POLICY.md` §2b points here). On their output
alone you may state exactly four things: a pinned body's bytes did or did not change; a named arity
did or did not change; a stated regex is or is not present in a named body; a named function or
preset field exists in one tree and not the other. "Vanilla fixed it", "this fix is still needed",
"that change is harmless" and "nothing moved under us" each need a second source: a read of the
replacement body in both trees, or a run in the game.

- `bodycheck.py` cannot see class c, semantics moving under a wrapper whose target body is
  byte-identical (6 of the 10 FIX rows in the 1.1.0 re-verification), anything outside the pinned
  body, or a defect that is an absence. A regex pinned to phrasing yields a false `DEFECT-GONE`, the
  direction that retires a live fix; a `DEFECT-GONE` is a REMOVE candidate, never a verdict.
- `treediff.py` misses anonymous `function(` literals and hunks outside every row span;
  `presetdiff.py` reads generated files only and cannot tell `REINDEX-SWAP` from a real change.
- None of them see the engine, runtime-only behaviour, or the 1.0.7 `DLC/` subtree. Copy-vs-wrapper
  is a practice (`luafn.find_bodies` over both archives plus our `Code/`), never a name proxy.
- A clean run over every module is not evidence that every fix still works.

Artefacts: `reports/vanillahunt/` (tracked) and `reports/VANILLA_DIFF_DISPOSITION.md`. All four tools
carry `--selftest`; doccheck gates only `bodycheck --selftest`.

## ⛔ Probe hygiene — HARD GATE before ANY testing (owner, 2026-08-01)

**No test session — attended or unattended — starts, and NO result is
recorded, until the stale-probe sweep has run and reported clean.** Stale
probes are how false facts got recorded: leftover instrumentation logs, hooks
messages, creates threads, and contaminates both the measurement and the log
it is read from (the 2026-07-31 probes were still armed days after their
questions were answered).

**The sweep (mechanical, one command):**

```
grep -rln "TEMPORARY" Code/ ../SMR-BugFixPack-TestKit/Code/
```

**CLEAN =** zero hits, **or** every hit is a probe that THIS session's test
design explicitly declares it needs — named in the brief and in the todo
list. Anything else: the session repairs first (delete the file + its
metadata/items lines, commit) or stops and reports.

**The rules that make this work:**

1. **Every temporary probe/experiment file MUST carry the literal word
   `TEMPORARY` in its header comment** — that is what the sweep greps for.
   A temp probe without the marker is itself a defect: file it on sight.
2. **A probe is STALE the moment its answer is recorded.** Deletion belongs
   in the SAME commit that records the answer (docs-never-lag, applied to
   instrumentation).
3. **The sweep result is part of the record:** every commit that flips a
   agent/bugs/ status, records a MEASURED fact, or reports a PASS/FAIL carries a
   `PROBE SWEEP:` line — either `clean` or `armed: <files>, declared by
   <test>`. **A result commit without that line is invalid and gets
   re-verified before anything builds on it.**
4. Both repos are in scope (the pack AND the TestKit) — the
   `GetPriorityForRequest` experiment that seeded agent/facts/ lived in the
   PACK's code list.
5. ⛔ **A PROBE FILE IS PRESENT IN `Code/` ONLY WHILE ITS RUN IS ACTUALLY
   HAPPENING** (owner decision, 2026-08-04 — *"I want to do whatever is safest,
   I do not want to get back into the situations where armed probes start
   giving us false problems or issues"*). **Placing the file and running are the
   same act; deleting it and recording the answer are the same commit.** There
   is no state in between, and therefore no armed probe can outlive the sitting
   that needed it.

   **What made this a decision rather than an observation.** `doccheck.py`'s
   `temporary_sweep()` (`tools/doccheck.py:501-517`) implements only the FIRST
   half of the CLEAN definition above — any marker in `Code/` is red, no
   declared-probe exception — and `tools/hooks/pre-commit` blocks on red. So a
   session may legitimately declare a probe but **cannot commit anything while
   it is armed**, which collides with the co-run rule that all prep is committed
   before the owner sits down. Found by co-run #0 (2026-08-04), the first job to
   arm a probe since doccheck landed. **The tool was NOT loosened, deliberately:
   a hatch a hurried session can open without saying so re-creates the
   2026-07-31 incident exactly.** ⛔ **`--no-verify` is not an alternative** —
   the hook documents its meaning as *"the docs are inconsistent, I know"*,
   which is a false statement when the only red is a declared probe.

   **How prep works under this rule, and it costs nothing.** Everything else
   commits normally and early: the staged save copy, the measure-moments list,
   the entry and checklist edits, and **the probe's source itself as a fenced
   code block in the session's own brief or spec**. Docs are not swept (the
   sweep walks `Code/` and TestKit `Code/` only), and a probe parked in a doc is
   **inert by construction** — the mod loads only files listed in
   `metadata.lua` `code`, all of which live under `Code/`, so a file that is not
   there cannot arm anything, log anything, or contaminate a measurement. At the
   sitting: write the file into `Code/`, add its metadata line, parse sweep,
   run. Then delete both in the commit that records the answer, per rule 2.

   **If the sitting slips, nothing is stranded and nothing is armed** — which is
   the whole point.

   ⚖️ **In force. The owner-requested recheck RAN 2026-08-04 (corun-rig prompt
   4) and the rule STANDS as written.** The diagnosis re-verified from primary
   sources (`temporary_sweep()` really has no conditional path,
   `tools/doccheck.py:501-517`; the hook really blocks on red; the CLEAN clause
   reads as quoted). The one claim the diagnosis had left unverified is now
   SOURCE-verified: **`ModDef:LoadCode` executes only the files listed in
   `metadata.lua` `code`** — both of its loops iterate `ipairs(self.code)`,
   no directory is scanned (`Mod.lua:490-521`) — so a parked probe is inert by
   construction in the strong form, not merely the outside-`Code/` form. The
   feared cost does not exist: the parse sweep is location-independent
   (measured GREEN on a parked path during co-run #1 prep), and the declined
   one-time override measured what any hatch would buy — **0.4 s of machine
   time and zero owner time** — against a red doccheck in the history and a
   live disarm deadline. No hatch is recommended; none was built.
   Two things the rule does NOT say, so nobody reads them into it: it does not
   ban long-lived instrumentation (that belongs in `90_Loggers.lua` behind an
   explicit toggle, permanent and non-`TEMPORARY` by design — the file exists
   and is the established home), and it does not excuse skipping the parse
   sweep — which runs at the sitting, on the real file, before the launch,
   exactly as before.

## Testing checklist per fix

**Leg-design rules (adopted 2026-08-04, from the first campaign sittings —
relocated here from the standing prompt, which is instructions, not a
logbook):**
- **An "objective counter" is only objective if it can FAIL, and it needs a
  liveness witness beside it.** PT-62's loop check counted a delivery the
  flagged dome was *required* to receive, so it could not fail; F11's `nil`
  reading only meant something because `#units` and `holder` were read in the
  same breath, ruling out an empty list and a call that never fired.
- ⛔ **A probe must reach the code the way PRODUCTION reaches it, and must not
  compute its expectation with the fix's own logic** (adopted 2026-08-24,
  f106-dispatch Pass E — two independent false-greens of the same family).
  A probe that indexes the table the fix patched cannot fail on a broken
  dispatch: the F33 probe called `GetClosestDests` straight off the patched
  base-class table and printed PASS from 2026-07 through the day F106 named
  the module a suspected no-op (TestKit `e896243`). A probe that derives its
  expected number with the patched arithmetic passes over the defect by
  construction (the C50 probe, TestKit `8feaf59`). So: dispatch through the
  production route (an instance-shaped table carrying the built class as its
  metatable resolves identically, with zero map footprint), and compute
  expectations independently — vanilla's algorithm or hand-derived constants.
  Corollary for guard probes: also assert the guard still DELEGATES
  (`LandscapeCostGuard` clause 2 — the clause that found F107; clause 1 alone
  passes for a wrapper that swallows every call). The F33 probe's repair is
  what turned F106 from a standing derivation into a one-boot reversal: a
  probe that can fail is the difference between a derivation and an answer.
- **When a test's trigger is a selection you cannot steer, delete the lottery:**
  invoke the shipped call site directly on a chosen target and settle the
  selection half by reconstructing the pool and reading it (F11's
  `SetCommand("EnterTransporter", …)` is verbatim the shipped caller's body —
  an unrunnable rider became a five-minute answer costing zero expeditions).
- ⛔ **A negative result must state the CONDITION it sampled, not just the
  count** (adopted 2026-08-04, co-run #1 correction C10). "Absence under N
  cycles is a rate bound" holds only if the condition the claim needs was
  actually present in those N cycles; absence of a never-sampled condition is
  not a negative result at all. The breach that earned this: a pre-registered
  corner-slam prediction was recorded REFUTED, with a confident false reason,
  when its y-axis condition had never been sampled — one 64 s re-run sampled
  it and confirmed the prediction to the pixel. The rate-bound rule is about
  counts; this one is about conditions; a verdict needs both.
- **Gates on owner actions DETECT the condition; they never ask for a typed
  token as the primary signal** (co-run #1, found by the owner). Run 1's brief
  told the owner to type a gate the code did not contain — the run proceeded
  without them and only the owner noticed. Run 2 polled until the condition
  itself held (cursor actually reading out of range) and could neither be
  mis-documented nor missed. Typed gates still work as a convenience
  (`GATE 1 RELEASED by owner`); they are one more thing to keep in sync.

1. Load a save (or new game) where the bug reproduces; confirm reproduction
   with the mod disabled.
2. Enable mod; confirm fixed behavior.
3. Confirm no error spam in the log (`%AppData%\Surviving Mars Relaunched\logs`).
4. Save with mod enabled → **disable the pack in the MOD MANAGER** → load: game
   must not break (PT-20 shape; FIX_POLICY §3).
   ⛔ **NOT a Mod Options toggle, ever.** A toggled-off module still has its
   hooks installed and its env present, so a captured frame resolves
   `SMRFixPack`, reads inactive and no-ops — **the load reads clean by
   construction whether or not the module leaks.** `Opt_DroneOverhaul` leaked at
   98 errors/session with its own toggle OFF; that is how F86 Site 2 was found.
   A Mod-Manager disable takes effect only after a FULL PROCESS RESTART; without
   one the pack is still loaded and the reading is a mixed state (PT-20 redo,
   2026-08-14; D13's four-states rule). The earlier 98-vs-98 comparison was taken
   without a restart and is superseded. `EF-002`.
5. Set the entry's status in `agent/bugs/<ID>.md` — front matter AND heading
   tag — per the checklist's reporting protocol. Not INDEX.md.
   ⚖️ **Which word (owner ruling 2026-08-15, checklist 26b):**
   * **`tested-attended`** — the owner was at the keyboard when it was
     confirmed. The strongest word the project has; it is what a
     troubleshooting session is entitled to lean on, because it carries both
     agent instrumentation and human eyes.
   * **`tested-unattended`** — confirmed by real launches with nobody watching.
     Full weight for anything an instrument can read; ⛔ **never for a screen
     event** — "the flag read false" is a measurement, "the popup visibly
     paused" is not, and no unattended leg may claim the second.
   * ⛔ **`tested` (bare) is LEGACY and closed to new work.** The 46 entries
     holding it predate this rule and their attendance was never recorded —
     17 carry the bare word with no narrative at all — so it means "attendance
     unaudited", not "attended". Do not promote one without re-deriving it
     from the archived record; do not read one as if it were attended.

The TestKit's `SMRTest.RunAll()` A/B pair (baseline vs full pack) is the
regression harness; run it as pre-flight when STATUS says one is owed.

### ⛔ Log review: NEVER silently discount a line (owner rule, 2026-08-01)

**Two facts about how legs actually run, and they change what a log is** (full
reasoning: `BUG_LIST_AUDIT.md` §10.6f(i); the same session provisioning is why
our test colonies are heavily loaded before any agent starts):

- **The owner does not close or refresh a game session unless a leg calls for
  it**, so a flushed log typically covers **1–6 hours of continuous play**.
- **The owner reviews the errors WITH the agent** and pushes back when a line
  does not fit the test. That has happened rarely — and **every time it has, it
  turned up a VANILLA defect that was not on our list.** The practice has paid
  for itself; it is not ceremony.

**The rule, and it is the whole point:**

> **"Not caused by our leg" is an ATTRIBUTION verdict, never a reason to stop
> looking.** Locating an error in time answers *"did we cause this?"* — it does
> **not** answer *"what is it, then?"* Collapsing those two is how a discovery
> gets thrown away.

**So: report every unexplained line, state its age, and let the owner decide.**
Do not reason privately that a line is hours older than the leg and therefore
irrelevant, and do not summarise it away as noise. If something is out of the
ordinary, **stop and say so** before continuing the leg.

**Why this works, stated precisely.** The agent writes its predictions before
the run (PT-58's P1–P7 shape) and so knows what it *should* see and why; the
owner independently reviews everything the agent saw and does not know what to
expect. **Anything outside the prediction is signal by construction** — and the
one party able to recognise it is the one being asked not to file it away
quietly. A log that only ever confirms the prediction has been read for the
prediction, not read.

**Corollary worth acting on:** since the logs span hours of ordinary play, **old
logs hold evidence no leg was designed to collect.** Mining them for `[LUA
ERROR]` of any origin is cheap and has a track record.

### ⛔ Cheats on playtest saves are the NORMAL condition, not a deviation (owner rule, 2026-08-12)

**Adopted mid-sitting during `corun-pt60`, in the owner's own words, after a leg
flagged six `ObjCheat CheatFill` markers as if they needed defending:**

> *"We really need a standing rule that these saves are play testing saves with
> colonies that are over sized and underindustrialized. They cannot support
> themselves so cheats are needed to keep the colonies alive and functional. So
> filling food, and maintance materials are needed for the game to run without
> all the colonists dieing or buildings breaking. And unless a chain truely
> needs a no cheat setup we will continue to have to use it, and we will need to
> prep a save with alot of reasouces if we need a no cheat run"*

**What binds, for every future leg:**

1. **The baseline expectation is that cheats WILL appear in a playtest log.**
   Every save in the owner's folder is a heavily-loaded test colony built to
   exercise defects, not a balanced economy — it cannot feed or maintain itself.
   `CheatFill` on food and maintenance resources is **life support for the
   fixture**, and without it the colony dies or its buildings break, which
   destroys the very state the leg was provisioned to read.
2. **Still count them, still name them, still put the reason in the log** —
   the reporting duty is unchanged (`git`-archived logs are the record). What
   changes is the FRAMING: a cheat marker is **attributed**, not excused, and
   **⛔ ask for the reason ONCE.** (`corun-batch-2`'s own ledger records that
   the cheat disclosure took three asks; that is the failure mode this rule
   retires.)
3. **⛔ A cheat is only a confound if the reading intersects what it changed,
   and the agent must NAME the intersection or state there is none.** "Cheats
   were used" is not by itself a caveat on a verdict — e.g. filled storages do
   not touch track shells, dome-Saint modifiers, colony `label_modifiers` or a
   field on `DroneControl`, so PT-60's P8/P9 readings were unaffected and said
   so.
4. **A leg that genuinely needs a no-cheat run must DECLARE it in its brief and
   PREP a resource-rich save in advance.** It cannot be improvised on an
   existing playtest save, and it may not be satisfied by asking the owner to
   stop using cheats on a colony that needs them to survive. Provisioning that
   save is prep-side work with a stated cost, like any other fixture.

**Why this is a rule and not a note:** the owner has now justified the same
practice across multiple sittings, and every re-ask spends the one resource the
co-run model exists to protect. See also the standing fixture rule — playtest
saves are PROVISIONED before an agent ever reads them, so their state is never
"fresh".

**SMR Tool Kit attribution — 2026-09-14 (smrtk 07, as built).** Use the
TestKit's Selected section and World controls in place of vanilla's cheat menu
for playtesting. Selected exposes supported curated and More methods; it does
not reproduce the entire vanilla menu. `[SMRTK] SMRTK_<Verb>` records are
intentional test actions, attributed by construction: **never ask the owner
about one**. Count and name them, and name any intersection with the mechanism
being measured. A vanilla `ObjCheat`/`Cheat` marker in a **new** log is now the
exception worth one attribution question; do not reopen old disclosures.
The taint strip detects a tainted save (`EF-095`). Its separate eligibility
field is `UNAVAILABLE:sandbox` on build 24995074 (`EF-096`); absence of taint
never proves eligibility OK. Normal life-support provisioning remains allowed;
a no-taint experiment must still declare and provision its clean fixture.
The advanced pages are built, with their first attended checks assigned to 08.

### ⛔ BOTH MODS LOADED is the rig's NORMAL condition (owner rule 2026-08-12 — ⚖️ ACTIVE since the `split-optins` terminal audit, same date)

**The owner's words, given while the `split-optins` chain was authored:**
*"Once we get it seperated I will keep the opt ins loaded in as they make
testing easier. So the agents should be aware of that, and it shouldn't be an
issue because we should be compatible as well."*

**What binds, for every leg after the split chain closes:**

1. **The baseline rig configuration is BOTH mods enabled** — the fix pack AND
   the standalone opt-in mod. A gate read shows two registries. ⭐ **MEASURED
   BASELINE (cell a2, 2026-08-12, audit-recounted from
   `archive/spa2_Mars.exe-20260812-18.44.24.log`): `fix pack present: 74/74` ·
   `opt-in pack present: 8/8` · suite ~~`78/0/10/0 of 88`~~ ⭐ **RE-MEASURED
   2026-08-13 (`archive/rs_r0_*`): `78 PASS / 0 FAIL / 16 SKIP / 0 ERROR` of
   94** — the six new SKIPs are the Save Rescue probes standing down (that
   separate rescue mod is NOT a standing rig mod; with it loaded the same run
   reads `84/0/10/0`, `rs_r1_*`), SKIPs BY NAME in `agent/STATE.md`; load order
   `1:SMR_CommunityFixPackTestKit 2:SMR_CommunityFixPack
   3:SMR_CommunityOptInPack` (enable order, `EF-054` — opt-in wrappers sit
   OUTERMOST).** Every "the pack" claim names WHICH pack. An opt-in-mod line
   in a fix-pack leg's log is expected background: attributed, never flagged
   as foreign.
   ⛔ **THAT SUITE BASELINE IS VOID as of 2026-09-09 (`100_DOCSWEEP`).** It was
   measured on the 74-module pack against game 1.0.7; the pack is now 44
   modules, the kit is a different 94-probe set rebuilt for 1.1.0 (32 of them
   `retired`), and the game is 1.1.0. The new baseline is the next attended
   `SMRTest.RunAll()` after the hotfix-2 upload, which re-stamps this line —
   none is written here.
2. **Same confound rule as cheats:** a loaded opt-in module is only a confound
   where the reading intersects what it changes (D09 dials touch drone
   speed/carry; NoHomeless/CohortHousing move colonists; MultipleSuns touches
   build limits) — **name the intersection or state there is none.** "The
   opt-in mod was loaded" is not by itself a caveat.
3. **A leg that genuinely needs the opt-in mod OFF must DECLARE it in its
   brief** — and budget the toggle honestly: a Mod-Manager disable takes
   effect only after a FULL PROCESS RESTART (D13's four-states rule), and the
   re-enable is handed back to the owner like any pack re-enable.
4. **The standing configuration is also the compatibility soak.** The owner's
   ordinary testing IS continuous both-mods exposure; any cross-mod
   interference that survives the split chain's matrix will surface here
   first — whole-log reviews watch for it as a named class, and a hit routes
   to BOTH repos' records.

⚖️ **ACTIVATED 2026-08-12 by the `split-optins` terminal audit** (the twin
clause in the new repo's WORKFLOW was activated in the same close). Single-pack
gate reads (`81/81`-era and earlier) are history — use their archived logs when
needed, and never quote them as current.

## Co-runs — moved 2026-09-12 (D5) to `agent/support/CO_RUNS.md`; still binding when a batch of bugs is being tested attended.

## Sign-off tiers — standing policy for every leg (adopted 2026-08-04, owner; stayed here when Co-runs moved out)

**Sign-off tiers: ✅ ADOPTED 2026-08-04 (owner, in their own hand on the
checklist — `----Approved` on the tiers item; integrated by the unattended-1
terminal audit).** Standing policy for every leg from here on:

- **Tier A — WITNESS.** The owner's eyes genuinely add information the log
  cannot carry; they attend the measure moment. Unchanged from before.
- **Tier B — EVIDENCE CARD.** Log-demonstrable; the owner quick-reads a
  one-screen card — scenario, forced-vs-organic, the raw before/after log
  lines, run conditions, the one-sentence falsifier — and OKs it. Sub-class
  **HANDS-ONLY**: a leg needing the owner's hands (a click, a cursor park)
  but not their eyes — they do the named act, then read the card as Tier B.
- **Tier C — DELEGATED.** Mechanically self-verifying (the probe-suite
  class): ships on the suite verdict; the owner gets a one-line digest per
  batch and keeps the veto.
- **Visible demotion:** when a designed-A item's card turns out strictly
  stronger than the eyes, the demotion is stated ON the card and applies to
  the NEXT instance — never silently.

⛔ **What adoption does NOT carry, in the item's own words:** *"`tested` still
means a pass at the keyboard per WORKFLOW, and no already-granted status is
reclassified."* Neither moves. ⚠️ The tiers are a *sign-off* axis, not this
routing axis: the triage above says who is present during a leg; the tiers
say what the owner reads afterwards. Owner-facing record of the decision:
`PLAYTEST_CHECKLIST.md` "Decisions waiting on you", 2026-08-04.

## Release steps

- Owner tasks first: preview image (PDX ≤2 MB / Steam ≤1 MB), screenshots,
  portal rules check for console publishing (`docs/archive/AUDIT_FINDINGS.md` plan 2.5).
- metadata.lua: bump `version_major`/`version_minor`, refresh `last_changes`.
  `short_description`, `optional_mod` are already in place (audit 2.1).
  `lua_revision` stays 350453.
  ⛔ **`ignore_files` is NOT already in place — owner ruling 2026-08-13
  (checklist 23), do it in this pass, in ALL THREE mods.** The upload packs the
  **entire mod folder recursively** and filters only on these patterns
  (`ModTools\Src\CommonLua\Classes\GedModEditor.lua:678-741`), so everything
  unlisted ships inside the player's download. Nothing *runs* (only `code`-listed
  files execute), but `CLAUDE.md` is agent instructions and does not belong on a
  player's disk. ⭐ 2026-09-10: `AGENTS.md` (the Codex mirror of `CLAUDE.md`)
  joined the list — `*AGENTS.md` sits in `metadata.lua`'s `ignore_files`, in
  `tools/pack_predict.py`'s literal `IGNORE` copy of that list, and in
  `upload_preflight.py`'s check, all three together. doccheck's **PACK IGNORE
  PARITY** gate fails when the predictor's copy and `metadata.lua` disagree, so
  a pattern added in one place turns the gate RED rather than making the
  predicted count lie. `upload_preflight.py`'s pack guards read the live list.
  ⛔ **2026-09-16 — the packer walks through junctions and symlinks.** A junction
  to the user's Claude projects folder sat in the mod folder outside every
  pattern; ~1.2 GB of private session transcripts entered the pack list, and
  the pack failed only on size — silently, since `DbgPackMod` ignores the error
  and opens `explorer ""`. `upload_preflight.py` now FAILs on a link whose
  contents would pack, on any packed file other than `Code/*.lua`,
  `metadata.lua`, `items.lua`, `LICENSE` and the preview image, and on a pack
  over 5 MB (falsified 2026-09-16 on scratch copies, one leg per guard).
  **Never put a link inside the mod folder unless an ignore pattern covers it.**
  ⭐ **Re-derived per mod 2026-08-13 (`public-docs/02_QA.md`) —
  the three lists are NOT the same:**
  | mod | add |
  |---|---|
  | fix pack | `tools/` · `CLAUDE.md` · `LICENSE` · `.gitattributes` |
  | opt-in pack | the same four |
  | **save rescue** | **`LICENSE` only** — it already ships a `*CLAUDE.md`
    pattern the other two lack, and has no `tools/` and no `.gitattributes` |
  ⭐ **Copy the rescue mod's `*CLAUDE.md` line into the other two** rather than
  inventing a pattern. ✅ `.github/` is no longer a question — the fix pack has
  none since the site moved out, and neither of the others ever had one.
  ⚠️ **One wildcard question survives and one command settles it:** whether `*`
  crosses `/` decides whether `*/docs/*` filters the whole `docs/` tree or only
  its top level. The engine's own defaults (`*.git/*`, `*/Source/*` —
  `Mod.lua:255`) only make sense if it does, but `MatchWildcard` is an engine
  function with no Lua body. ⇒ **Pack once with `DbgPackMod`, list the archive,
  confirm `docs/` is absent** — do it in this same pass.
- MOD_DESCRIPTION.md: delete the `[DRAFT NOTE]` markers; do NOT promise the
  ClassicRockets export half; sync the fix list with agent/bugs/ statuses.
  ⭐ **Add the "judgment calls" section** (owner ADOPTED the relabel proposal
  2026-08-04: F55, F40, F73(b), F70, F97 presented as design-judgment repairs,
  not plain bugs) — ⚠️ **its wording is OWED BY THE OWNER** and must be asked
  for if it does not exist yet; the checklist line tracks it.
  **Recount the probe number** quoted in the "What we can promise, and what we
  can't" block — it moves whenever a wave file gains or loses a probe, and a
  stale number there is a false claim in player-facing text. Authoritative count
  is in `agent/STATE.md`.
- **Drone overhaul, if it has shipped by then:** its design-drift disclaimer is
  MANDATORY (owner requirement — spec in `docs/archive/DRONE_RESEARCH_BRIEF.md`). Do not
  publish the module without it.
- Upload via the in-game Mod Editor (Paradox Mods / Steam Workshop). The
  editor round-trip is SAFE since audit 2.2: items.lua carries one
  `ModItemCode` per Code/ file in metadata order, so SaveDef regenerates the
  same `code` list. If a Code/ file is ever added/removed/reordered, update
  BOTH metadata.lua `code` AND items.lua in the same commit, same order.
- The TestKit must NOT be uploaded.
- Credit ChoGGi (Fix Bugs) + LukeH (Martian Express) as prior art — and the
  prior-art survey (`docs/agent/reports/PRIOR_ART_SURVEY.md`) backs the save-safety claim in
  player-facing text.

## Release marking — tags, not branches (adopted 2026-08-17)

**What is live on the portal is a fixed point in history, so it is marked with a
TAG.** `main` is *latest verified work*; the tag is *what shipped*. Main sitting
ahead of the published version is the NORMAL state of a mod repo — the reference
mod we surveyed publishes from tags and runs seven versions ahead on `main`.

⛔ **No standing `testing`/`published` branch, and the reasons are specific to
this repo — re-read them before anyone proposes one again:**

1. **The junction makes the checked-out tree the running mod.**
   `%AppData%\Surviving Mars Relaunched\Mods\SMR-BugFixPack` is a directory
   junction into the dev repo, so whatever is checked out is what the game
   loads. Every gate reading this project treats as load-bearing (`75/75`, the
   suite counts, the SKIP set BY NAME) would silently become "…on whichever
   branch was last checked out."
2. **The truth-bearing documents are rewritten in place, not appended.**
   `STATE.md` has hard byte caps with an eviction rule; `bugs/INDEX.md` and
   `facts/INDEX.md` are GENERATED. Parallel long-lived branches means every
   merge conflicts on exactly those files, and a badly-resolved `INDEX.md`
   merge is a red doccheck at best and a wrong index at worst.
3. **Uploading is manual** (in-game Mod Editor / portal, no CI), so "main holds
   unshipped code" only bites if you upload carelessly — and tagging at upload
   removes that.

**At upload, per mod:**

```
git tag -a fixpack-v<major>.<minor>.<version> -m "uploaded <portal> <date>"
git push origin <tag>
```

- Tag names: `fixpack-`, `optin-`, `rescue-` + the version `PackVersion` reads,
  which is `version_major.version_minor.version` from `metadata.lua`.
- ⛔ **The tag and `metadata.lua` must agree.** A tag whose version does not
  match the tree it points at is worse than no tag.
- Record portal version → commit sha on the ④ sheet
  (`agent/reports/RELEASE_PORTAL_PREP.md`) in the same pass.

**To reproduce what a player is running** — never disturb `main`:

```
git worktree add ../SMR-FixPack-shipped fixpack-v1.0.0
```
…then point the junction at that worktree for the investigation and put it back
afterwards. ⚠️ While it is pointed there, **the rig is running the shipped code,
not `main`** — no suite reading taken in that window describes current work.

**Hotfix path**, created the day it is needed and not before:

```
git checkout -b hotfix/fixpack-1.0.1 fixpack-v1.0.0
```
…fix, ship, tag, merge back to `main`.

⚖️ **When a short-lived branch IS justified:** a single chain producing code
nobody is sure about (a `FIX_POLICY` §1.5 full replacement is the standing
example). Branch per chain, code only, merged within days — ⛔ **doc changes
still go to `main` directly**, or reason 2 above bites.

## Authoring a prompt / job brief — required elements

Use the `prompt-authoring` skill for a brief written for another session.
Its body carries the required elements and the R-C derived-facts procedure.

**R-D · Self-split, authoring-side.** Depth is the cost: the same unit of work runs several
times more expensive deep in a session than early in one. So legs are **packed at authoring**
to roughly `filesize/4 × 1.7` and ~75% fill, never pushed to the edge of a window, and a retry
is a fresh fire rather than a continuation. Working legs are **blinded** to this — an agent
that feels a budget cuts the corner you cannot see. Attended sittings are exempt: they are
indivisible and run to their natural end.

## `[FAQ]` — the tag for "a player will ask about this"

Owner intends to write an FAQ doc at some point. Rather than start one early
(and rather than let the material scatter), **tag the source of truth in place**
with the literal marker `[FAQ]` and collect it later:

```
grep -rn "\[FAQ\]" docs/ Code/
```

Rules that keep the tag worth having:

- Put it on the **entry that already explains the thing** — an `agent/bugs/` entry, a
  parked item, a module header. Never create a doc just to hold a tag.
- Tag **behaviour a player could reasonably mistake for a bug**, or a question
  the design deliberately answers "no" to. Not every quirk.
- A `[FAQ]` tag is **not work and not a promise** — it is a bookmark. Writing
  the FAQ is a launch-time task, and tagging things is not progress toward it.
- If the tagged behaviour is later changed or fixed, **remove the tag** in the
  same commit, or the FAQ inherits a stale answer.

Currently tagged (re-derived from `grep -rn "\[FAQ\]" docs/ Code/` on
2026-08-01 — the previous list named a tag in `MOD_DESCRIPTION.md` that did not
exist):

- D01's parked-rocket activation limitation — `agent/bugs/` D01 entry +
  `FUTURE_IDEAS.md` entry 2.
- The save-repair framework's honest limits — `FUTURE_IDEAS.md` entry 4.
- "Put the mod back" as advice for a damaged save, and its F88 caveat —
  `agent/bugs/` F88 entry.
- The uninstall procedure and the standalone save-rescue artifact —
  `agent/bugs/` D13 + `FIX_POLICY.md` §3a + `F86_EXECUTION_PLAN.md` Phase 5.
- **Why we make a fuss about the savegame footprint at all** — the documented
  engine behaviour (mod code is serialised into saves by design) and the
  community norm we deliberately exceed: `MOD_DESCRIPTION.md`, added
  2026-08-01 from `PRIOR_ART_SURVEY.md` §1/§2/§4.
- **The no-precedent uninstall claim** — `MOD_DESCRIPTION.md`, added
  2026-08-01 but **written conditionally and marked do-not-publish until F86
  Tier 1 lands and verifies** (`PRIOR_ART_SURVEY.md` §6). A tag on a claim
  that is not yet true has to say so.

## Verification rails (adopted 2026-09-12, owner)

The global verification duties R-A, R-B, R-E, and R-G now live in `CLAUDE.md`'s
`Must_Read_Header`. The task-specific rails remain here.

R-C (brief element 9) lives in the `prompt-authoring` skill.

**R-F · Size the verification by owner-observability.** A player-visible defect is verified by
one attended A/B in the game — the owner is the cheapest verifier of "can a player actually do
this". An engine-internal defect is verified by desk harness plus audit, because no amount of
watching would show it. Choose the leg by who can see the thing, not by how thorough it feels.

### What these rails are not
They are not a licence to re-derive everything. Zero-trust re-derivation is the terminal
audit's job and no one else's: build legs **inherit** behind a fingerprint and re-derive only
what moved. A mechanism that is skeptical everywhere is the known failure mode — 26 chains
bought 4 real catches, all of them adversarial measurement, and a 45-seat review pilot bought
none. Cheap trusting workers, one expensive skeptic, triggered rather than constant.

### Trust by source
The three classes are stated once, in `CLAUDE.md`, because every agent needs them before it
could decide to load anything. R-A is how class 2 is discharged: one command, not a re-read.

## Writing in a shared tree (traps, each one cost a real error)

`80_AgentSlots.lua` is agent-owned, rewritten per sitting using `agent/support/SMRTK_SLOTS.md`, never edited by a build link.

Five or more interactive sessions work this checkout at once. The global identity,
attribution, status, and hunk-staging duties now live in `CLAUDE.md`'s `Must_Read_Header`.
- ⛔ **After a CHECKLIST-ONLY edit run `python tools/doccheck.py --regen-waiting`, NOT `--regen`.**
  `--regen` rebuilds both indices from **every entry on disk, a peer's uncommitted ones included**.
  An edit that touches **entries** as well still needs the full `--regen` — the distinction is what
  you changed, not a preference. Before any `--regen`, check `git status docs/agent/bugs/` for
  foreign ` M`/`??`.
