# F86 — second-round questions for the adjudicator

> ✅ **ROUND TWO — released 2026-07-31 after `docs\F86_ADJUDICATION.md` was
> delivered.** This file was withheld until then on purpose: several items point
> at specific answers, and reading it earlier would have contaminated a verdict
> that had to be independent.
>
> **Your verdict is strong and it is not being re-litigated.** Three findings in
> it were reached by neither position document — route (b) capture via
> `Fix_CaveInsNoDisasters` (§3.1), the `BombardEnd`/Mystery-7 correction (§3.2),
> and the GT-creation-ordering gate (§4.1) — and §3.1 correctly falsifies the
> discovery session's central claim. §5.4's "who is waiting on the promise this
> frame was keeping" is a better test than the tiering it replaces.
>
> ⚠️ **But one assumption runs through §2.9, §2.11 and §5.2, and it has now been
> MEASURED FALSE. See item 6(a) — it is no longer a question.** Item 6(b) you
> found independently and stated better than we did; it is kept only for the
> record.

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

## 6. The orphan-environment question — now MEASURED, and it contradicts §2.9 / §2.11 / §5.2

**(a) Do VANILLA globals resolve inside an orphaned mod function? YES. MEASURED
2026-07-31 21.23, with a clean control.**

A purpose-built Test Kit probe (`SMR-BugFixPack-TestKit/Code/99_OrphanEnvProbe.lua`)
registered a thread through `GlobalGameTimeThread` — the exact mechanism measured
leaking — parked it in a `Sleep`, saved, and the Test Kit was then disabled. Log
`Mars.exe-20260731-21.23.19`:

```
:266  Loaded mod items for: SMR_CommunityFixPack          <- Test Kit code ABSENT
:289  Unpersist missing permanent: Mod/SMR_CommunityFixPackTestKit
                                   | Fallback permanent: table: … [7]
:311  [LUA ERROR] SMRTEST-ORPHANENV RESOLVED — vanilla globals reachable in an
      orphan, GameTime=98125338       (Locals: now | number 98125338)
```

The env permanent failed to resolve, the fallback was substituted — the exact F86
condition — and the orphan **still called the vanilla global `GameTime()` and got
a real value.**

**The mechanism is therefore narrower than "the environment is gutted": the
fallback still reaches the real game globals. An orphan loses ONLY the names its
own mod created.** `SMRFixPack` reads nil after uninstall because the mod that
creates it never loaded — not because the environment was replaced.

**What this falsifies in your verdict:**

- **§2.9** — *"the orphaned `fixed_loop` dies at its first global lookup
  (`Sleep`) after uninstall — that rain type is then gone for the save"*.
  `fixed_loop` references **no mod-created name** (`Sleep`, `AsyncRand`,
  `CreateGameTimeThread`, `RainsDisasterActivation`, `WaitMsg`, `const` are all
  vanilla). It does not die. It runs our replacement loop **forever**.
- **§5.2** — the harm statement inverts. A player who uninstalls does not "lose
  rain types"; they **keep our rain loop permanently**, in a save they believe is
  vanilla, with nothing to tell them.
- **§2.11** — *"Each orphaned thread errors at its first post-resume global
  lookup and dies"* is the same assumption applied to all four own-thread
  modules, and it is what upgraded the Tier-3 "one log line" claim from REASONED
  to source-verified. A first pass suggests it holds for
  `Fix_MeteorStormWedge` and `Fix_TrackConnectorPingPong` (both reference
  `SMRFixPack.*`) but **not** for `Fix_CrystalMysteryHang` or
  `Fix_ExtenderFlapChurn`, whose bodies look pure-vanilla. **Please verify per
  module rather than trusting that pass** — it was a crude extraction.
- **Labelling.** §2.9 carries **RE-VERIFIED**, but "the orphan dies at `Sleep`"
  is not source-verifiable — it is an inference about environment behaviour that
  only a measurement can settle. The document's worth rests on those labels, so
  this one wants correcting alongside the finding.

It also retroactively explains the original `GetPriorityForRequest` orphan that
"kept working with zero errors": same mechanism, not an anomaly.

**Questions.** Which Tier-1/Tier-3 conclusions move? Does the corrected capture
rule in §5.1 need a fourth clause about what an orphan can still *reach* (as
opposed to how it got captured)? And does "runs our logic forever, silently"
change the `BombardmentSpread` D3 recommendation or the tiering's ADD side?

**(b) The two-route point — you got there first, and stated it better.**
Kept only for the record: this item originally asked whether the discovery
session's filter was incomplete because it omitted the storage route. Your §3.1
found that **and** route (b) — capture via a live local/upvalue in an engine
frame — which neither position document had, and §5.1's value-reachability rule
is the correct durable statement. Nothing owed here.

---

**If any of the above changes your verdict, amend `F86_ADJUDICATION.md` and say
which item caused the change.** If none does, say that too — a second round that
moves nothing is a real result.
