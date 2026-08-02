# Chain 8 — F86 Phase 4: the conversion batch + every approved audit fix, one leg

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

**Staleness check: `git log --oneline -10` + `git pull`.** Gates: prompt 5's
Tier-2 leg verified (D10/D12 unhold recorded) and prompt 7's outbox below
states which fixes were approved. Authority for the conversions:
`docs/reports/SAVE_SAFETY_REDESIGN.md` §5.4 (the six A-class chained-wrapper
conversions).

## Jobs (todo list first; ONE ITEM PER MODULE — the Phase-4 lesson about
coarse lists is on WORKFLOW element 1; never bundle the batch behind one
checkbox)

1. **The six §5.4-A wrapper conversions**, one module per todo item, each
   parse-swept and committed separately. These are safety-shape conversions
   (full replacement → chained wrapper); behavior must be byte-equivalent —
   say so in each commit.
2. **Every fix prompt 7 approved**, built exactly to the spec written on its
   BUGS entry, one item each, incl. (if approved) the **F44 shell amendment**
   (C33) — that one touches `Fix_TrackSalvageWipe`, a `tested` module, so
   its A/B expectations must be stated BEFORE the leg.
3. **Probes** for every new fix (TestKit; explicit `return "PASS", …` — the
   fall-off-the-end trap is documented); probe-count changes land in STATUS.
4. **ONE leg for the whole batch** (stale-probe gate first; write the
   predicted numbers down before launching; counts WILL move if prompt 7
   approved new modules — predict them).
5. STATUS.md: new counts, batch results, and the chain's remaining tail.

## Scope fence

**In:** the six conversions, the approved fixes, their probes, the leg.
**Out:** anything prompt 7 did not approve; the four design-pass modules
§5.4 marks B-class (they stay as-is unless a later owner decision); D10/D12
(prompts 9/10); layer 1 (⛔).

## Stop conditions

- A conversion is NOT byte-equivalent in behavior when you diff carefully →
  it is a B-class in disguise; skip it, record why, route to prompt 12.
- The leg fails prediction → stop, report; the chain waits.
- Context pressure → self-split (`8b_…_opus.md`) — with this many modules,
  splitting EARLY beats splitting late.

## What may not be claimed

"Converted" requires the before/after diff summary in the commit message.
No new fix may be called `fixed` without its probe existing and the leg
passing. Counts are claims — recount, don't increment.

## On completion

Outbox → `9_d10_workshops_build_opus.md` (state + new counts). Delete this
file, commit, push.

## Notes from upstream

### From prompt 7 (2026-08-02) — SEVEN builds approved, each specced on its BUGS entry; TWO owner decisions are open

**Nothing was built. Every spec below is written out in full on its own BUGS
entry — module, technique, code sketch, self-check, probe outline, intent
statement — so this prompt should not need to re-derive any of it. Read the
entry, not this summary.** Counts re-derived by counting, not incrementing:
**96 F + 12 D = 108 rows; 38 C.**

⚠️ **Do not treat any of these as a `wontfix` you may skip, and do not add to
the list.** Six candidates were run through §4 and closed the other way — they
are recorded on their entries with grounds and are **out of scope here**.

#### The approved builds — one todo item each

