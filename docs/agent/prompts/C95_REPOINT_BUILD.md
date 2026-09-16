# C95 re-point — the repair is attached to the legacy gather; move it to the one 1.1.0 uses

One-off, authored 2026-09-16 from an attended sitting that found the shipped module inert.
Tool-neutral. `git rm` this file **and its `prompts/README.md` row in the same commit** when
it has reported. Records: [C95](../bugs/C95.md) ·
[sitting](../reports/C95_SITTING_20260916.md) · [build](../reports/C95_HABITAT_DRAFT_BUILD.md).

Start with `git log --oneline -6`, `git pull`, `git status --short`. Authored against repo
HEAD `15a9b8e` and game 1.1.0.403908 build `6a91a190`; find this file's own commit with
`git log -1 --format=%h -- docs/agent/prompts/C95_REPOINT_BUILD.md` and re-derive only the
inputs in §5 that moved.

⛔ **The existing module is NOT broken and is NOT to be rewritten.** It is desk-verified and
attached to the wrong receiver. Your job is to move it, not to redesign it.

## 0 · How to work this

Open a live progress list before touching anything, one item per commit-and-verify unit,
exactly one in progress. Minimum shape: orient and staleness · §2 decision · §3 build ·
§4 desk suite extended · re-run the sitting with the owner · entry, report and checklist
close-out.

## 1 · What was measured, and what it means

The full chain is in the [sitting report](../reports/C95_SITTING_20260916.md); do not
re-derive it. The three load-bearing facts:

1. `SMRTest.Log.CrewDraft` wraps the **same** function the module hooks
   (`CargoTransporter.GatherAvailableColonists`). Armed and owned by the kit, it emitted
   **nothing** while the owner crewed and launched an expedition. The hooked function was
   never called.
2. The fixture's rocket is `UniversalZeusRocket` → `UniversalRocketBase`, whose parents
   include **`CargoTransporterNew`** and neither `CargoTransporter` nor
   `RocketExpeditionBase` (`Lua/UniversalRocket.lua:28-42`). The module's receiver guard
   cannot be true for it.
3. `CargoTransporterNew:GatherAvailableColonists` (`Lua/CargoTransporterNew.lua:235-280`)
   carries the same four-bucket structure and the same per-bucket
   `FilterColonistsByTrait` call at `:272`, with no residence exclusion.

## 2 · The decision you must make and justify — ⛔ not assume

**Which receivers does the repair cover?** Three candidate answers; pick one, state the
evidence, and record it in the entry:

- **New only.** Simplest. Correct if the legacy path is unreachable in 1.1.0.
- ⭐ **Both** (leading candidate). The legacy body still ships and `RocketExpeditionBase`
  still exists; a save, a DLC path or a modded rocket could still reach it. Costs one extra
  hook of a design that is already written.
- **A shared filter applied at both call sites.** Least duplication, widest blast radius.

⛔ **Settle reachability by evidence, not by taste.** Ask specifically: can any rocket in a
live 1.1.0 colony still be a `RocketExpeditionBase`, and does `LanderRocketBase`'s own
gather (`Lua/Buildings/LanderRocket.lua:1149`, filter calls at `:1171` and `:1182`) need the
same treatment or is it the deliberate player-choice path the owner wants left alone?
⭐ **The owner's design intent is explicit and unchanged: the AUTOMATIC draft leaves habitat
residents at home; deliberate player selection must keep working.** Any receiver you add
must respect that line.

## 3 · The build

Keep the shipped design: filter **before each bucket's** trait selection so later buckets can
still fill the crew, never filter the returned crew (that strands fillable expeditions — it
is why `01eb453` corrected the original brief). Keep `IsAutoPickerExempt` keyed on
`IsKindOf(unit.residence, "MicroGHabitatBase")`, which covers both habitat types.

Carry over unchanged: the `SMRFixPack.Require` preflight, the swap-restore of the
`FilterColonistsByTrait` global through plain assignment (**not** `rawset`), the
`pcall`-and-restore-then-retry fallback, and the body pin. ⚠️ **The pin is now
insufficient** — it names `CargoTransporter:GatherAvailableColonists` only. Add a pin for
the new receiver's body so drift in *either* is detected.

⚠️ **Re-check the no-yield property on the new path; do not inherit it.** The New body calls
`is_colonist_reachable`, `GetConnectedCities` and `GetCityLabelWithConnected`, which the
original analysis never read. The global swap is only safe across a non-yielding call.
⛔ If any of them can yield, the swap approach is unsafe there and you must say so rather
than ship it.

⛔ **`Require` must not fail the whole module when only one receiver is present.** A guard
that hard-fails on a missing legacy class would turn a working repair into a dead one.

