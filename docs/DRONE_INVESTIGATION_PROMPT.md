# Fable investigation prompt — drone task assignment / Hub Extender (kickoff, 2026-07-27 late)

Paste everything below into a fresh Claude Code session (Fable). This is a
**GAME-FREE INVESTIGATION leg**: static source analysis only. Do not launch
the game, do not edit any loadable code (`Code/` in either mod), do not touch
metadata. Findings land in docs and get committed; any actual fix is a
decision for the user AFTER the verdict is in.

**Coordination note:** a separate playtest-standby session (see
`docs/FABLE_NEXT_PROMPT.md`) runs at other times against this same repo. Start
with `git log --oneline -5` + `git pull` and make sure you're building on the
latest commits; keep your commits small so the two threads interleave cleanly.

---

You are continuing the Surviving Mars: Relaunched "Community Fix Pack"
(dev repo `C:\Dev\SMR-BugFixPack`, git). Game source, READ-ONLY, never modify:
`A:\SteamLibrary\steamapps\common\Project Spark\ModTools\Src`.

**First, read (in order):**
1. `docs\STATUS.md` — the "Key technical facts" engine-facts list (governs all
   analysis; e.g. file-locals invisible to wrappers, GameInit deferred,
   IsValid falsy for pure-Lua objects).
2. `docs\BUGS.md` — the **"Not yet swept (follow-up targets)"** section, the
   `DroneControl.lua` bullet: it carries the FULL evidence package this
   session exists to chase. Also read the F50, F55 and F58 entries (the
   pack's existing drone-domain knowledge) and F72 (a prior "predicate scans
   the wrong set" precedent).
3. `docs\FIX_POLICY.md` — binding if you sketch a fix.

## The problem (first-hand, live 2026-07-27, screenshots on file)

In the user's colony, with a large-range Drone Hub plus many drones and
overlapping hub coverage:

- The **four drones physically closest** to a malfunctioning building and a
  Polymer storage each read `command = "Idle"` — genuinely idle in the
  assignment layer, NOT wedged mid-command, NOT F55-unreachable-cached.
- Meanwhile a hub near the SECOND dome, much farther away, serviced
  everything — slowly. Work backed up; a PolymerPlant was caught at
  `performance = 0` with `auto_performance = 50` (transient disable).
- The idle drones are correctly parented: `command_center` = **DroneHub,
  handle 2608** (a regular hub near the idle cluster). The user verified **no
  RC commander was broadcasting a zone** nearby (rover niche ruled out).
- **User hypothesis from original-game experience: the Drone Hub Extender
  (repeater) is the trigger** — the pattern became prevalent once extenders
  entered a colony, and this colony runs them. Plausible mechanism: an
  extender stretches a far hub's effective service area over ground a nearer
  hub already covers, and request→hub matching is extender-transparent
  (first-registered-wins or distance-blind), so the far fleet captures work
  the near fleet should take.
- Performance also **degrades** as hub range × drone count grows, worse with
  multiple hubs in range of each other (original-game pattern, user reports
  it surviving into Relaunched).

## The mission — answer these from Src, with file:line evidence

Primary files: `Lua\Buildings\DroneControl.lua` (hubs + extender machinery),
`Lua\Units\Drone.lua` (idle loop / work pickup). Extender data:
`Lua\BuildingTemplate\DroneHubExtender.generated.lua`,
`Lua\XDef\customDroneHubExtender.generated.lua`. Requests:
`CommonLua\TaskRequest.lua` and wherever task_requests register with hubs.

1. **How does a task request reach a drone?** Per-hub queues or a global
   pool? Push (hub assigns idle drones) or pull (idle drones scan)? Where is
   the actual match loop, and what orders it (priority, distance, insertion
   order)?
2. **When a building sits in the range of TWO hubs, which hub's fleet gets
   its request?** Is there any handoff/stealing when one hub's drones are all
   busy and another hub's drones idle in range? (This is the observed
   failure.)
3. **Where does the Hub Extender plug in?** Does it extend the hub's
   request-REGISTRATION radius, its drones' work radius, or both? Does
   extender-mediated coverage look identical to native coverage in the match
   logic (the extender-transparency hypothesis)?
4. **Why do idle drones near work stay idle?** Trace `Drone`'s idle command:
   does an idle drone ever look for work itself, or only wait to be assigned?
   If it scans, what set does it scan (its own hub's queue only?)?
5. **The performance angle:** what per-tick/per-update work scales with
   range × drones × requests? Identify the hot loop(s) that would degrade
   with big overlapping hubs (the user's other observation).
6. **Reconcile with the evidence:** does the traced mechanism reproduce
   exactly what was observed (near fleet idle, far fleet over-committed,
   transient building disables)? If the extender is NOT required for the
   failure, say so and identify the real trigger.

## Deliverables (all committed, small commits as you go)

1. **A verdict** on the `DroneControl.lua` bullet in BUGS.md: defect(s) with
   file:line proof → file new F-number entry/entries (index row + detail
   entry, severity called per the existing scale); design-working-as-intended
   → record that verdict on the bullet with the trace. Partial answers are
   fine — record exactly what is proven vs suspected.
2. **A fix sketch** per FIX_POLICY §1 (least-invasive ranking) for each real
   defect, with a risk assessment — drone assignment is deep shared machinery
   (F50/F68/F71 territory); say explicitly what could break. DO NOT build it
   this leg; the build is a user decision.
3. **A live instrumentation plan** for the next attended sitting: exact
   console wrappers/reads (the F12/PT-38 timestamped-wrapper pattern; console
   sandbox rules and the verified command table are in
   `docs\PLAYTEST_CHECKLIST.md`) that would confirm the traced mechanism on
   the user's colony — hub 2608's queue vs its drones' states at a
   starvation moment. Repro recipe already banked on the bullet: hub A +
   hub B far apart, extender bridging B into A's area, break something in
   A's yard, watch which fleet answers.
4. `docs\STATUS.md` gets a short investigation-leg section; the BUGS bullet
   is updated in place. If the verdict spawns build work, add it to the
   FABLE_NEXT_PROMPT board as a USER-DECISION item, not a queued build.

## Hard rules

Never modify the game directory. No loadable-code edits this leg (docs-only
commits). STATUS.md engine facts govern; verify every claim against Src at
the cited file:line before writing it down (prior sessions falsified plenty
of plausible hypotheses — record falsified branches too, they are evidence).
Commit with
`git -c user.name="SMR-BugFixPack" -c user.email="154917955+catt144@users.noreply.github.com"`,
push when done, and end with a summary of verdicts + what needs the user.
