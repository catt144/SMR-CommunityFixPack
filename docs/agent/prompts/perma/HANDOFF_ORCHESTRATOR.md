# Handoff — session → next session (model-agnostic)

## Must_Read_Header
<!-- RULES -->
Rule: Do not retire, archive, gut, or delete this file without the owner's explicit instruction. [A3: pass]
<!-- /RULES -->

> ⭐ **LIVE.** `DISPATCH.md` is the route table for ad-hoc work and `docs/WAITING_ON_YOU.md` is the
> owner's generated queue — this file carries the **loose ends** those two cannot hold.

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

## 0 · Orient, then ask

⛔ **`perma/DISPATCH.md` §0–§1 is the orientation and the bindings — follow it, it is not repeated here.**
Add `ListAgents` (peers edit this tree concurrently) and open a **live todo list**.

**Unless the owner's message names a task, a pasted handoff means ORIENT: summarise and ASK what to take.**
Do not execute.

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

⭐⭐ **EFFORT 2 — the doc overhaul (ck176–ck183), owner-driven and peer-run.** `prompts/RULES_HEADERS.md`
is its live brief: N scattered rules become local header blocks plus ONE kernel rule. ⛔ **Sequencing
ruled by the owner: SMRTK finishes first, then RULES_HEADERS re-fires** — ✅ **SMRTK is finished**, so
this is the next effort to pick up. ⚠️ Its seat carries the STATE
policy and enforces it — **corrections SUBSTITUTE, they never stack**, and a fact fails STATE's
admission test unless it is universal to *every* session. That is why `EF-102` exists.

⭐ **OTHER PROMPTS READY TO FIRE, when neither effort is eating the attention.**
① `prompts/STANDDOWN_AUDIT.md` — no blocker, fire any time; a 21-module sweep, good Codex fan-out.
② `prompts/C92_ACHIEVEMENT_BUILD.md` — build + test, ⛔ **SHIPPING HELD by ck172 until the owner lifts
it in words**. ③ the owed **ck144 (a)** boot (§2a). ④ `prompts/DLC_DEEP_CHECK.md` — desk, unclaimed,
bounded.

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
**Rule 5b** replies are PULL-ONLY (`WORKFLOW.md:76`) · **rule 5a** a ruling carries the state it was made in
(`:60`). ⚖️ The **VOICE RULE** lives with the text it binds: `reports/still-needed/WORDING_RULED.md` and
`perma/PUBLIC_SURFACE_SWEEP.md`.

What is only here:

- **Delegate heavy reads; keep the conclusion.** Review peers at **SURFACE level** and **escalate rather
  than deep-check** — a high-context session is at *higher* hallucination risk than a fresh one.
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
