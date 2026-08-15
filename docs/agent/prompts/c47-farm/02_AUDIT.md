# C47 — terminal audit (backward QA of the measurement leg)

**Authored 2026-08-15** alongside `01_BUILD_AND_MEASURE.md`. Fresh session, and
⛔ **read prompt 01 LAST, not first** — the point of this pass is to re-derive
the result from the artefacts, then check what the brief asked for. Reading the
brief first trains you into its assumptions.

⭐ **Create a live todo list first** and keep it current.
**Start with `git log --oneline -10` + `git pull` in all four repos.**
⛔ **This prompt deletes ITSELF and the whole `c47-farm/` folder at close-out.**

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
