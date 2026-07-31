# ONE-OFF PROMPT — Popup & deferred-consequence audit (created 2026-07-30)

**Status: LIVE, un-run.** Delete this file (and its pointer in
`FABLE_NEXT_PROMPT.md`) when the audit is complete and its findings are recorded.
Paste everything below into a fresh Claude Code session — any Claude model.

---

You are working on the Surviving Mars: Relaunched **"Community Fix Pack"** at
`C:\Dev\SMR-BugFixPack` (git, pushes to `main`). Game source, read-only, NEVER
modify: `A:\SteamLibrary\steamapps\common\Project Spark\ModTools\Src`.

**Start with `git log --oneline -8` + `git pull`.** Then read, in order:
`docs\ENGINE_FACTS.md` (whole file) · `docs\STATUS.md` header ·
`docs\FIX_POLICY.md` (especially **§4a**) · the **F83** and **F06** entries in
`docs\BUGS.md` · the "Challenge review 2026-07-30" appendix at the end of
`docs\REACHABILITY_AUDIT.md`.

## Why you exist

The owner asked a question that stopped a fix from shipping:

> *"Are we 100% sure that this is the only thing that players can lose? No other
> decision popups can provide a reward or item? What happens with anomaly reports
> if they get hit with the save reload? Are they just text, or can they trigger
> events? Do they have mystery interactions? Do mysteries themselves have popups
> that have real failures? I think we need a deep dive into popups before we can
> unilaterally say we are fixing it by just giving the reward in a round about way
> and calling it 'fixed'."*

He is right. **F83 was filed as "First Asteroid loses three prefabs across a
reload", and a narrow fix was recommended. That recommendation is RETRACTED
pending your audit.** The suspicion is that F83 is one visible symptom of a
general defect: **player-facing consequences that are applied AFTER a wait, in a
thread that does not survive a save/load.**

## What is already established — do NOT re-derive

**The F83 mechanism, play-proven 2026-07-30:**
- Popups gate "open immediately" on `context.start_minimized == false`
  (`Lua/UI/PopupNotification.lua:261`) — an explicit `== false`. Presets and call
  sites that never set the field get `nil`, so they **start minimized** as a
  corner notification.
- The waiter is a **real-time thread** blocking in `WaitMsg(context.async_signal)`
  inside `WaitPopupNotification` (`:293-306`).
- Neither survives a load: real-time threads are not persisted, and
  `OnMsg.PersistSave` keeps only queue entries carrying a `sync_popup_id` —
  async ones are dropped.
- **The notification DOES survive.** So after a reload it still opens, any choice
  fires `Msg(async_signal, i)` with nothing listening, and the callback never runs.
- **PT-58 (archived) proved the consequence:** answered without a reload →
  prefabs `1/1/1`; saved unanswered, reloaded, answered → `0/0/0`.

**Already-cleared ground:**
- **`choiceN_func` is SAFE.** Presets may define `choice1_func`..`choice4_func`;
  they execute in the UI action handler (`PopupNotification.lua:135`) **before**
  `host:Close(i)`, i.e. not in the waiting thread. 8 uses in `Data/`. Confirm the
  list, but they are not at risk from this mechanism.
- **Eight `WaitPopupNotification` call sites pass a callback** (excluding the two
  `PreGameMission.lua` tutorial calls, which pass a `host` parent, not a
  callback): `Asteroids.lua:415` (grants 3 prefabs), `Discoveries.lua:126`
  (choice 2 = the paid Detailed Scan), and `ColonyViability.lua:52/173/185/199/216/260`
  (all `ViewAndSelectObject`, cosmetic).
- There are **~70** `ShowPopupNotification`/`WaitPopupNotification` call sites in
  total — the callback form is only a subset. **The return-value form matters
  just as much**: code written *after* the wait, in the same thread, is equally
  lost.

**The storybit lead — the reason this audit exists (source-read, NOT observed):**
Anomalies, planetary anomalies, random events and mystery beats all route
through storybits (`Discoveries.lua:49`, `PlanetaryAnomaly.lua:341`,
`ClassDef-StoryBits.lua:151`, `MarsStoryBits.lua:310` all call
`ForceActivateStoryBit`). Flow in `Lua/_StoryBits.lua`:
- `StoryBitState:ActivateStoryBit` (:461) →
  `self.run_thread = CreateGameTimeThread(self.RunWrapper, …)` (:475)
- `Run()` (:520-582) applies **ActivationEffects immediately** (these are before
  any wait — safe), then posts a corner notification and waits in a
  `WaitWakeup(100)` loop until the player clicks it or
  `const.StoryBits.NotificationTimeout` game-time elapses.
- `OpenPopup()` (:583-696) → `WaitStoryBitPopup` → reply → **`StoryBitPayCost`**
  → weighted outcome roll → outcome popup → **`ProcessOutcomeEffects`** →
  **`Complete()`**.
- **Everything from the reply onward is after the waits, in that thread.**
- `g_StoryBitActive` is a **GameVar** (:107) so the state object persists, but
  `run_thread` is a plain `CreateGameTimeThread` with **no
  `MakeThreadPersistable`**, and `OnMsg.LoadGame` (:109) only prunes states whose
  presets no longer exist. **No resume exists anywhere**, including
  `_StoryBitsRemaster.lua` / `MarsStoryBits.lua` (grepped).
- `Unregister()` runs at activation, so a stranded storybit cannot be re-picked.
- Storybit popups set `start_minimized = false` (`MarsStoryBits.lua:63-84`) so
  they open immediately — but they are **preceded by a corner notification**,
  which is the vulnerable window.

