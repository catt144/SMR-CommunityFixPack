# smrtk 99 — the terminal adversarial audit

Link 99 of `smrtk`. Fable, fresh context; your job is to **disbelieve the chain**. README rules 1–22 are yours.
Run only on a folder holding this file and `README.md` (or in the reduced form below).

## Full form

1. **Inbox audit:** every upstream close-out's outbox landed where it said (successor + here + README row) in one commit.
2. **Owed-work sweep:** every routed item has an owner and a TAKEABLE-WHEN; nothing lives only in a session's memory.
3. **The taint invariant, re-derived, never inherited:**
   - `grep -n "NetSyncEvent\|LogCheatUsed" <every SMRTK file + 80_AgentSlots.lua>` → 0, **with the presence side**
     (the same grep on `Data/CheatDef.lua` → 13+) so the negative is a sample;
   - every registered action's `run` read line by line against `EF-095`/`EF-098`: leaf call or not;
   - 02's and 08's `CheatsUsed` reads located in the **archived logs** by line, and the scratch-save control's RED;
   - the eligibility read at 08's end, in the log. On build 24995074 it must
     honestly report `UNAVAILABLE:sandbox` (`EF-096`). CanUnlockAchievement is
     blacklisted; no taint read proves full eligibility. Adjudicate this
     measurement limitation explicitly against requirement (A), never silently
     accept it as an observed eligibility PASS.
4. **The tag invariant:** from 08's archived log, every line the toolkit wrote carries `[SMRTK] SMRTK_`; count the
   toolkit's actions in the log against the panel's fire counters (a total is not a set — reconcile).
