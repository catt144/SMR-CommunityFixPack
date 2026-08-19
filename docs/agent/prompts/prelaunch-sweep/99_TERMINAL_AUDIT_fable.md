# Terminal audit — the chain's backward QA, and the last word before upload

♻️ **SELF-CONSUMING.** Delete this file in your closing commit, naming its grave.

You close the pre-launch sweep chain (`00_CHAIN_SPEC.md`). Every link before you
worked **blind to the others' findings by design**; you are the first and only
session that sees the whole body of work at once. ⛔ **You are also the only one
who may read `SWEEP_FINDINGS.md`** — read it, and every `sweep: link …` commit
body the links were forbidden to open.

⛔⛔ **THE UPLOAD IS PAUSED ON YOUR VERDICT.** The owner overrode a
ship-now-fix-later recommendation with *"I want us to be clean period"*, so the
last sentence you write decides whether this mod goes out.

---

## 0 · Read path and staleness

```
git log --oneline -20
git pull
python tools/doccheck.py --emit-counts
python tools/upload_preflight.py
grep -rln "TEMPORARY" Code/ ../SMR-BugFixPack-TestKit/Code/
```

`00_CHAIN_SPEC.md` · `SWEEP_LEDGER.md` · `SWEEP_FINDINGS.md` · every link's
commit body · every artifact under `docs/agent/reports/` the links produced ·
`Code/00_Core.lua` · `docs/agent/STATE.md` · `docs/PLAYTEST_CHECKLIST.md`
item 37 · `docs/agent/FIX_POLICY.md` · `RELEASE_PORTAL_PREP.md` §0.5.

## 1 · 🗒 Live todo list

One item per verification unit. One item per link audited. One for the final
sweep. One for the verdict.

## 2 · Part A — audit every link's work

⭐ **RUN THIS PART AS A FAN-OUT (added 2026-08-19, owner design).** Verifying N
already-settled findings is the one job in this chain that is genuinely parallel:
the findings are fixed, they do not compound, and each verification is
independent. ⛔ *Discovery* compounds and must stay sequential — that is why the
sweep was not fanned out (`CHAIN_METHOD.md` §5a).

**If your harness gives you subagents, spawn one per finding** (or per link, for
small sets) and have each **try to REFUTE**, not to confirm — default to *refuted*
when uncertain, and kill a finding on majority refutation. ⭐ Where a finding can
fail in more than one way, give each verifier a **distinct lens** (does the route
re-derive · does it reproduce · does it matter to a player) rather than N
identical skeptics.

⚠️ **If your harness has no subagents, do it serially — the concurrency is not the
point.** What is required is that each finding is checked **independently of the
report that produced it**, and that the check is adversarial rather than
confirmatory.

For each link, independently:

- **Re-derive the ROUTE, not the citations.** *Recorded facts are claims too* —
  this project has been wrong in both directions in one week with every cited
  line correct both times.
- **Does the fix do what the link says it does?** ⛔ Verified by that fix's own
  falsifier, not by a green suite.
- **Did any link's fix break, mask, or silently revert another's?** The links were
  blind to each other; ⭐ **you are the only defence against thrash**, and this is
  the specific risk the design accepted.
- **Is any fix outside what a link was permitted to do?** Links 3+ were
  record-only except for launch-blocking findings.
- **Did any link overstate?** Check the forbidden claims list (`01_LINK.md` §7)
  against what each actually wrote.

## 3 · Part B — ⛔ a hostile re-read of the 2026-08-17 core fixes

Both landed in `Code/00_Core.lua` in `2f077e8`, before the chain existed, and
they are the reason the upload stopped. **Read that commit message LAST**, so it
cannot lead you.

### B1 — the `update_suspect` leak

**Claimed:** `Require` marks `update_suspect` on a target-shape failure; several
modules fail a pass and then succeed (first pass runs before the class hierarchy
is flattened — documented, benign, every launch); nothing cleared the mark on
success; `UpdateSuspects` then read it on any later `inactive`, **including a
`latch(..., "benign")`**. Fixed at **both** sites restoring `active` —
`ctx.heal()` and `run_apply`'s success branch.

⛔ **The question that could sink it: does clearing the mark now HIDE GENUINE
PATCH ROT?** Construct the case — a module that succeeds and *later* genuinely
rots. What still catches it? **If the answer is "nothing", this fix traded a false
positive for a false negative and that is strictly worse.** Say so plainly.

Then: is there a **third** site? Is `nil` right rather than `false`? Does the
substring fallback still behave with `detail` cleared to `""`?

### B2 — the `order` double-append

**Claimed:** `SMRFixPack` survives `ReloadLua` by design; `Register` appended
unconditionally; every reload double-listed every module; guarded now on whether
`fixes[id]` existed **before** the overwrite.

