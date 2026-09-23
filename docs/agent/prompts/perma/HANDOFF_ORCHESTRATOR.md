# Handoff — session → next session (model-agnostic)

## Must_Read_Header
<!-- RULES -->
Rule: Do not retire, archive, gut, or delete this file without the owner's explicit instruction. [A3: pass]
<!-- /RULES -->

This file carries the loose ends that the owner's list, `docs/PLAYTEST_CHECKLIST.md`, cannot hold —
its entrance gate admits an item only when the next action is the owner's, which is most of why the
rest needs a home. It is a working document, not a session log: when you close something here,
delete its block, and prefer a link to a retelling. Verify every specific against `git log` and the tree; Claude and
Codex sessions both commit here, and Codex is invisible to `ListAgents`.

The owner is the sole retirement authority. Section 2 becoming empty is the trigger for asking once;
on 2026-09-13 the answer was to keep the file.

The gated map is [prompts/README.md](../README.md); a row there beats any pointer here. FR-1 (Linux,
NVIDIA 580, the temporary workaround mod) is not on this handoff: see
[LINUX_DISPATCH.md](LINUX_DISPATCH.md).

## 0 · Start here

### Releases

[release_prompt.md](release_prompt.md) owns a release end to end, and this file holds nothing for it.
Where one stands is in [RELEASE_OUTBOX.md](RELEASE_OUTBOX.md) (`Last released`, `Pending`); another
session may be mid-release, so never commit `metadata.lua` or `items.lua` you did not change. Whether
the site is published is a volatile external value: read the `publish-site.yml` runs before claiming
it. Publishing is the owner's act (`docs/UPLOAD_WORKFLOW.md` §4).

The owner reads nothing back from the log: they paste a line and say "flushed", and you read
`%APPDATA%\Surviving Mars Relaunched\logs\Mars.exe-*.log` (newest) yourself. Saves are reachable at
`saves/game` in this repo (WORKFLOW Layout).

Unless the owner's message names a task, a pasted handoff means orient, summarise and ask. Orient from
the `smr-orientation` skill; `docs/agent/STATE.md` and `docs/PLAYTEST_CHECKLIST.md` are pull-only.

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

## 1 · TestKit loose ends (repo `B:\Dev\SMR\SMR-BugFixPack-TestKit`)

TestKit builds go to Astra unless the owner asks a Claude session directly.

- **SMRTK witnesses owed.** The list, with each prediction, is [tools/SMRTK.md](../../../../tools/SMRTK.md)
  "Still owed": the World leaves from kit `82d4577` (`open_domes` is what makes [C103](../../bugs/C103.md)'s
  control runnable), Quick build on a pipe run and on a dome, and the Verbose button. Record results there.
