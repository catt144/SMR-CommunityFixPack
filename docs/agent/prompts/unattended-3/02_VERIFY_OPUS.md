# Chain prompt 2 — the unattended verification launches

**Read `README.md` first — binding chain rules apply.** Staleness check, live
todo list. ⛔ **EF-056 discipline brackets EVERY launch**: byte-copy every
autosave before, reconcile the save directory BY NAME after, each launch, not
just the one you expect to matter. ⭐ EF-051 is lifted — but if any of its 17
named strays reappears, stop and re-open the fact.

## Job 1 — the suite, both mods loaded (rig norm)

Full TestKit run with the new probes registered. Read PASS/FAIL/SKIP/ERROR out
of the flushed log by counting its own lines (the release-3 audit's method),
never from memory; **SKIPs by name, never a total** (STATE rule). Archive the
log `docs/archive/` byte-verified. Baseline comparison: the pre-build cell was
`78/0/16/0` of 94 (`archive/rs_r0_*`); every delta must be one of the new
probes or explained.

## Job 2 — the C39 bracket, on a staged copy of `CP15PT15`

The verification the ruling itself specified (`C39.md` §2026-08-12): re-run the
exact paused bracket — stage a `Copy-Item` of `CP15PT15.savegame.sav` (it holds
the measured `TVStudioWorkshopCCP1#1526` and the `Diner#1475` control),
pre-copy autosaves first (EF-056 — that save's lineage is the one that ate
`Sol 306`), enact `Policy_Automation_ServiceAutomation`, read paused
before/active/after:

* **Expected:** the subject now rides toward the ~2× uplift the control showed
  (`114→268` was the control's measured ride); revert restores both.
* Take the `Now()`/clock line at EVERY read including the revert — the 08-11
  bracket's one recorded harness gap was the missing pause evidence at revert.
* If only the TVStudio exists in the save, the other mismatches stay INFERRED —
  state it, as the entry does.

## Job 3 — the F85 flip reading

Whatever 01's probe design samples: run it in a real launch and read the log.
The honest boundary stands (README stop condition): a `dont_pause` value read
through the wrapper is a measurement; **"the popup visibly pauses the game" is
a SCREEN claim and stays unclaimed unattended** — do not upgrade by word
choice. If a screen witness is genuinely needed for `fixed`, route the ask as a
minutes-scale add-on to the owner's next sitting instead of claiming it.

## Job 4 — flip the entries on evidence, close the prompt

Entries F85/C39 updated with measured results and log citations; status flips
per house vocabulary (tag + index row, regenerate the index); the F85
distress-call watch rider retires **only if** its retirement condition ("when
the fix verifies") is actually met by what Job 3 sampled — otherwise say what
is still open. `--emit-counts` re-run · commit, push · **append Notes from
upstream to `03_AUDIT_FABLE.md`** (every claim with its log line, what was NOT
sampled, the exact counts at your moment) · delete this file in the closing
commit.

## Notes from upstream (prompt 01, 2026-08-15 — the build)

**Commits:** fix pack `92fe101` (both modules, both entries, INDEX, STATE,
checklist) + this prompt's closing commit · TestKit `5113cca` (probes).
⚠️ **The TestKit repo has NO git remote configured** (`git remote -v` is empty,
branch `master` has no upstream). Its commits are local-only; that is not a
push failure, but say so rather than claiming a push.

**Staleness at my moment:** fix pack `c0c6903` clean + `git pull` "Already up to
date"; TestKit `da432f8` clean. Src re-read at **1.0.7.396349** throughout.

### What was built — every new line, by file

| file | what |
|---|---|
| `Code/Fix_DistressPopupPause.lua` | **NEW.** id `DistressPopupPause`. §1.4 chained wrapper on `PopupNotification.Init` in its §3a **Layer 3** form: clears `self.dont_pause`, then calls the original, so **vanilla's own body** builds the `XPauseLayer`. Exposes `clear_pause_flag` on its def. |
| `Code/Fix_AutomationLawCompensation.lua` | **NEW.** id `AutomationLawCompensation`. §1.4 chained **post**-wrapper on `Workplace.GetWorkshiftPerformance` returning `orig(...) + exact delta`. Exposes `find_automation_law` and `compensation_delta` on its def. |
| `metadata.lua` (fix pack) | both files appended to `code`, immediately before `Code/90_SaveSanitizer.lua`. |
| `TestKit Code/59_Probes_Wave10.lua` | **NEW.** two `[behavior]` probes, ids `DistressPopupPause` and `AutomationLawCompensation`. |
| `TestKit metadata.lua` | the new wave file registered after `58_Probes_Wave9.lua`. |
| `docs/agent/bugs/F85.md` · `C39.md` | status `filed` → **`built`** (front matter + heading tag, index regenerated), plus a dated build section each. |
| `docs/agent/bugs/INDEX.md` | regenerated (never hand-edited). |
| `docs/agent/STATE.md` | counts block re-emitted; the ⑥ line now points at **you**; owner decisions 3 → **4**. |
| `docs/PLAYTEST_CHECKLIST.md` | **new item 30** — the C39 scope-growth confirm (reading-only, blocks nothing) + an awareness note that F85 is built. |

### ⭐ COUNTS AT MY MOMENT — emitted, never typed (`python tools/doccheck.py --emit-counts`, GREEN)

```
- modules: 76 registered (76 default-active, 0 optional-gated files)
- Code/*.lua files: 77
- TestKit probes: 96
- BUGS index rows: 103 F + 12 D + 46 C
```
⛔ **Re-emit these yourself** — do not inherit this block. Prompt 03 owns
reconciling them across cards, `metadata.lua`, site and portal sheet; you only
owe STATE's block if anything you do moves it.

### ⛔ THE C39 COVERAGE LIST — the build's contract, and it is EIGHT, not four

Carries an automation label · IS a `Workplace` · fails all three `IsKindOf`
gates. Full table with every class chain and every `performance` consumer:
`agent/bugs/C39.md` §2026-08-15.

| label | families |
|---|---|
| `ServiceBuildings` | `ArtWorkshop`, `BioroboticsWorkshop`, `VRWorkshop`, `TVStudioWorkshopCCP1` (the known four) **+ `SecurityStation`, `SecurityPostCCP1`** |
| `FactoryBuildings` | **`DroneFactory`, `BottomlessPitResearchCenter`** |
| `ResearchBuildings` | **none** — the sibling law exists (`Policy_Automation_ResearchAutomation`) and its label is clean |

Four label members are **not `Workplace`s** and are excluded by construction
(no `max_workers` property at all): `Amphitheater`, `OpenAirGym`,
`TaiChiGarden`, `MagneticFieldGenerator`. Nothing was routed under the README
stop condition — every mismatch is reachable by the ruled shape.

⚠️ **Only `TVStudioWorkshopCCP1` is MEASURED** (08-11). The other seven are
SOURCE. If your `CP15PT15` copy holds only the TV Studio, say so exactly as the
entry does — do not upgrade the other seven by proximity.

### What YOU must re-emit rather than inherit

1. **Every count** — `--emit-counts` at your moment (see above).
2. **The suite baseline.** The pre-build cell was `78/0/16/0` **of 94**
   (`archive/rs_r0_*`). The suite is now **96**. Every delta must be one of the
   two new probes or explained; ⛔ **SKIPs BY NAME, never a total.**
3. **PASS/FAIL/SKIP/ERROR read by counting the flushed log's own lines**, not
   from memory (the release-3 audit's method).
4. **Git log before you record any verdict** (FIX_POLICY §4 evidence freshness).

### How to sample each build — and where the honest boundary is

**F85 (your Job 3).** The probe reads
`SMRFixPack.defs.DistressPopupPause.clear_pause_flag` with three fixtures
(flag `true` → cleared; flag `false` → untouched; flag **absent** → still
absent) plus an idempotence pass. ⛔ **Why it does not touch the live call
site, and why you should not either:** after flattening,
`PopupNotification.Init` is the engine's **generated composite** (combined
method, `PropertyObject.lua:1663` + `classes.lua:1636-1652`) — calling it needs
a real parented XWindow, i.e. **a modal dialog on screen**, and
`debug.getinfo` on it names `classes.lua`, not the fix pack, so an `[install]`
probe would read false-negative. **The install evidence is the module's own
apply(): it reads the class method back and returns a reason string if the
write did not land, so a `ListFixes()` line reading `active` IS the witness.**
⛔ **A `dont_pause` value read through the wrapper is a MEASUREMENT; "the popup
visibly pauses the game" is a SCREEN claim and stays unclaimed** — the README
stop condition and the item-29 lesson from the same week. If a screen witness
is genuinely wanted, route it as a minutes-scale add-on to the owner's next
sitting.

**C39 (your Job 2).** The ruling's own bracket, unchanged: stage a `Copy-Item`
of `CP15PT15.savegame.sav`, ⛔ **pre-copy every autosave first (EF-056 — that
save's lineage is the one that ate `Sol 306`)**, enact
`Policy_Automation_ServiceAutomation`, read paused before/active/after.
⭐ **Take the `Now()`/clock line at EVERY read INCLUDING the revert** — the
08-11 bracket's one recorded harness gap is that `CP15.C39Revert` took none, so
the pause state at revert was never evidenced. Prediction, written here before
the run: the subject (`TVStudioWorkshopCCP1#1526`, 12 → 6 workers) should ride
from ~127 toward roughly **double**, in the shape the `Diner#1475` control was
measured taking (114 → 268 → 124), and the revert should restore both.
**The arithmetic says the delta on a full reduced shift of 6 identical workers
is exactly +100** (uncompensated 100 → compensated 200); a real colony's
workers differ, so expect the same shape, not that literal number.

### Design decisions made here that a verify leg must not silently re-open

* **C39 shipped a THIRD candidate**, not either of the two on the entry: a
  post-wrapper adding the **exact** delta (reconstructing only vanilla's
  per-worker loop, twice) instead of (a) scaling the whole result — which
  scales the overtime additive **and** is off by one on any heterogeneous shift
  (worked example: 152 where vanilla says 151) — or (b) a §1.5 body copy of a
  hot method, which §1.4b warns would reinstate the broken gate if an official
  patch ever fixes it. Reasoning is on the entry; if you disagree, route it,
  do not rebuild it.
* **F85's test is the FLAG (`self.dont_pause`), not a title/image fingerprint.**
  On 1.0.7.396349 those are the same set — `RivalColonies.lua:546` is the flag's
  sole user — so prompt 01's "only the distress popup" and the entry's ruling
  ("so ALL popups pause") are behaviourally identical here. Disclosed on the
  entry and in the module header: a future or mod-made popup that sets the flag
  would also be paused.
* **Both save-safety tiers are stated in the module headers and on the entries:**
  F85 = **Layer 3**, C39 = **Layer 2 by construction**, both **nothing
  persisted**. Neither writes anything new into a savegame. If your run finds
  otherwise, that is a stop-and-route, not a footnote.

### Open items you inherit

* ⚖️ **Checklist item 30** — the owner's confirm that C39's widened footprint
  (Security Stations, Drone Assembler, Bottomless Pit — renegades, drone build
  time, research throughput) ships as built. **Reading-only, blocks nothing**,
  and prompt 03 needs the answer before it writes card text. Do not chase it;
  just do not describe the fix as "the four Workshops" anywhere.
* **F85's §3.6 distress-call autosave rider retires only if what you sample
  actually meets its retirement condition** ("when the fix verifies"). If it
  does not, say what is still open rather than retiring it.
* **F85 severity/tier is still the owner's open decision** (checklist item 5),
  and nothing here needed it settled.
* ⚠️ **Neither entry may reach `fixed` on a probe alone** — the frozen bar is
  `fixed` + suite + self-checks + verified save-safety tier (owner, checklist
  14).