⛔ **The planted criticism — test it, do not take it on trust.** Before the guard,
two *different* modules registering the same id gave two `order` entries and one
silently overwritten table. After it: **one** entry and the same silent overwrite
— so **the guard may have made a genuine id collision quieter than it was.**
Decide whether re-registration with a *different* `def` should log. If it should,
that is a finding against the pre-chain work and you fix it.

Also: can `fixes[id]` be set by any path other than `Register`, making the guard
read the wrong signal?

### B3 — the rest of the pre-chain work

| claim | falsify by |
|---|---|
| `'image', "Mod/SMR_CommunityFixPack/preview.png"` resolves | ⭐ the **packed** case is the shipping case, and first load mounts on the **folder name** (`Mod.lua:1724-1740`). `98_LAUNCH_REHEARSAL.md` §4.3 tests it — did it? |
| Paradox before Steam | re-derive at Src |
| every editor save bumps `version` | `ModDef:SaveDef` |
| the package is 80 files | re-list the real `.fpk` |
| the update report "never fired in ~60 archived launches" | re-count `docs/archive/*.log` |

## 4 · Part C — your own final sweep

⛔ **You are not only a reviewer.** Take the lens the ledger shows was covered
**most shallowly**, or a ninth lens of your own, and sweep it properly.

⭐ **And ask the ledger's real question: what did EVERY link miss?** Not "did they
do their lenses" — *what question did none of the eight lenses ask?* That is the
shape of both defects found on 2026-08-17, and of every under-count in this
project's history: the brief never asked.

## 5 · Part D — rule on convergence, honestly

The stopping rule (`00_CHAIN_SPEC.md` §5) has three clauses and **only one of them
means the mod is clean.** State which clause the chain stopped on:

1. nothing new in unswept territory **and** no unswept area of consequence remains
   — ✅ genuine convergence;
2. two consecutive links returned only cosmetics — ⚠️ probable convergence;
3. the hard cap — ⛔ **not convergence**, and it must be reported as *"we stopped
   counting, not because there was nothing left."*

⛔ **A chain that stopped on clause 3 and is reported as clause 1 is the worst
outcome this design can produce.** It would launder a cap into a clean bill.

## 5a · ⛔ APPLYING FINDINGS INVALIDATES THE GATE — and how to discharge that cheaply

**Run B scored 10/10 on the tree as it stands** (2026-08-19,
`archive/runB_Mars.exe-20260819-17.20.44-*.log`). Every finding links 3–8
recorded is queued for you, and they land in **`Code/00_Core.lua`** — the file
all 75 modules route through. ⇒ ⛔ **The moment you edit it, the artifact run B
validated is no longer the artifact that would ship.** That is definitional, not
probabilistic, and this brief did not anticipate it: §4 says links record and the
audit applies, but the gate ran *before* the applying.

### What the queue actually is

⭐ **Known defects, unknown reachability.** They are measurements, not worries —
L8 seeded `SMRFixPack_Disabled = true` into the shipped source and lost **75 of
75** modules; seeded `SMRFixPack = {}` and lost 75 while `00_Core` survived.
⛔ **But every one is gated behind a third party** that does not exist in the
shipping configuration: a foreign mod writing our globals before we load, a
modder mis-reading the README, a foreign mod on one of two specific globals.
**None is reachable by a player running this pack alone.**
*(`L5-F3` is already OFF this queue — act 1 measured `AllMapsForEach` returning
`true 2085` with an object deliberately broken, so the three colonist-walking
fixes need no change.)*

### ⭐ The cheap discharge, and it rests on run B's own best result

**Run B proved the 75 applied module names PACKED are set-identical to the
UNPACKED run — packing changes no behaviour.** ⇒ **packed-vs-unpacked is no
longer an open variable**, so verifying an edit in the *unpacked* configuration
tells you what the packed one would do.

Unpacked verification is **run A** — TestKit on, opt-in off — **unattended, zero
owner cost.** One launch confirms 75 `applied` by name, no new `[LUA ERROR]`, and
the suite compared **by name** against `72/0/24/0`.

⇒ **The recommended route:**

> **Apply → verify with one unattended run A → carry it across to packed on run
> B's own finding, and state that argument explicitly rather than leaving it
> implicit.**

⛔ **The carry-over argument holds ONLY while no fix touches the packaging
surface** — the `code` list, `items.lua`, `metadata.lua`, or the file set. If one
does, the argument breaks and **run B genuinely needs re-running** (a two-act
owner sitting). Check this per change; do not assume it.

