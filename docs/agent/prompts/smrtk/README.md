# smrtk — the chain manifest (SMR Tool Kit)

Effort: replace the game's built-in cheat menu, for playtesting, with an **SMR Tool Kit panel** that lives in the
TestKit mod: every useful cheat action called through its **leaf body** (no `CheatsUsed` taint, `EF-095`), every
action logged under one **`SMRTK_`** tag so an agent reading a log never has to ask, a **slot engine** an agent can
pre-load before a sitting, **triggers** (breakpoints for a game), **save/load slots**, a **console tap + clipboard
copy**, the **TestKit on buttons**, and a **layout stamper** built on the game's own construction front door
(`EF-099`). Authored 2026-09-13 by `smr-bugfixpack-8f` (Fable) with the owner, in one design conversation.
Method: `agent/reports/CHAIN_METHOD.md` (shape D, kill-gated build). Authoring mechanics: `agent/WORKFLOW.md`
"Authoring a prompt" elements 1–9. Owner decisions: checklist **175**.

> ⚖️ **WHY, in the owner's words:** *"I don't like using the game's built in cheat. I triggered things that trip up
> agents and we also need rules about cheats in the documentation and I still get questions about it. Also I have to
> re-activate it every time I load."* And on the slot idea: *"we could build like 4 or 5 agent buttons so an agent could
> prebuild certain commands or scripts before I sit down for play testing … which would save massive amount of time
> copy and pasting."* And on the stamper: *"This would truly be a game changer in setting up testing scenarios."*
>
> ⚖️ **THE TWO HARD REQUIREMENTS (owner):** **(A)** nothing the panel does may register as a cheat in vanilla's
> detection — `CheatsUsed` stays empty, achievements stay eligible; **(B)** every line the panel writes is
> recognisably the toolkit's (`SMRTK_<Verb>`), so an agent attributes it at a glance.
>
> ⚖️ **SCOPE (owner, 2026-09-13):** *"I agree with all of that"* — the whole tiered list, hard items included
> (*"once we have it as a tool we have it forever"*). Home: the TestKit mod. UI: **both** — an infopanel section for
> per-object actions where the vanilla Cheats section sits, and a floating tabbed panel for everything else.

## The queue

| # | file | model | owner needed? | what it drains |
|---|---|---|---|---|
| 01 | `01_SKELETON_BUILD_opus.md` | Opus | no | job 0 re-validates this cut; core (slot engine, logger, ring buffer, taint assert, `ConsoleEnabled` arm), the panel frame (status strip, top row, tabs), MARK / Copy / Flush / cls / eligibility; predictions + 02's script |
| 02 | `02_SKELETON_SITTING_owner.md` | any (attended) | ✅ keyboard, ~20–30 min | ⛔ KILL GATE: no taint after a leaf action, console hotkey with the Mod Manager CLOSED, the console tap sees prints, clipboard copy pastes, panel survives a load |
| 03 | `03_WORLD_ACTIONS_opus.md` | Opus | no | the World page: disasters (cursor-targeted, leaf calls) + stop, quiet mode, speed / ultra / run-until, fix all / malfunction all, finish-waits, spawn / funding / research re-exposures, trait submenu |
| 03b | `03b_INFOPANEL_SECTION_opus.md` | Opus | no | the per-object section in the infopanel (Fill, Empty, Delete, Destroy, CleanAndFix, Malfunction, AddPrefab, Spawn*, Upgrade1–6, Dump, Pin) — the injection technique is its own risk |
| 04 | `04_AGENT_PAGE_opus.md` | Opus | no | the Agent page: `SMRTK.Bind`, the `80_AgentSlots.lua` contract, fire-once vs armed, click-to-target, auto-disarm, fire counters, pins A/B/C, triggers, note field, screenshot+mark |
| 05 | `05_SAVES_AND_KIT_opus.md` | Opus | no | Saves page (A/B/C with session-id guard, provenance stamp) + Kit page (RunAll / run-one-probe with verdicts, logger toggles, log tail, error counter, fingerprint, snapshot + diff, watch-a-field, force-open console) |
| 06 | `06_STAMPER_fable.md` | Fable | no | the layout stamper: capture → clipboard → `Layouts/<name>.lua`; ordered replay; fit check; grids; then state (upgrades) |
| 07 | `07_DOCS_AND_SITTING_PREP_opus.md` | Opus | no | WORKFLOW + PLAYTEST_HELP + TestKit README; `perma/SMRTK_SLOTS.md` (how an agent pre-loads a sitting); predictions + 08's script |
| 08 | `08_FULL_SITTING_owner.md` | any (attended) | ✅ keyboard, 07 prices it | the full attended leg: every page, every button class, a stamp, a save/load round trip, a trigger firing |
| 99 | `99_AUDIT_fable.md` | Fable | ✅ raises | terminal adversarial audit: the taint invariant re-derived against the ARCHIVED log, every action's route read for `NetSyncEvent`/`LogCheatUsed`, tag coverage, falsifiers RED, verdict, folder-empty gate, kickoff lines |

