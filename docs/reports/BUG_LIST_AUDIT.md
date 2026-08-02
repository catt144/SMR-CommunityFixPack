# Bug-list audit — tiering the tracker against external witnesses

**Run 2026-08-01 per `docs/archive/BUG_LIST_AUDIT_PROMPT.md` (one-off; consumed by
this delivery and archived with it). Game-free: nothing in `Code/` changed; the game installs were
read-only throughout.** Method: five parallel research passes (two player-report
hunts over Steam/Paradox/Reddit/YouTube/patch notes, one fix-author roster hunt,
one recovery pass for the six report-provenance entries whose quotes were never
recorded, and one full ChoGGi-corpus match + OG-vs-Relaunched code-identity pass
against a fresh clone), merged and **spot-verified against Relaunched Src before
anything was filed** — one agent claim was refuted by that verification (§7.3).

---

## 1. Verdict up front

| tier | count | entries |
|---|---|---|
| **GOLD** | **16** | F30 F44 F45 F46 F52 F55 F58 F65 F66 F67 F68 F70 F71 F73 F78 F81 *(F04 moved to BRONZE by the §9 addendum — its witness turned out to fit a different mechanism)* |
| **SILVER** | **25** | F01 F02 F03 F05 F06 F11 F16 F21 F35 F36 F37 F38 F40 F41 F43 F48 F50 F51 F53 F59 F60 F64 F69 F74 F76 |
| **BRONZE** | **30** | F04 F07 F08 F09 F12 F13 F14 F15 F17 F18 F19 F20 F22 F23 F25 F26 F27 F29 F31 F33 F34 F47 F54 F57 F72 F75 F77 F82 F84 F85 |
| **HOLD** | **0** | *(F49(a) briefly held; reclassified same day on owner challenge — §3)* |
| **NON-FIX (adjudicated)** | **12** | F10 F24 F28 F32 F42 **F49(a)** F49(c) F56 F61 F62 F63 F79 — hard "we are not fixing this" decisions with recorded grounds (§2.4); formalized as a first-class tier 2026-08-01 (owner) so they never muddy the maybe-BRONZEs |
| play-proven, exempt | 2 | F83 (PROVEN + A/B + tested), F80 (→ §4) |
| out of scope | — | F86–F88 (our own defects); D-entries (design, not defect claims); C-entries (leads, §4/§5) |

**Does anything in the shipped default-on set land in HOLD? NOTHING does —
the tier is empty.** Every default-on module is BRONZE or better, and every
BRONZE carries at least one hard tell from the challenge review's intent
list.

**Headline discoveries beyond the tiering:**

1. **A native Relaunched fix-modding scene exists and independently converges on
   our list.** GromGor's "Patch 1.0.7 No Disasters after Meteor Storm" describes
   **F81a's exact mechanism** ("After a meteor storm, one of the keys may not be
   removed, preventing further disasters from generating" — confirmed at code
   level in §9: he clears the same `g_DisastersPredicted` key our fix manages);
   his "Workshifts FixUp" repairs a *different, additional* workshift bug
   (→ C32 — and reading it cost F04 its GOLD, §9); Oxygenus's "Asteroid
   Rocket Waste Fix" (397 subs, the
   highest-subscribed Relaunched fix mod) is **F71**; and fredware's "Bug Fixes"
   (13 per-toggle fixes, **created 2026-07-31 — the day before this audit**)
   independently ships **F01, F74, F78/F81, and the F45/F48 track-demolition
   family**, plus seven fixes we do not have (§5).
2. **The Relaunched dev patch-note thread is a load-bearing witness corpus**:
   "Fixed drones endlessly moving resources between Landers" (=F68), "Fixed an
   issue where trains would endlessly transport some resources and not load
   others" (=F46), "Fixed an issue where train tracks would not transfer power
   if built in a specific order" (=F65 family), "Fixed the issue with Disasters
   (not starting/not ending/spamming notifications)" (=F78/F81 family), "Fixed
   several issues that could cause colonists to get stuck (sometimes
   indefinitely) while waiting for a train" (=F80), "Fixed homelessness,
   unemployment, overpopulation, and suffocation cases" (=F51-F60 family). A dev
   note fixing X is proof players hit X — and several of these recur in reports
   *after* the patch that claimed them.
3. **The retraction-risk pool behaved exactly as the prompt predicted.** No
   arithmetic entry (B1) gained contrary evidence. The two verdict corrections
   this audit itself produced were both **B3/reachability-shaped**: a false
   witness match on F31 (§4) and a corroboration claim on F34 that fell (§7.2).

## 2. The table

Sub-types: **B1** arithmetic/data · **B2** control-flow/reachability · **B3**
interface/affordance/intent. `UNREP` = UNREPORTABLE BY CONSTRUCTION (rule 4
exemption: latent-by-data, no player can ever report it; never HOLD on absence
of reports). Sources `[Sn]` in §8; **all quotes verbatim as machine-extracted**
(reporters' typos preserved). Game tags: **R** = Relaunched (Steam app
3215050), **OG** = original (464920). Provenance is the reachability audit's
verdict-table column (src-diff / player-report / mixed) plus `play` for entries
found at this project's own keyboard.

### 2.1 GOLD — Relaunched witness describes the symptom our mechanism predicts

Diagnostic verification retired; **implementation verification still owed**
(probe + one A/B leg) — all 17 already have probes; the ones not yet `tested`
owe their playtest as implementation (not diagnostic) checks.

