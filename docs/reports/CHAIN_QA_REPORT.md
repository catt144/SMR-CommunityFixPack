# Chain QA Report — the backward check over everything (chain prompt 12, 2026-08-03)

**Verdict up front: FINDINGS REPORT, not CLEAR — and every finding is bounded.**
The chain's work verified everywhere it was sampled, the doctrine the owner
ordered re-checked **holds**, and nothing owed was found dropped. The findings
are record defects, not work defects: one silently-excluded observation in a
scored table, two stale banners, one stale heading tag, one entry contradicting
its own forensics, and one permanent evidence loss (log rotation). All were
corrected in place with the finding recorded, per the scope fence. Chain
mechanics (inbox/outbox, self-consumption, counts) came through clean.

**Headline findings, most important first:**

1. **The "OFF is three different things" doctrine HOLDS** (job 0) — sub-claims A
   and B re-verified against the best remaining primary evidence; C stays
   INFERRED with a discriminating sitting designed and ready; D's
   installer table is below. **D13's population is confirmed: every player who
   ever installed any version of the pack, whatever their toggles.**
2. ⭐⭐ **The F97 rate question is SETTLED WITH NEW PRIMARY EVIDENCE** (job 8):
   this session extracted the original game's `Lua.hpk` and disassembled its
   dust-devil scheduler — **OG multiplies too**. The defect is
   broken-since-day-one, not a remaster regression. Verdict: **KEEP, with
   honest relabelling** (details in §4).
3. **The raw logs behind the founding F86 measurements are GONE** — the game
   keeps ~20 log files and all currently on disk are from 2026-08-02. The
   2026-07-31 discovery log and the 2026-08-01 Tier-1 logs are permanently
   unrecoverable; the same-day transcriptions are now the primary record.
   **Recommendation: copy the log file into the repo (or an archive folder)
   for any leg whose numbers a status flip will cite.**
4. **PT-61's vanilla arm ran TEN waves, not the nine its scored table shows** —
   WAVE 10 (`ATTEMPTED 1 … UNDER`, with the logger's own early-`break`
   diagnostic) was silently excluded. Defensible exclusion, silent record —
   disclosed on the F97 entry now. The verdict is unchanged. (Job 4, from the
   actual log file.)
5. **F76 is CLOSED — REFUTED** (job 10, owner-routed adjudication) and its
   unrefuted residue (the OG witness + the out-of-range-mouse lead) is
   preserved as **C41**. **D12 STANDS** (job 9). The blind audit's merit exam
   is complete with an ANNEX on `BLIND_AUDIT.md` (job 6b), which is now
   **committed to the repository** — the seal dissolves with this chain.

Corrections applied this session (all with findings recorded): D03's
toggle-method "uninstall" re-labels (×3 locations + the frozen PT-52 rider),
F29/F57's stale "OWNER DECISION OWED" banners, F68's lead paragraph, F55/F40/F73
framing notes, the D12 heading tag ("narrow reading" → the need_work rule), the
C40 note frozen on the superseded design, the F97 wave-10 disclosure, and the
uptime convention line in the checklist header.

---

## 1 · Job 0 — the doctrine, re-verified (owner: "we cannot be wrong about this")

### 1.1 Sub-claim A — the founding toggle-OFF measurement: **HOLDS**

Split as ordered. The **structural half** re-verified from primary source this
session: the pre-Tier-2 module (`git show 89bd463:Code/Opt_DroneOverhaul.lua`)
installs its wrappers at file scope with a per-call `module_active()` gate, and
the recorded error stack (`upvalue module_active`, line 96 ← line 190) proves
the wrapper was captured — while also proving the error itself is
**toggle-blind** (the throw happens at the `IsActive` read, before any branch).

