# C35 detector — the one thing left of chain A

Paste into a fresh Claude Code session. **Written 2026-09-09** (`smrcf-bugfixpack-0e`,
on-call) at the owner's instruction to *rewrite* chain A rather than run or delete
it. **Start with `git log --oneline -10` · `git pull` · read `agent/STATE.md`
(mandatory).**

> ⚖️ **WHY THIS FILE REPLACED A THREE-FILE CHAIN.** Chain A was *"one unattended
> launch answers four questions and arms two standing detectors, owner cost
> ZERO"*. Five of those six deliverables are now dead:
>
> | original job | why it is gone |
> |---|---|
> | 1 · dust-devil marker reachability | the defect it gated is **fixed in 1.1.0 vanilla** — `facts/EF-084.md` |
> | 2 · does `AsyncPopsDownloadFile` exist at runtime | serves `C52`, which is `parked` by owner ruling 2026-08-20 |
> | 3 · is map generation drivable from Lua | existed to plan chain D, **consumed** `49e32bf` |
> | 4 · does any save hold a Jumbo Cave | `C25` was confirmed from a field save and shipped as `F110` |
> | 5a · `C25` detector | same — `C25` is closed |
> | **5b · `C35` detector** | ⭐ **still live, and this brief is all of it** |
>
> ⛔ **Do not resurrect the old brief from its grave to "do the rest".** The graves
> are `git show <sha>:docs/agent/prompts/smrcf-verify/01_PROBE_opus.md` and
> `…/02_AUDIT_fable.md` (sha in the commit that deletes them), and they are history,
> not a backlog.

## 1 · ONE JOB

Install a **log-only detector** in the Test Kit for `C35`, prove its wiring, and
leave it in place. Nothing else.

**`C35`** — *"Edit Payload confirmed while units are on the cargo ramp tears down
the rocket's command-centre connection **with no wait**, where the takeoff path
doing the same thing waits."* Filed 2026-08-01 from the fredware-#11 comparison:
**a real gap against F67/F68/F70/F71 (different function, zero overlap), mechanism
traced, HARM UNPROVEN.** Status `cand`, evidence `cand`, and its own row says it
*"is not a package until a live repro exists"*.

⇒ **This detector exists to turn `C35` from an argument into evidence, or to let
it die honestly.** It is not a fix and must not become one.

## 2 · What to watch, precisely

Wrap `TaskRequester:InterruptDrones` and log any drone that passes the filter
while `drone.command == "Embark"`, together with the caller.

✅ **Both branches re-read 2026-09-09 so you do not have to, and the answer is that
the mechanism SURVIVED the update** — which is what makes this worth building at
all:

| tree | `function TaskRequester:InterruptDrones` | `assert(drone.command ~= "Embark")` |
|---|---|---|
| 1.1.0 live | `Lua/_TaskRequest.lua:329` | `:344` |
| 1.0.7 archive | `Lua/_TaskRequest.lua:290` | `:305` |

The body moved **+39 lines** and the `Embark` assert is still there, unchanged in
shape. ⚠️ Still confirm against the tree before you edit — a line number is the
cheapest thing in this project to go stale, and these were true at commit time
only.

`EF-008` is why that assert saves nothing: **`error()`/`assert()` do NOT unwind mod
code, they report and execution continues**, so the `SetCommand("Reset")` that
follows still runs on a drone mid-embark. The assert is a developer's note that
this state is forbidden, not a guard that prevents it.

**Log, per hit:** the drone, its `command`, the requester and its class, the
caller (one stack level is enough), and game time. ⛔ Nothing else — no state
change, no `SetCommand`, no cancellation. A detector that alters the path it
watches has destroyed the evidence it was installed to collect.

## 3 · ⛔ THE TRAP THAT WILL EAT THIS IF YOU LET IT — `EF-058`

**A wrapper on a base class intercepts NOTHING when `DefineClass` has flattened
the function into subclass tables** (`classes.lua:988`). This project has been
bitten by it **four times**, and the shape is always the same: the wrapper
installs, reports success, and watches an empty road while the built copies do
the work.

Binding, therefore:

1. **Enumerate every class whose lookup resolves to the shipped
   `InterruptDrones`** — do not assume `TaskRequester` is the only one, and do not
   stop at the first subclass that has its own copy.
2. **Install on every one of them.**
3. ⛔ **PROVE the wiring off LIVE INSTANCES before trusting a single line of
   output.** A count of zero from an unwired detector is indistinguishable from a
   count of zero from a wired one — that is the F114 failure exactly, and it is
   the only way this brief can waste the owner's time.
