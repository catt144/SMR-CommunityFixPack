# smrtk — the chain manifest (SMR Tool Kit)

Effort: replace the game's built-in cheat menu, for playtesting, with an **SMR Tool Kit panel** that lives in the
TestKit mod: every useful cheat action called through its **leaf body** (no `CheatsUsed` taint, `EF-095`), every
action logged under one **`SMRTK_`** tag so an agent reading a log never has to ask, a **slot engine** an agent can
pre-load before a sitting, **triggers** (breakpoints for a game), **save/load slots**, a **console tap + clipboard
copy**, the **TestKit on buttons**, and a **layout stamper** built on the game's own construction front door
(`EF-099`). Authored 2026-09-13 by `smr-bugfixpack-8f` (Fable) with the owner, in one design conversation;
**reshaped the same day at the owner's direction** into a cross-vendor build/judge pair (03A Codex fan-out,
03B Claude judge). Method: `agent/reports/CHAIN_METHOD.md` (shape D, kill-gated build; §5a fan-out for a fixed
contract). Authoring mechanics: `agent/WORKFLOW.md` "Authoring a prompt" elements 1–9. Owner decisions: checklist **175**.

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
>
> ⚖️ **SHAPE (owner, 2026-09-13):** *"3A and 3B … cross platform this as a primary / secondary with B being a judge
> of the work done. Codex does A and Claude does B."* — the five page builds are one fan-out link whose coordinator
> first settles the shared UI-hook techniques, and a cross-vendor judge sits between the build and the docs. Then:
> *"nearly all the work is being done by claude which makes our cross vendor checks weak … flip it to codex doing
> most of the build"* — **every build link is Codex, every check is Claude.**

## The queue

| # | file | model | owner needed? | what it drains |
|---|---|---|---|---|
| 01 | `01_SKELETON_BUILD_codex.md` | **Codex / Astra** | no | job 0 re-validates this Claude-authored cut (a cross-vendor read of the plan); core (slot engine, logger, ring buffer, taint assert, `ConsoleEnabled` arm), the panel frame (status strip, top row, tabs), MARK / Copy / Flush / cls / eligibility; predictions + 02's script |
| 02 | `02_SKELETON_SITTING_owner.md` | Claude attending (attended) | ✅ keyboard, ~20–30 min | ⛔ KILL GATE: no taint after a leaf action, console hotkey with the Mod Manager CLOSED, the console tap sees prints, clipboard copy pastes, panel survives a load |
| 03A | `03A_PAGES_FANOUT_codex.md` | **Codex / Astra** (top tier on P5) | no | the spike (shared UI-hook techniques, once), then the five payloads below as parallel subagents; gates per result; commit per file; a numbered-claims report |
| 03B | `03B_JUDGE_claude.md` | **Claude** (Opus) | no | re-runs every gate, samples routes against the facts, checks the shared techniques were shared, enumerates idle patches, consolidates every owner item into ONE ck175 append; PASS / PASS WITH FIXES / RE-FIRE |
| 07 | `07_DOCS_AND_SITTING_PREP_codex.md` | **Codex / Astra** | no | WORKFLOW + PLAYTEST_HELP + TestKit README; `perma/SMRTK_SLOTS.md` (how an agent pre-loads a sitting); predictions + 08's script |
| 08 | `08_FULL_SITTING_owner.md` | Claude attending (attended) | ✅ keyboard, 07 prices it | the full attended leg: every page, every button class, a stamp, a save/load round trip, a trigger firing |
| 99 | `99_AUDIT_fable.md` | Fable | ✅ raises | terminal adversarial audit: the taint invariant re-derived against the ARCHIVED log, every action's route read for `NetSyncEvent`/`LogCheatUsed`, tag coverage, idle invariant, the 03A/03B cross-vendor split adjudicated, falsifiers RED, verdict, folder-empty gate, kickoff lines |

### 03A's payloads (`payloads/`, consumed by 03A on its close-out)

