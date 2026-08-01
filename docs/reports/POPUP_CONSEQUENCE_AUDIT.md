# Popup & Deferred-Consequence Audit — what can a player actually lose across a save/load?

Audit date 2026-07-30 (one-off session, `docs/POPUP_AUDIT_PROMPT.md`, deleted on
completion). Question asked, verbatim from the owner: *"Are we 100% sure that
this is the only thing that players can lose? No other decision popups can
provide a reward or item? What happens with anomaly reports if they get hit with
the save reload? … Do mysteries themselves have popups that have real
failures?"* Game build audited: **1.0.7.396349** (fpk parity proven —
ENGINE_FACTS.md). Every claim below was made against
`A:\SteamLibrary\steamapps\common\Project Spark\ModTools\Src`, not against
BUGS.md's own text. Method notes at the end (§9) — including which of this
audit's own verdicts rest on inference and the single observation that settles
each.

**Tiers:** R1 live · R2 conditional · R3 latent-by-data · R4 unreachable ·
U unknown (settling observation named) · I intentional — per the revised §4
draft (REACHABILITY_AUDIT.md, Challenge review).

---

## Headline — the alarm that queued this audit is OVERTURNED, and F83 narrows back down

**The storybit lead was wrong, and it was wrong about the engine, not about the
code it read.** The retracted-pending-audit claim was: storybits apply cost +
outcome + effects after two waits "in a `CreateGameTimeThread` with no
`MakeThreadPersistable` and no resume on load", so anomalies, mysteries and
random events were all presumed exposed. The premise — that a game-time thread
needs `MakeThreadPersistable` to survive a save — is **backwards**:

> **Game-time threads are persisted BY DEFAULT, with their full call stacks,
> including blocked waits. Real-time threads are not.** (§1, three independent
> source proofs + play-observed corroboration.)

Storybits, mysteries, sequences (all scenario content), and challenges run their
waits in game-time threads. They are **save-safe by the engine's own design** —
the persist machinery exists precisely so a thread blocked mid-`WaitMsg`/
`WaitWakeup`/`Sleep` resumes after load (§1). The defect family is exactly what
F83 already proved and no wider: **consequences owned by a REAL-TIME thread
waiting on a popup.** Real-time threads die on load, period; everything after
their wait — callback form or return-value form alike — is lost.

The full enumeration (§3) finds the consequential members of that family are:

1. **`FirstAsteroid`** — 3 prefabs, permanent, `show_once` — **OBSERVED (PT-58)**. F83.
2. **`ReconCenterDiscoveryAsteroid`** — paid Detailed Scan silently refused — F83's
   second site, recoverability still needs eyes.
3. **Breakthrough choice popups ×3 + `AssemblyChoice`** — real-time waiters
   carrying heavyweight consequences (a breakthrough discovery; the entire
   politics initialization), but their popups open **immediately, modal and
   game-pausing**, so no ordinary save can exist inside their window. Latent,
   not live — filed as **F85** (tier U, settling observation named).

Everything else with a popup wait is either cosmetic (a dead View button),
recoverable by re-clicking (launch confirmations and other player-initiated
dialogs), pre-game/tutorial (saving disabled), or game-time (safe).

**Consequence for F83: the narrow-decouple recommendation is REINSTATED** (§7).
Storybits and mysteries need no fix; there is nothing systemic to supersede it.

---

## §1 The engine machinery — what persists and what dies (the keystone facts)

### 1a. Game-time threads persist by default; real-time threads do not

`MakeThreadPersistable(thread, set)` sets/clears `const.threadPersist`
(CommonLua\Core\cthreads.lua:224-230). The default is nowhere stated in Lua —
the flag is applied C-side at creation — but three shipped idioms prove it, and
observed play corroborates it:

- **XWindow.lua:1554-1578** — picks `CreateThread = bGameTime and
  CreateGameTimeThread or CreateRealTimeThread`, then **clears** the flag:
  `MakeThreadPersistable(thread, false)`. Clearing is only meaningful if the
  game-time branch arrives with the flag SET.
- **_fixup.lua:9-37** — `RestartGlobalRealTimeThread` must call
  `MakeThreadPersistable(_G[name])` explicitly (:36); its game-time twin (:18-22)
  does not — and `OnMsg.PersistPostLoad` (:50-66) re-creates a global game-time
  thread **only when the save carried none** (`data[name] == nil`), i.e. it
  expects the thread to normally come through the save.
