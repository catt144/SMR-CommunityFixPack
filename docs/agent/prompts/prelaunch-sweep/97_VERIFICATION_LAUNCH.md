# Verification launch — run A, pulled forward, because four links never opened the game

♻️ **SELF-CONSUMING.** Delete this file in your closing commit, naming its grave.

⛔ **You are NOT a lens link.** You take no lens, you do not disturb the rotation,
and your ledger row is marked *interlude*. `00_CHAIN_SPEC.md` governs you
otherwise — read it, and its **§6.5 launch obligation**, which exists because of
the pattern that produced this brief.

---

## 0 · Why you exist, in four quotations

Links 1–4 swept L1 through L4. **Not one opened the game.** Each said so, in
detail, in the ledger's *NOT reached* column:

> **L1** *"neither 2026-08-17 core fix has yet executed"*
> **L2** *"the fix and the two `2f077e8` core fixes remain unexecuted in Surviving Mars"*
> **L3** *"Nothing was run in a game. No save was opened, no footprint was weighed, no object counted"*
> **L4** *"Nothing was run in a game — **fourth link running**"*

⛔ **This was a defect in the chain spec, not four lazy sessions** — those columns
are exemplary and are the only reason the pattern was visible at all. Launches
were permitted and never obliged, so the cheap path was always taken and the gap
was *declared* rather than closed.

⇒ **Your job is to close it.** The chain has an excellent reading of this mod and
**no evidence about the running mod**, while the two core fixes that paused the
upload have never executed and the release gate itself (run B) is a launch.

## 1 · 🗒 Live todo list, from your first action

One item per launch, one per job below. The owner reads it to decide when to step
in. Expand it the moment a job turns out to be several.

## 2 · Configuration — run A, and the rig is probably already in it

**TestKit ON · opt-in pack OFF · fix pack from the junction, unpacked.** Confirm
rather than assume; a full restart is needed if you change a mod's enabled state
(D13).

⚠️ **Label every number you record with this configuration.** The project's
recorded baselines (`80/0/16/0 of 96`, gates `75/75` + `8/8`) are the
**all-three-mods** rig. Yours are **re-derived, not compared** — ⛔ a moved total
is not a regression until someone shows it is. Compare **SKIPs BY NAME**.

⛔ **You are run A, which is INFORMATION, not the gate.** Run B — packed install,
junction pulled, TestKit off — stays terminal in `98_LAUNCH_REHEARSAL.md` because
it must test the final tree. ⛔ Do not attempt B here.

## 3 · ⛔ Before the first launch, in this order

1. **Probe hygiene gate** — no result is recorded before this reports clean:
   ```
   grep -rln "TEMPORARY" Code/ ../SMR-BugFixPack-TestKit/Code/
   ```
   This brief declares **no** needed probes. Any hit: repair and commit, or stop.
2. ⛔⛔ **`EF-056` pre-copy.** Byte-copy **every** autosave-tagged save, keep the
   copies **OUTSIDE** the save directory (a copy of an autosave *is* an autosave to
   the rotation), and record MD5s. **Reconcile by name after EVERY launch, not
   just the one you expect to fire.** It has eaten files twice.
3. **Pre-register your predictions in a pushed commit** — every expected value
   below, written down and pushed *before* the game opens. Precedents `3f1856f`,
   `94eb508`, `d762964`; the closing audit proved each preceded its launch in git.

## 4 · Job 1 — ⭐ THE OVERDUE DEBT: do the two core fixes actually work?

`2f077e8` fixed two defects in `Code/00_Core.lua` and **paused this upload**. Four
links have now swept a tree whose core changed under them and was never run.
⛔ **This job is why you exist; do it first.**

```lua
print("suspects:", #SMRFixPack.UpdateSuspects(), table.concat(SMRFixPack.UpdateSuspects(), ", "))
DbgPackMod(Mods.SMR_CommunityFixPack, false)   -- forces the ReloadLua that caused the bug
local seen, dup = {}, {} for _, id in ipairs(SMRFixPack.order) do if seen[id] then dup[#dup+1] = id end seen[id] = true end print("order:", #SMRFixPack.order, "dupes:", #dup, table.concat(dup, ", "))
print("suspects after reload:", #SMRFixPack.UpdateSuspects(), table.concat(SMRFixPack.UpdateSuspects(), ", "))
```

**Expected `0` · `75` / `0` · `0`.** Pre-register those.

⚠️ **Before `DbgPackMod`, confirm the mod is CLEAN** (`Mods.SMR_CommunityFixPack:IsDirty()`
returns false). A dirty mod forces `SaveWholeMod`, which runs
`version = version + 1` (`Mod.lua:967`) and would ship **1.0.1** against the ruled
1.0.0. If it reports dirty: **stop and report.**

⭐ **Also read the SaintBlessing cycle in the log** — `applied` → `inactive
(no dome-colonists trait presets)` → `corrected N ... of M` is the normal,
every-launch sequence, and its end state is what the first core fix was about.

## 5 · Job 2 — the suite, in a configuration nobody has ever measured

`SMRTest.RunAll()`. **Nobody has run this suite with the opt-in disabled.**

