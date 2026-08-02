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
| F01 | player-report | (b)⚑ **→ see §10.4: RETRACTED, witness found** | ~~**Recorded "Matches live Paradox-forum report" is NOT re-derivable**~~ **RE-DERIVED 2026-08-01** by the owner's logged-in browse — Rubik, **May 8 2026, Game Version 1.0.7**, with steps to reproduce and the word "periodic" matching the mechanism. The Cloudflare block was the whole reason it looked unfindable. Partial OG witnesses also [S19]. ⚑ fredware #9 names the player-facing symptom: "Prevents periodic underground Marsquakes and cave-ins when No Disasters is enabled." [S23] **R**. Sibling tell (every other disaster checks the rule). Owner action: logged-in check of Paradox subforum 1189 |
| F02 | src-diff | (b) | Generic severity witnesses only ("about 40% of my colonists died when meteors collided" — MaritimeRetro, Nov 2025 [S20] **R**); nobody quantifies the ~6h cadence or the tower inversion. Sibling tell (intact loop 40 lines below) carries it |
| F03 | src-diff | (a)⚑ | ChoGGi fixed the same leak class in OG (Water Reclamation upgrade leak, per corpus match); mechanism in Relaunched proven by our PT-02 in play |
| F05 | src-diff | (b) | "Is there supposed to be a popup i missed telling me i 'won'…?" + community consensus that no win popup exists [S21] **R** — consistent with the crash swallowing "A dream fulfilled"; rules/error not confirmed in-thread |
| F06 | src-diff | (a) | ~~OG threads (title-grade, forum blocked): "Philosopher's Stone Stuck on Finishing", "Crystal Entity / Philosophers Stone Mystery stuck" [S22]~~ **CORRECTED 2026-08-01 (§10.4): the bodies were read. "Crystal Entity…" (1113731) is a RETRACTION — "NOT A BUG: I missed a crystal" — and is struck. "Stuck on Finishing" (1112166) is genuine and matches the signature, but is OG-2018, carries a destroyed-crystal confound, and its only second witness is the person who retracted the other. ONE confounded OG report, not two**; + R 1.0.6 patch note: "closed many of the things that could cause specific steps in the sequences to not trigger" [S5] |
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
| F64 | mixed | (b) | Dev-side: "Deleting a track will now prefab trains at stations that are still associated with it" + stored-train notifications added in 1.0.7 [S5] — the defect family acknowledged; the "trains go to void" report itself not relocated (likely in the blocked Paradox subforum). **◑ 2026-08-01 (§10.4): the block was removed and the FAMILY is witnessed live (Jan 30 2026), but the verbatim phrase was still NOT found — stop quoting it** |
| F69 | mixed | (b) | "it arrives at asteroid, it is then stuck there because it did not load the 70 fuel you wanted" — Jammy [S12]; "I've got an RC Commander and 6 drones STRANDED on this EFFING ASTEROID" — DwarfMurdered [S13] **R**. Manual-landing fuel-dump not isolated from F67/F68 |
| F74 | mixed | (b)⚑ **→ see §10.4: primary evidence found** | 1.0.7 note [paraphrase-grade]: RC-Transporter rare-metals rocket-overload exploit fixed [S32]; ⚑ fredware #10: "Prevents RC Transports from interrupting Universal Trade Rockets." [S23] **R**. **⭐ 2026-08-01: the rival-rocket report is FOUND — Homeshine, twice, OG Sep 5 2022 (overflow trigger) and Relaunched May 2 2026 on 1.07 (halt-mid-load trigger), both ending in a permanently bricked rocket.** Paraphrase-grade is superseded by primary; the note plausibly covers one trigger and not the other |
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
   ✅ **ALL THREE ARE NOW DONE — §7.1 CLOSES.** (c) was consumed by the §9
   packed-source round. **(a) and (b) were run by the owner on 2026-08-01 and
   are recorded in §10.4** — (a) returned two hits and one partial, and
   retracts this bullet's F01 claim; (b) returned a live console channel with
   a discovery problem. The general lesson stands and is worth keeping: **"the
   crawler cannot reach it" was doing far more work in this audit's grading
   than anyone noticed** — two of three reports existed all along.
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

