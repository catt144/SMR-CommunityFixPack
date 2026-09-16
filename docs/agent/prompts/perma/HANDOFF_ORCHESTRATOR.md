# Handoff — session → next session (model-agnostic)

## Must_Read_Header
<!-- RULES -->
Rule: Do not retire, archive, gut, or delete this file without the owner's explicit instruction. [A3: pass]
<!-- /RULES -->

> ⭐ **LIVE.** `docs/WAITING_ON_YOU.md` is the owner's generated queue — this file carries the
> **loose ends** it cannot hold.

⛔⛔ **THE 2026-09-15/16 PROMPTS OVERHAUL MOVED OR DELETED FILES THIS DOCUMENT STILL NAMES BELOW.**
Not every citation further down has been rewritten. Translate before following any of them:

| this file says | reality |
|---|---|
| `perma/DISPATCH.md` | **DELETED.** Orient from the `smr-orientation` skill + `STATE.md` + `WAITING_ON_YOU.md` |
| `perma/PUBLIC_SURFACE_SWEEP.md` | **DELETED**, no successor found |
| `perma/RELEASE.md` | → `perma/release_prompt.md` |
| `POST_UPLOAD_CLOSE.md` | → `agent/support/POST_UPLOAD_CLOSE.md` |
| `perma/SITE_AUDIT.md` | → `agent/support/LIVE_SITE_READ.md` |
| `perma/CO_RUNS.md` · `perma/SMRTK_SLOTS.md` | → `agent/support/` |

⛔ **`prompts/README.md` is the gated map and it is the authority** — a row there beats any pointer
in this file. The firing freeze that stood on 2026-09-15 was **LIFTED** on the owner's word (`7d63900`).

## Retirement authority

The owner is the sole retirement authority. Section 2 becoming genuinely empty is the trigger for
asking once; the last answer, on 2026-09-13, was to keep the file because too many loose ends remained.

⛔ **THIS IS A WORKING DOCUMENT, NOT A SESSION LOG.** History lives in `docs/archive/SESSION_LOG.md`.
**If you close something here, DELETE its block** — and prefer a pointer to a retelling: anything the
entry, brief or checklist already holds belongs there, not here.

⛔ **Verify every specific against `git log` and the tree — the records win, this file is a pointer.** Claude
and Codex sessions both commit here, several at once, and **Codex is invisible to `ListAgents`**.

⛔ **FR-1 is NOT on this handoff.** Every Linux / NVIDIA 580 / workaround-mod item is in
`prompts/perma/LINUX_DISPATCH.md`. The temp workaround mod is LIVE (Steam 3799500849 / Paradox 158711).

## 0 · START HERE — this handoff carries TWO tasks that EXECUTE

⭐⭐ **OWNER INSTRUCTION 2026-09-16: §0a then §0b start automatically when this handoff is fired, in
that order and without stopping to ask between them.** They are the deliberate exception to the
orient-and-ask default below, which resumes once both are done.

⛔ **`perma/DISPATCH.md` NO LONGER EXISTS** — the prompts overhaul deleted it 2026-09-15/16. Orient
from the **`smr-orientation` skill** plus `docs/agent/STATE.md` (now a short pull-only status file,
not a mandatory read) and `docs/WAITING_ON_YOU.md`. Bindings live in `CLAUDE.md` and document-local
`Must_Read_Header` blocks. Add `ListAgents` (peers edit this tree concurrently) and open a **live
todo list**.

**After §0a and §0b, the default returns: unless the owner's message names a task, a pasted handoff
means ORIENT — summarise and ASK what to take.** Do not execute anything else.

### 0a · FIRST TASK, auto-start — the C98 drop probe

**Build a log-only wrapper on `Drone:DropCarriedResource` and ride it on the next TestKit link.**
⛔ **The design, the discriminator table and the two desk questions are in
[`bugs/C98.md`](../../bugs/C98.md) § "How to settle this WITHOUT reproducing it" — read it there, it
is not restated here.**

Why it is first: the owner judged the scenario too hard to engineer in a playtest, and a desk audit
**cannot** close it (`GetPassablePointNearby` is a C export). The wrapper needs **no reproduction** —
it fires on every carried-resource drop, so ordinary play yields a population in minutes. TestKit
only, log-only, 0 shipped hashes, **no booked sitting**.

