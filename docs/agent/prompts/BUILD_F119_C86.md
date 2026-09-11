# Build F119 (TODAY) + C86 — one-off build brief (model-agnostic)

Written 2026-09-11 by `smr-bugfixpack-0d` at the owner's ask. **Staleness anchor: `5aff54f`** — verify every specific
below against `git log` and the tree; the records win.

⏱ **The owner wants F119 out TODAY.** It is game-breaking: a permanent Wildfire mystery soft-lock, two players in a day.
**F119 is the critical path.** C86 rides along ONLY if it is built and desk-verified before F119's attended check starts;
otherwise it waits for the next update. Nothing about C86 may delay F119.

**This brief deletes itself:** `git rm` it (and its row in `prompts/README.md`) in the final commit, once F119 is staged
for release.

## 0 · Orient

1. `git pull` · `git log --oneline -15` (compare against `5aff54f`) · `git status --short` · `ListAgents`.
   - Peers at writing time: `smr-bugfixpack-0d` (field diagnostics with the owner; docs only) and `smr-bugfixpack-24`
     (the fixtoggles chain, `prompts/fixtoggles/`). If a fixtoggles commit since `5aff54f` touched `Code/00_Core.lua`
     (Register/Require), read it before writing a module.
   - Codex sessions are invisible to `ListAgents`: a foreign uncommitted file under `Code/` → ask the owner.
2. Read `docs/agent/STATE.md`.
3. **Open a live todo list now** (WORKFLOW "Authoring a prompt" §1): one item per commit-and-verify unit, marked
   complete the moment it completes, exactly one in progress, rewritten when reality diverges. The owner reads it to
   decide when to sit down for the attended check. Suggested items in §5.
4. `tasklist | findstr Mars.exe` — the game must NOT be running before you touch `Code/` (a separate step from the edit).

## 1 · Read path (files, not folders)

- **Entries:** `docs/agent/bugs/F119.md`, `docs/agent/bugs/C86.md`; triage `docs/agent/reports/FIELD_LEADS_2026-09-11.md`
  §1 and §5. Index: `docs/agent/bugs/INDEX.md`, `docs/agent/facts/INDEX.md` — check the facts for rockets / cargo /
  modifiable properties BEFORE deriving an engine claim.
- **Policy:** `docs/agent/FIX_POLICY.md` §1, §2, §2a, §2b, §3a, §4; `docs/agent/WORKFLOW.md` "Per-fix discipline";
  STATE hazards H-02, H-06, H-09, H-10 and "Rules in force" (the post-launch bar).
- **Code templates:** `Code/00_Core.lua` (`SMRFixPack.Register` / `Require`, the probe form);
  `Code/Fix_LanderEmptyLaunch.lua` (a small wrap on `UniversalRocketBase` with the §2b manifest);
  `Code/Fix_ArrivalDeaths.lua` (layer-2 discipline); `items.lua`; `tools/desk_c83_arrivals.py` (desk-harness shape).
- **Game source** — 1.1.0.403908, read-only, `A:\SteamLibrary\steamapps\common\Project Spark\ModTools\Src`:
  - `Lua/UniversalRocket.lua` — `:500-516` (CmdLoad loop), `:535-559` (`IsCargoReady`), `:1891-1920`
    (`GetFuelResourceRequest`, `OnModifiableValueChanged`), `:1937-1951` (`UpdateCargoResourceRequests`), `:2020-2026`
    (`IsSpecialAutomode`), `:2631-2638` (`IsPlayerControlled`).
  - `Lua/CargoTransporterNew.lua` — `:1288-1306` (`GetCargoResourcesStatus`), `:1430-1463` (the request sizing).
  - `Data/FlightPolicyDef.lua:552-600` (the Trade landing branch); `Lua/Exploration.lua:36-45`, `:229-285`;
    `Lua/OrbitalProbe.lua:72-100`, `:161-176`.
  - 1.0.7 archive for the both-trees check: `C:\Dev\SMR-SrcArchive\1.0.7.396349\Src`.

## 2 · Scope fence

- **IN:** a module for F119 (and one for C86 if time allows), their `items.lua` entries, desk harnesses, entry updates, a
  `RELEASE_OUTBOX.md` pending entry per player-facing fix, the attended recipe in the checklist.
- **OUT:** C85 and C87 (diagnostics continue in the owner's session); TradePad / Rival rockets (F119 §Reach, unverified —
  file a finding, do not fix, unless the same predicate covers them with zero extra code AND the desk proves it); the
  upload (owner, `prompts/perma/RELEASE.md`); any `metadata.lua` version field and the Mod Editor (H-02).