4. State the proof in the close-out: which classes, how the wiring was
   demonstrated, and on what.

## 4 · Where it lives — the kit, permanently, and NOT as an armed payload

⛔ **The pack ships ZERO diagnostic code** (owner ruling 110). This is a Test Kit
module: `C:\Dev\SMR-BugFixPack-TestKit`, local-only with no remote **by design and
settled** — never raise a push there as owed.

⚠️ **It must NOT carry a `TEMPORARY` marker and must NOT go through
`tools/arm_leg.ps1`.** Those are for legs that arm, measure and disarm inside one
sitting; `doccheck`'s `temporary_sweep()` returns `not hits`, so a `TEMPORARY`
marker makes doccheck **RED** and blocks commits until it is removed. A **standing**
detector has to survive commits, so it is an ordinary permanent kit module in the
mould of `61_Probes_Wave11.lua` — it installs at load, watches passively, and pays
off during the owner's ORGANIC play rather than in a scripted run.

⇒ Follow the kit's own conventions: `README.md` (the three-mod rule, "Known probe
defects") and `Code/00_TestCore.lua`. ⚠️ **The kit was heavily rewritten by link
07 on 2026-09-09** (`d254b88`; kit `4f48c7b`) — read the current
`00_TestCore.lua` rather than any older description of it, and note that some
files bind `SMRTest` helpers to file-local aliases while others use
fully-qualified `SMRTest.*`. **Match the convention of the file you are in**; a
bare helper name in a file that never aliased it indexes a nil and ERRORs at run
time while parsing perfectly (found live in the kit on 2026-09-09).

## 5 · Owner cost, honestly stated

**Zero to build.** But ⛔ **do NOT repeat chain A's "owner cost: ZERO" claim as
though the detector pays for itself** — a passive detector only pays when the
owner plays, and `C35` needs a rocket, units on a cargo ramp, and an Edit Payload
confirm. That is a rare combination that may never occur organically.

⇒ **State that plainly in the close-out, and offer the owner the choice**: leave it
watching indefinitely at no cost, or spend ~10 attended minutes trying to trigger
it deliberately (the old chain B sitting carried exactly that 10-minute
ride-along). ⚖️ **The decision is the owner's, and it belongs in
`docs/PLAYTEST_CHECKLIST.md` → "Decisions waiting on you"**, not only here.

## 6 · Stop conditions — reporting beats pushing through

- **The wiring cannot be proven off live instances** ⇒ ⛔ **STOP. Do not install
  it.** Record why and hand the question back. An unproven detector is worse than
  none, because its silence reads as evidence.
- **`InterruptDrones` has changed shape on 1.1.0** such that the `Embark`
  condition no longer exists ⇒ that is an **ANSWER, not a failure**: `C35` may be
  vanilla-fixed like the dust-devil rider was. Check `EF-084` for the pattern,
  read both trees (1.1.0 live, 1.0.7 at `C:\Dev\SMR-SrcArchive\1.0.7.396349\Src`),
  and if so file the refutation as a **`facts/` entry** and flip `C35` — do not
  build a detector for a defect that is gone.
- **Watching it needs a behaviour change** ⇒ do not install it; say so.

## 7 · What may NOT be claimed

- **Not** "`C35` is real" — the detector firing once is evidence; the detector
  never firing is **not** evidence of absence, only of non-occurrence in the
  window watched. ⛔ Say which.
- **Not** "the detector works" until it has been **seen** to fire on a live
  instance, or its wiring demonstrated some other way that does not depend on the
  defect occurring.
- **Not** any status move on `C35` from a source read. ⛔ **Never move a status you
  did not witness**; `tested-attended` needs an attended witness.

## 8 · Close-out

`items.lua`/`metadata.lua` in the PACK are untouched — this writes no pack code, so
`H-10` does not apply. Kit commit(s) first (local; no push exists), then any pack
doc commit. `python tools/doccheck.py` GREEN before the doc commit, and a WARN goes
**verbatim** into the summary. Commits `git commit -F <file>` with an explicit list
of individual FILE paths (the git index is shared with several live sessions), then
**push** the pack — pushing is standing-allowed.

⛔ **`git rm` this file when the job is done**, and name its grave
(`CHAIN_METHOD.md:282`). If the folder ends empty, `smrcf-verify/` is finished and
chain A is closed — which also discharges the last live row of
`prompts/SMRCF_CHAIN_SET.md`, whose own rule is that it is deleted by the last
chain of the set to close. ⚠️ Chain C (`smrcf-modbrowser/`) is **kept by owner
ruling**, so it is NOT dead — check before concluding the set has closed.