[S1] steamcommunity.com/app/3215050/discussions/0/797838226728656171/ · [S2] steamcommunity.com/app/3215050/reviews/?browsefilter=toprated (Kudaku, Nov 14 2025) · [S3] steamcommunity.com/app/3215050/discussions/0/691998095298538348/ · [S4] steamcommunity.com/app/3215050/discussions/0/691994648689827064/ · [S5] steamcommunity.com/app/3215050/discussions/0/766309862211705626/ (dev fix-list thread) · [S6] steamcommunity.com/app/464920/discussions/0/1640918469751039933/ · [S7] steamcommunity.com/app/3215050/negativereviews/?browsefilter=toprated&l=english&p=1 (Rhodith) · [S8] steamcommunity.com/app/3215050/discussions/0/658215953538296888/ · [S9] steamcommunity.com/app/3215050/discussions/0/660467372238571824/ · [S10] steamcommunity.com/app/3215050/discussions/0/695372460980312562/ · [S11] steamcommunity.com/app/3215050/discussions/0/658215953538161940/ · [S12] steamcommunity.com/app/3215050/discussions/0/658215953538296815/ + /658216290030325560/ · [S13] steamcommunity.com/app/3215050/discussions/0/660467372238569064/ · [S14] steamcommunity.com/app/3215050/discussions/0/691994126364820085/ · [S15] steamcommunity.com/app/3215050/discussions/0/679607959154615075/ · [S16] steamcommunity.com/app/3215050/discussions/0/682986810375204974/ · [S17] steamcommunity.com/app/3215050/discussions/0/834998413871378587/ · [S18] steamcommunity.com/app/3215050/discussions/0/691994366768609081/ · [S19] steamcommunity.com/app/464920/discussions/0/3038230013019773675/ · [S20] steamcommunity.com/app/3215050/discussions/0/691994126364708516/ · [S21] steamcommunity.com/app/3215050/discussions/0/694249410478015485/ · [S22] forum.paradoxplaza.com threads 1112166 / 1113731 / 1495056 (title/snippet grade) · [S23] steamcommunity.com/sharedfiles/filedetails/?id=3775120166 (fredware Bug Fixes) · [S24] GromGor workshop items 3717125029 / 3676027320 / 3730839706 / 3745475097 · [S25] steamcommunity.com/sharedfiles/filedetails/?id=3604423090 (Oxygenus) · [S26] steamcommunity.com/app/3215050/discussions/0/682986292645092952/ · [S27] steamcommunity.com/app/3215050/discussions/0/660467372238618006/ · [S28] steamcommunity.com/app/464920/discussions/1/1742228532898283720/ · [S29] github.com/ChoGGi/SurvivingMars_Mods … /Fix Bugs/MoreInfo.md (verbatim copy in audit scratchpad) · [S30] steamcommunity.com/app/3215050/discussions/0/567036688513147663/ · [S31] steamcommunity.com/app/3215050/discussions/0/658216290030318639/ · [S32] steamcommunity.com/games/3215050/announcements/detail/534381453704692743 (1.0.7 notes) · [S33] steamcommunity.com/app/464920/discussions/0/3211505894106180744/ · [S34] steamcommunity.com/app/3215050/discussions/0/691994126364857669/ · [S35] steamcommunity.com/sharedfiles/filedetails/?id=2588520023 (Tremualin's Library) · **[S36] reddit.com/r/SurvivingMars/comments/1p6dnbj/ — "We are up to hotfix 1.0.3 now… anyone notice game getting better?", u/aom17, ~Dec 2025, read in full from an owner PDF export 2026-08-01 (§10.5). ⛔ HOTFIX-1.0.3-ERA — four generations before our pinned build; evidence of harm, never of current presence.** · **[S37] reddit.com/r/SurvivingMars/comments/1vblaf6/ — "Should I buy relaunched?", ~2026-07-30** · **[S38] reddit.com/r/SurvivingMars/comments/1vcylpm/ — "Is relaunched still broken?", 2026-08-01.** Both owner PDF exports, read in full (§10.6). **CURRENT — contemporaneous with our pinned build — but read §10.6's selection-bias caveat before quoting either: enthusiast "no bugs" testimony is data about the speaker, not the build.** Full per-query search logs live in the five agent outputs under the session task directory.

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
✅ **That comparison pass RAN 2026-08-01 (chain prompt 6) and the "overlaps"
guess was wrong — see §10.3. It is a real gap with zero overlap; filed as
C35, deliberately NOT promoted.**

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
(C04, C25). **Superseded 2026-08-01 by §10: C04 is closed and promoted to F90;
C32 is downgraded.** The §7.1 owner actions are updated: the GromGor/fredware
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

### 10.2 C04 — CONFIRMED and promoted to F90 (this one goes the other way)

§9 graded C04 "mechanism confirmed, one call-chain sweep away from an F-row".
The sweep ran and the chain closes with no gaps, so **C04 is closed and filed
as F90**. Caller: `City:HourlyUpdate` (`Lua\City.lua:148-149`) →
`RandomBreakSupplyGrid` (:178-181) → `SupplyGrid:RandomBreakElements`
(`Lua\SupplyGrid.lua:1017-1021`) → the map-blind `table.rand(self.connectors,
…)` at :677. Entry route for the underground connector: `SupplyGridFragment`
**is** a `MultiMapSupplyGrid` (:337-338); the elevator merges both sides'
fragments (`Lua\Buildings\Elevator.lua:402-440` → global `MergeGrids`
:1635-1650 → `AddElement` :547-548) and `AddCityElement` (:463-477) registers
the merged fragment on **both** cities' lists.

Two intent tells, one of them a sibling contradiction: `HasDustStorm` is
hard-gated to `MainMap` (`Lua\DustStorm.lua:41`), so the disaster is designed
surface-only; and the production pass sixteen lines above the break pass
guards the shared-fragment case *with a comment explaining that fragments span
cities* (:999-1001), while the break pass carries no guard at all.

Nothing built — the victim pick sits mid-function, so the fix shape runs into
FIX_POLICY §3a, and that is chain prompt 7's package. Two scope questions are
flagged on the F90 entry rather than decided here (the merged element count
also inflates the surface break *rate*; GromGor's own fix would index nil on
an empty surface list).

### 10.3 fredware #11 — §9 guessed "overlaps our F67/F68 family"; it does not

The comparison pass ran. His #11 wraps `LanderRocketBase:CanRequestPayload`
and blocks the Edit Payload affordance while the cargo ramp is in use. Ours
answer a different question entirely — F67 `IsCargoReady`, F68/F71
`CreateAutoCargoRequest`, F70 `CargoRequestNew:RetrieveRequests`/`:Apply` — all
of them about *what the payload contains*, none of them reading the ramp lists.
**Zero overlap; a real gap, and the nearest miss is ours**: F70 already wraps
`CargoRequestNew:Apply`, the exact call that fires `SetCommand("CmdLoad")`, and
does not guard the ramp.

The mechanism is located and the sibling tell is clean — the payload path runs
`DisconnectFromCommandCenters()` (`Lua\Buildings\CargoTransporter.lua:1017`)
with no wait, while the takeoff path makes the same call under the comment
*"so no more drones climb the ramp"* and then waits on `IsCargoRampInUse()`
(`Lua\Buildings\RocketBase.lua:757, 762-768`).

**But the harm is unproven, so it is filed as C35 and deliberately NOT
promoted to prompt 7.** Re-tasking a drone whose resource the player just
removed is the *designed* consequence of editing a payload; nobody has shown a
unit stranding. fredware himself ships it `beta`, off by default, and his
remedy takes an action away from the player — a §4 behaviour change, not a
repair. The settling observation is named on the C35 entry.

**Method note worth keeping:** §9 graded this "overlaps" from the fix
*descriptions*. Reading the two bodies against Src reversed it. Same lesson as
§9's own F04 bullet, one level up.

### 10.4 ⭐ The two owner web-checks were RUN (2026-08-01) — §7.1 closes, and one of this audit's own claims is retracted

**The owner ran both stop-and-ask items the same day prompt 6 routed them.**
Results below; per-entry records on BUGS F01 / F64 / F74 / C33.

**The headline is a correction to this audit, not to the pack.** §7.1 leaned on
"forum.paradoxplaza.com is crawler-blocked" to grade three reports
*unretrieved*. With a logged-in browser, **two of the three were found in one
sitting**. Nothing about the code changed — all three fixes were already
shipped and tested — but *"we could not reach the source"* had been quietly
functioning as evidence about the world, and it was not.

| Item | Result |
|---|---|
| **F01** — NoDisasters cave-ins | ⭐ **FOUND.** Rubik, **May 8 2026**, **Game Version 1.0.7**, Steam, with steps to reproduce. The recorded "matches live Paradox-forum report" is **vindicated**, and the replacement is stronger than the original claim — dated, version-stamped to our build family, and its word *"periodic"* matches `MapGameTimeRepeat("UndergroundMarsquake", …)` exactly. **§2's "NOT re-derivable" is retracted.** |
| **F74** — rival rocket | ⭐ **FOUND, twice, same reporter.** Homeshine: OG **Sep 5 2022** (*overflow* trigger) and Relaunched **May 2 2026 on 1.07** (*halt-mid-load* trigger). Both end in a rocket permanently stuck on the pad. **Primary evidence supersedes the paraphrase-grade dev note [S32]** — and the sane reading is that the note covers the overflow trigger while a player on 1.07 hit the other one. The defect survived the remaster. |
| **F64** — "trains go to void" | ◑ **PARTIAL.** The *family* is witnessed live (Kopernikus79, **Jan 30 2026**: station removed → train bookkeeping wrong afterwards and stayed wrong). The **verbatim phrase this project has quoted since the entry was written was not located.** It is now "searched with the block removed and not found" — **stop citing it as a quote.** Owner also reports **many** similar train threads, mostly past the forum's five-month necro threshold: the cluster is well-reported and largely stale, so absence of *recent* posts must not be read as "fixed". |
| **Paradox Mods (console channel)** | ✅ **RUN.** **GromGor mirrors there — an exact mirror of his Steam workshop, same titles. fredware does NOT; he is Steam-only.** So the channel is live and already used by a Relaunched fix author, and fredware's removed mod has no console-side copy either — our archived FPK remains the only recoverable form of his work. |
| **⚠️ Discovery on Paradox Mods is term-hostile** | Owner's observation: **searching `bug` or `fix` returns ZERO hits**, while searching the author name `gromgor` surfaces his bug-fix-titled mods immediately. Recorded as an **observation, not a mechanism** — one browse, and search behaviour changes. (The owner's read is that Paradox suppresses such terms; that is a hypothesis this audit does not test.) **If it holds, it is a distribution fact with teeth: a pack whose name and purpose are the words "bug" and "fix" would be undiscoverable by its own keywords on that channel.** Re-check before anything depends on it. |

