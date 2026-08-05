# Chain prompt 1 — unattended prep for the first batched co-run sitting

**Read `README.md` in this folder first — binding chain rules apply.**
Unattended; the owner is NOT needed until prompt 2's sitting. Start with
`git log --oneline -10` + `git pull`. Todo list up front, per-item updates as
you go — the owner reads that list live.

**Read path**: this folder's README · `agent/WORKFLOW.md` "Co-runs" (the
guardrails + envelope + adopted tiers) · the entries each leg runs from
(`F48.md` 2026-08-03 procedure block · `F26.md` 2026-08-03 procedure block ·
`F22.md`/`F75.md` · `D07.md` incl. the 2026-08-01 method correction ·
`F21.md` · `C42.md` leg-F block · `F85.md` ·
`POPUP_CONSEQUENCE_AUDIT.md` §8 + §3.6) · `PLAYTEST_HELP.md` verified command
table + rig section · the unattended-1 record in `SESSION_LOG.md` (2026-08-04
close entry) for what the staged save is known to contain.

⚠️ **The routing-sweep warning binds you personally: every design below was
written assuming the owner drove everything. Your job is the re-derivation in
rig terms — from the ENTRY, against Src, never from the checklist alone.**

## Jobs

**Job 1 — stage and confirm the fixture, one unattended cycle.** Copy
`TEST2H TRAIN` → `CB1STAGE.savegame.sav` (game closed). One confirm cycle
(harness pattern: clone the parked unattended-1 `97_U1Common` shape from git
`a433e42` — say so in the header), all label reads, no mutations:

- pack count AS READ (expect 81/81) + `Opt_CohortHousing` status by name;
- **Last Transmission**: is it an active faction on this save? (Leg 3's gate.
  Read the faction/politics state; if absent, leg 3 is `SKIP <reason>` in the
  brief and stays routed.)
- **Seniors + normal residences + free cohort slots** (leg 4's fixture);
- tracks / stations / running trains (leg 1: ≥2 connected stations, ≥1 train
  with a route — co-run #1 saw 7 trains on this save's ancestor);
- passages with element counts (C42 ride-along);
- dust-defence presence (leg 2's interception check needs at least one
  defence tower or the interception read is UNSAMPLED — say which);
- a cheap choice popup available? (popup trio — a launch-issue prompt is the
  documented cheapest; name the route to one on this save.)

Every reading prints APPLICABLE per the condition-sampled rule. A failed
confirm = `SKIP` in the brief, never a re-choice of save.

**Job 2 — Src-verify the two `[NEVER RUN]` instruments before the sitting
leans on them** (README rule 10; unattended-1's I6 is why this is not
optional):

- `StartBombard` — signature, argument meaning, gating (`Platform.cheats`?),
  and whether the entry's literal recipe
  `StartBombard(UIColony:GetCityAtMap(MainMap), 40*guim, 8, 500, 1500)` can
  raise on this save's state. Read the function, not the comment about it.
- `ProcessTrackElements` — plain global or file-local? Callable from the
  console/mod env? What exactly does it do to `start_el`/`end_el`/`elements`,
  and is F48's "unable to find the expected number" assert non-fatal in
  retail? If either is unreachable, the leg's shape changes NOW, in prep —
  not mid-sitting.

**Job 3 — park the probe sources.** One shared harness + per-leg payloads as
`.lua.txt` beside this file (probe hygiene rule 5). ⛔ Guardrails, all five,
stated in each header: used-vs-defined resolution cross-check run and quoted;
every completion/verdict counter names its liveness witness; every `pcall`
result printed; no per-chain fact in a per-process flag; ARM GATE read-back
before every launch. The sitting's probes are mostly READERS (the owner's
eyes are the instrument for the Tier-A moments) — keep them so; a reader that
mutates is a design smell here.

**Job 4 — write the sitting brief INTO `02_OPUS_SITTING.md`'s "Notes from
upstream".** The brief is the product; it contains:

- **The measure-moments list** — for each moment: leg, what the owner does or
  looks at, the verdict words to say, tier tag (A / HANDS-ONLY / B / C), and
  the minutes estimate. Sum the minutes; if the total exceeds ~25, flag the
  overflow to the owner in the kickoff report rather than silently trimming
  legs.
- **Ordering** exactly per README (reads → PT-53 assign → PT-37 → PT-47 →
  popups → leg-5 fixture → PT-53 uninstall LAST).
- **Predictions per leg, numbered, written before anything runs** — from the
  entries, with each one's falsifier. A prediction that misses is a finding.
- **Per-leg run-conditions template** (map, speed, loads, pack count, FORCED/
  ORGANIC declaration) and the `SKIP` lines Job 1 produced.
- **The evidence-card skeletons** (Tier B items) so the sitting fills cards
  rather than composing them live.
- Watchdogs/outside bounds per launch, and the expected first-output time so
  a stall is recognizable in under a minute (unattended-1's I2: the owner
  beat the rig's bound to a stall — do not let that be necessary twice).

**Job 5 — close out.** Commit (probes parked, brief written, fixture staged
and CONFIRMED, this file consumed in the same commit); update the manifest
row; doccheck green; push. The chain then WAITS — prompt 2 runs only when
the owner sits down. Report to the owner: what is confirmed, what is
SKIP-and-why, the total attended-minutes ask, and the kickoff line for the
sitting.

## ⛔ What you may not claim

- Nothing is `tested` by prep. Nothing is "ready" beyond what the confirm
  cycle actually read.
- No owner-minutes total presented as a promise — it is an estimate against
  which prompt 3 audits the actuals.

## Notes from upstream

*(Appended by the authoring session, 2026-08-04.)* The staged save's known
contents (from unattended-1, all AS READ on a copy of the same source save):
81/81 active · 17 tracks / 926 elements / 896 break-candidates · 244 drones
(60–81 idle) / 15 hubs · 13 domes / 47 dome label modifiers · 4 passages /
50 elements / 0 unit entries post-load · commander = rocketscientist ·
FrictionlessComposites NOT researched · 0 Large Wind Turbines · 0 Medical
Centers · 2 ArtificialSuns / 4 SolarPanels · 0 biorobots. Unknowns Job 1
exists to settle: Last Transmission presence, Seniors/cohort slots, dust
defences, popup availability, running-train count on THIS copy.