⚠️ **Each queued fix is a happy-path no-op by construction** — a type guard, a
`pcall`, two `or {}` refills; in the normal case the table is already a table and
nothing throws. ⛔ **That is also exactly what one says before a regression**, and
`00_Core.lua` is the one file where being wrong takes down all 75 at once, which
L8 did not argue but measured. **Verify; do not reason.**

### What is still the owner's, not yours

⚖️ **Whether to apply at all.** The owner overruled ship-now-fix-later once
(*"I want us to be clean period"*) — but that was a defect **players would see**
on a brand-new release. This queue needs a hostile third party. ⛔ **Do not assume
the same ruling repeats.** Route it to `docs/PLAYTEST_CHECKLIST.md` with the
options and a recommendation: apply + run-A verify (above) · apply nothing and
defer to 1.0.1 · apply and re-run B.

## 6 · Scope fence

**IN:** verifying and correcting the links' work · applying findings links 3+ only
recorded · your own final sweep · the convergence ruling · the upload verdict ·
moving the release tag.

**OUT:** ⛔ a version bump (1.0.0 is ruled; nothing has shipped) · ⛔ publishing
anything anywhere · ⛔ the opt-in and rescue repos (checklist 37 Q1 — owner's
call) · ⛔ `docs/archive/` and the frozen `MOD_DESCRIPTION.md` · ⛔ building fixes
for newly-found **game** defects (file the entry; item 34 already waits on the
owner with a recommendation of AFTER).

## 7 · Stop conditions

- **A pre-chain fix does not survive your re-read** → stop and report. The owner
  paused an upload for those two.
- **Two links' fixes conflict and you cannot determine the correct resolution** →
  route it; do not pick.
- **Run B (`98_LAUNCH_REHEARSAL.md`) was never completed** → ⛔ **you cannot issue
  an upload verdict.** B is the gate; without it you have no evidence about the
  configuration a player receives.
- `doccheck` red · save directory fails to reconcile → stop, and restore from the
  pre-copy first.
- ⚖️ **A NEW or UNATTRIBUTED `[LUA ERROR]`** → stop. ⛔ *Corrected 2026-08-19:*
  not *any* error — this rig carries **49 pre-existing vanilla ones every launch**
  (48× `Flight.lua:465` + 1× `:479`, documented since 2026-08-03). Attribution
  must be **shown** (line, age, reproduced count), never asserted.

## 8 · ⛔ What you may NOT claim

- ⛔ **"The mod is clean."** Say what was swept, by which lens, to what depth, and
  ⭐ **what was never reached** — the ledger's unreached column is the honest
  product of this whole chain.
- ⛔ **"Every link's work is verified"** without a falsifier per fix.
- ⛔ **Convergence** on a hard-cap stop.
- ⛔ **"Ready to upload"** without run B.
- ⛔ **Any count you did not emit or measure**; ⛔ any player-route claim without
  walking it; ⛔ `tested` (bare — closed to new work); ⛔ blanket verification over
  a table (provenance per row, ROUTE tagged separately — `WORKFLOW` R3).
- ⛔ **"Compatible with other mods"** — run A tested exactly one other mod, ours.

## 9 · Close-out

One commit: corrections and applied findings, each with its falsifier · your
final-sweep artifact · `SWEEP_LEDGER.md` closed with a convergence ruling ·
`RELEASE_PORTAL_PREP.md` updated wherever your measurements move it ·
owner-shaped items on `docs/PLAYTEST_CHECKLIST.md` · `STATE.md` extended, not
grown (byte caps, doccheck-enforced) · logs archived (`R8`) · `doccheck` GREEN · ⭐ **move
`fixpack-v1.0.0` onto the verified tree, local and remote (`--force`), if and only
if you clear it** — the tag must mark what actually gets packed, and it is
deliberately parked behind HEAD until then · `git rm` this file and
`98_LAUNCH_REHEARSAL.md` if it has run · commit naming both graves · push.

⛔⛔ **AND YOU DO NOT DELETE `99b_VERDICT_REVIEW_fable.md`** — added 2026-08-19 on
the owner's design. **Your verdict is reviewed by a second, independent Fable
before it is acted on.** You are the only session that has seen the whole body of
work, which makes you the single point of failure this chain has left; one session
ruling alone on whether a mod ships is exactly the shape this project distrusts
everywhere else. ⇒ **Hand off, do not sign off.**

**Then the owner report**, and the last sentence is the deliverable:

1. **Should this mod be uploaded?** — one sentence, no hedging in either direction.
2. What the chain found in total, and what you had to correct in its own work.
3. ⭐ **What was never looked at.**
4. Which stopping-rule clause, named.
5. Whether the chain method itself earned its cost — the owner will decide whether
   to use it again, and that judgement is worth more than a compliment.
