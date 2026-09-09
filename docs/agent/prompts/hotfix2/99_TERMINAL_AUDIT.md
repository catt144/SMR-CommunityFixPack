# 99 · Terminal audit — adversarial, backward, trusting nothing forward

Chain: `prompts/hotfix2/README.md`. **You are last.** Fresh context, by design:
you exist to find what forward motion structurally cannot see. Every "done"
upstream is a **claim** until you have re-derived it.

⚖️ **The bar you are auditing against, in the owner's words:** *"The last thing I
want is to release a half-baked patch and then have to immediately repatch it."*

## 0 · Start

`git log --oneline -20` · `git pull` · `ListAgents`. Build a todo list covering
all eight passes below before you begin.

**Read path:** `agent/STATE.md` · `VANILLA_FIX_QA.md` **§0 first** ·
`PACK_1_1_0_REVERIFICATION.md` · `agent/reports/HOTFIX_1_AUDIT.md` (the format
and standard your verdict follows) · `docs/PLAYTEST_CHECKLIST.md` items 98,
111–118 · `agent/FIX_POLICY.md` · `docs/UPLOAD_WORKFLOW.md` §3 ·
`agent/reports/STORE_CARD_LIVE.md` · **every `## Notes from upstream` block
appended below.**

## 1 · The folder-empty gate

`docs/agent/prompts/hotfix2/` must contain only this file and `README.md`, and
every README row must be struck. **A non-empty folder is a DO NOT SHIP**, full
stop — it means a link did not finish and nobody owns what it dropped.

## 2 · Pass A — the instruments, re-run by you

Re-run `doccheck.py` (+ `--emit-counts`), `sigcheck.py`, `bodycheck.py` and
`logscan.py` against the canonical boot log yourself. Do not read a result out of
an upstream summary.

⛔ **And audit the instruments, not just their output.** `bodycheck.py` was
written inside this chain by the session whose work it validates. Make it fail on
purpose — a deliberately wrong `SRC:` hash must produce `BODY-CHANGED`, a
`DEFECT:` you know is still shipped must NOT produce `DEFECT-GONE`. A tool that
returns GREEN on everything is indistinguishable from a broken one, and that is
precisely how F114 shipped past three instruments.

## 3 · Pass B — re-derive every code change against the 1.1.0 body

For each module touched by 03 and 04: open the shipped 1.1.0 function and check
the change against it. **The QA's pinned shapes are your checklist** —
`VANILLA_FIX_QA.md` §0.5 and Reader A's rows. Specifically:

- F-1: does the probe fail CLOSED? Does the save re-base exist, and is it
  reachable when the pass DECLINES (our old heal keyed on `rebased_from` is not)?
- F-3: is half (a) gone and half (b) intact?
- F-6: does the tutorial return precede the gate? Is the flag stamped on the
  confirmed path, not on `Apply` entry?
- F-7: is `not self.refuel_disabled` carried?
- F-9: is it a re-copy and **not** a distance pre-wrapper?
- F-10: is the BlackCube hook (`Train.lua:800-802`) carried?

⛔ **A body diff, never a grep.** F116 was filed off a keyword grep; two of its
four claims did not survive a real structural diff and a fifth divergence
appeared only when the bodies were diffed properly.

## 4 · Pass C — the deletions are actually gone, in all four places

For every removed module: absent from `Code/`, absent from `items.lua`, absent
from the boot log's `[CommunityFixPack]` block (**absent, not `inactive`**), and
absent from the deployed site's fix list. ⛔ `H-10` inverts on this patch — the
`code` list in `metadata.lua` is rebuilt from `items.lua` on a forced save, so
an inconsistency decides what ships.

Confirm the two save cleanups are keyed as the QA specified: F-5 on `prop` +
label (QA §0.2), and F-1's re-base (§0.3).

## 5 · Pass D — nothing on the KEEP list was touched