⭐ **Take it with the other two TestKit items rather than as its own errand** — the quick-build row
and the deferred crew-trace slot, both in §2b. One link, three rows.

### 0b · SECOND TASK, auto-start — author the C95 fix prompt, straight after §0a

⭐⭐ **OWNER INSTRUCTION 2026-09-16: go straight into this when §0a is done. Do not stop to ask.**

**Author a fix prompt for [C95](../../bugs/C95.md)** — the Naturalist/MicroG habitat residents who are
drafted for expeditions and never returned home. Use the **`prompt-authoring` skill**; the brief is
the deliverable.

⛔ **AUTHOR THE PROMPT, DO NOT AUTHOR THE FIX.** C95 carries the owner's standing *"do not author
it"*, and **[ck185](../../../PLAYTEST_CHECKLIST.md) is still open** — it asks the owner to say when
to build each of C95/C96. Writing the brief prepares that work; it does not start it, and the brief
itself must carry the hold. ⛔ Nothing ships without the owner lifting it in words.

**What is already settled and must be inherited, not re-derived** (read C95 for the bodies — do not
restate them in the brief):

- ⭐ **REPRODUCED IN PLAY**, owner at the keyboard, 2026-09-15 — this is one of the very few entries
  that is not source-only. Two habitat residents taken, neither returned, both re-homed into a dome;
  one later walked back unaided, proving the habitat was reachable the whole time.
- ⚖️ **The repair shape is the OWNER'S CHOICE and is not open for redesign:** *exclude habitat
  residents from the EXPEDITION draft* — ⛔ **NOT** a widening of the return path.
- ⚖️ Classed an **oversight bug solved by a judgment call** → **main pack, with the mark**,
  ⛔ **not opt-in**.
- ⛔ **SCOPE: expeditions only.** The asteroid lander gathers from a player-chosen passenger list and
  is not an auto-draft.
- ⚠️ **Still unisolated, and the brief must say so:** which gate excluded the habitat — the rail
  sweep or `CanVisit` capacity. A fix written without settling that risks repairing the wrong gate.
- Engine properties behind it: [`EF-103`](../../facts/EF-103.md) (a habitat is a Community, never a
  `Dome`) and [`EF-104`](../../facts/EF-104.md) (expedition crew is drafted colony-wide and boards by
  teleport; ⛔ carries one unexplained draft observation).

⚠️ **`EF-104`'s crew-trace slot (§2b) is the instrument that would settle the gate question** — the
brief should say whether it needs that first, rather than assuming either way.

---

## 1 · Where v10 landed — ⛔ `STATE.md` carries all of it; nothing is re-derived here

✅ **Discharged, and must not reappear on any owed list:** ck158 (the attended gate) · the three retirements
· C90 (`153d180`+`e5f1947`) · the STATE eviction **and** its cap revert to `18 * 1024` (`c820c7f`).
⚠️ **STATE's WARN threshold is TEMPORARILY raised for the doc overhaul (ck178)** — doccheck prints it as
`warn 15360 TEMPORARY`. ⛔ Read the live number from doccheck, never from a document, and do not treat the
headroom as permanent.

---

## 2 · What is open

### 2a · Owner

⛔ **Do NOT maintain an owner list here.** `docs/WAITING_ON_YOU.md` is **generated** from the checklist
markers by `doccheck --regen` and is the only list that can be trusted — a hand-kept copy in this file
went divergent within a day. **Read it, then read the checklist body it links to.**

⚠️ **Two things the generated list cannot tell you, so they stay here:**

- ✅ **144 (a) is DISCHARGED 09-15 (ck184 b/d)** — the RunAll ran under a same-day stamp, the play clauses
  closed by field evidence, A3/A10 struck. ⛔ **Never rebuild it as owed from an older document.**
- **151 (b)** is messaging, and **ck165 lets the owner defer it indefinitely — ⛔ do not raise it.**

⛔ **Never rebuild an "owed" list from an older document** — this file's did exactly that on 09-12 and
contradicted its own closed list for most of a day.

### 2b · The loose ends — this is why the file is still alive

⚠️ **Peers share this tree.** Re-check `git log` + `git status` before every write; a peer commits
here every few minutes.

