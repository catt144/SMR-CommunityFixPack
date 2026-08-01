# Prior-art survey — save-safety in the original game's modding community

**Run 2026-07-31 at the owner's direction (F86 follow-up item 8, flipped on).
Question asked: is F86-grade save-safety ("uninstall leaves a vanilla save")
attempting the impossible, or is permanent save-marking a community-accepted
design constraint?**

**Answer up front: it is a DOCUMENTED, INTENTIONAL ENGINE PROPERTY that mods
mark saves; the community's norm is to accept it, silence its symptoms, and
heal after the fact; nobody has ever attempted uninstall-cleanliness as a
requirement. We are not attempting the impossible — we are attempting the
achievable subset nobody bothered with, on an engine whose remaster finally
provides the hooks the original community explicitly wished for. The parts
that ARE impossible (in-flight command frames, inert residue) are exactly the
parts this project already declared accepted residuals.**

Corpus: ChoGGi's collection (473 mods, unpacked source,
`github.com/ChoGGi/SurvivingMars_CheatMods`, blobless clone read this
session); the 20 subscribed workshop items (Steam API: all 20 are ChoGGi mods,
so the GitHub corpus covers them — no HPK extraction needed); both games'
official ModTools docs; community threads.

---

## 1. The developers documented the F86 mechanism as a FEATURE

The original game's own modding documentation —
`Surviving Mars\ModTools\Docs\LuaSavegame.md.html` — states verbatim:

> "Any Lua threads sleeping when a savegame is triggered will be serialized as
> part of the savegame. This include any local variables anywhere in the call
> stack, any upvalues, and even the bytecode of the functions themselves, to
> allow loading the savegame even when a game update has changed the Lua code.
> **This means that after loading, pieces of "old" Lua code (coming from the
> savegame, not from the potentially updated game) will be running.** New
> invocations of these functions, however, will use their new versions."

Three consequences:

1. **By-value serialisation of sleeping threads is designed update-tolerance,
   not an oversight.** Mods inherit it as a side effect. Saves carrying mod
   code is the engine's *normal operating state*, described without so much as
   a warning to modders.
2. **"New invocations use their new versions" is official confirmation of the
   command-thread self-cleaning rule** (adjudication §2.7 / findings §2.4) and
   of the whole upgrade-path model.
3. The page also confirms the F86 rule set from the developer side: GT threads
   serialised, RT threads not, globals only via GlobalVar (the remaster's
   GameVar/PersistableGlobals). **The remaster's ModTools docs do not carry
   this page** — the current game's modders have *less* official guidance than
   the original's did.

## 2. The community's norm: accept, silence, heal-after

Census over all 471 mod folders in the collection (`Code/*.lua`):

| shape | count | note |
|---|---|---|
| mods with yields (`Sleep`/`WaitMsg`) in mod code | **112** | a quarter of the collection ships capturable code |
| mods creating their own GT threads | **45** | none disarms on save |
| mods touching `GlobalGameTimeThread` machinery | 3 | see §3 |
| mods touching `PersistableGlobals` | **0** | |
| mods using `GameVar` | **0** | persisted state goes onto game objects as instance fields instead |
| mods using save hooks | 2 | one is a debug printer; the other is the cleanup mod in §4 |

And the smoking guns, all in the flagship shared library:

- **`ChoGGi's Library` wraps the engine's `ReportPersistErrors` and ships a
  user-facing mod option literally named `IgnorePersistErrors`**
  (`Code/ModOptions.lua:175-186`: `if …IgnorePersistErrors then return 0, 0`).
  Persist errors from mods are so routine that the community's core tooling
  offers to silence the reporter wholesale.
