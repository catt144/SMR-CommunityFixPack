# Reply drafts for the two GitHub field reports (F104, F105)

⚠️ **A report is not authority** — `agent/bugs/F104.md` and `F105.md` are. This
file exists because these drafts were written in a session and **posting them is
the owner's action, not an agent's**. Without this file they would have lived only
in a transcript. Written 2026-08-24.

✅ **BOTH ARE ANSWERED AND BOTH REPORTERS REPLIED — 2026-08-24.** This file is now
a *record*, not a queue. Draft A went up verbatim on #1; #2 got a **different**
reply, written before Draft B existed. See "What was actually posted" below.
(This line replaces "⛔ NOT POSTED as of 2026-08-24", which was true when written
and stopped being true the same day.)

## Context a fresh session needs

* Both issues are from **the same reporter (Keelai)**, opened 2026-08-23 against
  the live listings — **the first field reports the pack has ever received.**
* ✅ **CAPTURED 2026-08-24**, which retires the "never captured" gap this file
  carried:

  | issue | title | entry | state, 2026-08-24 |
  |---|---|---|---|
  | **#1** | *"Colonist stuck homeless"* | **F104** | **CLOSED** 06:01:47Z (`completed`), 3 comments, reporter confirmed |
  | **#2** | *"Error when completing milestone"* | **F105** | OPEN, `bug` + `Fix in progress`, 3 comments, reporter acknowledged |

  The mapping is not from the titles alone: #2's attached log is
  `Mars.exe-20260824-00.01.27-6a22b86d.log`, which is the log `F105` was derived
  from. Both are assigned to the owner.
* ⛔⛔ **READ THE TRACKER THROUGH THE JSON API. NEVER THROUGH THE ISSUE PAGE.**
  This is the hardest-won line in this file. A sweep on 2026-08-24 fetched issue
  #1's rendered HTML **three times** — including once with a cache-busting URL —
  and every fetch reported **zero comments**. The issue had three. On that reading
  the sweep recorded "the reporter got no answer at all", wrote it into `F104`,
  `F105`, `STATE.md`, this file and a checklist item asking the owner to decide
  what to do about a silence that never existed. The owner corrected it in one
  sentence. ⇒ Use:
  ```
  api.github.com/repos/catt144/SMR-CommunityFixPack/issues?state=all      # numbers, state, COMMENT COUNT
  api.github.com/repos/catt144/SMR-CommunityFixPack/issues/<n>/comments   # the comments themselves
  ```
  ⭐ The `comments` **count** in the issues list is the cheap control: if it is
  non-zero and your reader shows you nothing, **your reader is lying**, not the
  tracker. A rendered page is a derived surface; the API is the record.
* ⛔ Record issue numbers in **`row_status`**, not a new front-matter key:
  `split_bugs.render_entry` writes only the eleven `FRONT_FIELDS`, so an added
  `issue:` key is silently dropped the next time entries are rendered.
* ⚖️ **OWNER RULING 2026-08-23, and it is why these drafts name the other mod:**
  *"We can't just say it's not our mod, we need to explain that it's the other
  mod, and why… it's not fair to users to just say it's not our issue, we don't
  need to slander anyone but it's also clear that that other mod has been
  abandoned as far as we can tell, it's not our job to protect them either."*
  ⇒ `FIX_POLICY` §8 still binds **store pages and load-order advice**; this ruling
  covers **issue replies**. Recorded on checklist 73; §8 should absorb it on its
  next edit.
* ⚠️ **"Abandoned" is an inference** from dates and metadata (last update
  2025-12-11, `saved_with_revision` 384011 vs game 396349), **not a statement from
  the author.** The drafts below say "hasn't been updated for the current build",
  never "abandoned". Keep it that way.

---

## Draft A — F104 (colonists won't auto-move; error on manual move / workplace change)

