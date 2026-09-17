# Replies to player reports — drafts to post, and what went up

⛔⛔ **REPLIES ARE PULL-ONLY — owner ruling, 2026-09-12 (checklist 165). THIS IS THE FIRST
THING TO READ IN THIS FILE.** *"We are gonna move replies to pull only, when I ask for them, not
agent tracked. We keep getting side tracked with replies. Replies are as we can do them, our
primary focus is fixing bugs, not a messaging service."*

**What that means, for agents, in order of how often it will be got wrong:**

1. ⛔ **Do NOT draft a reply unless the owner asks for one in that session.** A new field report
   is not a request for a draft.
2. ⛔ **Do NOT put replies on the owner's owed list** — not in `STATE.md`'s OWES line, not in a
   handoff's "decisions owed" table, not in a session summary's "waiting on you". They are not
   owed. They are pulled.
3. ⛔ **Do NOT raise a `DRAFT` sitting in this file as a prompt, a nudge, or a "while you're
   here".** A draft waiting here is **not** a task in progress. It waits indefinitely, by design.
4. ⛔ **Do NOT gate any other work on a reply going out**, and never let a reply's wording block a
   fix, a release or a sitting.
5. ✅ **When the owner DOES ask** — "draft a reply to X", "what do we say to Y" — draft it here,
   to the usual standard, and stop. One ask, one draft, no follow-on queue.

✅ **WHAT THIS RULING DOES NOT TOUCH — read this before narrowing anything:** a player's report is
still **evidence about a defect**, and triaging one into `agent/bugs/` is **ordinary bug-fixing
work that continues exactly as before**. The pack exists because players tell us things. What is
pull-only is the **messaging** — writing and chasing the reply. ⛔ Never use this rule to justify
not filing, not reading, or not investigating a report.

⚖️ **The condition it was ruled under** (WORKFLOW, Records and rulings — record the state, re-read it before
treating it as binding): the owner had **fielded a load of reply questions in a single day** while
the project's actual gate was an unrun playtest. The cost being cut is **owner attention diverted
from fixing bugs**, not the replies themselves.

⛔ **DEVELOPER REPORTS ARE THE SAME CLASS — owner ruling, 2026-09-16 (checklist 151 (b)).** *"dev
reports are only on request by the devs so that belongs in field_report_replies which is pull
only"*. A report written for the game's developers is **sent only when the developers ask for
one**. Until then it is never owed, never on a list, and never raised; the report stays in
`agent/reports/` as the record. Today that is
[`MIGRATION_DEV_REPORT.md`](agent/reports/MIGRATION_DEV_REPORT.md) — unsent, and if it is ever
asked for, the covering note must not claim the migration passes are finished (checklist 168 (d)).

---

**For you (the owner):** each section below is a reply drafted for a player's report
on Steam, Reddit or GitHub. Post the ones you want, whenever you want; nothing here
expires and nothing here is chasing you. Tell an agent what went up and it records
that under "What was actually posted". Every reply: check the thread first (skip it
if it is already answered), no version numbers, and no fix promise until the fix is
tested.

**For agents:** a reply is not authority — the `agent/bugs/` entries are. Drafts
live here because posting is the owner's action; update a draft in the same commit
that changes the fact it states. Moved here from `agent/reports/` on 2026-09-11
(owner ask); older records cite the old path.

## The status line — read this before adding or cutting a draft

Every draft carries **one line under its title, before its quote block**:

```
`STATUS: <token>` · thread: <Steam|Reddit|GH #n> · subject: <ID> · drafted <YYYY-MM-DD> · gate: <ck###|none>
```

**Exactly four tokens, no others:**

| token | means |
|---|---|
| `DRAFT` | written, not posted, nothing blocking it but the owner's decision |
| `POSTED <YYYY-MM-DDThh:mmZ>` | it went up; the timestamp is the posting time |
| `SUPERSEDED by <section>` | a later draft in this file replaces it |
| `HELD on <gate>` | it must not go up until that checklist item is answered |