| # | fix | technique | lands in | note |
|---|---|---|---|---|
| 1 | **F91** track-shell leak | 3 lines inside an existing §1.5 body + the existing LoadGame sweep | **`Fix_TrackSalvageWipe.lua`** (F44) | ⚠️ **`tested` module** — job 2's rule applies: state A/B expectations BEFORE the leg |
| 2 | **F92** Saint blessing | **§1.1** preset patch + one-shot load-time re-base | new module | changes real gameplay (Saints finally buff Religious colonists) — say so in the commit |
| 3 | **F93** dust-devil descriptor map | **§1.4b** global replacement, 7 lines, `CurrentMap` → `MainMap` | new module | header must name file/lines/build per §1.5 rules |
| 4 | **F94** asteroid-visit precedence | **§1.4b** global replacement, 12 lines, one pair of brackets | **`Fix_AsteroidLanderAvailable.lua`** (F72) | ⚠️ **the F72 header must be corrected in the same commit** — it advertises a chained delegation this fix removes, and the reason is on the F94 entry |
| 5 | **F95** Astrogeologist extractors | **§1.1** two additive `Effect_ModifyLabel` entries + load-time heal | new module | ⛔ build them with `PlaceObj`, **never** `:new{}` (the F87 rule) |
| 6 | **F96** sinkhole indestructible | **§1.1** one boolean on preset **and** class table | new module | side effects enumerated on the entry: exactly one behaviour changes |
| 7 | **F90** underground grid breaks | **§1.4 wrapper = §3a LAYER 3** (narrow the input, keep vanilla's body) | new module | ⚠️ `pcall` + restore + re-raise: `self.connectors` is a **persisted** field and must never be left swapped |

**Three of the seven are §1.1 preset patches and one is layer 3, so most of this
batch adds nothing to the save.** Only F91 and F94 touch modules that already
exist.

#### ✅ PACKAGE 0 — DECIDED BY THE OWNER 2026-08-02: **CONVERT. These are builds, not questions.**

**Three conversions join this batch**, each specced with its wrapper written out
on its entry: **F29 item 1** (post-wrapper: call `orig`, re-derive `count`,
truncate — `GetObjectsByLabel` returns `table.icopy`, so the list is safe to
mutate), **F29 item 3** (pre-wrapper, **zero copied lines**: order the two
fields before `return orig(self)` and vanilla's broken swap becomes
unreachable), **F57(a)** (pre-wrapper: clear the whole restrictor table before
`return orig(self)` — that table has exactly one writer in the tree, and this
**deletes `SMRFixPack_rocket_fuel_key` from the module and from every future
save**). All three are layer-2-shaped. **After this batch the pack holds ZERO
R3 §1.5 replacements**, which is what the §4 amendment was asking for. The
defect claims are untouched — technique only, so the A/B must read
byte-equivalent behaviour on all three.

#### ⚠️ C23 ITEM 1 — APPROVED **PROVISIONALLY** BY THE OWNER, AND IT IS THE ONE ITEM IN THIS BATCH THAT CAN BREAK A SAVE IF RUSHED

**Owner, 2026-08-02: "build it, accept the thread — for now, but it's not
locked. I want the QA run to personally review it and provide feedback."** So it
is a build, chain prompt 12 has a standing job to re-examine the decision, and
**the owner may reverse it** — do not treat it as settled precedent for anything
else.

⚠️ **Read the C23 entry's build spec in full before starting. This is NOT the
small fix an earlier draft of these notes described** — that description was
corrected the same day. The defective line is **inside the
`GlobalGameTimeThread("DustDevils", …)` body**, so the fix means owning a
**sleeping game-time thread**, i.e. a 14th §3a exposed site, on a **P3** item.
Three edges, two of which have already bitten this project:
1. **The F88 trap** — `RestartGlobalGameTimeThread` re-rolls the pending wave
   timer, so installing on every load recreates F88 exactly. Use F88's
   **version-latched one-shot**; a table swap alone does not reach an existing
   save.
2. **The `Fix_MeteorFrequency` uninstall trap** — a bare
   `if not SMRFixPack then return end` leaves the save with **no dust-devil
   scheduler at all, forever**. The gate must **hand the loop back to vanilla**
   (Tier 1's shape).
3. **Own A/B + long soak + a recorded per-site disposition** in
   `SAVE_SAFETY_REDESIGN.md`.

**⛔ Scale call is yours: this is Tier-1-scale work on a P3 item.** If it does
not fit alongside the six conversions and the other approved fixes, **chain
rule 3 (self-split) applies** — split it out rather than rushing it into the
shared leg. Verification rider is written on the entry (`VeryHigh_3`: 3-4 per
wave before, 0-or-6-8 after, dust storms off).

#### Background — why it was approved, in one paragraph

1. **C23 item 1 — the dust-devil `spawn_chance` truncation.** Defect confirmed
   and sharpened (`count_max` unreachable whenever `spawn_chance < 100`; the
   count can be 0 while `count_min` is 1). **Not approved**, because the repair
   changes the dust-devil RATE and two readings are live — §4's ambiguity rule
   points at the sibling Bernoulli gate, §4's "no balance changes" line points
   at leaving a difficulty number alone. ⛔ **The "§1.4b replacement of the count
   line" this line originally promised DOES NOT EXIST** — corrected above and on
   the entry; the line is inside a thread body.
   ⭐ **Updated the same day: the SHAPE question is now answered by a second
   control in another file.** `MapSettings_Meteor` declares the same trio with
   an identical idiom (`multispawn_chance` 30/1/100) and uses it **gate-then-
   count**: the chance decides *whether* (`Meteors.lua:284-290`), the count is
   drawn independently and never multiplied (`:137`). Two controls for
   gate-then-count, zero for chance-as-multiplier anywhere in `Lua\`. ⚠️ **The
   RATE question is still open** — and `DustDevils_Low` accidentally
   approximates the gate today (50% × count 1..2 truncates to 0-or-1), so the
   shipped rates may have been tuned around the bug. That is what the owner is
   deciding, not the shape.

#### Three things that will bite this prompt if it is not expecting them

- **F94 removes a compatibility property F72's header brags about.** A false
  positive cannot be filtered by a post-wrapper — the wrapper sees `true` and
  never learns which rocket produced it — so the predicate has to be owned.
  Fix the header; do not quietly leave it claiming the old behaviour.
- **F91's amendment sits on the `mass_delete` branch our F44 deliberately
  kept.** What mass salvage *removes* does not change; what changes is that the
  `TrackBase` is actually deleted afterwards instead of being left as a shell.
  The A/B must not read that as a behaviour regression.
- **F92 and F95 both need a load-time heal for existing saves**, because both
  repair something applied once (a trait on dome entry / a profile effect at
  game start). Both heals are specified as idempotent and both reuse vanilla's
  own application path rather than hand-rolling a modifier — keep that, it is
  what makes them safe to re-run on every load.

#### Probe outlines are on the entries

Seven probe outlines are written (`TrackShellLeak`, `SaintBlessing`,
`DustDevilsDescrMap`, `AsteroidVisitPrecedence`, `AstrogeologistExtractors`,
`SinkholeIndestructible`, `DustStormBreakMapFilter`). Several are **static
invariants** needing no scripted repro — cheap probe-count growth. Two have live
halves that belong on the checklist rather than in a probe, and the entries say
which.

#### Not for you

- **F82 is CLOSED `wontfix — intent`** — a timed *event announcement*, not a
  state warning. Do not build a removal-key fix for it.
- **C23 item 3** (marker dust devils ignoring `DustStormsDisabled`) — defect
  confirmed, **declined on shape**; all four routes over-reach into scripted
  content or put a sleeping mod thread in every save. F89's disposition.
- **F04's tier** was decided (the witness is unassigned, not C32's). Record
  correction only; no code.

#### Housekeeping this prompt inherits

**STATUS's count line was re-derived, not incremented** (`Select-String` over
the index block). If this batch files or closes anything, re-derive it the same
way — the line has now gone stale four separate times and it is the single most
drift-prone number in the project.

⛔ **The sealed document was NOT read, grepped, or surfaced at any point this
session** — no broad search touched it. The one place its contents were
referenced is the inheritance guard prompt 7 was handed about F29(a), which was
quoted *to* this session in its own brief and was **not** relied on: package 0's
provenance was re-derived from Src (four shipped Mystery 2 sites, zero presets
setting either sampling parameter).