- **Probe buttons refuse without an agent's stamp — owner deferred 2026-09-18 (*"Don't build it now"*).**
  `run_all` and `run_probe` (`Code/76_SMRTK_Kit.lua:102-119`) call `hygiene()` (`:55-63`), which refuses
  until `probe_preflight` is fed two full 40-character HEADs and a desktop grep's exact output, and any
  load expires it. That is kit code refusing a `RunAll`, which ck184 (2026-09-15, restated in
  `tools/SMRTK.md` "Probe preflight") rules out; the gate was built 2026-09-13 (kit `96c9f1a`) and never
  reconciled. Proposed: keep the stamp, drop the refusal — buttons always enabled, and an unprovisioned
  run marked "not attested" on its verdict rows. Until then the owner's route is `*r SMRTest.RunAll()` at
  the console (`*r` because wave 6's probes yield), and the Kit page's verdict rows read `SMRTest.last`,
  so results show without the log.
- **The Selected section title reads "Tool Kit ? Selected" — owner deferred 2026-09-18.** It is a literal
  `?` in source (`Code/73_SMRTK_Infopanel.lua:440`, `Untranslated("Tool Kit ? Selected")`), not a missing
  font glyph as first reported; most likely a separator lost to an encoding pass. One-character fix.
- **Unrun rows from TestKit `acafc74`.** Arm `SMRTest.Log.DroneDrop` (C98) and play normally. Arm
  `SMRTest.Log.CrewDraft` and deliberately under-supply an expedition (demand a specialisation nobody
  has), then read the rocket's panel; body and discriminators in [EF-104](../../facts/EF-104.md). The
  owner's 2026-09-15 deferral of the crew trace as an errand of its own still stands.
- **Shared-kit improvements (item 83):** a `RunAll` owner filter — `SMRTest.RunAll(kind_filter)` has no
  owner arm, and the cost is the data, not the filter: `owner` is set on 2 of 98 registrations, so
  populating it comes first. The `PACK_ID` half is **done** (`98_EnablePathLeg.lua:54`); what is left
  there is hoisting the literal `"SMR_CommunityFixPack"`, which 4 kit files still hardcode.
- **Stale desk tools in this repo, found 2026-09-16:** `tools/l2_reload_sim.py` crashes on the deleted
  `Fix_LastTransmissionStorage.lua`, and `tools/l8_hostile_input.py` loads deleted modules. For the
  hostile-globals rows, use `tools/desk_ck53_hostile_globals.py` instead. `tools/l6_reachability.py`
  needs `PYTHONIOENCODING=utf-8` on this console. ⚠️ ck204's catalog ([tools/README.md](../../../../tools/README.md))
  now lists all three among its 65 rows with no health column, so it presents them as available.

## 2 · What is open

The owner's queue is `docs/PLAYTEST_CHECKLIST.md`: read the item itself.
Never keep an owner list here, and never rebuild an owed list from an older document.

### Agent work

- **Game 1.1.1 is answered in code and playtested; the release is prepared and not fired.**
  Three rebases and sixteen retirements shipped as `45578d4`, audited on a second vendor
  (`e3a1613`), then playtested through phase 3 by the owner. Next action: fire
  [release_prompt.md](release_prompt.md) on a fresh seat; it reads the batch from
  [RELEASE_OUTBOX.md](RELEASE_OUTBOX.md) `Pending`, which carries the retirement list, the
  owner's change-note framing (lead with the vendor, not the subtraction), the ranch
  known-issue wording, and the trap that the player-facing count maps to
  `content/fix-list.md` rows **by meaning** and is re-derived, never computed. Retail
  evidence and everything deliberately not run are in
  [PLAYTEST_PLAN_1.1.1_2026-09-23.md](../../reports/PLAYTEST_PLAN_1.1.1_2026-09-23.md);
  its "Parked" section is owner-ruled low risk and **not agent-tracked**. Delete this
  block once the release closes.
- **One filing decision is open from that work.** The `Fix_OpenPastureStockpiles` removal
  residue is homed in [C93](../../bugs/C93.md) and carried to players in the outbox, but
  has no entry of its own, so it is not findable as a live defect from the bug index. The
  owner ruled it documented rather than fixed; whether it also earns an `F` id is unasked.
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
- **Wildfire cure, awaiting a check (2026-09-18).** The owner fired the one-off
  `WILDFIRE_CURE_INVESTIGATION_high.md` in another session; it landed as [C108](../../bugs/C108.md)
  and removed itself. The owner will bring the orchestrator back to check its result. Check it at surface level: the entry's
  control, the reach tier, and, if it built, a harness that FAILs the unfixed body in cold-boot order
  ([EF-109](../../facts/EF-109.md)). Delete this block once checked.
- **Drone "minimum safety state", owner deciding 2026-09-20.** The source read, the `rfSuspended`
  lever, what it cannot stop and the cheaper alternatives are in
  [DRONE_TASK_LEVERS.md](../../reports/DRONE_TASK_LEVERS.md). Nothing is built, and the owner stopped
  it on cost; they will say what they need to observe. Do not build from that report without their word.
- **Site report form, live since 2026-09-19.** Reports now go to `SMR-CommunityMods` issues through a
  Cloudflare Worker. The route, the secrets and the token renewal are in
  [REPORT_FORM.md](../../reports/REPORT_FORM.md); the owner's browser test is ck205. Nobody has asked for
  it yet, but this repo's `README.md` and `FIELD_REPORT_REPLIES.md` still send people to the old
  `SMR-CommunityFixPack/issues`.
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
  A vacuous control looks like success and never triggers that escalation, so a builder's re-verify
  must revert the guard in a scratch copy and require the leg to FAIL.
- Never implement and judge your own brief (owner, 2026-09-13: *"I would rather you not be the
  implementor and judge"*). Analyse, write the brief with a definition of done per phase, and
  adjudicate the output against the diff, not the report. A build that needs extending goes back to
  its builder as a brief. An explicit owner ask to build wins: build it, say in one line that it
  departs, and mark the builder's brief held.
- Before scoping a redesign of a surface reported as broadly wrong, look for a single render or
  registration fault. On 2026-09-14 one unresolved TextStyle blanked every button caption in the toolkit.
  A verdict on rendered output is worthless unless the log proves which code rendered it.
- When you refute a claim, state what the refutation depends on. The C90/C89 "everlasting flag"
  refutation holds only while no module is `optional`.
- A game label is not a diagnosis. On 2026-09-16 "Blocking objects" covered three unrelated passage
  refusals, and the tinted tree was a bystander (C103). Read the refusal reason, and check a cursor-based
  console read against the on-screen label before trusting it.
- Brief cross-vendor work as numbered falsifiable claims, disagreements first: a short FIXED list
  (owner requirements, safety rails) and everything else DEFAULT, so a builder may depart from a
  default with a stated reason and must report DEPARTURES and SUGGESTIONS. Judge on evidence, not
  conformance, and never put the same vendor on both sides of a check.
- In design work, do not fire a forced-choice widget mid-conversation; give findings and a
  recommendation, then end with a plain prose question, saving AskUserQuestion for a genuine fork
  once the owner is ready to choose. List tools or features by seat — tester vs agent — and mark
  cost honestly.
- After heavy investigation or design work, QA it in a fresh-session one-off prompt, not inside the
  session that produced it — accumulated context builds confirmation pressure. State each claim with
  its evidence and status (proven-live / static-only / disproved), and tell the reviewer not to trust
  the summary.
- A handoff or prompt doc pasted with no further instruction means orient, summarise where things
  stand, and ask which item to take — never execute or commit its work items, even one the doc names
  as first. The owner has stopped mid-work for this: *"just supposed to be an orientation."*
- Before carrying a shipped fix's leftover play clause as owed, ask whether its failure would be
  loud and visible to players and how long it has shipped silently; if so, propose closing it by
  field evidence — *"unless it poses a real risk."* Quiet failures (silent mis-scoring, corruption
  without a throw) do not qualify.
- Owner-pasted example code pictures intent, not a draft — *"I generally do not write it carefully
  or cleanly"* — so judge whether the approach works and flag a defect only when it changes the
  design or outcome, never typos, spacing, naming or harmless redundancy. Lead a load-bearing
  correction with what it changes, not its line.
- Public surfaces are not equal reach: the owner ranks Steam's store page far above Paradox's, and
  both far above this repo's site or README — *"most people just subscribe to a mod, they rarely do
  deep reading for a game mod."* Price a public-surface fix by that reach before recommending
  urgency; the exception is the two Paradox developers, who read the repo, so a `file:line` citation
  to them earns accuracy on its own.
- Do not price an ordinary post-release change against the project's one-time pre-release
  verification cost — that cost is the release gate amortised across launch, and reciting it inflates
  a cheap change. Post-release is patch-note-driven maintenance: read the notes, adjust what a patch
  invalidates, add fixes for new bugs; reserve multi-day tests and sweep chains for a major overhaul.
- Never re-measure context economics here; the sister Subathon Timer repo already did, folded into
  `CLAUDE.md`'s header rules. This repo's own plan is `.claude/BLUEPRINT.md` — read it, never the
  sister tree — and `/clear` is for consulting work only, never for work that creates rails.
- When a state doc's byte cap warns repeatedly, check whether the file is growing or being suppressed
  by plotting size across commits; a flat line pinned at the cap means the cap is too small. Raise the
  warn, never the hard backstop, size headroom in lines at the file's own density, and let the owner
  pick the number; never quote a stored byte figure, re-derive it.
- Consume another seat's gate signal but never republish its state: *"the gate I was blocked on is
  clear"* is mine to say; another chain's sha, verdict, title, sequence or status summary is not,
  however brief — the standing `git log` anchor is how that leak happens. Before writing a status
  line, ask whether it is this seat's lane or a sign for someone else's chain.

## 4 · Traps that have each cost this project a real error

Numbering keeps its old gaps so a citation of "trap 5" still resolves. The shared-tree rules (recheck before
writing, commit with a pathspec, attribute by sha and diff) are header rules in `CLAUDE.md`. Trap 11 is gone: the checklist's own
format gate now fails a stray heading. Trap 12 is gone too: the `STILL OPEN:` parser it guarded retired
with the WAITING register on 2026-09-16 (`tools/doccheck.py:480-486`), so its check,
`doccheck | grep WAITING:`, prints nothing on any tree. `docs/agent/STATE.md`'s open-decisions lines still
name that register and are owed a substitution under [STATE_EVICTION.md](STATE_EVICTION.md).

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

## 5 · Where things live that the maps do not say

- `EF-###` ids are allocated by this repo for both this pack and the opt-in mod (ck167, ck86).
- The opt-in mod's own decisions live in `B:\Dev\SMR\SMR-OptInPack\docs\DECISIONS_OWED.md` (moved 2026-09-12).