- Anything interesting found out of scope → **file an entry, do not fix it.**

## 3 · F119 — the build (critical path)

The design in F119 §Fix sketch is PROPOSED. Re-derive it; do not trust it.

1. **Re-verify every cited line** on 1.1.0 (WORKFLOW per-fix 2). The mechanism in one line: a landed Trade rocket's fuel
   request is sized once (`CargoTransporterNew.lua:1442-1458`); the only re-size on a `FuelResourceAmount` change is gated
   on `self:IsPlayerControlled()` (`UniversalRocket.lua:1916-1920`), which excludes `Trade` (`:2631-2638`).
2. **Count inheritors before wrapping.** Enumerate every class under `UniversalRocketBase` and whether any declares its own
   `OnModifiableValueChanged`. Find where `OnModifiableValueChanged` is dispatched from (the modifiable-property machinery),
   so you know the wrap is reached for a Trade rocket. The pack wraps CLASSDEFS before the class builder (F106/F107): the
   method must be declared on the class you wrap, or `prev` is nil — confirm `Require` catches that.
3. **The wrap (proposed):** post-wrap `UniversalRocketBase:OnModifiableValueChanged`. After `prev`, if
   `prop == "FuelResourceAmount"`, NOT `self:IsPlayerControlled()`, `self.cargo`, and the rocket is landed and loading, call
   `self:UpdateCargoResourceRequests()` — the game's own method, the call the player branch already makes. Choose the
   landed/loading predicate from the source (`IsRocketLanded()`, `self.command == "CmdLoad"`, `self.arrival_loc`) and justify
   each term with a cited line: the narrowest predicate that still reaches every Trade rocket on the pad.
4. **The load-time heal (proposed):** once per load, each landed Trade rocket in `CmdLoad` whose status is not "ready"
   because of fuel gets one `UpdateCargoResourceRequests()`. Show it is a no-op on a healthy rocket (requests already
   equal the live need) and cannot double-grant anything.
5. **§2a guard:** a behaviour probe or a shape `test` — never a version check. The gate is identical on 1.0.7
   (`UniversalRocket.lua:1658-1662 @1.0.7`); 1.0.7 players use the frozen v5 build (ck118). A wrapper that calls the game's
   own method is plausibly branch-neutral — state which guard you chose and why.
6. **§2b manifest:** `-- SRC:` lines from `python tools/bodycheck.py --pin <path> <selector>`, plus `-- DEFECT:` lines.
   **§3a:** layer-2 shape (nothing of ours left in a serialised frame); store nothing in the save.
7. **`items.lua` (H-10):** a module absent from `items.lua` ships absent.
8. **Desk harness `tools/desk_f119_trade_fuel.py`** (shape: `desk_c83_arrivals.py`; lupa shims per the desk-harness
   memory: ipairs/pairs-on-false, Min/Max-on-nil, `table.get`; load shipped bodies under their real file names + line
   offsets). Cases:
   - vanilla, DROP: land a Trade rocket (template 50000), size requests, lower `FuelResourceAmount` by 20000 → expect
     status "unloading" with supply 0 (**the soft-lock reproduced at the desk**);
   - module, DROP: supply 20000 → status reaches "ready" once unloaded;
   - vanilla / module, RISE (+10000): "loading" with demand 0 → module demand 10000;
   - the heal on a pre-stuck rocket; a player rocket: behaviour unchanged.
   Record the PASS count.
9. `python tools/parsecheck.py` · `python tools/bodycheck.py` · `python tools/doccheck.py` GREEN. Commit by pathspec
   (`git add <paths>`, then `git commit -F <file> -- <paths>`), push, verify HEAD == `origin/main` (test `$LASTEXITCODE`,
   never `$?`).
10. **F119 entry:** add a "#### The repair" section with the sha. The status stays `filed` — never reproduced in play, the
    F117/F118 precedent — until the owner's attended check decides.

## 4 · C86 — only if F119 is staged and time remains

- Re-verify `Exploration.lua:229-232`, `:274-275` and `OrbitalProbe.lua:72-100`. Proposed: pre-wrap `MapSector:Scan` so a
  call whose `status` ranks BELOW `self.status` (unexplored < scanned < deep scanned) returns early — vanilla's own early
  return, extended from "equal" to "lower".
- **Grep every caller of `MapSector:Scan`** and prove no legitimate downgrade exists (read the load path at
  `Exploration.lua:36-45`, and any story-bit or cheat caller).
