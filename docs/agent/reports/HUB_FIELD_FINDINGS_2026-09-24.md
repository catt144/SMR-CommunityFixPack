# TheGodUncle's save, read live: hubs, rescue rides and a centre-measured range (2026-09-24)

## Must_Read_Header

Reader: the owner, and the seat re-sweeping the migration cross-check with these facts. Every
number here is a console reading taken by the owner on the reporter's save, logged with an
`SMR*` tag; the two logs are archived at `docs/archive/logs/reporter_TheGodUncle_modsoff_*.log`
and `reporter_TheGodUncle_modson_*.log` (force-added past the `*.log` ignore, like the ck208 logs).
Source citations are the archived `1.1.1.405907` tree. The Passage Network 1.38 code that was read
is archived verbatim at `docs/archive/PassageNetwork_1.38_Code_PassageNetwork.lua`. The hub
source audit that this sitting tests is `MIGRATION_AUDIT_2026-09-24_D_hubs.md` (seat note,
claims cleared only where this file says so). Nothing here changes an entry's status.
Four statements below are corrected in §7 (appended 2026-09-24): the census, the control
configuration, the service override and the oxygen timer.

## 1 · The report and the colony

Steam, 2026-09-24, TheGodUncle: after 1.1.1 colonists "move to a new dome which is the same dome
they live in", go outside, "get stuck next to passages and on passage ramps" and suffocate;
removing passages, turning off mods, verifying files and reloading did not help. Fifteen other
mods, including Passage Network 1.38 and Dome and Extractor Range Extend.

Census on load (`SMRPOP`, both runs): **858 colonists, all resident in one Geoscape dome,
Brussels, radius 19 hexes**; ten other domes with zero residents, used for work and services;
six passage hubs. Constants (`SMRRANGE`): oxygen budget 120000, outside-work radius 20 hexes,
walk cap 40000, passage-ignore 120000, colonist speed 1000. All vanilla values.

## 2 · Two runs, same save

| run | mods | what it showed |
|---|---|---|
| mods-off (log `…12.55.27`) | pack v20 only | 264 colonists outside a dome or moving, all Brussels residents; **10 in a rescue shuttle ride to their own home**; 50 resting inside hubs; no entry failures, no migration journey, no Abandoned |
| mod-on (log `…13.07.16`) | pack v20 + Passage Network 1.38 | 163 such colonists; **12 rescue rides home**; same hub pattern; our vacuum-walk fix still `applied` |

Both runs: connection tables clean. `SMRNET` compared every dome's `connected_domes` against
real passages and hub links: **0 fake, 0 missing** in both runs. The persisted-residue hypothesis
for Passage Network is **refuted**.

## 3 · The chain, watched (`SMRWATCH`, mod-on run)

| colonist | first read | second read, about 150 s of game time later |
|---|---|---|
| 2000010336 | on hub surface (holder nil, marker 2026), 24 hexes from centre, access **false**, rescue task new | rescued; inside, VisitService |
| 2000010369 | surface, marker 1908, 25 hexes, access false, ready for pickup, shuttle assigned | at a workplace |
| 2000022849 | surface, marker 2692, 28 hexes, access false, ready for pickup, shuttle assigned | at a workplace |
| 2000011174 | **inside** hub 2692 (holder PassageHub, marker set), 12 hexes, access true, rescue task new | **outside, holder nil, marker nil, 21 hexes, access false, ready for pickup, no shuttle, outside for 71 s of 120** |

Reading, cleared on source: a colonist interrupted on a Brussels-side hub or passage is dumped onto
the hub surface with its hub marker kept (developer comment `Passage.lua:1147-1150`). Its next Idle
runs the `SetCommand` wrapper (`ColonistTransport.lua:382-503`), whose `HasLocalAccess` ends in
`HexAxialDistance(unit, dome) <= 20` measured to the **dome centre** (`:19-28`, `:293-299`;
`Workforce.lua`). For a radius-19 dome that band is one hex, so the hub at 24-28 reads unreachable,
and the wrapper books a rescue shuttle to the colonist's own home (`:461-471`) with the pickup at the
colonist's own position (`LRTransport.lua:106-111`). The colonist waits there up to one sol
(`_GameConst.lua:143`). The status line reads "Moving to a new Dome: Brussels" throughout (C111).

The fourth colonist is the death route: booked while inside the hub, it finished the crossing into
Brussels, where the marker is cleared (`Passage.lua:1235`), then walked back out through a dome door
to the pickup anchored at the hub, and the oxygen timer ran. A marked colonist never starts that
timer (`Unit.lua:469`); only a cleared one does. That is the hub audit's S2 route, now observed
once.

## 4 · Hub occupancy (`SMRHUBU`, `SMRHUBSET`)

Hub 2692 listed 71 units, **all with holder == hub, 0 invalid, 0 listed-but-elsewhere**; no
colonist anywhere carried a hub marker while outside a hub at that instant. Two reads of the hub's
member set about 500 s apart: 66 then 70 members, **4 handles in common, all four with a changed
command**. The hub is throughput on the one crossing between the Geoscape dome and three service
domes, not a holding defect. C42's and C99's stale-list shapes are **absent in this save**.