Model placement: Fable on **06** (the capture format is a contract every future layout depends on) and **99**
(the adversary) — 2 of 8 agent links. 01 is Opus because this README and `EF-095`–`EF-099` carry the contract;
**01's job 0 is to re-validate the cut** with authority to rewrite any unconsumed link (route a disagreement to
ck175 rather than absorb it). ⚠️ The owner may fire an adversarial fresh-context read of this folder before 01;
it is optional because 02 is the empirical check of every premise.

**Owner time:** two attended sittings (02 short, 08 longer) plus any ck175 rulings.

## Ordering

- **01 → 02, strictly.** 02 is a kill gate: nothing builds on the core until the game has shown the four premises
  (no taint · `ConsoleEnabled` route · console tap · clipboard) hold. If 02 KILLS, 99 runs in its reduced form.
- **After a 02 PASS:** 03, 03b, 04, 05 and 06 are independent (disjoint files, see the layout below; the core is
  01's and frozen unless a link routes a change back through this README) — any order, or in parallel sessions.
- **07 after 03–06** (it documents the final button set and writes 08's script). **08 after 07. 99 last**, on a
  folder holding only 99 + this README.

## File layout (TestKit, `C:\Dev\SMR-BugFixPack-TestKit`) — H-10: a file absent from `metadata.lua`'s `code` list ships absent

| file | owner link | holds |
|---|---|---|
| `Code/70_SMRTK_Core.lua` | 01 | `SMRTK` namespace, `SMRTK.Log` (the ONE logger), `SMRTK.Action` (register), `SMRTK.Bind` (slots), ring buffer (`ConsoleLine` + `OnLuaError`), taint assert, `ConsoleEnabled` arm, LocalStorage state |
| `Code/71_SMRTK_Panel.lua` | 01 | the floating panel: status strip, top row, tab bar, page registry (`SMRTK.Page`), collapse, persistence, hotkey |
| `Code/72_SMRTK_World.lua` | 03 | World page actions |
| `Code/73_SMRTK_Infopanel.lua` | 03b | the infopanel section |
| `Code/74_SMRTK_Agent.lua` | 04 | Agent page: slots UI, pins, triggers, note, screenshot+mark |
| `Code/75_SMRTK_Saves.lua` | 05 | Saves page |
| `Code/76_SMRTK_Kit.lua` | 05 | Kit page |
| `Code/77_SMRTK_Stamper.lua` + `Layouts/` | 06 | capture / stamp |
| `Code/80_AgentSlots.lua` | 04 (template) | **agent-owned**: the slots for the NEXT sitting; rewritten per sitting, never by 03–07 |

## Binding chain rules — every prompt inherits these

1. **Staleness check first.** `git log --oneline -10`, `git pull`, `git status --short`, `ListAgents`, in BOTH repos
   (the pack repo holds the docs; the TestKit repo holds the code and has no remote). Several sessions edit these
   trees; never touch a stranger's unstaged file; commit by explicit pathspec (`git commit -F <msg> -- <paths>`).
2. **Inbox / outbox.** Read `## Notes from upstream` at the bottom of your prompt first. On close-out append your
   outbox to the NEXT prompt's inbox **and** `99_AUDIT_fable.md`'s, strike your row here, `git rm` your own prompt,
   and commit all of it together (PROMPT MAP gate: the folder's row in `prompts/README.md` stays until 99).
3. **Route, do not drop.** Out-of-fence findings get FILED (a bug entry, a fact, a checklist item). Vanilla defects
   found on the way (`EF-098` is one) are dev-report material, never fixed here. Unsure? **STOP AND ASK.**
4. **Self-split at a clean commit boundary** into `NNb_*.md` with a full inbox and its own row here.
5. **Capture drift as evidence** — every mistake you catch goes into 99's inbox.
6. **⛔ NO SYNC WRAPPER, EVER.** Toolkit code never calls `NetSyncEvent`, `NetSyncEvents.*`, `LogCheatUsed`, or
   `def:run()` on any of `EF-098`'s 13 re-entering presets. Gate, run before every commit and quoted in the
   summary with its count: `grep -n "NetSyncEvent\|LogCheatUsed" C:/Dev/SMR-BugFixPack-TestKit/Code/7*_SMRTK*.lua
   C:/Dev/SMR-BugFixPack-TestKit/Code/80_AgentSlots.lua` → **0 lines** (presence side: the same grep on
   `ModTools/Src/Data/CheatDef.lua` returns 13+).
7. **⛔ ONE logger, one tag.** Every action writes exactly one line through `SMRTK.Log`, shaped
   `[SMRTK] SMRTK_<Verb> <k=v ...> t=<GameTime> id=<n>` (object as `Class(handle)`), and flushes (`FlushLogFile`).
   No bare `print` in toolkit code (gate: `grep -n "^\s*print(" <the files>` → 0). `SMRTK_` not `SMR_` — `SMR_` already
   matches the TestKit's own mod id in log lines.
8. **⛔ TAINT ASSERT after every action:** if `AreCheatsUsed()` becomes true, log `SMRTK_TAINT` with the action id
   and show it on the status strip. Never suppress it.
9. **⛔ IDLE = ZERO patched vanilla functions.** The TestKit is loaded during A/B pairs. The toolkit may LISTEN
   (`OnMsg.ConsoleLine`, `OnMsg.OnLuaError`, `OnMsg.GatherGameMetadata`) but may not wrap or replace a vanilla
   function while idle. Any wrap (the `print` tee fallback, watch-a-field, quiet mode) is a **toggle, off by
   default, logged `SMRTK_ARM`/`SMRTK_DISARM`, and uninstalls to the captured original** (the `90_Loggers.lua`
   toggle pattern). Armed things **auto-disarm on save, load and map change** and log each fire.
10. **⛔ Never write `config.BuildingInfopanelCheats`, never depend on `AreCheatsEnabled()`, never touch
    `AccountStorage` (blacklisted anyway; achievement testing stays `EF-094`'s route).** Set `ConsoleEnabled = true`
    directly (not `ConsoleSetEnabled`, which also shows the on-screen log — `EF-097`).
11. **⛔ TestKit only.** Nothing under the pack's `Code/`, `items.lua` or `metadata.lua` changes. No `version` edit
    anywhere. The TestKit is local-only by design and is never uploaded.
12. **Behind a fingerprint, inherit; re-derive only what MOVED.** `EF-095`–`EF-099` are the premises; run
    `python tools/doccheck.py --emit-fingerprint` and read the route you are about to call in the source before
    calling it (`CHAIN_METHOD` §2.3 — route failures sit above correct citations). ⚠️ Two premises are flagged
    unverified in the facts (native `ConsolePrint` → `ConsoleLine`; retail `Platform.cheats`); 01 designs the
    fallback for the first, 02 measures both.
13. **Predictions before every sitting** (`CHAIN_METHOD` §5 D): numbered, with the exact log line expected and a
    3× abort threshold. Sitting scripts are **fenced copy-paste lines, one per line, no placeholders, with a
    first-screen witness per step** (memory: owner-typed markers need copy-paste).
14. **Live todo list, one item per commit-and-verify unit**, marked done the moment it is done.
15. **Green gates before every commit:** `python tools/doccheck.py` GREEN (it parses the TestKit tree and sweeps
    `TEMPORARY`), `python tools/parsecheck.py` on every `.lua` touched, rule 6's grep, rule 7's grep. Pack repo:
    `git commit -F <file> -- <paths>` then push. TestKit repo: commit by pathspec; no remote, no push.
16. **⛔ `Code/` edits only with `Mars.exe` closed** (`tasklist` first, in a separate command).
17. **⛔ Never move a status you did not witness.** Every route is source-derived until a sitting ran it.
18. **Bindings in force:** `H-03` (no portal API from any script), `H-08`, `H-09`, the module-list gate is
    untouched (rule 11). Owner decisions go to `docs/PLAYTEST_CHECKLIST.md` → "Decisions waiting on you"
    (append to **175** or take the next free number AT THAT MOMENT), never only here.
19. **A doccheck WARN goes verbatim into your summary.** STATE.md is byte-capped; measure it (`STATE + STUBS`),
    never quote a stored number.
20. **UI rules.** X classes only (`XDialog`/`XWindow`/`XButton`/`XTextEditor`), built in Lua, no XTemplate preset
    that needs the Mod Editor. Panel hotkey default **Ctrl-Shift-K**; 01 greps `Data/XDef/GameShortcuts.lua` +
    `CommonShortcuts.lua` for a collision and routes a different default to ck175 if found. Six agent slots by
    default. Tabs share ONE footprint; the status strip and top row never scroll; `[_]` collapses to those two rows.

## Derived facts (R-C) — inherited by every link

| fact | measured how | build | re-check (one command) |
|---|---|---|---|
| taint is written only by the 3 `NetSyncEvents` wrappers; leaf bodies are clean | `grep -rn LogCheatUsed ModTools/Src` = 4 hits | 1.1.0 build 24995074 | `grep -rn "LogCheatUsed" "A:/SteamLibrary/steamapps/common/Project Spark/ModTools/Src" \| wc -l` → 4 |
| 13/105 presets re-enter `NetSyncEvent` | Python split on `PlaceObj('CheatDef'` | same | `grep -c "NetSyncEvent" ".../ModTools/Src/Data/CheatDef.lua"` → 13 |
| every name the kit needs is outside `ModEnvBlacklist`; `Cheat` is not a blacklisted prefix | per-name grep on `Mod.lua:1280-1470` + the two prefix handlers | same | `grep -cE "^\s+(SaveGame\|LoadGame\|SetGameSpeed\|CopyToClipboard\|ConsoleEnabled\|PlaceConstructionSite) = true" ".../Mod.lua"` → 0 |
| `DE_Console` is created under an `if`; F9/`cls` unconditional | source read + owner press | same | `grep -n "DE_Console\|DE_ClearScreen" ".../CommonShortcuts.generated.lua"` |
| `PlaceConstructionSite` is the controller's call; completion is two-pass | source read | same | `grep -n "PlaceConstructionSite(" ".../Lua/Construction/Construction.lua"` → 2 hits |

Structural drift check for all five: `python tools/doccheck.py --emit-fingerprint` — **HOLDS ⇒ read nothing**.

## Read path — declared

`docs/agent/STATE.md` (mandatory) · this README · your own link + its inbox · `agent/facts/EF-094.md`–`EF-099.md` ·
`C:\Dev\SMR-BugFixPack-TestKit\Code\00_TestCore.lua` (`SMRTest.Print`, the deferred-verdict pattern, the mod-env
global-creation pattern) · `90_Loggers.lua` (the toggle/uninstall pattern) · `metadata.lua` (the `code` list) ·
`docs/PLAYTEST_CHECKLIST.md` item 175 · `agent/WORKFLOW.md` § "Cheats on playtest saves" and § "Writing in a shared
tree" · `docs/PLAYTEST_HELP.md` § "Console" and § "Cheating without contaminating results". Game source (read-only):
`A:\SteamLibrary\steamapps\common\Project Spark\ModTools\Src` — the files each fact cites, by line.
