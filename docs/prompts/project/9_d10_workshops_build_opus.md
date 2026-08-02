# Chain 9 — D10: the workshops module build (+ the bundled F84 text decision)

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
unhold must be recorded (prompt 5). Authority: **the BUGS.md D10 entry is the
spec** — speced 2026-07-30, user-approved; do not re-design it.

## Jobs (todo list first)

1. **The bundled F84 decision — ask BEFORE building T1.** D10's T1 text
   repairs and F84's Universal-Tunnel description fix share the identical
   localization tradeoff (a localized `T` becomes an English-only
   `Untranslated` string) and the standing rule says they must not be
   answered twice differently (STATUS/F84 entry). Present both together:
   one owner answer covers T1's shape AND whether F84 ships with it.
2. **Build per the D10 entry**: T1 text repairs + T2 capacity dial
   (base/+50%/+100%, `max_workers` AND `consumption_amount` PAIRED), as an
   `Opt_` module per the entry's shape.
3. **Add PT-57** (~7 min, per the entry) to the checklist at build time —
   the owner runs it during the playtest campaign; this chain does NOT run
   attended tests.
4. **Probe + the module's own A/B leg** (stale-probe gate; predictions
   first). D10 touches colonist assignment — the reason it was held —
   so the leg's zero-FAIL bar is absolute.
5. STATUS/BUGS records; F84 entry updated with the decision either way.

## Scope fence

**In:** D10 exactly per its entry, the F84 co-decision, PT-57's checklist
row, the leg. **Out:** D12 (NEVER in the same session — the two both touch
colonist assignment and the standing rule says land them separately, each
with its own A/B); any workshop behavior beyond the entry's spec.

## Stop conditions

- The owner's F84/T1 answer changes T1's shape materially → re-check the
  entry's spec still holds before building; if it doesn't, stop and ask.
- Leg fails prediction → stop, report.

## What may not be claimed

`fixed` only after the leg; `tested` only after PT-57 PASSES (that flip
belongs to the playtest campaign, not this session — say so in the entry).

## On completion

Outbox → `10_d12_no_homeless_build_opus.md`. Delete this file, commit, push.

## Notes from upstream

(prompt 8 appends state + counts here)

### Routed here from chain prompt 6 (2026-08-01) — one claim to CHECK before you build

A Reddit thread read this day (`BUG_LIST_AUDIT.md` **§10.5**, source **[S36]**)
contains a player asserting that the devs *"squashed two of the most pressing
bugs with the 1.0, **homelessness and unemployment**"* — the exact subjects of
**D10 (workshops / unemployment)** and D12.

**Treat this as a prompt to verify, NOT as a reason to descope.** It is
third-hand, vague about which 1.0.x, and comes from a satisfied player, not a
patch note. ⛔ The thread is **hotfix-1.0.3-era, four generations before our
pinned 1.0.7.396349**, so it says nothing about the build we ship against
either way.

**What it costs you is one Src read**, and this project's own rule says who
wins if they disagree: *"fixed in Relaunched" only from current Src, never from
patch-note or forum text alone.* If unemployment's cost really did become
visible in a 1.0.x pass, D10's premise changes and you want to know that before
building, not after. If it did not, you have spent five minutes and closed a
loose claim that would otherwise have surfaced during QA.

**⚠️ And a CURRENT report pointing the other way, so you do not read the above
as settled.** Two Reddit threads from 2026-07-30/08-01 ([S37]/[S38], §10.6)
carry the symptom in plain terms: *"people genuinely just stopped working.
**There were jobs available in domes with unemployed people and they would not
fill the job slots anymore.** My entire industry started falling apart."* That
reporter was describing a launch-era game, so it is not proof of current
presence either — **which is the point: you have one player saying it was fixed
and another describing it in detail, and neither is Src.** Read the code.

**One more thing worth knowing before you scope D10.** The same threads produced
a mechanism hypothesis for the *homelessness* half (a politics law whose
residence-capacity bonus may track live law-spire staffing, making capacity
oscillate) — routed to prompt 10 and written up there. **If that shape is real
for housing, ask whether the jobs half has a twin**: a workplace-capacity or
performance modifier that also tracks a live workforce would make employment
churn the same way, and a design aimed at a *shortage* would not fix a *churn*.


### From chain prompt 8b (2026-08-02) — the batch is verified; three things bind you

**State you inherit, not a summary to re-derive.** Chain 8b built the seven
prompt-7-approved fixes (F90-F96), wrote seven probes, and **ran PT-60 with the
owner. The batch is verified**: `76 PASS, 0 FAIL, 9 SKIP, 0 ERROR` (85 = the probe
count), `79/79` modules active with zero `[LUA ERROR]`, measured on the **enable
path**, and 15 minutes of unpaused play produced no log output at all. Prompt 8's
**eight conversions are no longer unrun** — they install active and behave
invisibly. Counts are unchanged and already re-derived: **108 rows = 96 F + 12 D,
38 C; 79 registered modules / 73 default-active; 85 probes.** Recount, do not
inherit.

