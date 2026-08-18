# Sweep link — run this, once, with one lens

⛔ **RE-RUNNABLE. Do not delete this file.** You are link N of a chain governed by
`00_CHAIN_SPEC.md`. **Read that first — it is binding**, and it explains why the
rules below are shaped the way they are.

⛔⛔ **THE UPLOAD IS PAUSED FOR THIS CHAIN.** The package is built and the owner
overrode a ship-now-fix-later recommendation with *"I want us to be clean
period."* Nothing has been published, so there is no 1.0.1 — `metadata.lua` is
untouched and **1.0.0 is what 1.0.0 now is.**

---

## 0 · Open your eyes in the right order

```
git log --oneline -10          # ⛔ --oneline ONLY. See the fence below.
git pull
python tools/doccheck.py --emit-counts
python tools/upload_preflight.py
grep -rln "TEMPORARY" Code/ ../SMR-BugFixPack-TestKit/Code/
```

⛔⛔ **THE CONTAMINATION FENCE — the chain's whole design rests on this.**

* ✅ **MUST read:** `SWEEP_LEDGER.md` (what previous links covered and, crucially,
  what they did **not** reach).
* ⛔ **MUST NOT read:** `SWEEP_FINDINGS.md`, or the **commit body** of any
  `sweep: link …` commit. Their subject lines are deliberately uninformative so
  `--oneline` is safe; `git log -p` and `git show` on those commits are **not**.
* ⚠️ If you read one by accident, **say so in your report.** A contaminated link
  is still useful; a contaminated link that hides it corrupts the chain's only
  convergence signal.

**Read path (file granularity):** `docs/agent/STATE.md` · `Code/00_Core.lua` ·
`docs/agent/FIX_POLICY.md` §1, §2, §3+§3a, §6, §8 · `docs/agent/WORKFLOW.md`
§"Probe hygiene", §"Testing checklist per fix", §"Log review" ·
`docs/agent/facts/INDEX.md` (at minimum `EF-054`, `EF-056`, `EF-058`, `EF-064`) ·
`docs/agent/bugs/INDEX.md` · `metadata.lua`, `items.lua`.
⛔ `docs/archive/MOD_DESCRIPTION.md` is FROZEN — ≥6 known-false claims kept on
purpose. Do not touch it, do not cite it.

## 1 · 🗒 Live todo list, from your first action

One item per commit-and-verify unit. Expand it the moment a pass turns out to be
four things. Mark complete as they complete, never in a batch. Exactly one in
progress. **The owner reads this list to decide when to step in.**

## 2 · Claim your lens

Take the **first lens `SWEEP_LEDGER.md` does not record** (table in
`00_CHAIN_SPEC.md` §3). Write your claim into the ledger **before you start
work**, so a concurrent session cannot take the same one.

If every lens is used, take the one whose ledger entry admits the shallowest
coverage, and **go deeper than it did** — say in your report what "deeper" meant.

## 3 · Sweep — and hold yourself to the standard that found the last two defects

The two defects found on 2026-08-17 were both invisible to per-module review and
obvious to one question about the whole system. **That is the altitude.**

- **Re-derive the ROUTE, not the citations.** This project has been wrong in both
  directions in one week with every cited line correct both times. A recorded fact
  is a claim.
- **Prefer the mechanical artifact to the assertion.** "I checked for collisions"
  is worth nothing; a symbol→patchers table is worth a lot. Commit artifacts under
  `docs/agent/reports/`.
- ⛔ **Never convert "no evidence of a problem" into "no problem."** If your lens
  cannot reach something, that goes in the ledger's *unreached* column — that
  column is what lets the chain terminate honestly.
- ⚠️ **A `[FAQ]`-shaped or owner-shaped finding is not yours to decide.** Route it.

## 4 · Fix, or don't, per your link number

| you are | do |
|---|---|
| **link 1 or 2** | fix what you find; **each fix gets its own falsifier**, not a green suite |
| **link 3+** | ⛔ **record only** — the terminal audit applies fixes with the whole finding set visible |

