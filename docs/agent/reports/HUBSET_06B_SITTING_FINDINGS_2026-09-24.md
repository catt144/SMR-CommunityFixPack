# hubset 06B — desk findings after the only sitting

## Must_Read_Header

Reader: the owner deciding C111, C114 and C117, and link 99 auditing the evidence.
This is an unattended investigation, pending 99's independent audit; it changes no
entry status. The owner's one-sitting ruling stands. No further sitting is built
or requested here. C42, F127 and the VacuumWalks pins remain desk-verified.

## Answers at a glance

- **C111:** the wrapper rejects the game's `emigration_dome=false` default.
  The desk reproduces the miss and the repaired hit. That defect is proven;
  attribution to the exact 07 call is inferred because its field was not logged.
- **C114:** 07 cannot identify the native branch or explain its non-reproduction
  uniquely. The desk distinguishes a distant hub case needing the fix from a
  nearby-community case already accepted by native code.
- **C117:** the timeout diagnosis holds under the logged speed assumption.
  The fix is **desk-verified; unobserved in play**. No other traced 07 watch
  loses a verdict from this same timebase issue.

## Work and evidence receipt

- Complete: desk investigation and C111 repair committed and pushed on `hubset`,
  **`e5fc0c6`**. C114 gained a desk control; its module was not changed.
- Complete with this main close-out commit: report, 99 outbox and 06B retirement.

Main started at `c9b6e3d`. `git log --oneline -10`, `git pull` and
`git status --short` confirmed an up-to-date, clean tree. The corresponding
hubset log/status confirmed `7cf48a2`, clean; TestKit was `66288da`, clean.
The source below is always **archived build 1.1.1.405907**, at
`B:/Dev/SMR/SMR-Shared/SMR-SrcArchive/1.1.1.405907/Src`.

[The command receipt](../../archive/logs/hubset06b_desk_source_2026-09-24.txt)
contains each named command's exact invocation, working directory, output and
exit status. Command IDs below refer to those executable commands, not to an
unrecorded investigation. MEASURED means a log observation or a named desk run,
as specified; SOURCE means the archived Lua or TestKit definition; INFERRED
means the conclusion connecting them. Every substantive answer below names its
falsifier. The receipt reconciles harness summary totals against their named
PASS members. Paired `[mod] [SMRTK]` and `[SMRTK]` lines are duplicate sinks.

## Q1 — C111: an unset destination is false, not just nil

**SOURCE (commands `S-C111`, `S-transport-wait`).** Archived
`Lua/Units/Colonist.lua:106` declares `emigration_dome = false`; `:329`
also resets it to false. Own-home `Transport` does not assign a destination
there (`:3963-3970`). The native getter and hyperlink methods accept false
through Lua's ordinary truth test (`:4437-4440,4462-4465,4672-4716`).
The old wrapper instead required
`self.emigration_dome == nil or self.emigration_dome == task.dest_dome`.
A false value fails both sides. Falsifier: a different archived default or an
own-home Transport assignment replacing false before the getter.

**MEASURED on the desk (commands `C111-old`, `c111_fixed`,
`c111_absent`).** The extended `tools/desk_c111_rescue_text.py` extracts
the shipped class defaults as well as the native getter and hyperlink bodies.
With `--module-revision 7cf48a2`, both an inherited false and an explicit
false still return T 4333, while a synthetic nil-valued input says returning.
The repaired module says returning for those false inputs too. Removing the
fix restores the native wording and fails the own-home demand. Relocations,
foot migration, conflicting emigration targets, non-rescue tasks, dreaming
and the destination link retain their tested native behavior.
Falsifier: the old module already changes the false input, the new one misses
it, or a native-preservation control changes.

