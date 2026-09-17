# Handoff — session → next session (model-agnostic)

## Must_Read_Header
<!-- RULES -->
Rule: Do not retire, archive, gut, or delete this file without the owner's explicit instruction. [A3: pass]
<!-- /RULES -->

This file carries the loose ends that the generated owner queue, `docs/WAITING_ON_YOU.md`, cannot
hold. It is a working document, not a session log: when you close something here, delete its block,
and prefer a link to a retelling. Verify every specific against `git log` and the tree; Claude and
Codex sessions both commit here, and Codex is invisible to `ListAgents`.

The owner is the sole retirement authority. Section 2 becoming empty is the trigger for asking once;
on 2026-09-13 the answer was to keep the file.

The gated map is [prompts/README.md](../README.md); a row there beats any pointer here. FR-1 (Linux,
NVIDIA 580, the temporary workaround mod) is not on this handoff: see
[LINUX_DISPATCH.md](LINUX_DISPATCH.md).

## 0 · Start here

### C95 is cleared; the release is next

2026-09-17: the owner watched the three legs and granted `tested-attended`, and waived the train
return and the live C102 reroute. The release runs from [release_prompt.md](release_prompt.md) on the
Pending entry in [RELEASE_OUTBOX.md](RELEASE_OUTBOX.md), which carries the owner's asks: C95 is the
featured fix with its one gotcha, and the 21-line fix list gets a truth pass plus about six cuts to
make room.

The owner reads nothing back from the log: they paste a line and say "flushed", and you read
`%APPDATA%\Surviving Mars Relaunched\logs\Mars.exe-*.log` (newest) yourself. Saves are reachable at
`saves/game` in this repo (WORKFLOW Layout).

Unless the owner's message names a task, a pasted handoff means orient, summarise and ask. Orient from
the `smr-orientation` skill; `docs/agent/STATE.md` and `docs/WAITING_ON_YOU.md` are pull-only.

### Fixture helpers

Grant exactly 20 tech points without researching anything (each pass pays the current price):

```
*r for i=1,20 do UIPlayer:AddResearchPoints(UIPlayer.TechPointCost) end print(UIPlayer.TechPoints)
```

`Player:CanResearch` returns `nil` for a player with no tech points, even on an `enabled` tech
(`Lua/TechTree.lua:868-874`): grant first, or a healthy node reads as a defect.

List anything outside the Main tree that is already revealed. A lone `Breakthroughs Breakthroughs
locked` row is the inert group placeholder (`Data/Tech.lua:516-525`), not a reveal:

```
*r for id,t in pairs(Techs) do if TechGroupToSection(t.group) ~= "Main" and GetTechState(id, UIPlayer) ~= "hidden" then print(id, t.group, GetTechState(id, UIPlayer)) end end
```

To open the domes for real, use the game's cheat, not SMRTK's leaf (see §1):
`*r Presets.CheatDef.Terraforming.OpenAllDomes:run()`. It sets terraforming to 100% and enacts Open
Domes, which cannot be undone cleanly, so use a scratch copy. It skips the law under the No Politics
rule. That line has not been run, although its route through the preset was read.

## 1 · TestKit loose ends (repo `C:\Dev\SMR-BugFixPack-TestKit`)

TestKit builds go to Astra unless the owner asks a Claude session directly.

- **`Fill all storages` aborts on the first rocket.** Owner, 2026-09-16: note it, do not fix it now.
  `fill_storages` (`Code/72_SMRTK_World.lua:311-316`) sweeps `MechanizedDepot` and `StorageDepot`, and
  every rocket is a `StorageDepot` (`Lua/Buildings/StorageDepot.lua:329-330`). The rocket's `CheatFill`
  throws at `Lua/UniversalRocket.lua:1621` when a cargo line has no demand request, and there is no
  per-object `pcall`, so the remaining depots are never filled (measured live, `SMRTK_ERROR ...
  action=fill_storages`). Fix: exclude rockets and wrap the per-object call. The vanilla `CheatFill`
  throw is cheat-only, so it fails the reach test and has no entry.