✅ **EFFORT 1 — `prompts/smrtk/` (ck175), the SMR Tool Kit — CHAIN CLOSED 09-14** (99: SHIP WITH
CHANGES, `reports/SMRTK_AUDIT.md`; `e88bbe7`). ✅ **99's Code link (C-1/3/5/6) LANDED 09-15, TestKit
`f5fa650`**, witnessed 09-15 (`reports/CK144A_CLOSEOUT_SITTING.md`; C-3 refuted, C-5 unwitnessed, both
closed low-priority by the owner). ⚖️ **ck184 + ck183 RULED and CLOSED 09-15; ck144 (a) DISCHARGED.**
⛔ **NOTHING from this effort is owed** — the owner asked for it closed so it stops being raised. The
probe-maintenance names in STATE are instrument health, not this effort's.
- ✅ **STAMPER CUT 09-14, settled.** ⛔ Never re-open or re-cost it; `FUTURE_IDEAS.md` entry 5,
  **not agent-tracked**, ⛔ **no mention in any always-read doc** (owner's instruction, same day).

⭐ **OWNER REQUEST 2026-09-15, NOT SCHEDULED — the quick-build button is missing from Selected.**
Owner's words: *"I am missing the quick build button in the tool menu, that is something I frequently
use, it only build the thing I am focused on via the cheat."* ⚠️ **A new ask, not a reopening of the
closed chain** — take it with the next TestKit link, never as its own errand.
- **The gap, MEASURED.** `73_SMRTK_Infopanel.lua:11-27` lists 15 Selected leaves and **none completes
  a construction**. The colony-wide one exists on World (`72:276`, `complete_constructions` →
  `CheatCompleteAllConstructions`), so the kit has the all-at-once form and not the focused one.
- **The leaf to call:** `ConstructionSite:CheatDeliverResources(skip_group)`
  (`Lua/Buildings/ConstructionSite.lua:2042`) — sets `supplied = true`, zeroes every outstanding
  construction request, calls `StartConstructionPhase()`. ⭐ It delegates to the `ConstructionGroupLeader`
  for a grouped build (`:2043-2048`), so multi-part sites come out right for free.
- **Shape: one row in the `leaves` table.** `method_for` (`73:51-53`) already hides a leaf the object
  does not carry, so it appears only on construction sites. TestKit only, 0 shipped hashes, game closed.

⛔⛔ **OWED 2026-09-16 — [C97](../../bugs/C97.md) carries TEN KNOWN ERRORS and they are NOT corrected.**
An Opus re-check found them; everything is preserved in
[`reports/C97_RECHECK.md`](../../reports/C97_RECHECK.md) with line citations. ⛔ **Do not write a fix
or a control recipe from C97 until that report is applied** — four of the ten propagate, including a
code fence attributed to the wrong function **with an inverted truth condition**. The entry now warns
about itself at the top. ⭐ Applying it is a bounded desk job; the report is the work list.

⭐ **Three defects filed 2026-09-15/16 from field reports, all NOT reproduced:**
[C98](../../bugs/C98.md) (drone drop — §0a's probe settles it), [C99](../../bugs/C99.md) (hub passage
cannot be dismantled — ⭐ **links [C42](../../bugs/C42.md)'s stale-container mechanism to a field
symptom for the first time**), and [C93](../../bugs/C93.md)'s second report, which exposed a
**post-build** `CreateStockpiles` entry point at save load that the entry had never recorded.

✅ **The Wildfire cure investigation LANDED 2026-09-16 — cause found and fix built: `F120`**
(`80c9ebc` filed + reproduced, `d004494` the fix `Code/Fix_WildfireCureMigration.lua`). Legacy
`Research:AddTech` stored `field='Mysteries'`; the tech-point converter preserves only
BuriedWonders/Storybits/Breakthroughs, so a cure revealed before conversion stays hidden. The fix
restores that one entrance on `PostLoadGame`, additively, in a Wildfire colony only.
⛔ **Do not start a second investigation.**

⚠️⚠️ **F120 DOES NOT COVER THE REPORTER'S CASE, by its own header:** *"This does not explain a fresh
Steam colony's missing cure."* Reach is platform-conditional — retail Steam blocks pre-402200 saves,
non-Steam retail offers Load anyway. ⇒ **The original Steam report may still be unexplained.**
⭐ **OWNER SIGNAL 2026-09-15 night: multiple reporters are waiting to see something ship, and the
owner wants a release-worthy outcome soon.** F120 is the candidate; whether it answers the person who
reported it is the open question, and `bugs/F120.md` holds the reporter/evidence distinction. ⚠️ The owner's open question, unanswered: is the cause a **class**
spanning [C69](../../bugs/C69.md) (the dead "In Progress" research state), [C79](../../bugs/C79.md)
(`ChangeResearchCost` ignores its own `points` argument and always boosts 20%) and
[C92](../../bugs/C92.md)? Established and load-bearing: the mystery chain rewiring is **complete**
(5 chained families = 5 remapping entries), and the dead "In Progress" state is used **exactly once**
tree-wide — so mysteries are *not* broadly broken through that seam.

✅ **The 1.0.7-era candidate block is ARCHIVED 2026-09-16** (`481bbd7`, owner ruling): 38 rows to
`docs/archive/bugs/`, candidates 59 → 34, the unprioritised bucket now empty. ⭐ **doccheck's
`seq`/`row` contiguity rule was replaced by gap-accounting** so archiving no longer costs a renumber
of every surviving entry — archived entries keep their numbers and the gate reads them back.
⛔ **Never reuse an archived number**; doccheck goes RED on one claimed by both sides.

⭐ **SECOND TestKit ask, DEFERRED by the owner 2026-09-15 (*"lets save that"*) — a crew-trace slot.**
A log-only wrapper on `CargoTransporter.GatherAvailableColonists`, armed from a slot and restored on
disarm, to settle `EF-104`'s unexplained draft observation (three idle unemployed colonists passed over
while three employed were taken). ⛔ **Design, trigger and the cheaper first step are in `EF-104` — do
not restate them here.** Take it with the same TestKit link as the quick-build row above.

