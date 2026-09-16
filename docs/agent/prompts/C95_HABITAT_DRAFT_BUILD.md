# C95 — stop the expedition draft taking habitat residents (BUILD + TEST)

One-off, authored 2026-09-16, **rewritten the same day when the owner lifted the hold and asked for
it to be fireable.** Tool-neutral (Claude or Codex). `git rm` this file **and its
`prompts/README.md` row** in the commit that lands its result. Defect truth: [C95](../bugs/C95.md).

⭐ **The owner has a test save ready.** ⛔ Do not provision a fixture and do not ask them to build
one — ask what is in the save they have, and design the legs around it.

**Execution starts with** `git log --oneline -8`, `git pull`, `git status --short`, `ListAgents`.
The authoring commit is the one that last rewrote this file —
`git log --oneline -1 -- docs/agent/prompts/C95_HABITAT_DRAFT_BUILD.md`. Compare `<that sha>..HEAD`
across the read path and re-check only the groups that moved; an empty `git diff --stat` for a path
means it does not need reading.

**Read path, by file.** `docs/agent/bugs/INDEX.md` (grep it — ⛔ never read it whole), then
[C95](../bugs/C95.md) in full; `docs/agent/facts/INDEX.md`, then [`EF-103`](../facts/EF-103.md) and
[`EF-104`](../facts/EF-104.md); `docs/agent/FIX_POLICY.md` §§1, 2, 2a, 2b, 3a, 4, 6;
`docs/agent/WORKFLOW.md` "Probe hygiene" and "Testing checklist per fix"; this brief.
`docs/agent/STATE.md` only for scheduling status.
⛔ **Out of the read path on purpose:** C96 (a separate defect sharing the old hold) and
[C100](../bugs/C100.md) (habitat residents leaving of their own accord — a different drain,
unruled, [ck188](../../PLAYTEST_CHECKLIST.md)). Neither is this job.

---

## 0 · Authorisation — what is lifted and what is not

⚖️ **Owner, 2026-09-16:** *"can you rewrite the c95 build I want to fire it and then we can test it,
already have the test ready in a save."*

✅ **BUILD and TEST are authorised.** The standing *"do not author it yet"* on C95 is lifted, and
[ck185](../../PLAYTEST_CHECKLIST.md)'s C95 half with it.

⛔ **ck185's C96 half is UNTOUCHED and still open.** Do not build C96 off the back of this.

