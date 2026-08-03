# Chain 11 — F76: the depot resource-picker repair (P1, its own dedicated sitting)

> ## ⛔ SEALED: `docs/reports/BLIND_AUDIT.md` — DO NOT OPEN
>
> **This prompt is FORBIDDEN from reading, grepping, summarising, or acting on
> `docs/reports/BLIND_AUDIT.md` or any part of its contents.**
>
> **Why (so this is not rationalised around):** it is a **blind control**. It was
> produced by a fresh session that deliberately read no project docs, and its
> entire evidential value is that it was written without the project's own
> conclusions in view. **Chain prompt 12, job 6b** examines it against the full
> record it was forbidden to see, doing its own pass first and only then opening
> the sealed key — so that neither reading anchors the other. **Any earlier
> prompt that reads it destroys the independence that comparison depends on, and
> the contamination is undetectable afterwards.**
>
> - Do not open it. Do not `grep`/`Read` it. Do not ask a subagent to.
> - **If a broad search incidentally surfaces its contents: stop, discard, do not
>   use it, and say so in your handoff notes.**
> - This is not a scope call you may weigh against a deadline or a judgment call
>   the blanket pre-clearance covers. **Only prompt 12, at job 6b, may open it.**

**One-off; delete this file in your final commit. Read `README.md` in this
folder first.** ⚠ This is the ONE chain prompt that is an ATTENDED sitting:
the standing hard rule bans live UI-internals prototyping in play sessions
precisely because F76's picker interaction once HARD-LOCKED the UI (session
lost) — this dedicated sitting, on a throwaway fixture save, is the sanctioned
place for it.

