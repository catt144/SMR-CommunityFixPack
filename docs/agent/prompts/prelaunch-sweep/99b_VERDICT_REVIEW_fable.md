# Verdict review — disbelieve the terminal audit, then rule

♻️ **SELF-CONSUMING.** Delete this file in your closing commit, naming its grave.
You are the **last** session of the pre-launch sweep chain.

**Owner design, 2026-08-19:** a second adversarial ruling on the terminal audit's
verdict, because one session deciding alone whether a mod ships is the shape this
project distrusts everywhere else.

⛔⛔ **YOU ARE NOT A SECOND AUDIT. DO NOT REDO THE WORK.** The terminal audit read
every link, verified every finding and swept a final lens. Re-running that would
cost a day and buy little. **Your job is narrow and adversarial: try to break its
VERDICT.**

⚖️ **Default to refusing.** If you cannot decide, the answer is *do not upload
yet* — a delayed launch costs a day, a bad one costs the mod's reputation on the
only first impression it gets.

---

## 0 · Read path

```
git log --oneline -25
git pull
python tools/doccheck.py --emit-counts
python tools/upload_preflight.py
```

`00_CHAIN_SPEC.md` (⭐ its **§2**, **§5** and **§6.5** amendments especially) ·
`SWEEP_LEDGER.md` · `SWEEP_FINDINGS.md` · the terminal audit's commit and report ·
every link's commit body · `reports/` artifacts · `RELEASE_PORTAL_PREP.md` ·
`docs/PLAYTEST_CHECKLIST.md` items 37 and 45.

⭐ **Read the audit's own verdict LAST**, after you have formed a view from the
evidence. Its reasoning is persuasive by construction — you are the control on it.

## 1 · 🗒 Live todo list — one item per challenge below

## 2 · The five challenges

### C1 · Is the convergence clause honest?

`00_CHAIN_SPEC.md` §5 has three clauses and ⛔ **only clause 1 means the mod is
clean.** Clause 3 is the cap — *"we stopped counting, not because there was
nothing left."*

⛔ **The spec names laundering a cap into a clean bill as the worst outcome this
design can produce.** Check the ledger yourself: does unswept territory of
consequence remain? If it does, **clause 1 is unavailable no matter how the audit
phrased it.**

### C2 · Does run B actually support the verdict?

⛔ **No run B ⇒ no upload verdict** (`99` §7). And B is not a formality:

- Was it run in the **real** player configuration — **packed**, junction pulled,
  TestKit **and** opt-in off?
- ⚠️ Did it budget the **owner Mod-Manager tick** the junction/account-state
  defect makes mandatory (`98` §4.1), and **read the gate line first**? A B run
  that reports the pack absent measured the procedure, not the mod.
- Were **all ten** pass criteria met, **by name**? Criterion 4 — the absence of an
  `update report:` line — is the falsifier for the whole 2026-08-17 false-alarm
  class.
- ⭐ **Did packed behave differently from unpacked anywhere?** That difference is
  the most valuable thing the rehearsal could produce; *"no difference"* asserted
  without a comparison is not an answer.

### C3 · Are the two core fixes verified, or merely not-falsified?

They are why the upload stopped. ⚠️ **The trap is documented and the chain already
fell in it once:** the verification launch was told to prove them with
`UpdateSuspects() == 0`, ran it, got `0` — and that result is **uninformative**,
because `UpdateSuspects` reads the mark only on `error`/`inactive` entries
(`00_Core.lua:527-536`), so a stale mark on an `active` entry is invisible to it.

⇒ **Demand the direct evidence:** `SMRFixPack.fixes.SaintBlessing.update_suspect`
read as `nil`, and an `order` duplicate check **after a real second Lua load**.
⛔ A green suite is not evidence for either.

### C4 · Did the audit itself overstate?

Run `99` §8's forbidden-claims list against what the audit actually wrote:
*"the mod is clean"* · convergence on a cap · *"ready to upload"* without B ·
unmeasured counts · player-route claims not walked · **"compatible with other
mods"** when run A tested exactly one other mod, ours, switched off · bare
`tested` · blanket verification without provenance per row.

⭐ **And the subtler one: did it inherit rather than re-derive?** The audit was
told *recorded facts are claims too*. Spot-check two of its verifications by
walking the route yourself. If it cited where it should have derived, say so.

### C5 · What did the whole chain never ask?

⛔ **This is the question with the best track record in this project.** Both
2026-08-17 defects, and every under-count in its history, came from *the brief
never asked* — not from anyone doing their brief badly.

Eight lenses plus an interlude plus an audit. **Name what none of them asked.**
⚠️ If your answer is "nothing," you are almost certainly wrong — say instead which
question you are least confident was covered, and why.

## 3 · Scope fence

**IN:** challenging the verdict · walking spot-checks yourself · reading every
artifact · your own C5 answer · **overturning the verdict**.

**OUT:** ⛔ re-running the sweep · ⛔ new fixes (⚠️ unless you find something
launch-blocking, which you fix and put in your first sentence) · ⛔ a version bump
· ⛔ publishing anything · ⛔ the opt-in and rescue repos · ⛔ moving the release
tag — the audit does that, and ⭐ **if you overturn, say plainly whether the tag
must move back.**

## 4 · ⛔ What you may not claim

- ⛔ **"I agree with the audit"** as a finding. Agreement needs its own evidence;
  say what you checked to reach it.
- ⛔ **"The chain was thorough."** Thoroughness is not the question. **Is the
  verdict right?**
- ⛔ Any count you did not emit or measure · any player-route claim not walked ·
  bare `tested`.
- ⚠️ ⛔ **Do not manufacture a disagreement to look useful.** *"The verdict holds,
  here is what I tried to break and how it survived"* is a complete and valuable
  answer — an adversary that always finds something is as useless as one that
  never does.

## 5 · Close-out

One commit: your ruling · any launch-blocking fix · `SWEEP_FINDINGS.md` appended
with your challenges and their outcomes · `SWEEP_LEDGER.md` closed with **your**
convergence ruling if it differs from the audit's · owner items on
`docs/PLAYTEST_CHECKLIST.md` · `STATE.md` updated · `doccheck` GREEN ·
`git rm` this file · commit naming the grave · push.

**The owner report — short, and the first line is the whole product:**

1. ⭐ **UPHELD** or **OVERTURNED**, in one sentence.
2. What you tried to break, and what happened to each of the five challenges.
3. If overturned: **exactly what must be true before this uploads.**
4. Your C5 answer — the question nobody asked.
5. ⚖️ **Was the chain worth its cost?** The owner will decide whether to run this
   method again; an honest verdict on the method is worth more than a compliment,
   and you are the only session positioned to give one.