> Thanks for the detailed report, and especially for listing your mods — that's what made this findable.
>
> **The short version: this isn't the Fix Pack, and we can tell you exactly what it is.** We reproduced your crash here with your mod set and traced it. The error comes from **Passage Network**.
>
> Passage Network replaces one of the game's dome-connection functions. That function's job is to hand back a table describing which domes are linked; the mod's replacement does the work but doesn't hand anything back. The game then tries to read the thing it wasn't given, and errors out. It's triggered by building or removing a passage — the game throws away its dome-connection data at that moment and asks for it to be rebuilt.
>
> What you see as a player: **each time a passage is built or removed, the very next colonist decision gets dropped.** That decision is either "should I move to a different dome" or "which workplace should I take" — which is exactly where you noticed it. It recovers on its own after one failure, so it looks intermittent rather than broken.
>
> **Why our name is on the warning box.** The game doesn't actually work out which mod caused an error. It looks at the crash report and flags any mod whose name appears anywhere in it. The Fix Pack repairs bugs in shared game code, so it appears in a lot of crash reports it had nothing to do with. In this case Passage Network's own code had already finished running by the time the error happened, so its name isn't in the report at all — and ours is. We're looking at ways to make that less misleading, but the guess is the game's, not ours.
>
> **On your hunch about shuttles** — you may be onto something separate. The game has a rule that colonists ask for a shuttle rather than walk when two domes are more than a certain distance apart, *even if a passage connects them*, and Passage Network doesn't change that rule. So once you have a working Shuttle Hub, distant passage-linked domes can stop being walked. We haven't verified this on a live save, so treat it as a lead rather than an answer — but it would match "they expect there to be a shuttle."
>
> **Where that leaves you.** Passage Network's last update was December 2025 and it's built against an older game version than the current one; the Steam and Paradox copies are identical, so there's no newer build to switch to. We're not going to tell you to uninstall it — it does something the base game doesn't, and you may well decide the occasional dropped decision is worth it. But it's your call to make with the facts, and raising it with that mod's author is the only route to a real fix.
>
> Sorry you got sent to us by a warning box that pointed the wrong way. If you do see anything odd that *doesn't* line up with passage building, please open another issue — we'd rather check twice.

⚠️ **Decision the owner has not made:** the "hunch about shuttles" paragraph is the
only claim in either draft **never verified on a running game** (the ≥1200 m
`ColonistMinDistToIgnorePassage` clause, `Dome.lua:256-259`). It is screened out as
a cause on `F104` and recorded as derived-only. **Cut it if you want the reply to
carry only proven material** — the rest stands without it.

---

## Draft B — F105 ("Error when completing milestone")

⭐⭐ **Updated 2026-08-24 (second pass) — REPRODUCED AND VERIFIED, attended.**
The fix is no longer written, nor merely measured on a stand-in: the defect was
made to happen on our own rig and the fix was watched to stop it, across four
legs (`archive/f105_leg{A,B,C,D}_*.log`; `F105` §"THE FIELD ROUTE, REPRODUCED").
⇒ **Both caveats this draft used to carry are now DISCHARGED**, and the wording
below is strengthened accordingly — see the note under it for exactly which
sentence each leg bought.

> Thanks for the log — that's what made this solvable, and it turned out to be worth chasing.
>
> **This is a bug in the base game, not in the Fix Pack, and it happens with no mods installed at all.** Here's what's going on:
>
> When you level terrain, the game creates a construction site that skips one piece of its own bookkeeping. Separately, a few technologies reduce building costs — and when one of those finishes researching, the game sweeps every construction site on the map to update its numbers. It hits the levelling site, looks for the bookkeeping that was never filled in, and errors out.
>
> Your milestone was the trigger but not the cause. It awarded research points, those finished a tech, and that tech's cost reduction did the rest. Only three technologies in the game carry the effect that causes this — one of them is the NeoConcrete breakthrough, which your Start-with-all-Breakthroughs setup puts in your tree. So you'd hit it any time one of those completed while a levelling or rock-clearing job was active anywhere on the map.
>
> **Why the Fix Pack got named.** The game doesn't work out which mod caused an error — it flags any mod whose name appears anywhere in the crash report. The Fix Pack patches a function that happened to sit in the chain between your milestone and the crash, so our name is in the report. Without the Fix Pack installed you'd get the same error; it would just go quietly to the log with no warning box. We're looking at what we can do to make that less misleading, but the guess is the game's, not ours.
>
> **It's fixed, and we reproduced your error on our own machine to prove it.** With the fix off we get your exact error — `ConstructionSite.lua:673` — the moment a cost technology completes with a levelling job running. With the fix on, nothing. It skips the cost refresh on landscaping areas, which have nothing to refresh: their work is measured in volume of rock, not resources. Every other construction site is refreshed exactly as before.
>
> **You don't need a clean save.** We tested that specifically — saved a colony that was already throwing this error, installed the pack, and loaded it. Clean. Your levelling job can stay where it is; nothing needs demolishing.
>
> It goes out in the next update to both the Steam and Paradox listings.
>
> Worth knowing: this was reachable in the base game long before our mod existed, and as far as we can find nobody had reported it. So thank you — that log was genuinely useful.

