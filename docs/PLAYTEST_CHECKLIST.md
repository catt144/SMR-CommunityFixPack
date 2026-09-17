# Playtest checklist — the owner's list

## Must_Read_Header
<!-- RULES -->
Rule: Admit an item only when its next action is the owner's: a ruling in words, or a test only the owner can run. [A3: pass]
Rule: Write each item as `### ck<n> · opened <date>`, its ask, at most six bullet lines and a `Home:` line. [A3: pass]
Rule: Never change an item's opened date; at 30 days old it is purged or archived, however recently it was touched. [A3: pass]
Rule: Delete an item in the commit that records the owner's action on it. [A3: pass]
<!-- /RULES -->

What waits on your word or your hands, and nothing else. doccheck enforces the format and the age;
the sweep in `docs/agent/prompts/perma/STATE_EVICTION.md` clears what ages out. Old bodies are in
`docs/archive/PLAYTEST_ARCHIVE.md` under `## ck<number>`.

## Decide

### ck203 · opened 2026-09-17
C83 sent the reporter's botanists to a habitat that refuses them (C106): pursue it or drop it?
- They lived, homeless inside or beside the habitat; without C83 they would have walked to a dead dome.
- Needs a colony whose only live communities are habitats that refuse the arrivals. You called it niche.
- Also in C106: C83's one log line prints `table: …` and a blank destination. That is cheap to fix on its own.
Home: `docs/agent/bugs/C106.md`

### ck201 · opened 2026-09-17
Political Animal can't be earned on 1.1.0 (C104): build a fix, send the devs a report, or neither?
- For everyone: Night Shift Compensations and Right to Rest each block the other, and both count.
  Norman owners also have Secondary Produce vs GMO. A Politician can never enact Efficient Assembly.
- All three are new in 1.1.0. The devs edited this very achievement check in the same patch.
- Cheapest fix: stop counting one law of each pair, plus Efficient Assembly. Which half is your call.
- On PlayStation, Xbox and the Microsoft Store any mod blocks achievements, so a fix only helps Steam.
- Your C92 ruling (build and test, shipping held) was for C92. Say whether it covers this too.
Home: `docs/agent/bugs/C104.md`

### ck199 · opened 2026-09-16
Which of these WORKFLOW rules retire, each lapsed on the evidence but with no word of yours retiring it?
- Tag every upload per mod (Release marking, 08-17): the only tags are `fixpack-v1.0.0` and
  `v5-game-1.0.7`, and v11 is live.
- The `[FAQ]` tag convention (08-01): it collected material for an FAQ the site now has.
- Credit ChoGGi and LukeH as prior art (Release): no store card, site page or `metadata.lua` does.
- Execution markers on console lines in human docs (08-03): those docs carry no console lines now;
  entries and reports still use the markers, so the rule may just need its scope reworded.
Home: `docs/agent/WORKFLOW.md`

### ck188a · opened 2026-09-17
Who reported Wildfire, and do you take the five-minute live look or drop it?
- F120, the report and the handoff name Jäger, but his comment #8 is C99's tunnel bug and you said
  "jager was completely different". Your answer corrects or confirms the name in all three.
- The look: on a 1.1.0 colony, does SPECIAL show the cure node without panning, and does Ctrl-F
  "Wildfire" find it? Any save, scratch copy, recipe Leg A. Drop it and the report closes unexplained.
Home: `docs/agent/bugs/F120.md`, `docs/archive/PLAYTEST_ARCHIVE.md`

### ck188b · opened 2026-09-17
Habitat residents walk out on their own: a defect, or the price of the building?
- Measured 09-16 on your habitat beside DomeMega: five jobless residents never leave. The habitat
  copied 8 of the dome's workplaces onto its own list when built; a free slot in any of them counts
  as work at home, though no resident can ever be hired there (EF-107).
- So the drain is real only for a habitat with no free listed slot, such as Dermot's remote one.
- Adding the guard the dome's own sweep has would drain every habitat built beside a dome.
  Nothing is authored until you say.
Home: `docs/agent/bugs/C100.md`

### ck186 · opened 2026-09-17
What numbers do the skill caps get?
- Proposed, not set: warn 3,072 B, hard 5,120 B. Read current sizes from doccheck's SKILLS section.
- The largest skill would sit close to the proposed hard cap. Caps stay down until you pick.
Home: `docs/archive/PLAYTEST_ARCHIVE.md`

### ck183a · opened 2026-09-17
Which SMR Tool Kit design calls do you make?
- Where the slot engine lives once triggers move to Run: its own page, or riding with Probes.
- Defect 20's remedy: a cursor change, or a persistent banner.
- The cut Stamper is un-parked only in your words; it sits in FUTURE_IDEAS.
Home: `docs/archive/PLAYTEST_ARCHIVE.md`

