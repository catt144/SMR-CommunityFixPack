# Chain prompt 2 — adversarial audit, integration, chain close

**Read `README.md` in this folder first — binding chain rules apply. You are
the terminal prompt: this folder must be EMPTY when you finish.** Unattended.
Start with `git log --oneline -10` + `git pull`. Todo list up front.

**Read path**: this folder's remaining files · the outbox below · every
entry/checklist line prompt 1 touched · the archived logs it cites · every
module/TestKit file it edited (diff the shipped Lua against the entry's
described change — the CODE is a claim too) · the audit precedents
(`git show 0b22bc4^:docs/agent/prompts/corun-batch-2/03_FABLE_AUDIT.md` had
no build to audit; the batch-2 close record in SESSION_LOG 2026-08-10 sets
the log-fidelity floor).

**Every "done", "PASS", "SKIP" and "repaired" upstream is a claim.** This
chain SHIPPED CODE, which raises the floor: the audit verifies the shipped
diff against the entry's decision block AND against Src (README rule 13),
not just the log against the record.

## Jobs

**Job 1 — audit the record against the archived logs and the shipped code.**
Byte-compare every archived log against its on-disk original over the FULL
length; read the WHOLE log yourself. Per item: **F48** — the pass's repair
count line exists (R7), the case-A repair held across the R4 round trip, the
clean-fixture run reports zero, and the shipped diff is exactly the corrected
call the entry specifies (Src-verify the site yourself — trust nothing
carried). ⛔ If prompt 1 shipped on a failed acceptance, the audit REVERTS
and routes — that is a stop-condition breach, not a judgment call. **C43** —
the suite log carries zero TestKit `[LUA ERROR]`, the SKIPs print their
reason, no other probe verdict flipped, and the `set_global` caller count
landed on the entry. **F100** — the new line is in the boot log verbatim and
`81/81 active` holds. **PT-35 leg A** — every read has its before/after AND
its round trip; APPLICABLE=true on the turbine half (population 1, not 0);
zeros state their sampled condition. Forced/organic labels present (all
forced); no `tested` granted anywhere (nothing here can earn it). Commit
discipline: probes deleted, sweeps present, staged copies gone,
**`PT35FIXTURE.savegame.sav` and `TEST2H TRAIN` present and byte-verified**,
every cited log `git show`-verified. ⛔ A missing archived log is an
automatic finding. Whole-log sweep: unexplained lines with their age;
`TrackElement.lua:805` (an ORGANIC hit reopens F99 per the owner's
passive-watch ruling — route it); `invalid pos with no holder` (C45's
settling grep — a hit here is its second occurrence, record per its entry).

**Job 2 — status honesty.** F48's status matches what actually held
(`fixed` needs 4a+4b+4c; anything less stays `directed` with the gap named).
C43/F100 close only if their acceptance readings are in the archived log.
PT-35: leg A's turbine half either moves to its archive-ready state (case A
complete IN FULL — say whether the section archives or what remains) or
records exactly which read failed. Corrections visible, never silent; a
correction that changes a verdict re-routes that item to the owner.

**Job 3 — the ledger.** Prompt 1's misses vs the standing harness-rule
blocks (unattended-1's 1–4, batch-1's 1–6, batch-2's 1–9): what recurred (a
rule that fails twice is broken — say which and repair it in WORKFLOW
surgically), what is NEW. Economics one line (machine time; owner cost =
the kickoff word).

**Job 4 — integrate and close.** Entries verified carrying their verdicts;
checklist PT-35 line final; `STATE.md` chain CLOSED + outcomes + NEXT
(cap 60); `SESSION_LOG.md` record newest-first; `CHAIN_METHOD.md` one row
ONLY if this chain taught something the method does not already record.
Delete every remaining file in this folder in the closing commit (cite the
pre-deletion sha in the SESSION_LOG record). doccheck GREEN, push. **The
owner report ENDS with the next-chain kickoff** (chain rule 14): the
expected front is the **PT-20 redo co-run** (+ the 10-second Ctrl-F9 check
that settles F85) — if its chain is not yet authored, say so plainly and
name what authoring it takes.

## Stop conditions

- A load-bearing verdict fails its audit and the logs cannot settle it →
  correct visibly, re-route to the owner, keep closing.
- The run was partial → audit what ran, inventory the remainder into
  TAKEABLE riders with staged state cleaned up, and still empty the folder.

## ⛔ What you may not claim