| id | prov | witness (verbatim · source · game) |
|---|---|---|
| F30 | mixed | "My builder rover entombed itself and three other drones underneath an artificial lake." — Kudaku review, Nov 14 2025 [S2] **R** — incl. the constructor-is-the-victim detail our part (a) exempts |
| F44 | mixed | "If you place a single hex of track wrong and want to delete it you delete the entire track." — Kudaku review [S2] **R** |
| F45 | mixed | "I can I select the track, but when I click delete nothing happens" — A Lamp, Feb 26 [S3] **R** (silent no-op = the sort-error signature); + dev note "track segments would become undemolishable" [S5] |
| F46 | mixed | "Trains will run back and forth with empty loads or not empty their load." — Bored Peon, Dec 2 2025 [S4] **R**; + dev note "trains would endlessly transport some resources and not load others" [S5] |
| F52 | player-report | "All of them are outside running towards a dome when they run out of oxygen and sufficate." — Random Casualty, Aug 2019 [S6] **OG**; "They still have not bothered to fix the colonists walking from one distant dome to another and suffocating" — Rhodith review, Nov 14 2025 [S7] **R** |
| F55 | player-report | "i got atmos to 100% … now my drones are … trying to drive directly to the buildings, but their collision is still treating the dome as existing. all my buildings are breaking down and they are not getting repaired." — gjscott1996, Nov 15 2025 [S8] **R** |
| F58 | mixed | "It appeared that they reserved it (I see the teal shadow of a reserved slot), but never actually claimed it fully." — Witcher William, Nov 10 2025 [S9] **R** — mechanism-specific (the reservation itself observed) |
| F65 | src-diff | "the tunnels do not connect power as the say they do." — freakaholic15, Dec 4 2025 [S10] **R**; + dev note "would not transfer power if built in a specific order" [S5] |
| F66 | mixed | "It just keeps switching between which tracks are 'disconnected' (when they are connected)." — NeoKuro [S11] **R** — the oscillation IS the connector-steal loop's observable |
| F67 | mixed | "it doesn't take anything and launch completely empty with not enough fuel to go back." — Imagine12 [S12] **R**; ping-pong half: "launch[es]…not even to mars but back to the same asteroid" — Berserker [S13] |
| F68 | mixed | "every time a drone delivers requested cargo, a second drone instantly runs up and steals the cargo." — TheNightglow [S14] **R**; + dev note verbatim "Fixed drones endlessly moving resources between Landers." [S5] |
| F70 | mixed | "trying to set a payload makes the rocket completely ignore that and just unload itself." — Berserker [S13] **R** |
| F71 | src-diff | "it automatically filled up with waste rock and flew back up." — Iced_Delulu, Nov 11 2025 [S15] **R** — junk-over-valuables is uniquely predicted by alphabetical fill (WasteRock sorts first); + Oxygenus's independent fix [S25] |
| F73 | mixed | "Tourist stands outside the hab, suffocating, starving and dehydrated, refusing to walk in" — schrolock, Nov 25 2025, with dev reply in-thread [S16] **R**; + dev note "colonists were starving in Naturalist Habitats that were filled with food" [S5] |
| F78 | player-report | "disasters only occur once or twice early on and then stop triggering altogether." — Anders, May 2026 [S17] **R** (post-1.0.4, so the wedge class survived the dev fix); "disasters bug, where they stop occurring after a while" — jkund17, Nov 29 2025 [S18] |
| F81 | mixed | Same player witnesses as F78 (one symptom, two proven mechanisms — both live on our 194-sol save) **plus** GromGor's mechanism-specific description: "After a meteor storm, one of the keys may not be removed, preventing further disasters from generating." [S24] **R** |

*Note on F78/F81 sharing witnesses: the reports cannot discriminate the wedge
(F78) from the stranded flag (F81a) — but both mechanisms are play-PROVEN in
this project, the dev note couples "not starting/not ending", and an
independent author diagnosed the F81a key. GOLD for both is a judgment call
recorded as such.*

### 2.2 SILVER — high confidence; full playtest still required

(a) = OG report + mechanism still present in Relaunched Src; (b) = Relaunched
report, mechanism not discriminable from the report; ⚑ = independent fix-author
witness (BRONZE→SILVER promotion per prompt §Witnesses).

