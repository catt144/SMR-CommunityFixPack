# PLAYTEST_HELP_DISSOLUTION — dissolve a 62,965 B monolith across four destinations, and home the 17 KB the ruling does not name

Authored 2026-09-15 by the adjudicating seat, against **HEAD `d685f86`**. ck182 is **RULED —
dissolve, do not reframe**. `git rm` this file **and delete its row in `prompts/README.md`, in the
same commit**, when it has fired; doccheck's PROMPT MAP fails a commit that moves only one.

## 0 · Anchor — run first

```
git -C C:/Dev/SMR-BugFixPack pull
git log --oneline -6
git status --porcelain
python tools/doccheck.py | tail -1
python tools/doccheck.py | grep -E 'ROOT|RULES HEADERS|RULE PLACEMENT|SKILLS'
```

⚠️ Several interactive peers share this checkout under one git identity; `git log --author`
attributes nothing — identify by sha + diff, and re-check `git status` **immediately before every
write**. ⛔ Never `--no-verify`. ⛔ Never check out a branch in the main tree — it is the game's
loadable mod via a junction.

## 1 · The ruling, and why this is a deletion rather than a rewrite

ck182, ruled 2026-09-15: **`docs/PLAYTEST_HELP.md` is dissolved, not reframed.** Its finding is
that the file *"is an agent doc with an owner's name on it, which is why it accreted for six weeks
unread"* — its "Ground rules" section is agent material under an owner-sounding heading the owner
correctly never read, and the toolkit walk is measurably stale (six pages documented, seven real,
no `Run` page, two tab labels not matching their ids).

⛔ **Do not improve it. Do not re-walk it. It leaves.**

## 2 · ⭐⭐ THE CENTRAL FINDING — the ruling's four destinations do not cover the file

**Measured at `d685f86`**, per heading, `## ` and `### ` both counted:

| section | bytes | ck182 destination |
|---|---:|---|
| `## Ground rules` (proper) | 3,844 | **→ one line** into `prompt-authoring` (5a's *"never write 'play for a while first'"*) |
| `### EXTERNAL VALIDITY` | 1,927 | hazard → `prompt-authoring` |
| `### Cheating without contaminating results` | 3,691 | hazard → `prompt-authoring` |
| `### Compressing a scheduler with g_Consts` | 1,722 | hazard → `prompt-authoring` |
| `### Salvage mode` | 1,764 | hazard → `prompt-authoring` |
| `### NEVER read a MarsDebug tally as retail` | 1,395 | hazard → `prompt-authoring` |
| `### Test Kit helpers` | 6,072 | → SMRTK reference (agent-facing, pull-only) |
| `## The co-run rig` | 3,951 | → `perma/CO_RUNS.md` |
| `### Verified command reference` | 15,891 | **CUT** |
| `## Save fixtures` | 2,766 | **CUT** |
| `## Commands cited in archived TESTING.md` | 1,506 | **CUT** |
| ⛔ `### Console: what works and what silently does nothing` | **9,402** | ⛔ **NONE** |
| ⛔ `## The ENABLE-PATH leg` | **4,304** | ⛔ **NONE** |
| ⛔ `## The MarsDebug [install] pass` | **3,045** | ⛔ **NONE** |
| ⛔ `### Harness quick facts` | **598** | ⛔ **NONE** |

⛔⛔ **Roughly 17,349 B — about 28% of the file — has no destination in the ruling.** The four
destinations are not exhaustive and **must not be treated as such.** An agent that assumes they are
will either cut unhomed content (the deletion-not-routing failure) or stall.

⇒ **Stage B exists for exactly this.** Route each of the four, one at a time, and where the answer
is CUT, prove it the way §6 requires. ⚠️ `### Console: what works and what silently does nothing`
is the largest and the likeliest to hold live knowledge — it records what the console *silently*
ignores, which is the kind of fact that is expensive to rediscover and cheap to confirm.

## 3 · The job — five stages

### A · Route the eleven assigned sections

Per the table. ⛔ **Open each destination's actual passage before moving anything into it**; topic
overlap is not a home. Where a hazard already exists in `prompt-authoring`, do not duplicate it —
record that it is already carried and cut the source.

⚠️ **`perma/CO_RUNS.md` is already 29,406 B.** Moving the co-run rig into it finishes the 09-12
split that took the protocol and left the mechanics behind — but report its before/after size and
say plainly whether it has become the next monolith.

### B · Home the four unassigned sections — the stage this brief exists for

For each of the four marked ⛔ NONE: decide **route** or **cut**, and say which on the evidence.
⛔ A cut needs §6's proof. ⛔ A route needs the destination's passage opened and confirmed.
⚠️ If a section splits — part live, part spent — split it; do not take the whole either way.

### C · Inherited obligation — `PENDING_MOVES` row 3

The documentation-skills brief deferred one row here deliberately (`5245727`): **the warmed-up-save
rider line now has a `prompt-authoring` destination, and this task may move it with its source
removal.** Neither source nor destination was changed for that row. ⛔ Read `.claude/PENDING_MOVES.md`
row 3 before starting; it is gitignored and nothing in the tree points at it. **A half-move is worse
than none** — content lands in the destination *and* leaves the source, in one commit, and the row
is marked done.

### D · The gated deletion — `PLAYTEST_HELP.md` cannot leave quietly

Removing the file breaks three gated references. **All three change in the same commit as the
deletion, or the tree goes RED for every peer:**

- `CLAUDE.md:30` — the folder contract naming the six human files. ⛔ Edit `CLAUDE.md` and run
  `python tools/doccheck.py --regen` **in the same commit**, or `AGENTS.md` drifts.
- `docs/README.md:13` — the map the `ROOT` check reads to decide what `docs/` may hold.
- `tools/doccheck.py:125` — the required-rules-header list. Two comments at `:113` and `:1265` name
  the file in prose and should stop doing so.

⚠️ `PLAYTEST_HELP.md` carries a `Must_Read_Header` with one canonical rule. Removing the file
removes a rule from the corpus: the `RULES HEADERS` count drops from 32. **Report the new count and
confirm `RULE PLACEMENT` still passes.** That rule is the file's own content contract — it dies with
the file, which is correct, and is the one deletion here that needs no survivor.

### E · Consume

`git rm` this brief **and** its `prompts/README.md` row, same commit.

## 4 · Read path — these files, not their folders

`docs/PLAYTEST_HELP.md` · `docs/PLAYTEST_CHECKLIST.md` ck182 only (the ruling and its split) ·
`.claude/PENDING_MOVES.md` row 3 · `.claude/skills/prompt-authoring/SKILL.md` and
`doc-editing/SKILL.md` (destinations, and `doc-editing` governs every edit here) ·
`docs/agent/prompts/perma/CO_RUNS.md` · `CLAUDE.md`, `docs/README.md`, `tools/doccheck.py` (§D).
**For further records:** look up by identifier in `docs/agent/bugs/INDEX.md` and
`docs/agent/facts/INDEX.md` — generated rows are lookup targets, ⛔ never whole-folder reads.
⛔ **Out:** `docs/archive/` · the checklist below ck182 · checklist 177's marker gate.

## 5 · Derived facts (R-C) — every number is a CLAIM; re-derive before acting

An empty `git diff --stat d685f86..HEAD -- <paths>` means that source needs no re-reading.

| fact | measured | at | falsifier |
|---|---|---|---|
| `PLAYTEST_HELP.md` is **62,965 B** | `wc -c` | `d685f86` | `wc -c docs/PLAYTEST_HELP.md` |
| the per-section table in §2 | Python slice on `## `/`### ` boundaries, byte-counted | `d685f86` | re-run the slice; ⚠️ **a `## `-only slice reports "Ground rules" as 44,911 B** because it swallows every `###` under it — this seat made that error and ck182's 3,900 B was right |
| **~17,349 B has no ck182 destination** | §2 table minus the assigned rows | `d685f86` | re-derive from the table; it is a subtraction, not a reading |
| `CO_RUNS.md` is **29,406 B** before the move | `wc -c` | `d685f86` | `wc -c docs/agent/prompts/perma/CO_RUNS.md` |
| three gated references block the deletion | `grep -rn PLAYTEST_HELP CLAUDE.md docs/README.md tools/doccheck.py` | `d685f86` | the same grep |
| the corpus carries **32** canonical rules | doccheck `RULES HEADERS` | `d685f86` | `python tools/doccheck.py \| grep 'RULES HEADERS'` |

## 6 · What may NOT be claimed

- ⛔ Never claim a section was **routed** without having opened the destination's passage and
  confirmed it carries the finding *and* its conditions. Topic overlap is not a home.
- ⛔ Never claim a section is **spent** without the one command showing its referent is gone, or the
  named passage that supersedes it. *"It looks stale"* is not evidence; the file being dissolved is
  not evidence about any particular sentence inside it.
- ⛔ Never claim the dissolution is complete while any content exists **only** in the deleted file.
  That is deletion, not routing, and it is the failure this brief is most likely to produce.
- ⛔ Never claim `doccheck` GREEN proves nothing was lost. The gates check structure; **no gate can
  see a fact that stopped existing.**
- ⛔ Never treat §2's four destinations as exhaustive — they demonstrably are not.
- An agent that cannot cite evidence for a claim says the narrower true thing.

## 7 · Scope fence and stop conditions

**In:** routing and cutting `PLAYTEST_HELP.md`'s sections, the three gated references, `PENDING_MOVES`
row 3, the deletion, the consume. **Out:** rewriting any destination's existing content beyond
receiving the move · re-walking the toolkit surface (the staleness is a reason to dissolve, not a
repair job) · the SMRTK reference's own accuracy · checklist 177 · skill caps (ck186 is the owner's).