So the toggle-OFF half rests entirely on account state at save time, and that
was re-derived, not inherited: PT-52's B2 A/B had the toggle **ON** two days
earlier (2026-07-29), so the check was not vacuous. The owner set all toggles
back to base at the end of the 2026-07-30 night, and the
`Mars.exe-20260731-01.37.22` leg logged **`68/74` with six named
`inactive (opt-in module …)` lines** — landed exactly as predicted. Seven files
registered `optional = true` at that date and `Opt_DroneStatDials` is the known
active-at-base seventh, so **68/74 arithmetically requires `Opt_DroneOverhaul`
OFF**. The same-day evening reads (18.44 cold boot, 19.09 enable path) read
68/74 again. The PT-20TEST save was cut between those brackets, in a session
whose record shows no Mod Options interaction. **A holds — on same-day
log-derived brackets, because the raw log no longer exists** (finding 3 above).

### 1.2 Sub-claim B — manager-disable ≡ uninstall: **HOLDS**, same caveat

The 98-vs-98 junction-removal control survives only as same-day transcription
(`F86_DISCOVERY_POSITION.md` §1, written for adversarial review with log-level
texture: identical locals, `1 mods installed`, the engine's
`present, but not loaded` → `not present` wording delta). Consistent across
both records; unrecoverable as a file; cheap to re-take if it ever matters
(leg 5 already reproduced the manager arm once at 80 errors).

### 1.3 Sub-claim C — the toggled-OFF no-op: **stays INFERRED**, sitting designed