- Record PASS/FAIL/SKIP **BY NAME**, ⛔ never as a total.
- The SKIP set is the interesting artifact: which names skip *because* the opt-in
  is absent? That answer is needed by `98_LAUNCH_REHEARSAL.md` regardless.
- ⛔ Do not report a moved total as a regression. Different configuration.

## 6 · Job 3 — ⭐ falsify link 2's reload prediction, which is cheap and never observed

L2 established the second-Lua-load behaviour from two archived retail sessions and
predicted, among other things, **2 false suite FAILs on a reloaded session** —
⛔ *"neither two-load session ran the suite."* You can settle it in one sitting:

**suite → `DbgPackMod` (forces `ReloadLua`) → suite again.** Diff the two runs
**by name**. L2's prediction either fires or it does not; both answers are worth
having, and one of them means the suite lies after a reload.

⚠️ L2 also predicted **load 3 = load 2** with both archived sessions stopping at
two. A third `DbgPackMod` in the same session tests it for free.

## 7 · Job 4 — ⭐ the dialog that has never drawn, in any session, ever

L4 found the pack's **one designed screen surface** has never executed: its
pre-dialog log line has **zero** occurrences across every archived log. So how it
looks, where it lands and whether it is even legible is unmeasured.

**You have a console. Force it to draw** — set a suspect mark on one entry and
invoke the report path directly. ⛔ **From the console only. Do NOT add a file to
`Code/`** — that contaminates the very tree the chain is auditing.

Observe and record: does it draw · is the text legible and correctly wrapped ·
does it name the mod correctly (*"Relaunched Fix Pack"*) · where does it land ·
does it block anything. ⛔ **Restore the mark you set** and confirm
`UpdateSuspects()` returns to `0` before you close.

## 8 · Job 5 — harvest what else one sitting can carry

Read the ledger's four *NOT reached* columns and take what this configuration can
actually answer. ⛔ **Do not attempt what needs bespoke game state** — declare it
still-unreached instead, and be specific about what save or condition it would
need. Known to be out of reach here: L1's shelter-precondition co-occurrence,
L3's contended two-damage save, anything on a console platform, any non-English
run.

⚠️ **Nothing here is worth a fabricated setup.** An honest *"still unreached, and
here is the save it needs"* is worth more than a measurement of the wrong thing.

## 9 · What you may and may not do

⛔ **RECORD ONLY**, as links 3+ (`00_CHAIN_SPEC.md` §4). Findings go to
`SWEEP_FINDINGS.md`; the terminal audit applies them with the whole set visible.

⚠️ **One exception: a LAUNCH-BLOCKING finding is fixed immediately**, and your
report says so in its **first sentence**. ⭐ If job 1 shows either core fix does
**not** work, that is launch-blocking by definition — it is why the upload stopped.

⛔ **Never:** bump the version · publish anything · touch the opt-in or rescue
repos · add any file to `Code/` · attempt run B · leave the rig in a
configuration you did not document.

## 10 · Stop conditions

- **The mod reports dirty** before `DbgPackMod` → stop; the version is about to move.
- **Either core-fix falsifier fails** → stop, report, treat as launch-blocking.
- **`[LUA ERROR]` in any launch** → stop; do not keep launching.
- **The save directory does not reconcile by name** → ⛔ restore from your
  pre-copy *first*, before anything else.
- **`doccheck` red** → fix before committing.

## 11 · ⛔ What you may NOT claim

- ⛔ **"The core fixes are verified"** on a single launch that did not exercise the
  failing path. Say which path ran.
- ⛔ **A suite comparison against the recorded baselines** — different
  configuration. **By name, or not at all.**
- ⛔ **"Nothing appears on screen"** as a general claim — you ran run A, with the
  TestKit loaded and unpacked. That is not what a player has.
- ⛔ **"Compatible with other mods"** — run A tests exactly one other mod, and it
  is switched off. This configuration proves *less* about compatibility, not more.
- ⛔ Any count you did not emit or measure · any `tested` (bare — closed to new
  work; use `tested-unattended`, ⛔ never for a screen event, or `tested-attended`)
  · **"not caused by our leg"** as a dismissal — report unexplained log lines with
  their age.

## 12 · Close-out

One commit, subject exactly:

```
sweep: verification launch (interlude, no lens) — see SWEEP_FINDINGS.md
```

⛔ **Names no finding** — the subject's only job is to be boring enough that a
later link's `git log --oneline` staleness check is safe.

Carrying: your prediction commit (pushed **before** the launches) · logs archived
(`R8`) · **`SWEEP_LEDGER.md` appended with an *interlude* row** — ⛔ claim no lens,
and write *NOT reached* as **territory, not findings** · `SWEEP_FINDINGS.md`
appended · owner-shaped items on `docs/PLAYTEST_CHECKLIST.md` · `STATE.md`
extended, not grown (60-line cap) · `doccheck` GREEN · `git rm` this file · commit
naming the grave · push.

**Then the owner report:**

1. ⭐ **Do the two core fixes work?** — first sentence, no hedging.
2. What the suite did in this configuration, **by name**.
3. Whether L2's reload prediction fired.
4. Whether the dialog drew, and what it looked like.
5. ⛔ **What is still unreached, and what save or condition each item needs** —
   the chain inherits this, and it is the honest product of the sitting.