⚠️ **Constraints on Draft B — one still binds, two are discharged.**

1. ⛔ **STILL BINDING. It promises "the next update", never a date, deliberately.**
   The tree is one module ahead of both live listings and that upload has not
   happened (`H-04`'s successor: never treat a claim as covering what the owner
   has not done). ⛔ Do not tighten this wording, and do not post a version
   number — `H-02` leaves the version to the sitting, so nobody knows it yet.
2. ✅ **DISCHARGED 2026-08-24 — "we reproduced your error".** Legs A and C, pack
   off: 14 and 12 raises of `ConstructionSite.lua:673`, from a real Flatten job
   worked by real drones, state verified at the console before the trigger was
   fired. Leg B, pack on: zero. This draft may now say *reproduced*, which the
   previous version could not.
3. ✅ **DISCHARGED 2026-08-24 — the save sentence.** It used to read "repairs
   saves that already have a levelling job in the broken state", which was
   derived from the fix's shape and never witnessed. **Leg D witnessed the thing
   that matters to the reporter**: a save made while the error was live, pack
   installed afterwards, loaded clean.
   ⚠️ **The wording changed with it, and the change is not cosmetic.** We now say
   *"you don't need a clean save"* rather than *"it repairs saves"* — because the
   pack does **not** repair the save. The site stays in its broken state; the
   guard makes that harmless. Uninstall the pack and the error comes back. The
   old wording promised a repair we do not perform.

⚠️ **Still not shown, so still not claimed anywhere in this draft:** what the
error looks like to a player who is *not* driving it from the console. Every leg
fired the trigger through the console, and the reporter's own popup came from
research completing on the game thread. Nothing in the reply depends on that, but
do not add a sentence that does.

---

## Draft C — the #2 follow-up, for when 1.0.x is live (2026-08-24)

⭐ **This is the one to post.** Draft B below is superseded: it was written as a
*first* reply, and #2 already has a full explanation the reporter has thanked us
for. Re-explaining would be noise. This is short on purpose.

⚠️ **It is written to avoid all four overreaches in the posted reply** (listed
under "What was actually posted"). It never says *repairs*, never says *only
three technologies*, never claims anything about a warning box, and never claims
a clean install.

> This is live now — it went out to both the Steam and Paradox listings today.
>
> Since I last replied I managed to reproduce your error here, which I hadn't been able to do before: with the fix off, finishing a cost technology while a levelling job is running throws the same `ConstructionSite.lua:673` you saw. With the fix on, nothing.
>
> I also checked the case that matters for you specifically — a save where this is already happening, with the pack installed afterwards. It loads clean and carries on; the levelling job can stay where it is and nothing needs demolishing.
>
> Thanks again for the log. It's the whole reason this was findable.

**Notes for whoever posts it:**

* ⛔ **No version number.** The two stores legitimately show different numbers and
  explaining that to a reporter is noise they did not ask for.
* ⛔ **No date beyond "today"**, and only post it on the day of the upload.
* ✅ *"stops it happening / loads clean and carries on"* — never *"repairs your
  save"*. Leg D witnessed the outcome; nothing repairs the save.
* ✅ *"the same `ConstructionSite.lua:673` you saw"* is safe: their own log names
  that line, and legs A and C reproduced it 14 and 12 times.
* ⇒ After posting, the issue can be **closed**. `F105` is `fixed`, rig-verified,
  and the reporter has already acknowledged the explanation. The `Fix in
  progress` label comes off.

