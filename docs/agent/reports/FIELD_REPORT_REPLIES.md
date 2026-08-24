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

## Owed, and where it is tracked

| Item | Where |
|---|---|
| ~~Post Draft A, get reporter confirmation, close F104~~ ✅ **DONE 2026-08-24** — posted 03:40Z, confirmed 19:24Z, entry now `closed` | `F104`, discharged |
| ~~Capture the two GitHub issue numbers + titles~~ ✅ **DONE 2026-08-24** — #1=F104, #2=F105, in both `row_status` cells | here, resolved |
| ⚠️ **Optional, owner's call:** a short follow-up on **#2** when 1.0.x is live — *"this is out now"*. The explanation is already posted and accepted, so this is courtesy, not a debt | `F105` |
| ⛔ Draft B is now **unposted and superseded** — keep it as the accurate wording for any FUTURE reply, since the posted text has the four overreaches listed above | here |
| F105 end-to-end repro — attended, rides a sitting | `F105`; not a blocker for either reply |
