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

⚠️ **This is a reading you take when you START.** §12 has you AUTHOR
`100_DOCSWEEP.md` as your final act, so the folder is deliberately non-empty when
you finish. That is the designed end state, not a failed gate.

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
- F-8: repaired on `(map, mark, callback, ...)` reading `map.Landscapes[mark]` —
  ⛔ not the old signature, not the bare `Landscapes` global? Is the F115 gate
  still there?
- F-9: is it a re-copy and **not** a distance pre-wrapper? ⛔ And is its gate now
  **DELIBERATE**? It was inactive BY ACCIDENT (a `const.` → `g_Consts` rename
  broke the path spec); an accidental gate is one rename from silently re-arming
  a stale body, so "still inactive" is NOT a pass here.
- F-10: is the BlackCube hook (`Train.lua:800-802`) carried?

⚖️ **Group C (F-8, F-9, F-10) was RULED IN by the owner as ck123** — "all get
fixed" — which **partly and deliberately reverts ck109** ("gate, not repair" for
F-8). ⛔ Do not report that reversal as drift; ck109 was ruled mid-emergency with
a live P1, ck123 in a considered cycle. ⚠️ **What you SHOULD check is that the
gates survived it.** Re-arming a fix on top of a gate is the design; a gate
quietly removed to make a repair work is a finding, and it would also break the
1.0.7 decline (ck118).

⛔ **F-10 has an UNREAD PREMISE and the ruling did not change that.** Whether a
`rfSuspended` request still reports a positive `GetTargetAmount` is C-side and
nobody has established it. The module ships repaired either way — but if the
close-out or any patch-note line implies the defect was *confirmed*, that is a
finding. A ruling settles what we do, never what is true.

⭐ **04 WAS SPLIT into `04` (group B + the F116 edit) and `04b` (group C), before
either half ran** — pre-authorised by the owner under rule 4, not a failure to
finish. ⚠️ **Audit the two halves as ONE body of work** and check nothing fell
down the gap: all six modules landed somewhere, `04b` carried a real inbox rather
than a pointer, and neither half quietly dropped a module it assumed the other
had. ⛔ If a third link (`04c`) appeared for F-9, the same applies — that too was
pre-authorised, and a single-module link is a legitimate shape here.

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

35 modules should be untouched except for their `SRC:`/`DEFECT:` stamps and
**two named exceptions**. Diff them. An unexplained change to a KEEP module is a
finding.

