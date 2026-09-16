# C95 — stop the expedition draft taking habitat residents (BUILD; ⛔ NOT AUTHORISED YET)

One-off, authored 2026-09-16. Tool-neutral (Claude or Codex). `git rm` this file **and its
`prompts/README.md` row** in the commit that lands its result. Defect truth: [C95](../bugs/C95.md).

⛔⛔ **DO NOT FIRE THIS BRIEF UNTIL THE OWNER SAYS SO IN WORDS.** See §0. It was written so the
work is ready the moment they do; writing it did not start it.

**Execution starts with** `git log --oneline -8`, `git pull`, `git status --short`, `ListAgents`.
The authoring commit for this brief is the one that added it — `git log --oneline -1 --
docs/agent/prompts/C95_HABITAT_DRAFT_BUILD.md`. Compare `<that sha>..HEAD` across the read path
below and re-check only the groups that moved; an empty `git diff --stat` for a path means it
does not need reading.

**Read path, by file.** `docs/agent/bugs/INDEX.md` (grep it for the ids you need — ⛔ never read
it whole), then [C95](../bugs/C95.md) in full; `docs/agent/facts/INDEX.md`, then
[`EF-103`](../facts/EF-103.md) and [`EF-104`](../facts/EF-104.md); `docs/agent/FIX_POLICY.md`
§§1, 2, 2a, 2b, 3a, 4, 6; `docs/agent/WORKFLOW.md` "Probe hygiene" and "Testing checklist per
fix"; this brief. `docs/agent/STATE.md` only for current hold/scheduling status.
⛔ **Do not read C96 into this job** — it is a separate defect that happens to share the hold.

---

## 0 · ⛔ THE HOLD — read before anything else

⚖️ **Owner, 2026-09-15:** *"do not author it yet."* That standing instruction is recorded on C95
itself and is why this is a brief and not a module.

⚖️ **Checklist [185](../../PLAYTEST_CHECKLIST.md) is OPEN** and asks the owner to say when to
build each of C95 and C96. ⛔ **Until the owner lifts it in words, nothing in §§3–7 may be
started.** Reading, orienting and asking questions are always allowed; writing `Code/` is not.

⚠️ **This brief's existence is not the lift.** A future session that finds this file has found
prepared work, not permission. ⛔ Do not read "the brief exists, so it must be time" — check
`docs/WAITING_ON_YOU.md` and the checklist body for 185 before doing anything else.

---

## 1 · Your licence

Everything below is a **claim**, including the confident parts — house doctrine (`CLAUDE.md`).
⭐ **Assume there is an error in here and go looking for it.** One is already documented: this
brief corrects the handoff that commissioned it (§5).

- ⭐ **Question the engineering freely.** If the routing in §3 is wrong, refuting it is a better
  outcome than implementing it.
- ⛔ **Do NOT question the repair SHAPE.** §2 is the owner's ruling, argued by both seats and
  converged. Re-litigating it is out of scope; so is re-routing it to the opt-in pack.
- ⛔ This brief authorises a **build and desk tests**. It does not authorise a release, a save
  edit, a version bump, or launching the game without asking the owner.
- ⛔ **Shared tree.** Peers edit concurrently and **Codex is invisible to `ListAgents`**.
  `git log` / `git status` before any write; commit with a pathspec — ⚠️ which protects every
  *other* file but commits the working-tree content of any path you name.
- ⛔ A new `Code/*.lua` module **must** be added to `items.lua` or it ships absent.
  ⛔ Never open the Mod Editor; never hand-set `version`.

---

## 2 · Settled, inherited, NOT open for redesign

⛔ **Read the bodies in [C95](../bugs/C95.md); they are not restated here.** What follows is only
the list of things you must not re-derive or re-argue.

1. ⭐ **REPRODUCED IN PLAY** 2026-09-15, owner at the keyboard. This is one of very few entries
   that is not source-only.
2. ⚖️ **The repair is to exclude habitat residents from the EXPEDITION draft** — ⛔ **NOT** a
   widening of the return path. Owner's choice, with their reasoning on the entry.
3. ⚖️ **An oversight bug solved by a judgment call** → **main pack, with the judgment-call mark
   and the reasoning on the fix list.** ⛔ Not opt-in. The store card states no number by design,
   so only the fix list and FAQ move.
4. ⛔ **SCOPE: expeditions only.** The asteroid lander draws from a player-filled passenger list
   and is not an auto-draft — a hook on the expedition gather cannot reach it, and must not.
