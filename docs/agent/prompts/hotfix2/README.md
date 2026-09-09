# hotfix2 — the chain manifest

Effort: turn the 1.1.0 re-verification's findings into a shipped patch.
Authored 2026-09-08 by `smr-bugfixpack-91` under `prompts/HOTFIX_2_HANDOFF.md`
(now consumed). Method: `agent/reports/CHAIN_METHOD.md`. Authoring mechanics:
`agent/WORKFLOW.md` "Authoring a prompt" elements 1–8.

> ⚖️ **THE BAR, in the owner's words:** *"The last thing I want is to release a
> half-baked patch and then have to immediately repatch it."* Every prompt below
> is written against that sentence. Marathon, not sprint.

## The queue

| # | file | model | owner needed? | what it drains |
|---|---|---|---|---|
| ~~01~~ | ~~`01_CORE_AND_TOOLING.md`~~ | Fable | no | ✅ **DONE 2026-09-08** (`smr-bugfixpack-25`): `probe` form `6d452a3` · `tools/bodycheck.py` + falsifier `401f8a0` · `FIX_POLICY` §2a branch guard + §2b manifest grammar `6db7457` · all 35 KEEP modules stamped `e2490f3`. Outbox is in 02–05 and 99 |
| ~~02~~ | ~~`02_REMOVE_BLOCK.md`~~ | Opus | no | ✅ **DONE 2026-09-08** (`smr-bugfixpack-11`): ck98 ruled DELETE + ck117 ruled KEEP, both in-session. 36 modules deleted with `items.lua` **and** `metadata.lua`'s `code` list, 81→45 in all three `2dc1dbe` · R-7 half-edit + the sanitizer's dead F03 pass `f707903` · 43 bug entries stamped `9b0b82c` · 36 site fix-list entries removed (`SMR-CommunityMods` `7cef4f3`) · `C54` filed. ⛔ No F-5 cleanup — owner ruled it off (ck120). Outbox is in 03, 04, 06 and 99 |
| 03 | `03_HARMS.md` | Opus | ⛔ blocked on ck-F-2 | the applies-today repairs on modules that SURVIVE: F-1 probe-gate + save re-base, F-2 exemption (if kept), F-3 delete half (a) |
| 04 | `04_RECOPIES.md` | Opus | ✅ no | group **B** only: F-6, F-7, each with its `SRC:`/`DEFECT:` manifest and a 1.0.7 decline · **plus §7: `Fix_TrackSalvageWipe` (F116), the two divergences ruled as ck111 + ck119 — a scoped edit to a KEEP module, needs a re-stamp** |
| 04b | `04b_RECOPIES_C.md` | Opus | ✅ no | group **C**: F-8, F-9, F-10 — **all three RULED IN by ck123**, partly reverting ck109; every gate STAYS. ⛔ Highest-risk work in the patch; F-9 is a ~98-line rewritten function and may split again to `04c` |
| 05 | `05_TOOLS_TAIL.md` | Opus | no | `sigcheck.py` over `SetGlobal` sites (A-4), `logscan.py` heal-aware + benign-latch retire list (A-2/A-3), A-1 `GeneForging` |
| 06 | `06_TEXT.md` | Opus | no | ck112/113 store wording, `metadata.lua` `last_changes`, `UPLOAD_WORKFLOW` §3 paste backups, the site fix list |
| 99 | `99_TERMINAL_AUDIT.md` | Fable | reports to owner | adversarial backward QA over the whole result; SHIP / SHIP WITH CHANGES / DO NOT SHIP |

**Ordering.** 01 is strictly first — 02, 03 and 04 all use `bodycheck.py` and the
`probe` form. **02 before 03 and 04**, because 02 owns `items.lua` and the
`metadata.lua` `code` list and no other prompt may touch them. 03 and 04 are
independent of each other and may run in either order. **04 and 04b are also
independent of each other** — either order, or in parallel by two sessions, since
they share no module and no file. 05 and 06 are independent of everything except
01. 99 is last and runs only on an empty folder.