### ck181 · opened 2026-09-17
When do we sit the attended monolith audit that closes the doc overhaul?
- Your ruling 09-14: automate first, then a you-and-me pass over `WORKFLOW.md` and `FIX_POLICY.md`.
  No agent closes the overhaul alone.
- Your answer also ends 178, STATE's temporary +25% warn cap.
Home: `docs/archive/PLAYTEST_ARCHIVE.md`

### ck172 · opened 2026-09-17
Does C92 (restore the technology) ever ship?
- Build option B proceeds; no release, outbox entry or public row until you lift the hold in words.
- The test needs your hands: move `account.dat` aside, test, move it back (EF-094); it resets your
  account options until restored. 171's scope question is overtaken by B.
Home: `docs/agent/prompts/C92_ACHIEVEMENT_BUILD.md`, `docs/archive/PLAYTEST_ARCHIVE.md`

### ck148 · opened 2026-09-17
Do the fix toggles start, and how do you answer their three open calls?
- Deferred on your "skip". Start means firing `01_SPEC_fable.md`; links 03 (about 30 minutes) and
  11 (longer) are your sittings.
- The calls: (a) console players, (b) release gate, (c) who cut the chain.
Home: `docs/agent/prompts/fixtoggles/01_SPEC_fable.md`, `docs/archive/PLAYTEST_ARCHIVE.md`

### ck136 · opened 2026-09-17
Do you spend a profiling sitting on FR-3 (frame skip and stutter)?
- Its gate ("decide after link 99") has fired. One profiler session on a large colony would settle
  FR-3 and decide C60 and C81; a source read cannot measure frame time.
Home: `docs/archive/PLAYTEST_ARCHIVE.md`

## Run

### ck202 · opened 2026-09-17
When you next play a colony with a staffed Water Reclamation spire, one read settles C105.
- The code says the upgrade keeps the saving, but at 50%; a well-staffed spire can reach 70%.
- On any colony with a staffed spire, SMRTK-dump the spire and its dome, build the upgrade (granting
  `JumboCaveUpgrades` is fine), and dump both again.
- Not a bug if the spire then reads performance 100 and the dome's reclamation modifier reads -50.
- Invalid if another staffed spire shares the dome, or if the spire was already at 100 or less.
Home: `docs/agent/bugs/C105.md`

### ck200 · opened 2026-09-16
When you next play, run the C95 rebuild's two short legs; lines and witnesses are in the report's "Owner sitting".
- UI expedition crewed from habitat 2096 on a copy of BUG.savegame.sav: watch its resident land back inside.
- Pack disabled, full restart, load C95PLACEMID: watch the returnees finish home with no error.
- Provision a distant inhabited habitat with rail to the pad. The current fixture has none; this needs provisioning.
- Provision a live reachable dome beyond the nearest; switch the nearest off and watch a returnee reach the live dome.
- Open: with no safe dome anywhere, does the game's own choice stand? Recommended: keep it.
- The reporter's actual pack version is still unknown; ask it if you want their reported departure explained.
Home: `docs/agent/reports/C95_PLACE_HOME_BUILD.md`, `docs/agent/bugs/C95.md`, `docs/agent/bugs/C102.md`

### ck183b · opened 2026-09-17
When you next boot with SMRTK, confirm 09's menu layout and the `MechanizedDepotFood` numbers print.
Home: `docs/archive/PLAYTEST_ARCHIVE.md`

### ck169 · opened 2026-09-17
When the site's content changes, fire `workflow_dispatch` on the site repo.
Home: `docs/UPLOAD_WORKFLOW.md`

### ck192 · opened 2026-09-17
When colonists queue at a platform forever or walk past a working station, call an agent first.
- Adding trains destroys the evidence.
Home: `docs/agent/bugs/F80.md`

### ck193 · opened 2026-09-17
When you are near any working train line, take the two reads that re-earn F21's `tested` (optional).
Home: `docs/agent/bugs/F21.md`

### ck194 · opened 2026-09-17
When a colony meets an entry's takeable condition, run its recipe: C40, C42, F99.
Home: `docs/agent/bugs/C40.md`, `docs/agent/bugs/C42.md`, `docs/agent/bugs/F99.md`

### ck195 · opened 2026-09-17
When you reach a finished Mirror Sphere site or Mystery 10's epilogue, run the entry's procedure.
Home: `docs/agent/bugs/F16.md`, `docs/agent/bugs/F06.md`

### ck196 · opened 2026-09-17
When a depot click-load picks the wrong depot again, use the workaround command in F76.
Home: `docs/agent/bugs/F76.md`, `docs/agent/bugs/C41.md`

### ck197 · opened 2026-09-17
When a food seam's TAKEABLE line comes true (C56 to C61), run that entry's read.
Home: `docs/agent/bugs/C56.md`

### ck198 · opened 2026-09-17
When you want the number, take the both-packs stacked leg; information only, never a release gate.
Home: `docs/archive/PLAYTEST_ARCHIVE.md`