⇒ **A draft that reaches `POSTED` or `SUPERSEDED` is CUT at the next release sweep**,
and its timestamp is appended to "What was actually posted". This file is a queue of
live drafts plus a permanent record — never an archive of dead text. `HELD` is not a
cut condition: a held draft stays whole until its gate is answered.

⇒ **Nothing below is owed by anyone but the owner.** Every live draft is an owner
post, so the "owed" list is just the `DRAFT` and `HELD` lines below — there is no
separate table to keep in step. (Removed 2026-09-12; it derived from these headers
in full.)

## Context — the short version

* **Every fact in a draft belongs to a bug entry, not to this file.** The entry is
  the authority; cite it, do not restate it.
* **Voice** (`reports/still-needed/WORDING_RULED.md`): plain for players, precise for
  the two developers who read us, no hedging words. Say what the fix does and for whom.

⚖️ **OWNER RULING 2026-08-23 — kept verbatim, because this is its only home. It is why
a draft may name another mod:**

> *"We can't just say it's not our mod, we need to explain that it's the other mod,
> and why… it's not fair to users to just say it's not our issue, we don't need to
> slander anyone but it's also clear that that other mod has been abandoned as far as
> we can tell, it's not our job to protect them either."*

⇒ `FIX_POLICY` §8 still binds **store pages and load-order advice**; this ruling covers
**issue replies**. Recorded on checklist 73; §8 should absorb it on its next edit.
⚠️ **But "abandoned" is our inference**, from dates and metadata (Passage Network's last
update 2025-12-11, `saved_with_revision` 384011 vs game 396349) — **not a statement from
the author.** A draft says *"hasn't been updated for the current build"*, never
*"abandoned"*. Keep it that way.

---

## Field reports triaged 2026-09-11 (checklist 146 / 147 / 150 / 153)

Source: `reports/FIELD_LEADS_2026-09-11.md`. ⛔ Desk reads unless a draft says otherwise.
Check each thread first; skip a draft if it is already answered.

**Wildfire cure rocket stuck — F119**

`STATUS: DRAFT` · thread: Reddit · subject: F119 · drafted 2026-09-11 · gate: ck146

> This looks like a real bug in the game, and the Advanced Martian Engines hunch is right on target. The cargo rocket Earth sends works out how much fuel it needs once, when it lands. If the fuel cost changes while it's sitting on the pad (finishing Advanced Martian Engines cuts it by 20, which is exactly your "20 fuel to unload"), the rocket ends up holding fuel it no longer needs, and nothing is set up to take it off. The Fuel Conservation law can do the same. We've fixed this for the Relaunched Fix Pack — it's in the update that went out on 11 September, and it also repairs a rocket that's already stuck the moment you load your save. If you have a save from before that rocket landed, loading it and holding off on Advanced Martian Engines (and on changing Fuel Conservation) until the rocket has left avoids it too.

⛔ The save-reload advice is INFERRED, not route-checked. Do NOT mention the console: whether Relaunched players can open
one is unchecked, and PS5 has none. ✅ The load-heal claim is OBSERVED (`F119.md` §Attended check, 2026-09-11): a
pre-stuck rocket reloaded and left. ✅ `tested-attended` in play (checklist 149) and LIVE in v8.

**Deep scan finds nothing ("Possible Bug") — C86**

`STATUS: DRAFT` · thread: Steam · subject: C86 · drafted 2026-09-11 · gate: ck147

> Orbital probes only deep-scan once you've researched Adapted Probes. Deep Scanning on its own doesn't change probes; it lets your normal sector scans find deep deposits when a sector is scanned again. So probes launched before Adapted Probes only do a normal scan, which matches what you saw. One small real bug turned up while checking: with the five-sector Advanced Orbital Probe and no Adapted Probes, a neighbouring sector you had already deep-scanned gets marked back to "Scanned", and scanning it again finds nothing new. We've fixed that too — it's in the update that went out on 11 September.