✅ **EFFORT 2 — the doc overhaul (ck176–ck183) — BOTH HALVES LANDED 2026-09-15.** The rules half:
scattered rules became local header blocks plus a kernel list in `CLAUDE.md`, gated by doccheck's
`RULES HEADERS` and `RULE PLACEMENT` (`reports/RULES_HEADERS.md`). The document half: `doc-editing`
(`d716d9f`) and `prompt-authoring` (`7013326`) built, brief and its map row consumed (`d685f86`),
record `reports/DOC_EDITING_SKILLS_AUDIT.md`. ⛔ **Its brief is DELETED — `prompts/DOC_EDITING_SKILLS.md`
no longer exists, so do not follow an older document's pointer to it.**
- ⚠️ **The one loose end it could not discharge:** three documentation moves stay **PENDING** because
  the **fix-authoring destination does not exist and this task had no authority to create it**. ⛔ Body
  in that report's Deferred moves and `.claude/PENDING_MOVES.md` — read it there, it is not retold here.

⭐ **OTHER PROMPTS READY TO FIRE, when neither effort is eating the attention.**
① `prompts/STANDDOWN_AUDIT.md` — no blocker, fire any time; a 21-module sweep, good Codex fan-out.
② `prompts/C92_ACHIEVEMENT_BUILD.md` — build + test, ⛔ **SHIPPING HELD by ck172 until the owner lifts
it in words**. ③ `prompts/DLC_DEEP_CHECK.md` — desk, unclaimed, bounded.
⛔ **ck144 (a) was listed here as owed until 09-15 and is NOT — §2a discharged it.** The line is gone on
purpose; a fourth item citing it is an older copy of this file.

⛔ **The blocks below are POINTERS. The entry, brief or checklist item is the record — read it there.**

- **C92** — ck172 ruled *build it, shipping HELD until the owner lifts it in words*; **ck171 (scope)
  stays OPEN**. Brief `prompts/C92_ACHIEVEMENT_BUILD.md`; evidence closed out. ⛔ **Three claims are
  WITHDRAWN — do not reason from them:** a ≈44% water bonus, a "never-drawn" icon, unremovable residue.
  Seat/prerequisite/art are **design choices to be made**, not intent to be restored.
