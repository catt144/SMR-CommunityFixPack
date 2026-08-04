# Chain prompt 1 — reset the theory on F11 and F99

**Read `README.md` in this folder first — its binding chain rules apply to you,
especially rule 11 (the seal) and rule 6 (the record is a claim too).**
Unattended: you need no game, no keyboard, no owner. Start with
`git log --oneline -10` + `git pull`.

You are the second set of eyes. On 2026-08-03 a single session found, measured,
interpreted and proposed a fix for two things without any independent check. Your
job is to **derive both from scratch and only then look at what that session
concluded.** Where you agree, the finding gets stronger. Where you disagree, you
have found something.

---

## ⛔ THE SEAL — read this before opening any file

**Until you have written and COMMITTED your own derivation (job 2), these are
off-limits:**

- `docs/agent/bugs/F11.md` — everything below the `**Fix:**` line
- `docs/agent/bugs/F99.md` — the whole file
- `docs/archive/PLAYTEST_ARCHIVE.md` — the F11 rider section dated 2026-08-03
- `docs/agent/STATE.md` — the F11 and F99 paragraphs
- The 2026-08-03 commits `787ebcf` and `9ef9efa` (message bodies included)

**Allowed, and they are all you need:** `A:\SteamLibrary\steamapps\common\
Project Spark\ModTools\Src` (read-only truth), the two archived logs under
`docs/archive/logs/`, `Code/Fix_TrainPlatformWedge.lua`, `agent/facts/`,
`agent/FIX_POLICY.md`, and the raw readings quoted below.

The seal exists because an anchored second opinion is worth nothing. **Attest to
it in your outbox** — state plainly whether you held it, and if you broke it, say
where and why. Breaking it honestly is recoverable; breaking it silently destroys
the chain's only purpose.

---

## The raw evidence, quoted so you need not trust anyone's prose

**F11 — console readings from the live sitting**, in order, as printed. The
colonist was riding a train; the rocket was a landed surface rocket selected in
the UI.

```
(step 1) <train object> <colonist object> BoardVehicle
(step 2) table.find(SMRF11_train.units, SMRF11_col)          -> 1
(step 3) <pool rebuild>                                       -> 1543 1513
(step 4) SMRF11_col:GetMap() == MainMap                       -> false
         SMRF11_rocket:GetMap() == MainMap                    -> true
         SMRF11_col.city == MainCity                          -> false
(step 5) SMRF11_rocket:IsKindOf("Holder")                     -> true
         SMRF11_rocket:GetMap() ~= SMRF11_col:GetMap()        -> true
(step 6) *r SMRF11_col:SetCommand("EnterTransporter", SMRF11_rocket)
         SMRF11_col.holder == SMRF11_rocket                   -> true
(step 7) F11COUNTER <table.find> <#units> <holder==rocket>    -> F11COUNTER nil 6 true
```

The step-3 pool rebuild was this line:

```
*r local pool = table.copy(MainCity.labels.Colonist) for _, c in ipairs(GetConnectedCitiesForColonists(MainCity) or empty_table) do table.iappend(pool, c.labels.Colonist) end ConsolePrint(print_format(#pool, table.find(pool, SMRF11_col)))
```

A later read on the same colony, after a reload, returned `F99RESIDUE 0 0` from:

```
*r local a,b=0,0 for _, c in ipairs(Cities) do for _, t in ipairs(c.labels.TrackBase or empty_table) do if #(t.elements or empty_table) == 0 then a=a+1 end if t.repair_cgs and #t.repair_cgs > 0 and #(t.elements_under_construction or empty_table) == 0 then b=b+1 end end end ConsolePrint(print_format("F99RESIDUE", a, b))
```

**F99 — the error, 14 occurrences in one ~1h session**, from
`docs/archive/logs/Mars.exe-20260803-21.18.38-6a22b86d.log`:

```
[LUA ERROR] Lua/Buildings/TrackElement.lua:805: attempt to index a nil value (local 'start_el')
  Lua/Buildings/TrackElement.lua(805):  method Complete
  Lua/Buildings/ConstructionSite.lua(2483):  method Complete
  Lua/Cheats.lua(115):   <>
  [C](-1):  method MapForEach
  Lua/Cheats.lua(126):  global CheatCompleteAllConstructions
```

The owner states the session's context: they were cheat-building an underground
setup, using `CheatCompleteAllConstructions()` freely.

---

## Jobs

**Job 1 — todo list up front.** One item per commit-and-verify unit, one in
progress at all times, updated the moment each lands (`WORKFLOW.md` element 1).
The owner reads it to decide whether to step in.

**Job 2 — derive both, sealed, and COMMIT the derivation before unsealing.**

Write `DERIVATION.md` in this folder. It is your independent reading, owing
nothing to anyone. Cover, from `ModTools\Src` and the evidence above:

*F11:*
1. What `Colonist:ExitVehicle`'s stale-passenger branch is, when it runs, and
   what happens if it throws. What is the player-visible consequence.
2. What actually happens to `vehicle.units` when a colonist aboard a train is
   sent `SetCommand("EnterTransporter", <some holder>)`. Follow every step of
   the call chain yourself. Does anything remove the colonist from the train's
   list, and if so, what and using which API?
3. Whether the cross-map case differs from the same-map case, and why.
4. **Whether `F11COUNTER nil 6 true` supports the conclusion that the branch
   cannot fire.** Enumerate the OTHER states of the world that would produce that
   same triple. This is the single most important thing you will write.