✅ `tested-attended` in play (checklist 149) and LIVE in v8.

**Russia's "3 manned Extractors at 160% Performance" goal (Pancer1900) — no bug; see `agent/bugs/F108.md`**

`STATUS: DRAFT` · thread: Reddit · subject: F108 · drafted 2026-09-11 · gate: none

✅ **Approved to post — owner ruled YES on checklist 153, 2026-09-12.** The gate is discharged; nothing holds
this but the owner's click. Not posted as of 2026-09-12.

> **TL;DR — Performance and Production are two different numbers, and none of the extractor upgrades touch Performance.**
>
> Amplify, Fueled Extractor and Magnetic Extraction all boost **Production**. They've never added to **Performance**, in this update or the last one, so nothing changed there. The goal only counts Performance — and Performance comes almost entirely from the colonists working the building.
>
> A colonist's Performance is **50 + their Morale**. Perfect Morale on its own is ~150, which is exactly where you're stuck. Everything past that has to be stacked:
>
> **Traits that help**
> • Workaholic **+20**
> • Enthusiast **+20** — only while Morale is in the green
>
> **Traits to move out of those three buildings**
> • Renegade **−50**
> • Refugee **−40**
> • Lazy **−20**
> • Melancholic **−20** — whenever Morale drops into the red
> • Alcoholic **−10**
>
> **Specialisation — the biggest single lever**
> • Extractors want **Geologists**. A worker with the wrong specialisation is **−50**, which outweighs every trait above put together. Staff all three with Geologists first, then worry about traits.
> • Make sure they live in the dome they work in — working in another dome is **−10**.
>
> **Laws, techs and bonuses**
> • **Single Shift** law — **+40** to buildings running one active shift. Biggest thing you can switch on today.
> • **Double Shifts** +20 · **Triple Shifts** +10
> • **Productivity** law (Welfare) — **+10** for colonists with high Comfort
> • **Vocation-Oriented Society** tech — **+10** while Morale, Health, Sanity *and* Comfort are all green
> • **Heavy workload** — **+25** (it was +20 before the update, so this one actually got better)
> • Astrogeologist commander is +20 Extractor Performance, but that's a new-game pick, not something you can add mid-run
>
> Last thing, and it should save you a lot of grief: **the goal is checked once an hour and locks in as soon as it's met**, so all three extractors only have to be at 160 at the *same* check. You don't have to hold it there.

⚠️ Every number above is SOURCE on 1.1.0.403908 and diffed against the 1.0.7 archive: trait amounts
`Data/TraitPreset.lua`; `NonSpecialistPerformancePenalty` 50 / `NonHomeDomePerformancePenalty` 10 /
`OvertimedShiftPerformance` 25 (was 20) `Lua/__const.lua`; shift + Productivity laws `Data/LawDef/LawDef-Economy.lua`
`:1526/:1620/:1706` and `LawDef-Welfare.lua:347`; Vocation-Oriented Society `param1` 10 `Data/Tech.lua:2155-2163`;
Astrogeologist `Data/CommanderProfilePreset.lua:329-341`; `specialist = "geologist"` on both extractor templates.
✅ The hourly-check-and-latch claim rests on `Data/SponsorGoals.lua:557-576` plus our OWN attended run
(`F108.md`, 2026-08-28, goal ticked 3/3 and completed) — not on a player report.
⛔ Do NOT repeat F108's old "Amplify upgrade helped reach 160" line; it is corrected in that entry.
⚠️ Says nothing about the pack — this player has not said they use it and the answer is the same either way.
⛔ Do not tell them to avoid Extractor AI: on 1.1.0 vanilla no longer caps a staffed extractor at 50, so that
advice is stale. ⚠️ Enthusiast/Melancholic fire on `HighStatLevel`/`LowStatLevel` (70%/30%), `Colonist.lua:4864-4873`.