Confirmed inferred-only, and confirmed **not constructible from shipped code**:
post-Tier-2, no shipped file-scope wrapper sits on a blocking body (that was
Tier 2's whole point), and the layer-2 residuals have nothing after their
calls. The owner's pre-offered sitting is designed and ready, with two
corrections to the proposal in the brief:

- **The probe must live in the FIX PACK's `Code/`, not TestKit** — leg 2
  removes the pack in the Mod Manager, and only a frame closed over the
  *removed* mod's env orphans. TestKit supplies observation only. The probe
  carries `TEMPORARY` in its header and dies in the commit that records the
  answer (WORKFLOW probe hygiene).
- **Leg 1 should use the Mod Options toggle, not the veto** — C's recorded
  wording is "toggled OFF", and the toggle is the exact instrument. (The veto
  variant is equivalent for a file-scope installer; run it as a free second
  reading if desired.)

**The protocol (predictions before either leg; both legs on one save):**
1. TEMPORARY probe module in `Code/`: registers `optional = true`; file-scope
   POST-wrapper on `Drone:Idle` (the old Site 2 shape) which, after the call,
   consults `module_active()` and only then (a) writes a marker GameVar and
   (b) touches a mod-created name.
2. Toggle ON, capture frames (drone-idle population; PT-58's settle method got
   73), save.
3. **Leg 1 — env present, toggle OFF:** reload. **C predicts: zero errors AND
   the marker is NOT written.** Silence alone is not the pass.
4. **Leg 2 — env absent (Mod Manager disable):** same save. **Predicts: orphan
   error naming the probe file.** If leg 2 is silent, the frames were never
   captured and leg 1 proved nothing — fix the fixture, report no result.
5. Session uptime recorded per the new convention.

An honest gap remains until it runs: the doctrine's middle row is measured on
both ends and inferred in the middle, exactly as `ENGINE_FACTS.md` now says.

### 1.4 Sub-claim D — the installer table (what each off-switch actually removes)

**File-scope game-function wrappers — the veto cannot uninstall these; they
pass through per call** (all six verified on **synchronous** seams post-Tier-2,
so none seeds frames today):

| module | file-scope wrapper(s) | note |
|---|---|---|
| `Fix_ExtenderFlapChurn` | `DroneHubExtenderBase.UpdateUplinkRequesters` | when ACTIVE spawns a ~2s debounce GT thread (mod-added, capturable, bounded one-error orphan — §3a-dispositioned); inactive = tail-call |
| `Opt_ClassicRockets` | `UniversalRocketBase.GetFuelResourceRequest` | sync getter |
| `Opt_DroneOverhaul` | `TaskRequestHub.FindTask` + `Drone.CleanUnreachables` | both verified sync (Tier 2) |
| `Opt_MultipleSuns` | `SolarPanelBase.GameInit` | sync |
| `Opt_ResidencyControl` | `Community.CanAcceptNewColonists` | sync predicate |
| `Opt_NoHomeless` | `Colonist.FindEmigrationDome` | sync; its `ChooseDome` half is apply-time |

**File-scope side-installs only** (OnMsg / OnDataReady / GameVar declarations —
all checked and internally gated on registry status, so the veto is honored;
GameVars persist regardless of any switch): `90_SaveSanitizer`,
`Fix_AstrogeologistExtractors`, `Fix_BrokenTrackSalvage`,
`Fix_CrystalMysteryHang`, `Fix_DestroyedTunnels`, `Fix_DisasterPredictionLeak`,
`Fix_DustSicknessBiorobots`, `Fix_FirstAsteroidPrefabs` (+GameVar),
`Fix_FounderTraitNotification`, `Fix_GhostFarmOxygen`, `Fix_MeteorFrequency`
(+GameVar `SMRFixPack_MeteorLatch`), `Fix_MeteorStormWedge`,
`Fix_IndependenceTerraforming`, `Fix_RainsDeadlock`, `Fix_SaintBlessing`,
`Fix_StaleReservations`, `Fix_TrackSalvageWipe`, `Opt_CohortHousing`,
`Opt_DroneStatDials`.

**Everything else (~57 files): pure APPLY()-TIME** — the
`SMRFixPack_Disabled[id]` veto prevents their hooks from ever installing
(`Register` returns at `00_Core.lua:384-388`, verified). Heuristic validated by
sample (`Fix_ShelterReflex`, `Fix_ArrivalDeaths` wrap inside `apply`).

### 1.5 The sweep, and the D13 sizing feed

- **Toggle-reload results:** three residual instances found beyond the
  2026-08-01 corrections, all re-labelled in place (never deleted): D03's
  PT-49 step-8 "uninstall shape VERIFIED" (archive result + instruction) and
  its restatement in D03's heading tag, plus the frozen PT-52 Trigger C rider
  that called a toggle flip "PT-20-style". **D03 has never had a real
  Mod-Manager uninstall leg; its uninstall standing is DERIVED** (sync wrapper,
  one absent-tolerant field) — true, but now labelled as such.
- **Optionality-leaning dispositions:** zero live instances beyond the
  already-corrected set. §5.3/§5.4 scoped by full-replacement status, not
  optionality; `Opt_*` modules were dispositioned on the synchronous filter on
  their own merits.
- **D13 sizing (the owner's actual question):** the cleaner's population is
  **every save from every player who ever installed any version** — because
  (a) pre-Tier-1/2 versions seeded frames from default-ON modules regardless of
  toggles, (b) declarative state (GameVars, dome fields
  `SMRFixPack_closed_to_new_residents` / `SMRFixPack_no_homeless`, DroneStatDials'
  label modifiers, the F97 descriptor copy) enters saves whenever the writing
  feature was used, whatever the toggles' later state, and (c) Mod Options
  survive manager-disable, so no switch state is evidence about save contents.
  The current build seeds **no wrapper frames** on any switch setting — D13's
  work is version history plus declarative markers, and its spec must derive
  the marker list itself (its entry already binds it to).

---

## 2 · The backward QA (jobs 1–4)

**Job 1 — inbox audit: CLEAN.** All 18 chain prompt files consumed across 17
close-out commits; every sampled deletion commit (4 of 17 verified in detail)
appends its outbox to the successor prompts + prompt 12 + README in the same
commit. No unconsumed notes found. One item of record: prompt 7's brief carried
a **deliberate, scoped disclosure of sealed content** (the F29(a) inheritance
guard, authored by the informed-review session) — defensive in intent, recorded
as an independence caveat in the `BLIND_AUDIT.md` ANNEX §0.

**Job 2 — owed-work sweep: every hit classified.** Deliberately standing (gate
named): D13 (hard launch dependency, spec gated on its own derivation), F84 +
D10 (post-release, loc-table capability), drone track (D06 rebuild, PT-52
frozen, B2 re-run), F48 (`blocked` — corrected pass too invasive to ship
untested), D01 rare-metals half (explicitly not owed), C26/C25/C20/C39/C40/F77/F80
(campaign riders, below). Done-with-evidence: everything else sampled. DROPPED:
**none found.** Two stale "OWED" banners (F29/F57 package 0) were the only
owed-markers contradicting reality — struck with pointers to the ✅ blocks that
had superseded them on the same entries.

**Job 3 — consistency: CLEAN.** Re-derived by counting, not inherited: **82
`Code/` files; 81 registered modules; 74 default-active (7 opt-in toggles +
DroneStatDials active-at-base); 87 probes (88 `SMRTest.Register(` minus the
definition); BUGS 110 rows = 98 F + 12 D** (the F-grep's 99th hit is the known
F97 rate-table line) **; C rows 40 → 41 after this session files C41.** All 110
index rows agree with their heading tags (19 candidate mismatches all resolved
as extraction noise — except the D12 tag, corrected, see §5). Probe sweep
(`TEMPORARY`): **zero hits, both repos.** `docs/prompts/` holds exactly the two
standing prompts + this chain's last two files. PT-54/PT-52 references all
properly struck or frozen-annotated.

**Job 4 — verification sampling: 4 flips, all verified — three against the
actual log files still on disk** (a first for this project's QA):

| flip | walked back to | result |
|---|---|---|
| F97 → `tested` | `Mars.exe-20260802-16.25.43` + `-17.02.15` (uninstall) | ✅ every scored claim reproduces from the raw log — vanilla locked at 3s/4s, fixed arm 0 or 6–8 reaching 8 twice, uninstall `count=1..2 → 0..1`, zero LUA errors. ⚠️ Finding 4: the un-scored vanilla WAVE 10 `UNDER`, now disclosed on the entry |
| D12 partial leg | `Mars.exe-20260802-22.28.07` | ✅ `78 PASS / 0 FAIL / 9 SKIP / 0 ERROR`, the seam line (`with D12 DomeBasic shuttle`), zero LUA errors |
| F98 live control | `Mars.exe-20260802-20.28.19` | ✅ exactly one `userdata` hit; the entry cites the right log. (The handoff note in prompt 12 cited `20.43.08` — wrong log name in a consumed note; entry correct) |
| F02/F78/F81/F88 → `tested` (Tier 1) | commit `c6180ad` | ✅ one commit flips rows AND tags with leg numbers, log names and measured values (75/83/72 h gaps; F88's +2256501 ms). Raw logs rotated away — finding 3 |

---

## 3 · Job 6b — the blind audit, examined (summary; full ANNEX on `BLIND_AUDIT.md`)

The audit's hit rate holds up under the informed record: **F29(a)'s reason is
factually wrong (four shipped Mystery-2 callers, re-verified) while its latency
conclusion is right; F55's contested verdict is the report's best finding**
(the vanilla intent comment is real and the entry never carried it — both tells
now added); **F40's core survives qualified** (and one claim of the 2026-08-02
informed review is *rejected on evidence*: the cure path, enumerated,
removes the trait from every carrier — "androids-never-cured" is unsupported);
**F73(b)'s intent inference is undercut** by the dev reply + patch note;
**F68's tension-spot was a real record defect** (lead paragraph vs its own
forensics — reconciled, with the build-vintage story); **F78's I-don't-know is
answered by play evidence**; **§11.3 and the closing observations are endorsed
and feed job 7.** Independence caveats (the embedded key; the F29 disclosure)
are stated in ANNEX §0. `BLIND_AUDIT.md` is committed with this report.

### ⭐ OWNER DECISION — the mod-page relabel package (do not decide silently)

Five entries are correct fixes whose *bug-ness* is a design judgment, and the
audit's closing argument is right that mislabelling costs more than the feature
is worth. **Recommendation: add a short "judgment calls" section to
`MOD_DESCRIPTION.md`** (or per-entry phrasing) that labels these as
behavior/judgment repairs rather than plain bug fixes:

| entry | honest label | why |
|---|---|---|
| F55 forever-mark | "behavior change, defended" | vanilla comment says intended; GOLD witness says harmful |
| F40 android dust sickness | "design judgment" | no code error; theme + ChoGGi precedent |
| F73(b) shelter reflex | "added safety behavior" | an absence, not a mistake; dev thread suggests the family is defect territory |
| F70 template refill | "design judgment" | template-as-default arguably designed |
| F97 dust-devil gate | "restores authored settings — more devils on some maps" | see §4: no shipped version ever delivered the gate |

The choice of wording is the owner's; the recommendation is only that these
five not be presented identically to, say, F23 or F12.

---

## 4 · Job 8 — the F97 rate review: **KEEP, WITH RELABELLING**

**New primary evidence obtained this session.** The record's open complication
("the shipped rates *may* have been tuned around the truncation") had a
documented, unattempted resolution: read OG's scheduler. Done — OG's
`Packs\Lua.hpk` (BPUL container, `_ENVLZ4`-delimited raw-LZ4 blocks, payload =
**compiled Lua 5.3 chunks with debug info**, correcting the record's "source"
inference) was extracted and the `DustDevils` scheduler proto disassembled.
**OG line 199: `Random(count_min, count_max)` → `GETTABLE spawn_chance` →
`MUL` → `DIV` by constant 100.** No comparison instruction. **The multiply is
original-game code.** (Method and disassembly recorded on the C23 entry;
extraction recipe is reproducible from that note.)

**What that does to the decision — both directions, honestly:**
- It **kills the "restore" framing**: no player has ever experienced the gate,
  in either game. fredware's mod name is historically wrong. On `VeryHigh_2`
  the fix delivers a +125% mean no version ever shipped.
- It **does not touch the intent evidence**, which now spans both games: the
  presets were authored as gate parameters (`VeryHigh_3`'s 6..8 unreachable in
  both; the same field help text; the same file's marker sibling gating; the
  Meteors trio gating), with zero counter-examples in `Lua\`. "Tuned around the
  truncation" fails as a design story because the tuning surface designers
  touch is the preset numbers, and every control shows what those numbers meant.

**Verdict: KEEP.** This is the pack's broken-since-day-one class (F23's
never-firing notification, F08's inverted operator, F12's unsatisfiable guard)
— age does not make delivered-halved-forever correct. The build is verified
(PT-61), self-heals on uninstall (measured), costs no §3a site, and the default
preset is untouched. **Conditions:** (1) the mod page describes it per the
relabel package above — "restores authored wave sizes; on some map settings
that means noticeably more dust devils than the game has ever delivered"; (2)
the C23-item-3 decline is CONSISTENT with shipping item 1 (both applied the
same rule — ship when a clean route exists, decline when all routes over-reach)
**but inherits the 8c lesson**: its cost estimate has a shelf life, and if a
clean seam ever appears for item 3, the decline is revisable, exactly as item
1's "impossible" route turned out to exist. Reversal of F97 remains cheap if
the owner weighs the feel change differently — one module, no persisted state,
uninstall measured — but this review does not recommend it.

---

## 5 · Job 9 — D12 adjudication: **THE BUILD STANDS**

All five routed decisions upheld, with the two hardest checked independently:

1. **Subject test = vanilla's `need_work`** (neither specced option): UPHELD.
   Both listed options were *tested and failed on evidence* (narrow falsified
   live on the owner's own retirement dome; broad falsified by the
   Senior-signal argument and the outside-the-workforce trap), the decider was
   the owner live, and the chosen rule is the game's own predicate computed two
   lines above the tie it breaks. A spec's open question answered with an
   unlisted option is the process working when it happens this way.
2. **Dome precondition** (Nursery/Retirement Home built): UPHELD — it is a
   scoping device, not automation; checked in the wrapper (not only UI) so
   demolition makes the flag inert. If players ever ask for the general form,
   this is the single line to revisit.
3. **The veto over a positive shipped answer**: UPHELD — **verified from code
   this session**: it fires only for `is_push_subject` colonists
   (`CanWork() ∧ no workplace ∧ not user-forced ∧ not Tourist`), which is
   **disjoint from D07's subject set by construction** (cohort members fail
   `CanWork`), so the order-independence claim holds whichever wrapper is
   outermost; it removes a measured round trip (6 colonists en route into
   draining domes), and "return nothing" is the shipped stay-put answer.
4. **Trait-based `ChooseDome` filter**: ACCEPTED with its recorded bound — it
   cannot read employment, errs conservative, never empties a candidate list,
   never touches `safety_dome`, excludes cohort + tourists. The
   employed-stranded-commuter cost case is bounded by validated cross-dome
   commuting (§4c).
5. **Probe gap (ChooseDome half)**: CONFIRMED as a genuine gap. **Recommend** a
   probe case driving the `ChooseDome` global the way case 11 drives
   `FindEmigrationDome` — cheap, same fixture style.

**Gates and residue:** PT-62's remainder (P4/P6 under a stable colony, P12
mod-manager uninstall, P13 veto lever) stays the only path past `speced`. The
**pack-wide `SMRFixPack_Disabled` gap** (the console veto is dead for D03 and
D07 — only `IsActive` is consulted) is presented as a small pre-release
consistency item: either honor the veto per-call in both, or record that the
lever exists only for D12/F97-class modules; today nothing has been measured
wrong, but a future leg using the lever on D03/D07 would silently run live.
Drift fixed this session: the D12 heading tag still said "narrow reading"; C40's
entry note had frozen the superseded design.

---

## 6 · Job 10 — F76 adjudication: **CLOSED — REFUTED; residue preserved as C41**

The ruling and its full reasoning are on the F76 entry (adjudication block).
In one paragraph: the decisive control was re-verified from Src rather than
inherited (`XDialog.lua:139` feeds the raw mouse into `GetMouseTarget`'s
box hit-test — one coordinate space), the measurements stand (whole-screen safe
area; anchor ≈ mouse to the pixel; the original forensic box back-solves to
correct placement at the same scale), the load failure did not reproduce, and
the reporter's premise — that the picker was mod-rendered — is corrected. No
defect is established anywhere in the entry's own scope, so the entry closes,
and P1 releases with it. **The two things prompt 11 flagged as must-not-close-
silently are honored:** the OG "icon does not appear" witness (a different
symptom) and the M5 out-of-range-mouse lead are filed as **C41**, with the
`F76MISS` hook named as the one-sitting instrument if the symptom ever
resurfaces. `MOD_DESCRIPTION.md`'s F76 draft note is struck as VOID (text
kept). Five documents carried the refuted mechanism as the item's identity;
all are corrected this commit (BUGS row/tag/entry, MOD_DESCRIPTION, STATUS,
FABLE_NEXT_PROMPT).

---

## 7 · The F46 second opinion (owed to this QA by prompt 8)

**The skip stands, but its stated grounds need one correction.** Prompt 8
declined to convert `Fix_TrainCargoDumping` because (a) §5.4's named route does
not exist (verified — `GetTargetAmount` is native, savegame-permanent,
unkeyed; that half is beyond dispute) and (b) the second route — pre-wrapper
swapping `station.storable_resources` under `pcall` — "mutates a persisted
property on a live object, worse on §3a grounds than the copy." **Point (b) is
inconsistent with F90's approved precedent**, which ships exactly that shape
(pcall + restore + re-raise on a persisted field around a verified-no-yield
call), and `Train:UnloadAll` is verified no-yield (`F86_SESSION_FINDINGS`
§1.3), so the swap window is uncapturable for the same reason F90's is. The
honest ground for the skip is **cost-benefit, not §3a ranking**: F90 had to
ship a new fix and the swap was the only sound route; F46's copy already ships,
is certified save-safe, and the conversion buys only rot-reduction.
**Recommendation:** move `Fix_TrainCargoDumping` from §5.4 group C ("no route")
to group B ("real route, needs a design pass — F90's shape; marginal benefit"),
so the record stops saying a route does not exist that demonstrably does.
Owner's call whether the conversion is ever worth the leg.

---

## 8 · Standing items (the complete post-chain queue)

| item | status | who/when |
|---|---|---|
| **D13** — uninstall procedure + cleaner | HARD LAUNCH DEPENDENCY; spec gated on Tiers landing+verifying (done) and on its own derivation; sizing feed in §1.5 | after the playtest campaign, before release |
| **Release gates** — per-site §3a dispositions (all recorded), fpk extraction diff, MOD_DESCRIPTION final wording incl. the relabel package (§3) and the D12 wording bound | standing | release phase |
| **PT-62 remainder** (D12: P4/P6, P12, P13) | the one leg gating a build already adjudicated KEEP | campaign — first |
| **Doctrine C-sitting** (§1.3 protocol) | designed, owner pre-offered the keyboard | campaign |
| **Load-heal round-trip sweep** — F86 Tier-1 version latch, rains migration, `90_SaveSanitizer` never save/load round-tripped; the two heals that were tested were both defective | campaign — cheap, high value |
| **Owner web-checks** (audit §7.1) | ✅ BOTH RESOLVED 2026-08-01 same-day (recorded §10.4); nothing owed | closed |
| **C36-adjacent mysteries-gate grep** (`Lua\Mysteries\`/`Scenario\` for `IsDisasterPredicted` gates) | deliberately UNASSIGNED — cheap grep, owner's call whether it becomes work; not owed | owner decision |
| **Asserts-build introspection sitting** (clears the 8 `[install]` probe SKIPs; MarsDebug + console `EnableIntrospection`) | recommended as a STANDING PLAYTEST ITEM, not chain work | campaign, low priority |
| **D03/D07 dead `SMRFixPack_Disabled` veto** (§5) | small pre-release consistency decision | owner |
| **D12 ChooseDome probe case** (§5) | recommended | next build session |
| **F46 group C→B move** (§7) | recommended | owner |
| **Drone track** (D06 rebuild, PT-52 frozen/B2 re-run, cleanup mod) | own standing prompt; not this chain's | `DRONE_PROJECT_PROMPT.md` |
| **D10 + F84** (loc-table work) | post-release by owner decision; **not owed** | post-release |
| **Log archiving for load-bearing legs** (finding 3) | recommended convention | immediate, free |

## 9 · The playtest campaign's top — what to run first at the keyboard

1. **PT-62's remainder** — it is the only thing between an adjudicated-KEEP
   build and its status, and the fixture guidance is already written (stable
   colony so the drain isn't fighting an inflow; mod-manager uninstall half;
   the repaired veto lever).
2. **The load-heal round-trip sweep** — save, reload twice, read the numbers
   (Astrogeologist +10% class of defect). Two-for-two defective on the heals
   actually tested is the worst base rate in the project; this is an hour.
3. **The doctrine C-sitting** (§1.3) — closes the one INFERRED cell in the
   doctrine the owner said we cannot be wrong about.
4. **Opportunistic riders as situations arise** — C40 (Crowded Living, one
   minute once the law + ministry exist), F90's underground-break watch (first
   storm on an elevator colony), C25 (Jumbo Cave), C39 (Service Automation
   law), F82's replaced rider is closed, F77/F80's riders per checklist §3.

---

*Written by chain prompt 12 (Fable), 2026-08-03. This report, the
`DOC_STRUCTURE_REVIEW.md`, the `BLIND_AUDIT.md` annex, and the record
corrections above land in one commit; the chain folder empties in the same
commit and the owner is free to play.*