- **Notifications.lua:211-217** — a notification's game-time update thread is
  created bare (:212); the real-time variant gets an explicit
  `MakeThreadPersistable` + `DeleteThreadWithGame` (:214-216).
- **Corroborated in play, constantly:** every unit command thread is a bare
  `CreateGameTimeThread` (CommandObject.lua:100) and every save/load in this
  project's own playtests showed drones, rovers and colonists resuming
  mid-command (e.g. PT-25's rover kept its post-destruction route across a full
  save/quit/load). If game-time threads died on load, every load would
  idle-reset every unit.

The persist layer serializes blocked **stacks**: `OnMsg.PersistGatherPermanents`
(cthreads.lua:451-464) registers `Sleep`, `WaitMsg`, `WaitWakeup`, `WaitThread`
and `CObject.PlayState` as permanents with the comment *"this is another
sleeping function found in the thread stack"* — these are exactly the functions
a suspended coroutine has on its stack. `OnMsg.PersistSave` (:466-504)
additionally saves the wait registrations — which persistable thread is blocked
on which message key — filtered to `threadPersist` threads only, and the save
must run from a non-persistable thread (`assert` :467).

### 1b. The popup pipeline is 100% async — the persistable path is dead code

`ShowPopupNotification` (Lua\UI\PopupNotification.lua:245-291):

- **:246 `assert(not bPersistable) -- we don't support these`.** The sync
  (`sync_popup_id`) branch that `OnMsg.PersistSave` (:347-355) preserves across
  saves can never be taken by shipped code; no call site passes
  `bPersistable = true`. **Every shipped popup is async**
  (`context.async_signal = {}` :258), and the save handler therefore always
  stores an **empty** queue: an open popup's context never survives a load.
- **:261 `if context.start_minimized == false`** — the F83 fact: only an
  explicit `false` opens the popup immediately; `nil` (preset omits the field)
  means a **corner notification** (:268-288) whose `PressFunc` closure re-queues
  the context on click.
- Notifications ARE persisted — `GameVar("Notifications", {})`
  (Notifications.lua:1) — including closures. Observed: F83's surviving,
  clickable, dead-actioned notification after reload.
- An open popup is **modal** (`SetModal` :62-64), suppresses input
  (`XSuppressInputLayer` :10) and **pauses the game** (`XPauseLayer` :11-13)
  unless `context.dont_pause`. `PopupNotification:OnShortcut` (:154-162) eats
  every shortcut not in `PopupPropagateShortcuts`
  (MarsMessageQuestionBox.lua:1-9: Ctrl-F1, F9, F11, Shift-F11, -PrtScr, Alt-X,
  Alt-Shift-C). Quicksave is **Ctrl-F9** (GameCheatShortcuts.generated.lua:2210)
  — blocked; but the action is `ActionBindable = true` (:2211), so a player who
  rebinds Quick Save onto F9/F11 punches through the modal shield (F85, §7).
- `CanSaveGame` (CommonLua\Savegame.lua:92-99 + the `CanSaveGameQuery`
  handlers) knows nothing about popups — the only save blocks are tutorial,
  editor, pre-game menu, planetary view, camera transition, game-over. **The
  open-popup window is protected by UI reachability alone, not by the save
  system.**

### 1c. Why a game-time waiter + a minimized notification survives a load together

At save time during a minimized window, the persisted object graph contains BOTH
sides of the rendezvous: the blocked game-time thread (stack local
`async_signal`, plus the wait-registration keyed by that same table) and the
notification instance (whose `PressFunc`/`callback` closure captures the same
context). Persist serializes that graph **with shared-reference identity** — the
same mechanism that keeps a drone and its target request consistent across every
load. After load: click → context re-queued → popup opens → choice →
`PopupNotificationEnd` → `Msg(context.async_signal, i)` (:88-94) → the restored
thread is registered on that same restored table → **the wait completes and the
post-wait code runs.** *(Inferred from the persist design; the one live
confirmation is needs-eyes item 1 — it also covers storybits and sequence
popups, which ride the identical mechanism.)*

A REAL-TIME waiter has no line in the save at all — thread gone, wait
registration gone — while the notification half persists. That asymmetry is
F83's proven mechanism, and it is the **only** mechanism this audit found that
loses a consequence in ordinary play.

---

## §2 The safety rule (applies to every finding below)

A popup-gated consequence survives a save/load **iff the waiter is a game-time
thread**, because:

- **Minimized window** (notification sitting in the corner — the ordinary-play
  save window): GT waiter + notification both persist → reconnect (§1c).
  RT waiter → dies → F83.
- **Open-popup window**: the async context is dropped from `g_PopupQueue` on
  save (§1b) and the dialog is UI — nothing survives — but this window is
  **unreachable for saving** in ordinary play: modal + input-suppressed +
  game-paused (no autosave; sol-change autosaves ride game time), and the
  quicksave shortcut does not propagate at default bindings. Exceptions: a
  rebound quicksave key (F85), and the game's ONE `dont_pause` popup (§3.6).

---

## §3 Enumeration — every `WaitPopupNotification`/`ShowPopupNotification` call site

70 call sites in Src (67 live — one commented out, two are the function's own
definition/self-call). `ShowPopupNotification`'s `callback` parameter is **dead
code** — the body never stores or calls it (:245-291) — so every Show-only site
is pure display with no deferred consequence; they are listed once as a class.
The Wait sites are grouped by verdict. Thread type was read at each call site,
not assumed.

### 3.1 CONSEQUENTIAL + real-time + minimized — the F83 family (the live defect)

| Site | Thread | What is lost after a reload | Tier | Status |
|---|---|---|---|---|
| `Asteroids.lua:411-422` FirstAsteroid | `CreateRealTimeThread` :414 | 3 Micro-G extractor prefabs the popup's own text promises; `show_once` + `asteroid_count == 1` gate → **no second chance ever** | **R1** | **OBSERVED** — PT-58, 1/1/1 vs 0/0/0 |
| `Discoveries.lua:117-137` ReconCenterDiscoveryAsteroid | `CreateRealTimeThread` :118 | choice 1: planetary-view jump (cosmetic); **choice 2: the paid Detailed Scan** — `PerformDetailedScan` never runs, nothing charged, action silently refused. Fires on EVERY asteroid discovery | **R1** (frequency high) | Inferred; **recoverability of the scan via other UI = needs-eyes item 2** |