**Reply to the developer (ivanassen, post #7 in the Building Codes thread) — C88 + F37 + "where do you collect your bugs?"**

`STATUS: POSTED 2026-09-12` · thread: Steam · subject: C88 + F37 · drafted 2026-09-11 · gate: ck150 (a) — discharged

✅ **POSTED — owner-stated 2026-09-12; ck150 (a) is CLOSED.** The owner posted it and used **the majority of
A+B**: the sources paragraph **and** the line naming AI-assisted research and code review. ⚠️ **No posting
timestamp was given** — there is no API for a Steam comment, so the date is the day the owner said so, not a
read time, and the status line carries a date where the convention wants `YYYY-MM-DDThh:mmZ`. The row is in the
Steam table under "What was actually posted". ⇒ This draft is CUT at the next release sweep.

Drafted 2026-09-11 by `smr-bugfixpack-e6`. The farm paragraph was re-read on 1.1.0.403908 (F37's 1.1.0 section). The
owner picked the last paragraph (checklist 150 a).

> Thanks, that's great to hear. We'll add a fix for the prefab exemption to the pack and have it step aside by itself once your patch is out.
>
> On the farm oxygen one: you're right, and thanks for checking it. Our entry was written against 1.0.7, where a farm applied its oxygen bonus even while it wasn't working, so salvaging one that had never started work left the bonus on the dome. In 1.1.0 the bonus is only applied while the farm is working, and destroying or salvaging it switches working off while it's still attached to the dome (`Building:Destroy`, Building.lua 1560–1570; the dome is only cleared later, from `Done` at 537), so it can't leak any more. We'll retire that fix.
>
> **[A]** As for where the bugs come from: player reports mostly (Steam discussions and reviews, the Paradox forums, Reddit, and comments on our mod pages), plus reading the game's shipped Lua directly. We only ship a fix once we've found the cause in the code, and where we can we reproduce it in play with the fix off and on. Every fix on our list cites the file and line it repairs, and I'm happy to send the code reading and repro steps for any you're looking at, e.g. the colonist-migration ones.
>
> **[B, add to A]** We use AI-assisted research and code review to sweep the reports and the source; nothing ships on that alone, and each fix is checked against the code and tested.

✅ *"We'll retire that fix"* stands as written — checklist **156 ruled the farm-oxygen retirement YES** (2026-09-12),
which discharges the old "keep only if 150 (c) rules yes" condition on this paragraph.

**Lakes, "excavation too deep" — C87**

`STATUS: DRAFT` · thread: Steam · subject: C87 · drafted 2026-09-11 · **re-drafted 2026-09-12** · gate: none

✅ **THE HOLD IS DISCHARGED, and the check behind it will NOT be run — owner ruling, checklist 162 (c),
2026-09-12: "a lead not a test … only ever had one report … not spending time to run it down."** C87 is
**file-and-watch**. ⛔ The previous draft's closing clause — *"we're checking whether it happens on every
1.1.0 map"* — **promised work this project has now decided not to do, so it is removed rather than left to
go quietly false.** Nothing else in the reply depended on the check: every sentence below is source-derived
and true whether the warning turns out to be universal on 1.1.0 or specific to that player's map.

> Worth sending through the in-game report tool as the developer asked — that's the route that puts it in front of them. That warning means the game thinks the lake's bottom would end up below the lowest height the map allows, but your spot is ordinary flat ground, so it shouldn't fire there. The code that makes that decision is unchanged from the last version, so something it reads must have changed instead. The Relaunched Fix Pack doesn't touch lakes, so this one isn't ours either way — but the more detail you can put in that report, the better their chances of pinning it down.

⚠️ Revised 2026-09-11 after the owner's pushback (the first draft blamed very low ground; the player's screenshot shows
ordinary ground).

**Meteors — optional; recommendation (checklist 147): skip**

`STATUS: DRAFT` · thread: Steam · subject: none (no bug) · drafted 2026-09-11 · gate: ck147

> Meteors land at random spots across the whole map, and the way the spot is picked didn't change in the update, so a bigger base simply gets hit more often. The Relaunched Fix Pack doesn't change meteors any more.

---

## Field report triaged 2026-09-12 (checklist 157) — C89

**Prosperity for Mars "angry" about unemployment with 0 unemployed (Madmouse Ked)**

`STATUS: DRAFT` · thread: Steam · subject: C89 · drafted 2026-09-12 · gate: ck157 (a)

Drafted 2026-09-12 by `smr-bugfixpack-d0`. Not ours; the cause is inferred from the code, not reproduced, so the
reply asks for the two facts that decide it. Plain register, no hedging words.

> Thanks for the report. That one is the game's own faction logic rather than anything the fix pack changes, and here
> is what we can see in the code: the faction's "high unemployment" mark is checked once per game hour, and it counts
> any dome where one in ten colonists who could work has no job at that moment. So a single idle colonist in a small
> dome, a shift change, or a building you just switched off can set it at the top of the hour, and the panel keeps
> showing it until the next hour even though the Unemployed number at the top of the screen is already back to 0.
>
> Two things would tell us whether it is only that or something more:
> 1. Does the faction panel still list "Domes with more than 10% Unemployment" an hour or more later, with the top
>    bar still at 0?
> 2. Roughly how many colonists are in your smallest dome?
>
> If it stays on across hours, a save would let us pin it exactly, and we will pass it to the developers with the
> code lines.

**For the developers — C89** (owner posts where they read us)

`STATUS: DRAFT` · thread: Steam · subject: C89 · drafted 2026-09-12 · gate: ck157 (b)

> Faction "unemployment" dislikes fire on tiny domes, and four of five presets lack the guard the fifth has.
> `JusticeMovement.lua:104` gates `JusticeUnemployment` with `#obj.labels.Colonist >= 10 and …` (and `:129` for
> Homeless). `ProsperityForMars.lua:225`, `MarsDemocraticParty.lua:88`, `WorkersParty.lua:114` and `NewSol.lua:47`
> use the bare `#Unemployed * 100 >= 10 * #Colonist` (Homeless twins at `MarsDemocraticParty.lua:107`,
> `WorkersParty.lua:133`, `NewSol.lua:66`), so one idle colonist in a dome of nine is "more than 10%". Because
> `RecalcFactionsApproval` runs on `NewHour` and stores the list, and `AddFactionLikeDislikeNotification` fires for
> any id absent the previous hour, a one-hour blip on a small dome notifies the player while the top-bar count is
> already 0; at hour 0 the same snapshot feeds `EvalTension`. On large colonies the blips are long: a colonist who
> loses a job re-checks only every `Clamp(#Colonist / 300, 0, 12)` hours (`City.lua:118`). Same on 1.0.7. Player
> report: Steam, 2026-09-12.

---

## Built for v10 — three reply lines, drafted 2026-09-12 (checklist 158)

Drafted by `smr-bugfixpack-aa` when C85, C88 and C89 were built. **Drafts only; the owner posts.**
⛔ None of the three has been watched in a game yet (checklist 158), so nothing below claims it was.

**1 · The Building Codes thread — the developer's own thread (`ivanassen`), C88**

`STATUS: DRAFT` · thread: Steam · subject: C88 · drafted 2026-09-12 · gate: ck158

Post this where the developer answered. It is the one thread where a fix of ours is something they asked for.

> Done — it is in the next update of the pack. Both versions of the law now apply their maintenance change to
> prefab-deployed buildings, at whatever value the law is set to, and it reads that value from the law itself
> rather than carrying its own copy. It applies to buildings completed after the update: the finished building
> does not record that it came from a prefab, so there is nothing on an existing one to go by.
>
> It is written to get out of your way when your patch lands. Our modifier carries the law's own id, so once
> your handler applies it too the second write is a no-op and there is exactly one modifier, in either order —
> and the module checks the shipped handler at startup, so the moment it stops skipping prefabs ours switches
> itself off. No version check involved.
>
> One thing we found next door while doing it, in case it is useful: the maintenance half of Building Codes
> survives the law's repeal. The cost half is a `LawEffectModifyLabel` and its `OnStop` reverts it, but the
> maintenance half is the `ConstructionComplete` `MsgReaction`, and no `OnMsg.LawDeactivated` handler clears
> `maintenance_resource_amount` — `SavegameFixups.RemoveRepealedBuildingCodesMaintenance` is the only sweep,
> and it runs once per save. So a repeal after that sweep keeps the change. Ours behaves identically, on
> purpose, because it uses your id.

**2 · The clogged-producer reporters — C85 (two Steam players, "Clogged Extractor")**

`STATUS: DRAFT` · thread: Steam · subject: C85 · drafted 2026-09-12 · gate: ck158

Both said destroy-and-rebuild was the only way out; the important part for them is that they do not have to.
This replaces the 2026-09-11 diagnostic draft, which asked which popup answer they picked — moot now the fix
repairs the building whichever answer it was.

> The next update fixes this, and it repairs the buildings you already have — you do not need to rebuild
> anything. When you load a save, any building still stuck on "Clogged after a Dust Storm." is switched back
> on, and it checks again once a day after that. A building that is still waiting on your answer, or that is
> off because you chose "we'll fix it after the storm", is left alone.
>
> What happens is that the dust-storm event switches the building off before it asks you what to do, and if
> that question is ever lost — saving and reloading while it is on screen will do it — nothing switches the
> building back on. The game already has the timer that would have handled it; this one event does not use it.
> We have passed that to the developers.

**3 · The C89 reporter — appended to the C89 draft above (`Madmouse Ked`)**

`STATUS: DRAFT` · thread: Steam · subject: C89 · drafted 2026-09-12 · gate: ck158

⚖️ Append this to the C89 "not ours" reply rather than replacing it: the sampling half of what they saw is
still the game's and is not something we change. **Say "judgment call" plainly.**

> Following up: the next update does change one part of this, as a judgment call rather than a bug fix. Four of
> the five factions count a dome of any size when they check for "more than 10% unemployment", so one idle
> colonist in a dome of three counts. The Justice Movement's identical dislike waits until a dome has ten
> colonists. From the next update all five use that same ten-colonist rule, and homelessness too.
>
> That will stop it on small and half-built domes, which is where it is most annoying. It does not change how
> often the game checks, so if you are seeing it on a dome of ten or more we would still like the answers to
> the two questions above.

---

# What was actually posted — the permanent record

Read this before drafting anything new. GitHub rows re-pulled from the JSON API
**2026-09-12**; the comment count is the control and it matched on all three.

## GitHub — `github.com/catt144/SMR-CommunityFixPack/issues`

All three issues are **closed** (`state_reason: completed`) and all three are from the
same reporter, **Keelai**. Tie a number to an entry by its **attached log name**, not
its title.

| issue | title | entry | comments | closed | label |
|---|---|---|---|---|---|
| **#1** | *"Colonist stuck homeless"* | **F104** | 3 | 2026-08-24T06:01:47Z | *(none)* |
| **#2** | *"Error when completing milestone"* | **F105** | 4 | 2026-08-24T22:30:10Z | `Fixed` |
| **#3** | *"Jumbo cave reinforcements"* | **F110** | 3 | 2026-08-30T21:35:56Z | `Fixed` |

**#1 / F104** — the first field report the pack ever received. Keelai volunteers the
workplace half of the symptom 08-23T13:28:55Z; **the owner posts Draft A essentially
verbatim 2026-08-24T03:40:35Z**, naming Passage Network; issue closed 06:01:47Z; Keelai
08-24T19:24:28Z — *"Yeah i had a hunch that mod might be the problem but thanks for
checking :)"*. Closure gate (a reply **and** the reporter's confirmation) met; the entry
is `closed`. The draft is cut; its one unverified paragraph (the ≥1200 m
`ColonistMinDistToIgnorePassage` shuttle hunch, `Dome.lua:256-259`) was flagged as
derived-only and is screened out as a cause on `F104`.

