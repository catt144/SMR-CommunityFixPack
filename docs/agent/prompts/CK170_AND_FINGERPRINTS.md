# CK170_AND_FINGERPRINTS — close the audit's policy item, then reclaim the fingerprint base

**Fire with:** a fresh session rooted at `C:\Dev\SMR-BugFixPack`. Tool-neutral. Written 2026-09-13
by `smr-bugfixpack-da`; a different seat adjudicates the **output**, not the report.
`git rm` this file when it has fired.

## 0 · How to read this brief

⭐ **This states goals and reasoning, not a script.** The owner's ask: *"Make sure the prompt doesn't
box in codex, give it room to alter the plan if it finds a better way or stop and ask questions if
it's concerned."*

- **You may change the approach.** If a step below is the wrong way to reach the stated goal, take
  the better way and say what you changed and why. The goals in §2 and §3 are the contract; the
  suggested mechanics are not.
- **You may stop and ask.** A question costs one round trip; a wrong guess costs a pass. Ask.
- **A defect that does not reproduce is a finding** — record it, skip that item, **continue**. Do not
  halt a phase over one refuted item. (The last brief got this wrong and stranded three repairs.)
- **Two previous briefs from this seat over-constrained their implementor** — a count written as a
  fence, and a skip rule written as a halt. If something here reads as an absolute that was probably
  meant as a default, treat it as a default and say so. The ⛔ rails in §4 are the real absolutes.
- Every number below was measured 2026-09-13 and is **a claim** — re-derive before relying on it.

## 1 · Anchor

```
git -C C:/Dev/SMR-BugFixPack status -sb | head -1 ; git log --oneline -3
python tools/doccheck.py | grep -E 'MARKER|PUSH SET|STATE \+ STUBS|^doccheck'
python tools/doccheck.py --emit-fingerprint | grep -E 'FINGERPRINTS|HOLDS|MOVED|route by'
```
⚠️ Peers share this checkout under one git identity — identify by **sha + diff**, re-check
`git status` immediately before every write, never `--no-verify`.

## 2 · Phase 1 — the owner's ck170 rulings, so the item can close

Owner ruled 2026-09-13, in conversation. Agent docs are the only home these have.

**(a) Marker vocabulary — keep the four words** (`open · ruled · closed · deferred`).
`part-ruled` is **not** adopted: `status` says where the *decision* stands, `owner:yes` independently
says an *action* is owed, and a partial ruling is `open` + `owner:yes`.
Goal: **`MARKER INTEGRITY` reads on-disk == parsed, and the register renders the CURRENT ask.**
Today it reads `46 on disk, 45 parsed`, and your register row for **169** still shows the superseded
09-12 *"v10 IS READY TO UPLOAD"*. Known inputs:
- ck169 has two markers — `:73` `part-ruled owner:yes` on the current 09-13 heading, `:111`
  `open owner:yes` on the superseded heading inside the `<details>` block at 108-147. The invisible
  word means the archived marker wins the row.
- ck144 has two — `:2257` and `:2331`, **both** `closed owner:no`, on two genuinely different items
  sharing a number. A collision, not a supersession; benign only because they agree.
- Suggested shape, change it if you see better: a legal word on 169's live marker · `ck:-` on the
  archived heading (supported since `8f02d68`) · **RED** on an unknown status word or a `ck:`-shaped
  comment that fails `MARKER_RE` · duplicates **WARN when the markers agree, RED when they
  disagree**. That last one closes ck144 without renumbering, which matters because `ck<N>`
  citations are by number and there are hundreds tree-wide.

**(b) Byte accounting — normalise to LF before counting.** Caps unchanged, content unchanged.
`.gitattributes:18` pins `STATE.md` to LF because doccheck counts raw disk bytes, and its own comment
records that a CRLF checkout *"already produced one wrong diagnosis"*. A pin governs checkout, not a
session writing the file back. Goal: **identical content measures identically either way.**

**(c) Reading routes.** Three parts, all ruled in:
1. **Cite `R-A…R-G` from the documents that actually fire.** `grep -rlo "R-[A-G]\b"` across
   `docs/agent/prompts/` and the skills currently returns **zero files** — rails adopted 09-12 that
   nothing pointing at work references. ⚠️ Both skills already *do* R-A's job (`derived_at`,
   `--emit-fingerprint`, "HOLDS needs no re-read") without the label, so this is largely
   traceability; if a citation would add bytes without adding reach, say so and skip it.
2. ⭐ **`DISPATCH.md:34` step 3 says "Scan `docs/agent/bugs/INDEX.md` and `docs/agent/facts/INDEX.md`"
   — 97 KB, at step 3 of orienting, before the session has decided anything.** The step's own last
   sentence already says *"Open only the entry/fact files the task touches."* Only the word "Scan"
   costs 97 KB. Make targeted lookup the instruction; the indices are generated one-line rows, so
   they are grep targets, never reads.
