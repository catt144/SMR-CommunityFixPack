# REPAIR_PASS_C — finish group C, and close the marker situation

**Fire with:** a fresh session rooted at `C:\Dev\SMR-BugFixPack`. Tool-neutral. Short job, docs plus
three comment lines. Written 2026-09-13 by `smr-bugfixpack-da`; a different seat adjudicates the
**output**, not the report. `git rm` this file when it has fired.

⚠️ **Why this exists:** `REPAIR_PASS.md` group C halted on one refuted sub-item — the pilot had
already been deleted at `cf8d51f`. **That halt was the brief's fault, not yours.** Its §8 said "a
defect does not reproduce → stop", meaning *skip that item*; it read as *halt the group*, and three
unrelated repairs stopped with it. `fd54c7e`'s report records them honestly as "reproduced,
unrepaired".

⛔ **THE STOP RULE, CORRECTED — this is the one thing to read twice.** A defect that **does not
reproduce** is a **finding: record it, skip that item, and CONTINUE the group.** Halt only for a real
stop condition — a file dirty or owned by a running peer · doccheck RED outside your lane · a
rewrite that would change a sentence's meaning · **anything that looks like an owner decision**.

## 1 · Anchor

```
git -C C:/Dev/SMR-BugFixPack status -sb | head -1
git log --oneline -3
python tools/doccheck.py | grep -E 'MARKER|^doccheck'
grep -c '^\s*--' metadata.lua items.lua        # 0 ⇒ a POST_UPLOAD_CLOSE restore is owed, STOP
```
⚠️ Peers share this checkout under one git identity; re-check `git status` immediately before every
write. Never `--no-verify`.

## 2 · Part 1 — the four unrepaired items (one commit, no ruling needed)

Verified present 2026-09-13; re-derive each, and if one has since been fixed, say so and move on.

1. ⭐ **The marker obligation is still homed nowhere live.** *"Changing an item's status ALSO means
   updating its marker"* exists only at `prompts/perma/HANDOFF_ORCHESTRATOR.md:119`, a prompt whose
   retirement trigger fired. **Home it at the authoring entry point** — `agent/WORKFLOW.md`, with the
   owner-decision/register rules — and quote it from its new home in your report. This is the item
   the owner most wants closed. Verify:
   `grep -rn "updating its marker" --include=*.md . | grep -v docs/archive`
2. **`.claude/IMPLEMENT_PROMPT.md` still opens with a live firing route** — `**Fire with:** task …` —
   and carries no spent banner, though it is spent and was wrong four times. Put a
   ⛔ **SPENT — DO NOT FIRE** banner at the top, above the "Fire with" line, and neutralise that line.
   ⛔ **Do not delete the file** (kept deliberately as a record). ⚠️ It is gitignored — real on disk,
   not committed. Fix it anyway and say so; a firing route in ignored material still fires.
3. **`HANDOFF_ORCHESTRATOR.md:73` now makes a false claim** — *"`prompts/SELFCHECK_PILOT.md` …
   removal recommended, not done."* It **was** done, `cf8d51f`. Correct the line. While in that file,
   clear the residue its own fired retirement condition leaves (item 1 takes the biggest piece).
4. **Three shipped comments read as machine output** after the hazard pass's mechanical rewrite:
   `metadata.lua:159` breaks grammatically (*"and `editor/version rail (agent/prompts/perma/RELEASE.md
   § Release rails)` as reworded 2026-08-24 puts…"* — a long parenthetical between subject and verb) ·
   `:159` backticks the whole phrase where `:180` does not · `items.lua:203` runs ~140 chars against
   the files' ~78-char wrap. **Shorten to a consistent short form** (`RELEASE.md § Release rails`) and
   re-wrap. ⛔ Meaning must not change and every reference must still resolve. Comment lines only, no
   Lua logic.

**Done when:** doccheck GREEN · the obligation greppable and quoted from its new home · no file
deleted · `Code/` has no diff · each item marked repaired, or refuted with its command.

## 3 · Part 2 — the marker semantics ⚖️ FIRES ONLY IF THE OWNER HAS RULED ck170(a)

⛔ **If checklist 170's marker-vocabulary call is still open, do NOT touch any marker or any
threshold. Do Part 1, report, stop.** Check first: `grep -n "ck:170" -A2 docs/PLAYTEST_CHECKLIST.md`.

The two duplicates are **different problems**, measured 2026-09-13:

- **ck169** — `:73` `status:part-ruled owner:yes` sits on the CURRENT heading (09-13, *"UPLOADED …
  ➋ STILL OWED"*); `:111` `status:open owner:yes` sits on the SUPERSEDED heading, inside the
  `<details>` block at 108-147. `part-ruled` does not match `MARKER_RE` at all, so the **archived**
  marker is the one the register renders. One invisible marker plus one supersession.
- **ck144** — `:2257` and `:2331`, **both** `status:closed owner:no`, on two genuinely different
  items that share a number. Not a supersession: a numbering collision. Benign today *because they
  agree*; a silent wrong row the moment they do not.

**The proposal put to the owner (adopt only what they adopted):**
1. Keep the four words; `part-ruled` is **not** adopted. ck169's live marker becomes
   `status:open owner:yes` — its own heading says something is still owed.
2. The superseded heading inside `<details>` takes **`ck:-`** (already supported, `8f02d68`) so it
   stops competing for the row.
3. `MARKER_STATUSES` enforcement goes **RED** on an unknown word, and on a `ck:`-shaped comment that
   fails `MARKER_RE`.
4. **Duplicate `ck` numbers: WARN when the markers AGREE, RED when they DISAGREE.** ⇒ This resolves
   ck144 with no renumbering — and renumbering is the expensive wrong answer, because `ck<N>`
   citations are by number and there are hundreds of them tree-wide.

⛔ Whatever you change, **record the ruling in checklist 170 with its marker** — that is the
obligation Part 1 item 1 is documenting, and this pass is its first test.
**Done when:** `MARKER INTEGRITY` reports **on-disk == parsed** · every threshold change shown to
FIRE on a deliberately broken copy and then restored (`sha256sum` the restore) · doccheck GREEN.

## 4 · What may not be claimed

A count is not a finding — check where each hit landed, and never trust a deduped count. Never state
an absence from a truncated grep. A gate nobody has watched fail is not known to be a gate. "Done"
needs its diff-stat and its doccheck line; no count hand-typed.

## 5 · Handover

Append to `docs/agent/reports/REPAIR_PASS.md` (it is the same pass) under a `## Group C, completed`
heading: per item — the claim, did it reproduce, what changed, the quote from its new home where one
applies. Plus `MARKER INTEGRITY` before and after, your shas with diff-stats, and a **"not done"**
list with reasons.