- The wrapper's comment: *"be useful for restarting threads, see if devs will
  add it (yeah I think that isn't happening after two dev teams are gone)"* —
  ChoGGi **wanted a post-save hook to restart threads** (the rebuild half of
  our layer 1) and had to improvise it by posting `Msg("PostSaveGame")` from
  inside the wrapped error reporter. The original never gave mods the hook.
  **The remaster does** — `SaveGameStart`/`SaveGameDone` reach mods, measured
  by this project. We have the tool the best original-game author wished for.
- Changelogs treat persist errors as log-cosmetics: *"Removed the persist
  error that showed up in the log"* (`Solar Array Follows Sun/changes.txt:14`),
  *"Got rid of the persist error … (doesn't affect gameplay)"*
  (`RC Bulldozer/changes.txt:28`).
- **Restart-on-load is the standard community heal**, timer re-rolls included:
  `Game Rules Permanent Disasters` registers three of its own
  `GlobalGameTimeThread`s and restarts them via the engine's `SavegameFixups`;
  `Disable Disasters` calls `RestartGlobalGameTimeThread("Meteors")` etc. on
  toggle. Our §1.4 defect class (blind restarts re-rolling long timers) is
  endemic in community code and entirely unremarked.

## 3. The Tier-1 shape in the wild

Of 471 mods, exactly one **replaces** nothing but still owns the shape:
`Solar Array Follows Sun` registers its own
`GlobalGameTimeThread("SolarArrayOrientation", while-true/Sleep loop)` — a
mod-owned persisted global loop whose body touches only vanilla names and
upvalues. By the measured orphan mechanics (adjudication §8.1), after
uninstall **it keeps rotating the player's solar arrays forever, silently, in
a "vanilla" save**. Shipped for years; its only related changelog entry is
about hiding the persist error. No community mod was found that replaces a
*vanilla* global GT thread body the way `Fix_MeteorFrequency` does — the
closest analogue author instead **restarts vanilla's thread** and heals state
synchronously (§5). The absence the owner asked about is real: **the Tier-1
replace-a-vanilla-loop shape has essentially no prior art — and the one
adjacent case is a live example of the runs-forever orphan.**

## 4. Mod residue in saves is a named, player-visible community problem

- ChoGGi ships a *repair mod for saves damaged by other removed mods*:
  `Fix Missing Mod Buildings` — description: *"If you installed a mod that
  adds certain buildings, then removed the mod without removing them; **your
  game won't load**… This fixes that."* It sweeps `UnpersistedMissingClass`
  husks out of `s_Heaters` and the city labels **on `OnMsg.PersistPostLoad`**
  — community precedent for the exact hook our round-2 table surfaced, and
  proof the engine's designed degradation path (the fallback class) leaks into
  vanilla systems anyway.
- The "safe to remove" convention exists and is stated **per-mod, only when
  true**: *"You can remove this mod after saving your game"*
  (Fix Missing Mod Buildings), *"Once you save the game you can disable this
  mod"* (Terraforming Existing Saves). The default expectation is the
  opposite.
- Perennial help threads in both games' forums: "Mod missing message",
  "Removing reference to mod from save?", "Mods that will not uninstall"
  (original), "Can not uninstall mod More Deposits" (Relaunched). Players
  hex-edit `active_mods` out of save files. The engine's own load-time
  warning — the same `This savegame tries to load Mod …` line PT-20 logged —
  is a designed surface for an anticipated state.

## 5. The fix-shape comparison — the veteran chose our shapes

ChoGGi's fix-family mods, read against our F86 dispositions:

| their mod | their shape | our analogue |
|---|---|---|
| `Fix Cold Wave Stuck` | **synchronous heal on CityStart/LoadGame/ChangeMapDone**: patch the missing `GetMapID` onto the stuck object, call vanilla `StopColdWave()`, clear the global. Never touches the loop thread | our watchdog/heal shape (F78/F81 family) |
| `Fix Eternal Dust Storm` | synchronous heal that **posts the missed end-message** (`Msg("DustStormEnded")`) and clears state | **the exact RainsDeadlock repair design** — post `RainDisasterEnd` on the missed path |
| `Disable Disasters` | restart **vanilla's** global threads; never installs its own body | our watchdog restart of vanilla's body |
| `Fix Bugs` (3,105 lines, dozens of fixes incl. our F22/F40 cousins) | **215 orig-capture wrapper references vs 59 raw replacements**; zero global-thread bodies; zero save machinery | FIX_POLICY's wrap-over-copy preference, validated at years-of-players scale |

Two conventions differ, both in our favour:

- **Orig capture:** ChoGGi captures originals as file-scope locals
  (`local ChoOrig_X = X`) and gates on a local `mod_EnableMod` — all upvalues,
  so **his orphans resolve everything and run forever silently**. Our
  convention (originals and gates reached through the `SMRFixPack` global)
  makes orphans **die loudly at first touch** — the safer failure, per the
  measured orphan mechanics. Keep ours.
- **Persistence hygiene:** the community's zero use of
  GameVar/PersistableGlobals means state rides on instance fields (our
  fixture measured 919 `SMRFixPack_reserved_at` fields — we do this too, but
  declared and audited).

## 6. Verdict on the owner's question

**Permanent save-marking is the engine's documented design and the
community's accepted constraint — and that is precisely why F86 still
matters.** The community's standard is "the save needs the mod, or at least
forgives its absence"; the engine's standard is "old code runs from the save
by design"; nobody has ever promised "uninstall returns you to vanilla".

We are **not** attempting the impossible:

1. The impossible parts — clearing another thread's in-flight frames, seeing
   inert serialised residue — are exactly the parts this project already
   scoped out as accepted residuals (layer 2's dead weight; adjudication
   §8.5).
2. The achievable parts have prior art *in pieces*: synchronous heals, posting
   missed messages, restarting vanilla threads, PersistPostLoad cleanup — the
   veteran community independently converged on every shape our Tier-1/2
   designs use. What has no precedent is only the *guarantee* — treating
   uninstall-cleanliness as a requirement with an enumeration behind it.
3. The one capability gap that forced the original community into
   accept-and-silence — no save hooks — **does not exist in the remaster**,
   measured by this project. We hold the tool ChoGGi asked the devs for.

So the honest position for the store page and the docs: **this pack meets a
bar no Surviving Mars mod has ever claimed — not because others tried and
failed, but because the community reasonably never made the promise. The
engine makes the promise expensive, not impossible, and the parts of it we
cannot keep are named, bounded, and inert.**

**Adopted from the survey (actionable):**
- Keep the global-lookup helper discipline (die-loudly orphans) — now with a
  measured *reason* rather than a false premise.
- `LuaSavegame.md.html` is a primary source: cite it in ENGINE_FACTS for the
  by-value design intent and the new-invocations rule (done with this
  commit).
- The RainsDeadlock post-the-missing-Msg design gains a working precedent
  (`Fix Eternal Dust Storm`), from a synchronous hook — reinforcing that the
  wrapper variant must survive the GT-creation-ordering probe before it is
  preferred over a synchronous heal.
- No community evidence supports building layer 1; the one runs-forever
  precedent (§3) supports Tier 1's rewrite priority instead.

---

## 7. Addendum (same day) — two owner questions the survey answered

**7.1 "Can we adopt his method for all our fixes?" — We already share it where
it is good; the remaining differences are deliberate upgrades.** His four
ingredients, scored: (a) wrap-first with a local-captured `orig` — we already
do this in nearly every wrapper (the divergent zero-upvalue/global-helper
discipline exists only in the persisted thread bodies, which Tier 1 deletes);
(b) a single file-local `mod_EnableMod` gate — NOT adopted: our per-call
registry/veto reads are what make 74 individually vetoable fixes and
console-safe self-deactivation work (FIX_POLICY §2); (c) his repair shapes —
already adopted and now precedented (§5); (d) his persistence hygiene
(no GameVars, silence persist errors) — explicitly declined; ours is declared
and audited. Wholesale adoption would trade veto granularity, footprint
accounting, and die-don't-linger orphans for nothing we lack.

**7.2 "Is Relaunched different enough for a different outcome?" — Same
physics, different calculus, all three differences favouring our stricter
standard.** (i) **The hooks exist now** — ChoGGi's library carries a comment
wishing for a post-save thread-restart hook he was sure would never come;
Relaunched has `SaveGameStart`/`SaveGameDone` reaching mods, measured by this
project. (ii) **Consoles** — every mitigation his community leaned on (read
the log, console commands, third-party cleanup mods, hex-editing
`active_mods`) is PC-only; Relaunched ships mods to Xbox/PS5 where none of it
exists, so silent residue has no escape hatch — which is why the cleaner mod
(FUTURE_IDEAS entry 5, now prelaunch) is not optional. (iii) **The game is
alive** — the original stopped patching, so "old bytecode runs from your
save" converged to harmless; Relaunched's active patching makes version skew
between persisted bodies and current code (the §2.5 upgrade-path class) a
live failure mode his years-at-scale record never stress-tested.
