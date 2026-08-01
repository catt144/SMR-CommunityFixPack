# F86 — second-round questions for the adjudicator

> ⛔ **DO NOT READ THIS UNTIL YOU HAVE DELIVERED `docs\F86_ADJUDICATION.md`.**
> It is withheld deliberately. These questions come from the discovery session
> and the owner, and several of them point at specific answers — reading them
> first would contaminate a verdict that is supposed to be independent. If you
> have not yet written your verdict, stop and go back to
> `docs\F86_ADJUDICATION_PROMPT.md`.

**Purpose.** A second round, raised while you were working. Answer each on its
merits, and **amend your verdict if any of them changes it** — say so explicitly
rather than quietly revising. If you already covered one, say so and point at
where; that is a useful signal in itself.

---

## 1. Why is the whole remedy hanging off ONE hook?

**Owner's question, and it exposes a gap in method rather than in reasoning.**
The design found `SaveGameStart`, confirmed it reaches mods, and built layer 1 on
it. **Nobody ever enumerated the hook surface.** The mod message blacklist is
nine names (`CommonLua\Classes\Mod.lua:1430-1440`); everything else is available.
A five-minute enumeration finds at least these, none of them blacklisted, and
**two of which appear nowhere in either position document**:

| message | fires | used by us? |
|---|---|---|
| `SaveGameStart` / `SaveGameDone` | around the write (`Savegame.lua:1043`, `:1061`) | yes — layer 1 |
| `LoadGame` | after a save loads | yes |
| **`PersistPostLoad`** | **inside the unpersist** (`_fixup.lua:50`) | **never considered** |
| **`CanSaveGameQuery`** | when the game asks whether saving is allowed (`Savegame.lua:94`) | **never considered** |
| `PostNewGame`, `ChangeMapDone` | map/game lifecycle | no |

**Questions.** Is the enumeration above complete — what else is reachable? Does
`PersistPostLoad` offer anything `LoadGame` does not (it runs *earlier*, inside
the restore, with `data` in hand)? Is there any legitimate use for
`CanSaveGameQuery`, or is vetoing a player's save always unacceptable? **Should
the hook surface be written into `ENGINE_FACTS.md` as a table**, so the next
design does not discover hooks one at a time?

## 2. Reframe layer 1 as an invariant, not a fallback

`SAVE_SAFETY_REDESIGN.md` positions layer 1 as "for what layers 2 and 3 cannot
reach" — a last resort. The owner's framing is stronger:

> **The pack is never installed at the moment a save is written.**

Arm on load, disarm on save. Under that framing F86 becomes *structurally*
impossible rather than mitigated case by case, and **layers 2 and 3 stop being
alternatives to layer 1** — they become the thing that shrinks the set layer 1
must handle until it is small enough to be safe.

**Questions.** Is the invariant actually achievable, or does something break it?
Does adopting this framing change the build scope, the layer ordering in
`FIX_POLICY.md` §3a, or the decision to bar layer 1?

## 3. The limit that forces layering — confirm or refute it

The discovery session's reasoning for why one hook cannot carry the whole remedy:
**we cannot unwind another thread's stack.** Our own threads can simply be
deleted at `SaveGameStart`. But a *command* thread (`Drone:Idle`,
`Colonist:Arrive`) carries our frame inside a unit's command stack, and the only
lever is `SetCommand`, which would restart hundreds of units mid-action on every
save — including every autosave, roughly once a sol. That is a gameplay defect,
not a save-safety fix.

If that holds, the command-thread class **must** be solved by never putting code
there (layer 2), no matter how good the hooks are.

**Question.** Is that correct, or is there a way to clear our frame from another
thread's stack that neither session found?

## 4. A cleaner disarm — and the specific thing that would break it

The design's disarm is "restore vanilla bodies, then rebuild ours afterwards".
There may be a simpler move: **delete our thread and create nothing.** If the
save then carries nothing for that global name, vanilla's own `PersistPostLoad`
creates a fresh vanilla thread on load (`_fixup.lua:50-56`) — the engine does the
cleanup, we write less code, and the save is clean even for a player who never
reinstalls.

⚠️ **Verify before anyone builds on it.** That path fires only
`if data[name] == nil`, and `GlobalGameTimeThread` initialises the global to
**`false`, not `nil`** (`_fixup.lua:10-12`), with `PersistableGlobals[name] = true`
(`:15`). **If a deleted thread persists as `false` rather than absent, the rebuild
never runs and that colony's meteors are dead** — the exact F86 harm, delivered by
the F86 repair. One read settles it.

**Question.** Does the value persist as `false` or as absent, and does that kill
this variant?

## 5. The timer cost — and why §1.4 makes it cheaper than it looks

The standing objection to tear-down is that it discards in-flight timer state,
which is the autosave trap (a 35–115 h meteor timer reset roughly once a sol).

But `F86_SESSION_FINDINGS` §1.4 establishes that **we already pay exactly that
cost today — on every load, unconditionally, for no benefit whatever.** So a
disarm-on-save design that re-armed from a persisted deadline would be *strictly
better than what currently ships*.

That reframes §1.4: not merely a bug to fix, but evidence that **deadline
persistence is owed anyway**. And once it exists for §1.4, layer 1's principal
objection largely dissolves.

**Questions.** Is that right? Does it change the case for barring layer 1 — should
the bar be *"not yet, and here is the gate"* rather than *"not ever"*? What is the
gate?

## 6. Two things neither document tested, both cheap, both load-bearing

**(a) Do VANILLA globals resolve inside an orphaned mod function?**
We know mod globals do not — that is what killed both measured leak sites
(`SMRFixPack` → nil). But `ENGINE_FACTS` records an orphan that *kept working
with zero errors*, which implies vanilla names still resolve through the
substituted fallback env. **Both readings are live and they invert the harm
model:**

- **They resolve** → an orphaned `Fix_RainsDeadlock` loop does not die. It runs
  our replacement logic **forever, silently, in a save that is supposed to be
  vanilla.** Worse than the loud failure, and it makes the severity tiering's
  "net harm ≈ one log line" optimistic.
- **They do not resolve** → orphans die at their first vanilla call, and the
  tiering is roughly right.

Cheap to settle: one orphaned thread, one wake, one log read. **Neither document
flags it.**

**(b) The discovery session's filter is incomplete, by its own author's later
admission.** `F86_DISCOVERY_POSITION` §3 states the test as *"can it be blocked
below a yield on a game-time thread"* and concludes synchronous code can never be
captured. **There are two routes into a save, not one:** a function on a blocked
thread stack, **and** a function stored on a persisted object — which is the
original `GetPriorityForRequest` finding this entire line of work started from. A
perfectly synchronous function assigned onto a persisted instance *is* captured.
The audit's `= function` enumeration covered that route, so the practical
exposure list may be unaffected — but the filter as written drops it, and anyone
applying it as the sole test would miss that class.

**Question.** Does the two-route correction change the exposure list, and should
`FIX_POLICY.md` §3a state both routes?

---

**If any of the above changes your verdict, amend `F86_ADJUDICATION.md` and say
which item caused the change.** If none does, say that too — a second round that
moves nothing is a real result.
