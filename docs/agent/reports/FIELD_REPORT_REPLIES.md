# Reply drafts for the two GitHub field reports (F104, F105)

⚠️ **A report is not authority** — `agent/bugs/F104.md` and `F105.md` are. This
file exists because these drafts were written in a session and **posting them is
the owner's action, not an agent's**. Without this file they would have lived only
in a transcript. Written 2026-08-24.

⛔ **NOT POSTED as of 2026-08-24.** Strike this line when they are.

## Context a fresh session needs

* Both issues are from **the same reporter (Keelai)**, opened 2026-08-23 against
  the live listings — **the first field reports the pack has ever received.**
* ⛔ **The GitHub issue numbers and exact titles were never captured.** The owner
  referred to the F105 one as *"Error when completing milestone"*. F104 is the
  earlier one about colonists not auto-moving. If you touch these entries, ask
  for the numbers and record them in the front matter so the tracker and the bug
  list line up.
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

⭐ **Updated 2026-08-24:** the fix is no longer merely written — the guard is
**measured reached** on all three landscape leaf classes
(`archive/f106_Mars.exe-20260824-02.32.27.log`). The wording below already
reflects that.

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
> **We've written a fix.** It's in our code now and verified working, and it goes out in the next update to both the Steam and Paradox listings. It skips the pointless cost refresh on landscaping sites, which have nothing to refresh — their work is measured in volume, not resources. It also repairs saves that already have a levelling job in the broken state, so you won't need to demolish anything.
>
> Worth knowing: this was reachable in the base game long before our mod existed, and as far as we can find nobody had reported it. So thank you — that log was genuinely useful.

⚠️ **Two constraints on Draft B:**

1. ⛔ **It promises "the next update", never a date, deliberately.** The tree is one
   module ahead of both live listings and that upload has not happened
   (`H-04`'s successor: never treat a claim as covering what the owner has not
   done). Do not tighten this wording.
2. ⚠️ **The save-repair sentence is derived, not witnessed.** The guard shape was
   chosen partly because it heals sites already saved broken, and the guard is now
   measured to fire — but **F105 has never been reproduced end to end** (a cost
   tech sweeping a real levelling site). Cut that sentence if you want the reply
   to assert only what has been observed.

---

## Owed, and where it is tracked

| Item | Where |
|---|---|
| Post Draft A, get reporter confirmation, close F104 | `F104` "What is owed" |
| Post Draft B (after the 1.0.x upload, or before with the wording as-is) | `F105` |
| Capture the two GitHub issue numbers + titles into both entries' front matter | here, unresolved |
| F105 end-to-end repro — attended, rides a sitting | `F105`; not a blocker for either reply |