**#2 / F105** — ⚠️ **the first posted reply was NOT the draft in this repo.** Owner asks
for a save and which store 08-24T01:57:13Z; **owner posts a full F105 explanation
08-24T06:04:29Z, written before the rig legs ran**; Keelai 08-24T19:23:00Z — *"Nice and
thanks :) ill try and include both save and log in the future"*; **the owner posts Draft C
verbatim 2026-08-24T22:28:51Z** and closes the issue two minutes later. Four sentences of
the 06:04 reply are stronger than the tree can support — the numbered list below.
⇒ **The subject is retired.** 1.1.0 added the identical guard itself
(`ConstructionSite.lua:721`) and `Fix_LandscapeCostRefresh` was removed from the pack in
hotfix 2 (`F105.md`, decision 98). The unposted "Draft B" first reply was cut 2026-09-12:
it promised a fix that is no longer in the pack, so it could not be posted to anyone.

**#3 / F110** — *"Jumbo cave reinforcements"*, opened 2026-08-29T02:42:43Z with a log and a
Reddit link (thread `1un7ols`); the wonder wedged on clearing waste rock. Owner
08-30T17:52:52Z: it is vanilla, no mod involved, and asks for a save because the trigger
had never been reproducible. Keelai 08-30T18:15:51Z supplies one by Google Drive. Owner
08-30T21:35:56Z: *"Fix built, tested, and update is out now. Thanks for the save, that is
exactly what I have needed to close this. :)"* — issue closed the same minute, labelled
`Fixed`. That save is what promoted C25 to **F110** and it is the entry's confirmation
evidence (`Fix_JumboCaveReinforcementWedge.lua`). **No reply for this issue was ever
drafted here** — the owner answered it directly; recorded 2026-09-12 so the record is
complete.

