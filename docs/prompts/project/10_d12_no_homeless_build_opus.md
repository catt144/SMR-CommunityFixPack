# Chain 10 — D12: the no-homeless dome policy build

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
folder first.**

**Staleness check: `git log --oneline -10` + `git pull`.** Gate: the D10/D12
unhold recorded (prompt 5). ⚠️ **THIS GATE LINE WAS CORRECTED 2026-08-02 — it
used to read *"prompt 9 (D10) landed and its leg read clean"*, and BOTH halves
are false.** Prompt 9 ran and consumed itself but **built nothing and ran no
leg**: the owner parked D10 to post-release mid-prompt (see the notes below).
**Nothing about D12 is blocked by that** — the standing "never build D12 in the
same session as D10" rule is satisfied trivially, since D10 does not exist and is
not being built. Do not inherit a clean-leg fact from a leg that never ran.
Authority: **the BUGS.md D12 entry is the spec** — speced 2026-07-30,
user-approved.

## Jobs (todo list first)

1. **Build per the D12 entry**: own module; `Opt_ResidencyControl` as donor
   PATTERN only (not shared code); breaks vanilla's emigration tie for
   homeless colonists so specialist domes stop stranding them (also unwinds
   the D07 overpopulated deadlock without touching D07).
2. **Hard constraints from the entry (binding):** the new flag must NOT
   route through `CanAcceptNewColonists` (D03's gate) or it blocks the
   cohort delivery it exists to protect; **never expel to the surface**.
3. **Probe + the module's own A/B leg** (stale-probe gate; predictions
   first).
4. Its playtest item added to the checklist for the campaign (mirror what
   the entry specifies); STATUS/BUGS records.

## Scope fence

**In:** D12 per its entry, its probe, its leg, its checklist row.
**Out:** D10 (done or not — either way not here); D07 (untouched by design);
any residency behavior beyond the entry.

## Stop conditions

- The build cannot satisfy a hard constraint without redesign → STOP; the
  constraints are owner-set; spec the conflict on the entry and ask.
- Leg fails prediction → stop, report.

## What may not be claimed

`fixed` only after the leg; `tested` belongs to the playtest campaign. The
D07-unwind claim may not be asserted as verified — it is the entry's design
rationale until a playtest observes it.

## On completion

Outbox → `11_f76_depot_picker_repair_opus.md`. Delete this file, commit, push.

## Notes from upstream

(prompt 9 appends state here)

### Routed here from chain prompt 6 (2026-08-01) — one claim to CHECK before you build

A Reddit thread read this day (`BUG_LIST_AUDIT.md` **§10.5**, source **[S36]**)
has a player asserting the devs *"squashed two of the most pressing bugs with
the 1.0, **homelessness and unemployment**"* — homelessness being exactly D12's
subject. The same note went to prompt 9 for the unemployment half.

**Verify; do not descope on it.** Third-hand, vague about which 1.0.x, from a
satisfied player rather than a patch note, and ⛔ the thread is
**hotfix-1.0.3-era — four generations before our pinned 1.0.7.396349**. Project
rule stands: *"fixed in Relaunched" only from current Src.* One Src read settles
whether D12's premise survived a 1.0.x pass, and it is much cheaper before the
build than after.

### ⭐ AND a MECHANISM HYPOTHESIS for the same symptom — worth more than the claim above

Two **current** Reddit threads read the same evening ([S37]/[S38],
`BUG_LIST_AUDIT.md` **§10.6**) contain both halves of D12's symptom *and*, from
the player who lived it, a proposed cause nobody here has considered:

> *"people were constantly **flicking between being housed and unhoused**, and
> people genuinely just stopped working. There were jobs available in domes with
> unemployed people and they would not fill the job slots anymore."*
> …*"I think the homelessness issue was caused by **one of the law upgrades that
> allows homes to house more colonists**, because I'd check homes at their
> capacity would regularly fluctuate **because of staffing in the law spire**."*

A second commenter: *"Oh yeah, I heard about that."*

**Why this deserves a source read before you build.** If a politics law grants a
residence-capacity bonus that tracks **live law-spire staffing**, then dome
capacity oscillates as that building's workers come and go — and colonists at
the margin flip housed/unhoused on every swing. That is a **churn** mechanism,
not a shortage mechanism, and **a "no homeless" design aimed at shortage would
not fix it.** It would also explain why the symptom is reported as *flickering*
rather than as a steady deficit.