35 modules should be untouched except for their `SRC:`/`DEFECT:` stamps (and
`GeneForging`'s A-1 edit). Diff them. An unexplained change to a KEEP module is a
finding.

## 6 · Pass E — the 1.0.7 constraint (ck118)

Every module carrying a 1.1.0 body **declines on 1.0.7**, and it does so via a
per-module probe, ⛔ **not** a game-version detector. If anyone built a version
check, that is a finding: `lua_revision`, `ModMinLuaRevision` and
`ModRequiredLuaRevision` are all 350453 on both branches, so such a check is
either inert or wrong.

## 7 · Pass F — text against reality

Read every player-facing string against what actually shipped:
`metadata.lua` `description` / `short_description` / `last_changes`, the
`UPLOAD_WORKFLOW` §3 paste backups, `STORE_CARD_LIVE.md`, the site.

- Do the backups match `metadata.lua` **exactly**? They are the real delivery
  path; auto-fill has never produced a clean page in two cycles.
- Is every "Fixed" a claim someone actually confirmed? Name the ones that are not.
- Is the fix count recounted from the deployed fix list?
- Does the ck112 wording still overpromise given what this patch actually built?

## 8 · Pass G — the owner's controls, and what was never exercised

List, plainly, **what has not been run in a game**. At authoring time that was
everything: the 09-08 boot was menu-only, so trains, landscaping and track
salvage have never been exercised on 1.1.0 at all, and PT-20 uninstall safety was
verified on 1.0.7 only.

⛔ **You move no status.** You name what was not exercised, and you say which
claims rest on source reads alone.

## 9 · Pass H — drift corpus

Collect every drift instance appended to your inbox by upstream links, plus
everything you find. Ten-second fixes count. If the corpus shows a pattern rather
than a list, say what the pattern is — that is worth more than the individual
items.

## 10 · The verdict

One line: **SHIP** / **SHIP WITH CHANGES** / **DO NOT SHIP**, followed by:

- the changes, if any, each with the file and what to write;
- ⭐ **the "what would make this half-baked" list** — the QA format's most
  valuable section, and the direct answer to the owner's sentence;
- what is owed AFTER upload, and by whom;
- the kickoff line for whatever comes next, or "nothing queued".

Write it to `agent/reports/HOTFIX_2_AUDIT.md`. File owner decisions in
`docs/PLAYTEST_CHECKLIST.md` → "Decisions waiting on you", never only here.

## 11 · What may NOT be claimed

- ⛔ Not "verified" for anything you only read. Say "source-derived".
- ⛔ Not "safe to ship" on the strength of green instruments — you audited four
  tools that between them cannot see class c (semantics moving under a wrapper),
  which was 6 of the 10 FIX rows in this audit.
- ⛔ Not a status move. Not a `tested` grant. Not an upload.
- ⛔ Do not certify your own corrections. If you fix something, say a fresh
  context should look at it — the executor is the wrong person to certify its own
  rewrites, and this project has that on the record.

## 12 · Close-out

Green gates. `STATE.md` updated to point at the audit report (⚠️ byte-capped —
evict in the same commit). ⛔ **You do not delete this file** unless the chain is
truly finished; if the verdict is SHIP WITH CHANGES, the changes are somebody's
prompt and the chain is not over. Say which.

## Notes from upstream

*(From the authoring session, `smr-bugfixpack-91`, 2026-09-08. Links 01–06
append below as they close.)*

- ⚠️ **The decomposition and model placement of this chain were done by an Opus
  session, not a Fable one.** `CHAIN_METHOD` §4.0 says a chain of 6+ prompts
  should have its setup done by the top tier unless the owner overrides; the
  handoff assigned it here. Treat the chain's SHAPE as auditable, not given — if
  the split is wrong, that is a finding worth as much as any code defect.
- ⚠️ `sigcheck.py` bounds ARITY only and rated `Fix_TrackSalvageWipe` OK both
  before and after F116's defect was found. Do not accept it as a clearance
  anywhere, including in an upstream link's summary.
- ⚠️ `metadata.lua`'s "`PackVersion` renders version_major.version_minor.version"
  comment has zero hits in the 1.1.0 tree. Recorded facts are claims too.
- ck111 (F116's orphan policy — vanilla REHOMES an orphaned track fragment, our
  fix DELETES it) is **open and unruled**, and it is a player-harm question, not
  bookkeeping. It is not this chain's to close, but note whether the patch makes
  it more urgent.
- ck118 is ruled: 1.0.7 players are served by a frozen v5 GitHub release plus a
  site page, both live. The store-card line pointing at it is link 06's.