---

## What was actually posted (the record — read this before drafting anything new)

Pulled from the API 2026-08-24. **Both reporters replied and both are content.**

**Issue #1 / F104** — Draft A below went up essentially verbatim.
| when | who | what |
|---|---|---|
| 08-23T13:28:55Z | Keelai | *"Also appears when changing workplace."* — the workplace half of the symptom, volunteered |
| 08-24T03:40:35Z | owner | **Draft A**, naming Passage Network |
| 08-24T06:01:47Z | — | issue closed, `state_reason: completed` |
| 08-24T19:24:28Z | Keelai | *"Yeah i had a hunch that mod might be the problem but thanks for checking :)"* |

⇒ `F104`'s closure gate (a reply **and** the reporter's confirmation) is met, and
the entry is `closed`.

**Issue #2 / F105** — ⚠️ **the posted reply is NOT Draft B.**
| when | who | what |
|---|---|---|
| 08-24T01:57:13Z | owner | asks for a save + which store the modlist came from |
| 08-24T06:04:29Z | owner | **a full F105 explanation, written before the rig legs ran** |
| 08-24T19:23:00Z | Keelai | *"Nice and thanks :) ill try and include both save and log in the future"* |

⭐ It is a good reply and the reporter is satisfied; nothing here needs a
correction posted. But it was written **hours before** legs A–D, so four of its
sentences are **stronger than what the tree can now support**. ⛔ **Do not copy
any of them onto the fix list, a store card or `last_changes`** — those surfaces
have no reporter goodwill to spend and no thread to correct them in.

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

## Steam comments answered by the v7 update (C74, C83) — drafts, 2026-09-10

Both reports came from Steam comments the owner relayed, not GitHub issues, so
there is no API record to read — **check the Steam thread first; if it is already
answered, skip the draft.** ⛔ Post only AFTER the upload is live (these say
"today's update"); before that, say "the next update". No version number. Every
sentence below is witnessed attended (`bugs/C74.md`, `C77.md`, `C83.md`).

**C74 — "The Rare Metal Extractor's hammer doesn't make a sound…"**
> Thanks — you were right, and it wasn't only the hammer. The game had the sounds and effects for it, but nothing ever set them off; the same was true of six other machines. Today's update restores them. One thing to know: the drill-style Rare Metals Extractor has no strike sounds by design, so if yours has the drill, use Change Skin to switch it to the hammer.

⛔ Do not add "like the original game": whether the 2018 release played it is the
reporter's memory, never checked (`C77` §What is NOT established).

**C83 — "Rocket lands and colonists go to nearest dome with no life support…"**
> You were right that no listed fix covered this — it was a separate bug in the game. When the working domes nearby have no free homes left, the game falls back to the nearest dome the arrivals can walk to without checking that it is switched on, open or has life support. Today's update makes that fallback the nearest working, open, supplied dome instead. We reproduced your layout and watched every arrival go to the working dome.

⛔ Do not say the colonists in the bad dome died — the owner's run saw the
**Suffocation!** warning but did not wait it out (`C83` §OBSERVED).