**The two expected exceptions — anything else is a finding:**
1. `GeneForging`'s A-1 edit.
2. ⚖️ **`Fix_TrackSalvageWipe` (F116, `K-11`) — a REAL body edit, added to
   `04`'s fence on 2026-09-08 after the owner ruled ck111 + ck119.** Two changes
   only: the orphan loop rehomes instead of deleting, and post-split processing
   covers a track holding both completed and under-construction elements.
   ⛔ **Anything else changed in that module IS a finding**, including a
   re-derivation of the parts the `K-11` KEEP verdict already settled.
   ⚠️ **CORRECTED by link 04 (2026-09-08): the `SRC:` hash did NOT need
   re-taking and MUST NOT be.** It pins the SHIPPED body
   (`TrackElement.lua:467-618`), not ours, so a module-side edit cannot move it;
   `--pin` re-run after the edit emitted the identical `7466b940…` and the module
   reads OK either side (link 04's `fc318c7` records both runs). The check that
   actually catches a wrong edit here is a diff of OUR module against `e2490f3`:
   expect exactly the two ruled changes in the split branch plus the rewritten
   header block, and treat anything else as a finding. ⛔ A "re-stamp" on a
   module-side edit is the one move `FIX_POLICY` §2b forbids by name — re-pinning
   to make a BODY-CHANGED go away — so do not reintroduce the instruction.
   ⛔ **Do not treat the owner's ruling as making the change correct.** The
   ruling settled *whether* to do it; whether the code is right is yours. It has
   never run in a game, F116 has never been reproduced, and the module is
   destructive and save-persistent — it creates `TrackBase` objects that persist
   in saves, so a botched rehome loop re-creates F91's invisible-shell harm.

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

## 12 · YOUR LAST JOB — author `100_DOCSWEEP.md`

⚖️ **Owner instruction, 2026-09-08:** the doc sweep for this patch is a
**self-consuming prompt that YOU write, as the final act of this audit, and that
fires AFTER you.** ⛔ Not before — *"we need the audits results."* Your findings
are half its input; a sweep authored earlier would be sweeping against a
description of the patch rather than the audited fact of it.

⛔ **This does not change §1.** The folder-empty gate is a reading you take when
you START — every upstream link consumed. `100_DOCSWEEP.md` is created at the
END, by you, and is the one file permitted to outlive this audit. A later reader
finding `99` + `100` + `README` has found a chain that finished correctly, **not
a DO NOT SHIP.** Say so in the README row so nobody trips on it.

**Template: `prompts/PUBLIC_SURFACE_SWEEP.md`** — the standing sweep, run
"whenever a fix is added, retired, or materially re-scoped". Use its structure
(site → store cards → `metadata.lua` → reporter → close the loop → condensed
checklist) and its rule that **the bug entry is authority and every public
surface is derived from it, never the reverse.**

⛔ **But it is a TEMPLATE, not a form to fill in, and the reason is structural:
that sweep is written for ADDING one fix. This patch REMOVES ~36 and re-arms
several.** Its whole §0 logic — "does this fix have a player surface at all?" —
inverts. The questions your prompt must ask instead:
- what did a player SEE that they will no longer see, and how is that said
  without reading as a capability loss? (`02`'s framing: the game fixed these
  itself, and a fix duplicating the game's own is a risk with no benefit);
- which surfaces named a fix that **no longer exists**;
- which counts were derived from the fix list and are now wrong.

### ⚠️ Known-false surfaces to seed it with — but RE-CHECK THEM FIRST

⛔ **This section used to say "already found, do not re-derive". That was wrong
by the time link 06 ran, and the correction is the point.** `06`'s fence is
`metadata.lua`, `STORE_CARD_LIVE.md`, `UPLOAD_WORKFLOW` §3 and the site's
`fix-list.md` / `faq.md` / `index.md` — **exactly the surfaces named below.**
⇒ **Read `06`'s outbox and the current files before seeding anything.** A seed
that was true when written and is false when used is worse than no seed: it
sends `100` hunting surfaces someone already fixed, and "do not re-derive" would
have stopped it noticing.

⭐ **The general form, worth carrying into your verdict:** a hand-off note is a
claim with a timestamp. When the thing it describes is inside a LATER link's
fence, the note's shelf life ends when that link runs.

**As found on 2026-09-08** (state at that date, not necessarily now):
`F108` (`ExtractorStaffedPerformance`) and `F107`/`F105` (`LandscapeCostRefresh`)
were **named on the store cards and the site while both modules are gone.**
Link 02 removed the fix-list entries and filed the exact lines and wording for
the rest rather than editing across a fence. ⚠️ **Two different clocks, and the
sweep must not conflate them:**
- **the site is LIVE and WRONG NOW** — its FAQ and index pages still name removed
  fixes, and the deployed page is public today;
- **the store cards and `metadata.lua` become wrong ON UPLOAD** — they still
  describe v5, which really does contain those modules.

⇒ ⭐ **Say plainly in your verdict whether the live-site half should be fixed
BEFORE the upload or with it.** That is a real sequencing question and it is the
owner's to answer, not the sweep author's to assume.

### What the prompt you write must be

1. A **first-class chain member** — full inbox (⛔ a real copy, not a pointer:
   `99` is deleted on its own close-out), a README row, and rule 2's close-out
   (`git rm` itself, strike its row).
2. Carrying **your audit's findings**, especially Pass F's, verbatim enough that
   its session does not have to re-derive them.
3. ⛔ Naming the **count** discipline: `python tools/doccheck.py --emit-counts`
   and a recount from the deployed fix list. Never a hand-typed number, and
   never a count carried forward from before the deletions.
4. ⛔ Bound by `H-02` — no upload, no `version` edit, no Mod Editor. `EF-054` /
   `FIX_POLICY` §8 — never name fredware's mod, no load-order advice.
5. Explicit about the `UPLOAD_WORKFLOW` §3 **paste backups**: they are the real
   delivery path, auto-fill has never produced a clean page in two cycles, and
   they must be re-synced with `metadata.lua` in the same commit.

## 13 · Close-out

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
- ⚖️ **ck111 is now RULED and IS this chain's to close — this note has changed.**
  It previously read "open and unruled … not this chain's to close". On
  2026-09-08 the owner ruled it (b): ADOPT vanilla's policy — rehome the orphaned
  track fragment instead of deleting it — and folded the work into `04` §7, with
  **ck119**, a SECOND F116 divergence that had no ticket at all until the same
  ruling (post-split processing skips a track holding both completed and
  under-construction elements). ⛔ A third part was ruled too: the module's
  `OnMsg.LoadGame` sweep **KEEPS deleting** orphans (no split context at load;
  legacy debris only) — that is a RULING, not an oversight, and reopening it is
  a finding, not diligence.
  ⚠️ **The session that filed ck111 recommended the OPPOSITE (keep-and-defer) and
  reversed itself.** Stated plainly because you are told to treat the chain's own
  shape as auditable: the bug did not change, the machinery did — `bodycheck.py`
  did not exist, there was no body-copy link, and there was no terminal audit
  when the original recommendation was written. ⭐ **If you think that reversal
  was wrong, say so** — a ruled decision is still a decision someone can have
  talked the owner into, and the harm on the other side (untested changes to
  destructive save-persistent code) is real and has not gone away.
- ⛔ **ck119 is the process finding worth a line in your report, separate from the
  code.** It was fully documented in `bugs/F116.md` and in the module header, and
  still invisible to every surface anyone plans work from — no checklist item, no
  STATE line, no chain link — until it was looked for deliberately. The owner's
  stated goal for this patch is "everything we know about, fixed in this patch".
  **Ask what else is in that category:** a known divergence recorded only in a bug
  entry or a code comment is, operationally, not known at all.
  ⭐ **Answer it with a MECHANISM, not a list** (sharpened by the chain's author
  after review). The root cause is structural: the defect record (`bugs/`, module
  headers) and the surfaces anyone plans work from (the checklist, `STATE`, a
  chain folder) **are connected by nothing but a person remembering**. A list of
  what leaked this time decays the moment it is written; something that makes the
  next leak impossible — or at least noisy — does not. ⚠️ A count is the weaker
  deliverable here, so if you can only produce one, produce the mechanism and say
  the count is unknown. ⛔ And do not assume the answer is a new tool: "every
  deliberate divergence gets a checklist number at the moment it is recorded"
  would have caught ck119 with no tooling at all.
- ck118 is ruled: 1.0.7 players are served by a frozen v5 GitHub release plus a
  site page, both live. The store-card line pointing at it is link 06's.

### From link 01 — core, tooling and the manifest

⚠️ **For you specifically:** items 6, 7 and the closing paragraph are the claims to attack. Item 9 is drift caught in my own work, recorded per chain rule 5. Item 4's honest limit — no 1.0.7 game body exists to hash — is the one I would test hardest.

*(From link 01, `smr-bugfixpack-25`, 2026-09-08. Commits `6d452a3` probe form ·
`401f8a0` bodycheck.py · `6db7457` FIX_POLICY §2a/§2b · `e2490f3` KEEP set
stamped. ⛔ Nothing was run in a game; no status moved.)*

**1 · The `probe` form — exact signature and semantics** (`00_Core.lua`,
`SMRFixPack.Require`). `{ probe = function() … end, reason = "…" }`, a sibling of
`test`:

* The probe takes **no arguments** and runs under `pcall`.
* **ONLY the literal boolean `true` applies.** A throw, `nil`, `false`, or any
  other value (a captured table included) **declines**. "Captured nothing" is
  UNKNOWN and UNKNOWN is not permission.
* A throw is a DECLINE, never propagated. It is logged as
  `<id>: behaviour probe declined (threw: …)` so an authoring error in the probe
  cannot hide inside a silent decline.
* A probe failure returns `c.reason`, exactly like every other form, and does
  **NOT** set `update_suspect` — it is a behaviour verdict, not patch rot, and on
  the other branch a decline is the CORRECT outcome.
* Write the **stub contract beside it**: a comment naming what the stub must
  provide and why the target is safe to call on one. ⛔ Only for targets you can
  show, from the shipped 1.1.0 body, to be **synchronous and side-effect-free on
  a stub**. If you cannot show both, the module gets no probe and keeps its
  existing check — that is a permitted outcome, not a failure.
* Two shared lines were touched and both are identity for every existing form:
  `local ok, name` → `local ok, name, why`, and the return → `c.reason or why or
  (name .. " not found …")`. No existing reason string was reworded.
* `Require` is a plain function, so a `DataPatch` module may call it from inside
  its pass, after `DataLoaded`, for a preset-bound probe.

**2 · The branch guard, and it is not negotiable** (`FIX_POLICY §2a` — link 04,
this is Job D's answer verbatim). ⛔ **Do not build a game-version detector.** It
would be a LABEL check, against the rule that made the F115 gate correct; and it
is unbuildable anyway, because `lua_revision`, `ModMinLuaRevision` and
`ModRequiredLuaRevision` are ALL 350453 on both branches (`EF-077`) — which is
precisely why nothing warns a 1.0.7 player. There is no field to read. ✅ **The
per-module `probe` IS the branch guard**: a probe confirming the 1.1.0 body shape
a module was written for necessarily declines on a 1.0.7 body, per module, with
no version arithmetic anywhere and nothing global to keep in sync.

**3 · The manifest grammar** (`FIX_POLICY §2b` has the authoring rule;
`tools/bodycheck.py`'s docstring has the machine half). Header-block comments:

```lua
-- SRC: <path> <selector> sha256=<64 hex>      -- or:  -- SRC: none <reason>
-- DEFECT: <python regex>                      -- or:  -- DEFECT@<path>: <regex>
```

* `<path>` slash-separated, relative to `ModTools/Src` (`\` accepted).
* `<selector>`, no spaces: `Class:Method` (separator is a hint — both declaration
  forms and `Class.Method = function(` match), a bare `Name` for a global or
  `local function`, or `L<first>-<last>` for a literal span where there is no
  function to name.
* Body = declaration line → first bare `end` at the same indentation. The
  delimiter is `luafn.py:find_bodies`, **imported** by `bodycheck.py`, so there is
  never a second extractor. Line endings normalised, trailing whitespace stripped
  per line; indentation and comments kept; sha256 of the utf-8.
* `-- DEFECT:` searches the body of the `SRC:` above it. `-- DEFECT@<path>:`
  searches that whole file — the **DataPatch shape**: no body to hash, so declare
  `SRC: none` and state the defect against the shipped DATA.
* Several `SRC:` lines per module are fine; each `DEFECT:` binds to the nearest
  above it. Regexes are Python `re`, ONE line, **not** `re.MULTILINE` (`^`/`$`
  will not do what you want — use `\s+` to cross a line break). Shipped Lua
  indents with **tabs**: write `\s+`, never a literal space.
* ⛔ **State the DEFECT, never the PHRASING.** See item 5.
* ⛔ Never hand-type a hash: `python tools/bodycheck.py --pin <path> <selector>`
  emits the line and the range it hashed.

**4 · `tools/bodycheck.py` — CLI and what its falsifier proved.**

```
python tools/bodycheck.py                 # the pack against the live 1.1.0 tree
python tools/bodycheck.py --src <path>    # another ModTools/Src
python tools/bodycheck.py --code <path>   # another Code/ tree
python tools/bodycheck.py --all           # also print OK / NO-MANIFEST rows
python tools/bodycheck.py --module NAME   # one module
python tools/bodycheck.py --pin <path> <selector>
python tools/bodycheck.py --selftest      # ⛔ the falsifier
```

Exit 1 on `BODY-CHANGED`, `DEFECT-GONE`, `TARGET-ABSENT`, `TARGET-MULTI`,
`MALFORMED`; counts only for `NO-MANIFEST`, `NO-DEFECT`, `SRC-NONE`, `OK`.
⚠️ Deviation from the prompt, stated: `TARGET-ABSENT`, `TARGET-MULTI` and
`MALFORMED` also exit non-zero, not just the two named. A stamped module whose
target vanished, resolves ambiguously, or whose manifest does not parse cannot be
re-verified, and a manifest that merely *looks* like coverage is worse than none.

`--selftest` asserts ten legs, permanently, because a tool that returns GREEN on
everything is indistinguishable from a broken one. **Two legs are real game-side
events**: `DEFECT-GONE` fires on one of the actual 32 (`MinDaysFoodSupply
BeforeNotification` is gone from the whole 1.1.0 tree while
`ResourceTracking:GatheredResourcesOnHourlyUpdate` still exists with our arity —
invisible to `Require` and to `sigcheck`), and `TARGET-ABSENT` fires on
`Colonist:UpdateSatisfaction`, which 1.1.0 deleted. `BODY-CHANGED` fires on a
**real body edit** — F116's in-body repair at `add94b3`, pinning the pre-repair
body against the repaired tree — plus a hash negative control and the converse
leg, so it cannot pass by being always red.
⛔ **ONE HONEST LIMIT, in the file itself:** the 1.0.7 tree is GONE from disk
(`EF-075`), so no true 1.0.7-vs-1.1.0 **game** body pair exists to hash. The
mechanism is proven on a pack-side edit and a negative control, not on a
game-side branch pair.

**5 · The finding that will bite you if you skip it.** Writing the tool's OK
control walked straight into the trap. F46's 1.0.7 phrasing was
`station.demand[res]:GetTargetAmount()`; 1.1.0 hoisted it to
`local demand = station.demand and station.demand[res]` / `demand:GetTargetAmount()`
(`Train.lua:794-795`) — a pure **refactor**, defect untouched. A `DEFECT:` pinned
to phrasing therefore reports `DEFECT-GONE` for a bug that is still shipped: a
FALSE "vanilla fixed it", the direction that **retires a live fix** (R-15's
shape). The right expression states the fault — `Min\(carried,\s*station_cap\)`,
the unload computed from the cap alone. Locked in as fixture `Fix_Selftest
RefactorTrap`. ⚠️ **A `DEFECT-GONE` is a REMOVE candidate, never a verdict.**

**6 · What is stamped, and what "verified" means here.** All 35 KEEP rows (§1d),
76 manifest rows, 73 `OK` / 1 `NO-DEFECT` / 2 `SRC-NONE`, exit 0. ⛔ The FIX and
REMOVE sets are deliberately **unstamped** — 46 `NO-MANIFEST`, which is a count,
not a failure, until the pack is whole. Every hash was taken from the live tree,
so "the hash matches" is true by construction and proves nothing; its value is
future. What IS evidence: each target was resolved in the shipped tree and its
DEFECT expression written against the 1.1.0 body and confirmed to match there.
Three targets had moved far enough that the module's own 1.0.7 header no longer
describes them (`GetRareTraitChance` is now 5 lines through
`Techs.GeneSelection:ResolveValue`; `TunnelBase:AddPFTunnel` guards
`self.linked_obj`; `AlienDigger:GameInit` sits at `:87-96`).
⛔ **NOT a claim that the KEEP set is verified** — I pinned bodies the
re-verification read and re-read only what a defect expression needed. No KEEP
verdict was re-derived; K-9 and K-10 stay "on record, not re-read".

**7 · The named exceptions — a defect that is an ABSENCE cannot be stated
directly**, because a regex matches what is present:

| module | why | what was pinned instead |
|---|---|---|
| `Fix_SinkholeIndestructible` | missing `indestructible` / `disasters_strike_immunity` on a generated class table | the whole classdef by span (`L4-25`), so vanilla ADDING the flag reads as `BODY-CHANGED`. The one `NO-DEFECT` row |
| `Fix_BrokenTrackSalvage` (1st target) | `node_idx` missing from the parameters copied onto the repair site | the consequence, against the sort that raises (`a.node_idx < b.node_idx`) |
| `Fix_GeneForging` | `GeneForging` is unknown to `GetRareTraitChance` | the half that IS present. `DEFECT-GONE` will not fire if vanilla adds the tech alongside `GeneSelection` |
| `Fix_FreedHousingNotice` | `RemoveResident` wakes nobody | its tail (`ResetFreeSpace` as the last act), so adding the wake call stops the match |

**8 · Filed, not fixed (out of my fence).**
* **→ link 05:** `bodycheck.py --selftest` is NOT wired into `doccheck.py`; it is
  a manual gate today. Wiring it (alongside `harvest --check`) is the tools-tail
  fence, not mine.
* **→ link 06:** the inherited `metadata.lua` comment claiming "`PackVersion`
  renders version_major.version_minor.version" describes nothing that exists in
  the 1.1.0 tree (zero grep hits). Passed on from link 01's own inbox, still
  unfixed.
* `sigcheck.py` rated `Fix_TrackSalvageWipe` OK both before and after F116's
  defect was found. `bodycheck.py` is the instrument that closes that, and F116
  is now one of its falsifier legs — but only pack-side (see item 4's limit).

**9 · Drift caught in my own work (chain rule 5 — evidence, not shame).**
* The first block-balance checker counted a `for … ipairs({` whose `do` sits on a
  later line as **two** openers and flagged `Fix_RocketInteractGuard`, which is
  byte-identical at HEAD. Caught by checking HEAD before believing it. Fixed to
  pair each loop head with its own `do`, re-falsified against a deliberately
  broken copy; all 81 `Code/*.lua` balance 0. ⚠️ There is no Lua binary on this
  rig — block balance is the whole desk syntax check, so a wrong checker is a
  wrong gate.
* My first `EXPECT` sets in `--selftest` were wrong twice (a stamped fixture
  yields a row per manifest LINE, not one per module). The tool was right both
  times; I corrected the assertions, not the tool.
* Stamping wrote the 35 files LF where the working tree is CRLF. Content in git
  is unaffected (`git diff` = 35 files, 353 insertions, 0 deletions), but the
  repair pass converted **39 files I had not touched**; they had zero content
  diff and were restored with `git checkout --`. ⚠️ If you see EOL-only churn in
  `Code/`, that is where it came from, and it is not in any commit.

⛔ **What may NOT be claimed from this link.** Not "the pack is update-proof" —
class (c), semantics moving under a wrapper, is still seen by **nothing**. Not
"the KEEP set is verified". Not "probes are safe" in general. No status moved: a
tool run is not a test.

### From link 02 — the REMOVE block (36 deleted, 1 half-edited, 1 kept)

*(Link 02, `smr-bugfixpack-11`, 2026-09-08. Commits `2dc1dbe` the 36 deletions ·
`f707903` R-7 + the F03 pass · `9b0b82c` 43 bug entries · site `7cef4f3`.
⛔ Nothing was run in a game; no status moved.)*

**The three rulings that unblocked this link, because they bind you too.**

* ⚖️ **ck98 = DELETE, not gate.** Owner, verbatim: *"I am fine with the 1.0.7
  issue, we are giving a path which we don't have to do. The main mod serves the
  current patch period."* There is no 1.0.7 line in the live pack.
  ⛔ **This does NOT relax ck118's constraint on the re-copies.** Our
  `lua_revision` and 1.1.0's minimums are all 350453 (`EF-077`), so hotfix 2
  installs on a 1.0.7 rig with no warning of any kind. Delete-not-gate is a
  ruling about the REMOVE set only; a re-copied 1.1.0 body applied on a 1.0.7
  function is still the F114 failure mode in reverse.
* ⚖️ **ck117 = KEEP `90_SaveSanitizer`** (F35 + F48). It is NOT in the deletion
  set and its `items.lua` entry stays. Only the dead F03 pass was removed.
* ⚖️ **ck120 = the owner's general principle, and it is worth applying to your
  own calls:** *"we fix anything negatives, a small positive I am not as
  concerned about."* That is what killed the F-5 save cleanup — the stranded
  Astrogeologist +10% is an unearned bonus, so it is not chased. A **loss** is a
  different matter and gets fixed.

**What is now true of the tree.** `Code/*.lua` 81 → **45**; `items.lua` 81 → 45;
`metadata.lua`'s `code` list 81 → 45 (all three, per `H-10`); modules 80 → **44**
registered. `bodycheck.py` NO-MANIFEST **46 → 10**, which is link 01's predicted
landing point and is your free cross-check that the right set left.

**Expected boot-log consequence, for you to check.** Every one of the 36 removed
modules should be **absent** from the `[CommunityFixPack]` block — not `inactive`,
absent. `90_SaveSanitizer` and `Fix_DroneTransportMinors` must still be PRESENT.
Use `tools/logscan.py --build <id>`; a hand-rolled grep undercounted throws 30 vs
157 on 2026-09-08. ⛔ A log copied while `Mars.exe` is running is a PARTIAL log.

**Drift evidence, per the brief's instruction to capture it either way: ZERO
flips in 37 re-derived rows.** The QA flipped none in 46 and I flipped none in 37,
which is now two independent passes agreeing. One row LOOKED like a flip and was
not: R-14's citation failed to reproduce under my first grep because rains use
`GameTimeRepeat`, not `MapGameTimeRepeat` — my pattern was wrong and the record
was right. Worth keeping as evidence that a "flip" needs a second look before it
is reported as one.

**Drift caught in my own work (chain rule 5 — evidence, not shame).**
* ⛔ **I committed another session's in-progress files.** `git add -A` in a tree
  with concurrent sessions swept four of `smr-bugfixpack-a5`'s unstaged docs into
  my deletion commit. Caught immediately from the CRLF warnings, undone with a
  soft reset before any push, and re-committed by explicit pathspec. **The shared
  git INDEX is shared state in this tree, not just the working files** — a5 hit
  the mirror image of this from the other side. ⇒ In this repo, `git add -A` is
  unsafe; name paths. Worth a standing line in the chain method.
* **My first block-balance checker flagged 16 byte-identical files.** Same trap
  link 01 recorded, reached by a different route: regex comment/string stripping
  merged lines. I replaced it with a real lexer and gave it a 12-leg falsifier
  (keywords inside strings and long comments, `for`/`do` double-counting,
  `repeat`/`until`, `elseif`). All 45 files balance 0. ⚠️ There is no Lua binary
  on this rig, so this IS the whole desk syntax check — the checker is the gate,
  and a wrong checker is a wrong gate.

**Filed, not fixed — please confirm these were routed rather than dropped.**
* **`C54` — I FILED THIS AND THEN REFUTED IT THE SAME DAY. Do not re-open it, and do not count it as an
  owed run.** I read 1.1.0's `SavegameFixups.RemoveLeakedUpgradeModifiers` ending on an unguarded
  `ipairs(leaked)` and called it a candidate defect because vanilla guards `ipairs(x or empty_table)` in 36
  other places. ⛔ **That was a ONE-SIDED COUNT** — I never counted the unguarded sites, of which there are
  18 of the identical shape in shipped `Lua/`+`CommonLua/` (`Cooldown.lua:239-252` and
  `Notifications.lua:430-437` read in full; both leave the local `nil` in the ORDINARY case), plus 28+
  `ipairs(self.<field>)` sites where the class default is `false`, including the grid code. And `EF-005`
  already said so: *"Engine Lua tolerates `#nil`/`next(nil)`/`ipairs(false)` … don't report/fix
  nil-iteration as crashes."* I had not consulted the facts index before filing.
  ⇒ **Two process findings for you, both mine, both cheap to check for elsewhere in this chain:**
  (1) an asymmetry argument needs BOTH sides counted before it is evidence;
  (2) `agent/facts/INDEX.md` must be consulted before any engine-semantics claim is filed.
* **Dangling citations in files outside my fence**, all comments, none live code:
  `00_Core.lua:239` (cites `Fix_LastTransmissionStorage` as a donor) and
  `:304-305` (cites `Fix_AstrogeologistExtractors:174` and
  `Fix_IndependenceTerraforming:128`); `Fix_CrystalMysteryHang.lua:39,76`,
  `Fix_ExtenderFlapChurn.lua:48,93` and `Fix_TrackConnectorPingPong.lua:91,185`
  (all cite `Fix_MeteorStormWedge:154/:165` as a precedent);
  `Fix_SaintBlessing.lua:146`.
* **A gap in `doccheck`:** it reported GREEN while `metadata.lua`'s `code` list
  still held 81 entries and `items.lua` held 45. It counts them but does not
  cross-check them against each other — and `H-10` is the hazard about exactly
  that inconsistency. Link 05 owns the tools tail.
* **A fact worth recording that is not yet one:** Steam allows only ONE branch
  selected per install at a time (owner, 2026-09-08), so the rig cannot hold 1.0.7
  and 1.1.0 simultaneously. That is a standing constraint on every future
  re-verification, and it means `EF-075` stays true unless 1.1.0 access is given up.

⛔ **What may NOT be claimed from this link.** Not that the removed fixes were
never needed — they were correct on 1.0.7. Not that removal is verified safe — it
is verified in SOURCE; nothing ran. Not that no player is affected — a 1.0.7
player who updates loses 36 fixes. No status word was moved on any of the 43 bug
entries, including the three that deletion resolves (F111/F112/F113), because no
boot log has been taken since.
### From link 03 — the applies-today repairs: what changed, what the probe decides, and what has NOT been exercised in play

*(Link 03, `smr-bugfixpack-91`, 2026-09-08. Commits `3db4984` F-1 · `f38d6d2` F-2 ·
`19b5aaa` F-3. ⛔ **Nothing was run in a game. No status word moved on any of the
three bug entries.** `Code/*.lua` is still 45 files / 44 registered modules — this
link added and removed none, so `H-10` is untouched and `items.lua` /
`metadata.lua` were not opened.)*

#### Per module: what changed, what the self-check decides, what is unexercised

**F-1 `Fix_SaintBlessing`** (entry F92, `3db4984`)
* **Changed.** A behaviour probe now decides the branch, and a **second** one-shot
  save re-base was added for the 1.1.0 branch. The data rewrite is unchanged on the
  1.0.7 branch.
* **What the probe decides.** It calls the shipped
  `TraitPreset:AddDomeColonistsModifier` on stubs and reads back the label it filed
  under. Raw value ⇒ 1.0.7 ⇒ apply. Resolved label ⇒ 1.1.0 ⇒ decline the rewrite and
  arm the re-base. **Anything else, including nothing ⇒ UNKNOWN ⇒ do nothing at all
  and latch.** Two `Require` probes, not one inverted probe, precisely so UNKNOWN
  cannot fold into a branch. On 1.1.0 the expected verdict is DECLINE-and-arm.
* **⛔ NOT EXERCISED IN PLAY.** Nothing here has been run. Specifically unexercised:
  (i) the probe has never been evaluated in a live game — the stub contract is
  argued from the shipped body, not measured; (ii) the re-base has never touched a
  real save; (iii) the UNKNOWN branch has never fired, by construction. The owner
  control is checklist-batched and unrun.
* ⚠️ **The module stays `active` on 1.1.0 while patching nothing.** That is
  deliberate — the healing job is real and `WhenActive` requires `active` — but it
  means the boot log's active count is not evidence that a data patch happened.
  Read the module's own line instead: on 1.1.0 it says *"the shipped code resolves
  the trait label itself — data left untouched; save re-base armed for N preset(s)
  of M"*, which is a different string from the 1.0.7 *"corrected N … of M"* line.
  ⭐ Once the installed base has loaded once with this build the module is a REMOVE
  candidate. Recorded on the entry, deliberately not decided.

**F-2 `Fix_StaleReservations`** (entry F58, `f38d6d2`)
* **Changed.** One clause: a colonist whose `expedition_residence` is truthy is
  exempt from the **age** branch of the `NewDay` sweep. The invalid / desynced /
  dying branches deliberately still fire. Plus an honest header correction (below).
* **Self-check.** Unchanged — the existing `Require` existence pair. No probe: the
  module gains no 1.1.0 body shape, it is a post-wrapper reading fields present on
  both branches. ck118 does not bite it.
* **⛔ NOT EXERCISED IN PLAY.** No expedition has been run with this build. The
  residual we accepted is also unmeasured: a colonist lost permanently on an
  expedition while still a valid object now holds their home forever.

**F-3 `Fix_ShelterReflex`** (entry F73, `19b5aaa`)
* **Changed.** Half (a) — the `MicroGHabitatAutoResolve:IsSuitable` replacement —
  **deleted**. Half (b) kept byte-identical. One reason string reworded, because it
  named a target the module no longer touches; flagged in the file, since reason
  strings are otherwise preserved byte-for-byte.
* **Self-check.** No probe, and the file says why explicitly rather than leaving it
  implicit (§4 of the brief): half (b) carries no 1.1.0 body, so there is nothing
  for a branch guard to decline.
* **⛔ NOT EXERCISED IN PLAY.** The throw this removes has never been reproduced —
  it is source-derived, and its trigger (a trait filter set on an asteroid habitat)
  is why our own playtesting never hit it. The owner control is the first attempt to
  see it.

#### ⛔⛔ TWO TEST KIT PROBES WILL NOW REPORT A FALSE `FAIL` — filed, not fixed

The Test Kit is a separate repo and outside link 03's fence, so both were left
alone. **This matters to your verdict**, because a suite run is one of the
instruments a ship decision would lean on and two of its rows are now lying:

* **`SaintBlessing`** (`TestKit/Code/57_Probes_Wave8.lua:139-143`). Its static half
  asserts `saint.modify_trait == GetTraitLabel("Religious")` — i.e. that we
  rewrote the game's data. On 1.1.0 we deliberately no longer do. ⇒ **FAIL while
  the fix is correct.** Its *live* half (do the dome Saints carry the modifier
  under the resolved label) is exactly the right check and is the half that should
  be kept.
* **`ShelterReflex`** (`TestKit/Code/20_Probes_Wave2.lua:182-196`). It stubs a
  habitat with `GetScoreFor = function() return 0 end` and asserts
  `AR.IsSuitable(blipped, colonist)` is true — the behaviour we **deleted on
  purpose**. ⇒ **FAIL for a half the pack no longer claims.** The file's own F61
  precedent says a probe that tests removed behaviour goes with the fix.
* `StaleReservations` (`:679-708`) was checked and is **unaffected** — its stub path
  through 1.1.0's `ReserveResidence` still works and it should still pass.

⚠️ The owner has been warned about both on the checklist, in the same block as the
three controls, so a suite run cannot be misread as a regression.

#### Drift caught in my own work (chain rule 5)

* **The QA and the re-verification both named only ONE vanilla fixup.** There are
  **two**: `OrphanedDomeColonistsTraitModifiers` (`_fixup.lua:2138-2170`, the one
  cited) and `MigrateDomeTraitLabelModifiers` (`:2097-2136`, the 1.0.7→1.1.0
  migration, which also rehomes dome labels from `trait.id` to `GetTraitLabel`).
  **Both** call `AddDomeColonistsModifier` and **both** broke the same way under our
  wrong value. The re-base covers both because it keys on the missing entry rather
  than on which fixup ran, but the record was incomplete and now says so.
* **`colonist.traits` is a HYBRID set + array** (`Colonist.lua:493-495`:
  `traits[trait_id] = true` *and* `traits[#traits+1] = trait_id`). The existing
  1.0.7 heal walks it with `pairs`, so it also visits integer keys — inert, because
  `rebased_from[1]` is nil, but it is luck rather than design. The new 1.1.0 re-base
  uses `ipairs`, matching the shipped filing site (`Colonist.lua:441`) and both
  fixups.
* **A balance checker was needed for a third time and written for a third time.**
  Falsified in both directions before use (red on a truncated function; green on a
  file containing a multi-line `for … ipairs({ }) do`, the word `end` inside a
  string and inside a `--[[ ]]` block, and a `repeat … until`). 45/45 balance 0.
  Routed to 05 with the counting rule that survives falsification, since committing
  it is 05's fence.

#### Filed, not fixed — out of fence

* **→ 06 (and the doc sweep):** the site fix list's F73 card promises *"a habitat
  with a momentary life-support gap keeps its residents"*
  (`content/fix-list.md:182-184`, rendered `site/fix-list/index.html:996`) and calls
  the defect *"two things"* (`:178-180`). Only one survives. Same shape as F108 /
  F107 / F105.
* **→ 05:** `tools/harvest_wrap_targets.py:173-175`'s parenthetical describes the
  deleted `MicroGHabitatAutoResolve.IsSuitable` replacement.
  `tools/doccheck.py`'s `LOAD_ORDER_RULES` cites a `Fix_ShelterReflex.lua:70` that
  has moved (the rule itself is unchanged and still correct).
* **→ nobody yet:** `00_Core.lua:304` cites `Fix_AstrogeologistExtractors:174`
  (deleted by link 02) and `Fix_SaintBlessing:151` (moved by `3db4984`). Historical
  explanatory text, harmless, stale. 01 is consumed, so this has no owner — your
  call whether the doc sweep takes it.

#### ⛔ What may NOT be claimed from this link

* **Not "F-1 is fixed", "F-2 is fixed" or "F-3 is fixed".** Three source-derived
  repairs, zero game runs. The owner's 2026-09-08 rule binds our own notes too.
* **Not "saves are healed."** The F-1 re-base is untested until a save that loaded
  under the broken pack has been loaded again with this build.
* **Not "F-3 is now correct."** It is now **absent**, and 1.1.0 players get the
  vanilla behaviour, which still evicts a habitat's residents on a blip. That is a
  patch-note line and a stale site card, both routed.
* **Not "the probe form is proven."** F-1 is its first real use and it has never
  executed in a game. What is shown is that the target is synchronous and
  side-effect-free **on the shipped body as read**, and that the stub contract is
  written beside it. A tool run and a source read are not a test.
* **No status word moved**, on any of the three entries.
#### ⚖️ ADDENDUM from link 03 — the owner RULED the controls deferred (2026-09-08)

Ruled after 03 closed, so it postdates the block above and changes how you route
your own in-play controls. Owner, verbatim: *"Can the sitting be done after the
chain. I want to insure everything is green on this side and then we can check
the live side?"*

⇒ **ALL in-play controls merge into ONE consolidated sitting after link 99.**
Link 03's three (Saint blessing, expedition housing, asteroid habitat trait
filter) are on the checklist as **scheduled, not owed**. Route yours the same
way: file them in the checklist as usual, but present them as **joining the
post-99 sitting**, not as something owed now. ⛔ Do not open a second sitting.

Two things ride with it and both bind you:

1. ⛔ **A SHIP verdict from 99 is NOT clearance for the upload sitting.** It means
   the desk side is green; the controls sit BETWEEN 99 and the owner's sitting.
   `H-04` binds — never treat a future release as ready.
2. ⚠️ **⛔ DO NOT LOAD A SAVE THAT RAN UNDER THE BROKEN PACK.** The
   `SaintBlessing` save re-base is one-shot per save: the log line
   `SaintBlessing: restored N dome blessing(s) …` prints on the FIRST load of a
   poisoned save and never again. Any boot you take with a build carrying
   `3db4984` spends that evidence. 04/04b run nothing in a game, so this should
   not come up on its own — but if a leg of yours ever does load a save, **capture
   the full log** and say which save it was. ⛔ Do NOT copy a save as insurance
   (`H-06`: loading a copy runs that campaign's autosave rotation and deletes the
   owner's autosaves).

### From link 04 — the re-copies (F-6, F-7) and the F116 edit (§7)

*(Link 04, `smr-bugfixpack-ba`, 2026-09-08. Commits `3f8394b` F-7 · `177c7b2` F-6
· `fc318c7` F116 · the close-out commit carries this note. ⛔ Nothing was run in a
game; no status moved. 45 files / 44 modules unchanged; `items.lua` and
`metadata.lua` not opened.)*

**1 · Per module — what was copied, what was NOT carried, the decline condition,
and what has not been exercised (which, for all three, is everything).**

* **F-7 `Fix_RocketDroneChurn`** — the 1.1.0
  `CargoTransporterNew:UpdateCargoResourceRequests` (`CargoTransporterNew.lua:
  1430-1463`) with the F50 changes re-applied. Two-sided diff against the archived
  1.0.7 body: ONE line differs (the `not self.refuel_disabled` clause, `:1442`);
  our old copy's non-FIX lines matched 1.0.7 exactly. NOT carried: nothing.
  Decline: a `test` on `UniversalRocketBase.ToggleRefuel` + the `refuel_disabled`
  property (0 hits on 1.0.7). ⚠️ **Deviation from §4.3's "the per-module probe",
  stated:** a `test`, not a `probe`, because `TransportableResourceIds` is EMPTY
  at `ClassesBuilt` on a cold boot (`PreProcessResources` fills it on
  `DataChanged`, `Resources.lua:404-449`, `:492-500`) and a stub probe there reads
  UNKNOWN and kills the module every cold start. `FIX_POLICY` §2a admits the shape
  `test` where a probe cannot be shown reliable; the reason is in the file. If 99
  disagrees, the alternative is a probe run from a `DataLoaded` pass (the F-1
  shape), never a version check. Not exercised: the toggle, the hourly path, the
  drones.
* **F-6 `Fix_PayloadTemplateRefill`** — three bodies: `RetrieveRequests`
  (`:194-243`), the file-local `resolve_loc_cargo_template` (`:169-192`,
  reproduced), and `Apply` (`:368-385`, now a body copy instead of a pre-wrapper so
  the stamp can sit on the CONFIRMED path). All three 1.1.0 changes carried
  (destination-pick exemption, tutorial branch, automode nil-guard). ⚠️
  **Departure from the QA's pinned shape, stated:** the gate lives INSIDE the
  resolve, AFTER the `g_Tutorial` block, rather than around the resolve call in
  `RetrieveRequests` — same predicate, and the only placement where the tutorial
  return precedes it. Both confirmed branches stamp (mid-flight and `CmdLoad`);
  the cancel branch does not. NOT carried: the 1.0.7 `Apply`'s
  `target_spot`/`requested_spot` lines (gone from 1.1.0). Decline: a behaviour
  `probe` — the shipped `RetrieveRequests` on a stub with `prev_flight_data` and a
  stored request of 5; applies only if it files 0. Executed on BOTH shipped bodies
  under Lua 5.4: 1.1.0 files 0, 1.0.7 files 5. The stub contract is in the file
  (`table.find` returns on a nil array, `LuaExportedDocs/Global/table.lua:9-11`,
  so the nil-template path the probe takes is the shipped body's own everyday
  case). Not exercised: the dialog, a pick, the tutorial, the cancel path.
* **F116 `Fix_TrackSalvageWipe` §7** — ck111: vanilla's rehome loop (`:580-595`)
  replaces the F44 delete loop; a `tracks` list built from the sides that actually
  seeded. ck119: vanilla's tail (`:597-613`) with combined-list processing inlined
  through the already-Required `ProcessTrackElements` (= `TrackBase:
  ProcessAllElements`, `Track.lua:466-469`); counted loop instead of `ripairs`.
  NOT changed: anything else; the `OnMsg.LoadGame` sweep (ruled). No gate added —
  the latch/WhenActive trap from 03 is exactly why. Not exercised: everything;
  F116 has never been reproduced.

**2 · ⚠️ DRIFT IN MY OWN PROMPT AND IN YOUR PASS D, corrected (chain rule 5).**
`04` §7 trap 1 and your Pass D item 2 both said the `Fix_TrackSalvageWipe` `SRC:`
hash "had to be re-taken" after the edit. It cannot be: the pin hashes the SHIPPED
body (`TrackElement.lua:467-618`), not ours. `--pin` re-run after the edit emits
the identical `7466b940…`; the module reads OK before and after. Link 01's session
(`smr-bugfixpack-25`) reached the same reading unprompted. **I rewrote Pass D item
2's paragraph** so the audit diffs OUR module against `e2490f3` and expects exactly
the two ruled changes plus the header block. A false "re-stamp" instruction would
have a future session re-pinning to silence a BODY-CHANGED — the move §2b forbids.

**3 · ⭐ The 1.0.7 tree is back (`ad5f93d`,
`C:\Dev\SMR-SrcArchive\1.0.7.396349\Src`) and it changed what this link could
claim.** Link 01's outbox item 4 ("no true 1.0.7-vs-1.1.0 game body pair exists")
is out of date. `bodycheck.py --src <that tree> --module TrackSalvageWipe` →
BODY-CHANGED (pinned `7466b940…`, 1.0.7 body `fab72089…`, `:448-578`) — a real
game-side branch pair, RED as it should be. Both re-copies were diffed two-sided,
and `ProcessAllElements` = 0 hits on 1.0.7 (F116's premise, now verified). Link 25
offered to fold the 1.0.7 leg into `--selftest`; I left the tool alone (05's
fence) — 05/99 decide. ⚠️ The archive's `DLC/` subtree is NOT clean 1.0.7 (12
files vs 151; a Steam artefact of the branch switch); base-game paths are sound.

**4 · Desk controls, under a REAL Lua 5.4 — `lupa` is installed on this rig.**
There IS a Lua parser here, contrary to 01's and 03's "no Lua binary" notes (no
binary, but a Python-embedded Lua 5.4). The parse sweep is `load()` on every
`Code/*.lua`, falsified on a chunk missing an `end`; 45/45. Controls (scripts in
the session scratchpad, NOT committed — 05's call whether any becomes a tool):
the shipped 1.1.0 + 1.0.7 `RetrieveRequests` on the F-6 probe's stub (0 vs 5);
our F-6 copies through six cases (fresh 0 · stamped 5 · stamped+pick 0 · tutorial
rocket 2 stamped 7 · template-first-use 9 · template-stamped 0); the shipped 1.1.0
+ 1.0.7 + our `UpdateCargoResourceRequests` on a refuel-disabled stub (fuel demand
0/100/0; our disconnects 0 steady, 1 on a missing request); our
`DemolishAndSplitTrack` on a synthetic 6-element track with a broken expansion
link and a mixed track (orphan rehomed into a third track; three combined lists
processed; none under `skip_track_process`; one new track on a clean split). ⛔
Stubbed harnesses on synthetic input: they say the Lua does what was asked and
NOTHING about a real map.

**5 · Filed, not fixed.**
* Test Kit `PayloadTemplateRefill` probe (`30_Probes_Wave3.lua:11-70`) now
  FALSE-FAILs: it stubs `CreateRealTimeThread` to a no-op and expects `Apply` to
  stamp synchronously; the stamp is inside the thread's confirmed branch now. The
  owner is warned in the checklist (LINK 04 block). Third such probe after 03's two.
* `bodycheck.py`'s summary reports **no row** for a `SRC:` line that deliberately
  carries no `DEFECT:` (F-6 has two, F-1 one): the pack-wide `NO-DEFECT` count was
  1 before this link and is 1 after. Either the count keys on the module rather than
  the row, or those rows are silently OK — either way a deliberate no-defect pin is
  invisible in the summary. Cosmetic; 05.
* Link 01's outbox items 2 and 4 in `04` (and §4.3) read "the per-module probe" as
  the only admissible guard; §2a's own text admits the shape `test`. F-7 is the
  first module to need it, with the reason recorded. Worth one sentence in 05's
  `FIX_POLICY` pass if 99 agrees.
* My prompt's §9 says the in-play controls "for these three is everything" and
  routes them to the checklist as owed — the addendum's ruling (deferred to one
  post-99 sitting) supersedes that and was followed: rows 4–6 join link 03's rows
  1–3, no second sitting opened.

**6 · What may NOT be claimed.** Not "tested" — nothing ran in a game. Not
"matches vanilla" beyond what `bodycheck.py` says about the SHIPPED bodies and the
two-sided diffs say about our copies. Not "the gates are unnecessary". Not "F116 is
fixed" — never reproduced, and a desk harness is not a map. Not "F-7's decline is
proven on 1.0.7" — argued from 0 grep hits in the archived file, not from a boot.

**7 · ⭐ A link was ADDED to the chain after 04 closed: `07_TESTKIT.md`** (owner,
2026-09-08: *"Agreed, make the 07"*; authored by this session). The chain had no
owner for the Test Kit — every fence excluded it, 05's "In" list does not name
it, and you can only report — while ~40 of its 100 probes describe a pack that
no longer exists (37 target modules 02 deleted; 3 FALSE-FAIL on live modules; 3
pre-chain orphans; 2 sweep tables). ⚠️ **For your passes:** (a) the folder-empty
gate now waits on 07 as well; (b) Pass A's "re-run the instruments" should
include the kit's parse sweep 07 is told to build; (c) Pass C gains a runtime
half — 07's `retired` probes PASS on vanilla only if the REMOVE verdict was
right, so a FAIL there at the sitting is an R-15-shaped finding, not a probe
bug; (d) Pass G must hold the sitting to 07's PREDICTED suite census. ⚠️ **Audit
the addition itself** (CHAIN_METHOD §3): a chain that grew a row mid-run because
the owner asked a question is a decomposition miss worth naming, and 07's shape
(three units, self-split to `07b` at Unit A) was set by the session that found
the gap, not by a fresh reader.

### From link 04b (`smr-bugfixpack-94`, closed 2026-09-09) — group C: F-8, F-9, F-10, all three RE-ARMED on top of their gates

*(Commits `799f145` F-8 `LandscapeUnitFilter` · `3d4c933` F-10 `TrainCargoDumping` ·
`7a401f1` F-9 `VacuumWalks`. ⛔ Nothing ran in a game; no status moved. `Code/` still
45/44; `items.lua` and `metadata.lua` not opened. F-9 did NOT split to `04c`.)*

**1 · Per module — what was copied, what was not carried, the decline condition, whether
the probe is deliberate, what is unexercised** (§10 of my prompt, verbatim requirements):

| | F-8 `LandscapeUnitFilter` | F-10 `TrainCargoDumping` | F-9 `VacuumWalks` |
|---|---|---|---|
| 1.1.0 lines copied | `Landscaping.lua:509-523` + file-local `:505-507` | `Train.lua:779-805` | `Colonist.lua:1886-1983` (98 lines) |
| 1.1.0 changes carried | the ONLY two: `(map, mark, callback, ...)`, `map.Landscapes[mark]` | both nil-guards `:785-787`, `:794-795`; BlackCube hook `:800-802` | all seven: `need_work` slots on every committing branch; shuttle-owned skip `:1898`; `g_Consts` at call time; `-1`→`max_int`; `DiscardTransportTicket`; the five-rung task ladder; landing-slot `src_dome` search |
| deliberately NOT carried | nothing | nothing from 1.1.0. OUR helper dropped its `st.task_requests` read (its reason was 1.0.7's depot implementation; 1.1.0's `IsStoring` reads `demand[res]` + `rfSuspended`) — stated in the file | nothing |
| our diff vs shipped 1.1.0 | one line (`filter_embark` for `callback`) | one guard block after the cap read | one line (`or 0`) — mechanical diff confirms |
| APPLIES when | `MapVarValues.Landscapes` registered AND no `Landscapes` global AND the shipped fn asks a stub map's `Landscapes` for the probe mark | `MultiResourceDepotBase` declares `IsResourceEnabled` AND `BlackCubeMystery_AdjustStored` exists AND the shipped `UnloadAll` survives a storable resource with no demand entry (the F114 input) | `HasShuttleLandingSlots` + `Dome.ReserveWorkplace` + `Colonist.CancelWorkReservation` exist AND `const.Colonist.<walk consts>` are numbers AND the shipped fn calls `CanWork()` first |
| declines WITHOUT suspect (= 1.0.7) | `Landscapes` global present, no MapVar | no `MultiResourceDepotBase`, `UniversalStorageDepotBase` present | `const.ColonistMaxDomeWalkDist` a number, no `HasShuttleLandingSlots` |
| declines WITH suspect | every other decline | every other decline | every other decline |
| probe deliberate? | YES (new; the F115 shape test kept, sense inverted) | YES (new; the F114 shape test kept, sense inverted) | YES (new); the accidental path-spec gate is GONE |
| gate kept? | yes — same discriminator, inverted | yes — same discriminator, inverted | n/a (it was an accident); replaced by a deliberate one |
| desk harness | 5 branches: applies / 107 pre-game / 107 in-game / neither / 110-oldbody — all as designed | 4 branches + 6 functional cases (guard, not over-broad, no stranding, refab hatch, BlackCube hook, F114 input) | 4 branches + 5 functional cases vs the shipped body side by side |
| bodycheck | 3 OK; RED seen: BODY-CHANGED + DEFECT-GONE | 2 OK; RED seen both | 2 OK; RED seen both |
| unexercised in play | EVERYTHING — no landscaping site placed on 1.1.0 with this body | EVERYTHING — no train unloaded; none seen leaving its platform since F114 | EVERYTHING — vacuum walking never exercised on 1.1.0 |

**2 · F-10's premise (§4) is UNESTABLISHED and every surface says so** — the file header,
`bugs/F46.md`, `bugs/F114.md`, the checklist (row 10 = the console read), and 06's inbox
(no "fixed", no "confirmed"). Not cheaply establishable from Lua: `GetTargetAmount` has no
Lua definition outside `ResourcePile.lua:99`. Circumstantial only: 1.1.0's load side treats
stock at a disabled station as forbidden excess (`Train.lua:873`, `:897`, `:912`). If the
control reads 0, our guard is inert and F46 is a REMOVE candidate for the next patch.

**3 · Drift caught (chain rule 5 — evidence, not shame).**
* ⛔ **My prompt §2's 2026-09-08 "RE-CHECKED" note is wrong in the WIDER direction.** It
  says reach "really is Clear-Waste-Rock only — exactly one caller". The one call site
  (`ClearWasteRockConstructionSite.lua:81`) is a METHOD, and `LandscapeConstructionSite`
  is that class's SUBCLASS on both branches (`LandscapeConstructionSite.lua:4`), so
  flatten/raise/lower inherit it — the F115 stack trace in `bugs/F115.md` is itself a
  flatten site reaching `:81`. 1.1.0 moved the override UP a class; on 1.0.7 only flatten
  sites called this and clear-waste-rock used the hex sweep. **A caller count of a method
  must count its inheritors** — the F64 lesson applied to the other side. The note's own
  warning ("class X no longer defines Y is a statement about SELF-DECLARATION") was right
  and its conclusion still fell into the trap. §2/§9's "do not restate 20/20 because reach
  narrowed" rests on that; 20/20 is still not restated, but because it is a 1.0.7
  measurement, not because of reach. Recorded in `bugs/F34.md` and the checklist.
* ⚠️ My prompt §1: *"the gates … are what makes each module decline on 1.0.7"* —
  imprecise: as shipped they declined on **1.1.0**. I kept each gate by keeping its
  DISCRIMINATOR and inverting the sense (§2 anticipated it: *"that stops being true the
  moment you edit the body"*). ⚠️ **For your "a gate quietly removed" pass: an inverted
  gate is the kept gate.** Each file says so at the gate.
* ⚠️ My prompt §1 says "⚠️ 04 may still be in flight" — it had closed (`55b1d5e`) before
  I started; `ListAgents` showed no 04 session. No collision.
* `00_Core.lua:120-124` (the probe-form comment) illustrates a probe with
  `LandscapeForEachUnit(stub, cb)` whose THROW on 1.1.0 "IS the decline" — that is the
  probe-for-1.0.7 direction. The shipped probe probes FOR the 1.1.0 read (the direction
  §2a and 02's note require for a re-copy). Comment only, not wrong, but a reader could
  copy the wrong direction. One sentence for 05's core pass.
* Procedural: one Bash call (the F52 append + F-9 commit) failed at shell parse time and
  ran NOTHING — caught by `git status`, redone via files. The three earlier heredoc
  appends were checked afterwards and kept their backslash paths. Nothing lost.
* `sigcheck.py`: the F115 MISMATCH CLEARED with the F-8 edit (38 OK / 0 MISMATCH). STATE
  line "sigcheck MISMATCH there is CORRECT" evicted in my close-out commit. A
  re-appearance is a finding.

**4 · Method notes** (for CHAIN_METHOD / FIX_POLICY via 05 if you agree). The desk
harness (scratchpad, ~100 lines) loaded our module against the pack's REAL `Require`
(extracted from `00_Core.lua` with `luafn.find_bodies`) with the shipped 1.1.0 / 1.0.7
bodies standing in for the game — so one run per branch exercised the gate, the
three-valued marking AND the installed body. That is one step past link 04's
body-only harness and is what let me watch a probe throw and read as a decline before
any boot. Worth promoting to `tools/` as a fixture harness — out of my fence, routed to 05.

**5 · Test Kit (07's inbox has the detail).** All three modules now APPLY on the rig, so
their probes must run. `LandscapeUnitFilter` and `VacuumWalks` will `ERROR` as written
(old call shape; missing stub methods); `TrainCargoDumping` should PASS. Five named stale
results across the kit until 07 closes.

**6 · What may NOT be claimed.** Not "tested" — nothing ran in a game, and trains,
landscaping and vacuum walking have never been exercised on 1.1.0 at all. Not "matches
vanilla" beyond `bodycheck.py`'s pins and the mechanical diffs. Not "F-10 is fixed". Not
"the gates are unnecessary". Not "20/20". Not "the 1.0.7 declines are proven on 1.0.7" —
argued from the archived tree and the desk harness, never from a 1.0.7 boot.

**7 · Filed, not fixed.** `00_Core.lua:304` stale citations (from 03, still open). The
five stale kit probes (07). Nothing else out of fence was found.

### From link 04b's session, after close-out (2026-09-09) — the first cross-branch runs, now that the 1.0.7 tree is back

*(`smr-bugfixpack-94`, owner-requested: "any other checks now that 1.0.7 is on disk before I
fire 05". Commits: `42b9a17` (EF-083 + landscaping) and the one carrying this note. ⛔
Nothing ran in a game; no module changed.)*

**1 · `python tools/bodycheck.py --src C:\Dev\SMR-SrcArchive\1.0.7.396349\Src`** — every
pin hashes the 1.1.0 body, so BODY-CHANGED here = "target differs between branches".
28 rows: the 5 re-copies + `ShelterReflex` + `SaintBlessing` (TARGET-ABSENT) expected;
the rest KEEP. Classified by whether the module COPIES the target or WRAPS it, with a
mechanical diff of our body against both shipped bodies for every copy:

| KEEP module | target (branch diff lines) | technique | verdict |
|---|---|---|---|
| `TrackConnectorPingPong` | `CreateConnectorElements` (4) | body copy | on the 1.1.0 body; differs from 1.1.0 ONLY in the F66 guard block. ⚠️ see §2 |
| `TrackSalvageWipe` | `DemolishAndSplitTrack` (53) | body copy | F116, repaired in-body by 04; 4 of the 16 1.0.7-only lines still present verbatim in our file — your Pass D should say whether those are the deliberate FIX lines or residue |
| `DomeFreeSpaceMismatch` | pins `GatherFreeLivingSpaces` (13); COPIES `Dome:RefreshFreeLivingSpaces` (0) | body copy of an UNPINNED 3-line function | copied function identical across branches; the pinned helper changed but is called live. Coverage gap: the copied function is not the pinned one |
| `SinkholeIndestructible` | `L4-25` span (4) | data | formatting only (`}` placement) |
| `LayoutTechLock` | `Activate` (5: water markers) | WRAPPER (`orig_activate`) | carried |
| `RocketInteractGuard` | `CanInteractWithObject` (2: `MixedPoolStockpile`) | WRAPPER (`orig_can`) | carried |
| `GeneForging` | `GetRareTraitChance` (13: rewritten to 5 lines via `Techs.GeneSelection:ResolveValue`) | WRAPPER (`orig`, `SetGlobal`) | carried; our wrapper still passes `unit`, which the 1.1.0 body ignores — harmless. 05's A-1 stands |
| `AnomalyCaveInMap`, `BrokenTrackSalvage` (×2), `DestroyedTunnels`, `ExtenderFlapChurn`, `GhostFarmOxygen`, `JumboCaveReinforcementWedge`, `LakeEntombment`, `LanderEmptyLaunch`, `MirrorSphereSite`, `TrainsToVoid` | 12 / 8+53 / 4 / 4 / 6 / 8 / 16 / 9 / 4 / 2 | wrappers | change carried; class (c) exposure only |

⇒ **No new F116 shape in the KEEP set.** ⚠️ My first proxy (does the module define the
target's name) mis-flagged the two `orig_*` wrappers as copies; the real diff corrected it.
Recorded so nobody repeats the proxy without the diff.

**2 · THE ONE FINDING — `TrackConnectorPingPong` vs `SavegameFixups.ForceTrackReconnection2`
(NEW in 1.1.0, `TrackElement.lua:987-997`, 0 hits on 1.0.7).** The fixup rebuilds every
station's connectors with `"force"`; 1.1.0 relaxed the assert (`force or …`) for it.
Vanilla under force takes a contested hex from a live other building; our guard tests
`owned_by_live_other` BEFORE honouring `force`, leaves the hex, and that station gets no
connector there — F114's demoted "asymmetry" line, now with a call site. Once per
pre-fixup save; Steam blocks 1.0.7 saves, non-Steam loads them with a warning. Filed:
`bugs/F66.md` (with the one-line repair), `bugs/F114.md` addendum, checklist 125 (owner
picks the vehicle). ⛔ Unmeasured. ⛔ Not a second F114 cause.

**3 · `python tools/sigcheck.py --src <1.0.7>`**: 1 MISMATCH (`LandscapeUnitFilter`,
correct — 1.1.0 signature, declines on 1.0.7), 37 OK. Every other replacement site has
the same arity on both branches.

**4 · Manifest coverage gap (→ 05, tooling):** 11 sigcheck-known replacement sites carry
no `SRC:` pin of their own name (the module pins a neighbour): `ArrivalDeaths`
(`Colonist:OnArrival` 6 lines changed, `Colonist:Idle` 100), `FreedHousingNotice`
(`Colonist:SetResidence` 11), `RocketInteractGuard` (`RCTransport:InteractWithObject` 12),
`GhostFarmOxygen` (`Building:SetDome` 4), `TrackConnectorPingPong` (`Done` 4),
`TrackSalvageRefund` (`TrackGridElement:Demolish` 4), `TrainsToVoid` (`Building:OnDemolish`
2); identical across branches: `ExtenderFlapChurn` (`UpdateUplinkRequesters`),
`TrackTunnelPowerBridge` (`TrackBase:Done`), `TrainWaitTime` (`AddSpentTime`). Plus the
copied-but-unpinned `Dome:RefreshFreeLivingSpaces`. Lower bound — sigcheck does not see
`SetGlobal` sites or function literals.

**5 · For your KEEP pass (Pass on the wrappers):** the 1.0.7 tree turns "re-read the
wrapper's assumptions against 1.1.0" into "re-read them against exactly these lines". The
table in §1 plus §4 is the steer; `ArrivalDeaths` over `Colonist:Idle` (100 changed lines)
is the one I would open first. ⚖️ RULED 2026-09-09: this is YOURS — the owner took the
recommendation; decide per module which wrappers to re-read against their branch diff,
and say in your report which you did not open.

**6 · Landscaping (owner questions, same day):** rover-only AND research-gated on 1.1.0,
both verified NEW against 1.0.7 — `EF-083`. No code touched; checklist row 7 gained the
Dozer Rover prerequisite; F115's "unverifiable" line closed. ⚠️ For your Pass G: the
landscaping control now needs a mid-tree tech on the test colony.

### From link 04b's session (2026-09-09, later) — ck125(a) RULED and LANDED: the F66 guard yields to `force`

*(`smr-bugfixpack-94`. Owner: "Go ahead and do it." One-line code change in a KEEP module,
`Code/Fix_TrackConnectorPingPong.lua`; commit message carries the detail. ⛔ Nothing ran in
a game; no status moved.)*

* **The change:** `(force or not owned_by_live_other)` — the guard now yields to `force`
  exactly as 1.1.0's relaxed assert does (`TrainTransport.lua:130`). Every unforced path,
  where the F66 ping-pong lives, is unchanged.
* **Manifest:** untouched, correctly — the shipped body did not move (04's item 5: no
  re-stamp on a module-side edit). `bodycheck` 2 OK, `sigcheck` 38 OK, parse sweep 45/45.
* **Desk control** (the shipped 1.1.0 and 1.0.7 bodies and ours, forced and unforced, on a
  contested-hex stub) is in `bugs/F66.md`'s 2026-09-09 section: ours now matches vanilla
  1.1.0 under `force` (takes the hex, 0 asserts) and keeps the F66 behaviour unforced.
* ⚠️ **Correction to my earlier note (§2 above):** `force` callers existed on BOTH branches
  (the Station.lua fixup, `CreateConnectorElements(true)`, 1.0.7 `:1352`, 1.1.0 `:1510`);
  what 1.1.0 added is the second fixup `ForceTrackReconnection2` and the assert relaxation.
  The old guard diverged on every forced pass on either branch; nobody had named it.
* **For your Pass D/E:** this is the only KEEP-module code edit in the patch besides F116.
  It has no in-play control on the rig (Steam blocks the saves that trigger the fixup);
  the desk control is the evidence. 07 is asked to add a forced case to the kit probe.

### From link 05 — the tools tail, and a published count that was wrong

*(Link 05, `smr-bugfixpack-2b`, 2026-09-09. Commits `f25e530` A-4 sigcheck over
SetGlobal · `c9811e1` A-3/A-2 logscan heal-aware + retire list + the `00_Core`
string · `7ae0fc9` A-1 GeneForging · `29b7a68` two doccheck gates · `8754e00`
`tools/parsecheck.py` · `39e4ffe` `sigcheck --coverage`.
⛔ **Nothing was run in a game. No status moved. A tool run is not a test.**)*

## 1 · ⛔ THE PUBLISHED COUNT WAS WRONG, STATED RATHER THAN CORRECTED

My §6 stop condition fired. **The canonical 1.1.0 boot log reads 64 applied /
16 inactive, not 63 / 17.** `SaintBlessing` latches `inactive` at
`gated110_*.log:166` and heals at `:186`, ending the boot ACTIVE.

⭐ **AND THE LOG PROVED IT INDEPENDENTLY OF MY SOURCE READ — nobody had
reconciled it.** `UpdateSuspects` only considers entries whose status is
`inactive`, and SaintBlessing's `:166` latch is the NON-benign two-argument form,
which sets `update_suspect = true`. So had it ended `inactive`, it would
necessarily have appeared in the `:190` update report. It does not. The 16
inactive reconcile exactly as **14 named + 2 unnamed**, and both unnamed ones are
content/benign latches that correctly carry no suspicion
(`AutomationLawCompensation`, `LastTransmissionStorage`). Under 17 you would need
a THIRD unnamed inactive whose detail came from a non-benign latch — a
contradiction. **The old census was internally inconsistent with a line in the
same log, and the inconsistency sat unread through the audit that cited it.**

⇒ **What I changed and what I deliberately did not.** `STATE.md`'s live line now
reads 64/16 with the as-read 63/17 beside it. I did **NOT** rewrite the
historical records: `F115.md`'s "prediction 17/14, measured 17/14" is a true
record of a prediction matching a reading AS READ AT THE TIME, and rewriting it
would destroy the evidence that the prediction method worked. The same for
`HOTFIX_1_APPLY.md`, `HOTFIX_1_AUDIT.md`, `PACK_1_1_0_REVERIFICATION.md` and
`SESSION_LOG.md`. **"14 named" is unaffected and still correct.** For your Pass
D: the surfaces still carrying 63/17 are those five plus
`reports/HOTFIX_1_AUDIT.md:209`, and each is a historical reading, not a live
claim.

## 2 · What landed

**A-4 · `sigcheck` sees the `SetGlobal` sites.** 38 → **43** replacement sites,
5 of them SetGlobal, **0 MISMATCH / 0 UNRESOLVED**. Both live forms resolve: an
anonymous literal, and a named local followed backwards — including the
FORWARD-DECLARED `local X` / `X = function(...)` shape `Fix_BombardmentSpread`
uses, which a naive resolver would have dropped silently. An unfollowable value
is a new **UNRESOLVED** row, never a skip. 9-leg falsifier; F115's actual shape
driven through a SetGlobal site is one of the red legs.
⚠️ Your prompt and the report say **15** SetGlobal sites; that was true when
written, and link 02's deletions took it to **5** (verified against `2dc1dbe^`).

**A-3 · `logscan` is heal-aware.** Both counts always print — heal-aware
headline, first-pass beneath it — so a delta is stated, never quietly corrected.
⛔ **The report's suggested implementation is wrong and I did not use it.** It
proposed matching `corrected` / `made effective` / `re-based` / `added … missing`.
That list (a) MISSES two of the three live `ctx.heal()` sites — Sinkhole's and
SaintBlessing's 1.1.0 branch both print prose with no edit verb, and the 1.1.0
branch is the one that fires on the branch we ship against, so the keyword rule
reports a healthy module DEAD; and (b) CATCHES `re-based`/`restored`, which are
SaintBlessing's SAVE re-base lines and never run through `ctx.heal()` at all
(`F92` records a measured near-miss from exactly that). The shapes are instead
DERIVED FROM THE PACK SOURCE: `pack_signals()` finds each `ctx.heal()` and takes
the `log()` template that follows it. A post-`inactive` line matching no known
heal is printed as **UNRESOLVED**, never silently kept inactive.

**A-2 · the benign latch is a RETIRE signal.** `00_Core.lua`'s `ctx.latch` logs
`inactive (<detail> — already correct, RETIRE candidate)` when the site passes
`benign`. **THE LOG STRING ONLY** — `entry.status` still goes `inactive` (which
still gates that module's `WhenActive` handlers), `entry.detail` is untouched,
and the expression selects a format string and does nothing else; verified by
executing it under a Lua interpreter for all three argument shapes.
`logscan --retire` merges the latch list with `bodycheck`'s DEFECT-GONE rows —
one list from two instruments. ⚠️ Benign-ness is read from `ctx.latch`'s THIRD
ARGUMENT, never from prose: `Fix_SaintBlessing:289` latches NON-benign on
purpose, and a list keyed on "latched" would retire a module that failed closed.

**A-1 · `GeneForging`** — see §3; it is the only code change.

**Beyond the four augments,** all routed here by 01/02/03/04b as my fence:
`doccheck` gained the **H-10 three-way module-set gate** (RED, symmetric
difference by NAME) and now runs **`bodycheck --selftest`** as a gate;
`tools/parsecheck.py` replaces the block-balance checker three links kept
rewriting; `sigcheck --coverage` names the manifest gaps 04b filed.

## 3 · A-1 is a real latent player LOSS, and it was measured

`Fix_GeneForging` read `TechDef.GeneForging.param1`. **MEASURED: `TechDef` has
exactly ONE mention left in the entire shipped tree — the `GlobalMap = "TechDef"`
declaration itself (`ClassDef-PresetDefs.generated.lua:1730`). Zero readers.**
This module was the last consumer of a map the game abandoned, and R-32 shows one
stub already emptied. Desk red control, both techs researched, stubs emptied:
the **old module returns 100** — the whole Gene Forging bonus gone, silently,
while it still logs `applied` and every self-check stays green — and the new one
returns 150. It now reads `Techs.GeneForging:ResolveValue("param1")` (what the
shipped body does for GeneSelection one line above ours) with `TechDef` as
fallback, and asks the global `IsTechResearched` instead of hand-rolling
`(unit.city or MainCity).colony:IsTechResearched`.

⛔ **No branch guard, and that is ck118 applied rather than skipped.** The guard
is owed by a module that CARRIES a 1.1.0 body; this one carries none — it
delegates to `orig` and its value read is dual-branch by construction. Verified
against the archived 1.0.7 tree: **nothing places class `Tech` anywhere there**,
so `Techs` is empty, the first read is nil, and the fallback returns the same 50.
Full ladder (nil → 100 → 50 → 150) reproduces on BOTH branches on a desk harness
running the pack's real `Require`/`SetGlobal`/`Register` over each branch's
verbatim shipped body.

## 4 · Drift, per chain rule 5 — evidence, not shame

* **My own prompt §4 carries a false instruction**: "re-stamp it after the edit".
  The `SRC:` pin hashes the SHIPPED body, which a module-side edit does not
  touch. This is the same false instruction link 04's Pass D already corrected in
  §7 — it survived into a second prompt. `bodycheck` OK on both rows before and
  after, no re-stamp made.
* **04b's note to drop `GeneForging`'s `unit` plumbing as "harmless, 1.1.0
  ignores it" would have broken 1.0.7.** 1.1.0 ignores it and all three of its
  call sites pass nothing — but 1.0.7's signature is `GetRareTraitChance(unit)`
  and **two of its call sites DO pass a colonist** (`TraitPreset.lua:748`,
  `Colonist.lua:3559`), which `orig` uses to pick the city. The wrapper keeps a
  vararg; a red control confirms the 1.0.7 leg returns nil without it. The note
  reasoned only from the 1.1.0 body, and ck118 says a 1.0.7 player can install
  this build.
* **04b's manifest-coverage filing is half wrong.** It reported "11 sites, plus
  one copied-but-unpinned function (`Dome:RefreshFreeLivingSpaces` in
  `DomeFreeSpaceMismatch`)". My measured total is 12, which AGREES — and the sets
  do not. `Dome:RefreshFreeLivingSpaces` **is** pinned, at
  `Fix_DomeFreeSpaceMismatch.lua:42`, and `bodycheck` reports four OK rows for
  that module. Matching totals over different sets is exactly what the MODULE
  SETS gate I landed exists to catch, so the tool lists names. The 12:
  `FindCaveInLocation` (AnomalyCaveInMap:120), `Colonist:OnArrival` and
  `Colonist:Idle` (ArrivalDeaths:161,:180),
  `DroneHubExtenderBase:UpdateUplinkRequesters` (ExtenderFlapChurn:81),
  `Colonist:SetResidence` (FreedHousingNotice:67), `Building:SetDome`
  (GhostFarmOxygen:45), `RCTransport:InteractWithObject` (RocketInteractGuard:138),
  `TrackConnectedObjBase:Done` (TrackConnectorPingPong:223),
  `TrackGridElement:Demolish` (TrackSalvageRefund:195), `TrackBase:Done`
  (TrackTunnelPowerBridge:153), `TransportStatistics:AddSpentTime`
  (TrainWaitTime:108), `Building:OnDemolish` (TrainsToVoid:51).
* **My own logscan `--selftest` leg 10 asserted the wrong thing** and I corrected
  the assertion, not the tool: with no `Code/` to derive from, the LOG MARKER
  still stands on its own, so retire-detection degrades to marker-only rather
  than to nothing. The tool was right.
* **The `00_Core.lua` log-string rename did not touch control flow**, so §6's
  STOP-AND-ASK did not fire.

## 5 · Filed, not fixed — out of my fence

1. ⭐ **`ctx.heal()` logs nothing machine-readable**, which is why `logscan` has
   to infer heals from source-derived prose at all. **One line inside
   `ctx.heal()` would delete the entire inference.** §5 fenced my `00_Core` diff
   to the rename's string, so I did not take it. This is the single highest-value
   follow-up in this list.
2. ⚠️ **`STATE.md`'s byte cap is line-ending sensitive by 104 bytes.** The
   committed blob is LF; `core.autocrlf=true`, so a `git checkout` or a fresh
   clone writes CRLF and doccheck then measures **9297** where the same content
   read **9193**. The warn threshold is 9216 ⇒ **on a fresh clone the file WARNS
   with no content change**, and the owner would be told to run an eviction for
   nothing. My edit leaves it at **9212 (LF), under the warn**, but the
   sensitivity is real. doccheck should measure the file as git stores it.

   ✅ **DISCHARGED 2026-09-09 (`smr-bugfixpack-0e`, on-call, owner-authorised) —
   fixed from the git side, so doccheck needs no change.** `.gitattributes` now
   pins `docs/agent/STATE.md text eol=lf` (same shape as the existing
   `tools/hooks/*` pin), so every checkout materialises LF and the cap measures
   content instead of a checkout artefact. ⛔ **The phantom was real, not
   projected**: a fresh `git clone` of the pre-pin HEAD measured STATE.md at
   **9316 B / 105 CR** and doccheck printed the size warn verbatim, exit **0**
   (a size warn never blocks — `ok` is set by RED only). ⚠️ `core.autocrlf=true`
   is **system-level** here, the Git-for-Windows default, so this was every
   Windows clone's behaviour and not a quirk of one checkout. ⚠️ The `104`/`9297`
   /`9193` numbers above were correct for that day's line count; the delta is
   exactly **one byte per line**, so re-derive it, never quote it.
   ⛔ **The margin is the part that still bites: 9211 B against a 9216 warn = 5
   BYTES of real headroom.** §4's own requirement that this link point `STATE.md`
   at the audit report is a ~60–120 B addition ⇒ **99 trips the warn with
   certainty** and must budget an eviction in the same commit (link 06 got away
   with it only because `02–05` → `02–06` is byte-neutral). Link 07's re-emitted
   probe count is ~0 B while it stays three digits, so 07 probably does not.
3. `bodycheck.py --help` and `upload_preflight.py --help` still raise
   `UnicodeEncodeError` on this rig's cp1252 console. I fixed `sigcheck`,
   `logscan` and `parsecheck` (three lines each); both of those are outside my
   fence. `doccheck` already had the guard.
4. `sigcheck`'s comparator does not flag a site declaring MORE fixed parameters
   than the shipped function takes. `GeneForging` was `(unit)` against a
   parameterless shipped body and read OK. Harmless there and moot after A-1, but
   it is a blind spot; I left the comparator alone rather than widen it and
   create noise I could not evaluate.
5. `Fix_GeneForging` now depends on `Preset:ResolveValue`'s fall-through from
   `GetProperty` to `GetParameterValue` (`CommonLua/Preset.lua:554`), and **no
   instrument watches that**. A `SRC:` pin on it would produce a `NO-DEFECT` row
   andneed a `FIX_POLICY §2b` exception entry — FIX_POLICY is not mine.
6. `logscan`'s source-derivation is anchored to the CURRENT pack, so a DELETED
   module's benign-latch prose is no longer recognised in an old log —
   `LastTransmissionStorage`'s "the shipped presets are already correct" at
   `gated110_*.log:184` is not flagged as a retire candidate, although R-13 is the
   canonical example of one. Correct behaviour (the module is already gone) but
   worth knowing before reading an old log's retire list as complete.
7. A peer session (`smr-bugfixpack-e9`) suggested a **control-character scan over
   `docs/`** as a doccheck gate, after a quoted bash heredoc ate a backslash and
   left a literal `0x01` byte inside a path that rendered as almost-right. Four
   lines, real failure behind it. I did not build it — it is a third unrequested
   gate and rule 3 says file, do not fix.

   ⭐ **ADDENDUM 2026-09-09 (`smr-bugfixpack-0e`, on-call, owner-authorised): the
   scan was RUN, and it changes the gate's spec in two ways.** Scanned all **573
   tracked files** plus the 26 relevant TestKit files. Result: **3 files, 6
   bytes** — and ⛔ **the population is not what item 7 describes.**
   * ⚠️ **Build it over `docs/` as filed and it is RED on day one and RED
     FOREVER.** 4 of the 6 bytes are in `docs/archive/PLAYTEST_ARCHIVE.md`
     (2× `0x07`, from `\agent` → renders `gent/bugs/F46.md`) and
     `docs/archive/SESSION_LOG.md` (2× `0x08`). `docs/archive/` is append-only
     and never edited, so **those 4 bytes can never be repaired** — the gate
     MUST exclude `docs/archive/` or carry a 4-byte baseline.
   * ⚠️ **The mechanism is wider than "`0x01` in a path", and a path-shaped
     check misses the worst case.** Three escapes have been eaten so far —
     `\1`→`0x01`, `\b`→`0x08`, `\a`→`0x07` — i.e. exactly the **recognised** C
     escapes. In the same sentence as an eaten `\b`, a `\w*(...)\w*` regex
     **survived intact**, because `\w` is not a recognised escape. ⇒ the
     corruption is selective and silent: it eats precisely the escapes that
     leave plausible-reading text behind.
   * ⛔ **The `reports/GAME_1_1_0_AUDIT.md` §2c instance did not mangle a path —
     it INVERTED A TECHNICAL CLAIM, and I repaired it** (2 bytes, `\borig\b`
     restored). As shipped it read *"The detector tested `orig`, which does not
     match `orig_update_end`"*, **false as rendered** — a bare substring `orig`
     does match `orig_update_end`; the eaten `\b` was the whole reason the
     sentence was true. §2c's conclusion (population ~11–31, unsettleable by
     regex) was never affected, only its evidence line — but a reader checking
     the reasoning finds it does not hold, and the available inference is that
     the caution was unfounded, i.e. **re-trust a regex classifier.** That risk
     was live and pointed at: `reports/GAME_1_1_0_IMPACT.md:302` routes readers
     to §2c for exactly this, and §5 row 103 of THIS file refutes the sibling
     24/66 census from the *same* failure mode. ⚠️ The two `docs/archive/`
     copies of that same sentence still carry the inversion and MUST NOT be
     edited — cite §2c, never the archive copy.
   * ⇒ **Scope the gate to the repo, not `docs/`.** The highest-consequence case
     is currently clean and is the reason the four lines earn their place: the
     same trap inside a `tools/*.py` regex. A `\b` silently becoming `0x08` in
     `sigcheck`/`doccheck`/`logscan` makes the instrument quietly wrong **while
     reporting green** — the exact F114 class ("an instrument being green never
     means the code was checked"). `tools/`, `Code/`, `items.lua`,
     `metadata.lua` and the TestKit are **0 of 6** today.
   * ⛔ **Still not built.** Rule 3 holds for the gate itself; the owner
     authorised the scan and the two repairs, not a third gate.
8. The same peer notes a planned two-tree function differ (`VANILLA_DIFF_HUNT.md`)
   is scoped to import `luafn.find_bodies`. ✅ **I did not touch `luafn.py` or the
   `find_bodies` contract**; `bodycheck` still imports it unchanged.

## 6 · ⛔ What may NOT be claimed from this link

* **Not** "the tooling now catches game updates". It catches classes a, b, d, e.
  **Class c — semantics moving under a wrapper — is still seen by nothing**, and
  6 of the 10 FIX rows this audit were class c.
* **Not** "the log census is verified" beyond the ONE archived boot log I ran
  against. And that log predates several of this chain's commits: it describes an
  80-module pack, not today's 45.
* **Not** "sigcheck now clears the SetGlobal sites". It bounds their ARITY. The
  bodies behind them are exactly as unread as before. Widening what an instrument
  sees does not strengthen what it says — that implication is how F114 shipped.
* **Not** "A-1 is verified". It has desk controls on both branches and **zero
  in-game execution**; F41 stays `tested` on its pre-existing 2026-08-12 evidence.
* **Not** "the 12 unpinned sites are a defect list". They are bodies nothing
  watches, and the FIX/REMOVE sets are deliberately unstamped until the pack is
  whole.
* No status moved.

## 7 · Gates at close-out

`doccheck` **GREEN** — ⚠️ **verbatim, the 18 warns it prints are all
pre-existing frozen-index-row drift, unrelated to this link**: `F85`, `C12`,
`C13`, `C14`, `C15`, `C16`, `C17`, `C37`, `C35`, `C34`, `C38` (`the frozen
index-row cell says 'filed', entry says 'cand'/'wontfix'`), `C39`, `F100`, `C43`,
`C49`, `C50`, `C51`, `C52`. No STATE warn (9212 B, warn 9216).
`bodycheck` exit 0, 93 OK, `--selftest` PASS · `sigcheck` 43 sites, 0 MISMATCH,
`--selftest` PASS (9 legs) · `logscan --selftest` PASS (13 legs) ·
`parsecheck --selftest` PASS (7 legs) · Lua parse sweep 45/45 and TestKit 24/24.

### From link 05 — addendum, 2026-09-09: one correction to my own §1, and two items peers added

*(Same session, `smr-bugfixpack-2b`, after two sibling sessions read the close-out.
⛔ Still nothing run in a game; no status moved.)*

**1 · ⚠️ CORRECTING MY OWN FRAMING ABOVE. §1 overstates this link's part in the
census.** `smr-bugfixpack-91` (link 03) pushed back, and it is right: **the
re-verification report ALREADY called it.** `reports/PACK_1_1_0_REVERIFICATION.md:114`,
augment row A-3, says in as many words — *"the '17 inactive' headline is really
**16**"*. I quoted that row in my own tool docstring and still wrote the section
header as though the number were a discovery.

⇒ **Read §1 as: 05 IMPLEMENTED a known correction and added a second,
independent route to it.** There are now THREE routes to 16, which is worth more
than one discovery:
* the report's own A-3 row (the heal at `:186`, reasoned from the source);
* my `UpdateSuspects` argument (a non-benign latch is ALWAYS named, and
  SaintBlessing is absent from the `:190` report naming 14 — so it was not
  `inactive` at report time);
* link 03's independent line count (17 distinct modules log an `inactive` line;
  14 are in the named report; minus SaintBlessing = 16).
⛔ **99 must not count this as a fresh finding** — that would double-count one
insight three times over. What was genuinely unreconciled is narrower: nothing
had checked the census against the `:190` report in the same log.

**2 · SKIPs BY NAME (STATE's standing rule), applied here.** The two `inactive`
modules that are correctly absent from the named 14 are
**`AutomationLawCompensation`** and **`LastTransmissionStorage`** — both content
or benign latches, neither patch rot. Never write the reconciliation as
"14 named + 2".

**3 · ⚠️ A LIVE SURFACE MY "LEAVE THE HISTORY ALONE" CALL DOES NOT COVER — filed,
not fixed, because F115 is not my entry.** I argued above that the historical
records should keep their as-read numbers, and I stand by that for narrative
bodies and for `archive/`. But `bugs/F115.md` carries the old count in two places
that are **live claims, not history**:
**All FOUR occurrences, verified by grep as the complete set in that file, and
they do NOT all need the same treatment:**

| line | what it says | disposition |
|---|---|---|
| `:10` | `row_status:` front matter — *"✅ BOOT CONFIRMS the prediction exactly — 17 inactive / 14 named"* | asserts the boot MEASURED 17 |
| `:14` | the heading tag — *"[fixed 2026-09-08: … 17 inactive / 14 named, 0 errors]"*, the surface `doccheck` compares | asserts the boot MEASURED 17 |
| `:135` | *"PREDICTION as recorded ahead of the reading: 17 inactive / 14 named"* | ⭐ **LEAVE EXACTLY AS IT STANDS.** It records what was predicted BEFORE the reading. That is a true statement about a prediction, and it is the evidence that the pair was consistent |
| `:168` | *"17 inactive / 14 named, exactly as predicted before the reading"* | asserts the boot MEASURED 17 |

So three of the four assert a measurement, one records a prediction. Rewriting
`:135` would destroy the very evidence that makes the other three explicable.
Under the corrected census that **"exactly" is false in one of its two numbers**.
The prediction and the reading agreed because BOTH were computed
last-verdict-wins — a consistent pair built on one miscount, not a confirmation.
⭐ **The half that mattered for F115 is untouched and its verdict is unaffected:**
`LandscapeUnitFilter` is in the named 14 independently of any of this. So this is
a wording problem on a live claim, not a defect in F115.
⚠️ Accuracy note on the routing: the string is in live front matter but does NOT
reach the rendered `bugs/INDEX.md` row, so the exposure is the entry file itself
rather than the index. Reconciliation is yours.

**4 · ⭐ THE LINE-ENDING FINDING (§5 item 2) IS NOT HYPOTHETICAL — IT HAS ALREADY
PRODUCED A WRONG DIAGNOSIS.** `smr-bugfixpack-e9` reports that yesterday it read
`STATE.md` at **9310 bytes** mid-turn and **9203** immediately before and after,
diagnosed it as a transient caused by a sibling session's write, **reported that
conclusion to the owner**, and used it to argue that byte readings are unreliable
while siblings are live.

**I verified the pair against git rather than taking it on trust:** commits
`e96a1ff` and `5daaeb5` both hold `STATE.md` at **9203 bytes LF over 107 lines**,
whose CRLF form is **9203 + 107 = 9310**. Exactly the two numbers seen. So the
likelier cause was the file being momentarily CRLF on disk during a git
operation — a systematic, reproducible artefact attributed to random concurrency,
in the direction that stops anyone looking further.

⛔ **And the failure mode is worse than the phantom warn I filed.** A
CRLF-shaped reading taken mid-git-operation looks like NOISE, which invites
"ignore it" rather than "investigate it". A phantom warn at least gets attention.

⭐ **The framing to put to the owner, which is stronger than "it is off by 104"**
(e9's, and I agree): **an un-normalised byte count is itself a PROXY** — it
measures content plus one checkout artefact per line. Checklist 42's own ruling
is *cap the real resource, never a proxy*. **The cap as implemented defeats the
rule it was created to enforce.** The fix is to measure the file as git stores
it (normalise line endings before counting), not to raise the threshold.

**5 · Attribution, so nobody re-derives it.** Items 3 and 4 came from sibling
sessions reading this close-out — link 03's session (`smr-bugfixpack-91`) and
`smr-bugfixpack-e9`. Item 1 is link 03's correction of me. I verified each
against the tree or against git before recording it; none is taken on trust.

### From link 06 — the text: every surface I made true, and every claim I refused to make

*(Link 06, `smr-bugfixpack-05`, 2026-09-09. Commits `5abbfaa` site text in
`SMR-CommunityMods` · `641613e` the store card + change note + both synced backups.
⛔ Nothing was run in a game; no status moved; no `Code/`, `items.lua` or version
field was opened.)*

**⭐ READ THIS SECTION BEFORE YOU RE-SEED `100_DOCSWEEP` (§12).** Link 04b's
session asked me to be explicit about which seed surfaces are now CLEAN, because
your §12 seed named F108 / F107 / F105 as "already found, do not re-derive" and
those are exactly the surfaces I own. The seed is spent. What follows is the
replacement input.

#### 1 · The surfaces I FIXED — do not re-hunt these

| surface | what was false | now |
|---|---|---|
| `metadata.lua` `description` | "Eighty-two repairs" | **Forty-six**, recounted from the deployed fix list (`grep -c '^??? '` = 46; section tally 1+13+4+3+9+4+7+2+3 agrees) |
| same | "four of them repair things you cannot see" | **three** — "Under the hood" lost the battery/tank rate-modifier entry |
| same | **11 of the 20** "SOME OF WHAT IT FIXES" bullets named deleted fixes | all 20 redrawn from the surviving 46 |
| same | 3 of the 4 headline clauses (return-fuel lander, leaked upgrade bonuses, the 10%/20% terraforming discount) | replaced; the fourth (Comfort billed for the wait) survives |
| same | the modder veto example named `DustDevilSpawnGate`, deleted in `2dc1dbe` | `LakeEntombment`, live at `Code/Fix_LakeEntombment.lua:41` |
| same | no 1.0.7 route on the card (ck118) | a portal-neutral block pointing at the site's frozen-v5 page, in plain AND BBCode |
| `metadata.lua` `last_changes` | described hotfix **1** | rewritten wholesale (appending would post a duplicate changelog entry) |
| `UPLOAD_WORKFLOW` §3 (both blocks + change note) | matched the old card | synced in the SAME commit; proven byte-identical, see §5 |
| `STORE_CARD_LIVE.md` (both blocks) | matched the old card | synced in the same commit; its counts block and its stale "5,124 chars" corrected |
| site `fix-list.md` | "Under the hood: **these four**" with three entries | three |
| site `fix-list.md` | F73 promised **two** things; link 03 deleted half (a) | one thing; the "a habitat keeps its residents" promise is gone, judgment-call flag kept for the surviving half |
| site `faq.md` | "More dust devils" and "Automation policy" bullets | gone with the fixes they described |
| site `faq.md` ×3, `index.md` ×1 | "six judgment calls" | **three** (Biorobots · vacuum · Edit Payload) in all four places |
| site `faq.md` | the save-repair list named "leaked upgrade bonuses" and "a stuck weather flag" | removed — verified against `Code/*.lua`: no module carries either heal now |

#### 2 · ⛔ A FOURTH STALE PUBLIC CLAIM THAT NO UPSTREAM LINK ROUTED — F92, the Saint's blessing

This is the F108 / F107 / F73 shape on a fifth entry, and it reached me only
because I traced the store card's "a trait's colony-wide bonus that never reached
a single colonist" clause back to its fix-list entry instead of assuming the
upstream routing lists were complete.

`Fix_SaintBlessing.lua`'s own 1.1.0 header says it plainly:

> ⚠️ WHAT THIS MODULE IS ON 1.1.0, said plainly: a save healer for damage a
> previous version of THIS PACK did, and nothing else.

⇒ the site entry's *"After the fix: the blessing lands on the dome's colonists"*
and the card's clause were both describing a repair the pack **no longer
provides on the current game** — 1.1.0 repairs F92 itself. The clause is out of
the card; the entry keeps its history and gains a *Worth knowing* note saying so.

⚠️ **The general point is worth more than the instance, and it belongs in your
Pass H corpus:** link 02 routed the surfaces of the modules it DELETED, and link
03 routed the surface of the half it deleted. Neither was wrong. But a module
that was **KEPT** can strand a public claim just as dead as a deleted one, and
nothing in the chain was looking there. If you want one structural finding out of
Pass F, that is my candidate.

#### 3 · What I deliberately did NOT claim, and why

* ⛔ **No "Fixed", anywhere, for anything.** Every in-play control from 03, 04 and
  04b was still owed when I wrote. The change note's last bullet says so in the
  player's own words rather than hedging each line: *"None of this has been
  watched in a running colony on 1.1.0 yet — it is derived from the new game
  code."*
* ⛔ **No outright "1.1.0 compatible."** Nothing in either string says it.
* ⛔ **No count I did not recount from the fix list.** The 46 and the 3 both come
  from `grep -c` over `content/fix-list.md`, cross-checked against the section
  tally, and both stay checkable by a reader on the page the card links to.
* ⛔ **Nothing about another mod, and no load-order advice** (`EF-054`).
* ⛔ **Nothing about F12 `LowStorageWarning` beyond the blanket removal
  sentence.** The retracted "no low-Food warning at all" claim is not printed
  anywhere and I did not offer a restored warning as a future feature.
* ⛔ **F116 is capped at link 04's ceiling** — "matching the base game", never
  "fixed a bug that deleted track". It was never reproduced.
* ⛔ **F-10 is worded "re-enabled", never as a confirmed 1.1.0 defect** (04b's
  constraint 2; the C-side premise is still unread).
* ⚠️ **`FirstAsteroidPrefabs` got no line.** Link 02 said it "needs a note, not an
  apology": prefabs already granted cannot be taken back and the GameVar is
  absent-tolerant, so nothing breaks and nothing is visible to a player. I judged
  it below the bar for a store changelog. **Overrule me if you disagree** — it is
  the one routed item I consciously dropped rather than carried.

#### 4 · ⛔ ck112 — and a correction to how this chain has been WORDING it

Bullet 3 of HOW IT WORKS is **byte-identical to what shipped in v5**, asserted
mechanically (see §5). But my own prompt, checklist item 112 and commit `e1095d5`
all label this **"DEFERRED"**, and `smr-bugfixpack-d7` — the session that authored
`prompts/SELFCHECK_PROMISE_AUDIT.md` — flagged that the label misreports the
ruling. I checked their claim against checklist 112's own body and they are right:
that body already says "Neither (a) nor (b)".

> ⚖️ The owner did not defer the item. They **rejected both recorded options** and
> commissioned a third the item never offered: make the sentence TRUE rather than
> reword the promise down to match the code.

The difference matters for you specifically: **"deferred" reads as "we reword it
next cycle", which is option (b), which the owner explicitly turned down.** A
future reader trusting the label lands back on a rejected option believing it is
the standing decision. ⛔ Do not flag bullet 3 as an open loop or an unresolved
audit finding (checklist 112 forbids it), and do not describe it as deferred
either. It ships over-promising this cycle by the owner's accepted, recorded
choice, with `prompts/SELFCHECK_PROMISE_AUDIT.md` running against it.

#### 5 · Pass F is mechanically pre-answered — reuse the check rather than eyeballing it

Your §7 asks "do the backups match `metadata.lua` **exactly**?" I did not eyeball
it. `scratchpad/verify_sync.py` un-escapes the Lua literal and compares:

```
shipped description : 5342 chars
upload plain block  : 5342 chars
shipped vs upload-plain, 0 differing lines
BBCode blocks identical in both docs : True
change-note block == last_changes    : True
retired-claim sweep (18 phrases x 7 copies): 0 hits
ck112 bullet 3 UNCHANGED in shipped description: True
```

⚠️ The `STORE_CARD_LIVE` plain block is 5,485 — 143 chars longer — and that is
**by design, not drift**: it carries the two portal-specific passages the shipped
string must not (the "no comment section" line and the cross-link). Do not
"repair" that difference.

#### 6 · ⚠️ Length, which is the sitting's finding and not mine (my §8)

The shipped `description` is **5,342** chars, up from **5,228**. ⛔ While
measuring it I found `STORE_CARD_LIVE` had been carrying **"5,124"** — stale since
before the F105/F108/F110 additions, and the only number this project had on
record. Corrected in place, in both directions: the web editor took 5,165, but the
body that actually went through the **upload path** as v5 was 5,228, so the API is
known to accept at least that. This is +114 on a proven length, not a leap.
⛔ Still UNVERIFIED against the upload API. If an upload rejects it, that is the
sitting's finding and the field reverts.

#### 7 · Filed, not fixed — out of my §7 fence, and they are `100_DOCSWEEP` seeds

* `prompts/POST_UPLOAD_CLOSE.md:59` — *"expect **82 entries**"* in the packed
  artefact check. Becomes 46 after this upload. A **live instruction**, not a
  record, so it will mislead the next post-upload session.
* `prompts/PUBLIC_SURFACE_SWEEP.md:110` and `:272` — *"Eighty repairs"* as the
  card's count word. Already stale before I arrived (the card said Eighty-two),
  and it is the very template §12 tells you to build `100` from. ⇒ **fix the
  template's number, or `100` inherits it.**
* ⛔ `metadata.lua`'s `PackVersion` comment at `:165` / `:182` / `:275`. Link 01's
  session (`smr-bugfixpack-26`) messaged me mid-run to correct their own earlier
  relay of this: the honest status is **UNVERIFIABLE FROM SOURCE**, not false —
  `PackVersion` has zero hits in readable Lua on **either** branch, and absence
  from `Src` is not absence from the game (`GetTargetAmount`,
  `DisconnectFromCommandCenters`). Its gloss was already rewritten once on
  2026-08-29 after two wordings got it wrong. **Do not let `100` "fix" it on a
  name grep** — that would be the same error a third time.
* Everything else that greps for "Eighty-two" is a dated historical record
  (`PLAYTEST_CHECKLIST` 1054-1076, `RELEASE_OUTBOX`, `RELEASE_PORTAL_PREP`) and
  must NOT be edited.

#### 8 · Drift in my own work, per chain rule 5

* I twice wrote a patch script whose search strings used `\n` against
  `metadata.lua`, which is **CRLF** on disk while every `.md` in the tree is LF.
  The first pass silently succeeded anyway — because those passages live inside a
  single-line Lua literal where the newlines are escaped `\n` text, not real ones
  — and only the multi-line comment blocks failed. A checkout artefact that
  produces a *passing* result on one class of edit and a failure on another is
  exactly the shape that already caused a wrong diagnosis on `STATE.md` this week.
  The scripts now match the file's own ending.
* My first store pass asserted "exactly one occurrence" for the veto snippet and
  failed: it appears **twice** per doc, once in the plain block and once inside
  the BBCode `[code]` tag. The assertion caught it, which is the point — but a
  looser `replace()` would have shipped a half-updated Steam block.

#### 9 · Gates at close-out

`python tools/doccheck.py` **GREEN** · `sigcheck` unchanged (12 sites carry no
`SRC:` pin, a lower bound, unchanged by me) · `bodycheck` 93 OK / 2 NO-MANIFEST /
1 NO-DEFECT / 3 SRC-NONE · `parsecheck --dir .` 0 errors, CRLF preserved
(291 → 352 lines, all CRLF).

⚠️ **doccheck WARNs, verbatim, per chain rule 13** — all pre-existing bug-index
tag rows, none touched by me and none caused by this link:

```
warn F85/F100/C12/C13/C14/C15/C16/C17/C34/C35/C37/C38/C39/C43/C49/C50/C51/C52:
     the frozen index-row cell says 'filed', entry says '<wontfix|cand|fixed|
     tested-attended|tested-unattended|parked>'
STATE + STUBS: STATE.md 9211 bytes (warn 9216, hard 18432, line 200)
```

⚠️ **`bodycheck` NO-MANIFEST reads 2, where my prompt's §4 predicted 10 as the
cross-check that "the right set left".** It is not a discrepancy: links 03/04/04b
stamped the FIX and re-copy sets after link 01 wrote that prediction, and the
remaining 2 are `00_Core.lua` and `90_SaveSanitizer.lua`, which patch no game
function. The cross-check that actually bears is doccheck's **45 files / 44
registered / three-way module-set agreement**, and that reads exactly what link 02
said it would.

#### 10 · ⛔ THE SEQUENCING ITEM THE SITTING MUST NOT MISS

The card now says **"Forty-six repairs"** and tells the reader to go and count
them on the fix list. That page is **committed but NOT published** —
`publish-site.yml` is `workflow_dispatch` only, so committing never deploys, and
the live site still shows 82 entries. ⇒ **`UPLOAD_WORKFLOW` §4 (publish the site)
must happen in the same sitting as the upload**, or the card's own checkable
number disagrees with the page it points at. This is the failure mode the count
was chosen to avoid, arriving through the back door.

## Notes from upstream (continued — SELFCHECK_PROMISE_AUDIT, appended after link 06's close-out per the read path at line 19)

#### 9 · CORRECTION from the same session, after the Codex cross-check (2026-09-09, `397bf15`)

The owner ran a cross-vendor check (`reports/SELFCHECK_PROMISE_CROSSCHECK_CODEX.md`).
Four claims in my block above were refuted and I re-verified each against the
trees and the logs; the audit report now carries a §10 with all corrections.
Two touch this inbox directly:

- **§1 above, "StaleReservations … class (c) proper, measured, one module of
  44" — WRONG.** The two `SRC:` pins are identical on both branches, but
  `Residence:CancelResidenceReservation`, which the module DECLARES at
  `Fix_StaleReservations.lua:100` and CALLS at `:159`, gained
  `unit.expedition_residence = false` on 1.1.0 (`Residence.lua:393`). A pin
  over a module's declared dependencies would have declined F-2. The scope
  is "the code it patches and declares", and the known class-(c) residue on
  this patch is zero, not one.
- **§5 above, "all 4 `Error in mod` lines name the mod whose code threw" —
  WRONG for the act1 line.** `act1_…-6a22b86d.log:397` and `:416` are throws
  in VANILLA `Data/LawDef/LawDef-Welfare.lua:1892`/`:2026` (`ActiveLaws`
  false at the menu), provoked by the Test Kit's wave-4 probe
  (`40_Probes_Wave4.lua(921)`); the box named the kit as a CALLER of the throw
  site. My "shutdown artefact at quit()" came from a SESSION_LOG line about
  the 07-25 legs, not this log. The pack itself is still never misattributed
  in the archive; the kit line is a caller-named case.

Also corrected there, for your Pass D: bytecode pins flip on edits OUTSIDE the
pinned function (a file-local `ipairs` added at `Colonist.lua:13` changes
`FindTransportationModeToCommunity`'s compiled form with its text unchanged),
so "at most 17 false stand-downs" was wrong in direction; `run_apply` has no
rollback, so a multi-site module can decline on its second site with its first
already installed (`Fix_AnomalyCaveInMap.lua:99` then `:120`) — the sentence's
"does nothing at all" clause is not honoured by the runner today; and
`CommonLua/Core/ToLuaCode.lua:390` `LuaCodeToTuple` is an unblacklisted
indirect `load` in the engine environment behind a C-side checksum gate whose
behaviour on arbitrary text is unmeasured. ⛔ None of these is a hotfix-2 code
item; the last one is a sandbox fact to know, not to use.

### From SELFCHECK_PROMISE_AUDIT (`smr-bugfixpack-db`, closed 2026-09-09) — a parallel READ-ONLY audit; what it hands you, and what you must not read into it

Written into this inbox on the owner's explicit instruction (2026-09-09: *"You
can provide 99s outbox with anything you need to tell it"*); the audit's own
brief fenced this file off. Report: `agent/reports/SELFCHECK_PROMISE_AUDIT.md`,
commits `5f595bc` → `b9a994d` → `e460817` → `1d04bc7`. `Code/`, `items.lua`,
`metadata.lua`, `bugs/`, `STATE.md` and the checklist were NOT touched.

#### 1 · The verdict, so you do not re-derive it

**YES BUT SCOPED.** The store's bullet 3 can be made literally true for *the
code the fix patches*, not for *what the fix was written for*. Measured, not
argued: the engine's own `ModEnvBlacklist` + `LuaModEnv` lines (Mod.lua
1.1.0 `:1280-1441`, `:1551-1627`) executed verbatim on a desk Lua 5.3 resolve
`string.dump` for a mod chunk while `debug`/`io`/`load` are nil; `Mars.exe`
carries the `str_dump` error text and `Lua 5.3`. A signature read from the dump
needs no pin and, against the archived 1.0.7 tree, flags exactly F115 and
nothing else; a compiled-body pin would have caught F114 and six more FIX rows
but also stood down 17 working modules on 1.1.0 (`bodycheck --src <archive>`:
27 BODY-CHANGED rows over 24 modules). `StaleReservations`' two pinned bodies
are byte-identical on both branches — class (c) proper, measured, one module
of 44. ⛔ **Nothing ran in a game**; `string.dump` inside `Mars.exe` is the one
runtime read still owed (a 5-line Test Kit probe, report §4 item 3).

The owner's own summary of it, confirmed: today no runtime check switches a
full-body fix off when a patch fixes the defect (32 double-applied modules on
1.1.0 with every self-check passing); with a body pin the 15 REPLACE sites CAN
be guaranteed (the defect line is inside the copied function, so a fix must
edit it); wrappers/handlers/data patches whose fix lands elsewhere never can.

#### 2 · ⛔ What this audit is NOT, for your verdict

- **Not an open loop for hotfix 2.** ck112 bullet 3 stays exactly as 06 left
  it, on the owner's ruling; the audit recommends changing it ONLY in the
  release that carries the arity check, which is a post-99 code cycle
  (report §9 names implementer and cycle per item). Do not flag the unchanged
  bullet as a finding.
- **Not a clearance of anything.** Every "measured" in it is a tool run on both
  trees, a binary string read, an archived log or a desk Lua — never a boot.
- **Nothing from it lands in hotfix 2's code.** The only hotfix-2-shaped items
  are the five relays in §4 below, and each is a filing or a header-comment
  question, not a code change for this patch.

#### 3 · Corrections to recorded numbers (chain rule 5 — evidence, not shame)

- The audit prompt's seed table said **43 modules / 39 existence / 5 probe / 7
  test**. Re-derived by script and hand: **44 modules** (`90_SaveSanitizer`
  registers; doccheck's module-set gate agrees), **35 existence-only** (39
  double-counted the three probe+test modules), 5 probe, 7 test. Its author
  asked for the delta to be recorded.
- The prompt's *"6 of the 10 FIX rows were class (c)"* is **4 of 10** — the
  re-verification's table lists six class-(c) instances in total, of which
  F111/F112 were never FIX rows.
- A peer's *"probes ship in exactly two modules"* predates 04b; it is five.
- `archive/logs/unforced110_…15.57.09` is a 274-line prefix of
  `f114repro110_…15.57.09` — one session archived twice (`cmp` ends at byte
  14539). Not a defect; do not count it as two legs.

#### 4 · Five findings routed to you (all module-level, none this audit's to land)

1. **`90_SaveSanitizer.lua:28` states a reason that is FALSE on 1.1.0.** *"F48
   STAYS. The paren is still misplaced upstream."* — 1.1.0 `Station.lua:1504`
   reads `ProcessTrackElements(ResolveMap(track), track.elements)`, correct;
   the misplaced form survives only in the 1.0.7 archive (`:1346`). I confirmed
   both lines myself. ⛔ REMOVE-shaped, so it needs the replacement traced,
   not a verdict from here: a migrated 1.0.7 save may already list the fixup in
   `AppliedSavegameFixups` (that route, `CommonLua/SavegameFixup.lua`, was NOT
   OPENED by anyone), and QA §0.6 (R-36) already makes the sanitizer
   platform-conditional. Minimum: the header reason must change; whether the
   pass stays is a traced question.
2. **Two modules replace a global by plain assignment**, skipping
   `SMRFixPack.SetGlobal`'s §1.4b read-back: `Fix_WispRewards.lua:39`,
   `Fix_ShuttleTransportCache.lua:61`. `sigcheck.py` bounds their arity (both
   are `function Name(` declarations); the read-back is what is missing.
3. **Three `OnMsg` handlers are registered without `WhenActive`:**
   `Fix_CrystalMysteryHang.lua:115` (`MysteryEnd`),
   `Fix_TrackTunnelPowerBridge.lua:160` (`StationsConnected`) and `:166`
   (`PostLoadGame`). `FIX_POLICY` §2's A1 rule; benign-by-construction was NOT
   assessed.
4. **`Fix_PayloadTemplateRefill`'s probe has never run in a boot** (`177c7b2`
   at 23:48 postdates the newest archived log, 17:51) **and indexes
   `FlightPolicies` at apply time**, a global created only on `ClassesBuilt`
   (`Preset.lua:1404-1412`). It is safe today because the engine's mod-less
   first Lua pass built it before the reload that loads mod code; that is a
   boot-order dependency, not a contract. → 07's Unit B re-read should include
   it, and the post-99 sitting's log must show `PayloadTemplateRefill: applied`.
5. **Three modules carry no `Require` block** (`ExtenderFlapChurn`,
   `SequenceLatents`, `ShelterReflex`; `DustSicknessBiorobots` is a `DataPatch`
   whose checks live in its pass). Their inline checks are existence checks.
   Any future pack-wide mechanism in `Require` does not reach them until they
   are routed through it. A count for your Pass D, not a defect.

#### 5 · Job two (mod-blame), for the facts/checklist lane — route, do not drop

- **Zero misattributions in the archive**: all 4 `Error in mod` lines (3
  sessions) name the mod whose code threw. The two real cases are F104/F105
  (field, both pass-through frames, both named us ALONE).
- **The once-per-session dedupe is measured**: in the 15:57 session F115 drew
  the one line at `0:01:03`; F114's 157 throws from `0:25:42` drew none.
- **Box order = enable order** (`TurnModOn` → `AccountStorage.LoadMods`,
  `ModManager.lua:35-36`; `ModsReloadItems` `:2137-2143`).
- **ck73 option 2 (trampoline) is dead**: `load`/`loadstring` are blacklisted
  (`Mod.lua:1424-1432`). Option 0 (a breadcrumb via our own
  `OnMsg.OnLuaError`, not message-blacklisted) is buildable in ~15 lines.
- **Every pre-wrapper in the pack already tail-calls** (64 sites: PRE-TAIL 15,
  PRE-NOTAIL 0, POST 13, REPLACE 15, HANDLER 17, DATA 4) — the tail-call
  remedy is a `FIX_POLICY` §2 line, not an edit.
- Proposed `EF-065` addendum and ck73 addendum text: report §7a/§7d.

#### 6 · Owner-facing text I could not land (report §9)

A proposed checklist item (three calls: build the arity check post-99;
decline-all vs abstain-all on a pin quorum; bullet 3 interim) and a one-line
STATE entry. ⚠️ STATE is at 9211 of a 9216 warn — any addition needs an
eviction in the same commit (`prompts/STATE_EVICTION.md`). Either you land
them in your close-out or `100_DOCSWEEP` does; they are not landed now.

#### 7 · What the audit did NOT check, so you do not treat it as covered

Report §8, in full. Headline: no game boot; the engine's dump FORMAT assumed
stock 5.3; the 44-module classification is four subagent reads of which I
re-derived four shipped bodies myself (`DroneControl.lua:672-677`,
`Fix_GhostFarmOxygen.lua:44-58`, `Fix_WispRewards.lua:33-45`, the sanitizer
paren on both trees); `GetTargetAmount` still unread by anyone.

#### 8 · Gates at close-out

`python tools/doccheck.py` GREEN on every commit. ⚠️ **doccheck WARNs,
verbatim, per chain rule 13** — the same 18 pre-existing bug-index tag rows 06
reported, none touched by me:

```
warn F85/F100/C12/C13/C14/C15/C16/C17/C34/C35/C37/C38/C39/C43/C49/C50/C51/C52:
     the frozen index-row cell says 'filed', entry says '<wontfix|cand|fixed|
     tested-attended|tested-unattended|parked>'
STATE + STUBS: STATE.md 9211 bytes (warn 9216, hard 18432, line 200)
```