**⛔ [S22] IS PARTLY A BAD CITATION — RESOLVED SAME DAY, AND ONE OF THE TWO
THREADS IS A RETRACTION.** The clean URLs work (the earlier 404s were a
malformed address, not missing threads). The owner opened them, and **reading
the bodies reversed what the titles said** — which is the third time in one day.

- **`1113731` — "[Win10] Crystal Entity / Philosophers Stone Mystery stuck"
  (mgla, Aug 7 2018, game version 233,467). ⛔ THE REPORTER RETRACTED IT. The
  post's own first line reads "NOT A BUG: I missed a crystal."** This audit
  cited it as corroboration for **F06** on the strength of its *title*. It is
  the opposite of corroboration. **Struck.**
- **`1112166` — "Philosopher's Stone Stuck on Finishing" (Hockston, Jul 26
  2018, game version 231.777). Genuine, and it does match F06's signature** —
  the big crystal formed, then *"I gave up on the mystery completing after a
  good while of waiting for the crystal to do something. It didn't get the green
  checkmark on new game mystery list either."* A formed crystal that never
  resolves and a mystery that never marks complete is exactly the missed
  one-shot `Msg("CrystalFlyAway")` this project derived from Src.
  **But grade it honestly, because it is weaker than it looks:** (i) it is
  **OG-era 2018**, not Relaunched; (ii) the reporter had **destroyed several
  crystals**, leaving the formation *"not contiguous"* — a confound the report
  itself flags; and (iii) **its only apparent second witness is mgla**, whose
  *"I encountered the same problem on the newest version"* was posted the same
  day they closed their own identical report as user error. **So F06's Paradox
  corroboration is ONE OG report with a confound, not two reports.**