**S4 read (`SMRHUBOFF`, later in the mod-on run): not refuted, and leaning true.** Of the units
each hub listed as held, those standing farther from the hub than its collision radius (2309
units):

| hub | listed | beyond the radius |
|---|---|---|
| 1908 | 11 | 4 |
| 2026 | 11 | 6 |
| 2692 | 45 | 35 |
| 4113 | 3 | 2 |
| 11714 | 2 | 0 |
| 11985 | 1 | 1 |

Caveat: a hub's ramps may extend past its collision radius, so the decisive test is the hub's hex
footprint (`GetDomeAtHex`-style membership), not `GetDist2D`. Until that runs, "holder = hub carried
off the hub" stays a live hypothesis with this reading in its favour; if it holds, a rescued colonist
lands at home still "in the hub" and re-books, which is the audit's alternative chain for the
repeated rides.

## 5 · Passage Network 1.38, read (archived copy)

Three parts: `Dome:GetClusterDomes` and `Dome:IsInClusterWith` returned as the whole
`dome_network`; a `ReassignServices` override that swaps every dome's `connected_domes` for a flat
network list during the synchronous vanilla call (redundant on 1.1.1, whose body already iterates
`dome_network`, and harmless: no yield, tables restored, hash still matches); and two stray
`function Dome()` definitions that would replace the class global, which the live read `SMRDOME`
shows survive as a table because classes are rebuilt after mod code loads. The widening is live:
`SMRDOME2` read cluster 11 = network 11 against 9 direct neighbours.

The mod touches none of the hub, traversal, access or rescue code. Its effect is exposure: jobs and
services anywhere in the network mean more hub crossings per shift. It makes the access test pass
more often, not less, since the test loops over the cluster. **Not the cause, and not a trigger.**

## 6 · What this settles and what it opens

- **Symptom (a)** is C111, on the rescue-ride path, every time.
- **Symptom (b)** is the hub audit's S1 plus S2: centre-measured access, then a pickup anchored
  where the interrupt landed. Vanilla in every line; unchanged since 1.1.0. 1.1.1's new
  mass-interrupt source (switching a dome off kicks every worker en route, `Dome.lua:1905-1935`)
  is the best candidate for "after the update".
- **Symptom (c)** was not isolated in this save; C110 and C113 remain the source candidates.
- **The migration audit's C109** does not run here: no colonist had an entry failure. Its "vacuous
  if" condition, access failing, is what this colony hits instead.
- **New candidates to file** from the hub audit: S1, S2, S3, S5; corrections owed to C42, C99,
  C109, C111 as that note's §7 lists.
- **Owed measurements:** the S4 falsifier; the S2 pickup anchor read on a dying colonist
  (`transport_task.source_landing_site[1]` on a passage hex); the phase 2b controls still open.

## 7 · Corrections (appended 2026-09-24)

From the Codex [resweep](MIGRATION_CROSSCHECK_HUB_RESWEEP_2026-09-24.md). The coordinating seat
re-checked the first and third against the raw log and the archived 1.1.1.405907 source.

- **Census (§1).** "858, all resident in one Geoscape dome" holds for the mods-off run (OFF:735,
  :764). The mods-on run totals **868** (ON:623): Brussels 853, with 15 residents across ten other
  domes (Prague 2, Bern 1, Amsterdam 2, Tallinn 1, berlin 3, London 2, Paracelsus #1 1, Planck #1 3).
  The snapshots do not say which births, deaths or migrations made the difference.
- **Control configuration (§2).** Both runs loaded the pack, the TestKit, the Opt-In Pack,
  RailShaftDev and TrainHubDev (OFF:742, ON:380). This is a Passage Network off/on comparison, not a
  pack-only or unmodded control.
- **Service override (§5).** Not redundant. `ReassignServices` iterates `dome_network`
  (`Lua/Stats.lua:536-546`), but the helper it reaches, `PlaceServiceInConnectedDomes`, reads
  `home.connected_domes` (:375-386). Passage Network's temporary substitution therefore widens
  service-capacity distribution across the network, and restoring the tables does not undo the
  allocations. It remains outside the hub, access and rescue chain.
- **Oxygen (§3).** "A marked colonist never starts that timer" is too strong.
  `Buildings/Dome_Entrance.lua:71` sets outside regardless of the marker; a later marker-aware stop
  can clear it. The watched colonist had already lost its marker, so the chain stands.
- **`SMRDOME` (§5) and the startup dialog.** The read shows `Dome` is a table in game, after the
  class rebuild. It does not show what `Dome` was while mod code ran. On a rig where Passage
  Network's code runs before the pack's, VacuumWalks' load-time check (`Code/Fix_VacuumWalks.lua`,
  `has_110_helpers`) would see the stray function and decline with the dialog. In both runs here the
  pack loaded first (ON:95 before ON:136). Hypothesis, pending the owner's reversed-order sitting.