5. ⭐ **The predicate is vanilla's own:** `IsKindOf(unit.residence, "MicroGHabitatBase")`, the
   same test `IsSuitableWorkplace` already uses to keep habitat residents out of the colony's
   labour pool. ⛔ Key on `residence`, **not** `dome`. C95 carries why.
6. ⚖️ **The stall risk is CONSIDERED AND JUDGED NEGLIGIBLE**, with its reasons on the entry, and
   a stall is visible rather than silent. ⛔ **Do not re-raise it as a new finding.** If you find
   evidence that changes the judgment, that is a report to the owner, not a redesign.
7. ⚖️ **The scope sentence is load-bearing for the public copy:** nothing is being made
   ineligible; the change is **subtractive on one automatic picker**, not additive on player
   capability. The owner's publishable framing is on the entry — lead with it.

---

## 3 · The one real engineering decision — where the hook goes

⭐ This is the job's actual difficulty, and it is a **caller-and-inheritor question**, not a
design question.

**What was derived at authoring** (game 1.1.0.403908, `ModTools\Src`; re-verify per §7a):

- `CargoTransporter:GatherAvailableColonists` (`Lua/Buildings/CargoTransporter.lua:237`) is the
  colony-wide auto-draft. ⛔ `RocketBase` itself parents `CargoTransporter`
  (`Lua/Buildings/RocketBase.lua:2`), so **every rocket inherits it** — the class is not, on its
  own, an expedition scope.
- **Three implementations exist** and `EF-104` lists them. The lander
  (`LanderRocketBase:GatherAvailableColonists`, `LanderRocket.lua:1149`) **overrides** it with the
  player-filled list and never delegates to the base; `CargoTransporterNew` is a different class
  used by the space elevator.
- `CargoTransporter:Load` has exactly **two** call sites in the tree —
  `LanderRocket.lua:306` and `RocketExpedition.lua:536`. ⇒ **INFERRED, and this is the load-bearing
  inference of the whole job:** the only live route into the base gather is the expedition one,
  because the lander overrides it at line 196's dynamic dispatch.
- `RocketExpeditionBase:GatherAvailableColonists` (`RocketExpedition.lua:496-497`) does not
  inherit the body — it calls `CargoTransporter.GatherAvailableColonists(self, …)` **explicitly**,
  a table-field read at call time.

⚠️ **THE FLATTENING HAZARD, and it decides the hook.** Classes are flattened at build time, so a
runtime wrap of a parent class never fires for a leaf that holds its own copy. That makes
`RocketExpeditionBase` — the semantically perfect target — the *hard* one, and
`CargoTransporter.GatherAvailableColonists` — reached by an explicit table read — the *easy* one.
⛔ **Do not take the easy one on this brief's word.** The claim that it is expedition-scoped rests
on two call sites and one override; **count the callers and every inheritor yourself** before you
install anything, and say in the report what your count was and how you took it.

⚠️ **Whichever you hook, the module's `Require` block must name every `(class, method)` pair it
installs on or captures from** — the F107 rule, `FIX_POLICY` §1. And prefer the least invasive
technique that works (`FIX_POLICY` §1): filtering a pool the original returns is smaller than
replacing the body.

⚠️ **One shape question the builder owns, and it is not trivial.** Filtering *after* the original
returns is safe but wasteful in the failure case: the original may already have returned a short
list and set `colonist_summon_fail` off a population that included habitat residents. Filtering
the *pool* the original reads means reaching inside a body you do not own. ⭐ **Say which you
chose and what it costs**, and check what the choice does to the "Not enough Colonists" status
the player is shown.

---

## 4 · What the fix must NOT do

- ⛔ **No migration and no save fix-up.** The repair is **forward-only**: it changes who is
  eligible for a *future* draft. A habitat resident already away when a rocket lands still comes
  home by the old path and is still re-homed. Claim nothing more.
- ⛔ **No reach into the asteroid lander.** If your hook can affect a player-chosen passenger
  list, it is the wrong hook.
- ⛔ **No repair of the return path.** The owner declined it explicitly.
- ⛔ **No loud failure.** `FIX_POLICY` §2: if the predicate cannot be evaluated, vanilla behaviour
  must survive unchanged and silently.
- ⛔ **No status promotion without a witness.** Do not move C95 to a shipped status on a desk
  result.

---

## 5 · ⚠️ A correction to the handoff that commissioned this brief

The 2026-09-16 handoff (`perma/HANDOFF_ORCHESTRATOR.md` §0b) says the unisolated gate — rail
sweep vs `CanVisit` capacity — is *"still unisolated, and the brief must say so… A fix written
without settling that risks repairing the wrong gate,"* and asks whether this job needs
`EF-104`'s crew-trace instrument first.