**Stop and report — this is permission, not failure — if:** a section has no defensible home and no
proof it is spent · a destination's passage contradicts what you are about to move into it · the
deletion would take the last copy of anything · `CO_RUNS.md` grows past the point where it is the
new monolith · removing the file cannot keep doccheck GREEN in one commit · a peer is mid-flight in
a target file · anything that looks like an owner decision.

## 8 · Lifecycle, attendance, and the progress list

**Lifecycle:** one-off. Consumed at stage E — file and map row, same commit.

**Not applicable, stated rather than omitted:** no game boot, save, module or shipped Lua is
touched, so **the probe-sweep step does not apply.** Nothing here tests or records a test.

**Required — a live progress list before you start executing.** One item per commit-and-verify
unit: one per assigned section routed (§A) · one per unassigned section decided (§B) ·
`PENDING_MOVES` row 3 · each gated reference · the deletion · the rules-count report · the consume.
Exactly one in progress; expand a stage the moment it splits; put stable state in the item text.
⛔ Do not carry several commits behind one checkbox. The owner reads this list to decide when to
step in.

## 9 · Done when

Every section in §2's table is routed to a confirmed passage or cut with proof, **including all
four marked ⛔ NONE** · `PENDING_MOVES` row 3 is moved in both directions and marked done ·
`docs/PLAYTEST_HELP.md` no longer exists · `CLAUDE.md` (with `--regen`'d `AGENTS.md` in the same
commit), `docs/README.md` and `tools/doccheck.py` no longer name it · `ROOT` passes against the
updated map · the new `RULES HEADERS` count is reported and `RULE PLACEMENT` passes · `CO_RUNS.md`'s
before/after size is reported with a plain verdict on whether it is now a monolith · `doccheck`
GREEN at every step · one commit per unit so each reverts alone · executed model recorded (R-G) ·
this brief and its `prompts/README.md` row both gone, in the same commit.