⚖️ **Shipping shape was already ruled and is not yours to revisit:** main pack, with the
judgment-call mark and the reasoning on the fix list (C95's classification section). ⛔ The **release
itself** — version bump, upload, store text — is the release prompt's job and not this brief's. Land
the module and the evidence; do not push it out.

---

## 1 · Your licence

Everything below is a **claim**, including the confident parts — house doctrine (`CLAUDE.md`).
⭐ **Assume there is an error in here and go looking for it.** This brief has already been wrong
twice in one day: it called the post-filter shape "safe" when it hangs the game, and it proposed a
flag-based predicate that would have misfired on player-toggled domes. Both corrections are folded
in below; the third one is yours to find.

- ⭐ **Question the engineering freely.** If §3 is wrong, refuting it beats implementing it.
- ⛔ **Do NOT question the repair SHAPE.** §2 is the owner's ruling, argued by both seats and
  converged. Re-litigating it is out of scope, as is re-routing it to the opt-in pack.
- ⛔ **Shared tree.** Peers edit concurrently and **Codex is invisible to `ListAgents`**.
  `git log` / `git status` before any write; commit with a pathspec — ⚠️ which protects every
  *other* file but commits the working-tree content of any path you name.
- ⛔ A new `Code/*.lua` module **must** be added to `items.lua` or it ships absent.
  ⛔ Never open the Mod Editor; never hand-set `version`.
- ⛔ Do not launch the game without asking the owner first — ⭐ but note they are expecting a test
  this session and have the save ready, so ask early rather than at the end.

---

## 2 · Settled, inherited, NOT open for redesign

⛔ **Read the bodies in [C95](../bugs/C95.md); they are not restated here.** This is only the list of
what you must not re-derive or re-argue.

1. ⭐ **REPRODUCED IN PLAY** 2026-09-15, owner at the keyboard.
2. ⚖️ **Exclude habitat residents from the EXPEDITION draft** — ⛔ **NOT** a return-path widening.
3. ⚖️ **An oversight bug solved by a judgment call** → main pack, marked, reasoning on the fix list.
   ⛔ Not opt-in. The store card states no number by design, so only the fix list and FAQ move.
4. ⛔ **SCOPE: expeditions only.** The asteroid lander draws from a player-filled passenger list.
5. ⭐ **The predicate is vanilla's own:** `IsKindOf(unit.residence, "MicroGHabitatBase")` — the same
   test `IsSuitableWorkplace` (`Workplace.lua:1453`) already uses to keep habitat residents out of
   the colony labour pool. ⛔ Key on `residence`, **never** `dome`.
6. ⚖️ **The stall risk is CONSIDERED AND JUDGED NEGLIGIBLE**, with its reasons on the entry.
   ⛔ Do not re-raise it. New evidence is a report to the owner, not a redesign.
7. ⚖️ **The scope sentence is load-bearing for the public copy:** nothing is made ineligible; the
   change is **subtractive on one automatic picker**. The owner's publishable framing is on C95 —
   lead the fix-list row with it.

---

## 3 · The build — the owner's own design, and why it is the lead option

⭐⭐ **The owner designed this on 2026-09-16 and it is the route to build.** It beats what this brief
originally proposed, because it solves the scoping problem that made the per-bucket seam look
unusable.

### 3a · The predicate

One named helper, one line in it:

```lua
IsKindOf(unit.residence, "MicroGHabitatBase")
```

⭐ Keep it behind a named function even though it is one line — one place to read, one place to
change, and a door left open without inventing anything to hold it open.

⚠️ **Not `NaturalistHabitat`.** The two habitats are siblings: `NaturalistHabitat` →
`NaturalHabitatBase` → `MicroGHabitatBase`, and `MicroGHabitat` → `MicroGHabitatBase`. Keying on the
leaf silently misses the Micro-G habitat and ships a half-fix. ⭐ `IsKindOf` is a pure type test — it
pulls in **no** behaviour from the base class, so using the base costs nothing.

⚠️ **`residence` is readable at pick time.** It is only cleared at boarding
(`Colonist:EnterTransporter` → `SetDome(false)`), which runs after the gather has returned.
⭐ A `residence and …` guard is unnecessary: the picker itself passes a `false` workplace to
`IsKindOf` on every unemployed colonist, so the false case is proven safe every draft.

⛔ **Do NOT key on 1.1.0's residency flags** (`allow_work_in_connected`, `allow_service_in_connected`,
`accept_colonists`). They look like the game's own vocabulary for "exempt" — the shipped comment even
says *"residence-only communities (habitats) … opt out"* — but the 1.0.7 tree shows they are
**player-toggleable dome policies** (`Dome.lua:849`, `:883`, `Community.lua:147`). A predicate keyed
on them exempts **any dome whose player switched connected work off**: silent, colony-wide, and worse
than the bug. Body in `EF-103`. ⭐ The flags are the **fix-list reasoning**, not the `if`.

### 3b · The hook — wrap the per-bucket filter, scoped to the picker call

`CargoTransporter:GatherAvailableColonists` (`CargoTransporter.lua:237-292`) calls the global
`FilterColonistsByTrait` **once per priority bucket** (`:278`). Filtering there strips habitat
residents *inside* the picker, so the draft falls through to the next bucket and **fills the crew
normally**.

The scoping is the owner's insight: **swap the global only for the duration of the picker call**, from
a wrapper on `CargoTransporter.GatherAvailableColonists`. Outside that window the global is vanilla,
so the lander (`LanderRocket.lua:1171`, `:1182`) and the space elevator
(`CargoTransporterNew.lua:272`) — the other three of its five call sites — never see it.

⚠️ **Three things that decide whether it survives contact:**

1. ⛔ **Restore on the error path.** If the original throws and the swap is not put back, the global
   stays wrapped **permanently**, and from then on the lander and elevator filter habitat residents
   too — silently, with nothing to report it. `pcall` and restore on both paths.