**1 · ⛔ Every load-time heal in this pack is suspect until round-tripped.** Two of
this batch's three heals were **not idempotent**, and neither was visible to source
review, to code review, or to its own passing probe — only a save/load round trip
exposed them. `Fix_AstrogeologistExtractors` added +10% on *every* load, unbounded,
because its presence test compared **object identity** and the persisted key is a
different table after a load. **If D10 ships anything that runs at `LoadGame` or
migrates saved state, save-and-reload twice before believing it**, and do not key a
presence test on an object that crosses a save boundary. Full write-up: prompt 12's
job-7 block, where it is filed as a new shape.

**2 · A prediction that reads a module count must read the toggles first.** PT-60's
P1 predicted `73/79` from `metadata.lua`'s all-`false` `default_options` and the run
read **`79/79`** — because **Mod Options survive a Mod Manager disable** and six
opt-in modules were on in that profile. Now in `ENGINE_FACTS.md` beside the
three-switches table. Read `CurrentModOptions` or just run `ListFixes()`.

**3 · Two riders are open and cannot be taken on a terraformed colony.** F90's
underground-break distribution and F93's dust-devil map switch both need a colony
**below the `DustStormStop` atmosphere threshold** — dust devils share that gate
with dust storms (`TerraformingDisasters.lua:34-52, :69`), so on a terraformed save
both are structurally impossible. Check `DustStormsDisabled` before spending a
sitting on either.

⛔ **The sealed document was NOT read, grepped, or surfaced at any point in prompt
8b.** One `git add -A` staged it in a single commit; it was amended out before any
push and the file is untracked again. Nothing in it was opened. **Name your paths
when you stage.**
### From chain prompt 8c (2026-08-02) — counts moved, and one warning worth two minutes

**Counts, re-derived by counting — recount rather than inherit these too:**
**109 BUGS rows = 97 F + 12 D**; **38 C**; **80 registered modules / 74
default-active**; **86 TestKit probes**. `8c` filed and built **F97**
(`Fix_DustDevilSpawnGate`, C23 item 1) — one new module, one new probe, one new
row. ⚠️ **74 default-active is `80 − 6`, not `80 − 7`**: seven modules register
with `optional = true`, but `Opt_DroneStatDials` reports **active at base** by
design. `STATUS.md` now says so out loud; it did not before, and the pair
`79/73` had to be re-derived to work out why.

**The warning.** `8c` set out to build the route its approved spec described and
found the spec's route claim was **false** — a §3a layer-3 route existed that the
spec had ruled out in writing, which changed the item from "a 14th exposed site
plus a sleeping game-time thread" to a 250-line wrapper with no persisted state.
Prompt 8 hit the mirror image the same week: a route recorded as *"verified
feasible"* that did not exist. **Both were caught only by re-deriving the route
from Src, not by re-checking the spec's citations.** D10 is a build with its own
recorded design; **re-derive its route before you write to it**, and treat any
sentence of the form *"the only way to do this is X"* as the least-verified
sentence on the page.

⛔ **The sealed document was NOT read, grepped, or surfaced at any point in
prompt 8c.**

### One 30-second check owed to 8c, and it rides your leg for free

**`Fix_DustDevilSpawnGate` carries ONE change that PT-61 did not run.** After the
leg passed, the owner asked whether `DustDevils_VeryLow` also produces zero under
the fix; it does, because that preset ships `forbidden = true` and the scheduler
returns at `DustDevils.lua:194-196` before its wave loop. A `forbidden`
early-return was added to the module (and a matching passthrough assertion to the
probe) so we do not gate a system that is already switched off, or burn a
`SessionRandom` draw on a map where the fix does nothing.

**It is behaviour-neutral by construction** — the only branch it changes is one
where the thread exits immediately either way — **but that is reasoning, not a
measurement.** When you run `*r SMRTest.RunAll()` for your own leg, confirm
**`DustDevilSpawnGate` still PASSes** and say so. Probe count is unchanged at
**86** (an assertion was added to the existing probe, not a new probe).

⚠️ Two console facts PT-61 learned the hard way, both now in `PLAYTEST_HELP.md`
but worth knowing before you write a snippet: **`rawget` and `_G` are blacklisted
in the console** (a check inherited from a handover could never have executed and
nobody had run it), and **`ConsolePrint` takes exactly one string argument** — a
multi-argument or numeric call prints nothing and reports no error.
