# Chain 8b — the seven approved fixes, their probes, and the ONE batch leg

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

**Staleness check: `git log --oneline -12` + `git pull`.** This prompt was
written at **`8f58f30`** (chain prompt 8's last commit). Gate: prompt 8's
conversions are landed and committed — verify that before building, because this
prompt's leg covers them too.

## Where prompt 8 got to (state you inherit, not a summary to re-derive)

Prompt 8 **split under chain rule 3** after finishing every conversion in the
batch. It built **nothing** from the approved-fix list below.

**Landed (all pushed):**

| commit | what |
|---|---|
| `69c02b9` | `Fix_SmallLandscapeSites` → §1.4 pre-wrapper, **zero copied logic** |
| `26f0b57` | `Fix_NightShiftWork` → §1.4 post-wrapper (shift 1/2 now identical *by construction*) |
| `ab7d432` | `Fix_GeneForging` → §1.4b additive post-wrapper, installed via `SetGlobal` |
| `388c72a` | `Fix_ShuttleHubOffAvailable` → §1.4b post-wrapper as a **filter** |
| `21990fb` | `Fix_UpgradeModifierLeak` → §1.4 post-wrapper (`orig` is a proven no-op) |
| `10cd2b4` | ⛔ `Fix_TrainCargoDumping` **NOT converted** — stop condition fired; recorded + routed to prompt 12 |
| `1471533` | **Package 0**: F29 items 1 + 3 → post- and pre-wrapper (one module, one commit) |
| `8f58f30` | **Package 0**: F57(a) → pre-wrapper; `SMRFixPack_rocket_fuel_key` deleted, incl. from existing saves |

**Three things from that work you must not re-litigate or re-discover:**

1. ⛔ **`Fix_TrainCargoDumping` stays a §1.5 replacement and is OUT OF SCOPE
   here.** §5.4's "verified feasible" route does not exist: `GetTargetAmount` is
   a **native** method on the `TaskRequest` metatable, published as a savegame
   **permanent** through the mod-blacklisted `PersistGatherPermanents` hook,
   across 148 call sites with no key. Full reasoning on BUGS **F46**; §5.4's
   group counts are corrected to **5 / 4 / 10 / 3**; a second opinion on the skip
   is owed by **prompt 12**, not by you. **Do not try to build it.**
2. **The pack now holds ZERO R3 §1.5 replacements.** That is what package 0 was
   for, and STATUS/FIX_POLICY §4's amended R3 line now hold by construction. If
   anything you build here would create a new one, stop and re-read §4.
3. **No counts moved.** Prompt 8 filed and closed nothing: **108 rows = 96 F +
   12 D; 38 C**. Recount, do not inherit — see the housekeeping note at the end.

## Jobs (todo list first; ONE ITEM PER FIX AND ONE PER PROBE — the Phase-4
lesson about coarse lists is on WORKFLOW element 1; never bundle the batch
behind one checkbox)

1. **Every fix prompt 7 approved**, built exactly to the spec written on its
   BUGS entry, **one todo item and one commit each**. The seven are tabled
   below. **Read the entry, not the table** — each carries module, technique,
   code sketch, self-check, probe outline and intent statement in full.
   Includes the **F44 shell amendment (F91)** — that one touches
   `Fix_TrackSalvageWipe`, a `tested` module, so **its A/B expectations must be
   written down BEFORE the leg**.
2. **Probes** for every new fix (TestKit; explicit `return "PASS", …` — the
   fall-off-the-end trap is documented). Seven outlines are already written on
   the entries; several are static invariants needing no scripted repro.
   Probe-count changes land in STATUS.
3. **ONE leg for the whole batch — and the batch is prompt 8's conversions PLUS
   your seven fixes.** Stale-probe gate first; write the predicted numbers down
   before launching. Counts WILL move (new modules), so predict them.
   ⚠️ **The eight conversions are unrun.** They are technique-only and each
   carries a written byte-equivalence argument, but nothing has executed them in
   a game. Your predictions must cover them: every converted module reports
   `active` in `ListFixes()`, and no line in the log names one.
4. STATUS.md: new counts, batch results, and the chain's remaining tail.

## Scope fence

**In:** the seven approved fixes, their probes, the leg covering them and
prompt 8's conversions, STATUS.
**Out:** **C23 item 1** (→ `8c`, its own prompt — do not fold it into this
leg); `Fix_TrainCargoDumping` (above); anything prompt 7 did not approve; the
four design-pass modules §5.4 marks B-class; D10/D12 (prompts 9/10); layer 1 (⛔).

## Stop conditions

- The leg fails prediction → stop, report; the chain waits.
- A spec on an entry turns out not to match Src when you re-verify it → **do not
  improvise a different fix.** Record the divergence and route it; prompt 8
  already found one "verified feasible" claim that was not (F46).
- Context pressure → self-split (`8d_…_opus.md`) — seven fixes plus seven probes
  plus a leg is a lot; splitting EARLY beats splitting late.

## What may not be claimed

No new fix may be called `fixed` without its probe existing and the leg passing.
**No converted module may be called verified without the leg** — prompt 8's
equivalence arguments are arguments, not observations. Counts are claims —
recount, don't increment. Every result commit carries its `PROBE SWEEP:` line.

## On completion

Outbox → `9_d10_workshops_build_opus.md` (state + new counts), and anything C23
touches → `8c`. Delete this file, commit, push.

## Notes from upstream

