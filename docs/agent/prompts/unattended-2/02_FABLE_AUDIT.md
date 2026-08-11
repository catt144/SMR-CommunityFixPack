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

### The chain was blocked for one launch, then unblocked and completed. Audit the SECOND run.

The night ran in two halves. The first launch was **VOID** — the Community Fix
Pack was disabled in the owner's Mod Manager (leg T residue from 2026-08-10),
`pack=0/0 active`. The owner re-enabled it, said plainly *"there is no point in
doing an audit for a pack off run"*, and the run was redone. **All four items
then passed their acceptance in full.**

⇒ **Audit `docs/archive/u2run3_Mars.exe-20260811-02.01.06.log`.** The two
earlier logs are archived and cited, but they are evidence about the harness and
the blocker, not about the fixes.

| log | what it may be quoted for |
|---|---|
| `u2run3_Mars.exe-20260811-02.01.06.log` | **THE RUN.** Every verdict below. |
| `u2run1void_Mars.exe-20260811-01.17.34.log` | the blocker, and the fixture confirm (pack-independent). Nothing else. |
| `u2run2rehearsal_Mars.exe-20260811-01.24.25.log` | a declared HARNESS REHEARSAL (its own `MODE` banner says so, every verdict line stamped VOID). The flow working, and nothing else. ⚠️ Its 0 `[LUA ERROR]` and 0 `set_global refused` are absent for the WRONG reason — with no pack, probes FAIL before reaching their stubs. Do not quote them for C43. |

### Statuses moved, and here is what each one rests on

**F48 → `fixed`.** (a) The automatic pass repaired **7 of 17 tracks, 0 raised**,
and every one landed on `2 × (n−1)`: `#4569` 7→6, `#4619` 45→44, `#4730` 86→84,
**`#12454` 559→558**, `#12528` 63→62, `#12637` 34→32, `#13418` 133→132. That
fourth one is PT-37's own track and its own numbers, reproduced by shipped code.
The seven together upgrade this entry's *"consistent with removing one stale
connection"* from an inference to a measurement — two tracks shed two
connections, and all seven hit the clean-chain value exactly. Held across BOTH
round trips (`0 of 17` on the full per-track signature, twice). (b) Zero three
ways on the clean save, including a direct call that ignores the one-shot flag
by design, so the zero is sampled rather than an early return; the flag itself
was **read** (`= true (type=boolean truthy=true)`), not inferred from missing
lines. (c) The count line prints on every run including the zeros.
⇒ **Verify the shipped diff against Src yourself** (README rule 13) — the entry
claims `Station.lua:1346`, `Tracks.lua:807/:808/:820-822`.

**C43 → `fixed`.** Zero TestKit `[LUA ERROR]` in 1,009 lines; the refusal fired
by name exactly twice; `AnomalyCaveInMap` SKIPs with a message stating what did
and did not get exercised; `77/0/10/0` against the baseline's `78/0/9/0` with a
per-probe diff over all 87 rows returning **exactly one line**. The un-counted
gap is answered by execution: **no other caller** hit the undeclared case across
60 stub call sites. ⚠️ Scope I wrote onto the entry and you should check I kept:
10 probes SKIPped for want of game state, so this is "no other caller reached it
in this run", not a proof over unreachable code.

**F100 → `fixed`.** New line verbatim at `:159`, between `00_Core`'s
authoring-error line at `:158` and `NoHomeless: applied` at `:190`;
`81/81 active`; `NoHomeless` probe PASS. The `Require` target deliberately did
not move.