⚠️ **It is a player's hypothesis, not a finding** — no Src, one corroborating
"I heard about that", and the OP was describing a launch-era game. **Check it,
do not adopt it.** The check is small: find the law's `Effect_ModifyLabel` (or
equivalent) on residence capacity and see whether its amount is recomputed from
the spire's current workforce. If it is, D12's premise needs restating before a
line of code is written.

### From chain prompt 9 (2026-08-02) — D10 is PARKED, so three things move to you

**State you inherit, not a summary to re-derive.** Prompt 9 opened to build D10
and **built nothing**: the gate was clear, but when the bundled F84/T1
localisation decision went to the owner (job 1), the answer re-scoped the item —
**opt-in confirmed, text ships through our own `ModItemLocTable`, and D10 is now
PARKED / on hold, low priority, post-release.** Not owed, not scheduled, not to
be reported as outstanding. Counts re-derived by counting: **110 rows = 98 F +
12 D; 39 C**; **modules and probes UNCHANGED at 80 / 74 and 86** — prompt 9
shipped no code. **PROBE SWEEP: clean**, both repos. Recount, do not inherit.

**1 · ⛔ THE `DustDevilSpawnGate` CONFIRMATION OWED TO 8c IS NOW YOURS, AND IT
LOST ITS FREE RIDE.** 8c routed one unrun change to prompt 9 on the explicit
basis that it *"rides an existing suite run"* — the `forbidden` early-return
added to `Fix_DustDevilSpawnGate` after PT-61, which is behaviour-neutral **by
construction but not by measurement**. Prompt 9 runs no suite, so the ride does
not exist. **When you run `*r SMRTest.RunAll()` for D12's leg, confirm
`DustDevilSpawnGate` still PASSes and say so in your notes.** Probe count is
unchanged at **86** (8c added an assertion to the existing probe, not a probe).
⚠️ This is the second hop for this item; if D12 also ends without a suite run,
route it onward rather than dropping it.

**2 · ⭐ YOUR OWN JOB-1 CHECK JUST GOT A WORKED PRECEDENT — AND IT CUTS BOTH
WAYS.** Your brief carries the law-spire-staffing hypothesis for the *homeless*
half. Prompt 9 chased the twin question for the *jobs* half and found something
adjacent: **`Policy_Automation_ServiceAutomation` really does modify a workplace
capacity property from a law** — `LawEffectModifyLabel{Label="ServiceBuildings",
Prop="max_workers", Percent=-50}` (`Data\LawDef\LawDef-Technology.lua:227-234`).
So **"a law that moves building capacity" is a real, shipped shape in this game**
and your hypothesis is not exotic. ⚠️ **But that one is a static percent, not
recomputed from live staffing** — which is precisely the distinction your check
must make. Finding a law that touches capacity is not finding the churn
mechanism; the question is whether the *amount* tracks a workforce that changes.
Do not let the first half of that sentence stand in for the second.
Filed as **C39** in passing, for an unrelated reason (that law's compensation
keys on class while its effect keys on label, and the four Workshops sit on one
side only) — **not your work, do not adopt it.**

**3 · ⚠️ THE LOCALISATION FACT, BECAUSE ANY UI STRING YOU ADD IS GOVERNED BY IT.**
D12 ships a **dome infopanel toggle row**, which means player-visible text. Three
routes exist and only two work: **re-using a shipped translation id is a NO-OP in
retail** — `T(id, text)` returns `LocIdToLightUserdata(id)` and discards your
literal (`CommonLua\Core\localization.lua:250-252`), which is how our own
`Fix_TechDescriptionBuilding` turned out never to have worked (**F98**, filed
this session; **F25 demoted in both places and is no longer precedent for
anything**). Use `Untranslated("…")` for a new string, or `shipped_T ..
Untranslated("…")` to append to an existing one — `TMeta.__concat` works on the
retail light-userdata form (`:359`, `:373-412`; shipped precedent
`Workplace.lua:293`). ⚠️ **A 30-second live control is queued and unrun**:
`ModLog(type(T(8821, "ZZZ")))` — `userdata` confirms the reading, `table`
refutes it. **It costs one console line on your leg; please take it**, because
F98 currently rests on source alone.

⛔ **The sealed document was NOT read, grepped, or surfaced at any point in
prompt 9.**