**F06 is already a documented instance of this family** (Mystery 10's Epilogue
arrives minimized and a one-shot `CrystalFlyAway` is missed while it sits). Read
its entry and its audit note.

## Your task

Produce **`docs/POPUP_CONSEQUENCE_AUDIT.md`** on the model of
`docs/REACHABILITY_AUDIT.md`. Enumerate **every** path where a player-visible
consequence — a reward, a cost, a state change, a story outcome, a completion —
is applied after a wait, and classify each by whether it survives a save/load.

At minimum cover:
1. **Every `WaitPopupNotification` call site**, both the callback form and the
   return-value form. Say for each what is lost if the thread dies.
2. **Storybits end to end**: activation effects vs reply/outcome effects, the
   notification window, the popup window, `Complete()`, and what a stranded
   `g_StoryBitActive` entry does to future storybit selection.
3. **Anomalies** (map and planetary) and **mysteries** — where they enter the
   storybit system and what they can cost a player.
4. **Sequence-driven popups** (`SA_WaitMessage` and friends) — the F06 family.
5. Anything else you find with the same shape. Do not stop at popups if the
   pattern is broader.

For each finding record: file:line evidence · what a player loses · the
**reachability tier** (R1/R2/R3/R4/U/I) with a real enumeration, not a
self-description · a **positive intent statement** with a hard tell · and whether
it is **observed or inferred**.

Then: **recommend a fix shape for the family, not just for F83.** Say explicitly
whether F83's narrow decouple is still the right first step, or whether it should
be superseded.

## Testing — you have the game to yourself

**The owner is away from the keyboard.** You may run whatever you like,
unattended, including full A/B legs. `docs\FABLE_NEXT_PROMPT.md` has the harness
facts; the essentials:
- Launch: `& "c:\program files (x86)\steam\steam.exe" -applaunch 3215050 -smrautorun`.
  A leg takes ~70 s once Mars.exe appears, but Steam can take minutes to get
  there. **Never kill on a short timeout** (25 min no-kill guard).
- **Check Mars.exe is NOT running before touching loadable code** (`tasklist`).
- Current expected legs (76 probes): all six toggles ON → `73/73`,
  `66 PASS / 0 FAIL / 10 SKIP / 0 ERROR`; default config → `67/73`,
  `61 / 0 / 15 / 0`. Account state as of 2026-07-30: **six toggles OFF, both
  D09 dials at base** — read it, never assume it.
- The TestKit (`C:\Dev\SMR-BugFixPack-TestKit`, local-only, never pushed) can
  carry new probes if a probe is the right instrument. `SMRTest.Register` needs
  an explicit `return "PASS", …` — a `run` that falls off the end silently
  becomes a SKIP.
- Baseline legs overwrite the fix pack `metadata.lua` `code` list — **keep the
  `default_options` block**, restore from a saved copy, and **never
  `git commit -a` while that edit is in the tree**.

**The owner also keeps a save fixture for this family:** a save taken *before*
the `ReconCenter` tech was ever researched, on the PT-58 colony. Loading it
restores `g_ShownPopupNotifications`, so the `show_once` First Asteroid popup
re-offers itself on every run and the A/B is repeatable indefinitely. Ask before
assuming any other fixture exists.

**What you cannot do yourself:** anything needing a human at the keyboard —
watching whether the game permits saving while a popup is open, clicking a
storybit notification, judging feel. **Collect those into an explicit
"needs-eyes" list** with, for each, the single observation that settles it. That
list is your handoff.

## Hard rules

- **FIX_POLICY §4a (owner hard rule):** this pack never fixes other mods'
  problems, and never a vanilla bug reachable only from mod code. The test is
  **who benefits** — could a PLAYER be harmed now or after a future patch/DLC?
  Yes → real fix. Only-a-mod-benefits → barred. Judge by enumeration, never by an
  entry's own words.
- **Do NOT build or ship any fix.** This audit ends in findings and a
  recommendation. The owner decides what gets built. That includes F83's fix —
  it is explicitly on hold pending your verdict.
- **Source is decisive on "can this execute" and near-mute on "is this wrong".**
  Anything whose wrongness lives in UI, threading, hit-testing or save/load
  timing needs a keyboard observation before it is called a defect. Mark
  inferences as inferences (the F49(c) lesson — a confident source reading was
  wrong and cost a shipped guard).
- **Re-read `git log` between assembling conclusions and publishing them.**
- `error()`/`assert()` in mod code report and continue — they do not unwind.
- Commit with
  `git -c user.name="SMR-BugFixPack" -c user.email="154917955+catt144@users.noreply.github.com"`,
  push the fix pack; the TestKit stays local-only. Commit messages via
  `git commit -F <file>` — **no embedded double quotes** (PowerShell 5.1 splits them).
- Docs: never round-trip through PS 5.1 `Get-Content` without `-Encoding UTF8`
  both ends; prefer the editor's file tools.

## When you finish

1. `docs/POPUP_CONSEQUENCE_AUDIT.md` written, with the needs-eyes list.
2. **BUGS.md updated** — new F-numbers for anything that qualifies (highest in
   use is **F84**), and the **F83 entry updated** to say whether it stands as
   filed, is superseded, or should be re-scoped.
3. **STATUS.md** header updated (counts, open decisions, next gates).
4. A new leg prepended to `docs/archive/SESSION_LOG.md`.
5. **`docs/FABLE_NEXT_PROMPT.md` updated** — replace its pointer to this file
   with your actual findings, so the next playtest session picks up the
   needs-eyes items and the decision the owner now owes.
6. **Delete this file** and commit everything.