### ⛔ The four overreaches in #2's 06:04 reply — never copy these onto another surface

⭐ It is a good reply and the reporter is satisfied; nothing here needs a correction
posted. But it was written **hours before** legs A–D. ⛔ **Do not copy any of these onto
the fix list, a store card or `last_changes`** — those surfaces have no reporter goodwill
to spend and no thread to correct them in.

1. ⛔ *"It also **repairs saves** that already have a levelling job in the broken
   state"* — **we do not repair anything.** `F105`: the site stays broken, the
   guard makes it harmless. The *player outcome* in that sentence is right and is
   witnessed (leg D: install after the fact, zero `:673`, nothing to demolish) —
   the mechanism is not. Say **"stops it happening on a save it is already
   happening in"**, never "repairs".
2. ⚠️ *"**Only three** technologies in the game carry the effect"* — that is the
   `Effect_ModifyLabel` label-sweep set only. `OnMsg.ConstructionCostChanged`
   (`ConstructionSite.lua:2832`) is a second, class-filtered reader route **not
   ruled out by measurement**. The same guard covers it, so the fix claim is
   unaffected — the *"only"* is what overreaches.
3. ⚠️ *"it would just go **quietly to the log with no warning box**"* — the
   measured half is `Mod Flagged` = 0 with the pack off, in all three legs, and
   the raise still logging uncaught. The absence of a **box on screen** was never
   recorded by a witness, and screen claims need an attended one.