- **`Open all domes` only makes the glass transparent** (noted 2026-09-17, not fixed, no owner ruling).
  The leaf (`Code/72_SMRTK_World.lua:383`) calls the Lua `OpenAllDomes()` (`Lua/Buildings/Dome.lua:4034`).
  That is the view passage and demolish modes use, and the domes close again. The owner's test showed
  exactly that. The game's own cheat of the same name (`Data/CheatDef.lua:1036-1052`) is what actually
  opens the domes. Either call the cheat or rename the leaf; recorded also in [C103](../../bugs/C103.md).
- **Unrun rows from TestKit `acafc74`.** Each needs a witness in play; any ordinary colony will do.
  Arm `SMRTest.Log.DroneDrop` (C98) and play normally. Press the Selected-page **Quick build** leaf on a
  construction site. Its design reasoning, including why it calls `site:Complete("quick_build")` and not
  `CheatDeliverResources`, is in the leaf's comment block in `73_SMRTK_Infopanel.lua`. Arm
  `SMRTest.Log.CrewDraft` and deliberately under-supply an expedition (demand a specialisation nobody
  has), then read the rocket's panel. The body and discriminators are in [EF-104](../../facts/EF-104.md).
  The owner's 2026-09-15 deferral of the crew trace as an errand of its own still stands.
- **Owner's third ask, 2026-09-16 — not started, not investigated** (*"Don't investigate it now just
  add it as a note to do in the future"*). (1) A leaf that grants N tech points, built on the route
  above: `AddResearchPoints` is bound on the player (`Lua/TechTree.lua:727-733`), and converts at the
  current `TechPointCost` in a loop (`:692-706`), so the cost curve is honoured. The first point costs
  1000 research, rising about 10% every 4 (`:684-690`). (2) A breakthroughs picker: no design work is
  done or authorised; scope it with the owner first.
- **Shared-kit improvements (item 83):** a `RunAll` owner filter and a `PACK_ID` on the enable-path leg.
- **Stale desk tools in this repo, found 2026-09-16:** `tools/l2_reload_sim.py` crashes on the deleted
  `Fix_LastTransmissionStorage.lua`, and `tools/l8_hostile_input.py` loads deleted modules. For the
  hostile-globals rows, use `tools/desk_ck53_hostile_globals.py` instead. `tools/l6_reachability.py`
  needs `PYTHONIOENCODING=utf-8` on this console.

## 2 · What is open

The owner's queue is generated: read `docs/WAITING_ON_YOU.md`, then the checklist item it links to.
Never keep an owner list here, and never rebuild an owed list from an older document.

### Agent work

- **[C97](../../bugs/C97.md) carries ten known errors, not corrected.** They are preserved with
  citations in [C97_RECHECK.md](../../reports/C97_RECHECK.md). Do not write a fix or a control recipe from
  C97 until that report is applied; four of the ten propagate, including a code fence attributed to the
  wrong function with an inverted truth condition. It is a bounded desk job, and the report is the work list.