## 4 · Desk suite

Extend `tools/desk_c95_habitat_draft.py` rather than starting over; its 19 legs and their
falsifiers still hold for the legacy receiver. Add for the new one: both habitats excluded ·
full crew across buckets from ordinary candidates · the `cargo_request_passengers` pool
branch **and** the `GetCityLabelWithConnected` branch · the extra liveness test
(`IsDead` / `CanChangeCommand`) · exact global restore on success and on error · a
post-filter mutant that must be rejected · a scarcity case where the expedition legitimately
cannot fill. ⭐ **A fix invalidates its own tests:** base every harm leg on the pre-fix body
and run the whole suite, not only the new legs.

## 5 · Derived facts and falsifiers

| fact | how measured | falsifier |
|---|---|---|
| the logger and the module share a target | `sed -n '471,479p'` TestKit `Code/90_Loggers.lua` | read it |
| the logger emitted nothing while a crew launched | `grep -n "CrewDraft" <log>` on `Mars.exe-20260916-12.01.37-6a91a190.log` | re-grep that log |
| Universal rocket parents exclude both legacy classes | `sed -n '28,42p' Lua/UniversalRocket.lua` | read the parent list |
| the Universal rocket runs expeditions by type | `grep -n "Expedition" Lua/UniversalRocket.lua` (`:6`, `:1688`, `:1729`) | read those lines |
| the New gather repeats the defect | `sed -n '235,280p' Lua/CargoTransporterNew.lua` (`:272`) | read the body |
| the module is deployed and matches the repo | `diff` of the appdata mod copy against `Code/` | re-run the diff |

⛔ Volatile values — log paths, error counts, doccheck numbers — are read with a command
every time, never quoted from this file.

## 6 · Acceptance

⭐ **The owner's fixture is already prepared** (save `lD1jaGcMJOxaiFcU`, Naturalist Habitat
with 5 residents, rocket on the pad, expedition ready), so the re-run is cheap. Do not ask
for a new colony. Run the **probe-sweep step** first per `WORKFLOW.md` § Probe hygiene.

Re-run the same sitting, and this time **the logger must produce a trace** — that is the
first acceptance gate and its silence is what failed this round. Then: habitat candidates
present in the eligible pre-fix pool, absent from the returned crew, crew filled from
ordinary colonists, expedition departs. Plus the legs checklist 189 still holds: the
player-choice lander/elevator leg, the removal leg, and the EF-104 free reading.

⚠️ **Read the habitat's resident count before and after the launch** — the step this
sitting missed. It is the direct witness that the exclusion worked.

**Unwitnessed and to be declared, not dropped:** the **Micro-G** habitat leg, unless a
fixture with one appears.

## 7 · What may not be claimed

- ⛔ Not *"C95 is fixed"* until a live trace shows the exclusion firing on the path the
  owner's rocket actually uses. A green desk suite is what produced this round's false
  confidence.
- ⛔ Do not claim the legacy receiver is dead code without the §2 evidence.
- ⛔ Do not record 189 as satisfied from a desk result.

## 8 · Scope, read path and stop conditions

**Read these files:** `docs/agent/bugs/C95.md` · `docs/agent/reports/C95_SITTING_20260916.md`
· `docs/agent/reports/C95_HABITAT_DRAFT_BUILD.md` · `Code/Fix_HabitatExpeditionDraft.lua` ·
`tools/desk_c95_habitat_draft.py` · `docs/agent/FIX_POLICY.md` · `docs/agent/WORKFLOW.md`.
Look anything else up through `docs/agent/bugs/INDEX.md` and `facts/INDEX.md` by id —
⛔ never read either INDEX whole.

**In scope:** `Code/Fix_HabitatExpeditionDraft.lua` and its registration, the desk suite,
the sitting, the C95 entry, the reports, checklist 189.

**Out of scope, and finding it does not authorise fixing it:** the expedition **return**
homing (the owner ruled the draft exclusion instead, and the return path is C95's recorded
alternative, not this job) · C96, whose hold is untouched · C93's ranch work · any other
`CargoTransporterNew` defect you notice — file it.

**Stop and report rather than pushing on** when: §2's reachability question cannot be
settled from source; a callee on the new path can yield, making the swap unsafe; or the
re-run still produces no trace. ⭐ **"The sitting report was wrong about X" is a successful
outcome.**

⚠️ Peers share this tree. Re-check `git log` and `git status` before every write, stage exact
paths, commit with a pathspec (`git commit -F <msgfile> -- <paths>`), never `-a`. doccheck
GREEN before pushing.