- **`1495056`** (carrying **F16**) — the owner reports it *"looks like it might
  have multiple confirmations"*. **Content not yet read; still title-grade.
  Do not upgrade F16's citation until someone reads the bodies** — that is the
  precise mistake this bullet exists to record.

**F06's and F16's defect claims are untouched by all of this.** Both stand on
Src — for F06, a one-shot `Msg` with no re-broadcast and a `CrystalForceFlyAway`
escape hatch that has **no emitter anywhere in Src**. This is a provenance
repair, not a code risk, exactly as predicted when the retry was booked.

**Incidental find in `1112166` worth more than the citation it came from:** the
same reporter, same build, adds *"I also played through Spheres in 231.777 and
it did not complete once done, cold never went away, not marked as done, and
steam achievement didn't pop."* **Two different mysteries failing to mark
complete for one player on one build** points at shared completion machinery
rather than a crystal-specific bug — a lead for the mystery-stall family
(F06/F16 and the 1.0.3-era cave/network-node stalls in §10.5). Not filed; no
mechanism, and OG-era.

**The pattern, stated once because it has now happened three times in a day:**
§9 graded fredware's #11 an overlap from its *description* and was wrong; §7.1
graded three reports unretrievable from a *crawler block* and was wrong twice;
[S22] graded a retraction as corroboration from its *title*. **Every one of
these was a body that had never been read.**

**What §10.4 changes downstream:** F01 and F74 gain primary witnesses (tier
consequences are bookkeeping, not new decisions); F64 loses a quotation;
C33 gains a possible live symptom recorded as a **lead still missing its author,
date and build**; D13 gains a confirmed console channel plus a discovery problem.

**📌 Two source facts this round added, both of which make "no report found"
weaker evidence than §7.1 treated it as:**

1. **Paradox's in-game bug submitter can fail with HTTP 500.** The C33 lead
   exists as a *screenshot of a filled-in report form* precisely because its
   author's submission errored and they posted the picture to the forum by
   hand. If that is not isolated, **reported volume undercounts real
   incidence** — an unknown number of players stop at the error box. One
   observed instance; not established as systemic, and worth a second look if
   anyone ever reasons from report counts.
2. **reddit.com is blocked at host level for our tooling — confirmed
   first-hand 2026-08-01**, not inherited from §7.1. Both `www.reddit.com` and
   `old.reddit.com` refuse. r/SurvivingMars is therefore an **owner-only**
   channel, on the same footing as the logged-in forum and Paradox Mods: three
   of the four community sources this project cares about cannot be reached by
   any session, only by a person. **Workaround that works: the owner exported a
   thread to PDF and handed it over** — §10.5 is the first result of that, and
   it is the cheapest way to get Reddit into evidence.

### 10.5 The first Reddit thread ever read by this project [S36] — and the build caveat that governs all of it

**Source:** r/SurvivingMars, *"We are up to hotfix 1.0.3 now… anyone notice game
getting better?"*, u/aom17, **~Dec 2025**, 49 upvotes, ~40 comments; exported to
PDF by the owner 2026-08-01 and read in full.

> ⛔ **THE CAVEAT IS THE MOST IMPORTANT LINE IN THIS SECTION. This thread is
> hotfix-1.0.3-era — FOUR hotfix generations before our pinned 1.0.7.396349.
> Nothing in it is evidence that anything still exists.** It is evidence about
> **harm**: that these symptoms were real, widespread, and in several cases
> colony-ending. That answers §4a "who benefits", and it answers nothing about
> "is it still there" — which is what Src is for. Any future session quoting
> §10.5 must carry this sentence with the quote.

**What it corroborates (all of these are already Src-verified by us, so the
thread adds witnesses, not verdicts):**

- **F67 / F68 / F71 — the lander cargo family, described from the outside with
  startling precision.** j1dopeman independently reconstructs F68: *"I think
  they're just doing a **circular unload/load**… Even if it says it is full when
  you click takeoff the number will drop."* Next_Interaction4335 gives F67 twice,
  and adds a consequence our entry understated — the lander **strands** on the
  asteroid. turnipofficer gives both at once. Several players describe inventing
  the same workaround (over-request to compensate), which is what people do
  *instead* of filing a report.