4. ⚠️ *"it happens with **no mods installed at all**"* — derived at source
   (`ConstructionSite.lua:673` is vanilla), and every pack-OFF leg still ran with
   the rig's other junctions present. Never witnessed on a clean install.

## Steam — no API, so these are owner-stated

⛔ There is no machine-readable record of a Steam comment thread. Each row below is the
**owner's own statement**, recorded on the date given; nothing here was verified by a tool.

| what | subject | posted | how it is known |
|---|---|---|---|
| The C74 sounds reply ("you were right, and it wasn't only the hammer…") | C74 / C77 | with the **v7** update, 2026-09-10 | **owner-stated 2026-09-12** |
| The C83 rocket-arrivals reply ("no listed fix covered this…") | C83 | with the **v7** update, 2026-09-10 | **owner-stated 2026-09-12** |
| The Building Codes code reading + "is excluding prefabs intended?" question | C88 | 2026-09-11 | posted and **answered** — `ivanassen [developer]`: *"Excluding prefabs is wrong, and will be fixed in the next patch - until then, please include it in your mod."* (`C88.md` §"The devs' answer (2026-09-11)") |
| The reply to `ivanassen` (prefab fix + farm-oxygen retirement + "where do you collect your bugs?") | C88 + F37 | 2026-09-12 | **owner-stated 2026-09-12**, no timestamp given. The owner used **the majority of A+B** — the sources paragraph plus the line naming AI-assisted research and code review. Closes checklist 150 (a) |