**The long sounds-thread post (drafted in conversation 2026-09-10, BEFORE the build; posted or
not is the owner's to say — checklist 144 b).** Its sections, so a follow-up can honour them:
*Being restored* — the seven units (C74/C77), "currently in testing"; *Silent on purpose* — the
drill Rare Metals skin (NASA, SpaceY, BlueSun, Brazil, Roscosmos, Japan, ISRO default) and the
white CP3 MOXIE; *Can't fix* — the Metatron's 7 rotation sounds (never requested,
`Metatron.lua:78`, `:86`) and extra Rare Metals hammer variants (`hit-moment3` never fires on a
2-strike loop, `hit-moment4` is in no list — `reports/C74_SOUND_SWEEP.md`); *Haven't nailed down*
— Metatron rotation dust (fixable, untimed), Hydroponic Farm lift/spray/rotate (empty
`StartAnimThread`, possibly deliberate), and **"still checking"**: a Drone Hub effect while it
builds drones and one sound on a misspelled animation name. ⚠️ If that last line went out, the
two leads are OWED a check and a follow-up (row below).

**Follow-up for "still checking" (drafted 2026-09-10 late; both leads re-derived from the 1.1.0
tree, `reports/C74_SOUND_SWEEP.md` "Unreachable even WITH presets").** Post ONLY if the owner's
posted text said "still checking"; no version number needed.
> Following up on the two I said I was still checking — neither turned out to be something you're missing. The Drone Hub effect was made for building drones, but nothing in the game ever plays it on a Drone Hub, and there is no moment it was ever tied to, so there is nothing to restore without making one up. The misspelled one is real: one digging sound on a version of the Concrete Extractor never starts because its name is spelled wrong. But the same digging loop is already playing through that part of the dig, so correcting the spelling would only play the same sound twice on top of itself. Nothing there is silent that should be making noise.

⚠️ Desk-only (neither was ear-tested) — the post says nothing it would need an ear for. ⛔ Do not
name the extractor's skin: which skin uses `ConcreteExtractorCP3Dome` was NOT route-checked.

## Field reports triaged 2026-09-11 — drafts (checklist 146 / 147)

Source: `reports/FIELD_LEADS_2026-09-11.md`. ⛔ All desk reads — nothing here was witnessed in play. No version number,
no fix promise; "filed" is the strongest word. Check each thread first; skip a draft if it is already answered.

⭐ **Updated 2026-09-11 (release words, `RELEASE.md` step 1): F119 and the deep-scan bug went from "filed" to
`tested-attended` in play (checklist 149) and now ship in the next update** — the two drafts below are rewritten to say
so, superseding the "no fix promise" framing above for these two only. Still no version number (the upload is the
owner's, `H-02`).

**Wildfire cure rocket stuck (Reddit, r/SurvivingMars) — F119**
> This looks like a real bug in the game, and the Advanced Martian Engines hunch is right on target. The cargo rocket Earth sends works out how much fuel it needs once, when it lands. If the fuel cost changes while it's sitting on the pad (finishing Advanced Martian Engines cuts it by 20, which is exactly your "20 fuel to unload"), the rocket ends up holding fuel it no longer needs, and nothing is set up to take it off. The Fuel Conservation law can do the same. We've fixed this for the Relaunched Fix Pack — it's tested and will be in the next update, and it also repairs a rocket that's already stuck the moment you load your save. Until then, if you have a save from before that rocket landed, loading it and holding off on Advanced Martian Engines (and on changing Fuel Conservation) until the rocket has left should avoid it.

⛔ The save-reload advice is INFERRED, not route-checked. Do NOT mention the console: whether Relaunched players can open
one is unchecked, and PS5 has none. ✅ The load-heal claim is OBSERVED (`F119.md` §Attended check, 2026-09-11): a
pre-stuck rocket reloaded and left.

**Clogged after a dust storm (Steam, "Clogged Extractor") — C85**
> "Clogged after a Dust Storm" comes from a one-time story event, not from wear, so maintenance won't clear it. What happens next depends on which answer you picked in its popup: "Send a colonist" fixes it straight away; "Have the drones replace the entire component" turns it into a normal repair needing 3 Electronics; "We'll fix it after the storm" only fixes it when a later dust storm ends, and it can miss that storm's turn, so it may take more than one storm. If you remember which answer you chose, or whether you saved and reloaded while that popup was still open, please say — we're checking whether it can get stuck for good.

⚠️ "maintenance won't clear it" is INHERITED (`RequiresMaintenance.lua:413-417`, investigator read).

**Deep scan finds nothing (Steam, "Possible Bug") — C86**
> Orbital probes only deep-scan once you've researched Adapted Probes. Deep Scanning on its own doesn't change probes; it lets your normal sector scans find deep deposits when a sector is scanned again. So probes launched before Adapted Probes only do a normal scan, which matches what you saw. One small real bug turned up while checking: with the five-sector Advanced Orbital Probe and no Adapted Probes, a neighbouring sector you had already deep-scanned gets marked back to "Scanned", and scanning it again finds nothing new. We've fixed that too — it'll be in the next update.

**Building codes vs prefabs (Steam, helfisk; a PDX developer active in the thread) — C88**

⚠️ Replaced 2026-09-11: the first draft said "It looks intentional"; the owner disagreed (a prefab is an ordinary
building shipped from Earth). This version reports the code and asks the devs. Every file/line below was re-read on
1.1.0.403908 by `smr-bugfixpack-0d`. The owner is posting it (09-11) — record the post and any dev answer in C88.

> Following up on this one — we took a look at the game's Lua (the source that ships in the ModTools folder, game 1.1.0.403908), and it's a deliberate exemption in code, but the law text doesn't mention it.
>
> **What the code does:**
> - Lax and Strict each have two halves: a Concrete/Metals construction-cost change, and a maintenance change that gets applied to a building when its construction completes. Those maintenance halves are `ConstructionComplete` handlers in `Data/LawDef/LawDef-Efficiency.lua` (lines 699–704 for Lax, 907–912 for Strict).
> - Both handlers begin with `if from_prefab then return end`, so a building deployed from a prefab never gets the maintenance change. The `from_prefab` flag is new in 1.1.0: `ConstructionSite.lua` reads it from the site (line 1729) and passes it along with the `ConstructionComplete` message (line 1786).
> - The cost half doesn't come into play for prefabs anyway, since they don't pay a construction cost.
>
> **What that means in play:** under Strict, prefab buildings don't get the "30% less maintenance" the law promises; under Lax, they avoid the "50% more maintenance". Both law descriptions just say "new buildings", with no exception for prefabs.
>
> **Our question:** is excluding prefab buildings intended? If it is, it would help to say so in the two descriptions (e.g. "new buildings, except those deployed from prefabs"). If it isn't, dropping the `from_prefab` check from those two handlers would make prefab buildings follow the law like any other new building — which is what the description, and this report, expect.

Optional last line (commits the pack to leaving it alone until the devs rule): *"(We maintain the Relaunched Fix Pack;
we'll leave this alone in the pack and follow whatever you decide.)"*

**Lakes, "excavation too deep" (Steam)**
> Worth sending through the in-game report tool as the developer asked. That warning means the game thinks the lake's bottom would end up below the lowest height the map allows, but your spot is ordinary flat ground, so it shouldn't fire there. The check itself didn't change in the update, so something it reads did; we're checking whether it happens on every 1.1.0 map.

⚠️ Revised 2026-09-11 after the owner's pushback (the first draft blamed very low ground; the player's screenshot shows
ordinary ground). Hold this until the checklist 147 lake check has run — its result changes the reply (C87).

**Meteors (Steam) — optional; recommendation (checklist 147): skip**
> Meteors land at random spots across the whole map, and the way the spot is picked didn't change in the update, so a bigger base simply gets hit more often. The Relaunched Fix Pack doesn't change meteors any more.

## Owed, and where it is tracked

| Item | Where |
|---|---|
| ~~Post Draft A, get reporter confirmation, close F104~~ ✅ **DONE 2026-08-24** — posted 03:40Z, confirmed 19:24Z, entry now `closed` | `F104`, discharged |
| ~~Capture the two GitHub issue numbers + titles~~ ✅ **DONE 2026-08-24** — #1=F104, #2=F105, in both `row_status` cells | here, resolved |
| ⭐ **NOW DUE — 1.0.x went live 2026-08-24.** Post **Draft C** on #2, then close the issue and drop `Fix in progress` | `F105`, Draft C above |
| ⛔ Draft B is now **unposted and superseded** — keep it as the accurate wording for any FUTURE reply, since the posted text has the four overreaches listed above | here |
| F105 end-to-end repro — attended, rides a sitting | `F105`; not a blocker for either reply |
| Steam sounds thread — IF the long post went out with "still checking": post the follow-up drafted above. ✅ Leads re-derived + closed 2026-09-10 late (neither a loss) | checklist 144 (b); `reports/C74_SOUND_SWEEP.md` |
| 2026-09-11 field-report drafts (Wildfire, clogged, deep scan, building codes, lakes; meteors optional) — owner posts or not | checklist 146 / 147; `reports/FIELD_LEADS_2026-09-11.md` |