- **F80 — a witness cluster, and two observations that constrain the
  mechanism.** Recorded in full on the F80 entry. The short version: the
  dominant public symptom is not "colonists wait at the platform" but
  **"colonists ignore the train and walk, and die"** — plausibly the same
  unenumerable-destination defect at a different stage (no ticket issued →
  walk). Sorbicol's *"only between two domes… my rail network includes 3 lines"*
  is a specific-pair failure on a healthy network, which fits the directional
  enumeration theory and is hard to explain any other way.

**What it COSTS us — a lead filed hours earlier is now probably dead:**

- **The C33 "cannot add trains to tracks" lead is weakened, possibly spent.**
  The thread's top comment states that *"you can place trains on the train
  tracks again, **which Hotfix 1 broke**"* — i.e. that exact symptom was a known
  hotfix-1 regression **fixed in hotfix 2**. If the screenshotted report is from
  the 1.0.1/1.0.2 window it is that regression, not a track shell. **Its missing
  date is now the whole question.** Recorded on the C33 entry.

**Two items routed rather than filed** (neither is this audit's to decide):

- **D10 / D12 — a dev-fix claim that their build prompts must check.** Bst011:
  *"Theyve also squashed two of the most pressing bugs with the 1.0,
  **homelessness and unemployment**."* Those are the exact subjects of D12 (no
  homeless) and D10 (workshops / unemployment). Third-hand, vague about which
  1.0.x, and from a satisfied player rather than a patch note — **so it is a
  prompt to verify against Src, not a reason to descope anything.**
- **Unfiled observations, listed so nobody re-derives them as new:** cave/mystery
  stalls (*"the cave mystery appears to be bugged and does not complete"*, *"the
  ai build more network nodes mystery has not advanced"*, the Diggers *"dregers"*
  spawn question) — F06's family, no mechanism offered; a station that *"refuses
  to connect"*; naturalist habitats starving/suffocating; rockets vanishing in
  flight; train capacity/car-count complaints that are **balance, not defect**.
  None is filed: 1.0.3-era, no mechanism, and no current-build evidence.

**Method note.** The two most useful things in this thread were not the
complaints. They were **one commenter's throwaway memory of a hotfix history**
(which cost us a lead) and **one commenter's incidental precision about scope**
(*"only between two domes"*, which constrained a mechanism). Neither would
survive a keyword search. That is an argument for reading community threads
whole, and an argument against treating them as a bug-report feed.

### 10.6 Two CURRENT Reddit threads [S37][S38] — contemporaneous with our pinned build, and they cut both ways

**Sources, both exported by the owner 2026-08-01 and read in full:**
- **[S37]** *"Should I buy relaunched?"* (u/Regular_Future2474, **~2026-07-30**)
- **[S38]** *"Is relaunched still broken?"* (u/Thorn-of-your-side, **2026-08-01**, hours old)

**These are NOT §10.5.** That thread was 1.0.3-era and could only speak to harm.
These are current, so they can speak to the build we actually ship against —
which makes the sampling problem the important thing to state first.

> ⚠️ **SELECTION-BIAS CAVEAT (owner, recorded because it governs every use of
> [S37]/[S38]).** A subreddit is not a bug tracker. Enthusiasts report "no bugs"
> for reasons that are not evidence of absence: **they may be running fix mods
> and no longer remember**, they may be motivated to defend a game they want
> supported, and the loudest "it's fine now" posts sit next to detailed defect
> reports in the same thread. **Treat "I haven't seen that" as data about the
> speaker, not about the build.** Both threads contain both kinds, sometimes
> from people with hundreds of hours.

#### ⭐ 10.6a The strongest finding: our F81(a) has become standard community advice

**mizushimo ([S37], 1 day old):** *"It is buggy… **I recommend running the game
with the disasters patch mod (Patch 1.0.7 No Disasters After Meteor Storms)**"*
— and repeats it to a second player in [S38]: *"**disasters are broken but you
can fix it with a mod**."*

