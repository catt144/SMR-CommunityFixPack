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