**MEASURED live / INFERRED cause (commands `L-C111`, `S-C111`,
`C111-old`).** Segment B confirms `RescueReturnText: applied`, active at
boot, and subject 2000010346 returning T 4333 with home and displayed destination
both GeoscapeDome(1896). That display uses `emigration_dome or task.dest_dome`;
it therefore hid precisely the false/nil distinction the wrapper mishandled.
This is a sufficient, source-backed cause of the observed miss, not a direct
measurement of that subject's field. A dreaming native getter would return
T 6930, so dreaming does not explain T 4333 under the archived getter.
The desk dispatches through a class-indexed instance; it does not establish
retail class flattening or that subject's method identity.
Falsifier for the live attribution: a contemporaneous read showing
`emigration_dome` equals home and the installed wrapper was bypassed.
The missing discriminating reading is the field's raw and resolved values,
`dreaming`, and instance/class getter identity at that same call. Stop 1
applies to recovering that exact live cause; no further game work was done.

**SOURCE / MEASURED repair (command `c111_fixed`; inspect
`git show e5fc0c6 -- Code/Fix_RescueReturnText.lua`).**
The guard now uses `not self.emigration_dome`, accepting false and nil.
This remains FIX_POLICY §1.4's synchronous chained getter wrapper: a data
change to the shared command string cannot distinguish rescues from actual
relocations, and no additive event or public command-table entry supplies that
per-colonist distinction. Existing Require checks, native-result ID guard and
MANIFEST remain; `c111_pins` verifies the pins. No saved field, movement
command, thread or blocking frame was added (§3a layer 3).
Falsifier: the commit changes anything beyond the guard and its explanatory
comment, or the pinned/behavior controls fail. The existing
`Untranslated("Returning to Dome: ...")` wording still needs the owner's
approval. A fresh Lua runtime is a getter-reload control, not save serialization
or retail rendering.

**What the owner's choices cost and ship.** Keeping the repair ships the
corrected guard with the one release, after audit and wording approval, with
no successful play claim. Dropping C111 removes its wrapper and registration
before release and retains native “Moving to a new Dome” wording. Holding
C111 holds the one-release decision unless the owner changes membership.
The re-fix is already built; it remains at most fixed-pending-play in evidential
terms, with the entry unchanged and no second playtest in this chain.

## Q2 — C114: the recorded outcome does not identify an access branch

