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
   ⚠️ **It was stamped by 01 at `e2490f3` BEFORE this edit existed**, so its
   `SRC:` hash had to be re-taken. Confirm the re-stamp happened and that
   `bodycheck.py` was run either side — a stale pin here would read as GREEN
   while describing a body that no longer exists, which is the exact failure
   `bodycheck.py` was built to catch.
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
* **`C54`** (new entry, filed by me): 1.1.0's own
  `SavegameFixups.RemoveLeakedUpgradeModifiers` (`Building.lua:1313-1345`) ends on
  an unguarded `ipairs(leaked)` where `leaked` is `nil` for a container with no
  leaks. ⛔ **UNPROVEN** — whether `ipairs(nil)` raises in this engine was NOT
  established, only inferred from vanilla guarding `ipairs(x or empty_table)` in
  36 other places under `Lua/`. It needs a run, not a read.
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