- **Field reports open and not reproduced:** [C98](../../bugs/C98.md) (drone drop; the `DroneDrop`
  probe above settles it), [C99](../../bugs/C99.md) (a hub passage cannot be dismantled; it links C42's
  stale-container mechanism to a field symptom; the route is source plus a TestKit container read, never
  the reporter's save), and [C103](../../bugs/C103.md) (Open Domes stops passages on dome tree hexes).
  C103 was filed 2026-09-17 on the owner's word to look later; its unrun control is in the entry.
- **Migration residuals, in the entries:** F51 partial, with its leg unrun · F53 partial, no fresh
  1.1.0 evidence · F59's expedition half untested · F73 partial, organic benefit unverified · F80
  `investigating`, causation unproved · F54 never swept.
- **Hotfix 3 is item 135 only:** the `luafn.py` body-delimiter fix for one-line functions. It is a
  desk tool that changes no shipped hash. `find_bodies` still over-spans a one-line `local function`.
- **`treediff` should grow a `TABLE-HUNK` list** (`HUNT_AUDIT` §8 item 2). Compare content between trees,
  not position: see [PINNED_PARENTS_PASS.md](../../reports/PINNED_PARENTS_PASS.md).
- **Doc overhaul:** three documentation moves stay pending because the fix-authoring destination does
  not exist and no task has had authority to create it. Body in
  [DOC_EDITING_SKILLS_AUDIT.md](../../reports/DOC_EDITING_SKILLS_AUDIT.md) (Deferred moves) and
  `.claude/PENDING_MOVES.md`.
- **Prompts ready to fire** are listed in [prompts/README.md](../README.md). The C92 build's shipping
  hold lives in checklist ck172, and the stand-down audit's class-c blind spot is stated in its brief.

### Watch list, not tasks

- **Foreign Aid Rocket report** (Steam, wgtiii, 2026-09-12): stuck "Unloading cargo" with 2 Food for 40
  sols. Not ours and not filed; the owner messaged the reporter. Lead, so it is not re-derived:
  `LeaveForever` (`RocketForeignAid.lua:75-85`) sets `launch_after_unload = true`, so departure waits for
  the unload, and cargo that cannot be placed strands the rocket; their warnings showed Low Storage.
  If they reply, file it as a lead.
- **C89 reopens only on a countering field report**; its B2 panel leg was not run, by owner ruling.

## 3 · Method with no other home

- Delegate heavy reads and keep the conclusion. Review peers at surface level (`git log --stat`) and
  escalate rather than deep-check; a high-context session carries more hallucination risk than a fresh one.
- A STATE correction substitutes; it never stacks a qualifier beside the wrong line. Its admission test
  is in [STATE_EVICTION.md](STATE_EVICTION.md).
- Chain: Astra fans out and re-verifies its own subagents; the orchestrator sniff-tests; a cross-vendor
  Claude agent runs only if the sniff test fails. Hunts, broad diffs and heavy coordination go to Astra.
- Before scoping a redesign of a surface reported as broadly wrong, look for a single render or
  registration fault. On 2026-09-14 one unresolved TextStyle blanked every button caption in the toolkit.
  A verdict on rendered output is worthless unless the log proves which code rendered it.
- When you refute a claim, state what the refutation depends on. The C90/C89 "everlasting flag"
  refutation holds only while no module is `optional`.
- A game label is not a diagnosis. On 2026-09-16 "Blocking objects" covered three unrelated passage
  refusals, and the tinted tree was a bystander (C103). Read the refusal reason, and check a cursor-based
  console read against the on-screen label before trusting it.

## 4 · Traps that have each cost this project a real error

Numbering keeps its old gaps so a citation of "trap 5" still resolves. The shared-tree rules (recheck before
writing, commit with a pathspec, attribute by sha and diff) are header rules in `CLAUDE.md`. Trap 11 is gone: the checklist's own
format gate now fails a stray heading.

3. **After an upload, the Mod Editor writeback strips every comment from `metadata.lua` and `items.lua`.**
   No session may commit either file until `agent/support/POST_UPLOAD_CLOSE.md` has restored them. Check
   `grep -c '^\s*--' metadata.lua items.lua`; 0 means the restore is owed.
4. **Never state an absence from a truncated grep.** A claim that something is nowhere needs the
   presence side counted.
5. **A grep count is not a finding; check where each hit landed.**
6. **A status flip must hit both the front matter and the body's heading tag**, and a retirement also
   belongs in the title, because `INDEX.md` renders only title and status.
7. **A retirement orphans a promise; a new fix falsifies one.** Grep the public drafts whenever a fix is
   dropped or changes meaning.
8. **Never discard or overwrite a file you did not write without reading it first.**
9. **Bash heredocs eat one backslash level.** Anything carrying a backslash goes through `Write`, using
   the absolute scratchpad path.
10. **One stray NUL makes a doc binary, and `rg` skips binary files by default.** Detect with `file <p>`;
    repair by transcribing the byte as `\x00` and disclosing it beside the block.
12. **`STATE.md`'s `STILL OPEN:` line is parsed, and doccheck stays GREEN when it misparses.** A `(`
    ends the capture and drops every later id. Any bare 2–3 digit number followed by a lowercase word
    counts as owed, so an all-clear must read `none` with no digits. Check `doccheck | grep WAITING:`
    before and after any STATE edit.

## 5 · Where things live that the maps do not say

- `EF-###` ids are allocated by this repo for both this pack and the opt-in mod (ck167, ck86).
- The opt-in mod's own decisions live in `C:\Dev\SMR-OptInPack\docs\DECISIONS_OWED.md` (moved 2026-09-12).
