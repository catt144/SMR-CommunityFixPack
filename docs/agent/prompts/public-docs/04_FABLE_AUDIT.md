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

## ⭐ Job 1b — if prompt 3 handed off, the SEAM is your highest-yield target

⚠️ **Check first whether `03_BUILD_STORE_B.md` (or `_C`) ever existed** —
`git log --diff-filter=A -- 'docs/agent/prompts/public-docs/03*'`. The owner can
stop a session with the word `context` (`README.md`, chain rule 8), so this build
may have been written by two or three sessions in sequence.

**If it was, the handoff seam is where drift concentrates**, and the successor's
honesty is the thing to test:

* ⛔ **The successor was required to hand on STATE and POSITION, never FACTS.**
  Check its handoff note for counts, statuses or claims quoted as settled rather
  than pointed at. A fact handed on in prose is a fact that stopped being
  re-derived.
* ⛔ **Check the RE-DERIVE list was actually honoured**, not just received.
* ⭐ **Check the ledger survived the seam.** Every sweep finding handed on as
  un-adjudicated must have an adjudication now — or be handed on again, still
  marked. **A finding that quietly disappeared across a handoff is the single
  worst outcome this protocol can produce**, and it is invisible unless you go
  looking in the predecessor's note.
* **Check for the tidier story.** A session under context pressure has every
  incentive to describe itself as further along than it was.
* **Read across the seam for voice and terminology**, then apply Job 2 normally.

⇒ **If there was no handoff, say so and skip this job.** ⛔ Do not report it as
checked if you did not check whether one happened.

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

---

# Notes from upstream — prompt 3 (`03_BUILD_STORE.md`, consumed 2026-08-13)

**Both descriptions are written, swept by six subagents, arbitrated and
committed. Nothing was handed off; there was no seam** — so **job 1b does not
apply** and its budget goes to job 1.

## What is DONE — with the file and section to go and look at

| # | deliverable | where | commit |
|---|---|---|---|
| 1 | **Fix pack store description** | `agent/reports/STORE_FIXPACK.md` — player text between the two `PLAYER TEXT` rules; notes and the claim-trace table below them | `ed5724b`, arbitrated `6669b58` |
| 2 | **Opt-in store description** | `agent/reports/STORE_OPTIN.md`, same shape. ⛔ **Lives in this repo on purpose** — one voice, one audit target; **release prep copies the player text to `C:\Dev\SMR-OptInPack`** | `38239d8`, arbitrated `6669b58` |
| 3 | **`metadata.lua` strings ×2** | `agent/reports/STORE_METADATA_STRINGS.md` — **drafted, NOT applied.** `metadata.lua` is code and outside the chain's fence; routed to release prep, which opens that file anyway for the version bump and checklist 23 | `38239d8` |
| 4 | **The audit ledger** | `agent/reports/STORE_BUILD_AUDIT.md` — **this is your job 1 comparison target.** Per sweep: what was searched, what came back, a verdict on every finding, the negative half written out, and one section naming what the sweeps did **not** cover | `4543715` |

**Judgment calls (job 3 of my brief):** four of §9's five bullets ship verbatim
in `STORE_FIXPACK.md`. **The fifth is a one-line `⛔ HOLE`** — 22b was still
unstruck when I closed. The replacement bullet is written out in that file's
notes, ready to paste, in the approved *"on some map settings"* phrasing.

## What is NOT started, or deliberately not done

* ⛔ **`docs/agent/STATE.md` and `docs/PLAYTEST_CHECKLIST.md` were not written**,
  per my concurrency rules — the owner's combined sitting owns both. **What I owe
  them is in "For the checklist and STATE" below.** ⚠️ **Check whether the
  sitting has landed before you write either file.**
* **No site page, no fix list, no FAQ** — prompt 5's.
* **The modder-facing per-fix disable paragraph is not written as prose.** §9.1
  told me to rewrite it; `02_QA.md` §5 then ruled it belongs on the site, because
  it is useless without an identifier and rule 4 bars identifiers from player
  text. ⇒ **What shipped on the card is one identifier-free sentence** naming the
  companion-mod route, its limit, and the absence of any in-game switch. **The
  identifier-carrying instructions are prompt 5's to write on a modders page.**
* **`STORE_METADATA_STRINGS.md` went through sweep 6 only.** Its two
  `description` strings have **not** been through the rule-4, vocabulary,
  evidence, route or standalone sweeps. **Treat them as unaudited.**

## The sweep and arbitration ledger

Full record in `STORE_BUILD_AUDIT.md`. Headline: **six sweeps, 43 findings — 27
confirmed and fixed, 5 confirmed and deliberate, 8 refuted, 3 routed.** Nothing
is left un-adjudicated.