| payload | file | holds |
|---|---|---|
| P1 | `P1_WORLD.md` | `72_SMRTK_World.lua`: disasters (cursor-targeted, leaf calls) + stop, quiet mode, speed / ultra / run-until, fix all / malfunction all, finish-waits, spawn / funding / research re-exposures, trait submenu |
| P2 | `P2_INFOPANEL.md` | `73_SMRTK_Infopanel.lua`: the per-object section (Fill, Empty, Delete, Destroy, CleanAndFix, Malfunction, AddPrefab, Spawn*, Upgrade1–6, Dump, Pin) on the spike's injection route |
| P3 | `P3_AGENT.md` | `74_SMRTK_Agent.lua` + `80_AgentSlots.lua`: `SMRTK.Bind`, fire-once vs armed, click-to-target (spike route), auto-disarm, fire counters, pins A/B/C, triggers, note field, screenshot+mark |
| P4 | `P4_SAVES_KIT.md` | `75_SMRTK_Saves.lua` + `76_SMRTK_Kit.lua`: slots A/B/C with the session-id guard, provenance; RunAll / run-one-probe, logger toggles, log tail, error counter, fingerprint, dump, snapshot + diff, watch-a-field, force-open console |
| P5 | `P5_STAMPER.md` | `77_SMRTK_Stamper.lua` + `Layouts/`: the format contract, capture → clipboard, ordered replay, fit check, grids, then state |