- **C93** — filed `cand`; Outside Ranch produce stranded at the centre, ⛔ **cause UNRESOLVED and it is
  not ours**. The owner's "outdated mod" reading is leading but unproven — our own 09-09 log shows the
  same fallback in vanilla. Needs the reporter's log line + mod list ⇒ **PULL-ONLY (ck165): the ask is
  the owner's call, nothing is drafted and nothing is owed.**
- **D14 / stand-down** — brief `prompts/STANDDOWN_AUDIT.md` holds it. ⛔ The gap is **not** "did the body
  change" (`bodycheck` answers that at the desk) but its declared **class-c** blind spot: a vendor
  repairs a defect without touching the body we pinned and every instrument reads GREEN.
- **ck173** — `FIX_POLICY` §2a is factually wrong in one half, raised 09-13, **unruled**; body in the
  checklist. Reason 1 survives and is the real rule.
- **Facts filed 09-13/14 — inherit, never re-derive:** `EF-093` · `EF-094` (⛔ no mod and no retail
  console can clear an achievement flag — the console **is** the mod sandbox) · `EF-095`–`EF-099`
  (smrtk premises) · `EF-100`/`EF-101` · `EF-102` (the depot class tree).
  ⛔ **Read the fact, not this line** — `EF-102` was AMENDED 09-14 after its own FIX SHAPE bullet
  caused a failed repair, and this file carried the superseded "two branches" wording for a day.
  Summaries in `facts/INDEX.md`; ⛔ grep it, never read it whole.
- **C91** — open candidate: vanilla leaks the Building Codes maintenance modifier on repeal.
  ⭐ **08b found a read route** (Dump exposes the modifier on a live building) — body in ck183.
- **Migration residuals, in the entries (09-12) — the list nobody would reconstruct:** **F51** PARTIAL,
  leg re-filed **UNRUN** · **F53** PARTIAL, no fresh 1.1.0 evidence · **F59** repaired, **A1 expedition
  half UNTESTED** · **F73** PARTIAL, organic benefit unverified · **F80** `investigating`, causation
  unproved · **F54** never swept.
- **`treediff` gains a `TABLE-HUNK` list** (`HUNT_AUDIT` §8 item 2). ⭐ **Compare CONTENT between trees,
  not POSITION** — the position classifier's failures are in `reports/PINNED_PARENTS_PASS.md`.
- **83 (SHARED TestKit)** — a `RunAll` owner filter and a `PACK_ID` on the enable-path leg improve the
  kit **for us**, regardless of the opt-in mod.
- **Hotfix 3 — 135 only** (ck166): take the `luafn.py` delimiter fix. Desk tool, **0 shipped hashes**.
  ⛔ Do not re-derive the old table or the expired-triage "tension"; both are gone on purpose (ck161).
- ✅ **Closed, do not reopen.** 09-13: `SELFCHECK_PILOT.md` REMOVED on the owner's word (`cf8d51f`) ·
  the C92 placement/icon investigation · the ck170 doc overhaul pass · `GATE_WIRING` (adjudicated PASS).
  09-14: **`CHECKLIST_ARCHIVE.md` FIRED and consumed** (`41116e3`) — the settled backlog moved, ⛔ those
  bodies now live in `docs/archive/PLAYTEST_ARCHIVE.md` behind the `.rgignore`, so a grep that used to
  hit comes back empty · every smrtk link except 99 (listed once in §2b, not restated here).
  ⛔ Never re-run a passed kill gate to "check".

### 2c · Watch list, not tasks

- ⏳ **The Foreign Aid Rocket report** (Steam, wgtiii, 09-12): stuck "Unloading cargo", 2 Food, 40 sols.
  ⛔ **NOT ours and NOT filed** — the owner messaged the reporter and is waiting. F119 cannot touch it
  (that is `FuelResourceAmount` on **trade** rockets). Lead, so it is not re-derived: `LeaveForever`
  (`RocketForeignAid.lua:75-85`) sets `launch_after_unload = true`, so departure is gated on the unload
  finishing and unplaceable cargo strands the rocket; their warnings showed **Low Storage**.
  ⇒ **If they reply, file it as a lead.**
