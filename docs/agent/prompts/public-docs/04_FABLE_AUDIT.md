# Chain prompt 4 — terminal audit of the store descriptions

**Read `README.md` first — binding chain rules apply.** Staleness check across
all repos, live todo list updated per item.

⭐ **You are a fresh-context adversarial auditor on a long, heavy build.**
Prompt 3 wrote two store descriptions, ran six parallel sweeps and arbitrated
their findings. **Your job is to establish whether that actually happened.**

⛔⛔ **THE GOVERNING RULE: EVERY "DONE" IS A CLAIM.** A sweep reported as *ran,
clean* is a claim. A finding recorded as *refuted* is a claim. A count quoted in
the finished copy is a claim. **None of them is evidence until you re-derive it.**

---

## ⭐ Why this audit exists, and what it is actually looking for

**Owner instruction 2026-08-13**, and the reasoning is the brief:

> *"Since anything that writes that much is going to be using loads of context
> and that's when things can get confusing."*

⚠️ **This is a different failure mode from the one prompt 3's own sweeps target**,
and you should not spend your session re-running them in the same shape. Prompt
3's sweeps hunt **claims that were never true**. You are hunting **work that
degraded across a long session** — a distinct list:

| # | context-pressure failure | how it shows |
|---|---|---|
| 1 | **Drift** | tier 0 written in hour 1 and tier 2 written in hour 5 no longer agree; a term is defined early and used differently late |
| 2 | ⛔ **Steps claimed, not taken** | a sweep reported clean that never really bit; an arbitration verdict with no re-derivation behind it |
| 3 | ⛔ **Facts re-used without re-derivation** | a count derived early and quoted late. ⚠️ **This project has already done exactly this** — the probe count moved 88 → 94 *within hours* of a table being written |
| 4 | **Instructions dropped late** | the constraints that live at the bottom of a long brief are the ones a tired session forgets |
| 5 | **Compaction damage** | if the session was summarised mid-flight, something established early is now remembered wrong |
| 6 | ⭐ **The arbiter collapsing into the author** | phase 3 required re-deriving every subagent finding. Under pressure that becomes rubber-stamping, and it leaves no trace — the verdicts look identical either way |

⭐ **Failure 6 is the one you are best placed to catch and nobody else can.**

---

## Job 1 — the control that tests prompt 3's own auditors

⛔ **Do this FIRST, before reading prompt 3's audit log**, so its findings cannot
anchor you.

**Independently re-run TWO of the six sweeps** against the finished descriptions —
**the evidence sweep and the route sweep**, because those are the two that find
real defects and the two that were flagged as most likely to return a confident
wrong answer:

* **Evidence** — every factual sentence traced to its `agent/bugs/` entry or
  `agent/facts/` fact. ⛔ The bar is `fixed` + suite + per-fix self-checks + the
  verified save-safety tier. Nothing more.
* **Route** — every *"you can X"* names its route, and a retail player on **PC,
  Xbox and PlayStation** can walk it.

**Then, and only then, open prompt 3's records and compare yields.**

| what you find | what it means |
|---|---|
| your yield ≈ theirs | ✅ the sweeps bit. Sample the other four and move on |
| **you find things they did not** | ⛔ **the sweep did not really run.** Re-run all six yourself and say so plainly |
| they found things you did not | ✅ good — verify a sample of those and credit them |

⚠️ **A sweep that reported nothing is the one to look at hardest.** Silence is not
the same as clean, and an empty report usually means the rule was mis-specified.

## Job 2 — drift across the session

* **Read tier 0, tier 1 and tier 2 against each other**, in both descriptions.
  ⛔ **The standalone test is the instrument:** *"if a reader stops here and acts,
  is anything they now believe false?"* Tier 2 may only ever **add** — if it
  changes the meaning of anything in tier 1, that is drift and it is the exact
  failure the tiering exists to prevent.
* **Read the two descriptions against each other.** They are separate products
  with a shared voice; check the shared claims (save safety, no balance change,
  neither mod needs the other) say the *same* thing in both, not merely a
  compatible thing.
* ⭐ **Check the earliest-written and latest-written material specifically.**
  `git log -p` the build commits in order — drift lives at the seams between
  sittings, and the commit sequence is where you can see them.

## Job 3 — the landmine list, checked one at a time

Each of these is a known, specific way this project has already been wrong.
⛔ **Check every one against the finished copy** — presence or absence, no
sampling:

