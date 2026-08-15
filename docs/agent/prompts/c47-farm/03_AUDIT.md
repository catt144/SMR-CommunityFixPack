# C47 + C48 — terminal audit (backward QA of the whole chain)

**Authored 2026-08-15** alongside `01_BUILD_AND_MEASURE.md`, when this folder
held one measurement leg. ⚠️ **RESCOPED AND RENUMBERED 2026-08-15 (owner asked
the right question): the chain grew to three legs plus an attended sitting, so
this audit now runs LAST — after `02_C48_VEGETATION_SUPPLY.md`, not before it.**
It was numbered `02` and would have deleted the folder including the C48 prompt
and its built instrument.

Fresh session, and ⛔ **read the prompts LAST, not first** — the point of this
pass is to re-derive the results from the artefacts, then check what the briefs
asked for. Reading a brief first trains you into its assumptions.

⭐ **Create a live todo list first** and keep it current.
**Start with `git log --oneline -10` + `git pull` in all four repos.**
⛔ **This prompt deletes ITSELF and the whole `c47-farm/` folder at close-out** —
so run it only when `02_C48_VEGETATION_SUPPLY.md` has been consumed and deleted.
If that file is still present, **you are early: stop and say so.**

---

## What this audit now covers — four bodies of work, not one

| # | what | evidence |
|---|---|---|
| 1 | the **unattended C47 leg** (4 suite launches + 3 sampler launches) | `archive/c47suite1..4_*`, `archive/c47samp1..3_*` |
| 2 | the **attended sitting** on the owner's live `C47FARM` | `archive/c47ride_Mars.exe-20260815-18.38.23.log` |
| 3 | the **C48 vegetation-supply leg incl. the owner's speed ladder** | whatever `02_*` archived; find it by name |
| 4 | the permanent probe `Code/61_Probes_Wave11.lua` in the TestKit | suite logs |

⭐⭐ **The single most important thing to attack: the C47 leg CORRECTED ITSELF
FOUR TIMES, and three of those corrections came from the owner rather than from
the agent.** One is a **reversed verdict** — P1 was recorded FAILED ("the buffer
never reached 0") and later reversed to HELD on the argument that
`reason=Consumption` fires only when `CanConsume()` is false, i.e. stored == 0
(`Building.lua:611-613`, `HasConsumption.lua:366-368`). **Re-derive that
implication yourself at Src.** If it is wrong, a headline verdict is wrong in
the record. If it is right, then the agent's *original* method — reading a
sampled minimum as a true minimum — is a harness defect worth generalising into
`agent/facts/`, and it is not currently filed as one.

---

## The order

1. **`docs/agent/bugs/C47.md`** — the entry, whole, including the new dated
   section. This is the claim under audit.
2. **The archived log(s)** in `docs/archive/`. ⭐ **Re-count every number
   yourself from the verdict lines. Never inherit a tally**, including from the
   entry you just read — the recorded-facts-are-claims-too rule applies to our
   own записи. Byte-verify the archived log against what the leg says it archived.
3. **The probe and sampler source**, as committed. Does the instrument actually
   measure what the entry says it measured?
4. **`ModTools\Src`** — re-derive the route independently: the two template
   fields, the tick derivation, `iterations = 3 + Random(3)`, the
   `OnMsg.AddNotificationObject` path, and the `VoicePerObject` / `VoiceCooldown`
   preset values. ⭐ **Do this from the source tree, not from the entry's
   citations** — the entry's line numbers are claims.
5. **Only now**, prompt 01.

---

## What to attack hardest

* ⭐⭐ **The control.** If the `ForestationPlant` control was not sampled — no
  Forestation Plant in the colony, or it was never counted — then the leg's
  headline comparison is **unsupported by measurement** no matter how good the
  source ratio is, and the entry must say `UNSAMPLED` rather than implying a
  contrast. This is the single most likely way this leg goes wrong, and it is
  the same failure the C39 bracket hit (1 of 8 families sampled).
  ℹ️ *(It was sampled — 36 of them. Verify that yourself; do not take this line
  as the finding.)*
* ⭐ **The withdrawn internal control.** The C47 leg first claimed the two Open
  Farms were a clean A/B differing only in crop mix, then **withdrew it** when
  the owner pointed out they sit in different vegetation densities with different
  drone-extender coverage — and the leg's own numbers already contradicted it
  (the farms **spent** 9,425 vs 9,520 and differed in **receipt**, 7,320 vs
  8,361). ⛔ **Check that no surviving sentence anywhere still leans on the
  withdrawn version** — entry, checklist, STATE, or the C48 prompt.
* ⭐ **Owner credit.** Five findings in this chain are the owner's, not the
  agent's: the construction refutation, the vegetation seed-offer mechanism, the
  density/drone-coverage explanation, the speed hypothesis **and its ladder
  design**, and the D02 coverage boundary. Verify each is attributed by name
  where it is recorded. An agent quietly absorbing a user's finding is a defect
  in the record.
* ⭐ **The speed ladder's fairness.** Its rungs are equal in **game** time, not
  real time, because the day-385 freeze caps the whole budget at ~16 game hours.
  Check the report read the **per-game-hour** columns and not raw counts, and
  that any rung with `took=false` was treated as VOID and any unreached rung as
  UNSAMPLED rather than zero.
* ⭐ **D02.** The chain claims `Opt_AcknowledgedWarnings` cannot suppress a
  flapping building because recovery clears the stamp
  (`Opt_AcknowledgedWarnings.lua:124-129`). Re-derive it, and check the claim is
  recorded in **both** places it needs to be — `C47`'s repair-shape list and the
  opt-in pack's own `D02` entry.
* **Predictions written first?** Check the commit order in `git log`, not the
  file's own claim about itself. A prediction committed after the run is not a
  prediction.
* **The voice arithmetic.** The leg applies the 60 s per-object cooldown itself.
  Re-derive it: is the cooldown real time or game time, and did the leg use the
  right clock? Getting this backwards would inflate or deflate the headline.
* **Scope creep into a fix.** Prompt 01 forbids building one. If code appeared,
  that is a finding.
* **Screen claims.** Grep the entry and any other surface for language implying
  a player saw or heard something. The boundary is absolute.
* ⚠️ **The confound sentence.** Cheats-enabled and an oversized speed-run colony
  must sit beside any rate. If a rate travels without it, fix it.

---

## Then

* Sustain or overturn each verdict **in writing, per verdict**.
* Apply corrections agent-side where they are yours to make; ⛔ **route anything
  that is the owner's to `docs/PLAYTEST_CHECKLIST.md`** with a recommendation,
  never only to an agent doc.
* Re-emit every count with `python tools/doccheck.py --emit-counts`.
* Update `STATE.md` to the post-audit truth.
* `doccheck` GREEN, commit, push, then **delete `docs/agent/prompts/c47-farm/`
  entirely**.