⭐ **The two that would have shipped a false instruction:**

1. **The drone-dial uninstall recipe was wrong** — I wrote *"set both dials to
   base, load once, then uninstall"*, and the missing step is **save**. Setting
   the dials to base strips the modifiers from the running colony only; the file
   on disk keeps the boost until a new save is written. The frozen file had it
   right and I broke it.
2. **"What it writes is inert without it"** covered the one item that is
   deliberately not inert — the restored bonus that IS the repair.

⛔ **One whole sweep verdict was overruled, and you should look at it hardest.**
The evidence sweep called four of the opt-in page's eight module blocks
*unearned* because their design entries read `built` / `speced` / `opt-in`. I
refused it: that is the fix pack's F-entry status vocabulary applied to the
opt-in mod's design entries, where the word tracks the playtest item rather than
whether the module ships. My reasoning and what the sweep missed are in the
ledger's last section. ⚠️ **If you disagree, four module blocks come out — the
behavioural corrections that came out of those same blocks stand either way.**

## ⛔ RE-DERIVE THIS — do not inherit any of it from me

* **Every count.** `--emit-counts` in **both** repos at your own moment. The
  suite number appears in the fix pack's player text and it moved twice inside
  this chain.
* **Checklist 22b's state.** If it came back while I was closing, the hole gets
  filled from that file's notes — and check the shipped wording against what the
  owner actually said, not against my draft.
* **Three facts I could only source-verify**, which the combined sitting may have
  since measured: hole 11 (does the list command put anything on screen — **no
  surface of mine says it does**), hole 4's play half (a toggle without a
  restart — **I state it plainly, sourced from all eight module headers**), and
  **D13's `tested`**, which is what lets the uninstall half stop being a shape.
* **The claim-trace tables at the bottom of both descriptions.** They are my
  claims about my own evidence, and the evidence sweep found real gaps in them.
* **The route facts.** All source-derived, none play-verified — including the
  restart claim, the Apply claim, and the controller equivalents for Ctrl+click.

## Job 3's landmine list — my answers, for you to check rather than trust

1. **`F76`** — neither block crossed over in any form. 2. **No exposed-set
count** anywhere, in any form. 3. **22b** — unstruck at my close, so **neither
wording shipped**; the bullet is a hole. 4. **The four known-false claims** — all
absent; no console veto, no dials in the fix pack, no override-table name, no
*Mod Options → Community Fix Pack* path in either player text. 5. **The trains
overstatement** — the clause is **cut**, not softened; the route sweep confirmed
the button's own rollover names Metals and Electronics. 6. **`ListFixes()`** — no
surface mentions it at all. 7. **The uninstall-cleanliness sentence** — not
placed. 8. **The rescue artifact** — not named, not linked; one marked hole.
9. **The display name** — used throughout, both files. 10. **Rule 4** — clean;
the modder paragraph is the identifier-free sentence described above.

## Open, and routed

* **Load order** (design hole 3) — still unmeasured. My companion-mod sentence
  states the condition and promises no method; if you can derive an answer, the
  sentence can get shorter.
* **Store and site links** — three marked holes in the fix pack text, two in the
  opt-in. They exist when the owner uploads and turns Pages on.
* **The `%AppData%` path under the Microsoft Store's redirection** — neither the
  sweep nor I could verify it. Hedged to "usually in", which costs nothing.
* **Steam Deck** — the bug reporter is gated off there
  (`IsBugReporterEnabled()`); the copy now says so. Worth a second pair of eyes,
  because it is the kind of clause that reads as a defect if it is wrong.

## For the checklist and STATE — mine to hand over, not to write

⛔ **I did not touch either file.** Whoever writes them next lands these:

* **`PLAYTEST_CHECKLIST.md`** — nothing new is owed by the owner from my
  session. **22b is still the only open ask**, and its recommendation is
  unchanged: go back to *"on some map settings"*. ⭐ **Say the word and one line
  gets struck and one bullet pasted.** (22c — the hostile-reader page — is still
  open and is prompt 5's if the owner says yes.)
* **`STATE.md` ⑤** — the public-docs chain's line should read: descriptions
  **BUILT + swept + arbitrated 2026-08-13** (`reports/STORE_FIXPACK.md`,
  `STORE_OPTIN.md`, ledger `STORE_BUILD_AUDIT.md`, strings routed in
  `STORE_METADATA_STRINGS.md`); **next `04_FABLE_AUDIT.md`**; ③ is now assembly.
  ⛔ **Re-derive the wording and the counts before landing it**, and mind the
  60/60 line cap.