Model placement — **Codex builds, Claude judges** (owner, 2026-09-13: *"if claude is going to do most of the build
codex should do that audit or flip it to codex doing most of the build"* — flipped). Every build link (01, 03A, 07)
is Codex / Astra, with Codex's top tier on P5 (the capture format is a contract every future layout depends on);
every check (03B, 99) is Claude, Fable on 99; the two sittings are attended by Claude so the non-building vendor
scores the builder's predictions. 01 inherits the contract from this README and `EF-095`–`EF-099`, and **its job 0
re-validates a Claude-authored cut** — the first cross-vendor check happens before any code exists — with authority
to rewrite any unconsumed link (route a disagreement to ck175 rather than absorb it). The judge pair is standing, not
conditional: 03A is the chain's largest code drop, and without 03B the first check of it would be 99 — after 07 has
documented it and after the owner's sitting.

**Owner time:** two attended sittings (02 short, 08 longer) plus any ck175 rulings — 03B delivers those as one append.

## Ordering

**01 → 02 → 03A → 03B → 07 → 08 → 99, strictly.** 02 is a kill gate: nothing builds on the core until the game has
shown the four premises (no taint · `ConsoleEnabled` route · console tap · clipboard) hold; if 02 KILLS, 99 runs its
reduced form. Inside 03A the five payloads are parallel by construction (disjoint files, a frozen core API,
cross-references by registry id with stubs). 03B may send a payload back to 03A (RE-FIRE) — that loop closes before 07.

## File layout (TestKit, `C:\Dev\SMR-BugFixPack-TestKit`) — H-10: a file absent from `metadata.lua`'s `code` list ships absent

| file | owner | holds |
|---|---|---|
| `Code/70_SMRTK_Core.lua` | 01 | `SMRTK` namespace, `SMRTK.Log` (the ONE logger), `SMRTK.Action` (register), `SMRTK.Bind` (slots), ring buffer (`ConsoleLine` + `OnLuaError`), taint assert, `ConsoleEnabled` arm, LocalStorage state |
| `Code/71_SMRTK_Panel.lua` | 01 | the floating panel: status strip, top row, tab bar, page registry (`SMRTK.Page`), collapse, persistence, hotkey |
| `Code/72_SMRTK_World.lua` | P1 | World page actions |
| `Code/73_SMRTK_Infopanel.lua` | P2 | the infopanel section |
| `Code/74_SMRTK_Agent.lua` | P3 | Agent page: slots UI, pins, triggers, note, screenshot+mark |
| `Code/75_SMRTK_Saves.lua` · `76_SMRTK_Kit.lua` | P4 | Saves page · Kit page |
| `Code/77_SMRTK_Stamper.lua` + `Layouts/` | P5 | capture / stamp |
| `Code/80_AgentSlots.lua` | P3 (template) | **agent-owned**: the slots for the NEXT sitting; rewritten per sitting, never by a build link |
| `reports/SMRTK_UI_HOOKS.md` | 03A spike | the two shared UI-hook decisions, with rejected routes and line numbers |

## Binding chain rules — every prompt and payload inherits these

1. **Staleness check first.** `git log --oneline -10`, `git pull`, `git status --short`, `ListAgents`, in BOTH repos
   (the pack repo holds the docs; the TestKit repo holds the code and has no remote). Several sessions edit these
   trees; Codex is invisible to `ListAgents`; never touch a stranger's unstaged file; commit by explicit pathspec
   (`git commit -F <msg> -- <paths>`).
2. **Inbox / outbox.** Read `## Notes from upstream` at the bottom of your prompt first. On close-out append your
   outbox to the NEXT prompt's inbox **and** `99_AUDIT_fable.md`'s, strike your row here, `git rm` your own prompt,
   and commit all of it together (PROMPT MAP gate: the folder's row in `prompts/README.md` stays until 99).
3. **Route, do not drop.** Out-of-fence findings get FILED (a bug entry, a fact, a checklist item). Vanilla defects
   found on the way (`EF-098` is one) are dev-report material, never fixed here. Unsure? **STOP AND ASK.**
4. **Self-split at a clean commit boundary** into `NNb_*.md` with a full inbox and its own row here (links only —
   a payload that outgrows its budget reports the split point and stops; 03A re-fires the remainder as a payload).
5. **Capture drift as evidence** — every mistake you catch goes into 99's inbox (payloads: into your report's DRIFT).
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
   function while idle. Any wrap (the `print` tee fallback, watch-a-field, quiet mode, click capture) is a **toggle,
   off by default, logged `SMRTK_ARM`/`SMRTK_DISARM`, and uninstalls to the captured original** (the `90_Loggers.lua`
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
    (append to **175** or take the next free number AT THAT MOMENT), never only here — **03B consolidates the
    payloads' items into one append; a payload writes OWNER-ROUTED in its report and nothing to the checklist.**
19. **A doccheck WARN goes verbatim into your summary.** STATE.md is byte-capped; measure it (`STATE + STUBS`),
    never quote a stored number.
20. **UI rules.** X classes only (`XDialog`/`XWindow`/`XButton`/`XTextEditor`), built in Lua, no XTemplate preset
    that needs the Mod Editor. Panel hotkey default **Ctrl-Shift-K**; 01 greps `Data/XDef/GameShortcuts.lua` +
    `CommonShortcuts.lua` for a collision and routes a different default to ck175 if found. Six agent slots by
    default. Tabs share ONE footprint; the status strip and top row never scroll; `[_]` collapses to those two rows.
    **The two shared UI-hook techniques are decided once, by 03A's spike** (`reports/SMRTK_UI_HOOKS.md`); P2 and P3
    build on that decision or its declared fallback, never a third route.
21. **Payloads write, never commit.** A payload (`payloads/P*.md`) parse-checks and greps its own files, then returns
    a **numbered-claims report** (built · verified-how with command output · stopped · OWNER-ROUTED · for-07 · DRIFT);
    the coordinator re-runs the gates and commits per file. A payload never `git rm`s anything; 03A consumes the
    payload files on its own close-out.
22. **Cross-vendor rail.** Codex builds (01, 03A, 07); Claude judges (03B) and audits (99, Fable). Never the same
    vendor on both sides of a check. A report is a claim set: numbered, falsifiable by one command, **disagreements
    first**. A judge may not PASS a payload whose routes it did not open; a builder may not treat a payload's
    self-report as a gate. If the owner re-seats a link, re-seat its check to the other vendor in the same edit.

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

`docs/agent/STATE.md` (mandatory) · this README · your own link (or payload) + its inbox · `agent/facts/EF-094.md`–`EF-099.md` ·
`C:\Dev\SMR-BugFixPack-TestKit\Code\00_TestCore.lua` (`SMRTest.Print`, the deferred-verdict pattern, the mod-env
global-creation pattern) · `90_Loggers.lua` (the toggle/uninstall pattern) · `metadata.lua` (the `code` list) ·
`docs/PLAYTEST_CHECKLIST.md` item 175 · `agent/WORKFLOW.md` § "Cheats on playtest saves" and § "Writing in a shared
tree" · `docs/PLAYTEST_HELP.md` § "Console" and § "Cheating without contaminating results" · from 03A on,
`reports/SMRTK_UI_HOOKS.md`. Game source (read-only): `A:\SteamLibrary\steamapps\common\Project Spark\ModTools\Src` —
the files each fact cites, by line.
