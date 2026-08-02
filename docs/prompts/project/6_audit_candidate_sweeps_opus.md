# Chain 6 — audit candidate verification sweeps (game-free reading)

**One-off; delete this file in your final commit. Read `README.md` in this
folder first.** Game-free; no `Code/` changes; READ-ONLY on the game dir.
Evidence base: `docs/reports/BUG_LIST_AUDIT.md` §5/§9 + the BUGS.md C-entries
named below. Extracted mod sources, if needed, re-derive via
`tools/flpk_extract.py` over the archived FPKs in
`C:\Dev\workshop_fpk_archive\` (all six mods, copied 2026-08-01 before any
unsubscribe — including the REMOVED fredware mod, whose FPK is otherwise
unrecoverable). Workshop subscriptions are no longer required for any chain
work.

**Staleness check: `git log --oneline -10` + `git pull`.**

## Jobs (todo list first; one item per sweep; each ends in a BUGS entry update)

1. **C32 sweep (ShiftsBuilding label desync).** Find the de-labeling path in
   Src (map unload? relabel?); check whether `AddToLabel` re-registration is
   safe; **and answer the owner's standing challenge: did 1.0.7 already fix
   it?** (GromGor's workaround is 1.0.6-era — the one packed-source finding
   never verified against current Src.) If 1.0.7 fixed it AND the witness
   thread's reports predate 1.0.7 → **re-examine F04's witness reassignment**
   (BUGS F04 audit note) and correct the audit record either way.
2. **C04 sweep (cross-map supply-grid breaks).** Trace WHO calls
   `SupplyGridFragment:RandomBreakConnection` (`SupplyGrid.lua:669-683`)
   during a surface dust storm and HOW an underground connector enters
   `self.connectors`. Verdict: F-row (with tier + intent tell) or corrected
   record.
3. **F35 scope check.** Source-level: does the old-save fixup our F35 ships
   cover the LIVE Frictionless-Composites label miss the audit's witness
   thread describes (audit §2.2 flag)? If the live case is real and
   uncovered → file it (new F-row or F35 extension) — do not fix here. The
   keyboard rider from prompt 1 settles the live half if source can't.
4. **fredware #11 comparison pass.** His
   `bf_restore_asteroid_lander_cargo_safety` ("payload changes interrupting
   drones/passengers on the cargo ramp") vs our F67/F68/F70 family — gap,
   overlap, or covered? One paragraph on the audit report §9 + a C-row if
   it's a real gap.
5. **Owner homework reminder (no session work):** the two audit stop-and-ask
   items still open — a logged-in Paradox subforum browse (F01's claimed
   report, F64's "void" report, F74's rival-rocket report) and a Paradox
   Mods browser check (console channel; feeds D13). If the owner has done
   them, record the outcomes on the relevant entries; if not, route the
   reminder to prompt 12's inbox.

## Scope fence

**In:** the four sweeps + records. **Out:** any fix; any decision (prompt 7
owns decisions); C22-C24 (already Src-verified — nothing to sweep); anything
the sweeps surface gets filed + routed, not chased.

## Stop conditions

- A sweep contradicts a recorded audit verdict → update the record with the
  new evidence trail and say so prominently (recorded facts are claims).
- Context pressure → self-split (`6b_…_opus.md`).

## What may not be claimed

No verdict without file:line read this session. "Already fixed in 1.0.7" only
by reading current Src, never by patch-note text alone.

## On completion

Outbox → `6b_residual_candidate_sweeps_opus.md` (overlapping verdicts) and
→ `7_audit_candidate_decisions_opus.md`: sweep verdicts that change its
decision packages (esp. C32/F04). Delete this file, commit, push.

## Notes from upstream

### From prompt 2 (2026-08-01) — your job 3 is already answered by measurement; do not re-run it

**Your §3 "F35 scope check" says *"the keyboard rider from prompt 1 settles the
live half if source can't."* The rider was taken.** It rode the F86 Phase-0
sitting opportunistically (a colony was already up), and it settles the live half
outright, so job 3 shrinks to at most a source cross-check — **do not spend a
sweep on it and do not file an F-row for the live case.**

**Result: the live label path WORKS, for all three labels including
`WindTurbine_Large`.** Log `Mars.exe-20260801-14.59.57-6a22b86d.log`. From a
**pre-research save** (so our pass could not have run first — it early-returns at
`90_SaveSanitizer.lua:58` when the tech is not researched) with **no reload in
the window**: before = all three labels `NO MODIFIERS`; after = all three carry
`prop=electricity_production percent=100`, keyed by the vanilla
`Effect_ModifyLabel` objects with `id=GameEffect` (**not** `SMRFixPack_F35_*`, so
it is the tech's apply and not ours), and **Power doubled on every turbine**
(9.3→18.6 / 18.6→37.2 / 29.8→59.5) — so label membership is intact for these
classes too, not merely the colony table. Full record incl. the exact
grant-vs-natural-path equivalence: **BUGS.md F35**, where the audit's ⚠ OPEN
SCOPE QUESTION is now closed; the checklist row is struck through.

**What that leaves you:** F35 is the old-save migration failure it was filed as.
The audit's §2.2 ⚠ suspicion — that our fix is aimed one layer too shallow and
quietly repairs a live defect on every load — is dead. The one thing NOT
established is that the Nov 2025 witness was wrong about *their* game; this
measures 1.0.7.396349's live path only, so if your source pass wants to say
anything about older builds, say it as its own claim.

⚠️ **Carry this trap into any similar reading you do.** The first attempt read
the labels while **Low-G Turbines** was completing, not Frictionless Composites.
`LowGTurbines` (`TechPreset.lua:2830-2844`, group Physics) grants two
`Effect_UnlockUpgrade` entries and **no label modifier at all**, so its perfectly
correct `NO MODIFIERS` result looked like a defect three times bigger than the
one we were hunting and came close to being filed. It is also the "polymer
upgrade works now" half of the witness's own sentence. **Confirm the tech
identity (`IsTechResearched("<id>")`) in the same log line as any label read.**

*(Nothing else here is yours; C32's label-membership rider is untouched — its
mechanism is the asteroid-visit `ShiftsBuilding` case and this reading says
nothing about it.)*

### From chain prompts 5 + 5b (F86 Tier 2, 2026-08-01) — BUILT AND VERIFIED, chain is clear ahead of you

**Nothing here is work for you.** This is state, so you do not re-derive it.

**✅ F86 TIER 2 IS DONE.** Four modules moved off their blocking bodies onto
verified-synchronous seams (`88f3154`, `44e6af2`, `6f0cb95`, `ef7d49c`,
`e197190`, `77683c8`; TestKit `6eb3c0b`, `7bfa274`), and **PT-58 ran with the
owner and passed all seven predictions**: the uninstalled load carried **zero**
`Opt_DroneOverhaul` orphan errors against Tier-1 leg 5's **80**, over an article
holding 73 idle drones. **F86 Site 2 is CLOSED — both proven leak sites are now
repaired and verified.** The `ArrivalDeaths` half-(a) design pass was run and
found a route, so it was built rather than deferred; nothing was routed to
prompt 12 from it.

**What changed under you, in case a sweep touches these files:**
- `Fix_DroneUnreachableForever`, `Fix_TrainWaitTime`, `Fix_ArrivalDeaths` and
  `Opt_DroneOverhaul` are all wrappers now — **none replaces a body**. If a
  candidate sweep proposes anything for these, read the entry first.
- **F21 was downgraded `tested` → `fixed`** (PT-43 measured a retired body). F53
  and F55 stay `fixed`. **PT-58 earned NO status flip** — its P1-P3 are fixture
  results, and the leg verified save safety, not function.
- **D10/D12 are UNHELD** (prompts 9 and 10 are runnable). That does not change
  your order: 6 → 6b → 7 → 8 still runs first.

**Two limits recorded on PT-58 that a later session must not read past:**
1. **D06 part 2's moonlighting is untested** — every hub read `unclaimed=0`, so
   the `self.command == "Idle"` gate never fired. Save safety does not depend on
   it; function does. Its home is the frozen PT-52, not a sweep.
2. **The clean uninstall is not a Tier-3 clearance** — it means no accepted
   residual happened to be in an erroring state on that save.

**➡️ ONE ITEM ROUTED PAST YOU TO PROMPT 12** (not yours, recorded so it is not
lost twice): an asserts-build sitting with `SMRTest.EnableIntrospection(debug)`
typed into the un-sandboxed console would clear the **eight `[install]` probes
that SKIP on every retail run** — standing TestKit coverage the project has
never had. The mod sandbox applies on all builds, so MarsDebug alone does not do
it (verified 2026-07-26). Deliberately not run during PT-58, whose baseline was
measured on retail.

**Instrument note you may want:** `tools/blocking_analysis.py` takes a JSON list
of `[label, name]` pairs and answers "can this yield?" per name. Tier 2 used it
for every "verified synchronous" claim. If a sweep needs that question, use it
rather than grepping for `Sleep`.