### From prompt 7 (2026-08-02) via prompt 8 — SEVEN builds approved, each specced on its BUGS entry

**Nothing was built. Every spec below is written out in full on its own BUGS
entry — module, technique, code sketch, self-check, probe outline, intent
statement — so this prompt should not need to re-derive any of it. Read the
entry, not this summary.**

⚠️ **Do not treat any of these as a `wontfix` you may skip, and do not add to
the list.** Six candidates were run through §4 and closed the other way — they
are recorded on their entries with grounds and are **out of scope here**.

#### The approved builds — one todo item each

| # | fix | technique | lands in | note |
|---|---|---|---|---|
| 1 | **F91** track-shell leak | 3 lines inside an existing §1.5 body + the existing LoadGame sweep | **`Fix_TrackSalvageWipe.lua`** (F44) | ⚠️ **`tested` module** — state A/B expectations BEFORE the leg |
| 2 | **F92** Saint blessing | **§1.1** preset patch + one-shot load-time re-base | new module | changes real gameplay (Saints finally buff Religious colonists) — say so in the commit |
| 3 | **F93** dust-devil descriptor map | **§1.4b** global replacement, 7 lines, `CurrentMap` → `MainMap` | new module | header must name file/lines/build per §1.5 rules |
| 4 | **F94** asteroid-visit precedence | **§1.4b** global replacement, 12 lines, one pair of brackets | **`Fix_AsteroidLanderAvailable.lua`** (F72) | ⚠️ **the F72 header must be corrected in the same commit** — it advertises a chained delegation this fix removes, and the reason is on the F94 entry |
| 5 | **F95** Astrogeologist extractors | **§1.1** two additive `Effect_ModifyLabel` entries + load-time heal | new module | ⛔ build them with `PlaceObj`, **never** `:new{}` (the F87 rule) |
| 6 | **F96** sinkhole indestructible | **§1.1** one boolean on preset **and** class table | new module | side effects enumerated on the entry: exactly one behaviour changes |
| 7 | **F90** underground grid breaks | **§1.4 wrapper = §3a LAYER 3** (narrow the input, keep vanilla's body) | new module | ⚠️ `pcall` + restore + re-raise: `self.connectors` is a **persisted** field and must never be left swapped |

**Three of the seven are §1.1 preset patches and one is layer 3, so most of this
batch adds nothing to the save.** Only F91 and F94 touch modules that already
exist.

#### Three things that will bite this prompt if it is not expecting them

- **F94 removes a compatibility property F72's header brags about.** A false
  positive cannot be filtered by a post-wrapper — the wrapper sees `true` and
  never learns which rocket produced it — so the predicate has to be owned.
  Fix the header; do not quietly leave it claiming the old behaviour.
  ⭐ **Prompt 8 hit the identical shape in `Fix_ShuttleHubOffAvailable` and the
  outcome is worth carrying over:** the conversion was still worth doing, but the
  loop ended up *duplicated rather than eliminated*, and both the header and the
  entry now say so plainly. Do the same here — record what the technique does
  **not** buy, in the same breath as what it does.
- **F91's amendment sits on the `mass_delete` branch our F44 deliberately
  kept.** What mass salvage *removes* does not change; what changes is that the
  `TrackBase` is actually deleted afterwards instead of being left as a shell.
  The A/B must not read that as a behaviour regression.
- **F92 and F95 both need a load-time heal for existing saves**, because both
  repair something applied once (a trait on dome entry / a profile effect at
  game start). Both heals are specified as idempotent and both reuse vanilla's
  own application path rather than hand-rolling a modifier — keep that, it is
  what makes them safe to re-run on every load.
  ⭐ **And one more heal you were not told about, from prompt 8:** a spec that
  says "the new shape needs no persisted field" does **not** by itself remove
  that field from saves already written by the old shape. F57(a)'s conversion had
  to clear `SMRFixPack_rocket_fuel_key` explicitly to make its own entry's claim
  true. **If any of your seven changes what a module persists, ask the same
  question about existing saves.**

#### Probe outlines are on the entries

Seven probe outlines are written (`TrackShellLeak`, `SaintBlessing`,
`DustDevilsDescrMap`, `AsteroidVisitPrecedence`, `AstrogeologistExtractors`,
`SinkholeIndestructible`, `DustStormBreakMapFilter`). Several are **static
invariants** needing no scripted repro — cheap probe-count growth. Two have live
halves that belong on the checklist rather than in a probe, and the entries say
which.

#### Not for you

- **C23 item 1** — approved provisionally by the owner and **split to `8c`**.
  Do not build it, and do not let it into this leg.
- **F82 is CLOSED `wontfix — intent`** — a timed *event announcement*, not a
  state warning. Do not build a removal-key fix for it.
- **C23 item 3** (marker dust devils ignoring `DustStormsDisabled`) — defect
  confirmed, **declined on shape**; all four routes over-reach into scripted
  content or put a sleeping mod thread in every save. F89's disposition.
- **F04's tier** was decided (the witness is unassigned, not C32's). Record
  correction only; no code.
- **`Fix_TrainCargoDumping`** — see the state block at the top.

#### Housekeeping this prompt inherits

**STATUS's count line is re-derived, not incremented** (`Select-String` over the
index block). If this batch files or closes anything, re-derive it the same way —
the line has now gone stale four separate times and it is the single most
drift-prone number in the project.

⛔ **The sealed document was NOT read, grepped, or surfaced at any point in
prompt 8** — no broad search touched it.