5. **The idle invariant (rule 9):** with nothing armed, enumerate every vanilla function the toolkit has replaced
   (`SourceOf`-style, as the TestKit's `[install]` probes do) → 0; then arm each toggle, count, disarm, count 0 again.
6. **Falsifiers RED:** the session-id guard refusing a foreign slot; a stamp skipping an unbuildable hex by name;
   auto-disarm after a load; `SMRTK_TAINT` firing when you call a sync wrapper on purpose in a scratch save
   (then delete that save and record it).
7. **Docs vs built:** every button in PLAYTEST_HELP exists; every file in the README's layout table is in
   `metadata.lua`'s `code` list and vice versa; `perma/SMRTK_SLOTS.md` has a row.
8. **Verdict:** SHIP / SHIP WITH CHANGES / NO SHIP in `reports/SMRTK_AUDIT.md` and, in plain language, to ck175.
   "Ship" here means *the owner uses it*; the TestKit never uploads (`H-04` still binds the wording).
9. **Kickoff lines:** the first real sitting the panel serves (fire `perma/SMRTK_SLOTS.md` against it — the owed
   ck144(a) boot is the natural candidate; say whether it is), and none else unless queued.
10. Consume this file and the README's queue (the README stays as the record, its table fully struck); delete the
    folder's row in `prompts/README.md` **in the same commit** (PROMPT MAP gate); SESSION_LOG entry; STATE's NEXT line;
    record the executed model (R-G); push.

## Reduced form — if 02 KILLED the chain

Post-mortem appended to `agent/reports/CHAIN_METHOD.md` §3 (a row: failure · instance · countermeasure); the
respec-or-abandon decision routed to ck175 with a recommendation (the likely respec: which premise fell — if P1,
the toolkit cannot exist as designed; if P2–P4, it can, minus that feature); every unconsumed prompt `git rm`'d with
its grave (`git show <sha>:<path>`) named in the README; the five facts `EF-095`–`EF-099` **amended, not deleted**,
with what the game showed.

## What may NOT be claimed

Anything you did not re-derive or re-read yourself. "Release ready" (`H-04`). That the no-taint property holds on a
build other than the one 02/08 ran on.

## Notes from upstream

- (authoring session, reshaped 2026-09-13) 03A (Codex) built and 03B (Claude) judged; read 03B's **disagreements
  with 03A** before either report's claims, and adjudicate each on evidence — a cross-vendor split is the point of
  the pair, not noise. Also check 03A actually ran the spike BEFORE launching P2/P3 (commit order of
  `reports/SMRTK_UI_HOOKS.md` vs the payload files) and consumed `payloads/` on its close-out.

- (authoring session `smr-bugfixpack-8f`, 2026-09-13) Two premises were flagged unverified at authoring: native
  `ConsolePrint` → `ConsoleLine` (`EF-096`), and retail `Platform.cheats` (`EF-095`). Check 02 measured both rather
  than inherited them. The facts were written in one session from source reads at build 24995074 — if the game
  updated between authoring and 02, the fingerprint says MOVED and 01 must have re-derived; check that it did.

- **01 outbox, 2026-09-13:** core `774b55a`, panel `b400683`, metadata `5d8d3b3`
  in the local TestKit. `reports/SMRTK_SKELETON_PREDICTIONS.md` contains numbered
  claims, exact commands/results, actual API, **DRIFT**, **DEPARTURES** and
  **SUGGESTIONS**; `SMRTK_SKELETON_SMOKE.py` is the reproducible desk model.
  Code and metadata gates GREEN; nothing ran in game, no status promoted.
- **Disagreements to judge first:** CanUnlockAchievement's blacklist makes the
  proposed eligibility read impossible; Ctrl-Shift-K has a developer collision;
  00_TestCore already enables/rebuilds/auto-opens console and would mask our
  hook; an arbitrary old playtest save cannot provide the no-taint control.
  02's script handles these, registers its own Fill action, and separates
  toolkit ring insertion from actual native/tee output. Inspect the two
  native witness outputs, not input-command echoes or toolkit lines alone.
- **DEPARTURES:** eligibility unavailable; Ctrl-Shift-F11; current-mark/absolute
  index Copy; explicit isolated console rebuild control; empty payload pages.
  **SUGGESTIONS:** judge retirement of the legacy console bootstrap after 02;
  require delayed payload mutations to dispatch through Run/Fire inside their
  threads; budget clean fixtures. All drift (including desk corrections) is in
  the report. Scope was extended only for the reusable smoke and fact/prompt
  corrections required to route those findings. 07/08 inboxes carry the same
  eligibility correction. Requirement (A) has not been weakened.
- Model-seat drift: peer `b9501dd` updated the manifest/ck175 but the old 03A/07
  headers still said Astra. 01 aligned those two headers to Sol; payload seat
  choices are inherited from the manifest's explicit per-payload row.

- **02's OUTBOX, appended by the orchestrator (`smr-bugfixpack-8f`, 2026-09-13) — verbatim from `reports/SMRTK_SKELETON_SITTING.md`.** ⚠️ 02 wrote both outboxes into its report and struck its row and consumed its prompt, but did not append them to the inboxes; chain rule 2 requires both, and a pointer is weaker than an append because this is the file you actually read. Nothing below is my wording. The full verdict, the five superseding corrections and the archived logs are in that report.

  > The taint invariant is re-derivable from the archived logs alone: `ObjCheat`
  > count 1 in the control boot, 0 in the toolkit boot. The four `LogCheatUsed` call
  > sites were enumerated tree-wide and none is reachable from a direct leaf call.
  > Two instrument defects on the attending side are recorded in full rather than
  > quietly fixed — a truncated `grep | head -15` that hid the `CheatFill` override,
  > and a proposed flicker control that could not have cleared the panel because
  > `panel_toggle` only calls `SetVisible(false)`. The flicker itself is routed,
  > measured and **unattributed**; the last boot carried the mod with no strobe, so
  > it does not reproduce on mod-load alone.

### 03A build outbox, 2026-09-13

Codex 03A completed five payloads plus shared core/panel extensions. Final
TestKit HEAD `cee5bab230f2fac876aa0e6d86bb97f6b56ad020`; TestKit has no remote. The pack close-out commit
contains `reports/SMRTK_FANOUT_REPORT.md`, all five numbered payload reports,
format, independent gate/model commands, EF-099 source corrections, and the
spent briefs' removal. Restore a brief from the close-out commit's parent
when a re-fire is needed. No new page/native effect/save-load/stamp has run
in game. 02 final PASS/outbox remains the prerequisite authority; 08 is next
full game evidence after 03B/07. No status/version/pack-runtime edit occurred.

Re-run actual HEAD commands, opening routes rather than accepting reports:

```text
python docs/agent/reports/SMRTK_FANOUT_GATES.py --ordered --presence
python tools/parsecheck.py --dir ../SMR-BugFixPack-TestKit/Code --quiet
python docs/agent/reports/SMRTK_FANOUT_SMOKE.py
python docs/agent/reports/SMRTK_P1_SMOKE.py --selftest --list
python docs/agent/reports/SMRTK_P2_SMOKE.py
python docs/agent/reports/SMRTK_P3_SMOKE.py
python docs/agent/reports/SMRTK_P4_SMOKE.py
python docs/agent/reports/SMRTK_P5_DESK.py
python docs/agent/reports/SMRTK_FANOUT_MERGE.py --selftest
python tools/doccheck.py
```

Coordinator per-file gates are copied verbatim in the main report: parse0,
no-sync0/no-bare-print0 on each owned file, H-10 listed, doccheckGREEN;
presence26. Final TestKit tree clean. Main report contains all warnings,
full core/panel/90 diff and emitted file/function/line inventory. No payload
failed the required gate; no gate re-fire was used. Every final page and
cross-id resolves. Slot buttons deliberately remain unbound until sitting
preparation; print_tee is a registry helper, not a Kit button.

Cross contracts: P2 Dump=dump_selected; Pins=pin_A/B/C; P4 watch_field creates
P3 watch_selected_field disarmed, then explicit Arm; P5 follow-ups dynamically
Run fill_storages(), spawn_colonists(10), funding(500000000). Logger ids are
logger_<native name>; read-only 90 LoggerState returns enabled-copy. Quiet
and any native/toolkit logger refuse nesting, preserving captured originals.
MARK -> primary record -> taint assertion -> guarded after_record.MARK ->
separate fingerprint action covers normal/screenshot marks; refused marks
skip hook. The callback coordinates read-only/separately dispatched evidence.

Required disagreements/departures first: no building construction test flag;
terrain is not complete fit; owned-site completion avoids CompleteAll scope;
grid steps include endpoints/each returned cell must pass; passage topology
not represented; non-Code layouts load early via literal queue; safe helper
installation corrects broad blacklist claims; Delete class overrides/busy
mechanized refusal; ["do"] Lua spelling; trigger real-time effect handoff;
native screenshot accepted is not pixels; native metadata read helper avoids
DoneGame; deterministic save name; provenance callback attempts/last record;
scoped snapshot; explicit sitting-bound desktop probe attestation; P5 second
unit follows THREE SYNTHETIC PLANS, not native stamps. Passage/special objects
and variants have named v1 skips; native geometry/GameInit remains unmeasured.

Main report OWNER-ROUTED contains every merged payload recommendation, with
recommendations on hybrid surface/Delete/48-character save strip, unavailable
eligibility, quiet/modern rocket, run-until attempt semantics, scalar/error/
screenshot limits, probe attestation/current-branch fixture/legacy00 console,
scoped two-map snapshot and bounded Stamper/passages/partial abort. 03B makes
ONE ck175 append with its recommendation for each, no scattered requests.
Final per-page button table, emitted World registry, P3 verbatim slot template,
P4 preflight contract and P5 measured-count 08 recipe are for07 AFTER03B.

DRIFT is preserved, including stale02 header vs finalPASS, initial wrong
paths/quotes/globs/parse CLI, EF-099 linesRED->emittedregenGREEN, corrected P2
SHA before commit, untracked pathspec refusal before git-add, source/helper
claims, screenshot-thread falsifier failure, quiet re-arm correction, false
reads/provenance/id/disaster scope, P5 parent/FIRE refusal, shared scrollbar,
combined fake PropObjHasMember omission, and nine alias UNKNOWN initializer
false positives (00_TestCore order/probes/last opened19-21). Foreign dirty
archive planning remains untouched. Do not count failed queries as negatives.

Late03A source correction: native XTextEditor.Init clears its buffer; raw
constructor Text does not initialize it. P3 already used SetText correctly;
coordinator after release added setters in72/76/77, one-file gated commits.
Strict combined fake now discards constructor Text; three editor counterfeits
(World/Kit/Stamper) each goRED. Review XTextEditor171-175,221-228 and
XControl624-634. P5 nineteen cases did not model editor initialization.

### 03B judge outbox, 2026-09-13 — the cross-vendor split for you to adjudicate

Verdict **PASS WITH FIXES**, `reports/SMRTK_JUDGE.md`. Judged at pack `2be7c73`,
TestKit `cee5bab`; my one label fix makes TestKit `87f3130`. No game ran:
`tasklist` for `Mars.exe` returned `INFO: No tasks are running which match the
specified criteria.`

**My disagreements with 03A, verbatim, for you to split:**

**D1 — the one that matters.** 03A built P2's Selected section as a fixed table
of 22 `Cheat*` member names (`73_SMRTK_Infopanel.lua:6-23`). Vanilla's section
does not use a list: `InfopanelObj:CreateCheatActions`
(`Lua/X/Infopanel.lua:22-40`) walks the metatable chain and offers every
`Cheat*`/`AsyncCheat*` member. Measured on build 24995074: **94 `Cheat*` + 12
`AsyncCheat*` = 106** distinct member names; P2 covers 22; **84 are gone**, and
`AsyncCheat*` is absent as a category even though `SMRTK_UI_HOOKS.md:108`
records that 03A knew those already avoid taint. Because the toolkit never sets
`config.BuildingInfopanelCheats`, there is no fallback to them.
Sharpest instance: `CObject:CheatDelete()` is `DoneObject(self)`
(`_cobject.lua:1591-1593`) and is the only one of the 22 a Colonist matches, so
the section offers the blunt universal removal while hiding
`Colonist:CheatKill()` (`Colonist.lua:5144`) and `Drone:CheatDespawn()`
(`Drone.lua:2989`).
**03A conformed to its brief** — the P2 payload named exactly this list — so what
I am handing you is the frame, not the conduct: is this "built to spec", or "an
unstated gap in the headline deliverable"? I called it the second, because
neither DEPARTURES nor SUGGESTIONS states the ratio, the dynamic route, or the
dropped category. I did **not** RE-FIRE: no gate failed, no invariant broke, and
the repair is a build outside my fence. Routed to ck175 item 1 as an owner scope
call.

**D2 — 03A asked me to rule on retiring `00_TestCore`'s console bootstrap; I
ruled invert, not retire.** `00_TestCore.lua:519` calls `ConsoleSetEnabled(true)`
at load, the one spelling rule 10 forbids (it also calls `ShowConsoleLog`,
forcing the overlay `70_SMRTK_Core.lua:354` avoids). Retirement is wrong — the
console is how probes are run, and 00's comment records a real dead-binding
session — so the fix is to try plain assignment first and keep
`ConsoleSetEnabled` as the fallback. Not applied: pre-existing infra, outside my
five files. Note 02 already killed the evidence confounder with a discriminating
A/B (`SMRTK_SKELETON_SITTING.md:416-439`), so this is hygiene, not a hole.

**Where I agree with 03A, having checked rather than assumed:** all 54 P1 and all
21 P2 routes open to clean leaf bodies (I extracted each body from source and
grepped it for `NetSyncEvent`/`LogCheatUsed`); the three shared techniques were
genuinely shared (exactly one `terminal.AddTarget` site, `70:416`, with all
three consumers going through `T.AcquireClick`); rule 9 holds with exactly three
global writes in two toggles; rules 6/7/10/11 hold; every cross-id resolves;
P5's bounded completion via `site:Complete("quick_build")` is the correct
response to `EF-099`'s amendment; P4's refusal of `LoadMetadataCallback` (it
calls `DoneGame`) is load-bearing and right. I accepted P5's synthetic-plan
gate: the brief's native-stamp gate was unsatisfiable inside 03A's fence, so it
moves to 08 rather than being waived.

**Instrument caution for you.** 03A's gate/smoke/merge scripts are 03A's own
instruments. I re-ran the raw rule 6/7 greps and re-derived both README "Derived
facts" by hand rather than inherit the harness — they agreed. But the harness has
never been falsified against a known-bad tree. One cheap control if you want it:
point `SMRTK_FANOUT_GATES.py` at a scratch copy with a single `NetSyncEvent`
inserted and require RED. While re-running I found the manifest's own recipe is
vacuous: `grep -c "NetSyncEvent"` on `CheatDef.lua` returns **26**, not the 13
the table claims (13 calls + 13 `Comment =` lines). Routed to 07.

**A false alarm, recorded so it is not re-run.** `75_SMRTK_Saves.lua:6` calls
`os.time()` at load and `os = true` **is** in `ModEnvBlacklist` (`Mod.lua:1438`;
the table spans 1280-1441, while `EF-096` says 1280-1416 — also wrong). It is
still fine: `LuaModEnv` rawsets `env.os = { time = os.time }` at `Mod.lua:1618`
before attaching the metatable. No finding; two `EF-096` corrections routed to
07.

**DRIFT to add to yours:** 03A's close-out commit `b4aadb4` carries a UTF-8 BOM
in its subject line — the known PowerShell 5.1 rig hazard. My own drift: I spent
a full verification cycle on the `os.time` false alarm before finding
`Mod.lua:1618`; the blacklist read alone was not sufficient evidence and I
should have looked for the env constructor before drafting a finding.

**What I did not open**, so you know where I could be wrong: the panel's
rendering path (`71_SMRTK_Panel.lua` beyond its registered ids), `91_Stress.lua`,
and 25 of the 54 P3-P5 actions (I opened 29). I opened **all** of P1 and P2.