3. **R-D is an AUTHORING rule.** File it where authors read it (WORKFLOW's brief-authoring section)
   and keep it out of working-leg instructions — which is what R-D's own "blinded" already means.
⚠️ Already done, do not redo: *"a HOLDS verdict is a routing aid, not permission to skip evidence"*
landed in `424075c`; the live output says so.

**Then close it.** Record the rulings in checklist **170** and set its marker to `status:ruled
owner:no`. ⛔ This is the **only** status you may set, it is the owner's ruling being recorded, and it
is the first live test of the obligation homed at `WORKFLOW.md:60` — *"changing an item's status ALSO
means updating its marker."*

## 3 · Phase 2 — reclaim the fingerprint base (the real prize)

**Measured now:** `derived_at` across **93** facts — **55 MOVED** (`game 1.0.7.396349`), **18 HOLDS**
(`game 1.1.0 build 24995074`). Fact bodies total ~328 KB.

⇒ The fingerprint tells **every** session that ~59% of the fact base describes a tree that is not on
disk, i.e. re-derive it. Re-deriving one means reading shipped game Lua, far larger than the fact
body. That cost is **recurring and compounds with depth**, where the 97 KB index scan is paid once.
**This is the largest token lever in the whole effort.**

⭐ **And the dominant term is a guess.** **54 of those 55** MOVED facts carry an *inferred* date —
`derived_at: "game 1.0.7.396349 (inferred from updated:)"`. The verdict forcing re-derivation on 59%
of the base rests, in 54 cases out of 55, on an inference from the file's `updated:` field. Many of
those facts were derived on 1.1.0, or describe engine behaviour the patch never touched.

**Goal: shrink the MOVED set with EVIDENCE, never by ruling.** For each inferred-date fact, establish
what it was actually derived against and correct the field. Every fact that leaves MOVED honestly
leaves it for every future session.

⛔⛔ **The harm direction is asymmetric and it decides the method.** A fact wrongly moved **into**
HOLDS silently licenses skipping evidence that was needed — the worst category under the harm test
the owner adopted (`STATE_EVICTION.md` § Hazards admission test: a silent harm outranks a loud one).
A fact left wrongly in MOVED only costs tokens. ⇒ **Be conservative: leave it inferred unless the
real derivation is established, and name what established it for every reclassification.** A
plausible story is not evidence.

How you establish it is yours — the fact's own body, its git history, the entry or report it came
from, the citations it makes and whether those lines still say that in the installed tree. If you
find a better instrument, build it and say so. If a fact's derivation is genuinely unrecoverable,
that is a finding: say so and leave it.

⚠️ **Suspect your instrument.** Three separate instrument defects landed in this project on 09-13
alone — a pack parser that invented two entries, an extraction script that reported an untouched line
as changed, and a grep dedupe that under-counted citations into a brief as a fence. Whatever you use
here reads 93 files and decides what future sessions may skip: **give it a fixture before you trust
its output.**

## 4 · The rails — these are the absolutes

- ⛔ **No owner decision.** The single exception is ck170's own marker in §2. No other status moves,
  no hazard reworded, no rule re-filed beyond what §2(c) names.
- ⛔ **Any gate you add or change must be shown to FAIL on a deliberately broken copy, then
  restored** (`sha256sum` the restore). `_selftest` in `tools/flpk_extract.py` is the worked
  precedent. (b) touches the gate every peer commits through: if it is wrong, everyone stops.
- ⛔ **Emit before/after separately per change.** (b) will *reduce* the measured push set (~430 B of
  it is pure line endings) while (c1) may *grow* `DISPATCH.md`, already the second-largest file in
  that set. Two causes moving one number means neither is attributable.
- ⛔ No count hand-typed; every count carries its command and filter. A count is not a finding —
  check where each hit landed, and never trust a deduped count.
- ⛔ Never state an absence from a truncated grep.
- ⛔ Stop, do not push through: a file dirty or owned by a running peer · doccheck RED outside your
  lane · a rewrite that would change a sentence's meaning · a `POST_UPLOAD_CLOSE` restore owed on
  `metadata.lua`/`items.lua`.
- Phase 1 and Phase 2 are **separate commits**, and Phase 1 can stand alone. Phase 2 may be split
  as finely as you like.

## 5 · Handover

`docs/agent/reports/CK170_AND_FINGERPRINTS.md`. Phase 1: per ruling — what changed, the command that
proves it, `MARKER INTEGRITY` and the push set before/after. Phase 2: the before/after fingerprint
counts, and **per reclassified fact, what established its real derivation**; facts left inferred
listed with the reason. Plus your shas with diff-stats, anything you did differently from this brief
and why, and a **"not done"** list — an empty one on a job this size reads as a missing list.