- **Hardening rows 1 + 2 — DEPRIORITISED by ck53, not closed.** A non-table `SMRFixPack_Disabled` either
  passes the `or {}` adoption (`00_Core.lua:13`) so every id reads nil and **the modder's veto is silently
  ignored**, or throws and **kills the whole pack, log-only**. Row 2 is the same shape for
  `SMRFixPack_Optional` (`:17`, read at `:57`). ⚠️ A plain `type(x) == "table"` guard is **not** enough alone.
- **C89 reopens only on a countering field report** — its B2 panel leg was not run, by owner ruling.

---

## 3 · Method — only what has no other home

⛔ **Two of these are WORKFLOW rules, not this file's: read them there, they are canonical and dated.**
**Rule 5b** replies are PULL-ONLY · **rule 5a** a ruling carries the state it was made in — both
numbered in `WORKFLOW.md`; find them by number, never by line. ⚖️ The **VOICE RULE** lives with the text it binds: `reports/still-needed/WORDING_RULED.md` and
`perma/PUBLIC_SURFACE_SWEEP.md`.

What is only here:

- **Delegate heavy reads; keep the conclusion.** Review peers at **SURFACE level** and **escalate rather
  than deep-check** — a high-context session is at *higher* hallucination risk than a fresh one.
  ⚠️ Reading a peer's live files *to describe their work in your own* is deep-checking by another name:
  `git log --stat` is the surface read, and it is usually enough.
- ⚠️ **A STATE correction SUBSTITUTES, it never stacks** — replace the wrong line, do not append a
  qualifier beside it. Kept here because it is the half with no other home: its companion admission test
  (is this fact universal to *every* session?) is a ruled owner decision living in
  `perma/STATE_EVICTION.md` § Hazards admission test, and `EF-102` exists because a fact can fail it.
- **Chain:** Astra fans out → Astra re-verifies its own subagents → orchestrator sniff test → a cross-vendor
  Claude agent **only if the sniff test fails**. Hunts, broad diffs and heavy coordination go to **Astra
  (Codex)**; builds to a Claude session.
- ⭐⭐ **A SURFACE CANNOT BE DESIGN-JUDGED WHILE A RENDER BUG IS LIVE (08b, 09-14).** The owner called
  the toolkit "a mess" and was about to commission a redesign sweep; **one** unresolved TextStyle had
  blanked *every* button caption while every plain label rendered. Three of the "design" complaints
  were that bug, and three more were one shared defect class (a fixed cap that clips once content
  grows). ⇒ **When a surface is reported as broadly wrong, look for a single render/registration
  fault before scoping a redesign** — compare what renders against what does not, and find the one
  code path they differ on. Generalisation: ⛔ **a verdict on rendered output is worthless unless the
  log proves which code rendered it** — the first font verdict here would have been passed on a
  fallback font, and only a log line disappearing showed the real one was on screen.
- ⭐ **When you refute a claim, say what your refutation depends on.** The C90/C89 "everlasting flag"
  refutation holds *only while no module is `optional`* — the `fixtoggles` chain would end that. A
  refutation without its condition is a trap for the next reader. (The general form is rule 5a.)

---

## 4 · Marker rule — homed in WORKFLOW

The mandatory marker-update rule now lives in `agent/WORKFLOW.md` rule 5, beside owner-decision mirroring.
Its regeneration route lives there under "Writing in a shared tree". Read those canonical homes rather
than copying this handoff's retired instructions or recorded counts.

⭐ **Archiving a checklist body that `STATE.md` cites by number is a silent failure, not a tidy-up** —
`docs/archive/` sits behind an `.rgignore`, so a default `rg` would never surface the body again.

---

## 5 · Traps that have each cost this project a real error

✅ **HOMED 2026-09-13, and the duplicate copies are now GONE from here** — the one-git-identity trap, the
pathspec-is-half-a-fence trap and the `--regen-waiting` rule live in `agent/WORKFLOW.md` § "Writing in a
shared tree". Read them there; this list carries only what has no other home. Numbering keeps its old
gaps on purpose, so a citation of "trap 5" still resolves.

3. ⛔ **After an upload, the Mod Editor writeback STRIPS EVERY COMMENT from `metadata.lua` and `items.lua`**
   (v10: 319 → 0 and 51 → 0). ⛔ **No session may commit either file until `POST_UPLOAD_CLOSE.md` has restored
   them** — a commit naming the path takes its working-tree content and buries ~400 lines. Check:
   `grep -c '^\s*--' metadata.lua items.lua`; **0 means the restore is owed**.