⛔ **That is wrong, and C95 already ruled it wrong** in "Two things a future session must not get
wrong", item 1: **the gate is MOOT for this repair and is not a reason to delay.** A fix that
stops habitat residents being drafted at all means **neither gate is ever reached**. The gate
matters only to a return-path repair, which the owner declined.

⇒ **The answer to the handoff's question is NO: this job does not need the crew trace first.**

⭐ **But arm it anyway, for a different reason.** `SMRTest.Log.CrewDraft` (TestKit `acafc74`,
built 2026-09-16, **unrun**) prints the pool the shipped draft walked, the pre-filter's
casualties, both unemployed buckets and every colonist returned with the bucket they came from.
⇒ **It is the reach control for this fix**: armed before and after, it shows on one line whether
the habitat residents left the pool and whether anyone else did. ⛔ Read its design in `EF-104`;
⚠️ it must be armed **before** the expedition is assigned, because the gather runs once.

⚠️ `EF-104` also carries **one unexplained draft observation** (three idle+unemployed colonists
passed over while three employed were taken). ⛔ **That is not a blocker for this job either**,
and it is not this job's to settle — but if your testing produces a line that explains it, put it
on `EF-104` rather than losing it here.

---

## 6 · Acceptance

- **The predicate fires on both habitat classes.** Naturalist and Micro-G both descend from
  `MicroGHabitatBase`; prove one test covers both rather than assuming it.
- **An expedition draft in a colony with habitat residents takes none of them**, and the reach
  control (§5) shows them absent from the returned list while the rest of the pool is unchanged.
- ⭐ **The negative leg, and it is the one that catches a too-wide hook:** a **player-chosen
  asteroid-lander passenger list containing a habitat resident still carries them.** A fix that
  fails this has reached past its scope.
- **Trade / supply / colony-transfer drafts are untouched** — the space elevator's
  `CargoTransporterNew` path is a different class; show it is unaffected rather than assuming.
- **Fail-safe leg:** with the predicate made unevaluable (a colonist with no `residence`, a
  missing class), vanilla behaviour survives and nothing is logged loudly.
- **Removal leg:** with the module removed, the next load behaves exactly as vanilla.
- **A clean boot:** the module's `applied` line present, no error-shaped lines, exit 0.
- ⚠️ **A FIX INVALIDATES ITS OWN TESTS.** Base any harm leg on the **pre-fix** body and re-run the
  **whole** suite, not only the changed leg.

⚠️ Any behavioural or assignment-quality claim must state the fixture's scarcity, fleet, density
and layout, and report **that colony's** measurement rather than generalising from a forced setup.
⛔ Name every setup mutation; reject one that intersects the draft itself (⚠️ a colony-wide
employment reassignment is exactly such a mutation — it is `EF-104`'s leading hypothesis for the
unexplained observation).

---

## 7 · Deliverable and stop conditions

**Deliverable.** Module in `Code/`, registered via `SMRFixPack.Register`, gated via
`SMRFixPack.Require` with every `(class, method)` pair it touches. `items.lua` updated. Build
report at `docs/agent/reports/C95_HABITAT_DRAFT_BUILD.md` carrying the caller/inheritor count and
how it was taken, the hook choice and its cost, and everything that did not work. C95's front
matter **and** its body heading tag updated together — ⛔ a status flip must hit both or doccheck
goes RED, and a status change belongs in the title too, because `INDEX.md` renders title + status
and nothing else.

Label every claim **SOURCE / MEASURED / INFERRED**, keep a **Not opened** list, and say what each
refutation depends on. `python tools/doccheck.py` GREEN before committing; commit with a pathspec
after re-checking `git status` for a peer's uncommitted work.

**Owner-facing.** Put the playtest recipe on `docs/PLAYTEST_CHECKLIST.md` with its `ck` marker
(⛔ `### <date> — <n>: <title>` plus the marker comment; sub-headings are `####` — an `##` heading
silently closes "Decisions waiting on you" and orphans every item below it). Draft the fix-list
row and its judgment-call reasoning from the owner's own wording on C95. ⛔ Then **STOP**: nothing
ships until the owner lifts the hold in words.

**Stop conditions — permission to report rather than push on.** Stop and report if: the
caller/inheritor count contradicts §3's inference; no hook can be expedition-scoped without
reaching the lander; the predicate cannot be evaluated where the draft runs; the fix would need a
migration to be useful; or testing produces evidence that the stall risk is real after all. ⛔ In
each case the finding is the deliverable — do not improvise a different repair shape.