Intent (family): **unintended — self-contradiction.** FirstAsteroid's popup text
promises the delivery its own path can drop (the F83 entry's tell, unchanged);
and the engine ships a whole persistence apparatus (§1) that these two sites
bypass by choosing `CreateRealTimeThread` where every safe sibling (challenges,
storybits, sequences, status effects) uses game time. Sibling contradiction
inside one codebase.

### 3.2 Cosmetic + real-time + minimized — dead View buttons (F83's six, corrected to the true list)

All real-time waiters whose entire post-wait consequence is
`ViewAndSelectObject` or nothing at all. After a reload the surviving
notification opens a popup whose View does nothing (observed organically —
the original F83 finding) — no game state is lost.

- `ColonyViability.lua:50-56` FirstFounder‹trait› (callback View) — the observed one
- `ColonyViability.lua:170-177` LastFounderDies · `:182-189` FirstFounderDiesOfOldAge · `:196-203` FirstColonistDeath · `:213-220` LastFounderLeavingMars (all callback View; the enclosing `OnMsg` already set the GameVar latch and emitted its `Msg` BEFORE the thread spawns, so only the View dies)
- `ColonyViability.lua:91/93/119/148/150` ColonyViabilityExit_* / FirstPassengerRocket — `WaitPopupNotification` **is** the whole thread body; no post-wait code exists
- `Asteroids.lua:136-141` Asteroid_Evac — callback and return value both only `ChangeCurrentMapSlot` (view the asteroid); the evac state itself (`g_AsteroidsInEvac`, `LeaveAfterDelay`) is set outside the popup
- `Asteroids.lua:154-156` AsteroidLost — display only
- `Milestones.lua:102-104` AllMilestonesCompleted — display only

**Correction to the F83 entry's table:** the eighth callback site,
`ColonyViability.lua:260` (`class.popup_on_first`, the FirstStatusEffect_*
popups), is a **game-time** thread (:244) and its presets open immediately
(`start_minimized = false`) — it is safe on both axes and does not belong in the
exposed list. Tier for this whole class: R1 reachable, harm ≈ 0. Intent:
same family as 3.1; not worth fixing on its own (F83 entry option 4 stands).

### 3.3 CONSEQUENTIAL + real-time + opens-immediately — shielded by the modal window → F85 (latent)

These popups open instantly (`start_minimized = false` in preset or params),
modal + pause. No ordinary save can exist inside their window (§1b/§2) — but the
waiter is real-time, so any save that DOES land there (rebound quicksave;
a future `dont_pause`; a future minimized re-preset) silently voids a heavyweight
consequence. This is one latent family, filed as **F85**:

| Site | Thread | Consequence sitting after the wait |
|---|---|---|
| `Anomaly.lua:696-714` ShowBreakthroughChoicePopup (presets SubsurfaceAnomalyBreakthrough / PlanetaryAnomalyBreakthrough / Policy_Breakthrough; callers Anomaly.lua:393, PlanetaryAnomaly.lua:268, LawDef-Research.lua:78) | `CreateRealTimeThread` :703 | `UIColony:SetTechDiscovered(techs[res].id)` :708 + caller callback — **the breakthrough discovery itself**. The anomaly is already consumed (`DoneObject`, PlanetaryAnomaly.lua:351) |
| `Factions.lua:1191-1236` AssemblyChoicePopup (preset AssemblyChoice, `start_minimized = false`, Laws.lua:10) | `CurrentMap:CreateRealTimeThread` — MartianAssembly.lua:8 | `ApplyAssemblyChoice` :1214 — **faction weights, initial laws, standings init, `ElectMembers()`**: the entire politics system for the rest of the game. `AssemblyBase:GameInit` never re-runs |

Reachability: **U** — reachable only if a save can be produced with the popup
open. The one candidate vector at default bindings is none; with Quick Save
rebound onto F9/F11 (both in `PopupPropagateShortcuts`, and the action is
`ActionBindable`), the shortcut reaches the dialog. `CanSaveGame` does not
object (§1b). **Settling observation = needs-eyes item 3.** Intent: unintended
(same sibling contradiction as 3.1); the shield is an accident of modality, not
a design choice — but per the revised §4 draft, no fix is written on a U with
the observation pending.

### 3.4 Player-initiated confirmations + real-time + opens-immediately — recoverable, no fix warranted

Same shield as 3.3, and even if a save landed in the window the loss is a
confirmation flow the player simply re-triggers — no resource is spent before
the wait in any of them:

`CargoRequestNew.lua:303-354` + `LanderRocketCargoRequest.lua:206-217` (launch
issue prompts; post-wait `CmdLoad`/`CancelFlight`) · `RocketBase.lua:2199` +
`RocketUtilities.lua:103/118` + `LanderRocket.lua:90-99` (launch/depart
confirmations) · `PlanetaryView.lua:357/382/417/457` (expedition confirmations —
planetary view additionally **blocks saving entirely**, Lua\Savegame.lua:58-60)
· `XDef/PoliticsDlg:627` OfferAgenda → `PickAgendaOffer` ·
`XDef/LawVotingCard:469` Negotiations → quest insert · `:280` NegativeOutlook
(vote-anyway confirm) · `XDef/ResearchDlg:1211` (queue confirm) ·
`Legislature.lua:231-237` EarthCouncilIntro → `OpenElections` (UI) ·
`GameOver.lua:45` · `_StoryBits.lua:1199` + `MarsStoryBits.lua:277` (dev/testing
UI) · `ParadoxMenu.lua:310/343`, `PreGameMission.lua:823-879` (menu / pre-game —
no game to save) · `Tutorial.lua:436/444` + `Construction.lua:2375`
(tutorial popups — **saving is disabled in tutorial**,
CommonLua\Savegame.lua:76-78; tier I).

### 3.5 Game-time waiters — safe by the engine's design

- `Challenges.lua:26` challenge_thread and `:108` challenge_timeout_thread are
  both `CreateGameTimeThread`; the Challenge_Completed/Perfected loop (:76-104)
  and Challenge_Failed (:131-147, **return-value form** with restart/exit
  consequences) persist blocked and resume. Their presets open immediately
  anyway.
- `ColonyViability.lua:244-264` status-effect popups (GT thread, opens
  immediately).
- **Storybits** (§4) and **sequences/mysteries** (§5) — the two systems the
  owner asked about — below.

### 3.6 The one `dont_pause` popup — DistressCallPopup, and the queue-drop corner

`RivalColonies.lua:535-555`: the distress-call confirmation sets
`dont_pause = true` (:546) and waits in an `XWindow:CreateThread` (real-time by
definition, XWindow.lua:1412-1421). Because the game RUNS under this popup, a
sol-change **autosave can land while it is open** — the only shipped popup
window where that is true. What that save loses: the popup context (async →
dropped, §1b). On load the popup has vanished; nothing was committed before the
wait (no cooldown set, no standing spent — both post-wait :549-553), and the
Broadcast button is available again. **Harm ≈ 0, self-healing. Tier R2, no fix.**

The real corner is compound: any **other** async popup queued behind the open
distress popup at that autosave (including a storybit's `WaitStoryBitPopup`
context — queued, not yet open, so no corner notification exists for it either)
is dropped from `g_PopupQueue` with **no notification to resurrect it**. Its
game-time waiter persists blocked forever → for a storybit: event evaporates,
`g_StoryBitActive` ghost entry, and `Complete()`/re-`Register()` never run, so a
non-OneTime bit is dead for that colony. Reachability: **R3-edge** — needs the
player mid-distress-flow at the exact sol tick with a storybit popup queued
behind; recorded here for completeness, folded into F85's entry as a note, no
fix proposed.

---

## §4 Storybits end to end — the retracted lead, re-audited

Flow (`_StoryBits.lua`): `ActivateStoryBit` :461-476 →
`run_thread = CreateGameTimeThread(RunWrapper)` :475 → `Run()` :526-582 →
`OpenPopup()` :584-699 → `Complete()` :701-707.

- **Activation effects** (:548-552) run before any wait — safe (as the F83 entry
  already said).
- **Delay window** (:536 `StoryBitDelay` = plain `Sleep`, :1079-1081): GT thread
  asleep — **persists, resumes, safe.**
- **Notification window** (:568-580): `AddStoryBitNotification`
  (MarsStoryBits.lua:50-57 — a persisted notification carrying a callback
  closure) + a `WaitWakeup(100)` poll loop in the GT thread. Save here → thread
  + notification + `StoryBitState` (`g_StoryBitActive` GameVar :107, with
  `run_thread` a member :257) all persist in one graph → click after load →
  `Wakeup(self.run_thread)` :572 → loop exits → popup. Even in the worst case
  (upvalue sharing on `stop_wait` :569 not restored), the loop's own timeout
  fires: `const.StoryBits.NotificationTimeout` (__const.lua:1779-1785, help text
  *"before the pop up is forced"*) — the popup is **forced open** ~2 game hours
  after activation regardless. **Safe; degradation is cosmetic latency.**
  *(Inferred — needs-eyes item 1 is the live confirmation.)*
- **Popup window** (:621-625 → `WaitStoryBitPopup`, MarsStoryBits.lua:63-84):
  `start_minimized = false` :71 → opens immediately, modal, paused → no
  ordinary save window exists (§2). The GT waiter would even survive a save
  here — what would not is the queue entry (§1b) — but the window is shielded.
- **Cost ordering** (:667-671): `StoryBitPayCost` runs AFTER the reply is
  chosen, immediately before the outcome roll (:673-679); the outcome popup
  (:688, second `WaitStoryBitPopup`) sits between the payment and
  `ProcessOutcomeEffects` (:690) — so "paid but no outcome" requires a save
  **inside an open modal popup**, the shielded window. At default bindings:
  unreachable. Under F85's rebind vector: reachable, and the storybit family
  is where it would bite hardest (money gone, outcome lost, `Complete()`
  skipped). Covered by F85's settling observation.
- **Stranding bookkeeping**: `OnMsg.LoadGame` (:109-120) prunes deleted presets
  only, and `OnStopRunning` (:507-524) sweeps `g_StoryBitActive` entries whose
  `run_thread` is no longer a valid thread — a self-heal that exists for
  abnormal deaths. A thread blocked forever in `WaitMsg` is still "valid", so
  the §3.6 corner is not swept — but no ordinary path produces it.

**Verdict: the storybit system needs NO fix.** The retracted claim's specific
errors, for the record: (1) `MakeThreadPersistable` absence is the *safe*
default for GT threads, not a missing call; (2) "no resume exists anywhere" —
none is needed, the thread itself persists; (3) "the vulnerable window is the
notification" — that window is the *designed-safe* one, including a forced-popup
timeout backstop. What the lead got right: `Unregister()` at activation (:470)
does mean a storybit killed abnormally mid-run is not re-picked — but the only
reachable killer found is §3.6's compound corner.

Anomaly/mystery/event entries into storybits (`Discoveries.lua:49` recon Event
discoveries · `PlanetaryAnomaly.lua:341` expedition events ·
`ClassDef-StoryBits.lua:151` / `MarsStoryBits.lua:309-311` ActivateStoryBit
effect, ForcePopup default true = `immediate` → skips the notification window
entirely) — all inherit the same verdict.

---

## §5 Anomalies and mysteries — the owner's direct questions, answered

- **Map (rover-scanned) anomalies** (`Anomaly.lua:384-441` ScanCompleted):
  research points, tech unlocks, resource stockpiles are granted **inline in the
  scanner's game-time flow — no wait, nothing to lose.** The two deferred paths:
  `breakthrough` → §3.3 (F85, shielded), and `self.sequence` →
  `StartSequence` → §5b. **Anomaly reports are not "just text", and they are
  not exposed** — the answer to the owner's second question.
- **Planetary anomalies** (`PlanetaryAnomaly.lua:261-352` Scan): same shape —
  inline grants; `breakthrough` → §3.3; `event` → `ForceActivateStoryBit`
  (:341) → §4. The old `AnomalyAnalyzed` wait-popup is **commented out**
  (:299-305) in favor of a HUD notification — one fewer live site than the
  call-site grep suggests.
- **Mysteries** run as scenario **sequences**: `SequenceListPlayer`
  (CommonLua\Libs\Sequences\SequenceListPlayer.lua) starts each sequence thread
  as `seq.real_time and CreateMapRealTimeThread or CreateGameTimeThread`
  (:274) — and **no shipped scenario sets `real_time`** (whole-tree grep over
  `Lua\Scenario\*.generated.lua`: zero hits) → every mystery/anomaly-sequence
  thread is game-time and persists blocked, including inside `SA_WaitChoice`/
  `SA_WaitMessage` popups (SequenceAction.lua:333-338/391-394 — note their
  `start_minimized` **defaults true** :83/:207, so the minimized-window analysis
  of §1c is the operative one). The system even ships a persistable **watchdog**
  (:93-141) that detects an abnormally dead sequence thread and restarts the
  sequence **from the next action** — recovery machinery, further evidence the
  designers intended sequences to survive anything.
- **Mystery popups with "real failures"** — the third question: sequence choice
  results are returned into sequence registers and consumed by later
  `SA_WaitChoiceCheck` conditions; since the thread persists, the choice is not
  losable in ordinary play. **F06 is NOT a member of this family** and needs no
  re-scoping: its defect is a **one-shot `Msg` emitted while the sequence sat
  in a player-gated popup** (`CrystalFlyAway`, fired once, nobody listening
  yet) — a path-vs-state race that exists with no save/load involved at all.
  Its shipped fix (re-broadcast until consumed) remains the right shape, and
  its audit note ("easier to hit than the entry says") stands unchanged.

---

## §6 Broader sweep — same shape outside popups

Swept `CreateRealTimeThread` bodies containing waits across `Lua\` (multiline
grep + per-site reads). Beyond the popup sites already enumerated: visual/UI
lerps (Heat.lua:115-118, Flight.lua), camera/planet scene transitions
(PlanetScene, InGameInterface, OverviewModeDialog), PhotoMode, and
GamepadTerrainObjects — all cosmetic/UI state with no game-state consequence
after the wait. `WaitIssueDistressCall` (the actual resource delivery of §3.6)
runs in a **game-time** thread (RivalColonies.lua:550) — safe. No additional
consequential real-time-wait pattern was found. One-shot `Msg` races of the F06
kind were not exhaustively swept (they are path-driven, not save-driven, and out
of this audit's question); F06 remains the only observed instance.

---

## §7 Fix-shape recommendation for the family

**The family is per-call-site, not systemic.** The engine machinery is healthy
and the safe idiom (game-time waiter) is used by every subsystem that carries
real consequences — except the two sites in §3.1 and the latent class in §3.3.

1. **F83 option 1 — the narrow FirstAsteroid decouple — is REINSTATED as
   recommended, unchanged from the entry:** additive `OnMsg.SpawnedAsteroid`
   granting the three prefabs once behind a persistent flag (FIX_POLICY §1.2).
   It repairs the only observed loss; PT-58's fixture is the ready A/B (reload
   leg must read 1/1/1). Nothing found by this audit enlarges or supersedes it.
2. **`ReconCenterDiscoveryAsteroid`** — grade after needs-eyes item 2. If the
   Detailed Scan is reachable later from the planetary view, this is cosmetic
   (silently-refused click, retry available) → document, no fix. If not, the
   same decouple shape does not apply (the popup IS the offer); the honest fix
   would be flipping that one preset to `start_minimized = false` (data patch,
   §1.1) so the offer never sits in the vulnerable window — decide only with
   the observation in hand.
3. **F85 (breakthrough choices + AssemblyChoice)** — file, observe (needs-eyes
   item 3), fix nothing until U resolves. If the rebind vector proves real, the
   cheapest correct family fix is the same one vector-by-vector: move each
   consequence out of the RT thread (e.g. breakthrough: pick-and-apply in a GT
   thread, RT popup only reports) — but that is a decision for after the
   observation, per the revised §4 draft.
4. **The general re-arm** (F83 option 2 — resurrect stranded async waiters on
   load) stays **NOT recommended**, now with a stronger reason: the engine
   already persists every waiter that matters; a re-arm layer would exist for
   two call sites and risk double-delivery against the working GT machinery.
5. **Storybits, mysteries, sequences, challenges: no work.** The six cosmetic
   View sites: no work (document only — F83 entry option 4).

---

## §8 Needs-eyes list — the handoff

Single observations, cheapest first; none blocks the F83 fix (item 1 would
only *strengthen* the audit's central overturn, and items 2-3 gate their own
entries, not F83):

1. **Storybit save/load in the notification window** (confirms §1c/§4, the
   audit's one load-bearing inference). Console: `ForceActivateStoryBit("<any
   enabled bit with a popup>", MainMap)` (NOT immediate) → corner notification
   appears → save → load → `IsValidThread(g_StoryBitActive[1] and
   g_StoryBitActive[1].run_thread)` — expect **true** (thread survived) → click
   the notification → popup must open; answer it → outcome popup/effects must
   run. Also confirms sequence popups by mechanism-identity. ~5 min.
2. **Detailed Scan recoverability** (grades F83's second site, §7.2): let a
   `ReconCenterDiscoveryAsteroid` popup die across a reload (or just decline
   choice 2 on a live one), then check whether the planetary view / asteroid UI
   offers the paid Detailed Scan for that asteroid anywhere else. Needs a Recon
   Center holding ≥ `g_Consts.DiscoveryScanCost` Electronics for the comparison
   leg (`CanPerformDetailedScan()` true).
3. **The rebind save vector** (settles F85's U): rebind Quick Save to **F9**
   (Options → Key Bindings), open any choice popup (a launch-issue prompt is
   the cheapest), press F9. Does a save land? Then load it: the popup should be
   gone and its consequence gone with it. If the binding UI refuses or the
   save is blocked, F85 drops toward I/R4 and is a documentation note only.
4. **(Optional, completes §3.6)** With the distress-call popup left open, let a
   sol tick pass and confirm the autosave fires under it (the only popup window
   where the game runs). Confirms the compound corner's precondition; the
   corner itself is not worth staging.

---

## §9 Method notes & self-audit (the F49(c) discipline applied to this audit)

- **What is observed:** PT-58 (FirstAsteroid loss, 1/1/1 vs 0/0/0); the
  surviving-notification/dead-View mechanism (F83's keyboard session); units
  resuming mid-command across loads (every playtest — the behavioral proof of
  the GT-persist default); the dead `assert(not bPersistable)` and every
  call-site/preset/thread-type enumeration (source, decisive on "can this
  execute").
- **What is inferred and flagged:** §1c's identity-restoration argument (and
  with it §4's storybit-window and §5's sequence-window safety) — needs-eyes
  item 1; the F85 rebind vector — item 3; Detailed Scan recoverability —
  item 2. Per the Challenge-review lesson, none of these inferences authorizes
  a fix or a `wontfix` on its own; each carries its settling observation.
- **What this audit corrects in prior project docs:** the F83 entry's storybit
  paragraph (retraction of the retraction — see the entry's audit note); the
  same entry's call-site table (eighth site is GT + open-immediately, §3.2);
  ENGINE_FACTS gains the thread-persistence default and the all-popups-are-async
  facts (this audit's two keystone facts, both previously assumed backwards or
  unknown).
- **Evidence freshness:** `git log` re-read between assembling these verdicts
  and publishing (rule from the Challenge review); no commits landed mid-audit.
- **Bound on the sweep:** §6's non-popup sweep covered real-time-thread waits;
  it did not exhaustively hunt F06-style one-shot `Msg` races (path-driven, not
  save-driven — a different question with a different method).