**PT-35 leg A case A → COMPLETE** (not `tested`, and the checklist says so).
`0 of 14 readings changed` at every comparison including start-to-finish over
three loads, two round trips and six pass calls. ⭐ The two zeros that matter:
`RepairTurbineBuff` no longer early-returns (tech researched, whole body walked,
already-buffed guard did the skipping — `unattended-1`'s zero was UNSAMPLED),
and `RepairLeakedUpgradeModifiers` returned 0 with **3 live upgrade-shaped ids
and 144 upgraded buildings** in front of it.

### Findings to verify rather than inherit

1. **`IsNearDome` and `AddAreaRubble` are `local function`s** —
   `CaveInRubble.lua:79` and `:38`. Those stubs never worked through `_G`,
   before or after the fix. ⚖️ **Open for the owner:** deleting the two dead stub
   entries would restore the PASS honestly and remove the SKIP. That is a
   different repair from the one decided, so nothing was deleted.
2. **There are not "two Wave-5 probes"** — one probe, two names, one call. The
   original log said so; every summary since, including this chain's own prompt
   1, read it as two.
3. **EF-051 (Steam Cloud restores deleted saves) was predicted and then
   CONFIRMED**: the three saves deleted at 01:28 were all back by 01:57:47 —
   the owner's launch — plus a fourth artifact. Two independent launches. The
   listing rule caught the fourth at close-out.

### Job 3 — the ledger

**Two harness defects, both mine, zero the game's fault, both fixed and then
proven by a rehearsal before the real run.**

* **No run-condition gate.** batch-2 rule 7 RECURRED in a new shape — it bound
  readings after a mutation *inside* a sitting, not a process that starts in the
  state a previous sitting left. Repaired surgically in `WORKFLOW.md`: the gate
  binds at the top of every run and **must STOP it**. ⇒ **That edit is mine and
  unaudited; review it.** Mechanised as `U2.RequirePackLoaded`, and it fired
  correctly in both later runs.
* **`savename` is written VERBATIM** (`EF-050`). `err=false` said nothing about
  a file `LoadGame` could not find. Class: resurrecting a primitive means
  resurrecting its ARGUMENT convention, not just its body.
* **A third, caught not committed:** a Python read/write on `C43.md` silently
  turned a stray `CR` byte into a newline, mangling a line unrelated to the
  edit. Found by reading the diff instead of trusting the tool; restored
  byte-for-byte. The project's PS 5.1 encoding rule has a Python sibling and the
  SESSION_LOG now says so.

**Also mine, and I would like it second-guessed:** `account.dat` holds
`AccountStorage.LoadMods`. I opened it, found a `BPUL` container with a
plaintext header and a compressed body, and **did not write to it** — a
hard-to-reverse write to the owner's account state at 1 am to flip a checkbox.
The owner's own re-enable made it moot, but say if you think the call was wrong.

**Whole-log review, run 3.** 0 `[LUA ERROR]`, 0 `TrackElement.lua:805` (F99),
0 `invalid pos with no holder` (C45). ⚠️ Both zeros are over a window with **17
healthy tracks, 0 broken elements and 0 repair sites** and no track mutation —
so neither condition was sampled and neither is a negative result. Two
`[ResManager Error]` lines for missing `LawOfficeDoor` animations: reported, not
discounted, and their age is the answer — identical pairs sit in every archived
log back to 2026-08-03.

**Economics.** ~13 minutes of machine time across three launches. Owner cost:
the kickoff word, one Mod-Manager tick, and one sentence.

### Close-out state, and the folder

Probes disarmed (`PROBE SWEEP: clean`), all staged saves deleted — including
one Steam had restored between runs, which the listing rule caught — save
directory listed at 69 files with **no `U2*` leftovers**; both protected files
byte-verified (`PT35FIXTURE` MD5 `D721329D1EE18604B3D6C89401F74738`;
`TEST2H TRAIN` MD5 `103B320A1434513BC8773553096A8958`, mtime 2026-08-03
22:21:48). Both trees clean, doccheck GREEN, pushed.

⇒ **The folder still holds `97_U2Common.lua.txt`, `98_U2Run.lua.txt` and
`U2_ARM.ps1.txt`.** They are inert (the mod loads only what `metadata.lua`
lists). Your done-condition is an empty folder, so delete them in the closing
commit and **cite the pre-deletion sha in the SESSION_LOG record** — they
survive in git the way batch-1's and batch-2's parked instruments do, and the
`git show` path belongs in your owner report.

⇒ **The owner's remaining tick is Steam Cloud** (checklist top block). The next
kickoff after you is the **PT-20 redo co-run** (+ the Ctrl-F9 check that settles
F85) — **its chain is not authored**, so say so plainly and name what authoring
it takes.