| id | prov | grade | witness / basis |
|---|---|---|---|
| F01 | player-report | (b)⚑ | **Recorded "Matches live Paradox-forum report" is NOT re-derivable** (forum Cloudflare-blocked; no matching thread title found). Partial OG witnesses only [S19]. ⚑ fredware #9 names the player-facing symptom: "Prevents periodic underground Marsquakes and cave-ins when No Disasters is enabled." [S23] **R**. Sibling tell (every other disaster checks the rule). Owner action: logged-in check of Paradox subforum 1189 |
| F02 | src-diff | (b) | Generic severity witnesses only ("about 40% of my colonists died when meteors collided" — MaritimeRetro, Nov 2025 [S20] **R**); nobody quantifies the ~6h cadence or the tower inversion. Sibling tell (intact loop 40 lines below) carries it |
| F03 | src-diff | (a)⚑ | ChoGGi fixed the same leak class in OG (Water Reclamation upgrade leak, per corpus match); mechanism in Relaunched proven by our PT-02 in play |
| F05 | src-diff | (b) | "Is there supposed to be a popup i missed telling me i 'won'…?" + community consensus that no win popup exists [S21] **R** — consistent with the crash swallowing "A dream fulfilled"; rules/error not confirmed in-thread |
| F06 | src-diff | (a) | OG threads (title-grade, forum blocked): "Philosopher's Stone Stuck on Finishing", "Crystal Entity / Philosophers Stone Mystery stuck" [S22]; + R 1.0.6 patch note: "closed many of the things that could cause specific steps in the sequences to not trigger" [S5] |
| F11 | src-diff | (b) | **Escapes HOLD.** "One gets stuck at a station saying waiting for another station to be empty and there were no trains in that trains direction … they wont move or go away." — freakaholic15, Dec 2 2025 [S4] **R**. Cause not discriminable (tier U stands); the entry's settling observation remains the owed work |
| F16 | src-diff | (b) | Paradox title+snippet: "Sphere mystery dialog never leaves completely after mystery is over" [S22] — same incomplete-cleanup family, different surface (UI vs site). Dead-validation tell carries the mechanism |
| F21 | src-diff | (b) | "Colonists will take the train to the extractors, but won't take it back. Instead, they'll hoof it and end up dying on the way back." — Northernlightman, Dec 6 2025 [S26] **R** — asymmetric refusal fits wait-time-in-the-score; 1.0.7 attributes some to commute interruption (mechanism not isolated) |
| F35 | mixed | (b)⚠ | "none of these buffs apply to large wind turbines" + "Frictionless Composites" named + player-derived formula — TheNightglow thread, Nov 2025 [S27] **R**. ⚠ **The thread may witness a LIVE label miss, not (only) our old-save fixup repair — work item: verify our F35 scope covers the live case before calling this witnessed-and-fixed** |
| F36 | player-report | (a) | "Universities consider every open worker slot to be a needed geologist." — Tamren, Apr 2018 [S28] **OG**, mechanism exact; the Relaunched leg exists only as the RESEARCH.md paraphrase (rule 1 blocks GOLD) |
| F37 | src-diff | (a)⚑ | ChoGGi verbatim: "If you remove a farm that has an oxygen producing crop (workers not needed) the oxygen will still count in the dome." [S29] — same mechanism, same two-part fix shape |
| F38 | src-diff | (a)⚑ | ChoGGi verbatim: "Rovers will still use destroyed tunnels (in certain situations)." [S29] — same function, same PF-re-registration leak |
| F40 | src-diff | (a)⚑ | ChoGGi verbatim: "It doesn't always cure colonists for some reason and Biorobots never die, plus they're robots..." [S29]; his load-sweep is the same idea as ours |
| F41 | mixed | (a)⚑ | ChoGGi verbatim: "Gene Forging tech doesn't increase rare traits chance." [S29] — identical claim; our fix already credits and improves his approach |
| F43 | src-diff | (a)⚑ UNREP | ChoGGi fixed the same `LayoutConstructionController:Activate` hole in OG **where it was live** (Triboelectric Scrubber via DLC layouts); in Relaunched it is R3-latent. Witnessed mechanism + unreportable-today — ships as the cheap patch it is |
| F48 | — (blocked) | (b) | "no matter what the tracks won't connect" — NeoKuro; "Tracks refuse to connect, rebuilt and rebuilt many many times." — Cheezcake117.TTV [S11] **R**; + dev note "Resolved more instances of tracks and stations not connecting properly" [S5]. Confounded with F66; fixup path not isolated. Raises the value of unblocking F48's test |
| F50 | mixed | (b) | "Had a rocket come back from breakthrough mission and now its stuck unloading. There is nothing in it…" — Daddy Warbucks, Jun 2026 [S30] **R** — the visible face of trips-can-never-complete; hourly kick itself unobserved |
| F51 | player-report | (b) | "citizens unemployed in domes with job openings inside and in the near outside" — PamdaDev, Nov 17 2025 [S31] **R** + 1.0.4 note. Family-grade: cannot discriminate F51's cache from F54/F58/F59/F60; the "manually assign… they leave right after" detail matches a different mechanism |
| F53 | mixed | (b) | Family witnesses (F52's quotes + RESEARCH's "die walking rocket→dome" paraphrase); the arrivals-specific safety-dome detail is unwitnessed verbatim |
| F59 | src-diff | (b) | "They refuse to to find a home, even if there are plenty of free houses." — Boothy, Nov 17 2025 [S9] **R** + dev 1.0.4 note. Soft-intent flag from the challenge review stands as a caveat; escapes HOLD on the witness |
| F60 | src-diff | (b) | "Citizens become homeless despite free housing in both their own and adjacent domes." — Kudaku [S2] **R** — family-grade (overlaps F58/F59); counter-mismatch specifics unwitnessed |
| F64 | mixed | (b) | Dev-side: "Deleting a track will now prefab trains at stations that are still associated with it" + stored-train notifications added in 1.0.7 [S5] — the defect family acknowledged; the "trains go to void" report itself not relocated (likely in the blocked Paradox subforum) |
| F69 | mixed | (b) | "it arrives at asteroid, it is then stuck there because it did not load the 70 fuel you wanted" — Jammy [S12]; "I've got an RC Commander and 6 drones STRANDED on this EFFING ASTEROID" — DwarfMurdered [S13] **R**. Manual-landing fuel-dump not isolated from F67/F68 |
| F74 | mixed | (b)⚑ | 1.0.7 note [paraphrase-grade]: RC-Transporter rare-metals rocket-overload exploit fixed [S32]; ⚑ fredware #10: "Prevents RC Transports from interrupting Universal Trade Rockets." [S23] **R** |
| F76 | play | (a) | Own keyboard (owner verbatim in the entry) **plus** OG same-symptom witness: "The icon which should appear when I click on a deposit does not appear!" [S33] **OG** — suggests NOT ultrawide-only; raises this todo's priority |

### 2.3 BRONZE — sweep-only; finding report → owner review

Every entry keeps its named intent tell (challenge-review vocabulary). "NOT
FOUND" = a genuine search ran (queries recorded in the agent outputs, §6);
absence is a prior, not a verdict.