**What may NOT be claimed.** ⛔ Not "habitat residents can no longer go on expeditions" — the
player can still send them by hand. ⛔ Not "colonists already away are rescued" — the repair is
forward-only. ⛔ Not "confirmed live" on a desk result. Where the evidence will not carry the
claim, **write the narrower true statement.**

**Lifecycle.** This is a one-off. When it reports, `git rm` it and delete its `prompts/README.md`
row **in the same commit**. ⛔ No tombstone row, no struck-through line.

---

## 7a · Derived facts and falsifiers

| fact | how it was measured | at | falsifier |
|---|---|---|---|
| The repair shape, classification, scope and public framing are the owner's rulings | owner's own words quoted on C95, 2026-09-15 | C95 at this brief's authoring commit | a later owner ruling. ⛔ No source read and no test result overrides it |
| The gate (rail sweep vs `CanVisit`) is moot for this repair | C95 "Two things a future session must not get wrong" item 1 | same | a change of repair shape to a return-path widening — which the owner declined |
| `IsKindOf(unit.residence, "MicroGHabitatBase")` is vanilla's own habitat predicate | `IsSuitableWorkplace`, `Lua/Buildings/Workplace.lua:1446-1462`, quoted on C95 | game 1.1.0.403908 build 24995074 | `grep -n "MicroGHabitatBase" <Src>/Lua/Buildings/Workplace.lua` — no hit means the branch moved; re-read before keying on it |
| `RocketBase` parents `CargoTransporter`, so every rocket inherits the base gather | `grep` of `__parents` across `Lua`/`DLC` | same | `grep -rn '"CargoTransporter"' <Src>/Lua <Src>/DLC \| grep parents` — a new parent list changes the scope argument |
| `CargoTransporter:Load` has exactly two call sites, so the base gather is expedition-only in practice | `grep -rn "CargoTransporter\.Load\|self:Load(" <Src>/Lua <Src>/DLC` | same | the same grep returning a third site. ⛔ **INFERRED — re-run it and count inheritors before hooking** |
| `RocketExpeditionBase` calls the base gather by explicit table read, not inheritance | `RocketExpedition.lua:496-497` | same | reading those two lines; a change to `self:` dispatch breaks the easy hook |
| `SMRTest.Log.CrewDraft` exists and is the reach control | TestKit `acafc74`, built 2026-09-16 | TestKit HEAD at authoring | `git -C C:/Dev/SMR-BugFixPack-TestKit log --oneline -- Code/90_Loggers.lua`; ⛔ it was **never run in play** — treat its output as unwitnessed until a sitting sees it |
| Module and fix counts are not inputs to this job | no acceptance clause depends on a stored total | — | if the build adds a module, emit the number with `python tools/doccheck.py --emit-counts` rather than writing one here |

⚠️ The installed build is a durable structural fact group: run
`python tools/doccheck.py --emit-fingerprint` and re-derive only the groups that moved. ⛔ Many
older citations point into a tree the 1.1.0 auto-update overwrote.

---

## 8 · Live todo list — change it as you go

At execution start mark item 1 `IN PROGRESS` and every later item `PENDING`; thereafter keep
**exactly one** unfinished commit-and-verify unit in progress, expand a stage as soon as it
splits, mark each unit complete when it finishes, and rewrite the list when reality changes.
⛔ Do not carry several commits behind one checkbox or update the list only at the end. Put stable
results in the item text — the owner reads this list to decide when to step in.

- [ ] 1. Orient; ⛔ **confirm the owner has lifted ck185 in words** — if not, STOP here and say so
- [ ] 2. Re-derive §3's caller and inheritor counts yourself; record the count and the command
- [ ] 3. Choose the hook and the filter shape; justify both, including what the shape costs
- [ ] 4. Probe sweep per `WORKFLOW.md` "Probe hygiene", recorded in the measurement commit
- [ ] 5. Module + `items.lua` + `Require` block; clean boot witnessed
- [ ] 6. Acceptance §6: habitat legs, the **lander negative leg**, the elevator leg
- [ ] 7. Fail-safe and removal legs, both re-based on the pre-fix body
- [ ] 8. Build report; C95 front matter + heading tag + title updated together
- [ ] 9. Checklist recipe with its `ck` marker; fix-list row drafted from the owner's wording
- [ ] 10. ⛔ **STOP** — report, and ship nothing until the owner lifts the hold
- [ ] 11. Your own findings, including everything that did not work