**That mod is GromGor's workshop `3717125029`, which this project already holds
in the archive and has already read.** Its own description
(`metadata.lua`, verified this session): *"After a meteor storm, **one of the
keys may not be removed, preventing further disasters from generating.** This
mod fixes this issue."* — i.e. **precisely F81(a)**, the stranded
`g_DisastersPredicted` key our `Fix_DisasterPredictionLeak` /
`Fix_MeteorStormWedge` pair manages (§9 already matched the code; this matches
the *community's experience of it*).

**Why this is worth more than another bug report.** It is not one player hitting
a defect — it is a regular telling newcomers to install the fix **before they
start playing**, unprompted, twice, in two different threads, days ago. That is
about as strong a real-world reachability signal as this project is ever going
to get for F81(a), and it is independent of both our source reading and
GromGor's code.

#### 10.6b A mechanism hypothesis for D12, from the player who had the symptom

**Thorn-of-your-side ([S38] OP):** *"people were constantly flicking between
being housed and unhoused, and people genuinely just stopped working. There were
jobs available in domes with unemployed people and they would not fill the job
slots anymore."* Then, unprompted, a cause:
> *"I think the homelessness issue was caused by **one of the law upgrades that
> allows homes to house more colonists**, because I'd check homes at their
> capacity would regularly fluctuate **because of staffing in the law spire**."*

mizushimo: *"Oh yeah, I heard about that."* **A politics law whose residence-capacity
bonus tracks live law-spire staffing would make dome capacity oscillate, and
colonists would flick housed/unhoused as it moved** — a concrete, checkable
mechanism for a symptom D12 has only ever had as a symptom. **Routed to prompt
10; it is a hypothesis to test against Src, not a finding.** Note the OP was
describing a launch-era game, so currency is not claimed for the symptom — only
the hypothesis is new.

#### ⚠️ 10.6c A current claim that CONTRADICTS our verified lander family — recorded, not hidden

**lifeinneon ([S38], 2 hours old, "Research" flair):** *"They fixed the
showstopper bugs fairly quickly after launch… **Landers and the elevator work
much more smoothly now. The old bugs don't happen because they've completely
changed how both work to be more straightforward**."*

**Our F67/F68/F70/F71 are Src-verified against 1.0.7.396349 and live-tested
(PT-16/17/31/32).** So this claim is contradicted by stronger evidence and does
not move any verdict — **but it is recorded because burying inconvenient
testimony is exactly the failure mode this audit has spent the day correcting.**
It also sits *in the same thread* as a player describing F67 verbatim
(Thorn-of-your-side, [S37]: *"my rocket would just fly back and forth until it
was out of fuel and got stuck on the asteroid"*), which is the caveat above in
miniature. **Standing rule, unchanged: "fixed in Relaunched" only from current
Src.**

#### 10.6d Filed as candidates — and one of them SOLVED itself within the hour

- **⭐ C36 (Inner Light) — FILED AND CLOSED THE SAME DAY. It is not a new defect;
  it is a downstream victim of F81(a), which our pack already fixes.**
  `Lua\Mysteries\Dream.lua:20-34`: the mirage loop skips `Dream()` for as long as
  `IsDisasterPredicted()` is true — the exact flag F81(a) strands permanently —
  so the mystery stops advancing forever, silently. **It explains the reporters'
  "for some people" precisely** (you are affected iff a meteor storm completed
  during your run). `REACHABILITY_AUDIT.md` had already listed the Inner Light
  dream cycle as a downstream victim *as an inference*; the community supplied
  the observation and Src confirmed the path. **Recorded on F81 as a new
  player-visible consequence: (a) does not merely stop the weather, it voids a
  mystery playthrough.**
- **C37 (planetary anomalies / elevator)** — stands as a candidate:
  single-source, mechanism unread, but specific, current, and sitting on the
  same elevator seam **F90** just proved the surrounding code mishandles.

#### 10.6e Noted, NOT filed — with the reason in each case

- **Save-freeze / autosave corruption.** mizushimo, both threads: *"makes the
  save unplayable by **freezing in the same point in time every reload**"*, and
  *"the crashing was due to repeated crashes during autosave slowly corrupting
  your save file… turn off autosave"*, described as an OG-era problem too. **A
  deterministic, reload-stable save wedge is the same CLASS as F86** and bears
  on D13 and on our own save/reload test legs. Not filed: community hearsay,
  no mechanism, and it is vanilla. **Worth a look if D13 ever asks what a
  "rescued" save can be expected to survive.**
- **Console autosave lock.** YsoL8 (PS5): *"a bug with it locking when it
  autosaves if there isn't enough save space left."* Feeds the D13 console
  question; not ours.
- **Asteroid cave-ins.** Thorn-of-your-side (launch-era): cave-ins spawning on
  **asteroid** maps and *"filling the entire asteroid"*. If real, that is the
  **same map-scoping class as F90/C04** — a disaster reaching a map it was not
  scoped to. Launch-era and unverified; recorded because the class now has a
  proven member.
- **Passageway oscillation.** mizushimo: *"a rare bug with a passageway (where
  they **run back and forth endlessly** in a passageway)"*, plus *"dome mobbing"*
  from over-using filters. Adjacent to F52/F53 and to **C19** (prompt 6b job 2).
- **Trains vs shuttles.** sloppylaw: *"trains are still a bit buggy in that I
  can't get them to not want to take the shuttles."* Transport-mode selection;
  F80's neighbourhood, no mechanism.
- **Politics balance, food/research reworks, terraforming slog, seeders stopping
  at ~40%** — balance and roadmap, not defects.

#### ⭐ 10.6f "Crashes" and "bugs" are not two categories — and players report them as if they were (owner, 2026-08-01)

**The observation:** community threads carry a large volume of *"it crashes"*
alongside *"I haven't really found any major bugs"*, often from the same
population — as though instability were a separate phenomenon from defects.
**It very likely is not. A defect that leaves bad state can surface to the
player as a crash, a freeze, or a corrupted save, and the player will file that
under "unstable game" rather than under the bug that caused it.**

**This is not speculation about players; the threads contain the link being made
and missed in the same breath:**
- **Made:** Thorn-of-your-side, on runaway asteroid cave-ins — *"that would end
  up filling the entire asteroid with caveins and **I believe even caused some
  crashes when the game wanted to spawn more**."* A player tracing a crash back
  to a defect.
- **Missed:** the same thread's *"I haven't really found any major bugs"* from a
  player who is not reporting on their error log, because nobody can.
- **The chain, described by a third:** mizushimo — *"the crashing was due to
  **repeated crashes during autosave slowly corrupting your save file**"*, and
  the endpoint, *"makes the save unplayable by **freezing in the same point in
  time every reload**."* Deterministic replay of a bad state is what a corrupted
  save looks like, not what a driver fault looks like.

**The datum that makes it concrete — and it is from §10.5:** Bst011, playing
with debug enabled, reports *"you get a pop up **every time the game throws an
error code**, and the volume of pop-ups I get on the latest version is maybe
**1% of the volume it was on launch**."* **The retail game runs on a stream of
Lua errors that no ordinary player can see.** In this engine an error is
usually swallowed (`procall`) rather than fatal — so the visible consequence is
not a crash at the error, it is **state quietly going wrong**, and the crash or
freeze arrives later with nothing to connect it to.

**Three consequences for how this project reads evidence:**
1. **Crash reports are a LOWER BOUND on defect incidence, not a separate
   bucket.** A thread full of crash complaints is a thread reporting defects it
   cannot name.
2. **"I haven't seen any bugs" from someone who also reports crashing is not a
   clean report** — it sharpens §10.6's selection-bias caveat with a mechanism.
3. ⚠️ **It points back at us.** Our own `Opt_DroneOverhaul` threw **80–98 orphan
   errors per load** after uninstall (F86, leg 5 / PT-58) — completely silent to
   a player, who would eventually blame the game. **That is the whole argument
   for F86's per-site discipline and for D13**, and it is why our A/B legs count
   `[LUA ERROR]` instead of trusting "it seemed fine". **A playtest leg that
   reports "no crash" has measured nothing; the log is the instrument.**

**⭐ MECHANISM REFINED (owner, 2026-08-01) — the engine's answer to bad state is
a HANG, not a crash, and that is why the two categories collapse.** During the
F86 investigation an agent induced **massive save degradation**, and the session
had to be ended by **force-stopping the game**. Under abuse severe enough to
require a kill, **it still did not crash.** Combined with mizushimo's endpoint —
*"makes the save unplayable by **freezing in the same point in time every
reload**"* — the chain is almost certainly not `defect → process crash`. It is:

> **defect → wedged or runaway state → the game stops responding → the player
> force-quits → the player reports "it crashed."**

That is a **stronger** version of the connection, not a weaker one. It means
much of the community's "crash" volume is likely the **hang/freeze class, which
IS the state-corruption class** — the class this pack is largely aimed at. It
also fits the engine: Lua errors here are usually swallowed by `procall` rather
than fatal, so a defect cannot easily kill the process; it can only leave the
world wrong until something spins or blocks forever. Every wedged-thread defect
we hold (F02, F78, F81b, F88, F89) is exactly that shape.
⚠️ **Unmeasured.** The incident is the owner's account and is not anchored to a
log or leg in these docs — **if anyone can identify the session, anchor it**,
because an induced-degradation case that did *not* crash is a useful control in
its own right.

**Recorded as a framing correction, not a finding.** No measurement here ties
any specific crash to any specific defect, and some reports are plainly
unrelated (one commenter's PC froze while changing graphics settings). The
claim is only that the community's two categories are one category, and that
treating them as two makes defect incidence look smaller than it is.

**⭐ And §10.6 supplied a worked example of the same blindness at the DEFECT
level, not the crash level:** one commenter gave two unconnected pieces of
advice — *"install the disasters patch mod"* and *"avoid Inner Light"* — which
a source read (`Lua\Mysteries\Dream.lua:20-34`) showed to be **one defect**,
F81(a), whose stranded `IsDisasterPredicted()` flag freezes the Inner Light
dream loop forever. **Players do not group symptoms by cause, because they
cannot see causes.** Any future reading of community evidence should assume the
report count over-counts distinct defects and under-counts their severity.

##### 10.6f(i) Our own sample — a real observation, and why it is NOT a control

**Owner, 2026-08-01: across the entire beta campaign — ~58 hours of in-game
testing — the game has NEVER crashed with the fix pack installed**, including
during legs that do things no player would do (console-forced autosaves, planted
stale GameVars, deliberately killed and wedged threads, forced tech grants,
mid-session mod enable/disable, repeated save/load cycling, and a full uninstall
leg).

**⚠️ CORRECTED 2026-08-01, hours after first being written — the original
version of this block got the exposure profile WRONG, and it was the
load-bearing objection.** It claimed *"our legs are mostly short, targeted, and
early-to-mid colony… we may simply not be standing where the crashes are."*
**That describes only the agent-driven legs.** The owner's actual method:

> **The owner spends HOURS, solo, building each test save out before an agent
> ever starts** — deliberately provisioning colonies with large drone fleets,
> large populations, many rockets, asteroids, and **"hundreds or thousands of
> unrelated background tasks firing"**, precisely so the short measured leg runs
> against a realistically loaded world.

**So the 58 hours DOES include long, continuous, high-entity-count sessions —
which is exactly the profile the community's crash reports cluster in.** The
correction cuts two of the four original objections and leaves two standing.
**This is a fact about every leg result in this project, not just this one:**
the measured legs are short, but the worlds they run against are not fresh.

**What still stands, and it is the decisive one:**

1. **There is no vanilla arm.** No matched build-out of comparable length and
   complexity *without* the pack exists. Zero crashes in the treatment group
   with no control group is not a comparison — this alone prevents any claim
   that the pack improves stability.
2. **One machine, one driver stack, one player.**

**What no longer stands:** ~~the exposure-profile objection~~ (corrected above),
and ~~"we reload constantly, so accumulation never happens"~~ — true of the
agent legs, **false of the multi-hour build-out sessions**, which are continuous
play and are where accumulation would occur if it occurs at all.

**⭐ AND THE SESSIONS ARE LONG-LIVED PROCESSES, WHICH MATTERS FOR THE LOGS AS
MUCH AS FOR THE CRASH COUNT (owner, 2026-08-01).** The owner **does not close or
refresh a game session** unless a playtest specifically calls for a fresh leg.
So when an agent arrives, runs a leg and asks for a log flush, **the log it
receives typically covers a session that has been continuously active for 1–6
hours.**

Three consequences, and the first two are the ones nobody has been crediting:

1. **Our "zero `[LUA ERROR]`" results are stronger than they have been read
   as.** A zero across a 1–6 hour continuously-running process on a loaded
   colony is a substantially better result than a zero across a leg window, and
   that is what several of them actually are.
2. **Our logs contain far more evidence than the legs that produced them.** Hours
   of ordinary play sit in the same file as the measured window. **Old logs are
   worth mining** — for `[LUA ERROR]` of any origin, for vanilla wedges, for the
   kind of background-task noise no leg was designed to look for.
3. ⚠️ **But an error three hours older than the leg lands in the same file.**
   Anything attributed to a leg must be located **in time**, not merely found in
   the file. Existing legs have generally done this (they quote `t=` game-time
   stamps and line context) — this is a caution for future reading, not a
   retro-accusation.
   ⛔ **AND IT MUST NOT BE READ AS LICENCE TO DISCOUNT OLD LINES — the owner
   corrected this the moment it was written, and they were right.** *"Not caused
   by our leg"* is an **attribution** verdict; it does not answer *"what is it,
   then?"*. Collapsing the two is how a discovery is thrown away silently.
   **The owner reviews errors WITH the agent and pushes back when a line does
   not fit the test. That has happened rarely — and every time, it turned up a
   VANILLA defect that was not on our list.** The binding version of this rule
   now lives in `WORKFLOW.md` ("Log review: never silently discount a line"):
   report every unexplained line with its age and let the owner decide; stop the
   leg for anything out of the ordinary rather than resolving it privately.
   The mechanism that makes it work: **the agent pre-registers what it expects
   and knows why, the owner independently reviews everything the agent saw and
   does not — so anything outside the prediction is signal by construction, and
   the only party able to recognise it is the one being asked not to file it
   away quietly.**

⚠️ **One check this raises, worth naming rather than assuming away:** error
*counts* compared across arms are only comparable if the arms had comparable
exposure. PT-58's headline is **0 orphan errors against leg 5's 80** — if those
two sessions differed greatly in uptime, the zero would be less impressive than
it reads. **Small concern in that specific case**, because the mechanism fires
per drone-idle-tick over an article holding 73 idle drones, i.e. fast rather
than slow, so a zero would not need hours to be meaningful. **Still: session
uptimes were not recorded alongside the counts, and they should be.** Routed to
prompt 12's QA.

**⭐ The distinction that actually makes this datum usable.** Two different
claims are hiding in "58 hours, zero crashes", and they need different evidence:
- *"The pack improves on vanilla stability"* — **needs the control we do not
  have. Unsupported. Do not claim it.**
- *"The pack does not DESTABILISE a heavily loaded colony"* — **needs no vanilla
  arm at all**, because the question is whether *we* broke something, and the
  baseline is "a game that works". On that question, ~58 hours of deliberately
  overloaded play with zero crashes and zero `[LUA ERROR]` on clean runs is a
  real negative-safety result, and a relevant one given F86 exists precisely
  because our code can reach the save. **That is the version worth having, and
  it is already true.**

**The mechanistic case is real, though, and worth stating because it is what
would make the observation more than luck.** Several fixes repair exactly the
class §10.6f describes — persisted bad state: F81's stranded
`g_DisastersPredicted` key, F02/F78/F88/F89's wedged threads, C34's
stale-ACTIVE rain state, F64's leaked train prefabs, F35's missing label
modifiers. **If defects surface as instability, fixing state corruption should
reduce instability.** That is a plausible mechanism, not a measurement.

**⭐ The controlled version of this claim already exists, and it is stronger
than crash-counting: our A/B legs count `[LUA ERROR]` directly** — the thing
§10.6f argues *precedes* crashes — and they report zero with the pack applied on
clean runs (e.g. `63/0/15/0`; PT-58's *"zero `[LUA ERROR]` of any kind"*).
**That is the number to cite. "It never crashed" is the anecdote; the error
count is the instrument.**

⚠️ **PUBLICATION TRAP, flagged because this is exactly where it would go
wrong.** "58 hours, zero crashes" is a tempting line for `MOD_DESCRIPTION.md`
and **it would fail this project's own evidence bar** — the same bar that kept
the no-precedent uninstall sentence unpublished. A stability claim needs a
control; we do not have one. **Do not ship it.**