| id | sub | tell / note | owes |
|---|---|---|---|
| F04 | B2 ⚠️ **contested — see §10** | **Moved from GOLD by §9:** the stuck-night-shift thread fits C32's label-desync better (stuck BUILDINGS + asteroid-range correlation); our hour-window defect stands on its sibling tell (shift-1/2 windows correct) but no witness discriminates it. **The prompt-6 sweep refuted the reasoning behind this move (§10); tier decision sits with chain prompt 7** | probe (has) + owner skim |
| F07 | B1 | sibling contradiction; 1000× unit error. Reports NOT FOUND — a colony grid hides 1 kW vs 1 MW | probe (has) + owner skim |
| F08 | B1 | sibling tell; **defective inverted line re-confirmed live in Relaunched Src this audit** (`HolidayRating.lua:77`) | probe + owner skim |
| F09 | B1/B2 | asymmetric threshold pair; statistically invisible to players | probe + owner skim |
| F12 | B1 | unsatisfiable integer-division guard; the near-miss report found is the *grid* branch, which is correct — good discrimination. PT-07 proved fix by play | none new |
| F13 | B3 | dead rows (dead-code tell); PT-08 by play | none new |
| F14 | B3 | dead highlight (dead-code tell); PT-09 by play | none new |
| F15 | B1 | double-grant arithmetic; invisible over-grant | probe + owner skim |
| F17 | B1 | unused randomization; invisible | none new |
| F18 | B1 | preset self-contradiction (10 vs described 20) | none new |
| F19 | B3 | caption omission; PT-43 by play | none new |
| F20 | B3 | **explicit dev comment tell**; PT-43 by play | none new |
| F22 | B2 | wrong contract, R1-hourly; politically invisible drift | none new |
| F23 | B2 | dead validation tell; PT-44 by play | none new |
| F25 | B1 | preset self-contradiction; legacy-save gated | none new |
| F26 | B1 | dead local (`spawn_dir`) tell; cosmetic | none new |
| F27 | B1 UNREP | R3: no shipped rate modifier; §4a keeps it | exempt |
| F29 | B2 UNREP | R3: defaults mask both; 4 live Mystery-2 callers by enumeration | exempt |
| F31 | B2 UNREP | R3: trigger and precondition mutually exclusive. **False-GOLD averted: the Kudaku asteroid-cave-in quote was offered for F31 and REJECTED — F31's defect fires onto UndergroundMap (or crashes on `false`), never onto an asteroid. Quote reassigned to C02 (§4)** | exempt |
| F33 | B2 | crash path, min-brush dab; "lakes causing crashes" family reports too vague to attach | probe + owner skim |
| F34 | B2 | nil-guard latents. **Corroboration correction: RESEARCH.md's "ChoGGi's Landscaping Freeze corroborates F34(b)" FALLS — his fix targets mark exhaustion, which Relaunched redesigned away (`LandscapeMarkStart` now wraps/scans). Our items stand on their own Src evidence only** | owner skim |
| F47 | B1/B2 | refund arithmetic; PT-45 by play; plausibly masked by F44/F45 (players couldn't salvage at all) | none new |
| F54 | B2 | gate/list contradiction tell; PT-34 by play; adjacent reports never state hubs were off | none new |
| F57 | B2; (a) UNREP | (b) R1 by play; (a) R3 flagged | exempt for (a) |
| F72 | B2 | gate-and-list contradiction tell; PT-33 by play; the exact "No available landers" refusal unwitnessed | none new |
| F75 | B1 | dead validation tell; politics-latent salience | probe + owner skim |
| F77 | B2/B3 | owner-observed live symptom (fleet Idle churn); intent tell is consequence-shaped (challenge-review flag). The pending PT doubles as the intent observation — already queued | PT (queued) |
| F82 | B2 | owner verbatim observation on the entry; legacy `g_SplitSupplyGridPositions` refs; external reports NOT FOUND | own trace (queued) |
| F84 | B3 | **play-proven** (rover used the tunnel during PT-25); text-patch design is the recorded user decision | user decision (open) |
| F85 | B2 | audit-derived latent (F83-family mechanism play-PROVEN; this instance shielded by the modal); tier U | settling observation (queued: rebind quicksave) |

### 2.4 NON-FIX tier (adjudicated "we are not fixing this" — formalized 2026-08-01, owner)

**Definition:** entries where the decision NOT to fix is made and grounded —
R4 unreachable, tier-I intentional, §4a mod-facing-only, or owner-declined.
Distinct from BRONZE by construction: every BRONZE is a shipped fix (or a
filed defect awaiting decision) for a real player-reachable — or
§4a-deliberately-shipped latent — defect. Nothing in BRONZE belongs here; the
four latent R3s (F27/F29/F31/F57(a)) are *deliberate* fixes under the owner's
§4a rule (latent harm ships), not non-fixes.

| id | grounds |
|---|---|
| F10 | wontfix — faction funding conditions, designed/declined |
| F24 | R4 unreachable in vanilla; fix DELETED 2026-07-30 (user decision) |
| F28 | R4 — zero callers in all of Src; §4a mod-facing bar; fix + probe DELETED |
| F32 | wontfix — designed notification behavior |
| F42 | tier I — guard's purpose does not reach dust devils; designed scope (user 2026-07-25; ⚠ stale index row corrected this audit) |
| **F49(a)** | **R4, mod-tools-only entry into `place_track`** (exhaustive falsification: no InstantTracks const, no cheat, injection-only repro; self-corrects on palette refresh). ✅ **Wrinkle RESOLVED 2026-08-01 (owner direction): the no-op guard was STRIPPED from `Fix_TrainMinors` the same day** — wrapper, Require entries and the probe's palette half all removed; A/B code-gate leg owed (F49 entry). The tier now leaves no live code behind |
| F49(c) | tier I — designed behavior; guard REMOVED 2026-07-30 |
| F56 | tier I — auto RC Transports never covered rockets, by maintained design |
| F61 | wontfix — superseded by D03 (the need is met by design, not repair) |
| F62 | tier I — carried-forward design (services one passage hop) |
| F63 | tier I — carried-forward design (universities/emigration) |
| F79 | owner-declined 2026-07-31 — risk exceeds benefit on large maps |

(F39 is not a non-fix — folded into D04. F49(a) briefly sat in HOLD this
audit and was reclassified here on owner challenge, §3.) Our own defects F86/F87/F88: external
witnesses are category-inapplicable (though the prior-art survey already
benchmarked F86 against the community). D-entries are design decisions, not
defect claims. F83 is play-PROVEN + `tested` — no external witness owed.

## 3. HOLD list — EMPTY (corrected 2026-08-01 on owner challenge)

**F49(a) held here for a few hours and was reclassified: it does not meet
HOLD's own definition.** HOLD requires "the audit's own recheck **lacks
strong confidence**" — F49(a) is the opposite. The reachability audit's
lead-pass block is an exhaustive, high-confidence R4: no `InstantTracks`
const exists (the Instant* family is Cables/Passages/Pipes only), both
instant-build techs and the one sponsor perk touch other grids, the build
menu hardcodes `require_construction = true` for tracks, `Cheats.lua` has
zero track references, and the only reproduction ever achieved was
console-injecting `grid_elements_require_construction = false` — a
mod-tools-grade entry with no player-facing control (the PT-46 lesson:
injection-only = evidence FOR R4). The defect even self-corrects — a colony
colour-scheme change repaints every element with the correct palette.

F49(a) is therefore an **already-adjudicated R4 rider**, not an open
question: the reachability audit decided its disposition (keep the no-op
rider inside the module carried by the live (d) half; optionally strip on
next touch), and this audit adds nothing and defers to that record. It is
listed with the adjudicated set in §2.4, not here.

No other entry qualifies for HOLD: every no-witness entry is either
arithmetic (B1), carries a hard tell, is UNREPORTABLE-exempt, or gained a
witness this audit (F11's stuck-train report, F59's homeless thread).
**The tier ends the audit empty — nothing we ship rests on a
low-confidence, unwitnessed judgment call.**

## 4. NO MECHANISM FOUND — report prominently

**These are reported-and-real-looking with no located mechanism — potentially
the most valuable cell in the audit.**

- **C02 — cave-ins on asteroids.** Now carries a **verbatim Relaunched
  witness**, recovered by this audit and REASSIGNED from a false F31 match:
  *"Asteroids routinely have cave-ins. I could be wrong, but I'm pretty sure
  this event is supposed to trigger on the cave map, not on the asteroid
  map."* — Kudaku review, Nov 14 2025 [S2] **R**. Our sweep verified the
  underground-marsquake repeat cannot do this (`Environment == "Underground"`
  guard) and F31's defect fires the wrong *direction*. Something else triggers
  them: mod interaction, misattribution, or an unlocated real bug. The 1.0.4
  note "Marsquakes no longer occur on Asteroids" [S5] suggests the devs hit a
  sibling of this — and the review post-dates it.
- **F80 — trains skip valid waiting passengers.** Observed at our keyboard
  (17+ game hours, forensics on the entry) **and** by the community: *"I just
  had 52 colonists leave a ship and … they crowd a train station supposedly
  waiting for it to take them to the dome they're right next to!"* —
  reeses4brkfst, Nov 27 2025 [S34] **R**; dev note: "colonists … stuck
  (sometimes indefinitely) while waiting for a train" [S5]. Suspected
  enumeration-direction mechanism on the entry remains **untested** — this is
  the strongest reported-but-unpinned defect we hold.
- The unswept C-leads (C03–C11) remain report-derived candidates awaiting
  sweeps — not "no mechanism found" (nobody has looked yet). Two gained
  strength this audit: **C04** now has an independent Relaunched fix
  (GromGor's "No Underground supply grid breaks" — *"It's very strange to
  experience supply grid breaks underground during dust storms on the
  surface. This mod fixes it."* [S24]) and **C06** is confirmed real-in-OG by
  Tremualin's Library fix ("Fixed a bug where colonists would end up with
  multiple workplaces." [S35]).

## 5. ⭐ Gaps in OUR list

Filed as **C12–C31** in BUGS.md with this commit (evidence inline there).
Grades: **[VERIFIED]** = this audit read the Relaunched Src lines itself;
**[author]** = fix-author witness, Src not yet checked by us.

**Verified against Relaunched Src (C12–C17):**

1. **C12 — Support Struts ignore the Easy Maintenance game rule** (ChoGGi:
   "Devs didn't check for EasyMaintenance"). `SupportStruts.lua:17-22` verified
   bare — hard-malfunctions under a rule that should soften it. [VERIFIED]
2. **C13 — three FollowUp storybits mis-categorized as `TechResearched`**
   (Survey Offer opt-2, Free Will resolution, Cure For Cancer rare outcome) —
   ChoGGi: "it never shows up". `FreeWill_2.lua:4,8` + `SurveyOffer_TechEffect.lua:4,18`
   verified (`Cure4Cancer_RareOutcome.lua:4` category verified; it has no
   `Enabled` line — chain behavior needs one more check). [VERIFIED]
3. **C14 — Fhtagn! Fhtagn! option 2 cowards ALL colonists** — outcome text
   promises "all Religious Colonists become Cowards"; the effect at :71-82 has
   **no filter**, while the sibling outcome at :45-65 shows the correct
   filtered pattern. Sibling-contradiction tell. [VERIFIED]
4. **C15 — Dust Sickness: Deaths morale penalty never applied** — params and
   text advertise the penalty; the file contains **zero** outcome effects.
   [VERIFIED]
5. **C16 — flying drones malfunctioning mid-air stay stuck "flying"** —
   `FlyingDrone.lua:141-154`: `Malfunction/Freeze/NoBattery` are
   `assert(IsLanded())`+parent (asserts strip in retail) while `Dead()` right
   below lands first. Sibling-contradiction tell. [VERIFIED]
6. **C17 — The Man From Mars follow-up rewards nothing** — replies promise
   morale gains; zero `StoryBitOutcome`/`ActivationEffects` in the file,
   which remaster devs touched (QA stamps 2024-11/2025-04) without adding
   them. [VERIFIED]
7. **C18–C21** — investigate-grade with ChoGGi prior art + Src pointers:
   XenoExtraction label coverage vs now-native extractors (**intent question**
   — the description matches the four shipped effects, so no promise is
   broken; §4-amendment bar applies); `AreDomesConnectedWithPassage` has no
   distance term (F52/F53-adjacent); Philosopher's Stone paused sector-count;
   St. Elmo sinkholes not `indestructible` vs meteors (soft-lock class).

**Author-witnessed, not yet Src-checked (C22–C31):** fredware's Saint Blessing
morale stacking, dust devils continuing after terraforming disables storms,
ordinary rockets misclassified as asteroid landers, Jumbo Cave reinforcements
stuck on unreachable Waste Rock (confirms an old RESEARCH lead); SkiRich's
perpetual-maintenance repair-cycle bug ("Most people think its a drone issue.
It is not"), Signal Booster extender radius never applied, RC Transport
Optimization capacity never applied, children-only buildings admit all ages,
supply-pod reward pins stuck on HUD; GromGor's "Broken Meteor Storms in
1.0.7.396349" (**our exact pinned build**, mechanism unknown — possible F02/F78
relative). Each filed with its verbatim author description and source.

**Checked and NOT gaps (fixed in Relaunched — new confirmations beyond the
existing remaster-fixed list):** Blank Slate applicant removal (now in
`ActivationEffects`, remaster QA stamps — **this audit refuted its own agent's
claim here, §7.3**); Asylum prerequisites (Relaunched adopted essentially
ChoGGi's fix); Cyber War funding; The Door To Summer; UndergroundDeepScanning
category; expedition-rover cleanup; RCHarvester waste rock; `GetModifierObject`;
landscape mark exhaustion; `emptry_table` typo; daily-interest loop; expedition
"unknown status".

## 6. The roster (assembled and judged)

**Accepted (ChoGGi-tier bar: substantial fix corpus + readable source +
longevity/subscribers):**

- **ChoGGi** (index case) — OG only. Fix Bugs 7,752 subs, updated 2026-05-08;
  MoreInfo.md is a 398-line itemised fix list (verbatim copy in the audit
  scratchpad; corpus re-cloned and read locally). **Zero Relaunched output**;
  secondhand forum answer: "He said he will do it later when he has time."
  Only 3 "SMR" comments exist in his entire corpus; the one global statement is
  *"Hopefully most of this mod isn't needed for SMR..."* — hope, not audit.
- **SkiRich** — OG only; the clearest second ChoGGi-tier author. Six dedicated
  Fix mods (1.0k–4.8k subs each, workshop-only source) + Better Lander Rockets
  with a 19-item fix list that witnesses the whole OG lander/B&B cluster. His
  own words: "I made these patches since the devs havent fixed their code
  yet." Zero Relaunched output.
- **Tremualin** — OG only; accepted **with caveat** (hybrid content+fix). The
  fix corpus lives in Tremualin's Library (5,231 subs, updated 2025-06-09,
  GitHub MIT, Paradox Mods mirror): six listed fixes incl. the
  multiple-workplaces fix (=C06). Two of six are modded-trait infrastructure
  (out of our §4a scope).

**Relaunched-native (watch list — real fix authors, none yet at the bar,
all <9 months old):** **fredware** (Bug Fixes, 13 per-toggle fixes, MIT GitHub
with 112 commits though the Bug Fixes folder wasn't pushed at fetch time,
"Please complain! I can't fix what I don't know is broken" — the one to
watch — **⚠ REMOVED from the Workshop within ~a day of upload**: by the
owner's follow-up check later on 2026-08-01 the item page reads "removed from
the community for violating Steam Community & Content Guidelines", reason
unstated. The 13-fix description survives only as this audit's verbatim
API-read quote; his GitHub is the remaining watch channel, and the §7.1
subscribe suggestion is moot until/unless it returns); **GromGor** (5 fix/workaround mods, no readable source); **Oxygenus**
(Asteroid Rocket Waste Fix, 397 subs); MyNutzYurFace (underground lighting).

**Rejected (with reasons):** **LukeH** — one genuine fix mod (Martian Express
Patch — and its description witnesses the OG-DLC train families) but
content-first, no readable repo; note he IS active on Relaunched and his
recreation's description witnesses a vanilla SM:R defect ("Colonists can work
in any interior buildings of a dome in the range of their destination
station... (not working properly in vanilla SM:R)"). **Ayzo** — the "Martian
Express Fix Pack" is his, not LukeH's, and is an aggregator repack. **Fizzle
Fuze** (one-line fix corpus), **Silva/Dash** (content-only, both games),
**Thorik** (AI redesigns, not defect repair, no source), **akarnokd**
(automation QoL), **FirestormMk3** ("patch" = mission-patch decal), plus nine
one-off single-fix authors (listed in the roster agent output with links).

## 7. Method and its limits

1. **Source blocks.** forum.paradoxplaza.com and reddit.com are
   crawler-blocked. Every Paradox citation is title/snippet-grade; the three
   reports most likely living there (F01's NoDisasters thread, F64's "void"
   report, F74's rival-rocket report) are **unretrieved, not disproven**.
   **STOP-AND-ASK items for the owner:** (a) a logged-in browse of the
   Relaunched Bug Reports subforum (1189) for those three; (b) a browser check
   of Paradox Mods' Relaunched section (SPA, unfetchable) — it is the console
   channel, and whether fredware/GromGor mirror there matters for D13; (c)
   consider subscribing to GromGor's five mods (no public source — the
   workshop download would hand us his packed Lua for mechanism comparison
   on F04/F81a/C31) and fredware's Bug Fixes.
2. **Corrections to our own records made or flagged by this audit:** F42 index
   row (`blocked`→`wontfix`, fixed this commit); F34's claimed ChoGGi
   corroboration falls (§2.3); F35's witness may out-scope our fix (work item
   on the entry, §2.2); F01's non-re-derivable report claim replaced with what
   is actually on record (§2.2); Relaunched released **~Nov 13, 2025** (docs
   elsewhere imply Feb 2026; 1.0.4 = Dec 10 2025, 1.0.6 = Feb 16 2026).
3. **Verification discipline paid for itself:** of six agent-claimed Tier-A
   gaps spot-checked against Src, **one was refuted** (Blank Slate — fixed in
   SMR via `ActivationEffects`, which the agent misread as absent). All gap
   entries filed as [VERIFIED] were read by this session directly; [author]
   entries are explicitly marked unverified.
4. **Family-witness rule (applied throughout):** where one symptom is
   predicted by several mechanisms (homeless cluster F51/F54/F58/F59/F60;
   weather-silence F78/F81; track-connection F48/F66), a shared report gives
   GOLD only to the entry whose distinguishing detail it names (F58's
   reservation shadow, F66's oscillation); the rest cap at SILVER. This is
   rule 2's coincidental-match guard operationalized.
5. **Quotes** are machine-extracted verbatim (typos preserved) with URLs; a
   human re-check of any load-bearing quote before quoting it in a store page
   is cheap and recommended. Steam review permalinks don't exist — review
   quotes cite the browse page they were read from.
6. **`CANNOT DETERMINE`:** whether ChoGGi's captured-vanilla bodies match
   Relaunched for F37/F38/F40/F41/F43+F03 — his fixes for exactly these carry
   **no captured originals** (wrappers/data patches), so the ⭐
   identical-code upgrade is undecidable from local sources. See §7.7.
7. **Extraction report (Lua.hpk): ZERO entries needed it.** No tier in this
   audit depends on extracting the original game's Lua. The only thing it
   would buy is the ⭐ upgrade on the five ChoGGi-matched SILVER(a) entries —
   cosmetic to their standing. **Recommendation: do not build the extractor
   for this.** The dependency the prompt worried about evaporates.

## 8. Sources

[S1] steamcommunity.com/app/3215050/discussions/0/797838226728656171/ · [S2] steamcommunity.com/app/3215050/reviews/?browsefilter=toprated (Kudaku, Nov 14 2025) · [S3] steamcommunity.com/app/3215050/discussions/0/691998095298538348/ · [S4] steamcommunity.com/app/3215050/discussions/0/691994648689827064/ · [S5] steamcommunity.com/app/3215050/discussions/0/766309862211705626/ (dev fix-list thread) · [S6] steamcommunity.com/app/464920/discussions/0/1640918469751039933/ · [S7] steamcommunity.com/app/3215050/negativereviews/?browsefilter=toprated&l=english&p=1 (Rhodith) · [S8] steamcommunity.com/app/3215050/discussions/0/658215953538296888/ · [S9] steamcommunity.com/app/3215050/discussions/0/660467372238571824/ · [S10] steamcommunity.com/app/3215050/discussions/0/695372460980312562/ · [S11] steamcommunity.com/app/3215050/discussions/0/658215953538161940/ · [S12] steamcommunity.com/app/3215050/discussions/0/658215953538296815/ + /658216290030325560/ · [S13] steamcommunity.com/app/3215050/discussions/0/660467372238569064/ · [S14] steamcommunity.com/app/3215050/discussions/0/691994126364820085/ · [S15] steamcommunity.com/app/3215050/discussions/0/679607959154615075/ · [S16] steamcommunity.com/app/3215050/discussions/0/682986810375204974/ · [S17] steamcommunity.com/app/3215050/discussions/0/834998413871378587/ · [S18] steamcommunity.com/app/3215050/discussions/0/691994366768609081/ · [S19] steamcommunity.com/app/464920/discussions/0/3038230013019773675/ · [S20] steamcommunity.com/app/3215050/discussions/0/691994126364708516/ · [S21] steamcommunity.com/app/3215050/discussions/0/694249410478015485/ · [S22] forum.paradoxplaza.com threads 1112166 / 1113731 / 1495056 (title/snippet grade) · [S23] steamcommunity.com/sharedfiles/filedetails/?id=3775120166 (fredware Bug Fixes) · [S24] GromGor workshop items 3717125029 / 3676027320 / 3730839706 / 3745475097 · [S25] steamcommunity.com/sharedfiles/filedetails/?id=3604423090 (Oxygenus) · [S26] steamcommunity.com/app/3215050/discussions/0/682986292645092952/ · [S27] steamcommunity.com/app/3215050/discussions/0/660467372238618006/ · [S28] steamcommunity.com/app/464920/discussions/1/1742228532898283720/ · [S29] github.com/ChoGGi/SurvivingMars_Mods … /Fix Bugs/MoreInfo.md (verbatim copy in audit scratchpad) · [S30] steamcommunity.com/app/3215050/discussions/0/567036688513147663/ · [S31] steamcommunity.com/app/3215050/discussions/0/658216290030318639/ · [S32] steamcommunity.com/games/3215050/announcements/detail/534381453704692743 (1.0.7 notes) · [S33] steamcommunity.com/app/464920/discussions/0/3211505894106180744/ · [S34] steamcommunity.com/app/3215050/discussions/0/691994126364857669/ · [S35] steamcommunity.com/sharedfiles/filedetails/?id=2588520023 (Tremualin's Library). Full per-query search logs live in the five agent outputs under the session task directory.

## 9. Addendum (same day) — the packed-source comparison round

The owner subscribed to GromGor's five mods and fredware's "Bug Fixes" on
Steam; the workshop delivered all six `ModContent.fpk` files — **including the
removed fredware mod**. The FLPK container format was re-derived (the parity
session's extractor was not kept; the new one, with the format documented
in-file, is `flpk_extract.py` in the session scratchpad) and all six unpacked.
Everything below comes from reading the actual fix source against Src and our
own `Code/`, with the load-bearing claims re-verified in Src by this session.

**Tier corrections this round:**

- **F04: GOLD → BRONZE-B2** (counts in §1 updated). GromGor's "Workshifts
  FixUp" turned out to repair a *different* live mechanism — buildings falling
  out of `UIColony.labels.ShiftsBuilding` and never receiving `SetWorkshift`
  again — and that fits the witness thread better than our colonist
  hour-window bug (stuck BUILDINGS colony-wide; onset correlated with an
  asteroid leaving range, which fits label rebuilds on map transitions). The
  label-desync is filed as **C32**. F04's defect claim itself stands
  unchanged on its sibling tell. This is rule 2 doing its job at the source
  level: the false GOLD survived quote-matching and fell only to code.
  ⚠️ **CONTESTED 2026-08-01 by the prompt-6 C32 sweep — see §10. The
  parenthesised inference above ("which fits label rebuilds on map
  transitions") is not true of Src: there is no label rebuild on a map
  transition.** This bullet's own lesson now applies to itself.
- **F81a hardened**: GromGor clears the exact `g_DisastersPredicted
  .DisasterMeteorStorm` key our `Fix_MeteorStormWedge`/`Fix_DisasterPrediction
  Leak` pair manages — independent diagnosis confirmed at code level, not
  just description level.
- **C31 RESOLVED — not a new mechanism.** GromGor's "Broken Meteor Storms in
  1.0.7.396349": his `GenerateDir` half is a **no-op** (vanilla's is a
  file-local in `Meteors.lua:43-55` his global cannot shadow — and his copy
  is byte-identical to Src anyway, guard included); the effective ingredient
  is a one-shot `StopMeteorStorm()` on load — the F78 heal family. Verdict:
  independent corroboration that the F78 wedge still occurs on our pinned
  build. Side find: `Bombardment.lua:38-50`'s sibling `GenerateDir` lacks the
  zero-dir guard (F26's neighborhood; noted, not filed).
- **C04 mechanism confirmed**: vanilla `SupplyGridFragment:
  RandomBreakConnection` (`SupplyGrid.lua:669-683`) picks its break victim
  with **no map filter**; GromGor's working fix restricts to surface
  connectors. One call-chain sweep away from an F-row.

**fredware's 13 fixes vs ours (agent comparison, spot-verified):**

- **F01 — equivalent.** He wraps the repeat's COND slot + deletes live
  threads (reversible-at-runtime, his panel architecture demands it); we wrap
  FUNC. Same defect, same coverage, neither misses anything.
- **F74 — OURS IS A SUPERSET.** His guard blocks only `UniversalTradeRocket`
  and **misses `UniversalRefugeeRocket`** (a sibling class, not a subclass —
  his own description claims parity it doesn't deliver). Ours blocks both
  plus the legacy classes.
- **F78/F81 — overlapping, neither subsumes.** He clears the same stale
  meteor-storm flags (his liveness test is the same one our F78 uses) and his
  rains rewrite kills the F81b deadlock by `WaitThread` instead of our
  bounded `WaitMsg`. **But he never restarts the wedged `MeteorStorm`
  scheduler thread** — under his mod, weather resumes but the colony never
  sees another natural meteor storm; our F78 heal restarts it. Conversely
  **he clears stale state we do not**: → **C34** (stale-ACTIVE
  `g_RainDisaster` with a dead main thread, healed via vanilla
  `FinishRainProcedure`), plus minor `RainsDisasterThreads` structure
  repairs and mid-session (not just on-load) flag sweeps.
- **Track demolition — a THIRD defect, not F45/F48.** He does not attempt
  F48's blocked fixup at all. What he fixes is → **C33**: whole-track
  demolition via `DemolishAndSplitTrack` calls `OnDemolish` directly
  (`TrackElement.lua:468/:506/:520`, verified), which sets
  `CanDelete = ret_false` (`Track.lua:248-250`, verified) with no
  `DoneObject` ever following — an invisible, undeletable, save-persisted
  TrackBase shell that raises if deleted naively. **Our own F44 replacement
  keeps that call shape and reproduces the shell on mass salvage** — the
  single most actionable finding of the round.

**His four fixes we lacked, now graded:** C22 Saint blessing —
**Src-airtight** (`"Religious"` vs `GetTraitLabel` → `"TraitReligious"`,
verified; the trait has never worked); C23 dust devils — **three verified
defects** (spawn_chance misused as an integer-truncating count scaler :216 vs
the correct probability use :169; `CurrentMap` descriptor read under a
`MainMap` scheduler; no `DustStormsDisabled` term in the marker path); C24
asteroid-visit predicate — **precedence bug verified on
`PlanetaryView.lua:439`**, complementary to our F72 (we fix the false
negative, vanilla's false positive passes through our wrapper); C25 Jumbo
Cave — mechanism chain verified, trigger needs a repro. Also noted: his #11
(lander cargo-ramp safety) overlaps our F67/F68 family and deserves its own
comparison pass — recorded as a lead, not filed.

**On the removal:** nothing in his 22 files plausibly explains a Workshop
takedown — no copied vanilla bodies (his loop replacements are
re-implementations; our pack ships more captured vanilla code than his), no
network/filesystem/loadstring, persistence via the sanctioned mod-storage API
only, version 38 of careful in-place migration. The removal cause is likely
external to the code. His `bf_forecast.lua` (40KB) is an original
disaster-forecast overlay, off by default.

**Net effect on the audit's numbers:** GOLD 17→16, BRONZE 29→30, **HOLD 1→0**
(F49(a) reclassified to the adjudicated set on owner challenge — it is a
high-confidence R4, which fails HOLD's lacks-confidence definition, §3), and
the C-ledger grew to C12–C34 (23 filed candidates), of which **9 are now
Src-verified** (C12–C17, C22–C24, plus C33) and two more mechanism-confirmed
(C04, C25). The §7.1 owner actions are updated: the GromGor/fredware
subscribe suggestion is DONE and consumed; the Paradox subforum and Paradox
Mods browser checks remain open.

## 10. ⚠️ Candidate verification sweeps (2026-08-01, chain prompt 6) — where they contradict §9

**Read this before quoting §9's addendum.** §9 graded packed mod source against
Src; this section is the owed *own-sweep* pass over the candidates §9 left at
"mechanism confirmed, call chain owed". Two of its four results overturn a
recorded verdict. Full evidence trails live on the BUGS entries named; only the
contradictions are summarised here, because a summary is what gets quoted.

### 10.1 C32 — DOWNGRADED, and it takes §9's F04 demotion with it

§9 moved F04 GOLD → BRONZE-B2 on the strength of C32 being the better mechanism
match for the "Buildings are stuck on night shift" thread. The sweep read every
`ShiftsBuilding` label site in 1.0.7.396349 Src and found:

1. **No route for C32 as filed.** The label has exactly one add site
   (`ShiftsBuilding:GameInit`, `Lua\Buildings\ShiftsBuilding.lua:50`) and one
   remove site (`:54-57`, self-disabling, reached only from `OnDestroyed` and
   `Done`), plus the generic invalid-only purge in `ValidateLabels`
   (`Lua\Colony.lua:116-120,152`; `CommonLua\LabelContainer.lua:15-33`). A
   valid, non-destroyed building on a loaded map has no way out of the label.
2. **§9's load-bearing inference is false of Src.** "Onset correlated with an
   asteroid leaving range, which fits label rebuilds on map transitions" —
   there is **no label rebuild on a map transition**; `PostDoneMap` purges
   invalid objects, i.e. the unloaded map's own buildings, and never touches a
   main-map building.
3. **The wild-evidence is explained away.** GromGor's predicate fires on every
   destroyed-but-unrebuilt building, because `Building:OnDestroyed`
   (`Lua\Buildings\Building.lua:1366-1367`) is empty while
   `ShiftsBuilding:OnDestroyed` de-labels. That is not a defect.
4. **Owner's 1.0.7 challenge, answered: trigger yes, mechanism no.** Asteroids
   never expire on 1.0.7 (`Lua\Asteroids.lua:1,:208,:327,:331-348,:493-500`),
   so the reported onset cannot occur unattended; but the workshift tick is
   unchanged — one `OnMsg.NewWorkshift` handler in all of Src, still iterating
   `UIColony.labels.ShiftsBuilding` with no membership check.

**Limit, stated so nobody over-reads this:** the sweep read 1.0.7 only, and the
thread's reports are 1.0.6-era, when asteroid expiry did unload maps. C32 is
downgraded, not closed; F04's *defect* claim never depended on any of this.
**The F04 tier decision is chain prompt 7's** — §9's demotion should not be
quoted as settled.
