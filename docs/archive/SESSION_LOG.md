# Session Log — append-only, newest first

Every session leg lives HERE (moved out of STATUS.md 2026-07-29, audit
remediation 3.3; new legs are PREPENDED below this preamble). Everything in
this file is **history**: counts, statuses and "next" claims were true when
written and are NOT maintained — the current state lives in `docs/STATUS.md`,
defect truth in `docs/BUGS.md`, engine facts in `docs/agent/ENGINE_FACTS.md`.

---

## 2026-08-12 — owner challenge re-grades C46: the phantom-power harm is FORCED-ONLY; the omission is real but no organic route to it exists

Owner, day after the chain close: *"We destroyed the wisps via a command no
normal play could reach. Could our way of destroying the wisps be why we
observed a defect?"* Re-derived from Src the same day, and the challenge
lands — the **fourth** challenge-driven correction, and the second where the
ROUTE was wrong while every cited line was right.

Precision first: the command itself IS reachable — `SetLightTrapMode
("destroy")` is verbatim the player's *Experiment upon them* payload
(`Mystery 11.generated.lua:470-471`), and the destroy branch + the wisps' own
death path (`Fireflies.lua:676-688`, `:533-545`, `:313-321`) genuinely never
touch `el_prod_modifier` — the omission stands. **What normal play cannot
reach is the SEQUENCE the rig performed: free→destroy.** All three modifier
writers are gated on mode `"free"` (`:346`, `:479`, `:692`), so a pre-choice
(`"none"`) trap has never had the modifier written and produces 0 while
holding wisps; `SetLightTrapMode` has exactly two callers in the tree — the
once-only choice's own branches. ⇒ an organic destroy click arrives with
`amount=0` and leaves no phantom; the measured 15,000 stood only because the
rig flipped a consumed-choice save from free to destroy. Player-visible
defect claim WITHDRAWN (source-derived, not play-sampled; re-opens on any
route to free→destroy or a `"none"`-mode write). C46 entry re-graded +
heading tag synced, checklist decision 10 re-framed (wontfix/document now the
natural default; defensive `Change(0)` in our replacement offered), STATE
synced, index regenerated. doccheck GREEN, pushed.

## 2026-08-11 — `corun-pt15` CLOSED by the terminal audit: every leg SUSTAINED, F07's `tested` grant STANDS, EF-051's caveat retired

Terminal audit of the PT-15 mystery chain (prompts consumed at `f289b11` —
the pre-deletion sha; the folder is emptied in this record's own commit).

**Job 1 — the record, audited against the archived log.**
`cp15sitting_Mars.exe-20260811-15.09.30.log` byte-compared over the FULL
206,861 bytes against the on-disk original (`…-6a22b86d.log`) — IDENTICAL, MD5
`491483C73FC1E935A9A3A8945E5C296B` as claimed — and read whole (1,659 lines).
Sweep: **0 `[LUA ERROR]` · 0 `TrackElement` (F99) · 0 `invalid pos` (C45)**;
no `Game saved:`/`Save failed:` anywhere; cheat markers recounted **exactly**
as disclosed (`CheatFill` ×16, `CheatRepair` ×2, `!!! Quick Build !!!` ×4);
every unexplained line matches the notes' attribution (Braze offline telemetry,
the two `LawOfficeDoor` vanilla asset lines at load, one console typo of ours).
Pack organics re-attributed: F78's storm-wedge heal ×2 (1:00:53, 2:28:25),
F02's watchdog (2:42:44) — both entries already carry them.

* **PT-15/F07 — SUSTAINED, and the `tested` grant STANDS.** Recomputed from
  the log: `wisps=95`, `amount=95000` ⇒ ×1000 exactly; 95,000/218,520 = 43.5%
  of grid production; 95,000/2,000 = 47.5 Solar Panels. Four agreeing reads at
  one paused `GameTime()`; R4 held (`CP15PT15` saved, `LOAD OK #2`, identical
  readings; 47,370,762 bytes on disk, MD5 verified today). **Ruling grounds:**
  owner eyes attended the measure moment (Tier A — infopanel screenshot read
  against the log's internal values, UI÷1000 stated), the verdict is quoted
  verbatim on the entry (*"the screen shot is what I see, so it is working"*),
  and everything forced is named IN the grant (the decisive enact was FORCED
  after the organic click died; broken behaviour never observed). The quote is
  transcript-resident, not log-resident — recorded as exposure, not a strike:
  no rule requires log residency, owner rulings are recorded from chat
  project-wide, and the F85 quote's log copy is the same chat relayed through
  `CP15.Note`. Fixed FORWARD in WORKFLOW (new rule 3 below).
* **C39 — SUSTAINED; conclusion re-derived from the logged numbers alone.**
  Both members took the identical `max_workers{percent=50}` cut; only the
  control was compensated (114→268, ×2.35) while the subject sat in a 4-point
  band (127→131) with shifts 12/12/12→6/6/6. Revert restored both
  (`ActiveLaws=nil`, max_workers 12 and 2, perfs 129/124 ≈ baseline). ⇒
  **MISSING UPLIFT**, exactly as recorded; `cand` → confirmed-observed. Both
  `Activate`/`Deactivate` first executions pcall-printed with liveness
  witnesses. Repair options put to the owner (checklist decision 9); heading
  tag updated to agree with the row. Prep's "fired workers do not snap back"
  refutation confirmed in-log (full counts immediately after revert).
* **F85 — verified recorded-and-routed, decided nowhere.** Three negative
  witnesses + the structural control (`idQuickSave=nil` against 437 actions,
  `poscontrol=true`, `Platform.cheats=nil` corrected from `false`) all in the
  log at L408/L412. Disposition stays owner decision 5; STATE's stale "rides
  the PT-20 redo" line fixed.
* **F15 — the sitting's ONE integration gap: the entry was never updated.**
  The log supports it (paused immediate Δ=0 at the kill = the batch grant is
  gone; notification 1,500 = 15×100; delayed reading CONTAMINATED, ratio
  banned from quotation) — the audit wrote the 08-11 section and row_status.
  Stays `fixed*`; batch half MEASURED.
* **C46 — sustained as filed: OBSERVED, FORCED mode change, PRE-RELOAD ONLY**
  (one load of `CP15F15` closes the R4 gap — stated on entry + decision 10).
* **EF-051 — CLOSED; the WORKFLOW "never say gone" clause is RETIRED** (dated
  edit). Audit re-checked the working, not the word: untick commit `d03e4ef`
  09:43:57 verified in git; 55−2+2+1=56 re-derived; the corun-batch-1 archive
  quote read at source (*"they rotate out on their own"*); today's re-listing =
  **59 `.sav`, every name matching the sitting's list, 0 of 14 strays, no
  extensionless file** — a free THIRD data point (strays still absent after the
  sitting's own 15:09 launch). All three protected saves MD5-identical
  (`PT-15` `5D0D…C06`, `TEST2H TRAIN` `103B…958`, `PT35FIXTURE` `D721…738`).
  Surviving rules: names-never-counts; the byte-copy/restore signature
  ambiguity. Both methodology findings read correctly, not overstated.
* **EF-052 — sustained with one nit corrected:** conditions said "6 sinkholes";
  the log reads `sinkholes=1` minutes before the probes (6 was day-70).
* **Chain rule 12(B) — WITHDRAWN, premise refuted.** `MassFireflySpawn` is
  called by the mystery itself (`Mystery 11.generated.lua:337-351`, Src
  re-verified by this audit: sinkhole near the 80% Large Water Tank, wait
  `hour == 4`, spawn). Option B was never offered, never used; the 95-wisp
  trapful is the shipped mechanic — F07's "wisp supply as shipped" carries no
  asterisk. Third Src-refutation of a recorded fact in the project's history.

**Job 3 — the ledger.** Recurred vs the standing blocks: **rule-class
"source-derived UI claim briefed without eyes" recurred across chains** (F85's
dead F9-rebind advice → this brief's impossible "TrapRead BEFORE the choice";
now WORKFLOW corun-pt15 rule 2). NEW classes: the **stop-order during an open
time-sensitive gate** (the sitting's own biggest miss — the lost organic wisp
reading; rule 1) and **transcript-only owner verbatims** (one of four quotes
reached the log; rule 3 + CHAIN_METHOD row). Small harness nits recorded in
place: `C39Revert` takes no clock line (pause state at revert unevidenced —
on the entry); SpeedRamp's wrong selector (EF-052, harness-lesson bullet).
**Owner-time honesty:** promised ~45–90 min, actual **~3h10m attended** —
ours to own except the march (the owner playing their own colony; prep had
warned the mystery was far longer than first planned). Rig-side costs: the
lost organic reading, the 400× recommendation overridden by hand, the HUD
silently dropping the march to 1×, three asks for the cheat disclosure.
Owner deviations (extra passenger rocket, all-shifts activation) bought the
C39 reading and are not scored. **Economics, one line: ~3h10m of owner time
bought the campaign's first `tested` grant, two answered candidates (C39 sign,
F85 route), a measured fix half (F15), two new records (C46, EF-052), a second
EF-051 sample, and three organic watch firings.**

**Job 4 — integration.** F15 entry written (the gap above); C39 heading tag
synced; EF-051/EF-052 updated; WORKFLOW "never say gone" retired + 3 new
attended-sitting rules; CHAIN_METHOD +1 row (transcript-only verbatims / the
sitting's correct deferral of the grant ruling); checklist — PT-15 section and
the closed two-ticks block moved WHOLE to `PLAYTEST_ARCHIVE.md`, decisions 9
(C39 repair) and 10 (C46) added, sitting cost stated honestly; STATE rewritten
(chain CLOSED, NEXT = PT-20 redo, owner decisions 4 open). Chain folder
emptied in this commit (pre-deletion sha `f289b11`). doccheck GREEN, pushed.

## 2026-08-11 — `corun-pt15` BUILT and queued (owner order): the PT-15 mystery sitting, with C39 finally observed and F85's Ctrl-F9 check re-routed to ride it

Owner built the PT-15 fixture themselves (*"I setup a basic save for the
PT-15 with the mystery selected"* — `PT-15.savegame.sav`, 45.6 MB, St. Elmo's
Fire picked at new-game, tech deliberately un-cheated) and ordered the next
chain built around it, plus *"anything else you think would go well with it"*
and the C39 law question (*"laws are hidden until you progress down the
chain… either know what branch to focus on or a way to focus it"*).

**Authored: `agent/prompts/corun-pt15/`** — README + `01_OPUS_PREP` (game-
closed: Src-verify every scripted read, park the instruments resurrected from
`e5dca6f`, stage the fixture copy) + `02_OPUS_SITTING` (attended priority
queue: gate/fixture → **F85 Ctrl-F9, 10 s** → **C39 leg** → mystery march at
ultra, owner playing → **PT-15 wisp reading with R4** → F15 rider) +
`03_FABLE_AUDIT` (terminal; folder empty; kickoff = PT-20 redo). Owner eyes
present ⇒ PT-15 can earn `tested` (verbatim-quote rule binds).

**The C39 research that unblocked its leg (Src 2026-08-11, 1.0.7.396349):**
the law's policy `Automation` sits **10th of 11** in the Technology branch
(`Data\PolicyDef.lua:740-747`, SortKey 900) — that is why organic play never
surfaces it. **`LawDefs.Policy_Automation_ServiceAutomation:Activate()` is
the exact call a passed vote executes** (`Legislature:EnactLaw` ends in it,
`Legislature.lua:512-553`; `Activate`/`Deactivate` at
`ClassDef-Factions.generated.lua:1778-1813`, revert restores the policy
default), is not cheat-gated, and is console-reachable — first-execution
discipline binds. Vote-flow alternatives recorded (`g_AllPoliciesVisibleCheat`,
`g_QuickSessionsCheat` — plain GameVars; `CheatEnactAllLaws` is cheat-gated,
retail-dead per F101). **Mystery timing Src-read** (`Mystery 11.generated.
lua:74-78`): `ColonyApprovalPassed` + 10–20 sols uniform; game-time, so ultra
compresses it to 6–12 real minutes.

**Chain-shape calls, stated:** PT-20 redo deliberately NOT folded in (pack-
off run condition does not mix with a mystery sitting mid-flow; it stays the
named next front) — but **F85's Ctrl-F9 check re-routes here** (its only
requirement is a colony; answers the owner's open decision sooner; checklist
note appended without touching the owner's ruling text). `PT-15.savegame.sav`
joins the protected-fixture list (THREE now). The chain's first launch doubles
as **EF-051's post-untick falsifier** (listings scripted into prep + close-
out). D10 stays parked per C39's own warning.

STATE NEXT → corun-pt15 prompt 1. doccheck GREEN, pushed.

## 2026-08-11 — Steam Cloud unticked by the owner; the 14 strays are cleared to the pre-restore baseline

Owner, same day as EF-051's measurement: *"Steam settings done."* With the
game closed, the 14 Steam-restored strays (`CB1STAGE`, `CB2STAGE`, `CORUN0`,
`CORUN1`, `U1STAGE`, `CB2F85`, `CB2PKEY`, `CB2PKEY2`, `CB2UNINSTALL`,
`U1C0PROOF`, `U1C1HEAL`, `U1C2PT35`, `U1C6FORCED`, `U1C6HEALED`) were deleted
— **732 MB** — and the directory re-listed at **55 `.sav` files**, exactly
EF-051's pre-restore baseline, zero strays and zero `U2*` remaining. Both
protected fixtures MD5-verified untouched (`PT35FIXTURE`
`D721329D1EE18604B3D6C89401F74738`; `TEST2H TRAIN`
`103B320A1434513BC8773553096A8958`, mtime 2026-08-03 22:21:48).
⛔ **Recorded as "deleted, listing verified" — NOT "gone".** The untick is a
setting change, not yet a sampled behaviour; the first post-untick launch is
the falsifier (listing still 55 → the WORKFLOW caveat retires; a stray back →
EF-051 needs re-deriving). Checklist top block: both ticks now DONE, the
block stays until that launch listing. EF-051, WORKFLOW and STATE updated.

## 2026-08-11 — `unattended-2` prompt 2 (terminal audit): ALL FOUR VERDICTS SUSTAINED, three nits corrected visibly, the chain closes and its folder is empty

**Audit method, so the floor is checkable:** all three archived logs
byte-compared to their on-disk originals (MD5-identical over the full length),
the 1,009-line run-3 log read WHOLE, the C43 per-probe diff **re-derived by the
audit itself** (87 rows parsed from both logs — exactly one line,
`AnomalyCaveInMap` PASS→SKIP, against a genuine `78/0/9/0` baseline), and every
load-bearing Src citation re-read at
`A:\…\Project Spark\ModTools\Src` rather than trust-carried.

**Sustained, with what each re-derivation found:**
* **F48 `fixed`** — the seven per-track repair lines, both `0 of 17` round-trip
  diffs, the three-way clean-save zero and the boolean flag reads all at their
  quoted values; `Station.lua:1346` carries the misplaced paren verbatim;
  `ResolveMap` is one-argument (`realm.lua:92`); `Tracks.lua:807/:808` exact;
  the shipped pass calls `process(resolve(track), elements)` — the corrected
  paren, nothing else. **No stop-condition breach**: the build commit preceding
  the launch was the chain's design, and no acceptance was failed and shipped.
* **C43 `fixed`** — 0 `[LUA ERROR]` of any kind in run 3; the refusal by name
  exactly twice; the SKIP verbatim; **`CaveInRubble.lua:38`/`:79` re-read: both
  really are `local function`s**, so the dead-stub finding is CONFIRMED and the
  disposal of the two dead stub entries stays an owner call (on the entry, not
  a checklist decision — nothing is blocked on it). "One probe, not two"
  confirmed by the diff itself.
* **F100 `fixed`** — the diff moves the reason string only; the new string
  matches the log's `:159` character for character; `81/81` on all three loads.
* **PT-35 leg A case A COMPLETE** — all six `0 of 14` diffs located at their
  claimed comparisons; populations printed on every read (1 turbine, 144
  upgraded buildings, 3 live upgrade-shaped ids); the turbine zero sampled
  (`researched=1`, truthy number), not an early return.

**Findings — three, none touching a verdict, all corrected visibly:** (1) the
checklist's PT-35 status token still read `unrun` beside its own completion
record — flipped, with a note; the section STAYS (cases B/C are parked in it).
(2) `Tracks.lua:820-822` for the endpoint assignment was carried under a
"Src-verified" stamp in F48's build record; the audit's read puts it at
`:822-824`. (3) `Mod.lua:1556-1562` in C43's build record is one line shy
(`:1557-1563`). Both corrected on the entries; the shipped code comments carry
the same drift and were left as shipped. ⚠️ The class is the standing one —
*recorded facts are claims* — this time as verified-stamped line numbers two
lines off; the substance survived both times.

**Whole-log sweep, run 3:** 0 `[LUA ERROR]` · 0 `TrackElement.lua:805` (F99
stays passive-watch, nothing to route) · 0 `invalid pos with no holder` (C45
unsampled here — 17 healthy tracks, no mutation; the zero is not a negative
result). The `[Braze]` block (6 lines) and the `LawOfficeDoor` pair (2): present
identically in **all 26 archived logs** back to 2026-08-03 — age is the answer.

**Ledger review (Job 3):** the WORKFLOW rule-7 amendment is **approved as
written** — surgical, sits on the failing rule, and the mechanised gate is
proven in both later logs (it STOPPED nothing it shouldn't and stamped the
rehearsal VOID on every verdict line). The `account.dat` non-write is
**endorsed**: a hard-to-reverse write to owner account state to save one human
click — a click the owner then made in minutes — was correctly refused.
EF-050/EF-051 records check out (save dir re-listed by the audit: 69 files, no
`U2*`, both protected files MD5-identical to their recorded values). NEW and
caught-not-committed: the Python CR→newline mangle (recorded upstream; the PS
5.1 encoding rule has a Python sibling). RECURRED and repaired upstream:
batch-2 rule 7. Nothing else in the standing blocks (u1 1–4, b1 1–6, b2 1–9)
was hit. **Economics:** ~13 min machine time for the whole run night + one
audit session; owner cost the kickoff word, one Mod-Manager tick, one sentence.

**Close:** `CHAIN_METHOD.md` +1 row (the declared-VOID rehearsal pattern and
the run-top gate on externally-mutable state). The chain folder's remaining
five files (README, 02_FABLE_AUDIT, 97_U2Common.lua.txt, 98_U2Run.lua.txt,
U2_ARM.ps1.txt) are deleted in this commit — **pre-deletion sha `e5dca6f`**;
the parked instruments survive at
`git show e5dca6f:docs/agent/prompts/unattended-2/97_U2Common.lua.txt` (and
siblings), the way batch-1's and batch-2's do. doccheck GREEN, pushed.
⇒ **NEXT: author the PT-20 redo co-run chain (attended) + the Ctrl-F9/F85
check riding it. It does not exist yet.**

## 2026-08-11 — `unattended-2` prompt 1 REDONE after the owner re-enabled the pack: ALL FOUR ITEMS VERIFIED, and F48's inference became a measurement

Owner, on reading the blocker: *"I haved re enabled the pack, re do your run,
there is no point in doing an audit for a pack off run."* Re-staged, re-armed in
REAL mode, relaunched. **Retail 1.0.7.396349, pack 81/81 active AS READ (the
gate line, not an assumption), three loads, two save+reload round trips, 0
`[LUA ERROR]` in the whole 1,009-line final log.** Log
`docs/archive/u2run3_Mars.exe-20260811-02.01.06.log`. Everything FORCED/staged;
no `tested` granted anywhere.

⭐⭐ **F48 → `fixed`, and the shipped pass did better than the hand-run it had to
reproduce.** The automatic `PostLoadGame` pass repaired **7 of 17 tracks, 0
raised**, and every single one landed on `2 × (n−1)` — the value a linear chain
must hold:

| track | n | connections | target |
|---|---|---|---|
| `#4569` | 4 | 7 → 6 | 6 |
| `#4619` | 23 | 45 → 44 | 44 |
| `#4730` | 43 | 86 → 84 | 84 |
| **`#12454`** | **280** | **559 → 558** | **558** |
| `#12528` | 32 | 63 → 62 | 62 |
| `#12637` | 17 | 34 → 32 | 32 |
| `#13418` | 67 | 133 → 132 | 132 |

`#12454` is PT-37's own track and PT-37's own numbers, reproduced independently
by the shipped code — which was the stated acceptance. But the seven together
say something PT-37 could not: its 559 → 558 was recorded as *"consistent with
removing one stale connection"*, an inference from a single track. **Seven
tracks of five different lengths, two of them shedding two connections rather
than one, all landing exactly on the clean-chain value, is not an inference.**
Nine stale connections removed. The repair **held across BOTH round trips**
(`0 of 17` on the full per-track signature, twice), the one-shot flag was **read
off `UIColony`** rather than inferred from an absence of lines, and the
already-clean save reported **zero three separate ways** — including a direct
call that deliberately ignores the flag, so the zero is honestly sampled rather
than an early return.

✅ **C43 → `fixed`, and the entry's un-counted gap is answered by execution: no
other caller.** `77 PASS / 0 FAIL / 10 SKIP / 0 ERROR` against the retail
baseline's `78 / 0 / 9 / 0`; a per-probe diff of all 87 rows returns **exactly
one line** — the declared `AnomalyCaveInMap` PASS → SKIP. Zero TestKit
`[LUA ERROR]` lines, and the refusal fired by name exactly twice, for exactly
the two names this entry was filed for. Across 60 stub call sites the suite
found no third undeclared target.

✅ **F100 → `fixed`.** The new line is in the boot log verbatim at `:159`,
between `00_Core`'s `authoring error, not a game update` at `:158` and
`NoHomeless: applied` at `:190` — the log no longer contradicts itself, and it
now tells a reader how to tell this apart from the real regression.

✅ **PT-35 leg A case A is COMPLETE, both halves sampled for the first time.**
`0 of 14 readings changed` at every comparison — after each pass call, across
both R4 round trips, and start-to-finish over three loads and six calls.
⭐ `RepairTurbineBuff`'s zero is **no longer trivially forced**: `unattended-1`'s
came from the early return on an unresearched tech and was recorded UNSAMPLED;
here the tech reads researched, so the pass walked its whole body over all three
`Effect_ModifyLabel` entries and its already-buffed guard did the skipping.
⭐ `RepairLeakedUpgradeModifiers` returned 0 with **3 live upgrade-shaped
modifier ids and 144 upgraded buildings** in front of it — *"it does not strip
live state"* is now sampled on a real population instead of an unmeasured one.

⚖️ **EF-051's prediction was written down and then checked, and it held.** The
three saves deleted at 01:28 were all back by **01:57:47** — the owner's own
launch — creation stamps from that minute, original modification dates intact,
plus a fourth artifact Steam had also restored. Two independent launches by two
different people. They have been deleted again; expect them back until the
Steam Cloud tick.

**Statuses flipped honestly, corrections left visible.** The three "BUILT but
BLOCKED" sections written an hour earlier were not rewritten away — each now
carries a note saying what it first claimed and why it changed. ⚠️ One
self-inflicted scare worth recording: a Python read/write on `C43.md` silently
converted a stray `CR` byte into a newline, mangling a line the edit had nothing
to do with. Caught by reading the diff rather than trusting the tool, restored
byte-for-byte. **`Edit`, not a script, for these files — the memory rule about
PS 5.1 mangling no-BOM UTF-8 has a Python sibling.**

Close-out: probes disarmed (`PROBE SWEEP: clean`), all staged saves deleted —
including one Steam had restored between runs, which the listing rule caught —
save directory listed at 69 files with **no `U2*` leftovers**, both protected
files byte-verified (`PT35FIXTURE` `D721329D…`, `TEST2H TRAIN` `103B320A…`),
log archived and `cmp`-verified, both trees clean, doccheck GREEN.
⇒ **NEXT: `02_FABLE_AUDIT.md`, which now has a real run to audit.**

## 2026-08-11 — `unattended-2` prompt 1: all three builds SHIPPED, and the launch that was to verify them found the pack switched off

**Machine time ~9 min across two launches; owner cost the kickoff word. Nothing
verified, and the reason is not a code failure.**

**Job 1 — the three decided builds, all landed, all parse-GREEN** (pack
`3c1ccc8`, TestKit `d8e1fbf`). **F48**: the corrected pass in
`Code/90_SaveSanitizer.lua`, Src-re-derived first (`Station.lua:1346` verbatim,
`ProcessTrackElements` at `Tracks.lua:807`, the endpoint assignment at
`:820-822`). It counts an EFFECT — connection total and duplicate `node_idx`
either side of each call — so a clean save reports a truthful zero; one-shot
behind an `SMRFixPack_*` flag on `UIColony`; the console entry point ignores the
flag on purpose so a direct call can never return a trivially-forced zero.
**C43**: `set_global` may replace a global, never create one; the refusal is
returned as a third result and logged by name; `WithGlobals` defers a SKIP that
applies only when a probe came back empty-handed, so no existing PASS can flip
silently. **F100**: the reason string only.

⭐ **The C43 build turned up a better finding than the noise it was fixing.**
`IsNearDome` and `AddAreaRubble` are **`local function`s** in the shipped source
(`CaveInRubble.lua:79` / `:38`). A file local is unreachable through `_G`, so
those two stubs **never took effect, before or after this change** — the pair of
`[LUA ERROR]` lines was the only thing they ever produced. `AnomalyCaveInMap`
now SKIPs per the owner's decision, applied literally; deleting the dead stubs
would be a *different* repair, so they stay put and stay visible. Also
corrected: there are not "two Wave-5 probes" — there is one probe with two
undeclared names in a single call, which the original log said plainly and
everything downstream read as two. The un-counted gap is counted on the static
side (60 stub call sites across 10 probe files, 6 direct `SetGlobal` calls, 1 in
the core; no third file-local among the engine names) and is honestly UNSAMPLED
on the live side.

**⛔ Job 2 — VOID. The Community Fix Pack is disabled in the owner's Mod
Manager**, left that way by `corun-batch-2`'s leg T on 2026-08-10.
`pack=0/0 active`; the engine's own line reads *"present, but not loaded"*.
Source-proven unscriptable — `AccountStorage`, `SaveAccountStorage`,
`ModsReloadItems` are all `ModEnvBlacklist` keys, and there is no console at the
main menu. `account.dat` was examined and **deliberately not written**: it is a
compressed container holding the owner's settings, and flipping a checkbox is
not worth a hard-to-reverse write to their account state at 1 am. Routed to the
checklist as tick 1.

**Two harness defects, both mine, both fixed and then PROVEN by a second
launch.** (i) `SaveGame`'s `savename` is written **verbatim** — asking for
`U2RT1` produced a file called `U2RT1`, which `LoadGame("U2RT1.savegame.sav")`
could not find, and `err=false` said nothing about it (**EF-050**). Every prior
caller had passed the extension by accident of habit. (ii) The payload had **no
run-condition gate**: `ReadConditions` printed the zero and six more steps ran
anyway. Repaired in `WORKFLOW` surgically — batch-2 rule 7 now binds at the top
of EVERY run and must STOP it, since a gate whose only output is a log line is
not a gate. A declared HARNESS REHEARSAL (`REHEARSAL = true`, stamped in the
banner and on every verdict line as VOID) then drove all 15 steps, three loads
and two save/reload round trips clean.

⭐⭐ **And the close-out caught something nobody had been able to test: STEAM
CLOUD RESTORES DELETED SAVES.** 55 `.sav` files before the first launch, **69**
after the second — **14** staged saves this project had verifiably deleted
(`CB1STAGE`, `CB2STAGE`, `CORUN0`, `CORUN1`, `U1STAGE`, `CB2F85`, `CB2PKEY`,
`CB2PKEY2`, `CB2UNINSTALL`, `U1C0PROOF`, `U1C1HEAL`, `U1C2PT35`, `U1C6FORCED`,
`U1C6HEALED`), each with a creation stamp inside the 01:17:04–01:17:33 launch
window and its original modification date preserved, **all written before
`Mars.exe` started at 01:17:34**. That is Steam's pre-launch sync, and it
**clears two sessions recorded as having failed the save-dir gate**: they had
deleted the files. `agent/facts/EF-051`; the remedy is one owner tick and it is
checklist tick 2. Checklist item 7's parked hypothesis is now closed by
measurement.

**What IS banked, because it needs no pack:** `PT35FIXTURE.savegame.sav` is
**re-confirmed good** on a fresh load — `researched=1 discovered=163` (EF-048's
truthy-non-boolean shape, second sighting), 1 Large / 6 plain / 12 Diffuser
turbines, 144 upgraded buildings, 3 live upgrade-shaped modifier ids across 13
domes. **`APPLICABLE=true` on both halves of PT-35 leg A at last** — the
population that read 0 for `unattended-1` and again for `corun-batch-1`. The
chain's stop condition 3 is not triggered: the fixture is fine, the pack was off.

Whole-log review, both logs: **0 `[LUA ERROR]`**, 0 `TrackElement.lua:805`
(F99), 0 `invalid pos with no holder` (C45). Two `[ResManager Error]` lines for
missing `LawOfficeDoor` animations — reported rather than discounted, and their
age is the answer: identical pairs sit in all 26 archived logs back to
2026-08-03. ⚠️ The rehearsal's 0-error count may NOT be quoted for C43: with the
pack absent every probe FAILs before reaching its stubs, so the two error lines
are absent for the wrong reason.

Statuses unchanged and honest — **F48 stays `directed`, C43 and F100 stay
`filed`**; no `tested` anywhere; every reading FORCED/staged. Logs archived
`u2run1void_*` and `u2run2rehearsal_*`, both `cmp`-verified. Saves deleted and
the directory listed; both protected files byte-verified (`PT35FIXTURE`
`D721329D…`, `TEST2H TRAIN` `103B320A…`). ⇒ **NEXT: the owner ticks the Mod
Manager, and one relaunch takes every reading this chain owes.**

## 2026-08-11 — `unattended-2` BUILT and queued (same session): the decision-drive build batch, two prompts, owner kicks off before bed

Owner order ("Do the unattended build and I will kick that off before I call
it a night"), same session as the decision drive below.
`agent/prompts/unattended-2/` — README + `01_OPUS_RUN` (build F48's corrected
sanitizer pass + C43's `set_global` restriction + F100's reason string, then
ONE launch on a COPY of `PT35FIXTURE.savegame.sav` verifying all of it:
fixture confirm → F100 boot line → PT-35 leg A turbine half with R4 round
trips → F48 staged case-A acceptance incl. do-no-harm zero → C43 suite run)
+ `02_FABLE_AUDIT` (terminal: shipped-diff-vs-entry-vs-Src audit, R4/R7
enforcement, F99/C45 passive-watch greps, folder empty, kickoff line).
Binding: the full harness-rule stack (unattended-1 1–4, batch-1 1–6, batch-2
1–9, R4/R7), EF-047/048/049 read disciplines, Src at the `Project Spark`
path, **PT35FIXTURE and TEST2H TRAIN protected — the fixture is loaded as a
COPY and survives**. Stop conditions: F48 failing its own acceptance reverts
rather than ships; a broken fixture SKIPs leg A but never blocks the builds.
Kickoff: Opus session on `01_OPUS_RUN.md`.

## 2026-08-11 — decision drive, round 5: F48 ships, D07's ruling is recorded, and the decision board is nearly clear

1. **F48 → SHIP** (owner): the block lifts on evidence stronger than the
   criterion asked for (case A better-than-no-op on the owner's own lineage +
   case B's assert measured unreachable). Status `blocked` → `directed`; the
   corrected pass is queued into the next unattended chain, where PT-35 leg
   A's do-no-harm run covers it in the same launch.
2. **D07 → NO DOME PIN** (owner, confirming their 2026-08-10 typed line
   verbatim): the module's deliberate split stands, no code change. Closed
   checklist items 2 AND 8.
3. **DOC_STRUCTURE_REVIEW: R4 + R7 ADOPTED** as binding WORKFLOW rules
   (round-trip step for state-transition claims; effect-evidencing verdicts);
   **R9 + R14 DROPPED**. Disposition note on the report's §3.

⚠️ Count correction: rounds 1–4 said "15 → 7" but the 15 double-counted the
NoHomeless-preflight/F100 pair (one question, two list entries). True board
after round 5: **2 open** — F85 (evidence-gated on the Ctrl-F9 check riding
the PT-20 redo) and the relabel WORDING (owed owner text, unlocks at launch
prep). Eleven distinct decisions were taken across the drive.

⇒ **The queued unattended chain is now: F48 sanitizer build + C43
`set_global` fix + F100 reason-string fix + PT-35 leg A (verifying all of
them in one launch) — then the PT-20 redo co-run (+ the 10-s Ctrl-F9 check).**

## 2026-08-11 — decision drive, round 4: F99 goes to passive watch, the save-folder policy is ratified, and the owner's challenge holds F85 open

1. **F99 → PASSIVE WATCH** (owner): stays `cand`, zero work — every log
   grepped for `:805` (routine), cheat throws out of scope per the F101
   ruling, ONE organic throw reopens it as work. No more sampling ordered.
2. **Save folder → KEEP DELETING + VERIFY** (owner, decision 7 closed): the
   close-out directory listing is the standing gate; Steam-Cloud hypothesis
   parked until a deleted save ever returns.
3. ⚖️ **F85 stays OPEN — the owner challenged the "no quicksave on retail"
   claim, and the challenge is CORRECT as method:** the only sampled fact is
   the bindings screen's missing save row; "Ctrl-F9 does nothing on retail"
   is an inference chain (generated code gates `idQuickSave` under a measured
   `Platform.cheats=false`) that has never been pressed. A source-derived UI
   claim briefed without eyes is the exact failure that produced the dead
   F9-rebind advice this entry already carries. **The 10-second Ctrl-F9
   empirical check now rides the PT-20 redo sitting** and the disposition
   waits on it. Entry and checklist item 5 both carry the challenge verbatim.

F99's record moved to the archive; decision 7 struck in place. Open
decisions: **7**.

## 2026-08-10 (evening) — decision drive, round 3: our own noise gets fixed, the F100 hold lifts, PT-20 redo ordered

1. **C43 → option 2** (owner): `set_global` restricted to names that already
   exist; probes whose stub target is undeclared SKIP with a stated reason.
   Queued into the next unattended chain (suite-verified; the un-counted
   "how many probes do this" gap is in the same leg's scope).
2. **F100: hold LIFTED, reason-string fix ONLY** (owner) — the boot log stops
   crying wolf; the preflight target waits for D12's review. Same chain,
   boot-verified.
3. **PT-20: REDO NOW** (owner, decision 6) — a dedicated redo co-run is
   queued: disable click + FULL RESTART + ~10 min play owner-side, the rest
   rig-side; result supersedes the possibly-mixed-state 98-vs-98.

⇒ The queued unattended chain is now **PT-35 leg A + C43 fix + F100 string
fix** (one game launch verifies all three); the **PT-20 redo co-run** queues
behind it as the next ATTENDED item. Records moved/struck per the archive
rule. Open decisions: **9**.

## 2026-08-10 (evening) — decision drive, round 2: the F11 pair closes and the veto limit is recorded

1. **F11 rider CLOSED on 2-of-3 readings** (owner) — the wrapper's behaviour
   is witnessed; the third reading tests vanilla's own lines and is untakeable
   on this save (`LuxuriousTrains` + no forest track). If it ever becomes
   takeable it is one free ride-along — recorded on the entry, not owed.
2. **F11 priority P1 → P2** (owner) — correct repair, no demonstrated
   producer, no wedge ever seen live. Front matter + INDEX updated.
3. **`SMRFixPack_Disabled` veto limit RECORDED, not coded** (owner) — the
   lever covers only D12/F97-class modules; D03/D07 consult only `IsActive`.
   Notes on both entries + WORKFLOW Co-runs brief rule 9. No code change to
   two shipped `tested` modules for zero player benefit.

All three records + the completed F11 rider moved to `PLAYTEST_ARCHIVE.md`
per the round-1 rule. Open decisions: **12**.

## 2026-08-10 (evening) — decision drive, round 1 (same session as the batch-2 close): three owner calls landed, and looking for Src found it — behind the wrong folder name

**Format: the owner asked for the open decisions three at a time and answered
the first three.** Recorded, struck, and (per the new rule) moved:

1. **F46 `Fix_TrainCargoDumping`: group C → group B** (owner). A
   behaviourally-exact route exists (the `storable_resources` pre-wrapper) and
   is skipped on §3a cost-benefit, so "no route" was the wrong cell. Counts
   5/4/10/3 → **5/5/9/3**; nothing scheduled. `F46.md` +
   `SAVE_SAFETY_REDESIGN.md` §5.4, both annotated.
2. **The C36-adjacent mysteries grep: GO — and it RAN the same hour, CLEAN.**
   `IsDisasterPredicted` has exactly **9 references in the whole Src tree**;
   the only Mysteries hit is `Dream.lua:26` (C36's own site), no `Scenario\`
   tree exists, and every other hit is already on F81's victim list
   (`WaitCurrentDisaster` verified by read). **No other mystery carries the
   gate; nothing new filed.** Recorded on the C36 row.
3. **Archive rule for closed decision bullets: ADOPTED and applied** — seven
   fully-closed records moved whole to `PLAYTEST_ARCHIVE.md` (co-run #1, the
   load-heal withdrawal, the sign-off tiers, the probe-gate record, the
   TestKit-tree hardening, plus F46 and the C36 grep as they closed); the rule
   is in the checklist preamble. Anything on-hold or holding an owed input
   stays live (F100, the relabel wording).

⭐⭐ **THE SIDE FIND: `ModTools\Src` IS on this machine — batch-2 ledger S12 is
CORRECTED.** The Relaunched Steam `installdir` is literally **`Project
Spark`** (`A:\SteamLibrary\steamapps\common\Project Spark\ModTools\Src`), so
every folder-name search missed it, and the old 2018 game's Src-less
`ModTools` folder made the absence look confirmed. Recorded on EF-014 and in
the Co-runs rules. Three loops it unblocked were closed immediately:
- **F85's route refutation upgraded eyes-negative → SOURCE-CONFIRMED**: the
  game's only Quick Save action (`idQuickSave`, `GameCheatShortcuts.lua:1990`,
  `Ctrl-F9`, `ActionBindable`) is a child of the `__condition
  Platform.cheats` node (`:11-17`) — on retail it does not exist to bind,
  list, or fire. The owner's two bindings-screen reads were exactly right.
- **C45's mechanism source-read**: `Colonist:GetStartingPoint`
  (`ColonistTransport.lua:30-37`) logs `invalid pos with no holder` for a
  colonist with no `arriving`/`holder` on an invalid/out-of-bounds position,
  then falls through non-fatally. "Quantum Comet" is the COLONIST's name (the
  entry's rocket guess corrected); the producer state stays open, one line in
  the Src's favor of the C42/F11 desync neighborhood. Stays `cand`.
- The C36 sweep above, which needed the tree.

Open decisions after this round: **15 by the live enumeration** (4 from the
batch-2 sitting · F48, D07-pin, NoHomeless-preflight from batch-1 · relabel
wording, D03/D07 veto, F100-on-hold, F11-P1, F11-close, F99-severity, C43,
DOC_REVIEW from the older layer). Rounds 2+ continue next.

## 2026-08-10 — `corun-batch-2` CLOSED (prompt 3, Fable terminal audit): every leg verdict sustained, five record corrections, one new vanilla candidate, the folder is empty

**The second batched attended co-run chain is complete** — prep (Opus,
unattended) → sitting (Opus, owner at the keyboard) → this audit (Fable). The
chain's files (README, this prompt, the 4 parked sources) survive in git at
**`7110384`** (`git show 7110384:docs/agent/prompts/corun-batch-2/README.md`
etc.); the folder is deleted in this commit.

**Audit verdict (Job 1, every upstream claim vs the archived logs): EVERY
per-leg verdict SUSTAINED.** Both new logs are byte-identical to the on-disk
originals over their FULL length — the first chain with no unarchived tail,
because the sitting archived after process exit — and all three cited logs
`git show`-verify. Cell-by-cell: the keystone's three same-subject reads with
the middle one immediately before the save, thread handle rebuilt across the
load; F85's ordering witness holds in the log's own line order (popup
`1:10:59` → save `1:11:38-39`, techs 50 on both sides); leg Q's two 3-way
break witnesses, sites 2→0, zero `:805` anywhere; **all five `StartBombard`
first-executions carry printed `pcall` results**, plus one PAUSED refusal the
gate caught; leg S's grant before/after (`researched false→1`,
`discovered nil→163`) and the fixture save; leg T's attempt-1 void is real
(`pack=81/81` after the disable) and attempt-2's process is clean with all six
pack-naming lines accounted for. Commit discipline clean: probes deleted,
sweeps present, staged saves dead, `PT35FIXTURE.savegame.sav` named in the
recording commit and on disk (54,424,001 B), `TEST2H TRAIN` MD5
`103B320A…8958` / mtime 2026-08-03 22:21:48 unchanged, both trees clean.
Ledger claims audited too: S10's cited line numbers (2787/2829) are exact;
**S11 re-checked hours after close-out — the deletion HELD**, none of the 15
returned (a datum consistent with the Steam-Cloud hypothesis being wrong, not
a test of it — the owner question stands).

**What the audit caught — five corrections (none flips a verdict), one filing:**

- ⛔ **The "unattributed modal at ~16:02" IS in the log, and it was the
  keystone's own.** `Story bits: Reply selected - I can't say no to a hopeless
  romantic; let's have us some fireworks!` — sitting log line 378, uptime
  0:32:15 ≈ wall 16:02:31: run 1's `AnythingForLove`, answered ~95 s after the
  reload whose read said `g_StoryBitActive=0`. The handoff's "it is in NO log"
  and "it was not the keystone's" are both wrong, and run 1's "it expired
  before the save" story is amended: the bit reached its POPUP phase and was
  still answerable post-reload while the active table read empty — a state
  nothing read, recorded as an open margin note (archived rider + POPUP audit
  §8), touching nothing in run 2's pass.
- ⛔ **Ledger S5 is factually wrong: `PEFFECT` printed.** Five `[mod]` lines at
  0:32:18 (log:379-383) — the def plus 4 children (2 replies/2 outcomes: the
  2-reply bit it was inspecting). "ModLog is not reachable from the console
  sandbox" is refuted by those lines' own prefix. The false record's cause is
  the flush trap the handoff itself discovered: an ABSENCE verdict taken from
  a mid-session read of a lazily-flushed log (→ `facts/EF-047`). The
  witness-discipline recurrence stands — with a printed `pcall` the session
  would have known it ran.
- **Run 1's gap was ~15 m 20 s** (activation 0:15:06 → save 0:30:26), not the
  "~8 minutes" in the card, the commit message and the sitting record below.
  Run 1 stays VOID either way.
- **Prep's "0 defence towers" was NOT inherited** — `cb2confirm` STEP 6 walked
  `DefenceTowerBase` LIVE that morning (0 of a label that is not the class).
  A broken reader replicating its own zero, not a staleness failure; corrected
  on F26. The distinction matters: the archive cross-check rule WORKED — the
  missing guard is live verification of engine names and UI routes.
- **Leg R's "0 engine error lines across the whole log" was true only of
  `[LUA ERROR]`.** One vanilla `[ERROR]` with an 11-frame stack sits at
  1:28:33, between volleys 3 and 4: `Quantum Comet invalid pos with no holder`
  — a departing rocket's colonist-route read (`GenerateDepartures` →
  `CanReachByTrain` → `GetStartingPoint` → `Station.lua:1254`). First-seen in
  any archived log, no pack frame, unreported upstream. **Filed as `C45`**
  (cand, ONE occurrence, bombardment-collateral vs organic NOT established,
  settling = a passive grep of future logs). A/B confounds also annotated on
  F26 (volley 3 hit a different dome; volley 5 ran at speed 1; the same-dome
  same-speed signature 5, 6 → 7 stands).

**Integration.** PT-47 and the keystone + F85 riders moved WHOLE to
`PLAYTEST_ARCHIVE.md` with their verdicts (PT-47's decal-fade and
notification-CLEARING residue recorded THERE as not-owed — no working
instrument and no live line left open); the §3.6 rider stays and is now the
interesting popup half (the one `dont_pause` window); F99's rider records a
4th witnessed zero; C42's rider records that this save cannot sample it;
PT-20 carries the full-restart rule. New facts: `EF-047` (log tail flushes
only at exit — mid-session reads are partial), `EF-048` (four truthy
non-boolean returns; `== true` is a reader defect), `EF-049` (`ListForTag`
witness regression). D13, F85, F99, F21, F26, F35, F101 verified carrying
their verdicts as written by the sitting.

**Ledger delta vs batch-1's 8 (and unattended-1's 8): 14 entries, 3
recurrences.** RECURRING — and a rule that fails twice is a broken rule:
**S4** (engine-name reader defects, the F21 `spent_time` class's third
appearance; repair = Co-runs batch-2 rule 3, every engine name a reader
consumes gets one live read at confirm time); **S5** (mid-chain instrument
without witness discipline — batch-1's rule 3 recurring, compounded by the
flush trap; rules 4 and 6); **S11** (a false "deleted" record for the SAME
four files, second independent session; repair = the save-directory listing
is now part of close-out — WORKFLOW Co-runs — and its first enforced run
held). NEW: S1/S2/S3/S6/S7/S9/S10/S12/S14 → the batch-2 block, rules 1–8.

**Economics, scored per the override rule — the owner made NO scoring ruling
this sitting, so everything is scorable; their three deviations each BOUGHT
evidence (the MDS A/B, the ~1-minute baseline recovery that closed prediction
2, the keybind challenge that refuted F85's route).** ≈75 attended minutes
against 33–36 promised, every overrun minute rig-side and itemised: M1 ~16 vs
6 (no pre-save read; the ~15-minute conversational gap), M2 ~15 vs 5 (~2 min
hunting a keybinding that does not exist), M5 ~12 vs 4 (five volleys including
the owner's A/B — overrun that bought the control), M7 ~10 vs 5 (the restart
nobody knew was required), console ~12 vs 8 (28 lines typed vs 16 budgeted).
⛔ Not claimed: minutes "saved", anywhere; or that the co-run program is
validated — this is the delta, reported.

**`CHAIN_METHOD.md`: deliberately NO new row.** The simplest-first ordering
rule was queued for its first real test and never got one — no course change
happened, no split, no stop condition fired. A 2× overrun with zero legs cut
says nothing about ordering either way. Bank-incrementally did its work (seven
cards written the moment each leg closed; all seven audit-verified against the
logs) — but that is batch-1's lesson already on record, not a new one.

**Owed to the owner — 4 decisions, all already on the checklist (items 5–8):**
F85's third cell · the 4th OFF state + whether PT-20 gets redone · the
save-directory gate + Steam-Cloud hypothesis (now with the audit's
deletion-held datum) · the uncommitted-tree/D07-answer confirmation. **Routed
gaps, none owner-blocking:** §3.6/M3 (TAKEABLE, now the interesting half) ·
decal fade (no instrument on either side) · notification CLEARING · C42
(needs a passage-traffic fixture, not a better poller) · C45 (passive grep of
future logs) · the active=0-but-answerable storybit state (margin note).

## 2026-08-10 — `corun-batch-2` THE ATTENDED SITTING (Opus, owner at the keyboard): all seven legs ran, nine predictions held, and the rig broke in fourteen places

**Logs** `archive/cb2sitting_Mars.exe-20260810-15.30.16.log` (152,783 B, 2,881
lines) + `archive/cb2uninstall_Mars.exe-20260810-17.20.20.log` (6,667 B), both
`git add -f`, both verified byte-identical to the on-disk originals by `cmp`.
Retail 1.0.7.396349, staged `CB2SIT` copy of `TEST2H TRAIN`
(MD5 `103B320A…8958`), map `BlankBigCanyonCMix_09`, sol 333→335, pack 81/81
active as read, **0 `[LUA ERROR]` across both processes**.

**Cost: ≈75 attended minutes against a 33–36 estimate.** Reported as cost, not
as anything else. Every minute of overrun is itemised in the ledger below and
all of it is rig-side. The owner's three deviations each BOUGHT evidence.

### What each leg found

- **F21 ride-along — PASS.** The restamp was WITNESSED on a named subject across
  a real, unforced boarding: `Colonist#2000038450`, `start_wait 239310758 ->
  239344642`, **+33,884 ms**, after 205 polls reading `Waiting`. The fix
  observed doing its work rather than inferred from an average. NOT re-earned as
  `tested`.
- **Leg P (a), the popup keystone — PASS, both predictions.** A storybit's
  popup-carrying thread SURVIVES a save/load (`g_StoryBitActive=1` before and
  after, thread handle rebuilt …ACC4F98→…C596698) **and answering it afterwards
  still applies the outcome** (the reply's named target, an RC Explorer, present
  in the pre-answer save and gone after). The POPUP_CONSEQUENCE_AUDIT §8 item 1
  keystone, answered. ⚠️ **Run 1 was VOID and is recorded, not discarded** — an
  8-minute conversational gap between activation and save with no reading in
  between made its `1 → 0` uninterpretable.
- **Leg P (b), F85 — defect CONFIRMED, route REFUTED, and the entry's own fork
  cannot express it.** A timer-driven save landed **39 s inside the open
  `ShowBreakthroughChoicePopup` modal**; reloading it voided the choice (popup
  gone, techs still 50). But the retail key-bindings screen has **no save action
  at all**, so "rebind Quick Save to F9" is not a route. Third cell ⇒ owner.
- **Leg Q, F99 — zero throws over a genuinely built cell.** Two distinct tracks,
  breaks witnessed three ways each, sites 2→0, no `TrackElement.lua:805`. The
  2×2's last empty cell is filled. Both halves forced ⇒ rate datum only, and
  **weaker than sample 2** (2 sites vs 201), so the bound did not tighten.
- **Leg R, PT-47/F26 — PASS on every sampled check.** Five volleys, all ENDED
  (peaks 5/6/6/7/7, each with its liveness witness), spread reads as a scatter
  from a low camera, dome cracked ("Hoffman #1 - 3 fractures"), notification
  appeared. Decal fade UNSAMPLED.
- **Leg S, PT-35 — `PT35FIXTURE.savegame.sav` BUILT**, the one deliberate
  survivor: FrictionlessComposites researched, one Large Wind Turbine, one
  applied building upgrade (Remote Medic on a Hospital). Unblocks the turbine
  half, UNSAMPLED since 2026-08-04.
- **Leg T, PT-53 E — CLEAN, on the second attempt.** `pack=0/0 active`, zero
  engine errors, zero new log lines after a minute of sim.

### ⭐ The owner's three deviations, all of which bought evidence

1. **Disabling the MDS lasers for volleys 4–5**, unprompted. Turned an
   interception check the brief had written off as UNSAMPLED into a controlled
   A/B: peak in-flight **5, 6, 6 (on) → 7, 7 (off)** — a quantitative
   signature independent of the eyes, agreeing with what the eyes saw.
2. **Pushing back on an abandoned baseline.** The session declined a
   confirmation as "not worth it"; the owner asked whether that meant a re-run
   later. Re-pricing showed the load was already owed to the next leg, so the
   true cost was ~1 minute — and it closed prediction 2's outcome half.
   **The standing "do not pre-decline a cheap confirmation" rule was violated
   and recovered by the owner, not by the session.**
3. **Reading the key-bindings list twice and challenging the instruction** —
   which is what refuted F85's route instead of leaving it assumed.

### ⛔ The ledger — 14 entries, 0 of them the game's fault

Full text in the audit prompt's inbox. The load-bearing ones:

- **Three engine-name reader defects in ONE function** (`CB2.RResidue`):
  `DefenceTowerBase` (the class is `MDSLaser`, and the save carries **23**),
  the `DecRocketSplatter` decal read (returns a non-table), and the dome-crack
  field guess (printed 0/13 while a dome carried 3 fractures). **All three are
  the F21 `spent_time` class, and G1 cannot see any of them** because it only
  resolves the harness's own namespace. ⇒ **prep's "0 defence towers on this
  save" is REFUTED**, and it had been inherited rather than re-read.
- **The brief's console lines could not have executed as written** — four
  `Sleep()`-carrying entry points with no `*r`, and the bare console has no
  thread context. Caught at pre-flight.
- **No UI path exists to load a staged copy** — `Copy-Item` duplicates the
  display name, so every staged save shows as "TEST2H TRAIN" in the load list.
- **The SAVE primitive's liveness witness is dead** — `Savegame.ListForTag`
  returned a non-table on all five saves (`-1 -> -1`); it read 57→58 in
  `unattended-1`. Saves were witnessed by on-disk bytes and by loading them back.
- **A Mod-Manager disable needs a FULL PROCESS RESTART**, and the intermediate
  state is a NEW one: `pack=81/81 active` with the mod's persisted permanent
  ALREADY GONE. **"OFF is three different things" is now four** (D13), and any
  prior uninstall reading taken without a restart measured the wrong state —
  PT-20 is the named case to re-check.
- **Prep's save-directory cleanup did not happen.** `CB1STAGE`, `CORUN0`,
  `CORUN1`, `U1STAGE` — the exact four batch-1's audit ALSO recorded deleting on
  2026-08-05 — were still on disk, with five more. **Two independent sessions
  have now recorded the same deletion falsely.** 15 removed at this close-out
  (~780 MB). ⭐ **Untested hypothesis: Steam Cloud restores saves deleted while
  Steam is running** (`steam_autocloud.vdf` is in that directory).
- **The working tree was dirty at sitting start and prep reported it clean** —
  the F101 decision plus prep's own routing, including an owner-typed D07 answer
  recorded nowhere as a decision. Carried into this commit.

### Open, and deliberately not closed

M3 (the §3.6 sol-change corner) never ran. **One modal popup at ~16:02 is
UNATTRIBUTED** — it blocked the console, the owner had to click it, and it is in
no log; recorded rather than dismissed. Decal fade and the notification's
CLEARING are unsampled. C42 stayed SKIP as prep ruled.

### Close-out

`DISARM GATE: GREEN` · `PROBE SWEEP: clean` · both `Code/` trees swept ·
`metadata.lua` restored no-BOM · **save directory checked, which is P5's whole
point** · `TEST2H TRAIN` MD5 and mtime UNCHANGED · `last_save` still points at
it after five in-run saves, confirming the `save_as_last` discipline
empirically for the first time.


## 2026-08-05 — `corun-batch-2` BUILT and queued (same session, Fable): the never-ran remainder, simplest first by owner design

Owner order ("Ok go ahead and build out our next chain"), same session as the
batch-1 close below. `agent/prompts/corun-batch-2/` — README + 3 prompts
(Opus prep → Opus sitting → Fable audit). Payload, in run order: C42
traversal-WITNESSED read + F21 penalty read (iff prep solves the reader) →
popup trio + F85 → F99's untested cell (2+ tracks, `CheatBreakElement`,
forced both halves) → PT-47 bombardment (`StartBombard` first execution) →
PT-35 turbine FIXTURE build (the one surviving save) → PT-53 E uninstall
half dead last. ⭐ **The ordering is the owner's design input, recorded
verbatim in the README:** simplest first, *"so that if we run into somthing
that requires a course change we don't burn up all our context on the first
or 2nd task"* — composed with reads-first/process-mutations-dead-last, plus
a bank-incrementally rule (each leg's card written the moment it completes).
Prep must resurrect batch-1's corrected parked instruments from git
`530df63` rather than rewrite, archive-cross-check every briefed entry (the
S7 repair), name a subject-finder per moment (S2), and write an estimate
that includes console driving (S6). Excluded on purpose: PT-53's precedence
half (owner design decision, not a test), the dev-gate audit's ~43
candidates, and everything batch-1 already excluded. Kickoff: Opus session
on `01_OPUS_PREP.md`.

## 2026-08-05 — `corun-batch-1` CLOSED (prompt 3, Fable terminal audit): every verdict sustained, one attribution corrected, the owner's override honored, the folder is empty

**The first BATCHED attended co-run chain is complete** — 3 prompts,
self-consuming, prep unattended (Opus) → sitting attended (Opus, owner at the
keyboard) → this audit (Fable). The chain's files (README, this prompt, the 4
parked probe sources) survive in git at **`530df63`**
(`git show 530df63:docs/agent/prompts/corun-batch-1/README.md` etc.); the
folder is deleted in this commit.

**Audit verdict (Job 1, every upstream claim vs the archived log): EVERY
per-leg verdict SUSTAINED.** The archived log is a **byte-faithful prefix** of
the on-disk original (0 of 1286 shared lines differ; the unarchived 18-line
tail is one story bit + a clean exit-code-0 shutdown at uptime 2:18 — the
process idled ~20 min after the last read). Case A's table verifies cell by
cell (`559 → 558`, endpoints/`n`/`node_idx` untouched, 558 again after LOAD OK
#2 — persisted); case B's refusal is real (`8 broken / 8 sites / 1 repair_cgs`
yet `WALK … shadowed=0 missing=0`, the gate printed its refusal and the call
never ran); PT-42's SKIP was re-confirmed live (5 active factions, Last
Transmission not among them, 0 seats); D07's drain reads all match
(70/9/6 → 76/7/18 → 48/0/53 → 37/0/43, seniors 257→267, 0 employed
throughout); both F99 samples carry their completion witnesses (sites 8→0;
underground 926+201=1127 with tracks 20→18 — the merge demonstrably ran);
F101's five throws are all present with full stacks; D12's lines sit at
161-162/185 as cited; `ProcessTrackElements`' first execution printed its
`pcall` (`ok=true result=nil`); `StartBombard` appears nowhere (PT-47 truly
never ran, F26 stays `[NEVER RUN]`). Commit discipline clean: both cited logs
archived and `git show`-verified, all staged/throwaway saves gone from the
save dir, `TEST2H TRAIN` byte-identical (MD5 `103B320A…8958`, mtime 2026-08-03
22:21:48), both repos' trees clean, no probe residue in either `Code/`, no
leg-5 FIXTURE save exists because leg 5 never ran (none is claimed). The §7
aborted-relaunch amendment is corroborated by the second process's 9.9 KB
boot-only log (16:49:31, uncited, nothing ran). No `tested` was granted
anywhere, so the adopted tiers had nothing to demote.

**What the audit caught — one attribution correction, plus hygiene:**

- ⛔ **F101 mechanism (b)'s trigger was misattributed, and the correction is
  visible on the entry, HELP, and the owner's decision item 3.** The record
  said the 2 × `GetSpotNameColor` throws came from *"opening the object
  inspector (`~<expr>`) and moving the mouse"* (the owner's honest live
  recollection). The archived stacks say: `Infopanel.lua(47) OnAction →
  ToggleSpotVisibility → EditorShowSpots (GedGameObjectEditor.lua:104)` — an
  **infopanel spot-visibility dev button**, same surface class as the
  Meteor-Hit mechanism — and the session's one real GedInspector open
  (1:45:12–1:45:32) was **clean**, and came *after* both throws. The defect
  stands measured; the `~<expr>` claim is demoted to a static lead beside
  `!`/`ShowMe`. The truncated stack quote on the entry had hidden exactly the
  frames that contradicted the story.
- Ledger S4 overcounts: "PREDICTION 10 FALSIFIED" printed **twice** (0:14:54
  with 9 subjects, 0:23:05 with 7), not three times. The lesson stands.
- F21's "all trains `spent_time=nil`" was 4 of 8 trains sampled, all nil; the
  penalty half stays UNMEASURED either way.
- Two organic pack healings the sitting's own log review missed, now on their
  entries: **F78** storm-wedge heal at 1:01:55 (11 strays removed) and
  **F81** rains re-roll at 0:28:41 — with F02's watchdog at 0:13:49, all
  three 2026-08-03 organics fired again in one sitting.
- FYI, routed not cleaned: the game wrote its own `Autosave Sol 351/356`
  during the sitting window — rolling autosaves of the *staged lineage*, in
  the owner's save list; they rotate out on their own but predate nothing.

**Economics, scored per the owner's override (§8, their words: the detour was
their deliberate deviation and is not counted against the run).** Wall clock:
one process, uptime 1:58:42 at the close-out flush, 8 loads, save lineage
`CB1STAGE → CB1CASEA → F99UG`, ~2 h of owner time against a ~24-minute
promise. **Not scored:** the F99 hunt across both maps, the dev-cheat
exploration and its two static audits, the aborted restart — the
owner-directed block, which also produced the sitting's best finds (`F101`,
both F99 samples, the D07 staleness catch). **Scored, the rig's own miss:**
M1 budgeted 3 min, consumed ~25 — prep's measured fixture had evaporated by
sitting time and no instrument could find M1's subject (ledger S2 compounds
it). Both now bind as Co-runs rules (fixture re-confirm at sitting time;
subject-finder instrument per moment). ⛔ Not claimed: that the sitting came
in cheap, or that minutes were "saved" — the correct statement is that the
owner declined to have their own deviation counted, a scoping decision.

**Unforeseen-issues delta vs unattended-1's ledger (8 entries then, 8 now):**
2 recurrences — S1 (wrong-map aim, prep's P2 family; caught by the G1
pre-flight, the guardrail's second earn) and S7 ("recorded facts are claims
too", which recurred DESPITE being a standing rule: D07's entry sat 5 days
stale against PLAYTEST_ARCHIVE, prep inherited it, the brief repeated it to
the owner twice, the owner corrected it from memory — a guardrail that failed
twice, repaired as the new archive cross-check rule). 6 NEW, all attended-only
classes the unattended ledger could not see: a measure moment with no
subject-finder (S2); a no-BOM parked `.ps1` (S3, the BOM defect's mirror
image); mid-chain instruments without witness discipline (S4's
snapshot-FALSIFIED prints, S5's untyped `SelectedObj` capture — G2 applied to
legs but not to the day's own tooling); and the structural one, S6: **the rig
has no input path into a running game**, so the owner typed every console
line and the measure-moments model undercounts every attended sitting. S8:
two static audits produced four false-positive classes; only 2 of ~45
candidates were source-verified and only those filed. All routed into
WORKFLOW "Co-runs" (6 new attended-brief rules) and one CHAIN_METHOD row (an
attended brief is a priority queue, not a schedule; separate owner deviation
from rig misses before scoring; only the owner may rule their own time out).

**Owed to the owner — decisions only, all on the checklist:** F48 ship/hold
(case A better-than-no-op + case B unreachable-by-meteor is a STRONGER answer
than the criterion anticipated, but it is not the answer as written — routed,
not taken) · D07 forced-residence vs forced-dome · F101 severity (with the
corrected mechanism description) · D12 preflight fix. **Routed gaps, none
owner-blocking:** PT-47/M5/M6/M7 (never ran; M7 needs owner hands) · C42
within-session (now known to need a traversal WITNESS, not traffic) · F21
penalty half (reader gap, `spent_time` nil) · F99's untested cell
(repair-path × multi-track merge; instrument on the entry) · F101's third
instance (`!` → `ShowMe`, static only) · the dev-gate audit's ~43 unread
candidates · PT-35's turbine fixture (still a fixture request; re-confirmed
absent on every load).

## 2026-08-04 — `corun-batch-1` BUILT and queued (same session, Fable): the first batched co-run sitting, three prompts, owner sits once

Owner order ("Go ahead and build them out"), same session as the
unattended-1 close below. `agent/prompts/corun-batch-1/` — README +
`01_OPUS_PREP` (unattended: fixture confirms on a staged copy, rig-terms
re-derivation from the entries, parked probes, the measure-moments brief
with per-moment tiers and minutes) + `02_OPUS_SITTING` (the attended batch:
PT-37 as the F48 DECIDER · PT-47 · PT-42 fixture-gated on Last Transmission ·
PT-53 E with its uninstall half DEAD LAST · F21/C42/popup-trio ride-alongs ·
optional PT-35 turbine-fixture build, ~3–5 owner min) + `03_FABLE_AUDIT`
(terminal; audits `tested` grants against named Tier-A moments per the
adopted tiers). Unattended-1's five guardrails bind by rule; both `[NEVER
RUN]` instruments the sitting executes (`StartBombard`,
`ProcessTrackElements`) get prep-time Src-verification plus first-execution
discipline — leg E's broken-recipe lesson applied forward. Estimated owner
cost: one sitting, 15–25 attended minutes, exact minutes named per moment in
prompt 1's brief. Kickoff: Opus on `01_OPUS_PREP.md`; the sitting runs only
when the owner sits.

## 2026-08-04 — `unattended-1` CLOSED (prompt 3, Fable terminal audit): every verdict sustained, the owner's three answers integrated, the folder is empty

**The first fully unattended batch is complete** — 3 prompts, self-consuming,
run entirely under the owner's Opus-executes/Fable-audits rule. The chain's
files (README, this prompt, the 8 parked probe sources with their mid-run
rewrite headers) survive in git at `a433e42`
(`git show a433e42:docs/agent/prompts/unattended-1/README.md` etc.); the
folder is deleted in this commit.

**Audit verdict (Job 1, every upstream "done" treated as a claim): EVERY
per-leg verdict SUSTAINED against its archived log.** Leg C's four organic
repairs re-verified line-by-line (four distinct elements, each break witnessed
`broken=true sites=1 repair_cgs=1`, completion transitions real, no cheat call
in the log, zero `:805`); the SAVE-primitive proof reads exactly as promoted
(57→58 listed, load-back live, pack 81/81, 0.60 s off the log's own `Lua`
markers — EF-045's instrument); the C42 mechanism trace re-derived
independently against ModTools Src and HOLDS, all seven links; leg E's row
flips carried by real evidence including the two-sided `table.copy` control;
the one `[LUA ERROR]` in all 11 logs is cycle 6's forced C34 throw, inside its
marked window, attributed (`TerraformingDisasters.lua:411`,
`UpdateRainsThreads` — prompt 1's prediction right in kind, wrong in every
specific). Commit discipline clean: `PROBE SWEEP:` on all 7 recording commits,
no probe leftovers in either repo, all 11 cited logs actually committed, all
six U1 throwaway saves deleted, `TEST2H TRAIN` byte-identical (55,667,524 B,
2026-08-03 22:21:48).

**What the audit caught — hygiene, no verdict moved:** F99.md's leg-B heading
still carried the withdrawn "rider is discharged" claim (corrected, visibly);
"9 logs archived" was a miscount for 11 (7 good + 4 void); the C42 rider's
"`0` refutes outright" line predated the condition-sampled lesson (corrected);
ledger I5 conflates leg E's two void runs; **and `CORUN1.savegame.sav` sat in
the saves folder beside the ledger's `CORUN0`** — both byte-identical staged
copies of `TEST2H TRAIN` from the closed corun-rig chain, both now deleted
agent-side (routed gap 5, widened by one and discharged).

**Verdicts as they stand:** SAVE primitive PROVEN and in the envelope · leg
D1 nothing-fired/nothing-repeated (H1/H3 unsampled) · leg D2 PASSES all three
conditions at MECHANISM ceiling (H5/H6 forced, H1 unsampled — rocketscientist
profile) · leg A do-no-harm half PASSES, turbine half UNSAMPLED (fixture gap:
FrictionlessComposites unresearched, 0 turbines) · leg B rider precondition
never arose (`:805` did not throw), rider stays `unrun` · leg C **0 in 4
witnessed organic completions** — a rate bound with its condition stated, F99
stays `cand`, severity stays the owner's · leg F C42 limit 2 CLOSED, the zero
UNSAMPLED (0 unit entries, post-load) · both `[NEVER RUN]` rows flipped, the
devil row's documented recipe MEASURED BROKEN (34/40 raises) and corrected in
the HELP table.

**Economics of the batch, against the ~90 s/cycle + zero-owner expectation:**
7 good launches ≈ **9 min** machine time (61–97 s/cycle, predictions
~1.5–6 min); **≈ 21 min** including 4 wasted launches and the 8-minute
unarmed stall. Owner cost: **the kickoff word, plus one unprompted mid-run
message** — which caught the stall before the run's own outside bound did,
the single most important datum for the co-run program. Token actuals:
unrecorded. Component costs now in WORKFLOW's envelope (boot 19 s · cold load
10 s · warm load 6 s · save 0.6 s).

**Unforeseen-issues report (the run's second product): 8 entries, 0 the
game's fault, 3 of 7 parse-GREEN Src-verified parked probes wrong on first
run.** All eight are recorded in the recording commits and the rewrite
headers; the four brief-authoring classes (resolution cross-check; ARM GATE +
C11 piping corollary; liveness witness named in the brief; `pcall` always
printed; per-chain facts never in per-process flags) are now **binding in
WORKFLOW Co-runs**. CHAIN_METHOD gains the method lesson: on a run whose
executor self-corrects visibly, the audit floor's yield is certification plus
residue, not rescue — keep the tier, keep the void-log-beside-good-log
practice.

**Owner decisions integrated (their own hand, committed verbatim at
`f477cf4`):** sign-off tiers **ADOPTED** → standing policy in WORKFLOW,
limits kept verbatim; relabel package **adopted as proposal**, wording still
OWED, landed as a launch-prep instruction; F100 **ON HOLD** — not a decision,
stays open and counted. Stale-records sweep: two resolved decision bullets
moved WHOLE to `PLAYTEST_ARCHIVE.md` as a worked example; the general
treatment ROUTED to the owner (the documented rule covers test sections, not
decision bullets).

**Owed to the owner after this chain — decisions only:** F99 severity (the
0-in-4 lands on their existing line as input); whether D1+D2 close Do-first
item 2; the stale-bullet archiving go/no-go; the relabel wording (when launch
prep comes). Routed gaps, none owner-blocking: C42 within-session read · PT-35
turbine-half fixture (a fixture request, not a sitting) · F99 residue rider
still needs a run where `:805` throws · leg C's N widens at ~1 min per 4.

## 2026-08-04 — post-close session (same day, Fable): sweep adopted, doccheck gains a TestKit line, `unattended-1` built and queued

Same session as the chain close below, continuing on owner instructions.

- **Owner GO on the TestKit hardening** → `doccheck.py` prints a
  `TESTKIT TREE:` line every run (report-only, never blocks); verified on
  the clean and planted-file paths.
- **Routing triage written into `WORKFLOW.md`** (unattended / co-run /
  playtest / organic-only); **owner ADOPTED the full-queue sweep** — 17
  checklist items re-tagged with modes.
- ⛔ **Sweep correction, visible on the checklist:** "no verified command
  forces a dust storm" was table-staleness. `CheatDustStorm(storm_type,
  setting)` is UNGATED (`DustStorm.lua:540`, `normal`/`great`/
  `electrostatic`), and a static-charged dust devil is forcible outright
  (`electro_chance=100` descr copy, `DustDevils.lua:138`). Both in the HELP
  verified table as `[NEVER RUN]`. **F90 → co-run STAGEABLE**; PT-27/28
  stop waiting sols for weather.
- **Owner rules recorded** (WORKFLOW + CHAIN_METHOD): unattended work =
  Opus-executes + Fable-audits, batches = full chain with terminal Fable
  audit; terminal reports END with the next-chain kickoff line; mid-chain
  unattended→co-run escalation is an OFFERED inserted prompt before the
  audit (decline → checklist rider).
- ⭐ **`unattended-1` chain BUILT and queued** (`agent/prompts/`, 3
  prompts): PT-35 · F99 residue + no-cheat discriminator (kickoff = the
  owner's "say the word") · re-scoped load-heal sweep · both `[NEVER RUN]`
  executions · C42 ride-along. Known edge binned honestly: programmatic
  `SaveGame` (`Savegame.lua:1071`) is Src-verified, never executed —
  cycle 0 proves it before legs lean on it. Kickoff: Opus session on
  `01_OPUS_PREP.md`.

## 2026-08-04 — corun-rig chain CLOSED (prompt 4, Fable): the audit held, the economics are real at n=1, the tiers are routed, the folder is empty

**The 4-prompt kill-gated chain is complete.** Prompt 4 audited everything
upstream against primary evidence, closed the three owner-named jobs, routed
the tier decision, integrated the spec's surviving content, and deleted the
folder. The founding spec's full text survives in git:
`git show 93088ba:docs/agent/prompts/corun-rig/CORUN_RIG_SPEC.md` (likewise
`CORUN1_BRIEF.md` and the three `97_CoRun1*.lua.txt` harness sources).

**Audit verdict (every "done" upstream treated as a claim):** every sampled
verdict verified against the archived logs — card 1's counters (340/0/0/0),
card 2's TRACE #1–#8, card 3's L2A 29/300 + L2C 20/20 + the run-3 prediction
logged at +18.8 s against cycle 1 at +23.7 s, card 4's tie-break read, all
four `Time (ms)` cycle figures, both engine load lines, and run 3's load
(9,886 ms — §9 said "not re-read"; it was in the log). Forced/organic labels
present and honest throughout; F11's `tested` was correctly NOT granted (2 of
3 readings, close routed). **One number drift found and corrected visibly:**
STATE and C41 said the picker appeared **40/40**; the logs total **52/52**
(20+20+12, all ALIVE). No verdict changed.

**The probe-gate recheck (owner-named job) — the rule STANDS.** Diagnosis
re-verified from `temporary_sweep()` and the hook. The unverified load-path
claim is now SOURCE-verified: `ModDef:LoadCode` executes only
`metadata.lua` `code` entries (`Mod.lua:490-521`). The syntax-error objection
is dead (parse sweep is location-independent, measured in prep); the declined
override measured a hatch's whole value at **0.4 s machine / 0 owner**; the
long-lived-instrument reading holds (`90_Loggers.lua` is the home, said in
WORKFLOW). `--no-verify` accounting: **zero uses** — no override commit
exists, doccheck green, TestKit HEAD untouched through all four launches.
One hardening routed to the owner: a doccheck report-line on a dirty TestKit
tree (nothing checks it today).

**The TestKit orphan (owner-named job) — adjudicated and committed
(`6f4f103` in the TestKit repo).** Verdict: a close-out oversight in the
~5-minute window when the 2026-08-03 play sitting committed the pack repo
only; intent not establishable, no note anywhere claims deferral; the
comment's content is TRUE against the archived log. **Provenance, preserved
here because the investigation file is deleted:** the 5-line comment block in
`Code/96_AutoRunFlag.lua` was written whole at **2026-08-03 23:20:03**
(LastWriteTime = CreationTime, 1,346 bytes), **20 s** after the MarsDebug
session's last log write (23:19:43); the cited log genuinely reads
`---- 87 PASS, 0 FAIL, 0 SKIP, 0 ERROR ----` (archived:
`docs/archive/corun0evidence_MarsDebug.exe-20260803-23.14.05.log`); the
87/0/0 tally identifies the run uniquely (owner's own identification — retail
caps at 78/9, only the attended MarsDebug `[install]` pass reaches 0 SKIP);
the pack repo committed the same result at 23:22:16 (`0dec7f0`) and 23:24:55
(`b1d2c3d`) while the TestKit's HEAD stayed at `ab3111b` (13:25); the later
same-night sessions were different jobs with no reason to touch the TestKit.

**Economics (the owner's actual question), from recorded actuals only.**
A launch cycle costs **~30 s fixed + the payload** (loads stable 9.5–10.0 s
on the 56 MB save across four cold loads; cycles 64 / 80 / 85 / 398 s).
Owner-attended: **~1.5 min (co-run #0) + ~6.5 min (co-run #1, three
launches) ≈ 8 min total, against ~25–30 promised** — the briefs over-promised
~3×, which future briefs should correct rather than bank as savings. Marginal
cost of a ride-along item is ~0 owner and seconds of machine (the F99 read
cost 3 s of a 398 s cycle) — so batching is nearly free and the break-even
against an all-owner attended sitting is at ONE item that doesn't need
continuous eyes. ⭐ **The number that matters most is the RE-RUN cost:** runs
2 and 3 each closed a question run 1 left open for ~85 s / ~64 s of machine
and ~1 / ~0.5 min of owner — under the old regime both were riders waiting
for a future sitting. ⛔ Honest limits: one sitting, one save, one machine —
a data point, not a trend; token actuals were never instrumented (the spec's
60–150k GUESS stays a guess); and the rig buys nothing on eyes-only or
organic-evidence items, by design. Verdict: **yes, the rig buys owner time
back on the classes it covers, and the sitting measured it.**

**Integrated (spec §1–§9 dissolved):** run procedure + cost shape →
`PLAYTEST_HELP.md` "The co-run rig" (EXECUTED-4×); envelope + tier routing +
close-out rules (both-repo `git status`, C11 script-file arming) →
`WORKFLOW.md` "Co-runs"; condition-sampled-negatives rule (C10) +
detected-gates lesson → WORKFLOW leg-design rules; C8 → `EF-045`; DPI
measurement warning → PLAYTEST_HELP console facts (`EF-046`); kill-gated
chain shape → `CHAIN_METHOD.md` §5. Tiers routed on the checklist —
⛔ NOT adopted; `tested` unchanged. Cards stay at
`agent/reports/CORUN1_EVIDENCE_CARDS.md` as the routed decision's exhibit,
transient per the anti-sprawl rule.

## 2026-08-04 — CO-RUN #1, the first payload run: three launches, ~6.5 owner-minutes, three of four payload items settled

⭐⭐ **The rig earned its keep.** corun-rig prompt 3 (Opus) prepped unattended,
ran the sitting, found two gaps in its own run 1, authored run 2 from run 1's
log, and ran that in the same sitting. Owner-attended **~6 min against ~15–20
promised**; whole cycles **398 s** and **85 s**; loads **9,784 / 9,531 ms** by
the engine's own line; **zero** `[LUA ERROR]` in either. Cards:
`agent/reports/CORUN1_EVIDENCE_CARDS.md`. Costs + 4 corrections:
`CORUN_RIG_SPEC.md` §9. Logs: `docs/archive/corun1_*.log`, `corun1b_*.log`.

- ⭐ **F11's cross-map route is SETTLED — route (a).** The entry had it as *"not
  provable from Lua"*; the removal was observed happening, inside the
  `OnTransferToMapDone` bracket, not inferred from a post-hoc `nil`. The
  requested instrument (wrap `OnExitHolder`, print its caller) is **impossible**
  — `debug` is blacklisted — and shared-sequence ordering replaced it.
- ⭐ **F99's last unknown is MEASURED** — `HexGetTrackGridElement` returns the
  hidden element, which is what the seven crashes implied. The entry's "not
  readable from Lua (C binding)" framing was too strong: it is a one-line Lua
  wrapper. Still `cand`, nothing built, reachability untouched.
- ⭐ **C41 got its first measured mechanism** — `GetMousePos` reports
  virtual-desktop coordinates against a window-local `desktop.box` (`x` to 7665
  vs a box ending at 3840), and an out-of-range anchor fires the safe-area
  clamps, pinning the picker far from the cursor. **Run 3 reproduced the
  bottom-right corner box `(2224,1731)-(3840,2160)` to the pixel** against a
  prediction written to the log before any picker opened. ⛔ **The picker
  appeared 52/52** — the OG symptom did not reproduce, so this is mechanism,
  not confirmation. `cand`.
- ⛔ **A doctrine breach, caught by the owner.** Run 2 recorded that corner
  prediction as **REFUTED** when the condition had never been sampled, with a
  confident false reason attached. The project's existing rule (*"absence under
  N cycles is a rate bound, not a refutation"*) is written about **counts** and
  did not catch a **sampling** gap. Owner insisted on closing it properly —
  *"an agent later on can't try to decide that some error is because my mouse
  was at the bottom of the benq"* — and run 3 cost 64 s and ~30 s of their time.
  Generalisation routed to prompt 4 as spec correction **C10**.
- ⚠️ **`C11`: arming edits must be a script FILE.** An inline Python one-liner
  through PowerShell mangled its own quoting, the `metadata.lua` edit silently
  did not happen, and **the game launched unarmed**. Same hazard class the
  project already records for `git commit -m`.
- ⚖️ **F11's pre-wrapper rider took 2 of its 3 readings** (340 holder removals,
  7 trains, 0 wedges, owner-witnessed) and the third is **unavailable on that
  save**. ⛔ `tested` not claimed; close-on-2/3 routed to the owner.
- ⚖️ **The armed-prep override was DECLINED**, replaced by a measurement:
  arming at the sitting costs **0.4 s** and zero owner time, which is the whole
  of what the grant would have bought. **Rule 5 stands.** And prompt 2's "known
  weak spot" in rule 5 — that it pushes syntax errors to the sitting — **does
  not exist**: the parse sweep does not care where the file lives.
- ⚠️ **A real rule-5 cost, found the hard way:** co-run #0's probe source exists
  nowhere, so this session re-authored the harness from `95_AutoRun.lua`.

---

## 2026-08-04 — both of co-run #0's routed items DECIDED by the owner, same day: `C44` filed `wontfix`, and the probe gate resolved by tightening the protocol rather than loosening the tool

**The `LawOfficeDoor` asset error → `C44`, `wontfix`, closed.** The owner's
instruction was specific and it shaped the entry: *"file with a not fix tag and
a reason its probably best so another agent doesn't get distracted by it
again."* So `C44` opens with a **STOP HERE** banner stating that there is no
work and can never be any, above the evidence rather than below it. The evidence
itself got stronger than "not caused by our leg": across all 19 logs on this
machine the correlation is exact — 2 lines in every session that enters a game
map, 0 in every session that does not, always exactly 2 regardless of how many
maps load — and they fire inside the engine's own `Reloading assets from folder
'BinAssets/'` pass, in a MarsDebug session on a **synthetic** map as well as in
campaign ones. So: universal, once per process, save-independent, and not
dependent on a Law Office existing. `LawOffice` is a `DLC/thomas` building with
`entity = "LawOffice"`; the clips belong to its attached `LawOfficeDoor` entity.
Disposition is **forced, not chosen** — it is a missing *binary* asset and this
pack patches Lua at runtime, so no technique in FIX_POLICY §1 reaches it.

**The probe gate → the tool stays absolute; the protocol tightens.** Asked to
choose, the owner asked for the safest option, verbatim: *"I want to do whatever
is safest, I do not want to get back into the situations where armed probes
start giving us false problems or issues."* **No declared-probe hatch was built
in `doccheck.py`** — the rejected options are recorded in prompt 4's notes so
the reasoning survives, but a hatch a hurried session can open without saying so
re-creates 2026-07-31 exactly. Adopted instead, as **`WORKFLOW.md` probe hygiene
rule 5**: *a probe file is present in `Code/` only while its run is actually
happening.* Placing it and running are the same act; deleting it and recording
the answer are the same commit; there is no state in between, so no armed probe
can outlive its sitting. The co-run protocol's "all prep before the owner sits
down" bullet is amended to match — prep commits the probe's **source as text in
the brief**, which is inert by construction because the mod loads only files
listed in `metadata.lua` `code`, all under `Code/`. A slipped sitting now
strands nothing and arms nothing, and the thing that made co-run #0 survivable
(owner free immediately) is no longer load-bearing.

Also flagged to prompt 4 and not resolved here: the TestKit is a **second repo
nothing checks** — doccheck reads its `Code/` for the sweep and the probe count,
but no gate verifies its working tree is clean, so the comment-only
`96_AutoRunFlag.lua` edit from the 2026-08-03 MarsDebug session sat uncommitted
for a day and surfaced only because a co-run happened to run `git status` there.
A co-run touches both repos by construction, so the rig makes this likelier.

## 2026-08-04 — CO-RUN #0, the walking skeleton (corun-rig prompt 2, Opus): the rig's first end-to-end run, kill-gate PASSED WITH CORRECTIONS

The first co-run ever run. Everything was prepped unattended; the owner gave one
GO and watched. **The composite chain (U1) executed end to end on the first
attempt** — staged save copy → Steam launch → TestKit `LoadGame` at the main
menu → colony live → six scripted reads → forced ride-along → flush → `quit()` →
agent reads the log — with **zero relaunch churn**, which §3 named as THE cost
driver the design had to avoid.

**Costs, measured.** Whole cycle **79.9 s** launch to desktop (predicted 5–8
min). Launch → main menu **~2.7 s**; the 56 MB load **9,968 ms** (U2, engine's
own `GetPreciseTicks` line); quit **~1.5 s**. **Owner-attended: ~1.5 min against
the ~10 promised**, and no click was needed at all — no Steam picker interposed
(U3 = NO, by timestamp: the game's log existed 2.2 s after the launch command).
No `LOADERR`, no watchdog, no modal, no `[LUA ERROR]`, no `Assert failed`.
Spec §1's ⚠️-flagged S1/S2/S4/S5/S7 all answered YES and are now PROVEN.

**Five corrections came out of it** (`CORUN_RIG_SPEC.md` §8 C1–C5), and the
first one is the sharpest: **`RealTime()` does not advance across a loading
screen.** The same `LoadGame` call timed **864 ms** on the harness's clock and
**9,968 ms** on the engine's — an 11.5× understatement, because `RealTime` is
per rendered frame and `LoadGame` blocks in `WaitRenderMode` where none run. A
rig that reports its own costs cannot time itself. Filed as `agent/facts/EF-045`.
Also: a freshly loaded save arrives **PAUSED** (C4), which silently voids any
game-time work a scenario schedules; the readiness poll is redundant on the
load path (C3); and `doccheck.py` reds on any `TEMPORARY` marker with no
declared-probe hatch while `WORKFLOW.md` permits one, so **a co-run whose
sitting is not immediate cannot commit its prep** (C5, routed to prompt 4).

**The ride-along half-delivered, and the honest half is the interesting one.**
The F11 Done-timing trace fired, but the pair the script picked was **same-map**,
so `OnTransferToMapDone` never ran and the cross-map routes (a)/(b) are
untouched — the spec's verdict table was conditional and did not say so (C2).
What it *did* settle is the same-map removal path, which the 2026-08-03
correction block had explicitly left unmeasured. Recorded in `F11.md` with its
own limits attached: `#train.units` moved 12 → 4 over 15 s of game time, so the
count delta is not attributable to the abduction, and "the `:1209` route did it"
is an elimination ROUTE claim that a post-hoc read cannot fully close. The
instrument that would close it — wrap `Holder.OnExitHolder` and print its
caller — is named for co-run #1.

**§6 confirm table as read:** 8 trains with 59 riders aboard and a landed
surface `UniversalZeusRocket` (F11 payload GO); 11 depots and 658 stockpiles
(C41 GO); but **0 broken track elements and 0 repair sites** out of 926 track
elements — the hex tie-break and F99 items are gapped and need a staged meteor
break, exactly as §6 predicted. Routed as a gap, not a re-choice of save.

Probe `97_CoRun0.lua`, its metadata line and `CORUN0.savegame.sav` were all
deleted in the recording commit; `TEST2H TRAIN` was never written. Log archived
at `docs/archive/corun0_Mars.exe-20260804-10.51.15.log`. Reported and not filed:
two `[ResManager Error] … Animations/LawOfficeDoor_*.hgacl` lines that fire on
every load of this map and also appear in the owner's own 2026-08-03 campaign
logs — a vanilla missing asset, on the checklist for the owner's call.

## 2026-08-03/04 — f11-f99-review chain closed (terminal prompt, Fable): F11 converted to a pre-wrapper, F99's mechanism settled by reading, two of the second opinion's own claims overturned

The two-prompt second-opinion chain (sealed derivation `28c253f`, outbox
`068c5aa`) was audited and drained; the folder is deleted this commit. What the
terminal audit added on top of prompt 1, sampled against `ModTools\Src`:

- **Seal timing HELD in git** (derivation → outbox → STATE, no F11/F99 edits by
  prompt 1); the attested informational leak (mandatory STATE.md read + `git
  log` subjects) is real and is now a CHAIN_METHOD §3 row with countermeasures.
- **Prompt 1's F11 route claim was itself too strong.** "`OnTransferToMapDone`
  did it" is not provable from Lua — the Msg raise point is inside the C-side
  `TransferToMap`. What IS settled: both candidate routes end in
  `Holder:OnExitHolder` → `table.remove_entry`, the record's "the measurement
  shows it does not drop the holder link" was an over-claim either way, and the
  same-map path stays unmeasured. STATE briefly carried prompt 1's version.
- **Prompt 1's F99 self-reversal conceded too much.** Its outbox called the
  filed clear-and-rebuild route "mechanically correct"; reading refutes it —
  `ProcessTrackElements` returns early on an empty list (`Tracks.lua:808`),
  the `#elements == 1` and invalid-first cases never mutate the array, and
  every `OrderTrackElements` exit from a non-empty input leaves it non-empty
  (`:575-576` seed, `:582` no-clear, `:616-620` restore). So the list was empty
  BEFORE `TrackElement.lua:802`; the drain is `ExpandTrackFromElement:729`'s
  absorb-walk (the broken element is absorbed — only hidden by
  `Track.lua:639`, still in the hex grid — while its repair site keeps
  `params.track_obj`, `:635`). One link stays C-side: the per-hex tie-break.
- **F11 conversion BUILT** (`3a6512f`): §1.4 pre-wrapper, EF-012-pre, apply-once
  verified in 00_Core (non-optional entries never re-apply), `const.Scale.Stat`
  Require dropped, `IsSameMap` added. Declined the `vehicle.units` nil guard —
  `KickUnitsFromHolder` nils `units` before its kick loop, so shipped play runs
  `remove_entry(false, unit)` routinely; the guard would break byte-parity with
  the tested branch. ⛔ NOT `tested`; checklist rider owns earning it back.
- **F99 stays `cand`, nothing built** — §4 no-cheat reachability unproven,
  self-heal caps observed harm; fix shape recorded on the entry so it needs no
  re-derivation. EF-008 misuse in the entry corrected (it is about `assert`;
  these throws unwound to C). Count corrected everywhere to 7.

---

## Evicted from STATE.md 2026-08-03 — the D12 / PT-62 P4/P6 result, recorded and gated elsewhere

Moved out to pay for the MarsDebug complete-coverage line (mechanical rule 8).
The gate itself STAYS on STATE.md, with the owner's "not a release gate" call and
the owed items intact; only the narrative moved. Full record: `agent/bugs/D12.md`.

✅ **D12 — PT-62 P4/P6 PASS 2026-08-03** (attended): dome ran homeless
**23 → 10 → 0**, `overpop true → false`, 0 leaked subjects. ⭐ Owner: a win
needing more testing, ⛔ **NOT a release gate** (opt-in). Status stays `speced`.
Owed: P12/P13/P14 + the split loop counter through a landing. ⚠️ The old loop
check **could not fail** (it counted delivery a flagged dome must receive).

---

## Evicted from STATE.md 2026-08-03 — F76 closure + the docs restructure, both resolved

Moved out of STATE.md by the F11-rider sitting to pay for the F11 result and the
F99 filing (mechanical rule 8 — adding to a 60-line doc means evicting). Both
items below are **resolved**; the only live thread either leaves behind is `C41`,
which stays on STATE.md as a one-liner.

⚖️ **F76 — CLOSED, REFUTED** (QA job 10, owner-routed). Re-verified rather than
inherited: box and mouse are one coordinate space, the forensic box was correct
placement, the load failure did not reproduce, the picker is vanilla. **P1
released.** The unrefuted residue is **not** closed with it — the "icon does not
appear" witness and the out-of-range-mouse lead are **`C41` (cand)**, instrument
`F76MISS`; MOD_DESCRIPTION's F76 note is VOID.

✅ **Docs restructure + standing-prompts redesign COMPLETE 2026-08-03** —
`agent/reports/DOCS_RESTRUCTURE_REPORT.md`, `STANDING_PROMPTS_REDESIGN.md`.

---

## Evicted from STATE.md 2026-08-03 — the checklist redesign, resolved

Held a slot under "Gates and holds" after it stopped being one. **Checklist
REDESIGNED 2026-08-03** (owner-approved at the checkpoint): by-system groups,
Bug/Requirements/Setup format; the pre-redesign snapshot and the old protocol
are in `docs/archive/PLAYTEST_ARCHIVE.md`. Evicted to make room for D12's
free-work door under the 60-line cap (`WORKFLOW.md` mechanical rule 8).

---

## STATUS narrative archived 2026-08-03 (docs-restructure chain)

`docs/STATUS.md` became `docs/agent/STATE.md` — one screen, current only —
on 2026-08-03 (DOC_RESTRUCTURE_SPEC §3c). The WHOLE of the old file is preserved
below, byte for byte and in its own order, including the parts STATE.md
re-states: the archive keeps the record, STATE.md keeps the state. Its counts,
statuses and "next" claims were true when written and are NOT maintained.

# Project Status — read this first in a new session

> ✅✅ **THE PROJECT PROMPT CHAIN IS COMPLETE — 2026-08-03.** All 18 prompt
> files ran and consumed themselves; the final backward QA (chain prompt 12,
> Fable) verified the chain end to end and emptied the folder. **Read
> `docs/reports/CHAIN_QA_REPORT.md` first** — verdict, findings, the doctrine
> re-verification (it HOLDS), the F97/D12/F76 adjudications, the standing-item
> table, and the playtest campaign's ordered top. The documentation-structure
> recommendations the owner requested are `docs/reports/DOC_STRUCTURE_REVIEW.md`
> (recommendations only — owner decides). `docs/reports/BLIND_AUDIT.md` is now
> committed with its informed-examination ANNEX; its seal died with the chain.
> **The owner is free for the playtest campaign** (`PLAYTEST_CHECKLIST.md`;
> first at the keyboard: PT-62's remainder, then the load-heal round-trip
> sweep, then the doctrine C-sitting — QA report §9).
>
> 📁 **QUEUED (2026-08-03, owner-approved): the docs-restructure chain** —
> `docs/prompts/docs-restructure/`, 4 Opus prompts executing the DECIDED
> spec `docs/reports/DOC_RESTRUCTURE_SPEC.md` (agent-optimized doc tree,
> per-entry bugs/, doccheck + pre-commit hook, CLAUDE.md). Needs no
> keyboard; may run concurrently with the campaign. Its prompt 4 emits
> `DOCS_RESTRUCTURE_REPORT.md`, which the owner then feeds to a Fable
> session to REDESIGN the standing prompts against the new structure.
> `FABLE_NEXT_PROMPT.md` was rewritten the same day as a PURE playtest-standby
> prompt and no longer carries the board — chain-owned work found in a
> playtest session is routed to the chain, never started there. The spent
> `F86_NEXT_SESSION_PROMPT.md` and `F86_ADJUDICATION_FOLLOWUP.md` are
> archived. All six research-mod FPKs (incl. the removed fredware mod) are
> archived at `C:\Dev\workshop_fpk_archive\` — workshop subscriptions are no
> longer needed for any planned work.

Rewritten in place every session (structure since 2026-07-29, audit
remediation 3.3). Session legs are append-only in
`docs/archive/SESSION_LOG.md` (newest first); engine facts live in
`docs/agent/ENGINE_FACTS.md`; defect truth lives in `docs/BUGS.md`.

> 🚧 **TWO PROMPTS since 2026-07-31 (owner).** `docs/prompts/FABLE_NEXT_PROMPT.md` is the
> **general** prompt and no longer drives drone work — it may answer drone
> questions but may not start, plan or schedule that work.
> **`docs/prompts/DRONE_PROJECT_PROMPT.md`** owns it: D06, D08, D09, F77, the drone queue
> machinery, the consolidated drone playtest, and the cleanup mod. Reason: the
> drone project grew its own open design decision, its own frozen tests, and
> constraints that do not generalise, and sharing a prompt was degrading both.

⚖️ **F76 — CLOSED, REFUTED (chain-12 QA, job 10, 2026-08-03; owner-routed
adjudication).** The prompt-11 measurements and the source control were
re-verified rather than inherited: box and mouse are one coordinate space
(`XDialog.lua:139` control), the original forensic box was correct placement,
the load failure did not reproduce, and the picker is vanilla. **P1 released.**
The unrefuted residue is **NOT closed with it** — the OG "icon does not appear"
witness and the M5 out-of-range-mouse lead are filed as **`C41` (cand)** with
the `F76MISS` hook as the one-sitting instrument. `MOD_DESCRIPTION`'s F76 draft
note is struck VOID. Full ruling on the F76 entry; summary in
`CHAIN_QA_REPORT.md` §6.

✅ **D12 `Opt_NoHomeless` — ADJUDICATED 2026-08-03 (chain-12 QA, job 9): THE
BUILD STANDS.** All five live-review decisions upheld; the symmetric veto's
D07-independence claim verified independently from code (the veto's subject set
— workforce-age unemployed — is disjoint from D07's cohort subjects by
construction, so order-independence holds whichever wrapper is outermost).
**PT-62's remainder is the only gate left** (P4/P6 on a stable colony, P12
mod-manager uninstall, P13 veto lever) — D12 still claims nothing beyond
`speced` until it runs. Two recommendations recorded: a probe case for the
`ChooseDome` half, and a decision on the pack-wide `SMRFixPack_Disabled` gap
(the console veto is dead for D03/D07). `CHAIN_QA_REPORT.md` §5.

**Counts after chain-12 QA — re-derived by counting: 82 `Code/` files; 110
rows = 98 F + 12 D; ⚠️ C rows 40 → 41 (C41 filed by the F76 adjudication); 87
probes. PROBE SWEEP: clean, both repos.**

**Build state (authoritative counts — stated here and nowhere else):**
`Code/` = **82 files** (72 `Fix_` + 8 `Opt_` + `00_Core` +
`90_SaveSanitizer`) = **81 registered modules, 74 default-active** (the 7
toggle `Opt_` modules are opt-in via Mod Options; `Opt_DroneStatDials` (D09)
registers active but is byte-vanilla until a dial leaves base).
**Re-counted 2026-08-02 by chain prompt 10** — one new module,
`Opt_NoHomeless` (D12), added to prompt 8c's 80/74. It is **opt-in and off by
default, so default-active does NOT move**: the arithmetic is
`81 registered − 7 opt-in-and-off = 74`. ⚠️ The divisor tracks the opt-in
modules that are off, **not** the `optional = true` registrations — there are now
**8** of those and `Opt_DroneStatDials` is the eighth, reporting active at base.
Probes: **87** (86 + `NoHomeless`).
⚠️ **`Opt_NoHomeless` is UNRUN** — its leg is PT-62 and D12 claims no status
beyond `speced`. Prior recount, by
`Select-String` for
`SMRFixPack\.Register\(` over `Code/`, **minus the one false positive that
count has always had to drop: `00_Core.lua`'s own `function
SMRFixPack.Register(id, def)` definition line matches the same pattern.**
Was 74/68; the batch added **five new modules** (`Fix_SaintBlessing`,
`Fix_DustDevilsDescrMap`, `Fix_AstrogeologistExtractors`,
`Fix_SinkholeIndestructible`, `Fix_DustStormUndergroundBreaks`) and **two fixes
that needed no new module** (F91 amended `Fix_TrackSalvageWipe`, F94 landed
inside `Fix_AsteroidLanderAvailable`). Pinned game
build: **1.0.7.396349** (fpk parity proven — ENGINE_FACTS.md). BUGS.md index:
**110 rows** (98 `F` + 12 `D`) **plus 40 `C`** — **re-counted 2026-08-02 by chain
prompt 10**, by counting distinct ids. The row count is unchanged (D12 already had
its row); the `C` count is **+1**: **`C40`** filed by prompt 10's pre-build check —
"Crowded Living" grants +3 `Residence.capacity` gated on the **Ministry of
Culture's live `working` flag**, and every withdrawal **evicts** the tail
residents colony-wide (mechanism verified vs Src end to end; the live gating is
**intended** and advertised on the ministry building, so what is open is the
law's own description and the eviction consequence — harm unproven, nothing
built). ⭐ It came from a **Reddit player's hypothesis** that the routed brief
said to *check, not adopt* — and the player was right about the mechanism. It
decided D12's open question in favour of the narrow reading. The prior figure and
its history follow — was **110 rows** (98 `F` + 12 `D`) **plus 39 `C`**,
**re-counted 2026-08-02 by chain
prompt 9**, by counting. **Module and probe counts were UNCHANGED at 80/74 and 86:
prompt 9 shipped no code.** It filed **F98** (our own `Fix_TechDescriptionBuilding`
is a no-op in retail — re-using a shipped translation id discards the replacement
text at `T()` construction) and **C39** (`Policy_Automation_ServiceAutomation`
cuts `max_workers` by label while its performance compensation keys on class, and
the four Workshops are on the label only). ⚠️ **Counting trap worth knowing:** a
plain `grep -c '^| F'` over the index returns **99**, because the F97 *entry*
contains a rate table whose rows also begin `| F97 |`. Count distinct ids, not
matching lines. The prior figure and its history follow — was
**109 rows** (97 `F` + 12 `D`; **re-counted 2026-08-02 by chain prompt 8c** —
`F=97, D=12, C=38`. Chain prompt 8c filed **F97** (C23 item 1, the dust-devil
spawn gate); the `C` count is unchanged because a promoted candidate keeps its
row. The prior figure, and prompt 7's own recount, follow — was
**108 rows** (96 `F` + 12 `D`; **re-counted 2026-08-02 by chain prompt 7** —
`Select-String` over the index block, not by hand, and not by incrementing:
**F=96, D=12, C=38**. Prompt 7's six §4 packages filed **F91-F96**; the C count
is unchanged because promoted candidates keep their rows. The prior figure and
its history follow, because this line's drift is itself evidence — was
**102 rows** (90 `F` + 12 `D`; **re-counted 2026-08-01 by chain prompt 6** —
`awk` over the index block, not by hand. The "100 (88 F + 12 D)" figure here
had gone stale *twice within the same day*: F89 was filed mid-sitting during
Tier-1 leg 1, and F90 by this session's C04 sweep. The two before it, "98 (87 F
+ 11 D)" and "93", went stale the same way — **this line is the most
drift-prone number in the project; re-derive it, never carry it forward**),
**plus 38 `C` candidate rows** (re-counted 2026-08-02 by chain prompt 6b;
was 11 — the
2026-08-01 bug-list audit filed C12–C31, its same-day packed-source
addendum filed C32–C34, and chain prompt 6 filed **C35-C37** the same day — **C36 was closed the hour it was filed** (Inner Light is a downstream victim of F81(a), not a new defect); C rows
are leads, not defects, and are not counted in the 102. **Two more moved
without changing the count**: C04 is CLOSED and promoted to F90, C32
DOWNGRADED — both keep their rows as history. **2026-08-02, chain prompt 6b:
`C38` filed** (Astrogeologist's extractor bonus misses 2 of 12 buildable
extractors) — that is the +1; and **three moved without changing the count**:
**C18 and C19 CLOSED as declines** (no defect — the label system and the dome
distance term both turned out correctly scoped) and **C21's destruction route
VERIFIED**, promoted to prompt 7 with its soft-lock located but unproven.
**2026-08-02, chain prompt 6c: NOTHING FILED, counts UNCHANGED and
re-derived by `awk` (90 F + 12 D = 102; 38 C).** Four C rows moved without
changing the count: **C27, C28, C29 and C30 all CLOSED — no defect in
Relaunched** (the four SkiRich OG candidates whose mechanisms are present in
current Src, three of them where the code that looked missing is simply written
somewhere other than where the symptom points), and **C26 stays `cand` with a
recorded CANNOT DETERMINE** (the engine ships two savegame heals for exactly
that state but they are new-game-gated, and no producer exists in current Src).
That left **C26 as the only unresolved SkiRich candidate** — and it was closed
the same day on live evidence (below), so ⭐ **ALL FIVE SkiRich OG candidates
are now resolved: four on source, one on measurement.**
**Same day, owner at the keyboard — one more C row closed and one live-evidence
find, counts still unchanged (90 F + 12 D = 102; 38 C):**
**C20 CLOSED `wontfix — no player-visible cost`** — the pause-scan observation
was taken and read **DEFERRED, NOT LOST**: paused, the scan landed with no
`SectorScanned` signal; on unpause the voice-over fired, and `QueueVoice` sits
inside `AddHUDNotification` immediately before the `Msg`. ⭐ Free internal
control in the same scan — `NewAnomalies` appeared *before* the unpause and
`SectorScanned` the instant after, proving the scan executed under pause while
the message did not fire. ⚠️ 6b's "on-screen toast" wording was **corrected**
(it is a `HUDNotificationPreset` on `idOverview` with a voice line, not a popup
card) — it had sent the observer looking for something that does not exist.
✅⭐ **F82's MECHANISM IS MEASURED, NOT JUST TRACED** — the checklist rider ran the same night and passed: **`119999` real ms at 5x and `120001` real ms at 1x** (game ms 600000 vs 120000, exactly 5.000x) against a preset `Expiration = 120000`. Real time constant to **2 ms** across a 5x speed change; no state-cleared notification can do that. **Both legs left the grid unrepaired and the notification vanished anyway**, so the unreported-break half is observed, not inferred, and the P3-vs-P2 call is now decidable on data by prompt 7. ⚠️ The run also corrected a project-wide figure: the fastest **player-reachable** speed is **5x**, not `const.ultraGameSpeed`'s 20x, which is `Platform.debug`-gated — now in `ENGINE_FACTS.md`.
**C26 CLOSED `wontfix` — not reachable on current-build saves.** Two
**independent** colonies (`save_game_id` compared in the log, not assumed),
**347 sols of combined history**, both **founded on the pinned build so the
vendor fixups never ran**: `10 / 0` at sol 288 and `2 / 0` at sol 59 (~50 of
them organic pre-playtest), with **non-zero controls in both**, which is what
makes the zeros readable. ⚠️ A third dump was taken and **discarded** — it
shared `save_game_id` with the 288-sol save, i.e. the same playthrough earlier.
Closed as *not reachable*, **not** as *impossible*; a dirty line on any
current-build save reopens it.
⭐⭐ **F78 and F81(a) were caught occurring ORGANICALLY on TWO INDEPENDENT
COLONIES** during that sitting (log `Mars.exe-20260802-01.31.10`: `:252,:269-272`
and `:300,:315-316`) — a live storm wedge (7 stray meteor objects on the first)
and a live stranded `DisasterMeteorStorm` flag, **both defects on both saves**,
all healed on load. First non-fixture occurrences of either, and the
co-occurrence is what their shared `MeteorStorm` origin predicts. ⭐ It also
means two of three real playthrough saves were, at load, silently unable to
advance **Inner Light** — C36's mechanism observed rather than inferred.
⛔ **Prevalence, NOT prevention — and the figure is 2 of 3 old-pack saves, not
2 of 2.** A fourth load (a third independent colony, young and basic) carried
neither, most likely because it has not had a meteor storm yet; and the load
written under the **current** pack carried neither either. Both are suggestive
and both are recorded on the F78 entry **with their confounds named** — it is a later save
of an already-healed colony, n = 3, no vanilla control, and this fix was never a
prevention. **No "the pack improves vanilla stability" claim is licensed by it**,
least of all in `MOD_DESCRIPTION.md`. **No status flips earned** — both entries
are already `tested`; this is reachability evidence, not new verification.
⚠️ Prompt 6's own handoff note said "35 C"; counting says otherwise — the C
line drifts exactly like the 102 does, so re-derive it too.
**2026-08-02, chain prompt 7 — the §4 decision packages: SIX F-ROWS FILED
(F91-F96), counts re-derived by counting → 96 F + 12 D = 108; 38 C.** All six
are **approved and specced, none built** — ~~the build is chain prompt 8's~~ **→ chain prompt 8b's**, after prompt 8 split under rule 3 (see the 2026-08-02 prompt-8 entry below).
**F91** track-shell leak (from C33; our own F44 path reproduces it),
**F92** Saint blessing label mismatch (C22), **F93** dust-devil descriptor read
from the camera's map (C23 item 2), **F94** asteroid-visit precedence (C24),
**F95** Astrogeologist's short extractor list (C38), **F96** the destructible
St. Elmo sinkhole (C21). Five C rows move to **CLOSED — promoted** (C21, C22,
C24, C33, C38) and **C23 is PARTLY promoted** — its three sub-items got three
different answers. **Two closures without a build:** **F82** is `wontfix —
intent` (a timed event announcement, not a state warning — so its P3-vs-P2
question is void), and **C23 item 3** is declined on shape. **Two owner
decisions are open and are the only things blocking prompt 8 from a full
sweep** — ~~see the outbox in `8_f86_phase4_conversion_batch_opus.md`~~ **both
were DECIDED by the owner the same day: package 0 → CONVERT, C23 item 1 → build
it PROVISIONALLY**.
**2026-08-02, chain prompt 8 — THE WHOLE CONVERSION BATCH IS BUILT; nothing
filed or closed, so counts are unchanged and re-derived: 108 rows = 96 F + 12 D;
38 C.** Eight conversions landed, one commit each — §5.4 group A:
`Fix_SmallLandscapeSites` (`69c02b9`), `Fix_NightShiftWork` (`26f0b57`),
`Fix_GeneForging` (`ab7d432`), `Fix_ShuttleHubOffAvailable` (`388c72a`),
`Fix_UpgradeModifierLeak` (`21990fb`); **package 0**: F29 items 1+3 (`1471533`)
and F57(a) (`8f58f30`). ⭐ **The pack now holds ZERO R3 §1.5 replacements**, so
FIX_POLICY §4's amended R3 line is satisfied by construction rather than by the
owner's exception — and **one more persisted mod field has left the save**
(`SMRFixPack_rocket_fuel_key`, cleared from **existing** saves too, because the
new shape needing no memory does not by itself remove a field an old save already
carries). ⛔ **One conversion was DECLINED under the prompt's stop condition:
`Fix_TrainCargoDumping` stays a §1.5 replacement** (`10cd2b4`) — §5.4's
"verified feasible" route does not exist (`GetTargetAmount` is a **native**
`TaskRequest` metatable method published as a savegame **permanent** through the
mod-blacklisted `PersistGatherPermanents`, across 148 call sites with no key),
and the one route that would work mutates a **persisted property** on a live
object, which §3a ranks below keeping the copy. **§5.4 group counts corrected to
5 / 4 / 10 / 3**; routed to prompt 12 for a second opinion, with two job-7 drift
instances. ⚠️ **THE CONVERSIONS ARE UNRUN** — each carries a written
byte-equivalence argument, but an argument is not an observation; **the leg is
chain prompt 8b's** and no converted module may be called verified before it.
Prompt 8 **split under rule 3**: `8b` carries the seven approved fixes
(F90-F96) + their probes + the one batch leg; `8c` carries **C23 item 1**, split
out on its own scale call (Tier-1-scale work — a 14th §3a site, a sleeping
game-time thread — on a P3 item) and **gated on 8b**, since F93 patches the same
dust-devil subsystem.
⏸️ **2026-08-02, chain prompt 9 — D10 IS PARKED BY THE OWNER, NOTHING BUILT, AND
THE RE-DERIVATION IS WHAT THE SESSION LEAVES BEHIND.** Counts re-derived by
counting: **110 rows = 98 F + 12 D; 39 C**; **modules and probes UNCHANGED at
80 / 74 and 86** (no code shipped). **PROBE SWEEP: clean**, both repos.

The prompt opened to build D10. Gate clear (F86 hold discharged, PT-56 passed),
and the routed **[S36] "the devs squashed unemployment with 1.0" claim was
checked against Src and is FALSE** — `StatusEffect_Unemployed` is still icon-only
with zero stat modifiers (`StatusEffects.lua:73-80`, with `StatusEffect_Shock`
three lines below as the in-file control that the class supports stat damage), so
D10's premise held. The bundled F84/T1 localisation decision then went to the
owner as job 1 requires, and **the answer re-scoped the item instead of answering
the tradeoff**: opt-in confirmed, but the text ships through **our own
`ModItemLocTable`**, and D10 becomes **low-priority, post-release, PARKED — not
owed, not scheduled, not to be reported as outstanding.**

⛔ **THE APPROVED SPEC WAS RE-DERIVED FROM Src BEFORE ANY CODE, AND THREE OF ITS
CLAIMS FAILED.** (a) **"The three vocation Workshops" — there are FOUR**;
`TVStudioWorkshopCCP1` is the same build category and the same `Workshop` parent,
and is **DLC in the original game but base content in Relaunched** (owner), so
every player can build it. (b) **The `upgrade1` citation is false** — none of the
three carries an `upgrade1_id`, so that modifier never applies; the conclusion it
supported survives on **better** evidence (`Workplace:OnModifiableValueChanged`,
`:376-415`, handles `max_workers` in both directions and fires the excess through
`FireWorker`). (c) **"EVERY faction def carries unemployment clauses" — seven of
twenty-nine.** Two facts the spec never had also bind any future build:
**`max_workers` is hard-clamped at 20 while `consumption_amount` is not**, so the
paired dial must clamp its own percent per template or the pairing breaks against
the player at the ceiling (VR lands *exactly* on 20 at +100%); and **raising
capacity without staffing it lowers the Comfort payout**, because performance is
split across the slots and the workshop boost scales on performance.

⭐ **TWO DEFECTS FILED EN ROUTE, NEITHER OF WHICH THE D10 PLAN WOULD HAVE FOUND.**
**F98 — our own:** `Fix_TechDescriptionBuilding` (F25) **is a no-op in retail.**
It re-uses the shipped translation id, and `T(id, text)` in a non-dev build
returns `LocIdToLightUserdata(id)` and discards the literal
(`localization.lua:250-252`), so the assignment writes back the text already
there — in every language, English included. Found by re-checking the precedent
**F84's own entry asked to be re-checked** before its tradeoff was treated as
settled. **F25 demoted in both places and is no longer localisation precedent for
anything.** ⚠️ A 30-second live control is queued (`ModLog(type(T(8821,"ZZZ")))`
→ `userdata` confirms) — nothing should be built on the source reading alone.
**C39:** `Policy_Automation_ServiceAutomation` cuts `max_workers` on the
`ServiceBuildings` **label** (23 templates) while `GetWorkshiftPerformance`'s
compensation keys on `IsKindOf("Service")` — and the **four Workshops are the only
members of that label outside that class**. Tells are a self-contradiction plus
the block's own dev comment saying it *assumes* the two sets coincide. ⚠️ **Sign
NOT determined** and recorded that way; needs a keyboard observation. **Do not
build D10 while C39 is open** — both put a `max_workers` modifier on the same four
buildings and a leg could not attribute a reading to either.

⛔ **F84 IS UN-BUNDLED FROM D10** — the shared-tradeoff premise is void. Every
string D10's T1 needs is an **append**, and an append costs nothing in any
language (`shipped_T .. Untranslated(…)`; `TMeta.__concat` works on the retail
light-userdata form, shipped precedent `Workplace.lua:293`). **F84 half (a) is a
deletion** and concat cannot subtract. Two different questions that looked like
one. F84's user decision is now **taken** (route 3, our own loc tables) and it is
blocked on capability, not on anyone's call.

⭐ **2026-08-02, chain prompt 8c — C23 ITEM 1 IS BUILT AS `F97`
(`Fix_DustDevilSpawnGate`, `b43f1d9`), AND THE §3a COST ITS APPROVAL ACCEPTED DID
NOT MATERIALISE.** Counts re-derived by counting: **109 rows = 97 F + 12 D; 38 C**;
**80 registered modules / 74 default-active**; **86 probes**.
`DustDevils.lua:216` multiplies the wave count by `spawn_chance`, which is a
probability, and the divide truncates — so `count_max` is unreachable below 100%
and the count can be 0 while `count_min` is 1. `DustDevils_VeryHigh_3` is authored
`6..8 @ 50%` and can only ever produce 3 or 4.
⭐⭐ **THE APPROVED SPEC'S ROUTE CLAIM WAS FALSIFIED WHEN IT WAS RE-VERIFIED.** The
entry said *"the only precise route is owning the scheduler body"* and priced it: a
**14th §3a exposed site**, a **mod-owned sleeping game-time thread in every save**, a
§1.5 reconstruction, a version-latched one-shot restart, and a hand-back gate on
uninstall. Src says otherwise — `GetDustDevilsDescr` has **three callers, all inside
that one thread**, and the descriptor read is **1:1 with the count draw** — so §3a
**layer 3** reaches the defect by *substituting* the descriptor rather than mutating
it, the possibility the spec's "shared preset table" reasoning skipped. **Owner
confirmed the route change before any code was written.** Built as a §1.4b
post-wrapper on `OverrideDisasterDescriptor` (**4 callers, one per disaster**, keyed
on `original.class`), deliberately one level below `GetDustDevilsDescr` so it never
contends with **F93**, whose `DataPatch` runner re-installs its own body whenever
that global holds anything else. **Result: no 14th site, no sleeping thread, no
reconstruction, no latch, no restart and therefore no F88 timer re-roll**; existing
saves are reached with no load-time action, and uninstall self-heals within one wave.
The one residual is an **inert plain-data descriptor copy**, marked
`SMRFixPack_spawn_gate`, that carries no function values by construction —
per-site disposition in `SAVE_SAFETY_REDESIGN.md` **§8**.
✅ **PT-61 RUN WITH THE OWNER, SAME DAY — ALL TEN PREDICTIONS MET, F97 IS
`tested`.** Save `d10test1`, `Atmosphere 0`, 29 scored waves. **Vanilla produced
only 3s and 4s over nine waves and never once entered the authored `6..8`; the
fixed half produced 0 or 6-8 over twenty and reached 8 twice** — a value vanilla
cannot compute from that preset. The persisted descriptor copy **survived a save
boundary** and drove the far-side wave correctly; on **uninstall** the colony kept
its dust devils (8 in the carryover wave) and the descriptor reverted to vanilla
numbers on the very next read, **zero `[LUA ERROR]` in either log**. The
`Fix_MeteorFrequency` failure mode (F86 Site 1) could not occur — we own no body
and no thread.
⭐ **Two riders closed for free during the leg.** **F93's live half** (above), and
⭐ **the defect caught on the save's OWN shipped preset with no mod installed** —
post-uninstall, `DustDevils_Low` (authored `count 1..2`) computing `0..1`, two
consecutive waves of nothing. That is **reachability evidence**, which the rest of
the leg deliberately is not.
⚠️ **The RATE question is STILL NOT SETTLED, and PT-61 barely speaks to it** — it
measured `DustDevils_VeryHigh_3`, the *least*-affected played preset (+5% mean).
A per-preset derivation is now on the F97 entry and **job 8 should decide on that
table, not on the leg's averages**. ⚠️ **A claim in the first version of that table — that
`DustDevils_VeryLow` produces zero dust devils always, called there "the intent
argument at its sharpest" — was RETRACTED the same day on the owner's question.**
That preset ships `forbidden = true` and the scheduler returns at
`DustDevils.lua:194-196` before its wave loop, so the zero is a deliberate design
decision, not this defect. It was derived from a targeted grep that omitted the
field that mattered.

**2026-08-02, chain prompt 8b — ALL SEVEN APPROVED FIXES ARE BUILT, one commit
each, with seven probes and the batch leg specced. Nothing filed or closed, so
row counts are unchanged and re-derived: 108 rows = 96 F + 12 D; 38 C.**
**F91** (`a5b9db0`, amendment to `Fix_TrackSalvageWipe` — no new module; the
`tested` module's A/B expectations are written on the entry BEFORE the leg),
**F92** (`eb4c6d6`, `Fix_SaintBlessing`), **F93** (`b22dda5`,
`Fix_DustDevilsDescrMap`), **F94** (`3966fb3`, inside
`Fix_AsteroidLanderAvailable`), **F95** (`125783e`,
`Fix_AstrogeologistExtractors`), **F96** (`08b5d84`,
`Fix_SinkholeIndestructible`), **F90** (`b5628a7`,
`Fix_DustStormUndergroundBreaks`). ⚠️ **Two gameplay changes that a morale or
production reading must account for**: Saints now actually buff Religious
colonists (+10 morale), and an Astrogeologist colony gains 10% on two extractor
types. ⚠️ **F72 LOST AN ADVERTISED PROPERTY** — F94 turned that module's chained
post-wrapper into a §1.4b body copy, because a wrapper cannot filter a false
positive; **the module header, F72's BUGS entry, its heading tag and its index
row were all corrected in the same commit** rather than left advertising the
delegation. ⚠️ **EVERYTHING IN THIS BATCH IS UNRUN** — the leg is **PT-60**,
attended, predictions **P1-P9 written before any run**, and it covers prompt 8's
eight conversions too. Two live halves the probes deliberately do not claim went
to the needs-eyes riders (F90's underground-break distribution, F93's map switch).
✅ **2026-08-02, chain prompt 8b — PT-60 RUN WITH THE OWNER; THE BATCH IS
VERIFIED. `76 PASS, 0 FAIL, 9 SKIP, 0 ERROR` (85 = the probe count), all seven new
probes PASS, and no probe that passed before this batch regressed.** All 15 changes
report **`79/79 active`** with **zero `[LUA ERROR]`**, measured **on the ENABLE
PATH** (pack ticked at the main menu of a running process) — the harder of the two
paths FIX_POLICY §2 requires and the one F87 exists for. Fifteen minutes of
unpaused play produced **no log output at all**: no error, no line naming any new or
converted module. ⭐ **The eight conversions are no longer unrun** — they install
active and behave invisibly, which is what they were argued to do.
**Two fixes are `tested` (state reached BY PLAYING): F92** (10 Saints, organically
present in a 285-sol colony, heal idempotent across a reload) and **F95** (an
ordinary Astrogeologist new game; `1 1 0 0` pack-off → `1 1 1 1` pack-on on one
colony, with two known-paid labels as controls).
**Five are `fixed` with in-play verification on manufactured preconditions: F90,
F91, F96** — and **F93/F94 on probes alone**, their live halves being untakeable
here (see below).
⭐ **F90's DEFECT WAS OBSERVED IN PLAY for the first time** — a built fixture whose
electricity fragment holds 1668 connectors, **all underground**, on the main city's
list: **underground `0 → 15`** during a surface-only storm pack-OFF, **`0` on all 26
samples** pack-ON from the identical fixture and storm, surface still breaking in
both, and the **persisted `connectors` array back at 1668** afterwards. ~70% of the
pack-ON storm was watched from underground, so both defect and repair are
camera-independent.
⛔ **TWO OF OUR OWN DEFECTS WERE FOUND BY THIS LEG AND FIXED** — the `F95` and `F92`
load-time heals were **not idempotent** (`Fix_AstrogeologistExtractors` re-applied
+10% on *every* load, unbounded, because its presence test compared **object
identity** across a save boundary; `Fix_SaintBlessing` re-applied and re-logged
every load). Both repaired and both re-verified. **Neither was visible to source
review or to the probes — only a save/load round trip exposed them**, which is a new
shape for prompt 12's job-7 corpus.
⚠️ **Not claimed:** F90/F91/F96's preconditions were manufactured (a cheat-built
elevator colony, a deliberately-salvaged track, a console-placed Sinkhole), so those
are **fix verification, not reachability evidence** — the source enumerations still
carry R1/R2. ~~**F93 and F94 have no live reading at all**~~ ⭐ **F93's LIVE HALF IS
CLOSED 2026-08-02 (PT-61, chain prompt 8c) — in the rider's STRONG form, and free.**
The owner switched to the underground mid-leg of their own accord; that map read
`MapSettings_DustDevils = "disabled"` while `MainMap` read `DustDevils_VeryHigh_3`,
so unfixed this was the **nil** branch and every wave would have been postponed a
sol at a time. Observed instead: seven consecutive descriptor reads returning the
surface preset with the camera underground, and the wave cadence unbroken at its
compressed 4-hour rhythm (sol 8 h11 → sol 9 h12). **F94 still has no live reading.**
The colony was `Atmosphere 0`, which is why the rider was takeable at all — dust
devils share the `Atmosphere` / `DustStormStop` gate with dust storms
(`TerraformingDisasters.lua:34-52, :69`), so **F90's live rider still needs a
colony below that threshold and stays open**.
**TestKit probes: 86** (85 + chain prompt 8c's one — wave 9,
`58_Probes_Wave9.lua`, TestKit `7733f79`, `DustDevilSpawnGate`; the same commit
adds a `DustDevils` logger, which is not a probe and is not counted).
The 85 was 78 + prompt 8b's 7 (wave 8,
`57_Probes_Wave8.lua`, TestKit `2ef64a4`). The 78 was re-verified 2026-08-01 by
counting `SMRTest.Register(` across the TestKit's nine probe files:
10+20+18+12+7+3+2+6, **excluding the definition line in `00_TestCore.lua`, which
matches the same pattern and is the standing false positive in this count**;
unchanged by the 2026-08-01 teardown of `97_SaveHookProbe` — it was declared,
never registered — and the stale-probe sweep still returns **zero** hits in both
repos. **80 registered
modules** likewise re-verified
(81 `SMRFixPack.Register(` occurrences minus the definition in `00_Core.lua` —
it was 80 minus one before F97, and 75 minus one before prompt 8b's batch).
Counts moved 2026-07-31 with **PHASE 4 COMPLETE** (below).
> ⭐ **2026-07-31 (live sitting) — ALL FOUR DRONE RESEARCH GATES ARE ANSWERED and
> F83 is `tested`.** Nothing on the drone research side is owed. Full leg in
> `docs/archive/SESSION_LOG.md`; the answers live on the **D06 entry** and in
> `docs/reports/DRONE_PRIORITY_SYSTEM.md` §8-§10.
> - **Q1 = HONOURED, both legs** — a band-4 repair AND a band-4 haul were
>   consumed, the second on a cheat-free symmetric pair. The band scheme
>   survived the gate that could have killed it.
> - **Q2 = queues are PERSISTED** — allocated in `TaskRequestHub:Init()` at
>   construction, never on load. Learned by breaking a live save (§8).
> - **Q3** — both data tests settled with exact enumerations (5 life-support
>   producers; 4 food services). **Q4** — defaults are omitted from saves,
>   live-confirmed on both branches.
>
> ⚠️ **But the band scheme picked up TWO constraints that did not exist when it
> was drafted, and NO SIDE HAS BEEN PICKED — that is a design decision owed to a
> fresh session.** §9: uninstall is safe and silent but **lossy**, and the heal
> path **expires** once the map is fully scanned. §10: `DroneControl:RemoveBuilding`
> is bounded by a **file-local pinned at 3**, so every re-registration duplicates
> band-4/5 entries **with the mod installed and working**. The `-1..3` fallback
> now has two independent arguments in its favour.
>
> 🆕 **A NEW ENGINE FACT WITH PACK-WIDE REACH** (ENGINE_FACTS.md): a
> mod-authored closure stored on a **persisted game object** goes into the save,
> **survives uninstall, and keeps running** — measured, with zero errors logged.
> 5 of 6 `= function` sites in `Code/` are cleared (UI windows, class tables);
> **`Fix_MeteorFrequency` is UNRESOLVED**, and **PT-20 now carries a mandatory
> step 5** that names it. "It does not break" is no longer a sufficient PT-20
> pass.
>
> 💡 **THE CLEANUP MOD** (D06 entry) — owner frames it as a **beta response
> channel**. **Not approved to build**; owed with the overhaul, not with launch.
> ⚠️ **Its stated justification was corrected 2026-07-31:** the claim that mods
> get *no save hook at all* is **false** — `OnMsg.SaveGameStart` /
> `SaveGameDone` reach mods (measured; only `PersistSave`/`PersistLoad`/
> `PersistGatherPermanents` are blacklisted). A tear-down-on-save scheme is
> implementable after all. What survives is that no mod can run after its own
> removal, so residue *already inside a player's saves* still needs someone else
> to clean it.

> ⭐ **2026-08-01 — THE BUG-LIST AUDIT RAN (`docs/reports/BUG_LIST_AUDIT.md`,
> game-free, one-off prompt consumed).** Every shipped fix tiered against
> external witnesses: final **16 GOLD / 25 SILVER / 30 BRONZE / 0 HOLD**
> (initial 17/25/29/1; F04 fell to the §9 packed-source read, and F49(a)'s
> brief HOLD was reclassified on owner challenge — it is a high-confidence
> adjudicated R4, which fails HOLD's lacks-confidence definition); **the HOLD
> tier ends the audit EMPTY**, and a **NON-FIX tier (12 items) was formalized
> at the owner's direction** (audit §2.4) so hard we-are-not-fixing-this
> decisions (R4 / tier-I / §4a-barred / owner-declined) never muddy the
> maybe-BRONZEs — checked: nothing in BRONZE belongs there; the latent R3s
> ship deliberately per §4a. **And the tier's one code wrinkle is CLOSED
> (owner direction, same day): the F49(a) no-op guard was STRIPPED from
> `Fix_TrainMinors`** — wrapper + 3 Require entries + the probe's palette
> half (probe retained, cap-only; count stays 78; its PASS text changed —
> expect that one line in the next fingerprint diff). Counts unchanged
> (74 registered / 68 default-active). ✅ **The owed unattended A/B code-gate
> leg RAN CLEAR 2026-08-01** (default config; log
> `Mars.exe-20260801-14.15.08`): `fix pack present: 68/74 fixes active` ·
> `---- 63 PASS, 0 FAIL, 15 SKIP, 0 ERROR ----` · 78 verdict lines · zero
> `[CommunityFixPack]` error/disabled/FAILED lines · the predicted ONE
> fingerprint change (TrainMinors now `train cap recomputed 4->1, 40->2, 0->0`)
> plus the two known RNG lines · documented noise only. **Nothing is owed on
> the harness side.** Full quoted numbers on the F49 entry. Headlines: a native Relaunched fix-modding scene exists and
> independently converges on F01/F04/F71/F74/F78/F81 (fredware's 13-fix "Bug
> Fixes" created 2026-07-31, GromGor, Oxygenus); the Relaunched dev patch-note
> thread witnesses the train/lander/homeless clusters wholesale; **20 gap
> candidates filed as C12–C31** (6 VERIFIED against Src this audit — incl.
> Fhtagn cowards-everyone and two storybits that promise rewards they never
> apply); **`Lua.hpk` extraction: needed by ZERO entries — recommend not
> building it**. Corrections en route: F42's stale index row fixed; F34's
> claimed ChoGGi corroboration falls; F35's witness may out-scope the fix
> (work item); F01's recorded forum-report claim is not re-derivable
> (Paradox forum crawler-blocked). **Owner actions requested (audit §7.1):**
> logged-in Paradox subforum check (F01/F64/F74 reports), Paradox Mods
> browser check (console channel, matters for D13), ~~consider subscribing to
> GromGor's + fredware's mods for source comparison~~ — **DONE same day: the
> owner subscribed, all six FPKs (including fredware's REMOVED "Bug Fixes")
> were extracted and read (audit §9).** Results: **F04 GOLD→BRONZE** (its
> witness fits the newly-filed C32 label-desync better), final verdict
> **16 GOLD / 25 SILVER / 30 BRONZE / 0 HOLD**; C31 resolved (F78-heal, not a
> new mechanism); C04 mechanism confirmed vs Src; C22/C23/C24 VERIFIED vs Src
> (Saint blessing never worked; 3 dust-devil scheduler defects; asteroid-visit
> precedence bug); **C33 filed — whole-track demolition leaks an undeletable
> TrackBase shell AND OUR OWN F44 PATH REPRODUCES IT** (needs an F-row
> decision); C34 filed (stale-active rain state, F81b's sibling). fredware's
> F74 misses refugee rockets (ours is a superset); his disasters fix never
> restarts the wedged scheduler (ours does); nothing in his source explains
> the Workshop removal.

> ✅ **2026-08-01 — CHAIN PROMPT 1 DRAINED (playtest reorg + the §4 amendment +
> the consistency sweep; game-free, prompt consumed).** Five things changed:
> - **`FIX_POLICY.md` §4 is AMENDED AND IN FORCE** — the reachability audit's
>   drafted replacement applied verbatim (intent-first with five hard tells ·
>   per-tier reachability with symmetry of proof · R1-R4/U dispositions ·
>   tested-by-playing · evidence freshness). Authority: the owner's blanket
>   pre-clearance; the blocker died when F49(a)'s guard was stripped. **Every
>   session from here judges fixes by the amended §4, not the old
>   three-sentence rule.** ⚠️ **One decision it activated is OWED and routed to
>   chain prompt 7:** F29 (items 1+3) and F57(a) are R3 latent-by-data shipped
>   as §1.5 replacements — the combination the new R3 bullet makes conditional
>   on an explicit owner decision. Nothing presumed; both entries carry it.
> - **PT-54 is RETIRED UNRUN** — it tested bodies the F86 Tier-1 build deletes
>   and reorders. Triggers C/D/E ride the Tier-1 legs (prompt 4 records them as
>   the retirement made good); **triggers A and B are NOT absorbed** (they test
>   `Fix_DisasterPredictionLeak`, which is in no tier) and were routed to
>   prompt 3 to be written into the build prompt as legs. Full text preserved
>   in `PLAYTEST_ARCHIVE.md` under a RETIRED-UNRUN banner.
> - **The needs-eyes list gained four bug-list-audit riders** (F35 live-label,
>   C32 label-membership, F80 enumeration tap, F82 timing) and lost one: **F74
>   merged into F53(a)**, its question answered twice from outside.
>   **⬇️ THREE REMAIN as of 2026-08-01 evening: the F35 live-label rider was
>   TAKEN AND CLOSED** during the F86 Phase-0 keyboard sitting — exactly the
>   opportunistic capture it was written for. **The live label path works, all
>   three turbine labels including `WindTurbine_Large` (+100% applied, Power
>   doubled on every turbine), from a pre-research save with no reload** — so the
>   audit's suspicion that F35 is aimed one layer too shallow is dead and F35 is
>   the old-save migration failure it was filed as. Evidence and the
>   wrong-tech trap that nearly mis-filed it: BUGS.md F35; prompt 6's job 3 is
>   pre-answered and told not to re-run it. The list is
>   now split by intake, because two of the new rows check whether something we
>   believe is *incomplete*, which is not what the other two tables mean.
> - **`MOD_DESCRIPTION.md`** gained the documented-engine-behaviour paragraph
>   and a conditional, do-not-publish-yet no-precedent claim tied to prompt 4.
> - **The consistency sweep found four divergences** beyond the F42 row the
>   audit had already caught (F18's stale `fixed*`, F86's stale *heading*,
>   D01's missing tag, plus vocabulary drift on F84/F88/F10/D06). All 100 index
>   rows now agree with their heading tags, and the comparison is mechanical.
>   **Counts re-derived from the files, not inherited:** 100 index rows
>   (88 F + 12 D) — the 2026-07-31 "98" had gone stale within its own day.

> ✅ **F86 TIER 1 IS BUILT AND VERIFIED (2026-08-01, chain prompts 4 + 4b) —
> ALL FOUR BUILD UNITS LANDED AND ALL FIVE LEGS HAVE RUN** (owner at the
> keyboard, one game sitting plus the uninstall sitting). Save lineage
> `save_game_id HdmSxGs6kyd0uz6-` (test-2, map BlankBigCanyonCMix_09); logs
> `Mars.exe-20260801-16.42.31` (first load), `-17.11.08` (main sitting),
> `-19.14.11` (uninstall). **F02, F78, F81 and F88 are flipped to `tested` on
> that evidence** (index rows and heading tags both), and C34's rider is
> verified. What shipped:
> - **`Fix_MeteorFrequency` REWRITTEN (§6.2a-A):** layer-3 keyed
>   `GetDisasterWarningTime` wrapper over VANILLA's thread body; the body copy
>   and its heartbeat surface are deleted; the per-load restart (F88's defect)
>   replaced by a one-shot version-latched heal (`SMRFixPack_MeteorLatch`
>   GameVar + new core helper `SMRFixPack.PackVersion()`); watchdog liveness
>   moved onto an additive `OnMsg.MeteorDone` timestamp, threshold/ladder/
>   guards unchanged, restarts recreate vanilla's body.
> - **`Fix_RainsDeadlock` REWRITTEN (§6.2a-B):** the bounded-loop copy is
>   deleted; a layer-2 wrapper on `RainsDisasterActivation` mirrors the
>   collision test BEFORE the call and posts `Msg("RainDisasterEnd")` on the
>   early-return; the version-stamped PostLoadGame migration pass
>   (`SMRFixPack.MigrateRainsState`, `SMRFixPack_loop_version`, id-less
>   entries resolved by unique type) moves every persisted loop onto vanilla's
>   body and **carries the C34 rider** (structure → stale-ACTIVE
>   `FinishRainProcedure` heal → migration; manual fallback for invalid
>   `g_RainDisaster`).
> - **`Fix_DisasterPredictionLeak` rider (§6.2a-C):** the stranded-flag sweep
>   also runs on `OnMsg.NewDay` (the taken mid-session reconcile) — Tier-1 leg
>   4's A/B triggers test it in their changed shape.
> - **`SMRFixPack.StormWedgeHeal` REORDERED (§6.2a-D):** orphan gate at body
>   start and after every Sleep, vanilla-state resets before any mod-name
>   touch, logging last — the pack's one mod-owned GT thread in Tier-1 scope
>   is now §3a gate-compliant.
> - **TestKit probes realigned, count stays 78:** the F02 probe drives the
>   keyed wrapper + `wd.last_seen` watchdog (heartbeat surface is gone); the
>   RainsDeadlock probe drives the collision Msg, the version-stamped
>   migration (incl. the id-less `test 2i` shape) and the C34 heal;
>   FixtureCarry's version-lock warning is RESOLVED (the migration is
>   version-stamped) and `SMRFixPack_MeteorLatch` joins its GameVar list.
> - **F89 filed mid-sitting (2026-08-01, leg 1):** vanilla's `MeteorsDisaster`
>   drain loop wedges the Meteors thread on ORDINARY strikes (F78's class on
>   the singles path, invisible to the storm watchdog); measured live at 192h
>   silence and healed by the F02 watchdog at its threshold — the insurance
>   the spec kept proved itself. Covered, not fixable directly (entry).
>   **Index rows now 101 (89 F + 12 D).**
>
> **What the legs actually read (2026-08-01):**
> - **Leg 1 — cadence + warning timing.** Scheduler gaps 75h, 83h, 72h (plus
>   86.7h around the natural storm), all inside the designed 65–90h roll.
>   Storm-warning timing UNCHANGED, proven three independent ways: probe
>   keyed/unkeyed discrimination; a live `GetDisasterWarningTime` read from a
>   non-Meteors thread returning **2250000** (the tower cap, not the keyed
>   2700000); and the natural storm's UI countdown reading ≈74h. **Both**
>   §6.2a-D heal branches ran live on the reordered body — the release branch
>   on a forced storm and the force-clean branch on the scheduler's own
>   natural storm — with logging last in both, exactly as specced. Storms are
>   2-for-2 wedging in this colony, so F78's repro is robust.
> - **Leg 2 — F88's own repro as its regression test.** `t=216351730` →
>   quicksave → **three loads with zero pack lines** → `t=218608231
>   (+2256501 ms = 75 game hours)`. The meteor arrived on the pre-load
>   deadline; the per-load re-roll is gone.
> - **Leg 3 — rains.** The collision arrived NATURALLY (re-roll posted, rain
>   returned; a second one later), `'normal'` migrated and stamped 1.0.1 with
>   no re-migration on later loads, `toxic` correctly silent per the amended
>   id-less reading (`70e6d0c`), and the C34 stale-ACTIVE plant healed through
>   vanilla `FinishRainProcedure`.
> - **Leg 4 — stranded flags, both halves.** A stranded flag cleared on a
>   NewDay tick with NO reload *and* inside a load block; a genuine live
>   countdown survived both sweeps (reload and sol tick) with its flag intact.
> - **Leg 5 — uninstall (PT-20 method).** With the pack disabled: `Meteors`
>   and `MeteorStorm` threads both `valid=true` on vanilla bodies, **zero
>   lines and zero errors naming any Tier-1 module**, and residue only from
>   the allowed list — `SMRFixPack_MeteorLatch = (absent)` (below budget) and
>   inert `loop_version` fields in vanilla's own `RainsDisasterThreads`. F86
>   **Site 1's harm no longer happens**: removing the pack no longer kills the
>   colony's meteors.
>
> ⚠️ **Two limits leg 5 did NOT clear, recorded rather than glossed:**
> (1) **F86 Site 2 is untouched and still leaks** — the uninstall log carries
> **80** `[LUA ERROR] Opt_DroneOverhaul.lua:96` orphan errors, the same
> `(96)←(190)←sprocall←CommandObject.lua(246)` shape BUGS.md already records
> at 98/session. New this leg: they are confined to the FIRST load and are
> **zero after a save+reload** — the leak self-clears in one load. That site
> is layer-2/Tier-2 work and belongs to chain prompt 5, where its carve-out is
> pre-granted; it is **not** a Tier-1 falsification and did not gate the flips.
> (2) **No meteor cycle was instrumented in the uninstalled state** — the
> meteor logger is a per-session toggle and the game restart cleared it. The
> owner saw a warning with no strike behind it, which is ordinary vanilla F89
> with no watchdog to heal it. The uninstall claim rests on the thread/body
> read and the zero-error log, not on that observation. FixtureCarry also
> reports label modifiers as `NOT INSPECTABLE` — absence there is not evidence
> of absence.
>
> - ~~**Tier 2 still owes** (chain prompt 5): `DroneUnreachableForever`,
>   `TrainWaitTime`, `ArrivalDeaths` (b) + the (a) design pass, **F86 Site 2
>   (`Opt_DroneOverhaul`)**, and the D10/D12 unhold record.~~ **→ BUILT
>   2026-08-01, see the Tier-2 block immediately below.** The §5.4-A
>   conversions are chain prompt 8. Tier 1 verifying does not by itself make
>   the pack uninstall-clean.
>

> ⭐ **F86 TIER 2 IS BUILT AND VERIFIED — 2026-08-01, chain prompts 5 + 5b
> (`88f3154`, `44e6af2`, `6f0cb95`, `ef7d49c`, `e197190`; TestKit `6eb3c0b`,
> `7bfa274`). ✅ PT-58 RAN with the owner at the keyboard and PASSED all seven
> predictions — F86 SITE 2 IS CLOSED.**
>
> **The headline: ZERO `Opt_DroneOverhaul` orphan errors on the uninstalled load,
> where Tier-1's leg 5 read 80** (98 when first measured). Logs
> `Mars.exe-20260801-21.27.58` (pack ON) and `-21.54.16` (pack REMOVED), lineage
> `HdmSxGs6kyd0uz6-` on `BlankBigCanyonCMix_09` — the same save family and map as
> all five Tier-1 legs, so the comparison is like-for-like. **The article carried
> 73 drones in command `Idle` at save time**, the same population that produced
> the 80; a zero is only worth its denominator, and this one has one. Zero
> `[LUA ERROR]` of any kind all session, zero mentions of any other Tier-2
> module, and the uninstall was genuine (zero `[CommunityFixPack]` lines,
> `Unpersist missing permanent` at Lua `0:00:19` — leg 5's errors landed at
> `0:00:26`, inside that window). **Both proven leak sites are now repaired and
> verified.** Full reading: `PLAYTEST_CHECKLIST.md` PT-58.
>
> ⚠️ **What the leg did NOT establish, recorded rather than glossed:**
> **(1) No status flip is earned.** F53, F55 and F21 stay `fixed` — P1-P3 are
> *fixture* results, not live readings; no arrival was watched being re-routed,
> no drone was watched re-trying a written-off building, and the optional train
> re-take had no suitable line. The leg verified **save safety**, which is what
> F86 asked of it; the functional re-tests belong to ordinary playtesting.
> **(2) The `self.command == "Idle"` moonlight gate never fired** — every hub
> read `unclaimed=0` and the module read `moonlighted=0 vetoed=0`, so there was
> no work to take. P5 does not depend on it, but D06 part 2's *functionality* is
> untested; its home is the frozen PT-52, not a save-safety sitting.
> **(3) A clean uninstall here is not a general Tier-3 clearance** — it means no
> accepted-residual module happened to be in an erroring state. Tier 3 stays
> accepted by owner decision.
> **(4) P2's second clause was unmeasurable, not met** — retail has no
> `debug.getinfo`, so `FromFixPack(Colonist.Arrive)` could not read. The build
> question was asked and answered before the run (PT-58's retail-build box), and
> P6's zero answers the same property live.
>
> **All four Tier-2 modules now sit on synchronous seams; none replaces a blocking
> body any more. Per-site dispositions (FIX_POLICY §3a per-site release gate):**
>
> | site | was | now | disposition |
> |---|---|---|---|
> | `Fix_DroneUnreachableForever` | replaced `Drone:ApproachWrapper` (blocks in `DroneApproach`, our code after the call) | pre-wrapper on the **verified-synchronous** `Drone:CleanUnreachables` — `ts > GameTime()` → `ts - max_int` recovers the exact failure time; vanilla's writer and its 5-sol expiry both untouched | **REPAIRED IN-PACK, layer 3. No residue; nothing owed to D13.** |
> | `Fix_TrainWaitTime` | replaced `Colonist:BoardVehicle` (blocks for the whole journey via `PlayPrg`) | wrapper on the **verified-synchronous** `TransportStatistics:AddSpentTime`, keyed `IsKindOf(self,"Station")` — the only Station call site of three, and vanilla's own "the wait is paid" line. Boarding colonist identified by `command_thread == CurrentThread()` | **REPAIRED IN-PACK, layer 3. No residue.** |
> | `Fix_ArrivalDeaths` (a) | inside the replaced `Colonist:Arrive`, in a destructor after a `Sleep`, on an upvalue nothing could change | pre-wrapper on the **verified-synchronous** `Colonist:OnArrival`, which runs after the placement and (on the walking path) before `TransportByFoot` starts. **This is the design pass §6.2 booked as owed — run, and it found a route** | **REPAIRED IN-PACK, layer 3. No residue.** |
> | `Fix_ArrivalDeaths` (b) | same replaced body; destination read into a local at `:1260` before anything else runs | pre-wrapper on `Colonist:Idle` keyed on `self.arriving` — the only issuer of `"Arrive"`. Work before the call, `return orig_idle(...)` with nothing after | **REPAIRED IN-PACK, layer 2. Accepted residual: one inert captured frame — ethos tier 2, named and disclosed. Nothing owed to D13.** |
> | `Opt_DroneOverhaul` — **F86 Site 2** | post-wrapper on `Drone:Idle`, under three `Sleep`s: **80 orphan errors** on the Tier-1 uninstall leg, 98 when first measured | post-wrapper on `Drone:CleanUnreachables` gated `self.command == "Idle"` — vanilla's own last statement in the same fall-through, with **no statement between it and the end of `Idle`**. Beats the layer 2 the spec asked for | **REPAIRED IN-PACK, layer 3. No residue.** Verification = PT-58 P5. |
>
> **Carve-out honoured, not stretched:** the `Opt_DroneOverhaul` move changed the
> hook's call position and nothing else — same trigger condition, same ordering,
> same code — so no drone-design judgement was required and the pre-granted
> clearance covered it exactly. Part 1's `TaskRequestHub:FindTask` wrapper was
> checked in the same pass and is already on a synchronous C-backed seam, so the
> module now has **no capturable frame anywhere**.
>
> **Two records were corrected rather than quietly dropped:** `Opt_DroneOverhaul`'s
> header claimed *"saves made with the module enabled load identically without
> it"* — false, and Site 2 is the counter-example; and F53's entry claimed *"no
> wrapper can run in time"* for F21 — right about `BoardVehicle`, wrong about the
> repair, because it only ever asked whether that one body could be wrapped.
>
> **F21 was DOWNGRADED `tested` → `fixed`** in the same move: PT-43's pass was read
> against a body that no longer ships. PT-58 carries the optional re-take that
> earns the tag back; the probe alone does not.
>
> **`ChooseDome` was deliberately NOT wrapped**, though it is where F53's bad
> fallback is born: eight shipped call sites, only the arrival ones are F53's
> subject, and suppressing the fallback globally would change android spawning and
> the "Abandoned" path — behaviour with no evidence behind it (FIX_POLICY §4), and
> §5.3 requires the narrowest key that separates the sites.
>
> **Probe hygiene:** sweep **CLEAN** (zero `TEMPORARY` hits, both repos) at
> `ef7d49c`. Three probes asserted behaviour the pack no longer replaces and were
> **realigned onto the new seams** before any leg was specced — `ArrivalDeaths`
> and `DroneUnreachableForever` (TestKit `7bfa274`), `TrainWaitTime` (`6eb3c0b`).
>
> ⭐ **ETHOS + RELEASE GATE RESTATED BY THE OWNER 2026-08-01 (authoritative
> text: `FIX_POLICY.md` §3a — any "leave no trace" framing left elsewhere in
> the docs is superseded by it).** Leftovers are an accepted fact of this
> engine — the game's own code spells the mechanism out — so the ethos is
> three-tier: **(1)** leave no trace; **(2)** failing that, leave **inert**
> trace, named and disclosed; **(3)** failing that, leave harmful trace **only
> paired with its remedy**, the D13 cleaner. **The release gate is now
> PER-SITE, not blanket:** every exposed site needs a recorded disposition
> (repaired in-pack, or handed to the cleaner where no layer 3/2 route exists).
> A site without a disposition blocks release; a site with one does not.
> ⛔ **This is not permission to descope — build every reachable repair NOW.**
> A cleaner hand-off counts only *after* the in-pack attempt failed, because
> D13's target list is the OUTPUT of the builds and cannot be designed before
> them. **D13 is a HARD LAUNCH DEPENDENCY: launch waits for it, it does not
> wait for launch.**
>
> ⚠️ **DO NOT TRUST ANY EXPOSED-SET COUNT IN THESE DOCS — including the ones
> in this file.** Every recorded figure is an **open lower bound** ("at least
> 13", "≥13"), it moved 12→13 within a single day with the membership
> corrected *both* ways, the enumeration grep behind it is known blind to
> slot/global/preset assignments, and Tiers 1-2 have since changed the set by
> repairing modules. Several per-module tables still carry a stale **12**
> denominator. **D13 derives the set itself from source and that derivation is
> authoritative**, superseding every number recorded anywhere; it then updates
> all of them (the locations are listed on the D13 entry in `BUGS.md`).

> ✅ **F86 PHASE 0 IS DONE (2026-08-01, owner at the keyboard, one sitting) —
> the two engine measurements that gated the Tier-1 designs are MEASURED, and
> both came back the permissive way.** Log
> `Mars.exe-20260801-14.59.57-6a22b86d.log`; full records in ENGINE_FACTS.
> - **`CreateGameTimeThread` DEFERS** — the body does not run before the creating
>   statement continues. Measured twice, the second form creating the GT thread
>   *from a GT thread* and confirming a live `WaitMsg` receipt (the actual vanilla
>   shape), so the answer is not an inference off the console-context form.
>   **→ the authorised rains wrapper works as written; the synchronous-heal
>   fallback is NOT needed.** F02's defer-when-falsy guard turns out not to be
>   load-bearing and is kept only as defence in depth.
> - **The pre-save hook COVERS AUTOSAVES** — `SaveGameStart`/`SaveGameDone` with
>   `autosave=true err=false`, twice, positive control `LoadGame FIRED` present.
>   Both autosaves were console-forced through the engine's own `Autosave` entry
>   point (`CreateRealTimeThread(Autosave)` — literally what
>   `Savegame.lua:1550-1555` does); no naturally-timed autosave was observed.
> - `97_SaveHookProbe.lua` torn down in the recording commit; **the stale-probe
>   sweep now returns zero hits in both repos.**
> Phase 1 (chain prompt 3) is unblocked and inherits the wrapper shape.

> ⚖️ **F86 STATE AS OF 2026-07-31 EVENING — the block below is the original
> filing and parts of it are SUPERSEDED. Current truth:** the design was
> **adjudicated twice** (`F86_ADJUDICATION.md` — yes-with-changes) and a
> **prior-art survey ran** (`PRIOR_ART_SURVEY.md`). Corrections that override
> the text below: capture is **value-reachability**, not frame position ("an
> empty `_ENV`" is WRONG — orphans resolve vanilla globals and lose only
> mod-created names, measured); "synchronous can never be captured" holds for
> the **thread-stack route only** (exposed set is **≥13**, incl. the compliant
> `Fix_CaveInsNoDisasters`); F02's hold is LIFTED and the build is authorised
> (Tiers 1+2, layer 1 gated); the sweep is DONE; **F88 filed** (the per-load
> restart). **Plan of record: `F86_EXECUTION_PLAN.md`; next session:
> ~~`F86_NEXT_SESSION_PROMPT.md`~~ **→ since 2026-08-01 the numbered chain in
> `docs/prompts/project/` (prompts 2-3 carry the split + the audit's C34
> rider; the original is archived).**
> Owner directives of the evening: orphan-gate rule (FIX_POLICY §3a), latched
> heal, and the **prelaunch save-exit deliverables** (uninstall procedure +
> standalone cleaner — WORKFLOW release gates).
> **PHASE 0 MEASURED + PHASE 1 DONE (2026-08-01, chain prompts 2-3):** GT
> creation DEFERS and the autosave hook FIRES (ENGINE_FACTS); the **final
> Tier-1 spec is `SAVE_SAFETY_REDESIGN.md` §6.2a** (rains wrapper shape final,
> C34 rider riding the rains pass, F81a mid-session NewDay reconcile taken,
> StormWedgeHeal orphan-gate reorder specced); the five-shape enumeration
> re-derived the durable exposed list at **13, plus one inert route-(c) site**
> (`Fix_LastTransmissionStorage`, adjudication §4.4 CLOSED — no build); the
> build prompt was `F86_TIER1_BUILD_PROMPT.md` (chain prompt 4 ran it;
> **consumed 2026-08-01 once Tier 1 was built and verified** — see the
> post-Tier-1 block higher up this file for what the legs read).
>
> 🛑 **PT-20 FAILED 2026-07-31 — WE HAVE A P1 DEFECT OF OUR OWN, AND IT BLOCKS
> RELEASE. See `BUGS.md` F86.** Executing PT-20's step 5 for the first time
> measured **pack code being written into the player's savegame and still
> running after the mod is removed**. Two sites proven live:
> `Fix_MeteorFrequency` (the colony's meteors stop **permanently** and do not
> self-heal) and `Opt_DroneOverhaul` (98 errors/session, log noise only — and it
> leaked with **its own opt-in toggle OFF**). **Ten more are exposed — 12 in total**; the sweep corrected the membership both ways the same day (`Fix_DroneUnreachableForever` IN, `Fix_TrainCargoDumping` OUT — see the F86 entry).
> - **The route is a THREAD STACK, not a storage location.** A save captures
>   every game-time thread with its blocked stack; a mod function there is
>   serialised by value and comes back with an empty `_ENV`. The audit's
>   "class tables are safe" clearance is void — `Drone.Idle` is a class-table
>   write and leaked anyway.
> - **Synchronous code cannot be captured**, so ~62 of 74 modules are safe by
>   construction.
> - Controls: reproduces identically with the pack *disabled* and with the
>   junction *physically removed* (98 vs 98 errors, same locals).
> - ✅ **THE OWNER DECISION IS TAKEN (2026-07-31) — all four calls answered, and
>   ONE game-free item is owed.** Full spec and the recorded calls in
>   **`docs/reports/SAVE_SAFETY_REDESIGN.md`** §4.
>   1. **Layer ordering 3 → 2 → 1 ADOPTED** and written into **`FIX_POLICY.md`
>      §3a** as a hard rule binding new fixes as well as repairs (that section,
>      not BUGS.md, is now authoritative for it): patch a synchronous input
>      instead of replacing a blocking body; no mod code after a call that can
>      block; `SaveGameStart` tear-down last, only for what survives, each with
>      its own A/B plus a soak.
>   2. **The layer-3 sweep is AUTHORISED at full scope** (all full-replacement
>      modules, not just the 12 exposed). Game-free. ✅ **IT HAS RUN over the
>      exposed set** (`SAVE_SAFETY_REDESIGN.md` §5): **five of the twelve have a
>      layer-3 or layer-2 route out**, each via a verified-synchronous input;
>      only four own-thread modules plus `BombardmentSpread` are layer-1
>      candidates. ✅ **The non-exposed half ran too (§5.4, all 22 modules): 6
>      convert cleanly to a chained wrapper, 4 need a design pass, 9 are
>      correctly full replacements, 3 already optimal. DECISION 2 IS
>      DISCHARGED** — nothing further is owed on the sweep.
>   3. **F02 is HELD until that sweep reports.** Do not touch
>      `Fix_MeteorFrequency`. Accepted cost: the measured leak stays shipped
>      meanwhile.
>   4. **D10 and D12 are sequenced BEHIND the rules** — neither build starts yet.
> - ⚠️ **The F02 worked example was corrected with the decision:** the wrapper
>   keys on **`CurrentThread()`**, not the meteor descriptor — `Meteors.lua:279`
>   and the **`MeteorStorm`** thread at `Meteors.lua:326` pass the *same*
>   descriptor, so descriptor-keying would fire the storm warning ~5 sols early
>   and make Sensor Towers irrelevant to it (a balance change, FIX_POLICY §4).
> - ⚠️ **And the exposure list grew: 13, not 12.** The sweep caught
>   **`Fix_DroneUnreachableForever`** — it replaces `Drone:ApproachWrapper`, whose
>   `DroneApproach` call blocks, and runs mod code after it, the same layer-2
>   violation measured in `Opt_DroneOverhaul`. An earlier "no 13th site"
>   certification is **withdrawn**. Detail: `SAVE_SAFETY_REDESIGN.md` §4a.
> ⭐ **THE BUILD IS AUTHORISED (owner, 2026-07-31) — scope in
> `SAVE_SAFETY_REDESIGN.md` §6. Tiers 1 and 2; ⛔ LAYER 1 IS NOT TO BE BUILT.**
> The scope follows a severity tiering: exposure matters most where we
> **replaced a vanilla body**, because then uninstall leaves the player *worse
> than never installing* — as opposed to modules that **own their thread**, where
> the only cost is one log line for a fix the player just removed.
> - **Tier 1 (build first)** — `Fix_MeteorFrequency` (**measured**: meteors stop
>   permanently) and `Fix_RainsDeadlock` (**same shape, not previously called
>   out**: we replace the *global* `RainsDisasterLoop`).
> - **Tier 2** — `Fix_DroneUnreachableForever`, `Fix_TrainWaitTime`,
>   `Fix_ArrivalDeaths` half (b); plus `Opt_DroneOverhaul` ⛔ **blocked on the
>   drone carve-out**.
> - **NOT built** — the four own-thread modules and `Fix_BombardmentSpread`
>   (which has no layer-3 route at all). Accepted residual.
> - ~~**⚠️ `Fix_ArrivalDeaths` half (a)** — the raw `SetPos` with no passability
>   search — **has no route yet** and needs a design pass.~~ **→ DESIGN PASS RUN
>   2026-08-01 (chain prompt 5) AND IT FOUND A ROUTE, so it was built:** the fix
>   never needed to change `pos`, it needs the colonist to *end up* walkable, and
>   `Colonist:OnArrival` is a verified-synchronous, arrival-specific seam running
>   after the placement. Layer 3, no residue.
> - **F02's hold is LIFTED**; ~~D10/D12 stay held **until these repairs land**~~
>   **→ ⭐ D10/D12 UNHELD 2026-08-01.** The owner's condition was "repairs land
>   AND verify". Tier 1 landed and verified (five legs, `c6180ad`); Tier 2 landed
>   and verified (PT-58 PASS, F86 Site 2 closed at zero against leg 5's 80).
>   **Both D10 and D12 are runnable now** — chain prompts 9 and 10.
> - ⚠️ The tiering is **reasoned from the measured mechanism, not measured**.
>   The control, if ever wanted, is one PT-20-method leg against an own-thread
>   module.
> - ✅ **Remedy measured:** reinstalling the pack DOES revive a killed thread
>   (`IsValidThread(Meteors)` → `true`, restarted by our own `LoadGame`). The
>   answer for an affected player is "put the mod back" — real, and uncomfortable.

> ✅ **F87 IS FIXED (2026-07-31) — and the repair went into the shared scaffold,
> not the one file.** `Fix_DustSicknessBiorobots` threw at apply when the player
> enabled the mod, leaving F40 silently unfixed for that whole session — **every
> player's first run**, because a mod is never auto-enabled and the main-menu
> tick triggers an in-place reload where the presets are already loaded and the
> classes are not yet built.
> - **`SMRFixPack.DataPatch` now runs nothing before `ClassesBuilt`**, fires from
>   `ClassesBuilt` / `DataLoaded` / `ModsReloaded` / `DataChanged`, seeds its
>   `data_loaded` gate from the engine's own `DataLoaded` global (the message
>   never re-fires on that path), and `pcall`s its pass — `Msg` dispatches
>   through `procall`, so a throw there was swallowed and the fix would keep
>   reporting `active` while doing nothing. The filter is now built with
>   `PlaceObj`, which fails soft; the old `type(X) == "table"` guard passed on an
>   unflattened classdef, which is exactly why this shipped.
> - **The sweep it earned found THREE MORE sites silently dead on the enable
>   path** — `Fix_TechDescriptionBuilding` (the patch itself),
>   `Opt_MultipleSuns` (the build-limit lift, so the module ran half-live) and
>   `Fix_FirstAsteroidPrefabs` (its self-check). All repaired through the new
>   **`SMRFixPack.OnDataReady`**. Constructor sites: 6, all at runtime, none
>   exposed.
> - **FIX_POLICY §2 carries the rule** (no `apply()` may assume a cold boot;
>   both paths must be tested) and **ENGINE_FACTS carries the traced sequence**.
> - **Cold-boot A/B re-verified CLEAR** — see the leg rows below.
> - ✅ **AND THE ENABLE PATH ITSELF IS NOW MEASURED — the leg RAN and PASSED
>   (19.09, owner ticked the box).** `68/74` → **63/0/15/0**, probe-for-probe
>   identical to the cold boot bar two RNG lines, with the `DustSicknessBiorobots`
>   probe — which reads live preset data — PASSing on the path that used to
>   throw. The harness logged its own positive control (`ARMED — the pack is OFF`
>   before the click, `ENABLE DETECTED` after), so it is provably not a cold boot.
>   **This is the first measurement this project has ever taken of a player's
>   first session.**
> - ✅ **AND AGAIN WITH ALL SEVEN OPTIONAL MODULES ACTIVE (19.24): `74/74` ->
>   68/0/10/0**, matching the all-ON cold-boot reference exactly. All five `Opt_`
>   probes PASS on the enable path. The log carries
>   `MultipleSuns: Artificial Sun build-once limit lifted` — a line that can only
>   come from the new `OnDataReady`, so one of the three sweep repairs is
>   confirmed firing on the very path where it was dead.
> - 🛠 **CORRECTION: "this leg also verifies audit A2" is WITHDRAWN.** A2 was
>   **answered YES in play by PT-55 on 2026-07-30** ("all three hooks install and
>   run on a first mid-session enable, no relaunch") and the audit caveat was
>   retired then. A2 is also a different path — the MODULE toggle mid-session,
>   not the PACK enabled at the main menu.

**⛔ NEW HARD RULE 2026-07-30 (owner) — FIX_POLICY §4a: this pack never fixes
other mods' problems.** Neither bugs caused by another mod, nor vanilla bugs
reachable only from mod code. "For modder benefit" is no longer a valid reason
to ship anything. Overridable ONLY by asking the owner explicitly, per case —
never inferred, never carried forward. **The test is WHO BENEFITS, not how visible the problem is** (owner's
clarification, same day): if a player could be harmed now or after a future
patch/DLC — even invisibly, even latently — it is a real fix and it ships; only
"the sole conceivable beneficiary is another mod" is barred. Operationally that
is the **R4/R3 boundary**: R4 needs new *calling code* (mod territory, barred),
R3 needs new *data* (ships with patches and DLC, so player territory, allowed).
It retired **F28** (R4, zero callers anywhere) and **nothing else** —
**F29 was briefly flagged and is KEPT**: its self-description as "mod-facing /
No shipped user" is factually wrong, the audit found four live shipped callers
in Mystery 2, making it R3 latent-by-data like F27/F31/F43. §4a now warns
explicitly: judge by enumeration, never by an entry's own words.

**Counts changed twice on 2026-07-30 — TWO modules deleted:**
**`Fix_ReplaceTechCount` (F28)** went under the new §4a rule: `Research:ReplaceTech`
has **zero callers in all of Src** (re-verified independently), so only mod code
could reach it, and it was carried as a §1.5 full replacement. Its TestKit probe
went with it (**probes 77 → 76**) — it asserted the fixed counter, so it would
have FAILed every leg. **The A/B that owed for it RAN the same evening and is
CLEAR** (19.20 leg — `73/73`, 76 probes, `66/0/10/0`; table below). Earlier the
same day:
**`Fix_DomePipeMoveInside` DELETED**
— F24 closed `wontfix` by user decision after the trigger was proven
unreachable in the shipped game (full proof on the F24 entry). No TestKit probe
existed for it, so the 77-probe suite is unchanged. **The owed A/B RAN the same
evening and the code gate is CLEAR** — see the post-removal row in the table
below. `Fix_TrainMinors` also lost its (c) guard the same day (F49(c)
`wontfix`, designed behaviour), which changes no counts.

**Just landed (2026-07-29 late, D09 build):** the drone stat dials DECISION is
BUILT — `Code/Opt_DroneStatDials.lua` + two Mod Options dropdowns: Drone
speed 1x/2x/3x/5x (range widened from the DECISION's 1.5x/2.0x by user call
after the live no-clamp probe: `SetMoveSpeed(10000)` read back exactly, clean
movement at ultra) and Drone carry +0/+1/+2. Techs' own label-modifier
machinery, reconciled on ApplyModOptions/CityStart/PostLoadGame, base =
modifiers removed = vanilla. D09 entry in BUGS.md; **PT-56 PASSED IN FULL
2026-07-30 → D09 `tested`**. **The owed
post-D09 A/B pair RAN unattended the same night — see the probe-state table
below (code gate CLEAR).**

**Landed earlier the same day (audit-remediation session):** `docs/archive/AUDIT_FINDINGS.md` (ARCHIVED 2026-07-30 — Phases 1-3 complete; **Phase 4 EXECUTED 2026-07-31**, C3 permanently barred)
Phases 1-3 implemented — code: veto re-check in the three data-patch fixes
(A1), DustSickness data-loaded latch (B3), file-scope install for the three
flattening-unsafe Opt_ hooks so a first mid-session enable works (A2),
reconciler "error" retry + skip logging (B1), MeteorStormWedge clears the
prediction flag itself (B2), logger escaping + build stamps (C4);
packaging: short_description / last_changes / optional_mod / ignore_files +
75 ModItemCode items (editor round-trip no longer wipes the mod) (A3);
description/README truthful: CohortHousing block, honest savegame claim,
console achievements + per-fix-disable disclosures (A4/B4/D1/D2). Docs
restructured (this header, ENGINE_FACTS, SESSION_LOG, archives). Details:
the newest SESSION_LOG leg.

**⭐ F83 IS BUILT AND `tested` — `Code/Fix_FirstAsteroidPrefabs.lua`, shape
(i), the load-time heal.** (Built 2026-07-30 late; **PT-59 PASSED IN FULL on the
keyboard 2026-07-31**, archived — see the block below the build description.) The owner's go was recorded, the corrected brief was
followed, and the build ran with its own probe and a CLEAR harness leg
(`74/74`, `67 PASS / 0 FAIL / 10 SKIP / 0 ERROR` at 77 probes — the all-toggles-ON
configuration *as it stood at build time*; that leg and its owed twin have both
since been superseded by the post-Phase-4 set at 78 probes, and **nothing is owed
on the harness side for the COLD-BOOT configurations** — see the enable-path
caveat on the A/B table below, added 2026-07-31). What
ships: an `OnMsg.LoadGame` sweep that, when the FirstAsteroid popup notification
is still sitting in the persisted `Notifications` table after a load — the only
state the dead real-time waiter can leave — **removes** it, **grants** the three
prefabs through the shipped `ColonyAddPrefabs` calls, **latches** a persistent
`SMRFixPack_FirstAsteroidPrefabs` GameVar, and **re-shows** the popup as pure
display so the player still gets the story text. The healthy path is untouched
(no reload means no `LoadGame`), which is what makes the double-grant trap
unreachable rather than merely guarded. Removing the notification is
load-bearing: its `PressFunc` is the only route back to the dead context, so
exactly one grant path exists — and that stays true even if a future patch moves
the shipped waiter to a game-time thread. **Shape (ii), the `show_once`
pre-mark, was verified against Src and REJECTED** (it depends on OnMsg order and
on `CreateRealTimeThread` scheduling that Src cannot settle, it moves the grant
off the healthy path for everyone, and it cannot heal an already-stranded save).
**Correction to the audit's build note:** matching the notification on `text[1]`
works only in a dev build — retail `T()` returns **light userdata** when the id
is in the translation table (`localization.lua:268`); the fix uses `TGetID`
(`:48-65`) and reads the id from the live preset rather than hardcoding it.
**✅ PT-59 PASSED IN FULL 2026-07-31 → F83 is `tested`** (archived to
`PLAYTEST_ARCHIVE.md`; nothing owed). Reload leg **1/1/1** with the grant line;
healthy leg **1/1/1** with `SMRFixPack_FirstAsteroidPrefabs` still `false`, so
vanilla granted and our code never ran; and the sitting logged **10 game loads
against exactly 2 grants**, with 7 non-granting loads between the two — Trigger
C many times over. Log clean. Two unasked-for results worth keeping: the heal
**discriminated between two asteroid notifications** sitting in the corner list
together (the loc-id match is doing real work), and **8 of 10 loads granted
nothing**, so the no-op path is the common one and it is silent.
⚠️ **The test's own procedure was wrong and has been corrected** — it never said
*which* popup to answer, and answering `ReconCenterDiscoveryAsteroid` produces
`0/0/0`, indistinguishable from a fix failure. It was reported as a FAIL before
the source settled it. The `FirstAsteroid` preset declares no choices at all and
its callback runs on any answer, so there is no wrong *button*, only a wrong
*popup*.

**The finding it closes (2026-07-30, live play) — F83, P2, mechanism PROVEN.**
Minimized story popups lose their callback across a save/load: the waiter is a
real-time thread and the async popup context is not persisted, while the corner
notification *is* — so after a reload the notification still opens, any choice
closes it, and the callback never runs. Found via a dead **View** button on a
founder popup (unrelated to F23/PT-44; not caused by this pack), isolated at the
keyboard, and confirmed by a controlled quicksave/reload leg. Six of the seven
affected call sites are cosmetic; **the seventh is `FirstAsteroid`, whose
callback grants three Micro-G Auto Extractor prefabs that the popup's own text
promises and `show_once` never re-offers.** **PT-58 RAN AND PASSED the same day
and the consequence is now OBSERVED, not inferred:** one purpose-built fixture,
one variable, **1/1/1 answered without a reload vs 0/0/0 answered after one**.
The notification survives the load, opens normally, and grants nothing.
**✅ THE QUEUED POPUP AUDIT RAN 2026-07-30 (`docs/reports/POPUP_CONSEQUENCE_AUDIT.md`)
and the hold is LIFTED: the narrow-decouple recommendation is REINSTATED.** The
storybit alarm that stopped the fix was wrong about the engine — **game-time
threads persist by default with their blocked stacks; only real-time threads
die on load** (new ENGINE_FACTS entry, three source proofs + observed
unit-command resumption). Storybits, mysteries, anomaly sequences and
challenges are save-safe by design; the defect family is exactly "consequence
owned by a REAL-TIME popup waiter": F83's two consequential sites (FirstAsteroid
OBSERVED; ReconCenterDiscoveryAsteroid — Detailed Scan recoverability still
needs eyes), six-ish cosmetic dead-View sites, and one latent shielded class
filed as **F85** (breakthrough choices ×3 + the Assembly "Colony Values"
choice — real-time waiters behind an open-immediately modal window; tier U,
settling observation = the rebind-quicksave check). F06 is NOT this family
(one-shot Msg race; its fix stands). The audit also left a **4-item needs-eyes
list** (audit §8, mirrored on the checklist) and repaired a BUGS.md structural
break (the F84 filing had swallowed the D06 heading). **The owner gave the
build GO the same evening** ("review and action on your findings") — the F83
decouple is queued as the next session's headline task with a **corrected
build brief** (double-grant trap caught after the go: vanilla's popup callback
always runs, even show_once-suppressed — see the F83 entry and
FABLE_NEXT_PROMPT's board; PT-58's kept fixture is the A/B — reload leg must
read 1/1/1 AND the no-reload leg must still read 1/1/1, not 2/2/2). Full trail
on the F83/F85 entries and the audit file.

**⛔ SCOPE CONTROL, owner 2026-07-31 — `docs/FUTURE_IDEAS.md`.** New parking
file for good ideas that are NOT needed before launch. **Nothing in it is work:
not owed, not scheduled, not counted, and never to be reported as
outstanding**; un-parking is an explicit owner decision, one item at a time,
after launch. Reason on record: mission creep — every three items closed were
adding about six. **Defects never go there** (they stay in `BUGS.md` with a real
status; declining one is a `wontfix` with reasoning). Entry 1 is
seniors-in-workshops. A proposed-parking list sits at the bottom of that file
awaiting the owner's yes/no — **read it before treating anything on it as
owed.**

**⭐ PHASE 4 COMPLETE AND CERTIFIED (2026-07-31).** C2 shared helpers
(`SMRFixPack.Log/Require/SetGlobal/WhenActive/DataPatch` in 00_Core, 58 files
migrated), C4 deeper self-checks (42-file EXIST-only tier enumerated and
raised; declaring-class failures now loudly diagnosed via a `__parents` walk),
and the C1 update-deactivation report (pregame-menu dialog, console-visible,
shown only when ≥1 fix deactivated over a game-code change; honest about what
self-checks cannot see). Eleven unattended legs, every one identical to the
control fingerprint (`docs/archive/fingerprint_before.txt` →
`fingerprint_after.txt`); full certification with evidence and residual risk
in the newest SESSION_LOG leg. C3 merges were BARRED and not done; the three
drone modules are untouched per the carve-out. **✅ The owed default-config leg
RAN 2026-07-31 12.44 after the owner set the six toggles OFF + dials to base:
`68/74`, 63 / 0 / 15 / 0 at 78 probes — the certification's predicted numbers
exactly (fingerprint: `docs/archive/fingerprint_after_default.txt`). NOTHING
is owed on the harness side; both shipping configurations are measured
post-Phase-4, and the account is in the clean all-OFF/base state.**

> 🧭 **UNDECIDED, and deliberately so — a possible PACK SPLIT (owner, 2026-07-31).**
> Under serious consideration: separating the project into **(a) the true fixes**
> and **(b) a companion mod holding the opt-in modules**. **No decision has been
> made and the owner does not want one yet** — a third state, like D08 and
> D06-structural. It is **not owed, not scheduled, not counted**, and **nothing
> may be deferred "until the split is decided".**
>
> **The reason for not deciding is itself the record:** the current single-mod
> shape is the best one for *testing*. One mod is one configuration matrix, and
> every measurement we hold is calibrated to it — the `fix pack present: N/74
> fixes active` line, the 78-probe fingerprint, the three-leg A/B set, and the
> baseline mechanism (emptying the `code` list). Splitting mid-testing would
> invalidate the comparison base.
>
> **Known impacts, recorded so the eventual decision is informed rather than
> rediscovered:**
> - **The harness is calibrated to one mod.** Counts, the baseline leg, and the
>   opt-in leg bridge (`SMRFixPack_Optional`) all assume a single `code` list.
> - **The `OptionsMenu` probe asserts six toggle wirings PLUS the two D09 dial
>   wirings** in one place; a split divides that surface across two mods.
> - **D05 (Mod Options) currently lives in the pack**, and the opt-ins are
>   reached through it — the companion would need its own options surface or a
>   cross-mod bridge (note `CurrentModOptions` is **per-mod-env**, ENGINE_FACTS).
> - **It composes with the cleanup-mod proposal** (D06 entry): that would already
>   make a second shipped artifact, so the question becomes the shape of a
>   *family*, not whether to have one.
> - **It has a natural deadline** — it changes what players install, so it is
>   cheap before beta and expensive after.

**Open user decisions:** ~~F83 fix option 1 go/no-go~~ — **GO GIVEN, BUILT
2026-07-30, and `tested` 2026-07-31** (PT-59 PASSED IN FULL; nothing owed).
~~Phase 4 go/no-go~~ — **EXECUTED 2026-07-31, see above.** Still open:
D01 standing-export half
(spec decided 2026-07-26, unwritten); F48 (parked section below); drone
overhaul structural choice (DRONE_OVERHAUL_OPTIONS.md — the stat dials are
BUILT (D09); the structural choice stays gated on the B2 re-run);
**~~F79~~ — CLOSED `wontfix` 2026-07-31 (owner: risk exceeds benefit on large
multi-stop maps; F80 must be explained first if ever revisited)**; D08;
**~~seniors-in-workshops~~ — PARKED 2026-07-31, see `docs/FUTURE_IDEAS.md`**;
**D11 shuttle same-pair passenger batching — candidate with feasibility on
file (BUGS.md entry), explicitly NOT green-lit: re-ask the user before any
build; multi-hop passenger routing REJECTED outright.**
**Decided, build queued:** D10 workshops module (speced + user-approved
2026-07-30, BUGS.md entry — text repairs + capacity dial; build gated on
PT-56 PASS — **that gate is now OPEN, PT-56 passed 2026-07-30**). **D12
no-homeless dome policy** (speced + user-approved
2026-07-30, BUGS.md entry — own module, `Opt_ResidencyControl` as donor pattern
only; breaks vanilla's emigration tie for homeless colonists so specialist
domes stop stranding them, which also unwinds the D07 overpopulated deadlock
without touching D07). **D10 and D12 both touch colonist assignment — land them
separately, each with its own A/B.** ~~Unfiled candidate: Universal Tunnel
description~~ **now FILED as F84** (2026-07-30) — the description is wrong twice:
it claims rovers cannot use the tunnel (**disproven by play** during PT-25) and
omits that it bridges life support. Text patch, but it converts a localized `T`
into an English-only `Untranslated` string, so **decide it together with D10's T1
text repairs** — identical tradeoff, should not be answered twice differently.

**A/B probe state — CURRENT is the POST-PHASE-4 set at 78 probes (2026-07-31).**
All six toggles ON: `74/74` → **68 / 0 / 10 / 0** (leg 12.30.34). Baseline
(`code` list emptied): **1 / 62 / 15 / 0** (leg 12.32.11), where both the
`FirstAsteroidPrefabs` and the new `UpdateReport` probes **FAIL** with
`fix pack not loaded (bug reproduces)`, proving they discriminate. Default
config, six toggles OFF + dials at base (owner-flipped, leg 12.44.39):
`68/74` → **63 / 0 / 15 / 0** — predicted before the run and landed exactly;
the D09 probe reports the carry dial AT BASE on entry, so the account is
genuinely clean. Every measured leg: zero `[CommunityFixPack]`
error/disabled/FAILED lines, no log line naming our `Code/`, known noise only.

> ✅ **THE ENABLE PATH IS NO LONGER UNMEASURED (2026-07-31 19.09).** Every leg
> above except the 19.09 row is a COLD BOOT — launched with the pack already
> enabled, describing the *second session onward*. The session in which a player
> *turns the mod on* is where **F87** lived, and it now has its own leg: TestKit
> `Code/98_EnablePathLeg.lua` (armed like `96_AutoRunFlag`, recipe in
> `PLAYTEST_HELP.md`) boots with the pack off, waits for **the owner to tick it
> at the main menu**, then drives the normal flow. **Its first run PASSED.**
> ⚠️ **Coverage note:** that run had the six toggles OFF, so the five `Opt_`
> probes SKIPped — the optional modules are still unexercised on this path. A
> second leg with them forced ON closes it. **It does NOT bear on audit A2**,
> which PT-55 answered in play on 2026-07-30.
The post-F83 set at 77 probes (`74/74` → `67/0/10/0`; default `68/74` →
`62/0/15/0`; baseline `1/61/15/0`) is now historical, as are all older rows.

| Leg | Active | Result |
|---|---|---|
| **⭐ NEWEST — the F49(a)-strip code-gate leg, default config, 2026-08-01 14.15 (unattended), 78 probes** | **68/74** | **63 / 0 / 15 / 0** — the owed leg for the F49(a) guard strip, CLEAR. Fingerprint vs the 18.44 default-config reference differs in exactly ONE real line (`TrainMinors` now `train cap recomputed 4->1, 40->2, 0->0`, palette clause gone as predicted) plus the two known RNG lines (`TouristApplicants`, `FounderTraitNotification`). `PROBE SWEEP:` armed `97_SaveHookProbe.lua` only (declared); `99_OrphanEnvProbe.lua` deleted before the leg and no `SMRTEST-ORPHANENV` line in the log |
| **⭐ CURRENT — THE ENABLE-PATH LEG, all optional modules ON via the `SMRFixPack_Optional` bridge, 2026-07-31 19.24 (owner ticked the box), 78 probes** | **74/74** | **68 / 0 / 10 / 0** — matches the all-ON cold-boot reference exactly; all five `Opt_` probes PASS on the enable path, and `MultipleSuns: … limit lifted` proves the `OnDataReady` repair fired there |
| **⭐ CURRENT — THE ENABLE-PATH LEG, default config, 2026-07-31 19.09 (owner ticked the box at the main menu), 78 probes** | **68/74** | **63 / 0 / 15 / 0** — **the first leg ever run on a player's FIRST session.** Probe-for-probe identical to the 18.44 cold boot bar 2 RNG lines. `DustSicknessBiorobots` PASS on live preset data = the F87 patch really ran. ⚠️ toggles OFF, so the five `Opt_` probes SKIPped |
| **CURRENT — POST-F87-REPAIR cold-boot re-verify, default config, 2026-07-31 18.44 (unattended), 78 probes** | **68/74** | **63 / 0 / 15 / 0** — identical to the 12.44 reference; proves the scaffold change did not regress the cold boot. Says NOTHING about the enable path |
| **CURRENT — POST-PHASE-4, all six toggles ON, 2026-07-31 12.30 (unattended), 78 probes** | **74/74** | **68 / 0 / 10 / 0** |
| **CURRENT baseline — POST-PHASE-4, `code` list emptied, 2026-07-31 12.32 (unattended), 78 probes** | — | **1 / 62 / 15 / 0** — `FirstAsteroidPrefabs` + `UpdateReport` FAIL here (`bug reproduces`) |
| **CURRENT — POST-PHASE-4 default config, six toggles OFF + dials at base, 2026-07-31 12.44 (unattended), 78 probes** | **68/74** | **63 / 0 / 15 / 0** — predicted exactly; carry dial AT BASE on entry |
| Baseline, historical (`code` list emptied) | — | **1 PASS / 61 FAIL / 15 SKIP / 0 ERROR** *(77 probes, pre-F28)* |
| Fixed, default config (six toggles OFF) | 69/75 *(pre-F24-removal)* | **62 / 0 / 15 / 0** |
| Fixed, all six toggles ON + dials | 75/75 *(pre-F24-removal)* | **67 / 0 / 10 / 0** |
| Post-removal re-verify, 2026-07-30 17.25 (unattended) | 74/74 *(pre-F28-removal)* | **66 / 1 / 10 / 0** — the 1 FAIL was the probe defect below |
| All six toggles ON, 2026-07-30 19.20 (unattended), 76 probes | 73/73 | **66 / 0 / 10 / 0** — pre-F83-build |
| Default config, six toggles OFF + dials at base, 2026-07-30 19.32 (unattended), 76 probes | 67/73 | **61 / 0 / 15 / 0** — pre-F83-build |
| Post-F83 build (superseded by Phase 4), all six toggles ON, 2026-07-30 23.29 (unattended), 77 probes** | **74/74** | **67 / 0 / 10 / 0** |
| Post-F83 baseline (superseded by Phase 4), `code` list emptied, 2026-07-30 23.46 (unattended), 77 probes** | — | **1 / 61 / 15 / 0** — `FirstAsteroidPrefabs` FAILs here (`bug reproduces`) |
| Post-F83 default config (LAST measured default, superseded by Phase 4), six toggles OFF + dials at base, 2026-07-31 01.37 (unattended), 77 probes** | **68/74** | **62 / 0 / 15 / 0** |

**The 01.37 leg (2026-07-31) — the shipping default configuration post-F83,
CLEAN, and the last thing the build owed on the harness side.** Run after the
owner set all six toggles OFF and both dials back to base (their own
`deactivated via Mod Options` lines are on record in the 01.33 session log).
`fix pack present: 68/74 fixes active`, **62 / 0 / 15 / 0** — predicted before
the run and landed exactly: the five opt-module probes flip PASS→SKIP as
`inactive (opt-in)`, so 67/10 becomes 62/15 with the same zero FAIL and zero
ERROR. `FirstAsteroidPrefabs` applied and its probe PASSed here too, confirming
the F83 fix is toggle-independent (it is a default-on fix, not an opt module).
The D09 probe reported the **carry dial AT BASE on entry** — the account state
is genuinely clean for the first time since the PT-58 sitting. Six
`[CommunityFixPack] … inactive (opt-in module …)` lines (six, not five —
DroneOverhaul reports status despite having no probe), zero error / disabled /
FAILED lines, no log line names our `Code/`, same noise profile
(2 `ResManager` `LawOfficeDoor`, `objects_to_mark` 48).

**The 23.29 leg — the F83 build's gate, CLEAR.** `fix pack present: 74/74 fixes
active`, **67 / 0 / 10 / 0** at 77 probes — the predicted arithmetic exactly
(66 + the one new `FirstAsteroidPrefabs` probe). `[CommunityFixPack]
FirstAsteroidPrefabs: applied` on load; the probe PASSed all three of its legs
(*"stranded save granted 1/1/1 and latched; already-healed and non-FirstAsteroid
states granted nothing"*). Zero error / disabled / FAILED lines, no log line
names our `Code/`, known noise only. **What this leg also revealed: the account
toggles are ON again** — the prompt doc's "owner left all six OFF" had gone
stale during the PT-58 sitting, and the D09 dial probe reported the carry dial
off base too. Read the account state, never trust a doc for it.

**The 19.32 leg — the shipping default configuration, CLEAN.** Run after the
owner set all six toggles OFF and both dials to base. `fix pack present: 67/73
fixes active`, and the result was **predicted before the run and landed exactly**:
the five opt-module probes flip PASS→SKIP as `inactive (opt-in)` (five, not six —
D06 has no probe of its own), so 66/10 becomes 61/15 with the same zero FAIL and
zero ERROR. `DroneStatDials` and `OptionsMenu` both stay PASS, confirming the
dials and the Mod Options wiring are independent of the toggles. The six
`[CommunityFixPack] … inactive (opt-in module, off by default …)` lines are the
expected healthy default-config signature, **not** error lines — six here, not
five, because DroneOverhaul reports its status even though it has no probe. Zero
error / disabled / FAILED lines, no log line names our `Code/`, same noise
profile again (2 `ResManager` `LawOfficeDoor`, 1 shutdown artifact,
`objects_to_mark` 48).

**The 19.20 leg — the owed A/B, run and CLEAR.** `fix pack present: 73/73 fixes
active`, matching the post-F28 registry exactly; **zero** `[CommunityFixPack]`
error / inactive / disabled / FAILED lines; no log line names our `Code/`; noise
profile identical to the 17.25 leg (same 2 pre-existing `ResManager` animation
errors, same shutdown-artifact `[mod] Error in mod … Test Kit`, `objects_to_mark`
48→59 with the random map). The account had all six toggles ON at that point,
hence `73/73` — **read the state, never assume it.**

**The D09 probe defect is REPAIRED (TestKit, 2026-07-30 late) and verified.**
The probe used to take its baseline from the live const, valid only when the
account dial already sat at base; it now forces both dials to base through the
real Apply path, measures from there, and restores the leg's entry values, with
a cleanup check against the entry reading rather than against base. It went
**green on the 19.20 leg with the account carry dial still at +1** — the exact
state that FAILed it at 17.25. Consequence: **an A/B leg no longer has a
set-the-dials-to-base precondition.** PT-56 still does, for its own step-1
baseline reads (BUGS.md D09 entry, item 1).

**The 17.25 leg (superseded by 19.20, kept for the record):** the code gate for
the F24 and F49(c) removals, run unattended after both. `74/74 fixes active` —
exactly one fewer than the pre-removal 75/75, which was the F24 deletion and
nothing else — zero `[CommunityFixPack]` error lines, `DroneStatDials: applied`,
probe total still 77 (F24 had no probe). Its single FAIL was the D09 probe
defect described above, now repaired.

**Reading any leg:** baseline's 1 PASS is the FactionFundingCheck canary, and
the D09 probe FAILs baseline by design ("fix pack not loaded"). The 10 SKIPs in
a fixed leg are 9 `[install]` retail-sandbox probes + TechDescriptionBuilding; a
default-config leg's extra 5 are the opt-module probes reporting `inactive
(opt-in)` — five, not six, because D06 has no probe of its own (the stress
harness covers it). Known synthetic-map noise only: ~50-60 `Flight.lua`
`objects_to_mark` errors, a few GameInit nil-call lines, 2 `ResManager Error`
missing-animation lines (`LawOfficeDoor`, pre-existing and present in every leg),
the MultipleSuns "not found → lifted" load transient, and a `[mod] Error in mod …
Test Kit` line at quit (shutdown artifact).

**The post-D09 pair caught two real defects en route** (both fixed
same-session, see the D09 entry): the module's file-scope `Modifier.new` check
tripped the F64 pre-flattening trap, and the probe's first version wrote the
TestKit env's own `CurrentModOptions` (per-mod-env — new ENGINE_FACTS entry).

**⚠️ ACCOUNT STATE as of 2026-07-30 19.32 — READ IT, NEVER ASSUME IT.** The
owner set **all six toggles OFF and both dials to base** before that leg, and the
`67/73` reading confirms the toggles. **This is the clean state PT-56 needs** —
if a later sitting moves the dials again, PT-56's step-1 baseline reads go stale
the same way they did on 2026-07-30 afternoon. Note the repaired D09 probe is
deliberately *immune* to account dial state, so a leg's PASS no longer proves the
dials are at base; the probe was therefore extended the same evening to **report
the dial state it found on entry**, restoring the observability the broken
version had by accident. **Read the DIALS too, not just the toggles.** Pre-D09
reference set (76 probes): baseline 1/60/15/0 · default 61/0/15/0 at 68/74 ·
all-toggles 66/0/10/0 at 74/74.

**Next gates (owner playtests — PLAYTEST_CHECKLIST.md):** **PT-55 CLOSED IN
FULL 2026-07-30** (archived; audit A2 caveat retired; the D01 parked-rocket
limitation ACCEPTED by user call `4f5f61e` — a parked rocket picks the
behavior up on its next landing, `on_activate` enhancement on record but
unbuilt). **PT-48 CLOSED IN FULL 2026-07-30 → D02 `tested`** (archived; all
five steps on console counters, opened with a positive control; the acked
building held 4.2 vanilla windows and the stamp survived save/reload; a vanilla
GameTime-vs-RealTime curiosity on `InsufficientResources` was filed on the D02
entry for a game-free look). **PT-25 PASSED IN FULL 2026-07-30 → F38 `tested`**
(archived; rover used the tunnel, took the long way once destroyed, **still took
the long way after a save/quit/load** — the leak the fix closes — and **used it
again after Rebuild**, the over-reach guard. Its setup line was WRONG and was
corrected at the keyboard: the tester spotted that the underground has no tunnel
at all, and tunnels turned out to be a surface building — fourth PT found faulty
by executing it. F38 itself survived the challenge. **SAVE-B is retired**, PT-25
was its last consumer and never needed it. The rover check also **disproved the
Universal Tunnel's description → F84**.)
**PT-44 PASSED 2026-07-30 → F23 `tested`**
(archived; the notification fired 0→1 on the module's own counter and read
"Founder Has Trait / Ciara Grant: Fit" — exactly one, with the dead shipped
handler staying dead. Console-injected grant, so it verifies rendering; the path
is R1 by enumeration. It also corrected a checklist expectation: a notification
click selects its object **only when that object is visible** — an indoors
colonist gets a camera pan and no selection, which is correct vanilla.)
**PT-56 PASSED IN FULL 2026-07-30 → D09 `tested`**
(archived; all four steps live, including the stale-save reconcile — a save
carrying 2x/+1 modifiers, loaded against base dials, came back at the baseline
`1728/1`. **This UN-GATES the D10 workshops build**, which is speced,
user-approved and ready to write). Next: PT-53 Trigger E (the
last thing between D07 and `tested`); ~~PT-54 wedge watchdog~~ **(RETIRED
unrun 2026-08-01 → the F86 Tier-1 build legs)**; PT-52 Trigger B +
the B2 re-run on the v2 stress harness; PT-20 save/remove/load
incl. wave-6 persisted state; PT-21. **PT-46 tail: (d) PASSED 2026-07-30**
(cap follows length, `43/2`→`13/1` across a salvage); **(a) settled R4 by the
reachability audit** (no player-reachable entry into `place_track` — see the
audit's lead-pass block); **(c) closed `wontfix` 2026-07-30 (user decision,
tier I — designed behaviour), guard REMOVED (`d03417b`)**. F49 now holds at
`fixed*` on (a)+(d), carried by (d).

**Newest legs:** `docs/archive/SESSION_LOG.md` → the 2026-07-30 set, newest
first: the PT-55 closure leg, the PLAYTEST_CHECKLIST/PLAYTEST_HELP split leg,
the curiosity leg (tunnel water, workshop research → D10 spec, shuttle limits
→ D11 candidate), and the parallel playtest legs (PT-55/PT-53-A/D12); the
2026-07-29 D09-build and PT-11 legs sit below them.

**Playtest-method rule earned 2026-07-29 (applies beyond PT-11):** compressing a
scheduler's `g_Consts` interval does NOT shorten the sleep already in flight, so
a "nothing should happen" test must **re-arm the repeat**
(`RestartPeriodicRepeatThread`) and **carry a positive control**, or it
false-PASSes regardless of the fix. Full rule in PLAYTEST_HELP.md (the
checklist's reference half, split out 2026-07-30). Two tests have now been found unrunnable-as-written by actually running
them (PT-29, PT-11) — treat an un-run PT's procedure as unverified until it has
been executed once.

**Tech-gated fixes — coverage settled 2026-07-29, re-grounded by the
2026-07-30 reachability audit.** F41 is `tested` (PT-29). Of the other four,
**F28** (R4 — zero callers in all of Src; the audit's one DELETE candidate,
user decision pending), **F43** (R3 — corrected grounds: MoistureVaporator IS
tech-locked, but its `require_prefab`+unlocked cargo item routes it into the
branch the shipped code handles; the old "no tech-locked entry" wording was
wrong) and **F25** (R2 — pre-1.0.6 legacy saves; note the probe's SKIP label
may be mislabeled, see the entry) are correctly untestable in play. **F18** is
the only genuinely uncovered one: preset half probe-covered, play half needs
the Independence arc + a special project; judged not worth a PT for a
data-only P2.

**REACHABILITY AUDIT COMPLETE 2026-07-30 — `docs/reports/REACHABILITY_AUDIT.md`.**
All 66 fix modules + both sanitizer passes audited for player reachability
(the F24 question, asked pack-wide): ~21 R1, ~38 R2, five R3 (kept — F27,
F29†, F31, F43, F57(a)†; † = §1.5-latent, flagged), one U (F11, settling
observation on the entry), two R4 — F49(a) (kept, lives inside a module with
two live halves) and **F28 (DELETE candidate, awaiting user decision)**. A
proposed FIX_POLICY §4 amendment (reachability tier required before a fix
ships) ~~is drafted in the audit file, not applied~~ — **APPLIED 2026-08-01,
`FIX_POLICY.md` §4 is the authority now**; the two † entries above are exactly
the R3-plus-§1.5 combination it makes conditional on an owner decision, routed
to chain prompt 7. Eleven BUGS.md entries
carry new "Audit 2026-07-30" notes (evidence corrections: F06, F17, F22, F25,
F34, F37, F40, F43, F49, F74, F81 — plus F11's observation).
**CHALLENGED same day and one verdict fell: F49(c) was tabled "live R2"
unenumerated and was in fact designed behaviour** — closed `wontfix` by user
decision, guard removed. The "Challenge review 2026-07-30" appendix in the
audit file answers it: the three-part method failure (bundle inheritance;
grading reachability while inheriting defectiveness — source is decisive on
"can this path execute" and near-mute on "is it wrong", so UI-shaped
misreadings come back confident, not uncertain; evidence base going stale
mid-audit — `c3c4383`/`ba1e88b` landed during the run and were not re-read),
the two unenumerated verdicts (F49(c) wrong, F49(d) late-enumerated and
holding), the eleven-row source-blind-spot list with settling observations,
the new tier **I — Intentional**, and the REVISED §4 (**APPLIED 2026-08-01**,
`FIX_POLICY.md` §4) now requiring a
positive intent statement (hard tells: player report / dead code / sibling
contradiction / self-contradiction / dev comment; no tell → keyboard
observation before any fix is written). Still not applied — user go-ahead.

## What this project is

"Community Fix Pack" — a runtime-Lua bug-fix mod for Surviving Mars: Relaunched
(game dir `A:\SteamLibrary\steamapps\common\Project Spark`, Haemimont Sol engine,
NOT Unreal; full gameplay source shipped in `<game>\ModTools\Src`). No game files
are modified; planned community release after user testing. Dev repo:
`C:\Dev\SMR-BugFixPack` (git). Installed via junction at
`%AppData%\Surviving Mars Relaunched\Mods\SMR-BugFixPack`.

Companion **Test Kit** mod (never shipped): `C:\Dev\SMR-BugFixPack-TestKit` (git).
`SMRTest.RunAll()` runs one probe per fix and prints PASS/FAIL/SKIP; run it with
the fix pack disabled (expect FAILs) and enabled (expect PASSes). It also enables
the Lua console at load and carries observability loggers and state reports.

## Optional modules (6, off by default)

**Players enable them in Options → Mod Options (D05 — live toggles, both
directions, including a first mid-session enable since the 2026-07-29 audit
fix);** the pre-load `SMRFixPack_Optional = { <Id> = true }` table remains as
the override surface for other mods and the test harness.
`SMRFixPack.ListFixes()` reports them as `inactive` with the opt-in reason
until enabled. Files use an `Opt_` prefix instead of `Fix_` to mark them as
not-bug-fixes. Full detail: each module's BUGS.md D-entry and file header;
build history in SESSION_LOG.md.

- **ClassicRockets** (D01, `Code/Opt_ClassicRockets.lua`) — a player-controlled rocket
  parked at the colony keeps its launch ration requested even with no destination selected,
  so drones refuel it while it waits. Only the fuel half of D01; the standing Rare Metals
  export half is deliberately unwritten (see the D01 entry).
- **AcknowledgedWarnings** (D02, `Code/Opt_AcknowledgedWarnings.lua`, added 2026-07-27,
  **`tested` 2026-07-30 — PT-48 PASS in full**) — dismissing "Building Not Working"
  acknowledges the listed buildings until they recover; new breakages always warn
  immediately.
- **ResidencyControl** (D03, `Code/Opt_ResidencyControl.lua`, added 2026-07-27) —
  per-dome/habitat "closed to new residents" policy row; quarantine untouched.
- **MultipleSuns** (D04, `Code/Opt_MultipleSuns.lua`, added 2026-07-27) — lifts the
  Artificial Sun build-once limit and carries the absorbed F39 panel-binding fix.
  **This module is also where F56 would land** if the closed-`wontfix` auto-offload
  decision is ever reopened (user decision 2026-07-26): auto-offload and the export half
  are the same "rockets should load and unload themselves like they used to" request over
  the same machinery, so they ship together behind this one flag or not at all. Do not
  create an `Opt_AutoRocketOffload`.
- **DroneOverhaul** (D06, `Code/Opt_DroneOverhaul.lua`, added 2026-07-28, experimental) —
  closest-fleet-first claim gate on repair/clean work + idle-drone moonlighting for
  saturated neighbor hubs + `SMRFixPack.DroneReport()` telemetry. Stat dials and the
  structural choice are an open decision (DRONE_OVERHAUL_OPTIONS.md), gated on the
  B2 re-run with the v2 stress harness.
- **CohortHousing** (D07, `Code/Opt_CohortHousing.lua`, added 2026-07-28) — Seniors and
  Children in normal housing auto-move into free Retirement Home / Nursery slots (own
  dome first, reachable dome second); employed Seniors exempt, player orders win,
  quarantine/closed domes respected. PT-53 3-of-5 PASS; A/E halves owed.

## Parked by decision, not by effort — one entry left open (F48)

Each has a full write-up on its BUGS.md entry. None was parked for effort; each was parked
because the remedy is not a defect repair, or because the shipped code no longer matches
the tracker. **Only F48 is still open** — the other four are closed.

| ID | Why it is parked | What would unblock it |
|----|------------------|------------------------|
| **F56** | ~~blocked~~ **CLOSED `wontfix` 2026-07-26 (user decision), same grounds as F62/F63.** Screened in the wave-4 build leg: the cited code is designed scope (`GetAutoGatherDeposits` is a declared accessor; the `Automation_Unload` rocket exclusion goes through the Relaunched `IsRocketClass` shim, i.e. maintained intent; auto mode promises only "gather resources"). **No standalone opt-in** — if revisited it belongs in `Opt_ClassicRockets` beside D01's unwritten export half, never in an `Opt_AutoRocketOffload` of its own. | — done. Rides on whatever design decision D01's export half gets, or stays closed. |
| **F32** | ~~blocked~~ **CLOSED `wontfix` 2026-07-26 (user decision).** The shipped data already carries the fix (`NotWorkingBuildings` is now `Suppressable`); the other two presets are one-shot adds. The residual by-design annoyance (2-real-minute window, per-category suppression, no per-building ack) is spun out as **D02** — a planned `Opt_AcknowledgedWarnings` module, gated on **PT-38**; MOD_DESCRIPTION carries a player-facing "looks like a bug, isn't" explainer. | — done. D02 build belongs to a wave-4+ leg after PT-38. |
| **F42** | **NEW, wave-5 screening.** `blocked` — wontfix candidate. The tracked observation is entirely correct and does not add up to a defect: the guard it names exists to stop units being entombed, a dust devil has no footprint to be entombed in, the omission sits in declared overridable class members, no shipped text promises the block, and the game's one weather-gated placement rule (`RocketLandingDustStorm`) is implemented and working. Full write-up on the entry. | **A user decision.** Recommend `wontfix` on the F56/F62/F63 grounds. |
| **F48** | Mechanism confirmed, but the corrected call runs `OrderTrackElements`, which clears and rebuilds `el.connections` and rewrites `node_idx` on **every element of every track**, with a non-unwinding `assert` as its only failure handling. Too invasive to ship untested for a P3. | **PT-37** (added 2026-07-26) — exact console steps for the healthy-network + meteor-damaged-track test, on the user's in-person list. PASS → sanitizer behind a one-shot flag; FAIL → `wontfix`. |
| **F24** | **CLOSED `wontfix` 2026-07-30 (user decision) — fix DELETED.** Real defect (water grid passes `dome` where its electricity twin passes `self`), but **unreachable in the shipped game**: its only live call site can't reach the buggy line (`SpireBase` is not a life-support object), and the `Dome:OnLoad` sweep needs a state vanilla can't produce — domes refuse to place over buildings, no dome has an upgrade, interior shapes never change at runtime. Carried as a 34-line full-function replacement, so deletion beat latency. Counts 75→74 / 69→68. | — done. Rollback is one `git revert` if a counter-example appears. |
| **F49(c)** | **CLOSED `wontfix` 2026-07-30 (user decision) — guard REMOVED. It was fixing DESIGNED BEHAVIOUR**, a different and worse failure mode than F24's unreachable-but-real defect. Established at the keyboard: salvage mode targets objects not hexes, the cursor always names its target (red `Salvage` = no action permitted), the `Salvage Train Station`→`Salvage Track` handoff is seamless to the millimetre, and **no exposed control separates a station from its own connector track**. The propagation the item called a defect is what makes that boundary continuous; the guard would have carved a dead band into it. The module keeps (a) and (d) — counts unchanged. | — done. The reachability audit rated (c) "live R2" **without ever enumerating it**, and its R1-R4 vocabulary cannot express "reachable, but intended" — both ANSWERED in the audit's own "Challenge review 2026-07-30": new tier `I` — Intentional — with (c) reassigned to it. |
| **F28** | **CLOSED `wontfix` 2026-07-30 — barred by the new FIX_POLICY §4a hard rule.** Real defect, but `Research:ReplaceTech` has **zero callers in all of Src** — only mod code or the console can reach it, and it shipped as a §1.5 full replacement (37-line body copy) carrying per-update re-verification cost forever. Not an oversight: the entry said "No vanilla caller" the day it was filed and shipped anyway on a "modder benefit" rationale, which §4a now bars. Fix **and its probe** deleted; counts 74→73 / 68→67, probes 77→76. | — done. Rollback is one `git revert`. Optional later: rebuild the probe as a vanilla canary on the F10 precedent. |
| **F62** | ~~blocked~~ **CLOSED `wontfix` 2026-07-26 (user decision).** Verified identical to the original game (same one-hop algorithm, same two transitive-predicate callers): carried-forward dev vision in both games, breaks nothing. No opt-in module planned. | — done. |
| **F63** | ~~blocked~~ **CLOSED `wontfix` 2026-07-26 (user decision), same grounds** — no training term ever existed in either game's emigration score. | — done. |

Recorded on those entries but deliberately untouched (real inconsistencies, no action):
walkability says A↔C is walkable while services say C is invisible from A;
`CanWorkTrainHereDomeCheck` permits training at a train-reachable school that
`ChooseTraining` never offers; the `PlanetaryAsteroidVisitPossible` legacy branch's
`and`/`or` precedence slip; `IsDifferentAsteroidLocation` comparing a map to a
MapDescriptor. All are permissive failures — none blocks a player.

## Key technical facts — MOVED

The engine-facts section that lived here is now **docs/agent/ENGINE_FACTS.md** (sole
authoritative home; moved verbatim 2026-07-29, audit remediation 3.2).

## Waiting on the user

1. DONE 2026-07-25/26 — retail A/B pairs clean AND the MarsDebug [install] pass is
   complete (49 PASS / 0 FAIL, F73 fully verified — see the QA session leg in
   SESSION_LOG.md).
   **Automated + attended probe coverage is now 100%**; ~~nothing further is owed
   to the harness~~ — **corrected 2026-07-31: that "100%" covers the cold-boot
   path only. The enable path (player ticks the mod at the main menu) has never
   been measured and is where F87 lived.** ✅ **RAN 2026-07-31 19.09 and
   PASSED** — see the A/B table. A second leg with the optional modules forced
   ON covers the five `Opt_` probes on that path. All that remains otherwise is
   the human playtest.
2. DONE 2026-07-26 — author set to **catt144** in both mods' metadata.lua.
3. For the save-failure lead: logs from `%AppData%\Surviving Mars Relaunched\logs`
   and Ctrl+F1 reports from affected players would pin it.
4. An in-game observation for F55: do drones still enter a dome after the roof is
   opened? The Lua half of that report turned out not to be actionable (see the
   F55 entry) — only play can tell us whether the entity data is at fault.
5. Manual playtest per `docs/PLAYTEST_CHECKLIST.md` (**recounted 2026-08-01:
   17 PT sections carried, of which 2 are not runnable — PT-52 frozen, PT-54
   retired — so 15 live, plus the §6 needs-eyes riders**; the previous "35"
   predates the archive sweeps; no third-party mods;
   covers what scripts can't: feel, visuals, UI, long-running behavior). Results
   reported back flip each covered fix's BUGS.md status to `tested` — see that
   file's "Reporting protocol" section for the exact follow-up workflow.
6. **All decisions made (2026-07-26).** F32 closed `wontfix` → D02 filed (planned
   `Opt_AcknowledgedWarnings`, gated on PT-38); F62/F63 closed `wontfix` (carried-forward
   design in both games, user decision); F10 retirement STAGED (46 modules / 45 active,
   final `wontfix` gated on PT-36; rollback is one metadata line); F48 rides on PT-37;
   TestKit stays local-only. Nothing is blocked on a decision anymore — only on play.
8. ~~TestKit remote~~ **DECIDED 2026-07-26: local-only, by design.** The kit was never
   meant to ship publicly, so no remote is created. Note the consequence: the repo's
   51 commits exist in exactly one place — if a local backup is ever wanted,
   `git -C C:\Dev\SMR-BugFixPack-TestKit bundle create <somewhere-else>\testkit.bundle --all`
   is the one-liner (a bundle is a single file that `git clone` accepts).
7. A donated save that researched **Frictionless Composites before the game patched the
   tech** is the only true fixture for the F35 sanitizer pass (PT-35 case C). Everything
   else about that pass is probe-covered.
10. **~~OPEN (2026-07-29)~~ — CLOSED: the F81/F78 disaster fix scope decision was
   made and built on 2026-07-29** (both open questions answered by the QA
   review, watchdog chosen over the full replacement; label corrected
   2026-08-01, the resolution was already recorded in this item's own closing
   parenthetical). Kept for the reasoning. F81 is
   CONFIRMED LIVE and the leak is unconditional (every completed meteor storm
   strands the flag and kills that colony's weather). Proposed package:
   (a) replace the global `MeteorsDisaster` with a **per-invocation** bounded
   drain loop + guaranteed notification removal on every exit path; (b) a
   one-shot `OnMsg.LoadGame` reconciliation clearing stranded predicted flags,
   which is what heals saves already poisoned; (c) a bounded `WaitMsg` in
   `RainsDisasterLoop`. **Gated on the `QA_REVIEW_PROMPT.md` review** — the open
   danger is how to distinguish a stranded flag from a legitimate warning in (b)
   without suppressing a real disaster warning, plus whether a watchdog (F02
   precedent) beats a full-body replacement that rots on game patches.
   *(Review since fired and both questions answered: `FindNotification` +
   Dismissable=false makes the stranded/legit test sound, and the watchdog DID
   beat the replacement — wave 6 built 2026-07-29 late; ~~PT-54 gates it~~ →
   PT-54 RETIRED unrun 2026-08-01, the F86 Tier-1 build legs gate it.)*
11. **OPEN (2026-07-29): D08 — the extender overhaul**, five layers speced in
   `DRONE_OVERHAUL_OPTIONS.md` with a risk table. Recommended order is
   dispatcher → Command Center tab + advisory → cluster scoping → adjustable
   radius → building (last, gated on PT-20). Also gated on the QA review.
9. **~~OPEN: the F79 decision~~ — CLOSED `wontfix` 2026-07-31 (owner).** Trains
   never carry service seekers; the gap is real but feature-completion was
   DECLINED — risk of new issues exceeds the benefit, especially on a large
   multi-stop end-game map. Two facts on file back it: F80 (the train boarding
   layer has an open, unexplained defect) and the fix sketch's post-wrap on
   `Dome:GetService`, a hot path whose added station walk scales with exactly
   that map shape. **Not parked, not owed.** If ever revisited, F80 must be
   explained and closed first. Full reasoning on the F79 entry.

## Save-rescue expectations (for release messaging + sanitizer design)

~60% of fixes help broken saves IMMEDIATELY (behavioral code re-evaluated every
tick/cycle: drones, colonists, schedulers — F02 pattern of thread-restart on
LoadGame where needed). ~25% need active repair; those passes now ship — eight in
their own fix files plus F03 and F35 in `Code/90_SaveSanitizer.lua`. Only F48
remains queued, and it is blocked on an in-game test (see the blocked table). ~15% is irreversible history (dead colonists,
lost expeditions; F64 voided trains have no recorded count — heuristic
compensation option at best, and document the vanilla train re-purchase at
stations, Station.lua:573-611). Save rescue is the headline differentiator vs
official patches ("new games only") — lead with it.

## Distribution facts (researched 2026-07-25, source-verified)

- BOTH Steam Workshop AND Paradox Mods are supported; the in-game Mod Editor has
  upload buttons for each (ModEditor.lua:78/:115). Steam Workshop reaches PC
  only; **Paradox Mods is the only channel that reaches Xbox/PS5** — platform
  fan-out is automatic on the backend, no platform fields, no modder-side
  signing (PS5 signatures are created client-side at install, Mod.lua:49-95).
  Console loads packed Lua code mods fine; no engine restriction found.
- PDX upload hard-requires: title, short_description (≤200 chars), description,
  preview image, lua_revision; last_changes on every update; ≤10 tags
  (ParadoxMods.lua:13-54, Mod.lua:410). GitHub repo link goes in metadata
  `external_links` — "github" is a supported LinkType shown on the PDX portal
  (Mod.lua:180-201). Default ignore_files already excludes *.git/*.
- Public repo: github.com/catt144/SMR-CommunityFixPack (main). Commit identity
  is the GitHub noreply address — never commit with a real email again.
- **CORRECTED 2026-07-26 (user unlocked one in play):** achievements are NOT
  disabled by mods on PC/Steam. `DoModsBlockAchievements()` returns
  `Platform.playstation or Platform.xbox or Platform.windows_store`
  (Achievement.lua:61-63) — the ModManager.lua:78 string is warning TEXT shown
  only behind that gate. Mods block achievements on console/MS Store ONLY.
  Separately, cheat use is logged per save (`LogCheatUsed` → persisted
  `CheatsUsed`, Network.lua:241-255) and adds "cheats used" to the
  unlock-refusal reasons on retail — so cheated fixture saves self-block their
  achievements. Mod description: say achievements keep working on PC, are
  disabled on consoles.

## Release checklist (when fixes are tested)

Real author + version bump in metadata.lua; player-facing fix list in README +
mod description; upload via in-game Mod Editor (check docs/.git exclusion; the
Test Kit must NOT be uploaded); credit ChoGGi (Fix Bugs) + LukeH (Martian
Express) as prior art; keep per-fix disable instructions in the description.
Four `[DRAFT NOTE]` markers remain in `MOD_DESCRIPTION.md` (lines ~6, ~90 F76 explainer, ~390 ClassicRockets export half, ~448 final) and are
deleted before the text ships. The export-half one is load-bearing: do NOT promise the
ClassicRockets module's unwritten Rare Metals export half.

---

## ✅ F87 FIXED — the enable path is now owned by the shared scaffold, and the sweep it earned found three more casualties — 2026-07-31 late (game-free, unattended leg)

Started from `docs/prompts/FABLE_NEXT_PROMPT.md` at `82a6e8a`, board item 0 (owner: do
F87 first). Everything below is one session; five commits, all pushed.

### 1. The diagnosis moved: the defect was in the scaffold, not the file

The entry described a one-line repair in `Fix_DustSicknessBiorobots`. Reading
the shared `SMRFixPack.DataPatch` runner made it clear the file was innocent:
`apply()` runs before class flattening on **every** path, and the cold boot
merely hid it — the presets are not loaded then either, so every pass returned
early before touching a constructor. The enable path removes exactly that
coincidence. So the repair went into the runner and every `DataPatch` user
inherits it.

Source traced rather than assumed (all now in `ENGINE_FACTS.md`):
`ModsReloadItems` → `ReloadLua` → `dofile(autorun)` → `Msg("Autorun")` (classes
built) → `ContinueModsReloadItems` → `Msg("ModsReloaded")`. **`LoadData` is not
in that sequence**, which is why `DataLoaded` never re-fires; the engine's
`DataLoaded` *global* is `FirstLoad`-scoped and therefore survives the reload,
which is the only evidence available on that path. And it is set **after** the
message is posted, so it reads false inside a `DataLoaded` handler — a trap the
first draft of the repair would have walked into.

Two things the repair does that the entry did not ask for, both earned:
- **`pcall` around the pass.** `Msg` dispatches through `procall`
  (`cthreads.lua:20`), so a throw in a message handler is *swallowed* — the fix
  would have kept reporting `active` while doing nothing. That is the F87
  failure mode with no log line at all. Now it reports `error` and C1 sees it.
- **`PlaceObj` instead of `:new`.** Not only because the entry says so: it fails
  soft (returns nil for an unbuilt class) where `:new` throws, and it is the
  form the shipped data itself uses for the sibling filter.

### 2. The sweep found three more, and two of them were functional

All 75 files, both shapes the entry names. Constructor calls: 6 sites, every one
at runtime inside a patched method or a msg handler — none exposed. Preset
patching outside the scaffold: **three sites hung off `OnMsg.DataLoaded` alone**,
each silently dead for the whole session on the enable path —
`Fix_TechDescriptionBuilding` (the patch itself), `Opt_MultipleSuns` (the
build-once lift; with the toggle already ON from account state the module ran
half-live, binding fix working, limit not lifted) and `Fix_FirstAsteroidPrefabs`
(its self-check). All three now go through the new `SMRFixPack.OnDataReady`.

So the blast radius of "our harness only ever measured one load order" was four
modules, not one.

### 3. The harness leg exists now, and one click of it cannot be automated

`AccountStorage`, `SaveAccountStorage` and `ModsReloadItems` are **all** in
`ModEnvBlacklist`, and there is no console at the main menu — so no mod-side or
console-side path can flip the checkbox. Everything after the click is
automated: TestKit `Code/98_EnablePathLeg.lua` watches `ModsReloaded`, refuses to
run if the pack was already on at boot (that would be a cold boot wearing the
leg's name), and hands off to `SMRAutoRun.Flow()`, which was factored out of 95's
entry thread for the purpose.

No new probe was needed: `FixMissing` already FAILs any probe whose fix is not
`active` (an `apply()` that threw) and the data-patch probes read live preset
data (a patch that never ran). Both F87 symptoms are covered by the suite we
already have — which is the sharpest version of the finding: **the probes were
never the gap; the load order was.**

### 4. Cold-boot re-verify — CLEAR

18.44 unattended, default config, 78 probes: `fix pack present: 68/74 fixes
active` → **63 PASS / 0 FAIL / 15 SKIP / 0 ERROR**, identical to the 12.44
reference row. 68 `applied` lines including `DustSicknessBiorobots`, zero
`[CommunityFixPack]` error/FAILED/disabled lines, no log line names our `Code/`,
known noise only (`objects_to_mark` 48, 2 `LawOfficeDoor`, the TestKit GameInit
nil-call pair). **It proves no cold-boot regression and nothing about the enable
path** — only the new leg can speak to that.

### 5. The enable-path leg RAN the same evening — and PASSED

19.09, owner ticking the box at the main menu. `fix pack present: 68/74 fixes
active` -> **63 PASS / 0 FAIL / 15 SKIP / 0 ERROR**. **The first measurement this
project has ever taken of a player's first session.**

The leg carried its own positive control, which is what makes the result
interpretable: `ENABLE-PATH: ARMED — the pack is OFF` at boot *before* the click
and `ENABLE DETECTED — the pack loaded through an in-place mod reload` after it,
with `95_AutoRun` logging `standing down` so the `-smrautorun` command line
provably did not start a colony pack-less. The log carries the F87 fingerprint
exactly — two reload cycles in one process, `…TestKit` then
`…TestKit, …CommunityFixPack` — the same shape as the log that caught the
defect, now with zero errors.

The decisive line is `DustSicknessBiorobots` **PASS** — *"all 4 infection effects
filter Biorobots out"*. That probe reads the LIVE preset data, so it proves the
data patch really ran on the path where `apply()` used to throw. Diffed
probe-for-probe against the 18.44 cold boot: **2 of 78 lines differ and both are
RNG, not path** (a different randomly generated mystery; 400 tourist rolls
landing 156/332 vs 160/312). Same noise profile, zero fix-pack error lines.

### 6. Repeated with every optional module ON — and two procedure facts learned the hard way

The 19.09 run had the toggles OFF, so all five `Opt_` probes SKIPped. Repeated at
19.24 with a temporary `Code/97_OptInLeg.lua` forcing `SMRFixPack_Optional`
(the bridge overrides an OFF toggle and never touches account state, so the owner
flips nothing): **`74/74` -> 68 PASS / 0 FAIL / 10 SKIP / 0 ERROR**, matching the
all-ON cold-boot reference exactly, all five optional-module probes PASSing on
the enable path.

**A sweep repair caught in the act.** The log carries
`[CommunityFixPack] MultipleSuns: Artificial Sun build-once limit lifted`. That
line comes from `lift_build_limit()`, which on this path is driven ONLY by the
new `SMRFixPack.OnDataReady` — before today it hung off `OnMsg.DataLoaded`, which
never fires here, and the limit simply stayed in place. So one of the three
casualties the sweep found is confirmed repaired *on the exact path where it was
dead*, not merely by inspection.

**Two procedure facts, both learned by tripping over them** (now in
`PLAYTEST_HELP.md`):
- **The leg's own click PERSISTS.** `ModsUIDialogEnd` calls `SaveAccountStorage()`
  (`ModManager.lua:132`), so the pack stays enabled in account state and EVERY
  run must disable it again first. I told the owner the pack was "still unticked
  from last time"; it was not. **The guard caught it** — `ABORT — the fix pack was
  already enabled at boot` — instead of quietly measuring a cold boot and
  reporting it as a first-run result. That guard paid for itself on its second
  outing.
- **The leg's first load-detector was WRONG.** It read the `SMRFixPack` global,
  which is rawset into the real `_G` and **survives a Lua reload**, so after the
  pack was disabled it still looked loaded and the leg logged ABORT where it owed
  ARMED. Replaced with a `ModsLoaded` scan, which `ModsReloadItems` rebuilds from
  scratch every reload. The irony is exact: that survives-a-reload property is
  the same one the leg's own SawPackOff marker deliberately relies on — which is
  precisely why it could not also serve as the detector.

### What is owed out of this leg

**Nothing on F87.** What follows is a correction to a claim this session spent the
evening repeating, and it is the more useful lesson of the leg.

The F87 entry said the enable-path leg "would also verify audit finding **A2**",
and I propagated that into STATUS, the prompt and PLAYTEST_HELP. When the 19.09
run came back with the toggles OFF I "corrected" the docs to say **A2 is still
owed** — compounding the error, because **A2 was never open.** PT-55 answered it
in play on 2026-07-30: *"all three hooks install and run on a first mid-session
enable, no relaunch"*, with per-module results, and the audit's own "one live
confirmation still worthwhile" caveat was retired then. A2 is also a **different
path** — the MODULE toggle flipped mid-session, not the PACK enabled at the main
menu — and its three modules are `Opt_ClassicRockets` / `Opt_ResidencyControl` /
`Opt_MultipleSuns`, not the set the entry implied.

Two failures compounded: the original claim was never checked against
`AUDIT_FINDINGS.md`, and the "correction" was written from the same unchecked
premise rather than from source. **The standing rule that caught it in the end is
the one already on the books — read the record before publishing a conclusion.**
Withdrawn in BUGS/STATUS/PLAYTEST_HELP/prompt, with the withdrawal stated
explicitly so it cannot be re-filed as owed. The toggles-ON leg ran anyway
(section 6) as **coverage**, which is what it actually buys.

---

## 🛑 PT-20 FAILED — WE LEAK EXECUTABLE CODE INTO PLAYER SAVES (F86, P1, blocks release) — 2026-07-31 late (live sitting, owner at the keyboard)

Started from `docs/prompts/FABLE_NEXT_PROMPT.md` at `84427e1`. The plan was PT-20 plus
the F74/F53(a) riders. PT-20's steps 1-4 passed; **step 5 — executed for the
first time — found a P1 defect in our own pack**, and the riders were dropped
because the leg proved they cannot be run on this colony at all.

### 1. Setting the trap (the part that made the answer interpretable)

`PT-20TEST` cut from the 288-sol `test 2i`. Positive-control reads with the pack
ON: `MeteorFrequency` `active`, `IsValidThread(Meteors)` `true`, heartbeat phase
`rolled`. Descriptor read: spawn 65 h (+0-25 h), warning **75 h — capped**, i.e.
this colony is tower-rich.

**Two dead ends, both killed by controls before they could produce a false pass:**
- `debug.getinfo` — proposed as an instant read of the thread's body. It is
  **unavailable in the mod sandbox**, which `ENGINE_FACTS.md:69` already recorded
  and the Test Kit logs on every boot (`no debug.getinfo … [install] probes will
  SKIP`). Should have come from the facts file; cost one console line.
- `Wakeup(Meteors)` — proposed to force the in-flight `Sleep` to resume. **It
  only wakes `WaitWakeup` sleepers** (`thread.lua:62-71`). The positive control
  (phase still `rolled` afterwards) caught it immediately.

**What worked:** compress the next roll to 2 h (`GetMeteorsDescr()` returns a
live preset table — `TerraformingDisasters.lua:54-99` returns `original` or a
sibling, no copy), `RestartGlobalGameTimeThread("Meteors")`, confirm the phase
advances to `long-sleep-done`, pause, save at sol 290. The next wake is then
bounded to ~2 game hours, so a null result would have been *interpretable*
rather than "maybe it hasn't woken yet".

### 2. The result — F86

Pack disabled in the Mod Manager, save reloaded:

```
[LUA ERROR] attempt to index a nil value (global 'SMRFixPack')
  Mod/SMR_CommunityFixPack/Code/Fix_MeteorFrequency.lua(106):   <>
Locals:  spawn_time | number 60000     <-- the value WE injected before saving
         hit_time   | number 60000
```

Our stack frame, with our local variables, came back out of the savegame. The
`Meteors` thread then died: **that colony gets no more meteors, permanently**,
and a save written afterwards carries the dead thread (`_fixup.lua:54-55` only
rebuilds when the save carries *nothing* for the name), so it does not self-heal.

Alongside it, **98** errors from `Opt_DroneOverhaul.lua(190)` via drone command
threads — **with its own opt-in toggle OFF**, because the wrapper installs at
file scope and only early-returns. Harm there is log-only: line 188 runs
vanilla's `Idle` to completion first, and drones were observed working normally.

**Mechanism:** a save captures every game-time thread **with its blocked stack**;
a mod function is serialised **by value** (not in `PersistGatherPermanents`), and
each mod env is a permanent (`Mod.lua:1642-1644`) which cannot resolve after
removal — `Unpersist missing permanent: Mod/SMR_CommunityFixPack | Fallback
permanent: table` — so the orphan runs with an empty `_ENV`.

**This voids an audit clearance.** The 2026-07-31 audit asked *where is the
function stored* and cleared class tables. `Drone.Idle` is a class-table write
and leaked anyway. The route is the stack, not the storage.

### 3. Controls (owner-directed escalation ladder)

Rung 1 — junction physically removed (`1 mods installed`, Test Kit only) —
**reproduced identically against the same save file**: 98 vs 98 drone errors, the
same single meteor error with the same locals; the only difference was the
engine's wording (`present, but not loaded` → `not present`). Rungs 2-3 (Steam
verify, reinstall) were stood down by agreement: no game-install state can invent
our injected `spawn_time 60000` inside our own frame. A repo backup was taken to
`B:\Dev mod backup\2026-07-31_pre-uninstall-test` (both mods, byte-verified)
before the junction was touched; junction restored afterwards.

**A false alarm worth keeping:** a `rawget` sweep found `GetPriorityForRequest`
on **192 buildings**. That is vanilla — `RequiresMaintenance.lua:94` flattens it
onto every instance that does not require maintenance (26 distinct per-class
functions, none equal to the base). Neither mod writes that member. Presence-based
orphan detection is useless here, and comparing against the class value
false-positived on all 192 — which hardens the cleanup mod's "leave identifiable
markers" condition with a failed attempt rather than a theory.

### 4. A second, independent finding — MODS DO GET A SAVE HOOK

`ModMsgBlacklist` (`Mod.lua:1430-1440`) blocks only `PersistSave`, `PersistLoad`,
`PersistGatherPermanents` and five non-save messages. A Test Kit probe
(`97_SaveHookProbe.lua`, temporary) proved it, with `OnMsg.LoadGame` as a
positive control:

```
[SMRTest][savehook] LoadGame FIRED (positive control)
[SMRTest][savehook] SaveGameStart FIRED — params=table: … SavingGame=true
[SMRTest][savehook] SaveGameDone FIRED — name=savesavetest.savegame.sav autosave=nil err=false
```

**This falsifies the recorded "mods get no save hook / tidying up on save is
unimplementable" fact** in `STATUS.md` and the D06 cleanup-mod argument, both now
corrected. Autosaves are the same path (`SaveAutosaveGame` sets one flag and
calls `DoSaveGame`, `Savegame.lua:1450-1453`) — so the hook covers them, and so
does the leak. ⚠️ Which is also the trap: autosaves fire ~once a sol, so a
tear-down that *restarts* a long loop would reset a 35–115 h timer forever,
recreating PT-01's silence from our own code. Re-arm from a persisted deadline.

### 5. F02's root cause, sharpened (owner asked)

Not "a dead `if`" — a **collapsed polling loop**. The fossil in
`Meteors.lua:280-283` is the loop that still exists intact 40 lines below in
`MeteorStorm` (`:319-341`): same `start_time`, same comparison, same `Sleep(5000)`,
but with the `while` removed and the loop body pulled inside the `if`.
`Min(spawn_time, warning_time)` is **not** the bug — it is the correct clamp, and
`DustDevils.lua:171` has it verbatim. Consequences: towers *accidentally repair*
the cadence (no towers → 6 h; several → 65-75 h), and sensor towers contribute
nothing to single-meteor warning because that comes from `Predict()` /
`prediction_time` (30 game seconds, tower-independent). **Owner decision: that 30
seconds is adequate; tower-scaled meteor warning is a feature and is declined.**

### 6. What this costs us

- **F86 blocks release** (FIX_POLICY §3 — the pack must never hold a save hostage).
- **12 modules exposed**, ~62 safe by construction (synchronous code cannot be
  captured — a save only captures *blocked* threads). Full list on the F86 entry.
- **`Fix_ShelterReflex` is the one to measure next**: it wraps `Colonist:Idle`
  like the drone leak but ends `return orig_idle(self, ...)`, a proper tail call,
  which should replace our frame. If that holds, it becomes a cheap coding rule
  for the whole wrapper class.
- **F74 and F53(a) are un-runnable on this colony** and the PT-20 bundling is
  retired: any save whose colony was ever played with the pack installed carries
  pack code, so switching the pack off does **not** produce a vanilla control.
  They need a colony that has never had the pack — a fresh 10-minute save.
- **Redesign proposed, nothing built, owner decision owed**: patch synchronous
  inputs instead of replacing blocking bodies (F02 then needs no body at all), a
  tail-call rule for wrappers, `SaveGameStart` tear-down for the remainder.

### 7. Tail end of the sitting — remedy PASS, a new defect, and a killed experiment

- **Remedy test PASSED.** Loading the damaged `PT-20TEST-B` with the pack
  reinstalled brought the dead `Meteors` thread back: `IsValidThread(Meteors)`
  → `true`, phase `long-sleep-done` (a fresh restart that has already cleared its
  1-second first sleep). **The answer for an affected player is "reinstall the
  mod" — real, and uncomfortable.**
- **🥇 A NEW DEFECT, caught by Phase 4's C1 dialog on its first non-synthetic
  outing — F87.** On re-enabling the pack, `Fix_DustSicknessBiorobots` **threw**
  at apply (`HasTrait:new` before class flattening — the third F64
  pre-flattening trap), so F40 was silently unfixed. Status `error`, not
  `inactive`, so it is a crash rather than a self-check latch — which also means
  the C1 dialog's "the game code they patch has changed" wording is wrong for
  this case. **Trigger pinned over three passes, and the first two were wrong** —
  mod load order (wrong), then a mid-*session* enable (wrong). Owner correction
  settled it: the mod was ticked **at the main menu**, and since a mod is never
  auto-enabled, **this is the path every player takes on their first run**.
  Ticking it makes the engine do an IN-PLACE MOD RELOAD, and our code runs inside
  it with presets already loaded — so an apply-time data patch that is a no-op at
  cold boot does real work during file scope, before class flattening. **F40 is
  dead for that whole session** and self-corrects only from the next launch.
  Same hazard class as audit finding A2 (which moved three `Opt_` hooks to
  file-scope install so a first enable works); the shared `DataPatch` scaffold
  was never covered. **And the harness has never tested the enable path at all** —
  every A/B leg starts with the pack already on, so all `74/74` figures describe
  the second session onward. **Owner instruction: this is the FIRST thing done
  next session.**
- **A planned experiment was cancelled rather than run, and the reasoning is
  worth keeping.** The plan was a purpose-built probe to measure whether a proper
  tail call keeps a wrapper out of the save. It is **unfalsifiable by
  construction**: a tail call has nothing after it, so a vanished frame and a
  surviving frame both produce silence, and adding a detector after the call
  stops it being a tail call. Working that through improved the rule instead —
  it does not need TCO at all. **"No mod code after a call that can block"** is
  sound whether or not the frame survives, needs no engine guarantee, and is
  checkable by reading the source. That is now the layer-2 rule in the spec.
- **Redesign spec written** — `docs/reports/SAVE_SAFETY_REDESIGN.md`: the three layers,
  the per-module disposition for all 12 exposed modules, the autosave timer trap,
  and the four decisions owed to the owner.

### 8. Housekeeping

Junction restored and verified (75 `Code/` files through the link) — **the pack
is still unticked in the Mod Manager and must be re-enabled**. The temporary
`97_SaveHookProbe.lua` is still armed in the Test Kit (local-only, never ships)
and should be removed once the autosave firing is confirmed on the keyboard.

---

## ALL FOUR DRONE RESEARCH GATES ANSWERED + F83 `tested` — 2026-07-31 (live playtest sitting, owner at the keyboard)

Started from `docs/prompts/FABLE_NEXT_PROMPT.md` at `4d0d453`. Two jobs came in ahead of
plan and a third emerged from a mistake.

### 1. PT-59 PASSED IN FULL → F83 `tested` (`8387aaf`)

- **(A) reload leg** — counters **1/1/1**, flag `true`, exactly one
  `recovered after a save/load (3 granted)` line; answering the re-shown popup
  left it at 1/1/1.
- **(B) healthy leg** — **1/1/1** with `SMRFixPack_FirstAsteroidPrefabs` still
  `false`. Vanilla granted; our code never ran. That is the double-grant guard.
- **(C)** — exceeded: the sitting logged **10 game loads against exactly 2
  grants**, 14 minutes apart, with **7 non-granting loads between them**.
- Unasked-for results: the heal **discriminated between two asteroid
  notifications** sitting in the corner list together, and **8 of 10 loads
  granted nothing** — the no-op path is the common one and it is silent.
- ⚠️ **The test's own procedure was WRONG and is corrected.** It never said which
  popup to answer; answering `ReconCenterDiscoveryAsteroid` yields `0/0/0`,
  indistinguishable from a fix failure, **and it was reported as a FAIL** before
  source settled it. Another instance of the standing rule that an un-run PT's
  procedure is unverified until executed once.

### 2. The four gates — ALL ANSWERED

- **Q3 + Q4 fell to SOURCE, not playtesting** (`cd37235`). **Q3a:** use the
  game's own class test `IsKindOf("AirProducer"/"WaterProducer")` — docstrings
  claim completeness — catching exactly five buildings; the property test the
  brief proposed would have **missed one**. **Q3b:** the Food-demand test alone
  catches six, two of which are *residences*; adding `ServiceWorkplace` gives
  exactly four. **Q4:** defaults are omitted from saves, five-step chain, and
  **no template in the game sets `priority`**. Live-confirmed both branches
  (`2708d24`): untouched `ShopsFood_Small` → `rawget` **nil**; after moving the
  arrow → **3**.
- **Q1 = HONOURED, both legs** (`add2d8a`, `663facf`). On a new game the hubs
  allocated `-1..5` natively. Two Stirling Generators at band 3 and band 4:
  band 4's work request ran `80000 → 50000 → 25000 → 0` and cleared. A **second,
  cheat-free symmetric pair** (equidistant, single hub, Polymers stocked) closed
  the **haul** leg — `demand_queues[4][Polymers]` inspected directly, both haul
  targets `1000 → 0` by drone delivery. **The band scheme survived the gate that
  could have killed it.**
- **Q2 = PERSISTED, answered by an accident** (`97a55fb`) — see below.

### 3. THE INCIDENT — the experiment module broke a live save (`d88dd11`)

v1 widened `const.TaskRequest.MaxBuildingPriority` at file scope and **asserted
in its own header that this was "inert"**. It was not. On an existing save every
`FindTask` threw, drones froze colony-wide while the UI reported "heavy load",
and the log took tens of millions of lines. **Nothing had been armed.**

Cause: `TaskRequestHub:Init()` allocates the queue tables at **construction** and
never again — so a restored hub carries `-1..3` while the widened const makes
vanilla's loops iterate `-1..5` and index nil. **That is the Q2 answer.**

**Three corrections to our own reference doc** fell out of it: the cited
`InitRequestQueues` **does not exist**; the claim that the game defines no
`const.TaskRequest` group is **false** (it exists and carries 3 — home not
determined, likely `Data.fpk`, which the parity extraction never covered); and
the hub population is **`DroneHubBase`, `RocketBase` and `RCRover`**.

v2 was rebuilt **safe by construction** — a queue top-up pre-wrapped onto all
seven entry points that index the queues — and ran clean.

### 4. The uninstall picture, and a NEW ENGINE FACT with pack-wide reach

- **Uninstall is safe, silent and LOSSY** (`6c05053`). A save with wide tables
  loading into narrow vanilla loops throws **nothing** — the mirror of the
  incident. But `demand keys: -1,0,1,2,3,4,5` persisted **with the module gone**,
  and 4 entries sat in a band vanilla never visits.
- **The heal path EXPIRES.** `DepositsSpawned` re-registers every hub, but fires
  only from a sector scan that places deposits, and sector status is a one-way
  ladder — **no re-scan on a fully-explored map**. Owner's framing, and it is
  right: clearing the map is an early act, removing a mod is a late one.
  **The hub UI toggle does NOT re-register** (measured).
- 🆕 **ENGINE FACT** (`988b0a8`): **a mod-authored closure stored on a persisted
  game object goes into the save, survives uninstall, and KEEPS RUNNING** —
  `rawget(obj, "GetPriorityForRequest")` returned `function: 000001E95D57A6B0`
  with the module uninstalled, and it re-filed queue entries using the vanished
  mod's logic, **with zero errors**. Pack audited: 5 of 6 sites cleared (UI
  windows, class tables); **`Fix_MeteorFrequency` is unresolved** and PT-20 now
  carries a mandatory step 5 naming it (`93bbf47`).
- 🆕 **The duplicate leak** (`93bbf47`, `DRONE_PRIORITY_SYSTEM.md` §10): a
  reconnect healed the building but took band 4 from **4 → 6**, because
  `DroneControl:RemoveBuilding` is bounded by a **file-local** pinned at 3.
  **This happens with the mod installed and working** — it is a defect of the
  band design, not of uninstall.

### 5. Owner decisions taken this session

- **A save-safety wall RELOCATES the overhaul, it does not kill it** (`1e19056`).
- **THE CLEANUP MOD** (`cae4eec`) — supersedes forced-standalone. Mods get **no
  save hook** (`PersistSave` blacklisted) and cannot run after their own removal;
  a second mod is the only thing that can occupy that window. Framed by the owner
  as a **beta response channel**, and as a capability rather than a backlog.
- **A possible PACK SPLIT is UNDECIDED and deliberately so** (`2ee9745`) — not
  owed, not scheduled, and may not gate anything.

### What this leaves for the next session

The band scheme **passed** its decisive gate but picked up **two constraints that
did not exist when it was drafted** (§9 uninstall, §10 duplicate leak), and the
`-1..3` fallback now has two independent arguments in its favour. Both are
written up neutrally; **no side has been picked. That is a design decision for a
fresh session.**

---

## PHASE 4 COMPLETE — C2 helpers + C4 deeper self-checks + C1 update report, CERTIFIED — 2026-07-31 (one-off PHASE4_REBUILD_PROMPT session, 11 unattended legs)

Executed `docs/PHASE4_REBUILD_PROMPT.md` (deleted on completion per its own
rule). Preflight design record: `docs/archive/PHASE4_PREFLIGHT.md`. Control
fingerprint: `docs/archive/fingerprint_before.txt`; end-state fingerprint:
`docs/archive/fingerprint_after.txt`.

### THE CERTIFICATION — every claim with its evidence

**What was measured, and what it read.**
- **Control** (before any edit): leg `Mars.exe-20260731-11.43.28` —
  all-six-toggles-ON + carry dial off base (read from the leg itself),
  `74/74 fixes active`, **67 PASS / 0 FAIL / 10 SKIP / 0 ERROR** at 77 probes.
- **Eight build stages, one commit + one leg each**, every leg diffed
  line-by-line against the control (verdicts, per-probe ids, all
  `[CommunityFixPack]` lines, reason strings):
  S1 helpers `67a744c` leg 11.47.23 · S2 log clones `eb06e31` leg 11.50.40 ·
  S3 SetGlobal `6b4a555` leg 11.53.21 (its commit message mis-cites the leg as
  "12.01" — written from memory; the fingerprint header carries the true name;
  the counts stated are correct) · S4 WhenActive `2e1bf88` leg 11.57.28 ·
  S5a DataPatch+Dust pair `6f90161` leg 12.00.22 · S5b donor+Independence
  `ad7f7e1` leg 12.03.14 · S6a-d Require waves `d28bf4c`/`b5f172c`/`7203a55`/
  `21a1a8d` legs 12.09.00/12.13.40/12.18.14/12.23.32 — **all EIGHT identical
  to the control**, modulo exactly four documented random-input probe messages
  (TouristApplicants roll counts, CrystalMysteryHang current mystery,
  FounderTraitNotification random trait, BombardmentSpread volley directions —
  verdicts always identical) and the log's own timing suffixes. · S7 C1
  surface `79a8e92` leg 12.28.05 — **68 / 0 / 10 / 0 at 78 probes**, the
  numbers predicted before the run; diff vs control is exactly the new
  `UpdateReport` PASS line + the summary counts.
- **Final fresh legs** (assembled result, from scratch):
  all-toggles-ON leg `Mars.exe-20260731-12.30.34` — `74/74`,
  **68 / 0 / 10 / 0** at 78 probes, identical to S7's fingerprint;
  baseline leg `Mars.exe-20260731-12.32.11` (`code` list emptied via the
  saved-copy discipline, restored and hash-verified `4dab1410…`, nothing
  committed while the edit was in the tree) — **1 / 62 / 15 / 0**, the 1 PASS
  is the FactionFundingCheck canary and the new `UpdateReport` probe **FAILs**
  as `fix pack not loaded (bug reproduces)`, proving it discriminates.
- **✅ The default-config leg RAN the same sitting** — the owner set the six
  toggles OFF + dials to base on request and leg `Mars.exe-20260731-12.44.39`
  read **`68/74`, 63 PASS / 0 FAIL / 15 SKIP / 0 ERROR** at 78 probes — the
  numbers predicted above before the run, landed exactly. Six
  `inactive (opt-in module …)` lines (the healthy default signature, six not
  five because DroneOverhaul reports status without a probe), zero
  error/disabled/FAILED lines, the D09 probe reporting the **carry dial AT
  BASE on entry** — the account is genuinely clean again. Fingerprint:
  `docs/archive/fingerprint_after_default.txt`. **Both shipping
  configurations are measured post-Phase-4; nothing is owed on the harness
  side.** (For the record: at certification-writing time this leg was owed —
  the account had been all-ON throughout the build, the account-state
  lesson's third earning in two days, and the opt-in bridge is one-way ON.)

**Invariants verified, and how.**
- Reason strings preserved byte-for-byte: legs cannot see a passing check's
  reason, so every wave carried a static extract-and-diff of string-return
  sites against HEAD (0 missing everywhere; the only flagged items were the
  checker's own em-dash decoding artifact — verified intact in the files —
  and concat-loop reasons the helper now generates identically).
- Declaring-class rule: every migrated method check re-verified; three
  suspicious sites resolved — ShelterReflex's Community.HasLifeSupport check
  is CORRECT (MicroGHabitat.lua:4 lists Community as a parent of the live
  class), MoraleComfortTooltip's dead Colonist.GetProperty limb became the
  real PropertyObject check, TrainWaitTime gained the two never-checked
  station-method checks (Station.RemoveColonist, Station.lua:770;
  TransportStatistics.AddSpentTime, TransportStatistics.lua:31).
- Handler gates: WhenActive carries BOTH FIX_POLICY §2 checks; no handler
  lost its gate; the by-design ungated handlers (MysteryEnd, the two watchdog
  state resets) and the probe-visible verdict functions were left untouched.
- `%` escaping: centralised in SMRFixPack.Log — the 12 clones and 5 inline
  variants are gone; output byte-identical.
- No `rawset(_G, …)` introduced anywhere; the two previously-unverified
  global installs gained the standard read-back.
- Packaging: metadata `code` (75) and items.lua `ModItemCode` (75) identical
  in content and order (script-verified after the final leg).
- Probe-authoring audit: 78 `Register(` across 8 files, every file with ≥ as
  many explicit `return "PASS"` sites (10/10, 20/21, 18/18, 12/12, 7/7, 3/3,
  2/3, 6/6).
- Mod-environment API: the helpers use only APIs the pack already used, plus
  three engine globals new to the pack — `GetPreGameMainMenu` (the TestKit
  autorun's proven poll target), `WaitMessage` (the engine's own mod-error
  dialog surface, Mod.lua:2229-2243) and `RealTime` — none on the
  ModEnvBlacklist (ENGINE_FACTS sandbox entry).

**What shipped.**
- **C2**: `SMRFixPack.Log` / `Require` / `SetGlobal` / `WhenActive` /
  `DataPatch` in 00_Core; 58 files migrated onto them (11 log clones, 12
  global installs, 16 handler gates, 4 DataPatch scaffolds, ~60 Require
  preflights). The F75/B3/A1 lessons and the PT-51 detail rule now live in
  the runner, not in per-file copies. A failing declaring-class check now
  gets a loud `__parents`-walk diagnosis naming the true declarer, so the F64
  failure mode can no longer masquerade as a game update.
- **C4**: the EXIST-only tier enumerated (42 modules, criterion in the
  preflight doc); bare-global indexing rawget-guarded through the helper
  everywhere; the IndependenceTerraforming missing-target latch added (it
  previously reported `active` forever if a future patch removed the tech —
  the B3 gap); the deepening items above.
- **C1**: `SMRFixPack.UpdateSuspects()` + a pregame-menu `WaitMessage` dialog
  shown ONLY when ≥1 fix deactivated over a game-code change (status
  `error`, the `update_suspect` mark, or the target-changed/install-failed
  detail conventions; opt-in / Mod-Options-off / verified-already-correct
  are never reported). This title never fires `Msg("PreGameMenuOpen")`
  (its init.lua replaces OpenPreGameMainMenu without it — the audit's cited
  engine precedent is dead code here), so the surface polls
  `GetPreGameMainMenu()` the way the TestKit autorun does. The dialog is the
  engine's own gamepad-native message surface, so it reaches console players
  — the pack's first failure surface that does (FIX_POLICY §7).
- **NOT shipped, by preflight decision** (`9f51f52`): the shared watchdog
  skeleton (F02 and F78 are different mechanisms — heartbeat-vs-signature —
  and consolidating them removed ~zero duplication at maximum risk); force-
  fitting the three divergent DataLoaded scaffolds (TechDescriptionBuilding,
  Opt_MultipleSuns, FirstAsteroid's latch); Require for the three
  partial-install applies (ShelterReflex, StorageRateModifiers,
  SequenceLatents — their per-target semantics are not gate-or-die). C3
  merges were never in scope (BARRED). The three drone modules
  (Opt_DroneOverhaul, Opt_DroneStatDials, Fix_ExtenderFlapChurn) are
  untouched per the carve-out and verified present in every fingerprint.

**What this certification does NOT claim.**
- **NOT "no behaviour changed."** Probes drive planted globals; a stand-in
  cannot reach a game file that localised a global at load time. What IS
  claimed: every fix still applies, still reports the same status, detail
  and reason string, and every probe returns the same verdict, in the
  all-toggles-ON and baseline configurations, across eleven legs.
- **Nothing here is playtested on a real colony or a real save.** Owed:
  the default-config leg (above) and normal play regression exposure.
- **C4's deeper checks are untestable against a future patch today, by
  construction.** They would catch a renamed/removed/reshaped target at the
  moment it happens; they would NOT catch a same-named function edited in
  place — and neither can C1's report, whose dialog text says so.
- **Residual risk, named plainly:** a consolidated code path whose behaviour
  differs only on a real colony state the harness cannot plant — the most
  exposed candidates are the WhenActive-gated LoadGame/PostLoadGame sweeps
  and the DataPatch-run preset passes (identical fingerprints prove their
  load-time behaviour, not their mid-colony behaviour). What would close it:
  one ordinary play session with the log checked afterwards (zero
  `[CommunityFixPack]` error lines, fixes still `applied`), plus the owed
  default-config leg. The after-every-patch extraction diff (WORKFLOW.md)
  remains the only true re-verification for the ~29 pinned replacement
  bodies.

**Deliberate deviations from strict preservation** (all fail-path-only,
invisible in every measured configuration, itemised for the record): the two
outlier installs' new read-back failure strings; AcknowledgedWarnings'
sequential (vs batch) install verification; the WhenActive veto re-read on 14
handlers that previously checked status only (newly effective only for a
mid-session console veto — FIX_POLICY §2's stated intent); DataPatch's heal
guarded against `"disabled"`/`"error"` where LastTransmission's was
unguarded (unreachable difference); Independence's new missing-target latch
reason; ClassicRockets' first-vs-last failing-name report when multiple
targets vanish at once.

---

## F83 BUILT — the First Asteroid prefabs are recovered on load — 2026-07-30 late (build session, unattended harness leg)

The headline task the previous session queued. Read the audit (§1-§3, §7), the
F83 entry and FIX_POLICY first, then verified **both** candidate shapes against
Src before writing anything, per the corrected brief.

**What Src confirmed (the trap is real).** `ShowPopupNotification` early-returns
on a `show_once` preset already shown (`PopupNotification.lua:249-251`) —
returning nothing — and `WaitPopupNotification` then takes neither `WaitMsg`
branch but still reaches `procall(callback, res)` (`:302-304`). So vanilla's
grant callback runs unconditionally, and a naive additive handler that also
grants would pay **2/2/2** on the healthy path. Both candidate shapes were
therefore judged on how they avoid that, not just on whether they heal.

**SHIPPED: shape (i), the load-time heal** —
`Code/Fix_FirstAsteroidPrefabs.lua`, Register id `FirstAsteroidPrefabs`
(FIX_POLICY §1.2 additive handler + §3's sanctioned one-shot sweep). On
`LoadGame`, if the FirstAsteroid popup notification is still in the persisted
`Notifications` table — the only state a dead real-time waiter can leave — the
sweep **removes** it, **grants** the three prefabs through the shipped
`ColonyAddPrefabs(..., 1, nil, MainCity)` calls in the shipped order,
**latches** a persistent flag, and **re-shows** the popup as pure display so the
player still gets the story text. The healthy path is never touched: no reload
means no `LoadGame`, so the trap is unreachable rather than merely guarded.
Removing the notification is load-bearing, not tidiness — its `PressFunc` is the
only thing that can re-queue the dead context, so exactly one grant path exists,
and that stays true even if a future patch moves the shipped waiter to a
game-time thread (where it would persist and still be listening).

**REJECTED: shape (ii), the `show_once` pre-mark.** The mechanism is real and
was confirmed in Src, but its correctness rests on OnMsg handler order **and**
on `CreateRealTimeThread` not running its body during the Msg dispatch — a C
export whose scheduling Src cannot settle, and losing that race shows the player
two corner notifications. It also moves the grant off the healthy path for every
player (prefabs at spawn instead of on answer) and cannot heal a save already
sitting stranded — which shape (i) does, including the owner's own PT-58
fixture. Reasoning recorded in the fix header, per the brief.

**Correction to the audit's own build note.** It advised matching the
notification by the preset's T loc-id via `text[1]`. That works only in a dev
build: `T()` returns **light userdata**, not a table, whenever the id is in the
translation table (`localization.lua:268`) — the retail case. The fix uses
`TGetID` (`:48-65`), which handles both forms, and reads the id from the **live**
preset rather than hardcoding it. (The related caveat the audit got right: the
preset id is genuinely absent from the instance — `ShowPopupNotification` nils
`instance.id` at `:286` because `AddNotification` asserts an id-less instance.)

**Savegame footprint** — one GameVar, `SMRFixPack_FirstAsteroidPrefabs`. Checked
end to end that a mod-declared GameVar is safe in the sandbox: `GameVar` writes
the real `_G` and `PersistableGlobals` (`lib.lua:1040-1055`) regardless of
caller, `ModEnvMeta.__newindex` explicitly permits writing a name registered
there (`Mod.lua:1559`), and `OnMsg.PersistLoad` only restores names still listed
in `PersistableGlobals` (`persist.lua:135-142`) — so a save made with the mod and
loaded **without** it simply ignores the stray value (§3).

**Probe + harness.** New TestKit wave file `56_Probes_Wave7.lua` (**probes
76 → 77**) driving the real sweep against planted globals over three legs:
stranded (must grant 1/1/1, remove once, re-show once, latch), already-healed
(must grant nothing — the no-double-grant assertion), and a decoy
non-FirstAsteroid popup (must grant nothing and must not latch). Unattended leg
`Mars.exe-20260730-23.29.22`: **`74/74` active, 67 PASS / 0 FAIL / 10 SKIP /
0 ERROR**, the predicted arithmetic exactly; zero `[CommunityFixPack]`
error/disabled/FAILED lines; no log line names our `Code/`. **Baseline leg**
`Mars.exe-20260730-23.46.39` (`code` list emptied, `default_options` kept):
**1 / 61 / 15 / 0**, with `FirstAsteroidPrefabs` **FAILing** as
`fix pack not loaded (bug reproduces)` — which is the whole point of running it,
since a probe that PASSes on baseline is measuring nothing (the wave-6
probe-authoring trap). metadata.lua restored from the saved copy and re-verified
against items.lua. **`items.lua` also needed its own `ModItemCode` entry** for
the new file, in the same order as the `code` list — without it an editor
round-trip would regenerate `code` without the fix (audit A3); `last_changes`
recounted 66 → 67.

**The account-state trap bit again, and then closed.** The 23.29 leg came up
`74/74`, i.e. **all six toggles were ON** — the previous prompt's "owner left
all six OFF" had gone stale during the PT-58 sitting, and the D09 probe reported
the carry dial off base too. That made 23.29 the all-toggles-ON configuration
and left the default-config leg owed, which the one-way opt-in bridge (ON only)
cannot supply. **The owner set everything back to base at the end of the night
and the leg ran immediately after** (`Mars.exe-20260731-01.37.22`): **`68/74`
active, 62 PASS / 0 FAIL / 15 SKIP / 0 ERROR** — predicted before the run and
landed exactly, with the D09 probe reporting the carry dial **AT BASE** on
entry. `FirstAsteroidPrefabs` PASSes in this configuration too, confirming the
fix is toggle-independent (it is default-on, not an opt module). Six
`inactive (opt-in module …)` lines = the expected healthy default signature.
**All three post-F83 legs are now on file and nothing is owed on the harness
side.** Standing lesson, unchanged and now twice-earned in one day: read the
account state from the leg's own `fix pack present: N/74` line, never from a
doc.

**Docs:** BUGS.md F83 → `fixed` in both places with a full build record;
**PT-59 filed** in the checklist (§3) with three triggers — reload leg 1/1/1,
healthy leg still 1/1/1 (the trap guard), and reload-twice still 1/1/1;
MOD_DESCRIPTION player line; STATUS counts to 75 files / 74 modules /
68 default-active / 77 probes.

---

## The popup/deferred-consequence audit — the storybit alarm OVERTURNED, F83's narrow decouple REINSTATED — 2026-07-30 (one-off session, unattended, game not launched)

Ran `docs/POPUP_AUDIT_PROMPT.md` (deleted on completion). Deliverable:
**`docs/reports/POPUP_CONSEQUENCE_AUDIT.md`** — full enumeration of every path where a
player-visible consequence is applied after a wait, classified by save/load
survival. Headline: **the lead that stopped the F83 fix was wrong about the
engine.** A `CreateGameTimeThread` does NOT need `MakeThreadPersistable` —
**game-time threads persist by default with their full blocked stacks
(`WaitMsg`/`WaitWakeup`/`Sleep` are registered persist permanents "found in the
thread stack"); only real-time threads die on load.** Three source proofs
(XWindow clears the flag on a maybe-GT thread; `_fixup.lua` sets it only on the
RT twins and expects GT globals to arrive through the save;
Notifications.lua:214 flags only its RT variant) plus the everyday observed
fact that bare-GT unit command threads resume mid-command after every load.
Now an ENGINE_FACTS entry, alongside a second keystone: **every shipped popup
is async** — `ShowPopupNotification` opens with `assert(not bPersistable) --
we don't support these`, so the "persistable popup" branch the save handler
preserves is dead code and an OPEN popup's queue context never survives a load
(shielded in ordinary play because open popups are modal + game-pausing +
shortcut-eating; the shield is UI reachability, not the save system).

Consequences: **storybits, mysteries, anomaly sequences and challenges are
save-safe by design** (the storybit notification window even has a
forced-popup timeout backstop; no shipped scenario sequence is `real_time`;
the sequence system ships a watchdog that restarts abnormally-dead sequences).
**F06 is NOT an F83-family member** — one-shot `Msg` race, no save/load
involved, fix stands (entry note added). The real family is "consequence owned
by a REAL-TIME popup waiter": F83's two consequential sites + cosmetic
dead-View sites + a latent shielded class now filed as **F85** (breakthrough
choice popups ×3 grant `SetTechDiscovered` after an RT wait; the Assembly
"Colony Values" popup runs the ENTIRE politics init after one; all
open-immediately/modal, so tier **U** with a named settling observation — the
rebind-quicksave-to-F9 check, since `PopupPropagateShortcuts` lets F9/F11
through the modal layer and Quick Save is bindable). Also recorded: the one
`dont_pause` popup (distress call) admits sol-tick autosaves under it — the
popup itself is self-healing, but a second popup queued behind it at that tick
would be dropped with its GT waiter stranded (R3-edge, documented, no fix).

**F83: hold lifted, option 1 (narrow `OnMsg.SpawnedAsteroid` decouple)
REINSTATED as recommended — decision owed to the owner.** Entry corrections
from the audit: the eighth callback site (`ColonyViability.lua:260`) is GT +
open-immediately (safe, delisted); the `AnomalyAnalyzed` wait is commented out
in Src (dead site). **Needs-eyes list (4 items, audit §8):** (1) storybit
save/load in the notification window — the audit's one load-bearing inference,
~5 min console check; (2) Detailed Scan recoverability — grades F83's second
site; (3) the F85 rebind save vector; (4, optional) autosave under the
distress popup. No unattended game legs were run: the keystone fact has
observed corroboration, and every remaining question needs a keyboard.

**Rider repair:** the F84 filing commit (`21b92cb`) had spliced F84's last line
into the `### D06` heading, leaving D06's whole entry living under F84 —
heading restored in place, content untouched. Index 92 → **93 rows** (F85).

**Addendum, same evening — THE OWNER GAVE THE BUILD GO** (*"update the fable
next prompt to review and action on your findings"*), recorded on the F83
entry, STATUS and the next-prompt board. While writing the build brief the
session caught a **double-grant trap in option 1 as originally recorded**:
`WaitPopupNotification` procalls its callback even when `ShowPopupNotification`
early-returns on `show_once` (`PopupNotification.lua:249`, `:302-304`), and the
FirstAsteroid callback grants unconditionally — so "grant in our own additive
handler behind a flag" would pay 2/2/2 in the healthy no-reload path (the
entry's "the flag already stops a double grant" was wrong: the flag gates only
our handler). The brief now offers two corrected shapes — (i) a conservative
LoadGame sweep granting only when the stranded notification is detected
(matched by T loc-id, not T identity), or (ii) a show_once pre-mark that makes
vanilla's own always-run callback grant at spawn with the popup demoted to
display — build session verifies both against Src and picks one. PT-59 (the
kept fixture A/B) gains a second assertion: the no-reload leg must still read
1/1/1, not 2/2/2.

---

## Four PTs closed, two defects filed — and the F83 fix STOPPED by an owner question — 2026-07-30 (late evening, attended)

Continuation of the evening sitting below. **PT-58** (F83's consequence:
`1/1/1` vs `0/0/0`), **PT-44** (F23 → `tested`), **PT-25** (F38 → `tested`), on
top of **PT-56** (D09 → `tested`). Two new entries: **F83** (P2, proven) and
**F84** (P3, proven — the Universal Tunnel description is wrong twice).

**PT-25 is the one worth re-reading.** Its setup line said "SAVE-B / underground
access". The tester opened the underground build menu, found **no tunnel at all**,
and asked whether the premise was flawed — the same question that killed F24 and
F49(c). Half right: tunnels are a **surface** building (`UniversalTunnel` is the
only one in a player-facing category; `Tunnel` and `TrackTunnel` are `Hidden`),
so the underground reference was pure mis-specification — **fourth PT found
faulty by executing it**. But F38 itself held: the leaking sweep iterates
`TunnelBase`, and `UniversalTunnel` → `TrackTunnelBase` → `TunnelBase` with no
override. Corrected, run on the surface, passed all four steps including the
Rebuild over-reach guard. **SAVE-B retired** — its last consumer never needed it.
A free rider on that setup also disproved the tunnel's own description ("Rovers
cannot use this type of tunnel") → **F84**.

**Then the owner stopped a fix from shipping, and was right to.** F83's gate was
cleared and the narrow decouple was recommended and ready to build. He asked:
*are we 100% sure this is the only thing players can lose — what about anomaly
reports, mystery popups, story choices?* A first dive says the scope was drawn
too small:
- **`choiceN_func` is safe** — it runs in the UI action handler
  (`PopupNotification.lua:135`) before `host:Close(i)`, not in the waiting thread.
- **The return-value form of `WaitPopupNotification` is exposed exactly like the
  callback form.** The 8 callback sites are a subset of ~70 call sites; anything
  written after the wait dies with the thread.
- **Storybits are the likely real exposure**, and anomalies, planetary anomalies,
  mysteries and random events all route through them. `ActivateStoryBit`
  (`_StoryBits.lua:461`) spawns `run_thread = CreateGameTimeThread(RunWrapper)`;
  `Run()` posts a corner notification and waits; `OpenPopup()` then does reply →
  `StoryBitPayCost` → weighted outcome → `ProcessOutcomeEffects` → `Complete()`.
  Everything from the reply onward is after the waits. `g_StoryBitActive` is a
  persisted GameVar but `run_thread` has **no `MakeThreadPersistable`**,
  `OnMsg.LoadGame` only prunes dead presets, **no resume exists anywhere**, and
  `Unregister()` already ran so a stranded storybit cannot re-trigger.
  ActivationEffects run before the waits and are safe.
- **F06 was already an instance of this family** and nobody had connected it.

**The F83 narrow-decouple recommendation is RETRACTED and the fix is on hold.**
Fixing the asteroid grant alone would have papered over what looks like a general
defect — *player-facing consequences applied after a wait in a non-persisted
thread* — with the asteroid as its one proven symptom. A one-off audit prompt was
written (`docs/POPUP_AUDIT_PROMPT.md`): its own session, free to run unattended
A/B legs and add TestKit probes, explicitly barred from building any fix, and
required to separate observed from inferred. `FABLE_NEXT_PROMPT.md` now opens by
checking whether that file still exists.

**Lesson worth keeping:** the storybit exposure was reachable by grep the whole
time. It went unnoticed because F83 was scoped to the mechanism that produced the
*symptom* (a callback) rather than to the *shape* of the defect (consequences
after a wait). Scope a defect by its shape, not by the call form that surfaced it.

---

## PT-56 PASS IN FULL → D09 `tested`, D10 un-gated; and F83 filed from a surprise mid-setup — 2026-07-30 (evening, attended)

Live sitting with the tester at the keyboard, after the two unattended legs
below.

**PT-56 — PASS on all four steps**, on a one-speed-tech save (Low-G Drive only,
no Artificial Muscles), toggles off and dials at base going in. Baseline
`speed=1728 carry=1` · 2x/+1 → `speed=3168 carry=2` · back to base →
`1728/1` · **stale-save reconcile → `1728/1`**. The 3168 is the number worth
remembering: **+1440 exactly**, 100% of the 1440 BASE added additively beside
the tech — *not* a doubling of the live 1728. Log swept clean per PT-22 (zero
`[CommunityFixPack]` error lines; the only `Error` lines all session are the two
pre-existing `ResManager` `LawOfficeDoor` entries; four `MeteorFrequency
… restarting` lines are F02's watchdog across the sitting's four loads). D09 →
`tested`, section archived, **D10 workshops build un-gated**.

**Method lesson, paid for in this very test.** Step 4 was scored wrong first
time: it read `3168/2` and looked like a FAIL. The dials had simply not been set
back to base before the load, so the reading was correct behaviour. What caught
it was reading the **dial positions** alongside the values
(`Mods["SMR_CommunityFixPack"].options.DroneSpeedDial`) instead of the values
alone. Generalised onto the archived PT and the D09 entry: **for any dial test,
confirming the base state going INTO the load is its own step** — without it,
step 4 cannot distinguish a pass from a fail. Note this is the *third* time this
project has been bitten by account-persistent dial state in one day (the FAILed
probe, the 73/73-vs-67/73 leg, and now this).

**F83 filed — found by the tester mid-setup, and it grew.** A
`FirstFounderEnthusiast` popup arrived as a corner notification and its **View**
button did nothing. Chased live: the popup is a *scan* announcement of a founder
who already HAS the trait, so unrelated to F23/PT-44; the pack touches none of
this machinery; and `ViewAndSelectObject` called directly on the founder
**worked**, isolating the failure to callback delivery. A console repro of the
identical popup worked live, then the same repro left minimized across a
quicksave and load had its View die — tester verbatim: *"Correct view died after
a load."*

Mechanism: these popups always start minimized (`ShowPopupNotification` gates the
open-now branch on `start_minimized == false` and nothing ever sets it, so `nil`
takes the else branch); the waiter is a **real-time thread** blocking on
`WaitMsg(async_signal)`; neither the thread nor the async context survives a load
(`OnMsg.PersistSave` keeps only `sync_popup_id` entries) — **but the notification
does**. So after a reload it still opens, any choice signals nothing, and the
callback never runs.

**Eight call sites pass a callback; two are consequential.** `FirstAsteroid`
grants three Micro-G Auto Extractor prefabs its own popup text promises, is
`show_once`, and fires only at `asteroid_count == 1` — permanent silent loss.
`ReconCenterDiscoveryAsteroid` fires on *every* asteroid and its choice 2 is the
paid Detailed Scan, silently refused after a reload. The other six are dead View
buttons. Intent tell is self-contradiction (popup text vs delivery path);
reachability R1, reached organically before it was reproduced. **Honest caveat
recorded:** the mechanism is proven on the founder popup, the FirstAsteroid
consequence is *inferred* from identical code shape and is NOT observed —
**PT-58** added as the settling observation and gates any fix, per the F49(c)
rule. Nothing built; fix design is a user decision (recommended: decouple the
asteroid grant via an additive `OnMsg.SpawnedAsteroid`; a general popup-waiter
repair is not recommended). Family: same trap as F06.

The tester's current save had already met one asteroid, so it cannot serve as
PT-58's fixture — a fresh one is owed.

---

## The owed A/B ran and is CLEAR — and the D09 probe defect is repaired, not just recorded — 2026-07-30 (evening, unattended)

Session opened as playtest standby; the tester stepped away and released the
session for unattended work, so it took the two ⚠️ items at the top of the board
instead of waiting.

**The problem with the first item as written.** The board said: set both Mod
Options dials to base by hand, *then* run the owed A/B leg. That ordering exists
only because the D09 probe was broken — it read its baseline from the live
`g_Consts` value and asserted `base_carry + 1`, which is arithmetic against an
already-modified number whenever the account dial is off base. With nobody at the
keyboard the hand-flip was unavailable, and the leg would have FAILed again for
the same non-reason. **So the probe was repaired first and the precondition
disappeared.**

**TestKit repair** (`60_Probes_Opt.lua`, commits `ac30f54` + `e1d9bf1`). The probe
now reads the entry value, forces both dials to base through the real Apply path
(`rawset` on `Mods[pack].options` + `Msg("ApplyModOptions")`), takes its baseline
from *that* state, asserts that forcing base leaves no module modifier behind,
and restores the leg's entry values. Its tail cleanup check now compares the
restored const against the **entry** reading rather than against base, so it is
exact for any account dial state instead of speaking only when the account
happened to sit at base. STATUS had already written the remedy — *"it should
force base before measuring"* — this session just did it.

**Leg result (log `Mars.exe-20260730-19.20.24`, unattended via `-smrautorun`,
~70 s):** `fix pack present: 73/73 fixes active`, **76 probes, 66 PASS / 0 FAIL /
10 SKIP / 0 ERROR**.
- The counts land exactly where the F28 removal predicted (73 registered, 76
  probes), which is what the leg owed.
- **The dial probe went green with the account carry dial still at +1** — the
  exact state that FAILed it on the 17.25 leg — reporting `carry +1 over
  probe-forced base 1`. The repair is verified against the failing condition,
  not merely against a clean one.
- Zero `[CommunityFixPack]` error / inactive / disabled / FAILED lines; no log
  line names our `Code/`; noise profile identical to 17.25 (same 2 pre-existing
  `ResManager` `LawOfficeDoor` animation errors, same shutdown-artifact
  `[mod] Error in mod … Test Kit`, `objects_to_mark` 48→59 with the random map).
  The `LawOfficeDoor` pair was not previously on the documented noise list; it is
  now, having been shown present in both legs.
- The account still had all six toggles ON, hence `73/73` and not a
  default-config `67/73`. **A default-config leg has still not been run since
  the removals** — it needs the six turned off by hand, so it stays a keyboard
  item.

**Harness health check while the leg ran:** the falls-off-the-end-returns-SKIP
trap was re-audited across every probe file (`Register(` vs `return "PASS"`
counts). Clean — 10/10, 20/21, 18/18, 12/12, 7/7, 3/3, 6/6. Nothing is sitting
in that trap.

**What did NOT change.** D09 is still **not** `tested` — only the playtest flips
statuses, and PT-56's stale-save reconcile step is beyond any probe. **PT-56 also
still needs both dials set to base by hand**, because its step-1 baseline reads
come from the live game; the repair removed that precondition from *A/B legs*
only. The board's ⚠️ A/B item is now done and can come off; the ⚠️ dials-to-base
item survives as part of PT-56 itself.

### Second leg the same evening — the default configuration, and a self-inflicted blind spot found

The owner then set **all six toggles OFF and both dials to base** by hand — the
one thing the opt-in bridge cannot do, since it ORs with the saved toggles and
can only force a module ON. Leg run unattended immediately after, with the
expected result **stated before the run** so it could fail: log
`Mars.exe-20260730-19.32.16`, **`67/73` active, 76 probes, `61 PASS / 0 FAIL /
15 SKIP / 0 ERROR`.** It landed exactly. The five opt-module probes flip
PASS→SKIP as `inactive (opt-in)` — five, not six, because D06 has no probe of its
own — turning 66/10 into 61/15 with FAIL and ERROR still zero. `DroneStatDials`
and `OptionsMenu` both stay PASS, so the dials and the Mod Options wiring are
confirmed toggle-independent **in the shipping default configuration**, not just
with everything switched on. The six `[CommunityFixPack] … inactive (opt-in
module …)` log lines are the healthy default-config signature, not errors — six
here, not five, because DroneOverhaul reports its status despite having no probe.
Same noise profile a third time.

**The blind spot the leg exposed, in this session's own work.** Making the dial
probe immune to account dial state also made it *silent* about it — and that
silence costs something real, because the old broken probe's FAIL text
(`DroneResourceCarryAmount 3 → 2 (want 4)`) is precisely how the project learned
a playtest had left the carry dial at +1. A green leg now proves nothing either
way about the account, while **PT-56's own baseline reads still depend on it**.
Fixed the same evening (`e605ba6`): the probe compares its entry reading against
the base it forced and reports `account carry dial AT BASE on entry` or `OFF BASE
on entry (const N vs base M)`. Immunity for the verdict, visibility for the
human. General shape worth remembering: **when you make a check robust to some
ambient state, ask what the old fragility was accidentally reporting.**

Docs: STATUS A/B table + account-state block rewritten (17.25 compressed to
history), BUGS D09 entry item 2 flipped to repaired-and-verified with the new leg
recorded, PT-56's warning block corrected so it no longer tells the tester a
repaired defect is open, TestKit README's "Known probe defects" entry updated.

---

## HARD RULE: vanilla only, never other mods (FIX_POLICY §4a) — F28 retired under it — 2026-07-30 (late)

**The owner set a standing rule**, prompted by asking a simple question about
F28: *why did we build a "replace tech" fix when we have never replaced a tech?*

> *"This mod does not fix bugs caused from other mods. No agent should assume it
> does at any point going forward. The only way that should be able to be
> changed is if an agent specifically asks me to override as a one-off for
> something I specifically ask for."*

Recorded verbatim as **FIX_POLICY §4a**, with the corollary that actually occurs
in this tracker written out explicitly rather than left to interpretation: a
**vanilla bug reachable only from mod code is not a player fix and does not
ship**. The override procedure is the only one permitted — explicit ask, explicit
yes, one case, never inferred and never carried forward. Existing shipped fixes
are explicitly declared NOT precedent.

**Whole-tracker scan first, because setting the rule is only half of "don't slip
more in".** Exactly two shipped fixes rested on a mod-facing rationale: **F28**
and **F29**. (F34(b) is labelled mod-facing but was never actioned; F42 is
already `wontfix`.) Bounded blast radius.

**F28 retired under the rule.** The answer to the owner's question is that it was
**never an oversight** — the entry's second line said *"No vanilla caller; hits
mods/storybits/console"* the day it was filed, and it shipped anyway on a
"modder benefit" rationale. So F24 was an *error* (nobody knew it was
unreachable); **F28 was a decision, and the rule reversed it.** Independently
re-verified before deleting: the whole-tree grep over `Lua/`, `Data/`,
`CommonLua/` and `DLC/` returns exactly one `ReplaceTech` hit — the definition
at `Research.lua:684`.

Removed: `Code/Fix_ReplaceTechCount.lua`, its `metadata.lua` and `items.lua`
entries, the README row, and the `ReplaceTechCount` probe. **The probe had to go
too** — it drives the real method and asserts the *fixed* counter, so with the
fix gone it would FAIL in every leg. Recorded on the entry that it could later
be rebuilt as a vanilla canary on the **F10 precedent**, which is what
`FactionFundingCheck` became after F10's deletion; not done, because that is new
assertion code nobody asked for.

**Counts: 74 → 73 registered, 68 → 67 default-active, probes 77 → 76.** A fresh
A/B is **OWED** — unlike F24, this one moves the probe numbers. Also caught while
recounting: `metadata.lua`'s player-facing `last_changes` still advertised "68
bug fixes"; it derives as Fix_ files + the sanitizer and is now **66**, with the
derivation written into a comment so it stops drifting silently.

**F29 flagged — then UN-flagged the same evening, and the mistake is mine.** I
flagged it on the strength of its own words ("mod-facing bundle", "ship for
modder benefit", "No shipped user"). The owner asked the obvious question —
*what does F29 actually do?* — and reading the audit's enumeration to answer it
showed **the entry's self-description is false**: item 1 has **four shipped
callers**, all in Mystery 2 "Dredgers", all executing live in every playthrough;
item 3 runs for every digger that mystery spawns. Both are benign only because
the shipped *data* is benign (default sampling params; already-ordered timings).
That is **R3 latent-by-data**, not mod-only — same shape as F27/F31/F43. **KEPT.**

I made the exact error the audit made on F49(c): **trusted an entry's own
framing instead of the enumeration sitting right there.** There it was about
intent; here it was about provenance. §4a now carries the warning explicitly.

**The owner's clarification is what settled it**, and it is now the rule's
operative test: *"I don't want to fix things for other possible mods. But if
it's game code that could cause real problems for users now or in the future
even if they can't expressly see the issue, that is a real fix."* Ask **who
benefits**, not how visible the harm is. Invisible, latent and
nobody-has-complained are all irrelevant. Operationally it lands exactly on the
**R4/R3 boundary**: R4 needs new *calling code* to go live (only a mod can
supply that — barred); R3 needs new *data*, which ships with patches, DLC and
story content (player territory — allowed). So the rule retired **F28 alone**.

F29's one genuine open question is unrelated to §4a: it is R3 implemented as two
**§1.5 method replacements**, the combination the *pending* §4 amendment would
put to the owner. Paired with F57(a) in that bucket. No action unless a stricter
line is wanted.

---

## F49(c) removed; post-removal A/B leg run unattended — 2026-07-30 (late)

Owner away; work done to standing instruction, with two decisions deliberately
left untouched (below).

**F49(c) closed `wontfix`, guard removed (`d03417b`).** Full reasoning on the
F49 entry. The short version: the tester established at the keyboard that
salvage mode targets objects not hexes, the cursor always names its target
(bare red `Salvage` = no action permitted), the
`Salvage Train Station`→`Salvage Track` handoff is seamless to the millimetre,
and **no exposed control separates a station from its own connector track**.
The propagation item (c) called a defect is what makes that boundary
continuous — it is designed. Had the guard engaged it would have carved a dead
band into it. Removed the pre-guard, its apply-time self-check and the title
clause; (a) and (d) untouched; file parses; README never described (c).

**Post-removal A/B leg — code gate CLEAR.** Unattended, log
`Mars.exe-20260730-17.25.32`, 65 s. **74/74 fixes active** (exactly one fewer
than the pre-removal 75/75 = the F24 deletion), **zero `[CommunityFixPack]`
error/inactive/disabled lines**, probe total still 77. Result
**66 / 1 / 10 / 0**. The single FAIL is a **probe defect, not a pack
regression**: the D09 dial probe captures its baseline from the live value
(`60_Probes_Opt.lua:411`) and asserts `base_carry + 1` at `:431`, which only
holds if the account dial is already at base — today's playtest left it
off-base (same account change that produced 74/74 instead of 68/74). Neither
removal touches drones, modifiers or Mod Options, and the module logged
`applied`. **New TestKit defect recorded: the D09 probe is state-dependent and
can FAIL or false-PASS on account dial state; it must force base before
measuring.** Same family as the 2026-07-29 falls-off-the-end-returns-SKIP trap.
Confirmation is a 2-minute re-run with the dials at base — the natural moment
to run PT-56 as well. TestKit autorun armed and **disarmed** cleanly either
side.

**Challenge issued and answered the same evening.** The reachability audit
(`3398031`) had rated F49(c) "live R2" — the owner asked for it to be
challenged with our evidence rather than blind, on the grounds that catching
exactly this was the audit's premise. Prompt at `0d9435c`, answered `48d9edb`.
Its findings are worth more than the one corrected verdict: the method is
**decisive on reachability and near-mute on intent**, so a wrong
author-hypothesis sails through with full confidence; exactly **two** verdicts
in the whole table were unenumerated, both F49 items the lead kept for itself;
and the audit's own evidence base **went stale mid-run** — `c3c4383` and
`ba1e88b` landed while its sweeps ran and it never re-read `git log` before
publishing, so the falsifying evidence for (c) *and* the play-proof for (d)
were already in the repo. New tier **`I` (intended behaviour)** added, and (d)
late-enumerated and confirmed R2.

**Held for the owner, deliberately not actioned:** the **F28** delete decision
(the audit's sole DELETE candidate) and the **FIX_POLICY §4 amendment** (now
revised by the challenge to require a positive intent statement plus tier `I`).
Both were framed by the audit as the owner's call, and the project reserves fix
deletions and policy edits to them.

---

## PT-46 tail — F49(d) PASS; F49(a) parked on a reachability question — 2026-07-30

**(d) cap-follows-length: PASS.** Live 305-sol colony, read-only counter
printing actual vs shipped-formula expected per track. Track 3 went
`els=43 cap=2` → `els=13 cap=1` across a partial salvage — the surviving-track
case the fix exists for. All lines `OK` across four runs, including after a
reload and a second salvage on a freshly loaded track. The mid-track salvage
also split off a new track at `els=25 cap=1`, correct on its own, which
independently confirms the 2026-07-25 QA correction. Recorded honestly on the
entry: the `PostLoadGame` sweep's REPAIR of a stale cap is **not** proven and
cannot be from a healthy save — queued as a TestKit probe.

**(a) instant-track palette: parked, not run.** The attempt cost something and
is on record. Reaching `place_track` needed a `SetMode` injection with no
player-facing equivalent; it misbehaved and left an orphan `TrackBase` with
invisible elements blocking grid hexes on the live colony (cleared by reload).
That broke the project's own no-live-UI-internals rule (F76 lesson) — the
assistant handed it over, the rule existed, it was violated anyway.

**The user's response to that is the important output of this leg.** Their
question — *"are we forcing this to test something vanilla, or are we in a loop
of testing artifacts that aren't real bugs if you play the game correctly?"* —
reframed the whole thing. The debris was an artifact of an unreachable entry
path and is filed as nothing. And it exposed that F49(a) itself has never been
asked the F24 question: `place_track` serves "map setup, cheats, the
instant-build rule", and **none of the three is verified player-reachable**.

That became `docs/REACHABILITY_AUDIT_PROMPT.md` (commit `5b0ad35`) — a
game-free, read-only audit asking of every fix whether a player can reach the
defect at all, with F24 as the worked template, an R1-R4/U tier vocabulary,
decision rules keyed to patch cost, an explicit anti-over-pruning stance, and a
drafted FIX_POLICY §4 amendment (the policy demands a proven defect but has
never demanded proven reachability — which is exactly how F24 shipped).

**Gap noticed while writing this up:** F49**(c)** has no play coverage either —
PT-46's tail only ever covered (d) and (a). Cheap to close in salvage mode
(click a station-owned connector hex, confirm the station is not flagged).
F49 therefore stays `fixed*` on two items, not one.

---

## F24 CLOSED `wontfix` — fix DELETED, counts 75→74 / 69→68 — 2026-07-30

Came out of the user sitting down to run PT-44's F24 half and finding it
**impossible**: no dome will place over existing buildings ("Objects underneath
are blocking construction"), tried across dome types, sizes and angles. The
user's own read — "if this was ever a bug it needed a mod that breaks
boundaries or does upgrades" — turned out to be exactly right, and the question
they asked next is the one that settled it: *what are we really fixing here?*

**Reachability proof (now on the F24 entry, do not re-derive).** `MoveInside`
has two call sites in all of `Src`. `MartianAssembly.lua:60` is live in play but
cannot reach the buggy line — `SpireBase.__parents = { "Building" }` and the
template declares no water or air, so `LifeSupportGridObject:MoveInside` is not
in that chain. That leaves `Dome:OnLoad`'s repair sweep, which needs a
pipe-connected life-support building inside a dome's interior hexes with
`parent_dome ~= self` and live connections. Vanilla cannot produce that: domes
refuse to place over buildings, **no dome template carries any upgrade** (all
`*Dome*.lua` checked, zero `upgrade*_id`), and nothing mutates an interior shape
at runtime. The defect is real — it was never a player report, it was found by
diffing the water grid against its electricity twin — but it is unreachable.

**User decision: delete rather than carry as latent.** The F28/F43 precedent
(real-but-latent, keep) was offered and declined, on the reasonable grounds that
those are cheap patches while this one was a **34-line full-function replacement**
of `LifeSupportGridObject:MoveInside` that would rot on any future patch to it.
Removed: `Code/Fix_DomePipeMoveInside.lua`, its `metadata.lua` code entry, its
`items.lua` ModItemCode entry, and the README fix-table row.

**Verification of the removal:** both edited Lua files parse clean (luaparser);
`items.lua`'s CodeFileName list now diffs **identical** to `metadata.lua`'s code
list; 75 files = 66 `Fix_` + 7 `Opt_` + `00_Core` + `90_SaveSanitizer` → **74
registered / 68 default-active**. No TestKit probe existed for F24, so the suite
stays at 77 probes.

**OWED:** an A/B pair — every recorded leg predates this and was measured at
75/69; the default leg should now read **68/74**. Flagged in STATUS, the
continuation prompt, PLAYTEST_CHECKLIST (PT-22 item 4, PT-21 setup) and
PLAYTEST_HELP's ListFixes row. Rollback is one `git revert`.

**PT-44 consequence:** the F24 half is removed; PT-44 now covers F23 only. This
is the **third** PT procedure found unrunnable by executing it (PT-29, PT-11,
now PT-44's F24 half) — the standing rule earns another data point.

---

## PT-48 CLOSED IN FULL — D02 AcknowledgedWarnings → `tested` — 2026-07-30

Live playtest-standby sitting, parallel to the PT-55 closure session (that
agent held `PLAYTEST_CHECKLIST.md` / `PLAYTEST_ARCHIVE.md` dirty for most of
this leg; results were written only after `aac6798` landed and the tree went
clean — no collision).

**Why the item was open at all, since the user asked.** The D02 work everyone
remembers is **PT-38**, which is a *different test with a different job*: it was
the GATE that decided whether to build the module, and it corrected the premise
from "re-nags every 2 real minutes" to **120,000 GAME-ms = 4 game hours**.
Archived and done 2026-07-27. The module was BUILT the same day. **PT-48 — the
play verification — had never been run once**; its only coverage was the TestKit
stand-in probe, and probe-verified ≠ `tested`. Nothing had been lost.

**Method: counters, not eyes.** Steps 1-2 are "nothing should happen" tests, the
exact shape that has twice produced unrunnable procedures here (PT-29, PT-11).
So the sitting opened with a **positive control**: fixture built, module OFF,
dismissal armed `suppress_until = now + 120,000` to the millisecond, and the
notification RETURNED after the window — proving the no-power fixture generates
re-add attempts and that a later "it stayed quiet" could not be vacuous. Two
paste-safe console counters (per-building state + whole-ack-set enumeration) are
recorded verbatim in the archived section and are reusable for any future
notification work.

**Result: all five steps PASS.** Acked buildings held for 505,850 game-ms
(≈16.9 game hours = **4.2 vanilla windows**) with `shouldshow=true` proving they
actively qualified and were still excluded, and `suppress_until=nil` proving the
silence was the per-object filter rather than the shipped window. A new
building, placed while PAUSED, warned inside the interval vanilla would have
been silent. Repowering the original three cleared all three stamps
(`total_acked` 3 → 1) and re-breaking re-warned all three. The stamp survived
save/reload — flagged pre-run as the likeliest failure.

**Two findings worth carrying forward:**
1. **D02's blast radius is provably tiny.** Exactly **two** notification presets
   in the entire game are `Suppressable` — `InsufficientResources` and
   `NotWorkingBuildings` (`Data/NotificationPreset.lua:546/:646`). Since the
   module's guard is a literal `id == ID`, `InsufficientResources` is the only
   id in the game where it could differ from vanilla. It was forced (via
   `const.MinDaysFoodSupplyBeforeNotification`, restored after) and shown
   arming, expiring and re-nagging untouched. That reduces step 5 from a vague
   "check other warnings" to a single decisive observation.
2. **Vanilla curiosity, unexplained, filed on the D02 entry:**
   `InsufficientResources`' suppression resolved on **RealTime** while PT-38
   measured `NotWorkingBuildings` on **GameTime**, even though both presets
   leave `GameTime` at its default `true`
   (`NotificationPreset.lua:65-66/:126-128`). D02 never calls `GetTime()`, so
   the PASS is unaffected — but if the notification INSTANCE rather than the
   preset supplies `GameTime`, PT-38's recorded 4-game-hour fact may need
   scoping. Game-free item.

Also confirmed by reading before the sitting started: **D02 never had the
audit-1.3 first-enable defect.** Its three wrappers replace plain notification
GLOBALS rather than class methods, so runtime flattening never applies, and
`OnMsg.ApplyModOptions` re-runs `apply()` (`00_Core.lua:129`) on a first
mid-session enable. Verified in play — the module was enabled mid-session with
no relaunch and worked immediately.

**Docs:** D02 flipped in both BUGS.md places + full result block on the entry;
PT-48 section moved to PLAYTEST_ARCHIVE.md (37 sections) with the counters and
conditions; STATUS next-gates and optional-module list updated. MOD_DESCRIPTION
needed no change (it does not segregate tested/untested for opt-in modules).

---

## PT-55 CLOSED — step 3 run live, D01 limitation accepted — 2026-07-30

The bottleneck item is done, on the user's explicit "nothing else until it is
closed" directive. Two blockers resolved in order: (1) the D01 decision — the
parked-rocket first-enable limitation ACCEPTED as documented (user call,
`4f5f61e`), no `on_activate` refresh built, enhancement path recorded on the
D01 entry; (2) step 3 executed in the live sitting (log
`Mars.exe-20260730-12.03.01`): all six opt-ins `applied` → `deactivated` ×6 →
`re-activated` ×6 → `deactivated` ×6, with on-screen status reads AND full
`ListFixes` blocks agreeing at every step; log swept clean per PT-22 (zero
LUA ERRORs; Braze DNS + LawOfficeDoor ResManager noise only). Bonus capture:
`MultipleSuns: reconnected 1 solar panel(s)` on the mid-sitting reload — the
D04 self-heal visible in the log. PT-55 section archived (36 archived
sections now); audit A2 caveat retired in AUDIT_FINDINGS; STATUS + the
continuation prompt rewritten.

Tooling fact worth keeping: while Mars.exe holds the session log open, the
logs DIRECTORY reports a stale 0-byte size for it — NTFS directory metadata
only updates on handle close. `FlushLogFile()` works; open or copy the file
to read the flushed content instead of trusting the listing.

---

## PLAYTEST_CHECKLIST split: tests-only checklist + PLAYTEST_HELP.md — 2026-07-30

User call ("to the human eye its hard to find and organize play tests and then
find commands. its bloated"): the checklist now carries ONLY tests + the
reporting protocol; everything reference — ground rules, external-validity
rule, cheat discipline, console facts, the verified command table, Test Kit
helpers + stress harness, save-fixture recipes, the unverified-commands table —
moved verbatim to the new `docs/PLAYTEST_HELP.md`. Split executed by line-range
slice (python, utf-8, no round-trip); verified: all 46 headings survive, moved
content greps in exactly one of the two files. Cross-references updated:
checklist internal pointers, FABLE_NEXT read-list + jobs list, WORKFLOW.md
read-list, STATUS.md ground-rules pointer, TestKit README (own repo commit).
PLAYTEST_ARCHIVE and history docs untouched.

---

## Curiosity sitting → D10 speced: tunnel water, workshop research, unemployment truth — 2026-07-30

Assisted research session (game-free), three questions from the user, all
answered from Src with community cross-checks; ended in a new speced D-item.

- **"Can water reach an isolated mountain base?" — YES, through the Universal
  Tunnel, and the UI hides it.** `UniversalTunnel` → `TrackTunnelBase` →
  `TunnelBase` = `ElectricityGridObject` + `LifeSupportGridObject`;
  `GameInit` merges BOTH grids (Tunnel.lua:6,87-88; re-merged on track power
  reconnect, TrackTunnel.lua:12-17). Tracks/stations bridge electricity ONLY
  (Track.lua:112-123) — which is why players see power cross but never water.
  Recipe: pipes to both portals. The buildable Universal Tunnel's description
  says "tracks and power grids" — the hidden legacy Tunnel template still
  carries the correct "power and life support grids" text (description drift,
  F65 family). **Unfiled candidate** (user call): one-line description patch.
- **"What are 'workshops'?" — the three vocation buildings** (Art/VR/
  Biorobotics, build category "Workshops"), NOT factories: produce nothing,
  consume Polymers/Electronics/MachineParts per fraction-of-capacity, pay
  +10 Morale / +5 Comfort×performance. Community's three-camp unemployment
  argument adjudicated from code: no colonist-level penalty (icon-only
  status effect) — but **in Relaunched every faction def punishes ≥10% dome
  unemployment** (Workers' Party -900..-3000, WorkersParty.lua:103-121), so
  the inherited "ignore it, no penalty" advice is now wrong at colony level.
- **Design verdict on workshops** (user asked for honest): sound core loop,
  undersized (6-10 workers/shift), and illegible — the faction cost appears
  nowhere in workshop/unemployment UI text.
- **D10 SPECED + user-approved:** one Opt_ module — T1 text repairs
  (descriptions + Unemployed rollover state the faction cost) + T2 capacity
  dial (base/+50%/+100%, D09 label-modifier pattern, `max_workers` +
  `consumption_amount` PAIRED so per-worker cost stays vanilla —
  consumption is fraction-of-capacity × amount, ArtWorkshop.lua:35-39).
  **Build gated on PT-56 PASS** (same machinery, first live check first).
  Seniors-in-workshops deferred as its own decision (D07 employed-senior
  exemption interaction). Full spec: BUGS.md D10.
- **Shuttle-limits research (same sitting, follow-up curiosity):** three
  separate limits — cargo 3/shuttle (modifiable, +3 from HighPoweredJets =
  the game's only cargo buff), 10 shuttles/hub (+6 CompactHangars),
  passengers **1/trip structurally** (one vanilla task per colonist; the "1"
  is architecture, not a number). No breakthrough touches shuttles; fuel is
  the only shuttle law. Leftover cargo chains one extra hop or gets DUMPED
  as a ground pile (shipped comment: "noone wants this..dump it and go
  home"). Full reference on the new BUGS.md D11 entry.
- **D11 FILED AS CANDIDATE, NOT APPROVED (user's explicit framing):**
  same-pair passenger batching is feasible (task objects already carry the
  dome pair; hold fits 3-6 colonists; risks = boarding sync ×N, cancellation
  granularity, mod-removed-mid-flight landing). **The filing is for the
  record only — re-ask the user before any build. Multi-hop passenger
  routing REJECTED the same day.**

---

## D09 stat dials: decided → probed → range widened → BUILT → A/B clean, one evening — 2026-07-29 latest

**The whole D09 lifecycle ran in a single assisted evening.** During live play
the user asked where the planned speed/carry sliders were (answer: DECISION
recorded, build not started). Prep ran WHILE the user played (Mars.exe-running
rule respected: all drafting in scratchpad, zero repo writes); the user ran the
queued C-side clamp probe in-session (`SetMoveSpeed(10000)` → read back 10000,
movement clean at ultra — no C-side clamp, recorded on D09 + the DECISION
facts) and **widened the dial range 1.5x/2.0x → 2x/3x/5x on the strength of
it** (worst case 1440 × 5.6 = 8064 < 10000). On exit the build landed as
`9aae3de` (module + items/metadata + BUGS D09 + FIX_POLICY §5 dial addendum +
MOD_DESCRIPTION + PT-56 + STATUS/FABLE_NEXT), then the owed A/B pair ran
UNATTENDED (user pre-authorized):

- **Leg 1a FAIL — real catch #1:** the module's file-scope self-check read
  `Modifier.new` — the F64 pre-flattening trap (`new` is inherited, invisible
  on the classdef). Fixed `d8e309c` (presence-only at file scope, capability
  check in the reapply guard).
- **Leg 1b FAIL — real catch #2:** the new TestKit dial probe wrote its OWN
  env's `CurrentModOptions` — **per-mod-env** (each env aliases that mod's
  options object, Mod.lua:2128-2131/:679-683). New ENGINE_FACTS entry; probe
  now writes `Mods[pack].options` (TestKit `ed01ef7`).
- **Leg 1c: 67 PASS / 0 FAIL / 10 SKIP / 0 ERROR at 75/75** — dial probe
  PASSes both directions through the real Apply path. **Baseline:
  1/61/15/0** (D09 probe FAILs "fix pack not loaded" by design). Logs clean
  both legs; metadata baseline surgery restored from saved copy, tree clean.

**Account-state correction:** the legs read 75/75 — all six toggles were ON
again (re-enabled during the day's play). PT-55's all-OFF starting state must
be set by hand; the FABLE_NEXT/checklist notes claiming OFF were corrected.
D09 status: `built`, PT-56 owed (apply/stack reads, live removal, stale-save
reconcile — the clamp probe half is already done).

**Set completed 2026-07-30 (same assisted session):** the user flipped all six
toggles OFF and the default-config leg ran unattended — **62/0/15/0 at
69/75**, log clean, dial probe PASS (dials independent of the toggles; the
five opt-module probes back to `inactive (opt-in)` SKIPs). All three legs of
the post-D09 set now match expectations exactly. Side effect: the account is
in PT-55's required all-OFF starting state — PT-55 staged.

---

## PT-55 result + the D07 cohort-housing deadlock found in play — 2026-07-30

**PT-55 — the audit's A2 question is ANSWERED YES.** All three reworked hooks
install and run on a first mid-session enable, no relaunch. D03 clean ("no
issues at all"). D04 passes with an expected, self-healing timing limitation
(pre-existing panels can't be retro-bound because the wrap is on
`SolarPanelBase:GameInit`; a reload re-runs it and they snap to sun #2). D01's
hook is proven live — a rocket that LANDS after the flip fills immediately — but
**a rocket already parked does not begin refuelling and does not heal on
reload**, because `GetFuelResourceRequest` is only consulted when
`CargoTransporterNew:UpdateCargoResourceRequests` runs and nothing re-triggers
that for a parked rocket. PT-55 step 1's literal wording therefore fails for
D01. Open decision recorded on the D01 entry: an `on_activate` demand refresh.
The tester diagnosed the cause unaided ("my guess it's an on-land interaction")
and source confirmed it.

**D07 COHORT HOUSING — a self-reinforcing deadlock, found by deliberately
stressing homelessness.** Full chain, every link source-verified:

1. D07's cross-dome pass fills a nursery-only dome with Children.
2. They age up; the **Youth** trait's `apply_func` evicts them from the Nursery
   (`Data/TraitPreset.lua:760-764`) — so the tester's first hypothesis, that
   aged-up children clog the nursery, is WRONG; they are evicted correctly.
3. That dome has **no non-Child housing**, so they become homeless *there*.
4. `Dome:AddToLabel("Homeless", …)` sets
   `overpopulated = #Homeless >= g_Consts.OverpopulatedDome`
   (`Dome.lua:1026-1035`).
5. **D07's own `consider()` skips `community.overpopulated`**
   (`Opt_CohortHousing.lua:194`) — so the child dome is now permanently
   excluded as a destination.
6. New Children never migrate in. Observed live: nurseries at 5/26 and 3/26
   (68 free Child slots) with 28 homeless in the dome (**26 Youth, 2 Adult** —
   93% aged-out, the eviction signature), while a Child in a neighbouring dome
   commutes in to the school and goes home to a Smart Apartment.

`CanAcceptNewColonists()` is only `ui_working and accept_colonists`
(`Community.lua:61-63`) and read `true` live, so the quarantine is NOT involved
— `overpopulated` is the whole gate. **The module poisons its own destination**,
and the more children it delivers the more firmly it locks itself out.

**Separately established and NOT filed as a defect:** the homeless youths
themselves. `non-cohort free slots colony-wide: 0`, so total homelessness is set
by (population − housing capacity); D07 changes *which* colonist lacks a chair,
not how many. It arguably improves utilisation by freeing ordinary slots. A
caveat, not a bug — deliberately not given an F-number.

**RESOLVED SAME DAY → D12 SPECED AND APPROVED.** Four options were put to the
user (drop the `overpopulated` clause; refuse nursery-only domes; both;
document only) and **all four were rejected** in favour of a better direction
the user proposed: a per-dome **"no homeless residents"** policy that pushes
homeless colonists out to a dome that accepts them. It fixes the *cause* rather
than the symptom, is player-steerable rather than a hidden heuristic,
generalises to Retirement domes, and heals an already-poisoned dome — set the
flag, the homeless drain, `overpopulated` clears, D07 resumes unaided with no
change to D07 at all.

**Root cause reframed while speccing it.** The shipped eval *already* lets a
homeless colonist move to a dome with no free housing (`Colonist.lua:2676`,
comment: "if homeless, try changing community even if doesn't have living space
available"). What stops them is the gate above: candidates must score
**strictly better** unless home or work improves (`:2675`, `:2680-2681`). With
zero free slots colony-wide and unemployment saturated, every candidate **ties**
— and ties never move anyone. **This is the same tie rule D07's own header
cites as the reason cohort members never consolidate.** D12 is that same
tie-break applied to a different population.

**A design trap the user caught before it was written.** The first packaging
idea was to extend D03 ResidencyControl. The user asked whether that meant the
same UI control, and it would have been fatal: D03's row wraps
`Community:CanAcceptNewColonists`, which D07's `consider()` calls — so closing
the child dome to new residents would block the cohort delivery the feature
exists to protect. The two controls must act in **opposite directions on the
same dome simultaneously** (entry open, exit forced), so the new flag needs its
own field and its own gate. Packaging revised to a **separate module with D03 as
donor pattern only**, which also keeps D03's `tested` status intact.

**Chain confirmed end to end later the same sitting:**
`g_Consts.OverpopulatedDome` = **20**, dome read `overpopulated=true
homeless=20`. Step 4 is measured, not inferred. Note the threshold is `>=` and
the dome sat at **exactly** 20 (down from 28 as a few drained or died) — the
deadlock is genuine but marginal, so a future D12 test must show the drain
cleared it rather than attrition.

## PT-11 PASS → F01 `tested`, and the test that could not have worked — 2026-07-29 late

**PT-11 PASS → F01 `tested`** (P1, the first of the pack's fixes verified on the
SAVE-B no-disasters fixture). Preconditions live: `NoDisasters` true,
`Environment` Underground, fix `active`. Rubble baseline **27**; leg 1 (20 game
hours) **27**; save + reload, `g_Consts.MarsquakeSpawnTime` read back `1`, count
**27**; leg 2 (20 more) then the positive control
`CheatTriggerUndergroundMarsquake()` → **36**.

**Why +9 closes it:** `rubble_count = 10` (`Marsquake.lua:235`), so one quake
spawns at most ten cave-ins and nine landing (one `FindCaveInLocation` nil) is
the normal outcome. At most ONE quake occurred across the entire run, and the
control fired it. A single scheduler quake in leg 2 would have put the count
near 45; an unfixed pack, in the hundreds.

**THE TEST AS WRITTEN COULD NOT HAVE WORKED.** PT-11 said to set
`g_Consts.MarsquakeSpawnTime = 1` / `MarsquakeRandomTime = 1` and wait 20 game
hours. But a `MapGameTimeRepeat` computes its next interval at the END of each
tick and then sits in `Sleep(sleep)` (`CommonLua/Core/lib.lua:1590-1592`) — the
running thread keeps the interval it was handed *before* the edit. The defaults
are **384 and 96 hours** (`Lua/__const.lua:1085-1094`), i.e. **16 sols**, so the
prescribed 20-hour wait would have observed a thread still asleep on the old
interval and scored a PASS **whether or not the fix worked**. Every previous
reading of this test would have been vacuous.

Repaired by three additions, now in the checklist's ground rules as a general
rule (it applies to any scheduler-compression test, not just this one):
1. **`RestartPeriodicRepeatThread("<name>", CurrentMap)` after compressing**, so
   the fresh thread reads the new consts — verified with
   `IsValidThread(CurrentMap.RepeatThreads.<name>)`. It does not bypass a fix
   that wraps the repeat: the wrapper lives in `PeriodicRepeatInfo`, re-read
   every loop. **Must be repeated after each save/reload** — repeat threads are
   persistable (`MakeThreadPersistable`, `lib.lua:1595`), so a reload restores
   the old sleep.
2. **An objective counter** (`CurrentMap:MapGet("map", "CaveInRubble")`) instead
   of watching for damage. Also recorded: underground *buildings are irrelevant*
   to this test — `FindEpicentre` is `GetRandomPassable` →
   `GetPlayableAreaNearby` (`Marsquake.lua:237-241`), so quakes fire on a bare
   map and rubble lands near a random epicentre, not near the colony.
3. **A positive control at the end.** A negative test without one cannot
   distinguish "the fix worked" from "nothing would have happened anyway" —
   which was precisely this test's failure mode.

## PT-29 PASS + two documentation defects — 2026-07-29 late (live, on the SAVE-B fixture)

**PT-29 PASS → F41 `tested`** (index row + heading flipped, section moved to
PLAYTEST_ARCHIVE.md). Console read on a colony with both techs unresearched:
**`nil` → `50` → `150`**. Gene Forging alone now contributes its `param1 = 50`
where it contributed nothing before, and the two techs **add** — which is the
whole reason the fix is an additive sum rather than ChoGGi's GeneSelection
param1-bump (that approach pays out only when the *other* tech is also
researched, so Gene Forging alone would still have done nothing).

**Two documentation defects, both found by simply trying to run the test:**

1. **PT-29's trigger was unrunnable as written.** It read
   `MainCity.labels.Colonist[1]` while requiring the reading be taken "before
   researching anything" — you cannot have a colonist before the game
   auto-researches something. Neither constraint was real:
   `GetRareTraitChance(unit)` takes an **optional** unit
   (`local city = unit and unit.city or MainCity`, `Colonist.lua:3542`, a
   fallback the fix preserves verbatim), so a bare call works from sol 1; and
   the function consults **only** GeneSelection and GeneForging, so every other
   tech is irrelevant. Neither can arrive by accident either — GeneSelection is
   a **Breakthrough** (`CheatResearchAll` skips undiscovered ones) and
   GeneForging is a **Storybit** tech. PT-29 rewritten accordingly.
2. **`not understood` explained and written down.** The first attempt pasted the
   doc's `--> nil` annotations into the console and failed three times. Cause:
   the `*r` / `*g` rules splice the typed code into
   `CreateRealTimeThread(function() %s end) return` **on one line**
   (`uiConsole.lua:360-361`), so a `--` comment swallows the closing
   `end) return`, nothing compiles, no rule matches, and `console.lua:24`
   answers "not understood". Compounded by the console input being a SINGLE
   line — a pasted block concatenates, which is why `--> nil` and the next
   command arrived fused as `--> nilUIColony:SetTechResearched(...)`.
   **Never write a console snippet with a trailing comment or a `--> value`
   annotation.** Corollary also recorded: a bare expression is auto-wrapped in
   `ConsolePrint(print_format(...))` (`uiConsole.lua:363`), so a simple read
   needs neither `*r` nor `ConsolePrint`. Swept the rest of the checklist —
   PT-29 was the only instance of either trap.

**Coverage question raised and answered:** are any other playtests
research-sensitive? **No** — PT-29 was the only one, and the remaining un-run
items are gated on fixtures, mysteries and game rules, not research state (most
want *more* research, not less). But the check surfaced that **all four
tech-related fixes other than F41 have no playtest at all** — and three of them
correctly never will: **F28** is latent and mod-facing, **F43** is latent in the
shipped game (only one layout ships, `SelfSufficientDome`, and none of its
entries is tech-locked), and **F25** applies to pre-1.0.6 saves only, which is
also why its probe reports SKIP ("the tech has no description T") on a current
build — not a coverage hole, an unreachable defect. **F18** is the only
genuinely untested one; its preset half is already probe-covered
(`IndependenceTerraforming` PASSes), and the play half needs an Independence
sponsor plus a special project to observe `Consts.SpecialProjectResourcesModifier`
move 100 → 80 rather than → 90. Judged not worth a PT for a data-only P2;
recorded here so the question is not re-derived.

## Pre-flight A/B pair — 2026-07-29 late (unattended; the owed post-wave-6 re-baseline)

The A/B pair owed since wave 6 RAN, and it earned its keep: it caught a
TestKit defect that had made wave 6's automated coverage imaginary.

**Legs** (all unattended via `-smrautorun`, ~70 s each, logs in
`%AppData%\Surviving Mars Relaunched\logs`):

| Leg | Log | Result |
|---|---|---|
| Baseline (fix pack `code` list emptied) | 21.21.01 | **1 PASS, 60 FAIL, 15 SKIP, 0 ERROR** |
| Fixed, all six toggles ON | 21.22.35 | 63 PASS, 0 FAIL, **13** SKIP, 0 ERROR — 74/74 active |
| Fixed, re-verify after the probe repair | 21.25.56 | **66 PASS, 0 FAIL, 10 SKIP, 0 ERROR** — 74/74 active |
| Fixed, **default config** (six toggles OFF) | 21.36.51 | **61 PASS, 0 FAIL, 15 SKIP, 0 ERROR** — 68/74 active |

**76 probes now** (was 73). Baseline's 1 PASS is the FactionFundingCheck
canary, as always; all three wave-6 probes FAIL in baseline as designed —
including `RainsDeadlock`, which did NOT skip on the synthetic map (the
harness builds a colony, so `HasGame()` is true).

**THE FINDING — wave 6 had zero real probe coverage until this run.** The
middle leg showed PASS stuck at 63 while SKIP rose 10 → 13: the three wave-6
probes were reporting **SKIP with an empty message**. Cause: all three ran
every assertion and then fell off the end of `run()` without returning a
verdict, and `SMRTest.Run` turns a nil status into SKIP
(`00_TestCore.lua:243`). Every other wave file has exactly one `return "PASS"`
per probe; `55_Probes_Wave6.lua` had **none**. The file was written in the
post-QA build leg and never run against a *fixed* leg until now — baseline
FAILs come from the `FixMissing` guard and so never exercise the tail.

Repaired in the TestKit (local-only, commit `d701595`): explicit
`return "PASS", <what was verified>` in all three, and the two
`if x == nil then return end` holes now return an explicit FAIL — a bare
return read as an empty SKIP whether `WithGlobals` had deferred an ERROR or
the call simply answered nothing. Returning FAIL is safe for the deferred
case: `SMRTest.Run` overrides a FAIL with the pending ERROR
(`00_TestCore.lua:237-242`). Re-verified leg: 66/0/10/0. Reaching the tail
means every assertion had already passed, so the wave-6 *fixes* were correct
throughout — only the reporting was broken.

**Log hygiene, both legs:** zero `[CommunityFixPack]` inactive/error/disabled
lines, zero errors naming `SMR-BugFixPack\Code`. Four engine error signatures,
all present in BOTH legs and none ours: 48× `Flight.lua:465 objects_to_mark`,
1× `Flight.lua:479 objects_to_unmark`, plus the `GridObject:ApplyToGrids` /
`BuildWaypointChains` / `CreateResourceRequests` GameInit nil-calls (1× each in
baseline, 3× each in the fixed leg — each leg generates a different random map,
so per-signature counts vary; no new signature appeared).

**Account-state fact worth carrying:** the first fixed legs came up **74/74
active** — all six optional modules were already ON from the account's saved
Mod Options toggles (they are account-persistent, and no `SMRFixPack_Optional`
override was in play; the leg's temp file was never listed in metadata). So
those legs ARE the all-toggles leg. The user then turned all six OFF at the
main menu and the **default-config leg** ran: **68/74 active, 61/0/15/0**, with
the pack reporting all six `inactive (opt-in module, off by default)`. That
leg had to be done by hand because the pre-load override table can only force
modules ON, never off. **The A/B set is therefore complete — nothing is owed
to the harness.**

**Cross-leg arithmetic checks out exactly.** All-toggles 66/10 vs default
61/15: the difference is precisely the five opt-module probes
(ClassicRockets, AcknowledgedWarnings, ResidencyControl, MultipleSuns,
CohortHousing) moving PASS → SKIP. Five, not six, because **D06 has no probe
of its own by design** — the stress harness and PT-52 cover it. Against the
pre-wave-6 default leg (58/0/15/0 at 65/71): +3 PASS = the three repaired
wave-6 probes, SKIP identical at 15, active 65 → 68, total 71 → 74. The
toggles were left OFF afterwards, which is PT-55's required starting state.

**Harness discipline held:** `metadata.lua` was restored from a saved copy and
hash-verified byte-identical (`7C352189…`), the temporary `Code/97_OptInLeg.lua`
was deleted unused, nothing was committed while the baseline edit was in the
tree, and the TestKit autorun flag stayed commented out (the `-smrautorun`
command line armed the legs instead).

## Audit remediation session — 2026-07-29 (game-free, one-off AUDIT_FIX_PROMPT executed and deleted)

AUDIT_FINDINGS.md Phases 1-3 implemented in full, one commit per plan item
("Audit fix N.N" series, 88c2f08..HEAD). Parse sweep clean on every touched
Lua file; every patch target re-verified against Src before editing.

**Phase 1 (code):**
- 1.1 (A1) veto re-check in DustSicknessDamage / DustSicknessBiorobots /
  IndependenceTerraforming patch() (LastTransmissionStorage donor pattern);
  IndependenceTerraforming's status heal gated to never overwrite "disabled".
- 1.2 (B3) data_loaded latch in the DustSickness pair — absent targets after
  DataLoaded now latch `inactive` with a reason instead of reporting active
  forever.
- 1.3 (A2) file-scope install + per-call IsActive gate (Opt_DroneOverhaul
  donor) for Opt_ClassicRockets (whole fuel wrap), Opt_ResidencyControl
  (ONLY the CanAcceptNewColonists gate) and Opt_MultipleSuns (ONLY the
  GameInit binding wrap) — first mid-session enable now works; apply() keeps
  its self-checks and reason strings; headers tell the truth.
- 1.4 (B1) reconciler retries "error" entries on toggle-ON, logs every
  skip/failed retry and vetoed-toggle attempt, and surfaces
  on_activate/on_deactivate errors.
- 1.5 (B2) MeteorStormWedge's vanilla-release path clears
  g_DisastersPredicted.DisasterMeteorStorm itself (guarded on no live
  notification) — self-sufficient with F81 disabled, idempotent beside it.
- 1.6 (C4) %% escaping on all 6 remaining unescaped ModLog sites (the plan's
  "6 local + 4 inline" double-counted — grep proved exactly 6 existed);
  MoraleComfortTooltip's false returns-pass-through comment corrected
  (shipped UIStatUpdate verified to return nothing); build stamp
  1.0.7.396349 added to F05/F08/F07+F15/F29 headers.

**Phase 2 (packaging/storefront):**
- 2.1 metadata.lua: short_description (192 chars), last_changes,
  optional_mod=true, version 1.0, ignore_files (defaults + docs/.claude/
  README/.gitignore; LICENSE ships), description's per-fix-disable claim
  qualified. lua_revision confirmed and kept.
- 2.2 items.lua: 75 ModItemCode entries script-generated from metadata.lua
  and diff-verified identical order — the editor round-trip / upload flow no
  longer regenerates `code = false`. Toggles untouched.
- 2.3 MOD_DESCRIPTION.md: CohortHousing block (name verified in-game:
  "Retirement Home"); honest savegame-footprint wording replaces the false
  "stores nothing" claim; console achievements disclosure (Xbox/PS/MS Store
  blocked, Steam/PC not); PC-only per-fix-disable caveat; console
  bug-reporting variant.
- 2.4 README.md: 4 missing fixes + 2 missing modules added; findings count
  73 → 91. (2.5 preview image / screenshots / portal rules = owner tasks,
  still open.)

**Phase 3 (docs):**
- 3.1 F02 heading + RESOLUTION note (root cause pinned to F78/F81); D07
  heading matched to its index row; withdrawn fpk-divergence doctrine
  corrected in its last two live copies + BUGS/WORKFLOW framing now cites
  the 2,250/2,256 parity proof. (D06's index/heading already agreed.)
- 3.2 ENGINE_FACTS.md extracted verbatim from STATUS "Key technical facts"
  (sole authoritative home); pointers updated.
- 3.3 STATUS.md rebuilt as a ~225-line current-state doc (header with
  authoritative counts / open decisions / next gates + reference sections);
  all legs, wave records and superseded A/B tables moved verbatim to THIS
  file; stale "47 tracked defects" headline no longer styled as current.
- 3.4 sediment archived (ChatGPT report, RESEARCH, TESTING,
  CHEATS_INVENTORY) with promotions first: RESEARCH §3 leads → C03-C08,
  PLUS its three HIGH untraced leads → C09-C11 (small scope extension so
  archiving didn't bury them); CHEATS_INVENTORY's 11 missing commands +
  negative-knowledge list folded into the checklist's verified table (Src
  lines re-verified); TestKit README's probe table was already in place —
  its two stale pointers fixed (one docs-only TestKit commit, 39ecdba).
- 3.5 WORKFLOW.md rewritten (reading path, per-fix discipline, fpk
  extraction diff as an explicit release gate, post-audit release steps).
- 3.6 FIX_POLICY: global-replacement rank 4b, reconstruction sub-category,
  declaring-class rule, OnMsg status+veto rule, data_loaded-latch rule, new
  optional-modules / engine-semantics / console-platforms sections.
- 3.7 28 BUGS.md index rows slimmed to status + date + PT ref (prose
  verified present in entries first).

**Found beyond the audit:** nothing contradicting a finding; two counting
nits (the 1.6 "6+4" double-count; D06's 3.1 half already fixed pre-audit).
PT-55 added to the checklist for the owed human re-verify.

**Owed to humans:** PT-55 (three reworked opt-modules' live toggles, both
directions, mid-session FIRST enable); a PT-20-shaped save/remove/load cycle
covering wave-6 persisted state; the pre-flight A/B RunAll pair (still owed
since wave 6); owner tasks 2.5; the Phase 4 go-decision.

## Superseded rolling wrap (the pre-restructure STATUS header, through 2026-07-29)

Updated: **2026-07-29 LATE (QA-review session + wave-6 build): the
fresh-context QA review RAN and reported — every Track A/B claim verified at
source, the fpk-divergence doctrine WITHDRAWN (full `Lua.fpk` extraction:
2250/2256 files byte-identical to Src, build `1.0.7.396349` — see Key
technical facts), and the Track A plan was revised to an additive/watchdog
shape. That plan is now BUILT (user go, unattended leg): **F78 + F81 fixed** —
`Fix_DisasterPredictionLeak` (additive MeteorStormEnded removal + PostLoadGame
flag reconciliation), `Fix_MeteorStormWedge` (hourly wedge watchdog, heal via
RestartGlobalGameTimeThread + guarded stop pulse), `Fix_RainsDeadlock`
(bounded rains wait + persisted-loop refresh) — wave-6 probes in the TestKit
(`55_Probes_Wave6.lua`), **PT-54 is the live gate and an A/B RunAll pair is
QUEUED as the next session's pre-flight**. Track B decisions: claim gate
kept-but-demoted; the overhaul will ship Mod Options STAT DIALS (speed
×1.0/1.5/2.0, carry +0/+1/+2 — DECISION section in
`DRONE_OVERHAUL_OPTIONS.md`); the user's colony was measured at the vanilla
stat ceiling (2304 = +60% speed, 2× carry), so the structural choice (priority
escalation vs D08 dispatcher) is gated on the request-lifecycle
instrumentation — **BUILT 2026-07-29 (stress harness v2, TestKit
`91_Stress.lua`: per-request lifecycle tracing via RequestAssignUnit/
RequestUnitFulfill + StartDemandPhase/StartWorkPhase/Repair wrappers, gate
scored on the FindTask-decided cohort only, run-conditions header, stat-dial
legs first-class; `HARNESS_REVIEW_PROMPT.md` executed and deleted). Two new
Src facts recorded on D06: SetCommandKeepQueue preempts immediately (the ~57m
work→claim was NOT the deliverer handoff) and SHUTTLE deliveries misfire the
handoff (CargoShuttle has no Work method) so shuttle-hauled repairs DO go
through FindTask. The PT-52 B2 re-run with the v2 harness is the next live
gate.** Prior wrap: **2026-07-29 (live disaster leg — see the
section directly below): TWO P1 defects found. F81 CONFIRMED LIVE — a single
stranded `g_DisastersPredicted` flag was gating the colony's ENTIRE weather
system, and clearing it started rain instantly; the leak that strands it is
UNCONDITIONAL (every completed meteor storm does it). F78 reproduced on demand
and localized to the unbounded drain loop at `Meteors.lua:238-241`. F82 filed.
Drone stress harness built (TestKit, local-only) — its A/B has now RUN (null
result; see D06). D08 extender overhaul designed, nothing built.** Prior wrap: **2026-07-28 LATE (post-D07-build): D07 `Opt_CohortHousing` BUILT
(user-authorized unattended leg) with a FRESH A/B pair — 73 probes, baseline
1/57/15/0 · all-six-toggles 63/0/10/0 (71/71) — plus PT-23 → F46 and PT-09 →
F14 flips (twelve flips total on the day). See the "D07 build leg" section
directly below.** Prior wrap: **2026-07-28 session wrap — the PT-52 live sitting (D03 tested,
F71 tested, PT-52 telemetry healthy, F68 over-draw caught) + the same-day
game-free F68 repair leg with a FRESH A/B pair (baseline 1/57/14/0 ·
all-five-toggles 62/0/10/0, 70/70 — no pre-flight queued for the next
session). See the two 2026-07-28 leg sections below and the header
additions.** Prior wrap follows: 2026-07-27 night (**D05 SHIPPED AND TESTED same
night — optional modules enable in-game via Options → Mod Options, live both
directions, restart-persistent (PT-51 archived); PT-50 PASS in full → D04
tested; PT-49 core passing + row reposition verified; ListFixes crash found
by play and repaired; F76 surface widened to the dozer path; the drone
task-assignment investigate item is fully stocked and has its own kickoff
prompt.** 72 probes; last legs clean: baseline 1/57/14/0 · fixed 58/0/14/0
(64/68) · opt-in 61/0/11/0 (67/68); **an A/B re-verify is QUEUED as the next
session's pre-flight** (two mechanical repairs landed after the last pair —
expected numbers unchanged). See "Mod Options build leg" below; the earlier
same-day build leg and the playtest-marathon record follow). **2026-07-28:
the drone task-assignment static investigation leg is DONE (section below),
and the user-greenlit D06 overhaul core + F77 fix are BUILT the same day —
see the build-leg section directly below. PT-52 (attended, multi-iteration)
is the next sitting's centerpiece.** **2026-07-28 PT-52 sitting (live):
PT-49 COMPLETED in full → D03 `tested` (archived) — arrivals + tourists
proven against an adversarial pad-beside-the-closed-dome setup, an
unexpected child resident forensically cleared as in-dome birth, MicroG row
verified on an asteroid habitat and KEPT there by user decision (two real
auto-move-in paths exist: inter-habitat resettlement and stranded
re-homing).** **Same sitting, lander leg: PT-17 ratchet PASS (request pinned
at the hold across 4 automated cycles, no unload flip) and PT-32 PASS in
full → F71 `tested` (archived) — live two-resource priority inversion,
valuables first, nothing dropped. Capacity-edge leg: no wedge, BUT a NEW
FINDING on the F68 fix — request over-draws below the GET-WHEN-ABOVE
threshold under active mining (asteroid drained to 84 vs threshold 144);
root cause + repair sketch on the F68 entry (the fix double-implements the
anti-churn floor; delete the aboard-into-ground half). **BOTH queued repairs
LANDED the same evening (F68 over-draw + TestKit logger — see the repair-leg
section) with a fresh A/B pair; the build queue is EMPTY again.** PT-17
stays un-archived pending an attended capacity-edge re-run — **DONE 2026-07-28
next sitting: re-run PASS (ground settled AT the threshold, request tracked
instead of ratcheting) → F68 `tested`, PT-17 archived; PT-19 PASS same
sitting → F73 `tested`, archived (residence held through both gap shapes);
PT-33 PASS same sitting → F72 `tested`, archived (all three cases incl.
both not-over-broad negatives); PT-40 PASS same sitting → F65 `tested`,
archived (merge both geometries, clean salvage split, long-track control,
reload, log clean); PT-31 PASS same sitting → F70 `tested`, archived
(round trip held, prefill negative intact); PT-16 PASS same sitting →
F67 + F69 `tested`, archived — **the ASTEROID SECTION is COMPLETE.** PT-43
PASS in full same sitting → F19 + F20 + F21 `tested`, archived — **TEN
status flips in one sitting (F68, F73, F72, F65, F70, F67, F69, F19, F20,
F21), plus two NEW vanilla findings from the PT-43 setup (F79 trains-never-
serve-services, confirmed; F80 trains-skip-waiting-passengers,
investigating).**
Also proven this
sitting: the class-flattening runtime corollary (ENGINE_FACTS.md).**

## Disaster-system leg + drone stress harness + D08 design — 2026-07-29 (live, the project's biggest single-defect find)

One long attended session. **Two P1 defects found and one of them proven live,
end to end, with the recovery demonstrated on the user's save.** Full forensics
on the entries; this is the index.

- **F81 CONFIRMED LIVE (P1) — one stranded prediction flag was gating the
  colony's entire weather system.** `g_DisastersPredicted["DisasterMeteorStorm"]`
  sat `true` with no storm running; `IsDisasterPredicted()` therefore blocked
  rains (early-return in `RainsDisasterActivation`) and starved dust storms and
  cold waves (both scheduler loops push `wait_time` forward while it is true).
  `RemoveDisasterNotifications("DisasterMeteorStorm", MainMap)` → **rain started
  immediately**, then a toxic-rain warning, then a marsquake. 194 sols of "no
  weather ever" explained and fixed by one console line.
- **The leak is UNCONDITIONAL (grep-verified):** only three code paths ever
  remove that notification, and **the normal completion path of `MeteorsDisaster`
  is not one of them** (`Meteors.lua:242-251`). So on any map with storms
  enabled, the FIRST storm — wedged or perfectly healthy — permanently kills that
  colony's cold waves and rains. Highest-impact finding the project has made.
- **F78 REPRODUCED ON DEMAND AND LOCALIZED TO THREE LINES.** The stall is the
  unbounded drain loop `Meteors.lua:238-241`: `table.validate` works (73
  descriptors → 2) but two meteors never go invalid, so `#spawned` never reaches
  0. Hypothesis 1 was half right — not un-exitable, just unbounded. Controls:
  `single` completes cleanly; the spawn loop terminates normally.
- **New hazard for the repair: TWO storms wedged simultaneously**, and
  `g_MeteorStormStop` is a **shared global** consumed by whichever thread wakes
  first. Any bound must be per-invocation, and the fix must assume concurrency.
- **One confident theory DISPROVED by test** — we predicted a save/load inside a
  warning window would strand the flag; it does not (notification and thread both
  survive). `SavegameFixups.*` is a one-time legacy migration, not routine load
  behaviour. Recorded on the entry so it is not re-derived.
- **F82 filed (P3):** split power/life-support grid notification lingers ~a sol
  after the grid is rejoined; machinery located, updater cadence still to trace.
- ~~**Src ≠ shipped `Lua.fpk`, proven:** `GetCameraLookAtPassable` exists in Src and
  **not at runtime**, which is why bare `CheatMeteors("storm")` silently no-ops.
  Command table corrected. Treat all Src-only reasoning as provisional.~~
  **[WITHDRAWN 2026-07-29 — this was a misreading.** `GetCameraLookAtPassable`
  is a `local function` in Cheats.lua, invisible to the console *by design*,
  identical in Src and shipped. The full `Lua.fpk` extraction diff proved the
  shipped build IS Src: 2,250/2,256 files byte-identical, the 5 divergences
  engine/tooling only. The command-table correction stands on its own merits
  (always pass an explicit position). See ENGINE_FACTS.md → parity.]
- **Drone stress harness BUILT** (`TestKit/Code/91_Stress.lua`, local-only, no
  A/B owed): `SMRTest.Stress.Break/Targets/Report/Compare/HealAll/Stop`. Breaks a
  seeded deterministic set so the same save reloaded gives a true controlled A/B;
  captures every repair claim via a leaf-class pre-wrap on `Drone:Work` and
  reports **closest-hub first claims %** as the headline. *(That v1 metric was
  invalidated by the run below and the harness was REBUILT v2 on 2026-07-29 —
  see the header wrap and the D06 entry.)*
- **THE A/B RAN (2026-07-29) — NULL RESULT for D06's claim gate, and it exposed
  why.** Controlled: same quicksave reloaded, identical seeded set, both legs at
  normal speed, storages equalised. With the module ON the gate intervened
  **once** (`vetoed +1`) across 25 simultaneous malfunctions and the leg it
  arbitrates moved **58m → 57m**; the 34m total gain sits in the **hauling** leg
  D06 exempts by design, so it is variance. Cause: **0 of 25 targets were
  `no_resource` maintenance**, so `MaintenanceDroneUnload` → `StartWorkPhase(drone)`
  gave the first repair tick to the **delivering** drone every time, bypassing
  `FindTask` — **the metric measured which hub DELIVERED, not which won a
  claim** (the exact risk `HARNESS_REVIEW_PROMPT.md` §2 was written to catch).
  **Bigger finding: hauling is 3h03m of a 3h27m total — 88% of elapsed time**,
  which meets the options doc's own escalation condition and promotes D08's
  dispatcher (registration determines who can deliver) from speculation to
  evidence-backed. Full numbers and caveats on the D06 entry.
- **PT-52 sitting 3: healthy under real load** — DroneReport taken right after a
  marsquake damaged several buildings: nine hubs, `unclaimed=0` on every one,
  all laps `low`, `vetoed=3 / veto_expired=0 / moonlighted=0`.
- **D08 designed** (`DRONE_OVERHAUL_OPTIONS.md`) — extender overhaul in five
  layers with a risk table and five open questions. Origin: the user's live
  observation that extenders make the D06 problem worse. Nothing built.
- **`QA_REVIEW_PROMPT.md` written** — a one-off adversarial review prompt for a
  fresh session to QA both tracks before anything is implemented. *(Fired
  2026-07-29 late; verdict folded; file deleted per its own rule — see the
  newest wrap at the top of this document.)*
- **PT-53 PARTIAL PASS — D07 `Opt_CohortHousing` enabled live for the first time
  and works** ("it worked wonderfully"). Cross-dome consolidation confirmed from
  EVERY dome for both cohorts, over **trains, passages and shuttles chosen by
  distance**; graduation drain confirmed (with a transient homeless flicker that
  is the designed shape, recorded so it is not mistaken for a defect). Bonus:
  children reached services **via passages**, live corroboration of F79's
  passage-only service search. **No-churn also PASSED organically** — where
  cohort housing ran short those colonists simply stayed put with no hiccups,
  which is the "completely untouched when no slot exists" design confirmed at
  colony scale. **3 of 5 triggers pass; not flipped to `tested`** — the
  employed-senior exemption (A) and precedence/uninstall (E) are still owed.

## D07 build leg + two more flips — Fable, 2026-07-28 late (mixed live/game-free)

Same calendar day as the ten-flip sitting; a short live leg (user at keyboard)
followed by a user-authorized unattended build leg while they were away.

- **PT-23 PASS → F46 `tested` (archived), eleventh flip.** Both halves on the
  live 5-station network: forbidden Metals drained to 0/60 and STAYED; the
  all-five-stations-forbidden + drones-off leg proved trains dump rather than
  strand (zero loaded roamers). Isolated no-drone stations keeping stock =
  expected statics, recorded as an observation on the entry.
- **PT-09 PASS → F14 `tested` (archived), twelfth flip.** Red low-stat cell
  verified per-CELL both directions (red at Comfort 0, white on recovery).
  Two researched facts recorded: the peril statuses share a 12-36h
  per-colonist GRACE window before Health damage (StatusEffects.lua:93-98,
  then avg ~2x base rate, stacking); the fifth overview column is
  SATISFACTION (tourist-rating stat, ChangeSatisfaction zeroes gains past
  the tourist sol window) — its red 0 on every mature dome is CORRECT
  vanilla-intended rendering the F14 bug had been hiding.
- **D07 `Opt_CohortHousing` BUILT (user gave config + go the same evening:
  in-dome-first + cross-dome, Seniors+Children one toggle, then "start
  working on it" for the unattended window).** Colonist/housing-level rule,
  zero persisted state, all hooks per-call-gated: UpdateResidence post-wrap
  (in-dome move), FindEmigrationDome post-wrap (nearest-reachable cohort
  slot, tie rule bypassed; quarantine/D03/forced-dome/overpopulation
  respected), ColonistBecameYouth nudge. Mod Options toggle #6. Full notes
  on the D07 entry; PT-53 written into the checklist (5 triggers).
- **A/B pair FRESH (2026-07-28 late, 73 probes):** baseline **1/57/15/0** ·
  all-SIX-toggles **63/0/10/0 (71/71 applied)**, zero errors, both legs on
  predicted numbers. NO pre-flight owed. Two probe-side lessons from the
  leg (module itself never wrong): (a) **WithGlobals stubs cannot reach a
  game file that localizes the global at load time** — Colonist.lua:5 does
  `local IsValid = IsValid`, so stand-in probes must assert on the MODULE's
  action (absence/presence of its move), not on vanilla bookkeeping around
  plain-table stand-ins; (b) a fake colonist driven through the shipped
  FindEmigrationDome tail needs a PickEmigrationCommunity stub.
- Housekeeping: D07 config decision recorded on the entry when given
  (commit 6ca11a1); prompt un-run list updated (PT-09/PT-23 gone, PT-53
  added); Satisfaction/grace observations archived with their PTs.

## TEN-FLIP playtest sitting — Fable, 2026-07-28 evening (live, the project's most productive sitting)

One long attended session; full per-test evidence in `PLAYTEST_ARCHIVE.md`,
forensic trails on the entries. Zero pack code changed (no A/B owed).

- **Ten `tested` flips:** F68 (PT-17 capacity-edge re-run — ground settled AT
  the threshold), F73 (PT-19, both life-support gap shapes), F72 (PT-33, all
  three cases), F65 (PT-40 full procedure), F70 (PT-31 round trip), F67+F69
  (PT-16 — full-sol asteroid hold logged; manual-landing fuel ration kept and
  flown home), F19+F20+F21 (PT-43 in full). **The ASTEROID SECTION is
  COMPLETE.**
- **Validated live:** the map-switch console-death repair (workaround
  retired), the repaired AutoCargo logger (first live capture drove the F68
  re-run), the repaired CargoReady logger (leaf-class + change-only, repaired
  mid-session in a game-free break, first verdicts drove the F67 read).
- **F78:** hypothesis 1 (descriptor-validate infinite loop) REFUTED live
  (`table.validate` removes plain tables — `kept: 0`); on VeryLow the strike
  routine is statically seconds-bounded, so the 183h stall contradicts static
  analysis → on-demand repro plan banked on the entry (bracket taps +
  `CheatMeteors("single")` at empty ground).
- **NEW F79 (confirmed):** colonists never use trains for services —
  `Dome:GetService` is passage-only while the train-aware reachability serves
  only Workplace/Training/Residence. Fix = feature-completion, D-item, USER
  DECISION pending. **NEW F80 (investigating):** trains stopped 4+ times and
  skipped ~19 valid waiting passengers (full config-exonerating forensics on
  the entry; direction-blind-spot suspicion; mitigated by adding trains 2→5).
- **NEW D07 speced (user-commissioned, revised same day):
  `Opt_CohortHousing`** — colonist/housing-level rule, NO dome designation:
  cohort members in normal housing move to free Retirement Home/Nursery
  slots anywhere (in-dome reassignment first, cross-dome emigration
  second), completely untouched when no cohort slot exists; employed
  seniors exempt; graduation drains naturally; zero persisted state. Build
  awaits user go.
- **PT-52 sitting 2: healthy.** Readings `vetoed 1→9 / veto_expired 0→1 /
  moonlighted 0`, `unclaimed=0` on all seven hubs throughout (new hub 4230
  integrated); counters correctly survived a save reload and correctly reset
  on the mid-session relaunch. **Trigger B still un-run.** Log hygiene: the
  full session log swept — ZERO Lua/mod errors.
- New engine facts recorded on entries: `CheckAutoDepart` consults only the
  CURRENT side's rule set (empty side-set = designed collect-trip);
  `RoughTouchDown` storybit can strand a lander on a bare asteroid
  (`maintenance_request:SetAmount(0)` is the verified recovery);
  `Colonist:ChangeComfort(amount, reason)` is the clean stat-injection path;
  trains carry workers/trainees/migrants only (F79); the trip planner books
  tickets with no regard for actual train service.

## F68 over-draw repair leg — Fable, 2026-07-28 (game-free, post-playtest): same-day mechanical repair + fresh A/B pair

The PT-52 sitting's lander leg (PT-17 capacity edge) caught the pack's own
F68 fix over-exporting below the player's GET-WHEN-ABOVE threshold; the
repair landed the same evening once the user closed the game.

- **Root cause, live-proven before touching code:** the TAP2 console-tap
  arithmetic matched `ground + 2×aboard − threshold` EXACTLY at every
  recompute (52/72/98 at aboard 12/32/58; final ground 184−100=84) —
  **`GetTotalCargoAvailable` already counts a landed rocket's own hold**, so
  the v1 fix's aboard-into-ground addition double-counted every unit aboard
  and the request ratcheted monotonically to the hold cap. New engine fact,
  recorded here.
- **Repair (`Code/Fix_LanderCargoRatchet.lua`):** the addition
  (old :145-151) DELETED; the explicit request-floor block (never ask below
  aboard) now carries the whole F68 anti-churn fix. Header comment documents
  the discovery + repair. Parse clean.
- **TestKit AutoCargo logger repaired in the same leg** (local commit): two
  live-proven flaws — wraps the leaf class `UniversalLanderRocket` now (the
  flattening corollary made the old base-class runtime wrap structurally
  blind to real landers), and reads `self.cargo[res].requested` post-call
  (the return value it used to print is always nil).
- **A/B pair, fresh (also clears the queued pre-flight):** baseline
  1/57/14/0 · all-five-toggles 62/0/10/0 (**70/70 applied**, user's Mod
  Options toggles all on, zero pack errors, noise = the known synthetic-map
  set). The LanderCargoRatchet probe passes through the floor path
  (`request 300000 >= 300000 aboard`) — the probe needed no change, by
  design of the repair.
- **Validation debt: CLEARED 2026-07-28 (next sitting).** The attended
  capacity-edge re-run PASSed on the live colony: Concrete above 0 + Rare
  Metals above 140 with extractors replenishing mid-load; request tracked
  `aboard + surplus` (PreciousMetals 90000→92000, creeping only by the mined
  amount) instead of ratcheting; ground after departure 146 with miners
  running = settled AT the threshold. The repaired TestKit AutoCargo logger
  did the capture — its first live validation. **F68 → `tested`; PT-17
  archived.**

## D06 build leg — Fable, 2026-07-28: drone dispatch overhaul core v1 + F77 fix (user-greenlit, PT-52 pending)

Built same-day on the investigation verdict and the user's design review
(their proximity-cascade idea became option H in the study; the shipped claim
gate is its veto variant — reversible and orphan-proof, chosen for v1).

- **`Code/Opt_DroneOverhaul.lua`** (opt-in, off by default, Mod Options
  toggle "Drone dispatch overhaul (experimental)"; hooks installed at
  classdef time, gated per call on IsActive; NO persisted state):
  1. closest-fleet-first claim gate — chained wrapper on
     `TaskRequestHub:FindTask` (sole caller = drone auto-Idle, so player
     orders untouched): repair/clean work offered to a non-closest covering
     hub is withheld while the closest hub has idle drones; per-request
     strike cap (4 polls / 30s decay) makes starvation impossible;
  2. repair moonlighting — chained POST-wrapper on `Drone:Idle` (the body
     falls through exactly when workless — verified engine fact): workless
     drones take unclaimed repair/clean work of SATURATED neighbor hubs
     within 30 hexes and their own restrict area, vanilla-style SetCommand;
  3. `SMRFixPack.DroneReport()` telemetry (always on, read-only): per-hub
     state + module counters vetoed/veto_expired/moonlighted.
- **`Code/Fix_ExtenderFlapChurn.lua`** (F77, default-on fix): extender
  working-flaps now debounce+coalesce the whole-hub rebuild (2s, per root
  hub, chains resolved) instead of tearing it down twice per blip.
- Wire-up: items.lua toggle + metadata `default_options.DroneOverhaul` +
  code list. Parse sweep: all 4 touched files pass (python luaparser).
- Scope guards worth knowing when judging PT-52: rockets/rovers/construction/
  hauling all exempted by design; the claim gate cannot veto player orders
  structurally (FindTask is not on that path); toggling off restores vanilla
  instantly (registration layer untouched).
- Docs (full pass, same day): D06 entry + index row (BUGS), F77 flipped to
  `fixed` (row + tag), options doc carries the build note. **PT-52 is a full
  checklist procedure now** (PLAYTEST_CHECKLIST, optional-modules group):
  CAN/CANNOT-do lists, Trigger A passive watch, Trigger B controlled off/on
  A/B demo, Trigger C regression watch, result lines, knob log line.
  MOD_DESCRIPTION got the player-facing F77 bullet (Buildings & economy) and
  the "Drone dispatch overhaul — experimental" module block.
  FABLE_NEXT_PROMPT rewritten post-build (PT-52 centerpiece + assistant
  briefing notes, 65/70 module counts, D06 read-list pointers);
  DRONE_INVESTIGATION_PROMPT retired/deleted. `DroneReport` upgraded to
  print ON-SCREEN (ConsolePrint) AND to the log — the ListFixes lesson,
  applied before it bit.
- The user expects multiple iterations across sittings; knob changes get
  recorded on the D06 entry (mechanical, assistant may land same-day);
  design-level changes (H-v2, registration-H, balancer C) stay user
  decisions per the options doc.
- Testing debt, stated: no TestKit probes for the module yet (attended
  playtest is the v1 validation instrument; probes come with the iteration
  that stabilizes the design).

## Drone task-assignment investigation leg — Fable, 2026-07-28 (game-free, docs-only): verdict in

The `DRONE_INVESTIGATION_PROMPT.md` kickoff, executed as specced (no game, no
loadable-code edits, Src read-only). Full verdict + trace + instrumentation
plan live on the BUGS "Not yet swept" DroneControl bullet; **F77** filed
(index row + entry). Headlines:

- **Architecture verdict: working-as-coded, but with NO cross-hub locality
  anywhere.** Assignment is PULL and own-hub-only — `Drone:Idle`
  (`Drone.lua:564-641`) polls `command_center:FindTask(self)` (`:621`), the
  single FindTask call site in Src; the match itself is the C-side
  `Request_FindTask` over the hub's own queues (ordering/distance policy
  engine-internal — recorded as unverifiable from Lua). A building in overlap
  registers with EVERY covering hub and its (shared, C-side) request objects
  sit in every such hub's queues; the claim is first-poller-wins at command
  start and **held through the whole approach** (`Drone:Work`,
  `Drone.lua:898-924`); maintenance repair requests are **max_units = 1**
  (`RequiresMaintenance.lua:82`), so one far drone locks out a fleet parked
  next to the job. No handoff, stealing, or rebalancing exists anywhere.
- **Extender transparency CONFIRMED** (the user's hypothesis): both connect
  directions register the far HUB itself on the building
  (`DroneHubExtender.lua:156-160` building-side recursion;
  `DroneControl.lua:315-325` hub-side recursion) — extender-mediated coverage
  is indistinguishable from native in every match structure. Extenders do NOT
  extend drone movement: `const.DroneRestrictRadius` (100 hexes-worth) is
  anchored on the HUB position (`Drone.lua:227-230`, `_GameConst.lua:71`);
  post-SignalBoosters a 2-extender chain can register buildings a hub's
  drones can never legally reach (suspected F55-feeder, engine-side check —
  flagged for live).
- **NEW F77 (defect, provable):** every extender working transition (power
  blip, malfunction, repair, toggle — both edges) triggers a FULL
  disconnect+reconnect of the entire uplink hub's requester set
  (`DroneHubExtender.lua:171-178` → `DroneControl.lua:441-450`), Idle-kicking
  every drone en route to any connected building (`:720-729`) and burning
  O(B×D) + queue-rebuild work per flap. Reproduces both observed halves on
  its own. Fix sketch: debounce wrapper (user decision).
- **The live starvation stays two-hypothesis** until one attended sitting:
  (a) registration gap (starving buildings outside hub 2608's circle, inside
  the far hub's extender-stretched coverage — pure design) vs (b) claim
  lockout (in both queues, far fleet wins the claim race every chunk). The
  banked `target:0` read is consistent with both. **R1-R7 console reads** (on
  the bullet; sandbox-verified, incl. a `RequestAssignUnit` claim tap — no
  file-local alias in Drone.lua, so a console global wrapper is seen) settle
  it; R7 is the hub-A/hub-B/extender repro with `CheatMalfunction`.
- **Performance answer (the user's second observation):** per-idle-drone
  FindTask polls scan the hub's full queue set every ~3s and overlap
  multiplies queue content (k-hub overlap ≈ k× colony-wide scan work); the 1s
  empty-queue throttle can't engage while any drone holds unreachable-cache
  entries (`Drone.lua:630`); reconnect storms (radius change, F77 flaps, and
  `OnMsg.DepositsSpawned` reconnecting EVERY hub at once,
  `DroneHub.lua:188-199`) are O(B×D)-grade each. Range × drones × requests,
  exactly as reported.
- **Nothing was built** (per spec). Build decisions for the user: F77
  debounce (plain repair), and the locality levers — cross-hub idle-pull
  pre-wrap on `Drone:Idle` for (a) vs near-idle claim veto on
  `Drone:Work`/`PickUp` for (b) — which are assignment-POLICY changes
  (D-item territory). All sketches + risk statements on the bullet/F77 entry.
- **Follow-up same leg (user-commissioned): `docs/reports/DRONE_OVERHAUL_OPTIONS.md`**
  — the D06-candidate feasibility study for an optional overhaul toggle.
  Options A-G with verified patch points; key new engine findings:
  `Drone:Idle` falls through (returns) exactly when no work was found, so a
  chained POST-wrapper is a legal dispatch hook (the F73 pre-wrap-only rule
  is for command bodies that always SetCommand); `Drone:Work`/
  `ApproachWrapper` never consult `command_center` (cross-hub execution is
  clean); `Drone:SetCommandCenterUser` (`Drone.lua:2687-2694`) is the
  vanilla migration path. Recommended order: telemetry → repair
  moonlighting → migration balancer; claim-veto/handoff gated on the R1/R3
  live answer. USER DECISION before any build.

## Mod Options build leg (D05) — Fable, 2026-07-27 late: in-game enable surface for the optional modules

Triggered live: the user sat down for Group 8 and had **no main-menu console**
— and the briefed console route was falsified outright (the Opt_ gates run at
mod code load during startup, BEFORE the main menu; that is why the A/B
harness always needed the `97_OptInLeg.lua` flag FILE). Release context made
it a blocker: Steam Workshop + Paradox Mods, and **Paradox delivers PS/Xbox,
which have no console at all**. User picked "build now" over "temp file for
tonight". Full spec + Src evidence on the **D05** BUGS entry; summary:

- **items.lua (new):** four `ModItemOptionToggle`s (names == registry ids) put
  the pack on **Options → Mod Options** (main menu and pause menu, gamepad
  capable). **metadata.lua** gains the matching `default_options` table (what
  `HasOptions()` reads — without it the page ignores the pack).
- **00_Core:** `SMRFixPack.OptionEnabled(id)` (pre-load `SMRFixPack_Optional`
  OR the saved toggle — the values load before mod code, `CurrentModOptions`),
  `SMRFixPack.IsActive(id)`, defs retained, and an `OnMsg.ApplyModOptions`
  reconciler: ON = re-arm installed hooks or apply now (+`on_activate`); OFF =
  registry status flip (+`on_deactivate`). **Every optional module's wrappers
  consult IsActive per call**, so toggles are live in both directions with no
  unhooking. D04 flips the `build_once` template flag in its callbacks
  (restore guarded so a third-party limit mod is never stomped).
- **D04 cosmetic repair (pre-existing, exposed by the leg):** the transient
  pre-DataLoaded "ArtificialSun not found" detail no longer sticks on
  `ListFixes`; miss only recorded post-DataLoaded, cleared when the template
  appears. Engine fact: **DataLoaded fires more than once during startup; a
  template can miss the first pass.**
- **TestKit:** new probe `OptionsMenu` (60_Probes_Opt.lua) asserts the wiring
  in EVERY leg — metadata defaults, the four toggle items, the 00_Core bridge
  — and FAILs discriminatingly in baseline (registry absent). **72 probes.**
- **Legs (2026-07-27, logs Mars.exe-20260727-…):** parse sweep 82 files/0
  failures; baseline 21.20.32 = 1/**57**/14/0; fixed 21.21.51 = **58/0/14/0**
  (64/68); opt-in 21.34.28 = **61/0/11/0** (67/68) — all module probes +
  OptionsMenu PASS; gates log the new "enable it in Options → Mod Options"
  reason.
- **Docs same-commit:** D05 entry + index row, **PT-51** (Mod Options page
  eyes-on — now the FIRST step of the Group 8 sitting, since it is the enable
  mechanism), Group 8 preamble rewritten, MOD_DESCRIPTION optional-modules
  enable text now points at Mod Options (console-only instructions removed
  from player-facing text).
- **PT-51 first sitting, same night: `ListFixes()` crash found live and
  repaired** — latent since the 2026-07-25 F75/F18 status repairs
  (`entry.detail = nil` writers vs a concat in ListFixes; full trail on the
  D05 entry). Both writers now use `""`, ListFixes nil-tolerant. Takes effect
  on the user's next relaunch; **A/B pair re-verify queued for the next
  game-free window** (cosmetic to the probes — nothing reads ListFixes).
- **PT-51 COMPLETE, same night → D05 `tested` (archived):** all four toggles
  + tooltips good; live both ways proven twice (ClassicRockets on
  mid-session, MultipleSuns off/on vs the build menu); full shutdown +
  relaunch kept every toggle and the startup log shows all four modules
  self-activating from saved values; ListFixes printed 2×68 clean lines
  post-repair; log swept clean twice. **The PT-49 row reposition is also
  verified** ("UI good for dome" — the policy row now sits with the toggle
  group).
- **PT-49 first sitting, same night: core behavior PASSing** (closed
  high-comfort dome: zero move-ins, commute/services normal — screenshots).
  Cosmetic finding repaired same day: the policy row now inserts directly
  after the shipped accept-colonists toggle instead of below the stat bars
  (array reposition; trail on the D03 entry). Position re-check + the
  remaining PT-49 steps (arrivals, manual relocation, tourists, quarantine
  independence, MicroG row, uninstall) continue after the next relaunch.
- **PT-50 PASS in full, same night (the Group 8 sitting, running on the new
  Mod Options toggles) → D04 `tested`, F39's absorbed fix play-verified:**
  sun #2 built through the normal menu multiple sectors from #1; night
  production beside a sun matched the banked PT-26 signature exactly (3.6/9 @
  −21%; other sector 10 @ 0% — no atmospheric penalty there); sunless panels
  closed to 0 at night (not over-broad); save/reload clean; limit off/on
  verified LIVE via the toggle (doubles as PT-51 live-toggle evidence).
  Section archived. PT-51 partials recorded (page + live both ways verified;
  persistence-across-restart + log check remain). **Also observed live: an RC
  Terraformer (dozer) + waste-rock heap showed the F76 detached-hex picker
  rendering — Load-on-WasteRock is vanilla dozer behavior (RCTerraformer.lua:33,
  :224-237; pack ruled out, F74 wrappers refuse-only), and the picker surface
  DOES extend to the dozer path (user confirmed: hex appeared on CLICK) — F76
  addendum filed: any vehicle whose click-load reaches a storage-depot-class
  object is affected; loose rubble piles safe; the same TransferResources
  command workaround applies.**

## Build leg — Fable, 2026-07-27 late: F61 deletion + D02/D03/D04 built, A/B renumbered

The queued game-free build leg, executed as speced (all specs were on the BUGS
entries). Game never touched a save; three unattended `-smrautorun` legs only.

- **F61 retirement mechanics DONE:** `Code/Fix_HomeDomeMigrationGate.lua` + its
  metadata line deleted (git history restores them); the TestKit
  `HomeDomeMigrationGate` probe deleted with it (it tested the removed behavior —
  not an F10-style canary).
- **D02 `Opt_AcknowledgedWarnings` BUILT** (opt-in, off by default): dismissal of
  `NotWorkingBuildings` stamps every listed building
  (`SMRFixPack_ack_notworking`, absent-tolerant) and SKIPS the shipped
  4-game-hour whole-id window; stamped buildings' re-adds are dropped until
  recovery clears the stamp. Three chained wrappers on the notification helper
  GLOBALS (`SuppressNotification` — sole caller runs only under `dismissed`, so
  it IS the dismissal hook; `AddObjectToNotification`;
  `RemoveObjectFromNotification` — none is file-local in Notifications.lua, F22
  precedent). Only that one id is touched.
- **D03 `Opt_ResidencyControl` BUILT** (opt-in): new per-dome/habitat "closed to
  new residents" policy (`SMRFixPack_closed_to_new_residents` on the Dome,
  absent-tolerant). Gates: post-wrap `Community:CanAcceptNewColonists`
  (voluntary resettlement — only Src caller is FindEmigrationDome's filter) +
  post-wrap the global **`ChooseDome`** for arrivals. Build-time survey
  refinement: `GetDomesReachableByColonists` was rejected as the arrival patch
  point — it also feeds construction range display and worker checks, which must
  keep seeing closed domes; `ChooseDome` is the single choose-a-new-home funnel
  (rockets ×3, landers ×3, factory androids, stranded re-homing). `safety_dome`
  passes through unfiltered (no suffocation), `traits.Tourist` exempt (hotels).
  UI: post-wraps on `sectionDome:Init`/`sectionMicroGHabitat:Init` append the
  row; the toggle rides shipped `Community:TogglePolicy`/`SetPolicyState`
  (FX, Ctrl+click broadcast, rogue-dome UI lock for free). Closed state styled
  yellow/limit so it cannot be read as the red quarantine row.
- **D04 `Opt_MultipleSuns` BUILT** (opt-in): lifts
  `BuildingTemplates.ArtificialSun.build_once` from OnMsg.DataLoaded/DataChanged
  (handlers gate on registry status = opt-in + veto covered, F75 lesson; menu
  re-reads `CanBuildOnlyOnce()` live) AND absorbs the F39 wrapper + LoadGame
  sweep unchanged. `Fix_SecondArtificialSun.lua` DELETED; its probe reworked to
  the ClassicRockets SKIP-unless-opted pattern.
- **TestKit:** new `Code/60_Probes_Opt.lua` carries the three module probes
  (each SKIPs with the opt-in reason unless active); the two retired probes
  removed in place with dated tombstone comments.
- **Parse sweep:** 81 Lua files across both mods, 0 failures.
- **A/B pair + opt-in leg (2026-07-27, all clean, NEW EXPECTED NUMBERS —
  71 probes total now):**

| Leg | Log (Mars.exe-20260727-…) | Result |
|-----|---------------------------|--------|
| Baseline (pack emptied) | 20.38.21 | 1 PASS, **56 FAIL**, 14 SKIP, 0 ERROR |
| Fixed (default config) | 20.39.59 | **57 PASS, 0 FAIL, 14 SKIP, 0 ERROR** — 64/68 active (4 opt-in inactive) |
| Opt-in (three new modules on via temp flag file) | 20.41.49 | **60 PASS, 0 FAIL, 11 SKIP, 0 ERROR** — 67/68 active; all three new probes PASS incl. the live template lift |

  Renumbering from the old 1/58/11 · 59/0/11 (70 probes): −1 armed probe (F61
  deleted), F39's probe moved to opt-in SKIP, +2 new opt-in SKIPs (D02, D03).
  The 14 default-leg SKIPs = 10 [install] + 4 opt-in modules. Baseline's 1 PASS
  is still the FactionFundingCheck canary. Log noise unchanged (synthetic-map
  Flight.lua blocks in both legs; the quit-time TestKit mod-error artifact).
  Opt-in mechanism for the leg: temporary `Code/97_OptInLeg.lua` in the FIX
  PACK's code list right after 00_Core (set `SMRFixPack_Optional` before the
  Opt_ files load) — deleted after the leg; TestKit autorun flag line reverted.
- **Registered modules now 68** (67 − 2 deleted + 3 new); 64 active by default.
- **Docs same-commit:** BUGS index rows + heading tags (F39, F61, D02, D03,
  D04), MOD_DESCRIPTION Optional-modules section rewritten with the three new
  module blurbs (feature framing; F39 bug-fix bullet removed, sweep-list phrase
  dropped, D02 draft note resolved), PLAYTEST_CHECKLIST gains **Group 8:
  PT-48 (D02), PT-49 (D03 — first added infopanel row, needs eyes-on),
  PT-50 (D04, reworked PT-26 vs the banked single-sun baseline)**.
- **F76 was deliberately NOT touched** — attended sitting only (hard-lock
  vector; see the F76 entry and the prompt).

## Playtest marathon — Fable, 2026-07-26/27: 12 PTs resolved, F10 retired, D02 unblocked

One long interactive run with the user at the keyboard and this session driving
console instrumentation. Full per-test evidence is in `docs/PLAYTEST_ARCHIVE.md`
(new file — completed checklist sections move there, reporting-protocol step 8);
one-line summary here:

- **Flipped `tested`:** F03 (PT-02), F05 (PT-05), F12 (PT-07), F13 (PT-08),
  F44+F45 (PT-03), F47 (PT-45), F50 (PT-04), F51 (PT-12), F54 (PT-34),
  F66 (PT-41); **F52 `tested*`** (PT-13). F49(b) resolved no-defect (PT-46).
- **F12 second defect — the session's big catch (PT-07 first run):** the fixed
  updater's maintenance loop and food branch share the `"Food"` object key on
  the SAME notification; the maintenance else-path deleted the food branch's
  entry hourly → notification destroyed/recreated with FX + voice every game
  hour (voice plays only on whole-notification creation; VoicePerObject false).
  Latent in vanilla (broken math meant nothing could ever be added). Diagnosed
  by live console wrappers after five falsified hypotheses (dismissal cycle,
  threshold flap, object validation, stale second body, cross-city removal —
  full trail on the F12 entry). Repair: maintenance loop skips `"Food"`.
  **A/B clean 2026-07-27:** baseline 11.45.34 = 1/58/11/0; fixed 11.47.09 =
  59/0/11/0, 66/67 active. Re-run PASSed all behaviors incl. silent organic
  clears on both branches.
- **F10 CLOSED `wontfix` + DELETED (PT-36):** the three funding calls returned
  0 cleanly over a maximally nil organic history, and later read a real
  $544.5M tourist payout correctly — premise dead both ways.
  `Fix_FactionFundingCheck.lua` and its commented metadata line removed
  (git history restores both); the TestKit probe stays as a canary (it is the
  baseline's expected "1 PASS" — documented A/B numbers unchanged).
- **D02 gate DONE with a premise CORRECTION (PT-38):** the dismiss window is
  **120,000 GAME-ms = 4 game hours**, not 2 real minutes (`GameTime` defaults
  true; three live timestamped dismissal→return pairs = 120,000 +
  time-to-next-attempt, every in-window re-add attempt observed BLOCKED;
  suppression is per notification id). At ultra the re-nag is every few REAL
  seconds — D02's case is STRONGER. `Opt_AcknowledgedWarnings` build unblocked.
- **PT-06 (F08) DONE 2026-07-27 (later) → F08 `tested`:** 5★ 10-tourist
  departure paid at Earth ARRIVAL "+23 applicants, $544.5M" (2.3/head =
  top-tier); the tanked half (a 25-tourist group into a stripped dome —
  homeless, services off, Earthsick early leavers) paid "+7 applicants,
  $94.5M" = **0.28 applicants/$3.78M per head — an 8× per-head split**.
  Mechanics confirmed from Src during the run: departure rewards walk every
  boarded Tourist with no sols/reason filter (early leavers count); any stat
  < 30 caps the rating at the 2★ tier (`HolidayStatCapRating`); 7-from-25 is
  in band for the corrected mostly-1★ roll (~10 expected) and ~3σ below the
  shipped inverted roll (~15 expected) — corroborating evidence, not noise.
  Two cosmetic vanilla quirks
  recorded in the archive entry (overstay-cycle button no-ops silently on an
  empty sol-10+ bucket and only cycles the current map; sols-based tooltip
  labels early-leavers "Enjoying their holiday").
- **PT-26 (2026-07-27, later): F39's premise UNREACHABLE in the unmodded game →
  D04 filed (user decision).** The Artificial Sun is a `build_once` wonder
  enforced colony-wide incl. construction sites (`BuildMenu.lua:711-719`
  counting `UIColony.labels`; the tester's build menu refused sun #2 with sun
  #1 standing) — two suns can never coexist, so the F39 fix is latent hardening
  vanilla can never exercise. Resolution: **D04 `Opt_MultipleSuns`** — opt-in
  module that lifts the limit (`BuildingTemplates.ArtificialSun.build_once =
  false`, read live by the menu — verified in-session) AND absorbs the F39
  binding fix, so the pack provides the condition its fix needs and spares
  players a third-party limit mod that would hit the vanilla `[1]` bug.
  Single-sun baseline banked (night production at −21% atmospheric beside the
  lit sun). Standalone fix file deletion + module build queued for the
  game-free leg. Spec on the D04 entry.
- **F76 NEW FINDING (2026-07-27, found live during PT-39 setup): the RC
  Transport depot resource picker renders far from the cursor and cannot be
  clicked** (vanilla, P1). "Load from depot" looks completely broken — icon +
  noise, nothing loads — while ground piles work (no picker on that path). Live
  instrumentation proved the `ResourceItems` dialog opens and STAYS ALIVE
  (`box=(886,13)-(1054,442)`, 1 item) but draws as a giant detached hex near
  the top of the screen, and clicks on it fall through to the map (selection
  churn then closes it via its own `OnMsg.SelectionChange`). Suspected
  `terminal:GetMousePos()` vs scaled-UI coordinate mismatch (~1.88 display
  scale maps the box back onto the true cursor position); 1080p error is small
  enough that it passed QA. Pack ruled out (all wrappers pass-through). Also
  affects the multi-resource unload and route pickers. Command-level workaround
  verified. **Wave-6 build candidate** (`Fix_ResourcePickerAnchor`); PT-39's
  depot control half is blocked on it (trade-rocket half unaffected).
  **User's release warning, recorded: this WILL draw false bug reports against
  the pack** — MOD_DESCRIPTION carries a draft-note for a "known vanilla
  issue" explainer (D02 precedent). Full forensics on the F76 entry.
  **Escalations (same day, later):** the multi-resource UNLOAD surface confirmed
  by play; environment pinned (fullscreen 3840×2160, UI Scale ~80-85%); and the
  broken picker can **HARD-LOCK the UI** (every MouseEvent erroring on a
  destroyed window in the modal/anim chain, `XWindow.lua:1154` — Alt-F4
  required, session lost). Live prototyping also established the dialog's own
  scale is applied AFTER Init (Init-time anchor conversion is a no-op — the
  repair belongs in/around UpdateLayout). **Process decision: no further live
  UI-internals prototyping on play sessions; F76 repair is an attended
  game-free leg task.**
- **PT-39 (2026-07-27, later): F74 → `tested`.** A landed TRADE rocket was
  fully refused by the RC Transport cursor ("treats it like normal terrain")
  AND by the route path — the route endpoint fell back to a ground position
  and the cargo was dumped at the pad, rocket untouched (the route handler
  only stores targets the guarded interaction check approves). Controls
  clean: ground-pile pickup + depot loading via route mode both work (the
  route path skips F76's broken picker for single-resource depots,
  `RCTransport.lua:466-476`). Cosmetic aside recorded: rovers clip through
  the landed event rocket's model.
- **Engine/tooling facts learned (also in the prompt + command table):**
  infopanel cheat buttons need `Platform.cheats = true` AND ride the game-time
  sync queue (dead while paused); tourists are 5% of applicants and the
  passenger filter EXCLUDES the Tourist trait by default (`initial_filter`);
  tourist stay is 5-10 sols; tourism rewards fire at Earth arrival; funding
  history is a 12-sol ring (`Funding.lua:86`); `CityStart` fires at
  map-generation time — use `InGameInterfaceCreated` for UI-ready work (TestKit
  console repair 2026-07-26); TestKit gained `SMRTest.Cls`.
- **Docs restructure:** completed playtests + evidence now live in
  `docs/PLAYTEST_ARCHIVE.md`; the checklist carries only un-run work
  (reporting protocol step 8 keeps it that way).
- **PT-14 (2026-07-27, after the session wrap): F61's premise FALSIFIED →
  CLOSED `wontfix` (user decision same day), community ask re-filed as D03.**
  The accept-colonists toggle is a **quarantine**: its OFF state is titled
  "Quarantined" and the rollover promises "Colonists are not allowed to enter
  or leave" (reused original-game T-ids — carried-forward wording);
  `Colonist:FindEmigrationDome` enforces it with the literal comment
  "quarantine, no one enters or leaves" (`Colonist.lua:2632-2634`). The lockdown
  the tester observed is designed behavior, and the shipped fix half-SUBVERTED
  it — worse, a use-case survey found scripted content that depends on the seal
  (Wildfire's dome-local infection spread `Traits.lua:1155-1173`; the RogueDome
  story bit FORCE-quarantines a renegade dome via `SetBuildingRogueState` →
  `Dome:SetUIInteractionState`; arrival routing's `is_welcoming_community`).
  **Resolution: `Fix_HomeDomeMigrationGate.lua` deletion STAGED (F10 precedent;
  needs a game-free leg, A/B numbers shift by one probe), and the real community
  ask — block move-ins WITHOUT locking commute/services — is filed as D03
  `Opt_ResidencyControl`:** a new per-dome "closed to new residents" policy row
  appended by post-wrapping `sectionDome:Init` (the infopanel section is a plain
  Lua class building rows imperatively — verified), gating
  `Community:CanAcceptNewColonists` + the arrival path, quarantine untouched.
  Full spec on the D03 entry; build queued for a game-free leg alongside D02.
- **PT-24 (2026-07-27, later): F36 → `tested`, both halves.** Geologist demand
  went **11 → 0 at the ExtractorAI grant with every other row identical**
  (before/after screenshots — the user reloaded a pre-tech save for the
  baseline, which also disproves over-exclusion since the pack was active both
  sides); multiple `CheatCompleteTraining` rounds across two universities
  graduated **38 engineers + 2 medics, zero geologists** (tallies from the
  universities' `trained_specialists`, captured in log
  Mars.exe-20260727-15.19.26). Setup gotcha found live and corrected in the
  checklist command table: **`CheatResearchAll()` skips undiscovered
  breakthroughs** (`Cheats.lua:84` discoverable-or-discovered gate) — grant
  directly via `UIColony:SetTechResearched("<Id>")`; PT-27's Biorobots route
  corrected to `ThePositronicBrain` in the same pass.
**ONE live prompt (updated 2026-07-28 — post-D06 build):**
- `docs/prompts/FABLE_NEXT_PROMPT.md` — playtest-standby assistance: the user plays,
  the session drives console instrumentation and processes results live.
  Rewritten 2026-07-28: PT-52 (D06 overhaul watch-and-judge) is the board
  centerpiece with assistant-side briefing notes; carries the queued A/B
  re-verify as pre-flight (module counts moved to 65/70 — probe numbers
  unchanged), the F76 avoidance rules, and the attended-sitting spec.
- Retired prompt files (each done and deleted/superseded):
  ~~OPUS_BUILD_PROMPT~~, ~~FABLE_QA_PROMPT~~ (2026-07-25),
  ~~FABLE_PLAYTEST_PROMPT~~ (merged into the one live prompt),
  ~~DRONE_INVESTIGATION_PROMPT~~ (2026-07-28 — its verdict, F77, and the
  D06 build all landed; the R1-R7 forensics it produced live on the BUGS
  DroneControl bullet, and PT-52 carries the live half).
BUGS.md is
the canonical defect tracker, FIX_POLICY.md the patching rules, WORKFLOW.md the
dev/test/release process, RESEARCH.md the lead catalog (incl. ChatGPT dossier
cross-check), MOD_DESCRIPTION.md the player-facing mod-page draft (update its fix
list in the same commit that implements a fix; only `tested` fixes ship in the
final text), TESTING.md the force-the-bug test plan, CHEATS_INVENTORY.md the
shipped cheat/debug surface the tests drive.

## Follow-up session — Fable, 2026-07-26: F02 hunt + watchdog, F66 reclaim, F47 composition, version tags — A/B CLEAN

**Task 1 — F02 regression hunt (PT-01 FAIL, no reloads).** Every static explanation
was FALSIFIED against the playtest log (Mars.exe-20260725-19.04.10) — full record on
the F02 entry. Established: one uninterrupted session (single `Load Game:` marker,
day counters monotonic to 36, wave-3 roster); no `[LUA ERROR]` anywhere near the
stall; the tower wait-math is bounded (warning = Min(6h+12h·3, 75h) = 42h, two sleeps
total ≤ spawn+1s ≤ 60h on Meteor_VeryHigh); the descriptor-nil day-loop needs
Atmosphere > the **80%** MeteorStormStop threshold (TerraformingDisasters.lua:69,
TerraformingParam.lua:80-84) — impossible at sol 12; nothing in Src or either mod
deletes/restarts the thread mid-game; the PT-03 track debris postdates the silence.
Bonus finding: the first MeteorStorm (birth_hour = 250h + 0..25h) was due in the SAME
window and never visibly fired — BOTH disaster threads went quiet at t≈8.2-8.3M, so
the mechanism sits outside both loop bodies (scheduler/persist side) and needs a live
capture. **Root cause NOT pinned; the rework captures it next time:** heartbeat
phases in the thread body (zero closure upvalues — the persisted thread keeps the
engine-proven persistence shape), loud top-of-body exits, a daily OnMsg.NewDay
watchdog (`SMRFixPack.MeteorsWatchdogCheck`, threshold spawn+random+75h+1 sol, gives
up loudly after 3 restarts, respects the fix's status — F75 lesson) that logs
**thread ALIVE-but-stuck vs DEAD + last phase** before restarting, and a LoadGame
necropsy of the persisted thread — loading the user's sol-36 save answers
dead-vs-stuck directly. Probe reworked install→behavior (drives the watchdog with a
synthetic stale heartbeat; discriminates in the retail sandbox instead of SKIPping).

**Task 2 — F66 rebuild trigger (user decision: repair).** Landed in
Fix_TrackConnectorPingPong.lua: post-wrap of `TrackConnectedObjBase:Done` (declaring
class; destructor, not command-killed) records the dying building's connector hexes
before the shipped body runs, then `SMRFixPack.TrackConnectorReclaim` queries each
hex with `map:MapForEach(pos, "hex", 3, "TrackConnectedObjBase", …)` (spots reach
≤ ~2 hexes; no global rebuild) and schedules the engine's own deferred idiom with
in-thread revalidation (TrackElement.lua:194-198) for every other live,
non-destructing candidate; guarded CreateConnectorElements makes re-runs idempotent;
done_map early-returns. Probe extended: exactly one rebuild scheduled (live
neighbour), dying self + destructing excluded, hexes deduplicated.

**Task 3 — F47 composition under-refunds (both audit MEDIUMs).** Landed in
Fix_TrackSalvageRefund.lua: the stand-down test is now the `demolishing` stamp
`TrackBase:OnDemolish` writes (Track.lua:250 — survives object death), so a
trim-to-empty (dies via CanDelete→DoneObject, no OnDemolish) refunds instead of
being misread as "already handled"; map/drop-pos captured pre-orig. The
construction-site early-return is narrowed to the repair-site delegation only —
plain sites fall through and their zone's stamped completed elements are accounted
(no double-refund: sites never carry stamps). Details on the F47 entry.

**Release item:** all full-replacement headers now name the game version the copy
came from — **game 1.0.7.396349** (was "shipped Src, 2026-07" / "post-1.0.7").

**A/B pairs (both clean; probe-count change is by design: the F02 probe moved from
install-SKIP to a discriminating behavior probe, so 12 SKIP → 11, 57 FAIL → 58):**

| Leg | Log (Mars.exe-20260726-…) | Result |
|-----|---------------------------|--------|
| Baseline #1 (pack emptied) | 00.06.11 | 1 PASS, 58 FAIL, 11 SKIP, 0 ERROR |
| Fixed #1 (F02+F66 in) | 00.08.03 | **59 PASS, 0 FAIL, 11 SKIP, 0 ERROR** — watchdog exercised end-to-end in-log |
| Baseline #2 (after F47 + version tags) | 00.11.46 | 1 PASS, 58 FAIL, 11 SKIP, 0 ERROR |
| Fixed #2 (everything in) | 00.13.02 | **59 PASS, 0 FAIL, 11 SKIP, 0 ERROR**, 66/67 active (ClassicRockets opt-in) |
| Baseline #3 (after the seed-crash repair) | 00.48.22 | 1 PASS, 58 FAIL, 11 SKIP, 0 ERROR |
| Fixed #3 (seed repair + sweep extension in) | 00.50.08 | **59 PASS, 0 FAIL, 11 SKIP, 0 ERROR**, 66/67 active |
| Baseline #4 (after the F18 savegame sweep) | 11.33.34 | 1 PASS, 58 FAIL, 11 SKIP, 0 ERROR |
| Fixed #4 (F18 sweep in) | 11.34.58 | **59 PASS, 0 FAIL, 11 SKIP, 0 ERROR** — F18 probe verifies the sweep both ways |

Parse sweep: every .lua in both mods parses (python luaparser).

**Live playtest, same night (user on the sol-36 save, results processed live):**
- **F02 necropsy answered: the wedged Meteors thread was ALIVE** — "persisted
  Meteors thread on load was alive" — a live thread whose wake-up never came
  (scheduler/persist side), not a dead one. Post-load natural gaps **+49h and
  +40h**, both in band; >42h is impossible under the broken code with 3 towers, so
  the cadence+towers check is satisfied on real play. Watchdog reported `healthy`.
  Also confirmed: single meteors get NO tower-scaled warning banner in the shipped
  game (the singles thread posts no notification; only the ~30 s Predict marker,
  and only with objects in the blast area) — the PT-01 checklist expectation was
  corrected accordingly (towers' lead shows in the STORM countdown).
- **PT-03 F44 halves PASS:** the load sweep removed the 40 orphaned elements from
  the first attempt; repeated build → salvage → rebuild cycles on straight AND
  curved tracks clean; train survives; **partial-salvage Metals refund observed
  live** (F47's half B).
- **New defect found during the F45 attempt, repaired same night (seed crash):**
  destroying a repair site in the deletion zone ALSO destroys its broken twin
  (TrackGridElement:Done, TrackElement.lua:200-201); the twin shares the site's
  node_idx and can sit just outside the zone at the seed index, and the shipped
  blind seeds (`all_elements[last]`/`[first]`) then crash ExpandTrackFromElement
  on a dead element (TrackElement.lua:718-719, `map` nil — mod-flagged MouseEvent
  error; unreachable in vanilla because broken tracks were unsalvageable before
  F45). Repair in Fix_TrackSalvageWipe.lua: seeds walk outward to the first
  still-VALID survivor, a side with no survivor is tolerated (empty new_track
  destroyed), and the LoadGame sweep now ALSO purges destroyed entries left
  inside track arrays by the aborted split (log line reports both counts —
  expect it on the user's save). **F45's salvage step remains the open PT-03
  item** (retry procedure written into the checklist).

**Open for the user after this session (updated 2026-07-26 late):** PT-01 longer
silence-watch only (cadence, tower warning lead AND necropsy all verified live;
the watchdog self-reports if the wedge recurs); rest of the merged-pack
checklist; PT-36/37/38 gates; MarsDebug attended [install] pass for wave-4/5.
**DONE since this record was written (commits 4310fb2..bc4e828, same day):**
PT-03 F45 retry PASS → F03/F44/F45/F50 `tested`; PT-45 PASS → F47 `tested`;
PT-46 PASS → F49(b) resolved no-defect; PT-01 tower-extended ~42h storm warning
banner verified live. Those commits flipped the BUGS.md detail headings but not
the index rows; the rows were synced in the follow-up doc-sync commit.
**PT-41 PASS (recorded 2026-07-26 later) → F66 `tested`:** shared hex stable, no
connector churn in the 11.48.31 log; demolishing one building left the survivor
connected ("became its own node but stayed connected … no weird visuals" — the
reclaim repair); plain-tile control clean.
**PT-07 first run FAILED the steadiness half (2026-07-27) → F12 second defect
found + repaired, A/B PENDING:** the Food warning fired correctly but the
notification was destroyed/recreated hourly (flash + voice replay). Live console
instrumentation attributed it to the surface city's own tick: the maintenance
loop and the food branch share the `"Food"` object key, and the maintenance
else-path deleted the food branch's entry each hour (voice plays only on
whole-notification creation — VoicePerObject false). Repair: maintenance loop
skips `"Food"` (the food branch owns the key). Full forensic record on the F12
entry. **A/B pair re-verified clean same day (2026-07-27):** baseline
Mars.exe-20260727-11.45.34 = 1 PASS / 58 FAIL / 11 SKIP / 0 ERROR; fixed
-11.47.09 = **59 PASS / 0 FAIL / 11 SKIP / 0 ERROR**, 66/67 active,
LowStorageWarning applied, zero errors from our files. Repair landed. **Open:
the user re-runs PT-07 on the repaired build (warning fires AND sits steady +
the Machine Parts half).** → **DONE 2026-07-27: PT-07 PASS in full, F12 `tested`**
(fires once / steady a sol / silent organic clear, both branches; see the
checklist archive).
**PT-38 DONE (2026-07-27) — D02's premise measured and CORRECTED; build
unblocked.** The dismissal window is **120,000 GAME-ms = 4 game hours**, NOT 2
real minutes: `GetTime()` = `GameTime()` because `GameTime` defaults true and
the NotWorkingBuildings preset doesn't override it (`NotificationPreset.lua:65-66,
:126-128`). Live timestamp wrappers measured three dismissal→return pairs at
148,805 / 161,755 / 132,056 game-ms — each 120,000 + time-to-next-attempt, every
in-window attempt observed BLOCKED. At ultra the re-nag is every few REAL
seconds — D02's case is stronger than premised. Suppression is per notification
id (fuel warnings independent — user-observed). **D02 (`Opt_AcknowledgedWarnings`
+ probe) is now buildable in the next build leg with the corrected spec.** Two
engine facts from the sitting: infopanel cheat buttons need `Platform.cheats =
true` (ObjCheat gate, `Network.lua:218-219`) AND their presses ride the
game-time sync queue — dead-looking while paused, firing on unpause.
**TestKit console repair (2026-07-26 later, user report: console dead on every
NEW save, fine on loads):** root cause — `Msg("CityStart")` fires from
`OnMsg.NewMap` DURING map generation (`Lua/_init.lua:18-26`), so the kit's fixed
2 s sleep auto-opened the console into a desktop the loading flow then replaced.
Repair in TestKit 00_TestCore.lua: also hook **`InGameInterfaceCreated`** (end
of `InGameInterface:Open`, `Lua/UI/InGameInterface.lua:388` — fires on BOTH new
games and loads, guarantees the UI exists), the open thread now waits on
`WaitLoadingScreenClose()` (`CommonLua/UI/LoadingScreen.lua:374`) instead of
guessing, and auto-open arms once per session entry so mid-session interface
reopens re-assert enable+shortcut without popping the console again. **Engine
fact: CityStart is a map-generation-time message, NOT a UI-ready message — use
InGameInterfaceCreated for anything that needs the in-game UI.**

**F18 open half CLOSED (2026-07-26, user-driven):** the user asked whether
resetting the tech was the easy fix; the investigation it prompted found better —
the stored modifier is keyed by the effect object and the shipped applier passes
the tech preset as parent (`GameEffect.lua:36-40`), so a LoadGame sweep re-runs
`effect:OnApplyEffect(UIColony, tech)` argument-identically to research and
replaces the stale -10 with -20 in place. No reset, no re-research, no first-load
flag (state-detected, idempotent). Probe extended to drive the sweep both ways.
F18 status is now plain `fixed`.

**User decision 2026-07-26 (D01 export half): match the ORIGINAL game, not a new
design.** Spec = the legacy loader (RocketBase.lua:1729-1736: standing
PreciousMetals demand to max_export_storage, any-drone flags, per-rocket
allow_export toggle). Build queued for a build leg with three research items
(toggle mapping onto UniversalRocket, modern sell-on-arrival path, whether the
original auto-offloaded RC transports — decides if F56's behavior rides along);
own probe + playtest item; same ClassicRockets flag. Details on the D01 entry.

## QA session (waves 4+5) — Fable, 2026-07-25 evening: merge + audits + A/B CLEAN

**Task 0 — merge:** `wave4` merged to main in BOTH repos with zero conflicts (fix pack
2f09133, TestKit 17f7b3c), worktrees removed, branches deleted, fix pack pushed. The
commented-out F10 metadata line survived. 21 new modules → 68 metadata entries,
67 registered modules.

**Task 1 — parse sweep + A/B pair:** all 80 Lua files in both mods parse. Logs in
`%AppData%\Surviving Mars Relaunched\logs`:

| Leg | Log (Mars.exe-20260725-…) | Result |
|-----|---------------------------|--------|
| Baseline (pack code list emptied) | 22.46.34 | 1 PASS, **57 FAIL**, 12 SKIP, 0 ERROR — every armed probe FAILs |
| Full pack | 22.48.50 | **58 PASS, 0 FAIL**, 12 SKIP — exposed the F75/F18 status-relabel defects (fixed, cdff2ce) |
| Verification (status repairs in) | 22.52.57 | **66/67 active** (ClassicRockets opt-in inactive), **58 PASS, 0 FAIL, 12 SKIP, 0 ERROR** |

The 12 SKIPs: 10 `[install]` probes (retail sandbox — MarsDebug pass covers them),
ClassicRockets (opt-in, verified separately in the wave-3 opt-in leg), and
TechDescriptionBuilding (below). Non-Flight `[LUA ERROR]`s present in BOTH legs are
synthetic-map GameInit noise in shipped files (BuildingWayPoints/TaskRequest/GridObject);
nothing names an SMR file. A `[mod] Error in mod … Test Kit` line at quit time is a
shutdown artifact (fires at the harness's own `quit()`, exit code 0, results complete).

**The two wedged legs (21.01.55 and 22.29.10) were a TestKit probe defect, not the
game:** the TrainWaitTime probe faked the sleeping `PlayPrg` as a no-op, so the shipped
`while self.holder == vehicle do self:PlayPrg() end` ride loop span without yielding and
starved EVERY Lua thread — including the harness watchdog (why it never fired) and the
log writer (why the logs looked empty; the buffer only flushes at exit). Repairs
(TestKit bafbd61 + 80de593): the fake now ends the ride; the harness flushes the log
per line so a killed run keeps its evidence; `ShowStartGamePopup` is neutered when the
autorun is armed (the "Welcome to Mars, Commander!" popup was on screen but was NOT the
wedge); watchdog raised to 15 min. **Engine-fact lesson: a probe must never fake a
blocking primitive as a no-op inside a driven loop.**

**Task 2 — probe discrimination:** 19/20 wave-4/5 probes FAILed baseline → PASSed
fixed: RocketInteractGuard, TrackConnectorPingPong, TrackTunnelPowerBridge,
GridGlobalStorage, LastTransmissionStorage, TrainWaitTime, GraphConsumedCaption,
MoraleComfortTooltip, ReplaceTechCount, StorageRateModifiers, SequenceLatents,
FounderTraitNotification, IndependenceTerraforming, TrackSalvageRefund, LayoutTechLock,
TrainMinors, DroneTransportMinors, AnomalyCaveInMap, BombardmentSpread. **Not
discriminating: TechDescriptionBuilding** — SKIPs both legs ("the tech has no
description T": the probe finds `TechDef.UndergroundLargeDome.description` is not a
table at probe time). F25 is therefore NOT probe-verified; its playtest item is the
evidence path (or a console read of the description). F24 has no probe by design
(PT-44). FactionFundingCheck PASSes both legs as always (F10 retired, PT-36 gate).

**Task 3 — audit fan-out (14 read-only subagents, every verdict verified before
action):** CLEAN: F20, F21, F22, F24, F74 (premises held; only LOWs). Findings that
led to repairs, all landed and covered by the final A/B:
- **F57a HIGH (live game-breaker):** `rfRestrictorRocket` is a FILE-LOCAL
  (DroneControl.lua:12); the replacement read it as a global and raised on every
  rocket-restrictor update → drones would stop servicing rockets. Repaired 493f054.
- **F28 MEDIUM:** the dropped `assert(tech_def.group == status.field)` was load-bearing
  through its ARGUMENT (raises on unknown tech_id_new BEFORE mutation); the copy mutated
  first. Guard restored b66995f.
- **F26 HIGH (dead fix):** preflight checked BombardMissile for methods declared on
  BaseMeteor (invisible pre-flattening — the F64 lesson AGAIN) and required the
  SessionRandom GameVar at apply time; the fix could never activate. Repaired 11ecd22.
- **F75 HIGH + F18 sibling:** preset-patch fixes relabeled themselves
  "inactive: already correct" when the engine's post-DataLoaded `DataChanged(false)`
  reran them over their own corrections; F75 also bypassed the SMRFixPack_Disabled veto
  in its OnMsg path and misread the EMPTY pre-DataLoaded GlobalMap as a vanished
  target. Repaired 11ecd22 + cdff2ce. **Engine fact: `Msg("DataChanged", false)` fires
  right after every DataLoaded (Dlc.lua:715-717, :680-685); FactionDefs/TechDef
  GlobalMap tables exist EMPTY before DataLoaded.**
- **F43 HIGH (latent):** `IsValid()` on pure-Lua InitDone controllers is always falsy
  (C-side check; cf. RealTimeCommandObject's own override) — the teardown was dead code
  and would have leaked the cursor object when a tech-gated layout entry ever goes
  live. Guard dropped 11ecd22. **Engine fact: IsValid() rejects pure-Lua objects, not
  just probe stand-ins.**
- **F31 MEDIUMs:** the divergence paragraph's marsquake claim was FALSE (every engine
  TriggerCaveIn call is already Underground-gated, Marsquake.lua:285/:294/:323-325) —
  corrected in place; and the 8th call site crashes inside `FindCaveInLocation`
  (CaveInRubble.lua:27) before the wrapper — a second decline-wrapper now covers it
  (11ecd22, 8/8 sites).
- **F49:** (d)'s rationale was backwards (GameInit is DEFERRED, _object.lua:187-192 —
  the surviving track is the real defect, which the fix covers) and coverage gaps via
  AutoConnectTracks/instant-build reuse are recorded as accepted (sweep corrects on
  load); (c) implemented per the user's decision (below); (b)(e) screenings verified
  sound. F20/F74 wrappers got vararg pass-throughs (§1.4).
- **F65 HIGH:** the 2-element special deletion path (TrackConnectedObjBase:Done,
  TrainTransport.lua:24-27) DoneObjects the track with NO DisconnectFromGrids — and
  only F65 ever creates a bridged 2-element track, so demolishing an endpoint leaked
  tunnel mask/adjacency into the save. Repaired 8e0b177: TrackBase:Done is pre-wrapped
  to run the shipped DisconnectFromGrids (tolerates a dead endpoint by design;
  RemoveSupplyTunnel clears the flag so demolish-path double-calls no-op). The
  MEDIUM (different-grids test is one-shot; cable-topology declines re-check only on
  next load's sweep) is documented as accepted in the fix header.
- **F47 MEDIUMs (recorded, NOT yet repaired — both under-refunds, no over-refund/save
  hazard):** F44's trim-to-empty exit skips the refund (composition gap), and the
  construction-site early-return is broader than repair sites. On the list for a
  future leg.
- **F66 MEDIUM (recorded, awaiting user decision):** after the blocking neighbour is
  demolished, the guarded building never reclaims the connector hex (no rebuild
  trigger reaches it) until any track demolish fires the global rebuild or it is
  re-placed. Options given to the user: accept+document vs a demolition-path rebuild
  trigger.
- Recurring minors: full-replacement headers date the copy instead of naming the game
  version (FIX_POLICY §1.5) — release-checklist item; assorted citation drift fixed.

**User decisions recorded this session:** F42 CLOSED `wontfix`; F49(c) = "the click
does nothing", implemented.

**Playtest findings processed live (first sitting, wave-3 pack):** PT-02 PASS, PT-04
PASS (status flips belong to the playtest-report session). **PT-03 F44 curve FAIL →
diagnosed and REWORKED (a38cbf2):** the split branch could delete a physically
scattered zone whenever sorted order diverged from physical order (exactly the
non-numeric node_idx state the old comparator sorted as -1 and carried on with),
stranding orphaned elements (track_obj == false) that raise on every later click —
the user's "broke itself, became immune" with screenshots. Now: orphan clicks delete
the debris, the salvage declines BEFORE deleting anything when order can't be trusted,
the split tail is IsValid-guarded, and a LoadGame sweep removes orphans already baked
into saves (the user's playtest save will log `TrackSalvageWipe: removed N orphaned
track element(s)`). **PT-03 needs a re-run.** PT-01 (meteors stopped after sol ~12.5,
FAIL) is NOT yet diagnosed — first question is whether the user reloaded during the
quiet stretch (every load re-rolls the 65-90h Low-threat interval; frequent reloads
legitimately push strikes out). If they didn't reload, F02 has a real regression to
find.

**Commits this session (fix pack):** 2f09133 merge, b66995f F28, 493f054 F57a,
09af088 playtest notes, 11ecd22 audit repairs, 8e0b177 F49c+F65, 75c54f6 doc
corrections + F42 (NOTE: accidentally committed the baseline's emptied metadata via
`commit -a`; restored in 1321795 — never use `-a` while an A/B leg's metadata edit is
in the working tree), a38cbf2 F44 rework, cdff2ce F75/F18 status. TestKit: 80de593
harness hardening, bafbd61 probe wedge fix + 15-min watchdog.

**Open after this session (both user answers now in, 2026-07-25 late):**
- **PT-01: NO reloads** → F02 is genuinely regressed (meteors stopped for 560+ game
  hours on a max-threat map after Sensor Towers went up) — REOPENED `fixed*`,
  investigation speced in docs/prompts/FABLE_NEXT_PROMPT.md Task 1.
- **F66: user chose the rebuild-trigger repair** over accept-and-document — spec on
  the F66 entry + docs/prompts/FABLE_NEXT_PROMPT.md Task 2.
- PT-03 re-run (user, next sitting); F47 composition under-refunds; MarsDebug
  [install] pass for wave-4/5 (attended, SetupOnly); game-version tags on
  full-replacement headers (release checklist).

## Discovery: COMPLETE

- 73 tracked findings (~85 distinct defects) verified against the CURRENT
  (post-1.0.7) shipped source, each with file:line evidence + fix sketch in BUGS.md.
- 1 design-change verdict (D01 rocket auto-refuel/rare-metals — plan opt-in module).
- 2 candidates needing runtime checks (C01 BreakthroughOrder, C02 asteroid cave-ins).
- 3 critical UNTRACED leads (RESEARCH.md): 90%-breathable-atmosphere freeze,
  Last War mystery import lock at 54%, game-stops-saving. Plus smaller new leads
  from the ChatGPT dossier cross-check (top of RESEARCH.md).

## Implementation: 47 tracked defects DONE across 46 registered modules (ALL probe-verified in-game 2026-07-25 — wave-3 A/B pair clean, see the QA session section; F10 retirement STAGED 2026-07-26, premise falsified, final wontfix gated on PT-36)

Wave 1 (earlier session): F01 cave-ins/NoDisasters, F02 meteor frequency,
F03* upgrade-modifier leak, F04 night shift, F05 milestone crash, F07+F15* wisp
power/rewards, F08 tourist applicants, F10 faction funding, F64 trains-to-void.

Wave 2 (earlier session, in queue order): F67 lander empty launch, F68 lander cargo
ratchet, F69 lander return fuel, F73 shelter reflex, F45 broken-track salvage,
F44 track salvage wipe, F30 lake entombment, F37 ghost farm oxygen, F50 rocket
drone churn, F51 shuttle transport cache, F52* vacuum walks, F53 arrival deaths,
F55* drone unreachable-forever, F58* stale reservations, F61 home-dome migration
gate, F06 crystal mystery hang, F09 tourist satisfaction, F11 train platform
wedge, F12 low-storage warning, F13 Command Center numbers, F14 Domes Overview
highlight.
(* = partial; the remaining half is recorded on the BUGS.md entry.)

Wave 3, first leg (session 3, in queue order): F46 train cargo dumping, F36 university
overtraining, F38 destroyed tunnels, F39 second artificial sun, F40 Dust Sickness on
Biorobots, F17 Dust Sickness randomization, F41 Gene Forging, F16 Mirror Sphere site,
F70 Edit Payload template refill.

Wave 3, second leg (session 4, in queue order): **F71** auto-export capacity priority
(folded into `Fix_LanderCargoRatchet.lua` — F68 already replaced that function),
**F72** asteroid-lander availability gate, **F54** switched-off shuttle hubs,
**F59*** freed housing notifies the homeless, **F60** dome free-space member mismatch,
**F33** small landscaping site drone crash, **F34*** landscape units-underneath filter,
**F35 + F03 sweep** in the new `Code/90_SaveSanitizer.lua`, and **D01** as the opt-in
`Code/Opt_ClassicRockets.lua` (fuel half only).
(* = partial; the remaining half is recorded on the BUGS.md entry.)

**The whole wave-3 queue is now done.** Nothing from the session-3 handoff list is left
except the four entries deliberately parked as `blocked` (see below).

**Wave-3 fixes are now probe-verified in-game (2026-07-25 QA session):** the RunAll A/B
pair ran clean — every armed probe flipped FAIL→PASS, 46 fixes + sanitizer `applied`,
ClassicRockets `inactive` by default and `applied`+PASS in the opt-in leg. Full results
in the "QA session (wave 3)" section below.

Three first-leg fixes add their own `OnMsg.LoadGame` repair pass: F38 (close destroyed
tunnels left open in pathfinding), F39 (reconnect solar panels to a sun in range), F40
(clear Dust Sickness from already-infected Biorobots).

`Code/90_SaveSanitizer.lua` now exists and carries the remaining consolidated sweeps:
**F35** (restore the Frictionless Composites label modifiers the shipped migration fixup
dropped) and **F03** (remove upgrade modifiers orphaned by salvaged buildings). Both are
idempotent, both run on **`OnMsg.PostLoadGame`** (NOT LoadGame — the QA audit found that
`Msg("LoadGame")` fires BEFORE `FixupSavegame`, `Savegame.lua:810-813`, so a LoadGame-time
F35 pass raced the shipped turbine fixup and could bake +200% onto Shrouded turbines on a
never-patched save's first load; see the F35 entry), and both are exposed on
`SMRFixPack.Sanitizer` so QA can re-run them from the console (`RepairTurbineBuff` /
`RepairLeakedUpgradeModifiers`, each returns a repair count). **F48 is NOT in it** — see
its BUGS.md entry.

Other fixes carrying their own one-shot `OnMsg.LoadGame` / `OnMsg.NewDay` pass for state
already baked into savegames: F02 (thread restart), F45 (stamp repair sites), F37 (remove
phantom farm oxygen), F58 (release stale reservations), F06 (restart the crystal repeater),
plus F55's expiry which self-heals.

**Savegame footprint** (FIX_POLICY §3 — all absent-tolerant): `colonist.SMRFixPack_reserved_at`
(F58), `transporter.SMRFixPack_payload_set` (F70), an entry keyed `smr_shuttles` on a
transport-cache entry (F51, a hash key that does not affect `table.unpack`), and — only
where the sanitizer repaired one — a label modifier under `SMRFixPack_F35_<label>` (F35).
README's old "stores nothing in your savegames" claim has been corrected accordingly.

## Wave 4 — build leg DONE (branch `wave4`, NOT merged, NOT probe-run)

**14 new fix modules, 13 new probes, 6 new playtest items (PT-39..PT-44).** Everything
lives on the `wave4` branch in `C:\Dev\SMR-BugFixPack-wave4` and
`C:\Dev\SMR-BugFixPack-TestKit-wave4`; main is untouched, the game was never launched, and
**no probe has been run** — the A/B pair belongs to the wave-4 QA leg
(`docs/FABLE_QA_PROMPT.md`), which also performs the merge.

Implemented, in queue order:

| ID | Module | Note |
|----|--------|------|
| **F74** *(new)* | `Fix_RocketInteractGuard` | found by screening F56; the shipped guard at `RCTransport.lua:341` names only the pre-Relaunched trade/refugee classes |
| **F66** | `Fix_TrackConnectorPingPong` | enforces the invariant the shipped assert only states |
| **F65** | `Fix_TrackTunnelPowerBridge` | bridges only when the two stations demonstrably sit on different grids; PostLoadGame sweep |
| **F22** | `Fix_GridGlobalStorage` | one ratio over summed inputs instead of a sum of ratios plus a sentinel |
| **F75** *(new)* | `Fix_LastTransmissionStorage` | found by implementing F22; six conditions were on `Prerequisite`, which `Eval` never reads, and the Oxygen one measured Power |
| **F19** | `Fix_GraphConsumedCaption` | caption counts maintenance, like the bar |
| **F20** | `Fix_MoraleComfortTooltip` | hides the one row `UpdateMorale` no longer grants |
| **F21** | `Fix_TrainWaitTime` | full replacement — `BoardVehicle` blocks for the whole ride |
| **F23** | `Fix_FounderTraitNotification` | additive handler beside the dead one |
| **F24** | `Fix_DomePipeMoveInside` | `dome` → `self`; no probe, PT-44 covers it |
| **F27** | `Fix_StorageRateModifiers` | three post-wrappers |
| **F28** | `Fix_ReplaceTechCount` | entry title corrected: no crash is claimed, only that the line is wrong either way |
| **F29** | `Fix_SequenceLatents` | `fixed*` — items 1 and 3; item 2 is a Mod Editor code generator, deliberately left |
| **F18** | `Fix_IndependenceTerraforming` | `fixed*` — preset half; already-researched saves keep 10% |

**Screened and CLOSED `wontfix` (user decision 2026-07-26): F56.** Screening before
implementing found designed scope, not a defect — `GetAutoGatherDeposits` is a declared
accessor, the `Automation_Unload` rocket exclusion goes through the Relaunched
`IsRocketClass` shim (i.e. a developer consciously re-stated it for the new class tree),
and auto mode promises only "gather resources". Closed on the same grounds as F62/F63:
deliberately maintained design, breaks nothing. **No standalone opt-in is planned** — if it
is ever revisited it belongs in `Opt_ClassicRockets` beside D01's unwritten Rare Metals
export half, not in a module of its own (same request, same machinery, and shipping them
apart would let a player enable emptying without refilling). Full write-up on both entries.

**Still `todo` after wave 4 — eight entries, the P2/P3 tail:** F25, F26, F31, F42, F43,
F47, F49, F57. ~~Suggested order for a wave-5 build leg~~ **All eight were taken in wave 5
— seven implemented, F42 screened to `blocked`. Nothing is `todo` any more.** The `fixed*`
partials whose open half is recorded on the entry are now: F15, F18, F29, F34, F49, F52,
F55, F57, F58, F59.

**Every wave-4 fix is unverified in-game.** The four full replacements (F66
`CreateConnectorElements`, F21 `BoardVehicle`, F24 `MoveInside`, F28 `ReplaceTech`) and the
one global-function replacement (F22 `GetGridGlobalStorage`) are the highest-risk items for
the QA audit; F20's per-call instance `GetProperty` override and F65's PostLoadGame sweep
are the two most unusual techniques in the pack and deserve a look.

## Wave 5 — build leg DONE (branch `wave4`, NOT merged, NOT probe-run)

**7 new fix modules, 7 new probes, 3 new playtest items (PT-45..PT-47).** Everything lives
on the `wave4` branch beside wave 4's; main is untouched, the game was never launched, and
**no probe has been run** — the A/B pair belongs to the QA leg, which covers waves 4 and 5
together. **The BUGS.md `todo` queue is now empty.**

| ID | Module | Note |
|----|--------|------|
| **F47** | `Fix_TrackSalvageRefund` | sums every construction group's stamp instead of reading one; + partial-salvage refund |
| **F43** | `Fix_LayoutTechLock` | latent — no shipped layout has a tech-gated entry |
| **F49** | `Fix_TrainMinors` | `fixed*` — items (a) palette and (d) train cap; (b)(c)(e) screened, see the entry |
| **F57** | `Fix_DroneTransportMinors` | `fixed*` — (a) latent restrictor leak and (b) the unreachables table; (c) would undo F61 |
| **F31** | `Fix_AnomalyCaveInMap` | guards the argument, not the environment — the sketch's test would have killed marsquake cave-ins |
| **F25** | `Fix_TechDescriptionBuilding` | preset patch reusing the original translation id, so localised builds are untouched |
| **F26** | `Fix_BombardmentSpread` | the pack's **sixth and largest full replacement** (100 lines) |

**Screened items — both user decisions made 2026-07-25 (wave-4/5 QA session):**
- **F42** (buildings placeable on active dust devils) → **CLOSED `wontfix`** on the
  F56/F62/F63 grounds: the guard it names exists to stop units being *entombed*, a dust
  devil has no footprint and cannot be trapped, the omission is in declared overridable
  class members, and no shipped text promises the block.
- **F49(c)** (a salvage click on a station's connector hex reaches the station) →
  **user chose "the click does nothing"; IMPLEMENTED** in `Fix_TrainMinors.lua` as a
  demolish-mode pre-guard on `TrackGridElement:SelectionPropagate`.

**Every wave-5 fix is unverified in-game.** Highest-risk items for the QA audit, in order:
**F26** (100-line copy of `WaitBombard` — mechanically diffed against the shipped body,
identical apart from the function header, the dropped non-unwinding `assert`, and the one
`-- FIX:` line, but it replaces a whole disaster path); **F47's** partial-salvage wrapper on
`TrackGridElement:Demolish` (places resource stockpiles from a before/after snapshot);
**F49's** replacement of the global `ExpandTrackFromElement`; and **F43's** teardown of
live construction controllers inside a post-wrapper on `Activate`.

**New engine facts learned this leg (do not re-derive):**
- **Track is billed per construction GROUP, not per hex.** Groups hold at most
  `const.ConstructiongGridElementsGroupSize` = 5 elements (`_GameConst.lua:480`), and
  `Tracks.lua:463` leaves the leader's `construction_cost_multiplier` at 100 — one
  element's cost per group. Passages do it the other way (`Passage.lua:1969`).
- **`ConstructionGroupLeader:Complete` stamps the group's whole spend onto exactly ONE
  finished element** — the last it completed — after suppressing every member's own
  `MarkSpentResources` (`ConstructionSite.lua:2469`, `:2479-2489`). So
  `construction_cost_at_completion` is one stamp per group, spread along a track. This is
  what F47 turns on.
- **A T can be corrected without breaking translations** by rebuilding it with the SAME
  translation id: localised builds resolve the id and never see the literal, English builds
  fall back to it. Minting a fresh T would push English text into every language (F25).
- **`UndergroundMap` is a GameVar defaulting to `false`** (`RandomMapGenerator_Picard.lua:263`)
  and stays false under the "No Underground and Asteroids" rule — eight scenario call sites
  hand it straight to `TriggerCaveIn`, which indexes it unguarded (F31).
- **Verify every full replacement mechanically.** F26's 100-line copy was diffed against
  `ModTools\Src` with a throwaway Python script that strips comments and whitespace; it
  caught nothing this time, but it is the only way to be sure a copy that large is faithful.

## QA session (wave 3) — Fable, 2026-07-25 evening: A/B pair CLEAN, audits done

All four RunAll legs unattended via `-smrautorun` (Steam `-applaunch 3215050`); a
Python `luaparser` pre-pass first proved all 57 mod Lua files parse (no file-level
load failures possible). Logs in `%AppData%\Surviving Mars Relaunched\logs`:

| Leg | Log (Mars.exe-20260725-…) | Result |
|-----|--------------------------|--------|
| Baseline (pack code list emptied) | 16.19.54 | 1 PASS, **38 FAIL**, 11 SKIP, 0 ERROR — every armed probe FAILs, all discriminate |
| Full pack | 16.22.38 | **39 PASS, 0 FAIL**, 11 SKIP — 46/47 active + ClassicRockets `inactive` (expected); found the ModLog `%` defect (below) |
| Opt-in (`SMRFixPack_Optional.ClassicRockets`) | 16.28.35 | **40 PASS, 0 FAIL**, 10 SKIP — ClassicRockets `applied`, its probe asserts; F69 chain intact |
| Final verification (default config, repairs in) | 16.31.30 | **39 PASS, 0 FAIL**, 11 SKIP, zero errors from our code |

(The ~49 `[LUA ERROR] Flight.lua objects_to_mark` blocks per leg are engine noise on
the synthetic map — present in the baseline too, not ours.)

**Defects found and repaired this session (all verified by the later legs):**
1. **HIGH — SaveSanitizer fixup race** (subagent audit, verified first-hand): pass moved
   `OnMsg.LoadGame` → `OnMsg.PostLoadGame`; see the F35 BUGS entry. Not probe-coverable
   (needs a real never-patched save — PT-35 case C).
2. **ModLog re-formats its message**: `ModPrint` is a printf-style `CreatePrint`
   (Mod.lua:109-113 + lib.lua:164-174), so a literal `%` in an already-formatted message
   raises `[LUA ERROR] string.format` — three per fixed leg (sanitizer "+100%" lines,
   TurbineBuff PASS line). All four log helpers now escape `%` for the second pass
   (fix pack 00_Core + 90_SaveSanitizer; TestKit 00_TestCore + 95_AutoRun, whose
   "ModLog is %-safe" comment was WRONG — corrected). **Engine-facts correction.**
3. **F35 amount now scaled** via `GetModifiablePropScale` (dormant hardening, matches
   Tech.lua:298-301).

**Spot-audits of the six highest-risk wave-3 divergences (subagent fan-out, each
verified against Src):** F59 CLEAN (ordering + assert-race claims true; recursion
bounded — homeless have `residence == false`), F71/F68 CLEAN (body diff exact; pcall
degrades to shipped alphabetical order; reorder provably cannot drop or starve a
resource), F72 CLEAN (strict pass-through; scan is an exact subset of
GetRocketsForExpedition incl. supply-pod exclusion), F54 CLEAN (full reason-state
enumeration found a FIFTH string `ExceptionalCircumstancesMalafunction` (sic) —
provably never admitted, malfunction forces GetWorkNotPossibleReason truthy), F34(d)
CLEAN (params table matches shipped; engine never mutates it; per-call dedup),
SaveSanitizer = the HIGH defect above, now repaired. Recurring minor: header/BUGS
line-number drift (off-by-ones, catalogued in the session transcript — cosmetic).

**Probe-discrimination sweep (Task 2):** ground truth from the pair — every armed
probe FAILed baseline and PASSed fixed except **F10 `FactionFundingCheck`**, which is
**fundamentally non-discriminating**: the baseline drove the shipped body over 240 nil
hours and it returned 0 — **this engine tolerates `pairs(nil)`** (new engine fact,
consistent with the `next(nil)` tolerance). F10's defect premise is falsified; entry
updated, probe PASS message now says "not evidence". Decision for the user below.
The rewritten F51 probe now discriminates (FAIL→PASS observed). 10 `[install]` probes
still SKIP on retail — the MarsDebug.exe pair remains the missing coverage.

**MarsDebug [install] pass (2026-07-26, attended) — FULL COVERAGE, 49 PASS / 0 FAIL /
0 ERROR** (1 SKIP = ClassicRockets opt-in, verified separately in the opt-in leg). Logs:
MarsDebug.exe-20260725-17.40.38 (baseline, installs SKIP — see below) and -17.46.04
(fixed, attended). All 10 `[install]` probes PASS with real verdicts, and **F73's Idle
pre-wrapper half is verified** ("Idle carries the shelter branch") — the last unverified
wiring in the pack. Install-probe baselines are FAIL-by-construction (they test function
provenance), so the attended fixed leg alone completes the coverage.
Three facts corrected/learned doing it:
- **The mod sandbox applies on ALL builds including MarsDebug.exe** — the wave-2
  assumption that an asserts build un-sandboxes mod code is WRONG. An asserts build
  unsandboxes the CONSOLE (g_ConsoleFENV reads real `_G`, console.lua:36-44), and
  `ConsoleExec` is on the ModEnvBlacklist (Mod.lua:1285), so the introspection bridge
  cannot be automated — it is typed: `SMRTest.EnableIntrospection(debug)` then
  `SMRTest.RunAll()`.
- The TestKit autorun now has a flag-gated **SetupOnly mode** (95_AutoRun +
  96_AutoRunFlag comment) that builds the colony and hands the session to the human —
  the attended-leg harness.
- **The debug build pops MODAL dialogs for asserts** — the first is the known vanilla
  `Flight.lua:465 objects_to_mark` noise; click **Ignore All** or the run blocks (and
  the 8-min watchdog can then expire; harmless, relaunch).

**D01/ClassicRockets (Task 4):** default-off / opt-on / no-spam claims all verified;
the no-spam citation in the Opt file pointed at the wrong file (the `arrival_loc`
gates live in the UniversalRocketBase override, UniversalRocket.lua:1687-1692) —
corrected; a third benign `Msg("RocketRefueled")` path via DroneUnloadResource is
now documented in the file. MOD_DESCRIPTION wording tightened so the module text
cannot be read as promising the unwritten Rare Metals half.

## QA session snapshot (Fable, 2026-07-25) — kept for the audit record

**NOTE — everything actionable below is RESOLVED:** the F53 and F12 reworks
LANDED (commits aa980e7 / 40d5a73) and survived the final A/B pair; the autorun
harness IS committed (TestKit); the RunAll pair HAS run clean — see the FINAL
A/B section above. Still open from this section: F68 capacity-cap in-game check,
F44 curve-ended track visual check, wave-1 heading tags.

- BUGS.md index was stale (16 wave-2 rows said `todo` despite tagged headings) —
  synced in commit 0ef4e7c. README/MOD_DESCRIPTION verified complete. Follow-up:
  wave-1 detail headings (F04/05/07/08/10/15/64) lack the `[fixed]` tag.
- Nothing was marked `blocked` in the build session. F55's "open-air entrance half
  not actionable" verdict was re-verified and is CORRECT (CalcOpenAirSkin only
  empties skin[2] configurable attaches; Dome_Entrance is entity-spot auto-attach
  data, Dome.lua:404 — not patchable from Lua). F55 drone half diffs clean.
- Spot-audit of 6 fixes (F61, F12, F44, F53, F68, F73) — full reports in the
  session transcript; summary:
  * **F53 CRITICAL — rework before release.** The `not IsInWalkingDist` gate in
    Fix_ArrivalDeaths.lua is always true for cross-map elevator destinations
    (IsInWalkingDistDome returns false when maps differ, Dome.lua:248-251), so
    every legitimate elevator arrival triggers the re-choose; the re-choose
    discards ChooseDome's elevator return and never clears stale
    self.emigration_elevator → TransportByFoot rides the stale elevator, fails
    the map-slot check (Colonist.lua:2731) → SetCommand("Abandoned"). Repair:
    skip the gate when ValidateBuilding(self.emigration_elevator) routes to
    dome; on re-choice take BOTH returns and assign emigration_elevator.
  * **F12 MODERATE — rework.** Post-wrapper leaves shipped dead branch removing
    the notification hourly, wrapper re-adds → destroy/recreate churn + FX replay
    every game hour while active; dismiss/suppression semantics differ. Docs
    prescribe full replacement — do that instead.
  * **F68 MODERATE — verify in-game.** The requested-floor (belt-and-braces
    block) doesn't debit hold capacity: with multiple exports, an alphabetically
    earlier resource's request can exceed remaining capacity → status stuck
    "loading", automode rocket sits on pad (departure gate needs "ready").
    Consider capping the floor against remaining capacity.
  * **F61 CLEAN**, **F44 CLEAN** (in-game check: curve-ended remainder track
    visuals; F45-comparator fold-in disclosed), **F73 CLEAN** (note:
    IsSuitable is AutoResolveMethods "and"-combined with Residence.IsSuitable —
    correct today, document it; partial-application isn't reported in the log).
  * Recurring minor: header/BUGS line-number drift (off-by-ones); apply()
    self-checks don't pre-check every runtime symbol.
- AccountStorage research (for the RunAll pair): enabled mods live in
  AccountStorage.LoadMods (plain array of metadata.lua `id` strings), persisted
  in `%AppData%\Surviving Mars Relaunched\<SteamID64>\account.dat` — an
  in-memory HPK (magic BPUL) containing `account.lua`, AES-encrypted+HMAC with
  key SHA256(GetAppId()..config.ProjectKey), compressed. BUT the loader is
  best-effort: a plaintext `return {...}` account.lua inside the container still
  loads (lib.lua:2187-2216). Edit only with the game closed; ids for missing/
  too-old mods are auto-stripped at menu (Mod.lua:2033-2059). Escape hatch:
  `AccountStorage.LoadAllMods = true` loads every discovered mod, bypassing the
  list. Unpacked mods in Mods\ need metadata.lua with `id` + `lua_revision` ≥
  350453. No Paradox cloud sync of account.dat (CloudSavesAllowed() = false).
- RunAll before/after pair NOT run: the Relaunched profile has never been created
  (%AppData%\Surviving Mars Relaunched\ has only Mods; no saves/logs/AccountStorage;
  no Steam userdata for appid 3215050) and mods can't be enabled until first launch.
  TestKit is now junctioned next to the fix pack. An opt-in autorun harness
  (TestKit Code\95_AutoRun.lua: flag-file gated, auto new game via
  NewGame/InitNewGameMissionParams/LoadLastNewGameSettings + fill g_CurrentMapParams
  + GenerateCurrentRandomMap, then RunAll with [SMRAUTO] markers, watchdog, quit())
  was being built when the session ended — it is NOT committed; check the TestKit
  repo before relying on it. Retail exe ignores -save/-map (goldmaster-gated,
  autorun.lua:126-144); Mars.exe launches directly, no external Paradox launcher.

## FINAL A/B RunAll pair (repaired TestKit) — CLEAN SWEEP (2026-07-25)

Re-run after the TestKit repairs (WithGlobals now writes real globals; sentinel
SKIPs; probe fixes). Logs: Mars.exe-20260725-14.17.33 (baseline) / -14.20.37
(fixed). **19/19 discriminating probes flipped FAIL→PASS; zero FAILs remain;
all 30 fixes `applied`.** Probe-verified fixes: F03, F04, F07, F08, F09, F11,
F13, F14, F15, F50, F51*, F52, F55, F58, F61, F67, F68, F69, F73, F06.
Not discriminated on a virgin colony: F10 (funding table non-nil → PASS both),
F51 probe PASSed both runs (cache re-evaluated even unfixed in this synthetic
scenario — probe may need a stricter setup). 10 [install] probes SKIP on retail
(sandbox); run the pair once under MarsDebug.exe for that coverage. F73's Idle
wrapper half also needs the debug-exe run (PASS was the IsSuitable half).
`tested` status remains reserved for scenario/manual verification per
TESTING.md — probe-verified ≠ full in-game scenario pass, but the wiring and
regression harness are now proven.

## Superseded: first pair (buggy TestKit) — kept for the record

Unattended harness works end-to-end (TestKit 95_AutoRun, `-smrautorun` via Steam
relaunch; Steam DRM blocks direct Mars.exe launch — bootstrap exits in 28ms).
Baseline = fix pack metadata `code` emptied; B = full pack. **All 30 fixes
report `applied`** (no inactive/error self-checks). Results:
- **FAIL→PASS (10):** UpgradeModifierLeak, TouristApplicants, LanderEmptyLaunch,
  LanderReturnFuel, RocketDroneChurn, StaleReservations, CrystalMysteryHang,
  TouristSatisfaction, TrainPlatformWedge, CommandCenterNumbers.
- **Applied but probe still FAILs (4) — diagnose fix-vs-probe:** WispPower (nil
  power units both runs), LanderCargoRatchet (request still drops to 0 with
  cargo aboard), HomeDomeMigrationGate (same fail text both runs),
  DomeOverviewHighlight (baseline "renders as 0", B "renders as table:0x…" —
  behavior changed, probe may mis-parse a T() value).
- **Probe/tooling casualties:** 10 [install] probes ERROR both runs — the
  no-introspection sentinel itself crashes (00_TestCore.lua:76 indexes nil
  'lib'); ShelterReflex ERROR in B (same crash via its wrapper check);
  VacuumWalks SKIP in B ("unexpected route value: unset").
- **Non-discriminating on a virgin colony:** FactionFundingCheck PASS both
  (funding table not nil on fresh game); NightShiftWork/WispResearch/
  ShuttleTransportCache/DroneUnreachableForever SKIP both (need colonists/
  mystery/shuttle state).
- Full logs: %AppData%\Surviving Mars Relaunched\logs\Mars.exe-20260725-13.56.49
  (baseline) and -13.58.35 (fixed).
- For [install] coverage: run the pair under MarsDebug.exe (console/asserts
  build un-sandboxes introspection; auto-bridge then fires).

### Diagnosis of the four "applied but still FAIL" probes — ALL FOUR FIXES ARE SOUND

Every one of the four was a Test Kit defect; **no fix pack code changed**. Two
engine facts (both now recorded in the Test Kit sources) explain all of them plus
the tooling casualties:

1. **`error()` does not unwind mod code.** It REPORTS (the `[LUA ERROR]` block
   with stack + locals) and execution continues with the next statement — the
   same treatment `assert` gets ("asserts pop instead of being printed out",
   LuaExports.lua:567). So `SourceOf`'s sentinel printed a stack and then ran the
   line it was guarding (00_TestCore.lua:76 → ERROR, not SKIP), and
   `WithGlobals`' `if not ok then error(res, 0) end` swallowed every error raised
   inside a probe's driven code — the probe carried on with a nil result and
   reported FAIL. Never use `error()` for control flow in mod code.
2. **`rawset(_G, k, v)` from mod code writes nothing the game can see.** In the
   sandbox `_G` IS the mod's own env table (Mod.lua:1603) and `rawset` is the
   real rawset (only `rawget` is replaced, :1606), so the Test Kit's fake globals
   were shadows in the Test Kit's env — invisible to shipped code (real `_G`) and
   to the fix pack (its own env). Plain assignment `_G[k] = v` goes through
   `ModEnvMeta.__newindex` (:1557-1563), which rawsets the REAL `_G`; that is the
   write a probe needs. **Every `WithGlobals` probe in the pair was therefore
   driving the real globals**, which is why the numbers looked absurd.

Per item, with the evidence that settled it:
- **WispPower (F07) — probe.** The fake `MainCity.labels.LightTrap` was invisible,
  so `SetLightTrapMode` iterated the live (empty) label and never called
  `el_prod_modifier:Change` → `granted` stayed nil in BOTH runs. The `* 1000` fix
  (Fix_WispRewards.lua:49) matches the sibling call sites exactly.
- **LanderCargoRatchet (F68) — probe.** The fixed method ran; the fake
  `GetTotalCargoAvailable` was invisible, so the real one crashed on the
  synthetic city (`[LUA ERROR] Lua/ResourceOverview.lua:30: attempt to call a nil
  value (method 'GetMap')`, raised from WithGlobals) and the swallowed error left
  `captured` nil → "request dropped to 0". The requested-floor block is intact
  and would have engaged (`is_on_automode_target_loc` true, `export_above.Metals`
  set, 300k aboard). The separate audit finding stands and is NOT this:
  the floor still does not debit hold capacity — verify in-game with multiple
  exports.
- **HomeDomeMigrationGate (F61) — probe.** Proof the fix worked: the fake global
  `ChooseWorkplace` was invisible, so the *real* one ran on the synthetic
  colonist and crashed (`Lua/Buildings/Workplace.lua:1095: attempt to index a nil
  value (local 'traits')`) — which it can only have been handed after
  `GetCommutableWorkplaces` produced the connected list, i.e. after the
  `accept_colonists` gate was gone. No fifth ungated call path is involved.
- **DomeOverviewHighlight (F14) — probe.** The fix is right and the shipped UI
  wants exactly what it now passes: a T value is a TABLE in this engine
  (`Untranslated(s)` → `T{s, untranslated = true}`, localization.lua:343) and the
  shipped sibling paths hand the same kind of table to the same `SetText`
  (ColonyControlCenter.lua:502-507). The probe `tostring()`ed it and saw
  `table: 0x…`; it now reads the literal out of the T.
- **VacuumWalks (F52) — probe** (same root cause; the fixed run's "unset" meant
  `SetCommand` was never reached because the real `GetDomesPassagePath` answered).

Test Kit repairs (repo `C:\Dev\SMR-BugFixPack-TestKit`): deferred-verdict
mechanism replacing the raise (657b668), WithGlobals write-through (413d87c),
F73 partial PASS (57139f5), F14 T reader (3f1abb4), F52 message (77fdb72),
AutoRun `wait_for` timeout (d2636b7), Meteors logger global swap (42d9f43).
**The A/B pair must be re-run** — with the fakes finally visible, several probes
that "passed" or SKIPped were not testing what they claimed.
