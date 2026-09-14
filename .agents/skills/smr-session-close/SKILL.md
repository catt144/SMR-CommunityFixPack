---
name: smr-session-close
description: Close a session without losing anything — dump the session to a scratch doc, trim it against written criteria, route whatever has no home, and update the handoff with a measured delta. Use when the owner says it is time to hand off, time to close, or time to get on fresh context, or when context is running low.
---

# Session close — dump, then trim

⛔ **You have degraded context.** Never answer *"what did I learn?"* from memory — recall fails
first and fails silently. **Dump first, then judge what is on the page**: that turns every cut
into a decision instead of an omission.

## Mode

- **close** — any session. Route what is homeless; verify nothing is stranded.
  ✅ **A session with no finding needs no ceremony — say so in one line and stop.**
- **handoff** — the session owns a handoff doc. Do `close`, then §3.

⛔ **Both halves are THIS session's job.** A successor cannot trim — it cannot tell what you
omitted deliberately from what you forgot, and cutting is a one-way door.

## 1 · Dump — evidence first, memory second

Write to a scratch file. ⛔ Not from recall:

- `git log` your own commits — for each, did its lesson get a **home**, or only a commit message?
- `git status` — anything uncommitted or untracked you meant to keep?
- The handoff's open items — which did you touch, and is each one's stated state still true?
- Decisions made, and where each landed.
- **Then** narrative, marked as the weaker layer.

⛔ The dump is **scratch — delete it when consumed.** An accumulating dump is a tombstone.

## 2 · Trim — against these criteria, not judgement

**CARRIES:** live state and what unblocks it · decisions · measurements expensive to re-derive ·
traps that already bit, **with the receipt** · routing that cannot be inferred.

**DOES NOT CARRY:**
- ⛔ Anything with a canonical home — carry a **pointer, never a copy**. Chief source of bloat.
- ⛔ Narrative of what happened. `git log` holds it, more accurately.
- ⛔ Settled decisions with no live consequence — only the resulting state stays.
- ⛔ **Numbers you would have to re-emit.** If a doc forbids quoting its own numbers, they do not
  belong in it. Write the command instead.
- ⛔ Lessons that generalise past this seat — skill, doc or memory material.

### ⭐ The why-rule, by author

| author | carries |
|---|---|
| **owner decision** | the decision, bare, marked as theirs. ⛔ **No rationale** — authority terminates, and a why is a foothold for relitigating it. |
| **agent decision** | the decision **and its basis** — it is a claim, and a successor will redo it wrong without one. |

⭐ **If you need the why to know what a decision MEANS, it is recorded badly — fix the
statement, never append an argument.**

## 3 · Handoff mode — the ratchet

⛔ **Expect net-flat or net-negative** — you home things elsewhere as you add. **Growth is the
exception and needs one line of justification.**

- State the delta in **`wc -c` bytes** and name the unit; `git cat-file -s` and Python `len()`
  differ on the same file, and all three were confused here in one session.
- Trim **per section**: does this still earn its place? Rewriting instead of trimming is how a
  trim pass *grows* a file.

## 4 · Finish

Say what was routed and where, then state **"nothing load-bearing exists only in this
conversation"** — a checked claim listing the evidence, ⛔ never a ritual phrase.