**Staleness check: `git log --oneline -10` + `git pull`.** Authority: the
BUGS.md **F76 entry** — it carries the owner's verbatim symptom report, the
full live forensics (the picker opens ALIVE at a wrong position on the
4K/80%-scale ultrawide), and the verified `TransferResources` workaround.
**Audit context that raised this item's priority:** an original-game report
shows the same player-visible failure on ordinary setups
(`BUG_LIST_AUDIT.md` §2.2 F76 — "The icon which should appear when I click on
a deposit does not appear!"), so do NOT assume the defect is ultrawide-only;
the fix must not be either.

## Jobs (todo list first)

1. ~~**Game-free design first**: from the entry's forensics, locate the
   positioning path that puts the `ResourceItems` dialog at (886,13) on a
   3751px window; identify the smallest §1-technique repair (anchor/clamp),
   and its self-check. Write the design on the entry BEFORE any live work.~~
   **✅ DONE 2026-08-02 — written on the `BUGS.md` F76 entry under *GAME-FREE
   DESIGN PASS*. READ IT BEFORE JOB 2; do not re-derive it, and do not read
   the rest of this file's framing as still current.**
   ⛔ **It did not confirm the entry — it refuted it.** The recorded
   "coordinate-space mismatch" does not exist (boxes and `terminal.GetMousePos()`
   are one space; vanilla's own `XDialog.lua:139` is the control), the recorded
   "Fix sketch" would have *introduced* the displacement, the click-through is
   fully explained by `ItemMenuBase:OnMouseButtonDown` forwarding L-clicks to the
   world (`ItemsMenu.lua:510-518`), and **the (886,13) box solves backwards to a
   single anchor ≈(969,442) with no clamp firing — i.e. it is what correct
   placement looks like.** The separately-recorded `(1731,665)` anchor is from a
   different click and may not be paired with it.
   ⚠️ **This job as written above was authored in the confirm-the-conclusion
   voice** ("locate the positioning path that puts the dialog at (886,13)") on
   top of a hedge the entry had marked *Suspected*. Filed to prompt 12's job-7
   seed list as its own axis. **Job 2 therefore leads with measurement (M1-M4 on
   the entry), not with a candidate repair**, and the §1 technique per outcome is
   chosen there in advance so the sitting cannot rationalise toward whichever
   answer arrives.
2. **Attended verification sitting** (owner at keyboard, fixture save,
   cheats fine): reproduce once, apply the candidate repair via TestKit
   console harness, verify click-through works at the owner's resolution AND
   at a windowed non-ultrawide resolution (the OG witness says ordinary
   setups hit this too).
3. Build the fix module; probe; the standard A/B leg (stale-probe gate).
4. Records: F76 status, checklist item for the campaign if any residue needs
   eyes, STATUS counts.

## Scope fence

**In:** F76 only. **Out:** any other UI polish; the F13/F14/F19/F20 UI
family (shipped, out of scope); anything the sitting surfaces gets filed.

## Stop conditions

- The UI hard-locks again → quit safely, record the exact step, and STOP —
  a second lock means the repair approach is wrong, not unlucky.
- The positioning path is engine-side (not reachable from Lua) → record the
  finding on the entry, present the workaround-documentation option to the
  owner (MOD_DESCRIPTION `[FAQ]` tag), and close the design question
  honestly rather than shipping a cosmetic half-fix.

## What may not be claimed

"Repaired" needs the attended click-through observed at BOTH resolutions.
An unreproducible session proves nothing — say "did not reproduce", not
"fixed".

## On completion

Outbox → `12_final_qa_backward_check_fable.md`. Delete this file, commit,
push.

## Notes from upstream

(prompt 10 appends state here)

### From chain prompt 10 (2026-08-02) — D12 is BUILT and UNRUN, and three things move to you

**State you inherit, not a summary to re-derive.** Prompt 10 built D12 as
`Opt_NoHomeless` (`14e708f`; probe + `60_Probes_Opt.lua`, TestKit `a979270`) —
opt-in, off by default, own module, own flag, own gate, `Opt_ResidencyControl`
as donor PATTERN only. **⚠️ UNRUN: the leg is `PLAYTEST_CHECKLIST.md` PT-62,
attended, predictions P1-P13 written before any run.** D12 claims no status
beyond `speced`. Counts re-derived by counting: **82 `Code/` files; 81 registered
modules, 74 default-active** (opt-in adds none); **87 probes**; **110 rows = 98 F
+ 12 D; 40 C**. **PROBE SWEEP: clean**, both repos. Recount, do not inherit.

**1 · ✅ ~~THE `DustDevilSpawnGate` CONFIRMATION~~ — DISCHARGED 2026-08-02, DO NOT
CHASE IT.** It **PASSED** in log `Mars.exe-20260802-20.43.08` (`78 PASS, 0 FAIL,
9 SKIP, 0 ERROR`). ⚠️ The first run after this note was written FAILED it — and
that was a **probe** defect, not a fix defect: the probe used `forbidden` as
scaffolding and 8c had since given that flag real behaviour. Both were repaired
and the re-run is clean. History below kept because the routing lesson stands.

**~~1 (as written)~~ — THE CONFIRMATION WAS ON ITS THIRD HOP.** 8c routed one unrun change to prompt 9 on the basis that it *"rides an
existing suite run"* — the `forbidden` early-return added to
`Fix_DustDevilSpawnGate` after PT-61, behaviour-neutral **by construction but not
by measurement**. Prompt 9 built nothing and ran no suite; prompt 10 built code
but its own leg is unrun, so the ride did not exist there either. **F76 is an
attended sitting: when you run `*r SMRTest.RunAll()`, confirm
`DustDevilSpawnGate` still PASSes and say so in your notes.** ⚠️ Third hop. If
your sitting also ends without a suite run, route it onward rather than dropping
it — and consider saying so to the owner, because an item that cannot find a
suite run in three prompts is telling you something about the routing rule and
not about the change.

**2 · ✅ ~~THE F98 LOCALISATION CONTROL~~ — RUN 2026-08-02, RESULT `userdata`.**
It **confirms** F98: a re-used translation id is discarded at `T()` construction,
so `Fix_TechDescriptionBuilding` never worked in retail and F25 stays demoted.
F98 no longer rests on source alone. **Do not re-run it.** The rest of this note
still applies to any UI text F76 adds — new strings go through
`Untranslated(…)`, appending to a shipped string goes through
`shipped_T .. Untranslated(…)`. Original text follows.

**~~2 (as written)~~ — STILL UNRUN, AND IT IS THIRTY SECONDS.**
`*r ModLog(type(T(8821, "ZZZ")))` — `userdata` confirms F98's reading (a re-used
translation id discards the replacement literal at `T()` construction, which is
why our shipped `Fix_TechDescriptionBuilding` never worked), `table` refutes it
and F25 would need restoring in both places. It is written into PT-62 as well, so
whichever leg runs first takes it. **F98 currently rests on source alone**, and
F76's own repair is UI work that may well add player-visible text — in which case
the answer matters to you directly: new strings go through `Untranslated(…)`, and
appending to a shipped string goes through `shipped_T .. Untranslated(…)`
(`TMeta.__concat` works on the retail light-userdata form).

**3 · ⚠️ A NEW CANDIDATE THAT TOUCHES NOTHING YOU ARE BUILDING, BUT IS OWED A
KEYBOARD.** **`C40`** was filed by prompt 10's pre-build check: `Crowded Living`
grants **+3 `Residence.capacity` gated on the Ministry of Culture's live
`working` flag**, and every withdrawal **evicts** the tail residents colony-wide
(`Residence.lua:224-235`). Mechanism verified vs Src end to end; **the gating is
intended** and the ministry building advertises it, so the open part is the
**law's own description** — it interpolates the static `<capacity_increase>` only,
so the player is told +3 and may be receiving +6, with nothing saying that losing
it takes homes away from people who already have them. **Harm unproven, frequency
unmeasured, nothing built, not a §4 package.** Its next step is one console
observation (enact the law, note a Residence's capacity, stop the ministry, read
it again) — **not your work, do not adopt it**, but it is a cheap rider if your
sitting happens to be on a colony with the law enacted.

⭐ **Worth one line because it is the reusable lesson, not the finding:** C40 came
from a **Reddit player's hypothesis** that prompt 10's brief said to *check, not
adopt*. The player was right about the mechanism, and checking it before building
is what chose D12's narrow reading over the broad one — under the broad reading
D12 would have converted a transient ministry outage into permanent migrations.
**The trap was invisible from the D12 plan.** It is the second time in three
prompts that a routed third-party claim paid for itself when checked first.

⛔ **The sealed document was NOT read, grepped, or surfaced at any point in
prompt 10.**


### Correction appended by chain prompt 10 (2026-08-02, later the same evening)

⚠️ **Two of the three items above are now CLOSED — read their headers, not the
bodies.** They were routed to you before the suite ran; it then ran, and both
resolved. Only **C40** (item 3) is still open, and it was never your work.

**D12 also changed substantially after this outbox was written**, so nothing here
describes it accurately: the subject test became vanilla's own `need_work`, the
policy gained a dome precondition (a Nursery or Retirement Home must be built),
tourist housing is excluded, and the infopanel row was rebuilt. `BUGS.md` D12 and
`PLAYTEST_CHECKLIST.md` PT-62 are current; this section is not. **PT-62 is still
UNRUN and is still what D12 is waiting on.**
