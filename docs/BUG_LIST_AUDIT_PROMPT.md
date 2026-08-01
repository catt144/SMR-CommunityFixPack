# One-off prompt — tier the bug list against external witnesses

**Paste into a fresh session. One-off: consumed when `docs\BUG_LIST_AUDIT.md`
is delivered.** Model-neutral. **Game-free — do not launch the game, do not
modify `Code\`, do not fix anything.**

---

You are auditing the **evidence behind** a bug list, not the code that fixes it.
Project: the Surviving Mars: Relaunched "Community Fix Pack"
(`C:\Dev\SMR-BugFixPack`, git). Start with `git log --oneline -10` + `git pull`.

## Why this exists

The list was built two ways: **from player reports** (both games) and **from our
own source sweeps**. Every entry we have ever retracted came from the *sweep*
half — F49(c) was intended behaviour, F24 unreachable, F28 zero callers,
F62/F63 carried-forward design, F42 broke no promise. **None was an arithmetic
error; all were failures of reachability or intent** — the two things source
reading cannot see and an external witness can.

**This audit is a differentiator, not a cull.** Nothing gets deleted because it
scores low. The output is a confidence tier plus the work each tier owes.

## The tiers

| tier | definition | what it owes |
|---|---|---|
| **GOLD** | Reported **in Relaunched** AND our sweep confirms **the same mechanism the report describes** | Diagnostic verification RETIRED — no attended keyboard sitting. **Implementation verification is still owed**: its probe + one A/B leg (~90 s unattended). |
| **SILVER** | **(a)** reported in the **original** game AND our sweep finds that mechanism **still present in Relaunched source**; **or (b)** reported in Relaunched but the sweep cannot confirm the mechanism (player-feel, UI, timing) | High confidence. **Full playtest still required.** |
| **BRONZE** | Sweep-only. **"Concerned", not "bad."** | A detailed finding report per entry → **owner review**. Sub-type it (below). |
| **HOLD** | No report found, **not** arithmetic, and the audit's own recheck lacks strong confidence | Owner review **plus** a written defence: what it does, why we need it, and an **exit condition**. |

**Sub-type every BRONZE** — this is where the retraction history lives:

- **B1 — arithmetic / data.** Deterministic, no judgement (integer division,
  thresholds, preset fields). Historically never wrong here. High confidence.
- **B2 — control flow / reachability.** Dead branch, unreachable guard, caller
  count. Source reading is *correct* and the verdict still fails, because "can
  execute" ≠ "a player gets there". **F24 and F28 died here.**
- **B3 — interface / affordance / intent.** What the player sees, what the game
  promises. **100% of our judgement retractions.** Never trust a sweep alone.

## Witnesses, ranked

1. **Relaunched player report** — strongest. Evidence of reachability *and*
   salience.
2. **Original-game report** — requires checking the mechanism still exists in
   Relaunched source; the remaster may have changed it.
3. **ChoGGi's independent fix** — promotes **BRONZE → SILVER, never to GOLD**.
   ⭐ **Stronger than a normal report IF** the defective code is confirmed
   **identical between the original and Relaunched** — then you have independent
   diagnosis, proof the remaster did not change it, and years of in-the-wild
   validation of the approach.
4. **Other established fix authors.** `LukeH` is credited in the release
   checklist — ⚠️ **for Martian Express, which is a CONTENT mod. Verify he has a
   fix corpus at all before seating him at ChoGGi's tier.** Do not guess at other
   author names; if you find candidates, list them for the owner rather than
   promoting on them.

## Sources — local first, so this ages into evidence

- **`docs\archive\RESEARCH.md`** — the report corpus the list was built from.
  **Start here**; it is reproducible from the repo.
- **ChoGGi's collection** — already cloned/subscribed locally (~471 mod folders,
  unpacked source). His fixes routinely capture or paste the vanilla body
  (**215 orig-capture references** counted in `docs\PRIOR_ART_SURVEY.md`), so
  **his source is frequently a partial mirror of the original game's code** —
  often enough to settle "does the defective code match?" with no extraction.
- **The open internet — WIDE PERMISSION, GRANTED BY THE OWNER.** Search and read
  **anywhere publicly available**: Steam Workshop pages, discussions and reviews;
  the Paradox forums and bug tracker; Reddit; GitHub; wikis; YouTube
  descriptions; changelogs; patch notes for **both** games. Go as wide as the
  question needs — this axis is the entire point of the audit and it cannot be
  answered from the repo. See the quoting rule below.
- **You may STOP AND ASK the owner to download things.** If a mod, collection or
  workshop item would settle entries and is not already local, **stop, name it
  and say what it would settle** — the owner will subscribe or clone it and hand
  it over. That is a supported outcome, not a failure. Better a pause than a
  guess. Same for a paywalled or login-only source: name it rather than working
  around it.
- **`Packs\Lua.hpk` extraction is a FALLBACK, not a prerequisite.** Use it only
  where ChoGGi's source does not carry enough of the original to compare, and
  **report which entries needed it** — if that list is short the dependency
  evaporates; if long, say so and the owner will decide whether to build the
  extractor once. Precedent: this project already extracted Relaunched's
  `Lua.fpk` (FLPK, zstd per file) for the 2,250/2,256 parity proof.

## Hard rules

1. **Verbatim quote, source, and which game — inline, per entry.** A paraphrase
   is not a witness. `BUGS.md` already carries "verified identical to the
   original game" on F62/F63 with nothing on disk that can re-derive it; do not
   add a second generation of that.
2. **A report only counts for GOLD if it describes the symptom OUR mechanism
   predicts.** A coincidental match creates a false GOLD, and GOLD is the tier
   nobody re-reads. Mismatch ⇒ SILVER at best.
3. **`NOT FOUND` is a prior, not a verdict.** Never auto-`wontfix`. Latent and
   invisible defects are unreported *by definition*.
4. **Flag `UNREPORTABLE BY CONSTRUCTION`** for latent-by-data entries — F27,
   F31, F43, F57(a) and any others you find. No player will ever report them,
   they will look exactly like HOLD candidates, and they are correct. **They are
   exempt from the no-report penalty and must not be sent to HOLD on absence of
   reports alone** (FIX_POLICY §4a: invisible and latent still ship if a player
   could be harmed later).
5. **`NO MECHANISM FOUND` is its own bucket, not SILVER(b).** Reported in
   Relaunched but the sweep found no mechanism = mod interaction,
   misattribution, or a real bug we have not located. **Potentially the most
   valuable cell in the audit** — report it prominently.
6. **Scope: sweep-derived entries only.** Report-derived entries are
   corroborated by construction. The OG-vs-Relaunched code comparison runs for
   **BRONZE and HOLD only** — GOLD and SILVER do not need it to ship, and
   running all ~66 through it turns a validation pass into a second project.
7. **Produce work items, not scores.** Every BRONZE and HOLD entry ends with a
   concrete next step: a named tell (FIX_POLICY §4 draft: player report, dead
   code, sibling contradiction, self-contradiction, dev comment), or a named
   keyboard observation.

## Read first

`docs\STATUS.md` · `docs\BUGS.md` (the index, then entries as needed) ·
`docs\FIX_POLICY.md` (**§4a**, and the **drafted §4 amendment** at the end of
`docs\REACHABILITY_AUDIT.md` — its "hard tells" are the vocabulary this audit
should use) · `docs\REACHABILITY_AUDIT.md` "Challenge review 2026-07-30" (why
source is near-mute on *wrongness*) · `docs\PRIOR_ART_SURVEY.md` ·
`docs\archive\RESEARCH.md`.

## Deliverable — `docs\BUG_LIST_AUDIT.md`, committed

1. **Verdict up front** — how many entries in each tier, and whether anything in
   the shipped default-on set lands in HOLD.
2. **The table** — every audited entry: id · provenance (report / sweep) ·
   tier · sub-type if BRONZE · witness quote + source + game · what it owes.
3. **HOLD list** — each with its written defence and exit condition.
4. **`NO MECHANISM FOUND`** — separately and prominently.
5. **⭐ Gaps in OUR list** — bugs ChoGGi (or another verified fix author) fixed
   that we do **not** have. This is the half only available because we built
   independently first, and it may be the most valuable output. **File findings
   as `BUGS.md` entries with evidence; do not fix them.**
6. **Extraction report** — which entries needed `Lua.hpk` and could not be
   settled from local sources.
7. **Method and its limits** — including anything you could not determine and
   why. `CANNOT DETERMINE` is a first-class result.

## Standing rules

- Update your todo list **as you go**, one item per verifiable unit — the owner
  reads it to decide when to step in.
- **Never modify the game directory.** Src and both game installs are read-only.
- Commit with
  `git -c user.name="SMR-BugFixPack" -c user.email="154917955+catt144@users.noreply.github.com"`,
  push, and use `git commit -F <file>` — **no embedded double quotes**
  (PowerShell 5.1 splits them).
- `docs\FUTURE_IDEAS.md` is a **parking lot, not a backlog** — nothing in it is
  owed, and defects never go there.
- **Do not build, fix or refactor.** If you find a new defect, file it with
  evidence and stop.
