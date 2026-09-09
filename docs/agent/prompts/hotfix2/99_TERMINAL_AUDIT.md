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

### ⛔ Known-false surfaces to seed it with — already found, do not re-derive

`F108` (`ExtractorStaffedPerformance`) and `F107`/`F105` (`LandscapeCostRefresh`)
are **named on the store cards and the site while both modules are gone.**
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
is the one I would open first. Checklist 125 asks the owner whether this is yours or a
link's.

**6 · Landscaping (owner questions, same day):** rover-only AND research-gated on 1.1.0,
both verified NEW against 1.0.7 — `EF-083`. No code touched; checklist row 7 gained the
Dozer Rover prerequisite; F115's "unverifiable" line closed. ⚠️ For your Pass G: the
landscaping control now needs a mid-tree tech on the test colony.