**MEASURED live (commands `L-watch`, `L-reporter`,
`L-reporter-task`).** 07's main hub and flight follow events both say
`booked=false ended=safe`. The hub subject was 2000015055, holder
PassageHub(2026), with hub-to-home distance 29; the mid-spoke subject was
2000023141 on Passage(4035), with holder and marker absent at selection.
Its distance was not logged. By contrast, the reporter's earlier readings
show 2000010336, 2000010369 and 2000022849 holderless and hub-marked, with
access false at distances 24, 25 and 28 respectively. Earlier `SMRCOL`
rows for those same handles name Brussels as both home and task destination.
These are different subjects and moments, not interchangeable fixtures.
Falsifier: a booking or unsafe end for either 07 event, or true access at the
reporter's cited Transport readings. Later successful access readings are
preserved in the receipt and do not refute the earlier state.
The [field report's §7](HUB_FIELD_FINDINGS_2026-09-24.md) also corrects its
configuration claim: the earlier runs compared Passage Network off/on with
other mods present, not a fully unmodded control.

**SOURCE / INFERRED limit (commands `S-C114`, `S-rescue-final`,
`K-C114`, `L-watch`).** The exact native branch for either 07 subject
is **unknown**. Archived `ColonistTransport.lua:270-299` can accept current
dome, nearest community, home community or the final radius. The home-community
branch at `:288` is conditional on reaching that community; home identity
alone does not grant access. `SetCommand` also has train and home-route
alternatives (`:422-471`). TestKit `80_AgentSlots.lua:553-626` polls
booking and outcome, not the synchronous access decision. Even “no booking”
is limited to what those polls saw. At the recorded hub position, 29 exceeds
the nominal 20-hex fallback, but the query's actual position and other inputs
are absent. Falsifier: an archived access-call trace for those handles naming
the branch and its inputs. None is present in the instrument's output shape.

**Stop 1, exact missing reading.** To settle the branch retrospectively would
require a record at the same subject's `SetCommand/HasLocalAccess` call:
destination, returned result, current dome, holder and position, nearest
community, both community predicates, and any train/home route selected.
This report stops that part of Q2 at unknown; it does not authorize obtaining
the reading now.

**MEASURED on the desk (commands `C114-desk`, `C114-suite`).**
`python -B tools/desk_c114_sitting_findings.py` uses the archived native body
and the actual hubset wrapper:

| Explicit fixture | Native access | Fixed access |
|---|---|---|
| Holderless, marked, physically on a connected hub; home at 24, 25 or 28 hexes; no nearby community | false | true |
| Standing on that hub; home at 29 hexes; no nearby community | false | true |
| Same hub position but no holder/marker/flight identity | false | false |
| Last home connection removed | false | false |
| Nearby community within range, with home in its cluster | true | true |

The nearby-community control confirms a native bypass is possible, without
attributing it to 07. The existing suite also exercises native Idle rescue
booking with and without the wrapper. Falsifier: any table result differs,
or the existing fix-removed booking control ceases to discriminate.

**SOURCE / INFERRED reach (commands `S-network-final`, `S-C114`,
`L-watch`, `L-reporter`, `C114-desk`).** The connected-home shape uses
native tables: `Passage.lua:1593-1601` maintains `hub_domes`, and
`Buildings/Dome.lua:678-705` includes the attached dome itself in its network.
07 observed a holderless, marked hub dump; the reporter observed distant marked
false-access subjects. Combining those conditions is a source-supported
conditional play case, not a measured reconstruction of the reporter's exact
hex/topology. No single cited record establishes all inputs simultaneously.
The desk establishes access widening on that real structural shape; it does
not establish game path choice, successful entry, or the exact reporter
subjects' eligibility for the wrapper. Falsifier: a native constraint preventing
that combination, or the needed connection/physical-hub identity absent at the
relevant moment. The evidence does not support declaring the defect impossible;
neither does it support “C114 works in play.”

**What the owner's choices cost and ship.** Keeping C114 ships its existing
guarded access widening with conditional desk evidence, subject to 99's reach
and routing audit. Dropping it removes that widening before release; the
reporter's measured false-access rescue symptom remains unexplained by 07.
Holding for a unique live explanation delays the one-release decision and
would need a new owner ruling to permit another sitting. There is no new C114
re-fix supported by this investigation.

## Q3 — C117: the watch expired before the expected demolition boundary

**MEASURED live (commands `L-C117`, `L-watch`;
arithmetic command `C117-arithmetic`).**

| Segment | Arm game time | Timeout game time | Elapsed game ms |
|---|---:|---:|---:|
| A, main | 89514639 | 89605007 | 90368 |
| B, hubset | 89472236 | 89562604 | 90368 |

Both events say `drain_seen=false ended=timeout`. Both RunUntil arms log
factor 128000. The arithmetic command subtracts each pair independently and
checks equality. Falsifier: a different endpoint, factor or recorded drain
witness in those events. The factor was logged at arm, not continuously.

**SOURCE / INFERRED diagnosis (commands `S-C117`, `S-const`,
`S-drain`, `K-C117-corrected`, `C117-arithmetic`).**
`Demolishable.lua:102-117` sleeps 1000 game ms and subtracts
`min(1000, 1000*1000/GetTimeFactor())` from a countdown initialized to 5000
(`Lua/_GameConst.lua:114`; `Demolishable.lua:17,41`).
Only afterwards does `:133` call `OnDemolish`, which sets
`hub_draining` at `Passage.lua:1170`.
At constant factor 128000, ordinary fractional arithmetic gives 7.8125
countdown ms per tick and **640000 game ms** to finish; the command reconciles
640 ticks back to the full countdown. TestKit `:769,776` grants only three
game hours. This confirms 07's diagnosis under the stated speed/countdown
assumption. It does not directly measure the live countdown or prove that
`OnDemolish` never ran between polls.
Falsifier: a live zero countdown/drain before timeout, a different initial
countdown, or speed changes sufficient to complete it within the window.

**SOURCE / MEASURED scope of other watches (commands `K-C117-corrected`,
`K-C114`, `L-watch`, `S-transport-wait`).**
The rescue watch has a six-game-hour deadline and ended with
`timeout=false`; the fired-worker watch has a four-game-hour deadline and
each follow ended `safe`. Hub arrival, mid-spoke and busy-spoke are state
triggers without those expiry conditions. The native transport pickup wait
uses `GameTime` (`Colonist.lua:4000-4004`). No other traced 07 watch
awaits this real-time demolition countdown. Falsifier: another awaited
real-time-gated transition exceeding its game-time deadline, or a supposedly
state-completed event actually scored at timeout. This is scoped to the
07 watch definitions and traced outcomes, not every engine wait.
It voids no additional C115 P2, C116 P6 or R1-R6 HELD reading. C115 P1 and
C116 P5 retain their existing NOT_SAMPLED limits.

**MEASURED desk / SOURCE limits (command `C117-desk`).**
`python tools/desk_c117_hub_salvage.py` passes its native-body controls:
an in-flight unit keeps the hub endpoint until arrival, a removed-fix control
takes the outside branch, and new entrants respect the live-sibling and
native ClearPath contracts. Its scheduler, movement and pathfinder seams
are fixtures. It does not run the real demolition countdown, establish
traffic at that boundary, simulate the real pathfinder, serialize a save,
or prove a player reaches the chosen interleaving.
Falsifier: the removed-fix branch becomes indistinguishable or the native
decision controls fail. Supported wording: **desk-verified; unobserved in play**.

**INFERRED instrument correction, description only (commands
`K-drain-boundary`, `S-drain`, `C117-arithmetic`).** A corrected watch
would record speed and countdown, wait for demolition/drain state with a
compatible bounded timeout, and distinguish canceled, stalled and completed
demolition. It would establish a hub-bound in-flight subject at the actual
drain boundary before scoring the endpoint race. The current instrument
snapshots at the first poll seeing `hub_draining` (`:700-704`), which can
be later than entry; a busy spoke at the earlier salvage toggle does not
guarantee that later sample. Traffic can leave during the countdown.
Falsifier for an unsampled result: a boundary witness with a qualifying
in-flight subject and corresponding arrival/disconnect records.
This is an additional sampling limitation for 99, not a corrected slot build.

**What the owner's choices cost and ship.** Keeping C117 ships its existing
conditional drain repair with the desk-only limit stated, after audit.
Dropping it retains native disconnect-before-arrival behavior in the risky
interleaving. Holding it holds the one-release decision. Rebuilding the
instrument would serve a further sitting, which the owner has not authorized;
none was built, preloaded or requested.

## Audit handoff and limits

The [99 inbox](../prompts/hubset/99_AUDIT_high.md) owns this report until
independent audit. Pointers in C111, C114 and C117 remain deferred until that
audit; their entries and statuses were not changed.

Drift routed to 99: C111's nil-only original desk fixture masked the false
sentinel; 07's displayed destination did not prove the wrapper gate passed;
C114's precise native branch is absent from the evidence; and C117's long
countdown can empty the chosen traffic before the required boundary.
None of these findings undermines C115/C116 or the shared physical on-hub
test. The former HELD observations keep only their original narrow scope.

Validation: the command receipt holds the current and negative C111 controls,
C114 controls, C117 controls, C111 pins, parse result and declared-VOID 07
rehearsal. Hubset doccheck and its commit hook were GREEN; only the intended
tool-catalog row changed during regeneration. Main's commit hook verifies the
documentation after staging the prompt retirement (an unstaged deletion remains
in doccheck's tracked-file inventory). No game ran, no save was read,
no junction was repointed, and no TestKit file changed. Retail C111 dispatch,
rendering and serialization; the exact C114 call state; and live C117 timing
remain unobserved here. The A6 oxygen screenshots were not opened: the
recorded C114 comparison did not depend on them.