2. ⭐ **The swap is observationally atomic, and that is load-bearing.** Nothing between the label
   read (`:240`) and the returned list (`:292`) yields — no `Sleep`, no `WaitMsg`, no thread
   creation, and the callees are pure reads. ⛔ **Re-prove that; do not inherit it from this brief.**
3. ⚠️ **Plain assignment, not `rawset`.** Mod code runs in a sandboxed env where `rawset(_G, k, v)`
   writes a shadow only this mod sees, so the shipped picker would keep calling the real function.
   Plain `FilterColonistsByTrait = wrapper` goes through `ModEnvMeta.__newindex` and reaches the real
   global. ⭐ Comment the line, or someone will "fix" it into a no-op.

⚠️ **Verify the wrapper fires at all.** `RocketExpeditionBase:GatherAvailableColonists`
(`RocketExpedition.lua:496-497`) calls `CargoTransporter.GatherAvailableColonists(self, …)` by
**explicit table read**, so swapping that field intercepts it whatever the leaf rocket class was
flattened into. ⛔ But `RocketBase` itself parents `CargoTransporter`, so the class alone is not an
expedition scope — the scope rests on `CargoTransporter:Load` having only two call sites (the lander,
which overrides the gather, and the expedition). **Re-count callers and inheritors yourself and put
the count in the report.**

### 3c · The two fallbacks, and when to reach for them

⛔ Only if 3b fails a check above.