⚠️ **Exception at any link: a LAUNCH-BLOCKING finding is fixed immediately**, and
your report says so in its **first sentence**.

⛔ **Never:** bump the version · publish anything · touch the opt-in or rescue
repos · add an instrument to `Code/` (it contaminates the tree under test) ·
change what the mod promises.

## 5 · Verification, if you changed code

Unattended launches are yours to run; owner cost is zero.

⛔⛔ **`EF-056` IS LIVE AND HAS ALREADY EATEN FILES.** Byte-copy every
autosave-tagged save **before every launch**, keep the copies **outside** the save
directory (a copy of an autosave *is* an autosave to the rotation), and
**reconcile by name after every launch, not just the one you expect to fire.**

**Pre-register predictions in a pushed commit before each launch** (precedents:
`3f1856f`, `94eb508`, `d762964` — the closing audit proved each preceded its
launch in git).

⚠️ **Label every number with its configuration.** The recorded baselines
(`80/0/16/0 of 96`, gates `75/75` + `8/8`) are the **all-three-mods** rig. Numbers
you take in any other configuration are **re-derived, not compared.**

## 6 · Stop conditions — permission, not failure

- You cannot answer your lens's question from source → **say "unmeasured"** and
  put it in the ledger's unreached column.
- A finding needs a decision about what the mod should *do* → route to
  `docs/PLAYTEST_CHECKLIST.md` → *"Decisions waiting on you"*. **An ask recorded
  only in an agent doc is not asked.**
- `doccheck` red, or a launch produces `[LUA ERROR]` → stop and report.
- The save directory does not reconcile → **restore from your pre-copy first**,
  before anything else.
- You contaminated yourself on the fence → report it, keep going.

## 7 · ⛔ What you may NOT claim

- ⛔ **"The mod is clean" / "ready to ship."** Name what you checked, how, and
  **what you did not reach.**
- ⛔ **Any count you did not emit or measure.** Inheriting numbers is how
  "95 checks" survived two corrections.
- ⛔ **"No collisions" / "idempotent" / "save-safe in aggregate"** without the
  artifact, the actual reload, or the actual aggregate measurement. Per-module
  verifications do not sum themselves.
- ⛔ **A player-route claim** without walking the route on each platform.
- ⛔ **"Not caused by our leg"** as a dismissal — that is an attribution verdict.
  Report unexplained log lines with their age.
- ⛔ **Blanket verification over a table** — provenance per row, ROUTE tagged
  separately from citations (`WORKFLOW` R3).

## 8 · Close-out

One commit, and ⛔ **the subject line is fixed by the spec**:

```
sweep: link N — lens <name> — see SWEEP_FINDINGS.md
```

Detail goes in the **body** (which the next link is forbidden to read). The commit
carries:

- your fixes, each with its falsifier evidence;
- artifacts under `docs/agent/reports/`;
- **`SWEEP_LEDGER.md` appended** — lens, scope covered, depth, ⭐ **what you did
  NOT reach** (the column the stopping rule depends on). ⛔ No verdicts here;
- **`SWEEP_FINDINGS.md` appended** — everything you found, with routes;
- owner-shaped items on `docs/PLAYTEST_CHECKLIST.md`;
- `STATE.md` extended, not grown (60-line cap — evict resolved material to
  `archive/SESSION_LOG.md`, never an obligation);
- load-bearing logs archived (`R8`);
- `python tools/doccheck.py` GREEN.

**Then a plain-language report to the owner**, who decides whether to kick off the
next link:

1. **Does anything block launch?** (first sentence, always)
2. What lens you took, and what you actually swept.
3. What you found and what you did about it.
4. ⭐ **What you could not reach** — and your honest estimate of how much is left.
5. Whether you think the chain has converged, and **which stopping-rule clause**
   you are invoking if so.

⚠️ *"I found nothing"* is legitimate **only** if you can say what you looked at.
⛔ A "nothing found" while the ledger still lists unswept territory is **not
convergence — it is running out of lens**, and it must be reported as that.