4. ⛔ **Never state an absence from a truncated grep.** `| head -5` is not an enumeration. A claim that
   something is *nowhere* needs the presence side counted.
5. ⛔ **A grep COUNT is not a finding — check where each hit LANDED.** On 09-12 a count of retired-fix bullets
   in `STORE_CARD_LIVE.md` looked like two stale paste blocks; the hits were in the changelog prose that
   *documents the removal*. Both paste blocks were correct.
6. ⛔ **A status flip must hit BOTH the front matter and the body's heading tag** — doccheck goes RED on one
   without the other. ⚠️ A retirement also belongs in the **title**, because `INDEX.md` renders title + status
   and nothing else — otherwise the index reads a retired fix as live (the F60 precedent).
7. ⚠️ **A retirement orphans a promise; a new fix falsifies one.** `PUBLIC_SURFACE_SWEEP` §1 only ever taught
   the second direction, so 40 module deletions went unswept and `faq.md` promised a save repair the pack no
   longer did. The check now exists in that file — **use it, and grep the drafts whenever a fix is dropped.**
8. ⛔ **Never discard or overwrite a file you did not write without reading it first.**
9. ⚠️ **Quoted bash heredocs still eat one backslash level** — use the `Write` tool for scripts carrying
   escapes or regexes, and the absolute scratchpad path (`$TMPDIR` is not set in this shell). ⚠️ **Re-triggered
   09-13 by a session that had already read this trap** — the no-op even reported success. Written down is
   not applied: anything with a backslash goes through `Write`.
10. ⛔ **ONE stray NUL makes a doc BINARY and `rg` SKIPS binary files by default** — it looks normal in an
   editor while being invisible to every default search. Hit 09-13: a pasted savegame excerpt hid a whole
   report, build-blocking correction included. Same silent-boundary family as `docs/archive/`'s `.rgignore`.
   Detect `file <p>`; repair by transcribing the byte as `\x00` **and disclosing it beside the block**.
11. ⛔⛔ **AN `##` HEADING IN `PLAYTEST_CHECKLIST.md` CLOSES "Decisions waiting on you" AND ORPHANS EVERY
   ITEM BELOW IT — and doccheck stays GREEN through the whole thing.** Hit 09-14: one H2 appended mid-file
   dropped the section from **134 items to 8** (exactly the items above the insertion point) and silently
   cut 22 lines from `WAITING_ON_YOU.md`. **`WAITING: fresh` only asserts the render matches its source,
   never that the source is intact.** ⇒ **Verify a checklist edit against the ITEM COUNT, not the gate
   colour:** `doccheck | grep WAITING:` and `.claude/tools/archive_settled.py | sed -n 3p` must agree and
   must not fall. A new item is `### <date> — <n>: <title>` + its `<!-- ck:n ... -->` marker, sub-headings
   `####`. ⛔ And **never `git checkout --` the file to recover** — the owner blocked exactly that, which
   would have taken 132 lines of unrelated work back to HEAD.

---

## 6 · Where things live — ⛔ the map is `docs/README.md` and `prompts/README.md`

Only the things those two do not already say:

- ⭐ **`perma/RELEASE.md` SPANS the owner's upload and is finished at §6, not §2** — the close-out is part of
  its job, never a separate errand. A release that stops at "ready to upload" leaves the outbox uncleared and
  `metadata.lua`'s comments stripped (trap 3).
- **`STATE.md` is a kernel: status + pointer, never derivation.** ⇒ **Put closed rulings in the checklist,
  not there.** ⛔ Read its live byte number from `doccheck`, never from a document.
- **Owner decisions go in `docs/PLAYTEST_CHECKLIST.md` → "Decisions waiting on you"**, never only in agent
  docs; `docs/WAITING_ON_YOU.md` is the generated view of them (§2a).
- ⭐ **`EF-###` ids are allocated by THIS repo** for both repos (ck167/86). The opt-in mod's own decisions
  live in **`C:\Dev\SMR-OptInPack\docs\DECISIONS_OWED.md`** (moved 09-12, ck167).