Both C74/C83 replies said **"Today's update"**, meaning v7. **v8 and v9 have both shipped
since** (2026-09-11, checklist 155), so a follow-up on either thread must not reuse that
phrase. Their standing caveats, which still bind any future wording:
⛔ do not add *"like the original game"* to the C74 reply — whether the 2018 release played
the hammer is the reporter's memory, never checked (`C77` §What is NOT established);
⛔ do not say the colonists in the bad dome died — the owner's run saw the **Suffocation!**
warning but did not wait it out (`C83` §OBSERVED).

## Cut from this file, and why

| cut | date | why |
|---|---|---|
| Draft A (F104) | 2026-09-12 | POSTED 2026-08-24T03:40Z verbatim; #1 closed |
| Draft B (F105), never posted | 2026-09-12 | subject retired — 1.1.0 fixed it and `Fix_LandscapeCostRefresh` left the pack in hotfix 2, so it promises a fix we no longer ship |
| Draft C (F105) | 2026-09-12 | POSTED 2026-08-24T22:28Z verbatim; #2 closed, `Fix in progress` dropped |
| C74 and C83 replies | 2026-09-12 | POSTED with v7 (owner-stated 2026-09-12) |
| The C88 prefab question to the developers | 2026-09-12 | POSTED 2026-09-11 and answered |
| The 2026-09-11 C85 diagnostic draft | 2026-09-12 | SUPERSEDED by "Built for v10" reply 2 |
| **The long C74/C77 sounds post** | 2026-09-12 | ⛔ **Cut on the owner's word, checklist 162 (b) — an ACCEPTED LOSS, not an oversight.** Whether it went up was never recorded and the owner does not remember, so it could be marked neither POSTED nor live. Its four sections and both leads live on in `agent/bugs/C74.md`; the prose is in git at `git show 5923eeb:docs/FIELD_REPORT_REPLIES.md`. ⛔ Do not reconstruct it |
| **The C74 "still checking" follow-up** | 2026-09-12 | ⛔ **Cut on the owner's word, checklist 162 (b) — an ACCEPTED LOSS.** Its posting condition ("post only if the 09-10 post said *still checking*") became permanently unevaluable when ck144 (b) was cleared without recording what went up. Desk-only, never ear-tested, and stale on "currently in testing" since v7. Both findings survive in `agent/bugs/C74.md` — a fresh reply from them takes minutes if it is ever wanted. Prose in git at `git show 5923eeb:docs/FIELD_REPORT_REPLIES.md` |
| The two GitHub timeline tables and the "context a fresh session needs" block | 2026-09-12 | folded into this permanent record; no separate reporter doctrine remains |
| The "Owed, and where it is tracked" table | 2026-09-12 | fully derivable from the status lines; see the rule at the top |