5. Whether `SetCommand("EnterTransporter", rocket)` invoked by hand is a faithful
   stand-in for what crew-gathering actually does, or whether the real path does
   something the hand call skips.
6. Whether the step-3 pool rebuild faithfully reproduces the pool that
   `CargoTransporter:GatherAvailableColonists` builds. Quote the shipped lines and
   diff them against the console line.
7. ⚠️ **Test this premise specifically, because it was asserted and not
   verified:** *"an underground colonist cannot be in `MainCity.labels.Colonist`,
   therefore index 1513 can only have come from the connected-cities append."*
   Is that true? Find where colonists are added to city labels and check.
8. Whether anything OTHER than crew-gathering can leave a stale entry in
   `vehicle.units`. Enumerate what you find; "I found none" is a real answer if
   you say what you searched.

*F99:*
9. Read `TrackElement.lua` around the throw. What exactly is nil, and why. What
   empties the list, and under what conditions.
10. Where execution stops relative to the rest of the function. What is left
    undone. Whether that leaves persistent damage — and reconcile your answer
    with the observed `F99RESIDUE 0 0`.
11. Whether `quick_build` / the cheat is load-bearing for the failure, or merely
    the thing that fired it 14 times. What a non-cheat path to the same line
    would need.
12. Whether this is already covered by an existing entry (F44, F45, F48 and
    `C12-C38.md` are the neighbourhood — check, do not assume).

*The proposed code change:*
13. `Code/Fix_TrainPlatformWedge.lua` currently replaces `Colonist:ExitVehicle`
    wholesale. A conversion to a **pre-wrapper** has been proposed — intercept the
    stale branch, delegate everything else to the original. Independently assess:
    is that behaviour-preserving? Is a pre-wrapper safe on this method
    specifically? What does `agent/facts/EF-012` say, does it apply, and did you
    verify how `ExitVehicle` is invoked rather than assuming? What breaks if the
    condition is evaluated twice?
14. What the full-copy form costs today. Name the specific shipped lines the copy
    freezes and say which of them a game patch could plausibly change.

**Commit `DERIVATION.md` before you go on.** That commit is the seal.

**Job 3 — unseal, diff, and record every disagreement.**

Now read the sealed material. For each of your 14 points, record: AGREES /
DISAGREES / GOES FURTHER / NOT ADDRESSED. **Every disagreement goes in the
outbox, including trivial ones** (chain rule 5). Pay particular attention to:

- claims whose *route* is wrong even though every cited line is right — this
  project's characteristic failure, and the 2026-08-03 session already caught one
  instance of it in the old F11 entry, which makes a second instance in the NEW
  text exactly the thing to look for;
- anything stated as measured that is actually inferred;
- anything where the reporter's confidence exceeds their evidence.

**Job 4 — file anything you discover that this chain does not own.** New defect →
an `agent/bugs/` entry with an F/C number. Situation-gated observation → a
`PLAYTEST_CHECKLIST.md` rider with **TAKEABLE WHEN <condition>**. Unsure who owns
it → **STOP AND ASK**, do not absorb it.

**Job 5 — outbox, then self-delete.** Append to `## Notes from upstream` in
`02_FABLE_QA_AND_BUILD.md`: the seal attestation; your verdict per point; the
disagreement list; anything you filed; and — stated plainly — **what you would do
about the pre-wrapper conversion and about F99, with your reasoning**, since
prompt 2 decides and deserves your recommendation rather than only your findings.
Then strike your row in `README.md`, delete this file, and commit all of it
together.

---

## Scope fence

**In:** everything in the 14 points. **Out:** re-opening whether the F11 fix
ships (owner decided, README). Writing or editing any Lua — prompt 2 builds, you
assess. Editing `F11.md`/`F99.md` narrative (record disagreements in the outbox;
prompt 2 adjudicates and edits). Any live playtesting.

## Stop conditions

- A load-bearing premise you cannot settle from source → **write it up as
  unsettled and route it**, do not guess and do not launch the game.
- The seal broken accidentally → say so in the outbox immediately and continue;
  do not quietly restart.
- Context running short → self-split at a clean commit boundary (chain rule 4).

## ⛔ What you may not claim

- **Not** that you re-ran any live measurement. You did not; the game is not
  running and you must not launch it.
- **Not** that F99 is or is not reachable without the cheat, unless you can point
  at a shipped non-cheat path to that line. "Unproven" is the honest answer and
  is worth more than a guess.
- **Not** that the F11 branch is unreachable *in general*. The most any analysis
  can support is a statement about specific enumerated producers.
- **Not** that agreement with the 2026-08-03 session is verification, if you
  reached it by reading their reasoning rather than by deriving it.

## Notes from upstream

*(2026-08-03, chain author — the session under review.) I am the session whose
work you are checking, so treat this section as an interested party's account.
Three things I know are soft: (a) the underground-label premise in point 7 is
mine and I did not verify it; (b) my "no other producer" position rests on not
having looked hard, not on having looked hard and found nothing; (c) the
pre-wrapper proposal is untested by anything but reading. The F11 measurement
itself I stand behind — `#units` = 6 and `holder == rocket` were put in
specifically so the counter could fail — but the inference FROM it is exactly
what you should attack.*