- Not `tested` for anything — no owner eyes were anywhere in this chain.
- Not "the sanitizer is safe" in general — one fixture, one lineage; PT-35
  cases B/C stay parked and the do-no-harm claim stays scoped to what ran.
- Not any owner decision — F85 waits on its Ctrl-F9 evidence; the relabel
  wording stays owed; nothing this chain finds changes a ruling on its own.

## Notes from upstream

### ⛔ READ THIS FIRST: THE CHAIN IS BLOCKED, NOT FINISHED

**All three builds shipped. Not one acceptance reading exists.** The launch
that was to take them found **the Community Fix Pack DISABLED in the owner's
Mod Manager** — `pack=0/0 active`, and the engine's own line reads *"This
savegame tries to load Mod Community Fix Pack …, which is present, but not
loaded"*. `corun-batch-2`'s leg T turned it off on 2026-08-10 to test the
uninstall and nothing turned it back on. It is one human click, and it is
**source-proven unscriptable**: `AccountStorage`, `SaveAccountStorage` and
`ModsReloadItems` are all `ModEnvBlacklist` keys (`Mod.lua`) and there is no
console at the main menu. Routed as **tick 1** in a new block at the top of
`PLAYTEST_CHECKLIST.md`.

⇒ **Your Job 1 has almost nothing to audit against logs, and your Job 2's
status question is already answered: F48 stays `directed`, C43 and F100 stay
`filed`.** What you CAN audit in full is the shipped code against the entries
and against Src (which prompt 2's own brief says is the raised floor), plus
everything in this outbox. Your stop condition "the run was partial" is the
live one.

⇒ **The folder-empty rule collides with the re-run.** The parked instruments
(`97_U2Common.lua.txt`, `98_U2Run.lua.txt`, `U2_ARM.ps1.txt`) are what the
re-run needs. Your brief tells you to empty the folder even on a partial run,
so delete them and **cite the pre-deletion sha in the SESSION_LOG record** —
the re-run resurrects them the way batch-1's and batch-2's are resurrected.
State the exact `git show` path in the owner report so it is one command.

### What ran, and what each log may be quoted for

| log (archived, `cmp`-verified) | what it is |
|---|---|
| `docs/archive/u2run1void_Mars.exe-20260811-01.17.34.log` | run 1. **VOID for every pack-dependent claim.** Quotable for: the blocker itself, and the fixture confirm (which needs no pack). |
| `docs/archive/u2run2rehearsal_Mars.exe-20260811-01.24.25.log` | run 2, a **declared HARNESS REHEARSAL** — it says so in its own `MODE` banner and stamps `VOID(pack not loaded)` on every verdict line. Quotable for the flow working and **for nothing else**. |

⚠️ **One trap, stated so you do not walk into it:** the rehearsal log carries
**0 `[LUA ERROR]`** and a full `RunAll` (1 PASS / 71 FAIL / 15 SKIP / 0 ERROR).
That is **not** C43 evidence. With the pack absent, `SMRTest.FixMissing` FAILs
nearly every probe before it reaches a stub — `AnomalyCaveInMap` included, which
returns at its step 2 and never reaches the `:415` call that raises. The two
error lines are absent for the wrong reason. Zero `set_global refused` lines
appeared for the same reason.

### Job 1 findings you should verify rather than inherit

1. **F48's shipped diff.** Src-verify `Station.lua:1346` and
   `Tracks.lua:807/:808/:820-822` yourself. Check specifically that the pass
   counts an EFFECT (connection total + duplicate `node_idx` either side of each
   call), that the summary line prints on zero, that the console entry point
   **ignores** the one-shot flag, and that no `start_el`/`end_el` is
   hand-assigned (correction (d), applied to shipped code this time).
2. **C43's real finding, which is bigger than the noise it fixes.**
   `IsNearDome` and `AddAreaRubble` are **`local function`s** —
   `CaveInRubble.lua:79` and `:38`. Those stubs could never have worked through
   `_G`. Verify it; if it holds, the open question for the owner is whether the
   two dead stub entries should simply be deleted (which would restore the PASS
   honestly and remove the SKIP). Nothing was deleted, deliberately.
3. **A correction to the record itself:** there are not "two Wave-5 probes".
   One probe, two undeclared names, one `TryWithGlobals` call. The C43 entry's
   own log quote said so; every downstream summary — including this chain's
   prompt 1 — read it as two probes.
4. **The static half of C43's un-counted gap is counted** (60 stub call sites /
   10 probe files, 6 direct `SetGlobal` calls, 1 in the core; no third
   file-local among the engine-name targets). The **live** half is honestly
   UNSAMPLED and says so on the entry.