- **Swap the pool instead.** Replace `city.labels.Colonist` (and each connected city's) with a
  filtered copy for the duration of the call. Same atomicity requirement, more surface.
- **Copy the body** and put `if not IsAutoPickerExempt(unit) then … end` around the bucketing loop.
  ⭐ Semantically the cleanest placement — habitat residents never enter a bucket at all. ⚠️ But a
  full-body replacement is the most clash-prone shape the pack ships and carries the `D14` stand-down
  question; `FIX_POLICY` §1 wants the least invasive thing that works.

### 3d · ⛔ What will NOT work — do not rediscover this

**Filtering the list the picker returns.** Habitat residents are bucket 1, the first pick;
`GatherAvailableCargo` returns `false` on a short crew (`:196-199`); `Load` then loops
`while not succeed do Sleep(1000)` **forever** (`:124-130`), and expeditions reach `Load` with neither
`quick_load` nor `transfer_available`. ⇒ the unmodified original re-picks the same residents every
second and **the rocket waits on "Not enough Colonists" permanently in a colony full of eligible
people.** ⛔ That is the stall C95 judged negligible — this shape does not risk it, it manufactures it.

---

## 4 · What the fix must NOT do

- ⛔ **No migration, no save fix-up.** Forward-only: it changes who is eligible for a *future* draft.
  A habitat resident already away still comes home by the old path and is still re-homed. Claim
  nothing more.
- ⛔ **No reach into the asteroid lander.** If the hook can touch a player-chosen passenger list, it
  is the wrong hook.
- ⛔ **No reach into trade / supply / colony transfer.** `CargoTransporterNew` is a different class.
- ⛔ **No repair of the return path.** The owner declined it.
- ⛔ **No loud failure.** `FIX_POLICY` §2: if the predicate cannot be evaluated, vanilla behaviour
  survives unchanged and silently.
- ⛔ **Nothing from [C100](../bugs/C100.md).** Habitat residents walking out on their own is a
  separate, unruled defect ([ck188](../../PLAYTEST_CHECKLIST.md)). Finding more about it does not
  authorise touching it.

---

## 5 · Acceptance

⭐ **The owner has the save.** Ask what is in it before designing around it; do not provision.

- **Both habitat classes.** Naturalist and Micro-G both reach `MicroGHabitatBase` — prove one test
  covers both rather than assuming it.
- **The draft takes none of them.** With `SMRTest.Log.CrewDraft` armed (TestKit `acafc74`, a Kit-page
  arm/disarm button — ⚠️ arm it **before** the expedition is assigned, the gather runs once), the log
  shows the habitat residents absent from the returned list and the rest of the pool unchanged.
- ⭐⭐ **THE FILL LEG — the one that catches every wrong shape.** An expedition asking for N crew, in
  a colony holding N eligible non-habitat colonists, **departs with N**. ⛔ A rocket sitting on "Not
  enough Colonists" here is §3d's hang, not a scarcity result — check the colony before blaming the
  fixture.
- ⭐ **THE LANDER NEGATIVE LEG — the one that catches a too-wide hook.** A player-chosen asteroid
  lander passenger list containing a habitat resident **still carries them**.
- **The elevator leg.** Trade / supply / colony transfer drafts are untouched — show it, don't assume.
- **Fail-safe leg.** With the predicate made unevaluable (a colonist with no `residence`), vanilla
  behaviour survives and nothing is logged loudly.
- **Removal leg.** With the module removed, the next load behaves exactly as vanilla.
- **Restore leg** (specific to 3b): force an error inside the picker and prove the global came back.
- **Clean boot:** `applied` line present, no error-shaped lines, exit 0.

⚠️ **A FIX INVALIDATES ITS OWN TESTS.** Base every harm leg on the **pre-fix** body and re-run the
**whole** suite, not only the changed leg.

⚠️ Any behavioural or assignment-quality claim must state the fixture's scarcity, fleet, density and
layout and report **that colony's** measurement. ⛔ Name every setup mutation; reject one that
intersects the draft — ⚠️ a colony-wide employment reassignment is exactly such a mutation, and is
`EF-104`'s leading hypothesis for its unexplained observation.

⭐ **One free reading while you are in there, and it is not this fix's job to repair.** Under-supply
an expedition deliberately and **read the rocket's panel**. `EF-104` records that the line setting
`colonist_summon_fail` dereferences a nil on exactly that path, byte-identical since 1.0.7; "Not
enough Colonists" showing proves it executed, a blank panel on a waiting rocket is the tell. ⛔ Report
it, do not fix it here.

---

## 6 · Deliverable and stop conditions

**Deliverable.** Module in `Code/`, registered via `SMRFixPack.Register`, gated via
`SMRFixPack.Require` naming every `(class, method)` pair it installs on or captures from.
`items.lua` updated. Build report at `docs/agent/reports/C95_HABITAT_DRAFT_BUILD.md` carrying the
caller/inheritor count and how it was taken, the hook choice and its cost, the restore proof, and
everything that did not work.

C95's front matter **and** body heading tag updated together — ⛔ a status flip must hit both or
doccheck goes RED, and a status change belongs in the **title** too, because `INDEX.md` renders title
+ status and nothing else. ⛔ Do not promote past what was witnessed.

Label every claim **SOURCE / MEASURED / INFERRED**, keep a **Not opened** list, say what each
refutation depends on. `python tools/doccheck.py` GREEN before committing; commit with a pathspec
after re-checking `git status` for a peer's uncommitted work.

**Owner-facing.** Playtest recipe on `docs/PLAYTEST_CHECKLIST.md` with its `ck` marker (⛔ `### <date>
— <n>: <title>` plus the marker comment; sub-headings `####` — an `##` heading silently closes
"Decisions waiting on you" and orphans every item below it; verify with the item count, not the gate
colour). Fix-list row and its judgment-call reasoning drafted from the owner's own wording on C95.

**Stop conditions — permission to report rather than push on.** Stop and report if: the
caller/inheritor count contradicts §3b; something on the picker's path yields, so the swap is not
atomic; no hook can be expedition-scoped without reaching the lander; the predicate cannot be
evaluated where the draft runs; or the fill leg fails.

**What may NOT be claimed.** ⛔ Not "habitat residents can no longer go on expeditions" — the player
can still send them by hand. ⛔ Not "colonists already away are rescued" — forward-only. ⛔ Not
"confirmed live" on a desk result. Where the evidence will not carry the claim, **write the narrower
true statement.**

**Lifecycle.** One-off. When it reports, `git rm` it and delete its `prompts/README.md` row **in the
same commit**. ⛔ No tombstone row.

---

## 7 · Derived facts and falsifiers

| fact | how it was measured | at | falsifier |
|---|---|---|---|
| Build + test authorised; C96's half of ck185 still open | owner's words, 2026-09-16, recorded on the checklist | this rewrite's commit | a later owner ruling. ⛔ No source read overrides it |
| Repair shape, classification, scope and public framing are the owner's | their own words quoted on C95, 2026-09-15 | C95 at this commit | a later owner ruling |
| `IsKindOf(unit.residence, "MicroGHabitatBase")` is vanilla's own habitat predicate | `IsSuitableWorkplace`, `Workplace.lua:1446-1462` | game 1.1.0.403908 build 24995074 | `grep -n "MicroGHabitatBase" <Src>/Lua/Buildings/Workplace.lua` |
| Both habitats reach `MicroGHabitatBase`; the leaf class alone does not cover both | `__parents` chain in `NaturalHabitat.lua:1-2` and `BuildingTemplate/MicroGHabitat.generated.lua:5` | same | `grep -rn "DefineClass.NaturalHabitatBase" -A3 <Src>/Lua` |
| The connected-domes flags are player-toggleable policies, so unusable as a predicate | 1.0.7 tree: `Dome.lua:849`, `:883`, `Community.lua:147` → `TogglePolicy` | 1.0.7.396349 archive | re-grep both trees; body in `EF-103` |
| `FilterColonistsByTrait` is a global called once per bucket, with 5 sites across 3 gathers | `grep -rn "FilterColonistsByTrait" <Src>/Lua <Src>/CommonLua <Src>/DLC` | 1.1.0.403908 | re-run the grep; a different count changes the scoping argument |
| `RocketExpeditionBase` calls the base gather by explicit table read | `RocketExpedition.lua:496-497` | same | read those two lines; a change to `self:` dispatch breaks the hook |
| `CargoTransporter:Load` has two call sites, so the base gather is expedition-only in practice | `grep -rn "CargoTransporter\.Load\|self:Load(" <Src>/Lua <Src>/DLC` | same | ⛔ **INFERRED — re-count before hooking** |
| Nothing yields on the picker's path, so a scoped swap is atomic | no `Sleep`/`WaitMsg`/thread creation in `CargoTransporter.lua:220-292`; callees are pure reads | same | ⭐ re-grep that range and check any callee added since |
| A short crew is a permanent wait, not a smaller crew | `CargoTransporter.lua:196-199` + `:124-130`, `RocketExpedition.lua:536` | same | if `Load` gains a retry cap, re-price §3d |
| `SMRTest.Log.CrewDraft` is the reach control | TestKit `acafc74` | TestKit HEAD | `git -C C:/Dev/SMR-BugFixPack-TestKit log --oneline -- Code/90_Loggers.lua`; ⛔ **never run in play** — treat its output as unwitnessed until this sitting |
| Module and fix counts are not inputs to this job | no acceptance clause depends on a stored total | — | emit with `python tools/doccheck.py --emit-counts` rather than writing a number |

⚠️ Run `python tools/doccheck.py --emit-fingerprint` and re-derive only the groups that moved. ⛔ Many
older citations point into a tree the 1.1.0 auto-update overwrote.

---

## 8 · Live todo list — change it as you go

Mark item 1 `IN PROGRESS` and the rest `PENDING`; thereafter keep **exactly one** unfinished
commit-and-verify unit in progress, expand a stage as soon as it splits, mark each complete when it
finishes, and rewrite the list when reality changes. ⛔ Never carry several commits behind one
checkbox or update the list only at the end. Put stable results in the item text — the owner reads
this list to decide when to step in.

- [ ] 1. Orient; ask the owner what is in the test save before designing the legs
- [ ] 2. Re-derive §3b's caller and inheritor counts; record the count and the command
- [ ] 3. Prove the no-yield property on the picker's path; record how
- [ ] 4. Build the predicate + the scoped wrap, with the `pcall` restore
- [ ] 5. Probe sweep per `WORKFLOW.md` "Probe hygiene", recorded in the measurement commit
- [ ] 6. `items.lua` + `Require` block; clean boot witnessed
- [ ] 7. Owner sitting: `CrewDraft` armed, the **fill leg**, the **lander negative leg**
- [ ] 8. Elevator leg, fail-safe leg, removal leg, restore leg — re-based on the pre-fix body
- [ ] 9. Free reading: under-supply an expedition, read the panel, report (⛔ do not fix)
- [ ] 10. Build report; C95 front matter + heading tag + title updated together
- [ ] 11. Checklist recipe with its `ck` marker; fix-list row drafted from the owner's wording
- [ ] 12. Your own findings, including everything that did not work
