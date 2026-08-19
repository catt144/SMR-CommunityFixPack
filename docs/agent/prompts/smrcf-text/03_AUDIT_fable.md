# B·03 — terminal adversarial audit · fresh context · TRUSTS NOTHING FORWARD

**You are the adversary.** Read `README.md`, then `STATE.md`, then this, then
`## Notes from upstream`. Everything upstream is a **claim**.

## 0 · Staleness check
```
git log --oneline -10
git pull
```

## 1 · 🗒 Live todo list from your first action.

## 2 · The audit

### 2.1 Inbox audit
Every upstream note delivered, routed to a named owner, or explicitly declined.
**Zero orphans.**

### 2.2 Re-derive, do not inherit
- Every citation at `ModTools\Src`, **by symbol** — not by the line number you
  were handed.
- **Re-verify enrolment independently**: extract a shipped language pack yourself
  (`EF-063`) and confirm the ids the modules point at are actually in it. This is
  the load-bearing fact of the whole chain and it is checkable in a minute.
- Logs re-counted by you and byte-verified against the game's own.
- Prediction commits proven in `git` to precede their launches.

### 2.3 The `EF-039` trap — check it was not walked into
`C50`'s module must **append** via `shipped_T .. Untranslated("…")`. If it
replaced `T(880574954148, …)` with a new literal, **it regresses eight languages
to English** and that is a shipping defect, not a stylistic quibble. Read the
module, not the summary.

Same question for `C51` in the other direction: does the UI end up pointing at an
**enrolled** id, with no English literal in the retail path?

### 2.4 The first-of-kind risk
`C51` is this pack's first XDef/UI patch. Check what a normal review would not
think to: does the wrapper survive UI rebuilds, does it restore cleanly, does it
leave nothing behind on disable, and does it avoid `FIX_POLICY` §1.5 territory?

### 2.5 The conditional item
If the marker gate was built — was chain A's census actually non-zero, and on a
map a player visits? A fix for an unreachable defect is `C49` with extra steps
and should have been declined.

### 2.6 Status words
`tested-attended` requires the owner to have **personally seen** the thing
resolve, with the evidence re-readable. `tested-unattended` is ⛔ **closed to
screen events** — and all three items here are screen events. Check what was
granted against what was witnessed.

### 2.7 Consistency + drift
Front matter vs heading tags vs regenerated `INDEX.md`; counts tool-emitted;
`mkdocs --strict` if any public surface moved; **every drift recorded, not
silently fixed.**

## 3 · Scope fence
**IN:** audit, corrections, integration, folder-empty gate, owner report.
**OUT:** ⛔ no new runs · ⛔ no new fix code (a correction to a shipped module is
allowed and must be disclosed as one) · ⛔ no launching the game.

## 4 · Stop conditions
- A verdict cannot be re-derived from primary evidence → **do not sustain it.**
- A shipped module regresses a language → that is **release-blocking for that
  module**; pull it rather than ship it, and say so.
- The primary log is missing or mismatched → a finding, and an R8 process failure.

## 5 · ⛔ What may not be claimed
- ⛔ **"Audit-sustained"** for anything not re-derived from primary evidence.
- ⛔ **"Works in all nine languages"** — German is the pack we verified; the rest
  is inference, labelled as such.
- ⛔ **A `C35` conclusion.** Its detector firing is a precondition reading, not a
  harm finding.
- ⛔ Any claim about player-visible behaviour without a screenshot behind it.

## 6 · Close-out — the folder-empty gate
One commit: corrections applied · entries and heading tags in step · `STATE.md`
extended (byte caps, doccheck-enforced; evict resolved material, never an obligation) · card/site/
`metadata.lua` swept **if anything shipped** · counts re-emitted by the tool ·
doccheck GREEN (and `mkdocs --strict` if public pages moved) · `git rm` this file
— **the folder must end EMPTY** · grave named · push.

**End the owner report with the kickoff line for the next queued chain**, and say
in one sentence whether ④ has happened.

⭐ **If this was the LAST chain of the set to close**, delete
`agent/prompts/SMRCF_CHAIN_SET.md` in the same commit and name its grave.

## Notes from upstream