5. **PT-35's fixture is re-confirmed good and APPLICABLE=true on BOTH halves**
   (1 Large turbine; 144 upgraded buildings; 3 live upgrade-shaped modifier ids
   across 13 domes). Stop condition 3 is NOT triggered. ⚠️ The Remote Medic
   upgrade specifically was **not** identified — 144 upgraded buildings were,
   with four `SmartHome_Small` examples printed. Do not let that gap close
   silently.

### ⭐⭐ The out-of-scope discovery, already routed

**Steam Cloud restores deleted savegames at launch.** 55 `.sav` files before
launch 1, **69** after launch 2 — **14** staged saves this project had
verifiably deleted came back, each with a `CreationTime` inside the
01:17:04–01:17:33 launch window, its original modification date preserved, and
**all written before `Mars.exe`'s process start at 01:17:34**. `EF-051`. This
**clears two sessions recorded as having failed the save-dir gate** — they had
deleted the files. Checklist item 7's parked hypothesis is closed by
measurement; the remedy is checklist tick 2. ⛔ **Prediction with its
falsifier, for you to check:** `U2STAGE`, `U2RT1`, `U2RT2` (deleted 01:28) are
expected BACK after the next launch. If they are not, EF-051's mechanism is
wrong and needs re-deriving.

### Job 3 — the ledger, mine, and what I already repaired

**Two harness defects, both mine, zero the game's fault.**

* **U1 — no run-condition gate.** `ReadConditions` printed `pack=0/0 active` and
  the payload ran six more steps taking readings about code that never
  executed. **batch-2 rule 7 RECURRED**, in a new way: it bound a reading taken
  after a mutation *inside* a sitting, and said nothing about a process that
  simply STARTS in the state a previous sitting left. A rule that fails twice is
  broken, so I repaired it in `WORKFLOW.md` surgically — the gate now binds at
  the top of EVERY run and **must STOP the run, not merely print**. Mechanised
  as `U2.RequirePackLoaded`, default stop. ⇒ **Review that edit; it is mine and
  it is unaudited.**
* **U2 — `savename` is written VERBATIM** (`EF-050`). Asking for `U2RT1`
  produced a file called `U2RT1`; `LoadGame("U2RT1.savegame.sav")` returned
  `File Not Found`, and `SaveGame`'s own `err=false` said nothing about it.
  Every earlier caller passed the extension by habit, so the logs read as though
  the engine appended one. **Resurrecting a primitive means resurrecting its
  ARGUMENT CONVENTION, not just its body** — that is the class, and it is new.
* **Both were fixed and then PROVEN**, not merely asserted: the rehearsal drove
  all 15 steps, three loads and two save/reload round trips clean, with the
  corrected names appearing as `name=U2RT1.savegame.sav` /
  `name=U2RT2.savegame.sav` and the gate firing exactly as designed.

**A judgment call you should second-guess.** `account.dat` holds
`AccountStorage.LoadMods`. I opened it, found a `BPUL` container with a
plaintext metadata header and a compressed body, and **did not write to it** —
flipping a checkbox is not worth a hard-to-reverse write to the owner's account
state at 1 am without authorisation. If you disagree, say so; it is the one
place tonight where a different call would have unblocked everything.

**Whole-log review, both logs.** 0 `[LUA ERROR]`, 0 `TrackElement.lua:805`
(F99), 0 `invalid pos with no holder` (C45). Two `[ResManager Error]` lines for
missing `LawOfficeDoor` animations — reported, not discounted, and their age is
the answer: identical pairs appear in **all 26 archived logs** back to
2026-08-03, and they are already on record. ⚠️ Note the F99/C45 zeros are over a
window with **no pack loaded and no track mutation**, so they are not a sample
of either condition.

**Economics.** ≈9 minutes of machine time over two launches; owner cost was the
kickoff word. Nothing to report as saved — the run did not deliver its purpose.

**Close-out state.** Both trees clean, probes disarmed (`PROBE SWEEP: clean`),
all staged saves deleted and the save directory listed, both protected files
byte-verified (`PT35FIXTURE` MD5 `D721329D1EE18604B3D6C89401F74738`;
`TEST2H TRAIN` MD5 `103B320A1434513BC8773553096A8958`, mtime 2026-08-03
22:21:48). doccheck GREEN. Everything FORCED/staged; no `tested` granted
anywhere; no owner decision assumed.
