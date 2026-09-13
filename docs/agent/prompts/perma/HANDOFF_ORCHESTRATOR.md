# Handoff — session → next session (model-agnostic)

> **RETIRED — DO NOT FIRE (2026-09-13).** The launch and pending outbox are
> closed. Use `DISPATCH.md` for current work and `docs/WAITING_ON_YOU.md` for
> the owner's queue. The remaining text is a retained snapshot, not a task list.

## ✅ v10 IS SHIPPED. THIS DOCUMENT NO LONGER HAS A LAUNCH TO DRIVE.

Rewritten end-to-end **2026-09-13** after the v10 arc closed. Everything the launch needed is done and its
blocks are deleted, per the rule below. **There is no agent item blocking anything.**

⏳ **This file's own removal condition is MET and it is the owner's call** (owner, 2026-09-11: it stays in
`perma/` "until the pending outbox is empty or the owner says things have settled, then it is `git rm`'d").
`RELEASE_OUTBOX.md`'s **Pending is now empty**. `perma/DISPATCH.md` has taken over as the catch-all.
This file is retained pending the owner's removal call; do not grow it or fire its old routes.

⛔ **THIS IS A WORKING DOCUMENT, NOT A SESSION LOG.** History lives in `docs/archive/SESSION_LOG.md`
(append-only, newest first). **If you close something here, DELETE its block.**

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

## 1 · Where v10 landed

⛔ **`STATE.md` carries all of it** — version, portal ids, count word, what went in and out, the site
deployment, C90's unexercised status, the three TestKit probes now pointing at retired modules. **Read it
there; it is the kernel and every session already pays for it.** Nothing about v10 is re-derived here.

✅ **Discharged, and must not reappear on any owed list:** ck158 (the attended gate) · the three retirements
· C90 (`153d180`+`e5f1947`) · the STATE eviction **and** its cap revert to `18 * 1024` (`c820c7f`).

---

## 2 · What is open

### 2a · Owner

⛔ **Do NOT maintain an owner list here.** `docs/WAITING_ON_YOU.md` is **generated** from the checklist
markers by `doccheck --regen` and is the only list that can be trusted — a hand-kept copy in this file
went divergent within a day. **Read it, then read the checklist body it links to.**

⚠️ **Two things the generated list cannot tell you, so they stay here:**

- **144 (a), the owed boot** — ck151 (c) ruled that F52 passage / F54 hub / C83 arrival join it **only if
  the loaded colony already has those layouts; otherwise SKIP THEM BY NAME.** ⛔ Never build a layout to
  make a check possible. That boot also re-stamps the `RunAll()` line (`WORKFLOW.md:537`), VOID since 09-09.
- **151 (b)** is messaging, and **ck165 lets the owner defer it indefinitely — ⛔ do not raise it.**

⛔ **Never rebuild an "owed" list from an older document** — this file's did exactly that on 09-12 and
contradicted its own closed list for most of a day.

### 2b · Agent work, needing no ruling — the v10 fence is LIFTED, pick one with the owner

- **C91** — open candidate: vanilla leaks the Building Codes maintenance modifier on repeal. Dev-report material.
- **C92** — filed 09-13 by a peer (`1b7d695`), `cand` P2: Boundaries of Knowledge can never unlock once a
  Repeatable tech sits in a tracked group. Fix sketched, **not built** — scope call for the owner.
- **Migration residuals, read from the entries 09-12:** **F51** 1.1.0 PARTIAL, leg re-filed **UNRUN** ·
  **F53** PARTIAL, no fresh 1.1.0 evidence · **F59** repaired, **A1 expedition half UNTESTED** · **F73**
  PARTIAL, organic benefit unverified · **F80** `investigating`, causation unproved · **F54** never swept.
- **`treediff` gains a `TABLE-HUNK` list** (`HUNT_AUDIT` §8 item 2). ⭐ **It must compare CONTENT between
  trees, not POSITION** — the classifier reported a merely *moved* block as a new `DefineClass` and
  attributed `__parents` across adjacent blocks (`reports/PINNED_PARENTS_PASS.md`, one of seven rows).
- **Desk NEXT, unclaimed:** `prompts/DLC_DEEP_CHECK.md` (bounded; framing in its banner).
- **`prompts/SELFCHECK_PILOT.md`** — **REMOVED 2026-09-13 on the owner's word, `cf8d51f`.**
- **83 (SHARED TestKit)** — two of its five proposals (a `RunAll` owner filter, a `PACK_ID` on the
  enable-path leg) improve the kit **for us** regardless of the opt-in mod.
- **Hotfix 3 — 135 only.** RULED 09-12: take the `luafn.py` delimiter fix. Desk tool, **0 shipped hashes**.
  ⛔ Do not re-derive the old table or the expired-triage "tension"; both are gone on purpose (ck161).

### 2c · Watch list, not tasks

- ⏳ **The Foreign Aid Rocket report** (Steam, wgtiii, 09-12). Stuck "Unloading cargo", 2 Food, 40 sols.
  ⛔ **NOT ours and NOT filed** — the owner messaged the reporter and is waiting. F119 cannot touch it
  (that is `FuelResourceAmount` on **trade** rockets; this is a `ForeignAidRocketBase` carrying food).
  Lead, recorded so it is not re-derived: `LeaveForever` (`RocketForeignAid.lua:75-85`) sets
  `launch_after_unload = true`, so **departure is gated on the unload finishing** and cargo that can never
  be placed strands the rocket. Their warnings showed **Low Storage**. ⇒ **If they reply, file it as a lead.**
- **Hardening rows 1 + 2 — DEPRIORITISED by ck53, not closed.** `SMRFixPack_Disabled = "yes"` passes the
  `or {}` adoption at `00_Core.lua:13` and every id then reads nil ⇒ **the modder's veto is silently ignored**;
  `= true` throws at that index ⇒ **kills the whole pack, log-only**. Row 2 is the same shape for
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

✅ **HOMED 2026-09-13** — traps 1 and 2 plus the `--regen-waiting` rule above now live in
`agent/WORKFLOW.md` § "Writing in a shared tree". They were the three things that existed ONLY in
this file while its own retirement trigger had already fired. The copies here are a record.

1. ⛔ **All sessions share ONE git identity** — `git log --author` cannot attribute work. Identify by
   **sha + diff**, and list your own shas when relaying.
2. ⛔ **A pathspec is only HALF a commit fence.** It protects every OTHER file, but for a path you *name*, git
   commits that path's **working-tree** content — a peer's unstaged edits included (09-12, `cc3edf2`). On a
   file two sessions are inside at once: stage **your own hunks** (`git add -p`) and commit **without** a
   pathspec. Before `--regen`, check `git status docs/agent/bugs/` for foreign ` M`/`??`.
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
   escapes or regexes, and the absolute scratchpad path (`$TMPDIR` is not set in this shell).

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