⭐ **Why 04 split into 04 + 04b, recorded per `CHAIN_METHOD` §3.** Split
2026-09-08 **before either half ran**, under rule 4 and the owner's explicit
pre-authorisation (ck123: *"If the work is really that heavy we should have a 04
and and 04b"*). Six modules at this discipline — a body diff, a re-copy, a
manifest stamp, a `probe` gate, `bodycheck.py` either side and its own commit
each — do not fit one context, and F-9 alone is a ~98-line rewritten function.
⚠️ The judgement was made up front rather than left to a session to discover
mid-link, because **a link cannot see its own context budget** (owner,
2026-09-08). ⛔ Both halves carry a FULL inbox; neither points at the other for
link 01's probe spec, because each `git rm`s itself on close-out.

⚠️ **Deviation from the handoff's suggested split, stated per `CHAIN_METHOD` §3.**
The handoff put F-4/F-5/R-20 in the "harms" prompt and the rest of the removals
in the "remove block". This chain instead cuts **deletions vs repairs**: every
module deletion lands in 02. Reason: `H-10` inverts on this patch — with 37
modules leaving, the failure mode is a module dropped from `Code/` but left in
`items.lua` (or the reverse), and both portals rebuild `metadata.lua`'s `code`
list from items on a forced save. Splitting the deletions across two prompts
splits that consistency check across two sessions. One prompt owns it.

## Binding chain rules — every prompt inherits these

1. **Staleness check first.** `git log --oneline -10`, `git pull`, `ListAgents`.
   Several smr-bugfixpack sessions edit this tree at once; message any peer whose
   lane you are about to enter, and never touch a stranger's unstaged file.
2. **Inbox / outbox.** Read `## Notes from upstream` at the bottom of your prompt
   before you start. On close-out, append your outbox to the NEXT prompt's
   `## Notes from upstream` **and** to `99_TERMINAL_AUDIT.md`'s, update your row
   in this README (strike it), `git rm` your own prompt file, and commit all of
   it together.
3. **Route, do not drop.** Anything you find that is out of your fence gets
   FILED (a bug entry, a fact, a checklist item), never fixed and never dropped.
   Unsure whether it is yours? **STOP AND ASK** — do not guess.
4. **Self-split at a clean commit boundary.** If the job will not finish
   comfortably in this context, split it: commit what is done, write `NNb_*.md`
   as a first-class chain member with a full inbox, add its row here. Never push
   a job to the edge of a window.
5. **Capture drift as evidence, not shame.** Every mistake you catch in your own
   or an upstream prompt's work — including ten-second fixes — gets appended to
   99's `## Notes from upstream`. A silently-corrected instance is destroyed
   evidence.
6. **Re-derive the ROUTE, always.** The pinned shapes in your prompt are design,
   not permission to skip verification. Every route failure this project has had
   sat on top of individually-correct citations (`CHAIN_METHOD` §2.3). Read the
   1.1.0 body before you edit against it.
7. **⛔ No instrument here is a clearance.** `sigcheck.py` bounds ARITY only and
   rated `Fix_TrackSalvageWipe` OK both before and after its defect was found; a
   name sweep sees names; the runtime existence checks see existence. F114 was
   invisible to all three. Only a body read clears a body.
8. **Live todo list, one item per commit-and-verify unit**, marked complete the
   moment it completes. The owner reads it to decide when to step in.
9. **Green gates before every commit:** `python tools/doccheck.py` GREEN,
   `python tools/sigcheck.py`, `python tools/bodycheck.py` (from 01 onward), and
   a parse sweep of every `.lua` you touched. Commit with `git commit -F <file>`
   (embedded quotes split args under PS 5.1), then push.
10. **⛔ `Code/` edits only with `Mars.exe` closed.** A packed folder must never
    be staged beside a live junction (`H-09`).
11. **⛔ Never move a status you did not witness.** A source read is never
    `tested`. A patch note that says "Fixed" is a CLAIM, false until confirmed
    (owner rule, 2026-09-08).
12. **Bindings in force:** `H-02` (no Mod Editor, no `version` edit, no upload —
    those are the owner's sitting), `H-03`, `H-04`, `H-08`, `H-09`, `H-10`.
    Owner decisions go to `docs/PLAYTEST_CHECKLIST.md` → "Decisions waiting on
    you", never only into an agent doc.
13. **A doccheck WARN goes verbatim into your summary.** `STATE.md` is
    byte-capped (warn 9216) — any line you add needs an eviction in the same
    commit (`prompts/STATE_EVICTION.md`).

## ⛔ The constraint that binds every code prompt (ck118)

Nothing stops this build reaching a **1.0.7** player. Our `lua_revision` is
350453 and 1.1.0's `ModMinLuaRevision` / `ModRequiredLuaRevision` are BOTH
350453, so `ModDef:IsObsolete()` is false on both branches and the pack installs
and loads on 1.0.7 silently. For a deletion that is a regression. **For a module
carrying a 1.1.0 function body it is the F114 failure mode in reverse** — our
copy applied over a function that does not match it.

⇒ **Every module that gains a 1.1.0 body must carry a self-check that DECLINES on
1.0.7**, and that check must test the thing, not a label. This is not a
preference and it is not conditional on decision 98.

## Read path — declared

`docs/agent/STATE.md` (mandatory) · `agent/reports/VANILLA_FIX_QA.md` **§0 first**
· `agent/reports/PACK_1_1_0_REVERIFICATION.md` (the rows your prompt names) ·
`agent/FIX_POLICY.md` · `agent/WORKFLOW.md` "Authoring a prompt" ·
`docs/PLAYTEST_CHECKLIST.md` items 98, 111–118 · your own prompt's inbox.
⛔ QA §0 corrects the main report in four places and the main report says so —
read it before any row of the main report.

Game source: the 1.1.0 tree at
`A:\SteamLibrary\steamapps\common\Project Spark\ModTools\Src`. The 1.0.7 tree is
GONE (`EF-075`) — every "1.0.7 said X" is our module's own header or a bug entry,
never a re-read.