- Same discipline: §2a, §2b, §3a, `items.lua`, desk harness `tools/desk_c86_scan_downgrade.py` (vanilla downgrades; module
  holds "deep scanned"; unexplored→scanned and scanned→deep unchanged), parse/body/doccheck, its own commit.
- If C86 is not desk-verified before F119's attended check starts, **stop C86** and record where it stopped in `C86.md`.

## 5 · Suggested todo items

1 orient + Mars.exe check · 2 F119 re-verify + inheritor count · 3 F119 module + `items.lua` · 4 F119 desk harness PASS ·
5 F119 commit + push · 6 attended recipe in the checklist · 7 RELEASE_OUTBOX entry · (8 C86 re-verify + callers · 9 C86
module · 10 C86 desk PASS + commit) · 11 report to the owner · 12 `git rm` this brief.

## 6 · The attended check (the owner's, today) — write the recipe, don't run it

- The post-launch bar (STATE "Rules in force"): `items.lua` entry + one boot `applied` line + doccheck counts.
- Write the recipe into `docs/PLAYTEST_CHECKLIST.md` as a new item — **read the checklist for the next free number**
  (146 = F119's decision, 147 = field replies, 148 = fixtoggles at writing time). Plain numbered clicks, fenced copy-paste
  console lines, a first-screen witness line per leg, every console line marked `[NEVER RUN]`.
  - **Leg A (the bar):** boot any 1.1.0 colony with the pack; read the `[CommunityFixPack]` `applied` line for the new
    module(s) in the log.
  - **Leg B (the behaviour), if a route exists:** a console route that lands a Trade rocket in an existing 1.1.0 colony
    (candidates: the `SA_CallTradeRocketWithCargo` sequence action; the trade-rocket effect near
    `Data/ClassDef-Effects.lua:210-230`) and changes `FuelResourceAmount` while it waits (e.g.
    `GrantTech("AdvancedMartianEngines")` if not yet researched — otherwise a label modifier). ⛔ Trace the route to shipped
    code and ask "what makes this vacuous?" before handing it over: a colony that already has the tech, a rocket that never
    lands, a staged folder beside a live junction (H-09).
- ⛔ **Stale-probe gate** before the owner boots: `grep -rln "TEMPORARY" Code/ ../SMR-BugFixPack-TestKit/Code/` = zero hits
  (or every hit declared); put the line in the todo list; no result is recorded without it. H-06 if a campaign copy is
  loaded (pre-copy the autosaves).

## 7 · Release staging

- Append a `### Pending` entry to `docs/agent/prompts/perma/RELEASE_OUTBOX.md` per player-facing fix (F119 certainly; C86
  if built): what players see, the count word +1 each, the status. The upload runs through `prompts/perma/RELEASE.md` —
  the owner's action; do not start it.
- **Beta:** the fixtoggles chain (`prompts/fixtoggles/`, ck148) owns any Beta label; the mechanism does not exist yet.
  Mark the outbox entry "Beta candidate (untested in play)" and message `smr-bugfixpack-24`.

## 8 · Stop conditions — report instead of pushing through

- The desk harness cannot reproduce the stuck status with the shipped bodies → F119's mechanism is wrong; stop and report
  what the harness shows.
- A subclass overrides `OnModifiableValueChanged`, or the dispatch never reaches `UniversalRocketBase` for a Trade rocket →
  report before writing.
- The only working fix is a REPLACE of a shipped body → report the trade-off (FIX_POLICY §1).
- A peer has uncommitted changes in `Code/00_Core.lua`, `items.lua` or another file you need → message them / ask the owner.
- Anything would need a version check, the Mod Editor or a `metadata.lua` version edit → stop.

## 9 · What may NOT be claimed

- Not "fixed", "tested" or "works in game": a desk PASS is a desk PASS. After Leg A alone, say "applies cleanly on 1.1.0",
  never "fixes the soft-lock".
- Not that the heal un-sticks real saves — only the desk-simulated one — unless Leg B or a real stuck save showed it.
- Not the TradePad / Rival reach. Counts only from `python tools/doccheck.py --emit-counts`.

## 10 · Finish

- Report to the owner: module names + shas, the desk PASS lines, the checklist item number with the attended recipe, the
  outbox entry, what is left (the attended check, then `RELEASE.md`), and any stop.
- Prepend a `docs/archive/SESSION_LOG.md` entry. `git rm docs/agent/prompts/BUILD_F119_C86.md` and remove its row from
  `docs/agent/prompts/README.md` in the final commit.