1. ⛔ **`F76` quarantine.** Neither `[DRAFT NOTE]` block from
   `MOD_DESCRIPTION.md:225-249` crossed over **in any form** — not quoted, not
   paraphrased, not "rewritten in our own words". It describes a bug that does
   not exist and its prose flags nothing.
2. ⛔ **No exposed-set count**, in any form, anywhere, including the save-safety
   section. The player-facing artifact is the *enumerated footprint in player
   words* — a different thing from the derivation.
3. ⛔ **Checklist 22b.** The dust-devil bullet's scale word. **If 22b was not
   struck by the owner, NEITHER wording ships.** If it was, the shipped wording
   matches what the owner actually said.
4. ⛔ **The four known-false claims in the frozen file** are all corrected, and
   none was carried across by habit: the console veto · the drone dials' location
   (they moved to the opt-in mod; the fix pack has **no** Mod Options page) ·
   the `SMRFixPack_Optional` override table name (now `SMROptInPack_*`) · every
   *Mod Options → Community Fix Pack* path.
5. ⚠️ **The "never tells you about" overstatement** on replacement trains — the
   game does tell you, in a rollover on the button.
6. ⛔ **`ListFixes()` shows nothing on screen unless the capture sitting proved
   otherwise** (hole 11). No surface may say the console *shows* a list until
   that shot exists.
7. ⛔ **The uninstall-cleanliness sentence is not placed.** Reading A vs B is an
   owner call at launch.
8. ⛔ **The rescue artifact is not named and not linked.** "Build ≠ publish".
9. ✅ **The opt-in display name is "Community Fix Pack: Opt-In Modules"** — decided,
   swept, closed.
10. ⛔ **Rule 4** — no file path, function name, `F##`/`D##` id or house word in
    anything a player reads. ⚠️ Check the *modder* paragraph specifically: it
    needs an identifier to be useful, and the ruling was that it therefore
    belongs on the site rather than the store card.

## Job 4 — the counts, re-derived at YOUR moment

⛔ **Re-emit, do not read:** `python tools/doccheck.py --emit-counts` in both mod
repos. Then check **every number in the finished copy** against your own emission
— including any suite/probe number, which §4.5 says is re-derived at write time
and never copied. ⚠️ **It has already moved twice during this chain.**

## Job 5 — what prompt 3 left for prompt 5, and whether it is honest

* Read prompt 3's **Notes from upstream** — appended to the bottom of **THIS
  file**, which is prompt 3's outbox. Does it hand on every hole it actually
  left, or a tidier story than the work supports?
* ⛔ **A hole silently closed is worse than a hole left open.** If a hole is
  reported closed, verify the closure.
* ⭐ **Name anything prompt 3 was asked to do and did not** — including anything
  it dropped without saying so. A quiet omission at the end of a long session is
  the most likely single failure here.

---

## Verdict and close

* **First line: SUSTAINED or OVERTURNED**, per area, with what you re-derived.
  ⭐ **"Sustained" must name what you SAMPLED** — a sustain with no sample is the
  same rubber stamp you were sent to look for.
* ⭐ **Fix hygiene in place** (a stale banner, a wrong number, a contradicted
  heading). ⛔ **Route substance** — anything that changes a claim, a decision or
  an owner-approved sentence goes to `docs/PLAYTEST_CHECKLIST.md` and to your
  outbox, never quietly rewritten.
* Append **Notes from upstream** to `05_BUILD_SITE.md` (create it if prompt 3 did
  not — the manifest in `README.md` describes it).
* ⚠️ **If the combined sitting has landed by now**, three facts this chain holds
  as source-verified may have become measured — hole 11 (`ListFixes()` on
  screen), hole 4's play half (toggles without a restart) and D13's `tested`.
  **Check `STATE.md` and upgrade or downgrade the copy accordingly.**
* `python tools/doccheck.py` GREEN. Commit with `-F` (PowerShell 5.1 splits `-m`
  on embedded quotes), push, **delete this file in the same commit.**

## ⛔ What you may not do

- Rewrite the descriptions to your taste. **You are an auditor, not a third
  author** — attack the claims and the route, not the style.
- Re-open a decision the owner has already made.
- Publish anything, anywhere, or create an external account.
- Lift the `MOD_DESCRIPTION.md` freeze or overturn STATE's release sequencing.
- Write the fix list or any site page — that is prompt 5.
